# 检查(lint)工作流 — 参考

Wiki 健康检查的详细协议，用于发现结构问题、矛盾和知识缺口。

## 触发条件

用户说“lint”“健康检查”“review wiki”“检查一致性”“wiki维护”，或对应的中文表达。

## 核心流程

### Step 0: Preferences and Search Gate

Load `EXTEND.md` preferences using `references/config/extend-schema.md`. If no preference file exists, run first-time preference setup before continuing.

If `bm25.mode: auto_prompt`, check configured thresholds. If reached and BM25 is not initialized, ask whether to initialize it. If the user agrees, follow `references/workflows/bm25.md`.

### Step 1: Full Scan

Read `wiki/index.md` and `wiki/concept-table.md`, then read every page listed. Build an internal model of:

- All pages and their types
- All `[[wikilinks]]` and their targets
- All `sources` frontmatter entries
- All contradiction blocks
- All tags
- All concept table rows, concept types, statuses, and related pages

If BM25 is enabled, also run:

```bash
python3 scripts/wiki_fts.py stats
```

Record whether the index is fresh.

### Step 2: Run Checks

Execute each check category. Collect findings as a numbered list.

#### 2.1 Structural Checks

| Check               | Issue                                                                                                                     | 严重程度 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------- |
| Orphan pages        | Page exists but no other page links to it                                                                                 | 中       |
| Broken wikilinks    | `[[target]]` has no matching file                                                                                         | 高       |
| Missing pages       | Concept/entity mentioned 3+ times across pages but has no dedicated page                                                  | 中       |
| Index drift         | Page exists in `wiki/` but not listed in `index.md`                                                                       | 高       |
| Concept table drift | Concept page exists without a row, row points to a missing concept page, or row definition/status conflicts with the page | 中       |
| Empty pages         | Page has frontmatter but no meaningful body content                                                                       | 低       |

#### 2.2 Content Checks

| Check                      | Issue                                                                                         | 严重程度 |
| -------------------------- | --------------------------------------------------------------------------------------------- | -------- |
| Unresolved contradictions  | Contradiction block with `Resolution: pending` older than 2 ingests                           | 中       |
| Stale claims               | Page claims X, but a newer source (by date) contradicts it without the page being updated     | 高       |
| Single-source concepts     | Concept page backed by only 1 source                                                          | 低       |
| Stale concept table metadata | Concept row type or status conflicts with the concept page and sources                       | 中       |
| Outdated overview          | `wiki/overview.md` not updated since 3+ ingests ago                                           | 中       |

#### 2.3 Cross-reference Checks

| Check             | Issue                                                                          | 严重程度 |
| ----------------- | ------------------------------------------------------------------------------ | -------- |
| Missing backlinks | Page A links to Page B, but B doesn't link back to A (when topically relevant) | 低       |
| Isolated clusters | Groups of pages that link to each other but not to the rest of the wiki        | 中       |
| Tag inconsistency | Same concept tagged differently across pages                                   | 低       |

#### 2.4 Search Layer Checks

| Check                  | Issue                                                                                          | 严重程度 |
| ---------------------- | ---------------------------------------------------------------------------------------------- | -------- |
| Stale BM25 index       | `python3 scripts/wiki_fts.py stats` reports `Fresh: no`                                        | 中       |
| Missing BM25 files     | Preferences require or enable BM25 but `scripts/wiki_fts.py` or `indexes/README.md` is missing | 高       |
| Repeated unlinked term | BM25/`rg` finds a concept title in 3+ pages without wikilinks                                  | 低       |
| Duplicate candidates   | Similar page titles or repeated exact terms suggest duplicate pages                            | 中       |

### step 3：报告

按严重程度分组输出发现：

```markdown
## Wiki 检查报告 — {date}

### 高（{count}）

1. {包含具体文件引用的发现}
   ...

### 中（{count}）

1. ...

### 低（{count}）

1. ...

### 建议

- {主动建议：值得探索的主题、需要寻找的来源、需要创建的页面}
```

### step 4：分诊

询问用户：“现在应修复哪些项目？”接受：

- “All”——修复所有问题
- “仅高严重程度”——只修复高严重程度问题
- 指定编号——“修复 1、3、7”
- “不修复”——仅记录报告

### step 5：执行修复

对每个获准的修复内容：

- 按需创建或更新页面
- 更新交叉引用
- 如果较新的数据结论明确，则解决矛盾
- 更新 `wiki/index.md`
- 如果已启用 BM25 且 wiki 页面发生变化，重建 BM25

### step 6：记录日志

向 `wiki/log.md` 追加：

```text
## [{date}] lint
- 问题总数：{count}
- 高：{count}，中：{count}，低：{count}
- 已修复：{list of fixed items}
- 已推迟：{list of deferred items}
```

## 建议的检查频率

| Wiki 规模      | 建议频率                               |
| -------------- | -------------------------------------- |
| 少于 10 个来源 | 每 3 次摄取后                          |
| 10–50 个来源   | 每周或每 5 次摄取后                    |
| 50 个以上来源  | 每 10 次摄取后，或查询返回不一致结果时 |
