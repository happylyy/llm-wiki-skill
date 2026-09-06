# 日志

> 以追加方式记录所有 wiki 操作的时间顺序。
> 每个条目：`## [YYYY-MM-DD] operation | subject`
> 使用以下命令解析：`grep "^## \[" wiki/log.md | tail -10`

## [2026-09-05] init | Wiki 已创建

- 由 llm-wiki-v1 生成骨架
- 领域：面向专题研究的个人知识库，用于把论文、文章、会议记录与个人笔记中的知识，提炼为可追溯的论文摘要、主张、方法与数据集。
- 来源类型：网页文章、PDF 文档/论文、会议记录/发言稿、个人笔记/日记、图片/图表、数据文件
- 架构：SCHEMA.md（唯一事实来源）
- 指针文件：CLAUDE.md（workbuddy）、AGENTS.md（OpenAI Codex）、.github/copilot-instructions.md（Copilot）
- 注意：覆盖了之前的 wiki 骨架（备份保留在 `backup-2026-09-05/`，包含旧的 raw 与 wiki 完整副本）

## [2026-09-05] ingest | 研发项目管理办法 4.1

- Summary: wiki/sources/rd-project-management-measures-v4-1(研发项目管理办法4.1).md
- New pages: 1 来源摘要 + 38 概念 + 10 实体
- 概念（38）：研发（R&D）、产品创新类型、技术创新类型、公司支持R&D项目、部门级 R&D 项目、研发项目的产品成熟度、基于产品成熟度的研发项目管理模式、研发项目迭代轮次、特性验证、技术债、产品生命周期模型、投资管理域、项目管理域、资产管理域、软件资产全生命周期管理；产品换代升级、已有产品的衍生品、对已有产品的改进、全新产品/服务、技术机制封装、对已有技术的改进、新技术探索与导入、探索项目、成熟项目、敏态管理模式、稳态管理模式、最小可行产品（MVP）、最小可市场化特性（MMF）、规模化（Scaling）；价值主张、产品特性、项目集、两单一务、软件资产元模型、公共构块（CBB）、软件资产库、投资回报率（ROI）、折现现金流（DCF）
- 实体（10）：业务创新与技术委员会、产品创新与软件资产管理部、项目管理部、部门 PMO、财经管理部、测评部门（CNAS 软件评测实验室）、咨询管理中心、架构治理中心、资产运营中心、东软集团股份有限公司
- Contradictions: 原文 §4 与 §5.3 组织命名不一致（产品创新与软件资产管理部/公司 PMO·项目管理部/资产管理中心 vs 产品战略与研发管理中心/项目管理部/资产运营中心），按用户约定统一为项目管理部、资产运营中心，差异在实体页「原文表述」字段保留
- 保密说明：原文标「东软秘密，未经许可不得扩散」，仅用于个人知识库内部整理
- 提取铁律：所有概念/实体名称与定义逐字忠实原文，不自行创造概念

## [2026-09-06] lint | 来源—概念关联修正

- Issues found: 1
- Fixed: `rd-project-management-measures-v4-1(研发项目管理办法4.1).md` 的“相关概念”由 15 项补齐为 38 项，与概念页 `sources`、概念表和索引一致
- Deferred: none

## [2026-09-06] ingest | 关于数字化生产体系统一语言的通知

- Summary: wiki/sources/digital-production-system-unified-language-notice(关于数字化生产体系统一语言的通知).md
- New pages: 1 来源摘要 + 81 概念 + 10 比较 + 4 综合／映射
- Updated concepts: 价值主张（并列保留研发管理与 BIZBOK 语境，状态为 tentative）；公共构块（CBB）、软件资产全生命周期管理增加相关概念链接
- Updated entities: 东软集团股份有限公司、产品创新与软件资产管理部、项目管理部
- Persistent concepts from this source: 82；来源页与概念页双向关联按同一集合维护
- Terminology governance: 11 个治理概念完整保留在来源摘要，不建立独立页面
- OCR/structure notes: “物埋／仕”规范为“物理／在”并留痕；目录“模块 Building Block”以正文“构块”为准；页眉串行从定义中剥离
- Contradictions: none；“价值主张”为不同语境的侧重点差异，不标记为硬冲突
- Raw preservation: 未修改或恢复 raw/；附图仅从 Git 历史只读核对
- BM25: 摄取前未达到阈值，且 wiki 中不存在搜索脚本，未初始化或重建
