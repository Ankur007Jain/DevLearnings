# Day 1 — Implement & Manage: Workspace Config + Lifecycle Management
**Time:** 5–6 hours | **Exam weight:** Part of 30–35%

---

## SECTION 1: Workspace Settings Decision Table

The exam loves "a customer needs X — which setting do they configure?" questions.

| Setting Category | What It Controls | Where in Fabric UI | Exam Trigger Words |
|---|---|---|---|
| **Spark workspace settings** | Default Spark pool, runtime version, auto-scale, high concurrency mode | Workspace → Settings → Data Engineering/Science | "optimize notebook execution", "shared Spark sessions", "configure Spark pool" |
| **Domain workspace settings** | Assign workspace to a Fabric domain, inherit domain-level settings | Workspace → Settings → Domain | "data mesh", "group workspaces by business unit", "apply domain governance" |
| **OneLake workspace settings** | Managed/unmanaged items, storage location, cross-workspace access | Workspace → Settings → OneLake | "control where data is stored", "restrict item creation" |
| **Data workflow workspace settings** | Airflow environment, starter pool config for Data Factory workflows | Workspace → Settings → Data workflows | "Apache Airflow", "orchestrate external workflows" |

### Key Gotcha: Spark Settings
- **High Concurrency Mode** = multiple users share ONE Spark session (reduces cold start). Enable when: team of analysts all run notebooks interactively.
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

**Exam gotcha:** Shortcuts appear as folders in the Lakehouse `Files/` section. They are **read-only by default** from the shortcut's perspective — you can't write back through a shortcut to ADLS Gen2.

### OneLake Security (Tested Heavily)
- **Workspace roles** (Admin/Member/Contributor/Viewer) = coarse-grained access to ALL items in workspace
- **Item permissions** = fine-grained, set per item (e.g., give someone ReadData on Lakehouse 1 only)
- **OneLake data access roles** = folder/file level within a lakehouse (new feature, GA as of 2025)
  - Create a role → assign paths (e.g., `/Tables/Sales/`) → assign users
  - This is SEPARATE from workspace roles

**Decision: which security layer to use?**
- "User should see all items in workspace" → Workspace role
- "User should see only one lakehouse, not the warehouse" → Item permission
- "User should see only the Sales table, not HR table" → OneLake data access role (row-level via SQL endpoint = Row-Level Security in warehouse)

---

## SECTION 3: Lifecycle Management — Deployment Pipelines

This is a common source of exam questions. Know the flow cold.

### Deployment Pipeline Stages
```
Development → Test → Production
```

Each stage maps to a **separate Fabric workspace**.

### What Can Be Deployed
- Lakehouses, Warehouses, Notebooks, Pipelines, Dataflows Gen2, Reports, Semantic Models, KQL Databases, Eventhouses

### Key Rules
1. The pipeline deploys **metadata/definitions**, not the actual data in tables
2. You can set **deployment rules** per stage — e.g., override a data source connection string when deploying to Production
3. **Auto-binding**: if a report is bound to a semantic model, deploying the report also deploys the model (unless already exists)
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

### What Syncs to Git
Supported: Notebooks, Pipelines, Dataflows Gen2, Lakehouses (metadata only), Warehouses (metadata), Reports, Semantic models

NOT synced: Data in tables, pipeline run history, workspace settings

### Exam Gotchas on Git
- If a workspace is connected to Git, **workspace roles still control who can commit** — you can't bypass Fabric security via Git
- **Database projects** = a way to define warehouse schema as SQL scripts in a Git repo → deploy as code. Think of it as schema-as-code for your Fabric warehouse.
- Conflict resolution: if two people edit the same item, Fabric shows a conflict — you must resolve in the UI, not in the repo directly

---

## SECTION 5: Scenario Questions — Work Through These

**Q1.** Your team has 10 data scientists all running notebooks simultaneously. Spark sessions take 3 minutes to start. What should you enable to fix this?

<details>
<summary>Answer</summary>

**High Concurrency Mode** in Spark workspace settings. This allows multiple users to share a single live Spark session, eliminating cold start time for each user.

Do NOT confuse with autoscale — autoscale adjusts capacity, it doesn't share sessions.
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
1. Grant the user **ReadData** item permission on the specific lakehouse (not a workspace role, as that would expose all items)
2. Create an **OneLake data access role** scoped to `/Tables/HR/` only and assign the user to it

Do NOT use workspace role — that gives access to all items.

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
3. What security feature controls access at the folder level within a lakehouse? → **OneLake data access roles**
4. A shortcut to ADLS Gen2 — can you write data back through it? → **No — read-only**
5. What is a "database project" in Fabric? → **Schema-as-code (SQL scripts in Git) deployed to a warehouse**
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
