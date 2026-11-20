# DP-700 Reading Pack

Facts checked against Microsoft Learn between Oct 11 and Nov 16, 2026. Practice material written from public documentation, not real exam content.

## How to use this pack

The DP-700 exam uses the skills outline dated **October 19, 2026** (check the official study guide for newer changes). This pack covers every bullet in that outline, grouped under the three exam domains. Part numbers are fixed labels that the Update log and the Part 14 table refer to, so they are not sequential inside a domain. Every fact comes from a Microsoft Learn page opened between Oct 11 and Nov 16, 2026, and each part links its sources.

| Item | Detail |
|---|---|
| Exam | DP-700: Implementing Data Engineering Solutions Using Microsoft Fabric |
| Skills outline | As of October 19, 2026 ([official study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700)) |
| Pass score | 700 |
| Domains | Implement and manage an analytics solution (30–35%), Ingest and transform data (30–35%), Monitor and optimize an analytics solution (30–35%) |
| Oct 19 change log | "Configure Microsoft Fabric workspace settings" and "Optimize performance" are marked Minor; everything else is marked No change |
| Preview features | Most questions cover GA features; preview features can appear if they are commonly used |

**Reading order.** Work one domain at a time. Domain 1: Parts 2, 7, 8, 9. Domain 2: Parts 1, 3, 4, 5, 6. Domain 3: Parts 10, 11, 12. Parts 13 and 14 (common traps), the labs and the accuracy notes follow as reference and practice.

| Part | Topic | Exam domain |
|---|---|---|
| 2 | Workspace settings: Spark, domains, OneLake, Airflow | Implement and manage |
| 7 | Orchestration: tool choice, schedules, triggers, parameters | Implement and manage |
| 8 | Security and governance | Implement and manage |
| 9 | Lifecycle management: Git, database projects, deployment pipelines | Implement and manage |
| 1 | Foundations: OneLake and choosing a data store | Ingest and transform |
| 3 | Batch ingestion: shortcuts, mirroring, pipelines, Copy job, Dataflow Gen2, warehouse loading | Ingest and transform |
| 4 | Loading patterns: full and incremental, dimensional model, data quality | Ingest and transform |
| 5 | Batch transformation: choosing the tool, denormalize, aggregate | Ingest and transform |
| 6 | Streaming: Eventstream, windowing, Spark structured streaming, Eventhouse and KQL | Ingest and transform |
| 10 | Monitoring and alerts | Monitor and optimize |
| 11 | Identify and resolve errors | Monitor and optimize |
| 12 | Optimize performance | Monitor and optimize |

After each part, run the matching lab in **Hands-on tutorials** near the end. The labs stay in build order (Part 1 to Part 12) because later labs extend earlier ones. The **Accuracy notes** section lists claims often found in older notes and blog posts that current docs contradict.

**Update log (oldest first).** Each row says which parts changed. Facts added from practice questions were checked against Microsoft Learn first.

| Date | Where | What changed |
|---|---|---|
| Nov 6, 2026 | Parts 8, 11, 12, 14 | Added the item-permissions table (Part 8), a Copy activity error table (Part 11), a flag on two Learn pages that disagree about the activity timeout (Parts 11 and 12), and the first traps (Part 14). |
| Nov 6, 2026 | Study guide check | The study guide page showed "last updated 2026-10-30" with no change notes. The Oct 19 outline mapping in this pack has not been re-diffed against it. |
| Nov 6, 2026 | Parts 8, 14 | Added a table of where sensitivity labels carry and where they don't. |
| Nov 6, 2026 | Parts 11, 14 | Added a table of Spark and notebook capacity and permission errors (HTTP 430, 429, ReadAll, 403, Capacity Not Active). |
| Nov 7, 2026 | Parts 10, 14 | Added the Monitor hub job alerts comparison (free failure emails vs paid Activator rules). |
| Nov 12, 2026 | Whole pack | Regrouped the chapters under the three exam domains. Part numbers are unchanged, so they are not sequential inside a domain. |
| Nov 12, 2026 | Parts 3, 6, 14 | Added Dataflow Gen2 incremental refresh (Part 3) and the SQL operator's event-time rule and limits (Part 6). |
| Nov 12, 2026 | Part 14 | Added a reading section on code patterns (window syntax per engine, Spark deduplication, COPY INTO). |
| Nov 13, 2026 | Parts 12, 14 | Added optimization rules (eventstream throughput, autotune, warehouse V-Order and cold start, copy parallelism). |
| Nov 13, 2026 | Part 14 | Added traps on labels, masking, roles and two workspace-setting names. |
| Nov 15, 2026 | Part 14 | Added traps on column-level security, DefaultReader, deployment rules and endorsement. |
| Nov 15, 2026 | Part 14 | Added traps from Mock 1. |
| Nov 15, 2026 | Part 6 | Added a note on why the default streaming trigger creates tiny files. |
| Nov 15, 2026 | Part 6 | Added a note on what "topology" means in the SQL operator rule (new destination nodes). |
| Nov 15, 2026 | Part 3 | Added a compiled summary of Dataflow Gen2 update methods, fixed vs dynamic schema and incremental refresh. |
| Nov 15, 2026 | Part 6 | Added materialized view query by name vs materialized_view() and the max_age option. |
| Nov 15, 2026 | Part 6 | Added why a 0s soft-delete source needs a transactional update policy. |
| Nov 15, 2026 | Part 6 | Clarified that an update policy's source table is the ingestion table, not Event Hubs. |
| Nov 16, 2026 | Part 6 | Added what a structured streaming job is, the Spark job definition retry policy and its 90-day lifetime limit. |
| Nov 16, 2026 | Part 13 | Added a restaurant memory picture, Direct Lake on SQL vs on OneLake fallback, and the default semantic model change. |
| Nov 16, 2026 | Part 13 | Added Import mode: data stored on disk in the model, memory is a loading step. |
| Nov 16, 2026 | Part 13 | Added how each semantic model mode stays current: Import refresh options and limits, Direct Lake automatic updates. |
| Nov 16, 2026 | Part 13 | Added how to choose between Direct Lake, Import and DirectQuery. |
| Nov 16, 2026 | Part 7 | Added a full explainer of pipeline expressions: @, @{ } and @@. |
| Nov 20, 2026 | Part 14 | Added traps from Mock 2 and Mock 3, each checked against the linked Microsoft Learn page. |

# Domain 1 — Implement and manage an analytics solution (30–35%)

This domain covers Part 2 (workspace settings), Part 7 (orchestration), Part 8 (security and governance) and Part 9 (lifecycle management).

## Part 2 — Configure workspace settings

Four workspace setting areas are tested: Spark, domains, OneLake and Apache Airflow. Changing Spark settings needs the workspace **Admin** role.

### Spark settings (Workspace settings → Data Engineering/Science → Spark compute)

**Pool tab**

- **Starter pool**: created automatically with each workspace. It uses Medium nodes and sessions usually start in 5–10 seconds. That speed is best-effort, not guaranteed.
- A starter pool falls back to on-demand startup (2–5 minutes) when you pick another node size, customize compute, or the workspace uses Private Links or Managed VNets.
- **Custom Spark pool**: you choose node size, autoscale and dynamic executor allocation. It starts in about 3 minutes. Creating one needs workspace Admin, and the capacity admin's **Customized workspace pools** setting (on by default).
- Single-node pools are allowed: set minimum nodes to 1 and the driver and executor share one node.
- **Customize compute configuration for items**: when on, users can set driver and executor cores and memory per item through an Environment. When off, every environment uses the default pool's settings.

| Node size | vCores | Memory |
|---|---|---|
| Small | 4 | 32 GB |
| Medium | 8 | 64 GB |
| Large | 16 | 128 GB |
| X-Large (non-trial SKUs only) | 32 | 256 GB |
| XX-Large (non-trial SKUs only) | 64 | 512 GB |

- 1 capacity unit = 2 Spark vCores, with a 3× burst. An F64 gives 128 vCores, or 384 with burst.
- Billing covers active session time only, not idle pool time or cluster creation.

**Environment tab**: set a default Environment for the workspace, or pick the Fabric runtime version when no default environment is used.

**Jobs tab**

- Optimistic job admission is on by default. **Reserve maximum cores for active Spark jobs** turns it off.
- **Spark session timeout** for interactive notebook sessions defaults to **20 minutes**.
- **Set maximum job lifetime** cancels user-submitted jobs (notebooks, Spark job definitions, Livy and high concurrency sessions) that run past the limit. System jobs such as table maintenance aren't affected.

**High concurrency tab**

- Lets several notebooks or pipeline notebook activities share one Spark session. Each gets its own REPL core, so variables don't collide.
- Sharing requires the **same user**, the **same default lakehouse** and the **same Spark compute settings**. Otherwise a new session starts.
- Only the notebook or activity that started the session is billed.
- Default: up to **5** notebooks per session. Raise it to up to **50** with `spark.highConcurrency.max` (value 2–50) in the Environment's Spark properties.

### Domain settings

- A domain groups workspaces by business area. Every item in an assigned workspace inherits the domain. Domains don't change who can see or access items.
- **Fabric admin**: creates, renames and deletes domains and names domain admins.
- **Domain admin**: edits the description, assigns workspaces, names contributors and overrides delegated settings. Can't delete or rename the domain or add other admins.
- **Domain contributor**: a workspace Admin who is allowed to assign their own workspace to the domain from workspace settings.
- Subdomains have no admins of their own; they use the parent domain's admins.
- Delegated settings a domain can override: a default sensitivity label for the domain, and certification settings (on/off, certifiers, documentation URL).
- A default domain can be set for users or groups, so new workspaces they create are assigned to it.

### OneLake settings

- **Shortcut caching** (Workspace settings → OneLake tab): turn the cache on and set retention from **1 to 28 days**. Each access resets the clock. Files over 1 GB aren't cached. **Reset cache** clears it.
- Caching works for GCS, Amazon S3, S3-compatible and on-premises data gateway shortcuts. It does **not** apply to ADLS Gen2 shortcuts.
- **OneLake diagnostics**: streams data-access events as JSON logs into a lakehouse in the same capacity. It needs workspace Admin plus Contributor on the destination lakehouse.

### Apache Airflow settings (Workspace settings → Data Factory → Apache Airflow runtime settings)

| Property | Starter pool (default) | Custom pool |
|---|---|---|
| Size | Large compute node | You set node size (Small or Large), extra nodes and autoscale |
| Startup | Instant | Created in a stopped state |
| Idle behavior | Shuts down after 20 minutes of inactivity | Always on until paused manually |
| Suggested use | Development | Production |

Each extra node adds capacity for 3 more workers. Private networks and VNets aren't supported for Airflow jobs.

Sources: [Workspace admin settings](https://learn.microsoft.com/en-us/fabric/data-engineering/workspace-admin-settings) · [Spark compute](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute) · [High concurrency](https://learn.microsoft.com/en-us/fabric/data-engineering/high-concurrency-overview) · [Domains](https://learn.microsoft.com/en-us/fabric/governance/domains) · [OneLake shortcuts (caching)](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) · [OneLake diagnostics](https://learn.microsoft.com/en-us/fabric/onelake/onelake-diagnostics-overview) · [Airflow workspace settings](https://learn.microsoft.com/en-us/fabric/data-factory/apache-airflow-jobs-workspace-settings)

## Part 7 — Orchestrate processes

Pipelines orchestrate: they schedule, trigger, branch, loop and call notebooks, dataflows, Copy jobs and SQL. Notebooks and Dataflow Gen2 do the transformation work inside them.

### Choose Dataflow Gen2, a pipeline or a notebook

| Need | Choose | Why |
|---|---|---|
| Low-code transformation by Power Query users | Dataflow Gen2 | 300+ transformations in a visual editor |
| Move data at scale, control flow, retries, scheduling, events | Pipeline | Copy activity plus activities such as ForEach, If Condition, Lookup, Notebook, Dataflow, Fail and Invoke pipeline |
| Code-first or complex transformation on large data | Notebook | Spark (PySpark, Spark SQL, Scala, R) |
| Simple full, incremental or CDC copy with no orchestration | Copy job | Built-in state, watermark or CDC, merge or SCD 2 |
| Python-defined DAGs, existing Airflow skills | Apache Airflow job | Managed Airflow in Fabric |

### Schedules and event-based triggers

- A pipeline runs **on demand**, on a **schedule**, or from an **event**.
- A schedule needs a start date **and** an end date (there is no open-ended option), a frequency and a time zone. A pipeline can have **up to 20 schedules**, and each schedule can pass parameter values (typed in, or taken from a variable library).
- **Interval-based schedules (preview)** create fixed, non-overlapping windows and expose the `Window start time` and `Window end time` trigger parameters. You can't edit them (delete and recreate instead), and backfill isn't available yet.
- Failure email notifications can be set for **scheduled** runs, not on-demand runs.
- **Event triggers** react to OneLake file events, Azure Blob Storage events, job events and workspace events. Under the hood they use an Eventstream and an Activator rule, and the trigger is saved as an Activator (Reflex) item. Filter on the event's Subject to match folders or file names.
- Read the triggering file's name with `@pipeline()?.TriggerEvent?.FileName`. The `?` returns null instead of failing during manual test runs.

### Orchestration patterns, parameters and dynamic expressions

- **Pipeline parameters** are set per run; **variables** change during a run (Set variable). Reference them as `@pipeline().parameters.Name` and `@variables('Name')`.
- **Activity outputs**: `@activity('Lookup1').output.firstRow.MaxDate`, `@activity('Copy1').output.rowsCopied`, and on failure `@activity('X').error.message`.
- **Notebook activity**: base parameters overwrite the values in the notebook's parameter cell. The notebook returns a value with `notebookutils.notebook.exit(value)`, and the pipeline reads it as `@activity('Notebook1').output.result.exitValue`.
- **Metadata-driven pattern**: a Lookup reads a control table, ForEach loops over the rows, and each iteration runs a parameterized Copy or Notebook activity.
- **Fail activity**: stops the pipeline with your own error message and code, usually after an If Condition.
- **Notebook-to-notebook**: `notebookutils.notebook.run("name", timeout_seconds, {args}, workspaceId)` runs one notebook. `notebookutils.notebook.runMultiple(...)` runs a list in parallel or a DAG with dependencies **in the same Spark session**, which shares compute and cuts cost. DAG settings include `timeoutInSeconds` (default 43,200 = 12 hours) and `concurrency`. Don't call `notebookutils.notebook.exit()` inside a try/catch block.

**Pipeline expressions: `@`, `@{ }` and `@@`, once and for all.** From [Expressions and functions](https://learn.microsoft.com/en-us/fabric/data-factory/expression-language), opened Nov 16, 2026.

Memory aid: `@` starts code, `@{ }` is a code pocket inside text, `@@` is a real at-sign.

- **Rule.** A value in a pipeline can be a literal or an expression evaluated at runtime. If the value is an expression, Fabric removes the `@` and runs the rest. A literal string that starts with `@` must be escaped as `@@`.
- **`@expr` as the whole value** keeps the type. **`@{expr}` (string interpolation)** always produces a string, even inside a longer text.

| Value (`myNumber` = 42, `myString` = foo) | Result |
|---|---|
| `@pipeline().parameters.myString` | `foo` as a string |
| `@{pipeline().parameters.myString}` | `foo` as a string |
| `@pipeline().parameters.myNumber` | `42` as a **number** |
| `@{pipeline().parameters.myNumber}` | `42` as a **string** |
| `Answer is: @{pipeline().parameters.myNumber}` | the string `Answer is: 42` |
| `@concat('Answer is: ', string(pipeline().parameters.myNumber))` | the string `Answer is: 42` |
| `Answer is: @@{pipeline().parameters.myNumber}` | the literal text `Answer is: @{pipeline().parameters.myNumber}` |
| `@@` | a one-character string, `@` |

- **Common building blocks.** `@pipeline().parameters.Name`; `@variables('Name')`; `@activity('Name').output` and `.output.data` for a previous activity's result; `@item()` for the current element inside ForEach; system values such as `@pipeline().RunId`, `@pipeline().PipelineName` and `@pipeline().TriggerTime` (UTC, ISO 8601).
- **`?` means null-safe.** `@pipeline()?.TriggeredByPipelineName` evaluates to null instead of failing when not applicable. The same idea applies to `@pipeline()?.TriggerEvent?.FileName` in manual test runs.
- **A parameter that holds an object:** to reach a sub-field, use `[]` syntax instead of the dot operator.
- **Dynamic content editor.** It escapes characters when you finish editing, which breaks `\n` and `\t` inside `replace()`. Learn suggests editing in code view or using URL-encode, replace and decode steps instead.
- **Exam traps.** Number vs string: whole-value `@` keeps the number, `@{ }` turns it into text. Literal `@`: `@@`. A text that must show `@{...}` literally: `@@{...}`.
- Learn doesn't define `variables()` on this page beyond an example, and the function reference part of the page wasn't read in full.

```python
DAG = {
  "activities": [
    {"name": "bronze", "path": "nb_bronze", "args": {"date": "2026-10-11"}},
    {"name": "silver", "path": "nb_silver", "dependencies": ["bronze"]}
  ],
  "timeoutInSeconds": 43200,
  "concurrency": 5
}
notebookutils.notebook.runMultiple(DAG)
```

Sources: [Decision guide](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-pipeline-dataflow-spark) · [Run, schedule or trigger a pipeline](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs) · [NotebookUtils run and runMultiple](https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-run) · [Expressions and functions](https://learn.microsoft.com/en-us/fabric/data-factory/expression-language) · [Fail activity](https://learn.microsoft.com/en-us/fabric/data-factory/fail-activity) · [Notebook workflows in pipelines (Fabric blog)](https://blog.fabric.microsoft.com/blog/use-fabric-data-factory-data-pipelines-to-orchestrate-notebook-based-workflows) · [Airflow job concepts](https://learn.microsoft.com/en-us/fabric/data-factory/apache-airflow-jobs-concepts)

## Part 8 — Security and governance

Security is layered. The workspace role gives access to every item in a workspace. An item permission gives access to one item. T-SQL controls and OneLake security narrow what someone can see inside an item. For least privilege on a single item, share that item instead of granting a workspace role.

### Workspace-level access (roles)

| Capability | Admin | Member | Contributor | Viewer |
|---|---|---|---|---|
| Update or delete the workspace; add or remove admins | Yes | — | — | — |
| Connect the workspace to Git; create a workspace identity | Yes | — | — | — |
| Add members or lower roles; let others reshare | Yes | Yes | — | — |
| Create, edit and delete items; run notebooks and pipelines | Yes | Yes | Yes | — |
| Read lakehouse data through Spark, OneLake APIs or Lakehouse explorer (ReadAll) | Yes | Yes | Yes | — |
| Connect to the SQL analytics endpoint and read with T-SQL (ReadData) | Yes | Yes | Yes | Yes |
| View item content and run output | Yes | Yes | Yes | Yes |

Roles can go to users, security groups, Microsoft 365 groups, distribution lists and service principals. Someone in several groups gets the highest role among them.

### Item-level access (sharing)

- Sharing always grants **Read**: find and open the item, and connect to its SQL analytics endpoint.
- Optional extras: **Edit**, **Share** (reshare up to your own permissions), **Read all with SQL analytics endpoint** (ReadData), **Read all with Apache Spark** (ReadAll: Spark, OneLake APIs, Lakehouse explorer), **Build** (semantic models) and **Execute**.
- Link types: People in your organization, People with existing access (grants nothing new) and Specific people (guests included).
- A revoked permission can take up to 2 hours to apply to a user who is already signed in.

**Item permissions at a glance.** From the [OneLake security overview](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security), opened Nov 6, 2026.

| Permission | See item metadata? | See data in SQL? | See data in OneLake? |
|---|---|---|---|
| Write | Yes | Yes | Yes |
| Read | Yes | No | No |
| ReadData | No | Only in Delegated mode | No |
| ReadAll | No | No | Only through the DefaultReader role |

ReadData is not a stand-in for Read. It sees no item metadata, and the page says that, depending on the SQL analytics endpoint mode, users might need SQL permissions or ReadData *in addition to* Read access on the item. A DefaultReader role exists in all lakehouses and gives any user with ReadAll access to the lakehouse data; you can delete or edit it to remove that access. Learn doesn't describe User's identity mode in this table, and doesn't say how the table fits with OneLake security roles that apply to Viewers and users with Read.

### Row-, column-, object- and folder/file-level access

These T-SQL controls work in the Warehouse and the SQL analytics endpoint, and only for queries through T-SQL. Selecting a column you have no permission on, even through SELECT *, fails with error 230 instead of returning NULLs.

- **Object-level security**: `GRANT`, `DENY` and `REVOKE` on tables, views, functions and procedures.
- **Column-level security**: grant `SELECT` on specific columns, for example `GRANT SELECT ON dbo.Customer (CustomerID, Name) TO [user]`.
- **Row-level security**: an inline table-valued function plus `CREATE SECURITY POLICY … ADD FILTER PREDICATE`. Filter predicates silently hide rows from SELECT, UPDATE and DELETE; INSERT still works. Each table needs its own policy.
- RLS applies to **every** user, including db_owner and the workspace Admin, Member and Contributor roles. Write the predicate to let those roles through if they need all rows.
- To change an RLS function, drop the security policy first. A Power BI Direct Lake model over a warehouse with RLS falls back to DirectQuery.
- **Folder- and file-level access**: use OneLake security roles (below), not T-SQL.

### Dynamic data masking

| Mask | Result |
|---|---|
| `default()` | XXXX for strings, 0 for numbers, 1900-01-01 for dates |
| `email()` | aXXX@XXXX.com |
| `random(start, end)` | Random number in the range (numeric columns only) |
| `partial(prefix, "padding", suffix)` | Keeps the first and last characters with custom padding between |

- Workspace Admin, Member and Contributor hold `CONTROL` on the database, so they see **unmasked** data by default.
- Grant `UNMASK` (on a column) to let anyone else see real values. Adding or removing a mask needs `ALTER ANY MASK` plus `ALTER` on the table.
- Masking doesn't stop inference: range queries in a `WHERE` clause can reveal values. Combine it with CLS, RLS and object permissions.

### OneLake security

- OneLake security roles grant **Read** (or **ReadWrite** in a lakehouse) on chosen tables or folders, optionally with row- and column-level rules. They apply across Spark, the SQL analytics endpoint and other engines.
- It is **deny-by-default**: a user outside every role sees no data.
- It's supported on lakehouses (Read and ReadWrite), mirrored databases, mirrored catalogs and Azure Databricks mirrored catalogs (Read).
- Roles are created by users with Write and Reshare, usually Admin and Member.
- Admin, Member and Contributor are **not restricted** by OneLake security, because write access overrides it. Filtering applies to Viewers and to users with item permissions.
- The **DefaultReader** role includes everyone with ReadAll. Remove a user from it, or they keep full access.
- To enforce OneLake security through the SQL analytics endpoint, switch it from Delegated identity mode to **User's identity mode** (Security tab → Data access mode settings). In user identity mode, dynamic data masking isn't supported.
- A user in several roles gets the most permissive access.
- Exception: the SQL analytics endpoint intersects column-level allow lists across a user's roles instead of combining them. If any role hides a column, the endpoint blocks it. Keep related row and column rules for a table in one role.
- ReadAll is an item permission and does not grant data access by itself. DefaultReader is the OneLake security role that does, and its members are everyone with ReadAll. Delete DefaultReader and those users lose data access even though they still hold ReadAll.
- Only Grant roles exist. There are no Deny roles, and the only permissions are Read and ReadWrite.
- ReadWrite applies only to users who have Read, such as Viewers. It has no effect on Admin, Member or Contributor, and a ReadWrite role cannot contain row or column rules.
- You cannot define roles directly on a OneLake-to-OneLake shortcut. Target roles apply at the shortcut location as inferred roles, so effective access is the shortcut's roles intersected with the inferred target roles. OneLake-to-OneLake shortcuts pass the calling user's identity through, except when a T-SQL engine in Delegated identity mode (or Direct Lake over SQL) reads them: that uses the item owner's identity and then applies OneLake security roles. The documented workaround is T-SQL in User's identity mode, or Direct Lake over OneLake. External shortcuts always use delegated authentication. To create a shortcut you need Write on the item where it is created plus Read on the target (OneLake security Read, or item ReadAll where the item lacks OneLake security). Admin, Member and Contributor also need Read on the target path.
- Permissions inherit downward. Read on Files/folder1/subfolder11 covers everything under it, but not sibling files or folders in the parent.
- Role definition changes take about 5 minutes. Group membership changes take about an hour, and some engines may need an extra hour because of caching.
- Limits: 250 roles per item (1,000 on request), 500 members per role, 500 permissions per role.
- Source: [OneLake data access control model](https://learn.microsoft.com/en-us/fabric/onelake/security/data-access-control-model)

### Sensitivity labels

- Labels come from Microsoft Purview Information Protection. A tenant setting must allow users to apply them.
- **Downstream inheritance**: a label flows to dependent items, never overwrites a label someone applied manually, and is limited to 80 items. The default mode asks for user consent; a tenant setting makes it fully automatic.
- A default label policy can label new, unlabeled items. It doesn't apply to service principals, APIs or B2B guests.
- A domain can set its own default sensitivity label.

**Where a sensitivity label carries, and where it doesn't.** From the [Fabric sensitivity labels overview](https://learn.microsoft.com/en-us/fabric/governance/information-protection) and [downstream inheritance](https://learn.microsoft.com/en-us/fabric/governance/service-security-sensitivity-label-downstream-inheritance), opened Nov 6, 2026.

| Case | What Learn says |
|---|---|
| Item created from a labeled item: pipeline or notebook from a lakehouse, shortcut from a lakehouse, pipeline from a notebook, KQL queryset or pipeline from a KQL database | Inherits the label at creation, even if the tenant setting "Automatically apply sensitivity labels to downstream content" is disabled |
| Item autogenerated from a lakehouse or warehouse | Takes the label of that parent lakehouse or warehouse. It doesn't inherit from items further upstream |
| Direction of downstream inheritance | Supported: Power BI to Power BI, Fabric to Fabric, Fabric to Power BI. Not supported: Power BI to Fabric |
| Inheritance from data sources | Power BI semantic models only, and only in fully automated downstream mode |
| Power BI export | Label and protection carry on Export to Excel, PDF and PowerPoint, Analyze in Excel, PivotTable in Excel with a live connection (Microsoft 365 E3 and above), and download to .pbix |
| Export to .csv or .txt, and cross-tenant scenarios such as external data sharing | Not supported |
| Export from other Fabric items | No export method carries the label. A warning is issued |
| Mandatory labeling | Power BI items only, with limitations for some other items. For lakehouses, pipelines and warehouses with mandatory on and default off, the user can pick a label but can save without one unless the experience itself requires it. Not enforced through the flyout menu |
| Default labeling | On creation, only if the item has a clear create dialog. On update, any attribute change for Power BI items; for other items only name or description changes through the flyout |

- Manual labeling needs the user in the tenant's specified-users list **and** the label published to them in Purview. Labeling Power BI items also needs a Pro or PPU license. Programmatic labeling works for all Fabric items through the Power BI admin REST APIs.
- Downstream inheritance never overwrites a manually applied label and never replaces a label with a less restrictive one. Beyond 80 downstream items, none inherit.
- The two pages leave one default unreconciled. The downstream page calls user consent the default mode, yet says the fully automated tenant setting is enabled by default when information protection is on. The overview page says downstream inheritance is on by default. Learn doesn't say which wins in a given tenant.
- Learn doesn't state inheritance precedence between inherited and manual labels on the overview page, which items count as "Power BI" for mandatory labeling, or any workspace role rules for applying labels.

### Endorse items

| Badge | Who can apply | Applies to |
|---|---|---|
| Promoted | Anyone with write permission on the item | Any item except Power BI dashboards |
| Certified | Only reviewers named by a Fabric admin (can be delegated per domain); anyone can request it | Any item except Power BI dashboards |
| Master data | Only users named by a Fabric admin | Items that contain data, such as lakehouses and semantic models |

An item carries one endorsement badge. Certification and master data must be enabled by a Fabric admin.

### Fabric audit logs

- Search them in the Microsoft Purview portal; the Fabric admin portal's Audit logs link goes there. PowerShell works too.
- You need the **Audit Logs** or **View-Only Audit Logs** role. The Audit Manager and Audit Reader role groups include it.
- Warehouse SQL audit logs are a separate, warehouse-level setting.

Sources: [Workspace roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces) · [Share items](https://learn.microsoft.com/en-us/fabric/fundamentals/share-items) · [Warehouse security](https://learn.microsoft.com/en-us/fabric/data-warehouse/security) · [Row-level security](https://learn.microsoft.com/en-us/fabric/data-warehouse/row-level-security) · [Column-level security](https://learn.microsoft.com/en-us/fabric/data-warehouse/column-level-security) · [Dynamic data masking](https://learn.microsoft.com/en-us/fabric/data-warehouse/dynamic-data-masking) · [OneLake security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-onelake-security) · [OneLake security for SQL analytics endpoints](https://learn.microsoft.com/en-us/fabric/onelake/sql-analytics-endpoint-onelake-security) · [Information protection](https://learn.microsoft.com/en-us/fabric/governance/information-protection) · [Downstream inheritance](https://learn.microsoft.com/en-us/fabric/governance/service-security-sensitivity-label-downstream-inheritance) · [Endorsement](https://learn.microsoft.com/en-us/fabric/governance/endorsement-overview) · [Track user activities](https://learn.microsoft.com/en-us/fabric/admin/track-user-activities) · [SQL audit logs](https://learn.microsoft.com/en-us/fabric/data-warehouse/configure-sql-audit-logs)

## Part 9 — Lifecycle management

Git integration versions item definitions per workspace, database projects version warehouse schema as code, and deployment pipelines promote content between stage workspaces. None of the three copies data.

### Version control (Git integration)

- Providers: **Azure DevOps**, **GitHub** and **GitHub Enterprise**, cloud-hosted only.
- Integration is per workspace, and the workspace folder structure is kept (up to 10 levels).
- Supported items include lakehouses, notebooks, Spark job definitions, environments, pipelines, Dataflow Gen2, Copy jobs, mirrored databases, warehouses, SQL databases, Eventhouses, Eventstreams, KQL databases and querysets, Real-Time dashboards, Activator and variable libraries. Unsupported items are ignored, not deleted.
- Only item **definitions** are synced. Restoring an item through Git recreates its definition, not its data.

| Action | Workspace role needed |
|---|---|
| Connect, sync or disconnect the workspace | Admin |
| Commit or update | Contributor or higher, with write permission on all items |
| Switch or create a branch | Admin; Member or Contributor only if the workspace setting "Allow users with at least Contributor role to change Git branch" is on |
| Branch out to another workspace | Admin, Member or Contributor |
| See Git information | Viewers can't |

- **Commit** sends selected changed items to Git. It's blocked while Git has updates you haven't pulled.
- **Update** pulls the whole branch, never selected items, and is blocked while a conflict exists.
- On first connect, if both sides have content you choose the direction: commit overwrites Git, update overwrites the workspace.
- Each user signs in with their own Git credentials.
- Limits: 1,000 items per workspace, branch names up to 244 characters, file paths up to 250 characters, files up to 25 MB.

### Database projects

- A database project is the warehouse schema written as code. Create **SDK-style** SQL database projects with the VS Code **SQL Database Projects** and **MSSQL** extensions.
- Building a project produces a `.dacpac` (via DacFx). Use it to compare schemas, script changes, and publish with **SqlPackage**, including from Azure DevOps or GitHub CI/CD.
- Database references (to another project or `.dacpac`) model one-way dependencies between warehouses using SQLCMD variables.
- Lakehouse tables and SQL analytics endpoint objects aren't tracked the way warehouse projects are. Use a Warehouse for full schema-as-code.

### Deployment pipelines

- A pipeline has **2 to 10 stages** (3 by default). The number of stages and their names are fixed once it's created.
- Each stage maps to one workspace. **Assigning** a workspace to a stage only links it; you still run a deployment to copy content.
- **Pairing** links matching items in adjacent stages. Paired items overwrite on deploy and stay paired even if renamed. Unpaired items with the same name create a duplicate.
- You can deploy to the next or previous stage (backward deployment). One deployment can include up to 300 items.
- **Copied**: item definitions, data source and parameter settings (deployment rules can change them per stage), report pages, dashboard tiles, model metadata and item relationships.
- **Not copied**: data, item URL and ID, permissions, workspace settings, app content, and for semantic models the role assignments, refresh schedule, data source credentials and endorsement.
- **Autobinding** connects deployed items to their dependencies in the target stage, and the deployment fails if a dependency is missing; use **Select related**. Direct Lake semantic models don't autobind (use data source rules). Dataflow Gen2 doesn't support autobinding.
- Workspaces must be on a Fabric capacity.

| Action | Permissions needed |
|---|---|
| Manage, share or delete the pipeline | Pipeline admin (the pipeline's only permission level; not a workspace role) |
| Assign a workspace to a stage | Pipeline admin **and** workspace Admin of that workspace |
| Deploy between stages | Pipeline admin **and** Contributor or higher in both the source and target workspaces |
| Create or edit deployment rules | Pipeline admin, Contributor or higher in the target workspace, and owner of the item |

Sources: [Git integration overview](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration) · [Git integration process and permissions](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-integration-process) · [Warehouse development and deployment](https://learn.microsoft.com/en-us/fabric/data-warehouse/development-deployment) · [Cross-warehouse database projects](https://learn.microsoft.com/en-us/fabric/data-warehouse/cross-warehouse-development-database-projects) · [Deployment pipelines overview](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines) · [The deployment process](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/understand-the-deployment-process) · [Deployment rules](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/create-rules)

# Domain 2 — Ingest and transform data (30–35%)

This domain covers Part 1 (foundations and choosing a data store), Part 3 (batch ingestion), Part 4 (loading patterns), Part 5 (batch transformation) and Part 6 (streaming and Real-Time Intelligence).

## Part 1 — Foundations: OneLake and choosing a data store

Every Fabric data store writes to one OneLake per tenant in open Delta (or Iceberg) format, so the store choice is about who works on the data and how, not where it lives.

### OneLake essentials

- One OneLake per tenant. You can't delete it or create a second one.
- Hierarchy: tenant → workspace → item (lakehouse, warehouse, eventhouse, KQL database). Each workspace sits on a capacity tied to a region.
- Tables are stored as Delta Parquet or Apache Iceberg. Spark, T-SQL and Analysis Services all read the same single copy.
- OneLake is compatible with ADLS Gen2 APIs and SDKs. A workspace appears as a container and an item as a folder.
- Deleted files are kept for 7 days (soft delete).

### Choose a data store

| Store | Pick it when | Primary languages | Writes |
|---|---|---|---|
| Lakehouse | Big data and ML; unstructured, semi-structured or structured files; data engineering in notebooks | PySpark, Spark SQL, Scala, R | Spark writes; T-SQL is read-only through the SQL analytics endpoint |
| Warehouse | Enterprise data warehouse, SQL-based BI, star schemas, full multi-table T-SQL transactions | T-SQL | INSERT, UPDATE, DELETE, MERGE, COPY INTO, CTAS |
| Eventhouse (KQL databases) | Streaming events and high-granularity time, space or text data for interactive analytics | KQL, T-SQL | Streaming or queued ingestion |
| SQL database in Fabric | OLTP: ACID, high concurrency, enforced foreign keys, automatic index tuning; same engine as Azure SQL Database | T-SQL | Full OLTP DML; mirrored to OneLake automatically |
| Cosmos DB in Fabric | NoSQL and AI apps with vector data | REST APIs, app SDKs | Document writes |

All stores are in OneLake in open format by default. The exception is a KQL database, where OneLake availability is opt-in.

### Lakehouse SQL analytics endpoint

- It is **read-only** over Delta tables. Use Spark to change data.
- You can create views, functions, stored procedures and SQL security (object- and row-level) in it.
- Only Delta tables under `/Tables` appear. Files under `/Files` and external Delta tables created in Spark don't; add a shortcut under Tables to expose them.
- SQL permissions apply only to queries through the endpoint, not to Spark or OneLake access.
- Up to 150 warehouse and SQL analytics endpoint items per workspace.

Exam cue: "the team writes T-SQL including INSERT/UPDATE/DELETE" → Warehouse. "Mixed PySpark builders and T-SQL readers" → Lakehouse. "Telemetry, logs, time series, KQL" → Eventhouse.

Sources: [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview) · [Choose a data store](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-data-store) · [SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint)

## Part 3 — Batch ingestion

Pick the ingestion tool by whether you need to copy the data at all, how much transformation happens on the way in, and who builds it.

| Option | Copies data? | Best for | Transformation | Builder |
|---|---|---|---|---|
| OneLake shortcut | No (reference in place) | Using data already in OneLake, ADLS, S3, GCS and others without duplication | None | Anyone with access |
| Mirroring | Yes, continuous near real-time replica in Delta | Keeping an operational database in sync in OneLake | None | Low effort, no ETL |
| Pipeline copy activity | Yes | Large-scale, scheduled, no-code movement; 50+ sources, 40+ destinations; petabyte scale | Light: type conversion, column mapping, merge/split files, flatten hierarchy | Data engineer or integrator |
| Copy job | Yes | Full or incremental copy (watermark or CDC) without building a pipeline | Light | Analyst, integrator, engineer |
| Dataflow Gen2 | Yes | Power Query transformations before load; 150+ connectors | Low to high: 300+ transformation functions | Analyst or engineer who knows Power Query (M) |
| Notebook (Spark) | Yes | Code-first ingestion and complex logic | Low to high | Engineer (PySpark, Spark SQL, Scala, R) |

**How to choose**

1. Does the data need to be copied at all? Data already in OneLake or cloud storage: shortcut. An operational database to keep in sync: mirroring. Mirroring only goes from the source into OneLake, never back out.
2. Is there transformation on the way in? None or light: Copy job for a simple scheduled load, or the pipeline Copy activity as one step in a larger workflow. Heavy, with Power Query: Dataflow Gen2. Heavy, in code: notebook.
3. Is the target a Warehouse and the job a bulk file load? COPY INTO has the highest throughput.

**Copy job vs pipeline Copy activity**

|  | Copy job | Pipeline Copy activity |
|---|---|---|
| What it is | Standalone item, no pipeline needed | Activity inside a pipeline |
| Incremental loads | Built in: tracks the last successful run and resumes after a failure | You build the watermark logic with variables and parameters |
| Deletes | CDC mode captures deletes and supports SCD Type 2 | Not covered in the Copy activity docs |
| Scheduling | Its own schedules (several per job) and manual Run | Scheduled by the pipeline; event triggers apply to the pipeline |
| Tuning | Limited; auto-partitioning is in preview | Throughput units, parallel copies, staging, compression, fault tolerance, consistency checks |
| Chaining | Copy only, though it can run inside a pipeline through the Copy job activity | Chains with notebooks, stored procedures and alerts |
| Best for | Simple, reliable movement with no transformation | Copy as one step of a workflow, or fine control over performance and errors |

Sources: [What is Copy job](https://learn.microsoft.com/en-us/fabric/data-factory/what-is-copy-job) · [Copy activity](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity) · [Mirroring overview](https://learn.microsoft.com/en-us/fabric/mirroring/overview) · [Ingest data into a Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data-copy)

### OneLake shortcuts

- A shortcut behaves like a symbolic link. Deleting the shortcut leaves the target untouched. Deleting a file **inside** a shortcut deletes it at the target if you have write permission there.
- You can create shortcuts in lakehouses and KQL databases. In a KQL database, query them with `external_table()`.
- **Tables folder**: shortcuts only at the top level, no subfolders. Delta data is recognized as a table automatically. Names containing spaces aren't recognized as Delta tables.
- **Files folder**: any level, any format, no table discovery.
- **Internal** targets: lakehouses, warehouses, KQL databases, mirrored databases, mirrored Azure Databricks catalogs, semantic models and SQL databases. Access uses the **calling user's identity**, so the user needs permission on the target.
- **External** targets: ADLS Gen2, Azure Blob, Amazon S3, S3-compatible, Google Cloud Storage, Dataverse, Iceberg, and OneDrive/SharePoint. On-premises targets go through the on-premises data gateway. ADLS and S3 shortcuts authorize through a cloud connection, and you need permission on that connection to bind it.
- Limits: 100,000 shortcuts per item, 100 unique data source connections per item, 10 shortcuts per OneLake path, 5 direct shortcut-to-shortcut links, and no `%` or `+` in names.

### Mirroring

- **Database mirroring** replicates data. Sources include Azure SQL Database, Azure SQL Managed Instance, SQL Server, Azure Cosmos DB, Azure Database for PostgreSQL, Google BigQuery, Oracle, SAP, Snowflake, and Fabric SQL database (automatic).
- **Metadata mirroring** syncs catalog, schema and table names only and reads data through shortcuts. Examples are Azure Databricks Unity Catalog and Snowflake.
- **Open mirroring** lets any app write change data to a landing zone through public APIs.
- The result is a mirrored database item plus a read-only SQL analytics endpoint. Changes can arrive as often as every 15 seconds.
- Cost: replication compute is free and doesn't use capacity units. Each capacity unit includes 1 TB of free mirroring storage (F64 = 64 TB). Queries are billed normally, and replication stops while the capacity is paused.
- Retention: mirrored databases created after mid-June 2025 default to 1 day of history (older ones 7 days). Change it in Settings → Delta table management.

### Copy job

- **Full copy** copies everything each run. **Incremental copy** does a full first load, then only changes.
- Watermark-based incremental needs a ROWVERSION, datetime, date, integer or string-as-datetime column. It captures inserts and updates only.
- CDC-based incremental needs CDC enabled on the source. It captures inserts, updates **and deletes**, and supports SCD Type 2.
- Write methods: Append (default), Merge (uses the primary key by default), Overwrite, SCD Type 2.
- Copy job tracks its own state. A failed run resumes from the last successful run, and you can reset to a full copy per job or per table.

### Dataflow Gen2 destinations

- Destinations: Lakehouse tables and files, Warehouse, KQL database, Fabric SQL database, Azure SQL, Azure Data Explorer, ADLS Gen2, SharePoint files, Snowflake, PostgreSQL.
- Update methods are **Append** or **Replace**. KQL database and Azure Data Explorer don't support Replace.
- Automatic (managed) settings apply only to Lakehouse and Azure SQL. They drop and recreate the table on every refresh.
- A **Warehouse** destination requires staging, supports only a fixed schema, and only loads into a warehouse in the same workspace.

**Dataflow Gen2 incremental refresh is bucket-based, not a watermark.** From [Incremental refresh in Dataflow Gen2](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh), opened Nov 12, 2026.

- **Extract data from the past** is required. It sets the window the dataflow manages and does the initial load. **Bucket size** splits that window by a DateTime, Date or DateTimeZone column.
- Each refresh compares the maximum value of a change-detection column per bucket with the previous refresh. Only changed buckets are processed: the old data for that bucket is deleted, then the fresh data is inserted.
- So the only supported update method is **replace**, and the destination must use a **fixed schema**. Append is not supported.
- Supported destinations: Lakehouse, Warehouse and Azure SQL Database. The default destination configuration is not supported.
- Lakehouse: `OPTIMIZE` and `REORG TABLE` aren't supported on a table that uses incremental refresh, and other writers such as Spark should be avoided.
- Limits: 50 buckets per query, 150 per dataflow, and 10 concurrent bucket evaluations for a lakehouse.
- Contrast: a Copy job keeps a watermark and moves forward from the last successful run. Dataflow Gen2 re-checks every bucket in the window, so it also catches late changes to old rows.
- Learn doesn't say whether the bucket replace is transactional.

**Dataflow Gen2 destinations, compiled: update method, schema option, incremental refresh.** From [data destinations and managed settings](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings) and [incremental refresh](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh), opened Nov 15, 2026.

Think of it as three layers, decided in this order.

1. **Update method: append or replace.** Replace means the destination's data is replaced at each refresh. KQL databases and Azure Data Explorer don't support replace.
2. **Schema option, only if you chose replace: dynamic or fixed.** Append has no schema options ("changes to the schema aren't possible"). A Warehouse destination supports only fixed.
3. **Incremental refresh, only if you turn it on:** replace, fixed schema, Lakehouse, Warehouse or Azure SQL Database.

| Setup | What a refresh does to the table | Relationships and measures |
|---|---|---|
| Append | Adds rows. No schema changes possible. | Kept |
| Replace + fixed schema | Drops and replaces only the rows. If the query's columns no longer match the table, the publish fails. | Kept |
| Replace + dynamic schema | If the destination schema differs from the expected one, the table is dropped and recreated. | Can be lost |
| Automatic settings (new tables on Lakehouse, Azure SQL Database, Snowflake) | Replace with managed mapping. The table is dropped and recreated on every refresh. | Can be lost |
| Replace + incremental refresh | Only the rows of each changed bucket are replaced. Older buckets aren't touched. | Kept (fixed schema) |

**Incremental refresh rules.** Replace only. Fixed schema (change a dynamic table to fixed before configuring it). No `OPTIMIZE` or `REORG TABLE` on a lakehouse table that uses it, and avoid other writers such as Spark. Turn vacuuming off. Limits: 50 buckets per query, 150 per dataflow, 10 concurrent bucket evaluations. A Copy job's watermark incremental copy is a different feature.

**Other facts.** A table the dataflow didn't create is never recreated if you delete it. The Warehouse destination also needs staging and the same workspace.

**Exam shortcuts.** Append: no schema options. Warehouse: fixed only. Incremental refresh: replace and fixed, no `OPTIMIZE`. The table must adapt to new columns: replace and dynamic, and relationships and measures can be lost. Relationships or measures must survive: fixed.

**Learn doesn't say (unverified).** Which destinations other than Snowflake (both options with replace on new tables) and Warehouse (fixed only) offer the dynamic option. Why incremental refresh needs fixed schema: the bucket-by-bucket reason is my reading. What a dynamic-schema refresh does when the schemas already match: "just replaces the data" is my reading of the drop-and-recreate sentence.

### Load a Warehouse

- **COPY INTO** gives the highest throughput. It reads CSV, JSONL and Parquet from ADLS Gen2, Azure Blob and OneLake. `BULK INSERT` maps to the same behavior.
- By default COPY INTO uses the caller's Microsoft Entra identity. `CREDENTIAL = (IDENTITY = 'Workspace Identity')` uses the workspace identity for the source only.
- **T-SQL across items**: `INSERT…SELECT`, `SELECT INTO` and `CREATE TABLE AS SELECT` (CTAS) can read warehouses, lakehouses and mirrored databases **in the same workspace** using three-part names. `OPENROWSET` reads Parquet, CSV or JSONL files in Azure storage.
- Best practice: avoid singleton INSERTs, keep files at least 4 MB (ideally 100 MB–1 GB), and prefer ADLS Gen2 over Blob.
- The warehouse writes V-Order Parquet by default; Microsoft advises keeping it on.

```sql
-- Lakehouse to warehouse, same workspace
INSERT INTO dbo.FactSales
SELECT * FROM MyLakehouse.dbo.sales;
```

Sources: [Decision guide: copy, Copy job, dataflow, Eventstream, Spark](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-pipeline-dataflow-spark) · [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) · [Mirroring](https://learn.microsoft.com/en-us/fabric/mirroring/overview) · [Copy job](https://learn.microsoft.com/en-us/fabric/data-factory/what-is-copy-job) · [Dataflow Gen2 destinations](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings) · [Ingest data into the Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data)

## Part 4 — Loading patterns

Load dimensions before facts, load facts incrementally whenever the source lets you detect new rows, and never truncate and reload a dimension that has generated surrogate keys. The streaming loading pattern is covered in Part 6.

### Full vs incremental loads

| Pattern | How new or changed rows are found | Captures deletes? | Fabric tools |
|---|---|---|---|
| Full load | Reload everything each run | Yes, implicitly | Copy activity, Copy job (full copy), Dataflow Gen2 Replace, CTAS |
| High watermark | Store the last max ID or timestamp; next run reads rows above it | No | Lookup + Copy activity in a pipeline, Copy job (watermark), notebook |
| Change data capture (CDC) | Source tracks each row change (SQL Server, Azure SQL MI) | Yes | Copy job (CDC), Eventstream CDC sources, mirroring |
| Change tracking | Source flags changed rows (SQL Server, Azure SQL MI, Azure SQL DB) | Yes | Pipeline queries, notebook |

Upserts: Fabric Warehouse supports `MERGE` as a generally available feature. In a lakehouse, use Delta `MERGE INTO … WHEN MATCHED … WHEN NOT MATCHED` from Spark.

### Prepare data for a dimensional model

**ETL order**: (optional) load staging tables → process dimensions, in dependency order → process facts → post-processing, such as a semantic model refresh.

- Staging tables live in their own schema and are never exposed to business users. `TRUNCATE TABLE` is supported for clearing them. Mirroring and shortcuts can replace staging copies.
- **Surrogate keys**: use the smallest integer type that fits. Fabric Warehouse `IDENTITY` columns are **bigint only**. Values are unique but not guaranteed sequential, and you can't set seed or increment. `ALTER TABLE` can't add an IDENTITY column; use CTAS instead.
- Warehouse primary, unique and foreign keys must be `NOT ENFORCED`, so your ETL has to check referential integrity itself.
- Date dimension keys usually use the `YYYYMMDD` format. Extend the table each year, ideally with a stored procedure.

**Slowly changing dimensions**

| Type | When a tracked attribute changes |
|---|---|
| SCD 1 | Overwrite the attribute in place; update last-modified columns |
| SCD 2 | Expire the current row (set the end date and IsCurrent = FALSE), then insert a new row (start date = the old row's end date, IsCurrent = TRUE) |
| SCD 3 | Update in place like SCD 1, keeping the prior value in its own column |

Fact loads look up the surrogate key of the **current** version of an SCD 2 member.

### Duplicate, missing and late-arriving data

- **Late-arriving dimension (inferred member)**: the fact load inserts a dimension row with the natural key, "Unknown" attributes and `IsInferredMember = TRUE`. When the real details arrive, update that row in place (not as an SCD change) and set the flag to FALSE.
- **Failed key lookup**: store a special "Unknown" member's key so the fact row still loads, then fix it in a later process.
- **Deleted source rows**: soft-delete with an `IsDeleted` bit column instead of deleting dimension or fact rows.
- **Duplicates**: PySpark `df.dropDuplicates(["key"])`; T-SQL `ROW_NUMBER() OVER (PARTITION BY key ORDER BY modified DESC)` and keep row 1; KQL `summarize arg_max(Timestamp, *) by key`.
- **Missing values**: PySpark `df.fillna(...)` or `df.dropna(...)`; T-SQL `COALESCE` or `ISNULL`; KQL `coalesce()` and `isnull()` / `isempty()`.
- **Late events in Spark streaming**: `withWatermark("eventTime", "10 minutes")` sets how long state waits for late rows.

Sources: [Load tables in a dimensional model](https://learn.microsoft.com/en-us/fabric/data-warehouse/dimensional-modeling-load-tables) · [IDENTITY columns](https://learn.microsoft.com/en-us/fabric/data-warehouse/identity) · [T-SQL surface area (MERGE, constraints)](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) · [Copy job incremental and CDC](https://learn.microsoft.com/en-us/fabric/data-factory/what-is-copy-job) · [KQL arg_max](https://learn.microsoft.com/en-us/kusto/query/arg-max-aggregation-function) · [Spark structured streaming watermarks](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)

## Part 5 — Batch transformation

Match the transformation tool to where the data lives and the builder's skills: Power Query for low-code shaping, Spark for large or complex lakehouse work, T-SQL inside a warehouse, KQL inside an eventhouse.

### Choose a transformation tool

| Tool | Use when | Skill set | Where results land |
|---|---|---|---|
| Dataflow Gen2 | Low-code cleansing and shaping with 300+ Power Query transformations; analysts or engineers who know Power Query | Power Query (M) | Lakehouse, Warehouse, KQL database, SQL database and other destinations |
| Notebook | Large volumes, complex logic, ML prep, any file format; lakehouse medallion layers | PySpark, Spark SQL, Scala, R | Lakehouse Delta tables |
| T-SQL | Data already in a warehouse; set-based CTAS, INSERT…SELECT, MERGE, stored procedures | T-SQL | Warehouse tables |
| KQL | Data in an eventhouse; time-series, logs, telemetry; transform at ingestion with update policies | KQL | KQL database tables |

### Denormalize

Denormalizing joins dimension attributes onto facts to make wide, read-friendly tables for reporting.

- PySpark: `fact.join(F.broadcast(dim), "key", "left")`. Broadcasting the small dimension avoids shuffling the large fact table.
- T-SQL: `CREATE TABLE gold.SalesWide AS SELECT f.*, d.Category FROM dbo.FactSales f JOIN dbo.DimProduct d ON f.ProductKey = d.ProductKey;`
- KQL: `Sales | lookup kind=leftouter Products on ProductId`

### Group and aggregate

Fabric Warehouse and the SQL analytics endpoint support `ROLLUP`, `CUBE` and `GROUPING SETS` in `GROUP BY`.

| Clause | Output for (Region, Territory) |
|---|---|
| `ROLLUP(Region, Territory)` | Detail rows, a subtotal per Region, and a grand total (hierarchical) |
| `CUBE(Region, Territory)` | Every combination: detail, per Region, per Territory, grand total |
| `GROUPING SETS ((Region), ())` | Exactly the sets listed: here per-Region totals plus a grand total |
| `GROUP BY ALL` | Groups by every non-aggregated column (Fabric Warehouse and SQL analytics endpoint only) |

`GROUPING(col)` returns 1 when the NULL in a result row is a subtotal placeholder rather than real data. `GROUPING_ID()` combines those flags into one number.

- PySpark: `df.groupBy("Region").agg(F.sum("Sales").alias("Total"))`; `df.rollup(...)` and `df.cube(...)` mirror the SQL clauses.
- KQL: `Sales | summarize Total = sum(Amount) by Region, bin(Timestamp, 1h)`.

Sources: [Decision guide: transform tools](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-pipeline-dataflow-spark) · [Choose a data store](https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-data-store) · [GROUP BY in Fabric Warehouse](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=fabric) · [GROUPING](https://learn.microsoft.com/en-us/sql/t-sql/functions/grouping-transact-sql?view=fabric) · [KQL summarize](https://learn.microsoft.com/en-us/kusto/query/summarize-operator) · [KQL lookup](https://learn.microsoft.com/en-us/kusto/query/lookup-operator)

## Part 6 — Streaming and Real-Time Intelligence

Eventstream is the no-code way to capture, transform and route events. Spark structured streaming is the code-first path into lakehouse Delta tables. KQL in an Eventhouse is where streaming data is stored and queried at speed.

### Choose a streaming engine

| Engine | Choose it when | Code | Typical destination |
|---|---|---|---|
| Eventstream | Ingest and route events from Event Hubs, IoT Hub, Kafka, CDC databases or Fabric events with light no-code transforms | No code (SQL operator in preview) | Eventhouse, Lakehouse, Activator, derived stream, custom endpoint |
| Spark structured streaming | Complex logic, joins with reference data, writing Delta tables; production jobs needing retries | PySpark or Scala | Lakehouse Delta tables |
| KQL (Eventhouse) | High-speed analytics over time-series, logs and telemetry; transform at ingestion with update policies; precompute with materialized views | KQL | KQL database tables |

### Eventstream

- **Sources** include Azure Event Hubs, IoT Hub, Event Grid, Service Bus, Kafka (Apache, Confluent, Amazon MSK), Amazon Kinesis, Google Pub/Sub, CDC from Azure SQL, SQL MI, SQL Server on VM, PostgreSQL, MySQL, Cosmos DB and MongoDB, Fabric workspace item, OneLake, job and capacity events, Azure Blob Storage events, custom endpoints (Kafka protocol supported) and sample data.
- **Transformations**: Filter, Manage fields (add, remove, rename, change type; built-in string, date-time and math functions), Aggregate (sum, min, max or average recalculated as each event arrives), Group by (aggregations over a time window), Union (keeps only fields with the same name and type), Expand (one row per array element), Join (two streams on a condition).
- **Destinations**: Eventhouse (Direct ingestion, or Event processing before ingestion), Lakehouse (Delta), Activator, Derived stream, Custom endpoint, Spark Notebook (preview). Several destinations can be attached at once.
- Operators can sit before Lakehouse, Eventhouse (processing mode), Derived stream and Activator. For other destinations, send the operator output to a derived stream first.
- Limits: 1 MB maximum message size, 90 days maximum retention, **at-least-once** delivery. Eventstream needs at least an F4 capacity.

**SQL operator: event time and limits.** From [Process events using a SQL operator](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/process-events-using-sql-code-editor) and [TIMESTAMP BY](https://learn.microsoft.com/en-us/stream-analytics-query/timestamp-by-azure-stream-analytics), opened Nov 7, 2026.

**What "topology" means.** The SQL operator page says "if you add a SQL operator to your topology, you must create new destination nodes" and never defines the word. Read it as the layout of your eventstream on the editor canvas: the sources, operators and destinations (the boxes) and the arrows between them. "Existing destination nodes" are the destination boxes already on that canvas. Learn doesn't define the term, so this reading is plain English, not a quoted definition.

- An eventstream uses **arrival time** by default. To window on a field in the event, add `TIMESTAMP BY <field>` after the input name: `FROM input TIMESTAMP BY readingTime`.
- Window argument order: `HoppingWindow(timeunit, windowsize, hopsize)`. A hop equal to the size is a tumbling window.
- Adding a SQL operator requires **new destination nodes**; existing destination nodes can't be reused.
- A SQL operator can't share a processing path with other built-in operators, and SQL operators can't be chained.
- Eventstream names containing an underscore or a dot aren't compatible with SQL operators.
- The Fabric page names only Tumbling and Hopping windows. It doesn't say whether Session, Sliding and Snapshot work in the SQL operator, and gives no default late-arrival or out-of-order values.

### Windowing functions

The five window types apply to Eventstream Group by (and Azure Stream Analytics). Tumbling, hopping and session windows emit a result at the window end, timestamped with the window end. A sliding window emits only when its contents change. The maximum size is 7 days.

| Window | Behavior | Parameters |
|---|---|---|
| Tumbling | Fixed size, back to back, no overlap; each event lands in exactly one window | Size |
| Hopping | Fixed size, starts every hop, so windows overlap when hop < size; an event can count in several windows. Hop = size makes it a tumbling window | Size, hop, optional offset |
| Sliding | One window of fixed length that always covers the last N seconds. Emits output only when an event enters or exits the window; an event exits exactly one window length after it arrived. No hop and no fixed schedule | Size |
| Session | Starts at the first event, extends while the next event arrives within the timeout, closes on timeout or at the maximum duration; optional partition key | Timeout, max duration |
| Snapshot | Groups events that share the same timestamp (`GROUP BY System.Timestamp()`) | None |

The same ideas in code:

- Spark: `groupBy(window("eventTime", "10 minutes", "5 minutes"))` makes hopping windows; omit the slide for tumbling; `session_window("eventTime", "5 minutes")` for sessions.
- KQL: `summarize count() by bin(Timestamp, 5m)` makes tumbling buckets.

**Choosing a window**

- Fixed schedule, no overlap: tumbling ("count orders every 10 minutes").
- Fixed schedule, overlapping results: hopping ("every 10 minutes, report the last 30"). A 30-minute size with a 10-minute hop puts each event in three windows. If the hop is larger than the size, events in the gaps are never counted.
- A result whenever the contents change: sliding. It has no hop. An event leaves exactly one window length after it arrived, so results also appear when nothing new arrives. It produces nothing while the window is empty and no event arrives. For a result every second regardless of change, use hopping with a 1-second hop.
- Activity bursts separated by quiet gaps: session. The maximum duration is checked at fixed intervals, so one session can last up to twice the maximum.
- Events with the same timestamp: snapshot.

**Sliding vs tumbling.** A tumbling window is anchored to the clock: 3 seconds into the 10-to-20 second bucket, it has seen only 3 seconds of data and reports at second 20. A sliding window is anchored to now: it always covers the previous N seconds. Three failed logins at 9:58 and three at 10:02 fall into different 10-minute tumbling windows, but a 10-minute sliding window at 10:02 sees all six.

Sources (Azure Stream Analytics query docs): [Windowing overview](https://learn.microsoft.com/stream-analytics-query/windowing-azure-stream-analytics) · [Hopping window](https://learn.microsoft.com/stream-analytics-query/hopping-window-azure-stream-analytics) · [Sliding window](https://learn.microsoft.com/stream-analytics-query/sliding-window-azure-stream-analytics) · [Session window](https://learn.microsoft.com/stream-analytics-query/session-window-azure-stream-analytics)

### Spark structured streaming

```python
(df.writeStream
   .format("delta")
   .option("checkpointLocation", "Files/checkpoint")
   .outputMode("append")
   .trigger(processingTime="1 minute")
   .toTable("events"))
```

- A checkpoint location is required for fault tolerance.
- Batch writes with `.trigger(processingTime=...)` to produce fewer, larger files. Turn on Optimized Write (`spark.databricks.delta.optimizeWrite.enabled`) or use `partitionBy`, `repartition` or `coalesce`.
- In production, run streams as a **Spark job definition with a retry policy** (up to unlimited retries), not as a notebook.
- The Monitoring hub's Structured Streaming tab shows input rate, process rate, input rows, batch duration and operation duration.

**What a "structured streaming job" is.** From [Data streaming into a lakehouse with Spark](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-streaming-data) and the [streaming quickstart](https://learn.microsoft.com/en-us/fabric/data-engineering/get-started-streaming), opened Nov 16, 2026.

- **Structured streaming** is "a scalable, fault-tolerant stream processing engine built on Spark. It treats a live data stream as a table that new rows are continuously appended to." You write it with `readStream` and `writeStream`. Sources include files (CSV, JSON, ORC, Parquet), Kafka and Azure Event Hubs; the sink Learn covers is a Delta table.
- **A structured streaming job** is that code running continuously. Learn recommends notebooks for developing and testing, and **Spark job definitions** for production: non-interactive, code-oriented tasks that run on a Spark cluster with greater robustness and availability.
- **Retry policy** (Optimization tab on the job definition): restarts the job when it stops unexpectedly. Set a maximum number of attempts or **Allow unlimited attempts**, plus the time between attempts. Learn notes a **90-day lifetime limit** on the retry policy setup: after 90 days it stops working and the job is terminated, and you must restart it manually, which re-enables the policy.
- Learn doesn't explain what the checkpoint stores, and gives no delivery guarantee such as exactly-once.

**Why a stream fills a table with tiny files.** Structured streaming writes in micro-batches: it collects the events that have arrived, processes them, and writes them as new Parquet files. The trigger decides when the next micro-batch starts. With the default trigger, Spark starts the next one as soon as the previous one finishes, so each batch holds only a few events and still writes at least one file. Over days that becomes thousands of tiny files, and every read has to open them all. A `processingTime` trigger makes each batch bigger, and Optimized Write sizes the files without manual `repartition()` or `coalesce()`. In a question, "thousands of small files" plus "default trigger" is the clue to change the trigger.

### Eventhouse and KQL databases

- An Eventhouse is a container for several KQL databases that share capacity. It suits structured, semi-structured (JSON, XML) and free-text data, indexed by arrival time.
- Data policies: **retention** defaults to 3,650 days (1 day to 36,500 days, or unlimited). The **caching** (hot cache) period also defaults to 3,650 days and must be less than or equal to retention.
- **Update policy**: a function runs on each ingestion into a source table and writes the result to a target table, transforming data at ingestion time.
- **Materialized view**: a precomputed, continuously updated aggregation, for example `arg_max` deduplication.
- An Eventhouse suspends when idle and resumes in seconds. **Capacity Planner** keeps it always active or sets minimum capacity by schedule (default minimum 2 CUs).

### Native tables vs OneLake shortcuts vs query acceleration

| Option | Data copied into Eventhouse? | Query speed | Supports update policies and materialized views? | Cost |
|---|---|---|---|---|
| Native table | Yes, ingested | Fastest (indexed, hot cache) | Yes | Ingestion and storage |
| OneLake shortcut (standard) | No; queried with `external_table()` | Slower: network reads, no indexes | No | Query compute only |
| Shortcut with query acceleration | No; caches the last N days (the Hot property) and indexes them | Comparable to ingested data | No (behaves like an external table) | OneLake Premium cache meter plus indexing compute |

- Use query acceleration to query OneLake data at high speed without building ingestion pipelines or copying it, to join history in OneLake with live streams, or to join small mirrored dimension tables.
- Query acceleration limits: up to 900 columns. Parquet files over 6 GB compressed aren't cached. Over 2.5 million data files may not perform well. A schema change needs `.alter external table`.

Sources: [Eventstreams overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview) · [Event processing editor](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/process-events-using-event-processor-editor) · [Windowing functions](https://learn.microsoft.com/en-us/stream-analytics-query/windowing-azure-stream-analytics) · [Hopping](https://learn.microsoft.com/en-us/stream-analytics-query/hopping-window-azure-stream-analytics) · [Sliding](https://learn.microsoft.com/en-us/stream-analytics-query/sliding-window-azure-stream-analytics) · [Session](https://learn.microsoft.com/en-us/stream-analytics-query/session-window-azure-stream-analytics) · [Snapshot (Learn module)](https://learn.microsoft.com/en-us/training/modules/explore-event-streams-microsoft-fabric/4-route-event-data-to-destinations) · [Streaming into a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-streaming-data) · [Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse) · [Data policies](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-policies) · [Query acceleration](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/query-acceleration-overview)

# Domain 3 — Monitor and optimize an analytics solution (30–35%)

This domain covers Part 10 (monitoring and alerts), Part 11 (identify and resolve errors) and Part 12 (optimize performance).

## Part 10 — Monitor Fabric items and configure alerts

The Monitor hub is the starting point for job runs across items. Each workload then has its own deeper view: pipeline run details, Spark monitoring, Eventstream data insights, query insights and workspace monitoring.

### Where to look

| What you monitor | Where | What you see |
|---|---|---|
| Any job run (pipelines, Copy job, Dataflow Gen2, notebooks, Spark job definitions, semantic models, lakehouse jobs) | Monitor hub → Job runs | Status, duration, submitter, run details; filter by time, type, status and workspace. Any user can open it but sees only items they have permission on |
| Pipeline ingestion | Item → View run history, or Monitor hub → run details | Run ID, errors, each activity's input and output (for example `rowsRead`, `rowsCopied`), Gantt view, rerun from the failed activity |
| Dataflow Gen2 | Item → Refresh history | Each refresh with per-query detail and errors |
| Notebook and Spark transformation | Notebook cell monitoring, Spark advisor, Spark application detail page, Spark history server | Job and task progress, executors, cell-level Spark logs, real-time advice and error analysis |
| Eventstream | Select a node → Data insights and Runtime logs tabs (Viewer or higher) | Input and output events, backlogged events, runtime, data conversion and deserialization errors, watermark delay; logs at warning, error and information levels |
| Eventhouse ingestion | Workspace monitoring (EventhouseIngestionResultsLogs) and `.show ingestion failures` | Ingestion successes, failures and error details |
| Warehouse and SQL analytics endpoint queries | `queryinsights` views and DMVs | 30 days of completed query history, long-running and frequent queries |
| Semantic model refresh | Monitor hub (semantic model runs), the model's refresh history, a pipeline's Output tab | Refresh status, duration and errors |

### Monitor semantic model refresh

- Pipelines can refresh a model with the **Semantic model refresh** activity. It can refresh selected tables or partitions instead of the whole model.
- Its settings include **Wait on completion** (on by default), max parallelism, retry count, timeout, and commit mode (**Transactional** or **Partial Batch**).
- Watch the run in the pipeline's Output tab or the Monitor hub.

### Query insights (Warehouse and SQL analytics endpoint)

- Six views in the `queryinsights` schema: `exec_requests_history`, `exec_sessions_history`, `long_running_queries`, `frequently_run_queries`, `sql_pool_insights` and `external_api_call_stats`.
- History covers **30 days** of user queries (system queries are excluded). A completed query can take up to **15 minutes** to appear.
- Similar queries are grouped by shape (`query_hash`), even when their filter values differ.
- Admin, Member and Contributor see the full query text. Contributor or higher is needed to use the views.
- A non-zero `data_scanned_remote_storage_mb` means a cold start: data was fetched from OneLake instead of cache.
- Live activity: `sys.dm_exec_connections`, `sys.dm_exec_sessions` and `sys.dm_exec_requests`.

### Workspace monitoring

- It creates a read-only **monitoring Eventhouse** in the workspace that collects logs and metrics from the workspace's items. You query it with KQL.
- It keeps **30 days** of data and consumes capacity.
- To turn it on, a Fabric admin enables the tenant setting "Workspace admins can turn on monitoring for their workspaces". Then a workspace **Admin** opens Workspace settings → Monitoring → + Eventhouse.
- A workspace can use workspace monitoring or Log Analytics, not both.

### Configure alerts

- **Activator** watches event streams or Power BI data and acts when a condition is met. Actions: email, Teams message, run a pipeline, notebook, Spark job or function, or a Power Automate or custom action.
- **Alert on a failed job**: Real-Time hub → Fabric events → Job events (or workspace item events) → Set alert, then pick the condition and action.
- **Pipeline schedule failure notifications** email chosen users or groups when a **scheduled** run fails.
- The Monitor hub's **Alerts** page sets who is notified about job failures and other job events.

**Monitor hub job alerts: two types, easy to confuse.** From [Set up job alerts in the Monitor hub (preview)](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub-alerts) and [Create alerts for pipeline runs](https://learn.microsoft.com/en-us/fabric/data-factory/create-alerts-for-pipeline-runs), opened Nov 7, 2026.

|  | Schedule failure emails | Activator-based alert rules |
|---|---|---|
| Cost | Free | Paid (menu says "Alerts (paid)"), billed under Activator capacity usage |
| Events | A scheduled job fails. Scheduled runs only, not manual runs | Started, Succeeded and others (full list not given) |
| Items | Items that support schedules | Pipeline, Spark job, notebook, user data function, warehouse, lakehouse, mirrored database, SQL database, KQL database |
| Needs | An item that supports schedules | Workspace monitoring (not available in some regions) |
| Who can configure | At least Contributor, or Write on the item | Workspace Owner or Contributor |
| Channel | Email | More job events and richer notifications |

- Failure email recipients must be users or groups in your Entra tenant, including B2B guest users. Direct external email addresses aren't supported. Learn states no recipient rule for Activator-based rules.
- Activity-level alerts are a different mechanism: add an Outlook or Teams activity after the activity you watch, which needs a pipeline. A Copy job needs no pipeline.
- A pipeline's own schedule also has Failure notifications (Home, Schedule) for users or groups.
- Both job-alert types are in preview. Learn gives no rule limits, no alert latency, and doesn't confirm that a Failed event exists for Activator rules.

Note: older versions of the Monitor hub docs state 30 days of history and up to 100 activities per item. The current Job runs page (preview) doesn't list limits.

Sources: [Monitor hub](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub) · [Monitor hub job runs](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub-jobs) · [Monitor pipeline runs](https://learn.microsoft.com/en-us/fabric/data-factory/monitor-pipeline-runs) · [Spark monitoring overview](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-monitoring-overview) · [Monitor an eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor) · [Eventhouse ingestion results logs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/monitor-logs-ingestion-results) · [Query insights](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-insights) · [Semantic model refresh activity](https://learn.microsoft.com/en-us/fabric/data-factory/semantic-model-refresh-activity) · [Workspace monitoring](https://learn.microsoft.com/en-us/fabric/fundamentals/workspace-monitoring-overview) · [Enable workspace monitoring](https://learn.microsoft.com/en-us/fabric/fundamentals/enable-workspace-monitoring) · [Activator](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction) · [Activator tutorial](https://learn.microsoft.com/en-us/fabric/data-activator/data-activator-tutorial) · [Pipeline failure notifications](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs)

## Part 11 — Identify and resolve errors

For each item type, know where the error surfaces first and which documented causes to check. Exam questions usually pair one symptom with one fix.

| Item | Where the error surfaces | Documented causes and fixes |
|---|---|---|
| Pipeline | Run details in the Monitor hub or the Output tab: each activity's error code, failure type and message, plus input and output | Rerun the whole pipeline or from the failed activity; add retry and timeout on the activity; branch on failure and raise your own error with a **Fail** activity; read details with `@activity('X').error.message`. A Copy activity into a **Warehouse** requires staging |
| Dataflow Gen2 | Item → Refresh history (per-query details) | Warehouse destinations need staging and the same workspace. A nullable column detected as non-nullable fails with "We can't insert null data into a non-nullable column". Schema mismatch on a fixed-schema destination fails the publish. Don't delete the workspace's automatically created staging items |
| Notebook | Cell output, Spark advisor (real-time advice and error analysis), cell-level Spark logs, Spark application detail page | Interactive sessions expire after the workspace Spark session timeout (20 minutes by default). Runs past **Set maximum job lifetime** are cancelled. High-concurrency sharing fails when the user, default lakehouse or compute settings differ. Native execution engine falls back to standard Spark automatically for unsupported operations; it doesn't fail |
| Eventhouse | `.show ingestion failures` (management-command ingestion, kept 14 days); workspace monitoring `EventhouseIngestionResultsLogs` (queued ingestion, success and failure) | Read the error code and details per operation; filter with `\| where` or `with (OperationId = ...)` |
| Eventstream | Select the node → Data insights (runtime, data conversion and deserialization errors, backlogged events) and Runtime logs (warning, error, information) | Data conversion errors = output events that don't match the destination schema. Deserialization errors = input the engine can't parse. Messages over 1 MB aren't supported |
| T-SQL (Warehouse) | Query error message; `queryinsights.exec_requests_history`; `sys.dm_tran_locks` | Errors **24556** and **24706**: a snapshot-isolation update conflict. Two transactions ran UPDATE, DELETE, MERGE or TRUNCATE on the same **table** (conflicts are table-level); the first to commit wins. Fix with retry plus exponential backoff and by avoiding concurrent updates to one table. Unsupported syntax: triggers, materialized views, recursive queries, `SET TRANSACTION ISOLATION LEVEL`, distributed transactions, savepoints. Column permission denied = error 230 |
| OneLake shortcut | Access-denied or missing data when reading through the shortcut | Creating one needs Write on the shortcut path **and** Read on the target. Reading needs Read on both paths. The most restrictive side wins. Delegated shortcuts (required for cross-tenant and external sources such as S3 and GCS) use the connection's identity, so check that identity's access. Moving, renaming or deleting the target breaks the shortcut. Names with spaces aren't recognized as Delta tables; `%` and `+` aren't allowed |

Sources: [Monitor pipeline runs](https://learn.microsoft.com/en-us/fabric/data-factory/monitor-pipeline-runs) · [Fail activity](https://learn.microsoft.com/en-us/fabric/data-factory/fail-activity) · [Copy performance (staging into Warehouse)](https://learn.microsoft.com/en-us/fabric/data-factory/copy-performance-sql-databases) · [Dataflow Gen2 destinations](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings) · [Spark monitoring](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-monitoring-overview) · [Workspace admin settings](https://learn.microsoft.com/en-us/fabric/data-engineering/workspace-admin-settings) · [.show ingestion failures](https://learn.microsoft.com/en-us/kusto/management/ingestion-failures) · [Ingestion results logs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/monitor-logs-ingestion-results) · [Monitor an eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor) · [Warehouse transactions](https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions) · [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area) · [Shortcut security](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcut-security)

### Copy activity and pipeline errors: classify the error first

Match the error class to its documented fix before changing any setting. These rows come from Learn pages opened on Nov 6, 2026.

| Error or symptom | Documented cause | Documented fix |
|---|---|---|
| `DWCopyCommandOperationFailed`, or a "transport-level error" (connection forcibly closed, or the connected party did not respond), on a Warehouse destination | The server terminates the connection unexpectedly, usually due to network instability, timeout, or server-side resource limits | Check server logs and network stability. Split the copy into partitions instead of a long-running copy |
| `SHUTDOWN is in progress.` | A SHUTDOWN operation is in progress on the server | Check the server logs to confirm whether a shutdown was initiated, and make sure the server is fully available |
| `LakehouseForbiddenError` | The organizational account doesn't have sufficient permission to access the Lakehouse | Grant the account at least the Contributor role in the workspace that holds the Lakehouse |
| Copy with workspace staging runs longer than 60 minutes | Workspace staging times out after 60 minutes | Use external staging (an Azure Blob Storage or ADLS Gen2 connection) for long-running jobs |
| Copy with Enable staging on and Workspace staging | The pipeline's last modified user needs at least the Contributor role in the workspace | Check that user's workspace role |
| Staged copy with compression and service principal authentication on the staging blob connection | Not supported | Learn gives no workaround |

**Copy activity settings that change the outcome**

- **Fault tolerance** ignores errors such as incompatible rows between source and destination, or a file deleted during the copy. `skipErrorFile` covers `fileMissing`, `fileForbidden` and `invalidFileName`. **Enable logging** logs copied files, skipped files and rows. Learn doesn't say where the logs go or how long they are kept.
- **Data consistency verification** checks file size, last modified date and checksum for binary files. For tabular data it checks that rows read equal rows copied plus incompatible rows skipped. It affects performance. Learn doesn't say whether a failed check fails the run.
- **Activity timeout and retry** (Activity overview): Timeout default is 12 hours, maximum seven days, format `D.HH:MM:SS`. Retry defaults to 1 and the retry interval to 30 seconds.
- **Two Learn pages disagree on the timeout.** The Data Factory limitations page lists "Maximum timeout for pipeline activity runs" as 24 hours for both default and maximum. A value of 24 hours or less satisfies both pages, so avoid an answer that depends on the cap.
- **The connector troubleshooting overview** has no general workflow. It lists per-error causes and recommendations, and some entries have no recommendation.

**Habit (a rule of thumb, not Learn text).** Classify first: a dropped connection means partition the copy, Forbidden means fix the role, a 60-minute staging limit means external staging, and a run that reaches the timeout means the Timeout setting. Retries help intermittent failures. They repeat a deterministic one.

Sources: [Warehouse connector troubleshooting](https://learn.microsoft.com/en-us/fabric/data-factory/connector-troubleshoot-data-warehouse) · [Lakehouse connector troubleshooting](https://learn.microsoft.com/en-us/fabric/data-factory/connector-troubleshoot-lakehouse) · [Connector troubleshooting overview](https://learn.microsoft.com/en-gb/fabric/data-factory/connector-troubleshoot-overview) · [Copy activity](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity) · [Activity overview](https://learn.microsoft.com/en-us/fabric/data-factory/activity-overview) · [Data Factory limitations](https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-limitations)

### Eventstream errors: which tool answers which question

Pick the tool by the question you are asking. These rows come from Learn pages opened on Nov 6, 2026.

| Question | Where to look | Notes |
|---|---|---|
| Is data flowing at a node? | Node status: Active, Inactive, Loading, Error, Warning | Error means paused due to errors. Warning means operational with issues and traffic still occurring |
| Input side or output side? | Select the node, then **Data insights**: Deserialization errors (input events that can't be deserialized inside the engine) vs Data conversion errors (output events that can't be converted to the expected output schema) | Also Runtime errors (total event-processing errors), Backlogged input events, Watermark delay. Per node, for Azure Event Hubs, IoT Hub, lakehouse, eventhouse (event processing before ingestion), derived stream and Activator nodes |
| What does the engine report? | **Runtime logs**: warning, error, information. Filter by keyword, severity or type, then Refresh | For Event Hubs, IoT Hub, streaming connector sources, lakehouse, eventhouse (event processing before ingestion) and Activator nodes. Needs Viewer or higher on the workspace |
| Whole-stream throughput | Select the eventstream node: IncomingMessages, OutgoingMessages, IncomingBytes, OutgoingBytes | Counts and bytes only. They don't say which side fails |
| Kafka, CDC, MQTT or HTTP source | Source Incoming Events, Source Outgoing Events, Connector Errors Logged, Connector Processing Errors, Connector Processing Failures, Connector Events Skipped | Reached through Use external source, then Data insights in live view |
| History, queryable with KQL | Workspace monitoring tables `EventStreamNodeStatus` (about every 6 hours), `EventStreamMetrics` (every minute), `EventStreamErrorMetrics` (every minute; runtime, deserialization and data conversion error counts) | Needs the workspace Admin role, the tenant setting "Workspace admins can turn on monitoring for their workspaces", workspace monitoring on, and **Log Eventstream activity** enabled per eventstream. Preview. Retention not stated |

- Learn doesn't say which cause increments which counter, doesn't explain individual log messages, and gives no retention for runtime logs. It has no metric named data loss.
- Pause and resume: the options are "When streaming was last stopped", "Now" and "Custom time". Eventhouse (Direct Ingestion) and Custom endpoint destinations don't support it. Learn doesn't say whether resuming from an earlier point can re-deliver events.
- On publish, ingestion can start before routing, so data in the gap may not reach the destination (the page's example is a CDC initial snapshot). Fixes: clear **Activate ingestion** and activate it manually after publishing, or resume from a Custom time earlier than the first data.

Sources: [Monitor an eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor) · [Eventstream workspace monitoring](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/fabric-workspace-monitoring) · [Pause and resume data streams](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/pause-resume-data-streams)

### Notebook and Spark errors: capacity and permission

Read the exact error text first, then match it to a row. From the [Data Engineering troubleshooting page](https://learn.microsoft.com/en-us/fabric/data-engineering/troubleshoot-permissions-capacity), opened Nov 6, 2026.

| Error text | Documented causes | Documented fixes |
|---|---|---|
| `HTTP 430 Too many requests for capacity`, `Spark job can't be run because you exceeded a spark compute limit`, `Capacity limit exceeded` | Starting a notebook or Spark job definition while other Spark sessions run and exceed concurrent limits; large ETL beyond the SKU's Compute Units; orphaned or stalled sessions; SKU too small | Turn on **Autoscale Billing for Fabric Spark** (Capacity settings, Fabric capacity) and set the Maximum CU: Spark jobs then stop consuming the capacity's CUs and you pay only for CUs used up to the maximum. Check active and queued jobs on the Spark settings Jobs tab. Use the Capacity Metrics app (Compute, Timepoint, Throttling). Stagger jobs and stop stalled sessions. To clear orphaned sessions, restart the capacity and wait about 10 minutes. If throttling persists, move to a larger SKU |
| `HTTP 429 Too Many Requests`, `API Rate Limit Exceeded` | Looping over lakehouse metadata calls such as `ListTables` or `GetTable`; concurrent processes on the same items; no retry or backoff | Exponential backoff (1 s, 2 s, 4 s, 8 s) with jitter, respect `Retry-After`, cap retries. Reduce call frequency, cache, batch |
| `User is not authorized. User requires at least 'ReadAll' permission on the artifact` | Running a notebook or Spark job against a lakehouse without the item permission | On the item, Manage permissions: **ReadAll** = read all data using Apache Spark; **ReadData** = read all data using SQL; **Read** = Power BI metadata access. Users who need both SQL and Spark need both. Log out and back in |
| `403 Forbidden`, `Authentication Failed`, `Unauthorized To Access Table Files` | Workspace role below Contributor for most operations; missing Storage Blob Data Contributor or Reader on ADLS or OneLake storage; expired, invalid or wrong-scope token; stale external shortcut credentials | Add the user as Contributor, Member or Admin; assign the storage role; use scope `https://storage.azure.com/` for OneLake and Storage and `https://api.fabric.microsoft.com/` for Fabric APIs; refresh tokens before long operations; update shortcut credentials |
| `Capacity Not Active at Lakehouse Refresh` | Capacity unassigned, paused or suspended, or the workspace moved to a trial or free tier | Confirm the capacity is active and assigned (Workspace settings, License Info); check the tenant setting "Users can create Fabric items" |

- 430 and 429 are different errors with different fixes. Backoff doesn't fix a capacity limit, and Autoscale Billing doesn't fix an API rate limit.
- Fabric uses bursting and smoothing for temporary spikes. Sustained overload triggers throttling.
- Learn doesn't state concurrent Spark job limits, queue sizes, throttling thresholds or SKU CU capacities. It doesn't define what Viewer can't do, and doesn't say how long permission changes take beyond logging out and back in.

Source: [Troubleshoot permission and capacity errors in Data Engineering](https://learn.microsoft.com/en-us/fabric/data-engineering/troubleshoot-permissions-capacity)

## Part 12 — Optimize performance

Lakehouse tables need maintenance you run yourself (OPTIMIZE, V-Order, VACUUM). The Warehouse compacts its own files automatically, so tuning there is mostly about data types, statistics and batch loading.

### Optimize a Lakehouse table

- **V-Order** is a write-time Parquet layout for faster reads. Writes are about 15% slower on average, compression can improve by up to 50%, and files stay standard Parquet.
- V-Order is **off by default in new workspaces** (`spark.sql.parquet.vorder.default=false`). Turn it on per session with that setting, per table with `TBLPROPERTIES("delta.parquet.vorder.enabled" = "true")`, or per write with the `parquet.vorder.enabled` option. A session set to true overrides table and write settings of false.
- Changing V-Order affects only future writes. Rewrite existing files with OPTIMIZE.
- **OPTIMIZE** compacts small files into larger ones. Add `VORDER` to apply V-Order, or `ZORDER BY (col)` to cluster rows by columns that filters use often. Liquid clustering is the alternative for evolving layouts.
- **VACUUM** deletes unreferenced files older than the retention threshold, **7 days by default**. Portal and API requests under 7 days fail unless `spark.databricks.delta.retentionDurationCheck.enabled=false`. Shorter retention removes time travel and can break concurrent readers.
- Run maintenance from Lakehouse explorer (table → **Maintenance**), from a notebook, from the REST API, or on a schedule with the pipeline **Lakehouse Maintenance** activity (preview). Runs appear as `TableMaintenance` in the Monitor hub.
- **Optimized Write** (`spark.databricks.delta.optimizeWrite.enabled`) produces larger, fewer files at write time.
- Partition on low-cardinality columns such as year or date. Use Z-Order for high-selectivity filter columns.
- Maintenance (OPTIMIZE, VACUUM) applies only to Delta tables. Legacy Hive tables in Parquet, ORC, AVRO or CSV are not supported. Run it after major ingestion or updates, or when many small files slow reads.
- Source: [Delta table maintenance](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance)

### Optimize Spark performance

| Resource profile | Use for | Key settings |
|---|---|---|
| `writeHeavy` (default for new workspaces) | Ingestion and ETL | V-Order off; Optimized Write unset; bin size 128 |
| `readHeavyForSpark` | Repeated Spark reads | Optimized Write on; bin size 128 |
| `readHeavyForPBI` | Power BI over Delta | V-Order on; Optimized Write on; bin size 1 GB |
| `custom` | Your own mix | Anything you set |

Set a profile with `spark.fabric.resourceProfile` in an Environment, or at runtime with `spark.conf.set(...)`. The runtime setting wins.

- **Native execution engine** (Velox and Gluten, vectorized C++): turn it on in Environment → Spark compute → Acceleration, or with `"spark.native.enabled": "true"` in `%%configure`. It needs Runtime 1.3 or 2.0 and accelerates Parquet, Delta and CSV. It falls back to standard Spark automatically for unsupported work: structured streaming, JSON and XML, and ANSI mode on Runtime 1.3. Python and Scala UDFs and complex types are now supported. Operators it ran show names ending in `Transformer` in the query plan.
- **High concurrency** shares one session across notebooks and bills only the session starter; custom pools in high concurrency mode start up to 36 times faster.
- For predictable startup, use a custom live pool; custom pools otherwise take about 3 minutes to start.
- High concurrency shares a session only within one user, with the same default lakehouse configuration and the same Spark compute settings. The default is 5 notebooks per session. Raise it up to 50 with spark.highConcurrency.max in the attached Environment.
- Starter pools support only Medium nodes (8 vCores, 64 GB) and start in 5 to 10 seconds with default settings and no libraries. Libraries add 30 seconds to 5 minutes (Quick mode) or 1 to 3 minutes (Full mode). Choosing a different node size or customizing compute uses on-demand startup, which takes 2 to 5 minutes.
- An idle session expires after 20 minutes by default. The pool is deallocated if it is unused for 2 minutes after that.
- Sources: [High concurrency mode](https://learn.microsoft.com/en-us/fabric/data-engineering/high-concurrency-overview) · [Apache Spark compute](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)

### Optimize a data warehouse

- Statistics are created automatically. `CREATE STATISTICS` and `UPDATE STATISTICS` (single-column) help after large loads.
- Use the smallest fitting data types: `varchar(n)` rather than `varchar(max)`, integers rather than `decimal`, and `NOT NULL` where possible. Spark strings without a length arrive as `varchar(8000)`.
- Avoid trickle INSERT, UPDATE and DELETE; batch them. For COPY INTO, aim for files of 100 MB–1 GB, many files, and parallel COPY INTO statements into different tables.
- Compaction runs automatically in the warehouse, not in a lakehouse.
- Data clustering in `CREATE TABLE` or CTAS enables file skipping on filtered columns.
- V-Order is on by default in a warehouse. If you disable it, you can't turn it back on.
- The first run of a query can be slow (a cold start); judge performance on later runs.
- For the "non-scalable operation" warning, filter more data out or add `OPTION (FORCE DISTRIBUTED PLAN)`.
- Zero-copy table clones copy only metadata and keep RLS, CLS and DDM.

### Optimize a pipeline

| Setting or limit | Value |
|---|---|
| ForEach parallelism (batch count) | Default 20, maximum 50; tick **Sequential** to process items one at a time |
| ForEach items | Up to 100,000 |
| Activities per pipeline (including inner activities) | 120 |
| Lookup activity items | 5,000 |
| Maximum activity run timeout | 24 hours on the limits page, but the Activity overview page says default 12 hours and maximum 7 days (Learn pages disagree) |
| Concurrent Web, Stored procedure, Lookup and GetMetadata runs | 100 per workspace for each group |

- Copy activity: **Intelligent throughput optimization** (Auto, Standard, Balanced, Maximum) and **Degree of copy parallelism** (Auto or a maximum). Use partition options on large SQL sources. Staging is required when the sink is a Warehouse.

### Optimize Eventstream and Eventhouse

- **Eventstream event throughput** setting: Low, Medium or High. Higher settings start the processor at a higher capacity-unit rate (Low starts at one-third of the base rate). Processor consumption depends on throughput, processing complexity and the input partition count.
- **Eventhouse caching policy** keeps recent data on local SSD (hot cache). A longer hot period makes queries faster but costs more storage. The cache period must not exceed the retention period.
- Precompute frequent aggregations with **materialized views**. Transform once at ingestion with **update policies** rather than at every query.
- Use **query acceleration** for OneLake shortcuts you query often.
- Use **Capacity Planner** for latency-sensitive workloads so the Eventhouse doesn't suspend.

**Optimization rules from practice questions.** Sources opened Nov 13, 2026: [Eventstream settings](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/configure-settings), [Autotune](https://learn.microsoft.com/en-us/fabric/data-engineering/autotune), [Warehouse performance guidelines](https://learn.microsoft.com/en-us/fabric/data-warehouse/guidelines-warehouse-performance), [Copy activity performance](https://learn.microsoft.com/en-us/fabric/data-factory/copy-activity-performance-and-scalability-guide).

*Eventstream throughput*

- Levels: Low is under 10 MB/s, Medium is 10 to 100 MB/s, High is over 100 MB/s.
- An Azure Event Hubs source with fewer than four partitions is limited by its partition count, whatever the level. One partition gives about 9 MB/s.
- To change the level, deactivate the nodes that support pause and resume, update, then reactivate them. Nodes that can't be deactivated, such as a custom endpoint, don't block the change.
- Retention defaults to one day and the maximum is 90 days.

*Spark autotune (preview, off by default)*

- It tunes three settings only: `spark.sql.shuffle.partitions` (default 200), `spark.sql.autoBroadcastJoinThreshold` (default 10 MB) and `spark.sql.files.maxPartitionBytes` (default 128 MB). It doesn't tune executor memory or cores.
- It is compatible with Runtime 1.2 only, and doesn't run in high concurrency mode or with a private endpoint.
- It skips queries shorter than 15 seconds and needs about 20 to 25 runs to settle. Enable it with `spark.ms.autotune.enabled=true`.

*Warehouse*

- V-Order is on by default in every warehouse. Once disabled on a warehouse it can't be re-enabled, so disable it only on a write-only staging warehouse. For Spark in a new workspace the default is the opposite: off.
- A nonzero `data_scanned_remote_storage_mb` in `queryinsights.exec_requests_history` indicates a cold start. Don't judge a query by its first run.
- Top CPU and who ran it: `exec_requests_history` (`allocated_cpu_time_ms`, `login_name`). Slowest by elapsed time: `long_running_queries`.

*Copy activity*

- Lower the Degree of copy parallelism to reduce load on the source or destination machine. Intelligent throughput optimization (Auto, Standard, Balanced, Maximum, or 4 to 256) controls how much compute the service uses.

### Optimize query performance

- T-SQL: select only the columns you need, filter before joins, match data types on join and filter columns, and check `queryinsights.long_running_queries`.
- KQL: filter on the datetime column first, and prefer `has` over `contains` for whole-term searches.
- Lakehouse via SQL endpoint: run OPTIMIZE after big changes, and keep data in the same region as the capacity.

Sources: [V-Order and Delta optimization](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) · [Table maintenance](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance) · [Z-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-lake-z-order) · [Resource profiles](https://learn.microsoft.com/en-us/fabric/data-engineering/configure-resource-profile-configurations) · [Native execution engine](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-overview) · [NEE UDFs and complex types](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-udf-complex-types) · [Warehouse performance guidelines](https://learn.microsoft.com/en-us/fabric/data-warehouse/guidelines-warehouse-performance) · [Pipeline limits](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-limitations) · [Copy performance](https://learn.microsoft.com/en-us/fabric/data-factory/copy-performance-sql-databases) · [Eventstream capacity consumption](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor-capacity-consumption) · [Data policies](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-policies) · [KQL best practices](https://learn.microsoft.com/en-us/kusto/query/best-practices) · [Cross-workload table maintenance](https://learn.microsoft.com/en-us/fabric/fundamentals/table-maintenance-optimization)

# Reference and practice

These parts sit outside the three domains: Part 13 (semantic models) and Part 14 (common traps). The hands-on tutorials and the accuracy notes follow them.

## Part 13 — Semantic models

A semantic model (formerly a dataset) is the Power BI data model that reports and dashboards query. Microsoft defines it as "a logical description of an analytical domain, with metrics, business friendly terminology, and representation", typically a star schema of fact and dimension tables. It holds tables, relationships, calculations and row-level security roles.

### Why use one instead of querying the lakehouse or warehouse directly

- Business logic lives in one place. Measures and relationships are defined once and reused by every report, so numbers do not drift between analysts.
- Relationships let visuals slice and filter correctly. Raw tables do not carry them.
- Row-level security is defined in the model and applies per report user. For Direct Lake on OneLake, SQL-based RLS is not applied, so define RLS in the model.
- Import and Direct Lake use the VertiPaq in-memory engine, built for the aggregations that dashboards run constantly.
- Many reports can share one model.
- If you only need ad-hoc SQL or one simple table, you do not need a semantic model.

### Storage modes

| Mode | Where data lives at rest | Query engine | Refresh | Notes |
|---|---|---|---|---|
| Import | Cached copy inside the model | VertiPaq | Copies the data | Changes show after the next refresh |
| DirectQuery | Source system | Source database | None | Every query goes to the source |
| Direct Lake | Delta tables in OneLake | VertiPaq | Copies only metadata (framing), seconds | Falls back to DirectQuery past SKU limits or with unsupported features |

A Direct Lake model over a warehouse with row-level or column-level security falls back to DirectQuery so the security is enforced.

**Memory picture: the restaurant.** Lakehouse and warehouse tables are the pantry (raw ingredients). The semantic model is the menu and recipe book: named dishes (measures), how ingredients combine (relationships), and who may see which dishes (row-level security). Reports are the diners, and they order from the menu, never from the pantry. A "data model" is the general design idea (tables and keys, usually a star schema). The semantic model is the Fabric item that carries that design plus the business meaning on top. This contrast is a study aid, not a Learn definition.

**Direct Lake has two flavors, and fallback differs.** From [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) and [Semantic models in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-warehouse/semantic-models), opened Nov 16, 2026.

- **Direct Lake on SQL** (through the SQL analytics endpoint): falls back to DirectQuery when it can't load straight from a Delta table, such as a SQL view or a warehouse that uses SQL-based granular access control, and when guardrails are exceeded with fallback enabled (the refresh succeeds with a warning and queries run slower). The model's **Direct Lake behavior** property controls it.
- **Direct Lake on OneLake**: "doesn't fall back to DirectQuery mode via the SQL analytics endpoint." If guardrails are exceeded, the refresh fails and the model can't be queried until the Delta tables are optimized to fit the limits.
- The sentence above about falling back to DirectQuery to enforce row-level or column-level security describes Direct Lake on SQL.

**Default semantic models.** Since September 5, 2025, a default semantic model is no longer created automatically when a warehouse, lakehouse or mirrored item is created. By November 30, 2025, existing default models were disconnected from their item and became independent semantic models. New semantic models on a warehouse or SQL analytics endpoint use Direct Lake mode.

### Does a semantic model persist data?

- Import: yes. The model keeps a full cached copy.
- Direct Lake: no full copy. The model holds metadata and references to the latest Delta files, and data is loaded into memory as queries need it.
- DirectQuery: no. Nothing is stored.

**Import: disk vs memory.** From [Semantic model modes in the Power BI service](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand) and [Large semantic models](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-large-models), opened Nov 16, 2026.

- Imported data is **stored on disk in the semantic model itself**: "imported data is always stored to disk. When queried or refreshed, the data must be fully loaded into memory of the Power BI capacity." A refresh compresses the data and stores it with the VertiPaq engine.
- So memory is a loading step, not the home of the data. The source tables are **not** the fallback copy: the model has its own stored copy and is only as current as its latest refresh. A full refresh removes all data from all tables and reloads it from the source.
- An Import model is never partially loaded: the entire model must be in memory before it can be queried. Direct Lake loads only the data a query needs.
- Premium evicts inactive models from memory to make room for others, and an evicted model is reloaded when someone queries it, which can cause a noticeable delay. Large semantic models page in only the relevant data on demand.
- Learn doesn't state what happens after a capacity restart, or where an evicted model is reloaded from. Reloading from the model's own stored copy is an inference from "always stored to disk".

**Keeping a semantic model current.** From [Data refresh in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data) and [How Direct Lake works](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-how-it-works), opened Nov 16, 2026.

- **Import is a point-in-time copy.** Learn: "Because Power BI copies the data, you must refresh the semantic model to fetch changes from the underlying data sources." Changes in the source do not appear until a refresh. Learn doesn't say whether you can edit data values inside the model; the page covers schema sync only.
- **Ways to refresh an Import model:** scheduled refresh (up to 8 a day on shared capacity, up to 48 a day on Premium, PPU or Fabric capacity), **Refresh now** on the model settings page (on-demand refreshes don't count toward the scheduled limit), the REST API, Power Automate, and the XMLA endpoint (including a single partition). The pipeline Semantic model refresh activity is covered in Part 10.
- **DirectQuery** has no refresh: each query goes to the source. Automatic page refresh works at report page level and is only available for DirectQuery sources.
- **Direct Lake updates itself by default.** The model-level setting **Keep your Direct Lake data up to date** (Refresh section of the model settings) is on by default. When Delta table changes are detected, the model runs a framing operation, only on the tables that changed. Turn it off when an ETL job must finish before consumers see new data. Then refresh manually, on a schedule, or through the REST API or TOM.
- Power BI suspends automatic updates after a non-recoverable error, such as a refresh that keeps failing, and resumes them after the next on-demand refresh finishes without errors.
- Learn doesn't say how changes are detected or how soon framing starts after a change.

**Choosing Direct Lake, Import or DirectQuery.** From [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview), opened Nov 16, 2026.

| If the situation is | Choose | Why (Learn) |
|---|---|---|
| Large data already in OneLake Delta tables, IT-driven, lake-centric | **Direct Lake** | Fast loading into memory, frequent fast refresh, efficient capacity use, fast queries. Useful when copying everything into Import is impractical. |
| Self-service analyst who needs agility, or can't change the lakehouse, or needs Power Query prep | **Import** | Import supports data preparation with Power Query defined in the model. Learn: it "often works well for a self-service analyst". |
| Data isn't a Delta table in OneLake, or you need low latency on a source that supports DirectQuery | **DirectQuery** | It works with any connector that supports DirectQuery and reduces data latency without refresh. The source must handle the query load. |
| Both large lake data and some analyst-added tables | **Composite** (Import and Direct Lake tables together) | Learn: it "offers the scale and flexibility needed for many BI scenarios". |

- Direct Lake needs a **Fabric capacity** (SKU). Import and DirectQuery work with any Fabric or Power BI license. Direct Lake data sources are Fabric items whose OneLake storage resolves to valid Delta tables, natively or through shortcuts.
- Direct Lake on OneLake can't connect to SQL analytics endpoint views, can't use SQL analytics endpoint object-level or column-level security, and has no hybrid tables or user-defined aggregations.
- Why Direct Lake is normally faster than DirectQuery: Direct Lake and Import queries run in the model's VertiPaq engine, while DirectQuery sends each query to the source, and source databases "aren't typically optimized for heavy query load coming from reports".
- Learn recommends a proof of concept before committing to Direct Lake. It gives no numeric size thresholds and no ranking of the modes beyond "normally outperform".

Sources: [Semantic models in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-warehouse/semantic-models) · [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/get-started/direct-lake-overview) · [Semantic models in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-understand) · [Column-level security in Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/column-level-security)

## Part 14 — Common traps

These are the facts that practice questions most often got wrong. Most are exceptions to a general rule, so review them before the exam.

| Area | The fact | See |
|---|---|---|
| Security | Column-level security blocks a column, and a query that touches it fails. Dynamic data masking lets the query succeed with masked values unless the user has UNMASK, and does not stop inference with a WHERE clause. | Part 8 |
| Security | ReadAll is an item permission. DefaultReader is the OneLake security role that grants data access, and its members are everyone with ReadAll. Delete it and those users lose data access. | Part 8 |
| Security | A ReadWrite role has no effect on Admin, Member or Contributor, and it cannot contain row or column rules. | Part 8 |
| Security | OneLake security has only Grant roles. There are no Deny roles. | Part 8 |
| Security | Roles combine as a union, except the SQL analytics endpoint, which intersects column allow lists. If any role hides a column, the endpoint blocks it. | Part 8 |
| Security | Role definition changes take about 5 minutes. Group membership changes take about an hour, and some engines need an extra hour. | Part 8 |
| Ingestion | Mirroring only goes from a supported source into OneLake. It never writes back to the source. | Part 3 |
| Ingestion | Mirroring includes 1 TB of free storage per capacity unit (F64 = 64 TB). Replication compute is free and uses no capacity. | Part 3 |
| Ingestion | Mirrored databases created in the portal default to 1 day of retention. Older ones default to 7 days. | Part 3 |
| Ingestion | In a Copy job, watermark incremental copy captures only inserts and updates. CDC captures deletes too and supports SCD Type 2. | Part 3 |
| Streaming | A hopping window with size 30 and hop 10 puts each event in three windows. If the hop is larger than the size, events in the gaps are never counted. | Part 6 |
| Streaming | A session window closes after a quiet gap. Use it for bursts of activity per key. Tumbling windows cannot do this. | Part 6 |
| Delta | VACUUM keeps 7 days by default. Portal and API requests under 7 days fail unless spark.databricks.delta.retentionDurationCheck.enabled is false. | Part 12 |
| Delta | Lakehouse maintenance (OPTIMIZE, VACUUM) works only on Delta tables, not legacy Parquet, ORC, AVRO or CSV tables. | Part 12 |

**Traps from the practice questions**

| Area | The fact | See |
|---|---|---|
| Security | ReadData is not Read. In the item permissions table, ReadData sees no item metadata, sees SQL data only in Delegated mode, and sees no OneLake data. Read sees metadata but no SQL or OneLake data. | Part 8 |
| Ingestion | A Dataflow Gen2 Warehouse destination needs a fixed schema, staging, and the same workspace as the dataflow. Automatic settings apply only to Lakehouse and Azure SQL and drop and recreate the table on every refresh. | Part 3 |
| Errors | A `DWCopyCommandOperationFailed` transport-level error is a dropped connection. Learn's fix is to check server logs and network stability and split the copy into partitions. | Part 11 |
| Errors | Workspace staging times out after 60 minutes. Learn recommends external staging for long-running jobs. | Part 11 |
| Errors | Eventstream: Data conversion errors are output events that can't be converted to the expected schema. Deserialization errors are input events the engine can't deserialize. Viewer is enough for Data insights and Runtime logs. Workspace monitoring needs Admin. | Part 11 |
| Timeouts | Learn pages disagree. The Activity overview says default 12 hours and maximum 7 days. The Data Factory limitations page says 24 hours. | Parts 11, 12 |
| Governance | A sensitivity label does not survive export to .csv or .txt. Mandatory labeling is not enforced for lakehouses, pipelines or warehouses: the user can save without a label unless the experience itself requires one. | Part 8 |
| Governance | Downstream inheritance runs Power BI to Power BI, Fabric to Fabric and Fabric to Power BI. It does not run Power BI to Fabric. Items autogenerated from a lakehouse take the lakehouse's label, not one from further upstream. | Part 8 |
| Errors | HTTP 430 (capacity exceeded) and HTTP 429 (API rate limit) are different errors. 430: Autoscale Billing for Fabric Spark, job monitoring, Capacity Metrics app, staggering jobs. 429: exponential backoff with jitter and Retry-After. | Part 11 |
| Security | A Spark notebook error that names ReadAll needs the ReadAll item permission (Spark). ReadData is the SQL permission. Someone needing both needs both. | Parts 8, 11 |
| Alerts | Free schedule failure emails fire for scheduled runs only, and recipients must be Entra users, groups or B2B guests (no direct external addresses). Activator alert rules are paid and need workspace monitoring. Configuring failure emails needs Contributor or Write on the item. | Part 10 |
| Ingestion | Copy job watermark incremental copy captures inserts and updates, and a datetime column is a supported watermark. Default update method is append, which keeps history and duplicates updated rows. Merge uses the primary key. CDC needs CDC enabled on the source and is Preview. A failed run doesn't change the Copy job's state: the next run resumes from the last successful run. | Part 3 |
| Security | Creating a shortcut needs Write on the item where it is created plus Read on the target; Admin, Member and Contributor also need target Read. T-SQL in Delegated identity mode reads a same-tenant OneLake shortcut as the item owner; User's identity mode uses the caller. | Part 8 |
| Ingestion | Dataflow Gen2 incremental refresh replaces changed buckets inside a fixed look-back window. It needs the replace update method and a fixed schema, and OPTIMIZE isn't supported on that lakehouse table. Limits are 50 buckets per query and 150 per dataflow. A forward-moving watermark is the Copy job model. | Part 3 |
| Streaming | An eventstream SQL operator windows on arrival time unless the query says TIMESTAMP BY a field. A requirement to use the device's own timestamp means TIMESTAMP BY. A SQL operator also needs new destination nodes. | Part 6 |
| Streaming | Eventstream no-code operators: Union combines streams that share fields, Expand makes one row per array element, Join pairs two streams on a condition, Manage fields only adds, removes, renames or retypes fields. | Part 6 |
| Ingestion | Dataflow Gen2 never recreates an existing table it didn't create if you delete it. KQL database and Azure Data Explorer destinations don't support replace. Automatic settings cover Lakehouse, Azure SQL Database and Snowflake, not Warehouse. | Part 3 |
| Optimize | Autotune tunes only three Spark settings, runs only on Runtime 1.2, and not in high concurrency mode. Warehouse V-Order can't be re-enabled once disabled. An eventstream's throughput level can't beat an Event Hubs source with fewer than four partitions. | Part 12 |
| Errors | Warehouse error 24556 or 24706: write conflicts are detected at table level even when the rows differ. Fix by not running UPDATE, DELETE or MERGE concurrently on one table, or retry with backoff. Distributed transactions aren't supported and isolation-level changes are ignored. | Part 11 |
| Alerts | Often missed: free schedule failure emails cover failures only. An alert on Succeeded or Started needs an Activator rule, which needs workspace monitoring. | Part 10 |
| Governance | Often missed: a label never flows from a Power BI item to a Fabric item. Memory aid: labels follow the data downstream, and a lakehouse sits upstream of a semantic model. An autogenerated SQL analytics endpoint takes its parent lakehouse's label. A .csv or .txt export carries no protection. Mandatory labeling isn't enforced for lakehouses, pipelines or warehouses. | Part 8 |
| Security | The default() mask shows a number as 0, a string as XXXX and a date as 1900-01-01. A range filter in WHERE still returns the matching rows, so the real value can be inferred; combine masking with column-level and row-level security. | Part 8 |
| Security | Connecting a workspace to a Git repository is Admin only. A Viewer can read lakehouse and warehouse data with T-SQL (ReadData) but not through Spark or OneLake APIs (ReadAll). | Part 8 |
| Workspace settings | Two similar names. Customize compute configurations for items (workspace Admin, Pool tab) lets an environment set driver and executor size per item. Customized workspace pools (capacity admin, on by default) allows custom pools at all. A domain contributor assigns their own workspaces from workspace settings and has no Domains tab; a domain admin works in the admin portal. | Part 2 |
| Security | Column-level security doesn't hide a column, it denies it. SELECT * fails with Msg 230 (SELECT permission denied on the column); the user must name only the granted columns. Masking is the feature that returns rows with altered values. | Part 8 |
| Security | With OneLake security on, ReadAll gives data access only through the DefaultReader role. Delete DefaultReader and ReadAll users lose access until added to another role. Admin, Member and Contributor keep access through their Write permission. Across roles, row filters combine with OR; column rules combine as a union except at the SQL analytics endpoint, where any role that hides a column blocks it. | Part 8 |
| Lifecycle | Deployment rules by item: a notebook supports only a default lakehouse rule. Data source and parameter rules are for semantic models and Dataflow Gen1. Rules are created in the target stage by the item owner, never in the development stage, and apply from the next deployment. | Part 9 |
| Governance | Endorsement: anyone with write permission can promote. Only admin-specified users can certify or mark master data. Master data applies only to items that contain data, such as lakehouses and semantic models. Dashboards can't be promoted or certified. | Part 8 |
| Mock 1: ingestion | An Azure SQL database can't be mirrored while CDC is enabled on it, and only a writable primary can be mirrored. Mirroring types: database mirroring copies the data, metadata mirroring leaves it in the source (Snowflake, Databricks), open mirroring means writing your own application. COPY INTO file types are CSV, JSONL and PARQUET only. In a lakehouse, shortcuts go at the top level of Tables, or at any level of Files. | Part 3 |
| Mock 1: often missed | Three facts that were easy to miss more than once. Dataflow Gen2 incremental refresh needs replace AND a fixed schema. A KQL update policy with a 0s soft-delete on the source must be transactional. Deleting DefaultReader removes access for ReadAll users, while Admin, Member and Contributor keep it. | Parts 3, 6, 8 |
| Mock 1: monitor and optimize | Throttling by future capacity used: up to 10 minutes nothing, 10 to 60 minutes a 20-second delay on interactive requests, 60 minutes to 24 hours interactive rejected, over 24 hours everything rejected. HTTP 429 is an API rate limit (back off and retry); HTTP 430 is Spark capacity (Autoscale Billing). The native execution engine falls back for JSON, XML and structured streaming. A default domain never overrides a workspace's existing domain. | Parts 11, 12 |

**Traps from Mock 2**

| Area | The fact | See |
|---|---|---|
| Security | Trusted workspace access works only for OneLake shortcuts, pipelines, semantic models, the T-SQL COPY statement and AzCopy. A Spark notebook that reads a firewall-protected storage account directly needs a managed private endpoint, which a workspace admin creates. Trusted workspace access needs an F SKU, not a trial capacity. | [Trusted workspace access](https://learn.microsoft.com/en-us/fabric/security/security-trusted-workspace-access) · [Managed private endpoints](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview) |
| Ingestion | Dataflow Gen2 incremental refresh has two bucket limits, and both must hold: 50 buckets per query and 150 buckets per dataflow. For example, 3 queries × 45 buckets fits, but 4 × 40 breaks the dataflow limit. It also needs the replace update method and a fixed schema. | Part 3 · [Incremental refresh](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh) |
| Ingestion | With a dynamic schema, a Dataflow Gen2 refresh that finds a schema difference drops and recreates the destination table, which can remove relationships and measures added to it. A fixed schema keeps them and makes the publish fail on a mismatch instead. | Part 3 · [Data destinations](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-data-destinations-and-managed-settings) |
| Errors | Warehouse error 24556 (snapshot isolation update conflict): the documented fix is to retry the failed transaction and avoid concurrent writes to the same table. Setting another isolation level is ignored, because the warehouse always uses snapshot isolation. | Part 11 · [Transactions](https://learn.microsoft.com/en-us/fabric/data-warehouse/transactions) |

**Traps from Mock 3**

| Area | The fact | See |
|---|---|---|
| Ingestion | Often missed: an Azure SQL database can't be mirrored while CDC is enabled. Disable CDC first, then create the mirrored database. Mirroring's replication compute is free and doesn't consume capacity. | Part 3 · [Azure SQL mirroring limitations](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-limitations) |
| Streaming | When an eventstream with a CDC source is published, part of the initial snapshot can stay in the eventstream and never reach the destination. Clear **Activate ingestion** on the Lakehouse or Eventhouse (event processing before ingestion) destination before publishing, then activate it manually with **Custom time** set earlier than the snapshot. | Part 11 · [Eventhouse destination](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-kql-database) |
| Governance | A domain admin can edit the description, name contributors, assign workspaces and override delegated tenant settings such as certification. Only a Fabric admin can rename or delete the domain or add domain admins. A default domain never moves a workspace that already has a domain. | Part 2 · [Domains](https://learn.microsoft.com/en-us/fabric/governance/domains) |
| Orchestration | A Lookup with **First row only** returns `output.firstRow.<column>`; without it, rows are in `output.value` (an array). Inside SQL text, embed values with string interpolation, `'@{activity('X').output.firstRow.Col}'`. A bare `@activity(...)` inside quotes stays literal text, and `@@` escapes to a literal at sign. | Part 7 · [Incremental copy tutorial](https://learn.microsoft.com/en-us/fabric/data-factory/tutorial-incremental-copy-data-warehouse-lakehouse) |
| Streaming | A KQL materialized view created with `backfill=true` must use `.create async materialized-view`. | Part 6 · [.create materialized-view](https://learn.microsoft.com/en-us/kusto/management/materialized-views/materialized-view-create?view=microsoft-fabric) |
| Optimize | To change eventstream throughput, deactivate only the nodes that support pause and resume (for example an Azure Event Hubs source and a Lakehouse destination), change the level, then reactivate them. Custom endpoint sources and Eventhouse direct-ingestion destinations can't be paused. Medium (10–100 MB/s) covers about 40 MB/s; Eventhouse direct ingestion reaches about 50 MB/s at Medium. | Part 12 · [Eventstream settings](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/configure-settings) · [Pause and resume](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/pause-resume-data-streams) |
| Governance | Often missed: downstream inheritance runs Fabric item to Fabric item, Fabric item to Power BI item, and Power BI to Power BI, never Power BI to Fabric. It never overwrites a manually applied label or replaces a label with a less restrictive one, even in fully automated mode. | Part 8 · [Information protection](https://learn.microsoft.com/en-us/fabric/governance/information-protection) · [Downstream inheritance](https://learn.microsoft.com/en-us/fabric/governance/service-security-sensitivity-label-downstream-inheritance) |
| Loading | Warehouse IDENTITY columns must be **bigint**. Values are unique but can have gaps and aren't guaranteed sequential. ALTER TABLE can't add an IDENTITY column to an existing table; use CTAS or SELECT INTO. | Part 4 · [IDENTITY columns](https://learn.microsoft.com/en-us/fabric/data-warehouse/identity) |
| Optimize | Often missed: Spark autotune works only on Runtime 1.2, and doesn't run in high concurrency mode or with a private endpoint. | Part 12 · [Autotune](https://learn.microsoft.com/en-us/fabric/data-engineering/autotune) |
| Transform | `GROUP BY ROLLUP (Region, Territory)` returns (Region, Territory), (Region) and the grand total. CUBE also adds a total per Territory. GROUPING SETS lists exactly the groupings you name. | Part 5 · [GROUP BY](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql) |
| Monitor | OneLake diagnostics, turned on by a workspace admin in Workspace settings (OneLake tab), writes data-access events, including API and cross-workspace shortcut access, as JSON files to a lakehouse in the same capacity. The events can be made immutable for a retention period. Purview audit logs record user activities, not file-level OneLake access in your own lakehouse. | Part 2 · [OneLake diagnostics](https://learn.microsoft.com/en-us/fabric/onelake/onelake-diagnostics-overview) |

**Numbers to memorize**

| Topic | Number |
|---|---|
| OneLake security roles | 250 per item (1,000 on request), 500 members and 500 permissions per role |
| OneLake security role changes | About 5 minutes for role definitions, about an hour for group membership |
| Shortcut chain | 5 direct shortcut-to-shortcut links |
| Shortcuts per item / per OneLake path | 100,000 / 10 |
| Unique external connections per item | 100 |
| Shortcut caching | Files over 1 GB are not cached |
| Query acceleration | 900 columns maximum, Parquet files over 6 GB compressed not cached, performance caveat above 2.5 million files |
| Mirroring | 1 TB free storage per capacity unit, changes as fast as every 15 seconds, default retention 1 day for new portal-created databases |
| Stream Analytics window | 7 days maximum size |
| VACUUM retention | 7 days by default |
| High concurrency | 5 notebooks per session by default, up to 50 |
| Spark session | Expires after 20 minutes idle, pool deallocated 2 minutes later |
| Spark capacity | 2 Spark vCores = 1 capacity unit, F64 with 3x burst = 384 Spark vCores |
| Copy activity | Workspace staging times out after 60 minutes, one on-premises gateway per activity |

**Eventstream facts to memorize**

| Topic | Fact |
|---|---|
| Message size and retention | 1 MB maximum message size, 90 days maximum retention |
| Delivery guarantee | At least once, so duplicates are possible |
| Minimum capacity | F4 |
| Source and destination cap | Up to 11 combined, only for a custom endpoint source with custom endpoint and direct-ingestion Eventhouse destinations. Other types don't count |
| Aggregate vs Group by | Aggregate computes on every new event. Group by computes across all events in a time window |
| Union | Keeps only fields that match in name and data type, drops the rest |
| Operators before ingestion | Supported for Lakehouse, Eventhouse (event processing mode), derived stream and Activator. For other destinations, use a derived stream |
| Lakehouse destination | Converts events to Delta tables |
| Eventhouse modes | Direct ingestion for raw events. Event processing before ingestion when you filter or aggregate first, or attach after a derived stream |
| OneLake security role combining | Union across roles, except CLS in the SQL analytics endpoint, which intersects |
| Spark and OneLake security | Environment 3.5 or higher on Fabric runtime 1.3 |
| Spark node sizes | Medium is 8 vCores / 64 GB. X-Large and XX-Large only on non-trial SKUs |

### Reading section: KQL update policies

**What it is.** An update policy is a trigger on a table in an Eventhouse (KQL database). When new data lands in a source table, Azure Data Explorer's engine runs a KQL query over just the newly ingested data and writes the result into a target table. Think of it as an insert trigger that does ETL inside the database. Typical use: land raw events as one string column in a raw table, then parse them into typed columns in a clean table.

**How it works, step by step**

1. Data is ingested or moved into the source table.
2. The policy fires and runs its query on the new extents only, not the whole table.
3. The query output is written into the target table.
4. Both tables can have different schemas, retention policies and other policies.

**What triggers it.** Ingestion (`.ingest` pull or inline), `.set`, `.append`, `.set-or-append`, `.set-or-replace`, `.move extents` and `.replace extents`. It fires when data arrives, not when a policy is created, so existing data is not processed automatically.

**Example**

```kusto
.create table RawLogs (OriginalRecord:string)
.create table CleanLogs (Timestamp:datetime, ThreadId:int, Message:string)

.alter table CleanLogs policy update
@'[{ "IsEnabled": true, "Source": "RawLogs", "Query": "ExtractMyLogs()", "IsTransactional": true, "PropagateIngestionProperties": false}]'
```

**Policy properties**

| Property | Meaning |
|---|---|
| `IsEnabled` | Turns the policy on or off |
| `Source` | Table that triggers the policy |
| `Query` | KQL that produces the rows for the target, usually a stored function |
| `IsTransactional` | Default `false`. If `true` and the policy fails, the source ingestion fails too |
| `PropagateIngestionProperties` | Copies extent tags and creation time to the target. Only applies to ingestion, not `.move extents` or `.replace extents` |
| `ManagedIdentity` | Needed when the query reads other databases or RLS-enabled tables. The identity needs the `viewer` role |

**Transactional or not**

| Setting | If the policy fails |
|---|---|
| `IsTransactional: false` (default) | Data lands in the source table only, and the ingestion still succeeds. Target rows are silently missing |
| `IsTransactional: true` | Data goes to neither table and the ingestion fails, so you can retry |

Microsoft recommends `true` in production. A bad query can block ingestion into the source table, and the usual causes of failure are a schema mismatch or a query error. Check failures with `.show ingestion failures | where OriginatesFromUpdatePolicy == true`.

**Rules and limits**

- Source and target tables must be in the same database.
- Query output must match the target in column types and order.
- No cross-cluster or cross-Eventhouse queries, and no callouts (plugins).
- Don't reference the source with a qualified name like `database("X").T`. Use the plain table name.
- You can have several policies on one source table, and their order of execution isn't guaranteed.
- Cascading works (A to B to C). Circular chains are detected at runtime and cut, so data is ingested once per table.
- If a policy query uses `join`, disable streaming ingestion on the source table, and on all upstream tables in a cascade.

**Staging-table pattern (drop the raw data).** Set the source table's soft-delete period to `0s` and make the update policy transactional. The raw data isn't queryable or kept in durable storage. A policy that reads from a `0s` soft-delete table must be transactional.

**Why the staging pattern pairs `0s` soft-delete with a transactional policy.** From [Update policy overview](https://learn.microsoft.com/en-us/kusto/management/update-policy?view=microsoft-fabric) and [Retention policy](https://learn.microsoft.com/en-us/kusto/management/retention-policy?view=microsoft-fabric), opened Nov 15, 2026.

- **Soft-delete period here is a retention setting**, not the soft-delete command or a deleted flag. It is how long data is guaranteed to stay queryable after ingestion. Learn: with a period of `0`, "the ingested data won't be committed to the source table, avoiding the need to persist the data."
- **Transactional** controls what happens when the update policy fails. `false` (default): the data lands only in the source table and the ingestion still succeeds, so the target silently misses rows. `true`: the data goes to neither table and the ingestion fails, so you can retry.
- Put together: with `0s` the source keeps nothing, so a non-transactional failure would leave the rows in neither table while the ingestion looks successful. Learn states the rule ("any update policy referencing this table must be transactional") and that transactional policies avoid losing target data on transient failures. The combined "rows would be gone" reasoning is my reading, not a quoted sentence.
- With `0s`, `Recoverability` can only be `Disabled`. Learn names the staging use: ingest into a table, transform with a transactional update policy, redirect the output to another table.
- A typical scenario in one line: parse at ingestion means an update policy on the target `Events`; raw rows not kept means `0s` on `RawJson`; no loss on a transient failure means `IsTransactional: true`. A materialized view aggregates and doesn't fit.

**"Source table" in an update policy is not Event Hubs.** The outside feed (Event Hubs, an eventstream, a file) is just where data comes from. Learn's `Source` property is "the name of the table that triggers invocation of the update policy". So an Eventhouse update policy involves two tables: the table that data is ingested into first (the policy's source, `RawJson` in Q15) and the table the policy writes to (the target, `Events`). The policy is defined on the **target** table and names the source. You control each table with its own command: the retention (soft-delete) policy on the source table, `.alter-merge table RawJson policy retention softdelete = 0s`, and the update policy on the target table, with `Source`, `Query` and `IsTransactional` in its JSON. Flow: Event Hubs, then the source table, then the policy query, then the target table.

```kusto
.alter-merge table RawLogs policy retention softdelete = 0s
```

**Management commands:** `.show table T policy update`, `.alter table T policy update` (replaces), `.alter-merge table T policy update` (appends), `.delete table T policy update`.

**Exam traps**

- Default is non-transactional, so failures can silently lose target rows.
- A `0s` soft-delete source requires a transactional policy.
- Same database only. Cross-database lookups need `ManagedIdentity` with `viewer`.
- Update policy and materialized view solve different problems. An update policy transforms and routes rows at ingestion into another table. A materialized view keeps an always-fresh aggregation, and `materialized_view("Name")` reads only the already-processed part for speed.

**Materialized view: query by name vs `materialized_view()`.** From [Materialized views overview](https://learn.microsoft.com/en-us/kusto/management/materialized-views/materialized-view-overview?view=microsoft-fabric) and [materialized_view() function](https://learn.microsoft.com/en-us/kusto/query/materialized-view-function?view=microsoft-fabric), opened Nov 15, 2026.

- A view has two parts: the **materialized part** (aggregated rows already processed, one row per group-by combination) and the **delta** (rows newly ingested into the source table that aren't processed yet).
- **Query by name** (`ViewName`): combines the materialized part with the delta at query time. The result is always up to date, but it may not perform best, because the delta is aggregated at query time. Speed depends on the view's age and your filters.
- **`materialized_view("ViewName")`**: reads the materialized part only. Always faster than the full view, but not guaranteed to be the most up-to-date. Learn says to use it "when applicable", for example telemetry dashboards that tolerate some staleness.
- **`materialized_view("ViewName", 10m)`**: the optional `max_age` is the maximum staleness you accept. If the last materialization is newer than now minus `max_age`, you get the materialized part only. Otherwise you get the entire view, identical to querying by name (slower).
- Exam shortcut: need the newest rows, query by name. Fast dashboard where slight lag is fine, `materialized_view()`. Fast but with a staleness cap, `materialized_view()` with `max_age`.

Sources: [Update policy overview](https://learn.microsoft.com/en-us/kusto/management/update-policy?view=microsoft-fabric), [Materialized views overview](https://learn.microsoft.com/en-us/kusto/management/materialized-views/materialized-view-overview?view=microsoft-fabric).

**KQL facts to memorize**

| Topic | Fact |
|---|---|
| Update policy default | `IsTransactional` is `false` |
| Update policy scope | Source and target in the same database |
| Update policy schema | Output column types and order must match the target |
| Update policy cross-database | `ManagedIdentity` with the `viewer` role on the other database |
| Staging pattern | Source soft-delete `0s` plus a transactional policy |
| Materialized view, fast read | `materialized_view("Name")` reads the processed part only |
| Materialized view, cost | Lower source retention if you only need the aggregation |
| Materialized view ingestion rate | Recommended no more than 1 to 2 GB/sec |
| Retention default | `SoftDeletePeriod` is 1,000 years, recoverability enabled |
| Retention recoverability | 14 days, not configurable, managed at database level |
| Retention precedence | A table policy overrides the database policy |
| Retention of 0 | Allowed only at table level, and recoverability must be disabled |

### Reading section: deployment pipelines vs Git integration

They solve different problems and are often used together. **Git integration** versions the *definitions* of items in a workspace (a branch per workspace, commit and update). **Deployment pipelines** promote content *between* workspaces, one per stage (for example Dev, Test, Prod).

|  | Git integration | Deployment pipelines |
|---|---|---|
| Purpose | Source control and collaboration on item definitions | Promote content between environments |
| Unit | One workspace connected to one branch and folder | A fixed set of stages, each with its own workspace |
| Providers or requirements | Azure Repos and GitHub. Tenant admin must enable it | Workspaces must be on a Fabric capacity |
| Moves data? | No. Re-creates item definitions only, not data | No. Only metadata is copied, so refresh models after deployment |
| Who sets it up | Workspace Admin connects. Contributor or Member can commit and update with WRITE on all items. Viewer can do nothing | Pipeline admin. Deploying to an existing stage also needs Contributor on source and target workspaces |
| Rules for environment differences | Not applicable | Data source rules and parameter rules. Parameter rules only for semantic models and dataflows, type `Text`. Direct Lake models don't autobind |
| Key limits | 25 MB file size, 250 character path, 1,000 items per workspace, folders up to 10 levels | 300 items per deployment, stage count and names fixed after creation |

**Git behavior to remember**

- Commit lets you select specific changed items. Update always syncs the entire branch, and only one direction can run at a time.
- If the same item changed in both places, updates are disabled until you resolve the conflict.
- Restoring through Git re-creates an item with a **new item ID**, unlike the recycle bin, which keeps the original ID.
- Checkout a new branch is for when you can't write to the connected branch. Commit to the new branch and merge through a pull request.

**Deployment pipeline behavior to remember**

- You can deploy to any adjacent stage in either direction. Stages match by position, not by name.
- Not copied: data, workspace settings, permissions, and for semantic models the credentials, refresh schedule, role assignments and endorsement settings.
- Autobinding connects a deployed item to its linked item in the target stage. If the linked item is missing in the same workspace, the deployment fails. Use Select related to include dependencies.

**Pipeline scheduling and triggers**

- A schedule needs both a start and an end date, so use a far-future end date such as 01/01/2099 for an open-ended run.
- Failure notification emails apply to scheduled runs only, not on-demand runs.
- Event-based triggers use Eventstreams and Activator, and are stored as a Reflex item. Fabric parameter syntax is `@pipeline()?.TriggerEvent?.FileName`, not the Azure Data Factory `@triggerBody` syntax.
- Interval-based schedules (preview) allow up to 20 per pipeline, and can't be edited. Delete and re-create to change one.

**ALM and orchestration facts to memorize**

| Topic | Fact |
|---|---|
| Deployment pipeline stages | Count and names permanent after creation |
| Deployment limit | 300 items per deployment |
| Parameter rules | Semantic models and dataflows only, parameters of type `Text` |
| Deploy to existing stage | Pipeline admin plus Contributor on source and target |
| Deploy to empty stage | Pipeline admin plus Contributor on source |
| Git connect | Workspace Admin only |
| Git Commit vs Update | Commit selects items. Update syncs the entire branch |
| Git limits | 25 MB file, 250 character path, 1,000 items, 10 folder levels |
| Warehouse time travel | 30 calendar days default, configurable 1 to 120, UTC only, read-only SELECT |
| Pipeline schedule | Start and end date both required. Up to 20 interval-based schedules per pipeline |

Sources: [Deployment process](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/understand-the-deployment-process), [Git integration process](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-integration-process), [Warehouse time travel](https://learn.microsoft.com/en-us/fabric/data-warehouse/time-travel), [Pipeline triggers](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-storage-event-triggers).

### Reading section: Delta MERGE, Warehouse loading and capacity throttling

**Delta MERGE patterns**

- A merge can have any number of `whenMatched` and `whenNotMatched` clauses. All `whenMatched` clauses except the last must have a condition. `whenNotMatched` supports only insert. `whenNotMatchedBySource` supports delete and update, and can't reference source columns.
- **Multiple-match error:** if several source rows match one target row, the merge fails. Deduplicate the source first, for example keep only the latest change per key.
- **Insert-only merge for deduplication:** use only `WHEN NOT MATCHED THEN INSERT`. The incoming batch must also be deduplicated within itself. Adding a date range to the match condition limits the scan.
- **Schema evolution:** set `spark.databricks.delta.schema.autoMerge.enabled` to `true`. Without it, extra source columns are ignored by `updateAll` and `insertAll`.

**SCD Type 2 with MERGE**

1. Stage the updates by unioning two sets: all incoming rows keyed by the business key, and a second copy of the rows that change an existing record, with a NULL merge key.
2. The keyed rows match the current target row, so the matched clause sets `current = false` and `endDate` to the effective date.
3. The NULL-key rows can't match, so the not-matched clause inserts them as the new version with `current = true` and a NULL `endDate`.

**Warehouse ingestion: which option when**

| Option | Choose it when |
|---|---|
| `COPY INTO` | Code-rich, highest throughput, loading CSV, JSONL or Parquet from ADLS Gen2, Blob or OneLake |
| Pipelines | Code-free or low-code, repeated or scheduled, large volumes, full ETL |
| Dataflows | Code-free with custom transformations before loading |
| T-SQL ingestion | `INSERT...SELECT`, `SELECT INTO`, CTAS or `OPENROWSET`, tables in the same workspace |
| BCP API (preview) | Client-side ingestion when you can't stage files first |

- Avoid singleton `INSERT` statements. Use CTAS or `INSERT...SELECT`.
- Keep files at least 4 MB. Prefer ADLS Gen2 over legacy Blob Storage.
- All ingestion writes Parquet with V-Order, and you shouldn't disable it.
- `OPENROWSET` can be slower than querying a table, so ingest repeatedly used data into a table.
- Workspace Identity as the `COPY INTO` credential needs Storage Blob Data Reader on the storage, or Contributor on the source OneLake workspace. The executing user needs at least Viewer on the target workspace and `INSERT` on the target table.

**Warehouse table clones**

- A zero-copy clone copies only metadata and references the same Parquet files in OneLake, so creation is near-instant (`CREATE TABLE AS CLONE OF`).
- After creation the clone is independent. Changes to either side don't affect the other.
- A clone can be taken at the current time or a past point within the retention period (30 days default, 1 to 120 configurable, UTC). It can't go before a schema change.
- It inherits RLS, dynamic data masking, object-level security and key constraints.
- Not supported: cross-warehouse or cross-workspace clones, clones on a Lakehouse SQL analytics endpoint, and cloning a whole warehouse or schema.
- Creating a clone needs Admin, Member or Contributor (not Viewer), `SELECT` on all source rows and columns, and `CREATE TABLE` in the target schema.

**Capacity throttling**

| Future usage | Stage | What happens |
|---|---|---|
| Up to 10 minutes | Overage protection | Nothing is throttled |
| 10 to 60 minutes | Interactive delay | Interactive jobs delayed 20 seconds at submission |
| 60 minutes to 24 hours | Interactive rejection | Interactive jobs rejected, background jobs still start |
| Over 24 hours | Background rejection | All requests rejected |

- Smoothing: interactive operations spread over 5 to 64 minutes, background operations over 24 hours. Timepoints are 30 seconds, so a day has 2,880.
- Throttling is per capacity, and in-flight operations are not throttled. Error code is `CapacityLimitExceeded`.
- Warehouse operations are almost all background. Real-Time Intelligence has no 20-second delay stage, and Eventstreams get reduced CU allocation instead.
- F SKU remedies: temporarily scale up, pause and resume, or enable capacity overage billing (3x the normal rate). Autoscale is a P SKU remedy.
- Smoothing doesn't apply when Autoscale Billing for Spark is enabled.

Sources: [Delta update and merge](https://docs.delta.io/latest/delta-update.html), [Warehouse ingestion](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data), [Warehouse table clones](https://learn.microsoft.com/en-us/fabric/data-warehouse/clone-table), [Fabric capacity throttling](https://learn.microsoft.com/en-us/fabric/enterprise/throttling).

### Reading section: code patterns to recognise

Exam questions show short code and ask which line meets a requirement. You need to recognise these patterns, not write them from memory. Sources opened Nov 12, 2026.

**The same window has different names in each engine.**

| Requirement | Eventstream SQL operator | Spark structured streaming | KQL |
|---|---|---|---|
| Fixed, non-overlapping window | `TumblingWindow(minute, 5)` | `window("event_time", "5 minutes")` | `bin(Timestamp, 5m)` |
| Last 10 minutes, a result every minute (overlapping) | `HoppingWindow(minute, 10, 1)` | `window("event_time", "10 minutes", "1 minute")`. Spark calls this a sliding window | Not covered here |
| Group events that arrive close together | `SessionWindow(...)` with a timeout and a maximum duration | `session_window("event_time", "15 minutes")` | Not covered here |

In Spark the order is window size, then slide. In the SQL operator it is unit, size, then hop. Spark session-window aggregations don't support `update` output mode.

**Spark streaming: late data and duplicates.**

```python
# Allow events up to 10 minutes late, by the event_time column
events.withWatermark("event_time", "10 minutes")

# A: no watermark. Spark keeps every event_id for the life of the query (unbounded state)
events.dropDuplicates(["event_id"])

# B: state is evicted only because the watermark column is in the key.
#    A retry with a different event_time is NOT treated as a duplicate
events.withWatermark("event_time", "10 minutes").dropDuplicates(["event_id", "event_time"])

# C: event_id alone defines a duplicate, and state is kept only for the watermark horizon
events.withWatermark("event_time", "10 minutes").dropDuplicatesWithinWatermark(["event_id"])
```

Learn doesn't say late rows are always dropped: data older than the watermark might still be processed, with no guarantee.

**Warehouse: COPY INTO.**

```sql
-- Parquet, wildcard, caller's Entra identity
COPY INTO dbo.Sales
FROM 'https://myaccount.blob.core.windows.net/mycontainer/folder1/*.parquet'
WITH (FILE_TYPE = 'PARQUET');

-- CSV from OneLake, skip the header row
COPY INTO dbo.Sales
FROM 'https://onelake.dfs.fabric.microsoft.com/<workspaceId>/<lakehouseId>/Files/*.csv'
WITH (FILE_TYPE = 'CSV', FIRSTROW = 2);
```

- `FILE_TYPE` is CSV, JSONL or PARQUET. `FIRSTROW = 2` skips a header.
- `MAXERRORS` (default 0) is the number of rejected rows allowed, and `ERRORFILE` is where rejected rows go. Both are for CSV and JSONL; `MAXERRORS` can't be used with Parquet.
- Parquet column names must match the table exactly; a mismatch loads NULL.
- Cross-item load in one statement: `CREATE TABLE dbo.Orders AS SELECT * FROM SilverLH.dbo.Orders;` The source must be in the same workspace.

**KQL update policy.** The full command and its properties are in the section "Reading section: KQL update policies" above. The pattern to recognise: the policy is defined on the target table, `Source` names the table that triggers it, and `IsTransactional: true` plus a `0s` soft-delete on the source means raw rows are never kept and a failure loses nothing.

Sources: [Stateful structured streaming](https://learn.microsoft.com/en-us/fabric/data-engineering/structured-streaming-stateful-processing) · [COPY INTO](https://learn.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=fabric) · [Ingest data into the Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data) · [SQL operator](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/process-events-using-sql-code-editor) · [Update policy](https://learn.microsoft.com/en-us/kusto/management/update-policy?view=microsoft-fabric)

## Hands-on tutorials

These are Microsoft's official Fabric labs and Learn tutorials, mapped to the parts above. Labs marked **DP-700** are in Microsoft's DP-700 lab list (15 labs, about 9 hours in total). All need a Fabric trial or capacity, and a few steps need tenant admin rights.

**Part 1 — Foundations**

- [Create a Microsoft Fabric Lakehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/01-lakehouse.html) · 30 min · DP-700
- [Discover and connect to data in OneLake](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/25-discover-onelake.html) · 30 min · shortcuts across workspaces, SQL analytics endpoint
- [Analyze data in a data warehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06-data-warehouse.html) · 30 min · DP-700

**Part 2 — Workspace settings** (no official lab; do these in your own workspace)

- Open Workspace settings → Data Engineering/Science → Spark compute; create a custom pool, then turn on high concurrency for notebooks and pipelines ([settings guide](https://learn.microsoft.com/en-us/fabric/data-engineering/workspace-admin-settings))
- Workspace settings → OneLake tab: turn on shortcut caching and set the retention days
- [Create an Apache Airflow job](https://learn.microsoft.com/en-us/fabric/data-factory/create-apache-airflow-jobs), then compare starter and custom pools in Data Factory settings

**Part 3 — Batch ingestion**

- [Ingest data with a pipeline](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/04-ingest-pipeline.html) · 45 min · DP-700
- [Create and use Dataflows (Gen2)](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/05-dataflows-gen2.html) · 30 min · DP-700
- [Load data into a warehouse using T-SQL](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06a-data-warehouse-load.html) · 30 min · DP-700 · cross-database load from a lakehouse
- [Create a Copy job](https://learn.microsoft.com/en-us/fabric/data-factory/create-copy-job) · try incremental copy
- [Mirroring tutorial: Azure SQL Database](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-tutorial) · needs an Azure SQL database

**Part 4 — Loading patterns**

- [Design and implement a dimensional model](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/26-design-dimensional-models.html) · 30 min · star schema plus SCD Type 1 and Type 2
- [Create a medallion architecture in a lakehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/03b-medallion-lakehouse.html) · 45 min · DP-700

**Part 5 — Batch transformation**

- [Analyze data with Apache Spark](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/02-analyze-spark.html) · 45 min · DP-700
- [Use delta tables in Apache Spark](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/03-delta-lake.html) · 45 min · DP-700
- [Transform data with notebooks](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/26c-transform-data-notebooks.html) · 30 min · joins, aggregations, window functions
- [Transform data using dataflows](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/26b-transform-data-dataflows.html) · 30 min
- [Transform data in a warehouse using T-SQL](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/26d-transform-data-tsql.html) · 45 min
- [Query a data warehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06b-data-warehouse-query.html) · 30 min · DP-700

**Part 6 — Streaming**

- [Get started with Real-Time Intelligence](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/07-real-time-Intelligence.html) · 30 min · DP-700
- [Ingest real-time data with Eventstream](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/09-real-time-analytics-eventstream.html) · 30 min · DP-700 · aggregations into an eventhouse
- [Work with data in an eventhouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/12-query-data-in-kql-database.html) · 25 min · KQL and T-SQL over a KQL database
- In the Eventstream lab, add a **Group by** with a tumbling window, then change it to hopping and compare the output

**Part 7 — Orchestration** (extend the Part 3 pipeline)

- Add a Lookup → ForEach → parameterized Copy pattern, then a Notebook activity that returns `notebookutils.notebook.exit()` and an If Condition that reads `output.result.exitValue`
- Add a schedule and a OneLake file event trigger ([steps](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs))

**Part 8 — Security and governance**

- [Secure data in a data warehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06d-secure-data-warehouse.html) · 45 min · DP-700 · DDM, RLS, CLS, GRANT/DENY/REVOKE
- [Secure data access in Microsoft Fabric](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/19-secure-data-access.html) · 45 min · DP-700 · workspace roles, item permissions, OneLake security roles
- [Govern analytics data](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/19b-govern-analytics-data.html) · 30 min · endorsement and lineage
- [Implement row-level security in a warehouse (tutorial)](https://learn.microsoft.com/en-us/fabric/data-warehouse/tutorial-row-level-security)

**Part 9 — Lifecycle management**

- [Implement deployment pipelines](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/21-implement-cicd.html) · 20 min · DP-700
- [Get started with Git integration](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/git-get-started) · connect a workspace to a free GitHub repo, commit, then update
- [Develop warehouse projects in VS Code](https://learn.microsoft.com/en-us/fabric/data-warehouse/develop-warehouse-project)

**Part 10 — Monitoring and alerts**

- [Monitor Fabric activity in the monitoring hub](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/18-monitor-hub.html) · 30 min
- [Monitor a data warehouse](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06c-monitor-data-warehouse.html) · 30 min · DP-700 · DMVs and query insights
- [Use Activator](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/11-data-activator.html) · 30 min
- [Enable workspace monitoring](https://learn.microsoft.com/en-us/fabric/fundamentals/enable-workspace-monitoring) and query its Eventhouse with KQL

**Part 11 — Errors** (no official lab; break things on purpose)

- Run two `UPDATE` statements on the same warehouse table in separate sessions inside open transactions, then commit both and read the 24556 error
- Point a shortcut at a folder, rename the target, and see how the shortcut fails
- In the Eventstream lab, open Data insights and Runtime logs on each node

**Part 12 — Optimization**

- [Optimize lakehouse tables based on health checks](https://learn.microsoft.com/en-us/fabric/data-warehouse/tutorial-conditional-lakehouse-optimization)
- [Use data clustering in a warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/tutorial-data-clustering)
- On a lab table, run Maintenance (OPTIMIZE with V-Order, then VACUUM), and check `SET spark.sql.parquet.vorder.default` before and after

Source: [Microsoft Fabric interactive exercises (DP-700 list)](https://microsoftlearning.github.io/mslearn-fabric/)

## Accuracy notes — outdated claims to watch for

These eight claims show up in older study notes and blog posts, but current Microsoft Learn docs contradict them or add an important qualifier.

| Older notes often say | Current docs say | Source |
|---|---|---|
| queryinsights has **5** views | **6** views: exec_requests_history, exec_sessions_history, long_running_queries, frequently_run_queries, sql_pool_insights, external_api_call_stats | [Query insights](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-insights) |
| Native execution engine does **not** support Python/Scala UDFs; switch to standard Spark | It now supports Python UDFs, Scala UDFs and complex types. Unsupported work (structured streaming, JSON, XML) falls back to standard Spark **automatically**, with no switch needed | [NEE overview](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-overview) |
| Eventhouse: real-time only; no batch PySpark or SQL analytics | Eventhouse and KQL databases offer "Analyze data with" → SQL analytics endpoint (once OneLake availability and schema sync are on) and → Notebook. A Lakehouse is still the right pick for batch PySpark plus T-SQL | [Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse) |
| SDK-style project carries full schema + data and isn't a DAC | SDK-style SQL database projects are schema as code. They build with DacFx into a `.dacpac` and publish with SqlPackage. The docs don't describe them carrying data | [Warehouse development and deployment](https://learn.microsoft.com/en-us/fabric/data-warehouse/development-deployment) |
| V-Order disabled by default (no qualifier) | True for Spark in **new workspaces** (writeHeavy profile). In a **Warehouse**, V-Order is on by default, and once disabled it can't be turned back on | [V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) · [Warehouse performance](https://learn.microsoft.com/en-us/fabric/data-warehouse/guidelines-warehouse-performance) |
| Trigger types: verify Tumbling Window | Fabric pipelines have no tumbling window trigger. The closest equivalent is an **interval-based schedule** (preview): fixed, non-overlapping windows with Window start time and Window end time parameters | [Pipeline runs](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs) |
| Column-level security = DENY SELECT on columns | Microsoft's CLS article uses `GRANT SELECT ON table(allowed columns)`. Querying a column you lack, even via `SELECT *`, returns error 230 | [Column-level security](https://learn.microsoft.com/en-us/fabric/data-warehouse/column-level-security) |
| Monitor hub: 100 activities, 30 days | The current Job runs page (preview) doesn't state limits; older doc versions said 30 days and 100 activities per item. Know both | [Monitor hub job runs](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub-jobs) |

Still correct as of the same check: one OneLake per tenant; shortcut caching excludes ADLS; VACUUM default 7 days; deployment pipelines 2–10 stages; four DDM mask types; high concurrency limited to one user per session.

### Who bypasses what

The same three workspace roles behave differently under each control, which is a frequent exam trap.

| Control | Do workspace Admin, Member and Contributor bypass it? |
|---|---|
| Row-level security (warehouse) | **No.** The policy applies to everyone, including db_owner, unless the predicate lets them through |
| Column-level security (warehouse) | Not stated in the docs; test before relying on it |
| Dynamic data masking | **Yes.** They hold CONTROL, so they see unmasked data |
| OneLake security roles | **Yes.** Their write access overrides OneLake security; only Viewers and item-permission users are filtered |
| Item sharing | Not applicable; they already have access to every item in the workspace |

As of 2026-10-11. Microsoft updates these pages often, so re-check the [official study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) the week before you sit the exam.
