# DP-700 Mock 1 — answer key

**Answers:** 1 C | 2 A | 3 B | 4 D | 5 A | 6 B | 7 D | 8 A | 9 C | 10 B | 11 D | 12 A | 13 C | 14 B | 15 D | 16 A | 17 C | 18 D | 19 B | 20 C | 21 A | 22 D | 23 B | 24 A | 25 C | 26 D | 27 B | 28 C | 29 A | 30 B | 31 C | 32 A | 33 D | 34 B | 35 A | 36 C | 37 D | 38 B | 39 C | 40 A | 41 D | 42 B | 43 A | 44 C | 45 B

Facts were checked against Microsoft Learn on Nov 15, 2026. The [Reading Pack](../reading-pack.md) has the source links and longer explanations.

**Q1 — C.** An Azure SQL database can't be mirrored while CDC is enabled, and only a writable primary can be mirrored.

**Q2 — A.** Fewer than four Event Hubs partitions limits throughput whatever the level.

**Q3 — B.** Column-level security makes a query that names the column fail; the row-level security predicate must allow the Admin, who doesn't bypass it.

**Q4 — D.** A notebook supports only a default lakehouse rule, created in the target stages by the item owner.

**Q5 — A.** Free schedule failure emails go to Entra users, groups and B2B guests. Activator rules are paid and need workspace monitoring.

**Q6 — B.** In a DAG activity, dependencies sets the order, and retry with retryIntervalInSeconds sets the retry.

**Q7 — D.** "@pipeline().parameters.x" returns the value with its type; "@{...}" always returns a string; @@ escapes.

**Q8 — A.** Shortcuts go only at the top level of Tables, but at any level of Files.

**Q9 — C.** Deleting inside a shortcut deletes in the target if you have permission there. Deleting the shortcut removes only the shortcut.

**Q10 — B.** Row-level security, column permissions and masking on the source aren't propagated to the mirrored data.

**Q11 — D.** A KQL database treats a shortcut as an external table, queried with external_table().

**Q12 — A.** Caching covers S3, S3-compatible, GCS and gateway shortcuts; retention is 1 to 28 days; files over 1 GB aren't cached.

**Q13 — C.** 10 to 60 minutes of future capacity is the interactive delay stage: a 20-second delay.

**Q14 — B.** HTTP 429 is an API rate limit: back off with jitter and honor Retry-After. HTTP 430 is the capacity error.

**Q15 — D.** When both sides have content you choose a direction: commit overwrites Git, update overwrites the workspace.

**Q16 — A.** Incremental refresh needs replace and a fixed schema, with at most 50 buckets per query (weekly over 2 years is 104).

**Q17 — C.** Expand creates one row per array value.

**Q18 — D.** A 0s soft-delete on the source requires a transactional update policy, so a failure loses nothing.

**Q19 — B.** dropDuplicatesWithinWatermark with a watermark uses event_id alone and keeps bounded state.

**Q20 — C.** COPY INTO supports CSV, JSONL and PARQUET.

**Q21 — A.** The fact load looks up the surrogate key of the dimension's current version.

**Q22 — D.** materialized_view() reads only the materialized part: cheapest, possibly stale.

**Q23 — B.** Conflicts are detected at table level; run sequentially or retry with backoff.

**Q24 — A.** Completed queries can take up to 15 minutes to appear in query insights.

**Q25 — C.** A VACUUM retention under seven days fails by default.

**Q26 — D.** The native execution engine supports Parquet, Delta and CSV; JSON and XML fall back.

**Q27 — B.** A default domain doesn't override a workspace's existing domain.

**Q28 — C.** Commit needs Contributor (write on all items) plus Contribute permission in Git.

**Q29 — A.** Fabric to Power BI is a supported downstream direction; Power BI to Fabric isn't.

**Q30 — B.** Role definition changes take about 5 minutes; group membership changes about an hour.

**Q31 — C.** HoppingWindow for the overlapping window, TIMESTAMP BY for device time.

**Q32 — A.** Operators before an Eventhouse destination require event processing before ingestion.

**Q33 — D.** Metadata mirroring leaves the data in Snowflake. Open mirroring means writing your own replication application.

**Q34 — B.** SQL database in Fabric: operational, ACID, enforced foreign keys.

**Q35 — A.** KQL database (and Azure Data Explorer) destinations don't support replace.

**Q36 — C.** Autotune adjusts those three Spark settings only.

**Q37 — D.** Warehouse V-Order is on by default, is disabled per warehouse, and can't be re-enabled.

**Q38 — B.** Statistics refresh synchronously at query time; update them after a big load.

**Q39 — C.** Caching policy sets hot data; retention sets queryable data.

**Q40 — A.** Transactional commits all at once; Wait on completion holds the next activity.

**Q41 — D.** Data conversion errors is the output-side metric; Runtime logs give error detail; a Viewer can see both.

**Q42 — B.** Pipeline admin plus at least Contributor in both workspaces.

**Q43 — A.** Write where the shortcut is created, Read on the target.

**Q44 — C.** Customize compute configurations for items lets an environment set driver and executor size.

**Q45 — B.** ReadAll users lose access; Admins, Members and Contributors keep it through their Write permission.
