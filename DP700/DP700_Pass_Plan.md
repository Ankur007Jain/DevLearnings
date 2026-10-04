# DP-700 Pass Plan — Exam Mon Oct 26, 2026

Updated Oct 3, 2026

## Exam facts and what changed

Your Oct 26 sitting runs on the **Oct 19, 2026 skills outline**, which goes live one week before your exam. Your Study Hub notes were fact-checked against the July 21 outline on Sep 6, so only the Oct 19 changes are new.

| Item | Detail |
| --- | --- |
| Exam | DP-700: Implementing Data Engineering Solutions Using Microsoft Fabric |
| Certification | Microsoft Certified: Fabric Data Engineer Associate |
| Exam time / seat time | 100 min / 120 min (seat time covers instructions and agreement) |
| Questions | Microsoft says most exams have 40–60; DP-700's count is not published |
| Pass mark | 700 / 1000 |
| Domains | Implement & manage · Ingest & transform · Monitor & optimize, each 30–35% |
| Microsoft Learn in the exam | Opens in a split pane; learn.microsoft.com only; Ctrl+F works on a page; the timer keeps running |
| Breaks | Allowed, but the clock runs and you cannot return to any question seen before the break |

**What changed since your notes**

- **Jul 21, 2026:** "Configure Dataflows Gen2 workspace settings" was replaced by **"Configure Apache Airflow workspace settings."** Your Sep 6 notes cover it; the tracker's topic list did not until today's update.
- **Oct 19, 2026:** Microsoft's change log marks **workspace settings** and **optimize performance** as "Minor" changes and everything else "No change." The page does not spell out the exact wording delta, so give those two areas an extra pass on Oct 19 instead of guessing.
- Easy-to-skip bullets that are on the current list: Fabric audit logs, OneLake security, database projects, native tables vs OneLake shortcuts in Real-Time Intelligence, and Query acceleration for shortcuts vs standard shortcuts.

## Strategy

Spend weeks 1–2 closing Domain 1 and Domain 2 gaps, then give Domain 3 error resolution extra time, since your last-attempt report flagged it even though Mock 6 scored Domain 3 at 100%; every week ends with a timed mock and a hard score gate.

**Time budget (assumed):** about 1.5 hours on weekday evenings and 4 hours on Saturday and Sunday, roughly 40 hours in total. If a day slips, move its block to the next weekend morning rather than skipping it.

**Method, same loop that worked before:** practice question → wrong answer → gotcha box in `dp700_notes.html` or `dp700_kql.html` → retry the same topic 48 hours later. For every miss, write one line on why each wrong option is wrong. You have seen Mocks 2–5 and the Microsoft Practice Assessment before, so recognition inflates those scores; the explain-every-option rule is how you tell real recall from memory of the answer key.

| Topic area | Last known level | Priority |
| --- | --- | --- |
| Security & governance: workspace and item permissions, RLS/CLS/OLS, masking, OneLake security, labels, endorsement, audit logs | Domain 1 at 57% on Mock 6 | High |
| Lifecycle: Git integration, database projects, deployment pipelines | Several logged traps | High |
| Workspace settings: Spark, domains, OneLake, Apache Airflow | Airflow is the newest bullet | High |
| Loading patterns: full vs incremental, CDC, dimensional prep, COPY INTO vs CTAS | Domain 2 at 55% on Mock 6 | High |
| T-SQL grouping: GROUPING SETS vs ROLLUP vs CUBE | Known weak spot | High |
| Pipelines: Copy activity, parameters, dynamic expressions | Known weak spot | High |
| Real-Time Intelligence: Eventstream, Eventhouse, KQL, windowing | Known weak spot | High |
| Error resolution (Domain 3): pipeline, Dataflow Gen2, notebook, Eventhouse, Eventstream, T-SQL, shortcut errors | Flagged weak on last attempt; Mock 6 hid it | High |
| Spark and Delta Lake | Strong | Maintain |

**Readiness gates**

| Date | Gate | Target | If you miss it |
| --- | --- | --- | --- |
| Sat Oct 10 | Mock 2, timed at 100 min | 75%+, no domain below 65% | Repeat the two lowest Week 1 days before starting Week 2 |
| Sat Oct 17 | Microsoft Practice Assessment + community Mock 1 | 80%+ on the assessment, 75%+ on the mock | Swap Mon–Tue of Week 3 to the weakest domain |
| Thu Oct 22 | Community Mock 3, timed | 80%+ | Below 70%: check the reschedule cutoff in your Pearson VUE confirmation and decide that day |

Your tracker's last-attempt banner lists Security & Governance, Streaming and Error Resolution as weak; the official report outranks any mock, so those three lead each week.

## Week 1 (Sat Oct 3 – Fri Oct 9): Domain 1

This week closes the security, lifecycle and workspace-settings gaps that pulled Domain 1 down to 57%. Do each hands-on step in a trial or sandbox workspace, not a production one.

**Sat Oct 3 · 2 h · Baseline**

- [ ] Read the Oct 19 skills list end to end and rate every bullet red, amber or green in `DP700_Tracker.html`
- [ ] Take the Microsoft Practice Assessment once, cold, and log the per-domain scores
- [ ] Read the trap checklist at the end of this doc, then push the updated Study Hub files to GitHub

**Sun Oct 4 · 4 h · Workspace, item and OneLake access**

- [ ] Build a matrix: Admin, Member, Contributor, Viewer × create items, share, manage access, read via SQL endpoint, run notebooks
- [ ] Share one lakehouse three ways (Read, ReadData, ReadAll) and test what the SQL endpoint and Spark each expose
- [ ] Create a OneLake security role scoped to one table or folder; check on Learn which workspace roles it applies to and which bypass it
- [ ] Write the gotchas into section 1.6 of `dp700_notes.html`

**Mon Oct 5 · 1.5 h · Warehouse granular security**

- [ ] RLS: write a predicate function and `CREATE SECURITY POLICY`; test it with `EXECUTE AS USER`
- [ ] Column-level: `GRANT SELECT` on a column list; object-level: `DENY` on a table or view
- [ ] Dynamic data masking: try `default()`, `email()`, `partial()`, `random()`; then grant `UNMASK` and compare

**Tue Oct 6 · 1.5 h · Governance**

- [ ] Sensitivity labels: who can apply them and how they flow to downstream items
- [ ] Endorsement: Promoted vs Certified vs Master data, and who is allowed to certify
- [ ] Fabric audit logs: find on Learn where audit events are searched and which role is needed

**Wed Oct 7 · 1.5 h · Lifecycle management**

- [ ] Git integration: connect a workspace to a branch, commit, then update from Git; note which item types are supported
- [ ] Database project: create an SDK-style project for a Warehouse, build it, publish it once
- [ ] Deployment pipelines: stages, assigning vs deploying, deployment rules, pipeline admin vs workspace roles

**Thu Oct 8 · 1.5 h · Workspace settings**

- [ ] Spark: starter vs custom pools, environments, high concurrency, native execution engine, runtime version
- [ ] Domains: create one, assign workspaces, domain admin vs domain contributor
- [ ] OneLake workspace settings
- [ ] Apache Airflow: read the Airflow job concepts page and the workspace setting, then write 5 Q&A pairs into your notes

**Fri Oct 9 · 1.5 h · Orchestration**

- [ ] Decision table: Dataflow Gen2 vs pipeline vs notebook (skill set, scale, code vs low-code, orchestration)
- [ ] Scheduled vs event-based triggers, including storage events and job events
- [ ] Notebook orchestration: `notebookutils.notebook.run` vs `runMultiple` with a DAG and dependencies
- [ ] Pipelines: parameters, `@pipeline().parameters`, `@activity('X').output`, and the Lookup → ForEach metadata-driven pattern

## Week 2 (Sat Oct 10 – Fri Oct 16): Domain 2 and Real-Time Intelligence

This week targets loading patterns, GROUPING SETS, Copy activity and Real-Time Intelligence, the four Domain 2 areas you logged as weak.

**Sat Oct 10 · 4 h · Gate, then loading patterns**

- [ ] Mock 2 timed at 100 min, not its 130; log domain scores and write a gotcha for every miss
- [ ] Full vs incremental loads: watermark column, CDC, and mirroring as the no-code option
- [ ] Upserts: Delta `MERGE` in a notebook and the T-SQL version in a Warehouse
- [ ] Dimensional prep: surrogate keys, SCD Type 1 vs Type 2, late-arriving dimension rows

**Sun Oct 11 · 4 h · Batch ingestion**

- [ ] Pick a data store: one line each on when to use Lakehouse, Warehouse, Eventhouse and SQL database
- [ ] Shortcuts: internal vs ADLS Gen2 vs S3, shortcut caching, and whose permissions apply
- [ ] Mirroring: which sources, what it replicates, where it lands
- [ ] Copy activity: staging, fault tolerance, write behavior, degree of parallelism
- [ ] Warehouse loading: one working example each of `COPY INTO`, CTAS and `INSERT … SELECT`

**Mon Oct 12 · 1.5 h · T-SQL grouping drill**

- [ ] Write one sales query three ways: `ROLLUP(Region, City)`, `CUBE(Region, City)`, `GROUPING SETS ((Region, City), (Region), ())`; predict row counts before running
- [ ] Use `GROUPING()` to label subtotal and grand-total rows
- [ ] Window functions: `ROW_NUMBER()` to dedupe, `LAG`/`LEAD` to spot late rows

**Tue Oct 13 · 1.5 h · PySpark transforms**

- [ ] `dropDuplicates` vs `distinct`; `fillna`, `dropna`, `coalesce` for missing values
- [ ] `groupBy().agg()` and PySpark window functions
- [ ] Denormalize: join a fact to its dimensions, with a broadcast join for the small one
- [ ] For four sample scenarios, choose Dataflow Gen2, notebook, KQL or T-SQL and say why

**Wed Oct 14 · 1.5 h · Real-Time Intelligence, part 1**

- [ ] Choose a streaming engine: Eventstream vs Spark Structured Streaming vs KQL
- [ ] Eventstream: sources, destinations, transformations, derived streams
- [ ] Eventhouse: native tables vs OneLake shortcuts, and Query acceleration vs standard shortcuts

**Thu Oct 15 · 1.5 h · KQL**

- [ ] Redo all 11 exercises in `dp700_kql.html` without looking at the answers
- [ ] Operators: `where`, `project`, `extend`, `summarize … by bin()`, `arg_max`, join kinds, `make-series`
- [ ] Update policies vs materialized views: what each is for

**Fri Oct 16 · 1.5 h · Streaming patterns**

- [ ] Window types: tumbling, hopping, sliding, session, snapshot; sketch each over the same 10 events
- [ ] Structured Streaming: `readStream`, `writeStream`, `checkpointLocation`, trigger, `withWatermark`, `foreachBatch`
- [ ] Trace one streaming load end to end: Eventstream → Eventhouse, and Eventstream → Lakehouse

## Week 3 (Sat Oct 17 – Fri Oct 23): Domain 3 and full mocks

This week keeps Domain 3 sharp, absorbs the Oct 19 outline change, and moves from topic study to timed full-length mocks.

**Sat Oct 17 · 4 h · Gate**

- [ ] Microsoft Practice Assessment, fresh attempt; target 80%+
- [ ] Community Mock 1 (kengio study guide) timed at 100 min; target 75%+
- [ ] A gotcha for every miss, with a line on why each wrong option is wrong

**Sun Oct 18 · 4 h · Monitor and troubleshoot**

- [ ] Monitoring hub vs Capacity Metrics app vs workspace monitoring: which question each one answers
- [ ] Semantic model refresh history; an Activator alert on a failed pipeline or job
- [ ] One error drill each: pipeline activity output and retries; Dataflow Gen2 refresh history; notebook Spark UI and logs; Eventhouse `.show ingestion failures`; Eventstream runtime logs; T-SQL syntax a Warehouse rejects; a broken shortcut (path, connection, permission)

**Mon Oct 19 · 1.5 h · New outline goes live; optimize part 1**

- [ ] Re-open the official study guide and compare the workspace-settings and optimize-performance bullets with this doc; add anything new to your notes
- [ ] Lakehouse tables: `OPTIMIZE`, V-Order, Z-Order, `VACUUM`, partitioning, optimized write
- [ ] Warehouse: statistics, caching, and the query insights views

**Tue Oct 20 · 1.5 h · Optimize part 2**

- [ ] Spark: pool sizing, high concurrency sessions, native execution engine, shuffle partitions
- [ ] Pipelines: ForEach sequential vs parallel and batch count, Copy staging and throughput
- [ ] Eventstream and Eventhouse: caching vs retention policy, update policies, materialized views

**Wed Oct 21 · 1.5 h · Mock and fix**

- [ ] Community Mock 2 timed at 100 min
- [ ] Redo the three lowest sub-topics with a matching lab from `dp700_labs.html`

**Thu Oct 22 · 1.5 h · Final gate**

- [ ] Community Mock 3 timed at 100 min; target 80%+
- [ ] Decide: keep Oct 26, or under 70% check the reschedule cutoff in your Pearson VUE confirmation today

**Fri Oct 23 · 1 h · Exam UI and Learn lookups**

- [ ] Run the exam sandbox: case study tabs, mark for review, review screen
- [ ] Lookup drill: find five facts on learn.microsoft.com in under 90 seconds each (a masking function's syntax, `VACUUM`'s default retention, deployment rule types, shortcut source types, a KQL operator's arguments)

## Final 48 hours and exam day

Stop learning new material on Saturday at noon; the last two days are for recall, logistics and sleep.

**Sat Oct 24 · 2 h · Light review**

- [ ] Re-read the trap checklist and every gotcha box in `dp700_notes.html`
- [ ] One untimed 30-question set from the kengio live quiz; review only
- [ ] Nothing new after noon

**Sun Oct 25 · 1 h · Recall and logistics**

- [ ] Trap checklist once more, the KQL operator order, and ROLLUP vs CUBE vs GROUPING SETS
- [ ] Online exam: run the Pearson VUE system test on the same machine and network, clear the desk, set up a closed room, keep ID ready; test center: plan the route
- [ ] Normal bedtime

**Mon Oct 26 · Exam playbook**

1. Light breakfast and one read of the trap checklist. No new material.
2. Pace: check the question count on the first screen and set a halfway checkpoint around minute 45.
3. First pass: answer what you know and mark for review anything that needs a lookup.
4. Use Microsoft Learn only on marked questions, about 2 minutes each. Microsoft says it is designed so you cannot look up everything in time.
5. Read each question's last line first and find the qualifier: least privilege, minimal development effort, lowest latency, no-code. It usually decides between the two plausible options.
6. Case studies: skim the requirements, read the question, then go back to the exact requirement it tests.
7. Avoid breaks: the clock runs and you lose access to every question seen before the break.
8. Never leave a question blank; pick your best option and move on.

## Trap checklist

These are the mistakes you made in earlier practice; re-read them before every mock and once on exam morning.

| Trap | Remember | Notes section |
| --- | --- | --- |
| Pipeline admin role | Manages the deployment pipeline only; it is not workspace Admin or a workspace role | 1.4 |
| Assign vs deploy | Assigning a workspace to a stage only links it; deploying is a separate step | 1.4 |
| Database projects | SDK-style is the Fabric-native project type | 1.5 |
| Native execution engine and UDFs | Your Sep 6 fact-check reversed the old "disable it for UDFs" advice: the engine now supports UDFs | 1.2 |
| High concurrency | Sessions are shared only within one user's notebooks | 1.2 |
| COPY INTO | Warehouse only; know the wildcard path syntax and the rejected-row location option | 2.4 |
| CTAS | Lowest-effort way to combine Warehouse and Lakehouse data into a new table | 2.4 |
| Least privilege on one item | Item permission, never workspace Viewer, which exposes every item | 1.6 |
| Eventhouse vs Lakehouse | Eventhouse is the real-time KQL store; a PySpark + SQL batch scenario points to Lakehouse | 2.7 |
| KQL dynamic columns | `extend` to cast the field, filter on the extended column, then `project` | KQL Ex. 11 |
| ROLLUP / CUBE / GROUPING SETS | `ROLLUP(a,b)` = (a,b), (a), (); `CUBE(a,b)` adds (b); `GROUPING SETS` = only the sets you list | 2.4 |
| Qualifier words | Least privilege, minimal effort, lowest latency and no-code change the right answer | All |

## Sources

- [Study Guide for Exam DP-700, skills measured as of Oct 19, 2026](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) (Microsoft Learn)
- [Microsoft Certified: Fabric Data Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/) (Microsoft Learn): Oct 19 update notice, 100-minute duration, Practice Assessment and exam sandbox links
- [Exam duration and exam experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience) (Microsoft Learn): seat time, breaks, Microsoft Learn access during the exam
- [kengio/dp-700-study-guide](https://github.com/kengio/dp-700-study-guide) (community, MIT license): July 2026 change note, 3 free mocks, live practice quiz; verify its answers against Learn
