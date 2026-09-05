# 日志

> 以追加方式记录所有 wiki 操作的时间顺序。
> 每个条目：`## [YYYY-MM-DD] operation | subject`
> 使用以下命令解析：`grep "^## \[" wiki/log.md | tail -10`

## [2026-09-03] init | Wiki 已创建

- 由 llm-wiki-v1 生成骨架
- 领域：面向专题研究的个人知识库，用于把论文、文章、会议记录与个人笔记中的知识，提炼为可追溯的论文摘要、主张、方法与数据集。
- 来源类型：网页文章、PDF 文档/论文、会议记录/发言稿、个人笔记/日记
- 架构：SCHEMA.md（唯一事实来源）
- 指针文件：AGENTS.md、.github/copilot-instructions.md

## [2026-09-05] ingest | 研发项目管理办法 4.1

- Summary: wiki/sources/rd-project-management-measures-v4-1(研发项目管理办法4.1).md
- Updated: wiki/index.md, wiki/concept-table.md, wiki/overview(概览).md
- New pages: 1 source-summary, 8 concepts, 4 entities
- Contradictions: none
- Search index: BM25 未启用，未执行重建；继续使用 wiki/index.md 和文本检索
- Confidentiality: 原文标有“东软秘密，未经许可不得扩散”
