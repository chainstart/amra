# AMRA Legacy Module Disposition

日期：2026-05-18

状态：已校验的执行前置清单

范围：`src/ara_math/*.py`

校验结果：处置表覆盖当前 51 个 `src/ara_math/*.py` 文件；每个文件都有一条表格记录和至少一个第 2 节定义的处置标签。本任务不删除、移动或改写 legacy 模块。

## 1. 结论

`src/ara_math` 不能作为一个整体简单删除或一次性搬迁。它现在混合了：

- 运行基础设施；
- 问题库和项目 workspace；
- 旧 MVP pipeline；
- CoMath 状态、调度和 review gate；
- proof search / proof lab / Lean formalization；
- 新近加入的 pure agent 和 focused attack 能力；
- CLI 和 orchestrator 聚合层。

AMRA 重构要做的是模块处置，而不是目录级清空：

- 基础设施模块先保留并迁移到 `amra.core` / `amra.infra`。
- 数学证明、Lean、portfolio 相关模块迁移到 `amra.proof` / `amra.lean` / `amra.portfolio`。
- 旧的写作/论文导向模块逐步降级为 result bundle / writing brief 支撑，不再作为 AMRA 主流程。
- `cli.py`、`orchestrator.py`、`coordinator.py` 需要拆分，不能继续作为大聚合模块膨胀。
- `ara_math` 最终只保留 deprecated compatibility shim。

## 2. 处置标签

- `keep-core`：保留为底层能力，后续迁移到 AMRA canonical 包。
- `move`：迁移到 `src/amra` 对应子包，legacy 文件变 shim。
- `split`：拆分为多个更小模块。
- `merge`：并入 AMRA 新模块，避免重复抽象。
- `deprecate`：不再作为 AMRA 主流程，只保留兼容或导出用途。
- `shim`：最终只保留薄兼容层。
- `delete-later`：只有当新模块、测试、artifact 迁移完成后才删除。

## 3. 文件级处置表

| 文件 | 当前职责 | 问题/重合 | 处置 | 目标 |
|---|---|---|---|---|
| `__init__.py` | legacy package metadata | 旧命名入口 | `shim` | 保留 deprecated shim，导向 `amra` |
| `__main__.py` | legacy module CLI | 旧命名入口 | `shim` | 保留 `python3 -m ara_math` 兼容 |
| `accessibility.py` | premise/import 可达性规划 | proof search 子能力 | `move` | `amra.proof.accessibility` |
| `agent_tools.py` | pure agent 工具注册 | 和 portfolio runner 工具边界相关 | `move` | `amra.agents.tools` |
| `ara_library.py` | `ara_library` / `AraLibrary` 管理 | 名称已过时，但逻辑重要 | `move+shim` | 新实现 `amra.amra_library`，legacy 转发 |
| `artifact_graph.py` | artifact/dependency graph | AMRA/CoMath 都需要 | `keep-core` | `amra.core.artifacts` |
| `banking.py` | 本地 problem bank 同步 | portfolio scout 输入层 | `move` | `amra.problem_banks.sync` |
| `campaign_loop.py` | 单目标 proof/formalization loop | 与 portfolio outer loop 互补 | `move` | `amra.proof.campaign_loop` |
| `cli.py` | 所有命令聚合 | 过大、跨层 import 多 | `split+shim` | `amra.cli` 调度子命令，legacy 转发 |
| `closure.py` | strict Lean closure prover | active attack 子能力 | `move` | `amra.proof.closure` |
| `comath_benchmarks.py` | CoMath 本地 benchmark | AMRA eval harness 可复用 | `merge` | 合并到 `amra.evaluation.benchmarks` |
| `comath_capabilities.py` | CoMath 能力评估、证书、理论记忆 | 与 AMRA memory/eval 有重合 | `split+merge` | computation certificate 留 infra，theory memory 合并 portfolio memory |
| `comath_runners.py` | workstream executor adapters | 与 portfolio scheduler/runner 重合 | `split+merge` | executor adapters 迁入 `amra.scheduler.executors` |
| `comath_source_audit.py` | source audit loop | 与 AMRA needs_source/source_recover 对应 | `move` | `amra.source_audit` |
| `comath_specialists.py` | specialist prompt/provider/memory | 与 AMRA agent roles 对应 | `move+split` | `amra.agents.specialists` 和 `amra.agents.providers` |
| `context.py` | exact statement/context audit | AMRA 核心 project context | `keep-core` | `amra.core.context` |
| `convergence.py` | convergence planning | 旧 proof-search planning 层 | `merge` | 合并到 portfolio evaluator/scheduler |
| `coordinator.py` | CoMath project/workstream coordinator | 过大，和 AMRA scheduler/memory 重合 | `split+merge` | state functions -> memory；scheduler -> portfolio scheduler；dashboard -> reports |
| `deliverables.py` | deliverable type 判断 | 偏论文/报告导向 | `deprecate+merge` | 合并到 result bundle/writing brief，不做 AMRA 主状态 |
| `erdos_status.py` | Erdős status/source refresh | problem bank source adapter | `move` | `amra.problem_banks.erdos` |
| `evaluator.py` | evaluator planner/runner | 与 independent evaluator 相关 | `merge` | 合并到 `amra.portfolio_evaluator` |
| `focused_attack.py` | host-enforced Lean focused attack | AMRA active attack 核心 | `move` | `amra.proof.focused_attack` |
| `formalization.py` | Lean stub/formalization artifact prep | 与 Lean formalizer 前处理相关 | `merge` | 合并到 `amra.lean.formalization` |
| `goal_campaign.py` | root-goal driven campaign | 和 portfolio campaign 有重合 | `merge` | 作为 promoted target 子流程，不做外层主循环 |
| `lean.py` | Lean executor/cache/build/audit 集成 | 核心能力，入边多 | `keep-core+split` | `amra.lean.executor`、`amra.lean.cache`、`amra.lean.audit` |
| `lean_audit.py` | Lean source placeholder audit | 小而稳定 | `keep-core` | `amra.lean.audit` |
| `lean_contract.py` | Lean declaration header contract | focused attack/formalizer 共用 | `keep-core` | `amra.lean.contract` |
| `lean_formalizer.py` | proof-to-Lean loop | AMRA formalizer 核心 | `move` | `amra.lean.formalizer` |
| `literature.py` | literature/reference harvesting | source recovery 支撑，但文件过大 | `split` | `amra.sources.literature`、`amra.sources.references` |
| `math_attack.py` | math-only attack loop | 与 proof_lab/pure_agents 有重合 | `merge` | 合并为 AMRA ProofAgent runner 模式之一 |
| `math_scout.py` | active shallow math probes | portfolio scout 核心 | `move` | `amra.portfolio.scout` |
| `models.py` | ProblemRecord/ProofPlan/LeanBuildReport | 核心 schema | `keep-core` | `amra.core.models` |
| `obligation_refiner.py` | specialist output -> workstreams | 与 AMRA scheduler task materialization 相关 | `merge` | 合并到 `amra.scheduler.obligations` |
| `orchestrator.py` | 旧 MVP 主编排器 | 过大，跨所有层 | `split+deprecate` | 不做 AMRA 主入口；拆为 service adapters 后 legacy shim |
| `planning.py` | proof plan generation | 与 route ledger/proof agent 重合 | `merge` | 合并到 `amra.proof.routes` |
| `problem_bank.py` | problem bank load/save/registry | 核心输入层 | `keep-core` | `amra.problem_banks.registry` |
| `proof_lab.py` | clean-room proof lab | AMRA ProofAgent 核心 runner | `move` | `amra.proof.lab` |
| `proof_search.py` | autonomous proof-search loop | 大而重，含 retrieval/evaluator/Lean | `split+move` | search policy、runner、reports 分拆 |
| `proof_state.py` | proof artifact tracker | pure/focused agents 依赖 | `keep-core` | `amra.proof.state` |
| `proof_system.py` | proof-system planning/agendas | 与 scheduler/evaluator 相关 | `merge` | 合并到 `amra.proof.agenda` |
| `pure_agents.py` | Codex-episode theorem/proof/Lean agents | AMRA agent runner 核心，但过大 | `split+move` | `amra.agents.episode_loop`、`amra.agents.proof`、`amra.agents.lean` |
| `retrieval.py` | premise retrieval | portfolio memory/reuse 支撑 | `move` | `amra.retrieval` |
| `review.py` | math reviewer | 与 review gate/result bundle 相关 | `merge` | 合并到 `amra.review.project_review` |
| `review_gate.py` | workstream review gate | AMRA proof/review safety 核心 | `keep-core+move` | `amra.review.gates` |
| `runtime.py` | env/resource/guarded command | 核心基础设施 | `keep-core` | `amra.infra.runtime` |
| `scouting.py` | deterministic problem readiness scout | 与 `math_scout.py` 重合但更静态 | `merge` | 合并到 `amra.portfolio.scout` |
| `strategy.py` | open problem strategy planner | 与 evaluator/scheduler 重合 | `merge` | 合并到 ranking/evaluation policy |
| `uncertainty.py` | uncertainty + failed route ledger | AMRA failed-route memory 核心 | `merge` | 并入 `amra.portfolio_memory`，保留 schema compatibility |
| `workspace.py` | path/json/project workspace helpers | 入边最多，核心基础设施 | `keep-core+split` | `amra.core.workspace`、`amra.core.io`、`amra.projects.workspace` |
| `workstreams.py` | ProjectState/Workstream/Claim/Review records | 与 AMRA lifecycle/claim ledger 重合 | `merge` | 映射到 AMRA problem/claim/route/review schemas |
| `writing.py` | manuscript blueprint | AMRA 不应主导论文写作 | `deprecate+merge` | 仅保留 writing brief/result bundle export |

## 4. 模块簇和处理顺序

### 4.1 第一批：基础设施，先迁移不改语义

这些模块入边多，先只复制/迁移 API，不做行为重写：

- `models.py`
- `workspace.py`
- `runtime.py`
- `lean_audit.py`
- `lean_contract.py`
- `context.py`
- `problem_bank.py`
- `artifact_graph.py`

目标：新代码可以 import `amra.core.*` / `amra.lean.*`，旧 import 仍可用。

### 4.2 第二批：portfolio/memory 合并

这些模块应围绕 AMRA portfolio schema 统一：

- `workstreams.py`
- `uncertainty.py`
- `coordinator.py`
- `comath_capabilities.py`
- `obligation_refiner.py`
- `scouting.py`
- `math_scout.py`
- `evaluator.py`

目标：problem lifecycle、claim ledger、route ledger、failed route、evaluator recommendation 不再分散在 CoMath 和 portfolio 两套模型里。

### 4.3 第三批：proof/Lean agent runner 整理

这些模块是 AMRA 的核心执行能力，不删除，但要拆分边界：

- `proof_lab.py`
- `pure_agents.py`
- `focused_attack.py`
- `lean_formalizer.py`
- `campaign_loop.py`
- `goal_campaign.py`
- `closure.py`
- `proof_search.py`
- `math_attack.py`

目标：统一成 AMRA agent runner + scheduler 的执行后端，每次运行必须写 durable run directory。

`pure_agents.py` 是最近新增的关键执行模块，不能等同于普通 legacy 模块清理。它应先进入
`amra.agents.*` canonical runner，再由 scheduler 调用。迁移时必须保留现有
`CodexEpisodeLoopAgent`、`NaturalLanguageTheoremProverAgent`、`LeanFromNaturalProofAgent`、
`UnifiedProofAgentLoop` 行为和测试覆盖。

### 4.4 第四批：库和结果包

- `ara_library.py`
- `lean.py`
- `review_gate.py`
- `review.py`
- `writing.py`
- `deliverables.py`

目标：`ara_library` 迁移为 `amra_library`；写作类功能只服务 `amra_result_bundle` 和 ARA 消费，不再作为 AMRA 主流程。

### 4.5 第五批：大聚合层拆除

- `cli.py`
- `orchestrator.py`

目标：`amra.cli` 只组合子命令；`orchestrator.py` 不再是 AMRA 主编排入口，拆成各领域 service adapter 后变成 legacy shim。

## 5. 删除规则

短期不删除任何 `src/ara_math/*.py`。删除只允许发生在专门的 cleanup 任务中，且必须满足：

- 对应 `amra.*` canonical module 已存在；
- legacy import 有 shim 或迁移说明；
- 所有直接测试改为 canonical import，legacy tests 只测兼容；
- `python3 -m ara_math ...` 仍通过；
- ARA 通过 `research_lab.yaml` 仍能发现 AMRA；
- harness validation 通过。

## 6. Section 16.2 临时反向依赖例外

`src/amra` 原则上不能新增对 `ara_math` 的依赖。下面例外只用于尚未迁移完成的模块，必须由
`tests/test_amra_legacy_shims.py` 的 import audit 固定；新增例外需要先更新本节并说明迁移归宿。

- `src/amra/cli.py` -> `ara_math.banking`、`ara_math.campaign_loop`、`ara_math.comath_benchmarks`、`ara_math.comath_capabilities`、`ara_math.comath_source_audit`、`ara_math.comath_specialists`、`ara_math.coordinator`、`ara_math.goal_campaign`、`ara_math.orchestrator`、`ara_math.proof_lab`、`ara_math.scouting`、`ara_math.workstreams`：canonical CLI 聚合层已迁入 `amra.cli`，但这些命令处理器尚未拆到 canonical 子模块；`ara_math.cli` 只保留 deprecated shim。
- `src/amra/math_scout.py` -> `ara_math.scouting`：active scout runner 已迁入 canonical 模块，但 deterministic readiness helper 仍在 legacy scouting 模块，后续与 portfolio scout 合并。
- `src/amra/core/artifact_graph.py` -> `ara_math.workstreams`：artifact graph schema 暂时复用 legacy workstream enum/status。
- `src/amra/core/workspace.py` -> `ara_math.coordinator`：legacy project initialization/dashboard helper 仍由 coordinator 提供。

当前已经迁移并降级为 deprecated shim 的 legacy 模块包括：
`src/ara_math/models.py`、`src/ara_math/workspace.py`、`src/ara_math/runtime.py`、
`src/ara_math/context.py`、`src/ara_math/problem_bank.py`、`src/ara_math/artifact_graph.py`、
`src/ara_math/lean_audit.py`、`src/ara_math/lean_contract.py`、`src/ara_math/agent_tools.py`、
`src/ara_math/ara_library.py`、`src/ara_math/proof_state.py`、`src/ara_math/pure_agents.py`、
`src/ara_math/cli.py`、`src/ara_math/focused_attack.py`、`src/ara_math/math_scout.py`、
`src/ara_math/erdos_status.py`。

## 7. 立即需要加入 roadmap 的任务

新增一个前置任务：`amra-legacy-module-disposition`

验收：

- 本文档存在并覆盖全部 `src/ara_math/*.py` 文件；
- 自动检查文件列表和处置表一致，且处置标签来自第 2 节定义；
- 后续 roadmap 任务引用本文档，不再笼统写“改名”；
- 不执行删除。
