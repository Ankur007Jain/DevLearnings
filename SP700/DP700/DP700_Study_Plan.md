# DP-700 Exam Study Plan
**Exam Date:** Monday, June 2, 2026  
**Daily Time:** 5–6 hours  
**Profile:** SQL strong | PySpark ok | KQL weak | All domains roughly equal

---

## Exam Breakdown (Equal Weight)
| Domain | Weight | Key Trap Areas |
|---|---|---|
| Implement & Manage | 30–35% | Security layers, deployment pipelines, Spark config |
| Ingest & Transform | 30–35% | When to use what tool, streaming specifics, KQL |
| Monitor & Optimize | 30–35% | Error types per item, optimization choices |

**Pass mark:** 700/1000. Exam includes simulation-style tasks (UI navigation) not just MCQs.

---

## 4-Day Schedule (Compressed — Repeat Attempt)

| Day | Date | Focus | File |
|---|---|---|---|
| 1 | Tue May 26 | Implement & Manage: Workspace Config, Lifecycle, Security overview | `Day1_Implement_Manage.md` ✅ |
| 2 | Wed May 27 | Security & Governance deep + Orchestration + Ingest/Transform Batch | `Day2_Security_Ingest_Batch.md` |
| 3 | Thu May 28 | Ingest/Transform Streaming + KQL deep dive + Monitor & Error Resolution | `Day3_Streaming_KQL_Monitor.md` |
| 4 | Fri May 29 | Performance Optimization + Full Mock Exam + Targeted Weak-Spot Review | `Day4_Optimize_MockExam.md` |
| — | Sat–Sun | Buffer: review flagged topics, redo wrong mock answers only | — |
| — | Mon Jun 2 | Exam Day — no new topics, light scan of decision tables only | — |

---

## How Each Day Is Structured
Each day file contains:
1. **Decision Tables** — when to pick X over Y (exam loves these)
2. **Scenario Q&A** — realistic exam-style questions with explained answers
3. **Gotchas** — things that trip people up in the actual exam
4. **Hands-On Exercise** — do this in a free Fabric trial workspace
5. **Quick-Fire Review** — 10 rapid questions to close the day

---

## Setup Before Day 1
- Get a free Microsoft Fabric trial: https://app.fabric.microsoft.com (sign up with personal MSA)
- Enable all workloads in your trial workspace
- Bookmark the official practice assessment: https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/practice/assessment

---

## KQL Priority Topics (Your Weak Area — woven across Days 3, 4, 5)
- Basic query syntax: `| where`, `| project`, `| summarize`, `| extend`
- Windowing: `bin()`, `tumbling`, `sliding`, `session` windows
- Aggregations: `count()`, `sum()`, `avg()`, `dcount()`
- Time filtering: `ago()`, `between`, `datetime`
- When exam asks KQL vs SQL vs PySpark — know the trigger: **KQL = Real-Time / eventhouse / streaming logs**
