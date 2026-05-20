# AMRA Spec 实现状态矩阵

日期：2026-05-20

状态：动态维护中

主 spec：

- `docs/portfolio_campaign_spec.md`
- `docs/portfolio_campaign_spec.zh.md`
- `docs/repository_relationships_architecture.zh.md`
- `docs/amra_canonical_migration_spec.zh.md`

机器台账：`.engineering/spec_tasks.yaml`

决策记录：`docs/decisions/`

## Requirement 状态

| Requirement ID | 状态 | 当前证据 | 主要缺口 | 下一步 |
| --- | --- | --- | --- | --- |
| `REQ-AMRA-GOV-001` | `completed` | 本文档、`.engineering/spec_tasks.yaml`、决策记录 | 需要随每轮证明系统开发持续更新 | 接入 harness spec-sync |
| `REQ-AMRA-NAMING-001` | `completed` | canonical `amra` package、legacy shim、接口测试；`AMRA-LEGACY-SHIM-CLEANUP-001` 后 `src/ara_math` 51 个 Python 文件全部是 deprecated compatibility shim / forwarding wrapper | 无当前命名迁移缺口 | 保持 canonical/legacy import audit |
| `REQ-AMRA-MANIFEST-001` | `completed` | `research_lab.yaml`、AMRA CLI、ARA-facing contract | 随 ARA bundle contract 演进 | 保持 manifest smoke |
| `REQ-AMRA-PORTFOLIO-001` | `completed` | portfolio scaffold、scheduler/memory 模块；`amra-broad-scouting-integration`、`amra-independent-evaluator`、`amra-memory-consolidation`、`amra-portfolio-active-execution-loop`、`amra-source-quality-ranking`、`amra-domain-search-executors` 已 passed；本轮补齐 campaign ranking 的 difficulty/budget gate、abandon/park policy、resume-pack governance 与 active execution memory consolidation | 生产级长证明 campaign 仍依赖后续 Lean/proof-loop 能力，不在本地 deterministic smoke 内运行 | 保持 portfolio regression 与 CLI smoke，转入 AMRA-LEAN-001 强化 NL/Lean 证明闭环 |
| `REQ-AMRA-PROOF-001` | `completed` | pure/focused proof agents、problem banks、proof attempt 记录；`amra-proof-loop-consolidation`、`amra-agent-tool-normalization`、`amra-nontrivial-closed-theorem-benchmark` 已 passed；`AMRA-PROOF-RUNNERS-MIGRATION-001` 已把 proof_lab/proof_search/closure/math_attack/campaign/goal loop 与 retrieval/planning/proof-system runner 迁入 `amra.proof`；`AMRA-SOURCES-EVALUATION-MIGRATION-001` 已把 source/evaluation/scouting 辅助层迁入 canonical AMRA 模块；`AMRA-CANONICAL-CLI-ORCHESTRATOR-001` 已让 canonical CLI/orchestrator proof/search/formalization smoke path 不再导入 `ara_math`；legacy shim cleanup 已完成；`AMRA-PROOF-STABILITY-001` 新增 bounded deterministic proof-stability benchmark、resume JSONL、failure taxonomy、budget guard 和 mixed proof-search regression fixture | 生产级长证明 campaign 仍需由后续 Lean faithful-modeling 与 library curator 任务提升，但 natural-language/mixed proof-loop harness 缺口已收口 | 保持 `proof-stability benchmark` regression |
| `REQ-AMRA-LEAN-001` | `partial` | Lean executor/audit/contract、形式化产物；`amra-formalization-layer-consolidation`、`amra-known-problem-proof-smoke`、`amra-nontrivial-closed-theorem-benchmark` 已 passed；`AMRA-NL-LEAN-FAITHFULNESS-001` 已补充 faithful-modeling audit，`AMRA-LIBRARY-CURATOR-001` 复用其结果做 verified-only promotion gate | 更难目标上的 formalization 稳定性仍需长周期 campaign 验证 | 保持 proof-stability、faithfulness 和 curator regression |
| `REQ-AMRA-LIBRARY-001` | `completed` | AMRA library manager、library harvesting 计划；`amra-library-harvesting`、`amra-dashboard-result-bundle` 已 passed；`AMRA-LIBRARY-CURATOR-001` 新增 verified-only curator CLI、review records、reusable lemma metadata、rejection reasons 和 result-bundle artifact integration | 不在自动任务内直接写入 checked-in Lean library；promotion-ready artifact 需由后续人工或 harness 步骤应用 | 保持 `amra library curate` regression |
| `REQ-AMRA-ARA-001` | `completed` | AMRA result bundle、`artifact_manifest.json`、`handoff_notes.md`、known-problem smoke；`amra-ara-result-bundle-contract-hardening`、`amra-known-problem-proof-smoke`、`amra-dashboard-result-bundle` 已 passed | 跨仓库 public ARA consumer smoke 需在 ARA 任务 scope 内单独补充 | ARA 消费侧按 bundle consume order 读取 AMRA 产物 |
| `REQ-AMRA-CANONICAL-MIGRATION-001` | `completed` | `docs/amra_canonical_migration_spec.zh.md` 已定义目标和任务包；`src/amra/legacy_migration.py` 已覆盖 51 个 legacy 文件并提供 import audit；orchestration、proof runners、sources/evaluation、CLI/orchestrator 均已迁入 canonical AMRA 模块；`AMRA-LEGACY-SHIM-CLEANUP-001` 后 `src/ara_math` 全部为 deprecated compatibility shim / forwarding wrapper，`src/amra` 无 `ara_math` 反向依赖例外 | 无当前 canonical migration cleanup 缺口 | 保持 shim/audit regression |

## 2026-05-20 Canonical Migration 目标

本轮新增要求：AMRA 的完整数学定理搜索、编排、攻关能力必须由 `src/amra` 承载；`src/ara_math` 不再承载活实现，只保留 deprecated compatibility shim。

目标完成后：

## 剩余 Harness 任务包

- `AMRA-PROOF-STABILITY-001`：已完成；proof-loop 的剩余 partial 已转成 bounded deterministic stability benchmark，记录 resume、失败分类、预算和混合 proof-search regression。
- `AMRA-NL-LEAN-FAITHFULNESS-001`：已完成；自然语言证明义务到 Lean declaration 的 faithful-modeling 检查现在有独立 audit CLI、mismatch taxonomy、blocked formalization evidence 和 result-bundle artifact。
- `AMRA-LIBRARY-CURATOR-001`：已完成；新增 verified-only lemma/library promotion gate、curator review record、复用 metadata、拒绝原因和 result-bundle artifact integration。

- `python3 -m amra` 是 canonical CLI；
- `python3 -m ara_math`、`ara-math`、`ara_math` 只转发；
- `src/amra` 不再依赖 `ara_math` 未声明例外；
- proof search、proof lab、CoMath orchestration、source recovery、review gate、portfolio scheduler、Lean formalizer、result bundle 均有 canonical AMRA 模块入口。

## 2026-05-20 AMRA-CANONICAL-INVENTORY-001 同步说明

- 新增 `src/amra/legacy_migration.py` 作为 canonical migration 的机器清单和 AST import audit 源。
- 清单覆盖全部 51 个 `src/ara_math/*.py` 文件；`AMRA-LEGACY-SHIM-CLEANUP-001` 后全部标记为 `shim` / `retain_compatibility`。
- `tests/test_amra_legacy_migration_map.py` 固定清单覆盖、文档处置表一致性、JSON 可读性和 `src/amra` 反向依赖例外表。

## 2026-05-20 AMRA-ORCHESTRATION-MIGRATION-001 同步说明

- 新增 canonical `amra.orchestration`、`amra.review` 和 `amra.scheduler` package，承载原 CoMath project/workstream/claim state、coordinator loop、uncertainty ledger、review gate 和 workstream executor adapters。
- `ara_math.workstreams`、`ara_math.coordinator`、`ara_math.uncertainty`、`ara_math.review`、`ara_math.review_gate`、`ara_math.comath_runners` 现在是 deprecated compatibility alias。
- 新增 `tests/test_amra_orchestration_state.py`，直接验证 canonical AMRA API 可以创建 dashboard/artifact graph/ledger state、运行 bounded scheduler loop，并保持 legacy module identity。
- 本地验收通过：`python3 -m pytest -q tests/test_amra_orchestration_state.py tests/test_comath_state.py tests/test_comath_scheduler.py tests/test_comath_review_gate.py`。

## 2026-05-20 AMRA-PROOF-RUNNERS-MIGRATION-001 同步说明

- 新增 canonical `amra.proof.lab`、`amra.proof.search`、`amra.proof.closure`、`amra.proof.attack`、`amra.proof.campaign_loop`、`amra.proof.goal_campaign`、`amra.proof.retrieval`、`amra.proof.planning` 和 `amra.proof.proof_system`。
- `amra.proof` package 直接导出 proof lab/search/closure/attack/campaign/goal runner、retriever、planner 和 proof-system planner API；proof-loop registry 保留 legacy adapter ID，但这些 adapter module 解析为 canonical `amra.proof.*` alias。
- `ara_math` 中对应 proof runner 文件现在是 deprecated compatibility alias，旧导入与 canonical 模块共享 module identity。
- 本地验收通过：`python3 -m pytest -q tests/test_amra_proof_runners.py tests/test_proof_lab.py tests/test_proof_search.py tests/test_closure_prover.py tests/test_math_attack.py tests/test_pure_agents.py`。

## 2026-05-20 AMRA-SOURCES-EVALUATION-MIGRATION-001 同步说明

- 新增 canonical `amra.sources.literature`、`amra.sources.source_audit`、`amra.evaluation.capabilities`、`amra.evaluation.specialists`、`amra.evaluation.benchmarks`、`amra.evaluation.evaluator`、`amra.evaluation.strategy`、`amra.evaluation.convergence`、`amra.evaluation.scouting`、`amra.scheduler.obligations` 和 `amra.problem_banks.sync`。
- `ara_math` 中对应 source/evaluation/scouting/banking 文件现在是 deprecated compatibility alias，旧导入与 canonical 模块共享 module identity。
- `amra.math_scout` 直接依赖 `amra.evaluation.scouting`；source audit 和 specialist tests 使用 fake/local provider，避免 live crawling 和 live model calls。
- 本地验收通过：`python3 -m pytest -q tests/test_amra_sources_evaluation.py tests/test_literature.py tests/test_portfolio_evaluator.py tests/test_math_scout.py tests/test_amra_source_quality.py`。

## 2026-05-20 AMRA-CANONICAL-CLI-ORCHESTRATOR-001 同步说明

- 新增 canonical `amra.orchestrator`，`amra.cli` 已改为直接导入 `amra.problem_banks.sync`、`amra.evaluation.*`、`amra.sources.*`、`amra.orchestration.*`、`amra.proof.*`、`amra.lean.*`、`amra.result_bundle` 和 `amra.portfolio_*`。
- `ara_math.cli` 与 `ara_math.orchestrator` 保持 deprecated module alias；`python3 -m ara_math` 转发到 canonical `amra.cli`。
- `TEMPORARY_AMRA_LEGACY_IMPORTS` 已清空，`tests/test_amra_canonical_cli.py` 覆盖 canonical CLI import 边界和 legacy forwarding。
- 本地验收通过：`python3 -m pytest -q tests/test_amra_canonical_cli.py tests/test_cli_flow.py tests/test_amra_known_problem_smoke.py tests/test_amra_result_bundle.py`。
- 本地 smoke 通过：`python3 -m amra run-known-problem-smoke --problem imo_2025_p1 --max-seconds 60 --out /tmp/amra_canonical_cli_bundle --json >/tmp/amra_canonical_cli_bundle.json` 与 `python3 -m ara_math run-known-problem-smoke --problem imo_2025_p1 --max-seconds 60 --out /tmp/amra_legacy_cli_bundle --json >/tmp/amra_legacy_cli_bundle.json`，两者均为 `status=verified`、`llm_calls=0`。

## 2026-05-20 AMRA-LEGACY-SHIM-CLEANUP-001 同步说明

- `ara_math.accessibility`、`ara_math.deliverables`、`ara_math.writing` 已从 legacy 实现文件改为 deprecated module alias。
- `src/amra/legacy_migration.py` 中 51 个 legacy Python 文件全部为 `shim` / `retain_compatibility`，且无 `migration_blocked_by` 条目。
- `tests/test_amra_legacy_migration_map.py` 已同步为最终 cleanup 判定：legacy inventory 不再期望任何 `active_implementation`。

## 2026-05-20 AMRA-PROOF-STABILITY-001 同步说明

- 新增 `amra.proof.stability` 和 CLI `python3 -m amra proof-stability benchmark`，运行 `tests/fixtures/proof_stability_suite.yaml` 中的 deterministic local fixtures。
- benchmark 输出 `proof_stability_report.json`、`proof_stability_resume.jsonl`、per-case `result.json` 和 `summary.md`；报告固定声明 `llm_calls=0`、`live_model_calls=false`。
- failure taxonomy 覆盖 `budget_exhausted`、`blocked_formalization_gap`、`proof_search_exhausted`、`route_selection_regression` 等稳定分类；fixture 中包含 natural-language proof-lab、mixed proof-search、closure blocked gap 和 budget guard regression。
- 设计文档见 `docs/amra_proof_stability_benchmark.md`。

## 2026-05-20 AMRA-NL-LEAN-FAITHFULNESS-001 同步说明

- 新增 `amra.lean.faithfulness` 和 CLI `python3 -m amra formalization audit-faithfulness`，可审计 AMRA result bundle 或 proof-stability report directory。
- audit 输出 `faithfulness_report.json`、`blocked_formalization_evidence.json` 和 `faithfulness_summary.md`；result bundle export 同步写入 `faithful_modeling_report.json` 并在 `artifact_manifest.json` 中链接。
- mismatch taxonomy 覆盖 `faithfully_modeled`、`lean_statement_mismatch`、`missing_lean_declaration`、`blocked_formalization_gap`、`missing_formal_statement`、`informal_only` 和 `budget_guarded` 等分类。
- deterministic fixtures 见 `tests/fixtures/faithfulness_cases.yaml`；设计文档见 `docs/amra_nl_lean_faithfulness.md`。

## 2026-05-19 同步说明

- `amra-next-development-targets` 里共有 9 个任务；截至 `2026-05-19T07:21:56Z`，其中 8 个在 manifest 中已是 `passed`，1 个（`amra-canonical-core-migration`）为 `failed`。
- 这次已将 `.engineering/roadmap.yaml` 的该里程碑和对应任务状态同步到 manifest 实际结果，不再停留在统一的 `pending/planned`。
- 当前 AMRA 的主要矛盾不是“没做”，而是“已有较多实现，但 canonical migration 最后一段和跨仓库生产级闭环仍未收口”。
- `AMRA-ARA-001` 已补齐本仓库内的 ARA-facing bundle handoff：deterministic known-problem smoke 输出 `artifact_manifest.json`、`lean_build_report.json`、`verified_declarations.json`、`natural_language_proof_sketches.json`、`unresolved_blockers.md`、`limitations.md`、`writing_brief.md` 和 `handoff_notes.md`，并在 manifest 中声明 verification boundaries、Lean status、file checksums 和 ARA consume order。
- `AMRA-PORTFOLIO-001` 已补齐本仓库内的 portfolio campaign e2e loop：broad scout、source quality、domain executor signal、difficulty ranking、budget gate、abandon/park policy、isolated active execution、resume pack 与 global memory consolidation 都有 deterministic local regression。

## 维护流程

1. 开发前在 `.engineering/spec_tasks.yaml` 中确认任务和 requirement ID。
2. 开发后记录测试命令、Lean build 报告、result bundle、proof attempt ledger 或 blocker。
3. 如果发现 theorem statement、Lean modeling 或 proof route 改变，必须写入决策记录或 proof ledger。
4. 未验证 lemma 不能进入 reusable library，只能作为 candidate 或 blocker 证据。
