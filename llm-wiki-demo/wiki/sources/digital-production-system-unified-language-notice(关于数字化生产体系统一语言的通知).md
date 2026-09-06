---
title: "digital-production-system-unified-language-notice(关于数字化生产体系统一语言的通知)"
type: source-summary
created: 2026-09-06
updated: 2026-09-06
sources: [关于数字化生产体系统一语言的通知.md]
tags: [软件架构, 统一术语, 数字化生产体系, 四层环境三层映射]
---

# 关于数字化生产体系统一语言的通知

## 作品分类(Category)

公司内部术语规范汇编。原始 Markdown 实际拼接了两份 2026-04-30、V1.0 的正式定义文档：《软件架构 核心技术语定义》和《四层环境三层映射 核心术语定义》。原始证据见[原始 Markdown](../../raw/关于数字化生产体系统一语言的通知.md)。

## 主题摘要(Summary)

第一份文档旨在统一软件架构设计、分析、评审、交付和治理中的术语语义。它先规定适用范围、适用对象、使用原则和九项术语管理原则，再按基础通用、架构设计、业务架构、应用架构、数据架构、技术架构、设计与交付分类定义术语，随后说明 4A 架构、业务架构与运营模式、生产力度量框架和 C4 的关系，最后用十组对照划清容易混淆的概念边界。

第二份文档面向东软集团各部门、大区、分公司和全资子公司的生产体系，提出“四层环境三层映射”。四层依次是产品研发环境（PDT）、生产过程管理环境（PPM）、价值交付管理环境（VDM）和价值实现管理环境（VSM）；三层映射依次是 QCD 映射、业务价值衰减映射和生产结果映射，并以 TPP、VSM 要素作为评价输入，使软件生产、资产复用、价值交付和价值实现形成可度量、可预测的链路。

## 关键主张(Key Claims)

1. 软件架构术语必须统一命名、统一定义和统一使用口径；同一概念优先使用一个标准术语，易混术语必须说明适用语境和边界（§1–§2.1）。
2. 软件资产是生产视角下的物理软件资源，分为系统、应用和组件；是否构成复用应按 UI、API 等使用接口判断，直接修改源代码不属于本文定义的软件复用（§3.1）。
3. 业务架构以业务价值驱动应用架构和数据架构，二者构成业务的数字化映射；技术架构承接其软件、硬件实现与部署需求（§4.1及 p23 图）。
4. 价值流、业务流程、业务场景，以及领域、子域、限界上下文等术语分别回答不同问题，不应当作同义词混用（§5.1–§5.10）。
5. 四层环境三层映射通过逐层量化，把产品线资产能力、生产过程 QCD、客户价值衰减和最终生产结果连接为端到端预测与优化体系（第二份文档 §3–§5）。

## 作品结构(Structures)

### 《软件架构 核心技术语定义》

- 版本／日期：V1.0，2026-04-30
- 编制部门：东软集团股份有限公司 产品创新与软件资产管理部
- §1：目的、范围、对象与使用原则
- §2：九项术语管理原则及使用要求
- §3：七类正式术语定义
- §4：核心术语关系与映射
- §5：十组易混淆术语对照
- §6：参考依据

### 《四层环境三层映射 核心术语定义》

- 文件编号：C2-P07-D00-CQM043
- 版本／日期：V1.0，2026-04-30
- 编制部门：东软集团股份有限公司 项目管理部
- §1–§3：目标、范围与基础定义
- §4：四层环境、三层映射、TPP 要素与 VSM 要素
- §5：四层环境三层映射业务流程图

### 术语管理规则（不单独建概念页）

- 术语管理原则：统一性、准确性、简洁性、一词一义、分层分类、场景化、规范性、可追溯、演进性。
- 术语使用要求：首次出现宜给出中文全称及必要的英文名／缩写；图、文、表和评审材料保持一致；不混用含义接近但边界不同的术语；未定义的项目必需术语应补充定义并注明来源；歧义术语宜补充示例、反例或对比。

### 四层环境三层映射主链路

`PDT → 生产力度 → QCD 映射函数 → PPM → 业务价值衰减映射函数 → VDM → 生产结果映射函数 → VSM`

内部 TPP 要素进入 QCD 映射，外部 TPP 要素进入业务价值衰减映射，VSM 要素进入生产结果映射。原文还提到预测结果、生产活动、合同质量、人效、元效和按期按预算，但没有给出足以支持独立概念页的完整定义。

## 目录与实际结构的差异

- 目录写“模块 Building Block”，正文正式标题写“构块 Building Block”；本 Wiki 以正文“构块”为正式名称。
- 目录写“基础架构 Foundation Architectures”，正文写“基础级架构”；本 Wiki 以正文标题为准。
- 目录中的系统、应用、组件括注为“软件模块”，正文正式定义改用“软件构块”；概念页按正文表达。
- §3.2 架构拆分第 3 点被保密页眉串入，形成“要实东软秘密，未经许可不得扩散现”；派生页按上下文读取为“要实现”。
- §5.9 出现“物埋模型是仕逻辑模型基础上”的明显 OCR 错误；同节标题和表格明确为“物理模型”，派生页规范为“物理模型是在逻辑模型基础上”并保留此记录。
- QCD 映射段落写“产品研发管理环境”，正式术语是“产品研发环境（PDT）”；视为同一环境的原文名称变体。
- “客户价值述求”等无法仅凭本文断定为 OCR 的用词原样保留。

## 提及的实体(Entities Mentioned)

- [[neusoft-group(东软集团股份有限公司)|东软集团股份有限公司]]
- [[product-innovation-software-asset-management-department(产品创新与软件资产管理部)|产品创新与软件资产管理部]]
- [[project-management-department(项目管理部)|项目管理部]]

原文还提及《架构治理-架构设计方法参考》、TOGAF v10、BIZBOK v11、DAMA-DMBOK2、《Domain-Driven Design Reference》、Eric Evans、Chisholm（2001）、C4，以及 Java、Go、Rust。本文只记录其被原文引用的事实，不创建低信息实体页，也不使用外部资料补充身份。

## 相关概念(Concepts)

本节是该来源对应的完整持久概念清单，共 82 个。

### 基础通用术语

- [[software-asset(软件资产)|软件资产]]
- [[software-asset-reuse(软件资产的复用)|软件资产的复用]]
- [[software-product(软件产品)|软件产品]]
- [[software-solution(软件解决方案)|软件解决方案]]

### 架构设计术语

- [[architecture(架构)|架构]]
- [[architecture-partitioning(架构拆分)|架构拆分]]
- [[building-block(构块)|构块]]
- [[strategic-architecture(战略架构)|战略架构]]
- [[segment-architecture(分段架构)|分段架构]]
- [[capability-architecture(能力架构)|能力架构]]
- [[logical-architecture(逻辑架构)|逻辑架构]]
- [[physical-architecture(物理架构)|物理架构]]
- [[baseline-architecture(基线架构)|基线架构]]
- [[target-architecture(目标架构)|目标架构]]
- [[foundation-architectures(基础级架构)|基础级架构]]
- [[common-systems-architectures(通用级架构)|通用级架构]]
- [[industry-architectures(行业级架构)|行业级架构]]
- [[organization-specific-architectures(组织级架构)|组织级架构]]

### 业务架构术语

- [[business-architecture(业务架构)|业务架构]]
- [[value-stream(价值流)|价值流]]
- [[value-proposition(价值主张)|价值主张]]
- [[value-item(价值项)|价值项]]
- [[value-stream-stage(价值流阶段)|价值流阶段]]
- [[business-process(业务流程)|业务流程]]
- [[activity(活动)|活动]]
- [[business-capability(业务能力)|业务能力]]
- [[capability-instance(能力实例)|能力实例]]
- [[capability-behavior(能力行为)|能力行为]]
- [[business-object(业务对象)|业务对象]]
- [[information-concept(信息概念)|信息概念]]
- [[organization(组织)|组织]]
- [[business-unit(业务单元)|业务单元]]

### 应用架构术语

- [[application-architecture(应用架构)|应用架构]]
- [[system(系统)|系统]]
- [[application(应用)|应用]]
- [[component(组件)|组件]]

### 数据架构术语

- [[data-architecture(数据架构)|数据架构]]
- [[data-entity(数据实体)|数据实体]]
- [[data-product(数据产品)|数据产品]]
- [[data-platform(数据平台)|数据平台]]

### 技术架构术语

- [[technology-architecture(技术架构)|技术架构]]
- [[technology-service(技术服务)|技术服务]]
- [[technology-component(技术组件)|技术组件]]
- [[technology-platform(技术平台)|技术平台]]

### 设计与交付术语

- [[requirements(需求)|需求]]
- [[opportunities-and-solutions(机会及解决方案)|机会及解决方案]]

### 架构关系术语

- [[information-systems-architecture(信息系统架构)|信息系统架构]]
- [[operating-model(运营模式)|运营模式]]

### 易混淆术语补充

- [[business(业务)|业务]]
- [[project(项目)|项目]]
- [[system-function(功能)|功能]]
- [[business-scenario(业务场景)|业务场景]]
- [[domain(领域)|领域]]
- [[subdomain(子域)|子域]]
- [[bounded-context(限界上下文)|限界上下文]]
- [[module(模块)|模块]]
- [[data-model(数据模型)|数据模型]]
- [[conceptual-model(概念模型)|概念模型]]
- [[logical-model(逻辑模型)|逻辑模型]]
- [[physical-model(物理模型)|物理模型]]
- [[master-data(主数据)|主数据]]
- [[basic-data(基础数据)|基础数据]]
- [[reference-data(参考数据)|参考数据]]

### 四层环境三层映射术语

- [[four-layer-environment-three-layer-mapping(四层环境三层映射)|四层环境三层映射]]
- [[management-environment(环境)|环境]]
- [[quantitative-mapping-function(函数)|函数]]
- [[environment-factor(要素)|要素]]
- [[product-line(产品线)|产品线]]
- [[four-layer-environments(四层环境)|四层环境]]
- [[product-development-environment(产品研发环境（PDT）)|产品研发环境（PDT）]]
- [[production-process-management-environment(生产过程管理环境（PPM）)|生产过程管理环境（PPM）]]
- [[value-delivery-management-environment(价值交付管理环境（VDM）)|价值交付管理环境（VDM）]]
- [[value-realization-management-environment(价值实现管理环境（VSM）)|价值实现管理环境（VSM）]]
- [[three-layer-mappings(三层映射)|三层映射]]
- [[qcd-mapping-function(QCD 映射函数)|QCD 映射函数]]
- [[business-value-decay-mapping-function(业务价值衰减映射函数)|业务价值衰减映射函数]]
- [[production-result-mapping-function(生产结果映射函数)|生产结果映射函数]]
- [[tpp-factors(TPP 要素)|TPP 要素]]
- [[technical-completeness(技术完备性)|技术完备性]]
- [[process-effectiveness(过程有效性)|过程有效性]]
- [[resource-rationality(资源合理性)|资源合理性]]
- [[vsm-factors(VSM 要素)|VSM 要素]]

## 重要引文(Notable Quotes)

> 对于本文件已定义术语，不应随意改变其含义或以其他近义词替代。

- 位置：《软件架构 核心技术语定义》§1.4，行 163–167

> 架构 = 元素 + 关系 + 设计演进原则。

- 位置：《软件架构 核心技术语定义》§3.2，行 269–275

> 通过生产体系全链路量化，围绕产品研发、生产过程、价值交付、价值实现四层环境及生产要素分层穿透，构建端到端软件生产、资产复用与迭代优化的软件生产体系。

- 位置：《四层环境三层映射 核心术语定义》§3.1，行 805–807

## 局限／偏见(Limitations / Bias)

- 两份文档均为东软集团内部 V1.0 术语规范，反映单一组织的架构治理与生产管理口径；外部标准只作为原文参考依据，本 Wiki 未外部核验。
- 原文多处标注“东软秘密，未经许可不得扩散”；本次仅在本地个人 Wiki 内整理，不向外部服务发送内容。
- 当前工作区中的原图文件已被删除；本次仅依据原始 Markdown 和 Git 历史中可只读核对的附图提取关系，不恢复 `raw/assets`。
- 部分附图节点只有名称而没有独立定义，例如利益相关者、能力结果、OLAP/OLTP 应用、生产力度和映射预测结果；这些内容只保留在父页面或关系页。
