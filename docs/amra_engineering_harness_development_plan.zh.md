# AMRA Engineering Harness Development Plan

日期：2026-05-18

状态：供 engineering harness 执行

## 1. 当前基线

AMRA 已完成第一步框架重构：

- 新增 canonical Python package：`amra`。
- 新增 canonical CLI：`python3 -m amra` 和 console script `amra`。
- 保留 legacy package / CLI：`ara_math`、`python3 -m ara_math`、`ara-math`。
- 仓库根目录提供薄 shim，让未安装 checkout 也能直接运行 `python3 -m amra` 和 `python3 -m ara_math`；真实实现仍在 `src/amra` 和 `src/ara_math`。
- 新增 portfolio scaffold：
  - `amra.portfolio_campaign`
  - `amra.portfolio_memory`
- 新增 AMRA portfolio CLI：
  - `run-portfolio-campaign`
  - `evaluate-problem`
  - `harvest-library-candidates`
  - `summarize-portfolio-memory`
- 更新 `research_lab.yaml`，让上层 ARA 系统优先识别 AMRA canonical interface，并保留 legacy entrypoints。

本阶段不做一次性物理大改名。`src/ara_math` 仍保留为兼容实现层，后续阶段逐步把新实现迁移到 `src/amra`。

## 2. 执行原则

- AMRA 是数学证明系统，不 import ARA 的论文流水线。
- ARA 只通过 `research_lab.yaml`、受限命令、artifact manifest 和 `amra_result_bundle` 消费 AMRA 结果。
- AMRA 内部状态以数学对象为中心：problem、claim、route、failed route、Lean declaration、library asset。
- 所有 long-running proof/formalization 工作都必须写入 durable run directory。
- 不允许多个 worker 同时写同一个 canonical Lean workspace 或同一个 library module。
- Lean verified 声明和自然语言 proof sketch 必须严格区分。

## 2.1 Legacy 模块处置原则

`src/ara_math` 目录不能简单整体删除或机械改名。后续开发必须先遵守
`docs/amra_legacy_module_disposition.zh.md` 中的文件级处置表：

- 基础设施模块先迁移 API，不改语义。
- 大聚合模块先拆分，再把 legacy 文件降级为 shim。
- 旧写作/论文导向模块只保留为 result bundle / writing brief 支撑。
- 删除旧文件只能在专门 cleanup 任务中执行，且必须保留 legacy CLI/import 兼容。

## 3. 任务包 0：Legacy Module Disposition

目标：把 `src/ara_math/*.py` 的模块级处置作为后续重构前置约束。

范围：

- `docs/amra_legacy_module_disposition.zh.md`
- `docs/amra_engineering_harness_development_plan.zh.md`
- `.engineering/roadmap.yaml`
- `tests/test_amra_interfaces.py`
- `src/ara_math/*.py`（只读枚举输入；本任务不修改、移动或删除 legacy 模块）

要求：

- 文档覆盖所有 `src/ara_math/*.py` 文件。
- 每个文件都有明确处置：keep-core、move、split、merge、deprecate、shim、delete-later。
- 本任务不删除旧文件。
- 后续任务必须引用该处置文档。

验收：

```bash
python3 - <<'PY'
from pathlib import Path
doc = Path('docs/amra_legacy_module_disposition.zh.md').read_text(encoding='utf-8')
missing = [p.name for p in sorted(Path('src/ara_math').glob('*.py')) if f'`{p.name}`' not in doc]
if missing:
    raise SystemExit(f'missing module disposition entries: {missing}')
print('covered', len(list(Path('src/ara_math').glob('*.py'))))
PY
```

并运行：

```bash
python3 -m pytest -q tests/test_amra_interfaces.py
```

## 4. 任务包 1：AMRA Rename Hardening

目标：把 canonical `amra` 接口稳定下来，同时不破坏 legacy workspace。

范围：

- `src/amra/**`
- `src/ara_math/__init__.py`
- `src/ara_math/cli.py`
- `pyproject.toml`
- `research_lab.yaml`
- `tests/test_amra_interfaces.py`
- docs

要求：

- `python3 -m amra --help` 可用。
- `python3 -m amra list-problems --bank data/problem_bank.yaml --json` 可用。
- `python3 -m ara_math list-problems --bank data/problem_bank.yaml --json` 仍可用。
- 新文档和新测试使用 AMRA 命名。
- legacy alias（`python3 -m ara_math`、`ara-math`、`ara_math`）必须在 help 或 docs 中标记 deprecated。

验收：

```bash
python3 -m pytest -q tests/test_amra_interfaces.py tests/test_cli_flow.py
python3 -m amra --help >/tmp/amra_help.txt
python3 -m amra list-problems --bank data/problem_bank.yaml --json >/tmp/amra_problem_list.json
python3 -m ara_math list-problems --bank data/problem_bank.yaml --json >/tmp/ara_math_problem_list.json
```

## 5. 任务包 2：Portfolio Data Layer

目标：把 portfolio memory scaffold 扩展为完整可恢复数据层。

范围：

- `src/amra/portfolio_memory.py`
- `src/amra/portfolio_campaign.py`
- `tests/test_portfolio_memory.py`
- `tests/test_portfolio_campaign.py`

要求：

- problem lifecycle state transition append-only。
- claim ledger 支持 upsert、status 校验、依赖、证据和 reusable 标记。
- route ledger 支持 attempt history、blocker、evaluator verdict。
- failed route ledger 支持 dedup、failure mode、resume condition。
- global indexes 应 merge 多个 project，不覆盖历史条目。
- resume pack 生成稳定 Markdown。

验收：

```bash
python3 -m pytest -q tests/test_portfolio_memory.py tests/test_portfolio_campaign.py tests/test_amra_interfaces.py
```

## 6. 任务包 3：Broad Scouting Integration

目标：把 portfolio campaign 接入现有 `MathScoutRunner`，对多题目做短预算浅探。

范围：

- `src/amra/portfolio_campaign.py`
- `src/ara_math/math_scout.py`
- `src/ara_math/cli.py`
- `tests/test_portfolio_scouting.py`

要求：

- `run-portfolio-campaign` 可对 bank 中多个题目生成 per-problem probe artifacts。
- scout timeout/failure 也必须写有效 artifact。
- ranking 输入包含 exact statement、source quality、shallow proof signal、formalization signal。
- 不调用真实 LLM 的测试必须通过 fake runner。

验收：

```bash
python3 -m pytest -q tests/test_portfolio_scouting.py tests/test_math_scout.py
python3 -m amra run-portfolio-campaign --bank data/problem_bank.yaml --run-name harness-smoke --scout-limit 3 --promote-top 1 --scout-timeout 60 --json
```

## 7. 任务包 4：Independent Evaluator

目标：添加独立只读 evaluator，把 proof route / Lean artifact / failed route 转成 difficulty 和推荐动作。

范围：

- `src/amra/portfolio_evaluator.py`
- `src/amra/portfolio_campaign.py`
- `src/ara_math/cli.py`
- `tests/test_portfolio_evaluator.py`

要求：

- evaluator 不共享 proof agent 私有上下文，只读 durable artifacts。
- 输出 `amra.difficulty_evaluation.v1`。
- 能返回 `promote`、`continue`、`park`、`freeze`、`source_recover`、`counterexample_review`。
- counterexample-suspected route 默认不能继续长预算攻击。

验收：

```bash
python3 -m pytest -q tests/test_portfolio_evaluator.py tests/test_amra_interfaces.py
```

## 8. 任务包 4.5：Pure Agent Runner Migration

目标：把最近新增的 `pure_agents.py` 提升为 AMRA canonical proof agent runner，而不是放进普通 legacy cleanup。

范围：

- `src/ara_math/pure_agents.py`
- `src/ara_math/agent_tools.py`
- `src/ara_math/proof_state.py`
- `src/ara_math/focused_attack.py`
- `src/amra/agents/**`
- `tests/test_pure_agents.py`
- `tests/test_focused_attack.py`

要求：

- `pure_agents.py` 中的 Codex episode loop、natural-language theorem prover、Lean-from-proof agent、unified proof loop 必须保持现有行为。
- 新增 canonical AMRA 模块：
  - `amra.agents.episode_loop`
  - `amra.agents.tools`
  - `amra.agents.proof`
  - `amra.agents.lean`
  - `amra.proof.state`
- `ara_math.pure_agents`、`ara_math.agent_tools`、`ara_math.proof_state` 降级为 legacy shim 或兼容转发层。
- `FocusedLeanAttackAgent` 应优先从 AMRA canonical runner 导入，legacy import 继续可用。
- 每个 agent run 必须继续写 durable run directory、prompt、output、observations、report。
- 本任务不改变外部 Codex 调用语义，不删除 legacy 文件。

验收：

```bash
python3 -m pytest -q tests/test_pure_agents.py tests/test_focused_attack.py tests/test_amra_interfaces.py
python3 - <<'PY'
from amra.agents.proof import UnifiedProofAgentLoop
from amra.agents.lean import LeanFromNaturalProofAgent
from ara_math.pure_agents import UnifiedProofAgentLoop as LegacyUnifiedProofAgentLoop
assert UnifiedProofAgentLoop is LegacyUnifiedProofAgentLoop
assert LeanFromNaturalProofAgent is not None
PY
```

## 9. 任务包 5：Attack Scheduling And Locks

目标：将 promoted targets 接入 proof/formalizer/focused attack runner，并加入锁和隔离工作区。

范围：

- `src/amra/portfolio_scheduler.py`
- `src/amra/portfolio_campaign.py`
- `src/ara_math/campaign_loop.py`
- `src/ara_math/focused_attack.py`
- `src/ara_math/lean_formalizer.py`
- `tests/test_portfolio_scheduler.py`

要求：

- promoted problem 才能获得 focused attack budget。
- formalizer 写入 `projects/<problem-id>/workspaces/<run-id>/formal/`。
- 成功且 review 后才合并回 canonical formal workspace。
- `.locks/state.lock`、`.locks/formal.lock`、`.locks/library-promotion.lock` 包含 owner、PID、started_at、timeout。
- progress velocity 写入 run report。

实现约定：

- `amra.portfolio_scheduler` 负责 promotion queue 到 active assignment 的转换，只为 promotion queue 中的 problem 分配 focused attack budget。
- 每个 assignment 预留 canonical `projects/<problem-id>/formal/` 和 isolated `projects/<problem-id>/workspaces/<run-id>/formal/`，runner 可通过显式参数启用隔离工作区。
- canonical formal workspace 和 library promotion 只能在 run status 为 `verified` 且 review status 为 approved/pass/reviewed 后合并；合并期间持有 `formal.lock`，library module promotion 额外持有 `library-promotion.lock`。
- focused attack、Lean formalizer、campaign loop report 都包含 `amra.progress_velocity.v1` 指标。

验收：

```bash
python3 -m pytest -q tests/test_portfolio_scheduler.py tests/test_focused_attack.py tests/test_lean_formalizer.py
```

## 10. 任务包 6：Memory Consolidation

目标：自动从 proof outputs、Lean reports、review notes 更新 claim/route/failed-route ledger 和 global indexes。

范围：

- `src/amra/portfolio_memory.py`
- `src/amra/portfolio_campaign.py`
- `src/ara_math/proof_state.py`
- `tests/test_portfolio_memory_consolidation.py`

要求：

- failed route 出现在下一轮 prompt/resume pack。
- verified declaration 出现在 theorem asset index。
- global indexes 支持多 project merge。
- P6 side-filter multiplicity 作为 canonical failed-route regression fixture。

验收：

```bash
python3 -m pytest -q tests/test_portfolio_memory_consolidation.py tests/test_amra_interfaces.py
```

## 11. 任务包 7：AMRA Library Harvesting

目标：把 Lean verified declarations 安全提升到 AMRA library。

范围：

- `src/amra/amra_library.py`
- `src/amra/portfolio_campaign.py`
- `src/ara_math/ara_library.py`
- `src/ara_math/lean.py`
- `tests/test_amra_library.py`

要求：

- canonical 目录为 `amra_library`。
- canonical Lean module prefix 为 `AmraLibrary`。
- legacy `ara_library` / `AraLibrary` 通过 migration shim 支持。
- 不允许 `sorry`、`admit`、`axiom`、`opaque` 或 placeholder constants 被 harvest。
- registry 记录 provenance 和 import hints。

验收：

```bash
python3 -m pytest -q tests/test_amra_library.py tests/test_lean_executor.py
python3 -m amra init-amra-library --json
python3 -m amra build-amra-library --timeout 120 --json
```

## 12. 任务包 8：Dashboard And Result Bundle

目标：生成 portfolio report 和可供 ARA 消费的 `amra_result_bundle`。

范围：

- `src/amra/portfolio_reports.py`
- `src/amra/result_bundle.py`
- `src/ara_math/cli.py`
- `research_lab.yaml`
- `tests/test_amra_result_bundle.py`

要求：

- `final_report.md` 解释每个问题为什么 promoted/parked/frozen。
- `amra_result_bundle` 包含 theorem statement、proof summary、Lean build report、verified declarations、artifact manifest、writing brief、handoff notes。
- `artifact_manifest.json` 明确声明 verification boundaries、Lean status、ARA consume order 和文件 checksum。
- bundle 不能把 natural-language proof sketch 声称为 Lean verified。
- ARA 可通过 `research_lab.yaml` 发现 bundle schema。

验收：

```bash
python3 -m pytest -q tests/test_amra_result_bundle.py tests/test_amra_interfaces.py
```

## 13. 任务包 11：Known Problem Proof Smoke

目标：用 deterministic known-problem fixture 跑通 proof attempt ledger、Lean report、verified/blocked status 和
`amra_result_bundle` 导出，不依赖开放难题求解或长 LLM 调用。

范围：

- `src/amra/known_problem_smoke.py`
- `src/amra/result_bundle.py`
- `src/ara_math/cli.py`
- `tests/test_amra_known_problem_smoke.py`
- `tests/test_amra_result_bundle.py`

要求：

- `python3 -m amra run-known-problem-smoke --problem imo_2025_p1 --max-seconds 60 --out <dir> --json`
  必须在有 Lean toolchain 时输出 `verified`，缺 toolchain 或超时时输出结构化 `blocked`，但仍生成 bundle。
- bundle 包含 `proof_attempt_ledger.jsonl`、`lean_build_report.json`、`verified_declarations.json`、
  `natural_language_proof_sketches.json`、`unresolved_blockers.md`、`limitations.md`、`writing_brief.md`、
  `handoff_notes.md`、`artifact_manifest.json` 和 `known_problem_smoke_report.json`。
- proof attempt ledger 记录 `llm_calls=0` 和 `backend=deterministic_fixture`，证明该 smoke 不调用长 LLM。
- fixture 使用 `imo_2025_p1` 作为 harness key，但明确标注不是 official IMO 2025 P1 statement，避免 ARA 误写来源。

验收：

```bash
python3 -m amra run-known-problem-smoke --problem imo_2025_p1 --max-seconds 60 --out /tmp/amra_known_problem_bundle --json >/tmp/amra_known_problem_smoke.json
python3 -m pytest -q tests/test_amra_known_problem_smoke.py tests/test_amra_result_bundle.py
```

## 14. 后续抽象边界

暂不抽取 shared framework。只有在 ARA 与 AMRA 的 manifest/bundle/command 契约稳定后，才考虑提取薄层：

- guarded command runner；
- artifact manifest helper；
- workspace event log；
- LLM adapter；
- result schema validator。

不要抽取：

- ARA pipeline stages；
- AMRA proof agents；
- Lean theorem-specific logic。
