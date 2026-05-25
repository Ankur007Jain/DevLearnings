# Multi-Agent Orchestration — Test → Fix → Docs

**Learned:** 2026-05-25

---

## The pattern

```
ORCHESTRATOR
├── QA Agent     — finds bugs, writes tests, produces qa-report.md
├── Fix Agent    — reads qa-report, fixes bugs, verifies
└── Docs Agent   — updates TECHNICAL.md, ARCHITECTURE.md, CHANGELOG.md
```

Flow: `QA → bugs? → Fix → QA again` (up to 2 rounds) `→ Docs`

## How agents communicate

Agents don't talk to each other directly. They share state through **files**:
- `reports/qa-report.md` — QA Agent writes it, Fix Agent reads it
- Source files — Fix Agent edits them, QA Agent re-runs tests on them

## Write permission guards (isolation)

Each agent is blocked from touching what it shouldn't:

| Agent | Can write | Blocked from |
|-------|-----------|-------------|
| QA Agent | `tests/`, `__tests__/`, `reports/` | source files, docs |
| Fix Agent | any source file | test files, `.md` docs |
| Docs Agent | `*.md` files only | source files, test files |

This prevents the Fix Agent from "fixing" a bug by deleting the test, and prevents
the QA Agent from accidentally editing source code.

## Two ways to run it

### 1. Slash commands (interactive, uses Claude Code subscription)
```
/qa main HEAD          # QA Agent
/fix reports/qa-report.md  # Fix Agent
/docs-sync main HEAD   # Docs Agent
```
No API key. No billing beyond your subscription. Lives in `~/.claude/commands/`.

### 2. GitHub Actions (automated CI, uses Claude Code subscription)
`qa-pipeline.yml` runs the same slash commands via `claude-code-action@beta`.
Triggers automatically on every PR to `main`.
See: [agent-qa-pipeline.md](../github-actions/agent-qa-pipeline.md)

## When to use Python agents instead
Only for truly headless/autonomous runs where no Claude Code session is open
(e.g., scheduled nightly jobs). Requires `ANTHROPIC_API_KEY` and bills per token.
