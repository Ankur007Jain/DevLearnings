"""Rule-based T-SQL checks for the SQL PR review agent.

These are fast, free heuristics that run on every PR, with or without an AI key.
They are deliberately conservative: each rule targets a pattern that is almost
always worth a second look in SQL Server code. They are hints, not verdicts,
and the AI review is told to confirm or dismiss them.

The checker never connects to a database. It reads the file text only.
"""

from __future__ import annotations

import codecs
import re
from dataclasses import dataclass, asdict
from pathlib import Path

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Finding:
    path: str
    line: int
    severity: str  # high | medium | low
    rule: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


# --------------------------------------------------------------------------
# File reading
# --------------------------------------------------------------------------

def read_sql_text(path: Path) -> tuple[str, str]:
    """Read a .sql file and return (text, encoding).

    SQL Server Management Studio often saves scripts as UTF-16 with a byte
    order mark, so check for BOMs before falling back to UTF-8 and then
    Windows-1252.
    """
    raw = path.read_bytes()
    if raw.startswith(codecs.BOM_UTF8):
        return raw.decode("utf-8-sig"), "utf-8-sig"
    if raw.startswith(codecs.BOM_UTF16_LE) or raw.startswith(codecs.BOM_UTF16_BE):
        return raw.decode("utf-16"), "utf-16"
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace"), "cp1252"


# --------------------------------------------------------------------------
# Masking: blank out comments and string literals so rules don't fire on them
# --------------------------------------------------------------------------

def mask_comments_and_strings(sql: str) -> str:
    """Return a copy of ``sql`` with comments and string contents replaced by
    spaces. Newlines are kept, so character offsets and line numbers still
    match the original text. The quote characters of string literals are kept
    (only their contents are blanked), so a rule can still see that a string
    was assigned. T-SQL block comments can nest, and that is handled.
    """
    out = list(sql)
    n = len(sql)

    def blank(start: int, end: int) -> None:
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    i = 0
    while i < n:
        if sql.startswith("--", i):
            j = sql.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
        elif sql.startswith("/*", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if sql.startswith("/*", j):
                    depth += 1
                    j += 2
                elif sql.startswith("*/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif sql[i] == "'":
            j = i + 1
            closed = False
            while j < n:
                if sql[j] == "'":
                    if j + 1 < n and sql[j + 1] == "'":  # escaped quote ''
                        j += 2
                        continue
                    closed = True
                    break
                j += 1
            blank(i + 1, j)  # keep the opening and closing quotes
            i = j + 1 if closed else n
        else:
            i += 1
    return "".join(out)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# --------------------------------------------------------------------------
# Simple regex rules: (rule id, severity, pattern, message)
# --------------------------------------------------------------------------

FLAGS = re.IGNORECASE

SIMPLE_RULES: list[tuple[str, str, re.Pattern, str]] = [
    (
        "nolock-hint",
        "medium",
        re.compile(r"\b(?:NOLOCK|READUNCOMMITTED)\b", FLAGS),
        "NOLOCK / READUNCOMMITTED allows dirty reads: rows can be missed, read twice "
        "or read before they are rolled back. Confirm this is acceptable for the story.",
    ),
    (
        "read-uncommitted",
        "medium",
        re.compile(r"\bSET\s+TRANSACTION\s+ISOLATION\s+LEVEL\s+READ\s+UNCOMMITTED\b", FLAGS),
        "READ UNCOMMITTED isolation allows dirty reads for the whole session.",
    ),
    (
        "not-in-subquery",
        "medium",
        re.compile(r"\bNOT\s+IN\s*\(\s*SELECT\b", FLAGS),
        "NOT IN (SELECT ...) returns no rows at all if the subquery yields a NULL. "
        "NOT EXISTS is NULL-safe.",
    ),
    (
        "at-at-identity",
        "medium",
        re.compile(r"@@IDENTITY\b", FLAGS),
        "@@IDENTITY can return an identity value created by a trigger. "
        "SCOPE_IDENTITY() or an OUTPUT clause is safer.",
    ),
    (
        "dynamic-sql-exec",
        "medium",
        re.compile(r"\bEXEC(?:UTE)?\s*\(", FLAGS),
        "Dynamic SQL through EXEC(...). If the string is built from inputs, use "
        "sp_executesql with parameters to avoid SQL injection and plan-cache bloat.",
    ),
    (
        "ansi-nulls-off",
        "medium",
        re.compile(r"\bSET\s+ANSI_NULLS\s+OFF\b", FLAGS),
        "SET ANSI_NULLS OFF is deprecated and changes how = NULL comparisons behave.",
    ),
    (
        "hardcoded-password",
        "high",
        re.compile(r"\bPASSWORD\s*=\s*N?'", FLAGS),
        "Looks like a password is written into the script. Keep secrets out of source control.",
    ),
    (
        "truncate-table",
        "high",
        re.compile(r"\bTRUNCATE\s+TABLE\b", FLAGS),
        "TRUNCATE TABLE removes every row and cannot be filtered. Confirm it is intended.",
    ),
    (
        "non-sargable-predicate",
        "low",
        re.compile(
            r"\b(?:WHERE|AND|OR|ON)\s+\(?\s*(?:YEAR|MONTH|DAY|DATEPART|DATEDIFF|DATEADD|"
            r"CONVERT|CAST|ISNULL|COALESCE|UPPER|LOWER|LTRIM|RTRIM|TRIM|LEFT|RIGHT|SUBSTRING)\s*\(",
            FLAGS,
        ),
        "A function wraps the left side of a filter or join condition. If it wraps a column, "
        "SQL Server can't seek an index on that column (non-sargable). Consider rewriting "
        "as a range on the bare column.",
    ),
    (
        "cursor",
        "low",
        re.compile(r"\bDECLARE\s+@?\w+\s+(?:INSENSITIVE\s+|SCROLL\s+)*CURSOR\b", FLAGS),
        "Cursor found. A set-based statement is usually faster in SQL Server.",
    ),
    (
        "sp-prefix",
        "low",
        re.compile(
            r"\bCREATE\s+(?:OR\s+ALTER\s+)?PROC(?:EDURE)?\s+(?:\[?\w+\]?\.)?\[?sp_",
            FLAGS,
        ),
        "Procedure name starts with sp_. SQL Server checks the master database first "
        "for sp_ names; a different prefix avoids that lookup and name clashes.",
    ),
]

SELECT_STAR = re.compile(
    r"\bSELECT\s+(?:DISTINCT\s+)?(?:TOP\s*\(?\s*\d+\s*\)?\s*(?:PERCENT\s+)?)?\*", FLAGS
)
EXISTS_BEFORE = re.compile(r"\bEXISTS\s*\(\s*$", FLAGS)

DROP_OBJECT = re.compile(
    r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\s+(?:IF\s+EXISTS\s+)?([^\s;(]+)", FLAGS
)

BEGIN_TRAN = re.compile(r"\bBEGIN\s+(?:DISTRIBUTED\s+)?TRAN(?:SACTION)?\b", FLAGS)
END_TRAN = re.compile(r"\b(?:COMMIT|ROLLBACK)\b", FLAGS)
BEGIN_TRY = re.compile(r"\bBEGIN\s+TRY\b", FLAGS)

# UPDATE / DELETE without WHERE. The keyword must start a statement: skip
# "ON DELETE", "ON UPDATE", "AFTER UPDATE", "FOR UPDATE", "INSTEAD OF DELETE",
# "THEN UPDATE"/"THEN DELETE" (MERGE), "UPDATE STATISTICS" and UPDATE() in triggers.
DML_KEYWORD = re.compile(r"\b(UPDATE|DELETE)\b", FLAGS)
NOT_A_DML_START = re.compile(r"\b(?:ON|AFTER|FOR|OF|THEN|GRANT|DENY|REVOKE|,)\s*$", FLAGS)
STATEMENT_STARTERS = (
    r"SELECT|INSERT|UPDATE|DELETE|MERGE|IF|ELSE|BEGIN|END|DECLARE|EXEC|EXECUTE|WHILE|"
    r"RETURN|PRINT|GO|CREATE|ALTER|DROP|TRUNCATE|COMMIT|ROLLBACK|RAISERROR|THROW"
)
NEXT_STATEMENT = re.compile(r";|^\s*(?:" + STATEMENT_STARTERS + r")\b", FLAGS | re.MULTILINE)
WHERE_KW = re.compile(r"\bWHERE\b", FLAGS)
CASE_KW = re.compile(r"\bCASE\b", FLAGS)
END_KW = re.compile(r"\bEND\b", FLAGS)

GO_LINE = re.compile(r"^[ \t]*GO(?:[ \t]+\d+)?[ \t]*;?[ \t]*$", FLAGS | re.MULTILINE)


def _check_select_star(path: str, masked: str) -> list[Finding]:
    found = []
    for m in SELECT_STAR.finditer(masked):
        before = masked[max(0, m.start() - 40):m.start()]
        if EXISTS_BEFORE.search(before):
            continue  # EXISTS (SELECT * ...) is a harmless idiom
        found.append(Finding(
            path, line_of(masked, m.start()), "low", "select-star",
            "SELECT * returns every column, so the result changes when the table changes. "
            "List the columns the story needs.",
        ))
    return found


def _check_drop(path: str, masked: str) -> list[Finding]:
    found = []
    for m in DROP_OBJECT.finditer(masked):
        name = m.group(2).strip("[]")
        if name.startswith("#"):
            continue  # temp tables are fine to drop
        found.append(Finding(
            path, line_of(masked, m.start()), "high", "drop-object",
            f"DROP {m.group(1).upper()} {m.group(2)} permanently removes the object and its data. "
            "Confirm it is intended for this change.",
        ))
    return found


def _check_transactions(path: str, masked: str) -> list[Finding]:
    begins = list(BEGIN_TRAN.finditer(masked))
    if not begins:
        return []
    found = []
    first = line_of(masked, begins[0].start())
    if not END_TRAN.search(masked):
        found.append(Finding(
            path, first, "medium", "open-transaction",
            "BEGIN TRANSACTION without any COMMIT or ROLLBACK in this file can leave a "
            "transaction open and hold locks.",
        ))
    if not BEGIN_TRY.search(masked):
        found.append(Finding(
            path, first, "low", "transaction-without-try",
            "Transaction without TRY...CATCH. Consider SET XACT_ABORT ON plus TRY...CATCH "
            "with ROLLBACK so an error can't leave partial changes.",
        ))
    return found


def _check_dml_without_where(path: str, masked: str) -> list[Finding]:
    found = []
    for m in DML_KEYWORD.finditer(masked):
        before = masked[max(0, m.start() - 30):m.start()]
        if NOT_A_DML_START.search(before):
            continue
        after = masked[m.end():m.end() + 30]
        if re.match(r"\s*(?:\(|STATISTICS\b)", after, FLAGS):
            continue  # UPDATE(col) in a trigger, UPDATE STATISTICS
        keyword = m.group(1).upper()
        # Statement runs until a semicolon or a line that starts another statement.
        # A line that starts with SET is still part of an UPDATE. Candidates inside
        # parentheses (subqueries) or inside an open CASE expression are skipped.
        rest = masked[m.end():]
        end = len(rest)
        for nxt in NEXT_STATEMENT.finditer(rest):
            so_far = rest[:nxt.start()]
            if so_far.count("(") > so_far.count(")"):
                continue
            token = nxt.group(0).strip().upper()
            if token in ("ELSE", "END"):
                open_case = len(CASE_KW.findall(so_far)) - len(END_KW.findall(so_far))
                if open_case > 0:
                    continue
            end = nxt.start()
            break
        span = rest[:end]
        if not WHERE_KW.search(span):
            found.append(Finding(
                path, line_of(masked, m.start()), "high", f"{keyword.lower()}-without-where",
                f"{keyword} with no WHERE clause changes every row in the target "
                "(or every joined row). Confirm that is what the story asks for.",
            ))
    return found


def _parse_notes(path: str, text: str, masked: str) -> list[Finding]:
    """Best-effort dry-run parse with sqlglot's T-SQL dialect, batch by batch.

    sqlglot does not support every T-SQL construct, so a failure here is a
    note, not an error in the SQL. Returns low-severity 'parse-note' findings.
    """
    try:
        import sqlglot
        from sqlglot.errors import ParseError, TokenError
    except ImportError:
        return []

    notes = []
    starts = [0] + [m.end() for m in GO_LINE.finditer(masked)]
    ends = [m.start() for m in GO_LINE.finditer(masked)] + [len(text)]
    for start, end in zip(starts, ends):
        batch = text[start:end]
        if not batch.strip():
            continue
        try:
            sqlglot.parse(batch, read="tsql")
        except (ParseError, TokenError) as exc:
            first_line = str(exc).splitlines()[0][:200] if str(exc) else type(exc).__name__
            notes.append(Finding(
                path, line_of(text, start + (len(batch) - len(batch.lstrip()))), "low", "parse-note",
                f"The offline parser could not read the batch starting here ({first_line}). "
                "This may be T-SQL syntax the parser doesn't support rather than a real error.",
            ))
        except Exception:  # never let the parser break the review
            continue
    return notes


def check_sql(path: str, text: str, include_parse_notes: bool = True) -> list[Finding]:
    """Run every rule on one file's text and return findings sorted by line."""
    masked = mask_comments_and_strings(text)
    findings: list[Finding] = []
    for rule_id, severity, pattern, message in SIMPLE_RULES:
        for m in pattern.finditer(masked):
            findings.append(Finding(path, line_of(masked, m.start()), severity, rule_id, message))
    findings += _check_select_star(path, masked)
    findings += _check_drop(path, masked)
    findings += _check_transactions(path, masked)
    findings += _check_dml_without_where(path, masked)
    if include_parse_notes:
        findings += _parse_notes(path, text, masked)
    findings.sort(key=lambda f: (f.line, SEVERITY_ORDER.get(f.severity, 9), f.rule))
    return findings
