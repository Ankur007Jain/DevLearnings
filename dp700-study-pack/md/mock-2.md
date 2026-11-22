# DP-700 Mock 2 — 45 questions

Rules: 100 minutes total, 3 parts of 15. One best answer per question. No notes, no docs. Each answer is hidden under its question with a one-line reason, and the full key is at the end. All companies and scenarios are fictional, and the questions were written from Microsoft Learn documentation, not taken from the real exam.

Domains: Part 1 = Implement and manage an analytics solution. Part 2 = Ingest and transform data. Part 3 = Monitor and optimize.

---

# PART 1 (Q1–Q15)

## Case study: Redwood Outfitters (Q1–Q5)

Redwood Outfitters is a retailer moving analytics to Microsoft Fabric.
- Orders live in an on-premises SQL Server 2019 in the company datacenter. Inbound internet connections are blocked. Outbound traffic is allowed only to an approved list of hosts.
- Supplier files land in an Azure Data Lake Storage Gen2 account. Its firewall is set to "selected networks" and public access is disabled.
- One F64 capacity hosts three workspaces (Dev, Test, Prod) linked by a deployment pipeline. A separate Sandbox workspace runs on a Fabric trial capacity.
- Engineers use pipelines for ingestion and Spark notebooks for transformation.
- Internal audit must be able to show which user changed which item.

**Q1.** A nightly pipeline in Prod must copy the Orders tables from the on-premises SQL Server into a lakehouse. A gateway VM was installed last year (version 3000.190), and the Copy activity cannot reach the server. What should you do?
- A. Create a managed private endpoint from Prod to the SQL Server and select it in the Copy activity.
- B. Enable trusted workspace access for the SQL Server and create a resource instance rule for Prod.
- C. Upgrade the on-premises data gateway to a version that supports pipelines (3000.214.2 or later), allow outbound access from the gateway machine to *.frontend.clouddatahub.net, and create the connection under On-premises in Manage connections and gateways.
- D. Create a workspace identity for Prod and use it as the credential for the SQL Server connection.

<details>
<summary>Show answer</summary>

**Answer: C.** Pipelines reach on-premises sources only through an on-premises data gateway at version 3000.214.2 or later, with outbound access to `*.frontend.clouddatahub.net`. Managed private endpoints, trusted workspace access and workspace identities are for Azure resources.

</details>

**Q2.** A pipeline in Prod must copy supplier files from the firewall-protected ADLS Gen2 account into a lakehouse. Public network access on the storage account must stay disabled. Which approach meets the requirement?
- A. Create a workspace identity for Prod (on the F64 capacity), grant it Storage Blob Data Contributor on the storage account, and create a resource instance rule for Prod using an ARM template or PowerShell.
- B. Create a workspace identity for Prod, grant it Storage Blob Data Contributor, and create the resource instance rule in the Azure portal under the storage account's Networking blade.
- C. Do the same work in the Sandbox workspace on the trial capacity, using a workspace identity and an ARM-template resource instance rule.
- D. Create the workspace identity in the engineer's My workspace and build the pipeline there, using an ARM-template resource instance rule.

<details>
<summary>Show answer</summary>

**Answer: A.** Trusted workspace access needs a workspace identity on an F SKU capacity plus a resource instance rule, and that rule can be created only with an ARM template or PowerShell, not in the portal. Trial capacities and My workspace don't qualify.

Microsoft Learn: [Trusted workspace access](https://learn.microsoft.com/en-us/fabric/security/security-trusted-workspace-access)

</details>

**Q3.** A Spark notebook in Prod must read the same supplier files directly from the storage account. The pipeline in Q2 already works. What is needed for the notebook?
- A. Nothing. Trusted workspace access that works for the pipeline also covers Spark.
- B. Install an on-premises data gateway and select it as the notebook's Spark pool.
- C. Assign the workspace identity to the Spark environment so sessions run under it.
- D. A workspace admin creates a managed private endpoint from Prod to the storage account.

<details>
<summary>Show answer</summary>

**Answer: D.** Trusted workspace access covers only OneLake shortcuts, pipelines, semantic models, the T-SQL COPY statement and AzCopy. Spark reaches a firewall-protected storage account through a managed private endpoint, which a workspace admin creates.

Microsoft Learn: [Trusted workspace access](https://learn.microsoft.com/en-us/fabric/security/security-trusted-workspace-access) · [Managed private endpoints](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

</details>

**Q4.** Dev, Test and Prod each need a different lakehouse and storage path in their pipelines and notebooks. Requirement: after a deployment pipeline promotes content, nobody edits values by hand. Which design fits?
- A. Create one variable library per workspace and edit the values manually after each deployment.
- B. Create one variable library with a value set for each stage, set the active value set for each deployment pipeline stage, and have items reference the variables.
- C. Create one variable library with three value sets and activate all three at once in every workspace so that each item picks its value at runtime.
- D. Hard-code the values in each item and keep separate Git branches for each stage.

<details>
<summary>Show answer</summary>

**Answer: B.** One variable library holds a value set per stage, each stage's workspace keeps its own active value set, and items reference the variables, so nothing is edited by hand after a deployment.

</details>

**Q5.** Internal audit wants, for the past 30 days, a record of which user did what on which Fabric item. The auditor is not a Fabric admin. What is the correct approach?
- A. Search the audit logs in the Microsoft Purview portal. The auditor needs the Audit Logs role in Exchange Online (for example through the Compliance Management role group) and must set the date range, because the default search covers the past 7 days.
- B. Open the Microsoft Fabric Capacity Metrics app and filter by item to see the users.
- C. Use the monitoring hub in each workspace and filter by "Submitted by".
- D. Enable workspace monitoring and let the auditor, who is a workspace Viewer, query the monitoring database.

<details>
<summary>Show answer</summary>

**Answer: A.** User activity on Fabric items is in the Purview audit log. A non-admin needs the Audit Logs role in Exchange Online, and the search defaults to the past 7 days, so the date range must be widened.

</details>

## Standalone (Q6–Q15)

**Q6.** The Dev workspace now has a Managed VNet configured. Notebooks that used to start in 5–10 seconds now take 2–5 minutes to start. Nothing in the Environment changed. What is the best explanation?
- A. The capacity is being throttled; wait for burndown.
- B. Starter pools need Large nodes; resize the pool.
- C. High concurrency mode was disabled in the workspace.
- D. Starter pools are not supported with Managed VNets, so sessions start on on-demand compute that takes minutes. This is expected.

<details>
<summary>Show answer</summary>

**Answer: D.** Starter pools aren't available in a workspace with a Managed VNet, so sessions start on on-demand compute, which takes a few minutes. This is expected.

</details>

**Q7.** A pipeline runs 12 notebooks. All use the same user, the same default lakehouse configuration, and the same Environment with identical Spark compute settings. Only 5 notebooks share one session and the rest start new sessions. What should you change?
- A. Switch the Environment publish mode to Quick.
- B. In the Environment, set spark.highConcurrency.max to 12 (the allowed range is 2–50).
- C. Give each notebook a different default lakehouse so they split across sessions evenly.
- D. In the Environment, set spark.highConcurrency.max to 60.

<details>
<summary>Show answer</summary>

**Answer: B.** `spark.highConcurrency.max` sets how many notebooks share one session. The default is 5 and the allowed range is 2 to 50, so 12 is valid and 60 isn't.

</details>

**Q8.** An Environment must carry 25 Python packages plus one custom .jar. The Environment is used by production pipelines running Spark job definitions. Which publish mode do you choose?
- A. Quick mode, because publishing takes about 5 seconds.
- B. Quick mode, with %pip install at the top of each notebook.
- C. Full mode.
- D. Quick mode, uploading the .jar as a custom library.

<details>
<summary>Show answer</summary>

**Answer: C.** Quick mode applies to notebooks only, so an environment used by Spark job definitions must be published in Full mode.

</details>

**Q9.** A pipeline must process 40 files. For each file it runs a Copy activity and then a Script activity, in that order. Up to 10 files may be processed at the same time. Which configuration is correct?
- A. ForEach in parallel mode with batch count 10. Place Copy and Script inside the ForEach, linked with an on-success dependency, and reference the file with @item().
- B. ForEach in sequential mode with batch count 10.
- C. ForEach in parallel mode, with Copy and Script placed inside with no dependency, so both run at the same time within each iteration.
- D. ForEach in parallel mode with batch count 40, because batch count caps how many items complete.

<details>
<summary>Show answer</summary>

**Answer: A.** Parallel ForEach with batch count 10 caps concurrency at 10. Copy and Script stay in order inside each iteration through an on-success dependency, and `@item()` gives the current file.

</details>

**Q10.** A Copy activity occasionally hangs. It should be failed after 2 hours and retried twice, waiting 5 minutes between attempts. Which activity settings do this? (Timeout format is D.HH:MM:SS; the retry interval is in seconds.)
- A. Timeout 0.02:00:00, Retry 2, Retry interval 5
- B. Timeout 2.00:00:00, Retry 2, Retry interval 300
- C. Timeout 0.02:00:00, Retry 1, Retry interval 300
- D. Timeout 0.02:00:00, Retry 2, Retry interval 300

<details>
<summary>Show answer</summary>

**Answer: D.** Timeout uses D.HH:MM:SS, so 2 hours is `0.02:00:00`; Retry 2 gives two retries, and the interval is in seconds, so 5 minutes is 300.

</details>

**Q11.** The warehouse team wants to develop schema changes offline in VS Code, validate them at build time, produce a deployable artifact, and release it to Test and Prod from a CI pipeline without using the Fabric portal. What should they use?
- A. Export the schema from the Visual query editor and edit it by hand.
- B. A SQL database project (SDK-style) with the MSSQL extension for VS Code, built into a .dacpac and deployed with SqlPackage/DacFx.
- C. A Spark job definition that runs Delta DDL against the warehouse.
- D. A notebook that runs ALTER TABLE for every change, because the warehouse supports all ALTER TABLE operations.

<details>
<summary>Show answer</summary>

**Answer: B.** An SDK-style SQL database project in VS Code builds to a .dacpac that SqlPackage or DacFx deploys from a CI pipeline, with build-time validation.

</details>

**Q12.** A deleted workspace was restored. Pipelines that authenticated to storage with the workspace's identity now fail. What is the correct fix?
- A. Restore the deleted workspace identity from the Entra recycle bin.
- B. Wait one hour; a restored workspace regains its identity automatically.
- C. Create a new workspace identity in the restored workspace and re-grant it the required storage roles.
- D. Raise the tenant limit on workspace identities (default 10,000).

<details>
<summary>Show answer</summary>

**Answer: C.** A workspace identity isn't restored with the workspace, so create a new identity and grant it the storage roles again.

</details>

**Q13.** Priya is a workspace admin of Marketing-Analytics. A Fabric admin added her as a domain contributor of the Marketing domain. Which statement is correct?
- A. She can assign her own workspace to the Marketing domain, and the assignment does not change who can access items in it.
- B. She can assign any workspace to the domain and add other domain contributors.
- C. She must have a Fabric admin approve each workspace assignment.
- D. Assigning the workspace gives the domain's admins the workspace Admin role.

<details>
<summary>Show answer</summary>

**Answer: A.** A domain contributor can assign only workspaces they are an admin of, and domain assignment doesn't change who can see or access items.

Microsoft Learn: [Domains](https://learn.microsoft.com/en-us/fabric/governance/domains)

</details>

**Q14.** A team without Spark skills must move about 80 TB of raw binary files nightly from SFTP and Blob storage into a bronze lakehouse. There is no transformation. They want a low-code tool on a schedule. Which tool fits best?
- A. Dataflow Gen2
- B. A Spark notebook
- C. An eventstream
- D. A pipeline Copy activity

<details>
<summary>Show answer</summary>

**Answer: D.** A pipeline Copy activity is the low-code choice for large binary copies with no transformation, on a schedule.

</details>

**Q15.** A new analytical store needs T-SQL authoring, a star schema, multi-table transactions, cross-database queries and UPDATE/DELETE support through T-SQL. Which item do you create?
- A. Lakehouse, queried through its SQL analytics endpoint
- B. Eventhouse
- C. Warehouse
- D. SQL database in Fabric

<details>
<summary>Show answer</summary>

**Answer: C.** A Warehouse gives full T-SQL DML, multi-table transactions and cross-database queries for a star schema. A lakehouse SQL analytics endpoint is read-only for tables.

</details>

---

# PART 2 (Q16–Q30)

**Q16.** A warehouse load must upsert nightly from a staging table into a dimension, generate surrogate keys automatically, empty the staging table afterwards, and deduplicate rows in a session-scoped temp table. Which set uses only supported features?
- A. AFTER INSERT trigger on staging, IDENTITY surrogate key, TRUNCATE TABLE on staging
- B. MERGE into the dimension, IDENTITY surrogate key, TRUNCATE TABLE on staging, a #temp table for deduplication
- C. MERGE into the dimension, a synonym as alias for staging, IDENTITY surrogate key
- D. MERGE into the dimension, a recursive CTE to deduplicate, SET TRANSACTION ISOLATION LEVEL SERIALIZABLE

<details>
<summary>Show answer</summary>

**Answer: B.** MERGE, IDENTITY, TRUNCATE TABLE and #temp tables are supported in a Fabric Warehouse. Triggers, synonyms and recursive CTEs aren't, and isolation level changes are ignored.

</details>

**Q17.** In a Fabric Warehouse, which statement succeeds?
- A. `ALTER TABLE dbo.DimProduct ADD Color varchar(20) NULL;`
- B. `ALTER TABLE dbo.DimProduct ADD Color varchar(20) NOT NULL DEFAULT 'n/a';`
- C. `ALTER TABLE dbo.DimProduct ADD CONSTRAINT PK_DimProduct PRIMARY KEY (ProductKey);`
- D. `ALTER TABLE dbo.DimProduct ADD CONSTRAINT UQ_Sku UNIQUE (Sku);`

<details>
<summary>Show answer</summary>

**Answer: A.** ALTER TABLE ADD supports only nullable columns, and PRIMARY KEY and UNIQUE constraints must be declared NONCLUSTERED and NOT ENFORCED.

</details>

**Q18.** Analysts connect to a lakehouse SQL analytics endpoint. They want a reporting view over a Delta table and also need to correct 300 wrong rows in that table. What is the right plan?
- A. Create the view and run the UPDATE in the SQL analytics endpoint.
- B. Create a new table in the endpoint with CREATE TABLE AS SELECT and update that.
- C. Run MERGE in the endpoint for the corrections and create the view there.
- D. Create the view in the SQL analytics endpoint; correct the rows with a Spark notebook against the Delta table (table DML is not supported in the endpoint).

<details>
<summary>Show answer</summary>

**Answer: D.** The SQL analytics endpoint can hold views, but its tables are read-only, so corrections go through Spark against the Delta table.

</details>

**Q19.** A dataflow Gen2 refreshes incrementally into a Fabric Warehouse. If the source adds a column, the publish must fail rather than change the destination table. Which destination settings do you choose?
- A. Append, dynamic schema, incremental refresh
- B. Replace, fixed schema, incremental refresh
- C. Replace, dynamic schema
- D. Append, fixed schema

<details>
<summary>Show answer</summary>

**Answer: B.** Incremental refresh needs the Replace update method and a fixed schema, and a fixed schema makes the publish fail on a schema change.

Microsoft Learn: [Incremental refresh](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh)

</details>

**Q20.** A dataflow Gen2 uses incremental refresh into a lakehouse. Limits: 50 buckets per query and 150 buckets per dataflow. Which design stays within the limits?
- A. 4 queries × 40 buckets
- B. 2 queries × 60 buckets
- C. 3 queries × 45 buckets
- D. 5 queries × 35 buckets

<details>
<summary>Show answer</summary>

**Answer: C.** Both limits must hold: 3 × 45 = 135 buckets stays under 150 per dataflow and 45 under 50 per query. 4 × 40 = 160 and 5 × 35 = 175 break the dataflow limit; 60 per query breaks the query limit.

Microsoft Learn: [Incremental refresh](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh)

</details>

**Q21.** A streaming job writes to a Delta table with the default trigger and produces many small files. Business needs about 1 minute of freshness, continuously. What do you change?
- A. Delete the checkpoint nightly so Spark starts fresh.
- B. Add more partition columns so each micro-batch writes to more directories.
- C. Keep the default trigger and rely on V-Order.
- D. Use a processingTime trigger of 1 minute and enable Optimize Write (Auto Compaction optionally).

<details>
<summary>Show answer</summary>

**Answer: D.** A processingTime trigger of 1 minute writes larger micro-batches at the needed freshness, and Optimize Write reduces small files.

</details>

**Q22.** A nightly job must process only data that arrived since the previous run, then stop, and must resume exactly where the last run ended. Which setup is correct?
- A. Available-now trigger, checkpoint on durable OneLake storage, run as a scheduled Spark job definition or notebook.
- B. Default trigger; stop the session manually after a set time.
- C. Available-now trigger with the checkpoint on the driver's local disk.
- D. Available-now trigger, with a checkpoint directory shared with two other streaming queries.

<details>
<summary>Show answer</summary>

**Answer: A.** An available-now trigger processes what has arrived and stops; a durable checkpoint in OneLake, owned by this one query, lets the next run resume exactly where the last ended.

</details>

**Q23.** A foreachBatch function merges each micro-batch into a Delta table. After an executor failure, Spark reran a batch and duplicate business rows appeared. What is the fix?
- A. Wrap the write in try/except, log the error, and return success.
- B. Make the write idempotent, for example MERGE on a stable event key or use the batch ID.
- C. Delete the checkpoint after each failure so batches do not replay.
- D. Set unlimited retries; the retry policy removes duplicates.

<details>
<summary>Show answer</summary>

**Answer: B.** A batch can be replayed after a failure, so the write must be idempotent, for example a MERGE on a stable event key or a check on the batch ID.

</details>

**Q24.** A stream reads a silver Delta table that a nightly MERGE updates. After the first MERGE the streaming query fails. Downstream logic must see row-level changes. What do you do?
- A. Lower the trigger interval.
- B. Enable Optimize Write on the silver table.
- C. Read the table with change data feed, because a standard Delta stream expects append-only commits.
- D. Turn on spark.sql.streaming.schemaInference.

<details>
<summary>Show answer</summary>

**Answer: C.** A standard Delta stream expects append-only commits and fails after a MERGE. Change data feed delivers the row-level changes.

</details>

**Q25.** A production stream reads JSON files. Producers occasionally change a field's data type and break the query. What is the recommended handling?
- A. Define an explicit schema for the file source, route records with wrong types to a quarantine table, and treat incompatible changes as planned changes to the query.
- B. Enable schema inference for the production stream.
- C. Catch the exception and return success so the job stays green.
- D. Delete the checkpoint and restart the query.

<details>
<summary>Show answer</summary>

**Answer: A.** An explicit schema keeps the stream stable, bad records go to a quarantine table, and incompatible changes are handled as planned changes to the query.

</details>

**Q26.** Facts for a new customer arrive before the customer's dimension row. Facts must not be dropped or rejected, and attributes will arrive later and must not create a new version. What do you do?
- A. Reject the fact row into an error table until the dimension row arrives.
- B. Map the fact permanently to the Unknown member.
- C. Create a new SCD2 version of the customer when the attributes arrive.
- D. Insert an inferred member (IsInferredMember = TRUE, attributes Unknown), use its surrogate key, then update that row in place and clear the flag when the real row arrives. Do not treat it as an SCD change.

<details>
<summary>Show answer</summary>

**Answer: D.** An inferred member keeps the fact row with a valid surrogate key; when the real attributes arrive, update that row in place and clear the flag, with no new SCD version.

</details>

**Q27.** Raw events land in an Eventhouse table RawEvents and are transformed into Events by an update policy. Requirement: if the transformation fails, neither table may keep the batch, and ingestion must fail so it can be retried. Which configuration meets this?
- A. Policy on RawEvents with source Events, IsTransactional false.
- B. Policy on RawEvents, IsTransactional true.
- C. Policy on Events with source RawEvents, IsTransactional true.
- D. Policy on Events with source RawEvents, IsTransactional false and soft-delete period 0s on RawEvents.

<details>
<summary>Show answer</summary>

**Answer: C.** The update policy lives on the target table (Events) with RawEvents as its source; IsTransactional true makes a failed transformation fail the whole ingestion, so neither table keeps the batch.

</details>

**Q28.** An Eventhouse has a materialized view DailyDeviceAgg. A real-time alert query must include records not yet materialized and must be correct above all. An executive dashboard needs speed and tolerates some staleness. What should each query use?
- A. Alert: materialized_view("DailyDeviceAgg"); dashboard: query by name.
- B. Alert: query the view by name (materialized part plus delta); dashboard: the materialized_view() function (materialized part only, can be stale, bounded by max_age).
- C. Both query the view by name; the function is never faster.
- D. Both use materialized_view(); it always returns fresh data.

<details>
<summary>Show answer</summary>

**Answer: B.** Querying a materialized view by name combines the materialized part with the not-yet-materialized delta, so it's fresh. `materialized_view()` reads only the materialized part: faster but possibly stale, bounded by max_age.

</details>

**Q29.** In a pipeline, one property must receive the integer value of parameter pCount (value 3) as a number, and another property must contain the literal text @pCount. Which pair of expressions works?
- A. `@{pipeline().parameters.pCount}` and `@pCount`
- B. `@{pipeline().parameters.pCount}` and `@@pCount`
- C. `@pipeline().parameters.pCount` and `@pCount`
- D. `@pipeline().parameters.pCount` and `@@pCount`

<details>
<summary>Show answer</summary>

**Answer: D.** A plain `@` expression returns the parameter's own type (an integer), while `@{ }` interpolation always returns a string. `@@` escapes to a literal string that starts with @.

Microsoft Learn: [Expressions and functions](https://learn.microsoft.com/en-us/fabric/data-factory/expression-language)

</details>

**Q30.** A dataflow Gen2 writes to a lakehouse table with Replace. A column was added upstream. After the next refresh the semantic model built on that table lost its relationships and measures. The destination offers both schema options. Why, and what do you change?
- A. Dynamic schema drops and recreates the table when the schema differs, which can lose relationships and measures. Use a fixed schema so the publish fails on a mismatch instead.
- B. Replace always deletes semantic models. Switch to Append.
- C. The table needs OPTIMIZE after each refresh to keep metadata.
- D. Incremental refresh with dynamic schema preserves relationships, so enable it.

<details>
<summary>Show answer</summary>

**Answer: A.** With a dynamic schema, a refresh that finds a schema difference drops and recreates the table, which can remove relationships and measures. A fixed schema keeps them and fails the publish on a mismatch.

Microsoft Learn: [Data destinations and managed settings](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings)

</details>

---

# PART 3 (Q31–Q45)

**Q31.** In a Fabric Warehouse (no settings changed), which query's result is eligible for result set caching?
- A. `SELECT … WHERE OrderDate = CAST(GETDATE() AS date)` over a 5-million-row table
- B. A 5-million-row aggregation run inside BEGIN TRAN … COMMIT
- C. A pure SELECT with GROUP BY region over a 5-million-row fact table returning about 40 rows, no RLS or masking
- D. The same query as C, but the result is estimated at 80,000 rows

<details>
<summary>Show answer</summary>

**Answer: C.** Result set caching is on by default. GETDATE or CAST to date (A), an explicit transaction (B) and a result of more than 10,000 rows (D) all disqualify a query.

</details>

**Q32.** You want to benchmark the cold performance of one query without changing caching behavior for the rest of the warehouse. What do you do?
- A. `ALTER DATABASE <item> SET RESULT_SET_CACHING OFF`
- B. Wait 24 hours so the cache is evicted.
- C. Add `WHERE 1=1` to the query.
- D. Append `OPTION (USE HINT ('DISABLE_RESULT_SET_CACHE'))` to that SELECT.

<details>
<summary>Show answer</summary>

**Answer: D.** The `DISABLE_RESULT_SET_CACHE` query hint skips the cache for that one query; turning caching off for the item would affect everyone.

</details>

**Q33.** A workspace Contributor finds a runaway warehouse query started by another user. She wants to list all users' running requests and terminate the query. What is possible?
- A. A workspace Admin runs sys.dm_exec_requests (ordered by total_elapsed_time) and then KILL <session_id>.
- B. As Contributor, run sys.dm_exec_requests (shows all users) and then KILL.
- C. As Contributor, run sys.dm_exec_connections to find the session, then KILL it.
- D. Any workspace Member can run KILL on any session.

<details>
<summary>Show answer</summary>

**Answer: A.** Only a workspace Admin sees every user's requests in `sys.dm_exec_requests` and can KILL another user's session.

</details>

**Q34.** Two pipelines MERGE into the same warehouse table. One fails with error 24556, "Snapshot isolation transaction aborted due to update conflict." What is the documented fix?
- A. Pause and resume the warehouse.
- B. Retry the failed transaction (and avoid overlapping writes to the same table).
- C. Run `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` in the procedure.
- D. Wait 5–10 minutes and open a new connection.

<details>
<summary>Show answer</summary>

**Answer: B.** Error 24556 is a snapshot isolation update conflict. The documented fix is to retry the transaction and avoid concurrent writes to the same table; setting another isolation level is ignored.

Microsoft Learn: [Transactions in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions)

</details>

**Q35.** A complex warehouse query with JOIN, GROUP BY and ORDER BY fails because tempdb ran out of space. Which steps are recommended?
- A. Pause and resume the warehouse and nothing else.
- B. Add more ORDER BY columns so the plan is deterministic.
- C. Scale up the Spark pool.
- D. Verify and update statistics (especially after large DML), reduce the number of GROUP BY and ORDER BY columns, and rerun when no other queries are active.

<details>
<summary>Show answer</summary>

**Answer: D.** For a tempdb error the troubleshooting steps are: update statistics, reduce GROUP BY and ORDER BY columns, and rerun when fewer queries are active.

</details>

**Q36.** Dashboards that used a warehouse connection worked yesterday and now fail. No permissions, firewall or network settings changed. What should you do first?
- A. Retry the failed command in a loop every second.
- B. Recreate the warehouse.
- C. Check the warehouse is not paused, wait 5–10 minutes, establish a new connection, and try another application or machine.
- D. Add the users as workspace Admins.

<details>
<summary>Show answer</summary>

**Answer: C.** For a transient connection error: check the warehouse isn't paused, wait 5 to 10 minutes, open a new connection, and try another application or machine.

</details>

**Q37.** A long-running warehouse SELECT shows as succeeded on the backend but the client never receives the result. How do you isolate the problem?
- A. Scale up the capacity and rerun.
- B. Rerun in another client (SSMS, VS Code, SQL editor). If it still fails, run a CTAS with the same SELECT into another table in the same warehouse. If CTAS succeeds, the issue is likely the front end or client.
- C. Pause and resume the warehouse and rerun.
- D. Disable result set caching on the item and rerun.

<details>
<summary>Show answer</summary>

**Answer: B.** Rerun in another client; if it still fails, run the SELECT as a CTAS in the same warehouse. If the CTAS succeeds, the problem is in the client or front end.

</details>

**Q38.** Compliance requires removing unreferenced files older than 2 days from a lakehouse table. A maintenance run with a 2-day VACUUM retention fails. What is the documented way to allow it?
- A. Set `spark.databricks.delta.retentionDurationCheck.enabled` to false in the Fabric environment's Spark properties, then run maintenance with the 2-day retention.
- B. Select "Apply V-order" in the maintenance dialog.
- C. Run OPTIMIZE first; it removes old files.
- D. Set the retention to 0 days in the dialog.

<details>
<summary>Show answer</summary>

**Answer: A.** Retention shorter than 7 days is blocked until `spark.databricks.delta.retentionDurationCheck.enabled` is set to false in the environment's Spark properties.

</details>

**Q39.** Which statement about OPTIMIZE with V-Order in lakehouse table maintenance is accurate?
- A. V-Order adds about 50% to write times and gives about 15% more compression.
- B. V-Order is applied automatically by VACUUM.
- C. When selected with OPTIMIZE, V-Order applies optimized sorting, encoding and compression, with about a 15% average write-time impact and up to 50% more compression.
- D. V-Order replaces the need to compact small files.

<details>
<summary>Show answer</summary>

**Answer: C.** V-Order applies optimized sorting, encoding and compression, with about 15% average write-time cost and up to 50% more compression. VACUUM doesn't apply it.

</details>

**Q40.** A capacity has accumulated about 90 minutes of overage. What happens to new work?
- A. All interactive and background requests are rejected until burndown.
- B. Interactive requests are delayed 20 seconds at submission; background requests run normally.
- C. Nothing is affected until overage passes 24 hours.
- D. New interactive requests are rejected, background requests are still accepted, and running jobs complete.

<details>
<summary>Show answer</summary>

**Answer: D.** Between 60 minutes and 24 hours of overage, new interactive requests are rejected while background requests are still accepted. Running jobs complete.

</details>

**Q41.** Notebooks fail with HTTP 430 "Too many requests for capacity". What is the right response?
- A. Retry with exponential backoff (1, 2, 4, 8 seconds), honoring Retry-After.
- B. Check Spark concurrency in the monitoring tools and Capacity Metrics app, stagger the jobs, and consider Autoscale Billing for Spark or scaling up the capacity.
- C. Add jitter to the API client's retries.
- D. Cache and batch the API calls.

<details>
<summary>Show answer</summary>

**Answer: B.** HTTP 430 means the Spark concurrency limit of the capacity was reached. Check concurrency, stagger jobs, and consider Autoscale Billing for Spark or a larger capacity. Backoff and jitter answer HTTP 429.

</details>

**Q42.** The monitoring hub Structured Streaming tab shows input rate 4,000 rows/s, process rate 2,500 rows/s and batch duration rising steadily. What does this indicate?
- A. The query is accumulating backlog and needs more compute or less work per batch.
- B. Normal replay after a restart.
- C. The source has paused.
- D. The checkpoint is corrupted; delete it.

<details>
<summary>Show answer</summary>

**Answer: A.** Input faster than processing, with rising batch duration, means the query is building a backlog: add compute or reduce the work per batch.

</details>

**Q43.** A Spark job definition wraps its streaming query in try/except. When the query dies with a terminal exception the job shows Succeeded and the retry policy never fires. What fix is recommended?
- A. Set the retry interval to 0.
- B. Move the code to a notebook.
- C. Remove the swallowing and call query.awaitTermination() so the terminal exception reaches the job; keep a retry policy (unlimited for always-on) with an interval.
- D. Delete the checkpoint before each start.

<details>
<summary>Show answer</summary>

**Answer: C.** Swallowing the exception makes the job look successful. Let it surface through `query.awaitTermination()` so the retry policy can fire.

</details>

**Q44.** The native execution engine is on. A job reading 2 TB of JSON finishes without error but takes the same time as before. Why, and what do you do?
- A. The engine failed silently; disable and re-enable it on the capacity.
- B. JSON is not accelerated natively, so Spark falls back to the regular JVM engine without error. Land the data as Parquet or Delta for native acceleration and confirm in the plan or Advisor.
- C. Turn ANSI mode off for the job.
- D. Switch to structured streaming, which the engine accelerates.

<details>
<summary>Show answer</summary>

**Answer: B.** The native execution engine doesn't accelerate JSON, so it falls back to the JVM engine without an error. Parquet or Delta input gets native acceleration.

</details>

**Q45.** A warehouse query failed and you must open a Microsoft support case. Which information do you collect?
- A. A screenshot of the SSMS window only.
- B. The capacity ID and Azure region only.
- C. The session ID and query text only.
- D. The workspace ID, the Statement ID and Distributed request ID returned in the messages, the exact error text, and the time the query completed or failed.

<details>
<summary>Show answer</summary>

**Answer: D.** A support case needs the workspace ID, the Statement ID and Distributed request ID from the messages, the exact error and the time.

</details>

## Answer key

<details>
<summary>Show answer</summary>

1. C
2. A
3. D
4. B
5. A
6. D
7. B
8. C
9. A
10. D
11. B
12. C
13. A
14. D
15. C
16. B
17. A
18. D
19. B
20. C
21. D
22. A
23. B
24. C
25. A
26. D
27. C
28. B
29. D
30. A
31. C
32. D
33. A
34. B
35. D
36. C
37. B
38. A
39. C
40. D
41. B
42. A
43. C
44. B
45. D

</details>
