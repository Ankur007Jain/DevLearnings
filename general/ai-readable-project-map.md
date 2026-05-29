# AI-Readable Project Map — PROJECT_MAP.md Pattern

**Learned:** 2026-05-28 | **Project:** TravelPlannerV2

---

## What it is
A dense, structured reference file purpose-built so an AI model can orient itself in a codebase with minimal tokens. Different from a README (for humans) or ARCHITECTURE.md (narrative with diagrams) — this is a lookup table, not a document.

---

## How it works

Create `PROJECT_MAP.md` at the repo root. Wire it into `CLAUDE.md` so it auto-loads:

```markdown
# CLAUDE.md
@AGENTS.md
@PROJECT_MAP.md
```

The `@filename` syntax in CLAUDE.md tells Claude Code to include that file in every conversation context automatically.

### What to put in it

Use tables and structured lists. No prose, no Mermaid diagrams. Key sections:

```markdown
## What It Is             ← 3-line summary of the app
## Directory Layout       ← annotated tree (what's in each folder)
## Backend API Surface    ← every endpoint: method | path | description
## Database Tables        ← every table: name | key columns | notes
## Tier/Permission System ← access rules in a table
## Frontend Key Files     ← filename | what it does
## Key Services           ← service | what it does
## CI/CD Workflows        ← workflow | trigger | what it runs
## Environment Variables  ← var | purpose (frontend + backend separate)
## Test Locations         ← type | path | count + run commands
## Theming                ← rules in 3 lines
```

---

## Gotchas

- **Audit it after writing.** The first version missed: 2 CI workflows, 2 env vars, 21 chat files, all Next.js API routes, and had a wrong table count. Spawn an Explore agent with "compare PROJECT_MAP vs actual codebase, report only gaps" to catch misses.
- **Keep it current.** Update counts (test counts, file counts) when they change significantly. Stale facts are worse than no facts.
- **Don't duplicate CLAUDE.md rules.** PROJECT_MAP is for "what exists", CLAUDE.md is for "how to work". Keep them separate.
- **`trip_inspiration_cache` gotcha:** Table created via raw SQL migration, not SQLAlchemy model. Maps and docs that say "X SQLAlchemy models" should note migration-only tables separately.

---

## Quick reference

```
File: PROJECT_MAP.md (repo root)
Auto-load: add @PROJECT_MAP.md to CLAUDE.md
Audit command:
  "Compare PROJECT_MAP.md against actual codebase.
   Read every router, page.tsx, models.py, workflows/, services/, .env.
   Report ONLY what is missing or wrong."

Target size: ~250-300 lines. Dense enough to be complete, short enough to be cheap.
Rule of thumb: if an AI needs to read 5 files to understand the project, the map is too sparse.
```
