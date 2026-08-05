from __future__ import annotations

import unittest
from pathlib import Path

from tests.support import (
    DUAL_NAME_RE,
    FIXTURES_ROOT,
    WIKILINK_RE,
    parse_frontmatter,
    read_text,
    section,
)


class GeneratedWikiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wiki = FIXTURES_ROOT / "wiki"

    def test_content_pages_have_dual_names_and_frontmatter(self) -> None:
        seed_names = {"index.md", "concept-table.md", "log.md"}
        pages = sorted(self.wiki.rglob("*.md"))
        self.assertGreaterEqual(len(pages), 8)
        for path in pages:
            relative = path.relative_to(self.wiki)
            with self.subTest(path=relative.as_posix()):
                if path.name not in seed_names:
                    self.assertRegex(path.name, DUAL_NAME_RE)
                frontmatter = parse_frontmatter(read_text(path))
                for key in ("title", "type", "created", "updated", "sources", "tags"):
                    self.assertIn(key, frontmatter)

    def test_mechanism_has_evidence_based_argument_and_operation(self) -> None:
        path = self.wiki / "concepts" / "evidence-feedback-loop(证据反馈循环).md"
        text = read_text(path)
        self.assertIn("- **类型**：机制", text)
        argument = section(text, "作者论证")
        operation = section(text, "运行机制")
        for content in (argument, operation):
            self.assertNotIn(content, {"不适用", "不适用。", "未知", "无"})
            self.assertRegex(content, r"L\d+")
        self.assertIn("前提", argument)
        self.assertIn("结论", argument)
        self.assertIn("触发", operation)
        self.assertIn("产出", operation)

    def test_classification_retains_sections_as_not_applicable(self) -> None:
        path = self.wiki / "concepts" / "risk-level-classification(风险等级分类).md"
        text = read_text(path)
        self.assertIn("- **类型**：分类", text)
        self.assertEqual(section(text, "作者论证"), "不适用。")
        self.assertEqual(section(text, "运行机制"), "不适用。")

    def test_concept_table_matches_concept_pages(self) -> None:
        table = read_text(self.wiki / "concept-table.md")
        self.assertIn("Concept type(概念类型)", table)
        self.assertIn("证据反馈循环 | 机制", table)
        self.assertIn("风险等级分类 | 分类", table)
        self.assertNotIn("Maintenance note", table)
        self.assertNotIn("维护备注", table)

    def test_fixture_has_no_broken_semantic_wikilinks(self) -> None:
        pages = list(self.wiki.rglob("*.md"))
        stems = {path.stem for path in pages}
        for path in pages:
            for target in WIKILINK_RE.findall(read_text(path)):
                normalized = Path(target).name.removesuffix(".md")
                with self.subTest(path=path.name, target=target):
                    self.assertIn(normalized, stems)


if __name__ == "__main__":
    unittest.main()
