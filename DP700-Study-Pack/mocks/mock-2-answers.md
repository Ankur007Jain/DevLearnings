# DP-700 Mock 2 — answer key

**Answers:** 1C 2A 3D 4B 5A | 6D 7B 8C 9A 10D 11B 12C 13A 14D 15C | 16B 17A 18D 19B 20C 21D 22A 23B 24C 25A 26D 27C 28B 29D 30A | 31C 32D 33A 34B 35D 36C 37B 38A 39C 40D 41B 42A 43C 44B 45D

Domains: Q1–15 Implement and manage an analytics solution, Q16–30 Ingest and transform data, Q31–45 Monitor and optimize an analytics solution.

Sources are Microsoft Learn pages, checked on Nov 16, 2026 (URLs where recorded, otherwise the page title). **Unverified** marks a point that the Learn page doesn't state directly; it is never the only reason an answer is right.

**Q1 — C.** Pipelines use gateway 3000.214.2+, outbound *.frontend.clouddatahub.net, connection under On-premises. A: a managed private endpoint is not for pipelines/SQL Server; B: trusted workspace access is for storage only; D: workspace identity doesn't reach on-premises servers. Sources: On-premises data gateway.

**Q2 — A.** Workspace identity + F SKU + resource instance rule via ARM/PowerShell + storage RBAC. B portal can't create rule; C trial unsupported; D My workspace not supported. Sources: Trusted workspace access; Workspace identity.

**Q3 — D.** Trusted workspace access doesn't cover Spark; use managed private endpoint (workspace admin). Unverified: Learn page silent on approval step. Sources: Trusted workspace access; Managed private endpoints.

**Q4 — B.** Variable library, value set per stage, one active set per workspace/stage. C can't be all active; A/D manual. Sources: Variable library.

**Q5 — A.** Audit logs in Purview portal, Audit Logs role in Exchange Online, default 7 days. B/C don't give who-did-what; D workspace monitoring needs Contributor+ and isn't the audit log. Sources: Track user activities/audit logs.

**Q6 — D.** Starter pools unsupported with Tenant Private Links/Managed VNets; on-demand 2-5 min. Sources: Spark compute/starter pools. Unverified: Learn page doesn't say here that creating a private endpoint itself turns on Managed VNet; stem states it as given.

**Q7 — B.** Default max 5, spark.highConcurrency.max range 2-50 in Environment. D out of range; C opposite; A irrelevant. Sources: High concurrency.

**Q8 — C.** Full mode for >10 packages/production/pipelines/Spark job definitions/.jar. Quick: notebooks only, no .jar; %pip session-scoped. Sources: Environment libraries.

**Q9 — A.** Parallel + batch count; children run sequentially per item; @item(). Sources: ForEach activity. Unverified: Learn silent on default/max batch count.

**Q10 — D.** Timeout D.HH:MM:SS, retry count 2, interval in seconds (default 30). Sources: Activity overview.

**Q11 — B.** SDK-style database project, MSSQL extension, DacFx, .dacpac. D ALTER TABLE is limited. Sources: Warehouse source control.

**Q12 — C.** Restored workspace doesn't get identity back; create a new one; deleted identity can't be restored. Sources: Workspace identity. Unverified: re-granting roles is implied, not stated.

**Q13 — A.** Domain contributor = workspace admin assigns own workspace; domain assignment doesn't change item access; adding contributors/assigning others is domain admin. Sources: Fabric domains.

**Q14 — D.** Copy activity best low-code for moving petabytes, raw binary copy. A Dataflow Gen2 low-medium scenario; B code. Sources: Pipeline/dataflow/Spark decision guide (https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-pipeline-dataflow-spark).

**Q15 — C.** Warehouse = T-SQL, star schema, multi-table transactions, cross-database. A endpoint no table DML; B streaming; D OLTP. Sources: Data store decision guide (https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-data-store).

**Q16 — B.** MERGE GA, IDENTITY, TRUNCATE, #temp supported; triggers, synonyms, recursive queries, SET TRANSACTION ISOLATION LEVEL unsupported. Sources: T-SQL surface area (https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area).

**Q17 — A.** Only nullable ADD; PK/UNIQUE only NOT ENFORCED. B NOT NULL fails; C,D lack NOT ENFORCED. Same src.

**Q18 — D.** Endpoint allows views/functions/procedures, no table DDL/DML. Unverified: Learn doesn't show the Spark UPDATE route; Delta UPDATE via Spark is standard but not quoted on that page. Same src.

**Q19 — B.** Incremental = replace + fixed; Warehouse fixed only; fixed fails publish on mismatch. Sources: Dataflow Gen2 destinations/incremental refresh.

**Q20 — C.** 50/query, 150/dataflow: 3x45=135. A 160, B 60>50, D 175. Same src.

**Q21 — D.** ProcessingTime trigger + Optimized Write (+Auto Compaction). Sources: Structured streaming best practices (https://learn.microsoft.com/en-us/fabric/data-engineering/structured-streaming-best-practices).

**Q22 — A.** Available-now trigger for scheduled incremental, durable checkpoint, separate per query. Same src.

**Q23 — B.** ForeachBatch idempotent (stable keys/batch ID). Same src.

**Q24 — C.** Standard Delta stream expects append-only; use change data feed. Same src.

**Q25 — A.** Explicit schema, quarantine table; inference not recommended for production. Same src.

**Q26 — D.** Inferred member, update in place, not SCD change. Sources: Dimensional modeling/SCD load pattern pages; unverified: Learn gives no join logic for late facts.

**Q27 — C.** Update policy defined on target, source = landing table; transactional true = neither table keeps data, ingestion fails. B wrong table; A/D non-transactional; 0s needs transactional. Sources: Update policy / Kusto docs.

**Q28 — B.** By name = materialized + delta; materialized_view() = materialized part only, max_age. Sources: Materialized views.

**Q29 — D.** @expr keeps type; @@ literal @; @{} always string. Sources: Pipeline expressions.

**Q30 — A.** Dynamic = drop/recreate if schema differs; relationships/measures can be lost; fixed fails publish. Unverified: Learn confirms both options only for Snowflake explicitly; stem grants both offered.

**Q31 — C.** Eligible rules; A runtime constant; B explicit transaction; D >10,000 est rows. Sources: Result set caching (https://learn.microsoft.com/en-us/fabric/data-warehouse/result-set-caching).

**Q32 — D.** Per-query hint. A item-wide. Same src.

**Q33 — A.** Contributor sees own sessions/requests only, can't run dm_exec_connections; only Admin KILL. Sources: Monitor with DMVs (https://learn.microsoft.com/en-us/fabric/data-warehouse/monitor-using-dmv).

**Q34 — B.** Only fix stated is retry; SERIALIZABLE unsupported; D is for connection errors. Sources: Troubleshoot Fabric Data Warehouse (https://learn.microsoft.com/en-us/fabric/data-warehouse/troubleshoot-fabric-data-warehouse).

**Q35 — D.** Same page, tempdb steps.

**Q36 — C.** Same page, transient connection steps.

**Q37 — B.** Same page, CTAS test.

**Q38 — A.** Default 7 days; shorter fails; override in environment Spark properties. Sources: Lakehouse table maintenance (https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance). Unverified: Learn doesn't say whether 2 days is advisable.

**Q39 — C.** ~15% write impact, up to 50% more compression. Same src.

**Q40 — D.** 60 min-24 h interactive rejected; background still runs; running jobs complete. Sources: Throttling. Unverified: exact boundary behavior at 90 min stated by Learn bands.

**Q41 — B.** 430 = Spark capacity; 429 = API rate limit fixes (A,C,D). Sources: Fabric throttling/Spark errors pages. Unverified: another Learn page words 430 as "Spark compute or API rate limit".

**Q42 — A.** Batch duration growing while process rate behind input rate = backlog. Sources: Structured streaming best practices.

**Q43 — C.** AwaitTermination; don't catch and return success; unlimited retries with interval. Same src.

**Q44 — B.** JSON/XML fall back to JVM automatically; Parquet/Delta/CSV supported; detect via plan suffixes/Advisor. Sources: Native execution engine. Unverified: Learn gives no reason for list.

**Q45 — D.** Workspace ID, Statement ID, Distributed request ID, exact error, time. Sources: Troubleshoot Fabric Data Warehouse.
