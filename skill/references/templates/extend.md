# llm-wiki-v1 偏好设置

此文件用于自定义 llm-wiki-v1 skill 在当前项目或用户账户中的行为。
按照已配置的优先顺序找到的第一个 EXTEND.md 生效。

```yaml
bm25:
  # auto_prompt：达到阈值时提醒
  # manual：不自动提醒；仅在用户明确请求时执行
  # off：禁用 BM25 检查和提醒
  # enabled：BM25 可用时使用；如果缺失且用户同意，则进行初始化
  # required：配置后，ingest／query／lint 必须使用 BM25
  mode: auto_prompt

  # 如果为 true，用户拒绝后不再重复相同的 auto_prompt，
  # 直到达到强提醒阈值。
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

pdf_ocr:
  # 可选能力：需要摄取 PDF 时设为 enabled: true 并填写 token。
  enabled: false
  token: ""
  model: "PaddleOCR-VL-1.6"
  endpoint: "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
  poll_interval: 5
  use_doc_orientation_classify: false
  use_doc_unwarping: false
  use_chart_recognition: false
```

## 说明

- BM25 是可选功能。它是用于较大型 Markdown Wiki 的本地检索辅助工具。
- BM25 不取代 `wiki/`、`index.md`、`SCHEMA.md` 或 LLM 的判断。
- `indexes/fts.sqlite` 和 `exports/*.jsonl` 等生成的搜索产物均可重建，
  通常不应纳入 Git。
