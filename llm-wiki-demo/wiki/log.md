---
title: log(日志)
type: log
created: 2026-08-04
updated: 2026-08-04
sources: [原则.md]
tags: [operations, audit]
---

# 日志

> 以追加方式记录所有 Wiki 操作的时间顺序。
> 每个条目：`## [YYYY-MM-DD] operation | subject`
> 使用以下命令解析：`rg "^## \\[" wiki/log.md`

## [2026-08-04] init | Wiki 已创建

- 由 llm-wiki-bootstrap 生成骨架
- 领域：个人学习与阅读知识管理，涵盖知识提炼、概念整理、目标、习惯和经验沉淀
- 来源类型：网页文章、PDF 文档／论文、书籍、图片／图表
- 编辑器：Obsidian
- 架构：SCHEMA.md（唯一事实来源）
- 指针文件：AGENTS.md（OpenAI Codex）
- BM25：auto_prompt；使用推荐阈值；本次未初始化索引

## [2026-08-04] ingest | 原则

- Summary: wiki/sources/principles(原则).md
- Part summaries: wiki/sources/principles-part-one-my-journey(原则·第一部分：我的历程).md; wiki/sources/principles-part-two-life-principles(原则·第二部分：生活原则).md; wiki/sources/principles-part-three-work-principles(原则·第三部分：工作原则).md
- Updated: wiki/index.md; wiki/concept-table.md; wiki/overview(概览).md; wiki/log.md
- New pages: 4 source summaries; 17 concept pages; 2 entity pages
- Entities: ray-dalio(瑞·达利欧); bridgewater-associates(桥水)
- Concepts: principles(原则); personal-evolution(个人进化); pain-reflection-loop(痛苦—反思循环); five-step-process(五步流程); radical-open-mindedness(头脑极度开放); thoughtful-disagreement(深思熟虑的意见分歧); believability-weighted-decision-making(可信度加权决策); expected-value-decision-making(预期价值决策); systematic-decision-making(系统化决策); idea-meritocracy(创意择优); radical-truth(极度求真); radical-transparency(极度透明); machine-model(机器模型); people-role-fit(人岗匹配); tough-love(严厉之爱); meaningful-work(有意义的工作); meaningful-relationships(有意义的人际关系)
- Retained candidates: 意境地图; 塑造者; 两个你; 风险平价; 投资的圣杯
- Ignored as standalone concepts: 反馈环（并入相关概念）; 桥水工具实例
- Contradictions: none（摄取前 Wiki 无其他知识来源）
- BM25: 未启用；摄取后规模仍低于配置阈值

## [2026-08-04] maintenance | 更新概念表协议

- Updated: wiki/concept-table.md; wiki/index.md; wiki/log.md
- Migration: 为 17 个持久概念增加 Concept type(概念类型)，主表迁移到新版 7 列协议
- Type vocabulary: 原理、机制、方法、模型／框架、状态／属性、产出
- Preservation: 原有维护备注迁移到独立 Maintenance Notes(维护备注) 小节
- Status: 17 个概念继续标记为 single-source；未发现新增矛盾
- BM25: 未启用；当前规模低于配置阈值
