# What is an Agentic Loop?

**Learned:** 2026-05-25

---

## The concept

An agentic loop is when an AI runs in a `while` loop, using tools, until it decides it's done.

```
User gives goal
      │
      ▼
  ┌─────────────────────────────┐
  │  Claude thinks              │
  │  → decides to use a tool   │
  │  → tool runs locally        │
  │  → result fed back to Claude│
  │  → Claude thinks again      │
  └─────────────────────────────┘
      │  (repeats until Claude says "end_turn")
      ▼
  Final answer / done
```

## Key components

| Component | What it is |
|-----------|-----------|
| **System prompt** | Tells Claude what role it plays and what steps to follow |
| **Tool definitions** | JSON schema describing what tools Claude can call (bash, read file, write file, etc.) |
| **Agentic loop** | `while True:` — call Claude API, execute tools, feed results back, repeat |
| **Stop condition** | `stop_reason == "end_turn"` means Claude is done |

## The `stop_reason` values

```python
if response.stop_reason == "end_turn":
    break                          # Claude is done
elif response.stop_reason == "tool_use":
    # Execute the tools Claude asked for, feed results back
    ...
else:
    # max_tokens or other — handle dangling tool_use blocks
    # add synthetic tool_results and break
    break
```

## Why `if/elif/else` matters
If you use `if/if` instead of `if/elif/else`, the `else` case (e.g. `max_tokens`) doesn't
get handled. Claude's message history ends up with a `tool_use` block without a matching
`tool_result` → next API call fails with `400 BadRequestError`.

## Write mode safety guards
Each agent enforces what it can write:
```python
write_mode = "tests_only"   # QA Agent — can only write test files and reports
write_mode = "source_only"  # Fix Agent — can only write source files
write_mode = "docs_only"    # Docs Agent — can only write .md files
```

## Cost considerations
- Every API call re-sends the full message history → history grows each turn
- Large tool outputs (git diff, file reads) bloat context fast
- Tighten truncation limits: git_diff 8k, read_file 6k, run_command 5k
- Use Haiku for agents, not Sonnet — same capability for structured tasks, much cheaper
