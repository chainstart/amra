# 决策：AMRA 使用动态 spec 维护体系

日期：2026-05-19

状态：接受

## 背景

AMRA 的工作包括证明路线探索、Lean 形式化、题目组合筛选、focused attack、library harvesting 和 ARA 集成。单一 roadmap 只能描述工程任务，不能完整表达证明状态、失败路线和可复用 lemma 的可信度。

## 决策

AMRA 采用动态 spec 维护体系：

- 主设计继续由 portfolio spec 和仓库关系文档承载。
- `.engineering/spec_tasks.yaml` 维护 requirement 和工程任务状态。
- `docs/amra_implementation_status.zh.md` 维护人工可读状态矩阵。
- `docs/decisions/` 保存架构级决策。
- `docs/spec_update_log.jsonl` 保存自动或人工追加的任务状态更新。

## 影响

- engineering-harness 开发 AMRA 任务后，必须能回写 spec task 状态。
- 数学证明的中间产物必须区分 `proof_sketch`、`lean_verified`、`blocked_attempt` 和 `counterexample_suspected`。
- 长期未完成的题目必须留下可复用的 blocker 和 resume 信息。
