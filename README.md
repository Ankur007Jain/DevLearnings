# Dev Learnings

Personal reference notes — things I learned while building, organized by topic.

> Add new learnings with `/learn` inside any Claude Code session.

---

## Topics

| Folder | What's inside |
|--------|--------------|
| [github-actions/](github-actions/) | CI pipelines, workflows, DAG visualization |
| [claude-agents/](claude-agents/) | Agentic loops, multi-agent orchestration, slash commands |
| [claude-code/](claude-code/) | Claude Code tips, subscriptions, GitHub App setup |
| [frontend/](frontend/) | Next.js/React UI patterns, animations, event handling |
| [backend/](backend/) | FastAPI, Python, auth patterns |
| [general/](general/) | Cross-stack patterns, tooling, AI workflow |
| [templates/](templates/) | Copy-paste starter files for new projects |

---

## Index

### GitHub Actions
- [Agent QA Pipeline — visual DAG orchestrator](github-actions/agent-qa-pipeline.md)
- [Replicating the pipeline in a new repo](github-actions/replicate-for-new-repo.md)

### Claude Agents
- [What is an agentic loop?](claude-agents/agentic-loop.md)
- [Multi-agent orchestration — Test → Fix → Docs](claude-agents/multi-agent-orchestration.md)
- [Slash commands vs Python agents](claude-agents/slash-commands-vs-python-agents.md)

### Claude Code
- [claude-code-action setup (Pro subscription, no API key)](claude-code/claude-code-action-setup.md)

### Frontend
- [Sign-in page UI patterns — immersive lanes, marquee, photo carousel, event bubbling](frontend/sign-in-page-ui-patterns.md)
- [React hydration errors — locale formatters + pre-hydration DOM mutations](frontend/react-hydration-errors.md)

### Backend
- [Admin role: env var bootstrap + DB fallback pattern](backend/admin-dual-check-pattern.md)

### General
- [AI-readable project map — PROJECT_MAP.md pattern](general/ai-readable-project-map.md)

### Templates
- [.test-agent.yml](templates/test-agent.yml)
- [qa-pipeline.yml](templates/qa-pipeline.yml)
