# OPG 五题反例搜索执行方案

制定日期：2026-07-28

## 执行结论

本轮同时保留五题，但不平均撒算力。前 48 小时采用四个 worker：

1. `OPG-401`：先取得可完整复核的阶数下界；
2. `OPG-37271`：多重图最小阶线和三次多重图发现线并行推进；
3. `OPG-145`：从首个未知层 `Δ=5` 开始；
4. `OPG-348` 完成校准后，切到 `OPG-611, k=4, n=16`。

机器有 32 个逻辑 CPU，但总内存只有 7.6 GiB。并发上限固定为 4，每个
worker 以 RSS 约 1.2 GiB 为调度警戒线，至少留 2 GiB 系统余量。任何 timeout 都进入
hard queue；hard queue 未清零时，不允许写“已穷尽到 n”。

## 时间预算

| 问题 | 首轮调度 CPU·h | 预计墙钟 | 本轮必须交付 | 终止/升级闸门 |
| --- | ---: | ---: | --- | --- |
| `OPG-37271` | 120 | 30–48 h | 全部次三次多重图到 12 阶；全部三次多重图至少到 18 阶、目标 20 阶；SAT 着色逐图复核 | 6 色 UNSAT 立即停扫并双重认证；timeout>1% 或相邻阶中位耗时增长>10倍则改编码 |
| `OPG-401` | 70 | ≤48 h | 双连通、无三角、平面、`Δ≤3` 图至少完整到 17 阶，目标 18 阶；随后 24 h 结构变异 | 完成 18 阶且结构搜索 24 h 无候选，或连续两阶难度不再上升 |
| `OPG-145` | 134 | ≤72 h | 经证明归约后的候选到 10 阶；5-正则到 14 阶；`δ≥4` 到 11 阶；48 h hard-seed 变异 | 任一 UNSAT 转证明链；上述三层完成且 hard queue 清零后停止蛮力 |
| `OPG-348` | 224 | 3–6 d | 精确整数 evaluator；高 girth 三次图到 22 阶；命名 snark/随机族；generalized Petersen transfer-DP 原型 | 单图>30 s 或 memo>1 GiB 时停止一般 deletion–contraction；多项式根界闸门须等根隔离器实现后才启用 |
| `OPG-611` | 344 | 5–10 d | 首个可能阶 `n=16` 的 497 个缺边图四分片 SAT/CEGAR；候选的 `PACK4` UNSAT 证明 | 单分片>10^6 packing cuts、总计>160 CPU·h 或 proof>20 GiB 时升级对称破缺，不裸推 `n=17` |
| **合计** | **892** | 约 9–10 d（4 worker） | 每题均有可恢复状态、候选证书合同和明确负结果边界 | 每 24 h 重排一次，而非无条件烧完预算 |

“CPU·h”是累计调度预算，每 24 小时按进程 CPU 时间核账并决定是否释放下一阶段；
各 runner 的 `--wall-seconds` 只是单次启动的失效保护，不能相加解释成可用预算，
也不是操作系统级 CPU/RSS 强制配额。只有前一阶段通过正确性回归且吞吐稳定，
后一阶段预算才释放。

`campaign-plan.json` 对每个阶段标注 `implementation_status`。标为
`planned_no_runner` 的预算只是预留，必须先补齐生成器、独立判定、测试和完成判据，
才允许进入调度；当前结果不暗示这些后续阶段已经执行。

## OPG-37271：次三次多重图的 star-6 边染色

原命题允许 loopless multigraph；旧执行器只扫简单标号图到 6 点，因此不能复用
其“搜索边界”。采用两条互补线：

- 最小阶严格线：
  `geng -cq -D3 n | multig -q -D3 -m3 -T`；
- 反例发现线：
  `n=2` 时用 `geng -cq -d1 -D3 2`，`n≥3` 时用
  `geng -cq -d2 -D3 n`，再接 `multig -q -r3 -m3 -T`。

任意次三次反例可嵌入三次多重图，而 star-6 可染性对子图遗传，所以第二条线对
“是否存在某阶反例”的无界搜索是完整的；但扩张会增加顶点，因此“三次图扫到
`N` 阶”不能推出“所有 `N` 阶以下次三次图均无反例”。有限最小阶边界只能由
第一条线给出。两条生成命令中的 `-c` 也无损：不连通反例至少有一个反例分量。

CNF 为每条边一热 6 色、共端边异色，并对每个边身份明确的四边简单路/四圈及
每对颜色禁止交替 `a,b,a,b`。平行边保留不同 edge id。SAT 模型由独立 Python
checker 检查；UNSAT 才是候选，并需静态 CNF、CaDiCaL DRAT/LRAT、独立 proof
checker 和第二套回溯器。

安全剪枝只采用经过审计的定理条件，如 `mad(G)<5/2`。对一篇声称解决简单图
情形的 2026 年论文，初步审计发现其完美匹配“距离 2 冲突图”分类可能漏掉
`C4`（`Q3` 给出测试实例），且附录代码未明显执行最终着色；在补齐定理页码、
最小复现脚本和源码哈希前，只把它记为审计疑点，绝不作为安全剪枝或原猜想反例。

## OPG-401：`χ_c≤20/7`

生成器为：

```text
geng -q -Ctd2D3 n | planarg -q
```

`-C`、`δ≥2` 是无损的：圆染色可在割点处平移后拼接，最小反例可取一个 block。
再剔除二部图和 `Δ≤2` 图。判定器使用 `(20,7)` support-CNF：

```text
¬x[u,c] ∨ x[v,c+7] ∨ ... ∨ x[v,c+13]   (mod 20)
```

每个顶点恰一色，固定一个根为 0。SAT 映射逐边检查循环距离 7…13。候选需同时
保存 graph6、平面 rotation system、CNF、proof、哈希，并用独立 Z3 编码复核。

## OPG-145：`a'(G)≤Δ+2`

`Δ≤4` 已知，故只搜 `Δ=5` 和 7 色。主生成层：

```text
geng -q -C -d2 -D5 n
```

这里的 `δ≥2` 与 `-C` 是无损归约：叶边可在删去叶点后的着色上选一个未占用色
扩回；不同 block 的着色可作全局颜色置换，使割点处的入射边颜色互异，而任何
双色圈完全位于单个 block。

过滤 `Δ=5`，并剔除 3-sparse 图；正确方向是：若每条边至少一端度数不超过 3，
已有定理保证 `Δ+2`。保留条件因此是至少存在一条边的两个端点度数都不小于 4。

判定采用 lazy cycle cuts。先求 proper 7-edge-colouring；若两色诱导子图含圈，
加入阻断该具体交替圈的子句并增量重求。找到无双色圈的模型即为阴性见证；最终
静态 CNF 若 UNSAT，则足以证明不存在无环 7-边染色。主层之外依次搜索 5-正则、
`δ≥4`、随机 5-正则和 degree-preserving 2-switch 邻域。

## OPG-348：`Φ(G,11/2)>0`

原命题定义域是每个 2-edge-connected graph。当前完整枚举只覆盖其中
3-edge-connected、cubic、girth≥6 的有限子族；其阶数结果不能外推成原命题的
一般负边界。

对每个状态定义

```text
r = |E|-|V|+c(G)
N(G) = 2^r Φ_G(11/2) ∈ Z.
```

全程 bigint：

- 普通非桥非环边：`N(G)=N(G/e)-2N(G-e)`；
- 环：`N(G)=9N(G-e)`；
- 桥：`N(G)=0`；
- 分量相乘；
- 度 2 点压缩不改变 `N`。

内部状态必须支持 contraction 产生的平行边。小图由独立 spanning-subgraph 公式
复核。第一候选族是 3-edge-connected、cubic、girth≥6 图；再进入 generalized
Petersen、I-graph、snark、voltage lift 和 transfer-DP。已知 `G(119,7)` 的完整
多项式作为高阶回归 oracle，而不是反例。

## OPG-611：Bermond–Thomassen 的 `k=4`

利用 `k=3` 的已知定理得到无损归约：

- 可删弧至每点出度恰为 7；
- 反例不能含 directed 2-cycle，否则删去该圈后仍有最小出度 5，可再取三个圈；
- 因而反例是 oriented graph；
- `n=15` 只能是 7-regular tournament；Bang-Jensen、Bessy 和 Thomassé 已证明
  最小出度至少 `2k-1` 的 tournament 含 `k` 个点不交 3-圈；
- 首个可能阶为 `n=16`。

在 `n=16`，底层无向图等于 `K16\H`，其中 `H` 恰有 8 条边；非同构 `H` 只有
497 个，按目录索引模 4 拆成数量为 `125/124/124/124` 的 shard；这只近似平衡
对象数，不保证求解时间均衡。master SAT 约束每点出度 7、强连通，并加入必要
条件：每个 directed triangle 必须被某个外点完全支配；每个 directed 4-cycle
必须有外点支配至少三个圈点。

CEGAR 每次对一个定向精确查找四个点不交圈。找到 packing 就加入“这些圈弧不能
再次同时出现”的合法 cut；若找不到，则生成固定图的 `PACK4(D)` CNF。每个颜色
类非空，所选点在本色中恰有一入一出，且顶点至多属于一个颜色，因此 SAT 当且
仅当存在四个点不交有向圈。`PACK4(D)` UNSAT 才是候选。

### OPG-611 hard-pass 升级

首批 hard queue 的剖析显示，绝大多数时间耗在 master SAT，而不是 `PACK4`、
短圈枚举或 proof：不少实例在任何 CEGAR cut 之前就耗尽一小时。已新增不改动
原四分片源码哈希的独立 hard runner，使用以下可验证增强：

- 对缺边图 `H` 的 automorphism 群递归取逐点稳定子；每一步只在存在显式
  automorphism 交换允许边两端时固定该边方向。497 个 `H` 均可安全固定 3–8
  条单位弧，中位数 5 条；每条 witness permutation 均写入元数据并独立验证。
- `PACK4` 的四个颜色类按最小顶点严格递增，消去恰好 `4!` 个颜色标号，不改变
  SAT/UNSAT；候选仍由未加颜色破缺的原始 `PACK4` 公式独立重放。
- 每个 packing block 沿 `Aut(H)` 轨道作受限 BFS。每个轨道像本身仍是四个
  点不交有向圈的阻断，因而是逻辑有效 cut，而不只是 WLOG 约束；跨轮全局去重，
  每个 master 模型至多加入 1,024 条。
- 若已有 `t=1,2,3` 个点不交圈、顶点并为 `S`，任何反例必须有某个
  `x∉S` 满足 `|N⁺(x)∩S|≥2t+1`。否则 `D-S` 的最小出度分别至少为
  `5,3,1`，可由已知 `k=3`、`k=2` 和基本有向圈定理补足四个圈。hard runner
  对短圈二/三 packing lazy 加入精确 reified-threshold CNF，并同时限制完整
  packing 数和 DFS 节点数。
- 精确出度 7 给出
  `a(S,V-S)=7|S|-binom(|S|,2)+e_H(S)`。除目录 index 0 的
  `K1,8 ⊔ 7K1` 外，所有对象的任意度数可行定向都自动强连通；hard runner
  只接收 `Δ(H)≤7`，index 0 留给原始已认证流程。

120 秒 A/B 中，index 2 获得 7 个 master 模型并加入 7,168 个轨道 packing
cuts、28 个 residual cuts；公式为约 1.67 万变量、19.5 万子句。旧流程在同一
对象累计 458,752 个简单 packing cuts 后仍 timeout。index 13 取得一个模型并
加入 1,024 个轨道 cuts；index 12 和 20 即使加入 6/7 条单位弧，Glucose 与
MiniSat 在 120 秒内仍卡在首个 master，因此后两类必须用长时 solver portfolio，
不能把短基准误报成排除。

首轮 20 分钟长跑随后完成：index 2 取得 15 个 master 模型，加入 15,360 个
packing 轨道 cuts、60 个 residual cuts 和 1 个 4-cycle cut；index 32 取得
3 个 master 模型，加入 3,072 个 packing 轨道 cuts、12 个 residual cuts 和
1 个 4-cycle cut。两者均在预算耗尽后保留为 timeout，没有反例候选；这验证了
增强 cut 的低膨胀特性，但尚未形成排除结论。

## 证书和停止规则

结果分三级：

1. **A：反例候选**——主判定 UNSAT/非正，立即停止扩阶，双编码、双求解器、
   独立 proof checker、哈希和最小化全部通过后才能对外称“反例”；
2. **B：范围明确的严格负边界**——只对写明的输入族，规范生成计数闭合、所有
   实例有已复核见证且 hard queue 为空，才称“该输入族到 n 阶无反例”；
3. **C：次级突破**——发现文献算法或证明中的可复现缺口，只报告该缺口，不把它
   混同于原猜想反例。

每个 runner 原子写 checkpoint，并把 timeout/unknown 单独保留。运行产物置于
被 git 忽略的 `artifacts/opg_breakthrough/`；策略、预算和可重复命令保留在本目录。

## 首轮执行快照

更新时间：2026-07-29 10:10（Asia/Hong_Kong）。

- 三个新 runner 的专项回归 30 项、连同既有首批图测试共 47 项通过；软件测试
  只证明实现通过已写 oracle，不构成数学负边界。其中 OPG-611 的真实 CaDiCaL
  DRAT 证明已由
  `drat-trim` 独立验证。新 checkpoint 合同同时哈希源码、生成器/求解器及动态
  库、配置和有序输入目录。
- `OPG-37271` 的历史校准线完整跑完 2–12 阶全部次三次多重图，共 94,761 个，
  全部返回 star-6 SAT、无 timeout；该旧线未持久化着色见证，故只记为校准边界。
  持久化见证的三次多重图线已完整到 16 阶，共 36,093 个；18 阶仍在运行。
- `OPG-401` 的历史校准线已完整到 16 阶，共 126,897 个有效搜索对象全部 SAT、
  无 timeout；17 阶仍在运行。旧线未持久化映射，暂不标成最终证书边界。
- `OPG-145` 已完整跑完 7–9 阶：生成 48,787 个图，6,774 个由 3-sparse 定理
  安全过滤，余下 42,013 个全部保存无环 7-边染色且 hard queue 为空。所有
  42,013 份见证已由不调用 SAT 求解器的 Python checker 全量重放通过。
- `OPG-348` 的 girth≥6、3-edge-connected cubic 图已完整跑完 14–22 阶：
  各阶 `1,1,5,32,385` 个，共 424 个，全部精确 `N(G)>0` 且无 timeout；
  当前 evaluator 已对 424 个 numerator、cycle rank 和图族条件全量重放一致。
- `OPG-611` 的 497 项有序缺边图目录及四分片合同已闭合，四个 worker 均已
  启动。当前完成 `14/13/1/3` 项，共 31 项：11 项由 master CNF 排除，20 项
  进入 hard queue；当前无反例候选。第二代 hard runner 的 32 项专项回归通过；
  index 2 与 32 的首轮 20 分钟 orbit/residual 长跑均完成并仍为 timeout。
  telemetry 只用于状态观测，不冒充可恢复 checkpoint。

“历史校准边界”与“证书边界”严格分开：旧进程的实现指纹与当前源码不同，
且部分事件没有持久化见证；它们可以指导选题和吞吐估计，但不会被包装成最终
可发表的穷尽性结论。后续扩阶全部使用新目录和 checkpoint v2 合同。

## 主要来源

- Star edge-colouring 原始进展与低 `mad` 结果：
  [arXiv:1701.04105](https://arxiv.org/abs/1701.04105)；有缺口的近期声明
  [Fernando–Athapattu](https://jnsfsl.sljol.info/articles/12645/files/697c971d2e448.pdf)；
  仍将多重图问题列为猜想的
  [AIMS Mathematics 2026](https://www.aimspress.com/article/doi/10.3934/math.2026124)。
- Acyclic edge-colouring 的 3-sparse 边界：
  [arXiv:2501.11281](https://arxiv.org/abs/2501.11281)。
- OPG-401 原问题页：
  [Open Problem Garden 401](https://garden.irmacs.sfu.ca/comment/reply/401)。
- Flow polynomial 问题：
  [Mohar P0301](https://www.sfu.ca/~mohar/Problems/P0301FlowPolynomial.html)；
  高阶回归多项式来源 [arXiv:1009.4062](https://arxiv.org/abs/1009.4062)。
- `k=3` 的三个点不交有向圈定理：
  [SIAM J. Discrete Math.](https://epubs.siam.org/doi/10.1137/080715792)；
  tournament 情形见 Bang-Jensen、Bessy、Thomassé 的
  [Journal of Graph Theory 论文](https://onlinelibrary.wiley.com/doi/10.1002/jgt.21740)。
