#!/usr/bin/env python3
"""SQL pull-request review agent, version 1.

Runs in GitHub Actions on a pull request (see .github/workflows/sql-pr-review.yml):
  1. Lists the .sql files the PR adds or changes, with their diffs.
  2. Finds the Jira key in the PR title, branch or description and fetches the story.
  3. Runs rule-based T-SQL checks (sql_checks.py).
  4. Asks Claude to review the SQL against the story.
  5. Posts one comment on the PR, and updates that same comment on later pushes.

Every step degrades gracefully: no Jira settings means no story, no Anthropic key
means rule-based checks only. Nothing here connects to a database.

Local test run (no GitHub, prints the comment):
  python review_sql_pr.py --local --files samples/sample_member_claims.sql \
      --title "DATA-123 Members with recent claims" \
      --body-file samples/sample_pr_description.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests

import jira_client
from sql_checks import Finding, check_sql, read_sql_text

AGENT_DIR = Path(__file__).resolve().parent
COMMENT_MARKER = "<!-- sql-pr-review-agent -->"
DEFAULT_MODEL = "claude-opus-5-5"
# Models that accept the server-side refusal fallback parameter.
FALLBACK_CAPABLE_MODELS = {"claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5", "claude-fable-5-2", "claude-fable-5-1"}
GITHUB_API = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
MAX_COMMENT_CHARS = 65000  # GitHub's limit is 65,536
SEVERITY_LABEL = {"high": "High", "medium": "Medium", "low": "Low"}


@dataclass
class SqlFile:
    path: str
    status: str  # added | modified | renamed | local
    patch: str
    content: str
    encoding: str = ""
    note: str = ""


def env(name: str, default: str = "") -> str:
    value = os.environ.get(name, "")
    return value.strip() if value and value.strip() else default


def warn(message: str) -> None:
    """Print a warning that GitHub Actions shows as an annotation."""
    print(f"::warning::{message}" if os.environ.get("GITHUB_ACTIONS") else f"WARNING: {message}", file=sys.stderr)


# --------------------------------------------------------------------------
# GitHub
# --------------------------------------------------------------------------

def gh(method: str, url: str, token: str, **kwargs) -> requests.Response:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)
    resp.raise_for_status()
    return resp


def list_changed_sql_files(repo: str, pr_number: int, token: str) -> list[SqlFile]:
    """Changed .sql files from the PR's file list. Content is read from the
    checked-out PR head, so the workflow must check out the head commit."""
    files: list[SqlFile] = []
    page = 1
    while True:
        batch = gh("GET", f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/files", token,
                   params={"per_page": 100, "page": page}).json()
        for item in batch:
            name = item["filename"]
            if not name.lower().endswith(".sql") or item.get("status") == "removed":
                continue
            path = Path(name)
            content, encoding, note = "", "", ""
            if path.is_file():
                content, encoding = read_sql_text(path)
            else:
                note = "File not found in the checkout."
            patch = item.get("patch") or ""
            if not patch:
                note = (note + " " if note else "") + (
                    "GitHub sent no diff for this file (it may be too large or saved as UTF-16); "
                    "the full file is reviewed instead.")
            files.append(SqlFile(name, item.get("status", ""), patch, content, encoding, note))
        if len(batch) < 100:
            break
        page += 1
    return files


def upsert_comment(repo: str, pr_number: int, token: str, body: str) -> str:
    """Update this agent's earlier comment if there is one, otherwise create it."""
    page = 1
    existing_id = None
    while existing_id is None:
        comments = gh("GET", f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments", token,
                      params={"per_page": 100, "page": page}).json()
        for c in comments:
            if COMMENT_MARKER in (c.get("body") or ""):
                existing_id = c["id"]
                break
        if len(comments) < 100:
            break
        page += 1

    if existing_id:
        resp = gh("PATCH", f"{GITHUB_API}/repos/{repo}/issues/comments/{existing_id}", token, json={"body": body})
    else:
        resp = gh("POST", f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments", token, json={"body": body})
    return resp.json().get("html_url", "")


# --------------------------------------------------------------------------
# Prompt building and the Claude call
# --------------------------------------------------------------------------

def build_user_content(story_text: str, pr: dict, files: list[SqlFile], findings: list[Finding],
                       max_chars: int) -> tuple[str, list[str]]:
    """Build the review request. If it is too large, drop full file contents
    (keeping diffs), then shorten diffs, and report what was left out."""
    notes: list[str] = []
    findings_text = "\n".join(
        f"- {f.path}:{f.line} [{f.severity}] {f.rule}: {f.message}" for f in findings
    ) or "(none)"
    header = (
        f"<story>\n{story_text}\n</story>\n\n"
        f"<pull_request>\nTitle: {pr.get('title', '')}\nBranch: {pr.get('branch', '')}\n"
        f"Description:\n{pr.get('body') or '(empty)'}\n</pull_request>\n\n"
        f"<static_checks>\n{findings_text}\n</static_checks>\n\n"
    )

    def render(include_content: bool, diff_limit: int | None) -> str:
        blocks = []
        for f in files:
            patch = f.patch
            if diff_limit is not None and len(patch) > diff_limit:
                patch = patch[:diff_limit] + f"\n[... diff shortened, {len(f.patch) - diff_limit} characters left out ...]"
            parts = [f'<file path="{f.path}" status="{f.status}">']
            if f.note:
                parts.append(f"Note: {f.note}")
            parts.append(f"<diff>\n{patch or '(no diff available)'}\n</diff>")
            if include_content or not f.patch:
                parts.append(f"<full_content>\n{f.content}\n</full_content>")
            parts.append("</file>")
            blocks.append("\n".join(parts))
        return "\n\n".join(blocks)

    body = render(True, None)
    if len(header) + len(body) > max_chars:
        body = render(False, None)
        notes.append("The change was too large to send whole files, so the AI reviewed the diffs only.")
    if len(header) + len(body) > max_chars:
        per_file = max(2000, (max_chars - len(header)) // max(1, len(files)))
        body = render(False, per_file)
        notes.append("Some diffs were shortened to fit; the AI did not see every changed line.")
    return header + body, notes


def run_ai_review(user_content: str, model: str, effort: str) -> tuple[str, str]:
    """Call Claude and return (review_markdown, note). Uses streaming so a long
    review can't hit an HTTP timeout."""
    import anthropic

    system_prompt = (AGENT_DIR / "prompt.md").read_text(encoding="utf-8")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    kwargs = dict(
        model=model,
        max_tokens=16000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    if effort:
        kwargs["output_config"] = {"effort": effort}

    if model in FALLBACK_CAPABLE_MODELS:
        # If the model declines on a safety classifier, the API retries the same
        # request on a fallback model inside the same call.
        with client.beta.messages.stream(
            betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs
        ) as stream:
            message = stream.get_final_message()
    else:
        with client.messages.stream(**kwargs) as stream:
            message = stream.get_final_message()

    text = "".join(block.text for block in message.content if block.type == "text").strip()
    note = ""
    if message.stop_reason == "refusal":
        note = "The model declined to review this change."
    elif message.stop_reason == "max_tokens":
        note = "The AI review hit its length limit and may be cut off."
    return text, note


# --------------------------------------------------------------------------
# Comment rendering
# --------------------------------------------------------------------------

def md_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_comment(ctx: dict) -> str:
    lines = [COMMENT_MARKER, "## SQL review agent", ""]

    story = ctx.get("story")
    if story:
        lines.append(f"**Story:** [{story.key}]({story.url}): {md_cell(story.summary)}"
                     f"{f' ({story.status})' if story.status else ''}")
    else:
        lines.append(f"**Story:** {ctx['story_note']}")
    lines.append(f"**SQL files reviewed:** {len(ctx['files'])}")
    lines.append("")

    lines.append("### AI review")
    if ctx.get("ai_text"):
        lines += [ctx["ai_text"], ""]
    for note in ctx.get("ai_notes", []):
        lines.append(f"> {note}")
    if not ctx.get("ai_text") and not ctx.get("ai_notes"):
        lines.append("_Skipped._")
    lines.append("")

    issues = [f for f in ctx["findings"] if f.rule != "parse-note"]
    parse_notes = [f for f in ctx["findings"] if f.rule == "parse-note"]
    lines.append("### Rule-based checks")
    if issues:
        lines += ["| Severity | File | Line | Check | Note |", "|---|---|---|---|---|"]
        for f in issues:
            lines.append(f"| {SEVERITY_LABEL.get(f.severity, f.severity)} | `{md_cell(f.path)}` | {f.line} "
                         f"| {f.rule} | {md_cell(f.message)} |")
    else:
        lines.append("No rule-based findings.")
    lines.append("")
    if parse_notes:
        lines.append("<details><summary>Offline parser notes</summary>\n")
        for f in parse_notes:
            lines.append(f"- `{md_cell(f.path)}` line {f.line}: {f.message}")
        lines += ["", "</details>", ""]

    file_notes = [f for f in ctx["files"] if f.note]
    if file_notes:
        lines.append("<details><summary>File notes</summary>\n")
        for f in file_notes:
            lines.append(f"- `{md_cell(f.path)}`: {f.note}")
        lines += ["", "</details>", ""]

    lines += [
        "---",
        f"<sub>sql-pr-review-agent v1 · {ctx.get('model_label', 'rules only')} · "
        "Rule checks are heuristics and AI reviews can be wrong, so verify before applying. "
        "The SQL was not run against any database. This comment updates on each push.</sub>",
    ]
    body = "\n".join(lines)
    if len(body) > MAX_COMMENT_CHARS:
        body = body[:MAX_COMMENT_CHARS - 200] + "\n\n_[Comment shortened to fit GitHub's size limit. " \
               "The full review is in the workflow run's artifact.]_"
    return body


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def load_pr_context(args) -> dict:
    if args.local:
        body = Path(args.body_file).read_text(encoding="utf-8") if args.body_file else ""
        return {"repo": "", "number": 0, "title": args.title or "", "branch": args.branch or "", "body": body}
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr = event["pull_request"]
    return {
        "repo": os.environ["GITHUB_REPOSITORY"],
        "number": int(pr["number"]),
        "title": pr.get("title") or "",
        "branch": pr.get("head", {}).get("ref") or "",
        "body": pr.get("body") or "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Review the SQL in a pull request.")
    parser.add_argument("--local", action="store_true", help="Run on local files and print the comment.")
    parser.add_argument("--files", nargs="*", default=[], help="(--local) .sql files to review.")
    parser.add_argument("--title", help="(--local) PR title.")
    parser.add_argument("--branch", help="(--local) branch name.")
    parser.add_argument("--body-file", help="(--local) file holding the PR description.")
    parser.add_argument("--no-ai", action="store_true", help="Skip the Claude review.")
    args = parser.parse_args()

    pr = load_pr_context(args)
    token = env("GITHUB_TOKEN")

    # 1. Changed SQL files
    if args.local:
        files = []
        for name in args.files:
            content, encoding = read_sql_text(Path(name))
            patch = "\n".join("+" + line for line in content.splitlines())
            files.append(SqlFile(name, "local", patch, content, encoding))
    else:
        files = list_changed_sql_files(pr["repo"], pr["number"], token)
    if not files:
        print("No added or modified .sql files in this pull request; nothing to review.")
        return 0

    # 2. Jira story
    story, story_note = None, ""
    keys = jira_client.find_jira_keys(pr["title"], pr["branch"], pr["body"], jira_client.allowed_project_keys())
    if not keys:
        story_note = "No Jira key found in the PR title, branch name or description."
    elif not jira_client.jira_configured():
        story_note = (f"Found {keys[0]}, but Jira isn't set up for this repo yet (JIRA_BASE_URL and "
                      "JIRA_API_TOKEN), so the review used the PR description only.")
    else:
        try:
            story = jira_client.fetch_story(keys[0])
        except Exception as exc:  # report and continue without the story
            status = getattr(getattr(exc, "response", None), "status_code", None)
            story_note = (f"Found {keys[0]}, but couldn't read it from Jira"
                          f"{f' (HTTP {status})' if status else ''}; the review used the PR description only.")
            warn(f"Jira fetch failed for {keys[0]}: {type(exc).__name__}")
    if story:
        story_text = story.as_prompt_text()
        if len(keys) > 1:
            story_text += f"\n(Other keys mentioned on the PR, not fetched: {', '.join(keys[1:])})"
    else:
        story_text = f"No Jira story available. {story_note} If the PR description includes the story " \
                     "or acceptance criteria, use that."

    # 3. Rule-based checks
    findings: list[Finding] = []
    for f in files:
        if f.content:
            findings += check_sql(f.path, f.content)

    # 4. AI review
    model = env("ANTHROPIC_MODEL", DEFAULT_MODEL)
    effort = env("REVIEW_EFFORT", "high")
    ai_text, ai_notes, model_label = "", [], "rules only"
    if args.no_ai:
        ai_notes.append("AI review turned off for this run.")
    elif not env("ANTHROPIC_API_KEY"):
        ai_notes.append("AI review skipped: add an ANTHROPIC_API_KEY repository secret to turn it on.")
    else:
        user_content, size_notes = build_user_content(
            story_text, pr, files, findings, int(env("REVIEW_MAX_PROMPT_CHARS", "400000")))
        ai_notes += size_notes
        try:
            ai_text, note = run_ai_review(user_content, model, effort)
            model_label = f"model {model}"
            if note:
                ai_notes.append(note)
        except Exception as exc:
            ai_notes.append(f"AI review failed ({type(exc).__name__}); see the workflow log.")
            warn(f"AI review failed: {exc}")

    ctx = {"story": story, "story_note": story_note, "files": files, "findings": findings,
           "ai_text": ai_text, "ai_notes": ai_notes, "model_label": model_label}
    comment = render_comment(ctx)

    # 5. Save a record of the run (seed for the future feedback log) and post
    record = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo": pr["repo"], "pr_number": pr["number"], "title": pr["title"], "branch": pr["branch"],
        "jira_keys": keys, "story_fetched": bool(story), "model": model if ai_text else None,
        "files": [f.path for f in files], "findings": [f.to_dict() for f in findings],
        "ai_review": ai_text, "notes": ai_notes,
    }
    Path(env("REVIEW_OUTPUT_PATH", "sql-review-output.json")).write_text(json.dumps(record, indent=2), encoding="utf-8")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(comment + "\n")

    if args.local:
        print(comment)
        return 0

    try:
        url = upsert_comment(pr["repo"], pr["number"], token, comment)
        print(f"Review posted: {url}")
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        # Pull requests from forks get a read-only token, so commenting fails there.
        warn(f"Couldn't post the PR comment (HTTP {status}). The review is in the job summary.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
