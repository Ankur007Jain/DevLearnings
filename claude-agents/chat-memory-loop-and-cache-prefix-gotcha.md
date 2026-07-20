# Chat Memory Loop — Cross-Conversation Retrieval, User Learnings, and the Prompt-Cache Prefix Gotcha

**Learned:** 2026-07-19 | **Project:** FinanceCompanion

> Part 2 of the FinanceCompanion caching arc — [prompt-caching-and-context-tiering.md](prompt-caching-and-context-tiering.md)
> (Part 1) covers the tiered-context design and the *size-threshold* cache gotcha (a block too small to ever
> cache). This one covers a **different, sharper** cache gotcha (exact-prefix matching, not size), plus the
> memory system built on top of it: durable cross-conversation memory, two tool-gated "remember this" scopes,
> extended thinking, and four real production bugs found while shipping it (PRs #83–#90, 2026-07-18/19).

---

## 1. What It Is

Two problems, evidenced from real production data, not guessed at:

1. **No memory across conversations.** A user with 18+ substantial ticker-scoped conversations (MRK 38
   messages, BIOA/IBB 22, LLY 20…) asked directly whether the AI could see a past conversation — it couldn't.
   Each conversation was walled off from every other, including the user's own.
2. **Uncapped history was a live collision course, not just rising cost.** A real 116-message conversation
   resent its *entire* history every turn with no cap: 68x cost growth per turn (1.8K → 119K uncached input
   tokens), and by message 57 alone that's 60.8% of Sonnet's 200K context window.

The fix is four pieces, each scoped to a specific evidenced problem — not a general "add memory" feature:

| Piece | Fixes | Mechanism |
|---|---|---|
| Capped live history (`_MAX_LIVE_HISTORY=20`) | Cost/context-window blowup | Only the most recent N messages resent per turn |
| `get_chat_history` tool | The safety valve for #1, and cross-conversation memory | Verbatim SQL retrieval — never summarized |
| `save_learning` / `delete_learning` + `user_learnings` table | Durable facts about the *user* | Two scopes: global (every conversation) or ticker-scoped |
| `flag_stock_correction` | Factual corrections about the *ticker* | Writes to the same shared `StockMemory` the nightly Verdict Agent reads |

**Deliberately not built:** passive/automatic transcript summarization (an LLM deciding what a conversation
"meant" can misattribute conclusions — real hallucination risk) and a vector database for retrieval
(unnecessary — conversations are already ticker-tagged, so exact SQL filtering covers the actual need).
Verbatim-or-nothing was the design constraint throughout.

---

## 2. File Map

```
backend/
├── models.py
│   ├── Conversation.ticker          existing — what makes get_chat_history's SQL filter a plain query
│   ├── UserLearning                 NEW — user_email, learning, ticker (nullable = global), source_conversation_id
│   └── ToolCall                     NEW — logs every tool invocation (name, query, succeeded) — closed a real
│                                       observability gap; previously the only way to know tool usage was
│                                       inferring it from message TEXT
├── routers/
│   ├── streaming.py                 tool definitions + dispatch loop + the cache-topology assembly (§4)
│   ├── learnings.py                 NEW — REST API (list/edit/delete) for the /memory settings page,
│   │                                   separate from the chat tool path
│   └── jobs.py                      NEW — POST /jobs/admin/user-learnings, test-only seeding endpoint
├── services/
│   ├── prompt_builder.py
│   │   ├── build_user_learnings_block()   global learnings — own cache block (§4)
│   │   ├── _ticker_learnings_section()    ticker-scoped learnings — folded into build_ticker_dossier()
│   │   └── build_ticker_dossier()         unchanged signature, now also appends correlations + ticker learnings
│   ├── model_router.py
│   │   ├── _should_use_extended_thinking()  NEW — narrow keyword trigger (§6)
│   │   └── _SONNET = "claude-sonnet-5"      pinned with a re-check-by-date comment (§10)
│   └── stock_memory.py
│       └── append_lesson()             shared write path for flag_stock_correction AND the weekly
│                                          Scorecard — trim-oldest-first fix lives here (§7, bug #1)
├── main.py
│   └── _migrate_db()                   self-healing ALTER TABLE guards, one per column (§7, bug #3)
app/
└── memory/
    ├── page.tsx                       NEW — /memory route
    └── MemoryClient.tsx               NEW — settings page: global vs ticker-scoped lists, optimistic
                                          delete, inline edit, load-error handling (§7, bug #2)
tests/e2e/
├── fixtures.ts                        seedUserLearning() helper — seeds via the real admin endpoint
└── memory-page.spec.ts                NEW — asserts loading state resolves + seeded data renders
```

---

## 3. How It Works — Capped History + the Retrieval Safety Valve

```python
_MAX_LIVE_HISTORY = 20

history_rows = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
live_rows = history_rows[-_MAX_LIVE_HISTORY:] if len(history_rows) > _MAX_LIVE_HISTORY else history_rows
```

Trimming on its own would be silent data loss — the model would simply stop remembering turn 30 existed. The
`get_chat_history` tool is the same mechanism serving two different needs, dispatched on one argument:

```python
def _fetch_chat_history(ticker: str, conversation_id: str, user_email: str, db) -> str:
    if ticker:
        # cross-conversation: find the user's OTHER conversation about this ticker
        other_conv = db.query(Conversation).filter(
            Conversation.user_email == user_email,
            Conversation.ticker == ticker.upper(),
            Conversation.id != conversation_id,
        ).order_by(Conversation.updated_at.desc()).first()
        # ...pull its most recent 15 messages, verbatim
    else:
        # same-conversation: pull whatever _MAX_LIVE_HISTORY trimmed off THIS conversation
        older = all_rows[:-_MAX_LIVE_HISTORY]
        # ...take the most recent 15 of those, verbatim
```

**Why this works as a single tool instead of two:** both cases are "the model needs real messages it can't
currently see" — the only difference is *which* messages. Giving the model one tool with an optional `ticker`
argument, and a description that explains both trigger conditions, is simpler than two tools with overlapping
purposes and lets the model's own judgment decide which case it's in from the user's phrasing ("like we
discussed" vs. "in my SLV chat").

Retrieval is always **verbatim, never summarized** — lowest hallucination risk, and cheap to implement because
`Conversation.ticker` already exists (this is a plain SQL filter, not a RAG/vector-search problem).

---

## 4. How It Works — Two Memory Scopes, One Tool Design Principle

`save_learning(learning, ticker=None)`:

- **`ticker` omitted → global.** Surfaces in *every* conversation via `build_user_learnings_block()`.
- **`ticker` set → personal, ticker-scoped.** Surfaces only when that ticker's dossier is built, via
  `_ticker_learnings_section()`. Example: "already knows SLV/GLD overlap, don't re-explain."

**Confidence-gated confirmation**, encoded directly in the tool description (not application logic — this is
a case where the *prompt* is the safety mechanism):

```
Trigger on explicit language ('remember...', 'from now on...', 'don't forget...') or a clearly
stated lasting preference/fact — call this directly, no need to check first. If you're INFERRING
something might be worth remembering from a pattern in the conversation rather than the user
stating it outright, ask them to confirm before calling this tool — don't save an inferred guess
as if it were a confirmed instruction.
```

`delete_learning(learning)` — **exact-text-match only, no fuzzy matching.** The tool description tells the
model to copy the target text verbatim from what's already in its own context ("THINGS TO REMEMBER…" /
"Things you've told me about this ticker…") rather than paraphrase, and to ask the user to disambiguate if
unsure. An ambiguous or wrong match is refused, not guessed at — deleting the wrong saved fact is worse than
asking one clarifying question.

**`save_learning` vs. `flag_stock_correction` — the scope boundary that matters:**

| | `save_learning` | `flag_stock_correction` |
|---|---|---|
| Subject | The **user** (preference, fact about them) | The **ticker** (an objective correction) |
| Storage | `user_learnings`, keyed to `user_email` | `StockMemory`, keyed to `ticker` — no user column |
| Visibility | Only this user, every conversation (or one ticker) | **Every user** tracking that ticker |
| Read by | `build_user_learnings_block` / `_ticker_learnings_section` | The nightly Verdict Agent |

Getting this boundary wrong in either direction is a real privacy/quality bug: a personal preference leaking
into shared ticker memory (other users see it), or a factual correction about the ticker staying siloed to
one user instead of reaching the agent that produces tomorrow's verdict for everyone. The tool descriptions
state the boundary explicitly and cross-reference each other ("use flag_stock_correction instead" / "use
save_learning for those") so the model doesn't have to infer it.

---

## 5. How It Works — `flag_stock_correction` Reuses the Scorecard's Write Path

```python
def append_lesson(ticker: str, lesson: str, source: str, db: Session) -> StockMemory:
    """Same write path for both the weekly Scorecard's systematic-failure feedback
    and chat's flag_stock_correction tool — a correction caught in conversation
    reaches the nightly Verdict Agent the same way an audit-agent-caught one does."""
```

One function, two callers (`flag_stock_correction`'s tool dispatch, and the existing weekly Scorecard job).
The alternative — a separate, simpler append path just for chat — is exactly how the truncation bug in §7
happened in the first place: two paths doing "the same thing" that quietly drift apart. Collapsing to one
function means a fix applied once (the trim-oldest fix below) protects both callers permanently.

---

## 6. How It Works — Extended Thinking (Narrow Trigger, Isolated by Construction)

```python
_COMPLEX_DECISION_KEYWORDS = (
    "rebalance", "should i sell", "should i buy", "should i hold",
    "across my", "across all", "whole portfolio", "entire portfolio",
)
_THINKING_BUDGET_TOKENS = 3000

def _should_use_extended_thinking(message: str) -> bool:
    return any(kw in message.lower() for kw in _COMPLEX_DECISION_KEYWORDS)
```

Not "give a long answer" (that's `_estimate_max_tokens`'s separate job) but "reason through several
constraints before committing" — a narrow trigger set, not universal, so routine questions ("what's NVDA's
RSI") see zero cost or latency change. Matches the app's explicit priority: quality first, cost second, but
only pay the extra cost where the decision genuinely has multiple constraints to weigh.

Two implementation details worth keeping:

1. **`max_tokens` must exceed the thinking budget** — it caps thinking + output combined, so it's bumped up
   rather than eating into the existing output-size tier for these questions:
   ```python
   if use_thinking:
       max_tokens = max(max_tokens, _THINKING_BUDGET_TOKENS + 2000)
   ```
2. **Isolation from the saved message is structural, not a filter.** `content_block_delta` only appends
   `text_delta` chunks to `full_text` — a `thinking` content block never reaches that accumulator, so there's
   no way for thinking content to leak into what gets persisted as the assistant's message, by construction
   rather than by a check that could be forgotten later.
3. **A `thinking_start` SSE event covers the latency gap.** Extended thinking adds real time before the first
   visible token; without a signal, that gap silently reads as a hang to the user.

---

## 7. Gotchas & Lessons Learned

### G1 — Prompt-cache breakpoints match an exact PREFIX, not each labeled block independently

**This is the sharp one — a different failure mode than Part 1's "block too small to cache" gotcha.**

Symptom, found by checking whether switching between *different* ticker-scoped conversations still hit
cache: it didn't, even though the large shared block (all-tickers compact list, correlations, watchlist) was
otherwise byte-identical between them.

Root cause: the focus ticker's full dossier was embedded **inline at the START** of the dynamic-context
block, and Anthropic's cache matching walks the request **prefix-first**. A block that necessarily differs
per ticker, placed *before* a much larger block that doesn't need to differ, poisons the cache match for
everything after it — even though that later content, taken alone, was unchanged.

```
❌ BEFORE — focus dossier embedded first, poisons everything after it on every ticker switch
api_system = [
    { static role/rules,                                    cache_control: ephemeral },
    { focus_dossier(SLV) + all_tickers_compact_list + ...,  cache_control: ephemeral },
]
# switch to GLD conversation → focus_dossier(GLD) differs → ENTIRE block is a cache miss,
# including the all_tickers_compact_list portion that didn't actually change

✓ AFTER — variable content moved to its OWN block, placed LAST
api_system = [
    { static role/rules,               cache_control: ephemeral },
    { all_tickers_compact_list + ...,  cache_control: ephemeral },   # identical across every
                                                                       # ticker-scoped conversation
    { focus_dossier(ticker),           cache_control: ephemeral },   # only THIS block misses on a switch
]
```

**Rule of thumb: order cache blocks from most-shared to least-shared, and put the block that legitimately
varies every call LAST.** Anything that must differ per-request should never sit in front of something that
doesn't — every byte after the first difference is uncacheable regardless of its own content.

Verified against a real production DB (user with 83 tracked tickers, GLD and SLV both watched): the shared
block was confirmed **byte-identical** between the two ticker-scoped conversations after the fix (previously
it differed) — ~6,773 tokens, versus a ~940-token focus dossier that correctly still varies per ticker. That
shared block had previously been rewritten from scratch, and re-billed at full price, on every single ticker
switch.

**Also hit the same session: ran out of cache breakpoints.** Anthropic caps a request at **4 cache_control
breakpoints total**. Adding a breakpoint for the message-history split (§8-adjacent — see the streaming.py
history block) meant one existing breakpoint had to be freed. Fix: merge `base_prompt` + the small
`user-learnings` block into one shared cache block, since `base_prompt` alone (~500 tokens) is small and
`user-learnings` changes rarely — a `save_learning` mid-conversation now busts that whole merged block instead
of just its own slice, an acceptable tradeoff at that size for getting message-history caching working.

### G2 — Capped-append-then-truncate keeps the wrong end

Real production evidence: the weekly Scorecard flagged both MU and TMUS as systematic BUY failures and fed a
lesson back into `StockMemory` for both. TMUS's landed; MU's silently didn't — MU's memory was at exactly the
1200-char cap with no `[Scorecard]` tag anywhere.

```python
# ❌ BEFORE — trims the END, dropping whatever the append just added
combined = existing + "\n\n" + new_lesson
memory_narrative = combined[:_MAX_CHARS]   # keeps the FRONT (oldest), drops the newest — exactly
                                            # the thing this function exists to add, whenever memory
                                            # was already near-full

# ✓ AFTER — trim the OLDEST paragraphs first, so the newest lesson always survives
paragraphs = existing.split("\n\n")
paragraphs.append(tagged_new_lesson)
combined = "\n\n".join(paragraphs)
while len(combined) > _MAX_CHARS and len(paragraphs) > 1:
    paragraphs.pop(0)                       # drop oldest, not newest
    combined = "\n\n".join(paragraphs)
```

**General pattern: for any capped, append-only buffer, decide explicitly which end survives truncation — and
default to "the thing I just added," not "whatever was already there."** A silent `[:cap]` after concatenation
almost always keeps the wrong end for an append-oriented log. This bug was invisible in code review; it only
showed up by checking real production rows for the missing tag.

### G3 — A fetch/json() without try/catch leaves a spinner stuck forever, not an error

The `/memory` page shipped stuck on "Loading…" in production. Root cause: no `try/catch` around the
`fetch()`/`.json()` calls, so *any* failure (network error, CORS, a non-JSON error body from a gateway
timeout) threw before `setLoading(false)` ever ran — spinner stuck indefinitely, with nothing visible telling
the user (or the developer) why.

```tsx
// ✓ fix — catch covers BOTH fetch() throwing AND .json() throwing on a non-JSON body
async function load() {
  setLoading(true);
  setLoadError(null);
  try {
    const r = await fetch(url);
    setLearnings(r.ok ? await r.json() : []);
    if (!r.ok) setLoadError(`Couldn't load your memory (${r.status}).`);
  } catch {
    setLoadError("Couldn't reach the server. Check your connection and try again.");
  } finally {
    setLoading(false);     // guaranteed to run regardless of which branch failed
  }
}
```

**Rule of thumb: every `finally` that clears a loading flag must sit outside a `try` that can throw from more
than one call inside it** — `fetch()` throwing and `.json()` throwing on a malformed body are two different
failure points that both need the same catch.

Found the underlying cause was compounded by a second, unrelated issue during verification: the local backend
process was itself stale (pre-dated the session's work, running without `--reload`) — restarting it was
required before the fix could be verified end-to-end against real seeded data in an actual browser, not just
assumed correct from the diff.

### G4 — A migration guard must land in the SAME commit as the model field, not "later"

`ticker` was added to `UserLearning` in an earlier PR, but no matching `ALTER TABLE` guard was added to
`_migrate_db()` at the same time. `Base.metadata.create_all()` only creates missing *tables*, never alters
existing ones — so any production table that already existed before the column was added never got it.
Every `/learnings` query threw `psycopg2.errors.UndefinedColumn` in production from that point on, confirmed
via Railway logs.

```python
if "user_learnings" in tables:
    ul_cols = {c["name"] for c in inspector.get_columns("user_learnings")}
    if "ticker" not in ul_cols:
        conn.execute(text("ALTER TABLE user_learnings ADD COLUMN ticker VARCHAR"))  # nosemgrep
    conn.commit()
```

Same self-healing pattern as every other guard already in this function (`inspector.get_columns()` → check →
conditional `ALTER TABLE`) — the fix here wasn't inventing a new pattern, it was applying an existing one that
got skipped for one specific column. **Rule of thumb: adding a nullable column to a SQLAlchemy model is not a
migration by itself on Postgres — pair every new column with a `_migrate_db()` guard in the same commit,** or
grep the model file against `_migrate_db()` before merging any model change.

### G5 — An e2e test asserting on unseeded data only ever proves your local leftover state

`memory-page.spec.ts` originally asserted on specific learning text with nothing in the test creating it — it
only ever passed locally, against rows left over from a manual seed earlier in development. It never passed
in CI (confirmed failing on the PR that would have caught it).

Fix: added a test-only admin-secret endpoint (`POST /jobs/admin/user-learnings`), matching the existing
`ingest-analysis`/`ingest-snapshot` seeding pattern, and called it from the test before assertions:

```ts
await seedUserLearning(request, testEmail, "E2E test global learning.");
await seedUserLearning(request, testEmail, "E2E test ticker-scoped learning.", "ZE2E");
await page.goto("/memory");
await expect(page.getByText("E2E test global learning.")).toBeVisible();
```

**Rule of thumb: if a test's assertion text isn't created anywhere inside that test (or its fixtures), it's
not testing the feature — it's testing whatever state your machine happened to be in.** Always run a new e2e
test against a clean DB, not just locally against a warm one, before trusting it.

---

## 8. When to Use This Pattern

| Situation | Approach |
|---|---|
| Feature has multiple content blocks in one API request, only some of which vary per-call | Order blocks most-shared → least-shared; put the block that legitimately changes every call LAST |
| A cache block "looks" correctly marked but you haven't checked whether DIFFERENT contexts (not just repeated turns) still hit it | Test across variation, not just repetition — same-conversation cache hits can pass while cross-context hits silently fail |
| You've hit Anthropic's 4-cache-breakpoint cap and need a new one | Merge two small, rarely-changing blocks into one rather than dropping caching on either |
| An append-only field has a hard character/size cap | Decide explicitly which end survives truncation — for a log/lesson-append pattern, that's almost always "keep the newest" |
| A settings page needs to show/edit data an AI agent also writes | Give it its own REST API (not routed through chat) — a user shouldn't need to converse with the AI to fix what it got wrong |
| Two different callers need "the same kind of append" (a scheduled job + a live chat tool) | One shared function, not two similar ones — bugs found in one path get fixed for both automatically |
| A model gains a new nullable column | Add the `_migrate_db()` ALTER TABLE guard in the SAME commit, not as a follow-up |
| Writing a new e2e test against seeded UI state | Seed via a real API call inside the test/fixture — never assert on text nothing in the test created |
| A user might reference something outside the model's current context window ("like we discussed", "in my other chat about X") | Give it a verbatim-retrieval tool scoped by whatever natural key already exists (here: `Conversation.ticker`) — don't build summarization or vector search unless the exact-match key genuinely doesn't exist |

---

## 9. Quick Reference

```python
# Cache block ordering — most-shared first, most-variable LAST
api_system = [
    {"type": "text", "text": static_role_rules,        "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": shared_across_all_focus,   "cache_control": {"type": "ephemeral"}},  # same
                                                                                                     # regardless of which item is "in focus"
    {"type": "text", "text": per_focus_variable_block,  "cache_control": {"type": "ephemeral"}},   # LAST —
                                                                                                     # only this misses on a focus switch
]
# Anthropic hard cap: 4 cache_control breakpoints per request — merge small/rarely-changing
# blocks together before you run out of slots.

# Capped append-only buffer — keep the newest, trim the oldest
paragraphs = existing.split("\n\n") + [new_entry]
combined = "\n\n".join(paragraphs)
while len(combined) > MAX_CHARS and len(paragraphs) > 1:
    paragraphs.pop(0)              # drop OLDEST first
    combined = "\n\n".join(paragraphs)

# Every fetch()/json() pair needs a catch that covers BOTH failure points, with the
# loading-flag reset in `finally` so it always fires regardless of which one threw
try {
  const r = await fetch(url);
  const data = r.ok ? await r.json() : null;
} catch { setError("..."); } finally { setLoading(false); }

# New nullable column on an existing model -> pair with a migration guard, same commit
if "ticker" not in inspector.get_columns("user_learnings"):
    conn.execute(text("ALTER TABLE user_learnings ADD COLUMN ticker VARCHAR"))

# Extended thinking — narrow trigger, not universal; bump max_tokens past the budget
_THINKING_BUDGET_TOKENS = 3000
if use_thinking:
    max_tokens = max(max_tokens, _THINKING_BUDGET_TOKENS + 2000)

# Model pinning with a self-documenting expiration check
_SONNET = "claude-sonnet-5"  # intro pricing $2/$10 thru Aug 31 2026 — re-verify vs $3/$15 after that date

# e2e test seeding — always through a real endpoint, never asserted against ambient DB state
await seedUserLearning(request, testEmail, "...", tickerOrNull);
```
