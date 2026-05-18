# AMRA 题目组合攻关系统 Spec

状态：草案
创建日期：2026-05-18
负责人：AMRA

本文是 [portfolio_campaign_spec.md](portfolio_campaign_spec.md) 的中文版本。

## 1. 目标

AMRA，即 Automated Mathematical Research Agents，应该围绕一个广泛题目组合来优化：尽快产出经过验证的数学结果和可复用证明资产，而不是反复把大量资源耗在单个困难题目上。

系统应该能够：

- 对大量题目做浅层探测；
- 识别更可能快速产出完整证明或 Lean 形式化的题目；
- 将容易或高价值目标提升为重点攻关对象；
- 对困难、题意不清、或疑似有反例的目标进行停放，同时不丢失已有工作；
- 持久保存所有尝试、失败路线、部分引理、证明草稿、Lean 产物和审阅结果，作为后续工作的 memory；
- 将已经完成的 Lean 声明收获到共享本地库中。

本文定义组合级 campaign 系统的架构、数据模型、agent 角色、调度策略、memory 布局和开发阶段。

## 2. 命名与全量改名要求

项目名称确定为 AMRA。

本次重构中，旧的 `amra` 命名必须在代码、文档、CLI、测试、artifacts 和本地库 packaging 中全量替换为 AMRA 命名。

规范名称：

- 产品/系统名称：`AMRA`。
- 全称：`Automated Mathematical Research Agents`。
- 仓库名：`amra`。
- Python 包名：`amra`。
- Python 源码根目录：`src/amra`。
- CLI module：`python3 -m amra`。
- 可选 console script：`amra`。
- 本地可复用 Lean 库目录：`amra_library`。
- 本地可复用 Lean 库模块前缀：`AmraLibrary`。

必须执行的 rename map：

- `amra` -> `amra`。
- `ara_math` -> `amra`。
- `ARA Math` -> `AMRA`。
- `ara_library` -> `amra_library`。
- `AraLibrary` -> `AmraLibrary`。

向后兼容 alias 只允许作为临时迁移 shim 存在，并且必须标记 deprecated。新的实现、测试、文档和生成 artifact 应只使用 AMRA 命名。

## 3. 核心原则

优化单位是整个题目集合，而不是单个题目。

单题循环在目标被提升之后仍然有价值，但外层循环必须持续回答：

- 现在最可能产出已验证结果的是哪一道题？
- 哪一道题正在消耗时间但没有可衡量进展？
- 哪些部分结果应该被抽取出来，在其他题目中复用？
- 哪些失败路线必须记录下来，避免未来 agent 重复踩坑？

## 4. 可复用的现有组件

当前仓库已经有若干有用基础：

- `src/amra/math_scout.py`：浅层题目探测和主动 readiness 评估。
- `src/amra/campaign_loop.py`：单目标迭代证明/形式化循环。
- `src/amra/focused_attack.py`：针对命名 Lean 目标的有界攻关。
- `src/amra/pure_agents.py`：Codex 风格的可执行动作、观察结果的 agent 循环。
- `src/amra/artifact_graph.py`：持久 artifact/dependency graph。
- `src/amra/amra_library.py`：本地可复用 Lean 库管理器。
- `src/amra/comath_capabilities.py`：已有 theory memory 和 failed hypothesis 支持。
- `src/amra/review_gate.py`：独立审阅和 gate 机制。
- `data/problem_bank.yaml` 和 `data/banks/*.yaml`：题目来源。

组合攻关系统应该扩展这些模块，而不是推倒重写。

## 5. 非目标

本系统不应该：

- 假设每个被提升的题目都必须被解决；
- 因为证明 agent 声称证明完成就直接相信；
- 覆盖历史尝试，或把历史压缩成单个可变摘要；
- 要求每个部分引理都被全局提升；
- 允许多个 worker 同时写同一个 Lean 文件；
- 在题目通过独立可行性评估之前投入长预算。

## 6. 题目生命周期

每个题目都应该有明确生命周期状态。

允许状态：

- `unseen`：已从题库加载，但尚未主动探测。
- `scouted`：已完成浅层探测。
- `promising`：评估器建议继续投入。
- `active_attack`：当前正在获得重点证明/形式化资源。
- `formalization_ready`：自然语言证明或路线已经足够清楚，可以进入 Lean 工作。
- `verified`：主目标或被接受的子目标已经在 Lean 中无 placeholder 验证通过。
- `library_harvested`：可复用声明已经提升到 `amra_library`。
- `parked`：当前不值得继续投入，但未来可以恢复。
- `frozen`：没有人工 override 不应恢复。
- `counterexample_suspected`：当前 statement 或路线疑似为假。
- `needs_source`：精确题意或来源证据不足。

状态迁移必须以 append-only 方式写入历史日志。

示例：

```json
{
  "problem_id": "imo-2025-p6",
  "state": "counterexample_suspected",
  "previous_state": "active_attack",
  "changed_at": "2026-05-18T00:00:00+08:00",
  "reason": "Focused Lean attack found a diagonal uncovered-set counterexample candidate for the side-filter multiplicity lemma.",
  "evidence": [
    "projects/imo-2025-p6-formal-20260516/formal/focused_runs/p6-side-filter-multiplicity-2h-20260518/attack_note.md"
  ]
}
```

## 7. 目录布局

### 6.1 组合级 Run

每次 portfolio campaign run 应该写入一个不可变 run 目录：

```text
artifacts/portfolio_campaigns/<campaign-id>/
  campaign_manifest.json
  campaign_state.json
  campaign_log.jsonl
  scout_report.json
  evaluator_report.json
  ranking.json
  promotion_queue.json
  parked_queue.json
  active_assignments.json
  final_report.md
  problems/
    <problem-id>/
      probe/
      evaluation/
      promotion/
      attack_runs/
      formalization_runs/
      review/
```

### 6.2 单题项目

每个严肃攻关题目应该有一个持久项目目录：

```text
projects/<problem-id>/
  problem.yaml
  state.json
  state_history.jsonl
  difficulty.json
  resume_pack.md
  memory/
    claim_ledger.json
    route_ledger.json
    failed_routes.json
    evidence_index.json
    reviewer_notes.jsonl
  proof/
    sketches/
    audits/
    blockers/
    current_focus.md
  formal/
    MathProject/
  runs/
    <run-id>/
      run_manifest.json
      prompt.txt
      output.md
      report.json
      observations.jsonl
      tool_logs/
```

### 6.3 全局索引

组合级 memory 应该维护全局索引：

```text
artifacts/global_memory/
  problem_index.json
  claim_index.json
  failed_route_index.json
  theorem_asset_index.json
  difficulty_history.jsonl
```

这些索引不应该取代项目本地 memory。它们只是搜索和检索加速器。

## 8. Memory 模型

### 7.1 Claim Ledger

Claim ledger 是数学断言的权威记录。

每个 claim 应该包含：

- 稳定的 `claim_id`；
- 人类可读 statement；
- 可选 Lean 声明名；
- 状态；
- 依赖；
- 证明证据；
- 反例证据；
- 来源 provenance；
- 所属题目；
- 是否可复用。

示例：

```json
{
  "claim_id": "imo2025-p6-side-filter-multiplicity",
  "kind": "lemma",
  "statement_nl": "The eight side-pair filters around a common increasing/decreasing chain cell have cardinality at least 2025 + incLen + decLen - 3.",
  "lean_name": "P6Tiling.sidePairFilterMultiplicityLowerBound2025",
  "status": "counterexample_suspected",
  "dependencies": [
    "imo2025-p6-longest-chain-arm-sum",
    "imo2025-p6-side-pair-covering"
  ],
  "evidence": [
    {
      "type": "counterexample_candidate",
      "path": "focused_runs/p6-side-filter-multiplicity-2h-20260518/attack_note.md"
    }
  ],
  "reusable": false,
  "updated_at": "2026-05-18T00:00:00+08:00"
}
```

允许的 claim 状态：

- `hypothesis`
- `sketch`
- `route_supported`
- `needs_review`
- `review_rejected`
- `lean_stubbed`
- `lean_partial`
- `lean_verified`
- `counterexample_suspected`
- `false`
- `obsolete`

### 7.2 Route Ledger

Route ledger 记录证明策略，而不仅仅是 claim。

每条 route 应该包含：

- route 名称；
- 目标 claim；
- 核心想法；
- 所需依赖；
- 当前 blocker；
- 尝试历史；
- evaluator verdict；
- 继续投入成本估计。

示例状态：

- `new`
- `promising`
- `blocked`
- `failed`
- `superseded`
- `completed`

### 7.3 Failed Route Memory

失败路线必须成为一等 memory。这对于避免 P6 式重复循环非常关键。

每条 failed route 应该包含：

- 精确失败断言或方法；
- 失败模式；
- 证据路径；
- 失败是否属于逻辑、建模、形式化、来源或资源问题；
- 未来恢复条件。

示例失败模式：

- `counterexample_candidate`
- `lean_statement_mismatch`
- `missing_mathlib_api`
- `proof_gap`
- `combinatorial_case_explosion`
- `modeling_too_weak`
- `resource_timeout`

## 9. 难度评估

难度评估必须独立于证明生成。

### 8.1 分数

每个题目获得一个 `difficulty.json`：

```json
{
  "problem_id": "imo-2025-p1",
  "generated_at": "2026-05-18T00:00:00+08:00",
  "feasibility_score": 8.2,
  "formalization_score": 7.5,
  "expected_hours_to_result": 4.0,
  "confidence": 0.7,
  "recommendation": "promote",
  "primary_blocker": "formalization",
  "risk_flags": [],
  "evidence": [
    "artifacts/imo/2025/pure_proof_agent_runs/..."
  ]
}
```

### 8.2 信号

评估器应该考虑：

- 精确 statement 是否可用；
- 是否有已知定理或来源材料；
- 浅层证明是否成功；
- 未解决 obligation 的数量和深度；
- Lean build 状态；
- placeholder 数量；
- 形式化 statement 是否匹配自然语言定理；
- 每小时进展速度；
- 重复失败尝试次数；
- 是否出现反例候选；
- 是否依赖大量缺失理论；
- 中间引理的可复用性。

### 8.3 提升规则

默认提升阈值：

- 若 `feasibility_score >= 7` 且没有严重风险标记，则提升。
- 若存在已知定理/来源，且形式化看起来有界，则提升。
- 若 `feasibility_score < 5`，则停放。
- 若连续两次 run 没有可衡量进展，则停放。
- 若有强反例候选且未解决，则冻结。
- 若精确 statement 或 provenance 缺失，则送入 source recovery。

### 8.4 进展速度

每次 active attack 都应该更新进展指标：

```json
{
  "lean_verified_declarations_added": 3,
  "open_obligations_before": 12,
  "open_obligations_after": 7,
  "placeholder_count_before": 5,
  "placeholder_count_after": 2,
  "new_failed_routes": 1,
  "elapsed_seconds": 7200,
  "progress_velocity": 0.42
}
```

如果连续两轮 velocity 接近 0，除非存在人工 override，scheduler 应该停放该题。

## 10. Agent 角色

### 9.1 ScoutAgent

目的：短预算广泛探测。

输入：

- 题目 statement；
- metadata；
- 本地资产；
- 先前全局 memory 命中。

输出：

- 精确 statement 状态；
- 浅层证明尝试；
- 可能的已知定理；
- 可能的形式化目标；
- 可行性分数；
- blocker 类别。

默认预算：每题 5 到 20 分钟。

ScoutAgent 默认应该是 read-only。

### 9.2 ProofAgent

目的：生成或修正数学证明路线。

输入：

- 已提升题目；
- claim ledger；
- route ledger；
- evaluator 约束；
- 相关库 inventory。

输出：

- 自然语言证明草稿；
- 引理分解；
- 显式依赖图；
- 候选 Lean theorem statements；
- 反例检查。

ProofAgent 可以使用 Lean quick check、搜索、计算、本地脚本等工具。它不应该被限制为纯自然语言推理。

### 9.3 FormalizerAgent

目的：将已接受的证明路线转化为 Lean。

输入：

- 已审阅证明路线；
- 精确定理 statement；
- Lean workspace；
- 现有本地库；
- 允许编辑范围。

输出：

- 已验证 Lean 声明；
- 更新后的 proof gap notes；
- build report；
- 候选可提升声明列表。

FormalizerAgent 只能写入它被分配的 workspace。

### 9.4 EvaluatorAgent

目的：独立评估。

EvaluatorAgent 不应该共享 ProofAgent 的私有工作上下文。它只能读取持久 artifact：

- 证明草稿；
- Lean 文件；
- build reports；
- claim ledger；
- failed route ledger；
- run summaries。

输出：

- 难度分数；
- 证明置信度；
- 形式化置信度；
- 建议：`promote`、`continue`、`park`、`freeze`、`source_recover`、`counterexample_review`；
- 具体理由。

### 9.5 CounterexampleAgent

目的：压力测试 claims 和证明路线。

输入：

- 目标 claim；
- 假设；
- 模型定义；
- 已知边界情形。

输出：

- 反例候选；
- 如果可能，给出形式化反例；
- 修正 statement 或路线的建议。

当出现以下情况时，应自动调用该 agent：

- 证明路线依赖强组合不等式；
- Lean attack 报告 `counterexample_suspected`；
- evaluator 标记建模不匹配。

### 9.6 LibrarianAgent

目的：提升可复用的已验证 Lean 资产。

输入：

- 已验证 Lean 声明；
- provenance metadata；
- 项目源路径；
- 候选模块。

输出：

- 更新 `amra_library/formal/AmraLibrary/...`；
- 更新 `amra_library/registry.json`；
- build report；
- 供未来项目使用的 import hints。

只有在无 `sorry`、`axiom`、`admit`、`opaque` 或 placeholder constant 的情况下能 build 的声明，才应该被提升。

### 9.7 Coordinator

目的：在题目组合中调度工作。

职责：

- 维护队列；
- 分配预算；
- 避免重复工作；
- 强制执行写锁；
- 每次 run 后触发评估；
- 停放低价值目标；
- 对高价值目标启动 focused attack；
- 触发 library harvesting。

## 11. 多 Agent 执行模型

### 10.1 并行性

安全的并行工作：

- 多个 ScoutAgent 处理不同题目；
- 多个 EvaluatorAgent 以 read-only 模式运行；
- ProofAgent 和 CounterexampleAgent 在复制出的 artifacts 上工作；
- FormalizerAgent 在不同 Lean workspaces 中运行。

不安全的并行工作：

- 两个 writer 同时编辑同一个 Lean 文件；
- 两个 LibrarianAgent 同时修改同一个库模块；
- 一个 agent 重写项目状态，同时另一个 agent 更新生命周期状态。

### 10.2 锁

使用简单 lock 文件：

```text
projects/<problem-id>/.locks/
  state.lock
  formal.lock
  library-promotion.lock
```

Lock 记录应该包含：

- owner agent；
- 如果是本地进程，则记录 PID；
- started_at；
- intended action；
- timeout。

### 10.3 Workspace 隔离

长时间形式化尝试应该运行在隔离 workspace：

```text
projects/<problem-id>/workspaces/<run-id>/formal/
```

只有成功且经过审阅的变更，才应该合并回 canonical `formal/` workspace。

## 12. Scheduler 策略

### 11.1 外层循环

一次 portfolio round：

1. 加载候选 problem bank。
2. 检索全局 memory 命中。
3. 运行短 scouting probes。
4. 运行独立 evaluation。
5. 按预期产出收益排序题目。
6. 提升 top targets。
7. 分配有界证明/形式化工作。
8. 审阅输出。
9. 更新 ledgers 和全局 indexes。
10. 收获已验证可复用引理。
11. 停放或冻结低收益目标。

### 11.2 排名公式

初始排名可以使用：

```text
priority =
  3.0 * feasibility_score
  + 2.0 * formalization_score
  + 1.5 * reusable_asset_score
  + 1.0 * source_quality_score
  - 2.0 * risk_score
  - 1.0 * estimated_hours_to_result
  - 1.5 * repeated_failure_count
```

具体权重应该可配置。

### 11.3 预算类别

默认预算：

- `scout`：5 到 20 分钟。
- `micro_attack`：20 到 45 分钟。
- `focused_attack`：1 到 4 小时。
- `deep_attack`：需要显式提升和 evaluator confidence。

题目获得 `deep_attack` 之前必须满足：

- statement 精确；
- 至少有一条可信证明路线或已知定理；
- 独立 evaluator 分数超过阈值；
- 没有 unresolved strong counterexample candidate。

## 13. Review Gates

结果只有通过对应级别的 gate 后才算完成。

### 12.1 自然语言证明 Gate

必须包含：

- 精确 statement；
- assumptions；
- 引理依赖链；
- 没有未解释的关键“显然”步骤；
- stress-test notes；
- evaluator verdict。

### 12.2 Lean 形式化 Gate

必须包含：

- `lake build` 成功；
- 没有 `sorry`、`admit`、`axiom`、`opaque` 或 placeholder constants；
- theorem statement 匹配目标问题；
- review 确认没有弱化或错误建模目标；
- build report 已保存。

### 12.3 Library Promotion Gate

必须包含：

- 可复用声明名称；
- 源项目和文件；
- provenance note；
- `amra_library` build 成功；
- registry entry。

## 14. 检索与复用

在任何新的严肃尝试之前，agent 应该检索：

- 相似题目 statements；
- tag 重叠的历史失败路线；
- 来自 `amra_library` 的已验证 Lean declarations；
- claim indexes 中的部分引理；
- 已知 source/literature records。

Prompt 应该显式包含：

- “除非能处理 failure Y，否则不要重复 failed route X”；
- “优先使用 library declaration Z”；
- “当前精确 blocker 是 B”。

## 15. CLI 设计

建议新增命令：

```bash
python3 -m amra run-portfolio-campaign \
  --bank data/banks/imo_2025.yaml \
  --run-name imo-2025-portfolio-round-1 \
  --scout-limit 6 \
  --scout-timeout 600 \
  --promote-top 2 \
  --attack-budget 14400
```

```bash
python3 -m amra evaluate-problem \
  --project projects/imo-2025-p6-formal-20260516 \
  --run-name p6-independent-evaluation
```

```bash
python3 -m amra harvest-library-candidates \
  --project projects/imo-2025-p1 \
  --module AmraLibrary.Olympiad.IMO2025.P1
```

```bash
python3 -m amra summarize-portfolio-memory \
  --campaign artifacts/portfolio_campaigns/imo-2025-portfolio-round-1
```

## 16. 实现计划

### Phase 1：Portfolio Data Layer

新增：

- `src/amra/portfolio_campaign.py`
- `src/amra/portfolio_memory.py`
- `tests/test_portfolio_campaign.py`
- `tests/test_portfolio_memory.py`

实现：

- campaign 目录创建；
- problem state schema；
- claim ledger load/save/upsert；
- route ledger load/save/upsert；
- failed route load/save/upsert；
- global memory index update。

验收标准：

- 可以在一个小型 fake bank 上创建 portfolio campaign；
- 写出稳定 JSON artifacts；
- 可以 resume 且不会覆盖历史 entries。

### Phase 2：Broad Scouting Integration

扩展 `MathScoutRunner`，或在 `PortfolioCampaignRunner` 中包装它。

实现：

- 每题短 probe；
- 结构化解析；
- ranking report；
- promotion 和 parked queues。

验收标准：

- 给定 3 个测试题目，系统能排序并输出 promotion queue；
- failed 或 timed-out scout runs 仍然产生有效 artifacts。

### Phase 3：Independent Evaluation

新增 `EvaluatorAgentRunner`。

实现：

- read-only evaluation prompt；
- 标准化 difficulty output；
- risk flags；
- promote/park/freeze recommendation。

验收标准：

- evaluator 可以把 counterexample-suspected route 标记为 `freeze` 或 `counterexample_review`；
- evaluator 可以提升 easy known theorem target。

### Phase 4：Attack Scheduling

将 promoted targets 连接到：

- `AIProofLabRunner`；
- `LeanFormalizerRunner`；
- `FocusedLeanAttackRunner`；
- pure Codex proof loops。

实现：

- budget assignment；
- write locks；
- isolated workspaces；
- progress velocity metrics。

验收标准：

- 只有 promoted problems 获得 focused attack budget；
- 两个 formalizer workers 不能同时写同一个 canonical Lean workspace。

### Phase 5：Memory Consolidation

实现自动更新：

- 从 proof outputs 更新 claim ledger；
- 从 blockers 更新 failed route ledger；
- 从项目本地 memory 更新 global memory index；
- resume pack generation。

验收标准：

- 某次 run 的 failed route 会出现在下一次 prompt 中，作为应避免路线；
- verified declaration 会出现在未来 retrieval results 中。

### Phase 6：Library Harvesting

扩展 `AmraLibraryManager` workflow。

实现：

- 从已验证项目 declarations 中检测 candidate；
- provenance block；
- registry update；
- library build；
- import hint generation。

验收标准：

- 已验证声明可以被提升到 `amra_library`；
- 未来项目 prompt 包含相关 library inventory。

### Phase 7：Dashboard And Reports

新增 portfolio summary reports：

- active queue；
- promoted targets；
- parked targets；
- completed proofs；
- library assets added；
- highest-value blockers；
- repeated failure clusters。

验收标准：

- 一个命令产生 `final_report.md`；
- 用户可以看到每个题目为什么被提升、停放或冻结。

## 17. 测试策略

单元测试：

- state transitions；
- claim ledger merge；
- failed route deduplication；
- ranking formula；
- lock behavior；
- evaluator parser；
- library candidate detection。

集成测试：

- fake bank 包含 easy、medium、impossible targets；
- portfolio scout -> evaluate -> promote -> focused run；
- counterexample-suspected route 会被停放；
- verified lemma 会被收获到 library。

回归测试：

- P6 式 false main lemma 在 failed route 被记录后，不应该被反复攻击。
- 如果 P1 式 easier target 的 expected time to verified result 更低，它应该排在 P6 前面。

## 18. P6 经验应用

P6 side-filter multiplicity 事件应该成为标准 failed-route 示例。

记录：

- target claim：`sidePairFilterMultiplicityLowerBound2025`；
- status：`counterexample_suspected`；
- suspected model：identity diagonal uncovered set；
- consequence：不修正不等式之前，不继续这条精确路线；
- next allowed actions：
  - 形式化该反例；
  - 弱化或修正 side-filter bound；
  - 切换到不同计数路线。

除非新路线显式处理已记录 failure，否则 scheduler 不应该再次给这个精确引理分配长时间 focused proof budget。

## 19. 成功指标

Portfolio system 应根据以下指标评估：

- 每计算小时产生的已验证 Lean declarations 数量；
- 完成的问题级证明数量；
- 收获的可复用 library declarations 数量；
- 重复 failed-route attempts 的减少；
- 从 scouting 到 promotion decision 的平均时间；
- evaluator 对 easy vs hard targets 的判断准确性；
- 拥有完整 durable artifacts 的 runs 比例。

## 20. 开放设计问题

- 自然语言证明和 Lean 形式化应该是一个统一 agent loop，还是两个阶段性 loop 但共享工具？
- 自动 library promotion 应该多激进？
- 当 library 增长后，是否应该周期性重新评分 parked problems？
- 需要什么最低证据，才可以把一条路线 freeze 为 false，而不是仅仅 blocked？
- 在计算资源有限时，portfolio ranking 应该偏向 easy wins，还是偏向高价值可复用引理？

当前默认答案：

- active attack 使用统一 proof/formalization agents；
- evaluator 保持独立且 read-only；
- 只收获 Lean-verified declarations；
- library 有重大增长后重新评分 parked problems；
- 首先优化 verified outputs 和 reusable assets。
