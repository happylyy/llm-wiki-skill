from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tests.support import EXPORT_FIELDS, REPO_ROOT, copy_test_wiki, run_bm25, sha256


def fts5_available() -> bool:
    try:
        with sqlite3.connect(":memory:") as connection:
            connection.execute("CREATE VIRTUAL TABLE test_fts USING fts5(value)")
        return True
    except sqlite3.Error:
        return False


@unittest.skipUnless(fts5_available(), "SQLite FTS5 is unavailable")
class BM25EndToEndTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(
            prefix="llm-wiki-bootstrap-tests-"
        )
        self.root = copy_test_wiki(Path(self.temporary_directory.name))
        self.raw_hashes = {
            path.name: sha256(path) for path in sorted((self.root / "raw").glob("*.md"))
        }

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def assert_success(self, *arguments: str) -> str:
        result = run_bm25(self.root, *arguments)
        self.assertEqual(
            result.returncode,
            0,
            f"command failed: {arguments}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result.stdout

    def assert_raw_unchanged(self) -> None:
        current = {
            path.name: sha256(path) for path in sorted((self.root / "raw").glob("*.md"))
        }
        self.assertEqual(current, self.raw_hashes)

    def test_doctor_and_missing_index_state(self) -> None:
        self.assertIn("SQLite FTS5 is available", self.assert_success("doctor"))
        self.assertIn("BM25 index: missing", self.assert_success("stats"))
        self.assertFalse((self.root / "indexes" / "fts.sqlite").exists())
        self.assert_raw_unchanged()

    def test_build_search_and_all_exports(self) -> None:
        page_count = len(list((self.root / "wiki").rglob("*.md")))
        build_output = self.assert_success("build")
        self.assertIn(f"with {page_count} pages", build_output)

        stats = self.assert_success("stats")
        self.assertIn(f"Pages: {page_count}", stats)
        self.assertRegex(stats, r"Chunks: [1-9]\d*")
        self.assertIn("Fresh: yes", stats)

        search = self.assert_success("search", "证据反馈循环", "--limit", "5")
        self.assertIn("evidence-feedback-loop(证据反馈循环).md", search)

        jsonl_path = self.root / "exports" / "bm25-chunks.jsonl"
        self.assert_success(
            "export", "--format", "jsonl", "--out", str(jsonl_path)
        )
        rows = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()]
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertEqual(tuple(row), EXPORT_FIELDS)

        csv_path = self.root / "exports" / "bm25-chunks.csv"
        markdown_path = self.root / "exports" / "bm25-report.md"
        self.assert_success("export", "--format", "csv", "--out", str(csv_path))
        self.assert_success(
            "export", "--format", "markdown", "--out", str(markdown_path)
        )
        self.assertTrue(csv_path.is_file())
        self.assertIn("# BM25 Index Export", markdown_path.read_text(encoding="utf-8"))
        self.assert_raw_unchanged()

    def test_stale_index_is_detected_and_rebuild_restores_freshness(self) -> None:
        self.assert_success("build")
        database = self.root / "indexes" / "fts.sqlite"
        os.utime(database, (1, 1))
        self.assertIn("Fresh: no", self.assert_success("stats"))
        self.assert_success("rebuild")
        self.assertIn("Fresh: yes", self.assert_success("stats"))
        self.assert_raw_unchanged()


class TestIsolationGuardTests(unittest.TestCase):
    def test_repository_destination_is_rejected_before_writing(self) -> None:
        forbidden = REPO_ROOT / "tests" / "should-not-be-created"
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            copy_test_wiki(forbidden)
        self.assertFalse(forbidden.exists())


if __name__ == "__main__":
    unittest.main()
