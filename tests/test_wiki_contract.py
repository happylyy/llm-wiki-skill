from __future__ import annotations

import unittest
from pathlib import Path

from tests.support import (
    DUAL_NAME_RE,
    FIXTURES_ROOT,
    REPO_ROOT,
    WIKILINK_RE,
    parse_frontmatter,
    parse_frontmatter_list,
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

    def assert_source_concept_links_match_provenance(self, wiki: Path) -> None:
        concept_stems = {
            path.stem for path in (wiki / "concepts").glob("*.md")
        }
        concepts_by_source: dict[str, set[str]] = {}
        for path in (wiki / "concepts").glob("*.md"):
            frontmatter = parse_frontmatter(read_text(path))
            for source in parse_frontmatter_list(frontmatter["sources"]):
                concepts_by_source.setdefault(source, set()).add(path.stem)

        for path in (wiki / "sources").glob("*.md"):
            text = read_text(path)
            frontmatter = parse_frontmatter(text)
            source_files = parse_frontmatter_list(frontmatter["sources"])
            expected = set().union(
                *(concepts_by_source.get(source, set()) for source in source_files)
            )
            targets = [
                Path(target).name.removesuffix(".md")
                for target in WIKILINK_RE.findall(
                    section(text, "相关概念(Concepts)")
                )
            ]

            with self.subTest(wiki=wiki.name, source=path.name):
                self.assertEqual(len(targets), len(set(targets)), "duplicate concept link")
                self.assertTrue(set(targets).issubset(concept_stems))
                self.assertSetEqual(set(targets), expected)

    def test_fixture_source_concept_links_match_provenance(self) -> None:
        self.assert_source_concept_links_match_provenance(self.wiki)

    def test_demo_source_concept_links_match_provenance(self) -> None:
        self.assert_source_concept_links_match_provenance(
            REPO_ROOT / "llm-wiki-demo" / "wiki"
        )


if __name__ == "__main__":
    unittest.main()
