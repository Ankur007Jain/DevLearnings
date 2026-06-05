# Dynamic Flow in Production — FastAPI + Anthropic SDK

**Learned:** 2026-06-05 | **Project:** TravelAI (TravelPlannerV2)

---

## What it is

Dynamic flow = the AI decides the execution path at runtime, rather than you hardcoding it.

| | Static flow | Dynamic flow |
|--|-------------|--------------|
| **Who decides next step** | Developer (if/else in code) | The LLM (tool_use loop) |
| **Example** | Regex routes to Haiku vs Sonnet | Haiku classifies message complexity |
| **Example** | Single Claude call for trip plan | Claude calls `get_user_profile` → `get_liked_places` → then generates plan |

Three levels of dynamic flow, easiest to hardest:
1. **Dynamic routing** — AI picks which model/path to use
2. **Dynamic tool use** — AI gathers context via tools before answering
3. **Dynamic multi-agent** — parallel AI agents feed results to an orchestrator

---

## Phase 1 — Smart Model Router

Replace keyword regex with a cheap Haiku classification call:

```python
# services/model_router.py
async def classify_model(message: str, max_tokens: int, fallback=None) -> str:
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        resp = await client.messages.create(
            model=_HAIKU,
            max_tokens=5,        # only need one word back
            system="Reply with exactly one word: 'sonnet' or 'haiku'.",
            messages=[{"role": "user", "content": f"Query: {message[:500]}\n..."}],
        )
        token = resp.content[0].text.strip().lower()
        if "sonnet" in token: return _SONNET
        if "haiku" in token:  return _HAIKU
        return fallback(message, max_tokens) if fallback else _SONNET
    except Exception:
        return fallback(message, max_tokens) if fallback else _SONNET

# In streaming.py
model = await classify_model(message, max_tokens, fallback=_select_model_regex)
```

**Cost:** ~$0.0002 per message. Saves money by not sending complex plans to Haiku or simple Q&A to Sonnet.

---

## Phase 2 — Multi-step Tool Use Agent (streaming endpoint)

The agentic loop runs BEFORE the final streaming call. Only the final response streams to the client.

```python
# services/trip_planner_agent.py
async def run_trip_planner_agent(client, messages, api_system, max_tokens, ...):
    agentic_messages = list(messages)   # copy — don't mutate history
    loop_count = 0

    while loop_count < _MAX_LOOPS:     # safety guard (5)
        loop_count += 1
        try:
            response = await client.messages.create(
                model=_SONNET,
                max_tokens=1024,        # tool calls need few tokens — not the full budget
                system=api_system,
                messages=agentic_messages,
                tools=TRIP_PLANNER_TOOLS,
                tool_choice={"type": "auto"},
            )
        except Exception:
            break   # fall through to final stream with whatever context we have

        if response.stop_reason == "end_turn":
            agentic_messages.append({"role": "assistant", "content": response.content})
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    yield json.dumps({"type": "planning_step", "step": block.name})
                    result = execute_tool(block.name, block.input, ...)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            agentic_messages.append({"role": "assistant", "content": response.content})
            agentic_messages.append({"role": "user", "content": tool_results})
        else:
            break   # max_tokens or stop_sequence

    # Final streaming call with enriched context
    async with client.messages.stream(model=_SONNET, messages=agentic_messages, ...) as stream:
        async for chunk in stream.text_stream:
            yield json.dumps({"type": "chunk", "text": chunk})
```

---

## Phase 3 — Parallel Multi-agent (collab sessions)

```python
# services/collab_agents.py
async def run_collab_planner(client, participants, ...):
    # 1. Serialise ALL DB reads before asyncio.gather
    agent_inputs = [
        (name, fmt_profile(profiles[email]), fmt_liked(liked_map[email]))
        for email, name in participants
    ]

    # 2. Parallel Haiku agents (one per participant)
    tasks = [
        run_participant_preference_agent(client, name, persona_text, liked_text)
        for name, persona_text, liked_text in agent_inputs
    ]
    summaries_raw = await asyncio.gather(*tasks, return_exceptions=True)
    summaries = [s for s in summaries_raw if isinstance(s, str)]  # filter failures

    # 3. Sonnet orchestrator merges all preferences
    yield json.dumps({"type": "planning_step", "step": "merging_preferences"})
    orchestrator_messages = history[:-1] + [{
        "role": "user",
        "content": f"PARTICIPANT PREFERENCES:\n{chr(10).join(summaries)}\n\nUSER REQUEST: {user_message}"
    }]
    async with client.messages.stream(model=_SONNET, messages=orchestrator_messages, ...) as stream:
        ...
```

---

## Gotchas

### 1. Circular imports — don't cross-import services ↔ routers
`model_router.py` cannot import from `routers/streaming.py` (where `_SONNET`/`_HAIKU` constants live) — that creates a circular import. Solution: define the model ID strings in the service file itself.

### 2. Tool-call phase uses a small `max_tokens`
The tool-call loop should use `max_tokens=1024`, not the full value (e.g. 14000). Claude only needs to output a small JSON tool call, not an itinerary. Passing the full budget wastes reserved output buffer and can trigger premature `max_tokens` stop.

### 3. DB session scoping — pass serialised data, not the session
When using `asyncio.gather`, SQLAlchemy sessions are not safe for concurrent async access. Read all DB data **before** `asyncio.gather`, convert to plain strings, and pass those to the agents:
```python
# ❌ bad — passes db session to concurrent tasks
tasks = [agent(db, email) for email in emails]
await asyncio.gather(*tasks)

# ✓ good — serialise first, then parallelise AI calls
data = [(email, fmt_profile(db.query(...))) for email in emails]
tasks = [agent(profile_text) for _, profile_text in data]
await asyncio.gather(*tasks)
```

### 4. Agentic messages list ≠ persisted history
The `agentic_messages` list grows with tool call/result pairs during the loop. Only the **final text response** (`full_text`) gets saved to the DB — not the intermediate tool messages.

### 5. Prompt cache headers pass through correctly
The `api_system` list has `{"cache_control": {"type": "ephemeral"}}` on the base prompt. Pass this exact list to ALL Claude calls in the loop — tool calls AND the final stream. Cache hits accumulate across iterations.

### 6. "weekend" matches "week" in substring checks
```python
# ❌ bug: "weekend" contains "week"
if "week" in message.lower():
    return 14000  # wrongly triggers for "Plan a Nashville weekend"

# ✓ fix: use word boundary with negative lookahead
if re.search(r"\bweek(?!end)", message.lower()):
    return 14000
```

### 7. Tests: mock `messages.create` when the agentic path is active
If a test patches `anthropic.AsyncAnthropic` only for `messages.stream` and the agentic gate fires (e.g. "Plan a trip" with high token budget), the `messages.create` call in the tool loop raises because it's not mocked. Fix: add a `try/except` in the tool loop so failures fall through to the final stream instead of crashing.

### 8. SSE backward compatibility — new event types are safe
Add `planning_step` handling to the frontend event loop. Old clients silently skip unknown event types via `try/catch`, so no version flag is needed:
```typescript
} else if (event.type === "planning_step") {
  // no-op — or show a "thinking" indicator
}
```

---

## Quick reference

### Gate condition (when to use the agentic path)
```python
def is_trip_planning_request(message: str, max_tokens: int) -> bool:
    return max_tokens >= 6000 and bool(_PLANNING_KEYWORDS.search(message))
```

### Token accounting for multi-step calls
Yield a private `_final_usage` event from the agent generator, consume it in the caller:
```python
# In agent generator:
yield json.dumps({"type": "_final_usage", "usage": {
    "input_tokens": ..., "output_tokens": ..., ...
}})

# In streaming.py:
if event["type"] == "_final_usage":
    _agentic_usage = event["usage"]
    continue  # don't forward to client
```

### Safety guard
```python
_MAX_LOOPS = 5  # always cap the tool-call loop
```
