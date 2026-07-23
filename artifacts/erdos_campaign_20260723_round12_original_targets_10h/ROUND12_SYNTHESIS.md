# Erdős 21 题第十二轮终态汇总

日期：2026-07-23（Asia/Hong_Kong）

## 1. 预算与总判定

四个并行工作流统一计费区间为 `2026-07-23T06:28:31+08:00` 至
`2026-07-23T08:58:31+08:00`，每组登记 9,000 秒，累计 36,000 秒，即
10 agent-hours。证明期只使用低优先级单核诊断，峰值低于 WSL 8 个逻辑 CPU
的 50%；证明搜索在冻结准备阶段停止，硬边界后只作既定验证、敌意 QA、哈希
和汇总。

终态计数：

- 原始命题完整证明或证否：**0**；
- 改变公认主阶或主指数：**0**；
- 达到本轮 SCI 二区提前停止门槛：**0**；
- 发现已接受/已发表证明失效：**0**；
- 严格新阶段推进集中于：#256、#635、#679、#776、#827、#1083；
- 其余 15 题完成原量词路线复审，但没有新的严格主结果。

因此本轮没有把条件定理、有限点、内部路线反例、almost-all 结论或结构浓缩
冒充原题闭合。

## 2. 最强严格成果

### #776：全程 carry 缺口压到 rank 5 的固定常数界

令 `V=M-3`，并置

\[
F_q={V+1\choose q}+{V-1\choose q-1}+{V-2\choose q-2}.
\]

对所有 `V>=379`，原始 colex 起点的末端成功条件被严格化为

\[
E_3\le {V+2\choose3}+28
\quad\Longleftrightarrow\quad
E_5-F_5\le {376\choose2}=70500.
\]

等号和加一失败均已逐项核对。对 `V>=70501`，它又等价于显式 rank-6 下界

\[
F_6-E_6\ge {V-4\choose2}-{70496\choose2}.
\]

这把“控制全部 Macaulay 层”的模糊任务缩成一个标量统一界；该界本身仍未
证明，所以 #776 仍开放。`M=150000` 计算在冻结前中断、没有完整输出，未被
采用；`M=75000` 仍只是已核验的原始起点安全定点。

### #1083：rich rigid-motion 定理与两类轴障碍的 `9/20` 浓缩

对三维 `n` 点、距离数 `D`，当 `R` 大于球面容量常数倍时，同定向
`R`-rich 刚体运动数满足

\[
|G_R|\ll {n^4(D\log n)^{4/3}\over R^3}.
\]

临界代入给 `n^(9/5+o(1))`。结合全星无理转折计数，得到
`n^(3/5-o(1))` 个同运动三反射表示，并抽出 `n^(1/5-o(1))` 个不同、
`n^(1-o(1))`-rich 的无限阶旋转。

对其反射陪集作完整三分：reflection/共面轴、glide/平行轴、唯一不动点/共点
轴。后两支分别用仿射复数模型和射影四元数模型化为无重数点线关联，从而强迫
至少 `n^(9/20-o(1))` 张结构面及同规模共面/共球点见证。现有容量是
`n^(3/5+o(1))`，仍差 `n^(3/20)`；reflection 支还有平方级无理角尖锐模型。
所以没有改变 #1083 主指数。

### #679：增长 block 障碍、远端临界值与 Lau 权重提取

- Goudout 的正式短区间定理给：在 `H=exp(C log_2X log_3X)` 且
  `(1+eps)C>1` 时，几乎每个端点都在 `[H,2H)` 出现违例；还能对某个不可
  显式的 `G(X)->infinity` 对角延伸。稀疏无限例外仍可能存在。
- 对 exact-level cutoff 算到三、四阶：三阶主系数为正、四阶主系数为负，
  精确定位的是 Goudout 方法阈值，不是原题真值边界。
- Hardy--Ramanujan far union-bound 的临界幂为
  `D_0=(1+eps)/eps`；固定临界常数处符号失败，而乘一个趋于 1 的显式修正
  因子可恢复正余量。这仍是 growing-cutoff almost-all 定理。
- 对 Lau 权重使用 `min(R_k,tau(n+k))` 得 `max nu=x^o(1)`，从而提取至少
  `x^(0.4-o(1))` 个无权见证；但其 `C log k` 阈值仍弱于 #679，且不能强制
  与远端好集相交。

Tenenbaum 任意固定维给“快于任意固定对数幂”的候选稀疏性，早期轮次已经
记录；本轮只复核其无固定除数量词，明确不重复计为新成果。

### #256：two-support 的 signed-residue 完整分类

若奇素数 `p` 恰漏掉 `s` 个指数且条件分裂处于低能量 two-support 分支，则
外部 residues 在 `(+/-)` 商群上的直方图当且仅当呈现“一类 `2t+1`、其余
每类 `2t`”。反向充分性也由群环恒等式证明。任意有限组素数的这些一维边缘
可由 CRT 同时实现，严格封死“只并列 marginal histogram 即得矛盾”的路线；
`t=0` 分支另有精确递归 `E(pc_1,...,pc_m,b)=2E(c_1,...,c_m)`。尚缺覆盖任意
指数多重集的 universal bridge，所以没有新的通用 `f(n)` 主界。

### #635：proper Hall 化为带算术标号的 bicircular 核

奇部为两个不同奇素数的左点 `x=2^apq` 被精确化成交换边
`q(2^ap-1)--p(2^aq-1)`。对标号两两不冲突的边集，proper-neighbour Hall
恰好等价于每个分量为伪森林；最小反例只可能是 `theta`、`figure-eight`、
`dumbbell` 三类双圈核。

相交边得到任意 valuation 的完整局部冲突判据，固定层锐化为“公共端点删去
的两素数之差恰等于 `2^a`”。同时找到公共右点 `9471` 上四条两两不冲突边，
严格否定所有纯局部度数证明。固定层和混合层闭路又得到乘子乘积与双矩账本；
它们尚未排除三类双圈核，更没有覆盖 prime-square、高阶奇部和 canonical
增广，故 #635 原题仍开放。

### #827：超过 `1/4` 的两类强制障碍

若想得到 `N^(1/4+eta)` rainbow 子集，则必须排除一个支持
`N^(7/4-5eta)` 三角形的 #104-rich 半径，或排除
`N^(1-4eta)` 个中心各自携带同规模 pinned tangent matching 的结构。后者
还强迫固定 `j` 个中心有 `N^(1-4j eta)` 个公共端点；伙伴可落在公共集外且
半径可不同，所以尚无新的 `n_k` 指数。

## 3. 21 题逐题终态

| 题号 | 第十二轮终态 |
|---:|---|
| 25 | 任意 activated system 的 signed/Carleson 收费仍缺；OPEN |
| 143 | 跨 denominator fibre 的可积有符号控制仍缺；OPEN |
| 148 | 临界大素数窗相关平均未建立；无新主界；OPEN |
| 256 | signed-residue iff、CRT marginal no-go、`t=0` 递归；OPEN |
| 301 | 低拥塞规范表示/容量 Hall 仍缺；OPEN |
| 325 | `3<=k<=10` 零锥整数点总质量仍缺；OPEN |
| 332 | 弱 syndetic 差集条件的自然边界仍缺；OPEN |
| 377 | 多素数 digit-depth 无同步势；OPEN |
| 539 | 次多项式因子未改变；OPEN |
| 635 | semiprime bicircular 核、局部冲突与路径账本；原 `t=2` 仍 OPEN |
| 679 | 新增长 block/far 方法阈值与权重屏障；第一问仍 OPEN |
| 686 | Cartier 局部分支未回接全体自然数 `N`；OPEN |
| 776 | 原端点 iff rank-5 常数 70500；该界未证；OPEN |
| 788 | 多和证书联合压缩仍缺；OPEN |
| 827 | #104-rich / 多中心 matching 相图；无新 `n_k` 指数；OPEN |
| 934 | quotient fibre saturation 仍缺；OPEN |
| 950 | endpoint-weighted sieve 仍缺；三问均未闭合 |
| 952 | 固定步长无限 Gaussian-prime 路径/全屏障均未得；OPEN |
| 963 | reachable signed-span 跨层亏损仍缺；OPEN |
| 1063 | 本轮没有不同增长级新界；OPEN |
| 1083 | rich-motion 与 `9/20` 两支浓缩；主指数与全维目标仍 OPEN |

## 4. 发表门槛与下一断点

本轮没有一项可诚实标为“已具备 SCI 二区主论文”。最接近可独立发展的，是
#1083 的 rich rigid-motion 定理与 `9/20` 两分支浓缩、#776 的 rank-5/rank-6
精确等价归约，以及 #256 的 signed-residue iff 分类；前者尚缺主指数节省和
穷尽式新颖性审计，后二者仍分别缺统一残差界与 universal bridge。

最窄后续节点是：

1. #776：证明 `E_5-F_5<=70500`，等价地证明大参数 rank-6 二次下界；
2. #1083：对双富来源面给 `o(n^(9/20))`，并对 reflection 支给
   `o(n^(1/5))` 的共面轴富旋转界；
3. #679：控制 moving entropy cutoff 以上的有符号高 conductor 尾，或取得
   真正匹配原阈值的确定性短区间高 `omega` 定理；
4. #635：排除或构造标号独立的三类算术双圈核。

## 5. 证据入口

- `work/geometry/REPORT.md`、`work/geometry/INDEPENDENT_QA.md`；
- `work/679/REPORT.md`、`work/679/INDEPENDENT_QA.md`；
- `work/macaulay_pte/REPORT.md`、`work/macaulay_pte/INDEPENDENT_QA.md`；
- `work/broad/BROAD_REPORT.md`、`work/broad/BROAD_QA.md`。

各工作流的 `RESULT.json`、`SOURCE_MANIFEST.json` 与 `SHA256SUMS` 构成机器
可读终态。第十一轮已提交并推送为 `947654a`；第十二轮冻结证据包随包含本
文件的研究提交纳入仓库。
