# SQL PR review agent (v1)

A GitHub Actions workflow that reviews the SQL in a pull request against the Jira story it belongs to, and posts the result as one comment on the PR.

**Learned / built:** 2026-11-21

---

## What it does

On every pull request that adds or changes `.sql` files:

1. **Reads the changed SQL.** Lists the PR's `.sql` files with their diffs and reads each full file from the PR head. Handles UTF-16 files saved by SSMS.
2. **Finds the story.** Looks for a Jira key (like `DATA-123`) in the PR title, then the branch name, then the description, and fetches that issue from the Jira REST API.
3. **Runs rule-based checks.** Fast T-SQL heuristics (see [the list](#rule-based-checks)), plus a best-effort offline parse. Free, and they run even with no AI key.
4. **Asks Claude to review.** Sends the story, PR description, rule findings and SQL to the Claude API (default model `claude-opus-5-5`) with a review prompt ([`prompt.md`](prompt.md)).
5. **Posts one comment.** Summary, a story-fit verdict, issues by severity, suggested T-SQL fixes and questions for the author. Later pushes update the same comment instead of adding new ones.

Every step degrades gracefully: no Jira settings means it uses the PR description as the story; no Anthropic key means you get the rule-based checks only.

What it does **not** do yet: run the SQL against a database, or learn from feedback. Both are in [Next steps](#next-steps). It never blocks a merge.

## Files

| Path | What it is |
|---|---|
| `.github/workflows/sql-pr-review.yml` | The workflow. GitHub only runs workflows from this folder, so it lives at the repo root. |
| `sql-pr-review-agent/review_sql_pr.py` | Main script: collect files, fetch story, run checks, call Claude, post the comment. |
| `sql-pr-review-agent/sql_checks.py` | Rule-based T-SQL checks. |
| `sql-pr-review-agent/jira_client.py` | Jira key detection and story fetch (Cloud and Data Center). |
| `sql-pr-review-agent/prompt.md` | The review instructions Claude gets. Edit this to match your team's standards. |
| `sql-pr-review-agent/samples/` | A sample stored procedure and PR description for a test run. |
| `sql-pr-review-agent/tests/` | Unit tests for the checks and the Jira helpers. |

---

## Try it

### 1. Add the Anthropic API key (optional but recommended)

Create an API key in the Claude Console (platform.claude.com), then in this repo go to **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your Claude API key |

Without it, the comment still shows the rule-based checks.

### 2. Open a test pull request

The sample SQL has deliberate problems (wrong date window versus the story, `NOT IN` with a subquery, a non-sargable date filter, `NOLOCK`, `SELECT *`, no paid-status filter), so the review has something to find.

1. Create a branch, for example `feature/data-123-recent-claims`.
2. Copy `samples/sample_member_claims.sql` to any `.sql` path, or edit it.
3. Open a PR and paste `samples/sample_pr_description.md` as the description. It contains the story, so you don't need Jira for the test.
4. Watch the **SQL PR review agent** check, then read the comment on the PR.

The pull request that adds this agent also contains the sample `.sql` file, so the workflow runs on that PR too.

### 3. Connect Jira (optional)

| Name | Kind | Value |
|---|---|---|
| `JIRA_BASE_URL` | secret | e.g. `https://yourcompany.atlassian.net` |
| `JIRA_EMAIL` | secret | Jira Cloud: your Atlassian account email. Leave unset for Jira Data Center. |
| `JIRA_API_TOKEN` | secret | Jira Cloud: an API token from your Atlassian account's security settings. Jira Data Center: a personal access token. |
| `JIRA_PROJECT_KEYS` | variable | e.g. `DATA,ETL`. Only these project keys count, which avoids false matches. |
| `JIRA_EXTRA_FIELDS` | variable | e.g. `customfield_10050`, if acceptance criteria live in a custom field. |
| `JIRA_API_VERSION` | variable | `3` for Cloud (the default when `JIRA_EMAIL` is set), `2` for Data Center. |

With `JIRA_EMAIL` set, the token is sent with basic auth (Jira Cloud). Without it, the token is sent as a Bearer token (Jira Data Center personal access token).

**Network:** GitHub-hosted runners call Jira over the public internet. If your company's Jira is only reachable on the corporate network, this needs a self-hosted runner inside that network.

### Other settings

| Variable | Default | What it does |
|---|---|---|
| `ANTHROPIC_MODEL` | `claude-opus-5-5` | Any current Claude model id. |
| `REVIEW_EFFORT` | `high` | `low`, `medium`, `high`, `xhigh` or `max`. Lower is cheaper and faster. |

Cost: each review is one API call. For a small PR at effort `high` on `claude-opus-5-5` ($4 / $20 per million input / output tokens), expect roughly 10 to 30 cents; that's an estimate, and thinking tokens count as output. Lowering `REVIEW_EFFORT` or choosing a smaller model cuts it.

---

## Run it locally

```bash
cd sql-pr-review-agent
python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # optional; omit for rule checks only
python review_sql_pr.py --local \
  --files samples/sample_member_claims.sql \
  --title "DATA-123 Members with recent paid claims" \
  --branch feature/data-123-recent-claims \
  --body-file samples/sample_pr_description.md
```

It prints the comment it would post. Tests: `python -m pip install pytest && python -m pytest tests -q`.

---

## Rule-based checks

Heuristics on the SQL text after comments and string contents are blanked out. They point at things worth a second look; Claude is told to confirm or dismiss them.

| Severity | Check | Why |
|---|---|---|
| High | `update-without-where`, `delete-without-where` | Changes every row (or every joined row). |
| High | `drop-object` | `DROP TABLE/DATABASE/SCHEMA` on a non-temp object. |
| High | `truncate-table` | Removes every row. |
| High | `hardcoded-password` | `PASSWORD = '...'` in the script. |
| Medium | `nolock-hint`, `read-uncommitted` | Dirty reads. |
| Medium | `not-in-subquery` | `NOT IN (SELECT ...)` returns nothing if the subquery has a NULL. |
| Medium | `at-at-identity` | Can return a trigger's identity; use `SCOPE_IDENTITY()` or `OUTPUT`. |
| Medium | `dynamic-sql-exec` | `EXEC(...)` string execution; prefer `sp_executesql` with parameters. |
| Medium | `ansi-nulls-off` | Deprecated setting. |
| Medium | `open-transaction` | `BEGIN TRAN` with no `COMMIT`/`ROLLBACK` in the file. |
| Low | `select-star` | `SELECT *` (the `EXISTS (SELECT * ...)` idiom is skipped). |
| Low | `non-sargable-predicate` | A function on the left side of a filter, e.g. `WHERE YEAR(col) = 2026`. |
| Low | `cursor`, `sp-prefix`, `transaction-without-try` | Style and robustness hints. |
| Note | `parse-note` | The offline parser (sqlglot, T-SQL dialect) couldn't read a batch. Often a parser limit, not a real error, so these sit in a collapsed section. |

---

## Security and data notes

- The workflow uses `pull_request`, not `pull_request_target`, so pull requests from forks can't read the repo's secrets. On a fork PR the comment can't be posted; the review goes to the job summary instead.
- PR text, the story and the SQL are passed to Claude as data, and the prompt tells it not to follow instructions inside them. The model has no tools, so the worst a malicious PR could do is distort the comment.
- The SQL, the PR description and the Jira story are sent to the Claude API. For company code, check your company's policy on sending code to an external AI service before turning this on there.

## Using it at work (GitHub Copilot company)

The review step is one function, `run_ai_review` in `review_sql_pr.py`, so the model provider can be swapped without touching the rest. Options, depending on what your company allows (check with your GitHub or security admin):

1. **Claude through your company's cloud.** Claude is offered on Microsoft Foundry, Amazon Bedrock and Google Cloud Vertex AI. The Anthropic Python SDK has a client for each (for example `AnthropicFoundry`), so the call stays almost the same.
2. **GitHub Copilot code review** can follow repository custom instructions (`.github/copilot-instructions.md`), so the review standards in `prompt.md` can be reused there. It won't fetch the Jira story by itself, so this workflow's Jira step would still be needed to put the story in front of it.
3. **GitHub Models**, if your organization has it enabled, can be called from Actions with the workflow's token; that needs a small rewrite of `run_ai_review`.

---

## Next steps

1. **Run the SQL safely (the "run the SQL" part of the idea).**
   - Compile check against a dev SQL Server: `SET PARSEONLY ON` checks syntax only; `SET NOEXEC ON` compiles without running, but deferred name resolution means a missing table isn't always reported.
   - Then a disposable database in the workflow: a SQL Server Linux container as a service container (`mcr.microsoft.com/mssql/server`), schema deployed from your SSDT/DACPAC project or scripts, a little seed data, then run the procedure inside a transaction that is rolled back, and give Claude the result shape and row counts to compare with the story.
   - Optionally capture the estimated plan (`SET SHOWPLAN_XML ON`) to flag scans on large tables.
2. **Learn over time.** Each run already saves a JSON record (`sql-review-output.json`, kept 30 days as a workflow artifact). Next: let reviewers mark findings as useful or wrong (a reply command or reactions), collect those into a `team-conventions.md` that's added to the prompt, and use them to tune or silence rules.
3. **Inline comments** on the exact lines through the pull request review API, instead of one summary comment.
4. **Optional gate:** fail the check on High findings once the rules have proven reliable.
5. **Company version:** swap the provider as above and run on a self-hosted runner that can reach Jira.
