# OPG-1757 九阶有限层：数学范围与运行审计

日期：2026-07-29

## 结论

四个 `geng -c 9 19:36 i/4` 分片已经全部闭合：

| shard | 目录项 | 已计算 | 非违反 | timeout | violation |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0/4` | 26,861 | 26,861 | 26,861 | 0 | 0 |
| `1/4` | 28,101 | 28,101 | 28,101 | 0 | 0 |
| `2/4` | 37,477 | 37,477 | 37,477 | 0 | 0 |
| `3/4` | 27,028 | 27,028 | 27,028 | 0 | 0 |
| 合计 | **119,467** | **119,467** | **119,467** | **0** | **0** |

因此，在下面限定的语义和计算信任边界内，本次工作填补了九顶点、19--36
条边的全部连通简单图层。结合 Grimmett--Winkler 2003 年的已发表计算定理，
可以得到：

> 标准的“两个不同边”版本，在所有连通分量都至多有九个顶点的有限简单图上，
> 已获得计算性验证。

特别地，这覆盖所有至多九顶点的有限简单图。它不是任意阶猜想的证明。

## 命题语义

设 \(\mathcal F(G)\) 是 \(G\) 的所有森林边集，并记

\[
N=|\mathcal F(G)|,\quad
N_e=|\{F\in\mathcal F(G):e\in F\}|,
\]

以及类似的 \(N_f,N_{ef}\)。对两个**不同**的边 \(e\ne f\)，目标不等式等价于

\[
N\,N_{ef}\leq N_eN_f.
\]

本次计算的范围是：

- 有限简单图；源目录没有自环或重边；
- \(e\ne f\)；
- 在全部森林上的无权均匀分布，即权参数为 \(1\)；
- 只检查 edge-negative-association，也就是边对负相关；没有检查由不交边集
  支撑的一般递增事件之间的完整 negative association。

Grimmett--Winkler 原文明确假设图无自环、无重边，并明确写出 \(e\ne f\)。
仓库抓取的 OPG 网页句子漏写了后一条件。若按网页字面允许 \(e=f\)，则一条边
图已经反驳它：

\[
\Pr(e\in F\mid e\in F)=1>\Pr(e\in F)=\tfrac12.
\]

所以本次搜索遵循的是原始文献中的标准命题，而不是这个有缺字的字面版本。

## 从连通图归约到任意图

令

\[
G=G_1\sqcup\cdots\sqcup G_r .
\]

一个边集是 \(G\) 的森林，当且仅当它在每个 \(G_i\) 上的限制都是森林。因此
\(\mathcal F(G)\) 与 \(\prod_i\mathcal F(G_i)\) 双射，均匀森林在连通分量间
精确分解。

若 \(e,f\in E(G_k)\)，令 \(A=\prod_{i\ne k}|\mathcal F(G_i)|\)，则

\[
(N,N_e,N_f,N_{ef})
=A\,(N^{(k)},N_e^{(k)},N_f^{(k)},N_{ef}^{(k)}).
\]

总图的不等式两边都有因子 \(A^2\)，所以它与 \(G_k\) 内的不等式完全等价。

若 \(e\in E(G_i)\)、\(f\in E(G_j)\) 且 \(i\ne j\)，则乘积分解直接给出

\[
N\,N_{ef}=N_eN_f;
\]

不同连通分量中的边精确独立。故只枚举连通图没有遗漏反例。

## 与已发表范围的拼接

Grimmett--Winkler 的 Theorem 1.5 声明：uniform forest 的边对负相关性已经由
直接数值计算验证于

1. 所有至多八顶点的简单图；
2. 所有九顶点且至多十八条边的简单图。

一手来源：

- G. R. Grimmett and S. N. Winkler, *Negative association in uniform
  forests and connected graphs*, arXiv:math/0302185，
  <https://arxiv.org/abs/math/0302185>；
- 定理及计算范围见论文 PDF 第 2--3 页，
  <https://arxiv.org/pdf/math/0302185>。

现在对任意简单图作如下分类：

- 连通分量顶点数至多八：由该定理覆盖；
- 九顶点连通分量、边数至多十八：由该定理覆盖；
- 九顶点连通分量、边数十九至三十六：由本次 119,467 个非同构连通图覆盖；
- 两条边落在不同连通分量：由上节的乘积分解取等号。

这也说明结论不只适用于总顶点数至多九的图，而适用于任意多个、每个至多九
顶点的连通分量的并。另一方面，只要有一个连通分量含至少十个顶点，本次有限层
就没有给出一般排除。

2003 年低阶范围在这里作为已发表计算定理使用；本仓库没有重放其原始程序。

## 运行和目录证据

联合审计文件：

`artifacts/opg_breakthrough/certified/opg1757-n9-m19-36-six-hour/audit-v1.json`

- `campaign_complete=true`；
- `generated=events_replayed=nonviolating=119467`；
- `timeouts=violations=0`；
- 文件 SHA-256：
  `7a8e98c4cc62eb63df3545de2cef52a6f5a36e8f828ed790347bfa6432c11961`；
- `geng` SHA-256：
  `9730b53764bdb28ecd2fdf755fafbc76992050f39e5ea19bb7d91433a26583e9`；
- production implementation fingerprint：
  `d122d3d2c5be3bdd0f3ad3edbeb5ce477b46131ea1a68bf596d79a31accd9a50`；
- auditor SHA-256：
  `93c1ed12d4250c223298129356bc60ad06f80639ba840d8e6166ea4bce66c254`。

审计器重新生成每个分片，逐 index 和原始 graph6 字符串绑定事件，检查目录内
唯一性、连通性、边数范围、state 闭合、工具与动态库哈希、边编号和端点，以及
四个计数所形成的乘积和 margin 的精确整数恒等式。

另行以同一已哈希 `geng` 作了不分片与四分片并集核对。固定 `LC_ALL=C` 排序后，
两者均为 119,467 行，且 SHA-256 同为

`b08e12a7a417184b29c66cfe84e9b9a188438da55cc408819c632caf2ec60538`。

四分片合并后重复 graph6 数为零。这补足了联合审计器本身没有显式比较
“四分片集合”和“不分片集合”的合同缺口；它仍然依赖同一个 `geng` 生成器，
不是第二个图同构枚举实现。

专项测试：

`PYTHONPATH=src python3 -m pytest -q tests/test_opg_uniform_forest_search.py tests/test_opg_uniform_forest_run_audit.py`

结果为 `17 passed`。

## 计数器的静态数学审计

production 计数器的状态是“当前边位置 + 原顶点集的规范分区”。对下一条边：

- 删除分支总是合法；
- 当两个端点处在不同分区块时，加入分支合并这两个块；
- 当端点已在同一块时，该边在收缩 minor 中是环，只能删除。

按剩余边数归纳，这个 deletion--contraction 递推精确计数森林。预先收缩指定边
集合 \(S\) 后再次运行同一递推，精确得到包含 \(S\) 的森林数；若 \(S\) 成环则
返回零。固定边在扫描到自身时已经成为环，因此不会被重复选择。

`statistics()` 计算 \(N\)、每个 \(N_e\) 和所有无序不同边对的 \(N_{ef}\)。
`strongest_edge_pair()` 用整数交叉相乘最大化

\[
\frac{N\,N_{ef}}{N_eN_f}.
\]

所有分母在本目录中为正。因此，只要有一个边对违反不等式，最大比值边对也必然
违反，production 事件就会标为 `violation`。静态审查没有发现这条逻辑链中的
数学错误。

另有一套逐边 forward partition DP，即
`opg_uniform_forest_twin_transfer.forward_partition_distribution`，其状态推进
方向和 production deletion--contraction 不同。它对每个边数
\(m=19,\ldots,36\) 各取一个分层样本，共十八个样本；另检查四个 shard
尾样。事件所记录边对的 \((N,N_e,N_f,N_{ef})\) 全部逐整数匹配，零 mismatch。
最后出现的 \(m=35\) 实例 `H^~~~~~`、边对 `[4,13]` 得到

\[
(N,N_e,N_f,N_{ef})
=(8\,003\,950,1\,618\,820,1\,618\,820,323\,958),
\]

与事件完全一致。这些是分层样本交叉核验，不是 119,467 个事件的全量第二计数。

## 剩余信任边界和加固建议

联合审计应称为
`execution_evidence_verified_with_counting_trust_boundary`，不能称为全量独立
数学复算，原因是：

1. 每个事件只保存 production 选出的一个边对，没有保存完整 per-edge 和
   per-pair count matrix；
2. 审计器检查保存计数的整数一致性和基本组合界，但没有独立重新计算这些计数；
3. “保存的边对确为该图最强边对，因而没有未保存的违反边对”仍依赖已哈希的
   production 实现及上述静态代码审计；
4. 分层 forward-DP 和逐子集核验提高了置信度，但仍只是样本。

还发现两个非阻断的联合合同加固点：

- 联合审计目前比较四 shard 的 `geng_sha256`，但没有在代码中比较四份
  `geng_dependency_sha256` 映射；本次四份映射实际逐项相同；
- 联合审计没有直接重放不分片目录来证明 shard 间不重不漏；本次已用上面的
  sorted-catalogue SHA 和零重复检查补上该运行证据。

部分事件的最强边对来自不同 graphic-matroid block，margin 恰为零。这是结构性
独立，不是反例；因此 `minimum_reported_margin=0` 不能用来描述严格近边界前沿。

## 推荐对外表述

推荐：

> 对标准的不同边、有限简单图、无权 uniform-forest 边对负相关猜想，我们用
> 已哈希的精确 deletion--contraction 实现完成了九顶点、19--36 边全部
> 119,467 个连通非同构图的零 timeout 计算，未发现违反。执行审计重新生成并
> 逐事件绑定了完整目录；但因事件只保存 production 选出的边对，完整 pair
> matrix 没有被全量独立重算。结合 Grimmett--Winkler 2003 年对至多八顶点以及
> 九顶点至多十八边的已发表计算定理，并利用连通分量乘积分解，可称为“所有
> 连通分量至多九顶点的有限简单图上的计算性验证”。

不得表述为：

- “证明了 uniform forests 的一般负相关猜想”；
- “独立验证了 119,467 个图的全部边对计数”；
- “覆盖了重图、自环、加权版本或一般事件 negative association”；
- “按 OPG 网页字面允许 \(e=f\) 的版本仍然开放”。
