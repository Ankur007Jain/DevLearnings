# DP-700 Question Bank

By **Ankur Jain**, built with Claude (Anthropic) as study coach, November 2026.

66 practice questions written while preparing for DP-700 (Microsoft Fabric Data Engineer Associate). All scenarios are fictional and none come from the real exam. Every fact was checked against Microsoft Learn on the day the question was written; deeper explanations and source links are in the [Reading Pack](reading-pack.md). Answers are hidden: click **Show answer** under each question. The three full 45-question mocks are in the [mocks](mocks/) folder.

Each question header names the exam domain and skill: Domain 1 = Implement and manage an analytics solution, Domain 2 = Ingest and transform data, Domain 3 = Monitor and optimize an analytics solution.

# Section 1: practice questions 1 to 6 (mixed domains)

**Question 1 · Domain 3 · Identify and resolve errors in pipelines**

A pipeline copies an 800 GB fact table from Azure SQL Database into a Fabric Warehouse table with one Copy activity. **Enable staging** is on, using **Workspace** staging. Timeout and other settings are at their defaults. The pipeline's last modified user is a workspace Contributor.

Smaller tables in the same pipeline copy fine. On each of the last three nights, this table's copy failed. The team also re-ran it manually twice each night, and every attempt failed about 35 minutes after the copy started with the same error:

```
ErrorCode=DWCopyCommandOperationFailed ... 'DataWarehouse' Copy Command operation
failed with error 'A transport-level error has occurred when receiving results from
the server. (provider: TCP Provider, error: 0 - A connection attempt failed because
the connected party did not properly respond after a period of time, or established
connection failed because connected host has failed to respond.)'
```

Requirements:
1. The fix must address the cause the error points to.
2. No new Azure resources may be created.
3. The load must finish reliably inside a 4-hour nightly window.

Which action should you take?

**A.** Grant the pipeline's last modified user the Admin role in the workspace so the Copy Command has enough permission.

**B.** Change staging from Workspace to an external Azure Blob Storage or ADLS Gen2 staging connection.

**C.** Replace the single long-running copy with several smaller partitioned copies, and review the server logs and network stability.

**D.** Set the activity Timeout to `7.00:00:00` and Retry to 6 with an Increasing Delay interval.

<details><summary>Show answer</summary>

**Answer: C.** The transport-level error means the server dropped a long-running connection; the documented fix is to check server logs and network stability and split the copy into partitions. A isn't a permission error, B is for the 60-minute workspace staging limit, D retries the same failure.

</details>

**Question 2 · Domain 3 · Identify and resolve errors in an eventstream**

An eventstream reads from Azure Event Hubs and has two destinations: a Lakehouse and an Eventhouse. The Eventhouse destination uses **Event processing before ingestion** mode.

Yesterday someone changed the destination table's `amount` column to a numeric type. Since then, the Eventhouse table gets about 8% fewer rows per hour than the lakehouse table. The lakehouse table matches the Event Hubs count row for row. All events are valid JSON, and some now carry `amount` values such as `"N/A"`. You have the **Viewer** role in the workspace.

Requirements:
1. Confirm whether the missing events fail on the input side or the output side, and review the engine's error-level logs for the failing node.
2. Use only what a Viewer can do.
3. Make no changes to the eventstream or to workspace settings.

Which approach should you take?

**A.** Select the eventstream node itself, open **Data insights**, and compare IncomingMessages with OutgoingMessages.

**B.** Select the Eventhouse destination node, open **Data insights** and check **Data conversion errors**, then open **Runtime logs** and filter to errors.

**C.** Enable workspace monitoring, turn on **Log Eventstream activity** for this eventstream, and query `EventStreamErrorMetrics` with KQL.

**D.** Select the Eventhouse destination node, open **Data insights** and check **Deserialization errors**, then open **Runtime logs** and filter to errors.

<details><summary>Show answer</summary>

**Answer: B.** Data conversion errors count output events that can't be converted to the expected schema, and Runtime logs give error-level detail; both are available to a Viewer. A shows only message counts, C needs the Admin role and setting changes, D is the input-side metric.

</details>

**Question 3 · Domain 1 · Sensitivity labels (security and governance)**

Your tenant has sensitivity labels enabled with downstream inheritance left at its default. Mandatory labeling is on and default labeling is off. A lakehouse, `Sales_LH`, is labeled **Confidential**.

For each statement, answer **Yes** if it is correct or **No** if it is not. Reply as five letters, for example `YNYNN`.

1. A notebook created from `Sales_LH` inherits the **Confidential** label when it is created.
2. A Power BI report is exported to a `.csv` file. The file keeps the report's sensitivity label and its protection.
3. An item autogenerated from `Sales_LH` takes `Sales_LH`'s label and does not inherit labels from items further upstream.
4. Downstream inheritance carries a label from a Power BI semantic model to a Fabric item that depends on it.
5. Fabric enforces mandatory labeling for lakehouses: a user cannot save a new lakehouse without choosing a label.

<details><summary>Show answer</summary>

**Answer: YNYNN.** 1 Yes: a notebook created from a lakehouse inherits its label. 2 No: export to .csv or .txt isn't supported. 3 Yes: autogenerated items take the parent's label only. 4 No: Power BI to Fabric isn't a supported direction. 5 No: mandatory labeling isn't enforced for lakehouses.

</details>

**Question 4 · Domain 3 · Identify and resolve errors in notebooks and Spark (select two)**

Six notebooks run in parallel from a nightly pipeline at 02:00 on a shared Fabric capacity. Interactive users share the same capacity. Two problems are open.

**Problem 1.** Some nightly notebook activities fail with `HTTP 430 Too many requests for capacity`. In Workspace settings → Data Engineering/Science → Spark settings → Jobs, you see only the six nightly sessions, all legitimate and running or queued. None are stalled.

**Problem 2.** A new analyst has been shared the lakehouse with the **Read** item permission only. Their Spark notebook fails with `User is not authorized. User requires at least 'ReadAll' permission on the artifact`.

Requirements:
1. Fix problem 1 without changing the SKU, and so the nightly Spark workload stops consuming the capacity's CUs that interactive users rely on. Pay-as-you-go spend for Spark is approved up to a cap. The notebooks must not change.
2. Give the analyst only what they need to run Spark notebooks against the lakehouse. They don't need SQL access.

Which **two** actions resolve both problems?

**A.** Restart the capacity and wait about 10 minutes before the nightly run.

**B.** Move the capacity to the next larger SKU.

**C.** Grant the analyst the **ReadData** item permission on the lakehouse.

**D.** Grant the analyst the **ReadAll** item permission on the lakehouse.

**E.** Add exponential backoff with jitter and `Retry-After` handling to each notebook.

**F.** Turn on Autoscale Billing for Fabric Spark and set a maximum capacity unit limit.

<details><summary>Show answer</summary>

**Answer: D and F.** The error names ReadAll, the Spark permission (ReadData is SQL). HTTP 430 is a capacity limit, fixed without a SKU change by Autoscale Billing for Fabric Spark. E is the fix for HTTP 429; A is for orphaned sessions.

</details>

**Question 5 · Domain 2 · Spark Structured Streaming in production**

An orders stream from Azure Event Hubs is written to a Delta table in a lakehouse by a Structured Streaming query that runs in a notebook. It is now a production workload. Over the weekend the run stopped after an error, and nobody restarted it until Monday. The table also holds thousands of tiny Parquet files, because the query uses the default trigger.

Requirements:
1. The stream must restart automatically after failures, with no operator action even after many consecutive failures.
2. Delta files must get larger, without hand-written `repartition()` or `coalesce()` calls.
3. On-call must be able to see the stream's input rate and process rate in the Fabric UI.

Which approach meets all three?

**A.** Move the query into a Spark job definition with a retry policy of unlimited retries and a retry interval. Add `.trigger(processingTime="1 minute")` and enable Optimized Write with `spark.databricks.delta.optimizeWrite.enabled`. Watch the Monitoring hub's Structured Streaming tab.

**B.** Keep the query in the notebook and schedule the notebook from a pipeline with retries. Add the same trigger and enable Optimized Write. Watch the Monitoring hub's Structured Streaming tab.

**C.** Move the query into a Spark job definition with the retry policy capped at 3 retries. Add the same trigger and enable Optimized Write. Watch the Monitoring hub's Structured Streaming tab.

**D.** Move the query into a Spark job definition with unlimited retries and the same trigger. Call `repartition(48)` before each write instead of enabling Optimized Write. Watch the Monitoring hub's Structured Streaming tab.

<details><summary>Show answer</summary>

**Answer: A.** Production streams belong in a Spark job definition with a retry policy of unlimited retries; a processingTime trigger makes larger batches; Optimized Write removes manual repartition. B keeps a notebook, C caps retries, D hand-writes repartition.

</details>

**Question 6 · Domain 2 (streaming) · single answer · budget about 2 minutes**

*Fictional scenario.* An eventstream named `ColdRooms` ingests JSON from Azure Event Hubs. Each event has `roomId`, `temperatureF`, and `readingTime`, an ISO 8601 string stamped by the device's own clock. Requirements:

1. Once a minute, for each room, compute the average temperature over the **last 5 minutes**. A reading must count toward every 5-minute result it falls into.
2. Windows must use the device's `readingTime`, not the time the event reached Event Hubs.
3. Write only rooms whose 5-minute average is above 75 °F to a lakehouse.

The topology already contains a Lakehouse destination node named `LakehouseAlerts`, left over from an earlier prototype. You will do all the transformation in a single SQL operator with this skeleton. Only the marked parts differ between options:

```sql
SELECT System.Timestamp() AS WindowEnd, roomId, AVG(temperatureF) AS AvgTemp
INTO <output>
FROM input [TIMESTAMP BY readingTime]
GROUP BY roomId, <window>
HAVING AVG(temperatureF) > 75
```

Which option meets all three requirements and works within the SQL operator's documented limits?

**A.** `FROM input TIMESTAMP BY readingTime`, `GROUP BY roomId, TumblingWindow(minute, 5)`. Send the output to a new Lakehouse destination node.

**B.** `FROM input TIMESTAMP BY readingTime`, `GROUP BY roomId, SlidingWindow(minute, 5)`. Send the output to a new Lakehouse destination node.

**C.** `FROM input` with no TIMESTAMP BY, `GROUP BY roomId, HoppingWindow(minute, 5, 1)`. Send the output to a new Lakehouse destination node.

**D.** `FROM input TIMESTAMP BY readingTime`, `GROUP BY roomId, HoppingWindow(minute, 5, 1)`. Send the output to the existing `LakehouseAlerts` node.

**E.** `FROM input TIMESTAMP BY readingTime`, `GROUP BY roomId, HoppingWindow(minute, 5, 1)`. Send the output to a new Lakehouse destination node.

<details><summary>Show answer</summary>

**Answer: E.** HoppingWindow(minute, 5, 1) gives overlapping 5-minute windows every minute; TIMESTAMP BY switches from arrival time to the device time; a SQL operator needs new destination nodes. A doesn't overlap, B outputs only on change, C uses arrival time, D reuses an existing node.

</details>

# Section 2: case study 1, Harborview Care Analytics

**Case study 1 (fictional): Harborview Care Analytics**

**Overview**
Harborview is moving its claims reporting to Microsoft Fabric. The first release must load claims nightly, let analysts use partner eligibility data, and alert operations when loads fail.

**Existing environment**
- One paid Fabric capacity. Workspace `Claims-Prod` holds lakehouse `claims_lh`. Data engineers (`Claims-DE`) are Contributors. Analysts (`Claims-Analysts`, an Entra security group) are Viewers.
- Workspace `Partner-Data` (same tenant) is owned by the partner team. Its lakehouse `partner_lh` has a table `eligibility`, protected with OneLake security roles.
- Source: Azure SQL Database table `dbo.Claims`, about 600 million rows. Primary key `ClaimId`. A `LastModifiedAt` datetime column is updated on every insert and update. Claims are never hard-deleted; voided claims get `Status = 'Void'`. CDC is not enabled, and the DBA team won't enable it.
- The SQL analytics endpoint of `claims_lh` is in its default identity mode.

**Business requirements**
1. After the first load, each nightly run moves only new or changed claims.
2. `claims_lh` keeps exactly one current row per claim.
3. Eligibility data is not copied. The partner team stays its owner.
4. Analysts query eligibility together with claims through T-SQL, and what they see must follow their own access in `partner_lh`.
5. Operations learn about failed loads by email, at no extra cost.

**Technical requirements**
- The nightly load runs on a schedule, resumes after a failure, and uses no pipeline.
- No new workspace roles for analysts in `Partner-Data`.
- Operations is an Entra group. An external compliance consultant with no account in the tenant also needs the failure emails.
- Operators sometimes run the load by hand during the day.

**Known issues**
- Last week an engineer's attempt to create the `eligibility` shortcut in `claims_lh` failed with an authorization error.
- Compliance noted that T-SQL reads of that shortcut run under the owner of `claims_lh`, not under the analyst.

**Case study 1, question 1 · Domain 2**

You will build the claims load with a Fabric Copy job from `dbo.Claims` into a lakehouse table in `claims_lh`. Which configuration meets business requirements 1 and 2 and the technical requirements?

**A.** Full copy, overwriting the destination table each night.

**B.** Incremental copy with `LastModifiedAt` as the watermark column, using the default update method (append).

**C.** Incremental copy with `LastModifiedAt` as the watermark column, using the merge update method on `ClaimId`.

**D.** CDC-based incremental copy with the SCD Type 2 update method.

<details><summary>Show answer</summary>

**Answer: C.** No CDC, a reliable LastModifiedAt column, and one current row per claim: watermark incremental copy with merge on the key. Append duplicates updated claims; CDC isn't enabled.

</details>

**Case study 1, question 2 · Domain 1**

The engineer who failed to create the `eligibility` shortcut is a Contributor in `Claims-Prod` and has no role in `Partner-Data`. The partner team will grant the **minimum** access that lets the engineer create the shortcut in `claims_lh` that points to the `eligibility` table in `partner_lh`. What should they grant?

**A.** Write permission on the `partner_lh` item.

**B.** Read access to the `eligibility` table in `partner_lh` through OneLake security.

**C.** Make the engineer an Admin of `Claims-Prod`.

**D.** Make the engineer a Contributor in `Partner-Data`.

<details><summary>Show answer</summary>

**Answer: B.** Creating a shortcut needs Write where it is created plus Read on the target. A higher role in the source workspace doesn't supply target Read.

</details>

**Case study 1, question 3 · Domain 1**

Compliance's finding stands: T-SQL reads of the `eligibility` shortcut currently run under the owner of `claims_lh`, not under the analyst. The shortcut is a same-tenant OneLake shortcut created with default settings. Analysts query it through the `claims_lh` SQL analytics endpoint.

Requirement 4 says what analysts see must follow their **own** access in `partner_lh`. You also may not copy the data or give analysts new roles in `Partner-Data`. Which change meets all of that?

**A.** Recreate the shortcut with **Delegated identity**.

**B.** Grant the `Claims-Analysts` group the Contributor role in `Partner-Data`.

**C.** Define a T-SQL row-level security policy on the SQL analytics endpoint of `claims_lh`.

**D.** Switch the SQL analytics endpoint of `claims_lh` to **User's identity** mode.

<details><summary>Show answer</summary>

**Answer: D.** T-SQL in Delegated identity mode reads the shortcut as the item owner. User's identity mode uses the caller's own access.

</details>

**Case study 1, question 4 · Domain 3**

Requirement 5 says operations must learn about failed loads by email at no extra cost. The technical requirements say the load uses no pipeline, and recipients must include the Operations Entra group and the external compliance consultant, who has no account in the tenant. The nightly load is a scheduled Copy job.

Which setup meets all of that?

**A.** In the Monitor hub, configure **Schedule failure emails (free)** for the Copy job. Add the Operations group, add the consultant to the tenant as a B2B guest user, and select that guest as a recipient.

**B.** In the Monitor hub, configure **Schedule failure emails (free)** for the Copy job. Add the Operations group and type the consultant's external email address as a recipient.

**C.** Create an Activator-based alert rule for the Copy job and add the Operations group and the consultant as recipients.

**D.** Put the Copy job in a pipeline and add an Outlook activity after the Copy job activity.

<details><summary>Show answer</summary>

**Answer: A.** Schedule failure emails are free and need no pipeline. Recipients must be Entra users, groups or B2B guests; direct external addresses aren't supported. Activator rules are paid.

</details>

**Case study 1, question 5 · Domains 2 and 3 (select two)**

The failure emails from question 4 are now set up on the nightly Copy job. At 10:00 an operator runs the Copy job by hand and it fails. At 01:00 the next night, the scheduled run starts.

Which **two** statements are true?

**A.** Someone with only Viewer-level access to the workspace can reconfigure the failure notifications.

**B.** The 01:00 scheduled run resumes from the end of the last successful run.

**C.** The failed 10:00 run's partial progress advances the watermark.

**D.** The failure emails apply only to scheduled runs, so the failed manual run sends none.

<details><summary>Show answer</summary>

**Answer: B and D.** A failed run doesn't change the Copy job's state, so the next run resumes from the last successful run. Failure emails apply only to scheduled runs. Configuring them needs Contributor or Write.

</details>

# Section 3: questions 7 to 11 (Ingest and transform)

**Question 7 · Mirroring**

A retailer has an Azure SQL Database (orders) and a Snowflake account (marketing data). Requirements:
1. Order data must be replicated into OneLake in near real time.
2. Marketing data must stay in Snowflake, with no copy made in OneLake.
3. No custom application code.

Which design meets all three?

- **A.** Database mirroring for Azure SQL Database, and database mirroring for Snowflake
- **B.** Database mirroring for Azure SQL Database, and metadata mirroring for Snowflake
- **C.** Open mirroring for Azure SQL Database, and metadata mirroring for Snowflake
- **D.** Metadata mirroring for both sources

<details><summary>Show answer</summary>

**Answer: B.** Database mirroring copies Azure SQL data into OneLake; metadata mirroring leaves Snowflake data in place and uses shortcuts. A copies Snowflake data, C (open mirroring) needs custom code, D: Azure SQL isn't a metadata mirroring source.

</details>

**Question 8 · Dataflow Gen2 incremental refresh**

A Dataflow Gen2 loads `Orders` from Azure SQL Database into a Lakehouse table. Today the destination uses the append update method with a dynamic schema, and a nightly notebook runs `OPTIMIZE` on that table. You must turn on incremental refresh covering the past 3 years. Which configuration works?

- **A.** Append, fixed schema, monthly buckets, keep the nightly `OPTIMIZE`
- **B.** Replace, dynamic schema, monthly buckets, remove the nightly `OPTIMIZE`
- **C.** Replace, fixed schema, monthly buckets, keep `OPTIMIZE` but run it after the refresh
- **D.** Replace, fixed schema, monthly buckets, remove the nightly `OPTIMIZE`
- **E.** Replace, fixed schema, daily buckets, remove the nightly `OPTIMIZE`

<details><summary>Show answer</summary>

**Answer: D.** Incremental refresh supports only the replace update method, needs a fixed schema, doesn't support OPTIMIZE on that table, and allows 50 buckets per query. A appends, B is dynamic, C keeps OPTIMIZE, E has about 1,095 buckets.

</details>

**Question 9 · Loading a dimensional model**

A Fabric Warehouse has `DimCustomer` (SCD type 2, `IDENTITY` surrogate key) and a large `FactSales`. Some sales arrive before their customer exists in the dimension, and the source system sometimes deletes customers. Which practice follows Microsoft's guidance?

- **A.** When real details arrive for a customer that the fact load inserted as an inferred member, update the attributes in place and set the inferred-member flag to FALSE
- **B.** Truncate and fully reload `DimCustomer` each night so it always matches the source
- **C.** Hold back sales rows whose customer lookup fails, and load them once the customer arrives
- **D.** When the source deletes a customer, delete that customer's rows from `DimCustomer`

<details><summary>Show answer</summary>

**Answer: A.** An inferred member's real details are late-arriving details, not an SCD change: update in place and clear the flag. B invalidates surrogate keys, C: the fact row must still be inserted, D: use a soft delete.

</details>

**Question 10 · KQL materialized views**

An Eventhouse has a materialized view `LatestState`, defined as `DeviceState | summarize arg_max(Timestamp, *) by DeviceId`. Two consumers use it:
- An operations dashboard that must include records ingested seconds ago.
- A nightly report that tolerates some staleness and must run as cheaply as possible.

How should each one query?

- **A.** Both query `LatestState` by name
- **B.** Both use `materialized_view("LatestState")`
- **C.** The dashboard queries `LatestState` by name; the report uses `materialized_view("LatestState")`
- **D.** The dashboard uses `materialized_view("LatestState")`; the report queries `LatestState` by name

<details><summary>Show answer</summary>

**Answer: C.** Querying by name combines the materialized part with the not-yet-processed delta, so it is always fresh. materialized_view() reads only the materialized part: faster, possibly stale.

</details>

**Question 11 · Eventstream to Eventhouse**

An eventstream reads from Azure Event Hubs and needs two Eventhouse destinations:
1. `RawEvents`: every event, exactly as received.
2. `MinuteStats`: events filtered and aggregated with eventstream operators before they are ingested.
3. For `MinuteStats`, events that arrive between publishing and routing being initialized must not be missed.

Which setup meets all three?

- **A.** `RawEvents`: direct ingestion on the default stream. `MinuteStats`: direct ingestion attached straight after the Group by operator
- **B.** `RawEvents`: direct ingestion on the default stream. `MinuteStats`: event processing before ingestion, with **Activate ingestion** unchecked, then activated after publishing from a **Custom time** earlier than the publish
- **C.** `RawEvents`: direct ingestion on the default stream. `MinuteStats`: event processing before ingestion, with **Activate ingestion** checked
- **D.** `RawEvents`: direct ingestion on the default stream. `MinuteStats`: direct ingestion on the default stream, with filtering and aggregation done afterward in the Eventhouse

<details><summary>Show answer</summary>

**Answer: B.** Direct ingestion does no processing, so operators need event processing before ingestion. Unchecking Activate ingestion and resuming from an earlier Custom time covers events that arrive before routing is ready.

</details>

# Section 4: questions 12 to 21 (Ingest and transform)

**Question 12 · Choosing a tool**

An analyst who is an experienced Power Query user must pull low-to-medium volumes from several SaaS sources, apply many complex transformations, and write to a lakehouse. She must write no code. Which tool fits?

- **A.** Pipeline Copy activity
- **B.** Copy job
- **C.** Dataflow Gen2
- **D.** Spark notebook
- **E.** Eventstream

<details><summary>Show answer</summary>

**Answer: C.** Dataflow Gen2 is the no-code tool for a Power Query user with many connectors and complex transformations. Copy activity and Copy job do only light transformation; Spark needs code; Eventstream is for events.

</details>

**Question 13 · Loading a Warehouse**

A stored procedure in a Fabric Warehouse must load large Parquet files from ADLS Gen2 into a warehouse table. Requirements: the load is part of the T-SQL logic, throughput is as high as possible, and the data is stored in the table. Which approach?

- **A.** `COPY INTO` the table from the Parquet files
- **B.** A loop of single-row `INSERT` statements
- **C.** A view over `OPENROWSET` on the files, queried each time
- **D.** A Dataflow Gen2 with the Warehouse as its destination

<details><summary>Show answer</summary>

**Answer: A.** COPY INTO gives the highest ingestion throughput and runs inside T-SQL logic. Single-row INSERTs perform poorly, OPENROWSET doesn't store the data, Dataflow Gen2 isn't T-SQL.

</details>

**Question 14 · T-SQL across items**

Warehouse `SalesDW` and lakehouse `SilverLH` are in workspace W1. Lakehouse `FinanceLH` is in workspace W2. You want to create warehouse tables from `SilverLH.dbo.Orders` and `FinanceLH.dbo.Budget` using `CREATE TABLE AS SELECT` with three-part names. Which statement is true?

- **A.** Both tables can be loaded this way
- **B.** Neither can; reading a lakehouse from a warehouse needs a pipeline
- **C.** Only `Budget` can be loaded this way
- **D.** Only `Orders` can be loaded this way, because T-SQL table sources must be in the same workspace

<details><summary>Show answer</summary>

**Answer: D.** A warehouse can read another item with a three-part name only when it is in the same workspace. Orders (W1) qualifies; Budget (W2) doesn't.

</details>

**Question 15 · KQL ingestion-time transform**

An Eventhouse table `RawJson` receives raw events. Requirements:
1. Each row is parsed into a typed table `Events` as it is ingested.
2. The raw rows must not be kept or queryable.
3. A transient failure of the transform must not lose data.

Which design?

- **A.** An update policy on `Events` with `IsTransactional` false, and a `0s` soft-delete retention on `RawJson`
- **B.** An update policy on `Events` with `IsTransactional` true, and a `0s` soft-delete retention on `RawJson`
- **C.** A materialized view over `RawJson`
- **D.** An update policy on `Events` with `IsTransactional` true, and the default retention on `RawJson`

<details><summary>Show answer</summary>

**Answer: B.** An update policy transforms rows at ingestion. A 0s soft-delete on the source means raw rows aren't kept, and that requires a transactional policy, so a failure loses nothing. A isn't transactional, C is an aggregation, D keeps the raw rows. You skipped this one.

</details>

**Question 16 · Spark streaming deduplication**

A Spark structured streaming job reads device events. Retries resend the same `event_id`, sometimes with a different `event_time`. Events can be up to 10 minutes late. Requirements: remove duplicates in the stream by `event_id` alone, and keep the deduplication state bounded. Which code?

- **A.** `events.dropDuplicates(["event_id"])`
- **B.** `events.withWatermark("event_time", "10 minutes").dropDuplicates(["event_id", "event_time"])`
- **C.** `events.withWatermark("event_time", "10 minutes").dropDuplicatesWithinWatermark(["event_id"])`
- **D.** Write everything to Delta and remove duplicates in a nightly notebook

<details><summary>Show answer</summary>

**Answer: C.** dropDuplicatesWithinWatermark uses event_id alone and keeps state only for the watermark period. A has unbounded state, B treats a retry with a different event_time as new, D isn't in the stream.

</details>

**Question 17 · Spark windows**

The same job must count events per device over the last 10 minutes, with a new result every minute. Which grouping expression?

- **A.** `window("event_time", "10 minutes", "1 minute")`
- **B.** `window("event_time", "10 minutes")`
- **C.** `session_window("event_time", "10 minutes")`
- **D.** `window("event_time", "1 minute", "10 minutes")`

<details><summary>Show answer</summary>

**Answer: A.** In Spark, window(column, size, slide) is the overlapping (sliding) window: 10 minutes every 1 minute. B is tumbling, C is a session window, D has the arguments reversed.

</details>

**Question 18 · Eventstream operators**

Two sources send events with identical fields into one eventstream. Each event carries an array field `readings`. You need a single stream with one row per array element, using no-code operators. Which sequence?

- **A.** Join, then Expand
- **B.** Union, then Manage fields
- **C.** Group by, then Expand
- **D.** Union, then Expand

<details><summary>Show answer</summary>

**Answer: D.** Union combines streams that share fields; Expand creates one row per array value. Manage fields only adds, removes, renames or retypes fields; Join pairs two streams; Group by aggregates.

</details>

**Question 19 · Sharing a filtered stream**

An eventstream ingests all store events. Only events where `region = 'EU'` may be shared. Other teams must be able to find that filtered stream in the Real-Time hub, and an external application must consume it in real time over the Kafka protocol. Which setup?

- **A.** Add a custom endpoint destination to the default stream
- **B.** Add a Filter operator, output to a derived stream, and add a custom endpoint destination to that derived stream
- **C.** Add an Eventhouse destination with direct ingestion and let the application query the table
- **D.** Add a Filter operator and a Lakehouse destination, and let the application read the Delta table

<details><summary>Show answer</summary>

**Answer: B.** A Filter feeding a derived stream makes the subset discoverable in the Real-Time hub, and a custom endpoint on that derived stream serves Kafka clients. A shares unfiltered data; C and D aren't a Kafka stream.

</details>

**Question 20 · Dataflow Gen2 destinations (select two)**

Which two statements are true?

- **A.** A Warehouse destination supports only a fixed schema, needs staging enabled, and must be in the same workspace as the dataflow
- **B.** Automatic settings are supported for a Warehouse destination
- **C.** Fabric KQL database and Azure Data Explorer destinations don't support the replace update method
- **D.** With the append update method, a dynamic schema lets new source columns flow into the table
- **E.** If you manually delete an existing table that the dataflow didn't create, the next refresh recreates it

<details><summary>Show answer</summary>

**Answer: A and C.** A Warehouse destination needs a fixed schema, staging and the same workspace. KQL database and Azure Data Explorer don't support replace. Automatic settings exclude Warehouse; append can't change schema; a table the dataflow didn't create is never recreated.

</details>

**Question 21 · Choosing a data store**

A team is building an operational .NET application in Fabric. It needs high concurrency, full ACID transactions and enforced foreign keys. Analysts must query the same data without loading the application database. Which store?

- **A.** Fabric Data Warehouse
- **B.** Lakehouse
- **C.** Eventhouse
- **D.** SQL database in Fabric

<details><summary>Show answer</summary>

**Answer: D.** SQL database in Fabric is for operational apps with high concurrency, ACID transactions and enforced foreign keys, with a SQL analytics endpoint for analysts. A Warehouse doesn't enforce foreign keys.

</details>

# Section 5: questions 22 to 31 (Monitor and optimize)

**Question 22 · T-SQL error**

In a Fabric Warehouse, procedure A updates `FactSales` rows for region East while procedure B deletes rows for region West. B fails with error 24556, "Snapshot isolation transaction aborted due to update conflict". What explains it, and what is the fix?

- **A.** Row locks collided; add a `ROWLOCK` hint to both statements
- **B.** Conflicts are detected at table level even when the rows differ; run the procedures one after the other, or retry with backoff
- **C.** Snapshot isolation is too strict; set the session to `READ COMMITTED`
- **D.** The statements need one shared transaction; wrap both in `BEGIN DISTRIBUTED TRANSACTION`

<details><summary>Show answer</summary>

**Answer: B.** Warehouse write conflicts are detected at table level even when rows differ. Run the statements one after the other or retry with backoff. Isolation changes are ignored and distributed transactions aren't supported.

</details>

**Question 23 · Monitoring warehouse queries**

You need the queries that used the most CPU in a Warehouse over the past week, with the login that ran each one. Which view?

- **A.** `queryinsights.long_running_queries`
- **B.** `queryinsights.frequently_run_queries`
- **C.** `queryinsights.exec_requests_history`
- **D.** `queryinsights.exec_sessions_history`

<details><summary>Show answer</summary>

**Answer: C.** exec_requests_history has one row per completed request with allocated_cpu_time_ms and login_name. long_running_queries ranks by elapsed time; frequently_run_queries by count; exec_sessions_history covers sessions.

</details>

**Question 24 · Optimizing a lakehouse table**

A Delta table feeding Power BI reports has thousands of small files, and reads are slow. Old unreferenced files are also inflating storage. Compliance requires 7 days of time travel. Which maintenance run meets all of this?

- **A.** Compaction on with V-order applied, and VACUUM with a 7-day retention
- **B.** Compaction on with V-order applied, and VACUUM with a 1-day retention
- **C.** VACUUM only, with a 7-day retention
- **D.** Compaction on with V-order applied, and no VACUUM

<details><summary>Show answer</summary>

**Answer: A.** Compaction fixes small files, V-order speeds reads, and VACUUM at 7 days removes old files while keeping the required time travel. A 1-day VACUUM breaks time travel and fails by default.

</details>

**Question 25 · V-Order**

In a newly created workspace, one notebook session writes to both `bronze_raw` and `sales_gold`. Writes to `bronze_raw` must stay as fast as possible. New writes to `sales_gold` must be V-Ordered for dashboards. Which change does this?

- **A.** Run `SET spark.sql.parquet.vorder.default=TRUE` at the start of the session
- **B.** Nothing; V-Order is on by default in new workspaces
- **C.** Set the session default to TRUE, and add the writer option `parquet.vorder.enabled = false` on the `bronze_raw` write
- **D.** `ALTER TABLE sales_gold SET TBLPROPERTIES("delta.parquet.vorder.enabled" = "true")`

<details><summary>Show answer</summary>

**Answer: D.** The table property applies V-Order to writes on sales_gold only. A session default of TRUE V-Orders every write, even one explicitly set to false, and V-Order is off by default in new workspaces.

</details>

**Question 26 · Warehouse statistics**

A nightly load grows a Warehouse table from 1 million to 400 million rows. The first report query each morning is slow, and later runs are fast. What explains it, and what should you do?

- **A.** Fabric never creates statistics automatically; create them on every column
- **B.** Statistics are created or refreshed synchronously when a query needs them, so the first query pays for it; run `UPDATE STATISTICS` on the heavily used columns after the load
- **C.** Single-column statistics aren't enough; create multi-column statistics on the join keys
- **D.** Proactive statistics refresh is causing the delay; disable it

<details><summary>Show answer</summary>

**Answer: B.** Statistics are created or refreshed synchronously when a query needs them, so the first query pays. Run UPDATE STATISTICS after a load that changes row counts a lot. Multi-column statistics aren't supported.

</details>

**Question 27 · Eventhouse ingestion errors (select two)**

Which two statements about `EventhouseIngestionResultsLogs` are true?

- **A.** It records results for both successful and failed ingestions
- **B.** It is supported only for streaming ingestion
- **C.** `ShouldRetry` is a string that holds the time of the next retry
- **D.** `IngestionSourcePath` holds the source path or blob URI, and `IngestionErrorDetails` holds the error details
- **E.** It is a view in the Warehouse `queryinsights` schema

<details><summary>Show answer</summary>

**Answer: A and D.** The table records successful and failed ingestions, for queued ingestion. IngestionSourcePath holds the path or blob URI and IngestionErrorDetails the error. ShouldRetry is a boolean.

</details>

**Question 28 · Optimizing an Eventhouse**

A KQL table must keep 365 days of data queryable. Dashboards query only the last 30 days and must be fast. Older data is queried rarely, and the team wants to cut cost. What should you configure?

- **A.** Set the retention soft-delete period to 30 days
- **B.** Leave the caching policy at its default
- **C.** Set the caching policy so 30 days are hot, and keep retention at 365 days
- **D.** Create a materialized view over the table

<details><summary>Show answer</summary>

**Answer: C.** The caching policy sets how much data is hot; retention sets how much is queryable. 30 days hot with 365 days retention keeps dashboards fast and cuts cost. The default keeps everything hot.

</details>

**Question 29 · Semantic model refresh**

After a lakehouse load, a pipeline must refresh only the current partition of `FactSales` in a semantic model. The refresh must commit all at once, and the next activity must not start until the refresh has finished. Which setup?

- **A.** Semantic model refresh activity with the table and partition selected, Wait on completion on, and commit mode Transactional
- **B.** The same, with commit mode Partial Batch
- **C.** The same as A, with Wait on completion off
- **D.** A scheduled refresh in the semantic model's own settings, timed for when the pipeline usually ends

<details><summary>Show answer</summary>

**Answer: A.** Transactional commits the refresh all at once, and Wait on completion holds the next activity. Partial Batch commits in batches; a separate schedule isn't tied to the pipeline.

</details>

**Question 30 · Optimizing Spark**

A team enables the native execution engine at the environment level on Runtime 1.3. Which job will fall back to the regular Spark engine?

- **A.** A batch aggregation over Delta tables
- **B.** An ETL job that joins Parquet files
- **C.** A job that ingests CSV files
- **D.** A structured streaming job that reads from Azure Event Hubs

<details><summary>Show answer</summary>

**Answer: D.** The native execution engine doesn't support structured streaming, so that job falls back. Parquet, Delta and CSV are supported; JSON and XML also fall back.

</details>

**Question 31 · Alerts (retry of last week's miss)**

A scheduled notebook runs nightly. The team wants an email to a tenant security group each time a run **succeeds**. Workspace monitoring is not enabled, the engineer is a workspace Admin, and no pipeline may be added. What should the engineer do?

- **A.** Configure Schedule failure emails in the Monitor hub
- **B.** Enable workspace monitoring, then create an Activator-based alert rule on the Succeeded event
- **C.** Create an Activator-based alert rule on the Succeeded event without workspace monitoring
- **D.** Put the notebook in a pipeline and add an Outlook activity on success

<details><summary>Show answer</summary>

**Answer: B.** Free schedule failure emails fire only on failures. An alert on Succeeded needs an Activator-based rule, which needs workspace monitoring, and only a workspace Admin can enable that. D adds a pipeline.

</details>

# Section 6: questions 32 to 41 (Monitor and optimize)

**Question 32 · Capacity throttling**

Users report that interactive requests on a capacity are being rejected, while scheduled background jobs still start and run. Which throttling stage is the capacity in?

- **A.** Overage protection (10 minutes or less of future capacity used)
- **B.** Interactive delay (more than 10 and up to 60 minutes)
- **C.** Interactive rejection (more than 60 minutes and up to 24 hours)
- **D.** Background rejection (more than 24 hours)

<details><summary>Show answer</summary>

**Answer: C.** Over 60 minutes and up to 24 hours of future capacity is interactive rejection: interactive requests are rejected and background jobs still run.

</details>

**Question 33 · Recovering from throttling**

An F64 capacity is rejecting all requests. It is 2 a.m. and nothing is using it. The team must be able to accept new operations right away, will accept a billing event, and must not change the SKU. What should the admin do?

- **A.** Pause the capacity, then resume it
- **B.** Enable Autoscale on the capacity
- **C.** Scale up to F128
- **D.** Wait for the capacity to recover by itself

<details><summary>Show answer</summary>

**Answer: A.** Pausing bills the accumulated future usage; on resume the capacity has none and accepts work right away. Autoscale is for P SKUs, scaling up changes the SKU, waiting isn't immediate.

</details>

**Question 34 · Dataflow Gen2 errors**

A Dataflow Gen2 that refreshes through an on-premises gateway failed 10 days ago. An engineer with the workspace Viewer role needs the Power Query engine logs for that run. Which statement is true?

- **A.** The engineer needs at least the Contributor role to download the logs
- **B.** The logs are gone, because detailed logs are kept for 7 days
- **C.** The logs are available only if workspace monitoring was enabled before the run
- **D.** The engineer can open Recent runs, select the run and choose Download detailed logs, provided Admin consent for gateway diagnostics is enabled on the gateway

<details><summary>Show answer</summary>

**Answer: D.** Detailed logs can be downloaded from Recent runs for up to 28 days, the Viewer role is enough, and a gateway needs Admin consent for gateway diagnostics.

</details>

**Question 35 · Eventstream throughput**

An eventstream reads from an Azure Event Hubs source that has 1 partition. Ingestion tops out near 9 MB/s. The engineer sets the event throughput level to High and sees no improvement. Why?

- **A.** The retention period must be increased first
- **B.** With fewer than four partitions, throughput is limited by the partition count regardless of the level
- **C.** The throughput level applies only to destinations
- **D.** The High level needs an F64 capacity or larger

<details><summary>Show answer</summary>

**Answer: B.** With fewer than four Event Hubs partitions, throughput is limited by the partition count whatever the level. One partition gives about 9 MB/s.

</details>

**Question 36 · Changing eventstream throughput**

An eventstream has a Lakehouse destination and a custom endpoint destination, both active. How do you change the event throughput level?

- **A.** Change it directly; no node needs to be deactivated
- **B.** Delete the eventstream and recreate it at the new level
- **C.** Deactivate the nodes that support pause and resume, update the setting, then reactivate them
- **D.** Deactivate every node, including the custom endpoint, then update the setting

<details><summary>Show answer</summary>

**Answer: C.** Deactivate the nodes that support pause and resume, update the level, then reactivate. A custom endpoint doesn't support pause and resume, so it doesn't block the change.

</details>

**Question 37 · Warehouse cold start**

A Warehouse query is slow on its first run each morning. How do you confirm that a cold start caused it?

- **A.** Check `data_scanned_remote_storage_mb` in `queryinsights.exec_requests_history`; a nonzero value indicates a cold start
- **B.** Check `allocated_cpu_time_ms` in `queryinsights.exec_requests_history`
- **C.** Check the median elapsed time in `queryinsights.long_running_queries`
- **D.** Check `sys.dm_tran_locks` for blocking

<details><summary>Show answer</summary>

**Answer: A.** A nonzero data_scanned_remote_storage_mb in queryinsights.exec_requests_history indicates a cold start.

</details>

**Question 38 · V-Order in a Warehouse**

A team has a staging warehouse that only receives writes, and a reporting warehouse that is queried heavily. They are considering disabling V-Order. Which statement is correct?

- **A.** Disable it on both warehouses during the load, then re-enable it before reports run
- **B.** No action is needed, because V-Order is off by default in warehouses
- **C.** Disable it on the reporting warehouse to speed up report queries
- **D.** Disable it on the staging warehouse only, knowing it can't be re-enabled there

<details><summary>Show answer</summary>

**Answer: D.** V-Order is on by default in a warehouse and helps reads, so keep it on the reporting warehouse. Disable it only on a write-only staging warehouse; once disabled it can't be re-enabled.

</details>

**Question 39 · Spark autotune**

A team wants autotune to tune nightly Spark SQL queries. Their notebooks run on Runtime 1.3 in high concurrency mode. Which statement is true?

- **A.** Autotune won't run here: it is compatible only with Runtime 1.2 and doesn't run in high concurrency mode
- **B.** Autotune is on by default, so nothing needs to change
- **C.** Autotune will tune executor memory and cores for these queries
- **D.** Autotune will also tune their queries that finish in under 15 seconds

<details><summary>Show answer</summary>

**Answer: A.** Autotune (preview, off by default) works only on Runtime 1.2 and not in high concurrency mode. It tunes three settings (shuffle partitions, broadcast join threshold, max partition bytes) and skips queries under 15 seconds.

</details>

**Question 40 · Workspace monitoring**

A team wants 90 days of pipeline activity run logs, queryable with KQL. They enable workspace monitoring today. Which statement is true?

- **A.** The monitoring database is backfilled with the previous 30 days of activity
- **B.** Data is collected only from now on, and the default 30-day retention must be raised on the monitoring KQL database
- **C.** The team can add its own tables to the monitoring database
- **D.** Only workspace Admins can query the monitoring database

<details><summary>Show answer</summary>

**Answer: B.** Workspace monitoring collects data only from when it is turned on, and the default retention is 30 days. The database is read-only, and Contributors and above can query it.

</details>

**Question 41 · Copy activity tuning**

A Copy activity is overloading the on-premises SQL Server it reads from. You must reduce the load on that server. Which setting do you change?

- **A.** Set Intelligent throughput optimization to Maximum
- **B.** Set Intelligent throughput optimization to 256
- **C.** Lower the Degree of copy parallelism
- **D.** Raise the Degree of copy parallelism

<details><summary>Show answer</summary>

**Answer: C.** Lowering the Degree of copy parallelism reduces load on the machines that host the data store. Intelligent throughput optimization controls the service's compute.

</details>

# Section 7: questions 42 to 51 (Implement and manage)

**Question 42 · Deployment pipelines**

A team deploys a semantic model and its reports from Dev to an empty Test stage for the first time. In Test, the reports show no data and the model has no refresh schedule. What explains this?

- **A.** The deployment failed silently and must be rerun
- **B.** Deployment copies metadata only, and the refresh schedule isn't copied; refresh the model in Test and set a schedule there
- **C.** Workspace permissions were copied, but the viewers haven't accepted access yet
- **D.** A missing deployment rule stopped the data from being copied

<details><summary>Show answer</summary>

**Answer: B.** Deployment copies metadata only. Data and the refresh schedule aren't copied, so refresh the model in the target stage and set a schedule there.

</details>

**Question 43 · Deployment permissions**

An engineer is a pipeline admin, a Contributor in the Dev workspace and a Viewer in the Test workspace. Test already has content. Deploying from Dev to Test fails. What is the smallest change that fixes it?

- **A.** Make the engineer an Admin in both workspaces
- **B.** Make the engineer a Member in Dev
- **C.** Nothing; pipeline admin is enough, so retry
- **D.** Make the engineer a Contributor in Test

<details><summary>Show answer</summary>

**Answer: D.** Deploying to a stage with content needs pipeline admin plus at least Contributor in both the source and target workspaces.

</details>

**Question 44 · Row-level security**

A Warehouse table has a security policy so that each sales rep sees only their own rows. A workspace Admin now needs to see every row to validate a load, and sees only some. Which statement is correct?

- **A.** Security policies apply to all users, including dbo; the predicate must be written to allow the Admin
- **B.** Admin, Member and Contributor bypass row-level security automatically, so the policy must be broken
- **C.** The policy needs a block predicate for the Admin
- **D.** Grant the Admin the `UNMASK` permission

<details><summary>Show answer</summary>

**Answer: A.** Security policies apply to all users, including dbo. Admin, Member and Contributor don't bypass row-level security; the predicate must allow them.

</details>

**Question 45 · Dynamic data masking**

A `Salary` column in a Warehouse is masked with `default()`. An analyst with only `SELECT` runs:

```sql
SELECT Name, Salary FROM Employees WHERE Salary > 99999 AND Salary < 100001;
```

What happens, and what does it imply?

- **A.** The query fails, because masked columns can't be used in a `WHERE` clause
- **B.** No rows are returned, because the filter is evaluated against the masked value
- **C.** Matching rows are returned with `Salary` shown as 0, so the analyst can infer the real value; masking alone isn't enough
- **D.** Matching rows are returned with `Salary` shown as `XXXX`

<details><summary>Show answer</summary>

**Answer: C.** default() shows a number as 0 (a string as XXXX). The WHERE clause still runs on real values, so the rows returned reveal the range. Masking doesn't protect against inference.

</details>

**Question 46 · Workspace roles**

Priya must query a lakehouse through the SQL analytics endpoint with T-SQL, must not read the data through Spark or OneLake APIs, and must not edit anything. Sam must connect the workspace to a Git repository. What are the lowest roles that work?

- **A.** Priya: Viewer. Sam: Member
- **B.** Priya: Viewer. Sam: Admin
- **C.** Priya: Contributor. Sam: Admin
- **D.** Priya: Viewer. Sam: Contributor

<details><summary>Show answer</summary>

**Answer: B.** A Viewer can read with T-SQL but not through Spark or OneLake APIs. Connecting a workspace to a Git repository is Admin only.

</details>

**Question 47 · Sensitivity labels (retry of last week's miss)**

Which statement is true?

- **A.** A labeled Power BI report exported to a .csv file keeps the label's protection
- **B.** A label on a Power BI semantic model flows downstream to a lakehouse built from it
- **C.** With mandatory labeling on, a user can't save a pipeline that has no label
- **D.** A SQL analytics endpoint autogenerated from a lakehouse takes the lakehouse's label, not a label from further upstream

<details><summary>Show answer</summary>

**Answer: D.** An autogenerated SQL analytics endpoint takes its parent lakehouse's label. .csv export carries no protection, Power BI to Fabric isn't a supported direction, and mandatory labeling isn't enforced for pipelines.

</details>

**Question 48 · Spark workspace settings**

Engineers attach environments that set their own driver and executor cores and memory, but every notebook still runs with the default pool's configuration. What must change, and who can change it?

- **A.** A workspace Admin turns on "Customize compute configurations for items" on the Pool tab
- **B.** A workspace Contributor turns on high concurrency mode
- **C.** A capacity admin enables Customized workspace pools
- **D.** A workspace Admin turns on "Reserve maximum cores for active Spark jobs"

<details><summary>Show answer</summary>

**Answer: A.** Customize compute configurations for items (workspace Admin, Pool tab) lets an environment set driver and executor size. Customized workspace pools is a capacity setting that allows custom pools.

</details>

**Question 49 · Domains**

A finance lead is the Admin of several workspaces. She must be able to assign her own workspaces to the Finance domain from each workspace's settings, and must not get access to the Domains tab in the admin portal. Which role should she be given?

- **A.** Domain admin
- **B.** Fabric admin
- **C.** Domain contributor
- **D.** Workspace Member

<details><summary>Show answer</summary>

**Answer: C.** A domain contributor is a workspace Admin allowed to assign their own workspaces from workspace settings, with no access to the Domains tab. A domain admin works in the admin portal.

</details>

**Question 50 · Pipeline schedules and triggers (select two)**

Which two statements are true?

- **A.** Leaving the end date blank creates an open-ended schedule
- **B.** A single pipeline can have up to 20 schedules
- **C.** A storage event trigger runs without creating any other items in the workspace
- **D.** `@pipeline()?.TriggerEvent?.FileName` returns NULL in a manual test run
- **E.** Failure notification emails are also sent for on-demand runs

<details><summary>Show answer</summary>

**Answer: B and D.** A pipeline can have up to 20 schedules, and TriggerEvent.FileName is NULL in a manual test run. An end date is required; a trigger creates an eventstream and an Activator item; emails cover scheduled runs only.

</details>

**Question 51 · Spark job admission**

A workspace runs critical Spark jobs that must be guaranteed their maximum cores at the moment they are admitted. Which workspace setting do you change?

- **A.** On the Jobs tab, turn on "Reserve maximum cores for active Spark jobs"
- **B.** Raise the Spark session timeout
- **C.** Set a maximum job lifetime
- **D.** Turn on high concurrency mode for notebooks

<details><summary>Show answer</summary>

**Answer: A.** Optimistic job admission is the default. Reserve maximum cores for active Spark jobs turns it off and reserves the maximum cores.

</details>

# Section 8: questions 52 to 61 (Implement and manage, security and lifecycle)

**Question 52 · Column-level security**

In a Warehouse, an analyst has been granted `SELECT` on `Customers(CustomerID, FirstName, LastName)` only. The table also has a `CreditCard` column. The analyst runs `SELECT * FROM Customers;`. What happens?

- **A.** All rows are returned, with `CreditCard` shown as NULL
- **B.** All rows are returned, with `CreditCard` shown as `XXXX`
- **C.** The query fails with a permission-denied error on the `CreditCard` column
- **D.** Only the three granted columns are returned

<details><summary>Show answer</summary>

**Answer: C.** Column-level security denies the column: SELECT * fails with Msg 230. The user must name only the granted columns.

</details>

**Question 53 · OneLake security roles**

A user with the Viewer role belongs to two OneLake security roles on the same lakehouse table. Role 1 has a row filter `Region = 'EU'`. Role 2 has a row filter `Region = 'US'`. Which rows does the user see?

- **A.** No rows, because both filters must be true
- **B.** Rows for EU and rows for US
- **C.** Only EU rows, from the first role
- **D.** All rows in the table

<details><summary>Show answer</summary>

**Answer: B.** Across OneLake security roles, row filters combine with OR, so the user sees EU and US rows.

</details>

**Question 54 · The DefaultReader role**

A lakehouse has OneLake security enabled, and someone deletes its `DefaultReader` role. Dana has only the ReadAll item permission. Omar is a workspace Contributor. Who can still read the lakehouse data?

- **A.** Both Dana and Omar
- **B.** Neither
- **C.** Dana only
- **D.** Omar only; Dana loses access until she is added to another OneLake security role

<details><summary>Show answer</summary>

**Answer: D.** ReadAll gives data access only through DefaultReader. Delete the role and ReadAll users lose access; Admin, Member and Contributor keep it through their Write permission.

</details>

**Question 55 · Column rules across roles**

A user belongs to two OneLake security roles on the same table. Role A hides the `SSN` column. Role B grants every column. What does the user see?

- **A.** In Spark, `SSN` is visible; through the SQL analytics endpoint, `SSN` is blocked
- **B.** `SSN` is blocked in both
- **C.** `SSN` is visible in both
- **D.** In Spark, `SSN` is blocked; through the SQL analytics endpoint, `SSN` is visible

<details><summary>Show answer</summary>

**Answer: A.** Column rules combine as a union across roles, except at the SQL analytics endpoint, where any role that hides a column blocks it.

</details>

**Question 56 · Git integration**

A developer with the Contributor role has changed two items in a Git-connected workspace. Meanwhile a teammate pushed commits to the connected branch that change different items. The developer's Commit button is disabled. What should the developer do?

- **A.** Disconnect the workspace from Git and reconnect it
- **B.** Resolve a merge conflict in the Git repository
- **C.** Update the workspace from Git, then commit
- **D.** Ask a workspace Admin to commit, because only Admins can

<details><summary>Show answer</summary>

**Answer: C.** If the Git branch has new commits, Commit is disabled until you update the workspace. Different items changed, so there is no conflict.

</details>

**Question 57 · Git integration rules**

Which statement is true?

- **A.** Sensitivity labels are committed to Git along with the items
- **B.** Update always brings in the whole branch, while Commit lets you choose which items to include
- **C.** A workspace Viewer can see the Git status of items
- **D.** Updating from Git restores an item's data as well as its definition

<details><summary>Show answer</summary>

**Answer: B.** Update always brings in the whole branch; Commit lets you choose items. Labels aren't supported, a Viewer sees no Git information, and Git restores definitions, not data.

</details>

**Question 58 · Deployment rules**

A notebook in the Dev stage uses a dev lakehouse as its default. After every deployment to Test, it must use the test lakehouse as its default, with no manual step. What do you configure?

- **A.** A default lakehouse rule on the notebook in the Dev stage
- **B.** A parameter rule on the notebook in the Test stage
- **C.** A data source rule on the notebook in the Test stage
- **D.** A default lakehouse rule on the notebook in the Test stage, created by the notebook's owner

<details><summary>Show answer</summary>

**Answer: D.** A notebook supports only a default lakehouse rule. Rules are created in the target stage by the item owner, never in the development stage.

</details>

**Question 59 · Endorsement (select two)**

Which two statements are true?

- **A.** Any user with write permission on an item can promote it
- **B.** A Power BI dashboard can be certified
- **C.** Master data can be applied only to items that contain data, such as lakehouses and semantic models
- **D.** Once certification is enabled, any user can certify an item
- **E.** Certification can't be delegated to domain administrators

<details><summary>Show answer</summary>

**Answer: A and C.** Anyone with write permission can promote. Master data applies only to items that contain data. Dashboards can't be certified, only admin-specified users can certify, and certification can be delegated to domain admins.

</details>

**Question 60 · Sharing an item**

An analyst outside the workspace must read one lakehouse's data with T-SQL through the SQL analytics endpoint. She must not read it through Spark, and must not get access to anything else in the workspace. What do you do?

- **A.** Share the lakehouse with no additional permissions
- **B.** Share the lakehouse with "Read all with SQL analytics endpoint"
- **C.** Share the lakehouse with "Read all with Apache Spark"
- **D.** Add her to the workspace as a Viewer

<details><summary>Show answer</summary>

**Answer: B.** Read is always granted when sharing; Read all with SQL analytics endpoint adds T-SQL data access. A workspace role would expose every item.

</details>

**Question 61 · Selective deployment**

You want to deploy one report from Dev to Test. Its semantic model changed and doesn't exist in Test yet. You want to deploy only what is needed and avoid a failed deployment. What do you do?

- **A.** Deploy all content in the stage
- **B.** Create a deployment rule for the report
- **C.** Deploy backward from Test first
- **D.** Select the report, then use Select related to include the items it depends on

<details><summary>Show answer</summary>

**Answer: D.** Select related adds the items a selection depends on, which avoids a failed deployment.

</details>
