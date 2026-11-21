"""Tests for the rule-based checks and the Jira helpers.

Run from the sql-pr-review-agent folder:
    python -m pytest tests -q
"""

import codecs
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jira_client import adf_to_text, find_jira_keys  # noqa: E402
from sql_checks import check_sql, mask_comments_and_strings, read_sql_text  # noqa: E402


def rules(sql: str) -> list[str]:
    return [f.rule for f in check_sql("t.sql", sql, include_parse_notes=False)]


def test_masking_keeps_line_numbers_and_hides_comments_and_strings():
    sql = "SELECT 1 -- NOLOCK\n/* outer /* nested NOLOCK */ still comment */\nSELECT 'NOLOCK it''s';"
    masked = mask_comments_and_strings(sql)
    assert len(masked) == len(sql)
    assert masked.count("\n") == sql.count("\n")
    assert "NOLOCK" not in masked
    assert "still" not in masked


def test_nolock_found_but_not_in_comment():
    assert "nolock-hint" in rules("SELECT a FROM dbo.t WITH (NOLOCK);")
    assert "nolock-hint" not in rules("-- WITH (NOLOCK)\nSELECT a FROM dbo.t;")


def test_select_star_skips_exists_idiom():
    assert "select-star" in rules("SELECT * FROM dbo.t;")
    assert "select-star" in rules("SELECT TOP (10) * FROM dbo.t;")
    assert "select-star" not in rules("IF EXISTS (SELECT * FROM dbo.t) PRINT 'x';")
    assert "select-star" not in rules("SELECT COUNT(*) FROM dbo.t;")


def test_update_and_delete_scope():
    assert "update-without-where" in rules("UPDATE dbo.t SET a = 1;")
    assert "update-without-where" not in rules("UPDATE dbo.t\nSET a = 1\nWHERE id = 5;")
    assert "delete-without-where" in rules("DELETE FROM dbo.t;")
    assert "delete-without-where" not in rules("DELETE FROM dbo.t WHERE id = 5;")


def test_update_with_multiline_case_and_where_is_fine():
    sql = (
        "UPDATE dbo.t\n"
        "SET a = CASE WHEN b = 1 THEN 1\n"
        "ELSE 0\n"
        "END\n"
        "WHERE id = 5;\n"
    )
    assert "update-without-where" not in rules(sql)


def test_update_with_subquery_on_its_own_line():
    sql = "UPDATE dbo.t\nSET a = (\nSELECT MAX(x) FROM dbo.u\n)\nWHERE id = 5;"
    assert "update-without-where" not in rules(sql)


def test_non_statement_uses_of_update_and_delete_are_ignored():
    sql = (
        "CREATE TABLE dbo.c (id int REFERENCES dbo.p(id) ON DELETE CASCADE ON UPDATE NO ACTION);\n"
        "GO\n"
        "CREATE TRIGGER dbo.tr ON dbo.t AFTER INSERT, UPDATE AS BEGIN IF UPDATE(a) PRINT 'x'; END;\n"
        "GO\n"
        "MERGE dbo.t AS tgt USING dbo.s AS src ON tgt.id = src.id\n"
        "WHEN MATCHED THEN UPDATE SET tgt.a = src.a\n"
        "WHEN NOT MATCHED BY SOURCE THEN DELETE;\n"
        "UPDATE STATISTICS dbo.t;\n"
    )
    found = rules(sql)
    assert "update-without-where" not in found
    assert "delete-without-where" not in found


def test_drop_skips_temp_tables():
    assert "drop-object" not in rules("DROP TABLE IF EXISTS #work;")
    assert "drop-object" in rules("DROP TABLE dbo.Member;")


def test_transactions():
    assert "open-transaction" in rules("BEGIN TRAN; UPDATE dbo.t SET a = 1 WHERE id = 1;")
    found = rules(
        "SET XACT_ABORT ON;\nBEGIN TRY\nBEGIN TRAN;\nUPDATE dbo.t SET a = 1 WHERE id = 1;\n"
        "COMMIT;\nEND TRY\nBEGIN CATCH\nIF @@TRANCOUNT > 0 ROLLBACK;\nTHROW;\nEND CATCH;"
    )
    assert "open-transaction" not in found
    assert "transaction-without-try" not in found


def test_other_rules():
    assert "not-in-subquery" in rules("SELECT a FROM t WHERE id NOT IN (SELECT id FROM u);")
    assert "at-at-identity" in rules("SELECT @@IDENTITY;")
    assert "dynamic-sql-exec" in rules("EXEC (@sql);")
    assert "dynamic-sql-exec" not in rules("EXEC dbo.usp_Load @d = 1;")
    assert "non-sargable-predicate" in rules("SELECT a FROM t WHERE YEAR(d) = 2026;")
    assert "non-sargable-predicate" not in rules("SELECT a FROM t WHERE d >= CAST(@x AS date);")
    assert "sp-prefix" in rules("CREATE PROCEDURE [dbo].[sp_Load] AS SELECT 1;")
    assert "hardcoded-password" in rules("CREATE LOGIN x WITH PASSWORD = 'abc';")


def test_utf16_file_is_read(tmp_path):
    p = tmp_path / "u16.sql"
    p.write_bytes(codecs.BOM_UTF16_LE + "SELECT * FROM dbo.t;".encode("utf-16-le"))
    text, encoding = read_sql_text(p)
    assert text == "SELECT * FROM dbo.t;"
    assert encoding == "utf-16"


def test_find_jira_keys():
    assert find_jira_keys("DATA-12 fix", "feature/data-99-x", "see DATA-12 and ETL-7") == ["DATA-12", "DATA-99", "ETL-7"]
    assert find_jira_keys("Use UTF-8 and SHA-256", "", "") == []
    assert find_jira_keys("ABC-1 DATA-2", "", "", allowed={"DATA"}) == ["DATA-2"]


def test_adf_to_text():
    doc = {"type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "Return members"}]},
        {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "last 90 days"}]}]},
        ]},
    ]}
    text = adf_to_text(doc)
    assert "Return members" in text
    assert "- last 90 days" in text
