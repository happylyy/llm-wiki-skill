# BM25 搜索层

此目录包含本 Wiki 的本地 BM25 全文搜索索引。

BM25 是可选功能。当 Wiki 的规模超出 `wiki/index.md` 和 `rg` 能够轻松覆盖的范围后，它可以帮助 LLM 找到相关的 Markdown 段落。

## BM25 提供的功能

- 对 Wiki 页面进行快速的本地关键词搜索
- 提高对名称、产品、术语、论文标题、API 和特征性措辞的召回率
- 为查询(query）、摄取（ingest）和检查（lint）工作流提供可重建的导航层
- 导出文本块，用于审计、迁移或调试

## BM25 不提供的功能

- 不取代作为知识层的 `wiki/`。
- 不取代作为操作约定的 `SCHEMA.md`。
- 不判断某项主张是否真实。
- 对同义词的理解不如向量嵌入。
- 不生成最终答案。LLM 必须读取返回的 Wiki 页面，并使用常规的 Wiki 引用综合答案。

## LLM 与 BM25 的协作方式

```text
用户提问
  -> LLM 提取术语、实体和意图
  -> BM25 返回候选文本块
  -> LLM 打开匹配的 Wiki 页面
  -> LLM 阅读完整上下文并跟随 Wiki 链接
  -> LLM 使用 Wiki 页面引用作答
```

BM25 是检索辅助工具。Wiki 仍然是事实来源。

## 常规查询与导出使用

**常规查询**是 LLM 回答用户问题的方式。

1. 首先读取 `wiki/index.md`。
2. 运行 `python3 scripts/wiki_fts.py stats`。
3. 如果显示 `Fresh: no`，运行 `python3 scripts/wiki_fts.py rebuild`；如果重建失败且允许回退，则使用 `wiki/index.md` 和 `rg`。
4. 运行 `python3 scripts/wiki_fts.py search "{query}" --limit 10`。
5. 仅将返回的文本块视为候选位置。
6. 打开返回的 `page_path` 所指向的 `wiki/` 下文件，并阅读相关的完整上下文。
7. 跟随这些页面中有用的 Wiki 链接。
8. 使用 Wiki 页面引用作答，不要引用 BM25 数据行。

**导出使用**是一种运维和审计机制。

- 将导出用于审计、迁移、调试、外部分析，或检查已建立索引的文本。
- 当 `search` 可用时，不要将导出作为常规查询路径。
- 在面向用户的答案中，不要引用 `exports/*`、`indexes/fts.sqlite`、`chunk_id` 或 BM25 `score`。
- 导出内容包含已建立索引的 Wiki 文本，应将其视为敏感数据。

## 搜索输出约定

`search` 输出按相关性排序的候选文本块：

```text
1. {title} [{page_path}]
   heading: {heading_path}
   chunk: {chunk_id} score: {score}
   {snippet}
```

| 字段           | 含义                                                                                  | LLM 的使用方式                                     |
| -------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `title`        | 来自 frontmatter 或首个标题的页面标题。                                               | 仅作为便于阅读的标签。                             |
| `page_path`    | 相对于所生成 Wiki／项目根目录的路径，包含 `wiki/` 前缀，例如 `wiki/concepts/rag.md`。 | 回答前打开并阅读此文件。                           |
| `heading_path` | 页面内的标题路径，例如 `Overview > Limitations`。                                     | 打开页面后，用于定位相关小节。                     |
| `chunk_id`     | 稳定的文本块标识符：`{page_path}#{ordinal}`。                                         | 仅作为诊断句柄；不要将其作为证据引用。             |
| `score`        | 此次查询的 SQLite FTS5 BM25 分数。分数越低，相关性越高；值可能为负数。                | 仅用于对此次查询的候选项排序。不要跨无关查询比较。 |
| `snippet`      | 从已建立索引的文本块中截取的预览文本。                                                | 仅供预览。切勿只根据片段作答。                     |

当前搜索会将查询拆分为词项，并使用 OR 进行组合。为提高精度，请使用准确的页面标题、实体名称或 `wiki/index.md` 中的特征性短语，执行多次聚焦搜索。

## 数据模型

SQLite 数据库位于 `indexes/fts.sqlite`。它由 `scripts/wiki_fts.py` 根据 `wiki/` 生成，可以重建。当前 schema 版本为 `1`。

### 表：`pages`

`wiki/` 下的每个 Markdown 页面对应一行。

| 字段        | 类型               | 定义                                                                                  |
| ----------- | ------------------ | ------------------------------------------------------------------------------------- |
| `page_path` | `TEXT PRIMARY KEY` | 相对于所生成 Wiki／项目根目录的路径，包含 `wiki/` 前缀，例如 `wiki/concepts/rag.md`。 |
| `title`     | `TEXT NOT NULL`    | 页面标题，依次取自 frontmatter `title`、首个 `#` 标题或作为后备的文件名。             |
| `type`      | `TEXT NOT NULL`    | 来自 frontmatter `type` 的页面类型，例如 `concept`、`entity` 或 `source-summary`。    |
| `updated`   | `TEXT NOT NULL`    | frontmatter 的 `updated` 值；不存在时为空字符串。                                     |
| `sources`   | `TEXT NOT NULL`    | frontmatter 的原始 `sources` 值，以文本形式保留。                                     |
| `tags`      | `TEXT NOT NULL`    | frontmatter 的原始 `tags` 值，以文本形式保留。                                        |
| `mtime`     | `REAL NOT NULL`    | 用于新鲜度检查的文件系统修改时间。                                                    |

### 表：`chunks`

每个已建立索引的文本块对应一行。文本块根据每个页面的标题小节和字符窗口进行拆分。

| 字段           | 类型               | 定义                                             |
| -------------- | ------------------ | ------------------------------------------------ |
| `chunk_id`     | `TEXT PRIMARY KEY` | 稳定标识符 `{page_path}#{ordinal}`。             |
| `page_path`    | `TEXT NOT NULL`    | 父页面路径；与 `pages.page_path` 匹配。          |
| `title`        | `TEXT NOT NULL`    | 复制到每个文本块中的父页面标题。                 |
| `type`         | `TEXT NOT NULL`    | 复制到每个文本块中的父页面类型。                 |
| `heading_path` | `TEXT NOT NULL`    | 文本块所在小节的标题路径。                       |
| `ordinal`      | `INTEGER NOT NULL` | 文本块在父页面中的序号，从 1 开始。              |
| `sources`      | `TEXT NOT NULL`    | 复制到每个文本块中的父页面 `sources`。           |
| `tags`         | `TEXT NOT NULL`    | 复制到每个文本块中的父页面 `tags`。              |
| `updated`      | `TEXT NOT NULL`    | 复制到每个文本块中的父页面 `updated`。           |
| `text`         | `TEXT NOT NULL`    | 移除 Markdown 标记后用于搜索和导出的文本块正文。 |

### 虚拟表：`chunks_fts`

用于对文本块进行排序的 SQLite FTS5 表。

| 字段           | 是否索引          | 定义                                    |
| -------------- | ----------------- | --------------------------------------- |
| `chunk_id`     | 否（`UNINDEXED`） | 从 `chunks.chunk_id` 复制的诊断连接键。 |
| `title`        | 是                | 可搜索的页面标题文本。                  |
| `page_path`    | 否（`UNINDEXED`） | 用于导航的返回页面路径。                |
| `heading_path` | 是                | 可搜索的标题路径文本。                  |
| `text`         | 是                | 可搜索的主要文本块正文。                |

搜索通过 `chunk_id` 将 `chunks_fts` 连接回 `chunks`，以便 LLM 查看元数据和预览文本。BM25 `score` 在查询时根据 `chunks_fts` 计算；它不会存储在 `chunks` 中，也不会导出。

### 表：`metadata`

当前构建的键值元数据。

| 键               | 含义                           |
| ---------------- | ------------------------------ |
| `built_at`       | 索引构建时的 UTC 时间戳。      |
| `schema_version` | 数据模型版本；当前为 `1`。     |
| `root`           | 构建时使用的 Wiki 绝对根路径。 |
| `page_count`     | 已建立索引的 Wiki 页面数量。   |
| `chunk_count`    | 已建立索引的文本块数量。       |

### 导出字段

JSONL、CSV 和 Markdown 导出按照以下顺序包含 `chunks` 中的数据行：

```text
chunk_id, page_path, title, type, heading_path, ordinal, sources, tags, updated, text
```

导出不包含 `score`、`mtime` 或 FTS 内部信息。分数仅适用于单次查询，并且只由 `search` 计算。

## 命令

从 Wiki 根目录运行命令：

```bash
python3 scripts/wiki_fts.py doctor
python3 scripts/wiki_fts.py build
python3 scripts/wiki_fts.py rebuild
python3 scripts/wiki_fts.py search "query text" --limit 10
python3 scripts/wiki_fts.py stats
```

导出完整的已索引语料库：

```bash
python3 scripts/wiki_fts.py export --format jsonl --out exports/bm25-chunks.jsonl
python3 scripts/wiki_fts.py export --format csv --out exports/bm25-chunks.csv
python3 scripts/wiki_fts.py export --format markdown --out exports/bm25-report.md
```

导出内容包含文本块数据行、页面元数据字段和文本块正文。BM25 分数在查询时计算，因此不会导出。

## Git 策略

提交：

- `scripts/wiki_fts.py`
- `indexes/README.md`
- 如果偏好设置仅适用于当前项目，则提交 `.llm-wiki-v1/EXTEND.md`

通常不提交：

- `indexes/fts.sqlite`
- `exports/*.jsonl`
- `exports/*.csv`
- `exports/*.md`

数据库和导出内容均可根据 `wiki/` 重建。

## 隐私

`fts.sqlite` 和导出文件包含来自 Wiki 的可搜索文本。如果 Wiki 包含私密笔记、客户资料、个人日志或敏感研究内容，请勿随意分享这些文件。

## 故障排除

如果 `doctor` 失败，则本地 SQLite 构建不包含 FTS5。请使用启用了 SQLite FTS5 的 Python 发行版，或继续使用 `index.md + rg`。

如果 `stats` 显示 `Fresh: no`，请重建：

```bash
python3 scripts/wiki_fts.py rebuild
```

如果搜索未返回结果，请尝试 Wiki 中的准确术语、产品名称或论文标题，也可以使用 `rg` 作为后备方案。
