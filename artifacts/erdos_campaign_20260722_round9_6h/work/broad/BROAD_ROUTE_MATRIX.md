# Erdős 21 题第九轮：全覆盖路线矩阵

日期：2026-07-22（Asia/Hong_Kong）

本矩阵记录本轮对全部 21 题的覆盖。它刻意把“严格新定理”“等价重述”“方法
障碍”和“尚未完成的设想”分开。主目标始终是原题闭合；只有改变主阶/主指数或
闭合核心子问题、并通过独立 QA 的结果才可能触发 SCI-Q2 门槛。

## 逐题矩阵

| 题号 | 本轮实际攻击/复核 | 本轮最强结论 | 距原题最近的硬缺口 | 判定 |
|---:|---|---|---|---|
| 25 | 把 profinite first-kill forest 压到整除链 | 任意指定剩余类、`n_i|n_{i+1}` 时自然密度存在，且为 `1-sum_{i in I}1/n_i` | 一般 forest 在 `n_i<=X` 前可有线性多个有效新原子，周期端点误差不能求和 | 严格全参数子类；OPEN |
| 143 | 在 primitive fibre 中保留 `gcd(a,b)` 与 `lcm(q,r)` 的耦合，尝试 Möbius 局域化 | 旧 bracket 恒等式及大 GCD incidence 正确；共同 numerator gcd 还自动与 `qr` 互素 | 对薄 fibres 的 Möbius 边界项和跨分母 Carleson 和；totient 因子不足以产生分母可和性 | 严格局部；OPEN |
| 148 | 复核大素数只落在晚端分母的唯一残余类，尝试按 slack 与模 `p` 的 divisor progression 平均 | 小 slack、`p|w` 及前两种 allocation 已有幂次节省，旧链无新错误 | 最晚 allocation 中大 slack 的除数同余平均；逐点 divisor bound 恰失去所需幂次 | 路线集中；OPEN |
| 256 | 把 residue-chain 的“至少若干项”改成整数根重数矩问题 | `(1-u)^m|f in Z[u]`, `f!=0` 蕴含 `sum c_j^2>=2m`；故 `E(P)>=2m_qS_q` | 需证明某个 `q` 强迫 `m_qS_q/n` 无界，或分类所有方向同时取小的指数多重集 | 严格加强；OPEN |
| 301 | 复核近邻因子等价和 fractional Hall，尝试用规范表示稀疏化右端拥塞 | 固定内带典型点有许多表示不等于存在低拥塞全局收费 | 同一高端点可被许多低端点重复使用；需从 Maier--Tenenbaum 的分块证明抽取有容量的规范边 | 严格归约；OPEN |
| 325 | 不再追求硬腔逐点 coercivity，改审计零锥 dyadic tube 的平均签名账本 | Euler 等双四次幂射线确认点态路线不可修；平均目标必须直接节省一整幂 `P` | 对零层锥管的整数点总质量/横截 determinant estimate，且仍需独立重建预印本大纤维分类 | 旧路线无误但失效；OPEN |
| 332 | 检查能否以 additive-basis、粗增长或 sparse spectrum 替代复现性 | 平方数已否定 additive-basis 捷径；历轮零密度精确差谱构造仍正确 | 必须提出真正在局部模式上施加复现、又严格弱于正上 Banach 密度的自然条件 | 路线尸检；开放式问题未完成 |
| 377 | 在 radical/totient 重述上尝试 base-`p` 递降 `n -> floor(n/p)` | 缺素数条件递归等价于末位在下半区且 `p` 对商继续缺失；没有消去全深度 | 不同 `p` 产生不同商，不能用一个标量归纳汇总；仍缺 distinct-small-prime weighted sieve | 精确接口；OPEN |
| 539 | 同时测试高能量父层、稀疏曲面和非坐标边界三条逃逸路线 | 稠密 payload、Boolean 关系、suspension、单纯形薄层四类障碍彼此兼容 | 构造保持 `eta(G_i)>=exp(-O(i))` 且所有正正交象限投影仅平方根量级的显式族 | 多路线 no-go；OPEN |
| 635 | 把估值--奇部链用于单个完整 lower fibre 及固定 valuation 层 | 独立 fibre 有 `r` 个互异不越界 canonical 奇邻点；同层 canonical 碰撞图完全分类为无分叉有向路径 | 跨层真碰撞 `U(24)=L(54)=27`；需 proper-divisor 邻点的全局增广链 | 严格局部；原渐近已知，精确加强未完成 |
| 679 | stopping-line 重组、超小倾斜、增长矩、Hölder/SOS/随机 thinning 四路并攻 | 完整周期超多项式稀疏；低导子区间传递已到 `D=X exp(-2 logX log_3X/log_2X)` | 剩余是极高导有符号尾与继承起点相位的关联；任意平移的统一 suffix 黑箱已有严格 CRT 反例 | 本轮最接近原题；FULL TRANSFER OPEN |
| 686 | 对偶数半长度做 2-adic 单系数转移与 Cartier 试探 | 已严格覆盖 `v2(l)<=2`；首个缺失层还得 `C_(4s)` 对奇 `s>=3` 被 8 整除，并完成 `l=8,16` 孤立精确估值 | 统一除幂仍远未到目标 `2s-v2(s!)`；一般 Cartier 倍增及变化 `l` 的高度控制均缺 | 严格无限子族；OPEN |
| 776 | 直接攻击全 `r` Macaulay carry，并测试简单二项包络归纳 | colex 构造与两点悬挂仍正确；简单 rank-independent envelope 加 `r` 后产生正 residual shadow，不能闭合归纳 | 需跟踪长 Macaulay carry，证明第 6 层界 (8)/端点比较 (14) 对全部 `r` 成立 | 高价值单引理未证；OPEN |
| 788 | 从共同母集证书转向依赖删点模式的 matching vertex-cover 压缩 | 高于半密度 proper-GAP 分支已闭合；半密度处单个和有指数多个最小删点模式 | 构造只有 `n^{O(1)}` 或 `exp(o(s))` 种的多和联合证书，而非枚举 `2^{Theta(s)}` 模式 | 路线边界；OPEN |
| 827 | 完整分类等半径 `K_{2,2,2}`，再做全局与单双曲线计数 | 立方恰为同一矩形双曲线上三组中心反足对；全局 `<N^3/24`；固定双曲线内的半径曲面不可约且非群型，故每线 `O(m^{12/7})` | 对所有双曲线的富线求和仍是 `O(m^2)`，不能误写成全局 `N^{19/7}`；尚无 rainbow 主指数/对数增益 | 本轮最强几何分类；OPEN |
| 934 | 把左右差集 normal form 接近群/可解群归纳，复核 quasirandom 分支 | 交集目标与对偶不增长式正确；有限群扫描没有可外推性 | 商群归纳只给投满商，不能填满交换子纤维；需 quadratic intersection 或 fibre saturation | 核心非交换缺口；OPEN |
| 950 | 从 fixed bounded gap 改成 endpoint-weighted prime tuple 和 dyadic shell functional | Abel 恒等式和 count-only barrier 均正确；普通 Maynard “至少 m 个”不能保证 reciprocal yield | 需保留坐标权的 sieve 正性，或同时命中趋多 dyadic backward shells | 新素数相关输入缺失；OPEN |
| 952 | 从固定有理走廊尝试增长方向族与环形墙 | 任意固定有限走廊族不能承载无限 bounded-step Gaussian-prime path | 路径可不断换斜率；独立 CRT 墙的模数为 `exp(O(R log R))`，没有位置控制 | 严格子类；OPEN |
| 963 | 统一 AP-window 宽度与回绕次数，审计 universal residue decoder | 单模数每活跃层必损失 `log_2k-O(1)`；容量引理还推广到任意有限阿贝尔直积解码群 | 必须利用实际可达回绕/零 fibre 数值或全局相关，机械增加模坐标无效 | 架构 no-go；OPEN |
| 1063 | 阻止继续刷新同一下界，比较上下界闭合所需尺度 | `n_k >=(1-o(1))k^2/log k` 仍是严格论文级下界，但与指数型构造上界不匹配 | 主攻应转向多项式构造上界或指数型下界；再改善下界常数不会估计正确阶 | 既有 Q2 候选；原题 OPEN |
| 1083 | 把小缺陷反射接入中缺陷质量、轴铅笔和点--面 incidence | 小缺陷质量撤离、轴铅笔收费；正确控制 Rudnev 的共线面参数 `kappa<2n/Q`；高-`Q` 临界层强制几乎线性复合域及含 `n^{2/5-o(1)}` 点的正半径圆柱 | 作用域不在复合变换下不变；低-`Q<=sqrt n` 层仍需加权 incidence，或需利用富圆柱结构 | 严格高-`Q` 桥；尚无距离指数增益 |

## 本轮新路线为何没有提前停止

1. #679 的超小倾斜把完整周期问题压得极强，但完整周期模数远大于所需区间；
   “方差趋零”不能跨过 `Q/X`，所以不是候选完整证明。
2. #827 已完成一个真正的六点构型分类，且把固定色立方计数常数从临时的
   `1/4` 降至 `1/24`；阶仍为 `N^3`，没有导出 `n_k` 新指数。
3. #686、#256、#1083 都是可复用的严格定理，但尚未改变各自官方问题的主阶
   或核心开放断言。
4. #1063 的既有二次除对数下界仍值得写论文；本轮没有把上下界的指数鸿沟
   缩到可称“原题估计”的程度。

## 下一轮应避免的重复投入

- #1063：只把同一 prime-band 下界再提高一个常数；
- #1083：继续优化近完整反射面的线性常数，而不进入高缺陷 carrying layer；
- #963：只调单模数窗口宽度；
- #539：再次更换 Cartesian/Boolean/suspension/坐标薄层参数；
- #788：在半密度以下继续寻找对所有删点模式共同有效的单个和；
- #325：把其他符号腔的点态正性原样搬到零层锥附近。

本文件在统一预算边界前仍可因各工作流的新结果修订；最终状态以
`ROUND9_SYNTHESIS.md` 和各组 `RESULT.json` 为准。
