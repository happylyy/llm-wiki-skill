---
name: llm-wiki-bootstrap
description: >
  引导创建和操作 LLM Wiki：一个持久化的 Markdown 知识库，其中包含不可变的原始资料、
  由 LLM 维护的 wiki、作为操作契约的 SCHEMA.md、精简的运行时指针文件、作为偏好配置的EXTEND.md，以及可选的本地 BM25 搜索。当用户要求创建或初始化 LLM wiki、摄取(ingest)资料、
  查询(query)或检查(lint) wiki、配置 EXTEND.md 偏好，或为 LLM Wiki 设置 BM25/全文搜索时使用。
---

# LLM Wiki 引导

构建和维护一个个人 LLM Wiki：原始证据在 `raw/` 中保持不可变，经过整理的知识被编译到 `wiki/` 中，`SCHEMA.md` 是该Wiki的唯一操作规范。

本文档有意保持简短。仅加载用户所请求操作对应的详细参考资料。

## 操作模型

- 将 `SCHEMA.md` 作为每个所生成 wiki 中的唯一事实来源。
- 将 `wiki/concept-table.md` 作为根层持续维护的概念地图：它汇总书籍目录(Books)、跨书概念关联(Cross-book Concept Links)以及非书籍来源的持久性概念(concepts)、概念类型(concept types)、关系(relationships)、来源(sources)以及状态(status)，补充 wiki/index.md 的内容。每本书籍类来源的概念另存放于自己独立的 `wiki/books/{book-slug}(书名)/concept-table.md`，与其他书籍完全分开，以便单独浏览。
- 跨书籍的相似概念永不合并为同一页面，只在各自概念页追加跨书关联，并在根概念表记录。
- 将 `CLAUDE.md`、`AGENTS.md` 和 `.github/copilot-instructions.md` 保持为指向 `SCHEMA.md` 的精简指针；切勿在其中复制操作规则。
- 将 `raw/` 视为只读证据。仅在 `wiki/` 下创建和更新派生知识。
- 在执行初始化（bootstrap）、摄取（ingest）、查询（query）、检查（lint）或 BM25 工作之前应用 `EXTEND.md` 中的偏好。
- 仅询问缺失的决策信息，同时尽可能将批量设置的问题整合到一个用户提示中。
- 优先采用渐进式披露方式：读取能够完成当前任务的最小参考文件。

## 意图路由

| 用户意图                    | 执行操作                                                                                                                                                                                | 参考资料                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 初始化或引导建立新的 wiki   | 运行偏好预检，收集所需的设置信息，然后生成框架结构和初始化文件。                                                                                                                        | `references/workflows/bootstrap.md`                                                        |
| 摄取一个或多个资料来源      | 运行偏好预检，检查可选的 BM25 门控，然后将来源知识编译到 `wiki/` 中；书籍类来源额外执行概念识别工作流，并独立存储到 `wiki/books/{book-slug}(书名)/`，同时识别与其他书籍的跨书概念关联。 | `references/workflows/ingest.md`；书籍类来源另读 `references/workflows/ingest_concepts.md` |
| 将 PDF 转为 Markdown（OCR） | 运行偏好预检，从 `EXTEND.md` 读取 `pdf_ocr` 配置，运行 `scripts/pdf_to_markdown.py` 生成 `raw/{stem}.md`，再交给摄取工作流。                                                            | `references/workflows/pdf-to-markdown.md`                                                  |
| 根据 wiki 回答领域问题      | 运行偏好预检，从 `wiki/index.md` 导航，仅将 BM25 用作候选查找器，然后引用 wiki 页面。                                                                                                   | `references/workflows/query.md`                                                            |
| 检查 wiki 健康状况或一致性  | 运行偏好预检，扫描结构和内容，报告发现，然后仅修复获准的项目。                                                                                                                          | `references/workflows/lint.md`                                                             |
| 配置或使用 BM25 搜索        | 加载偏好，在初始化前询问，创建本地搜索文件，执行冒烟测试，并记录结果。                                                                                                                  | `references/workflows/bm25.md`                                                             |
| 配置偏好                    | 使用schema和模板(template)来定位或创建 `EXTEND.md`。                                                                                                                                    | `references/config/extend-schema.md`、`references/templates/extend.md`                     |

## 偏好预检

在执行任何工作流(bootstrap, ingest, query, lint, or BM25)前，先读取 `references/config/extend-schema.md`，按照查找顺序使用第一个可用的 `EXTEND.md`。如果不存在，则应先运行首次偏好设置，从 references/templates/extend.md 开始配置一个 `EXTEND.md`以继续操作。
会话中首次使用时说明当前启用的偏好文件；不得静默使用默认值。

## Reference加载规则

- Bootstrap功能：读取 `references/workflows/bootstrap.md`的内容，当需要创建特定文件时，再按需加载模板。
- 对于摄取(ingest)、查询(query)和检查(lint)：先读取匹配的工作流文件；仅当偏好或用户请求需要搜索行为时，才读取 `references/workflows/bm25.md`。
- 摄取完整书籍、章节或书籍节选时：在 `references/workflows/ingest.md` 判定来源类型后，额外读取并完整执行 `references/workflows/ingest_concepts.md`；非书籍来源不得加载该子流程。书籍类来源的概念页和概念表存放于 `wiki/books/{book-slug}(书名)/` 下，与其他书籍分开；跨书关联只记录在根 `wiki/concept-table.md`。
- 生成或更新概念页时：读取 `references/templates/concepts.md`，以完整模板为基础填充概念；允许追加自定义章节，但不得删除模板字段。
- 首次为某本书创建独立概念表时：读取 `references/templates/book-concept-table.md`，不要复用根概念表模板。
- Schema生成：读取 `references/templates/schema.md`的内容，并按需注入 `references/templates/domain-page-types.md`。
- 指针文件：读取 `references/templates/agent-pointer.md` 的内容，并保持精简。
- 初始化BM25：只有在用户确认后，才读取 `references/templates/wiki_fts.py` 和 `references/templates/bm25-readme.md` 的内容。

## package布局规则

- 将skill中用于辅助执行的脚本，放到scripts/ 中。
- `scripts/pdf_to_markdown.py` 是 skill 自有辅助脚本（调用 PaddleOCR 把 PDF 转为 Markdown），不会被复制进生成的 wiki。
- 将生成输出使用的模板放入 `references/templates/`。虽然这样生成的文件在复制到用户的 Wiki 页面后可能会变得可执行，但这样做仍然是一种有效的做法。
- 将长流程放入 `references/workflows/` 目录下，将偏好配置文件放在 `references/config/` 目录下。
- 在这个技能中，`references/templates/raw_ingest_validate.py` 是生成 wiki 中的 `scripts/raw_ingest_validate.py`的模板。
- 在这个技能中，`references/templates/wiki_fts.py` 是生成的维基页面中 `scripts/wiki_fts.py` 的模板；该模板并不会由技能直接执行。。

## 硬性规则

- 未经用户明确批准，绝不覆盖现有 wiki。
- 除了在引导创建期间创建 `.gitkeep` 等空骨架占位符之外，绝不修改 `raw/` 中的文件。
- 切勿直接根据 BM25 片段作答；必须先打开并阅读返回的 wiki 页面。
- 摄取时首先使用来源语言理解材料，然后生成wiki，除非用户明确要求使用其他语言的 wiki 界面。
- 所有新生成的 wiki 页面（来源、实体、概念、比较、综合和概览）必须使用 `english-slug(中文标题).md` 文件名：英文部分为小写 ASCII 连字符 slug，中文部分为正式页面标题。
- 文件名中的英文 slug 是稳定标识；如果目标文件已存在，则更新该页面，不得仅因中文标题差异创建重复页面。
- 书籍类来源的概念必须存放于 `wiki/books/{book-slug}(书名)/concepts/` 下，与其他书籍完全分开；`book-slug` 一旦创建不因该书标题措辞变化而重命名，同一本书的多个分卷/章节共用同一个文件夹。
- 跨书籍的相似概念永不合并为同一页面；`合并` 动作仅限同书内部的同义词/别名归并。
- 每当 wiki 内容发生变化时，更新 `wiki/index.md` 并追加写入 `wiki/log.md`。
- 如果搜索索引重建失败，保留 wiki 编辑，记录失败，并回退到 `wiki/index.md` 加文本搜索。

## 核心输出

成功的引导创建会生成一个包含以下内容的 wiki 根目录：

```text
raw/
wiki/index.md
wiki/concept-table.md
wiki/log.md
wiki/overview(概览).md
SCHEMA.md
.gitignore
```

可选输出取决于设置答案和偏好：运行时指针文件、`.vscode/settings.json`、`scripts/wiki_fts.py`、`indexes/`、`exports/`，以及仅在摄取过书籍类来源后才会出现的 `wiki/books/{book-slug}(书名)/`。
