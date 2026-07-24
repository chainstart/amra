# Erdős 630题轮换攻关总计划与总台账

> 台账版本：`erdos-portfolio-rotation-20260723-v1`；当前周期：`R004`；生成时间：`2026-07-24T03:26:24+00:00`。

## 总目标与口径

本计划覆盖冻结 cohort 的630题。当前快照中550题为 `open`；其余条目进入闭合证据维护、状态冲突核验或有限判定路线。开放题的主目标始终是精确原命题的证明或证否；论文级阶段结果、已有解声明核验和形式化工作分别记账，不与原题闭合混计。

630题 cohort 的批量状态快照生成于2026-07-19；每道题进入准入轮前必须重新核对官网、原论文和最新公开讨论。

初筛的 `feasibility_score` 只表示下一步可检验性。调度另设0至5级`closure_distance`：0为已闭合，1为一条明确闭合引理/证据核验，2为一个有限结构缺档，3为存在可命名桥梁，4为需要新的全局机制，5为路线被阻断或题面尚不稳定。

## 轮换制度

每个题目的生命周期为：状态刷新 → 60至90分钟准入 → 最多4小时深攻 → 独立QA → 晋级、论文转化、冷却或闭合。连续两个深攻周期未减少闭合距离的题进入3个周期冷却；只改善常数、扩大有限验证或增加条件定理不重置停滞计数。

晋级深攻必须同时满足：

- 精确重述原题量词并完成最新状态与文献核对
- 给出一条若成立即可闭合原题或明确子问的 closing lemma
- 不存在已知深层定理被当作黑箱缺口而未说明
- 路线与此前失败路线实质不同，或已修复其首个严格断点
- 有限计算必须服务于可证明的统一命题，不能单独作为晋级理由

轮换采用分层轮询而非单一总分排序：不同领域轮流获得准入槽；历史深挖题受到饱和惩罚；已有解声明进入 `resolution_audit`，不得占用原创证明槽。

## 规模与资源

- 同时研究槽上限：4；建议CPU占用不超过WSL资源的50%。
- 准入预算：每题90分钟；深攻预算：每题4小时；独立QA预算：每项60分钟。
- 全池覆盖规划：R001以强制队列中的2题做制度试运行；从R002起，每个宏周期准入12个此前未深挖的开放题，并用最多4个并行槽分三批执行，约46个宏周期可覆盖550题一次。

## 当前总体统计

- 总题数：630；状态分布：`disproved`=12、`disproved (Lean)`=8、`falsifiable`=2、`independent`=1、`open`=550、`proved`=12、`proved (Lean)`=22、`solved`=15、`solved (Lean)`=8。
- 任务通道：`closed_watch`=84、`closure_core`=4、`cooldown`=18、`deep_backlog`=268、`discovery_high`=36、`discovery_standard`=172、`finite_resolution`=2、`intake_active`=2、`paper_conversion`=2、`resolution_audit`=26、`resolution_ready`=1、`statement_audit`=15。
- 闭合距离：`0`=85、`1`=27、`2`=5、`3`=217、`4`=148、`5`=148。
- 当前追加事件流：73条、覆盖45题、登记12.00 agent-hours。
- 连同旧轮次，可直接核算的总投入下界为72.68 agent-hours；这里只累计首轮、第二轮及第6至12轮的可直接核算账本，尚未计第3至5轮，且不能精确均摊到单题。

## 当前周期 R004

### 原题闭合核心

| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |
|---:|---|---:|---:|---|---|
| [776](https://www.erdosproblems.com/776) | combinatorics | 1 | 4h | completed | 证明 W6<C(V-13,6) 的全参数界，或建立相邻参数 rank-8 loss potential。 |
| [809](https://www.erdosproblems.com/809) | graph_theory | 2 | 4h | completed | 把该引理接入完整 BCM Case1/Case2 归纳，首先闭合 near-two-clique 与低最小度接口。 |
| [592](https://www.erdosproblems.com/592) | ramsey_theory | 2 | 4h | completed | 重建有序 architect replay 引理并逐项保持 Definition 10.19/10.23 数据，或构造 solution-level pinning map。 |
| [635](https://www.erdosproblems.com/635) | number_theory | 2 | 4h | completed | 分析两个参数或非平行素数环如何进入同一分量，寻找非梯度冲突不变量或首个双环核。 |

### 新题准入

| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |
|---:|---|---:|---:|---|---|
| [313](https://www.erdosproblems.com/313) | number_theory | 3 | 1.5h | completed | 研究三素数及更高端口方程的可解族，或证明可应用的无条件筛/素数值定理。 |
| [749](https://www.erdosproblems.com/749) | combinatorics | 3 | 1.5h | completed | 建立两层有限模块的跨卷积下界或给出参数一致的可拼接构造。 |
| [811](https://www.erdosproblems.com/811) | graph_theory | 3 | 1.5h | completed | 从大特征向量提取近二部/分块结构，并在该结构上构造彩虹 C6 或反模板。 |
| [831](https://www.erdosproblems.com/831) | geometry | 4 | 1.5h | completed | 对最小饱和设计做代数消元并提取可推广圆支恒等式，或直接推进一般位置 #104。 |
| [671](https://www.erdosproblems.com/671) | analysis | 0 | 1.5h | completed | 作为 closed_watch 监测官网、正式仓库及出版记录，不再列入普通开放题攻关。 |
| [949](https://www.erdosproblems.com/949) | ramsey_theory | 3 | 1.5h | completed | 研究 sum-free 平移族的覆盖数或在满张成核中构造可递归避开的连续集。 |
| [323](https://www.erdosproblems.com/323) | number_theory | 3 | 1.5h | completed | 直接分解四次幂三元能量的非对角解，寻找超越 Hua 插值的六次矩节省。 |
| [644](https://www.erdosproblems.com/644) | combinatorics | 4 | 1.5h | completed | 改试带标签的稳定乘积或允许有界异常横截集的近次可加不等式。 |
| [812](https://www.erdosproblems.com/812) | graph_theory | 3 | 1.5h | completed | 定向构造从 n+1 阶临界着色到 n 阶对象的低重数映射。 |
| [838](https://www.erdosproblems.com/838) | geometry | 4 | 1.5h | completed | 建立 cup-cap 替换构造的凸子集生成函数，或寻找带低负载的大量见证定理。 |
| [1040](https://www.erdosproblems.com/1040) | analysis | 4 | 1.5h | completed | 构造一侧势垒或对非正则边界稳定的根迁移定理；发表前完成 MathSciNet/zbMATH 新颖性审计。 |
| [187](https://www.erdosproblems.com/187) | ramsey_theory | 4 | 1.5h | completed | 利用相邻尺度窗重叠和跨尺度颜色相关，或完全避开一般 W(2,k)。 |

### 已有解声明核验

| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |
|---:|---|---:|---:|---|---|
| [920](https://www.erdosproblems.com/920) | graph_theory | 0 | 1h | completed | 转 closed_watch，监测预印本修订、期刊审稿及官网 #920 状态同步。 |
| [689](https://www.erdosproblems.com/689) | number_theory | 1 | 1h | completed | 对 Lemma 5.3 与 Proposition 6.1 的局部因子、误差一致性和绝对常数作独立专家级审计。 |

### 论文转化（独立预算）

| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |
|---:|---|---:|---:|---|---|
| — | — | — | — | — | 本周期无任务 |

### 优先状态刷新

| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |
|---:|---|---:|---:|---|---|
| — | — | — | — | — | 本周期无任务 |

## 操作与证据规则

1. 进入任何研究阶段前刷新官网状态、原论文和最新公开讨论。
2. 每次工作结束向 `events.jsonl` 追加事件；不得覆盖历史结论。
3. 任何闭合候选必须另做题面量词审计、来源审计、独立数学QA和可复现实验/形式检查。
4. 论文级结果进入独立论文通道；它不自动降低原题闭合距离。
5. 下一轮由事件后的闭合距离、停滞计数、领域轮询和冷却期共同生成。

重建与检查：

```bash
python3 scripts/manage_erdos_rotation.py build
python3 scripts/manage_erdos_rotation.py validate
```

## 630题紧凑总台账

机器可读的完整阻塞点、下一动作、证据路径和事件统计见`artifacts/erdos_master_rotation/master_ledger.json`。下表用于快速巡检。

| # | 快照状态 | 领域 | 初筛 | 可检验分 | 题型 | 通道 | 距离 | 历史轮至 | 新事件尝试 | 停滞 |
|---:|---|---|---|---:|---|---|---:|---:|---:|---:|
| [1](https://www.erdosproblems.com/1) | open | combinatorics | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [3](https://www.erdosproblems.com/3) | open | combinatorics | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [5](https://www.erdosproblems.com/5) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [9](https://www.erdosproblems.com/9) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [10](https://www.erdosproblems.com/10) | open | number_theory | blocked | 2 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [12](https://www.erdosproblems.com/12) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [14](https://www.erdosproblems.com/14) | open | combinatorics | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [15](https://www.erdosproblems.com/15) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [18](https://www.erdosproblems.com/18) | open | number_theory | promising | 7 | binary_decision | deep_backlog | 4 | — | 1 | 0 |
| [20](https://www.erdosproblems.com/20) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [25](https://www.erdosproblems.com/25) | open | number_theory | promising | 8 | binary_decision | cooldown | 4 | 12 | 0 | 2 |
| [28](https://www.erdosproblems.com/28) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [30](https://www.erdosproblems.com/30) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [32](https://www.erdosproblems.com/32) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [33](https://www.erdosproblems.com/33) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [36](https://www.erdosproblems.com/36) | open | combinatorics | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [38](https://www.erdosproblems.com/38) | proved (Lean) | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [39](https://www.erdosproblems.com/39) | open | combinatorics | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [40](https://www.erdosproblems.com/40) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [41](https://www.erdosproblems.com/41) | open | combinatorics | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [42](https://www.erdosproblems.com/42) | solved (Lean) | combinatorics | malformed | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [43](https://www.erdosproblems.com/43) | disproved | combinatorics | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [44](https://www.erdosproblems.com/44) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [50](https://www.erdosproblems.com/50) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [51](https://www.erdosproblems.com/51) | open | number_theory | blocked | 2 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [52](https://www.erdosproblems.com/52) | open | combinatorics | partial | 6 | binary_decision | discovery_standard | 5 | — | 1 | 0 |
| [60](https://www.erdosproblems.com/60) | open | graph_theory | promising | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [61](https://www.erdosproblems.com/61) | open | graph_theory | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [62](https://www.erdosproblems.com/62) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [65](https://www.erdosproblems.com/65) | open | graph_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [66](https://www.erdosproblems.com/66) | open | number_theory | promising | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [68](https://www.erdosproblems.com/68) | open | number_theory | blocked | 2 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [70](https://www.erdosproblems.com/70) | open | graph_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [74](https://www.erdosproblems.com/74) | open | graph_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [75](https://www.erdosproblems.com/75) | open | graph_theory | malformed | 9 | mixed_or_unspecified | statement_audit | 4 | — | 0 | 0 |
| [77](https://www.erdosproblems.com/77) | open | graph_theory | blocked | 2 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [78](https://www.erdosproblems.com/78) | open | graph_theory | blocked | 8 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [80](https://www.erdosproblems.com/80) | open | graph_theory | partial | 0 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [81](https://www.erdosproblems.com/81) | open | graph_theory | promising | 0 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [82](https://www.erdosproblems.com/82) | open | graph_theory | blocked | 6 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [84](https://www.erdosproblems.com/84) | open | graph_theory | partial | 0 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [86](https://www.erdosproblems.com/86) | open | graph_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [87](https://www.erdosproblems.com/87) | open | graph_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [89](https://www.erdosproblems.com/89) | open | geometry | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [90](https://www.erdosproblems.com/90) | disproved (Lean) | geometry | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [91](https://www.erdosproblems.com/91) | open | geometry | partial | 6 | exact_or_characterisation | discovery_standard | 3 | — | 1 | 0 |
| [92](https://www.erdosproblems.com/92) | disproved | geometry | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [96](https://www.erdosproblems.com/96) | open | geometry | blocked | 2 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [98](https://www.erdosproblems.com/98) | open | geometry | blocked | 2 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [99](https://www.erdosproblems.com/99) | open | geometry | promising | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [100](https://www.erdosproblems.com/100) | open | geometry | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [101](https://www.erdosproblems.com/101) | open | geometry | partial | 4 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [102](https://www.erdosproblems.com/102) | open | geometry | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [103](https://www.erdosproblems.com/103) | open | geometry | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [104](https://www.erdosproblems.com/104) | open | geometry | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [108](https://www.erdosproblems.com/108) | open | graph_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [111](https://www.erdosproblems.com/111) | open | graph_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [112](https://www.erdosproblems.com/112) | open | graph_theory | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [114](https://www.erdosproblems.com/114) | falsifiable | analysis | partial | 7 | mixed_or_unspecified | finite_resolution | 2 | — | 0 | 0 |
| [117](https://www.erdosproblems.com/117) | open | number_theory | promising | 8 | open_ended_estimate | cooldown | 5 | — | 0 | 0 |
| [119](https://www.erdosproblems.com/119) | open | analysis | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [120](https://www.erdosproblems.com/120) | open | combinatorics | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [122](https://www.erdosproblems.com/122) | open | number_theory | malformed | 9 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [123](https://www.erdosproblems.com/123) | proved (Lean) | number_theory | malformed | 8 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [124](https://www.erdosproblems.com/124) | open | number_theory | partial | 7 | exact_or_characterisation | discovery_high | 3 | — | 0 | 0 |
| [125](https://www.erdosproblems.com/125) | disproved (Lean) | number_theory | known_resolution | 10 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [126](https://www.erdosproblems.com/126) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [129](https://www.erdosproblems.com/129) | open | graph_theory | counterexample | 10 | exact_or_characterisation | resolution_audit | 1 | — | 0 | 0 |
| [130](https://www.erdosproblems.com/130) | open | graph_theory | blocked | 2 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [131](https://www.erdosproblems.com/131) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [132](https://www.erdosproblems.com/132) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [137](https://www.erdosproblems.com/137) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [138](https://www.erdosproblems.com/138) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [141](https://www.erdosproblems.com/141) | open | combinatorics | promising | 6 | binary_decision | deep_backlog | 5 | — | 1 | 0 |
| [142](https://www.erdosproblems.com/142) | open | combinatorics | blocked | 4 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [143](https://www.erdosproblems.com/143) | open | number_theory | partial | 8 | mixed_or_unspecified | cooldown | 4 | 12 | 0 | 2 |
| [145](https://www.erdosproblems.com/145) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [146](https://www.erdosproblems.com/146) | open | graph_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [148](https://www.erdosproblems.com/148) | open | number_theory | promising | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [149](https://www.erdosproblems.com/149) | open | graph_theory | blocked | 5 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [151](https://www.erdosproblems.com/151) | open | graph_theory | promising | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [152](https://www.erdosproblems.com/152) | proved | number_theory | known_resolution | 10 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [153](https://www.erdosproblems.com/153) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [155](https://www.erdosproblems.com/155) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [156](https://www.erdosproblems.com/156) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [158](https://www.erdosproblems.com/158) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [159](https://www.erdosproblems.com/159) | open | graph_theory | blocked | 2 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [160](https://www.erdosproblems.com/160) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [161](https://www.erdosproblems.com/161) | open | ramsey_theory | malformed | 5 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [162](https://www.erdosproblems.com/162) | open | ramsey_theory | malformed | 6 | exact_or_characterisation | statement_audit | 4 | — | 0 | 0 |
| [165](https://www.erdosproblems.com/165) | open | graph_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [168](https://www.erdosproblems.com/168) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [169](https://www.erdosproblems.com/169) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [172](https://www.erdosproblems.com/172) | open | ramsey_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [173](https://www.erdosproblems.com/173) | open | geometry | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [174](https://www.erdosproblems.com/174) | open | geometry | partial | 7 | mixed_or_unspecified | discovery_high | 5 | — | 1 | 0 |
| [176](https://www.erdosproblems.com/176) | open | combinatorics | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [177](https://www.erdosproblems.com/177) | open | number_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [180](https://www.erdosproblems.com/180) | open | graph_theory | counterexample | 10 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [181](https://www.erdosproblems.com/181) | open | graph_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [183](https://www.erdosproblems.com/183) | open | graph_theory | partial | 3 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [184](https://www.erdosproblems.com/184) | open | graph_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [187](https://www.erdosproblems.com/187) | open | ramsey_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 4 | — | 2 | 0 |
| [188](https://www.erdosproblems.com/188) | open | geometry | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [190](https://www.erdosproblems.com/190) | solved | combinatorics | known_resolution | 9 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [193](https://www.erdosproblems.com/193) | open | geometry | partial | 5 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [195](https://www.erdosproblems.com/195) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [196](https://www.erdosproblems.com/196) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [197](https://www.erdosproblems.com/197) | open | number_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [200](https://www.erdosproblems.com/200) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [201](https://www.erdosproblems.com/201) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [202](https://www.erdosproblems.com/202) | solved (Lean) | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [203](https://www.erdosproblems.com/203) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [205](https://www.erdosproblems.com/205) | disproved (Lean) | number_theory | counterexample | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [208](https://www.erdosproblems.com/208) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [212](https://www.erdosproblems.com/212) | open | geometry | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [213](https://www.erdosproblems.com/213) | open | geometry | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [217](https://www.erdosproblems.com/217) | open | geometry | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [218](https://www.erdosproblems.com/218) | open | number_theory | partial | 7 | mixed_or_unspecified | discovery_high | 3 | — | 0 | 0 |
| [222](https://www.erdosproblems.com/222) | open | number_theory | partial | 6 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [233](https://www.erdosproblems.com/233) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [234](https://www.erdosproblems.com/234) | open | number_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [236](https://www.erdosproblems.com/236) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [238](https://www.erdosproblems.com/238) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 4 | — | 1 | 0 |
| [241](https://www.erdosproblems.com/241) | open | combinatorics | promising | 5 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [243](https://www.erdosproblems.com/243) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [244](https://www.erdosproblems.com/244) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [247](https://www.erdosproblems.com/247) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [249](https://www.erdosproblems.com/249) | open | number_theory | partial | 2 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [251](https://www.erdosproblems.com/251) | open | number_theory | partial | 2 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [252](https://www.erdosproblems.com/252) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [254](https://www.erdosproblems.com/254) | open | number_theory | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [256](https://www.erdosproblems.com/256) | open | analysis | partial | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [257](https://www.erdosproblems.com/257) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [258](https://www.erdosproblems.com/258) | proved (Lean) | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [260](https://www.erdosproblems.com/260) | open | number_theory | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [261](https://www.erdosproblems.com/261) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [263](https://www.erdosproblems.com/263) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [264](https://www.erdosproblems.com/264) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [265](https://www.erdosproblems.com/265) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [267](https://www.erdosproblems.com/267) | open | number_theory | promising | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [269](https://www.erdosproblems.com/269) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [271](https://www.erdosproblems.com/271) | open | combinatorics | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [272](https://www.erdosproblems.com/272) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [273](https://www.erdosproblems.com/273) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [274](https://www.erdosproblems.com/274) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [276](https://www.erdosproblems.com/276) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [278](https://www.erdosproblems.com/278) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [279](https://www.erdosproblems.com/279) | open | number_theory | promising | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [281](https://www.erdosproblems.com/281) | proved (Lean) | number_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [282](https://www.erdosproblems.com/282) | open | number_theory | blocked | 5 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [283](https://www.erdosproblems.com/283) | proved (Lean) | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [288](https://www.erdosproblems.com/288) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [289](https://www.erdosproblems.com/289) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [291](https://www.erdosproblems.com/291) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [293](https://www.erdosproblems.com/293) | open | number_theory | malformed | 7 | open_ended_estimate | statement_audit | 4 | — | 0 | 0 |
| [295](https://www.erdosproblems.com/295) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [301](https://www.erdosproblems.com/301) | open | number_theory | partial | 8 | open_ended_estimate | paper_conversion | 4 | 12 | 0 | 2 |
| [302](https://www.erdosproblems.com/302) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [304](https://www.erdosproblems.com/304) | open | number_theory | blocked | 4 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [306](https://www.erdosproblems.com/306) | open | number_theory | promising | 3 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [311](https://www.erdosproblems.com/311) | open | number_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [312](https://www.erdosproblems.com/312) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [313](https://www.erdosproblems.com/313) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [317](https://www.erdosproblems.com/317) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [318](https://www.erdosproblems.com/318) | solved | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [319](https://www.erdosproblems.com/319) | open | number_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [320](https://www.erdosproblems.com/320) | solved | number_theory | known_resolution | 8 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [321](https://www.erdosproblems.com/321) | solved | number_theory | partial | 7 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [322](https://www.erdosproblems.com/322) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [323](https://www.erdosproblems.com/323) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [324](https://www.erdosproblems.com/324) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [325](https://www.erdosproblems.com/325) | open | number_theory | partial | 8 | binary_decision | cooldown | 4 | 12 | 0 | 2 |
| [326](https://www.erdosproblems.com/326) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [327](https://www.erdosproblems.com/327) | open | number_theory | promising | 7 | binary_decision | intake_active | 3 | — | 1 | 0 |
| [329](https://www.erdosproblems.com/329) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [330](https://www.erdosproblems.com/330) | proved (Lean) | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [332](https://www.erdosproblems.com/332) | open | number_theory | partial | 8 | exact_or_characterisation | cooldown | 4 | 12 | 0 | 2 |
| [334](https://www.erdosproblems.com/334) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [335](https://www.erdosproblems.com/335) | open | combinatorics | counterexample | 6 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [336](https://www.erdosproblems.com/336) | open | number_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [338](https://www.erdosproblems.com/338) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [340](https://www.erdosproblems.com/340) | open | combinatorics | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [341](https://www.erdosproblems.com/341) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [342](https://www.erdosproblems.com/342) | open | number_theory | partial | 7 | exact_or_characterisation | discovery_high | 3 | — | 0 | 0 |
| [345](https://www.erdosproblems.com/345) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [346](https://www.erdosproblems.com/346) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [347](https://www.erdosproblems.com/347) | proved (Lean) | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [348](https://www.erdosproblems.com/348) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [349](https://www.erdosproblems.com/349) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [351](https://www.erdosproblems.com/351) | proved (Lean) | number_theory | malformed | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [352](https://www.erdosproblems.com/352) | open | geometry | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [354](https://www.erdosproblems.com/354) | open | number_theory | promising | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [357](https://www.erdosproblems.com/357) | open | number_theory | partial | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [358](https://www.erdosproblems.com/358) | proved | number_theory | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [359](https://www.erdosproblems.com/359) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [361](https://www.erdosproblems.com/361) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [365](https://www.erdosproblems.com/365) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [367](https://www.erdosproblems.com/367) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [368](https://www.erdosproblems.com/368) | open | number_theory | promising | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [369](https://www.erdosproblems.com/369) | proved (Lean) | number_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [371](https://www.erdosproblems.com/371) | open | number_theory | blocked | 10 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [373](https://www.erdosproblems.com/373) | open | number_theory | blocked | 9 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [374](https://www.erdosproblems.com/374) | open | number_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [376](https://www.erdosproblems.com/376) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [377](https://www.erdosproblems.com/377) | open | number_theory | promising | 8 | mixed_or_unspecified | cooldown | 4 | 12 | 0 | 2 |
| [380](https://www.erdosproblems.com/380) | proved | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [382](https://www.erdosproblems.com/382) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [383](https://www.erdosproblems.com/383) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [385](https://www.erdosproblems.com/385) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [386](https://www.erdosproblems.com/386) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [387](https://www.erdosproblems.com/387) | solved | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [388](https://www.erdosproblems.com/388) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [389](https://www.erdosproblems.com/389) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [390](https://www.erdosproblems.com/390) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [393](https://www.erdosproblems.com/393) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [394](https://www.erdosproblems.com/394) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [396](https://www.erdosproblems.com/396) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [397](https://www.erdosproblems.com/397) | disproved (Lean) | number_theory | counterexample | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [400](https://www.erdosproblems.com/400) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [401](https://www.erdosproblems.com/401) | proved (Lean) | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [404](https://www.erdosproblems.com/404) | open | number_theory | promising | 7 | exact_or_characterisation | discovery_high | 3 | — | 0 | 0 |
| [406](https://www.erdosproblems.com/406) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [408](https://www.erdosproblems.com/408) | open | number_theory | partial | 4 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [409](https://www.erdosproblems.com/409) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [410](https://www.erdosproblems.com/410) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [411](https://www.erdosproblems.com/411) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [412](https://www.erdosproblems.com/412) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [413](https://www.erdosproblems.com/413) | open | number_theory | partial | 7 | binary_decision | discovery_high | 3 | — | 0 | 0 |
| [414](https://www.erdosproblems.com/414) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [415](https://www.erdosproblems.com/415) | open | number_theory | partial | 7 | binary_decision | discovery_high | 3 | — | 0 | 0 |
| [416](https://www.erdosproblems.com/416) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [417](https://www.erdosproblems.com/417) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [420](https://www.erdosproblems.com/420) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [421](https://www.erdosproblems.com/421) | open | number_theory | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [422](https://www.erdosproblems.com/422) | open | number_theory | blocked | 2 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [423](https://www.erdosproblems.com/423) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [424](https://www.erdosproblems.com/424) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [425](https://www.erdosproblems.com/425) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [428](https://www.erdosproblems.com/428) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [430](https://www.erdosproblems.com/430) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [431](https://www.erdosproblems.com/431) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [432](https://www.erdosproblems.com/432) | open | number_theory | promising | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [436](https://www.erdosproblems.com/436) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [445](https://www.erdosproblems.com/445) | open | number_theory | blocked | 6 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [450](https://www.erdosproblems.com/450) | open | number_theory | malformed | 9 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [451](https://www.erdosproblems.com/451) | open | number_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [452](https://www.erdosproblems.com/452) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [454](https://www.erdosproblems.com/454) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [455](https://www.erdosproblems.com/455) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [456](https://www.erdosproblems.com/456) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [457](https://www.erdosproblems.com/457) | proved (Lean) | number_theory | known_resolution | 10 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [460](https://www.erdosproblems.com/460) | open | number_theory | malformed | 8 | exact_or_characterisation | statement_audit | 4 | — | 0 | 0 |
| [461](https://www.erdosproblems.com/461) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [462](https://www.erdosproblems.com/462) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [463](https://www.erdosproblems.com/463) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [467](https://www.erdosproblems.com/467) | open | number_theory | promising | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [468](https://www.erdosproblems.com/468) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [469](https://www.erdosproblems.com/469) | open | number_theory | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [470](https://www.erdosproblems.com/470) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [472](https://www.erdosproblems.com/472) | open | number_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [477](https://www.erdosproblems.com/477) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [478](https://www.erdosproblems.com/478) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [479](https://www.erdosproblems.com/479) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [483](https://www.erdosproblems.com/483) | open | ramsey_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [486](https://www.erdosproblems.com/486) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [488](https://www.erdosproblems.com/488) | falsifiable | number_theory | partial | 6 | binary_decision | finite_resolution | 2 | — | 0 | 0 |
| [489](https://www.erdosproblems.com/489) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [495](https://www.erdosproblems.com/495) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [500](https://www.erdosproblems.com/500) | open | graph_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [501](https://www.erdosproblems.com/501) | open | combinatorics | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [503](https://www.erdosproblems.com/503) | open | geometry | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [507](https://www.erdosproblems.com/507) | open | geometry | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [509](https://www.erdosproblems.com/509) | open | analysis | promising | 5 | mixed_or_unspecified | discovery_standard | 4 | — | 1 | 0 |
| [510](https://www.erdosproblems.com/510) | open | analysis | malformed | 8 | mixed_or_unspecified | statement_audit | 4 | — | 0 | 0 |
| [513](https://www.erdosproblems.com/513) | open | analysis | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [514](https://www.erdosproblems.com/514) | open | analysis | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [517](https://www.erdosproblems.com/517) | open | analysis | partial | 5 | binary_decision | discovery_standard | 5 | — | 1 | 0 |
| [520](https://www.erdosproblems.com/520) | open | number_theory | known_resolution | 9 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [521](https://www.erdosproblems.com/521) | open | analysis | promising | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [522](https://www.erdosproblems.com/522) | open | analysis | promising | 7 | binary_decision | closed_watch | 0 | — | 1 | 0 |
| [524](https://www.erdosproblems.com/524) | open | analysis | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [528](https://www.erdosproblems.com/528) | open | geometry | partial | 3 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [529](https://www.erdosproblems.com/529) | open | geometry | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [530](https://www.erdosproblems.com/530) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [531](https://www.erdosproblems.com/531) | open | ramsey_theory | promising | 7 | open_ended_estimate | discovery_high | 3 | — | 1 | 0 |
| [533](https://www.erdosproblems.com/533) | disproved | graph_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [535](https://www.erdosproblems.com/535) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [536](https://www.erdosproblems.com/536) | open | number_theory | partial | 7 | binary_decision | discovery_high | 4 | — | 1 | 0 |
| [538](https://www.erdosproblems.com/538) | open | number_theory | promising | 7 | mixed_or_unspecified | discovery_high | 3 | — | 0 | 0 |
| [539](https://www.erdosproblems.com/539) | open | number_theory | partial | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [543](https://www.erdosproblems.com/543) | disproved | number_theory | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [544](https://www.erdosproblems.com/544) | open | graph_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [545](https://www.erdosproblems.com/545) | open | graph_theory | counterexample | 10 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [550](https://www.erdosproblems.com/550) | open | graph_theory | known_resolution | 7 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [552](https://www.erdosproblems.com/552) | open | graph_theory | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [554](https://www.erdosproblems.com/554) | open | graph_theory | promising | 4 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [555](https://www.erdosproblems.com/555) | open | graph_theory | blocked | 5 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [557](https://www.erdosproblems.com/557) | open | graph_theory | blocked | 6 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [558](https://www.erdosproblems.com/558) | open | graph_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [560](https://www.erdosproblems.com/560) | open | graph_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [561](https://www.erdosproblems.com/561) | open | graph_theory | malformed | 4 | exact_or_characterisation | statement_audit | 4 | — | 0 | 0 |
| [562](https://www.erdosproblems.com/562) | open | graph_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [563](https://www.erdosproblems.com/563) | open | graph_theory | counterexample | 8 | exact_or_characterisation | resolution_audit | 1 | — | 0 | 0 |
| [564](https://www.erdosproblems.com/564) | open | graph_theory | blocked | 2 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [566](https://www.erdosproblems.com/566) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [567](https://www.erdosproblems.com/567) | open | graph_theory | blocked | 1 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [568](https://www.erdosproblems.com/568) | open | graph_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [569](https://www.erdosproblems.com/569) | open | graph_theory | promising | 7 | open_ended_estimate | resolution_audit | 1 | — | 0 | 0 |
| [571](https://www.erdosproblems.com/571) | open | graph_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [572](https://www.erdosproblems.com/572) | open | graph_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [573](https://www.erdosproblems.com/573) | open | graph_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [574](https://www.erdosproblems.com/574) | disproved | graph_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [575](https://www.erdosproblems.com/575) | open | graph_theory | counterexample | 10 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [576](https://www.erdosproblems.com/576) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [579](https://www.erdosproblems.com/579) | open | graph_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [584](https://www.erdosproblems.com/584) | open | graph_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [585](https://www.erdosproblems.com/585) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [588](https://www.erdosproblems.com/588) | open | geometry | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [589](https://www.erdosproblems.com/589) | open | geometry | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [591](https://www.erdosproblems.com/591) | proved | ramsey_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [592](https://www.erdosproblems.com/592) | open | ramsey_theory | promising | 7 | open_ended_estimate | closure_core | 2 | — | 3 | 0 |
| [593](https://www.erdosproblems.com/593) | open | graph_theory | partial | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [595](https://www.erdosproblems.com/595) | open | graph_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [596](https://www.erdosproblems.com/596) | open | graph_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 2 | 0 |
| [597](https://www.erdosproblems.com/597) | open | graph_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [598](https://www.erdosproblems.com/598) | open | ramsey_theory | promising | 6 | binary_decision | closed_watch | 0 | — | 2 | 0 |
| [600](https://www.erdosproblems.com/600) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [601](https://www.erdosproblems.com/601) | open | graph_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [602](https://www.erdosproblems.com/602) | open | combinatorics | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [603](https://www.erdosproblems.com/603) | solved | combinatorics | known_resolution | 10 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [604](https://www.erdosproblems.com/604) | open | geometry | promising | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [609](https://www.erdosproblems.com/609) | open | graph_theory | promising | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [610](https://www.erdosproblems.com/610) | proved (Lean) | graph_theory | known_resolution | 10 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [611](https://www.erdosproblems.com/611) | open | graph_theory | promising | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [612](https://www.erdosproblems.com/612) | open | graph_theory | counterexample | 8 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [614](https://www.erdosproblems.com/614) | open | graph_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [616](https://www.erdosproblems.com/616) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [619](https://www.erdosproblems.com/619) | solved (Lean) | graph_theory | counterexample | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [620](https://www.erdosproblems.com/620) | open | graph_theory | promising | 7 | binary_decision | closed_watch | 0 | — | 2 | 0 |
| [623](https://www.erdosproblems.com/623) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [624](https://www.erdosproblems.com/624) | open | combinatorics | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [625](https://www.erdosproblems.com/625) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [626](https://www.erdosproblems.com/626) | open | graph_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [627](https://www.erdosproblems.com/627) | open | graph_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [629](https://www.erdosproblems.com/629) | open | graph_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [635](https://www.erdosproblems.com/635) | open | number_theory | partial | 8 | binary_decision | closure_core | 2 | 12 | 3 | 0 |
| [638](https://www.erdosproblems.com/638) | open | graph_theory | counterexample | 10 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [640](https://www.erdosproblems.com/640) | open | graph_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [642](https://www.erdosproblems.com/642) | open | graph_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [643](https://www.erdosproblems.com/643) | open | graph_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [644](https://www.erdosproblems.com/644) | open | combinatorics | promising | 5 | binary_decision | discovery_standard | 4 | — | 1 | 0 |
| [650](https://www.erdosproblems.com/650) | solved (Lean) | number_theory | known_resolution | 10 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [652](https://www.erdosproblems.com/652) | proved | geometry | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [653](https://www.erdosproblems.com/653) | open | geometry | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [654](https://www.erdosproblems.com/654) | open | geometry | counterexample | 10 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [655](https://www.erdosproblems.com/655) | open | geometry | counterexample | 9 | open_ended_estimate | resolution_audit | 1 | — | 0 | 0 |
| [657](https://www.erdosproblems.com/657) | open | geometry | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [659](https://www.erdosproblems.com/659) | proved (Lean) | geometry | known_resolution | 8 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [660](https://www.erdosproblems.com/660) | open | geometry | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [661](https://www.erdosproblems.com/661) | open | geometry | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [662](https://www.erdosproblems.com/662) | open | geometry | malformed | 1 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [663](https://www.erdosproblems.com/663) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [665](https://www.erdosproblems.com/665) | open | combinatorics | promising | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [667](https://www.erdosproblems.com/667) | open | graph_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [668](https://www.erdosproblems.com/668) | open | geometry | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [669](https://www.erdosproblems.com/669) | open | geometry | blocked | 4 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [670](https://www.erdosproblems.com/670) | open | geometry | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [671](https://www.erdosproblems.com/671) | open | analysis | partial | 5 | exact_or_characterisation | closed_watch | 0 | — | 2 | 0 |
| [675](https://www.erdosproblems.com/675) | open | number_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [676](https://www.erdosproblems.com/676) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [677](https://www.erdosproblems.com/677) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [679](https://www.erdosproblems.com/679) | open | number_theory | partial | 8 | binary_decision | cooldown | 4 | 12 | 0 | 2 |
| [680](https://www.erdosproblems.com/680) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [681](https://www.erdosproblems.com/681) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [683](https://www.erdosproblems.com/683) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [684](https://www.erdosproblems.com/684) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [685](https://www.erdosproblems.com/685) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [686](https://www.erdosproblems.com/686) | open | number_theory | promising | 8 | mixed_or_unspecified | cooldown | 4 | 12 | 0 | 2 |
| [687](https://www.erdosproblems.com/687) | open | number_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [688](https://www.erdosproblems.com/688) | open | number_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [689](https://www.erdosproblems.com/689) | open | number_theory | partial | 5 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [690](https://www.erdosproblems.com/690) | solved | number_theory | known_resolution | 8 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [691](https://www.erdosproblems.com/691) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [693](https://www.erdosproblems.com/693) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [694](https://www.erdosproblems.com/694) | solved (Lean) | number_theory | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [695](https://www.erdosproblems.com/695) | open | number_theory | partial | 0 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [696](https://www.erdosproblems.com/696) | solved (Lean) | number_theory | known_resolution | 0 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [700](https://www.erdosproblems.com/700) | open | number_theory | partial | 0 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [701](https://www.erdosproblems.com/701) | open | combinatorics | counterexample | 0 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [704](https://www.erdosproblems.com/704) | open | geometry | partial | 0 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [705](https://www.erdosproblems.com/705) | disproved | graph_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [706](https://www.erdosproblems.com/706) | open | graph_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [708](https://www.erdosproblems.com/708) | open | number_theory | malformed | 4 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [709](https://www.erdosproblems.com/709) | open | number_theory | promising | 7 | exact_or_characterisation | discovery_high | 3 | — | 0 | 0 |
| [710](https://www.erdosproblems.com/710) | open | number_theory | partial | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [711](https://www.erdosproblems.com/711) | open | number_theory | partial | 3 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [712](https://www.erdosproblems.com/712) | open | graph_theory | malformed | 2 | open_ended_estimate | statement_audit | 4 | — | 0 | 0 |
| [713](https://www.erdosproblems.com/713) | open | graph_theory | malformed | 2 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [714](https://www.erdosproblems.com/714) | open | graph_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [719](https://www.erdosproblems.com/719) | open | graph_theory | blocked | 4 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [724](https://www.erdosproblems.com/724) | open | combinatorics | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [725](https://www.erdosproblems.com/725) | open | combinatorics | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [726](https://www.erdosproblems.com/726) | open | number_theory | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [727](https://www.erdosproblems.com/727) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [729](https://www.erdosproblems.com/729) | proved (Lean) | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [730](https://www.erdosproblems.com/730) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [731](https://www.erdosproblems.com/731) | open | number_theory | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [734](https://www.erdosproblems.com/734) | open | combinatorics | promising | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [738](https://www.erdosproblems.com/738) | open | graph_theory | partial | 6 | binary_decision | discovery_standard | 4 | — | 1 | 0 |
| [740](https://www.erdosproblems.com/740) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [741](https://www.erdosproblems.com/741) | solved (Lean) | combinatorics | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [749](https://www.erdosproblems.com/749) | open | combinatorics | promising | 5 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [750](https://www.erdosproblems.com/750) | proved (Lean) | graph_theory | blocked | 3 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [757](https://www.erdosproblems.com/757) | open | geometry | partial | 6 | binary_decision | discovery_standard | 4 | — | 1 | 0 |
| [761](https://www.erdosproblems.com/761) | open | graph_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [766](https://www.erdosproblems.com/766) | open | graph_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [768](https://www.erdosproblems.com/768) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [769](https://www.erdosproblems.com/769) | open | geometry | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [770](https://www.erdosproblems.com/770) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [773](https://www.erdosproblems.com/773) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [774](https://www.erdosproblems.com/774) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [776](https://www.erdosproblems.com/776) | open | combinatorics | promising | 8 | binary_decision | closure_core | 1 | 12 | 3 | 0 |
| [778](https://www.erdosproblems.com/778) | open | graph_theory | promising | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [782](https://www.erdosproblems.com/782) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [783](https://www.erdosproblems.com/783) | solved | number_theory | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [786](https://www.erdosproblems.com/786) | open | number_theory | known_resolution | 9 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [787](https://www.erdosproblems.com/787) | open | combinatorics | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [788](https://www.erdosproblems.com/788) | open | combinatorics | partial | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [789](https://www.erdosproblems.com/789) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [790](https://www.erdosproblems.com/790) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [791](https://www.erdosproblems.com/791) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [792](https://www.erdosproblems.com/792) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [793](https://www.erdosproblems.com/793) | proved (Lean) | number_theory | malformed | 4 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [796](https://www.erdosproblems.com/796) | open | number_theory | counterexample | 8 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [802](https://www.erdosproblems.com/802) | open | graph_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [805](https://www.erdosproblems.com/805) | open | graph_theory | promising | 4 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [809](https://www.erdosproblems.com/809) | open | graph_theory | partial | 7 | binary_decision | closure_core | 2 | — | 4 | 0 |
| [810](https://www.erdosproblems.com/810) | open | graph_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [811](https://www.erdosproblems.com/811) | open | graph_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [812](https://www.erdosproblems.com/812) | open | graph_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [813](https://www.erdosproblems.com/813) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [817](https://www.erdosproblems.com/817) | open | combinatorics | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [819](https://www.erdosproblems.com/819) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [820](https://www.erdosproblems.com/820) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [821](https://www.erdosproblems.com/821) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [824](https://www.erdosproblems.com/824) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [826](https://www.erdosproblems.com/826) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [827](https://www.erdosproblems.com/827) | open | geometry | promising | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [828](https://www.erdosproblems.com/828) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [829](https://www.erdosproblems.com/829) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [830](https://www.erdosproblems.com/830) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [831](https://www.erdosproblems.com/831) | open | geometry | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 1 | 0 |
| [836](https://www.erdosproblems.com/836) | open | graph_theory | counterexample | 6 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [837](https://www.erdosproblems.com/837) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [838](https://www.erdosproblems.com/838) | open | geometry | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 1 | 0 |
| [839](https://www.erdosproblems.com/839) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [840](https://www.erdosproblems.com/840) | open | combinatorics | partial | 6 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [846](https://www.erdosproblems.com/846) | disproved (Lean) | geometry | counterexample | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [847](https://www.erdosproblems.com/847) | disproved | combinatorics | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [849](https://www.erdosproblems.com/849) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [850](https://www.erdosproblems.com/850) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [851](https://www.erdosproblems.com/851) | proved | number_theory | known_resolution | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [852](https://www.erdosproblems.com/852) | open | number_theory | blocked | 4 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [853](https://www.erdosproblems.com/853) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [854](https://www.erdosproblems.com/854) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [856](https://www.erdosproblems.com/856) | open | number_theory | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [857](https://www.erdosproblems.com/857) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [858](https://www.erdosproblems.com/858) | solved | number_theory | known_resolution | 9 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [859](https://www.erdosproblems.com/859) | open | number_theory | promising | 7 | exact_or_characterisation | discovery_high | 3 | — | 0 | 0 |
| [860](https://www.erdosproblems.com/860) | open | number_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [863](https://www.erdosproblems.com/863) | proved | combinatorics | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [864](https://www.erdosproblems.com/864) | open | combinatorics | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [865](https://www.erdosproblems.com/865) | proved (Lean) | combinatorics | known_resolution | 8 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [866](https://www.erdosproblems.com/866) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [868](https://www.erdosproblems.com/868) | solved | number_theory | known_resolution | 7 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [869](https://www.erdosproblems.com/869) | disproved | number_theory | counterexample | 8 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [870](https://www.erdosproblems.com/870) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [871](https://www.erdosproblems.com/871) | disproved (Lean) | number_theory | counterexample | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [872](https://www.erdosproblems.com/872) | open | number_theory | partial | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [873](https://www.erdosproblems.com/873) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [875](https://www.erdosproblems.com/875) | open | combinatorics | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [876](https://www.erdosproblems.com/876) | open | combinatorics | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [878](https://www.erdosproblems.com/878) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [879](https://www.erdosproblems.com/879) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [881](https://www.erdosproblems.com/881) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [883](https://www.erdosproblems.com/883) | open | graph_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [884](https://www.erdosproblems.com/884) | disproved (Lean) | number_theory | counterexample | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [885](https://www.erdosproblems.com/885) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [886](https://www.erdosproblems.com/886) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [887](https://www.erdosproblems.com/887) | open | number_theory | blocked | 5 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [888](https://www.erdosproblems.com/888) | solved | number_theory | known_resolution | 9 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [889](https://www.erdosproblems.com/889) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [890](https://www.erdosproblems.com/890) | open | number_theory | counterexample | 8 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [891](https://www.erdosproblems.com/891) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [892](https://www.erdosproblems.com/892) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [893](https://www.erdosproblems.com/893) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [896](https://www.erdosproblems.com/896) | solved | number_theory | known_resolution | 5 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [901](https://www.erdosproblems.com/901) | open | combinatorics | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [902](https://www.erdosproblems.com/902) | open | graph_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [906](https://www.erdosproblems.com/906) | open | analysis | partial | 3 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [911](https://www.erdosproblems.com/911) | open | graph_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [912](https://www.erdosproblems.com/912) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [913](https://www.erdosproblems.com/913) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [917](https://www.erdosproblems.com/917) | open | graph_theory | known_resolution | 7 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [918](https://www.erdosproblems.com/918) | open | graph_theory | independent | 6 | mixed_or_unspecified | resolution_audit | 1 | — | 0 | 0 |
| [919](https://www.erdosproblems.com/919) | open | graph_theory | blocked | 2 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [920](https://www.erdosproblems.com/920) | open | graph_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [928](https://www.erdosproblems.com/928) | open | number_theory | promising | 4 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [929](https://www.erdosproblems.com/929) | open | number_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [930](https://www.erdosproblems.com/930) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [931](https://www.erdosproblems.com/931) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [932](https://www.erdosproblems.com/932) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [933](https://www.erdosproblems.com/933) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [934](https://www.erdosproblems.com/934) | open | graph_theory | promising | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [935](https://www.erdosproblems.com/935) | open | number_theory | known_resolution | 9 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [936](https://www.erdosproblems.com/936) | open | number_theory | promising | 7 | mixed_or_unspecified | discovery_high | 3 | — | 0 | 0 |
| [938](https://www.erdosproblems.com/938) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [939](https://www.erdosproblems.com/939) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [940](https://www.erdosproblems.com/940) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [942](https://www.erdosproblems.com/942) | open | number_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [943](https://www.erdosproblems.com/943) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [944](https://www.erdosproblems.com/944) | open | graph_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [945](https://www.erdosproblems.com/945) | open | number_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [948](https://www.erdosproblems.com/948) | solved | ramsey_theory | counterexample | 9 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [949](https://www.erdosproblems.com/949) | open | ramsey_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 2 | 0 |
| [950](https://www.erdosproblems.com/950) | open | number_theory | partial | 8 | binary_decision | cooldown | 4 | 12 | 0 | 2 |
| [951](https://www.erdosproblems.com/951) | open | number_theory | malformed | 5 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [952](https://www.erdosproblems.com/952) | open | number_theory | partial | 10 | mixed_or_unspecified | cooldown | 4 | 12 | 0 | 2 |
| [953](https://www.erdosproblems.com/953) | open | geometry | promising | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [954](https://www.erdosproblems.com/954) | open | number_theory | promising | 5 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [955](https://www.erdosproblems.com/955) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [956](https://www.erdosproblems.com/956) | open | geometry | promising | 7 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [959](https://www.erdosproblems.com/959) | open | geometry | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [960](https://www.erdosproblems.com/960) | disproved | geometry | counterexample | 10 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [961](https://www.erdosproblems.com/961) | open | number_theory | partial | 4 | open_ended_estimate | deep_backlog | 4 | — | 0 | 0 |
| [962](https://www.erdosproblems.com/962) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [963](https://www.erdosproblems.com/963) | open | number_theory | promising | 8 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [965](https://www.erdosproblems.com/965) | disproved | ramsey_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [968](https://www.erdosproblems.com/968) | open | number_theory | partial | 6 | mixed_or_unspecified | discovery_standard | 3 | — | 0 | 0 |
| [969](https://www.erdosproblems.com/969) | open | number_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [970](https://www.erdosproblems.com/970) | open | number_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [971](https://www.erdosproblems.com/971) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [972](https://www.erdosproblems.com/972) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [973](https://www.erdosproblems.com/973) | open | analysis | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [975](https://www.erdosproblems.com/975) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [976](https://www.erdosproblems.com/976) | open | number_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [978](https://www.erdosproblems.com/978) | open | number_theory | malformed | 5 | binary_decision | statement_audit | 4 | — | 0 | 0 |
| [979](https://www.erdosproblems.com/979) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [983](https://www.erdosproblems.com/983) | open | number_theory | blocked | 6 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [985](https://www.erdosproblems.com/985) | open | number_theory | counterexample | 4 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [986](https://www.erdosproblems.com/986) | proved | graph_theory | blocked | 2 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [987](https://www.erdosproblems.com/987) | proved | analysis | partial | 7 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [990](https://www.erdosproblems.com/990) | disproved (Lean) | analysis | blocked | 6 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [992](https://www.erdosproblems.com/992) | disproved | number_theory | known_resolution | 8 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [995](https://www.erdosproblems.com/995) | open | analysis | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [996](https://www.erdosproblems.com/996) | open | analysis | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [997](https://www.erdosproblems.com/997) | proved (Lean) | analysis | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1002](https://www.erdosproblems.com/1002) | open | analysis | partial | 5 | mixed_or_unspecified | discovery_standard | 3 | — | 1 | 0 |
| [1003](https://www.erdosproblems.com/1003) | open | number_theory | partial | 3 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [1004](https://www.erdosproblems.com/1004) | open | number_theory | promising | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1005](https://www.erdosproblems.com/1005) | open | number_theory | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1011](https://www.erdosproblems.com/1011) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1013](https://www.erdosproblems.com/1013) | open | graph_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [1014](https://www.erdosproblems.com/1014) | proved (Lean) | graph_theory | known_resolution | 9 | exact_or_characterisation | closed_watch | 0 | — | 0 | 0 |
| [1016](https://www.erdosproblems.com/1016) | open | graph_theory | blocked | 3 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [1017](https://www.erdosproblems.com/1017) | open | graph_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1021](https://www.erdosproblems.com/1021) | proved | graph_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1022](https://www.erdosproblems.com/1022) | proved (Lean) | combinatorics | counterexample | 10 | mixed_or_unspecified | closed_watch | 0 | — | 0 | 0 |
| [1029](https://www.erdosproblems.com/1029) | open | graph_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [1030](https://www.erdosproblems.com/1030) | open | graph_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1032](https://www.erdosproblems.com/1032) | open | graph_theory | blocked | 2 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1033](https://www.erdosproblems.com/1033) | open | graph_theory | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1035](https://www.erdosproblems.com/1035) | open | graph_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [1038](https://www.erdosproblems.com/1038) | open | analysis | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1039](https://www.erdosproblems.com/1039) | open | analysis | promising | 9 | open_ended_estimate | resolution_ready | 0 | — | 0 | 0 |
| [1040](https://www.erdosproblems.com/1040) | open | analysis | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 1 | 0 |
| [1044](https://www.erdosproblems.com/1044) | solved (Lean) | analysis | known_resolution | 9 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [1049](https://www.erdosproblems.com/1049) | open | number_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1051](https://www.erdosproblems.com/1051) | proved (Lean) | number_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1052](https://www.erdosproblems.com/1052) | open | number_theory | promising | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1053](https://www.erdosproblems.com/1053) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1054](https://www.erdosproblems.com/1054) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1055](https://www.erdosproblems.com/1055) | open | number_theory | blocked | 3 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1056](https://www.erdosproblems.com/1056) | open | number_theory | promising | 7 | binary_decision | intake_active | 3 | — | 1 | 0 |
| [1057](https://www.erdosproblems.com/1057) | open | number_theory | blocked | 4 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1059](https://www.erdosproblems.com/1059) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [1060](https://www.erdosproblems.com/1060) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1061](https://www.erdosproblems.com/1061) | open | number_theory | partial | 6 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1062](https://www.erdosproblems.com/1062) | open | number_theory | promising | 6 | exact_or_characterisation | discovery_standard | 3 | — | 0 | 0 |
| [1063](https://www.erdosproblems.com/1063) | open | number_theory | promising | 8 | open_ended_estimate | paper_conversion | 4 | 12 | 0 | 2 |
| [1065](https://www.erdosproblems.com/1065) | open | number_theory | blocked | 2 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1066](https://www.erdosproblems.com/1066) | open | graph_theory | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1068](https://www.erdosproblems.com/1068) | open | graph_theory | blocked | 3 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [1070](https://www.erdosproblems.com/1070) | open | geometry | counterexample | 8 | open_ended_estimate | resolution_audit | 1 | — | 0 | 0 |
| [1071](https://www.erdosproblems.com/1071) | proved (Lean) | geometry | known_resolution | 6 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1072](https://www.erdosproblems.com/1072) | open | number_theory | blocked | 10 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1073](https://www.erdosproblems.com/1073) | open | number_theory | blocked | 8 | binary_decision | deep_backlog | 5 | — | 0 | 0 |
| [1074](https://www.erdosproblems.com/1074) | open | number_theory | blocked | 9 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [1075](https://www.erdosproblems.com/1075) | open | number_theory | blocked | 7 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1083](https://www.erdosproblems.com/1083) | open | geometry | promising | 10 | open_ended_estimate | cooldown | 4 | 12 | 0 | 2 |
| [1084](https://www.erdosproblems.com/1084) | open | geometry | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [1085](https://www.erdosproblems.com/1085) | open | geometry | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1086](https://www.erdosproblems.com/1086) | open | geometry | promising | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1087](https://www.erdosproblems.com/1087) | open | geometry | promising | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [1088](https://www.erdosproblems.com/1088) | open | geometry | partial | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1089](https://www.erdosproblems.com/1089) | solved | geometry | known_resolution | 10 | open_ended_estimate | closed_watch | 0 | — | 0 | 0 |
| [1091](https://www.erdosproblems.com/1091) | solved | geometry | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1092](https://www.erdosproblems.com/1092) | disproved | geometry | counterexample | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1093](https://www.erdosproblems.com/1093) | open | number_theory | partial | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [1094](https://www.erdosproblems.com/1094) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1095](https://www.erdosproblems.com/1095) | open | number_theory | blocked | 4 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
| [1096](https://www.erdosproblems.com/1096) | proved | number_theory | known_resolution | 10 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1097](https://www.erdosproblems.com/1097) | open | combinatorics | partial | 6 | binary_decision | discovery_standard | 3 | — | 1 | 0 |
| [1100](https://www.erdosproblems.com/1100) | open | number_theory | promising | 5 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1101](https://www.erdosproblems.com/1101) | open | number_theory | blocked | 4 | exact_or_characterisation | deep_backlog | 5 | — | 0 | 0 |
| [1103](https://www.erdosproblems.com/1103) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1104](https://www.erdosproblems.com/1104) | open | graph_theory | partial | 7 | open_ended_estimate | discovery_high | 4 | — | 0 | 0 |
| [1105](https://www.erdosproblems.com/1105) | proved | graph_theory | known_resolution | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1106](https://www.erdosproblems.com/1106) | open | number_theory | partial | 4 | mixed_or_unspecified | deep_backlog | 3 | — | 0 | 0 |
| [1107](https://www.erdosproblems.com/1107) | open | number_theory | partial | 3 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [1108](https://www.erdosproblems.com/1108) | open | number_theory | blocked | 3 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1109](https://www.erdosproblems.com/1109) | open | number_theory | partial | 6 | open_ended_estimate | discovery_standard | 4 | — | 0 | 0 |
| [1110](https://www.erdosproblems.com/1110) | open | number_theory | partial | 5 | binary_decision | discovery_standard | 3 | — | 0 | 0 |
| [1111](https://www.erdosproblems.com/1111) | open | graph_theory | blocked | 4 | mixed_or_unspecified | deep_backlog | 5 | — | 0 | 0 |
| [1112](https://www.erdosproblems.com/1112) | open | combinatorics | counterexample | 9 | binary_decision | resolution_audit | 1 | — | 0 | 0 |
| [1113](https://www.erdosproblems.com/1113) | open | number_theory | promising | 4 | binary_decision | deep_backlog | 3 | — | 0 | 0 |
| [1117](https://www.erdosproblems.com/1117) | open | analysis | partial | 3 | exact_or_characterisation | deep_backlog | 3 | — | 0 | 0 |
| [1119](https://www.erdosproblems.com/1119) | independent | analysis | independent | 9 | binary_decision | closed_watch | 0 | — | 0 | 0 |
| [1120](https://www.erdosproblems.com/1120) | open | analysis | blocked | 5 | open_ended_estimate | deep_backlog | 5 | — | 0 | 0 |
