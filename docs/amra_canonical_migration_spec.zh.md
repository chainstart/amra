# AMRA Canonical Migration Spec

日期：2026-05-20

状态：待 engineering-harness 执行

## 1. 目标

AMRA 的活实现必须收敛到 `src/amra`。`src/ara_math` 不再承载数学定理搜索、证明编排、攻关、Lean 形式化、评审、source recovery、portfolio memory 或 result bundle 的主实现，只保留 deprecated compatibility shim。

最终状态：

- `src/amra` 具备完整的数学定理搜索、题目评估、proof route 规划、proof attack、Lean 形式化、review gate、library promotion、portfolio campaign、result bundle 输出能力。
- `python3 -m amra` 是唯一 canonical CLI。
- `python3 -m ara_math`、`ara-math`、`ara_math` 继续可用，但只转发到 canonical AMRA 实现，并在文档和接口元数据中标记 deprecated。
- `src/amra` 不新增对 `ara_math` 的反向依赖；迁移期例外必须逐项删除。
- `src/ara_math/*.py` 文件可以保留，但只能是薄 shim、导入转发或兼容报错，不再包含独立业务逻辑。

## 2. 非目标

- 不在本轮要求删除 legacy package 名称，因为 ARA 和历史脚本仍可能调用 `ara_math`。
- 不启动 live LLM、长 Lean campaign、远程抓取或开放问题长跑。
- 不把 ARA 的论文流水线、drafting 或 manuscript 写作逻辑引入 AMRA。

## 3. Canonical 模块边界

| 能力 | Canonical 目标模块 | Legacy 来源 |
| --- | --- | --- |
| project/problem/claim/workspace state | `amra.core`, `amra.orchestration` | `ara_math.workstreams`, `ara_math.coordinator`, `ara_math.workspace` |
| proof route/search/attack | `amra.proof` | `ara_math.proof_lab`, `ara_math.proof_search`, `ara_math.math_attack`, `ara_math.closure`, `ara_math.campaign_loop`, `ara_math.goal_campaign` |
| Lean audit/executor/formalizer | `amra.lean` | `ara_math.lean`, `ara_math.lean_audit`, `ara_math.lean_contract`, `ara_math.lean_formalizer`, `ara_math.formalization` |
| agents/tool loop | `amra.agents` | `ara_math.pure_agents`, `ara_math.agent_tools`, `ara_math.proof_state` |
| source/literature/source audit | `amra.sources` | `ara_math.literature`, `ara_math.comath_source_audit` |
| evaluator/scheduler/review | `amra.evaluation`, `amra.scheduler`, `amra.review` | `ara_math.evaluator`, `ara_math.obligation_refiner`, `ara_math.review`, `ara_math.review_gate`, `ara_math.strategy`, `ara_math.uncertainty` |
| portfolio memory/campaign/report | `amra.portfolio_*` | `ara_math.scouting`, `ara_math.convergence`, `ara_math.comath_capabilities`, `ara_math.comath_runners` |
| result bundle / ARA handoff | `amra.result_bundle` | `ara_math.deliverables`, `ara_math.writing` |
| reusable Lean library | `amra.amra_library`, `amra_library/` | `ara_math.ara_library`, `ara_library/` |

## 4. Required Task Packages

### AMRA-CANONICAL-INVENTORY-001

建立机器可读迁移清单、import audit 和 shim 判定标准。该任务不迁移大量实现，只让后续任务有可检验边界。

验收重点：

- 覆盖全部 `src/ara_math/*.py`。
- 输出 active implementation、shim、delete-later、blocked categories。
- 增加测试，防止 `src/amra` 新增未声明的 `ara_math` import。

### AMRA-ORCHESTRATION-MIGRATION-001

迁移 CoMath 状态、workstream、coordinator、uncertainty 和 review gate 到 canonical AMRA orchestration/review/scheduler 层。

验收重点：

- `amra.orchestration` 能创建 project、workstream、claim、artifact graph、uncertainty ledger 和 dashboard state。
- legacy `ara_math` 模块转发到 canonical 实现。
- 旧 CoMath 测试继续通过。

### AMRA-PROOF-RUNNERS-MIGRATION-001

迁移 proof lab、proof search、closure prover、math attack、campaign/goal loop 和 retrieval/planning/proof-system 能力到 `amra.proof`。

验收重点：

- canonical AMRA proof runner 能以短预算运行 deterministic closed-theorem smoke。
- 每次 proof/attack 运行写 durable run directory。
- legacy imports 与 canonical classes/functions identity 或行为兼容。

### AMRA-SOURCES-EVALUATION-MIGRATION-001

迁移 literature/source audit、specialist/evaluator、obligation refiner、strategy/scouting/convergence/banking 到 `amra.sources`、`amra.evaluation`、`amra.scheduler` 和 portfolio 层。

验收重点：

- source recovery、difficulty evaluation、park/continue/promote/freeze 决策均从 canonical AMRA 模块导出。
- 测试使用本地 fixture，不进行 live crawling。

### AMRA-CANONICAL-CLI-ORCHESTRATOR-001

让 `python3 -m amra` 的主入口完全使用 canonical modules，提供从 problem bank 到 proof/search/formalization/result bundle 的 canonical smoke path。

验收重点：

- canonical CLI 不依赖 `ara_math.cli`。
- `python3 -m amra run-known-problem-smoke ...` 仍输出有效 `amra_result_bundle`。
- legacy CLI 只转发。

### AMRA-LEGACY-SHIM-CLEANUP-001

收尾迁移：`src/ara_math` 只保留 shim，删除或标记所有未声明反向依赖例外。

验收重点：

- import audit 证明 `src/amra` 没有未声明 `ara_math` 依赖。
- `src/ara_math` 文件不再包含主动业务实现。
- AMRA theorem-search/orchestration/proof/Lean/library/bundle smoke tests 通过。

## 5. 完成定义

完成本 spec 不等于 AMRA 能解决所有难题。完成含义是：

- 系统架构完整：搜索、评估、编排、攻关、形式化、复审、库化、bundle 输出全部由 `src/amra` 承载。
- 难题可以被正确评估、park/freeze/resume，而不是无限拉扯。
- 容易题和 closed-theorem benchmark 可以走完整 deterministic smoke。
- ARA 只通过 `research_lab.yaml` 和 `amra_result_bundle` 消费 AMRA。
