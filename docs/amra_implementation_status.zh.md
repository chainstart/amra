# AMRA Spec 实现状态矩阵

日期：2026-05-19

状态：动态维护中

主 spec：

- `docs/portfolio_campaign_spec.md`
- `docs/portfolio_campaign_spec.zh.md`
- `docs/repository_relationships_architecture.zh.md`

机器台账：`.engineering/spec_tasks.yaml`

决策记录：`docs/decisions/`

## Requirement 状态

| Requirement ID | 状态 | 当前证据 | 主要缺口 | 下一步 |
| --- | --- | --- | --- | --- |
| `REQ-AMRA-GOV-001` | `completed` | 本文档、`.engineering/spec_tasks.yaml`、决策记录 | 需要随每轮证明系统开发持续更新 | 接入 harness spec-sync |
| `REQ-AMRA-NAMING-001` | `partial` | canonical `amra` package、legacy shim、接口测试 | `src/ara_math` cleanup 尚未全部完成 | 继续按 disposition 文档迁移 |
| `REQ-AMRA-MANIFEST-001` | `completed` | `research_lab.yaml`、AMRA CLI、ARA-facing contract | 随 ARA bundle contract 演进 | 保持 manifest smoke |
| `REQ-AMRA-PORTFOLIO-001` | `partial` | portfolio campaign spec、portfolio scaffold、scheduler/memory 模块 | 难度评估和多题目资源调度还需增强 | 完成 portfolio campaign 后续任务 |
| `REQ-AMRA-PROOF-001` | `partial` | pure/focused proof agents、problem banks、proof attempt 记录 | 纯证明能力不稳定，难题容易长时间拉扯 | 加强 scouting、abandon policy、resume pack |
| `REQ-AMRA-LEAN-001` | `partial` | Lean executor/audit/contract、形式化产物 | 自然语言证明到 Lean faithful modeling 缺口仍大 | 强化 NL/Lean 交替 proof loop |
| `REQ-AMRA-LIBRARY-001` | `partial` | AMRA library manager、library harvesting 计划 | verified lemma 打包和复用策略不足 | 增加 library curator gate |
| `REQ-AMRA-ARA-001` | `partial` | AMRA result bundle 方向、ARA lab integration | 需要跨仓库消费 smoke | 输出更稳定的 proof/result bundle |

## 维护流程

1. 开发前在 `.engineering/spec_tasks.yaml` 中确认任务和 requirement ID。
2. 开发后记录测试命令、Lean build 报告、result bundle、proof attempt ledger 或 blocker。
3. 如果发现 theorem statement、Lean modeling 或 proof route 改变，必须写入决策记录或 proof ledger。
4. 未验证 lemma 不能进入 reusable library，只能作为 candidate 或 blocker 证据。
