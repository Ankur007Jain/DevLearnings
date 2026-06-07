# Dynamic Flow — Concept, Architecture & Implementation

**Learned:** 2026-06-05 | **Updated:** 2026-06-07  
**Project:** TravelAI (TravelPlannerV2) | **Branch:** feature/dynamic-flow

---

## 1. What Is Dynamic Flow?

In a **static flow**, *you* (the developer) decide every step at code-write time:

```
user message
   → if "plan" in message: call Sonnet
   → else: call Haiku
   → return response
```

In a **dynamic flow**, *the LLM* decides what steps to take at runtime:

```
user message
   → LLM: "I need user profile and liked places before I can answer"
   → LLM calls get_user_profile() → gets data
   → LLM calls get_liked_places() → gets data
   → LLM: "Now I have enough context. Here's the itinerary."
   → return response
```

The LLM is no longer just a text generator — it's an **agent** that plans, fetches, and decides.

---

## 2. Three Levels (Easiest → Hardest)

| Level | Name | Who decides | Example in TravelAI |
|-------|------|-------------|---------------------|
| 1 | **Dynamic Routing** | LLM picks model/path | Haiku classifies: "use Sonnet or Haiku?" |
| 2 | **Tool Use Loop** | LLM fetches context via tools | Claude calls `get_user_profile` before writing plan |
| 3 | **Multi-Agent** | Parallel agents feed an orchestrator | Haiku agents per participant → Sonnet merges |

TravelAI implements all three — they compose on top of each other.

---

## 3. File Map

```
backend/
├── services/
│   ├── model_router.py          ← Phase 1: AI model classifier
│   ├── trip_planner_tools.py    ← Phase 2: tool schemas + executor + gate
│   ├── trip_planner_agent.py    ← Phase 2: agentic loop
│   └── collab_agents.py         ← Phase 3: parallel Haiku + Sonnet orchestrator
└── routers/
    └── streaming.py             ← wires all three phases into the SSE endpoint

app/chat/
├── useStreamingChat.ts          ← handles planning_step SSE events
└── ChatClient.tsx               ← shows "thinking" phrases during agent steps
```

---

## 4. Phase 1 — Smart Model Router

### Concept

Replace a brittle regex keyword check with a Haiku classification call.  
Haiku costs ~$0.0002/call — cheap enough to always run.

### Before (static regex)

```python
# streaming.py (old)
def _select_model(message: str, max_tokens: int) -> str:
    lower = message.lower()
    if any(k in lower for k in ["plan", "itinerary", "road trip"]):
        return "claude-sonnet-4-6"
    return "claude-haiku-4-5-20251001"
```

Problems: "plan a quick snack" → Sonnet (overkill). "What does itinerary mean?" → Sonnet (waste).

### After (dynamic routing)

```python
# services/model_router.py
async def classify_model(message: str, max_tokens: int, fallback=None) -> str:
    resp = await client.messages.create(
        model=_HAIKU,
        max_tokens=5,        # only need ONE word back
        system="Reply with exactly one word: 'sonnet' or 'haiku'.",
        messages=[{"role": "user", "content": f"Query: {message[:500]}"}],
    )
    token = resp.content[0].text.strip().lower()
    if "sonnet" in token: return _SONNET
    if "haiku" in token:  return _HAIKU
    return fallback(message, max_tokens) if fallback else _SONNET  # safe default
```

```python
# streaming.py — wiring
async def _resolve_model(message: str, max_tokens: int) -> str:
    return await classify_model(message, max_tokens, fallback=_select_model_regex)
#                                                    ↑ regex is now the fallback only
```

### Key Design Decisions

- `_select_model_regex` still exists as fallback — if Haiku call fails, we don't crash
- `max_tokens=5` — Claude only needs to say "sonnet" or "haiku", nothing more
- Model IDs are defined inside `model_router.py` — **not imported from streaming.py** (would create circular import)

---

## 5. Phase 2 — Agentic Trip Planner (Tool Use Loop)

### Concept

When a user asks for a multi-day plan, Claude needs:
- The user's travel profile (preferences, persona)
- Their liked/saved places (especially near the destination)
- Current trip context (origin, destination, travel style)

Instead of blindly injecting all this into the prompt every time, we let **Claude ask for what it needs**.

### Gate Condition

Not every message needs the agentic path — it adds latency. The gate checks two things:

```python
# services/trip_planner_tools.py
_PLANNING_KEYWORDS = re.compile(
    r"\b(plan|itinerary|schedule|day.by.day|route|road trip|multi.day|week(?!end))\b",
    re.IGNORECASE,
)

def is_trip_planning_request(message: str, max_tokens: int) -> bool:
    return max_tokens >= 6000 and bool(_PLANNING_KEYWORDS.search(message))
    #      ↑ short questions get small token budgets — skip them
```

`max_tokens >= 6000` because `_estimate_max_tokens` gives big budgets only to complex requests. This double-gates on both message content AND expected response length.

### Tool Schemas

```python
# services/trip_planner_tools.py
TRIP_PLANNER_TOOLS = [
    {
        "name": "get_user_profile",
        "description": "Retrieve the user's saved travel preferences and persona",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_liked_places",
        "description": "Retrieve places the user has liked/saved",
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "Filter by city/region"}
            },
        },
    },
    {
        "name": "get_trip_context",
        "description": "Retrieve origin, destination, travel style from conversation",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
]
```

### The Agentic Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC LOOP (max 5x)                    │
│                                                             │
│  messages.create(tools=TRIP_PLANNER_TOOLS)                  │
│        │                                                    │
│        ├─ stop_reason == "end_turn"  ──────────────────┐   │
│        │   Claude has enough context                    │   │
│        │                                                │   │
│        └─ stop_reason == "tool_use"                     │   │
│            │                                            │   │
│            ├── yield planning_step event (UI feedback)  │   │
│            ├── execute_tool(block.name, block.input)    │   │
│            ├── append tool_result to messages           │   │
│            └── loop again ──────────────────────────┐   │   │
│                                                     │   │   │
└─────────────────────────────────────────────────────┴───┴───┘
                                                      │
                                              FINAL STREAM
                                    messages.stream(model=Sonnet,
                                      messages=enriched_agentic_messages)
                                              │
                                    yield chunk events → SSE → client
```

```python
# services/trip_planner_agent.py (simplified)
async def run_trip_planner_agent(client, messages, api_system, max_tokens, ...):
    agentic_messages = list(messages)  # copy — never mutate the original history
    loop_count = 0

    while loop_count < _MAX_LOOPS:    # _MAX_LOOPS = 5
        loop_count += 1
        try:
            response = await client.messages.create(
                model=_SONNET,
                max_tokens=1024,       # ← small! tool calls are tiny JSON, not essays
                system=api_system,
                messages=agentic_messages,
                tools=TRIP_PLANNER_TOOLS,
                tool_choice={"type": "auto"},
            )
        except Exception:
            break  # fall through to final stream with whatever context we have

        if response.stop_reason == "end_turn":
            agentic_messages.append({"role": "assistant", "content": response.content})
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    yield json.dumps({"type": "planning_step", "step": block.name})
                    result = execute_tool(block.name, block.input, user_email, conv, profile, liked)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            agentic_messages.append({"role": "assistant", "content": response.content})
            agentic_messages.append({"role": "user",      "content": tool_results})
        else:
            break  # stop_sequence or other unexpected stop

    # Final streaming call — Claude now has enriched context in agentic_messages
    async with client.messages.stream(
        model=_SONNET, max_tokens=max_tokens,
        system=api_system, messages=agentic_messages,
    ) as stream:
        async for chunk in stream.text_stream:
            yield json.dumps({"type": "chunk", "text": chunk})

    # Emit token counts for accounting in streaming.py
    final_msg = await stream.get_final_message()
    yield json.dumps({"type": "_final_usage", "usage": {
        "input_tokens":  final_msg.usage.input_tokens,
        "output_tokens": final_msg.usage.output_tokens,
        ...
    }})
```

### Wiring Into streaming.py

```python
# routers/streaming.py — inside the SSE generate() function
if is_collab and is_trip_planning_request(message, max_tokens):
    # Phase 3 (multi-agent collab)
    gen = run_collab_planner(...)
elif is_trip_planning_request(message, max_tokens):
    # Phase 2 (single-user agentic)
    gen = run_trip_planner_agent(...)
else:
    # Simple stream (no tools)
    gen = simple_stream(...)

async for raw in gen:
    event = json.loads(raw)
    if event["type"] == "_final_usage":
        _agentic_usage = event["usage"]  # capture for token accounting
        continue                          # don't forward to client
    yield f"data: {raw}\n\n"
```

---

## 6. Phase 3 — Multi-Agent Collab Planner

### Concept

When 2+ people plan a trip together in a collab session, they have different preferences.  
Instead of Claude trying to infer everyone's preferences from one prompt, we run:

- **N Haiku agents** (one per participant) — each reads one person's profile → outputs 3-4 bullet preferences
- All run **simultaneously** via `asyncio.gather`
- **Sonnet orchestrator** reads all summaries → writes one plan that satisfies everyone

```
Participant A profile ──→ [Haiku agent A] ──┐
Participant B profile ──→ [Haiku agent B] ──┤──→ [Sonnet orchestrator] ──→ SSE stream
Participant C profile ──→ [Haiku agent C] ──┘
         (parallel, ~same time)                    (sequential, after all done)
```

### Critical: Serialise DB Reads Before asyncio.gather

SQLAlchemy sessions are **not safe** for concurrent async access. Read everything first, then parallelise.

```python
# services/collab_agents.py

# ❌ WRONG — passes db session into concurrent coroutines
tasks = [agent(db, email) for email in participants]
await asyncio.gather(*tasks)

# ✓ RIGHT — read from DB first, convert to plain strings, then parallelise
agent_inputs = [
    (name, fmt_profile(profiles[email]), fmt_liked(liked_map[email]))
    for email, name in participants
]
tasks = [
    run_participant_preference_agent(client, name, persona_text, liked_text)
    for name, persona_text, liked_text in agent_inputs
]
summaries_raw = await asyncio.gather(*tasks, return_exceptions=True)
summaries = [s for s in summaries_raw if isinstance(s, str)]  # filter failed agents
```

### Gate Condition

```python
# streaming.py
is_collab = bool(collab_participants)  # 2+ people in the session
is_planning = is_trip_planning_request(message, max_tokens)

if is_collab and is_planning:
    # multi-agent path
```

---

## 7. End-to-End Request Trace

**Request:** "Plan a 5-day trip to Tokyo for me and Sarah"  
**Collab session:** active (2 participants)

```
1. POST /stream
   ├── _resolve_model() → Haiku classifies → "sonnet"
   ├── _estimate_max_tokens("Plan a 5-day...") → 14000
   └── is_trip_planning_request() → True, is_collab → True

2. run_collab_planner() starts
   ├── DB reads: profiles[user], profiles[sarah], liked[user], liked[sarah]
   │     (serialised BEFORE asyncio.gather)
   ├── asyncio.gather([
   │     run_participant_preference_agent("Ankur", profile_text, liked_text),
   │     run_participant_preference_agent("Sarah", profile_text, liked_text),
   │   ])
   │   → Both Haiku calls fire simultaneously (~500ms each)
   │   → Returns: ["Ankur: adventure, budget, sushi...", "Sarah: relaxed, luxury, museums..."]
   ├── yield {"type": "planning_step", "step": "merging_preferences"}
   │     → client shows "Merging everyone's travel styles..."
   └── Sonnet orchestrator stream with merged preferences in context
         → yield {"type": "chunk", "text": "..."} × N

3. SSE events received by client:
   {"type": "planning_step", "step": "merging_preferences"}  ← thinking indicator
   {"type": "chunk", "text": "Day 1: Arrive in Tokyo..."}    ← streamed text
   {"type": "chunk", "text": " Check into hotel..."}
   ...
   {"type": "done"}
```

---

## 8. SSE Event Contract

| Event type | Direction | Purpose |
|------------|-----------|---------|
| `chunk` | agent → client | Streamed text token |
| `planning_step` | agent → client | UI feedback ("gathering context") |
| `_final_usage` | agent → streaming.py | Token counts (internal, never forwarded) |
| `done` | streaming.py → client | Stream complete |
| `error` | streaming.py → client | Something failed |

Frontend handles `planning_step` as a no-op (or shows a thinking phrase):

```typescript
// app/chat/useStreamingChat.ts
} else if (event.type === "planning_step") {
  // no UI change — ChatClient already shows rotating thinking phrases
}
```

---

## 9. Gotchas & Lessons Learned

### G1 — Tool-call loop uses small `max_tokens`

```python
# ✓ correct
response = await client.messages.create(max_tokens=1024, ...)

# ❌ wrong — wastes output buffer, can trigger early stop
response = await client.messages.create(max_tokens=14000, ...)
```

Tool calls are small JSON blobs. `max_tokens=1024` is plenty. The full budget is for the final streaming call.

### G2 — `agentic_messages` is NOT the persisted history

The tool call/result pairs are only in `agentic_messages` (in-memory, for this request). Only the **final text** (`full_text`) gets saved to the DB via `save_message()`. Don't save `agentic_messages` directly.

### G3 — Circular imports: define model IDs in the service file

`model_router.py` cannot import `_SONNET`/`_HAIKU` from `streaming.py` — that creates a circular import. Each service file defines its own model ID strings.

### G4 — "weekend" matches "week"

```python
# ❌ "Plan a Nashville weekend" triggers 14000 tokens
if "week" in lower: return 14000

# ✓ word boundary + negative lookahead
if re.search(r"\bweek(?!end)", lower): return 14000
```

### G5 — Prompt cache passes through all loop iterations

`api_system` has `cache_control: ephemeral` on the base prompt. Pass this **exact list** to every `messages.create` call in the loop — not just the final stream. Cache hits accumulate across iterations.

### G6 — Graceful fallback on agentic errors

Wrap `messages.create` in `try/except` in the tool loop. On any exception, `break` and fall through to the final stream with whatever `agentic_messages` we have. This means a partial tool loop is better than a crashed response.

### G7 — Token accounting with `_final_usage`

Multi-step calls produce token counts only from the final stream. The tool loop calls also consume tokens. Solution: emit a private `_final_usage` event from the agent generator, capture it in `streaming.py`, and pass it to `save_message()` instead of letting the caller try to read the stream's usage directly.

---

## 10. When to Use Each Phase

| Trigger | Use |
|---------|-----|
| Any message (always) | Phase 1 — smart model router |
| `max_tokens >= 6000` AND planning keywords | Phase 2 — agentic tool loop |
| Phase 2 conditions AND collab session active | Phase 3 — multi-agent collab |

All three phases compose — Phase 3 always includes Phase 1's model selection, and Phase 3's gate checks the same `is_trip_planning_request` predicate as Phase 2.

---

## 11. Quick Reference

```python
# Gate — should we use agentic path?
is_trip_planning_request(message, max_tokens)  # True when tokens ≥ 6000 AND planning keywords

# Phase 1
model = await classify_model(message, max_tokens, fallback=_select_model_regex)

# Phase 2
async for raw in run_trip_planner_agent(client, messages, api_system, max_tokens, ...):
    event = json.loads(raw)
    # handle: chunk, planning_step, _final_usage

# Phase 3
async for raw in run_collab_planner(client, participants, messages, ...):
    event = json.loads(raw)
    # same event types

# Safety constants
_MAX_LOOPS = 5          # cap the tool-call loop
max_tokens = 1024       # for tool-call phase (not the full budget)
```
