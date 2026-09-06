# 查询(query)工作流 — 参考

依据 wiki 内容进行做大的详细协议，并可选择将回答归档为新页面。

## 触发条件

用户询问 wiki 领域内的问题。无需特殊命令——任何问题都会触发此工作流。

## 核心流程

### step 0：偏好与搜索入口

使用 `references/config/extend-schema.md` 加载 `EXTEND.md` 偏好。如果偏好文件不存在，应首先完成首次偏好设置。

如果设置了 `bm25.mode: auto_prompt`，检查配置的阈值。如果达到阈值且尚未初始化 BM25，询问是否初始化。用户同意后，遵循 `references/workflows/bm25.md`进行操作。

### step 1：通过索引导航

阅读 `wiki/index.md`。对于概念性(conceptual)、关系性(relationship)、分类(taxonomy)或全局性(landscape)问题，在选择页面前还要阅读 `wiki/concept-table.md`。识别出可能与查内容询相关的页面。如果配置了 BM25，在阅读索引后将其作为额外的候选查找工具，而不是索引的替代品。

如果已启用 BM25，在读取索引后使用它：

```bash
python3 scripts/wiki_fts.py stats
python3 scripts/wiki_fts.py search "{user question or extracted query terms}" --limit 10
```

如果 `stats` 报告 `Fresh: no`，搜索前运行 `python3 scripts/wiki_fts.py rebuild`。如果重建失败且 `fallback_to_rg: true`，继续执行 `rg` 和 `wiki/index.md`。

BM25 只返回候选文本块。不要仅根据摘要片段回答；打开返回的页面并阅读该页面的完整内容。

### step 2：阅读相关页面

阅读已识别出的页面。如果某个页面引用了其他可能相关的页面，也继续阅读该相关页面。当获得足够上下文或已经阅读15个以上页面时(使用已有信息来完成工作)，就可以停止阅读了。

如果 BM25 不可用、已过期或没有返回有用结果，并且 `fallback_to_rg: true`，则回退到 `rg` 和 `wiki/index.md`。

### step 3：构建回答

回答文本的内容构成：

- 直接回答用户的问题
- 使用 wiki 页面内联引用：`[Page Title](wiki/path/to/page.md)`（页面标题可按实际内容替换）
- 标明置信度：高（多个来源相互印证）、中（单一来源）、低（推断）
- 如果 wiki 中没有足够信息完整作答，明确指出

### step 4：归档决策

在回答之后，评估一下：这个答案是否是值得保存的、有价值的成果？

**值得归档的情况**：

- 用户可能会再次进行的比较或分析
- 在已有的概念之间发现了新的联系
- 来自 3 个以上来源的整合
- 回答填补了 wiki 内容的缺口

**不值得归档的情况**：

- 简单的事实查询
- 关于 wiki 结构的问题
- 琐碎或一次性的查询

如果值得归档，提示用户：“这份分析内容似乎值得保留。是否归档为 `wiki/{type}/{english-slug}({中文标题}).md`？”

如果用户同意：

1. 使用正确的 frontmatter 创建页面
2. 添加与相关页面之间的双向引用
3. 如果归档的回答创建、重命名、合并、拆分或实质性修订了持久性的概念，应更新 `wiki/concept-table.md`文件
4. 更新 `wiki/index.md`文件
5. 追加到 `wiki/log.md` 中：

   ```text
   ## [{date}] query-filed | {title}
   - 提问：{original question}
   - 归档位置：wiki/{type}/{english-slug}({中文标题}).md
   - 相关页面：{list}
   ```

## 回答格式

根据问题类型调整输出格式：

| 提问类型                  | 回答格式                       |
| ------------------------- | ------------------------------ |
| “X 是什么？”              | 1–3 段文字说明                 |
| “比较 X 和 Y”             | 以比较维度为行的 Markdown 表格 |
| “关于 X，我们知道什么？”  | 带来源引用的结构化摘要         |
| “关于 X 有哪些开放问题？” | 带置信度评估的编号列表         |
| “总结 X 的现状”           | 按小节组织、包含关键主张的概览 |
| “X 的时间线”              | 按时间顺序排列的列表或表格     |

## Wiki 无法回答时

如果 wiki 缺少信息：

1. 明确说明缺少什么
2. 建议可能填补缺口的来源（网络搜索、具体文档）
3. 可选择创建一个记录知识缺口的占位页面：

   ```yaml
   ---
   title: "{topic}"
   type: concept
   created: { date }
   updated: { date }
   sources: []
   tags: [stub, needs-sources]
   ---
   ```
