# Day 1 — Implement & Manage: Workspace Config + Lifecycle Management
**Time:** 5–6 hours | **Exam weight:** Part of 30–35%

> ✅ **Fact-checked against live Microsoft Learn docs on 2026-09-06** (skills outline dated July 21, 2026). Corrections applied: "OneLake data access roles" renamed to **OneLake security roles**; shortcut write-through corrected (ADLS Gen2/internal shortcuts ARE writable — only S3/GCS/Dataverse are read-only); Git-sync and deployment-pipeline supported-item lists expanded (they cover far more than notebooks/pipelines/reports now); "database projects" clarified as a **preview**, VS Code–based workflow; autobinding mechanics corrected (it reconnects to an *existing* target-stage item, it does not auto-deploy a missing one); Apache Airflow workspace setting renamed from "Data workflow."

---

## SECTION 1: Workspace Settings Decision Table

The exam loves "a customer needs X — which setting do they configure?" questions.

| Setting Category | What It Controls | Where in Fabric UI | Exam Trigger Words |
|---|---|---|---|
| **Spark workspace settings** | Default Spark pool, runtime version, auto-scale, high concurrency mode | Workspace → Settings → Data Engineering/Science | "optimize notebook execution", "shared Spark sessions", "configure Spark pool" |
| **Domain workspace settings** | Assign workspace to a Fabric domain, inherit domain-level settings | Workspace → Settings → Domain | "data mesh", "group workspaces by business unit", "apply domain governance" |
| **OneLake workspace settings** | Managed/unmanaged items, storage location, cross-workspace access | Workspace → Settings → OneLake | "control where data is stored", "restrict item creation" |
| **Apache Airflow workspace settings** | Airflow environment, starter pool config for running Airflow DAGs as a Fabric item | Workspace → Settings → Apache Airflow Job | "Apache Airflow", "orchestrate external workflows" |

### Key Gotcha: Spark Settings
- **High Concurrency Mode** = ⚠️ **single-user boundary, not multi-user.** One user's own notebooks/pipeline activities share ONE running Spark session (reduces cold start — up to 36x faster). It does NOT let *different* users share a session. Requirements to share: same user + same default lakehouse + same Spark compute settings. Default limit is 5 notebooks per session, configurable up to 50 via `spark.highConcurrency.max` in the attached Environment's Spark Properties. Enable when: **one** user/pipeline runs many notebooks back-to-back or in parallel.
- **Autoscale** ≠ High Concurrency. Autoscale scales nodes up/down. High Concurrency shares a session.
- You can set a **default lakehouse** at workspace level — notebooks in that workspace inherit it automatically.

---

## SECTION 2: OneLake — What You Actually Need to Know

OneLake is the single storage layer for ALL Fabric items. Think of it like one data lake per tenant.

### OneLake Architecture
```
Tenant (OneLake)
 └── Workspace A
      ├── Lakehouse 1  → Tables/ + Files/
      ├── Warehouse 1  → (exposes SQL endpoint, backed by OneLake)
      └── KQL Database → (eventhouse, backed by OneLake)
```

### Shortcuts — Decision Table (This Is Heavily Tested)
Shortcuts let you reference external data without copying it.

| Shortcut Type | Source | Data moves? | Use When |
|---|---|---|---|
| **OneLake shortcut** | Another Fabric item (lakehouse, warehouse) | No | Reuse data across workspaces without duplication |
| **ADLS Gen2 shortcut** | Azure Data Lake Storage Gen2 | No | Existing data in Azure, don't want to migrate |
| **Amazon S3 shortcut** | AWS S3 bucket | No | Multi-cloud, keep data in AWS |
| **Dataverse shortcut** | Microsoft Dataverse | No | Power Platform data in Fabric |
| **Google Cloud Storage shortcut** | GCS bucket | No | Data in GCP |

**Exam gotcha (corrected):** Shortcuts appear as folders in the Lakehouse `Files/`/`Tables/` section. **This is NOT universally read-only** — internal OneLake shortcuts and ADLS Gen2 shortcuts support write-through to the target (if you have write permission on the target, deleting/writing through the shortcut affects the source). Only **Amazon S3, Google Cloud Storage, and Dataverse** shortcuts are read-only. Also, the shortcut type list is bigger than most notes assume — external sources now include ADLS Gen2, Blob Storage, S3, S3-compatible, GCS, Dataverse, Iceberg, OneDrive/SharePoint, and on-premises (via gateway); internal shortcuts can point to lakehouses, warehouses, KQL databases, SQL databases, semantic models, mirrored databases, and mirrored Azure Databricks catalogs.

### OneLake Security (Tested Heavily) — ⚠️ renamed feature
Microsoft renamed this feature. It's now officially **"OneLake security"** (data-plane security), distinct from **workspace roles + item permissions** (control-plane security):
- **Workspace roles** (Admin/Member/Contributor/Viewer) = control plane, coarse-grained access to ALL items in workspace
- **Item permissions** (Read/Write/ReadData/ReadAll via sharing) = control plane, fine-grained per item
- **OneLake security roles** (was called "OneLake data access roles") = data plane — grant Read/ReadWrite access scoped to folders, tables, schemas, **and now also rows and columns directly** (not just folder/file level, and not only via warehouse SQL RLS)
  - Create a role on an item → scope it to data (tables/folders/rows/columns) → assign Entra members
  - Only affects users in the **Viewer** role or with **Read** item permission — Admins/Members/Contributors already have full data access and aren't restricted by these roles
  - Every lakehouse has a built-in **DefaultReader** role you can edit/delete

**Decision: which security layer to use?**
- "User should see all items in workspace" → Workspace role
- "User should see only one lakehouse, not the warehouse" → Item permission (Read/Write)
- "User should see only the Sales table, not HR table" → OneLake security role scoped to that table (works directly in OneLake now, in addition to warehouse SQL RLS)

---

## SECTION 3: Lifecycle Management — Deployment Pipelines

This is a common source of exam questions. Know the flow cold.

### Deployment Pipeline Stages
```
Development → Test → Production   (the default — you can rename/add/remove)
```

Each stage maps to a **separate Fabric workspace**. ⚠️ You choose the number of stages at creation time: **2 to 10 stages**, default 3. Once the pipeline is created, the **number of stages and their names are permanent** — you can't change them later (only a stage's public/private status can change afterward).

### What Can Be Deployed
The supported-item list is large and spans every workload (Lakehouse, Warehouse, Notebook, Pipeline, Dataflow Gen2, Report, Semantic model, KQL database, KQL queryset, Eventhouse, Eventstream, Real-Time Dashboard, Activator, Environment, Spark Job Definition, Mirrored database, SQL database, Variable Library, and more — many Power BI items are preview-only). Don't assume a short fixed list; if a question asks "is X deployable," check the current supported-items page rather than memorizing an old short list.

### Key Rules
1. The pipeline deploys **metadata/definitions**, not the actual data in tables
2. You can set **deployment rules** per stage — e.g., override a data source connection string when deploying to Production
3. **Autobinding** (this is the real, official term): if a report depends on a semantic model, deploying the report **reconnects it to the semantic model already in the target stage, if one exists there**. If the semantic model does **NOT** already exist in the target stage, the **deployment fails** — autobinding does not automatically deploy the missing dependency for you. Use the **Select related** button when deploying to pull in dependencies together, or a **deployment rule** to point at a different target-stage item.
4. A workspace can only belong to ONE deployment pipeline stage

### Exam Scenario Type
> "A data engineer deploys a notebook from Dev to Test. The notebook connects to an ADLS storage account. In Test, it should connect to a different storage account. What should they configure?"

**Answer:** Deployment rules — set a parameter override for the storage connection at the Test stage.

---

## SECTION 4: Version Control in Fabric

Fabric supports Git integration (Azure DevOps or GitHub).

### How It Works
- Connect a workspace to a Git repo branch
- Changes to supported items sync to the repo as JSON/YAML definitions
- You can commit changes from Fabric UI or pull updates from the repo

### What Syncs to Git — ⚠️ list is much bigger than commonly assumed
The supported-items list has grown a lot; don't assume it's just "notebooks + pipelines + a few others." Currently supported (GA unless marked preview) spans every workload:
- **Data Engineering:** Environment, GraphQL, Lakehouse, Notebooks, Spark Job Definitions, User Data Functions
- **Data Factory:** Copy Job, Dataflow Gen2, Pipeline, Mirrored database, Mount ADF, Airflow *(preview)*, dbt Job *(preview)*, Mirrored Snowflake *(preview)*, Operations Agent *(preview)*
- **Real-Time Intelligence:** Activator, Eventhouse, Eventstream, KQL database, KQL queryset, Real-Time Dashboard, Maps, Event Schema Set *(preview)*, Digital twin builder *(preview)*, Anomaly detection *(preview)*
- **Data Warehouse:** Warehouse, Mirrored Azure Databricks Catalog
- **Power BI:** Report, Semantic model, Metrics Set, Org app, Paginated report *(most Power BI items are still preview)*
- **Database:** SQL database, Cosmos database *(preview)*
- **Data Science:** ML experiments/models *(preview)*, Data Agents

NOT synced: data in tables, run history, workspace settings. Supported Git providers: **Azure DevOps, GitHub, and GitHub Enterprise** (all cloud-based only).

### Exam Gotchas on Git
- If a workspace is connected to Git, **workspace roles still control who can commit** — you can't bypass Fabric security via Git
- **Database projects** *(preview)* = SDK-style database projects for a Fabric Warehouse, developed in **VS Code with the MSSQL extension** — define schema objects, build/validate the project, then publish to the warehouse. It's schema-as-code, but it's a specific VS Code project workflow, not just "any SQL script in a repo."
- Conflict resolution: if two people edit the same item, Fabric shows a conflict — you must resolve in the UI, not in the repo directly

---

## SECTION 5: Scenario Questions — Work Through These

**Q1.** ⚠️ *(corrected scenario — the original 10-users version doesn't actually match this answer)* One data scientist needs to run 5 notebooks back-to-back during exploration. Each Spark session currently takes 3 minutes to start. What should they enable to fix this?

<details>
<summary>Answer</summary>

**High Concurrency Mode** in Spark workspace settings. This lets **that one user's own** notebooks share a single live Spark session, eliminating cold start time between their notebooks.

Do NOT confuse with autoscale — autoscale adjusts capacity, it doesn't share sessions. Also note: High Concurrency Mode is a **single-user boundary** — it does NOT let *different* users share one session, so "10 data scientists share a session" is not something HCM does.
</details>

---

**Q2.** A lakehouse in Workspace A needs to expose its `Sales` table to users in Workspace B without duplicating data. What's the most efficient approach?

<details>
<summary>Answer</summary>

Create a **OneLake shortcut** in Workspace B's lakehouse pointing to the `Sales` table in Workspace A's lakehouse. No data is copied. Users in Workspace B query it through the shortcut.

</details>

---

**Q3.** A user must be able to read data from the `HR` table in a lakehouse but must NOT be able to read the `Salary` table. They should have no access to any other items in the workspace. What do you configure?

<details>
<summary>Answer</summary>

Two steps:
1. Grant the user **Read** item permission on the specific lakehouse (not a workspace role, as that would expose all items)
2. Create a **OneLake security role** scoped to the `HR` table only and assign the user to it

Do NOT use workspace role — that gives access to all items. (Note: this feature was previously called "OneLake data access roles" — Microsoft renamed it to "OneLake security" / "OneLake security roles.")

</details>

---

**Q4.** After deploying a pipeline from Dev to Test using a deployment pipeline, the pipeline in Test still points to the Dev database. What's missing?

<details>
<summary>Answer</summary>

A **deployment rule** was not configured. Deployment rules let you override item properties (like connection strings, parameters, data source references) per stage. Add a deployment rule for the pipeline that points its data source to the Test database connection.

</details>

---

**Q5.** A database project is used in a Fabric warehouse. A developer adds a new stored procedure to the SQL script in the Git repo. What happens next to deploy it?

<details>
<summary>Answer</summary>

The developer publishes the database project from the Git repo to the Fabric workspace. The publish operation applies the SQL schema changes (including the new stored procedure) to the warehouse. This is incremental — it only applies changes, not a full drop-and-recreate.

</details>

---

**Q6.** A workspace is connected to a GitHub repo. A team member makes changes to a notebook locally in the Fabric UI. Another team member pulls the latest from GitHub. What does the second team member see in Fabric?

<details>
<summary>Answer</summary>

The second team member sees the **updated version** from the repo if the first member committed their changes. If the first member made changes in Fabric UI but **did not commit**, those changes are only local to their workspace view — the repo and other members don't see them.

Key: Changes in Fabric UI do NOT automatically sync to Git. You must explicitly commit.

</details>

---

## SECTION 6: Hands-On Exercise (Do This in Fabric Trial)

**Goal:** Practice the deployment pipeline flow end-to-end.

1. Create **two workspaces**: `DP700-Dev` and `DP700-Test`
2. In `DP700-Dev`, create a simple Lakehouse called `SalesLH` and add one table (upload a CSV via the Lakehouse UI)
3. Create a **Deployment Pipeline** (under Workspaces → Deployment pipelines → New)
4. Assign `DP700-Dev` to the Dev stage, `DP700-Test` to the Test stage
5. Deploy the `SalesLH` from Dev → Test. Notice what gets deployed (schema/metadata) vs what doesn't (data)
6. Add a **deployment rule** — try overriding a parameter (even a dummy one)
7. In `DP700-Dev`, create a shortcut in the lakehouse pointing to any ADLS Gen2 path (or another OneLake path if you have one)

**What to notice:**
- Data in lakehouse tables does NOT move to Test — only the item definition
- Shortcuts need to be re-pointed in Test if they reference different storage

---

## SECTION 7: Quick-Fire Review (10 Questions)

1. What Spark feature lets multiple notebooks share one session? → **High Concurrency Mode**
2. Does a deployment pipeline move table data from Dev to Test? → **No — metadata/definitions only**
3. What security feature controls access at the folder/table/row/column level within a lakehouse? → **OneLake security roles** (formerly "OneLake data access roles")
4. A shortcut to ADLS Gen2 — can you write data back through it? → **Yes** — ADLS Gen2 and internal OneLake shortcuts support write-through (only S3, GCS, and Dataverse shortcuts are read-only)
5. What is a "database project" in Fabric? → **Preview feature: an SDK-style schema-as-code project for a Warehouse, developed in VS Code and published to the warehouse**
6. A workspace can belong to how many deployment pipeline stages? → **One**
7. Which workspace role gives read-only access to all items? → **Viewer**
8. What do you configure so a pipeline uses a different connection in Production vs Dev? → **Deployment rule**
9. Does committing to Git from Fabric UI require a workspace role? → **Yes — must be Admin or Member to commit**
10. OneLake shortcut from another Fabric workspace — what type is it? → **OneLake shortcut** (not ADLS, not S3)

---

## Tomorrow (Day 2)
**Security & Governance (deep) + Orchestration (Dataflow Gen2 vs Pipeline vs Notebook)**

Focus areas:
- Row-level security in warehouses vs OneLake data access roles
- Dynamic data masking
- Sensitivity labels
- When to choose Dataflow Gen2 vs Data Pipeline vs Notebook for orchestration
- Event-based triggers vs scheduled triggers
