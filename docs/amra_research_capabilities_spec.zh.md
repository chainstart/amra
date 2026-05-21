# AMRA 数学研究能力扩展 Spec

状态：Phase 1 ontology 已实现，后续能力包待实现
创建日期：2026-05-21
负责人：AMRA

## 1. 背景

AMRA 当前已经具备较完整的数学题目组合攻关、证明搜索、Lean 形式化、source audit、review gate、result bundle 和 canonical CLI 能力。现有系统的主轴仍然是：

- 从题库中选择数学题目；
- 生成证明路线和子命题；
- 执行自然语言证明、计算检查或 Lean 形式化；
- 通过 review gate 和 result bundle 交付可验证结果。

这条路线适合 IMO、竞赛题、closed theorem、开放问题攻关和 Lean formalization，但数学研究并不只包含计算和证明。完整的数学研究系统还需要支持：

- 新定义和新理论结构的提出；
- 新命题和猜想的发现；
- 反例、构造和极端样例搜索；
- 算法设计、复杂度分析和优化；
- 应用场景下的建模、参数估计和验证；
- 密码学与安全中的安全游戏、归约和攻击搜索；
- 机器学习与神经网络中的理论命题、经验规律和优化机制分析；
- 可复现实验、benchmark、负结果和研究记忆沉淀。

本文定义 AMRA 从“证明自动化系统”扩展为“数学研究自动化系统”的目标架构、数据模型、执行器、评审标准和阶段性验收方式。

## 2. 目标

AMRA Research Capabilities Expansion 的目标是让系统能够围绕更广泛的数学研究对象运行，而不是只围绕 theorem/proof 运行。

系统应该能够：

- 把猜想、实验、算法、模型、数据集、benchmark、反例、构造、安全假设和负结果作为一等 artifact 持久保存；
- 对研究命题执行 `propose -> test -> refine -> promote/reject -> archive` 循环；
- 用计算实验、SMT/SAT、搜索、仿真、benchmark 和形式化工具为研究对象提供证据；
- 区分证明证据、经验支持、统计证据、反例证据、benchmark 证据和 source 证据；
- 对新命题做 novelty audit，避免把已知结论包装为新结果；
- 对实验和 benchmark 做 reproducibility audit；
- 对建模结果做假设、参数、单位、外推范围和验证数据审查；
- 对密码学与安全结果做 threat model、security game、assumption 和 attack surface 审查；
- 对机器学习理论结果明确区分 theorem、empirical observation、heuristic explanation 和 open gap；
- 将有价值的研究资产提升为 proof task、Lean formalization task、paper section 或 reusable library candidate；
- 将失败路线和负结果保留为可复用研究记忆。

## 3. 非目标

本扩展不要求 AMRA 立即具备完全自动发现重大新理论的能力。

本扩展不应该：

- 把经验实验误标为已经证明的数学定理；
- 因为小规模搜索没有找到反例就声称命题为真；
- 因为 benchmark 上有提升就声称算法理论更优；
- 在没有 threat model 的情况下声称密码学方案安全；
- 在没有数据来源、seed、配置和统计审查的情况下接受机器学习实验结论；
- 用单个可变摘要覆盖研究过程中的失败路线、参数选择和负结果；
- 绕过现有 proof/Lean/source/review gate；
- 破坏 canonical `src/amra` 与 deprecated `src/ara_math` shim 的边界。

## 4. 现有基础

当前 AMRA 已有若干可复用基础，扩展应在这些基础上增量实现。

| 能力 | 当前基础 | 扩展方向 |
| --- | --- | --- |
| proof/formalization | `amra.proof`、`amra.lean` | 继续作为 theorem-grade verification 层 |
| project state | `amra.core`、`amra.orchestration` | 扩展为 research object state |
| artifact graph | `amra.core.artifact_graph` | 增加实验、模型、算法、benchmark、反例等 artifact |
| domain executors | `amra.domain_executors` | 泛化为 research executors |
| source audit | `amra.sources` | 增加 novelty、claim similarity 和 citation graph |
| evaluation/scouting | `amra.evaluation` | 支持非证明任务的价值评估 |
| review gate | `amra.review` | 增加统计、reproducibility、security、model validation gate |
| portfolio campaign | `amra.portfolio_*` | 从 theorem portfolio 扩展到 research portfolio |
| tool inventory | `amra.math_tools` | 支撑实验、SMT/SAT、CAS、benchmark 和 search |
| result bundle | `amra.result_bundle` | 增加 experiment、benchmark、negative result 和 theory map |

## 5. 核心原则

### 5.1 研究对象先于执行脚本

任何计算实验、搜索、benchmark、建模或攻击尝试，都必须挂到明确的 research object 上。脚本输出不是最终事实，只有带有上下文、参数、证据、审查状态和依赖关系的 artifact 才能被系统引用。

### 5.2 证据类型必须分级

AMRA 必须区分以下证据：

- `proof_evidence`：自然语言证明或可审查证明草稿；
- `lean_verified`：Lean 无 placeholder 验证；
- `computation_certificate`：可复现计算证书；
- `empirical_evidence`：实验或仿真支持；
- `statistical_evidence`：带统计检验或置信区间的证据；
- `benchmark_evidence`：在固定 benchmark 上的结果；
- `counterexample_evidence`：反例或反例候选；
- `source_evidence`：文献、数据库或标准来源；
- `security_evidence`：安全游戏、归约、攻击失败或攻击成功记录；
- `negative_evidence`：失败路线、不可行证据或反证。

不同证据不能互相冒充。经验支持不能自动升级为证明；benchmark 提升不能自动升级为复杂度结论；攻击未成功不能自动升级为安全证明。

### 5.3 负结果是研究资产

失败路线、反例、搜索无果、建模失配、benchmark 退化和攻击成功都必须保存。负结果用于：

- 避免重复探索；
- 缩小命题条件；
- 生成更精确的猜想；
- 判断研究方向是否应 park/freeze；
- 为论文或报告提供 limitation 和 related failure context。

### 5.4 可复现性是默认要求

所有实验、benchmark、搜索和建模任务必须尽量记录：

- 输入数据；
- 参数；
- seed；
- tool version；
- environment；
- budget；
- timeout；
- command；
- artifact checksum；
- rerun instruction；
- expected output schema。

无法复现的结果可以保留为 observation，但不能作为高置信结论。

## 6. 目标模块结构

建议新增以下 canonical package：

```text
src/amra/research/
  __init__.py
  objects.py
  graph.py
  evidence.py
  hypothesis_loop.py
  novelty.py
  reproducibility.py
  result_schema.py

src/amra/discovery/
  __init__.py
  conjecture_mining.py
  counterexample_search.py
  construction_search.py
  analogy.py

src/amra/algorithms/
  __init__.py
  specs.py
  benchmark.py
  optimization.py
  profiling.py
  complexity.py

src/amra/modeling/
  __init__.py
  model_spec.py
  calibration.py
  validation.py
  sensitivity.py

src/amra/crypto/
  __init__.py
  threat_model.py
  security_game.py
  reductions.py
  attack_search.py

src/amra/ml_theory/
  __init__.py
  experiment_manifest.py
  optimization_probes.py
  scaling_laws.py
  theory_claims.py

src/amra/research_review/
  __init__.py
  novelty_gate.py
  reproducibility_gate.py
  statistical_gate.py
  benchmark_gate.py
  model_validation_gate.py
  security_gate.py
  theory_coherence_gate.py
```

这些模块不替代 `amra.proof` 和 `amra.lean`。它们应该把成熟命题提升到证明系统，而不是绕开证明系统。

## 7. Research Object 数据模型

实现状态（2026-05-21）：Phase 1 已在 canonical `src/amra/research` 中实现 research object 与 evidence dataclasses，并通过 deterministic regression 固定 serialization、typed records 和 theorem-grade evidence boundary。后续 executor、review gate 和 portfolio 集成在后续任务中实现。

### 7.1 通用 ResearchObjectRecord

所有研究对象共享基础字段。

```json
{
  "object_id": "research-20260521-0001",
  "object_type": "conjecture",
  "title": "Bounded search suggests a divisibility invariant",
  "status": "active",
  "created_at": "2026-05-21T00:00:00+08:00",
  "updated_at": "2026-05-21T00:00:00+08:00",
  "domain": "number_theory",
  "tags": ["conjecture_mining", "divisibility"],
  "statement": "For all tested n <= 10^6, ...",
  "confidence": "low",
  "evidence_ids": [],
  "source_ids": [],
  "artifact_ids": [],
  "blocked_by": [],
  "metadata": {}
}
```

允许的 `object_type`：

- `conjecture`
- `hypothesis`
- `experiment`
- `dataset`
- `algorithm`
- `model`
- `benchmark`
- `counterexample`
- `construction`
- `security_game`
- `security_assumption`
- `ml_theory_claim`
- `negative_result`
- `theory_node`

允许的 `status`：

- `draft`
- `active`
- `testing`
- `empirically_supported`
- `counterexample_found`
- `proof_candidate`
- `lean_candidate`
- `verified`
- `rejected`
- `parked`
- `frozen`
- `archived`

### 7.2 ConjectureRecord

```json
{
  "object_type": "conjecture",
  "formal_statement": null,
  "informal_statement": "",
  "scope": "",
  "known_cases": [],
  "excluded_cases": [],
  "counterexample_search": [],
  "novelty_report": null,
  "promotion_target": "proof_task"
}
```

### 7.3 ExperimentRecord

```json
{
  "object_type": "experiment",
  "question": "",
  "method": "",
  "inputs": [],
  "parameters": {},
  "seed": null,
  "budget": {},
  "environment": {},
  "command": "",
  "outputs": [],
  "result_summary": "",
  "rerun_status": "not_rerun",
  "reproducibility_report": null
}
```

### 7.4 AlgorithmRecord

```json
{
  "object_type": "algorithm",
  "problem_spec": "",
  "baseline_ids": [],
  "candidate_ids": [],
  "complexity_claims": [],
  "benchmark_ids": [],
  "profiling_reports": [],
  "ablation_reports": [],
  "regression_risks": []
}
```

### 7.5 ModelRecord

```json
{
  "object_type": "model",
  "application_domain": "",
  "variables": [],
  "assumptions": [],
  "units": {},
  "parameters": {},
  "calibration_data": [],
  "validation_data": [],
  "sensitivity_reports": [],
  "validity_range": "",
  "known_failure_modes": []
}
```

### 7.6 SecurityGameRecord

```json
{
  "object_type": "security_game",
  "scheme": "",
  "adversary_model": "",
  "oracle_access": [],
  "winning_condition": "",
  "assumptions": [],
  "reductions": [],
  "attack_attempts": [],
  "security_status": "unstated"
}
```

### 7.7 MLTheoryClaimRecord

```json
{
  "object_type": "ml_theory_claim",
  "claim_kind": "empirical_observation",
  "training_setup": {},
  "dataset_ids": [],
  "metric_ids": [],
  "theoretical_statement": "",
  "empirical_support": [],
  "known_gaps": [],
  "promotion_target": "conjecture"
}
```

## 8. Artifact Graph 扩展

实现状态（2026-05-21）：`amra.core.artifact_graph` 已增加本节列出的 non-proof artifact kind 与 dependency relation，并提供 generic `record_research_object` helper；`amra.research.graph` 提供 research object/evidence 到 artifact graph 的 deterministic mapping。

`amra.core.artifact_graph` 应增加 artifact kind：

- `CONJECTURE`
- `HYPOTHESIS`
- `EXPERIMENT`
- `DATASET`
- `ALGORITHM`
- `MODEL`
- `BENCHMARK`
- `COUNTEREXAMPLE`
- `CONSTRUCTION`
- `SECURITY_GAME`
- `SECURITY_ASSUMPTION`
- `OPTIMIZATION_TRACE`
- `STATISTICAL_REPORT`
- `NEGATIVE_RESULT`
- `THEORY_NODE`

应增加 dependency relation：

- `GENERALIZES`
- `SPECIALIZES`
- `REFUTES`
- `EMPIRICALLY_SUPPORTS`
- `STATISTICALLY_SUPPORTS`
- `BENCHMARKS`
- `OPTIMIZES`
- `REDUCES_TO`
- `ASSUMES`
- `CALIBRATES`
- `VALIDATES`
- `INVALIDATES`
- `PRODUCES_COUNTEREXAMPLE`
- `SUGGESTS_CONJECTURE`
- `PROMOTES_TO_PROOF_TASK`

示例：

```json
{
  "from": "experiment-001",
  "to": "conjecture-001",
  "relation": "EMPIRICALLY_SUPPORTS",
  "confidence": "medium",
  "notes": "No counterexample found for n <= 1000000 under fixed search budget."
}
```

## 9. Workstream 扩展

实现状态（2026-05-21）：`amra.orchestration.workstreams` 已增加本节列出的 research workstream kind，并增加 non-proof research workstream status 与 claim/research status。Proof/Lean 状态和值保持兼容。

`amra.orchestration.workstreams` 应增加 workstream kind：

- `DISCOVERY`
- `EXPERIMENT`
- `ALGORITHM`
- `MODELING`
- `CRYPTO`
- `ML_THEORY`
- `BENCHMARK`
- `DATA`
- `THEORY_BUILDING`

应增加 claim/research status：

- `CONJECTURED`
- `EMPIRICALLY_SUPPORTED`
- `STATISTICALLY_SUPPORTED`
- `COUNTEREXAMPLE_FOUND`
- `MODEL_CALIBRATED`
- `MODEL_VALIDATED`
- `BENCHMARKED`
- `OPTIMIZED`
- `SECURITY_GAME_DEFINED`
- `ATTACK_FOUND`
- `REDUCTION_CANDIDATE`
- `NOVELTY_CHECKED`
- `REPRODUCED`
- `REJECTED_BY_EVIDENCE`

Proof/Lean workstream 仍保留最终定理级验证职责。非证明 workstream 只能将对象提升为 `proof_candidate` 或 `lean_candidate`，不能直接标记为 theorem-grade verified。

## 10. Research Executor 接口

现有 `DomainSearchExecutor` 应保留，同时新增更一般的 `ResearchExecutor`。

```python
class ResearchExecutor:
    executor_id: str
    supported_object_types: list[str]
    supported_domains: list[str]

    def can_run(self, request: ResearchExecutionRequest) -> bool:
        ...

    def run(self, request: ResearchExecutionRequest) -> ResearchExecutionResult:
        ...
```

`ResearchExecutionResult` 至少包含：

- `status`
- `result_kind`
- `summary`
- `evidence`
- `artifacts`
- `commands`
- `budget_used`
- `reproducibility`
- `next_actions`

允许的 `result_kind`：

- `conjecture`
- `counterexample`
- `construction`
- `benchmark_result`
- `optimization_trace`
- `statistical_evidence`
- `model_fit`
- `security_attack`
- `reduction_candidate`
- `negative_result`
- `proof_candidate`

## 11. 能力包规范

### 11.1 Discovery Pack

目标：从数据、例子、已知定理、失败路线和类比中提出新命题。

核心能力：

- integer sequence 和 combinatorial structure mining；
- invariant detection；
- small counterexample search；
- construction search；
- analogy transfer；
- conjecture refinement；
- novelty audit handoff。

验收标准：

- 能从固定 fixture 生成至少一个 conjecture record；
- 能运行 bounded counterexample search；
- 能把被反例推翻的猜想标记为 `rejected_by_evidence`；
- 能把未被推翻且有价值的猜想提升为 `proof_candidate`。

### 11.2 Algorithms Pack

目标：支持算法设计、优化、benchmark 和复杂度经验分析。

核心能力：

- algorithm problem spec；
- baseline registry；
- benchmark harness；
- profiler integration；
- optimization trace；
- ablation；
- regression detection；
- empirical complexity fitting。

验收标准：

- 每次 benchmark 有固定输入、指标、baseline 和输出 schema；
- 每个优化结果能追溯到 baseline；
- 性能提升必须附带 regression risk；
- 理论复杂度声明必须进入 proof/theory review，不能只靠 benchmark 接受。

### 11.3 Modeling Pack

目标：支持应用场景下的数学建模。

核心能力：

- variables/units/assumptions schema；
- parameter calibration；
- validation set；
- sensitivity analysis；
- uncertainty propagation；
- extrapolation warning；
- model failure mode ledger。

验收标准：

- 模型必须声明变量、单位、假设和有效范围；
- 参数必须标明来源或校准方法；
- 验证数据和校准数据必须区分；
- 外推结论必须被 gate 标记风险。

### 11.4 Crypto/Security Pack

目标：支持密码学、安全协议和安全假设研究。

核心能力：

- threat model；
- security game；
- adversary capability；
- oracle model；
- reduction graph；
- bounded attack search；
- assumption audit；
- toy parameter validation。

验收标准：

- 没有 threat model 时不能接受 security claim；
- attack success 必须生成 counterexample/security_attack artifact；
- attack failure 只能作为 bounded evidence，不能作为安全证明；
- security reduction 必须标明依赖假设和损失项。

### 11.5 ML Theory Pack

目标：支持神经网络和机器学习中的理论命题、经验规律和优化机制研究。

核心能力：

- experiment manifest；
- dataset/model/training config ledger；
- seed and environment capture；
- metric schema；
- scaling law fitting；
- optimization probe；
- theorem/empirical boundary tracking；
- leakage and reproducibility audit。

验收标准：

- 每个实验必须记录 dataset、model、optimizer、seed、metric 和 compute budget；
- 经验规律只能标记为 empirical observation 或 conjecture；
- 理论声明必须进入 proof/theory review；
- benchmark 或 dataset leakage 风险必须可被 gate 阻断。

### 11.6 Theory Pack

目标：支持新理论结构的组织和演化。

核心能力：

- definition graph；
- lemma/conjecture graph；
- dependency mining；
- failed hypothesis memory；
- abstraction proposal；
- theory coherence audit；
- paper section outline。

验收标准：

- 新定义必须记录 motivation、examples、non-examples 和依赖；
- 新 lemma 必须标明证明状态；
- 与已有理论冲突的节点必须被 gate 阻断；
- 可复用结构可被提升为 library candidate。

## 12. Review Gates

新增或扩展以下 gates。

### 12.1 Novelty Gate

检查：

- 是否已有相同或等价命题；
- 是否只是变量改名或弱化形式；
- 是否已有文献中的直接 corollary；
- 是否有明确 novelty claim。

输出：

- `novel`
- `known`
- `likely_known`
- `insufficient_source`
- `not_a_novel_claim`

### 12.2 Reproducibility Gate

检查：

- command 是否可重跑；
- seed、版本、输入和环境是否记录；
- 输出 checksum 是否稳定；
- rerun 是否通过；
- budget 是否足够。

输出：

- `reproduced`
- `not_reproduced`
- `partially_reproduced`
- `missing_reproducibility_metadata`

### 12.3 Statistical Gate

检查：

- 样本量；
- 置信区间；
- 多重比较；
- 选择偏差；
- train/test leakage；
- effect size。

输出：

- `statistically_supported`
- `underpowered`
- `leakage_suspected`
- `inconclusive`

### 12.4 Benchmark Gate

检查：

- baseline 是否公平；
- benchmark 是否固定；
- metric 是否合理；
- 是否只优化了单个 case；
- 是否存在 regression。

输出：

- `benchmark_passed`
- `benchmark_regression`
- `baseline_unfair`
- `metric_invalid`
- `insufficient_cases`

### 12.5 Model Validation Gate

检查：

- 变量、单位和假设；
- 参数来源；
- 校准/验证数据分离；
- 敏感性；
- 外推范围；
- 已知 failure modes。

输出：

- `model_validated`
- `model_under_specified`
- `parameter_debt`
- `validation_failed`
- `extrapolation_risk`

### 12.6 Security Gate

检查：

- threat model；
- security game；
- adversary capability；
- assumptions；
- reductions；
- attacks；
- toy vs real parameter gap。

输出：

- `security_claim_reviewed`
- `missing_threat_model`
- `attack_found`
- `assumption_gap`
- `reduction_gap`
- `toy_only`

### 12.7 Theory Coherence Gate

检查：

- 新定义是否非空且有例子；
- 命题之间是否冲突；
- 是否存在 hidden stronger assumption；
- 是否与已知 theorem/source 冲突；
- 是否有清晰 dependency path。

输出：

- `coherent`
- `definition_debt`
- `dependency_gap`
- `conflict_detected`
- `hidden_assumption`

## 13. Portfolio 扩展

现有 portfolio campaign 应扩展为 research portfolio campaign。

新的任务类型：

- `prove_theorem`
- `formalize_statement`
- `mine_conjecture`
- `search_counterexample`
- `optimize_algorithm`
- `run_benchmark`
- `build_model`
- `validate_model`
- `define_security_game`
- `search_attack`
- `probe_ml_theory`
- `organize_theory`

评分维度：

- `expected_information_gain`
- `novelty_potential`
- `evaluator_availability`
- `proof_promotion_potential`
- `computation_cost`
- `reproducibility_risk`
- `source_quality`
- `negative_result_value`
- `paper_value`
- `reusable_asset_value`
- `safety_or_security_risk`

调度策略：

- 先运行低成本 scouting 和 bounded executor；
- 对高信息增益任务投入中等预算；
- 对低 novelty、低 reproducibility 或 source debt 高的任务 park；
- 对出现反例、攻击或模型失配的任务转为 negative result 或 refinement；
- 对 proof-ready 或 Lean-ready 的任务交给现有 proof/Lean pipeline。

## 14. 目录布局

每次 research campaign 应写入独立目录：

```text
artifacts/research_campaigns/<campaign-id>/
  campaign_manifest.json
  research_portfolio.json
  ranking.json
  campaign_log.jsonl
  final_report.md
  objects/
    <object-id>/
      object.json
      evidence.jsonl
      artifact_graph.json
      review/
      runs/
      promotion/
```

单个 research object 目录：

```text
projects/<research-object-id>/
  object.yaml
  state.json
  state_history.jsonl
  evidence/
  experiments/
  benchmarks/
  sources/
  review/
  promotion/
  notes/
```

## 15. CLI 目标

建议新增 CLI：

```text
python3 -m amra research init-object
python3 -m amra research run-executor
python3 -m amra research review-object
python3 -m amra research campaign
python3 -m amra discovery mine-conjectures
python3 -m amra discovery search-counterexample
python3 -m amra algorithms run-benchmark
python3 -m amra algorithms optimize
python3 -m amra modeling validate
python3 -m amra crypto define-game
python3 -m amra crypto search-attack
python3 -m amra ml-theory run-experiment
```

所有 CLI 默认应支持：

- deterministic/local 模式；
- JSON 输出；
- explicit output directory；
- budget/timeout；
- no live model calls unless explicitly enabled；
- result artifact manifest。

## 16. Result Bundle 扩展

AMRA result bundle 应支持非证明研究产物。

新增 bundle artifacts：

- `research_objects.json`
- `research_artifact_graph.json`
- `experiment_reports.jsonl`
- `benchmark_reports.jsonl`
- `negative_results.jsonl`
- `novelty_reports.jsonl`
- `reproducibility_reports.jsonl`
- `model_validation_reports.jsonl`
- `security_review_reports.jsonl`
- `theory_map.json`
- `promotion_candidates.json`

Bundle 必须明确 verification boundary：

- 哪些结果已 Lean verified；
- 哪些只是 proof sketch；
- 哪些是 empirical evidence；
- 哪些是 bounded search evidence；
- 哪些是 benchmark evidence；
- 哪些是 negative result；
- 哪些结论不能作为 theorem 引用。

## 17. 阶段计划

### Phase 1：Research Ontology

任务包：

- `AMRA-RESEARCH-ONTOLOGY-001`
- `AMRA-RESEARCH-ARTIFACT-GRAPH-001`
- `AMRA-RESEARCH-WORKSTREAMS-001`

验收：

- 新增 research object dataclasses；
- artifact graph 支持新 artifact/relation；
- workstream 支持非证明研究任务；
- 有 deterministic unit tests；
- 不影响现有 proof/Lean/portfolio tests。

### Phase 2：Experiment And Reproducibility Harness

任务包：

- `AMRA-EXPERIMENT-HARNESS-001`
- `AMRA-REPRODUCIBILITY-GATE-001`
- `AMRA-RESEARCH-EXECUTOR-001`

验收：

- 可记录并重跑 bounded local experiment；
- 输出 experiment report 和 reproducibility report；
- executor result 能写入 artifact graph；
- result bundle 能包含实验 artifact。

### Phase 3：Discovery And Counterexample Search

任务包：

- `AMRA-CONJECTURE-DISCOVERY-001`
- `AMRA-COUNTEREXAMPLE-SEARCH-001`
- `AMRA-NOVELTY-GATE-001`

验收：

- 可从 fixture 生成 conjecture；
- 可执行 bounded counterexample search；
- 反例能 refute conjecture；
- novelty gate 能区分 known/likely_known/insufficient_source。

### Phase 4：Algorithm Optimization

任务包：

- `AMRA-ALGORITHM-SPEC-001`
- `AMRA-ALGORITHM-BENCHMARK-001`
- `AMRA-ALGORITHM-OPTIMIZATION-001`

验收：

- 支持 baseline/candidate/benchmark schema；
- benchmark 可复跑；
- optimization trace 可审查；
- benchmark gate 能阻断不公平 baseline 或 regression。

### Phase 5：Modeling, Crypto, ML Theory

任务包：

- `AMRA-MODELING-PACK-001`
- `AMRA-CRYPTO-SECURITY-PACK-001`
- `AMRA-ML-THEORY-PACK-001`

验收：

- modeling pack 支持 assumptions/units/calibration/validation；
- crypto pack 支持 threat model/security game/attack record；
- ML theory pack 支持 experiment manifest 和 theorem/empirical boundary；
- 对应 review gates 能生成 blocking decision。

### Phase 6：Research Portfolio And Paper Bundle

任务包：

- `AMRA-RESEARCH-PORTFOLIO-001`
- `AMRA-RESEARCH-RESULT-BUNDLE-001`
- `AMRA-THEORY-MAP-001`

验收：

- portfolio campaign 能混合调度 proof、experiment、discovery、algorithm、modeling 等任务；
- result bundle 能交付 research objects、experiments、negative results 和 promotion candidates；
- theory map 能展示 definitions、lemmas、conjectures、failures 和 proof candidates。

## 18. Requirement 建议

后续同步到 `.engineering/spec_tasks.yaml` 时，建议新增：

| Requirement ID | 标题 | 初始状态 |
| --- | --- | --- |
| `REQ-AMRA-RESEARCH-ONTOLOGY-001` | Research object ontology and artifact graph | `planned` |
| `REQ-AMRA-EXPERIMENT-HARNESS-001` | Reproducible experiment harness | `planned` |
| `REQ-AMRA-CONJECTURE-DISCOVERY-001` | Conjecture discovery and counterexample search | `planned` |
| `REQ-AMRA-ALGORITHM-OPTIMIZATION-001` | Algorithm benchmark and optimization system | `planned` |
| `REQ-AMRA-MODELING-001` | Applied mathematical modeling pack | `planned` |
| `REQ-AMRA-CRYPTO-SECURITY-001` | Cryptography and security research pack | `planned` |
| `REQ-AMRA-ML-THEORY-001` | Machine learning theory research pack | `planned` |
| `REQ-AMRA-RESEARCH-REVIEW-GATES-001` | Novelty, reproducibility, statistical, security and modeling gates | `planned` |
| `REQ-AMRA-RESEARCH-PORTFOLIO-001` | Research portfolio campaign and bundle integration | `planned` |

## 19. 完成定义

本 spec 完成后，AMRA 应不再只是 theorem/proof pipeline，而是能稳定承载多种数学研究活动。

完成标准：

- 非证明研究对象有 canonical schema；
- 实验、benchmark、模型、算法、猜想、反例、安全游戏和负结果能进入 artifact graph；
- bounded executor 能产生可审查 research result；
- review gates 能阻断不可靠的 empirical、statistical、security、modeling 或 benchmark claim；
- portfolio 能调度非证明研究任务；
- result bundle 能清晰区分 theorem、proof candidate、empirical observation、benchmark evidence、counterexample 和 negative result；
- 成熟命题能被提升到现有 proof/Lean pipeline；
- 现有 proof/Lean/portfolio canonical 能力不回退。
