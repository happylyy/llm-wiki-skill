---
title: Concept Table
type: concept-table
created: 2026-09-03
updated: 2026-09-05
sources: [研发项目管理办法 4.1.md]
tags: [concept-map, navigation, maintenance]
---

> 此表是 Wiki 的压缩概念地图。它与 `wiki/index.md` 互为补充：索引用于编目页面；此表用于说明持久概念的含义、类型以及相互关系。

## 维护规则

- 为 `wiki/concepts/` 下的每个持久概念页面保留一行。
- 每当创建、重命名、删除、合并、拆分或实质性修订概念页面时，更新此表。
- 按概念名称的字母顺序排列各行。
- 定义应简洁并体现证据情况；链接到完整的概念页面以提供详细信息。
- “概念类型”仅使用以下候选类型：
  - `原理`：解释为什么某件事成立。
  - `机制`：解释某件事如何发生。
  - `方法`：说明如何完成某项任务。
  - `模型／框架`：组织多个概念或步骤。
  - `分类`：划分不同类型或层次。
  - `区分`：澄清容易混淆的对象。
  - `状态／属性`：描述对象的重要特征。
  - `评价标准`：判断某事是否成立或完成的依据。
  - `产出`：某种方法预期生成的稳定结果。
- “状态”使用 `high confidence`、`single-source`、`tentative`、`needs sources` 或 `contradicted` 等值。
- 行内容使用相关概念页面的语言。

## 概念集群

| Cluster(概念簇) | Concepts(概念) | Current interpretation(当前解释) |
| --------------- | -------------- | --------------------------------- |
| 产品演进与差异化管理 | [[product-lifecycle-model(产品生命周期模型)]]、[[rd-project-iteration-rounds(研发项目迭代轮次)]]、[[maturity-based-rd-project-management(基于产品成熟度的研发项目管理模式)]] | 产品阶段、研发轮次与产品成熟度共同决定投资、过程和质量策略。 |
| 研发治理与资源配置 | [[rd-management-three-domain-model(研发管理三域模型)]]、[[milestone-based-rd-incentives(里程碑式研发激励)]] | 投资、项目和资产三域协同，资金通过质量与进度门禁分阶段拨付。 |
| 质量与资产产出 | [[feature-validation(特性验证)]]、[[rd-deliverable-tailoring(研发成果物裁剪)]]、[[software-asset-lifecycle-management(软件资产全生命周期管理)]] | 成果物按情境裁剪，但须支持特性验证、资产归档和复用。 |

## 概念

| Concept(概念) | Concept type(概念类型) | Working definition(工作定义) | Role in this wiki(作用) | Sources(来源) | Related pages(相关页面) | Status(状态) |
| ------------- | ---------------------- | ---------------------------- | ----------------------- | ------------- | ----------------------- | ------------ |
| [[feature-validation(特性验证)]] | 方法 | 以产品特性为核心，从价值交付视角评估特性、架构与代码质量的质量保障活动。 | 连接产品价值、质量门禁、认可测评和研发激励。 | 研发项目管理办法 4.1.md | [[rd-project-iteration-rounds(研发项目迭代轮次)]]、[[milestone-based-rd-incentives(里程碑式研发激励)]] | single-source |
| [[maturity-based-rd-project-management(基于产品成熟度的研发项目管理模式)]] | 模型／框架 | 按产品技术、市场和组织成熟度采用不同资金、过程与容错策略。 | 解释探索／敏态和成熟／稳态项目的差异化管理。 | 研发项目管理办法 4.1.md | [[rd-project-iteration-rounds(研发项目迭代轮次)]]、[[rd-deliverable-tailoring(研发成果物裁剪)]] | single-source |
| [[milestone-based-rd-incentives(里程碑式研发激励)]] | 机制 | 根据立项、架构、特性验证和结项结果分阶段核算与拨付研发奖金。 | 将投资节奏与项目进度、质量结果相绑定。 | 研发项目管理办法 4.1.md | [[feature-validation(特性验证)]]、[[maturity-based-rd-project-management(基于产品成熟度的研发项目管理模式)]] | single-source |
| [[product-lifecycle-model(产品生命周期模型)]] | 模型／框架 | 描述产品从概念、验证、完善、规模化到终止并循环演进的阶段模型。 | 为投资、项目和资产管理提供共同参照。 | 研发项目管理办法 4.1.md | [[rd-project-iteration-rounds(研发项目迭代轮次)]]、[[rd-management-three-domain-model(研发管理三域模型)]] | single-source |
| [[rd-deliverable-tailoring(研发成果物裁剪)]] | 方法 | 按管理模式、研发轮次和项目情境确定成果物必须项、可选项及承载方式。 | 将统一治理要求适配为具体交付清单。 | 研发项目管理办法 4.1.md | [[maturity-based-rd-project-management(基于产品成熟度的研发项目管理模式)]]、[[feature-validation(特性验证)]] | single-source |
| [[rd-management-three-domain-model(研发管理三域模型)]] | 模型／框架 | 以资金、项目与任务、正式成果与产物为对象的投资、项目、资产三域治理框架。 | 组织研发价值、技术债和风险的分工协同。 | 研发项目管理办法 4.1.md | [[product-lifecycle-model(产品生命周期模型)]]、[[software-asset-lifecycle-management(软件资产全生命周期管理)]] | single-source |
| [[rd-project-iteration-rounds(研发项目迭代轮次)]] | 分类 | 将研发目标划分为 MVP、MMF 和 Scaling 三类轮次。 | 决定目标、投资、门禁和成果物要求。 | 研发项目管理办法 4.1.md | [[product-lifecycle-model(产品生命周期模型)]]、[[feature-validation(特性验证)]] | single-source |
| [[software-asset-lifecycle-management(软件资产全生命周期管理)]] | 方法 | 从立项开始对软件资产进行入库、状态更新、确权、归档、授权和复用治理。 | 将项目成果转化为可跨项目复用的公司资产。 | 研发项目管理办法 4.1.md | [[rd-management-three-domain-model(研发管理三域模型)]]、[[rd-deliverable-tailoring(研发成果物裁剪)]] | single-source |
