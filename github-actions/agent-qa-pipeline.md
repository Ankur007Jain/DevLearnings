# Agent QA Pipeline — Visual DAG Orchestrator

**Learned:** 2026-05-25 | **Project:** TravelPlannerV2

---

## What it is

A GitHub Actions workflow that runs a multi-agent AI pipeline on every PR to `main`.
Each agent phase is its own **job**, so GitHub renders a clickable visual graph in the Actions tab.

## The pipeline

```
[Gate — pytest] ──┐
                  ├──→ [QA Agent] ──→ [Bugs Found?] ──→ [Fix Agent] ──→ [Re-test] ──→ [Docs Agent] ──→ [Post Summary]
[Gate — jest]  ──┘                        │
                                          └── (skipped, grey) if report is clean
```

- **QA Agent** — runs `/qa`, finds bugs, writes missing tests, produces `reports/qa-report.md`
- **Bugs Found?** — bash job that parses `qa-report.md` and outputs `bugs=true/false`
- **Fix Agent** — runs `/fix`, only starts if `bugs=true` (shows as **skipped/grey** otherwise)
- **Re-test** — re-runs `/qa` to verify fixes didn't break anything
- **Docs Agent** — runs `/docs-sync` to update TECHNICAL.md, ARCHITECTURE.md, CHANGELOG.md
- **Post Summary** — posts qa-report as a comment on the PR

## Key design decisions

### Why split into jobs instead of steps?
Steps inside one job are not visualized as a graph — they're just a flat log.
Jobs with `needs:` dependencies get rendered as boxes with arrows by GitHub. That's the visual DAG.

### Passing data between jobs
Jobs don't share a filesystem. Use **artifacts**:
```yaml
# Job A: upload
- uses: actions/upload-artifact@v4
  with:
    name: qa-report
    path: reports/qa-report.md

# Job B: download
- uses: actions/download-artifact@v4
  with:
    name: qa-report
    path: reports/
```

### Conditional jobs
```yaml
fix-agent:
  needs: check-bugs
  if: needs.check-bugs.outputs.bugs == 'true'
```
Pass values between jobs via `outputs`:
```yaml
check-bugs:
  outputs:
    bugs: ${{ steps.parse.outputs.bugs }}
```

### Docs Agent runs regardless of whether Fix ran
```yaml
docs-agent:
  needs: [check-bugs, fix-agent]
  if: always() && needs.check-bugs.result == 'success'
```

## Authentication
Uses Claude Pro/Max subscription — no per-token billing.
See: [claude-code-action setup](../claude-code/claude-code-action-setup.md)

## The workflow file
See template: [templates/qa-pipeline.yml](../templates/qa-pipeline.yml)
