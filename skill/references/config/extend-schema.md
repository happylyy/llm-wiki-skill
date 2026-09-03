# EXTEND.md 架构

`EXTEND.md` 用于存储 llm-wiki-bootstrap 的用户偏好。仅在首次设置已创建或选择偏好文件后，
它才是可选的；当不存在该文件时，不得静默回退到默认值。

## 查找顺序

读取第一个存在的文件：

| 优先级 | 路径                                                             | 作用域     |
| ------ | ---------------------------------------------------------------- | ---------- |
| 1      | `.llm-wiki-bootstrap/EXTEND.md`                                  | 项目       |
| 2      | `${XDG_CONFIG_HOME:-$HOME/.config}/llm-wiki-bootstrap/EXTEND.md` | XDG        |
| 3      | `$HOME/.llm-wiki-bootstrap/EXTEND.md`                            | 用户主目录 |

在会话中首次使用时，简要说明当前启用的是哪个文件：

```text
正在使用 {path} 中的偏好。你可以编辑 EXTEND.md，以自定义 BM25 阈值、摄取行为、搜索策略等。
```

如果不存在该文件，请在执行引导创建、摄取、查询、检查或 BM25 工作之前，先完成首次偏好设置。

## 首次偏好设置

询问用户要在何处创建该文件：

- 项目：`.llm-wiki-bootstrap/EXTEND.md`（推荐）
- XDG: `${XDG_CONFIG_HOME:-$HOME/.config}/llm-wiki-bootstrap/EXTEND.md`
- 用户主目录：`$HOME/.llm-wiki-bootstrap/EXTEND.md`

然后询问：

1. BM25 提醒模式：`auto_prompt`（推荐）、`manual` 或 `off`
2. 阈值：使用推荐值或自定义值
3. 摄取后的重建策略：`true`（推荐）或 `false`
4. 是否需要 PDF OCR（PaddleOCR）以支持 PDF 转 Markdown；若需要，询问并记录 `pdf_ocr.token` 与模型参数

根据回答，以 `references/templates/extend.md` 为基础创建该文件。

## 字段

```yaml
bm25:
  mode: auto_prompt
  prompt_once: true

  thresholds:
    source_count: 30
    wiki_page_count: 150
    wiki_text_chars: 250000
    index_lines: 500
    query_read_pages: 15

  strong_thresholds:
    source_count: 50
    wiki_page_count: 300
    wiki_text_chars: 500000

  index_paths:
    - wiki

  include_raw: false
  auto_rebuild_after_ingest: true
  fallback_to_rg: true

  chunking:
    max_chars: 1800
    overlap_chars: 200

  export:
    default_format: jsonl
    include_text: true
```

## BM25 模式语义

| `mode`        | 行为                                                  |
| ------------- | ----------------------------------------------------- |
| `auto_prompt` | 达到阈值时，询问是否初始化 BM25。                     |
| `manual`      | 不自动提示；仅在用户明确请求时初始化。                |
| `off`         | 禁用 BM25 检查和提醒。                                |
| `enabled`     | BM25 可用时使用；缺失时先询问再初始化。               |
| `required`    | 配置后，摄取、查询和检查必须使用 BM25；不可用时停止。 |

## 阈值语义

当 `mode: auto_prompt` 时，任一常规阈值达到后询问一次。
任一强阈值达到后，即使用户此前拒绝过常规提醒，也应再次询问。

推荐的常规阈值：

- `source_count >= 30`
- `wiki_page_count >= 150`
- `wiki_text_chars >= 250000`
- `index_lines >= 500`
- `query_read_pages >= 15`

推荐的强阈值：

- `source_count >= 50`
- `wiki_page_count >= 300`
- `wiki_text_chars >= 500000`

## pdf_ocr 字段

可选。用于把 `raw/` 中的 PDF 转为 Markdown，供 ingest 工作流读取。

| 字段                           | 含义                         | 默认                                                 |
| ------------------------------ | ---------------------------- | ---------------------------------------------------- |
| `token`                        | PaddleOCR 访问令牌（必填）。 | 空                                                   |
| `model`                        | OCR 模型名。                 | `PaddleOCR-VL-1.6`                                   |
| `endpoint`                     | 任务提交地址。               | `https://paddleocr.aistudio-app.com/api/v2/ocr/jobs` |
| `use_doc_orientation_classify` | 文档方向分类。               | `false`                                              |
| `use_doc_unwarping`            | 文档展平。                   | `false`                                              |
| `use_chart_recognition`        | 图表识别。                   | `false`                                              |
| `poll_interval`                | 轮询间隔（秒）。             | `5`                                                  |

`token` 属于敏感信息，不得写入生成的 wiki、`wiki/log.md` 或任何输出页面。
若未配置 `pdf_ocr.token`，PDF 摄取回退为询问用户是否有可用工具。

## 决策记录

如果用户拒绝初始化，请将该决定记录到当前启用的 `EXTEND.md` 中：

```yaml
bm25:
  last_prompt:
    date: YYYY-MM-DD
    decision: declined
    source_count: 34
    wiki_page_count: 168
    wiki_text_chars: 281000
```

不要在此处记录索引新鲜度等运行状态。请将运行事件存入 `wiki/log.md`，并根据文件修改时间或
`python3 scripts/wiki_fts.py stats` 推导新鲜度。
