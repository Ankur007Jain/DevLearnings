# Prompt Caching + Context Tiering — Cutting Chat Cost Without Losing Quality

**Learned:** 2026-07-14 | **Project:** FinanceCompanion

> Companion to [dynamic-flow-in-production.md](dynamic-flow-in-production.md) (TravelAI) — that doc covers the
> tool-use loop and a Haiku-classifier model router in depth; this one covers what it doesn't: prompt-caching
> mechanics (the exact silent-failure gotcha), a context-tiering design for large enumerable data (a user's
> whole watchlist, not just "the current trip"), and a case for *removing* routing entirely instead of
> improving it, when the stakes justify it.

---

## 1. What It Is

A chat feature with access to a large, enumerable universe of context (a user's stock watchlist — 30-50+
tickers) hit three compounding problems at once, discovered by pulling **real production token/message
data**, not by guessing:

1. A per-message model router (regex-based) was silently downgrading real financial decisions to a cheaper
   model, because it judged model choice from the current message alone, with no notion that a two-word
   reply ("no", "1 more") is a continuation of an active buy/sell conversation.
2. Every chat message resent full-paragraph analysis for **every tracked ticker**, not just the one being
   discussed — averaging **~27,860 input tokens/message** in production.
3. `cache_control` was present in the code and looked correct, but **caching had never once engaged** —
   `cache_read_input_tokens` was 0 on every message, ever, with zero errors or warnings anywhere.

The fix that resolves all three at once: **tiered context (full depth for the one thing being discussed,
numeric summary for everything else) + a tool for on-demand deep-dive + caching the block that's actually
large, not the one that merely looks "static."**

### Before / After (real production numbers)

| | Before | After |
|---|---|---|
| Model for chat replies | Router downgraded ~13% of messages to Haiku, including real advice | Always the high-quality model |
| Context per message (2-ticker test case) | ~27,860 tokens avg (production, full watchlist) | 3,247 total tokens |
| `cache_read_tokens` | 0, always, every message | Message 2 in a conversation = message 1's `cache_write_tokens`, exactly |
| Asking about a non-focus ticker | Same shallow context as everything else | Tool fetches full depth on demand — identical to the focus ticker |

---

## 2. The Three-Tier Context Design

| Tier | When it applies | What's included | What's dropped |
|---|---|---|---|
| **Focus** (full dossier) | The ticker the conversation is scoped to | Full reasoning, bull/bear case, memory (past lessons), news, ripple effects, 5-day history, position/P&L | Nothing |
| **Compact** (numeric line) | Every *other* tracked item, but only inside a scoped conversation | Verdict, position/P&L, day change %, conviction score, RSI, 52-week range position, moving averages, entry/exit/stop targets, analyst target, upcoming events, an "important today" flag | Reasoning paragraph, memory, news, ripple effects — the prose |
| **Full** (unchanged) | A *general* (non-scoped) conversation | Same as Focus tier, for every item | Nothing — trimming here would defeat the point |

**Rule of thumb:** trim prose, keep numbers. Anything that's a single number or short label is cheap and
might legitimately be screened across many items at once ("which position is red today," "any stops close
to triggering," "what earnings are coming up this week") — keep it ambient in every message. Anything that's
a paragraph is expensive per-token and is only valuable once the user is actually asking about that specific
item — move it behind a tool call instead of paying for it on every unrelated message.

**The one case where trimming is wrong:** a general/unscoped conversation. That's *exactly* the conversation
type meant to synthesize across the whole portfolio — trimming it removes the one thing it exists to do. Gate
the trim on "is there a specific subject in focus," not on cost alone.

---

## 3. File Map (FinanceCompanion backend)

```
backend/
├── services/
│   ├── model_router.py       ← simplified to a token-size estimator only; model
│   │                            selection removed entirely (see §5)
│   └── prompt_builder.py     ← the tiering logic lives here
│       ├── _format_analysis_deep()      full dossier — focus ticker
│       ├── _format_analysis_compact()   NEW — numeric one-liner, non-focus tickers
│       ├── _format_analysis()           full paragraph — general chat only, unchanged
│       ├── build_ticker_dossier()       NEW — shared by focus-ticker path AND the
│       │                                  tool executor (see §6) — one function,
│       │                                  so quality can't drift between entry paths
│       └── build_system_prompt()        orchestrates: focus gets deep dossier, others
│                                          get compact lines IFF ticker-scoped
└── routers/
    └── streaming.py           ← SSE endpoint: cache_control on both system blocks,
                                   tool definitions + dispatch loop, hardcoded model
```

---

## 4. Prompt Caching — the mechanics, and the exact silent-failure gotcha

### The concept

Anthropic prompt caching: mark a content block with `cache_control: {"type": "ephemeral"}`. On a cache hit
(identical prefix content, within the TTL — default 5 minutes), you pay roughly **10% of normal input token
price** for that block instead of full price.

### The gotcha

```python
api_system = [
    {"type": "text", "text": base_prompt, "cache_control": {"type": "ephemeral"}},  # ~500 tokens
]
if dynamic_context:
    api_system.append({"type": "text", "text": dynamic_context})   # ~3k–28k tokens, NO cache_control
```

This *looks* correct. `cache_control` is set, the request succeeds normally, nothing errors. But Anthropic
requires a **minimum token count per cache breakpoint** before it will actually create a cache entry —
roughly **1024 tokens for Sonnet/Opus, 2048 for Haiku**. Below that threshold, `cache_control` is silently
ignored: no error, no warning, the API just treats the block as uncached, forever.

Here, the block that *was* marked cacheable (`base_prompt`, the "static" role/rules text) was only ~500
tokens — permanently below the threshold no matter what changed elsewhere. Meanwhile the block that was
genuinely large and genuinely repeated across messages (`dynamic_context`, rebuilt fresh from the DB every
call but often byte-identical between messages sent minutes apart) had no `cache_control` at all — probably
because "dynamic" *sounds* like the wrong thing to cache.

**Net effect:** `cache_read_input_tokens` was 0 on every production message, ever, for months, with no
error surface anywhere pointing at it.

### How to detect this class of bug

Query stored usage data across every historical message for a chat feature:

```sql
SELECT model_used, AVG(cache_read_tokens), AVG(cache_write_tokens)
FROM messages GROUP BY model_used;
```

If both are always zero, caching isn't engaging — full stop, regardless of whether `cache_control` appears
correct in the request-building code. The code review would have passed; only the data caught it.

### The fix

Mark whichever block(s) are actually **large enough** cacheable — not whichever one *feels* static:

```python
api_system = [
    {"type": "text", "text": base_prompt, "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": dynamic_context, "cache_control": {"type": "ephemeral"}},  # the fix
]
```

"Dynamic" doesn't mean "don't cache" — it means "rebuilt fresh every call." If the underlying data hasn't
changed, the freshly-rebuilt string is byte-identical to the last one, which is exactly what a cache wants.
There's no staleness risk: you're not caching a value on purpose to reuse later — you're recognizing that a
freshly-computed value often *equals* the previous freshly-computed value, and letting the API skip
re-billing for that overlap.

### How to verify the fix actually works

Send two messages in the same conversation within the 5-minute TTL and check:

```
message 1: cache_write_tokens  ==  message 2: cache_read_tokens
```

A clean, unambiguous signal. Live example from this session:

```
message 1:  input=328   output=505   cache_read=0      cache_write=2919
message 2:  input=842   output=193   cache_read=2919    cache_write=0
```

---

## 5. Model Routing — when to remove it instead of improving it

[dynamic-flow-in-production.md §4](dynamic-flow-in-production.md) documents a good general pattern: replace
a brittle regex router with a cheap Haiku *classifier* call that decides Sonnet vs. Haiku per message. That's
the right move when misrouting is low-stakes (wrong tool call, slightly worse phrasing, wasted tokens).

It assumes misrouting is recoverable. In a domain where the wrong model choice means a user receives
financial (or medical, legal, etc.) advice from a less capable model, evaluate differently — and here, a
classifier wasn't even tried, because the evidence pointed somewhere more decisive.

### The evidence

Production logs, each Haiku-routed reply traced back to the exact user message that triggered it:

| User sent | Haiku replied with |
|---|---|
| `"mrk"` | **"MRK: Hold, don't sell today."** |
| `"no"` | "**Then don't add today.** Good instinct. Wait for..." |
| `"1 more"` | "**Good call.** Adding 1 more at $136.44 means..." |

The router (message length + keyword regex) had no notion that `"no"` was message #4 of an *active*
financial decision conversation — it saw a two-word message with no matching keyword, downgraded to the
cheap model, and the cheap model gave real advice anyway.

### The decision rule

| Condition | Action |
|---|---|
| Misrouting = wrong tool call, wasted tokens, slightly worse phrasing | **Improve the router** — classifier, better regex, conversation-aware heuristics |
| Misrouting = advice a user might act on with money/health/legal consequences, **and** the savings from the cheap path are small | **Remove routing** — always use the high-quality model for that feature |

Here: only ~13% of chat messages were routing to Haiku, averaging 229 output tokens each — trivial savings
against real risk. The fix was to hardcode the high-quality model for the whole feature, and keep the cheap
model *only* for genuinely separate, low-stakes jobs the user never sees as "the app's opinion" (title
generation, background field rewrites).

**Rule of thumb:** don't spend engineering effort making a risky heuristic slightly less risky when the
thing it's routing away from costs almost nothing in the first place. Measure the actual savings before
defending the router.

---

## 6. The Deep-Dive Tool — parity via one shared builder function

### The problem a naive trim creates

If non-focus items get trimmed to compact summaries, what happens when the user asks about one of them
directly? Two bad options:

- **(a)** Answer from the compact summary alone — degraded quality on exactly the question being asked.
- **(b)** Regex-match the user's message for known symbols and swap in full context — brittle, misses "the
  EV maker," "Nvidia," typos, or anything not in a fixed symbol list.

### The fix: a tool, and one function for both entry paths

```python
def build_ticker_dossier(ticker: str, db: Session, user_email: str) -> str:
    """Full institutional dossier for any ticker — same content whether it's the
    conversation's initial focus or one the user pivots to mid-chat via the
    get_stock_analysis tool, so quality never depends on which path got you here."""
    ...
```

Called from **two** places:
1. `build_system_prompt()` — for the ticker the conversation is originally scoped to.
2. The tool dispatcher in `streaming.py` — when the model calls `get_stock_analysis(ticker)` mid-conversation.

Because both paths call the *same* function, there's no way for a "pivoted-to" item to get a lesser
experience than the "started-with" item. This is the single most important design choice in the whole
pattern — it's tempting to write a separate, simpler "tool response" formatter, and that's exactly how
quality silently drifts between paths as one gets updated and the other doesn't.

### Tool definition (Anthropic tool-use schema)

```python
_GET_STOCK_ANALYSIS_TOOL = {
    "name": "get_stock_analysis",
    "description": (
        "Get the full analysis for a ticker — verdict, conviction, bull/bear case, reasoning, "
        "news, ripple effects, memory of past lessons, and 5-day history. Use this when the user "
        "asks specifically about a ticker other than the one in focus (you only have a compact "
        "numeric summary for those). Works for any ticker, not just ones the user tracks. Prefer "
        "this over web_search for anything we've already analyzed — it's our own vetted data."
    ),
    "input_schema": {
        "type": "object",
        "properties": {"ticker": {"type": "string", "description": "The stock ticker symbol, e.g. NVDA"}},
        "required": ["ticker"],
    },
}
```

### System-prompt tool-choice guidance matters

Adding the tool isn't enough on its own — tell the model explicitly when to prefer it over other tools
(here, `web_search`), or it may default to a generic web search over your own structured, vetted data:

```
Other tracked tickers are given as compact figures only — no reasoning or memory. If the user
asks about one of them specifically, call get_stock_analysis(ticker) to get the same full depth
as the focus ticker rather than guessing from the summary alone. It works for any ticker, not
just ones the user tracks. Use web_search only for what get_stock_analysis can't answer.
```

The tool-use loop mechanics (detect `tool_use` block → execute → feed `tool_result` back → continue
streaming) are the same pattern documented in
[dynamic-flow-in-production.md §5](dynamic-flow-in-production.md) — not repeated here.

---

## 7. End-to-End Trace

**Scenario:** user is in a conversation scoped to CTSH, then asks "what about NVDA, is it a better buy?"

```
1. Frontend POSTs to /conversations/{id}/messages/stream

2. build_system_prompt(user_email, db, conv.ticker="CTSH")
   ├── CTSH: full dossier via build_ticker_dossier() — reasoning, bull/bear, memory, history
   └── every OTHER watchlisted ticker (incl. NVDA): one compact numeric line

3. api_system = [
     {static role/rules block,   cache_control: ephemeral},
     {dynamic per-user context,  cache_control: ephemeral},   ← both cacheable now
   ]

4. First streaming call: model=sonnet, tools=[web_search, get_stock_analysis]
   → Claude's compact NVDA line isn't enough to answer confidently
   → emits a tool_use block: get_stock_analysis(ticker="NVDA")

5. Backend tool loop detects content_block_start/delta/stop, accumulates tool_uses
   → stop_reason == "tool_use" → dispatch:
       result = build_ticker_dossier("NVDA", db, user.email)   ← SAME function as step 2's CTSH call
   → tool_result appended to messages; loop continues

6. Second streaming call (api_system unchanged → hits cache from step 3 again)
   → Claude now has full NVDA depth, produces a real comparison

7. persist() saves the assistant message with usage SUMMED across both stream calls
   (input/output/cache_read/cache_write)
```

**Live-verified result** (real call, this session): the reply included a full comparison table — NVDA's
revenue growth (85.2%), margin (63.0%), ROE, forward P/E, MA200, earnings date, entry/stop/target — not a
degraded one-liner answer. Token accounting for that call: `input=3515, cache_read=5838, cache_write=0` —
the base context still hit cache even inside the tool-call round trip.

---

## 8. SSE Event Contract (streaming.py)

| Event | Direction | Purpose |
|---|---|---|
| `{"type": "chunk", "text": "..."}` | server → client | Streamed text token |
| `{"type": "tool_start", "tool": "get_stock_analysis"}` | server → client | UI feedback while a tool runs |
| `{"type": "tool_result", "query": "NVDA"}` | server → client | What the tool was asked (ticker or search query) |
| `{"type": "system_prompt", "text": "..."}` | server → client | Debug-only, gated to a single admin email |
| `{"type": "error", "message": "..."}` | server → client | Stream failed |

---

## 9. Gotchas & Lessons Learned — testing async streaming code with `unittest.mock`

Writing real tests for this (rather than trusting the mocked-but-never-actually-invoked helper that already
existed in the codebase) surfaced five sharp, easy-to-repeat `unittest.mock` gotchas.

### G1 — `MagicMock(name="x")` does not set `.name`

```python
# ❌ WRONG — `name` is a reserved Mock constructor kwarg (sets the mock's debug repr)
m = MagicMock(name="get_stock_analysis")
m.name   # returns a new auto-generated child Mock, NOT "get_stock_analysis"

# ✓ RIGHT — assign the attribute directly, after construction
m = MagicMock()
m.name = "get_stock_analysis"
```
This one is nasty because it fails silently — no exception, just wrong data flowing through your test.

### G2 — assigning a plain function to `mock.__aiter__` gets called as a bound method

```python
# ❌ WRONG
async def _aiter():
    for e in events:
        yield e
stream_ctx.__aiter__ = _aiter
# `async for x in stream_ctx:` → TypeError: _aiter() takes 0 positional arguments but 1 was given

# ✓ RIGHT — unittest.mock invokes assigned dunders AS bound methods (self passed implicitly)
async def _aiter(_self):
    for e in events:
        yield e
stream_ctx.__aiter__ = _aiter
```

### G3 — a plain `MagicMock()` is not awaitable; async dunders need `AsyncMock`

```python
# ❌ WRONG — async with raises deep inside the generator
stream_ctx.__aenter__ = MagicMock(return_value=stream_ctx)

# ✓ RIGHT
stream_ctx.__aenter__ = AsyncMock(return_value=stream_ctx)
stream_ctx.__aexit__  = AsyncMock(return_value=False)
```
**Why this is dangerous, not just wrong:** `Mock.call_args` is captured *synchronously at call time*, before
the async body ever runs. So a test asserting `mock.stream.call_args.kwargs["model"] == "sonnet"` can **pass
completely legitimately** even though `async with` crashed one line later and the rest of the function body
never executed. This is exactly what happened here — an existing, unused mock helper in the codebase had
this bug and nothing ever caught it, because it was never actually invoked by a real test.

### G4 — shared on-disk test DB + "realistic" seed data = order-dependent flakiness

If tests share one SQLite file across a whole pytest session (no per-test rollback), seeding a real-looking
ticker symbol like `"NVDA"` in a new test file can silently collide with another test file's seed data for
the same symbol and date. A query like "the latest analysis for this ticker" then non-deterministically
returns whichever row happened to insert last, depending on test execution order.

```python
# ❌ collides with 8 other test files that already seed "NVDA"
db_session.add(StockAnalysis(ticker="NVDA", analysis_date=date.today(), ...))

# ✓ use an obviously-fake, prefixed symbol scoped to this test file
db_session.add(StockAnalysis(ticker="ZPIVOT", analysis_date=date.today(), ...))
```
Passes in isolation, fails (or worse, silently returns the wrong data) only when run as part of the full
suite — always run the *whole* suite, twice, before trusting a new test.

### G5 — `patch(..., wraps=fn)` has no `spy_return` — that's a `pytest-mock` feature

```python
# ❌ AttributeError: 'function' object has no attribute 'spy_return'
with patch("module.fn", wraps=real_fn) as spy:
    ...
    assert "expected" in spy.spy_return   # spy_return only exists on pytest-mock's mocker.spy()

# ✓ wrap manually and capture the real return value yourself
captured = []
def _spy(*args, **kwargs):
    result = real_fn(*args, **kwargs)
    captured.append(result)
    return result
with patch("module.fn", side_effect=_spy):
    ...
assert "expected" in captured[0]
```

---

## 10. When to Use This Pattern

| Situation | Approach |
|---|---|
| Agent has a large, enumerable set of "things it might discuss" (watchlist, saved places, tracked items) | Tiered context: full depth for the current subject, compact summary for the rest |
| User might ask a portfolio/collection-wide question mid-conversation | Keep every *number* in the compact tier — only drop prose |
| User might pivot to discuss a different specific item | Add a tool, backed by the *same function* the original focus item uses |
| A repeated context block feels "dynamic" so you skip `cache_control` | Cache it anyway if it's large and often identical between calls — dynamic ≠ uncacheable |
| `cache_control` is present but you've never checked real usage data | Query it — a correct-looking implementation can silently do nothing |
| A router downgrades model quality on short/ambiguous messages in a high-stakes domain | Check whether the savings justify the risk; if not, remove the router rather than patch it |
| Writing tests for SSE/streaming code with `unittest.mock` | Use `AsyncMock` for every async dunder (`__aenter__`, `__aexit__`), and give bound-method dunders a dummy `self` param |

---

## 11. Quick Reference

```python
# Cache BOTH the static and dynamic system blocks if the dynamic one is large enough
# (Anthropic minimum: ~1024 tokens Sonnet/Opus, ~2048 Haiku, per breakpoint)
api_system = [
    {"type": "text", "text": static_block,  "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": dynamic_block, "cache_control": {"type": "ephemeral"}},
]

# Verify caching is real, don't trust the code alone
SELECT model_used, AVG(cache_read_tokens), AVG(cache_write_tokens) FROM messages GROUP BY model_used;
# want: message N's cache_write_tokens == message N+1's cache_read_tokens (same conversation, <5min apart)

# Three-tier context rule of thumb
#   focus item        -> full depth, always
#   other items       -> numbers only (position, verdict, targets, flags) — never prose
#   general/no-focus  -> full depth for everything (don't trim — this IS the synthesis case)

# Tool-parity rule
#   the function that builds "deep dive" context must be the SAME function whether it's
#   called for the initial focus item or via a tool call mid-conversation — never two paths

# Mock gotchas checklist for async streaming tests
#   1. MagicMock(name=...) does NOT set .name — assign it after construction
#   2. mock.__aiter__ = fn  ->  fn needs a dummy self param (called as bound method)
#   3. async dunders (__aenter__/__aexit__) need AsyncMock, not MagicMock
#   4. shared on-disk test DB -> use obviously-fake, file-scoped ticker/id symbols
#   5. patch(wraps=fn) has no .spy_return -> wrap with side_effect and capture manually
```
