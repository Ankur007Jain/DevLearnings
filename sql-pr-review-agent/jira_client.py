"""Find the Jira key on a pull request and fetch that story.

Configuration (all optional; the review still runs without Jira):
  JIRA_BASE_URL      e.g. https://yourcompany.atlassian.net
  JIRA_EMAIL         Jira Cloud: your Atlassian account email (basic auth with the token)
  JIRA_API_TOKEN     Jira Cloud API token, or a Jira Data Center personal access token
                     (leave JIRA_EMAIL empty to send it as a Bearer token)
  JIRA_API_VERSION   "3" (Cloud default) or "2" (Data Center default)
  JIRA_PROJECT_KEYS  comma list such as "DATA,ETL" to avoid false matches like "UTF-8"
  JIRA_EXTRA_FIELDS  comma list of extra field ids to include, e.g. an acceptance
                     criteria custom field such as "customfield_10050"
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

import requests

KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]{1,9})-(\d{1,7})\b")
# Common uppercase tokens that look like Jira keys but are not.
NOT_PROJECT_KEYS = {"UTF", "SHA", "ISO", "TLS", "SSL", "HTTP", "HTTPS", "SQL", "AES", "RFC", "CVE", "PEP", "COVID"}


@dataclass
class JiraStory:
    key: str
    url: str
    summary: str = ""
    status: str = ""
    issue_type: str = ""
    description: str = ""
    extra: dict = field(default_factory=dict)

    def as_prompt_text(self) -> str:
        parts = [
            f"Key: {self.key}",
            f"Type: {self.issue_type or 'unknown'}",
            f"Status: {self.status or 'unknown'}",
            f"Summary: {self.summary}",
            "Description:",
            self.description.strip() or "(empty)",
        ]
        for name, value in self.extra.items():
            parts += [f"{name}:", value.strip() or "(empty)"]
        return "\n".join(parts)


def find_jira_keys(title: str, branch: str, body: str, allowed: set[str] | None = None) -> list[str]:
    """Return Jira keys in priority order: PR title, branch name, PR body.

    Branch names are often lowercase (feature/data-123-new-proc), so the branch
    is upper-cased before matching. Title and body are matched as written.
    """
    keys: list[str] = []
    for source in (title or "", (branch or "").upper(), body or ""):
        for project, number in KEY_PATTERN.findall(source):
            if allowed:
                if project not in allowed:
                    continue
            elif project in NOT_PROJECT_KEYS:
                continue
            key = f"{project}-{number}"
            if key not in keys:
                keys.append(key)
    return keys


def allowed_project_keys() -> set[str] | None:
    raw = os.environ.get("JIRA_PROJECT_KEYS", "").strip()
    if not raw:
        return None
    return {k.strip().upper() for k in raw.split(",") if k.strip()}


def jira_configured() -> bool:
    return bool(os.environ.get("JIRA_BASE_URL", "").strip() and os.environ.get("JIRA_API_TOKEN", "").strip())


def adf_to_text(node) -> str:
    """Flatten Atlassian Document Format (Jira Cloud API v3 rich text) to plain text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_to_text(n) for n in node)
    if not isinstance(node, dict):
        return str(node)

    node_type = node.get("type")
    if node_type == "text":
        return node.get("text", "")
    if node_type == "hardBreak":
        return "\n"
    if node_type in ("mention", "emoji"):
        attrs = node.get("attrs", {})
        return attrs.get("text") or attrs.get("shortName") or ""
    if node_type == "inlineCard":
        return node.get("attrs", {}).get("url", "")

    inner = adf_to_text(node.get("content", []))
    if node_type == "listItem":
        return "- " + inner.strip() + "\n"
    if node_type in ("paragraph", "heading", "blockquote", "rule", "panel"):
        return inner.rstrip() + "\n\n"
    if node_type == "codeBlock":
        return "```\n" + inner + "\n```\n\n"
    if node_type == "tableRow":
        return " | ".join(adf_to_text(c).strip() for c in node.get("content", [])) + "\n"
    return inner


def field_to_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        if value.get("type") == "doc":
            return adf_to_text(value)
        for k in ("value", "name", "displayName"):
            if k in value:
                return str(value[k])
        return str(value)
    if isinstance(value, list):
        return ", ".join(field_to_text(v) for v in value)
    return str(value)


def fetch_story(key: str, timeout: int = 30) -> JiraStory:
    """Fetch one issue. Raises requests.HTTPError on 401/403/404 and similar."""
    if not KEY_PATTERN.fullmatch(key):
        raise ValueError(f"Not a Jira key: {key!r}")

    base = os.environ["JIRA_BASE_URL"].strip().rstrip("/")
    token = os.environ["JIRA_API_TOKEN"].strip()
    email = os.environ.get("JIRA_EMAIL", "").strip()
    version = os.environ.get("JIRA_API_VERSION", "").strip() or ("3" if email else "2")
    extra_fields = [f.strip() for f in os.environ.get("JIRA_EXTRA_FIELDS", "").split(",") if f.strip()]

    headers = {"Accept": "application/json"}
    auth = None
    if email:
        auth = (email, token)  # Jira Cloud: email + API token
    else:
        headers["Authorization"] = f"Bearer {token}"  # Jira Data Center personal access token

    fields = ["summary", "description", "status", "issuetype"] + extra_fields
    resp = requests.get(
        f"{base}/rest/api/{version}/issue/{key}",
        params={"fields": ",".join(fields)},
        headers=headers,
        auth=auth,
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json().get("fields", {}) or {}

    return JiraStory(
        key=key,
        url=f"{base}/browse/{key}",
        summary=data.get("summary") or "",
        status=field_to_text(data.get("status")),
        issue_type=field_to_text(data.get("issuetype")),
        description=field_to_text(data.get("description")),
        extra={f: field_to_text(data.get(f)) for f in extra_fields},
    )
