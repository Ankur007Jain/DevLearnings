# Replicating the Agent Pipeline in a New Repo

**Learned:** 2026-05-25

---

## What's global (already works everywhere)

The slash commands `/qa`, `/fix`, `/docs-sync` live in `~/.claude/commands/`.
They are available in **any** Claude Code session on your machine — no copying needed.

## What to add to each new repo

### 3 files

**1. `.test-agent.yml`** (at repo root) — customise per project:
```yaml
name: MyProject

test_commands:
  backend:  cd backend && pytest tests/ -v --tb=short
  frontend: npx jest --no-coverage

test_dirs:
  backend:  backend/tests/
  frontend: src/__tests__/

source_dirs:
  backend:  backend/
  frontend: src/

stack:
  backend_framework:  fastapi
  frontend_framework: react
  test_frameworks:    pytest, jest

report_path: reports/qa-report.md
```

**2. `.github/workflows/qa-pipeline.yml`** — copy as-is from TravelPlannerV2 or from [templates/qa-pipeline.yml](../templates/qa-pipeline.yml). Nothing to change.

**3. `reports/.gitkeep`** — empty file so the `reports/` directory exists in git.

### 2 one-time steps

**Step 1 — Install Claude Code GitHub App on the repo:**
Go to **https://github.com/apps/claude** → Install → select the repo.

**Step 2 — Add secret:**
Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `CLAUDE_CODE_OAUTH_TOKEN`
- Value: same token from `claude setup-token` (your existing token works for all repos)

## Trigger
The pipeline fires automatically on every PR targeting `main`. No manual trigger needed.
