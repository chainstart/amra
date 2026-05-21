# 决策：AMRA 引入数学研究能力扩展任务包

日期：2026-05-21

状态：接受

## 背景

AMRA 的 canonical theorem-search、proof loop、Lean formalization、source audit、review gate、portfolio campaign 和 result bundle 已经收敛到 `src/amra`。现有架构适合证明和形式化任务，但数学研究还包括猜想发现、计算实验、算法优化、应用建模、密码学安全分析、机器学习理论探索和负结果沉淀。

## 决策

新增 `docs/amra_research_capabilities_spec.zh.md` 作为 AMRA 数学研究能力扩展的主 spec。

该 spec 不并入 canonical migration spec，也不直接改写 portfolio spec。后续实现通过独立 requirement 和 task package 接入动态 spec 体系：

- `AMRA-RESEARCH-ONTOLOGY-001`
- `AMRA-EXPERIMENT-HARNESS-001`
- `AMRA-CONJECTURE-DISCOVERY-001`
- `AMRA-ALGORITHM-OPTIMIZATION-001`
- `AMRA-MODELING-PACK-001`
- `AMRA-CRYPTO-SECURITY-PACK-001`
- `AMRA-ML-THEORY-PACK-001`
- `AMRA-RESEARCH-REVIEW-GATES-001`
- `AMRA-RESEARCH-PORTFOLIO-001`

这些任务按依赖顺序执行。底层 ontology、artifact graph 和 workstream 扩展必须先完成；portfolio 和 result bundle 集成最后完成。

## 影响

- AMRA 的研究对象不再只包含 problem、claim、proof 和 Lean declaration。
- 猜想、实验、算法、模型、benchmark、反例、安全游戏、ML theory claim 和负结果都必须能作为 durable artifact 进入 artifact graph。
- 非证明证据必须和 theorem-grade proof/Lean verified 结果严格区分。
- 经验实验、benchmark、attack failure 和 bounded search 不得被误标为数学证明。
- engineering harness 后续应从 `.engineering/spec_tasks.yaml` 中按依赖顺序执行新增任务包。

