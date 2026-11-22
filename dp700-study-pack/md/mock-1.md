# DP-700 Mock 1

45 questions in three parts, starting with a case study. One best answer per question unless the question says otherwise. Each answer is hidden under its question, and the full key is at the end. All companies and scenarios are fictional, and the questions were written from Microsoft Learn documentation, not taken from the real exam.


## Part 1, case study: Tallgrass Freight (fictional)

**Overview.** Tallgrass Freight runs a trucking fleet and is building its analytics on Fabric.

**Existing environment.**
- One F64 capacity. Workspaces `Ops-Dev`, `Ops-Test` and `Ops-Prod` are stages of one deployment pipeline.
- An Azure SQL database, `Dispatch`, is the operational system. CDC is enabled on `Dispatch` for a legacy tool that is being retired.
- Trucks send GPS events to an Azure event hub with 2 partitions. An eventstream reads from it.
- Warehouse `FleetDW` has a `Drivers` table with a row-level security policy that filters by region, and a `LicenseNo` column.
- A notebook, `LoadFleet`, uses a different default lakehouse in each stage. It runs nightly on a schedule.
- Workspace monitoring is not enabled.

**Business requirements.**
1. `Dispatch` must be replicated into OneLake in near real time.
2. Auditors may query `Drivers`, but any query that names `LicenseNo` must fail.
3. The on-call team must get an email when the nightly `LoadFleet` run fails, at no extra cost.

**Technical requirements.**
- No pipelines or Copy jobs may be added for replication.
- `LoadFleet` must pick up the correct lakehouse after every deployment, with no manual step.
- The on-call team is an Entra security group plus a vendor engineer who has a B2B guest account.

**Known issues.**
- A workspace Admin validating `Drivers` sees only some rows.
- GPS ingestion is capped near 10 MB/s, even after the eventstream's throughput level was set to High.

**Q1.** What must happen so `Dispatch` can meet requirement 1?
- **A.** Create a Copy job with CDC-based incremental copy
- **B.** Create a metadata mirror of `Dispatch`
- **C.** Disable CDC on `Dispatch`, then set up database mirroring
- **D.** Mirror from a read-only secondary replica of `Dispatch`

<details>
<summary>Show answer</summary>

**Answer: C.** An Azure SQL database can't be mirrored while CDC is enabled, and only a writable primary can be mirrored.

</details>


**Q2.** What explains the GPS ingestion cap?
- **A.** The event hub has fewer than four partitions, which limits throughput whatever the level
- **B.** The F64 capacity is too small for the High level
- **C.** The eventstream's retention period is too short
- **D.** The throughput level applies only to destinations

<details>
<summary>Show answer</summary>

**Answer: A.** Fewer than four Event Hubs partitions limits throughput whatever the level.

</details>


**Q3.** Which change meets requirement 2 and fixes the Admin's issue?
- **A.** Mask `LicenseNo` with dynamic data masking, and grant the Admin `UNMASK`
- **B.** Grant auditors `SELECT` on the allowed columns only, and change the security predicate to include the Admin
- **C.** Grant auditors `SELECT` on the allowed columns only, and rely on the Admin role bypassing row-level security
- **D.** Mask `LicenseNo` with dynamic data masking, and change the security predicate to include the Admin

<details>
<summary>Show answer</summary>

**Answer: B.** Column-level security makes a query that names the column fail; the row-level security predicate must allow the Admin, who doesn't bypass it.

</details>


**Q4.** How do you meet the `LoadFleet` lakehouse requirement?
- **A.** Create a default lakehouse rule in the `Ops-Dev` stage
- **B.** Create a parameter rule on the notebook in each target stage
- **C.** Create a data source rule on the notebook in each target stage
- **D.** Have the notebook's owner create a default lakehouse rule in the `Ops-Test` and `Ops-Prod` stages

<details>
<summary>Show answer</summary>

**Answer: D.** A notebook supports only a default lakehouse rule, created in the target stages by the item owner.

</details>


**Q5.** How do you meet requirement 3?
- **A.** Configure Schedule failure emails in the Monitor hub, with the security group and the vendor's guest account as recipients
- **B.** Create an Activator-based alert rule for the notebook
- **C.** Put the notebook in a pipeline with an Outlook activity on failure
- **D.** Configure Schedule failure emails, typing the vendor's external email address

<details>
<summary>Show answer</summary>

**Answer: A.** Free schedule failure emails go to Entra users, groups and B2B guests. Activator rules are paid and need workspace monitoring.

</details>


## Part 1, standalone questions

**Q6.** In a `runMultiple` DAG, the `Load` notebook must start only after `Extract` finishes, and must retry once after 10 seconds if it fails. Which activity definition does this?
- **A.** `{"name": "Load", "path": "LoadNb", "dependsOn": ["Extract"], "retry": 1}`
- **B.** `{"name": "Load", "path": "LoadNb", "dependencies": ["Extract"], "retry": 1, "retryIntervalInSeconds": 10}`
- **C.** `{"name": "Load", "path": "LoadNb", "concurrency": 1, "timeoutInSeconds": 10}`
- **D.** `{"name": "Load", "path": "LoadNb", "args": {"after": "Extract", "retry": 1}}`

<details>
<summary>Show answer</summary>

**Answer: B.** In a DAG activity, dependencies sets the order, and retry with retryIntervalInSeconds sets the retry.

</details>


**Q7.** A pipeline parameter `myNumber` holds 42. Which expression returns it as a number, not a string?
- **A.** `"@{pipeline().parameters.myNumber}"`
- **B.** `"@@pipeline().parameters.myNumber"`
- **C.** `"pipeline().parameters.myNumber"`
- **D.** `"@pipeline().parameters.myNumber"`

<details>
<summary>Show answer</summary>

**Answer: D.** "@pipeline().parameters.x" returns the value with its type; "@{...}" always returns a string; @@ escapes.

</details>


**Q8.** Where can you create shortcuts in a lakehouse?
- **A.** In Tables only at the top level; in Files at any folder level
- **B.** In Tables at any level; in Files only at the top level
- **C.** At any level in both
- **D.** Only at the top level in both

<details>
<summary>Show answer</summary>

**Answer: A.** Shortcuts go only at the top level of Tables, but at any level of Files.

</details>


**Q9.** A lakehouse has a shortcut `MyShortcut` to an ADLS Gen2 folder, and the user has write permission on that storage. The user deletes the folder `MyShortcut/Foo/Bar` in the lakehouse. What happens?
- **A.** Only the shortcut is removed
- **B.** The delete fails, because shortcuts are read-only
- **C.** The `Bar` folder is deleted in the ADLS Gen2 account
- **D.** `Bar` is hidden in the lakehouse but stays in ADLS Gen2

<details>
<summary>Show answer</summary>

**Answer: C.** Deleting inside a shortcut deletes in the target if you have permission there. Deleting the shortcut removes only the shortcut.

</details>


**Q10.** An Azure SQL database with row-level security and dynamic data masking is mirrored to Fabric. What applies to the mirrored data in OneLake?
- **A.** Both are enforced automatically on the mirrored data
- **B.** Neither is propagated; the data must be secured again in Fabric
- **C.** Row-level security is propagated, masking is not
- **D.** Mirroring fails while either feature is in use

<details>
<summary>Show answer</summary>

**Answer: B.** Row-level security, column permissions and masking on the source aren't propagated to the mirrored data.

</details>


**Q11.** You create a OneLake shortcut in a KQL database. How do you query it?
- **A.** By table name, like any KQL table
- **B.** With the `materialized_view()` function
- **C.** With `OPENROWSET`
- **D.** With the `external_table()` function

<details>
<summary>Show answer</summary>

**Answer: D.** A KQL database treats a shortcut as an external table, queried with external_table().

</details>


**Q12.** A workspace has Amazon S3 shortcuts, and egress costs are high. Files are 200 MB to 3 GB. Which statement about shortcut caching is correct?
- **A.** Turn it on in the workspace's OneLake settings with a retention of up to 28 days; files over 1 GB won't be cached
- **B.** Turn it on with a 90-day retention; all files are cached
- **C.** Caching isn't available for S3 shortcuts
- **D.** Turn it on per shortcut; only files over 1 GB are cached

<details>
<summary>Show answer</summary>

**Answer: A.** Caching covers S3, S3-compatible, GCS and gateway shortcuts; retention is 1 to 28 days; files over 1 GB aren't cached.

</details>


**Q13.** A capacity has used 30 minutes of future capacity. What do users experience?
- **A.** Nothing; this is within overage protection
- **B.** Interactive requests are rejected
- **C.** Interactive requests are delayed by 20 seconds
- **D.** All requests are rejected

<details>
<summary>Show answer</summary>

**Answer: C.** 10 to 60 minutes of future capacity is the interactive delay stage: a 20-second delay.

</details>


**Q14.** A notebook that lists tables in a loop starts failing with HTTP 429. What is the documented fix?
- **A.** Turn on Autoscale Billing for Spark
- **B.** Retry with exponential backoff and jitter, honoring `Retry-After`
- **C.** Grant the user ReadAll on the lakehouse
- **D.** Restart the capacity

<details>
<summary>Show answer</summary>

**Answer: B.** HTTP 429 is an API rate limit: back off with jitter and honor Retry-After. HTTP 430 is the capacity error.

</details>


**Q15.** You connect a workspace to a Git branch for the first time. Both the workspace and the branch already have content. What happens?
- **A.** The connection fails until one side is emptied
- **B.** The branch content always overwrites the workspace
- **C.** The two are merged item by item
- **D.** You must choose a direction: commit overwrites Git, update overwrites the workspace

<details>
<summary>Show answer</summary>

**Answer: D.** When both sides have content you choose a direction: commit overwrites Git, update overwrites the workspace.

</details>


## Part 2

**Q16.** A Dataflow Gen2 must use incremental refresh over the past 2 years into a Lakehouse table. Which configuration is valid?
- **A.** Monthly buckets, replace update method, fixed schema
- **B.** Weekly buckets, replace update method, fixed schema
- **C.** Monthly buckets, append update method, fixed schema
- **D.** Monthly buckets, replace update method, dynamic schema

<details>
<summary>Show answer</summary>

**Answer: A.** Incremental refresh needs replace and a fixed schema, with at most 50 buckets per query (weekly over 2 years is 104).

</details>


**Q17.** Each event in an eventstream carries an array field `items`. Which no-code operator produces one row per array element?
- **A.** Manage fields
- **B.** Group by
- **C.** Expand
- **D.** Union

<details>
<summary>Show answer</summary>

**Answer: C.** Expand creates one row per array value.

</details>


**Q18.** A KQL table `Raw` receives JSON. Each row must be parsed into a typed table at ingestion, the raw rows must not be kept, and a failed transform must lose nothing. Which design?
- **A.** A materialized view over `Raw`
- **B.** A non-transactional update policy, with a `0s` soft-delete on `Raw`
- **C.** A transactional update policy, with the default retention on `Raw`
- **D.** A transactional update policy, with a `0s` soft-delete on `Raw`

<details>
<summary>Show answer</summary>

**Answer: D.** A 0s soft-delete on the source requires a transactional update policy, so a failure loses nothing.

</details>


**Q19.** A Spark stream must drop duplicates by `event_id` alone, with events up to 10 minutes late and bounded state. Which code?
- **A.** `events.dropDuplicates(["event_id"])`
- **B.** `events.withWatermark("event_time", "10 minutes").dropDuplicatesWithinWatermark(["event_id"])`
- **C.** `events.withWatermark("event_time", "10 minutes").dropDuplicates(["event_id", "event_time"])`
- **D.** `events.dropDuplicatesWithinWatermark(["event_id"])` with no watermark

<details>
<summary>Show answer</summary>

**Answer: B.** dropDuplicatesWithinWatermark with a watermark uses event_id alone and keeps bounded state.

</details>


**Q20.** Which value is not a supported `FILE_TYPE` for `COPY INTO` in a Fabric Warehouse?
- **A.** CSV
- **B.** PARQUET
- **C.** AVRO
- **D.** JSONL

<details>
<summary>Show answer</summary>

**Answer: C.** COPY INTO supports CSV, JSONL and PARQUET.

</details>


**Q21.** `DimCustomer` is SCD type 2. A customer changed region in March, which created a new version row. A sale for that customer loads in April. Which key does the fact row get?
- **A.** The surrogate key of the customer's current version
- **B.** The surrogate key of the customer's first version
- **C.** The customer's business key from the source
- **D.** The key of the Unknown member

<details>
<summary>Show answer</summary>

**Answer: A.** The fact load looks up the surrogate key of the dimension's current version.

</details>


**Q22.** A nightly report reads a KQL materialized view. It tolerates slightly stale data and must run as cheaply as possible. How should it query?
- **A.** By the view's name
- **B.** By querying the source table with the same `summarize`
- **C.** By the view's name with `take 100`
- **D.** With `materialized_view("ViewName")`

<details>
<summary>Show answer</summary>

**Answer: D.** materialized_view() reads only the materialized part: cheapest, possibly stale.

</details>


**Q23.** Two procedures run `MERGE` on the same Warehouse table at the same time, touching different rows. One fails with error 24556. What is the fix?
- **A.** Add a `ROWLOCK` hint
- **B.** Run them one after the other, or retry with backoff
- **C.** Set the isolation level to `READ COMMITTED`
- **D.** Enable result set caching

<details>
<summary>Show answer</summary>

**Answer: B.** Conflicts are detected at table level; run sequentially or retry with backoff.

</details>


**Q24.** A Warehouse query finished 5 minutes ago and isn't in `queryinsights.exec_requests_history`. Why?
- **A.** Completed queries can take up to 15 minutes to appear
- **B.** Only failed queries are stored
- **C.** Only workspace Admins can see other users' queries
- **D.** The view exists only for the SQL analytics endpoint

<details>
<summary>Show answer</summary>

**Answer: A.** Completed queries can take up to 15 minutes to appear in query insights.

</details>


**Q25.** In the Lakehouse maintenance dialog, a user runs VACUUM with a 2-day retention. What happens by default?
- **A.** It runs, and time travel is unaffected
- **B.** The retention is rounded up to 7 days
- **C.** The request fails, because the retention is under seven days
- **D.** It deletes the table's whole history

<details>
<summary>Show answer</summary>

**Answer: C.** A VACUUM retention under seven days fails by default.

</details>


**Q26.** With the native execution engine enabled, which job falls back to the regular Spark engine?
- **A.** A join over Parquet files
- **B.** An aggregation over Delta tables
- **C.** A load of CSV files
- **D.** A job that reads JSON files

<details>
<summary>Show answer</summary>

**Answer: D.** The native execution engine supports Parquet, Delta and CSV; JSON and XML fall back.

</details>


**Q27.** A Fabric admin sets a default domain for a security group. One member already administers a workspace that is assigned to another domain. What happens to that workspace?
- **A.** It moves to the default domain
- **B.** It keeps its current domain
- **C.** It belongs to both domains
- **D.** It becomes unassigned

<details>
<summary>Show answer</summary>

**Answer: B.** A default domain doesn't override a workspace's existing domain.

</details>


**Q28.** In a Git-connected workspace, who can commit workspace changes to Git?
- **A.** Only a workspace Admin
- **B.** A Viewer with write access to the repository
- **C.** A Contributor with write permission on all items, and Contribute permission in Git
- **D.** Only a Member

<details>
<summary>Show answer</summary>

**Answer: C.** Commit needs Contributor (write on all items) plus Contribute permission in Git.

</details>


**Q29.** In which case does a sensitivity label flow downstream?
- **A.** From a labeled lakehouse to a Power BI semantic model built on it
- **B.** From a labeled Power BI report to the lakehouse behind it
- **C.** From a labeled report to a .txt export
- **D.** From a tenant's mandatory labeling policy to a new warehouse

<details>
<summary>Show answer</summary>

**Answer: A.** Fabric to Power BI is a supported downstream direction; Power BI to Fabric isn't.

</details>


**Q30.** You edit the definition of a OneLake security role, without changing its members. About how long before the change applies?
- **A.** Immediately
- **B.** About 5 minutes
- **C.** About an hour
- **D.** About 24 hours

<details>
<summary>Show answer</summary>

**Answer: B.** Role definition changes take about 5 minutes; group membership changes about an hour.

</details>


## Part 3

**Q31.** An eventstream SQL operator must output, every minute, the average speed per truck over the last 10 minutes, using the device's `gpsTime`. Which query parts do this?
- **A.** `FROM input` with `HoppingWindow(minute, 10, 1)`
- **B.** `FROM input TIMESTAMP BY gpsTime` with `TumblingWindow(minute, 10)`
- **C.** `FROM input TIMESTAMP BY gpsTime` with `HoppingWindow(minute, 10, 1)`
- **D.** `FROM input TIMESTAMP BY gpsTime` with `SlidingWindow(minute, 10)`

<details>
<summary>Show answer</summary>

**Answer: C.** HoppingWindow for the overlapping window, TIMESTAMP BY for device time.

</details>


**Q32.** An eventstream applies a Filter operator, then sends the result to an Eventhouse. Which ingestion mode does that destination use?
- **A.** Event processing before ingestion
- **B.** Direct ingestion
- **C.** Either mode works after an operator
- **D.** Direct ingestion with a mapping transformation

<details>
<summary>Show answer</summary>

**Answer: A.** Operators before an Eventhouse destination require event processing before ingestion.

</details>


**Q33.** Marketing data in Snowflake must be queryable from Fabric, and no copy may be made in OneLake. Which feature?
- **A.** Database mirroring
- **B.** Open mirroring
- **C.** A Copy job
- **D.** Metadata mirroring

<details>
<summary>Show answer</summary>

**Answer: D.** Metadata mirroring leaves the data in Snowflake. Open mirroring means writing your own replication application.

</details>


**Q34.** An operational application needs high concurrency, ACID transactions and enforced foreign keys. Which Fabric store?
- **A.** Fabric Data Warehouse
- **B.** SQL database in Fabric
- **C.** Lakehouse
- **D.** Eventhouse

<details>
<summary>Show answer</summary>

**Answer: B.** SQL database in Fabric: operational, ACID, enforced foreign keys.

</details>


**Q35.** Which Dataflow Gen2 destination doesn't support the replace update method?
- **A.** Fabric KQL database
- **B.** Lakehouse
- **C.** Warehouse
- **D.** Azure SQL Database

<details>
<summary>Show answer</summary>

**Answer: A.** KQL database (and Azure Data Explorer) destinations don't support replace.

</details>


**Q36.** What does Spark autotune adjust?
- **A.** Executor memory and cores
- **B.** The number of nodes in the pool
- **C.** Shuffle partitions, the broadcast join threshold and the maximum partition bytes
- **D.** V-Order and optimized write

<details>
<summary>Show answer</summary>

**Answer: C.** Autotune adjusts those three Spark settings only.

</details>


**Q37.** Which statement about V-Order in a Fabric Warehouse is correct?
- **A.** It is off by default
- **B.** It can be switched on and off for each table
- **C.** Disabling it makes report queries faster
- **D.** It is on by default, is disabled for the whole warehouse, and can't be re-enabled

<details>
<summary>Show answer</summary>

**Answer: D.** Warehouse V-Order is on by default, is disabled per warehouse, and can't be re-enabled.

</details>


**Q38.** After a nightly load multiplies a Warehouse table's row count, the first query each morning is slow and later ones are fast. What should you add to the load?
- **A.** `OPTIMIZE` on the table
- **B.** `UPDATE STATISTICS` on the heavily used columns
- **C.** Multi-column statistics on the join keys
- **D.** A step that disables automatic statistics

<details>
<summary>Show answer</summary>

**Answer: B.** Statistics refresh synchronously at query time; update them after a big load.

</details>


**Q39.** A KQL table must keep 365 days queryable. Dashboards read only the last 30 days, and cost must come down. What do you set?
- **A.** A 30-day retention policy
- **B.** A materialized view
- **C.** A caching policy that keeps 30 days hot, with retention left at 365 days
- **D.** Nothing; the default caching policy is the cheapest

<details>
<summary>Show answer</summary>

**Answer: C.** Caching policy sets hot data; retention sets queryable data.

</details>


**Q40.** A pipeline must refresh a semantic model so that the refresh commits all at once, and the next activity waits for it to finish. Which settings on the Semantic model refresh activity?
- **A.** Commit mode Transactional, Wait on completion on
- **B.** Commit mode Partial Batch, Wait on completion on
- **C.** Commit mode Transactional, Wait on completion off
- **D.** Commit mode Partial Batch, Wait on completion off

<details>
<summary>Show answer</summary>

**Answer: A.** Transactional commits all at once; Wait on completion holds the next activity.

</details>


**Q41.** An engineer with the Viewer role must find out whether an eventstream's Eventhouse destination is failing to convert events to the output schema, and read the error-level logs. Where?
- **A.** The workspace monitoring database
- **B.** The destination node's Data insights tab, Deserialization errors
- **C.** The eventstream's IncomingMessages metric
- **D.** The destination node's Data insights tab, Data conversion errors, then the Runtime logs tab

<details>
<summary>Show answer</summary>

**Answer: D.** Data conversion errors is the output-side metric; Runtime logs give error detail; a Viewer can see both.

</details>


**Q42.** What does a user need in order to deploy content to a deployment pipeline stage that already has content?
- **A.** Pipeline admin only
- **B.** Pipeline admin, plus at least Contributor in both the source and target workspaces
- **C.** Admin in both workspaces
- **D.** Pipeline admin, plus Viewer in the target workspace

<details>
<summary>Show answer</summary>

**Answer: B.** Pipeline admin plus at least Contributor in both workspaces.

</details>


**Q43.** What does a user need in order to create a OneLake shortcut?
- **A.** Write on the item where the shortcut is created, and Read on the target
- **B.** Read on the item where the shortcut is created, and Write on the target
- **C.** Write on both
- **D.** The Admin role in both workspaces

<details>
<summary>Show answer</summary>

**Answer: A.** Write where the shortcut is created, Read on the target.

</details>


**Q44.** Environments set their own driver and executor sizes, but every notebook runs with the default pool's configuration. Which setting fixes this?
- **A.** Reserve maximum cores for active Spark jobs
- **B.** High concurrency mode for notebooks
- **C.** Customize compute configurations for items
- **D.** Customized workspace pools

<details>
<summary>Show answer</summary>

**Answer: C.** Customize compute configurations for items lets an environment set driver and executor size.

</details>


**Q45.** A lakehouse has OneLake security enabled, and its `DefaultReader` role is deleted. Who keeps data access?
- **A.** Users with the ReadAll item permission
- **B.** Workspace Admins, Members and Contributors
- **C.** Everyone who had access before
- **D.** No one

<details>
<summary>Show answer</summary>

**Answer: B.** ReadAll users lose access; Admins, Members and Contributors keep it through their Write permission.

</details>




## Answer key

<details>
<summary>Show answer</summary>

1. C
2. A
3. B
4. D
5. A
6. B
7. D
8. A
9. C
10. B
11. D
12. A
13. C
14. B
15. D
16. A
17. C
18. D
19. B
20. C
21. A
22. D
23. B
24. A
25. C
26. D
27. B
28. C
29. A
30. B
31. C
32. A
33. D
34. B
35. A
36. C
37. D
38. B
39. C
40. A
41. D
42. B
43. A
44. C
45. B

</details>
