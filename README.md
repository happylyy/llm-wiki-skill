# Karpathy LLM Wiki Bootstrap

一个可安装的 Skill，用于把文章、论文、书籍、研究笔记和其他资料编译成可持续维护的 Markdown Wiki。

它将原始资料、结构化知识和 agent 操作规则分层保存，让知识能够在持续摄取新资料的过程中不断累积、修订和关联。

## 核心理念

传统的文档问答通常在每次查询时重新检索和总结资料。LLM Wiki 则把理解和整理工作提前到资料摄取阶段，并将结果保存为可以长期维护的 Markdown 页面。

| 层级        | 用途                                                |
| ----------- | --------------------------------------------------- |
| `raw/`      | 保存不可变的原始资料和证据                          |
| `wiki/`     | 保存由 LLM 维护的来源、实体、概念、比较和综合页面   |
| `SCHEMA.md` | Wiki 的唯一操作契约，规定 agent 如何读取和维护内容  |
| 指针文件    | 为 Codex、Claude Code 或 Copilot 提供轻量运行时入口 |
| `EXTEND.md` | 保存 BM25、摄取和搜索等用户偏好                     |

核心原则是：原始证据保持不变，派生知识持续演进，所有重要变化都通过索引、概念表和日志沉淀下来。

## 安装

使用 Skills CLI 安装：

```bash
npx skills add happylyy/llm-wiki-skill@llm-wiki-v1
```

安装到用户级目录并跳过交互确认：

```bash
npx skills add happylyy/llm-wiki-skill@llm-wiki-v1 -g -y
```

更新已有安装：

```bash
npx skills update llm-wiki-v1
```

请使用复数形式的 `skills` CLI，不要使用 `npx skill ...`。

## 快速开始

安装完成后，让 agent 执行：

```text
初始化一个 wiki
```

初始化时，Skill 会收集以下设置：

- Wiki 的主题和范围
- Wiki 名称
- 使用的运行时，例如 OpenAI Codex、Claude Code 或 Copilot
- 主要编辑器，例如 Obsidian 或 VS Code
- 资料类型，例如网页、PDF、书籍、会议记录、图片或数据文件
- Wiki 的输出位置

完成设置后，Skill 会生成 Wiki 骨架、`SCHEMA.md`、运行时指针文件，以及可选的编辑器和偏好配置。

## 生成的 Wiki 结构

```text
wiki-root/
├── raw/                        # 不可变的原始资料
├── wiki/
│   ├── index.md                # 页面目录和主要导航
│   ├── concept-table.md        # 持久化概念地图
│   ├── log.md                  # 追加式操作日志
│   └── overview(概览).md       # Wiki 的顶层综合
├── SCHEMA.md                   # 唯一操作契约
├── AGENTS.md                   # Codex 指针（按运行时选择）
├── .llm-wiki-v1/
│   └── EXTEND.md               # 项目级偏好（可选）
└── .gitignore
```

如果选择其他运行时，Skill 也可以生成对应的 `CLAUDE.md` 或 `.github/copilot-instructions.md`。如果来源包含图片或图表，可以使用 `raw/assets/` 保存附件。

## 核心工作流

### Bootstrap：初始化

创建一个新的 Wiki 骨架，并生成：

- 只读的 `raw/` 来源层
- 可维护的 `wiki/` 页面层
- 作为唯一事实来源的 `SCHEMA.md`
- 运行时指针文件和编辑器配置
- 用户选择的 `EXTEND.md` 偏好文件

未经明确批准，Skill 不会覆盖现有 Wiki。

### Ingest：摄取资料

将资料放入 `raw/` 后，告诉 agent：

```text
使用中文编译 raw/{filename}
```

摄取流程会先完整读取来源，提炼摘要、关键主张、候选概念和实体，并在获得用户确认后创建或更新 Wiki 页面。随后更新：

- `wiki/index.md`
- `wiki/concept-table.md`
- `wiki/overview(概览).md`（必要时）
- `wiki/log.md`

原始资料只读，Skill 不会直接修改 `raw/` 中的来源文件。

### Query：查询 Wiki

对于领域问题，agent 会先读取 `wiki/index.md`，再打开相关 Wiki 页面；涉及概念关系或全局性问题时，也会读取 `wiki/concept-table.md`。

回答应引用 Wiki 页面，而不是直接把原始搜索片段或 BM25 片段当作证据。由查询产生的高价值比较或综合分析，也可以在用户确认后归档为新的 Wiki 页面。

### Lint：检查健康状况

使用以下触发词：

```text
lint
```

或：

```text
health check
```

检查内容包括：

- 页面之间的矛盾和过时主张
- 孤立页面和缺失的 wikilink 目标
- 概念表漂移
- 薄弱领域
- 相关页面之间缺少的交叉引用

Skill 会先报告问题，并在用户明确选择后执行修复。

## 偏好配置

Skill 会按照以下顺序查找第一个可用的 `EXTEND.md`：

1. 项目内的 `.llm-wiki-v1/EXTEND.md`
2. XDG 配置目录中的 `llm-wiki-v1/EXTEND.md`
3. 用户目录中的 `.llm-wiki-v1/EXTEND.md`

偏好文件可以控制：

- BM25 提醒模式和阈值
- 摄取后的索引重建策略
- 是否包含原始资料
- 文本分块大小和重叠范围
- 搜索导出格式

首次使用时，如果不存在偏好文件，Skill 会先询问偏好位置和 BM25 设置，不会静默使用默认值。

详细字段定义见 [`skill/references/config/extend-schema.md`](./skill/references/config/extend-schema.md)。

## 可选 BM25 搜索

Wiki 规模较大后，可以初始化本地 SQLite FTS5/BM25 搜索层。BM25 只负责从 Wiki 页面中查找候选内容，不是事实来源。

查询时必须打开并阅读 BM25 返回的完整 Wiki 页面，再使用页面内容回答。索引缺失或重建失败时，可以回退到 `wiki/index.md` 和文本搜索。

常用命令：

```bash
python3 scripts/wiki_fts.py doctor
python3 scripts/wiki_fts.py build
python3 scripts/wiki_fts.py search "query text" --limit 10
python3 scripts/wiki_fts.py stats
```

默认情况下，Skill 不会在初始化时自动创建 BM25 文件；是否提醒和何时重建由 `EXTEND.md` 控制。

## 文档入口

| 主题             | 链接                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------- |
| Skill 总入口     | [`skill/SKILL.md`](./skill/SKILL.md)                                                     |
| Bootstrap 工作流 | [`skill/references/workflows/bootstrap.md`](./skill/references/workflows/bootstrap.md)   |
| Ingest 工作流    | [`skill/references/workflows/ingest.md`](./skill/references/workflows/ingest.md)         |
| Query 工作流     | [`skill/references/workflows/query.md`](./skill/references/workflows/query.md)           |
| Lint 工作流      | [`skill/references/workflows/lint.md`](./skill/references/workflows/lint.md)             |
| BM25 工作流      | [`skill/references/workflows/bm25.md`](./skill/references/workflows/bm25.md)             |
| 偏好配置 schema  | [`skill/references/config/extend-schema.md`](./skill/references/config/extend-schema.md) |
| 模板目录         | [`skill/references/templates/`](./skill/references/templates/)                           |

## 许可证与来源

本项目基于 Karpathy 关于持久化 LLM Wiki 的思路，将其整理为可安装、可配置、可持续维护的 Skill。
