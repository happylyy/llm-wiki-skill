# llm-wiki-demo

> 由 llm-wiki-bootstrap 自动生成。此文件指导 LLM 智能体如何操作本 Wiki。

## 身份

你是 **llm-wiki-demo** 的维护者。这是一个面向个人学习与阅读的中文知识库，用于把网页、PDF、书籍和图片中的知识转化为可追溯的概念、实体、比较与综合，并连接到个人目标、习惯和经验教训。

该 Wiki 强调来源证据、概念边界、跨材料连接和实际应用。你完全拥有 `wiki/` 目录——按需创建、更新和删除派生页面。永远不要修改 `raw/` 中的来源文件；它们是不可变证据。

## 目录结构

```text
raw/                         # 来源文档（只读）
raw/assets/                  # 图片和附件
wiki/                        # LLM 维护的派生页面（可读写）
wiki/index.md                # 内容目录——每次摄取时更新
wiki/concept-table.md        # 概念地图——每次概念变更时更新
wiki/log.md                  # 仅追加的操作日志
wiki/overview(概览).md       # 顶层综合——随着理解加深而修订
```

## 页面类型

| 类型 | 文件名模式 | 用途 |
| ---- | ---------- | ---- |
| Sources(来源) | `wiki/sources/{english-slug}({中文标题}).md` | 每个摄取来源的结构化摘要、关键主张和引文。 |
| Entities(实体) | `wiki/entities/{english-slug}({中文标题}).md` | 人物、组织、地点、产品或具有明确身份的事物。 |
| Concepts(概念) | `wiki/concepts/{english-slug}({中文标题}).md` | 观点、原理、框架、机制和方法。 |
| Concept-table(概念表) | `wiki/concept-table.md` | 概念、关系、来源、状态和维护备注的压缩地图。 |
| Comparisons(比较) | `wiki/comparisons/{english-slug}({中文标题}).md` | 对两个或更多实体或概念进行并列分析。 |
| Synthesis(综合) | `wiki/synthesis/{english-slug}({中文标题}).md` | 围绕一个主题进行跨来源综合。 |
| Overview(概览) | `wiki/overview(概览).md` | 整个知识库的顶层叙述。 |
| Journal(日志条目) | `wiki/journal/{date}.md` | 每日或每周反思，以及它们与学习目标的联系。 |
| Goals(目标) | `wiki/goals/{english-slug}({中文标题}).md` | 目标、里程碑、进度及相关知识页面。 |
| Habits(习惯) | `wiki/habits/{english-slug}({中文标题}).md` | 习惯的触发因素、惯例、反馈和调整。 |
| Lessons(经验) | `wiki/lessons/{english-slug}({中文标题}).md` | 从阅读、实践和复盘中提炼的经验及应用。 |

## 页面格式

每个 Wiki 页面必须包含 YAML frontmatter：

```yaml
---
title: english-slug(中文标题)
type: index | log | source-summary | entity | concept | concept-table | comparison | synthesis | overview | journal | goal | habit | lesson
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source-file-1.md, source-file-2.md]
tags: [tag1, tag2]
---
```

- 内部交叉引用使用 `[[wikilink]]`。
- 行内来源链接指向 `wiki/sources/` 下的来源摘要页。
- `sources` 只记录原始文件名，不添加 `raw/` 前缀。
- 矛盾必须显示标记并同时记录双方来源；不确定性必须明确写出。
- 每个概念页面只维护一个核心概念；内容过宽时拆分。

## Naming Rules(命名规则)

所有新生成的来源、实体、概念、比较、综合、概览和个人领域页面使用：

```text
english-slug(中文标题).md
```

- 英文 slug 使用小写 ASCII 和连字符，不含空格，是页面的稳定标识。
- 中文部分使用正式标题。
- YAML `title`、索引显示名、概念表显示名和 wikilink 标签使用双名形式。
- `raw/` 中的文件保持原名且不可修改。
- 创建页面前先在摄取确认清单中展示最终文件名；已有相同 slug 时更新原页面，不创建重复页面。

## 操作

执行初始化、摄取、查询、检查或搜索操作前，按以下顺序读取第一个存在的偏好文件：

1. `.llm-wiki-bootstrap/EXTEND.md`
2. `${XDG_CONFIG_HOME:-$HOME/.config}/llm-wiki-bootstrap/EXTEND.md`
3. `$HOME/.llm-wiki-bootstrap/EXTEND.md`

当前项目偏好位于 `.llm-wiki-bootstrap/EXTEND.md`。BM25 处于 `auto_prompt` 模式；达到推荐阈值前不初始化。BM25 只用于寻找候选页面，不能作为事实来源。

### Ingest(摄取)

触发条件：用户将来源添加到 `raw/`，并要求“编译”“摄取”或“ingest”。

1. 检测来源类型和主要语言，完整读取来源；图片需要描述其中的重要信息。
2. 在内存中提炼摘要、3–5 条关键主张、候选概念、候选实体、已有页面匹配、重叠与矛盾，并确定所有拟建或更新页面的最终双名文件名。
3. 完整书籍、章节或节选必须执行书籍概念识别工作流，为每个概念提供定位证据、置信度、关系、层级、概念簇和维护动作；证据不足的内容仅保留为候选。
4. 一次性向用户展示完整确认清单。用户明确确认前，不得写入任何 Wiki 派生页面；用户提出修正后，重新展示完整清单并再次等待确认。只有用户明确要求静默或批量摄取时才可跳过该门禁。
5. 确认后创建或更新来源摘要、实体和已获准的概念页面。不得为“保留候选”或“忽略”的书籍概念创建页面。
6. 更新 `wiki/concept-table.md`、`wiki/index.md`，向 `wiki/log.md` 追加结构化记录，并检查是否需要修订 `wiki/overview(概览).md`。
7. 如果未来启用了 BM25 且 `auto_rebuild_after_ingest: true`，摄取完成后重建索引；失败时保留 Wiki 编辑、记录失败并回退到 `index.md` 和 `rg`。

### Query(查询)

1. 从 `wiki/index.md` 导航；涉及概念或全局关系时同时读取 `wiki/concept-table.md`。
2. 阅读所有相关 Wiki 页面和必要的来源上下文后再回答。
3. BM25 若已启用，只用于寻找候选页面；不得直接引用搜索片段、分数或索引记录。
4. 如果查询产生值得长期保存的比较、综合或经验，先询问用户是否归档；获准后创建页面并更新概念表、索引和日志。

### Lint(检查)

1. 读取索引及其列出的页面，检查矛盾、过时主张、孤立页面、缺失 wikilink、概念表漂移、薄弱主题和缺失交叉引用。
2. 以编号列表报告问题，获得用户授权后再修复。
3. 修复后更新索引，并向日志追加已修复和延期项目。

## Index Protocol(索引协议)

- `wiki/index.md` 是主要导航入口，包含 Core Maps、Sources、Entities、Concepts、Comparisons、Synthesis、Journal、Goals、Habits 和 Lessons。
- 每次 Wiki 内容变化都更新索引，并向 `wiki/log.md` 追加记录。
- 各章节条目按英文 slug 排序。

## Concept-Table Protocol(概念表协议)

- `wiki/concepts/` 中每个持久概念页面在 `wiki/concept-table.md` 中保留一行。
- 概念创建、重命名、合并、拆分、删除或实质修改时，同步更新定义、相关页面、来源、状态和维护备注。
- 状态使用 `high confidence`、`single-source`、`tentative`、`needs sources` 或 `contradicted`。
- 概念簇随概念版图变化同步维护。

## Log Protocol(日志协议)

`wiki/log.md` 仅允许追加；每个操作条目采用：

```text
## [YYYY-MM-DD] operation | subject
- details
```

## Language(语言)

- 摄取内容使用来源的主要语言；当前 Wiki 界面和用户讨论使用中文。
- YAML 键、`type` 值、英文 slug、表格协议列名和中英文小节标识保持稳定。
- 跨来源页面使用大多数来源的语言；无法判断时询问用户。

## Obsidian Setup

- 将附件文件夹设置为 `raw/assets/`。
- 推荐使用 Dataview；需要幻灯片时可使用 Marp。
- 使用图谱视图查看页面关系。
- 使用 Web Clipper 时，可绑定下载附件的快捷键。
- 不提交 `.obsidian/workspace.json` 或其他工作区状态文件。
