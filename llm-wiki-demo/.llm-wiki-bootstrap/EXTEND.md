# llm-wiki-bootstrap 偏好设置

此文件用于自定义 llm-wiki-bootstrap skill 在当前项目中的行为。
按照已配置的优先顺序找到的第一个 EXTEND.md 生效。

```yaml
bm25:
  # Wiki 达到阈值时提醒；初始化阶段不创建 BM25 索引。
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

## 说明

- BM25 是面向较大型 Markdown Wiki 的可选本地检索辅助工具。
- BM25 不取代 `wiki/`、`index.md`、`SCHEMA.md` 或 LLM 的判断。
- `indexes/fts.sqlite` 和 `exports/*` 等搜索产物均可重建，通常不应纳入 Git。
