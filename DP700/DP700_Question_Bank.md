# DP-700 Question Bank

Every question from the coach sessions of Nov 6 to Nov 15, 2026, with its options, the correct answer, a one-line reason and the answer you gave. All scenarios are fictional. Facts were checked against Microsoft Learn on the day each question was written; the full explanations and sources are in the Reading Pack and the chat.

**Questions you missed or skipped (36):** Question 3, Question 6, Case study 1, question 4, Case study 1, question 5, Question 8, Question 15, Question 18, Question 20, Question 22, Question 23, Question 31, Question 35, Question 36, Question 38, Question 39, Question 45, Question 46, Question 47, Question 48, Question 49, Question 50, Question 52, Question 54, Question 58, Question 59, Mock 1, Mock 8, Mock 13, Mock 14, Mock 16, Mock 18, Mock 20, Mock 26, Mock 27, Mock 33, Mock 45.

# Section 1: coach questions 1 to 6 (mixed domains)

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

> **Answer: C.** The transport-level error means the server dropped a long-running connection; the documented fix is to check server logs and network stability and split the copy into partitions. A isn't a permission error, B is for the 60-minute workspace staging limit, D retries the same failure. You answered C: correct.

**Question 2 · Domain 3 · Identify and resolve errors in an eventstream (a weak area)**

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

> **Answer: B.** Data conversion errors count output events that can't be converted to the expected schema, and Runtime logs give error-level detail; both are available to a Viewer. A shows only message counts, C needs the Admin role and setting changes, D is the input-side metric. You answered B: correct.

**Question 3 · Domain 1 · Sensitivity labels (security and governance, a weak area)**

Your tenant has sensitivity labels enabled with downstream inheritance left at its default. Mandatory labeling is on and default labeling is off. A lakehouse, `Sales_LH`, is labeled **Confidential**.

For each statement, answer **Yes** if it is correct or **No** if it is not. Reply as five letters, for example `YNYNN`.

1. A notebook created from `Sales_LH` inherits the **Confidential** label when it is created.
2. A Power BI report is exported to a `.csv` file. The file keeps the report's sensitivity label and its protection.
3. An item autogenerated from `Sales_LH` takes `Sales_LH`'s label and does not inherit labels from items further upstream.
4. Downstream inheritance carries a label from a Power BI semantic model to a Fabric item that depends on it.
5. Fabric enforces mandatory labeling for lakehouses: a user cannot save a new lakehouse without choosing a label.

> **Answer: YNYNN.** 1 Yes: a notebook created from a lakehouse inherits its label. 2 No: export to .csv or .txt isn't supported. 3 Yes: autogenerated items take the parent's label only. 4 No: Power BI to Fabric isn't a supported direction. 5 No: mandatory labeling isn't enforced for lakehouses. You answered YYYNY: **missed.**

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

> **Answer: D and F.** The error names ReadAll, the Spark permission (ReadData is SQL). HTTP 430 is a capacity limit, fixed without a SKU change by Autoscale Billing for Fabric Spark. E is the fix for HTTP 429; A is for orphaned sessions. You answered D and F: correct.

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

> **Answer: A.** Production streams belong in a Spark job definition with a retry policy of unlimited retries; a processingTime trigger makes larger batches; Optimized Write removes manual repartition. B keeps a notebook, C caps retries, D hand-writes repartition. You answered A: correct.

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

> **Answer: E.** HoppingWindow(minute, 5, 1) gives overlapping 5-minute windows every minute; TIMESTAMP BY switches from arrival time to the device time; a SQL operator needs new destination nodes. A doesn't overlap, B outputs only on change, C uses arrival time, D reuses an existing node. You answered C: **missed.**

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

> **Answer: C.** No CDC, a reliable LastModifiedAt column, and one current row per claim: watermark incremental copy with merge on the key. Append duplicates updated claims; CDC isn't enabled. You answered C: correct.

**Case study 1, question 2 · Domain 1**

The engineer who failed to create the `eligibility` shortcut is a Contributor in `Claims-Prod` and has no role in `Partner-Data`. The partner team will grant the **minimum** access that lets the engineer create the shortcut in `claims_lh` that points to the `eligibility` table in `partner_lh`. What should they grant?

**A.** Write permission on the `partner_lh` item.

**B.** Read access to the `eligibility` table in `partner_lh` through OneLake security.

**C.** Make the engineer an Admin of `Claims-Prod`.

**D.** Make the engineer a Contributor in `Partner-Data`.

> **Answer: B.** Creating a shortcut needs Write where it is created plus Read on the target. A higher role in the source workspace doesn't supply target Read. You answered B: correct.

**Case study 1, question 3 · Domain 1**

Compliance's finding stands: T-SQL reads of the `eligibility` shortcut currently run under the owner of `claims_lh`, not under the analyst. The shortcut is a same-tenant OneLake shortcut created with default settings. Analysts query it through the `claims_lh` SQL analytics endpoint.

Requirement 4 says what analysts see must follow their **own** access in `partner_lh`. You also may not copy the data or give analysts new roles in `Partner-Data`. Which change meets all of that?

**A.** Recreate the shortcut with **Delegated identity**.

**B.** Grant the `Claims-Analysts` group the Contributor role in `Partner-Data`.

**C.** Define a T-SQL row-level security policy on the SQL analytics endpoint of `claims_lh`.

**D.** Switch the SQL analytics endpoint of `claims_lh` to **User's identity** mode.

> **Answer: D.** T-SQL in Delegated identity mode reads the shortcut as the item owner. User's identity mode uses the caller's own access. You answered D: correct.

**Case study 1, question 4 · Domain 3**

Requirement 5 says operations must learn about failed loads by email at no extra cost. The technical requirements say the load uses no pipeline, and recipients must include the Operations Entra group and the external compliance consultant, who has no account in the tenant. The nightly load is a scheduled Copy job.

Which setup meets all of that?

**A.** In the Monitor hub, configure **Schedule failure emails (free)** for the Copy job. Add the Operations group, add the consultant to the tenant as a B2B guest user, and select that guest as a recipient.

**B.** In the Monitor hub, configure **Schedule failure emails (free)** for the Copy job. Add the Operations group and type the consultant's external email address as a recipient.

**C.** Create an Activator-based alert rule for the Copy job and add the Operations group and the consultant as recipients.

**D.** Put the Copy job in a pipeline and add an Outlook activity after the Copy job activity.

> **Answer: A.** Schedule failure emails are free and need no pipeline. Recipients must be Entra users, groups or B2B guests; direct external addresses aren't supported. Activator rules are paid. You answered C: **missed.**

**Case study 1, question 5 · Domains 2 and 3 (select two)**

The failure emails from question 4 are now set up on the nightly Copy job. At 10:00 an operator runs the Copy job by hand and it fails. At 01:00 the next night, the scheduled run starts.

Which **two** statements are true?

**A.** Someone with only Viewer-level access to the workspace can reconfigure the failure notifications.

**B.** The 01:00 scheduled run resumes from the end of the last successful run.

**C.** The failed 10:00 run's partial progress advances the watermark.

**D.** The failure emails apply only to scheduled runs, so the failed manual run sends none.

> **Answer: B and D.** A failed run doesn't change the Copy job's state, so the next run resumes from the last successful run. Failure emails apply only to scheduled runs. Configuring them needs Contributor or Write. You answered A and B: **missed.**

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

> **Answer: B.** Database mirroring copies Azure SQL data into OneLake; metadata mirroring leaves Snowflake data in place and uses shortcuts. A copies Snowflake data, C (open mirroring) needs custom code, D: Azure SQL isn't a metadata mirroring source. You answered B: correct.

**Question 8 · Dataflow Gen2 incremental refresh**

A Dataflow Gen2 loads `Orders` from Azure SQL Database into a Lakehouse table. Today the destination uses the append update method with a dynamic schema, and a nightly notebook runs `OPTIMIZE` on that table. You must turn on incremental refresh covering the past 3 years. Which configuration works?

- **A.** Append, fixed schema, monthly buckets, keep the nightly `OPTIMIZE`
- **B.** Replace, dynamic schema, monthly buckets, remove the nightly `OPTIMIZE`
- **C.** Replace, fixed schema, monthly buckets, keep `OPTIMIZE` but run it after the refresh
- **D.** Replace, fixed schema, monthly buckets, remove the nightly `OPTIMIZE`
- **E.** Replace, fixed schema, daily buckets, remove the nightly `OPTIMIZE`

> **Answer: D.** Incremental refresh supports only the replace update method, needs a fixed schema, doesn't support OPTIMIZE on that table, and allows 50 buckets per query. A appends, B is dynamic, C keeps OPTIMIZE, E has about 1,095 buckets. You answered C: **missed.**

**Question 9 · Loading a dimensional model**

A Fabric Warehouse has `DimCustomer` (SCD type 2, `IDENTITY` surrogate key) and a large `FactSales`. Some sales arrive before their customer exists in the dimension, and the source system sometimes deletes customers. Which practice follows Microsoft's guidance?

- **A.** When real details arrive for a customer that the fact load inserted as an inferred member, update the attributes in place and set the inferred-member flag to FALSE
- **B.** Truncate and fully reload `DimCustomer` each night so it always matches the source
- **C.** Hold back sales rows whose customer lookup fails, and load them once the customer arrives
- **D.** When the source deletes a customer, delete that customer's rows from `DimCustomer`

> **Answer: A.** An inferred member's real details are late-arriving details, not an SCD change: update in place and clear the flag. B invalidates surrogate keys, C: the fact row must still be inserted, D: use a soft delete. You answered A: correct.

**Question 10 · KQL materialized views**

An Eventhouse has a materialized view `LatestState`, defined as `DeviceState | summarize arg_max(Timestamp, *) by DeviceId`. Two consumers use it:
- An operations dashboard that must include records ingested seconds ago.
- A nightly report that tolerates some staleness and must run as cheaply as possible.

How should each one query?

- **A.** Both query `LatestState` by name
- **B.** Both use `materialized_view("LatestState")`
- **C.** The dashboard queries `LatestState` by name; the report uses `materialized_view("LatestState")`
- **D.** The dashboard uses `materialized_view("LatestState")`; the report queries `LatestState` by name

> **Answer: C.** Querying by name combines the materialized part with the not-yet-processed delta, so it is always fresh. materialized_view() reads only the materialized part: faster, possibly stale. You answered C: correct.

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

> **Answer: B.** Direct ingestion does no processing, so operators need event processing before ingestion. Unchecking Activate ingestion and resuming from an earlier Custom time covers events that arrive before routing is ready. You answered B: correct.

# Section 4: questions 12 to 21 (Ingest and transform)

**Question 12 · Choosing a tool**

An analyst who is an experienced Power Query user must pull low-to-medium volumes from several SaaS sources, apply many complex transformations, and write to a lakehouse. She must write no code. Which tool fits?

- **A.** Pipeline Copy activity
- **B.** Copy job
- **C.** Dataflow Gen2
- **D.** Spark notebook
- **E.** Eventstream

> **Answer: C.** Dataflow Gen2 is the no-code tool for a Power Query user with many connectors and complex transformations. Copy activity and Copy job do only light transformation; Spark needs code; Eventstream is for events. You answered C: correct.

**Question 13 · Loading a Warehouse**

A stored procedure in a Fabric Warehouse must load large Parquet files from ADLS Gen2 into a warehouse table. Requirements: the load is part of the T-SQL logic, throughput is as high as possible, and the data is stored in the table. Which approach?

- **A.** `COPY INTO` the table from the Parquet files
- **B.** A loop of single-row `INSERT` statements
- **C.** A view over `OPENROWSET` on the files, queried each time
- **D.** A Dataflow Gen2 with the Warehouse as its destination

> **Answer: A.** COPY INTO gives the highest ingestion throughput and runs inside T-SQL logic. Single-row INSERTs perform poorly, OPENROWSET doesn't store the data, Dataflow Gen2 isn't T-SQL. You answered A: correct.

**Question 14 · T-SQL across items**

Warehouse `SalesDW` and lakehouse `SilverLH` are in workspace W1. Lakehouse `FinanceLH` is in workspace W2. You want to create warehouse tables from `SilverLH.dbo.Orders` and `FinanceLH.dbo.Budget` using `CREATE TABLE AS SELECT` with three-part names. Which statement is true?

- **A.** Both tables can be loaded this way
- **B.** Neither can; reading a lakehouse from a warehouse needs a pipeline
- **C.** Only `Budget` can be loaded this way
- **D.** Only `Orders` can be loaded this way, because T-SQL table sources must be in the same workspace

> **Answer: D.** A warehouse can read another item with a three-part name only when it is in the same workspace. Orders (W1) qualifies; Budget (W2) doesn't. You answered D: correct.

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

> **Answer: B.** An update policy transforms rows at ingestion. A 0s soft-delete on the source means raw rows aren't kept, and that requires a transactional policy, so a failure loses nothing. A isn't transactional, C is an aggregation, D keeps the raw rows. You skipped this one.

**Question 16 · Spark streaming deduplication**

A Spark structured streaming job reads device events. Retries resend the same `event_id`, sometimes with a different `event_time`. Events can be up to 10 minutes late. Requirements: remove duplicates in the stream by `event_id` alone, and keep the deduplication state bounded. Which code?

- **A.** `events.dropDuplicates(["event_id"])`
- **B.** `events.withWatermark("event_time", "10 minutes").dropDuplicates(["event_id", "event_time"])`
- **C.** `events.withWatermark("event_time", "10 minutes").dropDuplicatesWithinWatermark(["event_id"])`
- **D.** Write everything to Delta and remove duplicates in a nightly notebook

> **Answer: C.** dropDuplicatesWithinWatermark uses event_id alone and keeps state only for the watermark period. A has unbounded state, B treats a retry with a different event_time as new, D isn't in the stream. You answered C: correct.

**Question 17 · Spark windows**

The same job must count events per device over the last 10 minutes, with a new result every minute. Which grouping expression?

- **A.** `window("event_time", "10 minutes", "1 minute")`
- **B.** `window("event_time", "10 minutes")`
- **C.** `session_window("event_time", "10 minutes")`
- **D.** `window("event_time", "1 minute", "10 minutes")`

> **Answer: A.** In Spark, window(column, size, slide) is the overlapping (sliding) window: 10 minutes every 1 minute. B is tumbling, C is a session window, D has the arguments reversed. You answered A: correct.

**Question 18 · Eventstream operators**

Two sources send events with identical fields into one eventstream. Each event carries an array field `readings`. You need a single stream with one row per array element, using no-code operators. Which sequence?

- **A.** Join, then Expand
- **B.** Union, then Manage fields
- **C.** Group by, then Expand
- **D.** Union, then Expand

> **Answer: D.** Union combines streams that share fields; Expand creates one row per array value. Manage fields only adds, removes, renames or retypes fields; Join pairs two streams; Group by aggregates. You answered B: **missed.**

**Question 19 · Sharing a filtered stream**

An eventstream ingests all store events. Only events where `region = 'EU'` may be shared. Other teams must be able to find that filtered stream in the Real-Time hub, and an external application must consume it in real time over the Kafka protocol. Which setup?

- **A.** Add a custom endpoint destination to the default stream
- **B.** Add a Filter operator, output to a derived stream, and add a custom endpoint destination to that derived stream
- **C.** Add an Eventhouse destination with direct ingestion and let the application query the table
- **D.** Add a Filter operator and a Lakehouse destination, and let the application read the Delta table

> **Answer: B.** A Filter feeding a derived stream makes the subset discoverable in the Real-Time hub, and a custom endpoint on that derived stream serves Kafka clients. A shares unfiltered data; C and D aren't a Kafka stream. You answered B: correct.

**Question 20 · Dataflow Gen2 destinations (select two)**

Which two statements are true?

- **A.** A Warehouse destination supports only a fixed schema, needs staging enabled, and must be in the same workspace as the dataflow
- **B.** Automatic settings are supported for a Warehouse destination
- **C.** Fabric KQL database and Azure Data Explorer destinations don't support the replace update method
- **D.** With the append update method, a dynamic schema lets new source columns flow into the table
- **E.** If you manually delete an existing table that the dataflow didn't create, the next refresh recreates it

> **Answer: A and C.** A Warehouse destination needs a fixed schema, staging and the same workspace. KQL database and Azure Data Explorer don't support replace. Automatic settings exclude Warehouse; append can't change schema; a table the dataflow didn't create is never recreated. You answered A and E: **missed.**

**Question 21 · Choosing a data store**

A team is building an operational .NET application in Fabric. It needs high concurrency, full ACID transactions and enforced foreign keys. Analysts must query the same data without loading the application database. Which store?

- **A.** Fabric Data Warehouse
- **B.** Lakehouse
- **C.** Eventhouse
- **D.** SQL database in Fabric

> **Answer: D.** SQL database in Fabric is for operational apps with high concurrency, ACID transactions and enforced foreign keys, with a SQL analytics endpoint for analysts. A Warehouse doesn't enforce foreign keys. You answered D: correct.

# Section 5: questions 22 to 31 (Monitor and optimize)

**Question 22 · T-SQL error**

In a Fabric Warehouse, procedure A updates `FactSales` rows for region East while procedure B deletes rows for region West. B fails with error 24556, "Snapshot isolation transaction aborted due to update conflict". What explains it, and what is the fix?

- **A.** Row locks collided; add a `ROWLOCK` hint to both statements
- **B.** Conflicts are detected at table level even when the rows differ; run the procedures one after the other, or retry with backoff
- **C.** Snapshot isolation is too strict; set the session to `READ COMMITTED`
- **D.** The statements need one shared transaction; wrap both in `BEGIN DISTRIBUTED TRANSACTION`

> **Answer: B.** Warehouse write conflicts are detected at table level even when rows differ. Run the statements one after the other or retry with backoff. Isolation changes are ignored and distributed transactions aren't supported. You answered D: **missed.**

**Question 23 · Monitoring warehouse queries**

You need the queries that used the most CPU in a Warehouse over the past week, with the login that ran each one. Which view?

- **A.** `queryinsights.long_running_queries`
- **B.** `queryinsights.frequently_run_queries`
- **C.** `queryinsights.exec_requests_history`
- **D.** `queryinsights.exec_sessions_history`

> **Answer: C.** exec_requests_history has one row per completed request with allocated_cpu_time_ms and login_name. long_running_queries ranks by elapsed time; frequently_run_queries by count; exec_sessions_history covers sessions. You answered A: **missed.**

**Question 24 · Optimizing a lakehouse table**

A Delta table feeding Power BI reports has thousands of small files, and reads are slow. Old unreferenced files are also inflating storage. Compliance requires 7 days of time travel. Which maintenance run meets all of this?

- **A.** Compaction on with V-order applied, and VACUUM with a 7-day retention
- **B.** Compaction on with V-order applied, and VACUUM with a 1-day retention
- **C.** VACUUM only, with a 7-day retention
- **D.** Compaction on with V-order applied, and no VACUUM

> **Answer: A.** Compaction fixes small files, V-order speeds reads, and VACUUM at 7 days removes old files while keeping the required time travel. A 1-day VACUUM breaks time travel and fails by default. You answered A: correct.

**Question 25 · V-Order**

In a newly created workspace, one notebook session writes to both `bronze_raw` and `sales_gold`. Writes to `bronze_raw` must stay as fast as possible. New writes to `sales_gold` must be V-Ordered for dashboards. Which change does this?

- **A.** Run `SET spark.sql.parquet.vorder.default=TRUE` at the start of the session
- **B.** Nothing; V-Order is on by default in new workspaces
- **C.** Set the session default to TRUE, and add the writer option `parquet.vorder.enabled = false` on the `bronze_raw` write
- **D.** `ALTER TABLE sales_gold SET TBLPROPERTIES("delta.parquet.vorder.enabled" = "true")`

> **Answer: D.** The table property applies V-Order to writes on sales_gold only. A session default of TRUE V-Orders every write, even one explicitly set to false, and V-Order is off by default in new workspaces. You answered D: correct.

**Question 26 · Warehouse statistics**

A nightly load grows a Warehouse table from 1 million to 400 million rows. The first report query each morning is slow, and later runs are fast. What explains it, and what should you do?

- **A.** Fabric never creates statistics automatically; create them on every column
- **B.** Statistics are created or refreshed synchronously when a query needs them, so the first query pays for it; run `UPDATE STATISTICS` on the heavily used columns after the load
- **C.** Single-column statistics aren't enough; create multi-column statistics on the join keys
- **D.** Proactive statistics refresh is causing the delay; disable it

> **Answer: B.** Statistics are created or refreshed synchronously when a query needs them, so the first query pays. Run UPDATE STATISTICS after a load that changes row counts a lot. Multi-column statistics aren't supported. You answered B: correct.

**Question 27 · Eventhouse ingestion errors (select two)**

Which two statements about `EventhouseIngestionResultsLogs` are true?

- **A.** It records results for both successful and failed ingestions
- **B.** It is supported only for streaming ingestion
- **C.** `ShouldRetry` is a string that holds the time of the next retry
- **D.** `IngestionSourcePath` holds the source path or blob URI, and `IngestionErrorDetails` holds the error details
- **E.** It is a view in the Warehouse `queryinsights` schema

> **Answer: A and D.** The table records successful and failed ingestions, for queued ingestion. IngestionSourcePath holds the path or blob URI and IngestionErrorDetails the error. ShouldRetry is a boolean. You answered A and D: correct.

**Question 28 · Optimizing an Eventhouse**

A KQL table must keep 365 days of data queryable. Dashboards query only the last 30 days and must be fast. Older data is queried rarely, and the team wants to cut cost. What should you configure?

- **A.** Set the retention soft-delete period to 30 days
- **B.** Leave the caching policy at its default
- **C.** Set the caching policy so 30 days are hot, and keep retention at 365 days
- **D.** Create a materialized view over the table

> **Answer: C.** The caching policy sets how much data is hot; retention sets how much is queryable. 30 days hot with 365 days retention keeps dashboards fast and cuts cost. The default keeps everything hot. You answered C: correct.

**Question 29 · Semantic model refresh**

After a lakehouse load, a pipeline must refresh only the current partition of `FactSales` in a semantic model. The refresh must commit all at once, and the next activity must not start until the refresh has finished. Which setup?

- **A.** Semantic model refresh activity with the table and partition selected, Wait on completion on, and commit mode Transactional
- **B.** The same, with commit mode Partial Batch
- **C.** The same as A, with Wait on completion off
- **D.** A scheduled refresh in the semantic model's own settings, timed for when the pipeline usually ends

> **Answer: A.** Transactional commits the refresh all at once, and Wait on completion holds the next activity. Partial Batch commits in batches; a separate schedule isn't tied to the pipeline. You answered A: correct.

**Question 30 · Optimizing Spark**

A team enables the native execution engine at the environment level on Runtime 1.3. Which job will fall back to the regular Spark engine?

- **A.** A batch aggregation over Delta tables
- **B.** An ETL job that joins Parquet files
- **C.** A job that ingests CSV files
- **D.** A structured streaming job that reads from Azure Event Hubs

> **Answer: D.** The native execution engine doesn't support structured streaming, so that job falls back. Parquet, Delta and CSV are supported; JSON and XML also fall back. You answered D: correct.

**Question 31 · Alerts (retry of last week's miss)**

A scheduled notebook runs nightly. The team wants an email to a tenant security group each time a run **succeeds**. Workspace monitoring is not enabled, the engineer is a workspace Admin, and no pipeline may be added. What should the engineer do?

- **A.** Configure Schedule failure emails in the Monitor hub
- **B.** Enable workspace monitoring, then create an Activator-based alert rule on the Succeeded event
- **C.** Create an Activator-based alert rule on the Succeeded event without workspace monitoring
- **D.** Put the notebook in a pipeline and add an Outlook activity on success

> **Answer: B.** Free schedule failure emails fire only on failures. An alert on Succeeded needs an Activator-based rule, which needs workspace monitoring, and only a workspace Admin can enable that. D adds a pipeline. You answered A: **missed.** (Question wording fixed Nov 16: it originally said Contributor, which cannot enable workspace monitoring.)

# Section 6: questions 32 to 41 (Monitor and optimize)

**Question 32 · Capacity throttling**

Users report that interactive requests on a capacity are being rejected, while scheduled background jobs still start and run. Which throttling stage is the capacity in?

- **A.** Overage protection (10 minutes or less of future capacity used)
- **B.** Interactive delay (more than 10 and up to 60 minutes)
- **C.** Interactive rejection (more than 60 minutes and up to 24 hours)
- **D.** Background rejection (more than 24 hours)

> **Answer: C.** Over 60 minutes and up to 24 hours of future capacity is interactive rejection: interactive requests are rejected and background jobs still run. You answered C: correct.

**Question 33 · Recovering from throttling**

An F64 capacity is rejecting all requests. It is 2 a.m. and nothing is using it. The team must be able to accept new operations right away, will accept a billing event, and must not change the SKU. What should the admin do?

- **A.** Pause the capacity, then resume it
- **B.** Enable Autoscale on the capacity
- **C.** Scale up to F128
- **D.** Wait for the capacity to recover by itself

> **Answer: A.** Pausing bills the accumulated future usage; on resume the capacity has none and accepts work right away. Autoscale is for P SKUs, scaling up changes the SKU, waiting isn't immediate. You answered A: correct.

**Question 34 · Dataflow Gen2 errors**

A Dataflow Gen2 that refreshes through an on-premises gateway failed 10 days ago. An engineer with the workspace Viewer role needs the Power Query engine logs for that run. Which statement is true?

- **A.** The engineer needs at least the Contributor role to download the logs
- **B.** The logs are gone, because detailed logs are kept for 7 days
- **C.** The logs are available only if workspace monitoring was enabled before the run
- **D.** The engineer can open Recent runs, select the run and choose Download detailed logs, provided Admin consent for gateway diagnostics is enabled on the gateway

> **Answer: D.** Detailed logs can be downloaded from Recent runs for up to 28 days, the Viewer role is enough, and a gateway needs Admin consent for gateway diagnostics. You answered D: correct.

**Question 35 · Eventstream throughput**

An eventstream reads from an Azure Event Hubs source that has 1 partition. Ingestion tops out near 9 MB/s. The engineer sets the event throughput level to High and sees no improvement. Why?

- **A.** The retention period must be increased first
- **B.** With fewer than four partitions, throughput is limited by the partition count regardless of the level
- **C.** The throughput level applies only to destinations
- **D.** The High level needs an F64 capacity or larger

> **Answer: B.** With fewer than four Event Hubs partitions, throughput is limited by the partition count whatever the level. One partition gives about 9 MB/s. You answered D or B: **missed.**

**Question 36 · Changing eventstream throughput**

An eventstream has a Lakehouse destination and a custom endpoint destination, both active. How do you change the event throughput level?

- **A.** Change it directly; no node needs to be deactivated
- **B.** Delete the eventstream and recreate it at the new level
- **C.** Deactivate the nodes that support pause and resume, update the setting, then reactivate them
- **D.** Deactivate every node, including the custom endpoint, then update the setting

> **Answer: C.** Deactivate the nodes that support pause and resume, update the level, then reactivate. A custom endpoint doesn't support pause and resume, so it doesn't block the change. You answered D: **missed.**

**Question 37 · Warehouse cold start**

A Warehouse query is slow on its first run each morning. How do you confirm that a cold start caused it?

- **A.** Check `data_scanned_remote_storage_mb` in `queryinsights.exec_requests_history`; a nonzero value indicates a cold start
- **B.** Check `allocated_cpu_time_ms` in `queryinsights.exec_requests_history`
- **C.** Check the median elapsed time in `queryinsights.long_running_queries`
- **D.** Check `sys.dm_tran_locks` for blocking

> **Answer: A.** A nonzero data_scanned_remote_storage_mb in queryinsights.exec_requests_history indicates a cold start. You answered A: correct.

**Question 38 · V-Order in a Warehouse**

A team has a staging warehouse that only receives writes, and a reporting warehouse that is queried heavily. They are considering disabling V-Order. Which statement is correct?

- **A.** Disable it on both warehouses during the load, then re-enable it before reports run
- **B.** No action is needed, because V-Order is off by default in warehouses
- **C.** Disable it on the reporting warehouse to speed up report queries
- **D.** Disable it on the staging warehouse only, knowing it can't be re-enabled there

> **Answer: D.** V-Order is on by default in a warehouse and helps reads, so keep it on the reporting warehouse. Disable it only on a write-only staging warehouse; once disabled it can't be re-enabled. You answered A: **missed.**

**Question 39 · Spark autotune**

A team wants autotune to tune nightly Spark SQL queries. Their notebooks run on Runtime 1.3 in high concurrency mode. Which statement is true?

- **A.** Autotune won't run here: it is compatible only with Runtime 1.2 and doesn't run in high concurrency mode
- **B.** Autotune is on by default, so nothing needs to change
- **C.** Autotune will tune executor memory and cores for these queries
- **D.** Autotune will also tune their queries that finish in under 15 seconds

> **Answer: A.** Autotune (preview, off by default) works only on Runtime 1.2 and not in high concurrency mode. It tunes three settings (shuffle partitions, broadcast join threshold, max partition bytes) and skips queries under 15 seconds. You answered C: **missed.**

**Question 40 · Workspace monitoring**

A team wants 90 days of pipeline activity run logs, queryable with KQL. They enable workspace monitoring today. Which statement is true?

- **A.** The monitoring database is backfilled with the previous 30 days of activity
- **B.** Data is collected only from now on, and the default 30-day retention must be raised on the monitoring KQL database
- **C.** The team can add its own tables to the monitoring database
- **D.** Only workspace Admins can query the monitoring database

> **Answer: B.** Workspace monitoring collects data only from when it is turned on, and the default retention is 30 days. The database is read-only, and Contributors and above can query it. You answered B: correct.

**Question 41 · Copy activity tuning**

A Copy activity is overloading the on-premises SQL Server it reads from. You must reduce the load on that server. Which setting do you change?

- **A.** Set Intelligent throughput optimization to Maximum
- **B.** Set Intelligent throughput optimization to 256
- **C.** Lower the Degree of copy parallelism
- **D.** Raise the Degree of copy parallelism

> **Answer: C.** Lowering the Degree of copy parallelism reduces load on the machines that host the data store. Intelligent throughput optimization controls the service's compute. You answered C: correct.

# Section 7: questions 42 to 51 (Implement and manage)

**Question 42 · Deployment pipelines**

A team deploys a semantic model and its reports from Dev to an empty Test stage for the first time. In Test, the reports show no data and the model has no refresh schedule. What explains this?

- **A.** The deployment failed silently and must be rerun
- **B.** Deployment copies metadata only, and the refresh schedule isn't copied; refresh the model in Test and set a schedule there
- **C.** Workspace permissions were copied, but the viewers haven't accepted access yet
- **D.** A missing deployment rule stopped the data from being copied

> **Answer: B.** Deployment copies metadata only. Data and the refresh schedule aren't copied, so refresh the model in the target stage and set a schedule there. You answered B: correct.

**Question 43 · Deployment permissions**

An engineer is a pipeline admin, a Contributor in the Dev workspace and a Viewer in the Test workspace. Test already has content. Deploying from Dev to Test fails. What is the smallest change that fixes it?

- **A.** Make the engineer an Admin in both workspaces
- **B.** Make the engineer a Member in Dev
- **C.** Nothing; pipeline admin is enough, so retry
- **D.** Make the engineer a Contributor in Test

> **Answer: D.** Deploying to a stage with content needs pipeline admin plus at least Contributor in both the source and target workspaces. You answered D: correct.

**Question 44 · Row-level security**

A Warehouse table has a security policy so that each sales rep sees only their own rows. A workspace Admin now needs to see every row to validate a load, and sees only some. Which statement is correct?

- **A.** Security policies apply to all users, including dbo; the predicate must be written to allow the Admin
- **B.** Admin, Member and Contributor bypass row-level security automatically, so the policy must be broken
- **C.** The policy needs a block predicate for the Admin
- **D.** Grant the Admin the `UNMASK` permission

> **Answer: A.** Security policies apply to all users, including dbo. Admin, Member and Contributor don't bypass row-level security; the predicate must allow them. You answered A: correct.

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

> **Answer: C.** default() shows a number as 0 (a string as XXXX). The WHERE clause still runs on real values, so the rows returned reveal the range. Masking doesn't protect against inference. You answered D: **missed.**

**Question 46 · Workspace roles**

Priya must query a lakehouse through the SQL analytics endpoint with T-SQL, must not read the data through Spark or OneLake APIs, and must not edit anything. Sam must connect the workspace to a Git repository. What are the lowest roles that work?

- **A.** Priya: Viewer. Sam: Member
- **B.** Priya: Viewer. Sam: Admin
- **C.** Priya: Contributor. Sam: Admin
- **D.** Priya: Viewer. Sam: Contributor

> **Answer: B.** A Viewer can read with T-SQL but not through Spark or OneLake APIs. Connecting a workspace to a Git repository is Admin only. You answered D: **missed.**

**Question 47 · Sensitivity labels (retry of last week's miss)**

Which statement is true?

- **A.** A labeled Power BI report exported to a .csv file keeps the label's protection
- **B.** A label on a Power BI semantic model flows downstream to a lakehouse built from it
- **C.** With mandatory labeling on, a user can't save a pipeline that has no label
- **D.** A SQL analytics endpoint autogenerated from a lakehouse takes the lakehouse's label, not a label from further upstream

> **Answer: D.** An autogenerated SQL analytics endpoint takes its parent lakehouse's label. .csv export carries no protection, Power BI to Fabric isn't a supported direction, and mandatory labeling isn't enforced for pipelines. You answered B: **missed.**

**Question 48 · Spark workspace settings**

Engineers attach environments that set their own driver and executor cores and memory, but every notebook still runs with the default pool's configuration. What must change, and who can change it?

- **A.** A workspace Admin turns on "Customize compute configurations for items" on the Pool tab
- **B.** A workspace Contributor turns on high concurrency mode
- **C.** A capacity admin enables Customized workspace pools
- **D.** A workspace Admin turns on "Reserve maximum cores for active Spark jobs"

> **Answer: A.** Customize compute configurations for items (workspace Admin, Pool tab) lets an environment set driver and executor size. Customized workspace pools is a capacity setting that allows custom pools. You answered C: **missed.**

**Question 49 · Domains**

A finance lead is the Admin of several workspaces. She must be able to assign her own workspaces to the Finance domain from each workspace's settings, and must not get access to the Domains tab in the admin portal. Which role should she be given?

- **A.** Domain admin
- **B.** Fabric admin
- **C.** Domain contributor
- **D.** Workspace Member

> **Answer: C.** A domain contributor is a workspace Admin allowed to assign their own workspaces from workspace settings, with no access to the Domains tab. A domain admin works in the admin portal. You answered A: **missed.**

**Question 50 · Pipeline schedules and triggers (select two)**

Which two statements are true?

- **A.** Leaving the end date blank creates an open-ended schedule
- **B.** A single pipeline can have up to 20 schedules
- **C.** A storage event trigger runs without creating any other items in the workspace
- **D.** `@pipeline()?.TriggerEvent?.FileName` returns NULL in a manual test run
- **E.** Failure notification emails are also sent for on-demand runs

> **Answer: B and D.** A pipeline can have up to 20 schedules, and TriggerEvent.FileName is NULL in a manual test run. An end date is required; a trigger creates an eventstream and an Activator item; emails cover scheduled runs only. You answered D: **missed.**

**Question 51 · Spark job admission**

A workspace runs critical Spark jobs that must be guaranteed their maximum cores at the moment they are admitted. Which workspace setting do you change?

- **A.** On the Jobs tab, turn on "Reserve maximum cores for active Spark jobs"
- **B.** Raise the Spark session timeout
- **C.** Set a maximum job lifetime
- **D.** Turn on high concurrency mode for notebooks

> **Answer: A.** Optimistic job admission is the default. Reserve maximum cores for active Spark jobs turns it off and reserves the maximum cores. You answered A: correct.

# Section 8: questions 52 to 61 (Implement and manage, security and lifecycle)

**Question 52 · Column-level security**

In a Warehouse, an analyst has been granted `SELECT` on `Customers(CustomerID, FirstName, LastName)` only. The table also has a `CreditCard` column. The analyst runs `SELECT * FROM Customers;`. What happens?

- **A.** All rows are returned, with `CreditCard` shown as NULL
- **B.** All rows are returned, with `CreditCard` shown as `XXXX`
- **C.** The query fails with a permission-denied error on the `CreditCard` column
- **D.** Only the three granted columns are returned

> **Answer: C.** Column-level security denies the column: SELECT * fails with Msg 230. The user must name only the granted columns. You answered D: **missed.**

**Question 53 · OneLake security roles**

A user with the Viewer role belongs to two OneLake security roles on the same lakehouse table. Role 1 has a row filter `Region = 'EU'`. Role 2 has a row filter `Region = 'US'`. Which rows does the user see?

- **A.** No rows, because both filters must be true
- **B.** Rows for EU and rows for US
- **C.** Only EU rows, from the first role
- **D.** All rows in the table

> **Answer: B.** Across OneLake security roles, row filters combine with OR, so the user sees EU and US rows. You answered B: correct.

**Question 54 · The DefaultReader role**

A lakehouse has OneLake security enabled, and someone deletes its `DefaultReader` role. Dana has only the ReadAll item permission. Omar is a workspace Contributor. Who can still read the lakehouse data?

- **A.** Both Dana and Omar
- **B.** Neither
- **C.** Dana only
- **D.** Omar only; Dana loses access until she is added to another OneLake security role

> **Answer: D.** ReadAll gives data access only through DefaultReader. Delete the role and ReadAll users lose access; Admin, Member and Contributor keep it through their Write permission. You answered C: **missed.**

**Question 55 · Column rules across roles**

A user belongs to two OneLake security roles on the same table. Role A hides the `SSN` column. Role B grants every column. What does the user see?

- **A.** In Spark, `SSN` is visible; through the SQL analytics endpoint, `SSN` is blocked
- **B.** `SSN` is blocked in both
- **C.** `SSN` is visible in both
- **D.** In Spark, `SSN` is blocked; through the SQL analytics endpoint, `SSN` is visible

> **Answer: A.** Column rules combine as a union across roles, except at the SQL analytics endpoint, where any role that hides a column blocks it. You answered A: correct.

**Question 56 · Git integration**

A developer with the Contributor role has changed two items in a Git-connected workspace. Meanwhile a teammate pushed commits to the connected branch that change different items. The developer's Commit button is disabled. What should the developer do?

- **A.** Disconnect the workspace from Git and reconnect it
- **B.** Resolve a merge conflict in the Git repository
- **C.** Update the workspace from Git, then commit
- **D.** Ask a workspace Admin to commit, because only Admins can

> **Answer: C.** If the Git branch has new commits, Commit is disabled until you update the workspace. Different items changed, so there is no conflict. You answered C: correct.

**Question 57 · Git integration rules**

Which statement is true?

- **A.** Sensitivity labels are committed to Git along with the items
- **B.** Update always brings in the whole branch, while Commit lets you choose which items to include
- **C.** A workspace Viewer can see the Git status of items
- **D.** Updating from Git restores an item's data as well as its definition

> **Answer: B.** Update always brings in the whole branch; Commit lets you choose items. Labels aren't supported, a Viewer sees no Git information, and Git restores definitions, not data. You answered B: correct.

**Question 58 · Deployment rules**

A notebook in the Dev stage uses a dev lakehouse as its default. After every deployment to Test, it must use the test lakehouse as its default, with no manual step. What do you configure?

- **A.** A default lakehouse rule on the notebook in the Dev stage
- **B.** A parameter rule on the notebook in the Test stage
- **C.** A data source rule on the notebook in the Test stage
- **D.** A default lakehouse rule on the notebook in the Test stage, created by the notebook's owner

> **Answer: D.** A notebook supports only a default lakehouse rule. Rules are created in the target stage by the item owner, never in the development stage. You answered B: **missed.**

**Question 59 · Endorsement (select two)**

Which two statements are true?

- **A.** Any user with write permission on an item can promote it
- **B.** A Power BI dashboard can be certified
- **C.** Master data can be applied only to items that contain data, such as lakehouses and semantic models
- **D.** Once certification is enabled, any user can certify an item
- **E.** Certification can't be delegated to domain administrators

> **Answer: A and C.** Anyone with write permission can promote. Master data applies only to items that contain data. Dashboards can't be certified, only admin-specified users can certify, and certification can be delegated to domain admins. You answered A: **missed.**

**Question 60 · Sharing an item**

An analyst outside the workspace must read one lakehouse's data with T-SQL through the SQL analytics endpoint. She must not read it through Spark, and must not get access to anything else in the workspace. What do you do?

- **A.** Share the lakehouse with no additional permissions
- **B.** Share the lakehouse with "Read all with SQL analytics endpoint"
- **C.** Share the lakehouse with "Read all with Apache Spark"
- **D.** Add her to the workspace as a Viewer

> **Answer: B.** Read is always granted when sharing; Read all with SQL analytics endpoint adds T-SQL data access. A workspace role would expose every item. You answered B: correct.

**Question 61 · Selective deployment**

You want to deploy one report from Dev to Test. Its semantic model changed and doesn't exist in Test yet. You want to deploy only what is needed and avoid a failed deployment. What do you do?

- **A.** Deploy all content in the stage
- **B.** Create a deployment rule for the report
- **C.** Deploy backward from Test first
- **D.** Select the report, then use Select related to include the items it depends on

> **Answer: D.** Select related adds the items a selection depends on, which avoids a failed deployment. You answered D: correct.

# Section 9: full mock 1 (45 questions, score 34 of 45)

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

**Mock 1.** What must happen so `Dispatch` can meet requirement 1?
- **A.** Create a Copy job with CDC-based incremental copy
- **B.** Create a metadata mirror of `Dispatch`
- **C.** Disable CDC on `Dispatch`, then set up database mirroring
- **D.** Mirror from a read-only secondary replica of `Dispatch`

> **Answer: C.** An Azure SQL database can't be mirrored while CDC is enabled, and only a writable primary can be mirrored. You answered D: **missed.**

**Mock 2.** What explains the GPS ingestion cap?
- **A.** The event hub has fewer than four partitions, which limits throughput whatever the level
- **B.** The F64 capacity is too small for the High level
- **C.** The eventstream's retention period is too short
- **D.** The throughput level applies only to destinations

> **Answer: A.** Fewer than four Event Hubs partitions limits throughput whatever the level. You answered A: correct.

**Mock 3.** Which change meets requirement 2 and fixes the Admin's issue?
- **A.** Mask `LicenseNo` with dynamic data masking, and grant the Admin `UNMASK`
- **B.** Grant auditors `SELECT` on the allowed columns only, and change the security predicate to include the Admin
- **C.** Grant auditors `SELECT` on the allowed columns only, and rely on the Admin role bypassing row-level security
- **D.** Mask `LicenseNo` with dynamic data masking, and change the security predicate to include the Admin

> **Answer: B.** Column-level security makes a query that names the column fail; the row-level security predicate must allow the Admin, who doesn't bypass it. You answered B: correct.

**Mock 4.** How do you meet the `LoadFleet` lakehouse requirement?
- **A.** Create a default lakehouse rule in the `Ops-Dev` stage
- **B.** Create a parameter rule on the notebook in each target stage
- **C.** Create a data source rule on the notebook in each target stage
- **D.** Have the notebook's owner create a default lakehouse rule in the `Ops-Test` and `Ops-Prod` stages

> **Answer: D.** A notebook supports only a default lakehouse rule, created in the target stages by the item owner. You answered D: correct.

**Mock 5.** How do you meet requirement 3?
- **A.** Configure Schedule failure emails in the Monitor hub, with the security group and the vendor's guest account as recipients
- **B.** Create an Activator-based alert rule for the notebook
- **C.** Put the notebook in a pipeline with an Outlook activity on failure
- **D.** Configure Schedule failure emails, typing the vendor's external email address

> **Answer: A.** Free schedule failure emails go to Entra users, groups and B2B guests. Activator rules are paid and need workspace monitoring. You answered A: correct.

## Part 1, standalone questions

**Mock 6.** In a `runMultiple` DAG, the `Load` notebook must start only after `Extract` finishes, and must retry once after 10 seconds if it fails. Which activity definition does this?
- **A.** `{"name": "Load", "path": "LoadNb", "dependsOn": ["Extract"], "retry": 1}`
- **B.** `{"name": "Load", "path": "LoadNb", "dependencies": ["Extract"], "retry": 1, "retryIntervalInSeconds": 10}`
- **C.** `{"name": "Load", "path": "LoadNb", "concurrency": 1, "timeoutInSeconds": 10}`
- **D.** `{"name": "Load", "path": "LoadNb", "args": {"after": "Extract", "retry": 1}}`

> **Answer: B.** In a DAG activity, dependencies sets the order, and retry with retryIntervalInSeconds sets the retry. You answered B: correct.

**Mock 7.** A pipeline parameter `myNumber` holds 42. Which expression returns it as a number, not a string?
- **A.** `"@{pipeline().parameters.myNumber}"`
- **B.** `"@@pipeline().parameters.myNumber"`
- **C.** `"pipeline().parameters.myNumber"`
- **D.** `"@pipeline().parameters.myNumber"`

> **Answer: D.** "@pipeline().parameters.x" returns the value with its type; "@{...}" always returns a string; @@ escapes. You answered D: correct.

**Mock 8.** Where can you create shortcuts in a lakehouse?
- **A.** In Tables only at the top level; in Files at any folder level
- **B.** In Tables at any level; in Files only at the top level
- **C.** At any level in both
- **D.** Only at the top level in both

> **Answer: A.** Shortcuts go only at the top level of Tables, but at any level of Files. You answered D: **missed.**

**Mock 9.** A lakehouse has a shortcut `MyShortcut` to an ADLS Gen2 folder, and the user has write permission on that storage. The user deletes the folder `MyShortcut/Foo/Bar` in the lakehouse. What happens?
- **A.** Only the shortcut is removed
- **B.** The delete fails, because shortcuts are read-only
- **C.** The `Bar` folder is deleted in the ADLS Gen2 account
- **D.** `Bar` is hidden in the lakehouse but stays in ADLS Gen2

> **Answer: C.** Deleting inside a shortcut deletes in the target if you have permission there. Deleting the shortcut removes only the shortcut. You answered C: correct.

**Mock 10.** An Azure SQL database with row-level security and dynamic data masking is mirrored to Fabric. What applies to the mirrored data in OneLake?
- **A.** Both are enforced automatically on the mirrored data
- **B.** Neither is propagated; the data must be secured again in Fabric
- **C.** Row-level security is propagated, masking is not
- **D.** Mirroring fails while either feature is in use

> **Answer: B.** Row-level security, column permissions and masking on the source aren't propagated to the mirrored data. You answered B: correct.

**Mock 11.** You create a OneLake shortcut in a KQL database. How do you query it?
- **A.** By table name, like any KQL table
- **B.** With the `materialized_view()` function
- **C.** With `OPENROWSET`
- **D.** With the `external_table()` function

> **Answer: D.** A KQL database treats a shortcut as an external table, queried with external_table(). You answered D: correct.

**Mock 12.** A workspace has Amazon S3 shortcuts, and egress costs are high. Files are 200 MB to 3 GB. Which statement about shortcut caching is correct?
- **A.** Turn it on in the workspace's OneLake settings with a retention of up to 28 days; files over 1 GB won't be cached
- **B.** Turn it on with a 90-day retention; all files are cached
- **C.** Caching isn't available for S3 shortcuts
- **D.** Turn it on per shortcut; only files over 1 GB are cached

> **Answer: A.** Caching covers S3, S3-compatible, GCS and gateway shortcuts; retention is 1 to 28 days; files over 1 GB aren't cached. You answered A: correct.

**Mock 13.** A capacity has used 30 minutes of future capacity. What do users experience?
- **A.** Nothing; this is within overage protection
- **B.** Interactive requests are rejected
- **C.** Interactive requests are delayed by 20 seconds
- **D.** All requests are rejected

> **Answer: C.** 10 to 60 minutes of future capacity is the interactive delay stage: a 20-second delay. You answered B: **missed.**

**Mock 14.** A notebook that lists tables in a loop starts failing with HTTP 429. What is the documented fix?
- **A.** Turn on Autoscale Billing for Spark
- **B.** Retry with exponential backoff and jitter, honoring `Retry-After`
- **C.** Grant the user ReadAll on the lakehouse
- **D.** Restart the capacity

> **Answer: B.** HTTP 429 is an API rate limit: back off with jitter and honor Retry-After. HTTP 430 is the capacity error. You answered D: **missed.**

**Mock 15.** You connect a workspace to a Git branch for the first time. Both the workspace and the branch already have content. What happens?
- **A.** The connection fails until one side is emptied
- **B.** The branch content always overwrites the workspace
- **C.** The two are merged item by item
- **D.** You must choose a direction: commit overwrites Git, update overwrites the workspace

> **Answer: D.** When both sides have content you choose a direction: commit overwrites Git, update overwrites the workspace. You answered D: correct.

## Part 2

**Mock 16.** A Dataflow Gen2 must use incremental refresh over the past 2 years into a Lakehouse table. Which configuration is valid?
- **A.** Monthly buckets, replace update method, fixed schema
- **B.** Weekly buckets, replace update method, fixed schema
- **C.** Monthly buckets, append update method, fixed schema
- **D.** Monthly buckets, replace update method, dynamic schema

> **Answer: A.** Incremental refresh needs replace and a fixed schema, with at most 50 buckets per query (weekly over 2 years is 104). You answered D: **missed.**

**Mock 17.** Each event in an eventstream carries an array field `items`. Which no-code operator produces one row per array element?
- **A.** Manage fields
- **B.** Group by
- **C.** Expand
- **D.** Union

> **Answer: C.** Expand creates one row per array value. You answered C: correct.

**Mock 18.** A KQL table `Raw` receives JSON. Each row must be parsed into a typed table at ingestion, the raw rows must not be kept, and a failed transform must lose nothing. Which design?
- **A.** A materialized view over `Raw`
- **B.** A non-transactional update policy, with a `0s` soft-delete on `Raw`
- **C.** A transactional update policy, with the default retention on `Raw`
- **D.** A transactional update policy, with a `0s` soft-delete on `Raw`

> **Answer: D.** A 0s soft-delete on the source requires a transactional update policy, so a failure loses nothing. You answered B: **missed.**

**Mock 19.** A Spark stream must drop duplicates by `event_id` alone, with events up to 10 minutes late and bounded state. Which code?
- **A.** `events.dropDuplicates(["event_id"])`
- **B.** `events.withWatermark("event_time", "10 minutes").dropDuplicatesWithinWatermark(["event_id"])`
- **C.** `events.withWatermark("event_time", "10 minutes").dropDuplicates(["event_id", "event_time"])`
- **D.** `events.dropDuplicatesWithinWatermark(["event_id"])` with no watermark

> **Answer: B.** dropDuplicatesWithinWatermark with a watermark uses event_id alone and keeps bounded state. You answered B: correct.

**Mock 20.** Which value is not a supported `FILE_TYPE` for `COPY INTO` in a Fabric Warehouse?
- **A.** CSV
- **B.** PARQUET
- **C.** AVRO
- **D.** JSONL

> **Answer: C.** COPY INTO supports CSV, JSONL and PARQUET. You answered D: **missed.**

**Mock 21.** `DimCustomer` is SCD type 2. A customer changed region in March, which created a new version row. A sale for that customer loads in April. Which key does the fact row get?
- **A.** The surrogate key of the customer's current version
- **B.** The surrogate key of the customer's first version
- **C.** The customer's business key from the source
- **D.** The key of the Unknown member

> **Answer: A.** The fact load looks up the surrogate key of the dimension's current version. You answered A: correct.

**Mock 22.** A nightly report reads a KQL materialized view. It tolerates slightly stale data and must run as cheaply as possible. How should it query?
- **A.** By the view's name
- **B.** By querying the source table with the same `summarize`
- **C.** By the view's name with `take 100`
- **D.** With `materialized_view("ViewName")`

> **Answer: D.** materialized_view() reads only the materialized part: cheapest, possibly stale. You answered D: correct.

**Mock 23.** Two procedures run `MERGE` on the same Warehouse table at the same time, touching different rows. One fails with error 24556. What is the fix?
- **A.** Add a `ROWLOCK` hint
- **B.** Run them one after the other, or retry with backoff
- **C.** Set the isolation level to `READ COMMITTED`
- **D.** Enable result set caching

> **Answer: B.** Conflicts are detected at table level; run sequentially or retry with backoff. You answered B: correct.

**Mock 24.** A Warehouse query finished 5 minutes ago and isn't in `queryinsights.exec_requests_history`. Why?
- **A.** Completed queries can take up to 15 minutes to appear
- **B.** Only failed queries are stored
- **C.** Only workspace Admins can see other users' queries
- **D.** The view exists only for the SQL analytics endpoint

> **Answer: A.** Completed queries can take up to 15 minutes to appear in query insights. You answered A: correct.

**Mock 25.** In the Lakehouse maintenance dialog, a user runs VACUUM with a 2-day retention. What happens by default?
- **A.** It runs, and time travel is unaffected
- **B.** The retention is rounded up to 7 days
- **C.** The request fails, because the retention is under seven days
- **D.** It deletes the table's whole history

> **Answer: C.** A VACUUM retention under seven days fails by default. You answered C: correct.

**Mock 26.** With the native execution engine enabled, which job falls back to the regular Spark engine?
- **A.** A join over Parquet files
- **B.** An aggregation over Delta tables
- **C.** A load of CSV files
- **D.** A job that reads JSON files

> **Answer: D.** The native execution engine supports Parquet, Delta and CSV; JSON and XML fall back. You answered B: **missed.**

**Mock 27.** A Fabric admin sets a default domain for a security group. One member already administers a workspace that is assigned to another domain. What happens to that workspace?
- **A.** It moves to the default domain
- **B.** It keeps its current domain
- **C.** It belongs to both domains
- **D.** It becomes unassigned

> **Answer: B.** A default domain doesn't override a workspace's existing domain. You answered A: **missed.**

**Mock 28.** In a Git-connected workspace, who can commit workspace changes to Git?
- **A.** Only a workspace Admin
- **B.** A Viewer with write access to the repository
- **C.** A Contributor with write permission on all items, and Contribute permission in Git
- **D.** Only a Member

> **Answer: C.** Commit needs Contributor (write on all items) plus Contribute permission in Git. You answered C: correct.

**Mock 29.** In which case does a sensitivity label flow downstream?
- **A.** From a labeled lakehouse to a Power BI semantic model built on it
- **B.** From a labeled Power BI report to the lakehouse behind it
- **C.** From a labeled report to a .txt export
- **D.** From a tenant's mandatory labeling policy to a new warehouse

> **Answer: A.** Fabric to Power BI is a supported downstream direction; Power BI to Fabric isn't. You answered A: correct.

**Mock 30.** You edit the definition of a OneLake security role, without changing its members. About how long before the change applies?
- **A.** Immediately
- **B.** About 5 minutes
- **C.** About an hour
- **D.** About 24 hours

> **Answer: B.** Role definition changes take about 5 minutes; group membership changes about an hour. You answered B: correct.

## Part 3

**Mock 31.** An eventstream SQL operator must output, every minute, the average speed per truck over the last 10 minutes, using the device's `gpsTime`. Which query parts do this?
- **A.** `FROM input` with `HoppingWindow(minute, 10, 1)`
- **B.** `FROM input TIMESTAMP BY gpsTime` with `TumblingWindow(minute, 10)`
- **C.** `FROM input TIMESTAMP BY gpsTime` with `HoppingWindow(minute, 10, 1)`
- **D.** `FROM input TIMESTAMP BY gpsTime` with `SlidingWindow(minute, 10)`

> **Answer: C.** HoppingWindow for the overlapping window, TIMESTAMP BY for device time. You answered C: correct.

**Mock 32.** An eventstream applies a Filter operator, then sends the result to an Eventhouse. Which ingestion mode does that destination use?
- **A.** Event processing before ingestion
- **B.** Direct ingestion
- **C.** Either mode works after an operator
- **D.** Direct ingestion with a mapping transformation

> **Answer: A.** Operators before an Eventhouse destination require event processing before ingestion. You answered A: correct.

**Mock 33.** Marketing data in Snowflake must be queryable from Fabric, and no copy may be made in OneLake. Which feature?
- **A.** Database mirroring
- **B.** Open mirroring
- **C.** A Copy job
- **D.** Metadata mirroring

> **Answer: D.** Metadata mirroring leaves the data in Snowflake. Open mirroring means writing your own replication application. You answered B: **missed.**

**Mock 34.** An operational application needs high concurrency, ACID transactions and enforced foreign keys. Which Fabric store?
- **A.** Fabric Data Warehouse
- **B.** SQL database in Fabric
- **C.** Lakehouse
- **D.** Eventhouse

> **Answer: B.** SQL database in Fabric: operational, ACID, enforced foreign keys. You answered B: correct.

**Mock 35.** Which Dataflow Gen2 destination doesn't support the replace update method?
- **A.** Fabric KQL database
- **B.** Lakehouse
- **C.** Warehouse
- **D.** Azure SQL Database

> **Answer: A.** KQL database (and Azure Data Explorer) destinations don't support replace. You answered A: correct.

**Mock 36.** What does Spark autotune adjust?
- **A.** Executor memory and cores
- **B.** The number of nodes in the pool
- **C.** Shuffle partitions, the broadcast join threshold and the maximum partition bytes
- **D.** V-Order and optimized write

> **Answer: C.** Autotune adjusts those three Spark settings only. You answered C: correct.

**Mock 37.** Which statement about V-Order in a Fabric Warehouse is correct?
- **A.** It is off by default
- **B.** It can be switched on and off for each table
- **C.** Disabling it makes report queries faster
- **D.** It is on by default, is disabled for the whole warehouse, and can't be re-enabled

> **Answer: D.** Warehouse V-Order is on by default, is disabled per warehouse, and can't be re-enabled. You answered D: correct.

**Mock 38.** After a nightly load multiplies a Warehouse table's row count, the first query each morning is slow and later ones are fast. What should you add to the load?
- **A.** `OPTIMIZE` on the table
- **B.** `UPDATE STATISTICS` on the heavily used columns
- **C.** Multi-column statistics on the join keys
- **D.** A step that disables automatic statistics

> **Answer: B.** Statistics refresh synchronously at query time; update them after a big load. You answered B: correct.

**Mock 39.** A KQL table must keep 365 days queryable. Dashboards read only the last 30 days, and cost must come down. What do you set?
- **A.** A 30-day retention policy
- **B.** A materialized view
- **C.** A caching policy that keeps 30 days hot, with retention left at 365 days
- **D.** Nothing; the default caching policy is the cheapest

> **Answer: C.** Caching policy sets hot data; retention sets queryable data. You answered C: correct.

**Mock 40.** A pipeline must refresh a semantic model so that the refresh commits all at once, and the next activity waits for it to finish. Which settings on the Semantic model refresh activity?
- **A.** Commit mode Transactional, Wait on completion on
- **B.** Commit mode Partial Batch, Wait on completion on
- **C.** Commit mode Transactional, Wait on completion off
- **D.** Commit mode Partial Batch, Wait on completion off

> **Answer: A.** Transactional commits all at once; Wait on completion holds the next activity. You answered A: correct.

**Mock 41.** An engineer with the Viewer role must find out whether an eventstream's Eventhouse destination is failing to convert events to the output schema, and read the error-level logs. Where?
- **A.** The workspace monitoring database
- **B.** The destination node's Data insights tab, Deserialization errors
- **C.** The eventstream's IncomingMessages metric
- **D.** The destination node's Data insights tab, Data conversion errors, then the Runtime logs tab

> **Answer: D.** Data conversion errors is the output-side metric; Runtime logs give error detail; a Viewer can see both. You answered D: correct.

**Mock 42.** What does a user need in order to deploy content to a deployment pipeline stage that already has content?
- **A.** Pipeline admin only
- **B.** Pipeline admin, plus at least Contributor in both the source and target workspaces
- **C.** Admin in both workspaces
- **D.** Pipeline admin, plus Viewer in the target workspace

> **Answer: B.** Pipeline admin plus at least Contributor in both workspaces. You answered B: correct.

**Mock 43.** What does a user need in order to create a OneLake shortcut?
- **A.** Write on the item where the shortcut is created, and Read on the target
- **B.** Read on the item where the shortcut is created, and Write on the target
- **C.** Write on both
- **D.** The Admin role in both workspaces

> **Answer: A.** Write where the shortcut is created, Read on the target. You answered A: correct.

**Mock 44.** Environments set their own driver and executor sizes, but every notebook runs with the default pool's configuration. Which setting fixes this?
- **A.** Reserve maximum cores for active Spark jobs
- **B.** High concurrency mode for notebooks
- **C.** Customize compute configurations for items
- **D.** Customized workspace pools

> **Answer: C.** Customize compute configurations for items lets an environment set driver and executor size. You answered C: correct.

**Mock 45.** A lakehouse has OneLake security enabled, and its `DefaultReader` role is deleted. Who keeps data access?
- **A.** Users with the ReadAll item permission
- **B.** Workspace Admins, Members and Contributors
- **C.** Everyone who had access before
- **D.** No one

> **Answer: B.** ReadAll users lose access; Admins, Members and Contributors keep it through their Write permission. You answered D: **missed.**

