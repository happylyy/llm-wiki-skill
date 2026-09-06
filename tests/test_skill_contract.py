from __future__ import annotations

import re
import unittest
from pathlib import Path

from tests.support import (
    CONCEPT_TYPES,
    MIRROR_ROOT,
    SKILL_ROOT,
    parse_frontmatter,
    read_text,
    sha256,
)


class SkillContractTests(unittest.TestCase):
    def test_agent_mirror_is_a_byte_identical_subset(self) -> None:
        mirror_files = sorted(path for path in MIRROR_ROOT.rglob("*") if path.is_file())
        self.assertGreaterEqual(len(mirror_files), 20)

        for mirror_path in mirror_files:
            relative = mirror_path.relative_to(MIRROR_ROOT)
            canonical_path = SKILL_ROOT / relative
            with self.subTest(path=relative.as_posix()):
                self.assertTrue(canonical_path.is_file(), "mirror file missing from skill/")
                self.assertEqual(sha256(canonical_path), sha256(mirror_path))

    def test_skill_frontmatter_is_minimal_and_valid(self) -> None:
        for root in (SKILL_ROOT, MIRROR_ROOT):
            text = read_text(root / "SKILL.md").replace("\r\n", "\n")
            self.assertTrue(text.startswith("---\n"))
            end = text.find("\n---", 4)
            self.assertGreater(end, 4)
            keys = {
                line.split(":", 1)[0].strip()
                for line in text[4:end].splitlines()
                if ":" in line and not line.startswith((" ", "\t"))
            }
            self.assertEqual(keys, {"name", "description"})
            self.assertIn("name: llm-wiki-v1", text[:end])

    def test_concept_template_has_ordered_complete_contract(self) -> None:
        template = read_text(SKILL_ROOT / "references" / "templates" / "concepts.md")
        headings = (
            "## 工作定义",
            "## 作者论证",
            "## 运行机制",
            "## 相关概念",
            "## 来源",
        )
        positions = [template.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertNotRegex(template, r"(?m)^## 定义\s*$")

        for concept_type in CONCEPT_TYPES:
            with self.subTest(concept_type=concept_type):
                self.assertIn(concept_type, template)

        self.assertIn("其他类型填写“不适用”", template)
        self.assertIn("核心机制”只保留一句话摘要", template)

    def test_concept_table_has_new_type_column_and_no_legacy_column(self) -> None:
        template = read_text(
            SKILL_ROOT / "references" / "templates" / "concept-table.md"
        )
        header = next(line for line in template.splitlines() if line.startswith("| Concept("))
        self.assertIn("Concept type(概念类型)", header)
        self.assertNotIn("Maintenance note", template)
        self.assertNotIn("维护备注", template)
        for concept_type in CONCEPT_TYPES:
            self.assertIn(f"`{concept_type}`", template)

    def test_source_template_is_complete_and_routed_from_ingest(self) -> None:
        template = read_text(SKILL_ROOT / "references" / "templates" / "sources.md")
        ingest = read_text(SKILL_ROOT / "references" / "workflows" / "ingest.md")
        frontmatter = parse_frontmatter(template)

        self.assertEqual(
            set(frontmatter),
            {"title", "type", "created", "updated", "sources", "tags"},
        )
        self.assertEqual(frontmatter["type"], "source-summary")

        headings = (
            "## 作品分类(Category)",
            "## 主题摘要(Summary)",
            "## 关键主张(Key Claims)",
            "## 作品结构(Structures)",
            "## 目录与实际结构的差异",
            "## 提及的实体(Entities Mentioned)",
            "## 相关概念(Concepts)",
            "## 重要引文(Notable Quotes)",
            "## 局限／偏见(Limitations / Bias)",
        )
        positions = [template.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))

        self.assertIn("references/templates/sources.md", ingest)
        self.assertIn("完整持久概念清单", template)
        self.assertNotIn("type: source-summary", ingest)
        self.assertNotIn("1. **作品分类(Category)**", ingest)

    def test_ingest_keeps_confirmed_notes_and_source_concepts_in_sync(self) -> None:
        ingest = read_text(SKILL_ROOT / "references" / "workflows" / "ingest.md")
        schema = read_text(SKILL_ROOT / "references" / "templates" / "schema.md")
        lint = read_text(SKILL_ROOT / "references" / "workflows" / "lint.md")

        for text in (ingest, schema):
            self.assertIn("来源页、概念页和实体页在内存中的笔记", text)
            self.assertIn("全部持久概念", text)
            self.assertIn("`保留候选` 和 `忽略`", text)
            self.assertIn("多来源概念必须出现在每个对应来源摘要中", text)
            self.assertIn("只链接最终规范概念页", text)
            for action in ("新增", "更新", "合并"):
                self.assertIn(action, text)

        self.assertRegex(lint, r"Source-concept drift.+中")
        self.assertIn("概念页 `sources`", lint)

    def test_schema_and_workflows_enforce_type_dependent_sections(self) -> None:
        schema = read_text(SKILL_ROOT / "references" / "templates" / "schema.md")
        ingest = read_text(SKILL_ROOT / "references" / "workflows" / "ingest.md")
        book = read_text(
            SKILL_ROOT / "references" / "workflows" / "ingest_concepts.md"
        )
        combined = "\n".join((schema, ingest, book))

        for heading in ("## 工作定义", "## 作者论证", "## 运行机制"):
            self.assertIn(f"`{heading}`", combined)
        for concept_type in ("原理", "机制", "方法", "模型／框架"):
            self.assertIn(concept_type, combined)
        self.assertIn("其他类型在“作者论证”和“运行机制”中填写“不适用”", book)
        self.assertIn("不得根据常识、模型记忆或外部资料补齐", book)

    def test_ingest_duplicate_conflict_and_confirmation_gates_are_explicit(self) -> None:
        ingest = read_text(SKILL_ROOT / "references" / "workflows" / "ingest.md")
        self.assertIn("此阶段只能读取和分析来源及现有 wiki，不得写入任何 wiki 派生页面", ingest)
        self.assertIn("只有用户明确确认后", ingest)
        self.assertIn("是重新导入（更新）还是跳过此过程", ingest)
        self.assertIn("冲突块(contradiction block)", ingest)
        self.assertIn("按顺序处理（不要并行", ingest)

    def test_bm25_and_lint_require_authorization(self) -> None:
        bm25 = read_text(SKILL_ROOT / "references" / "workflows" / "bm25.md")
        lint = read_text(SKILL_ROOT / "references" / "workflows" / "lint.md")
        self.assertIn("仅在用户明确批准后初始化", bm25)
        self.assertIn("BM25 是可选的本地组件", bm25)
        self.assertIn("现在应修复哪些项目", lint)
        self.assertIn("对每个获准的修复内容", lint)
        self.assertRegex(lint, r"Broken wikilinks.+高")

    def test_templates_and_workflows_have_no_legacy_definition_heading(self) -> None:
        for directory in (
            SKILL_ROOT / "references" / "templates",
            SKILL_ROOT / "references" / "workflows",
        ):
            for path in directory.rglob("*.md"):
                with self.subTest(path=path.relative_to(SKILL_ROOT).as_posix()):
                    self.assertIsNone(
                        re.search(r"(?m)^## 定义\s*$", read_text(path)),
                        "legacy concept heading remains",
                    )


if __name__ == "__main__":
    unittest.main()
