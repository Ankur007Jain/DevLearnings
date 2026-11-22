# DP-700 Mock 3 — answer key

Built Nov 16, 2026; every source was opened the same day. **Unverified** marks a point that the Learn page doesn't state directly; it is never the only reason an answer is right.

**Answers:** 1 C | 2 A | 3 D | 4 B | 5 C | 6 B,E | 7 D | 8 B | 9 A | 10 A,D | 11 C | 12 N,Y,Y | 13 N,Y,N | 14 D | 15 A | 16 C | 17 B | 18 D | 19 B | 20 A | 21 C | 22 Y,Y,N | 23 D | 24 C,E | 25 A,C | 26 Y,N,N | 27 A | 28 C | 29 B | 30 D | 31 A | 32 C | 33 B,D | 34 A,E | 35 D | 36 B | 37 Y,N,Y | 38 A | 39 C | 40 B | 41 D | 42 C,D | 43 A | 44 C | 45 B

**Domains** (D1 = Implement and manage, D2 = Ingest and transform, D3 = Monitor and optimize)

- D1 (16): 2, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 44
- D2 (14): 1, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41
- D3 (15): 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45
- Scoring: all-or-nothing per question (choose-two needs both; Yes/No needs all three). A practice target of 32/45 (about 70%) is a reasonable line; it isn't how Microsoft scores the exam.

**Skill map** (study guide last updated 2026-10-30)

- D1: Spark settings 37 | domain settings 13 | OneLake settings 43 | data workflow (Airflow) settings 28 | version control 31 | database projects 40 | deployment pipelines 25 | workspace + item access 7 | row/column-level + DDM 4 | object-level 16 | file-level (OneLake security) 2 | sensitivity labels 22 | endorse 34 | pipeline vs notebook 44 | schedules/event triggers 10 | parameters/dynamic expressions 19
- D2: full/incremental 8, 14 | dimensional prep 26 | streaming loading pattern 23 | data store 23, 41 (light) | dataflows/notebooks/T-SQL choice 41 | shortcuts 17 | mirroring 1 | pipelines ingest 35 | PySpark/SQL/KQL transform 11, 32, 38 | denormalize 41 | group/aggregate 32 | duplicates/late 20, 38 | streaming engine 29 | eventstreams 29 | structured streaming 38 | KQL processing 20 | windowing 5
- D3: monitor ingestion + transformation 45 | semantic model refresh 27 | alerts 9 | pipeline errors 3 | dataflow errors 36 | notebook errors 18 | eventhouse errors 24 | eventstream errors 6 | T-SQL errors 12 | lakehouse table 33 | pipeline 39 | warehouse 15 | eventstream/eventhouse 21 | Spark 30 | query 42

---

**Q1 — C.** Deciding sentences: Existing environment "CDC is enabled" + BR1 (no ETL, replication must not consume CUs). Learn: "Azure SQL Database can't be mirrored if the database has: enabled Change Data Capture (CDC), Azure Synapse Link for SQL, or the database is already mirrored in another Fabric workspace." Replication compute is free ("doesn't consume capacity").
- A wrong: mirroring can't be created while CDC is enabled. B wrong on BR1: a Copy job is an ETL item to schedule and maintain and it uses capacity (valid on its own for capturing changes, breaks BR1). D wrong: shortcut sources don't include Azure SQL Database (list: S3, S3 compatible, ADLS Gen2, Blob, Dataverse, GCS, Iceberg, OneDrive/SharePoint).
- Traps: only a writable primary; SAMI/UAMI must be on; RLS/DDM/column permissions are not propagated; max 1,000 tables.
- Sources: https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-limitations ; https://learn.microsoft.com/en-us/fabric/mirroring/overview ; https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts

**Q2 — A.** Deciding: environment (shared with Read all Apache Spark = ReadAll) + KI1 + TR1. Learn: DefaultReader members = "All users with ReadAll permission" (virtualized); roles combine "by using a union, or least-restrictive, model"; "You can modify or remove the default role... If you delete DefaultReader, users who relied on that role lose data access, even if they still have ReadAll."
- B wrong: roles apply across engines; problem is in Spark. C wrong: roles apply to users with item permissions; Viewer would expose every item in the workspace (breaks TR2) and doesn't remove DefaultReader access. D wrong: role is a month old (definition changes ~5 min, group changes ~1 hour).
- Unverified: Learn doesn't describe removing a single user from DefaultReader; it says modify or remove the role.
- Sources: https://learn.microsoft.com/en-us/fabric/onelake/security/data-access-control-model

**Q3 — D.** Deciding: environment "Enable staging ... Workspace staging" + KI3 "about 60 minutes". Learn: "Workspace staging times out after 60 minutes. For long-running jobs, it's recommended to use external storage for staging." External staging = Azure Blob Storage or ADLS Gen2 connection.
- A wrong: not the activity timeout (default 12 h). B wrong: Contributor is what workspace staging needs and shorter copies succeed. C wrong: no incompatible rows involved.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity

**Q4 — B.** BR3: rows by region = RLS (security policy + filter predicate, silently filters); NationalId must FAIL = column-level security (GRANT SELECT on the allowed column list; Msg 230 on SELECT * or the column); last four digits = dynamic data masking partial(). Agents have no workspace role and only Read (connect), so grants/masks apply.
- A wrong: default() mask returns masked values, the query succeeds; CLS can't show last four. C wrong: CLS doesn't filter rows; DENY on the table blocks everything. D wrong on all three.
- Traps: Admin/Member/Contributor see unmasked data; masking doesn't stop inference through WHERE; RLS applies to everyone incl. dbo.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/row-level-security ; .../column-level-security ; .../dynamic-data-masking

**Q5 — C.** BR2 "within any 10-minute period" + "only when a meter's count changes, not on a fixed schedule". Learn (sliding): "outputs events only for those points in time when the content of the window actually changes, in other words when an event entered or exits the window"; example HAVING COUNT(*) > 3 with SlidingWindow(minute,5).
- A wrong: tumbling is fixed, back to back, outputs at each window end; a burst across a boundary is split. B wrong: hopping outputs at every hop (scheduled overlapping windows). D wrong: session groups by gaps (timeout), can extend far beyond 10 minutes.
- Unverified: Fabric's own Group by text names tumbling and sliding windows only; the detailed semantics come from the Stream Analytics query reference.
- Sources: https://learn.microsoft.com/en-us/stream-analytics-query/sliding-window-azure-stream-analytics ; hopping-window... ; session-window... ; https://learn.microsoft.com/en-us/training/modules/explore-event-streams-microsoft-fabric/4-route-event-data-to-destinations

**Q6 — B,E.** KI2. Learn: on publish, ingestion and routing both start with Now; "data ingestion may begin faster than data routing... this data may not be routed to the destination. A common example is a database CDC source". Steps: uncheck Activate ingestion (Lakehouse or Eventhouse processing-mode destination), manually activate after publish, use Custom time with an earlier timestamp.
- A wrong: not a throughput problem. C wrong: Now is the default behaviour that causes the gap. D wrong: a derived stream doesn't change start order.
- Unverified: Learn doesn't say whether Custom time can re-deliver rows (duplicates).
- Sources: https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/pause-resume-data-streams

**Q7 — D.** Contributor: write/execute notebooks and pipelines, can't add members. Member: "Add members or others with lower permissions", "Allow others to reshare items"; can't update/delete workspace or add admins. Omar: one item only = item permission; ReadData ("Read all data using SQL") = db_datareader equivalent.
- A wrong: Member/Admin too much; Viewer sees every item. B wrong: Viewer sees every item. C wrong: Admin too much; ReadAll is Spark/OneLake, not T-SQL.
- Sources: https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces ; https://learn.microsoft.com/en-us/fabric/data-warehouse/share-warehouse-manage-permissions

**Q8 — B.** CDC-based incremental copy replicates inserts, updates and deletes; "For CDC with merge, rows are inserted, updated, or deleted." Merge uses the primary key by default.
- A wrong: Append keeps history (duplicates) and watermark tracks inserts/updates only. C wrong: watermark doesn't capture deletes. D wrong: SCD Type 2 keeps versions and soft-deletes.
- Unverified: Learn implies, rather than states, that watermark copy misses deletes ("use it when you only need to track inserts and updates").
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/what-is-copy-job

**Q9 — A.** Free failure emails: "Failure notifications apply only to scheduled runs, not to manual runs" and only failures. Activator-based rules: "more job events (such as Started and Succeeded)", menu "Alerts (paid)", prerequisite "Enable workspace monitoring". Preview.
- B wrong: no Succeeded event in free emails. C wrong: failure emails are for scheduled runs. D wrong: failure notifications don't fire on success.
- Unverified: Learn doesn't say whether Activator rules cover manual runs, or name the channels.
- Sources: https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub-alerts

**Q10 — A,D.** Event trigger on Azure Blob events, filter with the Subject field; file name = @pipeline()?.TriggerEvent?.FileName; the ? handles NULL "during manual testing".
- B wrong: schedules aren't event-based ("as soon as"). C wrong: not the Fabric expression. E wrong: without ? the manual-test requirement fails.
- Unverified: Learn's Fabric page doesn't mention triggerBody at all; it only documents the pipeline()?.TriggerEvent form.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs ; https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-storage-event-triggers

**Q11 — C.** "The default is innerunique" = "Inner join with left side deduplication". kind=inner = standard inner join.
- A wrong: on ColumnName is valid for same-named columns. B, D wrong: order isn't the cause; filter early is the best practice.
- Related: best practice says put the table with fewest rows on the left; lookup when the right side is small.
- Sources: https://learn.microsoft.com/en-us/kusto/query/join-operator?view=microsoft-fabric

**Q12 — N,Y,Y.** (1) No: "If you use T-SQL to change your isolation level, the change is ignored at query execution time and snapshot isolation is applied." (2) Yes: "Write-write conflicts ... are possible at the table level ... If two transactions attempt to modify different rows in the same table, they can still conflict." (3) Yes: "The first transaction to commit completes successfully and the other transactions are rolled back"; retry logic + exponential backoff; avoid concurrent UPDATE/DELETE/MERGE on the same table.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions

**Q13 — N,Y,N.** (1) No: domain admins "can't delete the domain, change the domain name, or add/delete other domain admins". (2) Yes: delegated certification settings (enable/disable, "Specify certifiers", documentation URL) with the Override tenant admin selection checkbox. (3) No: "If the workspace already has a domain assignment, it is preserved. The default domain doesn't override the current assignment."
- Sources: https://learn.microsoft.com/en-us/fabric/governance/domains

**Q14 — D.** Limits: "Each query can handle up to 50 buckets" and "For your entire dataflow, the limit is 150 buckets total." 36 per query is fine; 5 x 36 = 180 breaks the total. Quarter: 5 x 12 = 60. Split: 108 and 72.
- A wrong: 36 is under 50. B wrong: replace is the only supported method. C wrong: fixed schema is required.
- This is the mirror image of mock 2 Q20 (per-query cap broke there).
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh

**Q15 — A.** "disabling V-Order can only be done at the warehouse level, and it is irreversible: once disabled, it cannot be enabled again." "Microsoft Fabric Direct Lake mode depends on V-Order." Useful only for write-intensive staging warehouses; keep staging in a separate warehouse.
- B wrong: irreversible. C wrong: warehouse level only. D wrong: can't re-enable.
- Unverified: today's page didn't show the T-SQL command or state the default.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/v-order

**Q16 — C.** Read (share with no extra permissions) "only allows the recipient to connect"; then "provided access to objects ... using T-SQL GRANT". 
- A wrong: ReadData = all tables and views; new objects readable until denied; more effort. B wrong: Viewer sees every item; RLS filters rows, not objects. D wrong: "You can't explicitly run CREATE USER"; "Without Read permission at a minimum, the connection fails."
- Unverified: Learn's granular-permissions page doesn't state DENY-over-GRANT precedence.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/share-warehouse-manage-permissions ; https://learn.microsoft.com/en-us/fabric/data-warehouse/sql-granular-permissions

**Q17 — B.** "In the Tables folder, you can create shortcuts only at the top level." "OneLake doesn't recognize any shortcut containing a space in the name as a Delta table."
- A wrong: Files has no table discovery. C wrong: space in name. D wrong: subdirectory not supported; caching is for GCS, S3, S3-compatible and gateway shortcuts.
- Sources: https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts

**Q18 — D.** "inline commands are turned off by default in pipeline runs and aren't recommended for pipelines"; "Install libraries in an environment and use the environment in a pipeline instead."
- A wrong: !pip installs only on the driver node. B is the trap: it does enable %pip in a pipeline, but "%pip install can produce inconsistent results from run to run" (breaks "same versions every run", not the recommended approach). C wrong: "%pip install isn't supported in High Concurrency mode."
- Unverified: Learn doesn't state the exact error a disabled inline install produces.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/library-management

**Q19 — B.** Tutorial's exact pattern: '@{activity('LookupOldWaterMarkActivity').output.firstRow.WatermarkValue}'. Inside longer text an expression must be wrapped in @{ }.
- A wrong: a bare @ in the middle of text isn't evaluated. C wrong: with First row only selected the shape is firstRow, not value. D wrong: @@ is the escape for a literal @.
- Unverified: Learn's Lookup page names the two shapes (firstRow vs value) but doesn't spell out the value syntax.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/tutorial-incremental-copy-data-warehouse-lakehouse ; https://learn.microsoft.com/en-us/fabric/data-factory/expression-language ; https://learn.microsoft.com/en-us/fabric/data-factory/lookup-activity

**Q20 — A.** backfill: "Whether to create the view based on all records currently in SourceTable (true), or to create it from now on (false). Default is false." "When using this option, the create command must be async." Dedup: "If you need to constantly deduplicate a table, use materialized views" (take_any/arg_max).
- B wrong: created empty, only records ingested after creation. C wrong: backfill needs async. D wrong: query-time dedup costs "extra query time and load on the CPU every time the data is queried".
- Sources: https://learn.microsoft.com/en-us/kusto/management/materialized-views/materialized-view-create?view=microsoft-fabric ; https://learn.microsoft.com/en-us/azure/data-explorer/dealing-with-duplicates

**Q21 — C.** Low <10, Medium 10-100, High >100 MB/s. "deactivate all nodes that support pause and resume, then reactivate them after the update. The update isn't blocked if only nodes that don't support deactivation remain active". Custom endpoint source and Eventhouse (Direct Ingestion) destination don't support pause/resume.
- A wrong: those nodes can't be deactivated; High not needed. B wrong: must deactivate first. D wrong: step 2 isn't possible.
- Related: Event Hubs with fewer than 4 partitions caps throughput (1 partition about 9 MB/s, 3 about 10 MB/s); with 4, 16 or 32 the level decides.
- Sources: https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/configure-settings ; .../pause-resume-data-streams

**Q22 — Y,Y,N.** Supported: Power BI to Power BI, Fabric to Fabric, Fabric to Power BI. Not supported: Power BI to Fabric. "Downstream inheritance never overwrites labels that were applied manually."
- Sources: https://learn.microsoft.com/en-us/fabric/governance/information-protection ; https://learn.microsoft.com/en-us/fabric/governance/service-security-sensitivity-label-downstream-inheritance

**Q23 — D.** OneLake availability exposes KQL data as Delta in OneLake with "no extra storage cost"; default write delay "Up to 3 hours, or until files of sufficient size"; range 5 minutes to 3 hours via TargetLatencyInMinutes in the mirroring policy.
- A wrong: second ingestion path and second copy. B wrong: default can lag up to 3 hours. C wrong: opposite direction.
- Traps: shorter delay = more small files; while enabled you can't rename tables, alter column types, apply RLS, or delete/truncate/purge.
- Sources: https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-house-onelake-availability

**Q24 — C,E.** Non-transactional: "data is ingested only to the source table and not to the target table. In this scenario, ingestion operation is successful." Find failures: .show ingestion failures | where ... OriginatesFromUpdatePolicy == true. Transactional: data in neither table, ingestion unsuccessful; recommended in production.
- A wrong: 0s soft-delete requires a transactional policy and would stop keeping raw rows. B wrong: Source is the triggering table (Raw). D wrong: a materialized view aggregates, it doesn't parse and route rows.
- Sources: https://learn.microsoft.com/en-us/kusto/management/update-policy?view=microsoft-fabric ; https://learn.microsoft.com/en-us/kusto/management/ingestion-failures?view=microsoft-fabric

**Q25 — A,C.** Rules table: notebook = default lakehouse rule only; semantic model = data source and parameter rules. "you must be the owner of the item"; "Deployment rules can't be created in the development stage"; rules "only take effect the next time you deploy to that stage."
- B wrong: no rules in the development stage. D wrong: notebooks have no parameter rule. E wrong: reassigning loses rules and fixes nothing.
- Sources: https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/create-rules

**Q26 — Y,N,N.** "guaranteed unique, but the values aren't necessarily sequential or ordered, and gaps can occur"; "Only the bigint data type is supported"; "Adding an IDENTITY column to an existing table with ALTER TABLE isn't supported" (use CTAS or SELECT...INTO).
- Related: no seed/increment; IDENTITY_INSERT is supported.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/identity

**Q27 — A.** Setting "Keep your Direct Lake data up to date" is "enabled by default"; "you might need to allow completion of data preparation jobs or an ... ETL process before exposing any new data ... When disabled, you can trigger a refresh manually ..., on a refresh schedule, or programmatically". Refresh = framing (metadata, seconds). Activity: Wait on completion on by default; outcome in the pipeline Output tab.
- B wrong: with the setting on, framing happens whenever changes are detected. C wrong: Import copy and a clock schedule aren't tied to the job. D wrong: fallback isn't a consistency mechanism and no refresh appears in the pipeline.
- Sources: https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works ; https://learn.microsoft.com/en-us/fabric/data-factory/semantic-model-refresh-activity

**Q28 — C.** Starter pool: "Shuts down after 20 minutes of inactivity", resume "up to 5 minutes", suggested Developer. Custom pool: "Always on until manually paused", suggested Production; "Each node provides the capacity to run three more workers." Location: Workspace settings, Data Factory, Apache Airflow Runtime Settings.
- A wrong: starter pool shuts down. B wrong: autoscale and extra nodes are custom pool properties. D wrong: Spark pools don't run Airflow DAGs.
- Unverified: Learn doesn't say who may change these settings.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/apache-airflow-jobs-workspace-settings

**Q29 — B.** Group by: "aggregations across all events within a certain time window"; Aggregate: "every time a new event occurs over a period of time". Operators are supported before Eventhouse (event processing before ingestion), Lakehouse, derived stream, Activator.
- A wrong twice: Aggregate isn't one row per interval; Direct ingestion can't follow an operator. C wrong: needs Spark code. D wrong: needs KQL.
- Sources: https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview ; .../process-events-using-event-processor-editor

**Q30 — D.** "Autotune is compatible with Runtime 1.2. You can't enable it on runtime versions later than 1.2." "It doesn't run when high concurrency mode or private endpoint is enabled."
- A wrong: about 20 to 25 iterations. B wrong: it tunes shuffle partitions, autoBroadcastJoinThreshold, maxPartitionBytes. C wrong: enabled per environment or session; disabled by default.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/autotune

**Q31 — A.** Permissions table: "Branch out to another workspace: Admin, Member, Contributor" (Git: Read + Create branch). Switch branch: Admin, or Member/Contributor only with the workspace setting on. Commit needs "branch policy should allow direct commit". Connect/disconnect: Admin.
- B wrong: she isn't Admin and the setting is off; it would also change the shared workspace. C wrong: branch policy. D wrong: Admin only.
- Sources: https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-integration-process ; https://learn.microsoft.com/en-us/fabric/cicd/git-integration/branched-workspace

**Q32 — C.** ROLLUP(Region, Territory) = (Region, Territory), (Region, NULL), (NULL, NULL). CUBE adds (NULL, Territory). GROUPING SETS returns exactly the listed sets.
- Sources: https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=fabric

**Q33 — B,D.** "V-order is disabled by default for all newly created workspaces"; table property: "only future writes to the table are affected. Parquet files keep the ordering used when it was created" (rewrite through OPTIMIZE / table compaction; maintenance dialog has Apply V-order).
- A wrong: session-level default applies to all Parquet writes in sessions that use the environment (adds write time to bronze/silver, about 15%). C wrong: VACUUM only removes unreferenced files. E wrong: writeHeavy is already the default and has V-Order off.
- Unverified: Learn doesn't state in one sentence that table property = true wins when the session default is false; it says the property controls future writes to the table.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order ; .../configure-resource-profile-configurations ; .../lakehouse-table-maintenance

**Q34 — A,E.** "Any user with write permissions on an item can promote it"; "Any Fabric or Power BI item except Power BI dashboards can be promoted"; "Any user can request certification for an item, but only users specified by a Fabric administrator can actually certify"; master data only by specified users.
- Sources: https://learn.microsoft.com/en-us/fabric/governance/endorsement-overview

**Q35 — D.** "The Lookup activity can return up to 5,000 rows; if the result set contains more records, the first 5,000 rows are returned." 4 MB overflow makes the activity fail (so not B).
- A wrong: ForEach items limit is 100,000; batch count is parallelism (default 20, max 50). C wrong: 120 is activities defined per pipeline.
- Unverified: the Fabric page states the limit, not the workaround; paging the control table in ranges is the logical consequence.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/lookup-activity ; https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-limitations

**Q36 — B.** Documented cause: a nullable column detected as non-nullable. Documented fix: delete the table, remove the destination, Table.TransformColumnTypes with type nullable ..., add the destination again.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings

**Q37 — Y,N,Y.** (1) Yes: affects user-submitted jobs incl. "notebook runs orchestrated through a pipeline"; not system-managed jobs such as "Lakehouse table maintenance operations, such as optimize and vacuum". (2) No: it turns OFF optimistic job admission (on by default). (3) Yes: default 20 minutes.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/workspace-admin-settings

**Q38 — A.** "Watermarks advance when Spark processes new input. If no data arrives, a watermark might not advance, so window output ... can be delayed until a later microbatch receives data."
- D wrong and contradicts Learn: "Data older than the watermark might still be processed, but Spark doesn't guarantee it."
- Unverified: Learn's page doesn't define append-mode emission; C is ruled out because Learn describes Optimize Write as file sizing only.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/structured-streaming-stateful-processing

**Q39 — C.** ForEach runs sequentially or in parallel with Batch count; "ForEach parallelism" default 20, maximum 50.
- A wrong: never 600 at once (default 20). B wrong: above 50 and above the source limit. D wrong: still one table at a time.
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-limitations (ForEach activity page fetched earlier on Nov 16)

**Q40 — B.** Add Database Reference (project or .dacpac), "Same server, different database", SQLCMD variable such as [$(MarketingWarehouseName)]; build must show no SQL71501; publish the referenced warehouse first; no mutual dependencies.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/cross-warehouse-development-database-projects

**Q41 — D.** "Use ... INSERT...SELECT, SELECT INTO, or CREATE TABLE AS SELECT (CTAS) to read data from tables that reference other warehouses, lakehouses, or mirrored databases within the same workspace." Endpoint: "Creating, altering, and dropping tables, and insert, update, and delete operations are only supported in Warehouse ..., not in the SQL analytics endpoint".
- A wrong: no table DDL in the endpoint. B, C wrong: other tools/engines, not one T-SQL statement.
- Sources: https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data ; https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area

**Q42 — C,D.** "Apply predicates that act upon datetime table columns first." "Use the has operator. Don't use contains. When looking for full tokens, has works better."
- A wrong: documented anti-pattern (extend then filter). B, E wrong: change the result.
- Sources: https://learn.microsoft.com/en-us/kusto/query/best-practices?view=microsoft-fabric

**Q43 — A.** OneLake diagnostics: Workspace settings, OneLake tab, "Add diagnostic events to a lakehouse"; JSON logs in a lakehouse "within the same capacity"; needs workspace admin + contributor on the lakehouse; covers API access and cross-workspace shortcuts; optional immutability.
- B wrong: needs the Audit Logs role (tenant-level) and isn't files in a lakehouse. C wrong: item logs in a monitoring Eventhouse (KQL). D wrong: caching.
- Unverified: Learn doesn't give the allowed immutability period.
- Sources: https://learn.microsoft.com/en-us/fabric/onelake/onelake-diagnostics-overview

**Q44 — C.** Pipeline: schedule, Copy through gateway, stored procedure, semantic model refresh, failure email for scheduled runs. runMultiple: DAG with dependencies, retry, concurrency; "Parallel notebooks share compute resources within a single Spark session."
- B wrong: run() runs one notebook and has no dependency or retry fields.
- Sources: https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-run ; https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs

**Q45 — B.** Workspace monitoring: "pipeline and activity-level execution logs in an eventhouse" (KQL). Pipeline Spark activity: "deep links ... view Spark application execution details, the respective notebook and Spark job definition snapshot, and access Spark logs". Monitor hub: "centralized portal for browsing Spark activities across items".
- Sources: https://learn.microsoft.com/en-us/fabric/data-factory/monitor-pipeline-runs ; https://learn.microsoft.com/en-us/fabric/data-engineering/spark-monitoring-overview
