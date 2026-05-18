# ARA / AMRA / Blockchain-Security 仓库关系架构设计

日期：2026-05-18

状态：草案

## 1. 背景

当前本地有三个相互有关、但目标并不相同的研究型智能体项目：

- `ara`：通用自动科研流水线，偏论文生产、实验编排、报告生成和审稿返修。
- `amra`：数学研究智能体分支，重构后命名为 `AMRA`，目标是数学问题筛选、自然语言证明、Lean 形式化、证明库沉淀和多题目组合攻关。
- `abra`：区块链安全研究实验室，包含 Solidity 静态分析、DeFi 事件数据、Foundry replay、审计报告和论文材料。

三个仓库都属于“研究自动化”的大方向，但它们面对的对象、验证标准和失败形态不同。如果直接合并，会让通用科研流水线、数学证明系统和区块链安全实验互相污染；如果完全割裂，又会重复实现 LLM 调用、命令执行、artifact 管理、运行状态记录等基础能力。

本设计的核心目标是：仓库保持职责独立，通过稳定的 artifact / command / evidence 契约协作；只有足够通用且稳定的基础设施，才抽取为共享核心库。

## 2. 当前仓库观察

### 2.1 `ara`

该仓库已经形成通用科研流水线：

- 主流程是 `ideation -> planning -> experiment -> analysis_report -> writing -> revision`。
- `ara/orchestrator.py` 负责阶段编排。
- `ara/agents/experiment.py` 已经支持外部仓库命令执行、命令 allowlist、artifact 复制和实验结果记录。
- `ara/domain_context.py` 已经存在 `blockchain_security` 领域配置，并默认把兄弟目录 `abra` 当作外部实验仓库。
- `config.blockchain_*.yaml` 中已经配置了区块链实验命令前缀、artifact globs 和安全限制。

结论：`ara` 已经适合作为“论文和科研流程层”。它不应该直接吸收数学证明器或区块链分析器的内部代码，而应该调用外部实验室并消费其结果。

### 2.2 `amra` / `AMRA`

该仓库定位为数学研究智能体：

- README 中已经说明它有意和 ML 导向的 `ara` 分离。
- 现有模块覆盖 workspace、runtime、artifact graph、workstream、uncertainty、review gate、Lean 执行、proof search、goal campaign、focused attack、pure agents 等能力。
- 重构 spec 已经确定后续统一命名为 `AMRA`，仓库名、Python 包名、CLI、Lean 库前缀都要从 `amra` / `ara_math` 全量迁移。
- AMRA 的核心不是“写论文”，而是证明问题、筛题、沉淀引理库、维护 Lean build 可验证状态和管理长期证明记忆。

结论：AMRA 应该是独立的数学攻关系统。它可以把已验证或部分验证的数学结果打包交给 ARA 写论文，但不应该被 ARA 的六阶段论文流水线约束。

### 2.3 `abra`

该仓库是领域实验室：

- `tools/scanner.py` 和 `tools/analyzers/*.py` 提供 Solidity 静态分析。
- `tools/pipeline/*.py` 提供事件收集、标准化、数据质量报告、候选 incident 选择。
- `tools/replay_runner.py` 和 `test/replay/*.t.sol` 提供 Foundry replay 证据。
- `reports/`、`findings/`、`paper/` 中保存领域报告、论文草稿、replay 结果和审计材料。
- 当前不是标准 Python package，工具更像领域仓库内部命令集合。

结论：`abra` 应该继续作为独立领域实验室存在。它提供可运行命令、数据、报告和证据，不应反向依赖 ARA 或 AMRA。

## 3. 总体决策

### 3.1 三个仓库不合并

推荐保留三个仓库：

- `ara`：通用科研流程和论文生产系统。
- `amra`：数学研究、证明搜索、Lean 形式化和数学证明资产库。
- `abra`：区块链安全领域实验室。

理由：

- 三者的验证标准不同。ARA 的终点是论文质量和实验可复现；AMRA 的终点是数学证明和 Lean 验证；区块链安全的终点是静态分析、链上证据、fork replay 或审计证据。
- 三者的运行风险不同。区块链 replay 需要 RPC、Foundry 和安全命令限制；AMRA 需要 Lean build、证明状态和数学库演化；ARA 需要论文 artifact 校验和审稿循环。
- 三者的失败信号不同。AMRA 的“失败”可能是定理方向错误或引理不可证；区块链实验的“失败”可能是缺 archive RPC 或 replay 环境不可复现；ARA 的“失败”可能是 PDF、图表、论文分数或审稿返修不达标。

### 3.2 集成方式使用契约，而不是内部 import

仓库之间的默认关系应是：

- ARA 可以通过配置调用 `abra` 的允许命令，并复制 artifact。
- ARA 可以消费 AMRA 导出的证明结果包，用于写论文、综述、报告或实验论文。
- AMRA 不 import ARA 的论文流水线。
- `abra` 不 import ARA 或 AMRA。
- AMRA 和 `abra` 之间默认没有直接依赖；如果未来需要数学形式化安全证明，也应通过独立结果包交互。

即：通过文件、命令、manifest 和结果包集成，不通过跨仓库内部模块调用集成。

## 4. 推荐分层

### 4.1 ARA：科研流程层

ARA 应保留和强化这些职责：

- 研究 idea 生成和筛选。
- 实验计划生成。
- 外部实验室命令调用。
- 实验 artifact 收集。
- 分析报告生成。
- LaTeX / Markdown 论文写作。
- 审稿、返修、目标分数循环。
- 论文级可复现性检查。

ARA 不应负责：

- 直接实现 Lean 证明搜索。
- 直接维护数学引理库。
- 直接实现 Solidity analyzer。
- 直接判断区块链漏洞是否真实可利用，除非 evidence bundle 明确提供证据级别。

### 4.2 AMRA：数学证明层

AMRA 应保留和强化这些职责：

- 数学题库和定理库管理。
- 多题目 portfolio scouting。
- 难度评估、可攻关性评估和资源分配。
- 自然语言证明探索。
- Lean 形式化探索。
- 自然语言和 Lean 交替验证的 proof agent loop。
- focused attack 模块。
- theorem ledger、lemma ledger、proof attempt ledger。
- 已验证 Lean 定理打包为可复用数学库。
- 对未完成证明保存 blocker、失败路线、反例嫌疑和中间引理。

AMRA 不应负责：

- 通用论文 pipeline。
- 区块链安全数据采集。
- 非数学领域实验的通用编排。

### 4.3 Blockchain-Security：领域实验室层

`abra` 应保留和强化这些职责：

- Solidity 静态分析。
- DeFi incident 数据管线。
- Foundry fork replay。
- 审计发现和 evidence 分级。
- 报告、表格、事件卡片和论文素材。
- 领域内工具的测试和复现脚本。

`abra` 不应负责：

- 通用科研论文 agent。
- 数学证明 agent。
- 全局任务调度器。

## 5. 可选共享核心库

短期不建议立即抽取共享库。先让三个仓库通过 manifest 和 artifact contract 稳定协作。

当以下能力在至少两个仓库中反复稳定出现后，可以创建一个轻量共享库，例如 `research-agent-core`：

- LLM client / model adapter。
- 受限命令执行器和资源预算。
- workspace、artifact、event log 的基础读写。
- JSON schema 校验。
- 外部实验室 command adapter。
- 简单任务队列和运行状态记录。
- review result / score result / evidence result 的通用 schema。

共享库必须保持薄层，不应该包含数学逻辑、论文逻辑或区块链逻辑。

建议边界：

```text
research-agent-core
  - llm adapters
  - guarded command runner
  - workspace and artifact manifest helpers
  - event log schema
  - result bundle schema
  - scheduler primitives

ara
  - research pipeline
  - paper writing
  - revision loop
  - external lab orchestration

amra
  - proof agents
  - theorem ledgers
  - Lean integration
  - mathematical library

abra
  - Solidity analyzers
  - incident data
  - Foundry replay
  - security reports
```

## 6. 交互契约

### 6.1 领域实验室 manifest

每个可被 ARA 调用的领域实验室应在仓库根目录提供 `research_lab.yaml`。

示例：

```yaml
lab_id: abra
name: Blockchain Security Research Lab
version: 0.1

commands:
  allow_prefixes:
    - python3 tools/
    - python3 scanner.py
    - python3 tools/scanner.py
    - forge test --match-path test/replay/
    - forge test --match-contract
  deny_patterns:
    - rm -rf
    - git reset --hard
    - cast send
    - --broadcast
    - PRIVATE_KEY

environment:
  optional:
    - ETH_RPC_URL
    - ARCHIVE_RPC_URL

artifacts:
  include:
    - data/processed/*.csv
    - reports/*.md
    - reports/events/*.md
    - reports/replay_runs/*.json
    - findings/*.md
    - figures/generated/*

evidence_levels:
  static_alert: "Static analyzer finding only"
  reproduced_test: "Local deterministic test reproduced"
  fork_replay: "Fork replay reproduced with RPC metadata"
  manual_audit: "Human-reviewed audit finding"
```

ARA 读取该 manifest 后，只需要知道哪些命令可执行、哪些 artifact 应收集、每个结果的 evidence level 是什么。ARA 不需要了解 analyzer 或 replay 的内部实现。

### 6.2 实验 artifact manifest

每次领域实验运行后，应产生 `artifact_manifest.json`。

示例：

```json
{
  "run_id": "blockchain-replay-20260518-001",
  "lab_id": "abra",
  "command": "forge test --match-path test/replay/EulerFinanceReplay.t.sol",
  "status": "completed",
  "started_at": "2026-05-18T10:00:00+08:00",
  "finished_at": "2026-05-18T10:25:00+08:00",
  "artifacts": [
    {
      "path": "reports/replay_runs/euler_finance_20260518.json",
      "kind": "replay_report",
      "evidence_level": "fork_replay"
    }
  ],
  "limitations": [
    "Result depends on configured archive RPC endpoint."
  ]
}
```

### 6.3 AMRA 证明结果包

AMRA 不应把内部 workspace 直接暴露给 ARA。它应导出一个结果包，例如：

```text
amra_result_bundle/
  theorem_statement.md
  problem_metadata.json
  proof_summary.md
  proof_attempt_ledger.jsonl
  lean/
    lakefile.lean
    AmraLibrary/...
  lean_build_report.json
  verified_declarations.json
  unresolved_blockers.md
  artifact_manifest.json
  writing_brief.md
```

其中：

- `theorem_statement.md` 写清原始命题和形式化命题。
- `proof_summary.md` 写自然语言证明。
- `lean_build_report.json` 记录 Lean build 是否通过。
- `verified_declarations.json` 列出已验证定理、引理、依赖和声明名。
- `unresolved_blockers.md` 记录尚未完成或不 faithful 的部分。
- `writing_brief.md` 给 ARA 使用，说明该结果能写什么论文、哪些说法不能写。

ARA 消费该 bundle 时，只能把 `verified_declarations.json` 中的内容称为形式化验证；不能把自然语言 proof sketch 误写成 Lean 已验证结果。

## 7. 记忆与中间产物保存

三个仓库都需要长期记忆，但记忆类型不同。

### 7.1 ARA 记忆

ARA 的长期记忆应围绕论文项目：

- idea 来源。
- planning 决策。
- experiment 配置。
- result tables。
- paper drafts。
- reviews。
- revision history。
- final PDF 和失败原因。

建议保留在 `projects/<project-id>/` 中，并通过 `pipeline_results.json` 和 stage artifacts 统一索引。

### 7.2 AMRA 记忆

AMRA 的长期记忆应围绕数学对象：

- problem ledger。
- theorem ledger。
- lemma ledger。
- proof attempt ledger。
- failed route ledger。
- counterexample suspicion ledger。
- Lean declaration index。
- tactic failure patterns。
- reusable library packaging records。

这类记忆不应只按一次运行保存，而应能跨题目、跨 campaign 被检索和复用。

建议 AMRA 维护：

```text
memory/
  problems/
  theorems/
  lemmas/
  attempts/
  blockers/
  counterexamples/
  lean_declarations/
  evaluations/
```

### 7.3 Blockchain-Security 记忆

区块链安全仓库的长期记忆应围绕事件、协议、合约和证据：

- incident cards。
- protocol audit reports。
- static analyzer alerts。
- replay run metadata。
- RPC limitations。
- exploit reproduction status。
- manually reviewed findings。

建议将每条安全结论都绑定 evidence level，避免把静态告警误认为真实漏洞。

## 8. 多 Agent 协作设计

三个仓库的 agent 也应分工，而不是使用一个全能 agent。

### 8.1 ARA Agent

推荐角色：

- Ideation Agent。
- Planning Agent。
- Experiment Orchestrator。
- Analysis Report Agent。
- Writing Agent。
- Reviewer Agent。
- Revision Agent。

ARA 的 evaluator 主要评估论文质量、实验充分性、表格图形完整性和审稿分数。

### 8.2 AMRA Agent

推荐角色：

- Problem Scout：广泛扫描题库，估计难度和潜力。
- Proof Search Agent：自然语言和 Lean 混合探索。
- Focused Attack Agent：针对关键 lemma / blocker 定点攻关。
- Lean Formalization Agent：把证明对象稳定转化为 Lean 声明和构造。
- Proof Critic：独立评估证明是否有缺口。
- Difficulty Evaluator：独立估计继续投入是否值得。
- Library Curator：把完成引理和定理打包进 AMRA library。

证明器和评估器应该分离。证明器倾向于推进路线，评估器倾向于质疑路线、识别 blocker、估计机会成本，二者共享 artifact 但不共享即时思维上下文。

### 8.3 Blockchain-Security Agent

推荐角色：

- Static Analysis Agent。
- Incident Data Agent。
- Replay Agent。
- Evidence Reviewer。
- Report Agent。

区块链安全的 reviewer 应重点区分：

- 静态告警。
- 可复现单元测试。
- fork replay。
- 真实链上攻击证据。
- 需要人工确认的审计判断。

## 9. 典型协作流程

### 9.1 ARA 调用 Blockchain-Security

```text
ARA planning
  -> 读取 abra/research_lab.yaml
  -> 选择允许命令
  -> 在 abra 中执行实验
  -> 收集 artifact_manifest.json 和报告文件
  -> 生成 analysis_report
  -> 写论文和返修
```

ARA 可以负责编排和写作，但 evidence 的语义由 `abra` 的 manifest 和结果报告提供。

### 9.2 AMRA 导出数学结果给 ARA

```text
AMRA proof campaign
  -> 完成自然语言证明或 Lean 证明
  -> 生成 amra_result_bundle
  -> ARA 消费 writing_brief.md
  -> ARA 写数学实验论文、系统论文或证明发现报告
```

ARA 可以写“AMRA 如何发现证明”或“AMRA 的证明搜索实验”，但不能替代 AMRA 判断定理是否已经 Lean verified。

### 9.3 AMRA 内部组合攻关

```text
AMRA problem scout
  -> 对题目集合做初筛
  -> difficulty evaluator 排序
  -> 低难度题优先 proof search
  -> blocker 进入 focused attack
  -> 完成结果进入 library curator
  -> 太难题保留失败记忆，暂时放弃
```

该流程应服务于“尽快产出真实证明成果”，而不是把资源无限投入单个高难题。

## 10. 迁移计划

### 阶段 1：稳定契约

- 为 `abra` 添加 `research_lab.yaml`。
- 为 AMRA 定义 `amra_result_bundle` schema。
- 在 ARA 中把外部实验室读取从散落 config 逐步迁移到 manifest 驱动。
- 明确 evidence level 和 artifact manifest 规范。

### 阶段 2：AMRA 全量改名

- 仓库名从 `amra` 改为 `amra`。
- Python 包从 `ara_math` 改为 `amra`。
- CLI 从 `amra` 改为 `amra`。
- Lean library 从 `AraLibrary` / `ara_library` 改为 `AmraLibrary` / `amra_library`。
- 文档、测试、工作区路径、artifact schema 同步迁移。

### 阶段 3：抽取共享核心

只有当 manifest 和 bundle 已稳定后，才考虑抽取 `research-agent-core`。

优先抽取：

- guarded command runner。
- workspace event log。
- artifact manifest helper。
- LLM adapter。
- result schema validator。

不要抽取：

- ARA pipeline stages。
- AMRA proof agents。
- Solidity analyzers。
- Lean tactic / theorem-specific code。

### 阶段 4：统一 dashboard 或索引

可以在未来增加一个轻量 dashboard，跨仓库读取：

- ARA 论文项目状态。
- AMRA 题目和定理状态。
- Blockchain-security replay / audit 状态。

dashboard 只读 artifact 和 manifest，不直接操纵各仓库内部状态。

## 11. 风险与约束

### 11.1 过早抽象风险

如果现在就把三个仓库合并或抽取大框架，容易形成臃肿系统。数学证明、区块链安全和论文写作差异很大，共享层必须很薄。

### 11.2 证据语义混淆风险

ARA 写论文时必须区分：

- 静态分析发现。
- 实验复现。
- Lean verified theorem。
- 自然语言证明。
- agent 评估意见。

不同证据不能互相替代。

### 11.3 命名迁移风险

AMRA 全量改名会影响包名、CLI、Lean module、路径、测试、历史 artifact。迁移时应保留兼容 shim 或至少提供迁移脚本，避免旧 workspace 全部失效。

### 11.4 长期记忆污染风险

AMRA 的证明记忆应记录失败路线和 blocker，但不能把未验证 lemma 当成可复用事实。Blockchain-security 的静态告警也不能默认进入高置信 findings。

## 12. 推荐近期任务

1. 在 `abra` 根目录添加 `research_lab.yaml`。
2. 在 AMRA spec 中补充 `amra_result_bundle` schema，或单独新增 schema 文档。
3. 在 ARA 的外部实验模块中增加读取 `research_lab.yaml` 的能力，保留现有 config 作为 override。
4. 为 AMRA 改名做一次独立迁移 PR，不和 proof-agent 重构混在一起。
5. 为 AMRA 添加 proof attempt ledger、difficulty evaluator 和 library curator 的最小实现。
6. 为三个仓库定义统一的 `artifact_manifest.json` 字段子集。
7. 暂缓抽取 `research-agent-core`，等至少两条跨仓库流程稳定跑通后再做。

## 13. 最终建议

最佳架构不是把 `ara`、`AMRA` 和 `abra` 做成一个大仓库，而是形成“三层松耦合研究系统”：

- ARA 负责科研流程和论文生产。
- AMRA 负责数学证明和形式化验证。
- Blockchain-Security 负责区块链安全领域实验和证据。

三者通过 manifest、artifact bundle、evidence schema 和受限命令执行协作。共享核心库可以存在，但必须后置、薄层、基础设施化。这样既能复用 agent 工程能力，又不会牺牲各领域系统自己的验证标准和长期演化空间。
