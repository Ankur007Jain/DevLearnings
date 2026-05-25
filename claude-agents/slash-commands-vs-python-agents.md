# Slash Commands vs Python Agents

**Learned:** 2026-05-25

---

## The confusion

Both do similar things (run Claude, use tools, produce output) but through completely
different mechanisms with very different cost implications.

## Side by side

| | Slash Commands | Python Agents |
|--|---------------|--------------|
| **How** | Markdown files in `.claude/commands/` or `~/.claude/commands/` | Python script calling Anthropic SDK directly |
| **Runs inside** | Claude Code session (your subscription) | Standalone — needs `ANTHROPIC_API_KEY` |
| **Billing** | Included in Pro/Max subscription | Per-token API billing |
| **Triggered by** | You typing `/qa` in Claude Code, or `claude-code-action` in CI | `python agent.py` or GitHub Actions runner |
| **Good for** | Interactive use, CI via `claude-code-action` | Fully headless/scheduled jobs without Claude Code open |

## The key insight

If you have a Claude Code Pro/Max subscription, **slash commands + claude-code-action**
cover 95% of use cases with zero extra cost. Python agents are for the edge case where
you need a fully autonomous run with no Claude Code session at all.

## Where slash commands live

```
~/.claude/commands/     ← global, works in every project
  qa.md
  fix.md
  docs-sync.md

<repo>/.claude/commands/  ← project-specific only
```

Always put reusable commands in `~/.claude/commands/` so you don't have to copy them.

## How a slash command works

A `.md` file with instructions. Claude Code reads it as a system prompt when you type `/command-name`.
`$ARGUMENTS` is replaced with whatever you type after the command name.

```markdown
# qa.md
You are a senior QA engineer. Run the full QA pipeline.

Arguments: $ARGUMENTS
Parse first word as base branch (default: main), second as head (default: HEAD).

## Step 1 — Read config
Run: `cat .test-agent.yml`
...
```
