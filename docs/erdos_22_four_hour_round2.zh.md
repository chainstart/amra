# Erdős 22 条候选路线第二轮四小时续攻

> 生成日期：2026-07-19。每题 14,400 秒是硬上限，不是必须耗尽的目标；本报告只把相对第一轮的新增推导计作推进。

## 104 条证据问题是否意味着题目全部重开

不是。这里必须区分“证明有数学缺口”“题目原本就仍开放”和“状态/题面范围标签不精确”。在本次核验材料覆盖的 80 条机械归入非开放集合记录中，只有 #358 发现了足以使当前公开闭合证明不能完成定理的明确数学缺口：公开稿的中频论断存在具体参数反例，作者已承诺修订但尚无新版。因此 #358 目前应视为闭合尚未核实、仍需攻关；这仍不等于定理已被证伪，证明可能可以修补。

#114、#488 实际一直是 `falsifiable`/OPEN，只是被机械误收进这 80 条，并不存在一份后来被推翻的闭合证明；#783 的 `SOLVED` 对应后来修订的渐近题面，不等于冻结版本要求的逐个有限精确分类；#1022 的数学和 Lean 代码证明的是否命题，正确闭合方向应是 `DISPROVED (LEAN)`，不是重新开放。其余异常主要是题面条件或版本变化、复合题只解决一部分、Lean 把深层输入公理化、Lean 证明旧题面，或证据尚未同行评审。这些问题降低状态标签或证据成熟度的精度，但不会自动推翻已有数学证明。

24 条官网仍 OPEN 的冲突中，没有发现第二个像 #358 那样已定位公式反例且获作者承认的闭合证明漏洞。#520、#335 是先前分析错误；#638、#701、#918 是形式化或题面范围问题；#550、#1070 是近期声称的成熟度或复合题范围问题；#920 更像状态同步滞后。

| 审计集合 | 分类结果 | 对开放性的含义 |
|---|---|---|
| 80 条机械归入非 OPEN | 50 closed_verified；25 closed_scope_caveat；1 evidence_incomplete；4 status_or_statement_mismatch | #358 因现有闭合稿的具体缺口而应暂视为未核实；#114、#488 原本就仍开放；#783 是版本范围差；#1022 应改闭合方向。不能把这四类情形统称为“原证明全部失败” |
| 24 条官网 OPEN 冲突 | 12 literal_false_intended_open；6 still_open_correct；2 initial_analysis_wrong；2 recent_claim_unverified；1 independence_scope_mismatch；1 likely_status_stale | 它们本来就是 OPEN；审计主要澄清为何仍开放或官网是否可能滞后，不存在把 24 份原证明一并推翻的问题 |

## 覆盖与运行质检

| 指标 | 数值 |
|---|---:|
| 预期路线 | 22 |
| 已完成 | 22 |
| 缺失 | 0 |
| 累计题目运行时间（相加） | 7.53 小时 |
| 单题最长 | 2728.5 秒 |

### 第二轮结论分布

| 结论 | 数量 |
|---|---:|
| route_advanced | 21 |
| route_refuted | 1 |

route_advanced 只表示得到新的严格中间结论；route_blocked 表示未越过明确障碍；route_refuted 表示本轮所攻路线被否定。只有精确题面的全部量词闭合时才允许候选完整证明或候选反例标签。

### 重点推进及其边界

> 本轮严格 QA 后没有任何一条被标为官网原题的候选完整证明。#1063 是完整子定理证明，但因官网题面更开放，按统一标签规则记为 route_advanced。

| # | 本轮最强推进 | 不能据此声称的范围 | 独立复核 |
|---:|---|---|---|
| 1063 | 令 $L_k=\operatorname{lcm}(1,\ldots,k-1)$、$p$ 为最小的 $p>k/2$ 素数；证明 $n_k\le((2p-k+1)/p)kL_k=o(kL_k)$，并由 BHP 得 $O(k^{0.525}L_k)$。 | 完整闭合 FormalConjectures 的 better_upper 子定理；官网开放式“Estimate n_k”仍未闭合，且尚非 Lean 或已发表论文。 | PASS |
| 963 | 把渐近下界定量加强为 $f(n)\ge\log_2n-O((\log\log n)^2)$；另给出 $F(4)\ge27$。 | 误差仍发散，不能推出官网逐点猜想 $f(n)\ge\lfloor\log_2n\rfloor$。 | PASS |
| 950 | 证明局部极值只需检查 $f(p)$、$f(p+1)$，并得无条件 $\limsup f(n)\ge10651/7410$。 | 三个原极限问题均未解决；更高常数中依赖未评审预印本的部分已单列而未算成熟结论。 | PASS_WITH_MINOR_REPAIRS |
| 148 | 候选新界 $f_5(m,n)\ll_\varepsilon n^\varepsilon(n^2/m)^{446/289}$，继而改善 $F(k)$ 的同底数系数。 | 是经过内部复核的候选新上界，不是原问题的完整闭合，也尚未发表。 | PASS_WITH_MINOR_REPAIRS |
| 788 | 无条件证明 $f(n)=\Omega(\sqrt{n\log n})$，并精确得到 $f(13)=7,f(14)=8,f(15)=8$。 | 原题询问 $f(n)\le n^{1/2+o(1)}$，所以上界方向仍开放。 | PASS |
| 776 | 对所有 $r\ge4$ 证明 $g(2r+4,r)\le2r$，故 $n_0(r)\ge2r+4$。 | 这是新的统一下界，不是对阈值的精确确定。 | PASS |
| 827 | 得到 $n_k\ge(24\sqrt{\log2}+o(1))k^2(\log k)^{-1/2}e^{-4\sqrt{(\log2)(\log k)}}$。 | 只推进下界；匹配上界和原题整体仍开放。 | PASS |
| 325 | 证明 $f_{4,3}(x)\gg_\varepsilon x^{0.704143-\varepsilon}$。 | 只覆盖 $k=4$ 的部分改进，距离目标 $3/4$ 且其他 $k$ 均有缺口。 | PASS |
| 635 | 严格确定 $F_2(3000)=1506$、$F_2(5000)=2506$，并给出独立左 Hall 的有限刻画。 | 拟议的私有邻点定理仍未证明，不能外推为完整渐近解。 | PASS |
| 301 | 证明指定 punctured-box/完整赋值方法类的最优权重常数为 450/403。 | 这是固定方法类的最优性与障碍证书，并未改善官网原问题的最佳界。 | PASS_AFTER_TEXTUAL_REPAIR |
| 952 | 构造并交叉核验步长上界 D=4 的有限 Gaussian moat 证书。 | 只闭合 D=4 子情形；任意有界步长的原题仍开放。 | PASS_WITH_MINOR_REPAIRS |

## 新增结果总表

| # | 第一轮 | 第二轮 | 用时 | 最主要新增 |
|---:|---|---|---:|---|
| 952 | route_advanced | route_advanced | 1268.1 秒 | [第二轮新增] 严格反驳了更强的“高度400条带中存在 x-单调屏障”命题：两种实现均在 x=20断路，而真实证书含728753次回退。 |
| 1083 | route_blocked | route_advanced | 797.6 秒 | [第二轮新增] 第一轮“锐余维2界可统一闭合所有 d≥3”的路线在 d=3 严格失效：其平衡计算暗中使用了假的输入 f_1(m)≥m^{2-o(1)}；精确值是 f_1(m)=m−1。 |
| 25 | route_refuted | route_advanced | 823.5 秒 | [第二轮新增] 若有限周期幸存密度 d_K 的极限 d_*=0，则 A 不仅有对数密度，而且有自然密度 0。 |
| 117 | route_advanced | route_refuted | 996.4 秒 | [第二轮新增] 对任意奇素数 p 和任意奇数 t≥1，严格构造 W(2^t−1,p) 中大小 p^t+1 的 partial ovoid。构造的点对配对精确等于 N(b−a)，不是启发式或仅经有限枚举确认。 |
| 143 | route_advanced | route_advanced | 905.3 秒 | [第二轮复核加固] KLL 的块内 E₂ 平方质量估计已经存在；第一轮真正缺少的是 E₃ 的质量敏感增益以及跨尺度小 bracket 对的算术选择，不能笼统称为“加强 Proposition 2.15”。 |
| 148 | route_advanced | route_advanced | 1216.1 秒 | [第二轮新增] 严格证明带同余的无阈值加权和 S(m,n) 满足 f_5(m,n)≤S(m,n)≤5f_5(m,n)；这加固了 lifting 的组合含义，同时表明上一轮 next theorem 基本等价于直接改善 f_5。 |
| 256 | route_advanced | route_advanced | 808.6 秒 | [第二轮新增] 对任意 \varepsilon>0，命题“所有纯乘积均满足 \sum_jc_j^2\ge(2+\varepsilon)n”按原量词为假；六因子显式乘积已经达到 Tang 界的等号 \sum c_j^2=2n。八因子也有独立等号见证。 |
| 301 | route_advanced | route_advanced | 556.6 秒 | [第二轮新增] 证明加权穿孔盒定理：若 C⊂ℕ₀³ 且平移族 {c+B*:c∈C} 两两不交，其中 B*=[0,4]×[0,2]×[0,1]∖{(0,0,0)}，则 Σ_{(r,s,t)∈C}2^{-r}3^{-s}5^{-t}≤450/403。 |
| 325 | route_advanced | route_advanced | 949.7 秒 | [第二轮新增] 对每个 ε>0，严格得到 f_{4,3}(x)≫_ε x^{0.704143−ε}。这里 0.704143=(6−3.183428)/4；正整数表示是题面非负整数表示的子集，P=⌊(x/3)^{1/4}⌋闭合了 x 截断。 |
| 332 | route_advanced | route_advanced | 669.3 秒 | [第二轮新增] 若 δ=d*(A)>0 且 0<ε≤δ²，则下 Banach 密度满足 d_B^-(R_ε)≥ε/(δ−δ²+ε)。这严格强于上一轮 next theorem 仅要求 R_ε syndetic；假设、ε 范围及严格阈值均已逐项闭合。 |
| 377 | route_refuted | route_advanced | 842.5 秒 | [第二轮新增] 得到精确最高位必要区间：若 \(k=\lfloor\log_p n\rfloor\) 且 \(p\nmid\binom{2n}{n}\)，则 \((2n+1)^{1/(k+1)}\le p\le n^{1/k}\)；两端点及整数不等式已核对。 |
| 539 | route_advanced | route_advanced | 1249.5 秒 | [第二轮新增] 精确求得基带三项：\|B_W\|=W³−W²/2+3W/2，\|D(B_W)\|=(5W²−3W+4)/2，\|B_W−B_W\|=4W³−3W²+3W−1；第一轮只有相应粗界。 |
| 635 | route_advanced | route_advanced | 2728.5 秒 | [第二轮新增] 对 t=2，冲突边 {x,y}（x<y）等价于 gcd(x,y)=y−x≥2；亦即约分后的 y/x 是两个连续正整数之比。 |
| 679 | route_advanced | route_advanced | 842.8 秒 | [第二轮新增] 对任意固定 ε>0、K>e^e，记 N_{ε,K}(X) 为不超过 X 且对所有 K≤k<n 满足题面不等式的 n 数量，则 N_{ε,K}(X)=O_{ε,K}(X/log₂X)。特别地，任何可能的正解序列自然密度为 0。 |
| 686 | route_advanced | route_advanced | 2181.0 秒 | [第二轮新增] 若 N=4、k=5 有合法解，则中心变量必满足 y=n+3≥16 且 y+5≤x<4^{1/5}y<4y/3。 |
| 776 | route_advanced | route_advanced | 1895.0 秒 | [第二轮新增] 对 n=2r+4 的全部量词得到五层残余等式：a_{N−4+j}+c_{N−j}=r（0≤j≤4），其中 N=r+3；特别是 a_{N−2}+c_{N−2}=r，且两侧都有 r 个残余3集、至少 r−1 个补3覆盖和 r 个补4覆盖。 |
| 788 | route_advanced | route_advanced | 1477.8 秒 | [第二轮新增] 对所有充分大的 n，存在绝对常数 c>0 使 f(n)≥c√(n log n)。这严格加强第一轮的 Ω(√n) 下界，但仍与 n^{1/2+o(1)} 上界猜想相容。 |
| 827 | route_advanced | route_advanced | 1268.7 秒 | [第二轮新增] 对充分大 k，n_k≥(24√(log 2)+o(1))·k²/√(log k)·exp(−4√((log 2)(log k)))。它强化第一轮同一构造的次主项，但仍不确定 n_k 的阶。 |
| 934 | route_refuted | route_advanced | 1489.6 秒 | [第二轮新增] 对任意简单 r-正则 H，若 diam L(H)≤3，则对每条边 uv，集合 V(H)\(B_{≤2}(u)∪B_{≤2}(v)) 必为独立集；若 c=\|N(u)∩N(v)\|，进一步有 \|E(H)\|≤2r^3-2r^2+rc+1≤2r^3-r^2-r+1。该界弱于已知 (3/2)r^3，但严格揭示仅使用单条固定边的“远集独立”约束仍停留在首项常数2。 |
| 950 | route_advanced | route_advanced | 1100.8 秒 | [第二轮新增] 精确证明 \[\liminf_{n\to\infty}f(n)=\liminf_{p\to\infty}f(p),\qquad \limsup_{n\to\infty}f(n)=\limsup_{p\to\infty}f(p+1),\]其中 \(p\) 遍历素数；并证明第三问等价于只检查峰值子序列 \(f(p+1)=o(\log\log p)\)。 |
| 963 | route_advanced | route_advanced | 1341.8 秒 | [第二轮新增] 对充分大n，f(n)≥log₂n−O((log log n)²)。相较第一轮的(1−o(1))log₂n，这把未指定的o(log n)缺陷严格压到O((log log n)²)；误差仍发散，不能推出floor(log₂n)。 |
| 1063 | route_advanced | route_advanced | 1704.0 秒 | [第二轮新增] 令 p(k) 为最小的 p>k/2 素数、L_k=lcm(1,…,k−1)。充分大 k 时存在 1≤t≤2p−k+1，使 n=t kL_k/p 的失败集精确为{0}。因此 n_k≤[(2p−k+1)/p]kL_k=o(kL_k)。 |

## 逐题第二轮记录

### #952

- 第一轮障碍：原题需要对每个有限 D 都排除无限分支。周期筛路线为此需要随 D 构造模数或周期理想 m_D，使 B_{m_D} 的商图没有任何非零绕数。加入新素因子只会删点，因而不会重新产生无限分支，但目前没有定理保证有限多个新因子能击中全部绕行通道。CRT 局部空洞也不给出这种全局、周期一致的击中性质。
- 第一轮下一定理：最清晰的下一有限定理是独立机核 Gethner–Stark 第2节的 D=4 实例：对 m=7113990，证明 B_m 在差向量平方模≤4的图中无非零绕数闭路。由于 m² 枚举不可行，需要按 m=2·3·5·13·17·29·37 的 CRT 分解构造压缩商图/可检查证书；这将验证周期筛路线确实可从√2推进到2，并给一般 D 的算法接口。
- 第二轮用时：1268.1 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：攻击并完成上一轮提出的 m=7113990、D=4 周期筛机核：不用 m² 枚举，而按 Gethner–Stark 的高度400半周期条带构造可独立验证的拓扑屏障；同时先证伪更强的单调路径版本。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_MINOR_REPAIRS；范围：复核第二轮结果中 m=7113990、D=4（欧氏步长不超过2）的有限分量结论：流式重验 clear-site 路径证书、重跑两种条带洪泛、核对两条环面同调屏障及48个 Gaussian 素数例外；不复核、也不声称解决任意有限步长的原 Gaussian moat 问题。
- 复核方式：证书可从当前源码逐字节重建，13,850,303个压缩段内格点出现（计重数）全部通过独立算术判定；端点、接合、矩形范围和步数均正确。把水平、竖直两条本质屏障圈与有限周期商图的覆盖空间引理结合，足以推出 G_4(B_m) 的每个提升分量有限；加入恰好48个例外 Gaussian 素数后仍然有限。因此 D=4 子结论成立。结果文件已明确 full_solution_claim=none，并没有把它误写成 #952 的完整解。需要修补的是“嵌入图”和“任意起点”两处措辞，以及最好显式写出有限周期商图的覆盖引理；这些均不改变结论。
- 证据边界：该PASS只认证一个已有文献方向上的D=4有限子定理及其新可复现证书，不是论文同行评审或形式化证明认证。它没有给出D随意增大时的模数、条带高度或屏障存在定理；#952仍开放。

#### 第二轮实际尝试

- **证伪 x-单调条带屏障**（refuted）：定义 B_m={x+iy:gcd(x²+y²,m)=1}。逐列动态规划，要求从18i出发的屏障路径只作竖直移动或令 x 增加1。；用“直接检验 x²+y² 模各有理素因子”和“检验列出的 Gaussian 线性因子”两种算术实现，均在 x=20 得到空可达集。最终证书实际含728753次向左回退。因此文献条带不能加强为单调屏障。
- **精确 clear-site 条带洪泛**（advanced）：令格点 c 为 clear，当且仅当 c∉B_m，并且 c 不是两个水平或竖直相距2的 B_m 点的中点。在 0≤x≤m/2、0≤y≤400 上对 clear 点的四邻接图作位图 scanline flood-fill。；从(0,18)出发到达(3556995,363)。norm 与 Gaussian-linear 两种生成器完全一致：发现26034821个竖直段、119363629个clear点，遍历哈希均为0x18615cb2e9c68b7d。
- **压缩路径的独立逐点验证**（advanced）：从洪泛树抽取5,014,502段压缩路径；另写Python验证器，不复用位图或因子判定，而直接以 math.gcd(x²+y²,7113990) 检查路径经过的每个格点。；验证了相邻段 |Δx|=1、接合高度一致、端点正确，并逐点核验13,850,303个竖直路径格点均为clear。证书SHA-256为faf07c260110b0d7f3f58cd5b392932512de51c88ec22516141be2093755774b。
- **从半周期路径闭合无绕数结论**（advanced）：把 D=4 的 B_m 图作直线实现，并在长度2边的全部交点处细分为周期有限1-复形；反射并投影到二维环面，再使用同调交数与有限覆盖图引理。；clear路径的单位线段与该细分直线实现不交。以 x↦m−x 反射得到同调类(1,0)的补集闭走，从中抽取本质简单圈；以 x↔y 得类(0,1)的简单圈。细分商图任一连通分支 H 的环路均避开两圈，故 π₁(H)→ℤ² 的像为0；于是 H 的每个平面提升分支一层覆盖有限图 H，因而有限。原 B_m 图是该细分几何超图的子图，所以其提升分支也有限。

#### 第二轮新增严格进展

- [第二轮新增] 严格反驳了更强的“高度400条带中存在 x-单调屏障”命题：两种实现均在 x=20断路，而真实证书含728753次回退。
- [第二轮复核加固] 对 Gethner–Stark 的 m=7113990、D=4 构造给出了新的可复现机核：半周期clear路径从(0,18)到达(3556995,363)，并由独立Python程序逐点验证13,850,303个路径格点。
- [第二轮新增] 闭合了文献计算到上一轮“无非零绕数”表述之间的拓扑缺口：在长度2边交点细分后，两条同调基屏障圈与有限周期商图覆盖引理迫使 B_m 图的所有提升分支有限。
- [第二轮复核加固] 除 B_m 外的 Gaussian 素数仅为 m 的 Gaussian 素因子及其伴随，共48个点；D=4 图局部有限，加入这48个例外只能合并有限多个原有有限分支。因此步长≤2的真实 Gaussian 素数图没有无限分支。

#### 证伪与边界检查

- 允许差向量逐项检查为 (±1,0),(0,±1),(±1,±1),(±2,0),(0,±2)，恰为 0<N(δ)≤4；clear定义专门处理唯一可能穿过合数格点的长度2水平、竖直边。
- 单位clear线段不会在内部与长度1、√2或2的good线段相交：对角线与整数水平/竖直单位段只能在格点端点相遇，而端点不是good；长度2边穿过端点的情形已由中点条件排除。
- 路径不需要单调性；压缩证书明确记录728753次向左回退，防止用错误的逐列归纳替代洪泛。
- norm实现和Gaussian-linear实现对完整条带给出完全相同的计数、端点与遍历哈希；另以Python/gcd实现独立验证实际证书。
- m=2·3·5·13·17·29·37。其Gaussian素因子非伴随类数为1+1+2·5=12，连同四个单位倍数共48个例外，而非沿用m=130时的20个例外。
- 本轮结论只覆盖D=4。它既不是官网全部量词的反例，也不能通过“加入更多因子只删点”自动推出每个D均存在合适有限筛。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/monotone_moat.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/monotone_moat.cpp)：条带证书生成器，含norm与Gaussian-linear两种独立算术生成器、被反驳的单调DP及精确scanline洪泛。SHA-256: b595c0ca83a725ece3622fb194dd1e48c98fe61860bf70891b35b722a4ab6f19。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952 && g++ -O3 -std=c++17 -Wall -Wextra -pedantic monotone_moat.cpp -o monotone_moat && ./monotone_moat norm && ./monotone_moat linear && ./monotone_moat norm flood moat_path.recomputed.txt && ./monotone_moat linear flood；结果：两个单调运行均输出failed_x=20；两个洪泛运行均到达x=3556995、y=363，计数及哈希完全相同。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/moat_path.txt](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/moat_path.txt)：78,633,818字节的压缩clear路径证书，共5,014,502段。SHA-256: faf07c260110b0d7f3f58cd5b392932512de51c88ec22516141be2093755774b。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952 && sha256sum moat_path.txt；结果：路径从(0,18)到(3556995,363)，含728753次x方向回退。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/verify_moat_path.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952/verify_moat_path.py)：独立Python逐点验证器，直接调用整数gcd，不使用C++位图或线性因子逻辑。SHA-256: 2dd046084b0d18bc96c374555eccb8719935e8fb0323b52d1109f1194a894562。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/952 && python3 -m py_compile verify_moat_path.py && python3 verify_moat_path.py moat_path.txt；结果：verified=True；runs=5014502；checked_vertical_sites=13850303；backsteps=728753；endpoint=(3556995,363)。

#### 当前障碍

原题要求排除每个有限D。当前没有定理保证：对任意D，存在有限Gaussian素因子集合Π，使候选集 B_Π 的D步长图补集中出现同调类生成ℤ²的两条屏障圈。有限CRT空洞仍只控制局部平移形状；本轮D=4证书也没有给出随D增长的模数、条带高度或筛因子选择规律。

#### 下一精确定理

下一条最窄且可机核的有限定理是D=5版本：构造有限Gaussian模数M，使 B_M={z:gcd(N(z),N(M))=1} 的 N(δ)≤5 直线实现（在交点细分）补集中存在两条环面同调类组成ℤ²基的clear圈；或给出证明这种有限因子周期筛在D=5必然失败的绕数通道。该命题会检验本轮拓扑接口能否超越文献的步长2实例。

#### 第二轮证明记录

承接的第一轮事实

记 N(a+bi)=a²+b²。第一轮已经把原题化为：是否存在整数D，使Gaussian素数图 G_D 的边满足0<N(u−v)≤D且含无限分支；并提出核验m=7113990、D=4的周期筛实例。本轮不把第一轮的m=130计算或有限CRT空洞重新计为进展。

第二轮新增推导

取
\[
m=7113990=2\cdot3\cdot5\cdot13\cdot17\cdot29\cdot37,
\qquad B_m=\{x+iy:\gcd(x^2+y^2,m)=1\}.
\]
这与在ℤ[i]中筛去
\[
1+i,\ 3,\ 2\pm i,\ 3\pm2i,\ 4\pm i,\ 5\pm2i,\ 6\pm i
\]
的倍数等价。

令K为B_m上0<N(u−v)≤4的图的直线实现，并在长度2边的所有交点处细分为周期有限1-复形。一个格点c=(x,y)称为clear，若
\[
c\notin B_m,
\quad\neg[(x-1,y),(x+1,y)\in B_m],
\quad\neg[(x,y-1),(x,y+1)\in B_m].
\]
后两个条件恰好排除c位于长度2的水平或竖直K边内部。若两个clear点四邻接，则连接它们的单位格边与K不交：长度1边若重合便要求clear端点属于B_m；对角边只能在整数端点处相交；长度2边若穿过clear端点则违反上述中点条件。

精确洪泛在矩形
\[
R=[0,m/2]\times[0,400]\cap\mathbb Z^2
\]
中找到从(0,18)到(m/2,363)的clear路径P。独立验证器逐点核验了P的13,850,303个竖段格点出现（计重数；路径可回访）。以x=m/2反射P，得到从(0,18)到(m,18)且避开K的闭走，其在T²=ℝ²/mℤ²中的同调类为(1,0)。将闭走分解为简单圈；因纵坐标始终处于宽度远小于m的条带，总同调为(1,0)，故其中存在类(±1,0)的本质简单圈C_h。交换x,y得到类(0,±1)的C_v。

若γ是T²\(C_h∪C_v)内的闭路，因γ与两圈不交，代数交数给出
\[
[\gamma]\cdot(1,0)=0,\qquad [\gamma]\cdot(0,1)=0,
\]
故[γ]=0∈H_1(T²;ℤ)=ℤ²；在环面上这也就是其π₁像为0。将细分后K的有限环面商图的任一连通分支记为H。H中每条闭路都避开两圈，故π₁(H)到甲板群ℤ²的像为0；所以H的每个平面提升分支一层覆盖有限图H，含有限多个细分顶点和边。原B_m图是这个几何超图的子图，故其每个连通分支也有限。于是G_4(B_m)没有无限分支。

若Gaussian素数π不属于B_m，则π整除m的某个Gaussian素因子。非伴随因子共有12类，计入四个单位倍数共有48个Gaussian素数点。D=4时每点至多有12个允许差向量；把这48个点加入G_4(B_m)只能连接有限多个已有有限分支。因此真实Gaussian素数图在步长≤2时所有分支有限。

仍未闭合的缺口

原题的量词是“是否存在某个固定但任意大的有界步长可无限行走”；否定答案须对每个D构造屏障。本轮只独立机核了已由1997年论文声称的D=4实例。没有得到m_D的存在定理，也没有把局部CRT空洞升级为围住任意分支的全局屏障，所以不能声称解决原题。

来源成熟度与优先权

D=4结论的数学优先权属于Gethner–Stark 1997年第2节；本轮贡献只是提供原文未附的可复现证书和从条带计算到无绕数图结论的显式拓扑核验。Stumpenhusen 2024的arXiv v1摘要声称完整解答，但未取得可核查正文，且2026年官方题页仍列为open，故本记录不采用其声称。

#### 本轮核查来源

- [Erdős Problems #952](https://www.erdosproblems.com/952)；一手来源：true；核验：页面最后编辑于2026-04-08，仍标为 OPEN；题面要求存在一条无限互异 Gaussian 素数序列，并不指定起点，也不限定从原点出发。
- [Periodic Gaussian Moats, Gethner–Stark, Experimental Mathematics 6 (1997), 289–292](https://doi.org/10.1080/10586458.1997.10504616)；一手来源：true；核验：第2节第291页至292页的未编号构造取 m=7113990，筛去其 Gaussian 素因子；从18i出发，在 0≤x≤3556995、0≤y≤400 内追踪连通2-moat，并以 x=m/2 及 y=x 对称性延拓。本文没有公开程序或逐点证书。
- [On the Gaussian Moat Problem, Johann C. Stumpenhusen, arXiv:2401.08441v1](https://arxiv.org/abs/2401.08441)；一手来源：true；核验：v1摘要声称完整否定 Gaussian moat 问题；本轮仍只能从一手页面核到摘要，未取得可逐项审查的正文定理编号和证明。其后官方题页仍标 open，因此不采用该摘要作为定理。

### #1083

- 第一轮障碍：高重数颜色承载多数点对时，缺少一个对其并集进行局部支持分解并收费的定理。单色近极值稳定性太强、适用尺度太高；Solymosi–Vu 的现有余维递推又固有地损失固定幂。
- 第一轮下一定理：建议下一节点是如下“锐余维2非集中界”。固定 d≥3，P⊂R^d、|P|=n，令 m=max_H|P∩H|，其中 H 遍历余维2仿射平面。证明 |Δ(P)| ≥ n^{-o_d(1)} n^{(d²+d+2)/(2d²)} m^{-(d−1)/(2d)}. 另一方面平凡地有 |Δ(P)|≥f_{d−2}(m)。若归纳输入 f_{d−2}(m)≥m^{2/(d−2)-o(1)}，令 m=n^x，则两个指数分别为 A−bx 与 2x/(d−2)；最坏平衡点是 x=(d−2)/d，二者都恰等于2/d。该命题比 Solymosi–Vu Theorem 2.2 的 n 指数 (d+1)/(2d) 恰强 1/d²，并在格点上指数锐利。
- 第二轮用时：797.6 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：优先证伪第一轮提出的“锐余维2非集中界”及其作为全题归纳路线的充分性；检查各向异性格点和高阶距离矩；随后把幸存的高维部分缩成真正必要的最窄临界窗口，并为 d=3 单列正确的下一定理。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_AFTER_LOCAL_CORRECTIONS；范围：第二轮对第一轮统一归纳路线的审计、固定 q 胞腔推广、临界窗口缩减，以及长方格非反例检查；未证明或证伪 Erdős #1083 本身。
- 复核方式：独立逐式复算 d=3 平衡、固定 q 逐胞腔损失和长方格指数；修正后重跑 d=3..10、分母 12 的精确有理数枚举。
- 证据边界：原结果曾把总体标为 route_refuted，并在计算脚本中误写 2*a_1；现已改为 route_advanced、修正为 a_1+a_2，并在固定 q 推导中显式补入 (q-1) 与 epsilon_q。被否定的只是第一轮路线的统一充分性，#1083 仍开放。

#### 第二轮实际尝试

- **基维数 d=3 审计**（refuted）：把第一轮候选界及其声称的 d→d−2 归纳逐项代入 d=3。；候选第一项变成 D≫n^{7/9-o(1)}m^{-1/3}，但第二项只能使用 f_1(m)=m−1，而不是 m^{2-o(1)}。写 m=n^x，平衡 7/9−x/3=x 得 x=7/12，最多给 n^{7/12-o(1)}；7/12<3/5<2/3。因此即使候选不等式本身成立，它也不能闭合官网的 d=3 量词。
- **固定高阶一致元组**（blocked）：在 Solymosi–Vu 胞腔证明中把一致三元组替换成任意固定 q≥3 的一致 q 元组。；若 m 是余维2仿射平面最大交数，则同一球面上的 q 个互异点不可能共线；其等距中心集合包含于某个余维2平面，故重数≤m。逐胞腔使用 C(x,q)≥x−(q−1)，得到 N_{r,q}≥[n(n−1)−(q−1)(C_d n t r^{(d−1)/d}+2nr)]/m。对固定 q 取 r=ε_q(n/t)^{d/(d−1)}，其中 ε_q>0 充分小，遂有下界 Ω_q(n²/m)；胞腔上界为 O_{d,q}(n^q/r^{q−1})。消去 r 得 t(P)≫_{d,q}n^{(d+q−2)/(d(q−1))}m^{−(d−1)/(d(q−1))}。若 m=n^x，则指数为 1/d+(d−1)(1−x)/[d(q−1)]，在 0≤x≤1 时随 q 递减；q=3 已是该框架最强者。
- **各向异性长方格证伪**（advanced）：令边长为 K_1≥⋯≥K_d，并精确计算余维2平面最大交数；再做有理指数穷举及小参数仿射秩枚举。；任意余维2平面的方向空间存在一个满秩的 d−2 坐标投影，该投影在平面上单射，故 m≤∏_{i=1}^{d−2}K_i；坐标平面取等。若 K_i=n^{a_i+o(1)}，则 μ=log_n m=Σ_{i≤d−2}a_i≥(d−2)/d。候选右端指数不超过2/d；而最大的两条坐标轴给含 K_1K_2≥n^{2/d} 点的平面子格，Guth–Katz 给其至少 K_1K_2/log(K_1K_2)=n^{2/d-o(1)} 个距离。因此全部长方格族均非反例。
- **高维临界窗口缩减**（advanced）：假设 d−2 维目标已知，把 m=n^x 代入 Solymosi–Vu Theorem 2.2 的两个分支。；非集中分支指数 A_0−bx，其中 A_0=(d+1)/(2d)、b=(d−1)/(2d)，当 x≤(d−3)/(d−1) 时已至少2/d；低维分支指数 2x/(d−2)−o(1)，当 x≥(d−2)/d 时已至少2/d。故只剩宽度 2/[d(d−1)] 的窗口 ((d−3)/(d−1),(d−2)/d)。第一轮完整候选界在此窗口外是多余强化。
- **2026 年预印本完整性核验**（refuted）：检查其主定理证明中的量词，而不依据摘要或自我宣称。；Theorem 3.2 的证明只构造一族特殊点集。存在一个具有很多距离的配置既不给 f_d(n) 下界，也不给上界；因此该文没有闭合“每个 n 点集”这一量词。

#### 第二轮新增严格进展

- [第二轮新增] 第一轮“锐余维2界可统一闭合所有 d≥3”的路线在 d=3 严格失效：其平衡计算暗中使用了假的输入 f_1(m)≥m^{2-o(1)}；精确值是 f_1(m)=m−1。
- [第二轮新增] 对每个固定 q≥3，已严格推出一致 q 元组界 t(P)≫_{d,q}n^{(d+q−2)/(d(q−1))}m^{−(d−1)/(d(q−1))}；并证明在同一胞腔线性化方法内 q=3 对所有 m≤n 都最强，故提高固定矩阶不能补回缺失的1/d²。
- [第二轮新增] 在假设 f_{d−2}(s)≥s^{2/(d−2)-o(1)} 的 d≥4 归纳步中，真正未解的 m 范围精确缩为 n^{(d−3)/(d−1)+o(1)}<m<n^{(d−2)/d-o(1)}，其幂指数宽度为2/[d(d−1)]。
- [第二轮新增] 三维应改用余维1参数：若 h 是最大共面点数，Solymosi–Vu Theorem 2.1 与 Guth–Katz 给 D≫max{n/h^{2/3},h/log h}。因此三维只需桥接 h=n^y、1/2<y<2/3；这与第一轮错误使用的余维2归纳基不同。
- [第二轮复核加固] 对长方格 P=∏_{i=1}^d{0,…,K_i−1}，严格证明最大余维2平面交数恰为最大 d−2 条边长之积；解析证明及整数仿射秩枚举交叉一致，且该完整各向异性格点族不反驳候选界。

#### 证伪与边界检查

- f_1(m)=m−1 无渐近歧义：从最左点到其余 m−1 点已有 m−1 个不同距离；等差数列只有距离1,…,m−1，故取等。
- 一致 q 元组的重数界没有退化漏洞：q≥3 个同球面互异点不共线；其仿射张成维数至少2，所有等距中心满足至少两个独立线性垂直平分条件。
- 固定 q 推导只声称 q 为固定常数；逐胞腔损失带有因子 q−1，因而明确令 r=ε_q(n/t)^{d/(d−1)} 且 ε_q 依赖 q 充分小，没有把常数误写成对随 n 增长的 q 一致。
- 长方格最大交数的上界使用满秩坐标子投影的单射性，未假设余维2平面必须平行于坐标轴。
- 候选界本身尚未被反例否定；被否定的是它作为官网全部 d≥3 的充分归纳路线。
- arXiv:2002.00502v9 的范围核验落在证明正文第8–9页，而非仅凭摘要或官网状态判断。
- 计算部分使用两条独立检查：有理指数的穷举与闭式解析证书；小格点另用整数仿射秩和整数平方距离枚举，无浮点判等。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1083/candidate_bound_audit.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1083/candidate_bound_audit.py)：精确有理数穷举各向异性边长指数；独立输出解析 slack 证书；比较 q=3,…,8 的一致元组指数；对三、四维小长方格直接枚举平方距离及余维2仿射平面交数。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1083 && python3 -m py_compile candidate_bound_audit.py && python3 candidate_bound_audit.py --max-d 10 --denominator 12 --grid 2,3,4 --grid 2,2,2,3；结果：d=3,…,10 的全部有理组成均无负 slack，闭式证书精确为0；每个抽查 x 上 q=3 均支配 q=4,…,8。2×3×4 格与2×2×2×3格的最大余维2交数分别为4、6，与投影公式一致；平方距离数分别为12、7。

#### 当前障碍

路线有两个不可合并的阻塞点。其一，d=3 没有可用的 d−2 维最优基例；现有共面数递推在 h≈n^{3/5} 附近只给 n^{3/5}。其二，对 d≥4，即使假设低两维目标成立，仍缺少在极窄临界余维2交数窗口中的 n^{2/d-o(1)} 下界。Solymosi–Vu 的固定高阶一致元组推广严格不会改善三元组指数。

#### 下一精确定理

应拆成两个精确节点。（A）三维临界共面桥：对 P⊂R^3、|P|=n，令 h=max_{平面 H}|P∩H|；证明当 n^{1/2}≤h≤n^{2/3} 时 |Δ(P)|≥n^{2/3-o(1)}。区间外由 Theorem 2.1 与 Guth–Katz 已闭合。（B）高维临界余维2桥：固定 d≥4，并假设 f_{d−2}(s)≥s^{2/(d−2)-o(1)}；若 m=max_{codim H=2}|P∩H| 满足 n^{(d−3)/(d−1)}≤m≤n^{(d−2)/d}，证明 |Δ(P)|≥n^{2/d-o(1)}。这比第一轮要求对所有 m 证明带精确 m 幂的候选界严格更窄。偶数维可从 d=2 开始；奇数维仍必须先解决节点（A）。

#### 第二轮证明记录

一、承接的第一轮事实

沿用但不冒充本轮新结果的事实是：普通距离能量被 Lenz 型高重数距离支配；低重数截断分支已经闭合；Solymosi–Vu Theorem 2.2 给
\[
D\ge t(P)\gg_d \max\left\{n^{(d+1)/(2d)}m^{-(d-1)/(2d)},\ f_{d-2}(m)\right\},
\]
其中 m 是余维2仿射平面的最大交数。第一轮建议把第一项的 n 指数提高1/d²至
\[
A=\frac{d^2+d+2}{2d^2}.
\]

二、第二轮新增推导

首先检查归纳基。d=3 时 m 是最大共线点数，低维项为 f_1(m)=m−1，而非 m^{2-o(1)}。候选第一项成为 n^{7/9-o(1)}m^{-1/3}。若 m=n^x，它与 m 平衡于
\[
\frac79-\frac{x}{3}=x,\qquad x=\frac7{12},
\]
只给 n^{7/12-o(1)}，甚至弱于已知 n^{3/5}。所以“候选界+向 d−2 归纳”不能覆盖官网的 d=3；第一轮的统一路线在此被严格反驳。候选不等式本身仍未被证伪。

其次，尝试以更高距离矩修复三元组损失。记 t=t(P)。采用 Solymosi–Vu 的 r 胞腔分割；每胞腔含 O(n/r) 点。对固定 q≥3，胞腔内一致 q 元组总数至多
\[
N_{r,q}\ll_{d,q} r(n/r)^q=\frac{n^q}{r^{q-1}}.
\]
在每个以 v 为中心的距离球上，若各胞腔点数为 x_j，则
\[
\sum_j\binom{x_j}{q}\ge \sum_j(x_j-q+1)

after discarding negative terms. 与原证明相同地控制强、弱相交，并取足够小常数倍的
\[
r\asymp (n/t)^{d/(d-1)},
\]
可使所有球贡献 Ω_q(n²) 个带中心计数的一致 q 元组。q 个同球面互异点不能共线，故其等距中心集合包含于一个余维2仿射平面；每个无中心 q 元组至多被 m 个 v 计数。因此
\[
N_{r,q}\gg_q \frac{n^2}{m}.
\]
合并上下界并消去 r 得
\[
t(P)\gg_{d,q}
 n^{\frac{d+q-2}{d(q-1)}}m^{-\frac{d-1}{d(q-1)}}.
\]
写 m=n^x 后，其 n 指数等于
\[
\beta_q(x)=\frac1d+\frac{(d-1)(1-x)}{d(q-1)}.
\]
因0≤x≤1，β_q 随 q 单调不增，所以 q=3 已最强。由此严格排除了“只把三元组换成固定更高矩”这一自然修补。

第三，把高维所需命题缩到最窄范围。令
\[
A_0=\frac{d+1}{2d},\quad b=\frac{d-1}{2d},\quad m=n^x.
\]
假设 d−2 维目标成立，Theorem 2.2 的两个指数为 A_0-bx 和 2x/(d−2)-o(1)。前者达到2/d恰当且仅当
\[
x\le \frac{d-3}{d-1},
\]
后者达到2/d当
\[
x\ge \frac{d-2}{d}.
\]
所以只剩
\[
\frac{d-3}{d-1}<x<\frac{d-2}{d},
\qquad
\text{宽度}=\frac{2}{d(d-1)}.
\]
第一轮候选界对所有 m 给出精确 m 依赖，远强于闭合归纳实际所需。

第四，三维应改用共面数 h。Theorem 2.1 与平面 Guth–Katz 输入给
\[
D\gg \max\left\{\frac{n}{h^{2/3}},\frac{h}{\log h}\right\}.
\]
令 h=n^y；第一项在 y≤1/2 时达到 n^{2/3}，第二项在 y≥2/3 时达到 n^{2/3-o(1)}。故三维真正的下一节点是1/2<y<2/3的共面临界窗口，而不是错误的 d−2 归纳。

最后检查格点边界。对边长 K_1≥⋯≥K_d 的长方格，任意余维2平面存在一个满秩的 d−2 坐标投影，因此其格点交数至多 K_1⋯K_{d-2}，坐标平面取等。另一方面前两条轴形成 K_1K_2 点的平面子格；Guth–Katz 给至少 K_1K_2/\log(K_1K_2) 个距离。由于 K_1K_2≥n^{2/d}，整个各向异性长方格族都满足 n^{2/d-o(1)}，不能击穿候选。

三、仍未闭合的缺口

没有证明三维临界共面桥，也没有证明 d≥4 的临界余维2桥。更没有得到官网全题的证明或反例。固定高阶矩失败说明所需新输入必须利用胞腔内点集或多个距离颜色之间的额外几何结构，而非只提高一致元组阶数。

四、来源成熟度与潜在优先权

Solymosi–Vu 和 Guth–Katz 均为已发表工作的作者正文/arXiv版本，是本轮递推的可靠来源。2026年更新的 arXiv:2002.00502v9 尚不能作为解决文献：其证明量词明确是特殊构造，未覆盖任意点集。没有在检索到的一手来源中找到上述“临界窗口缩减”或固定 q 公式的精确独立陈述；它们是本轮从 Solymosi–Vu 证明直接推出的审计结论，但这里不主张文献优先权或可发表的新颖性。

#### 本轮核查来源

- [Erdős Problem #1083](https://www.erdosproblems.com/1083)；一手来源：true；核验：当前页面仍标 OPEN；精确题面覆盖所有固定 d≥3，并记录 f_3(n)≫n^{3/5} 及 d≥4 的固定指数缺口。
- [Near optimal bounds for the Erdős distinct distances problem in high dimensions](https://www.math.ubc.ca/~solymosi/sajatcikkek/distancesvu.pdf)；一手来源：true；核验：逐式复核 Theorem 2.1、Theorem 2.2。后者的低维项确为 t_{d−2}(m)；式(36)–(43)用胞腔内一致三元组得到 t(P)≫n^{(d+1)/(2d)}m^{−(d−1)/(2d)}。
- [On the Erdős distinct distance problem in the plane](https://arxiv.org/abs/1011.4105)；一手来源：true；核验：Guth–Katz 证明任意 N 个平面点确定 Ω(N/log N) 个距离，可作为 d=2 的归纳输入。
- [On the Erdős distance problem, arXiv:2002.00502v9](https://arxiv.org/pdf/2002.00502)；一手来源：true；核验：该预印本 Theorem 3.2 表面声称 n^{2/k−o(1)}，但证明第8–9页明确先“carefully choose”特殊点集，并以“for this construction”结束；这是存在型构造，不是对每个点集的下界，不能推出 f_k(n)。
- [Distinct Distances in Three and Higher Dimensions](https://doi.org/10.1017/S0963548304006091)；一手来源：true；核验：期刊页面的 Theorem 1.1 范围为三维 Ω(n^{77/141−ε})，并说明有相应 pinned-distance 结论及高维推论；没有覆盖目标指数。

### #25

- 第一轮障碍：完整周期交叠描述长期密度，却看不到 n≈n_i 处的“对角命中”。一般 Σ_i1/n_i=∞ 时，单块激活损失可为 1，且不能由该块造成的有限筛密度下降控制；尚缺允许坏块、但能跨尺度摊销的估计。
- 第一轮下一定理：令 B_K 为前 K 个完整剩余类的周期幸存集，密度 d_K，d_*=inf_Kd_K，并定义 ℓ_{K,j}=(log2)^{-1}Σ_{2^j≤n<2^{j+1}, n∈B_K\A}1/n。一个足以闭合原题、且未被单块反例否定的精确下一定理是：存在绝对常数 C，使对每个 K，limsup_{J→∞}J^{-1}Σ_{j<J}ℓ_{K,j}≤C(d_K-d_*)。由此 δ̲_log(A)≥d_K-C(d_K-d_*)，再令 K→∞ 即得 δ_log(A)=d_*。
- 第二轮用时：823.5 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：攻击上一轮跨尺度平均界，并寻找边界反例；幸存后把困难缩窄到 d_*>0、Σ_i1/n_i=∞ 且不存在倒数和发散的互素子族的重叠情形。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_MINOR_TEXT_REPAIR；范围：独立复核第二轮的四项内容：d_*=0时自然密度为0、含倒数和发散的两两互素模数子族时的结论、全部模数同属固定整数平移c时尤其c<0的边界分解，以及Araújo未激活反例不能移植；同时核对一般题面量词、自然/对数/上下密度的区别和剩余未证尾部命题。
- 复核方式：三项新增正面定理均成立，负平移边界公式及互素子族 CRT 论证没有量词漏洞；关键脚本按原参数重跑通过，另有独立大模数组合与任意剩余枚举交叉检查。结果正确保留一般问题，不存在完整解越界。Araújo 例激活尾项现已修正为 i*1_S(i)+k*p_i^4；固定平移密度等于 d_* 的理由也已在证明记录中明确。
- 证据边界：三项新增正面定理均成立，负平移边界公式及互素子族 CRT 论证没有量词漏洞；关键脚本按原参数重跑通过，另有独立大模数组合与任意剩余枚举交叉检查。结果正确保留一般问题，不存在完整解越界。Araújo 例激活尾项现已修正为 i*1_S(i)+k*p_i^4；固定平移密度等于 d_* 的理由也已在证明记录中明确。

#### 第二轮实际尝试

- **移植 Araújo Proposition 3.24 反例**（refuted）：逐项比较其振荡点、模数及本题 n≥n_i 的激活门槛。；该例用模数 p_i^4、低代表 i1_S(i)。造成振荡的点 i 满足 i<p_i^4，因而在本题中不会被筛掉。激活后只剩 i·1_S(i)+kp_i^4（k≥1），且 Σp_i^{-4}<∞，由 Theorem 3.26 反而有自然密度。因此该反例不能击穿官网题面。
- **固定负整数平移的边界分解**（advanced）：假设所有 a_i≡c，处理第一轮遗留的 c<0。写 c=−h、Q={n_i}、m=n+h。；令 M_Q 为 Q 的倍数集，并令 P={q∈Q:不存在 r∈Q，r<q 且 r|q}。当 m≥2h 时，m 的任何真因子 r 都满足 r≤m/2≤m−h=n，故 n 被激活筛掉当且仅当 m∈M_Q\P。P 是 primitive set；Erdős 1935 定理给 δ_log(P)=0，有限平移仍为零对数密度。结合 Davenport–Erdős，A 的对数密度存在。
- **零极限周期密度情形**（advanced）：沿用有限周期幸存集 B_K，强化第一轮仅写出的上对数密度估计。；若 d_*:=lim_Kd_K=0，则对 x≥n_K 有 A∩[n_K,x]⊆B_K。周期计数给 limsup_x|A∩[1,x]|/x≤d_K；令 K→∞，得到 A 的自然密度为 0。
- **发散互素子族**（advanced）：用 CRT 计算该子族有限筛的精确幸存密度。；若存在两两互素子族 Q' 且 Σ_{q∈Q'}1/q=∞，则任意剩余选择下，前若干个 Q' 条件的幸存密度为 ∏_{q∈Q'}(1−1/q)，随截断趋于0。因此 d_*=0，上一项给 A 的自然密度为0。若全部模数可分成有限个两两互素子族，则倒数和收敛时用已知可和特例，发散时至少一个子族发散；故这种模数系统全部有自然密度。
- **复核上一轮跨尺度常数界**（blocked）：把 dyadic 平均精确改写成激活尾集的上对数密度。；令 E_K=B_K∩⋃_{i>K}C_i=B_K\A。则上一轮左端等于 δ̄_log(E_K)。所猜不等式正是 δ̄_log(E_K)≤C(d_K−d_*)。当 d_*=0 时由 E_K⊆B_K 已以 C=1 成立；当 d_*>0 时既未找到反例，也未能从二阶交叠或 Araújo 反例推出该界。

#### 第二轮新增严格进展

- [第二轮新增] 若有限周期幸存密度 d_K 的极限 d_*=0，则 A 不仅有对数密度，而且有自然密度 0。
- [第二轮新增] 若模数含倒数和发散的两两互素子族，则对任意剩余类，A 的自然密度为 0。特别地，模数能分成有限个两两互素子族时，A 总有自然密度。
- [第二轮新增] 第一轮固定平移特例从 c≥0 严格扩张到所有固定 c∈ℤ。c<0 时的无限边界误差恰为 primitive core 的有限平移，其对数密度为0。
- [第二轮复核加固] Araújo Proposition 3.24 的未激活反例不能通过本题的 n≥n_i 门槛；其振荡完全来自低于模数的最小代表。

#### 证伪与边界检查

- 对 c=−h 的边界公式检查了等号端点 m=2h：真因子 r≤m/2=h=n，仍满足激活条件。m<2h 仅产生有限误差。
- 若 m∈Q 但已有更小 Q-除数，则该除数自动不超过 n；因此边界不是整个 Q，而精确是整除极小元 P。若 P 含1，则 P={1}，仍只是有限例外。
- 从 Σ_{p∈P}1/(p log p)<∞ 推出零对数密度时使用尾部分割：对固定 Y，Σ_{Y<p≤x}1/p≤log x·Σ_{p>Y}1/(p log p)，再先令 x→∞、后令 Y→∞。
- Araújo 例中 p_i^4>i 的方向已核对；若忽略该不等式，会错误地把未激活反例报告为本题反例。
- 单个或固定长度的 dyadic 坏块在 J 个对数块平均中贡献 O(1/J)，仍不能反驳上一轮长期平均命题。
- 有限计算只验证负平移恒等式和两个实现的一致性，不用于证明 primitive sequence 的无限定理。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/25/fixed_shift_boundary_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/25/fixed_shift_boundary_check.py)：用两个独立引擎核对固定负平移分解：其一逐点扫描全部激活同余条件，其二分别筛出激活算术级数与完整倍数集，再减 primitive core。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/25 && python3 -m py_compile fixed_shift_boundary_check.py && python3 fixed_shift_boundary_check.py --qmax 14 --hmax 8 --limit 240；结果：PASS：遍历 16383 个非空 Q⊆{1,…,14}、8 个负平移，共131064个实例；direct 与 sieve 两实现完全一致，且在 n+h≥2h 的精确范围内均等于“平移倍数集减 primitive core”公式。SHA-256: f31262e2d940988a84b328ee2e0bc81f61806480bd1790c67a4bc21121a8eda7。

#### 当前障碍

剩余硬核情形可假设 d_*>0、Σ_i1/n_i=∞，且每个两两互素模数子族的倒数和均收敛。这里模数必须高度共享素因子，而新增剩余类对 B_K 的长期周期损失 d_K−d_* 可能极小；仍无法控制它们在 n≈n_i 附近产生的累计激活命中。二阶 Bonferroni 只提供错误方向的并集下界，Araújo 的未激活反例又被门槛移除。

#### 下一精确定理

比上一轮统一线性界更弱、但足以闭合原题的精确下一定理是：在上述剩余硬核情形中，令 E_K=B_K∩⋃_{i>K}C_i，则证明 lim_{K→∞} δ̄_log(E_K)=0。因为 A⊆B_K 最终成立且 B_K 的密度为 d_K，这将给 δ̲_log(A)≥d_K−δ̄_log(E_K)，再令 K→∞ 得 δ_log(A)=d_*。上一轮的 δ̄_log(E_K)≤C(d_K−d_*) 会推出此命题，但目前没有理由要求统一线性速率。

#### 第二轮证明记录

承接的第一轮事实

写 R_i={n≥1:n≡a_i (mod n_i)}、C_i=R_i∩[n_i,∞)，并令 B_K=ℕ\⋃_{i≤K}R_i。B_K 是周期集，密度为 d_K，且 d_K↓d_*。对 n≥n_K 有 A⊆B_K。第一轮已经证明 Σ_i1/n_i<∞ 时 A 有自然密度；这些不计作本轮新增。

第二轮新增推导

首先强化 d_*=0 情形。周期计数给 |B_K∩[1,x]|=d_Kx+O_K(1)，所以
limsup_{x→∞}|A∩[1,x]|/x≤d_K.
令 K→∞ 即得 d(A)=0。这也解决了任何含发散互素子族的系统：若 Q' 两两互素，则 CRT 给有限幸存密度
∏_{q∈Q'_0}(1−1/q)≤exp(−∑_{q∈Q'_0}1/q)→0,
故 d_*=0。结合可和特例，模数能有限着色成两两互素族时，A 总有自然密度。

其次闭合所有固定整数平移。c≥0 已由第一轮化为倍数集。若 c=−h<0，设 Q={n_i}、M_Q={m:∃q∈Q,q|m}，以及
P={m∈Q:不存在 q∈Q，q<m 且 q|m}.
对 n+h=m≥2h，任意真因子 q|m 满足 q≤m/2≤m−h=n，因此
1_{n∈⋃C_i}=1_{m∈M_Q}−1_{m∈P}.
P 是 primitive：若 p_1<p_2 且 p_1|p_2，则 p_2不可能属于P。Erdős 1935 给 Σ_{p∈P,p>1}1/(p log p)<∞。对任意 Y，
(1/log x)Σ_{Y<p≤x,p∈P}1/p≤Σ_{p>Y,p∈P}1/(p log p),
故 P 的对数密度为0。平移 h 攭变调和和至多
Σ_{p>2h}h/[p(p−h)]<∞.
Davenport–Erdős 给 M_Q 的对数密度，因此 A 的对数密度存在，并等于 1−δ_log(M_Q)=d_*。

仍未闭合的缺口

令 E_K=B_K\A=B_K∩⋃_{i>K}C_i。上一轮 dyadic 量满足
limsup_{J→∞}J^{-1}Σ_{j<J}ℓ_{K,j}=δ̄_log(E_K).
所以其猜测是统一线性界 δ̄_log(E_K)≤C(d_K−d_*)。本轮只能证明 d_*=0 时它以 C=1 平凡成立；d_*>0 时没有证明或反例。当前更适当的目标是不要求速率，只证 δ̄_log(E_K)→0。

来源成熟度与优先权

Davenport–Erdős 及 Erdős 1935 是成熟原始来源。Araújo 的 Proposition 3.24/Theorem 3.26 是直接相关但非常新的 2026 学位论文/arXiv v1；这里只采用可逐行核查的精确命题。定向检索没有找到明确陈述“所有固定 c∈ℤ”或“发散互素子族”这两个特例的一手文献，故不能据此宣称新颖性或优先权。

#### 本轮核查来源

- FormalConjectures/ErdosProblems/25.lean；一手来源：true；核验：再次核对：模数为正自然数、StrictMono，剩余代表为任意整数；激活条件精确为 x<n_i 或不同余。
- [Francisco Araújo, Sarnak's Program for Erdős Sieves, Part I / dissertation](https://digital.ub.uni-paderborn.de/hs/download/pdf/8306542)；一手来源：true；核验：Proposition 3.24（PDF pp.40–41）构造未激活单剩余类筛无对数密度的例子 R_i=i1_S(i)+p_i^4ℤ；紧随其后的讨论明确指出去掉低于模数的最小代表正是 Erdős #25/#486。Theorem 3.26（p.42）只在 Σ_i|R_i|/b_i<∞ 时证明激活未筛集合有自然密度。
- [Francisco Araújo, Sarnak's Program for Erdős Sieves. Part I: Topological Dynamics and Light Tails](https://arxiv.org/abs/2602.24031)；一手来源：true；核验：arXiv:2602.24031v1 与学位论文相应章节一致；这是 2026 年近期预印本，不能视作成熟的最终文献结论。
- [P. Erdős, Note on Sequences of Integers No One of Which is Divisible By Any Other](https://users.renyi.hu/~p_erdos/1935-04.pdf)；一手来源：true；核验：p.126 的无编号 Theorem 证明：primitive sequence P 满足 Σ_{p∈P,p>1}1/(p log p)<∞；这足以推出 Σ_{p≤x,p∈P}1/p=o(log x)。DOI 10.1112/jlms/s1-10.1.126。
- [H. Davenport and P. Erdős, On Sequences of Positive Integers](https://users.renyi.hu/~p_erdos/1951-07.pdf)；一手来源：true；核验：正文重述并初等证明：任意整数集合的倍数集具有对数密度，等于有限倍数并集密度的单调极限。
- [Erdős Problem #25](https://www.erdosproblems.com/25)；一手来源：false；核验：页面截至 2026-01-20 编辑版本仍标 OPEN，并保留激活条件及“#486 的特例”。仅用于当前状态与题面交叉核对。

### #117

- 第一轮障碍：要把 h(7)≥10 的有限改进提升成更强的渐近底数，必须控制 W(2m−1,3) 最大 partial ovoid 的增长。m=3 已显示其并非简单的 3m+1；现有一般界不足以判断 extraspecial 3-群最终能否超过 √2。
- 第一轮下一定理：最明确的下一定理是：证明无限多个 m 满足 ω(W(2m−1,3))≤Cm+O(1)，其中 C<2log₂3≈3.169925；这会推出严格优于 √2 的下界。反之，若证明 ω(W(2m−1,3))≥(2log₂3−o(1))m，则可排除 extraspecial 3-群的渐近改进。
- 第二轮用时：996.4 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：检验是否可能有无限多个 m 满足 Ω_3(m)≤Cm+O(1)，其中 C<2log₂3；若不可能，则严格排除 extraspecial 3-群改进 √2 指数底数的路线。
- 第二轮结论：route_refuted；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_PROGRAM_SCOPE_CAVEATS；范围：独立复核第二轮有限几何结论：对每个奇素数 p 和每个奇数 t≥1，在辛空间 W(2^t−1,p) 中构造 p^t+1 点的 partial ovoid；由辛直和嵌入推出所有整数 m≥1 上 Ω_p(m)>m^(log_2 p)/p+1；再用先前已建立的 extraspecial 群恒等式 ω(E_{p,m})=Ω_p(m)、a(E_{p,m})=p^m+1，严格排除上一轮对 Ω_3 的线性上界路线。
- 复核方式：不把原代理的结论当作前提，逐式重做 Frobenius 下降、张量积形式的交替性与非退化性、范数配对、射影点互异、辛直和单调性、奇数 t 的整数选取和两个渐近推论；重生成并重验全部三个仓库证书；另压测 t=1、复合奇数 t、非奇素数 p 的程序边界。复核代理未编辑原文件；主代理随后收紧工具输入契约并补入 Moore 下降说明。
- 证据边界：独立复核未发现使一般构造、严格超线性下界或路线反驳失效的数学缺口。证书工具的 t=1、复合奇数 t、p 输入范围及 metadata 断言已按其真实有限覆盖范围修补；所有复合奇数 t 的全称量词仍来自一般 Moore/Galois 下降证明，而非三份有限证书。#117 仍未解决。

#### 第二轮实际尝试

- **攻击上一轮线性候选定理**（refuted）：把 PG(1,p^t) 经 Frobenius twisted tensor 嵌入 2^t 维空间，逐项检查下降、交替性和非正交条件。；当 t 为奇数时，t 个二维交替形式的张量积仍是非退化交替形式。对 a∈F_{p^t} 定义 v_a=⊗_{i=0}^{t−1}(e_0+a^{p^i}e_1)，并加入 v_∞=e_1^{⊗t}。Galois 固定空间在 F_p 上维数为 2^t，且 ⟨v_a,v_b⟩=N_{F_{p^t}/F_p}(b−a)≠0。故 W(2^t−1,p) 含 p^t+1 点 partial ovoid。
- **把稀疏维数列推广到所有秩**（advanced）：利用非退化辛直和嵌入和奇 t 序列相邻秩相差四倍。；给定 m，取最大奇数 t 使 2^{t−1}≤m。则 m<4·2^{t−1}，所以 Ω_p(m)≥p^t+1>m^{log₂p}/p+1。特别 Ω_3(m)>m^{log₂3}/3+1，故 Ω_3(m)/m→∞。
- **重新比较 extraspecial 3-群的指数效率**（advanced）：把新增的 Ω_3(m) 下界与 a(E_{3,m})=3^m+1 比较。；有 log(a(E_{3,m}))/ω(E_{3,m})≤3log(3)m^{1−log₂3}+o(1)→0。因此 (3^m+1)^{1/ω(E_{3,m})}→1，不仅不能超过 √2，甚至不产生任何固定大于1的指数底数。
- **计算证书与独立验证**（advanced）：第一程序在扩域中构造 twisted tensor、执行 Frobenius 下降并输出素域 Gram 矩阵；第二程序完全不做扩域运算，只在 F_p 上验证 Gram 矩阵非退化交替及所有点对非正交。；p=3,t=3 得到 8 维、28 点证书；p=3,t=5 得到 32 维、244 点证书；另以 p=5,t=3 得到 8 维、126 点证书检查一般奇素数参数。
- **用现有 p-rank 上界定位正确尺度**（advanced）：代入一手预印本定理2.1。；对 m≥2，m^{log₂3}/3+1<Ω_3(m)≤2m²+3m+2。故当前严格已知尺度位于幂指数 log₂3≈1.58496 与2之间，而非线性尺度。

#### 第二轮新增严格进展

- [第二轮新增] 对任意奇素数 p 和任意奇数 t≥1，严格构造 W(2^t−1,p) 中大小 p^t+1 的 partial ovoid。构造的点对配对精确等于 N(b−a)，不是启发式或仅经有限枚举确认。
- [第二轮新增] 对所有 m≥1，证明 Ω_p(m)>m^{log₂p}/p+1；特别 Ω_3(m)>m^{log₂3}/3+1。因此不存在固定 C 使 Ω_3(m)≤Cm+O(1) 在无限多个无界 m 上成立，上一轮 next_theorem_zh 被严格反驳。
- [第二轮新增] 对 extraspecial 3-群 E_{3,m}，证明 (a(E_{3,m}))^{1/ω(E_{3,m})}→1。因此该族不能改进 extraspecial 2-群给出的 √2 指数底数。相同论证适用于每个固定奇素数 p。
- [第二轮复核加固] 结合 Bamberg–Bishnoi–Ihringer–Ravi 定理2.1，得到 m≥2 时 m^{log₂3}/3+1<Ω_3(m)≤2m²+3m+2，明确替换了上一轮错误的线性目标尺度。

#### 证伪与边界检查

- 检查了最危险的奇偶边界：t 偶数且 p 为奇数时，张量积形式是对称形式而非交替形式，不能声称得到 W(2^t−1,p)；全部定理明确限制 t 为奇数。
- 检查了 Galois 下降的维数量词：坐标子集在循环移位下每个长度 d 的轨道贡献 F_{p^d}，即 d 个 F_p 维数；总和为全部 2^t 个坐标，因此固定空间恰为 2^t 维。
- 非退化性不只靠维数猜测：对每个长度 d 的循环轨道，取 F_{p^d}/F_p 基后，对应 Moore 矩阵可逆，故固定向量经扩标量张成该轨道全部坐标；于是 W⊗_{F_p}F_{p^t} 与原张量空间同构，张量积非退化形式确实下降为 W 上的非退化形式。
- 检查了方向性：partial ovoid 构造给出 ω 的下界，不能写成 h(n) 的新下界。本轮仅据此排除该群族的指数效率。
- 独立素域验证器确认 p=3,t=3 的 28 点证书完成378次非零配对检查；这也击穿了把 W(7,3) 误认为仍接近 3m+1=13 的边界外推。
- 独立素域验证器确认 p=3,t=5 的 244 点证书完成29646次非零配对检查，验证超线性现象并非仅有 t=3 的偶然小参数。
- 以 p=5,t=3 的126点证书作跨素数复算，完成7875次配对检查；结果与 p^t+1 一致。
- 检查 t=1 边界：构造退化为二维辛空间的全部 p+1 个射影点，公式仍成立。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/twisted_tensor_certificate.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/twisted_tensor_certificate.py)：仅用 Python 标准库实现有限域、多项式不可约性检查、twisted tensor、Frobenius 下降及素域证书输出。SHA-256：feeb8e695f20a5365b9e93df1c8c475106949efe58ce1d0bb4c95dc23280f6d8。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117 && python3 twisted_tensor_certificate.py 3 3 partial_ovoid_p3_t3.json && python3 twisted_tensor_certificate.py 3 5 partial_ovoid_p3_t5.json && python3 twisted_tensor_certificate.py 5 3 partial_ovoid_p5_t3.json；结果：分别输出 dimension=8 points=28、dimension=32 points=244、dimension=8 points=126。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/verify_partial_ovoid.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/verify_partial_ovoid.py)：独立素域证书验证器；不复用扩域或 twisted-tensor 代码，只检查矩阵交替性、满秩和全部点对配对。SHA-256：31195ac2b3d383944145054f1d66e4f7b5964cf5f4047ba58dc1f04a8f6b9203。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117 && python3 verify_partial_ovoid.py partial_ovoid_p3_t3.json && python3 verify_partial_ovoid.py partial_ovoid_p3_t5.json && python3 verify_partial_ovoid.py partial_ovoid_p5_t3.json；结果：依次输出 VERIFIED，并完成378、29646、7875次点对检查。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/partial_ovoid_p3_t5.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117/partial_ovoid_p3_t5.json)：最主要的32维、244点 F_3 精确证书，SHA-256：a170458b4e8cfba8cd7c52490e638ae2975181673f8d04692a0ffe0525722264。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/117 && python3 verify_partial_ovoid.py partial_ovoid_p3_t5.json；结果：验证为32维非退化交替空间中的244个两两非正交点。

#### 当前障碍

上一轮的 blocking step 已由否定方式闭合：extraspecial 3-群并非潜在的更优指数族。官网问题本身仍阻塞在完全不同的位置：必须找到非 extraspecial 的群族，使 a(G) 相对于 ω(G) 的指数效率超过 √2，或证明统一结构定理限制这种效率。现有 twisted-tensor 与 p-rank 结果都没有改进 Pyber 的全局指数常数。

#### 下一精确定理

有限几何侧最清晰的下一定理候选是确定 Ω_3(m) 的幂指数，例如证明或反驳 Ω_3(m)=m^{log₂3+o(1)}；当前仅知 m^{log₂3}/3<Ω_3(m)≤2m²+3m+2。即使该定理成立，它主要完成 extraspecial 3-群的内部刻画，并不解决官网 h(n) 的最优指数率。

#### 第二轮证明记录

【承接的第一轮事实】
设 E_{p,m} 是阶 p^{2m+1} 的 extraspecial p-群，V=E/Z(E) 是 F_p 上的 2m 维非退化辛空间。两元素交换当且仅当其像正交。因此 E 中两两不交换集与 W(2m−1,p) 中两两非正交射影点集一一对应，记其最大大小为 Ω_p(m)。第一轮已证明
\[
\omega(E_{p,m})=\Omega_p(m),\qquad a(E_{p,m})=p^m+1.
\]
p=2 时 Ω_2(m)=2m+1，从而产生约 √2 的指数下界；p=3 是否可能更优取决于 Ω_3(m) 是否保持足够小。

【第二轮新增推导】
取 K=F_{p^t}，U=K^2，并在 U 上取标准交替形式 β。考虑
\[
\widetilde W=U\otimes U^{(p)}\otimes\cdots\otimes U^{(p^{t-1})}.
\]
其 K-维数为 2^t。Frobenius 与张量因子的循环移位组合成阶 t 的半线性变换 T。若把张量基按子集 S⊆{0,…,t−1} 编号，则一个坐标轨道长度为 d 时，T-固定条件允许首坐标任取 F_{p^d}，故贡献 d 个 F_p 维数。对全部轨道求和得到
\[
\dim_{F_p}\widetilde W^T=\sum_{	ext{轨道}}d=2^t.
\]
令 W=\widetilde W^T。张量积形式
\[
B=\beta\otimes\beta^{(p)}\otimes\cdots\otimes\beta^{(p^{t-1})}
\]
在 W 上取值于 F_p。若 t 为奇数，则交换两个变量产生符号 (−1)^t=−1，所以 B 是交替形式；其非退化性由标量扩张回 \widetilde W 后的非退化性得到。

对 a∈K 定义
\[
v_a=\bigotimes_{i=0}^{t-1}(e_0+a^{p^i}e_1),
\qquad v_\infty=e_1^{\otimes t}.
\]
这些向量均被 T 固定。对 a≠b，逐因子计算得到
\[
B(v_a,v_b)=\prod_{i=0}^{t-1}(b^{p^i}-a^{p^i})
=N_{K/F_p}(b-a)\ne0,
\]
且 B(v_a,v_\infty)=1。故这些 p^t+1 个射影点两两非正交，从而
\[
\Omega_p(2^{t-1})\ge p^t+1\qquad(t\text{ 为奇数}).
\]

现在给定任意 m，取最大奇数 t 使 m_0=2^{t-1}≤m。W(2m_0−1,p) 可作为非退化辛直和因子嵌入 W(2m−1,p)，且下一允许的奇 t 对应4m_0，因此 m<4m_0。令 α=log_2p，则
\[
\Omega_p(m)\ge p^t+1=p m_0^\alpha+1
>\frac1p m^\alpha+1.
\]
对 p=3，
\[
\boxed{\Omega_3(m)>\frac13m^{\log_23}+1}.
\]
由于 log_2 3>1，Ω_3(m)/m→∞；所以不存在任何固定 C 使 Ω_3(m)≤Cm+O(1) 对无限多个无界 m 成立。上一轮要求 C<2log_2 3 的候选定理尤其被否定。

再结合 a(E_{3,m})=3^m+1，
\[
0\le \frac{\log a(E_{3,m})}{\omega(E_{3,m})}
\le 3\log3\,m^{1-\log_23}+o(1)\longrightarrow0.
\]
因此
\[
(a(E_{3,m}))^{1/\omega(E_{3,m})}\longrightarrow1.
\]
这严格排除了 extraspecial 3-群改进 √2 的可能。另一方面，Bamberg–Bishnoi–Ihringer–Ravi 定理2.1给出
\[
\Omega_3(m)\le\binom{2m+2}{2}+1=2m^2+3m+2,
\]
所以当前正确的严格区间是
\[
\frac13m^{1.58496\ldots}+1<\Omega_3(m)\le2m^2+3m+2.
\]

【仍未闭合的缺口】
上述结论只反驳 extraspecial 3-群路线。它没有给出新的 h(n) 下界，因为构造大 partial ovoid 给出的是 ω 的下界；把不等号方向倒置会是实质性错误。官网问题的最优指数率、Pyber 上界常数及是否存在比 extraspecial 2-群更高效的其他群族均未解决。

【来源成熟度与潜在文献优先权】
q 为奇数、t=3 的 q³+1 构造已明确见 Cossidente 2011 命题3.5；偶特征的一般 twisted-tensor 正交构造见 Cossidente–King 2004 定理4.1。第二轮检索没有找到明确写出“奇 p、所有奇 t、辛空间 W(2^t−1,p)”及其对 extraspecial p-群指数效率推论的一手命题。这里给出了自洽推导和有限证书，但不据此声称文献上的新颖性；优先权仍需更广泛的有限几何文献核查。

#### 本轮核查来源

- [Pyber, The Number of Pairwise Non-Commuting Elements and the Index of the Centre in a Finite Group](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms/s2-35.2.287)；一手来源：true；核验：论文摘要精确陈述：有限群若至多含 n 个两两不交换元素，则 |G:Z(G)|≤c^n。它仍只给官网问题的绝对指数上界。
- [Cossidente, On Twisted Tensor Product Group Embeddings and the Spin Representation of Symplectic Groups: The Case q Odd](https://onlinelibrary.wiley.com/doi/10.5402/2011/694605)；一手来源：true；核验：命题3.5证明 q 为奇数时，twisted-tensor 短轨道是 W(7,q) 的 complete partial ovoid；该轨道有 q³+1 点。这核实了本轮一般构造在 t=3 的已发表特例。
- [Cossidente–King, Twisted tensor product group embeddings and complete partial ovoids on quadrics in PG(2^t−1,q)](https://eprints.ncl.ac.uk/69141)；一手来源：true；核验：作者机构仓库中的接受稿定理4.1构造 PG(1,q^t) 的 twisted-tensor 像；论文主要处理偶 q 下的正交空间。它提供接近的一手先例，但不直接陈述本轮所需的奇 q、任意奇 t 辛空间命题。
- [Ceria–De Beule–Pavese–Smaldore, On large partial ovoids of symplectic and Hermitian polar spaces](https://arxiv.org/abs/2203.04553)；一手来源：true；核验：定理3.7给出 W(5,q) 中大小 q²+q+1 的 maximal partial ovoid；表1同时记录 W(7,q) 的 q³+1 构造。
- [Bamberg–Bishnoi–Ihringer–Ravi, Ramsey numbers and extremal structures in polar spaces](https://arxiv.org/abs/2406.03043)；一手来源：true；核验：定理2.1明确给出：定义在 F_{p^h} 上、向量维数 n 的辛空间 partial ovoid 至多有 binom(n+p−1,p−1)^h+1 点。代入 p=3、h=1、n=2m 得 Ω_3(m)≤2m²+3m+2。

### #143

- 第一轮障碍：一般第一问仍未闭合。KLL 的 Proposition 2.15 控制厚尺度块中的有理比例正相关，但最终误差按块数 O(J) 计；在仅假设目标级数发散时，对数壳 κ-质量可能如 1/log j 般趋零，使 J 远大于累计质量的平方。需要一个随实际 κ-质量缩放的相关性能量估计，或能把稀薄壳合并而不破坏 log α≈log β 的新选择引理。作者也明确指出现有构造的尺度可比性在第6、8节似乎是本质的。
- 第一轮下一定理：最清晰且由 KLL 第5页直接指向的下一定理是：设 A⊂Q_{>1} 满足原 dilation separation；把每个 α∈A 写成既约分数 a/q，并额外假设所有分子 a 均平方自由，则证明 ∑_{α∈A}1/(α log α)<∞。具体首个技术子目标应是建立一个“κ-质量版本”的 Proposition 2.15/分块能量界，使坏相关贡献为 O(κ(B)) 或 O(∑_j κ(B_j)^2)，而不是与所用尺度块数成正比。平方自由性保证分解 a=Aa_0 时 gcd(A,a_0)=1，可去掉 KLL 所述 Hauke–Vázquez–Walker 的额外损失；剩余核心正是跨尺度选择问题。
- 第二轮用时：905.3 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：核清 KLL 中 λ、κ、E₂、E₃ 的层级；寻找平方自由分子是否自动带来尺度局部化；建立可严格闭合的危险邻域与有界分母特例；将剩余障碍压缩为密度敏感的 Proposition 2.15 与跨壳选择定理。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核第二轮的四项有限进展：固定 beta 的危险未来邻域可和、平方自由既约分子不强迫跨尺度局部化的显式反例、指数壳质量 s_j<<1/j 及平方可和、以及既约分母一致有界的有理子例。另重跑全部四个计算资产，并检查 lambda/kappa 测度、图独立集、全部有序对和严格端点。
- 复核方式：四项数学结论均成立，现有结果对它们的逻辑范围也基本准确。固定 beta 结论只有依赖 beta 的逐点可和性；平方自由族只是反驳自动尺度局部化而不是原猜想；sum s_j^2<infinity 不推出 sum s_j<infinity，也不控制跨壳相关；有界分母子例则确实完整闭合。一般实数情形和平方自由分子特例均仍缺少统一尾界及跨壳选择/能量定理，所以 Erdős #143 第一问仍未解决。
- 证据边界：['固定beta的可和常数没有随beta一致性；对无穷多个beta的邻域求并或逐次删除，有限和可累计成无穷并吞掉全部发散质量。局部加权度有限本身也不保证存在发散权独立集。', 'sum s_j^2<infinity只处理可归入同壳平方质量的误差，不能控制跨壳小bracket对；平方自由显式族正说明这类对可跨任意多尺度。', '有界分母子例没有覆盖一般问题允许的无界有理分母及无理元素。平方自由分子特例本身也仍未闭合。', '结果文件将conclusion标为route_advanced、full_solution_claim标为none，并在blocking_step_zh与proof_note_zh明确保留上述两类缺口；不存在把四项进展误写为原题完整解的情况。']

#### 第二轮实际尝试

- **重新审计“κ-质量版 Proposition 2.15”**（advanced）：逐式区分 λ(E)=∑1/(αβ)、κ(E)、E₂ 和 E₃，并比较每块误差与实际壳质量。；第一轮建议需精确拆分：E₂≤∑κ(B_j)^2 已存在；真正需要密度增益的是 E₃。现有 Proposition 2.15 的 ye^{-z}(log x)^2 与 B 的实际质量无关，代回后每块仍为 O(1)。因此不能把裸 λ 上界误称为 κ-质量估计。
- **固定元素的危险未来邻域**（advanced）：固定 β，把 α/β 按既约分母 t 分纤维。；若 α>β、α/β=s/t 既约且 1<[α,β]≤10β，则由 [α,β]=t/β 得 t≤10β²，故只有有限多个 t。固定 t 时，若两个分子 s₁|s₂，则 α₂=(s₂/s₁)α₁，造成精确 dilation 冲突；所以该分子集 primitive。又 1/(αlogα)=(t/β)/(s log(βs/t))≪_{β,t}1/(s log s)，故 Erdős 1935 逐纤维给出收敛。
- **证伪“平方自由分子自动迫使尺度可比”**（refuted）：取 α₀=23/11，并加入所有满足 p≡1(mod 23) 的素数。；对任意此类素数 p 和 k≥1，|kα₀−p|=|23k−11p|/11≥1，因为分子模23恒为−11；反向及不同素数之间也满足条件。全部既约分子均为素数，但 p/α₀=11p/23，故 [p,α₀]=11，对任意大的 p 都成立。因此平方自由性本身不排除跨任意多尺度的小 bracket 对。
- **有界既约分母特例**（advanced）：按既约分母 q≤Q 分解 A。；固定 q 的分子集 P_q 若含 a|b 就产生 |(b/a)(a/q)−b/q|=0，故 P_q primitive。对 a≥q²，有 1/((a/q)log(a/q))≤2q/(a log a)；较小的 a 只有有限多个。有限个 q 分别应用 Erdős 1935 后求和，得到目标级数收敛。
- **平方自由有理网格有限反例搜索**（inconclusive）：枚举既约 a/q，使用整数冲突图和 HiGHS 最大权独立集；另用独立分支搜索及独立有序对验证器交叉检查。；在 2≤α≤40、q≤10、分子平方自由的882个候选中，最优解仍只是≤40的12个素数，目标值1.36996633642497；小模型 2≤α≤10、q≤3 的24个候选由两种优化实现均得到 {2,3,5,7} 和相同目标值1.22244163180865。结果只是否定性有限证据。

#### 第二轮新增严格进展

- [第二轮复核加固] KLL 的块内 E₂ 平方质量估计已经存在；第一轮真正缺少的是 E₃ 的质量敏感增益以及跨尺度小 bracket 对的算术选择，不能笼统称为“加强 Proposition 2.15”。
- [第二轮新增] 对每个固定 β∈A，危险未来邻域 D(β)={α∈A:α>β, 1<[α,β]≤10β} 满足 ∑_{α∈D(β)}1/(αlogα)<∞；任意有限 F⊂A 的 ∪_{β∈F}D(β) 亦可和。此结论无需 A⊂Q 或平方自由假设，因为 irrational ratio 的 bracket 为∞。
- [第二轮新增] 平方自由分子不蕴含逐对尺度局部化：无限 admissible 集 A={23/11}∪{p:p为素数且p≡1(mod23)} 的所有既约分子平方自由，但 [p,23/11]=11 且 log p/log(23/11) 无界。
- [第二轮新增] 设 B_j=A∩(e^j,e^{j+1}] 且 s_j=∑_{α∈B_j}κ(α)。由1间隔性和 Mertens 上界，∑_{α∈B_j}1/α≪1、κ(α)≪1/(jα)，故 s_j≪1/j，进而 ∑_j s_j²<∞。这精确说明：若 E₃ 每壳误差能由 O(1) 改为 O(s_j)，累计仅为 O(∑s_j)，足以被发散总质量的平方吸收。
- [第二轮新增] 完全闭合有界分母特例：若 A⊂Q 且所有元素的既约分母有统一上界，则官网第一问的加权级数必收敛。所有有序对、有限初项和 log 比较均已覆盖。

#### 证伪与边界检查

- 严格/非严格边界均按题设处理：构造族中 |k(23/11)−p| 的最小可能值恰可等于1；题设允许等号。
- 显式无限族使用 Dirichlet 素数算术级数定理保证 p≡1(mod23) 的素数无限；有限前13项由两份独立实现检查全部156个有序对，未发现冲突，且 bracket 均以 Fraction 精确算得11。
- 该无限族还反驳了“平方自由分子使全局分母集 primitive”的朴素归约：其既约分母含1和11，而1|11。
- 固定 β 的危险邻域可和并不足以抽象推出存在发散权独立子集：局部加权度有限的图仍可由越来越大的有限团组成，使总权重发散而每个独立集权重有限。因此仍需利用算术结构，不能做纯贪心删点。
- 有限 MILP 的冲突边完全用 Fraction/整数不等式生成；返回集合又由不同循环逻辑穷举所有可能 k。小模型的最优值另由不依赖 SciPy 的分支搜索重算。
- 检索到的2026年 primitive-set 新工作没有声称处理实数 dilation separation；未将相似整数定理当作本题进展。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/squarefree_rational_search.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/squarefree_rational_search.py)：平方自由既约有理数候选、精确冲突图、最大 Erdős 权独立集 MILP，并内置独立性证书检查。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143 && python squarefree_rational_search.py --xmin 2 --xmax 40 --qmax 10 --squarefree --weight erdos；结果：882个候选、89546条边；HiGHS Status 7 Optimal；选择2,3,5,…,37共12个素数，目标1.36996633642497；independent_certificate=True。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/brute_force_rational_search.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/brute_force_rational_search.py)：不调用 MILP 的小模型精确分支搜索，用于独立重算最优值。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143 && python brute_force_rational_search.py --xmax 10 --qmax 3；结果：24个候选；最优集合2,3,5,7，目标1.22244163180865，与 MILP 完全一致。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/cross_scale_family.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/cross_scale_family.py)：生成 A={23/11} 加前若干个 p≡1(mod23) 素数，穷举有序对并精确计算 KLL bracket。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143 && python cross_scale_family.py --ell 23 --q 11 --count 12；结果：生成13项，内部检查 ordered_bad=0，所有跨尺度 bracket 精确等于11。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/verify_rational_certificate.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143/verify_rational_certificate.py)：与搜索器独立实现的精确有序对证书验证器。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/143 && python verify_rational_certificate.py '23/11,47,139,277,461,599,691,829,967,1013,1151,1289,1381'；结果：n=13，ordered_pairs=156，bad=0，exact_certificate=true。

#### 当前障碍

一般第一问及平方自由分子特例仍未闭合。固定 β 的危险邻域虽可和，但现有证明没有随 β、壳位置和实际 κ-质量一致的尾界；对无穷多个 β 逐次删除可和邻域可能累计吞掉全部发散质量。另一方面，Proposition 2.15 对 E₃ 的上界与 λ(B) 无关，在薄壳质量 s_j→0 时仍支付每壳 O(1)。显式族表明平方自由性不能直接消除跨壳小 bracket 对。

#### 下一精确定理

清晰的下一技术定理应包含两项。第一，在既约分子平方自由时，对 B⊂[e^j,e^{j+1}] 的 Proposition 2.15 事件 E_{y,z} 证明密度敏感界 λ(E_{y,z})≪y e^{-z}j·λ(B)，替代现有 ≪y e^{-z}j²；代回(2.26)即给每壳 E₃≪κ(B)。第二，证明一个利用有理分母纤维结构的跨壳选择/能量引理，使 1<[α,β]≤10β 的跨壳 κ-能量为 O(S)，其中 S 是所选集合累计 κ-质量。两项合并后，误差 O(S)+O(∑s_j²)=o(S²)，第二矩方法才会闭合平方自由分子特例。

#### 第二轮证明记录

承接的第一轮事实

KLL Theorem 1 已严格给出 H(X)=o(log X)，但 Abel 分部不能推出目标级数收敛。KLL 使用
\[
\kappa(\alpha)=\frac1\alpha\prod_{p\le\alpha}\left(1-\frac1p\right)\asymp\frac1{\alpha\log\alpha},
\qquad \lambda(\alpha)=\frac1\alpha.
\]
在式(2.24)中，E₂ 是小 bracket 对的裸 κ-能量；完成 Lemma 2.13(b) 的尺度局部化后，已有
\[
E_2\le \sum_j\kappa(A'_j)^2.
\]
困难更尖锐地位于 E₃：Proposition 2.15 只有
\[
\lambda(E_{y,z}(B))\ll y e^{-z}(\log x)^2,
\]
不含 B 的实际质量，故代回(2.26)后每块仍支付 O(1)。

第二轮新增推导

首先固定 β∈A，研究
\[
D(\beta)=\{\alpha\in A:\alpha>\beta,\ 1<[\alpha,\beta]\le10\beta\}.
\]
若 α/β irrational，则 bracket 为∞，不会进入 D(β)。若 α/β=s/t 为既约分数，KLL Lemma 2.5 给
\[
[\alpha,\beta]=\frac{t}{\beta},\qquad \alpha=\frac{\beta s}{t}.
\]
所以 t≤10β²。固定 t，令 P_t 为出现的分子 s。若 s_1|s_2，写 s_2=ks_1，则相应元素满足 α_2=kα_1，违反题设。因此 P_t 是 primitive integer set。对充分大的 s，
\[
\frac1{\alpha\log\alpha}
=\frac{t/\beta}{s\log(\beta s/t)}
\ll_{\beta,t}\frac1{s\log s}.
\]
Erdős 1935 定理及有限多个 t 遂给
\[
\sum_{\alpha\in D(\beta)}\frac1{\alpha\log\alpha}<\infty.
\]
这是跨尺度选择方向上的实质推进：每个固定枢纽的全部危险未来质量均有限。但此界尚不对 β 一致。

其次，平方自由性不能替代选择引理。令
\[
A_0=\left\{\frac{23}{11}\right\}\cup\{p:\ p\text{ prime},\ p\equiv1\pmod{23}\}.
\]
Dirichlet 定理保证第二部分无限。不同尾部元素是不同素数，故整数 dilation 不会精确相等。对 p≡1(mod23)，
\[
\left|k\frac{23}{11}-p\right|=\frac{|23k-11p|}{11}\ge1,
\]
因为 23k−11p≡−11(mod23)，该剩余类中非零整数的最小绝对值是11；反向从大素数到23/11显然距离大于1。因此 A_0 满足官网全部 dilation 量词。所有既约分子均为素数，但
\[
\frac{p}{23/11}=\frac{11p}{23},\qquad [p,23/11]=\frac{11p}{p}=11.
\]
于是小 bracket 对跨越任意多对数尺度。这个族不反驳目标级数——其素数部分仍可和——但严格反驳了平方自由分子自动给 logα\asymp logβ 的路线。

再看薄壳质量。设 B_j=A∩(e^j,e^{j+1}]。1间隔性给
\[
\sum_{\alpha\in B_j}\frac1\alpha\ll1.
\]
Mertens 上界给该壳上 κ(α)≪1/(jα)，因而
\[
s_j:=\kappa(B_j)\ll\frac1j,
\qquad \sum_{j\ge2}s_j^2<\infty.
\]
这把所需增益定量化了：若平方自由情形能把每壳 E₃ 从 O(1) 降到 O(s_j)，则前 J 壳的总误差为 O(S_J)，其中 S_J=∑_{j≤J}s_j；当目标级数发散时 S_J→∞，故 O(S_J)=o(S_J²)。一个足够精确的局部命题是
\[
\lambda(E_{y,z}(B))\ll y e^{-z}j\,\lambda(B),
\qquad B\subset(e^j,e^{j+1}],
\]
它恰比现有 j² 界多出实际密度因子。

本轮还闭合了有界分母特例。若每个 α=a/q∈A 均既约且 q≤Q，固定 q 的分子集 primitive。对 a≥q²，
\[
\frac1{(a/q)\log(a/q)}\le\frac{2q}{a\log a}.
\]
有限初项与有限个 q 相加，得到目标级数收敛。

仍未闭合的缺口

固定枢纽危险邻域可和只是逐点结论，没有对不断增长的 β 给出统一尾率；纯图论贪心也不够，因为局部加权邻域有限并不保证存在无限权独立子集。另一方面，显式 A_0 说明跨尺度对不能由平方自由性逐对排除。因此仍需同时证明密度敏感 E₃ 界和利用有理纤维的聚合选择引理。未获得一般题面或平方自由分子特例的完整证明。

来源成熟度与优先权

核心来源 KLL 仍是作者预印本/arXiv 论文，作者本人只把平方自由分子结论表述为可能方向，而非定理。官网截至2026年4月仍标记问题开放；FormalConjectures 的精确加权命题仍为 sorry。本轮检索没有找到更晚的一手解决论文，但不声称文献检索穷尽。

#### 本轮核查来源

- [Koukoulopoulos–Lamzouri–Lichtman, Erdős's integer dilation approximation problem and GCD graphs（作者版，47页）](https://dms.umontreal.ca/~koukoulo/documents/publications/erdos-integer-dilations.pdf)；一手来源：true；核验：Theorem 1 只推出 H(X)=o(log X)。Definitions 2.3–2.4 与 Lemma 2.5 给出：若 α>β 且 α/β=s/t 为既约分数，则 [α,β]=t/β。式(2.17)定义 κ(α)≈1/(αlogα)、λ(α)=1/α；式(2.24)–(2.26)把误差分成 E₁,E₂,E₃。E₂ 在完成尺度局部化后已由 ∑κ(A'_j)^2 控制；Proposition 2.15 对 E₃ 给出 λ(E)≪ye^{-z}(log x)^2，最终仍损失每块 O(1)。第5页 Remark 仅称平方自由分子下的加权收敛“有希望”，并明确保留跨尺度障碍。
- [Koukoulopoulos, Erdős's dilation approximation problem（2025 CIRM 作者讲义）](https://www.cirm-math.fr/RepOrga/3213/Slides/erdos_dilations.pdf)；一手来源：true；核验：第9页把跨块小 bracket 对的排除归入厚壳选择；第10–14页才处理同壳 quasi-diagonal/GCD-graph 项。这确认跨尺度选择与 Proposition 2.15 是两个不同层次。
- [KLL arXiv 记录 2502.09539](https://arxiv.org/abs/2502.09539)；一手来源：true；核验：核对作者、日期和 Theorem 1 的摘要量词。本轮检索至2026年7月未找到声称解决加权第一问或平方自由分子特例的后续一手论文；这不是穷尽性声明。
- [Erdős Problem #143](https://www.erdosproblems.com/143)；一手来源：false；核验：页面截至2026年4月24日仍标记 OPEN，并只把 KLL 的 o(log X) 列作 partial resolution。
- [FormalConjectures/ErdosProblems/143.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/143.lean)；一手来源：true；核验：本地逐行复核 WellSeparatedSet 的全部量词；parts.ii 正是 subtype A 上 1/(x log x) 的 Summable，证明仍为 sorry。
- [Erdős 1935 作者档案扫描](https://combinatorica.hu/~p_erdos/1935-04.pdf)；一手来源：true；核验：扫描本轮抓取超时；未据此添加无法逐页核查的细节。只使用已由 KLL 公式(1.5)及期刊书目信息确认的 primitive set 加权收敛定理。

### #148

- 第一轮障碍：现有四项逐点界在 u=X^{2/5} 的交界处恰好饱和 X^{8/5}；单纯拼接两个分支或朴素固定前缀均无法降低指数。必须获得四项解对首分母参数 u 的平均节省，或直接把 n^{8/5}/m 的指数改善一个固定量。
- 第一轮下一定理：明确的充分目标是：存在 0<δ<3/5，使对所有 m≤5n，\[\sum_{\substack{0<u\le4n\\m\mid u+n}} f_4\!\left(u,\frac{n(u+n)}m\right)\ll_\epsilon n^\epsilon\left(\frac{n^2}{m}\right)^{8/5-\delta}.\]这会给五项指数 c=8/5−δ；套同一 lifting 与固定 L 模板，即严格改善为 \(F(k)\le c_0^{(1/5-\delta/8+o(1))2^k}\)。允许尾分母下界的严格递增版本也值得先证，但还需重写 lifting 引理以保持该约束。
- 第二轮用时：1216.1 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：优先证伪上一轮提出的加权平均目标，并检查能否混合已发表的不同四项界改善五项指数 8/5，继而改善 F(k) 的 Vardi 指数系数 1/5。
- 第二轮结论：route_advanced；完整解声明：none；置信度：medium

- 独立复核：PASS_WITH_MINOR_REPAIRS；范围：独立复核从 Elsholtz–Planitzer 的两个统一四项上界出发，经 u=ma_1−n 的同余 lifting、U=(n²/m)^(50/289) 分割和算术级数求和，得到 f_5(m,n)≪_ε n^ε(n²/m)^(446/289)；再核查 Lemma B 与固定 L 前缀/尾部模板，得到严格递增分母计数 F(k)≤c_0^((223/1156+o(1))2^k)，其中本报告统一采用官网的 c_0=1.264084735… 约定。
- 复核方式：逐式重推分割与三个求和贡献，独立证明算术级数估计的常数统一性，单列 m>5n、n<5、U 与 4n 的相对位置及 ε 重命名；核对原论文 Theorem 1、Corollary 1、Lemma B 的原始量词；重做 Curtiss 前缀计数和 Vardi 底数换算；重跑全部三个计算资产，并用独立 Fraction/Decimal 计算复核指数与常数索引。复核代理未改原文件；主代理随后落实文字补强。
- 证据边界：计算只能证伪有限反例，真正的 PASS 依据是统一算术级数估计、边界拼接和固定 L 量词的逐式证明。三处文字修补已落实到独立证明稿与结构化摘要；对外发布仍需数论专家审稿，不能把本报告表述为原题已经关闭。

#### 第二轮实际尝试

- **证伪“加权平均是更容易的中间目标”**（advanced）：保留同余 u≡−n (mod m)，把无阈值加权和解释为标记五项解中的一个分母。；令 S(m,n)=Σf_4(u,n(u+n)/m)，其中 0<u≤4n 且 u≡−n(mod m)。每一项等价于选择 a=(u+n)/m∈(n/m,5n/m]，再把剩余四个分母排序。所得五项解的每个原像对应一个不同的可标记分母，故原像数至多5；每个五项解的最小分母又必在该区间。因此 f_5(m,n)≤S(m,n)≤5f_5(m,n)。上一轮目标其实与直接改善 f_5 等价到常数因子，并非明显更弱的平均定理。
- **混合新旧四项界**（advanced）：置 X=n²/m、N=n(u+n)/m。在 u≤X^{50/289} 使用 N^{3/2}u^{-3/4}，在其余范围使用 N^{4/3}u^{-2/3}+N^{28/17}u^{-8/5}。；非零范围 m≤5n 内有 X≤N≤5X。小 u 贡献为 X^{3/2}Σ_{u≤U}u^{-3/4}≪X^{3/2}U^{1/4}。大 u 的 28/17 项为 X^{28/17}Σ_{u>U}u^{-8/5}≪X^{28/17}U^{-3/5}。令 U=X^{50/289}，二者都等于 X^{446/289}。
- **处理旧界中的 N^{4/3}/M^{2/3} 干扰项**（advanced）：利用 u≡−n(mod m) 的算术级数稀疏性，而不是删除同余。；对 0<α<1，有 Σ_{U<u≤V,u≡r(mod m)}u^{-α}≪U^{-α}+m^{-1}V^{1−α}。取 α=2/3、V=4n 后，干扰项至多 X^{4/3}U^{-2/3}+X^{4/3}n^{1/3}/m=X^{352/289}+X^{3/2}m^{-5/6}≪X^{446/289}。
- **边界量词与非约分检查**（advanced）：逐项检查 m>5n、X<1、N 的整数性和 f_4 定理适用范围。；m>5n 时 f_5(m,n)=0；若 n≥5 且 m≤5n，则 X≥1。余下 n<5 只有有限多个非零 (m,n)，可吸收进统一常数。同余保证 N=n(u+n)/m为整数，而原论文定理对所有正整数参数成立，故即使 gcd(u,N)>1 也可直接应用。
- **传播到 F(k)**（advanced）：把候选 c=446/289 代入论文 Lemma B，再用固定 L 尾部与 Curtiss/Vardi 前缀模板。；得到 f_L(m,n)≪_ε(Ln)^ε(L^{4/3}n²/m)^{(446/289)2^{L−5}}。这里统一采用官网 c_0=1.264084735…；论文因索引移位把其平方 1.5979102… 也记为 c_0。固定前 k−L 项时，剩余既约分母的官网 c_0 对数主项为 2^{k−L+1}；尾部贡献为 (223/1156)2^k。精确量词是：给定误差先固定充分大的 L，再令 k→∞；前缀贡献 (1+ε)2^{1−L}2^k 随后可消去。
- **一手文献优先权搜索**（inconclusive）：检索 arXiv、期刊页和作者论文目录中的精确常数及后续 Egyptian-fraction 上界。；未定位到含 446/289、223/1156 或同一混合求和论证的论文；官网仍列1/5。但检索不具穷尽性，不能据此断言新颖性。

#### 第二轮新增严格进展

- [第二轮新增] 严格证明带同余的无阈值加权和 S(m,n) 满足 f_5(m,n)≤S(m,n)≤5f_5(m,n)；这加固了 lifting 的组合含义，同时表明上一轮 next theorem 基本等价于直接改善 f_5。
- [第二轮新增] 从已发表的两个四项逐点界推出候选统一界 f_5(m,n)≪_εn^ε(n²/m)^{446/289}。关键分割指数为 50/289，三个求和贡献分别不超过 X^{446/289}、X^{446/289} 和 X^{352/289}+X^{3/2}。
- [第二轮新增] 候选五项引理经本轮独立内部审稿通过；Lemma B 与固定尾部模板逐量词给出 F(k)≤c_0^{(223/1156+o(1))2^k}，其中 c_0=1.264084735… 采用官网约定。223/1156=1/5−41/5780，严格改善同一底数下的官网系数1/5；这仍是未发表候选界。
- [第二轮复核加固] 已覆盖 m>5n 的零解边界、n<5 的有限例外、输入分数未约分以及严格 F(k) 到非降序 f_k(1,1) 的上界方向。

#### 证伪与边界检查

- 用阈值尾部求和与直接五项递归分别验证 f_5 恒等式；同时验证无阈值和位于 [f_5,5f_5]。例如 (m,n)=(1,1),(1,2),(1,3),(1,4) 时 f_5=147,2892,17253,51323，无阈值和为281,5359,30192,71202。
- 直接 DFS 与使用二项因式分解的缓存递归在 n≤3、m≤3 的全部测试上完全一致；不是只用同一计数实现自检。
- Fraction 有理运算与 SymPy 独立求解均得到交点 θ=50/289、c=446/289、c/8=223/1156，并验证同一官网底数下的改善量为41/5780；换成论文的平方底数时系数应为223/2312。
- 对所有 n≤500、1≤m≤5n 数值求和混合逐点 majorant；按 a 枚举和按 u 过滤两种实现在 n≤40 完全一致。归一化 kernel/X^{446/289} 的最大测试值为15.0959163446，出现在 (n,m)=(3,1)，没有发现随范围增长的反例。该实验不是渐近证明。
- 检查了最危险的 m 随 n 增长情形：若只把同余删除，N^{4/3}u^{-2/3} 项确会损失到更差指数；候选改进必须保留每段约 1+U/m 个点的稀疏性。
- 实时检索没有找到精确候选常数，但不存在性或新颖性不能由搜索结果证明。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/lifting_identity_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/lifting_identity_check.py)：直接五项计数、带阈值 lifting、无阈值标记和的精确交叉检查；含普通 DFS 与二项除数公式两套实现。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148 && python3 -m py_compile lifting_identity_check.py && python3 lifting_identity_check.py --max-n 4 --max-m 3 --plain-max-n 3；结果：所有测试均满足 direct=threshold 及 direct≤marked≤5·direct；普通 DFS 与快速计数在启用范围完全一致。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/exponent_certificate.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/exponent_certificate.py)：使用 Python Fraction 和 SymPy 两种独立代数实现核对交点、五项指数和 Vardi 系数。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148 && python3 exponent_certificate.py；结果：两种实现均输出 θ=50/289、c=446/289、c/8=223/1156；1/5−223/1156=41/5780。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/hybrid_kernel_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/hybrid_kernel_check.py)：对混合四项 majorant 沿精确同余类作数值证伪搜索；按首分母与按 u 过滤两种枚举交叉检查。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148 && python3 hybrid_kernel_check.py --max-n 500 --cross-n 40；结果：检查所有 n≤500、m≤5n；两种枚举一致，最大归一化比15.0959163446，未发现反例。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/route2_proof.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148/route2_proof.md)：候选五项界及传播到 F(k) 的自洽英文证明草稿，明确标注需要独立审稿。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/148 && sed -n '1,240p' route2_proof.md；结果：逐式记录 (1)–(7)，结论为候选 F(k)≤c_0^{(223/1156+o(1))2^k}。

#### 当前障碍

内部推导未发现未闭合的数学量词，但所得常数看似改善已发表最佳结果，当前最大阻塞是独立专家审稿与文献优先权确认。特别应重新核查算术级数估计在 Lemma B 所需统一常数中的使用；本报告不能把它直接称为已确认新纪录。

#### 下一精确定理

在候选 446/289 引理独立确认后，进一步改善的明确充分目标是：存在 ρ,η>0，使对所有 m≤5n、X=n²/m≥1，均有 \[\sum_{\substack{0<u\le4n,\ u\equiv-n\pmod m\\X^{50/289-\rho}<u\le X^{50/289+\rho}}} f_4\!\left(u,\frac{n(u+n)}m\right)\ll_\epsilon n^\epsilon X^{446/289-\eta}.\]区间外现有两分支分别自动节省至少 ρ/4 和 3ρ/5，因此该局部平均定理会把五项指数严格降到 446/289 以下，并把 F(k) 的系数进一步降到223/1156以下。

#### 第二轮证明记录

Write `f_k(m,n)` for nondecreasing positive denominators, as in
Elsholtz--Planitzer.  Put

\[
X=\frac{n^2}{m},\qquad c=\frac{446}{289},\qquad
\theta=\frac{50}{289}.
\]

Only the nonzero range `m <= 5n` matters for `f_5`; for `n >= 5` this gives
`X >= 1`.  If `a_1` is fixed and `u=ma_1-n`, then

\[
\frac mn-\frac1{a_1}=\frac{u}{n(u+n)/m},\qquad
0<u\le 4n,\qquad u\equiv-n\pmod m.
\]

Set `N=n(u+n)/m`.  Given the final exponent loss `epsilon>0`, invoke Theorem 1
and equation (7) / Corollary 1 of Elsholtz--Planitzer with their parameter
`epsilon/2`.  Since `X <= N <= 5X` and `N <= 5n^2`, the published factor
`N^(epsilon/2)` is at most `5^(epsilon/2)n^epsilon`; take the maximum of the
two published constants.  Thus, uniformly in such `u`,

\[
f_4(u,N)\ll_\varepsilon n^\varepsilon
\min\left\{X^{3/2}u^{-3/4},
 X^{4/3}u^{-2/3}+X^{28/17}u^{-8/5}\right\}. \tag{1}
\]

Split the lifting sum at `U=X^theta`.  Below `U`, use the first member of
(1) and forget the congruence.  If `U>4n`, extending the actual range
`u<=4n` to `u<=U` only increases the upper bound:

\[
X^{3/2}\sum_{u\le U}u^{-3/4}
 \ll X^{3/2}U^{1/4}=X^{446/289}. \tag{2}
\]

Above `U`, the `28/17` term contributes (with the actual upper endpoint
again safely extended to infinity)

\[
X^{28/17}\sum_{u>U}u^{-8/5}
 \ll X^{28/17}U^{-3/5}=X^{446/289}. \tag{3}
\]

For `0<alpha<1`, summation along one residue class gives

\[
\sum_{\substack{U<u\le V\\u\equiv r\pmod m}}u^{-\alpha}
 \ll U^{-\alpha}+m^{-1}V^{1-\alpha}. \tag{4}
\]

Applying (4) with `alpha=2/3`, `V=4n`, the remaining term is

\[
\begin{aligned}
X^{4/3}\sum_{\substack{U<u\le4n\\u\equiv-n\pmod m}}u^{-2/3}
&\ll X^{4/3}U^{-2/3}+X^{4/3}\frac{n^{1/3}}m\\
&=X^{352/289}+X^{3/2}m^{-5/6}
 \ll X^{446/289}. \tag{5}
\end{aligned}
\]

Here `X=n^2/m` was used in the equality.  When `m>5n`, `f_5(m,n)=0`; when
`n<5`, the nonzero range has only finitely many pairs `1<=m<=5n`.
Equations (1)--(5), with those finite cases absorbed in the same
`epsilon`-dependent constant, prove the candidate lemma

\[
f_5(m,n)\ll_\varepsilon n^\varepsilon
\left(\frac{n^2}{m}\right)^{446/289}. \tag{6}
\]

Indeed the ordered-tail lifting sum is at most the displayed unrestricted
`f_4` sum.  In fact, the unrestricted sum with the congruence retained is
between `f_5(m,n)` and `5f_5(m,n)`: it marks one distinct denominator in
`(n/m,5n/m]` in a five-term solution, and every solution has at least its
smallest denominator in this interval.

Lemma B of the same paper now applies to (6), replacing `8/5` by `446/289`.
Fix a tail length `L>=5`.  The prefix/tail argument gives, after division by
`2^k` and taking logarithms in the official Problem 148 base,

\[
\limsup_{k\to\infty}\frac{\log_{c_0}F(k)}{2^k}
\le \frac c8+(1+\varepsilon)2^{1-L}.
\]

Given any `eta>0`, first choose this fixed `L` sufficiently large and only
then let `k` tend to infinity (and choose the harmless epsilon loss).  The
constants depending on fixed `L`, factorial terms and polynomial factors are
`o(2^k)`.  Hence the coefficient `c/8` changes from `1/5` to

\[
\frac18\frac{446}{289}=\frac{223}{1156}
=\frac15-\frac{41}{5780}.
\]

Here `c_0=1.264084735...` is the convention used on erdosproblems.com, based
on `u_1=1`, `u_(j+1)=u_j(u_j+1)`.  Elsholtz--Planitzer use a shifted index and
call `1.5979102...=c_0^2` by the same name.  In their base the new coefficient
is `223/2312`; naked coefficients from the two bases must not be compared.
In the official common base, both the old `1/5` and the following
`223/1156` are directly comparable.  Consequently the candidate strengthened
upper bound is

\[
F(k)\le c_0^{(223/1156+o(1))2^k}. \tag{7}
\]

No claim of novelty or peer-reviewed correctness is made here.  The key point
requiring independent scrutiny is the uniform arithmetic-progression estimate
(5) and its insertion into the hypotheses of Lemma B.

#### 本轮核查来源

- [Erdős Problems #148](https://www.erdosproblems.com/148)；一手来源：true；核验：官网精确题面要求分母严格递增；截至页面 2025-09-27 版本仍列 F(k)≤c_0^{(1/5+o(1))2^k} 为已知最佳上界。
- [Elsholtz–Planitzer, Sums of four and more unit fractions and approximate parametrizations, Theorem 1, Corollary 1, Section 5 and Lemma B](https://arxiv.org/pdf/2012.05984)；一手来源：true；核验：Theorem 1 给 f_4(M,N)≪_εN^εN^{3/2}/M^{3/4}；Corollary 1 同时保留旧界 N^ε(N^{4/3}/M^{2/3}+N^{28/17}/M^{8/5})。Section 5 令 u=ma_1−n；Lemma B 对任意统一的 c>1 将 f_5(m,n)≪_εn^ε(n²/m)^c 提升到全部 k≥5。命题写成所有正整数 m,n，不要求输入分数预先约分。
- [Elsholtz–Planitzer, Bulletin of the London Mathematical Society 53 (2021), DOI 10.1112/blms.12452](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.12452)；一手来源：true；核验：期刊页面核对了论文题名、作者、卷期页码及开放获取出版记录；正文抓取受 403 限制，公式以 arXiv 正文为准。
- [Christian Elsholtz author publication repository](https://www.math.tugraz.at/~elsholtz/WWW/papers/papers.html)；一手来源：true；核验：作者目录列该论文为其第73项及 2021 年 BLMS 正式论文；目录中未发现其后关于本题上界的论文。这只能说明本次定位结果，不能证明不存在其他作者的改进。

### #256

- 第一轮障碍：该路线尚不能确定 f(n) 的真实阶。Belov–Konyagin 只构造出常数项 a_0=O((log n)^3) 的质量 n 非负余弦多项式，而桥梁仍损失约 log(n/a_0)；Tang 的单位圆零点/整数系数机制只给出 √n 级下界。两者目前没有可迭代的共同参数。检索中未找到一手来源声称闭合这一鸿沟。
- 第一轮下一定理：最直接的下一定理是：存在固定 δ>0，使每个充分大 n 都有有限非增非负整数序列 b_1≥b_2≥⋯、∑b_k=n，且 a_0+∑b_k cos(kx)≥0 对所有实 x 成立，同时 a_0=O((log n)^{3-δ})。由本次桥梁将立即推出 log f(n)=O((log n)^{4-δ})。另一独立目标是证明所有纯乘积均有 ∑c_j²≥(2+ε)n；这会提高 2√n 的常数，但不会改变增长指数。
- 第二轮用时：808.6 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：检验能否去掉 Belov–Konyagin 到乘积上界桥梁中的 \log(n/a_0) 损失，并检验是否存在对所有纯乘积成立的统一系数能量增益 \sum c_j^2\ge(2+\varepsilon)n；若失败则识别必须进入的更窄结构。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核第二轮的六因子与八因子纯乘积能量等号见证、Fejér 核的非负非增整系数结构、单位根下界与径向桥梁上界的 m log m 首阶匹配，以及该障碍为何不排除 K_Z^downarrow(N)=O((log N)^(3-delta)) 中 0<delta<=1。
- 复核方式：逐式重推两个乘积展开、Fejér Fourier 系数、单位根乘积及径向优化；重跑原证书；另用不导入原脚本的 itertools/Decimal 实现复算系数与渐近比值；核对 Tang Theorem 3.2、Cipu Table 1 和 Belov–Konyagin Theorem 0.5(2)/Corollary 0.3 的原文。
- 证据边界：计算资产只负责防止展开、归一化和数值渐近中的机械错误；PASS 的数学依据是上述精确恒等式和统一不等式。Fejér 障碍是未发表、未形式化的内部推导，不能据此声称文献首创，也不能把 #256 标为已关闭。

#### 第二轮实际尝试

- **证伪纯乘积的统一能量增益**（refuted）：先利用整数卷积寻找等号例，再用直接枚举所有子集及其奇偶性独立重算系数。；六因子见证 A=(1,2,3,4,5,7) 满足 P_A(z)=1-z-z^2+z^5+z^6-z^{10}-z^{12}+z^{16}+z^{17}-z^{20}-z^{21}+z^{22}，故 \sum c_j^2=12=2|A|。八因子见证 (1,2,3,5,7,8,11,13) 也有恰好 16 个非零系数，且全为 \pm1。
- **尝试普遍去掉径向桥梁中的对数**（refuted）：在完全满足非负、非增、非负整系数条件的 Fejér 核族上检验桥梁的真实尺度。；取 T_m(x)=m+2\sum_{k=1}^{m-1}(m-k)\cos(kx)=|1+e^{ix}+\cdots+e^{i(m-1)x}|^2。此时 a_0=m、b_k=2(m-k)、N=\sum b_k=m(m-1)。对应 P_m(z)=\prod_{k=1}^{m-1}(1-z^k)^{2(m-k)}。在 \zeta=e^{2\pi i/m} 处，利用对称性和 \prod_{k=1}^{m-1}|1-\zeta^k|=m 得 \log|P_m(\zeta)|=m\log m。因而 \log\|P_m\|_\infty\ge(1+o(1))a_0\log(N/a_0)。
- **比较第一轮优化桥梁与 Fejér 下障碍**（advanced）：把 N=m(m-1)、a_0=m 代入第一轮的最优径向参数公式。；所得上界为 \frac{m(m-1)}2\log(1+2/(m-1))+m\log(1+(m-1)/2)=m\log m+O(m)，而单位根给出的下界是 m\log m。因此通用桥梁连首阶量级都是渐近紧的。
- **搜索 K_{\mathbb Z}^{\downarrow} 的后续改进**（inconclusive）：检索期刊正文、MathNet、arXiv、作者托管调查及 2025 年 Tang 论文的引文和现状陈述。；找到的最新直接相关一手论文仍引用 K_{\mathbb Z}^{\downarrow}(N)\ll(\log N)^3 和 \log f(N)\ll(\log N)^4；未找到声称 \log^{3-\delta}N 常数项构造的论文。检索阴性不能证明不存在遗漏，故只记为未找到。

#### 第二轮新增严格进展

- [第二轮新增] 对任意 \varepsilon>0，命题“所有纯乘积均满足 \sum_jc_j^2\ge(2+\varepsilon)n”按原量词为假；六因子显式乘积已经达到 Tang 界的等号 \sum c_j^2=2n。八因子也有独立等号见证。
- [第二轮新增] 构造了完全位于 Belov–Konyagin 非增非负整系数类别内的 Fejér 核族，严格证明任何只依赖 (a_0,N) 的统一桥梁都不可能给出 o(a_0\log(N/a_0))。
- [第二轮新增] 第一轮径向桥梁在该 Fejér 核族上满足“显式单位根下界 m\log m、径向上界 m\log m+O(m)”，故其对数损失及首阶常数在抽象类别内渐近紧。
- [第二轮复核加固] Belov–Konyagin 的已知下界迫使任何目标 K_{\mathbb Z}^{\downarrow}(N)=O((\log N)^{3-\delta}) 的有效指数至多取 \delta\le1；这没有否定 0<\delta\le1，但把候选范围收窄。

#### 证伪与边界检查

- Fejér 核的归一化已逐项核对：余弦系数是 2(m-k)，不是 m-k；因此质量确为 N=m(m-1)。
- 取 \zeta=e^{2\pi i/m} 时，1\le k<m，故没有因子 1-\zeta^k 为零；单位根取值合法。
- 加权单位根公式逐项核对：若 L_k=\log|1-\zeta^k|，则 L_{m-k}=L_k，故 2\sum(m-k)L_k=m\sum L_k=m\log m。
- 六因子和八因子的系数由密集整数卷积与直接子集奇偶枚举两种实现得到完全相同的结果，没有依赖浮点最大化。
- 有限 n 等号只反驳原先写成“所有纯乘积”的定理；它不反驳仅对充分大 n 成立的渐近能量增益。本轮未找到无限等号族，故没有越界声称渐近版本为假。
- Fejér 族的 a_0\asymp\sqrt N，远大于 BK 的多对数见证；因此它证明的是通用桥梁不可改善，而不是证明 BK 特殊见证无法拥有额外抵消。
- 文献检索未找到改进不等于不存在改进；数学结论只采用已打开的论文正文及其中的精确命题。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/256/round2_certificates.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/256/round2_certificates.py)：精确证书脚本：分别用密集整数卷积和直接子集枚举核对 n=6、8 的能量等号；用 Laurent 系数计数核对 Fejér 展开，并以 100 位精度独立重算单位根乘积。SHA-256 为 4a90df47eb055bb37aa9a8f9b54a781646c00d252026bb7273235c41a2a5d1c9。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/256 && python round2_certificates.py --m 5 10 25 100 250；结果：全部断言通过。n=6、8 的能量分别为 12、16；m=250 时直接对数值与 250\log250 的绝对误差约 1.46\times10^{-98}，且 m\log m/[a_0\log(N/a_0)]\approx1.0007264。

#### 当前障碍

四次对数上界的损失现在可明确拆分：BK 构造给 a_0=O((\log N)^3)，而从一般非负非增整系数余弦多项式到纯乘积必须付出量级 \log(N/a_0)。Fejér 核证明后一个损失不能凭现有抽象假设降低。因此改进 \log f(N)=O((\log N)^4) 必须改善 BK 常数项构造，或提取其具体构造中不为一般 Fejér 核共有的额外结构。本轮未完成这一步。

#### 下一精确定理

当前最清晰且不会被 Fejér 障碍击穿的下一定理是：证明存在固定 \delta\in(0,1]，使 K_{\mathbb Z}^{\downarrow}(N)=O((\log N)^{3-\delta})。精确地说，对每个充分大 N，构造有限序列 b_1\ge b_2\ge\cdots\ge0，b_k\in\mathbb Z、\sum b_k=N，以及 a_0=O((\log N)^{3-\delta})，满足 a_0+\sum b_k\cos(kx)\ge0 对所有实 x 成立。第一轮桥梁随后严格推出 \log f(N)=O((\log N)^{4-\delta})。

#### 第二轮证明记录

承接的第一轮事实

令 P(z)=\prod_{i=1}^n(1-z^{a_i})。第一轮已独立闭合两项事实：Belov–Konyagin Theorem 0.5(2) 提供质量 N 的非负、非增、非负整系数余弦多项式，其常数项 a_0=O((\log N)^3)；径向正则化给
\[
\log\|P\|_\infty\le \frac N2\log\!\left(1+\frac{2a_0}{N}\right)+a_0\log\!\left(1+\frac{N}{2a_0}\right).
\]
故 \log f(N)=O((\log N)^4)。Tang Theorem 3.2 与 O’Hara–Rodriguez 不等式则给 f(N)\ge2\sqrt N。本轮不把这些重记为新进展。

第二轮新增推导

首先检验桥梁中的对数是否只是证明技术。对 m\ge2，定义
\[
T_m(x)=m+2\sum_{k=1}^{m-1}(m-k)\cos(kx).
\]
几何级数平方给出精确恒等式
\[
T_m(x)=\left|1+e^{ix}+\cdots+e^{i(m-1)x}\right|^2\ge0.
\]
故它完全满足 BK 类条件，其中
\[
a_0=m,\qquad b_k=2(m-k),\qquad N=\sum_{k=1}^{m-1}b_k=m(m-1).
\]
对应的纯乘积是
\[
P_m(z)=\prod_{k=1}^{m-1}(1-z^k)^{2(m-k)}.
\]
令 \zeta=e^{2\pi i/m}，并记 L_k=\log|1-\zeta^k|。由 L_{m-k}=L_k，
\[
\begin{aligned}
\log|P_m(\zeta)|
 &=2\sum_{k=1}^{m-1}(m-k)L_k\\
 &=m\sum_{k=1}^{m-1}L_k.
\end{aligned}
\]
另一方面，\prod_{k=1}^{m-1}(1-\zeta^k)=m，因此
\[
\log|P_m(\zeta)|=m\log m.
\]
由于 N/a_0=m-1，
\[
\frac{\log\|P_m\|_\infty}{a_0\log(N/a_0)}
 \ge \frac{\log m}{\log(m-1)}\longrightarrow1.
\]
这严格排除了仅凭 a_0、N 和 BK 类定义得到 o(a_0\log(N/a_0)) 的可能。再将 a_0=m、N=m(m-1) 代回第一轮上界，得到
\[
\frac{m(m-1)}2\log\!\left(1+\frac2{m-1}\right)
+m\log\!\left(1+\frac{m-1}{2}\right)
=m\log m+O(m).
\]
所以第一轮桥梁在这一族上连首阶量级都是紧的。

其次攻击候选能量增益。取 A=(1,2,3,4,5,7)，直接展开得
\[
\prod_{a\in A}(1-z^a)=1-z-z^2+z^5+z^6-z^{10}-z^{12}+z^{16}+z^{17}-z^{20}-z^{21}+z^{22}.
\]
右侧恰有十二个 \pm1 系数，故
\[
\sum_jc_j^2=12=2|A|.
\]
于是对任意 \varepsilon>0，它都不满足 \sum c_j^2\ge(2+\varepsilon)|A|。另一个独立见证 A=(1,2,3,5,7,8,11,13) 有十六个 \pm1 系数，能量也是 16=2|A|；这与 Cipu Table 1 的记录一致。该反例只处理原先“所有 n”的量词，不能推出充分大 n 的版本也失败。

仍未闭合的缺口

Fejér 族证明通用桥梁不能改善，但其 a_0=m\asymp\sqrt N，并非 BK 的多对数优良见证。因此仍可能利用 BK 构造中特有的算术或频谱结构绕过该障碍；本轮尚未识别出可陈述且可证明的额外条件。有限能量等号例也没有形成无限族，所以渐近命题 \sum c_j^2\ge(2+\varepsilon)n（充分大 n）仍未判定。完整增长阶仍处于 2\sqrt n 与 \exp(C(\log n)^4) 之间。

来源成熟度与优先权

BK 上下界来自 1996 年同行评审原论文；Cipu 的小规模纯乘积数据来自 2004 年同行评审论文；Tang 的 2025 年 arXiv v2 是作者一手预印本并给出完整定理证明。Lubinsky 调查用于核查截至其成稿时的文献现状，不承担原始定理证明。Fejér 障碍是本轮从经典恒等式独立推出的研究观察；未检索到相同表述，但不能据此主张文献首创权。

#### 本轮核查来源

- [Erdős Problem #256（官网精确题面）](https://www.erdosproblems.com/256)；一手来源：true；核验：页面当前仍标为 OPEN；精确题面允许 a_i 重复，并记录 Belov–Konyagin 的 \log f(n)\ll(\log n)^4。页面最后编辑于 2026-01-20。
- [Belov–Konyagin, An estimate of the free term of a non-negative trigonometric polynomial with integer coefficients](https://www.mathnet.ru/links/d34aa10fdcc78dbc415217aed0ab0297/im95_eng.pdf)；一手来源：true；核验：Theorem 0.5(2) 给出 (\log N)^2/\log\log N\ll K_{\mathbb Z}^{\downarrow}(N)\ll M_{\mathbb Z}^{\downarrow}(N)\ll(\log N)^3；Corollary 0.3 给出 \log f(N)=O((\log N)^4)。
- [Tang, An improved lower bound for Erdős–Szekeres products, arXiv v2](https://arxiv.org/pdf/2509.14182)；一手来源：true；核验：Theorem 1.2 对所有 n 给出 f(n)\ge2\sqrt n；Theorem 3.2 对所有非零、被 (1-z)^n 整除的整系数多项式给出 \sum|c_j|^2\ge2n。论文仍把 Belov–Konyagin 的四次对数界列为当前上界。
- [Cipu, Upper Bounds for Norms of Products of Binomials](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/54AFDDE29E4EB9D7B4F3C6667DFC7C3C/S1461157000001030a.pdf/upper-bounds-for-norms-of-products-of-binomials.pdf)；一手来源：true；核验：定义 A_1(n)、A_2(n) 后，正文第 39 页记录 A_1(n)=2n 对 n\le6 及 n=8 成立；Table 1 给出 n=8 的指数见证 (1,2,3,5,7,8,11,13)，其 Euclidean norm 平方为 16。Theorem 1.2 还证明每个固定 n 的最小长度问题可化为有限指数搜索。
- [Lubinsky, A Survey of Erdős–Szekeres Products（作者托管全文）](https://lubinsky.math.gatech.edu/SelectedPapers_files/ErdosSzekeresSurveyPaperMay2023.pdf)；一手来源：true；核验：第 6 页明确陈述 Belov–Konyagin 的 \exp(O((\log n)^4)) 上界此后未获改进；该调查后来收入 2025 年论文集。它是现状调查而非原始定理来源。

### #301

- 第一轮障碍：有限块方法目前卡在两个相互独立的问题：其一，尚无严格结构定理把任意密度大于 1/2 的集合压入某个固定单位分数配置；其二，即使固定 720 配置，也尚未证明标准赋值铺排在所有可能的不交起点集合中具有最大自然密度。有限计算无法消除无限赋值尾部。
- 第一轮下一定理：建议下一步精确证明如下加权穿孔盒定理：若 C⊂ℕ₀³ 且平移族 {c+B*:c∈C} 两两不交，其中 B*=[0,4]×[0,2]×[0,1]\{(0,0,0)}，则 Σ_{(r,s,t)∈C}2^{-r}3^{-s}5^{-t}≤450/403。等号由 C={(5i,3j,2k):i,j,k≥0} 达到。该定理若成立，将证明 120/403 是固定 720 块所有按 (v₂,v₃,v₅) 选取的不交缩放族中的最优密度；有限 MILP 已在 [0,15]×[0,9]×[0,6] 上支持它，但尚缺处理无限尾部的严格对偶或递归证书。
- 第二轮用时：556.6 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：攻击第一轮的 blocking step 和 next theorem：判定标准 (5,3,2) 赋值格是否真是所有不交 720 穿孔盒铺排中的最大权方案，并检查有限 MILP 推断是否存在边界漏洞。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_AFTER_TEXTUAL_REPAIR；范围：第二轮候选加权穿孔盒定理：若 C⊂ℕ₀³ 且 {c+B*:c∈C} 两两不交，B*=[0,4]×[0,2]×[0,1]∖{0}，则 Σ_{c∈C}2^{-c₁}3^{-c₂}5^{-c₃}≤450/403；等号的指数起点集唯一为 {(5i,3j,2k)}。由此，相应完整赋值类缩放因子集合的自然密度至多120/403，标准格唯一取等。
- 复核方式：不以自动代理的定理结论为前提，独立重建 B* 平移交判据、胞内兼容图、后继充电及无限求和；用第二份内联集合实现穷举全部相关差向量；重跑三个原资产及额外有限盒尺寸；最后从精确赋值类计数重做自然密度截断和 120/403→139/806→667/806 的常数方向。
- 证据边界：PASS_AFTER_TEXTUAL_REPAIR 表示候选定理的数学核心、等号唯一性和方法类常数均经内部独立复核；统一尾部论证及方法类范围限定已补入结构化结果和最终报告渲染。它不等同于论文发表、外部同行评审或原题闭合。

#### 第二轮实际尝试

- **无限加权穿孔盒定理**（advanced）：把 ℕ₀³ 分成 5×3×2 标准格胞，分类每胞内可共存的起点，并把双占胞的超额单射充给其 x 方向后继胞。；设格胞基准权为 λ。胞内唯一能共存的两点是低角与高角，双占贡献 λ(1+1/720)。双占会禁止 x 后继胞的低角；后继胞至多含一个非低角点，故相对其基准 λ/32 至少亏损 λ/64。因 1/64>1/720 且后继映射单射，总超额不超过总亏损。
- **等号情形与有限边界攻击**（advanced）：追踪充电中的严格余量，并用有限盒 MILP 搜索截断反例。；任何双占胞均产生严格净亏损；没有双占时，等号要求每胞恰取低角。因此等号唯一为标准格。另一方面，有限盒最后一胞可双占，确能超过同范围的截断标准格；这反驳了直接从有限截断最优推出无限定理的错误版本，但空的无限后继胞提供足够亏损。
- **分数重叠推广的初步证伪**（inconclusive）：对有限支持起点权 θ 建立点负载不超过 1 的线性规划，搜索权和超过 450/403 的方案。；在 385 起点和 1120 起点两个窗口中，HiGHS 均返回标准格的整数截断，较大窗口目标为 1.116619285599，低于无限标准值 450/403≈1.116625310174。由于这是浮点有限窗口结果，不能证明分数推广。

#### 第二轮新增严格进展

- [第二轮新增] 证明加权穿孔盒定理：若 C⊂ℕ₀³ 且平移族 {c+B*:c∈C} 两两不交，其中 B*=[0,4]×[0,2]×[0,1]∖{(0,0,0)}，则 Σ_{(r,s,t)∈C}2^{-r}3^{-s}5^{-t}≤450/403。
- [第二轮新增] 加强等号结论：上述不等式取等当且仅当 C={(5i,3j,2k):i,j,k≥0}。
- [第二轮新增] 推出方法类最优性：固定 D=Div(720)∖{1}，在所有仅通过 (v₂,v₃,v₅) 穿孔盒两两不交来选择完整精确赋值类的方案中，缩放因子集合的自然密度至多 120/403；在指数起点集 C 的层面，标准模 (5,3,2) 选择唯一达到上界。第一轮 blocking step 的第二部分因此闭合。
- [第二轮复核加固] 穷举所有局部差向量并直接计算平移集合交集，确认穿孔盒不相交的满盒重叠例外恰为差向量 ±(4,2,1)；混合符号角差仍相交。

#### 证伪与边界检查

- 发现有限截断边界陷阱：3×3×3 格胞 MILP 在末胞同时选择低、高两角，故有限最优值可严格超过同范围截断标准格；第一轮有限 MILP 本身不能证明无限定理。
- 无限证明没有同一边界漏洞：每个双占胞的 x 后继仍属于 ℕ₀³；若 C 在该后继胞无点，空胞的完整基准权即计入亏损。
- 无穷加权求和合法：所有权非负，且格胞基准总和是收敛几何级数；自然密度另用一致尾部控制——截去 r≥R、s≥S 或 t≥T 的赋值类后，尾并集包含于 2^Rℕ∪3^Sℕ∪5^Tℕ，上密度至多 2^{-R}+3^{-S}+5^{-T}。
- 唯一性已逐项检查：双占胞造成 λ(1/64−1/720)>0 的严格净亏损；无双占时，空胞或非低角单点也产生正亏损。这里的唯一性严格限定于指数起点集 C（或选中类全部纳入的精确赋值类方案），不声称任意实际整数子集逐点唯一。
- 新定理只排除重新铺排固定 720 块的不交起点，不能比较其他 divisor blocks，也不覆盖分数重叠块；因此没有改善 667/806，更没有推出 1/2。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/verify_punctured_box.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/verify_punctured_box.py)：纯 Fraction 局部证书：以直接集合相交独立核对闭式冲突判据，并验证胞内唯一兼容对、1/720 与 1/64 常数、450/403 和 120/403。SHA-256：1eb066c99003c5c94c019eec1bdce19ecb7d94a3f0b1e831a5b83eeab9583646。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301 && python3 -u verify_punctured_box.py；结果：全部精确断言通过：cell_points=30，唯一兼容对为 ((0,0,0),(4,2,1))，double_excess_ratio=1/720，forced_successor_deficit_ratio=1/64。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/crosscheck_punctured_box_milp.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/crosscheck_punctured_box_milp.py)：独立有限盒 HiGHS 反例搜索，并以 Fraction 重算选集权重和无限充电恒等式；用于发现截断边界陷阱。SHA-256：5de87e35e6761ce215cc12484cb9c715425465062a3c67d1128c50168259c173。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301 && python3 -u crosscheck_punctured_box_milp.py --cells 3 3 3；结果：HiGHS optimal；810 点、35090 冲突；末胞 (2,2,2) 双占。Fraction 重算确认相对无限标准权 450/403 仍有 excess≤deficit。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/search_fractional_overlap.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301/search_fractional_overlap.py)：有限支持分数块负载 LP 的反例搜索器。该项是浮点探索，不作为严格最优性证书。SHA-256：2f67f3fbafd48cf88f57ae640db93835a82371c1dba92979a4819559d66b3ec0。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/301 && python3 -u search_fractional_overlap.py --limits 10 6 4 && python3 -u search_fractional_overlap.py --limits 15 9 6；结果：两个窗口均未找到超过标准格的分数方案；1120 起点窗口返回64个标准格点，目标 1.116619285599。

#### 当前障碍

固定 720 块的“不交赋值铺排是否可更密”已不再是缺口。余下障碍是没有结构或覆盖定理迫使任意密度大于 1/2 的集合在可控的单位分数块族中产生足够遗漏。允许块重叠并作分数负载计数，以及更换有限配置，均未被本轮排除。

#### 下一精确定理

精确的下一定理是分数穿孔盒不等式：若 θ:ℕ₀³→[0,∞) 满足对每个 x∈ℕ₀³，Σ_{b∈B*, b≤x}θ(x−b)≤1，则证明 Σ_c θ(c)2^{-c₁}3^{-c₂}5^{-c₃}≤450/403。若成立，将封死固定 720 配置连同所有非负分数重叠权的改进；若存在严格大于 450/403 的有限支持有理反例，则按遗漏系数 (4/15)(139/240)Σ_cθ(c)w(c) 会严格改善 139/806。

#### 第二轮证明记录

【承接的第一轮事实】令 D=Div(720)∖{1}。其 (v₂,v₃,v₅) 指数图像为 B*=[0,4]×[0,2]×[0,1]∖{0}。Wang 预印本 Theorem 1 使用标准起点格 (5i,3j,2k)，其缩放因子密度为 120/403；结合前缀加权遗漏 139/240，得到 f(N)≤(667/806+o(1))N。本轮不把这些既有常数重写为新增结果。

【第二轮新增推导】写 w(r,s,t)=2^{-r}3^{-s}5^{-t}。两个 B* 平移相交，当且仅当其起点差 Δ 满足逐坐标 |Δ|≤(4,2,1)，且 Δ≠±(4,2,1)。满盒相交给出坐标条件；只有全正或全负的极端对角交点恰为某一平移中被删去的原点，混合符号角仍属于两个穿孔盒。

分割
Q_{ijk}=(5i,3j,2k)+[0,4]×[0,2]×[0,1],
并令 λ_{ijk}=w(5i,3j,2k)。在同一胞内，唯一不冲突的不同两点是低角 L 与高角 U=L+(4,2,1)。因此 C∩Q 至多有两点；双占时必为 {L,U}，贡献
λ(1+w(4,2,1))=λ(1+1/720)。
非双占胞贡献至多 λ，记相对 λ 的亏损为 δ_Q≥0。

若 Q_{ijk} 双占，则 U 与后继胞 Q_{i+1,j,k} 的低角 L'=L+(5,0,0) 之差为 (1,−2,−1)，所以冲突。后继胞不能双占；若含一点，由于低角缺失，其最大相对权为 w(1,0,0)=1/2。其贡献至多
(λ/32)(1/2)=λ/64，
故相对自身基准 λ/32 的亏损至少 λ/64。后继映射 Q_{ijk}↦Q_{i+1,j,k} 单射，且双占胞不可能成为这种后继。因此
Σ_{Q双占}λ_Q/720≤Σ_{Q双占}λ_Q/64≤Σ_{Q非双占}δ_Q。
逐胞求和得到
Σ_{c∈C}w(c)=Σ_Qλ_Q+Σ_{Q双占}λ_Q/720−Σ_{Q非双占}δ_Q≤Σ_Qλ_Q。
几何级数给出
Σ_Qλ_Q=1/[(1−2^{-5})(1−3^{-3})(1−5^{-2})]=450/403。
所有项非负且基准和收敛，故有限截断后以单调收敛取极限即处理无限尾部。

标准格每胞恰取低角，达到等号。若存在双占胞，则 1/64>1/720 给出严格亏损；若无双占而总和取等，则所有 δ_Q=0，只能每胞恰取低角。因此等号方案唯一。

固定赋值 c 的整数具有自然密度
(1−1/2)(1−1/3)(1−1/5)w(c)=(4/15)w(c)。
更严格地，把赋值截在有限盒；尾并集包含于 2^Rℕ∪3^Sℕ∪5^Tℕ，其上密度至多 2^{-R}+3^{-S}+5^{-T}→0。故任何由不交 B* 平移、并纳入完整精确赋值类的缩放族密度至多
(4/15)(450/403)=120/403，在指数起点集 C（或完整精确赋值类方案）的层面，标准赋值格唯一取等。这严格完成了第一轮 next theorem，但没有改变 f(N) 的上下界。

【仍未闭合的缺口】官网问题量化于所有无禁式 A；本轮只优化固定 D 的一类不交缩放法。允许块重叠并以负载权计数，或使用其他更强配置，仍可能改善 667/806。没有步骤把上界降到更小常数，更没有闭合到 1/2。

【来源成熟度与潜在优先权】官网仍标 open 且只记录 25/28。667/806 来自 2026-05-27 作者预印本，尚未见同行评审版本；其 Section 5 明说不声称 720 配置最优。本轮检索到的一手来源中未找到上述加权穿孔盒定理或等号唯一性的既有陈述；这只能表明有限检索未发现优先文献，不能据此断言原创性。

#### 本轮核查来源

- [Erdős Problems #301](https://www.erdosproblems.com/301)；一手来源：true；核验：核实官网精确使用等号，状态仍为 open；页面记录 N/2 下界和 van Doorn 的 25/28 上界，最后编辑日期为 2026-01-16。
- [Xinjun Wang, A 667/806 Upper Bound for Erdős Problem #301 on Unit-Fraction-Free Sets](https://doi.org/10.5281/zenodo.20404609)；一手来源：true；核验：作者上传的 2026-05-27 预印本中，Theorem 1 声称 f(N)≤(667/806+o(1))N；Lemma 2–3 使用标准赋值格并给出密度 120/403；Section 5 明确不主张 720 配置最优。该文尚非同行评审论文。
- [P. Erdős and R. L. Graham, Old and New Problems and Results in Combinatorial Number Theory (1980)](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf)；一手来源：true；核验：确认作者托管的原书 PDF 地址，但本轮正文抓取仍返回 502；未能定位本题在原书中的精确页码，故不声称复核了原书逐字命题。

### #325

- 第一轮障碍：原问题仍被3≤k≤10阻塞。现有结果没有给这些次数的 B^{3+o(1)} 全盒或混合能量；尤其 k=3 的最佳混合能量仍损失 δ₆=0.24871567。另一个文献性阻塞是尚未找到 Salberger 2019、k≥11 改进的完整证明论文。
- 第一轮下一定理：对每个固定3≤k≤10，构造集合 S_{1,B},S_{2,B},S_{3,B}⊂[1,B]，满足 |S_{1,B}||S_{2,B}||S_{3,B}|≥B^{3−o(1)}，并证明 E_k(S_1,S_2,S_3):=#{(a_i,b_i)∈S_i^2:∑_{i=1}^3a_i^k=∑_{i=1}^3b_i^k}≤B^{3+o(1)}。这将逐量词推出弱版本；若三个集合有固定正密度且 E_k≪_kB^3，则推出强版本。
- 第二轮用时：949.7 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：直接攻击第一轮的低次混合能量阻塞：核查四次幂光滑 Weyl 和的已发表六次矩，并将其逐量词转化为 f_{4,3}(x) 的显式下界；同时以两种独立枚举实现主动搜索小盒反例。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核第二轮 k=4 推论：对每个 ε>0，f_{4,3}(x)≫_ε x^(0.704143−ε)，其中 0.704143=(6−3.183428)/4。复核覆盖 Brüdern–Wooley 混合六次矩的一手陈述、光滑变量基数、正交性能量解释、Cauchy–Schwarz 指数、P 与 x 的截断以及所有依赖常数和 ε 量词。
- 复核方式：直接阅读 2000 年一手论文 Theorem 2 及其 permissible exponent 定义，不以第二轮摘要为前提；独立重建光滑数子集和 Cauchy 指数链；检查正整数构造到题面非负整数计数的包含关系；重跑两套矩枚举与 CSV 验证；把所有有限 B 数据严格降格为证伪检查。未改动其他题文件。
- 证据边界：PASS 表示本候选推论的数学链条在当前独立审计中成立，不等同于文献优先权确认、同行评审新结果或原题解决。对外稿应逐字引用 permissible exponent 的 τ/η 定义，并继续把有限计算标为证伪工具。

#### 第二轮实际尝试

- **四次幂经典×光滑×光滑混合能量**（advanced）：把 Brüdern–Wooley Theorem 2 的 s=6 积分按正交性解释为集合 [1,P]×A(P,P^η)×A(P,P^η) 的二阶能量，再应用 Cauchy–Schwarz。；若 A=A(P,P^η)，M=P|A|²，能量 E≤P^{3.183428+τ}。对任意 ρ>0，用分属若干互不相交素数区间的乘积可构造 |A|≫_ρP^{1−ρ}，故像集大小至少 P^{6−4ρ−3.183428−τ}=P^{2.816572−4ρ−τ}。取 P=⌊(x/3)^{1/4}⌋并令 ρ,τ 任意小，得到 f_{4,3}(x)≫_ε x^{0.704143−ε}。
- **光滑数基数的量词闭合**（advanced）：不把“光滑数有正密度”作为未引用黑箱；改用素数定理和唯一分解构造足够多的 P^η-光滑整数。；给定 ρ>0，取 Jη>1，并选互不相同的 0<a_j<η，使 Σa_j>1−ρ/2 且 Σa_j<1。分别从 [P^{a_j},2P^{a_j}] 取一个素数。其乘积对充分大 P 不超过 P、所有素因子不超过 P^η，且由唯一分解互不相同；素数定理给数量 P^{Σa_j}/(log P)^J≫P^{1−ρ}。
- **四次幂后续矩估计搜索**（blocked）：核查 2023 年同行评审论文列出的纯光滑四次幂可容许指数。；Lemma 2.1 的纯光滑六次矩指数为 3.1835，高于混合矩 3.183428；较新的高阶矩结果不能通过直接代入改善这个六变量能量。
- **题名相似论文的反向核验**（refuted）：逐式检查 Robert 2011，而不依据题名“somme de trois puissances”判断适用范围。；其次数向量始终为 (2,ℓ₁,ℓ₂)，所以即使取 ℓ₁=ℓ₂=k，也仍含平方变量；它不覆盖 (k,k,k)，排除了一个可能造成错误“已解决”结论的文献假阳性。
- **扩大精确小盒反例搜索**（inconclusive）：枚举 k=3,4,5,6 与 B=8,120,160,200；第一实现按无序三元组及置换权计能量，第二实现对 B=120 独立汇总有序二元和。；k=4 时 R₄(B)/B³ 在 B=120,160,200 分别为 6.0492778、6.0544243、6.0533980，非置换能量/B³ 分别为 0.1240000、0.1105181、0.0982980。没有出现反驳近对角能量的有限迹象，但这些数据不能证明渐近界。

#### 第二轮新增严格进展

- [第二轮新增] 对每个 ε>0，严格得到 f_{4,3}(x)≫_ε x^{0.704143−ε}。这里 0.704143=(6−3.183428)/4；正整数表示是题面非负整数表示的子集，P=⌊(x/3)^{1/4}⌋闭合了 x 截断。
- [第二轮新增] 该 k=4 指数严格强于全盒 Hua 插值路线给出的 x^{5/8−ε}=x^{0.625−ε}，提高 0.079143；但仍低于弱猜想临界指数 3/4，指数缺口为 0.045857。常数允许依赖 ε，故没有得到强版。
- [第二轮复核加固] k=4、B=120 的第二矩由两种独立算法均得到 10453152，不同和值均为 292356；k=3,5,6 的 B=120 结果也逐项一致。
- [第二轮复核加固] 在所核查的一手后续文献中，纯光滑六次矩指数 3.1835 并未击穿混合矩 3.183428；因此将“使用较新光滑 Weyl 和论文即可达到 P^{3+o(1)}”作为下一步会失败。

#### 证伪与边界检查

- 有限计算主动测试了 k=4 混合能量路线可能遭遇的大量非置换碰撞；B≤200 未见能量比值呈幂次爆炸，但有限样本不能排除对数增长或极小正幂。
- k=3 的 R₃(B)/B³ 从 B=120 的 7.5525972 增至 B=200 的 7.7022940，故计算没有支持把 k=3 全盒能量直接视为 O(B³)；也没有反驳 B^{3+ε}。
- k=4 数据中的 R₄(B)>6B³，说明不能把置换对角公式误当全部能量；本轮推导使用已证明的混合矩上界，没有忽略这些非对角解。
- Robert 2011 的相似题名已由正文次数条件排除，不能作为三个相同 k 次幂的定理。
- Salberger 2019 对 k=5,…,10 的 δ_k 未显式给出；因此没有伪造数值指数表，也没有把作者会议报告升级成完整同行评审证明。
- 没有找到一手论文明确把 Brüdern–Wooley Theorem 2 表述为本题 f_{4,3} 的 0.704143 下界；本轮只主张这是由该定理推出的严格推论，不主张文献优先权或世界纪录。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/second_round_moments.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/second_round_moments.py)：按无序三元组枚举和值，以置换重数 1、3、6 恢复有序二阶矩，并在小 B 上与笛卡尔积暴力法核验。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325 && python3 -m py_compile second_round_moments.py verify_moment_csv.py && python3 second_round_moments.py --ks 3 4 5 6 --Bs 8 120 160 200 --crosscheck-max 8 --output second_round_moments.csv && python3 verify_moment_csv.py second_round_moments.csv；结果：生成并核验 16 行精确数据；每行有序三元组总权重均等于 B³。脚本 SHA-256 为 d5c8370b5ba8074b3038afc22b1d72dec62ba3898e65198a08d6b67efe46f1cf。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/crosscheck_pair_sums.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/crosscheck_pair_sums.py)：独立实现：先汇总所有有序二元 k 次幂和，再与第三变量卷积，完全不使用无序三元组或置换权公式。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325 && python3 -m py_compile crosscheck_pair_sums.py && python3 crosscheck_pair_sums.py --ks 3 4 5 6 --B 120；结果：B=120 时 k=3,4,5,6 的（不同和值，二阶矩）分别为 (260416,13050888)、(292356,10453152)、(295233,10239384)、(295231,10239528)，与第一实现逐项一致。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/second_round_moments.csv](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325/second_round_moments.csv)：第二轮 k=3,4,5,6、B=8,120,160,200 的精确矩数据，包含置换对角、非对角能量和归一化比值。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/325 && sed -n '1,17p' second_round_moments.csv；结果：文件 SHA-256 为 230acf6822df84905c4e2d757104a5dc4c00838d44ada22aaff11f44ac41747a。

#### 当前障碍

原题仍被 k=3,…,10 阻塞；本轮只改善了 k=4。对 k=4，现有混合能量损失为 δ=0.183428，故只能得到 P^{3−δ} 个和值，而弱猜想需要 P^{3−o(1)}。k=3 仍有第一轮记录的 δ₆=0.24871567；对 k=5,…,10 也未定位到足以给出 B^{3+o(1)} 的全盒或稠密混合能量。

#### 下一精确定理

最清晰且最窄的下一定理是四次幂混合六次矩：对每个 τ>0，证明存在 η=η(τ)>0，使 R=P^η 时，F₄(α;P)=Σ_{n≤P}e(αn⁴)、f₄(α;P,R)=Σ_{n≤P,\,p|n⇒p≤R}e(αn⁴) 满足 ∫₀¹|F₄(α;P)|²|f₄(α;P,R)|⁴dα≪_τ P^{3+τ}。结合本轮已闭合的光滑集合基数论证，这将逐量词证明 k=4 的弱版本。若进一步得到无 P^τ 损失的 O(P³)，并使用固定 η 下光滑数的正密度，则可推出 k=4 强版本。

#### 第二轮证明记录

承接的第一轮事实

固定 k，盒表示函数的 Cauchy–Schwarz 归约为
\[
|\operatorname{supp}r|\ge \frac{(\sum_n r(n))^2}{\sum_n r(n)^2}.
\]
第一轮已闭合 k≥26 的已发表强版本以及条件于 Salberger 2019 报告的 k≥11 强版本；这些不是本轮新增。k=3 的最佳已核查指数仍来自经典变量与光滑变量的混合矩，而非全盒近对角估计。

第二轮新增推导

令
\[
\mathcal A(P,R)=\{m\le P:p\mid m\Rightarrow p\le R\},
\quad F(\alpha)=\sum_{n\le P}e(\alpha n^4),
\quad f(\alpha)=\sum_{m\in\mathcal A(P,R)}e(\alpha m^4).
\]
Brüdern–Wooley Theorem 2 的 s=6 情形给：对任意 τ>0，存在 η>0，使 R≤P^η 时
\[
E:=\int_0^1|F(\alpha)|^2|f(\alpha)|^4\,d\alpha
 \ll_\tau P^{3.183428+\tau}. \tag{1}
\]
正交性表明 E 精确计数
\[
a^4+b^4+c^4=a'^4+b'^4+c'^4,
\quad a,a'\le P,
\quad b,b',c,c'\in\mathcal A(P,R). \tag{2}
\]

还需谨慎处理光滑集合大小。给定任意 ρ>0，选 J 使 Jη>1，再选互异的 0<a_j<η，使 1−ρ/2<Σa_j<1。由素数定理，每个区间 [P^{a_j},2P^{a_j}] 含 ≫P^{a_j}/log P 个素数。每区间各取一个素数并相乘；充分大 P 时乘积≤P，所有素因子≤P^η，且唯一分解保证不同选择给不同整数。因此
\[
|\mathcal A(P,P^\eta)|\gg_{\rho,\eta} P^{\sum a_j}(\log P)^{-J}
 \gg P^{1-\rho}. \tag{3}
\]
这里 ρ 可依最终 ε 任意选小。

集合
\[
\{a^4+b^4+c^4:a\le P,\ b,c\in\mathcal A(P,P^\eta)\}
\]
共有 M=P|\mathcal A|^2 个带重数输入。由 (1)–(3)，其不同和值至少为
\[
\frac{M^2}{E}
 \gg P^{6-4\rho-3.183428-\tau}
 =P^{2.816572-4\rho-\tau}. \tag{4}
\]
取 P=⌊(x/3)^{1/4}⌋，所有和值均≤x，且 P≫x^{1/4}。先给定最终 ε>0，再取 ρ,τ>0 使 (4ρ+τ)/4<ε，得到
\[
f_{4,3}(x)\gg_\varepsilon x^{2.816572/4-\varepsilon}
=x^{0.704143-\varepsilon}. \tag{5}
\]
这覆盖了充分大 x、常数依赖、正整数到非负整数的包含关系以及所有 ε>0 的量词。它仍不是题面要求的 x^{3/4−ε}。

来源成熟度与优先权

式 (1) 来自 2000 年完整同行评审论文；式 (3)–(5) 是本轮从该定理作出的推论。2023 年同行评审论文的 Lemma 2.1 仅给纯光滑指数 3.1835，不能改善 (1)。Salberger 的 k≥11 改进仍只定位到作者会议报告。实时检索没有找到明确发表 (5) 的一手来源，故不声称该指数具有文献首创性。

仍未闭合的缺口

对 k=4，从 3.183428 降至 3+o(1) 尚差 0.183428 个 P 指数，对应 x 指数差
\[
\frac{0.183428}{4}=0.045857.
\]
对 k=3 和 k=5,…,10，本轮没有得到 B^{3+o(1)} 的适用混合能量。有限枚举只能排除当前范围内的明显幂次爆炸，不能证明任何所需渐近式。因此官网题面的全部 k≥3 量词仍未闭合。

#### 本轮核查来源

- [Brüdern–Wooley, On Waring's problem: two cubes and seven biquadrates, Tsukuba J. Math. 24 (2000), 387–417](https://www.math.purdue.edu/~twooley/publ/2000%20wp34.pdf)；一手来源：true；核验：Theorem 2 定义四次幂经典和 F(α;P) 与 P^η-光滑和 f(α;P,R)，并给出 s=6 的混合矩 ∫₀¹|F(α;P)|²|f(α;P,R)|⁴dα≪_{ε}P^{3.183428+ε}，其中存在 η>0 且 R≤P^η。该积分恰是一个经典变量、两个光滑变量的等和能量。
- [Brüdern–Wooley, Pairs of Diagonal Quartic Forms: The Non-Singular Hasse Principle, Q. J. Math. 74 (2023), 101–128](https://academic.oup.com/qjmath/article/74/1/101/6633716)；一手来源：true；核验：Lemma 2.1 给纯光滑四次幂六次矩的可容许参数 Δ₆=1.1835，即指数 6−4+Δ₆=3.1835；这略弱于 2000 年混合矩的 3.183428，因而不能用它进一步改善本轮指数。
- [Olivier Robert, Sur le nombre des entiers représentables comme somme de trois puissances, Acta Arith. 149 (2011), 1–21](https://www.impan.pl/shop/en/publication/transaction/download/product/82663)；一手来源：true；核验：正文 (1.4)–(1.5) 固定第一个指数 ℓ₀=2，并假设 2=ℓ₀≤ℓ₁≤ℓ₂；它研究一个平方加两个幂，而非三个相同 k≥3 次幂，不能用于本题。
- [Salberger, Equal sums of three dth powers, Oberwolfach Report 50/2019](https://ems.press/content/serial-article-files/46829)；一手来源：true；核验：Theorem 1 陈述 d≥5 时 n_d(B)=O_d(B^{7/2−δ})、d≥11 时 n_d(B)=6B³+O_d(B^{3−δ})，但 δ 只以存在形式出现；报告没有给出可据以制作 k=5,…,10 数值指数表的显式 δ_d，也仍不是完整证明论文。

### #332

- 第一轮障碍：当前充分条件定理本身没有遗留证明缺口。真正阻塞仍是开放问题的范围：哪些远弱于正上 Banach 密度的条件仍足以保证 D(A) syndetic，尚未刻画。实时检索也未找到明确写出本次“正上 Banach 密度、无限次差集、|B|≤1/δ”三者组合的原命题，因此不能声称新颖性或优先权。
- 第一轮下一定理：下一步可加强为“popular recurrent differences”版本：对 δ=d*(A)>0、0<ε<δ²，证明 R_ε={d∈ℤ:d*(A∩(A−d))>δ²−ε} syndetic。该命题需要完整重建对应原理的不等式方向与 Khintchine 回归，不能由本次有限交论证直接得到。
- 第二轮用时：669.3 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：攻击并闭合上一轮提出的 popular recurrent differences 命题；最终证明更强结论：若 δ=d*(A)>0 且 0<ε≤δ²，则 R_ε={d∈ℤ:d*(A∩(A-d))>δ²−ε} 的下 Banach 密度至少为 ε/(δ−δ²+ε)。特别地，D(A) 的下 Banach 密度至少为 δ。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：若 A⊂ℕ 的上 Banach 密度为 δ>0，且 0<ε≤δ²，则 R_ε={d∈ℤ:d*(A∩(A−d))>δ²−ε} 满足下 Banach 密度至少 ε/(δ−δ²+ε)。取 ε=δ² 得 d_B^−(D(A))≥δ。固定 δ=1/4、ε=1/32 的周期族同时严格否定只依赖 δ,ε 的统一最大间隙常数。
- 复核方式：独立逐式重建 correspondence inequality、Koopman 区间平均和阈值比例代数；从一手论文核对不等式方向及同一系统对所有有限平移同时成立；重跑两份互不调用的周期程序，并手算周期边界族的严格阈值、坏区间长度与半开区间最小 M。未修改原结果或脚本。
- 证据边界：PASS 是对这条正 Banach 密度标准推论的内部独立复核，不等同于新论文结果、Lean 形式化或 Erdős #332 完整闭合。报告将其标为 route_advanced、full_solution_claim=none 是合适的。

#### 第二轮实际尝试

- **对应原理回译方向与同时性**（advanced）：将 A 以零延拓视为 ℤ 的子集，直接应用 ergodic d* 对应原理。；得到遍历系统 (X,μ,T)、E⊆X，μ(E)=δ，且对每个 d∈ℤ 同时有 c(d):=μ(E∩T^{-d}E)≤d*(A∩(A-d))；若平移约定给出 A∩(A+d)，其与 A∩(A-d) 仅差整体平移和 d↦−d。
- **一致区间平均而非单点 Khintchine**（advanced）：对 f=1_E 使用 von Neumann 均值遍历定理，并保留区间起点 m 的一致性。；遍历性给出 N^{-1}∑_{j=0}^{N-1}U^jf→δ·1 于 L²。乘以 U^m 不改变范数，因此 sup_m|N^{-1}∑_{n=m}^{m+N-1}c(n)−δ²|→0。这比只证明每个长区间有一个回归时刻更强。
- **高相关时刻的比例计数**（advanced）：利用 0≤c(d)≤δ，而非仅利用平均值。；令 α=δ²−ε，G_ε={d:c(d)>α}，p_{m,N}=|G_ε∩[m,m+N)|/N。区间相关平均≤α+(δ−α)p_{m,N}；与一致极限 δ² 比较，得到下 Banach 密度 G_ε≥(δ²−α)/(δ−α)=ε/(δ−δ²+ε)。对应原理给出 G_ε⊆R_ε。
- **端点 ε=δ² 与 D(A)**（advanced）：把阈值降到严格正交密度。；ε=δ² 时 R_ε={d:d*(A∩(A-d))>0}，其下 Banach 密度至少 δ。正上 Banach 密度为正的交集是无限集，故每个这类 d 都由无穷多个 A 中有序对实现，因此 R_ε⊆D(A)。
- **固定参数周期族攻击统一 gap 界**（refuted）：取 q∈32ℕ，A_q={n≥0:n mod q∈{0,…,q/4−1}}，固定 δ=1/4、ε=1/32。；若 r=min(d mod q,q−(d mod q))，则交密度为 max(q/4−r,0)/q。popular 条件是 r<7q/32；其补集有 9q/16+1 个连续整数，故半开区间版本的最小命中常数为 M=9q/16+2→∞。
- **双实现有限周期穷举**（advanced）：分别用显式集合配对和循环位旋转计算所有周期相关数及全部临界阈值。；对每个 S⊆ℤ/qℤ 验证 ∑_d|S∩(S-d)|=|S|²，并以整数交叉乘法验证 popular-set 密度下界；两实现生成相同规范摘要。

#### 第二轮新增严格进展

- [第二轮新增] 若 δ=d*(A)>0 且 0<ε≤δ²，则下 Banach 密度满足 d_B^-(R_ε)≥ε/(δ−δ²+ε)。这严格强于上一轮 next theorem 仅要求 R_ε syndetic；假设、ε 范围及严格阈值均已逐项闭合。
- [第二轮新增] 取 ε=δ² 得 d_B^-({d:d*(A∩(A-d))>0})≥δ，进而 d_B^-(D(A))≥d*(A)。因此第一轮的“D(A) syndetic”在相同假设下被强化为带显式密度下界。
- [第二轮复核加固] 第一轮 blocking step 已由 Theorem 2.8 式 (2.6) 严格消除：模型相关测度从下方控制原集合交集的上 Banach 密度，而且所有 d∈ℤ 同时成立，不存在逐 d 更换窗口的问题。
- [第二轮新增] 固定 δ=1/4、ε=1/32 时，popular set 的最小 gap 常数仍可随周期 q 线性增大；故上述密度下界不能升级为只依赖 δ,ε 的统一有限 gap 常数。

#### 证伪与边界检查

- A⊆ℕ 的零延拓不改变其上 Banach 密度：远离原点的正向区间仍给出原上确界，跨越或落在负半轴的区间不能增大密度。
- 负差没有遗漏：D(A) 对称，且 d*(A∩(A-d))=d*(A∩(A+d))，因为两集合相差整体平移。
- 严格不等号已保留：c(d)>α 与 d*(交集)≥c(d) 合成后仍有 d*(交集)>α。
- ε=δ² 端点合法：阈值恰为 0，positive upper Banach density 直接保证交集无限；没有把一次出现误当成无限出现。
- δ=1 时模型 E 满测度，所有 c(d)=1，因而 R_ε=ℤ，公式下界为 1；没有分母退化。
- 周期反例族中 D(A_q) 和各交密度均由周期重复无限实现，不是有限窗口伪反例。
- 两种程序在 q≤16 的全部 131054 个非空周期模式、1062504 个阈值检查上均通过，且 SHA-256 完全相同。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332/periodic_popular_enum.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332/periodic_popular_enum.py)：显式集合实现；穷举周期模式、验证相关平均与密度下界，并输出固定参数反统一-gap 家族。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332 && python3 -m py_compile periodic_popular_enum.py && python3 periodic_popular_enum.py --max-q 16；结果：PASS：131054 个模式、1062504 个阈值；摘要 0b01491d19a0ad5f39248d3a67d73c44fed933cc91ed24355c35eaaf27d27f84。边界族的最小 M 从 q=32 时20增至 q=320 时182。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332/periodic_popular_bitset.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332/periodic_popular_bitset.py)：独立循环位旋转实现，不调用第一份脚本的相关数或阈值检查逻辑。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/332 && python3 -m py_compile periodic_popular_bitset.py && python3 periodic_popular_bitset.py --max-q 16；结果：PASS：模式数与阈值数相同；独立摘要同为 0b01491d19a0ad5f39248d3a67d73c44fed933cc91ed24355c35eaaf27d27f84。

#### 当前障碍

正上 Banach 密度路线本身已无证明缺口。真正阻塞转移到官网问题的开放范围：尚未刻画哪些 d*(A)=0 的稀疏集合条件仍足以迫使 D(A) syndetic 或具有正密度。本轮检索到 Stewart–Tijdeman 的自然密度版本及成熟的 popular-recurrence 理论，但未在核查的一手来源中找到逐字写出的“d_B^-(D(A))≥d*(A)”原命题；它应视为这些标准工具的推论，不能主张新颖性。

#### 下一精确定理

下一条真正超出本路线自动推论的目标应进入零 Banach 密度区域：寻找一个明确的局部能量或增长条件 C(A)，满足 d*(A)=0 仍可证明 d_B^-(D(A))>0；第一步需测试候选条件是否排除 Sidon 型集合、超指数序列及分块稀疏构造。

#### 第二轮证明记录

承接的第一轮事实

第一轮已经证明：若 d*(A)=δ>0，则存在有限 B⊆ℤ，|B|≤⌊1/δ⌋ 且 ℤ=B+D(A)，从而 D(A) syndetic。本轮不把这一覆盖结论计作新增进展。第一轮留下的实质问题是，能否证明
R_ε={d∈ℤ:d*(A∩(A-d))>δ²−ε}
本身 syndetic，以及对应原理能否严格回译到“差出现无穷多次”。

第二轮新增推导

将 A 以零延拓视为 ℤ 的子集。由 Bergelson–Ferré Moragues Theorem 2.8，存在遍历保测 ℤ-系统 (X,μ,T) 和 E∈𝔅，使 μ(E)=δ，并且对每个 d∈ℤ 同时有
c(d):=μ(E∩T^{-d}E)≤d*(A∩(A-d)).
平移符号约定若产生 A∩(A+d)，不影响结论，因为 d*(A∩(A+d))=d*(A∩(A-d)) 在 d↦−d 后相同。

令 f=1_E，U 为相应 Koopman 酉算子。遍历性与均值遍历定理给出
‖N^{-1}∑_{j=0}^{N-1}U^jf−δ·1‖₂→0.
对任意区间起点 m，
N^{-1}∑_{n=m}^{m+N-1}c(n)=⟨f,U^m(N^{-1}∑_{j=0}^{N-1}U^jf)⟩.
由于 U^m 是等距算子，右侧趋于 ⟨f,δ·1⟩=δ²，且误差对所有 m 一致。这一步闭合了 syndetic 所需的“每个平移区间”量词，而非只得到从原点出发的 Cesàro 平均。

取 0<ε≤δ²，置 α=δ²−ε，并令 G_ε={d:c(d)>α}。记
p_{m,N}=|G_ε∩[m,m+N)|/N.
因为 0≤c(d)≤δ，故
N^{-1}∑_{n=m}^{m+N-1}c(n)≤α+(δ−α)p_{m,N}.
将上一段的一致极限代入并先对 m 取下确界，再令 N→∞，得到
\underline d_B(G_ε):=liminf_{N→∞}inf_{m∈ℤ}p_{m,N}
≥(δ²−α)/(δ−α)=ε/(δ−δ²+ε).
对应原理的不等式给出 G_ε⊆R_ε，所以同一下界适用于 R_ε。正下 Banach 密度蕴含 syndetic，故上一轮 next theorem 完全闭合。

更进一步，取 ε=δ²，则 α=0，
\underline d_B({d:d*(A∩(A-d))>0})≥δ.
若 d*(A∩(A-d))>0，该交集无限；每个 x∈A∩(A-d) 给出有序对 (x+d,x)∈A²，且差为 d。因此该 popular set 包含于 D(A)，从而
\boxed{\underline d_B(D(A))≥d*(A)=δ.}
这在相同假设下严格强化了第一轮的纯 syndetic 结论。

边界攻击方面，令 q=32k，A_q 周期性取余数 0,…,q/4−1。固定 δ=1/4、ε=1/32。若 r 是 d 到 qℤ 的距离，则
 d*(A_q∩(A_q-d))=max(q/4−r,0)/q.
因此 d∈R_ε 当且仅当 r<7q/32。一个周期内补集存在 9q/16+1 个连续整数，故 Lean 半开区间定义下的最小命中长度为
M_q=9q/16+2→∞.
所以不存在只依赖 δ,ε 的统一 gap bound；这与每个固定 A_q 的 R_ε syndetic 及统一正下密度界并不矛盾。

仍未闭合的缺口

官网题面询问“哪些条件”，不是指定 d*(A)>0 的单一命题。本轮只完成并强化了这一条充分条件路线，没有触及 d*(A)=0 时的最优条件，也没有刻画充分条件的必要性。因此不能标为完整解决。

来源成熟度与潜在优先权

Stewart–Tijdeman 1979 的 Corollary 1 已在正上自然密度假设下证明下自然密度 D≥上自然密度 A；Griesmer 2019 明确定义同一 popular difference set，并记载其经典回归结构；Bergelson–Ferré Moragues 2020 提供本轮采用的精确 ergodic d* 对应原理。因此本轮的 Banach-density 表述虽比第一轮严格推进，也未在本次核查的一手来源中找到逐字同命题，但应视为成熟理论的直接推论，绝不主张新颖性。

#### 本轮核查来源

- [Erdős Problems #332](https://www.erdosproblems.com/332)；一手来源：true；核验：页面仍标记 OPEN；精确问题及进一步的“D(A) 有正密度”等方向未有评论声称解决。页面最后编辑于 2025-10-28。
- [Stewart–Tijdeman, On Infinite-Difference Sets](https://doi.org/10.4153/CJM-1979-085-6)；一手来源：true；核验：p.898 Theorem 2 给出正上自然密度时的有限平移覆盖；p.902 Lemma 2 与 Corollary 1 更已证明非负 infinite-difference set 的下自然密度至少为 A 的上自然密度。因此“差集具有正密度”在正上自然密度假设下是旧结果。
- [Bergelson–Ferré Moragues, An ergodic correspondence principle, invariant means and applications](https://arxiv.org/abs/2003.03029)；一手来源：true；核验：Theorem 2.8（Theorem 1.4 的 amenable-group 版本）给出 ergodic d* 对应原理。式 (2.6) 对所有群元素同时成立，并给出模型有限交测度≤相应组合有限交的上 Banach 密度，正是本轮回译所需方向。
- [Bergelson–Ferré Moragues, Uniqueness of a Furstenberg system](https://arxiv.org/abs/2005.07295)；一手来源：true；核验：Theorem 1.1 明确说明沿同一 Følner 子列，所有有限平移交的局部密度极限同时等于模型柱集交测度；这独立核实了第一轮 blocking step 中担心的对角抽取量词。
- [Griesmer, Recurrence, rigidity, and popular differences](https://arxiv.org/abs/1509.03901)；一手来源：true；核验：§2.4 定义 P_c(A)={n:d*(A∩(A−n))>c}，与本轮对象完全一致；p.4 还记载 c<μ(E)² 时模型 popular recurrence set 含 Bohr neighborhood 去掉上 Banach 密度零集的经典结构。因此本路线属于成熟回归理论，不能声称文献优先权。
- [FormalConjectures Erdős 332 definition](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/332.lean)；一手来源：true；核验：本地版本确认 D_A 使用有符号整数差和无限有序对；HasBoundedGaps 使用每个半开区间 [z,z+M) 命中的定义。文件仍为 answer(sorry) 占位。

### #377

- 第一轮障碍：必须联合控制素数大小和位数层，保留同一个 n 在不同层之间的相关性。固定素数族 \(n=(p^k-1)/2\) 表明，任何逐层取最坏情形再用可求和上界的策略都必然失败。现有的一位指数和估计也不能控制小素数的全部 base-p 数字。
- 第一轮下一定理：精确的下一定理应是“小素数核心引理”：证明存在绝对常数 \(A\)，使所有 \(n\) 都满足 \[\sum_{p\le n^{1/3}\atop p\nmid\binom{2n}{n}}\frac1p\le A.\]这一定理不会被固定素数显式族反驳，并与 Mertens 的 \(n^{1/3}<p\le n\) 常数界合并后闭合原题全部量词。证明它必须对 \((p,j)\) 二维区域整体估计，而不能逐层取 \(\sup_n\)。
- 第二轮用时：842.5 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：检验“小素数核心引理”能否由有限个 base-p 低位条件推出；搜索小素数同时零进位的峰值；把幸存缺口压缩为兼容固定素数反例的 dyadic 点态计数命题。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：第二轮三项条件性/障碍结果：零进位素数的最高位必要区间、任意固定 D 位截断核心和无界、以及局部计数命题 (L) 若成立则经 dyadic 求和闭合核心与原题；不包括 (L) 本身的证明。
- 复核方式：从 Legendre 每层余数公式重新推导数字判据和端点；独立检查固定深度乘积构造；逐块写出 (L) 的倒数和常数并与第一轮 Mertens 尾部拼接；重编译并以合理子规模交叉运行两套核心扫描、两套稀疏搜索及 Legendre 验证器。
- 证据边界：命题 (L) 目前没有证明，尤其 P=n^{o(1)} 的小素数块仍是核心障碍；本核验只确认‘若 (L)，则原题’的逻辑。固定 D 无界说明任何有限数字截断都不足，但不反驳使用随 log n/log p 增长深度的方法。全部计算都是有限证伪搜索，不能支持全局有界结论。因此 Erdős #377 仍开放，本轮结论应保持 route_advanced、full_solution_claim=none。

#### 第二轮实际尝试

- **最高位必要区间加固**（advanced）：令 \(k=\lfloor\log n/\log p\rfloor\)，利用全部 \(k+1\) 个数字的最大可能值。；若 \(p\nmid B_n\)，则 \[p^k\le n\le \frac{p-1}{2}(1+p+\cdots+p^k)=\frac{p^{k+1}-1}{2},\]故 \[(2n+1)^{1/(k+1)}\le p\le n^{1/k}.\]端点在 \(n=(p^{k+1}-1)/2\) 取到。该条件比纯位数层更窄，但单独逐层求和仍不产生可求和界。
- **证伪任意固定数字深度截断**（refuted）：只保留前 D 个低位无进位条件，并用素数乘积构造。；定义 \(T_D(n,p):n\bmod p^a\le(p^a-1)/2\;(1\le a\le D)\)。给定任意 \(M\)，取有限奇素数集 \(S\) 使 \(\sum_{p\in S}1/p>M\)，令 \(P=\prod_{p\in S}p\)、\(m=\max(D,3)\)、\(n=P^m\)。则每个 \(p\in S\) 满足 \(p^D\mid n\)，故全部 D 个截断条件成立；同时 \(p^3\le n\)。所以截断核心和至少为 \(\sum_{p\in S}1/p>M\)。
- **检验近年多基底小数字定理**（blocked）：逐项比较“坏数字为零”和“坏数字为 o(log n)”的量词。；Bloom–Croot Theorem 1 即使允许任意固定多个充分大基底，也只控制坏数字数目；Kummer 下这对应低 p-adic 重数，而本题需要重数严格等于0。因此该结果不能控制 f(n)，但说明仅证明坏数字比例趋零仍远远不够。
- **核心和双实现穷举**（advanced）：实现 p-adic 递推扫描与逐 (n,p) base-p 数字直接检查两套独立程序。；两套程序对所有 \(n\le2\times10^7\) 的纪录文件逐字节一致。核心纪录依次为 \(1,27,252,756,3160\)，最大值 \(g(3160)=1/3+1/5+1/7+1/11=0.767099567099567\ldots\)。
- **3、5、7 同时零进位稀疏搜索**（inconclusive）：分别用 ternary 位掩码和递归 DFS 枚举全部 \(n\le10^{12}\) 的 ternary 0/1 数，再直接检查 base 5、7。；两实现均得到16个候选同时满足3、5、7零进位，纪录输出逐字节一致；其核心最大值仍在 n=3160。该有限结果没有排除远处峰值。
- **提炼兼容固定素数反例的 dyadic 充分命题**（advanced）：把核心素数按 \((P,2P]\) 分块，同时保留一个容纳固定素数族的常数项。；若存在绝对常数 K，使所有 \(n\ge8\)、\(2\le P\le n^{1/3}\) 均有 \[\#\{P<p\le\min(2P,n^{1/3}):p\nmid B_n\}\le K\left(1+\frac{P}{\log n}\right),\tag{L}\]则每块倒数和至多 \(K(1/P+1/\log n)\)。对 \(P=2^j\) 求和，第一项为收敛几何级数，第二项只有 \(O(\log n)\) 项，故核心和为 \(O(K)\)，进而原题成立。

#### 第二轮新增严格进展

- [第二轮新增] 得到精确最高位必要区间：若 \(k=\lfloor\log_p n\rfloor\) 且 \(p\nmid\binom{2n}{n}\)，则 \((2n+1)^{1/(k+1)}\le p\le n^{1/k}\)；两端点及整数不等式已核对。
- [第二轮新增] 严格证明对每个固定 \(D\ge1\)，只检查前 D 个低位的截断核心和一致无界。因而一位方法的失败推广到任意固定有限深度；有效深度必须随 \(\log n/\log p\) 增长。
- [第二轮新增] 严格证明局部计数命题 (L) 足以闭合小素数核心及官网全部量词；其中常数项1正好避免被固定素数族 \(n=(p^k-1)/2\) 反驳。
- [第二轮复核加固] 两个算法结构独立的全扫描在 \(n\le2\times10^7\) 得到完全相同的核心纪录文件；两个独立枚举在 \(n\le10^{12}\) 的3、5、7零进位搜索中也完全一致。所有候选值另以 Legendre 阶乘估值重算通过。

#### 证伪与边界检查

- 固定深度构造中特意取 \(m=\max(D,3)\)：既保证 \(p^D\mid n\)，也逐项保证核心范围要求 \(p^3\le n\)；没有遗漏 D=1、2 的边界。
- 最高位端点使用 \(2n+1\le p^{k+1}\)，而不是忽略整数端点的 \(2n<p^{k+1}\)；显式族达到等号。
- 局部命题 (L) 保留了 O(1) 个素数的常数项；否则固定 p 显式族会立即反驳 \(O(P/\log n)\) 形式。
- 直接数字程序与 p-adic 递推程序不共享判定核心；两者对2×10^7范围的 CSV SHA-256 完全相同。
- 位掩码和 DFS 两种 ternary 枚举对10^12范围的候选数16、最大值及纪录 CSV 均一致。
- n=3160 的特殊性早在 EGRS75 第83页出现；本轮不主张该数值或其3、5、7、11性质具有文献优先权。
- 所有计算均为有限证伪搜索；没有用“未发现更大值”推断一致有界。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/core_scan.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/core_scan.cpp)：p-adic 递推核心扫描；与完全独立的 core_scan_direct.cpp 逐点 base-p 数字扫描交叉检查。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377 && g++ -O3 -std=c++17 core_scan.cpp -o core_scan && g++ -O3 -std=c++17 core_scan_direct.cpp -o core_scan_direct && ./core_scan 20000000 > core_records_2e7.csv && ./core_scan_direct 20000000 > core_records_direct_2e7.csv && diff -u core_records_2e7.csv core_records_direct_2e7.csv；结果：diff 无输出；两文件 SHA-256 均为 ed690a7fddbe7b21d67fbb4faa3b2f5cdb039003c0c63ddb09246067c429dd4d。最大核心纪录为 g(3160)=0.76709956709956706。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/triple_search.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/triple_search.cpp)：ternary 位掩码搜索；与独立递归实现 triple_search_dfs.cpp 交叉检查3、5、7同时零进位。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377 && g++ -O3 -std=c++17 triple_search.cpp -o triple_search && g++ -O3 -std=c++17 triple_search_dfs.cpp -o triple_search_dfs && ./triple_search 1000000000000 > triple_records_1e12.csv && ./triple_search_dfs 1000000000000 > triple_records_dfs_1e12.csv && diff -u triple_records_1e12.csv triple_records_dfs_1e12.csv；结果：两实现均报告16个候选、最大核心值0.76709956709956706于 n=3160；纪录文件 SHA-256 均为0ba8a0c00bcf08424bb0db98da77973c0fe623e0edf8aacdf105ce7a31e8149f。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/verify_candidates.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/verify_candidates.py)：用 Legendre 公式 \(v_p((2n)!)-2v_p(n!)\) 独立重算所有输出纪录的核心素数和。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377 && python3 verify_candidates.py core_records_2e7.csv triple_records_1e12.csv > verification_2e7_1e12.txt；结果：verified=5 status=OK；输出 SHA-256 为 b7386fbaea4ee2de68d7b63d1c5b504181330f5196e85df42a934afbb5d2f2e3。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/round2_research_note.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377/round2_research_note.md)：包含最高位区间、固定深度反例、局部充分命题及计算说明的自洽草稿。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/377 && sha256sum round2_research_note.md；结果：SHA-256：b100bde818ae6157d6798529b095b29cc8b85ebc8652f03ac9be3888bfc9c2f2。

#### 当前障碍

尚不能证明局部点态计数 (L)，困难集中在 \(P=n^{o(1)}\) 的小素数块。固定有限数字深度必然无界；Sander 的一位指数和、Bloom–Croot 的 o(log n) 坏数字结论也都无法把“少量进位”提升为“零进位”。需要真正利用约 \(\log n/\log P\) 个数字块的联合约束，并保持同一个 n 下不同素数之间的相关性。

#### 下一精确定理

证明存在绝对常数 \(K\)，使对所有 \(n\ge8\) 和所有实数 \(2\le P\le n^{1/3}\)，都有 \[\#\left\{p\text{ prime}:P<p\le\min(2P,n^{1/3}),\ p\nmid\binom{2n}{n}\right\}\le K\left(1+\frac{P}{\log n}\right).\]这是比第一轮核心引理更局部、可逐块验证的充分定理；它兼容所有已知固定素数族，并通过 dyadic 求和直接闭合原题。

#### 第二轮证明记录

【承接的第一轮事实】由 Legendre–Kummer，\[v_p\binom{2n}{n}=\sum_{a\ge1}\left(\left\lfloor\frac{2n}{p^a}\right\rfloor-2\left\lfloor\frac n{p^a}\right\rfloor\right),\]各项为0或1。对奇素数，\(p\nmid\binom{2n}{n}\) 当且仅当对每个 \(a\ge1\)，\(n\bmod p^a\le(p^a-1)/2\)，等价于全部 base-p 数字不超过 \((p-1)/2\)。第一轮已证明任意固定幂阈值以上的素数倒数和为常数，因此问题可归约到 \(p^3\le n\) 的核心；也已用 \(n=(p^k-1)/2\) 否定逐位数层取 \(\sup_n\) 的可求和方案。

【第二轮新增推导】首先把最高位也保留下来。若 \(k=\lfloor\log_p n\rfloor\)，无进位时 \[p^k\le n\le\frac{p-1}{2}\sum_{i=0}^kp^i=\frac{p^{k+1}-1}{2},\]故幸存素数只能位于 \((2n+1)^{1/(k+1)}\le p\le n^{1/k}\)。不过这个单条件仍没有控制多层总和。

接着直接攻击“多检查若干低位即可”的想法。对固定 \(D\) 定义 \(T_D(n,p)\) 为前 D 个余数条件全部成立。给定任意大的 M，选有限奇素数集 S 使 \(\sum_{p\in S}1/p>M\)，令 \(P=\prod_{p\in S}p\)、\(n=P^{\max(D,3)}\)。于是每个 \(p\in S\) 都有 \(n\bmod p^a=0\;(a\le D)\) 且 \(p^3\le n\)。所以 \[\sup_n\sum_{p^3\le n,\,T_D(n,p)}\frac1p=\infty.\]这严格说明：任何固定深度的低位筛都不可能证明核心引理；数字深度必须随 \(\log n/\log p\) 增长。

幸存的精确局部目标是 (L)。若每个 dyadic 块内零进位素数数目为 \(O(1+P/\log n)\)，则该块倒数和为 \(O(1/P+1/\log n)\)。沿 \(P=2^j\) 求和时，\(\sum 1/P=O(1)\)，而 \(O(\log n)\) 个块各贡献 \(O(1/\log n)\)，因此核心和一致有界。这一形式中的常数项不可删除：固定素数显式族会贡献约 \(1/P\)，但不会击穿含常数项的计数界。

【仍未闭合的缺口】目前没有得到 (L) 在 \(P=n^{o(1)}\) 范围的证明。固定 D 的条件已被上述乘积构造完全击穿；允许 \(o(\log n)\) 个坏数字的近年定理仍允许正 p-adic 重数，不能用于本题。计算在 \(2\times10^7\) 全扫描和 \(10^{12}\) 的3、5、7稀疏搜索中均未发现核心值超过0.7670995671，但这不关闭任何无限量词。

【来源成熟度与优先权】EGRS75 与 Sander94 是已发表论文；Croot–Mousavi–Schmidt 已发表于 Mathematika，其 arXiv 版本用于核对定理文字；Bloom–Croot 2025目前是一手 arXiv 预印本，不能视为已同行评议。n=3160 的异常早见于 EGRS75，本轮不主张优先权。固定深度无界命题是本轮从基本构造独立推出的研究障碍说明，未检索到其作为独立命题的明确文献表述，因此也不作新颖性声明。

#### 本轮核查来源

- [Erdős–Graham–Ruzsa–Straus, On the Prime Factors of the Central Binomial Coefficient](https://doi.org/10.1090/S0025-5718-1975-0369288-3)；一手来源：true；核验：第84页 Fact 给出全 base-p 数字判据；Theorem 1 证明任意两个素数可同时零进位无穷多次；Theorems 2、3给出一阶、二阶平均。第83页已经记录 n=3160 的最小奇素因子为13；第90页明确指出把对固定 p 的平均结果反转成固定 n、跨 p 的控制尚未做到。
- [J. W. Sander, On a Sum over Primes](https://hrj.episciences.org/129/pdf)；一手来源：true；核验：主定理只处理一位余数条件及权 \((\log p)/p\)。第4节指出 Jutila 指数和在 \(p\le \exp((\log n)^{2/3})\) 范围不能优于平凡界，而该范围的 \(1/p\) 总和已经过大。
- [Bloom–Croot, Integers with small digits in multiple bases](https://arxiv.org/abs/2509.02835)；一手来源：true；核验：2025年预印本 Theorem 1 在显式大基底条件下，仅保证每个基底至多 \(\epsilon\log n\) 个坏数字；Corollary 1 相应只给指定素数部分的低重数，而非零重数。正文强调全数字小的 Conjecture 1 仍未证明。
- [Croot–Mousavi–Schmidt, On a conjecture of Graham on the p-divisibility of central binomial coefficients](https://arxiv.org/abs/2201.11274)；一手来源：true；核验：Theorem 1 处理固定个充分大素数的低进位比例，不能推出任一指定素数完全不整除。
- [FormalConjectures Erdős Problem 377](https://github.com/google-deepmind/formal-conjectures/blob/9e126a6e1f7d108ced5904c43cac46b1c39b39cb/FormalConjectures/ErdosProblems/377.lean)；一手来源：true；核验：形式题面是 \(\exists C>0,\forall n\)，且求和只取 \(p\le n\)；主命题仍标记 research open。定向一手文献检索未找到闭合该精确量词的论文或机器证明。

### #539

- 第一轮障碍：当前悬挂把两个普通差独立组合，精确产生 \((2K-1)r^2\) 个普通差，使 \(r/m\) 每层近似平方；同一计数模板因此不可避免地产生 \(\exp(\Theta(2^s))\) 的深度常数。尚无能控制该普通差集爆炸、同时保留 \(Km^2\) 个点的新提升操作。
- 第一轮下一定理：一个清晰且足以推进的下一定理是：存在绝对常数 C，使对所有深度 s 和 n，\[h(n)\le \exp(Cs^2)n^{\alpha_s},\qquad \alpha_s=\frac{2^{s+1}}{2^{s+2}-1}.\]这把当前固定深度常数 \(\exp(O(2^s))\) 改为 \(\exp(O(s^2))\)；取 \(s\asymp\log_2\log n\) 将立即推出 \(h(n)\le\sqrt n\exp(O((\log\log n)^2))\)。本次障碍分析表明，证明它必须利用跨层正部差的额外重合或引入不同于独立笛卡尔平方的构造。
- 第二轮用时：1249.5 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：检验跨层重合或可变层宽 K_i∼k_iW 能否把原悬挂族的固定深度常数从 exp(O(2^s)) 降到 exp(O(s²))；若不能，确定替代提升必须满足的最窄结构条件。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核 ProofCouncil 基带 B_W 的规模、正部差与普通差三个精确计数，separated suspension 的正部差下界和普通差等式，以及从任意渐近线性层宽 K_i(W)/W→k_i∈(0,∞) 得到的归一化递推和 N_s≥2^((3·2^(s−1)−1)/2)。
- 复核方式：从定义重新证明三个基带集合刻画和悬挂的逐层差值结构；逐项审计 liminf、归一化幂次、t 参数消元和全局最小化；重跑仓库 Python/C++ 两套资产并逐字比较输出；另把 Python 有限枚举扩展到 W=3。
- 证据边界：有限枚举只核对小参数和实现一致性；PASS 的依据是集合分支的不交性、普通差的精确参数化和 liminf 递推。对外表述必须保留‘给定基带、完整 F×F、渐近线性宽度、全集合’四项限定，不能简写成所有 separated suspension 均被排除。

#### 第二轮实际尝试

- **精确化二维基带首项**（advanced）：不沿用第一轮的粗上界，逐一刻画基带的正部差和普通差。；对 L=W² 和 B_W={(i,j)∈[0,L]²:L≤i+j≤L+W−1}，正部差恰为两条轴段与三角形 {(u,v):u,v≥1,u+v≤W−1} 的不交并。因此 |D(B_W)|=(5W²−3W+4)/2。普通差恰为 {(u,v):|u|,|v|≤L, |u+v|≤W−1}，故 |B_W−B_W|=4W³−3W²+3W−1，而 |B_W|=W³−W²/2+3W/2。
- **寻找跨层重合反例**（refuted）：直接枚举一维最小集合及各层 gap，检查论文的正部差上界是否可能被误当作等式。；取 F={0,1}、K=3、最小合法位移 M=2。实际 |D(S_K(F))|=14，而 q²+2(K−1)r=16：负 gap 1、2 之间发生重合，负 gap 还与同层值重合。因此正部差公式只有上界；这击穿了任何依赖其“精确等号”的论证。
- **提取不受重合影响的正部差下界**（advanced）：只使用同层值和正层差，利用首坐标区分各分支。；同层正部差完整包含 {0}×D(F)×D(F)。正 gap a=1,…,K−1 的首坐标等于 a，第一个块恰遍历 aM·1+(F−F)，第二块为零；这些集合彼此及与同层不交。因此严格有 |D(S_K(F))|≥q²+(K−1)r。负 gap 是否重合完全不影响此式。
- **任意线性层宽的实际构造障碍**（advanced）：令 K_i(W)/W→k_i>0，同时追踪规模、普通差、正部差的首项并对 k_i 作全局优化。；写 m_i∼A_iW^{a_i}、r_i∼R_iW^{a_i}、B_i=liminf q_i/W^{b_i}，并置 V_i=R_i/A_i、N_i=B_i/A_i^{α_i}。由普通差精确式得 V_{i+1}=2V_i²；基带 V_0=4，故 V_i=2^{3·2^i−1}。由 q_{i+1}≥q_i²+(K_i−1)r_i，令 k_i=tA_i^{1/a_i}、β=α_{i+1}，得到 N_{i+1}≥(N_i²+tV_i)t^{−β}。其 t>0 全局最小值为 (1−β)^{β−1}β^{−β}N_i^{2(1−β)}V_i^β。因 N_0=5/2、β>1/2，遂有 N_s≥V_{s−1}^{1/2}=2^{(3·2^{s−1}−1)/2}。
- **比较 exp(O(2^s)) 与 exp(O(s²)) 的精确量词**（refuted）：固定深度 s 后令 W→∞，再让 s 增长。；上述 N_s 是 |D(F_s(W))|/|F_s(W)|^{α_s} 的下极限下界，且对所有逐层 k_i>0 的选择成立。给定任意绝对常数 C，充分大 s 时 2^{(3·2^{s−1}−1)/2}>exp(Cs²)，故该完整 F×F 悬挂族不能满足统一 exp(Cs²) 常数。这不反驳其他构造对 h(n) 的一般存在性上界。
- **尝试相关/对角 payload**（blocked）：以 E={(x,x):x∈F} 代替完整 F×F，检验能否避免普通差平方。；对角 payload 确实只有 |D(E)|=q、|E−E|=r，但 |E|=m 而非 m²；悬挂后规模仅 Km。取 K∼W 时跨层项已有 W·r 的 W 次数 a+1，与规模次数 a+1 相同，不能产生 α_{s+1}<1 的改进。有限个置换图的并同样损失一个 m 因子。

#### 第二轮新增严格进展

- [第二轮新增] 精确求得基带三项：|B_W|=W³−W²/2+3W/2，|D(B_W)|=(5W²−3W+4)/2，|B_W−B_W|=4W³−3W²+3W−1；第一轮只有相应粗界。
- [第二轮新增] 对 separated suspension 证明了不受负 gap 重合影响的反向不等式 |D(S_K(F))|≥q²+(K−1)r；同时给出 F={0,1}, K=3, M=2 的可复现反例，证明论文的 q²+2(K−1)r 上界一般不是等式。
- [第二轮新增] 对所有 K_i(W)/W→k_i∈(0,∞) 的完整笛卡尔悬挂迭代，证明归一化常数 N_s≥2^{(3·2^{s−1}−1)/2}（s≥1）。因此即使充分利用跨 gap 重合并任意优化线性层宽，该构造族仍必有 exp(Ω(2^s)) 损失。
- [第二轮复核加固] 上一轮仅从上界递推判断“调 K 无效”；本轮得到的是实际所构造集合的下界，因而严格排除了同一完整 F×F payload 族产生 exp(O(s²)) 常数，而不只是排除某种记账方法。

#### 证伪与边界检查

- W=1 时基带为 {(0,1),(1,0)}，精确公式给 (m,q,r)=(2,3,3)，避免把渐近首项误用于小参数。
- K=1 时悬挂只有单层，程序得到 q'=q²、r'=r²；变量宽度定理明确假设 K_i/W→k_i>0，因此没有把 K=1 混入渐近优化。
- 严格分离只要求 M 大于坐标直径；负 gap 的集合可以互相重合。本轮下界只使用正 gap，其首坐标记录 gap，故无需额外假设 M>2·diam(F)。
- 检查了同层集合与正 gap 的不交性：前者首坐标为 0，后者首坐标为正整数 a；q² 项不会因任何跨层碰撞消失。
- 检查整数取整：K_i(W)=⌊k_iW⌋ 或 ⌈k_iW⌉ 均有相同首项，归一化推导只使用 K_i/W→k_i。
- 固定维文献下界的维数分别为 3、4；本路线维数 d_s=3·2^s−1，故没有把 Theorems 1.2–1.3 错用于变维极限。
- 官网原题量词没有被关闭：本轮只反驳一个构造族，未证明一般 exp(Cs²)n^{α_s} 上界为假，更未证明 h(n)=Θ(√n)。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/verify_suspension_obstruction.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/verify_suspension_obstruction.py)：Python 实现两套计数：直接枚举全部有序点对，以及按同层/正 gap/负 gap 的符号公式构造差集；还核对基带精确公式和最小重合反例。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539 && python3 verify_suspension_obstruction.py --max-w 2 --max-k 3 > suspension_obstruction_results.json；结果：全部断言通过；脚本 SHA-256 6116a9e3b6f63dae5290b0a3e3bf1c208267ded2c942394d58519eeef5404050。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/suspension_obstruction_results.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/suspension_obstruction_results.json)：记录 W=1,2、K=1,2,3 的两实现交叉结果，以及深度 0,…,8 的指数和归一化障碍公式。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539 && sha256sum suspension_obstruction_results.json；结果：SHA-256 306cbf0390177ab0901929f1c4008f644106987e58d3c0363def4bd2c9f62d5c；例如 W=2,K=2 得基带 (m,q,r)=(9,9,25)，悬挂后 (162,131,1875)。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/crosscheck_suspension.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/crosscheck_suspension.cpp)：独立 C++ 直接有序点对枚举，没有调用 Python 的符号公式。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539 && g++ -O2 -std=c++17 -Wall -Wextra -pedantic crosscheck_suspension.cpp -o crosscheck_suspension && ./crosscheck_suspension > crosscheck_suspension.txt；结果：与 Python 的六组 (m,q,r) 逐项一致，并独立得到重合反例 actual=14、naive=16；源码 SHA-256 666d2ab086709b557e924bbd4407aed78c1b442e4cabdbd51173ba9fa9e2ddd1。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/crosscheck_suspension.txt](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539/crosscheck_suspension.txt)：C++ 独立枚举输出。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/539 && sha256sum crosscheck_suspension.txt；结果：SHA-256 1c40dba0d3115a67940e45ce55c3ad3c251648fe7f9255fb258ffaf7584041a1。

#### 当前障碍

完整 F×F 作为每层 payload 已被严格排除：其普通差比率满足 V↦2V²，而同层正部差保留 D(F)²。要达到 exp(O(s²))，必须找到非笛卡尔 payload E⊂F×F，同时保留接近 m² 个点、显著压缩同层 D(E)，并使 |E−E|/|E| 不发生平方；目前没有这样的 E，也没有一般组合引理保证其存在。

#### 下一精确定理

最窄的建设性下一定理是“非笛卡尔重置引理”：对第 i 层特殊集合 G_i(W)，存在 E_i(W)⊂G_i(W)×G_i(W)，使 |E_i|≥exp(−Ci)W^{2a_i}、|D(E_i)|≤exp(Ci)W^{2b_i}、|E_i−E_i|≤exp(Ci)W^{2a_i}，且两个坐标投影的普通差均≤exp(Ci)W^{a_i}。再取 K=W 悬挂并逐层相乘损失，将给出 |G_s|≥exp(−O(s²))W^{a_s}、|D(G_s)|≤exp(O(s²))W^{b_s}，从而推出上一轮目标。当前对角图只满足差集条件而不满足所需规模。

#### 第二轮证明记录

承接的第一轮事实

令 x^+=(max(x_j,0))_j、D(F)=(F−F)^+。素因子指数桥把原题精确化为变维整数向量问题；ProofCouncil 的构造从二维基带开始，反复使用
S_K(F)={(j,x+jM1,y−jM1):0≤j<K, x,y∈F}。
第一轮已复核其上界
|S_K(F)|=Km²， |D(S_K(F))|≤q²+2(K−1)r， |S_K(F)−S_K(F)|=(2K−1)r²，
以及 K=W 时 a_s=2^{s+2}−1、b_s=2^{s+1}、α_s=b_s/a_s。已知全局界仍只是
(1+√(8n−7))/2≤h(n)≤√n·exp(O(√log n))。

第二轮新增推导

先精确计算基带。设 L=W²，
B_W={(i,j)∈[0,L]²:L≤i+j≤L+W−1}。
规模为
|B_W|=W³−W²/2+3W/2。
若正部差两个坐标都正，则坐标和至多 W−1；反之落在轴上。反向构造表明所有这些值都出现，因此
D(B_W)={(u,0):0≤u≤L}∪{(0,v):0≤v≤L}∪{(u,v):u,v≥1,u+v≤W−1},
从而
|D(B_W)|=(5W²−3W+4)/2。
同样
B_W−B_W={(u,v):|u|,|v|≤L, |u+v|≤W−1}，
逐对角线求和得到
|B_W−B_W|=(2W−1)(2W²+1)−W(W−1)=4W³−3W²+3W−1。
所以基带首项比率 A_0=1、B_0=5/2、V_0=R_0/A_0=4。

其次提取悬挂的反向不等式。固定同层 j 后，正部差恰遍历
{0}×D(F)×D(F)，
故已有 q² 个值。固定正 gap a=j−j'>0 后，严格分离保证输出为
(a,aM1+u,0)， u∈F−F。
首坐标区分不同 a，也区分同层，故
|D(S_K(F))|≥q²+(K−1)r.  (1)
这不使用负 gap。事实上负 gap 确会重合：F={0,1},K=3,M=2 时实际正部差数为 14，而论文上界表达式给 16。

现在允许每层 K_i(W)/W→k_i>0。写
m_i∼A_iW^{a_i},  r_i∼R_iW^{a_i},
B_i=liminf_{W→∞}|D(F_i(W))|/W^{b_i},
V_i=R_i/A_i,  N_i=B_i/A_i^{α_i}。
普通差精确式给
A_{i+1}=k_iA_i²， R_{i+1}=2k_iR_i²，
所以
V_{i+1}=2V_i²， V_i=2^{3·2^i−1}.  (2)
由 (1)，
B_{i+1}≥B_i²+k_iR_i。
因 2b_i=a_i+1，令 k_i=tA_i^{1/a_i} 及 β=α_{i+1}=(a_i+1)/(2a_i+1)，可消去 A_i：
N_{i+1}≥(N_i²+tV_i)t^{−β}.  (3)
右边在
 t*=βN_i²/((1−β)V_i)
取得全局最小值
(1−β)^{β−1}β^{−β}N_i^{2(1−β)}V_i^β。
前置常数大于 1，且 N_0=5/2>1、β>1/2；因此对 s≥1，
N_s≥V_{s−1}^{1/2}=2^{(3·2^{s−1}−1)/2}=exp(Ω(2^s)).  (4)
给定任何绝对 C，充分大 s 时 (4) 大于 exp(Cs²)。所以不论逐层怎样选择线性宽度 k_i，也不论负 gap 重合有多强，完整笛卡尔悬挂族都不能证明统一的 exp(Cs²)n^{α_s} 上界。这是对上一轮“也许利用被忽略重合即可改善同一族”的严格反驳；它不是对该上界一般存在性的反例。

仍未闭合的缺口

要绕过 (4)，每层不能保留完整的同层 F×F，因为这强制出现 D(F)²；但只取对角图 E={(x,x)} 又把 payload 从 m² 降到 m，失去指数改进。尚需构造一个介于二者之间的 E⊂F×F：规模接近 m²，同时 D(E) 和 E−E 都远小于完整乘积的相应差集。当前没有证明这种 E 对特殊层集合存在，也没有反例证明它不可能存在。因此没有得到比 √n·exp(O(√log n)) 更强的 h(n) 上界。

来源成熟度与优先权

Granville–Roesler 与 Holzman–Lev–Pinchasi 是已发表同行评审文献；后者的精确固定维定理编号已由作者 PDF 核实。2026 ProofCouncil 材料是 arXiv 预印本，其 Appendix A.1 是清理后的模型输出，论文称经人工专家核验；显式次指数常数尚未 Lean 化。Oxford 2012 摘要确认 Bollobás–Leader 有相关未发表合作，但没有给出所得指数或可检查证明。此次检索未在这些一手来源中找到本轮归一化下界 (4) 的既有陈述；由于检索范围有限且 Bollobás–Leader 工作未公开，不主张文献优先权。

#### 本轮核查来源

- [Erdős Problem #539](https://www.erdosproblems.com/539)；一手来源：true；核验：页面截至 2026-06-15 仍标 open，记录 h(n)≤n^{1/2}exp(O(√log n)) 及 h(n)=n^{1/2+o(1)}，没有记录 Θ(√n) 结论。
- [ProofCouncil: An LLM Agent for Solving Open Mathematical Problems, Appendix A](https://arxiv.org/abs/2607.09474)；一手来源：true；核验：Theorem A.1 给出显式次指数上界；Lemma A.6 的每一层是完整 F×F，普通差数为 (2K−1)r²；Proposition A.7 取 K=W 迭代。附录 A.2 明说 Lean 只覆盖固定深度界和指数极限，不覆盖显式次指数常数优化。
- [ProofCouncil Lean project](https://github.com/eth-sri/proof-council/tree/main/lean)；一手来源：true；核验：README 列出 Base、Suspension、Iteration、Main 等模块及 Lean 4.29.1/mathlib 4.29.1；本轮新增的双指数归一化下界不在其声明的形式化范围内。
- [Projecting Difference Sets on the Positive Orthant](https://holzman.technion.ac.il/files/2012/09/project.pdf)；一手来源：true；核验：作者 PDF 的 Theorems 1.2、1.3 分别证明三维 |D(A)|≥|A|^{3/5}/6 和四维 |D(A)|≥c|A|^{6/11}/(log|A|)^{2/11}；这些是固定维下界，不能直接约束本路线随 s 增长的维数。
- [The Set of Differences of a Given Set](https://doi.org/10.2307/2589556)；一手来源：true；核验：核实 Granville–Roesler 论文发表于 American Mathematical Monthly 106(4), 338–344 (1999)；本轮没有借其名义附加未核实的新定理。
- [Positive projections, Oxford seminar abstract](https://www.maths.ox.ac.uk/node/9547)；一手来源：true；核验：2012 年 Imre Leader 报告明确把问题表述为正投影差集并注明与 Béla Bollobás 合作，但摘要没有给出所得指数或书面证明。

### #635

- 第一轮障碍：Elliott/Gram 二阶矩只产生 Lδ²≲1，其中 L≈log log N，因此无法逼近构造所示的 Θ(log N) 次主项。精确极值需要使用不同结构，尤其要同时利用不同 d 的路径约束之间的强依赖。
- 第一轮下一定理：最清晰的下一定理是 t=2 的精确候选：F_2(N)=⌈N/2⌉+#{k≥1:k为奇数且2^k≤N}。较稳健的中间目标是先证明 F_2(N)≤N/2+O(log N)。计算已支持精确式至 N=500（并检查若干 N≤2000），但尚无覆盖全部 N 的注入、匹配或对偶证书。
- 第二轮用时：2728.5 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：先证伪普通匹配/固定注入路线，再寻找能够闭合 t=2 精确候选的最窄结构命题；同时用独立集 MILP 与可直接核验的 clique 打包证书交叉检查新范围。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核 t=2 冲突边的 gcd 等价、N=20 的普通匹配模板反例、候选集合 B_N 与独立左集 Hall 条件的逐 N 充要关系，以及显式 clique 证书和 B_N 下界共同给出的 F_2(3000)=1506、F_2(5000)=2506。
- 复核方式：从官网 t=2 条件重建冲突图；不用优化器重算 N=20 的割邻域、孤立点及七边匹配；双向证明独立左集 Hall 等价；重跑仓库 clique 验证器并逐字比较输出；另以 gcd 为边判据逐行、逐 clique、逐顶点流式核验两条大证书，同时直接构造并验证 B_N。
- 证据边界：clique 文件虽由优化搜索找到，但一旦给出后，上界证明只依赖有限整数证书的逐边检查；生成器或 MILP 的正确性不再是定理前提。两个有限等式不可外推。私有邻点性质目前既未发表也未证明，必须继续按猜想/下一步引理表述。

#### 第二轮实际尝试

- **普通 Hall 匹配路线的证伪**（refuted）：令 B_N 为奇数与奇指数二次幂之并，尝试把 C_N=[N]\B_N 饱和匹配进 B_N。；在 N=20，S={12,16,18,20}⊂C_N 的 B_N-邻域恰为 {8,9,15}，故 |Γ(S)|=3<4。更强地，完整冲突图由一个15点奇分量和五个孤立点组成，故任何匹配至多7条；显式存在7条匹配，而候选上界需要8条不交边。
- **边与三角形联合打包**（advanced）：枚举冲突图的全部边和三角形，寻找互不相交的 cliques，并以 Σ(|C|−1) 为节省量。；独立集在每个 clique 中至多取一点，故节省量 s 给出 |A|≤N−s。N=3000 的证书含1110条边和192个三角形，s=1494；N=5000 含1874条边和310个三角形，s=2494，分别精确给出上界1506和2506。
- **自适应 Hall 缩减**（advanced）：只要求对实际可能出现的独立子集 S⊆C_N 验证 Hall 条件。；证明了 B_N 最大当且仅当每个在冲突图中独立的 S⊆C_N 满足 |Γ_{B_N}(S)|≥|S|。普通 Hall 的 N=20 见证并不独立，因而不反驳这个精确缩减。
- **私有邻点强化命题**（inconclusive）：搜索独立 S⊆C_N，使每个 B_N 邻点在 S 中的度均为0或至少2。；若每个非空独立 S 都有度恰为1的 B_N 邻点，则可删除该邻点对应的唯一顶点并归纳构造 Hall 匹配。直接线性编码对全部 N≤500 未找到反例，另抽查 N=750,1000,1500 亦无反例，但没有一般证明。
- **继续寻找 t=2 数值反例**（advanced）：用独立集二元 MILP 求精确最优值，并以完全不同的 clique 打包证书给上界。；新增检查 N=3000,5000；MILP 最优值分别为1506、2506，与候选相等，并由独立证书验证器重算上界。尝试更大的批次未在合理时间内完成，未作为结果报告。

#### 第二轮新增严格进展

- [第二轮新增] 对 t=2，冲突边 {x,y}（x<y）等价于 gcd(x,y)=y−x≥2；亦即约分后的 y/x 是两个连续正整数之比。
- [第二轮新增] 严格反驳了普通匹配证明模板：N=20 时 S={12,16,18,20} 的候选割邻域只有 {8,9,15}；完整冲突图最大匹配也只有7条。
- [第二轮新增] 证明了 t=2 精确候选与独立左集 Hall 条件逐 N 等价：B_N 最大，当且仅当所有独立 S⊆C_N 都满足 |Γ_{B_N}(S)|≥|S|。
- [第二轮新增] 给出并独立验证了有限精确值 F_2(3000)=1506、F_2(5000)=2506。上界来自显式不交边/三角形证书，下界来自 B_N，因而不依赖 MILP 的最优性声明。
- [第二轮复核加固] 独立集 MILP 与 clique 打包两种不同形式在 N=3000,5000 给出一致答案；整数证书验证器只使用定义 d=y−x≥2 且 d|y，逐 clique 检查。

#### 证伪与边界检查

- 普通 Hall 失败的邻域已逐边核算：12 的候选邻点为8,9,15；16仅有8；18有9,15；20仅有15。
- 完整图匹配上界不依赖优化器：N=20 有六个奇连通分量，所以每个匹配至少留下六点，匹配数至多7；脚本同时给出7条显式匹配。
- 固定前驱映射 φ(2^r u)=(2^r−1)u 也不可用：独立对 {24,42} 均映到21，而42−24=18不整除42。
- 自适应 Hall 的穷举实现检查了小规模独立子集；MILP 使用另一种变量编码，在抽查至5000的实例中最大 Hall 亏损为0。这仍只是有限证据。
- “私有邻点”搜索最终采用直接约束 x_u≤Σ_{w∈N(v)\{u}}x_w，并对返回候选另行验算；全部 N≤500 无反例。
- 未找到可公开检查、精确对应本题的约1980年 Erdős—Ruzsa 信件；也未找到已经处理 t=2 精确式或独立集问题的一手论文，故不主张文献优先权。
- Tao 评论中的“类似 O(1/log log N)”是非正式量级描述；可检查的 Exercise 8 是平方误差界。本轮没有把该评论升级成未经推导的更强定量结论。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_matching_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_matching_check.py)：构造候选割并分别用自写 Hopcroft–Karp 与 NetworkX 检查普通 Hall 匹配。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635 && python3 t2_matching_check.py 20 --method both --emit-matching；结果：两种实现均给最大匹配7<8；手检 Hall 见证为 S={12,16,18,20}。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_adaptive_hall.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_adaptive_hall.py)：穷举或 MILP 搜索独立左集的 Hall 亏损。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635 && python3 t2_adaptive_hall.py 20 50 100 200 500 1000 2000 5000 --method milp；结果：所列实例的最大亏损均为0；N=20 的穷举独立子集实现亦交叉通过。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/clique_certificates_3000_5000.jsonl](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/clique_certificates_3000_5000.jsonl)：N=3000、5000 的显式互不相交边/三角形上界证书。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635 && python3 verify_clique_certificate.py clique_certificates_3000_5000.jsonl；结果：验证得到上界1506、2506，与显式下界完全相等。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_exact_milp_round2.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_exact_milp_round2.py)：独立生成全部冲突边并求最大独立集的第二套精确优化实现。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635 && python3 t2_exact_milp_round2.py 500 1000 2000 3000 5000；结果：零 MIP gap；最优值254,505,1005,1506,2506，与构造及证书一致。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_private_neighbor.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635/t2_private_neighbor.py)：搜索违反“每个非空独立左集都有私有候选邻点”的集合。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/635 && python3 t2_private_neighbor.py $(seq 1 500)；结果：全部500个实例均不可行，即未找到私有邻点命题的有限反例。

#### 当前障碍

尚不能证明：对任意 N 和任意非空、冲突独立的 S⊆C_N，存在 b∈B_N 满足 |N(b)∩S|=1。普通 Hall 不成立，固定映射也会碰撞；目前缺少利用“碰撞顶点之间不得冲突”导出私有邻点的数论下降论证。没有这一步，就不能推出全 N 的 t=2 精确式，也未得到 N/2+O(log N)。

#### 下一精确定理

最清晰的下一定理是“私有邻点定理”：令 B_N={n≤N:n为奇数或 n=2^{2j+1}}，C_N=[N]\B_N。若 S⊆C_N 在 gcd(x,y)=|x−y|≥2 的图中独立且 S非空，则存在 b∈B_N，其在 S 中恰有一个邻点。该定理通过删除唯一邻点归纳推出独立左集 Hall 条件，继而证明 F_2(N)=⌈N/2⌉+#{j≥0:2^{2j+1}≤N}。第一优先仍应先在更大 N 上证伪该强化命题，因为它严格强于所需 Hall 条件。

#### 第二轮证明记录

承接的第一轮事实：第一轮已经由 Elliott/Gram 二阶矩得到固定 t 的 |A|≤N/2+O_t(N/√log log N)，并核验了下界集合 B_N（全部奇数加奇指数二次幂）。本轮没有把这些重新计作进展，也没有得到一般 t 的更强误差。Tao 的原评论同样强调 O(log N/N) 级精度超出 Elliott 路线。

第二轮新增推导：对 x<y，若 y−x|y，则 y−x 也整除 x；写 x=k(y−x)、y=(k+1)(y−x)，因 gcd(k,k+1)=1，得到 gcd(x,y)=y−x。反向显然。因此 t=2 冲突图可写为

{x,y}∈E ⇔ gcd(x,y)=|x−y|≥2.  (1)

令 B=B_N 为候选独立集、C=[N]\B。普通的 C→B 匹配并不存在：N=20 时 S={12,16,18,20} 有 Γ_B(S)={8,9,15}。这严格否定第一轮建议的直接匹配/注入模板。完整图的普通匹配也不足：其一个15点分量与五个孤立点都是奇分量，故最多匹配7条。

幸存的精确缩减必须利用 A∩C 自身独立。证明如下。若每个独立 S⊆C 都满足 |Γ_B(S)|≥|S|，则对任意独立 A，取 S=A∩C。由于 Γ_B(S)⊆B\A，

|A∩C|≤|Γ_B(S)|≤|B\A|,

故 |A|≤|B|。反之，若 B 已知最大，则对任意独立 S⊆C，集合

(B\Γ_B(S))∪S

仍独立，最大性给 |B|−|Γ_B(S)|+|S|≤|B|，即 Hall 条件。因此这不是启发式，而是与 t=2 精确公式完全等价的有限图命题。

一个更窄、可归纳的充分条件是私有邻点性质：每个非空独立 S⊆C 都有 b∈B，使 |N(b)∩S|=1。匹配该唯一邻点并对 S 删除一元素归纳，即得 Hall 条件。计算未找到反例，但本轮没有证明该性质。

有限证书方面，若 P 是互不相交的边与三角形族，则任一独立集满足

|A|≤N−Σ_{Q∈P}(|Q|−1).  (2)

N=3000 的证书节省1494，N=5000 的证书节省2494；故分别有 F_2≤1506、F_2≤2506。此时奇指数幂计数均为6，B 的大小分别为1500+6和2500+6，于是等号成立。这些只是两个新增有限定理，不可外推到所有 N。

仍未闭合的缺口：没有全 N 的私有邻点证明或统一 clique 打包构造，故 t=2 精确式和 N/2+O(log N) 仍未解决。固定映射也不能填补缺口，例如 φ(2^r u)=(2^r−1)u 在独立对 {24,42} 上碰撞于21。

来源成熟度与潜在优先权：可核验的一手来源只支持 Elliott 平方采样不等式以及 Tao 对方法局限的原评论；没有找到处理本题独立集或 t=2 精确式的一手论文，也无法取得原始 Erdős—Ruzsa 信件。因此本轮的 Hall 缩减和私有邻点目标不作原创性或文献优先权声明，必须先由独立研究者检索和审查。

#### 本轮核查来源

- [Terence Tao, 254A Notes 9 – second moment and entropy methods, Exercise 8](https://terrytao.wordpress.com/2019/11/12/254a-notes-9-second-moment-and-entropy-methods/)；一手来源：true；核验：Exercise 8 明确给出按 1/p 加权的平方采样误差界。它直接控制 Lδ²，未在正文中给出本题所需的 O(log N/N) 精度。
- [Terence Tao 在 Erdős Problem #635 讨论串中的原评论](https://www.erdosproblems.com/forum/thread/635)；一手来源：true；核验：Tao 本人的评论称只应视渐近子问为已解，Elliott 型误差衰减很慢，而精度 O(log N/N) 远超该方法；他同时明确说相关图论论文并未研究独立集。
- [P. D. T. A. Elliott, Probabilistic Number Theory I](https://link.springer.com/book/10.1007/978-1-4612-9989-9)；一手来源：true；核验：出版社页核实 1979 年专著及 DOI；本轮仍未取得可检查正文来独立核验所传引的 Lemma 4.7，因此不依赖该编号。

### #679

- 第一轮障碍：primorial 路线产生的超额仅为相对量 Θ(1/loglog k)：ω(n−k)=F(k)(1+O(1/loglog k))。第一问需要固定的乘法增益 1+δ 才能被统一反驳，或需要同时控制所有 k 才能被证明；本路线两者都没有。
- 第一轮下一定理：清晰的下一目标是 Lau 的 Conjecture 8：证明其指定短区间内总有满足 ω(m)≥C₀log₂m/log₃m 的整数，其中常数满足 1≤d<C₀。Lau 的 Theorem 7.3 已证明该猜想会给出某个固定 δ>0，并对每个充分大 n 产生 1≪k<n、ω(n−k)>(1+δ)log k/loglog k，从而否定第一问。
- 第二轮用时：842.8 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：检验能否把 primorial 的临界相对增益升级为固定乘法增益；补齐 Lau Conjecture 8 条件蕴含中的端点与统一阈值量词；寻找严格弱化或可证的最大空隙定理。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_FINITE_SCAN_CORRECTION；范围：独立复核第二轮三项结论：固定 ε、K 后，候选正解的计数为 O_{ε,K}(X/log_2 X)；Lau Conjecture 8 经 x=n−K 平移后严格蕴含 #679 第一问对某个固定 ε=δ 的否定；单一 primorial 的最大空隙基线恰停在临界系数 C_0，跨过障碍需要相对于 r log r 的固定比例节省。这里 log_j 表示 j 次迭代自然对数。
- 复核方式：逐项重建固定平移的二阶矩计数、Conjecture 8 的原始区间端点和统一 K 量词、一般最大空隙引理、primorial 格点构造及临界常数；核对 Lau、Khan、Axler 的一手文本；重跑两份 5,000,000 范围资产并用 SymPy 抽样交叉检查。另按 Conjecture 8 真正的窗口 ((log x)/2)^d 重算有限扫描，发现原脚本漏掉了因子 2^(−d)；主代理随后修正并重跑两份脚本。
- 证据边界：未发现推翻固定 K 二阶矩上界、x=n−K 条件修复或 primorial 临界系数的数学缺口。有限扫描漏掉 /2 的问题已修正，两份实现以精确窗口重跑得到一致计数，并显式标明 max_gap 与 xmin 的不同统计起点。最重要的状态边界是：零密度结论无条件；#679 第一问的负答案仍完全依赖尚未证明的 Lau Conjecture 8。

#### 第二轮实际尝试

- **固定 k 的密度攻击**（advanced）：在题面的全称量词中固定任意整数 k=K，并使用 ω 的二阶矩。；若 n 满足题面，则 ω(n−K)<B_{ε,K}:=(1+ε)log K/loglog K，故 ω(n−K)≤R_{ε,K}:=⌈B_{ε,K}⌉−1。R_{ε,K} 固定，而 Khan 式(1.3)和 Chebyshev 不等式给 #{m≤X:ω(m)≤R_{ε,K}}=O_{ε,K}(X/log₂X)。
- **复核并修补 Lau 的条件蕴含**（advanced）：不令 Conjecture 8 的区间右端为 n，而对任意预先给定 K 应用于 x=n−K。；所得 m≤n−K，令 k=n−m，则 k≥K，且 k<K+((log(n−K))/2)^d。于是 log k≤(d+o(1))log₂n，而 ω(m)≥(C₀+o(1))log₂n/log₃n。故对任意 0<δ<C₀/d−1，所有充分大 n 都有 k≥K 且 ω(n−k)>(1+δ)log k/loglog k。
- **用已知 Poisson 间距定理替代最大空隙猜想**（blocked）：核对 Khan Theorem 1.2 的尺度和量词。；该定理描述典型最近邻间距的分布，未给最长空隙的统一上界；分布收敛仍允许无限多个异常长空隙。因此不能推出每个充分大 n 都存在违反见证。
- **单一 primorial 攻击 Conjecture 8**（blocked）：取 r≈C₀log₂X/log₃X，以 Q_r 的倍数保证 ω≥r，并逐项比较区间指数。；log Q_r=(1+o(1))rlog r=(C₀+o(1))log₂X，所以 Q_r=(log X)^{C₀+o(1)}。倍数构造只能保证长度约 Q_r 的每个区间命中，而条件反证要求长度指数 d<C₀；缺少固定指数节省。
- **有限范围主动证伪**（inconclusive）：以两种独立算法计算 ω，并按 Conjecture 8 的动态阈值扫描左空隙。；按 Conjecture 8 的精确窗口 H=((log x)/2)^d，在 10^5≤x≤5×10^6 上，参数 (C₀,d)=(1.5,1),(2,1),(2.5,2) 分别出现 2,616,603、4,681,708、4,464,340 个失败端点。它们否定这些参数的有限起点版本，但不反驳“充分大 x”的渐近猜想；max_gap 字段从 x=2 起统计，与 failures 的 xmin 不同。

#### 第二轮新增严格进展

- [第二轮新增] 对任意固定 ε>0、K>e^e，记 N_{ε,K}(X) 为不超过 X 且对所有 K≤k<n 满足题面不等式的 n 数量，则 N_{ε,K}(X)=O_{ε,K}(X/log₂X)。特别地，任何可能的正解序列自然密度为 0。
- [第二轮复核加固] Lau Conjecture 8 的直接代入存在 m=x 导致 k=0 的端点可能；对任意固定 K 改用 x=n−K 后，命中右端点只会给 k=K，并且完整闭合“对任意统一阈值 K”的反证量词。
- [第二轮新增] 一般最大空隙判据：若高-ω 集合每个 (x−H(x),x] 都含 m，且 ω(m)≥C₀log₂m/log₃m、log H(x)≤(d+o(1))log₂x，其中 d<C₀，则对任意 δ<C₀/d−1、任意固定 K，所有充分大 n 都有 K≤k<n 违反 (1+δ) 界。
- [第二轮新增] 对 r=⌈C₀log₂X/log₃X⌉，单一 primorial 基线仅给空隙 exp((1+o(1))rlog r)=(log X)^{C₀+o(1)}。因此跨越第一问障碍等价于在 rlog r 的指数中取得某个固定比例节省，而非改进低阶项。

#### 证伪与边界检查

- 检查 Lau 区间命中右端点 m=x：直接令 x=n 确实可产生 k=0；平移 x=n−K 后同一边界变成允许的 k=K。
- 在最大空隙判据中使用 F(t)=log t/loglog t 的最终单调性；由 k<K+H(n−K) 得 F(k)≤F(K+H(n−K))，没有从单独的 log k 上界错误处理分母。
- 严格比较常数：只取 δ<C₀/d−1，而没有把渐近等式边界 δ=C₀/d−1 当作严格不等式。
- 两套 ω 数组在 0≤m≤5,000,000 上逐字节一致，SHA-256 均为 8e649ddc7f7cd5eb37c3724b5a5199b2e98651b1e0ab9163fc51edbb396c760b。
- 另以 sympy.factorint 对 1,008 个 primorial 边界点及固定随机种子样本复核，两种筛法均完全通过；首次检查因测试点 510510 超出临时数组上界而触发 IndexError，扩大数组后重算通过。
- 有限扫描按开区间左端正确判定：若最近合格数距离 dist≥H，则 (x−H,x] 失败；没有把左端等号误算为命中。
- 计算中的大量有限反例只用于否定小范围证据；由于 Conjecture 8 是最终渐近命题，未将其报告为反例。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679/gap_scan_sieve.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679/gap_scan_sieve.py)：按每个素数的倍数累加生成 ω；以精确窗口 H=((log x)/2)^d 扫描动态集合 A_{C₀} 的左空隙及 Conjecture 8 有限版本；max_gap 字段明确从 x=2 起统计。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679 && python3 gap_scan_sieve.py --nmax 5000000 --xmin 100000；结果：三组 (C₀,d) 的失败数依次为 2,616,603、4,681,708、4,464,340；最后失败端点依次为 4,999,994、4,999,994、5,000,000。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679/gap_scan_spf.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679/gap_scan_spf.py)：独立的最小素因子筛与递推 ω(v)=ω(v/p)+1_{p∤v/p} 实现；使用不同筛法，以同一精确窗口 H=((log x)/2)^d 扫描。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/679 && python3 gap_scan_spf.py --nmax 5000000 --xmin 100000；结果：输出逐字段与第一实现完全一致，包括 ω 数组哈希、失败数、最后失败端点、最大空隙及最坏 dist/H 比值。

#### 当前障碍

现有无条件结果只给 ω 的正常阶、固定维平移相关性或典型间距分布，不能控制高-ω 集合的最大空隙。单一 primorial 恰停在临界指数 exp((1+o(1))rlog r)；尚无方法把指数系数降为 1−η，也未在检索到的一手文献中找到这样的定理。

#### 下一精确定理

定义 G_r(X)=max_{X≤x≤2X} min{x−m:1≤m≤x, ω(m)≥r}。清晰的下一定理是：证明存在 C>1 和 η>0，使 r=⌈C log₂X/log₃X⌉ 时 G_r(X)≤exp((1−η)rlog r)。取略小于 C 的阈值常数并吸收 o(1) 后，这给出长度 (log X)^d，其中 d<C，从而经本轮的平移判据否定第一问。

#### 第二轮证明记录

【承接的第一轮事实】第一轮已经严格证明统一 O(1) 加法版本为假，并确认后退一级 primorial 见证的乘法比值趋于 1；本轮不把这些重新计为进展。第一问仍要求固定乘法增益或同时控制全部 k。

【第二轮新增推导】首先直接利用题面的全称量词。固定 ε>0、整数 K>e^e，并令
\[B_{\epsilon,K}=(1+\epsilon)\frac{\log K}{\log\log K},\qquad R_{\epsilon,K}=\lceil B_{\epsilon,K}\rceil-1.\]
若 n 对所有 K≤k<n 合格，则取 k=K 得 ω(n−K)≤R_{ε,K}。Khan 式(1.3)给出
\[\sum_{m\le X}(\omega(m)-\log_2X)^2\sim X\log_2X.\]
当 X 足够大且 ω(m)≤R_{ε,K} 时，偏差至少为 \(\tfrac12\log_2X\)。故
\[\#\{m\le X:\omega(m)\le R_{\epsilon,K}\}\ll_{\epsilon,K}\frac{X}{\log_2X}.\]
平移 m=n−K 即得候选 n 的同一上界。这不能排除无限稀疏序列，但严格证明任何正解集合必为零密度。

其次补齐 Lau 的条件反证。设某些 C₀>d>0 和 H 满足每个充分大 x 的 (x−H(x),x] 含 m，且
\[\omega(m)\ge C_0\frac{\log_2m}{\log_3m},\qquad \log H(x)\le(d+o(1))\log_2x.\]
给定任意固定 K，对 x=n−K 应用此条件并置 k=n−m。则
\[K\le k<K+H(n-K),\qquad m=n-k=n-o(n).\]
由于 F(t)=log t/loglog t 最终递增，
\[F(k)\le F(K+H(n-K))\le(d+o(1))\frac{\log_2n}{\log_3n},\]
而
\[\omega(m)\ge(C_0+o(1))\frac{\log_2n}{\log_3n}.\]
所以对每个 \(0<\delta<C_0/d-1\)，所有充分大 n 都有 k≥K 且
\[\omega(n-k)>(1+\delta)F(k).\]
这不仅修复 m=x、k=0 的端点，也覆盖任意候选统一阈值 K。Lau Conjecture 8 取 \(H(x)=((\log x)/2)^d\)，正好满足此判据。

最后精确定位 primorial 障碍。令 \(Q_r=\prod_{j\le r}p_j\)。任意长度 Q_r 的区间含 Q_r 的倍数，故能保证其中某个 m 满足 ω(m)≥r。但
\[\log Q_r=\vartheta(p_r)=(1+o(1))r\log r.\]
若 \(r=\lceil C_0\log_2X/\log_3X\rceil\)，则
\[r\log r=(C_0+o(1))\log_2X,\qquad Q_r=(\log X)^{C_0+o(1)}.\]
因此该构造只能达到指数 C₀；条件反证需要严格较小的 d。真正缺少的是
\[G_r(X)\le \exp((1-\eta)r\log r)\]
中的固定 η>0，而不是 primorial 渐近式的低阶修正。

【仍未闭合的缺口】没有无条件最大空隙界达到上述固定指数节省。Khan Theorem 1.2 只控制典型间距分布；它允许异常长空隙，故不能把“几乎所有区间”提升为“每个区间”。有限计算同样远离渐近尺度，不能支持或反驳 Conjecture 8。

【来源成熟度与优先权】Axler 2019 与 Khan 2010 均为已发表的一手论文；Lau 2026 目前是 arXiv v2，尚不应视为完成同行评审。Conjecture 8 及其对 #679 的条件反证优先权属于 Lau。本轮的 x=n−K 写法是对其端点和统一 K 量词的显式加固；零密度推论是由经典二阶矩直接推出的简单新观察，不主张文献首创。实时检索未找到证明所述 G_r(X) 固定指数节省的一手来源。

#### 本轮核查来源

- [Cheuk Fung Lau, On the Number of Prime Factors of Consecutive Integers, arXiv:2604.15042v2](https://arxiv.org/pdf/2604.15042)；一手来源：true；核验：第36页 Conjecture 8 令 A={m:ω(m)≥C₀log₂m/log₃m}，猜测某些 1≤d<C₀ 使每个充分大 x 的区间 (x−((log x)/2)^d,x] 命中 A；Theorem 7.3 声称这蕴含某个固定 δ>0 的统一反例。正文直接代入 x=n 时存在右端点 m=n、k=0 的可能性，但可用本轮的 x=n−K 平移严格修补。
- [Rizwanur Khan, Spacings between integers having typically many prime factors, arXiv:0803.1868v5 / Canadian Mathematical Bulletin 53 (2010), 102–117](https://arxiv.org/pdf/0803.1868)；一手来源：true；核验：式(1.3)给出 ∑_{m≤X}(ω(m)−log₂X)^2∼Xlog₂X；Theorem 1.2 是 δ-normal 整数的 Poisson 型间距分布，不是最大空隙上界。前者支持本轮的候选 n 零密度结论，后者不能替代 Lau Conjecture 8 的“每个区间”量词。
- [Christian Axler, New Estimates for the nth Prime Number, Journal of Integer Sequences 22 (2019), Article 19.4.2](https://cs.uwaterloo.ca/journals/JIS/VOL22/Axler/axler17.pdf)；一手来源：true；核验：式(1.1)为 p_r∼rlog r，式(1.2)给出更精细的 Cipolla 展开。结合素数定理 θ(p_r)∼p_r，可得第 r 个 primorial Q_r 满足 log Q_r=(1+o(1))rlog r。

### #686

- 第一轮障碍：最小未闭合分支现在是 N=4、k≥5。已有文献只说明每个固定 k>2 的解集有限，没有统一排除全部 k 的机制；因此尚不能声称 N=4 是反例，更不能解决原问题。
- 第一轮下一定理：精确下一定理：令 F₅(t)=∏_{i=1}^5(t+i)，证明方程 F₅(m)=4F₅(n) 没有满足 n,m∈ℕ、m≥n+5 的解。必须完整确定该五次曲线的相关整数点，或给出等价的可认证 Thue/Thue–Mahler 归约；单纯有界搜索不够。
- 第二轮用时：2181.0 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：先攻击第一轮提出的 F₅(m)=4F₅(n) 无解命题；将其降到 primitive 二次式和 genus 2 曲线，主动证伪过强的“目标区间无有理点”路线，并精确保留整数平方回升条件。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_MINOR_SCOPE_CLARIFICATIONS；范围：独立复核 N=4、k=5 分支的中心化归约、y≥16 与比例区间、primitive 的 D 四次方程、D² 整除和上界、genus-2 判别曲线及完整整数 lift 条件；并复核 r=14/11 只反驳“目标区间没有有理点”等过强中间命题。
- 复核方式：从原产品方程重新推导每个变量替换及反向 lift，独立核对多项式判别式、无重根和 genus；分析两种单调扫描与两种既约分母枚举的完整量词；按仓库原范围重跑 Python、PARI/GP、Sage，并以 SymPy 作第三套符号核验。未修改 #686 原结果或任何工作资产。
- 证据边界：中心化、y≥16、primitive 方程、D² 条件、genus-2 曲线和整数 lift 的数学链条通过独立复核。r=14/11 是对过强中间路线的真实反例，却不是原方程整数解。现阶段最强结论仍只是两个明确有限范围内没有 admissible lift；全局 k=5 及 #686 均保持开放。

#### 第二轮实际尝试

- **k=5 边界与尺度攻击**（advanced）：令 x=m+3、y=n+3，并研究 f(t)=t(t²−1)(t²−4)。；方程化为 f(x)=4f(y)，条件为 y≥3、x≥y+5。置 h(t)=f(t)/t⁵=1−5/t²+4/t⁴；t≥3 时 h'(t)=(10t²−16)/t⁵>0，故 x⁵<4y⁵。又 4^{1/5}<4/3，遂 x<4y/3；结合 x≥y+5 得 y≥16。
- **primitive 二次式归约**（advanced）：写 D=gcd(x,y)、x=Dv、y=Du、gcd(u,v)=1，并令 Z=D²。；由 f(Dv)=4f(Du) 得 (4u⁵−v⁵)Z²−5(4u³−v³)Z+4(4u−v)=0。目标区间内三个括号均为正。模 Z 立刻得到 Z∣4(4u−v)；因 v>u，进一步有 D²=Z<12u。
- **genus 2 商曲线归约**（advanced）：置 r=x/y、z=y²，把五次方程视为关于 z 的二次式。；得到 (r⁵−4)z²−5(r³−4)z+4(r−4)=0。其判别式为 Δ(r)=9r⁶+64r⁵−200r³+64r+144；该六次多项式无重根，故 C:s²=Δ(r) 是 genus 2 曲线。每个整数解必给出 C(ℚ) 上点及一个整数平方根 z。
- **证伪过强的空区间路线**（refuted）：精确枚举既约 r=p/q，满足 1<r、r⁵<4，并检查齐次判别式是否为平方。；找到 r=14/11，且 s=10740/11³，严格满足 C。二次式两根为 z=242/197 与 z=121/9；后者是有理平方 (11/3)²，给出有理解 (x,y)=(14/3,11/3)，但不是整数平方且 x−y=1。因此“C(ℚ) 在目标区间为空”乃至“没有有理 lift”的过强说法都被反驳，但该点不回升为原方程整数解。
- **原整数方程双实现搜索**（inconclusive）：Python 与 PARI/GP 分别利用 f 的严格单调性，对每个 y 定位唯一可能的 x，全程使用精确大整数。；两种实现均完整检查 3≤y≤5,000,000，没有 f(x)=4f(y)、x≥y+5 的点。恒等式 f(8)=252f(3) 仅作为中心化函数与大整数等式判断的代数正控制；它不是 N=4 扫描命中分支的正例。
- **尝试完整确定 C(ℚ)**（blocked）：检查本地 Sage 的 genus 2 功能及 Magma 官方 Chabauty 条件。；Sage 只能给出有界点表；本地缺少能认证 Jacobian 秩、Mordell–Weil 生成元和饱和性的 Magma 环境。因此没有得到完整有理点集合。

#### 第二轮新增严格进展

- [第二轮新增] 若 N=4、k=5 有合法解，则中心变量必满足 y=n+3≥16 且 y+5≤x<4^{1/5}y<4y/3。
- [第二轮新增] 对任何 k=5 解，primitive 参数满足 (4u⁵−v⁵)D⁴−5(4u³−v³)D²+4(4u−v)=0，并有 D²∣4(4u−v) 及 D²<12u。
- [第二轮新增] k=5 问题被精确压到 genus 2 曲线 C:s²=9r⁶+64r⁵−200r³+64r+144，再附加二次根 z 为整数平方、ry为整数及间距条件。
- [第二轮新增] 过强中间命题 C(ℚ)∩{1<r<4^{1/5}}=∅ 被 r=14/11 严格反驳；其两个 z 根为 242/197、121/9，其中 121/9=(11/3)² 给出有理解 (14/3,11/3)，但变量非整数且间距仅为 1，故不构成原题解。
- [第二轮新增] Python 与 PARI/GP 两种独立精确实现均排除 N=4、k=5、3≤y≤5,000,000 的全部合法点。这只是明确有界结论。
- [第二轮新增] 两种独立实现交叉枚举既约分母 q≤5000：目标区间内只找到 r=14/11，且无整数平方 lift；Python 单独延伸到 q≤10000，仍只有该点。

#### 证伪与边界检查

- Sage 的 bound=100 点表较短，bound=300 又出现 r=−19/9、4 等点；随后分母枚举还发现 r=14/11。这直接否定了把任一有界 Sage 点表当成 C(ℚ) 完整枚举的做法。
- 主动检验过强路线“目标实区间无有理点”，由 r=14/11 严格击穿；最终下一定理已保留平方回升条件。
- 边界 n=0 对应 y=3，双实现搜索从 y=3 开始，没有遗漏题面允许的零自然数。
- 代数控制 f(8)=252f(3) 在 Python 与 GP 中均通过，检查了中心化函数和大整数相等判断；它没有让 N=4 扫描分支产生实际命中，因此不承担单调扫描完整性的正例验证。
- Erdős–Straus 式 (1.1) 只允许对固定 t,k 断言有限性；没有把它错误交换为跨所有 k 的统一结论。
- Sage 验证 Δ(r) 的展开式和 genus；PARI/GP 独立验证判别式恒等式。r=14/11 的曲线等式与两个 z 根又由 Sage 独立重算。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_scan.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_scan.py)：Python 精确单调扫描 N=4、k=5，并检查 primitive 二次式与整除条件。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686 && python3 k5_scan.py --limit 5000000；结果：输出 hits: []；SHA-256 为 fdd93fb52801f9e998461cab320eb1ee2adc87778acb0090c39a507f57af09a4。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_crosscheck.gp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_crosscheck.gp)：独立 PARI/GP 大整数扫描，并验证判别式恒等式及中心化函数的代数控制。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686 && gp -q k5_crosscheck.gp；结果：独立输出 3≤y≤5,000,000 时 hits: []。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient_interval.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient_interval.py)：按既约分母精确搜索 genus 2 曲线的目标实区间，并对两个 z 根执行完整整数平方 lift 检查。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686 && python3 k5_quotient_interval.py --max-denominator 10000；结果：检查 9,712,235 个既约分数；只发现 (p,q,W)=(14,11,10740)，z 根为 242/197、121/9；admissible integer lifts 为空。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient_interval.gp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient_interval.gp)：PARI/GP 对目标区间既约分母枚举的独立实现。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686 && gp -q k5_quotient_interval.gp；结果：对 q≤5000 独立检查 2,428,402 个既约分数；同样只得到 [14,11,10740,242/197,121/9]，无整数平方 z。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient.sage](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686/k5_quotient.sage)：Sage 验证 genus 2 判别式、曲线 genus、有界点搜索，并独立核验 r=14/11。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/686 && DOT_SAGE=/tmp/sage686 sage k5_quotient.sage；结果：验证 Δ=9r⁶+64r⁵−200r³+64r+144、genus=2；bound=300 返回19点；独立确认 r=14/11 的 z 根为 242/197、121/9。

#### 当前障碍

尚未证明 N=4、k=5 全局无解。精确缺口是：排除 C(ℚ) 目标区间内那些二次根 z 恰为整数平方、且 x=ry为整数并满足 x−y≥5 的点。仅求 C(ℚ) 的一个有界子集不够；需要可认证的 Jacobian 秩、Mordell–Weil 生成元与饱和/Chabauty–Mordell–Weil sieve，或直接利用 D²∣4(4u−v) 的算术下降。即使 k=5 闭合，原问题的 N=4、k≥6 仍未解决。

#### 下一精确定理

精确下一定理：令 C:s²=9r⁶+64r⁵−200r³+64r+144。对每个满足 1<r、r⁵<4 的 (r,s)∈C(ℚ)，令 z_±=[5(r³−4)±s]/[2(r⁵−4)]。证明不存在符号使 z_±=y²，其中 y∈ℤ、y≥3、ry∈ℤ 且 ry−y≥5。等价的 primitive 形式是：不存在互素正整数 u<v 及 D≥1，使 Du≥3、D(v−u)≥5 且 (4u⁵−v⁵)D⁴−5(4u³−v³)D²+4(4u−v)=0。

#### 第二轮证明记录

承接的第一轮事实

第一轮已审计结论把所有非平方 N 用 k=2 的 Pell 构造处理，并把 N=4 在 k=2,3,4 的分支排除。本轮只把这些作为可挑战的前提；重新检查了题面自然数量词、k=4 降阶恒等式及 k=3 脚本的量词结构，没有把它们重记为新增进展。因此当前最小分支确为 N=4、k=5。

第二轮新增推导

令
f(t)=(t-2)(t-1)t(t+1)(t+2)=t^5-5t^3+4t,
并置 x=m+3、y=n+3。则 k=5 方程精确化为
f(x)=4f(y),\qquad y\ge3,\quad x\ge y+5.
对 t≥3，
h(t)=f(t)/t^5=1-5t^{-2}+4t^{-4},\qquad h'(t)=(10t^2-16)/t^5>0.
由于 x>y，等式给出 x^5h(x)=4y^5h(y)，从而 x^5<4y^5。又 4^{1/5}<4/3，故 x<4y/3；与 x≥y+5 合并得 y>15，即任何解必须有 y≥16。

再写 D=gcd(x,y)、x=Dv、y=Du、gcd(u,v)=1，令 Z=D²。展开后得到
(4u^5-v^5)Z^2-5(4u^3-v^3)Z+4(4u-v)=0. \tag{1}
由 1<v/u<4^{1/5} 可知三个括号均为正。式 (1) 模 Z 给出
Z\mid4(4u-v).
又 4u-v<3u，故 D²<12u。这是此前五次曲线描述中没有的 primitive 整除约束，但它尚未把 u 有界化。

置 r=x/y、z=y²，原式除以 y 后成为
(r^5-4)z^2-5(r^3-4)z+4(r-4)=0. \tag{2}
故判别式必须为有理平方：
s^2=25(r^3-4)^2-16(r^5-4)(r-4)
=9r^6+64r^5-200r^3+64r+144. \tag{3}
右侧六次多项式无重根，因此 (3) 定义 genus 2 曲线 C。反向回升并非自动成立：还必须有
z_\pm=\frac{5(r^3-4)\pm s}{2(r^5-4)}=y^2,
其中 y 是整数、ry是整数且 ry-y≥5。

最重要的证伪检查是：目标区间并非没有有理点。精确计算给出
r=14/11,\qquad s=10740/11^3,
它满足 (3)，且式 (2) 的两根是
z=242/197,\qquad z=121/9=(11/3)^2.
第二根给出有理解 (x,y)=(14/3,11/3)，但 x、y 不是整数且 x-y=1<5。故该点不产生原方程整数解，却严格推翻了“目标区间 C(ℚ) 为空”乃至“没有有理 lift”的过强路线；清分母得到 (14,11) 也不合法，因为 f 不是齐次函数。

两套独立大整数扫描均排除了 3≤y≤5,000,000。另两套既约分母枚举在 q≤5000 时都只找到上述 r=14/11，且无整数平方 lift；Python 延伸到约分后分母 q≤10000，结果不变。这些都是严格的有限范围结论，不能外推为全局无解。

仍未闭合的缺口

本轮没有完整确定 C(ℚ)，也没有证明所有目标区间有理点都不满足整数平方 lift 条件。Sage 的 rational_points(bound=300) 明确只是项目高度有界枚举；事实上它没有列出稍高的 r=14/11 点，恰好说明不能冒充完整证明。若用 Chabauty 路线，仍需认证 Jacobian 的 Mordell–Weil 秩、生成元和饱和指数；若走初等路线，则必须把 D²∣4(4u−v) 加强为真正有限的下降。并且即便 k=5 被排除，N=4 的 k≥6 仍是原题全称量词的缺口。

来源成熟度和潜在优先权

Erdős–Straus 1977 年论文的引言式 (1.1) 已直接覆盖固定 t、固定 k 的有限性，比第一轮采用的 2003 年一般连续积定理更早、更贴题；但其调用 Thue–Siegel 只给有限性，不给本题所需的完整点表。Erdős 1979 年原始论文的作者扫描件已核对书目信息，但实时 OCR 未定位官网精确全称题面的页码，故不声称找到了原始编号。Sage 和 Magma 的引用仅用于说明软件命令的严格范围及下一步认证条件，没有把软件文档当成数学证书。

#### 本轮核查来源

- [FormalConjectures, ErdosProblems/686.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/686.lean)；一手来源：true；核验：重新核对了 n,m∈ℕ、k≥2、m≥n+k 的量词；文件仍将总问题、平方分支及 N=4 标为 open。含 sorry 的变体没有被当作证明。
- [P. Erdős and E. G. Straus, On Products of Consecutive Integers, Number Theory and Algebra (1977), 63–70](https://combinatorica.hu/~p_erdos/1977-18.pdf)；一手来源：true；核验：引言定义 A(n,k)=(n+k)!/n!，并在式 (1.1) 后明确陈述：固定 k≥3、t>1 时，tA(n,k)=A(m,k) 只有有限多个整数解；还指出 k=2、非平方 t 的 Pell 构造。该结果直接给出固定 N=4,k=5 的有限性，但不提供有效枚举。它比第一轮引用的 2003 年一般性有限定理更早且更贴合本题。
- [P. Erdős, Some Unconventional Problems in Number Theory, Acta Math. Acad. Sci. Hungar. 33 (1979), 71–80](https://combinatorica.hu/~p_erdos/1979-23.pdf)；一手来源：true；核验：核对了作者档案中的论文身份与书目信息；实时可取 OCR 未能定位官网精确全称题面的页码或编号，因此不虚报原文位置。
- [SageMath official documentation: Hyperelliptic curves over a general ring](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/hyperelliptic_curves/hyperelliptic_generic.html)；一手来源：true；核验：官方文档说明 rational_points(bound=B) 是有界有理点枚举。故本轮 Sage 的 bound=300 输出只作为有限搜索，绝不视为 C(ℚ) 的完整集合。
- [Magma Handbook: Chabauty’s Method](https://magma.maths.usyd.edu.au/magma/handbook/text/1619)；一手来源：true；核验：官方文档给出 genus 2 曲线在 Jacobian 秩 0，或秩 1 且生成元、饱和条件获认证时，用 Chabauty 与 Mordell–Weil sieve 完整确定有理点的方法。本地没有 Magma，未执行或伪造此证书。

### #776

- 第一轮障碍：候选新定理已有第二位代理的独立逐步审阅和主代理的复跑核验，但属于未发表的新推导，仍需外部同行评审。继续提高到 $n=2r+4$ 时，残余格变为 $r+3$ 点并出现五个混合层；当前覆盖引理不再直接给出所需的 $r-1$ 个 2-覆盖。
- 第一轮下一定理：下一精确定理应是判定对所有 $r\ge4$ 是否有 $g(2r+4,r)\le2r$。对应的局部目标是推广覆盖引理：控制一个 $r$ 边图在同时存在连续高层补集反链时的 2、3、4-顶点覆盖轮廓；若该命题为假，则应从其最小覆盖轮廓构造 $n=2r+4$ 的反链。
- 第二轮用时：1895.0 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：先主动寻找 g(2r+4,r)=2r+1 的小参数反例，再把五个混合层写成两个残余反链的精确轮廓；在发现旧高层覆盖引理不能直接推广后，引入此前未使用的残余第3层，最终得到覆盖全部 r≥4 的候选证明。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：第二轮候选定理 g(2r+4,r)≤2r（所有 r≥4）、由此推出 n_0(r)≥2r+4、五层残余方程、单支二覆盖上界及 r=4 端点；不包括对完整 n_0(r) 的确定。
- 复核方式：从原反链重新推导端点共同星与两支残余分解，逐层核对补集方向和五个计数方程；独立审查 r≥5 图分类与 r=4 端点；重跑五个完整端点轨道、r=4 残余轮廓、全部标号覆盖层枚举及旧引理反例。
- 证据边界：该 PASS 是对内部候选证明的数学复核，不等于发表或形式化认证。程序只完整处理 r=4；r≥5 的全称量词来自上述符号分类。定理仅把已知阈值下界推进到 n_0(r)≥2r+4，仍未确定 n_0(r)，所以不是 Erdős #776 的完整闭合。

#### 第二轮实际尝试

- **主动证伪旧覆盖引理的朴素推广**（refuted）：只保留 r+3 点残余格中的2、3、4点覆盖层，寻找允许多个2点覆盖的配置。；r=6 时取六边星图、两个由星心与孤立点组成的2覆盖；在六个叶上取五边星作为3覆盖的残余对，再取其五个非心叶中的任意六个三元组作为4覆盖。全部覆盖和不可包含条件均成立。因此‘高覆盖层单独迫使至多一个2覆盖’为假，不能照搬第一轮引理。
- **n=12 的完整端点轨道 SAT**（advanced）：对 r=4 固定共同星心；按 s=|P∩Q|=0,1,2,3,4 穷尽端点同构轨道。每个兼容内部集合设布尔变量，每层恰选4个，并加入全部跨层包含冲突。；五个轨道全部由 Z3 返回 UNSAT；候选数逐层为 4,21,36,42,42,42,36,21,4，每个轨道包含冲突为2982或3009。这直接排除了最小参数的原问题反例，而非只排除简化轮廓。
- **五个混合层的残余轮廓**（advanced）：把含共同星心的成员投影到 U，把不含星心的成员在 R 中取补；令 N=r+3。；精确得到 a_{N−4+j}+c_{N−j}=r（j=0,…,4），并由 a_2=c_2=r 推出 a_{N−4}=c_{N−4}=r、a_{N−3},c_{N−3}≥r−1、a_{N−2}+c_{N−2}=r；同时两支第3层均恰有 r 个成员。
- **用残余第3层修复覆盖路线**（advanced）：设一支有 d≥2 个2点覆盖，先分类底层 r 边图，再用该支恰有 r 个3集限制 d。；两个2覆盖若不交则只可能给 K_{2,2} 且没有合格3覆盖；若相交，≥r−1个3覆盖排除额外横边，底图被迫为 r 边星。含星心的合格3集至多一个；不含星心者必须包含全部 d 个所选覆盖叶，故 d≥3 时也至多一个，与总数 r≥4 矛盾。因此每支 d≤2。r≥5 立即与两支 d 之和为 r 矛盾；r=4 的 d=2 等号由四点图独立三元组计数排除。

#### 第二轮新增严格进展

- [第二轮新增] 对 n=2r+4 的全部量词得到五层残余等式：a_{N−4+j}+c_{N−j}=r（0≤j≤4），其中 N=r+3；特别是 a_{N−2}+c_{N−2}=r，且两侧都有 r 个残余3集、至少 r−1 个补3覆盖和 r 个补4覆盖。
- [第二轮新增] 证明一支轮廓定理：在上述真实残余反链中，(N−2) 层至多有2个成员。关键不是错误的纯高层覆盖推广，而是同时利用残余第3层；若有至少两个补2覆盖，底层图必为星，随后3集计数排除三个或更多补2覆盖。
- [第二轮新增] 闭合候选定理的所有 r≥4 量词：r≥5 时两支上界2+2<r；r=4 时两边必各取2，补3覆盖在四点集上形成至少三边图，而其独立三元组至多一个，故补4覆盖总数至多2而非所需4。
- [第二轮新增] 因而候选结论为 g(2r+4,r)≤2r，并由阈值定义严格推出 n_0(r)≥2r+4；这比第一轮候选下界再推进一位，比 He–Tang v2 的下界推进两位。
- [第二轮复核加固] r=4 的五个原端点轨道全部精确 UNSAT；独立的覆盖层枚举遍历5985个七点四边图、3780个2覆盖对和31500个合格3覆盖族，最大合格4覆盖数为2，与符号证明的末端常数完全一致。

#### 证伪与边界检查

- 从 g≥n−3 到恰有 n−3 个出现层的步骤是保留任意 n−3 层并逐层删到恰好 r 个成员；没有把‘至少 r’偷换为未经论证的等号。
- 端点星的叶集 P,Q 允许任意重叠；残余推导和证明均未假设 P、Q 不交。r=4 的 SAT 另外穷尽了全部五个重叠轨道。
- 补集包含方向逐项核对：若 D_k 是高层成员的补，则底边不落入高层等价于 D_k 覆盖底图；高层反链性给 D_2 不包含于 D_3、D_4 以及 D_3 不包含于 D_4。
- 显式 r=6 配置证伪了过强的纯高层引理，确认新证明必须使用 A_3；没有从小 r 计算外推全体 r。
- r=4 末端没有遗漏不含星心的4覆盖：这类集合只能是全部四个星叶，故至多一个；含星心者对应四点图的独立三元组，也至多一个。
- 阈值推论检查了严格不等号：在 n=2r+4 处 g<n−3，故定义中要求所有 n>n_0 取等迫使 n_0≥2r+4，而不是 ≥2r+3。
- 候选定理只闭合单点下界，未被误标为完整求出 n_0(r) 或解决官网 #776。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/sat_n2r4_direct.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/sat_n2r4_direct.py)：n=2r+4 在共同星端点后的完整集合级 Z3 编码；r=4 时 |P∩Q| 穷尽全部端点轨道。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776 && for s in 0 1 2 3 4; do python3 sat_n2r4_direct.py --r 4 --overlap $s --timeout-ms 900000; done；结果：五个轨道全部 UNSAT；完整记录见 computation_summary.json。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/residual_profile_sat.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/residual_profile_sat.py)：独立的单支残余轮廓 Z3 编码，逐个判定 (a_{N−3},a_{N−2},a_{N−1}) 并按五层方程配对。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776 && python3 residual_profile_sat.py --r 4 --timeout-ms 900000；结果：20个单支轮廓全部判定；仅 (4,0,0),(4,1,0),(3,0,0),(3,1,0) 可行，无任何可配对双支见证。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/cover_layers_r4_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/cover_layers_r4_check.py)：不使用 Z3 的末端覆盖层全枚举，独立检查 r=4 特例。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776 && python3 cover_layers_r4_check.py；结果：遍历5985个标号四边图、3780个2覆盖对、31500个3覆盖族；合格4覆盖最大值2<4。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/high_layer_only_counterexample.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/high_layer_only_counterexample.py)：验证 r=6 的显式覆盖配置，证伪旧引理的朴素高层推广。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776 && python3 high_layer_only_counterexample.py；结果：PASS：2个2覆盖、5个3覆盖、6个4覆盖满足全部高层不可包含条件。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/proof_draft_n2r4.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/proof_draft_n2r4.md)：候选新定理 g(2r+4,r)≤2r 的自洽英文证明草稿，逐步记录量词归约、残余层指标、覆盖分类及 r=4 末端。；命令：sed -n '1,280p' /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/776/proof_draft_n2r4.md；结果：符号证明覆盖所有 r≥4；计算只承担 r=4 的独立有限审计。当前仍待外部专家评审。

#### 当前障碍

候选定理已经过三种计算编码的交叉核验和逐量词自审，但它是未发表的新推导，尚缺独立外部同行评审。即使该定理成立，完整 #776 仍需确定 n_0(r)；现有上界与 2r+4 之间仍有约 2log_2 r 的间隙。

#### 下一精确定理

下一精确节点是判定是否对所有 r≥4 有 g(2r+5,r)≤2r+1，从而 n_0(r)≥2r+5。此时 N=r+4 且出现六个混合方程 a_{N−5+j}+c_{N−j}=r（0≤j≤5）；中间只给 a_{N−3}+c_{N−2}=r 与 a_{N−2}+c_{N−3}=r，不再直接给两支 (N−2) 层之和。所需新引理应联合控制每支的补2覆盖数和补3覆盖数，而不能再次只看高覆盖层。

#### 第二轮证明记录

承接的第一轮事实

第一轮内部审计得到候选结论 g(2r+3,r)≤2r−1，并核对了端点共同星归约。本轮不把它重复计作新成果，只从其 next_theorem 精确攻击 n=2r+4。He–Tang v2 的正式文本范围仍止于 n≤2r+2。

第二轮新增推导

令 n=2r+4，反设 g(n,r)≥n−3。保留任意 n−3 个出现层并逐层删到恰好 r 个成员。0、n 层因容量不足不出现；若1层出现，其 r 个单点会使 n−r+1,…,n 全缺，加上0层至少缺 r+1≥5 层，矛盾；补集同理排除 n−1。因此出现层恰为2,…,n−2。

令 F_2 与 F_{n−2} 的补族 M 各为 r 个二元集。它们交叉相交。任一族若含两条不交边，另一族至多是四条 K_{2,2} 横边；r>4 立即矛盾，r=4 时反向命中这四条横边的二元集只有两个部类，也不够 r 个。因此两族均为相交边族，r≥4 迫使其为星；交叉相交再迫使共同星心 x。写叶集为 P,Q。

令 U=[n]\({x}∪P)、R=[n]\({x}∪Q)，则 |U|=|R|=N=r+3。含 x 的内部成员唯一写为 {x}∪Z、Z⊆U；不含 x 者必须包含 Q，唯一写为 Q∪W、W⊆R。前者残余组成反链 A，后者在 R 中取补组成反链 C，层数记 a_k,c_k。原第3层和第 n−3 层给 a_2=c_2=r，故 a_N=c_N=0。五个混合层 t=r+j 给

a_{N−4+j}+c_{N−j}=r，  j=0,1,2,3,4。

残余 (N−1) 层至多一个成员，因为其补单点必须属于全部 r 个不同的残余2集。于是

a_{N−4}=c_{N−4}=r，
a_{N−3},c_{N−3}≥r−1，
a_{N−2}+c_{N−2}=r。

还需证明每支 (N−2) 层至多2。以 A 为例，把 A_2 看作 r 边图 G，把 A_{N−2},A_{N−3},A_{N−4} 取补，分别得到 d 个2覆盖、至少 r−1 个3覆盖和 r 个4覆盖，且小覆盖不包含于所选大覆盖。若 d≥2，取两个2覆盖 X,Y。它们若不交，则 G 只能是 r=4 的 K_{2,2}，但每个顶点覆盖均包含 X 或 Y，不能有合格3覆盖。故 X={z,p},Y={z,q}。每条 G 边含 z 或等于 {p,q}；后一条若存在，合格3覆盖至多一个，仍矛盾。因此 G 是以 z 为心的 r 边星，在 N=r+3 点上另有恰好两个孤立点。

此时 A_3 恰有 r 个成员。含 z 的3集为避免包含星边，只能是 z 加两个孤立点，至多一个；不含 z 的3集为避免落入每个 A_{N−2} 成员，必须包含所有 d 个所选覆盖叶。当 d≥3 时这种3集也至多一个，总计至多2<r。故 d≤2；C 同理。若 r≥5，这与 a_{N−2}+c_{N−2}=r 矛盾。

只剩 r=4 且两支 d=2。任取一支，其底图是四边星。两个2覆盖写成 {z,p},{z,q}，余下 W 有四点。至少三个合格3覆盖均为 z 加 W 中一条边，形成 W 上至少三边的图 H。含 z 的合格4覆盖对应 H 的独立三元组；H 至少三边时独立三元组至多一个。不含 z 的4覆盖只能是全部四个星叶，也至多一个。因此合格4覆盖至多2，与所需4矛盾。候选定理 g(2r+4,r)≤2r 得证，并推出 n_0(r)≥2r+4。

仍未闭合的缺口

这只在一个新的 n 上排除了 n−3 个层，没有构造或确定最终阈值。n=2r+5 的六个混合层不再产生 a_{N−2}+c_{N−2}=r，当前单支上界无法直接闭合。

来源成熟度与潜在优先权

He–Tang v2 是可核对的一手预印本，第一轮草稿是内部材料。本轮定理及证明尚未发表，也未完成专门的全网优先权检索；因此不主张文献新颖性或优先权。直接 SAT、残余轮廓 SAT 和独立覆盖枚举只支持有限 r=4 审计，全体 r 的依据是上述符号证明，仍应提交外部组合数学专家复核。

#### 本轮核查来源

- [Yixin He and Quanyu Tang, An Erdős–Trotter problem on antichains with multiplicity r on each occurring level, arXiv:2602.09803v2](https://arxiv.org/abs/2602.09803v2)；一手来源：true；核验：再次核对 Definition 1.1/1.3、Remark 1.2 与 Proposition 3.1：至少 r 与恰好 r 对 g 等价；阈值量词是对每个 n>n_0；现有下界证明的范围止于 n≤2r+2。第二轮只沿用并重证其端点共同星归约。
- 第一轮 #776 已审计证明草稿与独立复核；一手来源：false；核验：第一轮已内部复核 g(2r+3,r)≤2r−1；其共同星归约与补集覆盖方向作为本轮可挑战起点。本轮没有把该结论重复计作新进展。
- [Erdős Problems #776](https://www.erdosproblems.com/776)；一手来源：true；核验：用于核对原题仍要求估计完整阈值 n_0(r)，而不是只判定单个 n。本轮候选定理即使成立也仅改善下界。

### #788

- 第一轮障碍：唯一实质阻塞是多项式稀疏随机 Cayley-sum 图的独立数：现有 Alon–Pham Theorem 4 给 p^{-3/2} 量级，而平方根目标要求在 p≈N^{-1/2} 时把它降到 p^{-1}N^{o(1)}。现有反对数稀疏结果无法外推到这一范围。
- 第一轮下一定理：足够且接近最弱的下一定理是：当 N→∞（至少沿偶数 N）且 p=N^{-1/2+o(1)} 时，随机 S_p⊆ℤ_N 以高概率满足 α(Γ⁺(ℤ_N,S_p))≤p^{-1}N^{o(1)}。更弱的确定性版本也足够：对每个偶数 N，存在 S_N⊆ℤ_N，使 |S_N|≤N^{1/2+o(1)} 且 α(Γ⁺(ℤ_N,S_N))≤N^{1/2+o(1)}。任一版本经上述模 2n 转移立即推出 f(n)≤n^{1/2+o(1)}。
- 第二轮用时：1477.8 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：攻击第一轮的随机 Cayley-sum 阻塞。下界方面利用和图三角形极少这一此前未使用的结构；上界方面把所需输入严格弱化到题目区间上的随机 Hankel 和图，并确定其不可避免的对数尺度。
- 第二轮结论：route_advanced；完整解声明：none；置信度：medium

- 独立复核：PASS；范围：严格复核第二轮新下界 f(n)>=c*sqrt(n log n)：图论等价、三角形到三个和标签的单射、三角形与边数界、随机稀疏化、删三角形、Shearer/Caro--Wei拼接、三个|B|区间及全部对数端点；并复核随机区间和图的空和下界及f(13),f(14),f(15)精确计算。
- 复核方式：新下界确实是无条件、存在绝对常数c>0并对所有充分大的整数n成立的全称渐近下界，不是平均B、随机B或某个n子序列的结论。概率法只在证明中对每个固定B分别选择一个稀疏诱导子图，中央区间内所需趋于无穷均对m=|B|一致，因此常数和n_0可统一。随机空和区间下界和n=13..15精确值也通过复算。该进展只加强下界；官网所问f(n)<=n^{1/2+o(1)}的上界仍未证明，原题没有闭合。
- 证据边界：['已认证的是新的确定性下界f(n)=Omega(sqrt(n log n))以及随机区间和图的必要独立数下界，不是f(n)的匹配上界。', '要回答官网特别询问的f(n)<=n^{1/2+o(1)}，仍需例如在p=sqrt(log n/n)处证明alpha(G_{B_p})=O(p^{-1}log n)=O(sqrt(n log n)) with high probability。现有结果没有这一步。', 'sqrt(n log n)=n^{1/2+o(1)}，故新下界与猜测上界相容；它提高合理的匹配尺度但不肯定或否定原上界问题。', '结果文件将conclusion记为route_advanced、full_solution_claim记为none，并明确保留随机独立数上界阻塞；没有完整解越界。']

#### 第二轮实际尝试

- **少三角形结构下界**（advanced）：把每条边标记为其端点之和，计数三角形；随机稀疏化顶点、删除三角形后调用 Shearer。；若三角形顶点为 x,y,z，其标签 a=x+y、b=x+z、c=y+z 两两不同，且 x=(a+b−c)/2、y=(a+c−b)/2、z=(b+c−a)/2。因此标签三元组唯一决定三角形，故 T(G_B)≤binom(|B|,3)。在 |B|≈√n 的关键区间取 q=(1/100)√(N/|B|³) 随机保留顶点；以正概率保留 Θ(qN) 个顶点、O(q²N|B|) 条边和至多 qN/8 个三角形。删去每个三角形的一个顶点后，所得无三角形图平均度 O(q|B|)，Shearer 给 α(G_B)≫(N/|B|)log(q|B|)。
- **随机区间和图的边界证伪**（advanced）：在随机 B 中寻找连续空和区间，并把它提升为独立的连续顶点区间。；若 B 以概率 p 独立选取且 np→∞，取 k=floor(log(np)/(16p))。可在中央区域放置 Θ(n/k) 个顶点区间 C_j，使其 restricted sumsets C_j ̂+ C_j 是两两不交、长度 2k−3 的整数区间。每个为空的概率至少 (np)^{-1/4}，且事件独立，故以高概率某个 C_j 独立。因此 α(G_B)≥c p^{-1}log(np)。这严格否定了无对数的 α=O(p^{-1}) 随机强化，但不否定 p^{-1}n^{o(1)}。
- **只控制题目区间而非整个循环群**（advanced）：逐项比较第一轮 next theorem 与题面实际所需事件。；平方根上界并不需要控制 Γ⁺(ℤ_{2n},S) 的全部顶点；只需控制其在 V_n 像上的诱导子图。更精确地，在 p≈√(log n/n) 时，只需证明随机 B_p⊆I_n 满足 α(G_{B_p})=O(p^{-1}log n)。该命题严格弱于全循环群猜想，并会给出与本轮下界匹配的 Θ(√(n log n))。
- **整数小倍增集合计数路线**（blocked）：尝试用 Green–Morris 的整数集合计数直接对所有候选 C 作加权并合。；固定倍增 K 的部分可处理，但目标 k≈p^{-1}log n 为多项式量级；覆盖大和集区域所需的 Proposition 5.1 明确只在 k≤100log N 下陈述。对中间倍增范围直接并合还会产生 exp(k log K) 损失，无法由 exp(−p|C ̂+ C|) 支付。
- **两种小规模精确求解**（advanced）：一法把 α≤a 写成击中所有 (a+1)-元 restricted sumsets 的 0–1 MILP；另一法枚举 B 并用补图最大团独立求 α。；两法对 n=3,…,15 完全一致；本轮新增 f(13)=7、f(14)=8、f(15)=8。MILP 给出的 B 又由最大团算法反查独立数。

#### 第二轮新增严格进展

- [第二轮新增] 对所有充分大的 n，存在绝对常数 c>0 使 f(n)≥c√(n log n)。这严格加强第一轮的 Ω(√n) 下界，但仍与 n^{1/2+o(1)} 上界猜想相容。
- [第二轮新增] 证明和图的结构引理 T(G_B)≤binom(|B|,3)：三角形的三个不同和标签唯一恢复其三个顶点。
- [第二轮新增] 在关键范围 √(N/log N)<|B|<√(N log N) 中严格得到 α(G_B)≫N log N/|B|；两侧分别由贪心界和 |B| 本身闭合。
- [第二轮新增] 对随机区间和图证明不可避免的下界 α(G_{B_p})=Ω(p^{-1}log(np))（whp，p≤1/2、np→∞）。因此下一随机定理中的对数因子在量级上不能完全删除。
- [第二轮复核加固] 第一轮 next theorem 可严格弱化到 V_n 上的诱导子图；无需控制整个 ℤ_{2n}。在 p=√(log n/n) 处证明 α=O(p^{-1}log n) 将直接给出 f(n)=Θ(√(n log n))。
- [第二轮新增] 两种独立精确实现得到 f(13)=7、f(14)=8、f(15)=8；这扩展了第一轮只到 n=12 的表。

#### 证伪与边界检查

- 检查三角形标签确实两两不同：若 x+y=x+z，则 y=z，与三角形三个顶点不同矛盾；因此不存在标签重合造成的计数漏洞。
- 检查三角形三元标签的恢复公式不依赖标签在三条边上的排序；任意无序三元组至多恢复同一个无序顶点三元组。奇偶性不合或顶点不在 V_n 时只会使其不产生三角形。
- 随机稀疏化中分别控制顶点、边和三角形：Chernoff 给 X≥qN/2；Markov 给 Y≤2q²Nm 和 Z≤qN/8，三个事件失败概率之和小于 1，故确有共同实现。
- 删除至多 Z 个顶点即可击中所有残余三角形；删除后得到的是 G_B 的诱导子图，所以其中独立集仍是原图独立集。
- Shearer 输入是删三角形后图的实际平均度。若实际平均度远低于其 O(qm) 上界，则改用 Caro–Wei；两种情况均给 Ω(h log D/D)，避免把平均度上界错误代入非单调公式。
- 随机空区间反例只说明 α不可能为 O(p^{-1})；其 Ω(p^{-1}log(np)) 仍属于 p^{-1}n^{o(1)}，故没有错误地宣称反驳 Alon–Pham 的多对数猜想。
- 精确计算忽略从未由两个不同 V_n 顶点表示的和是安全的：从 B 删除这些元素不改变 G_B 且只减小 |B|。
- 直接枚举按 |B|+ceil((n−1)/(|B|+1)) 剪枝；这是由 Δ≤|B| 导出的整层安全下界。n≤15 的结果又与 hitting-set MILP 独立一致。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788/verify_round2_788.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788/verify_round2_788.py)：包含两个独立精确求解器：restricted-sumset 击中集 MILP，以及 B 枚举加 NetworkX 补图最大团；并检查三角形标签注入。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788 && python3 verify_round2_788.py --min-n 3 --max-n 15 --direct-max-n 15 --output round2_exact_788.json；结果：两法对 n=3,…,15 一致，得到 2,3,3,4,4,5,5,6,6,7,7,8,8。脚本 SHA256 为 99637ce85daf7b08dee1afd3df5933a174521f4f046a30af89c45113c172e59a。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788/round2_exact_788.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788/round2_exact_788.json)：逐 n 保存每个 α 约束的最小击中数、实际独立数、两实现的极值和三角形检查结果。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/788 && sha256sum round2_exact_788.json；结果：SHA256 为 ca5f1523e8e2350c4fef2f06662a87c535a395daed178068a05d8854e0a2d258；另一次写入 /tmp 的独立重算逐项匹配 n=3,…,14。

#### 当前障碍

新的下界已把合理目标提高到 √(n log n)，但现有上界仍停在 n^{3/5+o(1)}。最窄实质阻塞是：在 p=√(log n/n) 时，证明题目区间随机和图 G_{B_p} 的独立数为 O(p^{-1}log n)。Alon–Pham Theorem 4 只给 p^{-3/2} 乘多对数；Green–Morris 的大和集计数范围又不覆盖 k≈p^{-1}log n。

#### 下一精确定理

证明以下局部随机 Hankel 图定理：令每个 b∈I_n 独立以概率 p=√(log n/n) 加入 B_p，则以高概率 α(G_{B_p})≤C p^{-1}log n=C√(n log n)。Chernoff 同时给 |B_p|=O(pn)=O(√(n log n))，故该定理结合本轮下界立即推出 f(n)=Θ(√(n log n))，从而肯定原 n^{1/2+o(1)} 问题。空和区间构造表明这一独立数量级至多只能改常数。

#### 第二轮证明记录

承接的第一轮事实

设 N=|V_n|=n−1。固定 B⊆I_n 后，最大许可集合 C 正是 G_B 的最大独立集，故
\[
f(n)=\min_{B\subseteq I_n}\bigl(|B|+\alpha(G_B)\bigr).
\]
第一轮已经独立复核 Δ(G_B)≤|B| 以及
\[
\alpha(G_B)\ge \frac{N}{|B|+1}.
\]
上界方面，Alon–Pham Theorem 4 经模 2n 转移给出
\[
f(n)=O\!\left(n^{3/5}(\log n)^{19/10}\right).
\]
这些不计作第二轮新增。

第二轮新增推导

写 m=|B|、G=G_B。首先，G 的边由其和标签 b=x+y∈B 着色，每个固定 b 的边形成匹配。因此 e(G)≤Nm/2。更关键的是三角形很少：若 {x,y,z} 是三角形，令
\[
a=x+y,\qquad b=x+z,\qquad c=y+z.
\]
三者两两不同，而且
\[
x=\frac{a+b-c}{2},\qquad y=\frac{a+c-b}{2},\qquad z=\frac{b+c-a}{2}.
\]
所以一个无序标签三元组至多产生一个三角形，得到
\[
T(G)\le {m\choose3}\le \frac{m^3}{6}. \tag{1}
\]

现证明新下界。若
\[
m\ge \sqrt{N\log N},
\]
则 |B| 本身已足够大。若
\[
m\le \sqrt{N/\log N},
\]
则贪心界给
\[
\alpha(G)\ge\frac{N}{m+1}\gg\sqrt{N\log N}.
\]
只需处理中央区间
\[
\sqrt{N/\log N}<m<\sqrt{N\log N}. \tag{2}
\]
取
\[
q=\frac1{100}\sqrt{\frac{N}{m^3}}
\]
并以概率 q 独立保留每个顶点。记保留的顶点、边、三角形数分别为 X,Y,Z。由 (1)，
\[
\mathbb E X=qN,
\quad \mathbb E Y=q^2e(G)\le\frac12q^2Nm,
\quad \mathbb E Z=q^3T(G)\le\frac{qN}{60000}.
\]
在 (2) 中 qN→∞。Chernoff 与 Markov 不等式说明，以正概率同时有
\[
X\ge\frac{qN}{2},\qquad
Y\le2q^2Nm,
\qquad Z\le\frac{qN}{8}.
\]
从每个残余三角形删除一个顶点，至多删除 Z 个顶点，得到无三角形图 H，且
\[
|V(H)|\ge\frac{3qN}{8},
\qquad
\bar d(H)\le\frac{32}{3}qm=:D.
\]
Shearer 的公式与 Caro–Wei 结合给出：对充分大的 D，任何无三角形 h 点图、平均度不超过 D，均满足
\[
\alpha(H)\gg h\frac{\log D}{D}.
\]
具体地，实际平均度至少 √D 时直接用 Shearer；低于 √D 时 Caro–Wei 给 h/(√D+1)，这更强。因此
\[
\alpha(G)\ge\alpha(H)
\gg \frac{qN\log(qm)}{qm}
=\frac{N}{m}\log(qm). \tag{3}
\]
而 (2) 给
\[
qm=\frac1{100}\sqrt{\frac Nm},
\qquad \log(qm)=\Theta(\log N).
\]
由 (3)，
\[
\alpha(G)\gg\frac{N\log N}{m}
\gg\sqrt{N\log N}.
\]
三个 m 范围合并，得到待独立审稿的新结论
\[
\boxed{f(n)=\Omega(\sqrt{n\log n})}. \tag{4}
\]

第二个新增结论是随机路线的必要对数。令 B_p 为 I_n 的 p-随机子集，其中 p≤1/2、np→∞，并取
\[
k=\left\lfloor\frac{\log(np)}{16p}\right\rfloor.
\]
可在 V_n 的中央区域选取 M=Θ(n/k) 个长度 k 的整数区间 C_j，使 J_j=C_j\,\hat+\,C_j 是两两不交、长度 2k−3 的和区间。事件 J_j∩B_p=∅ 独立，且
\[
\Pr(J_j\cap B_p=\varnothing)
=(1-p)^{2k-3}
\ge e^{-4pk}
\ge (np)^{-1/4}.
\]
于是空区间的期望数至少
\[
M(np)^{-1/4}
\asymp\frac{(np)^{3/4}}{\log(np)}\to\infty,
\]
独立性进一步给出以高概率至少出现一个。相应 C_j 是独立集，所以
\[
\alpha(G_{B_p})=\Omega\!\left(p^{-1}\log(np)\right) \quad\text{whp}. \tag{5}
\]
因此 p^{-1} 纯量级不可能，但 p^{-1}log n 正是合理目标。

仍未闭合的缺口

要把 (4) 匹配成渐近阶，足够证明 p=√(log n/n) 时
\[
\alpha(G_{B_p})=O(p^{-1}\log n)=O(\sqrt{n\log n})
\]
以高概率成立。此命题只涉及 V_n 上的诱导和图，严格弱于控制整个循环群。现有 Alon–Pham 输入仍为 p^{-3/2} 多对数；Green–Morris 的大和集计数又限制在对数级 k，均未闭合这里的多项式稀疏范围。公式 (5) 表明拟议下一定理若成立，在量级上已是最优的。

来源成熟度与潜在优先权

Shearer 定理和 Baltz–Schoen–Srivastav 上界是已发表期刊结果；Alon–Pham 当前核对的是作者预印本/arXiv 版本。新下界 (4) 是本轮从已发表 Shearer 定理和新的三角形注入观察推出的纸面论证，尚未经过外部同行审稿或机器形式化。针对 #788、Choi 原文及 strongly sum-free 文献的定向检索没有找到明确陈述 Ω(√(n log n)) 的一手来源，但检索不到不等于不存在，故不主张文献优先权。

#### 本轮核查来源

- [Shearer, A note on the independence number of triangle-free graphs](https://doi.org/10.1016/0012-365X(83)90273-X)；一手来源：true；核验：论文明确证明：平均度为 d 的无三角形 N 点图满足 α≥N(d ln d−d+1)/(d−1)^2，渐近为 (1+o(1))N log d/d。本轮只调用这一已发表公式。
- [Alon–Pham, Random Cayley graphs and random sumsets（作者版本 randomss5）](https://web.math.princeton.edu/~nalon/PDFS/randomss5.pdf)；一手来源：true；核验：Theorem 4 对任意有限阿贝尔群及 p≤1/2 给随机 Cayley 与 Cayley-sum 图 α≤Õ(p^{-3/2})；第3.1节的显式选择为 p^{-3/2}(log N)^{19/4}。Conjecture 2 仍是 Õ(p^{-1})。
- [Green–Morris, Counting sets with small sumset and applications](https://arxiv.org/abs/1305.3079)；一手来源：true；核验：Theorem 1.1 计数固定小倍增常数的集合；Proposition 5.1 的大和集计数明确限制 k≤100 log N。目标稀疏度下所需 k≈p^{-1}log N 为多项式量级，故不能直接套用。
- [Baltz–Schoen–Srivastav, Probabilistic construction of small strongly sum-free sets via large Sidon sets](https://matwbn.icm.edu.pl/ksiazki/cm/cm86/cm8623.pdf)；一手来源：true；核验：Theorem 2 的精确范围是 f(n)=O(n^{2/3}log^{2/3}n)；没有给出本轮的少三角形下界。
- [Erdős Problems #788](https://www.erdosproblems.com/788)；一手来源：true；核验：页面最后编辑于 2026-01-26，仍标 OPEN；记录的下界仅为 ≫√n，上界为 n^{3/5+o(1)}，并把平方根上界联系到随机 Cayley 独立数猜想。

### #827

- 第一轮障碍：题目仍远未“确定”：现有近二次下界与 O(k^5/log k) 上界之间有巨大指数缺口。通用的 2-good 三一致超图着色理论已给出 k^5/log k；继续推进必须利用“颜色来自欧氏外接半径”这一额外几何结构。低层冲突又能在线性规模的双曲线/高次代数曲线上集中，因此简单最大共度、局部引理或逐层取独立集均不能直接改善。
- 第一轮下一定理：一个精确且严格强于已知结果的下一定理是：存在 ε,c>0，使每个 N 点原始一般位置集都含至少 cN^{1/5}(log N)^{1/5+ε} 个点，其所有三元组外接半径互异。证明它等价于把 n_k 上界中的 log k 至少再提高固定正幂；可行切入口应是“富等半径代数曲线/稀疏剩余”二分，而非错误的统一常数共度假设。
- 第二轮用时：1268.7 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：精确化第一轮抛物面—Sidon 下界的次主项，并检验能否从六点冲突层的局部共度或随机删点中把已知 O(k^5/log k) 的对数再提高。
- 第二轮结论：route_advanced；完整解声明：none；置信度：medium

- 独立复核：PASS；范围：第二轮抛物面差集精确求和、m/r 参数优化及常数 24√ln2、generic 秩2投影坏簇、固定四点的 H6 线性共度构造；原题阶数与上界改进仍开放。
- 复核方式：独立逐式重算差集求和与渐近展开；用第二套小盒枚举和符号代数检查常数；重跑原 Fraction 证书；另按仿射秩2/3分别验证投影共圆多项式非恒零，并审计任意 q 的有限避让归纳。
- 证据边界：PASS 只覆盖报告声明的第二轮部分结果。正式投稿时应把 generic 投影的仿射秩2/3非恒零引理和 H6 构造中‘先选半径、再选 X、最后选 Y’的有限避让顺序写全；28点程序本身不能替代任意 q 的归纳证明。常数公式按自然对数解释。新下界与线性四共度屏障仍是未发表、未形式化结果，不改善 O(k^5/log k) 上界，也未确定 n_k 的阶。

#### 第二轮实际尝试

- **抛物面差集的精确求和**（advanced）：不再用统一最大范围估计；按基底差 u=b−a 逐项计算最后一个二次坐标的可能值数。；令 X={Φ(a)=(a,||a||²):a∈{0,…,r−1}^m}。固定 u∈{−r+1,…,r−1}^m，最后坐标差为 2a·u+||u||²，可能值数至多 1+2Σ_i|u_i|(r−|u_i|−1)。因 Σ_{t=−r+1}^{r−1}|t|(r−|t|−1)=r(r−1)(r−2)/3，故 |X−X|≤(2r−1)^m+[2m r(r−1)(r−2)/3](2r−1)^{m−1}≤[(m+3)/3]2^m r^{m+2}。
- **显式优化近二次下界**（advanced）：令 m 为最接近 2√(log k/log 2) 的整数，并取满足 [(m+3)/3]2^m r^{m+2}<k(k−1) 的最大整数 r。；generic 秩2线性投影可同时保持单射、无三共线、无四共圆。rainbow k 集中的非零有序差必须互异，否则四个互异点投影成平行四边形，其对角线两侧三角形全等。于是 k(k−1)≤|X−X|−1。对上述 m,r 展开 m log r，得到 n_k≥(24√(log 2)+o(1)) k²(log k)^{−1/2} exp(−4√((log 2)(log k)))。这把第一轮指数中的 −O(log log k) 精确到显式对数幂和主常数。
- **六点层四共度为常数的设想**（refuted）：固定两条等长弦 AB、CD；对一列互异半径 ρ_i，分别在过 AB、CD 的半径 ρ_i 圆上选择 X_i、Y_i。；可归纳避开有限条已有直线和圆，使全部点始终一般位置，而 R(ABX_i)=R(CDY_i)=ρ_i。故六点冲突超图中固定四点 {A,B,C,D} 至少有 q 条边 {A,B,C,D,X_i,Y_i}，在 n=4+2q 时 Δ_4≥q=(n−4)/2。随附有理样本在 n=28 时精确得到该固定四点共度12。
- **在朴素删点中直接加入额外 log**（refuted）：把保留率改为 p=n^{−4/5}(log n)^γ，并仍按每个六点冲突删除一点。；仅使用 M_6=O(n^5) 时，保留顶点项为 n^{1/5}(log n)^γ，而六点冲突项为 O(n^{1/5}(log n)^{6γ})。任何 γ>0 都使标准的一阶期望下界失效；因此已知 log 增益必须来自 uncrowded/独立集结构，不能由同一逐边删点式得到。这里没有声称排除所有依赖随机算法。
- **移植 2024 年改进 Behrend 常数**（refuted）：尝试用更大的三项等差数列自由集代替球面或抛物面 cap。；三项等差自由只排除参数 {0,1,2} 型中点；一条实直线上的参数 {0,1,3} 已给三个共线点却没有三项等差。线性投影无法消除原有共线性。若再加严格凸二次坐标，便恢复原来的 r² 差集损失，同时还丢掉该自由集的密度，不能改善本轮界。
- **上界对数的文献边界**（blocked）：把六点冲突层的五共度定理与完整三层冲突超图、以及抽象 sunflower anti-Ramsey 锐性逐一比较。；六点层确有 Δ_5≤20，故单层可取 Ω((n log n)^{1/5}) 独立集；但新构造表明其 Δ_4 可线性，且所得集合仍可能含四点、五点冲突。LRW 的抽象量级又表明仅靠 λ=O(1) 的 sunflower 条件不会再产生固定正幂的额外 log。未找到利用等半径代数曲线结构突破这一点的现成定理。

#### 第二轮新增严格进展

- [第二轮新增] 对充分大 k，n_k≥(24√(log 2)+o(1))·k²/√(log k)·exp(−4√((log 2)(log k)))。它强化第一轮同一构造的次主项，但仍不确定 n_k 的阶。
- [第二轮新增] 六点冲突层的固定四点共度可以达到 (n−4)/2；所以把 Δ_5≤20 误推广成全部 proper codegree 为常数是严格错误的。
- [第二轮复核加固] 精确差集式在 (m,r)=(2,3),(2,4),(3,3) 的全枚举中分别给实际大小45、141、275，均不超过逐 u 求和界65、273、425。
- [第二轮复核加固] O(k^5/log k) 仍由 2015 年单版预印本给出；1996 年已发表抽象定理说明若要把 log 再提高，必须使用不包含在 bounded-sunflower 假设中的几何输入。

#### 证伪与边界检查

- 若两个不同有序差相等且两对共享一个端点，则会出现三点共线或两对相同；因此在 X 无三共线时，产生平行四边形的四点确实互异。
- 平行四边形对角线两侧的两个三角形由三边分别为 |v|、|w|、|v+w|，故严格全等；不依赖原高维度量，也不依赖投影为等距映射。
- 对有限 X，投影碰撞、任一三点共线、任一四点共圆分别是秩2线性映射参数中的真多项式零条件；有限并可避开。
- 安全差集界逐步使用 (2r−1)^m≤(2r)^m 和 r(r−1)(r−2)≤r³，没有把渐近等号当成有限不等式。
- 取整损失为 o(1)：所选连续 r 指数增长，而 m=O(√log k)，故最大安全整数 r 与连续解之比趋于1。
- 展开 2log k−m log r 的精确式得到常数 log(24√log2)；k=10^1000 的整数优化给归一化对数2.992800，预测极限为2.994797。
- 28点有理证书用 Fraction 同时检查全部三元组与四元组，没有浮点共线、共圆判等。
- 2024 年进展只禁中点关系；报告没有把三项等差自由误写为实仿射 cap。
- 本轮没有证明上界更好，也没有把新下界称为完整解。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/827/round2_checks.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/827/round2_checks.py)：Fraction 精确构造固定四点线性 H6 共度证书；枚举小抛物面差集；用大整数验证安全差集不等式并检查渐近常数。SHA-256: e7520ffebf130eee6a6865a9d60740eaf1cf41dde36e983dc503e7e808e5e30a。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/827 && python3 -m py_compile round2_checks.py && python3 round2_checks.py --pairs 12 --digits 50 100 500 1000；结果：得到28点一般位置有理集、固定四点六冲突共度12；三个小差集枚举全部通过；k=10^1000 时归一化对数常数2.992800，接近理论极限2.994797，且精确安全上界严格小于 k(k−1)。

#### 当前障碍

下界仍只是 k^{2−o(1)}，而最佳已核对上界为 O(k^5/log k)。差集法若要改善 exp(−4√((log2)(log k))) 的主常数，需要构造比二次严格凸图更高密度、同时保持无三共线且差集更小的 torsion-free cap；现有改进三项等差自由集不够。上界若要增加 log 幂，则必须利用等半径圆族的额外几何结构，同时处理 H4、H5、H6，单层五共度定理与朴素删点均不足。

#### 下一精确定理

两个可量化的下一节点是任取其一：（A）存在 η>0，使 n_k≥k² exp(−(4√(log2)−η)√(log k))；这要求改进当前小差集 cap 的主指数常数。（B）存在 ε>0，使 n_k=O(k^5/(log k)^{1+ε})；这要求证明外接半径冲突超图严格强于一般 bounded-sunflower 着色。

#### 第二轮证明记录

一、精确差集计数

令 A={0,…,r−1}^m，Φ(a)=(a,||a||²)，X=Φ(A)。严格凸性说明 X 无三共线。对 u=b−a，
Φ(b)−Φ(a)=(u,2a·u+||u||²)。
固定 u_i=t 时，a_i 有 r−|t| 个连续整数选择，2a_i t 的范围长度为 2|t|(r−|t|−1)。所以固定 u 的最后坐标值数至多
1+2Σ_i|u_i|(r−|u_i|−1)。
记 q=2r−1，并用
Σ_{t=−r+1}^{r−1}|t|(r−|t|−1)=r(r−1)(r−2)/3，
对全部 u 求和得到
|X−X|≤q^m+[2m r(r−1)(r−2)/3]q^{m−1}
≤2^m r^m+(m/3)2^m r^{m+2}
≤[(m+3)/3]2^m r^{m+2}.

二、投影与 rainbow-Sidon 约束

对有限 X 可选 generic 秩2线性映射 π，使其在 X 上单射，且 P=π(X) 无三共线、无四共圆。每个坏事件都是投影参数空间中的真多项式零集。若 X 中两个不同有序对满足 y−x=y'−x'≠0，则无三共线保证 x,y,x',y' 四点互异。投影后它们形成平行四边形。取其一条对角线，两侧三角形的三边同为 |v|、|w|、|v+w|，所以全等并有相同外接半径。因此 P 的 rainbow 子集 S 必须满足所有非零有序差互异，
|S|(|S|−1)≤|X−X|−1。

三、参数优化

令 K=k(k−1)，取
m=round(2√(log k/log2))
以及满足
[(m+3)/3]2^m r^{m+2}<K
的最大整数 r。于是 P 有 r^m 个点，却没有 rainbow k 集，故 n_k>r^m。连续解 R=[3K/((m+3)2^m)]^{1/(m+2)} 趋于无穷且 m/R→0，所以 r/R→1。写 L=log k、a=log2，则
log(r^m)=m/(m+2)[2L−ma−log(m+3)+log3]+o(1)。
当 m=2√(L/a)+O(1) 时，
2L−log(r^m)=4√(aL)−4a+log(m/3)+o(1)
=4√(aL)+(1/2)log L−log(24√a)+o(1)。
因此
n_k≥(24√(log2)+o(1)) k²(log k)^{−1/2}exp(−4√((log2)(log k))).

四、局部共度反例

固定两条长度相同、相对位置一般的弦 AB、CD。对任意 q，依次选互异且足够大的 ρ_i。过每条弦存在两个半径 ρ_i 的圆；在相应圆上选 X_i、Y_i，使 R(ABX_i)=R(CDY_i)=ρ_i。每一步只需避开由已有点产生的有限条直线、圆及有限个交点；也可先避开会使候选圆等于已有三点圆的有限多个半径，所以归纳可保持一般位置。六点冲突层因而含 q 条经过固定四点 ABCD 的边，证明 Δ_4≥q=(n−4)/2。随附脚本给出完全有理的 q=12 证书。

五、为什么尚未改进上界

六点层固定五点的延拓仍至多常数，因此已发表独立集定理可单独给该层 Ω((n log n)^{1/5}) 的独立集；但四共度线性反例说明不能把它误当成所有 proper codegree 常数，而且单层独立集仍可能含 H4、H5。若仅在 M6=O(n^5) 上用 p=n^{−4/5}(log n)^γ 后逐边删除，冲突期望的 log 指数为6γ，严格压过顶点项的γ。抽象 LRW 量级又说明 bounded-sunflower 条件本身没有额外固定正幂 log 可取。故本轮只强化了下界，未突破 O(k^5/log k)。

六、来源成熟度

显式次主项与线性四共度构造未在检索到的一手来源中找到，属于本轮推导，虽有精确程序交叉检查仍待外部同行评审，不主张文献优先权。2015 年 O(k^5/log k) 仍是预印本层级；1996 与 2014 年所用抽象独立集结果已有正式发表。

#### 本轮核查来源

- [Erdős Problem #827](https://www.erdosproblems.com/827)；一手来源：true；核验：截至本轮仍标 OPEN；页面记录 O(k^9) 与评论中的 O(k^5)，但没有收录 2015 年预印本的 O(k^5/log k)。
- [Points defining triangles with distinct circumradii](https://doi.org/10.1007/s10474-014-0443-z)；一手来源：true；核验：已发表论文确认原题的一般位置为无三共线、无四共圆，并解释 Erdős 旧论证遗漏的等半径冲突类型。
- [A sunflower anti-Ramsey theorem and its applications](https://arxiv.org/abs/1505.05170v1)；一手来源：true；核验：Theorem 1 与 Corollary 1(1) 在 d=2、h=2、λ=2 时给 n_k=O(k^5/log k)；该稿仍只有 v1，关键有限定理只给证明框架。
- [Multicolored Subsets in Colored Hypergraphs](https://doi.org/10.1006/jcta.1996.0049)；一手来源：true；核验：已发表的抽象反 Ramsey 定理给 (log N)^{1/(2k-1)} 型 rainbow 下界，并说明在仅使用相交同色边限制的抽象着色类中量级可达；因此额外对数必须利用外接半径的几何结构。
- [On independent sets in hypergraphs](https://doi.org/10.1002/rsa.20453)；一手来源：true；核验：已发表定理对六一致超图在五共度 d 有界时给 Ω((N log N/d)^{1/5}) 独立集；它可单独处理六点冲突层，却不会自动排除四点、五点冲突层。
- [Improving Behrend's construction: Sets without arithmetic progressions in integers and over finite fields](https://arxiv.org/abs/2406.12290v1)；一手来源：true；核验：Theorem 1.1 改善的是三项等差数列自由集的 Behrend 常数；其定义只禁 x+z=2y，不禁任意比例的三个共线点，故不能直接替换本题下界中的无三共线高维集合。

### #934

- 第一轮障碍：初始路线的目标命题本身为假，不能继续尝试闭合其 BFS 交叠估计。新的上界问题必须允许由密集 $C_7$ 结构产生的常数级超额；当前一般上界仍为 $h_3(\Delta)\le\tfrac32\Delta^3+1$，与新下界常数 $253/225$ 之间有实质差距。
- 第一轮下一定理：新的精确目标是 2026 预印本 Problem 1.12：证明或反驳“对充分大的 $\Delta$，$h_3(\Delta)\le\frac{253}{225}\Delta^3$”。一个更窄、可先攻击的种子定理是：若 $H$ 为 $r$-正则且 $\operatorname{diam}L(H)\le3$，是否总有 $|E(H)|\le\frac{253}{225}r^3$？它若成立，只能封住现有射影极性放大机制，尚不足以证明完整上界。
- 第二轮用时：1489.6 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：先证伪正则种子上界：检查自然 Odd graph 延伸、命名距离正则图及低度循环 Cayley 图。幸存后提取固定边的严格局部约束，并定位从局部约束到 253/225 常数所缺的结构输入。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核第二轮结果中的固定边远集独立引理及其正则边数界、Odd graph O_5 的显式失败证书、度 4/5 循环 Cayley 图的充要判据与完整枚举，以及选定 Sage 命名图样本的双实现计算；不认证任意正则图上界、任意度循环图上界或 Problem 1.12/#934 的完整解。
- 复核方式：不把结果文件结论作为前提，逐式重推局部计数与 O_5 证书；从群差重新证明循环 Cayley 判据，独立计算 n 窗口和组合数；逐行审计两份源码，在隔离副本重跑 group、direct 与 Sage；同时核对两篇一手论文的 TeX 源和 #934 状态页。
- 证据边界：PASS 不表示 #934 已闭合。当前最强新增理论界仍弱于已知 3/2 首项，7046 个循环连接集和 25 个命名图都是严格但有限的排除证据；253/225 的新下界及 Problem 1.12 来自 2026-07-02 的 arXiv v1，尚未同行评审。

#### 第二轮实际尝试

- **固定边的远集约束**（advanced）：固定边 uv，令 S=B_{≤2}(u)∪B_{≤2}(v)，T=V(H)\S，并利用线图直径条件和正则性计数割边。；若 xy∈E(H[T])，则 uv 与 xy 的任意端点距离至少3，故它们在线图中距离至少4，矛盾，所以 T 独立。若 H 为 r-正则，c=|N(u)∩N(v)|，则 |S|≤2(r^2+1)-(2r-c)=2r^2-2r+c+2。又 r|T|=e(S,T)=r|S|-2e(S)，而 S 至少包含所有关联于 u 或 v 的 2r-1 条边，故 |V(H)|≤4r^2-4r+2c+2/r，进而 |E(H)|≤2r^3-2r^2+rc+1≤2r^3-r^2-r+1。
- **Odd graph 延伸的主动证伪**（refuted）：检查 O_5=KG(9,4)，寻找线图距离超过3的边对。；取 AB=({1,2,3,4},{5,6,7,8})，CD=({4,6,7,9},{2,3,5,8})。四个交叉端点交集大小依次为1,2,2,2。KG(9,4) 中两顶点相邻要求不交，而具有共同邻点要求交集至少3；故四对端点距离均至少3，从而 d_{L(O_5)}(AB,CD)≥4。
- **命名距离正则种子压力测试**（inconclusive）：使用 Sage 构造选定的命名或参数化距离正则图；一份实现直接计算二阶闭邻域外诱导边，另一份实现调用 Sage 全点对最短路。；成功精确检查25个候选，两种实现逐图一致。共有8图满足 diam L(H)≤3；截断 Witt 图的 |E|/r^3=253/225 居首，O_4 为35/32，其余更低。O_5、双截断 Witt 图、Large Witt 图等均失败。该样本不是全部正则图。
- **低度循环 Cayley 图的精确穷尽**（advanced）：对 H=Cay(Z_n,S)，分别以群差集判据和逐图 BFS 实现穷尽搜索。利用已知 |E(H)|≤(3/2)r^3，只搜索可能严格超过253/225的阶数窗口。；因为 |E|/r^3=n/(2r^2)，r=4 只需36≤n≤48；r=5 只需偶数58≤n≤74。群实现令 D_2={0}∪S∪(S+S)，逐一检查边型 (0,g),(x,x+h) 的四个端点差是否至少一个属于D_2；直接实现独立构图并计算二阶 BFS 球。共检查7046个连接集，两实现均得到 accepted=[]。

#### 第二轮新增严格进展

- [第二轮新增] 对任意简单 r-正则 H，若 diam L(H)≤3，则对每条边 uv，集合 V(H)\(B_{≤2}(u)∪B_{≤2}(v)) 必为独立集；若 c=|N(u)∩N(v)|，进一步有 |E(H)|≤2r^3-2r^2+rc+1≤2r^3-r^2-r+1。该界弱于已知 (3/2)r^3，但严格揭示仅使用单条固定边的“远集独立”约束仍停留在首项常数2。
- [第二轮新增] O_4 的成功不延伸至 O_5：给出了 O_5 中线图距离至少4的完全显式边对，严格否定把整个 Odd graph 族直接作为正则种子的路线。
- [第二轮新增] 机器辅助精确结论：不存在度4或5、密度 |E|/r^3>253/225 的循环 Cayley 种子图。搜索覆盖由一般3/2上界允许的全部阶数，共7046个连接集，并由群差集与直接BFS两种实现交叉确认。
- [第二轮复核加固] 在成功构造且规模不超过程序上限的25个命名距离正则候选中，截断 Witt 图恰以253/225居首；这加固了种子常数的有限证据，但不构成任意正则图上界。

#### 证伪与边界检查

- 重新核对阈值偏移：坏图有m条边只推出h_3(Δ)≥m+1；本轮没有把种子边数直接写成h_3的等式。
- 循环图程序以K_5和K_{4,4}作阳性自测，以C_8作阴性边界自测；两实现均通过这些测试。
- r=5 时握手引理要求n为偶数；程序虽报告形式下端n_min=57，实际只枚举58,60,…,74，没有遗漏可行阶数。
- 命名图筛查明确记录了规模上限和构造失败项；没有将数据库阴性结果表述成正则种子定理。
- 对O_5反例不依赖程序距离值：交集大小直接排除了相邻和共同邻点，因此四对端点的距离都严格大于2。
- 局部远集界逐项检查了三角形边界：|N[u]∪N[v]|=2r-c 且c≤r-1；未偷用无三角形或无C_7假设。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934/scan_circulant_seeds.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934/scan_circulant_seeds.py)：穷尽r=4,5的循环Cayley反例窗口；包含群差集和直接BFS两种独立判定以及阳性、阴性自测。SHA-256：c05c51d02dc9466080cac37b20c423dde8e1a4020efc09d8ace76389ea244c43。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934 && python3 scan_circulant_seeds.py --method group && python3 scan_circulant_seeds.py --method direct；结果：两次均报告tested=7046；r=4检查2552个连接集，r=5检查4494个；accepted=[]。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934/scan_named_seeds.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934/scan_named_seeds.py)：构造选定的Sage命名距离正则图，以手写二阶邻域位集和Sage最短路作双重判定。SHA-256：5a3b57c5f0dd00aa3cc8d2cc38e6427589599a469e1b47cab93ce9ae2b3a656f。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/934 && DOT_SAGE=/tmp/sage934 sage -c "exec(open('scan_named_seeds.py').read()); main()"；结果：成功精确检查25图；8图通过。前三名依次为截断Witt图253/225、O_4的35/32、O_3的5/9；没有严格超过253/225者。另有7个候选因预设规模上限跳过。

#### 当前障碍

固定边只能强迫远集独立，并给出首项常数2；CCJK Proposition 13 通过更细分层降到3/2，但其末层内部边估计仍允许大量由C_7型碰撞支撑的边。现无严格不等式能把这些碰撞压到253/225。更根本地，即使证明所有正则种子满足该常数，也只封住Lemma 3.4式射影放大，不能排除非正则坏图或不来自固定种子放大的渐近构造。

#### 下一精确定理

最窄的下一定理是：若H是有限简单循环图 Cay(Z_n,S)，度为r且diam L(H)≤3，则 |V(H)|≤(506/225)r^2；本轮已严格验证r=4,5。随后才可尝试同一命题对全部顶点传递图。二者都只是正则种子定理的子类，不能替代Problem 1.12。

#### 第二轮证明记录

承接的第一轮事实

坏图极值的精确定义是
\[h_3(\Delta)-1=\max\{|E(G)|:\Delta(G)\le\Delta,\ \operatorname{diam}L(G)\le3\}.\]
第一轮已严格反驳旧常数1路线，并从2026预印本得到截断Witt种子
\[(r,|E|)=(15,3795),\qquad \frac{|E|}{r^3}=\frac{253}{225}.\]
本轮没有重报这些为新结果，而是攻击辅助命题“所有r-正则种子的密度至多253/225”。需强调：文献的Problem 1.12问的是完整h_3(Δ)上界，量词显著更强。

第二轮新增推导

固定任意边uv，置
\[S=B_{\le2}(u)\cup B_{\le2}(v),\qquad T=V(H)\setminus S.\]
若T中存在边xy，则uv与xy的任意一对端点在H中距离至少3，故其线图距离至少4，与diam L(H)≤3矛盾。因此T独立。

设H为r-正则，c=|N(u)\cap N(v)|。每个二阶球至多有r^2+1个顶点，而
\[B_{\le2}(u)\cap B_{\le2}(v)\supseteq N[u]\cup N[v],\quad |N[u]\cup N[v]|=2r-c.\]
所以
\[|S|\le2r^2-2r+c+2.\]
由T独立，
\[r|T|=e(S,T)=r|S|-2e(S).\]
S包含所有关联于u或v的边，故e(S)≥2r-1。于是
\[|V(H)|=|S|+|T|\le2|S|-4+\frac2r
 \le4r^2-4r+2c+\frac2r,\]
并得到
\[|E(H)|\le2r^3-2r^2+rc+1\le2r^3-r^2-r+1.\]
这是严格局部引理，但首项仍为2，甚至弱于已知3/2；它准确显示单边BFS远集独立不足以接近253/225。

主动测试自然种子族时，O_5=KG(9,4)立即失败。两边
\[({1,2,3,4},{5,6,7,8}),\quad({4,6,7,9},{2,3,5,8})\]
的四个交叉端点交集均小于3且非空。KG(9,4)中共同邻点存在要求两个4集的并至多含5点，即交集至少3；故这些端点既不相邻也无共同邻点，线图距离至少4。

对循环Cayley图，令连接集为S_0。由平移对称性，只需比较边(0,g)与(x,x+h)。记
\[D_2=\{0\}\cup S_0\cup(S_0+S_0).\]
两边线图距离至多3当且仅当
\[\{x,x+h,x-g,x+h-g\}\cap D_2\ne\varnothing.\]
密度严格超过253/225等价于n>506r^2/225，而一般3/2上界给n≤3r^2。这使r=4,5的搜索成为有限且完整的7046个连接集。群差集实现与不使用平移简化的逐图BFS实现均无反例。

仍未闭合的缺口

上述计算只排除了低度循环图，命名距离正则图筛查也只是有限样本。它们不能证明任意正则种子上界。局部引理只利用T独立；要把3/2降至253/225，必须定量描述末层边、7圈碰撞和多条根边之间的兼容性。目前没有闭合这种全局稳定性估计。即便正则种子命题最终成立，完整Problem 1.12还必须把非正则坏图归约到近正则种子或另行控制，当前没有这种归约。

来源成熟度与优先权

CCJK结果已有2022年SIAM同行评审版本，可作为成熟的一手定理使用。253/225、截断Witt种子及Problem 1.12来自2026-07-02的arXiv v1，尚未同行评审；本轮独立重算了Sage所提供截断Witt图的参数和线图条件，但没有重建Steiner系统S(5,8,24)的完整生成证书。因此253/225应视为强一手预印本结果，不能表述成已审定的新最优定理。

#### 本轮核查来源

- [An improved bound for the strong clique index of graphs](https://arxiv.org/pdf/2607.02698)；一手来源：true；核验：2026-07-02 的 arXiv v1。Lemma 3.2 给出 15-正则、3795 边的截断 Witt 种子；Lemmas 3.3–3.4 给出射影平面放大；Theorem 1.11 证明 liminf h_3(Δ)/Δ^3≥253/225；Problem 1.12 精确询问充分大 Δ 时的反向上界。论文没有提出或证明正则种子上界。
- [Maximising line subgraphs of diameter at most t](https://arxiv.org/pdf/2103.11898)；一手来源：true；核验：Theorem 6 给出一般上界 h_t(Δ)≤(3/2)Δ^t+1；Theorem 10/Proposition 11 的改进要求无 C_{2t+1}；对 t=3 即无 C_7。Proposition 13 是一般 3/2 局部计数的核心，不能直接产生 253/225。
- [Maximizing Line Subgraphs of Diameter at Most t](https://epubs.siam.org/doi/10.1137/21M1437354)；一手来源：true；核验：SIAM J. Discrete Math. 36 (2022), 939–950 的期刊页面，确认上述论文已同行评审发表及其正式书目信息。

### #950

- 第一轮障碍：决定性缺口位于 \(d=n^{o(1)}\) 及更一般的 \(d<n^{0.52}\) 尺度。Brun–Titchmarsh 在每个乘法块只给密度约 \(2/\log D\)，跨尺度求和恰产生 \(2\log\log n\)；现有逐点短区间定理不能提供随 n 一致的额外节省。相同短尺度也是计算中大值的主要来源，因此既阻塞第三问，也阻塞 \(\limsup=\infty\)。
- 第一轮下一定理：优先证明以下精确的多尺度下界：对每个固定 \(\epsilon>0\)，\[\liminf_{n\to\infty}\sum_{n^\epsilon\le d\le n/2}\frac{\mathbf1_{\mathbb P}(n-d)}d\ge1-\epsilon.\]它与两矩给出的 \(\liminf f\le1\) 合并即可推出 \(\liminf f=1\)。相比逐个短区间的 PNT，这一命题只要求对数尺度加权后的总下界，因而是更清晰且可能更弱的下一定理。
- 第二轮用时：1100.8 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：先攻击第一轮的多尺度下一定理和短分母阻塞点；把全体整数问题约化到真正控制极值的素数子序列，再将同行评审的长分母下界与有界素数间隔叠加。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS_WITH_MINOR_REPAIRS；范围：独立重推第二轮结果中的精确递推、素数与合数步的局部极值、liminf/limsup 的素数子序列约化、第三问的峰值子序列等价、素数跳跃下界，以及 Guth–Maynard Corollary 1.3 与 Polymath 的 H_1≤246 叠加所得常数 10651/7410；同时从源码重跑两项计算资产并核对一手来源及成熟度。
- 复核方式：核心结论成立：递推和局部极值约化正确，f(p+1)-f(p)≥log 2 正确，Guth–Maynard 的逐点短区间定理可统一推出长分母质量 13/30-η，Polymath 的无条件 H_1≤246 可在同一子序列提供不交叠的 1+1/247，故 limsup f(n)≥10651/7410 无条件成立。发现一处证明正文中的错误等式：相关积分应为 (1/2)log(p/(p-1))，而不是 log(p/(p-1))；修正后仍足以吸收 q=2 项，故不改变跳跃下界。另需把 Polymath 的期刊定理编号从 Theorem 1.4(i) 改为 Theorem 4(i)。原题三问均未闭合，#950 仍开放。
- 证据边界：此 PASS_WITH_MINOR_REPAIRS 表示第二轮新增路线在修正错误积分等式和引文编号后可成立，不是对 #950 的完整解、论文同行评审或形式化证明认证。

#### 第二轮实际尝试

- **局部极值递推**（advanced）：逐项计算 \(f(n+1)-f(n)\)。；令 \[g(n)=\sum_{q<n}\frac1{(n-q)(n+1-q)}.\]则 \[f(n+1)-f(n)=\mathbf1_{\mathbb P}(n)-g(n).\]对 \(n\ge3\) 有 \(0<g(n)<\sum_{d\ge1}1/[d(d+1)]=1\)，而 \(g(2)=0\)。因此素数处严格上跳，合数 \(n>2\) 时严格下降。若 \(p_k<p_{k+1}\) 是相邻素数，则 \([p_k+1,p_{k+1}]\) 上最大值为 \(f(p_k+1)\)，最小值为 \(f(p_{k+1})\)。
- **素数跳跃的奇偶加固**（advanced）：利用两个奇素数之差必为偶数。；对素数 \(p\ge5\)，除 \(q=2\) 外的分母差 \(p-q\) 都是偶数。比较偶数全和并估计遗漏尾部，可得 \[g(p)\le\sum_{k\ge1}\frac1{2k(2k+1)}=1-\log2,\]因而 \[f(p+1)-f(p)\ge\log2.\]
- **长分母基线与有界素数间隔叠加**（advanced）：把 Guth–Maynard 的长尺度贡献与 Polymath 的两个短分母项作不交叠求和。；Guth–Maynard 给每个固定 \(\eta>0\) \[\liminf_{n\to\infty}\sum_{n^{17/30+\eta}\le d\le n/2}\frac{\mathbf1_{\mathbb P}(n-d)}d\ge\frac{13}{30}-\eta.\]取无穷多个相邻素数 \(q<p\)、\(p-q\le246\)，令 \(n=p+1\)。除上述长分母外，还有 \(p\) 给出的 \(1\) 和 \(q\) 给出的至少 \(1/247\)，故 \[\limsup f(n)\ge1+\frac1{247}+\frac{13}{30}=\frac{10651}{7410}.\]
- **第一轮多尺度下一定理的量词削弱**（blocked）：利用局部最小值只出现在素数处。；第一轮要求对所有整数中心、每个固定 \(\epsilon\) 控制截断和；本轮证明只需对素数中心满足：每个 \(\delta>0\) 存在某个 \(\eta>0\)，使截断和的下极限至少 \(1-\delta\)。这是严格较弱的充分命题，但现有逐点短区间定理仍只能供应其中长分母的 \(13/30\)。
- **第三问的峰值约化**（advanced）：在每个相邻素数区间利用单调性。；精确得到 \[f(n)=o(\log\log n)\ \text{对全部 }n \quad\Longleftrightarrow\quad f(p+1)=o(\log\log p)\ \text{沿素数 }p.\]反向蕴含来自 \(p_k<n\le p_{k+1}\) 时 \(f(n)\le f(p_k+1)\) 且 \(\log\log n\ge\log\log p_k\)。该约化没有为峰值短尺度给出新的上界。
- **扩大有限扫描并双实现复核**（inconclusive）：Python/NumPy FFT 扫描全部值；C++ 独立筛法和 long double 直接求和复核候选点。；扫描至 8000000。在区间 \([800000,8000000]\) 内最大点为 \(n=6561020\)、\(f(n)=2.6283618579354417\)，最小点仍为 \(n=1349651\)、\(f(n)=0.6500789377978458\)。全部递推符号符合严格局部极值引理。截断多尺度只作有限网格诊断。

#### 第二轮新增严格进展

- [第二轮新增] 精确证明 \[\liminf_{n\to\infty}f(n)=\liminf_{p\to\infty}f(p),\qquad \limsup_{n\to\infty}f(n)=\limsup_{p\to\infty}f(p+1),\]其中 \(p\) 遍历素数；并证明第三问等价于只检查峰值子序列 \(f(p+1)=o(\log\log p)\)。
- [第二轮新增] 对每个素数 \(p\ge5\) 严格有 \(f(p+1)-f(p)\ge\log2\)。这加固了局部极值约化，但尚不足以证明上极限无穷。
- [第二轮新增] 仅使用同行评审的 Guth–Maynard Corollary 1.3 和 Polymath 期刊版 Theorem 4(i)，严格得到 \[\limsup f(n)\ge\frac{10651}{7410}=1.4373819163\ldots.\]这严格强于第一轮的 \(248/247=1.004048\ldots\)。
- [第二轮新增] 若另接受尚未同行评审的 Li v8 Theorem 2 及其数值常数，则同一不交叠叠加给 \[\limsup f(n)\ge1+\frac1{247}+0.444299\overline3=1.4483479163\ldots.\]该加强不列为成熟无条件结论。
- [第二轮复核加固] 第一轮的“所有整数中心、每个 \(\epsilon\)”多尺度命题可严格削弱为只控制素数中心且允许截断指数依赖误差；但缺失质量仍恰位于 \(d<p^{17/30+o(1)}\)，所以削弱量词没有消除筛法障碍。

#### 证伪与边界检查

- 逐项检查递推端点：\(n=2,3\) 不影响极限；对合数 \(n>2\)，至少有素数 2 使 \(g(n)>0\)；对素数，有限子和严格小于望远镜全和 1。
- 奇偶加固中单独处理 \(q=2\)。令 \(m=(p-1)/2\)，有 \(\sum_{k=m}^\infty[2k(2k+1)]^{-1}\ge\int_m^\infty[2x(2x+1)]^{-1}dx=\tfrac12\log(p/(p-1))\ge1/(2p)\ge1/[(p-2)(p-1)]\)（\(p\ge5\)），足以吸收 \(q=2\) 项。
- 有界间隔项 \(d\le247\) 与 Guth–Maynard 使用的 \(d\ge n^{17/30+\eta}\) 最终不交叠，因此常数可以相加。
- 主动检索了声称 \(H_1\le234\) 的 2025 作者稿；由于其加权分布到普通 Maynard–Tao 假设的过渡和数值阈值均未闭合，未用它把 247 擅自替换为 235。
- 核对 Polymath 期刊版 Theorem 4（arXiv 版 Theorem 1.4）：\(H_2\le398130\)，排除了把排版数字误读成 398 后虚假加强的边界错误。
- 8000000 范围的 FFT 扫描中，全部合数步增量为负、全部素数步增量为正；候选点由独立 C++ 直接求和复核。
- 对 \(\epsilon=0.1\) 的 401 点网格，截断和样本最小值约 0.633，低于有限尺度目标 0.9；这表明收敛极慢，但固定有限反例不反驳渐近 liminf 命题。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/round2_scan.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/round2_scan.py)：独立第二轮实现：素数筛、FFT 卷积计算全部 \(f(n)\)、递推符号检查、直接 math.fsum 复核、截断多尺度网格采样。SHA256 为 32863655ac1e2d2edd2551e51f2958f9b937b4870f300ca88790df9ff70d72e5。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950 && python3 round2_scan.py --limit 8000000 --samples 401 --output round2_scan_8000000.json；结果：成功扫描到 8000000；区间最大候选 \(6561020\) 的直接值为 2.6283618579354417；递推符号零违例。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/verify_records.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/verify_records.cpp)：与 FFT 无关的独立 C++ 实现，使用 Eratosthenes 筛和 long double 补偿求和。SHA256 为 e12d5b9e725d90f30c845038542fa54dbc403b86d2b0ad7b66c5dfa3c0665578。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950 && g++ -O2 -std=c++17 verify_records.cpp -o verify_records && ./verify_records 855740 1349651 6561020；结果：依次得到 2.5592922936049984123、0.650078937797845703009、2.6283618579354416046，与 Python 直接求和在双精度舍入内一致。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/round2_scan_8000000.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950/round2_scan_8000000.json)：完整扫描结果、局部增量检查和五个截断指数的有限网格数据。SHA256 为 9b16bc56bedf7654b7ff9021da8f1191a2c64c8e055f3e896473cba2123a7416。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/950 && python3 -m json.tool round2_scan_8000000.json >/dev/null；结果：JSON 有效；明确标注网格极值不是全局或渐近证书。

#### 当前障碍

局部极值约化表明三个问题真正需要控制的是素数中心 \(f(p)\) 和峰值 \(f(p+1)\)。Guth–Maynard 只统一控制 \(d\ge n^{17/30+o(1)}\)，贡献 \(13/30\)；余下 \(d<n^{17/30+o(1)}\) 既能决定素数处的局部最小值，也能在峰值处跨尺度累积。Brun–Titchmarsh 在该区域仍只给 \(O(\log\log n)\)，有界素数簇则只增加固定常数，不能推出 \(\limsup=\infty\) 或小 \(o\)。

#### 下一精确定理

比第一轮目标严格更弱、且恰好足以闭合第一问的下一定理是：对每个 \(\delta>0\)，存在 \(\eta=\eta(\delta)>0\)，使得 \[\liminf_{\substack{p\to\infty\\p\ \mathrm{prime}}}\ \sum_{p^\eta\le d\le p/2}\frac{\mathbf1_{\mathbb P}(p-d)}d\ge1-\delta.\]它只要求素数中心，并允许截断指数依赖目标误差。结合本轮的局部最小值约化和两矩产生的趋于 1 子序列，即推出 \(\liminf f(n)=1\)。目前最窄的未覆盖部分仍是为素数中心补足长分母结果之外的 \(17/30\) 质量。

#### 第二轮证明记录

【承接的第一轮事实】写 \(a(m)=\mathbf1_{\mathbb P}(m)\)，则 \[f(n)=\sum_{1\le d\le n-2}\frac{a(n-d)}d.\]第一轮已审计的两矩给 \(f(n)\to1\) 依自然密度成立，从而存在 \(f(n_j)\to1\)；同行评审的 Guth–Maynard Corollary 1.3 经乘法分块给出 \[\liminf_n\sum_{n^{17/30+\eta}\le d\le n/2}\frac{a(n-d)}d\ge\frac{13}{30}-\eta.\]这里对目标指数 \(17/30+\eta\) 在 Corollary 1.3 中取 \(\epsilon<\eta\)，并把超过 \(x^{0.99}\) 的块再切分，保留参数留缝。这些只作为承接事实使用，没有重新包装成第二轮进展。

【第二轮新增推导】逐项使用 \(1/(d+1)-1/d=-1/[d(d+1)]\)，得到精确递推 \[f(n+1)-f(n)=\mathbf1_{\mathbb P}(n)-g(n),\qquad g(n)=\sum_{q<n}\frac1{(n-q)(n+1-q)}.\]由于 \(g(n)<\sum_{d\ge1}1/[d(d+1)]=1\)，素数步严格上升；合数 \(n>2\) 时 \(g(n)>0\)，故严格下降。若 \(p_k<p_{k+1}\) 相邻，则 \[\max_{p_k+1\le n\le p_{k+1}}f(n)=f(p_k+1),\qquad \min_{p_k+1\le n\le p_{k+1}}f(n)=f(p_{k+1}).\]于是三个全整数问题分别精确约化到 \(f(p)\)、\(f(p+1)\)。特别地，若峰值满足小 \(o\)，区间内任意 \(n\) 有 \[\frac{f(n)}{\log\log n}\le\frac{f(p_k+1)}{\log\log p_k},\]所以第三问与峰值子序列完全等价。

递推还能由奇偶性加固。对奇素数 \(p\)，除 \(q=2\) 外，\(p-q=2k\)。而 \[\sum_{k\ge1}\frac1{2k(2k+1)}=1-\log2.\]令 \(m=(p-1)/2\)。有限偶分母和遗漏的尾部至少为 \(\tfrac12\log(p/(p-1))\ge1/(2p)\ge1/[(p-2)(p-1)]\)，足以吸收 \(q=2\) 项；故 \(g(p)\le1-\log2\)，即 \(f(p+1)-f(p)\ge\log2\)。

上极限方面，取 Polymath 保证的无穷多个相邻素数 \(q<p\)、\(p-q\le246\)，并令 \(n=p+1\)。此时两个短分母贡献为 \[\frac1{n-p}+\frac1{n-q}=1+\frac1{p-q+1}\ge1+\frac1{247}.\]它们最终与 \(d\ge n^{17/30+\eta}\) 的 Guth–Maynard 部分不交叠，所以 \[\limsup f(n)\ge1+\frac1{247}+\frac{13}{30}=\frac{10651}{7410}.\]

第一轮多尺度目标可削弱为只在素数中心证明：对每个 \(\delta\) 可选择某个 \(\eta\)，使截断和至少为 \(1-\delta\)。这确实足够，因为所有局部最小值都在素数处；但它把问题送入 Erdős 原文已经指出更困难的 \(f(p)\) 范围，现有定理不能补足短尺度质量。

【仍未闭合的缺口】局部极值约化不提供新的短区间素数计数。对 \(f(p)\)，\(d<p^{17/30+o(1)}\) 的总质量未知，故不能把 \(13/30\) 推到 1。对峰值 \(f(p+1)\)，同一区域既阻塞无界性，也阻塞 \(o(\log\log p)\)。有限扫描中的高峰和低谷符合这一判断，但不是渐近证明或反例。

【来源成熟度与潜在优先权】无条件常数 \(10651/7410\) 只使用正式发表的 Guth–Maynard 与同行评审的 Polymath 结果。Li v8 的加强仍依赖未审稿预印本及 ancillary 数值代码。2025 年声称 \(H_1\le234\) 的作者稿存在未闭合的关键过渡，未采用。针对原题、递推公式及 reciprocal-distance 关键词检索后，没有找到一手来源明确记录本轮的局部极值约化或 \(10651/7410\) 叠加；这只能表述为“本轮未找到优先文献”，不能据此声称数学首创。

#### 本轮核查来源

- [P. Erdős, Problems in number theory and combinatorics, pp.62–63](https://www.renyi.hu/~p_erdos/1977-27.pdf)；一手来源：true；核验：第62–63页提出三项精确问题，并陈述两个矩渐近式。没有发现原文记载本轮的局部极值递推。
- [Erdős Problem #950](https://www.erdosproblems.com/950)；一手来源：false；核验：截至本轮检索仍标为 OPEN；题面、历史说明和输入材料一致。
- [L. Guth and J. Maynard, New large value estimates for Dirichlet polynomials, Corollary 1.3](https://annals.math.princeton.edu/2026/203-2/p06)；一手来源：true；核验：正式发表于 Annals of Mathematics 203 (2026)。Corollary 1.3 对 \(y\in[x^{17/30+\epsilon},x^{0.99}]\) 给逐点短区间素数渐近，足以推出所有中心 \(n\) 的长分母贡献下界 \(13/30\)。
- [D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, journal Theorem 4(i)](https://doi.org/10.1186/s40687-014-0012-7)；一手来源：true；核验：期刊版 Theorem 4(i)（arXiv 版 Theorem 1.4(i)）无条件证明 \(H_1\le246\)。同一定理的 \(H_2\) 显式界是 398130，而不是 398，故三素数簇并不改善本轮的小分母增益。
- [Runbo Li, The number of primes in short intervals and numerical calculations for Harman's sieve, v8, Theorem 2](https://arxiv.org/abs/2308.04458v8)；一手来源：true；核验：v8 于 2025-10-16 更新，仍是预印本；Theorem 2 及 ancillary 文件给第一轮采用的阶梯常数。本轮只把它用于明确标注的条件性加强。
- [Yuhang Shi, A Weighted Distribution of Primes and a New Unconditional Bound on Gaps Between Primes](https://www.researchgate.net/publication/393888742_A_Weighted_Distribution_of_Primes_and_a_New_Unconditional_Bound_on_Gaps_Between_Primes)；一手来源：true；核验：作者上传的未审稿稿件声称 \(H_1\le234\)，但其 Theorem 4.1 只控制特定稀疏权 \(\lambda_q\)，Corollary 5.1 却直接作为普通分布水平代入 Maynard–Tao；Appendix A 又以无显式常数的 \(O(\Delta\theta)\) 连续性跨越数值阈值。该稿不足以作为已证输入，本轮未采用 234。

### #963

- 第一轮障碍：当前最强幸存路线把底数3改善到渐近主项1，但每轮仍损失 O(log log N) 和常数；迭代只能控制总缺陷为 o(log N)，不能压到原猜想所需的常数0。秩3有限核分类也尚未显现可随 r 归纳的结构。渐近证明目前只见于论坛，尚无论文、预印本或形式化版本。
- 第一轮下一定理：优先目标是证明正整数版本 h(N)≥log₂N−O(1)，即把递推中的短区间密度损失从 c/(p log N) 改到 c/p，并控制取整误差；若能进一步把常数压到0，便得到原题。较小而明确的可审目标是把 F(3)=13 的有限核枚举转成可独立检查的证书或 Lean 形式化。
- 第二轮用时：1341.8 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：结果推进了幸存路线但没有解决原猜想：将渐近下界严格定量化为 f(n)≥log₂n−O((log log n)²)；证明最直接的“两模排回绕”改造必损失约 log₂k；并构造27元、耗散维数恰为4的集合，得到 F(4)≥27。
- 第二轮结论：route_advanced；完整解声明：none；置信度：medium

- 独立复核：PASS；范围：独立严格复核第二轮三项新进展：(i) 对充分大 n 的无条件下界 f(n) >= log_2 n - O((log log n)^2)；(ii) 循环间距障碍引理 2^|Gamma|(T+1) <= p 及其对最直接排回绕方案的否定；(iii) 13 元正集 P 的 d(P)=4 证书与由此得到的 27 元对称集、F(4)>=27。复核不把这些结论误报为原逐点猜想 f(n)>=floor(log_2 n) 的完整证明。
- 复核方式：没有发现 q 依赖、角色最大和定理适用范围或量词交换导致强新结论失效。Montgomery--Vaughan Theorem 1 的原文正是对模 q 的全部非主角色给 sum M(chi)^(2k) <<_k phi(q)q^k；取 k=2 得 O(q^3)，无隐藏 log q。概率估计只需联合零类及 Gamma 的 O(log p) 个类，p约为N^(1/5)时失败概率为 O(N^(-1/10)(log N)^3)。主证明成立，但结果稿必须补写 q 的明确选择、模 q 回拉的逻辑顺序，以及含 min 的递推展开；这些是可修复的文字/完备性缺口，不改变定理。
- 证据边界：PASS 认证的是内部候选渐近定理、障碍引理和有限秩下界，不等同于论文发表、同行评审或 Lean 形式化。新下界仍比 Erdős 的逐点目标少一个发散的 O((log log n)^2) 项；循环引理只封堵一种朴素改造；F(4)>=27 没有给 F(4) 上界。因此 #963 仍应保持开放。

#### 第二轮实际尝试

- **限制联合界并定量迭代模素数递推**（advanced）：只要求随机乘法在零类及Γ={1,2,4,…}对应的O(log p)个剩余类上成功，而不对全部p类联合；取p≈N^{1/5}。；对X_i=|rA∩B_i|有 E X_i≍N/(pk)、Var(X_i)≪N^{3/2}，单类失败概率≪p²k²/N^{1/2}。所需类数为O(log p)，当p≈N^{1/5}、k≤log₂N时总失败概率为O(N^{-1/10}(log N)^3)=o(1)。由修补后的半长区间和模p、模q拼接，得到 h(N)≥min(log₂N−1, floor(log₂p)+h(floor(cN/(p log₂N))))。令x_j=log₂N_j，迭代满足 x_{j+1}=(4/5)x_j−log₂x_j+O(1)；总缺陷 Σ_j log₂x_j=O((log x_0)^2)，故 h(N)≥log₂N−O((log log N)^2)。
- **把辅助模数扩大为m≈pk**（refuted）：尝试让新增剩余类贡献log₂k，以抵消短区间的k损失。；一般模数m给出的增益为log₂m，而零类递归规模为N/(mk)。m在增益和递归缩小量中相消后仍剩log₂k损失，因此单纯放大模数无效。
- **扩大整流区间并用模p层排除所有q回绕**（refuted）：设Γ⊂Z/pZ耗散，要求其非零有符号和避开±c,…,±Tc，其中c=q mod p。；令S为Γ的2^{|Γ|}个子集和。若上述禁差成立，则c^{-1}S任意两点的循环间距至少T+1；循环相邻间隙求和给出2^{|Γ|}(T+1)≤p。取T=k−1即 |Γ|≤log₂(p/k)+O(1)，所以这一改造自身必损失log₂k−O(1)。
- **秩4构造搜索与双判据证书**（advanced）：先在整数超图中搜索候选，再分别以全部子集和及{−1,0,1}关系枚举核验。；P={1,2,3,4,5,6,7,8,9,10,12,13,15}含耗散四元组{1,2,4,8}；其全部C(13,5)=1287个五元组均有非零{−1,0,1}关系。故d(P)=4。由第一轮已复核的射影恒等式，A={0}∪±P有27点且d(A)=4。
- **尝试继续扩张秩4整数样本**（inconclusive）：检查初始区间及较大有限整数候选域中的14元候选。；初始区间[1,12]的耗散维数为4，但加入13后出现耗散五元组{3,6,11,12,13}。有限搜索未产生经严格核验的14元样本；有限候选域不能承担任意实数情形的上界。

#### 第二轮新增严格进展

- [第二轮新增] 对充分大n，f(n)≥log₂n−O((log log n)²)。相较第一轮的(1−o(1))log₂n，这把未指定的o(log n)缺陷严格压到O((log log n)²)；误差仍发散，不能推出floor(log₂n)。
- [第二轮新增] 两模无回绕障碍引理：设p为素数、c∈(Z/pZ)^×、1≤T<p，且Γ⊂Z/pZ耗散。若Γ的每个非零有符号和均不属于{±c,…,±Tc}，则2^{|Γ|}(T+1)≤p。
- [第二轮新增] 上述引理严格反驳最直接的无损递推改造：若放宽q整流区间后仅靠同一Γ层排除一个k元和可能产生的±q,…,±(k−1)q回绕，则Γ至多贡献log₂(p/k)+O(1)，无法回收log₂k。
- [第二轮新增] 严格计算证书给出G(4)≥13及F(4)≥27。具体地，A={0}∪±{1,2,3,4,5,6,7,8,9,10,12,13,15}有27个元素而d(A)=4，因此f(27)≤4；这与floor(log₂27)=4相容。

#### 证伪与边界检查

- 论坛中声称逐点完整解答的帖子只证明特殊集合A={1,…,n}含二进制幂，未证明该A是最坏情形；不能作为全称结论。
- 辅助模数由p改成m≈pk后，递推仍为log₂m+h(N/(mk))，代数上仍损失log₂k。
- 循环间距引理明确只否定“由Γ单独排除全部回绕”的方案；它不排除利用零类实际数值协同消除回绕，因而没有反驳原猜想。
- P=[1,13]不是秩4构造，因为{3,6,11,12,13}耗散；程序以两个关系判据复核。
- 秩4证书分别枚举32个五元子集和及3^5−1个非零有符号系数；两个实现对全部1287个五元组一致。
- 循环间距公式在3≤p≤19的81个(p,T)边界情形中，经位掩码穷举与按基数组合/循环间隙搜索独立重算一致。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/verify_rank4_lower_bound.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/verify_rank4_lower_bound.py)：用两个精确判据核验13元正整数样本，并为每个五元组输出等子集和掩码与有符号关系。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963 && python3 verify_rank4_lower_bound.py > rank4_lower_bound_certificate.json && sha256sum verify_rank4_lower_bound.py rank4_lower_bound_certificate.json；结果：1287个五元组全部非耗散，{1,2,4,8}由两判据均确认为耗散。脚本SHA256=75a09c57145b0e8ae0b5bedf3c1c86490cfd2d12b187e5c9347163eb2d862058；证书SHA256=259543908b5508b22bb4a71d45e7927f22669a05db37005030367fb24ed8b041。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/rank4_lower_bound_certificate.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/rank4_lower_bound_certificate.json)：包含全部1287个五元组的非耗散证书，可不调用优化求解器逐项检查。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963 && python3 -c "import json; p=json.load(open('rank4_lower_bound_certificate.json')); assert p['conclusion']=='d(P)=4' and len(p['nondissociation_certificates'])==1287; assert all(any(c:=r['signed_relation']) and sum(a*b for a,b in zip(c,r['five_set']))==0 for r in p['nondissociation_certificates'])"；结果：断言通过；证书大小321385字节。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/verify_cyclic_packing.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/verify_cyclic_packing.py)：以全部位掩码和独立的组合/循环间隙算法交叉检查循环间距极值。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963 && python3 verify_cyclic_packing.py --max-p 19 > cyclic_packing_crosscheck.json && sha256sum verify_cyclic_packing.py cyclic_packing_crosscheck.json；结果：81个边界情形一致。脚本SHA256=120fd67a8e5b3f324b1a8f340757622d8200374bb01254a1bee10fbfaf249ac3；输出SHA256=0b651125a91254d9f4e0127a63728f5567a64b24db045b9e7cf92062e6aa68f4。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/second_round_note.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963/second_round_note.md)：本轮定量递推、两模障碍与秩4构造的自洽推导草稿。；命令：cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/963 && sed -n '1,260p' second_round_note.md && sha256sum second_round_note.md；结果：SHA256=8adaccdebc8ab44dea72b36cae709ad7080fb07a3e6b95616e213b94e76a09d6。全部程序再次运行后输出与保存文件逐字节相同。

#### 当前障碍

当前已严格排除最直接的无损两模改造：仅靠Γ的剩余类信息排除k−1种回绕必付出log₂k损失。要把log₂N−O((log log N)²)推进到log₂N−O(1)，必须利用零类元素的实际数值协同消除回绕，或建立不经过k阶整流的新压缩/拼接。有限秩方面仅知27≤F(4)≤81（后者为旧3^4容量界）；尚无覆盖全部任意实关系核的秩4上界证书。

#### 下一精确定理

最明确的主目标是“联合回绕消除引理”：存在绝对常数C，使模q随机压缩后可选二进制剩余类层Γ及零类耗散集D₀，二者并集的所有有符号和自动避开非零q倍数，同时每层总损失至多C。若成立可导向h(N)≥log₂N−O(1)。较小而可审的目标是确定G(4)∈{13,14,15}，即构造14/15元秩4正集，或给出覆盖全部秩4有理核签名的上界证书。

#### 第二轮证明记录

## 1. 一个定量化递推

令 `h(N)` 为任意 `N` 元正整数集保证的最大耗散子集大小。对使
`d(A)=h(N)` 的集合记 `k=d(A)+1`。若 `k>log_2 N`，则已有
`h(N)>log_2 N-1`。以下设 `k<=log_2 N`。

取素数 `p` 满足 `N^(1/5)<=p<=2N^(1/5)`。固定 `A,p,k` 后，再取任意素数

    q>max(max A,4pk).

于是 `A` 模 `q` 单射且不含零。`q` 可以依赖当前固定的 `A`；后面的失败
概率界对 `q,A` 一致，所以这里没有交换全称与存在量词。令
`g=floor(log_2 p)`，

    Gamma={1,2,4,...,2^(g-1)} subset Z/pZ,

并对 `i in {0} union Gamma` 记 `L=floor(q/(2pk))`，置

    B_i={p x+i:1<=x<=L} subset (Z/qZ)^*.

由 `q>4pk` 有 `L>=q/(4pk)`；又 `0<=i<p`，所以每个代表满足
`0<px+i<q/k`。

对均匀随机的 `r in (Z/qZ)^*`，置 `X_i=|rA intersect B_i|`。有

    E X_i=N L/(q-1)>=N/(4pk).

角色正交给出

    Var(X_i)=1/(q-1)^2
             sum_{chi!=chi_0}|S_A(chi)|^2|S_Bi(chi)|^2.

若 `u_i=i p^(-1) mod q`，则

    S_Bi(chi)=chi(p) sum_{x<=L} chi(x+u_i).

移位循环区间至多分成两个初始部分和之差，故其绝对值至多 `2M(chi)`
（使用宽松的 `4M(chi)` 也足够）。另一方面，角色正交和乘法能量平凡界给
`sum_chi |S_A(chi)|^4<=qN^3`。Montgomery--Vaughan Theorem 1 的一般式是
`sum M(chi)^(2 ell)<<_ell phi(q)q^ell`；取矩参数 `ell=2`，而不是集合大小
参数 `k`，得到 `sum M(chi)^4<<q^3`。Cauchy--Schwarz 因而给出

    Var(X_i)<<N^(3/2).

所以

    P(X_i<E X_i/2)<<p^2 k^2/N^(1/2).

这里只需对 `g+1=O(log p)` 个实际使用的类联合，而非对全部 `p` 个类联合。
由于 `p<=2N^(1/5)` 且 `k<=log_2 N`，总失败概率为

    O(N^(-1/10)(log N)^3)=o(1).

因此存在同一个 `r` 使所需每类都有至少 `cN/(pk)` 个点。令
`M=floor(cN/(p log_2 N))`。从零类任选 `M` 点，除以 `p` 后取一个
`h(M)` 元耗散集 `D_0`；从 `Gamma` 每类各取一点。

若 `g+h(M)>=k`，从并集中抽取恰好 `k` 个代表。若其在原集合 `A` 中的
逆像有非零有符号关系，乘以 `r` 后先得到模 `q` 关系。每个代表严格小于
`q/k`，故该 `k` 项和的绝对值严格小于 `q`，模 `q` 为零便迫使它作为
整数和也为零。再模 `p`，`Gamma` 的二进制幂耗散性迫使所有非零类系数
为零；余下零类关系除以 `p`，又被 `D_0` 的耗散性排除。这与
`d(A)=k-1` 矛盾。因此

    h(N)>=min(log_2 N-1,
              floor(log_2 p)+h(floor(cN/(p log_2 N)))).          (R)

为避免把 (R) 的 `min` 偷换成“总走第二分支”，令
`N_(j+1)=floor(cN_j/(p_j log_2 N_j))`、`x_j=log_2 N_j`、
`g_j=floor(log_2 p_j)`，直到 `N_T` 落入固定阈值。反复展开 (R) 得

    h(N_0)>=min(
      min_(0<=t<T)(sum_(j<t) g_j+x_t-1),
      sum_(j<T)g_j+h(N_T)).

同时

    x_(j+1)=(4/5)x_j-log_2 x_j+O(1),
    g_j=x_j-x_(j+1)-log_2 x_j+O(1).

迭代到固定阈值，步数 `T=O(log x_0)`，且

    sum_(j<T) log_2 x_j=O((log x_0)^2).

对每个可能停点 `t`，伸缩恒等式给

    sum_(j<t)g_j+x_t-1
      =x_0-sum_(j<t)log_2 x_j+O(t);

终端分支也等于 `x_0-O(sum_(j<T)log_2 x_j+T)`。因此 `min` 中的每一项
都有同一个下界，严格得到

    h(N)>=log_2 N-O((log log N)^2).

对任意 `n` 元实数集，先按 `a~-a` 取至少 `ceil((n-1)/2)` 个非零代表；
逐个改号不改变耗散性。选择有理线性泛函时，同时避开两点差及全部非零
ternary 组合对应的有限超平面，再清分母，便得到互异正整数像集并精确保留
所有耗散关系。这个整流只损失一个二进制位，故

    f(n)>=log_2 n-O((log log n)^2).                              (Q)

这严格强于第一轮只记录的 `(1-o(1))log_2 n`，但仍远弱于逐点零缺陷。

## 2. 两模“无回绕”方案的必要损失

设 `p` 为素数，`c` 在 `Z/pZ` 中非零，`Gamma subset Z/pZ` 耗散，
`|Gamma|=g`。若每个非零有符号和都避开

    {+-c,+-2c,...,+-Tc},

则令 `S` 为 `Gamma` 的 `2^g` 个子集和。对任意不同 `x,y in S`，差
`x-y` 是非零有符号和。因此 `c^(-1)S` 中任意两点的循环距离至少 `T+1`。
把这些点按循环顺序排列，相邻间隙之和为 `p`，所以

    2^g(T+1)<=p.

在放宽整流区间后，一个 `k` 元有符号和可能等于 `tq`，
`1<=|t|<=k-1`。对充分大 `N`，有 `k-1<p`；且 `q>p` 为不同素数，
所以 `q mod p` 非零。若仍企图只靠 `Gamma` 的模 `p` 剩余类统一排除
全部回绕，则上式取 `T=k-1`，必损失至少 `log_2 k-O(1)` 个二进制位。
因此，这一最直接的方案不能得到无损递推；该引理不排除利用零类实际数值
或完全不同机制的方案。

附带程序只枚举 `1<=T<=(p-1)/2` 的有限边界例；更大的 `T` 由上述循环
相邻间隙纸面证明覆盖，81 个计算例不承担全参数证明。

## 3. 秩四下界

令

    P={1,2,3,4,5,6,7,8,9,10,12,13,15}.

`{1,2,4,8}` 耗散。两个独立判据（枚举 32 个子集和；枚举 `3^5-1` 个
非零有符号系数）均核验 `P` 的全部 `C(13,5)=1287` 个五元子集不耗散。
因此 `d(P)=4`。由射影化恒等式，
`A={0} union (+-P)` 有 27 点且 `d(A)=4`，故

    G(4)>=13,   F(4)>=27,   f(27)<=4.

这与猜想 `floor(log_2 27)=4` 相容；它不是 `F(4)` 的上界。

## 4. 范围和来源

新渐近界仍比 Erdős 的逐点目标少一个发散的 `O((log log n)^2)` 项；
循环引理只封堵一种朴素改造；`F(4)>=27` 没有给 `F(4)` 上界。解析输入
Montgomery--Vaughan Theorem 1 是同行评审定理；渐近拼接方法的主体来自
KoishiChan 论坛路线。本轮加强尚未发表、未经外部同行评审，也未 Lean
形式化，因此 #963 仍开放。

#### 本轮核查来源

- [P. Erdős, Extremal Problems in Number Theory, p.188](https://users.renyi.hu/~p_erdos/1965-02.pdf)；一手来源：true；核验：第188页明确陈述任意n个实数可贪心得到至少 floor(log n/log 3) 个子集和互异的数，并询问能否改为 floor(log n/log 2)；A={1,…,n} 仅用于说明猜想近乎最佳。
- [KoishiChan, Erdős Problems #963 forum proof, 5 Dec 2025](https://www.erdosproblems.com/forum/thread/963?order=oldest)；一手来源：true；核验：原帖精确声称的是 (1−o(1))log₂n，并给出模素数递推；第122、169行附近的短区间端点随后被Tao质疑，作者认可修正。原帖Γ误写为整数区间，本轮继续采用第一轮修补后的二进制幂集合。
- [H. L. Montgomery and R. C. Vaughan, Mean Values of Character Sums, Theorem 1](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/9372DCDEE648FF605F66A10314977F5F/S0008414X00012116a.pdf/mean-values-of-character-sums.pdf)；一手来源：true；核验：Theorem 1给出非主特征最大部分和的固定阶矩估计；四阶特例提供 Σ_{χ≠χ₀}M(χ)^4≪q^3，是本轮方差估计使用的解析输入。
- [V. F. Lev and R. Yuster, On the size of dissociated bases, Theorem 2](https://arxiv.org/abs/1005.0155)；一手来源：true；核验：论文比较同一有限阿贝尔群子集中不同极大耗散集的大小；其结论不能把本题的有符号张成容量直接压至2^r，也不包含本轮定量下界。
- [A. Bailleul and R. Riblet, On the largest Sidon subset in a finite subset of R^N, Lemma 2.3](https://arxiv.org/pdf/2605.03181)；一手来源：true；核验：Lemma 2.3对Freiman 2关系给出循环群压缩，保留至少 |A|/2−|A|²/(2m) 个点。它只保存二阶关系，不保存任意长度子集和；将其分数部分窗口朴素推广到阶k会产生1/k保留率，这一点是本轮推论而非论文定理。
- [Erdős Problems #963](https://www.erdosproblems.com/963)；一手来源：false；核验：截至本轮检索，主页仍标OPEN并只列贪心下界；论坛已有渐近证明但主页未同步。未找到解决逐点猜想的论文、预印本、作者仓库或Lean代码。

### #1063

- 第一轮障碍：主要开放缺口仍是统一上界。新下界和候选稀疏化没有控制最小乘子 m；CRT 的朴素模数仍具有 exp((1+o(1))k) 规模，因而不能推出 FormalConjectures 所要求的严格渐近改进。
- 第一轮下一定理：令 m_k 为最小的 m，使某个 0≤e<k 对 n=mD(k)+e 给出唯一失败项。下一条精确目标是证明 log m_k=o(k)。由于 log D(k)=O((log k)^2)=o(k)，这将推出 n_k=exp(o(k))，从而严格解决 better_upper。第一步应给出所有 sqrt(k)<p≤k 的局部允许剩余类的精确分类，再尝试筛出 m≤exp(o(k))。
- 第二轮用时：1704.0 秒；硬上限 14400 秒；后端：completed
- 第二轮目标：在上一轮 D(k)|n−e 的稀疏化基础上，精确分类 e=0 路线的局部允许剩余类，主动审计 CRT 密度到短代表元的量词；若 log m_k=o(k) 仍过强，则直接寻找能统一删去 LCM 因子的短乘子构造。
- 第二轮结论：route_advanced；完整解声明：none；置信度：high

- 独立复核：PASS；范围：独立复核第二轮 deleted-large-prime 构造：对充分大的 k，取 L_k=lcm(1,…,k−1)、p 为最小的 p>k/2 素数，可以选择 1≤t≤2p−k+1，使 n=tkL_k/p≥2k 且 n 是 n,n−1,…,n−k+1 中唯一不整除 binom(n,k) 的项。因此 n_k=o(kL_k)，并可推出 n_k=O(k^0.525 L_k)。
- 复核方式：不采用原代理结论作为前提，逐式重做 p 的选取、短乘子鸽巢界和所有 q-adic 分支；另写内联 Python 实现直接检查二项式整除与 Legendre 赋值；随后重跑仓库原审计脚本，并独立核对 PNT 与 Baker–Harman–Pintz 0.525 输入的推论方向。复核代理未编辑原文件；主代理随后按复核意见补强了证明稿。
- 证据边界：PASS 是对当前候选数学证明的内部独立审稿结论，不等同于论文已发表、专家同行评审已完成或 Lean 已形式化。两处文字补强已落实到独立证明稿及结构化审计字段；开放式原题仍需更强的匹配上下界或渐近估计。

#### 第二轮实际尝试

- **e=0 路线的精确素数幂判据**（advanced）：令 n=mD(k)，把每个 p-adic Legendre 层写成长度 k 区间中的倍数盈余，并同时检查必要性与充分性。；对 p∤k、p^j≤k，第 j 层盈余等于 1 当且仅当 n mod p^j<k mod p^j。区间一定含 p^j 倍数；若任一层缺失，则最大 p-adic 赋值项无法被覆盖且其下标不可能是0。反之所有这些层均为1，p^j>k 的实际出现层也自动贡献1。故 n 的失败集恰为{0}当且仅当上述不等式对全部 p∤k、p^j≤k 成立；p|k 的部分由 D(k) 的赋值保证。
- **局部允许类计数与大素数完全分类**（advanced）：按 p 进制低位数字计数允许类，并对 p>sqrt(k) 单独展开。；若 p^h≤k<p^(h+1)，写 k 的低 h 位为 k_0,…,k_{h−1}，则模 p^h 的允许类数精确为 k_0∏_{a=1}^{h−1}(k_a+1)：最低位严格小于 k_0，其余各位不超过对应 k_a。若 p>sqrt(k)、k=up+s，则局部无失败恰在 n mod p<s；否则有 p² 倍数时它是唯一局部失败，没有 p² 倍数时全部 u 个 p 倍数失败。
- **CRT/筛法量词审计**（refuted）：计算全部局部允许类的乘积密度，并检查密度能否推出最小正代表元。；对 p>sqrt(k)，余数 k mod p 两两不同，否则两个大素数会同时整除同一个小于 k 的 k−s；由阶乘下界与 pi(k)=O(k/log k)，大素数的负对数密度为 O(k loglog k/log k)，小素数幂总成本为 O(sqrt(k)log k)，合计 o(k)。但密度为 exp(−o(k)) 不蕴含区间 [1,exp(o(k))] 中有代表元：乘法逆像可把恒定密度的允许区间推到模 p 的末段。故朴素 CRT 独立性推断存在严格量词缺口。
- **删去一个近 k/2 素数的短乘子构造**（advanced）：取 L_k=lcm(1,…,k−1) 及最小素数 p>k/2，从 kL_k 中删去 p，再用模 p 的最小正允许乘子修复唯一局部缺口。；置 A=kL_k/p、s=k−p。充分大 k 时 PNT 给 k/2<p<k、p=k/2+o(k)，从而 v_p(A)=0、s≥2。t↦tA mod p 是置换；允许区间[0,s−1]的 s 个原像中一个是 t=0，余下 s−1 个为正，故最小正原像满足 t≤p−s+1=2p−k+1≤p−1。取 n=tA。p 处区间恰含两个 p 倍数，Legendre 赋值等于二者最大赋值；其他不整除 k 的素数幂仍整除 n；每个 q|k 覆盖全部 i≥1 而严格使 i=0 失败。于是 n 是合法唯一失败见证。
- **更强目标 log m_k=o(k)**（blocked）：尝试由局部密度或简单族 m=1,k,k−1,lcm(1,…,sqrt(k)) 控制 n=mD(k) 的最小乘子。；简单族均出现很小反例；而局部密度不控制短区间代表元。本轮删素数构造足以闭合 better_upper，却仍有 log m=(1+o(1))k，不能证明更强的 log m_k=o(k)。

#### 第二轮新增严格进展

- [第二轮新增] 令 p(k) 为最小的 p>k/2 素数、L_k=lcm(1,…,k−1)。充分大 k 时存在 1≤t≤2p−k+1，使 n=t kL_k/p 的失败集精确为{0}。因此 n_k≤[(2p−k+1)/p]kL_k=o(kL_k)。
- [第二轮新增] 这给 FormalConjectures 的 better_upper 一个显式候选答案：有限多个小 k 中，3≤k<K 取 Cambie 的 kL_k，k=2 取 n_2=4，k=0,1 任意定义；其余取 U(k)=[(2p(k)−k+1)/p(k)]kL_k。于是 n_k=O(U(k)) 且 U(k)=o(kL_k)。
- [第二轮新增] 结合 Baker–Harman–Pintz 的下一素数间隙 O(x^0.525)，还得到定量新上界 n_k=O(k^0.525·lcm(1,…,k−1))。
- [第二轮新增] 得到 e=0 的精确局部充要条件和每个素数的 p 进制数字盒计数；这把后续 Fourier/筛法问题从启发式变成明确的短区间 CRT 命中问题。
- [第二轮新增] 得到 p>sqrt(k) 的全部局部失败分类，并证明局部 CRT 允许集合的倒密度仅为 exp(o(k))；同时严格指出该密度本身不能推出 log m_k=o(k)。

#### 证伪与边界检查

- 边界 r=0 被单列：在 t∈{0,…,p−1} 中其唯一原像是 t=0；t=p 虽也给 r=0，却正好退回旧构造 kL_k。因为 s=k−p≥2，必有非零允许类且选出的 t≤p−1。
- p 的范围被单列：只对充分大 k 用 PNT 选 p，确保 k/2<p<k；故 p 在 L_k 中恰出现一次、p∤k、v_p(kL_k/p)=0。小 k 中仅 3≤k<K 使用已知 kL_k 上界；k=2 单列 n_2=4。
- 对 q≠p 分三类复核：q>k 时分母无 q；q≤k且q∤k时所有 q^j≤k 仍整除 n，逐层有 N_j−floor(k/q^j)=1；q|k 时 v_q(n−i)=v_q(i) 对1≤i<k，且 v_q(C(n,k))=v_q(n)−v_q(k)，只让 i=0 失败。q=p 的两个倍数另作精确层计数。
- 新构造对全部 10≤k≤5000 共4991项通过短乘子和局部条件检查；其中291项通过独立 p-adic 完整失败集检查，141项另以实际整数 binomial 逐项取模，全部得到失败集[0]。
- 大素数局部分类穷举316314个(k,p,n)配置无反例；e=0 充要判据检查9900个(k,m)实例，数字计数公式检查1294个(k,p)实例无反例。
- 简单统一乘子 m=1、m=k、m=k−1 和 m=lcm(1,…,floor(sqrt(k))) 均被有限反例否定；未把小 k 数表外推成渐近结论。

#### 可复现资产

- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py)：本轮全整数审计脚本：删素数构造、直接 binomial 与独立 p-adic 双检、e=0 充要判据、p 进制数字计数和大素数局部分类。SHA256=3b5cee651c73a0bb30f2667466482b30201bc9498f0086a13ccc1cef3c97bcb8。；命令：python3 artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py construct --kmin 10 --kmax 5000 --exact-kmax 300；结果：checked=4991，exact_padic=291，exact_direct=141；全部通过。输出保存为 construction_check.txt，SHA256=e1c4dc7088153d583de8118dc7d26771ac38b8709f2394090ea8a938834abb25。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py)：精确局部充要判据和数字盒计数回放。；命令：python3 artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py localcheck --kmax 100 --mmax 100；结果：1294个数字计数及9900个完整局部等价实例全部通过；输出 local_criterion_check.txt，SHA256=513e44804157e6d2cd6664958884d4e0d94bd1a553eba71d88a053b54d8db7a8。
- [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/round2_proof_note.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/round2_proof_note.md)：删素数短乘子定理、全部素数边界、局部充要条件、数字计数及 CRT 量词审计的完整证明稿。；命令：python3 -m py_compile artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py；结果：证明稿与可执行检查均已保存；尚待外部同行评审或形式化。

#### 当前障碍

FormalConjectures 的 better_upper 子目标已有经内部独立复核的完整数学证明，但官网原题只说“Estimate n_k”，新上界仍与上一轮 primorial 子序列下界相距巨大。更强的 log m_k=o(k) 仍卡在短区间 CRT 命中：允许类的乘积密度是 exp(−o(k))，却没有足够的 Fourier/筛法分布定理保证 exp(o(k)) 内出现正代表元。

#### 下一精确定理

优先把删素数定理独立审稿并形式化；其精确陈述是 n_k=O(k^0.525·lcm(1,…,k−1))，little-o 版本只需 PNT。若继续攻更强界，应证明：对 n=mD(k) 的 p 进制数字盒系统，存在 m≤exp(o(k))；不能只使用全周期密度，必须给出短区间 Fourier 误差或高维筛法的定量下界。

#### 第二轮证明记录

Let

\[
L_k=\operatorname{lcm}(1,2,\ldots,k-1).
\]

This note proves a new uniform upper bound which is strictly smaller than the
Cambie bound (kL_k).  It therefore settles the precise `better_upper`
subproblem in the current FormalConjectures statement, although it does not
give a matching estimate for the original, deliberately open-ended problem.

## 1. Deleted-large-prime construction

### Theorem

Let (p=p(k)) be the least prime strictly larger than (k/2).  For all
sufficiently large (k), there is an integer (t) such that

\[
 1\le t\le 2p-k+1
\]

and, with

\[
 n=\frac{t kL_k}{p},
\]

the only member of (n,n-1,\ldots,n-k+1) which does not divide
\(\binom nk\) is (n).  Consequently

\[
 n_k\le \frac{2p-k+1}{p}\,kL_k=o(kL_k).
\]

Using Baker--Harman--Pintz's (O(x^{0.525})) bound for the next-prime gap,
this sharpens quantitatively to

\[
 n_k=O\!\left(k^{0.525}L_k\right).
\]

### Choosing the short multiplier

For large (k), the prime number theorem gives

\[
 k/2<p<k,\qquad p=k/2+o(k).
\]

Put (s=k-p) and (A=kL_k/p).  Since (p>k/2), the prime (p) occurs to
the first power in (L_k), and (p\nmid A).  Multiplication by (A) permutes
the residues modulo (p).  Hence exactly (s) values of
(t\in\{0,1,\ldots,p-1\}) satisfy

\[
 0\le tA\bmod p<s.
\]

One is `t=0`, and the other `s-1` are positive.  If `t_0` is the least
positive one, then the elementary worst-case placement of `s-1` elements in
\(\{1,\ldots,p-1\}\) gives

\[
 t_0\le p-s+1=2p-k+1.
\]

Here `t=p` would also give residue zero, but it recreates the old value
`k L_k`.  It is not selected: since `s>=2` for all sufficiently large `k`,
there is at least one nonzero allowed residue and the displayed bound is at
most `p-1`.  Write `r=t_0 A mod p`.  Necessarily `0<r<s`.

### Divisibility at the deleted prime

The interval of indices (0\le i<k) contains exactly the two solutions

\[
 i=r,\quad i=r+p
\]

to (p\mid n-i), because (r<s=k-p).  Since (k<p^2), at most one of
these two integers is divisible by (p^2).  If the larger (p)-adic
valuation among the two is (M\ge1), then

\[
 v_p\binom nk
 =\sum_{i=0}^{k-1}v_p(n-i)-v_p(k!)
 = (M+1)-1=M.
\]

Thus the (p)-part of every (n-i) divides the binomial coefficient.

### Divisibility at every other prime

Let (q\ne p) be prime.

* If (q>k), then (v_q(k!)=0), so each numerator factor (n-i) is
  automatically covered.
* Suppose (q\le k) and (q\nmid k).  Every prime power (q^j\le k)
  divides (L_k/p) (equality (q^j=k) would force (q\mid k)), hence
  (q^j\mid n).  Also (q^j\nmid k).  At each such level the block of
  (k) consecutive numerator factors therefore has exactly one more
  multiple of (q^j) than (k!): in the notation below,
  \(N_j-\lfloor k/q^j\rfloor=1\).  Levels above (k) contribute one whenever
  they occur.  It follows that
  (v_q\binom nk\ge v_q(n-i)) for every (i).
* Suppose (q^a\parallel k), and put
  (b=\lfloor\log_q(k-1)\rfloor).  The integer (n) is divisible by
  (q^{a+b}).  For (1\le i<k),
  (v_q(n-i)=v_q(i)\le b).  Equivalently, every factor
  ((n-i)/i) in \(\binom{n-1}{k-1}\) is a (q)-adic unit, and hence

  \[
  v_q\binom nk=v_q(n)-a\ge b\ge v_q(n-i).
  \]

  For (i=0), however,
  (v_q\binom nk=v_q(n)-a<v_q(n)).  Thus (n) fails to divide
  \(\binom nk\).

This proves that (n) is the unique failed member.  Finally,
(L_k/p\to\infty), so (n\ge2k) for all sufficiently large (k).  For the
finitely many remaining values, use Cambie's (kL_k) construction when
\(k\ge3\), take \(n_2=4\), and define the irrelevant \(k=0,1\) values
arbitrarily when assembling an `atTop` upper-bound function.

Since (p=k/2+o(k)), the factor ((2p-k+1)/p) tends to zero.  To spell out
the quantitative corollary, Baker--Harman--Pintz gives a prime in
\([X-X^{0.525},X]\) for all large \(X\).  Put
\(X=x+2x^{0.525}\); then \(X-X^{0.525}>x\) for large \(x\), so the least
prime above \(x\) is \(x+O(x^{0.525})\).  Taking \(x=k/2\) gives
(2p-k=O(k^{0.525})), yielding the displayed quantitative bound.

## 2. Exact local criterion for the (e=0) route

The following reduction explains why the construction works and repairs a
quantifier weakness in a naive CRT heuristic.

Let

\[
D(k)=k\prod_{q\mid k}q^{\lfloor\log_q(k-1)\rfloor}
\]

and write (n=mD(k)).  Then (n) is the unique failed member if and only if,
for every prime (q\nmid k) and every (q^j\le k),

\[
 n\bmod q^j<k\bmod q^j. \tag{1}
\]

Indeed, with (N_j=\#\{0\le i<k:q^j\mid n-i\}),

\[
v_q\binom nk=\sum_{j\ge1}\left(N_j-\lfloor k/q^j\rfloor\right),
\]

and every summand is zero or one.  For (q^j\le k), it is one exactly when
the inequality in (1) holds.  As the block contains a multiple of every such
(q^j), covering its maximum (q)-adic valuation forces all these summands
to be one.  Conversely, (1), together with the automatically positive levels
above (k), covers every valuation.  Primes dividing (k) make (n) fail
and cover every (n-i), (i\ge1), by the preceding argument.

If (k=\sum k_aq^a) in base (q), and (q^h\le k<q^{h+1}), the number of
residue classes (x\pmod {q^h}) satisfying all the local inequalities is

\[
 k_0\prod_{a=1}^{h-1}(k_a+1).
\]

This follows digit by digit: the first digit must satisfy (x_0<k_0), and
each later digit satisfies (x_a\le k_a).

For (q>\sqrt{k}), writing (k=uq+s), this reduces to the particularly
simple exact classification:

* if (n\bmod q<s), the prime (q) causes no failure;
* otherwise, if there is a (q^2)-multiple in the block, that term alone is
  the local failure;
* otherwise all (u) multiples of (q) are local failures.

The exhaustive checker confirms this classification on 316,314 triples.

## 3. Why density alone does not prove \(\log m_k=o(k)\)

The local CRT set has subexponentially small reciprocal density.  For
(q>\sqrt{k}), the allowed fraction is ((k\bmod q)/q).  The nonzero
remainders (k\bmod q) are distinct as (q) ranges over primes larger than
\(\sqrt{k}): two such primes dividing the same (k-s<k) would have product
larger than (k).  Together with the elementary factorial bound and the
\(O(\sqrt{k})\) total logarithmic cost from smaller prime powers, this gives

\[
 -\log(\text{CRT density})
 =O\!\left(\frac{k\log\log k}{\log k}+\sqrt{k}\log k\right)=o(k).
\]

This does **not** by itself put a representative below \(\exp(o(k))\).  Even
for one prime, a set of allowed residues of constant density can be pulled
back by multiplication to the final segment of
\(\{1,\ldots,q-1\}\), so its first positive representative can be of order
\(q\).  A short-interval sieve or Fourier-discrepancy input is still needed
to prove the stronger target \(\log m_k=o(k)\).  The deleted-prime theorem
sidesteps that unjustified independence step and proves exactly the weaker
asymptotic improvement requested by `better_upper`.

## 4. Reproduction

From the repository root:

```bash
python3 artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py classify --kmax 80 --nmult 10
python3 artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py localcheck --kmax 100 --mmax 100
python3 artifacts/erdos_followup_20260719/proof_routes_round2_4h/work/1063/explore_1063_round2.py construct --kmin 10 --kmax 5000 --exact-kmax 300
```

The first command checks 316,314 large-prime local configurations.  The
second checks 1,294 digit-count cases and 9,900 exact `e=0` equivalences.  The
third verifies the short-multiplier bound for every `10<=k<=5000`, performs a
complete exact p-adic failure-set check for 291 eligible values through
`k=300`, and independently checks the literal binomial divisibilities in 141
cases through `k=150`.

## Sources used in this round

* Erdős Problems #1063 and its discussion thread:
  <https://www.erdosproblems.com/1063>
* FormalConjectures #1063, snapshot commit
  `c252a41054125b5fd9c8356e2137cd9b55337657`.
* R. C. Baker, G. Harman and J. Pintz, *The Difference Between Consecutive
  Primes, II*, Proc. London Math. Soc. 83 (2001), 532--562,
  <https://doi.org/10.1112/plms/83.3.532>.

#### 本轮核查来源

- [Erdős Problem #1063](https://www.erdosproblems.com/1063)；一手来源：true；核验：官网截至本轮仍标 OPEN；题面要求估计 n_k，并记录 Cambie 上界 n_k≤k·lcm(1,…,k−1)。
- [FormalConjectures/ErdosProblems/1063.lean, snapshot c252a410](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/1063.lean)；一手来源：true；核验：better_upper 的精确量词是存在 U，使 n(k)=O(U(k)) 且 U=o(k·lcm(1,…,k−1))；当前声明含 sorry。
- [Baker–Harman–Pintz, The Difference Between Consecutive Primes, II](https://doi.org/10.1112/plms/83.3.532)；一手来源：true；核验：Proc. London Math. Soc. 83 (2001), 532–562；其 0.525 次幂短区间素数定理给下一素数间隙 O(x^0.525)，用于把本轮 o(kL_k) 上界量化为 O(k^0.525 L_k)。仅用素数定理也足以得到所需 little-o。
