---
title: 日志
type: operation-log
created: 2026-08-04
updated: 2026-08-04
sources: []
tags: [operations]
---

# 日志

> 以追加方式记录所有 Wiki 操作的时间顺序。
> 每个条目：`## [YYYY-MM-DD] operation | subject`

## [2026-08-04] init | Wiki 已创建

- 由 llm-wiki-bootstrap 生成骨架
- 领域：专题研究，围绕研究资料、论文、主张、方法和数据集建立可追溯的个人知识库
- 来源类型：网页文章、PDF 文档／论文、书籍、个人笔记／日记
- 架构：SCHEMA.md（唯一事实来源）
- 指针文件：AGENTS.md
- 偏好文件：.llm-wiki-bootstrap/EXTEND.md
- BM25：尚未初始化；达到配置阈值时提示

## [2026-08-04] ingest | 原则：应对变化中的世界秩序

- Summary: wiki/sources/principles-for-dealing-with-the-changing-world-order(原则：应对变化中的世界秩序).md
- Updated: wiki/index.md, wiki/concept-table.md, wiki/overview(概览).md
- New pages: 4 个来源摘要、14 个概念页、5 个实体页
- Source partitions: 第一部分“世界是如何运转的”、第二部分“500年世界发展史”、第三部分“未来”
- Concepts: 大周期、进化上行趋势、五大力量、国家实力指标、长期债务周期、货币体系类型、储备货币周期、和谐去杠杆化、资本市场大周期、内部秩序周期、外部秩序周期、国家冲突类型、历史类比法、不确定性应对法
- Entities: 瑞·达利欧、荷兰帝国、大英帝国、美国、中国
- Candidates retained without pages: 市场四因子、三类货币政策、相互保证毁灭、桥水基金
- Contradictions: none；记录原书“18项决定因素”与后续第19–22项的计数口径差异
- Search: BM25 未达到配置阈值，未初始化

## [2026-08-04] lint | 《原则：应对变化中的世界秩序》摄取后检查

- 问题总数：14
- 高：0，中：0，低：14
- 低严重度发现：14 个概念当前均为 single-source，已在概念表中明确标注
- 已修复：无；结构、frontmatter、索引覆盖、概念表、Wikilink 与 Markdown 链接检查均通过
- 已推迟：等待未来独立来源验证或反驳现有概念
- 原始资料：Markdown SHA-256 保持为 9F6D86DFA311F6BEC4A7942885BE75C383FBC8601126866F51122A6A9A37736E；图片 214 个，共 11193252 字节
- BM25 gate: 4 个来源摘要、27 个 Wiki 页面、约 4.8 万字符、索引 88 行，均低于初始化阈值
