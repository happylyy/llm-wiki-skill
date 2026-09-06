# 引导创建（bootstrap）工作流

只有在用户想要创建新的 LLM Wiki 框架时，才需要使用这个工作流。先按照 `references/config/extend-schema.md` 查找偏好并完成首次设置偏好，然后再进入第一阶段。

## 目标

创建一个即用的 LLM Wiki 页面体系，包含不更改的来源层、相对稳定的 raw-ingest 快照层、由 LLM 维护的 wiki 层、`SCHEMA.md`操作契约，以及用户可选择的运行时指针和用户设置的编辑/搜索配置。

## 阶段 1：收集需求

未经确认不能跳过：在创建文件之前必须完成此阶段。

在一次user prompt中收集下面所有问题：

| 标题      | 问题                          |                                                                                              提示|
| --------- | ----------------------------- | ------------------------------------------------------------------------------------------------ |
| 领域/范围 | Wiki 的主题是什么？           | 单选：研究主题；小说／媒体；个人（目标、健康、学习等）；企业／团队；其他。                       |
| Wiki 名称 | wiki根目录使用什么名称？      | 文本：建议使用```{domain}-wiki``` 格式，如```lm-wiki```这样的短标签。                                |
| 运行时    | 哪些运行时程序会读取此 wiki？ | 多选：Claude Code、OpenAI Codex、Copilot (VS Code)、及其他/通用类型。                            |
| 编辑器      | 主要使用哪个编辑器？          | 单选：Obsidian（推荐）、VS Code、其他/plain 文件。                                               |
| 来源类型  | 你会添加哪些类型的来源？      | 多选：网页文章、PDF 文档/论文、书籍、会议记录/发言稿、个人笔记/日记、图片/图表、数据文件、其他。 |
| 输出位置  | 你想将wiki创建在哪里？        | 单选：当前目录或自定义路径。                                                                       |

## 阶段 2：创建目录结构

请在 `{wiki-root}/` 下方创建这个基础树结构：

```text
{wiki-root}/
├── raw/
│   └── assets/                 # 仅在需要图片附件时创建
├── wiki/
│   ├── index.md
│   ├── concept-table.md
│   ├── log.md
│   └── overview.md
├── SCHEMA.md
├── {pointer-files}
└── .gitignore
```

有条件的输出：

| 条件                        | 添加内容                                              |
| --------------------------- | ----------------------------------------------------- |
| 选择任意来源类型            | `raw/.gitkeep`                                        |
| 来源类型包括图片/图表等     | `raw/assets/`                                         |
| 编辑器选择Obsidian          | 不要创建 .obsidian/，Obsidian 会自动创建它。          |
| 编辑器选择VS Code           | 创建 .vscode/settings.json，默认设置为Markdown 格式。 |
| 运行时包含Claude Code       | 创建`CLAUDE.md` 指针。                                |
| 运行时包含OpenAI Codex      | 创建`AGENTS.md` 指针。                                |
| 运行时包含Copilot (VS Code) | 创建`.github/copilot-instructions.md` 指针。          |

使用 `references/templates/gitignore.md` 创建 `.gitignore`。
在写入现有路径前，先检查。如果生成的文件会覆盖已有的用户内容，必须获得批准，或者存放在另外一个wiki根目录下。

## 阶段 3：生成 SCHEMA.md

使用 `references/templates/schema.md` 生成 `{wiki-root}/SCHEMA.md`。
变量模板：

| 变量                   | 来源                                      |
| ---------------------- | ----------------------------------------- |
| `{WIKI_NAME}`          | 回答的Wiki名称。                          |
| `{DOMAIN_DESCRIPTION}` | 回答的领域内容被扩展为 1-2 段清晰的句子。 |
| `{SOURCE_TYPES}`       | 回答的来源类型列表，用逗号分隔。          |
| `{EDITOR}`             | 回答的编辑器。                            |
| `{DATE}`               | 当前日期。                                |
| `{DOMAIN_PAGE_TYPES}`  | `domain-page-types.md` 中匹配领域的片段。 |

从references/templates/domain-page-types.md文件中匹配注入页面类型的片段：
| 领域 | 添加页面类型 |
| ---------------------- | ----------------------------------------- |
| 小说/媒体 | Character, timeline, plot thread, theme, location. |
| 专题研究 | Papers(论文), Claims(主张), Methods(方法), Datasets(数据集). |
| 个人 | Journal entry, goal, habit, lesson. |
| 企业/团队 | Decision log, meeting summary, project, stakeholder. |
| 其他 | 除非用户给出了更明确的分类标准，否则请使用通用的页面类型 |

如果编辑器是 Obsidian，那么在 `SCHEMA.md` 部分添加一个 `## Obsidian Setup` 节：

- 请将附件文件夹的路径设置为 `raw/assets/` 。
- 推荐使用的插件：Dataview，以及当使用幻灯片演示时使用的 Marp。
- 使用图表视图来查看维基页面的结构。
- 如果使用的是 Web Clipper，可以绑定一个下载附件的快捷键。

不要把编辑器设置写入指针文件中。

## 阶段 4：生成指针文件

对于除“其他/通用”之外的每个选定的运行环境，都从 `references/templates/agent-pointer.md` 创建一个瘦指针。

| 运行时             | 路径                                          | `{SCHEMA_PATH}` |
| ------------------ | --------------------------------------------- | --------------- |
| Claude Code        | `{wiki-root}/CLAUDE.md`                       | `./SCHEMA.md`   |
| OpenAI Codex       | `{wiki-root}/AGENTS.md`                       | `./SCHEMA.md`   |
| Copilot（VS Code） | `{wiki-root}/.github/copilot-instructions.md` | `../SCHEMA.md`  |

## 阶段 5：生成初始 Wiki 页面

请创建这些种子页面：

| 文件                     | 模板                                    | 自定义内容                                           |
| ------------------------ | --------------------------------------- | ---------------------------------------------------- |
| `wiki/index.md`          | `references/templates/index.md`         | 添加通用部分以及特定领域的部分。                     |
| `wiki/concept-table.md`  | `references/templates/concept-table.md` | 将 {DATE} 填充当前日期，"概念"行留空。               |
| `wiki/log.md`            | `references/templates/log.md`           | 请添加第一条关于当前日期的维基创建条目。             |
| `wiki/overview.md` | `references/templates/overview.md`      | 添加一段简短的简介，说明该维基页面的用途和所属领域。 |

通用索引部分包括：Core Maps, Sources, Entities, Concepts, Comparisons, Synthesis.
特定领域索引部分：
| 领域 | 章节 |
| ------------------------ | --------------------------------------- |
| 专题研究 | Papers(论文), Claims(主张), Methods(方法), Datasets(数据集). |
| 小说／媒体 | Characters(角色), Timelines(时间线), Themes(主题), Locations(地点). |
| 个人（目标、健康、学习等） | Journal(日记), Goals(目标), Habits(习惯), Lessons(教训). |
| 企业／团队 | Decision Logs(决策日志), Meetings(会议记录), Projects(项目), Stakeholders(干系人信息). |

对于空白的章节，可以使用占位符注释来填充，而不是编造内容。

## 阶段 6：编辑器配置

如果编辑器是 VS Code，那么创建 `{wiki-root}/.vscode/settings.json` ：

```json
{
  "files.exclude": { "**/.DS_Store": true },
  "editor.wordWrap": "on",
  "markdown.preview.breaks": true
}
```

如果编辑器是 Obsidian 或其他类型的文件，请不要创建超出 Obsidian 官方指南所规定范围的编辑器设置。这些设置已经包含在 `SCHEMA.md` 中了。

## 阶段 7：总结

所有文件都创建完成后，报告：

```
Wiki scaffolded at {wiki-root}/

Structure:
  raw/          -> Drop source documents here
  wiki/         -> LLM-maintained pages
  wiki/concept-table.md -> Maintained concept map
  SCHEMA.md     -> Single source of truth for agent behavior

Pointer files:
  {list generated pointer files, or "none"}

Next steps:
  1. Open {wiki-root}/ in {editor}
  2. Add the first source to raw/
  3. Tell the agent: "Read {wiki-root}/SCHEMA.md, 使用中文编译 raw/{filename}"
```

在初始化过程中，除非用户明确要求或偏好规定必须启用BM25，否则不要初始化 BM25。如果确实需要初始化 BM25，那么在完成基础框架的构建后，再执行 `references/workflows/bm25.md` 操作。
