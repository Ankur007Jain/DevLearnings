# DP-700 Mock 3 — 45 questions (final mock)

**Rules**
- 100 minutes total. No notes, no docs.
- The question order mixes the three domains, like the exam. The part breaks are only pacing checkpoints (about 33 minutes each).
- There are three answer formats:
  - **One best answer:** one letter, for example `3 B`.
  - **Choose two:** both letters, for example `6 A,C`. Both must be right to score.
  - **Yes/No statements:** three answers in order, for example `12 Y,N,Y`. All three must be right to score.
- Send your answers by number in chat. I grade only after question 45 is answered.
- All companies and scenarios are fictional. Every fact was checked against Microsoft Learn pages opened on Nov 16, 2026.

---

# PART 1 (Q1–Q15)

## Case study: Lakemont Energy (Q1–Q6)

**Overview.** Lakemont Energy is a regional electricity utility. It is moving billing and smart-meter analytics to Microsoft Fabric.

**Existing environment**
- One F64 capacity. Workspaces LM-Dev, LM-Test and LM-Prod are the three stages of one deployment pipeline.
- **BillingDB** is an Azure SQL Database (a writable primary, with a system-assigned managed identity on the server). Change data capture (CDC) is enabled on it. CDC was set up for a legacy integration that was retired last month, and nothing reads the change tables any more.
- **es-meters** is an eventstream in LM-Prod. Its sources are Azure Event Hubs (meter events) and, since last week, an Azure SQL Database CDC source for the MeterRegistry table. Its destinations are lakehouse **MeterLake** (tables `meter_events` and `meter_registry`) and an Eventhouse.
- **BillingDW** is a warehouse in LM-Prod. Pipeline `pl-billing` loads it every night with a Copy activity that has Enable staging turned on with Workspace staging. The load volume has doubled this quarter.
- **MeterLake** has OneLake security enabled. Field analysts have no workspace role. The lakehouse was shared with them with "Read all Apache Spark" selected. A month ago a role named FieldUsage was created that grants them Read on `Tables/usage_daily` only.
- Call-center agents have no workspace role. BillingDW is shared with them with no additional permissions.

**Business requirements**
- **BR1.** BillingDB tables must be available in OneLake in near real time, with no ETL to build or maintain, and the replication itself must not consume capacity units.
- **BR2.** Operations must be alerted when a meter reports more than 3 voltage-sag events within any 10-minute period. A result is wanted only when a meter's count changes, not on a fixed schedule.
- **BR3.** Call-center agents query BillingDW with T-SQL. They may see only customers in their own region. Any query of theirs that references the NationalId column must fail. They may see only the last four digits of AccountNumber.

**Technical requirements**
- **TR1.** Field analysts must be able to read only `usage_daily`, from Spark notebooks.
- **TR2.** Use least privilege and the least administrative effort.

**Known issues**
- **KI1.** Field analysts can read every table in MeterLake from their notebooks.
- **KI2.** When es-meters was published with the new CDC source, part of the MeterRegistry initial snapshot never reached `meter_registry`. The source and the destination show Active and report no errors.
- **KI3.** The `pl-billing` Copy activity has failed on the last four nights, each time about 60 minutes after it started. Before the volume grew, it finished in about 40 minutes. Other, shorter copies in the same pipeline succeed.

**Q1.** You need to meet BR1. What should you do first?
- A. Create the mirrored database for BillingDB now. Mirroring reuses the existing CDC capture.
- B. Create a Copy job with CDC-based incremental copy and the Merge method, scheduled every 5 minutes.
- C. Disable CDC on BillingDB, and then create a mirrored Azure SQL Database.
- D. Create a OneLake shortcut to BillingDB in MeterLake.

**Q2.** What explains KI1, and what fixes it while meeting TR1 and TR2?
- A. The analysts hold ReadAll, so they are members of the DefaultReader role, and access from several roles is combined as a union. Delete the DefaultReader role (or narrow what it covers) and keep the analysts in FieldUsage.
- B. OneLake security roles are enforced only at the SQL analytics endpoint. Switch the endpoint to User's identity mode.
- C. Roles apply only to users who have a workspace role. Add the analysts as workspace Viewers.
- D. Role changes can take about an hour to apply. Wait and test again.

**Q3.** What should you do to resolve KI3?
- A. Set the Copy activity Timeout to 7.00:00:00 and Retry to 3.
- B. Give the pipeline's last modified user the workspace Admin role.
- C. Turn on fault tolerance so that incompatible rows are skipped.
- D. Change staging from Workspace to an external Azure Blob Storage or ADLS Gen2 staging connection.

**Q4.** Which combination implements BR3 for the call-center agents?

| | Only own-region rows | Queries on NationalId fail | Last four digits of AccountNumber |
| --- | --- | --- | --- |
| A | Row-level security | Dynamic data masking with `default()` | Column-level security |
| B | Row-level security | Column-level security | Dynamic data masking with `partial()` |
| C | Column-level security | `DENY SELECT` on the table | Dynamic data masking with `partial()` |
| D | Dynamic data masking with `random()` | Column-level security | Row-level security |

**Q5.** Which window type meets BR2?
- A. Tumbling window, 10 minutes
- B. Hopping window, size 10 minutes, hop 5 minutes
- C. Sliding window, 10 minutes
- D. Session window, timeout 10 minutes

**Q6.** A second CDC source will be added to es-meters next week. Which two actions prevent a repeat of KI2? Each correct answer presents part of the solution. **(Choose two.)**
- A. Raise the eventstream's throughput level to High before you publish.
- B. Clear **Activate ingestion** on the lakehouse destination before you publish.
- C. After publishing, resume the destination with the **Now** option.
- D. Insert a derived stream between the source and the lakehouse destination.
- E. After publishing, activate the destination manually and use **Custom time** with a timestamp earlier than the start of the snapshot.

## Standalone questions (Q7–Q15)

**Q7.** Three people need access to workspace Retail-Prod:
- Mia must create, edit and run notebooks and pipelines. She must not be able to add users to the workspace.
- Noor must add users to the workspace as Contributors or Viewers and allow others to reshare items. She must not be able to delete the workspace or add admins.
- Omar, an external auditor, must query all tables of one warehouse, SalesDW, with T-SQL. He must not see any other item in the workspace.

Which assignment follows least privilege?
- A. Mia: Member. Noor: Admin. Omar: workspace Viewer.
- B. Mia: Contributor. Noor: Member. Omar: workspace Viewer.
- C. Mia: Contributor. Noor: Admin. Omar: SalesDW shared with "Read all data using Apache Spark".
- D. Mia: Contributor. Noor: Member. Omar: SalesDW shared with "Read all data using SQL".

**Q8.** Table dbo.Policies in an Azure SQL Database has a primary key and a LastModified datetime column. Rows are updated in place and are sometimes hard-deleted. CDC is enabled on the table. A lakehouse table must always match the current state of the source: one row per policy, and deleted policies must disappear. You use a Copy job. Which configuration meets the requirements?
- A. Incremental copy on the LastModified watermark column with the default Append method
- B. CDC-based incremental copy with the Merge method
- C. Incremental copy on the LastModified watermark column with the Merge method
- D. CDC-based incremental copy with the SCD Type 2 method

**Q9.** An operations team wants two notifications from the Monitor hub:
1. An email when the scheduled nightly run of pipeline pl-load fails.
2. A notification whenever a run of notebook nb-score succeeds.

Workspace monitoring isn't enabled in the workspace. Which statement is correct?
- A. Need 1 is covered by the free schedule-failure email. Need 2 requires an Activator-based alert rule, which is paid and needs workspace monitoring to be enabled first.
- B. The free schedule-failure emails cover both needs.
- C. Both needs require Activator-based alert rules, because failure emails are sent only for manual runs.
- D. Need 2 is met by adding the team as recipients of the notebook's failure notifications.

**Q10.** Supplier price files (.csv) arrive at unpredictable times in an Azure Blob Storage container. Pipeline pl-prices must start as soon as a file lands in the `incoming` folder, and its Copy activity must read exactly the file that raised the event. The file-name expression must not break manual test runs from the canvas, where no trigger values exist. Which two actions should you perform? Each correct answer presents part of the solution. **(Choose two.)**
- A. Add a trigger to pl-prices on Azure Blob Storage events, and filter on the Subject field for the folder and file type.
- B. Add 20 schedules to pl-prices, and begin the pipeline with a Get Metadata activity that looks for new files.
- C. Read the file name with `@triggerBody().fileName`.
- D. Read the file name with `@pipeline()?.TriggerEvent?.FileName`.
- E. Read the file name with `@pipeline().TriggerEvent.FileName`.

**Q11.** In a KQL database, table Readings has many rows per DeviceId, and table Devices has one row per DeviceId. An analyst runs:

```kusto
Readings
| where Timestamp > ago(1h)
| join (Devices) on DeviceId
| summarize Events = count() by Site
```

The counts are far too low. Each device contributes only one reading. What is the cause, and what is the fix?
- A. `on DeviceId` matches only the first row of each table. Use `on $left.DeviceId == $right.DeviceId`.
- B. `summarize` must run before the join.
- C. Without `kind`, join uses innerunique, which deduplicates the left table on the join key. Add `kind=inner`.
- D. The time filter must be applied after the join.

**Q12.** Two stored procedures run at the same time in a Fabric Warehouse. One runs UPDATE on rows of dbo.FactSales for store 10. The other runs DELETE on rows of dbo.FactSales for store 20. One of them fails with error 24556. For each statement, answer Yes or No. **(Yes/No ×3)**
1. Adding `SET TRANSACTION ISOLATION LEVEL READ COMMITTED` to both procedures prevents the error.
2. The transactions conflicted even though they changed different rows, because write-write conflicts are evaluated at the table level.
3. The transaction that committed first succeeded. The other was rolled back and should be retried, ideally with exponential backoff.

**Q13.** A Fabric admin creates a Finance domain and names Ana as its domain admin. For each statement, answer Yes or No. **(Yes/No ×3)**
1. Ana can rename the Finance domain and add a second domain admin.
2. Ana can specify her own certification reviewers for the Finance domain by overriding the delegated tenant setting.
3. The Fabric admin makes Finance the default domain for a security group. A workspace that a member of the group administers, and that is already assigned to the Sales domain, moves to Finance.

**Q14.** A Dataflow Gen2 has five queries that load fact tables into a lakehouse with incremental refresh. Each query is set to extract data from the past 3 years with a bucket size of one month. The destinations use Replace with a fixed schema. The configuration breaks one documented limit. Which limit, and which change fixes it while keeping all three years under incremental refresh?
- A. Each query exceeds the limit of 50 buckets. Change the bucket size to quarter.
- B. Incremental refresh requires the Append update method. Change Replace to Append.
- C. Incremental refresh requires a dynamic schema. Change fixed to dynamic.
- D. The dataflow exceeds the limit of 150 buckets in total (5 × 36 = 180). Change the bucket size to quarter (5 × 12 = 60), or move two of the queries to a second dataflow.

**Q15.** A Fabric Warehouse named EDW serves Power BI reports in Direct Lake mode. It also takes heavy nightly loads into staging tables that are read once and then truncated. An engineer proposes to disable V-Order on EDW to speed up the loads, and to enable it again if reports slow down. What do you recommend?
- A. Reject it for EDW. Disabling V-Order is done for the whole warehouse and can't be undone. Move the staging tables to a separate staging warehouse and disable V-Order only there.
- B. Approve it. V-Order can be turned back on at any time.
- C. Disable V-Order only for the staging tables inside EDW.
- D. Approve it, and run OPTIMIZE on the reporting tables each morning to re-apply V-Order.

---

# PART 2 (Q16–Q30)

**Q16.** A regulator's analyst must query two views, rpt.vw_Outages and rpt.vw_Reliability, in warehouse OpsDW. She has no workspace role. She must not be able to read any other table or view in the warehouse, including objects created later. Which approach meets the requirements with least privilege?
- A. Share OpsDW with "Read all data using SQL", and then DENY SELECT on every other object.
- B. Add her as a workspace Viewer, and create row-level security policies on the other tables.
- C. Share OpsDW with no additional permissions, and then GRANT SELECT on the two views to her.
- D. Run CREATE USER for her in OpsDW and GRANT SELECT on the two views. Don't share the item.

**Q17.** An ADLS Gen2 account holds a Delta table in a folder. In lakehouse LH1, an engineer tries to create a shortcut to it named `sales 2026` under `Tables/archive/`. Analysts must be able to query the data through the SQL analytics endpoint without copying it. What must the engineer do so that the data appears as a table?
- A. Create the shortcut under `Files/archive/` with the same name.
- B. Create the shortcut at the top level of the Tables folder, with a name that has no spaces, such as `sales_2026`.
- C. Create the shortcut at the top level of the Tables folder and keep the name `sales 2026`.
- D. Keep the shortcut under `Tables/archive/` and turn on shortcut caching in the workspace's OneLake settings.

**Q18.** A notebook begins with `%pip install` of a parsing library and works when it is run interactively. When the same notebook runs from a pipeline's Notebook activity, the library isn't installed. The team needs the approach that Microsoft recommends for pipelines, with the same library versions on every run. What should you do?
- A. Replace `%pip install` with `!pip install`.
- B. Add the boolean parameter `_inlineInstallationEnabled` = True to the Notebook activity.
- C. Enable high concurrency mode for the pipeline's notebooks.
- D. Add the library to an environment, publish the environment, and attach it to the notebook.

**Q19.** A pipeline has two Lookup activities, both with **First row only** selected. `LookupOld` returns the column `WatermarkValue` from a control table. `LookupNew` returns `NewWatermarkValue`, the MAX(LastModifytime) of the source table. Which Copy activity source query returns only the rows changed between the two watermarks?

A.
```
select * from dbo.Orders
where LastModifytime > '@activity('LookupOld').output.firstRow.WatermarkValue'
  and LastModifytime <= '@activity('LookupNew').output.firstRow.NewWatermarkValue'
```
B.
```
select * from dbo.Orders
where LastModifytime > '@{activity('LookupOld').output.firstRow.WatermarkValue}'
  and LastModifytime <= '@{activity('LookupNew').output.firstRow.NewWatermarkValue}'
```
C.
```
select * from dbo.Orders
where LastModifytime > '@{activity('LookupOld').output.value.WatermarkValue}'
  and LastModifytime <= '@{activity('LookupNew').output.value.NewWatermarkValue}'
```
D.
```
select * from dbo.Orders
where LastModifytime > '@@{activity('LookupOld').output.firstRow.WatermarkValue}'
  and LastModifytime <= '@@{activity('LookupNew').output.firstRow.NewWatermarkValue}'
```

**Q20.** An eventstream delivers events at least once, so Eventhouse table Events holds duplicate rows that share an EventId. Dashboards must read a deduplicated set that stays up to date, includes the 400 million rows already in the table, and doesn't pay the deduplication cost in every query. Which command do you run?

A.
```kusto
.create async materialized-view with (backfill=true) DedupEvents on table Events
{ Events | summarize take_any(*) by EventId }
```
B.
```kusto
.create materialized-view DedupEvents on table Events
{ Events | summarize take_any(*) by EventId }
```
C.
```kusto
.create materialized-view with (backfill=true) DedupEvents on table Events
{ Events | summarize take_any(*) by EventId }
```
D.
```kusto
.create function DedupEvents()
{ Events | summarize arg_max(Timestamp, *) by EventId }
```

**Q21.** An eventstream has an Azure Event Hubs source (16 partitions), a custom endpoint source, a Lakehouse destination, and an Eventhouse destination in Direct ingestion mode. Event throughput is set to Low, and traffic has grown to about 40 MB/s. You must move to the lowest throughput level that fits. These steps are available:

1. Deactivate the Azure Event Hubs source and the Lakehouse destination.
2. Deactivate the custom endpoint source and the Eventhouse destination.
3. Set Event throughput to Medium.
4. Set Event throughput to High.
5. Reactivate the nodes that you deactivated.

Which sequence is correct?
- A. 2, 4, 5
- B. 3, 5
- C. 1, 3, 5
- D. 1, 2, 3, 5

**Q22.** A tenant uses fully automated downstream inheritance of sensitivity labels. In one workspace, lakehouse LH1 (a Fabric item) feeds semantic model SM1, which feeds report R1 (both Power BI items). Treat each statement separately, starting with no labels on any item. For each statement, answer Yes or No. **(Yes/No ×3)**
1. You apply Confidential to LH1. SM1 inherits Confidential.
2. R1's owner applied General to R1 manually. You then apply Highly Confidential to SM1. R1 keeps General.
3. You apply Highly Confidential to SM1. LH1 becomes Highly Confidential.

**Q23.** An eventstream ingests smart-meter telemetry into Eventhouse table MeterReadings for KQL dashboards. Data scientists need the same table as Delta in OneLake for Spark notebooks, no more than about 10 minutes behind. There must be only one ingestion path and no second paid copy of the data. What should you do?
- A. Add a Lakehouse destination to the eventstream.
- B. Turn on OneLake availability for the table and keep the default settings.
- C. Create a OneLake shortcut in the KQL database that points to a lakehouse table.
- D. Turn on OneLake availability for the table, and set `TargetLatencyInMinutes` in the table's mirroring policy to a value between 5 and 10.

**Q24.** Raw JSON lands in Eventhouse table Raw. An update policy on table Clean (Source = Raw, IsTransactional = false) parses it. Since yesterday's change to the parsing function, ingestion into Raw reports success and Raw keeps growing, but Clean has received no new rows. You must confirm the cause from inside the KQL database and make sure a failing policy can't pass silently again. Which two actions should you perform? **(Choose two.)**
- A. Set the soft-delete period of Raw to 0 seconds.
- B. Run `.show table Clean policy update`, and change Source to `Clean`.
- C. Run `.show ingestion failures | where OriginatesFromUpdatePolicy == true`.
- D. Replace the update policy with a materialized view over Raw.
- E. Set IsTransactional to true in the update policy.

**Q25.** A deployment pipeline has Dev, Test and Prod stages. After the first deployment from Dev to Test, notebook nb_load in Test still has the Dev lakehouse as its default lakehouse, and the Import semantic model Sales in Test still connects to the Dev Azure SQL server. Which two actions correct this for the next deployments? Each correct answer presents part of the solution. **(Choose two.)**
- A. In the Test stage, the notebook's owner creates a default lakehouse rule for nb_load.
- B. In the Dev stage, create the rules so that they are deployed to Test with the content.
- C. In the Test stage, the semantic model's owner creates a data source rule for Sales.
- D. In the Test stage, create a parameter rule for nb_load.
- E. Unassign the Test workspace from its stage, and assign it again.

**Q26.** You design surrogate keys for dimension tables in a Fabric Warehouse by using IDENTITY columns. For each statement, answer Yes or No. **(Yes/No ×3)**
1. Keys generated by IDENTITY are unique, but they can have gaps and are not guaranteed to be sequential.
2. To save space, the surrogate key column can be declared as `int IDENTITY`.
3. An IDENTITY column can be added to an existing dimension table with ALTER TABLE.

**Q27.** A Direct Lake semantic model reads six gold Delta tables. A pipeline rewrites the tables every night in a job that takes 40 minutes. While the job runs, reports show a mix of old and new data. Reports must switch to the new data only after all six tables are complete, and the outcome of the model refresh must be visible in the pipeline run. What should you do?
- A. Turn off **Keep your Direct Lake data up to date** for the model, and add a Semantic model refresh activity as the last step of the pipeline.
- B. Leave the setting on, and add a Wait activity at the end of the pipeline.
- C. Change the model to Import mode and schedule eight refreshes a day.
- D. Turn off the setting, and let queries fall back to DirectQuery while the job runs.

**Q28.** A team runs Apache Airflow jobs in a production workspace that still uses the default Apache Airflow runtime setting. The first DAG of the night often starts late, because the Airflow environment has shut down after inactivity and needs up to 5 minutes to resume. The team also wants to run more DAGs at the same time. Which change do you recommend?
- A. Keep the Starter pool. It stays warm for as long as the capacity is running.
- B. Keep the Starter pool and enable autoscale on it.
- C. In Workspace settings, under Data Factory, open Apache Airflow runtime settings, create a custom pool, and add extra nodes.
- D. Create a custom Spark pool with autoscale under Data Engineering/Science, and run the DAGs on it.

**Q29.** Operations staff with no Spark or KQL skills must build a solution in a visual editor. Events arrive from Azure Event Hubs. For each device, they need one row per 5-minute interval with the average temperature, stored in an Eventhouse table. Which solution meets the requirements?
- A. An eventstream with an Aggregate operator (average over 5 minutes) and an Eventhouse destination in Direct ingestion mode
- B. An eventstream with a Group by operator (5-minute tumbling window, grouped by device) and an Eventhouse destination in Event processing before ingestion mode
- C. A Spark structured streaming job that groups by `window("event_time", "5 minutes")`
- D. An eventstream with Direct ingestion into the Eventhouse, and a materialized view that summarizes by `bin(Timestamp, 5m)`

**Q30.** A team sets `spark.ms.autotune.enabled = true` in an environment to speed up a recurring Spark SQL job. The environment uses Runtime 1.3, and the job's notebooks run in high concurrency mode. After 30 runs, nothing has been tuned. Which statement explains this?
- A. Autotune needs at least 50 runs of a query before it changes anything.
- B. Autotune only adjusts executor memory and cores, which the pool fixes.
- C. Autotune must be turned on for the capacity by a Fabric admin. The environment property has no effect.
- D. Autotune is compatible with Runtime 1.2 only, and it doesn't run in high concurrency mode.

---

# PART 3 (Q31–Q45)

**Q31.** Workspace Shared-Dev is connected to the main branch of an Azure DevOps repository. Branch policy on main doesn't allow direct commits. Priya has the Contributor role in Shared-Dev with write permission on all items, and she may create branches in the repository. The workspace setting "Allow users with at least Contributor role to change Git branch" is off. She must build a new notebook without changing what other developers see in Shared-Dev, and deliver it to main through a pull request. What should she do?
- A. Use **Branch out** to a new workspace, develop there, commit to the new branch, and open a pull request to main.
- B. Use **Switch branch** in Shared-Dev to point the workspace at a new feature branch.
- C. Commit from Shared-Dev directly to main, and ask a workspace Admin to approve it.
- D. Disconnect Shared-Dev from Git, make the change, and connect it again.

**Q32.** A warehouse query must return total sales for each (Region, Territory) pair, a subtotal for each Region, and one grand total. It must not return a total for each Territory across regions. Which clause do you use?
- A. `GROUP BY CUBE (Region, Territory)`
- B. `GROUP BY GROUPING SETS ((Region), (Territory), ())`
- C. `GROUP BY ROLLUP (Region, Territory)`
- D. `GROUP BY Region, Territory`

**Q33.** A workspace was created last month. Spark notebooks load bronze and silver tables all day and write large gold Delta tables once a night. A Direct Lake semantic model reads the gold tables, and its queries are slower than expected. No Spark or table settings have been changed since the workspace was created. You must improve read performance for the existing gold data and for future gold writes, without adding write overhead to the bronze and silver jobs. Which two actions should you perform? Each correct answer presents part of the solution. **(Choose two.)**
- A. Set `spark.sql.parquet.vorder.default` to true in the workspace's default environment.
- B. Set the table property `delta.parquet.vorder.enabled` to true on the gold tables.
- C. Run VACUUM on the gold tables with the default retention.
- D. Run table maintenance (OPTIMIZE) with **Apply V-order** on the gold tables.
- E. Set the resource profile of the gold notebooks to `writeHeavy`.

**Q34.** A data steward has the Contributor role in a workspace and write permission on its items. Certification and master data endorsement are enabled in the tenant, but the steward is not among the users who may certify items or label master data. Which two actions can the steward perform? **(Choose two.)**
- A. Promote a notebook.
- B. Certify a semantic model.
- C. Promote a Power BI dashboard.
- D. Label a lakehouse as master data.
- E. Request certification of a lakehouse.

**Q35.** A metadata-driven pipeline uses a Lookup activity to read a control table that has 7,200 rows, one per source table. A ForEach activity then runs a parameterized Copy activity for each row. Every run succeeds without errors, but only 5,000 tables are loaded. What is the cause, and what should you change?
- A. ForEach can iterate over at most 5,000 items. Raise Batch count to 50.
- B. The Lookup output exceeded 4 MB. Select First row only.
- C. A pipeline can hold at most 120 activities. Move the Copy activity into a child pipeline.
- D. A Lookup activity returns at most 5,000 rows, and it returns only the first 5,000 without failing. Read the control table in ranges of at most 5,000 rows, for example from an outer pipeline that calls the loading pipeline once per range.

**Q36.** A Dataflow Gen2 loads a query into a new lakehouse table. The source column Discount contains nulls. The refresh fails with:

```
MashupException.Error: DataFormat.Error: Error in replacing table's content with new data in a version: #{0}.,
InnerException: We can't insert null data into a non-nullable column.
```

What is the documented fix?
- A. Change the update method from Replace to Append.
- B. Delete the table from the destination, remove the data destination from the dataflow, set the affected columns to nullable types with `Table.TransformColumnTypes` (for example `type nullable Int64.Type`), and then add the destination again.
- C. Turn on staging for the query.
- D. Change the schema option to dynamic, so that the column becomes nullable on the next refresh.

**Q37.** A workspace admin reviews the Spark settings of a workspace. For each statement, answer Yes or No. **(Yes/No ×3)**
1. **Set maximum job lifetime** can cancel a notebook run that a pipeline started, but it doesn't cancel lakehouse table maintenance jobs such as OPTIMIZE and VACUUM.
2. Turning on **Reserve maximum cores for active Spark jobs** enables optimistic job admission.
3. With the default setting, an idle interactive notebook session expires after 20 minutes.

**Q38.** A Spark structured streaming query counts events in 5-minute tumbling windows with `.withWatermark("event_time", "10 minutes")` and appends the results to a Delta table. The source stops sending events every Friday at 18:00. The window that ends at 18:00 is missing from the table until Monday morning, a few minutes after events resume. No errors are logged. What explains this?
- A. A watermark advances only when Spark processes new input, so the last windows can't be finalized until a later micro-batch receives data.
- B. The checkpoint was lost over the weekend, so Spark rebuilt the window on Monday.
- C. Optimize Write holds back the last files until enough data has accumulated.
- D. Data older than the watermark is always dropped, so the window was discarded and then recomputed.

**Q39.** A pipeline's ForEach activity loads 600 small tables from an Azure SQL Database, running one Copy activity per table. **Sequential** is selected, and a run takes 5 hours. The source database can serve about 30 concurrent queries without affecting its users. The run must finish as fast as possible without going over that number. What should you change?
- A. Clear Sequential and leave Batch count empty, so that all 600 items run at once.
- B. Clear Sequential and set Batch count to 100.
- C. Clear Sequential and set Batch count to 30.
- D. Keep Sequential, and set intelligent throughput optimization on the Copy activity to Maximum.

**Q40.** Warehouses SalesDW and MarketingDW are in the same workspace, and each has its own SQL database project in VS Code. A view in the Sales project joins a table in the other warehouse by the hard-coded name `MarketingDW.dbo.CustomerEngagement`. The Sales project fails to build with SQL71501 unresolved reference errors. The same project must deploy to Dev, Test and Prod, where the Marketing warehouse has a different name in each environment. What should you do?
- A. Copy the CREATE TABLE script of CustomerEngagement into the Sales project.
- B. In the Sales project, add a database reference to the Marketing project (or its .dacpac), and use a SQLCMD variable such as `[$(MarketingWarehouseName)]` for the warehouse name. Build and publish Marketing first.
- C. Add database references in both directions, so that each project references the other.
- D. Keep the hard-coded three-part name and ignore the SQL71501 errors.

**Q41.** Lakehouse SilverLH and warehouse GoldDW are in the same workspace. A SQL-only team must build a wide reporting table that joins SilverLH's Delta table `sales` (900 million rows) to two dimension tables in GoldDW. They want one T-SQL statement that they can keep in a stored procedure, no separate data movement tool, and the least development effort. Where should the table be created, and how?
- A. In SilverLH, with CREATE TABLE AS SELECT run through its SQL analytics endpoint
- B. In GoldDW, with a Dataflow Gen2 that merges the three tables
- C. In SilverLH, with a Spark notebook that reads the GoldDW dimension tables
- D. In GoldDW, with CREATE TABLE AS SELECT that reads `SilverLH.dbo.sales` by its three-part name

**Q42.** Table Logs in a KQL database holds 4 billion rows covering several months. The word timeout always appears as a whole term in the Message column. This query is slow:

```kusto
Logs
| where Message contains "timeout"
| where Timestamp > ago(1d)
| summarize count() by ServiceId
```

Which two changes follow the documented KQL best practices and keep the result the same? **(Choose two.)**
- A. Add `| extend Msg = tolower(Message)` and filter on `Msg` instead of `Message`.
- B. Move the `summarize` line above both `where` lines.
- C. Move `where Timestamp > ago(1d)` to directly after `Logs`.
- D. Replace `contains "timeout"` with `has "timeout"`.
- E. Replace `summarize count() by ServiceId` with `distinct ServiceId`.

**Q43.** Security analysts must investigate who read or wrote which OneLake files in workspace Ops-WS, including access through APIs and access from other workspaces through shortcuts. The events must be stored as files that the team can query with Spark, and it must be possible to protect them from tampering for a retention period. A workspace admin who has no tenant-level admin role must be able to set this up. What should you configure?
- A. In Workspace settings, on the OneLake tab, turn on **Add diagnostic events to a lakehouse**, choose a lakehouse in the same capacity, and make the diagnostic events immutable.
- B. Search the audit logs in the Microsoft Purview portal.
- C. Enable workspace monitoring and query the monitoring Eventhouse.
- D. Turn on shortcut caching on the OneLake tab with a 28-day retention period.

**Q44.** A team must build two processes.
- **Process X:** every night on a schedule, copy tables from an on-premises SQL Server through the on-premises data gateway, run a warehouse stored procedure, refresh a semantic model, and email the team if the scheduled run fails.
- **Process Y:** run 24 transformation notebooks as one dependency graph that is defined in code, with per-notebook retries and a concurrency limit, sharing the compute of a single Spark session.

Which tools should the team use?
- A. X: an orchestrator notebook. Y: a pipeline with a ForEach activity.
- B. X: a pipeline. Y: an orchestrator notebook that calls `notebookutils.notebook.run` in a loop.
- C. X: a pipeline. Y: an orchestrator notebook that calls `notebookutils.notebook.runMultiple` with a DAG.
- D. X: a Spark job definition. Y: an orchestrator notebook that calls `notebookutils.notebook.runMultiple` with a DAG.

**Q45.** Match each need to the monitoring surface that Microsoft documents for it.
- **Need 1:** Query pipeline and activity-level execution logs with KQL, together with the logs of other items in the workspace.
- **Need 2:** Starting from a failed Notebook activity in a pipeline run, open the Spark application's execution details, the snapshot of the notebook as it ran, and the Spark logs.
- **Need 3:** Browse, in one place, the Spark applications that are in progress across items, whether they were started from notebooks, Spark job definitions or pipelines.

Which option is correct?
- A. 1: Monitor hub. 2: Capacity Metrics app. 3: Workspace monitoring.
- B. 1: Workspace monitoring. 2: The deep link on the Notebook activity in the pipeline run. 3: Monitor hub.
- C. 1: Capacity Metrics app. 2: The notebook's Recent runs. 3: The notebook's cell-level monitoring.
- D. 1: Workspace monitoring. 2: Monitor hub export. 3: The notebook's Recent runs.
