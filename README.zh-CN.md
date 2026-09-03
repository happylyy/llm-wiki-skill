# Karpathy LLM Wiki

[English](./README.md)

把文章、论文、书籍、调研笔记等资料编译成由 LLM 持续维护的 Markdown Wiki。

![Karpathy LLM Wiki Bootstrap 封面图](./cover-image/llm-wiki/cover.png)

这个仓库同时包含一个可安装的 Skill 和一个真实参考 Wiki。Skill 用来初始化新的 Wiki；参考 Wiki 展示这套模式如何从 [Karpathy 的 LLM Wiki 原始想法](./karpathy-llm-wiki-original.md) 出发，逐步长出持久页面、链接、概念、对比和综合判断。

目标不是做一次总结，而是生成一个可以通过 ingest、query、lint 持续变好的知识工件。

## 为什么需要它

大多数 LLM 文档工作流仍然停留在 query-time RAG：检索几个片段、回答当前问题，然后中间结构就消失了。LLM Wiki 把更多工作沉淀到一个可维护的 Markdown 层里。

| 层级        | 用途                                                                         |
| ----------- | ---------------------------------------------------------------------------- |
| `raw/`      | 不可变的原始资料和证据                                                       |
| `wiki/`     | LLM 持续维护的摘要、概念、实体、对比和综合                                   |
| `SCHEMA.md` | 所有 agent 共同遵循的操作契约                                                |
| 指针文件    | `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` 等轻量运行时入口 |

结果是一个会复利的 Wiki：新资料会更新旧页面，有价值的回答可以归档回来，lint 会持续检查结构健康。

## 仓库包含什么

- [skill/](./skill)：可安装的 Skill 包，包含模板和工作流。
- [llm-wiki/](./llm-wiki)：使用该 Skill 生成并维护过的真实参考 Wiki。
- [karpathy-llm-wiki-original.md](./karpathy-llm-wiki-original.md)：原始想法笔记的仓库内副本。
- [from-article-to-llm-wiki.article.zh-CN.md](./from-article-to-llm-wiki.article.zh-CN.md)：完整中文 walkthrough。

## 快速开始

安装 Skill：

```bash
npx skills add happylyy/Karpathy-llm-wiki-bootstrap-skill@llm-wiki-v1
```

然后对你的 agent 说：

```text
初始化一个 wiki
```

初始化时可以这样选择：

| 问题            | 示例回答                                             |
| --------------- | ---------------------------------------------------- |
| Domain          | `Research topic`                                     |
| Wiki name       | `llm-wiki-demo`                                      |
| Runtime         | `OpenAI Codex`、`Claude Code` 或 `Copilot (VS Code)` |
| Editor          | `Obsidian` 或 `VS Code`                              |
| Source types    | `Web articles`                                       |
| Output location | `Current directory`                                  |

添加原始资料：

```bash
cp karpathy-llm-wiki-original.md llm-wiki-demo/raw/
```

然后对 agent 说：

```text
Read llm-wiki-demo/SCHEMA.md, then ingest llm-wiki-demo/raw/karpathy-llm-wiki-original.md
```

第一次 ingest 后，重点查看：

- `llm-wiki-demo/wiki/index.md`
- `llm-wiki-demo/wiki/concept-table.md`
- `llm-wiki-demo/wiki/overview.md`
- `llm-wiki-demo/wiki/log.md`

如果你想从一开始就构建中文 Wiki，直接告诉 agent：

```text
使用中文编译 karpathy-llm-wiki-original.md
```

## 参考 Wiki

[llm-wiki/](./llm-wiki) 是最快理解这套系统的入口。它不是占位内容，而是一个由真实资料生成并维护过的示例 Wiki。

建议先看：

| 文件                                                               | 为什么看它                                           |
| ------------------------------------------------------------------ | ---------------------------------------------------- |
| [llm-wiki/SCHEMA.md](./llm-wiki/SCHEMA.md)                         | agent 操作规则的权威契约                             |
| [llm-wiki/wiki/index.md](./llm-wiki/wiki/index.md)                 | 所有 Wiki 页面目录                                   |
| [llm-wiki/wiki/concept-table.md](./llm-wiki/wiki/concept-table.md) | 持续维护的概念地图：定义、关系、来源、状态、维护备注 |
| [llm-wiki/wiki/overview.md](./llm-wiki/wiki/overview.md)           | 整个 Wiki 的顶层综合                                 |
| [llm-wiki/wiki/log.md](./llm-wiki/wiki/log.md)                     | 按时间记录的操作历史                                 |

当前结构：

```text
llm-wiki/
├── SCHEMA.md
├── AGENTS.md
├── raw/
│   ├── Karpathy x.md
│   └── llm-wiki-pattern.md
└── wiki/
    ├── index.md
    ├── concept-table.md
    ├── overview.md
    ├── log.md
    ├── concepts/
    ├── entities/
    ├── comparisons/
    ├── sources/
    └── synthesis/
```

## 核心工作流

| 操作   | 触发方式                 | 结果                                                           |
| ------ | ------------------------ | -------------------------------------------------------------- |
| Ingest | `ingest raw/{file}`      | 读取资料，创建或更新 Wiki 页面，并更新概念表、索引、总览和日志 |
| Query  | 直接提领域问题           | 读取索引和相关页面，可选使用 BM25，然后用 Wiki 页面引用回答    |
| Lint   | `lint` 或 `health check` | 检查矛盾、过期结论、孤儿页、概念表漂移和缺失链接               |

每个 Wiki 的关键文件：

| 文件                    | 作用                                         |
| ----------------------- | -------------------------------------------- |
| `SCHEMA.md`             | agent 行为的单一真源                         |
| `wiki/index.md`         | 页面目录和主要导航面                         |
| `wiki/concept-table.md` | 压缩概念地图：定义、关系、证据状态、维护备注 |
| `wiki/overview.md`      | 顶层综合判断                                 |
| `wiki/log.md`           | 追加式操作历史                               |

## 可选 BM25 搜索

当 Wiki 变大后，Skill 可以初始化一个本地 SQLite FTS5/BM25 搜索层。BM25 只是候选召回工具，不是知识真源：agent 必须打开返回的 `wiki/` 页面后再回答。

在生成的 Wiki 内常用命令：

```bash
python3 scripts/wiki_fts.py doctor
python3 scripts/wiki_fts.py build
python3 scripts/wiki_fts.py search "query text" --limit 10
python3 scripts/wiki_fts.py stats
```

完整流程和数据模型规则见 [skill/references/workflows/bm25.md](./skill/references/workflows/bm25.md)。

## 安装说明

使用复数形式的 CLI：

```bash
npx skills add nanzhipro/Karpathy-llm-wiki-bootstrap-skill@llm-wiki-v1
```

非交互式用户级安装：

```bash
npx skills add nanzhipro/Karpathy-llm-wiki-bootstrap-skill@llm-wiki-v1 -g -y
```

更新已有安装：

```bash
npx skills update llm-wiki-v1
```

不要使用 `npx skill ...`；那是另一个 CLI。

## 文档入口

| 主题                 | 链接                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------- |
| 完整中文 walkthrough | [不是读完就算](./from-article-to-llm-wiki.article.zh-CN.md)                            |
| 英文 walkthrough     | [Reading Is Not Enough](./from-article-to-llm-wiki.article.en.md)                      |
| Skill 入口           | [skill/SKILL.md](./skill/SKILL.md)                                                     |
| Bootstrap 工作流     | [skill/references/workflows/bootstrap.md](./skill/references/workflows/bootstrap.md)   |
| Ingest 工作流        | [skill/references/workflows/ingest.md](./skill/references/workflows/ingest.md)         |
| Query 工作流         | [skill/references/workflows/query.md](./skill/references/workflows/query.md)           |
| Lint 工作流          | [skill/references/workflows/lint.md](./skill/references/workflows/lint.md)             |
| BM25 工作流          | [skill/references/workflows/bm25.md](./skill/references/workflows/bm25.md)             |
| 偏好配置 schema      | [skill/references/config/extend-schema.md](./skill/references/config/extend-schema.md) |

## 来源

这个仓库基于 Karpathy 的 LLM Wiki 原始笔记：

- 原始 gist：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- 仓库内副本：[karpathy-llm-wiki-original.md](./karpathy-llm-wiki-original.md)

这个项目把这套想法封装成一个可安装 Skill，并用一个持续维护的参考 Wiki 展示它如何实际运行。
