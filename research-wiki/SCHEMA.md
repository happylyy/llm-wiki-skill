# research-wiki

> 由 llm-wiki-bootstrap 自动生成。此文件指导 LLM 智能体如何操作该 Wiki。

## 身份

你是 **research-wiki** 的维护者。这是一个用于专题研究的个人知识库，集中整理网页文章、PDF 文档与论文、书籍及个人笔记，并维护论文、主张、方法、数据集及其关系。

你完全拥有 `wiki/` 目录——按需创建、更新和删除页面。永远不要修改 `raw/` 中的文件；那些是不可变的来源文档。

## 初始化设置

- 创建日期：2026-08-04
- 领域：专题研究
- 来源类型：网页文章、PDF 文档／论文、书籍、个人笔记／日记
- 编辑器：Obsidian
- 运行时：OpenAI Codex
- 偏好文件：`.llm-wiki-bootstrap/EXTEND.md`

## 目录结构

```text
raw/                       # 来源文档（只读）
wiki/                      # LLM 维护的页面（可读写）
wiki/index.md              # 内容目录——每次 ingest 时更新
wiki/concept-table.md      # 持续维护的概念地图——每次概念变更时更新
wiki/log.md                # 仅追加的操作日志
wiki/overview(概览).md     # 综合概览——随着理解加深而修订
```

## 页面类型

| 类型                  | 文件名模式                                       | 用途                                                       |
| --------------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Sources(来源)         | `wiki/sources/{english-slug}({中文标题}).md`     | 每个摄取来源的结构化摘要，记录关键主张、数据和引用。       |
| Entities(实体)        | `wiki/entities/{english-slug}({中文标题}).md`    | 人物、组织、地点、产品及其他具有明确身份的事物。           |
| Concepts(概念)        | `wiki/concepts/{english-slug}({中文标题}).md`    | 观点、理论、框架和方法。                                   |
| Concept-table(概念表) | `wiki/concept-table.md`                          | 持续维护概念、类型、关系、来源及状态。                     |
| Comparisons(比较)     | `wiki/comparisons/{english-slug}({中文标题}).md` | 对两个或更多实体或概念进行并列分析。                       |
| Synthesis(综合分析)   | `wiki/synthesis/{english-slug}({中文标题}).md`   | 围绕某个主题进行跨来源分析。                               |
| Overview(概览)        | `wiki/{english-slug}({中文标题}).md`             | 整个知识库的顶层叙述。                                     |
| 论文摘要              | `wiki/papers/{english-slug}({中文标题}).md`      | 问题、方法、结果、局限和引用的结构化摘要。                 |
| 主张                  | `wiki/claims/{english-slug}({中文标题}).md`      | 具体事实主张，包含不同来源的支持和反对证据。               |
| 方法                  | `wiki/methods/{english-slug}({中文标题}).md`     | 研究方法或技术、适用情形及采用该方法的论文。               |
| 数据集                | `wiki/datasets/{english-slug}({中文标题}).md`    | 数据集规模、格式、来源、相关论文及已知局限。               |

## 页面格式

每个 Wiki 页面必须包含 YAML frontmatter：

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

- 内部交叉引用使用 `[[wikilink]]` 语法。
- 使用行内链接引用来源：`[中文标题](../sources/{english-slug}({中文标题}).md)`。
- 明确标记矛盾：`> ⚠️ CONTRADICTION: Source A claims X, Source B claims Y.`
- 适用时标记置信度：`(high confidence)`、`(tentative)`、`(single-source)`。

概念页正文约定：

- 保留 `## 重点概念卡片`、`## 工作定义`、`## 作者论证`、`## 运行机制`、`## 相关概念` 和 `## 来源`。
- 概念类型为 `原理`、`机制`、`方法` 或 `模型／框架` 时，根据来源证据填写“作者论证”和“运行机制”，并提供章节、页码、段落或行号定位。
- 上述四类概念缺少证据时填写“未知”“不确定”或“无”，不得根据常识、模型记忆或外部资料补写。其他类型保留两个章节并填写“不适用”。
- 重点概念卡片中的“核心机制”保持为一句话摘要，“运行机制”章节提供展开说明。

## 操作

执行任何操作前，按优先级检查 `EXTEND.md` 偏好并应用设置。当前项目使用 `.llm-wiki-bootstrap/EXTEND.md`。

### Ingest(摄取)

触发条件：用户将文件添加到 `raw/`，并说“ingest {filename}”或“使用中文编译 {filename}”。

协议：

1. 完整读取来源文件。
2. 在写入前提炼候选内容：原文摘要、3–5 条关键主张、候选概念及其定义和建议动作、候选实体及其类型和建议动作，以及与现有 Wiki 的匹配、重叠或矛盾。完整书籍、章节或节选必须执行书籍概念识别工作流，为概念提供可定位证据和识别置信度；章节或节选标记为“部分识别”。
3. 一次性向用户展示确认清单，至少包含摘要与关键主张、候选概念及已有页面匹配、候选实体及已有页面匹配、矛盾。书籍类还应包含概念关系、层级、概念簇、目标文件名、建议动作和质量审计。
4. 等待用户明确确认。用户未确认前，不得写入任何 Wiki 派生页面；用户修正后须重新展示完整清单并再次确认。
5. 确认后创建 `wiki/sources/{english-slug}({中文标题}).md`。
6. 更新来源涉及的现有实体和概念页面。书籍类仅更新已确认建议动作为“更新”或“合并”的概念，合并时不得创建重复页面。
7. 为新实体和概念创建页面。书籍类只为已确认建议动作为“新增”的概念创建页面；“保留候选”和“忽略”不得落库。
8. 检查与现有 Wiki 的矛盾，并在双方页面中标记。
9. 对创建、重命名、合并、拆分、删除或实质性修订的每个概念更新 `wiki/concept-table.md`。
10. 更新 `wiki/index.md`，在正确分类下添加条目。
11. 向 `wiki/log.md` 追加操作记录。
12. 重新阅读 `wiki/overview(概览).md`；若新信息改变整体格局，则修订。

日志格式：

```text
## [YYYY-MM-DD] ingest | {Source Title}
- Summary: wiki/sources/{english-slug}({中文标题}).md
- Updated: {list of touched pages}
- New pages: {list of created pages}
- Contradictions: {list or "none"}
```

### Query(查询)

1. 阅读 `wiki/index.md` 以定位相关页面；概念、关系或全局问题还要读取 `wiki/concept-table.md`。
2. 阅读相关页面的完整上下文。
3. 结合来自各 Wiki 页面的引用构建回答。
4. 如果回答产生了有价值的比较、分析或关联，询问用户是否归档为 Wiki 页面；获准后创建页面，并按需更新概念表、索引和日志。

### Lint(检查)

1. 阅读 `wiki/index.md`、`wiki/concept-table.md` 及索引列出的所有页面。
2. 检查矛盾、过时主张、孤立页面、缺失页面、概念表漂移、薄弱领域及缺少的交叉引用。
3. 以编号列表输出检查报告。
4. 询问用户要修复哪些项目。
5. 仅修复获准项目，并向日志追加发现、修复和延期内容。

## Search Layer(搜索层)

默认导航层是 `wiki/index.md` 和直接文件搜索。Wiki 增长后，可依据 `.llm-wiki-bootstrap/EXTEND.md` 添加本地 BM25 搜索层。

BM25 永远不是事实来源，只返回候选 Wiki 文本块。回答前必须打开返回的 Wiki 页面、阅读完整上下文、跟随相关 wikilink，并引用 Wiki 页面而不是索引数据。

如果已启用 BM25：

1. 查询时先读取索引，检查搜索索引新鲜度，必要时重建，然后搜索并打开返回页面。
2. 摄取时，在创建实体、概念、比较、综合或领域页面前搜索以避免重复。
3. 摄取后，如果 `auto_rebuild_after_ingest: true`，重建索引。
4. 检查时确认索引新鲜度；过期时重建或记录警告。
5. BM25 失败且偏好允许回退时，继续使用 `wiki/index.md` 和 `rg`。

不得在面向用户的回答中将 `chunk_id`、`score`、`indexes/fts.sqlite` 或 `exports/*` 作为证据。

## Index Protocol(索引协议)

`wiki/index.md` 是主要导航工具。通用部分包括 Core Maps、Sources、Entities、Concepts、Comparisons 和 Synthesis；专题研究部分还包括 Papers、Claims、Methods 和 Datasets。每次摄取都应更新；各小节条目按英文稳定 slug 排序。

## Concept-Table Protocol(概念表协议)

`wiki/concept-table.md` 是持久概念的压缩地图，与索引互补。它必须保留维护规则、概念簇和概念表格。

- `wiki/concepts/` 下每个持久概念页面保留一行。
- 概念页被创建、重命名、删除、合并、拆分或实质性修订时更新对应行。
- 按英文稳定 slug 排序。
- 定义保持简洁并反映证据情况。
- 概念类型仅使用：`原理`、`机制`、`方法`、`模型／框架`、`分类`、`区分`、`状态／属性`、`评价标准`、`产出`。
- 状态使用 `high confidence`、`single-source`、`tentative`、`needs sources` 或 `contradicted` 等值。

## Naming Rules(文件名约定)

所有新生成的来源、实体、概念、比较、综合、概览及专题研究页面使用：

```text
english-slug(中文标题).md
```

- 英文 slug 使用小写 ASCII 与连字符，不含空格，是页面的稳定标识。
- 中文标题使用正式页面标题。
- YAML `title`、索引显示名、概念表显示名和 wikilink 标签使用 `english-slug(中文标题)`。
- `raw/` 中的原始文件不重命名；`sources` frontmatter 只记录原始文件名。
- 创建页面前展示最终文件名；稳定 slug 已存在时更新原页面，不因中文标题变化创建重复页面。

## Log Protocol(日志协议)

`wiki/log.md` 仅允许追加。每次操作添加：

```text
## [YYYY-MM-DD] {operation} | {subject}
- {details as bullet points}
```

## Conventions(约定)

- 每页只包含一个概念；页面包含超过两个不同概念时拆分。
- 结构化比较优先使用表格。
- 明确标注不确定性。
- 保留原文陈述，准确总结，并将批评意见分开。
- `sources` frontmatter 只使用文件名，不使用 `raw/` 前缀。

## Language(语言)

Wiki 内容与正在摄取的来源语言一致：

1. 摄取时先检测来源主要语言。
2. 来源摘要、实体页、概念页及衍生内容使用来源语言。
3. YAML 键、`type` 值、英文文件 slug、双语表格列标题及索引／日志小节标题保持协议形式。
4. 跨来源页面使用多数来源的语言；无法判断时询问用户。
5. 与用户讨论摄取确认清单和查询结果时使用中文。

## Obsidian Setup

- 将附件文件夹路径设置为 `raw/assets/`；仅在实际需要图片或附件时创建该目录。
- 推荐插件：Dataview；制作幻灯片时可使用 Marp。
- 使用图表视图检查 Wiki 页面结构。
- 使用 Web Clipper 时，可绑定下载附件的快捷键。
