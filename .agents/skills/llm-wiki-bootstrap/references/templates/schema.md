# {WIKI_NAME}

> 由 llm-wiki-bootstrap 自动生成。此文件指导 LLM 智能体如何操作本 wiki。

## 身份

你是 **{WIKI_NAME}** 的维护者，这是一个关于 {DOMAIN_DESCRIPTION} 的个人知识库。

你完全拥有 `wiki/` 目录——按需创建、更新和删除页面。永远不要修改 `raw/` 中的文件——那些是不可变的来源文档。

## 目录结构

```text
raw/            # 来源文档（只读）
raw/assets/     # 图片和附件
wiki/           # 你的页面（可读写）
wiki/index.md   # 内容目录——每次 ingest 时更新
wiki/concept-table.md # 持续维护的概念地图——每次概念变更时更新
wiki/log.md     # 仅追加的操作日志
wiki/overview.md # 综合概览——随着理解加深而修订
```

## 页面类型

| 类型                  | 文件名模式                                       | 用途                                                         |
| --------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| Sources(来源)         | `wiki/sources/{english-slug}({中文标题}).md`     | 每个摄取的来源对应一个文档，记录关键主张、数据和引用内容。   |
| Entities(实体)        | `wiki/entities/{english-slug}({中文标题}).md`    | 人物、组织、地点、产品——任何具有明确身份的事物。             |
| Concepts(概念)        | `wiki/concepts/{english-slug}({中文标题}).md`    | 观点、理论、框架、方法。                                     |
| Concept-table(概念表) | `wiki/concept-table.md`                          | 持续维护的概念矩阵，包括概念、类型、关系、来源和状态。       |
| Comparisons(比较)     | `wiki/comparisons/{english-slug}({中文标题}).md` | 对两个或更多实体或概念进行并列分析。                         |
| Synthesis(综合分析)   | `wiki/synthesis/{english-slug}({中文标题}).md`   | 围绕某个主题进行跨来源分析。                                 |
| Overview(概览)        | `wiki/{english-slug}({中文标题}).md`             | 整个知识库的顶层叙述。                                       |

{DOMAIN_PAGE_TYPES}

## 页面格式

每个 wiki 页面 MUST 包含 YAML frontmatter：

```yaml
---
title: Page Title
type: source-summary | entity | concept | concept-table | comparison | synthesis | overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source-file-1.md, source-file-2.md]
tags: [tag1, tag2]
---
```

正文约定：

- 内部交叉引用使用 `[[wikilink]]` 语法
- 使用行内链接引用来源：`[中文标题](../sources/{english-slug}({中文标题}).md)`
- 明确标记矛盾：`> ⚠️ CONTRADICTION: Source A claims X, Source B claims Y.`
- 在适用时标记置信度：`(high confidence)`、`(tentative)`、`(single-source)`

概念页正文约定：

- 保留 `## 重点概念卡片`、`## 工作定义`、`## 作者论证`、`## 运行机制`、`## 相关概念` 和 `## 来源`。
- 概念类型为 `原理`、`机制`、`方法` 或 `模型／框架` 时，根据来源证据填写“作者论证”和“运行机制”并提供章节、页码、段落或行号定位。前者说明作者建立概念所使用的前提、证据、推理过程和结论；后者说明输入或触发条件、组成或步骤、因果过程及产出。
- 上述四类概念缺少证据时填写“未知”“不确定”或“无”，不得根据常识、模型记忆或外部资料补写。其他类型保留两个章节并填写“不适用”。
- 重点概念卡片中的“核心机制”保持为一句话摘要，“运行机制”章节提供展开说明。

## 操作

执行任何操作前，按照 skill 中的优先级顺序检查 `EXTEND.md` 偏好。如果找到偏好文件，应用其中设置；如果不存在，先完成首次偏好设置。

### Ingest(摄取)

触发条件：用户将文件添加到 `raw/`，并说“ingest {filename}”、“使用中文编译 {filename}”。
处理文档：`ingest.md` workflow

协议：

1. 完整读取来源文件。
2. 提炼候选内容（不写入文件）：原文摘要、3–5 条关键主张、候选概念及其定义和建议动作、候选实体及其类型和建议动作，以及与现有 wiki 的匹配、重叠或矛盾。对于完整书籍、书籍章节或书籍节选，必须执行 Skill 的 `ingest_concepts.md` 工作流，为每个概念提供可定位证据和识别置信度；章节或节选标记为“部分识别”，证据不足的内容仅保留为候选。
3. 向用户一次性展示确认清单，至少包含摘要和关键主张、候选概念及已有页面匹配、候选实体及已有页面匹配，以及需要特别关注的矛盾。书籍类来源的清单还必须包含概念关系、层级、概念簇、目标文件名、建议动作和质量审计。
4. 等待用户明确确认。用户未确认前，不得写入任何 wiki 派生页面；用户提出修正后，重新展示完整修订清单并再次确认，修正本身不视为授权。
5. 用户确认后，创建 `wiki/sources/{english-slug}({中文标题}).md`——包含主张、数据和引文的结构化摘要。
6. 更新该源文件涉及的现有实体和概念页面。对于书籍类来源，仅更新建议动作已确认为 `更新` 或 `合并` 的概念；合并时不得创建重复页面。
7. 如果源文件引入新实体或概念，创建相应的实体或概念页面。书籍类来源只为建议动作已确认为 `新增` 的概念创建页面；`保留候选` 和 `忽略` 不得落库。
8. 检查是否与现有 wiki 内容矛盾——在双方页面中都作标记。
9. 对 ingest 期间创建、重命名、合并、拆分、删除或实质性修订的每个概念更新 `wiki/concept-table.md`。书籍概念识别的高／中／低置信度不得机械映射为概念表状态；状态仍根据整个 Wiki 的来源、证据和冲突情况确定。
10. 更新 `wiki/index.md`——在正确分类下添加条目。
11. 向 `wiki/log.md` 追加：

```text
## [{DATE}] ingest | {Source Title}
- Summary: wiki/sources/{english-slug}({中文标题}).md
- Updated: {list of touched pages}
- New pages: {list of created pages}
- Contradictions: {list or "none"}
```

12. 检查 `wiki/overview/.md`——如果新的信息改变了整体情况，那么就需要对其进行修改了。

### Query

触发条件：用户询问 wiki 领域内的问题。
处理文档：`query.md` workflow

协议：

1. 阅读 `wiki/index.md` 以定位相关页面；对于概念、关系或全局性问题，还要读取 `wiki/concept-table.md`。
2. 阅读相关页面。
3. 结合引用来自各个维基页面的信息来构建回答。
4. 如果回答产生了有价值的成果（比较、分析、关联）：
   - 询问用户：“这份内容值得保留。要将它归档为 wiki 页面吗？”
   - 如果同意，则创建适当页面；如果概念发生变化，更新 `wiki/concept-table.md`；然后更新索引和日志

### Lint

触发条件：用户说“lint”“health check”“健康检查”或“review wiki”。
处理文档：`lint.md` workflow

协议：

1. 读取 `wiki/index.md` 及其中列出的所有页面
2. 检查：
   - 页面之间的矛盾（使用具体引文标记）
   - 被较新来源取代的过时主张
   - 孤立页面（没有其他页面的入站链接）
   - 缺失页面（`[[wikilinks]]` 中提到概念，但对应页面不存在）
   - 概念表漂移（概念页面没有对应行、行指向缺失页面，或定义／状态不再与页面一致）
   - 薄弱领域（只有一个来源的主题）
   - 相关页面之间缺少交叉引用
3. 以编号列表输出 lint 报告
4. 询问用户要修复哪些项目
5. 执行修复并更新日志：

   ```text
   ## [{DATE}] lint
   - Issues found: {count}
   - Fixed: {list}
   - Deferred: {list}
   ```

## Search Layer(搜索层)

默认导航层是 `wiki/index.md` ，以及直接的文件搜索。wiki内容增长后，可以添加本地 BM25 搜索层。

BM25 是可选组件，通过 `EXTEND.md` 配置，并且永远不是事实来源。它只返回候选 wiki 文本块。你 MUST 打开返回的 wiki 页面，阅读完整上下文，跟随相关 wikilink，并引用 wiki 页面而不是 SQLite 中的行数。

如果已启用 BM25：

1. Query(查询) 时，读取 `wiki/index.md`，运行 `python3 scripts/wiki_fts.py stats`；如果 `Fresh: no` 则重建；运行 `python3 scripts/wiki_fts.py search "{query}" --limit 10`；打开返回的页面；然后使用 wiki 页面引用作答。
2. Ingest(摄取) 时，在创建新的实体、概念、比较、综合或领域专用页面前搜索 BM25，以避免重复页面。
3. Ingest(摄取) 后，如果 `EXTEND.md` 中启用了 `auto_rebuild_after_ingest`，运行 `python3 scripts/wiki_fts.py build`。
4. Lint(检查) 时，运行 `python3 scripts/wiki_fts.py stats`；如果索引过期，重建或记录警告。
5. 如果 BM25 失败且偏好允许回退，继续使用 `wiki/index.md` 和 `rg`。

Normal Query(普通查询) 指 LLM 问答：使用 `stats` 检查新鲜度，尽可能重建过期索引，使用 `search`，打开返回的 `page_path` 文件，阅读完整 wiki 上下文，并引用 wiki 页面。Export Use(导出使用) 则用于运维、审计、迁移、调试或外部分析等任务；当 `search` 可用时，不要把导出文件作为正常查询路径。

搜索输出字段：

| 字段           | 含义                                                                               | 用法                             |
| -------------- | ---------------------------------------------------------------------------------- | -------------------------------- |
| `page_path`    | 包含匹配内容的 wiki 页面路径；相对于生成的 wiki／项目根目录，并包含 `wiki/` 前缀。 | 回答前，先打开此页面。           |
| `heading_path` | 页面内的标题路径。                                                                 | 定位相关的章节。                 |
| `chunk_id`     | `{page_path}#{ordinal}` 诊断标识符。                                               | 不要引用。                       |
| `score`        | 查询本地 SQLite的 FTS5 BM25 分数；越低越相关，值可能为负。                         | 仅用于对单次查询的候选结果排序。 |
| `snippet`      | 截断的文本片段预览。                                                               | 绝不能仅根据文本片段回答。       |

在面向用户的回答中，切勿引用 `chunk_id`、`score`、`indexes/fts.sqlite` 或 `exports/*` 作为证据。BM25 数据用于查找候选页面；wiki 页面才是引用目标。

BM25 数据模型在 `indexes/README.md` 中有详细的文档说明。其导出的表格中确实包含这些字段：

```text
chunk_id, page_path, title, type, heading_path, ordinal, sources, tags, updated, text
```

## Index Protocol 索引协议

`wiki/index.md` 是 LLM 的主要导航工具。结构如下：

```markdown
# Index

## Core Maps(核心地图)

| File(文件)                               | Purpose(用途)                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [overview(概览).md](<overview(概览).md>) | High-level synthesis of the whole wiki                                                         |
| [concept-table.md](concept-table.md)     | Maintained concept map with types, definitions, relationships, sources, and status |

## Sources(源文件)

| File(文件) | Title(标题) | Date Added(添加日期) | Tags(标签) |
| ---------- | ----------- | -------------------- | ---------- |

## Entities(实体)

| File(文件) | Name(名称) | Type(类型) | Sources(来源) |
| ---------- | ---------- | ---------- | ------------- |

## Concepts(概念)

| File(文件) | Name(名称) | Sources(来源) |
| ---------- | ---------- | ------------- |

## Comparisons(对比)

| File(文件) | Topic(主题) | Sources(来源) |
| ---------- | ----------- | ------------- |

## Synthesis(综合分析)

| File(文件) | Topic(主题) | Sources(来源) |
| ---------- | ----------- | ------------- |
```

每次摄取信息时都应更新。每个小节内的条目按字母顺序排列。

## Concept-Table Protocol(概念表协议)

`wiki/concept-table.md` 是 LLM 对持久概念的压缩地图。它与 `wiki/index.md` 互为补充：索引对页面进行编目，而概念表解释概念的含义、类型和相互关系。

保持以下结构：

```markdown
## Maintenance Rules

## Concept Clusters

| Cluster | Concepts | Current interpretation |
| ------- | -------- | ---------------------- |

## Concepts

| Concept(概念) | Concept type(概念类型) | Working definition(工作定义) | Role in this wiki(作用) | Sources(来源) | Related pages(相关页面) | Status(状态) |
| ------------- | ---------------------- | ---------------------------- | ----------------------- | ------------- | ----------------------- | ------------ |
```

规则：

- `wiki/concepts/` 下的每个持久化的概念页面都保留一行
- 每当概念页面被创建、重命名、删除、合并、拆分或实质性修订时，更新对应行
- 按概念名称的字母顺序排列各行
- 定义保持简洁并体现证据情况；详细内容链接到完整概念页面
- `Concept type` 仅使用以下候选类型：
  - `原理`：解释为什么某件事成立
  - `机制`：解释某件事如何发生
  - `方法`：说明如何完成某项任务
  - `模型／框架`：组织多个概念或步骤
  - `分类`：划分不同类型或层次
  - `区分`：澄清容易混淆的对象
  - `状态／属性`：描述对象的重要特征
  - `评价标准`：判断某事是否成立或完成的依据
  - `产出`：某种方法预期生成的稳定结果
- `Status` 使用 `high confidence`、`single-source`、`tentative`、`needs sources` 或 `contradicted` 等值
- 列标题保持中英文，因为它们是协议标识符；行内容使用相关概念页面的语言

## naming rules文件名约定

所有新生成的来源、实体、概念、比较、综合和概览页面都必须使用以下格式：

```text
english-slug(中文标题).md
```

- 所有新页面使用 `english-slug(中文标题).md`，例如 `attention-is-all-you-need(注意力就是一切).md`，是稳定的页面标识。
- `english-slug` 使用小写 ASCII、连字符分隔且不含空格。
- `中文标题` 使用页面正式中文标题；全角标点可以保留在括号内。
- YAML `title`、`wiki/index.md` 显示名、`wiki/concept-table.md` 显示名和 wikilink 标签使用`english-slug(中文标题)`。
- `raw/` 中的原始文件不重命名；`sources` frontmatter 仍只记录原始文件名。
- 创建页面前，在确认清单中展示最终文件名。若目标文件已存在，则更新该页面，不因标题变化创建重复页面。

## log protocol 日志协议

`wiki/log.md` 仅允许追加。每次操作都添加一个条目。格式：

```text
## [YYYY-MM-DD] {operation} | {subject}
- {details as bullet points}
```

可使用以下命令解析：`grep "^## \[" wiki/log.md | tail -10`

## Conventions 约定俗成的规定/惯例

- 每页只包含一个概念。如果某个页面包含超过两个不同的概念，则将其拆分为多个页面。
- 结构化比较优先使用表格。
- 当存在不确定性时，应该明确注明这种不确定性，而不是忽略它。
- 务必保留原文中的原始陈述——进行准确的总结，同时单独提出批评意见。
- 在 `sources` frontmatter 中只使用文件名（例如 `[article(文章).md, paper(论文).md]`），不要使用 `raw/article(文章).md` 之类的完整路径

## Language 语言

所有 wiki 内容 MUST 与正在 ingest 的来源语言一致：

1. **检测**：每次摄取时，在写入任何 wiki 页面前检测来源的主要语言。
2. **内容页面**：来源摘要、实体页面、概念页面及所有衍生内容使用来源语言编写。
3. **结构元素保持中英文**：YAML frontmatter 键、`type` 值、文件名 slug、表格列标题，以及 `index.md`／`log.md` 中的 Markdown 小节标题保持中英文——它们是协议标识符，不是内容。
4. **跨来源页面**：对于需要比较、综合以及概述多个来源的内容，应使用大多数来源所使用的语言。如果有多重选择，请征求用户的意见。
5. **对话**：与用户讨论关键收获（Step2 摄取、查询）时，使用中文。
