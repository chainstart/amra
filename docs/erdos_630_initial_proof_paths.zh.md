# Erdős 冻结 630 题逐题初步证明路径

> 生成日期：2026-07-19。这是初步研究筛查，不是 630 道题已被证明的声明。

## 范围与方法

本文覆盖仓库 `erdos_open_shortlist_refreshed.yaml` 中冻结的 630 条记录。该清单是历史 cohort；状态按当前 Erdős Problems 数据库快照重新核对。每题输入精确题面、官方背景、现有 Lean 文件（如有）以及一份不可信的既有候选答案，再进行独立的浅层证明/反例/归约审计。每题所在的代理批次硬超时不超过30分钟；条目中的秒数是批次墙钟时间按题数均摊，并非单题独占计时。

- 当前元数据来源：[teorth/erdosproblems](https://github.com/teorth/erdosproblems)，提交 `aab2deceb51aee0ef28c17d8d194249cbee13d7a`
- 题面与既有候选来源：[neelsomani/gpt-erdos](https://github.com/neelsomani/gpt-erdos)，提交 `21b48ae6b97279e9fe6781e3744e1cdd835e2cc1`
- 已完成独立探测：630/630
- 判定含义：`promising` 表示找到值得继续验证的具体路线；`partial` 表示有严格局部推进；  `blocked` 表示尚未越过开放核心；其他判定用于已知解、反例、病题或独立性。
- 严格免责声明：凡当前官方状态仍为 `open` 的题，本文中的“完整证明”、“反例”或“独立性”都只算待复核候选；未经独立专家审稿，不改变官方状态。

## 状态总览

| 当前状态 | 数量 |
|---|---:|
| open | 550 |
| proved (Lean) | 22 |
| solved | 15 |
| disproved | 12 |
| proved | 12 |
| disproved (Lean) | 8 |
| solved (Lean) | 8 |
| falsifiable | 2 |
| independent | 1 |

## 初筛结论分布

| 初筛判定 | 数量 |
|---|---:|
| partial | 239 |
| blocked | 146 |
| promising | 133 |
| known_resolution | 63 |
| counterexample | 28 |
| malformed | 19 |
| independent | 2 |

## 结构质检与冲突清单

| 检查项 | 结果 |
|---|---:|
| cohort 覆盖 | 630/630 |
| 待处理题目 | 0 |
| cohort 外结果 | 0 |
| 必填字段错误 | 0 |
| 后端非完成状态 | 0 |
| 批次累计运行时（按题均摊求和） | 10.17 小时 |
| 最长单批墙钟时间 | 508.6 秒 |
| 最大单题均摊时间 | 138.5 秒 |

- **官方仍为 open、但初筛给出解答型判定（24 条）**：[#129](https://www.erdosproblems.com/129)、[#180](https://www.erdosproblems.com/180)、[#335](https://www.erdosproblems.com/335)、[#520](https://www.erdosproblems.com/520)、[#545](https://www.erdosproblems.com/545)、[#550](https://www.erdosproblems.com/550)、[#563](https://www.erdosproblems.com/563)、[#575](https://www.erdosproblems.com/575)、[#612](https://www.erdosproblems.com/612)、[#638](https://www.erdosproblems.com/638)、[#654](https://www.erdosproblems.com/654)、[#655](https://www.erdosproblems.com/655)、[#701](https://www.erdosproblems.com/701)、[#786](https://www.erdosproblems.com/786)、[#796](https://www.erdosproblems.com/796)、[#836](https://www.erdosproblems.com/836)、[#890](https://www.erdosproblems.com/890)、[#917](https://www.erdosproblems.com/917)、[#918](https://www.erdosproblems.com/918)、[#920](https://www.erdosproblems.com/920)、[#935](https://www.erdosproblems.com/935)、[#985](https://www.erdosproblems.com/985)、[#1070](https://www.erdosproblems.com/1070)、[#1112](https://www.erdosproblems.com/1112)。
- **官方已非 open、但初筛仍呈未闭合/题面错配（11 条）**：[#42](https://www.erdosproblems.com/42)、[#114](https://www.erdosproblems.com/114)、[#123](https://www.erdosproblems.com/123)、[#321](https://www.erdosproblems.com/321)、[#351](https://www.erdosproblems.com/351)、[#488](https://www.erdosproblems.com/488)、[#750](https://www.erdosproblems.com/750)、[#793](https://www.erdosproblems.com/793)、[#986](https://www.erdosproblems.com/986)、[#987](https://www.erdosproblems.com/987)、[#990](https://www.erdosproblems.com/990)。

以上是人工复核队列，不是结构错误，也不是状态改写。常见原因包括题面按字面可反驳、官方保留的是修正版、元数据更新时间差、或 Lean 形式化题面与当前自然语言版本不一致。

## 当前开放题中的优先续攻路线

下表只保留官方仍为 `open`、初筛为 `promising/partial` 且可行性至少 8/10 的 23 条路线。分数只是下一步是否具体可检验，不代表接近完整解决。

| # | 分数 | 判定 | 下一项可检验任务 |
|---:|---:|---|---|
| 952 | 10 | partial | 固定小整数 C，形式化一个有限“环带证书”：列出一条格点闭曲线，使其 C-邻域内每个 Gaussian 整数都有显式非平凡因子，并用有限图搜索验证该曲线确实分离内外。成功只能排除该 C，但可检验 CRT 屏障路线的可扩展性。 |
| 1083 | 10 | promising | 对距离按 M_t≤n^{2−η} 与 M_t>n^{2−η} 截断：低重数部分用能量估计，高重数部分尝试证明点集集中在少数正交球面或低维代数簇上，再归约到较低维 distinct-distance 问题。先在 d=4 的两圆 Lenz 模型上验证该分解能恢复 Ω(n^{1/2}) 个距离。 |
| 1039 | 9 | promising | 逐行重建并形式核验引理：若 $\|z_i\|\le1$ 且 $\|w_i-z_i\|\le\varepsilon$，则 $\prod_i\prod_j\|w_i-z_j\|\le((1+\varepsilon)^n-1)^n$；重点检查重根、$\varepsilon=0$、严格/非严格边界及 Hadamard/Vandermonde 步骤。 |
| 25 | 8 | promising | 按模数分 dyadic 块 $2^j<n_i\le2^{j+1}$，检验能否利用“每个模数至多一个剩余类”和模数互异性，证明尾块并集的调和质量严格优于粗糙和 $\sum1/n_i$；首先计算两剩余类交集为空或密度为 $1/\operatorname{lcm}(n_i,n_j)$，再做二阶 Bonferroni 下的最坏重叠优化。 |
| 117 | 8 | promising | 计算 limsup h(n)^{1/n} 的候选下界：系统比较 extraspecial p-群及其中心积，明确求出 ω(G) 与最小阿贝尔覆盖数，看 p>2 或非经典辛 spread 是否改进 √2。 |
| 143 | 8 | partial | 从 KLL 的 GCD-graph 论证中提取定量逆定理：检验能否推出 $H(X)\ll\log X/(\log\log X)^{1+\delta}$ 或某个分块可求和估计；任何这样的界经 Abel 分部都会解决第一问。 |
| 148 | 8 | promising | 对固定前 k−4 个分母，把剩余有理数归约为 m/n，并复现 Elsholtz–Planitzer 的四项分母参数计数；可检验目标是从上述递推上界中消去 log k，而不是直接追求最佳常数 1/5。 |
| 256 | 8 | partial | 把 Belov–Konyagin 的三角多项式定理逐项翻译成指数多重集，核对常数项、允许重复以及从其定理到 log f(n)≪(log n)^4 的参数对应；这是可独立审计的下一步。 |
| 301 | 8 | partial | 枚举较小乘数集合 T，建立其单位分数关系超图，并计算分数覆盖数；只保留能用 p-adic 剩余类铺成不交缩放块且给出超过 3/28 遗漏密度的候选。 |
| 325 | 8 | partial | 对每个3≤k≤10整理现有六变量均值估计的明确指数 θ_k（R≪x^{θ_k}），代入 6/k−θ_k 得到可核验的 f_{k,3} 指数表，优先复算 k=3 的0.91709477。 |
| 332 | 8 | partial | 写出一个纯组合版本：从任意 d*(A)>δ 出发构造有限 F（目标 \|F\|≤⌈1/δ⌉ 型界），证明 F+D(A)=ℤ；逐项检查由有限窗口中的高重叠到“无穷多次出现”的对角抽取。 |
| 377 | 8 | promising | 继续把小素数按 base-p 位数 j 分层，即 n^{1/(j+1)}<p≤n^{1/j}；先对固定 j=2 写出两位无进位条件对应的二维区间，并检验筛上界求和是否仍为 O(1/j^2)。若能得到对 j 可求和的界，才可能闭合全范围。 |
| 539 | 8 | partial | 逐引理审计 ProofCouncil 的高维正部差集构造，重点检查维数选择、边界计数，以及由 \(\mathbb Z_{\ge 0}^d\) 指数向量嵌入互异整数时是否完整保持 \(Q(A)\)。 |
| 635 | 8 | partial | 把 Elliott 不等式代入 f=1_A 的常数和端点误差完整写出，得到一个显式误差（例如 O_t(N/√log log N) 量级），再检查能否通过分块或迭代采样改善；这是可逐行核验的下一步。 |
| 679 | 8 | partial | 把修正后的 P_r 构造写成引理，并用一个明确可引用的 p_r=r(log r+loglog r−1+O(loglog r/log r)) 估计逐项验证常数 c；这也会彻底排除先前候选的“小 k”漏洞。 |
| 686 | 8 | promising | 先固定最小未解决平方值并逐个检验 k=3：化为 \((m+2)^3-(m+2)=N[(n+2)^3-(n+2)]\)，再对所得三次曲线做严格的整数点/Thue 方程归约，而非仅搜索有理点。 |
| 776 | 8 | promising | 逐引理核对 He–Tang 的下界证明：从 2 层与 n-2 层的交叉相交结构出发，验证其如何利用第 3、n-3 层排除 n≤2r+2；随后检查上界构造中 2log₂r 项来自何种二进制编码。 |
| 788 | 8 | partial | 逐项核对 Alon–Pham Theorem 4 的 p 取值范围和多对数常数，并写出从 ℤ/qℤ 到开区间 (2n,4n) 的完整概率事件交集；这可把 n^{3/5+o(1)} 归约整理成可发表的独立引理。 |
| 827 | 8 | promising | 把等半径冲突视为顶点数为 n、边大小 4至6 的超图，计算其可能的独立数下界是否可由局部度进一步提升；首项可检验任务是严格求 M6 的最大共度并试用局部引理或容器法改进 n^{1/5}。 |
| 934 | 8 | promising | 先在 $t=3$ 写出两端 BFS 层的双计数，按奇圈 $C_7$ 是否存在分情；检验无 $C_7$ 情形中交叠项能否直接恢复论文所述精确型界，再定位一般图中奇圈造成的损失。 |
| 950 | 8 | partial | 检验能否对大多数 dyadic 尺度建立统一节省：证明对每个 ε>0，所有充分大 n 都有 ∑_{j≤log₂n}2^{-j}(π(n-2^j)-π(n-2^{j+1}))≤ε log log n；先在可计算范围记录最坏 n 及贡献最大的尺度，以判断障碍来自少数短区间还是跨尺度累积。 |
| 963 | 8 | promising | 对小 r 穷举可实现的有符号关系型（按有理线性同构归类），检验命题：若 B 是 A 中最大耗散集，则 \|A\|≤2^{r+1} 或某个更接近 2^r 的界；先从 r≤5 寻找反例或可归纳结构。 |
| 1063 | 8 | promising | 先形式化并逐例验证下界中的关键引理 S≤M-v_p(k)，尤其覆盖 p^r≤k 且 r>v_p(k) 时区间可有两个 p^r 倍数的情形；随后计算 k≤100 的下界比值 log n_k/k，寻找应按 k 的素因子结构分层表述的估计。 |

## 仓库既有深度项目补充

这五题已有多轮专项证明或形式化工作；以下结论优先于均匀首轮，但仍不构成整题解决声明。

### #866 深度补充

仓库深挖把首个未决案例定位为 k=7：Lean 已验证 $g_7(N)=O(N^{7/8})$；自然语言证明并经独立审计、但尚未 Lean 化的结果为，充分大 N 时 $g_7(N)>\frac1{16}N^{2/3}$。项目明确不声称 #866 已解决；当前核心是必须保留配置结构的逆定理，例如暴露二次因子或精确控制 $R_{10}$ 的碰撞商。

证据：[仓库记录](/home/biostar/work/projects/amra/projects/erdos-866-ai-continuation-20260505/proof/current_focus.md)

### #212 深度补充

深度运行已 Lean 验证反演所得不可约三次曲线、无限有理距离零点集的传递以及射影参数化双射。第一未闭合点是多项式到 $\operatorname{RatFunc}(\mathbb R)$ 参数化的反向核包含/精确核等式，之后才可能建立函数域有理性与属层面的结论；这些局部定理不能改写为整题已解。

证据：[仓库记录](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/runs/erdos212-quadratic-to-irreducible-cubic/erdos212-quadratic-to-irreducible-cubic-supervised-4h/proof_lab/round-026/summary.md)

### #1084 深度补充

深度运行已对水平射线穿越、水平边块的终端线段包含和终端可见性得到声明级无 `sorryAx` 的局部 Lean 结果。下一节点是可见极大水平边块的同侧切触/异侧穿越奇偶分类，随后仍需路径不变性和全局 Jordan 分割；整文件的占位符总数不能替代声明级审计。

证据：[仓库记录](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/runs/erdos1084-polygonal-ray-crossing-parity/erdos1084-polygonal-ray-crossing-parity-supervised-4h/proof_lab/round-011/summary.md)

### #972 深度补充

深度来源审计的第一阻塞点是精确的外部解析数论定理：对每个固定无理数 $\alpha>1$，需证明 $\#\{p<X:p,\lfloor\alpha p\rfloor\ \text{均为素数}\}\gg_\alpha X/(\log X)^2$（或等价相关下界）。普通的 Beatty 序列素数渐近不能替代这个双素数相关。

证据：[仓库记录](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-03/state.json)

### #1052 深度补充

现有计算只给有界盒证据。第一阻塞点是全局旋量因子尾部定理或可执行证书：给出显式截止 B，并证明每个奇 3-Higgs 素数 $p>B$ 的 $\Phi_{4p}(2)$ 都有一个非 3-Higgs 素因子，再附上 $p\le B$ 的完整有限见证表；固定范围计算本身不能控制素因子总数。

证据：[仓库记录](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-02/state.json)


## 逐题记录

### #1

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $A\subseteq \{1,\ldots,N\}$ with $\lvert A\rvert=n$ is such that the subset sums $\sum_{a\in S}a$ are distinct for all $S\subseteq A$ then\[N \gg 2^{n}.\]
- 题意摘要：对象是整数集 A⊆{1,…,N}，|A|=n，且映射 S↦∑_{a∈S}a 在 2^A 上单射。问题问是否存在绝对常数 c>0，使所有这类 A（至少对 n≥1，等价地渐近意义下）均满足 N≥c·2^n；c 不得依赖 n、N、A。
- 状态核对：按冻结日期 2025-08-31，此问题仍为 open。已知精确下界 N≥binom(n,⌊n/2⌋)，仅为 Θ(2^n/√n)。本地 Lean 文件中的主定理 `erdos_1` 仍以 `sorry` 占位，不能视为形式化证明；其编码还额外排除了 N=0，并使用严格不等式。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令 M=max A，并按子集和从小到大取恰好 2^{n-1} 个子集组成 D。因所有权重为正，D 是下闭族。若 T∈∂D，则 T=S∪{i}，其中 S∈D；取 t=max_{S∈D}∑S，可得 t<∑T≤t+M。边界子集和是互异整数，故 |∂D|≤M。Harper 半立方体边界定理给 |∂D|≥binom(n,⌊n/2⌋)，从而 N≥M≥binom(n,⌊n/2⌋)。随后尝试把该特殊加权阈值族的边界下界加强到 Ω(2^n)，但此加强本身为假。
- 局部结论：直接计数给出 2^n≤∑_{a∈A}a+1≤nN+1，因此 N≥(2^n−1)/n。；上述阈值族—边界论证严格推出已知精确下界 N≥binom(n,⌊n/2⌋)∼√(2/π)·2^n/√n；候选答案的这部分论证成立。；候选答案声称“这些特殊阈值族必须有 Ω(2^n) 边界”并不成立。取奇数 n=2m+1、M=2^n、a_i=M+2^{i-1}。不同基数的子集和由 M 分离，同一基数内由二进制部分区分，故全部子集和互异；前一半恰为 |S|≤m，而其外边界只有第 m+1 层，大小 binom(n,m+1)=Θ(2^n/√n)。因此 Erdős 猜想即使为真，也不能仅靠加强这个无权边界数得到。
- 第一阻塞点：第一处无法闭合的是从 |∂D|≥Θ(2^n/√n) 升级到 M≥c2^n。单纯证明 |∂D|=Ω(2^n) 的设想已被上述合法的 sum-distinct 构造否定；必须利用边界子集和之间的算术间距、多个阈值切片或其他额外信息，而不能只数一个半立方体边界。
- 下一步：下一项可检验任务：对多个分位阈值 D_q={S:∑S≤t_q} 建立并验证一个“边界数×边界和跨度”的多尺度不等式；先在 a_i=2^n+2^{i-1} 和 a_i=2^{i-1} 两族上计算该统计量，排除仍只能恢复中心二项式下界的版本，再尝试证明能累计到 Ω(2^n) 的精确命题。形式化方面，可先补齐本地文件中 Harper 半立方体定理的 `sorry`，从而完整核验已知下界，但这不会解决原猜想。
- 来源核对：核对 Dubroff–Fox–Xu 原论文预印本：其 Theorem 3 正是半立方体外顶点边界下界，第二证明推出 a_n≥binom(n,⌊n/2⌋)：[arXiv:2006.12988](https://arxiv.org/abs/2006.12988)。；核对期刊元数据：论文发表于 SIAM Journal on Discrete Mathematics 35 (2021), 322–324，DOI 10.1137/20M1385883。；检查本地 `1.lean`：主猜想及关键 Harper 计数步骤均含 `sorry`；现有辅助引理不构成无条件形式化解决。
- 时间记账：所在批次墙钟时间按题数均摊约 138.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean`；既有候选答案（按不可信材料审计）

### #3

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $A\subseteq \mathbb{N}$ has $\sum_{n\in A}\frac{1}{n}=\infty$ then must $A$ contain arbitrarily long arithmetic progressions?
- 题意摘要：量词为：对每个满足调和子级数发散的集合 A⊆ℕ，以及每个长度 k，A 中都应存在非平凡 k 项等差数列；“任意长”不要求同一数列嵌套。
- 状态核对：按冻结日期 2025-08-31 仍为开放题。长度 3 已知成立，但一般 k 未解决。先前候选对此状态判断基本正确。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：固定 k，反设 A 不含 k 项非平凡等差数列。对二进块 I_j=[2^j,2^{j+1})，有 |A∩I_j|≤r_k(2^{j+1})，故尝试用极值上界控制调和和。
- 局部结论：严格有 ∑_{n∈A∩I_j}1/n≤r_k(2^{j+1})/2^j；因此若 ∑_j r_k(2^j)/2^j<∞，则所有 k-AP-free 集合的倒数和收敛。；特别地，r_k(N)≪N/((log N)(loglog N)^2) 会给出可和上界 ≪1/(j(log j)^2)，足以解决固定 k。；对 k=3，Bloom–Sisask 型越过对数障碍的界足以推出结论；删除任意有限初段仍保持倒数和发散，所以实际上可得到无穷多个彼此不全局限于有限初段的 3 项等差数列。
- 第一阻塞点：一般 k 的现有界代入二进分块后仍不给出可和级数；例如 N/exp((loglog N)^{c_k}) 只产生 exp(-(log j)^{c_k}) 量级，已知参数范围不足以闭合求和。这里正是路线第一次失效之处。
- 下一步：对 LSS 的明确常数范围逐条核算，并尝试改用非二进、自适应分块；可检验目标是证明现有 r_k 上界与某种跨块稀疏性结合后是否仍能推出 ∑|A∩I_j|/2^j<∞。
- 来源核对：已核对本地 3.lean：其量词是对所有 A，最终任意大的 k 均存在长度 k 的等差数列，与原题相容。；冻结官方上下文所列 Bloom–Sisask、Kelley–Meka、Green–Tao、Gowers、Leng–Sah–Sawhney 界均未被误写成一般问题的证明。
- 时间记账：所在批次墙钟时间按题数均摊约 63.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/3)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/3.lean`；既有候选答案（按不可信材料审计）

### #5

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $C\geq 0$. Is there an infinite sequence of $n_i$ such that\[\lim_{i\to \infty}\frac{p_{n_i+1}-p_{n_i}}{\log n_i}=C?\]
- 题意摘要：给定每个实数 C≥0，问是否存在严格趋于无穷的指标子列 n_i，使连续素数间隔 d_{n_i}=p_{n_i+1}-p_{n_i} 满足 d_{n_i}/log n_i→C；等价于所有有限 C 都属于该序列的子列极限集 S。
- 状态核对：按冻结日期仍开放。已知 0∈S、∞∈S、[0,c]⊆S，以及测度和有界空隙结论，都不等于 S=[0,∞]。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试沿“可容许素数元组的缩放位移”路线：在约为 log N 的尺度布置多个候选位置，希望筛法保证其中两个成为相邻素数，并让它们的位移差逼近指定 C。
- 局部结论：由素数定理 log p_n/log n→1，所以用 log p_n 或 log n 归一化具有相同的有限子列极限点。；子列极限集 S 在扩充半直线 [0,∞] 中是闭集：对趋向 S 内各点的序列作对角子列即可。因而“处处稠密”确实等价于 S=[0,∞]。；现有小间隔与大间隔定理分别严格给出 0、∞ 两个端点；Pintz 的结果还给出某个 [0,c]，但闭性、正测度和有界空隙均不能填满其余空档。
- 第一阻塞点：筛法型结果通常只能保证候选位移集合中“某一对”产生相关间隔；无法指定是哪一对，也无法同时排除两端之间的额外素数。因此不能把得到的差强制为预先给定的 C。
- 下一步：选取一个具体 C>c，构造有限可容许位移族 H，使所有可能被筛法选中的相邻差都落在 (C-ε,C+ε)；先以有限组合程序检验这种 H 是否可能，再核对现有素数元组定理是否提供足够的相邻性。
- 来源核对：冻结官方上下文明确列出 Westzynthius、GPY、Pintz、Banks–Freiberg–Maynard、Merikoski 的结论。；先前候选称 log p_n 与 log n“本质等价”；这里已用素数定理补足所需乘法因子趋于 1 的严格理由。
- 时间记账：所在批次墙钟时间按题数均摊约 63.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/5)；既有候选答案（按不可信材料审计）

### #9

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be the set of all odd integers not of the form $p+2^{k}+2^l$ (where $k,l\geq 0$ and $p$ is prime). Is the upper density of $A$ positive?
- 题意摘要：令 A 为所有不存在 p 素数及 k,l≥0 使 n=p+2^k+2^l 的奇正整数。问题是 limsup_{N→∞}|A∩[1,N]|/N 是否严格为正；分母计数全部整数，因此即使所有奇数都异常，上密度也至多 1/2。
- 状态核对：按冻结日期仍开放。已知 |A∩[1,N]|≫_εN^{1-ε} 仍允许其密度趋于 0，不能回答本题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试以奇偶性先压缩表示类型，再用有限模数筛构造一批统一不可表示的剩余类，从而获得正密度异常集。
- 局部结论：若 n 和 p 都为奇数，则 2^k+2^l 必须为偶数，故要么 k,l≥1，要么 k=l=0；若恰有一个指数为 0，则只能有 p=2。；混合指数且 p=2 的表示只产生 O(log N) 个 n≤N；k=l=0 的表示 n=p+2 至多 O(N/log N) 个。因此正密度问题的主要部分可归约到 k,l≥1。；若能找到模数 W 和正比例的奇剩余类 R，使每个 r∈R、每对指数余类都迫使 r-2^k-2^l 被某个固定小素数整除，则除有限个等于该小素数的例外外，R 中整数都属于 A。
- 第一阻塞点：无法构造覆盖全部指数对的有限同余障碍。2^k 在奇模数下周期循环，而不同 (k,l) 所需的素因子条件彼此冲突；现有论证甚至不能得到一个保证不可表示的无限算术级数，更不能得到正比例剩余类。
- 下一步：对小素数集合 Q 和指数周期 L=lcm_{q∈Q}ord_q(2) 做有限 SAT/整数规划搜索：寻找 r mod ∏Q，使每个 (k,l)∈(ℤ/Lℤ)^2 至少有 q∈Q 满足 r≡2^k+2^l mod q；若连续扩大 Q 均不可行，提取不可行证书以识别结构性障碍。
- 来源核对：已核对本地 9.lean：A 同时要求 Odd n，并否定所有 p,k,l 的表示；upperDensity 正是相对于全部自然数。；先前候选正确区分了 N^{1-o(1)} 下界与正密度，但没有提供能跨越该差距的证明。
- 时间记账：所在批次墙钟时间按题数均摊约 63.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/9)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/9.lean`；既有候选答案（按不可信材料审计）

### #10

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some $k$ such that every integer is the sum of a prime and at most $k$ powers of 2?
- 题意摘要：问是否存在一个绝对整数 k，使每个整数 n≥2 都可写成 n=p+∑_{i=1}^j2^{a_i}，其中 p 为素数、0≤j≤k，指数可重复；k 不依赖 n。
- 状态核对：按冻结日期仍开放。Gallagher 的结论只覆盖任意接近 1 的下密度，不能消除最后的零密度异常集。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：沿否定方向固定 k，尝试用覆盖同余系和中国剩余定理构造一个算术级数，使对所有 j≤k 及所有指数元组，n-∑2^{a_i} 都有预定小素因子，因而除有限例外外不可能为素数。
- 局部结论：对固定奇素数 q，正指数的 2^a mod q 只依赖 a mod ord_q(2)，所以固定 k 后同余覆盖问题可化为有限指数余类问题。；若这种有限覆盖存在，则 CRT 给出正模数的算术级数；沿该级数取充分大的 n，可排除“差恰等于其小素因子”的有限例外，从而反驳该固定 k。；若 Granville–Soundararajan 的“每个奇数>1至多三项”猜想成立，则每个偶数 n≥4 可对 n-1 加上一项 2^0，故 k=4 足够；n=2 单独由素数 2 表示。
- 第一阻塞点：有限覆盖尚不能对任意固定 k 构造出来；幂和余类数量随 k 激增，且不同指数元组要求互不相容的 CRT 条件。这正是从 k=1 型覆盖障碍推广到统一 k 时的首个缺口。
- 下一步：先对 k=2、3 建立精确的有限覆盖模型，要求同时涵盖 j=0,1,…,k；输出可机器核验的覆盖表或不可行证书，并特别检查指数 0 与差等于小素数的边界情形。
- 来源核对：已核对本地 10.lean：使用 multiset，允许空和、指数重复，并明确把目标全集写成 ℕ\{0,1}。；先前候选以题 9 的“不是素数加恰好两项 2 的幂”直接断言 k=2 失败，逻辑不足：这些异常数仍可能是素数或素数加一项 2 的幂；必须另行排除 j=0,1。
- 时间记账：所在批次墙钟时间按题数均摊约 63.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/10)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/10.lean`；既有候选答案（按不可信材料审计）

### #12

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be an infinite set such that there are no distinct $a,b,c\in A$ such that $a\mid (b+c)$ and $b,c>a$. Is there such an $A$ with\[\liminf \frac{\lvert A\cap\{1,\ldots,N\}\rvert}{N^{1/2}}>0?\]Does there exist some absolute constant $c>0$ such that there are always infinitely many $N$ with\[\lvert A\cap\{1,\ldots,N\}\rvert<N^{1-c}?\]Is it true that\[\sum_{n\in A}\frac{1}{n}<\infty?\]
- 题意摘要：对象是无限 A⊆ℕ，且不存在互异 a,b,c∈A 满足 b,c>a 及 a∣b+c。三问分别为：(i) 是否存在单个 A 使 liminf_{N→∞}A(N)/√N>0；(ii) 是否存在统一 c>0，使每个此类 A 都在无穷多个 N 上满足 A(N)<N^{1-c}；(iii) 是否每个此类 A 都有 ∑_{n∈A}1/n<∞。
- 状态核对：输入冻结状态把三问整体列为 open。当地文件出现了冻结日期之后的元数据，称前两问已有形式化证明/反证，但当前副本的证明体均为 `sorry`，且未重建所链接证明，故本次不把它们计作已核验解决；第三问在本地仍标 open。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：先验证 p²（p≡3 mod4）构造，再尝试把单个 a 所施加的模 a 禁配条件叠加，以得到计数或调和和上界。
- 局部结论：若 a=p²、b=q²、c=r²，且 p,q,r≡3 mod4 为互异素数，p²∣q²+r² 会给出 (qr^{-1})²≡-1 mod p，和 p≡3 mod4 时 -1 为二次非剩余矛盾；故该素数平方集合确实满足条件。；该构造只有约 √N/log N 个元素，故不能回答第一问；但其倒数和被 ∑_p1/p² 控制而收敛。；固定 a∈A 后，把大于 a 的元素按模 a 分类：对每个非自反配对 {r,-r}，两类不能同时出现；自反类 2r≡0 mod a 中至多出现一个尾部元素。因此仅由一个 a 可严格推出 A 尾部的上密度至多约 1/2。
- 第一阻塞点：不同 a 给出的“选择 r 还是 -r”高度相关，模数又可能有大公因子，不能把各个约 1/2 的损失相乘。于是既得不到统一幂次节省，也得不到二进块计数的可和性；第一问方面，素数平方构造的对数损失也无法在保持非剩余论证时消除。
- 下一步：选取有限 B⊂A，显式计算同时满足所有模 a（a∈B）禁配条件的剩余类最大密度，并将结果按 gcd 图分层；目标是证明当 B 含足够多近互素元素时密度出现可量化乘法衰减，或构造反例说明相关性确实阻断该路线。
- 来源核对：已核对本地 12.lean：`IsGood` 以“若整除且 b,c>a，则 b=c”准确编码 b,c 不得互异。；同一文件把 parts.i 标成 answer(True)、parts.ii 标成 answer(False)，并链接外部提交，但当前仓库仅保留 `sorry`；这只能算待重建的一手线索，不能作为本次证明。；先前候选按冻结资料称三问均开放；其素数平方说明可严格补成二次非剩余论证，但“已知构造接近平方集”的启发不能推出第三问。
- 时间记账：所在批次墙钟时间按题数均摊约 63.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/12)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/12.lean`；既有候选答案（按不可信材料审计）

### #14

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$. Let $B\subseteq \mathbb{N}$ be the set of integers which are representable in exactly one way as the sum of two elements from $A$. Is it true that for all $\epsilon>0$ and large $N$\[\lvert \{1,\ldots,N\}\backslash B\rvert \gg_\epsilon N^{1/2-\epsilon}?\]Is it possible that\[\lvert \{1,\ldots,N\}\backslash B\rvert =o(N^{1/2})?\]
- 题意摘要：对任意固定的集合 $A\subseteq\mathbb N$，令 $r_A(n)$ 为 $n=a+a'$ 的无序表示数（允许 $a=a'$），$B=\{n:r_A(n)=1\}$，$E_A(N)=|[1,N]\setminus B|$。第一问是：是否对每个 $A$、每个 $\varepsilon>0$，最终有 $E_A(N)\ge c_{A,\varepsilon}N^{1/2-\varepsilon}$；第二问是：是否存在单个无限集合 $A$ 使 $E_A(N)/\sqrt N\to0$。若把 $\gg_\varepsilon$ 严格解释为常数不得依赖 $A$，则第一问还要更强；本地形式化采用逐个 $A$ 的 Big-Omega。
- 状态核对：截至 2026-07 官方页仍列为 open。候选材料有两处明确错误：有序“恰好一种”与无序版本并不等价——非对角表示在有序计数下自动出现两次；另外 $N^{1/3-\varepsilon}$ 小于而非“大于”$\sqrt N$。本地 `allUniqueSums` 正确采用交换两项视为同一表示。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：取 $S=A\cap[0,N]$、$s=|S|$，把每个 $n\in B\cap[1,N]$ 映到其唯一无序表示对，尝试把 $E_A(N)$ 很小转化为接近极值的 Sidon 型结构。进一步令 $P_N=\sum_{n\le N}r_A(n)$，按唯一和与异常和分拆表示对。
- 局部结论：唯一表示给出到 $S$ 的无序二元多重子集的单射，故 $N-E_A(N)\le \binom{s+1}{2}$。特别地，若 $E_A(N)=o(\sqrt N)$，则 $|A\cap[0,N]|\ge \sqrt{2N}-\tfrac12-o(1)$。；对每个 $n\le N$ 有 $r_A(n)\le\lceil s/2\rceil$，因此 $P_N\le N-E_A(N)+E_A(N)\lceil s/2\rceil$。这精确表达了所有重复表示只能集中在至多 $E_A(N)$ 个和上。；这些结论只给出 $A$ 的必要密度及碰撞集中性；它们没有给出 $E_A(N)$ 的正下界。
- 第一阻塞点：第一处断点是缺少稳定性定理：从约 $N$ 个不同且唯一的受限二元和，无法推出至少 $N^{1/2-o(1)}$ 个缺失或碰撞的和。经典 Sidon 上界要求所有二元和唯一，而这里允许碰撞任意集中在异常和上，故不能直接套用。
- 下一步：检验一个明确的稳定性命题：若 $S\subset[0,N]$ 且至少 $N-E$ 个 $n\le N$ 各有唯一表示，能否仅用加性能量或 restricted-sum graph 证明 $E\gg N^{1/2}/(\log N)^C$；第一步是对每个 dyadic 层 $S\cap(2^{-j-1}N,2^{-j}N]$ 建立碰撞能量下界。
- 来源核对：[Erdős Problem #14 当前状态与已记录界](https://www.erdosproblems.com/14)；核对本地 `14.lean` 及 `Combinatorics/Basic.lean`：唯一性按无序对定义。；未把 Erdős 未给出处的构造声明当成已重建证明。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/14)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/14.lean`；既有候选答案（按不可信材料审计）

### #15

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that\[\sum_{n=1}^\infty(-1)^n\frac{n}{p_n}\]converges, where $p_n$ is the sequence of primes?
- 题意摘要：令 $p_n$ 为第 $n$ 个素数（$p_1=2$），问题是实数级数 $\sum_{n\ge1}(-1)^n a_n$、$a_n=n/p_n$ 是否收敛；这里只问通常收敛，不问绝对收敛。
- 状态核对：截至 2026-07 仍为 open；Tao 只在强定量 Hardy–Littlewood 素数元组猜想下证明收敛。候选答案的开放状态和非绝对收敛判断正确，但数值极限未在本次筛查中独立核验，故不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把相邻奇偶项配对，并将差分写成素数间隔 $g_n=p_{n+1}-p_n$ 的函数，试图把问题归约为偶、奇编号素数间隔的偏差估计。
- 局部结论：由素数定理 $p_n\sim n\log n$，故 $a_n\sim1/\log n\to0$，而 $\sum a_n$ 发散，所以原级数不绝对收敛。；偶数部分和满足 $S_{2M}=\sum_{m\le M}(a_{2m}-a_{2m-1})$；又因 $a_n\to0$，原级数收敛当且仅当这个配对差级数收敛。；有精确恒等式 $a_{n+1}-a_n=(p_n-ng_n)/(p_np_{n+1})$。因此所需抵消确实涉及 $g_n$ 按编号奇偶性的相关性，而不仅是素数定理。
- 第一阻塞点：现有无条件素数定理或平均间隔估计不控制 $\sum(-1)^n(p_n-ng_n)/(p_np_{n+1})$ 的尾部；取绝对值会丢掉恰好需要的奇偶抵消。这里就是第一处不能闭合的步骤。
- 下一步：严格重建 Tao/Said 的等价变换到 $\sum_{m\ge2}(-1)^{\pi(m)}/(m\log m)$，然后用分部求和验证可检验的充分条件：若 $F(x)=\sum_{m\le x}(-1)^{\pi(m)}=O(x/(\log x)^\delta)$ 对某个 $\delta>0$ 成立，则级数收敛；再明确现有筛法距离该估计多远。
- 来源核对：[Erdős Problem #15 当前状态](https://www.erdosproblems.com/15)；[Tao 2023 原论文页面](https://arxiv.org/abs/2308.07205)：结论明确是强 Hardy–Littlewood 假设下成立。；本地 `15.lean` 的零指标重编号与原级数符号一致。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/15)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/15.lean`；既有候选答案（按不可信材料审计）

### #18

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：We call $m$ practical if every integer $n<m$ is the sum of distinct divisors of $m$. If $m$ is practical then let $h(m)$ be such that $h(m)$ many divisors always suffice. Are there infinitely many practical $m$ such that\[h(m) < (\log\log m)^{O(1)}?\]Is it true that $h(n!)<n^{o(1)}$? Or perhaps even $h(n!)<(\log n)^{O(1)}$?
- 题意摘要：若每个 $1\le r<m$ 都能写成 $m$ 的互异正因子之和，则 $m$ practical；$h(m)$ 是对这些 $r$ 所需最少因子数的最大值。三问分别为：(i) 是否存在 $C>0$ 及无穷多个 practical $m$ 满足 $h(m)<(\log\log m)^C$；(ii) 是否对每个 $\varepsilon>0$ 最终有 $h(n!)<n^\varepsilon$；(iii) 是否存在 $C>0$ 使最终 $h(n!)<(\log n)^C$。
- 状态核对：截至 2026-07 三问仍 open。官方页只记录 Erdős 的 $h(n!)<n$ 与 Vose 的“无穷多个 practical $m$ 满足 $h(m)\ll\sqrt{\log m}$”。候选答案额外声称 Vose 已证 $h(n!)\ll\sqrt n$，本次未从原文或官方记录核实，故不复述；其中小规模数值也未采用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：一方面重建阶乘的递归表示，另一方面用可用因子子集的数量建立信息论下界，以确定 polylog 上界若成立时可能的最小指数。
- 局部结论：若 $q$ 可由 $n!$ 的至多 $h(n!)$ 个互异因子表示，写 $r=(n+1)q+s$、$0\le s<n+1$，把这些因子乘以 $n+1$，并在 $s>0$ 时加入因子 $s$，得到 $(n+1)!$ 的互异因子表示。因此 $h((n+1)!)\le h(n!)+1$，迭代恢复 $h(n!)<n$ 量级。；令 $t=\tau(m)$、$k=h(m)$。覆盖 $1,\dots,m-1$ 至少需要 $m-1$ 个不同因子子集，故 $m-1\le\sum_{j=0}^k\binom tj\le(k+1)t^k$。因 practical 情形可取 $k\le t$，得到 $h(m)\ge \log(m-1)/\log\tau(m)-O(1)$。；已知 $\log\tau(n!)\sim c_0\log(n!)/(\log\log(n!))^2$，$c_0\approx1.25775$；代入得 $h(n!)\ge(c_0^{-1}+o(1))(\log n)^2$。所以任何阶乘 polylog 上界的指数至少为 $2$，但这不否定题目。
- 第一阻塞点：递归每升一级最多增加一个因子，但没有办法把许多连续层合并成只花 $o(1)$ 个新因子的“块递归”；计数下界又只是必要条件，完全不保证短子集和能覆盖连续区间。这是上界路线的首个断点。
- 下一步：选取块长 $L$，尝试证明可检验引理 $h((n+L)!)\le h(n!)+O(L/\log L)$；先在 $L$-smooth 余数上验证能否由 $(n+1),\dots,n+L$ 的因子结构统一编码。即使反例出现，也能定位逐级递归无法摊薄的原因。
- 来源核对：[Erdős Problem #18 当前状态及 Vose 已记录结论](https://www.erdosproblems.com/18)；[Vose, Egyptian Fractions 出版页](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms/17.1.21)；[Erdős–Graham–Ivić–Pomerance：$\tau(n!)$ 渐近式](https://math.dartmouth.edu/~carlp/factorial.pdf)；本地 `18.lean` 的递归构造已逐步核对；其定义额外覆盖 $r=m$，但表示 $m=\{m\}$ 不提高 $h(m)$。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/18)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/18.lean`；既有候选答案（按不可信材料审计）

### #20

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n,k)$ be minimal such that every family $\mathcal{F}$ of $n$-uniform sets with $\lvert \mathcal{F}\rvert \geq f(n,k)$ contains a $k$-sunflower. Is it true that\[f(n,k) < c_k^n\]for some constant $c_k>0$?
- 题意摘要：对固定 $k\ge3$，$k$-sunflower 是 $k$ 个互异集合，其任意两者交集都等于同一个核。$f(n,k)$ 是使每个至少含 $f(n,k)$ 个互异 $n$-元集合的族都含 $k$-sunflower 的最小阈值。问题是：对每个固定 $k$，是否存在仅依赖 $k$ 的 $c_k>0$，使所有 $n\ge1$ 都有 $f(n,k)<c_k^n$。
- 状态核对：截至 2026-07 仍 open，即使 $k=3$ 亦然。当前官方纪录仍为 $f(n,k)<(Ck\log n)^n$。候选答案所述 2025 预印本没有被当前官方页列为已核准纪录，本筛查不把它当成确定的最好界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：重建分块下界与 Erdős–Rado 归纳上界，精确观察归纳中产生超指数 $n!$ 的位置。
- 局部结论：把底集分成 $n$ 个大小为 $k-1$ 的块，取所有“每块恰选一个元素”的集合，共 $(k-1)^n$ 个。若其中 $k$ 个形成 sunflower，则在每个块中所选元素必须全同或两两不同；后者因块仅有 $k-1$ 个元素而不可能，前者又迫使这 $k$ 个集合相同。故 $f(n,k)>(k-1)^n$。；若 $\mathcal F$ 不含 $k$-sunflower，则其最大两两不交子族至多有 $k-1$ 个成员；这些集合的并 $X$ 大小至多 $n(k-1)$，并且击中 $\mathcal F$ 的每个成员。；某个 $x\in X$ 至少属于 $|\mathcal F|/[n(k-1)]$ 个成员。删去这些成员中的 $x$ 后仍是 $(n-1)$-均匀且无 $k$-sunflower，故得到递推 $M(n,k)\le n(k-1)M(n-1,k)$，从而恢复 $n!(k-1)^n$ 型经典界。
- 第一阻塞点：首个断点非常明确：击中集 $X$ 的大小为 $n(k-1)$，每次降维损失一个因子 $n$，迭代即产生 $n!$。要得到 $c_k^n$，必须把平均每层损失降到仅依赖 $k$ 的常数；上述最大不交族论证本身做不到。
- 下一步：检验一个局部替代命题：对无 $k$-sunflower 的 $n$-均匀族，是否总能找到大小 $O_k(1)$ 的集合 $X$，使至少固定比例的成员与 $X$ 相交于同一非空模式。先在“最大不交子族恰为 $k-1$”的模型类中证明或构造反例。
- 来源核对：[Erdős Problem #20 当前状态与 $(Ck\log n)^n$ 纪录](https://www.erdosproblems.com/20)；本地 `20.lean` 核对了阈值量词；其形式化写成一个函数 $c(k)$ 同时覆盖所有 $n,k$。；未将讨论区或未经核准预印本视作开放题的解决。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/20)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/20.lean`；既有候选答案（按不可信材料审计）

### #25

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_1<n_2<\cdots$ be an arbitrary sequence of integers, each with an associated residue class $a_i\pmod{n_i}$. Let $A$ be the set of integers $n$ such that for every $i$ either $n<n_i$ or $n\not\equiv a_i\pmod{n_i}$. Must the logarithmic density of $A$ exist?
- 题意摘要：给定严格递增正整数 $n_1<n_2<\cdots$ 及任意剩余类 $a_i\pmod{n_i}$，定义禁集 $C_i=\{n\ge n_i:n\equiv a_i\pmod{n_i}\}$，$A=\mathbb N\setminus\bigcup_iC_i$。问题是对每一组这样的数据，极限 $\lim_{x\to\infty}(\log x)^{-1}\sum_{n\le x,n\in A}1/n$ 是否必存在。
- 状态核对：截至 2026-07 仍 open。候选答案给出的 $\sum_i1/n_i<\infty$ 特例可以严格闭合；$a_i=0$ 时的倍数集特例也与 Davenport–Erdős 定理一致。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：以有限个禁剩余类的周期集合逼近无限并集，并用尾部的上对数密度控制逼近误差。
- 局部结论：对固定 $K$，$U_K=\bigcup_{i\le K}C_i$ 与一个模 $\operatorname{lcm}(n_1,\dots,n_K)$ 的周期集合只差有限集，故 $U_K$ 及其补集都有自然密度和对数密度。；单个 $C_i$ 的对数密度为 $1/n_i$；由有限/可数并集估计，尾集 $T_K=\bigcup_{i>K}C_i$ 的上对数密度至多 $\sum_{i>K}1/n_i$。；因此若 $\sum_i1/n_i<\infty$，则 $U_K$ 与 $U=\bigcup_iC_i$ 的上下对数密度之差一致趋于零，故 $A$ 的对数密度存在。这对任意剩余类成立。
- 第一阻塞点：在一般情形 $\sum_i1/n_i$ 可发散，尾部并集估计不再趋于零。有限阶段密度虽单调收敛，却不能直接交换“$K\to\infty$”与“$x\to\infty$”；对数密度只具有限可加性，没有所需的从上连续性。这是第一处断点。
- 下一步：按模数分 dyadic 块 $2^j<n_i\le2^{j+1}$，检验能否利用“每个模数至多一个剩余类”和模数互异性，证明尾块并集的调和质量严格优于粗糙和 $\sum1/n_i$；首先计算两剩余类交集为空或密度为 $1/\operatorname{lcm}(n_i,n_j)$，再做二阶 Bonferroni 下的最坏重叠优化。
- 来源核对：[Erdős Problem #25 当前状态](https://www.erdosproblems.com/25)；[Davenport–Erdős 原论文出版记录](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/2/1/93274/on-sequences-of-positive-integers)；本地 `25.lean` 核对了正模数、严格递增及任意整数剩余代表的量词。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/25)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/25.lean`；既有候选答案（按不可信材料审计）

### #28

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $A\subseteq \mathbb{N}$ is such that $A+A$ contains all but finitely many integers then $\limsup 1_A\ast 1_A(n)=\infty$.
- 题意摘要：对象是任意集合 A⊆ℕ。假设存在 n₀，使每个 n≥n₀ 都属于 A+A。令 r_A(n)=#{(a,b)∈A²:a+b=n}，按有序对计数；目标是证明：对每个 K，存在任意大的 n 使 r_A(n)>K。
- 状态核对：截至冻结日仍是 Erdős–Turán 二阶渐近基猜想，不能把已知常数下界或文字性的生成函数讨论当成解决。旧候选正确识别了开放性，但其“limsup≥8”未提供可核验的一手依据，本次不采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：反设存在 K、n₁，使 n≥n₁ 时 r_A(n)≤K；先用覆盖计数夹住 A(N)，再考察生成函数 F(z)=∑_{a∈A}z^a，其中 F(z)²=∑r_A(n)z^n，尝试由系数最终处于 [1,K] 推出矛盾。
- 局部结论：覆盖区间 [N,2N] 至少需要 N+1 个有序表示，故 A(2N)²≥N+1，特别地 A(x)≳√x。；若 r_A(n) 最终≤K，则 A(N)²≤∑_{n≤2N}r_A(n)≤2KN+O(1)，所以 A(N)=O_K(√N)。任何反例都必须处于临界密度 A(N)=Θ(√N)。；交换 (a,b)↔(b,a) 给出 r_A(2m)≡1_A(m) (mod 2)，而 r_A(2m+1) 为正偶数，故充分大的奇数至少有两个有序表示。
- 第一阻塞点：从 F(z)² 的系数最终有界且非零，尚不能推出解析矛盾；普通平均只重现 A(N)=Θ(√N)，没有迫使表示函数出现无界峰值。这正是路线第一次无法闭合处。
- 下一步：在“r_A≤K”假设下，对截断圆周积分 ∫|F(re^{it})|⁴dt 建立带显式边界项的上下界，检验奇偶约束能否使加法能量超过 K∑r_A(n)r^{2n}。
- 来源核对：[Erdős Problems #28](https://www.erdosproblems.com/28)仍将其列为开放题。；已核对本地 Lean 文件：它使用 ℕ∞ 中的 limsup=⊤，与“表示数沿无穷子列无界”等价。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/28)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/28.lean`；既有候选答案（按不可信材料审计）

### #30

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(N)$ be the maximum size of a Sidon set in $\{1,\ldots,N\}$. Is it true that, for every $\epsilon>0$,\[h(N) = N^{1/2}+O_\epsilon(N^\epsilon)?\]
- 题意摘要：h(N) 是 [1,N] 中 Sidon 集的最大基数；Sidon 指无序二元和只有平凡重复。问题要求：对每个固定 ε>0，同时有上下两侧的 |h(N)−√N|≤C_εN^ε，且对所有充分大的 N 成立。
- 状态核对：冻结状态为开放。旧候选主要讨论上界，遗漏了等式还要求 h(N)≥√N−O_ε(N^ε)；Singer 的 (1−o(1))√N 本身不能推出这一误差。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：重建 Erdős–Turán 的短差分法。设 Sidon 集为 a₁<⋯<a_m，并固定 1≤k<m；考察 d_{i,j}=a_{i+j}−a_i（1≤j≤k，1≤i≤m−j）。Sidon 性保证这些正差全部不同。
- 局部结论：差分总数 T=km−k(k+1)/2，故其和至少 T(T+1)/2。；望远镜求和给出 ∑_{j≤k}∑_i(a_{i+j}−a_i)≤N·k(k+1)/2，因此 T(T+1)≤Nk(k+1)。；于是 m≤√(N(k+1)/k)+(k+1)/2；取 k≈N^{1/4} 得 h(N)≤√N+N^{1/4}+O(1)。
- 第一阻塞点：误差来自 √N/k 与 k 两项的平衡；只利用“短差不同”和区间直径时，最优选择必然停在 k≈N^{1/4}。此外该路线完全没有构造任意 N 上误差 N^{o(1)} 的 Sidon 集。
- 下一步：分别检验两端：上界端为短差加入二阶矩/端点分布约束；下界端量化 Singer 构造从素数幂参数 q 转移到任意 N 时的损失，明确它需要何种素数幂间隙界。
- 来源核对：[Erdős Problems #30](https://www.erdosproblems.com/30)确认冻结期记录仍为 N^{1/4} 量级误差。；本地形式化文件表达了大 O 目标，但自然语言中的“对每个 ε>0”仍应作为实际量词标准。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/30)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/30.lean`；既有候选答案（按不可信材料审计）

### #32

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a set $A\subset\mathbb{N}$ such that\[\lvert A\cap\{1,\ldots,N\}\rvert = o((\log N)^2)\]and such that every large integer can be written as $p+a$ for some prime $p$ and $a\in A$? Can the bound $O(\log N)$ be achieved? Must such an $A$ satisfy\[\liminf \frac{\lvert A\cap\{1,\ldots,N\}\rvert}{\log N}> 1?\]
- 题意摘要：寻找固定 A⊆ℕ，使存在 n₀，对每个 n≥n₀ 都有 n=p+a，其中 p 为素数、a∈A。依次询问 A(N)=o(log²N) 是否可行、能否达到 O(log N)，以及每个这种 A 是否满足 liminf A(N)/log N>1。
- 状态核对：前两问在冻结状态下开放；第三问已经由 Ruzsa 解决，且有更强下界 e^γ。不能把“几乎所有整数可表示”的结果用于“除有限多个外全部可表示”。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先检验朴素随机覆盖是否能突破 log²N：在有限区间内以同一概率独立选取候选平移，并对所有待覆盖整数作并合界；同时用素数定理重建必要下界。
- 局部结论：对固定 n，可用的平移约有 π(n)≈n/log n 个；若每个候选以概率 ρ 独立选取，则未覆盖概率至多 exp(−ρπ(n))。要让长度 N 区间的并合界小于1，需要 ρN/log N≳log N，期望选取数因而为 Ω(log²N)。；若 A+P 覆盖所有充分大整数，则 N−O(1)≤(A(N)+1)π(N)。由素数定理得到 liminf A(N)/log N≥1。；已知 Ruzsa 将最后常数严格提高为 e^γ≈1.781，因此第三问答案为“是”。
- 第一阻塞点：独立抽样加逐点并合界固有地产生第二个 log N；表示事件高度相关，目前没有严格的局部引理或去相关估计把“覆盖全部”所需的失败概率降下来。基本计数也只能给常数1，不能自行重建 e^γ。
- 下一步：在一个 dyadic 区间上写出 Erdős 随机构造的精确失败事件，并计算 Janson/负相关界能否利用不同 n 的共享素数平移；若仍产生 log²N，即形成可检验的路线障碍。
- 来源核对：[Erdős Problems #32](https://www.erdosproblems.com/32)明确区分前两问开放与第三问已解。；[Ruzsa 原论文出版页](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/86/3/110177/on-the-additive-completion-of-primes)核对了论文及出版信息。；本地 Lean 文件也分别将 log²、log 两问标作 open，将 e^γ 下界标作 solved。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/32)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/32.lean`；既有候选答案（按不可信材料审计）

### #33

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{N}$ be such that every large integer can be written as $n^2+a$ for some $a\in A$ and $n\geq 0$. What is the smallest possible value of\[\limsup \frac{\lvert A\cap\{1,\ldots,N\}\rvert}{N^{1/2}}?\]Is\[\liminf \frac{\lvert A\cap\{1,\ldots,N\}\rvert}{N^{1/2}}>1?\]
- 题意摘要：A⊆ℕ 满足：存在 M，使每个 m≥M 都可写成 m=n²+a，其中 n≥0、a∈A。第一问取所有这种 A 上 limsup A(N)/√N 的下确界；第二问询问每个 A 是否都有 liminf A(N)/√N>1。
- 状态核对：精确的最小 limsup 在冻结状态下开放；第二问已知为真，甚至 liminf≥4/π。旧候选引用的 2025年12月预印本晚于冻结日，故其额外严格改进不纳入本 cohort。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：对 m≤N 的表示对计数：R(N)=∑_{0≤n≤√N}A(N−n²)，忽略有限例外后 R(N)≥N−O(1)。若 C=limsup A(x)/√x<∞，用 A(x)≤(C+ε)√x 代入，并把和视为四分之一圆的黎曼和。
- 局部结论：粗计数 R(N)≤(√N+1)(A(N)+1) 给出 liminf A(N)/√N≥1。；黎曼和满足 N^{-1}∑_{n≤√N}√(N−n²)→∫₀¹√(1−t²)dt=π/4。；因此 1≤(C+ε)π/4，令 ε→0 得每个补集都有 limsup A(N)/√N≥4/π；结合冻结材料中的构造，目标常数位于 [4/π,2φ^{5/2}]。
- 第一阻塞点：liminf 只提供某些 N 上 A(N) 较小，不能控制所有 A(N−n²)；单调性退化为常数1。要得到严格大于1或4/π，必须定量处理多个表示之间的碰撞，当前计数没有这部分信息。
- 下一步：研究碰撞方程 a₁+x²=a₂+y²，即 a₂−a₁=(x−y)(x+y)，并对固定差 d 用约数函数上界碰撞数，尝试把覆盖所需的 N 个不同和转化为 A(N)>(1+δ)√N。
- 来源核对：[Erdős Problems #33](https://www.erdosproblems.com/33)给出冻结期采用的 4/π 下界和 van Doorn 上界。；本地 Lean 将“充分大整数”改为“所有整数”；加入有限多个例外数即可实现该改写，且不改变归一化 limsup/liminf。；旧候选所引 2025年12月材料晚于 2025-08-31，未用于冻结结论。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/33)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/33.lean`；既有候选答案（按不可信材料审计）

### #36

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find the optimal constant $c>0$ such that the following holds. For all sufficiently large $N$, if $A\sqcup B=\{1,\ldots,2N\}$ is a partition into two equal parts, so that $\lvert A\rvert=\lvert B\rvert=N$, then there is some $x$ such that the number of solutions to $a-b=x$ with $a\in A$ and $b\in B$ is at least $cN$.
- 题意摘要：对每个 N，令 M(N) 为所有等分 [1,2N]=A⊔B 中 max_{x∈ℤ}#{(a,b)∈A×B:a−b=x} 的最小值。题目所求最优常数是 sup{c:充分大 N 均有 M(N)≥cN}=liminf M(N)/N；若已知极限存在，则等于该极限。
- 状态核对：冻结状态下精确值开放，给定记录为 0.379005<c<0.380924。旧候选把端点写成非严格不等式且未说明数值认证细节；当前网页已有冻结日后的更小上界，不能倒灌到本 cohort。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先对差值分布 M_x 作总质量平均，再核验中心区间构造。这里 ∑_xM_x=|A||B|=N²，而可能差值至多4N−1个。
- 局部结论：对任意等分，max_xM_x≥N²/(4N−1)=(1/4+o(1))N，所以 c≥1/4。；当 N 为偶数，取 A={N/2+1,…,3N/2}、B 为两端区间；逐段求交可得每个平移的交叠至多 N/2，故 c≤1/2。；差值平均只使用总质量，没有使用 B=[2N]\A 所产生的自相关/Fourier约束；这解释了它停在1/4。
- 第一阻塞点：要超过1/4，必须证明差值质量不可能接近均匀分布。仅由 ∑M_x=N² 和支撑长度4N−1无法做到；补集关系转化出的 Fourier 非负性约束尚未被利用并闭合。
- 下一步：把 A 的指示函数中心化为 f=1_A−1/2，写出 M_x 与自相关 ∑_nf(n)f(n−x) 的精确恒等式；截取前若干 Fourier 模式，建立一个可用有理算术认证的小型凸规划，先复现 Scherk 下界。
- 来源核对：[Erdős Problems #36](https://www.erdosproblems.com/36)当前仍列为开放；其 2026 更新已晚于冻结日期。；[White 2022 一手预印本](https://arxiv.org/abs/2201.05704)确认其路线是 Fourier 分析转凸优化。；本地 Lean 文件明确记录了极限存在这一已知变体，但正文所求极限值仍为 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/36)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/36.lean`；既有候选答案（按不可信材料审计）

### #38

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Does there exist $B\subset\mathbb{N}$ which is not an additive basis, but is such that for every set $A\subseteq\mathbb{N}$ of Schnirelmann density $\alpha$ and every $N$ there exists $b\in B$ such that\[\lvert (A\cup (A+b))\cap \{1,\ldots,N\}\rvert\geq (\alpha+f(\alpha))N\]where $f(\alpha)>0$ for $0<\alpha <1 $? The Schnirelmann density is defined by\[d_s(A) = \inf_{N\geq 1}\frac{\lvert A\cap\{1,\ldots,N\}\rvert}{N}.\]
- 题意摘要：求证存在同一个集合 B⊆ℕ 和函数 f，使 B 不是任何有限阶的弱加法基，且 f(α)>0（0<α<1）；对每个 A⊆ℕ，令 α=d_s(A)，再对每个 N≥1，都存在可依赖于 A,N 的 b∈B，使 |(A∪(A+b))∩[1,N]|≥(α+f(α))N。
- 状态核对：先验候选称其开放已经过时。官方页现标为肯定解决并经 Lean 核验。本地 cohort 文件的顶层证明仍是 `sorry`，证明证书实际位于其注解链接的外部项目。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建稀疏随机构造：独立地以 p_n≈(log n)^ε/n 选取 n∈B。对 B∩(N/2,N] 的随机 Fourier 和作一致浓缩，再把 Σ_{b∈B}|(A+b)∩([1,N]\A)| 与相应确定性加权和比较；Schnirelmann 下界控制所有初段，最终得到某个 b 带来 ≫α(1−α)^2N 的新增点。
- 局部结论：E|B∩[1,x]|≈Σ_{n≤x}p_n≍(log x)^{1+ε}；经浓缩可固定一个实现，使 B(x) 仅为多对数级。；对任意固定 k，|⋃_{j≤k}jB∩[1,x]|≤(B(x)+1)^k=x^{o(1)}，故不能覆盖所有充分大的整数；B 不是弱加法基。；若能同时对所有大 N、所有频率 θ 建立 sup_θ|\widehat{1_{B_N}}(θ)−\widehat p_N(θ)|=o(|B_N|)，则 Fourier 恒等式把随机平移平均转成确定性加权平移平均，后者给出 f(α)≫α(1−α)^2。
- 第一阻塞点：本次受限重建中第一处不能仅凭上述摘要闭合的是：用网格化、导数控制和尾概率求和，严格证明对所有 N 与连续频率同时成立的一致 Fourier 浓缩，并处理小 N。已链接的 Lean 证明据称完整排除了此缺口，故这不是现存开放步骤。
- 下一步：逐项核验外部 Lean 证明中“一致 Fourier 浓缩”定理的假设、连续频率离散化以及从大 N 扩展到全部 N 的有限修补。
- 来源核对：[官方 #38 页面](https://www.erdosproblems.com/38)标为 PROVED (LEAN)，并给出 f(α)≫α(1−α)^2。；[讨论帖](https://www.erdosproblems.com/forum/thread/38)记录了随机 Fourier 路线及形式化核对。；已检查本地 `38.lean`：陈述使用 `IsWeakAddBasis`，但顶层证明本身为 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 66.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/38)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/38.lean`；既有候选答案（按不可信材料审计）

### #39

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an infinite Sidon set $A\subset \mathbb{N}$ such that\[\lvert A\cap \{1\ldots,N\}\rvert \gg_\epsilon N^{1/2-\epsilon}\]for all $\epsilon>0$?
- 题意摘要：问是否存在一个无限 Sidon 集 A⊆ℕ，使对每个 ε>0，均存在常数 c_ε>0，使所有充分大的 N 满足 A(N):=|A∩[1,N]|≥c_εN^{1/2−ε}。Sidon 指 a+b=c+d 只允许无序对 {a,b}={c,d}。
- 状态核对：仍为开放题；先验候选的开放判断及 Ruzsa 指数与官方资料一致，但其中额外文献断言未在本次筛查中采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试最直接的随机选择加逐个删除冲突：在一个长度 X 的区间中，以 p=X^{-1/2−ε} 独立选点，期望保留 X^{1/2−ε} 个点；然后对每个非平凡等和四元组删除至少一个点。
- 局部结论：区间内满足 a+b=c+d 的候选四元组至多 O(X^3)，故期望冲突数为 O(p^4X^3)=O(X^{1−4ε})。；期望点数为 Xp=X^{1/2−ε}。要让逐冲突删除保留同阶数量，指数比较要求 1−4ε≤1/2−ε，即 ε≥1/6。；因此这一朴素路线至多触及 X^{1/3} 尺度，准确解释了为何独立抽样加一次删除无法逼近平方根指数。
- 第一阻塞点：当 ε<1/6 时，预期冲突数远多于点数；冲突高度相关，逐个删除估计完全失效。尚无可证明的局部修正机制能同时保留 X^{1/2−ε} 个点并消除全部冲突，更不用说兼容无限多个尺度。
- 下一步：把四元组冲突写成随机超图，计算顶点度与余度；检验容器法或半随机 nibble 是否能超越 ε=1/6 阈值，并明确哪一个余度条件首先失败。
- 来源核对：[官方 #39 页面](https://www.erdosproblems.com/39)仍标为 OPEN，并列出当前最佳指数 √2−1+o(1)。；已检查本地 `39.lean`；其量词以渐近 Big-O 形式表达。
- 时间记账：所在批次墙钟时间按题数均摊约 66.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/39)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/39.lean`；既有候选答案（按不可信材料审计）

### #40

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For what functions $g(N)\to \infty$ is it true that\[\lvert A\cap \{1,\ldots,N\}\rvert \gg \frac{N^{1/2}}{g(N)}\]implies $\limsup 1_A\ast 1_A(n)=\infty$?
- 题意摘要：需刻画趋于 +∞ 的函数 g。对给定 g，要求：对每个 A⊆ℕ，只要存在 c>0 使所有充分大的 N 有 A(N)≥c√N/g(N)，就必须有 limsup_{n→∞}r_A(n)=∞，其中 r_A(n)=|(a,b)∈A²:a+b=n|，通常计有序表示。
- 状态核对：仍开放。先验候选有一处逻辑过强：已知反例只排除“g(N)最终至少为某个固定幂”的情形，不能对不规则函数直接推出必要条件 g=N^{o(1)}。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先用有界表示集构造反例区间，再尝试仅靠表示总数平均证明正方向。
- 局部结论：已知对每个固定 ε>0，有 A(N)≫_εN^{1/2−ε} 且 sup_nr_A(n)<∞ 的集合。故若 g(N)≥cN^ε 最终成立，则该 A 满足 √N/g(N)≪N^{1/2−ε}，所求蕴含为假。；令 m=A(N)。恒等式 Σ_{n≤2N}r_{A∩[1,N]}(n)=m² 给出 max_{n≤2N}r_A(n)≥m²/(2N)。代入 m≫√N/g(N)只得到 ≫1/g(N)²，随 N 反而趋零。；若 A 是二阶渐近基，则计数覆盖给出 A(N)≫√N；因此只要对任何一个发散 g 证明所述蕴含，即可推出 Erdős–Turán 猜想。
- 第一阻塞点：总表示数平均完全丢失跨尺度累积信息；密度下界中的 g(N)^{-1} 恰使所得下界退化。需要一种能迫使同一个和获得越来越多表示的跨尺度能量或重叠不等式。
- 下一步：先限定 g 单调，研究 dyadic 能量 E(A∩[1,2^j])，检验假设 Σ_j1/g(2^j)^2=∞ 是否足以通过二阶矩或增量重叠推出无界表示；若失败，记录明确的能量集中反例。
- 来源核对：[官方 #40 页面](https://www.erdosproblems.com/40)仍标为 OPEN，并明确其对 Erdős–Turán 猜想的蕴含。；本地 `40.lean` 形式化了任意函数集合 G，并已形式化“全体 g 情形推出 #28”的归约。
- 时间记账：所在批次墙钟时间按题数均摊约 66.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/40)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/40.lean`；既有候选答案（按不可信材料审计）

### #41

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{N}$ be an infinite set such that the triple sums $a+b+c$ are all distinct for $a,b,c\in A$ (aside from the trivial coincidences). Is it true that\[\liminf \frac{\lvert A\cap \{1,\ldots,N\}\rvert}{N^{1/3}}=0?\]
- 题意摘要：A⊆ℕ 无限，且任意两个来自 A 的三项无序多重集若和相同，则多重集相同；允许重复项。问是否必有 liminf_{N→∞}A(N)/N^{1/3}=0。
- 状态核对：仍开放。需特别注意：本地 `NtupleCondition A 3` 只比较含三个互异元素的 Finset，遗漏 a+a+b 一类重复项，因而弱于原题的 B₃ 条件；该 Lean 陈述不能视为原题的忠实形式化。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试直接计算三重和数目，并检查能否从有限区间上界升级为 liminf 消失。
- 局部结论：若 m=A(N)，则来自 A∩[1,N] 的无序三项多重集共有 C(m+2,3) 个，其和全落在 [3,3N]；故 C(m+2,3)≤3N，得到 m≤(18N)^{1/3}+O(1)。；B₃ 条件蕴含 Sidon 条件：若 a+b=c+d 有非平凡巧合，向两边加入同一个 A 元素便产生非平凡三重和巧合。；计数只给出 A(N)/N^{1/3}=O(1)，即临界尺度常数上界；它没有产生任何趋零子序列。
- 第一阻塞点：从 C(A(N)+2,3)≤3N 到 liminf=0 需要利用不同 N 之间的相容性，而单区间注入计数没有余量。偶数 h 的方法可把和拆成两半并利用二次型结构；h=3 缺少该对称分拆。
- 下一步：以 a_n 为第 n 个元素，把目标改写为 limsup a_n/n³=∞；在 dyadic 块中统计跨块三重和，检验假设 a_n≤Cn³ 最终成立是否迫使两个不同块型的和区间重叠并产生碰撞。
- 来源核对：[官方 #41 页面](https://www.erdosproblems.com/41)仍标为 OPEN；偶数 h 已知，h=3 未解。；已逐字检查本地 `41.lean`，确认其 Finset 定义排除了重复 summand。
- 时间记账：所在批次墙钟时间按题数均摊约 66.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/41)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/41.lean`；既有候选答案（按不可信材料审计）

### #42

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $M\geq 1$ and $N$ be sufficiently large in terms of $M$. Is it true that for every Sidon set $A\subset \{1,\ldots,N\}$ there is another Sidon set $B\subset \{1,\ldots,N\}$ of size $M$ such that $(A-A)\cap(B-B)=\{0\}$?
- 题意摘要：字面量词为：每个 M≥1 存在 N₀(M)，使 N≥N₀ 时，对每个 Sidon 集 A⊆[1,N]，存在 Sidon 集 B⊆[1,N]，|B|=M 且 (A−A)∩(B−B)={0}。
- 状态核对：意图中的“非空 A”版本已解决并经 Lean 核验；但输入的字面陈述遗漏 A≠∅。取 A=∅ 时 A−A=∅，交集不可能等于 {0}。本地 Lean 又只量化极大 Sidon 集，极大性保证非空；因此它没有证明输入的字面全称命题。先验候选既错报开放，也漏掉空集反例。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：对意图版本重建紧 Cayley 图路线：先把非空 Sidon 集扩张为极大 Sidon 集；在允许差集合，即 (A−A)ᶜ 上建 Cayley 图。利用 Sidon 差相关的近正定 Fourier 结构及紧致性得到任意固定大小的团，再从足够大的团中贪心抽取 M 元 Sidon 子集。
- 局部结论：空集给出字面反例：对任意 B，(∅−∅)∩(B−B)=∅≠{0}。；若 A非空，可在有限区间内扩张为极大 Sidon 集 A′；若 B 的非零差避开 A′−A′，则也避开 A−A。故极大版本足以推出非空版本。；若允许差 Cayley 图含一个大小 R 的团 C，则 C−C 的非零部分避开 A−A；按贪心法，每加入第 k 个 Sidon 元素只禁掉 O(k³) 个候选，故 R=O(M⁴) 已足以从 C 抽出 M 元 Sidon 集。
- 第一阻塞点：字面命题无法闭合，因为 A=∅ 是决定性反例。对修正后的非空版本，受限重建中最难的步骤是严格证明有限 Cayley 图团引理；外部 Lean 证明已承担这一环节。
- 下一步：冻结陈述前加入 A.Nonempty，或明确“Sidon 集”按约定非空；随后核对外部 Lean 的紧 Cayley 引理，并把“极大版本推出任意非空版本”的有限扩张引理纳入本地文件。
- 来源核对：[官方 #42 页面](https://www.erdosproblems.com/42)标为 SOLVED (LEAN)。；[讨论帖](https://www.erdosproblems.com/forum/thread/42)明确出现“non-empty Sidon set”版本及紧 Cayley/Fourier 路线。；本地 `42.lean` 的已解决定理只假设 `IsMaximalSidonSetIn A N`，顶层仍以 `sorry` 引用外部形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 66.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/42)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/42.lean`；既有候选答案（按不可信材料审计）

### #43

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：If $A,B\subset \{1,\ldots,N\}$ are two Sidon sets such that $(A-A)\cap(B-B)=\{0\}$ then is it true that\[ \binom{\lvert A\rvert}{2}+\binom{\lvert B\rvert}{2}\leq\binom{f(N)}{2}+O(1),\]where $f(N)$ is the maximum possible size of a Sidon set in $\{1,\ldots,N\}$? If $\lvert A\rvert=\lvert B\rvert$ then can this bound be improved to\[\binom{\lvert A\rvert}{2}+\binom{\lvert B\rvert}{2}\leq (1-c+o(1))\binom{f(N)}{2}\]for some constant $c>0$?
- 题意摘要：对象为任意整数 N≥1 及 Sidon 集 A,B⊆[N]，且两个有向差集仅交于 0。第一问询问是否存在与 N,A,B 无关的常数 K，使充分大 N 时两项无序差数之和不超过 binom(f(N),2)+K。第二问在 |A|=|B| 时询问是否存在绝对常数 c>0，得到渐近固定比例节省。
- 状态核对：两问均已有反例。输入中的旧候选错误地称第一问仍开放；官网现明确说明：问题42的构造可令 |A|=f(N) 而 |B|→∞，故第一问也为否。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建两条反例路线。第一问：反设存在误差常数 K，取固定 m 使 binom(m,2)>K；问题42的已验证结论保证，当 N 足够大时，对极大 Sidon 集 A⊆[N]（|A|=f(N)），存在 |B|=m 且差集互斥的 Sidon 集 B，于是立即超过该上界。第二问：取奇素数幂 q、M=q²−1=2N 及模 M 的 q 元 Bose–Chowla Sidon 集 S；按奇偶拆分、等量截取并除以 2，得到 [N] 中的 A,B。
- 局部结论：第一问中，lhs=binom(f(N),2)+binom(m,2)>binom(f(N),2)+K，严格否定任何统一 O(1) 上界。；若偶、奇部分大小分别为 a,b，则所有同奇偶的非零有向差互异且落在 N−1 个非零偶剩余类中，故 a(a−1)+b(b−1)≤N−1，进而 (a−b)²≤2q−3。；取 m=min(a,b)=q/2−O(√q) 后，所得 A,B 等大、差集仅交于 0，且 2binom(m,2)=N/2+O(N^(3/4))=(1−o(1))binom(f(N),2)，排除任意固定 c>0。
- 第一阻塞点：没有未闭合步骤；第一问依赖问题42已经建立并形式化核验的定理，第二问的模 Sidon 奇偶拆分计数可逐行闭合。
- 下一步：将“问题42 ⇒ 第一问反例”的量词展开形式化：给定 K，先选 m，再取适用于该 m 的阈值 N₀，并实例化到每个 N≥N₀ 的极大 Sidon 集。
- 来源核对：[问题43官方页](https://www.erdosproblems.com/43) 已于2026-05-10标为 disproved，并明确写出第一问由问题42否定。；[问题42官方页](https://www.erdosproblems.com/42) 记录全体固定 m 的结论已在 Lean 中验证。；[问题43讨论中的完整奇偶拆分证明](https://www.erdosproblems.com/forum/thread/43) 给出 (a−b)²≤2q−3 及最终渐近式。
- 时间记账：所在批次墙钟时间按题数均摊约 43.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/43)；既有候选答案（按不可信材料审计）

### #44

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $N\geq 1$ and $A\subset \{1,\ldots,N\}$ be a Sidon set. Is it true that, for any $\epsilon>0$, there exist $M$ and $B\subset \{N+1,\ldots,M\}$ (which may depend on $N,A,\epsilon$) such that $A\cup B\subset \{1,\ldots,M\}$ is a Sidon set of size at least $(1-\epsilon)M^{1/2}$?
- 题意摘要：量词为：对每个 N≥1、每个 Sidon 集 A⊆[N]、每个 ε>0，允许依赖于 N,A,ε 选择某个 M>N 及 B⊆{N+1,…,M}，要求 A∪B 仍为 Sidon 集且 |A∪B|≥(1−ε)√M。并非要求同一个 M 对所有 A 或 ε 有效。
- 状态核对：仍开放。旧候选提及的“放到很右侧可得约 1/√2 常数”可以严格重建；但关于完美差集的材料并不能解决本题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：取很大的长度 X，选 S⊆[X] 为大小 (1−o(1))√X 的 Sidon 集。令 D=(A−A)\{0}。因 S 为 Sidon 集，每个固定 d∈D 至多由一个有向对表示；删除每个坏表示的一个端点，得到 S'，满足 |S'|≥|S|−|D|，且 (S'−S')∩D=∅。再取 L>X+N，并令 B=L+S'，使 A+A、A+B、B+B 位于互不相交的数值区间。
- 局部结论：删除至多 |D|≤|A|(|A|−1) 个元素后，S'仍有 √X−O_A(1) 个元素，且 A+B 内部表示唯一。；L>X+N 保证 max(A+B)<min(B+B)，而 L>2N 也分离 A+A 与 A+B；结合 A、S' 各自 Sidon，A∪B 为 Sidon 集。；取 L=X+N+1、M=L+X，可得 |A∪B|≥(1/√2−o(1))√M。这验证了旧候选所称的弱常数路线。
- 第一阻塞点：区间分离迫使 M≈2X，因此该具体路线天然损失因子 1/√2；要达到 1−ε，必须允许三个和集区间重叠并同时控制 A+B 与 B+B 的碰撞，现有删除论证做不到。
- 下一步：检验能否用模循环 Sidon 集替代区间分离：对固定有限约束 D=A−A，证明存在近满大小的循环 Sidon 集及一个切口，使提升到整数后既避开 D，又只删除 o(√M) 个绕回碰撞。
- 来源核对：[问题44官方页](https://www.erdosproblems.com/44) 确认上述全称—存在量词及开放状态。；本地 [44.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/44.lean) 的主陈述与原题量词基本一致。
- 时间记账：所在批次墙钟时间按题数均摊约 43.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/44)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/44.lean`；既有候选答案（按不可信材料审计）

### #50

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Schoenberg proved that for every $c\in [0,1]$ the density of\[\{ n\in \mathbb{N} : \phi(n)<cn\}\]exists. Let this density be denoted by $f(c)$. Is it true that there are no $x$ such that $f'(x)$ exists and is positive?
- 题意摘要：令 f(c) 为 φ(n)/n<c 的自然密度，定义域为 c∈[0,1]。问题询问是否不存在 x（自然解释为区间内部 x∈(0,1)）使通常双侧导数存在且 0<f'(x)<∞；端点若包括在内则必须另行指定单侧导数。
- 状态核对：仍开放。已知“纯奇异”只推出 f'(x)=0 几乎处处，不能排除零测集上存在有限正导数。旧候选在这一核心点上是审慎的，但其关于特定点右导数无穷的附加说法未由给定官方材料核实，故不作为本次推导依据。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `medium`
- 尝试路线：把极限分布写成随机 Euler 乘积 X=∏p(1−1/p)^{ξ_p}，其中 ξ_p 独立且 P(ξ_p=1)=1/p；有限素数整除事件的自然密度给出这一模型。尝试对单个素数 p 条件化，以获得局部缩放恒等式，进而排除有限正斜率。
- 局部结论：因 Σp E|ξ_p log(1−1/p)|<∞，随机乘积几乎处处收敛；其分布函数就是 f。；若 F_p 是删去因子 p 后乘积的分布函数，则严格有 f(x)=(1−1/p)F_p(x)+(1/p)F_p(x/(1−1/p))。；纯奇异性结合单调函数定理只给出 f'=0 几乎处处；逻辑上与某个例外点满足 0<f'(x)<∞ 完全相容。
- 第一阻塞点：第一处缺口是无法把随 p 变化的 F_p 的局部增量统一换回 f 的局部增量。没有这种定量稳定性，缩放恒等式不能迫使一个假设的有限正导数复制成矛盾的局部质量。
- 下一步：固定候选 x，数值并理论估计 sup_{|h|≤p⁻²}|[F_p(x+h)−F_p(x)]−[f(x+h)−f(x)]|，目标是得到比 h/p 更小的统一误差；若失败，可明确否定该条件化路线。
- 来源核对：[问题50官方页](https://www.erdosproblems.com/50) 只记录开放状态及 Erdős 的纯奇异性结果。；本地 [50.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/50.lean) 存在形式化瑕疵：它只约束 f 在 [0,1] 上的密度值，却禁止全实轴任何点出现正导数；在区间外修改延拓即可反驳该 Lean 陈述，故不能视为原题的准确形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 43.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/50)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/50.lean`；既有候选答案（按不可信材料审计）

### #51

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an infinite set $A\subset \mathbb{N}$ such that for every $a\in A$ there is an integer $n$ such that $\phi(n)=a$, and yet if $n_a$ is the smallest such integer then $n_a/a\to \infty$ as $a\to\infty$?
- 题意摘要：设 T={a∈N:∃n,φ(n)=a}，并对 a∈T 定义 g(a)=min{n:φ(n)=a}。问题等价于：g(a)/a 在 totient 集 T 上是否无界；若无界，可递归选取互异 a_k 使 g(a_k)/a_k>k，形成所求无限集并沿 a_k→∞ 发散。
- 状态核对：仍开放。旧候选关于“甚至 C=3 也未知”等具体文献断言未在官方上下文中得到支持，本筛查不采纳。
- 初步判定：`blocked`；证明尝试：`failed`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试用 primorial 原像制造大比值：令 P_y=∏_{p≤y}p，a_y=φ(P_y)=∏_{p≤y}(p−1)。已知 P_y/a_y=∏_{p≤y}p/(p−1) 渐增，故这个显式原像具有大比值；再尝试证明它是最小原像或所有原像也有大比值。
- 局部结论：a_y 确为 totient，且 g(a_y)≤P_y，因此 primorial 只给出 g(a_y)/a_y≤P_y/φ(P_y)，方向是上界而非所需下界。；任意解 n=∏p^{e_p} 必须满足 a=∏p^{e_p−1}(p−1)，且 n/a=∏_{p|n}p/(p−1)；问题因此归约为排除所有支持过小的这种乘法分解。；若能对每个 C 构造一个 a，使所有分解 a=∏p^{e_p−1}(p−1) 对应的素数支持均满足 ∏p/(p−1)>C，则可递归得到原题所需无限集。
- 第一阻塞点：primorial 构造不能阻止 a_y 还有另一个更小原像；因各 p−1 之间大量共享因子，当前没有唯一分解或强制包含许多小素数的机制。这正是路线中首个方向性失败。
- 下一步：实现并证明完备的逆 totient 递归枚举：对候选 a，利用 p−1|a 逐层枚举所有可能素数 p 和指数 e；先检验 primorial 型 a_y 是否很快出现小原像，并从失败分解中寻找可加入的同余障碍。
- 来源核对：[问题51官方页](https://www.erdosproblems.com/51) 确认开放状态及最小原像的原始量词。；本地 [51.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/51.lean) 用 subtype A 上的 atTop 表达趋于无穷；这隐含按 a 的数值趋于无穷，基本符合原题。
- 时间记账：所在批次墙钟时间按题数均摊约 43.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/51)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/51.lean`；既有候选答案（按不可信材料审计）

### #52

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be a finite set of integers. Is it true that for every $\epsilon>0$\[\max( \lvert A+A\rvert,\lvert AA\rvert)\gg_\epsilon \lvert A\rvert^{2-\epsilon}?\]
- 题意摘要：对每个 ε>0，应存在仅依赖 ε 的常数 Cε>0，使每个有限整数集 A 都满足 max(|A+A|,|AA|)≥Cε|A|^{2−ε}。小规模集合可吸收进常数；核心为 |A|→∞。
- 状态核对：整数版本仍开放。输入官方上下文中的 1270/951 记录已过时；当前官方页记录 Cushman 的 1962/1469≈1.3356。旧候选给出的等价指数 4/3+10/4407 与此相同。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建乘法能量路线。先去掉 0 并取同号子集，损失至多常数因子，从而可设 A⊂R_{>0}、|A|=n。令 Q=max(|A+A|,|AA|)。由 Cauchy–Schwarz，乘法能量 E×(A)≥n⁴/|AA|≥n⁴/Q；再代入 Solymosi 型上界 E×(A)≪|A+A|²log n≤Q²log n。
- 局部结论：两能量界合并给 n⁴/Q≪Q²log n，故 Q≳n^(4/3)(log n)^(−1/3)。；该结论已经严格超过任意 n^(4/3−δ)，但与要求的 n^(2−ε) 尚有巨大差距。；若能把能量上界中的 |A+A|² 改成 |A+A|^{1+o(1)}n^{o(1)}，同一代数框架才可能接近二次指数。
- 第一阻塞点：首个无法闭合处是乘法能量的上界指数 2：现有几何排序/相邻斜率论证天然产生约 |A+A|² 个容器。仅优化对数因子不会把最终指数从 4/3 推向 2。
- 下一步：在附加假设 |A+A|≤n^{2−ε} 下，检验是否能按乘法倍数类分层，把 E×(A) 的上界改写为 o(n⁴/|AA|)；具体先对高重数比值集合 {r:|A∩rA|≥τ} 建立依赖 doubling 常数的尾界。
- 来源核对：[问题52官方页](https://www.erdosproblems.com/52) 于2026-05-28仍标为 open，并记录当前指数 1962/1469。；[Cushman 预印本](https://arxiv.org/abs/2512.13849) 的摘要给出 4/3+10/4407−ε，与 1962/1469−ε 相等。；本地 [52.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/52.lean) 将 ε 限为 0<ε<1；ε≥1 的情形较弱，可由调整常数补出，因此不改变实质。
- 时间记账：所在批次墙钟时间按题数均摊约 43.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/52)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/52.lean`；既有候选答案（按不可信材料审计）

### #60

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does every graph on $n$ vertices with $>\mathrm{ex}(n;C_4)$ edges contain $\gg n^{1/2}$ many copies of $C_4$?
- 题意摘要：量词为：是否存在绝对常数 c>0、n₀，使每个 n≥n₀ 及每个 n 顶点简单图 G，只要 e(G)>ex(n,C₄)，就含至少 c√n 个不同的 C₄ 副本。因可删边至恰有 ex(n,C₄)+1 条边，研究该临界层已足够。
- 状态核对：截至所核来源仍为一般情形开放；He–Ma–Yang 只确认了无限多个有限几何参数。先前候选中“加任意缺边恰产生 q−1、q 或 q+1 个四圈”等精确说法未获所查来源支持，故不采用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：取临界图，并以共邻数 d(x,y)=|N(x)∩N(y)| 双计数。若从一个极值 C₄-free 图 H 加缺边 uv，则新四圈数正是 H 中 u、v 之间三边路的条数，即 e_H(N_H(u),N_H(v))；尝试由极值性迫使该量为 Ω(√n)。
- 局部结论：恒等式严格成立：#C₄(G)=½∑_{\{x,y\}} binom(d(x,y),2)，因为每个四圈有两对对顶点。；∑_{\{x,y\}}d(x,y)=∑_v binom(d(v),2)；结合凸性可在边数显著超过 n^{3/2} 尺度时给出通常的 supersaturation 下界。；若 H 是 C₄-free，则任意两点至多一个共邻；加 uv 后所有新 C₄ 必含 uv，并与 H 中的三边 u-v 路一一对应。
- 第一阻塞点：在 e=ex(n,C₄)+1 的精确阈值，共邻数的平均值约为 1；凸性误差远大于“一条边”的超额。极值性只能保证每个缺边至少闭合一个四圈（对饱和极值图），不能推出 e_H(N(u),N(v))≥c√n。这是该路线第一处无法闭合之处。
- 下一步：对所有 C₄-free 极值图 H 检验命题 min_{uv∉E(H)} e_H(N(u),N(v))=Ω(√n)，先在已知 polarity 图及小阶极值图上精确计算；若失败，所得缺边即给出该“加边路线”的反例结构。
- 来源核对：[He–Ma–Yang 论文摘要](https://arxiv.org/abs/1912.00986)明确称一般猜想开放，并只确认无限多个 n。；其结果给出 n=q²+q+1 附近的 stability/supersaturation，而不是一般 n 的上述缺边局部下界。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/60)；既有候选答案（按不可信材料审计）

### #61

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any graph $H$ is there some $c=c(H)>0$ such that every graph $G$ on $n$ vertices that does not contain $H$ as an induced subgraph contains either a complete graph or independent set on $\geq n^c$ vertices?
- 题意摘要：对每个固定有限简单图 H，要求存在只依赖 H 的 c(H)>0，使每个不含 H 的诱导副本的 n 顶点图 G 都满足 max{ω(G),α(G)}≥n^{c(H)}（等价地可只要求充分大的 n）。
- 状态核对：这是一般 Erdős–Hajnal 猜想，仍开放。所查一般最好界为 exp(c_H√(log n·log log n))，仍是 n^{o(1)}。Lean 文件正确把 H 固定为任意有限类型上的图，并用单射 comap 表达诱导嵌入；它采用“最终对所有 n”版本，与通常渐近表述一致。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试强化 Rödl/密度路线：在每个足够大的诱导子图中寻找两个线性大小、彼此完全相连或完全不相连的顶点集，再递归构造大型 cograph；cograph 中必有大小至少平方根级的 clique 或 stable set。
- 局部结论：补图对称：H 的结论与 complement(H) 的结论等价，因为诱导禁图、clique 和 independent set 同时互换。；若能在 H-free 图中找到含 n^δ 个顶点的诱导 cograph，则该 cograph 的递归并/连接分解给出 max{ω,α}≥n^{δ/2}。；因此问题可具体归约为：证明一般 H-free 图含多项式大小的诱导 cograph；BNSS 的现有路线确实以 cograph 参数组织一般次多项式界。
- 第一阻塞点：现有密度定理只保证一个较大且很稀或很密的诱导子图，不能把“稀/密”升级为两块之间完全无边/全有边，同时仍保持多项式规模。正是这一升级才会把递归深度从次多项式提高到固定幂。
- 下一步：固定最小未解决的 H，检验一个可证伪的局部引理：每个 H-free 图是否含大小至少 n^δ 的诱导 cograph；先通过随机/代数 H-free 构造估计其最大诱导 cograph，确定该归约是否可能成立。
- 来源核对：[BNSS 原论文](https://arxiv.org/abs/2301.10147)给出 exp(c√(log n log log n))，并明确说明其归纳需要控制少量诱导 H 副本。；本地 [61.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/61.lean) 的量词及诱导嵌入编码已核对。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/61)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/61.lean`；既有候选答案（按不可信材料审计）

### #62

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G_1,G_2$ are two graphs with chromatic number $\aleph_1$ then must there exist a graph $G$ whose chromatic number is $4$ (or even $\aleph_0$) which is a subgraph of both $G_1$ and $G_2$?
- 题意摘要：给定任意两个可能无限的简单图 G₁,G₂，且 χ(G₁)=χ(G₂)=ℵ₁，是否存在同一个图 H 分别嵌入为二者的普通子图，并满足 χ(H)=4？更强问题要求 χ(H)=ℵ₀。这里不是诱导子图。
- 状态核对：两问仍开放；不是已知的 ZFC 独立性问题。先前候选所说“总有共同的充分长奇圈”与官方背景相符，但不能由此跃迁到色数 4。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把每个 G 的有限色谱 S₄(G) 定义为其中所有有限 4-临界子图的同构型，尝试证明 S₄(G₁)∩S₄(G₂)非空；利用 de Bruijn–Erdős 紧致性和已知的强制奇圈定理。
- 局部结论：χ(G)=ℵ₁ 蕴含 G 含任意大有限色数的有限子图：否则所有有限子图可用某固定 k 色，紧致性会使 G 也可 k 色。；从色数至少 4 的有限子图逐条删边，可在色数首次降到 4 时取得一个有限 4-色子图，再取 4-临界子图；故每个 S₄(G_i)均非空。；Erdős–Hajnal–Shelah 定理给每个 G_i 一个阈值，超过两阈值的任一奇圈都同时出现，故共同色数 3 子图严格成立。
- 第一阻塞点：两个非空、甚至各自无限的可数同构型集合不必相交；紧致性只在单个图内产生高色有限子图，完全不控制其同构型。没有已知的有限 4-色图族被每个 ℵ₁-色图共同强制。
- 下一步：枚举有限 4-临界图族 F_g（例如按 girth 分层），检验较弱陈述：是否存在 g，使每个 ℵ₁-色图都包含某个 girth≥g 的 F∈F_g；并研究两图所对应强制谱能否由有限阻碍集分离。
- 来源核对：[Erdős Problem 62 页面](https://www.erdosproblems.com/62)在 2026 年仍列为 open，并记录共同充分长奇圈的 EHS74 结果。；未发现来源支持先前候选额外声称的“所有有限二部图恰为普遍强制图”这一完整分类，故本筛查不依赖该说法。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/62)；既有候选答案（按不可信材料审计）

### #65

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph with $n$ vertices and $kn$ edges, and $a_1<a_2<\cdots $ be the lengths of cycles in $G$. Is it true that\[\sum\frac{1}{a_i}\gg \log k?\]Is the sum $\sum\frac{1}{a_i}$ minimised when $G$ is a complete bipartite graph?
- 题意摘要：令 C(G)={a₁<a₂<…}为 G 中出现过的不同简单圈长度，而非圈副本的多重集。对 n 顶点、kn 条边的图，第一问要求 ∑_{a∈C(G)}1/a≥c log k；第二问询问相同密度约束下完全二部图是否给出精确最小值。
- 状态核对：第一问已解决，第二问仍开放。完全二部图的“精确极小”需说明参数匹配：给定任意 n,k 未必存在恰有 kn 条边且无孤点的 K_{a,b}；自然极值函数通常允许密度至少 k，或允许加孤立点。先前候选把 K_{t,t} 的平均度与 k 混同：其平均度为 t，但本题 k=e/n=t/2。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建已知下界的骨架：由平均度 2k 抽取最小度 Ω(k) 的子图，再用扩张子图中的可调路径产生长区间的偶圈长度；该区间的倒数和给出对数项。同时直接计算完全二部图的值以核对常数。
- 局部结论：反复删除度小于 k 的顶点，剩余图非空且最小度至少 k；否则删去总边数小于 kn，与原有 kn 条边矛盾。；K_{s,t}（s≤t）的圈长恰为 4,6,…,2s，故其和为 ½(H_s−1)。特别地 K_{2k,2k} 有 n=4k、e=kn，和为 ½(H_{2k}−1)=½log k+O(1)。；GKS 定理严格给出 Ω(log k)；Liu–Montgomery 的平均度—偶圈方法把首项提高到 (1/2−o(1))log k，与上述族渐近匹配。
- 第一阻塞点：扩张/可调路径定理只控制总和的渐近下界，不给等号结构。要证明精确极小，还须说明任何奇圈、缺失的偶圈或不平衡度序列都会使倒数和至少达到某个具体 K_{s,t} 的值；现有论证没有这种稳定性加离散比较。
- 下一步：先把第二问形式化为明确的极值函数 f(k)=inf{∑1/a: e(G)/v(G)≥k}，计算小 k 的所有极小圈长谱；检验“极小图可取二部且 complete bipartite”这两个独立的压缩引理，寻找最先失败者。
- 来源核对：[GKS 后续论文的原始扫描件](https://www.renyi.hu/~gyarfas/Cikkek/21_GyarfasPromelSzemerediVoigt_OnTheSumOfTheReciprocalsOfCycleLengthInSparseGraphs.pdf)明确记录 GKS 已证明对数级下界。；[Liu–Montgomery 论文](https://arxiv.org/abs/2010.15802)包含“平均度与偶圈长度”部分；其摘要主定理另述色数与奇圈，不能把两者混为同一命题。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/65)；既有候选答案（按不可信材料审计）

### #66

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there $A\subseteq \mathbb{N}$ such that\[\lim_{n\to \infty}\frac{1_A\ast 1_A(n)}{\log n}\]exists and is $\neq 0$?
- 题意摘要：求是否存在 A⊆ℕ及常数 c≠0，使有序表示函数 r_A(n)=∑_{j=0}^n1_A(j)1_A(n−j)满足 r_A(n)/log n→c，对全部充分大的 n 成立，不允许删去零密度异常集。因 r_A(n)≥0，若极限非零则必有 c>0。
- 状态核对：仍开放。Lean 文件使用 atTop 的普通逐点极限和 sumRep，量词与原题一致。已有围绕 log n 的 √log n 级障碍不足以排除 r_A(n)=c log n+o(log n)。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：假设该极限存在，令 F(z)=∑_{a∈A}z^a。由 F(z)^2=∑_nr_A(n)z^n，先做 Abel 变换，再以非负系数的 Karamata Tauber 定理反推出 A 的计数函数必须具有精确渐近式，尝试再从整数/傅里叶波动推出矛盾。
- 局部结论：由 r_A(n)∼c log n，Abel 求和给 F(z)^2∼c(1−z)^{-1}log(1/(1−z))，故 F(z)∼√c(1−z)^{-1/2}√log(1/(1−z))。；对非负系数应用 Karamata 定理可得 A(x)=|A∩[0,x]|∼(2√c/√π)√(x log x)。这是任何候选 A 必须满足的刚性必要条件。；较初等地，∑_{n≤N}r_A(n)∼cNlog N，且 A(N/2)^2≤∑_{n≤N}r_A(n)≤A(N)^2，已可推出 A(N)=Θ(√(Nlog N))。
- 第一阻塞点：径向生成函数只看平均增长，不能控制单位圆附近的非径向值；而逐点卷积的振荡正编码在那里。现有 Erdős–Fuchs 型均方障碍达到 √log n 尺度，却与允许的 o(log n) 误差相容，因此尚不能产生矛盾。
- 下一步：在必要渐近 A(x)∼(2√c/√π)√(xlog x) 下，计算 F(re^{it})²在 t≈1/N 的 L² 下界，并检验能否强迫某个系数误差 |r_A(n)−c log n|≥ε log n；若只能得到 Ω(√log n)，则明确证明该傅里叶路线的上限。
- 来源核对：本地 [66.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/66.lean) 确认使用有序加法表示函数的逐点极限。；官方给定背景中的 Erdős–Sárközy 与 Horváth 结论均只排除更小的 √log n 级误差，逻辑上不否定本题所需的 o(log n)。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/66)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/66.lean`；既有候选答案（按不可信材料审计）

### #68

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is\[\sum_{n\geq 2}\frac{1}{n!-1}\]irrational?
- 题意摘要：令 $S=\sum_{n=2}^{\infty}(n!-1)^{-1}$；问题是不存在 $p\in\mathbb Z,q\in\mathbb N_{>0}$ 使 $S=p/q$。正项级数绝对收敛。
- 状态核对：截至核查时官方仍列为 open。旧候选只报告状态，没有作证明尝试。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：采用“假设有理并清除前缀分母”的经典路线。令 $S_N=\sum_{n=2}^N1/(n!-1)$，$D_N=\operatorname{lcm}_{2\le n\le N}(n!-1)$。若 $S=p/q$，则 $x_N=qD_N(S-S_N)$ 是正整数。再尝试用阶乘尾项使 $x_N<1$。
- 局部结论：几何展开严格成立：$1/(n!-1)=\sum_{k\ge1}(n!)^{-k}$；因各项非负，可交换两重求和。；设 $T_N=S-S_N$。由 $a_{n+1}/a_n<1/n$ 可得 $T_N=(1+O(1/N))/((N+1)!-1)$。；有理性假设严格推出 $qD_NT_N\in\mathbb Z_{>0}$，故必须有 $qD_NT_N\ge1$。
- 第一阻塞点：要矛盾需沿某个无穷子列证明 $D_N=o((N+1)!)$（至少需 $qD_NT_N<1$）。但现有直接估计只有 $D_N\le\prod_{n\le N}(n!-1)$，远大于尾项倒数；各数 $n!-1$ 的公因子结构不足以给出所需上界。这是该路线第一处无法闭合之处。
- 下一步：计算并因式分解中等范围内的 $D_N$，检验 $\log D_N$ 相对 $\log((N+1)!)$ 的增长；若其明显超线性，则正式淘汰此清分母路线，转而研究双重级数中固定 $k$ 层的线性形式。
- 来源核对：[Erdős Problem 68](https://www.erdosproblems.com/68) 仍标为 OPEN，并记载相同双重级数恒等式。；本地 Lean 文件核对了求和指标为 $n+2$，并已形式化证明几何展开恒等式；研究命题本身仍为 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 77.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/68)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/68.lean`；既有候选答案（按不可信材料审计）

### #70

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\mathfrak{c}$ be the ordinal of the real numbers, $\beta$ be any countable ordinal, and $2\leq n<\omega$. Is it true that $\mathfrak{c}\to (\beta, n)_2^3$?
- 题意摘要：把 $\mathfrak c$ 视为连续统基数对应的初始序数。所问是：对每个可数序数 $\beta$、每个有限 $2\le n<\omega$、每个染色 $d:[\mathfrak c]^3\to\{0,1\}$，是否必有序型为 $\beta$ 的 $0$-齐次集，或大小为 $n$ 的 $1$-齐次集。
- 状态核对：官方仍列为 open。旧候选关于 $n=2,3$ 的结论正确，但不能据其未经核验的二手引文扩大已知范围。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先限制染色到 $\mathfrak c$ 中按序型排列的一个 $\omega$-子集，并应用无限 Ramsey 定理 $\omega\to(\omega)^3_2$；再结合 Erdős–Rado 已知的 $\mathfrak c\to(\omega+m,4)^3_2$ 做单调性归约。
- 局部结论：对所有有限 $n$，若 $\beta\le\omega$，结论成立：无限齐次集若颜色为 $0$，可截取序型 $\beta$；若为 $1$，可截取 $n$ 个点。；对 $n=2$，第二分支因三元组集合为空而自动成立；对 $n=3$，若存在颜色 $1$ 的三元组即完成，否则整个 $\mathfrak c$ 为颜色 $0$。故这两种 $n$ 对任意可数 $\beta$ 均成立。；由已知定理及序型单调性，$n=4$ 且 $\beta\le\omega+m$（某个有限 $m\ge2$）时成立。
- 第一阻塞点：对一般 $n\ge4$、尤其 $\beta\ge\omega\cdot2$，Ramsey 定理只给无穷齐次集而不能控制所需的更大可数序型；Erdős–Rado 特例的第二目标固定为 $4$，也不能推出大小 $n>4$ 的齐次集。这里缺少能同时提升序型和有限目标的分割关系。
- 下一步：首先检验下一最小边界实例 $\mathfrak c\to(\omega\cdot2,4)^3_2$：把现有 $\omega+m$ 证明逐引理拆开，定位其为何只能增加有限尾部，并尝试构造两个连续 $\omega$-块。
- 来源核对：[Erdős Problem 70](https://www.erdosproblems.com/70) 仍标为 OPEN，只明确列出 $\mathfrak c\to(\omega+m,4)^3_2$。；官方[修订记录](https://www.erdosproblems.com/history/70)与输入陈述一致。
- 时间记账：所在批次墙钟时间按题数均摊约 77.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/70)；既有候选答案（按不可信材料审计）

### #74

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)\to \infty$ (possibly very slowly). Is there a graph of infinite chromatic number such that every finite subgraph on $n$ vertices can be made bipartite by deleting at most $f(n)$ edges?
- 题意摘要：量词为：对每个 $f:\mathbb N\to\mathbb N$ 且 $f(n)\to\infty$，是否存在一个固定图 $G$，满足 $\chi(G)$ 无限，并且每个恰有 $n$ 个顶点的有限子图 $H\subseteq G$ 都能删除至多 $f(n)$ 条边而成为二部图。
- 状态核对：官方仍列为 open，甚至 $f(n)=\sqrt n$ 未知；旧候选的线性情形只是已知部分结果。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试把高围长、高有限色数的有限图 $G_r$ 作不交并。各 $\chi(G_r)$ 无界会使不交并的色数为 $\aleph_0$；逐渐增大的围长则让小子图自动成为森林。先可将 $f$ 替换为非降尾部下包络 $g(n)=\min_{m\ge n}f(m)\le f(n)$。
- 局部结论：若 $\chi(G_r)\to\infty$，则 $G=\bigsqcup_rG_r$ 满足 $\chi(G)=\aleph_0$。；若 $G_r$ 的围长大于 $n$，则其中任意 $n$ 顶点子图无环，因而无需删边。；对横跨多个分量的 $H$，二部化删除数至多各分量删除数之和；因此只有围长不超过 $n$ 的有限多个早期分量可能贡献。
- 第一阻塞点：构造 $G_r$ 后，其边数可能极大，而它一旦在某个规模出现奇环，就可能需要删除许多边。任意慢增的 $f$ 未必在该“激活规模”前增长到足以支付这笔边数。高围长高色数定理没有给出所需的围长、规模与奇环边横截数的联合控制；这正是拼接路线首次失效处。
- 下一步：定义有限型参数 $b_r(t)$：色数至少 $r$、围长至少 $t$ 的有限图中，最小可能的最坏 $n$-顶点二部化删除数。先对 $r=3,4$ 和有限 $t,n$ 求界，检验能否得到只依赖 $n/t$ 而非整个分量边数的估计。
- 来源核对：[Erdős Problem 74](https://www.erdosproblems.com/74) 仍标为 OPEN，并确认 Rödl 的 $\varepsilon n$ 情形及 $\sqrt n$ 情形仍未知。；本地 Lean 陈述确认为 $\forall f\,\exists G\,\forall n$ 的统一量词，并以最大二部化边距离表达条件。
- 时间记账：所在批次墙钟时间按题数均摊约 77.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/74)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/74.lean`；既有候选答案（按不可信材料审计）

### #75

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a graph of chromatic number $\aleph_1$ such that for all $\epsilon>0$ if $n$ is sufficiently large and $H$ is a subgraph on $n$ vertices then $H$ contains an independent set of size $>n^{1-\epsilon}$?
- 题意摘要：输入的字面量词是：存在 $G$，$\chi(G)=\aleph_1$，且 $\forall\epsilon>0\,\exists N\,\forall n\ge N\,\forall H\subseteq G$（$|V(H)|=n$），有 $\alpha(H)>n^{1-\epsilon}$。但当前官方题目和本地 Lean 文件还要求 $|V(G)|=\aleph_1$；输入漏掉了这一关键条件。
- 状态核对：因此该条目内部不一致：字面陈述已由已知定理肯定解决，而带 $|V(G)|=\aleph_1$ 的实际第75题仍 open。旧候选的推导解决的是前者，其错误是把一个通常有 $2^{\aleph_1}$ 个顶点的图当作解决了后者；在 $\Diamond$ 下得到 $\omega_1$ 顶点也不是 ZFC 证明。
- 初步判定：`malformed`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：核对 Lambie-Hanson 定理：任给 $F:\mathbb N\to\mathbb N$，存在 $\aleph_1$-色图 $G$，使每个少于 $F(k)$ 个顶点的子图色数小于 $k$。取 $F(k)=2^{k^2}$，对 $n$ 顶点子图取 $k=\lceil\sqrt{\log_2 n}\rceil+3$。
- 局部结论：因 $n<F(k)$，有 $\chi(H)<k$，故 $\alpha(H)\ge n/\chi(H)>n/k$。；对每个固定 $\epsilon>0$，充分大时 $k<n^\epsilon$，于是 $\alpha(H)>n^{1-\epsilon}$；因此输入中的字面陈述在 ZFC 中成立。；该定理的通常构造可有 $2^{\aleph_1}$ 个顶点；加入 $|V(G)|=\aleph_1$ 后，上述归约不能提供所需见证。
- 第一阻塞点：对输入的字面陈述没有阻塞，证明由已知定理闭合。对实际强化题，第一处阻塞是无法把 Lambie-Hanson 图压缩到 $\aleph_1$ 个顶点并同时保持色数及所有有限子图界；已知的 $\Diamond$ 构造不能无条件使用。
- 下一步：修复 cohort 数据：在 exact_statement 中补入“with $\aleph_1$ vertices”。随后把任务改为检验 Lambie-Hanson 构造中使用的猜测原则能否由更弱、可分离的组合原理替代。
- 来源核对：[当前官方第75题](https://www.erdosproblems.com/75) 明确含 $|V(G)|=\aleph_1$，并说明不加此条件的版本已有构造。；Lambie-Hanson 的[原论文摘要](https://arxiv.org/abs/1902.08177)确认任意函数 $F$ 对应的有限子图色数增长定理。；本地 Lean 文件同样显式包含 `#V = ℵ_ 1`，证实输入 exact_statement 有遗漏。
- 时间记账：所在批次墙钟时间按题数均摊约 77.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/75)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/75.lean`；既有候选答案（按不可信材料审计）

### #77

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $R(k)$ is the Ramsey number for $K_k$, the minimal $n$ such that every $2$-colouring of the edges of $K_n$ contains a monochromatic copy of $K_k$, then find the value of\[\lim_{k\to \infty}R(k)^{1/k}.\]
- 题意摘要：$R(k)=R(k,k)$ 是最小的 $N$，使每个 $K_N$ 的红蓝边染色含单色 $K_k$。所问首先包括极限 $\lim_{k\to\infty}R(k)^{1/k}$ 是否存在，其次才是其数值。
- 状态核对：截至核查时仍 open；旧候选给出的状态及指数上下界基本正确，但没有尝试解决极限存在性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先重建经典指数界，再尝试对 $a_k=\log R(k)$ 建立可用 Fekete 引理的近似次可加关系 $a_{k+\ell}\le a_k+a_\ell+o(k+\ell)$。
- 局部结论：随机红蓝染色中单色 $K_k$ 的期望数为 $2\binom Nk2^{-\binom k2}$；取 $N=2^{k/2-o(k)}$ 可使其小于 $1$，故 $\liminf R(k)^{1/k}\ge\sqrt2$。；经典递推 $R(s,t)\le R(s-1,t)+R(s,t-1)$ 给出 $R(k)\le\binom{2k-2}{k-1}$，从而经典 $\limsup\le4$；现有文献把它改进到约 $3.7992$。；标准分块或词典积染色控制的是团大小的乘积，不能产生关于 $\log R(k)$ 的所需近似次可加式。
- 第一阻塞点：没有已知办法由 Ramsey 递推或染色积构造推出 $R(k+\ell)\le R(k)R(\ell)e^{o(k+\ell)}$（或足够强的反向关系）。因此 Fekete 路线在建立近似次可加性这一步立即中断；上下界本身也不迫使根极限存在。
- 下一步：系统检验非对角数 $R(s,t)$ 的已知乘积不等式：明确计算它们在对角线 $s=t$ 上产生的误差是否为 $e^{o(k)}$；若误差仍为 $e^{\Theta(k)}$，即可排除这条极限存在性路线。
- 来源核对：[Erdős Problem 77](https://www.erdosproblems.com/77) 仍标为 OPEN，并明确指出连极限存在性也未知。；Campos–Griffiths–Morris–Sahasrabudhe 的[原论文](https://arxiv.org/abs/2303.09521)确认首次得到 $(4-\varepsilon)^k$ 型指数改进；官方页记录后续约 $3.7992$ 的优化。
- 时间记账：所在批次墙钟时间按题数均摊约 77.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/77)；既有候选答案（按不可信材料审计）

### #78

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Give a constructive proof that $R(k)>C^k$ for some constant $C>1$.
- 题意摘要：令对角 Ramsey 数 R(k)=R(k,k)。要求存在绝对常数 C>1，并给出被该问题认可的显式构造：对每个充分大的 k，构造一个含至少 C^k 个顶点的图，同时满足 ω(G),α(G)<k。这里“constructive”不能仅指有限穷举或把概率存在性用指数级条件期望搜索确定化。
- 状态核对：冻结状态为 open。先前候选没有解决问题：逐边条件期望虽是确定算法，但计算势函数需要枚举约 binom(n,k) 个集合，实质仍是 n^{Θ(log n)} 级搜索；评审指出这不符合本题的构造性含义。另有一个严格不等式错误：R(k)>⌊2^{k/2}⌋不能推出 R(k)>2^{k/2}，至多可改取任意 C<√2 并限于充分大 k。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：检验经典代数候选 Paley 图 P_q：取 q≡1 (mod 4)，以非零平方剩余定义邻接。它显式、自补，并可用特征值控制齐次集，故是最直接的“真正显式”路线。
- 局部结论：P_q 自补，因此 α(P_q)=ω(P_q)。；Paley 图的非平凡邻接特征值为 (-1±√q)/2；Hoffman 型界给出 α(P_q),ω(P_q)≤√q（取整误差无关紧要）。；所以该路线只能在 q=O(k²) 时保证无 k 阶 clique/independent set，得到多项式规模，而非 q≥C^k。
- 第一阻塞点：第一处无法闭合的是把平方根界改进为 O(log q)。现有二次特征和/谱估计只产生 √q 量级；所需结论等价于控制所有约 log q 阶顶点集合的高阶相关性，普通 Weil/谱界不足。
- 下一步：对具体 Paley/有限域候选建立一份精确的高阶相关和公式，并检验是否存在可迭代的双线性化，使 k=a log q 时坏集合计数获得 q^{-Ω(k)} 衰减；若只能得到 q^{-O(1)}，即可明确否决这条候选路线。
- 来源核对：官方条目仍把目标解释为显式 O(log n)-Ramsey 图，并列为开放问题：[Erdős Problem #78](https://www.erdosproblems.com/78)。；已有显式结果仍弱于 O(log n) 齐次集；这与条件期望穷举不能结题相符：[短列表 Ramsey 图论文](https://arxiv.org/abs/1210.4408)。
- 时间记账：所在批次墙钟时间按题数均摊约 55.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/78)；既有候选答案（按不可信材料审计）

### #80

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c>0$ and let $f_c(n)$ be the maximal $m$ such that every graph $G$ with $n$ vertices and at least $cn^2$ edges, where each edge is contained in at least one triangle, must contain a book of size $m$, that is, an edge shared by at least $m$ different triangles. Estimate $f_c(n)$. In particular, is it true that $f_c(n)>n^{\epsilon}$ for some $\epsilon>0$? Or $f_c(n)\gg \log n$?
- 题意摘要：固定 c>0。对所有 n 顶点、至少 cn² 条边且每条边至少属于一个三角形的图 G，记最大书本大小 bk(G)=max_{uv∈E}|N(u)∩N(v)|；则 f_c(n) 是这些图的 bk(G) 的最小可能值。问题要求估计它，特别询问固定 c 下是否有 f_c(n)>n^ε，或至少 f_c(n)≫log n。
- 状态核对：冻结状态为 open，但幂次下界在 c<1/4 时已被 Fox–Loh 的 n^{o(1)} 上界否定；c>1/4 时已知线性下界。真正未闭合的是 c<1/4 的定量下界，尤其 log n。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：从三角形移除引理重建 Szemerédi 的 f_c(n)→∞ 论证，并尝试定量反演。设 b=bk(G)，T 为三角形数。
- 局部结论：由每条边在三角形中，3T=∑_{e∈E}t(e)≥|E|≥cn²；又 t(e)≤b，故 T≤b|E|/3≤bn²/6。；贪心选边不交三角形：每选一个至多排除 3b 个三角形，故存在至少 T/(3b)≥cn²/(9b) 个边不交三角形。因此要删成无三角形图，至少须删 cn²/(9b) 条边。；若 b≤B 为固定常数，三角形移除引理给 T≥δ(c/(9B))n³；这与 T≤Bn²/6 对充分大 n 矛盾。因此严格推出 f_c(n)→∞。
- 第一阻塞点：要推出 f_c(n)≫log n，必须从隐式不等式 b≥6δ(c/(9b))n 得到对数级反演；已知三角形移除函数 δ(ε) 的定量衰减仍太弱，代入不能给出 log n。
- 下一步：选定当前最强的三角形移除界 δ(ε)，逐常数反演 b≥6δ(c/(9b))n，核算它实际给出的迭代指数型下界；同时检查“每边至少一个三角形”能否加强一般移除引理中的 δ。
- 来源核对：Fox–Loh 原论文摘要确认：对每个固定 c<1/4，有 f_c(n)≤n^{O(1/log log n)}，从而排除固定幂次下界：[Fox–Loh](https://arxiv.org/abs/1106.0290)。；同一来源确认 c>1/4 时已知至少 n/6 的书本；先前候选额外写出的 (2c−1/3)n 未在本次筛查中重建，故不作为已核结论。
- 时间记账：所在批次墙钟时间按题数均摊约 55.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/80)；既有候选答案（按不可信材料审计）

### #81

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a chordal graph on $n$ vertices - that is, $G$ has no induced cycles of length greater than $3$. Can the edges of $G$ be partitioned into $n^2/6+O(n)$ many cliques?
- 题意摘要：对每个 n 顶点弦图 G，询问其边集能否划分为至多 n²/6+O(n) 个完全子图的边集；“划分”要求每条边恰好出现一次，2-顶点 clique 允许。O(n) 的常数必须对所有弦图统一。
- 状态核对：冻结状态为 open。已知下界例的领先常数 1/6 可严格核对；一般上界仍只有大于 1/6 的常数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：先精确分析极值 split 图，再尝试把相同的“节省量—已消耗内部边”记账嵌入弦图的完美消去序。令 A=K_k、B 为 2k 个独立点，并连接 A 与 B，故 n=3k。
- 局部结论：对每个 b∈B，含 b 的分割 cliques 在 A 上形成一个分块。若块大小为 s，相对把 s 条横边分别作为 K₂，节省 s−1 个 clique，但同时占用 binom(s,2) 条 A 内部边。；由于边划分不许重复，同一条 A 内部边至多被一个这样的块占用；又 s−1≤binom(s,2)，总节省至多 binom(k,2)。故 clique 数至少 2k²−binom(k,2)=3k²/2+k/2=n²/6+n/6。；把 K_k 的边分解成匹配，并把各匹配分配给不同的 b∈B，可用大小二的块实现全部上述节省，故在相应整除情形下该下界可达；先前候选给出的数值因而可成立，但其原文没有提供必要的边划分论证。
- 第一阻塞点：在一般弦图的完美消去序中，一个 clique 会同时覆盖当前顶点的若干后向边和后向顶点之间的边。局部节省会消耗后续边，但这些消耗跨多个不同邻域耦合；尚不能证明全局总节省足以把朴素边数界压到 n²/6+O(n)。
- 下一步：固定完美消去序，把每个分割 clique 归属给其最早顶点，建立“节省量”和被提前占用的后向边之间的精确充电不等式；先在区间图或所有后向邻域嵌套的阈值图上验证常数 1/6，再寻找一般弦图中失败的最小配置。
- 来源核对：原论文摘要确认下界例、开放性及已知 (1−c)n²/4 上界：[Erdős–Ordman–Zalcstein](https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/clique-partitions-of-chordal-graphs/CEA1F929F2A88B5A4C7C8E23DFD0DD29)。；split 图论文明确记录该例的精确值 n²/6+n/6（在适当整除条件下）：[Chen–Erdős–Ordman PDF](https://ordman.net/MathResearch/CEOClique_Parts.pdf)。
- 时间记账：所在批次墙钟时间按题数均摊约 55.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/81)；既有候选答案（按不可信材料审计）

### #82

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(n)$ be maximal such that every graph on $n$ vertices contains a regular induced subgraph on at least $F(n)$ vertices. Prove that $F(n)/\log n\to \infty$.
- 题意摘要：定义 F(n)=min_{|V(G)|=n} max{|S|:G[S]为正则图}。目标极限的完整量词是：对每个 M>0，存在 N，使所有 n≥N 及所有 n 顶点图 G 都含有某个诱导正则子图 G[S]，满足 |S|≥M log n。正则度数可依赖 G、S、n。
- 状态核对：冻结状态为 open。Lean 文件忠实表达了极限，但定理仍为 sorry。先前候选把 AKS 精确上界写成 log^{1/4}n；本地形式化说明及论文版本给出的是 log^{3/4}n，因此该指数不能沿用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：从 Ramsey 齐次集路线出发，再考察能否借“近正则诱导子图”升级为精确正则。
- 局部结论：由 R(k,k)≤binom(2k−2,k−1)<4^{k−1}，每个 n 顶点图含大小至少 ⌊log₄n⌋+1 的 clique 或独立集；二者分别是诱导 (k−1)-正则和 0-正则图。因此 F(n)=Ω(log n)。；取补图不改变可用顶点数：G[S] 为 d-正则当且仅当 complement(G)[S] 为 (|S|−1−d)-正则，所以稠密、稀疏两端完全对称。；AKS 的近正则结果能给大得多的 S 且 Δ(G[S])≤(1+ε)δ(G[S])，但这只限制度数区间长度，不能保证存在大顶点子集在重新诱导后度数完全相等。
- 第一阻塞点：第一处断裂是“近正则⇒含大型诱导正则子图”。删除一个顶点会同时改变其所有邻点的度数，度数相同的顶点集合在取诱导子图后也未必继续同度；简单鸽巢或迭代删除均没有保持不变量。
- 下一步：对 AKS 产生的近正则图 H，检验一个明确子命题：若 |V(H)|=m 且 Δ−δ≤D，是否必有大小 g(m,D) 的诱导正则子图，其中 g(m,D) 超过 C log m；先用小图穷举寻找反例形态，再决定该桥接引理是否值得证明。
- 来源核对：AKS 原始论文确认精确正则情形仅有 Ω(log n) 下界，并给出 O(n^{1/2}log^{3/4}n) 上界：[AKS PDF](https://people.math.ethz.ch/~sudakovb/nearly-regular.pdf)。；本地形式化文件将目标写成 Tendsto，并把 AKS 上界记录为 sqrt(n)(log n)^{3/4}；两处尚均为 sorry，不能视为形式化证明。
- 时间记账：所在批次墙钟时间按题数均摊约 55.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/82)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/82.lean`；既有候选答案（按不可信材料审计）

### #84

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：The cycle set of a graph $G$ on $n$ vertices is a set $A\subseteq \{3,\ldots,n\}$ such that there is a cycle in $G$ of length $\ell$ if and only if $\ell \in A$. Let $f(n)$ count the number of possible such $A$. Prove that $f(n)=o(2^n)$. Prove that $f(n)/2^{n/2}\to \infty$.
- 题意摘要：对每个 n，f(n) 统计所有可由某个 n 顶点简单图实现的圈长集合 A⊆{3,…,n} 的数量。题目含两个独立渐近断言：(i) f(n)/2^n→0；(ii) f(n)/2^{n/2}→∞。
- 状态核对：整体冻结为 open，是因为第二问仍开放；第一问已由 Verstraëte 解决，Nenadov 又改进其上界。先前候选的扇形图表述遗漏了“两条弦也会组成圈”，原论证按字面不严密。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：第一问采用已知计数定理核验；第二问修正扇形构造：在路径 1-2-…-n 上只添加从 1 到远端点的弦，并只读取足够大的圈长。
- 局部结论：Nenadov 定理给 f(n)≤2^{n−n^{1/2−o(1)}}；由于 n^{1/2−o(1)}→∞，立即严格推出 f(n)/2^n≤2^{-n^{1/2−o(1)}}→0。第一问因此已有证明。；该扇形图的每个圈恰由顶点 1 的两条关联边及其端点间的路径组成；若端点为 a,b，则圈长为 |a−b|+2。故两条远端弦确实会产生额外圈长，不能笼统声称每个圈只用一条弦。；若 n=2k，对任意 S⊆{k+2,…,2k} 添加弦 1a（a∈S），则两条新增弦产生的圈长至多 k+1，而大于 k+1 的圈长恰为 S。因此得到至少 2^{k−1} 个不同圈长集合；奇数情形类似得到 2^{⌊n/2⌋−O(1)}。
- 第一阻塞点：修正后的构造只给 f(n)≥2^{n/2−O(1)}，与目标相差一个趋于无穷的乘法因子。要叠加额外参数，新增边往往产生跨参数的差值圈长 |a−b|+2，使不同编码碰撞；目前没有可解码的不交“附加自由度”。
- 下一步：尝试在扇形编码上加入一个独立、可从低圈长区间唯一识别的参数族 T，并严格证明映射 (S,T)↦cycle-set 为单射；首个可检验目标是获得 Ω(log n) 个互不碰撞的 T，从而把下界提高到 n·2^{n/2−O(1)}。
- 来源核对：Nenadov 的原始论文摘要明确给出 2^{n−n^{1/2−o(1)}} 上界，并说明采用 Verstraëte 的 Hamilton 圈加弦计数框架：[Nenadov](https://arxiv.org/abs/2501.09904)。；该来源只改进第一问的上界；未声称第二问解决，因此不能从文字上的“improved bound”误判整个问题已解。
- 时间记账：所在批次墙钟时间按题数均摊约 55.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/84)；既有候选答案（按不可信材料审计）

### #86

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $Q_n$ be the $n$-dimensional hypercube graph (so that $Q_n$ has $2^n$ vertices and $n2^{n-1}$ edges). Is it true that every subgraph of $Q_n$ with\[\geq \left(\frac{1}{2}+o(1)\right)n2^{n-1}\]many edges contains a $C_4$?
- 题意摘要：令 f(n)=max{|E(H)|:H⊆Q_n 且 H 不含 C_4}。问题问：是否 f(n)/(n2^{n-1})≤1/2+o(1)，即对每个固定 δ>0，充分大 n 时，边数至少 (1/2+δ)n2^{n-1} 的 H 必含 C_4。
- 状态核对：截至官方页面最近核对仍为开放。先前候选仅报告状态，没有推进上界；其“隔层取边”构造确为 C_4-free，但不能证明上界。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：按二维面逐个计数。Q_n 有 2^{n-2}·C(n,2) 个二维面，每条边属于 n−1 个二维面。若 H 无 C_4，则每个二维面至多保留3条边，故对面—边关联双计数。
- 局部结论：严格得到 (n−1)|E(H)|≤3·2^{n-2}C(n,2)，从而 |E(H)|≤(3/4)n2^{n-1}。；保留权重层间隙 (0,1),(2,3),… 的全部边时，每个方形跨越两个相邻层间隙，至少缺两条边，故构造无 C_4。其边数为总边数的 1/2+O(1/√n)，足以解释主项 1/2，但精确余项需更细构造。；单纯使用“每个面至多3边”只能到密度3/4；必须利用相邻二维面共享边所造成的全局一致性。
- 第一阻塞点：第一处无法闭合的是把局部缺边比例1/4提升为全局缺边比例1/2−o(1)：C_4-free 条件允许不同二维面共用同一条缺边，当前双计数没有控制这种重叠。
- 下一步：定义每条缺边覆盖的二维面数及面缺边重叠图；先检验能否证明除 o(n2^n) 个面外，每个面平均至少有2条缺边，或构造高密度例子否定该中间命题。
- 来源核对：官方页面仍标为 OPEN，并列出 f(n)≤0.60318n2^{n-1} 的已知上界：https://www.erdosproblems.com/86；独立核算二维面数、每边所属面数及隔层构造；未把未受信候选当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 39.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/86)；既有候选答案（按不可信材料审计）

### #87

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon >0$. Is it true that, if $k$ is sufficiently large, then\[R(G)>(1-\epsilon)^kR(k)\]for every graph $G$ with chromatic number $\chi(G)=k$? Even stronger, is there some $c>0$ such that, for all large $k$, $R(G)>cR(k)$ for every graph $G$ with chromatic number $\chi(G)=k$?
- 题意摘要：这里 R(G)=R(G,G)，R(k)=R(K_k,K_k)。第一问量词为：对每个固定 ε>0，存在 k₀(ε)，使所有 k≥k₀ 及所有有限图 G，只要 χ(G)=k，就有 R(G)>(1−ε)^kR(k)。第二问要求存在绝对常数 c>0，对所有充分大 k 和所有此类 G，有 R(G)>cR(k)。
- 状态核对：两问仍开放；第二问确实更强，因为固定 c 最终大于 (1−ε)^k。先前候选的随机着色思路基本正确，现独立补齐量词与计数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：取 G 的 k-临界子图 H，记 v=|V(H)|、e=|E(H)|。临界性给 δ(H)≥k−1，故 e≥(k−1)v/2。随机二染 K_N 的边，以一阶矩排除单色 H。
- 局部结论：至多 N^v 个标号嵌入中，每个像单色的概率为2^{1−e}，故期望至多 2N^v·2^{−(k−1)v/2}。取 N≤2^{(k−1)/2}/2 时该期望至多2^{1−v}<1，因此 R(G)>N，统一得到 R(G)≫2^{k/2}。；结合 R(k)≤4^k，上式已推出第一问在 4(1−ε)<√2，即 ε>1−1/(2√2) 的范围成立；ε≥3/4 只是更容易的子范围。；k=4 的五边形轮满足 χ=4、R=17<R(4)=18，故原先更强的常数1版本错误，但不反驳题中任一渐近断言。
- 第一阻塞点：第一处无法闭合的是将 R(G)≫2^{k/2} 与 R(k) 作足够精细的比较：现有一般上界 R(k)≤4^k 在较小 ε 时指数损失过大，更完全无法给出 R(G)/R(k) 的正下界。
- 下一步：研究 m(k)=min_{χ(G)=k}R(G)，首先检验临界图的边数、顶点数或独立数能否使随机着色计数优于2^{k/2}；目标是为某一类临界图获得依赖 R(k) 而非仅依赖4^k的下界。
- 来源核对：官方页面截至最近编辑仍标两问 OPEN，并记录随机着色下界及轮图反例：https://www.erdosproblems.com/87；重新验证了 k-临界子图、一阶矩和常数范围；未直接采信先前候选。
- 时间记账：所在批次墙钟时间按题数均摊约 39.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/87)；既有候选答案（按不可信材料审计）

### #89

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does every set of $n$ distinct points in $\mathbb{R}^2$ determine $\gg n/\sqrt{\log n}$ many distinct distances?
- 题意摘要：对每个有限 A⊂R²，|A|=n，令 D(A)为不同非零欧氏距离数。问题问是否存在绝对常数 c>0、n₀，使所有 n≥n₀ 及所有这样的 A 都满足 D(A)≥cn/√log n。
- 状态核对：仍为开放；Guth–Katz 已证明统一下界 D(A)≫n/log n。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用距离能量。对每个距离 r 令 m_r 为产生 r 的无序点对数，并令 E(A)=Σ_r m_r²。由 Σ_r m_r=C(n,2)，对距离类别使用 Cauchy–Schwarz。
- 局部结论：严格有 C(n,2)²≤D(A)E(A)，因此 D(A)≥C(n,2)²/E(A)。；Guth–Katz 型估计 E(A)=O(n³log n)立即给出 D(A)=Ω(n/log n)。；目标结论可由改进能量界 E(A)=O(n³√log n)推出；整数格的距离数约为 n/√log n，说明这一能量尺度至少在数量级上不能随意再降低。
- 第一阻塞点：第一处无法闭合的是把等距四元组的总计数从 O(n³log n)降到 O(n³√log n)。现有路线中的对称线/富线分层求和产生完整的 log n，普通 Cauchy–Schwarz 不提供额外的平方根节省。
- 下一步：把 Guth–Katz 能量证明按富度 dyadic 层拆开，计算每一层对 E(A) 的贡献；检验是否能证明只有 O(√log n) 个层可同时接近极值，或由多层同时饱和推出近格结构。
- 来源核对：官方页面仍标 OPEN，并明确给出 Guth–Katz 的 Ω(n/log n)：https://www.erdosproblems.com/89；本地 Lean 文件把目标正确写为 n/√log n = O(minimalDistinctDistances n)，方向与原命题一致。
- 时间记账：所在批次墙钟时间按题数均摊约 39.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/89)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/89.lean`；既有候选答案（按不可信材料审计）

### #90

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Does every set of $n$ distinct points in $\mathbb{R}^2$ contain at most $n^{1+O(1/\log\log n)}$ many pairs which are distance 1 apart?
- 题意摘要：令 ν(P)为有限平面点集 P 中距离恰为1的无序点对数，ν(n)=max_{|P|=n}ν(P)。原猜想断言存在绝对常数 C,N，使每个 n≥N 都有 ν(n)≤n^{1+C/loglog n}。其否定为：对任意 C,N，存在 n≥N 及 n点集 P，使 ν(P)>n^{1+C/loglog n}。
- 状态核对：原题已被否定：现有结果构造绝对常数 δ>0及无穷多个 n，使 ν(n)≥n^{1+δ}。先前候选声称“仍开放”已经过时，不能保留。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：重建已知反例路线：构造次数趋于无穷的全实数域 L_j，其根判别式有界且若干固定素数完全分裂；令 K_j=L_j(i)。利用理想类抽屉原理得到指数多个 u∈K_j，满足所有复嵌入下 |σ(u)|=1。把这些 u 当作高维 Minkowski 格中的单位平移，在多圆盘窗口内平均计数，再投影到一个复坐标。
- 局部结论：理想类数至多随 [L_j:Q] 指数增长，而完全分裂素数提供更多二元理想选择；适当选参数可得 |U_j|≥exp(γ[L_j:Q])，γ>0。；窗口平均给出某个有限格点集 X_j，具有至少 exp(γf_j/2)|X_j|/2 条投影后单位距离；单坐标投影因域嵌入的单射性不会合并不同点。；格点分离与装箱估计给 |X_j|≤exp(Bf_j)。于是 ν(|X_j|)≥|X_j|^{1+δ}，可取 δ=γ/(4B)>0；因 |X_j|→∞，这严格否定任意 C/loglog n 上界。
- 第一阻塞点：已知论文路线能够闭合。此次受限重建中第一项未逐引理复核的是 Golod–Shafarevich/Shafarevich 关系秩步骤：商掉指定素数的 Frobenius 正规闭包后，所得 pro-3 群仍无限，从而产生所需无穷非分歧塔。
- 下一步：逐条核验论文第3节的群论不等式：确认被杀死的 Frobenius 元位于 Frattini 子群、增加的关系数不超过3t，并验证 r+3t<d²/4；这是反例路线最关键且可独立检查的技术节点。
- 来源核对：官方页面已标 DISPROVED (LEAN)，并链接反例论文：https://www.erdosproblems.com/90；反例论文定理1.1及其构造概要：https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf；本地 90.lean 仍含 sorry，且把上界写成 eventually 精确等式；该文件本身不是忠实、完整的反例证明，不能单独支持“Lean 已验证”的说法。数学否定结论由上述反例论文路线支持。
- 时间记账：所在批次墙钟时间按题数均摊约 39.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/90)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/90.lean`；既有候选答案（按不可信材料审计）

### #91

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Suppose $A\subset \mathbb{R}^2$ has $\lvert A\rvert=n$ and minimises the number of distinct distances between points in $A$. Prove that for large $n$ there are at least two (and probably many) such $A$ which are non-similar.
- 题意摘要：令 f(n)=min_{|A|=n}D(A)，并把达到 f(n) 的点集称为极小器。命题要求存在 N，使每个 n≥N 都至少有两个在平面相似变换下不等价的极小器；不是仅要求无穷多个 n。
- 状态核对：仍为开放。明确吸收人工评审：先前候选只证明了无穷多个任意大的 n，最后却称“正是所求”，量词错误；其论证至多是部分结果。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：审查并保留先前路线中可严格成立的部分：由格点构造得 f(n)=o(n)；整数非降函数 f 因而有无穷多个平台 f(n)=f(n+1)。在平台处，从一个 n+1 点极小器 B 删除不同的非凸包顶点。
- 局部结论：f(n)非降且为整数；若从某处起每步严格增加，则 f(n)=Ω(n)，与格点给出的 f(n)=O(n/√log n)矛盾。因此 f(n)=f(n+1) 对无穷多个 n 成立。；若 B 有 h 个凸包顶点，则凸位置点集的等腰三角形计数给 D(B)≥(h−1)/3，所以 h≤3f(n+1)+1=o(n)。；对平台 n，删除任一非凸包顶点 p 后，B\{p}仍是 n点极小器且凸包不变。固定凸 h 边形至多有2h个相似自同构，而可删点数为 n+1−h≫h；故这些删点极小器分属至少两个、事实上趋于无穷多个相似类。于是结论对无穷多个 n 严格成立。
- 第一阻塞点：第一处无法闭合的是把“平台 f(n)=f(n+1) 无穷多次”加强为“每个充分大 n 都能制造两个极小器”。f(n)=o(n)只排除最终处处严格递增，完全允许任意长的严格递增区间，因此不能提供最终全称量词。
- 下一步：检验能否证明有界间隙平台，例如存在固定 L，使每个充分大的区间 [n,n+L] 内都有 f(m)=f(m+1)；随后研究从 m点极小器连续删去 m−n 个内点是否仍保持 f(n)。任一环节失败都应寻找相应数值或结构反例。
- 来源核对：官方页面明确表述为“n sufficiently large”并仍标 OPEN：https://www.erdosproblems.com/91；本地 Lean 陈述为 eventually ¬UniqueMinimizer n，与“所有充分大 n”一致。；重新检查凸位置等腰三角形计数、凸包对称群上界及删点论证；这些支持无穷子序列结论，但不支持最终全称结论。
- 时间记账：所在批次墙钟时间按题数均摊约 39.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/91)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/91.lean`；既有候选答案（按不可信材料审计）

### #92

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that there exists a set $A$ of $n$ points in $\mathbb{R}^2$ in which every $x\in A$ has at least $f(n)$ points in $A$ equidistant from $x$. Is it true that $f(n)\leq n^{o(1)}$? Or even $f(n) < n^{O(1/\log\log n)}$?
- 题意摘要：对每个整数 n，f(n) 是最大整数 k，使得存在 n 点集 A⊂R²，并且对每个 x∈A，都存在一个可依赖于 x 的半径 r_x>0，使至少 k 个其他点 y∈A 满足 |x-y|=r_x。问题询问是否对所有充分大 n 有 f(n)=n^{o(1)}，乃至 f(n)≤n^{C/log log n}（某绝对常数 C）。
- 状态核对：已于2026-05-21被否证。先验候选所称“仍开放”已经过时。否证不能仅由单位距离图的高平均度直接推出逐点高次数，必须使用删点剪枝。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：调用已核验的第90题反例：存在 δ>0 及无限多个 N 点集 P_N，其单位距离图有至少 N^{1+δ} 条边。反复删除当前单位度数小于 N^δ 的顶点；若全部删除，被删除边总数严格小于 N·N^δ=N^{1+δ}，与原边数矛盾。因此剩下非空诱导子图 H，最小度至少 N^δ。令 m=|H|，则 m≤N 且 m≥N^δ+1，所以 m→∞，并有 δ(H)≥N^δ≥m^δ。于是 f(m)≥m^δ，且这样的 m 有无限多个。
- 局部结论：平均度至少 2N^δ 的单位距离图含最小度至少 N^δ 的非空诱导子图。；所得子图阶数 m→∞，且每个点都有至少 m^δ 个距离恰为1的邻点。；因此 f(m)≥m^δ 沿无限子序列成立，同时否定 f(n)=n^{o(1)} 和 f(n)≤n^{O(1/log log n)} 两种最终上界。
- 第一阻塞点：归约本身完全闭合；本次受限筛查没有重建第90题中依赖无限类域塔与 Golod–Shafarevich 理论的18页算术构造，而将其已核验的定理1.1作为输入。
- 下一步：逐引理审计第90题证明中“数域构造→平面单位距离点集”的几何投影步骤，并核对固定 δ 对整条无限序列一致。
- 来源核对：[第92题官方页](https://www.erdosproblems.com/92) 标为 DISPROVED，并明确说明由第90题否证。；[第90题原证明 PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf) 的定理1.1给出 ν(N)≥N^{1+δ}；紧随其后的文字明确执行平均度到最小度子图的归约。；[第92题讨论页](https://www.erdosproblems.com/forum/thread/92) 给出了相同的逐步剪枝论证。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/92)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/92.lean`；既有候选答案（按不可信材料审计）

### #96

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $n$ points in $\mathbb{R}^2$ form a convex polygon then there are $O(n)$ many pairs which are distance $1$ apart.
- 题意摘要：令 A 为处于凸位置的 n 个平面点，即它们全是某凸 n 边形的顶点。记 e(A) 为无序点对 {x,y}⊂A 中满足 |x-y|=1 的数量。猜想存在绝对常数 C，使每个这样的 A 都满足 e(A)≤Cn。
- 状态核对：截至官方页2026-01-23更新仍为开放；已知上界为 n log₂n+4n，构造下界为2n-7。先验候选提到的中心对称特例未在给定官方材料中核验，本筛查不使用它。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：把单位距离对作为图 G 的边。任意两顶点 u,v 的共同单位邻点同时位于以 u、v 为圆心的两个单位圆交集，故至多两个；所以 G 不含 K_{2,3}。对每个顶点对计数共同邻点，得 Σ_w C(d(w),2)≤2C(n,2)。由凸性及 Cauchy–Schwarz 可推出 e(G)=O(n^{3/2})。尝试再利用顶点的循环次序，把共同邻点计数压到 O(n)，但没有得到所需的凸位置禁型。
- 局部结论：单位距离图必为 K_{2,3}-free。；由 Σ_w C(d(w),2)≤2C(n,2) 和 Σ_w d(w)=2e，可严格推出 e=O(n^{3/2})。；该路线尚未使用凸性，因而不可能自动达到当前已知的 O(n log n)，更不能宣称线性界。
- 第一阻塞点：第一处无法闭合的是：无法证明凸多边形的循环次序会使上述共同邻点总量或某种分层后的单位边数降到 O(n)。K_{2,3}-free 本身只支持 n^{3/2} 量级。
- 下一步：固定一条对角线把顶点分成两条凸链，检验跨链单位边的邻接区间是否具有可证明的单调性；若有，先证明每个二分层级只有 O(n) 条边，再重建 O(n log n) 分治界。
- 来源核对：[第96题官方页](https://www.erdosproblems.com/96) 确认开放状态、n log₂n+4n 上界及2n-7下界。；K_{2,3}-free 论证也见[第90题原证明 PDF](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)导言，但这里已独立重建其两圆相交理由。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/96)；既有候选答案（按不可信材料审计）

### #98

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be such that any $n$ points in $\mathbb{R}^2$, with no three on a line and no four on a circle, determine at least $h(n)$ distinct distances. Does $h(n)/n\to \infty$?
- 题意摘要：h(n) 应理解为所有满足“无三点共线、无四点共圆”的 n 点集所确定的不同正距离数的最小值。问题是：是否对任意这样的点集都有距离数 n·ω(1)，即 h(n)/n→∞。
- 状态核对：仍为开放。先验候选的线性下界可独立验证；但其“高维格点作一般投影仍保留少量距离”的解释不可采信，因为一般线性投影通常不保距离相等，可能产生 Θ(n²) 个距离。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：把完全图的边按距离着色，共有 t 种颜色。对固定顶点 x 和固定距离 d，同色邻点都在圆 S(x,d) 上；无四点共圆保证其数目至多3。因此 n-1≤3t。进一步计数以 x 为顶点的等腰三角形：若第 d 色有 e_d 条边，则其贡献至少 2e_d²/n-e_d；对距离求和并用 Cauchy–Schwarz，同时利用每个局部色度≤3所得上界，仍只回收到 t≥(n-1)/3。
- 局部结论：每个顶点在每种距离颜色中的度数至多3。；严格得到 h(n)≥⌈(n-1)/3⌉。；等腰三角形能量法在仅使用“无四点共圆”时不会产生超线性结论：其上下界恰停留在线性常数量级。
- 第一阻塞点：第一处无法闭合的是把“无三点共线”转化为跨不同圆心、不同距离颜色的额外全局稀疏性；当前计数完全没有使用无三点共线，故不能使常数下界升级为 ω(n)。
- 下一步：分类局部色度为3的圆：对两个圆心共享的三点配置写出代数约束，并检验大量此类配置是否必迫使三点共线或四点共圆；目标是证明色度3事件总数为 o(n²) 或产生可迭代的结构定理。
- 来源核对：[第98题官方页](https://www.erdosproblems.com/98) 确认问题开放，并记录构造上界 h(n)<n exp(c√log n)。；官方材料没有支持先验候选所述的简单“一般投影保留少量距离”机制，故该解释已剔除。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/98)；既有候选答案（按不可信材料审计）

### #99

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq\mathbb{R}^2$ be a set of $n$ points with minimum distance equal to 1, chosen to minimise the diameter of $A$. If $n$ is sufficiently large then must there be three points in $A$ which form an equilateral triangle of size 1?
- 题意摘要：对每个 n，在所有最小点距至少1的 n 点集之间最小化直径；缩放说明极小值处最小点距恰为1。问题问是否存在 n₀，使 n≥n₀ 时每一个直径极小配置都含三个两两距离为1的点，即单位正三角形。
- 状态核对：仍为开放；n=4的单位正方形是小规模反例，但不处理“充分大 n”的量词。先验候选只陈述状态，没有给出可闭合证明。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `medium`
- 尝试路线：先建立极小配置存在性：用整数直线点集给出直径≤n-1的候选，固定一个点后，可把搜索限制在闭有界集合；距离约束与直径连续，故最小值达到。对一个极小配置构造接触图 G：顶点为点集，距离1连边。单位线段不能真交叉，否则交点把两条长度1线段分段后，四条相邻端点折线路径中至少一条长度≤1，而非共线的三角不等式严格给出某端点距离<1。故 G 平面。若没有单位正三角形，则 G 无三角形，从而 e(G)≤2n-4。
- 局部结论：直径极小配置确实存在，且可归一化为最小距离1。；其单位接触图是简单平面图。；若目标结论失败，则接触图无三角形并满足 e≤2n-4。
- 第一阻塞点：第一处无法闭合的是证明直径极小性迫使接触图拥有超过2n-4条边，或迫使某个三角面。渐近最密堆积只控制主项密度；对三角格点作微小扰动可消除精确接触而几乎不改变密度，所以密度渐近式本身不足。
- 下一步：对有限 n 的极小配置写出刚性应力/KKT条件，检验无三角接触图能否支撑所有直径约束；先从“接触图为二部图或外平面图”两个可计算子类证明其存在缩短直径的可行运动。
- 来源核对：[第99题官方页](https://www.erdosproblems.com/99) 确认开放、三角格点的渐近最优性及 n=4正方形反例。；官方表述只给出渐近堆积信息，没有给出把接触边数提升到2n-3的稳定性定理。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/99)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/99.lean`；既有候选答案（按不可信材料审计）

### #100

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be a set of $n$ points in $\mathbb{R}^2$ such that all pairwise distances are at least $1$ and if two distinct distances differ then they differ by at least $1$. Is the diameter of $A$ $\gg n$?
- 题意摘要：A 是 n 个不同平面点，所有距离至少1；把出现的不同距离排序为 1≤d₁<⋯<d_t，还要求 d_{i+1}-d_i≥1。问题是是否存在绝对常数 c>0、n₀，使所有 n≥n₀ 的这类 A 都满足 diam(A)≥cn。
- 状态核对：仍为开放。已知 Guth–Katz 不同距离定理给出 diam(A)≫n/log n；先验候选的这一步归约正确，但不是线性结论。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：由距离谱间隔，d_i≥d₁+i-1≥i，故 D=diam(A)=d_t≥t。Guth–Katz 定理对任意 n 个平面点给出 t≥c₀n/log n，因此 D≥c₀n/log n。整数直线点集 {0,1,…,n-1}×{0} 满足全部条件且 D=n-1，说明所猜线性阶若成立将是阶数最优。尝试利用1-分离距离谱改善不同距离下界，但现有能量论证的对数损失来自距离重数/富线结构，谱值彼此分离并不直接限制单个距离的重数。
- 局部结论：若共有 t 个不同距离，则 D≥t。；严格得到 D≫n/log n。；存在满足条件且 D=n-1的配置，所以任何普适下界至多具有线性阶。
- 第一阻塞点：第一处无法闭合的是证明在距离谱1-分离这一附加条件下，Guth–Katz 的 t≫n/log n 可改进为 t≫n；间隔条件只约束不同距离值的位置，尚未控制每个值出现多少次。
- 下一步：回到 Guth–Katz 的距离能量四元组计数，逐项定位 log n 损失；检验距离值1-分离能否排除造成该损失的 dyadic rich-line 层。若不能，构造一个同时具有高距离重数和1-分离谱的有限模型作为路线反证。
- 来源核对：[第100题官方页](https://www.erdosproblems.com/100) 确认开放，并明确记录 D≫n/log n。；[Guth–Katz 原论文预印本](https://arxiv.org/abs/1011.4105) 的主结果是任意 N 点至少确定 cN/log N 个不同距离。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/100)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/100.lean`；既有候选答案（按不可信材料审计）

### #101

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given $n$ points in $\mathbb{R}^2$, no five of which are on a line, the number of lines containing four points is $o(n^2)$.
- 题意摘要：令 P⊂R²，|P|=n，且任一直线至多含4个P中点。记 t₄(P) 为恰含4点的直线数；命题是 sup_P t₄(P)/n²→0。这里“含四点”因无五点共线等同于“恰含四点”。
- 状态核对：截至核验页面仍为 open；未发现给定材料中的候选答案解决了问题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把四点线视为以P为顶点的4-一致线性超图。先做点对双计数，再假设 t₄≥εn²，尝试从高超图度推出违反平面可实现性的结构。
- 局部结论：每条四点线占用6个点对，且不同直线不能共用一个点对，故 6t₄≤C(n,2)，即 t₄≤n(n−1)/12。；若 t₄≥εn²，则 Σ_{p∈P}d(p)=4t₄≥4εn²；逐次删除超图度小于2εn的点，可留下非空子集，其每点至少位于2εn条剩余四点线上。；对任一点p，经过p的不同四点线在其余点上互不相交，故 d(p)≤(n−1)/3。上述高密度假设因此确实产生线性规模的局部方向数，但尚不矛盾。
- 第一阻塞点：第一处缺口是：线性4-一致超图本身可以有Θ(n²)条边（设计理论给出抽象模型），所以点对预算和度数剪枝不能推出o(n²)；必须使用这些超边可由实平面直线同时实现这一额外几何约束，而当前路线没有给出相应的禁形或稳定性定理。
- 下一步：固定ε>0，检验高最小度线性4-超图的最小局部构型能否强迫一个在实射影平面不可表示的有限子配置；可先对小规模配置做定向拟阵可实现性筛查。
- 来源核对：[Erdős Problems #101](https://www.erdosproblems.com/101)仍列为OPEN，并记录n^{2−O(1/√log n)}下界。；本地101.lean确实取所有n点、无五点共线配置中四点线数的最大值，再陈述little-o；量词与上述重述一致。；独立复核候选答案的双计数：常数1/12正确，但只能得到O(n²)。
- 时间记账：所在批次墙钟时间按题数均摊约 51.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/101)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/101.lean`；既有候选答案（按不可信材料审计）

### #102

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c>0$ and $h_c(n)$ be such that for any $n$ points in $\mathbb{R}^2$ such that there are $\geq cn^2$ lines each containing more than three points, there must be some line containing $h_c(n)$ many points. Estimate $h_c(n)$. Is it true that, for fixed $c>0$, we have $h_c(n)\to \infty$?
- 题意摘要：较精确地应定义 h_c(n)=min_P max_ℓ|P∩ℓ|，其中|P|=n且至少cn²条不同直线各含≥4点；问题问其数量级及对每个固定、非空可行的c是否h_c(n)→∞。若可行配置集合为空，原表述没有规定h_c(n)。
- 状态核对：截至核验页面仍为 open。需补充可行域约定：当c≥1/12时，对充分大n条件不可能成立，蕴含式会真空为真，不能据此定义有限的“最大保证值”。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：用每条丰富直线消耗的点对数分层，并严格归约到问题101的“是否最终至少有五点共线”子问题。
- 局部结论：若丰富直线数L≥cn²，则6L≤Σ_ℓ C(|P∩ℓ|,2)≤C(n,2)，所以必须 c≤(n−1)/(12n)，且在非空情形h_c(n)≥4。；对固定c>0，“充分大n时h_c(n)≥5”等价于：不存在无五点共线且有至少cn²条四点线的配置。对所有c成立正是问题101的little-o断言。；二维m×m格点给出n=m²且最大共线数≤m=√n。取Θ(m²)个适当的本原方向，每个方向有Θ(m²)条含至少4个格点的线，可得到某个绝对c₀>0下Θ(n²)条丰富线，故至少对0<c≤c₀有h_c(n)=O(√n)。
- 第一阻塞点：分层点对不排除所有丰富线都恰含4点；在这一极端情形它完全退化为问题101。因此该路线第一次无法闭合之处就是无法证明固定正密度的四点线必产生一条五点线。
- 下一步：把格点论证定量化：选定例如m/8≤a,b≤m/6的本原方向，精确计算含四点线的数量和所得c₀；随后研究提高c时h_c(n)的分段上界。
- 来源核对：[Erdős Problems #102](https://www.erdosproblems.com/102)仍列为OPEN，并明确说甚至未知是否能保证5点共线。；官方页面记录高维格点加随机投影给出h_c(n)≪n^{1/log(1/c)}；候选答案对此只作状态总结，没有独立证明其常数与对数底数约定。；候选答案称问题“仅在0<c≤1/12有意义”仍不够精确：c=1/12时对每个有限n也有n(n−1)/12<n²/12，故条件为空。
- 时间记账：所在批次墙钟时间按题数均摊约 51.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/102)；既有候选答案（按不可信材料审计）

### #103

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ count the number of incongruent sets of $n$ points in $\mathbb{R}^2$ which minimise the diameter subject to the constraint that $d(x,y)\geq 1$ for all points $x\neq y$. Is it true that $h(n)\to \infty$?
- 题意摘要：在所有n点集合P⊂R²、两两距离≥1的配置中，令D_n为可达到的最小直径；h(n)是满足diam(P)=D_n的配置按平面欧氏等距（通常包括反射）分类后的非全等类数。问题问h(n)→∞。
- 状态核对：截至核验页面仍为 open，且甚至未知是否对所有充分大n都有h(n)≥2。原题默认h(n)是可比较的有限整数；若极小构型类无限，需要采用扩展解释。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先在归一化配置空间证明极小值达到并估计D_n，再考察极小值集合模欧氏群后的维数：若存在非刚性连续族，立即得到多个乃至无限多个非全等极小构型。
- 局部结论：令x₁=0。直线上间距1的n点给出D_n≤n−1，因此只需在闭球B(0,n−1)^{n−1}内取配置；两两距离≥1是闭条件，故紧致性和直径连续性保证D_n确实达到。；在每个点周围放半径1/2的不交圆盘，其并集直径≤D_n+1。由等直径不等式，nπ/4≤π(D_n+1)²/4，故D_n≥√n−1。；极小配置集合由有限个二次不等式及等式定义，是紧半代数集。若其模等距群后含正维分支，则该n的h(n)不是1，而是无限；因此唯一性只能发生在模刚体运动孤立的极小框架上。
- 第一阻塞点：第一处缺口是从D_n=Θ(√n)或局部致密堆积，推不出精确极小框架的数量。渐近面积估计不识别哪些距离约束在D_n处活跃，也不能证明存在正维分支或两个孤立的非全等最优点。
- 下一步：对小n的极小构型建立接触图：枚举平面单位距离图候选，对每个图用刚性矩阵和区间算术检验其是否为孤立全局极小值；重点寻找可推广的局部“边界换位”操作。
- 来源核对：[Erdős Problems #103](https://www.erdosproblems.com/103)仍列为OPEN，并明确记录h(n)≥2最终成立也未知。；候选答案关于三角格点形状的描述只是启发式，不能用来计数精确极小构型；本筛查未将其作为证明步骤。
- 时间记账：所在批次墙钟时间按题数均摊约 51.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/103)；既有候选答案（按不可信材料审计）

### #104

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given $n$ points in $\mathbb{R}^2$ the number of distinct unit circles containing at least three points is $o(n^2)$.
- 题意摘要：对每个n点集合P⊂R²，记u(P)为圆心任意、半径恰为1且含至少3个P中点的不同圆的数量。命题是U(n)=max_{|P|=n}u(P)满足U(n)/n²→0。
- 状态核对：截至核验页面仍为 open；O(n^{3/2})是更强的悬赏猜测，不是已知上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：对单位圆与其圆上点对做带重双计数，再把每个圆选取一个三点组，尝试由所得3-一致超图的低码数推出次二次。
- 局部结论：若圆C含m_C≥3个点，则Σ_C C(m_C,2)≤2C(n,2)，因为一个点对至多属于两个单位圆。因此3u(P)≤2C(n,2)，即u(P)≤n(n−1)/3。；若u(P)≥εn²，则至少有3εn²个圆—点关联；但这仍与每点线性平均关联数相容。；Elekes型构造可直接核对：取一般位置的单位向量e_i，点集为e_i+e_j；每个三元组{i,j,k}给出以e_i+e_j+e_k为圆心、通过对应三个两两和的单位圆。一般位置保证退化和重合可避开，故n≈s²/2时得到Θ(s³)=Θ(n^{3/2})个圆。
- 第一阻塞点：给每个圆选一个三点组只得到点对码数≤2的3-一致超图，而这类抽象超图允许Θ(n²)条边。圆—圆至多交两点也没有增加约束；缺失的是把“所有三点外接圆半径都恰为1”转化为可累积的代数或能量损失。
- 下一步：把圆按圆上点数m_C分层；先检验能否用单位距离点—圆关联界证明所有m_C≥4的圆贡献o(n²)，从而把核心压缩到恰含3点的单位圆。
- 来源核对：[Erdős Problems #104](https://www.erdosproblems.com/104)仍列为OPEN，记录上界n(n−1)/3和Elekes的Ω(n^{3/2})构造。；独立检查候选构造中的距离：|(e_i+e_j+e_k)−(e_i+e_j)|=|e_k|=1，几何核心正确；圆互异仍需“一般位置”条件，不能无条件断言。
- 时间记账：所在批次墙钟时间按题数均摊约 51.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/104)；既有候选答案（按不可信材料审计）

### #108

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For every $r\geq 4$ and $k\geq 2$ is there some finite $f(k,r)$ such that every graph of chromatic number $\geq f(k,r)$ contains a subgraph of girth $\geq r$ and chromatic number $\geq k$?
- 题意摘要：对每个整数r≥4、k≥2，是否存在有限整数f(k,r)，使每个有限图G只要χ(G)≥f(k,r)，便含一个非必诱导子图H，满足girth(H)≥r且χ(H)≥k；森林的girth按∞处理。
- 状态核对：截至核验页面仍为 open；r=4已知。候选答案的k=3结论可以核实，但其引述和常数说明不够严谨。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先解决边界参数，再对一般k,r尝试随机保留边并从每个长度<r的圈删一条边，同时要求剩余图仍不可(k−1)-着色。
- 局部结论：k=2时f(2,r)=2可取：任一有边图含K₂，K₂无圈且色数2。；若G非二分且最长奇圈长度为ℓ，Erdős–Hajnal界χ(G)≤ℓ+1。因此χ(G)≥r+1时存在长度至少r的奇圈；只保留该圈的边便得到girth≥r、色数3的子图，所以f(3,r)≤r+1。；性质对参数单调：若(r,k)成立，则所有r'≤r、k'≤k也成立。Rödl定理给出r=4对所有k成立。
- 第一阻塞点：随机稀疏化路线的第一处缺口是无法同时控制色数：输入图的顶点数不受χ(G)控制，短圈数量可任意大；删去所有短圈的一条边后，没有仅依赖χ(G)、k、r的下界保证剩余色数。对所有(k−1)-着色做并合界也因顶点数任意大而失效。
- 下一步：先处理下一未解格点(k,r)=(4,5)：把G缩到色临界子图，检验短圈的边击中集是否必能分成有界个二分图；若能证明删除该击中集只损失有界色数，即可形成可迭代引理。
- 来源核对：[Erdős Problems #108](https://www.erdosproblems.com/108)仍列为OPEN，并确认Rödl证明了r=4。；关于k=3，文献摘要记录Erdős–Hajnal界χ(G)≤ℓ+1，其中ℓ为最长奇圈长度：[Kenkre–Vishwanathan](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.20209)。这足以独立重建上述论证。；本地108.lean没有Fintype V限制，却量化任意类型V；官方页面把无限色数版本另列为开放问题，因此该Lean陈述与通常的有限图命题存在潜在量词偏差，不能视为已验证形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 51.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/108)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/108.lean`；既有候选答案（按不可信材料审计）

### #111

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G$ is a graph let $h_G(n)$ be defined such that any subgraph of $G$ on $n$ vertices can be made bipartite after deleting at most $h_G(n)$ edges. What is the behaviour of $h_G(n)$? Is it true that $h_G(n)/n\to \infty$ for every graph $G$ with chromatic number $\aleph_1$?
- 题意摘要：对固定图 G 和正整数 n，令 τ(H) 为把有限图 H 变成二部图所需删除的最少边数，则 h_G(n)=max_{A⊆V(G), |A|=n}τ(G[A])；这里可只看诱导子图，因为 τ 对加边单调。问题问：每个 χ(G)=ℵ₁ 的图是否都满足 h_G(n)/n→∞。
- 状态核对：截至当前官方页面仍列为 open。候选答案正确地区分了已知线性下界和未解决的超线性结论，但它只是现状综述，不是证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：沿“互不相交的固定长度奇圈”路线。删去任意可数顶点集后，剩余图仍有色数 ℵ₁，因而仍含奇圈。按 α<ω₁ 递归选择互不相交的奇圈；奇数长度只有可数多种，故其中某个长度 ℓ=2r+1 出现 ℵ₁ 次。取 q=floor(n/ℓ) 个这样的圈并补足到 n 个顶点。
- 局部结论：τ(H)=|E(H)|−MaxCut(H)，所以每个保留下来的奇圈至少迫使删除一条边。；上述 n 点诱导子图含 q 个顶点互不相交的奇圈，因此 h_G(n)≥floor(n/ℓ)。；从而 liminf h_G(n)/n≥1/ℓ>0；这严格重建了 h_G(n)=Ω_G(n)。
- 第一阻塞点：第一处断点是：固定长度奇圈只给每 ℓ 个顶点一个独立障碍，无法推出每顶点所需删除边数趋于无穷。要得到 h_G(n)/n→∞，必须证明存在二部化边数/顶点数无界的有限子图；χ(G)=ℵ₁ 尚不能由上述打包论证推出这一点。
- 下一步：检验一个明确加强命题：对每个 C，χ(G)=ℵ₁ 是否迫使存在有限 H⊆G 满足 τ(H)>C|V(H)|；先研究它是否能由高奇围长或大量边不交奇圈的打包—覆盖对偶推出。
- 来源核对：[Erdős Problem 111](https://www.erdosproblems.com/111) 仍标为 open，并记录统一线性下界及某个例子的 O(n^{3/2}) 上界。
- 时间记账：所在批次墙钟时间按题数均摊约 45.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/111)；既有候选答案（按不可信材料审计）

### #112

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k=k(n,m)$ be minimal such that any directed graph on $k$ vertices must contain either an independent set of size $n$ or a transitive tournament of size $m$. Determine $k(n,m)$.
- 题意摘要：在通常的 oriented graph 约定下，k(n,m) 是最小 K，使每个 K 点定向图都含一个 n 点无弧集，或一个 m 点传递竞赛图。目标是对所有正整数 n,m 确定该阈值；若允许双向弧，定义及下述归约需另行调整。
- 状态核对：一般情形仍 open。候选答案中“n=2 时 2^{m−1} 且紧”错误：2^{m−1} 是保证竞赛图含 m 点传递子竞赛图的标准递推上界，不是一般已知精确阈值。候选所述更强现代渐近式也未由给定官方材料支持，本筛查不采用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：沿普通 Ramsey 数夹逼。下界：取一个 α<n 且不含 K_m 的无向图并任意定向其边，它既无 n 点独立集，也无 T_m。上界：先给顶点固定线性次序，把每对点染成“无边、向前弧、向后弧”三色，再用三色 Ramsey 定理。
- 局部结论：R(n,m)≤k(n,m)：传递 m-竞赛图的底图必为 K_m。；k(n,m)≤R(n,m,m)：无边色的 n-齐次集是独立集；任一方向色的 m-齐次集按固定次序构成传递竞赛图。；边界值 k(n,2)=n；而 k(2,m) 正是强迫 T_m 的竞赛图阈值，只能立即得到递推上界 k(2,m)≤2^{m−1}。
- 第一阻塞点：Ramsey 夹逼丢失了定向相容性的细节：下界只排除底图 K_m，上界却要求整个 m-团同向齐次；两者间没有可逆归约，因此不能给出 k(n,m) 的精确值或正确主项。
- 下一步：先做可检验的小参数任务：对 m=3，把“无传递三角形”的局部邻域结构写成递推或整数规划，独立复核 k(n,3)≤n²，并枚举小 n 寻找与普通 R(n,3) 的差距。
- 来源核对：[Erdős Problem 112](https://www.erdosproblems.com/112) 确认问题仍 open，并给出 R(n,m)≤k(n,m)≤R(n,m,m) 及 Erdős–Rado 显式上界。；原始题目研究的是定向图/二元关系的传递域；这也说明必须固定是否允许双向弧的约定。
- 时间记账：所在批次墙钟时间按题数均摊约 45.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/112)；既有候选答案（按不可信材料审计）

### #114

- 当前状态：`falsifiable`（冻结清单状态：`open`）
- 精确题面：If $p(z)\in\mathbb{C}[z]$ is a monic polynomial of degree $n$ then is the length of the curve $\{ z\in \mathbb{C} : \lvert p(z)\rvert=1\}$ maximised when $p(z)=z^n-1$?
- 题意摘要：对每个固定次数 n，在所有首一 p∈ℂ[z]、deg p=n 中，比较 lemniscate Λ_p={z:|p(z)|=1} 的总弧长 L(p)，问是否总有 L(p)≤L(z^n−1)，并刻画等号。
- 状态核对：“falsifiable”在官方数据库中的含义仍是开放、但有限次数反例即可推翻，并非已有反例。已知 n=2 成立；Tao 已证明所有充分大的 n 成立且极值者唯一到平移/旋转，因此只剩有限多个小次数。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：先直接重建模型曲线长度。令 w=z^n=1+e^{it}。每个正则点有 n 个根分支，而 dz=(1/n)w^{1/n−1}dw；把所有分支长度相加并积分 t∈[0,2π]。一般极值不从头重证，而核对 Tao 的高次数定理。
- 局部结论：L(z^n−1)=∫₀^{2π}|1+e^{it}|^{1/n−1}dt=2^{1/n}B(1/2,1/(2n))。；由 Beta/Gamma 渐近展开，L(z^n−1)=2n+4log 2+O(1/n)。；Tao 的定理给出：存在 n₀，使 n≥n₀ 时所有首一 p 均满足 L(p)≤L(z^n−1)，等号仅来自相应的平移/旋转模型。
- 第一阻塞点：第一处不能闭合的是把模型积分计算提升为任意 p 的全局上界；这正需要 Tao/Fryntov–Nazarov 的稳定性、临界点和近极值结构分析。现有高次数定理也没有给出输入材料中可直接核验的显式 n₀，故不能据此宣称所有次数已解决。
- 下一步：从 Tao 证明中抽取可计算的阈值 n₀，并对 3≤n<n₀ 建立经区间算术验证的有限维极值程序；任何严格超过模型长度的多项式都会成为有限反例。
- 来源核对：[Tao 的论文摘要](https://arxiv.org/abs/2512.12455) 明确声称解决所有充分大次数。；[Erdős Problem 114](https://www.erdosproblems.com/114) 当前标作 falsifiable，并明确说明仍 open、n=2 已知、高次数已解决。；候选长度公式的 Beta 参数经直接积分核对为 1/(2n)，不能写成 n/2。
- 时间记账：所在批次墙钟时间按题数均摊约 45.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/114)；既有候选答案（按不可信材料审计）

### #117

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be minimal such that any group $G$ with the property that any subset of $>n$ elements contains some $x\neq y$ such that $xy=yx$ can be covered by at most $h(n)$ many Abelian subgroups. Estimate $h(n)$ as well as possible.
- 题意摘要：令 ω(G) 为 G 中两两不交换元素集的最大基数，令 a(G) 为覆盖 G 所需的最少阿贝尔子群数。题目中的假设等价于 ω(G)≤n，而 h(n)=sup_{ω(G)≤n}a(G)，目标是尽量精确估计其增长。
- 状态核对：问题仍 open，但指数级增长已知：存在绝对常数 c₂>c₁>1，使 c₁^n<h(n)<c₂^n。候选答案的 extraspecial 2-群路线可以独立严格重建；其“对所有 n”公式需排除 n=1 等退化小值。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：取阶 2^{2m+1} 的 extraspecial 2-群 E，令 V=E/Z(E)。交换子给 V 一个 2m 维非退化辛形式 B；元素交换当且仅当对应向量正交。于是阿贝尔子群对应全迷向子空间，非交换集对应 B(v_i,v_j)=1 的向量集。
- 局部结论：若 s 个向量满足 B(v_i,v_j)=1（i≠j），对任一线性关系配对各 v_j 可知关系空间至多一维，故 s≤2m+1；利用一个非奇异的 2m 阶“非对角全 1”Gram 矩阵并加入所有基向量之和，可达 s=2m+1。因此 ω(E)=2m+1。；每个全迷向子空间至多有 2^m−1 个非零向量，而 V 有 2^{2m}−1 个非零向量，故任何阿贝尔覆盖至少需 (2^{2m}−1)/(2^m−1)=2^m+1 个子群。；有限辛空间存在由 2^m+1 个拉格朗日子空间组成的 spread；提升到 E 得到同样大小的阿贝尔覆盖。因此 a(E)=2^m+1，并且 h(2m+1)≥2^m+1。另一方面 Pyber 的 |G:Z(G)|≤C^{ω(G)} 配合每个中心陪集包含于 ⟨g,Z(G)⟩，给 h(n)≤C^n。
- 第一阻塞点：extraspecial 族只确定一个具体指数底数下界约 √2；Pyber 上界中的底数来自完全不同的中心指数估计。当前路线没有说明哪类群能同时使非交换团数小、阿贝尔覆盖数更大，因而无法闭合最优指数率。
- 下一步：计算 limsup h(n)^{1/n} 的候选下界：系统比较 extraspecial p-群及其中心积，明确求出 ω(G) 与最小阿贝尔覆盖数，看 p>2 或非经典辛 spread 是否改进 √2。
- 来源核对：[Erdős Problem 117](https://www.erdosproblems.com/117) 确认指数上下界及 open 状态。；[Pyber 1987 论文页面](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms/s2-35.2.287) 的摘要明确给出 |G:Z(G)|≤c^n。
- 时间记账：所在批次墙钟时间按题数均摊约 45.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/117)；既有候选答案（按不可信材料审计）

### #119

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $z_i$ be an infinite sequence of complex numbers such that $\lvert z_i\rvert=1$ for all $i\geq 1$, and for $n\geq 1$ let\[p_n(z)=\prod_{i\leq n} (z-z_i).\]Let $M_n=\max_{\lvert z\rvert=1}\lvert p_n(z)\rvert$. Is it true that $\limsup M_n=\infty$? Is it true that there exists $c>0$ such that for infinitely many $n$ we have $M_n > n^c$? Is it true that there exists $c>0$ such that, for all large $n$,\[\sum_{k\leq n}M_k > n^{1+c}?\]
- 题意摘要：量词是：对每个单位圆上的无限序列 (z_i)，定义 p_n(z)=∏_{i=1}^n(z−z_i) 及 M_n=max_{|z|=1}|p_n(z)|。第一问是否对每个序列 limsup M_n=∞；第二问是否存在绝对 c>0，使每个序列都有无穷多个 n 满足 M_n>n^c；第三问是否存在绝对 c>0，使每个序列对所有充分大 n 都满足 ∑_{k≤n}M_k>n^{1+c}。
- 状态核对：第一问由 Wagner、第二问由 Beck 肯定解决；第三问仍 open。候选对第二问的推论缺少一句必要论证：由 max_{n≤N}M_n>N^c 选出的指标必须无界，否则固定有限多个 M_n 不可能随 N^c 增长。补上后结论成立。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试把 Beck 的稀疏大峰值转化为第三问的累计下界。先用 Jensen 平均和递推 p_{k+1}=p_k(z−z_{k+1}) 控制相邻 M_k。
- 局部结论：对每个单位根 ζ，(2π)^{-1}∫₀^{2π}log|e^{it}−ζ|dt=0；相加得 log|p_n| 的圆周平均为 0，故 M_n≥1，进而 ∑_{k≤n}M_k≥n。；因 |z−z_{k+1}|≤2，M_{k+1}≤2M_k；所以一个峰值 M_j=A 至少给出 M_{j-r}≥A/2^r，峰值前的几项总贡献为 Ω(A)。；Beck 的 max_{j≤N}M_j>N^c 因此确实推出第二问；但对第三问至多直接给出线性基线与稀疏峰值贡献，尚得不到 n^{1+c'}。
- 第一阻塞点：首个断点是缺乏峰值密度或峰值后的下界。递推只有 M_{k+1}≤2M_k，后续加入的根可使当前最大点处因子很小；Beck 的前缀最大值允许峰值极稀疏，不能推出每个大 n 的超线性部分和。
- 下一步：建立并检验一个块版本命题：是否存在固定 δ,c>0，使每个大 N 的区间 [N,(1+δ)N] 内都有某个 k 满足 M_k>N^c；若成立，再结合反向相邻递推可转化为累计增长。先检查 Beck 的证明是否实际含有这种局部化。
- 来源核对：[Erdős Problem 119](https://www.erdosproblems.com/119) 确认 Wagner、Beck 两项已知结果及第三问仍 open。；本地 [119.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/119.lean) 将前两问标为 solved、第三问标为 open。其 p n 使用 range n，正确实现 n 个因子；第三问的 range n 包含 M₀ 而止于 M_{n−1}，与原式有一位移，形式化时应补证渐近等价。
- 时间记账：所在批次墙钟时间按题数均摊约 45.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/119)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/119.lean`；既有候选答案（按不可信材料审计）

### #120

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq\mathbb{R}$ be an infinite set. Must there be a set $E\subset \mathbb{R}$ of positive measure which does not contain any set of the shape $aA+b$ for some $a,b\in\mathbb{R}$ and $a\neq 0$?
- 题意摘要：量词为：对每个无限集 $A\subseteq\mathbb R$，是否存在依赖于 $A$ 的可测集 $E\subseteq\mathbb R$，满足 $m(E)>0$，且对所有 $a\ne0,b\in\mathbb R$ 都有 $aA+b\not\subseteq E$。
- 状态核对：仍为 Erdős similarity problem；截至正式页面 2026-01-23 更新仍开放，甚至 $A=\{2^{-n}:n\ge0\}$ 未知。先前候选只正确报告状态，没有给出证明进展。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先严格完成标准归约，再尝试对收敛序列使用紧致正测集。若 $A$ 无界，取有界正测集；若 $A$ 在某区间稠密，取正测的闭无处稠密集。其余有界无限情形，从 $A$ 选取严格单调子列 $A_0=\{a_n\}$，令 $a_n\to L$，平移后归约为 $a_n\to0$。由于 $A_0\subseteq A$，避开 $A_0$ 的全部仿射像即避开 $A$。再设法构造正测紧集 $E$，使其不含任何 $b+aa_n$。
- 局部结论：无界情形可取 $E=[0,1]$。；若 $A$ 在非退化区间稠密，任取正测闭无处稠密集 $E$；若 $aA+b\subseteq E$，闭性迫使 $E$ 包含一个区间，矛盾。；对 $a_n\to0$ 和紧集 $E$，若 $b+aa_n\in E$ 对所有 $n$，则闭性给出 $b\in E$；故问题化为排除以某点为极限、具有固定比例结构的无限配置。
- 第一阻塞点：第一处缺口是构造一个仍有正测度、同时对不可数参数族 $(a,b)$ 排除全部无限配置的紧集。逐尺度随机删除可以控制固定 $(a,b)$，但尚无一致估计覆盖连续参数空间；有限截断也无济于事，因为有限集合具有 Steinhaus 型普适性。
- 下一步：针对 $A=\{2^{-n}\}$，建立一个可检验的参数离散化引理：若紧集 $E$ 含某个完整仿射副本，证明在每个尺度上存在网格参数 $(a_j,b_j)$，其前 $N_j$ 项均落入 $E$ 的 $O(2^{-N_j})$ 邻域；随后估计这些网格事件概率是否可求和。
- 来源核对：正式状态与困难特例已核对：[Erdős Problem 120](https://www.erdosproblems.com/120)。；本地 Lean 文件准确表达 $\forall A\,\exists E\,\forall a,b$，但主定理仍含 `sorry`，不是证明。
- 时间记账：所在批次墙钟时间按题数均摊约 58.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/120)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/120.lean`；既有候选答案（按不可信材料审计）

### #122

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which number theoretic functions $f$ is it true that, for any $F(n)$ such that $f(n)/F(n)\to 0$ for almost all $n$, there are infinitely many $x$ such that\[\frac{\#\{ n\in \mathbb{N} : n+f(n)\in (x,x+F(x))\}}{F(x)}\to \infty?\]
- 题意摘要：输入字面陈述是：分类算术函数 $f$，使得对每个满足 $f(n)/F(n)\to0$（在密度为 $1$ 的整数集合上）的正函数 $F$，计数比 $N_F(x)/F(x)$ 沿无穷多个 $x$ 趋于无穷，其中 $N_F(x)=\#\{n:n+f(n)\in(x,x+F(x))\}$。但“无穷多个 $x$ 且趋于无穷”还应明确为 $\limsup_{x\to\infty}N_F(x)/F(x)=\infty$。
- 状态核对：输入把关键比值写反了。当前正式页面是 $F(n)/f(n)\to0$，并与 $\omega(n)$ 的已知结果相容。先前候选对输入的字面版本给出的反例思路有效，但其关于负值函数的充分条件未经证明，不应采纳。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `high`
- 尝试路线：先审查字面版本。对任意非负整数值 $f$，取 $F(x)=x^2+f(x)^2$。则由 $2xf(x)\le x^2+f(x)^2$ 得 $f(x)/F(x)\le1/(2x)\to0$。若 $n+f(n)\in(x,x+F(x))$，非负性给出 $n<x+F(x)$，从而计数至多 $x+F(x)+O(1)$。另对正式版本，检验 EPS 的区间聚集路线：把一段较宽的 $n$ 区间经 $n\mapsto n+\omega(n)$ 压入较窄区间。
- 局部结论：对输入的字面版本，$N_F(x)/F(x)\le1+x/F(x)+O(1/F(x))\le1+1/x+o(1)$，故所有非负算术函数都不满足所问性质。；这个反例不依赖 $f$ 的增长规律，因此直接否定先前候选中“标准非负函数或许需要分类”的方向。；对正式版本，EPS 给出的宽度分别约为 $(\log x/\log\log x)^{1/2}$ 与 $(\log\log x)^{1/2}$；若整个前一区间映入后一区间，计数比至少为 $\asymp \sqrt{\log x}/\log\log x\to\infty$。
- 第一阻塞点：无法同时把输入版本与文献状态闭合：二者是相反的渐近条件。对正式版本，区间聚集定理还必须与任意给定的 $F$ 对齐，而不能仅选择一个方便的窗口宽度。
- 下一步：回查 EPS97 原文，固定三项定义：比值究竟是 $F/f$、‘almost all’的密度含义，以及结论是否为 $\limsup=\infty$；在修正陈述后，再把 EPS 的聚集区间嵌入任意 $F$ 的量词。
- 来源核对：当前正式页面明确写 $F/f\to0$：[Erdős Problem 122](https://www.erdosproblems.com/122)。；该页同时说明所考虑的是慢增长算术函数，并记录 $\tau$、$\omega$ 的正面结果，与输入的反向比值不相容。
- 时间记账：所在批次墙钟时间按题数均摊约 58.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/122)；既有候选答案（按不可信材料审计）

### #123

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $a,b,c$ be three integers which are pairwise coprime. Is every large integer the sum of distinct integers of the form $a^kb^lc^m$ ($k,l,m\geq 0$), none of which divide any other?
- 题意摘要：字面量词是：对所有两两互素的整数 $a,b,c$，是否存在 $N$，使每个 $n\ge N$ 都能写成有限个互异数 $a^kb^\ell c^m$ 的和，且所选数在整除偏序下构成反链。标准意图还要求 $a,b,c>1$。
- 状态核对：“proved (Lean)”与证据冲突：正式页面截至 2026-01-20 仍标 OPEN；本地 Lean 主定理也标 `research open` 且证明为 `by sorry`。此外，本地形式化额外加入 $a,b,c>1$，并非输入的字面陈述。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：先检查遗漏的底数限制。若允许正整数 $1$，取 $(a,b,c)=(1,1,1)$；三者两两互素，而可用集合只有 $\{1\}$。互异求和最多得到 $1$，故不是 $d$-complete。对标准的 $a,b,c>1$ 版本，尝试利用已知二底数子系统：若三底数集合包含一个已知 $d$-complete 子集，则其原有反链表示仍是三底数集合中的合法表示。
- 局部结论：输入的字面命题被 $(1,1,1)$ 立即反驳；若‘整数’还允许 $0$ 或负底数，定义问题更严重。；对标准版本，若某两个底数生成的集合已经 $d$-complete，则加入第三个互素底数不会破坏完备性；特别地，已知二底数结果可直接给出一族三底数特例。；反链条件在扩大候选集合时保持：继续使用原表示即可，无须加入新的 summand。
- 第一阻塞点：标准 $a,b,c>1$ 版本的第一处缺口，是从局部区间覆盖或缩放归纳构造表示时，保证新加入的 summand 与递归表示中的全部 summand 互不整除；普通完全序列的贪心论证不控制这一反链条件。
- 下一步：先修正 cohort 状态及底数域；随后对一个未覆盖的小三元组，枚举有限区间中的反链表示，检验能否找到文献型的‘区间覆盖推出全局 $d$-complete’证书。
- 来源核对：正式页面仍为开放问题并要求 $a,b,c\ge1$：[Erdős Problem 123](https://www.erdosproblems.com/123)。；本地 [123.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/123.lean) 明确增加 $a,b,c>1$，主定理仍是 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 58.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/123)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/123.lean`；既有候选答案（按不可信材料审计）

### #124

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $d\geq 1$ and $k\geq 0$ let $P(d,k)$ be the set of integers which are the sum of distinct powers $d^i$ with $i\geq k$. Let $3\leq d_1<d_2<\cdots <d_r$ be integers such that\[\sum_{1\leq i\leq r}\frac{1}{d_r-1}\geq 1.\]Can all sufficiently large integers be written as a sum of the shape $\sum_i c_ia_i$ where $c_i\in \{0,1\}$ and $a_i\in P(d_i,0)$? If we further have $\mathrm{gcd}(d_1,\ldots,d_r)=1$ then, for any $k\geq 1$, can all sufficiently large integers be written as a sum of the shape $\sum_i c_ia_i$ where $c_i\in \{0,1\}$ and $a_i\in P(d_i,k)$?
- 题意摘要：问题含两部分。给有限递增底数 $3\le d_1<\cdots<d_r$，且输入实际假设 $r/(d_r-1)=\sum_i1/(d_r-1)\ge1$。第一问取 $k=0$；第二问另假设 $\gcd(d_1,\dots,d_r)=1$，要求对每个固定 $k\ge1$，所有充分大整数属于 $P(d_1,k)+\cdots+P(d_r,k)$。
- 状态核对：整体仍开放，但第一问已经正面解决并形式化；开放的是 $k\ge1$ 部分。输入条件比通常使用的 $\sum_i1/(d_i-1)\ge1$ 更强。先前候选的 Brown/no-gap 证明路线基本正确。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：重建第一问。将所有带底数标签的幂 $d_i^j$ 排成非降多重序列。设当前每个底数已选到指数 $e_i-1$，下一枚硬币为 $q=\min_i d_i^{e_i}$。此前硬币总和为 $S=\sum_i(d_i^{e_i}-1)/(d_i-1)$。由 $d_i\le d_r$ 和输入假设，得 $\sum_i1/(d_i-1)\ge r/(d_r-1)\ge1$，故 $S\ge q-1$。于是 Brown 无间隙归纳表明每个 $n\ge0$ 都是这些带标签幂的子集和；按底数分组即得 $n=\sum_i a_i$，$a_i\in P(d_i,0)$。对第二问尝试同一归纳。
- 局部结论：第一问不仅对充分大整数成立，而且每个 $n\ge0$ 都可表示。；分组不会违反‘同一底数幂互异’，因为排序的是带底数标签的每个幂各一枚；不同底数间数值相同不影响各自属于不同的 $P(d_i,0)$。；当 $k\ge1$ 时，每个可用幂至少为 $d_i^k$，Brown 归纳在整数 $1$ 处即无法启动；$\gcd(d_i)=1$ 只消除固定同余障碍。
- 第一阻塞点：第二问的第一处缺口是证明某个有限初始区间被尾部幂的子集和完全覆盖。无间隙不等式只能从已覆盖的连续区间向外传播，而删去所有低于 $k$ 的幂后并没有这样的种子区间；互素性本身不提供它。
- 下一步：把已知 $\{3,4,7\}$ 证明抽象成有限证书：明确所需的种子区间长度及一次扩张引理，然后对一般 $D,k$ 检验该证书能否仅由 $\sum_i1/(d_i-1)\ge1$ 与 $\gcd D=1$ 推出。
- 来源核对：正式页面确认第一问已有 Lean 形式化、第二问仍开放：[Erdős Problem 124](https://www.erdosproblems.com/124)。；本地 [124.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/124.lean) 分别将 `erdos124.zero` 标为 solved、`erdos124.ne_zero` 标为 open。
- 时间记账：所在批次墙钟时间按题数均摊约 58.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/124)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/124.lean`；既有候选答案（按不可信材料审计）

### #125

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $A = \{ \sum\epsilon_k3^k : \epsilon_k\in \{0,1\}\}$ be the set of integers which have only the digits $0,1$ when written base $3$, and $B=\{ \sum\epsilon_k4^k : \epsilon_k\in \{0,1\}\}$ be the set of integers which have only the digits $0,1$ when written base $4$. Does $A+B$ have positive density?
- 题意摘要：令 $A,B\subseteq\mathbb N$ 分别为三进制、四进制数字只含 $0,1$ 的数。当前文献口径问的是下渐近密度是否为正，即是否存在 $c>0$，使所有充分大 $x$ 都满足 $|(A+B)\cap[0,x)|\ge cx$。
- 状态核对：已知反例结论是 $\underline d(A+B)=0$，并有 Lean 核验；因此先前候选所称“仍开放”已过时。自然密度为正也随之不可能，但正上密度是否成立仍开放。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 Pach–Pintz/形式化中的尺度空隙机制。Dirichlet 逼近给出任意精度的 $k,m$，使 $3^k$ 与 $4^m$ 相对接近。利用数字集合在 $3^k,4^m$ 尺度上的自相似分块，对任意起始尺度 $M$ 构造更大尺度 $N$，使前缀密度至多乘以 $14/15$。迭代 $r$ 次得某个 $N>M$ 满足密度 $\le(14/15)^r$；令 $r\to\infty$ 即产生趋于无穷的尺度序列 $N_j$，其前缀密度趋于零。
- 局部结论：精确计数为 $|A\cap[0,3^k)|=2^k$、$|B\cap[0,4^m)|=2^m$。；形式化的一步收缩引理迭代后给出：对每个 $r,M$，存在 $N>M$，使 $|(A+B)\cap[0,N)|/N\le(14/15)^r$。；因此存在 $N_j\to\infty$ 使该比值趋于 $0$，从而 $\underline d(A+B)=0$；这严格否定正下密度。
- 第一阻塞点：已知证明路线可以闭合；在本次简述中未展开的核心技术步骤是一步收缩计数：由 $3^k\approx4^m$ 构造缺口并证明密度至多乘 $14/15$。外部 Lean 文件已经形式化闭合该步骤，故它不是现有定理的开放缺口。
- 下一步：独立复核时，应在锁定的 Lean commit 上重新编译 `multiple_gaps_bound_step → exists_sparse_scale → pach_pintz_diophantine_gaps → lower_density_zero` 这条依赖链，并确认所用 `lowerDensity` 与 $[0,N)$ 前缀下密度定义一致。
- 来源核对：正式页面记录 2026-03-30 的反证及零下密度结论：[Erdős Problem 125](https://www.erdosproblems.com/125)。；公开 Lean 证明包含 `pach_pintz_diophantine_gaps` 与 `lower_density_zero`：[formal-conjectures 125.lean](https://github.com/mo271/formal-conjectures/blob/c27415379b5dbe34105d1fdd707994540c4c6fc7/FormalConjectures/ErdosProblems/125.lean)。；本地文件仅保留主证明为 `sorry` 并链接外部正式证明，因此本地占位符本身不能当作核验。
- 时间记账：所在批次墙钟时间按题数均摊约 58.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/125)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/125.lean`；既有候选答案（按不可信材料审计）

### #126

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that if $A\subseteq\mathbb{N}$ has $\lvert A\rvert=n$ then $\prod_{a\neq b\in A}(a+b)$ has at least $f(n)$ distinct prime factors. Is it true that $f(n)/\log n\to\infty$?
- 题意摘要：令 \(\omega_A=\left|\bigcup_{\{a,b\}\in\binom A2}\operatorname{Prime}(a+b)\right|\)。由于题中有序乘积只把每个 \(a+b\) 重复一次，素因子集合不变，故 \(f(n)=\min_{|A|=n}\omega_A\)。问题问：是否对每个固定 \(M\)，充分大时所有 \(n\)-元正整数集都满足 \(\omega_A>M\log n\)。
- 状态核对：截至核查时官方仍列为 open。候选答案声称一般结论 \(n\le2^k\)，但可核对的 Erdős–Turán 界是 \(n<3\cdot2^{k-1}\)；因此不能采用候选中的更强常数。Lean 形式化使用 \(\mathbb N\)，可能包含 0，但这不影响当前渐近路线，正式对应时仍需核对约定。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：设所有两两和的素因子并集为 \(P\)，\(|P|=k\)。尝试把每个 \(a\in A\) 编成关于各 \(p\in P\) 的剩余类/赋值签名，并证明同一签名类至多常数个；若能把每加入一个素数造成的最大容量因子从 2 降到 \(2-o(1)\)，即可得到 \(k/\log n\to\infty\)。
- 局部结论：Erdős–Turán 定理给出 \(n<3\cdot2^{k-1}\)，因而 \(f(n)\ge \log_2 n-O(1)\)。；取 \(A=\{1,\dots,n\}\)，所有素因子均不超过 \(2n\)，所以 \(f(n)\le\pi(2n)=O(n/\log n)\)。；单个素数条件 \(p\mid a+b\) 等价于 \(a\equiv-b\pmod p\)，说明每个 \(p\) 只直接控制“相反剩余类”之间的边，确实具有二分型结构。
- 第一阻塞点：不存在仅依赖单个顶点 \(a\) 的二值签名，能够判定每条边 \(a+b\) 由哪个 \(p\in P\) 整除：整除条件依赖一对互为相反数的剩余类，而且一个和可含多个 \(P\) 中的素数。因而现有编码只能恢复指数底数 2 附近的经典界，无法证明超对数增长。
- 下一步：固定小 \(k\)，把条件写成边覆盖问题：每个 \(p\) 产生若干完全二部图 \(A_r\times A_{-r}\)（另加 \(r=0\) 类），用 SAT/整数规划计算最大 \(|A|\) 的抽象剩余类模型；检验是否存在统一的 \((2-\delta)^k\) 上界，或模型本身已产生接近 \(2^k\) 的障碍。
- 来源核对：[Erdős Problem 126：状态及经典上下界](https://www.erdosproblems.com/126)；已读取本地 Lean 文件；其中 `offDiag` 使用有序对，但不改变不同素因子的集合。
- 时间记账：所在批次墙钟时间按题数均摊约 52.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/126)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/126.lean`；既有候选答案（按不可信材料审计）

### #129

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(n;k,r)$ be the smallest $N$ such that if the edges of $K_N$ are $r$-coloured then there is a set of $n$ vertices which does not contain a copy of $K_k$ in at least one of the $r$ colours. Prove that there is a constant $C=C(r)>1$ such that\[R(n;3,r) < C^{\sqrt{n}}.\]
- 题意摘要：对固定 \(r\ge2\)，\(R(n;3,r)\) 是最小的 \(N\)，使每个 \(K_N\) 的 \(r\)-边染色都含一个 \(n\)-点集 \(S\)，并存在至少一种颜色 \(c\)，使 \(S\) 内没有颜色 \(c\) 的三角形。题述要求 \(R(n;3,r)<C(r)^{\sqrt n}\)。
- 状态核对：虽然页面标签仍为 open，官方说明已明确指出原命题按现有文字为假。候选答案的概率反例路线经常数检查后成立。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：独立均匀随机给 \(K_N\) 的边染 \(r\) 色。对每个 \(n\)-集 \(S\) 和颜色 \(c\)，利用 \(K_n\) 中大量边互不相交的三角形，估计 \(S\) 不含颜色 \(c\) 三角形的概率，再对 \((S,c)\) 作并合界。
- 局部结论：贪心删除三角形，最终余图无三角形；由 Mantel 定理，删除出的边不交三角形数 \(m\ge(\binom n2-n^2/4)/3\ge n(n-2)/12\)。；固定 \((S,c)\)，上述三角形的单色事件相互独立，故 \(\Pr(S\text{ 无颜色 }c\text{ 三角形})\le(1-r^{-3})^m\le e^{-n(n-2)/(12r^3)}\)。；所有坏事件的期望数至多 \(r\binom Nn e^{-n(n-2)/(12r^3)}\)。取 \(N=\lfloor e^{n/(24r^3)}\rfloor\)，该量对充分大 \(n\) 小于 1。因此存在染色，使每个 \(n\)-集在每种颜色中都含三角形，故 \(R(n;3,r)>N=e^{\Omega_r(n)}\)。
- 第一阻塞点：不存在证明断口：这条路线完整反驳了所写上界。唯一未解决的是原作者可能本想表述什么不同的问题；现有定义无法据此恢复。
- 下一步：查阅原始文献 Er97b 的上下文，逐字核对是否漏掉了“某颜色类”或其他量词；在确定修正版前，不应继续尝试 \(C^{\sqrt n}\) 上界。
- 来源核对：[Erdős Problem 129：官方记录的同一概率反例](https://www.erdosproblems.com/129)
- 时间记账：所在批次墙钟时间按题数均摊约 52.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/129)；既有候选答案（按不可信材料审计）

### #130

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{R}^2$ be an infinite set which contains no three points on a line and no four points on a circle. Consider the graph with vertices the points in $A$, where two vertices are joined by an edge if and only if they are an integer distance apart. How large can the chromatic number and clique number of this graph be? In particular, can the chromatic number be infinite?
- 题意摘要：量词是：对任意可能不可数的无限 \(A\subset\mathbb R^2\)，假设无三点共线、无四点共圆；定义 \(G_A\) 的边为正整数距离点对。问题询问 \(\chi(G_A)\) 与 \(\omega(G_A)\) 的可能范围，特别是否存在这样的 \(A\) 使 \(\chi(G_A)\) 无限。
- 状态核对：无限色数问题仍为 open。候选答案中“没有无限团，所以 \(\omega(G_A)<\infty\)”并不严格：一个图可以没有无限团，却含任意大的有限团，从而其团数的上确界为 \(\aleph_0\)。Erdős–Anning 只排除实际的无限完全子图。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试从有限的高色数整数距离图出发，逐步放置点并保持所需整数距离边，同时避开导致三点共线或四点共圆的代数曲线；先检查这一路线能严格给出的上下界。
- 局部结论：把平面分成边长 \(1/2\) 的半开方格，并给每格一个不同颜色。格内直径 \(\sqrt2/2<1\)，故无正整数距离边；因此对任意 \(A\)，\(\chi(G_A)\le\aleph_0\)。若色数无限，它只能是 \(\aleph_0\)。；已知存在七个一般位置且两两整数距离的点，给出 \(K_7\)。从该七点开始，可递归避开旧点对确定的直线、旧三点确定的圆，以及以旧点为圆心、整数为半径的圆；每步只排除可数条曲线。因此可扩充成满足条件的可数无限集，且仍有 \(\chi\ge7\)。；Erdős–Anning 定理说明平面中的无限两两整数距离集必共线；结合无三点共线，\(G_A\) 不可能含无限完全子图。
- 第一阻塞点：整数距离等式在微扰下不会保持。一般位置可通过避开曲线轻易实现，但这样会同时删掉用于维持高色数的整数距离边；目前没有一族色数趋于无穷、且能兼容所有一般位置约束的有限整数距离图可供极限构造。
- 下一步：先做有限目标：搜集或构造满足一般位置的整数距离图 \(H_m\)，并用严格程序证书验证 \(\chi(H_m)>m\)。若连 \(m=8\) 都无法超过已知 \(K_7\)，应定位是距离方程还是共圆条件造成障碍。
- 来源核对：[Erdős Problem 130：开放状态与 Erdős–Anning 结论](https://www.erdosproblems.com/130)；[Kreisel–Kurz：一般位置的七点整数距离构形](https://arxiv.org/abs/0804.1303)
- 时间记账：所在批次墙钟时间按题数均摊约 52.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/130)；既有候选答案（按不可信材料审计）

### #131

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(N)$ be the maximal size of $A\subseteq\{1,\ldots,N\}$ such that no $a\in A$ divides the sum of any distinct elements of $A\backslash\{a\}$. Estimate $F(N)$. In particular, is it true that\[F(N) > N^{1/2-o(1)}?\]
- 题意摘要：\(F(N)\) 是满足下述性质的 \(A\subseteq[N]\) 的最大基数：对每个 \(a\in A\) 及每个由 \(A\setminus\{a\}\) 中互异元素组成的非空子集 \(B\)，都有 \(a\nmid\sum_{b\in B}b\)。一般增长率仍待估计；特别问题问是否有 \(F(N)>N^{1/2-o(1)}\)。
- 状态核对：总体估计仍 open，但特别提出的平方根级下界已经被否定。候选答案的核心归约正确；其声称的具体出版信息未用于结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把非整除集归约为非平均集：若某个 \(a\) 是其他互异元素的平均值，则这些元素之和是 \(|B|a\)，直接违反非整除条件；随后应用非平均集的最新锐界。
- 局部结论：每个非整除集必为非平均集：\(a=|B|^{-1}\sum_{b\in B}b\Rightarrow a\mid\sum_{b\in B}b\)。；Pham–Zakharov 证明 \([N]\) 中最大非平均集大小为 \(N^{1/4+o(1)}\)，故 \(F(N)\le N^{1/4+o(1)}\)。这与 \(N^{1/2-o(1)}\) 相差固定指数，严格否定特别问题。；结合已知 Csaba/ELRSS 构造，目前范围为 \(N^{1/5}\ll F(N)\le N^{1/4+o(1)}\)。
- 第一阻塞点：反向归约失败：非平均性只禁止 \(\sum B=|B|a\)，而非整除性还禁止 \(\sum B=ta\) 的所有整数 \(t\)。因此非平均集的下界不能直接转成同量级的非整除集，无法由现有锐界闭合 \(1/5\) 与 \(1/4\) 的指数间隙。
- 下一步：对已知 \(N^{1/5}\) 构造逐项重建，明确其参数为何损失一个五次方；然后检验采用当前最佳非平均集作为输入时，哪些额外倍数关系 \(\sum B=ta\) 首先破坏构造。
- 来源核对：[Erdős Problem 131：已知上下界](https://www.erdosproblems.com/131)；[Pham–Zakharov：最大非平均集为 \(N^{1/4+o(1)}\)](https://arxiv.org/abs/2410.14624)
- 时间记账：所在批次墙钟时间按题数均摊约 52.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/131)；既有候选答案（按不可信材料审计）

### #132

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{R}^2$ be a set of $n$ points. Must there be two distances which occur at least once but between at most $n$ pairs of points? Must the number of such distances $\to \infty$ as $n\to \infty$?
- 题意摘要：对每个由 \(n\) 个互异平面点组成的集合 \(A\)，令 \(\mu_A(d)=|\{\{x,y\}\subset A:|x-y|=d\}|\)，并令 \(q(A)=|\{d:1\le\mu_A(d)\le n\}|\)。第一问是是否对所有相关 \(A\) 都有 \(q(A)\ge2\)；第二问是 \(\min_{|A|=n}q(A)\to\infty\) 是否成立。
- 状态核对：一般问题仍 open。\(n=4\) 时第一问为假；\(n=5,6\) 已知为真。2026 年版本的一手论文仍只证明凸位置及“不过分凸”的情形，未解决一般情形。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从直径图出发：直径的重数至多 \(n\)，故已有一个合格距离。尝试假设它是唯一合格距离，再用总点对数及不同距离数推出矛盾。
- 局部结论：Hopf–Pannwitz 定理给出直径重数至多 \(n\)，所以对每个 \(A\) 都有 \(q(A)\ge1\)。；若只有直径合格，而不同距离总数为 \(D\)，则其余 \(D-1\) 个距离各至少出现 \(n+1\) 次，故 \(\binom n2\ge1+(D-1)(n+1)\)，即 \(D\le1+(\binom n2-1)/(n+1)\sim n/2\)。；四点反例可直接核验：两个等边三角形沿一条边粘合，边长距离出现 5 次，另一条对角线距离出现 1 次；因 \(n=4\)，只有后一距离合格。
- 第一阻塞点：上面的计数只给出 \(D\lesssim n/2\)，而一般平面点集的已知不同距离下界远低于线性常数 \(1/2\)，故没有矛盾。更关键的是，删去直径边后不能再次直接应用直径图定理，因为剩余边并非某个完整点集的全部最大距离对。
- 下一步：在“唯一合格距离”的反设下研究每个非直径距离对应的单位距离型图；先检验能否证明这些 \(>n\) 边的距离图必须共同强迫大量凸层结构，从而落入 Clemen–Dumitrescu–Liu 已解决的“不过分凸”条件。
- 来源核对：[Erdős Problem 132：状态、小规模结果与四点反例](https://www.erdosproblems.com/132)；[Clemen–Dumitrescu–Liu 2026 v5：凸及不过分凸情形](https://arxiv.org/abs/2505.04283)
- 时间记账：所在批次墙钟时间按题数均摊约 52.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/132)；既有候选答案（按不可信材料审计）

### #137

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$. Can the product of any $k$ consecutive integers $N$ ever be powerful? That is, must there always exist a prime $p\mid N$ such that $p^2\nmid N$?
- 题意摘要：量词为：对每个整数 $k\ge3$，是否不存在正整数 $n$ 使 $N=\prod_{i=0}^{k-1}(n+i)$ 为 powerful；等价地，是否对所有 $n$ 都存在素数 $p$ 满足 $v_p(N)=1$。
- 状态核对：截至 2026-01-20 官方页仍列为 open。先前答案正确区分了 powerful 与 perfect power，但其所述“奇指数大素数”结果没有给出可核查来源，不能纳入证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：利用相邻因子的受控最大公因数，把问题归约到各项的“大素数部分”。若 $p\ge k$，则 $p$ 不可能同时整除两个 $n+i$；因此反例必须使每个出现在某一项中的 $p\ge k$ 都在该项中至少平方整除。
- 局部结论：对 $0\le i<j<k$，有 $\gcd(n+i,n+j)\mid(j-i)$；故任何 $p\ge k$ 至多整除一个因子。；若整个乘积 powerful，则每个 $n+i$ 的 $k$-rough 部分 $R_i=\prod_{p\ge k}p^{v_p(n+i)}$ 本身 powerful；特别地，不允许 $v_p(n+i)=1$。；对 $k=3$，若 $n$ 为奇数，则素数 $2$ 只来自 $n+1$，故反例还必须满足 $v_2(n+1)\ne1$，即 $n\equiv3\pmod4$。
- 第一阻塞点：需要证明某个 $n+i$ 含有指数恰为 $1$ 的素因子 $p\ge k$（或直接在整个乘积中找到指数 $1$ 的素数）。现有最大素因子定理通常只能保证大素因子存在，不能排除该因子以 $p^2$ 或更高次幂整除唯一的一项。
- 下一步：对固定小 $k$ 实施可认证的分段筛：筛出所有含某个 $p\ge k$ 且 $v_p(n+i)=1$ 的区间，只保留每项的 $k$-rough 部分均 powerful 的候选；输出覆盖到明确上界 $X$ 的素数证书，并观察剩余候选能否归入有限个平方曲线。
- 来源核对：官方状态及精确表述核对：[Erdős Problem 137](https://www.erdosproblems.com/137)。；官方页确认 Erdős–Selfridge 仅证明连续整数乘积不是 perfect power；这不能推出非 powerful。
- 时间记账：所在批次墙钟时间按题数均摊约 49.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/137)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/137.lean`；既有候选答案（按不可信材料审计）

### #138

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let the van der Waerden number $W(k)$ be such that whenever $N\geq W(k)$ and $\{1,\ldots,N\}$ is $2$-coloured there must exist a monochromatic $k$-term arithmetic progression. Improve the bounds for $W(k)$ - for example, prove that $W(k)^{1/k}\to \infty$.
- 题意摘要：$W(k)$ 是使每个对 $[N]$ 的二染色在 $N\ge W(k)$ 时必含单色非平凡 $k$ 项等差数列的最小整数。目标是改进随 $k\to\infty$ 的界，示例目标为 $\log W(k)/k\to\infty$。
- 状态核对：截至 2026-06-02 仍 open；官方页现记最佳一般下界为 $W(k)\gg2^k$。先前答案引用的 $2^k/k^{\varepsilon}$ 已不是最佳已知一般下界。其 LLL 证明还未严格证明所用依赖度 $D<kN$，并在最后不等式中忽略了 $D+1$。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：独立随机二染色并对“某个 $k$-AP 单色”应用对称 Lovász 局部引理。显式重算依赖度，避免沿用先前答案中的未经证明常数。
- 局部结论：每个坏事件的概率为 $p=2^{1-k}$。；固定点 $x\in[N]$ 所在的 $k$-AP 数至多 $k\lfloor(N-1)/(k-1)\rfloor$；因此固定 $k$-AP 与至多约 $k^2N/(k-1)$ 个坏事件相依。；由 $ep(D+1)\le1$ 可严格得到某个 $W(k)\ge c\,2^k/k$ 的显式下界；取较小绝对常数即可避开取整边界。但其 $k$ 次根仍只趋近于 $2$。
- 第一阻塞点：这一路线把每个局部约束的概率 $2^{1-k}$ 与约 $kN$ 个依赖事件平衡，天然只给指数底数约为 $2$ 的界；没有机制使 $\log W(k)/k$ 发散。
- 下一步：检验是否能对按公差分层的坏事件建立非对称/簇展开局部引理，使小公差 AP 的强重叠产生可量化收益；首个明确任务是计算每一公差层的依赖矩阵谱半径，而不是只用最大度。
- 来源核对：最新状态与最佳一般下界核对：[Erdős Problem 138](https://www.erdosproblems.com/138)。；官方讨论页说明 Kozik–Shabanov 给出 $W(k)>c2^k$，并纠正了旧的 Szabó 型描述：[discussion](https://www.erdosproblems.com/forum/thread/138)。
- 时间记账：所在批次墙钟时间按题数均摊约 49.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/138)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/138.lean`；既有候选答案（按不可信材料审计）

### #141

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$. Are there $k$ consecutive primes in arithmetic progression?
- 题意摘要：对每个固定整数 $k\ge3$，问是否存在某个指标 $n$ 和公差 $d>0$，使连续素数 $p_n,p_{n+1},\ldots,p_{n+k-1}$ 恰为 $a,a+d,\ldots,a+(k-1)d$；“连续”指它们之间没有其他素数。
- 状态核对：截至 2025-09-28 官方页仍 open；已知存在性验证到 $k\le10$，但即使 $k=3$ 是否有无穷多个仍未知。Green–Tao 不控制 AP 各项之间的额外素数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把问题条件归约到 Dickson/素数 $k$-元组猜想。先用 CRT 强制 AP 项之间的所有整数合数，再要求剩余 $k$ 个线性型同时取素数。
- 局部结论：令 $d=\prod_{q\le k}q$。对每个 $t\in[1,(k-1)d-1]$ 且 $d\nmid t$，选互异素数 $q_t>(k-1)d$，并规定 $a\equiv-t\pmod{q_t}$；于是 $a+t$ 恒被 $q_t$ 整除。；同时规定 $a\equiv1$ 模每个 $q\mid d$。CRT 给出剩余类 $a\pmod M$；取 $a=a_0+Mm$ 后，所有非 AP 位置 $a+t$ 在充分大时均为合数。；目标线性型 $L_j(m)=a_0+jd+Mm$（$0\le j<k$）构成 admissible 系：若素数 $\ell\le k$，则 $\ell\mid d$ 且各常数项非零；若 $\ell>k$，至多 $k<\ell$ 个剩余类不能覆盖全部模 $\ell$。因此 Dickson 猜想若成立，就给出无穷多个所求连续素数 AP。
- 第一阻塞点：最后必须证明这组 admissible 线性型同时无限次取素数，这正是一般 Dickson/素数 $k$-元组猜想的未知情形；现有筛法存在 parity barrier。
- 下一步：把上述 CRT 构造对 $k=3,4$ 写成最小模数的显式线性型，并计算其奇异级数；随后用有界区间搜索检验预测计数是否与 Hardy–Littlewood 主项相符。
- 来源核对：状态、量词及 $k\le10$ 的说明核对：[Erdős Problem 141](https://www.erdosproblems.com/141)。；官方页明确说明 Green–Tao 的素数 AP 不保证这些素数连续。
- 时间记账：所在批次墙钟时间按题数均摊约 49.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/141)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/141.lean`；既有候选答案（按不可信材料审计）

### #142

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r_k(N)$ be the largest possible size of a subset of $\{1,\ldots,N\}$ that does not contain any non-trivial $k$-term arithmetic progression. Prove an asymptotic formula for $r_k(N)$.
- 题意摘要：固定 $k\ge3$，$r_k(N)$ 是 $[N]$ 中不含公差 $d\ge1$ 的 $k$ 项 AP 的集合的最大基数。要求的是当 $N\to\infty$ 时与真实主量等价的渐近公式，而非仅证明密度趋零。
- 状态核对：仍 open，甚至 $k=3$ 的数量级也未知。明确吸收人工评审意见：先前答案把 Szemerédi 定理给出的 $r_k(N)=o(N)$ 称为“渐近公式”，这是错误的；它既不给主项，也不给正确数量级。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试先从极值函数的拼接性质建立极限结构，再判断能否提升为主项。把 $[M+N]$ 分成两个连续区间，分别限制任意 AP-free 集合。
- 局部结论：严格有 $r_k(M+N)\le r_k(M)+r_k(N)$：极值集合在两个区间中的部分分别平移为 $k$-AP-free 集合。；由 Fekete 引理，$r_k(N)/N$ 的极限存在并等于 $\inf_N r_k(N)/N$；Szemerédi 定理进一步说明该极限为 $0$。；另有 $r_k(N)\ge r_3(N)$，因为任何 $3$-AP-free 集合自动不含更长 AP；但已知上下界之间仍相差巨大，无法识别主量。
- 第一阻塞点：次可加性只控制线性尺度，而极限恰为零；它不提供衰减速度。要得到渐近公式，需要匹配构造下界和结构性上界，目前即 $k=3$ 也没有这种匹配。
- 下一步：检验“无进位数字积构造”能否给出带显式损失的近超乘性：选大基数嵌入两个 progression-free 数字集，精确分类进位产生的 AP。先确定是否能推出 $\log r_k(N)/\log N$ 的极限存在。
- 来源核对：官方页明确称渐近公式即使对 $k=3$ 仍遥不可及：[Erdős Problem 142](https://www.erdosproblems.com/142)。；Kelley–Meka 原始预印本只给出强上界而非渐近公式：[Strong Bounds for 3-Progressions](https://arxiv.org/abs/2302.05537)。
- 时间记账：所在批次墙钟时间按题数均摊约 49.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/142)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/142.lean`；既有候选答案（按不可信材料审计）

### #143

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset (1,\infty)$ be a countably infinite set such that for all $x\neq y\in A$ and integers $k\geq 1$ we have\[ \lvert kx -y\rvert \geq 1.\]Does this imply that $A$ is sparse? In particular, does this imply that\[\sum_{x\in A}\frac{1}{x\log x}<\infty\]or\[\sum_{\substack{x <n\\ x\in A}}\frac{1}{x}=o(\log n)?\]
- 题意摘要：对每个可数无限集 $A\subset(1,\infty)$，假设对所有有序的不同元素 $x,y\in A$ 及每个整数 $m\ge1$ 都有 $|mx-y|\ge1$。问是否必有加权级数收敛；另问截断调和和 $H(X)=\sum_{x\in A,x<X}1/x$ 是否为 $o(\log X)$。
- 状态核对：整体仍 open，因为加权级数收敛尚未解决；但第二个结论已由 Koukoulopoulos–Lamzouri–Lichtman 于 2025 年证明。先前答案的核心状态判断正确，但公式中曾出现排版成 $|n,a-b|$ 的歧义，应为 $|n\alpha-\beta|$。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：重建 KLL 定理的直接逆否应用，再用 Abel 分部检查第二结论能否推出第一个。
- 局部结论：KLL 定理说：若 $\limsup H(X)/\log X>0$，则对每个 $\varepsilon>0$ 存在不同 $\alpha,\beta\in A$ 和正整数 $m$ 使 $|m\alpha-\beta|<\varepsilon$。取 $\varepsilon=1$ 与假设矛盾，故严格得到 $H(X)=o(\log X)$。；取 $m=1$ 还立即得到 $A$ 中不同元素间距至少 $1$，所以每个有界区间只含有限多个元素，截断和与 Abel 分部均合法。；Abel 分部给出 $\sum_{a\le X}1/(a\log a)=H(X)/\log X+\int H(t)/(t\log^2t)\,dt$（忽略固定下端项）。仅有 $H(t)=o(\log t)$ 时，被积函数只是 $o(1/(t\log t))$，不足以保证积分收敛。
- 第一阻塞点：KLL 的定性 $o(\log X)$ 没有可积的衰减率；例如抽象增长律 $H(X)=\log X/\log\log X$ 同时满足 $o(\log X)$，但对应上界积分仍按 $\int dt/(t\log t\log\log t)$ 发散。必须进一步利用 dilation separation 的结构，而不能只做部分求和。
- 下一步：从 KLL 的 GCD-graph 论证中提取定量逆定理：检验能否推出 $H(X)\ll\log X/(\log\log X)^{1+\delta}$ 或某个分块可求和估计；任何这样的界经 Abel 分部都会解决第一问。
- 来源核对：官方页确认第二问已解决、第一问仍使整体保持 open：[Erdős Problem 143](https://www.erdosproblems.com/143)。；KLL 预印本摘要中的精确量词已核对：[Erdős's integer dilation approximation problem and GCD graphs](https://arxiv.org/abs/2502.09539)。
- 时间记账：所在批次墙钟时间按题数均摊约 49.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/143)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/143.lean`；既有候选答案（按不可信材料审计）

### #145

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $s_1<s_2<\cdots$ be the sequence of squarefree numbers. Is it true that, for any $\alpha \geq 0$,\[\lim_{x\to \infty}\frac{1}{x}\sum_{s_n\leq x}(s_{n+1}-s_n)^\alpha\]exists?
- 题意摘要：令所有正平方自由数依次为 s_1<s_2<⋯。问题问：对每个固定实数 α≥0，包含跨过 x 的末端间隙在内，M_α(x)=x^{-1}∑_{s_n≤x}(s_{n+1}-s_n)^α 是否有有限极限。量词是“每个固定 α”，不是关于 α 的一致收敛。
- 状态核对：按冻结日期仍开放。Chan 的论文摘要严格给出 0≤α<15/4，而不是 α=15/4；输入官方上下文中的“≤3.75”与论文摘要不一致，应采用前者的严格开区间。先前候选关于“该级数对每个 α 都快速收敛”没有给出可核查依据，本次不采纳。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：按间隙长度 h 分层。令 N_h(x)=#{n:s_n≤x，s_{n+1}-s_n=h}。先证明每个固定 h 的密度 δ_h=lim N_h(x)/x 存在，再将 M_α(x) 截断为 h≤H，最后尝试用一致尾估计令 H→∞。
- 局部结论：对固定 h，“m、m+h 平方自由而 m+1,…,m+h−1 非平方自由”是有限窗口中的局部整除条件。只使用 p≤P 的素数平方时由中国剩余定理得到周期密度；忽略 p>P 的误差至多 O(h∑_{p>P}p^{-2})，故 δ_h 严格存在。；因此对每个固定 H，lim_{x→∞}x^{-1}∑_{s_n≤x, s_{n+1}-s_n≤H}(s_{n+1}-s_n)^α=∑_{h≤H}h^αδ_h。特别地 α=0 时极限为平方自由数密度 6/π²。；若能证明 lim_{H→∞}limsup_{x→∞}x^{-1}∑_{s_n≤x, gap>H}gap^α=0，则全极限存在且等于 ∑_{h≥1}h^αδ_h；这精确隔离了所需的统一可积性。
- 第一阻塞点：第一处不能闭合的是上述大间隙尾项。固定 h 的密度不控制 h 随 x 增长的部分；单纯知道最大间隙为 O(x^{5/26}) 也不足以控制任意高阶矩。
- 下一步：从 Chan 证明中抽取其间隙计数函数 A(x,H)=#{s_n≤x:s_{n+1}-s_n>H} 的显式分段上界，逐段计算 α=15/4 时的 dyadic 尾和，检查端点究竟出现对数发散还是可消除损失。
- 来源核对：[Chan 论文摘要](https://arxiv.org/abs/2310.08448)明确写的是 0≤γ<3.75。；[Erdős Problems #145](https://www.erdosproblems.com/145)仍列为开放，并记录早期范围及 ABC 条件结果。；[Chan 的短区间论文](https://arxiv.org/abs/2110.09990)给出 O(x^{5/26}) 型最大间隙控制，但它本身不推出所有矩。
- 时间记账：所在批次墙钟时间按题数均摊约 50.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/145)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/145.lean`；既有候选答案（按不可信材料审计）

### #146

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $H$ is bipartite and is $r$-degenerate, that is, every induced subgraph of $H$ has minimum degree $\leq r$, then\[\mathrm{ex}(n;H) \ll n^{2-1/r}.\]
- 题意摘要：固定一个二部图 H 和整数 r，使 H 的每个非空诱导子图都有度数≤r的顶点，即 H 为 r-退化。问题断言存在只依赖 H 的常数 C_H，使所有 n 都满足 ex(n,H)≤C_H n^{2−1/r}。这里退化度条件不等于某一侧最大度≤r。
- 状态核对：按冻结日期开放，甚至 r=2 未知。AKS 已证明一般上界 O_H(n^{2−1/(4r)})，而当二分一侧最大度≤r时，目标指数已知。先前候选对这一区分是正确的，但其 DRC 草图只证明后一特殊情形。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：取 H 的退化序 v_1,…,v_m，使每个 v_i 至多有 r 个更早邻点；尝试在一个边数≫n^{2−1/r}的二部宿主图中按该次序嵌入，并用依赖随机选择保证每次所需的至多 r 元共同邻域足够大。
- 局部结论：退化序确实把每个嵌入步骤的已嵌入邻点数限制为 r；这是目标指数出现 1/r 的直接原因。；r=1 时 H 是森林。若宿主图平均度至少 2(|V(H)|−1)，反复删去度小于 |V(H)|−1 的点可得到最小度足够大的子图并贪心嵌入 H，故 ex(n,H)=O_H(n)，与 2−1/r=1 一致。；若 H 的某一二分侧最大度≤r，一次 DRC 可先嵌入另一侧，再利用所有至多 r 元组的大共同邻域嵌入该侧，得到目标阶。
- 第一阻塞点：一般退化序在二分两侧来回嵌入。一次 DRC 只在一个方向提供共同邻域；先嵌入的高次数顶点会把后续候选集任意削薄，无法保证反方向的所有 r 元共同邻域仍大。把“一侧最大度≤r”的证明直接套到退化图正是在此失效。
- 下一步：先处理 r=2 且退化核为单个偶环的最小非特殊结构：写出双侧交替 DRC 所需的候选集不变量，并检验两轮 DRC 后候选集是否仍有 Ω(n^c) 大小；若失败，构造明确的候选集坍缩例。
- 来源核对：[AKS 原论文](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/EE0B02FFBEA4A2910E6183F148C3B68E/S0963548303005741a.pdf/turan_numbers_of_bipartite_graphs_and_related_ramseytype_questions.pdf)核对了 Turán 数对象及其方法来源。；输入所给冻结页面记录的一般指数为 2−1/(4r)，并明确目标结论甚至 r=2 开放；本轮未把检索到的非正式幻灯片当作解决证明。
- 时间记账：所在批次墙钟时间按题数均摊约 50.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/146)；既有候选答案（按不可信材料审计）

### #148

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(k)$ be the number of solutions to\[ 1= \frac{1}{n_1}+\cdots+\frac{1}{n_k},\]where $1\leq n_1<\cdots<n_k$ are distinct integers. Find good estimates for $F(k)$.
- 题意摘要：F(k) 计数严格递增的正整数 k 元组 n_1<⋯<n_k，满足 ∑1/n_i=1。问题不是只问有限性，而是要求 k→∞ 时尽可能精确的增长估计。
- 状态核对：按冻结日期开放。已知最佳量级窗口为 2^{c^{k/log k}}≤F(k)≤c_0^{(1/5+o(1))2^k}。先前候选的小值表未在本轮核验，故不采用；其“双对数下界为 Ω(k/log k)”需把常数写成 log c，并隐含 c>1。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：用剩余和的分母递推给出一个完全初等的有限性及双指数型粗上界；同时对每个展开式分裂最大分母，构造到下一层的显式单射。
- 局部结论：设 R_j=1−∑_{i≤j}1/n_i>0，P_j=∏_{i≤j}n_i。因 R_j 的既约分母整除 P_j，有 R_j≥1/P_j；又剩余 k−j 项均≤1/n_{j+1}，故 n_{j+1}≤(k−j)P_j。；令 B_1=k，B_{j+1}=(k−j)∏_{i≤j}B_i，则归纳得 n_j≤B_j，因而 F(k)≤∏B_j=exp(O(2^k log k))。这严格证明有限性并得到粗双指数上界，但弱于已知的 exp(O(2^k))。；对最大分母 M 使用 1/M=1/(M+1)+1/[M(M+1)]。两个新分母都大于原有其余分母，且从新展开式的两个最大分母可恢复 M，所以这是单射，得到 F(k+1)≥F(k)。
- 第一阻塞点：递推中用 R_j≥1/P_j 丢掉了剩余分子、互素性以及严格递增条件的绝大多数信息，产生额外 log k；分裂单射每个解只产生一个后继，也远不足以给出已知的双指数下界。
- 下一步：对固定前 k−4 个分母，把剩余有理数归约为 m/n，并复现 Elsholtz–Planitzer 的四项分母参数计数；可检验目标是从上述递推上界中消去 log k，而不是直接追求最佳常数 1/5。
- 来源核对：[Erdős Problems #148](https://www.erdosproblems.com/148)核对了冻结输入中的最佳上下界及归属。；[Elsholtz–Planitzer 原论文](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.12452)按递增顺序计数，并给出四项及更多项的上界。；[Konyagin 论文记录](https://m.mathnet.ru/eng/mzm10417)核对了双指数下界论文的题名、作者和出版信息。
- 时间记账：所在批次墙钟时间按题数均摊约 50.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/148)；既有候选答案（按不可信材料审计）

### #149

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph with maximum degree $\Delta$. Is $G$ the union of at most $\tfrac{5}{4}\Delta^2$ sets of strongly independent edges (sets such that the induced subgraph is the union of vertex-disjoint edges)?
- 题意摘要：对任意有限简单图 G，最大度为 Δ。问能否用至多 (5/4)Δ² 个诱导匹配覆盖其全部边。覆盖可改成划分，因为诱导匹配的子集仍是诱导匹配；等价地问 χ(L(G)²)≤(5/4)Δ²。
- 状态核对：按冻结日期仍开放。已知一般渐近上界为 1.772Δ²（充分大 Δ）。先前候选关于 Δ=4 的“最佳为21”等附加信息不在输入来源中，本轮未独立核验，故不采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先严格重建冲突图 L(G)² 的贪心上界与 C_5 膨胀下界，再尝试把贪心着色改进为利用冲突邻域稀疏性的着色。
- 局部结论：对边 e=uv，与 e 在 L(G)² 中相邻的边至多来自 u、v 的邻边以及这些邻边另一端的邻边，总数≤2Δ(Δ−1)。故贪心给出 χ'_s(G)≤2Δ²−2Δ+1。；当 Δ=2t 时，把 C_5 的每个顶点替换为 t 个独立点、相邻点簇间放完全二部图。所得图为 Δ-正则且有 5t²=(5/4)Δ² 条边。任意两条边若不相交，其端点间仍有交叉边，因此每个诱导匹配至多含一条边；目标常数不能下降。；故困难不是遗漏一个简单计数：冲突图的最大度约 2Δ²，而极值例本身形成大小 (5/4)Δ² 的团；需要利用非极值邻域的缺边来节省颜色。
- 第一阻塞点：局部稀疏着色需要对每个 e 统一上界 L(G)²[N(e)] 的边数，并在接近 C_5 膨胀的高密度情形给出稳定性分解。仅有最大度计数不能把常数从 2 降到 5/4；即使团数≤5Δ²/4也不会自动控制色数。
- 下一步：固定 e=uv，把距离至多2的冲突边按其经由 u 或 v 的第一步分类，建立邻域边数的精确二次优化；检验“超过目标稀疏阈值时，G 在 e 附近必须接近五簇结构”的稳定性命题。
- 来源核对：[Erdős Problems #149](https://www.erdosproblems.com/149)核对了等价表述、贪心界、C_5 膨胀和开放状态。；[Hurley–de Joannis de Verclos–Kang 原论文页面](https://www.advancesincombinatorics.com/article/38107-an-improved-procedure-for-colouring-graphs-of-bounded-local-density)说明其局部稀疏着色方法及应用。；[作者存档摘要](https://hdl.handle.net/11245.1/aa4ecb9f-a277-4258-969e-705b51460ef0)明确给出充分大 Δ 时的 1.772Δ²。
- 时间记账：所在批次墙钟时间按题数均摊约 50.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/149)；既有候选答案（按不可信材料审计）

### #151

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For a graph $G$ let $\tau(G)$ denote the minimal number of vertices that include at least one from each maximal clique of $G$ on at least two vertices (sometimes called the clique transversal number). Let $H(n)$ be maximal such that every triangle-free graph on $n$ vertices contains an independent set on $H(n)$ vertices. If $G$ is a graph on $n$ vertices then is\[\tau(G)\leq n-H(n)?\]
- 题意摘要：τ(G) 是击中 G 的每个含至少两点的极大团所需的最少顶点数；孤立点形成的单点极大团不计。H(n)=min{α(F):|V(F)|=n，F 无三角形}。问题问每个 n 点图 G 是否都有 τ(G)≤n−H(n)。
- 状态核对：按冻结日期开放，输入称甚至 K_4-free 情形也未解决。先前候选对三角形自由情形的等式正确；其 n−√(2n)+O(1) 可由相关问题页和原论文记录支持，但不是目标结论。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把极大团族视为超图，并尝试为每个非平凡极大团选择一条代表边，使所有代表边组成三角形自由图 Q；若成功，Q 的大独立集将给出所需团超图独立集。
- 局部结论：令 𝒞 为所有非平凡极大团。T 是团横截集当且仅当 S=V(G)\T 不完整包含任何 C∈𝒞。因此目标等价于寻找 |S|≥H(n) 的 𝒞-独立集。；若能为每个 C∈𝒞 选边 e_C⊂C，使 Q=(V,{e_C:C∈𝒞}) 三角形自由，则 Q 有大小至少 H(n) 的独立集 S；S 不含任何 e_C，因而不含任何 C，立即推出目标不等式。；当 G 本身三角形自由时，每个非平凡极大团就是一条边，可取 Q=G；于是 τ(G) 是最小点覆盖数 n−α(G)，从而 τ(G)≤n−H(n)。
- 第一阻塞点：第一处无法闭合的是代表边选择引理：不同极大团所选的三条边可能形成三角形，而逐个改选一条边可能制造新的三角形；目前没有势函数或局部引理保证全局可选。该引理若成立会直接解决原问题，不能把它当作显然事实。
- 下一步：先对 K_4-free 图建立代表边选择问题的最小反例条件：枚举一个三角形 abc 的三条边分别由哪些极大三角形强迫，并检验对应的三角形超图是否总有无三角形的边横截；这是输入中特别指出仍困难的首个情形。
- 来源核对：[1992 年原论文书目信息与摘要](https://www.sciencedirect.com/science/article/pii/0012365X92906815)核对了 τ 所击中的是按包含关系极大的团。；[问题汇编页面](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/CliqueTransversal.html)记录目标不等式、H(n)=Θ(√(n log n)) 量级以及 n−√(2n)+O(1) 的旧上界。
- 时间记账：所在批次墙钟时间按题数均摊约 50.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/151)；既有候选答案（按不可信材料审计）

### #152

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：For any $M\geq 1$, if $A\subset \mathbb{N}$ is a sufficiently large finite Sidon set then there are at least $M$ many $a\in A+A$ such that $a+1,a-1\not\in A+A$.
- 题意摘要：量词为：对每个整数 M≥1，存在 n₀(M)，使每个有限 Sidon 集 A⊂ℕ（即无序二元和表示唯一）只要 |A|≥n₀，其和集 S=A+A 中满足 s−1,s+1∉S 的元素至少有 M 个。
- 状态核对：已于 2026 年肯定解决，而且得到二次量级下界。旧候选称其仍开放，已经过时；其引用的一侧缺邻居估计也不足以解决本题。讨论中另有“由 ESS94 立即推出更强界”的说法，但作者随后明确撤回，故未采用。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建已形式化的组合计数路线。令 n=|A|、S=A+A、D=A−A、I(S)=|{s∈S:s±1∉S}|，并令 N_k(X)=|X∩(X−k)|。先对有限整数集建立邻接点、距离 1、2、3 点对间的指标不等式；再用 Sidon 唯一性把 a+b+k=c+d 的四元组计数从 S 转移到 D。代入 k=1,2,3 后消去中间邻接项，得到 16I(S)+100n+16≥n²。
- 局部结论：Sidon 性给出 |S|=n(n+1)/2，并使每个非零有向差至多有一种表示，故 |D|=n(n−1)+1≤n²。；形式化计数链闭合为 I(S)≥(n²−100n−16)/16，因此孤立和不仅趋于无穷，而且为 Ω(n²)。；给定 M，只需取 n₀ 使 n₀²−100n₀−16≥16M；则所有 |A|≥n₀ 的 A 均有 I(A+A)≥M。
- 第一阻塞点：无数学缺口：关键的指标不等式、四元组转移及边界修正已有完整 Lean 证明。当前 cohort 文件中的定理体仍写作 sorry，但它明确链接到固定提交中的完整证明。
- 下一步：若做进一步审计，应逐条把四元组转移界和最终消元式从固定 Lean 提交翻译成纸笔引理，并核对自然数端点 s=0 的 +16 修正。
- 来源核对：[官方题页确认 PROVED 及 Ω(|A|²) 强化](https://www.erdosproblems.com/152)。；[官方讨论给出不等式、证明骨架、撤回的 ESS94 误证及澄清](https://www.erdosproblems.com/forum/thread/152)。；[固定提交中的 Lean 形式化证明](https://github.com/mo271/formal-conjectures/blob/29c60aa79729701905cf9e92517af23f588971f2/FormalConjectures/ErdosProblems/152.lean)。
- 时间记账：所在批次墙钟时间按题数均摊约 53.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/152)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/152.lean`；既有候选答案（按不可信材料审计）

### #153

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be a finite Sidon set and $A+A=\{s_1<\cdots<s_t\}$. Is it true that\[\frac{1}{t}\sum_{1\leq i<t}(s_{i+1}-s_i)^2 \to \infty\]as $\lvert A\rvert\to \infty$?
- 题意摘要：其统一量词是：令 A 遍历有限 Sidon 集，S=A+A={s₁<⋯<s_t}，其中 t=n(n+1)/2、n=|A|；是否对每个 R>0，存在 n₀，使 n≥n₀ 时所有 A 都满足 t⁻¹∑_{i<t}(s_{i+1}−s_i)²≥R？
- 状态核对：自然语言问题截至核对时仍为 open。旧候选正确指出“大间隙存在”本身不控制全部间隙的二阶矩，但其外围文献断言未在本次筛查中采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试由跨度和 Cauchy–Schwarz 强迫二阶矩。设 d_i=s_{i+1}−s_i。Sidon 集 A={a₁<⋯<a_n} 的正差两两不同，故 diam(A)=a_n−a₁≥n(n−1)/2；于是 ∑d_i=2diam(A)≥n(n−1)。再用 ∑d_i²≥(∑d_i)²/(t−1)。
- 局部结论：得到严格下界 (1/t)∑d_i²≥n²(n−1)²/[t(t−1)]，其极限为 4；因此该路线只能给常数下界。；若仅知一个最大间隙 L(n)→∞，其对目标平均量的贡献只有 L(n)²/t；例如 L(n)=O(log n) 远不足以推出发散。；本地 Lean 文件并未忠实形式化原题：它把总和除以 n=|A|，不是除以 t=|A+A|。对该错误版本，上述 Cauchy 下界约为 2n，实际上已足以推出发散。
- 第一阻塞点：第一处无法闭合的是把固定的跨度下界升级为超常数的间隙平方能量；Cauchy 在近乎均匀间隙时取等，而 Sidon 性尚未被证明能排除这种全局近均匀性。
- 下一步：先修正 153.lean 的归一化分母为 (A+A).card；数学上下一项可检验任务是证明或计算是否存在绝对 ε>0 及趋于无穷的 L(n)，使每个 n 元 Sidon 集至少有 εt/L(n) 个间隙不小于 L(n)。这会直接给二阶矩下界 εL(n)。
- 来源核对：[官方题页确认原式分母为 t 且状态为 OPEN](https://www.erdosproblems.com/153)。；已读取本地 153.lean：定义 f(n) 的求和项除以 n，与原题不一致。
- 时间记账：所在批次墙钟时间按题数均摊约 53.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/153)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/153.lean`；既有候选答案（按不可信材料审计）

### #155

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(N)$ be the size of the largest Sidon subset of $\{1,\ldots,N\}$. Is it true that for every $k\geq 1$ we have\[F(N+k)\leq F(N)+1\]for all sufficiently large $N$?
- 题意摘要：定义 F(N)=max{|A|:A⊂{1,…,N} 为 Sidon 集}。问题是：对每个固定整数 k≥1，是否存在 N₀(k)，使所有 N≥N₀(k) 均有 F(N+k)≤F(N)+1？N₀ 可以依赖 k。
- 状态核对：仍为 open。旧候选对 k=1 的删除论证正确；其有限计算数据与渐近界未作为证明依据。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把问题归约为 F 的单位跳跃点间距。单点扩张给 0≤F(N+1)−F(N)≤1，因此 F(N+k)−F(N) 正好是区间 (N,N+k] 内单位跳跃的个数。原命题等价于：对每个固定 k，充分大的两个跳跃点之间距离大于 k。另取极值 Sidon 集并按 [N] 与尾段拆分。
- 局部结论：删除 N+1（若存在）严格证明 F(N+1)≤F(N)+1；故 k=1 对所有 N 成立。；将 A⊂[N+k] 分成 A∩[N] 与 A∩{N+1,…,N+k}，平移尾部后仍为 [k] 中 Sidon 集，故 F(N+k)≤F(N)+F(k)。；若结论失败，则存在无穷多个 N，使长度 k 的窗口含至少两个跳跃点；因此问题可精确改写为排除渐近的局部跳跃聚簇。
- 第一阻塞点：分块只利用了两部分各自的 Sidon 性，完全丢失跨块和的碰撞约束，因而停在 +F(k)；已知 F(N) 的全局平方根级渐近也不能排除相邻的两个单位跳跃。
- 下一步：对固定小 k 做可验证的结构枚举：从满足 F(N+k)≥F(N)+2 的极值集提取尾部至少两个元素，分类其与前部差集必须避开的模式；目标是得到一个只依赖 k、但随 F(N) 增长最终矛盾的禁差引理。
- 来源核对：[官方题页确认量词、OPEN 状态及更强的 k≈ε√N 猜想](https://www.erdosproblems.com/155)。；本地 155.lean 的 eventually-atTop 量词与自然语言陈述一致。
- 时间记账：所在批次墙钟时间按题数均摊约 53.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/155)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/155.lean`；既有候选答案（按不可信材料审计）

### #156

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does there exist a maximal Sidon set $A\subset \{1,\ldots,N\}$ of size $O(N^{1/3})$?
- 题意摘要：“O(N^{1/3})”应理解为一个统一族：是否存在常数 C、N₀，使每个 N≥N₀ 都存在按包含关系极大的 Sidon 集 A_N⊂[N]，且 |A_N|≤CN^{1/3}；这里 maximal 不是最大基数 maximum。等价地，最小极大集大小 m(N) 是否为 O(N^{1/3})。
- 状态核对：仍为 open；已知下界 Ω(N^{1/3})，官方记录的构造上界为 O((N log N)^{1/3})。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先严格重建覆盖下界，再考察随机种子后贪心补全的构造路线。若 A 是极大 Sidon 集且 x∈[N]\A，则加入 x 必产生涉及 x 的新和碰撞；只能是 x+a=b+c，或 2x=b+c，其中 a,b,c∈A。故每个未选 x 都落入 A+A−A 或满足 2x∈A+A。
- 局部结论：有覆盖 [N]⊂A∪(A+A−A)∪{x:2x∈A+A}。；若 m=|A|，粗计数给 N≤m+m³+m²，从而每个极大 Sidon 集都有 m=Ω(N^{1/3})。；若能构造大小 O(N^{1/3}) 的 Sidon 种子 B，使其阻塞集覆盖除 O(N^{1/3}) 个点外的 [N]，再逐点极大扩张，便会得到所求上界；这给出具体的覆盖设计归约。
- 第一阻塞点：第一处缺口是同时控制“B 保持 Sidon”与三元阻塞集 B+B−B 的近完全覆盖。独立随机选点会产生过多加法碰撞；删除冲突后，覆盖事件高度相关，现有简单二阶矩估计会损失对数因子。
- 下一步：在有限域 Sidon 模板上检验随机投影/平移族：明确计算每个 x 被 B+B−B 覆盖的概率及两点未覆盖事件的协方差；目标是把期望未覆盖数压到 O(N^{1/3})，同时保持 |B|=O(N^{1/3})。
- 来源核对：[官方题页确认 OPEN、Ω(N^{1/3}) 下界及 Ruzsa 的 O((N log N)^{1/3}) 上界](https://www.erdosproblems.com/156)。；输入未提供本地形式化文件，因而没有可核对的 Lean 量词。
- 时间记账：所在批次墙钟时间按题数均摊约 53.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/156)；既有候选答案（按不可信材料审计）

### #158

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{N}$ be an infinite set such that, for any $n$, there are most $2$ solutions to $a+b=n$ with $a\leq b$. Must\[\liminf_{N\to\infty}\frac{\lvert A\cap \{1,\ldots,N\}\rvert}{N^{1/2}}=0?\]
- 题意摘要：对每个无限 A⊂ℕ，若对所有整数 n，方程 a+b=n 在 a,b∈A、a≤b 下至多有两组解，即 A 为 B₂[2] 集，是否必有 liminf_{N→∞}|A∩[1,N]|/√N=0？
- 状态核对：仍为 open。g=1 的无限 Sidon 情形已知成立，但允许第二种表示后，现有筛查路线不能保留足够的唯一性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先尝试有限前缀能量计数。令 B=A∩[1,N]、m=|B|。共有 m(m+1)/2 个无序二元组，其和落在 [2,2N]，每个和值容纳至多两组；再尝试把该估计施加到几何增长的前缀或区间，以反证一致下界 m≥c√N。
- 局部结论：直接计数严格给出 m(m+1)/2≤2(2N−1)，所以 m≤(√(32N−15)−1)/2；这只给 O(√N)，不能令归一化密度趋于零。；同样论证平移后适用于任意长度 L 的整数区间：其中 A 的点数为 O(√L)。；假设 liminf>0 仅给所有充分大前缀 A(N)≥c√N；它与上述 O(√N) 上界相容，故单尺度容量计数不会产生矛盾。
- 第一阻塞点：第一处缺口出现在跨尺度累积：g=1 时相等差/和的唯一性可将许多尺度的计数损失叠加；g=2 允许每个和出现第二次，恰好吸收了当前配对论证产生的碰撞，无法推出某个前缀必须稀疏。
- 下一步：建立带重数的 dyadic 能量表：对 I_j=(2^j,2^{j+1}] 记录块内和与相邻块交叉和，在线性规划中加入每个和值总容量 2；先检验“所有大 N 均有 A(N)≥c√N”是否已与任意有限层数的这些约束矛盾。若始终可行，就能精确定位还缺少哪类三块相关约束。
- 来源核对：[官方题页确认 B₂[2] 的无序表示量词、OPEN 状态及 g=1 已知结论](https://www.erdosproblems.com/158)。；本地 158.lean 使用 Iio N 而非 [1,N]，并允许自然数 0；两者只造成 O(1) 边界差，除以 √N 后等价。
- 时间记账：所在批次墙钟时间按题数均摊约 53.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/158)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/158.lean`；既有候选答案（按不可信材料审计）

### #159

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：There exists some constant $c>0$ such that $$R(C_4,K_n) \ll n^{2-c}.$$
- 题意摘要：求证存在绝对常数 c,C>0 及 n₀，使所有 n≥n₀ 都有 R(C₄,K_n)≤Cn^{2-c}；等价地，每个独立数小于 n 的 C₄-free 图，其顶点数至多 Cn^{2-c}。
- 状态核对：截至官方条目 2026-03-07 更新仍为 open。先前候选把下界写成 n^{3/2}/log n，与条目所列 n^{3/2}/(log n)^{3/2} 不符，不能采纳。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：从 C₄-free 图的共邻点约束出发，尝试推出比平方根更强的独立集下界。若 G 有 N 个顶点，则任意两点至多有一个公共邻点，故 Σ_v binom(d(v),2)≤binom(N,2)。结合凸性控制平均度，再用 Caro–Wei 贪心估计 α(G)。
- 局部结论：由共邻点计数严格得到 Σ_v d(v)(d(v)-1)≤N(N-1)，因而平均度 d̄≤(1+o(1))N^{1/2}。；Caro–Wei 给出 α(G)≥Σ_v1/(d(v)+1)≥N/(d̄+1)≥(1-o(1))N^{1/2}。；因此该路线直接只能推出 N≲α(G)^2，即 R(C₄,K_n)=O(n²)，没有固定幂次节省。
- 第一阻塞点：第一处缺口是把局部二阶矩约束升级为 α(G)≥N^{1/2+ε}。上述共邻点不等式本身只给平方根量级；已知 Szemerédi 对数改进需要更细的多尺度/局部稀疏分析，而现有论证没有产生固定 ε。
- 下一步：检验强化命题：对每个 C₄-free 图，是否可从若干度层中抽出诱导子图 H，使 |H|/d(H) 至少为 N^{1/2+ε}；先在极图、射影平面型图及 Spencer 型随机构造上计算该比值，排除错误的度分层引理。
- 来源核对：[官方条目 #159](https://www.erdosproblems.com/159)仍列界 n^{3/2}/(log n)^{3/2}≪R(C₄,K_n)≪n²/(log n)²，并标记 open。
- 时间记账：所在批次墙钟时间按题数均摊约 51.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/159)；既有候选答案（按不可信材料审计）

### #160

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(N)$ be the smallest $k$ such that $\{1,\ldots,N\}$ can be coloured with $k$ colours so that every four-term arithmetic progression must contain at least three distinct colours. Estimate $h(N)$.
- 题意摘要：h(N) 是最小颜色数 k，使存在 χ:[N]→[k]，且对所有整数 x,d≥1、x+3d≤N，四点 x,x+d,x+2d,x+3d 至少出现三种颜色。
- 状态核对：截至官方条目 2025-12-02 更新仍为 open；已知窗口为 exp(c(log N)^{1/9})≲h(N)≲N^{log3/log22+o(1)}。候选对 Hunter 构造只给了未证明的“ABBA 着色”描述，不能视为重建了上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：走下界路线：证明每个单色类在初始区间 [M]（M=⌊2N/3⌋）中无三项等差数列，再调用 r₃(M) 的已知上界。
- 局部结论：若 x,x+d,x+2d≤M 同色，则 d≤(x+2d)/2≤M/2≤N/3，故 x+3d≤N；所得四项等差数列至多使用两色，矛盾。因此每个 A_i∩[M] 都是 3-AP-free。；于是 M=Σ_i|A_i∩[M]|≤k r₃(M)，严格得到 h(N)≥M/r₃(M)。；代入 Bloom–Sisask 型界 r₃(M)≤M exp(-c(log M)^{1/9})，得到 h(N)≥exp(c'(log N)^{1/9})。
- 第一阻塞点：该归约只逐个约束单色类，完全没有利用更强事实“A_i∪A_j 对每对颜色 i,j 都无 4-AP”。因此到达现有 Roth 型下界后无法继续逼近多项式规模。
- 下一步：建立并检验一个双类密度引理：若 A,B⊂[N] 且 A∪B 无 4-AP，能否用 |A|、|B|及能量 E(A,B) 给出比单独 3-AP-free 更强的联合上界；先对 N≤200 做穷举/整数规划，寻找可能的正确指数和反例。
- 来源核对：[官方条目 #160](https://www.erdosproblems.com/160)确认当前上下界。；[MathOverflow 原构造](https://mathoverflow.net/questions/410808/what-are-bounds-on-this-van-der-waerden-esque-problem)明确给出 F_p³ 中扭曲三次曲线划分及 N^{2/3} 上界；未据此擅自声称验证 Hunter 的更强乘积构造。
- 时间记账：所在批次墙钟时间按题数均摊约 51.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/160)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/160.lean`；既有候选答案（按不可信材料审计）

### #161

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha\in[0,1/2)$ and $n,t\geq 1$. Let $F^{(t)}(n,\alpha)$ be the largest $m$ such that we can $2$-colour the edges of the complete $t$-uniform hypergraph on $n$ vertices such that if $X\subseteq [n]$ with $\lvert X\rvert \geq m$ then there are at least $\alpha \binom{\lvert X\rvert}{t}$ many $t$-subsets of $X$ of each colour. For fixed $n,t$ as we change $\alpha$ from $0$ to $1/2$ does $F^{(t)}(n,\alpha)$ increase continuously or are there jumps? Only one jump?
- 题意摘要：输入文字写“最大的 m”，但正确问题是最小阈值 m：存在对 K_n^{(t)} 的二染色，使每个 |X|≥m 的顶点集内，两色各占至少（通常应作严格正于）αbinom(|X|,t)。研究 α 从 0 趋近 1/2 时该最优阈值的渐近尺度是否发生多次跃迁。
- 状态核对：必须吸收人工评审：largest 是排版错误，先前候选据此令 m=n 并“解决”问题是无效论证。另有第二个端点问题：若 α=0 且使用“至少”，条件恒真，不可能成为通常 Ramsey 函数；“α=0 是 Ramsey 情形”要求严格不等式或单独定义端点。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：采用修正后的最小阈值，并对固定 α∈(0,1/2)作随机染色。先用子集平均证明只需控制恰好 m 个顶点的集合，再对 Bin(binom(m,t),1/2) 的下尾作并合界。
- 局部结论：若某个 s>m 的集合在一种颜色中少于 αbinom(s,t) 条边，随机取其 m-子集，期望同色边数少于 αbinom(m,t)，故存在坏的 m-子集；因此控制所有 m-集即可。；固定 m-集坏掉的概率至多 2exp(-D(α‖1/2)binom(m,t))。与 binom(n,m) 作并合界可得 F^{(t)}(n,α)≤C_{t,α}(log n)^{1/(t-1)}。；对 t=3，Conlon–Fox–Sudakov 保证任意染色含大小 c_α√log n 的几乎单色集；与随机上界合并，固定 α>0 时为 Θ_α(√log n)。
- 第一阻塞点：随机论证的常数在 α↓0 时不能与 α=0 的最优 Ramsey 染色结构衔接；它只说明每个固定正 α 的尺度。第一处真正未闭合的是排除 α=α(n)→0 时出现额外中间尺度或多个跃迁。
- 下一步：令 q=αbinom(m,t) 分区讨论 q<1、q=O(1)、q→∞，对随机染色尾概率作统一估计，并与反 Ramsey 构造拼接；先确定首次可能跃迁是否必须位于 α≈1/binom(m,t)。
- 来源核对：[官方条目 #161](https://www.erdosproblems.com/161)现已把 largest 更正为 smallest，并记录 t=3 的单一固定-α 跃迁结论。；[Conlon–Fox–Sudakov 原论文](https://arxiv.org/abs/0901.3912)证明三元超图中存在 c√log N 大小的几乎单色子集。
- 时间记账：所在批次墙钟时间按题数均摊约 51.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/161)；既有候选答案（按不可信材料审计）

### #162

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha>0$ and $n\geq 1$. Let $F(n,\alpha)$ be the largest $k$ such that there exists some 2-colouring of the edges of $K_n$ in which any induced subgraph $H$ on at least $k$ vertices contains more than $\alpha\binom{\lvert H\rvert}{2}$ many edges of each colour. Prove that for every fixed $0\leq \alpha \leq 1/2$, as $n\to\infty$,\[F(n,\alpha)\sim c_\alpha \log n\]for some constant $c_\alpha$.
- 题意摘要：输入按字面定义 F(n,α) 为满足性质的最大 k；但预期问题应是最小阈值 k：存在 K_n 的二染色，使每个至少 k 点的诱导子图中，两色边数都严格超过 αbinom(|H|,2)，并问 F(n,α)/log n 是否收敛。
- 状态核对：原文量词自相矛盾：对固定 α<1/2，取 k=n 并把全图近乎均分即得字面上的 F=n；α=1/2 时两色又不可能同时严格超过一半。因此所给“largest”版本及闭端点均不能成立。官方讨论区也明确提出 largest 应为 smallest。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：对修正后的最小阈值 f(n,α)，尝试用精确大偏差率定位常数：随机独立二染色，并把所有较大集合的条件归约到恰好 k 点；下界则使用任意染色中的单色团。
- 局部结论：平均引理：若某个 s≥k 的集合某色边数≤αbinom(s,2)，则某个 k-子集同色边数≤αbinom(k,2)。；令 I_α=D(α‖1/2)>0。随机染色中固定 k-集坏掉的概率至多 2exp(-I_α binom(k,2))，故并合界给 f(n,α)≤(2/I_α+o(1))log n。；由 R(r,r)≤4^r，任意二染色含 Ω(log n) 大小的单色团，所以对 α≥0（以严格条件解释 α=0）有 f(n,α)≥c log n。
- 第一阻塞点：并合界只给某个可行着色的常数，Ramsey 下界则给不同常数；没有近似次可加性或阈值定理保证最优值 f(n,α)/log n 有极限。随机着色的候选常数也未证明对最优确定性染色是下界。
- 下一步：检验乘积/替换着色能否给出近似次乘关系 n_{a+b}≥n_a n_b（其中 n_k 为存在所有 k-集平衡的最大阶数）；若误差为 o(k)，Fekete 型论证可能先建立指数增长率，从而推出所求极限常数。
- 来源核对：[官方条目 #162](https://www.erdosproblems.com/162)仍显示 largest，但同时声称 Θ(log n)，两者不相容。；[官方讨论区](https://www.erdosproblems.com/forum/thread/162)明确记录“largest 是否应为 smallest”的勘误意见。
- 时间记账：所在批次墙钟时间按题数均摊约 51.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/162)；既有候选答案（按不可信材料审计）

### #165

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Give an asymptotic formula for $R(3,k)$.
- 题意摘要：当 k→∞，确定 R(3,k) 的渐近常数；等价地，确定使每个 N 点无三角形图都含 k 点独立集的临界 N。
- 状态核对：截至官方条目 2026-03-07，最佳界为 (1/2+o(1))k²/log k≤R(3,k)≤(1+o(1))k²/log k，问题仍 open；候选所述最新常数 1/2 已由原论文核对。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把目标常数转成无三角形图独立数问题。设 G 为 N 点无三角形图、平均度 d、最大度 Δ。邻域均为独立集，所以 α(G)≥Δ；另一方面应用 Shearer 型估计 α(G)≳N log d/d，并尝试在 d 上优化。
- 局部结论：由每个 N(v) 独立，严格有 α(G)≥Δ≥d。；与 Shearer 下界合并得 α(G)≳max{d,N log d/d}；两项平衡在 d²≈N log d，产生 α(G)≳(1/√2+o(1))√(N log N)。；反演该独立数界正好对应 R(3,k)≤(1+o(1))k²/log k；而 HHKP 构造 α(G)≤(1+o(1))√(N log N)，对应下界常数 1/2。
- 第一阻塞点：要证明猜测常数 1/2，需把所有无三角形图的独立数下界从 (1/√2)√(Nlog N) 提升到 (1-o(1))√(Nlog N)。单独优化“一个大邻域”与平均度 Shearer 界在 1/√2 处卡死，没有利用不同邻域之间的全局相互作用。
- 下一步：尝试二层邻域分解：按度数截断，比较高阶点邻域并集与低阶诱导子图的 Shearer 下界；先证明或反驳带代码数修正项的形式 α(G)≥Nlog d/d+c·Σ_v(d(v)-d)_+²/(Nd²)。
- 来源核对：[官方条目 #165](https://www.erdosproblems.com/165)确认当前 1/2 与 1 两个常数界。；[Hefty–Horn–King–Pfender 原论文](https://arxiv.org/abs/2510.19718)定理给出 R(3,k)≥(1/2+o(1))k²/log k，并构造独立数约 √(Nlog N) 的无三角形图。
- 时间记账：所在批次墙钟时间按题数均摊约 51.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/165)；既有候选答案（按不可信材料审计）

### #168

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(N)$ be the size of the largest subset of $\{1,\ldots,N\}$ which does not contain any set of the form $\{n,2n,3n\}$. What is\[ \lim_{N\to \infty}\frac{F(N)}{N}?\]Is this limit irrational?
- 题意摘要：对每个 N，F(N) 是 [N] 中不含完整三元组 {n,2n,3n} 的子集的最大基数。问题先求实数极限 L=lim_{N→∞}F(N)/N，再问 L∉Q 是否成立。极限存在和值的级数公式已知；开放部分是无理性。
- 状态核对：冻结状态 open 合理：存在性已经解决，但无理性仍未解决。旧候选给出的十进制 0.800965755006558989…与 Eberhard 修正程序错误后的数值一致，但数值计算不证明无理性。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：按整数的 2、3-free 核分块。每个 n 唯一写成 n=m2^a3^b，其中 gcd(m,6)=1；{n,2n,3n} 不跨越不同的 m。令 d_1<d_2<…为 3-smooth 数，f(k) 为 {d_1,…,d_k} 上的极值，Δ_k=f(k)-f(k-1)，K={k:Δ_k=1}。逐块计数并展开 f(k)=Σ_{j≤k}Δ_j。
- 局部结论：加入一个点至多使独立集最大值增加 1，故 Δ_k∈{0,1}。若 C(x)=#{m≤x:gcd(m,6)=1}，则严格有 F(N)=Σ_{j∈K}C(N/d_j)。；C(x)=x/3+O(1)，且 Σ_j1/d_j=Σ_{a,b≥0}2^{-a}3^{-b}=3。截断后令 N→∞，再用该绝对收敛级数控制尾项，得到 L=(1/3)Σ_{j∈K}1/d_j。；这也给出有效误差控制：有限截断部分使用 C(x) 的 O(1) 误差，尾部至多由 Σ_{j>J}1/d_j 控制，因此 L 可计算到任意指定精度。
- 第一阻塞点：无理性处首次断裂：K 由一族有限极值问题定义，目前没有足够的结构描述。仅知它是 3-smooth 指数格上的某个 0-1 集，不能推出 Σ_{k∈K}1/d_k 无理；一般的 3-smooth 子级数完全可能是有理数。十进制非周期的有限观察也无效。
- 下一步：计算并用整数规划证书核验更大范围的 Δ_k，然后检验 K 在指数格 (a,b) 上是否满足有限自动机、最终周期或可证明的非周期性质；任何无理性方案首先必须给出可验证的 K-结构定理。
- 来源核对：本地 [168.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/168.lean) 的 F 与 NonTernary 定义和上述量词一致。；[Erdős Problems 讨论页](https://www.erdosproblems.com/forum/thread/168)记录了相同分块方法及修正后的十进制值；它没有给出无理性证明。
- 时间记账：所在批次墙钟时间按题数均摊约 77.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/168)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/168.lean`；既有候选答案（按不可信材料审计）

### #169

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $f(k)$ be the supremum of $\sum_{n\in A}\frac{1}{n}$ as $A$ ranges over all sets of positive integers which do not contain a $k$-term arithmetic progression. Estimate $f(k)$. Is\[\lim_{k\to \infty}\frac{f(k)}{\log W(k)}=\infty\]where $W(k)$ is the van der Waerden number?
- 题意摘要：固定整数 k≥3；A 遍历所有不含非平凡 k 项等差数列 a,a+d,…,a+(k-1)d（d>0）的正整数集，允许无限集。f(k) 是其倒数和的上确界，可能取 +∞。问题要求估计 f(k)，并问扩展实数意义下 f(k)/log W(k) 是否趋于 +∞，其中 W(k)=W(2,k)。
- 状态核对：冻结状态 open 与后续页面一致。旧候选关于 f(3)<∞ 的说法可以由 Bloom–Sisask 界严格推出；“所有 k 的有限性”等价于 Erdős 倒数和等差数列猜想，但不能据此断言某个 k≥4 有限。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先重建与 W(k) 的加权二染色下界，再考察能否通过每个临界染色的调和权重不平衡，把常数 1/2 提高。另用二进区间分解核验 f(3)<∞。
- 局部结论：由 W(k) 的极小性，[W(k)-1] 存在无单色 k-AP 的二染色 R∪B。两色均为 k-AP-free，故 f(k)≥max(Σ_{n∈R}1/n,Σ_{n∈B}1/n)≥H_{W(k)-1}/2≥(1/2)log W(k)。；若 A 无 3-AP，Bloom–Sisask 给出 |A∩[2^j,2^{j+1})|≪2^j/j^{1+c}。该块的倒数和≪j^{-1-c}，求和收敛，故每个此类 A 的倒数和一致有界，即 f(3)<∞。；f(k) 随 k 单调不减。若某个 k_0 有 f(k_0)=∞，则所有 k≥k_0 也为 ∞，极限问题在扩展实数意义下立即为真；真正困难的情形正是所有 f(k) 都有限。
- 第一阻塞点：加权临界染色路线在第一项强化即停止。设两色调和权重差为 D；现有平均论证只给 max=(H+|D|)/2，没有理由保证所有无单色 k-AP 的临界染色都满足 |D|≥δ log W(k)。甚至把 1/2 改成任意固定更大常数仍属开放。
- 下一步：对已知的小 k 建立精确 0-1 整数规划：在 [W(k)-1] 的所有无单色 k-AP 染色中最小化调和权重差 |Σ_R1/n-Σ_B1/n|。若最优值快速趋近 0，这条“权重不平衡”路线应淘汰；若出现刚性结构，再尝试证明递归下界。
- 来源核对：[Bloom–Sisask](https://arxiv.org/abs/2007.03528)明确给出 r_3(N)≪N/(log N)^{1+c}，足以支持上述二进求和。；[Erdős Problems #169](https://www.erdosproblems.com/169)列出 Gerver 的 (1-o(1))k log k 下界、1/2 障碍、有限性等价和 Walker 的 Kempner 归约；页面至 2026-04 仍标为 open。
- 时间记账：所在批次墙钟时间按题数均摊约 77.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/169)；既有候选答案（按不可信材料审计）

### #172

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that in any finite colouring of $\mathbb{N}$ there exist arbitrarily large finite $A$ such that all sums and products of distinct elements in $A$ are the same colour?
- 题意摘要：量词为：对每个有限颜色数 r、每个染色 χ:N→[r] 和每个 m，是否存在有限 A⊂N、|A|≥m，以及同一个颜色 c，使每个非空 S⊂A 都满足 χ(Σ_{x∈S}x)=χ(∏_{x∈S}x)=c。S 为单点时说明 A 的每个元素本身也必须是颜色 c。
- 状态核对：冻结状态 open。旧候选把题意解释为所有非空子集是正确的；它所述“二染色且 |A|=2”已由 Bowen 证明，但这远未覆盖任意有限染色和任意 m。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试分别调用加法与乘法半群上的 Hindman 型结论，再寻找共同生成元：先取得一个序列，其所有有限和同色；另一个序列的所有有限积同色；目标是通过颜色细化或块选择使两种结构落在同一组生成元上。
- 局部结论：m=1 平凡成立；r=1 时任意大小 A 都成立。；只要求有限子集和时由 Hindman 定理成立；只要求有限子集积时对半群 (N,×) 应用同一半群形式也成立。由此可见障碍不是两侧分别的 Ramsey 性，而是同步性。；Bowen 已证明任意二染色存在无穷多个单色 {x,y,x+y,xy}，所以 r=2、m=2 成立。Moreira 的 {x,x+y,xy} 结果不包含必须同色的 y，不能单独证明该特例。
- 第一阻塞点：首次不能闭合之处是“交叉细化”：加法 IP 集中的进一步乘法齐次子集不一定仍由同一批生成元保持全部有限和；乘法方向同样如此。普通 Hindman 定理没有提供同时兼容两个不同半群运算的幂等结构。
- 下一步：聚焦最小未覆盖情形 r=3、m=2，尝试把 Bowen 的 balanced-colouring 引理推广到三色；明确写出一个可检验的颜色聚焦引理，若成立应推出 {x,y,x+y,xy} 同色，若有限模型给出反例则淘汰该推广。
- 来源核对：本地 [172.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/172.lean)确实量化所有非空 S，并要求和、积共享同一 c。；[Alweiss](https://arxiv.org/abs/2307.08901)证明的是 Q 上任意有限规模的完整非空子集和、积模式。；[Bowen](https://arxiv.org/abs/2205.12921)明确证明 N 的任意二染色中有无穷多个 {x,y,xy,x+y} 单色。
- 时间记账：所在批次墙钟时间按题数均摊约 77.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/172)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/172.lean`；既有候选答案（按不可信材料审计）

### #173

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：In any $2$-colouring of $\mathbb{R}^2$, for all but at most one triangle $T$, there is a monochromatic congruent copy of $T$.
- 题意摘要：对每个二染色 χ:R²→{0,1}，考察非退化三角形的全等类型 T；要求至多存在一个全等类型 T，使平面中没有 χ-单色的全等副本。例外按边长三元组理解，而不是某个固定位置的三点集。
- 状态核对：冻结状态 open。旧候选所称“问题等价于只研究等边三角形”的两个强等价没有在所核对的一手论文中出现，故本次不采用。该论文只证明了带拓扑或多边形边界正则性的染色结果。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：反证地固定两个不全等三角形 T_1,T_2，构造超图 H：顶点为 R²，超边为 T_1 或 T_2 的全等副本。题目等价于证明 H 不可二染。利用紧致性，把每一对固定三角形进一步归约为寻找有限的不可二染子超图证书。
- 局部结论：若 H 的每个有限子超图均可二染，则由乘积空间 {0,1}^{R²} 的紧致性存在全局二染，避开两类单色三角形；反之有限不可二染证书显然排除全局染色。因此对固定 T_1,T_2，存在性问题严格等价于一个有限证书问题。；Shader 的定理排除了所有直角三角形成为例外，所以任何潜在例外必为非直角三角形。；令 h=√3s/2，把平面按高度 h 的半开平行条带交替染色。边长 s 的等边三角形在竖直方向的跨度至少 h、又小于 2h；同色条带指标必须同奇偶，故三点若同色只能处于同一条带，但跨度至少 h 排除这一点。因此确有染色避开一个指定等边类型，“至多一个”不能删去。
- 第一阻塞点：紧致性只保证：若某一对 T_1,T_2 不可同时避开，则存在有限证书；它不给证书的大小或构造。第一处缺口是无法对任意两组边长统一构造有限点集，使其中 T_1/T_2-超边不可二染。连续的边长参数也阻止从有限个数值实验直接推出全称结论。
- 下一步：先固定可代数化的一参数族，例如两个等边三角形且边长比 q∈Q。枚举小型三角格点配置并用 SAT 检验二可染性；若找到不可二染核，再提取对 q 的符号化坐标证明及最小证书。
- 来源核对：[Jelínek–Kynčl–Stolař–Valla](https://arxiv.org/abs/math/0701940)证明闭/开分割及多边形边界染色下的结果，并讨论避免指定等边三角形的染色；其摘要不支持旧候选声称的普遍等价归约。；条带宽等于等边三角形高度的标准反例亦由该论文相关介绍明确记载。
- 时间记账：所在批次墙钟时间按题数均摊约 77.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/173)；既有候选答案（按不可信材料审计）

### #174

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：A finite set $A\subset \mathbb{R}^n$ is called Ramsey if, for any $k\geq 1$, there exists some $d=d(A,k)$ such that in any $k$-colouring of $\mathbb{R}^d$ there exists a monochromatic copy of $A$. Characterise the Ramsey sets in $\mathbb{R}^n$.
- 题意摘要：固定有限 A⊂R^n。A 为 Ramsey 指：对每个整数 k≥1，存在维数 d=d(A,k)，使每个染色 χ:R^d→[k] 都含有一个与 A 全等的单色副本；允许把 A 等距嵌入更高维。要求刻画所有这样的 A。
- 状态核对：冻结状态 open。已知必要条件是 A 共球面；“所有球面集均 Ramsey”和“恰为可嵌入有限传递集的 subtransitive 集”是彼此不同的竞争猜想。旧候选若被理解为所有传递集或 subtransitive 集已知 Ramsey，则过强；LRW 将该方向也列为猜想。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：重建“Ramsey⇒球面”的代数证明。设 A={a_i}。共球面等价于存在 c,β 使 ||a_i||²=2c·a_i+β。若不共球面，由线性代数可取 λ_i，使 Σλ_i=0、Σλ_i a_i=0，但 δ=Σλ_i||a_i||²≠0；再用 EGMRSS 的有限染色引理染色平方范数。
- 局部结论：上述线性方程给出严格的共球面判据；不共球面时的 λ 是一个有限、可核验的反证证书。；任意高维全等副本 x_i=Ua_i+t 都满足 Σλ_i||x_i||²=δ，因为平移项和交叉项分别由 Σλ_i=0 与 Σλ_i a_i=0 消失。；EGMRSS 染色引理给出 R 的有限染色，使仿射方程 Σλ_i y_i=δ 没有单色解。用 y=||x||² 拉回到 R^d，即在每个 d 中避免 A 的单色副本，从而严格推出非球面 A 不是 Ramsey。
- 第一阻塞点：必要性证明到此闭合，但反向首次断裂：球面方程只给出距离几何约束，不产生任何有限 Ramsey 见证或传递群作用。一般球面集也未必能嵌入有限传递集，因此不能从已知的矩形、单纯形或可解传递群情形直接推广。
- 下一步：取 LRW 给出的显式“球面但非 subtransitive”循环四边形，核验其精确代数参数，并尝试把它嵌入现有已知 Ramsey 类。证明它 Ramsey 或非 Ramsey 将直接区分两套候选刻画，是当前路线最具体的判别任务。
- 来源核对：[EGMRSS 文献记录](https://www.maths.tcd.ie/EMIS/classics/Erdos/cit/27605001.htm)明确列出所需的实数有限染色引理及“Ramsey 蕴含球面”定理路线。；[Leader–Russell–Walters](https://www.dpmms.cam.ac.uk/~par31/preprints/ert.pdf)把“Ramsey 当且仅当 subtransitive”列为 Conjecture A，并说明证明所有传递集 Ramsey 本身仍需新的组合命题。；[LRW 摘要](https://arxiv.org/abs/1012.1350)确认存在球面但不能嵌入任何有限传递集的例子，因此两种猜想确实不同。
- 时间记账：所在批次墙钟时间按题数均摊约 77.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/174)；既有候选答案（按不可信材料审计）

### #176

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $N(k,\ell)$ be the minimal $N$ such that for any $f:\{1,\ldots,N\}\to\{-1,1\}$ there must exist a $k$-term arithmetic progression $P$ such that\[ \left\lvert \sum_{n\in P}f(n)\right\rvert\geq \ell.\]Find good upper bounds for $N(k,\ell)$. Is it true that for any $c>0$ there exists some $C>1$ such that\[N(k,ck)\leq C^k?\]What about\[N(k,2)\leq C^k\]or\[N(k,\sqrt{k})\leq C^k?\]
- 题意摘要：对整数 k≥1、实数阈值 ℓ，N(k,ℓ) 是最小 N，使每个二染色 f:[N]→{−1,1} 都有一个完全落在 [N] 内的 k 项等差数列 P 满足 |∑_{n∈P}f(n)|≥ℓ。所问指数上界应理解为固定 0<c≤1 时 C 可依赖 c；若照字面取 c>1，则 N(k,ck)=∞。
- 状态核对：冻结记录及当前官方页仍标为 open。候选稿的偶数 k 结论正确，但不能据此处理奇数 k；其具体五层塔界未在本次筛查中核实，故不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：按奇偶拆分，并对“所有 k 项和均小于 2”的奇数情形写出滑动窗口约束。令 k=2^tm、m 奇。由 Spencer 公式及偶数个 ±1 之和的奇偶性，偶数 k 时 N(k,2)=N(k,1)。奇数 k 时，若尚未出现目标进展，则每个 k-AP 的和只能是 ±1；沿固定公差 d 比较相邻窗口 S_a=∑_{j=0}^{k−1}f(a+jd)。
- 局部结论：若 ℓ>k，则任何 P 都有 |∑_P f|≤k，故 N(k,ℓ)=∞；这修正了“任意 c>0”的字面量词。；若 k 为偶数，则 N(k,2)=N(k,1)=2^{v_2(k)}(k−1)+1≤k(k−1)+1，因此该子序列远强于 C^k。；若 k 为奇数且所有 k-AP 均未达到阈值 2，则 S_a∈{−1,1}，且 S_{a+d}−S_a=f(a+kd)−f(a)。若 S_{a+d}=−S_a，则必有 f(a)=S_a、f(a+kd)=−S_a；若两和相同，则两端颜色相同。
- 第一阻塞点：这些一维滑动约束尚不能在不同公差 d 之间闭合：没有推出有限区间内必然矛盾，也没有得到奇数 k 的指数长度上界。这正是候选稿用偶数奇偶性无法跨越的第一处。
- 下一步：把上述约束对奇数 k=5,7 及公差 1≤d≤k 编成有限 SAT 实例，计算最大可行 N，并检验“长解必出现短周期/仿射结构”这一可证伪的结构猜想；若猜想存活，再尝试证明周期长度 O(k²)。
- 来源核对：[官方问题页](https://www.erdosproblems.com/176)仍列 open，并记录 Spencer 公式、Erdős 指数下界及未解决的三个上界问题。；2026 年页面出现未纳入正式 remarks 的 AI/Lean 评论；它们不是同行核验的状态更新，本筛查未将其当作解决。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/176)；既有候选答案（按不可信材料审计）

### #177

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find the smallest $h(d)$ such that the following holds. There exists a function $f:\mathbb{N}\to\{-1,1\}$ such that, for every $d\geq 1$,\[\max_{P_d}\left\lvert \sum_{n\in P_d}f(n)\right\rvert\leq h(d),\]where $P_d$ ranges over all finite arithmetic progressions with common difference $d$.
- 题意摘要：须找一个单一函数 f:ℕ→{−1,1}，同时对每个 d≥1 控制 D_f(d)=sup_{a,m≥1}|∑_{j=0}^{m−1}f(a+jd)|≤h(d)。量词次序是 ∃f ∀d ∀a,m；不能对每个 d 分别选择 f。所谓“最小 h”实质是研究所有可同时实现的包络函数的最优渐近阶，未必存在逐点最小元。
- 状态核对：仍为 open。已核对 Beck 的结论：对每个 ε>0，存在同一个 f，使充分大 d 均有 D_f(d)≤d^{8+ε}。官方记录 Roth 型下界 h(d)≫√d。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试从周期平衡构造开始：周期序列容易控制 d=1 的区间和，因此先判断能否逐级选择周期并取极限。该路线立即暴露一个严格障碍。
- 局部结论：D_f(1)<∞ 等价于前缀和 F(n)=∑_{j≤n}f(j) 有界；此时任意连续区间和为两个前缀和之差。特别地 D_f(1)≥1，而交替染色单独实现 D_f(1)=1。；若 f 具有周期 q，则取 d=q 后 f(a+jq)=f(a)，故长度 m 的和为 mf(a)，从而 D_f(q)=∞。因此任何真正可行的统一染色都必为非周期。；更一般地，任何最终周期染色也在某个周期倍数 d 上产生无界差异；所以有限周期逼近只有在极限中不断破坏旧周期才可能成功。
- 第一阻塞点：逐级修改周期块时，修正新公差会重新改变旧公差的任意长级数；目前没有得到一种使每个坐标 d 的累计改变量可求和的稳定化估计。这是从初等周期构造通向 Beck 型无限维向量平衡的第一处缺口。
- 下一步：构造并验证一个有限版本：给定 D,L，寻找最小 B(D,L)，使 [L] 可二染色且所有 d≤D、所有落在 [L] 内的 d-AP 差异≤B；先用线性规划/整数规划检验 B(D,L) 是否在 L→∞ 时稳定，并测试分块拼接所需的边界修正量。
- 来源核对：[官方问题页](https://www.erdosproblems.com/177)列出 d^{1/2} 与 d^{8+ε} 之间的已知范围。；[Beck 论文资料页](https://scholarship.libraries.rutgers.edu/esploro/outputs/bookChapter/A-Discrepancy-Problem-Balancing-Infinite-Dimensional/991031665483404646)明确给出同一个染色同时控制所有充分大 d 的量词。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/177)；既有候选答案（按不可信材料审计）

### #180

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $\mathcal{F}$ is a finite set of finite graphs then $\mathrm{ex}(n;\mathcal{F})$ is the maximum number of edges a graph on $n$ vertices can have without containing any subgraphs from $\mathcal{F}$. Note that it is trivial that $\mathrm{ex}(n;\mathcal{F})\leq \mathrm{ex}(n;G)$ for every $G\in\mathcal{F}$. Is it true that, for every $\mathcal{F}$, there exists $G\in\mathcal{F}$ such that\[\mathrm{ex}(n;G)\ll_{\mathcal{F}}\mathrm{ex}(n;\mathcal{F})?\]
- 题意摘要：对每个有限图族 𝓕，问题断言存在某个固定 G∈𝓕 和仅依赖 𝓕 的常数 C，使对所有充分大 n，ex(n;G)≤C·ex(n;𝓕)。子图不是诱导子图。
- 状态核对：按输入仍标 open，但精确的全称命题已有官方页注明的 folklore counterexample。吸收人工评审意见：下面只是重建并核对该已知反例，不能宣称为新的问题解决；可能仍开放的是排除此星—匹配障碍后的修正版。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：取 𝓕={K_{1,2},2K_2}。直接分类任意两条边是相交还是不相交，并分别计算单个禁图的极值数。
- 局部结论：任何含至少两条边的图，要么两边相交而含 K_{1,2}，要么两边不交而含 2K_2。因此 n≥2 时 ex(n;𝓕)=1。；K_{1,2}-free 图的最大度至多 1，故 ex(n;K_{1,2})=⌊n/2⌋。；2K_2-free 图可取含 n−1 条边的星；反过来两两相交的简单图族是星或至多三角形，故 n≥4 时 ex(n;2K_2)=n−1。于是两个单禁图的极值数均为 Θ(n)，不可能被常数倍的 ex(n;𝓕)=1 控制。
- 第一阻塞点：原命题已被完整反驳，没有证明缺口。剩余未闭合的是另一个、经过修改的问题：若排除同时含非平凡星和非平凡匹配的图族，结论是否成立。
- 下一步：将修正版准确形式化，并先证明可检验的森林子类：分类哪些有限森林族能使 ex(n;𝓕)=O(1)，确认星—匹配对是否为唯一机制。
- 来源核对：[官方问题页](https://www.erdosproblems.com/180)明确把星与匹配组成的有限族称为 folklore counterexample，同时仍将排除该障碍后的版本视为可能开放。；人工评审指出反例已在网站记录；本结论相应标为已知反例而非 prior candidate 的原创解决。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/180)；既有候选答案（按不可信材料审计）

### #181

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $Q_n$ be the $n$-dimensional hypercube graph (so that $Q_n$ has $2^n$ vertices and $n2^{n-1}$ edges). Prove that\[R(Q_n) \ll 2^n.\]
- 题意摘要：R(Q_n) 是最小 N，使 K_N 的每个红蓝边染色都含一个单色的 n 维立方体图 Q_n；目标是存在绝对常数 C，使所有 n 均有 R(Q_n)≤C2^n。
- 状态核对：仍为 open。Tikhomirov 的已核对结果为 R(Q_n)=O(2^{(2−c)n})，可取约 c=0.03656，尚远于线性顶点数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：复核候选稿的依赖随机选择路线。多数颜色图密度至少 1/2；取 n 个随机顶点的公共邻域 S，并删去公共邻域小于 m=2^n 的坏 n-元组，再随机嵌入 Q_n 一个二分部，最后贪心嵌入另一部。
- 局部结论：取 N=64m² 时，Jensen 给出 E|S|≥32m；坏有序 n-元组的期望数至多 m^n。由加权平均可选到 |S|≥m 且坏元组数 X≤2^{-4n}|S|^n。；候选稿把“无放回的互异元组”坏概率误写成 X/|S|^n。正确上界是 X/(|S|)_n≤2^{-4n}|S|^n/(|S|)_n；因 |S|≥2^n 且 n≤2^{n−1}，粗略比值至多 2^n，联合界仍小于 1。因此该漏洞可修补，确实得到 R(Q_n)≤64·4^n。；嵌入第一二分部后，每个另一部顶点有至少 m 个候选公共邻点，而总共只嵌入 m 个顶点，故贪心注入严格成立。
- 第一阻塞点：若把 N 降到 C2^n，朴素 DRC 中 E|S|约为 N·2^{-n}=C，不足以容纳大小 2^{n−1} 的立方体二分部；这里第一次发生指数级损失。仅调整常数或修补候选稿的采样分母不能达到目标。
- 下一步：在有限 n 上检验 Tikhomirov 的三分结构：对密度 1/2 的二分图分别测量坏公共邻域的重叠、增密子图和块结构，尝试证明一个简化二分命题，至少把 DRC 的 4^n 常数指数严格降低。
- 来源核对：[官方问题页](https://www.erdosproblems.com/181)仍列 open，并记录当前上界。；[Tikhomirov 原论文](https://arxiv.org/abs/2208.14568)给出 O(2^{2n-cn})；论文证明明确结合 DRC、增密和块结构三种情形。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/181)；既有候选答案（按不可信材料审计）

### #183

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(3;k)$ be the minimal $n$ such that if the edges of $K_n$ are coloured with $k$ colours then there must exist a monochromatic triangle. Determine\[\lim_{k\to \infty}R(3;k)^{1/k}.\]
- 题意摘要：R(3;k) 是最小 n，使 K_n 的任意 k 边染色含单色三角形。要求确定 k→∞ 时 R(3;k)^{1/k} 的极限，包括先证明它是有限实数；颜色数 k 是趋于无穷的参数。
- 状态核对：仍为 open，甚至极限是否有限也未知。候选稿关于极限存在的主结论可修复，但其积构造论证漏掉了“三个顶点位于三个不同纤维”的情形。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：令 a_k=R(3;k)−1，使用字典积染色证明超乘性，再检查标准顶点邻域递推能否给出指数上界。积构造在不同第一坐标间用 k 色底层染色，同一纤维内用另一组 ℓ 色。
- 局部结论：完整检查三角形：全在一纤维由 ℓ 色染色排除；恰在两纤维时同时出现两组颜色；在三个不同纤维时三条边投影到底层无单色三角形。故 a_{k+ℓ}≥a_ka_ℓ。；由 Fekete 引理，lim a_k^{1/k}=sup a_k^{1/k}∈[2,∞] 存在；又 a_k≥2^k，故把 a_k 换成 R(3;k)=a_k+1 不改变根极限。；在无单色三角形的 K_N 中固定顶点 v，按 v 到其他点的颜色分成 k 个邻域；第 i 个邻域内部不能使用颜色 i，故大小至多 R(3;k−1)−1，得到 R(3;k)≤2+k(R(3;k−1)−1)，进而仅有阶乘上界。
- 第一阻塞点：要证明根极限有限，必须把递推中随 k 增长的乘子 k 压成绝对常数或获得等价的指数上界；单顶点邻域分割没有提供各颜色邻域之间的额外兼容性。这是该路线第一处不能闭合之处。
- 下一步：研究双顶点而非单顶点的颜色邻域矩阵：对每对颜色 (i,j) 计数 N_i(u)∩N_j(v)，尝试证明一个可计算的不等式 R(3;k)≤C^tR(3;k−t)+O(1)，先对固定 t=2 用已知小 k Ramsey 数据检验常数 C 是否可能独立于 k。
- 来源核对：[官方问题页](https://www.erdosproblems.com/183)仍列 open，记录最好下界 380^{k/5}−O(1) 及阶乘型上界。；官方页当前给出的较精确上界为 (e−1/6)k!+1；它仍不能证明根极限有限。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/183)；既有候选答案（按不可信材料审计）

### #184

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Any graph on $n$ vertices can be decomposed into $O(n)$ many edge-disjoint cycles and edges.
- 题意摘要：存在绝对常数 C，使每个 n 顶点有限简单图 G 的边集都能被分割为至多 Cn 个部分；每部分或者是一条单边，或者是一个简单环。不同部分必须边不交，且覆盖 E(G)。
- 状态核对：截至 2026-07 仍开放。已知一般上界为 O(n log* n)，不能把候选答案中的 O(n log n) 论证冒充线性证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：采用“反复删除长环”路线。当前剩余图有 m≥2n 条边时，取一个最小度至少 m/n 的非空子图；最长路端点论证给出长度至少 m/n+1 的环。删去该环后 m 至少按比例 1-1/n 下降，直至只剩 O(n) 条边。另用 K_{3,n-3} 核查线性下界。
- 局部结论：迭代满足 m_t≤m_0(1-1/n)^t≤m_0e^{-t/n}；因 m_0<n²，O(n log n) 次删环后仅余 O(n) 条边，得到严格的 O(n log n) 分解。；对 K_{3,n-3}，大侧每个顶点度数为 3；环在每个顶点贡献偶数度，故至少 n-3 条边必须作为单边部分。；该图中每个环至多使用小侧三个顶点，故长度至多 6；余下至多可由环覆盖的 2(n-3) 条边至少需 (n-3)/3 个环，总部分数至少 4(n-3)/3。
- 第一阻塞点：第一处断点是把乘法衰减过程的 Θ(log n) 个密度尺度压缩成常数个尺度；长环引理只保证长度约 m/n，因此按此势函数求和天然产生 n log n，无法推出 O(n)。
- 下一步：检验能否对某个固定稀疏尺度建立批量打包引理：当 m∈[2^jn,2^{j+1}n] 时，是否能用 O(n/2^j) 个边不交环一次覆盖该尺度中除 O(n) 外的全部边；失败时记录产生的稀疏割结构。
- 来源核对：官方状态页：https://www.erdosproblems.com/184；Bucić–Montgomery：https://arxiv.org/abs/2211.07689；本地 Lean 陈述确认量词为统一的 f=O(n)，且分解是边集的严格分割。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/184)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/184.lean`；既有候选答案（按不可信材料审计）

### #187

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find the best function $f(d)$ such that, in any 2-colouring of the integers, at least one colour class contains an arithmetic progression with common difference $d$ of length $f(d)$ for infinitely many $d$.
- 题意摘要：求尽可能大的函数 f:N→N，使对每个二染色 χ:Z→{红,蓝}，存在一个固定颜色 c，并有无穷多个不同的正整数 d，使某个首项 a 满足 χ(a)=χ(a+d)=…=χ(a+(f(d)-1)d)=c。两种颜色若随 d 变化，由无限抽屉原理仍可固定一种。
- 状态核对：截至 2026-07 仍开放。Beck 给出存在某个染色使可用长度至多 (1+o(1))log₂d。候选答案所说“没有任何有效下界”过强：van der Waerden 数至少给出一个可明确定义但极慢的无界阶梯函数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令 W_k=W(2,k)。递归选整数 L_{k+1}>L_kW_k，并定义 f(d)=k 当 L_k≤d<L_{k+1}。对任意二染色，把它限制到缩放集合 {0,L_k,…,(W_k-1)L_k}，再应用 van der Waerden 定理。
- 局部结论：得到指标公差 r≥1 的单色 k-AP，因此原整数中的公差 d_k=rL_k。；由 r(k-1)≤W_k-1，得 L_k≤d_k<L_kW_k<L_{k+1}，所以 f(d_k)=k，所获进展长度确实达到要求。；不同 k 对应不交区间，故 d_k 两两不同；再由两色抽屉原理，同一颜色承担其中无穷多个。因此上述 f(d)→∞ 严格成立。
- 第一阻塞点：该构造的 L_{k+1} 必须超过 L_kW(2,k)，只给出极稀疏阶梯；它无法产生诸如 log log d 的常规下界，更无法接近 Beck 的 log₂d 上界。
- 下一步：把任务具体化为：寻找可替代完整 van der Waerden 数的“缩放块”定理，使 L_{k+1}/L_k 有可控上界；首先测试是否能用已知 W(2,k) 上界推出一个显式的迭代对数型 f。
- 来源核对：官方状态及 Beck 上界：https://www.erdosproblems.com/187；官方页明确表述 van der Waerden 定理迫使 f(d)→∞。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/187)；既有候选答案（按不可信材料审计）

### #188

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the smallest $k$ such that $\mathbb{R}^2$ can be red/blue coloured with no pair of red points unit distance apart, and no $k$-term arithmetic progression of blue points with distance $1$?
- 题意摘要：令 ℓ_k={x,x+u,…,x+(k-1)u}，其中 x,u∈R² 且 ||u||=1。求最小 k，使存在红蓝染色 R²=R∪B，红集没有单位距离点对，且 B 不含任何刚性运动方向上的 ℓ_k。
- 状态核对：仍开放，但可严格核得 6≤k≤10^10。下界来自 Tsaturian：任何无红单位点对的染色都有蓝色 ℓ_5。上界来自 Conlon–Fox 原论文的明确 m=10^{5n}，取 n=2。候选答案的数值结论可保留，但其来源应直接核对原论文；官方页只列无证明的历史性约 10^7。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：把红集视为平面单位距离图的独立集，同时它必须击中每个单位步长 ℓ_k。先研究有限单位距离配置所诱导的独立集—击中集不可满足性。
- 局部结论：在任一单位方向直线上，颜色词不能出现 RR；若还避开蓝 ℓ_k，也不能出现连续 k 个 B。；当 k=2 时每条单位边必须恰有一个红端点，即要求单位距离图二分；一个单位等边三角形即给出矛盾。；Tsaturian 的有限几何论证把这种不可满足性推进到 k=5，从而排除 k≤5；Conlon–Fox 的周期随机构造则证明某个 k≤10^10 可行。
- 第一阻塞点：独立重建下界时，第一处未闭合步骤是找出并逐项验证迫使蓝 ℓ_5 的有限单位距离配置；仅沿单条直线的禁词条件允许周期词 RBRB…，不足以产生矛盾，必须使用多个方向间的几何耦合。
- 下一步：从 Tsaturian 论文抽取有限点配置及其全部单位边、ℓ_5 超边，编码为 SAT：变量为点色，子句禁止红单位边并要求每个 ℓ_5 至少一红；先机器核验 UNSAT，再提取可人工检查的最小不可满足核心。
- 来源核对：官方状态页：https://www.erdosproblems.com/188；Tsaturian：https://arxiv.org/abs/1703.10723；Conlon–Fox 原论文：https://www.its.caltech.edu/~dconlon/euclideanramsey.pdf；本地 Lean 陈述把平面实现为 C，并量化所有范数为 1 的公差。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/188)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/188.lean`；既有候选答案（按不可信材料审计）

### #190

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $H(k)$ be the smallest $N$ such that in any finite colouring of $\{1,\ldots,N\}$ (into any number of colours) there is always either a monochromatic $k$-term arithmetic progression or a rainbow arithmetic progression (i.e. all elements are different colours). Estimate $H(k)$. Is it true that\[H(k)^{1/k}/k \to \infty\]as $k\to\infty$?
- 题意摘要：对每个 k，H(k) 是最小 N，使任意映射 χ:[N]→C（C 为任意有限颜色集，颜色数不预先固定）都含一个 k 项等差数列，其颜色或者全部相同，或者两两不同。问题包括估计 H(k)，尤其判定 H(k)^{1/k}/k 是否趋于无穷。
- 状态核对：极限问题已于 2026 年肯定解决；候选答案的“仍开放”结论已过时。精确增长率仍未解决。官方页记录 Bae 的 H(k)≥k^{(2-o(1))k}，以及 Fox–Hunter 更强的 H(k)≥k^{(1-o(1))k log k}。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 Bae 路线。采用 W(r,k) 表示 r 色 k 项 van der Waerden 数。用至多 k-1 色的反例可同时排除彩虹 k-AP，故 H(k)≥W(k-1,k)。取 r₀=floor(k/log k)，先以对 k-AP 超图应用对称 Lovász 局部引理，得到 W(r₀,k)≥r₀^{k-1}/(16k)；再用 BCT 递推把颜色数提升到接近 k 的素数 p*，Baker–Harman–Pintz 保证 k-1-p*=O(k^{0.525})。
- 局部结论：抽屉归约 H(k)≥W(k-1,k) 是严格的：只使用 k-1 种颜色时不可能出现彩虹 k-AP。；BCT 迭代与 Erdős–Lovász 初值合成后，主因子为 r₀·exp(-r₀log k/k)；在 r₀≈k/log k 处最大，值为 (1/e+o(1))k/log k。；因此 H(k)^{1/k}/k≥(1/e-o(1))k/log k→∞。这已经严格回答原来的极限问题；Fox–Hunter 后续下界更强。
- 第一阻塞点：对原问题的肯定部分没有开放断点；若要求本文内完全复证，第一项外部黑箱是 BCT 的受限递推，其参数范围必须逐条核对。对“估计 H(k)”的剩余断点则是缺乏接近上述下界的上界。
- 下一步：逐式核对 BCT 递推从 r₀ 到 p* 的指数，并与 Fox–Hunter 的更强构造比较；随后把未解决部分重新表述为寻找 H(k) 的有效上界，而不是再检验该极限。
- 来源核对：官方更新：https://www.erdosproblems.com/190；Bae 证明：https://arxiv.org/abs/2604.20588；官方页于 2026-06-02 记录 Fox–Hunter 下界及 solved 状态。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/190)；既有候选答案（按不可信材料审计）

### #193

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $S\subseteq \mathbb{Z}^3$ be a finite set and let $A=\{a_1,a_2,\ldots,\}\subset \mathbb{Z}^3$ be an infinite $S$-walk, so that $a_{i+1}-a_i\in S$ for all $i$. Must $A$ contain three collinear points?
- 题意摘要：对每个有限步集 S⊂Z³，以及每个序列 a:N→Z³，若 a_{i+1}-a_i∈S 且值域 {a_i:i∈N} 无限，是否必有三个互异值域点位于同一直线上？无限值域条件排除了常值或有限回路的退化反例。
- 状态核对：截至 2026-07 仍开放。Gerver–Ramsey/Lidbetter 的构造只把任一直线上的点数统一控制到 188，并未降到 2，故不是反例。候选答案的“|S|=3 时长度 9”未由本次核查来源确认，不纳入结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令步长 s_i=a_{i+1}-a_i。寻找相邻等长块具有相同非零位移：若 sum_{j=0}^{l-1}s_{i+j}=sum_{j=l}^{2l-1}s_{i+j}=v≠0，则 a_i,a_{i+l},a_{i+2l} 是三个互异且等距的共线点。尝试用有限字母表上的重复块原理强迫这种情形。
- 局部结论：无共线三点时，对所有 i,l，只要相邻两个 l-步块的位移相等，该公共位移就必须为 0。；特别地，两个相邻的相同非零步长立即产生 a_i,a_{i+1},a_{i+2} 的共线三点；故反例的步长词不能含非零平方 ss。；问题等价于：有限字母步长词的前缀和在 Z³ 中能否保持无限值域，同时避免所有关系 a_i+a_{i+2l}=2a_{i+l}，并进一步避免任意三个不同下标对应的仿射共线关系。
- 第一阻塞点：有限字母表并不强迫出现相邻重复块：三字母以上存在无限平方自由词；即使两个远隔块相同，也只给出相同位移，不能保证它们首尾相接。因此普通鸽巢或词重复论证在这里首次失效。
- 下一步：研究额外的三维阿贝尔化约束：对候选平方自由代换词计算所有相邻等长块的 Parikh 向量差，检验是否仍必出现相等且非零的块和；这是一项有限自动机/代换矩阵可检验任务。
- 来源核对：官方状态页：https://www.erdosproblems.com/193；Lidbetter：https://arxiv.org/abs/2303.14579；本地 Lean 陈述明确要求值域无限，并要求三个互异点在 Q 上共线。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/193)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/193.lean`；既有候选答案（按不可信材料审计）

### #195

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the largest $k$ such that in any permutation of $\mathbb{Z}$ there must exist a monotone $k$-term arithmetic progression $x_1<\cdots<x_k$?
- 题意摘要：令 K 为满足下述性质的最大自然数：对每个双向排列（双射）f:ℤ→ℤ，都存在指标 i₁<⋯<i_K，使 f(i₁),…,f(i_K) 是公差非零的等差数列，并按该顺序递增或递减。问题求 K。
- 状态核对：冻结状态及目前官方页面均标为 open。已知 3≤K≤4：DEGS 的三项不可避免结果给出下界；Adenwalla 构造了避免五项单调等差数列的 ℤ 排列，给出 K≤4。候选答案的结论范围正确，但应说明从正整数到 ℤ 排列的序型归约。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：取任意 f:ℤ≃ℤ，只保留正整数值，按其原指标排序。对应指标子集若下有界，诱导出 ω 型排列；若上有界，反向后为 ω 型；若双向无界，则为 ζ 型双向排列。DEGS 分别排除正整数的单向或双向三项避免排列，故 f 必含单调三项。随后尝试把同一归约推进到四项，但正整数的四项问题本身正是 #196。
- 局部结论：正整数值形成的指标集必属于 ω、ω*、ζ 三种序型之一；反转 ω* 不改变“存在单调等差子列”。；调用 DEGS 的单向及双向三项定理，可严格推出每个 ℤ 排列含单调三项，即 K≥3。；Adenwalla 的显式五项避免排列严格推出 K≤4，因此只剩 K=3 或 K=4。
- 第一阻塞点：第一处不能闭合的是证明每个 ℤ 排列含四项：正整数诱导子序列若为 ω 型，这一步立即包含尚未解决的 #196，现有三项定理不能提升长度。
- 下一步：检验“模 p 的四项避免次序＋分块提升”路线：对一个尚未覆盖的小素数 p 枚举循环四项避免排列，并逐条验证提升到 ℤ 分块排列时跨块四项是否仍被排除。
- 来源核对：本地 `195.lean` 确认对象为 f:ℤ≃ℤ，且使用 `HasMonotoneAP`。；Erdős Problems #195 仍列为 open，并记载 Geneson 的 K≤5 与 Adenwalla 的 K≤4：https://www.erdosproblems.com/195；Adenwalla, arXiv:2211.04451，定理给出 ℤ 的五项避免排列，并综述三项不可避免结果：https://arxiv.org/abs/2211.04451
- 时间记账：所在批次墙钟时间按题数均摊约 63.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/195)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/195.lean`；既有候选答案（按不可信材料审计）

### #196

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Must every permutation of $\mathbb{N}$ contain a monotone 4-term arithmetic progression? In other words, given a permutation $x$ of $\mathbb{N}$ must there be indices with either $i<j<k<l$ or $i>j>k>l$ such that $x_i,x_j,x_k,x_l$ are an arithmetic progression?
- 题意摘要：对每个单向排列 x:ℕ≃ℕ，是否必有四个严格递增指标 i<j<k<l，使 x_i,x_j,x_k,x_l 依次构成公差非零的等差数列？原陈述的 i>j>k>l 情形反转后等价于此，其中公差变号。
- 状态核对：仍为 open。DEGS 已证明三项必然出现，并构造了避免五项的排列；四项是缺口。候选答案的“反转指标”化简正确，其三项短证明也正确，但必须补上目标数为何一定出现在右侧。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：设首项为 m=x₁，令 b=x_j 是首个晚于 m 且数值大于 m 的项。由于 2b−m 与 3b−2m 都大于 m，按 j 的最小性，它们都只能出现在 b 之后。若 2b−m 先于 3b−2m 出现，则 m,b,2b−m,3b−2m 已是所求四项。
- 局部结论：首个大于 m 的项 b 必存在。目标 2b−m 在 b 以前既不可能位于首位，也不可能位于中间位置，故严格出现在 b 后；这给出强迫三项 m,b,2b−m。；同理 3b−2m 也出现在 b 后。；因此任何避免四项的排列都必须满足 pos(3b−2m)<pos(2b−m)，这是首项 m 与首个较大项 b 所强制的具体逆序条件。
- 第一阻塞点：最先失效之处是无法比较 2b−m 与 3b−2m 的出现位置；排列性及 b 的最小选择只说明二者都在 b 后，不能排除所需次序恰好被反转。
- 下一步：迭代研究射线 m+n(b−m)：把避免四项转写成这些点的位置排列不得含四个递增或递减连续参数，先检验能否从 n=0,1 的固定前缀与多个不同 b 的交叉射线导出有限矛盾。
- 来源核对：本地 `196.lean` 与 `HasMonotoneAP` 定义确认量词及指标方向。；Erdős Problems #196 仍列为 open：https://www.erdosproblems.com/196；DEGS 原论文书目信息及开放下载页：DOI 10.4064/aa-34-1-81-90。；Adenwalla 的综述明确记载正整数三项不可避免、五项可避免、四项仍开放：https://arxiv.org/abs/2211.04451
- 时间记账：所在批次墙钟时间按题数均摊约 63.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/196)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/196.lean`；既有候选答案（按不可信材料审计）

### #197

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Can $\mathbb{N}$ be partitioned into two sets, each of which can be permuted to avoid monotone 3-term arithmetic progressions?
- 题意摘要：问是否存在互补的两个无限集 A,B⊂ℕ，以及双射 f:ℕ→A、g:ℕ→B，使两个枚举都没有严格递增指标 i<j<k，其对应值依次为 a,a+d,a+2d 或反向序列。这里不是要求 A、B 本身无三项等差数列，而是要求各自存在避免单调三项的排序。
- 状态核对：仍为 open；允许三个集合时已有构造。候选答案把这种集合简称为“3-free”容易与通常的“集合本身不含三项 AP”混淆，必须限定为“可作三项避免排序”。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用密度障碍。令 α 为可作三项避免排序集合的最大上密度，β 为最大下密度。若 ℕ=A⊔B，则对每个 n 有 d_n(A)+d_n(B)=1，因而 limsup d_n(A)+liminf d_n(B)=1。若 A、B 均可排序，则前者≤α、后者≤β，故两分方案必要地满足 1≤α+β。
- 局部结论：任何可排序集合都不能包含一个完整仿射射线 a+qℕ：否则抽取该子序列并除以 q，会得到 ℕ 的三项避免排列，与 DEGS 矛盾。；两分方案严格蕴含密度必要条件 α+β≥1。；文献中的猜测 α=1/2、β=1/4 若成立，会立即否定两分方案；但这些等式目前没有证明。
- 第一阻塞点：密度路线首先卡在缺少足够强的上界。现有构造给的是 α、β 的下界，而 Adenwalla 明确指出甚至尚无把相关密度严格上界到 1 以下的一般技术，因此不能推出 α+β<1。
- 下一步：以“可排序集合不能含仿射射线”为起点，检验能否定量化：证明正上密度集合必含一个密度受控的仿射子结构，并验证该结构是否足以继承 DEGS 的三项强迫论证；若只能得到有限 AP，则记录该量化断点。
- 来源核对：本地 `197.lean` 明确要求 A、B 互补，且各有 ℕ 到该集合的双射。；Erdős Problems #197 仍列为 open，并说明三集合情形可行：https://www.erdosproblems.com/197；Adenwalla 论文第 6 个问题重述两分问题，并给出 α+β<1 的否定准则及当前密度障碍：https://arxiv.org/abs/2211.04451
- 时间记账：所在批次墙钟时间按题数均摊约 63.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/197)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/197.lean`；既有候选答案（按不可信材料审计）

### #200

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does the longest arithmetic progression of primes in $\{1,\ldots,N\}$ have length $o(\log N)$?
- 题意摘要：令 L(N) 为满足下述条件的最大 k：存在 d>0 与素数 a,a+d,…,a+(k−1)d≤N。问题是是否 L(N)/log N→0。
- 状态核对：仍为 open。已知素数定理给出 L(N)≤(1+o(1))log N。候选答案直接假定所有项都大于 k 并称其为“典型”并不足以证明该上界；该缺口可通过删除小素数项严格修复。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：设有 k 项素数 AP。删去所有不超过 k 的项；因数列递增，这些项构成前缀，数目 r≤π(k)。余下尾段长度 m=k−r≥k−π(k)，且每项都大于 k。对任意素数 q≤m，若 q∤d，则尾段最初 q 项模 q 遍历全部剩余类，故其中一项被 q 整除；但该项大于 k≥q，不可能是素数。因此每个 q≤m 都整除 d。
- 局部结论：严格得到 primorial m#=∏_{q≤m}q 整除 d。；由 (m−1)d≤N 得 θ(m)=log(m#)≤log N；素数定理 θ(m)∼m 给出 m≤(1+o(1))log N。；又 r≤π(k)=o(k)，故 m=(1−o(1))k，最终恢复 k≤(1+o(1))log N。
- 第一阻塞点：primorial 条件只给 log d≥(1−o(1))k；当 k≈c log N 时，这与 d≤N 完全相容。要得到小 o，必须证明除了局部同余可容许性外还有额外的全局稀疏性，现有论证没有这种输入。
- 下一步：固定 ε>0，对 k≥εlog N 且 m#|d 的候选对 (a,d) 建立统一筛上界；具体先计算 Selberg 筛能否使“全部 k 个线性式同时为素数”的候选总数趋于 0，并明确奇异级数随 k 增长造成的损失。
- 来源核对：Erdős Problems #200 仍列为 open，并明确记载 PNT 上界：https://www.erdosproblems.com/200；候选答案的 Green–Tao 下界背景与本题上界方向相容，但并不推进 o(log N)。；已独立检查局部模论证中的“小素数项例外”，并用删除至多 π(k) 项修复。
- 时间记账：所在批次墙钟时间按题数均摊约 63.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/200)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/200.lean`；既有候选答案（按不可信材料审计）

### #201

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G_k(N)$ be such that any set of $N$ integers contains a subset of size at least $G_k(N)$ which does not contain a $k$-term arithmetic progression. Determine the size of $G_k(N)$. How does it relate to $R_k(N)$, the size of the largest subset of $\{1,\ldots,N\}$ without a $k$-term arithmetic progression? Is it true that\[\lim_{N\to \infty}\frac{R_3(N)}{G_3(N)}=1?\]
- 题意摘要：对有限 A⊂ℤ 定义 r_k(A)=max{|B|:B⊂A 且 B 不含非平凡 k 项 AP}；则 G_k(N)=min_{|A|=N}r_k(A)，而 R_k(N)=r_k({1,…,N})。问题要求 G_k(N) 的数量级、与 R_k(N) 的关系，并特别问 R_3(N)/G_3(N)→1 是否成立。
- 状态核对：总体问题及极限问题仍 open。平凡地 G_k≤R_k；KSS 已证明 R_k≪_kG_k，故二者相差至多依赖 k 的常数。候选答案关于 G₃(14)=7 超出了官方材料：官方只陈述 G₃(14)≤7，不能据此宣称等号。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试用随机仿射模素数转移。取 C⊂𝔽_p 为无非平凡循环 k-AP 的集合，随机选 u∈𝔽_p^*、v∈𝔽_p，并令 B={a∈A:ua+v∈C}。每个 a 以 |C|/p 的概率进入 B，故存在选择使 |B|≥N|C|/p。
- 局部结论：若 B 中有公差 d 且 p∤d 的整数 k-AP，其像是 C 中的非平凡循环 k-AP，矛盾；因此 B 中残留 AP 的公差全部被 p 整除。；这给出一个严格的单模筛选引理及期望大小 N|C|/p。；直接由定义有 G_k(N)≤R_k(N)；结合已知 KSS 定理则 c_kR_k(N)≤G_k(N)≤R_k(N)，但常数夹逼不能推出比值趋于 1。
- 第一阻塞点：模筛选的第一处失败是无法处理 p|d 的等差数列。A 可被对手整体放入同一模 p 剩余类，甚至取 A=pA′；此时筛选没有减少任何加法结构，单模方法不具尺度不变性。
- 下一步：重建 KSS 的尺度不变归约：先对 A 除去全体元素差的最大公因子，再逐条核对其线性方程定理如何迭代处理“全部公差被 p 整除”的剩余类；记录所得常数是否可能随 N 改善为 1+o(1)。
- 来源核对：Erdős Problems #201 给出 G_k≤R_k、KSS 的 R_k≪_kG_k，以及小例 G₃(5)=3、G₃(14)≤7：https://www.erdosproblems.com/201；KSS 原论文：Komlós–Sulyok–Szemerédi, Acta Math. Acad. Sci. Hungar. 26 (1975), 113–121。；已直接核验候选中的五元集合 {1,3,4,5,7}：删去任一元素后仍有三项 AP，因此其最大三项无关子集至多 3；三元素子集显然可取，故确证 G₃(5)≤3 的见证。
- 时间记账：所在批次墙钟时间按题数均摊约 63.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/201)；既有候选答案（按不可信材料审计）

### #202

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $n_1<\cdots < n_r\leq N$ with associated $a_i\pmod{n_i}$ such that the congruence classes are disjoint (that is, every integer is $\equiv a_i\pmod{n_i}$ for at most one $1\leq i\leq r$). How large can $r$ be in terms of $N$?
- 题意摘要：定义 f(N) 为满足下列条件的最大 r：存在严格递增模数 1≤n₁<⋯<n_r≤N 及剩余类 aᵢ mod nᵢ，使任意两类在 ℤ 中不相交。结论是当 N→∞，若 L(N)=exp(√(log N log log N))，则 f(N)=N L(N)^{-1+o(1)}。
- 状态核对：官方页于 2026 年记录为 solved (Lean)，旧候选所称“精确阶仍开放”已经过时。不过官方页同时写着完整命题尚无本地形式化；因此这里只重建并核对新证明的数学路线，不把状态标签误说成已核验整篇 Lean 证明。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：重建 Ho 的新上界路线。先用判据 a mod q 与 b mod r 相交当且仅当 a≡b mod gcd(q,r)。经 BFV 剪枝，把极值族缩为模数具有相同素因子数 K≪√(log N/log log N)、不同平方自由核的子族。剩余素数支撑形成相交的 K-均匀集合族。Park–Pham 的 spread-disjointness 推出 dense-core 引理：某非空核 C 出现在至少 (C₀log(eK))^{-|C|} 比例的成员中。反复固定该核及相应素数幂，构造下降链；与具有给定素因子数的整数计数比较，最终优化得到上界常数 1。下界沿用 BFV 构造。
- 局部结论：两剩余类不相交等价于 aᵢ≢aⱼ mod gcd(nᵢ,nⱼ)；这是把算术问题转成相交支撑族的严格入口。；若一个相交 k-均匀族对每个非空 T 都满足 |F_T|≤|F|κ^{-|T|}，且 κ≥C·2log(ek)，则 spread-disjointness 会给出两个不交成员，矛盾；故确有密核 C，损失仅为 (C₀log(eK))^{|C|}。；在 K≪√(log N/log log N) 下，下降链累计的 log K 损失为 exp(o(log N))，不改变 L(N) 指数常数；证明文中的最终不等式 1+o(1)≤cσ-c²/4≤σ² 给出 σ≥1+o(1)。
- 第一阻塞点：本次筛查没有从头复证 BFV 剪枝命题及其所有一致的 o(1) 估计；新论证的闭合依赖这些输入。dense-core 新步骤和最终代数优化可直接核对，但整条证明的独立重建在此处停止。
- 下一步：逐项对照 BFV 原文重证新文 Proposition 3.1、Lemma 3.2 的统一性，特别检查把每步 L(o(1),N) 累积 O(K) 次仍为 exp(o(log N)) 的量词。
- 来源核对：[官方问题页](https://www.erdosproblems.com/202) 已核对最新状态、结论及更新时间。；[新证明全文](https://boonsuan.github.io/erdos202.pdf) 已核对 Theorem 1.1、spread-core 引理、下降链与最终优化。；旧候选只复述 2013 年上下界，未包含 2026 年解决结果。
- 时间记账：所在批次墙钟时间按题数均摊约 44.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/202)；既有候选答案（按不可信材料审计）

### #203

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an integer $m$ with $(m,6)=1$ such that none of $2^k3^\ell m+1$ are prime, for any $k,\ell\geq 0$?
- 题意摘要：求证是否存在正整数 m≥1，满足 gcd(m,6)=1，且对所有自然数 k,l≥0，2^k3^l m+1 都不是素数。这里是一个 m 同时应付全部二维指数对。
- 状态核对：仍为开放题。旧候选提出 m=-1，但官方现明确要求 m≥1；本地 Lean 中 m,k,l 也都是 ℕ，因此该“反例”越出论域，必须剔除。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试二维有限覆盖同余法。对选定素数 p∤6，若给定指数格中的一个周期单元 C_p={(k,l):2^k3^l≡c_p mod p}，便规定 m≡-c_p^{-1} mod p；则 C_p 内所有 2^k3^l m+1 均被 p 整除。若能用有限个不同素数对应的周期单元覆盖 ℕ²，CRT 可同时选出 m，并另加 m≡1或5 mod 6。
- 局部结论：对每个 p∤6，条件只依赖于 (k mod ord_p(2), l mod ord_p(3))，所以每个素数产生一个可明确计算的二维周期覆盖块。；若存在有限覆盖且所用素数互异，CRT 给出无穷多个满足全部整除条件并与 6 互素的正整数 m。取足够大的 CRT 代表元，还可保证各被 p 整除的数严格大于 p，从而确为合数。；必要条件 k=l=0 已迫使 m+1 合数；同时 m 必须为奇数且不被 3 整除。
- 第一阻塞点：第一处不能闭合的是构造有限素数族，使集合 {(k,l):2^k3^l≡c_p mod p} 覆盖整个 ℕ²。一般矩形同余类不能任意实现为这种乘法轨道等值集，二维覆盖的兼容性正是实质障碍。
- 下一步：做有限可检验搜索：枚举 p≤B、计算 ord_p(2)、ord_p(3) 及所有等值单元，把一个共同周期盒上的覆盖问题编码为 SAT/整数规划；若有解，再逐项核验 CRT 与合数性。
- 来源核对：[官方问题页](https://www.erdosproblems.com/203) 已核对 m≥1、开放状态及无已认领部分解。；已检查本地 203.lean：存在量词位于 ℕ，故负整数候选不适用。
- 时间记账：所在批次墙钟时间按题数均摊约 44.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/203)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/203.lean`；既有候选答案（按不可信材料审计）

### #205

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is it true that all sufficiently large $n$ can be written as $2^k+m$ for some $k\geq 0$, where $\Omega(m)<\log\log m$? What about $\Omega(m)<\epsilon\log\log m$, or another more slowly growing bound?
- 题意摘要：原命题断言：存在阈值 N₀，使每个 n≥N₀ 都有 k≥0 和正整数 m=n-2^k，满足 Ω(m)<log log m；并追问能否换成 εlog log m 或更慢趋于无穷的界。Ω 按重数计素因子。
- 状态核对：原命题已被反驳。官方记录更强结论：无穷多个 n 对每个 2^k<n 都有 Ω(n-2^k)≫√(log n/log log n)。限制 n 为奇数的变体仍开放。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 CRT 反例。固定大整数 E。对每个 0≤k<E 分配 E 个彼此不同的奇素数 p_{k,j}，并要求 n≡2^k mod p_{k,j}；同时要求 n≡0 mod 2^E。所有模数互素，CRT 给出一个同余类及无穷多个 n。于是 k<E 时 n-2^k 有 E 个不同奇素因子；k≥E 时 2^E整除n-2^k，故 Ω(n-2^k)≥E。
- 局部结论：上述 CRT 构造严格给出：对所有满足 2^k<n 的 k，Ω(n-2^k)≥E。；取最小正代表再加一个总模数，可令 log n=O(E²log E)：所用约 E² 个最小奇素数，其乘积对数为 O(E²log E)。因此 E≫√(log n/log log n)。；由于 0<n-2^k<n，故 log log(n-2^k)≤log log n=O(log E)，而 E/log E→∞；对充分大 E，每一种分解都违反 Ω(m)<log log m，且同样击破任意固定 εlog log m。
- 第一阻塞点：原命题的负解路线已经闭合。若要求官方最强渐近常数和完全形式化版本，则尚需精确引入第 E² 个素数的上界；但仅用 Bertrand 型粗界也足以反驳原命题。该构造依赖 n≡0 mod 2^E，不能处理奇数 n 变体。
- 下一步：将 CRT 构造写成独立引理，并分别用 Bertrand 上界和素数定理量化 log n；随后明确测试为何把 2^E 条件替换为奇数剩余类会使 k≥E 的统一控制失效。
- 来源核对：[官方问题页](https://www.erdosproblems.com/205) 已核对负解、量化下界及奇数变体状态。；[官方讨论](https://www.erdosproblems.com/forum/thread/205) 明确记录 CRT 机制和形式化链接；这里已独立重建其核心论证。
- 时间记账：所在批次墙钟时间按题数均摊约 44.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/205)

### #208

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $s_1<s_2<\cdots$ be the sequence of squarefree numbers. Is it true that, for any $\epsilon>0$ and large $n$,\[s_{n+1}-s_n \ll_\epsilon s_n^{\epsilon}?\]Is it true that\[s_{n+1}-s_n \leq (1+o(1))\frac{\pi^2}{6}\frac{\log s_n}{\log\log s_n}?\]
- 题意摘要：令 s₁<s₂<⋯ 枚举全部正平方自由整数。第一问量词为：对每个 ε>0，存在 C_ε和n₀，使 n≥n₀ 时 s_{n+1}-s_n≤C_εs_n^ε。第二问要求存在 η_n→0，使最终 s_{n+1}-s_n≤(1+η_n)(π²/6)log s_n/log log s_n。
- 状态核对：两问均无条件开放。已知第一问由 ABC 推出；无条件上界仍是幂次型。第二问的常数 π²/6 与 Erdős 的无穷多大间隙下界相匹配。旧候选的总体状态正确，但其数值性旁枝不构成证明进展。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试直接分析一个不含平方自由数的区间 (x,x+H]。每个 h≤H 必有某素数 p 使 p²整除x+h。把素数按 p≤√H 与 p>√H 分开：小素数 p²在区间内最多命中 H/p²+1 个位置；大素数平方最多命中一个位置。希望证明大素数平方不能覆盖剩余的正比例位置，从而得到短区间上界。
- 局部结论：小素数平方覆盖的位置数至多 H∑_{p≤√H}1/p²+π(√H)。由于 ∑_p1/p²<1，这一部分单独不能覆盖全部 H 个位置。；因此若整个区间都非平方自由，则有正比例的 h 对应某个 p>√H 且 p²∣x+h；同一 p 至多对应一个 h。问题严格归约为控制短区间内具有大平方因子的整数数目。；反向地，给每个 1≤h≤H 选择不同素数 p_h，并用 CRT 解 x≡-h mod p_h²，可构造任意长的平方自由间隙；但这种朴素选择只给 log x约为2Hlog H，达不到猜想中的 π²/6 常数。
- 第一阻塞点：第一处无法闭合的是对 p>√H 的大平方因子作足够强且统一的短区间计数。平凡求和给出的界过大；要达到 x^ε 或对数尺度，需要远强于初等筛的相关性控制。
- 下一步：先复现 Filaseta–Trifonov/Pandey 方法中的大平方因子计数命题，明确其指数 1/5 的来源；计算若该命题中的关键误差改进到何种强度，才会推出任意 ε 上界。
- 来源核对：[官方问题页](https://www.erdosproblems.com/208) 已核对开放状态、已知无条件指数及 ABC 条件结果。；已核对本地 208.lean：第一问使用 atTop 大 O；第二问使用趋零函数和最终量词。
- 时间记账：所在批次墙钟时间按题数均摊约 44.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/208)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/208.lean`；既有候选答案（按不可信材料审计）

### #212

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a dense subset of $\mathbb{R}^2$ such that all pairwise distances are rational?
- 题意摘要：问是否存在 S⊆ℝ²，使 S 在整个平面稠密，并且对任意不同 P,Q∈S，欧氏距离 |P-Q| 都属于 ℚ。稠密性和全体点对的有理距离必须同时成立。
- 状态核对：仍为开放题；Bombieri–Lang 条件下不存在。旧候选的开放状态正确，但“圆上存在稠密例子”即使正确也只说明一维子集可行，不能接近平面稠密性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：作坐标归约。若 S 稠密，可取三个不共线点 A,B,C∈S。经平移、旋转并按有理数 |AB| 缩放，令 A=(0,0)、B=(1,0)、C=(u,v)。由 AC、BC∈ℚ 得 u∈ℚ、d=v²∈ℚ_{>0}。对任意 P=(x,y)∈S，由 PA、PB∈ℚ 得 x∈ℚ、y²∈ℚ；再由 PC∈ℚ 得 yv∈ℚ，所以 y=qv、q∈ℚ。于是问题归约为在 ℚ² 中寻找对二次型 Q(Δx,Δq)=Δx²+dΔq² 的平方值形成的稠密无限团。
- 局部结论：任一候选稠密集经相似变换后必包含于 {(x,q√d):x,q∈ℚ}，其中固定 d∈ℚ_{>0}。；对任意两点对应的有理坐标 (x,q)、(x',q')，必要且充分的距离条件是 (x-x')²+d(q-q')² 为 ℚ 中的平方。；该载体本身在 ℝ² 稠密，但两点差的二次型一般不是平方；因此稠密性并未自动解决全对条件，困难被集中为一个明确的有理二次型 clique 问题。
- 第一阻塞点：第一处不能闭合的是：无法证明上述二次型平方图不存在稠密无限团，也无法递归加入新点并保持与既有所有点的距离为有理数。加入有限多个点对应若干二次曲线的联立条件；点数增加后会进入高亏格曲线/一般型簇，而无条件缺乏所需的有理点有限性定理。
- 下一步：固定四个一般位置基点，显式消元写出第五点的参数曲线并计算其属；检验退化到直线或圆的条件。这可精确定位 Bombieri–Lang 路线中首次需要深层算术几何之处。
- 来源核对：[官方问题页](https://www.erdosproblems.com/212) 已核对开放状态、Bombieri–Lang 条件结论及代数曲线结构结果。；已核对本地 212.lean：以 ℂ 表示 ℝ²，要求 Dense 且对不同点的距离落在 Rat.cast 的像中。
- 时间记账：所在批次墙钟时间按题数均摊约 44.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/212)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean`；既有候选答案（按不可信材料审计）
- 深度项目：深度运行已 Lean 验证反演所得不可约三次曲线、无限有理距离零点集的传递以及射影参数化双射。第一未闭合点是多项式到 $\operatorname{RatFunc}(\mathbb R)$ 参数化的反向核包含/精确核等式，之后才可能建立函数域有理性与属层面的结论；这些局部定理不能改写为整题已解。 [证据](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/runs/erdos212-quadratic-to-irreducible-cubic/erdos212-quadratic-to-irreducible-cubic-supervised-4h/proof_lab/round-026/summary.md)

### #213

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n\geq 4$. Are there $n$ points in $\mathbb{R}^2$, no three on a line and no four on a circle, such that all pairwise distances are integers?
- 题意摘要：量词是：对每个整数 n≥4，是否分别存在一个恰含 n 个点的有限集 S⊂R²，使任意三点不共线、任意四点不共圆，且每个无序点对的欧氏距离均为整数；不是要求一个无限点集同时容纳所有 n。
- 状态核对：截至核查时仍为 open。Kreisel–Kurz 已严格构造 7 点例，因此 4≤n≤7 均成立；n≥8 未知。候选所列坐标未在本轮逐项验算，故不把它当作证明依据。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：固定两点 A=(0,0)、B=(D,0)，D∈Z_{>0}。若新点 P 到 A、B 的整数距离分别为 a,b，则 P=(x,y) 必须满足 x=(a²-b²+D²)/(2D)，y²=a²-x²>0。尝试把增点问题归约为：寻找多个整数对 (a,b)，使所得二次域坐标之间的所有距离也为整数，同时避开有限多个共线、共圆方程。
- 局部结论：一般位置和整距性质都对子集遗传；故已知 7 点构型严格推出每个 4≤n≤7 的存在性。；相对于固定整数基边 AB，每个候选新点的横坐标是有理数，纵坐标平方是有理数；因此所有候选点均落在由有限个平方根生成的代数扩张中。；给定已有有限构型，共线和共圆禁条件各排除有限条直线或圆；真正困难不是一般位置，而是同时满足到所有旧点的整数距离。
- 第一阻塞点：从第三个旧点开始，还需对每个 P_i 强制 (x-x_i)²+(y-y_i)² 为完全平方整数；没有可用的局部—整体原理或参数族保证这些二次条件能同时相容。这里是该增点路线的第一处未闭合步骤。
- 下一步：以公开 7 点构型为输入，精确计算满足到其中任取三点距离为整数的低高度代数候选点，再逐个检验其到其余四点的距离；这能检验“直接增添第八点”路线，而不声称穷尽所有构型。
- 来源核对：本地 213.lean 确认对象是恰有 n 点的有限集合，且陈述为 ∀n≥4 的存在性。；Erdős Problems 当前页面仍列为 OPEN：https://www.erdosproblems.com/213；Kreisel–Kurz 原论文存档明确声称给出两个满足条件的 7 点构型：https://epub.uni-bayreuth.de/id/eprint/649/
- 时间记账：所在批次墙钟时间按题数均摊约 47.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/213)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/213.lean`；既有候选答案（按不可信材料审计）

### #217

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which $n$ are there $n$ points in $\mathbb{R}^2$, no three on a line and no four on a circle, which determine $n-1$ distinct distances and so that (in some ordering of the distances) the $i$th distance occurs $i$ times?
- 题意摘要：对给定 n，要求存在 n 个平面点，任意三点不共线、任意四点不共圆；全部 C(n,2) 个无序点对恰产生 n−1 个不同距离，并可把这些距离编号为 1,…,n−1，使第 i 种距离恰出现 i 次。因 1+⋯+(n−1)=C(n,2)，这些重数正好覆盖全部点对。
- 状态核对：截至核查时仍为 open。已知 n≤8 存在；这里若允许正整数 n，则 n=1,2 是空/单距离的平凡情形，n=3 可取非等边等腰三角形，n=4 可取非直角等腰三角形及其外心。n≥9 未知；候选把“没有已知构造”表述成所有 n≥9 均未知是合适的，但不是不存在证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把完全图 K_n 的边按距离着色，第 i 个颜色类恰有 i 条边；尝试先从一般位置推出每个颜色图的组合限制，再枚举 n=9 的有限颜色型，最后用距离几何方程判定可实现性。
- 局部结论：固定点 P 和固定距离 r，同距邻点都在以 P 为圆心、r 为半径的圆上；无四点共圆立即给出每个距离颜色在每个顶点的度数至多 3。；因此含 i 条边的颜色类至少接触 ceil(2i/3) 个顶点；特别是重数 n−1 的距离至少接触 ceil(2(n−1)/3) 个点。；n=4 的外心构造中，三条外接半径、两条等腰边和一条底边分别给出重数 3、2、1；选非直角且非等边的等腰三角形即可保持一般位置。
- 第一阻塞点：最大度≤3 等组合约束仍允许大量具有边数 1,…,n−1 的边分拆；尚无论证说明 n=9 的每一种可行着色都违反某个 Cayley–Menger 行列式、共线或共圆条件。这是从组合筛选过渡到几何不可能性的首个缺口。
- 下一步：枚举 K_9 的边着色同构类，颜色类大小固定为 1,…,8，并先施加每色最大度≤3；对剩余类型建立平方距离变量及所有五点 Cayley–Menger 行列式为零的方程，选最小类型做 Gröbner 基或实可满足性检验。
- 来源核对：Erdős Problems 当前页面仍列为 OPEN，并分别记录 Palásti 的 n=6,7,8 构造：https://www.erdosproblems.com/217；候选引用的术语“crescent configuration”可用于检索，但本轮结论只依赖官方问题页及上述直接推导。
- 时间记账：所在批次墙钟时间按题数均摊约 47.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/217)；既有候选答案（按不可信材料审计）

### #218

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d_n=p_{n+1}-p_n$. The set of $n$ such that $d_{n+1}\geq d_n$ has density $1/2$, and similarly for $d_{n+1}\leq d_n$. Furthermore, there are infinitely many $n$ such that $d_{n+1}=d_n$.
- 题意摘要：令 p_n 为第 n 个素数、d_n=p_{n+1}−p_n。三个断言分别是：集合 {n:d_{n+1}≥d_n} 的自然密度为 1/2；集合 {n:d_{n+1}≤d_n} 的自然密度为 1/2；集合 {n:d_{n+1}=d_n} 无限。有限个初始索引不影响密度。
- 状态核对：整体仍为 open。两个密度 1/2 断言及相等事件无限多均未解决。本轮可严格推进候选中的辅助结论：在采用标准、对 d 一致的 Brun 三元组上界后，相等事件的自然密度为 0；这与其可能无限并不矛盾。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：令 T(x)=#{n:p_{n+2}≤x，d_n=d_{n+1}}，按共同间距 d 是否超过 y=(log x)^(4/3) 分割。大间距用间距总和伸缩；小间距放宽为计数素数三元组 m,m+d,m+2d，再用 Brun 上界。
- 局部结论：若 d>y，则相应首个素数间距也大于 y，而 ∑_{p_m≤x}d_m≪x，故 T_{>y}(x)≪x/y=o(π(x))。；若 d不被3整除，则除涉及素数3的有限例外外，m,m+d,m+2d 中必有一个被3整除；主要贡献只需考虑 6|d。；标准一致 Brun 筛给出 A_d(x)≪x(log x)^(−3)∏_{p|d}(1−1/p)^(−2)。对 d≤y，该乘积至多为缓慢增长因子；求和得 T_{≤y}(x)≪xy(loglog y)^{O(1)}/(log x)^3=o(π(x))。因此相等事件密度为0，并使两个非严格密度断言等价于相应严格不等式的密度断言。
- 第一阻塞点：这条路线无法从“相等事件密度为0”推出其无限性，也无法比较严格上升与严格下降事件的频率。所需的是连续素数间距的联合分布；现有无条件筛法没有给出足以证明对称密度 1/2 的误差项。
- 下一步：把小间距步骤写成独立引理，明确给出对所有 d≤(log x)^(4/3) 一致的 Brun 筛常数和奇异级数界；随后数值检验严格上升比例的收敛速度，但仅作为联合分布猜想的诊断。
- 来源核对：本地 218.lean 确认三个断言被分别形式化；其中注释所称“等价于三项等差素数”应理解为三项连续素数等差数列。；当前问题页仍列整体为 OPEN，并记录 Banks 的条件性启发式：https://www.erdosproblems.com/218；讨论页记载了同一小/大间距分割，但该页也未把它列作经同行审查的正式部分解答，因此本轮仅在明确调用标准一致 Brun 筛时接受该辅助结论：https://www.erdosproblems.com/forum/thread/218
- 时间记账：所在批次墙钟时间按题数均摊约 47.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/218)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/218.lean`；既有候选答案（按不可信材料审计）

### #222

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_1<n_2<\cdots$ be the sequence of integers which are the sum of two squares. Explore the behaviour of (i.e. find good upper and lower bounds for) the consecutive differences $n_{k+1}-n_k$.
- 题意摘要：令 n_1<n_2<⋯ 为所有可表示成 a²+b² 的正整数的递增序列，研究每一个相邻差 g_k=n_{k+1}−n_k 的统一上界、无穷多次下界及典型行为；这是开放式“求好界”，不是单一真假命题。
- 状态核对：仍为 open。已知统一上界 g_k≪n_k^(1/4)，以及无穷多次 g_k≥(0.868…−o(1))log n_k。候选基本记录正确，但 Landau–Ramanujan 计数渐近本身只推出平均间距尺度，不能单独推出“多数间距”结论。其区间上界还需从 x=n_k+1 开始，才确保找到的是下一项而非 n_k 本身。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建 Bambah–Chowla 型四次方根上界：对任意整数 x，取 u=floor(sqrt x)、r=x−u²，并令 v=ceil(sqrt r)。同时用二平方和判别定理和中国剩余定理构造显式空区间。
- 局部结论：u²+v²≥x，且 u²+v²−x=v²−r<2sqrt(r)+1≤2sqrt(2)x^(1/4)+1。取 x=n_k+1，得到 n_{k+1}−n_k≤2sqrt(2)(n_k+1)^(1/4)+2。；对任意 L，选互异素数 q_j≡3 mod 4，并用 CRT 令 A+j≡q_j mod q_j²；则 v_{q_j}(A+j)=1，所以 A+1,…,A+L 均非二平方和，故间距无界。；m²与m²+1=m²+1² 是相邻整数且均为二平方和，所以它们必为序列中的相邻项；从而 g_k=1 无穷多次，liminf g_k=1。
- 第一阻塞点：上界构造的损失来自 v²−r=O(sqrt r)，而最坏情形 r约为sqrt x，正好产生 x^(1/4)。要改进指数，必须证明在若干邻近的 u 中至少有一个剩余 x−u²异常接近平方；简单取整没有这种统一保证。CRT 路线则因模数约为所选素数乘积的平方，只给出远弱于 c log x 的定量下界。
- 下一步：对长度 H≈x^(1/4−δ) 的一段候选 u，研究剩余 x−u² 到最近平方的最小距离；先计算其最坏样本并检验能否由模分布或间隔原理得到优于单个 u 的覆盖引理。
- 来源核对：当前问题页确认最佳统一上界 n_k^(1/4) 和已公布的 0.868… 对数下界：https://www.erdosproblems.com/222；DEKKM 原论文记录页：https://arxiv.org/abs/1810.03203
- 时间记账：所在批次墙钟时间按题数均摊约 47.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/222)；既有候选答案（按不可信材料审计）

### #233

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d_n=p_{n+1}-p_n$, where $p_n$ is the $n$th prime. Prove that\[\sum_{1\leq n\leq N}d_n^2 \ll N(\log N)^2.\]
- 题意摘要：存在绝对常数 C、N_0，使所有 N≥N_0 都有 ∑_{1≤n≤N}(p_{n+1}−p_n)²≤CN(log N)²。等价地，前 N 个素数间距的均方根为 O(log N)。
- 状态核对：截至核查时仍为 open。本地 Lean 陈述用 atTop 的大 O 表达同一量词。已知 PNT 给出匹配下界；Maynard 无条件证明按 p_n≤x 求和时为 O_ε(x^(5/4+ε))，远弱于目标。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把二次矩写成大间距尾分布。令 A_x(h)=#{n:p_n≤x，d_n>h}，则精确地 ∑_{p_n≤x}d_n²=∫_0^∞2hA_x(h)dh。尝试用短区间中无素数事件的筛估计控制 A_x(h)。
- 局部结论：Cauchy–Schwarz及 ∑_{n≤N}d_n=p_{N+1}−2 给出 ∑d_n²≥(p_{N+1}−2)²/N≫N(log N)²，所以目标阶数若成立即为最佳。；目标上界立即推出尾界 #{n≤N:d_n≥H}≤CN(log N)²/H²，以及逐项界 d_n≪sqrt(n)log n。；若能一致证明 A_x(h)≪(x/log x)exp(−c h/log x)，尾积分便给出 O(x log x)，经 x约为N log N 转换正是 O(N(log N)²)。这准确定位了所需的概率型输入。
- 第一阻塞点：上界筛擅长控制“若干指定数同时为素数”，却不能给出所需强度的“整个区间没有素数”事件上界；素数间的相关性和极端大间距使指数尾估计超出现有无条件短区间理论。这是尾积分路线的第一处不可闭合步骤。
- 下一步：先证明一个分段版本：对 dyadic H，整理现有技术能给出的 A_x(H) 上界并代入 ∑_j H_j²A_x(H_j)；明确究竟是哪一段 H 对 Maynard 的 x^(5/4+ε) 总界贡献最大，从而把改进目标缩成一个可检验的尾区间估计。
- 来源核对：本地 233.lean 确认目标为 N→∞ 的大 O，并另列 PNT 下界和 RH 条件上界。；当前问题页仍列为 OPEN：https://www.erdosproblems.com/233；Maynard 原论文摘要明确给出 ∑_{p_n≤x}d_n²≪_εx^(5/4+ε)：https://arxiv.org/abs/1201.1787
- 时间记账：所在批次墙钟时间按题数均摊约 47.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/233)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/233.lean`；既有候选答案（按不可信材料审计）

### #234

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For every $c\geq 0$ the density $f(c)$ of integers for which\[\frac{p_{n+1}-p_n}{\log n}< c\]exists and is a continuous function of $c$.
- 题意摘要：令 \(p_n\) 为第 \(n\) 个素数、\(d_n=p_{n+1}-p_n\)。问题要求存在同一个连续函数 \(f:[0,\infty)\to\mathbb R\)，使对每个固定 \(c\ge0\)，集合 \(\{n:d_n/\log n<c\}\) 的自然密度存在且等于 \(f(c)\)。有限个 \(n\) 上 \(\log n\) 的异常不影响密度。
- 状态核对：截至核对日官网仍标为 open；没有把先前候选中的 Poisson 启发式当作证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：走 Gallagher 型条件归约：把 \(d_n>c\log p_n\) 改写为素数 \(p_n\) 后长度约 \(c\log p_n\) 的区间内没有素数，再用容斥把“空区间”概率展开为固定阶素数元组计数。若对每个固定阶都有足够一致的 Hardy–Littlewood 渐近，平均奇异级数给出各阶因子矩，Bonferroni 截断后令阶数趋于无穷，得到尾分布 \(e^{-c}\)，即 \(f(c)=1-e^{-c}\)。
- 局部结论：经验分布 \(F_N(c)=N^{-1}|\{n\le N:d_n/\log n<c\}|\) 对 \(c\) 单调；因而任何逐点子列极限也是单调的。；严格不等式下 \(F_N(0)=0\)，故若所求密度存在则 \(f(0)=0\)。；在上述统一 Hardy–Littlewood 假设下，容斥路线确实给出连续的指数分布；但这只是条件结论。
- 第一阻塞点：第一处无条件无法闭合之处，是连空区间概率所需的高阶联合素数统计都不可得；现有筛法上下界不能证明 \(F_N(c)\) 收敛。另有 \(\log p_n/\log n\to1\)，但仅凭此不能无条件替换归一化：还需控制落在移动边界窄带中的间隙比例。
- 下一步：写出固定截断阶 \(K\) 的 Bonferroni 上下界，并逐项标明所需的素数 \(k\)-元组一致性；先核验 \(K=1,2\) 时现有筛法究竟能给出哪些严格的 limsup/liminf 界。
- 来源核对：[Erdős Problems #234](https://www.erdosproblems.com/234) 于核对时仍标 OPEN。；已检查本地 Lean 陈述：它形式化为存在连续 \(f\)，且每个 \(c\) 对应集合具有自然密度。；[Pintz 关于 Gallagher 奇异级数定理的论文](https://arxiv.org/abs/1004.1084)支持条件路线中的平均奇异级数环节，而非无条件结论。
- 时间记账：所在批次墙钟时间按题数均摊约 60.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/234)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/234.lean`；既有候选答案（按不可信材料审计）

### #236

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ count the number of solutions to $n=p+2^k$ for prime $p$ and $k\geq 0$. Is it true that $f(n)=o(\log n)$?
- 题意摘要：对每个整数 \(n\)，\(f(n)=|\{k\ge0:n-2^k\text{ 为素数}\}|\)。问题是点态地证明 \(f(n)/\log n\to0\)，而不是只对几乎所有 \(n\) 或某个子列成立。
- 状态核对：官网截至 2026 年仍标为 open，并记录 Erdős 已证明无限多个 \(n\) 满足 \(f(n)\gg\log\log n\)。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试在指数变量 \(k\) 上筛。若奇素数 \(q\nmid n\)，且 \(d=\operatorname{ord}_q(2)\)，那么满足 \(2^k\equiv n\pmod q\) 的一个剩余类 \(k\bmod d\) 必须从候选指数中删去；除去至多一个使 \(n-2^k=q\) 的例外，否则该差为合数。目标是对许多小素数 \(q\) 联合筛去 \([0,\log_2n]\) 中比例趋近于一的指数。
- 局部结论：平凡地 \(f(n)\le \lfloor\log_2 n\rfloor+1=O(\log n)\)。；精确的一阶矩恒等式为 \(\sum_{n\le N}f(n)=\sum_{2^k<N}\pi(N-2^k)\)；由素数定理可得该和为 \((1+o(1))N/\log2\)。；由上一式和 Markov 不等式，任意固定 \(\varepsilon>0\) 下，满足 \(f(n)\ge\varepsilon\log n\) 的 \(n\le N\) 至多为 \(O_\varepsilon(N/\log N)+O(\sqrt N)\)，故反例若存在只能形成零密度集合。
- 第一阻塞点：指数筛的第一处障碍是删去的剩余类模数 \(\operatorname{ord}_q(2)\) 高度相关，而且当 \(q\mid n\) 时该素数完全不给限制。现有信息不足以对所有 \(n\) 统一证明剩余指数的比例趋于零；一阶平均估计也无法排除稀疏的极端 \(n\)。
- 下一步：固定参数 \(y\)，对 \(q\le y\) 建立一个完全显式的指数筛上界，并按 \(q\mid n\) 与 \(q\nmid n\) 分类；检验能否仅用乘法阶的已知分布把上界改进到 \(o(\log n)\)，或明确找出最坏的模数相关结构。
- 来源核对：[Erdős Problems #236](https://www.erdosproblems.com/236) 于 2026 年页面仍标 OPEN，并给出 \(\gg\log\log n\) 的已知下界。；本地 Lean 定义只枚举 \(0\le k\le\lfloor\log_2n\rfloor\)，与原问题等价；其结论是 atTop 上真正的 little-o。
- 时间记账：所在批次墙钟时间按题数均摊约 60.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/236)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/236.lean`；既有候选答案（按不可信材料审计）

### #238

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c_1,c_2>0$. Is it true that, for any sufficiently large $x$, there exist more than $c_1\log x$ many consecutive primes $\leq x$ such that the difference between any two is $>c_2$?
- 题意摘要：量词是：对任意固定 \(c_1,c_2>0\)，存在 \(X(c_1,c_2)\)，使每个实数 \(x\ge X\) 前都能找到超过 \(c_1\log x\) 个在全体素数序列中连续、且均不超过 \(x\) 的素数，任意两者之差均大于 \(c_2\)。对递增素数块，这等价于块内所有相邻素数间隙都大于 \(c_2\)。
- 状态核对：完整量词仍为 open；“\(c_1\) 足够小”版本已知。官网文字称依赖于 \(c_1\) 显然是自指笔误，数学上应是阈值依赖于 \(c_2\)。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把间隙 \(\le c_2\) 称为坏间隙。对有限多个整数 \(1\le h\le c_2\)，Brun 上界筛给出 \(|\{p\le x:p,p+h\text{ 均素}\}|=O_h(x/\log^2x)\)，所以坏间隙总数 \(B(x)=O_{c_2}(x/\log^2x)\)。用这些坏间隙切割前 \(\pi(x)\) 个素数，最长好间隙串至少有平均长度量级。
- 局部结论：任意两素数之差大于 \(c_2\) 与全部相邻差大于 \(c_2\) 等价。；由 \(\pi(x)\sim x/\log x\) 及 \(B(x)=O_{c_2}(x/\log^2x)\)，最长连续好间隙串长度为 \(\gg_{c_2}\log x\)。；因此存在 \(c_*(c_2)>0\)，使结论对所有 \(0<c_1<c_*(c_2)\) 成立；这重建了官方所述的小 \(c_1\) 情形。
- 第一阻塞点：平均串长只给一个固定常数乘 \(\log x\)，不能处理任意大的 \(c_1\)。而且不能期望仅把 \(B(x)\) 改成 \(o(x/\log^2x)\)：固定小素数差的素数对预计本就有 \(\asymp x/\log^2x\) 个。需要控制好串长度的尾部，而非仅控制坏间隙总数。
- 下一步：令 \(L=\lceil c_1\log x\rceil\)，研究长度 \(L\) 的索引块含坏间隙的二阶矩或高阶覆盖数；先证明坏间隙对的联合筛上界是否足以排除“每个长度 \(L\) 块都被覆盖”。
- 来源核对：[Erdős Problems #238](https://www.erdosproblems.com/238) 于 2026 年仍标 OPEN，并确认小 \(c_1\) 版本。；本地 Lean 文件另列 small_c1 为 solved variant；形式化条件采用相邻 primeGap，与上述等价化一致。
- 时间记账：所在批次墙钟时间按题数均摊约 60.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/238)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/238.lean`；既有候选答案（按不可信材料审计）

### #241

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be the maximum size of $A\subseteq \{1,\ldots,N\}$ such that the sums $a+b+c$ with $a,b,c\in A$ are all distinct (aside from the trivial coincidences). Is it true that\[ f(N)\sim N^{1/3}?\]
- 题意摘要：令 \(A\subseteq\{1,\dots,N\}\)。允许三元组有重复；要求若 \(a_1+a_2+a_3=b_1+b_2+b_3\)，则两个三元素多重集相同，排列造成的重合才算“平凡”。\(f(N)\) 是此类 \(A\) 的最大基数；问题问 \(f(N)/N^{1/3}\to1\)。
- 状态核对：官网仍标 open。先前候选关于 White 改进的方向是对的：原论文确实改进了 \(B_3[1]\) 上界；官网仍写 Green 最佳，属于未更新备注。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先做三重和计数，再尝试 Green–White 的能量路线。若 \(|A|=m\)，无序可重复三元组有 \(\binom{m+2}{3}\) 个，且其和落在 \([3,3N]\)。更强路线把 \(1_A*1_A\) 的 \(L^2\) 能量下界，与 \(B_3\) 性质给出的表示数上界结合，并通过缩放化为非负函数的自卷积极值问题。
- 局部结论：直接计数严格给出 \(\binom{m+2}{3}\le3N-2\)，故 \(m\le(18N)^{1/3}+O(1)\)；这只确定指数。；Bose–Chowla 构造给出 \(f(N)\ge(1-o(1))N^{1/3}\)。；White 的已核对推论给出 \(\limsup f(N)/N^{1/3}\le(2/0.574636066)^{1/3}\approx1.5155\)，确实略优于 Green 的 \((7/2)^{1/3}\approx1.5183\)。
- 第一阻塞点：能量路线要把常数降到 1，需要远强于现有自卷积下界或额外利用 \(B_3\) 的离散结构。White 的极值常数本身约为 0.57464，代入该框架仍留下约 1.5155；因此单纯优化同一连续不等式无法闭合猜想。
- 下一步：检查 Green 能量论证中从离散 \(B_3\) 结构到连续自卷积不等式的每个松弛点，特别测试是否能加入三重表示唯一性所蕴含、但连续松弛丢失的约束；先在小 \(N\) 极值集合上数值比较这些松弛项。
- 来源核对：[Erdős Problems #241](https://www.erdosproblems.com/241) 于 2026-04 更新后仍标 OPEN，但其“Green 最佳”备注未吸收 White 的结果。；[White, An optimal L² autoconvolution inequality](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/an-optimal-l2-autoconvolution-inequality/8D109D51F271CC78EBDA2C99FB35612D) 的 Corollary 1.2 明列 \(\sigma_3(1)\le(2/\mu_2^2)^{1/3}\)，并给出 \(\mu_2^2\ge0.574636066\)。；本地 Lean 定义明确使用三元素 Multiset，因此包含重复元素并只容许多重集相同的重合。
- 时间记账：所在批次墙钟时间按题数均摊约 60.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/241)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/241.lean`；既有候选答案（按不可信材料审计）

### #243

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1<a_2<\cdots$ be a sequence of integers such that\[\lim_{n\to \infty}\frac{a_n}{a_{n-1}^2}=1\]and $\sum\frac{1}{a_n}\in \mathbb{Q}$. Then, for all sufficiently large $n\geq 1$,\[ a_n = a_{n-1}^2-a_{n-1}+1.\]
- 题意摘要：对任意严格递增正整数序列 \((a_n)\)，若 \(a_{n+1}/a_n^2\to1\)，且实数级数 \(S=\sum_n1/a_n\) 是有理数，则要证明存在 \(n_0\)，使所有 \(n\ge n_0\) 都满足 \(a_{n+1}=a_n^2-a_n+1\)。下标平移不影响原陈述。
- 状态核对：官网和本地形式化均仍标 open。先前候选把额外 LCM 条件下的 Erdős–Straus 定理与原猜想区分开，这一点必须保留。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从有理尾和的分母整除性入手。写 \(S=u/v\) 为既约分数，\(L_n=\operatorname{lcm}(a_1,\dots,a_n)\)，\(T_n=\sum_{j>n}1/a_j\)。则 \(M_n=vL_nT_n\) 是正整数。增长条件又使尾和由首项支配：\(T_n=(1+o(1))/a_{n+1}\)。随后研究整数 \(M_n\) 的递推，希望迫使它稳定并产生 Sylvester 递推。
- 局部结论：由最终的 \(a_{n+1}\ge a_n^2/2\) 可严格控制余尾，得到 \(T_n=1/a_{n+1}+O(1/a_{n+2})=(1+o(1))/a_{n+1}\)。；因为 \(vL_nS\) 及 \(vL_n\sum_{j\le n}1/a_j\) 都是整数，所以 \(M_n=vL_nT_n\in\mathbb Z_{>0}\)。因此 \(L_n/a_{n+1}\ge(1-o(1))/v\)。；若 Sylvester 递推最终成立，则 \(1/a_n=1/(a_n-1)-1/(a_{n+1}-1)\)，尾和严格望远镜化并必为有理数。
- 第一阻塞点：第一处无法闭合的是控制 \(M_n\) 或 \(L_n/a_{n+1}\) 的上界。精确地，\(M_{n+1}=(L_{n+1}/L_n)M_n-vL_{n+1}/a_{n+1}\)，其中 \(L_{n+1}/L_n=a_{n+1}/\gcd(a_{n+1},L_n)\) 可剧烈波动；近平方增长不给出所需的 gcd/LCM 控制。这正是 Erdős–Straus 附加条件所处理、原题尚缺的一步。
- 下一步：以整数递推 \(M_{n+1}=(L_{n+1}/L_n)M_n-vL_{n+1}/a_{n+1}\) 为核心，先检验附加假设 \(L_n/a_{n+1}=O(1)\) 下如何推出最终 Sylvester 递推，再精确定位证明中唯一使用该上界的位置，尝试用近平方条件替代。
- 来源核对：[Erdős Problems #243](https://www.erdosproblems.com/243) 于核对时仍标 OPEN，并记录其 LCM 型必要条件。；[Erdős–Straus 1964 原论文](https://combinatorica.hu/~p_erdos/1964-19.pdf)的 Theorem 1 在附加 \(L_n/a_{n+1}\) 有界条件下给出最终递推；不能把它误述成原问题的证明。；本地 Lean 陈述把有理性表达为 \(\mathbb Q\) 中的 Summable；这比单纯实级数收敛更直接地编码了有理和，但目标仍是同一 eventual recurrence。
- 时间记账：所在批次墙钟时间按题数均摊约 60.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/243)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/243.lean`；既有候选答案（按不可信材料审计）

### #244

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $C>1$. Does the set of integers of the form $p+\lfloor C^k\rfloor$, for some prime $p$ and $k\geq 0$, have density $>0$?
- 题意摘要：量词为：对每个固定实数 $C>1$，令 $A_C=\{p+\lfloor C^k\rfloor:p\text{ 为素数},\ k\in\mathbb N_0\}$；问其下渐近密度 $\liminf_{x\to\infty}|A_C\cap[1,x]|/x$ 是否严格为正。
- 状态核对：冻结状态为 open；2026 年页面仍列为开放。整数 $C\ge2$ 由 Romanoff 解决，Ding 证明几乎处处的实数 $C>1$ 成立。先前候选只正确概述状态，未构成证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：采用 Romanoff 二阶矩。取 $a_k=\lfloor C^k\rfloor\le x/2$，定义 $r_x(n)=\#\{k:n-a_k\text{ 为素数}\}$。先估计 $\sum_{n\le x}r_x(n)$，再希望由 Cauchy–Schwarz 从 $\sum r_x(n)^2=O_C(x)$ 推出支集有线性大小。
- 局部结论：满足 $a_k\le x/2$ 的互异移位数为 $K=(\log x)/(\log C)+O_C(1)$；由素数定理，$\sum_{n\le x}r_x(n)\ge K\pi(x/2)=(1/(2\log C)+o_C(1))x$。；对不同 $i,j$，筛法把相关项控制为 $\ll x(\log x)^{-2}\prod_{q\mid(a_j-a_i),\ q>2}(q-1)/(q-2)$。因此只要这些奇异因子的双重平均为 $O_C(K^2)$，便有 $\sum r_x^2=O_C(x)$，从而得到正下密度。；Ding 的几乎处处证明所使用的充分条件正是同类平均估计，例如以 $\prod_{q\mid(a_j-a_i)}(1+1/q)$ 表示的可比权重。
- 第一阻塞点：第一处无法闭合的是：对任意给定实数 $C$，尚不能一致证明 $\sum_{i<j\le K}\prod_{q\mid(\lfloor C^j\rfloor-\lfloor C^i\rfloor)}(1+1/q)\ll_C K^2$。整数幂的同余结构可处理，但取整后的任意实底数没有已知的逐点平均控制。
- 下一步：固定一个非整数代数数（首选 $C=\sqrt2$），计算并尝试证明上述奇异因子平均有界；具体先按平方根奇偶指数拆分 $\lfloor(\sqrt2)^k\rfloor$，检查能否归约为有限组整数幂差。
- 来源核对：本地 Lean 陈述明确采用 `lowerDensity`。；[Erdős Problem 244](https://www.erdosproblems.com/244) 仍标为开放，并记录整数情形与几乎处处结果。；[Ding 的论文](https://arxiv.org/abs/2503.22700) 明确证明几乎所有 $C>1$ 的正下密度，并给出上述二阶矩充分条件。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/244)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/244.lean`；既有候选答案（按不可信材料审计）

### #247

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1<a_2<\cdots$ be a sequence of integers such that\[\limsup \frac{a_n}{n}=\infty.\]Is\[\sum_{n=1}^\infty \frac{1}{2^{a_n}}\]transcendental?
- 题意摘要：量词为：对每个严格递增的正整数序列 $a_1<a_2<\cdots$，若 $\limsup_{n\to\infty}a_n/n=\infty$，是否必有 $\alpha=\sum_{n\ge1}2^{-a_n}$ 超越于 $\mathbb Q$？
- 状态核对：冻结状态及当前页面均为 open。先前候选正确判为开放，但其“更强条件意味着最终超过每个幂”的解释错误：对每个 $t$ 有 $\limsup a_n/n^t=\infty$ 只保证相应子序列无界，并非最终增长。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把 $\alpha$ 看成二进制展开中恰在位置 $a_n$ 出现数字 $1$ 的数。先用最终周期性排除有理数，再用截断 $P_N/2^{a_N}$ 尝试通过 Roth 型逼近排除代数无理数。
- 局部结论：可以严格证明 $\alpha$ 无理：若其二进制展开最终周期且含无限多个 $1$，则 $1$ 的计数具有正渐近密度；但在位置 $a_n$ 处该密度为 $n/a_n$，其下极限为 $0$。二进制双重表示的例外也不发生，因为序列中既有无限多个 $1$，又由该稀疏子序列保证并非最终全为 $1$。；截断满足 $0<\alpha-P_N/2^{a_N}\le2^{1-a_{N+1}}$。因此若存在 $\varepsilon>0$ 及无穷多个 $N$ 使 $a_{N+1}>(2+\varepsilon)a_N$，Roth 定理立即推出超越性。；原假设不蕴含这种乘法间隙；例如适当取整后的 $a_n\sim n\log n$ 满足 $a_n/n\to\infty$，但 $a_{n+1}/a_n\to1$。
- 第一阻塞点：第一处无法闭合的是从“计数函数沿某子序列密度趋零”推出足以违反代数数二进制复杂度或丢番图逼近下界的定量结构；原条件允许所有相邻间隙相对于 $a_n$ 都很小。
- 下一步：检验能否从 $\limsup a_n/n=\infty$ 推出二进制子词复杂度 $p(m)=O(m)$ 的某个无穷子序列；若能，再与代数无理数的复杂度下界对接。第一步应对 $a_n=\lceil n\log n\rceil$ 明算 $p(m)$，判断该路线是否已被反例序列否定。
- 来源核对：本地 Lean 文件核对了“对所有严格递增自然数序列”的量词。；[Erdős Problem 247](https://www.erdosproblems.com/247) 仍列为开放，并准确陈述 Erdős 的较强 limsup 条件。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/247)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/247.lean`；既有候选答案（按不可信材料审计）

### #249

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is\[\sum_n \frac{\phi(n)}{2^n}\]irrational? Here $\phi$ is the Euler totient function.
- 题意摘要：对象是单个收敛实数 $S=\sum_{n=1}^{\infty}\varphi(n)2^{-n}$，其中 $\varphi$ 为 Euler 函数；问题是 $S\notin\mathbb Q$ 是否成立。
- 状态核对：冻结状态及当前页面均为 open。先前候选只是状态汇总；数值展开不能作为无理性证据。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先把生成函数改写成 Möbius–Lambert 级数，并另行考察假设 $S=A/B$ 后，二进制尾项受到的整格约束。
- 局部结论：由 $\varphi(n)=n\sum_{d\mid n}\mu(d)/d$，绝对收敛允许换序，得到 $\sum_{n\ge1}\varphi(n)x^n=\sum_{d\ge1}\mu(d)x^d/(1-x^d)^2$；故 $S=\sum_{d\ge1}\mu(d)2^d/(2^d-1)^2$。；若 $S=A/B\in\mathbb Q$，令 $U_N=\sum_{j\ge1}\varphi(N+j)/2^j$，则 $B U_N\in\mathbb Z$ 对每个 $N$ 都成立，因为 $2^NS$ 与有限前缀之差恰为 $U_N$。；尾项满足精确递推 $U_{N+1}=2U_N-\varphi(N+1)$；但模 $1$ 后整数项消失，因此该递推本身不会产生矛盾。
- 第一阻塞点：第一处无法闭合的是证明 $U_N$ 不可能全部落在某个未知格点 $(1/B)\mathbb Z$。系数 $\varphi(n)>1$ 会发生进位，不能把该级数直接当作以 $\varphi(n)$ 为二进制数字的展开；Lambert 形式的公分母增长又远快于其指数尾误差。
- 下一步：对每个固定奇数 $B$，尝试寻找可证明的同余类 $N$ 使截断 $\sum_{j\le L}\varphi(N+j)/2^j$ 与 $(1/B)\mathbb Z$ 保持大于尾界的距离；先从 $B=1,3,5$ 和小 $L$ 做严格的有限同余覆盖测试。
- 来源核对：本地 Lean 陈述核对为单个实数的 `Irrational` 命题。；[Erdős Problem 249](https://www.erdosproblems.com/249) 仍标为开放。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/249)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/249.lean`；既有候选答案（按不可信材料审计）

### #251

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is\[\sum \frac{p_n}{2^n}\]irrational? (Here $p_n$ is the $n$th prime.)
- 题意摘要：令 $p_n$ 为第 $n$ 个素数（$p_1=2$），对象是 $S=\sum_{n=1}^{\infty}p_n/2^n$；问题是这个单个实数是否不属于 $\mathbb Q$。
- 状态核对：冻结状态及当前页面均为 open。先前候选正确报告状态，但没有进行证明尝试。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：假设 $S=A/B$，把每个二进制尾项放入固定格点，并将尾项改写为未来素数间隙的加权和，希望与素数间隙结构冲突。
- 局部结论：级数收敛，例如由 $p_n=O(n\log n)$ 得到绝对收敛。；设 $U_N=\sum_{j\ge1}p_{N+j}/2^j$。若 $S=A/B$，则 $BU_N\in\mathbb Z$ 对所有 $N$ 成立。；写 $g_m=p_m-p_{m-1}$，换序可得精确恒等式 $U_N=p_N+\sum_{i\ge1}g_{N+i}/2^{i-1}$；因此有理性会迫使所有未来素数间隙的加权和同时落在固定格点。截到长度 $L$ 的误差由素数定理界为 $O((N+L)\log(N+L)2^{-L})$。
- 第一阻塞点：第一处无法闭合的是从素数间隙的已知性质排除上述固定格点条件。除有限例外外间隙均为偶数，这反而与二进制分母相容；现有间隙结果没有控制足够长的连续间隙块以产生统一的模 $B2^L$ 矛盾。
- 下一步：把 $BU_N\in\mathbb Z$ 截断为关于 $(g_{N+1},\ldots,g_{N+L})$ 的模 $2^{L-1}$ 条件，明确列出有理性对每个 $L$ 强迫的剩余类；随后检查已知可实现的素数星座是否能对某个固定小 $L$ 排除全部奇数 $B$。
- 来源核对：本地 Lean 文件确认使用 `Nat.nth Nat.Prime`，仅有索引起点的形式差异。；[Erdős Problem 251](https://www.erdosproblems.com/251) 仍列为开放，并记录阶乘分母的已知对照结果。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/251)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/251.lean`；既有候选答案（按不可信材料审计）

### #252

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 1$ and $\sigma_k(n)=\sum_{d\mid n}d^k$. Is\[\sum \frac{\sigma_k(n)}{n!}\]irrational?
- 题意摘要：量词为：对每个整数 $k\ge1$，令 $\sigma_k(n)=\sum_{d\mid n}d^k$，问 $\alpha_k=\sum_{n=1}^{\infty}\sigma_k(n)/n!$ 是否无理。整个问题要求所有 $k$；并非固定一个未说明的 $k$。
- 状态核对：总命题仍 open，但 $k=1,2,3,4$ 已知成立，真正未决部分是所有 $k\ge5$。Schinzel 假设或素数元组/Dickson 型猜想可条件推出一般结论。先前候选对此总体判断正确。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：重建标准的阶乘清分母路线。反设 $\alpha_k=A/B$；对充分大的 $n$，$B\mid n!$，于是乘以 $n!$ 后，级数尾项必须是整数。再截掉可控的小尾巴，得到短除数函数表达式趋近整数。
- 局部结论：令 $T_n=\sum_{j\ge1}\sigma_k(n+j)/[(n+1)\cdots(n+j)]$。若 $\alpha_k\in\mathbb Q$，则对充分大 $n$ 有 $T_n\in\mathbb Z$。；对固定 $k\ge2$，由 $\sigma_k(m)\le\zeta(k)m^k$ 及阶乘分母估计，$\sum_{j\ge k+1}\sigma_k(n+j)/[(n+1)\cdots(n+j)]=O_k(1/n)$。因此有理性严格蕴含 $\left\|\sum_{j=1}^{k}\sigma_k(n+j)/[(n+1)\cdots(n+j)]\right\|=O_k(1/n)$。；这解释了已知证明为何选择使 $n+1,\ldots,n+k$ 具有特殊素因子结构的 $n$：若能算出上述短和的主分数部分并使其远离整数，即得矛盾。$k=4$ 的无条件实现需要筛法、光滑数分布和指数和，而非单纯尾估计。
- 第一阻塞点：第一处无法闭合的是：对一般 $k\ge5$，无法无条件构造无穷多个 $n$，使连续整数 $n+1,\ldots,n+k$ 的因子结构既可精确计算短和，又保证其分数部分与整数相隔 $\gg1$。这正是条件证明调用素数元组类猜想、而 $k=4$ 证明需要深筛法的环节。
- 下一步：选定首个未决情形 $k=5$，把短和按 $1/n$ 展开到常数项，明确列出对 $n+1,\ldots,n+5$ 所需的最小素因子模式；随后验证该模式是否等价于一个可容许的线性素数五元组，或是否能降为现有筛法可处理的“素数加几乎素数”条件。
- 来源核对：本地 Lean 文件分别标出 $k=1,2,3,4$ 已解决及 $k\ge5$ 开放。；[Erdős Problem 252](https://www.erdosproblems.com/252) 核对了无条件与条件结果。；[Pratt 的原论文](https://arxiv.org/abs/2209.11124) 明确证明 $k=4$，并将“有理性推出近整数性”作为证明起点。；[Friedlander–Luca–Stoiciu 论文记录](https://eudml.org/doc/128087) 核对了 $k=3$ 的无条件结果及更高 $k$ 的条件路线。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/252)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/252.lean`；既有候选答案（按不可信材料审计）

### #254

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be such that\[\lvert A\cap [1,2x]\rvert -\lvert A\cap [1,x]\rvert \to \infty\textrm{ as }x\to \infty\]and\[\sum_{n\in A} \{ \theta n\}=\infty\]for every $\theta\in (0,1)$, where $\{x\}$ is the distance of $x$ from the nearest integer. Then every sufficiently large integer is the sum of distinct elements of $A$.
- 题意摘要：对每个集合 A⊆ℕ，若 dyadic 壳层计数 |A∩[1,2x]|−|A∩[1,x]| 随 x→∞ 趋于∞，且对每个实数 0<θ<1 都有 ∑_{n∈A}‖θn‖=∞，则存在 M，使每个整数 m≥M 都是 A 中有限个互异元素之和。
- 状态核对：截至给定日期仍为开放题。Cassels 定理同时采用更强的壳层增长和更强的平方距离发散条件；不能直接套用。旧候选答案正确识别了傅里叶乘积的二次衰减，但提出的“非完备必产生绝对可和频率”只是未经证明的逆定理。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先从 θ=1/q 提取所有有限商中的局部完备性，再尝试由模 q 的覆盖升级为整数区间覆盖。对固定 q≥2、截断点 N，距离 ‖n/q‖在 n不被q整除时至少为1/q，故假设蕴含 A 中在 N 之后有无穷多个非 q 倍数。进而每条尾集 A∩[N,∞) 的元素在 ℤ/qℤ 中生成整个群。考察依次加入这些剩余类所得的子集和集合；若它最终稳定在真子集，其稳定子群将包含所有充分靠后的剩余类，与尾集生成整个群矛盾。因此某个有限尾子集的互异子集和已覆盖 ℤ/qℤ。
- 局部结论：对每个 q≥2，A 中有无穷多个不被 q 整除的元素。特别地，每个尾集的整数 gcd 都是1。；对任意 q≥2 和 N，存在有限集 F⊆A∩[N,∞)，使 F 的互异子集和覆盖 ℤ/qℤ 的全部剩余类。；第一条件单独蕴含 A 无限，并且每个充分大的 dyadic 壳层包含任意预先指定数目的 A 元素。
- 第一阻塞点：模每个 q 可覆盖并不提供子集和在实整数轴上的间隙控制；所选 F 的元素和可能远大于待表示整数。第一处缺口是：无法仅由无界壳层人数构造一个既覆盖所需模类、又把子集和填满一个长度超过下一尺度的连续区间的有限块。Cassels 的乘积估计在此使用 ∑‖θn‖² 发散；线性发散不能保证该平方和发散。
- 下一步：检验一个明确的有限块引理：若 B⊆(x,2x]、|B|=r 且所有模 q 的尾部生成条件成立，能否从 B 中抽取 C，使其子集和在某个模数 q 下覆盖全部剩余类，同时最大间隙为 o(x)；先对 q≤r 和具有受控加倍常数的壳层做计算实验或证明。
- 来源核对：核对了本地 254.lean：量词、distToNearestInt、最终对所有 m 的表述与原题一致，主定理仍为 sorry。；依据给定 Cassels 文献说明核对了条件方向：平方和发散比线性和发散更强。；未把旧候选中的傅里叶“逆定理”当作已有结论。
- 时间记账：所在批次墙钟时间按题数均摊约 79.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/254)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/254.lean`；既有候选答案（按不可信材料审计）

### #256

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n\geq 1$ and $f(n)$ be maximal such that for every $a_1\leq \cdots \leq a_n\in \mathbb{N}$ we have\[\max_{\lvert z\rvert=1}\left\lvert \prod_{i}(1-z^{a_i})\right\rvert\geq f(n).\]Estimate $f(n)$ - in particular, is it true that there exists some constant $c>0$ such that\[\log f(n) \gg n^c?\]
- 题意摘要：对每个 n，令 f(n) 为所有非降正整数 n 元组 a₁≤⋯≤aₙ 对应的 M(a)=max_{|z|=1}|∏_{i=1}^n(1−z^{a_i})| 的下确界；要求估计 f(n)，特别询问是否存在固定 c>0 使 log f(n)≫n^c。允许 a_i 重复。
- 状态核对：完整渐近估计仍开放，但特别问题已有否定答案：Belov–Konyagin 给出 log f(n)≪(log n)^4。旧候选提及的 2025 年预印本下界不在所给冻结状态资料中，且本次无法独立核验，因此不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：重建否定答案的逻辑归约。Belov–Konyagin 的非负整系数三角多项式构造应用于允许重数的指数多重集，给出某个 a₁≤⋯≤aₙ 满足 M(a)≤exp(C(log n)^4)，因而按 f 的下确界定义得到同一上界。另一方面，对任意固定 a，展开 P(z)=∏(1−z^{a_i})；其常数项和最高次项均为±1，Parseval 给出 max_{|z|=1}|P(z)|²≥∑|c_k|²≥2。结合已知 Erdős–Szekeres 定理可加强为 f(n)>√(2n)。
- 局部结论：严格按量词有 f(n)=inf_{a₁≤⋯≤aₙ} M(a)，而非对某个预定元组取最大值。；Parseval 的初等论证给出 f(n)≥√2；所给文献定理给出更强的 f(n)>√(2n)，故 log f(n)≥(1/2)log n+O(1)。；Belov–Konyagin 上界与 (log n)^4=o(n^c) 对每个固定 c>0 一起，严格否定 log f(n)≫n^c。
- 第一阻塞点：特别问题已经闭合；未闭合的是 f(n) 的真实增长阶。当前上下界之间仍有从约 log n 到 (log n)^4 的指数尺度鸿沟，而本路线没有给出改进 Belov–Konyagin 构造或 √n 下界的新机制。
- 下一步：把 Belov–Konyagin 的三角多项式定理逐项翻译成指数多重集，核对常数项、允许重复以及从其定理到 log f(n)≪(log n)^4 的参数对应；这是可独立审计的下一步。
- 来源核对：依据给定官方上下文核对了 Erdős–Szekeres、Atkinson、Odlyzko 与 Belov–Konyagin 的界。；特别结论只使用给定的 1996 上界，没有采用未核验的新预印本。
- 时间记账：所在批次墙钟时间按题数均摊约 79.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/256)；既有候选答案（按不可信材料审计）

### #257

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be an infinite set. Is\[\sum_{n\in A}\frac{1}{2^n-1}\]irrational?
- 题意摘要：量词是：对每个无限集合 A⊆ℕ，正项收敛级数 S_A=∑_{n∈A}(2^n−1)^{-1} 是否必为无理数。改变 A 的有限多个元素只给 S_A 加减有理数，故不影响无理性。
- 状态核对：一般情形仍开放；A=ℕ、两两互素且倒数和收敛的 A，以及给定资料中的素数/素数幂情形已有肯定结果。旧候选没有提供一般证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试分母最小公倍数反证。设 L_N=lcm{2^n−1:n∈A,n≤N}，并令 r_N=min(A∩(N,∞))。若 S_A=p/q，则 qL_N 乘以前 N 项为整数，而正尾项满足 ∑_{n∈A,n>N}1/(2^n−1)≤∑_{n≥r_N}2^{1−n}=2^{2−r_N}。因此若沿某子序列 L_N·2^{2−r_N}→0，则 0<qL_N·尾项<1，却又必须为整数，矛盾。
- 局部结论：Tonelli 定理严格给出 S_A=∑_{m≥1}f_A(m)/2^m，其中 f_A(m)=|{d∈A:d∣m}|。；删除或添加有限多个 A 元素不改变“是否无理”。；得到一个充分判据：若 liminf_N L_N2^{2−r_N}=0，则 S_A 无理。它适用于下一元素相对既有分母最小公倍数极稀疏的集合。
- 第一阻塞点：一般无限 A 完全不保证该充分判据：L_N 可能极快增长，而 r_N 可能仅为 N+1。第一处无法闭合的是寻找既让有限部分整除、又让尾部小于其倒数的截断点；Lambert 展开中的 f_A(m) 不是二进制数字，进位也阻止由“有理数最终周期”直接推出矛盾。
- 下一步：精确刻画充分判据覆盖的稀疏类：估计 log lcm_{n∈A,n≤N}(2^n−1)，并检查能否把阈值从 r_N≫log₂L_N 降到只依赖 A 的加性能量或整除重合度。
- 来源核对：核对了本地 257.lean：一般命题仍标为 research open，Lambert 恒等式和 A=ℕ 版本分别列为教材/已解决变体。；吸收给定官方上下文中的 2025 年素数与素数幂结果，但未将其外推到任意 A。
- 时间记账：所在批次墙钟时间按题数均摊约 79.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/257)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/257.lean`；既有候选答案（按不可信材料审计）

### #258

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $a_1,a_2,\ldots$ be a sequence of integers with $a_n\to \infty$. Is\[\sum_{n} \frac{\tau(n)}{a_1\cdots a_n}\]irrational, where $\tau(n)$ is the number of divisors of $n$?
- 题意摘要：按已形式化的无歧义版本：对每个自然数序列 a_n≥2 且 a_n→∞，令 Q_n=a₁⋯a_n，则 ∑_{n≥1}τ(n)/Q_n 为无理数；不要求单调。原文若允许任意整数且早期出现0，分母会无定义，故必须采用非零、通常 a_n≥2 的解释。
- 状态核对：给定状态已于 2026-04-21 更新为“proved (Lean)”。旧候选声称一般情形仍开放，现已过时。工作区文件引用 Chojecki–GPT-5.4 Pro 的 2026 证明和 ster-oc 的外部 Lean 形式化；但仓库中的封装定理本身以 sorry 占位，不能把该本地文件单独当作已编译证明证书。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：重建证明的尾项离散化框架。设 x=∑τ(n)/Q_n，并定义 R_N=Q_N(x−∑_{n≤N}τ(n)/Q_n)=∑_{j≥1}τ(N+j)/(a_{N+1}⋯a_{N+j})。若 x=u/v∈ℚ，则 vR_N=Q_Nu−v·整数，因此 vR_N∈ℤ；同时 R_N>0，且递推 a_NR_{N−1}=τ(N)+R_N。已解决证明的关键尾项引理断言：在 a_n→∞ 时可选 N_k 使 R_{N_k}→0。于是最终 0<vR_{N_k}<1，与其为整数矛盾。
- 局部结论：有理性假设把每个正规化尾项限制在固定格点 (1/v)ℤ，而不是仅给渐近周期性。；尾项满足精确递推 R_N=a_NR_{N−1}−τ(N)，这是证明中连接 Cantor 级数与除数函数的核心关系。；一旦建立 liminf_N R_N=0，无理性立即严格推出；单调性在这一最后步骤完全不需要。
- 第一阻塞点：若不调用 2026 年已证明的尾项引理，第一处实质难点是仅由 a_n→∞ 推出 liminf R_N=0：逐项粗界 τ(m)≤2√m 对增长极慢的 a_n 无效。此次环境无法联网取得并重新编译外部 Lean 文件，故这里只重建到该已知关键引理，未独立复现其完整证明。
- 下一步：取得引用的 ster-oc Lean 文件，在 mathlib v4.28.0 中无 sorry 编译，并定位证明 liminf R_N=0 的具体引理；随后逐行核对它是否只用 a_n≥2、Tendsto a atTop atTop，而未暗用单调性。
- 来源核对：读取了本地 258.lean：主定理明确为 answer(True)，假设 `∀n, 2≤a n` 与 `Tendsto a atTop atTop`，不含 Monotone。；同一文件把单调版本另列为 Erdős–Straus 变体，说明新主定理确实声称消除了单调性。；本地文件主证明仍写 `by sorry`，真正形式化证书位于其引用的外部 gist；网络受限，未能独立下载编译，因此降低置信度。
- 时间记账：所在批次墙钟时间按题数均摊约 79.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/258)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/258.lean`；既有候选答案（按不可信材料审计）

### #260

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1<a_2<\cdots$ be an increasing sequence such that $a_n/n\to \infty$. Is the sum\[\sum_n \frac{a_n}{2^{a_n}}\]irrational?
- 题意摘要：对每个严格递增正整数序列 a₁<a₂<⋯，若 a_n/n→∞，询问 x=∑_n a_n/2^{a_n} 是否必为无理数。等价地，令 ε_m=1_{m∈A}，其中 A={a_n} 且计数函数 A(t)=o(t)，研究 x=∑_{m≥1}mε_m2^{-m}。
- 状态核对：一般情形仍开放。已知在所有相邻间隙趋于∞或更强的定量增长条件下成立。旧候选仅复述状态，没有提供能处理平均稀疏性的证明。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试利用有理数二进制尾部的周期性。令 R_N=∑_{a_n>N}a_n2^{N−a_n}，则 2^Nx 与 R_N 相差整数，且若 N∉A，有 R_N=2R_{N−1}。若 x为有理数，其分数部分 {2^Nx} 最终周期，周期记 h。若某个长度至少 h 的 A-空区间内存在 N、N+h 且 0<R_N,R_{N+h}<1，则周期性给 R_{N+h}=R_N；空区间递推却给 R_{N+h}=2^hR_N，矛盾。
- 局部结论：a_n/n→∞ 等价于 A(t)=o(t)，并蕴含相邻间隙无界，即 limsup(a_{n+1}−a_n)=∞。；正规化尾项满足 R_N−2R_{N−1}=−Nε_N；在无 A 元素的区间上它精确倍增。；得到条件性无理判据：若存在任意长 A-空区间，其中相距固定 h 的两个正规化尾项都落在 (0,1)，则 x 不可能是分母奇数部分的二进制周期为 h 的有理数；dyadic 有理数甚至只需一个 0<R_N<1。
- 第一阻塞点：平均稀疏 A(t)=o(t) 只保证无界间隙，不保证间隙长于 log₂a，也不保证对应 R_N<1；远处许多项的进位可使 R_N很大。第一处缺口正是从 a_n/n→∞ 推出一个兼具“长空档”和“小正规化尾项”的位置。已知猜测连 limsup 间隙∞都可能不足，说明不能忽略该尾项条件。
- 下一步：针对 R_N 做可检验的平均估计：在每个区间 [a_k,a_{k+1}) 计算 min R_N，并检验附加条件 a_{k+1}−a_k≥(1+δ)log₂a_{k+1} 是否足以产生 R_N<1；若成立，可先得到介于已知定理与原猜想之间的严格子类。
- 来源核对：核对了本地 260.lean：量词为所有严格单调整数序列及其 HasSum，主定理仍为 research open/sorry。；本地文件明确把两个已知较强条件留作待补变体，与给定官方上下文一致。
- 时间记账：所在批次墙钟时间按题数均摊约 79.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/260)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/260.lean`；既有候选答案（按不可信材料审计）

### #261

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many $n$ such that there exists some $t\geq 2$ and distinct integers $a_1,\ldots,a_t\geq 1$ such that\[\frac{n}{2^n}=\sum_{1\leq k\leq t}\frac{a_k}{2^{a_k}}?\]Is this true for all $n$? Is there a rational $x$ such that\[x = \sum_{k=1}^\infty \frac{a_k}{2^{a_k}}\]has at least $2^{\aleph_0}$ solutions?
- 题意摘要：问题含三层量词：(i) 是否有无穷多个正整数 n，使存在 t≥2 及两两不同的正整数 a_1,…,a_t 满足 n/2^n=Σa_k/2^{a_k}；(ii) 是否每个 n 都如此；(iii) 是否存在有理数 x，具有至少连续统多个无穷表示。第三问按上下文应要求 a_k 两两不同（通常递增）；原句未再次明写这一点，若允许重复则是不同问题。
- 状态核对：第一问已知为“是”；全体 n 和连续统多表示仍开放。旧候选的有限恒等式正确，但“至少九个表示”等旁支没有在给定官方材料中核实，故不作为结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 f(r)=r/2^r。先验证分裂恒等式：若 N=2^{m+1}-m-2，则 f(N)=Σ_{j=1}^m f(N+j)。再尝试连续统构造：若某个有理 x 的一个表示中包含无穷多个支撑两两不交、且每个都可作上述等值替换的有限块，则对任意 I⊆ℕ独立选择替换块，立即得到 2^{aleph_0} 个表示。
- 局部结论：由 Σ_{j=1}^m2^{-j}=1-2^{-m} 和 Σ_{j=1}^m j2^{-j}=2-(m+2)2^{-m}，严格得到 Σ_{j=1}^m(N+j)/2^{N+j}=N/2^N 当且仅当 N=2^{m+1}-m-2。取 m≥2 给出无穷多个不同 N。；若存在无穷个互不干涉的二选一等值有限块，则从 P(ℕ) 到表示集的映射是单射；这一步确实给出连续统下界，而非仅可数多个表示。；该分裂总把指标推向右侧，因此有限次替换不会破坏正性或收敛性；支撑分离时也不会产生重复指标。
- 第一阻塞点：尚不能构造一个“总和恰为有理数”的初始无限支撑，同时保证其中含无穷多个独立分裂块。任取稀疏特殊指标 N_j 后，Σf(N_j) 的有理性没有理由成立；反复分裂单个有限表示又只保持有限支撑，不能自动产生无穷个独立选择点。
- 下一步：寻找特殊指标 N_j=2^{m_j+1}-m_j-2 的递归排列，使尾和 Σ_{j≥r}f(N_j) 本身等于某个有限块的权重；先对小 m_j 做精确有理搜索，检验能否形成支撑不交的自相似替换方程。
- 来源核对：[Erdős Problems #261](https://www.erdosproblems.com/261) 在 2025-12-01 更新后仍列为开放，并记录 Borwein–Loring 的无穷族及 n≤10000 的计算核验。
- 时间记账：所在批次墙钟时间按题数均摊约 60.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/261)；既有候选答案（按不可信材料审计）

### #263

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_n$ be a sequence of integers such that for every sequence of integers $b_n$ with $b_n/a_n\to 1$ the sum\[\sum\frac{1}{b_n}\]is irrational. Is $a_n=2^{2^n}$ such a sequence? Must such a sequence satisfy $a_n^{1/n}\to \infty$?
- 题意摘要：按当前修订版：a_n 是严格递增正整数序列；对每个正整数序列 b_n，只要 b_n/a_n→1，就要求 Σ1/b_n 收敛到无理数。问题问 a_n=2^{2^n} 是否具有此性质，以及每个这种递增序列是否必有 a_n^{1/n}→∞。输入的 exact_statement 漏掉了“正、严格递增”。
- 状态核对：修订后的两问仍开放。但按输入的字面陈述（不要求递增），第二问实际为假：可通过重排构造反例。本地 Lean 文件也把该非递增版本标为 false。旧候选没有吸收这一量词错误；另外把另一种性质称为逻辑上的“更强”也不严谨，两种允许的扰动类别并无直接包含关系。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先处理漏掉单调性的字面版本。取 A_m=2^{3^m}。若 d_m/A_m→1，则 d_m^{1/2^m}→∞，由经典快速收敛判据，Σ1/d_m 无理，故 A 是所需序列。将 A 用一个置换 π 重排成 a_n=A_{π(n)}，并让 π(n_j)=j、n_j远大于 log A_j。
- 局部结论：任意 ℕ 的置换及其逆都把趋于无穷的指标送到趋于无穷；故若 c_n/a_n→1，令 d_m=c_{π^{-1}(m)}，便有 d_m/A_m→1，而且 Σ1/c_n=Σ1/d_m。性质在重排下保持。；可选 n_j 使 log A_j/n_j→0，于是 a_{n_j}^{1/n_j}=exp(log A_j/n_j)→1；因此 a_n^{1/n} 不可能趋于∞。这严格否定无单调性版本的第二问。；对边界序列 2^{2^n}，原始分母满足 Π_{i=1}^N a_i=a_{N+1}/4；常规“部分分母乘积小于下一分母”的论证在这里恰好没有指数余量。
- 第一阻塞点：对 b_n∼2^{2^n}，乘积 Π_{i≤N}(b_i/a_i) 可因许多趋于1的误差累积而趋零、趋∞或振荡。因此从假设总和为有理数所得的整数性 q(Π_{i≤N}b_i)R_N∈ℤ，不能逼近一个固定的非整数常数；这正是边界法第一处失效。修订版第二问也不能使用重排反例，因为重排破坏严格递增。
- 下一步：针对边界序列先证明一个可检验的稳定性引理：在附加条件 Σ_{i≤N}|b_i/a_i-1|=O(1) 下分析 q(Πb_i)R_N 的极限并排除有理和；随后明确哪些步骤能否放宽到仅 b_n/a_n→1。
- 来源核对：[Erdős Problems #263](https://www.erdosproblems.com/263) 于 2026-04-02 明确补入“严格递增正整数”，并说明旧版因漏掉单调性已有反例。；[Koizumi 论文](https://arxiv.org/abs/2504.05933)研究相邻双指数序列；官网记录其“除可数多个 α 外”结果，但不解决 α=2。；本地 263.lean 未编码 StrictMono，且将第二问标记为 answer(False)，与上述旧版反例机制一致。
- 时间记账：所在批次墙钟时间按题数均摊约 60.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/263)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/263.lean`；既有候选答案（按不可信材料审计）

### #264

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_n$ be a sequence of integers such that for every bounded sequence of integers $b_n$ (with $a_n+b_n\neq 0$ and $b_n\neq 0$ for all $n$) the sum\[\sum \frac{1}{a_n+b_n}\]is irrational. Are $a_n=2^n$ or $a_n=n!$ examples of such a sequence?
- 题意摘要：给定正整数序列 a_n；量词遍历所有有界整数序列 b_n，并逐项要求 b_n≠0、a_n+b_n≠0；问 Σ1/(a_n+b_n) 是否总为无理数。分别判断 a_n=2^n 与 a_n=n!。
- 状态核对：2^n 已知不是例子；n! 仍开放。旧候选声称可取 b_n∈{1,…,5} 且总和恰为 3/4，但未给构造或可核来源，故不复述。另一本地 Lean 定义错误地取 b:ℕ→ℕ，遗漏负扰动，严格说没有完整形式化原题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：对 2^n 直接核验 Kovač–Tao 的否定判据。令 a_n=2^n，则 a_n^2Σ_{k>n}a_k^{-2}=4^nΣ_{k>n}4^{-k}=1/3，且 Σ1/a_n 收敛，所以判据产生某个合法有界整数扰动，使总和为有理数。对 n! 再检验同一判据是否适用。
- 局部结论：2^n 满足否定判据的 liminf=1/3>0，故确实存在有界、逐项非零的整数 b_n，使 Σ1/(2^n+b_n) 为有理数；这严格否定第一候选。；对 a_n=n!，有 (n!)²Σ_{k>n}1/(k!)²=(n+1)^{-2}(1+O(n^{-2}))→0，因此该否定定理恰好不提供信息。；固定扰动 b_n=-1 已把正面证明至少包含为特殊子问题：必须证明 Σ1/(n!-1) 无理；现有路线连这一特例也未闭合。
- 第一阻塞点：阶乘情形的尾平方质量趋零，Kovač–Tao 用概率/区间覆盖制造有理和的机制失去所需厚度；反方向上，部分和的公共分母 Π_{k≤N}(k!-1) 太大，普通有理逼近下界远弱于尾项约 1/(N+1)!，不能导出矛盾。
- 下一步：先研究 b_n=-1：计算并尝试证明 L_N=lcm(2!-1,…,N!-1) 的增长上界，使 L_N·Σ_{k>N}1/(k!-1)→0；若成功即可用有理部分和法解决这一特例，失败的位置也会量化所需的新算术信息。
- 来源核对：[Erdős Problems #264](https://www.erdosproblems.com/264) 于 2026-01-20 仍列 n! 为开放，并记录 Kovač–Tao 对 2^n 的否定定理。；[Kovač–Tao 原论文](https://arxiv.org/abs/2406.17593)的摘要确认其研究这两类 irrationality sequence。；本地 264.lean 的 b 类型为 ℕ→ℕ，与官网“bounded sequence of integers”不一致。
- 时间记账：所在批次墙钟时间按题数均摊约 60.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/264)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/264.lean`；既有候选答案（按不可信材料审计）

### #265

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：How fast can $a_n\to \infty$ grow if\[\sum\frac{1}{a_n}\quad\textrm{and}\quad\sum\frac{1}{a_n-1}\]are both rational?
- 题意摘要：现行陈述要求 1≤a_1<a_2<⋯ 为严格递增整数序列，并且 Σ1/a_n、Σ1/(a_n-1) 都收敛到有理数；问题寻求其最快可能增长率，特别是临界尺度 exp(C·2^n)。
- 状态核对：已有亚临界双指数构造：对某个 β>1，可有 a_n^{1/β^n}→∞。仍开放的是能否达到 limsup a_n^{1/2^n}>1。旧候选的“可以双指数增长”应按这一精确量词理解，不能解释成已达到 2^n 临界指数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先重建两个端点。下端验证 Cantor 的伸缩和；上端将 Kovač–Tao 对相邻移位 0、1 的构造平移：若 c_n 使 Σ1/c_n 与 Σ1/(c_n+1) 都有理，置 a_n=c_n+1 即得到题设的移位 0、-1，且渐近增长率不变。
- 局部结论：取 a_n=n(n-1)/2、n≥3，则 Σ1/a_n=1；又 1/(a_n-1)=2/((n-2)(n+1))=(2/3)(1/(n-2)-1/(n+1))，故第二和为 11/9。；Kovač–Tao 构造经 a_n=c_n+1 的平移，严格保留两和的有理性，并给出某个 β>1 下 log a_n/β^n→∞。；快速收敛判据只排除 lim a_n^{1/2^n}=∞；它没有排除有限的 limsup a_n^{1/2^n}>1，因此不能闭合临界问题。
- 第一阻塞点：现有构造的递归分枝/误差修正只保证某个低于临界的指数 β；将参数推到 2 时，必须同时保持整数选择、两个有理目标和尾误差可修正。现有结论没有给出足以保证 limsup(log a_n/2^n)>0 的参数余量。
- 下一步：把 Kovač–Tao 构造中每轮可选分母数、误差收缩率和最大分母写成显式递推，计算其允许的最大指数 β；首个判定任务是确认参数优化是否必然给 β<2，还是存在被粗估丢失的临界余量。
- 来源核对：[Erdős Problems #265](https://www.erdosproblems.com/265) 于 2026-01-21 仍把 limsup a_n^{1/2^n}>1 列为开放。；[Kovač–Tao 原论文](https://arxiv.org/abs/2406.17593)摘要明确给出同时控制 j=0,…,d-1 多个移位的双指数构造。
- 时间记账：所在批次墙钟时间按题数均摊约 60.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/265)；既有候选答案（按不可信材料审计）

### #267

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F_1=F_2=1$ and $F_{n+1}=F_n+F_{n-1}$ be the Fibonacci sequence. Let $n_1<n_2<\cdots $ be an infinite sequence with $n_{k+1}/n_k \geq c>1$. Must\[\sum_k\frac{1}{F_{n_k}}\]be irrational?
- 题意摘要：量词为：对任意严格递增正整数序列 n_1<n_2<⋯，若存在固定实数 c>1 使每个 k 都有 n_{k+1}/n_k≥c，是否必有 Σ_k1/F_{n_k} 无理。
- 状态核对：全题在 1<c<2 仍开放；Badea 已证明全部 c≥2。旧候选只给出 c>2 的超越性及 c=2 的个别例子，遗漏了 c=2 的一般已知定理。Nguyen 另证明 c>2 时甚至超越。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：尝试初等有理逼近法。令 S_N=Σ_{k≤N}1/F_{n_k}=A_N/Q_N，其中可取 Q_N=Π_{k≤N}F_{n_k}。若总和 S=p/q 为有理数，则正尾 R_N=S-S_N≥1/(qQ_N)。另一方面由 F_m≈φ^m 和比例间隔，R_N≪φ^{-n_{N+1}}。
- 局部结论：由 n_i≤n_N c^{-(N-i)} 得 Σ_{i≤N}n_i≤(c/(c-1)+o(1))n_N，故 log Q_N≤(logφ)(c/(c-1)+o(1))n_N。；而 n_{N+1}≥c n_N。当 c>2 时，c>c/(c-1)，所以 φ^{-n_{N+1}}=o(Q_N^{-1})，与 1/(qQ_N)≤R_N 矛盾；这给出 c>2 的完整初等无理性证明。；在 c=2 时两个主指数相等，乘积分母法没有余量；特殊序列 n_k=2^k 的和为 (7-√5)/2，说明临界值可以是代数无理数而非超越数。
- 第一阻塞点：当 1<c<2 时，c<c/(c-1)，上述上、下界方向反转，尾项并不足以小于通分所得的最小有理间距。这是该具体路线第一处无法闭合之处；仅改善常数无效，必须显著缩小实际公共分母。
- 下一步：利用 gcd(F_r,F_s)=F_{gcd(r,s)}，研究 L_N=lcm(F_{n_1},…,F_{n_N}) 而非乘积 Q_N；下一项明确任务是证明或否定在比例间隔假设下 log L_N≤(c-ε)n_N logφ。任何 ε>0 且上界低于 n_{N+1}/n_N 都会把无理性范围推进到某些 c<2。
- 来源核对：[Erdős Problems #267](https://www.erdosproblems.com/267) 于 2026-01-18 更新：Badea 覆盖 c≥2，剩余范围为 1<c<2。；[Nguyen 2020 原论文](https://arxiv.org/abs/2009.02446)证明 c>2 时该和超越，并指出阈值 2 对“超越”结论最优。；[Badea 1993 论文条目](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/63/4/107785/a-theorem-on-irrationality-of-infinite-series-and-applications)核对了原始论文的出版信息。
- 时间记账：所在批次墙钟时间按题数均摊约 60.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/267)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/267.lean`；既有候选答案（按不可信材料审计）

### #269

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $P$ be a finite set of primes with $\lvert P\rvert \geq 2$ and let $\{a_1<a_2<\cdots\}=\{ n\in \mathbb{N} : \textrm{if }p\mid n\textrm{ then }p\in P\}$. Is the sum\[\sum_{n=1}^\infty \frac{1}{[a_1,\ldots,a_n]},\]where $[a_1,\ldots,a_n]$ is the lowest common multiple of $a_1,\ldots,a_n$, irrational?
- 题意摘要：量词为：对每个有限素数集 $P$（$|P|\ge2$），将全部正的 $P$-光滑数递增排列为 $a_1<a_2<\cdots$，问实数 $S_P=\sum_{n\ge1}[a_1,\ldots,a_n]^{-1}$ 是否必为无理数。
- 状态核对：当前仍为开放题。旧候选关于收敛及 LCM 公式正确，但没有证明有限 $P$ 情形的无理性；“去掉重复项”的尾估计也不能直接用于原级数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：按 LCM 的跳跃点分块。令 $L_n=[a_1,\ldots,a_n]$。因 $a_1,\ldots,a_n$ 恰为不超过 $a_n$ 的全部 $P$-光滑数，故 $L_n=\prod_{p\in P}p^{\lfloor\log_p a_n\rfloor}$。因此 $L_n$ 只在 $a_n$ 是某个 $p^r$ 时改变；把相邻素数幂之间的重复次数记为 $c_j$，即可写成 $S_P=\sum_j c_j/M_j$，其中 $M_{j+1}/M_j\in P$。尝试假设 $S_P=u/v$，取 $j$ 使 $v\mid M_j$，再用清分母后的正尾项制造介于 $0$ 与 $1$ 之间的整数。
- 局部结论：严格有 $L_n=\prod_{p\in P}p^{\lfloor\log_p a_n\rfloor}$，且 LCM 的跳跃恰发生在所枚举的数为纯素数幂时。；级数绝对收敛：$L_n\ge a_n$，故 $S_P\le\sum_{m\ P\text{-光滑}}m^{-1}=\prod_{p\in P}(1-p^{-1})^{-1}<\infty$。；问题可精确归约为带重复系数的 Cantor 型级数 $\sum_j c_j/M_j$；去重版本对应全部 $c_j=1$，而原题的困难正是 $c_j$ 不受一致常数控制。
- 第一阻塞点：若 $S_P\in\mathbb Q$ 且 $v\mid M_j$，则需要证明清分母尾项 $M_j\sum_{r>j}c_r/M_r<1$（或得到其他非整数性判据）。现有估计只控制分母按素数倍增长，无法抵消区间内可能很大的重复次数 $c_r$；这是该路线第一处不能闭合之处。
- 下一步：对 $P=\{2,3\}$ 先证明或否定一个明确的块尾估计，例如研究 $T_j=M_j\sum_{r>j}c_r/M_r$ 的下极限、上极限及其是否可能落在整数上；这可通过格点计数 $\#\{(e,f):2^e3^f\in I_j\}$ 精确检验。
- 来源核对：[Erdős Problems #269](https://www.erdosproblems.com/269) 当前标为 OPEN，并记载无限 $P$ 与去重版本。；本地 FormalConjectures 文件的开放标签已核对；其级数定义存在索引偏移，但仅相差有理的初始项，不影响无理性问题。
- 时间记账：所在批次墙钟时间按题数均摊约 73.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/269)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/269.lean`；既有候选答案（按不可信材料审计）

### #271

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $n$, let $A(n)=\{0<n<\cdots\}$ be the infinite sequence with $a_0=0$ and $a_1=n$, and for $k\geq 1$ we define $a_{k+1}$ as the least integer such that there is no three-term arithmetic progression in $\{a_0,\ldots,a_{k+1}\}$. Can the $a_k$ be explicitly determined? How fast do they grow?
- 题意摘要：对每个固定正整数 $n$，从 $a_0=0,a_1=n$ 开始；每个 $k\ge1$ 取最小的整数 $a_{k+1}>a_k$，使已选集合仍不含三个不同元素组成的三项等差数列。问题要求一般性的显式描述，并确定 $a_k$ 随 $k$ 的增长。
- 状态核对：一般情形仍开放。$n=3^r$、$2\cdot3^r$ 有数字展开描述；普遍二次上界已知。旧候选中关于 2025 年数值预印本的额外断言不是本次筛查所需，也不能替代证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：采用贪心过程的“覆盖”计数。每个被跳过的整数 $x\in[n,a_k]$ 在当时必与两个更早选中项构成三项等差数列；因为此前项均小于 $x$，只能有 $x=2a_j-a_i$（$i<j$）。因此每个遗漏值可关联到一对已选项。另对 $n=1$ 尝试用三进制归纳：无数字 $2$ 的整数保持 3-free，而每个含数字 $2$ 的整数都被两个更小的无-$2$ 数覆盖。
- 局部结论：区间 $[n,a_k]$ 内有 $k$ 个已选项，遗漏项至多 $\binom{k}{2}$ 个，故 $a_k-n+1-k\le\binom{k}{2}$，即 $a_k\le n+\frac{(k-1)(k+2)}2$。；当 $n=1$ 时，若将 $k=\sum b_i2^i$ 的二进制数字原样解释为三进制，则 $a_k=\sum b_i3^i$；从而 $a_k=\Theta(k^{\log_2 3})$。；计数证明只使用每个遗漏值至少有一个表示 $2a_j-a_i$，因此适用于任意两项种子 $\{0,n\}$，但没有提供相应数量级的下界。
- 第一阻塞点：要从二次上界推进到 $k^{\log_2 3}$ 或 $k^2/\log k$ 的二分，需要控制映射 $(i,j)\mapsto2a_j-a_i$ 的碰撞数或证明结构性三进制自相似。一般 $n$ 下既无足够的碰撞下界，也无稳定数字结构；这正是第一处缺口。
- 下一步：针对 $n=4$，计算并严格统计前 $K$ 项中表示函数 $r(x)=\#\{(i,j):2a_j-a_i=x\}$ 的一、二阶矩，检验能否证明被覆盖整数数目至少为 $\gg k^2/\log k$；该命题若成立会给出相应增长上界。
- 来源核对：[Erdős Problems #271](https://www.erdosproblems.com/271) 当前仍标 OPEN，并给出显式二次界。；[Moy 论文摘要](https://arxiv.org/abs/1101.0022) 核对了普遍计数函数下界 $S(A,x)\ge(\sqrt2-\varepsilon)\sqrt x$。
- 时间记账：所在批次墙钟时间按题数均摊约 73.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/271)；既有候选答案（按不可信材料审计）

### #272

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $N\geq 1$. What is the largest $t$ such that there are $A_1,\ldots,A_t\subseteq \{1,\ldots,N\}$ with $A_i\cap A_j$ a non-empty arithmetic progression for all $i\neq j$?
- 题意摘要：对每个 $N\ge1$，在 $[N]=\{1,\ldots,N\}$ 的幂集中，求最大家庭 $\mathcal F$，使任意两个不同成员 $A,B$ 的交集都是非空的有限等差数列；长度 $1$、$2$ 也算等差数列。
- 状态核对：仍开放。旧候选把 Szabó 的下界 $\binom N2+\lfloor(N-1)/4\rfloor+1$ 错报为精确值；其“上界证明”中的关键收费引理没有证明，且官方资料明确只称其为构造下界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：审查旧候选中的局部替换构造。取 $q=\lfloor(N-1)/4\rfloor$、$m=2q+1$。从所有含 $m$ 且大小至多 $3$ 的集合开始；对每个 $1\le d\le q$，删除两个非等差三元组 $\{m-2d,m,m+d\}$、$\{m-d,m,m+2d\}$，加入以 $m$ 为中心附近、步长为 $d$ 的两个四项 AP 和一个五项 AP。逐类检查交集。
- 局部结论：基准星族 $\{A:m\in A,\ |A|\le3\}$ 合法，大小为 $1+(N-1)+\binom{N-1}{2}=\binom N2+1$。；上述每个 $d$ 删除两集、加入三集，且边界条件 $m-2d\ge1$、$m+2d\le N$ 成立。不同新增 AP 的交集仍是含 $m$ 的 AP；与保留三元组的交集若有三点，则被删掉的恰是两个非 AP 情形。因此该构造严格给出 $t(N)\ge\binom N2+\lfloor(N-1)/4\rfloor+1$。；已知上界只达到 $t(N)=N^2/2+O(N^{5/3}(\log N)^3)$；这与上述下界同主项，但不能推出线性误差，更不能推出精确公式。
- 第一阻塞点：要证明候选精确公式，必须把任意极值家庭归约为具有公共元素的星形家庭，并证明每加入一个大集合至少要按可注入方式删除足够多三元组。旧候选直接声称“每个步长净增至多 $1$”，既未处理没有公共点的家庭，也未给出跨步长的全局收费注入；第一处缺口就在这里。
- 下一步：先证明一个有限而明确的条件命题：若 $\bigcap\mathcal F$ 含某个 $m$，则是否有 $|\mathcal F|\le\binom N2+O(N)$；可把每个 $A\ni m$、$|A|\ge4$ 映射到其内部非 AP 三元组，建立二部图并检验 Hall 型收费不等式。
- 来源核对：[Erdős Problems #272](https://www.erdosproblems.com/272) 明确区分 Szabó 下界、已知误差项和仍开放的 $O(N)$ 猜想。；[Szabó 论文页面](https://www.sciencedirect.com/science/article/pii/S0195669897901761) 的摘要仅声称改进构造并解决渐近主项，不支持旧候选的精确公式。
- 时间记账：所在批次墙钟时间按题数均摊约 73.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/272)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/272.lean`；既有候选答案（按不可信材料审计）

### #273

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a covering system all of whose moduli are of the form $p-1$ for some primes $p\geq 5$?
- 题意摘要：按 Erdős–Graham 的严格覆盖系统口径，问是否存在有限个模数两两不同的同余类 $a_i\pmod{m_i}$ 覆盖全部整数，且每个 $m_i=p_i-1$，其中 $p_i\ge5$ 为素数。若不要求模数不同，四个模 $4$ 同余类会使问题平凡。
- 状态核对：当前仍开放。本地形式化定义 StrictCoveringSystem 明确要求模数映射单射，因此旧候选对“重复模数时平凡”的提醒正确，但没有提供开放版本的进展。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：利用所有允许模数均为偶数。按所选剩余类 $a_i$ 的奇偶性把覆盖分成两组。对固定 $\varepsilon\in\{0,1\}$，将整数写成 $2x+\varepsilon$；若 $a_i\equiv\varepsilon\pmod2$，则 $2x+\varepsilon\equiv a_i\pmod{p_i-1}$ 等价于 $x\equiv(a_i-\varepsilon)/2\pmod{(p_i-1)/2}$。于是原问题归约为用两组互不重复的“安全素数前驱半模数”分别覆盖 $\mathbb Z$。
- 局部结论：奇剩余类和偶剩余类各自除以 $2$ 后都必须单独覆盖全体整数；不能只在总体上满足密度条件。；若 $I_0,I_1$ 是两组指标，则必要条件为 $\sum_{i\in I_\varepsilon}2/(p_i-1)\ge1$；因此总体必须满足 $\sum_i1/(p_i-1)\ge1$。；任何有限候选都以 $L=\operatorname{lcm}(p_i-1)$ 为周期，存在性可精确转化为有限循环群 $\mathbb Z/L\mathbb Z$ 上的集合覆盖问题。
- 第一阻塞点：密度不等式只是必要条件；即使两组倒数和都超过 $1$，仍须选择剩余类使所有周期点被覆盖。当前没有定理保证受限模数 $(p-1)/2$ 能形成两套覆盖，也没有从奇偶分裂推出矛盾。
- 下一步：按素数上界 $B$ 建立可复核的 SAT/整数规划：变量表示每个允许模数选择哪个剩余类，约束模数至多使用一次且覆盖 $\mathbb Z/L\mathbb Z$；先分别求两种奇偶组，再合并。无解证书可揭示需要证明的有限阻碍模式。
- 来源核对：[Erdős Problems #273](https://www.erdosproblems.com/273) 当前标为 OPEN，并记载允许 $p=3$ 时 Selfridge 的结果。；本地 CoveringSystem.lean 已核对：StrictCoveringSystem 的 injective_moduli 明确排除重复模数。
- 时间记账：所在批次墙钟时间按题数均摊约 73.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/273)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/273.lean`；既有候选答案（按不可信材料审计）

### #274

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G$ is a group then can there exist an exact covering of $G$ by more than one cosets of different sizes? (i.e. each element is contained in exactly one of the cosets)
- 题意摘要：标准 Herzog–Schönheim 口径为：是否存在群 $G$、$k>1$ 个左陪集 $a_iH_i$，恰好分割 $G$，同时有限指标 $[G:H_i]$ 两两不同？在有限群中这等价于陪集大小两两不同。
- 状态核对：一般情形仍开放；所有 $H_i$ 次正规的情形（特别是阿贝尔群）已否定，且阶小于 $1440$ 的群已核验。人工评审指出旧候选忽略“指标两两不同”，该错误成立：其 $\mathbb Z_{12}$ 例子使用两个同为指标 $4$ 的子群陪集，不能反驳猜想；单点拆分也大量重复指标。另需注意：本地 erdos_274 主定理用子群基数两两不同，而 herzog_schonheim 定理用指标两两不同；对无限群二者并不等价。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试将有限指标反例压缩到有限商。设 $N=\bigcap_i\operatorname{core}_G(H_i)$。每个 core 都是有限指标正规子群，故 $N$ 亦为有限指标正规子群且 $N\le H_i$。每个 $a_iH_i$ 是若干 $N$-陪集的并，故原分割下降为有限群 $G/N$ 的陪集分割，并保持全部指标。随后使用分割的密度恒等式限制可能指标。
- 局部结论：任何采用有限指标子群的反例都会给出一个有限群反例：$a_iH_i$ 在 $G/N$ 中变为 $(a_iN)(H_i/N)$，且 $[G/N:H_i/N]=[G:H_i]$。；有限反例的指标 $n_i=[G:H_i]\ge2$ 必满足埃及分数恒等式 $\sum_i1/n_i=1$。若 $k=2$，唯一可能是 $n_1=n_2=2$，故两两不同指标的反例至少有三个分片。；结合已知小群结果，任何有限商反例的阶至少为 $1440$；若所有相关子群次正规，则 Sun 的定理还保证最大指标必须重复。
- 第一阻塞点：埃及分数条件不编码陪集的实际相交结构；例如 $(2,3,6)$ 数值上满足倒数和为 $1$，却不能据此构造分割。要继续必须从群作用或群代数恒等式 $\sum_i1_{a_iH_i}=1_G$ 中推出某个指标重复；一般非次正规子群下，现有谱/表示论论证无法完成这一提取。
- 下一步：以最小可能阶 $1440$ 为起点，把有限反例进一步归约到 core-free 数据，并枚举满足 $\sum1/n_i=1$、各 $n_i\mid1440$ 且两两不同的指标组；随后逐组检查相应传递置换表示能否容纳不交陪集。这比搜索任意陪集分割更小且可验证。
- 来源核对：[Erdős Problems #274](https://www.erdosproblems.com/274) 当前标为 OPEN，并列出次正规及小群结果。；[Sun 2004 论文页面](https://www.sciencedirect.com/science/article/pii/S002186930300526X) 明确陈述指标为有限指标，并证明次正规子群情形最大指标有重复。；本地 FormalConjectures 已核对到“基数版本”与“指标版本”在无限群上的形式化口径差异。
- 时间记账：所在批次墙钟时间按题数均摊约 73.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/274)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/274.lean`；既有候选答案（按不可信材料审计）

### #276

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an infinite Lucas sequence $a_0,a_1,\ldots$ where $a_{n+2}=a_{n+1}+a_n$ for $n\geq 0$ such that all $a_k$ are composite, and yet no integer has a common factor with every term of the sequence?
- 题意摘要：求是否存在函数 a:ℕ→ℕ，使得对每个 n，a_{n+2}=a_{n+1}+a_n；每个 a_n 都是合数；并且对每个整数 m>1，都存在 k 使 gcd(m,a_k)=1。“公因子”必须理解为大于 1 的公因子。
- 状态核对：截至当前官方记录仍为开放。Graham 已构造全合数序列，但由有限覆盖系统保证；Ismailescu–Son 给出候选序列，却未证明题目要求的无有限素数覆盖性质。旧候选答案对此状态判断基本正确，但不能把“看不出覆盖系统”当成证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把最后一个量词改写为有限素数覆盖问题。令 Z_p={n:p∣a_n}。题目要求所有 n 均属于某个 Z_p，同时对任意有限素数集 S，都有 ℕ⊄⋃_{p∈S}Z_p。再利用递推矩阵 [[1,1],[1,0]] 在模 p 下可逆，研究各 Z_p 的周期结构。
- 局部结论：“∀m>1，∃k，gcd(m,a_k)=1”等价于“对任意有限素数集 S，存在 k 使所有 p∈S 都不整除 a_k”；取 m=∏_{p∈S}p 即得两个方向。；gcd(a_n,a_{n+1})=gcd(a_0,a_1) 对所有 n 成立，因为 gcd(a_{n+1},a_{n+2})=gcd(a_{n+1},a_n)。因此若初值互素，没有单个素数能整除两个相邻项。；对每个素数 p，状态 (a_n,a_{n+1}) mod p 从初始时刻起纯周期，故 Z_p 是周期集合。问题因此归约为：能否构造由这些特殊周期集合形成的可数覆盖，但不存在有限子覆盖。
- 第一阻塞点：即使每个 Z_p 周期且不含相邻指标，也无法推出有限个 Z_p 的并不覆盖 ℕ；不同素数的零点周期可能互补。对 Ismailescu–Son 候选，恰缺少“任给有限 S，可找到一个奇指标项避开 S”的严格证明。
- 下一步：对该显式候选建立奇数项两个因子的模 p 周期表；给定有限 S，用 CRT 搜索同时避开所有零点类，并检验能否证明每个新增素数都不能消灭全部剩余类。这是可证伪、也可能产生有限覆盖证书的任务。
- 来源核对：[Erdős Problem #276](https://www.erdosproblems.com/276) 当前仍标为 OPEN，并明确说候选例子尚未排除有限覆盖。；本地 Lean 陈述已核对：其最后条件正是 ∀m>1,∃k,gcd(m,a_k)=1，而非只要求不存在一个共同素因子。
- 时间记账：所在批次墙钟时间按题数均摊约 59.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/276)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/276.lean`；既有候选答案（按不可信材料审计）

### #278

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{n_1<\cdots<n_r\}$ be a finite set of integers. What is the maximum density of integers covered by a suitable choice of congruences $a_i\pmod{n_i}$? Is the minimum density achieved when all the $a_i$ are equal?
- 题意摘要：固定有限且互异的正整数模数 A={n_1<⋯<n_r}。对每个 i 独立选择剩余类 a_i mod n_i，求并集 ⋃_i(a_i+n_iℤ) 的最大自然密度；另问最小密度是否在所有 a_i 来自同一整数时取得。
- 状态核对：最大值的一般结构仍开放；最小值问题已由 Simpson 的结果肯定解决。旧候选给出的“素数幂模数公式”等额外断言不是解决一般最大值所需，本次不依赖它。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：令 L=lcm(n_1,…,n_r)，把问题化为有限集合 ℤ/Lℤ 上的覆盖优化。对每个非空 I，用广义 CRT 判定相应剩余类交集是否为空，再作精确容斥。
- 局部结论：密度恒为 |{x mod L:∃i,x≡a_i mod n_i}|/L，因此最大值确实存在，并可由有限搜索计算；开放之处是关于任意 A 的有效结构公式，而非单个输入不可计算。；对非空 I，交集非空当且仅当 a_i≡a_j mod gcd(n_i,n_j) 对所有 i,j∈I；非空时其密度恰为 1/lcm(n_i:i∈I)。所以目标函数是这些 CRT 相容性指示量的有限容斥和。；当 r=2 时可完全求解：若 gcd(n_1,n_2)=1，密度与剩余类无关，等于 1/n_1+1/n_2−1/(n_1n_2)；若 gcd(n_1,n_2)>1，可选不相容剩余类使两类不交，最大值为 1/n_1+1/n_2。
- 第一阻塞点：r≥3 时，高阶交集的容斥符号交替；局部消灭一个两两交集可能同时改变许多三重及更高交集。因此不能把最大化简化成逐对选择“不相容”，也尚无一般方法描述所有最优 CRT 相容模式。
- 下一步：先处理“模数整除图为森林”这一可检验子类：枚举边上的相容/不相容条件，证明高阶相容性是否由树边决定，再用动态规划精确优化容斥和。失败时会给出最小环状反例。
- 来源核对：[Erdős Problem #278](https://www.erdosproblems.com/278) 当前把最大值列为开放，并记录 Simpson 已解决最小值问题。；最小值的精确值为所有剩余类对齐时的容斥式 ∑_{∅≠I}(-1)^{|I|+1}/lcm(n_i:i∈I)；本次未冒充重新证明 Simpson 的一般不等式。
- 时间记账：所在批次墙钟时间按题数均摊约 59.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/278)；既有候选答案（按不可信材料审计）

### #279

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$. Is there a choice of congruence classes $a_p\pmod{p}$ for every prime $p$ such that all except finitely many integers can be written as $a_p+tp$ for some prime $p$ and integer $t\geq k$?
- 题意摘要：量词为：对每个固定 k≥3，是否存在一组同时为所有素数指定的代表元 0≤a_p<p，以及 N，使每个 n≥N 都存在素数 p 和整数 t≥k，满足 n=a_p+tp。a_p 可依赖 k，但不能依赖 n。
- 状态核对：截至当前仍开放，甚至 k=3 未知。旧候选有一处重要错误：它声称 k=2 时已知“除有限个整数外全部覆盖”；当前官方备注只断言在弱化为“几乎所有整数”后，对任意 k≥2 和倒数和发散的模数集成立。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：随机且独立地令每个 a_p 在 ℤ/pℤ 上均匀分布。对固定 n，只有 p≤n/k 可能给出 t≥k；计算 n 未被这些素数覆盖的概率，再考察能否用概率法升级为最终全覆盖。
- 局部结论：若 p≤n/k 且 a_p≡n mod p，则以标准代表元 a_p∈[0,p−1] 有 n=a_p+p⌊n/p⌋，且 ⌊n/p⌋≥k。反之 p>n/k 不可能满足 n=a_p+tp、t≥k。；因此固定 n 未覆盖的概率精确为 ∏_{p≤n/k}(1−1/p)，由 Mertens 乘积估计为 O(1/log n)。；于是任意大区间 [X,2X] 上未覆盖数的期望为 O(X/log X)，故对每个该区间至少存在一组有限素数剩余类达到同样量级的例外数。这真实解释了“几乎覆盖”为何可行。
- 第一阻塞点：O(1/log n) 的单点失败概率不可求和，第一 Borel–Cantelli 引理不能推出只有有限多个失败；而分别优化各区间得到的剩余类选择也未必相容。这里正是从零密度例外升级到有限例外的首个缺口。
- 下一步：固定 k=3 和有限区间 [X,2X]，把未覆盖事件写成关于变量 a_p 的约束系统，计算其依赖图并检验 Lovász 局部引理或重抽样算法的条件；重点测量大素数导致的低度约束能否清除随机筛剩下的 O(X/log X) 个整数。
- 来源核对：[Erdős Problem #279](https://www.erdosproblems.com/279) 当前仍为 OPEN，并明确区分题设的“all sufficiently large”与已知弱化版“almost all”。；本地 Lean 陈述已核对为 ∀k≥3,∃a,∃N,∀n≥N,∃p,t≥k；它正确保留了统一选择 a 和有限例外量词。
- 时间记账：所在批次墙钟时间按题数均摊约 59.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/279)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/279.lean`；既有候选答案（按不可信材料审计）

### #281

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $n_1<n_2<\cdots$ be an infinite sequence such that, for any choice of congruence classes $a_i\pmod{n_i}$, the set of integers not satisfying any of the congruences $a_i\pmod{n_i}$ has density $0$. Is it true that for every $\epsilon>0$ there exists some $k$ such that, for every choice of congruence classes $a_i$, the density of integers not satisfying any of the congruences $a_i\pmod{n_i}$ for $1\leq i\leq k$ is less than $\epsilon$?
- 题意摘要：设严格递增 n_i。假设对每个无限剩余类序列 a=(a_i)，避开全部 a_i mod n_i 的整数集合都有自然密度 0。要证明：对每个 ε>0，存在只依赖 ε 的 k，使对所有 a，避开前 k 个类的密度均小于 ε。核心是把对 a 的逐点收敛升级为一致收敛。
- 状态核对：该题现已肯定解决并有 Lean 核验。候选中的 profinite–Dini 证明经独立检查可闭合；另有 Davenport–Erdős 与 Rogers 定理给出的较短已知路线。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：在 X=∏_iℤ/n_iℤ 上令 d_k(a) 为避开前 k 个类的密度。把有限周期集合解释为 profinite completion ℤ̂ 中 clopen 集 C_k(a) 的 Haar 测度；先证明 d_k(a)↓0，再用 Dini 定理取得一致收敛。
- 局部结论：有限阶段有 d_k(a)=μ(C_k(a))，且由测度从上连续性，lim_k d_k(a)=μ(C(a))。；若某个 C(a) 有正 Haar 测度 δ，则 ℤ̂ 上的平移 x↦x+1 是遍历的；取 Birkhoff 泛型点 x，并令 b_i≡a_i−x mod n_i，便得到整数轨道在 C(b) 中的自然密度 δ>0，违反对所有 b 的假设。因此 μ(C(a))=0。；每个 d_k 只依赖前 k 个有限坐标，故在紧空间 X 上连续；又 d_k 单调降至连续函数 0。Dini 定理给出 sup_a d_k(a)→0，正是所求量词。
- 第一阻塞点：无未闭合步骤。需要引用的标准事实是 ℤ̂ 上加一变换的遍历性、Birkhoff 遍历定理和 Dini 定理；它们的适用条件均满足。
- 下一步：若要进一步形式化或降低依赖，可改走官方记录的初等路线：对零剩余类应用 Davenport–Erdős 密度极限定理，再用 Rogers 定理说明有限系统的未覆盖密度在全部剩余类为零时最大。
- 来源核对：[Erdős Problem #281](https://www.erdosproblems.com/281) 标为 PROVED (LEAN)，并给出 Davenport–Erdős/Rogers 证明摘要。；人工核验过的候选证明中，关键平移恒等式 C(b)=C(a)−x 与自然密度的轨道解释方向正确，没有把整数点密度直接无条件等同于任意闭集的 Haar 测度。
- 时间记账：所在批次墙钟时间按题数均摊约 59.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/281)；既有候选答案（按不可信材料审计）

### #282

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be an infinite set and consider the following greedy algorithm for a rational $x\in (0,1)$: choose the minimal $n\in A$ such that $n\geq 1/x$ and repeat with $x$ replaced by $x-\frac{1}{n}$. If this terminates after finitely many steps then this produces a representation of $x$ as the sum of distinct unit fractions with denominators from $A$. Does this process always terminate if $x$ has odd denominator and $A$ is the set of odd numbers? More generally, for which pairs $x$ and $A$ does this process terminate?
- 题意摘要：给定无限 A⊆ℕ 和有理数 0<x<1，每步取满足 n∈A、n≥1/x 的最小 n，再以 x←x−1/n 迭代。主问题是 A 为全体奇数且 x 的既约分母为奇数时是否必在有限步到达 0；一般问题要求刻画终止的 (x,A)。
- 状态核对：奇分母情形仍开放。旧候选正确地区分了“存在某个有限奇单位分数表示”和“该贪心过程终止”，但它没有注意到题面所称“产生互异分母”对这一算法定义并不总成立。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：设当前余项为既约 a/b>0，b 为奇数，令 n 为不小于 b/a 的最小奇数。考察新余项 (an−b)/(bn)，尝试以既约分子作为递降势函数，并检查分母是否必严格增加。
- 局部结论：由 n−2<b/a≤n 得 0≤an−b<2a。因此新余项的未约分分子小于旧分子的两倍；若 n恰为通常的 ceiling，则更强地有 an−b<a，这就是普通 Fibonacci 贪心终止证明。；当 ceiling(b/a) 为偶数时必须多跳一步到下一个奇数，分子只得到 <2a 而非严格下降；例如 x=4/5 时首步取 n=3，新分子从 4 增至 7。；题面关于互异分母的附带断言按字面是假的：4/5→7/15→2/15 的前两步都选择 n=3，故 1/3 被重复使用。终止问题本身仍有定义，但不能以“分母严格递增”作为证明前提。
- 第一阻塞点：找不到在“跳过偶数 ceiling”的步骤也严格下降的整数势函数；分子可增长，分母也可短暂重复。存在有限奇分母表示并不能控制这条确定性贪心轨道。
- 下一步：枚举既约状态 (a,b) 并按 q=⌈b/a⌉ 的奇偶分类，检验二步或三步势函数，例如 log a−c log b 或按 q 加权的字典序量；首要目标是寻找最小反例，或证明每次分子增长后在有界步数内下降到原值以下。
- 来源核对：[Erdős Problem #282](https://www.erdosproblems.com/282) 当前仍为 OPEN，并区分表示存在性与贪心终止问题。；本地 Lean 定义同样不会删除已经使用的分母，因此 4/5 的重复 n=3 现象也适用于该形式化定义；“对应互异单位分数表示”的注释需要修正或补充去重规则。
- 时间记账：所在批次墙钟时间按题数均摊约 59.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/282)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/282.lean`；既有候选答案（按不可信材料审计）

### #283

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $p:\mathbb{Z}\to \mathbb{Z}$ be a polynomial whose leading coefficient is positive and such that there exists no $d\geq 2$ with $d\mid p(n)$ for all $n\geq 1$. Is it true that, for all sufficiently large $m$, there exist integers $1\leq n_1<\cdots <n_k$ such that\[1=\frac{1}{n_1}+\cdots+\frac{1}{n_k}\]and\[m=p(n_1)+\cdots+p(n_k)?\]
- 题意摘要：对每个整系数多项式 p，若首项系数正且 gcd{p(n):n≥1}=1，则存在 M=M(p)，使每个整数 m≥M 都能写成 m=Σp(n_i)，其中 1≤n_1<⋯<n_k 且 Σ1/n_i=1。
- 状态核对：截至 2026-05-10，官方已改列“PROVED (LEAN)”。先前候选称一般情形开放，现已过时。当前工作区的 283.lean 仍含 sorry，只是旧形式化陈述；完整外部证明约 1.1 万行，并以 Roth–Szekeres–Graham 完备序列定理为核心。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建局部切换证明。取 u_j=36j+1、D_j=u_ju_{j+1}。恒等式 1/D_j=1/(2D_j)+1/(3D_j)+1/(6D_j) 允许在不改变倒数和的前提下，把 p-和增加 q(j)=p(2D_j)+p(3D_j)+p(6D_j)-p(D_j)。再用完备多项式序列定理，以互异 q(j) 之和填满某固定模数类中的所有充分大差额；有限多个基准埃及分数负责覆盖其余模类。
- 局部结论：若 deg p=d、首项系数 c>0，则 q(j) 是次数 2d 的整系数多项式，首项系数为 c·36^{2d}(2^d+3^d+6^d−1)>0。；望远镜恒等式 Σ_{j<J}1/D_j+1/(36u_J)=1/36 严格成立；它提供可任意延长的、彼此不同的基准分母骨架。；对任意被选中的 j 作上述切换，倒数总和保持不变，而 p-和恰增加 q(j)；因此问题归约为互异多项式值的完全性及有限模类拼接。
- 第一阻塞点：本次受限重建未逐行复核完整 Lean 文件中“为每个剩余模类构造避开 0,1,2,3,6 mod 36 的基准分母集”及所有切换分母不碰撞的技术部分。讨论摘要还把尾分母 36u_J 的 p-贡献误写成 p(u_J)，不能直接当作证明；正式证明必须使用 p(36u_J)。这属于本次审计边界，不是已登记证明中的已知缺口。
- 下一步：检出完整 Proof_flat.lean 中基准模类引理、分母互异引理及最终定理的依赖闭包；用无 sorry/额外公理检查器重新编译，并比对其最终量词与原题完全一致。
- 来源核对：[官方题页：已列 PROVED (LEAN)，并说明更强的任意正有理数版本](https://www.erdosproblems.com/283)；[官方讨论：给出切换多项式、完备序列路线及形式化说明](https://www.erdosproblems.com/forum/thread/283)；[外部 Lean 文件 Proof_flat.lean](https://github.com/Shashi456/erdos-formalizations/blob/main/Erdos/P283/Proof_flat.lean)；本地 FormalConjectures/ErdosProblems/283.lean 的主定理和 Graham 变体均仍为 sorry，故它本身不能支持“Lean 已证明”。
- 时间记账：所在批次墙钟时间按题数均摊约 47.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/283)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/283.lean`；既有候选答案（按不可信材料审计）

### #288

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that there are only finitely many pairs of intervals $I_1,I_2$ such that\[\sum_{n_1\in I_1}\frac{1}{n_1}+\sum_{n_2\in I_2}\frac{1}{n_2}\in \mathbb{N}?\]
- 题意摘要：问满足 S(I_1)+S(I_2)∈N 的正整数有限区间有序对是否只有有限多个，其中 S([a,b])=Σ_{n=a}^b1/n；题面没有要求两区间互异或不相交。甚至 I_2 为单点的子问题仍问有限性。
- 状态核对：官方仍列开放。先前候选只报告状态和小范围搜索，没有构成证明；其列出的含 [1,1] 的平凡对也不能说明渐近有限性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用 p-adic“唯一最大估值项”排除法。对两区间中的所有分母按重数合并；若某素数 p 的最大 v_p(n) 只由一个倒数项取得，则通分后该项在模 p 下非零，其余项全为零，故总和不可能是整数。
- 局部结论：任何解都满足：对每个 p，所有出现分母中达到最大 p-adic 阶的项至少出现两次；重叠区间中的同一分母须按两次计数。；在单点版本 I_2={b} 中，若 I_1 内恰有一个 n 满足 v_p(n)=e=max_{m∈I_1}v_p(m)，且 v_p(b)≠e 或存在更高阶但仍唯一的项，则不可能为解。；单区间长度大于 1 时，Kürschák 的 2-adic论证正是该准则的特例：区间中存在唯一具有最高 2-adic 阶的分母，故其调和和不为整数。
- 第一阻塞点：要推出全局有限性，必须对任意足够远的区间 I_1 找到足够多“唯一最高阶”的素数幂，迫使单点 b 同时满足互相冲突的估值条件。现有初等素数分布结论不足以在所有区间长度和位置上统一保证这种素数幂；这是该路线第一处无法闭合之处。
- 下一步：先对单点版本证明一个可检验的有限范围引理：若 I=[a,c] 含某 p^e 的唯一倍数且 c< p^{e+1}，精确列出 b 必须满足的 v_p(b) 条件；随后计算多个此类 p^e 所给条件的交集，检验能否导出 b 的指数级下界。
- 来源核对：[官方题页：开放，且 |I_2|=1 仍开放](https://www.erdosproblems.com/288)；本地 Lean 文件忠实使用正整数闭区间；主定理仍为 sorry，未提供证明。
- 时间记账：所在批次墙钟时间按题数均摊约 47.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/288)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/288.lean`；既有候选答案（按不可信材料审计）

### #289

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for all sufficiently large $k$, there exist finite intervals $I_1,\ldots,I_k\subset \mathbb{N}$, distinct, not overlapping or adjacent, with $\lvert I_i\rvert \geq 2$ for $1\leq i\leq k$ such that\[1=\sum_{i=1}^k \sum_{n\in I_i}\frac{1}{n}?\]
- 题意摘要：要求存在 K，使每个 k≥K 都有恰好 k 个有限正整数区间；每区间至少含两个整数，任意两区间互异、无交叠且不相邻，并且所有区间内倒数之和恰为 1。
- 状态核对：官方仍列开放。先前候选正确区分了无几何限制的容易版本与当前版本，但没有证明尝试。另有形式化偏差：本地 Lean 条件 b_i<a_j 只保证不重叠，仍允许 b_i+1=a_j 的相邻区间，弱于原题。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试建立可迭代的局部替换：寻找参数化恒等式 S([a,b])=S([c,d])+S([e,f])，其中两个新区间各长至少 2、彼此及旧区间均隔至少一个整数。若这种替换能在任意大尺度反复使用，则从一个种子解可把区间数逐次增加。
- 局部结论：任一解都不含分母 1，否则其余正项使总和大于 1。；写区间按位置排序为 [a_i,b_i]，原题的非相邻条件应为 b_i+1<a_{i+1}，而不是仅 b_i<a_{i+1}。；与 288 相同：对任意素数 p，达到所有所用分母中最大 v_p 的倒数项不能唯一；这给任何候选替换恒等式一个快速、严格的局部否定检验。
- 第一阻塞点：调和区间和 H_b−H_{a−1} 不具缩放不变性；普通埃及分数分裂 1/n=1/(n+1)+1/(n(n+1)) 产生单点而非长度至少 2 的连续块。尚未找到一个满足全部间隔条件、并可无限迭代的参数化区间替换恒等式。
- 下一步：做精确有理数搜索，固定较小长度 2≤|I|≤L，寻找 S(I)=S(J_1)+S(J_2) 的参数族；先用上述 p-adic准则剪枝，再检验所得恒等式能否嵌入官方给出的五区间种子或其他和为 1 的种子。
- 来源核对：[官方题页：当前强化版本开放，并说明无这些限制时容易](https://www.erdosproblems.com/289)；本地 289.lean 的区间分离公式允许相邻区间，因此不能视为原题的精确形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 47.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/289)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/289.lean`；既有候选答案（按不可信材料审计）

### #291

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n\geq 1$ and define $L_n$ to be the least common multiple of $\{1,\ldots,n\}$ and $a_n$ by\[\sum_{1\leq k\leq n}\frac{1}{k}=\frac{a_n}{L_n}.\]Is it true that $(a_n,L_n)=1$ and $(a_n,L_n)>1$ both occur for infinitely many $n$?
- 题意摘要：令 L_n=lcm(1,…,n)，并以未约分形式 H_n=a_n/L_n 定义整数 a_n。问题包含两个无限性断言：gcd(a_n,L_n)=1 是否无穷多次出现，以及 gcd(a_n,L_n)>1 是否无穷多次出现。
- 状态核对：第二个断言已有初等证明；第一个仍开放，所以合取问题仍列开放。先前候选的主要结论正确，但“p−1 情形需 Wolstenholme”并不必要，模 p 下求逆置换即可。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：固定素数 p≤n，令 p^e≤n<p^{e+1}，写 n=kp^e+r，其中 1≤k≤p−1。将 a_n=Σ_{j≤n}L_n/j 模 p 化简：除 j=tp^e（1≤t≤k）外全部项消失。
- 局部结论：严格得到 a_n≡(L_n/p^e)Σ_{t=1}^k t^{-1} (mod p)，且 L_n/p^e 是模 p 单位。因此 p|gcd(a_n,L_n) 当且仅当 Σ_{t=1}^k1/t 的分子被 p 整除。；取 p=3、k=2，有 1+1/2=3/2；故每个 2·3^e≤n<3^{e+1} 都满足 3|gcd(a_n,L_n)，从而 gcd>1 无穷多次出现。；若 H_n=u_n/v_n 为既约分数，则 v_n=L_n/gcd(a_n,L_n)；所以 gcd=1 等价于调和数的既约分母恰为 L_n。
- 第一阻塞点：要证明 gcd=1 无穷多，需要同时避开所有 p≤n 的坏首位数字条件。不同素数的首位由 {log_p n} 控制，既非独立同余条件，也无法用有限 CRT 同时处理；现有约 x/log x 的独立性启发不能给出无条件下界。
- 下一步：对有限素数集 P 严格估计同时避开坏区间的 n 的测度，再量化加入 p>y 的误差；关键可检验目标是证明大素数造成 p|a_n 的事件总贡献为 o(x)，或明确找出该估计失败的规模。
- 来源核对：[官方题页：给出素数判据、显式无限族及剩余开放部分](https://www.erdosproblems.com/291)；官方页仍列整体问题 OPEN；条件密度结果不等于无条件证明 gcd=1 无穷多。
- 时间记账：所在批次墙钟时间按题数均摊约 47.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/291)；既有候选答案（按不可信材料审计）

### #293

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 1$ and let $v(k)$ be the minimal integer which does not appear as some $n_i$ in a solution to\[1=\frac{1}{n_1}+\cdots+\frac{1}{n_k}\]with $1\leq n_1<\cdots <n_k$. Estimate the growth of $v(k)$.
- 题意摘要：按题面字面，v(k) 是没有在任何“恰含 k 个互异分母”的 1 的埃及分数分解中出现的最小正整数。真正被研究的版本显然应把最小值限制为整数 ≥2。
- 状态核对：题面存在致命定义遗漏：k≥2 时分母 1 不可能出现，因此字面上 v(k)=1；k=1 时唯一分解为 1=1/1，故 v(1)=2。这样不存在所述增长问题。官方给出的 e^{ck²} 下界只能对应修正版 v(k)=min{m≥2:m 不出现}。先前候选虽自行采用修正版，却错误地把“恰好 k 项”改述为“至多 k 项”，并给出格式损坏的上界公式。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先审查定义，再对修正版重建标准上界。对任意 k 项分解，将分母递增排列；用贪心余量估计迭代控制每个 n_i，得到最大分母 n_k≤k u_k，其中 u_1=1、u_{i+1}=u_i(u_i+1)。因此大于该界的整数不可能出现。
- 局部结论：字面版本完全确定：v(1)=2，而所有 k≥2 有 v(k)=1。；修正版中，每个可能出现的分母都不超过 k u_k，故 v(k)≤k u_k+1；又 u_k=c_0^{2^k+o(2^k)}，于是 v(k)≤exp(O(2^k))。；结合已记录的 van Doorn–Tang 结果，修正版目前有 exp(ck²)≤v(k)≤exp(C2^k)；下界意味着每个 2≤m<exp(ck²) 都出现在某个恰好 k 项的分解中，不能擅自改成“至多 k 项”。
- 第一阻塞点：初等余量递推只约束任何单个分解的最大分母，不能证明大量较小整数都实际出现；把下界从 exp(ck²) 推到双指数需要对指定分母 m 构造恰好 k 项分解的统一方法，而现有路线在控制项数与分母互异性时停止。
- 下一步：首先正式修订定义为 m≥2，并核对 2025 论文始终使用“恰好 k 项”。随后针对给定 m，写出论文构造增加项数的基本变换，逐项验证它保持分母 m、互异性及精确项数，以定位 exp(ck²) 下界中可改进的瓶颈。
- 来源核对：[官方题页同时给出原字面定义、exp(ck²) 下界和双指数上界](https://www.erdosproblems.com/293)；三者合看即暴露了缺少“m≥2”的定义问题。；[官方 LaTeX 源同样写 1≤n_1，却未在 v(k) 的最小值中排除 1](https://www.erdosproblems.com/latex/293)；官方当前仍将修正意图下的增长估计列为 OPEN。
- 时间记账：所在批次墙钟时间按题数均摊约 47.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/293)；既有候选答案（按不可信材料审计）

### #295

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $N\geq 1$ and let $k(N)$ denote the smallest $k$ such that there exist $N\leq n_1<\cdots <n_k$ with\[1=\frac{1}{n_1}+\cdots+\frac{1}{n_k}.\]Is it true that\[\lim_{N\to \infty} k(N)-(e-1)N=\infty?\]
- 题意摘要：对每个整数 N≥1，k(N) 是把 1 表成互异单位分数之和、且所有分母均至少为 N 时所需的最少项数。问题问实数序列 k(N)−(e−1)N 是否趋于 +∞。
- 状态核对：冻结状态为 open；官方条目仍只记录 −c<k(N)−(e−1)N≪N/log N。先前候选正确说明了主项来源，但没有推进所问的发散。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：取给定项数 k 时可能达到的最大和，即连续最小分母的调和块 S_N(k)=∑_{j=0}^{k−1}1/(N+j)。任何表示都满足 1≤S_N(k)。再用 Euler–Maclaurin 精确检查该必要条件能否产生增长余项。
- 局部结论：严格地，若存在 k 项表示，则 1≤H_{N+k−1}−H_{N−1}，故 k(N) 至少是使该调和块达到 1 的最小整数 r_N。；当 k=(e−1)N+c 且 c=O(1) 时，S_N(k)=1+[c/e+(e−1)/(2e)]/N+O(N⁻²)，因此 r_N=(e−1)N+O(1)。；这说明仅利用“分母互异且 ≥N”的大小排序，至多给出常数量级余项；所求发散必须利用单位分数等式的算术稀疏性。
- 第一阻塞点：从 S_N(k)≥1 只能推出 k≥(e−1)N−O(1)；无法证明靠近连续分母极值的调和质量不能被某组非连续分母恰好拼成 1。
- 下一步：固定小整数 C，研究 k≤⌊(e−1)N⌋+C 时方程 ∑1/n_i=1 的模素数障碍；先计算若干 N 的候选表示，并检验是否存在一个随 N 增长的“必须新增分母数”参数。
- 来源核对：[官方条目](https://www.erdosproblems.com/295)确认题面、开放状态及 Erdős–Straus 界。；本地 Lean 文件把 k 定义为 Fin (k+1) 的 Nat.find，存在“项数减一”的偏移；该偏移不影响趋于 +∞ 的真假，但定义并非逐字对应原题。
- 时间记账：所在批次墙钟时间按题数均摊约 47.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/295)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/295.lean`；既有候选答案（按不可信材料审计）

### #301

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be the size of the largest $A\subseteq \{1,\ldots,N\}$ such that there are no solutions to\[\frac{1}{a}\neq \frac{1}{b_1}+\cdots+\frac{1}{b_k}\]with distinct $a,b_1,\ldots,b_k\in A$? Estimate $f(N)$. In particular, is $f(N)=(\tfrac{1}{2}+o(1))N$?
- 题意摘要：输入中的“≠”是转录错误；官方题面为等号。f(N) 是最大 |A|，其中 A⊆{1,…,N}，且不存在某个 k≥1 及两两不同的 a,b₁,…,b_k∈A 满足 1/a=∑1/b_i；k=1 因互异性自动不可能。
- 状态核对：整体最优渐近仍 open。先前候选的结论范围与官方记录相符，但其上界只作了概述；这里独立重建五元块论证。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：采用 S_x={2x,3x,4x,6x,12x}，其中 x=8^u9^v d、(d,6)=1。先验证块内禁式，再用 2-adic、3-adic 赋值证明各块不交并计数。
- 局部结论：块内有 1/(2x)=1/(3x)+1/(6x)、1/(3x)=1/(4x)+1/(12x) 及 1/(2x)=1/(4x)+1/(6x)+1/(12x)。逐一检查删去哪一个元素可知：完整五元块至少遗漏两个元素；当 N/12<x≤N/6 时至少遗漏一个。；乘数 2,3,4,6,12 的 (v₂ mod 3,v₃ mod 2) 两两不同，所以表示 x=8^u9^v d 使这些块两两不交。；此类 x≤X 的数量为 (3/7+o(1))X。因此总遗漏数至少 (3/7)(N/6+N/12)+o(N)=3N/28+o(N)，重得 f(N)≤(25/28+o(1))N。
- 第一阻塞点：这些局部恒等式只强制遗漏密度 3/28；没有理由表明任意密度超过 1/2 的集合会在某个五元块或其有限扩张中触发禁式。
- 下一步：枚举较小乘数集合 T，建立其单位分数关系超图，并计算分数覆盖数；只保留能用 p-adic 剩余类铺成不交缩放块且给出超过 3/28 遗漏密度的候选。
- 来源核对：[官方条目](https://www.erdosproblems.com/301)明确使用等号，并记录五元块及 25/28 上界。；输入先前候选中对题面“笔误”的修正是必要的；若按字面“无解于 ≠”，问题会变成完全不同且近乎退化的命题。
- 时间记账：所在批次墙钟时间按题数均摊约 47.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/301)；既有候选答案（按不可信材料审计）

### #302

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be the size of the largest $A\subseteq \{1,\ldots,N\}$ such that there are no solutions to\[\frac{1}{a}= \frac{1}{b}+\frac{1}{c}\]with distinct $a,b,c\in A$? Estimate $f(N)$. In particular, is $f(N)=(\tfrac{1}{2}+o(1))N$?
- 题意摘要：f(N) 是最大 |A|，其中 A⊆{1,…,N}，且不存在两两不同的 a,b,c∈A 满足 1/a=1/b+1/c。题目要求估计 f(N)，并特别询问其是否为 (1/2+o(1))N。
- 状态核对：整体精确估计仍 open；但“是否为 1/2”这一子问已被已知的 5/8 构造否定。人工评审指出先前候选只是重述已知结果，因此不能把该构造包装成开放题的新解。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：独立核验构造 A={奇数 n≤N/4}∪([N/2,N]∩ℕ)，使用分解恒等式 (b−a)(c−a)=a²、奇偶性及端点估计排除所有三元组。
- 局部结论：由 (b−a)(c−a)=a² 可知 b,c>a；若 b,c≤N，则 a≤N/2。；若 a 是构造中的小奇数，且 b 或 c 也是小奇数，则 b−a 或 c−a 为偶数，与右端 a² 为奇数矛盾。因此 b,c 都必须属于上半区。；上半区中不同的 b,c 满足 1/b+1/c<4/N，故 a>N/4，与 a≤N/4 矛盾。于是该 A 无解，且 |A|=(5/8+o(1))N。
- 第一阻塞点：论证只给出构造性下界；奇偶性依赖于特定分层集合，不能约束任意高密度 A，因此无法接近已知 9/10 上界，更不能确定真实常数。
- 下一步：利用完整参数化 b=a+d、c=a+a²/d（d∣a²）建立有限模数上的三元超图；优化由若干区间和剩余类组成的周期构造，检验能否严格超过 5/8。
- 来源核对：[官方条目](https://www.erdosproblems.com/302)记录 5/8 构造和 9/10 上界。；已吸收人工评审：5/8 是官网已知观察，只解决“1/2 是否正确”这一子问，并未解决整体估计问题。
- 时间记账：所在批次墙钟时间按题数均摊约 47.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/302)；既有候选答案（按不可信材料审计）

### #304

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For integers $1\leq a<b$ let $N(a,b)$ denote the minimal $k$ such that there exist integers $1<n_1<\cdots<n_k$ with\[\frac{a}{b}=\frac{1}{n_1}+\cdots+\frac{1}{n_k}.\]Estimate $N(b)=\max_{1\leq a<b}N(a,b)$. Is it true that $N(b) \ll \log\log b$?
- 题意摘要：对每个 1≤a<b，N(a,b) 是将 a/b 表为互异单位分数 1/n_i（1<n₁<⋯<n_k）之和所需的最少项数；N(b)=max_{1≤a<b}N(a,b)。问题问是否存在绝对常数 C，使充分大的 b 均满足 N(b)≤C log log b。
- 状态核对：冻结状态为 open；已知 log log b≪N(b)≪√log b。先前候选提出约数和归约，但把它与 Vose 证明直接关联并未给出来源或证明，故这里只保留可严格验证的归约本身。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：选取 b 的倍数 M，并把候选分母限制为 M/d，其中 d 是 M 的互异真约数。原单位分数问题随即化为一个稀疏的互异约数子集和问题。
- 局部结论：对任意 D⊆{d:d∣M,d<M}，有 a/b=∑_{d∈D}1/(M/d) 当且仅当 aM/b=∑_{d∈D}d；分母互异等价于 d 互异。；因此若能对每个 1≤a<b 选择某个 M≡0 mod b，使 aM/b 是至多 C log log b 个互异真约数之和，就会推出所猜上界。；a=1 时 N(1,b)=1；困难来自要求对所有分子、尤其最坏分子，取得与 b 仅双对数相关的稀疏度。
- 第一阻塞点：“M 有很多且稠密的约数”并不蕴含每个目标 aM/b 都有 O(log log b) 项的互异约数表示；目前缺少这一均匀稀疏子集和引理。
- 下一步：对 b≤B 选择结构化倍数 M=b·lcm(1,…,y)，用精确子集和算法测量所有目标 aM/b 的最少约数项数；检查最大值是否随 log log b 增长，并识别失败目标的同余特征。
- 来源核对：[官方条目](https://www.erdosproblems.com/304)确认 Erdős 下界、Vose 的 √log b 上界及开放状态。；本地 Lean 版本用 Finset 表达互异分母，与有序列表在数学上等价；但文件本身也注明尚未证明可表示集合总是非空。
- 时间记账：所在批次墙钟时间按题数均摊约 47.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/304)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/304.lean`；既有候选答案（按不可信材料审计）

### #306

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a/b\in \mathbb{Q}_{>0}$ with $b$ squarefree. Are there integers $1<n_1<\cdots<n_k$, each the product of two distinct primes, such that\[\frac{a}{b}=\frac{1}{n_1}+\cdots+\frac{1}{n_k}?\]
- 题意摘要：对每个正有理数 q=a/b（应先约分），若约分后的分母 b 无平方因子，是否存在有限个严格递增分母 n_i=p_iq_i，其中 p_i、q_i 是不同素数，使 q=∑1/n_i？量词覆盖所有正有理数，而非仅 b=1。
- 状态核对：冻结状态为 open。先前候选给出的必要条件正确，但其中具体 48 项例子未作独立核验且与证明普遍命题无关，故不采用。官网目前仍标 open；评论区出现 claimed solution 不能视为已审定结果。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `medium`
- 尝试路线：把每个分母 pq 看成素数图的一条边。令 L 为所有出现素数的乘积，并研究和式分子 X=∑_{pq∈E}L/(pq) 在各素数模下的消去条件。
- 局部结论：所有 n_i 均平方自由，故其最小公倍数 L 平方自由；约分后和式的分母整除 L，因此平方自由。这严格证明题设条件的必要性。；对顶点素数 r，有 X≡(L/r)∑_{s:rs∈E}s⁻¹ (mod r)。所以 r 在约分时消去，当且仅当邻点倒数和模 r 为 0。；若辅助素数 r 不整除目标约分分母，则 r 不能是叶子：叶子时邻点倒数模 r 非零。因而任何构造都必须把辅助素数组织成满足局部模消去条件的度数至少为 2 的图。
- 第一阻塞点：局部模条件没有同时控制分数和的精确大小与正性；目前无法构造一个有限简单图，使所有辅助素数恰好消去、b 中素数恰好保留，并令最终分子等于指定的 a。
- 下一步：先固定一个小平方自由 b，搜索最小素数图 E：对 r∤b 强制 ∑s⁻¹≡0 mod r，对 r∣b 强制非零，再检查精确等式。优先测试这些同余条件是否已排除大量候选或产生可复用的循环 gadget。
- 来源核对：[官方条目](https://www.erdosproblems.com/306)确认开放状态，并仅记录三素因子、b=1 的已知定理。；本地 Lean 形式化以 ω(n)=Ω(n)=2 表示恰为两个不同素数的乘积，并用 n(0)=1 作为哨兵；实际求和从索引 1 开始，与原题含义一致。
- 时间记账：所在批次墙钟时间按题数均摊约 47.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/306)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/306.lean`；既有候选答案（按不可信材料审计）

### #311

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the minimal value of $\lvert 1-\sum_{n\in A}\frac{1}{n}\rvert$ as $A$ ranges over all subsets of $\{1,\ldots,N\}$ which contain no $S$ such that $\sum_{n\in S}\frac{1}{n}=1$? Is it\[e^{-(c+o(1))N}\]for some constant $c\in (0,1)$?
- 题意摘要：令原题约束量为 Δ(N)=min{|1-∑_{n∈A}1/n|：A⊆{1,…,N}，且 A 不含任何 S⊆A 满足 ∑_{n∈S}1/n=1}。问题问是否存在固定 c∈(0,1)，使 Δ(N)=exp(-(c+o(1))N)。官方现采用无约束的最小非零误差 δ(N)，并称两种表述等价。
- 状态核对：截至官方页 2026-01-16 更新仍为 open。候选答案直接把两量定义为“相同”不够严谨；应先证明在误差 <1/N 后极小集自动满足原约束。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：走最小公倍数格点与两表述归约。设 L_N=lcm(1,…,N)。任一子集和为整数/L_N。若无约束极小集 A 含有和为 1 的子集 S，则因误差非零，S⊊A，且 |∑_{A}1/n-1|=∑_{A∖S}1/n≥1/N。因此一旦已知 δ(N)<1/N，无约束极小集便是原题允许的集合，故 Δ(N)=δ(N)。Tang 的已知上界足以保证大 N 时这一条件成立。
- 局部结论：严格下界 Δ(N)≥1/L_N=exp(-(1+o(1))N)。；若 δ(N)<1/N，则原约束量与无约束最小非零误差严格相等，而不只是渐近同阶。；已知 δ(N)≤exp(-cN/(log N·loglog N)^3)，故上述等价对充分大 N 成立。
- 第一阻塞点：格点论证只给指数常数 1 的下界；现有构造的上界指数为 -N/polylog(N)，无法推出固定正指数率，更无法证明极限 -log Δ(N)/N 存在并位于 (0,1)。
- 下一步：可检验任务：研究近似乘法或拼接不等式，例如能否对误差极小集证明 Δ(N+M)≤exp(o(N+M))Δ(N)Δ(M)，并用计算先检验 -log Δ(N) 是否呈近似超可加性。
- 来源核对：[官方 #311](https://www.erdosproblems.com/311) 核对了 open 状态、两表述等价说明、LCM 下界及 Tang 上界。；候选答案中“含 proper S 的误差≥1/N”正确，但遗漏了必须先取得 δ(N)<1/N 才能据此证明极小值相同。
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/311)；既有候选答案（按不可信材料审计）

### #312

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does there exist some $c>0$ such that, for any $K>1$, whenever $A$ is a sufficiently large finite multiset of integers with $\sum_{n\in A}\frac{1}{n}>K$ there exists some $S\subseteq A$ such that\[1-e^{-cK} < \sum_{n\in S}\frac{1}{n}\leq 1?\]
- 题意摘要：所求量词是 ∃c>0，∀K>1，∃N₀(K)，使任意基数 n≥N₀ 的正整数有限多重集 A，只要 ∑_{a∈A}1/a>K，就存在子多重集 S，满足 1-e^{-cK}<∑_{a∈S}1/a≤1。这里“充分大”指多重集基数，且阈值可依赖 K。
- 状态核对：截至官方页 2026-01-20 更新仍为 open；已知 Erdős–Graham 版本只保证亏损 O(K^{-2})。本地 Lean 陈述与上述量词一致。候选把结论改写为 ε(A)≤e^{-cR(A)} 并不逐字等价，因为 N₀ 依赖所选 K，不能无条件令 K=R(A)。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试贪心装箱：依次处理各倒数，只要加入后不超过 1 就加入，得到极大子多重集 S，记亏损 r=1-∑_{S}1/a。每个未选项在被拒时均大于当时余量，因余量随后只减小，故最终每个未选倒数都大于 r。试图由剩余总质量>K-1 迫使 r 指数小。
- 局部结论：贪心所得 S 总满足 0≤∑_{S}1/a≤1。；若 r>0，则每个未选项满足 1/a>r，等价于 a<1/r。；由于已选质量≤1，全部未选项的倒数总和>K-1。
- 第一阻塞点：“未选项都大于 r”与“未选总质量>K-1”不能控制 r：多重集允许同一分母任意多次出现，未选项个数没有上界。需要交换论证或多子集和碰撞来利用基数，而单一贪心极大性不足。
- 下一步：可检验任务：固定一个分母尺度 [x,2x)，对该层的多重集建立定量交换引理——若该层总倒数质量为 T，能否构造不超过 1 且亏损 ≤exp(-cT) 的子多重集；先对所有分母相同的模型完整求出最优亏损。
- 来源核对：[官方 #312](https://www.erdosproblems.com/312) 核对了正整数、多重集、open 状态及 O(K^{-2}) 已知结果。；本地 312.lean 明确形式化为 ∀K∃N₀∀n≥N₀，确认候选的 R(A) 改写存在量词缺口。
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/312)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/312.lean`；既有候选答案（按不可信材料审计）

### #313

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many solutions to\[\frac{1}{p_1}+\cdots+\frac{1}{p_k}=1-\frac{1}{m},\]where $m\geq 2$ is an integer and $p_1<\cdots<p_k$ are distinct primes?
- 题意摘要：问满足 m≥2、p₁<⋯<p_k 为互异素数且 ∑ᵢ1/pᵢ=1-1/m 的整数—素数集对是否有无限多个；等价地问 primary pseudoperfect numbers 是否无限。
- 状态核对：截至官方当前记录仍为 open，已知八个。候选答案关于 m=∏pᵢ 的证明可以修复为严格论证，但它只完成归约，不解决无限性。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先作模素数归约，再尝试递推生成。令 P=∏pᵢ。乘以 mP 得 m∑P/pᵢ=(m-1)P，故 m|P。若某 p_j∤m，把 ∑m/pᵢ=m-1 中 pᵢ|m 的整数项移走；对其余素数乘 Q=∏_{pᵢ∤m}pᵢ，再模 p_j，只有 j 项不消失，矛盾。因此 P|m，遂 m=P。进一步，若 M 已满足 1/M+∑_{p|M}1/p=1 且 q=M+1 为素数，则 N=Mq 也满足该恒等式。
- 局部结论：任何解必有 m=∏ᵢpᵢ，因而 m 平方自由，且每个 m 至多对应一个素数集。；问题严格等价于平方自由整数 m 满足 1/m+∑_{p|m}1/p=1 是否有无限多个。；递推引理：若 M 是 primary pseudoperfect 且 M+1 为素数，则 M(M+1) 仍是 primary pseudoperfect；代入后新增的 1/(M(M+1))+1/(M+1) 恰为 1/M。
- 第一阻塞点：递推要求 M+1 为素数，不能证明可无限迭代；实际经典链在 M=1806 后即因 1807 合数而停止。现无机制保证从任意已知解产生更大的新解。
- 下一步：可检验任务：系统求解更一般的扩张条件 N=Mq₁⋯q_r，把所需恒等式化为 ∑1/q_i+1/(M∏q_i)=1/M，并先分类 r=2 时可能的素数对。
- 来源核对：[官方 #313](https://www.erdosproblems.com/313) 核对了 open 状态、m=素数乘积归约及八个已知数。；本地 313.lean 将解定义为 (m,P) 的无限集合，并另列 primary pseudoperfect numbers 无限性；两者借唯一性归约一致。
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/313)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/313.lean`；既有候选答案（按不可信材料审计）

### #317

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some constant $c>0$ such that for every $n\geq 1$ there exists some $\delta_k\in \{-1,0,1\}$ for $1\leq k\leq n$ with\[0< \left\lvert \sum_{1\leq k\leq n}\frac{\delta_k}{k}\right\rvert < \frac{c}{2^n}?\]Is it true that for sufficiently large $n$, for any $\delta_k\in \{-1,0,1\}$,\[\left\lvert \sum_{1\leq k\leq n}\frac{\delta_k}{k}\right\rvert > \frac{1}{[1,\ldots,n]}\]whenever the left-hand side is not zero?
- 题意摘要：第一问：是否存在统一 c>0，使每个 n≥1 都有 δ₁,…,δ_n∈{-1,0,1}，其非零调和线性组合绝对值小于 c2^{-n}。第二问：是否存在 n₀，使所有 n≥n₀、所有这类系数的非零组合都严格大于 1/L_n，其中 L_n=lcm(1,…,n)。
- 状态核对：两问仍 open。官方记录弱上界 2^{-n(logloglog n)^{1+o(1)}/log n}；严格下界在小 n 失败。候选的非严格 LCM 论证正确。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：第一问采用可严格验证的素数子集和碰撞。取 P_n={p素数:n/2<p≤n}。这些素数倒数的 2^{|P_n|} 个子集和互异：若两和相等，乘所有 p 的乘积并模一个仅出现在一侧的 p 即矛盾。将这些数排序，在长度至多 ∑_{p∈P_n}1/p<1 的区间中，两相邻值之差至多 1/(2^{|P_n|}-1)，其差给出 {-1,0,1} 系数。第二问则乘 L_n，把问题化成整数方程 ∑δ_kL_n/k=±1 是否最终无解。
- 局部结论：对所有充分大 n，存在非零组合满足 |∑δ_k/k|≤1/(2^{π(n)-π(n/2)}-1)=exp(-Θ(n/log n))。；任一非零组合均为非零整数除以 L_n，故绝对值≥1/L_n；等号恰当且仅当 ∑δ_kL_n/k=±1。；n=4 有 1/2-1/3-1/4=-1/12=-1/L₄，故严格式不能对所有 n 成立。
- 第一阻塞点：区间素数只有 Θ(n/log n) 个，碰撞法因此只能给 exp(-Θ(n/log n))，距 2^{-n} 缺线性指数。对第二问，模单个素数或最高素数幂只给若干同余约束，尚不能排除带符号的 Bézout 表示 ±1。
- 下一步：可检验任务：对整数权重 w_k=L_n/k 建立 SAT/整数规划搜索，记录等式 ∑δ_kw_k=±1 的最小支持及其模各最高素数幂约束；检验是否存在可归纳的“新最高素数幂迫使某 δ_k=0”消元模式。
- 来源核对：[官方 #317](https://www.erdosproblems.com/317) 核对了两问均 open、弱上界和 n=4 等号例。；本地 317.lean 的非严格不等式与 n=4 反例均单列；候选将第一问解释为不同子集和间距是正确的。
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/317)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/317.lean`；既有候选答案（按不可信材料审计）

### #318

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be an infinite arithmetic progression and $f:A\to \{-1,1\}$ be a non-constant function. Must there exist a finite non-empty $S\subset A$ such that\[\sum_{n\in S}\frac{f(n)}{n}=0?\]What about if $A$ is an arbitrary set of positive density? What if $A$ is the set of squares excluding $1$?
- 题意摘要：性质 P₁(A) 指：对每个非常值 f:A→{-1,1}，存在有限非空 S⊂A，使 ∑_{n∈S}f(n)/n=0。题目分别询问无限等差数列、任意正密度集合、以及 A={k²:k≥2}。
- 状态核对：该组合题现已解决：无限等差数列为“是”（Sattler）；任意正密度集合一般为“否”；平方数去掉 1 为“是”（Larsen，2026）。候选答案把最后一问写成 open，已被 2026 年更新推翻。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建可直接核验的否定部分，并核对两个肯定定理。正密度反例取 A={2}∪{奇正整数}，令 f(2)=-1、其余 f=1。若 2∉S，和为正；若 2∈S，等式要求若干奇分母倒数之和为 1/2，但左边通分后约分所得分母仍为奇数，不可能等于 1/2。等差数列部分调用 Sattler 的 P₁ 定理；平方数去 1 部分对应 Larsen 的新定理 P₁({k²:k≥2})。
- 局部结论：正密度不足：上述 A 的自然密度为 1/2，却不存在所需 S。更一般地，恰含一个偶数的集合存在同类 2-adic 障碍。；若平方数集合包含 1，取 f(1)=1、其余平方数取 -1，则任何含 1 的有限和大于 1-∑_{k≥2}1/k²>0，不含 1 的和为负；因此排除 1 确属必要。；官方记录及本地 318.lean 均确认 Larsen 已证明 P₁({k²:k≥2})，所以最后一问不能再标为 open。
- 第一阻塞点：状态和反例已核闭；但当前可访问材料只给 Larsen 论文链接与定理结论，未能从 PDF 文本逐引理重放平方数肯定证明。因此这是已知定理核对，不冒充独立重证。
- 下一步：可检验任务：取得 Larsen 论文可检索文本，逐项核对其核心有限恒等式/归纳引理是否确实覆盖所有非常值符号函数，并将其假设与 P₁({k²:k≥2}) 的量词逐字对齐。
- 来源核对：[官方 #318](https://www.erdosproblems.com/318) 于 2026-04-01 更新为 solved，并明确记载 Larsen 对平方数去 1 的肯定证明。；本地 318.lean 已更新引用 [La26]，并把等差数列、单一偶数反例、平方数去 1 分别标为已解决定理；其中平方数定理主体仍为 sorry，不能视作形式验证完成。；候选答案的正密度反例正确，但其“平方数情形 open”已过时。
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/318)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/318.lean`；既有候选答案（按不可信材料审计）

### #319

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the size of the largest $A\subseteq \{1,\ldots,N\}$ such that there is a function $\delta:A\to \{-1,1\}$ such that\[\sum_{n\in A}\frac{\delta_n}{n}=0\]and\[\sum_{n\in A'}\frac{\delta_n}{n}\neq 0\]for all non-empty $A'\subsetneq A$?
- 题意摘要：令 M(N) 为满足下述条件的最大基数：存在 A⊆{1,…,N} 及同一个符号函数 δ:A→{−1,1}，使全和为 0，而每个非空真子集 A'⊊A 的相应带符号倒数和均非零。问题要求确定 M(N)。
- 状态核对：冻结状态为 open。现有材料给出线性下界，但没有确定最佳常数或精确渐近。候选答案的 M(N)≤N−1 论证经独立检查是成立的，但仍未解决开放部分。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：下界采用 Croot 的单位分数集合；上界采用 2-adic 唯一最大赋值障碍。设 2^j≤N<2^{j+1}。若 2^j∈A，令 L=lcm(A)，则 L/2^j 为奇数，而对所有其他 n∈A，因 v₂(n)<j，L/n 为偶数；整数化后的零和模 2 矛盾。
- 局部结论：若 Croot 给出 B⊆[(e^{-1}−o(1))N,N] 且 ∑_{b∈B}1/b=1，则该整段的倒数和为 1+o(1)，故遗漏部分的倒数和为 o(1)；每项至少 1/N，所以遗漏元素为 o(N)，从而 |B|=(1−e^{-1}+o(1))N。；取 A=B∪{1}、δ(1)=1、δ(b)=−1。未含 1 的非空子集之和为负；含 1 的真子集因遗漏至少一个正倒数，其和严格为正。因此 A 是支撑极小的零和。；上述 2-adic 论证给出 M(N)≤N−1，故 (1−e^{-1}+o(1))N≤M(N)≤N−1，特别地 M(N)=Θ(N)。
- 第一阻塞点：第一处无法闭合的是把 2-adic 的“至少排除一个元素”加强为排除正比例多个元素；当前路线没有给出 M(N)≤(1−η)N 的固定 η>0，更无法匹配 1−1/e。
- 下一步：检验多素数版本：对每个素数 p，分类具有区间内唯一最大 v_p 的分母，并建立这些强制排除条件之间的重叠界；先计算它是否能推出正密度排除。
- 来源核对：已核对本地 319.lean：量词确为存在单一 δ，且要求所有非空真子集非零。；已核对 Erdős Problems #319 对 Croot 下界的陈述。；候选答案中“Croot 下界的基数理由”表述过快；上述通过遗漏部分倒数和 o(1) 补足。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/319)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/319.lean`；既有候选答案（按不可信材料审计）

### #320

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $S(N)$ count the number of distinct sums of the form $\sum_{n\in A}\frac{1}{n}$ for $A\subseteq \{1,\ldots,N\}$. Estimate $S(N)$.
- 题意摘要：S(N) 是映射 A⊆{1,…,N}↦∑_{n∈A}1/n 的像集大小；不同子集允许碰撞，问题是估计这一像集的增长。
- 状态核对：冻结标签为 solved，宜理解为重建已发表的上下界，而非精确渐近已知。输入所引 BGMS25 首次提交于 2025-09-12，晚于 status_last_update=2025-08-31，存在时间戳不一致；其定理本身可由论文核对。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：先重建可完全证明的素数下界，再定位 Bleicher–Erdős/BGMS 递推的关键机制。若 U 为加入分母 n 后像集恰好翻倍的 n，则每个 n∈U 贡献一位独立二进制选择，因而 log S(N)≥|U∩[1,N]|log 2；论文通过素数乘法封闭性和积分递推估计 U。
- 局部结论：不同素数子集给出不同和：将一条 {−1,0,1} 关系乘以所有相关素数之积，再模对称差中的一个素数，即得矛盾。因此 S(N)≥2^{π(N)}。；显然 S(N)≤2^N；Bleicher–Erdős 的精细分母分类进一步给出 log S(N)≤(N/log N)(log_rN∏_{i=3}^r log_iN)，在其参数条件下为次线性指数。；BGMS 的已核对定理为 log S(N)≥(N/log N)·2log2·(1−3/(2log_kN))∏_{i=3}^klog_iN，条件 k≥4、log_kN≥3/2。
- 第一阻塞点：从“加入 n 时翻倍”的局部判据到所需数量的 n，需要证明集合 U 的除数稳定性及带素数扩张的积分递推；仅凭素数模约化不能重建该递推的全部误差与参数范围。
- 下一步：逐条复核 BGMS 论文 Lemma 1、2、7：形式化证明 n∈U 当且仅当不存在涉及 1/n 的 {−1,0,1} 倒数关系，并验证积分递推在 log_kN≥3/2 下的常数传播。
- 来源核对：已核对 Bleicher–Erdős 1975 原论文首页及其迭代对数下界。；已核对 arXiv:2509.10030 的定理陈述、定义 E_N=S(N) 及递推证明框架。；候选答案称“真阶仍未钉住”与现有上下界相容，但不应把 frozen solved 标签解释为精确渐近已解决。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/320)；既有候选答案（按不可信材料审计）

### #321

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：What is the size of the largest $A\subseteq \{1,\ldots,N\}$ such that all sums $\sum_{n\in S}\frac{1}{n}$ are distinct for $S\subseteq A$?
- 题意摘要：R(N) 是最大 |A|，其中 A⊆{1,…,N}，且对任意两个子集 S,T⊆A，等式 ∑_{n∈S}1/n=∑_{n∈T}1/n 必须推出 S=T。空子集也包括在内。
- 状态核对：输入标为 solved，但本地 321.lean 和当前官方页面仍把精确问题标为 research open；可重建的是 Bleicher–Erdős 上下界。因此这里不把候选答案的概括当作完整解。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：下界寻找不存在非平凡 {−1,0,1} 倒数关系的分母集；上界把 A 的 2^{|A|} 个不同子集和嵌入问题 320 的全部 S(N) 个值中。
- 局部结论：任意两两互素且均大于 1 的 A 都可行：将关系乘以 P=∏_{a∈A}a，再模某个 a，只有该项保留，迫使其系数为 0。因此取所有 p≤N 的素数得 R(N)≥π(N)。；一般地 2^{R(N)}≤S(N)，故 R(N)≤log S(N)/log2；把问题 320 的 Bleicher–Erdős 上界代入，立即得到官方所列 R(N) 上界。；Bleicher–Erdős 的构造又给出 R(N)≥(N/log N)∏_{i=3}^klog_iN，在 log_kN≥k 的条件下成立。
- 第一阻塞点：初等互素构造只能达到约 N/log N；要得到迭代对数乘积，必须构造大量具有受控素因子层级的合数，同时排除所有 {−1,0,1} 关系。该独立性引理是当前路线第一处不能自行闭合之处。
- 下一步：从 1975 论文中抽取其 Q_k(N) 集合的精确定义，并验证：这些分母的任意 {−1,0,1} 倒数关系均平凡；随后单独核对 Q_k(N) 的筛法计数。
- 来源核对：已核对 321.lean 中 InjOn 在 A.powerset 上的量词。；已核对官方所列 Bleicher–Erdős 参数化上下界。；候选答案声称 R(N)=(N/log N)(log_3N)^{1+o(1)}；该式不能直接由其展示的固定 k,r 版本推出，故未采纳。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/321)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/321.lean`；既有候选答案（按不可信材料审计）

### #322

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $A\subset \mathbb{N}$ be the set of $k$th powers. What is the order of growth of $1_A^{(k)}(n)$, i.e. the number of representations of $n$ as the sum of $k$ many $k$th powers? Does there exist some $c>0$ and infinitely many $n$ such that\[1_A^{(k)}(n) >n^c?\]
- 题意摘要：对每个固定 k≥3，令 r_k(n)=1_A^{(k)}(n) 计数有序 k 元组正整数 (x_1,…,x_k) 满足 ∑x_i^k=n；若采用无序计数只差至多 k!。问题问其最大阶，特别是是否存在固定 c>0，使 r_k(n)>n^c 对无穷多个 n 成立。
- 状态核对：冻结状态为 open。k=3 已知肯定答案；k≥4 的固定幂次大值问题仍开放。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先核验 Mahler 的 k=3 参数恒等式，再考察它能否推广到高次。正确恒等式为 m^{12}=(9t^4)^3+(m^4−9mt^3)^3+(9m^3t−9t^4)^3。
- 局部结论：取 1≤t≤c m，其中固定 c<min(1,9^{-1/3})，三个底数均为正；不同 t 给出至少常数倍 m 个有序表示。因此 r_3(m^{12})≫m=(m^{12})^{1/12}。；对任意固定 k，∑_{n≤N}r_k(n) 等于区域 ∑x_i^k≤N 内的格点数；由内外立方体夹逼可严格得 Θ_k(N)，故平均表示数为 Θ_k(1)。这不控制最大值。；官方所引 Erdős–Chowla 结果给每个 k≥3 无穷多个 n 满足 r_k(n)≫n^{c_k/loglog n}，但指数趋于 0，不能推出任何固定幂次。
- 第一阻塞点：Mahler 恒等式依赖三次曲面的特殊参数化；对 k≥4，没有构造出一个固定 n 的正维整数参数族并同时保证至少 n^c 个不同正整数点。
- 下一步：对 k=4 先做代数任务：搜索齐次恒等式 M^D=F_1(t,M)^4+⋯+F_4(t,M)^4，并用维数与次数计算其即使成立时能提供的指数 c；若维数计数不足即可淘汰该模板。
- 来源核对：已核对 Erdős Problems #322 对 Mahler、Erdős–Chowla及 k≥4 开放性的说明。；候选答案写出的三立方恒等式变量和项次不正确，直接展开一般不成立；已改用经核对的 m^{12} 恒等式。；正整数、有序表示的规范与官方 A⊂N 表述一致；改变排列规范不影响指数问题。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/322)；既有候选答案（按不可信材料审计）

### #323

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1\leq m\leq k$ and $f_{k,m}(x)$ denote the number of integers $\leq x$ which are the sum of $m$ many nonnegative $k$th powers. Is it true that\[f_{k,k}(x) \gg_\epsilon x^{1-\epsilon}\]for all $\epsilon>0$? Is it true that if $m<k$ then\[f_{k,m}(x) \gg x^{m/k}\]for sufficiently large $x$?
- 题意摘要：固定整数 1≤m≤k，f_{k,m}(x) 计数 n≤x 中至少有一种表示 n=a_1^k+⋯+a_m^k、a_i≥0 的不同整数 n。问题分别量化为：对所有 k 及每个 ε>0，是否 f_{k,k}(x)≫_{k,ε}x^{1−ε}；以及对所有 m<k，是否 f_{k,m}(x)≫_{k,m}x^{m/k}。
- 状态核对：冻结状态为 open。k=2 的对角情形由 Landau 解决；输入官方背景明确指出 k>2 甚至是否 f_{k,k}(x)=o(x) 都未知。候选答案关于 m=2 的额外历史断言未从给定官方背景充分核实，故不作为本次筛查依据。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：采用加法能量归约。令 X=⌊(x/m)^{1/k}⌋，考虑 [0,X]^m 的 T=(X+1)^m 个元组；其和均不超过 x。若 E_{k,m}(X) 计数两组元组具有相同 k 次幂和，则 Cauchy–Schwarz 给 f_{k,m}(x)≥T²/E_{k,m}(X)。
- 局部结论：固定等式中的前 2m−1 个变量后，最后一个变量至多有一个非负整数值，故 E_{k,m}(X)≤(X+1)^{2m−1}；于是无条件得到 f_{k,m}(x)≫x^{1/k}。；要推出预期的 f_{k,m}(x)≫x^{m/k}，沿此路线只需证明 E_{k,m}(X)≪X^m，即碰撞基本只有对角量级。；当 m=k 时，若能证明 E_{k,k}(X)≪_εX^{k+ε}，便得到 f_{k,k}(x)≫_εx^{1−ε/k}；这正是 Hardy–Littlewood K* 型二阶矩障碍。
- 第一阻塞点：第一处无法闭合的是把平凡能量界 X^{2m−1} 降至 X^{m+o(1)}。这要求控制方程 ∑a_i^k=∑b_i^k 的全部非对角整数解；现有初等凸性或逐变量固定不能提供所需节省。
- 下一步：先对最小未解决实例 (k,m)=(4,3) 分解能量为对角与非对角部分，计算已知 Vinogradov 均值或确定性方法实际给出的指数；检验是否至少能把 x^{1/4} 改进为某个显式更大幂次。
- 来源核对：已核对 323.lean：非负变量、不同可表示整数的 ncard，以及两个 Big-O 量词均与上述重述一致。；已核对 Erdős Problems #323 的 Landau 特例及 k>2 的开放说明。；候选答案列出的 Wooley 指数和 m=2 全范围结论未在本轮获得足够的一手来源支持，故没有复述。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/323)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/323.lean`；既有候选答案（按不可信材料审计）

### #324

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does there exist a polynomial $f(x)\in\mathbb{Z}[x]$ such that all the sums $f(a)+f(b)$ with $a<b$ nonnegative integers are distinct?
- 题意摘要：求是否存在一个固定的整数系数多项式 f，使映射 (a,b)↦f(a)+f(b) 在所有非负整数对 a<b 上单射；即两组无序二元组产生相同和时必须完全相同。
- 状态核对：仍为开放题。现有结果排除所有次数≤3的整数多项式；经典结果只排除特定四次式 x^4，并未排除所有四次多项式。候选答案在这一点上应作此区分。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：检验官方候选 f(x)=x^5。若 a^5+b^5=c^5+d^5，先按 a<c≤d<b 排列非平凡碰撞，再用模11的五次幂剩余筛选，企图排除本原解。
- 局部结论：若两对共享一个指标，例如 a=c，则消去后 b^5=d^5，故 b=d；任何反例必须有四个互异指标。；非平凡碰撞经交换两对及每对内部次序后必可写成 a<c<d<b，并满足 b^5-d^5=c^5-a^5。；模11时，x^5∈{0,1,-1}；因此两边四个数的“是否被11整除及二次剩余符号”之和必须完全相同。这给出严格但远不足够的同余筛。
- 第一阻塞点：同余条件并不能排除本原的四个互异非负整数解；所缺正是排除 a^5+b^5=c^5+d^5 非平凡解的深层步骤，不能由上述模11筛推出。
- 下一步：枚举其他小素数 p 的五次幂剩余，构造覆盖全部可能残余模式的有限筛；若仍有模式存活，明确给出最小存活模式，而不是把有限搜索误作证明。
- 来源核对：[官方条目](https://www.erdosproblems.com/324)于2026-04-11仍标为开放，并明确列出 x^5 候选、x^4 的失败及三次多项式排除结果。；Dubickas–Novikas 论文摘要确实声称对每个次数≤3的整数多项式构造无限多个四个指标互异的碰撞；未采用候选答案中的 ResearchGate 转述。；本地 Lean 陈述与输入量词一致：要求在集合 {(a,b):a<b} 上 InjOn。
- 时间记账：所在批次墙钟时间按题数均摊约 70.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/324)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/324.lean`；既有候选答案（按不可信材料审计）

### #325

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $f_{k,3}(x)$ denote the number of integers $\leq x$ which are the sum of three nonnegative $k$th powers. Is it true that\[f_{k,3}(x) \gg x^{3/k}\]or even $\gg_\epsilon x^{3/k-\epsilon}$?
- 题意摘要：对每个固定整数 k≥3，令 f_{k,3}(x) 为 n≤x 中可写成 a^k+b^k+c^k（a,b,c≥0）的不同整数个数。问题问是否存在依赖于 k 的正常数使 f_{k,3}(x)≫x^{3/k}；较弱版对每个 ε>0 问 f_{k,3}(x)≫_{k,ε}x^{3/k-ε}。
- 状态核对：全体 k≥3 的断言仍开放；k=3 的已知指数0.91709477低于1。候选答案关于 k≥11 的路线有依据，但这只是部分范围，不能把原问题整体标为已解。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：令 r_k(n) 为有序正整数三元组表示数，T=∑_{n≤x}r_k(n)，R=∑_{n≤x}r_k(n)^2。用 Cauchy–Schwarz 将问题归约为等和六变量方程的二阶矩估计。
- 局部结论：取1≤a,b,c≤⌊(x/3)^{1/k}⌋即得 T≫_k x^{3/k}；故 f_{k,3}(x)≥T^2/R。；若能证明 R≪_{k,ε}x^{3/k+ε}，便严格推出 f_{k,3}(x)≫x^{3/k-ε}；若 R≪_k x^{3/k}，则推出强版本。粗略地固定五个变量只给 R≪x^{5/k}，因而仅得 x^{1/k}。；Salberger公布的 k≥11 估计 n_k(B)=6B^3+O_k(B^{3-δ})可应用于正整数三元组，给 R≪x^{3/k}，从而至少严格推出 k≥11 的强下界；允许零只会扩大目标集合。
- 第一阻塞点：对3≤k≤10，当前路线缺少 R≪x^{3/k+ε}；尤其 k=3 时必须把等和三次幂六变量解的二阶矩从现有水平压到近对角规模。
- 下一步：对每个3≤k≤10整理现有六变量均值估计的明确指数 θ_k（R≪x^{θ_k}），代入 6/k−θ_k 得到可核验的 f_{k,3} 指数表，优先复算 k=3 的0.91709477。
- 来源核对：[官方条目](https://www.erdosproblems.com/325)仍标为开放，并记录 Wooley 的 k=3 下界。；[Wooley 原论文](https://www.math.purdue.edu/~twooley/publ/20150506sum3cub2.pdf)的 Theorem 1.1 给出指数 β=0.91709477。；[Salberger 的 Oberwolfach 报告](https://ems.press/content/serial-article-files/46829)明确陈述 d≥11 时 n_d(B)=6B^3+O_d(B^{3-δ})；这里仅使用其足以推出下界的部分，没有照搬候选答案中未经展开的精确常数渐近式。
- 时间记账：所在批次墙钟时间按题数均摊约 70.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/325)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/325.lean`；既有候选答案（按不可信材料审计）

### #326

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{N}$ be an additive basis of order $2$. Must there exist $B=\{b_1<b_2<\cdots\}\subseteq A$ which is also a basis such that\[\lim_{k\to \infty}\frac{b_k}{k^2}\]does not exist?
- 题意摘要：冻结题面量词是：对每个二阶加法基 A⊂N，是否存在递增枚举 B={b_k}⊂A，使 B仍为二阶基且实数序列 b_k/k^2 不收敛。这里要的是某个子基，不要求 B为真子集。
- 状态核对：冻结题面标为开放，但当前官方网页已改成“是否存在具有正二次极限的极小二阶基”，与输入文字不相同；因此本项以输入及本地 Lean 冻结陈述为准。Cassels 只说明某些基本身具有极限，不能否定其中存在不规则子基。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：若 A本身不规则便取 B=A；困难情形是 A={a_k}具有极限。尝试在交替的长区间中删除非必要元素，使子基计数函数时疏时密，同时保留所有充分大整数的二元表示。
- 局部结论：任一二阶渐近基 C={c_k}满足 |C∩[1,x]|(|C∩[1,x]|+1)/2≥x-O(1)，故 c_k≤(1/2+o(1))k^2；任何存在的正极限至多为1/2。；若 A本身的 a_k/k^2 不收敛，结论立即成立；潜在反例必须使 A及其每个仍为基的子集都收敛。；若存在一个具有 c_k/k^2→c>0 的极小二阶基 C，则取 A=C会直接反驳冻结题面，因为它没有真子基仍为基，而 B=A又收敛。
- 第一阻塞点：删除构造首先卡在“局部有冗余表示”不能推出“无限轮删除后仍覆盖所有充分大整数”。极小基恰好说明逐个元素都可能对无穷多个整数不可替代；不能用未经证明的 Zorn/对角交论证取得合适子基。
- 下一步：检验一个明确的冗余引理：若每个充分大 n至少有两种互不共享元素的 A+A 表示，能否分块删除并保持基性质，同时令两个子序列上的 b_k/k^2 分离；先证明或构造反例于该加强假设。
- 来源核对：本地 326.lean 与冻结输入一致，量化所有 A并要求存在递增 b、range(b)为基且不趋于任何实数。；[当前官方页面](https://www.erdosproblems.com/326)在2026-04-17后展示的是不同的“极小基且正极限”问题；这一版本漂移已明确隔离，不能用来悄然改写冻结题目。
- 时间记账：所在批次墙钟时间按题数均摊约 70.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/326)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/326.lean`；既有候选答案（按不可信材料审计）

### #327

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Suppose $A\subseteq \{1,\ldots,N\}$ is such that if $a,b\in A$ and $a\neq b$ then $a+b\nmid ab$. Can $A$ be 'substantially more' than the odd numbers? What if $a,b\in A$ with $a\neq b$ implies $a+b\nmid 2ab$? Must $\lvert A\rvert=o(N)$?
- 题意摘要：对每个 N研究图 G_m(N)：顶点为1,…,N，若不同 a,b满足 a+b∣mab则连边。第一问 m=1时独立集能否在渐近意义上显著超过奇数集的约 N/2；第二问 m=2时是否每个独立集族都满足 |A|/N→0。
- 状态核对：两项渐近问题仍开放。候选答案中的两个 N=50例可直接核验，但有限例不能决定“substantially”或 o(N)；其 N=100、200最优值及 O(N log log N)边数没有可靠来源，故不采纳。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先完整参数化边，再计数边数并用贪心/Caro–Wei型估计构造独立集。写 a=gx,b=gy，(x,y)=1。
- 局部结论：因 gcd(x+y,xy)=1，严格等价于 a+b∣mab ⇔ x+y∣mg ⇔ (x+y)/gcd(x+y,m)∣g。故所有边可写成 a=tqx,b=tqy，其中 q=(x+y)/gcd(x+y,m)、(x,y)=1。；由 tqy≤N及 q≥(x+y)/m，边数 E_m(N)≤mN∑_{y≤√(mN)}∑_{x<y}1/[y(x+y)]=O_m(N log N)。因此两种情形都存在大小 Ω_m(N/log N)的独立集。；逐对检查确认候选给出的两个 N=50集合均有38个元素，并分别满足 m=1、m=2条件；这只证明具体有限断言，不证明正密度。
- 第一阻塞点：O(N log N)边数只给 Ω(N/log N)，仍是 o(N)；要回答第一问需构造密度>1/2的无限族或加强上界，要否定第二问则需正密度构造。参数化本身没有控制边在各尺度间的聚集。
- 下一步：按2-adic层及比值区间分块计算边密度，尝试找出一个固定有限层模板，其诱导子图可证明具有密度正的独立集；同时用整数规划只作为发现模板的工具，再对模板作符号化证明。
- 来源核对：[官方条目](https://www.erdosproblems.com/327)仍标为开放，并记录 m=1情形的上界障碍：密度达到25/28+o(1)必含坏对。；官方页没有支持候选答案所称 N=100、200精确最优值或 O(N log log N)边数，因此未复述这些断言。
- 时间记账：所在批次墙钟时间按题数均摊约 70.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/327)；既有候选答案（按不可信材料审计）

### #329

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Suppose $A\subseteq \mathbb{N}$ is a Sidon set. How large can\[\limsup_{N\to \infty}\frac{\lvert A\cap \{1,\ldots,N\}\rvert}{N^{1/2}}\]be?
- 题意摘要：在所有无限 Sidon 集 A⊂N中，求 L(A)=limsup_{N→∞}|A∩[1,N]|/√N 的上确界。Sidon指每个和 a+b（通常取a≤b）具有至多一种无序表示。
- 状态核对：精确上确界仍未知；已知存在 L=1/√2的构造，且所有 A满足 L≤1。目标是判断上界1能否达到。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从接近最优的有限 Sidon 集出发，试图把它们放入迅速增长的区块并嵌套成一个无限 Sidon 集，使某些区块终点的归一化计数趋近1。
- 局部结论：若 A∩[1,N]有m个元素，其 m(m−1)/2个正差互异，故初等地 m≤√(2N)+O(1)；更精细的 Erdős–Turán滑动区间计数把无限情形的 limsup上界改进到1。；有限近完美 Sidon 集本身不足以构造无限例：新旧混合和碰撞等价于新块差 v−v'等于旧块差 u'−u，因此平移新区块不会消除这种碰撞。；把新区块放大 D倍可令其非零差超过旧差并避免上述碰撞，但区块直径也放大 D倍，归一化密度损失因子 D^{-1/2}；这解释了朴素分块路线无法达到1。
- 第一阻塞点：缺少一列相容的近完美有限 Sidon 集，使每一级的差集既避开此前差集又无需固定比例放大。官方所述“每个有限 Sidon 集可嵌入完美差集”正可填补这一兼容性缺口，但该嵌入命题本身开放。
- 下一步：对小阶完美差集做可复现计算：给定一个有限 Sidon 集 S，求包含其仿射副本的最小完美差集阶数；测量必要膨胀率是否趋近1，并找出最早的不可嵌入候选。
- 来源核对：[官方条目](https://www.erdosproblems.com/329)确认下界1/√2、上界1及“达到1”的开放性，并说明有限 Sidon 集嵌入完美差集会推出达到1。；本地 Lean 陈述把问题形式化为所有 Sidon 集上 sidonUpperDensity 的上确界；与输入量词一致。
- 时间记账：所在批次墙钟时间按题数均摊约 70.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/329)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/329.lean`；既有候选答案（按不可信材料审计）

### #330

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Does there exist a minimal basis with positive density, say $A\subset\mathbb{N}$, such that for any $n\in A$ the (upper) density of integers which cannot be represented without using $n$ is positive?
- 题意摘要：求证存在集合 A⊆ℕ，使其为二阶渐近加法基，A 具有正上密度，并且对每个 a∈A，私人集 E_A(a):=(A+A)\((A\{a})+(A\{a})) 也具有正上密度；后一性质自动蕴含删除 a 后不再是渐近基，故 A 极小。
- 状态核对：已于 2026-05-11 被列为肯定解决且经 Lean 验证。旧候选称其仍开放，已失效。需特别区分：题目的正确版本使用上密度和恰好两个加数；给出的本地 330.lean 仍含 sorry，且 Set.HasPosDensity 表示存在正自然密度、Rep 使用至多 h 项，不能把这个本地文件本身当成已验证证明。独立的 Lean 工程明确形式化了正确的上密度二项和版本。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建已知构造的骨架：为每个已激活元素 a 配置个人素数 m_a；以后加入 A 的元素避开模 m_a 的两个危险剩余类。用 CRT 有限乘积构造每一阶段的稠密尾块，同时为当前服务的 a 构造一段受保护的私人和块。公平调度使每个 a 被服务无穷多次，阶段覆盖端点趋于无穷，从而取各阶段有限集之并得到最终 A。
- 局部结论：若每阶段的允许剩余类密度满足 ∏_{a∈P}(1-1/m_a)≥1-∑_{a∈P}1/m_a≥δ₀>0，则在趋于无穷的阶段端点 x_j 上有 |A∩[1,x_j]|≥(δ₀/4)x_j，因此 d̄(A)>0。；每次服务 a 时，可产生永久受保护块 B_{a,j}⊆E_A(a)，并满足 |B_{a,j}|≥(δ₀/(8m_a))Y_j；若服务端点 Y_j→∞，则 d̄(E_A(a))≥δ₀/(8m_a)>0。；E_A(a) 有正上密度，因而包含任意大的整数；故 A\{a} 漏掉无穷多个大整数，极小性随即成立。
- 第一阻塞点：本次没有重新闭合完整的有限 CRT 装置：关键是同时证明所选坐标产生私人和、非所选坐标仍具有两种安全表示，并把乘积模型经 CRT 转回整数剩余类。该步骤在现有 Lean 工程中已处理，但不能由本地含 sorry 的 330.lean 单独核验。
- 下一步：在固定的一组小素数上逐条核验“selected-coordinate/privacy”和“two-safe-pairs”有限引理，并在独立工程中执行无 sorry 编译；同时记录其与本地自然密度版本并不等价。
- 来源核对：[官方页面](https://www.erdosproblems.com/330)标记 PROVED (LEAN)，并链接构造与形式化。；[讨论与形式化说明](https://www.erdosproblems.com/forum/thread/330)明确指出正确目标是正上密度，并概述个人素数、剩余类保护机制。；[证明忠实的形式化工程](https://github.com/AllenGrahamHart/FormalConjectures-Bench/tree/main/formalizations/erdos330)采用 exact two-fold sums 与 upperDensity；其说明明确拒绝把原有 answer(sorry)/自然密度陈述当作规范目标。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/330)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/330.lean`；既有候选答案（按不可信材料审计）

### #332

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ and $D(A)$ be the set of those numbers which occur infinitely often as $a_1-a_2$ with $a_1,a_2\in A$. What conditions on $A$ are sufficient to ensure $D(A)$ has bounded gaps?
- 题意摘要：给定 A⊆ℕ，令 D(A)={d∈ℤ: 存在无穷多对 (a,b)∈A² 使 a-b=d}。问题不是一个单一真假命题，而是寻找尽可能弱、可检验的 A 的充分条件，使 D(A) syndetic，即存在 M，使每个长度 M 的整数区间都与 D(A) 相交。
- 状态核对：仍开放；已知正渐近密度是充分条件。人工评审所说“还要进一步研究 D(A) 的正密度”等是官方列出的加强问题，不应误写成原陈述已被完全刻画。旧候选给出的正上 Banach 密度路线可作为更强的已知型充分条件，但并未回答“哪些条件”的最佳范围。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `medium`
- 尝试路线：取 d*(A)=δ>0，使用平移系统的对应原理得到保测系统 (X,μ,T) 与 μ(E)=δ。对 ε=δ²/2 应用 Khintchine 回归：R={n: μ(E∩T^{-n}E)>δ²/2} 为 syndetic。再把每个 n∈R 转回 A 中无穷多对相距 n 的元素。
- 局部结论：若某个固定 d 满足 d*(A∩(A-d))>0，则 A∩(A-d) 为无限集，所以 d∈D(A)。；Khintchine 回归若适用于对应系统，则 R⊆D(A)，而 syndetic 集的任意超集仍 syndetic，故 D(A) 有界间隙。；厚集是可直接验证的特例：A 含任意长区间时，每个固定 d 都出现无穷多次，故 D(A)=ℤ（按正差版本则为 ℕ₀）。
- 第一阻塞点：第一处需认真闭合的是对应原理的回译：一般对应原理先给出 μ(E∩T^{-d}E)≤或受控于某种局部密度，必须确认所得正测度确实推出原集合中该差出现无穷多次，而不是只在极限模型中回归。此步骤是标准的，但这里未重建全部紧致性证明。即使闭合，也只给出充分条件，不能刻画更弱阈值。
- 下一步：写出一个纯组合版本：从任意 d*(A)>δ 出发构造有限 F（目标 |F|≤⌈1/δ⌉ 型界），证明 F+D(A)=ℤ；逐项检查由有限窗口中的高重叠到“无穷多次出现”的对角抽取。
- 来源核对：[官方页面](https://www.erdosproblems.com/332)确认问题开放，并记载 Prikry、Tijdeman、Stewart 等已证明正密度充分。；本地 332.lean 只用 answer(sorry) 占位，并未形式化具体充分条件；其 D_A 为有符号差集，HasBoundedGaps 定义为 ℤ 上 syndetic。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/332)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/332.lean`；既有候选答案（按不可信材料审计）

### #334

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find the best function $f(n)$ such that every $n$ can be written as $n=a+b$ where both $a,b$ are $f(n)$-smooth (that is, are not divisible by any prime $p>f(n)$.)
- 题意摘要：定义点态最优量 F(n)=min_{a,b≥1,a+b=n} max(P⁺(a),P⁺(b))，其中 P⁺(1)=1。问题要求确定支配所有 n 的最佳渐近函数 f，即对每个 n 都有 F(n)≤f(n)，并尽量确定其最小数量级。
- 状态核对：仍开放。已知一般上界为 F(n)≪_ε n^{4/(9√e)+ε}；n^{o(1)} 仍属猜想，不能把 n^{0.2695+o(1)} 称作已确定的“最优函数”。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试用 p≡3 (mod 4) 的素数输入把问题归约到最小二次非剩余。设 p=a+b 且 a,b 均为 y-smooth；反设所有不超过 y 的素数都是模 p 的二次剩余，则 a、b 也都是非零二次剩余。但 a≡-b (mod p)，于是 Legendre 符号满足 (a/p)=(-1/p)(b/p)=-(b/p)，矛盾。
- 局部结论：对每个素数 p≡3 (mod 4)，任意平滑分拆 p=a+b 的某个素因子必须是模 p 的二次非剩余。；若 ℓ(p) 表示最小的素数二次非剩余，则 F(p)≥ℓ(p)。这给出两平滑数加法问题到最小二次非剩余问题的严格障碍归约。；平凡地 F(n)≤P⁺(n-1)，由 n=1+(n-1) 得到；真正困难在于为所有 n 同时显著压低两个最大素因子。
- 第一阻塞点：归约只给出依赖 ℓ(p) 的下界；目前无法对一列 p≡3 (mod 4) 给出足以接近 Balog 指数的无条件增长率。反方向上，从丰富的 y-smooth 数分布推出每个 n 都落在 S(y)+S(y)，也需要远强于仅计数 |S(y)∩[1,n]| 的均匀加法覆盖。
- 下一步：对 p≤X 计算 F(p) 与 ℓ(p)，检验障碍何时取等；理论上先证明固定 Y 下存在无穷多个 p≡3 (mod 4) 使所有 q≤Y 均为二次剩余，再量化该构造中 p 相对 Y 的大小。
- 来源核对：[官方页面](https://www.erdosproblems.com/334)确认问题开放，并记载 Balog 的指数 4/(9√e)。；旧候选关于二次非剩余的障碍经上述 Legendre 符号论证独立核对；但其中“三个加数”资料未用于本次判断。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/334)；既有候选答案（按不可信材料审计）

### #335

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d(A)$ denote the density of $A\subseteq \mathbb{N}$. Characterise those $A,B\subseteq \mathbb{N}$ with positive density such that\[d(A+B)=d(A)+d(B).\]
- 题意摘要：在自然密度 d(A),d(B),d(A+B) 都存在且 d(A),d(B)>0 的前提下，刻画满足 d(A+B)=d(A)+d(B) 的所有 A,B⊆ℕ；必有 d(A)+d(B)≤1。
- 状态核对：仍开放，且 2026 年已有附加“某集合遇到每个剩余类”假设下的部分结果。人工评审指出旧候选错误地宣称密度等式强迫一维紧阿贝尔因子与区间结构；该结论不成立，以下用概率构造直接解释其失败。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令 A=B 为偶数集合 2ℕ 的独立 Bernoulli(1/2) 随机子集。证明几乎必然 d(A)=1/4，而 A+A 除有限多个例外包含所有偶数，于是 d(A+A)=1/2=2d(A)。该路线产生大量没有明显旋转区间结构的等号例。
- 局部结论：强大数律给出 |A∩[1,N]|/N→1/4，故 d(A)=1/4。；对偶数 2m，可选约 m/2 个互不相交的表示 2m=2i+2(m-i)；每一对同时入 A 的概率为 1/4，所以 2m 不可表示的概率至多 (3/4)^{⌊(m-1)/2⌋}。；上述失败概率可求和；由 Borel–Cantelli，几乎必然只有有限多个偶数不在 A+A，而奇数永不在 A+A。因此 d(A+A)=1/2=d(A)+d(A)。
- 第一阻塞点：该构造只是否定“等式自动强迫一维区间模型”的路线，并显示在无额外假设时结构可极其随机；它没有给出所有等号对的可操作分类。第一处无法闭合之处正是从一个纯密度等式恢复逐点或模结构：密度忽略零密度扰动，也允许在一个周期类内部任意随机化。
- 下一步：把目标限制到官方部分结果的假设：例如要求 B 遇到每个模 q 的剩余类且 d(A+B)<1；随后逐条核对是否可由 Kneser 型稳定子分析导出“圆周×有限循环群”或“缺一个剩余类”二分。
- 来源核对：[官方页面](https://www.erdosproblems.com/335)明确给出同一随机偶数子集反例机制，并说明无附加假设的完整刻画似乎无望。；该页面还记载 Ackelsberg–Richter 2026 在一个集合遇到每个剩余类的附加假设下取得部分分类；因此旧候选的无条件 iff 分类不能接受。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/335)；既有候选答案（按不可信材料审计）

### #336

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For $r\geq 2$ let $h(r)$ be the maximal finite $k$ such that there exists a basis $A\subseteq \mathbb{N}$ of order $r$ (so every large integer is the sum of at most $r$ integers from $A$) and exact order $k$ (so every large integer is the sum of exactly $k$ integers from $A$). Find the value of\[\lim_r \frac{h(r)}{r^2}.\]
- 题意摘要：对每个整数 r≥2，h(r) 是所有满足下列条件的有限 k 的最大值：存在 A⊆ℕ，使每个充分大整数可由至多 r 个 A 元素之和表示，同时每个充分大整数可由恰好 k 个 A 元素之和表示。要求确定 r→∞ 时 h(r)/r² 的极限值。加数通常允许重复。
- 状态核对：仍开放；官方资料把该极限视为研究对象，并给出 1/3≤lim h(r)/r²≤1/2，以及 h(2)=4、h(3)=7、10≤h(4)≤11。旧候选擅自改写为 liminf/limsup 并加上“如果极限存在”，缺少依据，不沿用。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `medium`
- 尝试路线：尝试沿 Nash/Kneser 路线把 A 的“至多 r 项覆盖”与“恰好 k 项覆盖”投影到有限循环商群。若某个中间和集出现小增长，Kneser 定理产生稳定子 H；在商群 G/H 中跟踪逐次和集增长，期望把达到全群前的层数 k 控制为约 r²/2。下界则对应设计分层的有限循环模型，再提升为整数渐近基。
- 局部结论：若枚举 A={a₁<a₂<⋯} 的相邻差 gcd 大于 1，则 A 最终落在固定模数的一个剩余类中，恰好 k 项和只能落在一个剩余类，故不存在有限 exact order；这解释已知 gcd=1 判据的必要方向。；现有 Kneser 路线确实把增长控制降为有限商群中的加法直径/稳定子问题，并给出量级 h(r)=Θ(r²)，不是更高阶增长。；任何最终常数都必须落在 [1/3,1/2]；小值 h(2)=4、h(3)=7 与二次尺度相容，但不足以区分端点。
- 第一阻塞点：第一处未闭合的是把每次商群增长的损失同时用 order r 约束，并对所有可能稳定子链求出尖锐总和。粗计数能导向 O(r²)，但要把常数压到 1/2 已需 Nash 的精细 Kneser 分析；要确定极限还必须构造与上界同常数的模型或进一步改进其中一侧。
- 下一步：建立有限优化问题：枚举小 r 下所有循环群 G、子集 S 与稳定子链，计算“≤r 层覆盖”允许的最大 exact-layer 延迟；先验证该模型重现 h(2)=4、h(3)=7，并观察最优构型趋向 1/3 还是 1/2。
- 来源核对：[官方页面](https://www.erdosproblems.com/336)确认开放状态、区间 [1/3,1/2]、小 r 数值及 Grekos/Nash/Plagne 的来源。；本题没有本地形式化文件；本次未把旧候选的 liminf/limsup 改写视为已知定理。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/336)；既有候选答案（按不可信材料审计）

### #338

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：The restricted order of a basis is the least integer $t$ (if it exists) such that every large integer is the sum of at most $t$ distinct summands from $A$. What are necessary and sufficient conditions that this exists? Can it be bounded (when it exists) in terms of the order of the basis? What are necessary and sufficient conditions that this is equal to the order of the basis?
- 题意摘要：对象是渐近基 A⊆ℕ：普通阶 h 是使每个充分大整数可由至多 h 个 A 中元素之和表示的最小整数，允许重复；限制阶 t 要求加数两两不同。问题分别询问限制阶存在、由 h 一致控制、以及等于 h 的充要条件，量词均遍及所有渐近基 A。
- 状态核对：截至官方页面最近记录仍为 open。下面只验证 Bateman 模障碍，它否定“h≥3 时普通阶自动保证限制阶存在”，不构成一般刻画。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：固定 h≥3，取 A={1}∪hℕ_{>0}。先精确核对其普通阶，再研究不同元素之和模 h 的可能剩余类。
- 局部结论：若充分大 n≡r(mod h)，0≤r<h，则 n=(n-r)+1+⋯+1，其中使用 r 个 1；故至多 h 个加数，普通阶≤h。；对充分大的 n≡h−1(mod h)，若只用≤h−1个加数，则模 h 强迫恰用 h−1 个 1，所得和仅为 h−1；故普通阶恰为 h。；限制表示中 1 至多使用一次，其余项均为 h 的倍数，所以只能得到剩余类 0、1(mod h)；因此该 A 没有任何有限限制阶。更一般地，有限限制阶必要求每个模数下相应的有限长度不同元素子集和覆盖全部剩余类。
- 第一阻塞点：模剩余覆盖只是必要条件，不能把局部同余表示提升为对每个充分大整数的实际表示；尤其对“A\F 对每个有限 F 仍为基”的情形，表示阈值依赖 F，无法令 F 随待表示整数变化而保持统一。
- 下一步：检验有限删除稳定假设能否推出一个统一结论：是否存在固定 r，使每个充分大 n 至少有一个 r 项表示避开任意预先给定的、大小≤r的有限集；若能证明这种一致避障性质，再尝试逐次排除重复加数。
- 来源核对：[官方问题 338](https://www.erdosproblems.com/338) 仍标 open，并明确记录该 Bateman 例、Kelly 的 h=2 上界4及 HHP 的指数型下界。；未采用先验答案所引的 2023 密度陈述，因为它不是本次局部证明所需，且不能提供一般充要条件。
- 时间记账：所在批次墙钟时间按题数均摊约 66.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/338)；既有候选答案（按不可信材料审计）

### #340

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{1,2,4,8,13,21,31,45,66,81,97,\ldots\}$ be the greedy Sidon sequence: we begin with $1$ and iteratively include the next smallest integer that preserves the Sidon property (i.e. there are no non-trivial solutions to $a+b=c+d$). What is the order of growth of $A$? Is it true that\[\lvert A\cap \{1,\ldots,N\}\rvert \gg N^{1/2-\epsilon}\]for all $\epsilon>0$ and large $N$?
- 题意摘要：从 a₁=1 开始，每步选择大于当前末项的最小整数，使所得集合仍为 Sidon 集，即含对角和在内的无序二元和均唯一。令 A(N)=|A∩[1,N]|；问题问其增长级，并问对每个 ε>0 是否存在 c_ε,N_ε，使 N≥N_ε 时 A(N)≥c_εN^{1/2−ε}。
- 状态核对：官方页面截至 2025-11 的编辑仍标 open。本次路线严格重建已知 N^{1/3}≪A(N)≪N^{1/2}，没有触及猜想指数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：设当前贪心前缀 S_k={a₁,…,a_k}。刻画不能加入的 x>a_k：任何新 Sidon 冲突必化为 x+u=v+w，因此坏值属于 S_k+S_k−S_k；随后计数该三重和差集。
- 局部结论：每个已选 y∈S_k 都可写成 y+u−u；每个先前被拒绝的 x≤a_k 在拒绝时已有 x+u=v+w，且该关系保留至 S_k。因此 [1,a_k]⊆S_k+S_k−S_k。；该三重和差集至多有 k³ 个值，故其最小正缺失值大于 a_k 且≤k³+1；它可安全加入，于是 a_{k+1}≤k³+1，推出 A(N)≫N^{1/3}。；Sidon 性使所有正差 a_j−a_i（i<j）互异，故 C(k,2)≤a_k−1；于是 A(N)≤O(N^{1/2})。
- 第一阻塞点：要达到 a_k≤k^{2+o(1)}，必须证明远强于 |S_k+S_k−S_k|≤k³ 的结构性覆盖/重合估计。Sidon 条件本身只控制二元和相等，不能强迫三元表达 v+w−u 大量重合。先验答案直接从“至多 k³ 个坏值”跳到 a_{k+1}≤k³+1，漏写了 [1,a_k] 已全在坏值集合中的关键论证；补上后结论才闭合。
- 下一步：对前 k 项计算表示函数 r_k(x)=#{(u,{v,w}):x=v+w−u}，检验能否在区间 [1,k^{3−δ}] 上证明或否证一个可累积的平均重数下界；这是把立方计数改进为次立方计数的直接可检验节点。
- 来源核对：[官方问题 340](https://www.erdosproblems.com/340) 确认 open，并只声称平凡下界 A(N)≫N^{1/3}。；[OEIS A005282](https://oeis.org/A005282) 核对了递推、初项以及已记录的二次—三次界。；本地 Lean 陈述把目标正确写成 √N/N^ε=O(A(N))；其已验证初项与题面一致，但主定理仍为 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 66.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/340)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/340.lean`；既有候选答案（按不可信材料审计）

### #341

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{a_1<\cdots<a_k\}$ be a finite set of integers and extend it to an infinite sequence $\overline{A}=\{a_1<a_2<\cdots \}$ by defining $a_{n+1}$ for $n\geq k$ to be the least integer exceeding $a_n$ which is not of the form $a_i+a_j$ with $i,j\leq n$. Is it true that the sequence of differences $a_{m+1}-a_m$ is eventually periodic?
- 题意摘要：量词遍及每个有限严格递增正整数种子 A={a₁<⋯<a_k}。此后 a_{n+1} 是大于 a_n、且不能写成已有两项 a_i+a_j（允许 i=j）的最小整数。问题问是否对每个种子都存在 p≥1、m₀，使所有 m≥m₀ 有 a_{m+p+1}−a_{m+p}=a_{m+1}−a_m。
- 状态核对：官方页面及 Green 2025 更新均仍把一般情形列为 open。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试把逐整数的“属于序列/属于旧二和集”判定编码为有限状态自动机；先证明递推永远可继续，并核对一个完全可解种子。
- 局部结论：若当前最大项为 a_n，则 2a_n+1 不可能是两个旧项之和，故下一项存在且 a_{n+1}≤2a_n+1。；每个大于初始最大值的整数最终要么被选入序列，要么在被越过时已属于此前项的二和集；所以最终集合 S 满足尾部覆盖 ℕ=S∪(S+S)。；种子 {1} 的扩张严格为 1,3,5,…：若已有前 n 个奇数，则下一个偶数 2n 是旧二和，而 2n+1 不可能是两个奇数之和；故该例差分恒为2。
- 第一阻塞点：判定 x∈S 需要知道是否存在跨越整个历史的配对 a_i+a_j=x；即使近邻间隔有界，也不能仅由固定长度尾窗恢复这一卷积信息。因此预期的有限状态数没有得到与时间无关的上界，抽屉原理无法启动。
- 下一步：先研究受限命题：若从某处起所有表示 x=a_i+a_j 都至少有一个加数落在 [x−L,x]，证明其差分最终周期；随后用计算寻找一般贪心序列是否违反任意固定 L，以精确定位全历史障碍。
- 来源核对：[官方问题 341](https://www.erdosproblems.com/341) 仍标 open。；[Green 的问题表第7题](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf) 明确说 Dickson 与 Queneau 两种变体的最终周期性都仍开放。；本地 Lean 版本只假设递推关系“最终成立”，且未编码有限正整数种子和全程严格递增；它比原题弱且可能包含额外序列，不能视为原题的等价形式。
- 时间记账：所在批次墙钟时间按题数均摊约 66.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/341)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/341.lean`；既有候选答案（按不可信材料审计）

### #342

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：With $a_1=1$ and $a_2=2$ let $a_{n+1}$ for $n\geq 2$ be the least integer $>a_n$ which can be expressed uniquely as $a_i+a_j$ for $i<j\leq n$. What can be said about this sequence? Do infinitely many pairs $a,a+2$ occur? Does this sequence eventually have periodic differences? Is the density $0$?
- 题意摘要：对象是唯一的经典 Ulam 序列：a₁=1,a₂=2；对每个 n≥2，a_{n+1} 是大于 a_n、且恰有一个表示 a_i+a_j（i<j≤n）的最小整数。三个明确问题是：集合中是否有无穷多对 x,x+2；差分是否最终周期；其密度是否为0。对“密度0”，本次采用上密度为0这一无歧义的强形式。
- 状态核对：三个问题仍未解决。本次路线给出周期性与密度问题之间的严格排斥关系。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先用最大旧二元和保证递推继续；再假设差分从某处起以索引周期 p 重复，计算一个周期的总位移 D，并由此求集合密度。
- 局部结论：a_n+a_{n−1} 是旧的不同两项和中的唯一最大值，因此是合法唯一表示候选；故序列无限且 a_{n+1}≤a_n+a_{n−1}。；若差分最终以周期 p 重复，令 D=Σ_{j=0}^{p−1}(a_{m+j+1}−a_{m+j})，则尾部满足 a_{n+p}=a_n+D；因此尾集合是模 D 的 p 个剩余类（计重后实际仍有 p 个不同位置），自然密度为 p/D>0。于是“上密度为0”与“差分最终周期”不可能同时成立。；在同一周期假设下，尾部若出现一次 Ulam 对 x,x+2，则平移 D 后出现无穷多次；若一个周期内没有这种剩余类配对，则尾部一次也没有。因此周期性会把第一问化为有限检查。
- 第一阻塞点：递推的唯一表示条件目前既不能给出上密度趋零，也不能排除某个周期模板；上述论证只证明两个候选结论不能同时为真，不能决定哪一个失败。
- 下一步：分类所有满足已知局部限制且密度 p/D≤6/17的短周期差分模板，并逐个寻找由唯一表示递推导致的首个矛盾；若短周期全部排除，可得到可验证的“最小可能周期/位移”下界。
- 来源核对：[官方问题 342](https://www.erdosproblems.com/342) 仍将三问列为 open。；[Green 的问题表第7题](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf) 在 2025 更新中仍询问正密度，并记录相关周期性问题开放。；[OEIS A002858](https://oeis.org/A002858) 核对了初项；其中约0.074的密度与波状结构均只是计算观察，未当作证明。；本地 Lean 将第三问具体化为 upperDensity(range a)=0，这比仅询问自然密度是否存在且为0更明确。
- 时间记账：所在批次墙钟时间按题数均摊约 66.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/342)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/342.lean`；既有候选答案（按不可信材料审计）

### #345

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be a complete sequence, and define the threshold of completeness $T(A)$ to be the least integer $m$ such that all $n\geq m$ are in\[P(A) = \left\{\sum_{n\in B}n : B\subseteq A\textrm{ finite }\right\}\](the existence of $T(A)$ is guaranteed by completeness). Is it true that there are infinitely many $k$ such that $T(n^k)>T(n^{k+1})$?
- 题意摘要：对每个 k≥1，令 A_k={n^k:n≥1}；P(A_k) 由互不重复的 A_k 元素的有限子集和组成。T_k 是使所有 N≥T_k 都可表示的最小整数。问题问满足 T_k>T_{k+1} 的 k 是否有无穷多个。
- 状态核对：问题仍为 open。题面资料存在差一冲突：按所给 T 定义，若 θ_k 是最大不可表示数，则 T_k=θ_k+1；OEIS 给 θ₂=128，而官方背景写 T(n²)=128，两者不能同时成立。以下严格按 exact_statement，采用 T₂=129 的规范。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：落实 Erdős–Graham 建议的 k=2^t 路线。取 M=2^{t+1}：证明偶底数的 k 次幂为0(mod M)，奇底数的 k 次幂为1(mod M)，再由表示中奇底数项的数量给出显式不可表示数。
- 局部结论：对 t≥1、k=2^t，偶数 x 满足 x^k≡0(mod M)；由二进制 LTE，奇数 x 满足 x^k≡1(mod M)。；若 N 是不同 k 次幂之和，并令 q 为其中奇底数项数，则 q≡N(mod M)。若 N≡r(mod M)，0≤r<M，则 q≥r，故 N至少为 S_{k,r}=Σ_{j=1}^r(2j−1)^k。；因此 L_{k,r}=r+M⌊(S_{k,r}−1−r)/M⌋ 满足 L_{k,r}<S_{k,r}、L_{k,r}≡r(mod M)，从而不可表示；严格得到 T_k≥L_{k,r}+1。可取 r=M−1 得到显式强下界。
- 第一阻塞点：该同余路线只给 T_{2^t} 的下界；目标不等式还需要 T_{2^t+1} 的严格上界，小于上述不可表示数。现有完备性证明的上界过大，无法完成比较。这是第一处真正缺失，而非模计算本身。
- 下一步：固定 t=3（k=8），取 r=15 算出 L_{8,15}，再用已验证的 θ₉ 下界和可获得的 T₉ 上界比较；若方向已不可能，则系统搜索其他 r 或更高2-adic模数，明确该候选路线在 k=8 是否有数值空间。
- 来源核对：[官方问题 345](https://www.erdosproblems.com/345) 仍标 open，并提出 k=2^t 的2-adic候选路线。；[OEIS A001661](https://oeis.org/A001661) 明确定义其数列为“最大不可表示数”，首项 θ₂=128，并说明 θ_k+1 称为 anti-Waring number；这证实官方背景中的 T 数值存在差一错误。；先验答案识别了 θ 与 T 的差一关系，这一点正确；但若直接沿用题面背景所列 T=128 又同时称128为最大不可表示数，就会自相矛盾，故本筛查明确统一约定。
- 时间记账：所在批次墙钟时间按题数均摊约 66.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/345)；既有候选答案（按不可信材料审计）

### #346

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{1\leq a_1< a_2<\cdots\}$ be a set of integers such that {UL} {LI} $A\backslash B$ is complete for any finite subset $B$ and {/LI} {LI} $A\backslash B$ is not complete for any infinite subset $B$.{/LI} {/UL} (Here 'complete' means all sufficiently large integers can be written as a sum of distinct members of the sequence.) Is it true that if $a_{n+1}/a_n \geq 1+\epsilon$ for some $\epsilon>0$ and all $n$ then\[\lim_n \frac{a_{n+1}}{a_n}=\frac{1+\sqrt{5}}{2}?\]
- 题意摘要：量词为：对严格递增正整数序列 A=(a_n)，若对每个有限 B⊂A，A\B 都能表示所有充分大整数；对每个无限 B⊂A，A\B 都不完整；且存在 ε>0 使所有 n 都有 a_{n+1}/a_n≥1+ε，是否必有该比值收敛到 φ=(1+√5)/2？
- 状态核对：截至官网最近记录仍为开放题。先前候选只报告状态和 Fibonacci 启发，没有形成证明。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：采用“子集和间隙”路线。固定有限删除集 B，将剩余项递增写成 b_1<b_2<⋯。若无穷多个 k 满足 b_{k+1}>1+∑_{i≤k}b_i，则整数 1+∑_{i≤k}b_i 无法由剩余项表示，且趋于无穷，和完整性矛盾。然后尝试把这一必要条件与统一比值下界结合，并寻找当比值长期偏离 φ 时仍可无限稀疏删除而保持完整的构造。
- 局部结论：删除任意有限前缀后仍完整，故每一尾序列都完整。；对每个固定尾起点 r，充分大的 k 必有 a_{k+1}≤1+∑_{i=r}^k a_i；否则产生无穷多个明确的不可表示整数。；由 a_{j+1}≥(1+ε)a_j 得 ∑_{i=r}^k a_i≤a_k(1+(1+ε)^{-1}+⋯)<a_k(1+ε)/ε，因此可严格推出 limsup a_{k+1}/a_k≤(1+ε)/ε，但这远弱于 φ。
- 第一阻塞点：第一处缺口是：当比值不趋于 φ 时，如何从偏离比值中选出一个固定的无限删除集 B，同时证明 A\B 仍完整。逐点的子集和间隙不等式只控制全部前项之和，不能保证删除后的表示区间仍重叠。
- 下一步：检验一个明确的稀疏删除引理：若某个 δ>0 下有无穷多个 k 满足 a_{k+1}≤a_k+a_{k-1}−δa_{k-1}，能否从这些 k 中抽取无限 B，使删除 B 后所有充分大的相邻子集和区间仍重叠。证明或反驳该引理会直接测试“低于 φ”方向。
- 来源核对：官网仍标 OPEN，并记录 Graham 序列及 φ 阈值背景：[Erdős Problem 346](https://www.erdosproblems.com/346)。；本地 Lean 文件的主命题仍含 answer(sorry)，不能视为证明；其中若干 variants 也只是带 sorry 的接口声明。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/346)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/346.lean`；既有候选答案（按不可信材料审计）

### #347

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is there a sequence $A=\{a_1\leq a_2\leq \cdots\}$ of integers with\[\lim \frac{a_{n+1}}{a_n}=2\]such that\[P(A')= \left\{\sum_{n\in B}n : B\subseteq A'\textrm{ finite }\right\}\]has density $1$ for every cofinite subsequence $A'$ of $A$?
- 题意摘要：要求存在单调整数序列 a_n，使 a_{n+1}/a_n→2，并且对每个余有限指标集 I⊂N，由 {a_i:i∈I} 的有限子集和组成的集合具有自然密度 1。这里结论仅要求密度 1，不要求包含所有充分大整数。
- 状态核对：已肯定解决并经 Lean 验证。输入中的先前候选已过时：它在 2026-01-16 称开放，但完整构造于 2026-01-21 提交，随后状态更新为 PROVED (LEAN)。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建分块构造：第 n 块取 M_n,2M_n,…,2^{k_n-2}M_n，以及修正项 (2^{k_n-1}−1)M_n+1，其中 k_n 缓慢趋于无穷，M_{n+1}约为(2^{k_n}−3/2)M_n。普通块数字给出近似进位制展开；末项的 +1 用来逐单位修正余数。
- 局部结论：固定块的子集和包含两串 jM_n 与 jM_n+1；在临界数字 c_n=(2^{k_n-1}−1)M_n 处可把 c_n 替换为 c_n+1。；因为 k_n→∞ 且 M_n→∞，块内相邻比值及跨块比值都趋于 2。；删除有限项后仍保留某处以后的所有完整块；缺少足够多可修正数字的展开数量至多由多项式因子乘 (2^{k_n}−2)^{块数} 控制，相对总尺度趋于 0，故异常整数密度为 0。
- 第一阻塞点：该路线已经闭合。若只依据简短非形式说明，第一项需要外部证明补足的是：当 k_n 缓慢变化时，近似展开算法与异常计数在全部块边界上保持一致；现有 Lean 证明正是核验这些账目。
- 下一步：复核正式构造中 k_n、M_n 的精确定义，并将“异常数/o(M_N)”估计抽成独立引理，以便确认自然密度而非仅沿块端点的子序列密度。
- 来源核对：官网明确标为肯定解决且 Lean 验证：[Erdős Problem 347](https://www.erdosproblems.com/347)。；讨论页给出分块构造、计数框架及人工复核记录：[347 discussion](https://www.erdosproblems.com/forum/thread/347)。；本地形式化声明与官网量词基本一致；仓库文件中的 sorry 是汇总库占位，实际证明由 formal_proof 链接指向外部可编译文件。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/347)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/347.lean`；既有候选答案（按不可信材料审计）

### #348

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For what values of $0\leq m<n$ is there a complete sequence $A=\{a_1\leq a_2\leq \cdots\}$ of integers such that {UL} {LI} $A$ remains complete after removing any $m$ elements, but {/LI} {LI} $A$ is not complete after removing any $n$ elements? {/LI} {/UL}
- 题意摘要：对每对整数 0≤m<n，问是否存在一个非降整数序列 A，使删除任意恰好 m 个项后仍能表示所有充分大整数，而删除任意恰好 n 个项后都不能表示所有充分大整数。重复项应按序列中的不同出现位置处理。
- 状态核对：弱完整性版本仍开放；已知 m=0、m=1 的全部后继情形可由经典例子和单调性得到，而 (2,3) 尚未知。强版本 P(A)=N 对 m≥2 已知不存在。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先严格核验 powers-of-two 与 Fibonacci 两个构造，再利用删除的单调性扩展 n。先前候选关于 2^k 被删后仅指出单个缺失数，这不足以证明“不完整”；需改为构造无穷多个缺失数。
- 局部结论：对 A={1,2,4,…} 删除 2^j 后，所有同余于 2^j mod 2^{j+1} 的正整数都不可表示：较小幂之和至多 2^j−1，较大幂均被 2^{j+1} 整除。因此 (m,n)=(0,n) 对所有 n≥1 成立。；Fibonacci 序列删除一个 F_j 后仍满足区间覆盖判据 b_{r+1}≤1+∑_{i≤r}b_i，故仍完整。；删除 F_i,F_j（i<j）后，F_{j+1+2r}−1 对所有 r≥0 均不可表示：基例由较小可用项总和不足得到；归纳时任何表示都必须使用 F_{k-1}，减去它便回到 F_{k-2}−1。因此 (1,n) 对所有 n≥2 成立。
- 第一阻塞点：第一处开放缺口出现在 m=2：需要让每次删除任意两项后只造成有限缺口，却保证任意三项删除造成无穷缺口。简单的区间覆盖判据对这一精确“删除阈值”没有足够分辨率。
- 下一步：针对 (2,3) 建立有限状态搜索：以缺口量 d_k=a_{k+1}−1−∑_{i≤k}a_i 及删除一个、两个最大前项后的对应缺口为状态，枚举可周期延拓的递推模板；任何候选再证明其两删状态最终恢复、三删状态产生无穷缺口。
- 来源核对：官网确认弱版本开放、(2,3) 未知及强版本否定结果：[Erdős Problem 348](https://www.erdosproblems.com/348)。；本地 Lean 表述用把被删指标更新为 0 来模拟删除；因 range 会压缩重复值，它未完全忠实表达原序列的重数语义，不能据此解决原分类。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/348)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/348.lean`；既有候选答案（按不可信材料审计）

### #349

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For what values of $t,\alpha \in (0,\infty)$ is the sequence $\lfloor t\alpha^n\rfloor$ complete (that is, all sufficiently large integers are the sum of distinct integers of the form $\lfloor t\alpha^n\rfloor$)?
- 题意摘要：对每个 t,α>0，令 S={⌊tα^n⌋:n∈N}；问哪些参数使 S 的有限、互异数值子集和包含所有充分大整数。按题面“distinct integers”与本地 Lean 的 range-set 解释，重复数值只能使用一次。
- 状态核对：完整分类仍开放。先前候选把 α=1 时无限重复的 1 当作可重复使用，和题面的“互异整数”及 Lean 的集合语义冲突；因此其“⌊t⌋=1 时完整”结论错误。候选给出的若干精确分段条件仅来自评论，未在本次筛查中独立核实。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：使用增长间隙判据处理边界区间，再尝试把 1<α<2 化为相邻有限子集和区间重叠问题。
- 局部结论：若 0<α<1，则 ⌊tα^n⌋ 最终为 0，S 有限；若 α=1，S={⌊t⌋} 仍有限。因此按互异数值约定，所有 α≤1 都不完整。；若 α>2，则 ∑_{i<n}⌊tα^i⌋≤t(α^n−1)/(α−1)，而 ⌊tα^n⌋与此前总和之差趋于无穷；故出现无穷多个不可填补间隙，序列不完整。；对 1<α<2，渐近上下一项小于此前项总和，即粗增长障碍消失；但这只是必要的区间重叠尺度，不保证实际子集和形成连续区间。
- 第一阻塞点：第一处无法闭合之处是从“下一项小于此前总和”提升到“此前子集和含有足够长的连续整数区间”。取整序列的奇偶及更一般剩余类分布无法控制；这也解释了 α=3/2 的已知困难。
- 下一步：固定 α=3/2，计算前 N 项在各模数 q≤Q 下的取值及可达子集和，并检验是否存在持久的模障碍；若无障碍，再尝试证明某个有限窗口的子集和包含长度超过下一项的连续区间。
- 来源核对：官网仍标 OPEN，并明确指出 1<α<φ 的核心猜想及 ⌊(3/2)^n⌋ 奇偶障碍：[Erdős Problem 349](https://www.erdosproblems.com/349)。；本地 Lean 定义使用 Set.range，确认重复值按集合压缩；这与先前候选的 α=1 论证不相容。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/349)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/349.lean`；既有候选答案（按不可信材料审计）

### #351

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $p(x)\in \mathbb{Q}[x]$. Is it true that\[A=\{ p(n)+1/n : n\in \mathbb{N}\}\]is strongly complete, in the sense that, for any finite set $B$,\[\left\{\sum_{n\in X}n : X\subseteq A\backslash B\textrm{ finite }\right\}\]contains all sufficiently large integers?
- 题意摘要：输入的字面命题量化所有 p∈Q[x]，未限制次数或首项系数；但当前已解决的官方版本量化所有非常数、正首项系数的有理多项式 p，并要求对每个有限 B⊂A，A\B 的有限互异元素和包含所有充分大整数。
- 状态核对：冻结输入内部不一致：current_status=proved (Lean) 对应后来修正的“非常数且正首项系数”版本，而 exact_statement 漏掉该假设。字面输入命题为假；修正版已肯定解决并经 Lean 验证。先前候选的 p=−x 反例适用于字面旧题，但其“加入正性后仍开放”已过时。
- 初步判定：`malformed`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：先审查字面命题：取 p(x)=−x。再重建修正版路线：把目标整数表示转化为同时满足 ∑1/n_i=1 与 ∑p(n_i)=M−1 的问题，并调用问题 283 的正首项多项式单位分数分拆定理；有限删除通过要求所有 n_i 超过给定阈值吸收。
- 局部结论：对 p(x)=−x，p(n)+1/n≤0（n≥1），故任何有限子集和都≤0；字面 exact_statement 因而有严格反例。；修正版中，若找到互异 n_i 使 ∑1/n_i=1 且 ∑p(n_i)=M−1，则立即有 ∑(p(n_i)+1/n_i)=M。；任意有限 B⊂A 只对应有限多个相关指标/数值；强化的单位分数分拆定理允许把所用 n_i 推到任意给定下界之外，因而得到 strong completeness。
- 第一阻塞点：字面命题已被反例闭合。对修正版的有限重建中，首个未在此重新证明的步骤是问题 283 的强化形式：它必须同时处理有理系数的分母/固定除数、指定目标同余类，并允许所有分母避开任意有限集合；现有 Lean 证明核验了这一归约。
- 下一步：修正 cohort 的 exact_statement，加入 0<natDegree(p) 与 leadingCoeff(p)>0，并把本地旧快照更新到带 formal_proof 链接的 2026-05 版本；随后逐项比对 351 证明调用的 283 强化定理是否确实含“避开有限集合”量词。
- 来源核对：当前官网题面明确含正首项系数，并标 PROVED (LEAN)：[Erdős Problem 351](https://www.erdosproblems.com/351)。；讨论页记录了旧题被 p=−x 反驳以及随后修正题面的经过：[351 discussion](https://www.erdosproblems.com/forum/thread/351)。；问题 283 已有更强的正解并经 Lean 验证：[Erdős Problem 283](https://www.erdosproblems.com/283)。；线上 formal-conjectures 主分支的 351 声明已改为 solved，并量化非常数正首项系数多项式；本地冻结文件仍是较旧的 open/sorry 版本。
- 时间记账：所在批次墙钟时间按题数均摊约 45.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/351)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/351.lean`；既有候选答案（按不可信材料审计）

### #352

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some $c>0$ such that every measurable $A\subseteq \mathbb{R}^2$ of measure $\geq c$ contains the vertices of a triangle of area 1?
- 题意摘要：求证是否存在绝对常数 c>0，使每个 Lebesgue 可测集 A⊆R²，只要 |A|≥c，就存在三个点 x,x+u,x+v∈A 满足 |det(u,v)|/2=1。常数须与 A 的形状、有界性和连通性无关。
- 状态核对：截至 2026-01-23 官方仍标为开放。候选答案只罗列了已知结果，没有尝试弥合一般可测集情形。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用三重交相关 C_A(u,v)=∫1_A(x)1_A(x+u)1_A(x+v)dx。先由平移在 L¹ 中连续，寻找 C_A(u,v)>0 的邻域，再试图用 |A| 的下界把该邻域定量扩大到包含 det(u,v)=±2 的参数。
- 局部结论：若 0<|A|<∞，则存在依赖于 A 的 δ>0，使 |u|,|v|<δ 时 C_A(u,v)>0：因为 |A∩(A-u)∩(A-v)|≥|A|-‖1_A(·+u)-1_A‖₁-‖1_A(·+v)-1_A‖₁。；因此每个正测度 A 都包含所有充分小面积的三角形：给定足够小的 η>0，可选小向量 u,v 使 det(u,v)=2η，再由 C_A(u,v)>0 取得共同顶点。；任何可行常数必有 c≥4π/√27：半径 R<2·3^{-3/4} 的圆盘内三角形最大面积为 (3√3/4)R²<1，而圆盘面积可任意逼近 4π/√27。
- 第一阻塞点：L¹ 平移连续性给出的 δ 完全依赖 A；仅由 |A|≥c 无法在这条路线中得到统一的 δ。把大测度分散成许多细小、远隔的碎片时，局部交相关尺度可以任意小。因此不能严格推出存在 det(u,v)=2 的正交相关参数。
- 下一步：检验一个有限尺度替代命题：对固定网格尺度 h，证明或反驳“|A|≥c 强迫某个面积保持仿射像上的三重交相关在 det=2 处为正”；先对有限个凸开集的并建立显式误差界，再考察该界是否随凸块数恶化。
- 来源核对：[官方题页：状态及已知凸集、无界集结果](https://www.erdosproblems.com/352)
- 时间记账：所在批次墙钟时间按题数均摊约 61.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/352)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/352.lean`；既有候选答案（按不可信材料审计）

### #354

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha,\beta\in \mathbb{R}_{>0}$ such that $\alpha/\beta$ is irrational. Is the multiset\[\{ \lfloor \alpha\rfloor,\lfloor 2\alpha\rfloor,\lfloor 4\alpha\rfloor,\ldots\}\cup \{ \lfloor \beta\rfloor,\lfloor 2\beta\rfloor,\lfloor 4\beta\rfloor,\ldots\}\]complete? That is, can all sufficiently large natural numbers $n$ be written as\[n=\sum_{s\in S}\lfloor 2^s\alpha\rfloor+\sum_{t\in T}\lfloor 2^t\beta\rfloor\]for some finite $S,T\subset \mathbb{N}$? What if $2$ is replaced by some $\gamma\in(1,2)$?
- 题意摘要：对任意 α,β>0 且 α/β∉Q，令 x_s=⌊2^sα⌋、y_s=⌊2^sβ⌋。问是否存在 N，使每个 n≥N 都是两个序列中各项至多使用一次的有限子集和；另问把 2 换成任意给定 γ∈(1,2) 后是否成立。零值项不影响子集和。
- 状态核对：截至 2025-12-01 基数 2 的一般情形及 γ 变体仍开放。候选答案的状态说明基本吻合，但其关于 γ^k 对齐可能构成障碍的说法只是提示，不能视为反例。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：把两个序列合并并递增排列为 c_1≤c_2≤⋯，尝试使用完全序列的区间扩张准则：若已有有限子集和覆盖一段长度至少 c_{j+1} 的连续整数区间，且 c_{j+1}≤1+∑_{i≤j}c_i，则加入 c_{j+1} 后可继续扩张。
- 局部结论：递推式严格成立：x_{s+1}=2x_s+ε_s、y_{s+1}=2y_s+η_s，其中 ε_s,η_s∈{0,1}；它们就是 α、β 小数部分的二进制数字。；合并序列最终满足有很大余量的 Brown 型大小不等式 c_{j+1}≤1+∑_{i≤j}c_i：在每个二进尺度之前，两条几何尾的累计和与下一项同阶，而取整总误差只有 O(j)。；任意充分远尾部的所有项的公因数为 1。否则某个 d≥2 整除两条尾部；由 x_{s+1}-2x_s∈{0,1} 可知这些差最终全为 0，两数遂均为二进有理数，与 α/β 无理矛盾。
- 第一阻塞点：“尾部 gcd=1”加上 c_{j+1}≤1+∑_{i≤j}c_i 并不足以保证完全性；仍需证明某个有限前缀的子集和覆盖足够长的连续区间。模障碍可永久存在，例如 2,3,6,12,24,…满足相同大小条件且 gcd=1，却永远缺少某些模 6 剩余类。当前路线尚不能从两条取整递推的无理错位中排除这种持久模缺口。γ∈(1,2) 时连二进数字递推也消失。
- 下一步：对每个模数 q 建立可计算命题：寻找显式 L(q)，证明前 L(q) 个 x_s,y_s 的子集和覆盖 Z/qZ；先穷举小 q 并尝试用 ε_s、η_s 的不同步递推归纳。随后还需把模覆盖升级为一个长度超过下一项的整数区间。
- 来源核对：[官方题页：开放状态及 Hegyvári 等人的特例](https://www.erdosproblems.com/354)
- 时间记账：所在批次墙钟时间按题数均摊约 61.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/354)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/354.lean`；既有候选答案（按不可信材料审计）

### #357

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1\leq a_1<\cdots <a_k\leq n$ be integers such that all sums of the shape $\sum_{u\leq i\leq v}a_i$ are distinct. Let $f(n)$ be the maximal such $k$. How does $f(n)$ grow? Is $f(n)=o(n)$?
- 题意摘要：在所有严格递增整数列 1≤a_1<⋯<a_k≤n 中，要求每个非空连续区间和 ∑_{i=u}^v a_i 两两不同；f(n) 是最大可能长度 k。问题是确定其增长阶，特别问 f(n)/n→0 是否成立。
- 状态核对：截至 2026-01-12 仍开放。候选答案中的显式下界构造可以严格核对；但其由无限序列低密度断言 liminf f(n)/n=0 的“紧致性”推论没有给出相容嵌套构造，不能采纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：用前缀和 s_0=0、s_j=∑_{i≤j}a_i，把条件化为所有正差 s_j-s_i 两两不同；同时直接核验候选答案提出的末端连续整数构造。
- 局部结论：取 m=⌊√n⌋、L=2m-1，并令 a_i=n-L+i。固定长度 r 的窗口和严格递增。长度 r 的最大和与长度 r+1 的最小和之差满足 min_{r+1}-max_r=n+r²-(r+1)(L-1)≥(r-m+1)²+1>0，故不同长度也不碰撞。于是 f(n)≥2⌊√n⌋-1。；前缀和集合 {s_0,…,s_k} 是一个所有正差互异的 Golomb ruler，且相邻差严格递增并不超过 n。简单计数只给 k(k+1)/2≤s_k≤kn-k(k-1)/2，尺度相消，无法推出 o(n)。；已知的无单调版本上界可直接用于本题，因为严格递增列只是其子类；官方记录因而给出 f(n)≤(2/3-1/512+o(1))n，但仍是线性界。
- 第一阻塞点：第一处缺口是怎样定量利用“Golomb ruler 的相邻间距本身严格递增”。普通差集计数只看到总跨度 O(kn)，与 Θ(k²) 个差恰好允许 k=Θ(n)；现有路线没有产生额外的超二次占用或足够多被迫碰撞。
- 下一步：固定 k,n，把差按窗口长度 r 分层，计算各层在区间 [r(r+1)/2, rn-r(r-1)/2] 内的占用；下一步检验相邻两至三层的能量或模 q 占用是否必有 Ω(k³/n) 次潜在碰撞，并用小规模整数规划搜索最可能的有效 q。
- 来源核对：[官方题页：开放状态、下界及无单调版本上界](https://www.erdosproblems.com/357)
- 时间记账：所在批次墙钟时间按题数均摊约 61.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/357)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/357.lean`；既有候选答案（按不可信材料审计）

### #358

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $A=\{a_1<\cdots\}$ be an infinite sequence of integers. Let $f(n)$ count the number of solutions to\[n=\sum_{u\leq i\leq v}a_i.\]Is there such an $A$ for which $f(n)\to \infty$ as $n\to \infty$? Or even where $f(n)\geq 2$ for all large $n$?
- 题意摘要：求一个无限严格递增正整数序列 A={a_1<a_2<⋯}，使每个充分大的 n 作为某段连续项 a_u+⋯+a_v 的表示数 f(n)趋于无穷；较弱问题只要求最终 f(n)≥2。
- 状态核对：此题已于 2026-04-01 标为肯定解决。旧候选答案称其仍开放，已被 2026 年 Tao 的构造明确推翻，不能沿用。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 Tao 的概率构造：先取每个整数独立以概率 1/2 入选的随机集 A_0；在不同二进块中保留随机“红块”，其连续元素和处理典型 n；再为红表示不足的稀疏异常 n，在互不相交的“蓝块”短区间中加入确定选出的元素。素数长度及互素条件用于避免不同修补区间碰撞。
- 局部结论：若 I_{n,q}=[n/q-2q,n/q+2q]∩N，则其中存在 q 个互异整数之和恰为 n：q 元子集和从最小值到最大值逐一覆盖所有中间整数。；把 A_0 看作更新过程，其相邻间距是独立几何分布。Tao 的局部极限定理估计给出：一个合格红区间恰由 q 个连续随机元素表示 n 的概率 ≫1/q。；对互不相交的合格区间应用独立性和 Chernoff 界；再以素数长度和互素限制分配蓝色修补，可得 P(r_A(n)<c log n)≪n^{-2}。求和并用 Borel–Cantelli，存在确定 A 使所有充分大 n 满足 r_A(n)≫log n，故原问题两种要求均成立。
- 第一阻塞点：已知证明本身没有开放缺口。本次受限核查中未逐行复算的最精细环节是局部极限定理的 Fourier 误差估计，以及蓝区间碰撞引理中由有理数极小推出其为零的参数层级；论文给出了这些闭合步骤。值得注意的是论文还明确指出早先由其他模型参与生成的若干声称证明并不完整。
- 下一步：若要完成独立审稿，应逐行核验论文 Proposition 3.1 的一致局部极限定理常数，以及 Lemma 2.4(d)、Proposition 2.2(ii) 的所有指数不等式；这是证明中最可能隐藏参数依赖错误的两处。
- 来源核对：[官方题页：PROVED 及 Tao 构造链接](https://www.erdosproblems.com/358)；[Tao 2026 论文：定理 r_A(n)≫log n](https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos-358-2.pdf)
- 时间记账：所在批次墙钟时间按题数均摊约 61.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/358)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/358.lean`；既有候选答案（按不可信材料审计）

### #359

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1<a_2<\cdots$ be an infinite sequence of integers such that $a_1=n$ and $a_{i+1}$ is the least integer which is not a sum of consecutive earlier $a_j$s. What can be said about the density of this sequence? In particular, in the case $n=1$, can one prove that $a_k/k\to \infty$ and $a_k/k^{1+c}\to 0$ for any $c>0$?
- 题意摘要：给定首项 a_1=n，并要求序列递增；每一步取大于 a_i 的、不能表示为此前某个连续段 a_u+⋯+a_v 的最小整数。问其密度。特别在 n=1 时，是否同时有 a_k/k→∞，以及对每个固定 c>0 都有 a_k/k^{1+c}→0。
- 状态核对：截至 2025-12-28 仍开放。n=1 时规则等价于取此前连续段和集合的最小正缺失数；候选答案正确区分了 Porubský 的“无穷多个 k”上界和全极限。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 s_0=0、s_j=∑_{i≤j}a_i；此前连续段和正是差集 {s_v-s_{u-1}}。利用 greedy mex 性质计数缺失数之前必须出现多少个不同差。
- 局部结论：在 n=1 情形，a_{k+1} 是 k 个已有项的连续段和集合的最小正缺失数，故每个 1≤m<a_{k+1} 都必须是某个 s_v-s_{u-1}。；k 个项只有 k(k+1)/2 个连续区间，因而 a_{k+1}-1≤k(k+1)/2，即 a_k≤k(k-1)/2+1。于是可严格推出 a_k/k^{1+c}→0 对所有 c>1，但远未达到题目要求的每个 c>0。；同一计数反向说明：若要证明 a_k/k→∞，必须证明连续段和在初始区间内存在大量重复或空洞；单纯计算区间数无法超越平凡下界 a_k≥k。
- 第一阻塞点：mex 性质只保证 [1,a_{k+1}) 被差集覆盖，却没有控制这些数的表示重数。要把二次上界降到 k^{1+o(1)}，需证明 k(k+1)/2 个区间中绝大多数和落在已覆盖区或彼此重复；目前没有这种结构性重数下界。反方向 a_k/k→∞ 同样需要排除正密度 greedy 轨道，计数不足。
- 下一步：精确计算前若干千项，并按长度 r 统计差值 s_{j+r}-s_j 的重复能量 E_k=∑_m r_k(m)^2；检验能否证明 E_k≥k^{3-o(1)}。若成立，Cauchy–Schwarz 可把不同连续和数压到 k^{1+o(1)}，从而接近所需上界。
- 来源核对：[官方题页：开放状态、Andrews 猜想及 Porubský 结果](https://www.erdosproblems.com/359)
- 时间记账：所在批次墙钟时间按题数均摊约 61.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/359)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/359.lean`；既有候选答案（按不可信材料审计）

### #361

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c>0$ and $n$ be some large integer. What is the size of the largest $A\subseteq \{1,\ldots,\lfloor cn\rfloor\}$ such that $n$ is not a sum of a subset of $A$? Does this depend on $n$ in an irregular way?
- 题意摘要：固定实数 c>0。对每个充分大的整数 n，令 m=⌊cn⌋，定义 F_c(n)=max{|A|:A⊆[m]，且不存在 B⊆A 使 ∑_{b∈B}b=n}。问题要求确定 F_c(n) 的规模，并判断其对 n 的依赖是否有算术性波动。
- 状态核对：开放。候选答案中 c≥1 的精确公式正确；但其关于 c<1“已经显示不规则性”的数值和文献性断言未由官方页面支持。此外，本地 Lean 文件并未正确形式化原题：它只要求 A 自身的总和不等于 n，而非 A 的每个子集总和都不等于 n；且 hA 中的 c 被重新量化。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先用互补对 {x,n−x} 做禁配计数，再加入整除模障碍。若 m≥n，所有大于 n 的数均可自由加入；在 [n] 中排除 n，并从每个真正的二元互补对至多取一个，而偶数情形的 n/2 可取一次。若 m<n，则在区间 [n−m,m] 上保留同样的互补对约束；作为下界，选择 A={a≤m:q|a}，其中 q∤n。
- 局部结论：当 c≥1（因而 m≥n）时可严格得到 F_c(n)=m−⌈n/2⌉。下界取 A=[⌈n/2⌉,n−1]∪[n+1,m]；上界由互补对计数给出。；当 m>n/2 时，仅用二项子集已给出 F_c(n)≤m−⌊(2m−n+1)/2⌋；当 m≤n/2 时该互补对界没有损失。；对任意整数 q≥2 且 q∤n，倍数集给出 F_c(n)≥⌊m/q⌋。这是严格的算术依赖下界，但本身不能证明最优值发生不规则波动。
- 第一阻塞点：在 c<1 时，互补对只排除了二项表示；要把三项及更长子集和约束合并成匹配的上界，当前路线缺少结构定理。模构造的跳变也不能推出极值 F_c(n) 必然跳变。
- 下一步：固定一个具体区间（优先 c=3/4），用可验证的整数规划计算一段 F_c(n)，同时按 n 对小模数的余数分类；检验极值集是否总可压缩为“模类＋大尾部”的形状。
- 来源核对：官方页面仍标为开放，且未列出已认领的部分解：https://www.erdosproblems.com/361；已直接检查本地 FormalConjectures/ErdosProblems/361.lean；其中 filter 条件是 n≠∑_{a∈B}a，不能表达“B 的所有子集均避开 n”。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/361)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/361.lean`；既有候选答案（按不可信材料审计）

### #365

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Do all pairs of consecutive powerful numbers $n$ and $n+1$ come from solutions to Pell equations? In other words, must either $n$ or $n+1$ be a square? Is the number of such $n\leq x$ bounded by $(\log x)^{O(1)}$?
- 题意摘要：强数指每个整除它的素数都至少以二次幂出现。第一问量化为：是否每个满足 n、n+1 均为强数的整数 n，都有 n 或 n+1 为完全平方？第二问令 S(x)=#{n≤x:n,n+1 均为强数}，问是否存在常数 C 使 S(x)≪(log x)^C。
- 状态核对：第一问已有否定答案且有无穷反例；第二问仍开放。因此整题的 open 标签指计数问题，不能把显式反例误报为整题解决。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：重建 Walker 路线：若 7^3x^2=3^3y^2+1，则 N=3^3y^2 与 N+1=7^3x^2 连续且均为强数。再尝试把该方程化为广义 Pell 方程，并用固定二次域单位生成解。计数方面，每个固定 Pell 族的解按指数增长。
- 局部结论：12167=23^3，12168=2^3·3^2·13^2，二者均为强数且都不是平方，已严格否定第一问。；在 Walker 方程的任一整数解中，3∤x 且 7∤y；所以 3^3y^2 与 7^3x^2 的相关素数指数确为奇数，两个数都不是平方。；任一具有非平凡初始解并由固定基本单位迭代的 Pell 族，其成员大小指数增长，因而在 x 以下贡献 ≍log x 个连续强数对；故 polylog 上界若成立，指数不可能小于 1。
- 第一阻塞点：从一个解严格生成无穷多个仍满足所需整除同余的 Walker 方程解，需要核对单位作用保存的同余类；即使完成，也只给出下界，完全没有控制所有可能的平方自由核组合，因而不能证明 S(x) 的 polylog 上界。
- 下一步：写出 7U^2−3V^2=1 的最小适用解及范数为 1 的基本单位，逐项验证递推保持 U≡0 (mod 7)、V≡0 (mod 3)，从而完整重建 Walker 的无穷反例族。
- 来源核对：官方页面明确记录 Golomb 反例及 Walker 的无穷反例方程，同时仍将计数问题列为开放：https://www.erdosproblems.com/365；候选答案所说“每对都能写成系数随该对变化的广义 Pell 方程”在代数上成立，但这是重编码，不解决固定 Pell 族分类或计数问题。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/365)；既有候选答案（按不可信材料审计）

### #367

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $B_2(n)$ be the 2-full part of $n$ (that is, $B_2(n)=n/n'$ where $n'$ is the product of all primes that divide $n$ exactly once). Is it true that, for every fixed $k\geq 1$,\[\prod_{n\leq m<n+k}B_2(m) \ll n^{2+o(1)}?\]Or perhaps even $\ll_k n^2$?
- 题意摘要：固定整数 k≥1。对整数 t，B_2(t) 是由所有指数至少为 2 的素数幂组成的因子。问是否对 n→∞ 有 ∏_{i=0}^{k−1}B_2(n+i)≤n^{2+o(1)}；更强地，是否存在只依赖 k 的常数 C_k，使该积≤C_kn^2。
- 状态核对：n^{2+o(1)} 仍开放。O_k(n^2) 对 k≤2 成立，但对每个 k≥3 已知为假；官方页面记录 k=3 时无穷多次达到 ≫n^2log n。候选答案给出的具体 Pell 指标未独立核实，故不复述为证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试利用短区间整数的互素性。记 Q_i=B_2(n+i)。由于 Q_i|n+i，任意 i≠j 有 gcd(Q_i,Q_j)||i−j|；因此大于 k 的素数不可能同时出现在两个 Q_i 中。再把 n+i=Q_iR_i，其中 R_i 平方自由且 gcd(Q_i,R_i)=1，试图由 Q_iR_i−Q_jR_j=i−j 控制所有 Q_i 的乘积。
- 局部结论：k=1 时 B_2(n)≤n；k=2 时 B_2(n)B_2(n+1)≤n(n+1)=O(n^2)。；对 0≤i<j<k，gcd(B_2(n+i),B_2(n+j))整除 j−i；所以各 B_2 的共同大素因子完全被排除，重叠只可能来自依赖 k 的有限小素数。；官方已知的 k=3 下界 ≫n^2log n 自动延伸到所有 k≥3，因为额外因子 B_2(n+i)≥1；它否定 O_k(n^2)，但仍与 n^{2+o(1)} 相容。
- 第一阻塞点：“大素因子互不重叠”并不限制它们分别在不同 Q_i 中很大；方程 Q_iR_i−Q_jR_j=i−j 是一组同时的广义 Pell/Thue 型关系，当前没有统一到 n^{o(1)} 损失的高度界。这正是从平凡 n^k 降到 n^{2+o(1)} 的第一处缺口。
- 下一步：先做 k=3 的可检验子命题：在剔除所有 p≤k 的固定因子后，证明或反驳三个两两互素的 powerful 部分之积≤n^{2+o(1)}；同时从官方评论原文逐式核验 ≫n^2log n 的 Pell 构造。
- 来源核对：官方页面确认开放主界、k≤2 的平凡界以及 k≥3 的反例下界：https://www.erdosproblems.com/367；未把候选答案中 j_t=(3·5^{t−1}−1)/2 等未经原始证明核验的细节当作已证事实。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/367)；既有候选答案（按不可信材料审计）

### #368

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：How large is the largest prime factor of $n(n+1)$?
- 题意摘要：令 F(n)=P^+(n(n+1))=max(P^+(n),P^+(n+1))。问题寻求对每个大 n 的统一下界及无穷子序列上的小值规模；官方猜测的自然尺度约为 (log n)^2。
- 状态核对：开放。已知 F(n)→∞；当前官方页面列出的统一下界是 F(n)≫(log log n)^2/log log log n，并记录 Schinzel 的无穷小值子序列。
- 初步判定：`promising`；证明尝试：`known_theorem`；可行性 `5/10`；置信度 `high`
- 尝试路线：从 S-unit 方程入手。若 F(n)≤y，则 n 和 n+1 的所有素因子都属于 S={p:p≤y}，于是 (n+1)−n=1 是同一有限素数集上的 S-unit 方程。固定 y 时应用 S-unit 方程有限性，可排除 F(n) 有界；再尝试让 y 随 n 增长并量化解的高度。
- 局部结论：因 gcd(n,n+1)=1，F(n)=max(P^+(n),P^+(n+1))，且两边使用的素数集合不相交。；对任意固定 y，满足 F(n)≤y 的 n 只有有限多个；因此 S-unit 有限性路线可恢复定性结论 F(n)→∞。；Pasten 的已知定理给出 F(n)≫(log log n)^2/log log log n；这比上述纯定性路线强，但距离猜测的 (log n)^2 仍很远。
- 第一阻塞点：标准 S-unit 有限性对随 y 增长的素数集不提供足够均匀的高度界；已有显式界对 |S|=π(y) 的依赖过大，无法反演出接近 (log n)^2 的统一下界。
- 下一步：把 Pasten 关于 P^+(xy(x+y)) 的定理专门代入 x=1、y=n，逐项核对其高度、互素和常数条件，得到一份完全可追踪的现有最佳下界推导。
- 来源核对：官方页面列出 Pólya、Mahler、Schinzel 与 Pasten 的界，并保持开放状态：https://www.erdosproblems.com/368；候选答案中的代入应写成 xy(x+y)=n(n+1)；其夹杂的“xy$x+y$”只是排版错误，不影响代数代入。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/368)；既有候选答案（按不可信材料审计）

### #369

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$ and $k\geq 2$. Is it true that, for all sufficiently large $n$, there is a sequence of $k$ consecutive integers in $\{1,\ldots,n\}$ all of which are $n^\epsilon$-smooth?
- 题意摘要：严格按字面量词：对每个 ε>0 和整数 k≥2，存在 N=N(ε,k)，使每个整数 n≥N 都包含某个 k 个连续整数组成的集合 P⊆{1,…,n}，且 P 中每个数的最大素因子不超过 n^ε。
- 状态核对：字面命题已解决且是初等事实。人工评审指出候选答案没有处理隐含的额外约束；应明确区分：初等证明只证明原文，不能冒充对“每项 m^ε-smooth”或“区间靠近 n”等意图版本的证明。官方页面目前还记录了这些强化版本的额外结果。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：取固定区块 P={1,…,k}。令 N=⌈max(k,k^{1/ε})⌉。对 n≥N 以及任意 1≤m≤k，每个素因子 p|m 都满足 p≤m≤k≤n^ε，因此 m 是 n^ε-smooth；同时 P⊆[n]。
- 局部结论：上述选择直接满足全部显式量词，给出原题的完整证明。；阈值 N 只依赖 ε、k，且同一个固定区块 P 对所有 n≥N 都有效。；该证明完全没有说明 P 靠近 n，也没有证明每个 m∈P 是 m^ε-smooth；这些是不同命题，必须另引 Balog–Wooley 或后续结果。
- 第一阻塞点：字面命题没有未闭合步骤。若转向原作者可能意图的强化版，固定初始区块立即失效；需要控制大数附近连续整数的最大素因子，这是候选初等论证无法跨越的第一步。
- 下一步：在 cohort 中把“字面 Lean/初等命题”和两个强化版拆成三个独立条目，并记录各自量词；若核验 Lean 状态，还需定位实际 theorem 文件或构建日志，因为当前官方页面同时显示“PROVED (LEAN)”和“Formalised statement? No”。
- 来源核对：官方页面确认字面命题的初始区块证明，并列出两个非平凡强化及后续近端区间结果：https://www.erdosproblems.com/369；已吸收人工评审：不再把候选答案的字面证明描述为解决所有可能的隐含约束。；当前本地 ErdosProblems 目录未检出 369 的 Lean 文件；这与 cohort 的“proved (Lean)”标签及官网“Formalised statement? No”之间存在需要单独核对的元数据不一致。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/369)；既有候选答案（按不可信材料审计）

### #371

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $P(n)$ denote the largest prime factor of $n$. Show that the set of $n$ with $P(n)<P(n+1)$ has density $1/2$.
- 题意摘要：令 P(n) 为 n 的最大素因子。要求证明自然密度极限 lim_{x→∞} x^{-1}#{n≤x:P(n)<P(n+1)} 存在且等于 1/2；这里不是对数密度，也不是“几乎所有尺度”的结论。
- 状态核对：截至冻结日期仍为开放问题。先前候选正确区分了自然密度与对数密度，但它实际上重建的是 Teräväinen 的已知对数密度定理，不能作为原命题的证明。候选中把两个归一化变量都除以 log n 时，第二个变量并不与原比较完全等价：P(n)<P(n+1) 对应 X_n<Y_n 尚可，但若使用文献中以 log(n+1) 归一化的变量，则必须单独控制边界误差。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：尝试把问题归约为连续极限下的二元 friable 分布。设 X_n=log P(n)/log n、Y_n=log P(n+1)/log n。若能在普通 Cesàro 平均下证明 (X_n,Y_n) 弱收敛到具有密度 u(x)u(y) 的两个独立同分布变量，则由交换对称性，区域 y>x 的质量为 1/2。可先在矩形 [0,a]×[0,b] 上把所需结论写成相邻整数同时光滑的计数式，再用矩形逼近三角形 y>x。
- 局部结论：对 n≥2，gcd(n,n+1)=1，故 P(n)≠P(n+1)；不存在需要贡献密度的相等情形。；单变量的最大素因子分布由 Dickman 理论控制，因此上述路线缺少的不是边缘分布，而是相邻整数的二元相关控制。；若对所有连续点 a,b∈(0,1) 有 x^{-1}#{n≤x:P(n)≤n^a, P(n+1)≤n^b}→ρ(1/a)ρ(1/b)，则通过有限矩形逼近可严格推出目标密度为 1/2。
- 第一阻塞点：第一处不能闭合的是普通平均下的相邻 friable 指示函数渐近独立性，而且必须对逼近对角线所需的参数范围有足够一致性。现有无条件结果只给出对数平均或几乎所有尺度，不能直接去掉坏尺度。
- 下一步：选定有限网格 0=t_0<…<t_J=1，明确写出只需证明的矩形相关误差；随后检查现有 friable 数 Elliott–Halberstam 型估计究竟在哪个模数范围失效，并量化该范围是否已足以处理固定网格。
- 来源核对：仅依据题面冻结状态和 official_context 核对：自然密度开放，对数密度 1/2 已知，条件于 friable Elliott–Halberstam 可得自然密度。；未把 untrusted_prior_candidate 中对 Teräväinen 定理编号和公式的转述当作独立证明。
- 时间记账：所在批次墙钟时间按题数均摊约 40.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/371)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/371.lean`；既有候选答案（按不可信材料审计）

### #373

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Show that the equation\[n! = a_1!a_2!\cdots a_k!,\]with $n-1>a_1\geq a_2\geq \cdots \geq a_k\geq 2$, has only finitely many solutions.
- 题意摘要：要求证明满足 n! = ∏_{i=1}^k a_i!、n-1>a_1≥…≥a_k≥2 的全部有限整数元组只有有限多个；k 不是预先固定的，也允许不同 a_i 相等。
- 状态核对：截至冻结日期仍开放。先前候选主要陈述开放性及 abc 条件结果，没有尝试无条件路线；其“显式 abc 下恰有四解”的更强归属不在给定官方材料中，故本筛查不采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `high`
- 尝试路线：从素数估值和最大参数局部化入手。把等式改写为 ∏_{j=a_1+1}^n j=∏_{i=2}^k a_i!。先利用大素数估值迫使 a_1 靠近 n，再希望在短区间 (a_1,n] 中选取一个只在左侧出现一次、而右侧无法匹配其估值的素因子。题面给出的已知结果 a_1≥n-(1/log 2+o(1))log log n 正好把左侧压缩为短乘积。
- 局部结论：若存在素数 p∈(a_1,n]，则 p整除 n!，却不整除任何 a_i!，矛盾；因此区间 (a_1,n] 不含素数。；由 v_2(t!)=t-s_2(t) 得到精确恒等式 Σ_i a_i=n-s_2(n)+Σ_i s_2(a_i)，其中 s_2 为二进制数字和；这给出了参数总量与 n 的必要约束。；引用 official_context 中已知的无条件局部化结果，可把任何大解限制到 n-a_1≤(1/log 2+o(1))log log n。
- 第一阻塞点：即使 n-a_1=O(log log n)，仍不能保证短乘积 (a_1+1)…n 含有一个其素数估值无法由若干较小阶乘共同复制的素因子。仅知道 P(n(n-1)) 较大也需要额外估值论证；不能把“有大素因子”直接当成矛盾，因为该素数仍可能小于 a_1。
- 下一步：固定 d=n-a_1，并对每个素数 q>d 写出等式两边的 v_q：左侧是长度 d 区间内 q 的倍数计数，右侧为 Σ_{i≥2}⌊a_i/q⌋（高次项也需保留）。先检验能否在 d=2,3 的情形证明参数有界，再寻找可随 d 统一的估值障碍。
- 来源核对：使用了 official_context 明载的最大参数局部化结果，但未声称重新证明该结果。；没有采纳先前候选关于 Baker 显式 abc 下完整分类的未经题面来源支持的强化陈述。
- 时间记账：所在批次墙钟时间按题数均摊约 40.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/373)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/373.lean`；既有候选答案（按不可信材料审计）

### #374

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $m\in \mathbb{N}$, let $F(m)$ be the minimal $k\geq 2$ (if it exists) such that there are $a_1<\cdots <a_k=m$ with $a_1!\cdots a_k!$ a square. Let $D_k=\{ m : F(m)=k\}$. What is the order of growth of $\lvert D_k\cap\{1,\ldots,n\}\rvert$ for $3\leq k\leq 6$? For example, is it true that $\lvert D_6\cap \{1,\ldots,n\}\rvert \gg n$?
- 题意摘要：对每个正整数 m，在所有严格递增的 2≤k 个整数 a_1<…<a_k=m 中，令 F(m) 为使 ∏a_i! 成为平方的最小 k；若不存在则 F(m) 未定义。D_k={m:F(m)=k}。问题要求确定 3≤k≤6 时 D_k 在 [1,n] 中的增长阶，特别问 D_6 是否具有正下密度。
- 状态核对：截至冻结日期仍开放。先前候选给出了许多精确增长下界和结构性判据，但这些并未出现在 official_context，且没有提供可核验证明；本筛查只保留能够直接重建的部分。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：把每个阶乘映到有限支撑的素数奇偶向量 w(a)=(v_p(a!) mod 2)_p。于是 F(m) 是包含 w(m) 的、由不同下标组成的最短零和集合长度。先构造短零和族，再尝试用奇偶向量排除更短表示，从而得到 D_k 的计数。
- 局部结论：若 m 为素数，则 m 在 m! 中指数为 1，而所有 a_i<m 的阶乘均不含 m，故 F(m) 不存在。；对 m=2t^2且 t≥2，有 2!(m-1)!m!=2m((m-1)!)^2=(2t(m-1)!)^2；三个下标严格递增。又因 m 非平方且题面给出 D_2={s^2:s>1}，故 2t^2∈D_3。于是 |D_3∩[1,n]|≥⌊√(n/2)⌋+O(1)。；一般地，候选集合 {a_1,…,a_k} 可行当且仅当 Σ_j w(a_j)=0；这把搜索和反例检查化为有限域 F_2 上的零和问题。
- 第一阻塞点：构造 F(m)≤6 不足以证明 m∈D_6；必须同时排除所有含 m 的 2、3、4、5 元零和集合。当前没有对正密度 m 统一排除这些短关系的结构定理，这正是从构造到 D_6≫n 的第一处断裂。
- 下一步：对 m≤M 递推计算 w(m)=w(m-1)+奇偶分解向量(m)，并用 meet-in-the-middle 精确判定最短含 m 的零和长度；按 m 的平方自由核和小素因子模式分组，寻找一个可证明具有正密度且实验上最短长度恒为 6 的同余类族。
- 来源核对：直接核验了 2t^2 的三阶乘平方恒等式及其严格下标条件。；未采用先前候选中的 D_4=Θ(n)、D_5≫n/log n、D_6≫n/log n、小素数判据和 13q 判据，因为在给定材料中没有足够证明可独立核对。
- 时间记账：所在批次墙钟时间按题数均摊约 40.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/374)；既有候选答案（按不可信材料审计）

### #376

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many $n$ such that $\binom{2n}{n}$ is coprime to $105$?
- 题意摘要：问是否存在无穷多个正整数 n，使 3、5、7 均不整除中央二项式 C(2n,n)，即 gcd(C(2n,n),105)=1。
- 状态核对：截至冻结日期仍开放。先前候选正确给出 Kummer 等价和开放状态，但只列举例子，没有推进证明。
- 初步判定：`promising`；证明尝试：`heuristic_route`；可行性 `6/10`；置信度 `high`
- 尝试路线：采用多基数数字集交集路线。对奇素数 p，定义 A_p(X) 为 [0,X] 内所有 base-p 数字均≤(p-1)/2 的整数。目标是证明 A_3∩A_5∩A_7 无界。拟在共同尺度 X 上用离散 Fourier 展开三个数字集的指示函数：主项由各自密度给出，非零频率项需用数字乘积结构的指数和衰减控制。
- 局部结论：由 Kummer 定理，p∤C(2n,n) 当且仅当 n+n 在 base p 中无进位，等价于每一位数字≤(p-1)/2；因此题面所列三组数字限制完全等价于原问题。；对完整区间 0≤n<p^r，满足 base-p 限制的整数恰有 ((p+1)/2)^r 个。；独立性启发下，三集合交集到 X 的预期幂指数为 log_3 2+log_5 3+log_7 4-2≈0.026>0；这不是证明，但说明主项仅以很小的正幂增长，任何误差估计都必须非常尖锐。
- 第一阻塞点：第一处无法闭合的是三个不同基数数字集的非零 Fourier 相关和。单个数字集有乘积公式，但基数 3、5、7 的尺度彼此不对齐；现有两基数方法不能自动给出小于约 X^0.026 的总误差。
- 下一步：在 X=3^r 附近明确写出三重 Fourier 主项与误差，数值计算各频率块的 L^2/L^4 能量；检验是否存在可迭代的频率分区，使大谱的交集维数严格小于主项指数 0.026。
- 来源核对：Kummer 等价可直接重建，无需依赖候选中的网页引文。；候选列出的具体解及 2025年12月、2026年1月状态不属于冻结输入，未用于判断。
- 时间记账：所在批次墙钟时间按题数均摊约 40.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/376)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/376.lean`；既有候选答案（按不可信材料审计）

### #377

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some absolute constant $C>0$ such that\[\sum_{p\leq n}1_{p\nmid \binom{2n}{n}}\frac{1}{p}\leq C\]for all $n$ (where the summation is restricted to primes $p\leq n$)?
- 题意摘要：定义 f(n)=Σ_{p≤n, p∤C(2n,n)}1/p，其中只对素数求和。问题问是否存在与 n 无关的绝对常数 C，使所有正整数 n 都有 f(n)≤C。
- 状态核对：截至冻结日期仍开放。先前候选正确说明平均值和已知 O(log log n) 型最坏界，但没有给出可用于统一界的具体分段论证。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `medium`
- 尝试路线：按 p>√(2n) 与 p≤√(2n) 分割。对大素数写 n=qp+r。由于 q<p/2，此时无进位条件只剩 r≤(p-1)/2；因此对每个 q，贡献素数落在一个很短的乘法区间。尝试用 Brun–Selberg 型短区间素数上界逐段求和。
- 局部结论：Kummer 给出 p∤C(2n,n) 当且仅当 n 的所有 base-p 数字≤(p-1)/2。；若 p>√(2n)、q=⌊n/p⌋，则 q<p/2，且无进位等价于 n-qp≤(p-1)/2；忽略整数端点后，p 位于 (2n/(2q+1), n/q]。；对 1≤q<√(n/2)，上述区间的相对长度约 1/(2q)。用标准筛上界估计其中素数的倒数和为 O(1/(q log(n/q)))，再对 q 求和得到大素数部分 Σ_{√(2n)<p≤n}1_{p∤C(2n,n)}/p=O(1)。
- 第一阻塞点：剩余小素数 p≤√(2n) 的倒数和仍可能达到约 log log n。大素数区间分解不会递归控制这些 p，而平均值与二阶矩信息也不能排除稀有 n 的峰值。这里是统一常数路线的第一处实质障碍。
- 下一步：继续把小素数按 base-p 位数 j 分层，即 n^{1/(j+1)}<p≤n^{1/j}；先对固定 j=2 写出两位无进位条件对应的二维区间，并检验筛上界求和是否仍为 O(1/j^2)。若能得到对 j 可求和的界，才可能闭合全范围。
- 来源核对：平均值、二阶矩及 c log log n 上界仅按 official_context 记录，没有把它们误用为一致有界性。；大素数部分的 O(1) 需要标准的统一短区间筛上界；端点和小 n 可吸收到绝对常数，但完整常数尚未计算。
- 时间记账：所在批次墙钟时间按题数均摊约 40.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/377)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/377.lean`；既有候选答案（按不可信材料审计）

### #380

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：We call an interval $[u,v]$ 'bad' if the greatest prime factor of $\prod_{u\leq m\leq v}m$ occurs with an exponent greater than $1$. Let $B(x)$ count the number of $n\leq x$ which are contained in at least one bad interval. Is it true that\[B(x)\sim \#\{ n\leq x: P(n)^2\mid n\},\]where $P(n)$ is the largest prime factor of $n$?
- 题意摘要：对每个实数 x，令 B(x) 计数所有 n≤x，使得存在整数区间 [u,v]∋n，且区间乘积的最大素因子在乘积中的指数至少为 2。需证明 B(x) 与 S(x)=#{n≤x:P(n)^2∣n} 渐近相等。
- 状态核对：已于 2026 年由 Tao 肯定解决。旧候选称其仍开放，状态判断已经过时；其中结构观察可单独审查，但不能代替新证明。现有定量结论为 B(x)=(1+O((log x)^{-1+o(1)}))S(x)。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 Tao 证明的主干：先按尺度二分坏区间；设其长度为 H、乘积最大素因子为 p。由 H≤N 及 Sylvester–Schur 得 p>H，故 p 只整除区间内一个数，该数为 p²m，且整个区间均为 p-smooth。再把任意坏区间缩成长度可比、以 p²m 为端点且长度为 2 的幂的“规范区间”，利用离散 Hardy–Littlewood 极大不等式控制覆盖损失。最后剔除非典型区间，对典型区间实施反筛、特征和及二阶矩估计，证明非单点坏区间新增的覆盖量为 O((log x)^{-1+o(1)}S(x))。
- 局部结论：单点区间立即给出 S(x)≤B(x)。；在 H≤N 的坏区间中，Sylvester–Schur 给出 p>H；因此 p 的倍数至多一个，而坏性迫使该元素形如 p²m。又因 p 是全乘积的最大素因子，区间内每个整数均为 p-smooth。；取不超过约 H/2 的最大二幂 H′，以 p²m 为左端点或右端点的两个长度 H′ 子区间至少有一个包含于原区间；故可归约到规范区间而仅损失绝对常数级覆盖量。
- 第一阻塞点：本次受限重建首先无法独立闭合的是典型规范区间的二阶矩/反筛估计：它需要控制素数上的 Dirichlet 特征和、排除少数例外特征，并调用 Guth–Maynard 的新零密度估计。旧式 Huxley 界在所需参数范围内不足。此处是已发表预印本中的技术定理，不是问题仍开放。
- 下一步：逐式核验论文 Proposition 6.5–6.8：检查例外特征计数、二阶矩求和及其最终误差是否确实为 O((log x)^{-1+o(1)}S(x))，并核对 v2 修订是否处理了讨论区曾提出的问题。
- 来源核对：[Erdős Problems #380](https://www.erdosproblems.com/380) 已标为 PROVED，并记录定量误差项。；[Tao, Products of consecutive integers with unusual anatomy](https://arxiv.org/abs/2603.27990) 的 Theorem 1.7 明确肯定该渐近式；核查版本为 2026-04-22 的 v2。；论文 Section 6 明示使用 Guth–Maynard 零密度估计，并指出旧 Huxley 估计不足以闭合。
- 时间记账：所在批次墙钟时间按题数均摊约 52.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/380)；既有候选答案（按不可信材料审计）

### #382

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $u\leq v$ be such that the largest prime dividing $\prod_{u\leq m\leq v}m$ appears with exponent at least $2$. Is it true that $v-u=v^{o(1)}$? Can $v-u$ be arbitrarily large?
- 题意摘要：对任意整数 u≤v，若 A=∏_{m=u}^v m 的最大素因子 p 满足 ν_p(A)≥2，问是否对所有这类趋于无穷的区间均有 v−u=v^{o(1)}；另问满足条件的长度 v−u 是否无界。
- 状态核对：截至核查仍开放。#380 的新证明明确说明没有推进这里的“所有坏区间都极短”或“长度无界”两问。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：走 Sylvester–Schur与素数间隙路线。令 H=v−u+1。先证明区间不能含素数，因此它落在一个合数间隙中；再用 Bertrand 排除 u≤v/2，并用 Sylvester–Schur锁定最大素因子的唯一倍数。
- 局部结论：ν_p(A)≥2 迫使 p≤v/2：若 p>v/2，则 [1,v] 中唯一的 p 倍数是 p，且 p²>v，只能贡献一次。若 u≤v/2，Bertrand 定理给出 q∈(v/2,v]∩[u,v]，与 p≤v/2 矛盾，故 u>v/2。；令 H=v−u+1。若 u=H，则 [u,2u−1] 含有 Bertrand 素数，矛盾；故 u>H。Sylvester–Schur于是给出 p>H。区间内仅有一个 p 倍数，ν_p(A)≥2 迫使 p²≤v，因此 H<p≤√v，特别地 v−u<√v。；区间事实上不含素数：若含素数 q，则因 u>v/2 有 q>v/2；任何更大的素因子也只能以自身出现于区间，故取区间中最大素数便得到全乘积最大素因子且指数为 1。因而 v−u 不超过包含 [u,v] 的相邻素数间隙长度；若最大素数间隙为 x^{o(1)}，第一问随即成立。
- 第一阻塞点：第一处无法闭合的是把已知无条件素数间隙界加强到 v^{o(1)}；这至少需要类似 Cramér 猜想的统一短区间素数结论。第二问则需构造任意长的连续 p-smooth 块，并使其中某项含 p²，目前没有相应无条件构造。
- 下一步：对给定 H 编写有限搜索，专门寻找素数 p 与区间 [p²,p²+H−1]，检验每项是否 p-smooth；同时把成功率与 (1−log 2)^{H−1} 的启发式预测比较。这只能检验无界性路线，不会证明无穷。
- 来源核对：[Erdős Problems #382](https://www.erdosproblems.com/382) 仍标为 OPEN，并记录 Ramachandra 界及 Cramér 条件路线。；[Tao 2026 论文 Section 6.1](https://arxiv.org/html/2603.27990) 明确称未推进坏区间长度的两项猜想。；Sylvester–Schur 的使用条件已独立检查：H 个连续整数均须严格大于 H；先排除 u=H 后条件成立。
- 时间记账：所在批次墙钟时间按题数均摊约 52.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/382)；既有候选答案（按不可信材料审计）

### #383

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that for every $k$ there are infinitely many primes $p$ such that the largest prime divisor of\[\prod_{0\leq i\leq k}(p^2+i)\]is $p$?
- 题意摘要：量词为：对每个固定整数 k≥0，是否存在无穷多个素数 p，使 P⁺(∏_{i=0}^k(p²+i))=p。这里 p 可依赖于 k，且要求无穷多个，而非每个 k 只找一个见证。
- 状态核对：截至核查仍开放。旧候选正确区分了有限计算与无穷性，但其“任何固定 k≥1 均无已知证明”的断言缺乏原始文献支撑，不在此当作已核定事实。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `medium`
- 尝试路线：将问题严格化为同时光滑性问题，再分析各因子的公共素因子。目标是尝试用筛法证明一批素数 p 同时满足 P⁺(p²+i)≤p。
- 局部结论：因 i=0 项为 p²，目标等价于对每个 1≤i≤k 都有 P⁺(p²+i)≤p；当 p>k 时，p不整除任何 p²+i，因此乘积的最大素因子恰为 p。；若 i≠j，则 gcd(p²+i,p²+j)∣|i−j|≤k。因此大于 k 的素因子不可能在两个不同的平移项中重复；这排除了由共享大素因子造成的相关性，但没有给出所需光滑性。；任一这样的 p 使区间 [p²,p²+k] 满足 #382：所有素因子≤p，而 p²贡献 p 的指数 2，所以最大素因子为 p 且区间长度为 k。故对每个 k 只需一个见证即可推出 #382 长度无界；本题要求的“无穷多个”更强。
- 第一阻塞点：第一处无法闭合的是同时光滑值的下界筛：Dickman 密度只描述一般整数，不能直接用于素数参数上的相关多项式值 p²+1,…,p²+k。现有筛法还不能证明满足全部 P⁺(p²+i)≤p 的素数 p 有正下界，更不能证明无穷。
- 下一步：先攻 k=1：把计数函数 #{p≤X:p为素数且P⁺(p²+1)≤p} 写成按 p²+1 的因子分解求和，检查现有二次多项式光滑值定理是否能在素数参数上给出趋于无穷的下界。
- 来源核对：[Erdős Problems #383](https://www.erdosproblems.com/383) 仍标为 OPEN，并明确只给出 Dickman 型启发式。；官方讨论中的 p=9188057、k≤10 只是有限见证，不能支持“无穷多个”的量词。；旧候选引用的非对称计算样本未作为证明材料使用。
- 时间记账：所在批次墙钟时间按题数均摊约 52.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/383)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/383.lean`；既有候选答案（按不可信材料审计）

### #385

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[F(n) = \max_{\substack{m<n\\ m\textrm{ composite}}} m+p(m),\]where $p(m)$ is the least prime divisor of $m$. Is it true that $F(n)>n$ for all sufficiently large $n$? Does $F(n)-n\to \infty$ as $n\to\infty$?
- 题意摘要：对每个足够大的整数 n，令 F(n) 在所有 m<n 的合数中取 m+p(m) 的最大值，其中 p(m) 是 m 的最小素因子。第一问是否最终恒有 F(n)>n；第二问是更强的逐点极限：对每个 A，是否存在 N(A)，使 n≥N(A) 时 F(n)−n>A。
- 状态核对：两问仍开放。第二问不能由第一问本身推出；旧候选在措辞上仅说会由“足够强版本”推出，这一点需保持区分。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：令 m=n−d，将问题化为在 n 左侧寻找最小素因子足够大的合数；再尝试用短区间半素数筛实现。
- 局部结论：精确恒等式为 F(n)−n=max_{d≥1，n−d为合数}(p(n−d)−d)。因此 F(n)≤n 当且仅当每个合数 n−d 都满足 p(n−d)≤d。；奇数 n≥5 时取 m=n−1 得 F(n)≥n+1；偶数 n≥6 时取 m=n−2 得 F(n)≥n。因此第一问只在偶数上非平凡；若偶数 n 的 n−1 为合数，则取 d=1 已得 F(n)≥n+2，所以潜在反例必须满足 n−1 为素数。；若 d≥√n，则 p(n−d)≤√(n−d)<d；故寻找 F(n)>n 只需考察 d<√n。沿素数 p 的子序列 n=p²+1，取 m=p² 得 F(n)−n≥p−1，严格证明 limsup(F(n)−n)=∞，但不是全极限。
- 第一阻塞点：为得到全极限，需要对每个大 n 找到 d<√n，使 n−d 为合数且 p(n−d)>d+A；自然候选是两个都大于 d+A 的素数之积。证明每个相关短区间都含这类半素数遇到筛法的奇偶障碍，并可能受 Siegel 零造成的最坏情形修正影响。
- 下一步：固定尺度 h，精确估计区间 [n−h,n) 中形如 qr、q,r>h+A 的半素数个数；先在平均 n 意义下验证主项，再定位从平均结论升级到“每个 n”时失效的误差项。
- 来源核对：[Erdős Problems #385](https://www.erdosproblems.com/385) 截至 2026 年仍标为 OPEN。；[Tao 关于 #385 的分析](https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/) 明确解释了奇偶障碍及 Siegel 修正可能抵消主项的机制。；旧候选的奇偶 n 初等界及 p²+1 子序列已逐式复核。
- 时间记账：所在批次墙钟时间按题数均摊约 52.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/385)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/385.lean`；既有候选答案（按不可信材料审计）

### #386

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $2\leq k\leq n-2$. Can $\binom{n}{k}$ be the product of consecutive primes infinitely often? For example\[\binom{21}{2}=2\cdot 3\cdot 5\cdot 7.\]
- 题意摘要：问是否存在无穷多个整数对 (n,k)，满足 2≤k≤n−2，且 binom(n,k) 等于某一段连续素数 q_aq_{a+1}⋯q_b 的乘积。k 允许随 n 变化；固定 k=2 的无穷性只是足以给肯定答案的子问题。
- 状态核对：截至核查仍开放，甚至 k=2 的无穷性未知。已知有限例子不能支持“无限常有”。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先限制到 k=2，将连续素数积记为 Q。由 binom(n,2)=n(n−1)/2=Q 转成平方值问题 8Q+1=(2n−1)²，再尝试研究连续素数块乘积的 Pell 型/指数丢番图方程。
- 局部结论：连续素数的乘积是平方自由数，因此任何解都必须使 binom(n,k) 平方自由；等价地，对每个素数 ℓ 都有 ν_ℓ(binom(n,k))≤1。Kummer 定理将其转为 k 与 n−k 的 ℓ 进制加法至多产生一次进位。；在 k=2 情形，Q=binom(n,2) 当且仅当 8Q+1=(2n−1)²；此外 Q 平方自由迫使 n 与 n−1 除被分母 2 消去的一次 2 因子外均无平方因子。；若 n≥2k，分子中的 k 个连续整数均大于 k；Sylvester–Schur 给出某个素数 r>k 整除分子，因 r不整除 k!，故 r∣binom(n,k)。因此所取连续素数块的右端至少超过 k。
- 第一阻塞点：第一处无法闭合的是证明方程 8(q_a⋯q_b)+1=y² 只有有限或有无限多解。连续素数条件使 Q 的素因子集合没有缺口，但现有平方筛/丢番图方法没有给出足以决定解数的统一估计；一般 k 的平方自由条件同样只是必要条件。
- 下一步：对 k=2 按端点素数 q_b 分层，研究 y²≡1 mod 8q_a⋯q_b 的 CRT 根与大小约束 y²=8Q+1 是否能产生有效间距下界；先检验能否证明固定左端 q_a 时只有有限多个右端。
- 来源核对：[Erdős Problems #386](https://www.erdosproblems.com/386) 仍标为 OPEN，并列出已知例子及 k=2 的 n=4,6,15,21,715。；官方页明确没有评论声称部分或完整解答。；旧候选仅报告计算和例子，没有提供可审查的无穷性论证；本筛查未把计算截止范围当成数学结论。
- 时间记账：所在批次墙钟时间按题数均摊约 52.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/386)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/386.lean`；既有候选答案（按不可信材料审计）

### #387

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Is there an absolute constant $c>0$ such that, for all $1\leq k< n$, the binomial coefficient $\binom{n}{k}$ has a divisor in $(cn,n]$?
- 题意摘要：问是否存在统一的绝对常数 c>0，使每一对整数 1≤k<n 的二项式系数 C(n,k) 都有某个整数因子 d 满足 cn<d≤n。
- 状态核对：2026-07-02 已否定解决。旧候选完全误答成 Erdős #385，其 F(n) 与本题无关，全部弃用。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 BNPZ26 的反例路线：以受限剩余类覆盖消除各单项产生的“大因子”，再用筛法和指数和估计排除多个小因子拼成区间内因子的可能。
- 局部结论：由 C(n,k)=C(n,n−k)，只需处理 1≤k≤n/2。；已知定理给出无穷多组 k≈√(log log n)，使 C(n,k) 在 (ρ(n)n,n] 内没有因子，其中 ρ(n)=log log log log n/log log log n→0。；任给固定 c>0，取上述反例中充分大的 n 使 ρ(n)<c，则 (cn,n]⊂(ρ(n)n,n]；因此 C(n,k) 在 (cn,n] 中也没有因子，严格否定原命题。
- 第一阻塞点：若要求从头重证，首次不能在本次筛查内闭合的是受限覆盖定理以及后续“divisor problem”的筛法、指数和估计；此处依赖 BNPZ26 的主定理。
- 下一步：逐条核对 BNPZ26 v2 主定理中的迭代对数层数、k 的范围及无穷多量词，并追踪正式发表版是否修改参数。
- 来源核对：官方页面于 2026-07-02 标为 solved，并陈述否定性区间：https://www.erdosproblems.com/387；arXiv:2605.21221 v2（2026-06-30）增加 Naprienko，并注明论证已去除 GRH：https://arxiv.org/abs/2605.21221
- 时间记账：所在批次墙钟时间按题数均摊约 41.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/387)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/387.lean`；既有候选答案（按不可信材料审计）

### #388

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Can one classify all solutions of\[\prod_{1\leq i\leq k_1}(m_1+i)=\prod_{1\leq j\leq k_2}(m_2+j)\]where $k_1,k_2>3$ and $m_1+k_1\leq m_2$? Are there only finitely many solutions?
- 题意摘要：按该数论问题的通常约定，变量取正整数：分类所有 k1,k2>3、m1+k1≤m2 且 ∏_{i=1}^{k1}(m1+i)=∏_{j=1}^{k2}(m2+j) 的四元组，并问总数是否有限。
- 状态核对：仍开放。旧候选的负整数反射族在代数上成立，但不适用于默认正整数域；其“仅有四个标准例子”等文献性断言也未获权威来源支持。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：比较两个分离整数块的长度和因子大小，再利用右块素因子必须由左块供给的约束；固定 (k1,k2) 后可化为两上升阶乘多项式取相同值的整数点问题。
- 局部结论：必有 k1>k2：若 k2≥k1，右块前 k1 项逐项严格大于左块对应项，右积已经严格较大。；右块 [m2+1,m2+k2] 不含素数；若其中有素数 p，则 p>m1+k1，故 p 不整除左块任何因子，与两积相等矛盾。；每个解因此产生长度 k2≥4 的全合数区间；但任意固定长度的全合数区间可由阶乘构造无穷多个，所以该条件不足以推出有限性。
- 第一阻塞点：首次缺口是从“右块全合数且素因子均由左块供给”推出 k1、k2 或 m1 的统一上界。固定长度的素数间隙信息不够；固定 (k1,k2) 的代数曲线结论也不能直接对所有长度求和。
- 下一步：对固定 (k1,k2) 计算曲线 (x+1)…(x+k1)=(y+1)…(y+k2) 的无穷远分支和 genus，核查 Runge/Siegel 型定理能否严格给出整数点有限；再检查所得界是否可能对长度统一。
- 来源核对：官方讨论仅提示固定长度对的有限性路线，并明确这不推出全局有限：https://www.erdosproblems.com/forum/thread/388；官方材料未把 m1,m2 扩张为任意整数，故采用正整数约定。
- 时间记账：所在批次墙钟时间按题数均摊约 41.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/388)；既有候选答案（按不可信材料审计）

### #389

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that for every $n\geq 1$ there is a $k$ such that\[n(n+1)\cdots(n+k-1)\mid (n+k)\cdots (n+2k-1)?\]
- 题意摘要：量词为：对每个整数 n≥1，是否存在整数 k≥1，使 A=∏_{i=0}^{k−1}(n+i) 整除紧接其后的 B=∏_{i=0}^{k−1}(n+k+i)。
- 状态核对：仍开放。旧候选的二项式等价式正确，但“标准 Kummer+CRT 路线可以证明存在”的暗示没有完成关键步骤，不能采信。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：将 A∣B 化为所有素数上的估值不等式，逐层分析每个素数幂在两个相邻等长区间中的倍数数目。
- 局部结论：A=k!·C(n+k−1,k)，B=k!·C(n+2k−1,k)，故 A∣B 等价于 C(n+k−1,k)∣C(n+2k−1,k)。；对每个素数 p，v_p(B/A)=Σ_{r≥1}(⌊(n+2k−1)/p^r⌋+⌊(n−1)/p^r⌋−2⌊(n+k−1)/p^r⌋)；原题恰要求所有这些和非负。；若 p^r∣k，则该素数幂层的括号恒为 0；因此令 k 高度可整除确能消除许多局部障碍。
- 第一阻塞点：首次不能闭合的是同时控制所有不整除 k 的素数幂，尤其 p^r>k 时左区间可能含一个倍数而右区间没有。CRT 只能预控有限模数，而危险素数幂集合依赖最终选出的 k 和区间端点。
- 下一步：固定 n，测试 k=lcm(1,…,L)：验证所有 p^r≤L 层确为零，并用精确估值定位首个造成负总和的 p^r>L；检查能否迭代吸收该障碍且保证过程终止。
- 来源核对：官方页面确认问题仍开放，并给出 n=2、3 的实例：https://www.erdosproblems.com/389；未把有限范围计算当作全称命题的证明。
- 时间记账：所在批次墙钟时间按题数均摊约 41.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/389)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/389.lean`；既有候选答案（按不可信材料审计）

### #390

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the minimal $m$ such that\[n! = a_1\cdots a_k\]with $n< a_1<\cdots <a_k=m$. Is there (and what is it) a constant $c$ such that\[f(n)-2n \sim c\frac{n}{\log n}?\]
- 题意摘要：f(n) 是所有表示 n!=a1⋯ak、n<a1<⋯<ak=m 中末项 m 的最小值；问是否存在常数 c，并求 c，使 f(n)−2n∼c n/log n。
- 状态核对：仍开放；已知仅有 f(n)−2n≍n/log n。旧候选声称的显式常数 1/9 和 1.7 未获本次权威来源核实，故不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先用因子个数和大小恢复 2n 主尺度，再识别 n/log n 正修正项必须使用的算术约束。
- 局部结论：每个 ai 的所有素因子都≤n，否则该素数整除右侧乘积却不整除 n!；所以所选因子均为 n-smooth。；区间 (n,m] 最多提供 m−n 个互异整数，且每个不超过 m，故 n!≤m^{m−n}，即 m−n≥log(n!)/log m。；在 m=O(n) 的范围中代入 Stirling 公式，只能得到 m≥2n−O(n/log n)：它恢复了主项 2n，却不能推出已知的正向间隙。
- 第一阻塞点：首次缺口是把“因子互异且必须 n-smooth”量化成 m≥2n+c1 n/log n。纯体积估计的误差方向不够；需要 EGS82 的素因子分配论证。即使得到双边常数界，也仍不能证明归一化量收敛。
- 下一步：重读 EGS82，抽取上下界所用的主导素数区间，写出相应的 liminf/limsup 常数表达式；检验两端是否由同一素数密度泛函控制。
- 来源核对：官方页面确认开放，并记录 EGS82 的 Θ(n/log n) 定理：https://www.erdosproblems.com/390；未找到足够权威材料支持旧候选所报的显式常数。
- 时间记账：所在批次墙钟时间按题数均摊约 41.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/390)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/390.lean`；既有候选答案（按不可信材料审计）

### #393

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ denote the minimal $m\geq 1$ such that\[n! = a_1\cdots a_t\]with $a_1<\cdots <a_t=a_1+m$. What is the behaviour of $f(n)$?
- 题意摘要：对每个 n，在所有互异正整数 a1<⋯<at、乘积为 n! 的表示中，f(n) 是端点宽度 at−a1 的最小正值；问题要求描述其增长和分布行为。
- 状态核对：仍开放；无条件甚至不知道 f(n)=1 是否无穷多次出现。旧候选的有限多项式归约可保留，但须区分“宽度恰为 m”与 f(n)=m。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：固定宽度 m，以端点均被选择的偏移子集编码表示，将问题归约为有限族多项式—阶乘方程。
- 局部结论：存在宽度恰为 m 的表示，等价于存在 x≥1 和 S⊆{0,…,m}，满足 0,m∈S 且 n!=P_S(x):=∏_{s∈S}(x+s)；固定 m 只有 2^{m−1} 个候选多项式。；m=1 时唯一多项式是 P(x)=x(x+1)，故 f(n)=1 必须满足 n!=x(x+1)；最简单情形已触及公开难点。；由固定 m 的 F_m(N)≪_m N^{33/34}，对固定 M 有 #{n≤N:f(n)≤M}=O_M(N^{33/34})，所以 f(n)→∞ 在自然密度意义下成立。
- 第一阻塞点：首次不能无条件闭合的是证明任一固定方程 P_S(x)=n! 只有有限多组整数解。现有计数上界只给稀疏性；Luca 的有限性步骤依赖 ABC，不能升级为无条件的逐点发散。
- 下一步：先研究 m=1：由 gcd(x,x+1)=1，把 n! 中各素数幂分配到相邻两因子，枚举 prime-power blocks 的分拆；检查 S-unit、线性形式或 abc 方法能否至少处理一个可证明的无限参数子族。
- 来源核对：官方页面记录 Berend–Osgood、BPZ23 的稀疏性以及 Luca 在 ABC 下的发散结论：https://www.erdosproblems.com/393；BPZ23 的 N^{33/34} 界不能解释为固定 m 仅出现有限次。
- 时间记账：所在批次墙钟时间按题数均摊约 41.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/393)；既有候选答案（按不可信材料审计）

### #394

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $t_k(n)$ denote the least $m$ such that\[n\mid m(m+1)(m+2)\cdots (m+k-1).\]Is it true that\[\sum_{n\leq x}t_2(n)\ll \frac{x^2}{(\log x)^c}\]for some $c>0$? Is it true that, for $k\geq 2$,\[\sum_{n\leq x}t_{k+1}(n) =o\left(\sum_{n\leq x}t_k(n)\right)?\]
- 题意摘要：令 t_k(n) 为满足 n∣∏_{i=0}^{k-1}(m+i) 的最小正整数 m。问题分别问：(i) 是否存在固定 c>0，使 x→∞ 时 ∑_{n≤x}t_2(n)≪x²/(log x)^c；(ii) 是否对每个固定整数 k≥2 都有 ∑_{n≤x}t_{k+1}(n)=o(∑_{n≤x}t_k(n))。
- 状态核对：截至官方页面 2025-10-28 更新，两问仍开放。已知 Erdős–Hall 上界只有 x²·logloglog x/loglog x。候选答案的开放性判断正确，但没有给出实际归约。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：对 k=2 使用相邻整数互素性。若 n∣m(m+1)，则每个素数幂 p^e∥n 必须完整分配给 m 或 m+1。因此存在互素分解 n=de，使 m≡0 (mod d)、m≡−1 (mod e)；反之每个这种分解都由 CRT 给出一个模 n 的可行剩余类。于是 t_2(n) 等于所有互素分解 n=de 所对应最小正 CRT 解的最小值。尝试通过平均这些模逆元获得对数节省。
- 局部结论：精确公式：t_2(n)=min_{de=n,(d,e)=1} r(d,e)，其中 1≤r(d,e)≤n 且 r≡0 (mod d)、r≡−1 (mod e)。特别地 t_2(n)≤n。；若 p 为素数，则只有分解 1·p 或 p·1，故 t_2(p)=p−1；于是素数贡献给出 ∑_{n≤x}t_2(n)≫x²/log x，排除 c>1。；一般地 t_{k+1}(n)≤t_k(n)，而当素数 p≥k 时 t_k(p)=p−k+1。因此若第二问成立，分母 ∑t_k(n) 必须远大于共同的素数贡献 x²/log x。
- 第一阻塞点：CRT 归约后，需要证明对足够多的 n，某个单位分解 n=de 的模逆元异常小；现有初等平均不能控制“对每个 n 取最小值”的相关性。这里正是无法推出固定 log 幂节省的第一步。第二问还需要定量说明新增一个连续因子在平均意义下使最小起点下降一个消失比例；单调性本身远远不够。
- 下一步：按 ω(n) 分层，计算并检验 r(d,n/d)/n 在全部 2^{ω(n)} 个单位分解上的最小值分布；先尝试证明在 ω(n)≥δloglog n 的层上，至少有一个 CRT 解≤n/(log n)^c。
- 来源核对：官方页面确认开放状态、Erdős–Hall 上界及素数下界：https://www.erdosproblems.com/394；本地 Lean 文件确实把 m 限定为正整数，并分别形式化存在 c 与对所有 k≥2 的量词；文件中的定理仍含 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 45.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/394)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/394.lean`；既有候选答案（按不可信材料审计）

### #396

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that for every $k$ there exists $n$ such that\[\prod_{0\leq i\leq k}(n-i) \mid \binom{2n}{n}?\]
- 题意摘要：对每个自然数 k，是否存在整数 n，使下降阶乘 n(n−1)…(n−k) 整除中央二项式系数 C(2n,n)。任何见证自动满足 n>k，否则左侧为 0 而右侧非零。
- 状态核对：仍开放。官方讨论记录了截至 k=13 的计算见证，但有限计算不能解决全称量词。候选答案只列到 k=7，现已过时。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：逐素数使用 Legendre–Kummer：整除当且仅当对每个素数 p，∑_{i=0}^k v_p(n−i)≤v_p(C(2n,n))；右端等于基 p 下 n+n 的进位次数 κ_p(n)。尝试把长块条件归约到有限个小素数和单因子条件。
- 局部结论：得到精确判据：对所有素数 p，∑_{i=0}^k v_p(n−i)≤κ_p(n)。它同时计入同一 p 在多个块元素中的贡献，不能用“每个 n−i 分别整除 C(2(n−i),n−i)”代替。；若 p>2k、p∣m=n−j（0≤j≤k），则 n 的最低基 p 位为 j<p/2，最低位加倍不进位；故 κ_p(n)=κ_p(m)。这说明任何“非单因子型”障碍只能来自 p≤2k 的小素数。；因此固定 k 时，可把候选筛查分成有限个 p≤2k 的联合赋值条件，以及 p>2k 的单因子携带条件；这严格解释了现有小素数屏障计算法。
- 第一阻塞点：第一处缺口是同时满足有限个小素数条件与所有大素数条件。不同 p 的携带事件高度相关，而 Pomerance 的单个因子结果或“向前乘积密度 1”均不能保证 k+1 个下降因子的赋值总和受控。
- 下一步：固定 k，先严格估计由 p≤2k 条件定义的剩余类集合在模 ∏_{p≤2k}p^L 下的密度，再检验大素数筛是否有可求和的失败概率；这会直接测试概率筛路线能否闭合。
- 来源核对：官方页面确认问题仍开放及 Pomerance 的两项部分结果：https://www.erdosproblems.com/396；官方讨论记录截至 k=13 的计算结果和小素数屏障：https://www.erdosproblems.com/forum/thread/396；本地 Lean 陈述使用 descFactorial n (k+1)，与下降乘积量词一致，但证明仍为 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 45.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/396)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/396.lean`；既有候选答案（按不可信材料审计）

### #397

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Are there only finitely many solutions to\[\prod_i \binom{2m_i}{m_i}=\prod_j \binom{2n_j}{n_j}\]with the $m_i,n_j$ distinct?
- 题意摘要：令 B_t=C(2t,t)。问题问：满足 ∏_{m∈M}B_m=∏_{n∈N}B_n、且 M,N 为互不相交有限指标集的解是否只有有限多个。
- 状态核对：结论为否，且已标为 DISPROVED (LEAN)。候选答案的参数恒等式经独立代数核验正确。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：取任意 a≥2，令 c=8a²+8a+1，并比较 B_aB_{2a+2}B_c 与 B_{a+1}B_{2a}B_{c+1}。使用 B_t/B_{t+1}=(t+1)/(2(2t+1)) 化为有理恒等式。
- 局部结论：B_{2a+2}/B_{2a}=2(4a+3)(4a+1)/((a+1)(2a+1))。与 B_a/B_{a+1} 相乘得到 (4a+3)(4a+1)/(2a+1)²。；由 c+1=2(2a+1)²、2c+1=(4a+3)(4a+1)，可得 B_c/B_{c+1}=(2a+1)²/((4a+3)(4a+1))，故两边乘积相等。；六个指标严格排序为 a<a+1≤2a<2a+2<c<c+1；每个参数 a 给出合法解，且并集的最小指标就是 a，因此不同 a 产生不同解，解集无限。
- 第一阻塞点：无：参数恒等式、指标互异和解族无限性均已闭合。
- 下一步：若需进一步审计，可复现所链接 Lean 证明并检查其无 sorry/admit；数学反例本身已完整。
- 来源核对：官方页面给出同一参数族并标记 DISPROVED (LEAN)：https://www.erdosproblems.com/397；本地形式化陈述把解表示为互不相交 Finset，并链接外部 Lean 证明；当前镜像中的包装定理本身仍写作 sorry，但参数恒等式已可直接手算核验。
- 时间记账：所在批次墙钟时间按题数均摊约 45.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/397)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/397.lean`；既有候选答案（按不可信材料审计）

### #400

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $k\geq 2$ let $g_k(n)$ denote the maximum value of\[(a_1+\cdots+a_k)-n\]where $a_1,\ldots,a_k$ are integers such that $a_1!\cdots a_k! \mid n!$. Can one show that\[\sum_{n\leq x}g_k(n) \sim c_k x\log x\]for some constant $c_k$? Is it true that there is a constant $c_k$ such that for almost all $n<x$ we have\[g_k(n)=c_k\log x+o(\log x)?\]
- 题意摘要：对每个固定 k≥2，g_k(n) 是所有自然数 a_1,…,a_k 满足 ∏a_i!∣n! 时的最大超额 ∑a_i−n。分别问是否存在常数 c_k 使平均值 ∑_{n≤x}g_k(n)∼c_kxlog x，以及是否对几乎所有 n≤x 有 g_k(n)=c_klog x+o(log x)。
- 状态核对：两问仍开放；官方上下文只确认一致上界 g_k(n)≪_k log n。候选答案额外声称几乎处处下界及 Θ(xlog x)，依赖未在官方页收录的外部定理，本次未把它当作已核定事实。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：使用唯一容易统一控制的 2-adic 赋值。由 Legendre 公式 v_2(m!)=m−s_2(m)，将阶乘整除转为二进制数位和不等式；再考察“正常阶”是否蕴含平均渐近。
- 局部结论：整除给出 ∑(a_i−s_2(a_i))≤n−s_2(n)，故 g_k(n)≤∑s_2(a_i)−s_2(n)。又每个 a_i!∣n!，除极小退化情形外 a_i≤n，所以 g_k(n)≤k(⌊log_2n⌋+1)，重建了 O_k(log n) 上界。；添加一个 a_{k+1}=1 不改变整除性而使超额增加 1，故 g_{k+1}(n)≥g_k(n)+1。；由于已有一致界 g_k(n)≤C_klog x，若第二问的正常阶以常数 c_k 成立，则由有界收敛式分拆可推出 ∑_{n≤x}g_k(n)/(xlog x)→c_k；因此正常阶命题严格强于相同常数的平均值命题。
- 第一阻塞点：2-adic 条件只给上界；要构造超额 δlog n，还必须同时控制所有奇素数的 Legendre 亏损。第一处无法闭合的是证明存在固定 δ>0，使这种同时控制对密度 1 的 n 成立，更不用说证明归一化后的亏损集中到唯一常数。
- 下一步：对 k=2、候选 a=n/2+u、b=n/2（u≈c log n），计算 D_p=v_p(a!)+v_p(b!)−v_p(n!) 的联合分布；先验证是否能证明 ∑_{p:D_p>0}D_p log p=O(log n) 在正密度集合上成立。
- 来源核对：官方页面仅确认开放状态及 O_k(log n) 上界：https://www.erdosproblems.com/400；本地 Lean 文件形式化了平均值、正常阶和上界；研究定理仍含 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 45.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/400)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/400.lean`；既有候选答案（按不可信材料审计）

### #401

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is there $f(r)\to\infty$ such that, for infinitely many $n$, there are $a_1,a_2$ with $a_1+a_2>n+f(r)\log n$ and $a_1!a_2!\mid n!2^n3^n\cdots p_r^n$?
- 题意摘要：按官方采用的量词解释：存在函数 f(r)→∞，使对每个固定 r 都有无穷多个 n，并存在 a_1,a_2 满足 a_1+a_2>n+f(r)log n 且 a_1!a_2!∣n!∏_{i=1}^r p_i^n。原文量词有歧义；“对所有充分大 n”的替代版本为假。
- 状态核对：官方状态为 PROVED (LEAN)，应重建肯定路线而非继续当开放题处理。官方页同时显示“Formalised statement? No”，与状态标签存在元数据不一致；讨论区则链接了可编译 Lean 文件。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：调用已解决问题 729 的构造：对每个 c>0，存在 A(c)，并在任意充分大尺度找到 m，令 n=2m、a_1=m+⌊c log m⌋、a_2=m，使 n!/(a_1!a_2!) 的分母只含素数≤A(c)。再用 ∏_{i≤r}p_i^n 吸收这些小素数。
- 局部结论：对 p>A(c)，729 的结论直接给出 v_p(a_1!)+v_p(a_2!)≤v_p(n!)。；对 p≤A(c)，Legendre 公式给出亏损 D_p=v_p((m+q)!)+v_p(m!)−v_p((2m)!)=O_c(log m)，其中 q=⌊c log m⌋；而附加因子提供指数 n=2m，所以充分大 m 时 D_p≤n。由此得到所需整除。；可令 R(j) 满足 p_{R(j)}≥A(2j)，再定义 f(r)=max({j:r≥R(j)}∪{0})。则 f(r)→∞；对给定 r 取 c=2f(r) 的构造，有 q>f(r)log(2m)（充分大 m），从而得到无穷多个见证。
- 第一阻塞点：在接受问题 729 的已证明构造后没有剩余缺口。本次没有重新证明 729；它是该重建路线唯一的重大输入。
- 下一步：对最终证书做一次依赖审计：确认 729 的 Lean 定理确实给出每个固定 c 下无穷多个尺度，而非仅一个 m，并核对 401 外部文件中的 r、n 量词与官方采用解释完全一致。
- 来源核对：官方页面确认肯定解、量词歧义及替代版本反例：https://www.erdosproblems.com/401；讨论区第 228–235 行明确给出从 729 推出 401 的构造及 f(r) 定义：https://www.erdosproblems.com/forum/thread/401；官方页称 PROVED (LEAN)，但同页数据库栏称尚无正式形式化陈述；应保留这一证书元数据差异。
- 时间记账：所在批次墙钟时间按题数均摊约 45.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/401)

### #404

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which integers $a\geq 1$ and primes $p$ is there a finite upper bound on those $k$ such that there are $a=a_1<\cdots<a_n$ with\[p^k \mid (a_1!+\cdots+a_n!)?\]If $f(a,p)$ is the greatest such $k$, how does this function behave? Is there a prime $p$ and an infinite sequence $a_1<a_2<\cdots$ such that if $p^{m_k}$ is the highest power of $p$ dividing $\sum_{i\leq k}a_i!$ then $m_k\to \infty$?
- 题意摘要：固定整数 a≥1 与素数 p，考察所有有限严格递增序列 a=a₁<⋯<aₙ，并令 S=∑aᵢ!；问可实现的 v_p(S) 是否有有限上界，若有则研究最大值 f(a,p)。第二问是：是否存在固定 p 及无限递增序列 (aᵢ)，使部分和的 p-adic 赋值趋于无穷。
- 状态核对：按冻结状态仍为开放。旧候选把 Lin 的结果误写成 f(2,2)=254；给定官方材料只支持 f(2,2)≤254，不能升级为等号。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先处理可严格证明的阻断族，再用乘积空间紧致性核对第二问与“某个 f(a,p) 无界”的等价性。令 t=v_p(a!)。若 p|(a+1)，则每个 j>a 都满足 p^(t+1)|j!，故任意允许的和均为 a! mod p^(t+1)。另一方面，若对每个 K 都存在包含 a! 的有限子集和模 p^K 为零，则在 {0,1}^{ℕ≥a} 中定义闭集 C_K；高阶 factorial 模 p^K 自动为零，所以 C_K 实际只依赖有限坐标。C_K 非空且递降，紧致性给出共同选择。
- 局部结论：若 a≡−1 (mod p)，则每个允许和都恰有 v_p(S)=v_p(a!)，所以 f(a,p)=v_p(a!)。；“f(a,p) 无界”严格蕴含存在一个无限 0/1 选择，使 factorial 级数在 ℤ_p 中等于 0；该选择不可能有限，因为它包含正整数 a!。；枚举被选指标后，部分和 p-adically 收敛到 0，故其赋值趋于无穷；反向蕴含显然。因此第二问等价于存在某对 (a,p) 使可实现赋值无界。
- 第一阻塞点：紧致性只把第二问归约为无界性，并不产生任何无界的 (a,p)。第一处真正缺口是：对某个未被局部模 p^(t+1) 阻断的 pair，须证明所有层级 C_K 均非空；这正是尚未解决的 factorial 子集和覆盖问题。
- 下一步：选定最有希望的 (a,p)，例如 (1,5)，对每个 K 建立有限状态的子集和递推，检验从模 p^K 到 p^(K+1) 的覆盖引理；必须输出可人工核验的归纳条件，而非仅给大规模样例。
- 来源核对：已按输入中的官方 #404 陈述核对量词。；官方上下文仅记载 Lin 证明 f(2,2)≤254；旧候选的等号说法无来源支持。；旧候选的紧致性等价经补全闭集有限坐标性、非有限选择及部分和收敛三步后成立。
- 时间记账：所在批次墙钟时间按题数均摊约 47.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/404)；既有候选答案（按不可信材料审计）

### #406

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that there are only finitely many powers of $2$ which have only the digits $0$ and $1$ when written in base $3$?
- 题意摘要：问集合 E={n≥0：2^n 的三进制展开每一位都属于 {0,1}} 是否有限；等价地，是否只有有限多个 2 的幂可写成互异 3 的幂之和。题目只问有限性，并未要求证明已知样例 1,4,256 是全部。
- 状态核对：按冻结状态仍为开放。输入称 Saye 已验证 16≤n≤5.9×10²¹ 的 2^n 含全部三种三进制数字；这是有限计算，不能推出有限性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试先用低模约束筛掉指数，再把问题转成可递推的数字自动机。若 n≥1 且三进制数字仅为 0,1，则个位不能为 0，因为 3∤2^n，所以个位为 1；于是 2^n≡1 (mod 3)，强制 n 为偶数。再考察模 2^t：三进制位选择满足 ∑ε_j3^j≡0 (mod 2^t)（当 n≥t），可用 3^j 在模 2^t 下的周期建立有限状态图。
- 局部结论：除 n=0 外，任何候选指数 n 必为偶数。；若 n≥1，则三进制最低位必为 1；且因 2^n 为偶数，三进制展开中数字 1 的总数必为偶数。；对固定 t，所有足够大的候选展开都对应模 2^t 的 0/1 子集和状态 0；该条件可由有限自动机精确检验。
- 第一阻塞点：固定模数的自动机只能给周期性或局部禁配条件；未能证明随着位长增长，接受状态最终消失。也不能直接套用固定项数的 S-unit 方程定理，因为非零三进制位的个数不受限制。
- 下一步：构造同时跟踪模 2^t 与数值区间 2^n≤∑ε_j3^j<2^(n+1) 的转移系统，先检验是否存在某个小 t 形成可证明的“无可延伸状态”；若不存在，应记录循环状态作为该路线的明确障碍。
- 来源核对：本地 406.lean 形式化为满足 isPowerOfTwo 且 Nat.digits 3 n⊆[0,1] 的自然数集合有限，与原题对象一致。；已直接复算 1=(1)₃、4=(11)₃、256=(100111)₃。；未采用旧候选中“这些恰为全部”的猜测作为已知结论。
- 时间记账：所在批次墙钟时间按题数均摊约 47.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/406)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/406.lean`；既有候选答案（按不可信材料审计）

### #408

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\phi(n)$ be the Euler totient function and $\phi_k(n)$ be the iterated $\phi$ function, so that $\phi_1(n)=\phi(n)$ and $\phi_k(n)=\phi(\phi_{k-1}(n))$. Let\[f(n) = \min \{ k : \phi_k(n)=1\}.\]Does $f(n)/\log n$ have a distribution function? Is $f(n)/\log n$ almost always constant? What can be said about the largest prime factor of $\phi_k(n)$ when, say, $k=\log\log n$?
- 题意摘要：定义 φ₁(n)=φ(n)、φ_k(n)=φ(φ_{k−1}(n))，以及到达 1 的最小步数 f(n)。第一问指经验分布 lim_{x→∞}x⁻¹#{n≤x:f(n)/log n≤y} 是否存在；第二问问是否存在常数 c，使 f(n)/log n→c 对几乎所有 n 成立；第三问研究例如 k=⌊log log n⌋ 时 P⁺(φ_k(n))。
- 状态核对：冻结状态为开放。官方上下文只给出：前两问在某种 Elliott–Halberstam 假设下得到肯定答案；无条件结论不能从该条件结果中删去假设。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：采用 Shapiro 的加性化路线。定义 H(n)=f(n)（n 偶）及 H(n)=f(n)−1（n 奇）；通过素因数分解可将高度问题归约到 H(p) 在素数上的平均行为，再拟用 Turán–Kubilius 型集中估计。对第三问，逐步使用：若 q|φ(m)，则通常来自 q²|m 或某素因子 r|m 且 r≡1 (mod q)，从而把大素因子追溯为逆向素数链。
- 局部结论：直接迭代得 f(2^a)=a，且 f(2·3^b)=b+1；故沿稀疏序列可分别逼近 1/log2 与 1/log3，这不反驳密度一的常数行为。；对 n>2，φ(n) 为偶数，且此后每次至少缩小一半，因此 f(n)≤1+log₂n；Pillai 型下界与此共同确认正确尺度是 log n。；当 k=⌊log log n⌋ 时，仅靠 φ(m)≤m/2 得 P⁺(φ_k(n))≤n/2^k=n/(log n)^{log2+o(1)}，远弱于 n^{o(1)}。
- 第一阻塞点：加性函数集中所需的关键输入是 H(p) 在素数上的一阶平均及方差控制；这牵涉 p−1 的因子与长素数链分布，现有无条件素数算术级数估计不足。第三问同样卡在控制几乎所有 n 中长逆向同余链 r≡1 (mod q)。
- 下一步：从 EGPS 的条件证明中抽取一条精确的 EH 型平均估计，逐项标出它在 H(p) 均值和方差中的用途；然后检查现有无条件 Bombieri–Vinogradov 范围能否至少处理固定链长或给出截断版结论。
- 来源核对：官方上下文明确区分条件性结论与无条件开放状态。；旧候选给出的 Shapiro 分解经样例 n=6、9、12 复算相容，但完整一般公式仍应以原论文为准，未把它当作本次新证明。；未采用旧候选依赖 OEIS 转引的具体 ε>2/3 声称，因为输入的官方材料未提供该精确阈值。
- 时间记账：所在批次墙钟时间按题数均摊约 47.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/408)；既有候选答案（按不可信材料审计）

### #409

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：How many iterations of $n\mapsto \phi(n)+1$ are needed before a prime is reached? Can infinitely many $n$ reach the same prime? What is the density of $n$ which reach any fixed prime?
- 题意摘要：令 T(n)=φ(n)+1，F(n)=min{k≥0:T^k(n) 为素数}。第一问因措辞含混，应理解为 F(n) 的良好逐点或极值上界；第二问是是否存在素数 p，使 basin B_p={n:∃k,T^k(n)=p} 无限；第三问问每个固定 p 的 B_p 的自然密度。
- 状态核对：冻结状态为开放，但“每条正整数轨道终止于素数”本身容易证明；开放部分是优良上界、无限 basin 与密度。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先严格证明下降及 O(√n) 上界，再把固定素数的 basin 写成有限分支的逆 Euler-totient 树。若 m≥4 合数，取最小素因子 q≤√m，则 φ(m)≤m(1−1/q)≤m−√m，所以 T(m)≤m−√m+1。令 u=√m，可验证 u²−u+1≤(u−1/4)²（u≥2）。
- 局部结论：合数 m>1 满足 T(m)<m，而素数是固定点，因此每个 n>0 都在有限步内到达素数。；每个合数步骤令平方根至少下降 1/4，故 F(n)≤4√n+O(1)，从而 F(n)=o(n)。；对任意奇素数 p，T(2p)=p，所以 F(2p)=1；而固定目标 p 的直接前驱恰是有限集合 {m:φ(m)=p−1}。
- 第一阻塞点：逆树每层有限并不推出整棵树有限；需要排除任意长的链 φ(m_{j+1})=m_j−1。现有下降估计只从起点向前控制长度，不能对固定根 p 给出统一高度界，也不给出 basin 的密度。
- 下一步：对固定 p 建立逆树的层计数 A_j(p)，并尝试证明 ∑_j A_j(p;x)=o(x)；首个可检验子任务是利用已知逆 Euler-totient 上界，给出深度 1、2 的一致计数并检查估计在迭代时损失何处失控。
- 来源核对：本地 409.lean 明确量化 n>0，并另列 termination 为可测试命题；这与下降证明一致。；旧候选的 O(√n) 推导已逐项检查，不等号方向正确。；旧候选称每个 basin 有限是“猜想”；输入官方上下文未正式给出该猜想，故这里只保留为未解决可能性，不宣称共识。
- 时间记账：所在批次墙钟时间按题数均摊约 47.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/409)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/409.lean`；既有候选答案（按不可信材料审计）

### #410

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\sigma_1(n)=\sigma(n)$, the sum of divisors function, and $\sigma_k(n)=\sigma(\sigma_{k-1}(n))$. Is it true that\[\lim_{k\to \infty} \sigma_k(n)^{1/k}=\infty?\]
- 题意摘要：对固定起点 n，令 a₀=n、a_{k+1}=σ(a_k)。按本地形式化的 intended quantifier 是每个 n>1，问是否 a_k^{1/k}→∞。若逐字把 n=1 也包括在原文中，则命题立即为假，因为 σ(1)=1。
- 状态核对：对 n>1 的标准版本按冻结状态仍为开放；旧候选正确注意到 n=1 的量词陷阱。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把增长写成乘法增量：log(a_k^{1/k})=k⁻¹log n+k⁻¹∑_{j<k}log(σ(a_j)/a_j)。尝试证明这些平均增量趋于无穷。可先利用 σ(m)≥m+1（m>1）得到严格增长；若 m 为偶数，则 σ(m)≥m+m/2=3m/2，得到一次固定比例跃升。
- 局部结论：对 n>1，a_{k+1}>a_k，因而 a_k≥n+k；但这只给 a_k^{1/k}→1 的下界尺度，远不足以证明目标。；每当 a_j 为偶数时有 a_{j+1}/a_j≥3/2；即使能证明偶数状态具有正密度，也至多先得到固定指数增长，仍不能直接推出 kth root→∞。；目标等价于沿轨道的平均量 k⁻¹∑_{j<k}log(σ(a_j)/a_j)→∞；因此必须证明 σ(a_j)/a_j 的典型规模沿单条轨道本身无界地增长，而非仅偶尔大于常数。
- 第一阻塞点：没有机制保证轨道频繁进入具有越来越多小素因子的整数。σ(m) 的奇偶判据还允许平方或两倍平方造成例外；现有初等下界只产生线性或固定底数的指数增长，无法使 kth root 发散。
- 下一步：沿若干起点精确记录 a_j 的小素数整除集合，并检验命题：对每个 y，轨道是否最终以密度趋近 1 的频率被所有素数 q≤y 整除。若能对固定 y 严格证明正密度版本，则 σ(a_j)/a_j≥∏_{q≤y}(1+1/q) 可形成分阶段的可量化下界。
- 来源核对：本地 410.lean 明确写成 ∀n>1，排除了 n=1 反例。；官方上下文只将问题列为开放，没有给出可用于闭合证明的额外定理。；旧候选中的数值增长启发未被当作证明；本次只使用可直接验证的 σ(m)≥m+1 与偶数情形 σ(m)≥3m/2。
- 时间记账：所在批次墙钟时间按题数均摊约 47.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/410)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/410.lean`；既有候选答案（按不可信材料审计）

### #411

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g_1=g(n)=n+\phi(n)$ and $g_k(n)=g(g_{k-1}(n))$. For which $n$ and $r$ is it true that $g_{k+r}(n)=2g_k(n)$ for all large $k$?
- 题意摘要：对象为正整数 n,r；要求存在 K，使对每个 k≥K 都有 g_{k+r}(n)=2g_k(n)，其中 g(x)=x+φ(x)，g_k 为第 k 次迭代。必须区分起点 n 与最终到达的尾点 x=g_K(n)。
- 状态核对：整体仍开放，尤其 r≠2 及 r=2 的例外素数情形。旧候选把 r=2 的已知结构说成“完整分类”，并把尾点分类直接当成所有起点分类，均过强；传播公式 g(2m)=2g(m) 还要求 m 为偶数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先作奇偶筛除，再把 r=2 化为单个丢番图方程。若尾点 x 为偶数，则 g_2(x)=2x 等价于 φ(x)+φ(x+φ(x))=x。由于偶数 y>2 满足 g(y) 为偶数，且偶数 y 满足 g(2y)=2g(y)，一次成立便可沿轨道传播。
- 局部结论：任何解必有 n 为偶数且 n>2：奇数 >1 的轨道始终为奇数，而右端 2g_k(n) 为偶数；n=1,2 很快进入奇数轨道。；r=1 不可能：在最终的偶数尾点 x>2，有 g(x)=x+φ(x)<2x。；对 r=2，若某个偶数尾点 x 满足 φ(x)+φ(x+φ(x))=x，则 g_2(x)=2x，并由 g(2x)=2g(x) 严格推出以后每一步仍满足二步倍增。可直接核验 x=2^a t（a≥1，t∈{1,3,5,7,35,47}，纯 2 幂取足够大的指数）形成三个二步循环族。
- 第一阻塞点：第一处不能闭合的是排除 Steinerberger 结构定理留下的例外素数 p≡7 (mod 8)，即控制 φ((3p−1)/4)=(p+1)/2；更不能由 r=2 方程推导一般 r 必等于 2。
- 下一步：对例外分支加入已知的平方自由性和素因子相容条件，编写可验证筛法：逐个素因子 q|(3p−1)/4 推导 q−1 对目标 φ 值的整除限制，并检查能否把 p 的下界继续推高。
- 来源核对：Steinerberger 原论文摘要确认六个显式族及例外素数条件：[arXiv 2504.08023](https://arxiv.org/abs/2504.08023)。；最新问题页仍将一般问题列为开放，并给出 Cambie 的归约：[Erdős Problem 411](https://www.erdosproblems.com/411)。
- 时间记账：所在批次墙钟时间按题数均摊约 40.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/411)；既有候选答案（按不可信材料审计）

### #412

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\sigma_1(n)=\sigma(n)$, the sum of divisors function, and $\sigma_k(n)=\sigma(\sigma_{k-1}(n))$. Is it true that, for every $m,n\geq 2$, there exist some $i,j$ such that $\sigma_i(m)=\sigma_j(n)$?
- 题意摘要：对每个 m,n≥2，问是否存在正整数 i,j，使 σ^{∘i}(m)=σ^{∘j}(n)。若允许 i,j=0，命题等价，因为一次相遇可同时再迭代一步。
- 状态核对：仍开放。旧候选列出的“21 棵树”和大规模计算不能证明反例；其基本单调性与相遇后合并则正确。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把问题视为有向函数图的连通性，并尝试用最小候选对 2、5 寻找分离不变量。考察了大小、奇偶性及 σ(x) 为奇数的判据。
- 局部结论：对 x>1，σ(x)≥x+1，故每条轨道严格递增、无周期。；若两轨道在某点相遇，则其后完全相同；因此只需证明每个 n≥2 的轨道都与固定的 2-轨道相交。；σ(x) 为奇数当且仅当 x 是平方或二倍平方；所以奇偶性不是轨道不变量，无法据此分离 2 与 5 的轨道。
- 第一阻塞点：第一处断裂是找不到在 σ 下保持、且能区分两条候选轨道的同余或赋值不变量。严格递增只排除回返，并不强迫两个稀疏递增序列相交。
- 下一步：对 2、5 两条轨道做可复核的逆像搜索：对每个已到达值 X，完整枚举 σ(a)=X 的解并建立有限深度逆树，记录是否出现可推广的素因子或 2-adic 禁止模式；有限不相交本身不作为反例。
- 来源核对：最新汇总仍标为开放，且没有被收录的部分解：[Erdős Problem 412](https://www.erdosproblems.com/412)。；本地 Lean 陈述使用零次迭代，但与原题的正次迭代版本等价；文件量词为所有 m,n≥2。
- 时间记账：所在批次墙钟时间按题数均摊约 40.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/412)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/412.lean`；既有候选答案（按不可信材料审计）

### #413

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\omega(n)$ count the number of distinct primes dividing $n$. Are there infinitely many $n$ such that, for all $m<n$, we have $m+\omega(m) \leq n$? Can one show that there exists an $\epsilon>0$ such that there are infinitely many $n$ where $m+\epsilon \omega(m)\leq n$ for all $m<n$?
- 题意摘要：第一问要求集合 {n:∀m<n, m+ω(m)≤n} 无限。第二问要求存在一个固定实数 ε>0，使 {n:∀m<n, m+εω(m)≤n} 无限。令 m=n−k 后，条件分别为 ω(n−k)≤k 和 εω(n−k)≤k（1≤k<n）。
- 状态核对：按冻结日期 2025-08-31 两问均为 open；但冻结后 Lau（2026）已正面解决第二问，并证明第一问的常数宽度削弱版。第一问仍开放。因此旧候选关于“第二问仍开放”的说法现已过时。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `medium`
- 尝试路线：采用“短后向窗口+筛法”路线。利用 ω(a)≤log_2 a，把所有 k 的约束缩减为靠近 n 的对数长度窗口，再检查最小 k 所施加的局部因子条件。
- 局部结论：ε=1 时，k=1 强迫 ω(n−1)≤1，所以 n−1 必为 1 或素数幂；一般 ε 时有 ω(n−1)≤⌊1/ε⌋。；由于 ω(n−k)≤log_2 n，只要 k≥ε log_2 n，第二问的约束自动成立；真正困难的只有 O_ε(log n) 个最近邻。；第一问同理只需控制 1≤k<log_2 n；但这些约束包含 n−1 为素数幂等近似素数元组条件，普通平均筛界不足以同时保证。
- 第一阻塞点：在冻结时点的具体路线中，第一处无法闭合的是同时构造无限多个 n，使增长中的整个窗口 1≤k<O(log n) 都满足 ω(n−k)≤k；CRT 能安排小素因子，却不能保证剩余因子数足够少。Lau 的新工作克服了固定 ε 版本，但未给出 ε=1 的完整屏障。
- 下一步：重建 Lau 定理 Ω(n−k)≤C log k 的证明，并精确检查 k=1 的处理；随后将其常数 C 转译为可显式给出的 ε。对第一问则定位其方法在 k=1,…,C 的损失，判断是否正好对应已知的常数宽度缺口。
- 来源核对：2026 年更新明确称 Lau 已肯定回答第二问，并得到第一问的常数宽度版本：[Erdős Problem 413 discussion](https://www.erdosproblems.com/forum/thread/413?embed=1)。；相关定理被表述为存在 C，使无限多个 n 满足 Ω(n−k)≤C log k（1<k<n）：[Erdős Problem 679](https://www.erdosproblems.com/679)。；本地 Lean 文件仍按冻结版本把两问均标为 research open，故状态元数据已滞后。
- 时间记账：所在批次墙钟时间按题数均摊约 40.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/413)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/413.lean`；既有候选答案（按不可信材料审计）

### #414

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h_1(n)=h(n)=n+\tau(n)$ (where $\tau(n)$ counts the number of divisors of $n$) and $h_k(n)=h(h_{k-1}(n))$. Is it true, for any $m,n$, there exist $i$ and $j$ such that $h_i(m)=h_j(n)$?
- 题意摘要：对所有正整数 m,n，问是否存在迭代次数 i,j，使 h^{∘i}(m)=h^{∘j}(n)，其中 h(x)=x+τ(x)。形式化版本允许 i,j=0；这与正次版本等价。
- 状态核对：仍开放。旧候选的轨道归约正确，但其声称自行验证到 100000 的数值结果没有证书，不能采信为本次筛查结论。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试用“小步长导致轨道接近”来逼迫相交。对每条轨道考察首次越过给定高度 X 的点，并用初等除数界控制超越量。
- 局部结论：τ(x)≥1，故每条轨道严格递增；一旦相交便永久合并。于是全称两两相交等价于每条轨道都与 1 的轨道相交。；初等配对除数给出 τ(x)≤2√x，因此 h(x)≤x+2√x。；任一轨道首次达到或越过 X 的点都落在 [X,X+2√X)；所以所有轨道在加性尺度 O(√X) 上都相当稠密。
- 第一阻塞点：第一处不能闭合的是从“两条轨道在每个大尺度都各自进入同一个 O(√X) 窗口”推出精确相等。整数间距趋于相对很小并不排除永久错位，且 h 缺乏单调性或收缩不变量。
- 下一步：研究两轨道相邻点的差 d，并完整分类小差值碰撞方程 a+τ(a)=b+τ(b)（先做 |a−b|≤10）；寻找能把 O(√X) 距离递降到有限差值集合的确定性引理。
- 来源核对：最新汇总仍列为开放：[Erdős Problem 414](https://www.erdosproblems.com/414)。；本地 Lean 陈述的对象是正自然数，并明确量化所有 m,n 及存在 i,j。
- 时间记账：所在批次墙钟时间按题数均摊约 40.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/414)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/414.lean`；既有候选答案（按不可信材料审计）

### #415

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $n$ let $F(n)$ be the largest $k$ such that any of the $k!$ possible ordering patterns appears in some sequence of $\phi(m+1),\ldots,\phi(m+k)$ with $m+k\leq n$. Is it true that\[F(n)=(c+o(1))\log\log\log n\]for some constant $c$? Is the first pattern which fails to appear always\[\phi(m+1)>\phi(m+2)>\cdots \phi(m+k)?\]Is it true that 'natural' ordering which mimics what happens to $\phi(1),\ldots,\phi(k)$ is the most likely to appear?
- 题意摘要：严格解释下，F(n) 是最大的 k，使 S_k 的每个排列 π 都能由某个 m+k≤n 的互异数列 φ(m+1),…,φ(m+k) 实现。第二问比较最早缺失的排列；第三问涉及允许相等的“自然弱序”及尚未指定的出现频率。
- 状态核对：三问不能统一标成单一开放命题：严格序解释下，第一问已有否定答案；第二问仍未解决；第三问若不定义弱序和“最可能”的统计方式则不完备。旧候选关于第一问的核心否定路线正确，但没有充分区分 PPT 论文中的一般单调子集与第 8 节的连续区间定理。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：取 G_↓(n) 为 [1,n] 内连续 totient 严格递减段的最大长度。因为全排列实现必包含递减排列，立即有 F(n)≤G_↓(n)；再代入 Pollack–Pomerance–Treviño 对连续段的渐近式。
- 局部结论：严格序下 F(n)≤G_↓(n) 是直接包含关系。；已知 G_↓(n)∼log_3 n/log_6 n；因此 F(n)=o(log_3 n)，排除了任何 c>0 的 F(n)=(c+o(1))log_3 n。第一问据此为否定。；φ(1)=φ(2)=1，故“模仿 φ(1),…,φ(k)”从 k=2 起已经含相等；它不是 k! 个严格排列之一。第三问必须改用弱序，并指定按 m≤N 的频率、首次出现位置或其他概率模型。
- 第一阻塞点：第二问的断点是：递减排列给出 F 的上界，并不证明所有其他排列在该阈值前均已出现；递增段具有同阶渐近也不能比较有限 n 时谁先缺失。第三问则在定义层面尚不能进入证明。
- 下一步：对固定严格排列 π，逐项检查 PPT 第 8 节的同余构造能否把所需 φ(x_i)/x_i 次序任意排列，同时保持连续整数及严格不等号；目标是证明每个 π 的最长实现段都有统一的 log_3 n/log_6 n 下界。
- 来源核对：最新版问题页已明确记录 F(n)≤G(n) 及第一问的否定答案：[Erdős Problem 415](https://www.erdosproblems.com/415)。；PPT 原论文第 8 节确实处理连续整数段，而非仅一般子集，并构造长度约 log_3 x/log_6 x 的单调段：[MonotonePhi.pdf](https://math.dartmouth.edu/~carlp/MonotonePhi.pdf)。；问题页同时指出 Er36b 实际只证明相邻比较各约占一半；旧官方背景所称 F(n)≍log log log n 未在该文中找到。
- 时间记账：所在批次墙钟时间按题数均摊约 40.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/415)；既有候选答案（按不可信材料审计）

### #416

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $V(x)$ count the number of $n\leq x$ such that $\phi(m)=n$ is solvable. Does $V(2x)/V(x)\to 2$? Is there an asymptotic formula for $V(x)$?
- 题意摘要：令 \(V(x)=\#\{n\in\mathbb N:n\le x,\ \exists m\in\mathbb N,\phi(m)=n\}\)。问题分别问 \(V(2x)/V(x)\to2\) 是否成立，以及是否存在显式 \(M(x)\) 使 \(V(x)\sim M(x)\)。
- 状态核对：冻结状态为 open；官方页仍称 Ford 的双边阶估计不足以推出渐近式或倍增极限。候选答案所称 \(V(cx)-V(x)\asymp_cV(x)\) 未在所给官方材料中得到支持，本筛查不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把 Ford 主尺度记为 \(M(x)=\frac{x}{\log x}\exp(P(\log_3x,\log_4x))\)，尝试先证明该尺度正则变化，再把 \(V(x)\asymp M(x)\) 提升为相对误差渐近式。
- 局部结论：直接展开迭代对数可得 \(\log_j(2x)-\log_jx\to0\)（\(j\ge2\)），因而 Ford 型显式尺度满足 \(M(2x)/M(x)\to2\)。；若能加强到 \(V(x)=M(x)(1+o(1))\)，则立即有 \(V(2x)/V(x)\to2\)。；现有 \(V(x)\asymp M(x)\) 只能推出倍增比被两个正常数夹住；隐藏的有界乘子可以振荡，不能推出极限。
- 第一阻塞点：第一处断点是把 Ford 估计中指数的 \(O(1)\)（等价于乘法常数不确定性）压缩为 \(o(1)\)，且须在 \([x,2x]\) 上一致；现有筛法/素因子配置计数没有给出这一精度。
- 下一步：逐项检查 Ford 参数化中产生乘法常数损失的配置求和，先验证能否证明较弱的对数平滑性 \(\log V(2x)-\log V(x)\to\log2\)。
- 来源核对：[Erdős Problems #416](https://www.erdosproblems.com/416) 仍列为 open，并明确说明已知阶估计不足以解决倍增极限。
- 时间记账：所在批次墙钟时间按题数均摊约 38.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/416)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/416.lean`；既有候选答案（按不可信材料审计）

### #417

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[V'(x)=\#\{\phi(m) : 1\leq m\leq x\}\]and\[V(x)=\#\{\phi(m) \leq x : 1\leq m\}.\]Does $\lim V(x)/V'(x)$ exist? Is it $>1$?
- 题意摘要：\(V'(x)=\#\{\phi(m):1\le m\le x\}\)，而 \(V(x)=\#\{t\le x:\exists m\ge1,\phi(m)=t\}\)。问 \(V(x)/V'(x)\) 的极限是否存在，以及若存在是否严格大于 \(1\)。
- 状态核对：冻结状态及当前官方页均为 open；Erdős 曾猜测比值甚至可能趋于无穷。候选答案关于 \(V'\) 的精细阶和数值表未由官方材料核实，故不作为证明输入。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：对每个欧拉函数值 \(t\) 定义最小原像 \(\mu(t)=\min\{m:\phi(m)=t\}\)，把问题归约为最小原像超过截断点 \(x\) 的尾部比例。
- 局部结论：精确地，\(V'(x)=\#\{t\le x:t\in\operatorname{im}\phi,\ \mu(t)\le x\}\)，故 \(V(x)-V'(x)=\#\{t\le x:t\in\operatorname{im}\phi,\ \mu(t)>x\}\)。；因此比值存在且大于 \(1\) 等价于上述尾部计数除以 \(V'(x)\) 收敛到一个正数；趋于无穷则要求尾部远大于截断内部分。；若 \(x+1\) 为素数，则 \(x=\phi(x+1)\) 被 \(V(x)\) 计数，但不被 \(V'(x)\) 计数，因为 \(m\le x\) 时 \(\phi(m)<x\)。故 \(V(x)>V'(x)\) 对无穷多个 \(x\) 成立，但差至少一项不足以控制相对比例。
- 第一阻塞点：第一处断点是缺少最小原像 \(\mu(t)\) 的分布估计；现有 \(V(x)\) 的总体计数并不区分 \(\mu(t)\le x\) 与 \(\mu(t)>x\)。
- 下一步：计算并分层统计 \(T_k(x)=\#\{t\le x:kx<\mu(t)\le(k+1)x\}\)，先检验能否对某个固定 \(k\) 证明 \(T_k(x)\gg V(x)\) 或 \(o(V(x))\)。
- 来源核对：[Erdős Problems #417](https://www.erdosproblems.com/417) 只确认 \(V'\le V\)、开放状态及“极限可能无穷”的猜测。
- 时间记账：所在批次墙钟时间按题数均摊约 38.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/417)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/417.lean`；既有候选答案（按不可信材料审计）

### #420

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $\tau(n)$ counts the number of divisors of $n$ then let\[F(f,n)=\frac{\tau((n+\lfloor f(n)\rfloor)!)}{\tau(n!)}.\]Is it true that\[\lim_{n\to \infty}F((\log n)^C,n)=\infty\]for large $C$? Is it true that $F(\log n,n)$ is everywhere dense in $(1,\infty)$? More generally, if $f(n)\leq \log n$ is a monotonic function such that $f(n)\to \infty$ as $n\to \infty$, then is $F(f,n)$ everywhere dense?
- 题意摘要：对整数 \(n\) 及实函数 \(f\)，令 \(k=\lfloor f(n)\rfloor\)、\(F(f,n)=\tau((n+k)!)/\tau(n!)\)。分别问：是否存在充分大的固定 \(C\) 使该比值对所有 \(n\to\infty\) 发散；\(f(n)=\log n\) 时值集是否在 \((1,\infty)\) 稠密；以及对任意单调、趋于无穷且 \(f(n)\le\log n\) 的函数是否同样稠密。
- 状态核对：三问仍为 open。候选答案“\(C\ge2\) 全部开放”需细化：已知正常阶结果严格否定每个 \(C<2\)，但在临界 \(C=2\) 及以上没有无条件的全序列结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把阶乘逐项加入，并用区间内素数给出确定性下界；然后把发散问题归约为所有短区间中的素数数目趋于无穷。
- 局部结论：若 \(R(m)=\tau(m!)/\tau((m-1)!)\)，则 \(F(f,n)=\prod_{m=n+1}^{n+k}R(m)\)；每个 \(R(m)>1\)。；当 \(m\) 为素数时 \(R(m)=2\)，所以严格有 \(F(f,n)\ge2^{\pi(n+k)-\pi(n)}\)。因此若能证明每个长度 \((\log n)^C\) 的区间都含趋于无穷多个素数，第一问即成立。；若 \(C<2\)，已知对几乎所有 \(n\)，\(F((\log n)^C,n)\sim1\)，故全序列趋于无穷不可能；另一方面，\(\liminf F(c\log n,n)=1\) 与 \(\limsup=\infty\) 只给出两端振荡，逻辑上不蕴含稠密。
- 第一阻塞点：第一问的首个断点是无条件地控制每一个多对数长度区间中的素数；第二、三问更早地卡在无法把素数造成的离散倍增与合数造成的小增量精确调谐到任意目标区间。
- 下一步：固定 \(1<a<b\)，由素数指数的精确增量公式枚举使 \(\log F\in(\log a,\log b)\) 的充分局部条件，再判断现有短区间筛法是否能让该条件无穷次出现。
- 来源核对：[Erdős Problems #420](https://www.erdosproblems.com/420) 核实了几乎处处趋于 \(1\)、\(n^{4/9}\) 尺度发散、下极限及条件性结论。
- 时间记账：所在批次墙钟时间按题数均摊约 38.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/420)；既有候选答案（按不可信材料审计）

### #421

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a sequence $1\leq d_1<d_2<\cdots$ with density $1$ such that all products $\prod_{u\leq i\leq v}d_i$ are distinct?
- 题意摘要：求严格递增整数序列 \(D=\{d_i\}\)，其自然密度 \(\lim_{x\to\infty}\#(D\cap[1,x])/x=1\)，并要求对任意两个不同的有限指标区间 \([u,v]\ne[u',v']\)，相应连续块乘积不相等。
- 状态核对：冻结状态为 open。2026 年官方讨论区出现一份声称解决的复杂预印本，但页面仍标 open，且讨论明确记录了符号、局部正则性及几何估计一致性方面的漏洞或待核查点，不能视为已解决。候选答案把 Ruzsa 上界直接描述成 \(1/e\) 也不够可靠；相关强性质还取决于是否允许重复因子。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先严格重建 Selfridge 的 \(1/e\) 路线，再考察能否通过逐尺度删除 \(o(x)\) 个整数把密度提升到 \(1\)。
- 局部结论：相同长度的两个不同连续块自动有不同乘积：若起点较后，则每个对应因子都严格较大。因此碰撞必涉及不同块长。；取有限大素数集 \(P\)，令 \(\Omega_P(n)=\sum_{p\in P}v_p(n)\)，并取 \(A=\{n:\Omega_P(n)=1\}\)。乘积恒等式两边应用完全加性函数 \(\Omega_P\)，即得因子数相同；故递增枚举 \(A\) 后所有连续块乘积互异。；该集合密度为 \((\sum_{p\in P}1/p)\prod_{p\in P}(1-1/p)\)；选取大素数使倒数和趋近 \(1\)，密度可趋近 \(1/e\)。这里必须使用“选定素数的总重数恰为一”，仅说“恰被一个选定素数整除”会因高次幂而不足。
- 第一阻塞点：提升到密度一时，第一处断点是无法证明逐尺度产生的坏碰撞可由 \(o(X)\) 个位于 \([X,2X)\) 的删除点全部击中；现有声称证明正依赖尚未核严的一致整点估计和局部正则性。
- 下一步：把最新声称证明的“每条分离变量曲线在次数 \(d\asymp\log X\) 时仅有 \(X^{o(1)}\) 个整点”写成带次数、高度及不可约分量量词的独立引理，并逐一核对引用定理是否真正一致适用。
- 来源核对：[Erdős Problems #421](https://www.erdosproblems.com/421) 仍列 open，但标记有未经确认的 claimed solution。；[#421 讨论区](https://www.erdosproblems.com/forum/thread/421) 记录了该声称证明的具体漏洞及对次数/高度一致性的担忧。；[Erdős Problems #786](https://www.erdosproblems.com/786) 核实 Selfridge 构造及“允许重复”版本的歧义。
- 时间记账：所在批次墙钟时间按题数均摊约 38.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/421)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/421.lean`；既有候选答案（按不可信材料审计）

### #422

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(1)=f(2)=1$ and for $n>2$\[f(n) = f(n-f(n-1))+f(n-f(n-2)).\]Does $f(n)$ miss infinitely many integers? What is its behaviour?
- 题意摘要：从 \(f(1)=f(2)=1\) 开始；对每个 \(n>2\)，仅当两个下标 \(n-f(n-1)\)、\(n-f(n-2)\) 都是已定义的正整数时，令 \(f(n)\) 等于相应两项之和。问题先隐含要求证明递推对所有 \(n\) 有定义，再问其值域的补集是否无限，并寻求长期行为。
- 状态核对：仍为 open；连全局良定义性都未知。候选答案中的远程计算界、遗漏值列表、\(n/2\) 趋势和波动指数均属实验材料，不能替代证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试建立可归纳的不变量 \(1\le f(n)\le n\)。良定义性可由这一上界自举；再尝试用相邻项和的下界闭合上界归纳。
- 局部结论：若递推已定义至 \(n-1\)，且所有 \(k<n\) 满足 \(1\le f(k)\le k\)，则两个新下标均落在 \([1,n-1]\)，所以 \(f(n)\) 至少形式上可定义。；记 \(a=n-f(n-1)\)、\(b=n-f(n-2)\)。在已有上界下，\(f(n)=f(a)+f(b)\le a+b=2n-f(n-1)-f(n-2)\)。；因此若还能证明辅助不变量 \(f(n-1)+f(n-2)\ge n\)，就会推出 \(f(n)\le n\)，并由归纳得到全局良定义；初始若干项确实满足这一辅助不等式。
- 第一阻塞点：第一处断点正是无法归纳证明 \(f(n-1)+f(n-2)\ge n\)：递推下标随前项非单调变化，已知的正性只给出常数级下界，不能补足线性下界。未解决良定义性前，更不能严格讨论所有后期遗漏值。
- 下一步：对已计算前缀检验更有余量且可能闭合的窗口不变量，例如 \(\sum_{j=0}^{r-1}f(n-j)\ge c_r n-O(1)\)，并用区间算术验证递推是否保持；优先寻找能推出 \(f(n)\le n\) 的最小窗口。
- 来源核对：[Erdős Problems #422](https://www.erdosproblems.com/422) 核实序列身份、开放状态及全局良定义性未知。
- 时间记账：所在批次墙钟时间按题数均摊约 38.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/422)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/422.lean`；既有候选答案（按不可信材料审计）

### #423

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1=1$ and $a_2=2$ and for $k\geq 3$ we choose $a_k$ to be the least integer $>a_{k-1}$ which is the sum of at least two consecutive terms of the sequence. What is the asymptotic behaviour of this sequence?
- 题意摘要：令 S_j=∑_{i≤j}a_i。第 k 步从已有块和 S_j−S_i（0≤i<j≤k−1，j−i≥2）中，取严格大于 a_{k−1} 的最小整数。问题要求确定 n→∞ 时 a_n 的增长。
- 状态核对：冻结状态为 open；2026-03 更新的官方页仍标 OPEN。页面已收录后续部分结果：a_n−n 单调无界、a_n=n+Ω(log log n)，以及远弱于预期的幂次上界。因此先前候选关于“只有无界性”的总结已过时，但主渐近仍未解决。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用前缀和差集路线：所有连续块和都是严格凸序列 {S_j} 的差，尝试用凸集差集下界迫使在阈值 a_k 附近出现候选值。
- 局部结论：b_k:=a_k−k 非减，因为 b_{k+1}−b_k=(a_{k+1}−a_k)−1≥0。；最后两项之和合法且大于 a_k，故 a_{k+1}≤a_{k−1}+a_k；从而得到 Fibonacci 型粗界 a_k≤F_{k+1}。；可用块和精确组成 D_k={S_j−S_i:0≤i<j≤k，j−i≥2}；因 S_i 的相邻差 a_i 严格增加，{S_i} 是离散严格凸集。
- 第一阻塞点：差集基数很大并不保证差值集中在 a_k 附近。许多差可能远大于 a_k；而已经越过的整数即使后来成为块和，也不会被贪心过程补选。因此仅凭 |D_k| 无法推出 a_{k+1}−a_k=o(a_k) 或 a_k=n+o(n)。
- 下一步：计算并研究局部分层计数 N_k(t)=|D_k∩(a_k,a_k+t]|；首个可检验目标是寻找绝对常数 C,δ>0，使某个 t≤Ca_k/k^δ 总满足 N_k(t)>0。
- 来源核对：[官方题页](https://www.erdosproblems.com/423) 于 2026-03-23 仍标 OPEN，并列出 Tang、Bolan 的无界性及 Tang 的后续界。
- 时间记账：所在批次墙钟时间按题数均摊约 86.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/423)；既有候选答案（按不可信材料审计）

### #424

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_1=2$ and $a_2=3$ and continue the sequence by appending to $a_1,\ldots,a_n$ all possible values of $a_ia_j-1$ with $i\neq j$. Is it true that the set of integers which eventually appear has positive density?
- 题意摘要：令 A_0={2,3}，A_{t+1}=A_t∪{xy−1:x,y∈A_t，x≠y}，A=⋃_tA_t。所问应解释为是否存在 c>0，使所有充分大 X 都有 |A∩[1,X]|≥cX，即正下密度，而非预设自然密度极限存在。
- 状态核对：冻结状态为 open；2026-03 官方页仍为 OPEN。先前候选正确给出模 3 上界，但其数值实验没有可核来源。Lean 文件采用逐代闭包定义，不过研究定理仍含 sorry。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：从闭包中的仿射映射 T_2(x)=2x−1、T_3(x)=3x−1 构造显式子族，并检查同余结构能否产生筛法下界。
- 局部结论：归纳得 A⊆{0,2} mod 3：初值如此，且 x,y∈{0,2} 时 xy−1∈{0,2}。因此上密度至多 2/3。；由 3∈A 且反复与 2 运算，2^k+1∈A（k≥1）；再与 3 运算得 3·2^k+2∈A（k≥2）。这证明 A 无限，但只给 O(log X) 个不超过 X 的元素。；逐代闭包与“反复追加此前所有不同元素对产生的值”等价：每个有限表达式树在有限代出现，反之每代元素均有这种表达式。
- 第一阻塞点：要由 T_2、T_3 的大量词得到 ≫X 个不同且不超过 X 的值，必须控制不同仿射词之间的碰撞；简单模 2、模 3 信息不足以唯一解码。模 3 障碍本身只给上界。
- 下一步：固定词长 L，枚举 T_2、T_3 作用于 5 的值和碰撞，寻找可由有限模数唯一解码的正规词族；目标是构造至少 cM 个互异词值落在 [1,M]。
- 来源核对：[官方题页](https://www.erdosproblems.com/424) 明确说明“正密度”最可能指正下密度，并核对模 3 障碍。；本地 [424.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/424.lean) 定义了逐代闭包，但定理尚未证明。
- 时间记账：所在批次墙钟时间按题数均摊约 86.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/424)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/424.lean`；既有候选答案（按不可信材料审计）

### #425

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(n)$ be the maximum possible size of a subset $A\subseteq\{1,\ldots,N\}$ such that the products $ab$ are distinct for all $a<b$. Is there a constant $c$ such that\[F(n)=\pi(n)+(c+o(1))n^{3/4}(\log n)^{-3/2}?\]If $A\subseteq \{1,\ldots,n\}$ is such that all products $a_1\cdots a_r$ are distinct for $a_1<\cdots <a_r$ then is it true that\[\lvert A\rvert \leq \pi(n)+O(n^{\frac{r+1}{2r}})?\]
- 题意摘要：首句应将 N 统一为 n：F(n) 是 A⊆[n] 中使无序二元子集 {a,b}↦ab 单射的最大大小。第一问求二阶项是否有固定常数 c。第二问应理解为：对每个固定 r≥2，若所有 r 个互异元素的子集乘积均不同，是否 |A|≤π(n)+O_r(n^{(r+1)/(2r)})。
- 状态核对：原文 N/n 不一致是可修正的记号瑕疵，并非实质畸形。冻结及 2026-06 官方状态均为 OPEN；二元情形目前只有两个正常数倍之间的夹逼。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把选入的半素数 pq 编为二部图边。二元碰撞对应 C_4；一般 r 元碰撞可由长度不超过 2r 的偶圈产生。尝试用禁短偶圈极值估计重建误差指数。
- 局部结论：所有不超过 n 的素数组成合法集合：不同 r-子集的乘积由唯一分解定理区分，故极值至少为 π(n)。；若 |A|≥r+2 且有二元碰撞 ab=cd，则两对必不相交；加入另外 r−2 个共同元素便得到两个不同 r-子集的等积碰撞。因此 r-元唯一性推出二元乘法 Sidon 性，并给出较弱界 |A|≤π(n)+O(n^{3/4}(log n)^{-3/2})。；在半素数图中，C_{2k} 的两组交替边乘积相等；若 k≤r 且有足够圈外元素，可共同填充至 r 个因子。因此相关图必须不含长度至多 2r 的偶圈。
- 第一阻塞点：禁短偶圈只直接控制某个半素数层。对任意整数集合，还需按大素因子和余因子分解所有合数，并把各尺度误差总和压到 O_r(n^{(r+1)/(2r)})。现有二元分解只给 n^{3/4}(log n)^{-3/2}；图极值也不能单独给出第一问所需的稳定极限常数。
- 下一步：先处理 r=3：按 m=p·u（p 为最大素因子）唯一分层，逐层使用 C_4、C_6-free 边界，精确核算总和能否达到 O(n^{2/3})；若某个尺度已超标，即可定位所缺的额外算术约束。
- 来源核对：[官方题页](https://www.erdosproblems.com/425) 核对了 open 状态、Erdős 的 c_1,c_2 两侧界及原文的 N/n 记号不一致。
- 时间记账：所在批次墙钟时间按题数均摊约 86.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/425)；既有候选答案（按不可信材料审计）

### #428

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a set $A\subseteq \mathbb{N}$ such that, for infinitely many $n$, all of $n-a$ are prime for all $a\in A$ with $0<a<n$ and\[\liminf\frac{\lvert A\cap [1,x]\rvert}{\pi(x)}>0?\]
- 题意摘要：量词为：存在一个固定 A⊆ℕ，使得（i）有无穷多个 n，对每个 a∈A 且 0<a<n，n−a 都是素数；（ii）liminf_{x→∞}|A∩[1,x]|/π(x)>0。A、见证 n 与下极限的量词次序不能互换。
- 状态核对：冻结及当前官方状态均为 open。untrusted_prior_candidate 完全复制了第 425 题，与本题无关，故整体弃用。Lean 陈述核对了上述量词次序，但仍含 answer(sorry)。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：令 B 为见证 n 的集合，研究 A 与 B 的模素数相容性：若 n∈B，则除差恰为该素数外，A 不能在 n 的同余类中出现。
- 局部结论：A 必为无限集，因为正下极限相对 π(x) 强迫 |A∩[1,x]|→∞。；若 n<m 是两个足够大的见证且 d=m−n 为奇数，则 n−a 与 m−a 是相差奇数的两个素数，只能较小者等于 2。因此所有 a∈A∩[1,n) 都须等于 n−2，故该截断至多一个元素，矛盾。于是所有充分大的见证具有同一奇偶性。；对任意素数 q，若 n<m 是同余模 q 的见证，则 A∩[1,n) 中不存在 a≡n mod q，否则 n−a、m−a 均为被 q 整除的素数，却不可能同时等于 q。由鸽巢原理，B 在模 q 的某个剩余类中无穷出现，进而 A 必完全避开该剩余类。
- 第一阻塞点：“对每个素数模数避开一个剩余类”与 |A(x)|≈x/log x 完全相容，典型筛集正有这个量级。要产生同一个 A 的正下密度和无穷多个见证，必须对不断增长的全部截断同时实现素数条件；素数 k-元组猜想只处理每次有限的可容许族，不能自动提供跨尺度一致性及 liminf 控制。
- 下一步：构造有限层模型：选取每个 q≤y 的禁余类 r_q，令 A_y={a≤X:a≠r_q mod q 对所有 q≤y}；检验能否选择 n≡r_q mod q，使有限移位族 {n−a:a∈A_y} 对每个素数均可容许。
- 来源核对：[官方题页](https://www.erdosproblems.com/428) 仍标 OPEN，仅记录在假设素数 k-元组猜想并把 liminf 换成 limsup 后可得肯定结果。；本地 [428.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/428.lean) 核对了 ∃A、无穷多个 n、∀a 及 liminf 的量词顺序。
- 时间记账：所在批次墙钟时间按题数均摊约 86.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/428)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/428.lean`；既有候选答案（按不可信材料审计）

### #430

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Fix some integer $n$ and define a decreasing sequence in $[1,n)$ by $a_1=n-1$ and, for $k\geq 2$, letting $a_k$ be the greatest integer in $[1,a_{k-1})$ such that all of the prime factors of $a_k$ are $>n-a_k$. Is it true that, for sufficiently large $n$, not all of this sequence can be prime?
- 题意摘要：按官方例 n=8 在 7,5 后停止，候选项必须理解为 m>1；否则 1 会因没有素因子而空真地合格，使题目平凡化。对固定 n，序列正是所有 m∈{2,…,n−1} 且每个素因子均大于 n−m 的数，按降序列出。所问是充分大 n 时列表中是否必有合数。
- 状态核对：冻结及 2026-06 官方状态均为 open。先前候选正确注意到 1 的歧义，但不能据字面空真宣称问题平凡；官方停止例确定了预期约定。候选列出的巨大计算例没有核验，故不采用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：以 P^-(m) 表示合数 m 的最小素因子，把问题归约为在 n 左侧寻找距离 h=n−m 小于 P^-(m) 的合数，并先覆盖显式可构造的 n 区间。
- 局部结论：合数 m 合格当且仅当 P^-(m)>n−m，即 m+P^-(m)>n。令 F(n)=max_{2≤m<n,m合数}(m+P^-(m))，题目等价于问充分大 n 是否总有 F(n)>n。；若 n−1 为合数，则首项已经解决；故任何非平凡例外 n 必须是偶数且 n−1 为素数。又因 P^-(m)≤√m，合格合数必满足 m>n/2 且 n−m<√n。；若 p 为素数且 p²<n<p²+p，则 m=p² 合格，因为 n−m<p=P^-(m)。所以素数平方之后长度 p−1 的区间全部得到肯定结论。
- 第一阻塞点：必须覆盖每个充分大的 n：即在其左侧距离小于 √n 内找到合数 m，并且最小素因子仍大于该距离。素数平方后的显式区间之间有大空档；一般筛法又需区分素数与恰有两个大因子的数，初等覆盖在此处停止。
- 下一步：对 h≤√n 分层计数 n−h=uv、h<u≤v 的解；先尝试证明平均版本：对 N<n≤2N 中除 o(N) 个 n 外，存在 h≤N^{1/2}/log N 的此类分解，再识别从“几乎所有”升级到“所有”所需的最大间隙估计。
- 来源核对：[官方题页](https://www.erdosproblems.com/430) 仍标 OPEN，给出 n=8 后停止的约定，并记录其与 #385 第一部分的等价性。
- 时间记账：所在批次墙钟时间按题数均摊约 86.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/430)；既有候选答案（按不可信材料审计）

### #431

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there two infinite sets $A$ and $B$ such that $A+B$ agrees with the set of prime numbers up to finitely many exceptions?
- 题意摘要：问是否存在无限集 A,B⊂ℕ，使得存在 N₀，对每个 n≥N₀，n 为素数当且仅当 n∈A+B={a+b:a∈A,b∈B}；即 (A+B)△P 有限。
- 状态核对：截至官方页面 2026-04-08 更新仍为开放的 Ostmann 逆 Goldbach 问题。候选答案仅正确报告了状态和已知计数界，并未提供证明；其中关于“带符号素数/Ruzsa”的附加说法既非本题路线，也未由给定官方材料支持，故不采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试以小模数筛法推出矛盾。对素数 q，令 R_A(q)、R_B(q) 分别为 A、B 中出现无穷多次的模 q 剩余类。若 r∈R_A(q)、s∈R_B(q)，可选任意大的 a≡r、b≡s；因 a+b 最终必须为素数，故 r+s≠0 mod q。于是 R_A(q)+R_B(q)⊂𝔽_q\{0}。
- 局部结论：取 q=2 得 R_A(2)、R_B(2) 都是单点且互为相反类；换言之，删去有限项后 A、B 各有固定且相反的奇偶性。；由 Cauchy–Davenport，|R_A(q)+R_B(q)|≥|R_A(q)|+|R_B(q)|−1，而左侧至多 q−1，故 |R_A(q)|+|R_B(q)|≤q。；若取有限截集 A∩[1,x/2]、B∩[1,x/2]，则 |(A+B)∩[1,x]|≥A(x/2)+B(x/2)−1；结合素数计数得到 A(x/2)+B(x/2)≤π(x)+O(1)，但远弱于已知 Elsholtz–Harper 界。
- 第一阻塞点：第一处不能闭合之处是：对每个 q 的支持约束 |R_A(q)|+|R_B(q)|≤q 完全可能同时成立，例如两集分别集中在单一剩余类；这些局部条件本身不能推出某个大合数必在 A+B 中。把多模约束转化为全局计数矛盾正是需要深筛法而仍未解决的部分。
- 下一步：可检验任务：对平方自由 Q=∏_{q≤z}q，建立 R_A(Q)、R_B(Q) 的兼容支持上界，并检查结合 A(x),B(x) 的已知下界能否改进现有大筛常数；目标应是明确的新必要条件，而非宣称否定分解。
- 来源核对：[Erdős Problems #431](https://www.erdosproblems.com/431) 核实开放状态、精确表述及 Elsholtz–Harper 界。；[Elsholtz–Harper 论文预印本](https://arxiv.org/abs/1309.0593) 核实其研究的是渐近加法分解，而非已解决二元情形。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/431)；既有候选答案（按不可信材料审计）

### #432

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A,B\subseteq \mathbb{N}$ be two infinite sets. How dense can $A+B$ be if all elements of $A+B$ are pairwise relatively prime?
- 题意摘要：给定无限 A,B⊂ℕ，令 S=A+B；要求任意两个不同的 s,t∈S 满足 gcd(s,t)=1。题目问 S 能有多稠密，但未指定采用上密度、下密度还是计数函数的最优阶。以下采用 S(x)=|S∩[1,x]|。
- 状态核对：官方页面仍列为开放。候选答案中的最小素因子注入是正确的，但它只给出适用于任意两两互素集合的通用上界，没有利用 S 是两个无限集的完整和集，因此不是问题的解决。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先把每个 s>1 映到其最小素因子 p(s)，再用一维和集不等式把 A、B 的计数函数与 S(x) 联系起来。
- 局部结论：因不同 s,t∈S 不共享素因子，s↦p(s) 为单射，故 S(x)≤π(x)+1=(1+o(1))x/log x；特别地 S 的上渐近密度为零。；对 A_x=A∩[1,x/2]、B_x=B∩[1,x/2]，整数和集不等式给出 |A_x+B_x|≥|A_x|+|B_x|−1，因此 A(x/2)+B(x/2)−1≤S(x)。；合并可得 A(x/2)+B(x/2)≤π(x)+2，所以两个加数集各自也至多具有 O(x/log x) 的该尺度计数。
- 第一阻塞点：最小素因子注入对任意两两互素集合已经基本尖锐（素数集本身达到 π(x) 量级），故无法单靠它排除 S(x)≈x/log x。第一处缺口是尚无论证把“完整笛卡尔和集”结构转化为额外共享素因子或更强的计数损失。
- 下一步：固定 b₁≠b₂∈B，系统研究条件 gcd(a+b₁,a+b₂)=1，即 gcd(a+b₁,b₂−b₁)=1；对许多差 b₂−b₁ 联合筛 A，检验能否得到 A(x)=o(x/log x)，再与对称下界结合。
- 来源核对：[Erdős Problems #432](https://www.erdosproblems.com/432) 核实题目仍开放，且官方没有声称现有部分解。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/432)；既有候选答案（按不可信材料审计）

### #436

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $p$ is a prime and $k,m\geq 2$ then let $r(k,m,p)$ be the minimal $r$ such that $r,r+1,\ldots,r+m-1$ are all $k$th power residues modulo $p$. Let\[\Lambda(k,m)=\limsup_{p\to \infty} r(k,m,p).\]Is it true that $\Lambda(k,2)$ is finite for all $k$? Is $\Lambda(k,3)$ finite for all odd $k$? How large are they?
- 题意摘要：对固定 k,m≥2 及素数 p，r(k,m,p) 是最小正整数 r，使 r,…,r+m−1 都属于 (𝔽_p^×)^k（有限个 p≤r+m 可另行处理）；Λ(k,m)=limsup_{p→∞}r(k,m,p)。问题包含三部分：所有 k 的 m=2 有界性、所有奇 k 的 m=3 有界性，以及这些量随 k 的大小。
- 状态核对：这是部分已解决、整体仍开放的问题：Hildebrand 已证明每个固定 k 都有 Λ(k,2)<∞；Λ(3,3)=23532，而奇数 k≥5 的三连问题及增长率仍开放。候选答案正确区分了这些部分，但其数值表只是状态汇总，不构成证明。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：把 k 次幂剩余性放入商群 G_p=𝔽_p^×/(𝔽_p^×)^k；它是阶 d=gcd(k,p−1) 的循环群。尝试寻找一个只依赖 k 的有限整数集合，使整数间的乘法恒等式迫使某对或某三连整数在 G_p 中同时为单位元。先重建 k=2 的有限强迫论证。
- 局部结论：k=2 时，1、4、9 恒为平方剩余。若 2 是平方剩余，则 (1,2) 成功；否则若 5 是平方剩余，则 (4,5) 成功；若 2、5 都非剩余，则其乘积 10 是平方剩余，故 (9,10) 成功。因此对所有充分大的奇素数 r(2,2,p)≤9。；一般情形中 G_p 的阶总是整除 k；所以证明 Λ(k,2)<∞ 可归约为对有限多个循环群阶 d|k 建立统一的有限乘法强迫引理。；若 gcd(k,p−1)=1，则幂映射 x↦x^k 是 𝔽_p^× 的双射，因而 r(k,m,p)=1（对 p>m）；真正的困难只来自 gcd(k,p−1)>1 的素数。
- 第一阻塞点：二次情形使用了“两个非剩余之积必为剩余”，即商群阶为 2；当 d>2 时，两个非单位元的乘积未必为单位元。因而该三分法不能推广。三连情形还需要同时控制三个相邻整数，现有乘法恒等式没有给出所需有限强迫引理。
- 下一步：可检验任务：固定 k=5，把小整数分解产生的关系编码为 C₅ 中的有限约束满足问题，搜索最小 R，使任何满足乘法关系的标号都迫使某个 r,r+1 同标为 0；随后逐条验证搜索证书能否转成 Hildebrand 型有限组合引理。三连版本则先测试同一编码是否存在任意长无三连标号。
- 来源核对：[Erdős Problems #436](https://www.erdosproblems.com/436) 核实 Hildebrand 已解决二连有界性、Λ(3,3)=23532 及剩余开放部分。；[OEIS A000445](https://oeis.org/A000445) 仅用于交叉核对小 k 数值和 Hildebrand 文献，不把数据库条目当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/436)；既有候选答案（按不可信材料审计）

### #445

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for any $c>1/2$, if $p$ is a sufficiently large prime then, for any $n\geq 0$, there exist $a,b\in(n,n+p^c)$ such that $ab\equiv 1\pmod{p}$?
- 题意摘要：量词是：对每个实数 c>1/2，存在 P₀(c)，使每个素数 p≥P₀(c) 及每个整数 n≥0，都存在自然数 a,b 满足 n<a,b<n+p^c 且 ab≡1 mod p。n 可远大于 p，故本质上要求每个长度约 p^c 的循环剩余区间 I 都与其逆像 I^{-1} 相交。
- 状态核对：本地 Lean 陈述与上述量词一致：∀c，最终对所有 p，若 p 为素数则 ∀n 存在 a,b。官方仍列开放；已知 Heath-Brown 用 Kloosterman 和证明 c>3/4。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令 H≈p^c，并计数 N(I)=#{x∈I mod p:x^{-1}∈I}。展开区间指示函数的离散 Fourier 级数，非零频率给出完整 Kloosterman 和；用 Weil 界和区间 Fourier 系数的 L¹ 界估计误差。
- 局部结论：标准展开给出 N(I)=H²/p+O(p^{1/2}(log p)²)，对循环区间的位置一致；端点及跨越 0 只贡献 O(1) 调整。；若 c>3/4，则 H²/p=p^{2c−1} 最终严格大于 p^{1/2}(log p)²，所以 N(I)>0，重建了已知的 c>3/4 结论。；阈值 1/2 是必要的：若 c<1/2，取 n=1；充分大 p 时 1<a,b<1+p^c<√p，故 1<ab<p，不可能 ab≡1 mod p。
- 第一阻塞点：第一处不能闭合的是 c∈(1/2,3/4]：上述点态误差 O(p^{1/2}log²p) 可能大于主项 H²/p。仅重复 Weil 界或改变 Fourier 截断不能产生所需的额外抵消。候选答案关于更强猜想只能到 2/3 的旁论不影响这一缺口，故不作为结论。
- 下一步：可检验任务：研究所有平移 I 的二阶或高阶矩 ∑_n|N(I_n)−H²/p|²，并明确它是否能从“多数 n”升级到“每个 n”；若不能，应构造达到大误差的平移以定位必须改进的点态估计。
- 来源核对：[Erdős Problems #445](https://www.erdosproblems.com/445) 核实开放状态及 c>3/4 的已知结果。；[Heath-Brown 原文](https://www.nieuwarchief.nl/serie5/pdf/naw5-2000-01-4-380.pdf) 给出计数主项及 O(p^{1/2}log²p) 型误差。；已读取本地 FormalConjectures/ErdosProblems/445.lean，确认形式化量词没有把 n 限制到 [0,p)。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/445)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/445.lean`；既有候选答案（按不可信材料审计）

### #450

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：How large must $y=y(\epsilon,n)$ be such that the number of integers in $(x,x+y)$ with a divisor in $(n,2n)$ is at most $\epsilon y$?
- 题意摘要：令 D_n={m∈ℤ:存在整数 d，n<d<2n 且 d|m}。题面问区间 (x,x+y) 内 D_n 元素至多 εy 时 y 应多大，但没有说明对 x 是“所有 x”“某个 x”还是平均 x，也没有说明是存在一个 y 还是所有充分大的 y；这些选择会改变问题。
- 状态核对：应判为量词不完整。更严重的是，官方备注按字面称在“∀x”解释下，当 ε(log n)^δ(loglog n)^{3/2}→∞ 时无此 y；这与周期性给出的直接构造方向相反。候选答案关于密度障碍的方向较合理，但它擅自固定了 ∀x，不能视为原题答案。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `high`
- 尝试路线：先作不依赖深定理的周期性一致性检查。令 Q=lcm(n+1,…,2n−1)。D_n 是模 Q 的剩余类并，因此具有有理自然密度 ρ_n=|D_n∩[1,Q]|/Q。再对长度为 Q 或其倍数的窗口计数。
- 局部结论：采用半开整数窗口 (x,x+Q] 时，每个窗口恰含 ρ_nQ 个 D_n 元素；严格开区间只产生 O(1) 端点误差。因此若 ε>ρ_n，取充分大的 Q 的倍数即可使所有 x 的计数≤εy。；反之，对起点 x 在一个周期内平均，长度 Y 窗口的平均计数为 ρ_nY+O(1)。所以若要求对所有 x 且 Y→∞，ε<ρ_n 时必有某个窗口违反上界。；Ford 的结果给 ρ_n 的量级约为 1/((log n)^δ(loglog n)^{3/2})，δ≈0.08607。因此 ε(log n)^δ(loglog n)^{3/2}→∞ 表示 ε≫ρ_n，恰落在上述周期构造可行的一侧，而不是“无 y”的一侧。
- 第一阻塞点：第一处无法闭合并非估计技术，而是原始量词缺失；此外官方备注的渐近方向与严格周期论证冲突。在澄清“至多/至少”、x 的量词以及 y 的阈值含义前，所谓 y(ε,n) 没有唯一数学定义。严格开区间在 y≤1 时甚至可能不含整数，更显示必须规定离散端点约定。
- 下一步：首要可检验任务：查阅 ErGr80 第89页原文，核对不等号及 x、y 的量词。若确定为“∀x、所有 Y≥y”，则正式定义极值函数，并先证明其存在当且仅当 ε≥ρ_n（边界 ε=ρ_n 需处理端点）；若为“∃x”，则用周期平均给出完全不同的基准上界。
- 来源核对：[Erdős Problems #450](https://www.erdosproblems.com/450) 核实原页面确实缺少 x 的量词，并逐字核对了存在方向冲突的 Cambie 备注。；[Ford, Annals of Mathematics 168 (2008)](https://annals.math.princeton.edu/2008/168-2/p01) 核实其研究整数具有指定区间内因子的计数阶；此处只采用官方给出的 ρ_n 量级，不冒充重建 Ford 的深层证明。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/450)；既有候选答案（按不可信材料审计）

### #451

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Estimate $n_k$, the smallest integer $>2k$ such that $\prod_{1\leq i\leq k}(n_k-i)$ has no prime factor in $(k,2k)$.
- 题意摘要：对每个整数 k，令 n_k 为最小的整数 n>2k，使连续块 n-k,…,n-1 的乘积不被任何素数 p∈(k,2k) 整除；问题要求估计 n_k 随 k 的增长。
- 状态核对：仍为开放问题，但输入截至 2025-08-31 的背景已过时：2026 年 van Doorn–Tang 已证明 n_k>exp((log k)^2/(20 log log k))（充分大 k），从而得到超多项式下界；尚未得到预期的 exp(Θ(k/log k)) 量级。先前候选把周期密度的倒数当作首个命中的尺度，这只能是启发式，不能推出 n_k 的估计；其“数值上明显次指数”也不是证明。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：令 P_k={p素数:k<p<2k}、M_k=∏_{p∈P_k}p。先严格计算可行整数在模 M_k 下的密度，再尝试由密度控制最小正代表。对每个 p，坏剩余恰为 n≡1,…,k (mod p)，故可行剩余有 p-k 个；CRT 给出密度 D_k=∏_{k<p<2k}(1-k/p)。截去 p-k 很小的端点、用素数定理并对端点作筛上界，可严格得到 log D_k^{-1}=(log 4+o(1))k/log k。
- 局部结论：可行集合是模 M_k 的周期集合，恰有 ∏_{k<p<2k}(p-k) 个剩余类。；D_k=exp(-(log 4+o(1))k/log k)；这里常数来自 ∫_1^2-log(1-1/u)du=log 4，但端点奇性必须单独控制。；取 n=2M_k 总是满足所有模 p 条件且 n>2k，故 n_k≤2M_k=exp(O(k))；充分大 k 时也可取 M_k。结合 2026 年结果已有 n_k>exp((log k)^2/(20loglog k))。
- 第一阻塞点：第一处不能闭合的是“周期密度 D_k ⇒ 区间 (2k,C/D_k] 内必有可行代表”。任意周期集合即使密度已知，其最小正代表仍可能远大于平均间距；CRT 类之间存在强相关，第一矩或平均间距论证不能排除初始长空段。
- 下一步：可检验任务：对可行剩余类在 [1,H] 的计数建立二阶矩/大筛下界，先测试 H=exp(Ck/log k) 时能否证明计数非零；明确记录误差是否小于主项 HD_k。
- 来源核对：官方页面目前仍标为 OPEN，并已收录 2026 年超多项式下界：https://www.erdosproblems.com/451；van Doorn–Tang 原始预印本及明确常数 1/20：https://arxiv.org/abs/2606.19863
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/451)；既有候选答案（按不可信材料审计）

### #452

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\omega(n)$ count the number of distinct prime factors of $n$. What is the size of the largest interval $I\subseteq [x,2x]$ such that $\omega(n)>\log\log n$ for all $n\in I$?
- 题意摘要：令 L(x) 为 [x,2x] 中最长连续整数块 I 的基数，使每个 n∈I 都满足 ω(n)>log log n；问题询问 L(x) 的真实增长阶，量词是 x→∞。
- 状态核对：开放。密度为 1/2 只描述全局比例，不能控制最长连续段。先前候选的 CRT 主线正确，但“模数 M≤x 即可”遗漏右端点：应安排 M+L≤x，或留出等价余量。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：尝试严格重建 CRT 下界。取 r=⌊log log(2x)⌋+1，取 rL 个互异小素数并分为 L 块 B_0,…,B_{L-1}，每块 r 个。施加 N+j≡0 (mod p)（p∈B_j）。CRT 给出唯一剩余类模 M=∏p；若 M+L≤x，则可选该类代表 N∈[x,2x-L]。
- 局部结论：每个 N+j 被块 B_j 中的 r 个不同素数整除，故 ω(N+j)≥r>log log(N+j)。；由第 y 个素数乘积的对数渐近 y log y，取 L=(1-o(1))log x/(log log x)^2 可使 log M≤log(x-L)。；因此 L(x)≥(1+o(1))log x/(log log x)^2；这里 1+o(1) 应理解为与该表达式比值下界趋于 1。
- 第一阻塞点：第一处不能闭合的是把此构造提升到 L≫log x/(loglog x)^2。当前方案每个位置消耗约 loglog x 个新素数，而当偏移差小于所用素数时，同一素数不能同时满足两个不同偏移的整除同余；素数预算遂给出上述屏障。全局密度 1/2 对突破该屏障无帮助。
- 下一步：把“素数 p 选择一个剩余类并覆盖偏移 j≡a_p (mod p)”写成有限覆盖优化问题；计算在约束每个偏移被至少 r 次覆盖、log M≤log x 下，小素数复用能否使 L 超过 CRT 基准常数或量级。
- 来源核对：官方页面确认 OPEN、密度 1/2 及 CRT 下界：https://www.erdosproblems.com/452；输入所引 Erdős 1937 结果仅支持总体密度，不能推出最长游程。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/452)；既有候选答案（按不可信材料审计）

### #454

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[f(n) = \min_{i<n} (p_{n+i}+p_{n-i}),\]where $p_k$ is the $k$th prime. Is it true that\[\limsup_n (f(n)-2p_n)=\infty?\]
- 题意摘要：对第 n 个素数 p_n，定义 f(n)=min_{1≤i<n}(p_{n+i}+p_{n-i})。问题等价于：对每个 A 和 N，是否存在 n≥N，使所有 1≤i<n 都有 p_{n+i}+p_{n-i}-2p_n≥A？
- 状态核对：开放；Pomerance 已证明该 limsup 至少为 2。先前候选的状态判断与此一致，但“局部素数间隙不对称”必须同时对全部 i 控制，不能只考察 i=1。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：令 d_j=p_{j+1}-p_j。则对每个 i，Δ_i(n):=p_{n+i}+p_{n-i}-2p_n=∑_{r=0}^{i-1}d_{n+r}-∑_{r=1}^{i}d_{n-r}。尝试选取素数图点 (n,p_n) 的严格下凸包顶点；支撑直线可同时保证所有 Δ_i(n)>0。
- 局部结论：精确恒等式 f(n)-2p_n=min_{1≤i<n}Δ_i(n)，所以问题要求所有前后累计间隙差同时很大。；除涉及素数 2 的小指标外，p_{n+i}+p_{n-i}-2p_n 为偶数；因此严格正性自动提升为至少 2。；严格下凸包顶点给出 Δ_i(n)>0（所有允许 i），从而解释几何方法为何自然只能直接产生下界 2。
- 第一阻塞点：第一处不能闭合的是从“严格位于弦下方”推出到弦的竖直距离趋于无穷。凸包只给严格正距离；整性和奇偶性仅把它量化为 2，没有任何机制排除无穷多个顶点的最小裕量始终等于 2。即使强素数元组猜想也不直接控制这些稀疏极点。
- 下一步：计算并证明一个可审计的有限命题：对给定 A，若某凸包顶点两侧斜率与所有有理数 a/i（1≤i≤H）保持显式距离，则 min_{i≤H}Δ_i(n)>A；随后检查能否由已知素数间隙结果产生这种斜率分离。
- 来源核对：官方页面确认 OPEN 及 Pomerance 的 limsup≥2：https://www.erdosproblems.com/454；本地 Lean 文件核对了 i 的范围为 0<i<n；其自然数截断减法不表达负裕量，但对“limsup=∞”这一目标无实质影响。；Pomerance 原论文书目信息：Math. Comp. 33 (1979), 399–408。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/454)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/454.lean`；既有候选答案（按不可信材料审计）

### #455

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $q_1<q_2<\cdots$ be a sequence of primes such that\[q_{n+1}-q_n\geq q_n-q_{n-1}.\]Must\[\lim_n \frac{q_n}{n^2}=\infty?\]
- 题意摘要：量词为：对任意严格递增的无限素数序列 q_1<q_2<⋯，若差 d_n=q_{n+1}-q_n 对所有 n 都非递减，是否必有 q_n/n²→∞？
- 状态核对：开放。Richter 证明 liminf q_n/n²>0.352…；先前候选只是复述状态，没有给出可检验路线。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：尝试从素数性限制相同差值的连续平台。若 d_n=d 连续出现 ℓ 次，则相应 q 项构成公差 d 的素数等差数列。对任意不整除 d 的素数 r，长度达到 r 时某项必为 0 (mod r)，除至多一个等于 r 的例外；因此平台长度受最小不整除 d 的素数控制。
- 局部结论：除序列可能包含 2 的初段外，所有 d_n 都是正偶数，且改变时至少增加 2。；若 d 的所有小素数因子只到 y，则 d≥∏_{p≤y}p=exp((1+o(1))y)；反过来，最小不整除 d 的素数为 O(log d)。故差值 d 的连续平台长度至多 O(log d)，忽略一个可单独处理的异常项。；结合差值每次至少增加 2，这一路线至多自然导向 d_n≳n/log n、q_n≳n²/log n，甚至弱于 Richter 的正二次常数；它说明仅控制平台不足以解决问题。
- 第一阻塞点：第一处不能闭合的是把单个平台的 O(log d) 上界变成平均平台长度 o(1)，而后者才可能强迫 d_n/n→∞。不同递增差值对应不同模结构，逐个平台的等差数列筛法没有跨平台累积排斥。
- 下一步：重建 Richter 三页论文中的筛计数，明确常数 0.352…来自哪个有限优化；然后在反设 q_N≤CN² 下，把前 N 项按差值区间分桶，检验跨桶大筛是否能给出随 C 改善并最终排除每个固定 C。
- 来源核对：官方记录及原问题状态：https://www.erdosproblems.com/455；Richter 原论文元数据及全文入口：https://eudml.org/doc/205474；本地 Lean 文件正确表达了严格递增、逐项素数、非递减差值及 Tendsto 到 +∞；从 0 开始编号不影响尾部命题。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/455)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/455.lean`；既有候选答案（按不可信材料审计）

### #456

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p_n$ be the smallest prime $\equiv 1\pmod{n}$ and let $m_n$ be the smallest integer such that $n\mid \phi(m_n)$. Is it true that $m_n<p_n$ for almost all $n$? Does $p_n/m_n\to \infty$ for almost all $n$? Are there infinitely many primes $p$ such that $p-1$ is the only $n$ for which $m_n=p$?
- 题意摘要：对每个正整数 n，p_n 是最小的满足 p≡1 (mod n) 的素数，m_n=min{m≥1:n|φ(m)}。三问分别是：(A) m_n<p_n 是否在自然密度 1 的 n 上成立；(B) 是否对每个固定 C，p_n/m_n≤C 的 n 密度趋零；(C) 是否有无穷多个素数 p，使对所有正整数 n，m_n=p 当且仅当 n=p-1。
- 状态核对：三问目前均开放。先前候选给出的等号族、二幂严格不等族及 Fermat 素数的条件性唯一性基本正确；但这些零密度族不能回答“几乎所有”。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先从 φ 的显式构造刻画可证关系。总有 m_n≤p_n，因为 n|φ(p_n)。进一步尝试用 n 的素因子分解构造较小的合数 m，并将第三问化为检查 p-1 的所有真因子。
- 局部结论：m_n为素数当且仅当m_n=p_n：若m_n=r为素数，则n|r-1，故r≥p_n；反向由m_n≤p_n得等号。因此(A)等价于m_n为合数对几乎所有n成立。；若n=q-1且q为素数，则m_n=p_n=q；另一方面，若n=2^{2k+1}，则m_n≤2n，而n+1被3整除，故p_n≥2n+1，得到无穷多个严格不等例子。；一般取m=n·rad(n)，有φ(m)=n∏_{ℓ|n}(ℓ-1)，故m_n≤n·rad(n)。若p为Fermat素数、p-1=2^s，则其任意真因子n=2^r满足m_n≤2n<p，而m_{p-1}=p；故此类p满足(C)的唯一性。
- 第一阻塞点：对(A)(B)，第一处不能闭合的是把合数候选 m≤n·rad(n) 与最小同余素数 p_n 作密度一比较：Linnik 只给 p_n 的上界，不能证明 p_n 通常大于所构造的 m，更不能给比值趋∞。对(C)，Fermat 素数路线卡在是否存在无穷多个 Fermat 素数这一著名开放问题。
- 下一步：可检验任务：对 n≤X 枚举 m_n，并按 n 的最大素因子、rad(n)/n 分层，测试简单候选 n·rad(n) 或各素数幂候选何时真正小于 p_n；目标是提出一个可由现有平均最小同余素数定理处理、且覆盖密度 1 的充分条件。
- 来源核对：官方页面确认三问均保持 OPEN，并记录 Linnik、等号族和二幂族：https://www.erdosproblems.com/456；独立核算了 n·rad(n) 构造、m_n为素数与m_n=p_n的等价，以及 Fermat 素数的唯一性论证；这些均不依赖先前候选所引二手资料。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/456)；既有候选答案（按不可信材料审计）

### #457

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is there some $\epsilon>0$ such that there are infinitely many $n$ where all primes $p\leq (2+\epsilon)\log n$ divide\[\prod_{1\leq i\leq \log n}(n+i)?\]
- 题意摘要：求证存在固定 ε>0，使得满足下述条件的自然数 n 有无穷多个：每个素数 p≤(2+ε)log n 都整除 ∏_{1≤i≤⌊log n⌋}(n+i)。
- 状态核对：已肯定解决；官方页面于 2026-03-07 标为 proved (Lean)。旧候选所称“仍开放”已经过时。需注意：本地 FormalConjectures 文件中的主定理仍以 sorry 占位，真正证明位于其标注的外部 Lean 文件。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建外部形式证明的构造。取 A=binom(2m,m)，Q={q 素数:2m<q≤3m}。由同时丢番图逼近选 1≤k≤6^|Q|，使每个 q∈Q 都有整数 ℓ 满足 |kA−ℓq|<q/6；令 c=⌊3m/5⌋、n=kA−c。按 p≤m、m<p≤2m、2m<p≤3m 三段证明短区间 (n,n+log n] 含 p 的倍数，并控制 2.1log n<3m。
- 局部结论：p≤m 时，因 log n≥1.2m≥p，任意连续 ⌊log n⌋ 个整数包含 p 的倍数。；m<p≤2m 时 p|A，故 p|(n+c)，且 1≤c≤⌊log n⌋。；2m<p≤3m 时令 r=kA−ℓp；由 |r|<p/6≤m/2，取 i=c−r，可验证 1≤i≤⌊log n⌋ 且 p|(n+i)。
- 第一阻塞点：原问题的证明路线已经闭合，外部 Lean 定理取 ε=0.1。当前审计层面的缺口只是尚未在指定 mathlib/Lean 版本下重新编译外部文件；本地文件自身的 sorry 不能单独充当证明证书。
- 下一步：在 Lean 4.24.0、指定 mathlib commit 下无 sorry 重编译外部 ErdosProblem457.lean，并核对 #print axioms 仅含标准公理。
- 来源核对：官方页面确认肯定解决及构造概要：https://www.erdosproblems.com/457；外部完整 Lean 证明：https://raw.githubusercontent.com/Woett/Lean-files/main/ErdosProblem457.lean；本地 457.lean 的 erdos_457 仍为 sorry，但元数据指向上述外部证明。
- 时间记账：所在批次墙钟时间按题数均摊约 40.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/457)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/457.lean`；既有候选答案（按不可信材料审计）

### #460

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $a_0=n$ and $a_1=1$, and in general $a_k$ is the least integer $>a_{k-1}$ for which $(n-a_k,n-a_i)=1$ for all $1\leq i<k$. Does\[\sum_{i}\frac{1}{a_i}\to \infty\]as $n\to \infty$? What about if we restrict the sum to those $i$ such that $n-a_j$ is divisible by some prime $\leq a_j$, or the complement of such $i$?
- 题意摘要：按输入的字面版本：固定 n，a0=n、a1=1；对 k≥2，ak 是大于 a(k−1) 且使 gcd(n−ak,n−ai)=1（1≤i<k）的最小整数。问整个无限序列的倒数和及两个按 n−ai 的小素因子条件划分的子和，随 n→∞ 是否发散。
- 状态核对：输入版本缺少官方当前主表述中的限制 0<ai<n，且初值、互素指标也不同。字面版本事实上平凡发散；真正标为 open 的是有限截断版本。旧候选对无限延拓的核心观察基本正确，但不应把它当作解决官方开放问题。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：令 bi=n−ai。则 bi 严格递减，且新项是小于前项、与所有既有 bj 互素的最大整数。对 n≥3，正整数阶段有限，必到达 b=1；随后 b=−1，并考察所有先前已经“占用”的素因子。
- 局部结论：在到达 b=1 前，每个素数 p<n 必已整除某个先前 bj；否则扫描到 b=p 时它合格，不可能被越过。；越过 −1 后，下一个绝对值是最小的未占用素数；归纳得序列包含 ai=n+p，其中 p 依次遍历所有 p≥n 的素数。；因此字面总和至少为 ∑_{p≥n}1/(n+p)≥(1/2)∑_{p≥n}1/p=∞；这些尾项也全部属于“存在素数 q≤ai 且 q|(n−ai)”一类。
- 第一阻塞点：字面版本没有未闭合步骤；真正的第一处障碍出现在改回 0<ai<n 后：素数尾被截掉，必须对每个 n（而非平均意义）证明有限贪心序列贡献无界。官方只记录了相关粗糙数函数在 n 上的平均下界。另有 n=1,2 等边界退化，不能无条件照搬无限尾描述。
- 下一步：固定官方有限版本，严格证明或反驳下界 ∑_{a<n}1_{P^-(n-a)>a}1/a→∞；第一项可检验任务是计算其最小值 min_{N≤n≤2N}，而不只计算平均值。
- 来源核对：官方当前表述明确加入 ∑_{0<ai<n}，并说明原始来源可能隐含此限制：https://www.erdosproblems.com/460；官方页面也明确记录：若无截断，序列含所有 n+p（p>n 素数），故和为无穷。
- 时间记账：所在批次墙钟时间按题数均摊约 40.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/460)；既有候选答案（按不可信材料审计）

### #461

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $s_t(n)$ be the $t$-smooth component of $n$ - that is, the product of all primes $p$ (with multiplicity) dividing $n$ such that $p<t$. Let $f(n,t)$ count the number of distinct possible values for $s_t(m)$ for $m\in [n+1,n+t]$. Is it true that\[f(n,t)\gg t\](uniformly, for all $t$ and $n$)?
- 题意摘要：对整数 t≥2，将 m 分解为 s_t(m)r，其中 s_t(m)含有 m 的全部 p<t 的素因子幂，而 r 的素因子均 ≥t。f(n,t) 是长度 t 的整数区间 [n+1,n+t] 中 s_t(m) 的不同取值数。问题是是否存在绝对常数 c>0，使所有 n,t 都有 f(n,t)≥ct。
- 状态核对：仍为开放问题；已记录的统一下界是 f(n,t)≫t/log t。旧候选的“大于等于 t 的 smooth component 不碰撞”结论正确，但没有触及保证正比例此类整数的核心。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：研究同一 smooth component 的碰撞。若 m1=d r1、m2=d r2 且 s_t(m1)=s_t(m2)=d，则 d整除m1−m2。按 d 的大小分层，尝试由每个纤维的最大重数推出像集线性下界。
- 局部结论：若 d≥t，则同一长度 t 区间中该值至多出现一次，因为 0<|m1−m2|<t 不可能被 d 整除。；一般地，同一 d 的出现次数至多 1+⌊(t−1)/d⌋。；因此若能统一证明至少 δt 个区间元素满足 s_t(m)≥αt，则这些元素至少贡献约 αδt 个不同值。
- 第一阻塞点：无法严格证明任意长度 t 区间内有正比例的 m 满足 s_t(m)≥αt；小值 d（尤其 d=1）允许很大的碰撞纤维，而上述整除间距本身不能排除这种集中。这正是从 t/log t 提升到 t 所缺的均匀输入。
- 下一步：检验分层命题：是否存在固定 α,δ>0，使每个区间都有至少 δt 个 m 满足 s_t(m)≥αt；先对极端区间搜索反例，并分别统计 d<t/j 各层的占比。
- 来源核对：官方页面确认开放状态及已知 t/log t 下界：https://www.erdosproblems.com/461
- 时间记账：所在批次墙钟时间按题数均摊约 40.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/461)；既有候选答案（按不可信材料审计）

### #462

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p(n)$ denote the least prime factor of $n$. There is a constant $c>0$ such that\[\sum_{\substack{n<x\\ n\textrm{ not prime}}}\frac{p(n)}{n}\sim c\frac{x^{1/2}}{(\log x)^2}.\]Is it true that there exists a constant $C>0$ such that\[\sum_{x\leq n\leq x+Cx^{1/2}(\log x)^2}\frac{p(n)}{n} \gg 1\]for all large $x$?
- 题意摘要：令 p(n) 为 n 的最小素因子。字面问题问：是否存在固定 C>0 及固定 c0>0，使所有充分大的实数 x 都有 ∑_{x≤n≤x+C√x(log x)^2}p(n)/n≥c0；第二个和按所写量词包含素数 n。
- 状态核对：仍开放。首个渐近式排除素数，而目标和没有排除素数，存在解释不一致。旧候选从全局渐近式“形式求导”得到局部常数质量只是启发：全局渐近等价不能推出每个这种短区间的增量下界。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先按字面包含素数处理：区间若含素数，单项贡献即为1。为避免完全归约到短区间素数，另限制到平衡半素数 m=pq，并把目标化为短区间中的计数问题。
- 局部结论：区间内任一素数 n 满足 p(n)/n=1，立即给出所需常数下界。；若 x充分大、m=pq位于目标区间且 √x/2≤p≤q≤2√x，则 p(m)/m=1/q≥1/(2√x)。；所以若能在每个目标区间统一找到至少 δ√x 个这样的平衡半素数，则复合数部分的总贡献至少 δ/2。
- 第一阻塞点：第一处无法闭合的是对每个 x 给出 Ω(√x) 个平衡半素数；全局平均渐近式不控制如此短的每个区间。另一方面，“含一个素数”只是充分条件，并不与原命题等价。
- 下一步：建立明确的局部计数目标：对 h=C√x(log x)^2，计算并尝试下界 #{pq∈[x,x+h]:√x/2≤p≤q≤2√x}；同时分别记录包含素数和排除素数两种版本，避免量词混淆。
- 来源核对：官方页面确认开放，且目标和按排版确实未写“n not prime”：https://www.erdosproblems.com/462
- 时间记账：所在批次墙钟时间按题数均摊约 40.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/462)；既有候选答案（按不可信材料审计）

### #463

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a function $f$ with $f(n)\to \infty$ as $n\to \infty$ such that, for all large $n$, there is a composite number $m$ such that\[n+f(n)<m<n+p(m)?\](Here $p(m)$ is the least prime factor of $m$.)
- 题意摘要：问是否存在函数 f:ℕ→ℕ，满足 f(n)→∞，并且对所有充分大的 n，都存在复合数 m，使 n+f(n)<m<n+p(m)，其中 p(m) 是 m 的最小素因子。量词次序是 ∃f、最终对所有 n、再 ∃m。
- 状态核对：仍开放；本地 Lean 文件忠实表达了上述量词，但定理以 sorry 占位。旧候选给出的平方例只覆盖某些 n，不能处理“所有充分大 n”。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：定义 D(n)=max({d≥1:n+d为复合数且d<p(n+d)}∪{0})。先把原命题精确归约为 D(n)→∞，再将候选 m=pq 解释为覆盖整数轴的向左区间。
- 局部结论：复合 m 满足 p(m)≤√m；故 d=m−n 满足 d²<n+d，从而 d<(1+√(1+4n))/2，D(n)确实是有限最大值且 D(n)=O(√n)。；原命题等价于 D(n)→∞：正向有 D(n)>f(n)；反向可取 f(n)=⌊D(n)/2⌋。；每个复合 m 覆盖所有整数 n∈(m−p(m),m)；若 m=pq、p≤q，则覆盖区间长度约 p。问题等价于这些覆盖区间在每个大 n 处的覆盖深度 D(n)趋于无穷。
- 第一阻塞点：无法证明这些半素数/复合数覆盖区间之间的最大未充分覆盖间隙趋于零；平方 m=p² 只覆盖 (p²−p,p²)，相邻素数平方之间留下很长区域。该路线需要远强于现有均匀分布信息的“每点覆盖”结论。
- 下一步：对 N≤n≤2N 精确计算 min D(n)，并按 m=pq、一般复合数分别计算覆盖贡献；若最小值增长，定位实现最小值的空隙结构并尝试把它归约为短区间半素数计数。
- 来源核对：官方页面确认开放及与 F(n)=min_{m>n}(m−p(m)) 的关系：https://www.erdosproblems.com/463；本地 463.lean 的量词与题面一致，但证明为 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 40.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/463)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/463.lean`；既有候选答案（按不可信材料审计）

### #467

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Prove the following for all large $x$: there is a choice of congruence classes $a_p$ for all primes $p\leq x$ and a decomposition $\{p\leq x\}=A\sqcup B$ into two non-empty sets such that, for all $n<x$, there exist some $p\in A$ and $q\in B$ such that $n\equiv a_p\pmod{p}$ and $n\equiv a_q\pmod{q}$.
- 题意摘要：按官方推定含义，量词应读作：存在 X，使每个实数参数 x≥X 都可为全部素数 p≤x 选一个剩余类 a_p，并把这些素数分成非空 A、B，使每个整数 0≤n<x 同时被某个 A 中的类和某个 B 中的类覆盖。原文仅写 n<x；若允许所有负整数，含义会完全不同，因此必须采用有限区间解释。
- 状态核对：仍列为 open；官方也明确说原始出处缺少关键量词。先前候选把区间取成 0≤n<x，属于合理解释，但不是原文严格给出的量词。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：用 CRT 将所有 a_p 合并为一个 m modulo P=∏_{p≤x}p：n≡a_p (mod p) 当且仅当 p|(m−n)。随后随机二染素数并随机选择 a_p。对固定 n，没有 A-覆盖的概率为 ∏_{p≤x}(1−1/(2p))≪(log x)^(−1/2)，B 同理。线性期望给出一个选择，仅有 O(x/√log x) 个失败点；再尝试保留大素数逐点修补。
- 局部结论：CRT 等价严格成立：问题等价于寻找连续的约 x 个整数 m−n，使每个数都同时有一个来自 A 和一个来自 B 的、至多 x 的素因子；m−n=0 时整除条件也成立。；随机方法严格给出“两色条件对除 O(x/√log x) 外的所有 n 成立”。当 x 足够大时该上界小于区间长度，因此实现该上界的 A、B 自动都非空。；若预留 p>x/2，则一个剩余类在长度 x 区间内至多命中两个点；若预留 p接近x，则基本只能作常数次修补。可用预留素数总数仅约 x/log x，少于当前 O(x/√log x) 异常规模。
- 第一阻塞点：第一处缺口是把随机筛后的异常集压到可由未使用素数双重覆盖的规模和结构。现有一阶期望只给 x/√log x 个异常，而逐点双修补大约需要与异常数同阶的两色资源；同时修改旧剩余类又可能破坏已经获得的覆盖。
- 下一步：做一个两阶段可检验实验：只用 p≤x/2 随机筛，记录异常集 E；随后把 x/2<p≤x 建成二部匹配，左右各放一份 E，素数 p 与其剩余类能命中的异常点相连。测试最大匹配缺陷是否为 o(|E|)，并据此寻找可证明的 Hall 条件。
- 来源核对：[Erdős Problems #467](https://www.erdosproblems.com/467) 当前仍标为 OPEN，并明确提示原始题目的量词有歧义。；先前候选的 CRT 归约和随机乘积计算已独立复核，均成立；但它没有给出从 almost-all 到 all 的闭合步骤。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/467)；既有候选答案（按不可信材料审计）

### #468

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $n$ let $D_n$ be the set of sums of the shape $d_1,d_1+d_2,d_1+d_2+d_3,\ldots$ where $1<d_1<d_2<\cdots$ are the divisors of $n$. What is the size of $D_n\backslash \cup_{m<n}D_m$? If $f(N)$ is the minimal $n$ such that $N\in D_n$ then is it true that $f(N)=o(N)$? Perhaps just for almost all $N$?
- 题意摘要：令 1<d₁<⋯<d_r 为 n 的全部大于 1 的正因子，D_n={d₁,d₁+d₂,…,d₁+⋯+d_r}。第一问研究 a(n)=|D_n∖⋃_{m<n}D_m|。第二问对确实属于某个 D_n 的 N 定义 f(N)=min{n:N∈D_n}，问 f(N)/N→0，或至少是否对密度 1 的 N 成立。f 对所有 N 是否有定义本身也不是原陈述自动保证的。
- 状态核对：整题仍因 a(n) 的结构/渐近问题而列为 open；但冻结日期之后，第二问的“全体”及“几乎所有”版本已有否定结果。因此先前候选的结论方向正确，但引用的是论坛证明而非已正式审稿论文。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先把 debut 数解释为 f 的纤维，再重建 Tao 路线。若 σ_k(m) 表示删去 k 个最大因子后的因子和，则每个前缀和都等于某个 σ_k(m)。关键平均估计为 ∑_{m≤x}σ_k(m)≪x²/k^{1.1}。对 k 求和并用 Markov 不等式，可控制小 m 所能命中的大 N 数量。
- 局部结论：严格恒等式：a(n)=#{N:f(N)=n}；这是定义的直接结果，不依赖 f 是否处处有定义。另有 |D_n|=τ(n)−1，因为正因子前缀和严格递增。；取 N=σ(n)−1，即 D_n 的最后一个前缀和，则 f(N)≤n。利用 limsup σ(n)/n=∞，得到 liminf f(N)/N=0。；由上述 σ_k 平均估计可推出 #{N∈[1,X]:f(N)≤δN}/X≪δ²；故 f(N)=o(N) 不仅不是逐点成立，也不可能在密度 1 的集合上成立。后续论坛工作声称更强衰减，但本筛查只采用已清楚展示的 δ² 路线。
- 第一阻塞点：第二问的否定路线可闭合；尚未闭合的是第一问：这些平均估计控制所有命中值的总体数量，却没有给出单个纤维 #{N:f(N)=n} 的上界、无界性或平均渐近。
- 下一步：验证并实现精确恒等式 a(n)=#{k:σ_k(n) 未曾作为 σ_j(m),m<n 出现}，计算到更高范围，同时按 τ(n)、σ(n)/n 分层；首个理论目标是证明平均界 ∑_{n≤x}a(n)=O(x) 或构造 a(n)→∞ 的显式子序列。
- 来源核对：[Erdős Problems #468](https://www.erdosproblems.com/468) 仍标为 OPEN，且注明评论中有部分结果。；[问题 #1054 的状态说明](https://www.erdosproblems.com/1054) 记录 Tao 的上密度 ≪δ² 结论。；[完整讨论串](https://www.erdosproblems.com/forum/thread/1054) 展示了 σ_k 平均估计、Markov/并集界及其导出步骤；它也明确区分了后续尚未正式审稿的增强结果。；先前候选声称 f 只差一个平移；这对“包含因子 1”的版本成立，但须同时平移目标值，并注意原函数可能未定义，不能无条件当作处处定义的数列。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/468)；既有候选答案（按不可信材料审计）

### #469

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be the set of all $n$ such that $n=d_1+\cdots+d_k$ with $d_i$ distinct proper divisors of $n$, but this is not true for any $m\mid n$ with $m<n$. Does\[\sum_{n\in A}\frac{1}{n}\]converge?
- 题意摘要：A 包含所有正整数 n，使 n 能写成若干互异真因子之和，且每个真因子 m|n 都不能写成其自身互异真因子之和。问题是正项级数 ∑_{n∈A}1/n 是否收敛。这里的原始性量词只遍历 m|n，而不是所有 m<n。
- 状态核对：仍为 open。A 即 primitive pseudoperfect numbers。先前候选的总体状态判断正确，但其关于 Pollack 书中 S₁/S₂ 分解的叙述未在本次筛查中从原文重建，故不作为已核实结论。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：按最大素因子分层。写 n=pm，其中 p=P(n)。从一组互异真因子表示 n 出发，模 p 考察其中不被 p 整除的项；再尝试对给定 m 计数可能的 p。另检查显式族 n=2^k p，以判断 A 的稀疏程度。
- 局部结论：模 p 子集不能为空：若所有被选因子均被 p 整除，除以 p 就会把 m 写成互异真因子之和，与原始性矛盾。因此不被 p 整除的选中因子之和是正的 p 倍，且至多 σ(m)，从而 p≤σ(m)。这补上了先前候选模 p 论证遗漏的“非空”理由。；若 2^k<p<2^(k+1) 为素数，则 n=2^kp∈A：用 p,2p,…,2^(k−1)p，再用互异的 1,2,…,2^k 的二进制子集补足 p。每个真因子 2^jp（j<k）满足 σ(2^jp)<2·2^jp，故不可能 pseudoperfect。；上述整个显式子族的倒数和收敛：对固定 k，区间内所有素数的贡献至多 2^k/(2^k·2^k)=2^(−k)。所以 A 无穷并不自动造成原级数发散。
- 第一阻塞点：约束 p≤σ(m) 太弱：忽略原始性后，对 m 求和的粗略上界仍类似 ∑(log log σ(m))/m，不能收敛。需要证明对绝大多数 m，可行的最大素因子 p 远少于 p≤σ(m) 的全部素数，或利用 m 本身不 pseudoperfect 的强限制。
- 下一步：固定 m≤10^6，枚举满足 P(m)≤p≤σ(m) 且 pm∈A 的素数 p，统计每个 m 的数量和 ∑_p1/p；检验可否建立统一界 ∑_{p:pm∈A}1/p≪1/(log m)^{1+ε}。这是最大素因子分层能否导出收敛的直接判据。
- 来源核对：[Erdős Problems #469](https://www.erdosproblems.com/469) 仍标为 OPEN，并确认 A006036 的对应关系。；[OEIS A006036](https://oeis.org/A006036) 的定义是“不为任何其他 pseudoperfect number 的倍数”，与题中对真因子 m 的量词等价。；本地形式化文件把原始性写为 ∀m<n, m∣n→¬IsSumDivisors(m)，与上述重述一致；但定理主体仍含 sorry，不能视为形式化证明。；先前候选给出的 2^kp 家族已独立验算，结论成立；其模 p 论证则必须加入排除空子集的原始性论证。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/469)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/469.lean`；既有候选答案（按不可信材料审计）

### #470

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Call $n$ weird if $\sigma(n)\geq 2n$ and $n$ is not pseudoperfect, that is, it is not the sum of any set of its divisors. Are there any odd weird numbers? Are there infinitely many primitive weird numbers, i.e. those such that no proper divisor of $n$ is weird?
- 题意摘要：采用标准定义：n weird 当且仅当 σ(n)≥2n，且 n 不能写成互异真因子之和。问：(i) 是否存在奇 weird 数；(ii) 是否有无穷多个 primitive weird 数，即 weird 且所有真因子均非 weird。题面若把“divisors”字面理解为包含 n 本身，则单元素集合 {n} 会使定义空洞，必须解释为 proper divisors。
- 状态核对：两问目前均为 open；奇 weird 数在 10^21 以下不存在。无穷多个 primitive weird 数仅在特定强素数间隙假设下已知。先前候选的状态判断与官方背景一致。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：使用丰盈余量 Δ=σ(n)−2n。全部真因子之和为 n+Δ，因此 n 可由真因子子集表示，当且仅当 Δ 可由其补集表示。对 n=2^kpq 构造 Δ 落在二进制因子总和与最小奇素因子之间的窗口，得到 weird；再用真因子亏数条件保证 primitive。
- 局部结论：补集引理严格成立：对 abundant n，n pseudoperfect ⇔ Δ 是互异真因子之和。因此 Δ=0 或 1 时因 {1} 等立即可表示，不会产生 weird。；设 p<q 为奇素数，n=2^kpq，且 2^(k+1)−1<Δ<p。小于 p 的真因子恰为 1,2,…,2^k，总和小于 Δ；含 p 的子集又超过 Δ，故 Δ 不可表示，n 为 weird。；若再有 σ(2^(k−1)pq)<2·2^(k−1)pq，则 n/2 亏；而 p,q>2^(k+1)−1 使 2^kp、2^kq 亏。由 abundancy index 对整除的单调性，所有真因子均亏，故 n 是 primitive weird。
- 第一阻塞点：要得到无穷族，必须对无穷多个 k 找素数 p<q，使显式的 Δ=(2^(k+1)−1)(p+1)(q+1)−2^(k+1)pq 落入上述狭窄窗口，同时低一层仍亏。这转化成短区间素数问题；现有无条件素数间隙界不足以保证所需的无限多配对。奇数情形则连一个候选也没有，补集引理尚未产生足够强的矛盾。
- 下一步：把两条不等式代数化为 q 关于 p、k 的明确开区间，计算其长度并与现有无条件 prime-gap 指数比较；若长度仅为 O(√p)，即可精确定位为何 Melfi 的 p_{r+1}−p_r<0.1√p_r 假设能闭合而现有定理不能。
- 来源核对：[Erdős Problems #470](https://www.erdosproblems.com/470) 记录两问开放、Melfi 的条件性无穷结果以及至少六个不同素因子的限制。；[Fang 论文摘要](https://arxiv.org/abs/2207.12906) 明确给出 10^21 以下无奇 weird 数，以及附加丰盈限制下搜索至 10^28。；本地 Lean 文件使用 Nat.Weird 和 properDivisors，确认标准定义必须排除 n 本身；其中各结论仍为 sorry 占位，不能算机器核验。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/470)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/470.lean`；既有候选答案（按不可信材料审计）

### #472

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given some initial finite sequence of primes $q_1<\cdots<q_m$ extend it so that $q_{n+1}$ is the smallest prime of the form $q_n+q_i-1$ for $n\geq m$. Is there an initial starting sequence so that the resulting sequence is infinite?
- 题意摘要：存在量词是：是否存在某个有限严格递增素数列 q₁<⋯<q_m，使递推对每个 n≥m 都有定义。递推时在全部 1≤i≤n 中考察 q_n+q_i−1，取其中最小的素数作为 q_{n+1}；若所有候选均合数，过程停止。
- 状态核对：仍为 open。官方仅把起点 3,5 作为可能无限的候选。先前候选声称自行算到十万项及具体末项，但未提供可复核程序或证书，本筛查不采信该数值。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：研究起点 3,5 的最小增量结构，并把“继续一步”改写为有限素性析取。由于所有后续素数为奇数，候选增量 q_i−1 均为偶数；首先考察 q_n+2 与 q_n+4，再考虑历史增量集合。
- 局部结论：递推严格递增，因为每个 q_i≥2，所以 q_n+q_i−1>q_n。停止的充要条件是对所有 i≤n，q_n+q_i−1 均为合数；这给出每一有限阶段可完全验证的停止/继续证书。；对起点 3,5，若 q_n+2 或 q_n+4 是素数，则下一项必为二者中较小的素数，因为其余历史增量至少为 6。；当 q_n>3 时，q_n+2 与 q_n+4 中恰有一个被 3 整除；因此这两个最小候选至多有一个可用。递推的长期存活必须反复依靠唯一未被 3 排除者或更大的历史增量。
- 第一阻塞点：第一处无法闭合的是证明每个动态产生的 q_n 至少有一个历史增量 q_i−1 使 q_n+q_i−1 为素数。现有素数分布定理不对这种随历史自适应、且要求每一步成功的有限平移集合给出保证。计算任意长前缀也不能排除以后停止。
- 下一步：生成带证书的前缀：每一步记录获选 i、q_{n+1} 的素性证书，并为所有更小候选记录合数因子；同时统计停止条件中候选的最小素因子覆盖。目标是寻找一个有限的增量子集 H，使序列状态总落在可证明“某个 q+h 为素数”的同余类结构中，或反向找到覆盖系统迫使某类起点终止。
- 来源核对：[Erdős Problems #472](https://www.erdosproblems.com/472) 仍标为 OPEN，并只陈述 3,5 序列“可能”无限。；先前候选关于 5 立即停止、11,13 在 23 停止的例子可直接验算；其十万项计算因无代码、哈希或证书而未被视为已核实事实。；题面没有明写 i≤n；这是递推可定义性的自然且必要解释，应在任何形式化版本中显式加入。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/472)；既有候选答案（按不可信材料审计）

### #477

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a polynomial $f:\mathbb{Z}\to \mathbb{Z}$ of degree at least $2$ and a set $A\subset \mathbb{Z}$ such that for any $n\in \mathbb{Z}$ there is exactly one $a\in A$ and $b\in \{ f(n) : n\in\mathbb{Z}\}$ such that $n=a+b$?
- 题意摘要：问是否存在次数至少 2 的整值多项式 $f:\mathbb Z\to\mathbb Z$ 与集合 $A\subseteq\mathbb Z$，使每个 $m\in\mathbb Z$ 都恰有一组 $(a,b)\in A\times f(\mathbb Z)$ 满足 $m=a+b$；即要求直和分解 $\mathbb Z=A\oplus f(\mathbb Z)$。
- 状态核对：截至 2026-04-11 官方页面仍标为 open，但已收录“二次多项式不可能”的部分结果。旧候选的二次论证基本正确，不过须区分整系数多项式与一般整值多项式；以下用二项式基底覆盖后者。[官方页面](https://www.erdosproblems.com/477)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：研究差集障碍。唯一表示蕴含 $(A-A)\cap(B-B)=\{0\}$，其中 $B=f(\mathbb Z)$。若某个 $q\neq0$ 满足 $q\mathbb Z\subseteq B-B$，无限集 $A$ 中必有两个元素同余模 $|q|$，立即产生两种表示。
- 局部结论：$A$ 必为无限集：若 $|A|=r<\infty$，则覆盖 $[-X,X]$ 需要 $\gg X$ 个不同的 $f$ 值落在某个长度 $O(X)$ 的区间内；但次数 $d\ge2$ 时这样的值只有 $O(X^{1/d})$ 个。；若 $f(n)=p\binom n2+qn+r$ 为任意整值二次多项式，则 $f(k)-f(-k)=(2q-p)k$。当 $2q-p\neq0$ 时，$B-B$ 包含 $(2q-p)\mathbb Z$，故不可能平铺。；若 $2q-p=0$，则 $f(n)=mn^2+r$ 且 $f(k+1)-f(k-1)=4mk$；同样得到 $4m\mathbb Z\subseteq B-B$。因此所有二次情形均被严格排除。该方法也排除任何已能证明 $f(\mathbb Z)-f(\mathbb Z)$ 包含非零子群的高次多项式。
- 第一阻塞点：对一般三次及以上多项式，诸如 $f(k)-f(-k)$ 只是高次多项式值集，通常并不包含 $q\mathbb Z$；当前路线无法从“差集很大”提升为“包含一个完整非零子群”。
- 下一步：对三次整值多项式按平移和仿射归一化分类，逐类检验二元差值方程 $f(x)-f(y)=qt$ 是否对所有 $t\in\mathbb Z$ 可解；先确定除退化对称型外，差集子群判据究竟覆盖哪些三次族。
- 来源核对：核对了截至 2026-04-11 更新的 [Erdős Problems #477](https://www.erdosproblems.com/477)：总问题仍开放，二次障碍与上述差集证明一致。；独立重算了整值二次多项式的两个差分恒等式，未直接采信旧候选。
- 时间记账：所在批次墙钟时间按题数均摊约 40.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/477)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/477.lean`；既有候选答案（按不可信材料审计）

### #478

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p$ be a prime and\[A_p = \{ k! \pmod{p} : 1\leq k<p\}.\]Is it true that\[\lvert A_p\rvert \sim (1-\tfrac{1}{e})p?\]
- 题意摘要：对每个素数 $p$，令 $A_p$ 为序列 $1!,2!,\ldots,(p-1)!$ 在 $\mathbb F_p^*$ 中所取的不同值集合。问题是当素数 $p\to\infty$ 时，是否有 $|A_p|/p\to1-e^{-1}$。
- 状态核对：截至 2026-04-12 仍开放。已知最佳点态下界为 $|A_p|\ge(\sqrt2-o(1))p^{1/2}$，远未达到正比例。[官方页面](https://www.erdosproblems.com/478)；[GSSV 论文](https://ems.press/journals/rmi/articles/10143992)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试把问题化为碰撞矩控制。令 $r_x=|\{k:1\le k<p,\ k!\equiv x\pmod p\}|$，则 $|A_p|=|\{x:r_x>0\}|$。Poisson(1) 启发式要求控制 $\sum_x(r_x)_j$；先严格计算短距离碰撞。
- 局部结论：$A_p/A_p=\mathbb F_p^*$：对 $2\le t<p$，有 $t=t!/(t-1)!$，而 $1$ 显然属于比集。因此 $p-1\le|A_p|^2$，得到初等下界 $|A_p|\ge\sqrt{p-1}$。；若 $j=i+d$，碰撞 $i!\equiv j!\pmod p$ 等价于 $\prod_{s=1}^{d}(i+s)\equiv1\pmod p$。对固定 $d<p$，左端减 1 是次数 $d$ 的非零多项式，故至多有 $d$ 个起点 $i$。；所以对任意固定 $D$，间距不超过 $D$ 的碰撞对总数至多为 $\sum_{d\le D}d=D(D+1)/2$；尤其相邻项从不相等。
- 第一阻塞点：绝大多数可能碰撞具有随 $p$ 增长的长间距；次数界对这些间距求和只给出 $O(p^2)$，没有非平凡矩估计。即使只得到二阶碰撞数，也不足以确定未命中 residue 的比例为 $e^{-1}$。旧候选把“平均漏值数无界”表述成排除 $|A_p|$ 接近 $p$，这是过强解读：无界的次线性漏值仍与 $|A_p|/p\to1$ 相容。
- 下一步：计算并界定固定 $d_1,d_2$ 的联立碰撞方程 $i!=(i+d_1)!=(i+d_2)!$ 的解数，检验能否对所有 $d_1,d_2\le p^\theta$ 得到一致的低阶阶乘矩估计；这是 Poisson 路线的首个可证伪测试。
- 来源核对：[Erdős Problems #478](https://www.erdosproblems.com/478) 确认开放状态、$\sqrt2$ 下界及 Wilson 上界。；[Grebennikov–Sagdeev–Semchankau–Vasilevskii](https://ems.press/journals/rmi/articles/10143992) 核对了 2024 年论文及其 factorial value-set 结果。；未采用旧候选中未经来源核验的数值表。
- 时间记账：所在批次墙钟时间按题数均摊约 40.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/478)；既有候选答案（按不可信材料审计）

### #479

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for all $k\neq 1$, there are infinitely many $n$ such that $2^n\equiv k\pmod{n}$?
- 题意摘要：量词为：对每个固定整数 $k\neq1$，是否存在无穷多个正整数 $n$ 使 $n\mid 2^n-k$。$n$ 可依赖于 $k$；结论要求每个允许的 $k$ 各自有无限族，而非仅有一个解。
- 状态核对：截至 2025-12-03 官方页面仍列为 open；已知 $k=2^i$（$i\ge1$）及 $k=-1$ 有特殊构造。[官方页面](https://www.erdosproblems.com/479)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试从已有解乘入一个新素因子。设 $n$ 为奇数且 $n\mid2^n-k$。寻找素数 $q\nmid2n$，使 $q\mid2^n-k$ 且 $\operatorname{ord}_n(2)\mid n(q-1)$。
- 局部结论：在上述条件下 $N=nq$ 仍是解：模 $q$，由 Fermat 得 $2^{nq}\equiv2^n\equiv k$；模 $n$，指数差 $n(q-1)$ 被 $\operatorname{ord}_n(2)$ 整除，故 $2^{nq}\equiv2^n\equiv k$；再由中国剩余定理合并。；$k=0$ 有显式无限族 $n=2^r$；$k=2$ 有无限族为所有奇素数 $n=p$，因为 $2^p\equiv2\pmod p$。；对 $k=1$，旧候选的最小素因子证明需补偶数分支：偶数 $n$ 显然不可能；若 $n$ 为奇数且 $p$ 是其最小素因子，则 $\operatorname{ord}_p(2)\mid n$ 且小于 $p$。任何大于 1 的 $n$ 的因子至少为 $p$，故该阶只能为 1，矛盾。
- 第一阻塞点：提升引理要求新素数 $q$ 同时整除固定数 $2^n-k$ 并满足一个同余条件；现有论证既不能保证存在这样的新素因子，也不能保证反复迭代。对 $k=3$ 等一般值，这正是第一处断裂。
- 下一步：对若干已知种子解建立有限“提升图”：分解 $2^n-k$ 的可计算部分，筛出满足 $\operatorname{ord}_n(2)\mid n(q-1)$ 的新素因子，检查该机制是否能连续提升两步；若总在第一步失败，应转向允许改变多个素因子的 CRT 构造。
- 来源核对：[Erdős Problems #479](https://www.erdosproblems.com/479) 确认一般问题开放，并记录 $k=2^i,-1$ 的已知特例。；独立检查了 $k=1$ 论证，补上了旧候选遗漏的偶数情形。
- 时间记账：所在批次墙钟时间按题数均摊约 40.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/479)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/479.lean`；既有候选答案（按不可信材料审计）

### #483

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(k)$ be the minimal $N$ such that if $\{1,\ldots,N\}$ is $k$-coloured then there is a monochromatic solution to $a+b=c$. Estimate $f(k)$. In particular, is it true that $f(k) < c^k$ for some constant $c>0$?
- 题意摘要：$f(k)$ 是最小的 $N$，使任意映射 $\chi:\{1,\ldots,N\}\to\{1, \ldots,k\}$ 都存在同色的 $a,b,c$（允许 $a=b$）满足 $a+b=c$。等价地，$f(k)-1$ 是可分成 $k$ 个 sum-free 集的最大初始区间长度。问题特别询问是否存在与 $k$ 无关的常数 $c$ 使所有 $k$ 均有 $f(k)<c^k$。
- 状态核对：这是 Schur 数问题，仍开放。截至 2026-04-10，官方所列最佳渐近界为 $(380)^{k/5}-O(1)\le f(k)\le(e-1/6)k!$。输入快照中的 $(e-1/24)k!$ 已过时；旧候选正文采用的 $(e-1/6)k!$ 与当前页面一致。[官方页面](https://www.erdosproblems.com/483)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：重建两个基础构造：一是 sum-free 着色的三倍递推，二是把整数着色转化为完全图边着色，从而归约到多色三角 Ramsey 数。
- 局部结论：若 $[1,m]$ 有 $k$ 色无 Schur 三元组着色，则 $[1,3m+1]$ 有 $k+1$ 色着色：中段 $[m+1,2m+1]$ 用新色；两端用原着色，并令上段 $x$ 继承 $3m+2-x$ 的颜色。逐类检查可知同色等式会还原为原区间中的 Schur 三元组。因此 $f(k+1)\ge3f(k)-1$，迭代得 $f(k)\ge(3^k+1)/2$。；若 $[1,N]$ 被 $k$ 着色，就把完全图顶点 $0,1,\ldots,N$ 的边 $\{x,y\}$ 染成 $|x-y|$ 的颜色。单色三角形 $x<y<z$ 给出同色的 $(y-x)+(z-y)=z-x$。故 $f(k)\le R_k(3)-1$。；上述两条严格重建出指数下界和 Ramsey 上界，但现代模板已把下界底数提高到 $380^{1/5}\approx3.2806$。
- 第一阻塞点：Ramsey 归约结合已知递推只产生阶乘上界；要得到 $c^k$，需要全新的 Schur 着色结构约束，或证明 $R_k(3)$ 的一致指数上界。当前构造没有利用“边色由差值决定”这一额外结构，因此在此处停止。
- 下一步：定义差值型三角 Ramsey 数 $D_k$（仅考虑颜色由 $|x-y|$ 决定的边着色），针对小 $k$ 枚举极值着色并寻找直接递推 $D_{k+1}\le C D_k$；首要检验是现有 Ramsey 阶乘递推中哪些分支因差值一致性而不可能。
- 来源核对：[Erdős Problems #483](https://www.erdosproblems.com/483) 核对了 2026 年更新的最佳上下界、精确小值和开放状态。；独立验证了三倍下界构造与 $f(k)\le R_k(3)-1$ 的差值着色归约。
- 时间记账：所在批次墙钟时间按题数均摊约 40.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/483)；既有候选答案（按不可信材料审计）

### #486

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$, and for each $n\in A$ choose some $X_n\subseteq \mathbb{Z}/n\mathbb{Z}$. Let\[B = \{ m\in \mathbb{N} : m\not\in X_n\pmod{n}\textrm{ for all }n\in A\textrm{ with }m>n\}.\]Must $B$ have a logarithmic density, i.e. is it true that\[\lim_{x\to \infty} \frac{1}{\log x}\sum_{\substack{m\in B\\ m<x}}\frac{1}{m}\]exists?
- 题意摘要：任取 $A\subseteq\mathbb N$，并对每个 $n\in A$ 任取禁集 $X_n\subseteq\mathbb Z/n\mathbb Z$。整数 $m$ 属于 $B$ 当且仅当对每个满足 $n<m$ 的 $n\in A$，都有 $m\bmod n\notin X_n$。问题问对所有这些选择，调和计数 $\frac1{\log x}\sum_{m<x,m\in B}1/m$ 是否必有极限。
- 状态核对：截至 2026-04-08 仍开放。$X_n=\{0\}$ 时由 Davenport–Erdős 定理肯定；即使每个 $|X_n|=1$，一般问题也尚未解决。[官方页面](https://www.erdosproblems.com/486)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：用有限约束周期集逼近。对 $y\ge1$ 定义 $C_y$：只施加来自 $n\in A, n\le y$ 的约束，并仍保留激活条件 $n<m$。则 $C_{y+1}\subseteq C_y$，且每个 $C_y$ 在有限初段以后以 $L_y=\operatorname{lcm}(A\cap[1,y])$ 为周期。
- 局部结论：每个 $C_y$ 有自然密度及同值的对数密度 $\delta_y$；由于集合递减，$\delta_y$ 单调下降，故 $\delta=\lim_y\delta_y$ 存在。；$B=\bigcap_y C_y$。更强地，对每个观测尺度 $x$，有 $B\cap[1,x)=C_x\cap[1,x)$，因为模数 $n\ge x$ 尚未对任何 $m<x$ 激活。；由 $B\subseteq C_y$ 可严格得到 $\overline\delta_{\log}(B)\le\delta_y$，进而 $\overline\delta_{\log}(B)\le\delta$。因此只缺相反方向的下对数密度估计。
- 第一阻塞点：虽有 $B\cap[1,x)=C_x\cap[1,x)$，但 $C_x$ 的周期 $L_x$ 可能远大于 $x$，所以在区间 $[1,x)$ 内的调和平均不必接近其周期密度 $\delta_x$。缺少对这种“变化周期的三角阵列”的一致遍历估计；任意大的 $X_n$ 也使简单尾和界完全失效。
- 下一步：先处理可检验的受限情形：假设 $\log L_y=o(y)$ 或给定 $L_y\le y^C$，证明 $C_y$ 在对数尺度上的周期平均误差一致趋零；随后构造增长最快的模数序列，检验该条件是否接近必要。
- 来源核对：[Erdős Problems #486](https://www.erdosproblems.com/486) 确认一般问题及 $|X_n|=1$ 特例仍开放。；[Davenport–Erdős 1936 原论文入口](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/2/1/93274/on-sequences-of-positive-integers) 核对了集合之倍数具有对数密度的经典特例。；未采用旧候选关于“去掉激活阈值即可破坏收敛”的未核实附带断言。
- 时间记账：所在批次墙钟时间按题数均摊约 40.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/486)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/486.lean`；既有候选答案（按不可信材料审计）

### #488

- 当前状态：`falsifiable`（冻结清单状态：`open`）
- 精确题面：Let $A$ be a finite set and\[B=\{ n \geq 1 : a\mid n\textrm{ for some }a\in A\}.\]Is it true that, for every $m>n\geq \max(A)$,\[\frac{\lvert B\cap [1,m]\rvert }{m}< 2\frac{\lvert B\cap [1,n]\rvert}{n}?\]
- 题意摘要：设非空有限集 $A\subset\mathbb N_{\ge1}$，令 $F_A(x)=|\{t\le x:\exists a\in A,a\mid t\}|$。问题要求对所有整数 $m>n\ge\max A$ 严格证明 $F_A(m)/m<2F_A(n)/n$。
- 状态核对：“falsifiable”只是指可由有限反例否定，并不表示已有反例；截至核查时，正确的“倍数”版本仍列为开放。旧候选把计算证据写成肯定答案，不能接受。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先删去被其他元素整除的冗余元素，使 $A$ 为 primitive；再检验单元素、双元素情形，观察一般路线在哪一步因不同倍数集的交叠而失效。
- 局部结论：若 $A=\{a\}$，则 $F_A(x)=\lfloor x/a\rfloor$，可直接验证所求不等式；取 $n=2a-1,m=2a$ 时密度比为 $2-1/a$，故常数 $2$ 确实最优。；若约化后 $A=\{a,b\}$ 且 $a<b$、$a\nmid b$，则对 $n\ge b$ 有 $F_A(n)\ge\lfloor n/a\rfloor+1\ge(n+1)/a$，而 $F_A(m)\le m/a+m/b<2m/a$，从而严格得到结论。；若 $a\mid b$，则 $B$ 只是 $a$ 的倍数；由 $n\ge b\ge2a$ 仍可直接证明。故命题对 $|A|\le2$ 成立。
- 第一阻塞点：对至少三个 primitive 元素，粗并集上界 $F_A(m)\le m\sum_{a\in A}1/a$ 无法由 $F_A(n)$ 控制：容斥中的 $\operatorname{lcm}$ 交叠可能在两个截点产生不同的取整误差。这里没有可严格成立的“最坏情形必为单元素”归约。
- 下一步：首个可检验任务是完整处理 primitive 三元组：按所有 $\gcd(a_i,a_j)$ 与 $\operatorname{lcm}(a_i,a_j)$ 写出容斥公式，并验证是否恒有 $2mF_A(n)-nF_A(m)>0$；若失败，穷举该表达式的取整余类以寻找真实反例。
- 来源核对：[官方页面](https://www.erdosproblems.com/488)明确把倍数版本标为 FALSIFIABLE/Open，并给出常数最优例。；官方讨论中的反例针对旧的“不被整除”误植，或违反 $n\ge\max A$，不能移用于本题。
- 时间记账：所在批次墙钟时间按题数均摊约 52.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/488)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/488.lean`；既有候选答案（按不可信材料审计）

### #489

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be a set such that $\lvert A\cap [1,x]\rvert=o(x^{1/2})$. Let\[B=\{ n\geq 1 : a\nmid n\textrm{ for all }a\in A\}.\]If $B=\{b_1<b_2<\cdots\}$ then is it true that\[\lim \frac{1}{x}\sum_{b_i<x}(b_{i+1}-b_i)^2\]exists (and is finite)?
- 题意摘要：给定 $A\subseteq\mathbb N$，满足计数函数 $A(x)=|A\cap[1,x]|=o(x^{1/2})$；令 $B$ 为不被任何 $a\in A$ 整除的正整数并递增枚举为 $(b_i)$。问当 $x\to\infty$ 时，$x^{-1}\sum_{b_i<x}(b_{i+1}-b_i)^2$ 是否总有有限极限。题面隐含 $B$ 可无限枚举；若采用 $1\in\mathbb N$，还须排除 $1\in A$。
- 状态核对：一般情形仍开放；平方自由数是已知特例。旧候选关于有限 $A$ 的周期性结论正确，但没有触及从有限截断到无限 $A$ 的关键一致可积性问题。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 $A_R=A\cap[1,R]$，考察有限筛所得周期集合 $B_R$，再尝试用尾部 $A\setminus A_R$ 的稀疏性把平方间隙平均从 $B_R$ 传递到 $B$。
- 局部结论：分部求和给出 $\sum_{a\in A}1/a<\infty$：对充分大 $t$，$A(t)\le\varepsilon\sqrt t$，故 $\sum_{a>R}1/a\le A(R)/R+\int_R^\infty A(t)t^{-2}dt=O(\varepsilon/\sqrt R)$。；对每个有限 $A_R$（且 $1\notin A_R$），$B_R$ 以 $L_R=\operatorname{lcm}(A_R)$ 为周期，因此其间隙序列周期，平方间隙平均存在且有限。；由并集界，$B_R\setminus B$ 的上密度至多 $\sum_{a\in A,\,a>R}1/a\to0$。
- 第一阻塞点：平方间隙泛函对零密度删点并不连续：极少数删点仍可能合并成长间隙，并对平方和产生不可忽略贡献。当前假设给出了删点密度控制，却尚未给出 $\sum g^2$ 的统一尾界。
- 下一步：证明或否定如下统一估计：对充分大 $H$，所有截断 $R$ 均满足 $x^{-1}\sum_{b_i^{(R)}<x,\,b_{i+1}^{(R)}-b_i^{(R)}>H}(b_{i+1}^{(R)}-b_i^{(R)})^2=o_H(1)$。这正是可把周期极限传到 $B$ 的一致可积性条件。
- 来源核对：[官方页面](https://www.erdosproblems.com/489)仍标为开放，并明确记录平方自由数特例。；题面若允许 $A=\{1\}$，则 $B=\varnothing$、枚举不存在；正式使用时应补充 $1\notin A$ 或直接假设 $B$ 无限。
- 时间记账：所在批次墙钟时间按题数均摊约 52.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/489)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/489.lean`；既有候选答案（按不可信材料审计）

### #495

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha,\beta \in \mathbb{R}$. Is it true that\[\liminf_{n\to \infty} n \| n\alpha \| \| n\beta\| =0\]where $\|x\|$ is the distance from $x$ to the nearest integer?
- 题意摘要：对每一对实数 $\alpha,\beta$，是否存在趋于无穷的整数子列 $n_j$，使 $n_j\|n_j\alpha\|\|n_j\beta\|\to0$？这正是 Littlewood 猜想。
- 状态核对：仍为开放问题。旧候选列出的“非 badly approximable”与有理相关情形可以严格重建，但不能外推到任意 badly approximable 对。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先用连分数处理单坐标可异常逼近及 $1,\alpha,\beta$ 有理相关的情形；随后尝试二维 Dirichlet 同时逼近。
- 局部结论：若 $\liminf_q q\|q\alpha\|=0$，则沿相应子列 $q\|q\alpha\|\|q\beta\|\le\frac12q\|q\alpha\|\to0$；对 $\beta$ 同理。故反例必须使两数都 badly approximable。；若 $u+v\alpha+w\beta=0$ 为非平凡整数关系且 $w\ne0$，取 $\alpha$ 的收敛分母 $q$ 并令 $n=|w|q$，则两项距离均为 $O(\|q\alpha\|)$，所以乘积为 $O(q\|q\alpha\|^2)=O(1/q)\to0$；退化情形给出某一数有理。；二维 Dirichlet 只能在尺度 $q\le Q^2$ 上保证两距离均 $\le Q^{-1}$，由此仅得 $q\|q\alpha\|\|q\beta\|\le1$，不足以趋零。
- 第一阻塞点：临界指数处缺少任意增益：需把同时逼近中的 $Q^{-1}$ 至少一处改成 $o(Q^{-1})$，或证明对应对角轨道必进入更深尖点；这正是 Littlewood 猜想的核心，而非取整技术缺口。
- 下一步：对一个具体未覆盖类别（例如不同实二次域中的两个二次无理数）计算其 $SL_3(\mathbb R)/SL_3(\mathbb Z)$ 对角轨道，检验能否证明非紧性；成功即给出该类别的严格特例。
- 来源核对：[官方页面](https://www.erdosproblems.com/495)确认其为开放的 Littlewood 猜想。；[Einsiedler–Katok–Lindenstrauss](https://annals.math.princeton.edu/2006/164-2/p04)证明潜在反例集的 Hausdorff 维数为零；这不是空集结论。
- 时间记账：所在批次墙钟时间按题数均摊约 52.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/495)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/495.lean`；既有候选答案（按不可信材料审计）

### #500

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is $\mathrm{ex}_3(n,K_4^3)$? That is, the largest number of $3$-edges which can placed on $n$ vertices so that there exists no $K_4^3$, a set of 4 vertices which is covered by all 4 possible $3$-edges.
- 题意摘要：在所有顶点集大小为 $n$ 的三一致超图中，求不含完整四点三图 $K_4^3$（某四点的四个三元子集全为边）者的最大边数 $\mathrm{ex}_3(n,K_4^3)$；既问有限 $n$ 精确值，也包含渐近密度问题。
- 状态核对：精确值及猜想密度 $5/9$ 仍开放。旧候选所引“0.5615 改进”来源与题目不匹配，不能采纳；通行资料给 Razborov 上界约 $0.561666$，而输入官方文本的 $0.5611666$ 疑似数字误植。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：独立核验 Turán 三分构造的无 $K_4^3$ 性质与计数，再用四点集—缺边双计数取得一个完全初等的上界。
- 局部结论：把顶点均分为 $X_0,X_1,X_2$，取横截三元组及型别 $X_iX_iX_{i+1}$。按四点在三部中的分布 $(4,0,0),(3,1,0),(2,2,0),(2,1,1)$ 检查，每种至少缺一条三边，故构造确实 $K_4^3$-free。；若各部大小约 $n/3$，边数为 $|X_0||X_1||X_2|+\sum_i\binom{|X_i|}{2}|X_{i+1}|=(5/9+o(1))\binom n3$。；任一 $K_4^3$-free 三图的每个四点集至少含一条非边；每条非边属于 $n-3$ 个四点集，故非边数至少 $\binom n4/(n-3)=\binom n3/4$，从而 $e(H)\le(3/4)\binom n3$。
- 第一阻塞点：初等双计数只记录“每个四点至少一条非边”，完全丢失不同四点约束之间的相关性，无法把 $3/4$ 压到接近 $5/9$；达到现有上界需要旗代数或同等强度的局部密度约束。
- 下一步：建立四点诱导型的线性规划：列出各型密度、三点边密度及五点扩张一致性；先复现一个严格优于 $3/4$ 的有理上界，再判断哪些附加半正定约束是逼近 $0.561666$ 所必需。
- 来源核对：[官方页面](https://www.erdosproblems.com/500)记录 $5/9$ 构造及 Razborov 路线。；[Razborov 原论文](https://epubs.siam.org/doi/10.1137/090747476)确认使用旗代数/半正定方法改进多个数值界；其他文献通常转述该上界为约 $0.561666$，应核对原表格后再引用更多小数。
- 时间记账：所在批次墙钟时间按题数均摊约 52.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/500)；既有候选答案（按不可信材料审计）

### #501

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For every $x\in\mathbb{R}$ let $A_x\subset \mathbb{R}$ be a bounded set with outer measure $<1$. Must there exist an infinite independent set, that is, some infinite $X\subseteq \mathbb{R}$ such that $x\not\in A_y$ for all $x\neq y\in X$? If the sets $A_x$ are closed and have measure $<1$, then must there exist an independent set of size $3$?
- 题意摘要：第一问：对任意映射 $y\mapsto A_y$，其中每个 $A_y\subset\mathbb R$ 有界且外测度小于 $1$，是否必有无限 $X$，使所有不同的有序对 $x,y\in X$ 都满足 $x\notin A_y$？第二问改设每个 $A_y$ 闭且测度小于 $1$，问是否至少存在三点独立集；第二问没有有界性假设。
- 状态核对：这是复合问题：第一问仍列为开放，并记录 CH 下否定；第二问据最新官方整理已由 Newelski–Pawlikowski–Seredyński 更强地肯定——存在无限独立集。旧候选把第二问说成“无界闭集时三点仍开放”是错误的，必须删除。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `medium`
- 尝试路线：对第二问接受并核对已知自由集定理；对第一问尝试有限集逐点扩张，并审查旧候选给出的 CH 良序构造。
- 局部结论：对任意有限 $F\subset\mathbb R$，因为每个 $A_y$ 有限外测度且有界，存在无穷多个 $z\notin\bigcup_{y\in F}A_y$；因此扩张时所有“新点不属于旧集合”的方向可同时满足。；扩张失败只可能来自反方向条件 $y\notin A_z$：题设没有给出映射 $z\mapsto A_z$ 的可测性或联合规律，故上述选择不能控制它。；旧候选的 CH 简化构造不成立：不存在覆盖全体实数且每个初段都 bounded 的 $\omega_1$ 良序。若各区间 $[-N,N]$ 外已有点首次出现于某些可数序数，取这些序数之上确界后，相应初段已无界。因而不能用“令 $A_y$ 为全部早于 $y$ 的实数”满足有界性。
- 第一阻塞点：第一问的贪心扩张在反向条件处立即中断；而 CH 否定结果需要比“良序初段”精细得多的集合映射构造。仅凭二手摘要无法重建该构造，且当前官方讨论还质疑 Hechler 论文与精确题面的对应关系。
- 下一步：逐页核对 Hechler 1972 的集合映射定义、是否要求各值有界，以及其 CH 构造对应原题的哪一部分；随后把构造写成明确的 $A_y$ 并逐项验证 bounded、$m^*(A_y)<1$、无无限自由集。
- 来源核对：[最新官方页面](https://www.erdosproblems.com/501)明确称 NPS87 对闭且测度小于 $1$ 的情形给出无限独立集，故第二问已肯定解决。；同页仍记录第一问在 CH 下为否；但[官方讨论](https://www.erdosproblems.com/forum/thread/501)出现对 Hechler 结果究竟对应哪一版本的质疑，因此在读原论文前不宜把整题标成已证明独立。
- 时间记账：所在批次墙钟时间按题数均摊约 52.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/501)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/501.lean`；既有候选答案（按不可信材料审计）

### #503

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the size of the largest $A\subseteq \mathbb{R}^d$ such that every three points from $A$ determine an isosceles triangle? That is, for any three points $x,y,z$ from $A$, at least two of the distances $\lvert x-y\rvert,\lvert y-z\rvert,\lvert x-z\rvert$ are equal.
- 题意摘要：对每个维数 d，令 I(d) 为所有有限 A⊂R^d 中满足“任取三个互异点，其三条边至少两条等长”的集合的最大基数；问题要求确定 I(d)。已知 I(2)=6、I(3)=8，一般情形开放。
- 状态核对：开放状态与给定官方材料、本地 Lean 陈述一致。先前候选声称 d≤8 的精确值已知，但未获官方材料支持，且与“仅列出 d=2,3 的精确结果”的上下文明显冲突，故不采纳该表及其极值构型断言。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先严格核验超单纯形构造，再尝试把三点条件转为低次数多项式约束。令 m=d+1，在超平面 H={x∈R^m:Σx_i=2}≅R^d 中取 v_ij=e_i+e_j，并加入重心 c=(2/m)(1,…,1)。固定两点 x,y∈A 后，其余 z 必须落在两个球面或垂直平分超平面的并集，等价于一个次数至多 5 的多项式为零；希望以多项式维数控制 |A|。
- 局部结论：不同 v_ij,v_kl 的距离只有 sqrt(2)（两条边共享端点）和 2（端点不交）两种，因此任意三个 v_ij 自动构成等腰三角形。；对所有 i<j，有 ||v_ij-c||²=2-4/m，故含 c 的任意三点中两条从 c 出发的边相等。于是严格得到 I(d)≥C(d+1,2)+1（d≥2）。；固定 x≠y 后，每个 z∈A\{x,y} 满足 (||z-x||²-||x-y||²)(||z-y||²-||x-y||²)(||z-x||²-||z-y||²)=0。
- 第一阻塞点：这些次数至多 5 的消失多项式随点对 (x,y) 改变，彼此存在大量依赖；尚不能构造足够多线性无关的插值函数，把零点条件转化为 C(d+2,2) 级的秩界，更无法缩小已知上下界间的差距。
- 下一步：对小维 d=4 建立上述点对多项式在 A 上的评价矩阵，计算其秩和线性关系；检验能否把三次因子结构降到二次多项式空间，而不是直接处理次数 5。
- 来源核对：本地 503.lean 确认一般问题开放，并分别形式化了 d=2、d=3 及 Blokhuis 上界。；超单纯形加重心构造已直接计算核验，不依赖先前候选。
- 时间记账：所在批次墙钟时间按题数均摊约 38.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/503)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/503.lean`；既有候选答案（按不可信材料审计）

### #507

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha(n)$ be such that every set of $n$ points in the unit disk contains three points which determine a triangle of area at most $\alpha(n)$. Estimate $\alpha(n)$.
- 题意摘要：对每个 n，定义 α(n)=sup_{P⊂D, |P|=n} min_{三点子集 T⊂P} Area(T)，其中 D 是单位圆盘。也就是说，α(n) 是对任意 n 点配置都能保证出现的小三角形面积阈值中的最小最佳值；要求估计其渐近阶。
- 状态核对：仍开放；给定材料给出的已知区间为 (log n)/n²≪α(n)≪n^{-7/6+o(1)}。候选答案没有解决该缺口。其“由三角剖分平均面积得 O(1/n)”需要补足面数计算，下面给出严格版本。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：上界采用平面三角剖分；下界采用随机点并删除所有面积过小三角形的概率法，以重建初等的 n^{-2} 级结论。
- 局部结论：若 P 不共线，将其作直边三角剖分。设凸包顶点数为 h，则有 2n-h-2≥n-2 个有界三角面，总面积不超过 π，故某三角形面积≤π/(n-2)。若有三点共线，最小面积已为 0。因此 α(n)≤π/(n-2)。；取两个独立均匀圆盘点 p,q。给定 p,q，第三点使三角形面积≤t 的区域包含在直线 pq 周围宽度 O(t/|p-q|) 的带内，故条件概率≤C min(1,t/|p-q|)。圆盘内 E(|p-q|^{-1})<∞，所以单个随机三角形成为坏三角形的概率≤Ct。；先随机取 2n 个点，令 t=c/n²。坏三角形期望数≤C·C(2n,3)t=O(cn)。取 c 足够小，可找到坏三角形少于 n 的配置；每个坏三角形删去一个点后仍余至少 n 点，且不再有面积≤t 的三角形。因此 α(n)≥c'/n²。
- 第一阻塞点：该删除法的三元事件只使用一阶期望，天然在 t≈n^{-2} 处饱和；它不能产生 KPS 下界中的额外 log n。要得到该因子必须利用坏三角形超图的依赖、度数或局部稀疏结构，而不能逐坏边删除。
- 下一步：精确估计坏三角形三均匀超图的共度分布，并检验适用的独立集/容器引理是否能从 2n 个随机点保留 n 点且容许 t≈(log n)/n²。
- 来源核对：本地 507.lean 将 α 定义为极值量，并记录 trivial O(1/n)、Erdős Ω(1/n²)、KPS 与 CPZ 界。；已独立补全三角剖分面数及随机删除法；未把文献级最优界冒充为本次证明。
- 时间记账：所在批次墙钟时间按题数均摊约 38.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/507)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/507.lean`；既有候选答案（按不可信材料审计）

### #509

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)\in\mathbb{C}[z]$ be a monic non-constant polynomial. Can the set\[\{ z\in \mathbb{C} : \lvert f(z)\rvert \leq 1\}\]be covered by a set of circles the sum of whose radii is $\leq 2$?
- 题意摘要：对每个首一、非常数复多项式 f，令 E_f={z∈C:|f(z)|≤1}。问题问：是否总存在有限或可数个闭圆盘覆盖 E_f，且半径总和不超过 2？这里必须解释为圆盘；若“circles”仅指圆周，则有内点的 E_f 不可能被覆盖。
- 状态核对：一般情形开放；已知普遍常数 2e、改进常数 2.59，以及 E_f 连通时常数 2。先前候选的 Cartan 路线方向正确，但只是重建已知 2e 界，并未接近证明常数 2。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：将 f(z)=∏_{j=1}^n(z-z_j)，应用根的聚类覆盖思想。先核验低次数，再考察 Cartan 覆盖引理中常数 e 的来源能否借助首一 lemniscate 的特殊结构消除。
- 局部结论：E_f 是紧集：|f(z)|→∞ 当 |z|→∞，故只需考虑有限子覆盖。；若 n=1，则 E_f 本身是半径 1 的圆盘；若 n=2，则 ∏_{j=1}²|z-z_j|≤1 蕴含至少一个 |z-z_j|≤1，所以两个单位圆盘覆盖 E_f，半径和正好为 2。因此问题对次数≤2成立。；按 Cartan 覆盖引理的标准形式，参数 H=e 时，在总半径≤2e 的圆盘外有 ∏|z-z_j|>1，从而严格重建普遍 2e 覆盖。
- 第一阻塞点：Cartan 合并根簇时得到的乘积下界含有 e^{-n} 损失。仅利用“乘积≤1”无法像二次情形那样推出某根距离≤2/n 或形成总半径 2 的聚类；尚无严格不等式可把 H=e 降至 H=1。
- 下一步：先处理次数 3：按三根最小生成树的两条边长度分类，显式构造至多三个圆盘并优化半径和；若出现反例式参数区间，再计算其 lemniscate 连通分支以调用连通情形结果。
- 来源核对：本地 509.lean 明确把 cover 对象定义为闭圆盘，并分别记录 2e、2.59 和连通情形常数 2。；次数 1、2 的覆盖已直接核验。
- 时间记账：所在批次墙钟时间按题数均摊约 38.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/509)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/509.lean`；既有候选答案（按不可信材料审计）

### #510

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $A\subset \mathbb{Z}$ is a finite set of size $N$ then is there some absolute constant $c>0$ and $\theta$ such that\[\sum_{n\in A}\cos(n\theta) < -cN^{1/2}?\]
- 题意摘要：字面陈述量词是：是否存在统一常数 c>0，使每个有限 A⊂Z（N=|A|）都有某个实数 θ 满足 Σ_{n∈A}cos(nθ)<-c√N。若采用标准 Chowla 版本，则应限定 A 为不含 0 的正整数集合，通常只要求所有充分大的 N。
- 状态核对：输入的 exact_statement 按字面是假的，与 current_status=open 不一致。先前候选指出零频率障碍是正确的，但应更直接用 A={0}；本地 510.lean 已修正为 A⊂N、0∉A 且对充分大 N，修正版仍开放。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：先反驳字面版本；随后对修正版尝试从均值和二阶矩推出负值，并定位为何初等矩方法达不到 √N。
- 局部结论：取 A={0}，N=1。对所有 θ，Σ_{n∈A}cos(nθ)=1，不可能小于 -c。因此 exact_statement 对任何 c>0 均失败。；对修正版令 S(θ)=Σ_{n∈A}cos(nθ)。若 A⊂N\{0}，则平均值 ∫S=0，且归一化二阶矩 ∫S²=N/2。又 -m≤S≤N，其中 m=-min S；由 (N-S)(S+m)≥0 得 S²≤(N-m)S+Nm。积分后得到 N/2≤Nm，即 min S≤-1/2。；上述方法即使保留精确二阶矩，也只给常数量级；要达到 -c√N 必须引入更高阶加性结构或谱/切割信息。
- 第一阻塞点：从 L² 质量不能推出负部振幅为 Ω(√N)：正部允许达到 N，并可承载大部分二阶矩。缺少控制正尖峰或强迫负部扩散的结构性估计，这正是开放问题的核心。
- 下一步：对修正版计算 ∫S^{2k} 的加性关系解释，并在低加性能量（近 Sidon）与高加性能量两类中分别测试能否推出优于常数的负下界；同时正式修订数据中的 exact_statement，加入 0∉A 或 A⊂Z_{>0}。
- 来源核对：本地 510.lean 明确采用 A⊂N、0∉A、N→∞ 的修正版，并记录 N^{1/7} 已知结果。；零频率反例及二阶矩不等式均已独立核验。
- 时间记账：所在批次墙钟时间按题数均摊约 38.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/510)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/510.lean`；既有候选答案（按不可信材料审计）

### #513

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f=\sum_{n=0}^\infty a_nz^n$ be a transcendental entire function. What is the greatest possible value of\[\liminf_{r\to \infty} \frac{\max_n\lvert a_nr^n\rvert}{\max_{\lvert z\rvert=r}\lvert f(z)\rvert}?\]
- 题意摘要：对每个超越整函数 f(z)=Σa_nz^n，定义最大项 μ_f(r)=max_n|a_n|r^n 和最大模 M_f(r)=max_{|z|=r}|f(z)|。问题所求是 S=sup_f liminf_{r→∞} μ_f(r)/M_f(r)；“greatest”应理解为上确界，不预设有函数取到它。
- 状态核对：开放；给定材料称 1/2<S≤2/π-c。先前候选的稀疏级数只能构造 liminf=1/2，不能解释严格不等式 S>1/2；其 Parseval 路线可给一个较弱但可严格闭合的普遍上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：核验候选中的 lacunary 构造，并用最大项切换半径结合 Parseval，尝试取得普遍上界。
- 局部结论：对 f(z)=Σ_{k≥0}e^{-4^k}z^{2^k}，在相邻项切换半径 log r_k=3·2^k 时，第 k、k+1 项相等；其余项相对它们指数级小。因系数非负，M(r)=f(r)，故 μ(r_k)/M(r_k)→1/2。相邻切换之间单项占优，从而该例的 liminf 为 1/2。；超越整函数有无穷多个有效最大项；其上凸包相邻有效项的切换半径趋于无穷。在每个切换半径，至少两个不同项同时等于 μ(r)。；Parseval 给 M(r)²≥(1/2π)∫|f(re^{iθ})|²dθ=Σ|a_n|²r^{2n}≥2μ(r)²。因此沿无穷切换半径 μ(r)/M(r)≤1/√2，严格得到 S≤1/√2；这弱于已知的 2/π-c。
- 第一阻塞点：Parseval只记录平方和，完全丢失切换项的相位与圆周最大值几何；两项同时最大只能给常数 1/√2。要降到 2/π 附近乃至确定 S，必须控制较长的近最大项区块及其三角多项式峰值，而本路线尚不能保证这种区块存在。另一方面，正系数稀疏构造在每次两项交接时被锁死在 1/2，不能产生 Kővári 的严格提升。
- 下一步：研究三个连续有效最大项的对数凸包间距：给定两次相邻切换半径之比，建立对应三项三角多项式的最优 L∞/最大系数下界；先数值求解该有限维极值，再尝试证明统一不等式。
- 来源核对：本地 513.lean 将目标形式化为对超越整函数的上确界，并记录 2/π-c 上界及严格大于 1/2。；稀疏级数的切换半径、旁项衰减与 Parseval 推导均已重新计算；没有把候选中的文献摘要当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 38.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/513)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/513.lean`；既有候选答案（按不可信材料审计）

### #514

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)$ be an entire function. Does there exist a path $L$ so that, for every $n$,\[\lvert f(z)/z^n\rvert \to \infty\]as $z\to \infty$ along $L$? Can the length of this path be estimated in terms of $M(r)=\max_{\lvert z\rvert=r}\lvert f(z)\rvert$? Does there exist a path along which $\lvert f(z)\rvert$ tends to $\infty$ faster than a fixed function of $M(r)$ (such that $M(r)^\epsilon$)?
- 题意摘要：官网现行量词是：对每个超越整函数 f，是否存在同一条趋于无穷的路径 L，使得对每个整数 n≥0，|f(z)|/|z|^n→∞；另问该路径截断长度 ℓ_L(r) 能否由 M(r) 控制，以及能否在路径上取得如 |f(z)|≥M(|z|)^ε 一类下界。输入文本漏掉了“超越”。
- 状态核对：若按输入的“任意整函数”，命题立即被多项式反驳；官网已于 2025-10 修正为超越整函数。Boas 的未刊结果解决了存在路径的第一问，但后两个定量问题仍开放，旧候选列出的具体长度定理未得到本次原始来源核实，故不采纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：考察开集 U_n(R)={z:|z|>R且|f(z)|>|z|^n}，试图选择嵌套的无界分支并拼成一条路径。超越性先保证每个 U_n(R) 在任意充分大尺度上非空；若能证明适当无界分支嵌套，便可对 n 作对角化。
- 局部结论：若 f 是 d 次多项式，则取 n>d，沿任何趋于无穷路径都有 |f(z)/z^n|→0；因此“超越”假设必不可少。；对超越整函数，log M(r)/log r→∞，故对每个固定 n，M(r)/r^n→∞；于是每个充分大的圆周上都有满足 |f(z)|>|z|^n 的点。；圆周最大模点的存在只给出离散点列；任意连接这些点的线段可能穿过小模区域，既不保持下界，也不给出路径长度控制。
- 第一阻塞点：第一处缺口是无法仅由 M(r)/r^n→∞证明 U_n(R) 含有可兼容、嵌套的无界连通分支；最大模原理不排除高模区域在不同半径间换支。M(r)^ε 问题还需先固定“最终下界”还是“比值趋于无穷”的量词。
- 下一步：对 U_n(R) 的连通分支做有限半径计算/拓扑引理检验：证明或寻找反例于“每个大圆都交 U_n(R) ⇒ U_n(R) 有无界分支”；若失败，则定位 Boas 证明中额外使用的最小模或子调和函数工具。
- 来源核对：[Erdős Problems 514 现行页](https://www.erdosproblems.com/514)及其修订历史确认现行对象是超越整函数。；Boas 结果仅由官方页记载为未刊；未找到可独立重建其全部证明的原始文本。
- 时间记账：所在批次墙钟时间按题数均摊约 66.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/514)；既有候选答案（按不可信材料审计）

### #517

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)=\sum_{k=1}^\infty a_kz^{n_k}$ be an entire function (with $a_k\neq 0$ for all $k\geq 1$). Is it true that if $n_k/k\to \infty$ then $f(z)$ assumes every value infinitely often?
- 题意摘要：设 n_1<n_2<…、a_k≠0，且级数 f(z)=∑_{k≥1}a_kz^{n_k} 在整个复平面收敛；假设 n_k/k→∞。问题是：是否对每个 w∈ℂ，纤维 {z:f(z)=w} 都是无限集。
- 状态核对：仍为 Fejér–Pólya 开放问题。人工评审指出的错误完全成立：Murai 并未构造遗漏 0 的 Fabry-gap 整函数；其主定理反而是更强的 Fejér-gap 条件下没有有限亏值。由 δ(0,g)=1 即使成立也不能推出 g 无零点，而“逐盘无零的近似多项式”若缺少共同的逐盘最终无零性质，也不能应用 Hurwitz。旧候选反例作废。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：用大 Picard 定理把问题归约到排除唯一可能的例外值。若某个 w 只被取有限次，则 f-w 的零点有限，因而可写成 f-w=P e^g，其中 P 为记录这些零点的多项式、g 为整函数；再尝试用 f 的零密度 Taylor 支撑与 Pe^g 的系数结构矛盾。
- 局部结论：n_k/k→∞蕴含 n_{k+1}-n_k 无界；否则 n_k=O(k)。因此有限阶情形落入 Pólya 已知定理的适用范围。；f 是超越整函数；由大 Picard，至多存在一个复数 w 不是被无限次取到。因此只需排除一个有限纤维例外值。；若 f(z)=w 只有有限多个解（计重数），则除去相应多项式 P 后，(f-w)/P 是无零整函数；因 ℂ 单连通，它有整对数，故 f-w=Pe^g。
- 第一阻塞点：无法严格证明 Pe^g 的 Taylor 系数不可能支撑在密度为零的指数集上。指数展开存在全局抵消，而 Fabry 条件 n_k/k→∞本身不给出 Fejér 条件 ∑1/n_k<∞所提供的可求和控制。
- 下一步：先检验可证的中间命题：若 Pe^g 的非零 Taylor 指数满足 n_k/k→∞，是否必有 g 为多项式；可从 g 为一次或有限次多项式的系数递推开始，确定有限阶证明究竟使用了哪一项增长估计。
- 来源核对：[Murai 1983 原论文页面](https://aif.centre-mersenne.org/articles/10.5802/aif.930/)明确写明：Fejér gaps 的整函数没有有限亏值。；本地 Lean 陈述使用 `HasFabryGaps n`，并把结论形式化为每个纤维均为无限集；文件本身仍含 `sorry`，不是机器证明。；[Erdős Problems 517](https://www.erdosproblems.com/517)仍列为开放。
- 时间记账：所在批次墙钟时间按题数均摊约 66.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/517)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/517.lean`；既有候选答案（按不可信材料审计）

### #520

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f$ be a Rademacher multiplicative function: a random $\{-1,0,1\}$-valued multiplicative function, where for each prime $p$ we independently choose $f(p)\in \{-1,1\}$ uniformly at random, and for square-free integers $n$ we extend $f(p_1\cdots p_r)=f(p_1)\cdots f(p_r)$ (and $f(n)=0$ if $n$ is not squarefree). Does there exist some constant $c>0$ such that, almost surely,\[\limsup_{N\to \infty}\frac{\sum_{m\leq N}f(m)}{\sqrt{N\log\log N}}=c?\]
- 题意摘要：在同一概率空间上给各素数独立赋 Rademacher 符号，并令 f(n)=∏_{p|n}f(p)（n 平方自由），非平方自由时为 0。问是否存在确定常数 c>0，使几乎每个样本都有 limsup_{N→∞} S_N/√(N log log N)=c，其中 S_N=∑_{m≤N}f(m)。
- 状态核对：冻结日期 2025-08-31 时仍开放；但 Caich 预印本的 2026-03-22 修订版 Theorem 1.1 宣称几乎处处上界 √x(log log x)^{1/4+ε}。若该修订定理成立，它已经否定题目：limsup 必为 0，而非正数。由于这是冻结后预印本更新，结论应标作“由当前预印本给出的已知否定”，并等待同行评审/官网状态同步。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：先独立计算二阶矩，再把 Caich 的新上界代入题中归一化。取任意固定 0<ε<1/4，则 |S_N|/√(N log log N)≪(log log N)^{-1/4+ε}→0，故该有符号比值也趋于 0。
- 局部结论：对不同平方自由数 m≠n，E[f(m)f(n)]=0，因为其素因子集合的对称差非空；且 E f(n)^2=1_{n平方自由}。；因此 E S_N^2=#{n≤N:n平方自由}∼(6/π²)N；独立变量类比会猜测 √12/π，但二阶正交不足以应用经典 LIL。；采用 2026 修订版上界并取 ε=1/8，可严格推出 |S_N|/√(N log log N)≪(log log N)^{-1/8}→0，故 limsup=0。
- 第一阻塞点：内部推导没有缺口；唯一外部依赖是 Caich 2026 修订版 Theorem 1.1 的正确性与最终出版状态。冻结材料中的旧指数 3/4 不能推出该结论。
- 下一步：逐节审查 Caich 修订稿中把 3/4 降至 1/4 的新 Hoeffding/超鞅估计，特别核验 Proposition 6.11 的坏事件可求和性；随后请求官方问题页更新状态。
- 来源核对：[Caich 当前 arXiv 正文](https://arxiv.org/abs/2304.00943)标注 2026-03-22，Theorem 1.1 给出指数 1/4+ε；页面旧摘要仍显示 3/4，存在元数据不同步。；[Harper 的几乎处处下界](https://arxiv.org/abs/2012.15809)给出 √x(log log x)^{1/4+o(1)} 量级，与新上界相容。；本地 Lean 陈述量化为存在统一 c>0；其中仍有 `sorry`，不能视为形式化证明。
- 时间记账：所在批次墙钟时间按题数均摊约 66.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/520)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/520.lean`；既有候选答案（按不可信材料审计）

### #521

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $(\epsilon_k)_{k\geq 0}$ be independently uniformly chosen at random from $\{-1,1\}$. If $R_n$ counts the number of real roots of $f_n(z)=\sum_{0\leq k\leq n}\epsilon_k z^k$ then is it true that, almost surely,\[\lim_{n\to \infty}\frac{R_n}{\log n}=\frac{2}{\pi}?\]
- 题意摘要：固定一条无限 i.i.d. Rademacher 系数序列，并令 f_n(x)=∑_{k=0}^nε_kx^k。R_n 是 f_n 在整个实轴上的实根数（通常计重数）。问题要求在这一共同耦合下，几乎处处沿所有 n 有 R_n/log n→2/π。
- 状态核对：仍开放。Do 已证明同一耦合下 [-1,1] 内根数除以 log n 几乎处处趋于 1/π；这只给总根数的一半。旧候选关于倒数多项式的警告正确：逐个 n 的分布对称不能自动成为整个序列的几乎处处结论。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：分解 R_n=N_n([-1,1])+N_n(ℝ\[-1,1])。第一项用 Do 的强律；对第二项令 f_n^*(x)=x^nf_n(1/x)=∑_{k=0}^nε_{n-k}x^k，则外部非零根与 f_n^* 在 (-1,1) 内的根一一对应。尝试把 Do 的强律应用于倒序三角阵列。
- 局部结论：Do 的定理严格给出 N_n([-1,1])/log n→1/π 几乎处处，因此 liminf R_n/log n≥1/π。；对每个固定 n，f_n^* 与 f_n 同分布，且除去端点后 N_n(ℝ\[-1,1])=N_{f_n^*}((-1,1))。所以外部根数/log n→1/π 至少在概率意义下成立。；现有浓度界沿几何增长子序列可由 Borel–Cantelli 给出总实根数/log n→2/π 的几乎处处子序列结论。
- 第一阻塞点：序列 (ε_{n},ε_{n-1},…,ε_0) 随 n 改变其起点，不是某条固定 i.i.d. 幂级数的前缀；故 Do 的最大不等式不能直接用于全部倒数多项式。根数随 n 也不单调，不能在稀疏子序列间夹逼。
- 下一步：证明一个倒序块最大估计：对 dyadic 块 2^j≤n<2^{j+1}，控制 sup_n|N_{f_n^*}((-1,1))-(1/π)log n|，并使偏差 εj 的概率对 j 可求和。
- 来源核对：[Do 2024 原预印本](https://arxiv.org/abs/2403.06353)的主定理仅覆盖 [-1,1]；其 lacunary 部分可覆盖 ℝ。；[Can–Nguyen 浓度论文](https://arxiv.org/abs/2311.15446)说明全实轴尾界仍次优。；[Erdős Problems 521](https://www.erdosproblems.com/521)仍列为开放。
- 时间记账：所在批次墙钟时间按题数均摊约 66.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/521)；既有候选答案（按不可信材料审计）

### #522

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)=\sum_{0\leq k\leq n} \epsilon_k z^k$ be a random polynomial, where $\epsilon_k\in \{-1,1\}$ independently uniformly at random for $0\leq k\leq n$. Is it true that, if $R_n$ is the number of roots of $f(z)$ in $\{ z\in \mathbb{C} : \lvert z\rvert \leq 1\}$, then\[\frac{R_n}{n/2}\to 1\]almost surely?
- 题意摘要：固定同一条无限 i.i.d. Rademacher 序列，P_n(z)=∑_{k=0}^nε_kz^k；R_n 按重数统计闭单位圆盘 |z|≤1 内的零点。问题要求几乎处处沿所有 n 有 2R_n/n→1。
- 状态核对：冻结状态为开放；Yakir 仅证明依概率收敛。2026-04 出现一份无署名、未见同行评审的网络稿件声称强律及 O_ω(n^{149/150})，但不能仅凭“像证明”就认定解决，故这里只把其 Jensen 路线作为待审材料。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：使用倒数多项式 Q_n(z)=z^nP_n(1/z)。若 U_n 是单位圆上的零点数，则确定性地有 R_n(P_n)+R_n(Q_n)=n+U_n；且对固定 n，P_n、Q_n 同分布。再尝试通过 Jensen 公式在半径 1 与 ρ_n=1-n^{-1-α} 间控制 R_n-n/2，并对 dyadic 块使用 Borel–Cantelli。
- 局部结论：倒数映射把 |z|<1 与 |z|>1 的零点互换，边界零点固定，因此 R_n(P_n)+R_n(Q_n)=n+U_n。；由同分布性，E R_n=n/2+E U_n/2；若单位圆零点概率趋零，则得到 E R_n=n/2+o(n)，但这不含样本间集中信息。；Yakir 的结果给出 P(|R_n-n/2|≥n^{9/10})→0，故 2R_n/n→1 依概率；若能取得多项式衰减尾界，则沿足够稀疏子序列可直接用 Borel–Cantelli 得到几乎处处收敛。
- 第一阻塞点：第一处缺口是从单个 n 的概率尾界过渡到所有 n：已给出的误差概率不保证对 n 可求和，而 R_n 随次数增加不单调。2026 网络稿试图用平滑对数积分的块一致估计填补此处，但其关键的统一小值控制和块插值尚需逐行独立核验。
- 下一步：审计该稿的核心 Lemma 9/Proposition 10：核验 Nazarov–Nishry–Sodin 对数可积估计能否同时、统一地用于 P_n、Q_n、r∈{1,ρ_n} 及整块 n，并重新计算 Chebyshev 后的指数是否确实可求和。
- 来源核对：[Yakir 原论文](https://arxiv.org/abs/2011.06234)只证明 n^{9/10} 偏差概率趋于 0。；[Erdős Problems 522](https://www.erdosproblems.com/522)在冻结记录中仍为开放。；[2026-04 无署名网络稿](https://www.ulam.ai/research/erdos522.pdf)声称强律；因来源与审稿状态不明，本筛查不把它当作已知定理。；本地 Lean 陈述正确使用共同无限系数序列并统计闭圆盘内重根，但证明仍为 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 66.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/522)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/522.lean`；既有候选答案（按不可信材料审计）

### #524

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $t\in (0,1)$ let $t=\sum_{k=1}^\infty \epsilon_k(t)2^{-k}$ (where $\epsilon_k(t)\in \{0,1\}$). What is the correct order of magnitude (for almost all $t\in(0,1)$) for\[M_n(t)=\max_{x\in [-1,1]}\left\lvert \sum_{k\leq n}(-1)^{\epsilon_k(t)}x^k\right\rvert?\]
- 题意摘要：除二进有理数这一零测集外，令独立 Rademacher 符号为 $a_k(t)=(-1)^{\epsilon_k(t)}$。问题要求描述几乎处处的序列 $M_n(t)=\sup_{|x|\le1}|\sum_{k\le n}a_kx^k|$ 的正确量级；结合 Chung 的结果，目标应包含下包络行为，而不只是 $\limsup$。
- 状态核对：截至核查时仍列为 open。候选答案证明的 LIL 型 limsup 即使成立，也没有回答下包络问题；它与 Chung 给出的无穷多个 $M_n\ll\sqrt{n/\log\log n}$ 并不矛盾。人工评审指出的目标错位应明确吸收。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 $A_m=\sum_{k\le m}a_k$、$B_m=\sum_{k\le m}(-1)^ka_k$。先用端点和 Abel 变换夹住 $M_n$，再用 $A_n,B_n$ 的二维小球概率尝试证明下包络下界。
- 局部结论：严格有 $\max(|A_n|,|B_n|)\le M_n\le\max_{m\le n}(|A_m|,|B_m|)$；右式来自分别在 $[0,1]$、$[-1,0]$ 上作 Abel 变换。；写 $E=\sum_{2j\le n}a_{2j}$、$O=\sum_{2j-1\le n}a_{2j-1}$，则 $(A_n,B_n)=(E+O,E-O)$，且 $E,O$ 独立。因此对 $1\le u\le\sqrt n$，局部中心极限定理给出 $\Pr(M_n\le u)\le\Pr(|A_n|,|B_n|\le u)\ll (u+1)^2/n$。；LIL 夹逼确实推出几乎处处 $M_n=O(\sqrt{n\log\log n})$，并可推出相应尺度的 limsup；这只是上包络结论。
- 第一阻塞点：取猜测尺度 $u\asymp\sqrt{n/\log\log n}$ 时，上述小球上界仅为 $O(1/\log\log n)$，不可求和；而跨 $n$ 的事件高度相关。端点估计无法证明最终一致的下界，也无法重建 Chung 的无穷多次上界。
- 下一步：对几何子序列 $n_j$，计算条件小球概率 $\Pr(M_{n_j}\le u_j\mid\mathcal F_{n_{j-1}})$；首要可检验目标是判断能否得到足以应用条件 Borel–Cantelli 的准独立估计，取 $u_j=C\sqrt{n_j/\log\log n_j}$。
- 来源核对：Erdős Problems #524 页面仍标为 OPEN，并明确记录 Chung 的无穷多次小值和 Erdős 的下界：https://www.erdosproblems.com/524；页面于 2025-12-27 更新，仍未报告完整解答。
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/524)；既有候选答案（按不可信材料审计）

### #528

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n,k)$ count the number of self-avoiding walks of $n$ steps (beginning at the origin) in $\mathbb{Z}^k$ (i.e. those walks which do not intersect themselves). Determine\[C_k=\lim_{n\to\infty}f(n,k)^{1/n}.\]
- 题意摘要：固定整数 $k\ge1$，$f(n,k)$ 是从原点出发、顶点互异的 $n$ 步最近邻格路数；要求确定固定 $k$ 时指数增长率 $C_k=\lim_{n\to\infty}f(n,k)^{1/n}$。
- 状态核对：极限存在是已知定理，但对方格等一般 $\mathbb Z^k$ 的精确常数仍未知；因此“确定”尚未完成。候选答案关于次乘性的部分正确，数值估计不构成确定值。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用切割映射证明次乘性，再以有限长度枚举给出可验证上界；同时检查简单单调族能否给出匹配下界。
- 局部结论：在时刻 $m$ 切开一条 $(m+n)$ 步 SAW，并平移后缀，得到单射，故 $f(m+n,k)\le f(m,k)f(n,k)$。Fekete 引理于是给出 $C_k=\inf_{n\ge1}f(n,k)^{1/n}$。；只使用正坐标方向得到 $f(n,k)\ge k^n$；禁止立即折返得到 $f(n,k)\le2k(2k-1)^{n-1}$，所以 $k\le C_k\le2k-1$。；$k=1$ 时只有一直向左或一直向右两条路，故 $C_1=1$。任意精确枚举值 $f(m,k)$ 都立即给出严格可核验上界 $C_k\le f(m,k)^{1/m}$。
- 第一阻塞点：切割后得到的两段并非任意可拼接：它们还须彼此不相交。次乘性完全丢失了这一跨切口约束，且损失可能是指数级，因此不能由有限段计数反推出精确 $C_k$ 或匹配下界。
- 下一步：对指定的小维数（优先 $k=2$）枚举长度 $m$ 的 SAW，并加入桥分解；检验桥数的超乘性是否给出与 $f(m,2)^{1/m}$ 收敛的上下界区间。
- 来源核对：Erdős Problems #528 仍标为 OPEN，并记录 Hammersley–Morton 的极限存在性及 $k\le C_k\le2k-1$：https://www.erdosproblems.com/528；Slade 的资料页列出 lace expansion 对大维渐近展开的研究：https://personal.math.ubc.ca/~slade/research.html
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/528)；既有候选答案（按不可信材料审计）

### #529

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d_k(n)$ be the expected distance from the origin after taking $n$ random steps from the origin in $\mathbb{Z}^k$ (conditional on no self intersections) - that is, a self-avoiding walk. Is it true that\[\lim_{n\to \infty}\frac{d_2(n)}{n^{1/2}}= \infty?\]Is it true that\[d_k(n)\ll n^{1/2}\]for $k\geq 3$?
- 题意摘要：在所有从原点出发的 $n$ 步 SAW 上取均匀分布，令 $X_n$ 为终点、$d_k(n)=\mathbb E\|X_n\|_2$。问题分别问：二维是否有 $d_2(n)/\sqrt n\to\infty$；以及每个固定 $k\ge3$ 是否有 $d_k(n)=O_k(\sqrt n)$。
- 状态核对：截至核查仍 open。第二问对 $k\ge5$ 已知为真；对 $k=3,4$ 未解决且现行预测为假。候选答案中由均方位移直接推出一阶矩下界的表述不充分：$d_k\le(\mathbb E\|X_n\|^2)^{1/2}$ 只有一个方向，反向需要尾界或分布收敛。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：从尾积分公式 $d_k(n)=\int_0^n\Pr(\|X_n\|>r)\,dr$ 出发，尝试把已知的次弹道尾界及高维高斯极限转化为所需的一阶矩结论。
- 局部结论：Duminil-Copin–Hammond 的结论给出：每个固定 $v>0$，$\Pr(\max_{j\le n}\|X_j\|>vn)\le e^{-c(v)n}$。于是 $d_k(n)/n\le v+e^{-c(v)n}$，先令 $n\to\infty$ 再令 $v\downarrow0$，严格得到所有 $k\ge2$ 的 $d_k(n)=o(n)$。；恒有 $d_k(n)\le R_k(n):=(\mathbb E\|X_n\|^2)^{1/2}$；反向只由 $\|X_n\|\le n$ 得到很弱的 $d_k(n)\ge R_k(n)^2/n$。；对 $k\ge5$，lace expansion 给出线性均方位移及高斯尺度极限；配合二阶矩一致可积性，可推出 $d_k(n)/\sqrt n$ 收敛到正的高斯一阶矩常数，故该范围内第二问成立。
- 第一阻塞点：二维次弹道尾界只排除了线性尺度，完全不排除 $d_2(n)=O(\sqrt n)$。要证明超扩散，必须在 $r\gg\sqrt n$ 的尺度得到正质量下界；现有尾积分路线没有这样的反集中估计。对 $k=3,4$ 同样缺少足以判定 $O(\sqrt n)$ 的端点尺度控制。
- 下一步：选取 $r_n=\sqrt n\,L(n)$，直接研究可枚举的比率 $\#\{\omega:\|X_n\|\ge r_n\}/f(n,k)$；理论上的首个目标是对某个 $L(n)\to\infty$ 证明该比率乘以 $L(n)$ 不趋零，从而经尾积分推出二维结论。
- 来源核对：原论文摘要给出所有 $d\ge2$ 的指数型次弹道尾界：https://arxiv.org/abs/1205.0401；Hara–Slade 的高维结果记录了 $d\ge5$ 的线性均方位移及布朗极限：https://kyushu-u.elsevierpure.com/en/publications/self-avoiding-walk-in-five-or-more-dimensions-i-the-critical-beha/；Erdős Problems #529 仍标为 OPEN，并记录二维、三维、四维的预测尺度：https://www.erdosproblems.com/529
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/529)；既有候选答案（按不可信材料审计）

### #530

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\ell(N)$ be maximal such that in any finite set $A\subset \mathbb{R}$ of size $N$ there exists a Sidon subset $S$ of size $\ell(N)$ (i.e. the only solutions to $a+b=c+d$ in $S$ are the trivial ones). Determine the order of $\ell(N)$. In particular, is it true that $\ell(N)\sim N^{1/2}$?
- 题意摘要：令 $s(A)$ 为有限实数集 $A$ 中最大 Sidon 子集的大小，其中 $a+b=c+d$ 只允许无序对 $\{a,b\}=\{c,d\}$。则 $\ell(N)=\min_{A\subset\mathbb R,\,|A|=N}s(A)$；已问清其阶，并进一步问 $\ell(N)/\sqrt N\to1$ 是否成立。
- 状态核对：指数阶已经由 KSS 定理确定为 $\Theta(\sqrt N)$，但常数 1 的渐近式仍 open。候选答案的这一状态判断与权威记录一致。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：独立尝试随机抽样后删除冲突：以概率 $p$ 保留每个元素，再从每个非平凡加法四元组中删除至少一个点。
- 局部结论：非平凡关系 $a+b=c+d$ 的有序数量至多 $N^3$，因为给定 $a,b,c$ 后 $d$ 唯一。；若随机保留集为 $R$，则 $\mathbb E|R|=pN$，完整落入 $R$ 的冲突数期望至多 $p^4N^3$。逐冲突删一点后仍有 Sidon 集，故存在大小至少 $pN-p^4N^3$ 的 Sidon 子集。；取 $p=cN^{-2/3}$ 并优化常数，严格恢复 $\ell(N)\gg N^{1/3}$。结合已知 KSS 投影/结构定理可升级为 $\ell(N)\gg\sqrt N$；取 $A=[N]$ 则给出 $(1+o(1))\sqrt N$ 的已知上界。
- 第一阻塞点：粗略把冲突数界为 $N^3$ 并逐个删除，会重复支付高度重叠的关系；目标 $p\asymp N^{-1/2}$ 时删除项估计为 $\asymp N$，大于保留的 $\asymp\sqrt N$。该方法看不到 KSS 所利用的线性关系结构，更看不到常数 1。
- 下一步：重建并量化 Ruzsa projection trick：把任意 $N$ 元实数集在保持所有四项线性关系的意义下嵌入长度 $O(N)$ 的算术级数；逐项核查嵌入长度常数，判断它能否把 $[m]$ 中近最优 Sidon 构造传回并改善通用下界常数。
- 来源核对：Erdős Problems #530 在 2026-04-08 更新后仍标为 OPEN，并确认 KSS 下界及常数 1 未知：https://www.erdosproblems.com/530；2025 年 Pach–Zakharov 论文的预备部分再次陈述任意有限实数集含 $c\sqrt{|A|}$ 大小 Sidon 子集，并指出 Ruzsa projection trick：https://real.mtak.hu/221002/1/s00493-025-00151-5.pdf
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/530)；既有候选答案（按不可信材料审计）

### #531

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(k)$ be the minimal $N$ such that if we two-colour $\{1,\ldots,N\}$ there is a set $A$ of size $k$ such that all subset sums $\sum_{a\in S}a$ (for $\emptyset\neq S\subseteq A$) are monochromatic. Estimate $F(k)$.
- 题意摘要：$F(k)$ 是最小的 $N$，使每个二染色 $[N]$ 都存在 $k$ 元集 $A\subset[N]$，满足全部非空子集和组成的集合 $\Sigma^*(A)\subset[N]$ 且同色；包含条件等价于 $\sum_{a\in A}a\le N$。要求估计 $F(k)$。
- 状态核对：存在性由 Folkman/Rado 理论保证，但数量级仍 open。已知下界为双指数 $2^{2^{k-1}/k}$；候选答案声称某个具体“最佳塔高”上界，输入官方材料没有支持，本轮不采纳。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先尝试最直接的均匀独立随机二染色与联合界，并定位它为何只能给单指数下界；再对照已知的 2-adic 相关染色机制。
- 局部结论：固定 $A$，若 $r(A)=|\Sigma^*(A)|$，其全部子集和同色的概率恰为 $2^{1-r(A)}$。；对 $k$ 个不同正整数，标准压缩论证给出 $r(A)\ge k(k+1)/2$，等号由缩放的 $\{1,\ldots,k\}$ 达到。故坏事件总期望至多 $\binom Nk2^{1-k(k+1)/2}$。；取例如 $N\le (k/(2e))2^{(k+1)/2}$，上述期望小于 1，严格得到 $F(k)>N$，即一条初等但仅为 $k2^{k/2}$ 量级的下界。
- 第一阻塞点：均匀随机染色被小和集族卡住：形如 $p\{1,\ldots,k\}$ 的集合只有 $k(k+1)/2$ 个不同子集和，单个坏事件概率太大，联合界不可能产生双指数尺度。候选答案把“典型 $A$ 有约 $2^k$ 个和”的启发直接用于所有 $A$，忽略了这些结构化集合。
- 下一步：复核 BENTW 的具体染色：先随机染奇数，并强制 $\chi(2x)\ne\chi(x)$。下一项可检验任务是对固定 $A$ 证明其引理型界 $\Pr(\Sigma^*(A)\text{ 单色})$，按 $A$ 中奇偶子集和结构分类，独立重现双指数下界的核心概率估计。
- 来源核对：BENTW 原论文明确给出 $F(k)\ge2^{2^{k-1}/k}$，并说明均匀随机染色不足、改用沿倍增链交替的随机染色：https://arxiv.org/abs/1703.02473；Erdős Problems #531 仍标为 OPEN：https://www.erdosproblems.com/531
- 时间记账：所在批次墙钟时间按题数均摊约 52.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/531)；既有候选答案（按不可信材料审计）

### #533

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $\delta>0$. If $n$ is sufficiently large and $G$ is a graph on $n$ vertices with no $K_5$ and at least $\delta n^2$ edges then $G$ contains a set of $\gg_\delta n$ vertices containing no triangle.
- 题意摘要：原命题量词为：对每个固定的 \(\delta>0\)，存在 \(c_\delta>0,n_0\)，使得每个 \(n\ge n_0\) 的 \(K_5\)-free 图，只要 \(e(G)\ge\delta n^2\)，就有顶点集 \(S\) 满足 \(|S|\ge c_\delta n\) 且 \(G[S]\) 无三角形。否定式只需找到一个 \(\delta>0\)，使任意 \(c>0\) 都有任意大的反例。
- 状态核对：已证伪。冻结输入后的官方更新给出精确 Ramsey–Turán 密度 \(\delta_3(5)=1/12\)。候选答案的结论实质正确；人工评审所称“违反已知 \(\delta>1/16\) 结果”并不成立，因为候选反例只取 \(\delta<1/12<1/16\)。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：采用已知构造定理：Liu–Reiher–Sharifzadeh–Staden 构造 \(K_5\)-free 图列 \(G_N\)，满足 \(e(G_N)=(1/12-o(1))N^2\) 且最大无三角形诱导顶点集 \(\alpha_3(G_N)=o(N)\)。固定例如 \(\delta=1/13\)，即得到原命题的反例。
- 局部结论：当 \(N\) 足够大时，\(e(G_N)\ge N^2/13\)。；对任意固定 \(c>0\)，由 \(\alpha_3(G_N)=o(N)\)，最终有 \(\alpha_3(G_N)<cN\)。；因此不存在适用于 \(\delta=1/13\) 的正常数 \(c_\delta\)；而密度高于 \(1/12\) 时线性无三角形集确实被迫出现。
- 第一阻塞点：作为自足重建，第一处未展开的是 LRSS 几何构造为何同时保证 \(K_5\)-free、边密度 \(1/12-o(1)\) 和 \(\alpha_3=o(N)\)；这里调用了已发表构造定理。
- 下一步：逐条重建 LRSS 论文中对应 \((p,q)=(3,5)\) 的参数代入，核对其边数归一化是按 \(N^2\) 而非 \(\binom N2\)。
- 来源核对：[Erdős Problem 533](https://www.erdosproblems.com/533) 明确记录证伪及阈值 \(1/12\)。；核对了原始构造论文 [Geometric constructions for Ramsey–Turán theory](https://arxiv.org/abs/2103.10423) 的问题对象与参数范围。
- 时间记账：所在批次墙钟时间按题数均摊约 68.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/533)；既有候选答案（按不可信材料审计）

### #535

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 3$, and let $f_r(N)$ denote the size of the largest subset of $\{1,\ldots,N\}$ such that no subset of size $r$ has the same pairwise greatest common divisor between all elements. Estimate $f_r(N)$.
- 题意摘要：固定整数 \(r\ge3\)。\(f_r(N)\) 是所有 \(A\subseteq[1,N]\) 中满足“任何 \(r\) 个互异元素的全部两两 gcd 不恒等”的最大 \(|A|\)。所求是随 \(N\to\infty\) 的增长率，常数可依赖 \(r\)。
- 状态核对：仍开放，但冻结材料中的上界已过时：官方页面现记录现代向日葵界推出 \(f_r(N)\le N^{C_r\log\log\log N/\log\log N}=N^{o(1)}\)，强于旧的 \(N^{1/2+o(1)}\)。猜想仍是去掉分子中的 \(\log\log\log N\)。本地 Lean 文件只是带 `sorry` 的陈述，未形式验证。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先验证候选的分块素数下界，再考察向日葵归约。取 \(m(r-1)\) 个素数分成 \(m\) 块，每个数从每块恰选一个素数。若 \(r\) 个数的两两 gcd 均为 \(d\)，则每块由抽屉原理有一素数出现在某一对中，故它整除所有两两 gcd，从而出现在全部 \(r\) 个数中；逐块看便迫使这 \(r\) 个数相同，矛盾。
- 局部结论：恒等 gcd 为 \(d\) 等价于写成 \(a_i=db_i\) 后 \(b_i\) 两两互素；主问题本身不额外要求 \((b_i,d)=1\)。；上述构造严格给出 \(|A|=(r-1)^m\)，而取最小的 \(m(r-1)\) 个素数可令 \(m=(1+o(1))\log N/\log\log N\)。故 \(f_r(N)\ge N^{(\log(r-1)+o(1))/\log\log N}\)。；在平方自由、固定素因子数层中，\(r\) 个素数支持集形成向日葵就直接产生恒等两两 gcd；这是现代向日葵定理进入问题的严格局部归约。
- 第一阻塞点：第一处不能闭合的是把任意 \(A\subseteq[1,N]\) 无损压到平方自由、统一大小的支持集族：素数幂指数和不同 \(\Omega(n)\) 层会造成损失。现有方法控制该损失后仍留下 \(\log\log\log N\)，当前路线不能达到猜想的 \(N^{C_r/\log\log N}\)。
- 下一步：写出按 \(\Omega(n)\) 与大/小素因子分层的定量账本，精确定位 \(\log\log\log N\) 损失来自层数还是向日葵常数；尝试在最重层用带重数的向日葵版本消除该损失。
- 来源核对：[Erdős Problem 535](https://www.erdosproblems.com/535) 记录了当前 \(N^{o(1)}\) 上界及猜想。；现代输入定理核对自 [Alweiss–Lovett–Wu–Zhang](https://arxiv.org/abs/1908.08483)。；本地 Lean 陈述正确区分主问题与更强的 \(\Omega(n)=k\) 辅助版本，但全部证明仍为 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 68.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/535)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/535.lean`；既有候选答案（按不可信材料审计）

### #536

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$ and $N$ be sufficiently large. Is it true that if $A\subseteq \{1,\ldots,N\}$ has size at least $\epsilon N$ then there must be distinct $a,b,c\in A$ such that\[[a,b]=[b,c]=[a,c],\]where $[a,b]$ denotes the least common multiple?
- 题意摘要：等价表述为：令 \(f(N)\) 是不含三个互异元素 \(a,b,c\) 满足 \([a,b]=[b,c]=[c,a]\) 的最大子集大小；问题问 \(f(N)=o(N)\) 是否成立，即对每个固定 \(\epsilon>0\)，存在 \(N_0(\epsilon)\)，使所有 \(N\ge N_0\) 及 \(|A|\ge\epsilon N\) 的 \(A\subseteq[1,N]\) 都含这种三元组。
- 状态核对：一般情形仍开放。已知 \(f(N)\le(221/225+o(1))N\)，所以可严格处理 \(\epsilon>221/225\)，但离任意正密度尚远。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：使用互不相交的显式 LCM 三角形。对 \(m\le N/15\) 且 \((m,30)=1\)，三元组 \(T_m=\{6m,10m,15m\}\subseteq[1,N]\) 的三对 lcm 都是 \(30m\)。互素限制保证不同 \(m\) 的这些三元组不相交。
- 局部结论：若共同 lcm 为 \(L\)，令 \(x=L/a,y=L/b,z=L/c\)，则条件等价于 \(x,y,z\) 两两互素，并有 \(\{a,b,c\}=\{tyz,txz,txy\}\)，其中 \(t=L/(xyz)\)。；可用的 \(m\) 数量为 \((4/225+o(1))N\)，因为 \(\varphi(30)/30=8/30\)。；无 LCM 三角形的 \(A\) 必须从每个互不相交的 \(T_m\) 至少删去一点，故 \(|A|\le(221/225+o(1))N\)。
- 第一阻塞点：第一处无法推进到任意 \(\epsilon>0\) 的步骤是：这族固定模板只能覆盖正比例 \(4/225\) 的互不相交约束；迭代更多模板会大量重叠，单纯相加删点数不再合法。
- 下一步：建立由所有小型模板 \(\{txy,txz,tyz\}\) 生成的三均匀超图，对截断模板族计算分数匹配数；若能超过 \(4N/225\)，即可得到可检验的新密度常数。
- 来源核对：[Erdős Problem 536](https://www.erdosproblems.com/536) 记录开放状态、上下界及 \(221/225\) 常数。；本地 Lean 陈述的自然语言量词基本一致，但以 `answer(sorry) ↔ ...` 包装，不能视为证明。
- 时间记账：所在批次墙钟时间按题数均摊约 68.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/536)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/536.lean`；既有候选答案（按不可信材料审计）

### #538

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$ and suppose that $A\subseteq\{1,\ldots,N\}$ is such that, for any $m$, there are at most $r$ solutions to $m=pa$ where $p$ is prime and $a\in A$. Give the best possible upper bound for\[\sum_{n\in A}\frac{1}{n}.\]
- 题意摘要：固定 \(r\ge2\)。对每个整数 \(m\)，有序表示 \((p,a)\)（\(p\) 为素数、\(a\in A\)、\(m=pa\)）至多 \(r\) 个；在所有 \(A\subseteq[1,N]\) 中求 \(S(A)=\sum_{a\in A}1/a\) 的最佳上界。
- 状态核对：仍开放。候选宣称的精确指数上界不能接受；人工评审指出的错误确实存在：所谓“每个纤维至多为第 \(r-1\) 个基本对称和”的局部不等式没有证明，且未经归一化时连包含 \(1\) 的简单纤维也可违背其形式。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：上界先做严格双计数；下界则独立复核候选的素数分块构造。令每块选择恰好 \(r-1\) 个素数。若 \(m=pa\)：当 \(p\mid a\) 或 \(p\) 在全部块外时表示唯一；当 \(p\) 位于某块但未整除 \(a\) 时，\(m\) 在该块恰有 \(r\) 个素因子，删去其中任一个恰给出 \(r\) 个表示。
- 局部结论：严格双计数给出 \(S(A)\sum_{p\le N}1/p\le r\sum_{m\le N^2}1/m\)，故 \(S(A)\ll r\log N/\log\log N\)。；分块构造确实满足“每个 \(m\) 至多 \(r\) 个表示”，这部分不依赖被评审否定的纤维上界。；令每块素数倒数和趋于 \(w\)，取 \(k\sim\log\log N/w\)，可得下界指数 \(((r-1)\log w-\log((r-1)!))/w\)。在 \(w=e((r-1)!)^{1/(r-1)}\) 处最大，得到 \(S(A)\ge(\log N)^{\alpha_r-o(1)}\)，\(\alpha_r=(r-1)/(e((r-1)!)^{1/(r-1)})\)。
- 第一阻塞点：首个缺口正是从全局“表示度至多 \(r\)”推出候选的逐块纤维基本对称和上界；条件允许素数幂、不同块型及纤维间耦合，现有论证没有排除这些贡献。因此下界虽可核验，却没有匹配上界。
- 下一步：先对 \(r=2\) 做有限素数支撑的加权极值计算，枚举所有满足表示度约束的下闭包/纤维，检验正确的局部不等式是否应带常数项或采用谱半径形式。
- 来源核对：[Erdős Problem 538](https://www.erdosproblems.com/538) 目前只记录 Erdős 的双计数上界。；候选的下界构造已逐情形核对表示数；其上界部分按人工评审意见剔除。
- 时间记账：所在批次墙钟时间按题数均摊约 68.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/538)；既有候选答案（按不可信材料审计）

### #539

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be such that, for any set $A\subseteq \mathbb{N}$ of size $n$, the set\[\left\{ \frac{a}{(a,b)}: a,b\in A\right\}\]has size at least $h(n)$. Estimate $h(n)$.
- 题意摘要：定义 \(Q(A)=\{a/\gcd(a,b):a,b\in A\}\)，并令 \(h(n)=\min_{A\subseteq\mathbb N,\ |A|=n}|Q(A)|\)。问题是估计 \(h(n)\) 的增长。
- 状态核对：官方状态仍列 open，但冻结输入已过时：2026 年更新记录了 \(h(n)\le n^{1/2}e^{O(\sqrt{\log n})}\)。结合经典下界，现已知 \(h(n)=n^{1/2+o(1)}\)；尚未得到 \(\Theta(\sqrt n)\) 或精确次多项式因子。候选声称 \(\Theta(n^{2/3})\) 的下界确如人工评审所指出，未被证明且现在也与更强上界不相容。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `medium`
- 尝试路线：先自足重建平方根下界，再检查候选二维构造。固定 \(b_0\in A\)，对每个 \(a\in A\) 记 \(x=a/(a,b_0)\)、\(y=b_0/(a,b_0)\)。则 \(x,y\in Q(A)\)，且 \(a/b_0=x/y\)，所以 \(a\mapsto(x,y)\) 单射。上界方面，二维带状集合 \(A_{t,s}=\{2^i3^j:t\le i+j\le t+s\}\) 可直接计数。
- 局部结论：由上述单射，\(n\le|Q(A)|^2\)，故 \(h(n)\ge\sqrt n\)。；二维带状构造满足 \(|A_{t,s}|=(s+1)(2t+s+2)/2\)，而 \(|Q(A_{t,s})|=(s+1)(s+2)/2+2t\)；取 \(t\asymp s^2\) 得旧上界 \(h(n)\ll n^{2/3}\)。；新近高维构造把上界改进到 \(\sqrt n\,e^{O(\sqrt{\log n})}\)，故指数极限若按 \(\log h(n)/\log n\) 衡量已经等于 \(1/2\)。
- 第一阻塞点：自足复现新上界时，第一处尚未闭合的是构造高维指数向量集，使其正部差集同时只有 \(\sqrt n\,e^{O(\sqrt{\log n})}\) 个元素；二维带状体只能给 \(n^{2/3}\)，不能靠同一参数平衡达到平方根。
- 下一步：逐引理审计 ProofCouncil 的高维正部差集构造，重点检查维数选择、边界计数，以及由 \(\mathbb Z_{\ge 0}^d\) 指数向量嵌入互异整数时是否完整保持 \(Q(A)\)。
- 来源核对：[Erdős Problem 539](https://www.erdosproblems.com/539) 记录经典界及 2026 年的新上界。；经典二维几何转化可与 [Granville–Roesler](https://doi.org/10.2307/2589556) 对照。；新证明材料位于 [ProofCouncil 仓库](https://github.com/eth-sri/proof-council/blob/main/ProofCouncil.pdf)；目前属于公开证明材料而非已确认的期刊同行评审结果。；本地 Lean 文件仍把 \(n^{2/3}\) 上界列作旧变体，尚未纳入 2026 年改进；且其有限集允许 \(0\)，与原题 \(A\subseteq\mathbb N\) 的正整数惯例有轻微对象差异。
- 时间记账：所在批次墙钟时间按题数均摊约 68.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/539)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/539.lean`；既有候选答案（按不可信材料审计）

### #543

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Define $f(N)$ be the minimal $k$ such that the following holds: if $G$ is an abelian group of size $N$ and $A\subseteq G$ is a random set of size $k$ then, with probability $\geq 1/2$, all elements of $G$ can be written as $\sum_{x\in S}x$ for some $S\subseteq A$. Is\[f(N) \leq \log_2 N+o(\log\log N)?\]
- 题意摘要：对每个整数 N，f(N) 是最小整数 k，使得对每个阶为 N 的有限阿贝尔群 G，从其所有 k 元子集中均匀随机选 A 时，以至少 1/2 的概率有 Σ(A):={∑_{x∈S}x:S⊆A}=G。问题问是否对所有 N→∞ 有 f(N)≤log₂N+o(log log N)。
- 状态核对：已被否定。先前候选称其仍开放，已过时。Ma–Tang 证明沿素数 p 有 f(p)≥log₂p+(1/(2log2)+o(1))log log p，足以否定所问的统一 o(log log N) 上界。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建素数阶反例路线：取 G=(F_p,+)，令 k=⌊log₂p+c log log p⌋，其中 0<c<1/(2log2)。研究随机 k 元集 A 的未覆盖剩余类数 X=|F_p\Σ(A)|；通过缺失事件的二阶矩估计证明 P(X>0)→1，因而这种 k 尚不足以达到成功概率 1/2。
- 局部结论：纯计数给出必要条件 2^k≥p，所以 f(p)≥⌈log₂p⌉。；已知定理给出：对每个固定 c<1/(2log2)，上述 k 满足 P(Σ(A)=F_p)→0。故充分大的素数 p 上 f(p)>k。；令 c趋近1/(2log2)，得到 f(p)≥log₂p+(1/(2log2)+o(1))log log p；因此原命题为假。
- 第一阻塞点：在受限重建中，第一处不能从简单计数严格闭合的是二阶矩所需的相关性估计：不同剩余类“未被子集和覆盖”的事件高度相关，必须控制重叠子集和关系；这正是论文的主要技术部分，不能用独立优惠券模型代替。
- 下一步：逐项核验论文中 E[X]、E[X²] 的估计及从固定大小随机子集模型到结论 P(X>0)→1 的转换，特别检查常数 1/(2log2)。
- 来源核对：[Ma–Tang 预印本摘要与主定理](https://arxiv.org/abs/2602.05768)明确给出素数阶下界。；[Erdős Problems #543](https://www.erdosproblems.com/543)现标为 DISPROVED，并记录该反例路线。
- 时间记账：所在批次墙钟时间按题数均摊约 43.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/543)；既有候选答案（按不可信材料审计）

### #544

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Show that\[R(3,k+1)-R(3,k)\to\infty\]as $k\to \infty$. Similarly, prove or disprove that\[R(3,k+1)-R(3,k)=o(k).\]
- 题意摘要：记 Δ_k=R(3,k+1)−R(3,k)，其中 R(3,k) 是迫使红色 K₃ 或蓝色 K_k 的最小完全图阶数。两个独立问题是：(i) 是否对每个 M，充分大 k 均有 Δ_k>M；(ii) 是否 Δ_k/k→0。
- 状态核对：截至核查仍开放。先前候选关于“无界”和 liminf Δ_k/k=0 的局部结论正确，但不能升级成两个所求极限。2026 年的新相邻比值界只给 Δ_k≪k^{-c}R(3,k)，仍不足以推出 Δ_k=o(k)。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用望远镜求和，把已知 R(3,k)≍k²/log k 转化为对增量的平均约束；尝试由区间平均控制逐点增量。
- 局部结论：若 Δ_k 最终有界，则 R(3,n)=R(3,K)+∑_{k=K}^{n-1}Δ_k=O(n)，与 R(3,n)≫n²/log n 矛盾；故 limsup Δ_k=∞。；取足够大的固定 t>1，由两侧渐近界可使 R(3,⌊tk⌋)−R(3,k)≫k²/log k；故区间 [k,tk] 中某个 j 满足 Δ_j≫k/log k。；若存在 ε>0 使所有充分大 k 都有 Δ_k≥εk，则求和得到 R(3,n)≫n²，与 R(3,n)≪n²/log n 矛盾；所以 liminf Δ_k/k=0。
- 第一阻塞点：望远镜求和只控制区间平均，不能排除无限多个很小的 Δ_k 与很大尖峰交替出现，也不能排除稀疏的线性级尖峰；缺少把邻近 k 的 Ramsey 极值结构联系起来的逐点稳定性定理。
- 下一步：检验能否从临界无三角图的顶点删除/扩张操作推出相邻增量的局部正则性，例如对 Δ_{k+1}/Δ_k 或 Δ_k−Δ_{k+1} 建立统一界；任何此类界与上述平均估计结合都可直接测试两个极限。
- 来源核对：[Erdős Problems #544](https://www.erdosproblems.com/544)仍标为 OPEN，并记录 R(3,k)≍k²/log k。；[Erdős Problems #1014](https://www.erdosproblems.com/1014)记录 R(3,k+1)≤(1+O(k^{-c/9}))R(3,k)；该指数不足以自动给出 o(k)。；[Erdős Problems #165](https://www.erdosproblems.com/165)核对了当前两侧渐近界。
- 时间记账：所在批次墙钟时间按题数均摊约 43.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/544)；既有候选答案（按不可信材料审计）

### #545

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph with $m$ edges and no isolated vertices. Is the Ramsey number $R(G)$ maximised when $G$ is 'as complete as possible'? That is, if $m=\binom{n}{2}+t$ edges with $0\leq t<n$ then is\[R(G)\leq R(H),\]where $H$ is the graph formed by connecting a new vertex to $t$ of the vertices of $K_n$?
- 题意摘要：给定边数 m，唯一写成 m=binom(n,2)+t、0≤t<n。令 H 由 K_n 加一个新顶点并把它连接到其中 t 个顶点得到。字面命题量化所有无孤立点且恰有 m 条边的有限图 G，问是否总有对角 Ramsey 数 R(G)≤R(H)。
- 状态核对：字面命题已有小 m 反例；网站保留 OPEN，是因为通常关注排除这些有限例外后的大 m/渐近版本。先前候选给出的 m=3 匹配反例可以严格核对，但它没有解决“充分大 m 是否成立”的残余问题。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：直接测试最小的完全图边数 m=3。此时 n=3、t=0，去掉新增孤立点后 H=K₃；选择无孤立点图 G=3K₂，并比较两个已知且可直接验证的 Ramsey 数。
- 局部结论：R(H)=R(K₃)=6。；二色匹配公式 R(rK₂,rK₂)=3r−1 给出 R(3K₂)=8。其下界可由 K_5∪K_3 型着色构造得到；上界是二色匹配定理的 r=3 情形。；因此 R(G)=8>6=R(H)，字面上的全称命题为假。
- 第一阻塞点：该反例只处理 m=3。若把问题修正为“是否对所有充分大 m 成立”，第一处障碍是没有机制把任意 m 边图压缩成准团而保证 Ramsey 数不下降；Ramsey 数对移边/压缩并无已知单调性。
- 下一步：明确冻结 cohort 采用字面版本还是“除有限例外的大 m 版本”；对后者，下一项可检验任务是研究标准 colex 压缩的一步操作是否保持或增大 R(G)，并先在小图数据库中系统寻找反例。
- 来源核对：[Erdős Problems #545](https://www.erdosproblems.com/545)明确记录 m=2 至 5、7 至 9 有反例，同时把一般版本保留为 OPEN。；匹配公式与 R(K₃)=6 均为经典精确结果；先前候选的 m=3 数值与官方所列小例外一致。
- 时间记账：所在批次墙钟时间按题数均摊约 43.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/545)；既有候选答案（按不可信材料审计）

### #550

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $m_1\leq\cdots\leq m_k$ and $n$ be sufficiently large. If $T$ is a tree on $n$ vertices and $G$ is the complete multipartite graph with vertex class sizes $m_1,\ldots,m_k$ then prove that\[R(T,G)\leq (\chi(G)-1)(R(T,K_{m_1,m_2})-1)+m_1.\]
- 题意摘要：固定 k≥2 及 1≤m₁≤⋯≤m_k。需存在仅依赖这些固定参数的 n₀，使每个 n≥n₀、每棵 n 顶点树 T 都满足 R(T,K_{m₁,…,m_k})≤(k−1)(R(T,K_{m₁,m₂})−1)+m₁；这里 χ(G)=k。
- 状态核对：冻结输入标为 open，但 2026-06-24 的新预印本声称精确证明该结论。先前候选的“直接套 CRST 得到所有大树的 Burr 等式”是错误的，人工评审意见必须保留：该等式不对任意树成立，故其三步论证无效。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `medium`
- 尝试路线：按新预印本重建反证框架。设 r=R(T,K_{m₁,m₂})、N=(k−1)(r−1)+m₁，并假设有 N 顶点红蓝染色既无红 K_{m₁,…,m_k} 又无蓝 T。先用 r=n+o(n) 与新的 off-Turán 树嵌入定理推出红图密度接近 (k−1)-部 Turán 极值；再用稳定性分解成 k−1 个大 reservoir，最后以有界秩 blocker 超图的紧致性与取整，把例外顶点分配到 reservoirs，迫使红色多部图或蓝树。
- 局部结论：k=2 时右端为 R(T,K_{m₁,m₂})−1+m₁≥R(T,K_{m₁,m₂})，结论立即成立。；在假想反例序列中，已知统一渐近 r=n+o(n)，故 N=(k−1+o(1))n；这是应用 Turán 稳定性的正确尺度。；新论文的 off-Turán 嵌入结论推出：若蓝图无 T 且红图无目标多部图，则红边数至少 t_{k−1}(N)−o(N²)，从而红图具有近 (k−1)-部结构。
- 第一阻塞点：受限重建首先卡在新的 off-Turán 树嵌入定理及其“对所有 n 顶点树一致”的误差控制；其后还需验证 blocker 超图紧致性取整。它们均是新论文的核心定理，不能由 Chvátal或 CRST 一行替代。
- 下一步：对预印本做定理依赖审计：先独立检查 r=n+o(n) 的统一性，再核对 off-Turán 定理是否对任意树一致，最后检查紧致性取整是否保留 m₁ 个例外顶点的精确常数。
- 来源核对：[Li 预印本：A Resolution of Erdős Problem 550](https://arxiv.org/abs/2606.23659)的 Theorem 1.1 与题目量词完全一致。；[Erdős Problems #550](https://www.erdosproblems.com/550)抓取页面仍标 OPEN，显然尚未吸收 2026-06-24 的预印本；因此此处称“预印本声称解决”，不冒充已同行评审定理。；人工评审指出的 CRST 误用已明确排除。
- 时间记账：所在批次墙钟时间按题数均摊约 43.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/550)；既有候选答案（按不可信材料审计）

### #552

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Determine the Ramsey number\[R(C_4,S_n),\]where $S_n=K_{1,n}$ is the star on $n+1$ vertices. In particular, is it true that, for any $c>0$, there are infinitely many $n$ such that\[R(C_4,S_n)\leq n+\sqrt{n}-c?\]
- 题意摘要：f(n)=R(C₄,K_{1,n}) 是最小 N，使每个 K_N 的红蓝边染色都含红 C₄ 或蓝 K_{1,n}。第二问的量词是：对每个固定实数 c>0，是否存在无穷多个整数 n 满足 f(n)≤n+√n−c。
- 状态核对：仍开放。已知 n+√n−6n^{11/40}≤f(n)≤n+⌈√n⌉+1；已知精确族均为 n+⌈√n⌉ 或再加 1，不能回答第二问。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：转成 C₄-free 最小度问题并做二步路径计数。若 N=n+s 的染色没有蓝 K_{1,n}，则红图 F 满足 δ(F)≥s。若 F 又无 C₄，则每对顶点至多有一个共同邻点，因此 ∑_v binom(d(v),2)≤binom(N,2)。
- 局部结论：由凸性，N·binom(s,2)≤∑_v binom(d(v),2)≤binom(N,2)，故 s(s−1)≤N−1=n+s−1。于是 s≤1+√n，恢复 f(n)≤n+√n+O(1) 的正确主尺度。；取 s=⌈√n⌉+1。若 n 非平方，则 s(s−1)>n+s−1，立即矛盾，因此得到相应 Parsons 型上界。；若 n=q² 且计数取等，则红图必须为 (q+1)-正则且每对不同顶点恰有一个共同邻点，故邻接矩阵满足 A²=qI+J；谱与 trace(A)=0 对 q>1 造成严格算术限制，说明平方情形必须另行分析而非忽略等号。
- 第一阻塞点：目标要求在 s≈√n−c 时也排除 C₄-free 最小度图，但此时二步路径不等式有 Θ(c√n) 的余量，完全不矛盾。需要远强于平均二步路径计数的结构或谱稳定性结论。
- 下一步：固定 c，令 s=⌊√n−c⌋，研究接近等号的 C₄-free 图是否必接近有限几何的极性图；把二步路径计数的亏损精确写成度方差与“无共同邻点”的顶点对数，再测试能否从整除、谱或设计参数推出无穷多个 n 不可实现。
- 来源核对：[Erdős Problems #552](https://www.erdosproblems.com/552)核对了开放状态、一般上下界及 Parsons 的两个素数幂精确族。；先前候选的最小度等价形式基本正确，但这里补正了精确阈值：无蓝 K_{1,n} 等价于红图 δ≥N−n。
- 时间记账：所在批次墙钟时间按题数均摊约 43.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/552)；既有候选答案（按不可信材料审计）

### #554

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(G;k)$ denote the minimal $m$ such that if the edges of $K_m$ are $k$-coloured then there is a monochromatic copy of $G$. Show that\[\lim_{k\to \infty}\frac{R(C_{2n+1};k)}{R(K_3;k)}=0\]for any $n\geq 2$.
- 题意摘要：固定整数 n≥2。这里 R(G;k) 严格指 k 种颜色的对角多色 Ramsey 数；目标是证明当 k→∞ 时，R(C_{2n+1};k)/R(K_3;k)→0。
- 状态核对：仍为开放题，且 n=2（C5）即未解决。旧候选把 R(G;k) 攅读成二色非对角数 r(G,K_k)，改变了题目量词和对象，其后 Kim–Sudakov 比值计算与本题无关。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：设一个 k-着色不含单色 C_{2n+1}。固定顶点 v，并令 V_i={x:c(vx)=i}。研究颜色 i 在 V_i 内形成的图，尝试由“单色三角形很少”归约到无单色三角形着色。
- 局部结论：颜色 i 在 V_i 内不含长度 2n−1 的路径；否则将该路径两端通过 v 闭合，得到颜色 i 的 C_{2n+1}。；由 Erdős–Gallai 路径界，e_i(V_i)≤(n−1)|V_i|。因此经过 v 的单色三角形至多 (n−1)(m−1)。；对所有 v 求和可得：任一无单色 C_{2n+1} 的 k-着色中，单色三角形总数至多 n−1 倍量级的 m²，具体为至多 m(n−1)(m−1)/3。
- 第一阻塞点：第一处缺口是把“只有 O_n(m²) 个单色三角形”统一转化为一个规模显著增大的无单色三角形 k-着色。逐颜色使用三角形移除引理会累积依赖于 k 的删除量；即便只删 o(m²) 条边，也不能直接取得足够大的完全子图。这正是比值结论所需的定量桥梁。
- 下一步：检验一个彩色三角形移除命题：若 k-着色 K_m 仅有 O_n(m²) 个单色三角形，能否通过删除或重着色 o(m²/k) 级别的边/每色，得到无单色三角形的近完全着色；先在 k=O(log m) 的参数区间估计现有移除界是否足够。
- 来源核对：题面多色定义与开放状态按 [Erdős Problems #554](https://www.erdosproblems.com/554) 核对；未采用旧候选的二色改写。；路径计数步骤使用的 Erdős–Gallai 形式为：无长度 ℓ 路径的 N 顶点图至多 (ℓ−1)N/2 条边；该表述亦见[相关论文摘要](https://arxiv.org/abs/2504.01501)。
- 时间记账：所在批次墙钟时间按题数均摊约 46.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/554)；既有候选答案（按不可信材料审计）

### #555

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(G;k)$ denote the minimal $m$ such that if the edges of $K_m$ are $k$-coloured then there is a monochromatic copy of $G$. Determine the value of\[R(C_{2n};k).\]
- 题意摘要：对每个 n≥2、k≥1，确定使每个 K_m 的 k-边着色都含单色 C_{2n} 的最小 m；主要未知参数区间是固定 n、k 增长时的精确值或阶。
- 状态核对：开放。旧候选主要讨论固定 k、n→∞ 的二色及三色结果，没有处理官方界所针对的固定 n、k→∞ 问题，因而不是本题的证明尝试。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：从偶圈极值数出发证明通用上界：在 K_m 的 k-着色中取边数最多的颜色，再用 ex(m,C_{2n})=O_n(m^{1+1/n}) 强迫偶圈；下界方面先检查朴素随机着色能达到什么程度。
- 局部结论：某颜色至少含 binom(m,2)/k 条边。若 binom(m,2)/k>ex(m,C_{2n})，该颜色必含 C_{2n}。；代入 ex(m,C_{2n})≤c_n m^{1+1/n}，严格得到 R(C_{2n};k)=O_n(k^{n/(n−1)})，即题面上界 k^{1+1/(n−1)}。；独立均匀随机着色下，单色 C_{2n} 的期望至多 O(m^{2n}k^{1−2n})；该方法只在 m≪k^{1−1/(2n)} 时有效，甚至弱于已知的超线性下界，明确显示朴素一阶矩不足。
- 第一阻塞点：第一处无法闭合的是下界构造：独立随机着色不能产生 k^{1+1/(2n)} 规模；需要颜色类同时具有高边密度且避免 C_{2n} 的相关设计或图分解，而极值图的简单随机平移不能保证覆盖 K_m 的每条边恰好一次。
- 下一步：选定 n=2，显式核查有限几何给出的 K_m 边分解为何达到 m≈k²，并尝试识别可推广到 C_{2n} 的必要交数条件；这是可计算验证的首个模型。
- 来源核对：[Erdős Problems #555](https://www.erdosproblems.com/555) 仍列为开放，并记录 k^{1+1/(2n)}≪R_k(C_{2n})≪k^{1+1/(n−1)}。；同一条目核实 C4 的特殊界：当 k−1 为素数幂时 R_k(C4)>k²−k+1，且总有 R_k(C4)≤k²+k+1。
- 时间记账：所在批次墙钟时间按题数均摊约 46.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/555)；既有候选答案（按不可信材料审计）

### #557

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(G;k)$ denote the minimal $m$ such that if the edges of $K_m$ are $k$-coloured then there is a monochromatic copy of $G$. Is it true that\[R(T;k)\leq kn+O(1)\]for any tree $T$ on $n$ vertices?
- 题意摘要：自然量词解释为：对每个固定颜色数 k，是否存在仅依赖 k 的常数 C_k，使每棵 n 顶点树 T 都满足 R(T;k)≤kn+C_k。若 O(1) 要求绝对地独立于 k，则是更强命题，题面未明确支持该解释。
- 状态核对：开放，并由 Erdős–Sós 极值猜想蕴含。旧候选的条件归约方向正确，但不能把未完整核定的 Erdős–Sós 状态当成已知定理。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：取最大颜色类，将 Ramsey 问题归约为树的极值边数。先用最小度嵌入恢复系数 2，再精确定位把系数降到 1 所需的命题。
- 局部结论：任意平均度 d 的图含一个最小度至少 d/2 的非空子图；最小度至少 n−1 的图可逐叶贪心嵌入任意 n 顶点树。因此 m>2k(n−1)+1 足以强迫单色 T。；若 m−1>k(n−2)，最大颜色类有超过 (n−2)m/2 条边。；所以只要成立极值断言 ex(m,T)≤(n−2)m/2（Erdős–Sós 形式），立即得到 R(T;k)≤k(n−2)+2，强于所求 kn+O_k(1)。
- 第一阻塞点：第一处缺口恰是对所有树 T 和所有相关 m 证明 ex(m,T)≤(n−2)m/2。仅靠平均度到最小度的删点论证会损失因子 2；平均度略大于 n−2 并不保证存在最小度 n−1 的子图。
- 下一步：把路线限制到一个可检验树族（例如直径至多 4 的树），直接证明所需极值界；同时明确常数是否允许依赖 k，避免量词歧义。
- 来源核对：[Erdős Problems #557](https://www.erdosproblems.com/557) 核实该题仍开放、由 #548 蕴含，并记录星图给出的 kn−O(k) 障碍。；旧候选声称的一般 2kn 上界可由上述最小度删点与贪心嵌入独立重建，无需把引用当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 46.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/557)；既有候选答案（按不可信材料审计）

### #558

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R(G;k)$ denote the minimal $m$ such that if the edges of $K_m$ are $k$-coloured then there is a monochromatic copy of $G$. Determine\[R(K_{s,t};k)\]where $K_{s,t}$ is the complete bipartite graph with $s$ vertices in one component and $t$ in the other.
- 题意摘要：给定正整数 s,t,k，确定 k 色对角 Ramsey 数 R(K_{s,t};k)。因 K_{s,t}≅K_{t,s}，可约定 2≤s≤t；s=1 是星图的独立特殊情形。
- 状态核对：一般情形开放。旧候选罗列了若干结果，但没有从定义证明任何界；其“不平衡参数”叙述还容易因交换 s,t 而混淆，故这里只采用题面明确给出的范围。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：上界采用 Kővári–Sós–Turán 双计数：最大颜色类若超过 ex(N,K_{s,t}) 就结束。下界采用独立均匀 k-着色并对所有 K_{s,t} 做一阶矩。
- 局部结论：固定一份 K_{s,t} 单色的概率为 k^{1−st}；候选副本数至多 N^{s+t}/(s!t!)。故当 N^{s+t}k^{1−st}<s!t! 时，存在无单色 K_{s,t} 的着色，得到 R(K_{s,t};k)=Ω_{s,t}(k^{(st−1)/(s+t)})。；KST 界 ex(N,K_{s,t})≤(t−1)^{1/s}N^{2−1/s}+O_s(N)。最大颜色类至少有 binom(N,2)/k 条边。；比较两式得到 R(K_{s,t};k)=O_{s,t}(k^s)；保留低阶项可恢复题面所列 (t−1)(k+k^{1/s})^s 型上界。
- 第一阻塞点：两条严格路线给出的指数分别为 (st−1)/(s+t) 与 s，通常存在真实缺口。一阶矩忽略不同副本的高度相关性，而 KST 只控制单个颜色类；当前步骤没有能把 k 个接近极值的 K_{s,t}-free 图同时拼成 K_N 边分解的结构信息。
- 下一步：先固定 (s,t)=(2,3)，用有限域或循环差集搜索 k 个 K_{2,3}-free 图的边覆盖，比较所得 N 与 k²；该实验能直接检验“指数等于较小侧 s”的构造路线。
- 来源核对：题面的一阶矩下界、KST 型上界及特殊情形来自 [Erdős Problems #558](https://www.erdosproblems.com/558)。；未复述旧候选未经本轮核查的星图奇偶精确公式；它不影响 s,t≥2 的本路线。
- 时间记账：所在批次墙钟时间按题数均摊约 46.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/558)；既有候选答案（按不可信材料审计）

### #560

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\hat{R}(G)$ denote the size Ramsey number, the minimal number of edges $m$ such that there is a graph $H$ with $m$ edges such that in any $2$-colouring of the edges of $H$ there is a monochromatic copy of $G$. Determine\[\hat{R}(K_{n,n}),\]where $K_{n,n}$ is the complete bipartite graph with $n$ vertices in each component.
- 题意摘要：对每个 n，求所有满足 H→(K_{n,n})_2 的图 H 中最小边数；这里宿主 H 任意，不要求完全图或二部图。目标至少包括确定其关于 n 的渐近阶。
- 状态核对：开放；已知上下界相差一个 n 因子。旧候选仅转述这些界，没有重建下界着色机制。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：对任意有 m 条边的宿主 H 独立红蓝着色。通过给每份 K_{n,n} 选择一个完美匹配，直接上界 H 中 K_{n,n} 的副本数，再用一阶矩排除单色副本。
- 局部结论：每份 K_{n,n} 含 n! 个完美匹配；给定 H 中一个 n 边匹配，其端点至多有 2^{n−1} 种二部定向可能形成 K_{n,n}。故副本数至多 2^{n−1}binom(m,n)/n!。；固定副本单色的概率为 2^{1−n²}。因此单色副本期望至多 [e²m·2^{1−n}/n²]^n。；若 m<e^{−2}n²2^{n−1}，上述期望小于 1，故存在避免单色 K_{n,n} 的着色；这独立重建了 \hat R(K_{n,n})=Ω(n²2^n) 的正确量级下界。
- 第一阻塞点：该均匀独立着色的阈值天然停在 n²2^n：副本计数的 n!² 正好贡献 n^{2n}。要达到猜测的 n³2^n 下界，必须利用宿主顶点度的不均匀性并采用依度数着色或局部引理；当前一阶矩没有额外的 n 因子来源。
- 下一步：按顶点度将 H 分层，并测试概率 p_{uv}=f(d(u),d(v)) 的非均匀红蓝着色；目标是分别界定红、蓝 K_{n,n} 的期望并确定何种 f 能多取得一个 n 因子。
- 来源核对：[Erdős Problems #560](https://www.erdosproblems.com/560) 核实已知 (1/60)n²2^n<\hat R(K_{n,n})<(3/2)n³2^n 及开放状态。；[Conlon–Fox–Wigderson 原论文](https://arxiv.org/abs/2111.05420) 核实其在 t=Ω(s log s) 时确定 \hat R(K_{s,t}) 的常数阶；这不覆盖对角 t=s。；论文正文说明其改进下界使用依赖端点度数的随机着色，与本路线的下一步一致。
- 时间记账：所在批次墙钟时间按题数均摊约 46.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/560)；既有候选答案（按不可信材料审计）

### #561

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\hat{R}(G)$ denote the size Ramsey number, the minimal number of edges $m$ such that there is a graph $H$ with $m$ edges such that in any $2$-colouring of the edges of $H$ there is a monochromatic copy of $G$. Let $F_1$ and $F_2$ be the union of stars. More precisely, let $F_1=\cup_{i\leq s} K_{1,n_i}$ and $F_2=\cup_{j\leq t} K_{1,m_j}$. Prove that\[\hat{R}(F_1,F_2) = \sum_{2\leq k\leq s+2}\max\{n_i+m_j-1 : i+j=k\}.\]
- 题意摘要：按官方题面，应先将星的大小降序排列：$F_1=\bigsqcup_{i=1}^sK_{1,n_i}$、$F_2=\bigsqcup_{j=1}^tK_{1,m_j}$。非对称边数 Ramsey 数 $\hat R(F_1,F_2)$ 是使某图每次红蓝边染色均含红色 $F_1$ 或蓝色 $F_2$ 所需的最少边数。目标公式应为 $\sum_{k=2}^{s+t}l_k$，其中 $l_k=\max_{i+j=k}(n_i+m_j-1)$；输入中的上限 $s+2$ 是转录错误，一般情形甚至会出现空集最大值。
- 状态核对：官方条目截至2026年仍标为开放，并列出若干特殊情形。先前候选正确发现了上限错误，但其推进算法应在 $i=s$ 或 $j=t$ 时立即停止，否则 $n_{i+1}$ 或 $m_{j+1}$ 未定义。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：验证容易方向。取 $H=\bigsqcup_{k=2}^{s+t}K_{1,l_k}$。处理第 $k$ 个星时，若此前已取得 $a$ 个红星、$b$ 个蓝星且尚未完成目标，则 $a+b=k-2$、$a<s$、$b<t$。因为 $l_k\ge n_{a+1}+m_{b+1}-1$，该星的红度至少 $n_{a+1}$，或蓝度至少 $m_{b+1}$，于是相应增加 $a$ 或 $b$。
- 局部结论：上述过程每步使用不同的连通分支，故所得各星顶点互不相交，确实组成星森林。；经过 $s+t-1$ 步后，若此前未停止，则 $a+b=s+t-1$ 且 $a\le s,b\le t$，所以必有 $a=s$ 或 $b=t$。因此严格得到 $\hat R(F_1,F_2)\le\sum_{k=2}^{s+t}l_k$。；该证明只使用各条对角线的最大值，不要求同一对 $(i,j)$ 同时实现多个 $l_k$。
- 第一阻塞点：反向不等式要求：对任意边数少于 $\sum l_k$ 的图构造一种染色，同时避免红 $F_1$ 和蓝 $F_2$。上述证明严重依赖见证图本身是互不相交的星；对含环、共享高阶顶点或稠密小块的一般图，没有合法方式把边逐块分配给一条对角线。这是该路线第一处无法闭合之处。
- 下一步：先检验一个可控归纳命题：对任意极小箭头图 $H\to(F_1,F_2)$，能否删除或拆分一个低度顶点，将剩余问题归约到 $(F_1-K_{1,n_s},F_2)$ 或 $(F_1,F_2-K_{1,m_t})$，并使损失至少对应某个 $l_k$；首先在 $s=t=2$ 的全部小参数上枚举极小图，检查该结构命题是否已有反例。
- 来源核对：[官方题面](https://www.erdosproblems.com/561)明确给出上限 $s+t$，并仍标为开放。；官方条目记录：同型星、若干奇偶参数及 $s=1$ 等特殊情形已经解决，不能把一般上界误报为完整证明。
- 时间记账：所在批次墙钟时间按题数均摊约 83.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/561)；既有候选答案（按不可信材料审计）

### #562

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R_r(n)$ denote the $r$-uniform hypergraph Ramsey number: the minimal $m$ such that if we $2$-colour all edges of the complete $r$-uniform hypergraph on $m$ vertices then there must be some monochromatic copy of the complete $r$-uniform hypergraph on $n$ vertices. Prove that, for $r\geq 3$,\[\log_{r-1} R_r(n) \asymp_r n,\]where $\log_{r-1}$ denotes the $(r-1)$-fold iterated logarithm. That is, does $R_r(n)$ grow like\[2^{2^{\cdots n}}\]where the tower of exponentials has height $r-1$?
- 题意摘要：固定整数 $r\ge3$，$R_r(n)$ 是每个二染色的完全 $r$-一致超图都含单色 $K_n^{(r)}$ 的最小顶点数。所求量词是：存在仅依赖 $r$ 的常数 $0<c_r<C_r$，使充分大 $n$ 满足 $c_rn\le\log^{(r-1)}R_r(n)\le C_rn$。
- 状态核对：截至2026年官方条目仍为开放；$r=3$ 的下界正是题564。先前候选对已知界的总体判断正确，但其 Erdős–Rado 蓄水池论证不能写成“忽略 $-1$”：须保留取整，利用 $\lceil(2^A-1)/2^B\rceil=2^{A-B}$ 才严格。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：上界沿 Erdős–Rado 递推：令 $M=R_{r-1}(n-1)$，逐次选顶点并按至多 $2^{\binom{i}{r-2}}$ 种颜色模式缩小蓄水池；保留天花板取整可得到 $R_r(n)\le2^{\binom{M}{r-1}}+O_r(1)$。下界则从随机三元组染色出发，再尝试经典 stepping-up。
- 局部结论：由递推和 $R_2(n)\le4^n$，对固定 $r$ 可严格推出 $\log^{(r-1)}R_r(n)=O_r(n)$。；随机二染色给出 $R_3(n)>2^{c n^2}$：单色 $n$-集的期望至多 $2\binom Nn2^{-\binom n3}$，取 $N=2^{cn^2}$、$c<1/6$ 即趋于零。；从三一致情形向上使用二色 stepping-up，每升一次一致度增加一层指数，得到一般下界为高度 $r-2$ 的塔；因而目前只推出 $\log^{(r-1)}R_r(n)=\Omega_r(\log n)$。
- 第一阻塞点：缺失的是二色的“图到三元组”有效升阶。二进制差值构造只在差值序列单调时直接继承图染色；出现局部极值时，二种颜色不足以同时控制所有可能的单色大集合。四色情形可编码这些额外类型，但这不能合并为二色而保持所需禁单色性质。
- 下一步：把候选的差值构造形式化为有限模式问题：枚举长度至8的差值序列，分类首个局部极值，检验任何仅依赖相邻差值及极值类型的二色规则是否必产生大型单色模式；这可否定一整类朴素 stepping-up 方案，或找到可继续验证的新规则。
- 来源核对：[官方题目562](https://www.erdosproblems.com/562)截至2026年仍标为开放，并明确把题564列为特例。；本地 Lean 陈述把结论写成渐近等价 `~`，这比题面的 $\asymp_r$（双边常数界）更强，不能作为忠实形式化版本。
- 时间记账：所在批次墙钟时间按题数均摊约 83.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/562)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/562.lean`；既有候选答案（按不可信材料审计）

### #563

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(n,\alpha)$ denote the largest $m$ such that there exists a $2$-colouring of the edges of $K_n$ so that every $X\subseteq [n]$ with $\lvert X\rvert\geq m$ contains more than $\alpha \binom{\lvert X\rvert}{2}$ many edges of each colour. Prove that, for every $0\leq \alpha\leq 1/2$,\[F(n,\alpha)\sim c_\alpha\log n\]for some constant $c_\alpha$ depending only on $\alpha$.
- 题意摘要：输入按字面定义 $F(n,\alpha)$ 为满足性质的“最大”阈值 $m$，并包含端点 $\alpha=1/2$。官方题面实际是“最小”阈值，并只量化 $0\le\alpha<1/2$。
- 状态核对：输入版本不是开放问题的正确陈述。先前候选准确指出了“最大/最小”错误，但还应明确吸收第二个错误：$\alpha=1/2$ 必须排除。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：先按输入字面寻找反例，再重建预期问题。若 $\alpha<1/2$ 固定，充分大 $n$ 时可把 $K_n$ 的总边数近乎等分染色；取 $m=n$ 后只需检查 $X=[n]$，两色边数均严格大于 $\alpha\binom n2$。对修正后的最小阈值，检查大小恰为 $m$ 的集合即可，并对随机染色使用二项大偏差与并合界。
- 局部结论：字面定义下性质随 $m$ 增大而变弱，所以一旦存在任何可行阈值，最大值就是 $n$；因此固定 $\alpha<1/2$ 时充分大 $n$ 有 $F(n,\alpha)=n$，否定 $F\sim c_\alpha\log n$。；当 $\alpha=1/2$ 时，对 $X=[n]$ 两色边数之和为 $\binom n2$，不可能二者都严格大于一半；故不存在可行 $m\le n$。；对修正版，若某个较大集合是坏集，则随机取其 $m$-子集并平均可得一个坏的 $m$-集。因此并合界给出 $F(n,\alpha)\le(2/D(\alpha\|1/2)+o(1))\ln n$；普通 Ramsey 上界则给出 $F(n,\alpha)=\Omega(\log n)$。
- 第一阻塞点：对修正版，概率法只给某个显式上界常数，Ramsey 论证给较小的下界常数；没有已知的次可加或乘法结构能迫使 $F(n,\alpha)/\log n$ 收敛。特别是 $\alpha=0$ 已包含对角 Ramsey 数指数增长率的困难。
- 下一步：研究修正版的近乘法不等式：给定 $n_1,n_2$ 上的好染色，对词典积染色逐类计算任意顶点集的两色密度，检验能否证明 $F(n_1n_2,\alpha)\le F(n_1,\alpha)+F(n_2,\alpha)+O_\alpha(1)$；若成立，Fekete 型论证可能给出极限。
- 来源核对：[官方题目563](https://www.erdosproblems.com/563)使用“smallest”并限定 $0\le\alpha<1/2$，确认输入有两处转录错误。；官方条目只声称容易得到 $\asymp_\alpha\log n$，完整渐近常数仍标为开放。
- 时间记账：所在批次墙钟时间按题数均摊约 83.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/563)；既有候选答案（按不可信材料审计）

### #564

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $R_3(n)$ be the minimal $m$ such that if the edges of the $3$-uniform hypergraph on $m$ vertices are $2$-coloured then there is a monochromatic copy of the complete $3$-uniform hypergraph on $n$ vertices. Is there some constant $c>0$ such that\[R_3(n) \geq 2^{2^{cn}}?\]
- 题意摘要：问是否存在绝对常数 $c>0$，使所有充分大的 $n$ 都满足二色三一致对角 Ramsey 数 $R_3(n)\ge2^{2^{cn}}$。本地形式化也采用“最终对所有 $n$”这一量词。
- 状态核对：截至2026年仍开放，不能把四色情形的双指数下界转用于二色情形。先前候选的状态判断正确。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先对独立随机二染色作第一矩估计。令 $N=\lfloor2^{c n^2}\rfloor$；单色 $K_n^{(3)}$ 的期望不超过 $2\binom Nn2^{-\binom n3}$。再测试是否可直接把 $N$ 提升到双指数规模。
- 局部结论：取二进制对数，期望的上界为 $1+n\log_2(eN/n)-\binom n3$；若 $c<1/6$，则对充分大 $n$ 为负，严格得到 $R_3(n)>2^{c n^2}$。；若改取 $N=2^{2^{cn}}$，正项 $n\log_2N=n2^{cn}$ 远大于负项 $\binom n3$；独立随机染色的第一矩路线完全失效，而非仅损失常数。；从图 Ramsey 二染色直接升到三元组时，标准差值构造需要额外颜色记录非单调模式；已知四色情形因此不能推出所求二色情形。
- 第一阻塞点：要达到双指数规模，必须构造具有强相关性的三元组染色，使每个 $n$-集单色的概率或可能性远低于独立模型；目前路线没有控制差值序列局部极值所产生的单色集合的方法。
- 下一步：固定一种二进制差值二色规则，对所有长度 $q$ 的序列建立SAT实例：变量为局部极值模式的颜色，约束为禁止单色 $n$-子集；逐步增大 $n,q$，判断该规则族是否存在一致解，并从最小不可满足证书提取结构性障碍。
- 来源核对：[官方题目564](https://www.erdosproblems.com/564)截至2026年仍开放，并给出经典界 $2^{cn^2}<R_3(n)<2^{2^n}$。；同一条目明确说明四色情形已有双指数下界，颜色数不能省略。
- 时间记账：所在批次墙钟时间按题数均摊约 83.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/564)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/564.lean`；既有候选答案（按不可信材料审计）

### #566

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be such that any subgraph on $k$ vertices has at most $2k-3$ edges. Is it true that, if $H$ has $m$ edges and no isolated vertices, then\[R(G,H)\ll m?\]
- 题意摘要：正确量词是先固定有限图 $G$，假设每个含 $k\ge2$ 个顶点的子图 $J$ 满足 $e(J)\le2k-3$；问是否存在依赖于 $G$ 的常数 $C_G$，使每个无孤立点、含 $m$ 条边的图 $H$ 都满足普通 Ramsey 数 $R(G,H)\le C_Gm$。
- 状态核对：官方条目截至2026年仍开放。先前候选用 $H=K_2$ 反驳“绝对常数”并非原问题的量词：$\ll$ 的常数允许依赖固定的 $G$。此外，本地 Lean 文件误把普通 $R(G,H)$ 写成了边数 Ramsey 数 `sizeRamsey G H`。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试从稀疏条件提取可用于嵌入的分解。对每个非空子图，平均度小于4，故存在度至多3的顶点；同时 $e(J)/(v(J)-1)<2$，由 Nash–Williams 判据可把 $G$ 的边分成两个森林。随后设红图不含 $G$、蓝图不含给定 $H$，尝试利用该双森林分解逐层嵌入红色 $G$。
- 局部结论：假设严格蕴含 $G$ 为3-退化图。；假设还蕴含 $G$ 的 arboricity 至多2，即 $E(G)$ 可分成两个森林。；以通常定义 $m_2(G)=\max_{v(J)\ge3}(e(J)-1)/(v(J)-2)$，该条件等价于 $m_2(G)\le2$；这解释了为何它正处在与 $m=e(K_q)=\Theta(q^2)$ 相匹配的临界位置。
- 第一阻塞点：蓝图不含一个任意的 $m$ 边图 $H$，并不给出统一的最大度、密度或色数上界；因而双森林分解尚不能保证红图中逐步嵌入 $G$。第一处缺失的严格命题是：在 $N=C_Gm$ 个顶点上，若红图不含固定的双森林图 $G$，则其补图必包含每个无孤立点的 $m$ 边图 $H$。这基本就是原问题，简单贪心无法证明。
- 下一步：先把路线限制到 vertex-cover 数至多2的 $H$：刻画蓝图不含这类 $H$ 时共同邻域必须满足的界，并尝试用3-退化顺序嵌入红色 $G$。若能得到常数仅依赖 $G$ 的线性界，再逐步推广到有界 vertex-cover 的 $H$。
- 来源核对：[官方题目566](https://www.erdosproblems.com/566)明确解释为“固定 $G$ 是否 Ramsey size linear”，并仍标为开放。；官方条目记录的已知正面范围是 $e(G)\le v(G)+1$；不能由此覆盖临界假设 $e(J)\le2v(J)-3$。；本地形式化文件的注释写 $R(G,H)$，实际公式却使用 `sizeRamsey`，对象不一致。
- 时间记账：所在批次墙钟时间按题数均摊约 83.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/566)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/566.lean`；既有候选答案（按不可信材料审计）

### #567

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be either $Q_3$ or $K_{3,3}$ or $H_5$ (the last formed by adding two vertex-disjoint chords to $C_5$). Is it true that, if $H$ has $m$ edges and no isolated vertices, then\[R(G,H)\ll m?\]
- 题意摘要：对每个固定的 G∈{Q_3,K_{3,3},H_5}，问是否存在仅依赖于 G 的常数 C_G，使每个无孤立点、恰有 m 条边的有限图 H 都满足 R(G,H)≤C_Gm。
- 状态核对：截至2026年7月官方条目仍列为开放。已知 H_5=K_4^* 对所有二分 H 成立；至少6个顶点的 K_4 细分图也已解决，但不包括五顶点的 H_5 对一般 H。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `1/10`；置信度 `high`
- 尝试路线：先处理森林，再尝试用 H 的最大割归约到二分情形。令 g=v(G)。若 H 是森林，则可在同一顶点集上补边成为树 T，且由 Chvátal 公式及 G⊂K_g，R(G,H)≤R(K_g,T)=(g−1)(v(H)−1)+1=O_G(m)。一般 H 取最大割所得生成二分子图 B，有 e(B)≥m/2；对 H_5 可对 B 应用已知线性定理。
- 局部结论：三个指定 G 对所有森林 H 都满足 R(G,H)=O_G(m)。；对 H_5，当 H 本身是二分图时结论成立。；最大割保证每个 H 含有一个保留至少 m/2 条边的生成二分子图 B。
- 第一阻塞点：蓝色图中出现 B 并不推出出现 H：最大割删除的部内边完全没有被控制。因此“二分子图线性”不能直接提升为“一般 H 线性”。对 Q_3、K_{3,3}，甚至所需的全体二分目标图版本也尚未由该路线得到。
- 下一步：先检验最小强化：证明或否定“若删除一条边即可使 H 二分，则 R(H_5,H)=O(e(H))”；这要求量化 BGS 嵌入中一对指定顶点的共同蓝色邻域。
- 来源核对：官方状态与已知部分结果：[Erdős Problem 567](https://www.erdosproblems.com/567)。；BGS 原始论文摘要确认至少6顶点的 K_4 细分结论：[Bradač–Gishboliner–Sudakov](https://arxiv.org/abs/2202.10388)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/567)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/567.lean`；既有候选答案（按不可信材料审计）

### #568

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph such that $R(G,T_n)\ll n$ for any tree $T_n$ on $n$ vertices and $R(G,K_n)\ll n^2$. Is it true that, for any $H$ with $m$ edges and no isolated vertices,\[R(G,H)\ll m?\]
- 题意摘要：固定有限图 G。假设存在仅依赖 G 的常数，使对每棵 n 顶点树 T_n 都有 R(G,T_n)=O_G(n)，并且 R(G,K_n)=O_G(n²)。问是否随之存在 C_G，使所有无孤立点的 m 边图 H 都满足 R(G,H)≤C_Gm。
- 状态核对：截至2026年7月仍为开放问题。候选答案关于“树条件自动成立”的观察正确，但不能由此推出结论。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：把问题化为红色 G-free 图的独立集增长。树条件确实冗余：若 g=v(G)，则 R(G,T_n)≤R(K_g,T_n)=(g−1)(n−1)+1。若 R(G,K_t)≤At²，则每个 N 顶点的 G-free 红图都含大小至少 ⌊√(N/A)⌋ 的独立集，即蓝色团。尝试反复抽取这些蓝色团，按 H 的色类嵌入 H。
- 局部结论：树假设对每个固定 G 自动成立。；结论若成立，则题设两项都是必要条件：树有 n−1 条边，而 K_n 有 Θ(n²) 条边。；团假设等价地给出 G-free 红图的定量独立集下界 α≥c_G√N。
- 第一阻塞点：依次找到的蓝色团之间没有保证全部为蓝边；而嵌入一般 H 需要控制不同色类之间的指定边或共同蓝色邻域。仅有全局独立集下界不能闭合迭代嵌入。
- 下一步：检验一个可证的中间命题：在同一假设下，对色数固定且各色类间邻接型数量有界的 H，能否用共同邻域迭代得到 O_G(e(H))；首先处理完整二部图加有限个顶点的情形。
- 来源核对：官方量词和开放状态：[Erdős Problem 568](https://www.erdosproblems.com/568)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/568)；既有候选答案（按不可信材料审计）

### #569

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 1$. What is the best possible $c_k$ such that\[R(C_{2k+1},H)\leq c_k m\]for any graph $H$ on $m$ edges without isolated vertices?
- 题意摘要：固定 k≥1。按字面定义 c_k= sup_H R(C_{2k+1},H)/e(H)，其中上确界遍历所有无孤立点的有限图 H，包括 m=1；问题要求确定这个统一常数，而不只是 m→∞ 时的首项系数。
- 状态核对：官方条目仍列为开放；2026年论文已证明当 m 相对 k 足够大时 R(C_{2k+1},H)≤2m+k，故渐近最优系数是2，但这不自动确定字面上的全 m 常数 c_k。候选答案把两种问题混为一谈。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：分别建立大 m 与小 m 约束。取 H=K_2，则 R(C_{2k+1},K_2)=2k+1，故字面上的 c_k≥2k+1。取 H=mK_2，已知在 m≥2k+1 时 R(C_{2k+1},mK_2)=2m+k，说明渐近比值趋于2。新定理又给所有充分大的 m 和所有 H 以同样的上界2m+k，因此剩余障碍被压缩到依赖 k 的有限多个 m。
- 局部结论：字面统一常数满足 c_k≥2k+1，而不是仅有 c_k≥2。；渐近最优乘法系数确为2；匹配给出下界，新定理给出统一上界。；确定字面 c_k 现只需解决有限范围 1≤m<m_0(k)，但其中每个 Ramsey 极值仍可能困难。
- 第一阻塞点：尚无证明表明所有小 m 都满足 R(C_{2k+1},H)≤(2k+1)m，也没有已知反例使比值超过2k+1。候选答案中的“R≥v(H)≥2m”方向错误：无孤立点实际给 v(H)≤2m；只有专门取匹配时才有 v(H)=2m。
- 下一步：完整提取2026年论文 Theorem 10 的全 m 上界函数 f_k(m)，计算 sup_m f_k(m)/m，并检查它是否已给出≤2k+1；若没有，再从 m=2 开始分类无孤立点图 H 并求 R(C_{2k+1},H)。
- 来源核对：官方仍将字面问题列为开放：[Erdős Problem 569](https://www.erdosproblems.com/569)。；2026年原始论文证明充分大 m 时的 2m+⌊(ℓ−1)/2⌋ 上界，并给出匹配等号情形：[Cambie–Freschi–Morawski–Petrova–Pokrovskiy](https://arxiv.org/abs/2601.10238)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/569)；既有候选答案（按不可信材料审计）

### #571

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Show that for any rational $\alpha \in [1,2)$ there exists a bipartite graph $G$ such that\[\mathrm{ex}(n;G)\asymp n^{\alpha}.\]
- 题意摘要：对每个有理数 α∈[1,2)，要求存在一个固定的有限二分图 G，以及依赖 G 的正常数 c,C，使所有充分大的 n 都有 cn^α≤ex(n,G)≤Cn^α；G 必须是单个图，不是禁图族。
- 状态核对：一般情形仍开放。Bukh–Conlon 只证明每个 α∈(1,2) 可由一个有限禁图族实现；这不能直接选出族中的单个成员。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：写 α=2−a/b，其中 0<a≤b。采用 Bukh–Conlon 的平衡根树 T_{a,b}，其未根顶点数为 a、边数为 b，故密度 ρ=b/a。对适当 p，其幂族 𝒯^p 满足 ex(n,𝒯^p)=Θ(n^{2−1/ρ})=Θ(n^α)。尝试从有限族 𝒯^p 中选一个成员作为 G。
- 局部结论：α=1 已解决：取 G=P_3，则 ex(n,P_3)=⌊n/2⌋。；对每个 1<α<2，平衡根树方法严格构造了有限族 𝒯^p，使 ex(n,𝒯^p)=Θ(n^α)。；族结论给每个成员 G∈𝒯^p 以 ex(n,G)≥ex(n,𝒯^p)=Ω(n^α)，但不给所需的 O(n^α) 上界。
- 第一阻塞点：“𝒯^p-free”要求同时避开族中每个图，远强于只避开一个成员；族的 O(n^α) 上界不能传给任一单图。候选答案还声称“树副本的并自动二分”，但允许不同副本的未根顶点重合时需要额外验证；Bukh–Conlon 的正式定理本身只表述为有限图族，不能据此宣称得到单个二分图。
- 下一步：对给定最小参数 (a,b) 显式列出 𝒯^p 的重合类型，寻找一个成员 G，使族上界的树计数论证实际只使用 G；若计数必须在多个退化类型间分流，就记录这正是单图化失败的位置。
- 来源核对：官方状态及已知指数清单：[Erdős Problem 571](https://www.erdosproblems.com/history/571)。；Bukh–Conlon 原始论文明确给出的是 finite family，并陈述根树幂的上下界：[Rational exponents in extremal graph theory](https://www.its.caltech.edu/~dconlon/Rationalexponents.pdf)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/571)；既有候选答案（按不可信材料审计）

### #572

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Show that for $k\geq 3$\[\mathrm{ex}(n;C_{2k})\gg n^{1+\frac{1}{k}}.\]
- 题意摘要：对每个固定整数 k≥3，要求存在 c_k>0、n_0(k)，使所有 n≥n_0(k) 都有 ex(n,C_{2k})≥c_kn^{1+1/k}；即构造具有该边数且不含长度恰为2k的循环的图。
- 状态核对：一般 k 仍开放；k=3、5 已知成立。候选构造可严格恢复这两个特例，但不能覆盖一般 k。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：取有限域 F_q，令 v(z)=(1,z,…,z^{k−1})∈F_q^k。以 F_q^k 的点及方向 v(z) 的仿射直线为两侧作关联图 D_k(q)。它有 N=2q^k 个顶点和 q^{k+1}=Θ(N^{1+1/k}) 条边。若存在 2k-圈，沿圈相加得到 ∑a_iv(z_i)=0。把相同 z_i 合并后，由至多 k 个不同 Vandermonde 向量线性无关，推出每个出现的方向至少出现两次。
- 局部结论：当 k=3 时，三个方向位置中必有相邻的同方向直线，矛盾，故 D_3(q) 不含 C_6。；当 k=5 时，五个位置中某方向至少出现三次；C_5 的独立数为2，故两条同方向直线相邻，矛盾。因此 D_5(q) 不含 C_10。；取二次幂 q 与 (n/2)^{1/k} 相差常数倍，再添加孤立点，可把上述下界从 N=2q^k 推广到所有充分大的 n。
- 第一阻塞点：对偶数 k，方向可各出现两次并交替排列；例如 k=4 时模式 a,b,a,b 不含相邻同方向直线，Vandermonde条件不产生矛盾。对更大的奇数，某方向也未必出现超过循环独立数的次数。因此该组合论证首次在 k=4 失效。候选中的线性无关表述应为“任意至多 k 个不同向量”，修正后只支持 k=3,5。
- 下一步：在 D_4(q) 中直接解方向模式 a,b,a,b 对应的闭合方程，确定它是否确实生成 C_8；若生成，则加入一个额外代数坐标并计算其对边数和 C_8 方程的影响。
- 来源核对：官方开放状态、k=3,5 特例及当前一般下界：[Erdős Problem 572](https://www.erdosproblems.com/572)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/572)；既有候选答案（按不可信材料审计）

### #573

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that\[\mathrm{ex}(n;\{C_3,C_4\})\sim (n/2)^{3/2}?\]
- 题意摘要：对每个 n，令 ex(n;{C3,C4}) 为不含非诱导 C3、C4 子图的 n 顶点简单图的最大边数。问题问当 n→∞ 时，该数除以 (n/2)^{3/2} 是否趋于 1。
- 状态核对：仍为开放问题。旧候选把它标为开放是正确的，但其中关于最新二阶项和“竞争猜想”的细节不用于本次证明筛查。2025 年论文仍称确定该函数为长期问题。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试利用无三角形带来的邻域独立性，再结合无 C4 的局部不交性控制度数二阶矩。若 v 的邻点为 u1,…,ud，则各集合 N(ui)\{v} 两两不交；又因无 C3，它们都落在 V\(N(v)∪{v})。故 ∑_{u∈N(v)}(d(u)-1)≤n-d(v)-1，即 ∑_{u∈N(v)}d(u)≤n-1。对 v 求和得到 ∑_u d(u)^2≤n(n-1)，再用 Cauchy 得 m≤(1/2)n√(n-1)。
- 局部结论：严格得到 ex(n;{C3,C4})≤(1/2)n√(n-1)=(1/2+o(1))n^{3/2}。；平衡二部 C4-free 构造同时无三角形，给出 ex(n;{C3,C4})≥(1/(2√2)+o(1))n^{3/2}。；若能把二阶矩界加强为 ∑d(v)^2≤(1/2+o(1))n^2，则 Cauchy 立即给出所猜上界；因此问题可具体归约到这个加强版二阶矩命题。
- 第一阻塞点：现有局部不交性只给出常数 1，而目标二阶矩常数是 1/2。逐点不等式允许很大松弛，尚无严格机制证明这些松弛不能在许多顶点同时发生。
- 下一步：先在近正则情形验证命题：证明或寻找反例——若 G 无 C3、C4 且所有度数均为 (1+o(1))d，是否必有 n≥(2-o(1))d^2？这正对应所需常数，并可对有限阶高围长图作计算检验。
- 来源核对：[Ma–Yang 论文](https://arxiv.org/abs/2112.13689)仍将 ex(n,{C3,C4}) 的确定称为长期问题。；[Erdős Problems #573](https://www.erdosproblems.com/573)记录了相同开放状态及经典下界背景。
- 时间记账：所在批次墙钟时间按题数均摊约 43.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/573)；既有候选答案（按不可信材料审计）

### #574

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Is it true that, for $k\geq 2$,\[\mathrm{ex}(n;\{C_{2k-1},C_{2k}\})=(1+o(1))(n/2)^{1+\frac{1}{k}}.\]
- 题意摘要：量词应读作：对每个固定整数 k≥2，当 n→∞ 时，所有同时不含 C_{2k-1} 与 C_{2k} 的 n 顶点图，其最大边数是否等于 (1+o(1))(n/2)^{1+1/k}。只需一个固定 k 的无限反例序列即可否定全称命题。
- 状态核对：已被反驳。旧候选称其“总体开放”已经过时，且漏掉了早已存在的 k=3、5 构造；本次明确吸收并纠正该错误。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 k=3 的反例。采用已知 Lazebnik–Ustimenko–Woldar 二部 C6-free 图族，其顶点数为 n_j→∞，边数为 (2/3^{4/3}+o(1))n_j^{4/3}。二部性自动排除 C5，所以这些图同时 {C5,C6}-free。
- 局部结论：猜测在 k=3 时预言的常数是 2^{-4/3}。；反例常数严格较大：2/3^{4/3}>1/2^{4/3}，因为两者之比的立方为 128/81>1。；因此沿 n_j 这一无限序列，ex(n_j;{C5,C6})/(n_j/2)^{4/3} 的下极限大于 1，所声称的渐近式不可能成立。
- 第一阻塞点：不存在证明阻塞；反例路线已闭合。若要求完全从零重证，则未在此重建有限域图的全部定义及无 C6 验证，而是调用已发表构造定理。
- 下一步：逐页核对 LUW 构造的顶点计数与边数常数，整理成“定义—二部性—无 C6—渐近计数”四步自足证明；这只影响来源重建，不影响反驳逻辑。
- 来源核对：[Erdős Problems #574](https://www.erdosproblems.com/574)现明确标为 DISPROVED，并给出 k=3、5 的常数比较。；[LUW：A new series of dense graphs of high girth](https://arxiv.org/abs/math/9501231)核实了所用二部高围长构造的来源。
- 时间记账：所在批次墙钟时间按题数均摊约 43.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/574)；既有候选答案（按不可信材料审计）

### #575

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $\mathcal{F}$ is a finite set of finite graphs then $\mathrm{ex}(n;\mathcal{F})$ is the maximum number of edges a graph on $n$ vertices can have without containing any subgraphs from $\mathcal{F}$. Note that it is trivial that $\mathrm{ex}(n;\mathcal{F})\leq \mathrm{ex}(n;G)$ for every $G\in\mathcal{F}$. Is it true that, for every $\mathcal{F}$, if there is a bipartite graph in $\mathcal{F}$ then there exists some bipartite $G\in\mathcal{F}$ such that\[\mathrm{ex}(n;G)\ll_{\mathcal{F}}\mathrm{ex}(n;\mathcal{F})?\]
- 题意摘要：对任意有限图族 F，只要 F 至少含一个二部图，是否总能在 F 内选到某个二部成员 G，使得存在仅依赖 F 的常数 C_F，满足对所有充分大 n，ex(n;G)≤C_F ex(n;F)。
- 状态核对：输入仍标 open，但精确陈述按字面已被一个森林反例否定；网站讨论也确认“as written”存在该反例。可能真正拟议的开放版本额外假设 F 不含森林。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：独立检查旧候选的反例。取 F={P3,2K2}，两者均为二部森林。任取两条不同边：若相交便形成非诱导 P3；若不相交便形成 2K2。因此 F-free 图至多有一条边。
- 局部结论：对 n≥2，ex(n;F)=1。；P3-free 图的最大度至多 1，故 ex(n;P3)=⌊n/2⌋。；对 n≥4，2K2-free 图的边族是两两相交的二元集合族，故最多 n−1 条边，星达到该值；特别地 ex(n;2K2)=n−1。两个比值都随 n 线性发散。
- 第一阻塞点：无阻塞：该反例完整否定输入中的字面命题。它不处理额外加入“F 不含森林”的修正版。
- 下一步：核对原始 Erdős–Simonovits 文献是否遗漏了“无森林”或 ex(n;F) 超线性等假设；若有，应把修正版另立为问题，不能把本反例误报为解决那个修正版。
- 来源核对：[Erdős Problems #575 讨论页](https://www.erdosproblems.com/forum/thread/575)明确记录 Wigderson 给出了对当前文字表述的平凡反例，并建议排除森林。；旧候选的核心反例经独立逐项检查成立；仅补充了 ex(n;2K2)=n−1 需取 n≥4，n=3 有三角形例外。
- 时间记账：所在批次墙钟时间按题数均摊约 43.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/575)；既有候选答案（按不可信材料审计）

### #576

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $Q_k$ be the $k$-dimensional hypercube graph (so that $Q_k$ has $2^k$ vertices and $k2^{k-1}$ edges). Determine the behaviour of\[\mathrm{ex}(n;Q_k).\]
- 题意摘要：固定维数 k，Q_k 是具有 v=2^k 个顶点、e=k2^{k-1} 条边的超立方体图。问题要求确定当 n→∞ 时 ex(n;Q_k) 的数量级或渐近行为；k≥3 已经开放。
- 状态核对：开放。k=2 时 Q2=C4，已知 ex(n,Q2)=(1/2+o(1))n^{3/2}；k=3 及以上未确定。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试一般随机图加删边下界。取 G(n,p)，其中 p=a n^{-(v-2)/(e-1)}。期望边数为 Θ(a n^r)，Q_k 副本期望数为 O_k(a^e n^r)，这里 r=2-(v-2)/(e-1)。固定 k 后取足够小的 a，使前者常数大于后者；再从每个残余 Q_k 删除一条边。
- 局部结论：严格得到 ex(n,Q_k)=Ω_k(n^{2-(2^k-2)/(k2^{k-1}-1)})。；因 Q_k 含 C4，任何 C4-free 图都是 Q_k-free，所以另有 Ω(n^{3/2}) 下界；对 k=3，这强于上述随机删边指数 16/11。；已知上界为 O_k(n^{2-1/(k-1)+1/((k-1)2^{k-1})})；代入 k=3 得 13/8，弱于经典 8/5，故 k=3 当前仍夹在 3/2 与 8/5 之间。
- 第一阻塞点：随机删边只利用 Q_k 的顶点数和边数，完全忽略其大量重叠 4-面结构；已知上界恰恰利用这些结构。当前路线无法把下界指数推进到上界附近，也不能决定真实指数。
- 下一步：对 k=3 做可检验的专门任务：从代数 C4-free 图出发，统计添加一条边所产生的 Q3 数量，检验能否用稀疏增边加局部删边把 Ω(n^{3/2}) 改进为 n^{3/2+ε}。
- 来源核对：[Janzer–Sudakov 原论文](https://arxiv.org/abs/2211.02015)核实了所列幂次改进上界。；[Erdős Problems #576](https://www.erdosproblems.com/576)核实了 k=3 的经典 3/2 与 8/5 界。
- 时间记账：所在批次墙钟时间按题数均摊约 43.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/576)；既有候选答案（按不可信材料审计）

### #579

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\delta>0$. If $n$ is sufficiently large and $G$ is a graph on $n$ vertices with no $K_{2,2,2}$ and at least $\delta n^2$ edges then $G$ contains an independent set of size $\gg_\delta n$.
- 题意摘要：量词为：对每个固定 δ>0，是否存在 c(δ)>0 与 N(δ)，使得每个 n≥N(δ) 且 e(G)≥δn² 的 n 顶点 K_{2,2,2}-free 图都满足 α(G)≥c(δ)n。这里禁的是非诱导 K_{2,2,2}。
- 状态核对：仍开放；δ>1/8 的范围已知。旧候选关于共同邻域的表述有一处需纠正：约束适用于每一对顶点，而不只是非边，因为所禁子图不是诱导子图，同一部内允许出现额外边。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：双计数寻找大的共同邻域。令 c(x,y)=|N(x)∩N(y)|，则 ∑_{x<y}c(x,y)=∑_v binom(d(v),2)。由凸性及平均度至少 2δn，右端为 (2δ²+o(1))n³，所以某对 x,y 满足 |S|=c(x,y)≥(4δ²-o(1))n。若 G[S] 含 C4，其四个顶点连同 x,y 构成非诱导 K_{2,2,2}；故 G[S] 必为 C4-free。
- 局部结论：存在大小 Ω_δ(n) 的共同邻域 S，且 G[S] 为 C4-free。；由 ex(s,C4)=O(s^{3/2}) 及 α(H)≥|V(H)|²/(2e(H)+|V(H)|)，得到 α(G)≥α(G[S])=Ω_δ(√n)。；该推导对 x,y 是否相邻没有要求，修正了旧候选只处理非边的漏洞。
- 第一阻塞点：C4-free 性本身只能由一般独立集估计给出 √n 量级；已知稠密 C4-free 图说明不能仅从“一个线性大小共同邻域是 C4-free”推出线性独立集。必须同时利用许多共同邻域之间的相容性，而当前计数没有实现这一点。
- 下一步：量化高余度对的整体结构：证明至少 c_δn² 对 (x,y) 具有 |N(x)∩N(y)|≥c_δn，然后研究这些 C4-free 共同邻域的重叠。首个具体检验是：其关联二部图是否必含一个线性大小顶点集，使所有相关共同邻域共享同一稀疏分割；若否，构造有限反例模式。
- 来源核对：[Erdős Problems #579](https://www.erdosproblems.com/579)记录该题开放并注明 δ>1/8 已知。；共同邻域归约已按“非诱导子图”重新核验；旧候选限定为非边并不正确。
- 时间记账：所在批次墙钟时间按题数均摊约 43.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/579)；既有候选答案（按不可信材料审计）

### #584

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph with $n$ vertices and $\delta n^{2}$ edges. Are there subgraphs $H_1,H_2\subseteq G$ such that {UL} {LI}$H_1$ has $\gg \delta^3n^2$ edges and every two edges in $H_1$ are contained in a cycle of length at most $6$, and furthermore if two edges share a vertex they are on a cycle of length $4$, and {LI}$H_2$ has $\gg \delta^2n^2$ edges and every two edges in $H_2$ are contained in a cycle of length at most $8$. {/UL}
- 题意摘要：给定简单图 G，|V(G)|=n、e(G)=δn²。问是否存在 H₁,H₂⊆G：e(H₁)≥cδ³n²，H₁ 中任意两边同处于长度至多 6 的圈，且相邻两边同处于一个 C₄；同时 e(H₂)≥cδ²n²，H₂ 中任意两边同处于长度至多 8 的圈。常数 c 的一致性及 δ 的允许范围是题面隐含量词；原论文实际研究 δ=n^{-β} 且 β 在某个固定小区间内。
- 状态核对：按预期的“小 β 稀疏区间”解释仍为开放问题。Fox–Sudakov 已证明 H₂ 对 0<β<1/5 成立，且相邻边可置于长度至多 6 的圈。旧候选把“任意更小密度下仍是同一个公开猜想”说得过宽：原论文 Problem 1.1 明确只要求存在 β₀>0，使结论对 β≤β₀ 成立。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：取 G 的一个最大割得到二部子图 B，e(B)≥δn²/2。对一侧顶点度数作凸性计数，寻找具有大公共邻域的一对顶点，从而抽取 K_{2,t}。
- 局部结论：若 δn 足够大，则 ∑_x C(d_B(x),2) 的平均值给出某对同侧顶点有 t=Ω(δ²n) 个公共邻点，因此 G 含有 K_{2,t}，其边数为 Ω(δ²n)。；任意 K_{a,b}（a,b≥2）都同时满足 H₁、H₂ 的圈条件：任意两边可补成一个 C₄；特别是相邻两边也在 C₄ 上。；因此该路线严格产生一个满足全部局部圈条件、但通常只有 Ω(δ²n) 条边的子图。
- 第一阻塞点：目标 H₁ 需要 Ω(δ³n²)、H₂ 需要 Ω(δ²n²) 条边；单次公共邻域提取损失了一个 n 因子。把许多 K_{2,t} 合并时，来自不同块的两条边未必同处于一个短圈，这正是第一处无法闭合之处。
- 下一步：构造“边为顶点、两边同处于 C₆/C₈ 时相邻”的辅助图，检验 Fox–Sudakov 的正则化步骤能否给出一个含 Ω(δ²n²) 个原图边的单一高密度分量；首先应在 β=1/5 临界处逐项核算其坏边删除估计。
- 来源核对：[Fox–Sudakov 原论文](https://arxiv.org/abs/0706.1920) 的 Problem 1.1 使用“存在 β₀>0”量词；Theorem 1.2 给出 β<1/5 的强 C₈ 连通结论。；该论文还明确记录旧结果只直接给出 Ω(n^{2-3β}) 的 C₆-连通子图，允许长度 12 时才达到 Ω(n^{2-2β})。
- 时间记账：所在批次墙钟时间按题数均摊约 97.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/584)；既有候选答案（按不可信材料审计）

### #585

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the maximum number of edges that a graph on $n$ vertices can have if it does not contain two edge-disjoint cycles with the same vertex set?
- 题意摘要：令 f(n) 为满足下述禁形条件的 n 顶点简单图的最大边数：不存在两个圈 C₁,C₂，使 E(C₁)∩E(C₂)=∅ 且 V(C₁)=V(C₂)。圈的长度没有预先固定。
- 状态核对：仍开放；已知 Ω(n log log n)≤f(n)≤n(log n)^{O(1)}。2024 年上界甚至保证任意固定 k 个两两边不交、顶点集相同的圈。旧候选的主要界与原论文一致。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先把禁形归约为固定图禁形：显式检查 K_{4,4} 含有两个边不交且使用同一组 8 个顶点的 Hamilton 圈，再应用 Kővári–Sós–Turán 型上界。
- 局部结论：将 K_{4,4} 的四个完美匹配按循环位移编号为 M₀,…,M₃；M₀∪M₁ 和 M₂∪M₃ 分别是 8-圈，二者边不交且顶点集相同。故所求图必为 K_{4,4}-free。；因此固定禁图方法严格给出 f(n)=O(n^{7/4})。更精细的固定 blow-up 禁图结果可降至 n^{3/2+o(1)}，但仍远弱于多对数上界。；若存在两个所禁圈，则其并图在公共顶点集上是 4-正则图。因此“无任何 4-正则子图”的 PRS 构造必然满足禁形条件，解释了 Ω(n log log n) 下界。反向蕴含不成立：一般 4-正则图未必分解成两个 Hamilton 圈。
- 第一阻塞点：固定禁图/Turán 路线至多利用局部稠密模式，不能从平均度 polylog(n) 强迫一个跨越同一顶点集的两套 Hamilton 结构；需要正则化、扩张、吸收及路径连接，这里无法从 K_{4,4} 归约严格推出。
- 下一步：重建 CJMM 的第一项关键正则化引理：从平均度 polylog(n) 的图中抽取近正则子线性扩张器，并逐项核验随机保留顶点后连接性质是否仍成立。
- 来源核对：[CJMM 原论文](https://arxiv.org/abs/2404.07190) Theorem 2 给出统一指数 t，使 e(G)≥c_k n(log n)^t 时存在 k 个所需圈。；同一论文明确给出 K_{4,4} 禁图的 O(n^{7/4}) 旧上界，以及 PRS 无 4-正则子图构造所给的 Ω(n log log n) 下界。
- 时间记账：所在批次墙钟时间按题数均摊约 97.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/585)；既有候选答案（按不可信材料审计）

### #588

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f_k(n)$ be minimal such that if $n$ points in $\mathbb{R}^2$ have no $k+1$ points on a line then there must be at most $f_k(n)$ many lines containing at least $k$ points. Is it true that\[f_k(n)=o(n^2)\]for $k\geq 4$?
- 题意摘要：固定整数 k≥4。对每个 n，在所有 n 点平面点集 P（任一直线上至多 k 点）中，取含至少 k 点的直线数的最大值 f_k(n)。由于至多 k 点，这些恰是恰含 k 点的直线。问题是对每个固定 k≥4 是否有 f_k(n)/n²→0。
- 状态核对：仍开放，甚至 k=4 未知。Solymosi–Stojaković 构造给出 f_k(n)≥n^{2-c_k/√log n}，所以任何固定幂节省 O(n^{2-ε}) 都不可能。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把每条 k 点线视为点集 P 上的一个 k-元超边。由于两点决定唯一直线，这得到一个线性 k-一致超图；先做点对计数，再考察能否由线性性推出次二次界。
- 局部结论：不同 k 点线所含的点对互不相交，故 f_k(n)C(k,2)≤C(n,2)，即 f_k(n)≤n(n-1)/(k(k-1))。；若反设存在固定 ε>0 及无限多个 n 使 f_k(n)≥εn²，则总关联数为 kf_k(n)，所以至少一个点通过 Ω(n) 条 k 点线；更一般地，点的平均富线度为 Ω(n)。；纯组合线性性不足以导致矛盾：Steiner 型线性 k-一致超图可以有 Θ(n²) 个超边。因此任何 o(n²) 证明必须实质使用这些超边可由实平面共线关系实现。
- 第一阻塞点：第一处障碍是从“某点经过线性多个 k 点线”推出全局几何退化。删除该点后，这些线只给出许多互不相交的 (k−1)-点组，并不强迫另一条线出现 k+1 个点；点对计数也已达到设计理论允许的极限。
- 下一步：对假设 f_k(n)≥εn² 的配置作射影对偶，精确计算 n 条对偶线的 k 重交点、二重交点和面数，检验 Melchior/Hirzebruch 型不等式在“最大重数 k”条件下是否能迫使 Ω(n²) 个普通交点，并判断这能否与原配置的富线数矛盾。
- 来源核对：[Solymosi–Stojaković 原论文](https://arxiv.org/abs/1107.0327) 的摘要明确给出每个 k>3 的 n^{2-c/√log n} 构造。；未采用旧候选引用的 Wikipedia；这里的上界直接由点对唯一决定直线得到。
- 时间记账：所在批次墙钟时间按题数均摊约 97.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/588)；既有候选答案（按不可信材料审计）

### #589

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ be maximal such that in any set of $n$ points in $\mathbb{R}^2$ with no four points on a line there exists a subset on $g(n)$ points with no three points on a line. Estimate $g(n)$.
- 题意摘要：对每个无四点共线的 n 点集 P，令 α(P) 为其中无三点共线的最大子集大小；题目的 g(n)=min_{|P|=n}α(P)，即对所有 P 都能保证的最大整数。
- 状态核对：仍开放。已核对的已知界为 Ω(√(n log n))≤g(n)≤n^{5/6+o(1)}，并且 g(n)=o(n)。输入 official_context 中的“n^{1/2} log n≪g(n)”疑似排版遗漏根号范围；Füredi 原论文摘要及后续论文均写 √(n log n)。因此旧候选在这一点是正确的。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：建立三一致超图 H(P)：顶点为 P，共线三元组为超边。无四点共线保证任意一对顶点至多属于一条超边。选择一个极大独立集 A，并用极大性计数 P\A。
- 局部结论：Q⊆P 无三点共线当且仅当 Q 是 H(P) 的独立集；故 g(n)=min_P α(H(P))。；对极大独立集 A，每个 v∈P\A 都与 A 中某一对 {a,b} 构成超边。由于一对点至多确定一个第三点，该映射 v↦{a,b} 可选为单射。于是 n−|A|≤C(|A|,2)。；解该二次不等式得 |A|≥(√(8n−7)−1)/2=√(2n)−O(1)，严格重建了基础 Ω(√n) 下界。
- 第一阻塞点：上述注入只使用“线性三图”性质，已经无法产生额外 log 因子；要达到 Füredi 的 Ω(√(n log n))，必须调用线性/无短圈三图的更强独立集定理或其随机选择证明，而该定理未在本次受限尝试中重证。
- 下一步：逐条重建 Füredi 1991 年论文中从平面三图到 Ω(√(n log n)) 独立集的归约，特别核验其超图 girth/局部结构假设是否确由“无四点共线”满足。
- 来源核对：[Füredi 论文页面](https://epubs.siam.org/doi/pdf/10.1137/0404019) 摘要给出的下界是 Ω(√(n log n))，不是 √n·log n。；[Balogh–Solymosi 原论文](https://arxiv.org/abs/1704.05089) 给出存在无四点共线配置，使每个 n^{5/6+o(1)} 大小子集均含共线三点。
- 时间记账：所在批次墙钟时间按题数均摊约 97.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/589)；既有候选答案（按不可信材料审计）

### #591

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $\alpha$ be the infinite ordinal $\omega^{\omega^2}$. Is it true that in any red/blue colouring of the edges of $K_\alpha$ there is either a red $K_\alpha$ or a blue $K_3$?
- 题意摘要：令 α=ω^{ω²}，序数运算均为序数运算。量词是：对每个染色 c:[α]^2→{红,蓝}，或者存在 X⊆α 且 otp(X)=α，使 [X]^2 全红；或者存在三个顶点，其三条边全蓝。即 α→(α,3)^2，而不是仅按可数基数解释 K_α。
- 状态核对：状态“proved”核对无误；这是 Schipperus 定理的直接特例，Darby 也独立得到该特例。旧候选结论正确，但应把定理假设准确表述为：β 的 Cantor 标准形至多有两个加法项。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建已知归约：应用 Schipperus 的定理“若可数序数 β 的 Cantor 标准形至多有两个加法项，则 ω^{ω^β}→(ω^{ω^β},3)^2”，并代入 β=2。
- 局部结论：β=2=ω⁰+ω⁰ 是可数序数，其 Cantor 标准形按重复项计至多两个加法项，满足定理假设。；代入后 ω^{ω^β}=ω^{ω²}=α，故得到 α→(α,3)^2，恰好对应题面红 K_α 或蓝 K₃。；本地 Lean 文件确实将目标编码为 OrdinalCardinalRamsey (ω ^ ω ^ 2) (ω ^ ω ^ 2) 3；但证明体仍为 sorry，所以它只是陈述编码，不构成形式验证。
- 第一阻塞点：在引用 Schipperus 已发表定理后没有逻辑缺口；本次没有重建的第一项深层步骤正是该定理本身的跨有限块/序数归纳证明。因此结论属于已知定理核对，而非新的自足证明。
- 下一步：若需形式核验，下一任务是先在 Lean 中形式化 Schipperus 定理的“至多两个 Cantor 标准形项”特例，再证明 β=2 的参数条件并消除当前 sorry。
- 来源核对：[Schipperus 定理的形式化论文说明](https://api.repository.cam.ac.uk/server/api/core/bitstreams/8ebcb085-66b0-4dbb-9b3b-b8d0d83b45cb/content) Theorem 2.2 明确陈述上述两项 Cantor 标准形条件。；本地 FormalConjectures 文件标注该题由 Schipperus 与 Darby 独立解决，但 theorem 仍含 sorry，故未误报为 formally verified。
- 时间记账：所在批次墙钟时间按题数均摊约 97.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/591)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/591.lean`；既有候选答案（按不可信材料审计）

### #592

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Determine which countable ordinals $\beta$ have the property that, if $\alpha=\omega^{^\beta}$, then in any red/blue colouring of the edges of $K_\alpha$ there is either a red $K_\alpha$ or a blue $K_3$.
- 题意摘要：对每个可数序数 \(\beta<\omega_1\)，令 \(\alpha=\omega^\beta\)。要求判定何时对所有染色 \(c:[\alpha]^2\to\{\mathrm{red},\mathrm{blue}\}\)，或者存在序型为 \(\alpha\) 的全红子集，或者存在三个点组成全蓝三角；即 \(\omega^\beta\to(\omega^\beta,3)^2\)。
- 状态核对：冻结状态为 open，当前公开条目仍为 open，但输入背景及旧候选已经过时：\(\beta=\omega^2\) 已由 Schipperus 与 Darby 证明为正例，不能再称为首个开放情形。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先用 Galvin–Larson 必要条件把 \(\beta\ge3\) 限制为 \(\beta=\omega^\gamma\)，再对 \(\gamma\) 的 Cantor 正规形应用 Schipperus 的正、负结果。这样把分类问题归约到 \(\gamma\) 恰为三个加法不可分序数之和的情形。
- 局部结论：若 \(\beta\ge3\) 且关系成立，则 \(\beta\) 加法不可分，故 \(\beta=\omega^\gamma\)；所有加法可分的 \(\beta\ge3\) 都是严格反例。；写成 \(\beta=\omega^\gamma\) 后，若 \(\gamma\) 是一个或两个加法不可分序数之和，则 Schipperus 给出 \(\omega^{\omega^\gamma}\to(\omega^{\omega^\gamma},3)^2\)。特别地 \(\beta=\omega^2\) 已解决为正。；当前条目记载：若 \(\gamma\) 是四个或更多加法不可分序数之和则关系失败；因此剩余核心是恰有三个加法不可分加项的 \(\gamma\)。小值另有 \(\beta=0,1,2\) 为正，有限 \(3\le\beta<\omega\) 为负。
- 第一阻塞点：现有正面构造只能控制至多两个 Cantor 加项，负面着色从四个加项开始；在三个加项时，两种递归结构之间留下缺口，无法证明红色子集仍有完整序型，也无法构造规避蓝三角的着色。
- 下一步：取最小测试族 \(\gamma=\omega^{\rho_0}+\omega^{\rho_1}+\omega^{\rho_2}\)，逐条核对 Schipperus 正证明中“两个块”的融合引理，判断第三块首次破坏的是哪一条 pinning/递归引理，并尝试在 \(\rho_0=\rho_1=\rho_2=0\) 即 \(\gamma=3\) 上闭合或反驳该引理。
- 来源核对：[Erdős Problem #592 当前条目](https://www.erdosproblems.com/592) 明确记载 Schipperus 的正负范围及剩余三加项情形。；[Schipperus, Countable partition ordinals](https://www.sciencedirect.com/science/article/pii/S0168007209002188) 的摘要支持“一或两个不可分加项”的正定理。；旧候选关于“所有 \(\gamma\ge2\) 均开放、首例 \(\beta=\omega^2\)”的结论已被后续资料否定。
- 时间记账：所在批次墙钟时间按题数均摊约 93.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/592)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/592.lean`；既有候选答案（按不可信材料审计）

### #593

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Characterize those finite 3-uniform hypergraphs which appear in every 3-uniform hypergraph of chromatic number $>\aleph_0$.
- 题意摘要：固定有限简单三一致超图 \(F\)。称其 obligatory，若对每个三一致超图 \(H\)，只要顶点色数 \(\chi(H)>\aleph_0\)，就存在单射 \(f:V(F)\to V(H)\) 将每条 \(F\)-边送到 \(H\)-边；不要求诱导。问题是刻画所有这样的 \(F\)。
- 状态核对：冻结状态及当前公开条目均为 open。旧候选列出了若干现代必要条件和充分族，但它们并未组成分类。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：从最简单的充分族“有限匹配”入手，尝试由不可数色数直接推出任意大的匹配。反设不存在大小 \(m\) 的匹配，取极大匹配并用其顶点集构造有限顶点覆盖和显式有限着色。
- 局部结论：若 \(H\) 的匹配数有限，则一个有限极大匹配的顶点并集 \(S\) 覆盖所有边；否则可加入一条与之不交的边。；把 \(S\) 中每个顶点赋予不同颜色，把 \(V(H)\setminus S\) 赋予一个新颜色，则没有单色边，所以 \(\chi(H)\le |S|+1<\aleph_0\)。；因此 \(\chi(H)>\aleph_0\) 的三一致超图含可数无限匹配，尤其每个有限三一致匹配都是 obligatory。
- 第一阻塞点：该覆盖论证只处理彼此不交的边。加入一条与旧边恰交一个顶点时，极大匹配的顶点覆盖不保留所需交叠模式；需要一种保持不可数色数的 link/残余超图引理，当前论证无法给出。
- 下一步：检验如下可证伪引理：若 \(\chi(H)>\aleph_0\)，是否存在顶点 \(v\) 使其 link 图在某个不可数色数残余集合上足以扩张给定 loose tree；若否，尝试用所有 link 均“可数可控”构造全局可数顶点着色。
- 来源核对：[Erdős Problem #593](https://www.erdosproblems.com/593) 确认完整刻画仍开放。；[Reiher, Obligatory hypergraphs](https://arxiv.org/abs/2403.11223) 确认该现代术语及存在更大的已知充分族；本次局部证明不依赖其深层定理。；旧候选对“线性、三部”等必要条件及二部图 expansion 的陈述需要逐一定理级核对；它们即使正确也不足以闭合分类。
- 时间记账：所在批次墙钟时间按题数均摊约 93.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/593)；既有候选答案（按不可信材料审计）

### #595

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an infinite graph $G$ which contains no $K_4$ and is not the union of countably many triangle-free graphs?
- 题意摘要：求是否存在一个图 \(G\)，满足 \(K_4\nsubseteq G\)，且不存在序列 \((G_n)_{n<\omega}\) 的三角形自由子图使 \(E(G)=\bigcup_{n<\omega}E(G_n)\)。等价地，每个边染色 \(c:E(G)\to\omega\) 都产生单色三角形。
- 状态核对：公开状态仍为 ZFC 中 open。Shelah 证明正答案相对一致，但这本身不构成独立性：尚未给出否定答案模型。旧候选把它称作“ZFC 未知”是合适的。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试把每个有限 \(n\) 的 Folkman 图拼成一个统一见证。取 \(K_4\)-自由图 \(F_n\)，使任何 \(n\)-边染色都有单色三角形，并考察不交并 \(G=\bigsqcup_nF_n\)。
- 局部结论：“可数个三角形自由子图覆盖”与“可数边染色无单色三角形”等价：从覆盖可把每条边分配给一个包含它的最小指标。；上述不交并确实对每个固定有限色数失败，因为相应分量 \(F_n\) 已经失败。；但该不交并只有可数条边；给每条边不同颜色即可避免单色三角形。因此任何真正见证必须有不可数多条边，且其非孤立顶点集不可数。
- 第一阻塞点：有限 Folkman 性质仅说明覆盖数在有限基数中无界，不能由紧致性推出覆盖数大于 \(\aleph_0\)；直接极限或不交并恰好仍可被可数颜色逐边稀释。这是该路线第一处严格失败。
- 下一步：研究一个连续链 \((G_\xi)_{\xi<\omega_1}\) 的扩张条件：给定先前任意可数无单色三角形染色，能否在下一阶段强迫其某个已有颜色形成三角形，同时保持 \(K_4\)-自由；先在长度 \(\omega+1\) 的有限近似树上检验相容性。
- 来源核对：[Erdős Problem #595](https://www.erdosproblems.com/595) 确认 ZFC 问题仍开放及所有有限色数版本已知。；[旧 Erdős 问题档案](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/InfiniteTriangleFreeCovering.html) 明确记载 Shelah 的相对一致正答案以及 ZFC 可证性未知。
- 时间记账：所在批次墙钟时间按题数均摊约 93.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/595)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/595.lean`；既有候选答案（按不可信材料审计）

### #596

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which graphs $G_1,G_2$ is it true that {UL} {LI} for every $n\geq 1$ there is a graph $H$ without a $G_1$ but if the edges of $H$ are $n$-coloured then there is a monochromatic copy of $G_2$, and yet{/LI} {LI} for every graph $H$ without a $G_1$ there is an $\aleph_0$-colouring of the edges of $H$ without a monochromatic $G_2$. {/UL}
- 题意摘要：对图 \(G_1,G_2\)，令 \(q_{G_2}(H)\) 为避免单色 \(G_2\) 所需的最小边颜色数。要求同时满足：对每个整数 \(n\ge1\)，存在不含 \(G_1\) 的图 \(H_n\) 且 \(q_{G_2}(H_n)>n\)；但对每个不含 \(G_1\) 的图 \(H\)，均有 \(q_{G_2}(H)\le\aleph_0\)。问题是刻画全部这样的有序对。
- 状态核对：完整分类仍 open；但 \((C_4,C_6)\) 是已知正例，不是待证猜想。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建 \((C_4,C_6)\) 的两半：有限色一半调用 Nešetřil–Rödl 的受限 Ramsey 构造；可数色一半使用 Erdős–Hajnal 的定理，把任意 \(C_4\)-自由图的边覆盖为可数棵树，再把重叠覆盖细化成边分割。
- 局部结论：对每个有限 \(n\)，存在 \(C_4\)-自由的 \(H_n\) 使每个 \(n\)-边染色均有单色 \(C_6\)。；若 \(H\) 不含 \(C_4\)，写 \(E(H)=\bigcup_{k<\omega}E(T_k)\)，其中每个 \(T_k\) 是树；把每条边分配给最小可用的 \(k\)，所得每个颜色类是森林。；森林不含 \(C_6\)，故该分配给出可数边染色且无单色 \(C_6\)。因此 \((C_4,C_6)\) 严格满足两项条件。
- 第一阻塞点：这只验证一个点而非分类。旧候选进一步声称所有“有圈且围长大于 4”的 \(G_2\) 都与 \(C_4\) 配对成功；第二项确由树覆盖推出，但第一项需要精确版本的高围长 Ramsey 定理。所给官方材料只明确支持 \(C_6\)，故本筛查不把该推广当作已核实结论。
- 下一步：查明 Nešetřil–Rödl 定理是否逐字保证：对每个有限、含圈且 \(C_3,C_4\)-自由的 \(F\) 及每个 \(n\)，存在 \(C_4\)-自由 \(H\) 满足 \(H\to(F)^2_n\)。若成立，即可严格扩张出一整族 \((C_4,F)\)。
- 来源核对：[Erdős Problem #596](https://www.erdosproblems.com/596) 明确确认 \((C_4,C_6)\) 的两项定理及完整分类开放。；候选的更广 \(C_4\)-族没有从其所给 Erdős 条目直接得到支持，必须回到 Nešetřil–Rödl 原定理核对围长假设。
- 时间记账：所在批次墙钟时间按题数均摊约 93.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/596)；既有候选答案（按不可信材料审计）

### #597

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph on at most $\aleph_1$ vertices which contains no $K_4$ and no $K_{\aleph_0,\aleph_0}$ (the complete bipartite graph with $\aleph_0$ vertices in each class). Is it true that\[\omega_1^2 \to (\omega_1\omega, G)^2?\]What about finite $G$?
- 题意摘要：固定至多有 \(\aleph_1\) 个顶点、且不含 \(K_4\) 和 \(K_{\aleph_0,\aleph_0}\) 的图 \(G\)。问是否对每个 \(c:[\omega_1^2]^2\to\{0,1\}\)，或者存在序型 \(\omega_1\cdot\omega\) 的全 0 集，或者存在单射 \(f:V(G)\to\omega_1^2\) 使每条 \(G\)-边映成颜色 1；复制不要求诱导。另问有限 \(G\) 的情形。
- 状态核对：一般情形及有限 \(K_4\)-自由图情形仍标为 open。Baumgartner 的 \(K_{\aleph_0,\aleph_0}\) 反例解释了第二个排除条件。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从 Erdős–Hajnal 已知关系 \(\omega_1^2\to(\omega_1\omega,K_3)^2\) 出发，尝试按顶点逐步扩张蓝色嵌入。先确定该基例实际能覆盖的全部 \(G\)。
- 局部结论：若没有序型 \(\omega_1\omega\) 的红齐次集，则已知定理保证存在蓝色 \(K_3\)。；因此，只要删去孤立点后的 \(G\) 是 \(K_3\) 的子图，所求关系成立；至多 \(\aleph_1\) 个孤立点可从其余顶点中任意补入，因为复制非诱导。；Baumgartner 的结果表明不能仅凭 \(K_4\)-自由假设处理任意无限 \(G\)：\(G=K_{\aleph_0,\aleph_0}\) 已失败。
- 第一阻塞点：逐点扩张有限 \(K_4\)-自由图时，若新顶点需连接到已嵌入的若干点，就必须在这些点的蓝色邻域交中找到新点。现有 \(K_3\) 定理只产生一次三角形，没有任何有限共同蓝邻域仍保留足够序型的扩张引理；证明在此首次中断。
- 下一步：先处理最小的未覆盖有限图 \(P_4\) 或 \(C_4\)：假设蓝图不含该图，尝试证明其结构迫使红图含序型 \(\omega_1\omega\) 的独立集。具体可检验蓝色邻域差族是否必为链状/星状，并对 \(\omega_1\) 个 ordinal blocks 做压缩。
- 来源核对：[Erdős Problem #597](https://www.erdosproblems.com/597) 确认 \(K_3\) 正结果、Baumgartner 反例以及开放状态。；旧候选讨论的 CH 下 \(K_4\) 负关系针对被题设明确排除的 \(G=K_4\)，不能推进有限 \(K_4\)-自由情形；本筛查不把它计作局部进展。
- 时间记账：所在批次墙钟时间按题数均摊约 93.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/597)；既有候选答案（按不可信材料审计）

### #598

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $m$ be an infinite cardinal and $\kappa$ be the successor cardinal of $2^{\aleph_0}$. Can one colour the countable subsets of $m$ using $\kappa$ many colours so that every $X\subseteq m$ with $\lvert X\rvert=\kappa$ contains subsets of all possible colours?
- 题意摘要：令 \(\kappa=(2^{\aleph_0})^+\)。对每个固定无限基数 \(m\)，问是否存在映射 \(c:[m]^{\aleph_0}\to\kappa\)，使每个 \(X\in[m]^\kappa\) 都满足 \(c[[X]^{\aleph_0}]=\kappa\)。这里“可数子集”按大小恰为 \(\aleph_0\) 理解。
- 状态核对：整题仍标为开放；但 \(m=\kappa\) 有直接的 ZFC 正解。旧候选所谓“本质归约到 \(m=\kappa\)”不成立：从大 \(m\) 限制到一个 \(\kappa\)-子集只给出必要条件，不能反向覆盖大 \(m\) 的所有 \(\kappa\)-子集。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先严格解决临界情形 \(m=\kappa\)。把 \(E^\kappa_\omega=\{\delta<\kappa:\operatorname{cf}(\delta)=\omega\}\) 分割为两两不交的平稳集 \((S_\xi)_{\xi<\kappa}\)。定义 \(c(a)=\xi\) 当 \(\sup a\in S_\xi\)，其余情况任意着色。若 \(X\in[\kappa]^\kappa\)，则正则性使 \(X\) 无界，\(\operatorname{acc}(X)\) 是 club；故每个 \(S_\xi\) 与之相交于某个余终度 \(\omega\) 的 \(\delta\)。从 \(X\cap\delta\) 取可数余终子集 \(a\)，即得 \(c(a)=\xi\)。
- 局部结论：若 \(m<\kappa\)，在通常把“着色”理解为取值于调色板 \(\kappa\) 时，条件因不存在 \(X\in[m]^\kappa\) 而真空成立。；\(m=\kappa\) 在 ZFC 中成立；上述证明只用正则基数上的平稳集分割定理。；若某个 \(m\ge\kappa\) 有所求着色，则限制到任意 \(Y\in[m]^\kappa\) 给出 \(m=\kappa\) 的着色；反向延拓没有得到。
- 第一阻塞点：对 \(m>\kappa\)，无法给每个 \(X\in[m]^\kappa\) 同时提供类似“平稳集交 club”的结构；任意投影 \(m\to\kappa\) 在某个 \(\kappa\)-大小集合上可能高度塌缩。这是该具体路线第一次无法闭合之处。
- 下一步：检验以下明确子问题：对哪些 \(m>\kappa\) 存在函数 \(s:[m]^{\aleph_0}\to E^\kappa_\omega\)，使每个 \(X\in[m]^\kappa\) 的像与每个平稳子集相交；若不能，尝试由失败的 \(s\) 构造反例型 \(X\)。
- 来源核对：[官方条目仍标为开放](https://www.erdosproblems.com/598)。；[官方讨论中也出现了同一平稳集特例证明](https://www.erdosproblems.com/forum/thread/598)；这里已逐步独立核验，而未把评论当作完整解答。
- 时间记账：所在批次墙钟时间按题数均摊约 95.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/598)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/598.lean`；既有候选答案（按不可信材料审计）

### #600

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $e(n,r)$ be minimal such that every graph on $n$ vertices with at least $e(n,r)$ edges, each edge contained in at least one triangle, must have an edge contained in at least $r$ triangles. Let $r\geq 2$. Is it true that\[e(n,r+1)-e(n,r)\to \infty\]as $n\to \infty$? Is it true that\[\frac{e(n,r+1)}{e(n,r)}\to 1\]as $n\to \infty$?
- 题意摘要：固定整数 \(r\ge2\)。令 \(e(n,r)\) 为最小阈值，使每个 \(n\) 点图，只要边数至少为该阈值且每条边至少属于一个三角形，就必有一条边属于至少 \(r\) 个三角形。分别问 \(e(n,r+1)-e(n,r)\to\infty\) 及 \(e(n,r+1)/e(n,r)\to1\)。
- 状态核对：两问均仍开放。已知的 \(e(n,r)=o(n^2)\) 对比较相邻 \(r\) 尚不足够。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：引入极值量 \(F_r(n)=\max\{|E(G)|:|V(G)|=n,\ 1\le t_G(e)\le r-1\text{ 对所有边 }e\}\)，则 \(e(n,r)=F_r(n)+1\)。尝试用不交并和小完全图比较相邻参数：\(K_{r+2}\) 的每条边恰在 \(r\) 个三角形中，所以它可用于 \(F_{r+1}\)。
- 局部结论：\(F_{r+1}(n)\ge F_r(n)\)，故 \(e(n,r+1)\ge e(n,r)\) 且相应比值至少为 \(1\)。；不交并给出超可加性 \(F_r(a+b)\ge F_r(a)+F_r(b)\)。特别地，\(F_{r+1}(n+r+2)\ge F_r(n)+\binom{r+2}{2}\)。；由不交三角形，\(F_r(n)\ge3\lfloor n/3\rfloor\)，所以 \(e(n,r)\to\infty\)；要证比值趋于 \(1\)，只需但仍须证明 \(F_{r+1}(n)-F_r(n)=o(F_r(n))\)。
- 第一阻塞点：不交并只产生带固定顶点位移 \(n\mapsto n+r+2\) 的下界。删除这些顶点可能同时破坏“每条剩余边仍在三角形中”，因此不能把位移不等式转成同一 \(n\) 下的差值增长，更不能控制差值为 \(o(F_r(n))\)。
- 下一步：检验“近极值图中存在可删除的 \(O_r(1)\) 个顶点且只损失 \(o(F_r(n))\) 条有效边”这一稳定性命题；先对 \(r=2\) 用三角形分解结构做计算或寻找反例。
- 来源核对：[官方条目确认两问开放，并记载固定 \(r\) 时 \(e(n,r)=o(n^2)\)](https://www.erdosproblems.com/600)。
- 时间记账：所在批次墙钟时间按题数均摊约 95.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/600)；既有候选答案（按不可信材料审计）

### #601

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which limit ordinals $\alpha$ is it true that if $G$ is a graph with vertex set $\alpha$ then $G$ must have either an infinite path or independent set on a set of vertices with order type $\alpha$?
- 题意摘要：对每个极限序数 \(\alpha\)，判断是否满足：每个顶点集按自然序恰为 \(\alpha\) 的无向图 \(G\)，或者含有一条可数单向无限简单路径，或者含有独立集 \(I\subseteq\alpha\) 且 \(\operatorname{otp}(I)=\alpha\)。所求是全部此类 \(\alpha\) 的分类。
- 状态核对：完整分类仍开放。旧候选把“临界点独立”混同于“整题已分类”并不妥；不过临界实例确有相对一致性机制：\(\Diamond\) 给出反例，而 \(MA+\neg CH\) 使该序数低于连续统，从而由 Larson 定理得到正例。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先重建初始序数情形。若 \(\alpha=\kappa\) 是无限基数，对边/非边作二染色并应用 Erdős–Dushnik–Miller 关系 \(\kappa\to(\kappa,\omega)^2\)：得到大小 \(\kappa\) 的独立集，因其为 \(\kappa\) 的子集而序型为 \(\kappa\)；或得到可数无限团，从中枚举出无限路径。再尝试把这一论证沿 \(\alpha\) 的序数分块推广。
- 局部结论：所有无限初始序数 \(\kappa\) 都满足所求二择一。；已知 Erdős–Hajnal–Milner 证明所有极限 \(\alpha<\omega_1^{\omega+2}\) 成立。；在 \(\Diamond\) 下，区间 \(\omega_1^{\omega+2}\le\alpha<\omega_2\) 有反例；在 \(MA\) 且连续统大于 \(\omega_1\) 的模型中，临界序数低于连续统并满足正关系。因此临界实例不是单纯的 ZFC 证明目标。
- 第一阻塞点：对非初始序数，把 \(\alpha\) 分成基数大小的块并分别取大独立集后，无法保证不同块所取集合之间没有边；直接应用基数 Ramsey 定理只控制基数，不保持完整序型 \(\alpha\)。这正是分块路线第一次失效处。
- 下一步：选取首个未由已知区间覆盖的正规形 \(\alpha=\omega_1^{\omega+2}\)，把 Baumgartner–Larson 的 \(\Diamond\) 构造拆成一个可核验引理：其图为何无无限路径，以及每个序型 \(\alpha\) 的集合为何必含边；同时核对 MA 侧所需的连续统严格不等式。
- 来源核对：[官方条目给出 ZFC 正区间与 MA 结果](https://www.erdosproblems.com/601)。；[Baumgartner–Larson 论文摘要明确说明 \(\Diamond\) 下临界区间的反例](https://www.sciencedirect.com/science/article/pii/016800729090013R)。
- 时间记账：所在批次墙钟时间按题数均摊约 95.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/601)；既有候选答案（按不可信材料审计）

### #602

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $(A_i)$ be a family of sets with $\lvert A_i\rvert=\aleph_0$ for all $i$, such that for any $i\neq j$ we have $\lvert A_i\cap A_j\rvert$ finite and $\neq 1$. Is there a $2$-colouring of $\cup A_i$ such that no $A_i$ is monochromatic?
- 题意摘要：给任意指标集 \(I\) 及可数无限集合族 \((A_i)_{i\in I}\)，假设不同成员的交集有限且大小不等于 \(1\)，问是否总存在 \(c:\bigcup_iA_i\to\{0,1\}\)，使每个 \(A_i\) 同时含两种颜色。
- 状态核对：仍开放。人工评审指出的极限阶段错误成立，旧候选不能作为证明：后继步不立即破坏已修集合，并不蕴含在极限步仍不单色。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先保留旧路线中可严格证明的局部翻色引理：若 \(A_i\) 当前单色，翻转其中一点 \(x\)，则其他 \(A_j\) 不会在该后继步首次变成单色，否则必推出 \(A_i\cap A_j=\{x\}\)。随后尝试用乘积紧致性处理极限阶段，并检查可数子族作为基例。
- 局部结论：单次修复引理正确：禁止单点交排除了任何一步中对其他集合的即时破坏。；任意可数子族甚至无需交集条件即可二染色：递归为第 \(n\) 个集合选取两个此前从未选过的点，分别染成 \(0,1\)。；任意有限子族同样可染；但这不足以通过普通紧致性推出任意族，因为“\(A_i\) 非单色”是依赖无限多个坐标的开条件，而非闭条件。
- 第一阻塞点：在极限序数 \(\lambda\)，某个集合可能在每个 \(\beta<\lambda\) 都保有两色，却没有任何固定的异色见证对永久保留；颜色变化的共尾累积可能使它在极限首次单色。旧候选的“每点至多翻一次”正是在此处未经证明，且其理由只说明翻色当下的状态。
- 下一步：尝试强化递归不变量：每次修复 \(A_i\) 时指定一对永久冻结的异色见证，并把问题归约为能否在禁止单点交的几乎不交族中选择互不冲突的见证对；先验证所有大小 \(\le\aleph_1\) 的子族或构造该选择命题的反例。
- 来源核对：[官方条目仍将问题列为开放](https://www.erdosproblems.com/602)。；已明确吸收输入中的人工评审：不再复述错误的极限递归结论。
- 时间记账：所在批次墙钟时间按题数均摊约 95.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/602)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/602.lean`；既有候选答案（按不可信材料审计）

### #603

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $(A_i)$ be a family of countably infinite sets such that $\lvert A_i\cap A_j\rvert \neq 2$ for all $i\neq j$. Find the smallest cardinal $C$ such that $\cup A_i$ can always be coloured with at most $C$ colours so that no $A_i$ is monochromatic.
- 题意摘要：量词是：寻找单一基数 \(C\)，使对任意大小的集合族 \(\mathcal A\)，只要每个成员可数无限且不同成员交集大小不为 \(2\)，就能用至多 \(C\) 色染 \(\bigcup\mathcal A\)，并使每个成员非单色。
- 状态核对：按输入冻结状态重建后，结论是不存在这样的基数 \(C\)，而非 \(C=\aleph_0\)。当前网页缓存仍显示 OPEN，但其讨论和 2026 年证明材料给出了完整反例；组合论证可独立核验。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：固定任意候选基数 \(\mu\)。由 Erdős–Rado 定理取 \(\kappa\) 使 \(\kappa\to(\omega)^2_\mu\)；无限 \(\mu\) 可取 \(\kappa=(2^\mu)^+\)。令底集 \(V=[\kappa]^2\)，并对每个 \(X\in[\kappa]^\omega\) 置 \(A_X=[X]^2\)。任意 \(\mu\)-着色 \(V\) 都有可数无限齐次集 \(H\)，于是 \(A_H\) 单色。
- 局部结论：每个 \(A_X\) 可数无限。；\(A_X\cap A_Y=[X\cap Y]^2\)；若 \(|X\cap Y|=n<\omega\)，交集大小为 \(\binom n2\in\{0,1,3,6,\ldots\}\)，若交集无限则大小为 \(\aleph_0\)，故永不等于 \(2\)。；由于上述构造对每个基数 \(\mu\) 都产生色数大于 \(\mu\) 的族，所求统一基数不存在。若题意另限定族本身可数，则精确答案才是 \(2\)。
- 第一阻塞点：在接受标准 Erdős–Rado 分割关系后证明已经闭合；唯一外部输入是 \((2^\mu)^+\to(\mu^+)^2_\mu\)，它立即蕴含所需的可数齐次集。
- 下一步：将该反例写成正式定理时，显式区分“任意指标族”与“可数序列”两种读法，并把 Erdős–Rado 关系作为唯一引用引理单独核验或形式化。
- 来源核对：[三页证明材料给出 Erdős–Rado 构造及全部交集计算](https://www.ulam.ai/research/erdos603.pdf)。；[官方讨论记录了解答及两种题意读法](https://www.erdosproblems.com/forum/thread/603)。；[官方修订历史确认当前题面要求每个集合可数无限](https://www.erdosproblems.com/history/603)。
- 时间记账：所在批次墙钟时间按题数均摊约 95.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/603)；既有候选答案（按不可信材料审计）

### #604

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given $n$ distinct points $A\subset\mathbb{R}^2$ must there be a point $x\in A$ such that\[\#\{ d(x,y) : y \in A\} \gg n^{1-o(1)}?\]Or even $\gg n/\sqrt{\log n}$?
- 题意摘要：对每个整数 n 和每个 n 点集 A⊂R²，问是否必存在 x∈A，使钉住距离数 d_A(x)=#{|x-y|:y∈A} 至少为 n^{1-o(1)}；更强地，是否存在绝对常数 c>0 使 d_A(x)≥cn/√log n。这里 o(1) 随 n→∞。
- 状态核对：仍开放。Katz–Tardos 的已知指数约为 0.864137，不能据此宣称接近线性结论。先前候选对状态和格点障碍的判断基本正确，但只是在综述已知结果，并非证明尝试。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用钉住距离能量。令 ν_x(t)=#{y∈A:|x-y|=t}、E_x=Σ_t ν_x(t)^2。Cauchy–Schwarz 给 d_A(x)E_x≥n²。再把总能量写成等腰三元组数 T=Σ_xE_x=n²+Σ_{y≠z}|A∩B(y,z)|，其中 B(y,z) 是 yz 的垂直平分线。目标于是归约为控制带重数的点—垂直平分线关联。
- 局部结论：精确地，max_x d_A(x)≥n³/T；因此若能证 T≤n^{2+o(1)}，就得到 n^{1-o(1)} 的目标。；更强的 n/√log n 结论可由 T≪n²√log n 推出；这明确标出了该能量路线所需的定量命题。；对 m×m 整数格点（n=m²），每个钉点的平方距离均为 a²+b²≤2m²。Landau–Ramanujan 计数给 d_A(x)=O(n/√log n)，故该尺度确为一致的上界障碍。
- 第一阻塞点：第一处缺口是证明 T≤n^{2+o(1)}，甚至 T≪n²√log n。普通点线关联定理不能直接做到，因为许多有序对 (y,z) 可产生同一条垂直平分线，权重高度集中；丢掉重数会遗漏主要项。
- 下一步：按垂直平分线重数 μ(ℓ) 分层，检验能否对每个 M 证明 Σ_{ℓ:M≤μ(ℓ)<2M} μ(ℓ)|A∩ℓ| 的统一界，并明确哪一层迫使使用 Katz–Tardos 的熵不等式。
- 来源核对：[Erdős Problems #604](https://www.erdosproblems.com/604) 于 2026-03-23 更新的条目仍列为 open，并记录 Katz–Tardos 指数及格点障碍。；未把 untrusted_prior_candidate 的文献综述视为证明。
- 时间记账：所在批次墙钟时间按题数均摊约 90.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/604)；既有候选答案（按不可信材料审计）

### #609

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the minimal $m$ such that if the edges of $K_{2^n+1}$ are coloured with $n$ colours then there must be a monochromatic odd cycle of length at most $m$. Estimate $f(n)$.
- 题意摘要：令 N=2^n+1。f(n) 是最小整数 m，使任意把 K_N 的边染成 n 色的染色，都含有某一颜色的奇圈 C_ℓ，其中 ℓ≤m。任务是估计 f(n) 随颜色数 n 的增长。
- 状态核对：仍开放；当前记录界为 2^{c√log n}≤f(n)≪n^{3/2}2^{n/2}。先前候选称下界“仍小于任意 n^ε”是不合法推论：下界函数是次多项式，并不意味着未知的 f(n) 本身有该上界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从每个颜色类的二分性编码入手。若所有颜色类均二分，对每种颜色任选一个二分划分，把每个顶点编码成其在 n 个划分中的侧向量 σ(v)∈{0,1}^n。随后尝试把“短奇圈均不存在”强化为一种近似侧向量编码。
- 局部结论：若所有颜色类都二分，则 σ 必为单射：若 σ(u)=σ(v)，边 uv 的颜色 i 会要求 u、v 位于第 i 个二分划分的异侧，矛盾。因此这种染色至多有 2^n 个顶点。；所以 K_{2^n+1} 的任意 n-染色至少有一个非二分颜色类，因而必含单色奇圈；这严格证明 f(n) 有限。；同一编码也给出 K_{2^n} 的无单色奇圈构造：以 {0,1}^n 为顶点，按两端首个不同坐标染色，每个颜色类二分。
- 第一阻塞点：第一处不能闭合之处是把“某颜色类非二分”转化为短奇圈。产生非二分性的颜色类可能极稀疏；另一方面，边数最大的颜色类虽有约 N²/n 条边，却完全可能是二分图。因此密度极值界与侧向量碰撞不能直接落在同一颜色上。
- 下一步：建立并检验一个稳定性引理：若每个颜色类的奇围长都大于 L，是否能删除总计少于一条边覆盖量的边，使所有颜色类同时二分；若能把所需删除量压到小于完整图边数，就可恢复侧向量矛盾并给出 L 的上界。
- 来源核对：[Erdős Problems #609](https://www.erdosproblems.com/609) 记录了 Day–Johnson 下界及 Janzer–Yip 上界，条目仍为 open。；独立核对了先前候选中的基本二分编码；没有接受其从次多项式下界推出 f(n) 次多项式的错误措辞。
- 时间记账：所在批次墙钟时间按题数均摊约 90.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/609)；既有候选答案（按不可信材料审计）

### #610

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：For a graph $G$ let $\tau(G)$ denote the minimal number of vertices that include at least one from each maximal clique of $G$ (sometimes called the clique transversal number). Estimate $\tau(G)$. In particular, is it true that if $G$ has $n$ vertices then\[\tau(G) \leq n-\omega(n)\sqrt{n}\]for some $\omega(n)\to \infty$, or even\[\tau(G) \leq n-c\sqrt{n\log n}\]for some absolute constant $c>0$?
- 题意摘要：约定只横截大小至少 2 的极大团。对所有 n 顶点图 G，求 τ(G) 的最坏情形；特别要证存在绝对 c>0，使 τ(G)≤n-c√(n log n)，从而也有 τ(G)≤n-ω(n)√n。
- 状态核对：已解决，且 cohort 标为 proved (Lean)。先前候选截至旧资料仍称开放，现已过时，必须明确否定。实际可得更精确的 max_{|V(G)|=n}τ(G)=n-Θ(√(n log n))。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 clique colouring 归约。设 χ_c(G)=q，即顶点可分成 q 个颜色类，且每个大小至少 2 的极大团至少使用两色。取最大颜色类 V_1，则其补集横截所有这些极大团。再代入 Joret–Micek–Reed–Smid 的 χ_c(G)≤A√(n/log n)。
- 局部结论：最大颜色类满足 |V_1|≥⌈n/q⌉，故严格有 τ(G)≤n-⌈n/χ_c(G)⌉。；代入 χ_c(G)≤A√(n/log n)，得到 τ(G)≤n-A^{-1}√(n log n)，常数和小 n 可统一调整。；若 G 是三角形自由图，则极大团（大小至少 2）恰为边，所以 τ(G)=n-α(G)。Kim 型图满足 α(G)=O(√(n log n))，给出相反方向 max τ(G)≥n-O(√(n log n))。
- 第一阻塞点：归约本身已闭合；唯一外部输入是 JMRS 的 clique chromatic number 定理及 Kim 的 Ramsey 构造。若要求完全自足或逐行复核 Lean，则需另行展开这两个深定理。官方页面虽显示 PROVED (LEAN)，同时仍显示“Formalised statement? No”，说明公开元数据存在接口不同步，不能仅凭该字段定位形式化文件。
- 下一步：取得对应 Lean artifact 的仓库与 commit，核对其形式化对象是否明确排除孤立点，并确认形式化的是上述归约还是连同 JMRS 渐近定理的完整实例化。
- 来源核对：[Erdős Problems #610](https://www.erdosproblems.com/610) 明确标为 PROVED (LEAN)，并给出 JMRS→横截集的归约。；[A note on the clique-transversal number](https://www.ulam.ai/research/erdos610.pdf) 给出完整的一页归约及 Kim 构造下界，结论为 n-Θ(√(n log n))。
- 时间记账：所在批次墙钟时间按题数均摊约 90.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/610)；既有候选答案（按不可信材料审计）

### #611

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For a graph $G$ let $\tau(G)$ denote the minimal number of vertices that include at least one from each maximal clique of $G$ (sometimes called the clique transversal number). Is it true that if all maximal cliques in $G$ have at least $cn$ vertices then $\tau(G)=o_c(n)$? Similarly, estimate for $c>0$ the minimal $k_c(n)$ such that if every maximal clique in $G$ has at least $k_c(n)$ vertices then $\tau(G)<(1-c)n$.
- 题意摘要：固定密度参数 c>0（实质上 0<c<1）。第一问量词为：是否对每个固定 c，所有 n 顶点图只要每个极大团大小至少 cn，就一致满足 τ(G)/n→0？第二问定义最小阈值 k_c(n)，使上述最小极大团条件蕴含 τ(G)<(1-c)n。
- 状态核对：仍开放。已知一般估计只给线性横截集，不能推出 o_c(n)。先前候选的 τ≤n-k+1 是正确的集合论观察，但不足以解决任一核心渐近问题。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：把极大团族视为秩至少 k 的超图并尝试随机横截：每个顶点以概率 p 入选；一个大小至少 k 的极大团被漏掉的概率至多 e^{-pk}。用极大团数至多 3^{n/3} 作并合估计。
- 局部结论：确定性地，任取 n-k+1 个顶点都横截所有大小至少 k 的极大团，因为其补集只有 k-1 个顶点；故 τ(G)≤n-k+1。特别地 k=cn 时仅得 τ(G)≤(1-c)n+1。；随机路线要求 e^{-pk}3^{n/3}<1，即 p≳n/k。若 k=cn，只得到常数 p，横截集仍为 Θ_c(n)，无法得到 o(n)。；按官方记录的 EGT 界 τ(G)≤n-√(kn)（端点处需按原文作整数修正），取 k略大于c²n 可推出 k_c(n)=O_c(n)；已知构造则给 k_c(n)≥n^{c'/log log n}。
- 第一阻塞点：第一处缺口是极大团族的结构性计数：Moon–Moser 的指数级上界使并合界必然选择常数概率。要得到 o(n)，必须证明“大极大团”条件显著降低有效团数，或证明这些团之间存在可利用的强重叠；现有路线没有这种引理。
- 下一步：固定 c 后计算或证明极值量 M_c(n)=max #{极大团 K:|K|≥cn} 的指数率；若 log M_c(n)=o(n)，则取 p=(log M_c(n)+ω(1))/(cn)=o(1) 可直接产生 o(n) 横截集。
- 来源核对：[Erdős Problems #611](https://www.erdosproblems.com/611) 仍列为 open，并记录 EGT 的上下界及 τ=1 的极端阈值。；对先前候选的“任意 n-k+1 点均横截”独立核验为正确，但其余已知界只作为外部定理使用。
- 时间记账：所在批次墙钟时间按题数均摊约 90.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/611)；既有候选答案（按不可信材料审计）

### #612

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a connected graph with $n$ vertices, minimum degree $d$, and diameter $D$. Show if that $G$ contains no $K_{2r}$ and $(r-1)(3r+2)\mid d$ then\[D\leq \frac{2(r-1)(3r+2)}{2r^2-1}\frac{n}{d}+O(1),\]and if $G$ contains no $K_{2r+1}$ and $3r-1 \mid d$ then\[D\leq \frac{3r-1}{r}\frac{n}{d}+O(1).\]
- 题意摘要：对固定整数 r，原命题含两部分：在相应整除条件下，分别要求所有连通 K_{2r}-free 图及所有连通 K_{2r+1}-free 图满足给定的 D=O(n/d) 常数界；O(1) 应对固定参数一致而不随 n 增长。
- 状态核对：整体不能按待证明命题处理：第一部分对每个 r≥2 已被反例否定；第二部分 r=1 已知成立，r≥2 在仅禁 K_{2r+1} 的条件下仍开放。因此网页的 open 标签只能理解为尚存的第二部分，而非两式都可能成立。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：第一部分核对 CSS 反例的常数并直接比较；第二部分重建 r=1 的测地线—邻域双计数证明。取直径测地线 v_0,…,v_D，并令 S_i=N[v_{2i}]∪N[v_{2i+1}]。
- 局部结论：CSS 构造的渐近系数为 B_r=(6r-5)/(2r-1)，原猜想系数为 A_r=2(r-1)(3r+2)/(2r²-1)，且 (6r-5)(2r²-1)-2(r-1)(3r+2)(2r-1)=1，所以 B_r>A_r。取充分大的、满足整除条件的 d 后得到真正反例。；当 r=1 时图无三角形。相邻 v_{2i},v_{2i+1} 的闭邻域交恰为这两个顶点，因此 |S_i|≥2d。；测地性保证每个顶点至多属于两个 S_i；故 2d⌊(D+1)/2⌋≤Σ_i|S_i|≤2n，从而 D≤2n/d+O(1)，正是第二式在 r=1 的情形。
- 第一阻塞点：第一式没有缺口而是被否证。对第二式 r≥2，邻接顶点可能有大量共同邻点，因而 |N[u]∪N[v]|≥2d 这一步立即失效；仅由 K_{2r+1}-free 无法给出所需的逐块邻域下界。
- 下一步：对第二式先攻 r=2：沿测地线把连续若干层组成块，精确求 K_5-free 条件下块内邻域并集的最小权重；用小规模整数规划搜索极端局部模板，再判断能否证明每个模板满足平均系数 5/2。
- 来源核对：[Erdős Problems #612](https://www.erdosproblems.com/612) 明载 CSS21 反例公式、修正版猜想以及第二部分的剩余状态。；已独立完成反例系数差的代数核算；先前候选给出的 r=1 双计数路线经检查可闭合。
- 时间记账：所在批次墙钟时间按题数均摊约 90.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/612)；既有候选答案（按不可信材料审计）

### #614

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n,k)$ be minimal such that there is a graph with $n$ vertices and $f(n,k)$ edges where every set of $k+2$ vertices induces a subgraph with maximum degree at least $k$. Determine $f(n,k)$.
- 题意摘要：对整数 n,k（非平凡情形 n≥k+2），f(n,k) 是满足下述性质的 n 顶点简单图 G 的最少边数：每个恰含 k+2 个顶点的集合 S 都满足 Δ(G[S])≥k。若 n<k+2，量词为空，故 f(n,k)=0。
- 状态核对：截至官方条目当前仍为 open。候选答案的补图变换基本正确，但只是把原问题等价改写成一个族的 Turán 数，并未“确定”一般的 f(n,k)。其普通子图禁形等价需要补上“取边极小生成子图”的论证。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：令 H=\overline G。对 |S|=k+2，有 deg_{G[S]}(v)+deg_{H[S]}(v)=k+1，故原条件等价于不存在 S 使 δ(H[S])≥2。令 \mathcal F_k 为所有顶点集大小 k+2、δ≥2 且对此性质边极小的图。若 H[S] 的最小度至少 2，逐边删除可得到一个生成的 F∈\mathcal F_k；反向显然。因此 H 必须在普通子图意义下 \mathcal F_k-free。
- 局部结论：严格得到 f(n,k)=\binom n2-\operatorname{ex}(n,\mathcal F_k)。这是等价归约，不是一般闭式解。；k=1 时 \mathcal F_1={K_3}，故由 Mantel 定理 f(n,1)=\binom n2-\lfloor n^2/4\rfloor；k=2 时边极小性给出 \mathcal F_2={C_4}，故 f(n,2)=\binom n2-\operatorname{ex}(n,C_4)。；固定 k≥2 时 K_{2,k}∈\mathcal F_k，故 \operatorname{ex}(n,\mathcal F_k)≤O_k(n^{3/2})，从而 f(n,k)≥\binom n2-O_k(n^{3/2})；另一方面任意森林都合格，故 f(n,k)≤\binom n2-(n-1)。
- 第一阻塞点：第一处实质缺口是求 \operatorname{ex}(n,\mathcal F_k)：即使 k=2 已包含尚无一般精确公式的 C4-Turán 问题。候选答案列出的 k=3 三个禁形尚需独立完成分类证明，不能仅凭列举接受。
- 下一步：对 k=3 做有限分类：枚举五顶点、最小度至少 2 的图，逐一删边至极小，核对是否恰为 C5、K_{2,3}、K_1\vee2K_2；随后用小 n 的无标号图枚举计算对应 Turán 数，作为可检验数据。
- 来源核对：[官方 #614](https://www.erdosproblems.com/614) 当前标为 OPEN，且未声称已有部分解。；独立检查确认候选补图等式正确；其“f=二项式−O(n^{3/2})”只能理解为距完全图至多一个 O 上界，未给出该误差的匹配下界。
- 时间记账：所在批次墙钟时间按题数均摊约 101.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/614)；既有候选答案（按不可信材料审计）

### #616

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 3$. For an $r$-uniform hypergraph $G$ let $\tau(G)$ denote the covering number (or transversal number), the minimum size of a set of vertices which includes at least one from each edge in $G$. Determine the best possible $t$ such that, if $G$ is an $r$-uniform hypergraph $G$ where every subgraph $G'$ on at most $3r-3$ vertices has $\tau(G')\leq 1$, we have $\tau(G)\leq t$.
- 题意摘要：对每个 r≥3，令 t(r) 为所有满足局部条件的 r-一致超图 G 的横截数 τ(G) 的最大可能值：凡边子族 G' 的全部顶点至多 3r−3 个，就必须有 τ(G')≤1，即该非空边族有公共顶点。要求确定最小的普适上界 t(r)。
- 状态核对：问题仍为 open。候选声称 τ(G)≤r−2，但关键的“可假设 e∩f_{ij}={v_i,v_j}”完全未证，不能接受。官方页面印出的 3r/16+7/8≤t≤r/5 若按所有 r≥3 逐字理解会矛盾（例如 r=3 时右端小于 1），显然缺少适用范围、取整或存在排版错误，引用前须查原论文。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：从小边族开始提取结构。两条边 e,f 的并至多 2r≤3r−3，故必须相交。若三条边 e,f,g 没有公共点，则由两两相交和容斥，|e∪f∪g|=3r-|e∩f|-|e∩g|-|f∩g|≤3r−3，于是局部条件又迫使三者有公共点，矛盾。因此每三条边都有公共点。固定任意两条边 e,f，则 I=e∩f 与每条边相交，故 I 是一个横截。路线转化为寻找交集很小的一对边。
- 局部结论：G 是两两相交族。；事实上 G 是三重相交族：任意三条边的总交非空。；对任意 e,f，e∩f 都是全局横截，因而 τ(G)≤min_{e,f}|e∩f|（只有一条边时 τ=1）。
- 第一阻塞点：需要由完整的 3r−3 局部条件推出存在一对边满足 |e∩f|约至多 r/5。三重相交本身远不足以给出这个常数。候选答案恰在此跳步；它既未证明交集可从单点强化为指定的两点，也没有处理 r=3 或没有两对不交指标的情形。
- 下一步：取一个最小横截 T⊆e∩f。对每个 x∈T 选见证边 g_x，使 g_x∩T={x}；系统写出三重相交对 g_x,g_y,e 及 g_x,g_y,f 强迫的交点，并双计数这些位于 (e∪f)\T 的交点。这是检验能否重建 EHT 上界常数的下一步。
- 来源核对：[官方 #616](https://www.erdosproblems.com/616) 当前标为 OPEN，并把上下界归于 EHT91。；官方网页所印上下界对小 r 数值不相容；未取得原论文正文前，不把该公式当作无条件逐点命题。
- 时间记账：所在批次墙钟时间按题数均摊约 101.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/616)；既有候选答案（按不可信材料审计）

### #619

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：For a triangle-free graph $G$ let $h_r(G)$ be the smallest number of edges that need to be added to $G$ so that it has diameter $r$ (while preserving the property of being triangle-free). Is it true that there exists a constant $c>0$ such that if $G$ is a connected graph on $n$ vertices then $h_4(G)<(1-c)n$?
- 题意摘要：正确量词应为：是否存在绝对常数 c>0，使每个有限、连通、无三角形的 n 顶点图 G，都能添加少于 (1−c)n 条边，得到仍无三角形且直径至多 4 的同顶点超图。这里 h_4(G) 是最少新增边数。
- 状态核对：该问题已于 2026 年被否定并以 Lean 验证。候选答案称其仍开放，已经过时，必须弃用。原文字“直径为 4”及末句漏写 triangle-free 存在歧义；正式化采用“直径至多 4”和连通无三角形 G。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建反例路线：取 m 顶点、最大度 d、独立数 α(H)≪(m/d)log d 的连通无三角形核心 H；给每个核心顶点挂 s 个叶子，得 G，n=(s+1)m。对任意无三角形、直径至多 4 的超图 G'⊇G，设新增边数为 t，并考察叶子诱导图中没有新增边连向核心的分支分量族 \mathcal C。新增的叶间边及核心—叶边计数迫使 t≥sm-|\mathcal C|。再用直径条件把每对这样的分量编码为 H 中距离至多 2 的一对核心点。
- 局部结论：挂叶构造保持连通性和无三角形性，且 n=(s+1)m。；若 \mathcal C 如上，则对叶子诱导图各分量取生成森林，并给每个不属于 \mathcal C 的分量计一条新增核心边，可严格得到 t≥sm-|\mathcal C|。；直径至多 4 迫使任意两个 \mathcal C-分量通过核心形成很短的连接；考虑每个核心仅有 s 个原始叶子，可归约为 |\mathcal C|^2受 s^2 倍“核心中距离≤2的点对数”控制。
- 第一阻塞点：在不直接调用已形式化证明时，第一处尚未于此处闭合的是核心点对引理：证明在保持无三角形的前提下，添加至多 n 条边只能把距离≤2的核心点对增加 O(nα(H)) 个。该引理结合原有 O(md^2) 点对才给出最终参数优化。
- 下一步：逐行核对 Lean 证明中的核心点对引理及其映射到上述组合对象；之后代入 d≈(n log n)^{1/3}、m≈n^{8/9}(log n)^{2/9}，复核 h_4(G)≥n−O(n^{8/9}(log n)^{2/9})。
- 来源核对：[官方 #619](https://www.erdosproblems.com/619) 明确记录否定解及 h_4(G)≥n−O(n^{8/9}(log n)^{2/9})。；[讨论中的构造概要](https://www.erdosproblems.com/forum/thread/619) 给出无三角形核心加叶子、分量计数和参数优化。；[Formal Conjectures 的 619 文件](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/619.lean) 将结论形式化为 answer(False)，并链接实际 Lean 证明；仓库展示页的声明本身含 sorry，因此可信依据是其链接的完整证明及官方状态，而不是这段占位声明。
- 时间记账：所在批次墙钟时间按题数均摊约 101.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/619)；既有候选答案（按不可信材料审计）

### #620

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G$ is a graph on $n$ vertices without a $K_4$ then how large a triangle-free induced subgraph must $G$ contain?
- 题意摘要：定义 f(n)=min_G max{|S|:G[S]无三角形}，其中最小值遍历所有 n 顶点 K4-free 简单图 G，且要求的是诱导子图。问题是确定 f(n) 的数量级及对数因子。
- 状态核对：仍为 open；已知 f(n)=n^{1/2+o(1)}。候选的初等 √n 论证正确，但它把已知下界写成 Ω(√(n log n/loglog n))，比官方记录的 √(n log n)/loglog n 强一个 √(loglog n) 因子，不能接受。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：按最大度 Δ 分情形。取度为 Δ 的顶点 v。由于 G 无 K4，N(v) 中不可能有三角形，所以 G[N(v)] 是 Δ 顶点的诱导无三角形子图。另一方面贪心独立集给出 α(G)≥⌈n/(Δ+1)⌉，独立集也是诱导无三角形子图。
- 局部结论：每个 K4-free 图都含大小至少 max{Δ,⌈n/(Δ+1)⌉} 的诱导无三角形子图。；最小化上式得到 f(n)≥⌊√n⌋（差一个常数或取整不影响结论）。；官方记录的当前范围是 √n·√(log n)/(loglog n)≪f(n)≪√n log n，因此初等路线只捕获主幂指数，尚未产生对数增益。
- 第一阻塞点：最大度与普通贪心独立集只能平衡到 √n。要得到已知对数因子，必须利用 K4-free 图中邻域无三角形的更细稀疏结构及 Shearer 型独立集估计；候选没有给出该定理的准确版本，而且其下界公式与官方记录不一致。
- 下一步：查明并写出 Shearer 1995 中实际使用的精确引理（包括 loglog 的幂次和最大度假设），再对 Δ 分段优化；这是可以直接核验候选对数因子是否正确的任务。
- 来源核对：[官方 #620](https://www.erdosproblems.com/620) 当前给出的最佳范围为 √n·√(log n)/(loglog n)≪f(n)≪√n log n。；候选末段把官方下界的分母 loglog n 攁成了根号内部的 loglog n，二者不等价。
- 时间记账：所在批次墙钟时间按题数均摊约 101.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/620)；既有候选答案（按不可信材料审计）

### #623

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $X$ be a set of cardinality $\aleph_\omega$ and $f$ be a function from the finite subsets of $X$ to $X$ such that $f(A)\not\in A$ for all $A$. Must there exist an infinite $Y\subseteq X$ that is independent - that is, for all finite $B\subset Y$ we have $f(B)\not\in Y$?
- 题意摘要：量词为：对每个满足 |X|=ℵ_ω 的集合 X，以及每个函数 f:[X]^{<ω}→X，若对所有有限 A⊆X 都有 f(A)∉A，是否必存在一个无限 Y⊆X，使对所有有限 B⊆Y 都有 f(B)∉Y。B 包括空集，所以还要求 f(∅)∉Y。
- 状态核对：当前状态是 open，不是已知 independent。Erdős 说“perhaps undecidable”只是猜测，不能据此宣称 ZFC 独立。候选基本只复述状态，没有进行证明尝试。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试递归构造 Y={y_0,y_1,…}。若有限 A 已经独立，则加入 x 后的精确条件为：(i) x不属于{f(B):B⊆A}；(ii) 对每个 C⊆A，f(C∪{x})∉A；其中 f(C∪{x})≠x 由原假设自动成立。条件 (i) 只排除有限多个点，但条件 (ii) 涉及若干映射纤维，可能排除 X 的全部剩余部分，故朴素递归不能继续。
- 局部结论：任何独立 Y 必须避开 f(∅)；删除这一点不改变 |X|=ℵ_ω。；只看一元限制 g(x)=f({x}) 时，g 无不动点，其无向函数图可有限着色，故存在无限集合 Y 满足 g[Y]∩Y=∅；因此真正障碍来自二元及更高元同时约束。；上述 (i)、(ii) 是有限独立集 A 可扩张一个点的充要条件，准确定位了递归路线的失败处。
- 第一阻塞点：没有任何基数界控制坏点集合 {x:f(C∪{x})∈A}；仅由 f(D)∉D，它完全可能具有基数 ℵ_ω。必须利用跨越所有有限 ℵ_n 层级的自由集/集合映射结构，而普通的逐点避开有限集合论证无效。
- 下一步：固定分解 X=⋃_{n<ω}X_n、|X_n|=ℵ_n，尝试证明一个“层级扩张引理”：给定有限独立 A⊆X_n，是否可在某个 X_m\X_n 中找到 x 满足上述 (i)、(ii)；若失败，则从覆盖全部高层的坏纤维中明确提取 Erdős–Hajnal 的有限基数反例结构。
- 来源核对：[官方 #623](https://www.erdosproblems.com/623) 当前仍标为 OPEN；只记载 Erdős 对可能不可判定的猜测。；本地 Lean 陈述确实量化所有 Finset B，包括空集，并仍带 research open/sorry；它是陈述形式化，不是证明。
- 时间记账：所在批次墙钟时间按题数均摊约 101.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/623)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/623.lean`；既有候选答案（按不可信材料审计）

### #624

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $X$ be a finite set of size $n$ and $H(n)$ be such that there is a function $f:\{A : A\subseteq X\}\to X$ so that for every $Y\subseteq X$ with $\lvert Y\rvert \geq H(n)$ we have\[\{ f(A) : A\subseteq Y\}=X.\]Prove that\[H(n)-\log_2 n \to \infty.\]
- 题意摘要：对每个正整数 n，令 H(n) 为满足下述性质的最小整数 m：存在一个统一的映射 f:P(X)→X，使每个 |Y|≥m 的 Y⊆X 都满足 {f(A):A⊆Y}=X，其中 |X|=n。目标是证明 H(n)−log₂n→∞。
- 状态核对：截至冻结日期仍为开放问题。形式化文件也明确把 H 定义为最小 m；题面没有 f(A)∉A 条件。旧候选擅自加入该条件，且其“贪心自由集”论证无效：A 可以含有晚于 y_j 选取的元素，f(A)=y_j 并不推出某个 B⊆Y_{j−1} 满足 f(B)=y_j。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试推广 Alon 的碰撞法。固定任意 f。若 n=2^k，则全部二元集在 n 个像值中分桶；某桶至少含 C(n,2)/n=(n−1)/2 个二元集。任选 r=⌊k/2⌋ 个同像二元集，其并集至多有 2r≤k 个点，故可扩充为 k 元集 Y。
- 局部结论：在该 Y 的 2^k 个子集输入中，至少 r 个不同输入具有同一像，因此像集大小至多 2^k−r+1<2^k=n。；所以对 n=2^k 严格得到 H(2^k)≥k+1；这不需要任何 set-mapping 附加条件。；更一般地，用同像的 s 元集只能在一个 h 元 Y 内强制至多约 h/s 个显式碰撞，因而该朴素路线产生的亏损至多为 O(h)。
- 第一阻塞点：当 h=⌊log₂n⌋+C 且 n 不接近 2^h 时，需要克服的容量余量 2^h−n 可达 Θ(n)，而固定大小集合的朴素同像桶只能保证 O(log n) 个碰撞，无法证明任意固定 C 最终都不足。
- 下一步：检验“多层碰撞”版本：对每个 Y 定义亏损 D_f(Y)=2^|Y|−|f(P(Y))|，计算随机 h 元 Y 的 E[D_f(Y)]，看能否仅由各纤维 f^{-1}(x) 的层分布证明 max_Y D_f(Y)>2^h−n；第一目标是处理 h=⌊log₂n⌋+1。
- 来源核对：已核对本地 624.lean：H 确为最小阈值，且没有 f(A)∉A 假设。；官方页面仍标为 open，并记载 Alon 的 n=2^k 碰撞证明：https://www.erdosproblems.com/624
- 时间记账：所在批次墙钟时间按题数均摊约 94.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/624)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/624.lean`；既有候选答案（按不可信材料审计）

### #625

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：The cochromatic number of $G$, denoted by $\zeta(G)$, is the minimum number of colours needed to colour the vertices of $G$ such that each colour class induces either a complete graph or empty graph. Let $\chi(G)$ denote the chromatic number. If $G$ is a random graph with $n$ vertices and each edge included independently with probability $1/2$ then is it true that almost surely\[\chi(G) - \zeta(G) \to \infty\]as $n\to \infty$?
- 题意摘要：令 G∼G(n,1/2)。ζ(G) 是把 V(G) 分成最少若干块、每块诱导空图或完全图所需的块数。问题是：是否对每个固定 M 都有 P(χ(G)−ζ(G)≥M)→1？
- 状态核对：截至冻结日期仍未解决完整整数序列。已知约 95% 的 n 上有近线性下界，但这不能推出沿所有 n 的高概率收敛；旧候选在这一点上的结论基本正确。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：对 ζ 作直接一阶矩筛查。固定一个有序 t-分划，块大小为 s₁,…,s_t。每块成为团或独立集的概率至多 2^t·2^{−Σ_i C(s_i,2)}。把所有有序分划粗略计为至多 t^n 个，得到存在 t-共着色的期望上界 t^n2^t2^{−Σ_i C(s_i,2)}。
- 局部结论：由凸性，Σ_i C(s_i,2)≥n²/(2t)−n/2，因此 P(ζ(G)≤t)≤t^n2^{t−n²/(2t)+n/2}。；这个估计在 t≈n/(2log₂n) 附近出现主项抵消，正确地恢复 ζ 的一阶尺度，却不足以稳定识别 χ−ζ 的加性差。；由于 G 与补图同分布，团块和独立块在该计数中完全对称；只比较块的同质性不会自动提供 χ 的额外下界。
- 第一阻塞点：要证明差值发散，必须把 ζ 与 χ 的二阶项放在同一个高概率事件上比较；上述并合界在临界窗损失约 n log log n 量级，远大于所需的任意发散加性差。
- 下一步：对块大小集中在典型独立数附近的分划做截断二阶矩：先计算含 q 个团块、t−q 个独立块的精确期望，再验证非典型块型的总贡献是否可忽略。可检验目标是先排除 ζ≤χ−1 没有意义，应改为在 Heckel 未覆盖的 n 上证明 ζ≤χ−M(n)，其中 M(n)→∞。
- 来源核对：官方页面确认完整问题仍 open，并列出约 95% 整数上的结果：https://www.erdosproblems.com/625；Heckel 论文摘要只声称对约 95% 的 n 给出肯定答案：https://arxiv.org/abs/2409.17614；Heckel 与 Steiner 的较弱结果确实只排除统一的低阶高概率上界，不能推出全序列发散：https://arxiv.org/abs/2408.13839；https://arxiv.org/abs/2408.02400
- 时间记账：所在批次墙钟时间按题数均摊约 94.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/625)；既有候选答案（按不可信材料审计）

### #626

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 4$ and $g_k(n)$ denote the largest $m$ such that there is a graph on $n$ vertices with chromatic number $k$ and girth $>m$ (i.e. contains no cycle of length $\leq m$). Does\[\lim_{n\to \infty}\frac{g_k(n)}{\log n}\]exist? Conversely, if $h^{(m)}(n)$ is the maximal chromatic number of a graph on $n$ vertices with girth $>m$ then does\[\lim_{n\to \infty}\frac{\log h^{(m)}(n)}{\log n}\]exist, and what is its value?
- 题意摘要：第一问对每个固定 k≥4，g_k(n) 是恰有 n 个顶点、χ(G)=k 的图所能达到的最大无短圈阈值 m，问 g_k(n)/log n 是否收敛。第二问对每个固定 m，h^(m)(n) 是 n 顶点、围长大于 m 的图的最大色数，问 log h^(m)(n)/log n 是否收敛并求其值。
- 状态核对：两个一般性极限仍开放。旧候选列出的数量级及 m=3 的基准结论合理，但没有给出能迫使极限存在的结构。官方背景中涉及尚未证明存在的极限时，应审慎理解为 liminf/limsup 型界。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试用临界子图、Moore 界和填充操作建立近次可加性。任一 k-色图含 k-临界子图 H，故 δ(H)≥k−1；对 H 作无碰撞 BFS 展开可控制其围长。另一方面，给图添加孤立点不改变色数或围长。
- 局部结论：标准 Moore 展开给出 |V(H)|≥(k−2)^{(g(H)−1)/2}，从而 g_k(n)≤2log n/log(k−2)+1。；添加孤立点表明 g_k(n) 与 h^(m)(n) 均关于 n 单调不减，并且 h^(m)(n)≥k 当且仅当 g_k(n)>m。；不交并只能给 g_k(n₁+n₂)≥min(g_k(n₁),g_k(n₂))；它没有产生可供 Fekete 引理使用的加法或乘法关系。
- 第一阻塞点：自然的放大操作均不闭合：覆盖图可能降低色数，词典积或顶点替换通常制造短圈，而不交并只保留两个围长的最小值。因此无法从单调性推出任一归一化极限存在；两个极值函数的点态逆关系也缺少 k、m 同时增长时的统一误差控制。
- 下一步：寻找保持 χ=k 的高围长 lift：固定一个 k-临界底图，枚举随机 N-lift，检验是否能同时证明围长≥c log N 且仍不可 (k−1)-着色。若能得到可迭代、损失 O(1) 的 lift，便可能建立 g_k(Nn)≥g_k(n)+c log N−O(1)。
- 来源核对：官方页面确认一般极限仍 open，并给出 Kostochka–Erdős 上下界：https://www.erdosproblems.com/626；旧候选对 m=3 的陈述与三角形自由 Ramsey 渐近相容，但它只是特例，不能回答一般 m。
- 时间记账：所在批次墙钟时间按题数均摊约 94.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/626)；既有候选答案（按不可信材料审计）

### #627

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\omega(G)$ denote the clique number of $G$ and $\chi(G)$ the chromatic number. If $f(n)$ is the maximum value of $\chi(G)/\omega(G)$, as $G$ ranges over all graphs on $n$ vertices, then does\[\lim_{n\to\infty}\frac{f(n)}{n/(\log n)^2}\]exist?
- 题意摘要：对每个 n，在所有 n 顶点简单图中取 f(n)=max χ(G)/ω(G)。问题是归一化量 f(n)/(n/(log n)^2) 是否有极限；常数随对数底改变，官方常数区间以自然对数理解为 (ln2)^2·[1/4,1]。
- 状态核对：冻结状态为开放。2025 年底的后续论文改进了上界常数，但其摘要没有宣称解决极限存在性。旧候选引用该论文作“仍开放”的证据可接受，但其中更精细的 liminf/limsup 等式不能仅凭摘要确认。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先检验随机图能否给出稳定下界，再尝试寻找缩放结构。对 G(n,1/2)，典型地 χ(G)∼n/(2log₂n)、ω(G)∼2log₂n，因此 χ/ω∼n/(4(log₂n)^2)。
- 局部结论：换成自然对数归一化，随机图给出 liminf f(n)/(n/(ln n)^2)≥(ln2)^2/4。；添加孤立点说明 f(n) 单调不减，但 n/(log n)^2 的归一化会把这种单调性破坏，故不能排除振荡。；不交并、团吹胀和词典积均不能给 χ/ω 一个精确乘法公式；尤其团吹胀涉及多重着色数，不能直接建立归一化量的次可加性。
- 第一阻塞点：上界优化实质依赖 Ramsey 数在不同参数比例下的精细渐近，以及把大独立集反复剥离成接近最优着色的统一估计。现有 Ramsey 指数常数本身没有已知极限，因而该路线无法证明 f(n) 的归一化极限。
- 下一步：把问题化为一个明确的 Ramsey 稳定性命题：对所有诱导子图 H，给出 α(H) 的统一下界并积分贪心剥离过程；随后检查若对角及近对角 Ramsey 指数存在统一极限，是否足以推出 f(n) 的极限，而不额外假设多重着色稳定性。
- 来源核对：官方页面当前仍标为 open：https://www.erdosproblems.com/627；Araujo–Filipe–Miyazaki 的摘要确认上界常数由 4 改进到小于 3.72，但未声称极限存在：https://arxiv.org/abs/2512.16062
- 时间记账：所在批次墙钟时间按题数均摊约 94.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/627)；既有候选答案（按不可信材料审计）

### #629

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：The list chromatic number $\chi_L(G)$ is defined to be the minimal $k$ such that for any assignment of a list of $k$ colours to each vertex of $G$ (perhaps different lists for different vertices) a colouring of each vertex by a colour on its list can be chosen such that adjacent vertices receive distinct colours. Determine the minimal number of vertices $n(k)$ of a bipartite graph $G$ such that $\chi_L(G)>k$.
- 题意摘要：对每个正整数 k，n(k)=min{|V(G)|：G 为二分图且 χ_L(G)>k}；也就是最小的不具 k-可选性的二分图阶数。要求确定整个函数 n(k)，而非只找某个见证图。
- 状态核对：一般 k 仍开放，已知 n(2)=6、n(3)=14。旧候选的“m(k)≤n(k)≤2m(k)”本身可由其构造证明，但不是官方给出的更强比较；ERT 的界是 m(k)≤n(k)≤m(k+1)。因此不能把因子 2 比较冒充关键最佳归约。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先对任意二分图及任意 k-列表赋值作随机颜色二分。独立地把全体颜色染红或蓝，各以概率 1/2。设二分部为 L、R；L 中顶点需要列表含红色，R 中顶点需要列表含蓝色。
- 局部结论：每个顶点失败的概率为 2^{-k}；若 |V(G)|<2^k，并合界给总失败概率小于 1，因此存在一种颜色二分使所有顶点成功。；从每个 L 顶点列表选红色、每个 R 顶点列表选蓝色，即得合法列表着色。因此严格推出 n(k)≥2^k。；若 F 是含 m(k) 个 k-集的最小非 Property-B 族，把 F 的各集合分别作为 K_{m(k),m(k)} 两侧的列表，则任何合法着色都会给出 F 的 Property-B 分割，矛盾；故 n(k)≤2m(k)。
- 第一阻塞点：随机二分只利用单个列表完全落在错误颜色侧的事件，无法产生已知的额外 √(k/log k) 因子；进一步改进正好进入非 Property-B k-一致超图的依赖结构，而上界构造也受 m(k) 的未定渐近控制。
- 下一步：对随机二分法应用熵压缩或局部引理，显式利用同一颜色在多个列表中的重叠。最先可检验的有限任务是把 k=4、N=15,…,39 的非 k-可选性编码为 SAT，结合二分部大小和列表同构消去，尝试缩小由递推给出的 n(4)≤40。
- 来源核对：官方页面确认 ERT 的准确比较为 m(k)≤n(k)≤m(k+1)，并列出 n(2)=6、n(3)=14 及递推式：https://www.erdosproblems.com/629；旧候选的 K_{m,m} 论证仅给 n(k)≤2m(k)，虽正确但弱于官方归约；其“可假设极值图为完全二分图”只表示可补边，不代表两侧必须等大。
- 时间记账：所在批次墙钟时间按题数均摊约 94.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/629)；既有候选答案（按不可信材料审计）

### #635

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $t\geq 1$ and $A\subseteq \{1,\ldots,N\}$ be such that whenever $a,b\in A$ with $b-a\geq t$ we have $b-a\nmid b$. How large can $\lvert A\rvert$ be? Is it true that\[\lvert A\rvert \leq \left(\frac{1}{2}+o_t(1)\right)N?\]
- 题意摘要：固定整数 t≥1；对每个 N，考察 A⊆[N]，要求任意 a<b 属于 A 且 b−a≥t 时，均有 b−a∤b。问题既问最大值 F_t(N) 的精确阶，也问固定 t、N→∞ 时是否 F_t(N)≤(1/2+o_t(1))N。
- 状态核对：整体精确极值仍开放，但第二个渐近子问在输入日期之后已有肯定路线。先前候选所称“Ruzsa 已给出 N/2+O_t(N/log N)”未找到可靠依据，且与 Tao 所述现有方法仅给很慢的 o(1) 相冲突，不能采用。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：令 f=1_A，并取素数 p≥t。集合 B_p={m≤N/p:pm∈A} 不含相邻整数；再用 Elliott 采样不等式比较 A 的全局密度与其在 p 的倍数上的密度，并对许多素数求和。
- 局部结论：违例恰为一对 kd,(k+1)d，其中 d≥t；故对每个 d≥t，A 在 d,2d,…,⌊N/d⌋d 上至多取 ⌈⌊N/d⌋/2⌉ 个点。；特别地，对每个素数 t≤p≤N^{0.1}，有 (p/N)∑_{p|n}1_A(n)≤1/2+O(p/N)。；Elliott 不等式给出这些采样密度与 α=|A|/N 的加权平方偏差总和 O(α)。若 α≥1/2+δ，结合 ∑_{t≤p≤N^{0.1}}1/p→∞ 即迫使 δ=o_t(1)，从而严格推出 |A|≤(1/2+o_t(1))N。该路线不确定的只是误差优化，不影响 o_t(1)。
- 第一阻塞点：该方法不能逼近已知 t=2 构造所显示的 O(log N) 级次项；Elliott 型二阶矩只产生缓慢衰减的 o_t(1)，无法推出先前候选声称的 O_t(N/log N)，更无法确定 F_t(N)−N/2 的真实阶。
- 下一步：把 Elliott 不等式代入 f=1_A 的常数和端点误差完整写出，得到一个显式误差（例如 O_t(N/√log log N) 量级），再检查能否通过分块或迭代采样改善；这是可逐行核验的下一步。
- 来源核对：[官方条目：整体仍 open、第二子问已有肯定解](https://www.erdosproblems.com/635)；[官方讨论：Tao 指出 Elliott 路线及其定量局限](https://www.erdosproblems.com/forum/thread/635)；[Tao 讲义中的 Elliott 采样不等式](https://terrytao.wordpress.com/2019/11/12/254a-notes-9-second-moment-and-entropy-methods/)
- 时间记账：所在批次墙钟时间按题数均摊约 100.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/635)；既有候选答案（按不可信材料审计）

### #638

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $S$ be a family of finite graphs such that for every $n$ there is some $G_n\in S$ such that if the edges of $G_n$ are coloured with $n$ colours then there is a monochromatic triangle. Is it true that for every infinite cardinal $\aleph$ there is a graph $G$ of which every finite subgraph is in $S$ and if the edges of $G$ are coloured with $\aleph$ many colours then there is a monochromatic triangle.
- 题意摘要：给定有限图族 S，假设对每个正整数 n，都存在 G_n∈S，使每个映射 E(G_n)→{1,…,n} 都产生单色三角形。所问是：对每个无限基数 κ，是否存在某图 G，使 G 的每个有限子图（按同构）均属于 S，且每个 κ-边着色 E(G)→κ 都产生单色三角形。
- 状态核对：按字面量词命题为假；数据库仍标 open，是因为原意很可能漏写了对 S 的闭包/年龄条件。先前候选的稀疏完全图反例正确，但其“于是 G 必为无边图”还应补充：即使无边图的有限子图未必属于 S，也已足以说明任何满足该条件的 G 不可能具有所需 Ramsey 性质。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：取 S={K_{R_3(n)}:n≥1}，其中 R_3(n) 是 n 色三角形 Ramsey 数，直接检验前提与结论。
- 局部结论：对每个 n，K_{R_3(n)}∈S 且任意 n-边着色含单色 K_3，所以前提成立。；若 G 的每个有限子图都属于 S，而 G 有边，则该边给出有限子图 K_2；但 K_2∉S，矛盾。因此任何候选 G 都无边。；无边图没有三角形，故其任意 κ-着色都不可能产生单色三角形；字面命题被反驳。
- 第一阻塞点：反例已经闭合；真正障碍是原题语义不完整。若额外规定 S 遗传，必须重新研究，不能把上述反例冒充为对预期版本的解决。2026 年讨论中的更强反例稿仍含未形式化的稀疏 Ramsey 输入，不能在本筛查中视为定理。
- 下一步：从 Erdős 原始出处核定“every finite subgraph is in S”是否隐含 S 为遗传类或 S 为某个图的 age；随后对精确的加强版本单独立题。
- 来源核对：[官方条目承认缺少闭包时有平凡反例](https://www.erdosproblems.com/638)；[官方讨论及尚未完全形式化的加强反例声明](https://www.erdosproblems.com/forum/thread/638)
- 时间记账：所在批次墙钟时间按题数均摊约 100.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/638)；既有候选答案（按不可信材料审计）

### #640

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some function $f$ such that for all $k\geq 3$ if a finite graph $G$ has chromatic number $\geq f(k)$ then $G$ must contain some odd cycle whose vertices span a graph of chromatic number $\geq k$?
- 题意摘要：问是否存在单一函数 f，使对每个整数 k≥3、每个有限图 G，只要 χ(G)≥f(k)，就存在一个奇圈 C（不要求诱导），使其顶点集诱导出的图 G[V(C)] 满足 χ(G[V(C)])≥k。
- 状态核对：仍开放。必须区分“C 是诱导奇圈”和“C 的顶点所张成的图”：若误读为诱导奇圈，则其色数恒为 3。先前候选在这一点上的最终重述基本正确。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试经 BFS 分层把高色数集中到一层，再调用“路径顶点张成高色数子图”的版本，并把层内路径与到根的最短路闭合成奇圈。
- 局部结论：k=3 完全闭合：χ(G)≥3 意味着 G 非二部，故含奇圈 C，而 G[V(C)] 非二部，所以 χ(G[V(C)])≥3；可取 f(3)=3。；若 G 连通且按距根距离分层 L_i，则不同且同奇偶的层之间无边；因此 χ(G)≤2 max_i χ(G[L_i])。故 χ(G)≥2r−1 时某层的色数至少 r。；在某层中，连接任意两点到根的最短路在首次汇合处截断后，两条树路长度相同；因此若层内连接两端的路径长度为奇数，闭合所得圈为奇圈。
- 第一阻塞点：第一处不能严格闭合的是：从 χ(G[L_i]) 很大得到一条层内路径 P，使 χ(G[V(P)])≥k，并同时选择/截短 P 保持足够色数且长度为奇数。这个“路径版本”本身正是等价的开放核心，不能作为已证引理调用。
- 下一步：精确证明并核查路径版到奇圈版的转换常数：从 χ≥2g(k+1)−1 开始，逐项验证删去路径端点后色数至多下降 1、奇偶选择及闭合后 V(P) 仍包含于圈顶点集。
- 来源核对：[官方条目及 k=3、路径版等价性说明](https://www.erdosproblems.com/640)；[官方讨论中的 BFS 转换草图](https://www.erdosproblems.com/forum/thread/640)
- 时间记账：所在批次墙钟时间按题数均摊约 100.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/640)；既有候选答案（按不可信材料审计）

### #642

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the maximal number of edges in a graph on $n$ vertices such that all cycles have more vertices than diagonals. Is it true that $f(n)\ll n$?
- 题意摘要：在 n 顶点有限简单图中，要求每个圈 C 的弦数严格小于 |V(C)|；f(n) 是满足条件图的最大边数。问是否存在绝对常数 C 使 f(n)≤Cn。
- 状态核对：仍开放；已知上界为 O(n(log n)^8)。先前候选的 K_{3,n−3} 线性下界可直接核验，成立。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先把条件改写成圈顶点集上的边数约束，再按 2-连通块分解；若能对每个 admissible 的 2-连通块证明统一线性边界，即可推出全图线性。
- 局部结论：对圈 C，弦数=e(G[V(C)])−|C|，所以条件等价于 e(G[V(C)])<2|C|。注意这只约束确实承载该圈的顶点集，并不约束所有顶点子集。；所有圈都位于某个 2-连通块；且各块满足 ∑_B(|V(B)|−1)≤n−1。因此若每个块满足 e(B)≤C(|V(B)|−1)，立即有 e(G)≤C(n−1)。；K_{3,n−3} 有 3n−9 条边。其圈长度仅为 4 或 6；对长度 2r 的圈，r≤3，弦数为 r²−2r，分别为 0 或 3，均小于 2r。因此 f(n)≥3n−9。
- 第一阻塞点：耳分解或最长路论证不能保证某一个圈的顶点集同时捕获块中足够多的边；高平均度可能分散在许多圈上。这正是从块的高密度推出 e(G[V(C)])≥2|C| 的首个未闭合步骤，也是现有证明需使用几乎正则扩张子图和随机游走的原因。
- 下一步：先检验局部命题：“每个满足条件的 2-连通图是否含度数至多某个绝对常数的顶点”。可枚举小阶图寻找反例；若命题成立则由递归删点直接给线性上界，若失败则分析最小反例的耳结构。
- 来源核对：[官方条目及 O(n(log n)^8) 上界](https://www.erdosproblems.com/642)；[Draganić–Methuku–Munhá Correia–Sudakov 原论文预印本](https://arxiv.org/abs/2306.09157)
- 时间记账：所在批次墙钟时间按题数均摊约 100.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/642)；既有候选答案（按不可信材料审计）

### #643

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n;t)$ be minimal such that if a $t$-uniform hypergraph on $n$ vertices contains at least $f(n;t)$ edges then there must be four edges $A,B,C,D$ such that\[A\cup B= C\cup D\]and\[A\cap B=C\cap D=\emptyset.\]Estimate $f(n;t)$ - in particular, is it true that for $t\geq 3$\[f(n;t)=(1+o(1))\binom{n}{t-1}?\]
- 题意摘要：对 n 顶点 t-一致超图，禁止四条互异边 A,B,C,D，使 A、B 不交，C、D 不交，且两对的并相同。题面 f(n;t) 定义为“至少 f 条边即必出现配置”的最小阈值；固定 t≥3 时问其是否渐近于 binom(n,t−1)。
- 状态核对：仍开放，但存在记号偏差：原论文以 f_t(n) 表示无禁形超图的最大边数，而题面把 f 写成强迫阈值。若记极值数为 g(n,t)，严格地有阈值 F(n,t)=g(n,t)+1；渐近式不受这个 +1 影响。先前候选正确注意到该点，但引用精确上下界时必须统一记号。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把每个无序不交边对 {A,B} 映到其 2t 元并 A∪B；禁形条件正是该映射单射。随后检验“全星加匹配”的下界，并尝试用交叠结构稳定性控制非星边。
- 局部结论：取固定顶点 x，加入所有含 x 的 t-集，再在其余 n−1 个点上加入大小 ⌊(n−1)/t⌋ 的匹配 M。任何不交边对必由一条星边和一条 M 中边组成。；若两个这样的不交对有相同并，且使用不同匹配边 M_1,M_2，则 M_1∪M_2 已有 2t 个点却还必须包含 x，矛盾；若使用同一匹配边，则其补集星边也相同。因此该构造无禁形，给出 g(n,t)≥binom(n−1,t−1)+⌊(n−1)/t⌋，题面阈值还应再加 1。；禁形等价于不交边对的并集映射为单射；这是一个正确的编码归约，但直接计数只给 #不交边对≤binom(n,2t)，对星形集族过弱。
- 第一阻塞点：第一处失败在于从并集映射单射推出 m≤(1+o(1))binom(n,t−1)：接近全星的族中绝大多数边对相交，故不交对计数几乎看不到 m。必须先证明稳定性——大族要集中在某个顶点的星附近——而这正是尚未获得常数 1 的核心。
- 下一步：证明一个可检验的近星命题：若某顶点度数至少 (1−ε)binom(n−1,t−1)，则所有不含该点的边至多 O_t(ε n^{t−1}+n)。先从 t=3 写成交叉不交图并核验；成功后可封闭“最大度数高”的情形。
- 来源核对：[官方条目及 Füredi、Pikhurko–Verstraëte 已知界](https://www.erdosproblems.com/643)；[Pikhurko–Verstraëte 原论文 PDF](https://mathweb.ucsd.edu/~jverstra/generalizedc4.pdf)
- 时间记账：所在批次墙钟时间按题数均摊约 100.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/643)；既有候选答案（按不可信材料审计）

### #644

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(k,r)$ be minimal such that if $A_1,A_2,\ldots$ is a family of sets, all of size $k$, such that for every collection of $r$ of the $A_is$ there is some pair $\{x,y\}$ which intersects all of the $A_j$, then there is some set of size $f(k,r)$ which intersects all of the sets $A_i$. Is it true that\[f(k,7)=(1+o(1))\frac{3}{4}k?\]Is it true that for any $r\geq 3$ there exists some constant $c_r$ such that\[f(k,r)=(1+o(1))c_rk?\]
- 题意摘要：把族视为至少含 r 条边的 k-一致超图 H。假设任取 r 条边所得子超图的横截数均不超过 2；f(k,r) 是所有此类 H 的全局横截数 τ(H) 的最大可能值。问题分别问 f(k,7)/k→3/4，以及对每个固定 r≥3，f(k,r)/k 是否有正有限极限 c_r。
- 状态核对：截至核查仍为开放。旧候选给出的 3/4 下界和 7/8 上界确有文献依据，但一般极限的存在不能由 O_r(k) 推出。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：检验完全超图下界。取 n<rk/(r-3) 且 n<2k，在 [n] 上取全部 k-子集。任取 r 条边，度数总和为 rk>(r-3)n，故某顶点属于至少 r-2 条边；余下至多两条边因 n<2k 必相交，再取其交点，即得二点横截。该超图的 τ=n-k+1。
- 局部结论：对 r≥7，令 n=⌈rk/(r-3)⌉-1，可得 f(k,r)≥n-k+1=(3/(r-3))k+O(1)；r=7 时为 3k/4+O(1)。；若 H 有 r 条两两不交的边，则这 r 条边不可能被两点击中，故 ν(H)≤r-1；极大匹配所有顶点构成横截，因而 f(k,r)≤(r-1)k。；文献还证明 f(4m,7)≥3m+1（m≥10）及 f(k,7)≤⌈7k/8⌉；前者比完全超图只改善常数项。
- 第一阻塞点：要得到 3/4 上界，必须把任意满足局部 (7,2) 条件的超图压到 τ≤(3/4+o(1))k；上述最大匹配论证只给 6k，1999 年的精细结构分析也停在 7k/8。对一般 r，也没有已证的次可加性或缩放不等式来保证 f(k,r)/k 收敛。
- 下一步：先检验一个明确的“近次可加性”命题：固定 r，是否存在 C_r 使 f(k+ℓ,r)≤f(k,r)+f(ℓ,r)+C_r；若成立，Fekete 型论证可处理极限存在性。首要小任务是对 ℓ=1 尝试构造从 (k+1)-边到 k-边的删点映射，并搜索小型反例。
- 来源核对：[官方问题页](https://www.erdosproblems.com/644)仍标为 open，并记录 r=3,4,5,6 的精确值。；[Fon-Der-Flaass–Kostochka–Woodall 论文](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf)明确给出 f(4m,7)≥3m+1 与 f(k,7)≤⌈7k/8⌉。
- 时间记账：所在批次墙钟时间按题数均摊约 51.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/644)；既有候选答案（按不可信材料审计）

### #650

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $f(m)$ be such that if $A\subseteq \{1,\ldots,N\}$ has $\lvert A\rvert=m$ then every interval in $[1,\infty)$ of length $2N$ contains $\geq f(m)$ many distinct integers $b_1,\ldots,b_r$ where each $b_i$ is divisible by some $a_i\in A$, where $a_1,\ldots,a_r$ are distinct. Estimate $f(m)$. In particular is it true that $f(m)\ll m^{1/2}$?
- 题意摘要：对每个 m，f(m) 是最大的统一保证值：任意 N、任意 m 元集 A⊆{1,…,N}、任意长度 2N 的正实区间中，都能选出 r≥f(m) 个互异整数 b_i，并将它们匹配到互异的 a_i∈A，使 a_i∣b_i。等价地，这是相应整除二部图最小可能的最大匹配数。
- 状态核对：已解决且有 Lean 核验；精确答案是 f(m)=min(m,⌈2√m⌉)，故原问 f(m)≪√m 为真，但常数 1 的不等式通常为假。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建论文路线：用 König–Ore 公式把最大匹配写成 m−max_{S⊆A}(|S|−|N(S)|)。下界部分把区间分成两个半区间，并把每个模数映到两侧邻域中的一对倍数；经“端点恰为倍数”的特殊分类修正后得到 |N(S)|≥2√|S|，从而匹配数至少 min(m,⌈2√m⌉)。上界先构造 |A|=st 的例子，使区间内所有相关倍数落在至多 s+t 个整数上，得到 f(st)≤s+t，再取相邻的 k(k+1) 或 (k+1)^2。
- 局部结论：f(m) 随 m 单调不减：对任意较大集合取一个 m 元子集即可。；二参数构造 f(st)≤s+t 蕴含 f(m)≤⌈2√m⌉：若 k²<m≤(k+1/2)²，用 m≤k(k+1)；否则用 m≤(k+1)²。；König–Ore 公式把所需下界精确归约为对每个 S⊆A 控制邻域亏损，而非只研究某一个最大匹配的未匹配点。
- 第一阻塞点：本次简化重建中，唯一不能在数行内独立闭合的是端点 x 被某些 a 整除时那组三类型注入的逐类无碰撞验证；这正是早期 AI 草稿曾出现缺口、后来由 Lean 修复的步骤。旧候选的“每个 a≤N 在任意长度 2N 的开区间内至少有两个倍数”并不成立，例如 a=N、区间 (0,2N) 仅含倍数 N，因此其较弱下界证明不能原样接受。
- 下一步：逐行复核论文定理 4.1 的三类型映射：分别验证同类型由坐标差确定 a，异类型的三种配对均矛盾；同时核对开区间端点约定与输入中“长度 2N”的版本完全等价。
- 来源核对：[官方问题页](https://www.erdosproblems.com/650)记录精确公式及 solved (Lean) 状态。；[van Doorn–Li–Tang 论文](https://arxiv.org/abs/2603.28636)给出人类整理的完整上下界证明，并说明早期下界注入曾有缺口。；论文处理区间长度 2 max A；输入允许 N≥max A。下界可在长度 2N 区间内取长度 2 max A 的子区间，上界取 N=max A，故两个定义给出同一极值。
- 时间记账：所在批次墙钟时间按题数均摊约 51.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/650)；既有候选答案（按不可信材料审计）

### #652

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ and let $R(x_i)=\#\{ \lvert x_j-x_i\rvert : j\neq i\}$, where the points are ordered such that\[R(x_1)\leq \cdots \leq R(x_n).\]Let $\alpha_k$ be minimal such that, for all large enough $n$, there exists a set of $n$ points with $R(x_k)<\alpha_kn^{1/2}$. Is it true that $\alpha_k\to \infty$ as $k\to \infty$?
- 题意摘要：对每个 n 点集，将各点的 pinned distinct-distance 数 R(p) 递增排列。α_k 是使得“对所有充分大的 n，存在某个 n 点集满足 R(x_k)<α_k√n”的最小常数。需证明这些最优存在常数随固定指标 k→∞ 而无界。
- 状态核对：已肯定解决。更直接的已知输入是 Mathialagan 的二部距离定理；它给出 α_k≳√k。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：给任意 n 点集取 P={x_1,…,x_k}、Q 为全点集。Mathialagan 定理称，当 2≤k≤n^{1/3} 时，P 中某点到 Q 确定至少 c√(kn) 个不同距离。去掉可能的零距离后，该点满足 R(p)≥c√(kn)−1；又因 p∈P，R(x_k)≥R(p)。固定 k 后令 n→∞，得到任何可行 α 均至少 c√k。
- 局部结论：对固定 k，条件 k≤n^{1/3} 在所有充分大的 n 自动成立。；任意配置均有 R(x_k)≥c√(kn)−1；因此存在性定义中的配置也不能绕过该下界。；令 n→∞ 消去 1/√n，得到 α_k≥c√k，从而 α_k→∞。
- 第一阻塞点：若要求完全自足证明，第一处外部输入是二部 pinned-distance 定理 D(P,Q)≳√(|P||Q|) 在 |P|≤|Q|^{1/3} 时的证明；它依赖 crossing-number/incidence 方法。旧候选的圆关联路线方向正确，但其“第二项自动低阶”必须先固定 k、α 再令 n→∞，不能作为 k、n 同时变化时的一致估计。
- 下一步：重建 Mathialagan 定理的 crossing-number 核心：明确画图的顶点、边重数截断和交叉数上下界，并检查常数对 k 独立；这会把当前引用定理的证明改成自足证明。
- 来源核对：[官方问题页](https://www.erdosproblems.com/652)记录 Mathialagan 定理及其对本题的直接推论。；[原论文摘要](https://arxiv.org/abs/1912.01883)明确给出 m≤n^{1/3} 时二部距离下界 Ω(√mn)。
- 时间记账：所在批次墙钟时间按题数均摊约 51.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/652)；既有候选答案（按不可信材料审计）

### #653

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ and let $R(x_i)=\#\{ \lvert x_j-x_i\rvert : j\neq i\}$, where the points are ordered such that\[R(x_1)\leq \cdots \leq R(x_n).\]Let $g(n)$ be the maximum number of distinct values the $R(x_i)$ can take. Is it true that $g(n) \geq (1-o(1))n$?
- 题意摘要：对每个由 n 个互异平面点组成的集合，计算每点的整数 R(p)∈{1,…,n−1}；记该配置中出现的不同 R 值数目。g(n) 是在所有 n 点配置上对此数目的最大值。问题问是否存在配置使除 o(n) 个碰撞外，几乎每点都有不同的 R 值，即 g(n)≥(1−o(1))n。
- 状态核对：截至核查仍开放；已知 0.7n<g(n)<n−cn^{2/3}，后二者并不矛盾于 conjecture。所给 Lean 文件只是带 `answer(sorry)` 的声明和 `sorry` 证明，不能作为实质形式化证据。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先检验最简单的显式构造：取 x_i=(i,0)，1≤i≤n。此时从 x_i 出发的距离为 1,…,max(i−1,n−i)，故 R(x_i)=max(i−1,n−i)。直接枚举这些整数值。
- 局部结论：等差共线构造给出恰好 ⌈n/2⌉ 个不同 R 值，因此独立得到 g(n)≥⌈n/2⌉。；该构造中的唯一系统性碰撞来自反射 i↔n+1−i；除中心外每个 R 值恰出现两次。；若用非等距共线点消除反射，R(p) 不再等于较远一侧的点数；距离和关系会产生不可控的新碰撞，因此简单扰动不能保持上述可计算公式。
- 第一阻塞点：这一路线在 ⌈n/2⌉ 处首先卡住：单个等差数列必有反射成对，而尚无可验证的多尺度扰动规则能让其中一个点的 R 增加、另一个不增加，并同时控制所有其他点的距离相等关系。更无法从该局部构造推出 1−o(1)。
- 下一步：做一个有限且可检验的构造搜索：令坐标为递增整数 0=t_1<⋯<t_n≤M，精确计算各差值集合，搜索最大不同 R 值数；先检查 n≤12 的最优共线模式是否超过 ⌈n/2⌉，再从最优实例提取可递推的 gap 序列。
- 来源核对：[官方问题页](https://www.erdosproblems.com/653)仍标为 open，并记录 7n/10 下界与 n−cn^{2/3} 上界。；本地 [653.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/653.lean)含 `answer(sorry)` 和最终 `sorry`，没有形式化解决本题。
- 时间记账：所在批次墙钟时间按题数均摊约 51.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/653)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/653.lean`；既有候选答案（按不可信材料审计）

### #654

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ with no four points on a circle. Must there exist some $x_i$ with at least $(1-o(1))n$ distinct distances to other $x_i$?
- 题意摘要：量词是：是否对每个充分大的 n、每个无四点共圆的 n 点集，都存在一点 p，使 R(p)≥(1−o(1))n。要否定它，只需给出无穷多个 n 的配置，使每一点均满足 R(p)≤cn，其中某个固定 c<1。
- 状态核对：输入状态已过期。官方页面现记录 2026 年 Aletheia 的反例；最强的 (1−o(1))n 断言为假。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：取 n=4m，K={10,…,m+9}，令 P={(0,±3^k):k∈K}、Q={(±2^j,0):j∈K}。若一圆含四个构造点，它必须在两坐标轴上各取两点。相交弦定理给 y_1y_2=x_1x_2，取绝对值后成为 3^{k_1+k_2}=2^{j_1+j_2}，与唯一分解矛盾。
- 局部结论：S=P∪Q 有 4m 个点且无四点共圆。；固定 p=(0,±3^{k_0})∈P，到 Q 的距离只依赖 |x|=2^j，故至多 m 种；到 P\{p}至多 2m−1 种。因此 R(p)≤3m−1。Q 中点完全对称。；所以每一点均有 R(p)≤3m−1<3n/4；沿 n=4m 的无穷子序列即否定任何 (1−o(1))n 的统一保证。
- 第一阻塞点：原问题已由该路线严格闭合，没有证明缺口。它不否定附加“无三点共线”的版本，因为构造全部位于两条直线上；官方页面仍将那个强化版本区别对待。旧候选把本题称为 open，已被 2026 年状态更新推翻。
- 下一步：若继续筛查，应转向尚未解决的强化问题：在无三点共线且无四点共圆条件下，能否保证 (1/3+c)n；第一项任务是核对已有一般位置构造是否真的控制每个 pinned R(p)，而不只是全局距离总数。
- 来源核对：[更新后的官方问题页](https://www.erdosproblems.com/654)明确记录 3n/4 反例。；[公开构造及证明](https://github.com/google-deepmind/superhuman/blob/main/aletheia/Erdos/Erdos.tex)给出双坐标轴、2 与 3 的幂的完整论证。
- 时间记账：所在批次墙钟时间按题数均摊约 51.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/654)；既有候选答案（按不可信材料审计）

### #655

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ be such that no circle whose centre is one of the $x_i$ contains three other points. Are there at least\[(1+c)\frac{n}{2}\]distinct distances determined between the $x_i$, for some constant $c>0$ and all $n$ sufficiently large?
- 题意摘要：量词为：是否存在绝对常数 c>0 和 N，使所有 n≥N、所有满足“以任一点 x_i 为圆心的任一圆至多经过另外两个点”的 n 点集，都确定至少 (1+c)n/2 个不同距离。
- 状态核对：字面命题已被正 n 边形反驳；目录仍标 open，是因为原意可能还包含一般位置条件。人工评审所说“与 Hunter 的退化解相同”只否定候选答案的新颖性，不否定反例本身；不能据此宣称解决一般位置变体。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `high`
- 尝试路线：独立核验正多边形，并用按距离着色的完全图核验极值。对每个距离 d，等距图 G_d 的每个顶点度数至多 2，故 |E(G_d)|≤n。正 n 边形中弦长为 2R sin(kπ/n)，1≤k≤⌊n/2⌋。
- 局部结论：若共有 D 个距离，则 C(n,2)=Σ_d|E(G_d)|≤Dn，所以 D≥⌈(n-1)/2⌉=⌊n/2⌋。；正 n 边形满足圆心条件：从每个顶点看，每种弦长最多出现两次。；这些弦长严格递增，故恰有 ⌊n/2⌋ 个距离；因此任意固定 c>0 的所求下界最终都失败。
- 第一阻塞点：字面命题已闭合为反例；无法继续闭合的是推测中的“一般位置”变体，因为正多边形违反“无四点共圆”，上述极值构造不再适用。
- 下一步：对一般位置变体，检验能否将正多边形作小扰动，同时把新增距离控制在 (1/2+o(1))n；首先计算扰动后弦长等式必然分裂多少个等价类。
- 来源核对：[官方条目](https://www.erdosproblems.com/655)明确记录 Hunter 的正多边形反例及一般位置歧义。；本地 655 Lean 文件准确编码原量词，但主定理仍为 `answer(sorry)` 与 `by sorry`，不是反例的机器验证。
- 时间记账：所在批次墙钟时间按题数均摊约 60.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/655)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/655.lean`；既有候选答案（按不可信材料审计）

### #657

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that if $A\subset \mathbb{R}^2$ is a set of $n$ points such that every subset of $3$ points determines $3$ distinct distances (i.e. $A$ has no isosceles triangles) then $A$ must determine at least $f(n)n$ distinct distances, for some $f(n)\to \infty$?
- 题意摘要：令 Φ(n) 为所有 n 点平面集合 A（任意三点的三条边长两两不同）所确定距离数的最小值。问题等价于问 Φ(n)/n→∞，即存在 f(n)→∞，使每个这样的 A 都有至少 nf(n) 个距离。
- 状态核对：截至所给冻结状态仍开放。候选答案的线性匹配下界正确，但不能由此断言它是最佳已知平面下界；官方材料给出的超线性结果属于一维无三项等差数列模型，不能直接推广到任意平面点集。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把 K_n 的边按长度着色。无等腰三角形意味着同色两边不能共享端点，所以每个颜色类是匹配；尝试从匹配之间的欧氏实现约束推出颜色数超线性。
- 局部结论：每个顶点到其余 n−1 点的距离两两不同，故 Φ(n)≥n−1。；更精确地，每色至多 ⌊n/2⌋ 条边，所以 Φ(n)≥n−1（n 偶）及 Φ(n)≥n（n 奇）。；仅有“每色为匹配”不足：抽象 K_n 存在使用 n−1 或 n 种颜色的最优边染色，正好达到上述线性级别。
- 第一阻塞点：第一处断点是无法证明欧氏距离矩阵排除近似 1-因子分解式的长度着色；三角不等式及单个四点的 Cayley–Menger 约束尚未给出累积到 ω(n) 个颜色的机制。
- 下一步：固定两种颜色，枚举其匹配并写出每个交替偶圈对应的 Cayley–Menger 方程；检验是否能证明大量双色 4-圈迫使退化、共圆或等腰三角形。
- 来源核对：[官方条目](https://www.erdosproblems.com/657)仍列为 open，并明确区分平面问题与一维 3-AP-free 差集问题。；未发现本题本地形式化文件；候选答案引用的一维构造只能给平面问题的上界示例，不能给任意平面集合的下界。
- 时间记账：所在批次墙钟时间按题数均摊约 60.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/657)；既有候选答案（按不可信材料审计）

### #659

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is there a set of $n$ points in $\mathbb{R}^2$ such that every subset of $4$ points determines at least $3$ distances, yet the total number of distinct distances is\[\ll \frac{n}{\sqrt{\log n}}?\]
- 题意摘要：要求对每个 n 构造 n 点集 P_n⊂R²，使每个四点子集至少产生三种距离，并存在绝对常数 C，使总距离数至多 Cn/√log n。
- 状态核对：按冻结状态已肯定解决。这里重建的是已知构造，不主张新证明。需纠正候选答案中的坐标排版：格点是 (i,√2j)，不是 `(i,√2,j)`。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：取 P_m={(i,√2j):0≤i,j<m}。距离平方为 u²+2v²。用 Bernays 定理计数该二元二次型表示的整数；局部性质则用四点二距离构型的六型分类，并逐一排除正方形、等边三角形及正五边形四顶点型。
- 局部结论：所有距离平方属于 {u²+2v²≤3m²}；Bernays 定理给其基数 O(m²/√log m)。取 m=⌈√n⌉ 后删至 n 点，仍得 O(n/√log n)。；格中无非退化正方形：边向量 (a,√2b) 旋转 90° 后为 (−√2b,a)；它再次属于该格迫使 a=b=0。；格中无等边三角形：若边长平方为 q、格行列式为 √2k，则 Gram 行列式同时给 2k²=3q²/4，即 8k²=3q²，无非零整数解。正五边形型的两种距离平方之比为 (3+√5)/2，但格中任意两个距离平方之比为有理数。
- 第一阻塞点：短重建不能自行证明两个外部输入：Bernays 的表示数渐近式，以及“四点恰有两种距离只有六个相似型”的完整分类；接受这两项已知定理后路线闭合。另，本地 Lean 包装文件的主证明是 `by sorry`，且注释说明数论部分以公理输入 Bernays 定理，故该文件本身不是自包含的无公理验证。
- 下一步：形式化核验应先导入并证明六型分类，再明确列出 Bernays 定理为外部公理或完成其形式化；随后检查外部所称 Lean proof 是否无 `sorry`，不要只检查当前包装文件的 solved 标签。
- 来源核对：[Grayzel 论文](https://arxiv.org/abs/2601.09102)明确给出格 L=Z×√2Z、Bernays 计数及六型分类路线。；[官方条目](https://www.erdosproblems.com/659)标为 PROVED (LEAN)。；本地 `659.lean` 的定理体实际为 `by sorry`；因此只核实了陈述和证明依赖，未核实一份自包含 Lean 证书。
- 时间记账：所在批次墙钟时间按题数均摊约 60.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/659)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/659.lean`；既有候选答案（按不可信材料审计）

### #660

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^3$ be the vertices of a convex polyhedron. Are there at least\[(1-o(1))\frac{n}{2}\]many distinct distances between the $x_i$?
- 题意摘要：对每个由 n 个不同极点组成的三维凸多面体顶点集 P，问其距离数 D(P) 是否一致满足 D(P)≥(1−o(1))n/2；等价地，对每个 ε>0，充分大 n 时所有 P 都有 D(P)≥(1−ε)n/2。
- 状态核对：仍开放。候选答案把 Erdős 对 Altman 的转述写成“最佳已发表保证”过强：官方条目明确说没有给出参考，故这里只把 Ω(n) 当作历史性报告，不作为已核验定理。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `medium`
- 尝试路线：先核验 n/2 尺度的双锥上界，再尝试按距离的边重数计数。令 m=n−2 个底点为半径 R 的正 m 边形，加高为 ±h 的两顶点；选择 k 使 2Rsin(kπ/m)>R，并令 R²+h²等于该弦长平方。
- 局部结论：该双锥确为凸多面体，底面距离只有 ⌊m/2⌋ 种；顶点到底点的距离可并入一种底面弦长，顶点间距离至多再添一种，故 D≤⌊m/2⌋+1=n/2+O(1)。；若某配置中每种距离 d 的重数为 e_d，则 C(n,2)=Σ_de_d，因而任何统一上界 e_d≤M 都给 D≥C(n,2)/M。；但双锥可让同一长度同时出现在底面弦和两组顶点—底点边中，产生约 3n 条同长边；因此简单证明 e_d≤(1+o(1))n 的路线直接失败。
- 第一阻塞点：第一处无法闭合的是把凸性转化为足够强的全局重数约束。三维凸性既不给顶点循环次序，也不使固定距离图平面；仅控制最大 e_d 至多常数倍 n 也无法把常数推进到 1/2。
- 下一步：研究重数尾和而非最大值：对 t≥2，尝试界定 #{d:e_d≥tn}，并检验双锥是否为高重数层的极端模型；若能证明前 D 个最大重数之和小于 C(n,2) 对所有 D<(1−ε)n/2，即可闭合。
- 来源核对：[官方条目](https://www.erdosproblems.com/660)仍列为 open，并注明 Altman 的三维线性界只有 Erdős 转述、无参考。；双锥的距离计算已直接核验；候选答案所给构造尺度正确，但不提供所需下界。
- 时间记账：所在批次墙钟时间按题数均摊约 60.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/660)；既有候选答案（按不可信材料审计）

### #661

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there, for all large $n$, some points $x_1,\ldots,x_n,y_1,\ldots,y_n\in \mathbb{R}^2$ such that the number of distinct distances $d(x_i,y_j)$ is\[o\left(\frac{n}{\sqrt{\log n}}\right)?\]
- 题意摘要：在标准非平凡解释下，要求对所有充分大 n，存在两个各含 n 个不同平面点的集合 P_n={x_i}、Q_n={y_j}，使交叉距离集合 {|x_i−y_j|} 的大小为 o(n/√log n)。若允许列表内重复，命题可由重合点平凡实现，故必须采用集合解释。
- 状态核对：截至官方 2026-01-11 更新仍开放。候选答案给出的 Ω(n/log n) 与 O(n/√log n) 缝隙和现有论文相符，但它没有构成 little-o 构造。
- 初步判定：`promising`；证明尝试：`heuristic_route`；可行性 `4/10`；置信度 `medium`
- 尝试路线：从 2n 点格盒分成 P、Q 得标准 O(n/√log n)；为争取 little-o，尝试改用随 n 变化的各向异性格 L_q={(a,√q b)}，把问题化为统一计数盒内 u²+qv² 的不同取值。
- 局部结论：把一个含 2n 点的整数格盒任意分成两个 n 点集，交叉距离是全部距离的子集，故 F(n,n)=O(n/√log n)。；二部距离能量满足 (n²)²≤D·E；现有刚性运动/直线相交估计 E=O(n³log²n)，从而 D=Ω(n/log n)。；对任一固定 q，Bernays 型估计只给 C_q n/√log n，常数不随 n 消失；因此固定二次型路线本身不能推出 little-o。
- 第一阻塞点：第一处断点是缺少对判别式随 n 增长的二次型表示数的一致上界。令 q=q(n) 可能使 Bernays 常数变小，但现有固定判别式渐近式不统一，且 q 过大时盒内不同值可能反而接近 n²。
- 下一步：证明一个带显式 q 依赖的筛法上界：估计 N_q(m)=|{u²+qv²:|u|,|v|<m}|，先在 1≤q≤(log m)^A 范围内优化 N_q(m)/(m²/√log m)，检查其下确界是否趋于 0。
- 来源核对：[官方条目](https://www.erdosproblems.com/661)确认问题仍开放，并给出 F=o(f) 的推广表述。；[Mathialagan 的论文](https://arxiv.org/abs/1912.01883)证明平衡情形 D(n,n)=Ω(n/log n)，并记录格构造的 O(n/√log n) 上界。；候选答案默认了点互异；这是必要但原文未显式写出的非平凡解释。
- 时间记账：所在批次墙钟时间按题数均摊约 60.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/661)；既有候选答案（按不可信材料审计）

### #662

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Consider the triangular lattice with minimal distance between two points $1$. Denote by $f(t)$ the number of distances from any points $\leq t$. For example $f(1)=6$, $f(\sqrt{3})=12$, and $f(3)=18$. Let $x_1,\ldots,x_n\in \mathbb{R}^2$ be such that $d(x_i,x_j)\geq 1$ for all $i\neq j$. Is it true that, provided $n$ is sufficiently large depending on $t$, the number of distances $d(x_i,x_j)\leq t$ is less than or equal to $f(t)$ with equality perhaps only for the triangular lattice? In particular, is it true that the number of distances $\leq \sqrt{3}-\epsilon$ is less than $1$?
- 题意摘要：给定最小互距至少为 1 的有限点集，原文似欲用三角格中半径 t 邻域的点数 f(t) 控制“距离不超过 t 的数目”；但没有说明这是总点对数、每点邻居数、平均度，还是不同距离值数。
- 状态核对：应判为题面损坏而非已解决开放题。官方也明确指出原文至少有一处笔误。此前候选把一种自行选定的解释反驳后称原题已否定，不成立。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `1/10`；置信度 `high`
- 尝试路线：先逐种核验最自然解释。若指总点对数，取 x_i=(i,0)：t≥1 时至少有 n-1 个短点对，不可能由固定的 f(t) 控制。若指单点邻居数，取方格点阵；当 √2<t<√3 时，内部点有 8 个邻居，而三角格对应值为 6。
- 局部结论：三角格向量平方长度为 a²+ab+b²；半径 3 内实际有 6+6+6+12+6=36 个非原点格点，因此题面的 f(3)=18 与“球内格点数”解释矛盾。；在“总短点对数”解释下，任意 t≥1 均被长链严格反驳。；在“最大局部邻居数”解释下，方格对 √2<t<√3 给出 8>6；但这只能反驳该特定解释。
- 第一阻塞点：第一处无法闭合之处不是几何估计，而是待估量根本未定义；尤其“少于 1 个距离”也无法与前文任何自然的整数计数一致。
- 下一步：回查 Er97e 第532页及相邻记号，确定是否遗漏了除以 n、平均每点计数或密度极限；在此之前不应继续证明原句。
- 来源核对：[官方题页及歧义说明](https://www.erdosproblems.com/662)仍将其列为 open，但明确说原文按字面无意义。；独立核算三角格壳层，确认 f(3)=18 与球内格点计数不符。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/662)；既有候选答案（按不可信材料审计）

### #663

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ and $q(n,k)$ denote the least prime which does not divide $\prod_{1\leq i\leq k}(n+i)$. Is it true that, if $k$ is fixed and $n$ is sufficiently large, we have\[q(n,k)<(1+o(1))\log n?\]
- 题意摘要：固定整数 k≥2。令 q(n,k) 为不整除 A=∏_{i=1}^k(n+i) 的最小素数；问题问 n→∞ 时是否对所有充分大的 n 有 q(n,k)≤(1+o(1))log n。
- 状态核对：截至核查仍为开放题。此前候选给出的初等 k 倍上界和 primorial 锐性例子正确，但不是目标结论。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：设 Q=q(n,k)，把每个 k<p<Q 的素数分配给它整除的唯一一个 n+i。令 M_i 为分配到第 i 项的这些不同素数之积，则 M_i∣n+i，并尝试利用相邻整数关系，而不只使用总乘积。
- 局部结论：由 ∏_{p<Q}p∣A 得 θ(Q)≤k log(n+k)，故 Q≤(k+o(1))log n。；若 p>k 同时整除 n+i 与 n+j，则 p∣i-j，矛盾；故 M_i 两两互素，且写 n+i=M_i a_i 后有 M_i a_i-M_j a_j=i-j。；取 n=∏_{p≤y}p-1，则所有 p≤y 都整除 n+1，因而 q(n,k)>y，而 log n∼y；所以目标中的常数 1 若成立将是最优的。
- 第一阻塞点：关系 M_i a_i-M_j a_j=i-j 尚不能排除素数在 k 个 M_i 间近乎均匀分配；现有确定性信息仍只给出 ∑log M_i≈Q 和每个 M_i≤n，因而停在常数 k。
- 下一步：先对固定 k、ε>0严格估计区间 [X,2X] 中满足 q(n,k)>(1+ε)log X 的 n 的数量；目标是用大筛或分配计数得到幂次节省，并明确检查能否从“稀少”升级为“最终不存在”。
- 来源核对：[官方题页](https://www.erdosproblems.com/663)确认目标、初等 k 倍上界及开放状态。；primorial 例和素数唯一分配均已独立核算，未依赖候选答案的结论。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/663)；既有候选答案（按不可信材料审计）

### #665

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there some constant $c$ such that for every $n$ there are $A_1,\ldots,A_m\subseteq \{1,\ldots,n\}$ such that $\lvert A_i\rvert >n^{1/2}-c$ for all $i$, and $\lvert A_i\cap A_j\rvert \leq 1$ for all $i\neq j$, and every pair $1\leq x<y\leq n$ has $\{x,y\}\subseteq A_i$ for some $i$?
- 题意摘要：按修订后的非平凡 PBD 题意：对所有充分大的 v，是否存在常数 C及一族真子块 2≤|A_i|<v，使每一对点恰在一个块中，并且所有 |A_i|>√v-C？
- 状态核对：输入所录旧句确实允许 A_1=[v]，但人工评审指出网站已修订。现行定义明确要求 |A_i|<v，因此不复述此前候选的单块“解”；问题仍开放。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把 PBD 视为 K_v 的团分解，令 s=min_i|A_i|。使用点对计数、过一点的块分割以及 de Bruijn–Erdős 不等式，尝试证明这种设计必须接近射影平面。
- 局部结论：精确恒等式为 ∑_i C(|A_i|,2)=C(v,2)；若 s>√v-C，则块数 m≤v(v-1)/(s(s-1))=v+O_C(√v)。；非平凡有限线性空间满足 m≥v，因此 m=v+O_C(√v)；这已把候选设计压缩到接近射影平面的窄范围。；对每个点 x，含 x 的块将其余 v-1 个点分割，故 ∑_{A_i∋x}(|A_i|-1)=v-1，进而复制数 r_x≤(v-1)/(s-1)=√v+O_C(1)。射影平面阶 q 在 v=q²+q+1 时给出 |A_i|=q+1>√v，故至少在该子序列存在。
- 第一阻塞点：第一处缺口是稳定性：由 m-v=O(√v)及 r_x=√v+O(1)尚不能推出设计可嵌入某个射影平面。Shrikhande–Singhi 的深刻嵌入定理正处理这一跳跃；再结合“射影平面阶皆为素数幂”猜想才得到条件否定。
- 下一步：重建 Shrikhande–Singhi 嵌入定理的准确参数，并从上述恒等式逐条核验其稳定性假设；随后把允许的 C 转化为相邻可用射影平面阶之间的有界间隙命题。
- 来源核对：[修订后的官方题页](https://www.erdosproblems.com/665)明确加入 2≤|A_i|<v，并将量词写为“所有充分大的 v”。；[Shrikhande–Singhi 论文页面](https://doi.org/10.1007/BF02579251)确认其嵌入定理及条件性否定方向。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/665)；既有候选答案（按不可信材料审计）

### #667

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p,q\geq 1$ be fixed integers. We define $H(n)=H(N;p,q)$ to be the largest $m$ such that any graph on $n$ vertices where every set of $p$ vertices spans at least $q$ edges must contain a complete graph on $m$ vertices. Is\[c(p,q)=\liminf \frac{\log H(n)}{\log n}\]a strictly increasing function of $q$ for $1\leq q\leq \binom{p-1}{2}+1$?
- 题意摘要：固定 p≥2。H(n;p,q) 是所有满足“每个 p 点诱导子图至少有 q 条边”的 n 阶图必含团的最大保证阶数；问 c(p,q)=liminf_{n→∞}log H/log n 是否在 1≤q≤C(p-1,2)+1 上逐项严格递增。原句 p=1 时约束不可满足，通常应排除。
- 状态核对：严格单调性仍开放；单调不减、终端跃迁以及 p=3 可严格验证。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：转到补图 F。原条件等价于每个 p 点在 F 中至多 r=C(p,2)-q 条边，而 G 中的团正是 F 的独立集；于是问题化为局部稀疏图所强制的独立数指数是否随 r 严格变化。
- 局部结论：q 增大使允许的补图类缩小，故 H(n;p,q)及 c(p,q)单调不减；但 liminf 本身不能把非严格单调升级为严格。；在 q=C(p-1,2)+1 时 r=p-2。若 F 有至少 p 个顶点的连通分量，其中可取 p 点树，产生至少 p-1 条边，矛盾；故各分量至多 p-1，α(F)≥n/(p-1)，从而 c=1。；在前一值 q=C(p-1,2)已有 c≤1/2，故最后一步确有严格跃迁。对 p=3，Ramsey 定理给 c(3,1)=1/2，而上述分量论证给 c(3,2)=1。
- 第一阻塞点：对中间 q，局部条件“每个 p 点至多 r 条补边”没有提供足以分离相邻 r 的独立数幂指数估计；现有容斥或平均度界通常只给同一幂次，无法证明严格差。
- 下一步：先处理最小未知参数（例如 p=4 的中间 q）：明确列出补图的有限禁子图族，并分别构造随机下界与容器法上界，检查 q 与 q+1 的独立数指数区间是否已经分离。
- 来源核对：[官方题页](https://www.erdosproblems.com/667)确认开放状态、Ramsey 端点界、c=1 端点及前一值 c≤1/2。；补图端点证明已独立检查；此前候选的该段论证成立。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/667)；既有候选答案（按不可信材料审计）

### #668

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that the number of incongruent sets of $n$ points in $\mathbb{R}^2$ which maximise the number of unit distances tends to infinity as $n\to\infty$? Is it always $>1$ for $n>3$?
- 题意摘要：令 u(n) 为 n 个平面点可确定的最大单位距离数，g(n) 为达到 u(n) 的点集在全等下的类数。主问 g(n)→∞ 是否成立；次问是否每个 n>3 都有 g(n)>1。
- 状态核对：主问仍开放；次问已由 n=4 的唯一极值构型否定。计算只枚举单位距离图的同构类，不能直接等同于全等类数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：研究增量 Δ_n=u(n+1)-u(n)。从任一 n 点极值集 S 出发，在某点 a 的单位圆上加入新点，并避开与其余点形成单位距离的有限多个位置。
- 局部结论：总可加入一个只与 a 相距 1 的新点，故 u(n+1)≥u(n)+1。；若 u(n+1)=u(n)+1，则上述单位圆上除有限点外的连续族全是极值集；有限点集间的全等只能诱导有限多个点置换，故得到连续多个全等类，特别是 g(n+1)=∞。；u(4)=5：K_4不能作为平面单位距离图，而两个共边等边三角形给出5条。任何5边构型的图为 K_4-e；两个等边三角形的第三顶点必须位于公共边两侧，因此全等类唯一，即 g(4)=1。
- 第一阻塞点：无法证明 Δ_n=1 会无限多次发生；若最终总有 Δ_n≥2，现有单位距离上界也不排斥。因而这条增量路线尚不能推出 g(n)无界，更不能推出趋于无穷。
- 下一步：利用 n≤21 的已认证极值图数据逐项计算 Δ_n，并检查所有 Δ_n=1 的位置是否确实产生连续嵌入族；随后尝试证明任何长期保持 Δ_n≥2 的序列会违反已知的 u(n)上界或结构限制。
- 来源核对：[官方题页](https://www.erdosproblems.com/668)确认主问开放、g(4)=1，并提醒图同构与几何全等不同。；[Alexeev–Mixon–Parshall](https://arxiv.org/abs/2412.11914)只声称 n≤21 时枚举最稠密单位距离图，不能据此直接断言几何全等类数。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/668)；既有候选答案（按不可信材料审计）

### #669

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F_k(n)$ be minimal such that for any $n$ points in $\mathbb{R}^2$ there exist at most $F_k(n)$ many distinct lines passing through at least $k$ of the points, and $f_k(n)$ similarly but with lines passing through exactly $k$ points. Estimate $f_k(n)$ and $F_k(n)$ - in particular, determine $\lim F_k(n)/n^2$ and $\lim f_k(n)/n^2$.
- 题意摘要：固定整数 k≥2。对每个 n 点集 P⊂R²，令 t_j(P) 为恰含 j 个点的直线数；则 f_k(n)=max_P t_k(P)，F_k(n)=max_P∑_{j≥k}t_j(P)。问题要求估计二者，尤其证明相应二次归一化极限存在并求值。
- 状态核对：截至当前资料仍属开放；k=2,3 已知。候选答案没有解决 k≥4，并把 Szemerédi–Trotter 的量级估计说得过于接近“确定极限”；网格是否给出所声称的、对所有参数一致的恰含 k 点下界也未作核验。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先作点对计数，再尝试由 Szemerédi–Trotter 控制富线；随后考察能否通过拼接近极值配置证明 n^{-2}f_k(n)、n^{-2}F_k(n) 收敛。
- 局部结论：严格恒等式为 ∑_{j≥2} C(j,2)t_j(P)=C(n,2)，故 F_k(n)≤C(n,2)/C(k,2)，从而 limsup F_k(n)/n²≤1/[k(k−1)]，且 f_k≤F_k。；k=2 时取一般位置点集得 f_2(n)=F_2(n)=C(n,2)，极限为 1/2；题面所引 BGS74 给出 k=3 时 f_3(n),F_3(n)=n²/6−O(n)，故两极限均为 1/6。；Szemerédi–Trotter 可推出 F_k(n)≪n²/k³+n/k；对固定 k 这只给 O(n²)，不会给出极限常数。将两个配置作一般位置拼接只能可靠保留原有 k-富线，得到近似超可加性 f_k(n+m)≥f_k(n)+f_k(m)，其尺度是线性的，不能控制除以 n² 后的振荡。
- 第一阻塞点：第一处无法闭合的是把不同规模的近极值配置“二次放大”：普通拼接会产生不可控的跨块直线，而单纯超可加性不足以证明二次归一化极限存在。
- 下一步：对一个明确的放大操作做检验：将每个点替换为小型仿射副本，逐类计算旧直线、块内直线和跨块直线的重数，判断能否得到 f_k(mn)≥m²f_k(n)−o(m²n²) 或相应 F_k 不等式。
- 来源核对：当前问题页仍标为 OPEN，并只记录 k=2,3 及点对上界：[Erdős Problems #669](https://www.erdosproblems.com/669)。；候选答案中的 Green–Tao 精确公式即使适用于 f_3，也不自动证明关于 F_3 的断言；这里仅采用题面已给出的 BGS74 渐近式。
- 时间记账：所在批次墙钟时间按题数均摊约 55.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/669)；既有候选答案（按不可信材料审计）

### #670

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{R}^d$ be a set of $n$ points such that all pairwise distances differ by at least $1$. Is the diameter of $A$ at least $(1+o(1))n^2$?
- 题意摘要：按通常意图先固定 d，再令 n→∞：A⊂R^d 有 n 个点，任意两条不同的无序点对距离之差至少为 1；问 diam(A)≥(1+o_d(1))n² 是否成立。若要求对随 n 增长的 d 也一致成立，则是另一命题。
- 状态核对：固定 d 的版本仍开放；字面上若允许 d=d(n)，现已存在反例，直径可至约 (1−1/π²)n²。因此必须明确量词。候选答案遗漏了这一维数增长反例。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把 M=C(n,2) 个距离排序为 r_1<⋯<r_M，并尝试利用间隔条件及三角不等式，把平凡常数 1/2 提升到 1。
- 局部结论：n≥3 时每个距离至少为 1：给定 x≠y，取第三点 z，则 ||x−z|−|y−z||≥1，而反三角不等式给出该差≤|x−y|。；因此 r_j≥j，特别是 diam(A)=r_M≥M=C(n,2)=(1/2+o(1))n²。；每个三角形的三边也是三项至少相隔 1 的距离值，但这些局部约束大量重叠；直接求和只重复得到距离排序或三角不等式，尚不能额外贡献约 n²/2。
- 第一阻塞点：要达到常数 1，必须从欧氏距离之间的全局相容性再获得约 C(n,2) 的总空隙；逐三角形使用三角不等式无法把这些空隙无重叠地分配给全局距离序列。
- 下一步：固定 d=2 或 3，建立距离秩 r(x,y) 的组合模型，检验 Cayley–Menger 行列式或端点投影能否迫使正比例的相邻秩间隔超过 1；先对四点子集给出可求和的不等式。
- 来源核对：问题页说明固定 d 是预期解释，并记录维数 d=n²−n 时的反例：[Erdős Problems #670](https://www.erdosproblems.com/670)。
- 时间记账：所在批次墙钟时间按题数均摊约 55.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/670)；既有候选答案（按不可信材料审计）

### #671

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given $a_{i}^n\in [-1,1]$ for all $1\leq i\leq n<\infty$ we define $p_{i}^n$ as the unique polynomial of degree $n-1$ such that $p_{i}^n(a_{i}^n)=1$ and $p_{i}^n(a_{i'}^n)=0$ if $1\leq i'\leq n$ with $i\neq i'$. We similarly define\[\mathcal{L}^nf(x) = \sum_{1\leq i\leq n}f(a_i^n)p_i^n(x),\]the unique polynomial of degree $n-1$ which agrees with $f$ on $a_i^n$ for $1\leq i\leq n$ (that is, the sequence of Lagrange interpolation polynomials). Is there such a sequence of $a_i^n$ such that for every continuous $f:[-1,1]\to \mathbb{R}$ there exists some $x\in [-1,1]$ where\[\limsup_{n\to \infty} \sum_{1\leq i\leq n}\lvert p_{i}^n(x)\rvert=\infty\]and yet\[\mathcal{L}^nf(x) \to f(x)?\]Is there such a sequence such that\[\limsup_{n\to \infty} \sum_{1\leq i\leq n}\lvert p_{i}^n(x)\rvert=\infty\]for every $x\in [-1,1]$ and yet for every continuous $f:[-1,1]\to \mathbb{R}$ there exists $x\in [-1,1]$ with\[\mathcal{L}^nf(x) \to f(x)?\]
- 题意摘要：节点是一个三角阵列，每行 n 个互异点。第一问量词为 ∃节点阵列 ∀f∈C[-1,1] ∃x：Lebesgue 函数 Λ_n(x)=∑|p_i^n(x)| 无界且 L^nf(x)→f(x)。第二问要求同一阵列还满足 ∀x Λ_n(x) 无界，同时仍有 ∀f∃x 插值收敛。
- 状态核对：整体仍列为开放。1958 年 Erdős 原文明确声称构造可肯定第一问，但该段没有给出构造证明；因此可视为强烈的已知路线，不能仅凭一句声明独立认证。第二问仍未由该声明解决。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：把 T_{n,x}:C[-1,1]→R 定义为 T_{n,x}f=L^nf(x)，尝试用一致有界原理和 Baire 类方法处理第二问中的量词交换。
- 局部结论：对固定 x，||T_{n,x}||=Λ_n(x)：上界由三角不等式；下界可取连续函数在有限节点上等于 sign(p_i^n(x))。；若 limsup Λ_n(x)=∞，一致有界原理给出某个依赖于 x 的连续 f，使 sup_n|L^nf(x)|=∞；但这只是 ∀x∃f，不能交换为 ∃f∀x。；若 Λ_n(x) 对每个 x 都无界，则对任一可数稠密集 D，Baire 论证给出剩余类的 f，使插值在每个 x∈D 上无界；这仍不排除该 f 在某个 x∉D 收敛。
- 第一阻塞点：第一处障碍正是从可数稠密集推广到全部不可数点：L^nf 的次数和导数随 n 增长，缺少能把某点收敛传播到邻域的统一等度连续估计。
- 下一步：重建 Erdős 所称第一问构造：逐行写出被挤压的 Chebyshev 节点，证明相应坏点集为 continuum，并逐一核对对任意固定 f 的完整序列收敛，而不只是子列收敛。
- 来源核对：当前页面仍将两问整体列为 OPEN，并记录 Bernstein 与 Erdős–Vértesi 的结果：[Erdős Problems #671](https://www.erdosproblems.com/671)。；Erdős 1958 原文确实写道存在阵列，使每个连续 f 在 continuum 多个 Λ_n 无界点仍有插值收敛；紧接着说明他不能决定“处处无界”情形：[原论文第3页](https://old.renyi.hu/~p_erdos/1958-14.pdf)。；因此候选答案对第一问的方向有原文支持，但把未展示证明的声明直接当作已独立核验定理，证据强度偏高。
- 时间记账：所在批次墙钟时间按题数均摊约 55.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/671)；既有候选答案（按不可信材料审计）

### #675

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：We say that $A\subset \mathbb{N}$ has the translation property if, for every $n$, there exists some integer $t_n\geq 1$ such that, for all $1\leq a\leq n$,\[a\in A\quad\textrm{ if and only if }\quad a+t_n\in A.\]{UL} {LI}Does the set of the sums of two squares have the translation property?{/LI} {LI}If we partition all primes into $P\sqcup Q$, such that each set contains $\gg x/\log x$ many primes $\leq x$ for all large $x$, then can the set of integers only divisible by primes from $P$ have the translation property?{/LI} {LI}If $A$ is the set of squarefree numbers then how fast does the minimal such $t_n$ grow? Is it true that $t_n>\exp(n^c)$ for some constant $c>0$?{/LI} {/UL}
- 题意摘要：平移性质是：∀n∃整数 t≥1，使 ∀1≤a≤n，a∈A⇔a+t∈A。问题分别询问两平方和集、由稠密素数划分 P⊔Q 得到的 P-光滑整数集，以及平方自由数时最小可行平移 t_n 的增长。
- 状态核对：前两部分仍开放；平方自由数具有平移性质。候选答案的伸缩指数论证引用有误：q^{3/2+ε} 是 Prachar 型界，Heath-Brown 给出更强的 13/9 指数；而 Nunes 文中的改进限于平方自由模数，不能直接用于 q=p²。不过所需 exp(n^c) 下界可用更初等的计数严格推出。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：前两问尝试“CRT 强制负例＋筛法保护正例”；第三问先证明一个模 p² 的覆盖引理，再强迫大量 p²整除任意可行平移。
- 局部结论：两平方和情形可为每个原本不是两平方和的 a 指派不同的 q≡3 mod 4，并用 t≡−a+q (mod q²) 强迫 v_q(a+t)=1；但对原本是两平方和的 a，仍须同时排除所有未预先指定的 q≡3 mod 4 的奇指数，CRT 本身不能完成。P⊔Q 情形有同样结构：可强迫负例含 Q-素因子，却难保证所有正例避免稠密的 Q。；平方自由平移存在：对非平方自由的 a，用互异大素数 q_a 规定 q_a²|(a+t)；在所得算术级数中，要求有限多个对应于平方自由 a 的线性式同时平方自由。坏条件来自模 r² 的有限剩余类，而 ∑_r1/r²<∞，标准有限筛给出可行 t。；设 t 对前 n 项有效。若每个非零模 p² 剩余类都含某个≤n的平方自由数，则必须 p²|t；否则取平方自由 a≡−t (mod p²)，会有 p²|(a+t)，矛盾。进一步，利用 ∑_{素数 r}r^{-2}<1 的并集计数，可证明每个与 q 互素的剩余类模 q 都有 O(q²) 大小的平方自由代表。取 q=p²处理 p∤a 的类；对 a≡pb mod p²，先在 b mod p 中取 O(p²) 的平方自由 m，再用 pm。故所有非零类都有 O(p⁴) 的平方自由代表。于是所有 p≪n^{1/4} 均满足 p²|t_n，因而 log t_n≥2∑_{p≪n^{1/4}}log p≫n^{1/4}，特别地 t_n>exp(n^c) 对某个 c>0（例如任意 c<1/4）最终成立。
- 第一阻塞点：前两问的第一处缺口是筛余量：被保护的若干平移数必须避开一个具有正素数密度的禁因子族，简单的收敛筛 ∑1/p²<∞ 已不适用。第三问的 exp(n^c) 子问题则在上述标准素数估计下已闭合。
- 下一步：把第三问的 O(q²) 最小平方自由代表引理写成完整带常数证明；前两问则先计算对应多线性筛的局部密度乘积，确定是否存在 parity problem 或覆盖同余障碍。
- 来源核对：当前页面确认前两问开放、平方自由数具有平移性质：[Erdős Problems #675](https://www.erdosproblems.com/675)。；Nunes 的论文明确记载 Prachar 的 q^{3/2+ε} 与 Heath-Brown 的 q^{13/9+ε}；其自身改进要求 q 平方自由：[Nunes 2016](https://arxiv.org/abs/1605.03347)。；候选答案把 Heath-Brown 指数写错且未注意 Nunes 模数条件；这里的 n^{1/4} 路线不依赖该错误引用。
- 时间记账：所在批次墙钟时间按题数均摊约 55.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/675)；既有候选答案（按不可信材料审计）

### #676

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is every sufficiently large integer of the form\[ap^2+b\]for some prime $p$ and integer $a\geq 1$ and $0\leq b<p$?
- 题意摘要：量词为：是否 ∃N，使每个 n≥N 都存在素数 p、整数 a≥1 与 0≤b<p，满足 n=ap²+b。等价地，是否每个充分大 n 都存在 p≤√n，使最小非负余数 n mod p² 小于 p。
- 状态核对：仍开放；已知几乎所有整数可表示，筛法只说明例外稀疏。候选答案正确指出开放，但没有进行实际反例或证明路线。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试用中国剩余定理构造无限反例：对一批小素数 p，规定 n mod p²∈{p,…,p²−1}，从而排除这些 p；再估计尚未控制的大素数。
- 局部结论：表示条件的余数重述严格成立：a≥1 强迫 p²≤n，而给定 p≤√n，令 b=n mod p²，则 b<p 正好等价于所需表示。；对任意有限素数集合 S，可以由 CRT 构造任意大的 n，使每个 p∈S 都不能表示 n；例如统一规定 n≡p (mod p²)，各模数两两互素。；对随机 n，固定 p 的有利剩余类比例为 p/p²=1/p；形式上的独立性启发式给出避免所有 p≤√n 的概率约 ∏(1−1/p)≈1/log n，与“例外可能无限但密度为零”相容，却不是证明。
- 第一阻塞点：CRT 构造出的 n 通常远大于已控制素数上界 y，因而还必须排除 y<p≤√n 的全部新素数；有限同余构造对此没有任何控制。这是反例路线的第一处实质缺口。
- 下一步：对 CRT 生成的算术级数应用上界筛，估计其中被某个 y<p≤√n 覆盖的比例；可检验目标是证明该覆盖比例严格小于 1，哪怕只对精心选择的模数和区间成立。
- 来源核对：当前问题页仍标为 OPEN，并记录例外数 ≪x/(log x)^c：[Erdős Problems #676](https://www.erdosproblems.com/676)。；候选答案所提未经核验的 2025 预印本不是本次证明尝试所需依据，故未采用。
- 时间记账：所在批次墙钟时间按题数均摊约 55.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/676)；既有候选答案（按不可信材料审计）

### #677

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $M(n,k)=[n+1,\ldots,n+k]$ be the least common multiple of $\{n+1,\ldots,n+k\}$. Is it true that for all $m\geq n+k$\[M(n,k) \neq M(m,k)?\]
- 题意摘要：对所有自然数 n,m 及正整数 k，若 m≥n+k（两个长度同为 k 的整数区间不相交），是否必有 M(n,k)=lcm(n+1,…,n+k)≠M(m,k)？
- 状态核对：官方页面仍标为 open；固定 k 时由 Thue–Siegel 只能得到反例对 (m,n) 有限，不能排除全部反例。先前候选的 k=1,2 结论正确，但没有推进一般情形。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：采用逐素数赋值比较。若两个 LCM 相等，则对每个素数 p，两个区间中 v_p 的最大值相同；尝试证明后一区间必出现一个超过 n+k 的素数幂因子，从而矛盾。
- 局部结论：k=1 时等式迫使 m=n，与 m≥n+1 矛盾；k=2 时 M(n,2)=(n+1)(n+2)，该量随 n 严格递增，故命题成立。；若 M(n,k)=M(m,k)，则对每个 j≤k 及每个素数幂 p^a∣m+j，必有 p^a≤n+k：否则前一区间没有数能被 p^a 整除，两个 LCM 的 p-adic 赋值不可能相等。；特别地，后一区间每个 m+j 的全部素数幂因子均受 n+k 控制；若其中存在素因子 p>n+k，立即得到矛盾。
- 第一阻塞点：第一处缺口是无法证明任意不相交的后一区间必含某个数，其某一素数幂因子超过 n+k。光滑数可以成簇出现；现有固定 k 有限性结果也不提供“零个例外”。
- 下一步：固定 k=3，穷尽三个数的 p-adic 最大值模式，把假设 M(n,3)=M(m,3) 化为有限组 Thue 型方程；先检验能否无条件排除这一最小未解长度。
- 来源核对：[官方题页：状态、Thue–Siegel 有限性及已知异长例子](https://www.erdosproblems.com/677)；本地 Lean 陈述确实量化 m,n,k∈ℕ，并显式要求 k>0；与题面一致。
- 时间记账：所在批次墙钟时间按题数均摊约 47.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/677)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/677.lean`；既有候选答案（按不可信材料审计）

### #679

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$ and $\omega(n)$ count the number of distinct prime factors of $n$. Are there infinitely many values of $n$ such that\[\omega(n-k) < (1+\epsilon)\frac{\log k}{\log\log k}\]for all $k<n$ which are sufficiently large depending on $\epsilon$ only? Can one show the stronger version with\[\omega(n-k) < \frac{\log k}{\log\log k}+O(1)\]is false?
- 题意摘要：第一问的精确量词是：对每个 ε>0，是否存在只依赖 ε 的 K，使得有无穷多个 n 满足对所有 K≤k<n，ω(n−k)<(1+ε)log k/loglog k？第二问询问把右端改成 log k/loglog k+C（统一常数误差）的版本是否必然失败。
- 状态核对：第一问仍 open；第二问已有反证，而且官方页面记录了更强的正偏差 c·log k/(loglog k)^2。2026 年页面另记载 Lau 的上界 C log k，但尚未解决第一问。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：审查先前候选的 primorial 构造。其取“紧邻 n 的前一个 primorial”会使 k=n−P_r 可能等于 1，不能满足 k→∞，因此原论证有实质缺口。可改取再往前一个 primorial。令 P_r=∏_{j≤r}p_j，并选 r 使 P_{r+1}<n≤P_{r+2}，取 k=n−P_r。
- 局部结论：此时 k≥P_{r+1}−P_r=P_r(p_{r+1}−1)→∞，且 n−k=P_r，所以 ω(n−k)=r。；又有 k<P_{r+2}。由标准的第 r 个素数及 Chebyshev θ 函数二阶渐近，可得 log P_{r+2}/loglog P_{r+2}≤r−c r/log r（充分大 r，某个绝对 c>0）。；因 x/loglog x 最终递增，遂有 ω(n−k)≥log k/loglog k+c'log k/(loglog k)^2；故对每个充分大 n 都存在一个趋于无穷的 k 破坏任意固定加法常数版本。
- 第一阻塞点：这条路线只给出相对误差 1+Θ(1/loglog k)，仍小于任何固定 ε；因此不能否定或证明第一问的 (1+ε) 界。若要完全严格重建第二问，还需写明所用 p_r、θ(p_r) 的带余项二阶估计及常数传递。
- 下一步：把修正后的 P_r 构造写成引理，并用一个明确可引用的 p_r=r(log r+loglog r−1+O(loglog r/log r)) 估计逐项验证常数 c；这也会彻底排除先前候选的“小 k”漏洞。
- 来源核对：[官方题页：第一问 open、第二问的定量反证及 Lau 部分结果](https://www.erdosproblems.com/679)；先前候选的选择 P_{m−1}<n≤P_m、k=n−P_{m−1} 不保证 k 足够大；例如 n=P_{m−1}+1 时 k=1。
- 时间记账：所在批次墙钟时间按题数均摊约 47.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/679)；既有候选答案（按不可信材料审计）

### #680

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for all sufficiently large $n$, there exists some $k$ such that\[p(n+k)>k^2+1,\]where $p(m)$ denotes the least prime factor of $m$? Can one prove this is false if we replace $k^2+1$ by $e^{(1+\epsilon)\sqrt{k}}+C_\epsilon$, for all $\epsilon>0$, where $C_\epsilon>0$ is some constant?
- 题意摘要：第一问：是否存在 N，使每个 n≥N 都有正整数 k 满足最小素因子 p(n+k)>k²+1？第二问：对每个 ε>0，是否存在 Cε>0，使上述“最终对每个 n 都有见证”的断言在阈值 exp((1+ε)√k)+Cε 下为假，即存在任意大的无见证 n？
- 状态核对：两部分官方仍标为 open。本地 Lean 第二部分的量词正是 ∀ε>0 ∃C>0，¬(最终对所有 n 存在 k)。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把见证分为 n+k 为素数与合数两类，并严格确定合数见证的可行范围；第二部分则从“无见证”推出 Cramér 尺度的素数空区间。
- 局部结论：若 n+k 合数，则 p(n+k)≤√(n+k)。若 k⁴≥n，则 (k²+1)²=k⁴+2k²+1>n+k，因此合数不可能成为见证；所以这一区域的见证只能是素数。；若在 (n,n+√n−1] 中有素数 q=n+k，则 q>k²+1，因而第一问成立。故“每个充分大 n 后 √n 内有素数”是足够条件，但远强于目前可用结果。；对指数阈值，若无见证，则在所有满足 exp((1+ε)√k)+Cε<n+k 的 k 上都不能有 n+k 为素数；因此得到长度约 (log n)²/(1+ε)² 的素数空区间。
- 第一阻塞点：第一问的合数小 k 区域 k<n^{1/4} 仍可能提供粗数见证，现有路线无法统一控制。第二问中 Cramér 尺度素数空区间只是反例的必要条件，并非充分条件：区间内的合数还必须各自具有不超过指数阈值的小素因子。先前候选把“构造大素数间隙”近似当成充分条件，论证未闭合；其 √n+1>√(2n) 也明显错误，虽可用上面的平方恒等式修复相关结论。
- 下一步：研究一个有限覆盖同余系：对 1≤k≤K≈(log n)²/(1+ε)²，指定小素数 q_k≤exp((1+ε)√k)+Cε 且令 q_k∣n+k；检验筛覆盖能否兼容 CRT 并产生任意大的 n。
- 来源核对：[官方题页：两问 open 及 Cramér/Granville 启发](https://www.erdosproblems.com/680)；本地 Lean 陈述要求 k≠0；第二问的否定量词与上述重述一致。
- 时间记账：所在批次墙钟时间按题数均摊约 47.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/680)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/680.lean`；既有候选答案（按不可信材料审计）

### #681

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that for all large $n$ there exists $k$ such that $n+k$ is composite and\[p(n+k)>k^2,\]where $p(m)$ is the least prime factor of $m$?
- 题意摘要：是否存在 N，使每个 n≥N 都有正整数 k，令 n+k 为合数且其最小素因子严格大于 k²？这里素数 n+k 明确不算见证。
- 状态核对：官方仍为 open。先前候选仅给必要大小界，没有利用奇偶性把困难 n 精确缩减。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先按 n 的奇偶性及 n+1 的素合性分类，再在唯一困难类 n=p−1 中筛选可能的 k。
- 局部结论：若 n 为奇数，则 n+1 为偶合数，取 k=1，且 p(n+1)=2>1，立即成立。；若 n 为偶数且 n+1 为合数，同样 k=1 成立。因此唯一需要处理的是 n=p−1，其中 p 为奇素数。；在 n=p−1 情形，偶数 k 使 n+k 为偶数且最小素因子为 2≤k²，所以见证必须是奇数 k≥3；又因合数的最小素因子≤√(n+k)，必要条件为 k⁴<n+k。
- 第一阻塞点：需证明对每个充分大素数 p，都存在某个奇数 3≤k≲p^{1/4}，使 p−1+k 合数且没有不超过 k² 的素因子。普通筛法可统计避开小素数的数，却难以同时保证留下的数是合数而非素数，并且筛限 k² 随 k 变化。
- 下一步：对区间 3≤k≤p^{1/4}/2 的奇数建立变筛限集合 {k:q∤p−1+k 对所有 q≤k²} 的下界，再减去其中 p−1+k 为素数的数量；检查现有上界筛是否能产生正差。
- 来源核对：[官方题页：状态与精确题面](https://www.erdosproblems.com/681)；本地 Lean 陈述明确要求 k>0、n+k 合数，并以最小素因子条件表达严格不等式。
- 时间记账：所在批次墙钟时间按题数均摊约 47.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/681)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/681.lean`；既有候选答案（按不可信材料审计）

### #683

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that for every $1\leq k\leq n$ the largest prime divisor of $\binom{n}{k}$, say $P(\binom{n}{k})$, satisfies\[P\left(\binom{n}{k}\right)\geq \min(n-k+1, k^{1+c})\]for some constant $c>0$?
- 题意摘要：是否存在一个绝对常数 c>0，使所有 1≤k≤n 都满足 P(C(n,k))≥min(n−k+1,k^{1+c})？边界 k=n 时 C(n,n)=1，须采用 P(1)=1 的约定；本地 Lean 版本则只量化 0<k<n，并把 ≥ 改成严格 >，并非逐字等价。
- 状态核对：官方仍为 open；Sylvester–Schur 给 k≤n/2 时 P(C(n,k))>k，Erdős 给出 ≫k log k，但尚达不到固定幂增益。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：利用二项式对称性 C(n,k)=C(n,n−k)，先完整处理 k>n/2，再把真正开放部分缩到 k≤n/2。
- 局部结论：设 k>n/2 且 k<n，令 j=n−k，则 1≤j<n/2。Sylvester–Schur 应用于 C(n,j) 给 P(C(n,k))=P(C(n,j))>j=n−k。因两边为整数，P≥n−k+1，故题设不等式在整个 k>n/2 区域成立，且不依赖 c。；k=n 的边界在约定 P(1)=1 时为等号；k=1 时右端为 1，也平凡成立。因此困难核心确为 2≤k≤n/2。；在困难区，已知 P≫k log k 只能达到对数增益；对任何固定 c>0，k log k=o(k^{1+c})，故不能直接推出所需 k^{1+c}。
- 第一阻塞点：第一处缺口是在 k≤n/2 且 n−k+1≥k^{1+c} 时必须证明 P(C(n,k))≥k^{1+c}；现有统一下界 k log k 与目标之间仍有固定幂级差距。素数间隙启发不能替代该一致估计。
- 下一步：按等价问题 #961 的路线，把“所有相关素因子≤k^{1+c}”转写为区间乘积 n(n−1)…(n−k+1) 的光滑性约束；首先对 n≥k² 检验现有光滑数间隔定理能否给出任何显式 c>0 的子范围。
- 来源核对：[官方题页：状态、Sylvester–Schur、Erdős下界及与 #961 的关系](https://www.erdosproblems.com/683)；本地 Lean 文件排除了 k=n 且使用严格 >；筛查时采用题面原始的 ≥ 版本，并明确处理边界约定。
- 时间记账：所在批次墙钟时间按题数均摊约 47.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/683)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/683.lean`；既有候选答案（按不可信材料审计）

### #684

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For $0\leq k\leq n$ write\[\binom{n}{k} = uv\]where the only primes dividing $u$ are in $[2,k]$ and the only primes dividing $v$ are in $(k,n]$. Let $f(n)$ be the smallest $k$ such that $u>n^2$. Give bounds for $f(n)$.
- 题意摘要：对每个整数 n 及 0≤k≤n，将 \(\binom nk\) 唯一分解为 \(uv\)，其中 \(u\) 保留全部素因子 \(p≤k\) 的幂，\(v\) 保留全部 \(k<p≤n\) 的幂；\(f(n)\) 是首个满足 \(u>n^2\) 的 k。问题要求其增长上下界。
- 状态核对：按冻结日期仍为开放题。旧候选的中心二项式路线正确，但只给很弱的线性上界，不能视为解决。当前网页含 2026 年后的更强声明，因晚于 cohort 截止日未纳入结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：取 \(k=\lfloor n/2\rfloor\)。此时 v 的素因子均大于 \(n/2\)（奇数 n 时多出的边界素数只会使下面的整除上界更宽），且在 \(\binom nk\) 中指数至多 1，故 \(v\mid\prod_{n/2<p≤n}p\)。结合 \(\binom n{\lfloor n/2\rfloor}≥2^n/(n+1)\) 和素数定理估计 u。下界方向则对每个固定 k 应用 Mahler 于连续乘积 \((n-k+1)\cdots n\)。
- 局部结论：\(\log u≥n\log2-\log(n+1)-[\vartheta(n)-\vartheta(n/2)]=(\log2-1/2)n+o(n)\)，所以充分大 n 时 \(f(n)≤\lfloor n/2\rfloor\)。；固定 k 时，令 A 为 \((n-k+1)\cdots n\) 的 k-smooth 部分，则 \(u=A/k!\)。Mahler 给出任意 \(\eta>0\) 下 \(A<n^{1+\eta}\) 最终成立；取 \(\eta<1\) 得 \(u<n^2\)。；因此对每个固定 K，存在不可计算的 \(N(K)\)，使 \(n≥N(K)\Rightarrow f(n)>K\)，即 \(f(n)\to\infty\)。
- 第一阻塞点：中心项路线只在 k 与 n 同阶时留下指数级的小素数部分；若令 \(k=o(n)\)，对 \(v\) 使用全部大素数乘积会严重过估，无法推出次线性上界。Mahler 的常数又依赖 k 且无效，不能反演成显式下界。
- 下一步：对 \(k=n^\alpha\) 写出 Kummer 条件 \(n\bmod p^a<k\bmod p^a\)，分素数幂区间估计 \(\log u\)；首个可检验目标是证明某个明确 \(\alpha<1\) 时 \(\log u>2\log n\)。
- 来源核对：冻结表述及 Mahler 背景与[问题页](https://www.erdosproblems.com/684)一致。；旧候选的 \(f(n)≤n/2\) 推导已逐式核对；其引用的非原始网页不是证明所必需。
- 时间记账：所在批次墙钟时间按题数均摊约 44.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/684)；既有候选答案（按不可信材料审计）

### #685

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$ and $n$ be large depending on $\epsilon$. Is it true that for all $n^\epsilon<k\leq n^{1-\epsilon}$ the number of distinct prime divisors of $\binom{n}{k}$ is\[(1+o(1))k\sum_{k<p<n}\frac{1}{p}?\]Or perhaps even when $k \geq (\log n)^c$?
- 题意摘要：固定 \(\epsilon>0\)，要求当 n 充分大时，对所有 \(n^\epsilon<k≤n^{1-\epsilon}\)，证明或否定 \(\omega\binom nk=(1+o(1))k\sum_{k<p<n}p^{-1}\)，其中 o(1) 必须在该 k 匏围内一致；并询问能否降至 \(k≥(\log n)^c\)。
- 状态核对：开放。旧候选有一处明确错误：p>k 时区间中虽至多有一个 p 的倍数，但该整数可能被 \(p^2\) 整除，故 \(v_p\binom nk\) 不一定属于 \(\{0,1\}\)，如 \(v_3\binom{10}{2}=2\)。其“按 n 平均后立即由 CRT 和 Chebyshev 得证”也未控制截断边界误差。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：只计不同素数。对 p>k，Kummer 定理仍严格给出 \(p\mid\binom nk\iff n\bmod p<k\)。再按 \(q=\lfloor n/p\rfloor\) 分组，将问题化为许多短区间中的素数计数。
- 局部结论：令 \(S(n,k)=\#\{p:k<p≤n,\ n\bmod p<k\}\)，则 \(\omega\binom nk=S(n,k)+O(\pi(k))\)。；在给定幂次范围内 \(\pi(k)=o(k)\)，而 \(k\sum_{k<p<n}1/p\asymp_\epsilon k\)，故小素数贡献确为相对误差 o(1)。；精确分组为 \(S(n,k)=\sum_{q≤n/k}\#\{p:\max(k,(n-k)/q)<p≤n/q\}\)，端点按严格不等式调整。每段长度约 \(k/q\)。
- 第一阻塞点：要把上述总和替换成期望主项，需对中心约为 \(n/q\)、长度仅约 \(k/q\) 的大量短区间统一作素数定理级估计；现有一般短区间控制不足以覆盖全部 \(n^\epsilon<k\)。这正是第一处无法闭合之处。
- 下一步：先截取 \(q≤Q\) 与 \(q>Q\)，用现有短区间素数定理处理前段、筛法上界处理尾段；检验能否在某个明确子范围 \(k≥n^\theta\) 得到所需总误差 o(k)。
- 来源核对：[冻结问题页及讨论](https://www.erdosproblems.com/685)确认全范围仍开放，并明确指出其与短区间素数分布的关系。；旧候选关于 p-adic 指数及“几乎所有 n”的论证已独立否定；但其整除判据本身成立。
- 时间记账：所在批次墙钟时间按题数均摊约 44.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/685)；既有候选答案（按不可信材料审计）

### #686

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Can every integer $N\geq 2$ be written as\[N=\frac{\prod_{1\leq i\leq k}(m+i)}{\prod_{1\leq i\leq k}(n+i)}\]for some $k\geq 2$ and $m\geq n+k$?
- 题意摘要：按预期及本地形式化，量词是：对每个自然数 \(N≥2\)，是否存在自然数 \(k,n,m\)，满足 \(k≥2\)、\(m≥n+k\)，且 \(N=\prod_{i=1}^k(m+i)/\prod_{i=1}^k(n+i)\)。
- 状态核对：总问题开放。人工评审指出的错误必须吸收：旧候选取 \(n=-2N\)，不在自然数论域，因而不是解。本地 Lean 文件也明确使用 \(n,m:\mathbb N\)。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：固定 \(k=2\)。方程等价于 \((2m+3)^2-N(2n+3)^2=1-N\)。对非平方 N，取 Pell 单位 \(a+b\sqrt N\) 满足 \(a^2-Nb^2=1\)，并令 \(X+Y\sqrt N=(1+\sqrt N)(a+b\sqrt N)\)。
- 局部结论：由乘法范数，\(X=a+Nb\)、\(Y=a+b\) 满足 \(X^2-NY^2=1-N\)。；把任意正 Pell 单位平方，可保证 a 为奇数、b 为偶数；取足够高次还可令 X、Y≥3，故 \(m=(X-3)/2,n=(Y-3)/2\) 是自然数。；\(X-Y=(N-1)b\) 可任意大，故最终 \(m≥n+2\)。因此每个非平方 \(N≥2\) 都已有严格的 k=2 表示。
- 第一阻塞点：当 \(N=s^2\) 时 Pell 方程退化，以上无限单位机制消失；尚无统一处理所有平方 N 的 k 构造。这是总量词的首个未闭合分支。
- 下一步：先固定最小未解决平方值并逐个检验 k=3：化为 \((m+2)^3-(m+2)=N[(n+2)^3-(n+2)]\)，再对所得三次曲线做严格的整数点/Thue 方程归约，而非仅搜索有理点。
- 来源核对：已读取并核对本地 [686.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/686.lean)，其中自然数量词及非平方 Pell 路线与上述重建一致。；[官方页面](https://www.erdosproblems.com/686)仍列总问题为开放；其讨论也明确否定负 n 构造作为预期版本的解。
- 时间记账：所在批次墙钟时间按题数均摊约 44.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/686)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/686.lean`；既有候选答案（按不可信材料审计）

### #687

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $Y(x)$ be the maximal $y$ such that there exists a choice of congruence classes $a_p$ for all primes $p\leq x$ such that every integer in $[1,y]$ is congruent to at least one of the $a_p\pmod{p}$. Give good estimates for $Y(x)$. In particular, can one prove that $Y(x)=o(x^2)$ or even $Y(x)\ll x^{1+o(1)}$?
- 题意摘要：对每个实数 x，给每个素数 p≤x 任选一个剩余类 \(a_p\pmod p\)；\(Y(x)\) 是能使每个整数 \(1≤t≤y\) 至少落入一个所选类的最大整数 y。目标是估计 Y，特别是证明 \(o(x^2)\) 或 \(x^{1+o(1)}\) 上界。
- 状态核对：开放；冻结背景中的已知界为 \(x\log x\log_3x/\log_2x\ll Y(x)\ll x^2\)。旧候选对此状态的陈述基本正确。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：用中国剩余定理选 M 满足 \(M\equiv-a_p\pmod p\)。覆盖 \([1,y]\) 等价于 \(M+1,\ldots,M+y\) 均与 \(P(x)=\prod_{p≤x}p\) 不互素，即化为 Jacobsthal 最大空段。上界路线套用 Iwaniec 对 r 个素数的移位筛界。
- 局部结论：按常见 Jacobsthal 约定，\(Y(x)=j(P(x))-1\)；差 1 仅来自 j 的端点定义。；可直接证明粗下界 \(Y(x)≥\lfloor x/2\rfloor\)：令 \(r=\lfloor x/2\rfloor\)，用 p≤r 的零剩余类覆盖 2,…,r，再由 Bertrand 定理取 r<q≤x，以 \(a_q=1\) 覆盖 1。；Iwaniec 的 \(C(r)\ll r^2(\log r)^2\) 与 \(r=\pi(x)\) 给出 \(Y(x)\ll\pi(x)^2(\log\pi(x))^2\ll x^2\)。
- 第一阻塞点：该移位筛估计在临界筛选长度只给固定常数倍的二次界；现有推导中没有随 x 消失的节省，因而连 \(o(x^2)\) 都不能推出。
- 下一步：在 Iwaniec 的筛下界中保留 r、筛选层级和余项的显式依赖，检验是否任何参数选择能把 \(C(r)/(r^2\log^2r)\) 压到 o(1)；若不能，应精确定位线性筛极限处的损失。
- 来源核对：[官方问题页](https://www.erdosproblems.com/687)记录 Iwaniec 上界、FGKMT 下界及 Maier–Pomerance 猜想。；核对了[Iwaniec 原论文书目信息](https://doi.org/10.1515/dema-1978-0121)及 [FGKMT 的 JAMS 论文](https://doi.org/10.1090/jams/876)。
- 时间记账：所在批次墙钟时间按题数均摊约 44.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/687)；既有候选答案（按不可信材料审计）

### #688

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Define $\epsilon_n$ to be maximal such that there exists some choice of congruence class $a_p$ for all primes $n^{\epsilon_n}<p\leq n$ such that every integer in $[1,n]$ satisfies at least one of the congruences $\equiv a_p\pmod{p}$. Estimate $\epsilon_n$ - in particular is it true that $\epsilon_n=o(1)$?
- 题意摘要：对固定 n 和实数 ε，只允许使用素数 \(n^ε<p≤n\)，每个素数选一个剩余类；要求覆盖全部 \(1,…,n\)。\(\epsilon_n\) 应理解为所有可行 ε 的上确界，并问其数量级及是否趋于 0。
- 状态核对：开放。严格说“最大值”可能因 \(n^ε<p\) 的严格不等式而不取到；本地形式化正确地使用 sSup。旧候选的容量上界有效，但其“光滑数后用大素数收尾”只是启发式，未给出不重复使用素数的完整构造。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：采用覆盖容量计数。一个模 p 的类在 \([1,n]\) 中至多命中 \(n/p+1\) 个整数；若完全覆盖，则所有命中数之和至少为 n。再用素数倒数的 Mertens 公式。
- 局部结论：任一可行 ε 满足 \(1≤\sum_{n^ε<p≤n}1/p+\pi(n)/n\)。；若 ε 沿某子列有正下界，则 Mertens 公式一致给出 \(\sum_{n^ε<p≤n}1/p=-\log ε+o(1)\)。；因此 \(\limsup\epsilon_n≤e^{-1}\)，等价地 \(\epsilon_n≤e^{-1}+o(1)\)。结合冻结背景中的 Erdős 结果，有 \(\log_3n/\log_2n\ll\epsilon_n≤e^{-1}+o(1)\)。
- 第一阻塞点：容量计数完全忽略不同剩余类的重叠；要证明 \(\epsilon_n=o(1)\)，必须对每个固定 δ>0 证明使用 \(n^δ<p≤n\) 时必有未覆盖点。直接二阶容斥的每对余项累积过大，无法给出正的未覆盖数。
- 下一步：固定 δ>0，把目标改写为：任意这些剩余类的补集非空；按 p≤√n 与 p>√n 分层，尝试用大筛或覆盖系统不等式证明统一的未覆盖下界。首个检验指标是能否把交叠误差控制到 o(n)。
- 来源核对：已核对本地 [688.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/688.lean)：定义使用实数 ε 的上确界，且记录 Erdős 下界。；[官方问题页](https://www.erdosproblems.com/688)仍将 \(\epsilon_n=o(1)\) 列为开放问题。
- 时间记账：所在批次墙钟时间按题数均摊约 44.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/688)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/688.lean`；既有候选答案（按不可信材料审计）

### #689

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n$ be sufficiently large. Is there some choice of congruence class $a_p$ for all primes $2\leq p\leq n$ such that every integer in $[1,n]$ satisfies at least two of the congruences $\equiv a_p\pmod{p}$?
- 题意摘要：量词为：是否存在 N，使每个 n≥N 都能为每个素数 p≤n 选一个剩余类 a_p mod p，并使每个 m∈{1,…,n} 至少被两个不同素数对应的同余式 m≡a_p (mod p) 命中。
- 状态核对：仍应按开放题处理。官方页面虽记录了若干 AI 辅助的完整证明声称，但明确表示关键加权矩估计尚待专家或同行评审核验，不能据此宣布解决。旧候选只报告开放状态，没有作实质证明尝试。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：概率法近似覆盖：对每个 p≤n 独立均匀选择 a_p mod p。固定 m，令 X_m 为命中它的素数数目。则各命中事件独立且概率为 1/p。先证明存在一种选择，使覆盖次数不足二的整数只有 O(n loglog n/log n) 个，再尝试用保留素数清理这些例外。
- 局部结论：令 V(n)=∏_{p≤n}(1−1/p)、S(n)=∑_{p≤n}1/(p−1)，则严格有 P(X_m<2)=V(n)(1+S(n))，与 m 无关。；因此坏点数 B 满足 E B=nV(n)(1+S(n))；由 Mertens 估计，存在一组选类使 B=O(n loglog n/log n)。；这给出了真实的“几乎双覆盖”，但远不足以推出零坏点；相比全取 a_p=0，它也避免了只处理 1 与素数幂的误导性简化。
- 第一阻塞点：第一处无法闭合的是清理坏点：若先固定大部分 a_p，改变某个剩余类会同时影响约 n/p 个整数；目前没有严格的匹配或吸收论证，能在覆盖全部坏点的同时保证原有双覆盖不被破坏。
- 下一步：做一个可检验的两阶段实验/引理：只用 p≤z 随机预覆盖，精确记录每个坏点可用的保留素数 p∈(z,n]，检验所得坏点—剩余类超图是否满足可应用 nibble/匹配定理的度与共度条件。
- 来源核对：本地 Lean 文件确实形式化为 eventually n、存在函数 a、对每个 m∈[1,n] 过滤出的命中素数基数至少 2；但定理正文仍为 `sorry`。；[官方问题页及讨论](https://www.erdosproblems.com/689)目前仍标为 OPEN，并把现有完整证明称为待核验声称。
- 时间记账：所在批次墙钟时间按题数均摊约 65.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/689)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/689.lean`；既有候选答案（按不可信材料审计）

### #690

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $d_k(p)$ be the density of those integers whose $k$th smallest prime factor is $p$ (i.e. if $p_1<p_2<\cdots$ are the primes dividing $n$ then $p_k=p$). For fixed $k\geq 1$ is $d_k(p)$ unimodular in $p$? That is, it first increases in $p$ until its maximum then decreases.
- 题意摘要：对每个固定整数 k≥1及依次排列的素数 p，d_k(p) 是满足“p 为该整数第 k 个最小的不同素因子”的正整数集合的自然密度。问题可理解为逐 k 判定序列 p↦d_k(p) 是否先不减后不增。
- 状态核对：已知完整分类为：k≤3 单峰，k≥4 非单峰。必须吸收人工评语：旧候选的 k=4 反例只能否定“对所有 k 都单峰”的统一命题，不能回答逐个固定 k 的一般分类。2026 年 Wang–Crapis 预印本补出了所有 k≥4 的统一论证。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `medium`
- 尝试路线：先独立推导密度公式并精确复算最小反例；一般路线则研究相邻素数处的一阶差分，把符号化为素数间隔与初等对称多项式比值的比较，再分别制造一次下降和稍后一次上升。
- 局部结论：严格公式为 d_k(p)=p⁻¹∏_{q<p}(1−1/q)·e_{k−1}((1/(q−1))_{q<p})。这是有限 CRT 独立性直接给出的自然密度。；独立有理数计算确认 d_4(13)=31/5005>d_4(17)=206/36465<d_4(19)=1308/230945，故 k=4 确实非单峰。；已知完整路线利用精确差分阈值：较大素数间隔造成严格下降，稍后的较小间隔造成严格上升；有限范围由证书计算处理，统一尾部由素数分布估计与 CRT 构造处理。
- 第一阻塞点：本次受限重建首先未独立闭合的是“对所有足够大 k，统一构造先大后小的两个合适素数间隔，并验证对称多项式阈值”的整段估计；k=4 的局部反例本身已经完全闭合。
- 下一步：运行论文公开的精确 verifier，并逐项核对它引用但不重证的显式素数估计、记录素数间隔和 CRT 构造；这正是从局部反例升级到全 k 分类所需的可检验步骤。
- 来源核对：[Cambie 2025](https://arxiv.org/abs/2501.10333)证明 k≤3，并计算验证 4≤k≤20 非单峰。；[Wang–Crapis 2026](https://arxiv.org/abs/2605.08542)陈述并给出所有 k≥4 非单峰的完整分类及公开数值验证器。；[官方讨论](https://www.erdosproblems.com/forum/thread/690?order=oldest)解释了旧“solved”解释歧义及随后全 k 稿件的核验情况。
- 时间记账：所在批次墙钟时间按题数均摊约 65.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/690)；既有候选答案（按不可信材料审计）

### #691

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Given $A\subseteq \mathbb{N}$ let $M_A=\{ n \geq 1 : a\mid n\textrm{ for some }a\in A\}$ be the set of multiples of $A$. Find a necessary and sufficient condition on $A$ for $M_A$ to have density $1$.
- 题意摘要：给定任意 A⊆N，M_A 是至少被一个 a∈A 整除的正整数集合。要求用 A 自身的结构给出 M_A 的自然密度存在且等于 1 的充要条件；1∈A 时结论当然成立。
- 状态核对：仍开放。旧候选给出的“有限子集 F⊂A 的倍数密度可任意接近 1”在 Davenport–Erdős 定理下是逻辑等价表述，但本质上重新编码了待判定密度，并不是所求的结构性刻画，不能据此声称解题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从倒数和及互素子族入手：证明无 1 时倒数和发散是必要条件；若 A 含有倒数和发散的两两互素子族，则证明充分。然后检查这两者之间能否通过 gcd/lcm 结构补齐。
- 局部结论：若 1∉A 且 d(M_A)=1，则必有 ∑_{a∈A}1/a=∞。否则取有限 F 使尾和小于 1−d(M_F)；由并集上界，尾部倍数集的上密度不超过尾和，从而 M_A 的上密度小于 1，矛盾。；若存在两两互素 B⊆A 且 ∑_{b∈B}1/b=∞，则有限 B_r 的未覆盖密度为 ∏_{b∈B_r}(1−1/b)→0，故 d(M_A)=1。；对任意有限 F，d(M_F) 可用周期 L=lcm(F) 或容斥精确计算；Davenport–Erdős 给出的 sup_F d(M_F)=1 是有效等价判据，但尚非结构分类。
- 第一阻塞点：第一处无法闭合的是从一般 A 的倒数和发散推出足够独立的互素或低相关子族。大量公因子会使倍数集高度重叠；官方给出的块序列 η_k=1/k 正说明倒数质量发散仍可能密度小于 1。
- 下一步：在 primitive reduction（删去被 A 中其他元素整除的元素）后，计算有限截断的 lcm 容斥量，并检验能否以可量化的 gcd 能量条件控制重叠；先证明一个形如“二阶 gcd 能量有限 ⇒ Behrend”的充分判据。
- 来源核对：[官方问题页](https://www.erdosproblems.com/691)仍标为 OPEN，并明确记录 η_k=1/k 的反例现象及 Tenenbaum 的受控块序列阈值 β=log 2。
- 时间记账：所在批次墙钟时间按题数均摊约 65.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/691)；既有候选答案（按不可信材料审计）

### #693

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ and $n$ be sufficiently large depending on $k$. Let $A=\{a_1<a_2<\cdots \}$ be the set of those integers in $[n,n^k]$ which have a divisor in $(n,2n)$. Estimate\[\max_{i} a_{i+1}-a_i.\]Is this $\leq (\log n)^{O(1)}$?
- 题意摘要：固定 k≥2；对充分大的 n，令 A_n={m∈Z:n≤m≤n^k，存在整数 d 满足 n<d<2n 且 d|m}，按升序写成有限序列 a_1<⋯<a_t。目标估计内部最大间隔 max_{1≤i<t}(a_{i+1}−a_i)，特别问是否由只依赖 k 的某个 log n 幂控制。
- 状态核对：仍开放。旧候选的总体尺度基本合理，但其端点修正写成 O(n) 对 k>2 不正确：把 Ford 的 (n,2n] 改为题目的 (n,2n) 最多删除约 n^{k−1}/2 个 2n 的倍数，而非 O(n)。这仍是低阶项。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：结合一个确定性网格上界与 Ford 的全局计数下界：固定合法除数 d=n+1，其全部倍数都属于 A；另一方面以 H(n^k,n,2n) 估计 |A|，再由总跨度推出至少一个平均尺度的大间隔。
- 局部结论：因 d=n+1 合法，A 含有 (n+1),2(n+1),…；首项就是 n+1，末个该类倍数距 n^k 小于 n+1，所以每个内部间隔严格小于或等于 n+1。；Ford 定理给 H(n^k,n,2n)≍n^k/((log n)^δ(loglog n)^{3/2})，δ=1−(1+loglog2)/log2。删除除数恰为 2n 的倍数只损失 O(n^{k−1})，故 |A| 仍具有同一量级。；A 的首末项跨度为 n^k−O(n)，所以最大间隔至少为常数倍的 (log n)^δ(loglog n)^{3/2}。因此严格可得 (log n)^δ(loglog n)^{3/2}≪max gap≤n+1。
- 第一阻塞点：第一处无法闭合的是把 Ford 的全局计数局部化到每一个长度 (log n)^C 的短区间。平均密度不能排除稀有长空洞，而现有路线没有所需的统一短区间下界。
- 下一步：明确证明一个充分的短区间命题：寻找固定 C(k)，使所有 x∈[n,n^k−(log n)^C] 都满足 H(x+(log n)^C,n,2n)−H(x,n,2n)>0；先在较长尺度 n^θ 上测试筛法能达到的最小 θ。
- 来源核对：[官方问题页](https://www.erdosproblems.com/693)仍标为 OPEN。；[Ford 的定理](https://arxiv.org/abs/math/0607473)给出 3≤y≤√x 时 H(x,y,2y) 的正确数量级。
- 时间记账：所在批次墙钟时间按题数均摊约 65.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/693)；既有候选答案（按不可信材料审计）

### #694

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $f_{\max}(n)$ be the largest $m$ such that $\phi(m)=n$, and $f_{\min}(n)$ be the smallest such $m$, where $\phi$ is Euler's totient function. Investigate\[\max_{n\leq x}\frac{f_{\max}(n)}{f_{\min}(n)}.\]
- 题意摘要：只对 totient 值 n（即存在 m 使 φ(m)=n）定义纤维极值 f_min(n)、f_max(n)，并令 R(x)=max_{n≤x, n∈im φ}f_max(n)/f_min(n)。结论是 x→∞ 时 R(x)=(e^γ+o(1))loglog x。
- 状态核对：按当前 cohort 应重建已知解。旧候选误报为开放且把关键下界留作猜想，已过时。还需精确说明“solved (Lean)”的信任边界：本地 FormalConjectures/694.lean 仍含 `sorry`；外部完整 Lean 文件无该占位，但把 Mertens 乘积定理和 Linnik 定理作为显式公理输入。这两者是经典无条件定理，因此数学归约有效，却不是仅靠当前 Mathlib 内核定理的零额外公理证明。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：上界用 totient 纤维有限性与 Landau 最大阶；下界构造同一 totient 的两个原像。令 P_Y=∏_{p≤Y}p、A_Y=φ(P_Y)=∏_{p≤Y}(p−1)。由 Linnik 取素数 ℓ≡1 mod A_YP_Y，置 U=(ℓ−1)/A_Y（故 P_Y|U），再令 Q 为 U 中大于 Y 的不同素因子的乘积。比较 a=ℓQ 与 b=P_YUQ。
- 局部结论：初等估计 m≤2φ(m)^2 保证每个正 totient 纤维有限；若 n≤x，则 f_max(n)≤2x²，且 f_max/f_min≤f_max/n=f_max/φ(f_max)。Landau–Mertens 因而给 R(x)≤(e^γ+o(1))loglog x。；上述构造可严格核算 φ(ℓQ)=φ(P_YUQ)，且 b/a=(P_Y/A_Y)((ℓ−1)/ℓ)。Mertens 给 P_Y/A_Y∼e^γlogY，而 ℓ→∞ 使第二因子趋于 1。；Linnik 的多项式界及 P_Y,A_Y≤4^Y 给共同 totient n≤exp(KY)。取 Y≈(log x)/K，便有 n≤x 且 logY=loglogx+O(1)，得到匹配下界。
- 第一阻塞点：作为数学重建，核心路线已闭合；本次核验的首个形式化信任边界是 Lean 文件中的 `mertens_product` 与 `linnik_dvd` 两个 axiom，而本地 cohort 定理本身仍是 `sorry`。因此不能描述成“完全由 Mathlib 已证明”。
- 下一步：用对应版本 Lean 运行外部 Proof.lean 的 `#print axioms totient_fibre_extremes`，确认依赖恰为内核公理加上述两个经典输入；随后把它适配回本地 FormalConjectures 定理签名并消除该文件的 `sorry`。
- 来源核对：[官方问题页](https://www.erdosproblems.com/694)现标为 SOLVED (LEAN)，并给出精确渐近式。；[外部 Lean 源文件](https://github.com/Shashi456/erdos-formalizations/blob/main/Erdos/P694/Proof.lean)明确列出 Mertens 与 Linnik 两项公理化输入，并形式化了碰撞构造和上下界归约。；本地 `/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/694.lean` 的主定理仍以 `by sorry` 结束，不能单凭该文件声称本地验证完成。
- 时间记账：所在批次墙钟时间按题数均摊约 65.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/694)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/694.lean`；既有候选答案（按不可信材料审计）

### #695

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p_1<p_2<\cdots$ be a sequence of primes such that $p_{i+1}\equiv 1\pmod{p_i}$. Is it true that\[\lim_k p_k^{1/k}=\infty?\]Does there exist such a sequence with\[p_k \leq \exp(k(\log k)^{1+o(1)})?\]
- 题意摘要：第一问量词是：对每个无限严格递增素数列 $(p_i)$，若 $p_{i+1}\equiv1\pmod{p_i}$，是否必有 $\log p_k/k\to\infty$。第二问是存在性：是否至少有一个这样的链满足 $\log p_k\le k(\log k)^{1+o(1)}$。
- 状态核对：截至核对日期仍开放。先验答案正确区分了“每条链”与“存在一条链”，但 Linnik 上界不能证明第一问；另外本地 Lean 文件把 $o(1)$ 写成了最终恒等于 1，并非正确形式化。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：写成 $p_{i+1}=a_i p_i+1$。研究乘子 $a_i$ 的几何平均；第二问则对最小后继素数采用条件估计 $p'\le p(\log p)^C$。
- 局部结论：除可能的首步外，$p_i,p_{i+1}$ 均为奇素数，故 $a_i$ 为正偶数，特别地 $a_i\ge2$，从而只能无条件推出 $p_k\gg2^k$。；由 $p_{i+1}>a_i p_i$ 得 $\log p_k>\log p_1+\sum_{i<k}\log a_i$；所以第一问可归约为证明所有无限素数链中乘子的平均对数趋于无穷。若结论失败，则存在无穷多个 $k$ 使该平均有界。；条件地，若每个素数 $p$ 都有后继 $p'\equiv1\pmod p$ 且 $p'\le p(\log p)^C$，令 $u_i=\log p_i$，则 $u_{i+1}\le u_i+C\log u_i$，比较递推可得 $u_k=O(k\log k)$，因而满足第二问的上界。
- 第一阻塞点：第一处无法闭合的是从“所有 $p_i$ 均为素数”推出 $\frac1k\sum_{i<k}\log a_i\to\infty$。固定乘子 $a_i=2$ 就成为无限 Cunningham 链问题，现有筛法无法排除；第二问所需的统一近线性最小素数进展估计也未知。
- 下一步：对给定阈值 $T$，尝试证明任意长度 $k$ 的链中 $a_i\le T$ 的步数至多 $(1-\delta_T)k$，且 $\delta_T\log T\to\infty$；先对固定有限乘子集合用组合筛给出可验证的有限链计数界。
- 来源核对：官方状态及 Linnik/条件最小素数路线：https://www.erdosproblems.com/695；已直接检查本地 FormalConjectures/ErdosProblems/695.lean；其中 `o =o[atTop] 1` 不表示 $o(k)\to0$。
- 时间记账：所在批次墙钟时间按题数均摊约 54.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/695)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/695.lean`；既有候选答案（按不可信材料审计）

### #696

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be the largest $\ell$ such that there is a sequence of primes $p_1<\cdots < p_\ell$ all dividing $n$ with $p_{i+1}\equiv 1\pmod{p_i}$. Let $H(n)$ be the largest $u$ such that there is a sequence of integers $d_1<\cdots < d_u$ all dividing $n$ with $d_{i+1}\equiv 1\pmod{d_i}$. Estimate $h(n)$ and $H(n)$. Is it true that $H(n)/h(n)\to \infty$ for almost all $n$?
- 题意摘要：对每个整数 $n$，$h(n)$ 是由整除 $n$ 的严格递增素数组成、相邻满足 $p_{i+1}\equiv1\pmod{p_i}$ 的最长链长；$H(n)$ 允许任意正整数因子。问题要求几乎所有 $n$ 的正常阶，并询问 $H(n)/h(n)$ 是否依自然密度趋于无穷。
- 状态核对：状态已变为 solved (Lean)。旧候选所称“比值问题仍开放”已经过时。现有结论为 $h(n)=(\tfrac12+o(1))\log_*n$、$H(n)=(1+o(1))\log_*n$，故比值几乎处处趋于 2，而非无穷。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `0/10`；置信度 `medium`
- 尝试路线：重建塔尺度证明：上界排除过短的相邻因子；下界在独立素因子模型中逐层构造后继，再以 CRT 转回均匀整数。素数后继使用 Siegel–Walfisz；复合后继使用有限阿贝尔群中的子集乘积等于单位元。
- 局部结论：若 $d<e$、$e\equiv1\pmod d$，则 $(d,e)=1$；两者都整除 $n$ 的整数比例至多约为 $1/(de)$。又对 $e<\exp\sqrt d$ 求和得到 $\sum 1/(de)\ll\sum d^{-3/2}$，故几乎所有 $n$ 不含大的“过短”步，推出 $H(n)=O(\log_*n)$。；在适当双指数窗口内，Siegel–Walfisz 给出 $q\equiv1\pmod p$ 的充分大倒数质量；独立模型中未选中任何后继的概率指数衰减，塔尺度迭代给出 $h(n)\gg\log_*n$。；精细塔级计数中素数步消耗两层、复合因子步消耗一层，得到 $h(n)=(\tfrac12+o(1))\log_*n$、$H(n)=(1+o(1))\log_*n$，从而 $H(n)/h(n)=2+o(1)$。
- 第一阻塞点：本次受限核查没有逐行重证精确常数所需的概率模型—CRT 转移及复合后继引理。Lean 工程无 `sorry`，但把 Siegel–Walfisz、Brun–Titchmarsh、Mertens作为三个显式公理输入；这些是标准定理，却不是在该工程内从 Mathlib 证明的。
- 下一步：运行 `#print axioms Erdos696.Main.erdos_696` 并逐项核对三个公理的量词、均匀范围与引用定理；随后单独审计产生常数 $1/2$ 和 $1$ 的塔层记账。
- 来源核对：官方更新与证明概要：https://www.erdosproblems.com/696；讨论串中的精确渐近式及路线：https://www.erdosproblems.com/forum/thread/696?order=newest；论文与 Lean 仓库、公理审计：https://github.com/davidturturean/erdos-696
- 时间记账：所在批次墙钟时间按题数均摊约 54.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/696)；既有候选答案（按不可信材料审计）

### #700

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[f(n)=\min_{1<k\leq n/2}\textrm{gcd}\left(n,\binom{n}{k}\right).\]{UL} {LI}Characterise those composite $n$ such that $f(n)=n/P(n)$, where $P(n)$ is the largest prime dividing $n$.{/LI} {LI}Are there infinitely many composite $n$ such that $f(n)>n^{1/2}$?{/LI} {LI} Is it true that, for every composite $n$,\[f(n) \ll_A \frac{n}{(\log n)^A}\]for every $A>0$?{/LI} {/UL}
- 题意摘要：对每个合数 $n$，在整数 $2\le k\le n/2$ 中取 $\gcd(n,\binom nk)$ 的最小值 $f(n)$。三个独立问题分别是：刻画 $f(n)=n/P(n)$；严格不等式 $f(n)>\sqrt n$ 是否有无穷多合数解；以及对每个固定 $A>0$ 是否一致有 $f(n)\ll_A n/(\log n)^A$。
- 状态核对：三问整体仍开放。必须区分第二问的严格 $>$ 与由素数平方得到的 $\ge$；旧候选在这一点上最终区分正确。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：用恒等式 $\binom nk=(n/k)\binom{n-1}{k-1}$ 和 $p$-进赋值，把第一问化为所有允许 $k$ 的整除条件；第三问先最大化 $n$ 的素数幂分量。
- 局部结论：若 $d=(n,k)$，则 $n/d\mid\binom nk$。因为 $d<n$，有 $n/d\ge p(n)$，故 $f(n)\ge p(n)$。；若 $p^a\mid n$，则 $\gcd(n,\binom n{p^a})=n/p^a$：恒等式先给出其余因子，而 Lucas 定理给出 $\binom{n-1}{p^a-1}\not\equiv0\pmod p$。因此 $f(n)\le n/P(n)$，且 $f(n)=n/P(n)$ 等价于对每个 $2\le k\le n/2$ 都有 $n/P(n)\mid\binom nk$。；令 $R(n)=\max_{p^a\parallel n}p^a$，则 $f(n)\le n/R(n)$。若所有素数幂分量不超过 $y$，则 $n\mid\operatorname{lcm}(1,\ldots,\lfloor y\rfloor)$，故由 $\log\operatorname{lcm}(1,\ldots,y)\sim y$ 得 $R(n)\ge(1-o(1))\log n$，恢复 $f(n)\le(1+o(1))n/\log n$。
- 第一阻塞点：最大素数幂路线在近似 primorial 的数上只能给出 $R(n)\asymp\log n$，无法产生任意次对数节省。第一问的等价整除判据仍需同时控制所有素数的 Kummer 进位；第二问中素数平方只给等号，尚无可证明的无限严格超越族。
- 下一步：先研究 $n=2pq$（$p<q<2p$）并用 Lucas/Kummer 判据精确判定何时所有 $2\le k\le n/2$ 都满足 $2p\mid\binom nk$；这会把严格 $f(n)>\sqrt n$ 化为一个明确的素数对与基数位条件。
- 来源核对：官方状态、基本上下界及已知例子：https://www.erdosproblems.com/700；官方页确认第二问要求严格 $>$，而 $p^2$ 仅证明 $\ge$。
- 时间记账：所在批次墙钟时间按题数均摊约 54.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/700)；既有候选答案（按不可信材料审计）

### #701

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\mathcal{F}$ be a family of sets closed under taking subsets (i.e. if $B\subseteq A\in\mathcal{F}$ then $B\in \mathcal{F}$). There exists some element $x$ such that whenever $\mathcal{F}'\subseteq \mathcal{F}$ is an intersecting subfamily we have\[\lvert \mathcal{F}'\rvert \leq \lvert \{ A\in \mathcal{F} : x\in A\}\rvert.\]
- 题意摘要：标准有限版本是：对有限地面集上的有限下闭族 $\mathcal F$，存在一个元素 $x$，使每个两两相交子族 $\mathcal F'\subseteq\mathcal F$ 都满足 $|\mathcal F'|\le|\mathcal F_x|$。但输入字面及本地 Lean 文件量化任意类型和任意集合族，没有有限性。
- 状态核对：有限版本仍是 Chvátal 猜想，开放；无限字面版本则为假。因此旧候选的无限反例不能宣称解决官方有限问题，但确实暴露了当前形式化/陈述缺失有限性。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：对有限版本取一个极大相交子族，并从其中最小集合 $S$ 出发覆盖；同时独立检查无限反例：取共尾数为 $\omega$、大于连续统的基数 $\kappa$，构造 $\kappa$ 个两两相交的可数集合，而每个元素只落在少于 $\kappa$ 个生成集合中，再取下闭包。
- 局部结论：若有限相交族含单点集 $\{x\}$，则所有成员都含 $x$，结论立即成立。；若下闭族秩至多 2，则相交的二元集族只能是星或三角形；星情形显然，三角形的任一顶点之星还包含该单点集，大小至少 3。因此秩至多 2 的版本成立。；无限反例中可令 $A_\mu=(\{\mu\}\times\omega)\cup\{2^c3^d:c\le n_\mu\le d\}$。若 $\mu\le\nu$，则 $2^{n_\mu}3^{n_\nu}\in A_\mu\cap A_\nu$，所以 $\{A_\mu:\mu<\kappa\}$ 是大小 $\kappa$ 的相交族；其下闭包中每颗星至多是少于 $\kappa$ 个可数幂集之并，故大小严格小于 $\kappa$。
- 第一阻塞点：有限路线中，若最小成员 $S$ 的大小大于 1，只能由 $\mathcal F'\subseteq\bigcup_{x\in S}\mathcal F_x$ 推出某颗星至少为 $|\mathcal F'|/|S|$；目前没有严格方法消去因子 $|S|$。无限版本则已经由上述基数构造否定。
- 下一步：首先修正正式陈述为 `[Fintype X]` 且有限族；随后尝试把秩 2 论证推广到秩 3，按最小成员大小分类并验证每个压缩步骤是否保持原族最大星的上界。
- 来源核对：官方有限意图及已知特例：https://www.erdosproblems.com/701；官方讨论明确指出无限形式化存在反例：https://www.erdosproblems.com/forum/thread/701；已检查本地 701.lean：其定理量化任意 `Type*`、使用基数比较，确实没有有限性假设。
- 时间记账：所在批次墙钟时间按题数均摊约 54.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/701)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/701.lean`；既有候选答案（按不可信材料审计）

### #704

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G_n$ be the unit distance graph in $\mathbb{R}^n$, with two vertices joined by an edge if and only if the distance between them is $1$. Estimate the chromatic number $\chi(G_n)$. Does it grow exponentially in $n$? Does\[\lim_{n\to \infty}\chi(G_n)^{1/n}\]exist?
- 题意摘要：$G_n$ 的顶点是全部 $\mathbb R^n$，恰距 1 的点对相邻；$\chi(G_n)$ 是避免同色单位距离所需的最少颜色。问题包含渐近估计、是否至少指数增长，以及根序列 $\chi(G_n)^{1/n}$ 是否收敛。
- 状态核对：“是否指数增长”已由 Frankl–Wilson 肯定；整个问题仍开放是因为精确指数率及极限存在性未知。目前官方记录为 $(1.239\ldots+o(1))^n\le\chi(G_n)\le(3+o(1))^n$。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `0/10`；置信度 `high`
- 尝试路线：下界采用定重 0–1 向量构成的有限距离图：把 $r$-子集映为其关联向量并缩放，使指定交数恰对应距离 1，再用交集定理控制独立集。对极限则尝试建立维数方向的次乘性。
- 局部结论：对 $r$-子集 $A,B\subset[m]$，关联向量满足 $\|1_A-1_B\|^2=2(r-|A\cap B|)$；适当统一缩放后，禁止某一交数正好成为单位距离条件。；有限图总有 $\chi\ge |V|/\alpha$；Frankl–Wilson型交集上界使 $|V|/\alpha$ 指数大，现有优化给出下基数约 $1.239$。Larman–Rogers 给出上基数 3，故 $1.239\ldots\le\liminf\chi(G_n)^{1/n}\le\limsup\chi(G_n)^{1/n}\le3$。；坐标嵌入 $\mathbb R^n\hookrightarrow\mathbb R^{n+m}$ 给出 $\chi(G_{n+m})\ge\chi(G_n)$，但单调性本身不足以保证根极限存在。
- 第一阻塞点：自然的乘积着色不能给出 $\chi(G_{n+m})\le\chi(G_n)\chi(G_m)$：单位距离可由两个坐标块中的非单位距离平方和组成。事实上 $\chi(G_1)=2$ 而 $\chi(G_2)\ge5>4$，精确次乘性已在 $1+1$ 维失败；尚无次指数损失的替代不等式可应用 Fekete 引理。
- 下一步：构造并检验带距离容差的颜色数 $\chi_n(\varepsilon)$，尝试证明 $\chi_{n+m}(\varepsilon)\le\chi_n(\varepsilon')\chi_m(\varepsilon')e^{o(n+m)}$，再研究 $\varepsilon\downarrow0$ 时能否无指数损失地回到精确单位距离。
- 来源核对：官方最新上下界与开放状态：https://www.erdosproblems.com/704；Larman–Rogers 上界的现代重证：https://arxiv.org/abs/1610.02846
- 时间记账：所在批次墙钟时间按题数均摊约 54.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/704)；既有候选答案（按不可信材料审计）

### #705

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a finite unit distance graph in $\mathbb{R}^2$ (i.e. the vertices are a finite collection of points in $\mathbb{R}^2$ and there is an edge between two points if and only if the distance between them is $1$). Is there some $k$ such that if $G$ has girth $\geq k$ (i.e. $G$ contains no cycles of length $<k$) then $\chi(G)\leq 3$?
- 题意摘要：量词为：是否存在整数 K，使每个有限点集 P⊂R² 所诱导的 faithful 单位距离图 G(P)（xy∈E 当且仅当 ||x−y||=1），只要 girth(G)≥K，就有 χ(G)≤3？否定它须对每个 K 构造这样的有限 P，满足 girth≥K 且 χ≥4。
- 状态核对：已知否定解。吸收人工评审意见：旧候选没有核实 O'Donnell 的嵌入是否 faithful；仅有“指定边均为单位长”的非忠实嵌入确实不够，因为额外单位边可能产生短圈。2026-01-27 的状态更新是在重新检查 O'Donnell 论文/学位论文后作出的。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 O'Donnell 路线：先构造对任意 g≥3 都具有 girth g、染色数4的抽象有限图，再通过其附件与连续变形嵌入方法实现为平面单位距离图。对给定候选阈值 K，取 g≥K；所得图直接反驳该阈值。
- 局部结论：若 O'Donnell 的定理给出的是 faithful 实现，则取 g≥K 立即得到 girth≥K 且 χ=4，故不存在题设 K。；仅把抽象图的边画成单位线段不能完成反例：取同一点集后的完整单位距离图会加入额外边；χ不会下降，但 girth可能下降。；O'Donnell 学位论文定理28表述为：每个 k≥3 都存在 girth k、4-色的单位距离图；两篇论文分别处理抽象图描述与平面嵌入。
- 第一阻塞点：本次受限重建没有逐坐标复核嵌入部分中“所有非边距离均不等于1”的通用位置论证；这是回应旧人工评审时必须核对的第一处技术点，不能由标题或定理摘要代替。
- 下一步：逐页核对 O'Donnell《High girth unit-distance graphs》对 unit-distance graph 的定义，并检查 Part II 中每次附件/扰动是否明确排除非边成为单位距离；最好抽取为一个“有限个禁等式可同时避开”的引理。
- 来源核对：Erdős Problems #705（2026-01-27 更新）明确列为 DISPROVED，并引用 O'Donnell 的任意 girth 构造：https://www.erdosproblems.com/705；讨论页明确记录旧评审的 faithful 质疑及后续核查，并指出学位论文定理28：https://www.erdosproblems.com/forum/thread/705；Geombinatorics 作者索引核对了两篇论文的题名、卷期和页码：https://geombina.uccs.edu/author-index/paul-odonnell
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/705)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/705.lean`；既有候选答案（按不可信材料审计）

### #706

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $L(r)$ be such that if $G$ is a graph formed by taking a finite set of points $P$ in $\mathbb{R}^2$ and some set $A\subset (0,\infty)$ of size $r$, where the vertex set is $P$ and there is an edge between two points if and only if their distance is a member of $A$, then $\chi(G)\leq L(r)$. Estimate $L(r)$. In particular, is it true that $L(r)\leq r^{O(1)}$?
- 题意摘要：对每个整数 r≥1，L(r) 是统一控制量：对任意 r 元距离集 A⊂(0,∞) 和任意有限 P⊂R²，完整距离图 G_A(P)（xy∈E 当且仅当 ||x−y||∈A）均满足 χ(G_A(P))≤L(r)。问题要求估计最坏情形 L(r)，特别问是否存在常数 C 使 L(r)≤r^C。
- 状态核对：仍开放。旧候选的 Ω(r√log r) 结论可由格点严格推出，但把 Naslund 的固定距离数、高维渐近定理直接代入平面并令 r→∞是不合法的；这里改用经典格点距离计数。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：上界采用单距离7着色的直积；下界取 q×q 整格点 P。令 A包含 P出现的全部非零距离，则 G_A(P)=K_{q²}。再用 Landau–Ramanujan 型计数估计可出现的平方距离 u²+v²。
- 局部结论：对 A={d₁,…,d_r}，分别缩放一个避开距离1的7着色以避开 d_i，并以 r 元颜色向量着色，严格得到 L(r)≤7^r。；q×q 格点有 q² 个点，而其不同距离数至多 O(q²/√log q)；把这些距离放入 A 后得到团 K_{q²}。必要时向 A 添加无关距离至恰有 r 个元素，不会降低染色数。；反演上述关系得到 L(r)≥c r√log r（调整 q 可覆盖所有充分大的 r）。因此目前这条路线给出 c r√log r≤L(r)≤7^r。
- 第一阻塞点：直积着色逐个处理距离，颜色数必然相乘；要得到多项式上界，必须找到一个单一平面分割同时避开任意 r 个尺度。当前路线没有控制不同尺度之间的相互作用，这是第一处无法闭合之处。
- 下一步：固定一种周期格/六边形分割，精确写出其“坏缩放参数”集合；检验能否随机选取 O(log r) 个平移或尺度，使每个 d∈A 都被某一坐标分离，并计算最终颜色数是否为 r^{O(1)}。
- 来源核对：Naslund 原论文核对了多禁距参数定义；其摘要中的 (Γχ√(m+1)+o(1))^n 是维数 n 的渐近，不能直接证明平面 r→∞ 的格点下界：https://arxiv.org/abs/2205.12312；当前题页及其无限图表述由 de Bruijn–Erdős 紧致性联系；开放状态未见改变：https://www.erdosproblems.com/706
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/706)；既有候选答案（按不可信材料审计）

### #708

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ be minimal such that for any $A\subseteq [2,\infty)\cap \mathbb{N}$ with $\lvert A\rvert =n$ and any set $I$ of $\max(A)$ consecutive integers there exists some $B\subseteq I$ with $\lvert B\rvert=g(n)$ such that\[\prod_{a\in A} a \mid \prod_{b\in B}b.\]Is it true that\[g(n) \leq (2+o(1))n?\]Or perhaps even $g(n)\leq 2n$?
- 题意摘要：字面量词是：求最小整数 g(n)，使对每个 n元集合 A⊂{2,3,…}、每个由 M=max(A) 个连续整数组成的集合 I，都存在普通子集 B⊂I，且恰有 |B|=g(n)，满足 ∏_{a∈A}a 整除 ∏_{b∈B}b。随后询问 g(n)≤(2+o(1))n 或 g(n)≤2n。
- 状态核对：按输入的“恰等于 g(n)”字面解释，陈述与官方下界不相容，应视为转录/形式歧义。因 A 有 n 个不同且≥2的整数，M≥n+1；取 A={2,…,n+1} 时 |I|=n+1，所以任何 B⊂I 都有 |B|≤n+1，不可能出现约2n的 g(n)。文献显然意指“存在 |B|≤g(n) 的 B”（或等价的最坏最小基数）。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：对修正后的参数写成素数赋值覆盖问题：令 D_p=Σ_{a∈A}v_p(a)。需从 I 中选尽量少的不同整数 B，使对每个素数 p 都有 Σ_{b∈B}v_p(b)≥D_p。尝试为各 a选取区间内的倍数并合并。
- 局部结论：整除条件严格等价于对每个 p≤M 满足 Σ_{b∈B}v_p(b)≥Σ_{a∈A}v_p(a)。；长度 M 的任意整数区间对每个 a≤M 至少含一个 a 的倍数；但为不同 a选到同一个整数时，普通集合不能重复计数，因此这只给出逐项覆盖，不能推出乘积覆盖。；若允许多重集 B，则为每个 a选一个倍数即可用 n 项完成；故原问题中“B是集合、元素必须不同”正是产生约2n下界的关键。
- 第一阻塞点：从“每个 a各有一个倍数”过渡到同时满足全部 p-adic 需求时，碰撞会丢失重数；没有证明能用至多2n个不同整数重新分配这些赋值。这是具体路线的第一处缺口。
- 下一步：先向数据源确认定义应为 |B|≤g(n)。随后把选择问题写成带容量的整数规划，并对 n≤6、所有按整除偏序约化后的 A 与区间起点模 lcm(A) 穷举，查找最小反例结构及碰撞素数。
- 来源核对：Erdős Problems #708 页面仍把问题列为开放，并同时报告 Erdős–Surányi 的 g(n)≥(2−o(1))n；这反证了“恰等于”字面读法能够是预期定义：https://www.erdosproblems.com/708；旧候选发现了等号问题，但其“因此 g(n)不能超过n+1”应理解为对字面陈述的不相容诊断，而不是修正版参数的上界。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/708)；既有候选答案（按不可信材料审计）

### #709

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be minimal such that, for any $A=\{a_1,\ldots,a_n\}\subseteq [2,\infty)\cap\mathbb{N}$ of size $n$, in any interval $I$ of $f(n)\max(A)$ consecutive integers there exist distinct $x_1,\ldots,x_n\in I$ such that $a_i\mid x_i$. Obtain good bounds for $f(n)$, or even an asymptotic formula.
- 题意摘要：求最小实数/整数倍数 f(n)，使对每个 n元集合 A={a₁,…,a_n}⊂{2,3,…}，令 M=max A 后，每个含 f(n)M 个连续整数的区间 I 都含有两两不同的 x₁,…,x_n，分别满足 a_i|x_i。量词中的 A、I 均为任意。
- 状态核对：开放。冻结输入给出 (log n)^c≪f(n)≪√n；2026 年结果把下界提高到 log n/loglog n，且2026-07的新预印本若核验无误可进一步给出 f(n)≫log n。旧候选只报 f(n)≤n，遗漏了输入已给出的经典 √n 上界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：建立二分图：左侧为 A，右侧为 I，a与x相连当且仅当 a|x。用 Hall 定理把问题化为对每个 S⊂A，区间中被至少一个 a∈S整除的整数数目不少于 |S|。先做分块上界，再把“首 n 个模数”的坏区间嵌入一般问题得到下界。
- 局部结论：把长度 nM 的区间分成 n 个长度 M 的块，第 i 块必含 a_i的倍数；不同块给出不同整数，故严格有初等上界 f(n)≤n。；取 A={2,…,n+1}。若一个含超过n个整数的区间可匹配这些 n 个模数，则尚有一个未用整数可分配给模数1；因此任何对 {1,…,n+1} 的坏区间也给出本题坏例。；结合 van Doorn 的坏区间定理，上述归约给出 f(n)≫log n/loglog n。2026-07 Kominers 预印本声称存在长度 c n log n 的坏区间；若其定理通过核验，同一归约立即提升为 f(n)≫log n。
- 第一阻塞点：Hall 条件要求同时控制所有 S⊂A 的算术级数并集。简单下界 Σ_{a∈S}|I|/a 会严重重复计数；当前路线没有对任意 A 的重叠给出足以达到 O(√n)乃至更好上界的统一估计。
- 下一步：按 gcd/lcm 对 S 分层，先证明一个可检验的受限引理：当 S中任意两数的 lcm>2|I| 时，Hall 条件可由单点计数直接验证；再计算剩余“高重叠”模数能否压缩到 O(√n) 个整除链。
- 来源核对：官方 LaTeX 已加入 van Doorn 2026 下界，仍列经典 f(n)≪√n：https://www.erdosproblems.com/latex/709；van Doorn 定理明确给出长度 0.36 n log n/loglog n 的坏区间：https://math.colgate.edu/~integers/aa7/aa7.pdf；Kominers 2026-07 预印本把坏区间长度提高到任意 c<1/e 乘 n log n；这是冻结日期后的新材料，尚不据此改判状态：https://arxiv.org/abs/2607.10431
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/709)；既有候选答案（按不可信材料审计）

### #710

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be minimal such that in $(n,n+f(n))$ there exist distinct integers $a_1,\ldots,a_n$ such that $k\mid a_k$ for all $1\leq k\leq n$. Obtain an asymptotic formula for $f(n)$.
- 题意摘要：对每个 n，f(n) 是最小区间增量 F，使开区间 (n,n+F) 内可选出 n 个两两不同整数 a₁,…,a_n，并对每个 1≤k≤n 满足 k|a_k。要求 n→∞ 时的渐近公式。这里起点固定为 n，不是任意区间。
- 状态核对：仍开放。Erdős–Pomerance 已证明下界 (2/√e+o(1))n√(log n/loglog n) 和上界 (1.7398…+o(1))n√log n。旧候选据此推出 f(n)=n(log n)^{1/2+o(1)}是正确的，但其简述的“k光滑则a_k也光滑”并非一般事实，不应作为下界证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：同样建立 Hall 二分图，左侧 [n]、右侧 (n,n+F)∩Z，边为整除。尝试选择一族具有受控素因子的左顶点 S，使其邻域 N(S) 过小，从而由 Hall 得到下界；上界则需证明每个 S 的邻域足够大。
- 局部结论：存在所需配对当且仅当对每个 S⊂[n]，都有 |{m∈(n,n+F): 存在 k∈S, k|m}|≥|S|。；仅由右侧需容纳 n 个不同整数即可得 F≥n+1（依开区间端点取整微调）；真正的已知下界必须构造更强的 Hall 障碍。；由已知两侧估计可严格推出 f(n)/n→∞，以及 log f(n)=log n+(1/2)loglog n+O(logloglog n)，即 f(n)=n(log n)^{1/2+o(1)}；这仍不是常数级渐近公式。
- 第一阻塞点：选择光滑数集合 S 后，倍数 kq 可能引入大素因子，故不能直接把 N(S) 包含在光滑数中。需要 Erdős–Pomerance 的递归缩放及精细 Ψ(x,y) 估计来控制邻域；这里是旧候选证明梗概的第一处不严谨点。
- 下一步：从原论文逐式重建其下界引理：明确所选 S、允许的乘子范围以及 Ψ(x,y) 的参数区间；数值优化 y 后复算常数2/√e，检查每一步是否真的是 Hall 邻域上界。
- 来源核对：Erdős Problems #710 截至2026仍列为 OPEN，并保留原两侧常数：https://www.erdosproblems.com/710；Erdős–Pomerance 原论文明确以 Hall/König 定理处理上界，并以小 y 区域的光滑数计数处理下界：https://math.dartmouth.edu/~carlp/PDF/matching.pdf；原论文的文献评述核对上界常数为 √r/(1−r)，其中 e^(−r)=r，数值约1.7398：https://www2.math.ethz.ch/EMIS/classics/Erdos/cit/42610048.htm
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/710)；既有候选答案（按不可信材料审计）

### #711

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n,m)$ be minimal such that in $(m,m+f(n,m))$ there exist distinct integers $a_1,\ldots,a_n$ such that $k\mid a_k$ for all $1\leq k\leq n$. Prove that\[\max_m f(n,m) \leq n^{1+o(1)}\]and that\[\max_m (f(n,m)-f(n,n))\to \infty.\]
- 题意摘要：对每个正整数 n、整数起点 m，令 f(n,m) 为区间中可选出两两不同的 a_1,…,a_n 且 k∣a_k 的最短长度。问题包含两个断言：一致地对所有 m 有 f(n,m)≤n^{1+o(1)}；以及 max_m(f(n,m)−f(n,n))→∞。原题开区间与论文采用的 (m,m+L] 相差至多 1，不影响渐近结论。
- 状态核对：第一问仍开放；第二问已由 van Doorn（2026）证明，故整题只能标为部分解决。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `3/10`；置信度 `high`
- 尝试路线：第一问写成 Hall 匹配：左部为 [n]，右部为候选区间整数，k 与其倍数相连；所求等价于对每个 S⊆[n]，区间内被 S 中元素整除的整数并集至少有 |S| 个。第二问重建 van Doorn 的缩放路线：对 k=⌈0.6√(log n/loglog n)⌉，先证明 kn+f(kn,kn)≤k²n+f(n,k²n)，再代入 Erdős–Pomerance 对 f(x,x) 的上下界。
- 局部结论：缩放不等式严格成立：对 n<i≤kn 取 a_i=ki∈(kn,k²n]；对 i≤n 使用 f(n,k²n) 所给的倍数，两个值域不交。；由 f(x,x)>(2/√e+o(1))x√(log x/loglog x) 得 f(kn,kn)>(2.01)k²n；由 f(n,n)<(2+o(1))n√log n 得 0.01k²n>f(n,n)。；因此 max_m f(n,m)−f(n,n)>0.36n log n/loglog n，特别趋于无穷。先前候选把 k 错写成 floor；原论文是 ceiling，只有后者直接保证 k²≥0.36log n/loglog n。
- 第一阻塞点：近线性第一问的首个缺口是：在 L=n^{1+o(1)} 时，无法对所有 S⊆[n] 统一证明 Hall 并集下界；倍数之间的高重合使单纯度数估计只能导向已知的约 n^{3/2} 尺度。
- 下一步：按 S 中元素的最大公因子、大小区间及平滑部分分层，先检验能否对 |S|≤n^{1/2} 或 S⊆[n/2,n] 建立 L=n·exp(O(log n/loglog n)) 的 Hall 下界。
- 来源核对：[van Doorn 原论文](https://math.colgate.edu/~integers/aa7/aa7.pdf)核对了缩放引理、常数 0.36 和 2026 年发表信息。；[arXiv 正文](https://arxiv.org/abs/2601.16972)明确显示 k 使用 ceiling，而非先前候选的 floor。；[Erdős Problems #711](https://www.erdosproblems.com/711)仍将第一问列为开放，并记录第二问的定量解答。
- 时间记账：所在批次墙钟时间按题数均摊约 41.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/711)；既有候选答案（按不可信材料审计）

### #712

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Determine, for any $k>r>2$, the value of\[\frac{\mathrm{ex}_r(n,K_k^r)}{\binom{n}{r}},\]where $\mathrm{ex}_r(n,K_k^r)$ is the largest number of $r$-edges which can placed on $n$ vertices so that there exists no set of $k$ vertices which is covered by all $\binom{k}{r}$ possible $r$-edges.
- 题意摘要：固定整数 k>r>2；在所有 n 点、无 K_k^r 的 r-一致超图中最大化边数 ex_r(n,K_k^r)，意图是确定归一化密度 ex_r(n,K_k^r)/C(n,r) 在 n→∞ 时的极限。原文字面没有写 lim。
- 状态核对：一般情形开放。题面还存在归一化不一致：若分母确为 C(n,2)，Turán 定理给 r=2 极限 1−1/(k−1)，不是官方背景写的 1/2·(1−1/(k−1))；后者对应除以 n²。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先证明极限存在，再尝试多部构造。取 n 点极值超图，随机删去一点；诱导的 (n−1) 点子图平均保留 (n−r)/n 比例的边，由此比较相邻 n 的归一化密度。下界则把顶点均分为 k−1 部，只保留横跨 r 个不同部分的边。
- 局部结论：令 d_n=ex_r(n,K_k^r)/C(n,r)。随机删点给 d_{n−1}≥d_n，因此 d_n 单调下降且有极限 π(K_k^r)。；(k−1)-部横截构造不含 K_k^r：任意 k 点中有两点同部，包含这两点的某个 r-子集不是边。；该构造给 π(K_k^r)≥(k−1)_r/(k−1)^r，其中 (q)_r=q(q−1)…(q−r+1)。
- 第一阻塞点：单调性和显式构造没有提供匹配上界；对 r≥3，局部共度数约束不足以迫使密度超过上述构造的超图包含 K_k^r。另因题面遗漏 lim 且 r=2 归一化常数错误，必须先固定正式版本。
- 下一步：先修订题面为 lim_{n→∞}ex_r/C(n,r)，然后对最小情形 K_4^3，把候选构造的拉格朗日量与已发表的旗代数上界证书逐项核验，而不把数值证书误作精确解。
- 来源核对：[Erdős Problems #712](https://www.erdosproblems.com/712)截至 2026 年仍列为开放。；同一官方页面同时展示了分母 C(n,r) 与 r=2 的半常数，确认题面确有归一化冲突。
- 时间记账：所在批次墙钟时间按题数均摊约 41.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/712)；既有候选答案（按不可信材料审计）

### #713

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for every bipartite graph $G$, there exists some $\alpha\in [1,2)$ and $c>0$ such that\[\mathrm{ex}(n;G)\sim cn^\alpha?\]Must $\alpha$ be rational?
- 题意摘要：量词是：对每个固定有限二部图 G，是否存在依赖于 G 的 α∈[1,2) 和 c>0，使 n→∞ 时 ex(n;G)/(cn^α)→1；若存在，α 是否必为有理数。
- 状态核对：按通常隐含的非平凡版本仍开放；但字面“每个二部图”是假的：G=K_2 时 ex(n;G)=0，不可能有 c>0。因此需排除 K_2（以及无边图）后才是标准开放问题。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试先证明幂指数存在。若 G 的二分部大小为 s,t，则 K_{s,t} 包含 G，故 Kővári–Sós–Turán 给 ex(n,G)=O(n^{2−1/min(s,t)})。另一方面，当 v(G)≥3 时，取若干个 K_{v(G)−1} 的不交并得到线性下界。再考察 log ex(n,G)/log n 是否收敛。
- 局部结论：对含至少三点的固定 G，有 ex(n,G)=Ω(n)：不交并若干个大小 v(G)−1 的完全图不可能容纳 G。；若 G 是二部图且两个部均非空，则 ex(n,G)=O(n^{2−δ})，其中可取 δ=1/min(s,t)>0。；因此所有可能的上、下幂指数均落在 [1,2)；但这只控制 liminf 与 limsup，不证明二者相等，更不产生渐近常数。
- 第一阻塞点：第一处缺口是无法证明 log ex(n,G)/log n 收敛；极值数没有足够强的乘法性或次乘法性。即使指数收敛，仍需更强估计才能证明 ex(n,G)/n^α 收敛到正有限常数。
- 下一步：固定一个尚无常数极限的具体 G（如 C_6），检验 blow-up/随机抽样能否给 ex(mn,G) 的准乘法不等式；明确记录误差是否为 n^{o(1)}，以判断 Fekete 型论证是否可用。
- 来源核对：[Erdős Problems #713](https://www.erdosproblems.com/713)仍列标准非平凡版本为开放，并区分 ∼ 与较弱的 asymp。；检索到的相关文献只给出许多新的有理 Turán 指数，未给出单个任意二部图的普遍指数或常数定理。
- 时间记账：所在批次墙钟时间按题数均摊约 41.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/713)；既有候选答案（按不可信材料审计）

### #714

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that\[\mathrm{ex}(n; K_{r,r}) \gg n^{2-1/r}?\]
- 题意摘要：对每个固定整数 r≥2，问是否存在仅依赖 r 的 c_r>0，使所有充分大 n 都满足 ex(n,K_{r,r})≥c_r n^{2−1/r}；这里 gg 按极值图论惯例表示常数因子下界，不是 omega。
- 状态核对：r=2、3 已知成立；r≥4 仍开放。先前候选讨论“gg 也许表示 omega”的分支与本题惯例无关。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：采用随机图加删边。取 G(n,p)，每出现一个 K_{r,r} 删除一条边；估计剩余边数的期望，并选择 p 使初始边数与 K_{r,r} 数量同阶。
- 局部结论：E[e(G)]≈n²p/2，而 E[#K_{r,r}]≤C_r n^{2r}p^{r²}。；令 p=c n^{-2/(r+1)}，两项指数均为 2−2/(r+1)；取 c=c(r) 足够小，删除后仍有 Ω_r(n^{2−2/(r+1)}) 条边。；目标指数与随机删边指数之差为 (2−1/r)−(2−2/(r+1))=(r−1)/(r(r+1))>0；故该通用随机路线严格达不到猜想。
- 第一阻塞点：平衡一阶边数与副本数时，随机模型必然停在指数 2−2/(r+1)。要达到 2−1/r，必须构造强相关的邻域，使大量潜在 K_{r,r} 系统性消失；独立边模型无法提供这种结构。
- 下一步：针对 r=4，检验有限域点—超曲面关联构造：精确计算共同邻域，目标是证明任意四个左顶点至多有三个共同邻点，同时保留 Ω(n^{7/4}) 条边。
- 来源核对：[Erdős Problems #714](https://www.erdosproblems.com/714)记录 KST 上界、r=2,3 的正结果及一般开放状态。；[经典随机删边路线说明](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/TuranKrr.html)给出同一指数 2−2/(r+1)。
- 时间记账：所在批次墙钟时间按题数均摊约 41.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/714)；既有候选答案（按不可信材料审计）

### #719

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\mathrm{ex}_r(n;K_{r+1}^r)$ be the maximum number of $r$-edges that can be placed on $n$ vertices without forming a $K_{r+1}^r$ (the $r$-uniform complete graph on $r+1$ vertices). Is every $r$-hypergraph $G$ on $n$ vertices the union of at most $\mathrm{ex}_{r}(n;K_{r+1}^r)$ many copies of $K_r^r$ and $K_{r+1}^r$, no two of which share a $K_r^r$?
- 题意摘要：固定 r、n。要求对每个 n 点 r-一致超图 G，把 E(G) 分割为若干单边 K_r^r 与完整的 K_{r+1}^r；任意两块不共享 r-边；块数至多 ex_r(n,K_{r+1}^r)。
- 状态核对：一般 Erdős–Sauer 猜想仍开放；r=2 化为每个图可用至多 floor(n²/4) 个边或三角形分解，这是 Erdős–Goodman–Pósa 定理。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把问题归约为边不交 K_{r+1}^r 的打包。设 e=e(G)，ν 为 G 中最大边不交 K_{r+1}^r 数；使用 ν 个大块后其余边作单块，总块数为 e−rν。因此猜想等价于 rν≥e−ex_r(n,K_{r+1}^r)。再考察贪心最大打包。
- 局部结论：若 e≤ex_r(n,K_{r+1}^r)，全部用单边即可，结论成立。；任取最大打包并删除其大块，余图不含 K_{r+1}^r，故余边数 q≤ex；相应块数为 (e+rq)/(r+1)。；由 e≤C(n,r)、q≤ex 只能推出块数≤(C(n,r)+r·ex)/(r+1)，比所需 ex 多至多 (C(n,r)−ex)/(r+1)；所以“贪心后余图极值”本身不够。
- 第一阻塞点：首个缺口正是把超额边 e−ex 转换成至少 (e−ex)/r 个边不交 K_{r+1}^r。普通超饱和性只给很多可能高度重叠的团，不能保证所需打包数。
- 下一步：对 r=3、较小 n 建立整数规划，枚举代表性超图并比较 ν_{K_4^3}(G) 与 (e−ex_3(n,K_4^3))/3；同时求分数打包最优值，以定位缺口来自超饱和性还是整数性。
- 来源核对：[Erdős Problems #719](https://www.erdosproblems.com/719)仍将一般命题列为开放的 Erdős–Sauer 猜想。；[边—三角形分解资料](https://lidicky.name/pub/tile23_short.pdf)明确引述 r=2 时至多 floor(n²/4) 个 K_2、K_3 的 Erdős–Goodman–Pósa 定理。
- 时间记账：所在批次墙钟时间按题数均摊约 41.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/719)；既有候选答案（按不可信材料审计）

### #724

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the maximum number of mutually orthogonal Latin squares of order $n$. Is it true that\[f(n) \gg n^{1/2}?\]
- 题意摘要：令 $f(n)$ 为阶为 $n$ 的两两正交拉丁方的最大个数。问题是：是否存在绝对常数 $c>0,N$，使每个整数 $n\ge N$ 都满足 $f(n)\ge c\sqrt n$？这要求对所有充分大的阶数一致成立，而非只沿素数幂子列。
- 状态核对：截至冻结日期仍为开放问题。旧候选正确指出素数幂情形，但没有给出一般证明。已知一般下界仍是 Beth 的 $f(n)\gg n^{1/14.8}$。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用拉丁方的直积构造：若分别有阶 $u,v$ 的 $r$ 个 MOLS，则逐坐标组合得到阶 $uv$ 的 $r$ 个 MOLS，故 $f(uv)\ge\min(f(u),f(v))$。再代入有限域构造 $f(q)=q-1$（$q$ 为素数幂）。
- 局部结论：若 $n=uv$，其中 $u,v$ 均为素数幂，则 $f(n)\ge\min(u-1,v-1)$。；若进一步 $1/K\le u/v\le K$，则 $f(n)\ge K^{-1/2}\sqrt n-1$；所以目标结论在两个大小可比的素数幂之积上成立。；特别地，对所有素数幂 $q$，有线性下界 $f(q)=q-1$。
- 第一阻塞点：直积下界由最小因子控制。对含固定小素数幂因子的阶数，例如 $n=2m$，该路线只给常数级下界；没有严格方法把大因子的 MOLS 数量提升到整个乘积而不受小因子瓶颈限制。
- 下一步：检验 Wilson/PBD 闭包定理能否给出如下可量化引理：对每个充分大 $n$，构造块大小均为 $\gg\sqrt n$、且各块阶数拥有 $\gg\sqrt n$ 个 MOLS 的可解 PBD；若不能，应明确是哪一条整除或覆盖条件失败。
- 来源核对：[Erdős Problems #724](https://www.erdosproblems.com/724) 仍列为 open，并记录 $1/91,1/17,1/14.8$ 三个一般指数。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/724)；既有候选答案（按不可信材料审计）

### #725

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Give an asymptotic formula for the number of $k\times n$ Latin rectangles.
- 题意摘要：令 $L_{k,n}$ 为符号集 $[n]$ 上的 $k\times n$ 拉丁矩形数：每行是 $[n]$ 的排列，每列无重复，且 $1\le k\le n$。问题要求在相应的联合极限中给出渐近公式；现有结果尚未覆盖接近 $k=n$ 的稠密范围。
- 状态核对：整体问题仍开放。旧候选所写 Godsil–McKay 公式及范围 $k=o(n^{6/7})$ 基本正确，但引用的是后来的计算论文而非原始证明，而且该公式并未覆盖所有 $k$，不能算解决本题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：逐行添加。已有 $r$ 行时，下一行对应一个 $(n-r)$-正则二分图的完美匹配，其数目是邻接矩阵的 permanent。对每一步分别应用 van der Waerden 下界和 Bregman 上界。
- 局部结论：严格地，对所有 $1\le k\le n$，有 $L_{k,n}\ge n!\prod_{r=1}^{k-1} n!\bigl((n-r)/n\bigr)^n$。；同理有 $L_{k,n}\le n!\prod_{r=1}^{k-1}((n-r)!)^{n/(n-r)}$。这些界不依赖前 $r$ 行的具体形状。；$k=2$ 时可精确化为 $L_{2,n}=n!D_n\sim (n!)^2/e$，与 $e^{-\binom22}(n!)^2$ 一致。
- 第一阻塞点：上述 permanent 上下界在稠密范围的对数误差累积后不再是 $o(1)$，不能把夹逼提升为相对误差 $1+o(1)$。尤其当 $k$ 接近 $n$ 时，扩展数强烈依赖已有矩形的结构。
- 下一步：计算两条乘积界的对数差在 $k=n^\alpha$ 时的首项，精确确定简单 permanent 夹逼失效的阈值；随后测试是否可按典型扩展数而非最坏情形缩小该差。
- 来源核对：[Godsil–McKay 原论文](https://users.cecs.anu.edu.au/~bdm/papers/LatinRectangles.pdf)证明其公式适用于 $k=o(n^{6/7})$。；[Erdős Problems #725](https://www.erdosproblems.com/725) 仍将未限定范围的计数问题列为 open。；[后续论文对公式的明确转述](https://link.springer.com/article/10.1007/s00373-015-1643-1)与旧候选中的表达式一致。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/725)；既有候选答案（按不可信材料审计）

### #726

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：As $n\to \infty$ ranges over integers\[\sum_{p\leq n}1_{n\in (p/2,p)\pmod{p}}\frac{1}{p}\sim \frac{\log\log n}{2}.\]
- 题意摘要：定义 $S(n)=\sum_{p\le n}p^{-1}\mathbf1_{\{n\bmod p\in(p/2,p)\}}$。命题是沿每个整数 $n\to\infty$ 都有 $S(n)/(\tfrac12\log\log n)\to1$，不是密度一或概率意义的断言。
- 状态核对：仍开放。人工评审指出的量词错误必须吸收：旧候选只声称“几乎所有 $n$”。而且其证明还有更直接的致命问题：对任一固定普通整数 $n$，当 $y>2n$ 时 $S_y(n)=S(n)$ 已稳定，不可能随 $y$ 像 $\frac12\log\log y$ 增长；CRT 上的 Haar-随机整数不能通过所写 Borel–Cantelli 步骤转化为普通整数的逐点结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：不用概率化，按 $j=\lfloor n/p\rfloor$ 作确定性分块。条件 $n-jp>p/2$ 精确等价于 $n/(j+1)<p<2n/(2j+1)$，从而把 $S(n)$ 写成一族随 $n,j$ 变化的短素数区间上的倒数和。
- 局部结论：有精确恒等式 $S(n)=\sum_{j\ge1}\sum_{n/(j+1)<p<2n/(2j+1)}1/p$，端点若为素数须按原严格不等式处理。；由 Mertens 定理，$p>\sqrt n$ 的总可能贡献至多 $\sum_{\sqrt n<p\le n}1/p=\log2+o(1)$，相对 $\log\log n$ 可忽略。；对任意固定 $A>0$，$p\le(\log n)^A$ 的贡献至多 $\log\log\bigl((\log n)^A\bigr)+O(1)=o(\log\log n)$；因此主项必须来自 $(\log n)^A<p\le\sqrt n$。
- 第一阻塞点：在主贡献范围内 $j=n/p$ 很大，而区间长度约为 $n/(2j^2)$；接近 $p\asymp\sqrt n$ 时长度仅为常数量级。普通 PNT/Mertens 不能对所有这些移动短区间给出足够统一的逐点误差，这正是该确定性路线首先无法闭合之处。
- 下一步：选择可变截断 $y=n^{1/2}/(\log n)^B$，用目前可得的短区间素数定理严格估计 $p\ge y$ 部分；明确剩余区间的总权重及所需最弱的统一短区间误差，形成一个可核验的条件归约。
- 来源核对：题目所给 EGRS75 上下文明确将其作为逐点猜想，而非 almost-all 命题。；人工评审的量词批评已纳入；独立检查还发现旧候选的 CRT/Borel–Cantelli 转移本身无效。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/726)；既有候选答案（按不可信材料审计）

### #727

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$. Does\[(n+k)!^2 \mid (2n)!\]for infinitely many $n$?
- 题意摘要：量词是：对每个固定整数 $k\ge2$，集合 $\{n\in\mathbb N:(n+k)!^2\mid(2n)!\}$ 是否无限？甚至固定 $k=2$ 也未知。
- 状态核对：仍开放。旧候选没有宣称解决，这一点正确；但其中若干计算样例是错误的，不能采信。用 Legendre 估值复核得：所列 $k=2$ 的 $n=1650,1790$、$k=3$ 的 $n=11548$、$k=4$ 的 $n=103359$ 均不是解。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：将问题化为中心二项式系数的逐素数条件，再用 Legendre/Kummer 分析大素因子。精确地，令 $P_k(n)=\prod_{i=1}^k(n+i)$，则整除等价于 $P_k(n)^2\mid\binom{2n}{n}$。
- 局部结论：对每个素数 $p$，条件等价于 $v_p\binom{2n}{n}\ge2\sum_{i=1}^k v_p(n+i)$；左边也等于把 $n+n$ 作 base-$p$ 加法时的进位数。；若 $p^2>2n$，则 $v_p\binom{2n}{n}\le1$；故任何解都要求每个 $n+i$ 的所有素因子满足 $p\le\sqrt{2n}$，即整个长度 $k$ 的块均为 $\sqrt{2n}$-smooth。；若 $\sqrt n<p\le\sqrt{2n}$、$p>2k$ 且 $p\mid n+i$，则 $n\bmod p=p-i>p/2$，$p$ 项和 $p^2$ 项各产生一次进位，因而 $v_p\binom{2n}{n}=2$；这恰可吸收 $p$ 在 $P_k(n)$ 中的一次出现。
- 第一阻塞点：同时制造无限多个长度 $k$ 的连续 $\sqrt{2n}$-smooth 数，并保证所有小素数的总进位数至少是所需估值的两倍，目前没有可用定理。平滑性本身也远非充分条件。
- 下一步：对固定 $k=2$ 做可复现实验：仅用 Legendre 公式枚举到预定界 $X$，对每个失败候选记录最小亏损素数及其属于 $p$, $p^2$ 或更高位的哪次进位；据此检验主要障碍究竟来自大素因子还是小素数估值亏损。
- 来源核对：[本地 Lean 陈述](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/727.lean)正确表达了 $\forall k\ge2$ 后各自无限多个 $n$ 的量词，但证明体仍为 `sorry`。；旧候选的前若干数值已用逐素数 Legendre 公式独立复核，发现上述四个反例。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/727)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/727.lean`；既有候选答案（按不可信材料审计）

### #729

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：For every constant $C>0$, are there infinitely many $a,b,n$ with $a+b>n+C\log n$ such that the denominator of $n!/(a!b!)$ contains only primes bounded in terms of $C$?
- 题意摘要：对每个实常数 $C>0$，要求存在只依赖于 $C$ 的素数界 $A(C)$，以及无限多组正整数 $a,b,n$，满足 $a+b>n+C\log n$，并且约分后 $n!/(a!b!)$ 的所有分母素因子均不超过 $A(C)$。
- 状态核对：该题已获肯定解并经 Lean 验证；应重建已知路线，不再当作开放猜想尝试。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：采用已证构造：对任意充分大的尺度 $M$，选择 $m\in[M,2M]$，令 $n=2m$、$b=m$、$a=m+k$，其中 $k=\lfloor c\log M\rfloor$ 且 $c>C$ 略作放大。核心选择引理保证对所有素数 $p$，$v_p\binom{2m}{m}-v_p\binom{m+k}{k}\ge0$，并在 $p\le2k$ 时给出 $\gg\log M/\log p$ 的余量。
- 局部结论：此构造满足 $a+b-n=k$；因 $\log n=\log M+O(1)$，选定 $c>C$ 后对所有充分大 $M$ 有 $a+b>n+C\log n$。；恒等式 $\frac{(2m)!}{(m+k)!m!}=\frac{\binom{2m}{m}}{k!\binom{m+k}{k}}$ 表明还需用核心引理的估值余量吸收 $v_p(k!)$。；当 $p>2k$ 时 $v_p(k!)=0$；当 $A(C)<p\le2k$ 时，$v_p(k!)\le k/(p-1)$，取 $A(C)$ 足够大即可使其不超过 $\gg\log M/\log p$ 的余量。因此所有负估值只能发生在 $p\le A(C)$。每个充分大尺度都有一组，故得到无限多组。
- 第一阻塞点：结论已经闭合。若要求从零重证，本次筛查未展开的唯一深处是“每个大尺度可选到合适 $m$”的中等素数选择引理；官方记录表明该引理及整条推导已经 Lean 验证。
- 下一步：进行证明审计时，应从 Lean 文件逐项提取核心选择引理的精确常数和量词，并核对从 $c$ 到最终 $A(C)$ 的依赖没有使用隐藏的 $M$ 依赖。
- 来源核对：[Erdős Problems #729](https://www.erdosproblems.com/729)明确记录肯定解及 Lean 验证。；[官方讨论线程](https://www.erdosproblems.com/forum/thread/729)给出构造 $n=2m,a=m+k,b=m$、核心估值差及用 $v_p(k!)$ 确定小素数阈值的机制。
- 时间记账：所在批次墙钟时间按题数均摊约 53.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/729)

### #730

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many pairs of integers $n\neq m$ such that $\binom{2n}{n}$ and $\binom{2m}{m}$ have the same set of prime divisors?
- 题意摘要：问集合 S={(n,m)∈N²:n<m 且 rad(C(2n,n))=rad(C(2m,m))} 是否无限；这里只比较素因子集合，不比较指数，也不要求 m=n+1。Lean 文件中的量词与此一致。
- 状态核对：截至核查日仍列为 open；(87,88)、(607,608) 及三元组 (10003,10004,10005) 只是有限见证，不能推出无限性。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：用 Kummer/Legendre 把素因子相等转化为所有素数下的进位模式相同，再先考察位于 n、m、2n、2m 附近的素数以制造必要的素数空区间。
- 局部结论：对素数 p，p|C(2n,n) 当且仅当 n+n 的 p 进制加法至少有一次进位；特别地，每个 n<p≤2n 的素数都整除 C(2n,n)。；若 n<m 是所求对，则 (2n,2m] 中不能有素数：该区间内的素数整除 C(2m,m)，却大于 2n，因而不整除 C(2n,n)。结合 Bertrand 定理可推出 m<2n。；由 m<2n，若素数 p∈(max(n,2m/3),m]，则 v_p(C(2n,n))=1 而 v_p(C(2m,m))=0。因此这一较短区间也必须无素数。
- 第一阻塞点：这些必要素数空区间能筛掉大量候选对，却没有给出可迭代构造；现有素数间隙理论也不能保证存在无限多对，同时满足全部素数的进位模式一致。
- 下一步：对固定差 d=m-n，严格枚举由 Legendre 公式产生的所有临界区间，并检验能否证明 d 相对 n 的必要上界；随后用筛法估计同时避开这些区间的候选 n 数量。
- 来源核对：[Erdős Problems #730](https://www.erdosproblems.com/730) 当前仍标记 OPEN。；核对了本地 730.lean：正式集合要求 n<m、两个 centralBinom.primeFactors 相等，并已形式化验证给定有限例子。；[Erdős–Graham–Ruzsa–Straus 1975 原文](https://electronicsandbooks.com/edt/manual/Magazine/M/Mathematics%20of%20Computation/1960-2002/pdf/1975_v029_n129/2005464.pdf) 支持以小素数估值和进位性质为核心的背景路线。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/730)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/730.lean`；既有候选答案（按不可信材料审计）

### #731

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find some reasonable function $f(n)$ such that, for almost all integers $n$, the least integer $m$ such that $m\nmid \binom{2n}{n}$ satisfies\[m\sim f(n).\]
- 题意摘要：令 M(n)=min{m≥2:m∤C(2n,n)}。要求找确定函数 f，使自然密度为 1 的整数 n 满足 M(n)/f(n)→1；已知的 exp((log n)^(1/2+o(1))) 只确定对数尺度，远弱于渐近等价。
- 状态核对：仍为 open。先前候选给出的带常数和四次方因子的 f 只是独立性模型所得，不能视为答案；人工评审指出的事件独立性错误必须吸收。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先精确约化到素数幂，再用 Kummer 的进位自动机计数低估值事件；只尝试建立无需独立性假设的单素数尾界。
- 局部结论：严格地，M(n)=min_p p^(v_p(C(2n,n))+1)：任一不整除者必含一个指数超过相应 p-adic 估值的素数幂，而该素数幂不大于原数。；对奇素数 p 和 n<p^k，p∤C(2n,n) 的 n 恰有 ((p+1)/2)^k 个；这是所有 p 进制数字均≤(p-1)/2 的精确计数。；更一般地，对固定 p、a，低于 a 次进位的 k 位串数至多为 O_{p,a}(k^a((p+1)/2)^k)（p=2 有相应多项式界）。故每个固定素数幂最终几乎总整除，进而 M(n) 在密度意义下趋于无穷。
- 第一阻塞点：要定位最小失败素数幂，必须控制随 x 增长的许多 p-adic 事件的联合分布。它们并不独立，而且还要计入 v_p(C)<a、a>1 的竞争者；因此方程 Σq_p≈1 及候选 f(n) 均未被严格推出。
- 下一步：建立对所有 p^a≤exp(C√log x) 一致的进位自动机上界，并先用并集界严格恢复 M(n) 的一侧 exp(c√log n) 正常阶；这一步完全不需要假设不同素数事件独立。
- 来源核对：[Erdős Problems #731](https://www.erdosproblems.com/731) 仍标记 OPEN，只记录 M(n)=exp((log n)^(1/2+o(1)))。；[1975 原论文](https://electronicsandbooks.com/edt/manual/Magazine/M/Mathematics%20of%20Computation/1960-2002/pdf/1975_v029_n129/2005464.pdf) 研究小素数的高次整除，但未给出候选答案声称的精确正常阶。；明确拒绝先前候选的独立性近似：它至多是启发式，也遗漏了较小素数幂可能先失败的问题。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/731)；既有候选答案（按不可信材料审计）

### #734

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Find, for all large $n$, a non-trivial pairwise balanced block design $A_1,\ldots,A_m\subseteq \{1,\ldots,n\}$ such that, for all $t$, there are $O(n^{1/2})$ many $i$ such that $\lvert A_i\rvert=t$.
- 题意摘要：对每个充分大的 n，须构造一个非平凡 PBD：每对点恰落在一个块中，并存在绝对常数 C，使每个整数 t 对应的 t-块数量都≤C√n。
- 状态核对：当前仍为 open。先前候选错误地对随 n 改变的图族 G_n 使用 Lamken–Wilson 的“固定 G、n≥n₀(G)”定理；未知阈值 n₀(G_n) 不能统一控制。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：改用显式有限几何：从阶 q 的射影平面 PG(2,q) 取 n 点 X，并以各直线与 X 的交集（大小至少 2）为块，把问题归约为直线交数的均匀分布。
- 局部结论：任意 X⊆PG(2,q) 自动给出 PBD：X 中每对点位于唯一射影直线上；大小 0 或 1 的交集可删除。；用 Bertrand 定理可选素数 q=Θ(√n) 且 q²+q+1≥n，所以该路线可覆盖每个充分大的 n，而非仅覆盖某个稀疏参数序列。；该构造满足目标当且仅当对每个 s，具有 |L∩X|=s 的直线数为 O(q)。容量上并无矛盾：共有 Θ(q²) 条线和 O(q) 个可能交数。
- 第一阻塞点：第一处缺口是构造这样的 n 点集 X。均匀随机 X 的交数近似二项分布，集中在 O(√q) 个值上，峰值约 q²/√q=q^(3/2)，只给 O(n^(3/4))，达不到 O(√n)。
- 下一步：对小素数幂 q 做整数规划/有限域搜索，寻找直线交数直方图最大值 O(q) 的点集；若出现代数模式，再尝试用轨道并、差集或有限域曲线证明该模式对无限 q 成立。
- 来源核对：[Erdős Problems #734](https://www.erdosproblems.com/734) 当前仍标记 OPEN。；[问题页](https://www.erdosproblems.com/734) 确认 PBD 的量词是每对点恰被一个块覆盖。；已明确吸收人工评审意见：固定分解族的存在阈值不能在 G=G_n 时直接推出统一的“所有充分大 n”。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/734)；既有候选答案（按不可信材料审计）

### #738

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G$ has infinite chromatic number and is triangle-free (contains no $K_3$) then must $G$ contain every tree as an induced subgraph?
- 题意摘要：标准含义是：对每棵有限树 T，每个三角形自由且 χ(G) 为无限基数的图 G，是否含有 T 的诱导拷贝。等价的有限表述是：是否存在有限 f(T)，使每个三角形自由且 χ(G)≥f(T) 的图含诱导 T。
- 状态核对：一般情形仍 open，即 Gyárfás–Sumner 猜想的 K₃-free 特例；不能把“tree”扩张为任意基数的无限树。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：尝试按树的叶子数归纳：先嵌入 T−x，再寻找一个只邻接叶子父节点、且不邻接其余已嵌入顶点的新顶点。
- 局部结论：无限版与有限阈值版严格等价：若不存在 f(T)，取一列三角形自由、诱导 T-free 且色数趋于无穷的有限图的不交并，即得色数 ℵ₀ 的反例。反向蕴含直接成立。；所有星 K_{1,k} 都成立：若三角形自由图的最大度小于 k，则可用 k 色贪心着色；故无限色数迫使某顶点度至少 k，而其邻域因无三角形而独立。；已知文献证明半径 2 的树这一整类，与上述星形基例相容，但并未覆盖任意树。
- 第一阻塞点：给定一个诱导 T−x 后，高色数本身不能保证存在只连接指定父节点的顶点；候选顶点可能全部同时邻接已嵌入树的其他顶点。把这些“错误邻接型”全部染色所需的统一界，正是归纳无法闭合之处。
- 下一步：固定最小未覆盖树（可先取半径 3 的细分星），按新顶点对已嵌入 T−x 的邻接型分层；检验三角形自由条件是否使每个错误类型具有有界色数，从而留下正确类型。
- 来源核对：[Erdős Problems #738](https://www.erdosproblems.com/738) 当前仍标记 OPEN。；[Gyárfás–Szemerédi–Tuza 原论文](https://www.renyi.hu/~gyarfas/Cikkek/14_GyarfasSzemerediTuza_InducedSubtreesInGraphsOfLargeChromaticNumber.pdf) 的摘要与正文确认有限阈值表述及半径 2 特例。；未采用先前候选关于任意无限树的字面反例作为问题答案，因为官方语境指有限树的 χ-bounded 猜想。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/738)；既有候选答案（按不可信材料审计）

### #740

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\mathfrak{m}$ be an infinite cardinal and $G$ be a graph with chromatic number $\mathfrak{m}$. Let $r\geq 1$. Must $G$ contain a subgraph of chromatic number $\mathfrak{m}$ which does not contain any odd cycle of length $\leq r$?
- 题意摘要：对每个无限基数 m、每个 χ(G)=m 的简单图 G 及整数 r≥1，问是否存在一个边/点子图 H⊆G，使 χ(H)=m 且 H 不含长度≤r 的奇圈。这里不是诱导子图要求。
- 状态核对：官方截至核查日仍列 open，而非 independent。先前候选声称 Komjáth–Shelah 给出 aleph₁ 的一致性反例，未找到支持该推论的原始来源，且与官方状态冲突，不能采纳。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：从按长度逐类删除短奇圈入手，检查删除一组击中所有短奇圈的边后能否保持原色数基数；同时分离平凡 r 和 Rödl 已知子情形。
- 局部结论：r≤2 时条件为空，取 H=G；r=3 时条件恰为无三角形。；m=aleph₀、r=3 的肯定答案由 Rödl 定理给出；这不能自动推广到不可数 m，也不能自动排除 C₅、C₇ 等。；若命题对某 r 成立，则对所有较小 r 成立；反之，r=3 的反例会同时否定所有 r≥3。但目前没有经核验的 ZFC 或一致性反例可用于这一步。
- 第一阻塞点：逐圈选边删除虽然能消灭所有短奇圈，却没有理由保持 χ(H)=m；大量短圈可能迫使删除的边集承载全部 m-色复杂性。不可数情形也缺少把有限 Rödl 界紧化为同一基数子图的紧致性原理。
- 下一步：先针对正则不可数 m，把短奇圈组成有限秩超图，检验是否能将其击边集分成 <m 个二部图或低色数图；若能，则至少一个剩余部分可能保留色数 m。首个目标应是 r=3。
- 来源核对：[Erdős Problems #740](https://www.erdosproblems.com/740) 当前明确标记 OPEN，并只列出 m=aleph₀、r=3 的 Rödl 结果。；本地 740.lean 量化所有 χ(G)≥aleph₀ 的图和所有自然数 r，并要求所得子图色数等于 G；与逐个无限基数的原题实质一致。；检索到的 [Komjáth–Shelah《Finite subgraphs of uncountably chromatic graphs》](https://arxiv.org/abs/math/0212064) 摘要不支持先前候选所述 K(ω+1)-free 一致性反例；该主张很可能混入了邻近但不同的问题。；[Erdős Problems 的版本记录](https://www.erdosproblems.com/history/740) 同样没有记录独立性或反例，因此不将本题分类为 independent。
- 时间记账：所在批次墙钟时间按题数均摊约 46.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/740)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/740.lean`；既有候选答案（按不可信材料审计）

### #741

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \mathbb{N}$ be such that $A+A$ has positive density. Can one always decompose $A=A_1\sqcup A_2$ such that $A_1+A_1$ and $A_2+A_2$ both have positive density? Is there a basis $A$ of order $2$ such that if $A=A_1\sqcup A_2$ then $A_1+A_1$ and $A_2+A_2$ cannot both have bounded gaps?
- 题意摘要：第一问必须区分三种量词：对每个 A⊆ℕ，若 A+A 的自然密度存在且为正（严格密度版），或仅上密度为正，是否存在不交分拆 A=A₁⊔A₂，使两个自和集具有相应正密度？第二问是：是否存在一个二阶渐近基 A，使对每个分拆 A=A₁⊔A₂，A₁+A₁ 与 A₂+A₂ 不可能同时 syndetic（有界间隙）？
- 状态核对：已知结论为：严格自然密度版第一问否；上密度版第一问是；第二问是；下密度版仍开。候选答案把两问均称为开放，已过时。本地 Lean 文件确实分别记录 False、upper=True、第二问=True，但当前工作区证明体是 sorry，只通过 formal_proof 属性指向外部已验证版本。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建上密度证明：取快速增长的端点 M₀<M₁<⋯，将 A 的相邻块交替赋给 A₁、A₂。若 A 本身上密度正，则在交替尺度上两部分各有正上密度，且 |X_N+X_N|≥2|X_N|−1。若 d̄(A)=0 而 d̄(A+A)>0，选 c>0 和 M_{j+1} 使 |(A+A)∩[1,M_{j+1}]|≥cM_{j+1} 且 M_j|A∩[1,M_{j+1}]|≤cM_{j+1}/4；旧颜色只出现在 [1,M_j]，故含旧颜色的和至多 M_j|A∩[1,M_{j+1}]| 个，留下至少 3cM_{j+1}/4 个新颜色自和。第二问采用“铰点”构造：建立越来越远的阶段，每阶段有 distinguished point c_k 和长区间 J_k，使 A+A 覆盖所有充分大整数，同时每个 n∈J_k 的表示都必须使用 c_k。
- 局部结论：若 d̄(X)>0，则 d̄(X+X)≥d̄(X)，因为 |(X∩[1,N])+(X∩[1,N])|≥2|X∩[1,N]|−1。；若 B∩[1,N]⊆[1,K]，则 |(X+B)∩[1,N]|≤K|X∩[1,N]|；这严格闭合了交替块证明中的误差估计。；在铰点构造中，某一颜色包含无穷多个 c_k；另一颜色的自和集避开相应 J_k。因 |J_k|→∞，该自和集不是 syndetic。
- 第一阻塞点：上密度版的交替块论证已闭合。对第二问，若不直接引用已发表/形式化证明，第一处需逐项核验的是阶段构造的隔离引理：除 c_k+B_k 外，旧阶段、同阶段其他块及未来阶段的和都不进入 J_k。下密度版不能沿交替尺度路线闭合，因为在稀疏好尺度之间没有统一下界。
- 下一步：逐行复核 APSSV 阶段参数所给的隔离不等式；另将 lowerDensity 版本单列，测试能否把“好尺度”加强为所有充分大尺度。
- 来源核对：官方题页（2026-05-02 更新）：https://www.erdosproblems.com/741；自包含证明笔记：https://www.ulam.ai/research/erdos741.pdf；本地 741.lean：严格密度 False、上密度 True、第二问 True、下密度 open
- 时间记账：所在批次墙钟时间按题数均摊约 61.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/741)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/741.lean`；既有候选答案（按不可信材料审计）

### #749

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$. Does there exist $A\subseteq \mathbb{N}$ such that the lower density of $A+A$ is at least $1-\epsilon$ and yet $1_A\ast 1_A(n) \ll_\epsilon 1$ for all $n$?
- 题意摘要：量词为：对每个 ε>0，是否存在 A⊆ℕ 及仅依赖 ε 的有限常数 C_ε，使下密度 d_(A+A)≥1−ε，并且对所有 n，ordered representation function r_A(n)=|(a,b)∈A²:a+b=n|≤C_ε。常数不能依赖 n。
- 状态核对：下密度版本仍开放；2026 年仅上密度版本已有构造。候选答案的开放判断基本正确，但遗漏了这一新的上密度进展。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试从有限循环群中的有界表示覆盖集出发做分块提升：在尺度 N_j 上放置稀疏、近 √N_j 大小的块，使块内和覆盖长度约 N_j 的绝大部分，并快速拉开尺度以避免不同块之间产生过多重合。目标是把有限模构造拼成具有下密度覆盖的无限集合。
- 局部结论：若 r_A(n)≤C，则对 A(x)=|A∩[0,x]| 有 A(x)²=∑_{n≤2x}r_{A∩[0,x]}(n)≤C(2x+1)，故 A(x)=O_C(√x)。；若 |(A+A)∩[0,N]|≥(1−ε)(N+1)，则每个被覆盖的和至少贡献一个表示，所以 A(N)²≥(1−ε)(N+1)；候选集合必须在无穷多个乃至所有大尺度上具有 √N 级规模。；单个有限块可以同时具有约 √N 个元素、线性多的不同和及有界块内表示；因此没有纯计数矛盾。
- 第一阻塞点：第一处无法闭合的是分块之间的交叉表示：对固定 n，来自许多不同尺度块对的表示可能累积；若把尺度拉得足够远来消除累积，则相邻尺度之间通常出现长覆盖空档，只能保证上密度而不能保证下密度。这正解释了为何已知上密度构造不能直接解决本题。
- 下一步：建立并计算一个两层有限模型：给定 C、ε，寻找 B⊆[0,N]，使 [0,N] 中至少 (1−ε)N 个数被 B+B 覆盖、每个和至多 C 次，并额外控制 B+B′ 的最大重数；检验这种“可拼接”有限模块能否在 N→∞ 时保持参数一致。
- 来源核对：官方题页及上密度变体更新：https://www.erdosproblems.com/749；本地 749.lean 的量词与 sumRep 定义一致
- 时间记账：所在批次墙钟时间按题数均摊约 61.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/749)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/749.lean`；既有候选答案（按不可信材料审计）

### #750

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $f(m)$ be some function such that $f(m)\to \infty$ as $m\to \infty$. Does there exist a graph $G$ of infinite chromatic number such that every subgraph on $m$ vertices contains an independent set of size at least $\frac{m}{2}-f(m)$?
- 题意摘要：正确量词是：对每个非负函数 f:ℕ→ℝ 且 f(m)→∞，是否存在一个无限色数图 G，使对每个 m≥1 和每个 m 元顶点集 S，都有独立集 I⊆S，满足 |I|≥m/2−f(m)。这里不是先选一个特殊 f，而是任意趋于无穷的 f。
- 状态核对：输入的 current_status='proved (Lean)'不正确：截至 2026-07 官方题页仍为 OPEN；本地 750.lean 也标记 research open，证明体为 sorry。形式化了命题不等于形式化证明。候选答案在这一点反而正确。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试把 Erdős–Hajnal–Szemerédi 的“有限子图近二分”结果对角化。更强的充分条件是每个 m 元诱导子图删去至多 2f(m) 个顶点后成为二分图，因为剩余二分图的一侧给出大小至少 m/2−f(m) 的独立集。设法构造色数趋于无穷的有限图序列，再取极限或并。
- 局部结论：若 H[S] 有一个至少 m−2f(m) 个顶点的诱导二分子图，则 α(H[S])≥(m−2f(m))/2=m/2−f(m)。；已知固定 η>0 时可以取得线性误差 ηm；因此本题对所有满足 f(m)≥ηm/2 的 m 已有相应局部机制。；对任意固定 M，条件 f(m)→∞ 对 m>M 没有解决 m≤M 的限制；这些有限限制可能要求禁掉三角形等特定小子图，但高色数本身与这些有限禁形并不矛盾。
- 第一阻塞点：线性误差 ηm 不能用一个固定 η 控制任意次线性 f(m)。令 η 随构造阶段趋零又产生循环依赖：EHS 图的阶数取决于 η，而所需 η≤2f(m)/m 必须覆盖直到该未知阶数。即使得到有限图序列，直接取不交并也未必保持不等式，因为一般没有 ∑f(m_i)≤f(∑m_i)。
- 下一步：先验证有限化命题：对给定 f 和 k，是否存在有限 χ≥k 的图，对其所有顶点子集满足目标不等式；若成立，再研究用紧致性构造嵌套极限，而非不交并。
- 来源核对：官方题页仍为开放：https://www.erdosproblems.com/750；本地 750.lean 明确标记 category research open；Erdős–Hajnal–Szemerédi 原论文：https://combinatorica.hu/~p_erdos/1982-11.pdf
- 时间记账：所在批次墙钟时间按题数均摊约 61.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/750)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/750.lean`；既有候选答案（按不可信材料审计）

### #757

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{R}$ be a set of size $n$ such that every subset $B\subseteq A$ with $\lvert B\rvert =4$ has $\lvert B-B\rvert\geq 11$. Find the best constant $c>0$ such that $A$ must always contain a Sidon set of size $\geq cn$.
- 题意摘要：设 A⊂ℝ、|A|=n，且每个四元子集 B 的六个正距离中至少五个不同，等价于 |B−B|≥11。求最大的统一常数 c，使每个这样的 A 都含有大小至少 cn 的 Sidon 子集，即其所有无序点对距离互不相同。
- 状态核对：问题仍开放，但候选界已过时。2026 年 Ma–Tang 将已知范围改进为 9/17≤c≤4/7。另有形式化错误：本地 IsAdmissible 使用 (B−B).ncard=11，而原题是 ≥11；等号错误地排除了 |B−B|=13 的 Sidon 四元组，因此该 Lean 命题不忠实于原题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把 A 中的三项等差数列作为三元超边。先证明在题设下，距离碰撞只能来自共享中点的两条边，即三项等差数列；于是 Sidon 子集恰是该三元超图的独立集。再尝试利用四点条件限制超边交叠，并转化为独立数下界。
- 局部结论：若两条相等距离使用四个互异端点，例如 b−a=d−c，则同时有 c−a=d−b，四点中出现至少两次碰撞，违反“至少五种距离”；故这种碰撞不可能。；两条相等距离若共享一个端点，排序后必为 y−x=z−y，即 {x,y,z} 是三项等差数列。因此在此类 A 中，S 为 Sidon 当且仅当 S 不含三项等差数列。；两个不同的三项等差数列不能共享两个点；否则其至多四点的并集中会产生至少两种距离碰撞。因此所得三元超图至少是线性的。
- 第一阻塞点：线性三元超图本身不足以推出线性独立数达到 9/17，更不能确定最优常数；一般线性三元超图甚至可能有次线性独立数。必须继续使用实数直线上的次序和等差方程，而候选答案在等价化后没有提供这一步。
- 下一步：从 Ma–Tang 的 9/17 证明中抽取一个可有限核验的结构引理：枚举一个顶点可参与的三项等差数列在“左端/中点/右端”三种角色下的允许交叠，并验证其加权删点递推是否确实给出 9/17。
- 来源核对：官方题页与最新界：https://www.erdosproblems.com/757；Ma–Tang 论文 arXiv:2602.23282（由官方讨论链接）；本地 757.lean：误将 ≥11 写成 =11
- 时间记账：所在批次墙钟时间按题数均摊约 61.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/757)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/757.lean`；既有候选答案（按不可信材料审计）

### #761

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：The cochromatic number of $G$, denoted by $\zeta(G)$, is the minimum number of colours needed to colour the vertices of $G$ such that each colour class induces either a complete graph or empty graph. The dichromatic number of $G$, denoted by $\delta(G)$, is the minimum number $k$ of colours required such that, in any orientation of the edges of $G$, there is a $k$-colouring of the vertices of $G$ such that there are no monochromatic oriented cycles. Must a graph with large chromatic number have large dichromatic number? Must a graph with large cochromatic number contain a graph with large dichromatic number?
- 题意摘要：对无向图 G，δ(G)=max_D χ⃗(D)，其中 D 遍历 G 的所有定向，χ⃗(D) 是把顶点分成无有向圈类的最少颜色数。第一问的精确量词是：对每个 k，是否存在 N(k)，使 χ(G)≥N(k) 蕴含 δ(G)≥k？第二问是：对每个 k，是否存在 Z(k)，使 ζ(G)≥Z(k) 蕴含 G 含某个子图 H 满足 δ(H)≥k？
- 状态核对：两问仍开放。候选答案对定义和开放状态基本正确；2026 年已有 list-chromatic/list-dichromatic 类比结果，但它依赖大列表色数，尚未解决普通色数版本。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试随机定向。设每个 k-着色（这里允许任意着色，目标是使某色类含有向圈）都含 q 个顶点互不交的单色 K_t。随机独立定向所有边；一个 K_t 的定向无圈当且仅当它是传递锦标赛，概率 p_t=t!/2^{t choose 2}。对全部至多 k^n 个着色作并合界。
- 局部结论：若 k^n p_t^q<1，则存在一个定向，使每个 k-着色至少有一个单色 K_t 非传递，因而含有向圈；故 δ(G)>k。；对 G=K_n，每个 k-着色可打包至少约 n/t−k 个互不交的单色 K_t。先取 t 足够大使 −log(p_t)/t>log k，再取 n 大，并合界成立；这独立重建了 δ(K_n)随 n 无界的基本机制。；该方法实际需要的不只是大 χ，而是每个 k-划分中有线性多个稠密、互不交的单色障碍。
- 第一阻塞点：高普通色数不保证上述 clique packing；高色数无三角图立即使 t≥3 的路线失效。高 ζ 也可能主要来自难以分成团或独立集的互补结构，而独立集在任何定向下自动无圈。第一处缺口因此是：从大 χ 或某个大 ζ 子图中提取足够多可独立随机化的潜在有向圈障碍。
- 下一步：把 K_t 换成固定含圈图 F，定义“每个 k-划分中的顶点不交 F 打包数”，并检验已知高色数稀疏图族是否能给出线性打包；若不能，寻找使用许多重叠圈的局部引理或列表色数桥梁。
- 来源核对：官方题页：https://www.erdosproblems.com/761；Mohar–Wu 分数版本：https://arxiv.org/abs/1510.05982；2026 列表版本：https://arxiv.org/abs/2603.01020
- 时间记账：所在批次墙钟时间按题数均摊约 61.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/761)；既有候选答案（按不可信材料审计）

### #766

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n;k,l)=\min \mathrm{ex}(n;G)$, where $G$ ranges over all graphs with $k$ vertices and $l$ edges. Give good estimates for $f(n;k,l)$ in the range $k<l\leq k^2/4$. For fixed $k$ and large $n$ is $f(n;k,l)$ a strictly monotone function of $l$?
- 题意摘要：固定整数 $k<l\le k^2/4$，令 $f(n;k,l)$ 为所有恰有 $k$ 个顶点、$l$ 条边的简单图 $G$ 的 Turán 数 $\mathrm{ex}(n;G)$ 的最小值。问题要求估计 $n\to\infty$ 时的量级，并问：对每个固定 $k$，是否存在 $n_0(k)$，使所有 $n\ge n_0(k)$ 时 $l\mapsto f(n;k,l)$ 在该整数区间严格递增？
- 状态核对：截至冻结日期仍为开放题。候选稿的非严格单调性和随机下界基本正确；但 theta 图段落没有证明所构造图一定含 $C_{2r}$，因而“匹配下界指数”不能接受。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先用删边比较证明非递减，再以随机图删副本法和 Kővári–Sós–Turán 定理夹逼。若 $l_1<l_2$，每个 $(k,l_2)$ 图都含一个同顶点集的 $(k,l_1)$ 子图 $H$，故 $\mathrm{ex}(n;H)\le\mathrm{ex}(n;G)$。随机取 $G(n,p)$，每个禁图副本删一条边，并令 $p\asymp n^{-(k-2)/(l-1)}$。上界则取最小的 $s$ 满足 $l\le s(k-s)$，选取一个 $l$ 边图 $G\subseteq K_{s,k-s}$。
- 局部结论：严格得到 $f(n;k,l_1)\le f(n;k,l_2)$；所以问题只剩严格性，而不是单调性本身。；对固定 $(k,l)$，有限多个同构类型允许统一常数，得到 $f(n;k,l)\ge c_{k,l}n^{2-(k-2)/(l-1)}$。；令 $s=\min\{j:l\le j(k-j)\}$，则 $f(n;k,l)\le\mathrm{ex}(n,K_{s,k-s})=O_{k,l}(n^{2-1/s})$。此外固定 $(k,l)$ 且 $n$ 充分大时，极小者可限制为二部图：存在二部候选给出 $o(n^2)$，而每个非二部候选由 Erdős–Stone 给出 $\Omega(n^2)$。
- 第一阻塞点：子图比较只能给 $\le$。要得到严格不等式，必须排除某个 $(k,l+1)$ 图 $G$ 与其删边子图 $H$ 具有相同 Turán 数，且还要同时控制两层有限极小化；现有比较没有提供正间隙。
- 下一步：对最小未决的固定 $k$ 枚举二部 $(k,l)$ 图，并检验相邻层候选之间是否存在已知的精确 Turán 数相等；这可直接发现严格性的有限反例，或确定第一个真正需要新估计的图对。
- 来源核对：官方页面仍标为 OPEN，并只记录 Dirac–Erdős 的边界外结果：https://www.erdosproblems.com/766；候选稿 theta 路线中的“含有 $C_{2r}$”没有从任意路径长度分配推出；不同长度路径形成的圈长度是两条路径长度之和，未必等于 $2r$。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/766)；既有候选答案（按不可信材料审计）

### #768

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{N}$ be the set of $n$ such that for every prime $p\mid n$ there exists some $d\mid n$ with $d>1$ such that $d\equiv 1\pmod{p}$. Is it true that there exists some constant $c>0$ such that for all large $N$\[\frac{\lvert A\cap [1,N]\rvert}{N}=\exp(-(c+o(1))\sqrt{\log N}\log\log N).\]
- 题意摘要：集合 $A$ 由所有正整数 $n$ 组成，满足：对每个素因子 $p\mid n$，都存在一个依赖于 $p$ 的除数 $d\mid n$，其中 $d>1$ 且 $d\equiv1\pmod p$。问题问是否存在同一个常数 $c>0$，使 $|A\cap[1,N]|/N=\exp(-(c+o(1))\sqrt{\log N}\log\log N)$。
- 状态核对：冻结状态为开放。候选稿主要复述已知上下界和光滑数启发，没有真正检查定义条件；下面给出一个直接的必要条件，但它远不足以达到目标计数尺度。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从最大素因子入手。设 $n>1$、$P=P^+(n)$，写成 $n=P^a m$，其中 $(P,m)=1$。把定义应用于 $p=P$，分析相应见证除数 $d$。随后尝试用最大素因子分布计数这些必要条件。
- 局部结论：见证 $d\equiv1\pmod P$ 不可能含因子 $P$，故 $d\mid m$；又因 $d>1$，必有 $m\ge d\ge P+1$。；因此每个 $n\in A\setminus\{1\}$ 都满足 $n=P^am\ge P(P+1)$，特别是 $P^+(n)<\sqrt n$。；这确实把 $A$ 包含在一类 $\sqrt n$-光滑整数中，但该集合仍有正比例数量，单独使用这一条件甚至不能重证密度为零。
- 第一阻塞点：定义要求对每个素因子分别存在一个乘法同余见证；最大素因子条件只给出一次光滑性约束。没有严格方法把这些相关的同余见证迭代成约 $\sqrt{\log N}\log\log N$ 的熵损失。候选稿用 Dickman 函数只能解释尺度，不能给出所需上界或常数存在性。
- 下一步：按素因子递减排列 $p_1>p_2>\cdots$，计算并证明可迭代的约束：每个 $p_i$ 必须有一个由其余素数幂组成、且乘积为 $1\pmod{p_i}$ 的子乘积；下一步是对前两层约束建立可求和的筛上界，并检查能否产生额外的 $\log\log N$ 因子。
- 来源核对：官方页面确认量词及 Erdős 的两侧界：https://www.erdosproblems.com/768；已知上界的指数为 $\sqrt{\log N\log\log N}$，而猜想尺度为 $\sqrt{\log N}\log\log N$；候选稿对此差距的描述正确，但光滑数类比不是证明。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/768)；既有候选答案（按不可信材料审计）

### #769

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c(n)$ be minimal such that if $k\geq c(n)$ then the $n$-dimensional unit cube can be decomposed into $k$ homothetic $n$-dimensional cubes. Give good bounds for $c(n)$ - in particular, is it true that $c(n) \gg n^n$?
- 题意摘要：令 $D_n$ 为能把单位 $n$-立方体分割成恰好 $k$ 个较小同似 $n$-立方体的整数 $k$ 的集合；$c(n)$ 是使 $[c(n),\infty)\cap\mathbb N\subseteq D_n$ 的最小阈值。问题要求估计 $c(n)$，尤其问是否存在绝对常数 $C>0$，使充分大 $n$ 有 $c(n)\ge Cn^n$。
- 状态核对：仍为开放题。已知一般下界只有 $2^{n+1}-1$。候选稿把 $c(3)=48$ 写得近似已知，但官方材料只称其为 Meier 猜想；其 Dehn 定理说明也没有给出可核验的必要性，应删除。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用可严格验证的“细分一个小立方体”路线。把任意一块等分为 $m^n$ 块，会使总块数增加 $m^n-1$。由此把可实现块数与由 $m^n-1$ 生成的数值半群联系起来，并检查这种算术构造能否反向产生 $n^n$ 级下界。
- 局部结论：对任意有限序列 $m_i\ge2$ 和 $t_i\ge0$，块数 $1+\sum_i t_i(m_i^n-1)$ 都可由反复细分实现。；若某个有限集合 $M$ 满足 $\gcd\{m^n-1:m\in M\}=1$，则该数值半群余有限，从而给出一个显式但通常很大的 $c(n)$ 上界；这也解释了问题 770 中共同最大公因数与本题的直接联系。；这条路线天然产生上界。它本身不能排除存在非层级、不同尺度的立方体分割，故不能推出 $c(n)\gg n^n$。
- 第一阻塞点：当 $n+1=p$ 为素数时，$m^n-1$ 对所有 $m<p$ 都被 $p$ 整除，确实使上述半群构造在小生成元上有同余障碍；但没有理由认为每个几何分割都来自逐块规则细分。因此把半群缺口提升为所有立方体分割的缺口是第一处无法闭合的步骤。
- 下一步：对一般同似立方体分割建立一个不依赖层级结构的模 $p$ 不变量：先在 $n=2,3$ 的已知小分割上测试候选不变量，再检验当 $p=n+1$ 时它是否强迫块数小于 $p^n$ 的某些剩余类不可实现。
- 来源核对：官方页面确认 $c(3)=48$ 只是猜想，并记录 Connor–Marmorino 的界：https://www.erdosproblems.com/769；已核对的已知范围为 $c(n)\ge2^{n+1}-1$（$n\ge3$）；若 $n+1$ 非素数则 $c(n)\le e^2n^n$，素数情形则 $c(n)\le1.8n^{n+1}$。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/769)；既有候选答案（按不可信材料审计）

### #770

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be minimal such that $2^n-1,3^n-1,\ldots,h(n)^n-1$ are mutually coprime. Does, for every prime $p$, the density $\delta_p$ of integers with $h(n)=p$ exist? Does $\liminf h(n)=\infty$? Is it true that if $p$ is the greatest prime such that $p-1\mid n$ and $p>n^\epsilon$ then $h(n)=p$?
- 题意摘要：这里“互素”必须解释为整体最大公因数为 $1$：$h(n)$ 是最小的 $m$，使 $\gcd(2^n-1,\ldots,m^n-1)=1$。三个问题分别是：每个素数 $p$ 的水平集 $\{n:h(n)=p\}$ 是否有自然密度；是否 $\liminf_{n\to\infty}h(n)=\infty$；以及对每个固定 $\varepsilon>0$，是否对充分大 $n$，若 $p$ 是满足 $p-1\mid n$ 的最大素数且 $p>n^\varepsilon$，便有 $h(n)=p$。
- 状态核对：三问均仍开放。本地 Lean 形式化明确采用整体 gcd，并把第三问写成 $\forall\varepsilon>0,\ \forall^{\mathrm{eventually}}n$。因此候选稿用单个 $n=4044$ 宣称第三问“为假”是量词错误：有限反例不能否定最终成立的命题。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把 $h(n)=p$ 化为模素数的连续幂剩余障碍。若素数 $q$ 整除 $\gcd_{2\le a<p}(a^n-1)$，则 $q>p-1$，且 $1,2,\ldots,p-1$ 全落在 $\mathbb F_q^*$ 的 $n$ 次单位根子群。加入 $p^n-1$ 后，只有当所有这种 $q$ 都不再整除时 gcd 才降为 $1$。
- 局部结论：若 $h(n)=m$ 且 $m$ 合成，写 $m=ab$、$2\le a,b<m$；此前 gcd 的任一素因子 $q$ 同时整除 $a^n-1,b^n-1$，也整除 $m^n-1$，矛盾。因此除低阶退化情形外 $h(n)$ 必为素数。；若 $p-1\mid n$，Fermat 定理给出 $p\mid a^n-1$（$2\le a<p$），故 $h(n)\ge p$；题目第三问正是在大 $p$ 条件下要求这个下界取等。；额外障碍可精确描述为素数 $q>p$，满足 $1,\ldots,p$ 全属于 $H_q=\{x\in\mathbb F_q^*:x^n=1\}$。于是 $p\le |H_q|=\gcd(n,q-1)\le n$，但这尚不与 $p>n^\varepsilon$ 冲突。
- 第一阻塞点：需要证明当 $p>n^\varepsilon$ 时，不存在一个素数 $q>p$，使某个阶整除 $n$ 的真乘法子群包含完整区间 $[1,p]$。初等子群大小界只有 $p\le n$，远弱于所需结论；必须获得适用于所有相关 $q$ 的长连续幂剩余区间界。
- 下一步：把第三问归约为可检验的字符和命题：若非平凡乘法特征 $\chi\pmod q$ 的阶整除 $n$，估计满足 $\chi(1)=\cdots=\chi(p)=1$ 的最大 $p$；检查 Burgess 型界在 $p>n^\varepsilon$ 且 $q$ 无先验上界时究竟缺少哪一个参数约束。
- 来源核对：官方状态与三问原文：https://www.erdosproblems.com/770；本地形式化文件确认 collective gcd 解释及第三问的 eventually 量词：/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/770.lean；本地定义把 $m$ 限为 $m>2$，所以不覆盖 $n=1$ 时可能的低阶退化；这不影响密度和渐近问题。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/770)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/770.lean`；既有候选答案（按不可信材料审计）

### #773

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：What is the size of the largest Sidon subset $A\subseteq\{1,2^2,\ldots,N^2\}$? Is it $N^{1-o(1)}$?
- 题意摘要：令 $F(N)$ 为集合 $\{1^2,2^2,\ldots,N^2\}$ 的最大 Sidon 子集大小；即所有无序和 $a+b$（允许 $a=b$）两两不同。问题问 $F(N)$ 的量级，尤其是否 $F(N)=N^{1-o(1)}$。
- 状态核对：冻结日期时已知 $N^{2/3}\ll F(N)\ll N/(\log N)^{1/4}$，问题开放。候选稿正确重建了这两个冻结界。不过 2026 年冻结后出现了更强上界 $F(N)\le N\exp(-c\log N/\log\log N)$；它仍与 $N^{1-o(1)}$ 相容，故未解决原问题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：建立四元冲突超图：顶点为 $[N]$，每个非平凡等式 $x^2+y^2=z^2+w^2$ 是一个坏关系。先估计坏关系数 $Q$，再随机保留顶点并对每个残留坏关系删去一个顶点。由 $(x-z)(x+z)=(w-y)(w+y)$ 和除数函数界，可得 $Q\le N^{2+o(1)}$。
- 局部结论：若以概率 $p$ 选择每个指标，则期望保留 $pN$ 个顶点、产生至多 $p^4Q$ 个坏关系；取近似最优 $p\asymp(N/Q)^{1/3}$ 并逐个删除，得到 $F(N)\ge N^{2/3-o(1)}$。；Sidon 性使 $\binom{F(N)+1}{2}$ 个和互异；Landau–Ramanujan 计数给出至多 $O(N^2/\sqrt{\log N})$ 个候选和，因此 $F(N)\ll N/(\log N)^{1/4}$。；单纯的一阶随机删除损失了 $N^{o(1)}$；要达到 Lefmann–Thiele 的干净 $\gg N^{2/3}$，必须利用冲突超图的度与余度结构，而不能只用总边数。
- 第一阻塞点：该路线只控制冲突总数，无法把 $N^{2+o(1)}$ 改成足以直接给出近线性 Sidon 集的规模，也没有显示冲突集中在少量顶点上。因而从 $N^{2/3}$ 跳到 $N^{1-o(1)}$ 的第一处缺口是缺少强得多的结构或容器定理输入。
- 下一步：计算冲突超图的顶点度和二点余度的统一上界，并对高表示数的和单独截断；随后检验超图容器或局部引理能否把独立集下界提升到 $N^{2/3+\eta}$，哪怕只对固定小 $\eta>0$。
- 来源核对：冻结界及官方状态：https://www.erdosproblems.com/773；冻结后预印本给出 $F(N)\le N\exp(-c\log N/\log\log N)$：https://arxiv.org/abs/2606.17487；新上界等于 $N^{1-c/\log\log N}$，指数仍趋于 $1$，所以它不能否定也不能证明 $F(N)=N^{1-o(1)}$。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/773)；既有候选答案（按不可信材料审计）

### #774

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：We call $A\subset \mathbb{N}$ dissociated if $\sum_{n\in X}n\neq \sum_{m\in Y}m$ for all finite $X,Y\subset A$ with $X\neq Y$. Let $A\subset \mathbb{N}$ be an infinite set. We call $A$ proportionately dissociated if every finite $B\subset A$ contains a dissociated set of size $\gg \lvert B\rvert$. Is every proportionately dissociated set the union of a finite number of dissociated sets?
- 题意摘要：对象是无限集 A⊆ℕ。存在一个只依赖于 A 的常数 c>0，使每个有限 B⊆A 都含有 S⊆B，满足 |S|≥c|B| 且 S 的所有有限子集和互异。问题问：是否存在有限个 dissociated 集 D₁,…,D_t，使 A=⋃D_i？
- 状态核对：截至 2026-07 官方仍标为 open。形式化文件也明确量化了全局常数 c、A 的无限性及有限并覆盖。先前答案只是在报告状态，没有构成证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：把所有最小的 {-1,0,1} 加法关系之支撑看成超图边；dissociated 集正是该关系超图的独立集。尝试从“每个有限诱导子超图都有线性大独立集”迭代抽取颜色类，进而得到有限着色。
- 局部结论：D dissociated 等价于不存在有限支撑、非全零的 ε_a∈{-1,0,1} 使 ∑ε_a a=0；这是把两个子集和相等后消去交集所得。；若 A 已是 t 个 dissociated 集之并，则任意有限 B⊆A 至少有一个交集 B∩D_i 的大小不小于 |B|/t，故反向蕴含成立，常数可取 1/t。；在给定比例常数 c 下，反复从余集抽取大小至少 c 倍的 dissociated 集，可把任意有限 B 分成至多 ⌈log|B|/(-log(1-c))⌉+1 个 dissociated 集。
- 第一阻塞点：迭代只给 O(log|B|) 个颜色，无法得到与 |B| 无关的常数。一般遗传超图中“每个诱导子图有线性独立集”并不自动推出有界色数；尚缺利用整数 {-1,0,1} 关系结构排除这种对数增长的引理。
- 下一步：检验一个明确的受限版本：若所有最小加法关系的支撑大小≤s，比例独立数条件是否推出只依赖 c,s 的色数界；先从 s=3、4 建模为有界秩关系超图并寻找证明或有限反例。
- 来源核对：[Erdős Problems #774](https://www.erdosproblems.com/774) 于 2025-12-28 更新后仍列为 open，并说明 Pisier 等价与相关 Sidon 变体的反例不能解决原问题。；已核对本地 FormalConjectures/ErdosProblems/774.lean：其定义确实要求 ∃c>0 对所有有限 B⊆A 一致成立。
- 时间记账：所在批次墙钟时间按题数均摊约 61.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/774)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/774.lean`；既有候选答案（按不可信材料审计）

### #776

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$ and $A_1,\ldots,A_m\subseteq \{1,\ldots,n\}$ be such that $A_i\not\subseteq A_j$ for all $i\neq j$ and for any $t$ if there exists some $i$ with $\lvert A_i\rvert=t$ then there must exist at least $r$ sets of that size. How large must $n$ be (as a function of $r$) to ensure that there is such a family which achieves $n-3$ distinct sizes of sets?
- 题意摘要：令 𝓕⊆2^[n] 为反链，即任意不同 A,B∈𝓕 均有 A⊄B；每个实际出现的层 𝓕_t={A∈𝓕:|A|=t} 都满足 |𝓕_t|≥r。求阈值 n₀(r)，使每个 n>n₀(r) 都存在恰好出现 n-3 个不同大小的这种反链。
- 状态核对：输入状态已滞后：问题仍未得到精确 n₀(r)，但 2026 年已有实质性部分解：n₀(2)=3、n₀(3)=8，且 r≥4 时 2r+2≤n₀(r)≤2r+2log₂r+O(log log r)，所以 n₀(r)∼2r。先前候选的 Ω(√r) 与“约 2r+1”猜测已被更新结果取代；其以 r>n 强迫遗漏第 1 层的理由也不是正确的结构性理由。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：从极端层的影限制入手。因为 0、n 层各只有一个集合，必定缺失；要出现 n-3 层，只能再缺两个内部层。分析若第 1 层或第 n-1 层出现 r 次，会强迫大量其他层消失，再把第 2 与第 n-2 层转成两族交叉相交的边，作为线性下界路线的起点。
- 局部结论：若第 1 层含 r 个单点，所有其他成员都必须避开这 r 个点，故其大小至多 n-r；于是 n-r+1,…,n 全部缺失。对偶地，若第 n-1 层出现 r 次，则任何更小成员必须包含相应的 r 个缺失点，故 0,…,r-1 层缺失。特别地，r≥5 时要只缺四层，就必须恰好出现 2,3,…,n-2 层。；设第 2 层选出的 r 个集合为 E_i，第 n-2 层选出的 r 个集合的补集为 F_j。反链条件等价于 E_i∩F_j≠∅ 对所有 i,j，即得到两族各含 r 条边的交叉相交图问题。；He–Tang 已严格证明 n₀(r)=2r+o(r)，并给出上述上下界；因此正确的一阶尺度是 2r，而不是先前答案的 √r 计数尺度。
- 第一阻塞点：仅由两族 2-边交叉相交还推不出 n₀(r)≥2r+2，因为未使用所有中间层同时存在所施加的迭代影约束。重建论文证明时，第一处关键缺口是把这些跨层约束压缩成足够强的核/影不等式。
- 下一步：逐引理核对 He–Tang 的下界证明：从 2 层与 n-2 层的交叉相交结构出发，验证其如何利用第 3、n-3 层排除 n≤2r+2；随后检查上界构造中 2log₂r 项来自何种二进制编码。
- 来源核对：[He–Tang 论文摘要](https://arxiv.org/abs/2602.09803) 明列 n₀(2)=3、n₀(3)=8 及 2r+2≤n₀(r)≤2r+2log₂r+O(log₂log₂r)。；[Erdős Problems #776](https://www.erdosproblems.com/776) 已于 2026-04 纳入该部分结果，但仍将精确问题列为 open。
- 时间记账：所在批次墙钟时间按题数均摊约 61.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/776)；既有候选答案（按不可信材料审计）

### #778

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Alice and Bob play a game on the edges of $K_n$, alternating colouring edges by red (Alice) and blue (Bob). Alice goes first, and wins if at the end the largest red clique is larger than any of the blue cliques. Does Bob have a winning strategy for $n\geq 3$? (Erd\H{o}s believed the answer is yes.) If we change the game so that Bob colours two edges after each edge that Alice colours, but now require Bob's largest clique to be strictly larger than Alice's, then does Bob have a winning strategy for $n>3$? Finally, consider the game when Alice wins if the maximum degree of the red subgraph is larger than the maximum degree of the blue subgraph. Who wins?
- 题意摘要：包含三个有限完全信息游戏：(i) Alice、Bob 依次各染一条未染边红、蓝，Alice 先手；终局仅当 ω(R)>ω(B) 时 Alice 胜，故平局归 Bob，问所有 n≥3 是否 Bob 胜。(ii) Alice 每轮一边、Bob 随后两边；这次仅当 ω(B)>ω(R) 时 Bob 胜，问 n>3 是否总能做到。(iii) 恢复一比一走子，以 Δ(R)>Δ(B) 为 Alice 胜负标准，问胜者。
- 状态核对：截至 2026-07 三问整体仍 open。已知第一问 Bob 获胜的 n 密度至少 3/4，且 Alice 若在 n 获胜，则 Bob 在 n+1,n+2,n+3 获胜；第三问相应密度至少 2/3。先前候选引用了未在官方上下文核实的后续小规模结论，本筛查不依赖它们。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：尝试用顶点置换诱导的边轨道作在线回应策略。无偏游戏用无不动点对合 π 配对非匹配边；1:2 游戏在 3|n 时用阶为 3、无固定顶点的 π，把每个三边轨道中 Alice 取得的一边之外的两边全部交给 Bob。
- 局部结论：在 1:2 游戏且 3|n 时，可把顶点分成三循环并令 π 同时旋转。每条边的轨道大小都是 3；Bob 吃掉 Alice 所在轨道的另外两边。于是每个红团 K 的 π(K) 与 π²(K) 都是同样大小的蓝团，严格得到 ω(B)≥ω(R)。；无偏情形若 n≡0 mod 4，可用无固定点对合 π 配对全部非匹配边，并把 π 的固定匹配边彼此配对。任何不含 π-匹配边的红团都会被 π 映成同样大小的蓝团。；同一对合策略用于最大度游戏时，对每个顶点 v，非匹配红度恰等于 π(v) 的非匹配蓝度；匹配边只造成至多 1 的误差，因此可推出 |Δ(R)-Δ(B)|≤1。
- 第一阻塞点：三条路线都恰差题目所需的一格：1:2 策略只能保证团数不小于而非严格更大；无偏团策略无法处理含对合固定匹配边的红团；度数策略只能得到 Δ(B)≥Δ(R)-1，不能排除 Alice 领先 1。
- 下一步：对 1:2 且 3|n 的轨道策略做局部增强搜索：给定一个最大红团 K，检验是否能在 π(K) 外找到一个对所有 π(K) 顶点均为蓝邻接的额外顶点；若失败，枚举最小反例的轨道型以识别严格不等式的真实障碍。
- 来源核对：[Erdős Problems #778](https://www.erdosproblems.com/778) 当前仍列 open，并记录第一问的 3/4 密度及第三问的 2/3 密度结果。；[Malekshahian–Spiro 原始预印本](https://arxiv.org/abs/2410.18304) 的摘要核实了第一问的游戏定义与 Erdős 猜想。
- 时间记账：所在批次墙钟时间按题数均摊约 61.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/778)；既有候选答案（按不可信材料审计）

### #782

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Do the squares contain arbitrarily long quasi-progressions? That is, does there exist some constant $C>0$ such that, for any $k$, the squares contain a sequence $x_1,\ldots,x_k$ where, for some $d$ and all $1\leq i<k$,\[x_i+d\leq x_{i+1}\leq x_i+d+C.\]Do the squares contain arbitrarily large cubes\[a+\left\{ \sum_i \epsilon_ib_i : \epsilon_i\in \{0,1\}\right\}?\]
- 题意摘要：第一问要求存在一个与 k 无关的绝对常数 C>0，使每个 k 都有 k 个平方数 x_i 和某个共同整数步长 d，满足 d≤x_{i+1}-x_i≤d+C。第二问按标准非退化含义要求：对任意维数s，存在 a,b₁,…,b_s，使所有 2^s 个互异数 a+∑ε_i b_i 都是平方数；若允许 b_i=0 或子集和重合，问题会退化。
- 状态核对：截至 2026-07 两问均 open；已知第一问肯定会推出第二问肯定，而 Bombieri–Lang 猜想蕴含第二问否定。先前候选所列更细数值结果未由给定官方材料支持，本筛查不把它们当作已核实事实。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：第一问把平方数写成 x_i=y_i²，并研究近乎恒定的平方间隙；第二问则把每个立方体顶点写成平方根变量，把所有二维面转成二次丢番图方程，尝试进入高型曲线/簇与 Bombieri–Lang 路线。
- 局部结论：令 g_i=x_{i+1}-x_i=d+δ_i，其中 0≤δ_i≤C。则 x_i=x_1+(i-1)d+E_i，E_i=∑_{j<i}δ_j，故 0≤E_i≤(i-1)C。误差会线性累积，不能直接把长准进展压成固定宽度内的真正等差数列。；若 y_{i+1}=y_i+h_i，则 g_i=2y_i h_i+h_i²，且所有这些整数都落在同一长度 C 的区间内；因此 |(2y_i h_i+h_i²)-(2y_j h_j+h_j²)|≤C。这给出明确的近丢番图约束，但尚不强迫 h_i 恒定。；任一平方立方体的二维面满足 y_{00}²+y_{11}²=y_{10}²+y_{01}²。维数增加时这些方程高度耦合；这正是把大立方体解释为代数簇上大量有理点的入口。
- 第一阻塞点：近恒定平方间隙公式尚不能控制整数步长 h_i 的升降；误差 E_i 随 i 增长，经典“四个平方不能成等差数列”不能直接应用。立方体路线的第一处非闭合步骤则是无条件证明相关高维代数簇的有理点一致有界；现有负结论需要 Bombieri–Lang。
- 下一步：先做一个有限、可证伪的子任务：固定 C，枚举并分类允许连续三次改变 h_i 的局部模式，利用 |g_i-g_j|≤C 推导 y_i 的显式上界；若成立，可把长序列迫入 h_i 单调或周期的有限状态问题。
- 来源核对：[Erdős Problems #782](https://www.erdosproblems.com/782) 于当前抓取仍标为 open，并明确记录 QP⇒cube 及 Bombieri–Lang 条件否定 cube。；官方页面未报告评论中的任何完整或部分解，故没有把先前候选的额外文献断言视为本次证明依据。
- 时间记账：所在批次墙钟时间按题数均摊约 61.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/782)；既有候选答案（按不可信材料审计）

### #783

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Fix some constant $C>0$ and let $n$ be large. Let $A\subseteq \{2,\ldots,n\}$ be such that $(a,b)=1$ for all $a\neq b\in A$ and $\sum_{n\in A}\frac{1}{n}\leq C$. What choice of such an $A$ minimises the number of integers $m\leq n$ not divisible by any $a\in A$? Is this minimised by letting $n\geq q_1>q_2>\cdots$ be the consecutive primes in decreasing order and choosing $A=\{q_1,\ldots,q_k\}$ where $k$ is maximal such that\[\sum_{i=1}^k\frac{1}{q_i}\leq C?\]
- 题意摘要：固定 C>0。对每个大 N，在所有有限、两两互素的 A⊆{2,…,N} 且 μ(A):=∑_{a∈A}1/a≤C 中，最小化 U_A(N)=#{m≤N:∀a∈A,a∤m}。原猜测候选是从最大素数≤N 向下取连续素数尾段，直到 reciprocal budget 尽量饱和。
- 状态核对：状态为 solved，但解决的是 Erdős 所意指的渐近极值：min_A U_A(N)=(ρ(e^C)+o(1))N。素数尾段达到该值；一般 C 下它未必是逐个 N 的字面唯一极小集，精细有限 N 分类仍开放。C≤log 2 时已有字面极值结果。人工评审指出的错误完全成立：当 |A|→∞ 时不能用 U_A(N)≈N∏(1-1/a) 而无一致误差控制；先前以此得 e^{-C} 并构造反例的比较无效。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建已知筛法路线：先保留精确容斥；按模数大小分成小、中、大三段。大合数利用两两互素性和最小素因子计数证明稀少；中段用二进分割选成总贡献可忽略；小段用 Brun 筛替换成具有近似相同 Euler 数据的素数集合，最后调用 Hildebrand 的素数情形和 Dickman 函数不等式 ρ(u₁)ρ(u₂)≥ρ(u₁u₂)。
- 局部结论：精确恒等式为 U_A(N)=∑_{S⊆A}(-1)^{|S|}⌊N/∏_{a∈S}a⌋。把每个下取整替换为 N/∏a 的总误差粗界是 2^{|A|}，当 |A| 增长时完全可能不可忽略；这直接吸收了人工评审。；对素数尾段 A={p:y<p≤N}，未被任何 a 整除的 m≤N 恰是所有素因子≤y 的 y-smooth 数，故 U_A(N)=Ψ(N,y) 精确成立。由 ∑_{y<p≤N}1/p=C+o(1) 得 y=N^{e^{-C}+o(1)}，于是 Ψ(N,y)=(ρ(e^C)+o(1))N。；已知筛法归约给任意 admissible A 下界 U_A(N)≥(ρ(e^C)+o(1))N；与素数尾段上界匹配，故它在 o(N) 精度下渐近最优。
- 第一阻塞点：若只从上述初等容斥开始，第一处不能自行闭合的是对小模数作统一替换而保持筛余集合下界；朴素乘积近似正是在这里失效。已知证明用纯 Brun 筛、Hildebrand 素数情形及 ρ 的对数凹性补上。尚未闭合的是更精确的有限 N 极小集分类，而不是主项渐近式。
- 下一步：可检验的后续任务是逐项复核修正版证明中的小素数引理：明确验证 ρ(u₁)ρ(u₂)≥ρ(u₁u₂) 的使用方向，并追踪三段分解的误差对所有两两互素 A 一致为 o(N)；这也是早期版本曾出现符号错误的位置。
- 来源核对：[Erdős Problems #783](https://www.erdosproblems.com/783) 于 2026-05-28 标为 solved，并给出 Tao 的渐近下界及素数尾段构造。；[官方讨论串](https://www.erdosproblems.com/forum/thread/783) 记录了修正机制：早期小素数论证有致命符号错误，修正版使用 ρ(u₁)ρ(u₂)≥ρ(u₁u₂)；本答案采用修正版而未复述错误论证。；同一讨论串明确指出精确有限 N 极值及比 o(N) 更细的误差仍未完全解决，因此没有把“solved”夸大为完整分类。
- 时间记账：所在批次墙钟时间按题数均摊约 61.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/783)；既有候选答案（按不可信材料审计）

### #786

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$. Is there some set $A\subset \mathbb{N}$ of density $>1-\epsilon$ such that $a_1\cdots a_r=b_1\cdots b_s$ with $a_i,b_j\in A$ can only hold when $r=s$? Similarly, can one always find a set $A\subset\{1,\ldots,N\}$ with this property of size $\geq (1-o(1))N$?
- 题意摘要：按字面解释，乘积中的因子允许重复：问对每个 ε>0，是否存在具有自然密度 >1-ε 的 A⊆ℕ，使任意有限序列 a_i,b_j∈A 满足 ∏a_i=∏b_j 时必有 r=s；有限版问是否对每个大 N 可取 |A_N|=(1-o(1))N。若要求同侧因子互异，则是另一较弱版本。
- 状态核对：冻结状态已过时。2026 年更新表明：允许重复的字面版本已有否定答案；互异因子版本仍开放。本地 Lean 的 IsMulCardSet 用 Finset，只形式化了互异版本，不能据此证明字面版本仍开放。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：允许重复时，把整数写成素数指数向量 v(n)。性质保证赋值 v(a)↦1 在 A 生成的自由阿贝尔群上相容：若两种整数线性表示相等，把正负部分移项即得到两个 A-乘积相等，故两侧系数和相同。于是得到加性函数 F，并有 A⊆{n:F(n)=1}；可再把 A 扩大到整个一级集。随后应用 Erdős–Ruzsa–Sárközy 关于加性函数一级集的密度定理。
- 局部结论：上述线性化严格说明：任何允许重复的可行 A 都嵌入某个完全加性函数 F 的一级集。；ERS 定理给出该一级集的密度至多 1/2，因此取 ε<1/2 即否定无限版；相应有限定理给出 |A_N|≤(1-c)N，否定 (1-o(1))N。；Selfridge 路线须取 Σ_i v_{p_i}(a)=1，而不只是“恰被一个 p_i 整除”。此时乘积取该加性权重立即推出 r=s，密度为 ∏_i(1-1/p_i)·Σ_i1/p_i≈e^{-1}。先前候选所说“扔掉可忽略的平方倍数”方向正确但条件必须明确，不能把原集合直接用于赋值计数。
- 第一阻塞点：这条路线完全处理允许重复版本，却不适用于 Finset/互异版本：相同元素不能重复使用，因而整数关系中的系数不能任意移项实现，F 的良定义在这里首次失败。
- 下一步：对互异版本，检验“有限整数关系是否能通过引入辅助元素模拟为 0/1 关系”；先在小素数指数维数上用 SAT/整数规划搜索是否存在高密度集合而没有可扩张的加性权重。
- 来源核对：[Erdős Problems #786（2026-04-11 更新）](https://www.erdosproblems.com/786)明确区分重复与互异版本，并记录 ERS 定理给重复版本的否定答案。；已读取本地 786.lean：其定义量化 Finset，且文件注释也承认网页原意可能允许重复。
- 时间记账：所在批次墙钟时间按题数均摊约 91.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/786)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/786.lean`；既有候选答案（按不可信材料审计）

### #787

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ be maximal such that given any set $A\subset \mathbb{R}$ with $\lvert A\rvert=n$ there exists some $B\subseteq A$ of size $\lvert B\rvert\geq g(n)$ such that $b_1+b_2\not\in A$ for all $b_1\neq b_2\in B$. Estimate $g(n)$.
- 题意摘要：精确定义为 g(n)=min_{A⊆ℝ,|A|=n} max{|B|:B⊆A，且任意互异 x,y∈B 都有 x+y∉A}；注意禁集是原来的 A，而不只是 B。
- 状态核对：仍开放。已知范围为 (log n)^{1+1/68+o(1)}≪g(n)≪exp(O(√log n))；这里只独立重建初等的 Ω(log n) 路线。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：从 A 中取较大的同号部分 P，故 |P|≥(n-1)/2。在 P 上连边 xy 当且仅当 x+y∈A。若 P 为正数并按 x_1<⋯<x_m 排列，则对固定 x_i，每个邻点对应唯一的和 x_i+x_j，它是 A 中大于 x_i 的正元素，所以 deg(x_i)≤m-i；负数情形反向排序同理。对该图应用 Caro–Wei 界。
- 局部结论：所求 B 正是上述图的独立集。；α(G)≥Σ_i1/(deg(x_i)+1)≥Σ_{j=1}^m1/j=H_m，因此 g(n)≥log n-O(1)。；先前候选中“把负数乘以 −1”若只变换选出的半边，并不自动保持“和属于原 A”；直接对负数反向排序可修复此处。
- 第一阻塞点：度数界只给调和级别；要超过 log n，必须利用不同顶点的邻域受加法关系耦合。Caro–Wei 将这些邻域当作任意图，正是在此处丢失了 Sanders/Beker 所需的配置结构。
- 下一步：证明并量化一个可检验的局部命题：若许多顶点度数落在同一二进尺度，邻域平移关系必须产生多少个 k-configuration；再将该计数代入独立集抽样，而不是只用度数。
- 来源核对：[Erdős Problems #787](https://www.erdosproblems.com/787)核对了开放状态、Klarner 初等下界及 Sanders、Ruzsa、Beker 的当前界。
- 时间记账：所在批次墙钟时间按题数均摊约 91.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/787)；既有候选答案（按不可信材料审计）

### #788

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that if $B\subset (2n,4n)\cap \mathbb{N}$ there exists some $C\subset (n,2n)\cap \mathbb{N}$ such that $c_1+c_2\not\in B$ for all $c_1\neq c_2\in C$ and $\lvert C\rvert+\lvert B\rvert \geq f(n)$. Estimate $f(n)$. In particular is it true that $f(n)\leq n^{1/2+o(1)}$?
- 题意摘要：令 V=(n,2n)∩ℕ。对每个 B⊆(2n,4n)∩ℕ，要求存在 C⊆V，C 中任意不同两数之和不在 B；f(n) 是对所有 B 都能保证的 |B|+|C| 的最大下界，即 f(n)=min_B(|B|+α(G_B))，其中 xy∈E(G_B)⇔x+y∈B。
- 状态核对：仍开放，但 2026 年已有输入未收录的改进 f(n)≤n^{3/5+o(1)}。人工评审关于 Alon–Pham 路线存在依据，但先前候选宣称 O(√(n log n))、进而肯定 n^{1/2+o(1)} 是错误的；相关 Lean 工作只形式化归约并把 Alon–Pham 定理作为假设，并非端到端证明该猜想。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：下界用 G_B 是 |B| 个匹配之并。上界取素数 q∈(4n,8n)，把 V 嵌入 ℤ/qℤ；取密度 p 的随机 Cayley 和生成集 S，并令 B=S∩(2n,4n)。因 V 中两数之和小于 q，G_B 正是完整 Cayley 和图在 V 上的诱导子图。调用 Alon–Pham 的 α≤p^{-3/2}·(log q)^{O(1)}，同时 |S|=O(pq)。
- 局部结论：若 m=|B|，则 Δ(G_B)≤m，故 α(G_B)≥(n-1)/(m+1)，从而 f(n)≥2√(n-1)-1。；嵌入无模回绕，且 α(G_B)≤α(G_S)、|B|≤|S|，所以存在 B 满足 |B|+α(G_B)≤O(pn)+p^{-3/2}(log n)^{O(1)}。；取 p=n^{-2/5} 并吸收多对数，得到 f(n)≤n^{3/5+o(1)}。
- 第一阻塞点：要达到 n^{1/2+o(1)}，同一平衡要求随机 Cayley 和图满足 α≤p^{-1+o(1)}；Alon–Pham 目前只证明指数 3/2 的界，而最优指数仍是其猜想。先前候选假定的 α≈n log n/|B| 没有得到证明。
- 下一步：逐项核对 Alon–Pham Theorem 4 的 p 取值范围和多对数常数，并写出从 ℤ/qℤ 到开区间 (2n,4n) 的完整概率事件交集；这可把 n^{3/5+o(1)} 归约整理成可发表的独立引理。
- 来源核对：[Erdős Problems #788 的 2026 更新](https://www.erdosproblems.com/788)已记录 n^{3/5+o(1)}，并明确平方根指数仍依赖 Cayley 图猜想。；核对了 Alon–Pham 的原始预印本 [Random Cayley graphs and random sumsets](https://arxiv.org/abs/2509.02561) 中随机 Cayley 和图独立数定理。
- 时间记账：所在批次墙钟时间按题数均摊约 91.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/788)；既有候选答案（按不可信材料审计）

### #789

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be maximal such that if $A\subseteq \mathbb{Z}$ with $\lvert A\rvert=n$ then there is $B\subseteq A$ with $\lvert B\rvert \geq h(n)$ such that if $a_1+\cdots+a_r=b_1+\cdots+b_s$ with $a_i,b_i\in B$ then $r=s$. Estimate $h(n)$.
- 题意摘要：经典且本地形式化采用的对象是非空子集和：h(n)=min_{|A|=n}max|B|，其中 B⊆A，且任意两个非空子集 S,T⊆B 若 ΣS=ΣT，则 |S|=|T|；各元素在每个和中至多出现一次。
- 状态核对：此子集和版本仍开放，已知 (n log n)^{1/3}≪h(n)≪n^{1/2}。原题文字未写“互异”；若真允许重复，则取 A={1,…,n} 时任何含两个正整数 x≠y 的 B 都因 (y/g)·x=(x/g)·y 且项数不同而失败，问题退化到常数级。因此先前候选指出歧义是必要的，但不能把未写出的条件静默加入结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：重建 Erdős 的随机圆周筛选。给定 k 满足 4k^3≤n-1，令 θ=1/(2k)、δ=1/(4k²)。随机取 α∈[0,1]，保留非零 a∈A 中满足 {αa}∈(θ-δ/2,θ+δ/2) 的元素；期望个数至少 (n-1)δ≥k，故某个 α 可选出 k 元集合 B。
- 局部结论：若 S,T⊆B、1≤|S|,|T|≤k 且和相等，令 d=|S|-|T|。模 1 后 dθ 到整数的距离至多 (|S|+|T|)δ/2≤1/(4k)。；若 d≠0，则 1≤|d|≤k-1，而 dist(d/(2k),ℤ)≥1/(2k)，矛盾；因此 |S|=|T|。；于是严格得到 h(n)≥⌊((n-1)/4)^{1/3}⌋，但尚未恢复已知的 (log n)^{1/3} 增益。
- 第一阻塞点：单一区间方案中，分离 k 个基数层迫使区间宽度 δ=O(k^{-2})；而期望保留 nδ 个元素，条件 nδ≥k 只能给 k=O(n^{1/3})。这就是该具体路线首次遇到的定量壁垒。
- 下一步：尝试以多个间隔良好的短弧替代单弧，并计算二阶矩：检验能否在保持所有 1≤r≠s≤k 的 rI、sI 不相交时，把总测度提高到 Ω(k^{-2}log k)。
- 来源核对：[Erdős Problems #789](https://www.erdosproblems.com/789)核对了随机 α 构造和当前上下界。；已读取本地 789.lean：它明确量化非空 Finset S,T，确认形式化对象是互异项的子集和。
- 时间记账：所在批次墙钟时间按题数均摊约 91.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/789)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/789.lean`；既有候选答案（按不可信材料审计）

### #790

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $l(n)$ be maximal such that if $A\subset\mathbb{Z}$ with $\lvert A\rvert=n$ then there exists a sum-free $B\subseteq A$ with $\lvert B\rvert \geq l(n)$ - that is, $B$ is such that there are no solutions to\[a_1=a_2+\cdots+a_r\]with $a_i\in B$ all distinct. Estimate $l(n)$. In particular, is it true that $l(n)n^{-1/2}\to \infty$? Is it true that $l(n)< n^{1-c}$ for some $c>0$?
- 题意摘要：定义 l(n)=min_{A⊆ℤ,|A|=n}max{|B|:B⊆A，且不存在两两互异的 a_1,…,a_r∈B（r≥2）满足 a_1=a_2+⋯+a_r}。问题既问总体阶，也分别问 l(n)/√n→∞ 及是否存在固定 c>0 使 l(n)<n^{1-c}。
- 状态核对：总体仍开放；第一个特问已由 Choi–Komlós–Szemerédi 的下界肯定解决，第二个特问仍开放，且其 n^{1-o(1)} 猜想预言答案是否定的。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `5/10`；置信度 `high`
- 尝试路线：以 CKS 定理为已知输入重建两个特问的逻辑后果：对每个 n 元整数集均有强无和子集大小 ≥c√(n log n/loglog n)，同时存在坏集合使最大此类子集 ≤Cn/log n。随后尝试把上界加强为多项式节省，形式化为对候选大子集族的容器计数问题。
- 局部结论：由 l(n)≥c√(n log n/loglog n)，立即有 l(n)/√n≥c√(log n/loglog n)→∞；第一个特问答案为是。；已知 l(n)≤Cn/log n 只证明 o(n)，不能推出任何固定 c_0>0 的 l(n)<n^{1-c_0}，因为 (n/log n)/n^{1-c_0}=n^{c_0}/log n→∞。；若 CKS 猜想 l(n)≥n^{1-o(1)} 成立，则它会排除所有固定多项式节省。
- 第一阻塞点：要沿概率/容器上界路线得到 n^{1-c}，需要对所有大小 k=n^{1-c} 的强无和集合给出足够小的统一容器族；现有 n/log n 构造没有这种指数级计数控制。这是从亚线性节省升级到多项式节省时的第一处缺口。
- 下一步：固定一个候选坏集模型，先证明可检验的容器引理：每个 k 元强无和子集是否都被某个大小 O(k log n) 的“少子集和”容器覆盖，并估计容器总数；若计数不足以做并合界，该模型即可被否决。
- 来源核对：[Erdős Problems #790](https://www.erdosproblems.com/790)核对了 CKS 双边界、第一特问的肯定结论及 n^{1-o(1)} 猜想。
- 时间记账：所在批次墙钟时间按题数均摊约 91.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/790)；既有候选答案（按不可信材料审计）

### #791

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ be minimal such that there exists $A\subseteq \{0,\ldots,n\}$ of size $g(n)$ with $\{0,\ldots,n\}\subseteq A+A$. Estimate $g(n)$. In particular is it true that $g(n)\sim 2n^{1/2}$?
- 题意摘要：对每个整数 n，g(n) 是所有 A⊆{0,…,n} 中满足每个 x∈{0,…,n} 都可写成 x=a+a′（a,a′∈A，允许相等）的最小基数。问题要求估计 g(n)，尤其检验 g(n)∼2√n。
- 状态核对：整体常数问题仍开放，但“g(n)∼2√n”已被 Mrose 的构造否定；因此不能把该特例仍当作开放命题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先做无序和的计数下界，再用商余分解构造显式二阶加法基。取 m=⌈√n⌉，A={0,…,m−1}∪{0,m,2m,…,⌊n/m⌋m}。
- 局部结论：若 |A|=k，则不同无序对至多 k(k+1)/2 个，故 n+1≤k(k+1)/2，从而 g(n)≥√(2n)+O(1)。；任意 x≤n 可唯一写成 x=qm+r，其中 0≤r<m、qm≤n；上述 A 因而覆盖 [0,n]，且 |A|=m+⌊n/m⌋≤2√n+O(1)。；结合已核对的已知结果，目前有 (2.181…+o(1))n≤g(n)^2≤(3.458…+o(1))n；特别地，上界常数小于 4，严格否定 g(n)∼2√n。
- 第一阻塞点：初等计数只利用和的数量，没有利用 [0,n] 必须连续覆盖所造成的重叠与边界约束；无法由此逼近 2.181… 的下界，更不能证明极限常数存在。
- 下一步：把候选 A 按低端、中段、高端分块，计算各类无序和对覆盖区间时不可避免的重数，先尝试得到一个严格优于 k(k+1)/2≥n+1 的有限 n 线性规划不等式。
- 来源核对：官方页面仍标为开放，并记录 Yu/Kohonen 的界及 Mrose 对 2√n 猜想的否定：[Erdős Problem 791](https://www.erdosproblems.com/791)。；旧候选的两条初等推导可直接核验；其最佳常数部分只是文献汇总，不构成新证明。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/791)；既有候选答案（按不可信材料审计）

### #792

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that in any $A\subset \mathbb{Z}$ with $\lvert A\rvert=n$ there exists some sum-free subset $B\subseteq A$ with $\lvert B\rvert \geq f(n)$, so that there are no solutions to\[a+b=c\]with $a,b,c\in B$. Estimate $f(n)$.
- 题意摘要：令 α_sf(A)=max{|B|:B⊆A，且不存在 a,b,c∈B 满足 a+b=c}，其中变量可重复。则 f(n)=min_{A⊆Z, |A|=n} α_sf(A)。要求估计这一最坏情形保证值。
- 状态核对：线性主项已知：f(n)=(1/3+o(1))n；开放的是超过 n/3 的精细余项。旧候选据此宣布“正确渐近常数”为 1/3 没错，但没有解决页面保留的精细问题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：执行 Erdős 的随机圆法：均匀选 θ∈R/Z，令 Bθ={x∈A:{θx}∈(1/3,2/3)}。
- 局部结论：区间 I=(1/3,2/3) 在圆群中是 sum-free：若 u,v∈I，则 u+v mod 1∉I；故每个 Bθ 都是整数意义下的 sum-free 集。；对每个非零 x，{θx} 均匀分布，所以 E|Bθ|=|A∖{0}|/3；这独立推出 α_sf(A)≥⌈(n−1)/3⌉，已足以给出 f(n)≥n/3−O(1)。；结合 Eberhard–Green–Manners 构造的 f(n)≤n/3+o(n)，严格得到 f(n)=(1/3+o(1))n。
- 第一阻塞点：这一路线的一阶期望完全固定为约 n/3；要得到统一的 c log log n 增益，必须控制 θ↦|Bθ| 的正偏差或相应三角和的 L¹ 范数，单纯取期望无法闭合。另需注意 0 永远不能属于非空 sum-free 集，旧候选直接写 E|Bθ|=n/3 在 0∈A 时不正确。
- 下一步：对不含 0 的 A 计算 |Bθ| 的二阶矩，并在具体结构类（如元素互异模某个素数）中检验能否从方差推出正的加性增益；同时明确哪些结构会使二阶矩方法失效。
- 来源核对：官方页面记录当前精细夹逼 n/3+c log log n≤f(n)≤n/3+o(n)：[Erdős Problem 792](https://www.erdosproblems.com/792)。；已吸收旧候选在 0∈A 时的期望计数遗漏；这不影响一阶渐近，但影响其声称的逐 n 下界证明。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/792)；既有候选答案（按不可信材料审计）

### #793

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $F(n)$ be the maximum possible size of a subset $A\subseteq\{1,\ldots,n\}$ such that $a\nmid bc$ whenever $a,b,c\in A$ with $a\neq b$ and $a\neq c$. Is there a constant $C$ such that\[F(n)=\pi(n)+(C+o(1))n^{2/3}(\log n)^{-2}?\]
- 题意摘要：F(n) 是满足下述条件的 A⊆{1,…,n} 的最大基数：对任意 a,b,c∈A，只要 a≠b 且 a≠c（不要求 b≠c），就有 a∤bc。问题问是否存在常数 C，使 F(n)=π(n)+(C+o(1))n^{2/3}/(log n)^2。
- 状态核对：输入的 current_status='proved (Lean)' 与冻结题面、local_formal_statement 为空以及现行官方页面均冲突：页面仍标 OPEN 且明确“Formalised statement? No”。因此不能按“已证明”处理；这是一处状态元数据错误，而不是 Lean 已解决开放题。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：重建 Erdős 的图论上界。把每个非平方 m≤n 分解为 m=uv，使 u≤n^{2/3}，而 v≤n^{2/3} 或 v 是大于 n^{2/3} 的素数；以这些因子为顶点、m为边标签。
- 局部结论：所需分解存在：若 m 有大素因子 p>n^{2/3}，取 v=p；否则按素因子分组，可使两个乘积均≤n^{2/3}。；若三个不同标签 xy,yz,zw 构成一条三边路径，则 yz∣(xy)(zw)，违反 A 的条件；故所得简单边图不含 P4。；丢掉至多 ⌊√n⌋ 个平方标签以避免环，再用 Erdős–Gallai 的 ex(N,P4)≤N，可严格得到 F(n)≤π(n)+n^{2/3}+O(√n)。这重建了粗上界的核心机制，但没有得到二阶尺度的常数。
- 第一阻塞点：要把顶点集压缩到 π(n)+O(n^{2/3}/log²n)，必须精细选择小因子集合，并证明几乎所有 m∈A 都能注入相应边；粗分解使用了全部 [1,n^{2/3}]，损失正好过大。官方上下文中“无 P4 因而必为树”也不严格：无 P4 图可以是星森林或三角形；应使用 P4 极值定理。
- 下一步：对区间 [1,n^{2/3}] 按最小素因子分层，明确写出可删除的小顶点集合及无法表示的异常 m 数量，目标是验证异常项是否为 O(n^{2/3}/log²n)。
- 来源核对：现行页面明确仍为开放且未形式化：[Erdős Problem 793](https://www.erdosproblems.com/793)。；旧候选称问题仍开放与现行资料一致，但其依赖二手来源，且没有发现输入中“proved (Lean)”元数据矛盾。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/793)；既有候选答案（按不可信材料审计）

### #796

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ and let $g_k(n)$ be the largest possible size of $A\subseteq \{1,\ldots,n\}$ such that every $m$ has $<k$ solutions to $m=a_1a_2$ with $a_1<a_2\in A$. Is it true that\[g_3(n)=\frac{\log\log n}{\log n}n+(c+o(1))\frac{n}{(\log n)^2}\]for some constant $c$?
- 题意摘要：固定 k≥2，g_k(n) 是 A⊆{1,…,n} 的最大基数，使每个整数 m 至多有 k−1 个无序且两因子不同的表示 m=a₁a₂，其中 a₁<a₂ 且 a₁,a₂∈A。冻结题面问 k=3 时余项是否为 (c+o(1))n/(log n)^2。
- 状态核对：冻结题面含 log²，但现行官方页面已把主问题更正为余项 n/log n，并解释旧文中的 log² 很可能是重复排印错误。故对输入中的精确命题，答案是否定的；更正后的常数问题仍开放。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：审查旧候选的显式构造：取全部素数，并加入 pq≤n，其中 p≤√n<q 均为素数。按表示中因子是素数或此类半素数分类。
- 局部结论：若乘积含一个大素因子 Q，则可能的“素数×半素数”表示至多把另一个素因子与 Q 配对，最多两个；若两个因子都是半素数，则只有两种交叉配对。因此该 A 对 k=3 确实可行。；所加入的跨越 √n 的半素数数目等于半素数总数减去两个素因子均≤√n者；后者为 O(n/log²n)。结合半素数计数的二阶估计，得到 |A|=n log log n/log n+Ω(n/log n)。；由于 n/log n 不是 O(n/log²n)，冻结题面的展开式不可能成立。
- 第一阻塞点：该构造只给更正尺度 n/log n 的下界；它不能证明 g₃(n) 的 n/log n 系数收敛。旧候选进一步断言具体系数为 1+M，需要精确统一半素数计数约定及低阶项，当前筛查不采纳该未经完整推导的数值。
- 下一步：在同一计数约定下写出跨越 √n 的半素数数目的完整二项展开，并与 Erdős 上界中的常数逐项比较；检验上下界常数能否归结为同一个有限维优化问题。
- 来源核对：现行页面已更正题面为 n/log n，并详细说明 log² 版本疑为排印错误：[Erdős Problem 796](https://www.erdosproblems.com/796)。；旧候选的核心构造方向正确，但其“具体系数 1+M”没有在候选文本中充分核算，故只保留足以否定冻结命题的 Ω(n/log n) 结论。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/796)；既有候选答案（按不可信材料审计）

### #802

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that any $K_r$-free graph on $n$ vertices with average degree $t$ contains an independent set on\[\gg_r \frac{\log t}{t}n\]many vertices?
- 题意摘要：对每个固定 r（实质上 r≥3），是否存在仅依赖 r 的常数 c_r>0，使任意 n 顶点、平均度 t 的 K_r-free 图 G 都满足 α(G)≥c_r n log t/t；通常理解为 t 足够大，小 t 可调整常数处理。
- 状态核对：r=3 已知成立；固定 r≥4 仍开放。一般情形当前已知下界少一个 log log(t+1) 因子。
- 初步判定：`blocked`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试利用 K_r-free 蕴含每个邻域 G[N(v)] 为 K_{r−1}-free，并按度数 dyadically 分层；希望从许多邻域内的独立集拼出全局独立集。
- 局部结论：删去度数大于 2t 的顶点后仍保留至少 n/2 个顶点，且剩余图最大度≤2t；因此问题可先约化到有界最大度情形，只损失绝对常数。；对任意顶点 v，G[N(v)] 是 K_{r−1}-free；若在该邻域上使用归纳型下界，可找到大小约为 log d(v) 的独立集。；当 r=3 时每个邻域本身独立，已知 AKS 方法能把这种局部稀疏性放大为 α(G)≫n log t/t；对一般 r，Shearer 的已知方法达到 α(G)≫_r n log t/[t log log(t+1)]。
- 第一阻塞点：不同顶点邻域中选出的独立集高度重叠，而且它们之间可能有任意多交叉边；不能把约 n/t 个局部独立集直接并合。仅有“N(v) 为 K_{r−1}-free”也不能推出其色数有界，因此无法调用 Alon 的较强局部着色定理。这里正是缺失 log log 因子的第一处实质障碍。
- 下一步：在最大度≤2t 的约化后，选取一个距离至少 3 的顶点集，使其邻域互不相交；精确估计所得邻域总质量，并检验对各邻域随机抽取独立集后，跨邻域冲突图的平均度是否足够低以保留 log t 因子。
- 来源核对：官方页面确认 r=3 的 AKS 定理、Shearer 的一般下界及 r≥4 的开放状态：[Erdős Problem 802](https://www.erdosproblems.com/802)。；旧候选的状态总结正确，但只是文献摘要；本次路线明确定位了从局部 K_{r−1}-free 到全局独立集时无法闭合的拼接步骤。
- 时间记账：所在批次墙钟时间按题数均摊约 46.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/802)；既有候选答案（按不可信材料审计）

### #805

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For which functions $g(n)$ with $n>g(n)\geq (\log n)^2$ is there a graph on $n$ vertices in which every induced subgraph on $g(n)$ vertices contains a clique of size $\geq \log n$ and an independent set of size $\geq \log n$? In particular, is there such a graph for $g(n)=(\log n)^3$?
- 题意摘要：令 r_n=⌈log n⌉，并把 g(n) 取整。问题问：对哪些整数值函数 g，是否对每个充分大的 n 都存在一个 n 阶图 G_n，使每个恰有 g(n) 个顶点的集合 S 都满足 ω(G_n[S])≥r_n 且 α(G_n[S])≥r_n；特别问 g(n)≈(log n)^3。若性质在 g 个顶点上成立，则自动在所有至少 g 个顶点的集合上成立。
- 状态核对：截至当前官方页面仍为开放。已知某常数 c>0 下，g=c(log n)^3/loglog n 不可能；而存在性阈值至多为 2^{2^{(loglog n)^{1/2+o(1)}}}。先前候选对总体状态判断正确，但应说明“不可能”向更小 g 传播依赖上述单调性，而不是直接把单点定理写成任意渐近下界。[官方状态](https://www.erdosproblems.com/805)；[ABS21](https://arxiv.org/abs/2004.04718)
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：检验最自然的随机图 G(n,1/2) 路线。固定一个 g=(log_2 n)^3 元集合 S，并令 r=⌈log_2 n⌉。其中 r-团数 X 满足 E X=binom(g,r)2^{-binom(r,2)}，故 log_2 E X≤r log_2(eg/r)-r(r-1)/2=−(1/2+o(1))r^2。于是 P(X>0)≤E X→0；补图同分布，独立集亦然。
- 局部结论：随机图甚至对一个预先固定的 g-子集通常都没有所需的 r-团，因此不可能通过对所有子集作并合界得到 g=(log n)^3。；定义 m_n(r)=min_G min{m：每个至少 m 点的集合同时含 K_r 和独立 r-集} 后，原问题等价于 m_n(r_n)≤g(n)。；若已知在 g_0(n) 不存在这种图，则由单调性，对所有 g(n)≤g_0(n) 也不存在；ABS21 的构造则给出其阈值以上的存在性。
- 第一阻塞点：随机模型失败后，第一处缺口是构造一个高度非均匀、同时对 G 与补图都具有局部团结构的分布；独立边模型没有任何可调参数能克服固定子集中的团数期望趋零。
- 下一步：对 ABS21 的词典积构造做参数级复算：固定目标 m=(log n)^3，检查其递归“团规模翻倍”步骤在哪个不等式首次失效；这会把开放问题压缩为一个明确的递归参数优化任务。
- 来源核对：[Alon–Sudakov 原论文](https://arxiv.org/abs/0706.4099)确实研究 s=log^3 n、t=log n 的局部独立集条件。；[ABS21 摘要](https://arxiv.org/abs/2004.04718)明确给出双指数于 sqrt(loglog n) 的上界。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/805)；既有候选答案（按不可信材料审计）

### #809

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and define $F_k(n)$ to be the minimal $r$ such that there is a graph $G$ on $n$ vertices with $\lfloor n^2/4\rfloor+1$ many edges such that the edges can be $r$-coloured so that every subgraph isomorphic to $C_{2k+1}$ has no colour repeating on the edges. Is it true that\[F_k(n)\sim n^2/8?\]
- 题意摘要：固定 k≥3。F_k(n) 是在所有恰有 n 个顶点、⌊n²/4⌋+1 条边的图 G 中，使每个 C_{2k+1} 的全部 2k+1 条边颜色互异所需颜色数的最小值。问题要求对每个固定 k≥3，在 n→∞ 时是否 F_k(n)=(1/8+o(1))n²。
- 状态核对：输入的 2025 状态已经过时。Bucić–Chen–Ma 于 2026 年证明了所有 k≥4 的情形；k=3，即 C_7，仍未由该定理覆盖，所以完整的“所有 k≥3”陈述仍有一个开放例外。先前候选所称“所有 k≥3 均开放”已失效。[BCM26](https://arxiv.org/abs/2603.18952)
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：先作冲突图归约：以 E(G) 为顶点集，若 G 的两条边同处某个 C_{2k+1} 中，就在它们之间连边，所得冲突图记作 Q_k(G)。所求彩色条件严格等价于 Q_k(G) 的正常顶点着色，因此 F_k(n)=min_G χ(Q_k(G))。对 k≥4，重建 BCM26 主定理：其更强公式为 f(n,e,C_{2k+1})=e/2+(n/2)√(e−n²/4)+o(n²)。代入 e=⌊n²/4⌋+1，第二项为 O(n)，得到 n²/8+o(n²)。
- 局部结论：“至少 e 条边”和题目的“恰有 e 条边”版本可通过删边联系：删边不会产生新的非彩虹奇圈，因此两个极小化版本在这里没有实质差异。；BCM26 的一般公式代入临界边数立即给出 k≥4 的目标常数 1/8。；剩余问题精确缩减为 k=3 的 C_7 情形，而不是整个 k≥3 家族。
- 第一阻塞点：BCM26 的证明假设 k≥4；其结构归约需要足够长的奇圈来延伸路径，不能直接用于 C_7。当前无法严格证明 C_7 的冲突图必有 (1/8−o(1))n² 的色数，或构造相匹配的着色。
- 下一步：逐条检查 BCM26 中首次使用 k≥4 的路径延伸/稳定性引理，并针对 C_7 搜索最小反配置；可先计算小规模近 Turán 图的 Q_3(G)，检验预期极值结构是否仍成立。
- 来源核对：[Erdős Problems #809](https://www.erdosproblems.com/809)于 2026-04 更新为 k≥4 已解决。；[BCM26 原始预印本](https://arxiv.org/abs/2603.18952)的摘要明确写明 k≥4，并给出全边数区间公式；不能据此宣称 C_7 已解决。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/809)；既有候选答案（按不可信材料审计）

### #810

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does there exist some $\epsilon>0$ such that, for all sufficiently large $n$, there exists a graph $G$ on $n$ vertices with at least $\epsilon n^2$ many edges such that the edges can be coloured with $n$ colours so that every $C_4$ receives $4$ distinct colours?
- 题意摘要：问是否存在绝对常数 ε>0，使每个充分大的 n 都有一个 n 顶点、至少 εn² 边的图 G，以及一个至多 n 色的边着色，使 G 的每个 C_4 的四条边颜色两两不同。G 和着色均可依赖 n。
- 状态核对：截至 2026 年仍开放，原作者倾向答案为否。先前候选的结论正确，但把问题直接等同于通常要求正常边着色的 B-coloring 有额外假设，不能无条件采用。[官方状态](https://www.erdosproblems.com/810)
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：取 G 的一个至少保留一半边的二部子图，部为 A,B。固定 x,x'∈A，令 D=N(x)∩N(x')、d=|D|。若 d≥2，则由任取 y≠z∈D 得到 C_4=xyx' zx，彩虹条件迫使涉及 x,x' 与 D 的全部 2d 条边颜色两两不同。
- 局部结论：对每对左端点 x,x'，其共同邻居数若至少 2，则必有 2d≤n，因此 d≤n/2。；同色的任意两条边绝不能共同落在某个 C_4 中；问题等价于稠密图的 C_4-冲突图可否用 n 色正常着色。；把每条着色边 uv（颜色 c）编码为三元组 (u,v,c)，一个非彩虹 C_4 会产生四条三元超边，其并集至多含 7 个点，解释了与 (7,4) 问题的联系。
- 第一阻塞点：稠密二部图的平均共同邻居数只有 Θ(ε²n)，与局部上界 n/2 相容；上述二阶矩/共度计数因此不能推出矛盾。还缺少能同时利用许多顶点对之间颜色重用的全局不等式。
- 下一步：建立颜色类对共同邻居矩阵贡献的能量恒等式，尝试证明 n 个颜色在 Ω(n²) 条边上必产生一个同色边对共同属于 C_4；若只能得到线性超图情形，则精确记录线性化损失并与 g(n;7,4) 比较。
- 来源核对：[官方页](https://www.erdosproblems.com/810)记录：除完全二部图外的连通二部图已有更强否定结果，而 C_4 正是剩余例外。；同页记录 χ_S(n,cg(n;7,4),C_4)≤n，支持上述三元超图归约，但目前未知 g(n;7,4)=o(n²)。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/810)；既有候选答案（按不可信材料审计）

### #811

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Suppose $n\equiv 1\pmod{m}$. We say that an edge-colouring of $K_n$ using $m$ colours is balanced if every vertex sees exactly $\lfloor n/m\rfloor$ many edges of each colours. For which graphs $G$ is it true that, if $m=e(G)$, for all large $n\equiv 1\pmod{m}$, every balanced edge-colouring of $K_n$ with $m$ colours contains a rainbow copy of $G$? (That is, a subgraph isomorphic to $G$ where each edge receives a different colour.)
- 题意摘要：固定有限图 G，令 m=e(G)。对所有充分大的 n≡1 mod m，考察 K_n 的 m-边着色，要求每个顶点在每种颜色中度数都恰为 (n−1)/m。问题是分类哪些 G 在每个这样的平衡着色中都必有一份边色两两不同的 G。
- 状态核对：完整分类仍开放，但“所有图都成立”已被否定：K_4 不具该性质，且已有无限多个反例图。先前候选的森林论证基本可修复；其“已用顶点至多 m+1”在 G 含孤立点时错误，应改为固定常数 |V(G)|。[官方状态](https://www.erdosproblems.com/811)
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：对森林给出直接贪心证明。先嵌入各树分量的根，再按父子顺序处理其 m 条边，同时预先指定 m 个不同颜色。嵌入父顶点 x 后，目标颜色 c 在 x 处有 q=(n−1)/m 条边；至多 |V(G)|−1 条通向已占用顶点。当 q>|V(G)|−1 时可选未用邻点作为该子顶点。最后任意安置孤立点。
- 局部结论：上述论证严格证明每个固定森林 G 都具有该性质，包括带任意但固定数量孤立点的森林。；由 d_{C_4}(n)≤(1/4−c)n，而平衡四色着色每色最小度为 (n−1)/4，充分大时可推出 C_4 也具有该性质。；K_4 已有无限多个满足同余条件的平衡六色反例，故“所有 G”猜想为假；任意大反例 n 已足以否定“所有充分大 n”。
- 第一阻塞点：森林贪心依赖每加入一条边都引入新顶点；第一条回边出现时，目标颜色必须连接两个已嵌入顶点，平衡度数不给出该特定边的颜色。因此该路线在任何含圈图上立即中断。
- 下一步：以 C_6 为首个测试：先嵌入一条五边彩虹路径，再对其两个端点统计第六种颜色的闭合边；尝试通过对所有端点对双计数证明至少一个可闭合，或构造满足所有闭合边避色的平衡模板。
- 来源核对：[Erdős–Tuza 与后续结果汇总](https://www.erdosproblems.com/811)支持 C_4 的正例及 K_4 的反例。；官方页只陈述 Axenovich–Clemen 的特定无限族；未核得先前候选中较强的“most cliques”说法，故不采用该措辞。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/811)；既有候选答案（按不可信材料审计）

### #812

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that\[\frac{R(n+1)}{R(n)}\geq 1+c\]for some constant $c>0$, for all large $n$? Is it true that\[R(n+1)-R(n) \gg n^2?\]
- 题意摘要：这里 R(n)=r(n,n)。第一问量词为：是否存在与 n 无关的 c>0，使所有充分大的整数 n 都有 R(n+1)≥(1+c)R(n)。第二问的 ≫ 意为：是否存在 C>0、N，使每个 n≥N 都有 R(n+1)−R(n)≥Cn²。
- 状态核对：两问截至 2026 年仍开放。先前候选把已知差分下界推成 4n−4，是未经核实且与原文汇总、Lean 文件均冲突的错误；可靠记录是 4n−8，必须舍弃该递推论证。[官方状态](https://www.erdosproblems.com/812)
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 Δ_n=R(n+1)−R(n)。利用已知两步差分 R(n+2)−R(n)=Δ_n+Δ_{n+1}≫n^{2−o(1)}，得到每个充分大的 n 都有 max(Δ_n,Δ_{n+1})≫n^{2−o(1)}。另检验两问关系：若第一问成立，则 Δ_n≥cR(n)；结合经典指数级 Ramsey 下界，立即推出 Δ_n≫n²，所以第一问严格蕴含第二问。
- 局部结论：每两个相邻差分中至少一个达到 n^{2−o(1)} 量级；因此接近二次下界的“大跳跃”不能连续缺席两步。；固定乘法间隙若成立，会给出指数级差分，远强于第二问的二次差分。；形式化文件准确表达了 eventually 量词与渐近下界，并把已解决变体记录为 Δ_n≥4n−8。
- 第一阻塞点：两步估计只控制 Δ_n+Δ_{n+1}，没有机制排除质量在奇偶位置交替集中；从和的下界不能推出两个加数分别有二次下界。这是该路线的第一处严格缺口。
- 下一步：研究 BEFS 的差分注入论证能否与两步下界结合，建立相邻差分可比性，例如 Δ_{n+1}≤n^{o(1)}Δ_n；任何这样的局部平滑估计都会把两步结果转成单步进展。
- 来源核对：[Erdős Problems #812](https://www.erdosproblems.com/812)记录 Δ_n≥4n−8 及两步下界 ≫n^{2−o(1)}。；本地形式化文件 `812.lean` 同样将已解决下界写为 4n−8，没有支持候选答案的 4n−4。
- 时间记账：所在批次墙钟时间按题数均摊约 57.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/812)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/812.lean`；既有候选答案（按不可信材料审计）

### #813

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be minimal such that every graph on $n$ vertices where every set of $7$ vertices contains a triangle (a copy of $K_3$) must contain a clique on at least $h(n)$ vertices. Estimate $h(n)$ - in particular, do there exist constants $c_1,c_2>0$ such that\[n^{1/3+c_1}\ll h(n) \ll n^{1/2-c_2}?\]
- 题意摘要：定义 \[h(n)=\min\{\omega(G):|V(G)|=n，且每个7点集诱导的子图都含三角形\}.\] 问题要求估计其增长率，特别问是否存在固定的 \(c_1,c_2>0\)，使充分大 \(n\) 时 \(h(n)\) 分别严格高于 \(n^{1/3+c_1}\) 和严格低于 \(n^{1/2-c_2}\)（按幂指数意义）。令 \(H=\overline G\)，则等价为在所有满足“任意7点含独立3集”即 \(\alpha_7(H)\ge3\) 的 \(n\) 点图中最小化 \(\alpha(H)\)。
- 状态核对：仍为开放题。Bucić–Sudakov 已证明 \(h(n)\ge n^{5/12-o(1)}\)，故任取 \(c_1<1/12\) 均成立；是否有 \(c_2>0\) 仍未知。必须纠正先前候选答案：三角形自由图的补图路线借助 Ramsey 构造只给 \(O(\sqrt{n\log n})\)，不能称为 \(O(\sqrt n)\)，因而并未重建官方所述的经典 \(n^{1/2}\) 级上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：在补图 \(H\) 中作禁子图归约。局部条件等价于：\(H\) 不含任何7点、独立数至多2的子图。特别地，若 \(H\) 含一个 \(K_4\)，则其余顶点不能含与之不交的 \(K_3\)，否则这两个团的并只有两个团块，独立数至多2；故删去该 \(K_4\) 后图为三角形自由。由此把困难情形归约到 \(K_4\)-自由并同时禁掉所有7点独立数2图的情形，这正是 Bucić–Sudakov 的 Ramsey/邻域计数路线入口。
- 局部结论：补图变换严格给出 \(h(n)=\min\{\alpha(H):|H|=n,\alpha_7(H)\ge3\}\)。；若合格的 \(H\) 含 \(K_4\)，则 \(H-V(K_4)\) 三角形自由；于是该分支由三角形自由图的独立数下界直接给出至少 \(\Omega(\sqrt{n\log n})\) 量级，已强于所需的 \(n^{5/12-o(1)}\)。；因此寻找极小独立集的真正困难分支可以假设 \(H\) 为 \(K_4\)-自由，并禁掉例如 Bucić–Sudakov 使用的特定7点图 \(H_7\)。
- 第一阻塞点：第一处不能自行闭合的是：在 \(K_4,H_7\)-自由且 \(\alpha(H)<n^{5/12-o(1)}\) 的假设下，需要严格完成多层共同邻域、三角形匹配和独立集抽取的计数。简单的 Ramsey 或平均度估计到不了 \(5/12\)，更不能逼近 \(1/2\)。
- 下一步：逐条重建 Bucić–Sudakov 定理1.3中从 \(K_4,H_7\)-自由到 \(n^{5/12-o(1)}\) 的邻域分解，并单独测试其文中指出的 \(3/7\) 方法屏障究竟出现在哪个计数不等式。
- 来源核对：[Bucić–Sudakov 原论文](https://arxiv.org/abs/2007.03667)明确给出 \(\alpha_7(H)\ge3\Rightarrow\alpha(H)\ge n^{5/12-o(1)}\)，并把 \(n^{1/2-o(1)}\) 列为问题。；[Erdős Problem 813](https://www.erdosproblems.com/813)用于核对题目状态与官方界。
- 时间记账：所在批次墙钟时间按题数均摊约 62.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/813)；既有候选答案（按不可信材料审计）

### #817

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and define $g_k(n)$ to be the minimal $N$ such that $\{1,\ldots,N\}$ contains some $A$ of size $\lvert A\rvert=n$ such that\[\langle A\rangle = \left\{\sum_{a\in A}\epsilon_aa: \epsilon_a\in \{0,1\}\right\}\]contains no non-trivial $k$-term arithmetic progression. Estimate $g_k(n)$. In particular, is it true that\[g_3(n) \gg 3^n?\]
- 题意摘要：固定 \(k\ge3\)。\(g_k(n)\) 是最小的 \(N\)，使存在恰含 \(n\) 个不同正整数的 \(A\subseteq[1,N]\)，其全部子集和集合 \[H(A)=\{\sum_{a\in A}\epsilon_a a:\epsilon_a\in\{0,1\}\}\] 不含公差非零的 \(k\) 项等差数列。特别问是否存在绝对常数 \(c>0\)，使所有充分大 \(n\) 都有 \(g_3(n)\ge c3^n\)。
- 状态核对：仍开放。2026年新预印本把下界精确推进到中央三项式系数给出的 \((\sqrt3/(2\sqrt\pi)+o(1))3^n/\sqrt n\)，但明确说明能否去掉 \(\sqrt n\) 仍开放。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：走三元系数与集中性路线。若 \(A=\{a_i\}_{i=1}^n\)，则 \(H(A)\) 无非平凡3项等差数列，当且仅当所有 \(3^n\) 个 \(\sum_i\eta_i a_i\)、\(\eta_i\in\{0,1,2\}\)，两两不同。随后令独立随机变量 \(\varepsilon_i\) 均匀取 \(-1,0,1\)，研究 \(S=\sum_i\varepsilon_i a_i\)。上述等价性保证全部 \(S\) 值不同，而 \(\operatorname{Var}S=(2/3)\sum a_i^2\le(2/3)nN^2\)。
- 局部结论：等价性是严格的：3-AP 给出一个非零的 \([-2,2]\)-系数关系；反之，若该关系的三种子集和表示退化为相同整数，则已存在不同子集的等和关系，而消去交集后 \(0,t,2t\subset H(A)\) 又给出非平凡3-AP。；由 Chebyshev，至少 \(3/4\) 的 \(3^n\) 个互异整数 \(S\) 落在长度至多 \(4N\sqrt{2n/3}\) 的区间内，所以 \(N\ge c3^n/\sqrt n\)。；取 \(A=\{1,3,\ldots,3^{n-1}\}\)，利用无进位三进制逐位比较可得 \(H(A)\) 无非平凡3-AP，故 \(g_3(n)\le3^{n-1}\)。此外3-AP-free蕴含 \(k\)-AP-free，所以 \(g_k(n)\le g_3(n)\)。
- 第一阻塞点：集中性只把 \(3^n\) 个互异整数压入宽度 \(O(N\sqrt n)\) 的中央区间，因此必然留下 \(\sqrt n\) 损失。第一处无法闭合的是证明整数线性排列 \(\eta\mapsto\sum\\eta_i a_i\) 比一般三元网格的最优带宽多一个 \(\sqrt n\) 因子；新预印本也指出普通带宽法在现有下界处恰好耗尽。
- 下一步：对小维数建立整数线性布局的 ILP：最小化 \(\max_i a_i\)，约束所有 \(\{0,1,2\}^n\) 点积互异；比较其最优值与三元网格带宽 \(b_n\)，检验差值是否随 \(n\) 系统增长。
- 来源核对：[2026年预印本](https://arxiv.org/abs/2606.24139)证明精确有限下界 \(g_3(n)\ge (T_n-1)/2+\sum_{j<n}T_j\)，并确认常数因子问题仍开放。；本地 Lean 文件只形式化了 \(3^n=O(g_3(n))\) 这一待证命题；其定义与这里的量词一致。；[Erdős Problem 817](https://www.erdosproblems.com/817)记录原有 \(3^n/n^{O(1)}\) 下界。
- 时间记账：所在批次墙钟时间按题数均摊约 62.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/817)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/817.lean`；既有候选答案（按不可信材料审计）

### #819

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be maximal such that there exists $A\subseteq \{1,\ldots,N\}$ with $\lvert A\rvert=\lfloor N^{1/2}\rfloor$ such that $\lvert (A+A)\cap [1,N]\rvert=f(N)$. Estimate $f(N)$.
- 题意摘要：令 \(k=\lfloor\sqrt N\rfloor\)。在所有恰含 \(k\) 个元素的 \(A\subseteq[1,N]\) 中，最大化不超过 \(N\) 的不同二元和数目： \[f(N)=\max_{|A|=k}|(A+A)\cap[1,N]|,\] 其中允许 \(a+a\)。问题要求估计 \(f(N)\)。
- 状态核对：仍开放；已知 \((3/8-o(1))N\le f(N)\le(1/2+o(1))N\)。先前候选给出的循环 Sidon 构造思路可修正，但原文忽略了 \(\lfloor\sqrt N\rfloor\) 与 \(2q\) 的差异以及从特殊 \(N\) 推到任意 \(N\) 时补足元素的步骤。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：上界按无序对计数。下界取 \(M=q^2-1\) 及循环群 \(\mathbb Z_M\) 中大小 \(q\) 的 Bose–Chowla Sidon 集 \(B\)，选整数代表后考察 \(B\cup(B+M)\)。模 \(M\) 的 Sidon 性保证 \(B+B,(B+B)+M,(B+B)+2M\) 作为整数集合互不相交。平移到正整数，并取 \(N_0=4M\)，所有这些和均落在 \([1,N_0]\)。
- 局部结论：任意 \(A\) 的每个不同和至少对应一个无序可重复对，故 \(f(N)\le\binom{k+1}{2}=N/2+O(\sqrt N)\)。；在 \(N_0=4(q^2-1)\) 时，\(\lfloor\sqrt{N_0}\rfloor=2q-1\)。从上述 \(2q\) 元集合删去一个元素至多损失 \(2q\) 个不同和，仍留下 \(3\binom{q+1}{2}-O(q)=(3/8+o(1))N_0\) 个合格和。；对一般 \(N\)，取 \(q=(1-o(1))\sqrt N/2\) 且 \(4(q^2-1)\le N\)，嵌入该集合，再任意加入元素直至大小 \(\lfloor\sqrt N\rfloor\)；加入元素不会删去已有和，故得到 \((3/8-o(1))N\)。
- 第一阻塞点：该路线在 \(3/8\) 处闭合，但要逼近 \(1/2\)，需构造近 Sidon 的 \(\sqrt N\) 元集合，使几乎所有无序对既有不同和又满足和不超过 \(N\)。循环双层构造固有地只产生三个而非四个互不重叠的和层，因此首个结构性缺口正是第四层的碰撞/截断损失。
- 下一步：把问题写成准-Sidon优化：对缩放分布 \(a_i/N\) 同时统计碰撞能量和满足 \(a_i+a_j\le N\) 的对；先证明任何候选若达到 \((1/2-o(1))N\)，则碰撞对和超界对都必须是 \(o(N)\)，再与问题840的准-Sidon上界逐项比较。
- 来源核对：[Erdős–Freud 论文页面](https://www.sciencedirect.com/science/article/pii/0022314X9190083N)核对其研究对象是小于截断点的 Sidon 和数。；[Erdős Problem 819](https://www.erdosproblems.com/819)记录开放状态及 \(3/8,1/2\) 两端界。
- 时间记账：所在批次墙钟时间按题数均摊约 62.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/819)；既有候选答案（按不可信材料审计）

### #820

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $H(n)$ be the smallest integer $l$ such that there exist $k<l$ with $(k^n-1,l^n-1)=1$. Is it true that $H(n)=3$ infinitely often? (That is, $(2^n-1,3^n-1)=1$ infinitely often?) Estimate $H(n)$. Is it true that there exists some constant $c>0$ such that, for all $\epsilon>0$,\[H(n) > \exp(n^{(c-\epsilon)/\log\log n})\]for infinitely many $n$ and\[H(n) < \exp(n^{(c+\epsilon)/\log\log n})\]for all large enough $n$? Does a similar upper bound hold for the smallest $k$ such that $(k^n-1,2^n-1)=1$?
- 题意摘要：对每个正整数 \(n\)，\(H(n)\) 是最小的 \(l\)，使存在正整数 \(k<l\) 满足 \(\gcd(k^n-1,l^n-1)=1\)。问题包含三个量词命题：是否有无穷多个 \(n\) 满足 \(H(n)=3\)，即固定 \((k,l)=(2,3)\) 可行；是否存在同一个常数 \(c>0\) 给出所述极大阶的无限次下界和最终上界；以及固定底数2时最小可行 \(k\) 是否有类似最终上界。
- 状态核对：三部分均未解决。\(H(n)=3\) 的无穷性是 Ailon–Rudnick 猜想的 \((2,3)\) 特例。官方题页仍只记录无限多 \(n\) 上的 \(\exp(n^{c/\log\log n})\) 型下界草图，没有匹配的统一上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用 Fermat 素数障碍。令 \(P(n)=\{p:p\text{ 为素数且 }p-1\mid n\}\)。若 \(p\in P(n)\) 且 \(p\nmid a\)，则 Fermat 小定理给出 \(p\mid a^n-1\)。因此任何可行对 \(k<l\) 对每个 \(p\in P(n)\) 都必须满足 \(p\mid k\) 或 \(p\mid l\)。
- 局部结论：不同的 \(p\in P(n)\) 全部整除 \(kl\)，故 \(\prod_{p\in P(n)}p\mid kl<l^2\)，从而 \[H(n)>\Big(\prod_{p-1\mid n}p\Big)^{1/2}.\]；若能在无穷多个 \(n\) 上证明 \(|P(n)|\ge n^{c/\log\log n}\)，仅用 \(p\ge2\) 就推出 \(H(n)\ge\exp(Cn^{c/\log\log n})\)，常数可吸收到稍小的指数参数中。；固定2的变体中，每个奇素数 \(p\) 满足 \(p-1\mid n\) 时都整除 \(2^n-1\)，故可行的 \(k\) 必须被所有这些 \(p\) 整除。反向的粗构造 \(k=\operatorname{rad}(2^n-1)\) 确有 \(\gcd(k^n-1,2^n-1)=1\)，但只给 \(k\le2^n-1\)。
- 第一阻塞点：Fermat 障碍只给必要条件。第一处不能闭合的是反向选择较小的 \(k,l\)：即使把所有 \(p-1\mid n\) 的素数分配给 \(k\) 或 \(l\)，仍可能有大量阶整除 \(n\) 但 \(p-1\nmid n\) 的素数同时整除两项。现有论证无法把这些额外公因子统一排除，因而得不到猜测尺度的上界。
- 下一步：对给定 \(n\) 计算所有可能公因子素数的条件 \(\operatorname{ord}_p(k),\operatorname{ord}_p(l)\mid n\)，比较其集合与 \(P(n)\)；先检验“只处理 \(p-1\mid n\) 后随机分配素数给 \(k,l\)”是否在小规模上仍频繁留下额外公因子。
- 来源核对：[Erdős Problem 820](https://www.erdosproblems.com/820)截至2025年12月仍标为开放，并记录加强下界草图。；[Ailon–Rudnick 原论文](https://arxiv.org/abs/math/0202102)明确提出乘法独立整数情形的无穷次互素猜想。；[2026年关于该 gcd 序列的预印本](https://arxiv.org/abs/2606.07959)仍以 Ailon–Rudnick 问题为目标，只给结构归约，未宣称解决。
- 时间记账：所在批次墙钟时间按题数均摊约 62.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/820)；既有候选答案（按不可信材料审计）

### #821

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ count the number of $m$ such that $\phi(m)=n$. Is it true that, for every $\epsilon>0$, there exist infinitely many $n$ such that\[g(n) > n^{1-\epsilon}?\]
- 题意摘要：令 \[g(n)=|\{m\in\mathbb N:\varphi(m)=n\}|.\] 问题问：对每个固定 \(\epsilon>0\)，是否存在无穷多个正整数 \(n\) 使 \(g(n)>n^{1-\epsilon}\)。这里 \(n\) 是同一个欧拉函数值，计数变量是其全部原像 \(m\)。
- 状态核对：仍开放。已知无穷多个 \(n\) 满足 \(g(n)>n^{0.71568\ldots}\)，尚不能使指数任意接近1。先前候选答案只汇报状态，没有给出实际归约；这里补上光滑移位素数导致大纤维的具体计数入口。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：设 \(\mathcal P\) 是一批素数，且每个 \(p-1\) 的素因子都不超过 \(y\)。对子集 \(S\subseteq\mathcal P\) 定义平方自由数 \(m_S=\prod_{p\in S}p\)，则 \[\varphi(m_S)=\prod_{p\in S}(p-1).\] 把每个像编码为素数 \(q\le y\) 上的指数向量 \((v_q(\varphi(m_S)))_{q\le y}\)，再对映射 \(S\mapsto\varphi(m_S)\) 作抽屉计数。
- 局部结论：不同子集给出不同的 \(m_S\)，所以任一相同指数向量的纤维都直接产生同一个 totient 值的多个不同原像。；若指数向量的可能数为 \(V\)，则某个 \(n\) 严格满足 \(g(n)\ge2^{|\mathcal P|}/V\)。这把原问题归约为同时取得大量光滑移位素数和足够小的乘积向量空间。；若只用逐坐标范围 \(v_q\le |\mathcal P|\log x/\log q\) 的盒计数，则 \[V\le\prod_{q\\le y}\left(1+\frac{|\mathcal P|\log x}{\log q}\right).\] 该式是严格的，但过于粗糙，不能推出相对于所得 \(n\) 的 \(1-\epsilon\) 次幂下界。
- 第一阻塞点：第一处无法闭合的是把纤维大小 \(2^{|\mathcal P|}/V\) 与该纤维对应的具体值 \(n\) 比较到 \(n^{1-\\epsilon}\)。逐坐标盒计数丢失了 \(p-1\) 指数向量之间的整体乘积约束；恢复所需指数正是光滑移位素数分布和精细乘积碰撞估计的核心。
- 下一步：在假设存在 \(\gg_\epsilon x/\log x\) 个 \(p\le x\)、且 \(P^+(p-1)\le p^ \epsilon\) 的条件下，完整写出固定子集大小层上的纤维估计，验证其确实推出 \(g(n)>n^{1-O(\epsilon)}\)；随后定位无条件指数 \(0.71568\ldots\) 中每一处使用 \(0.2843\ldots\) 的位置。
- 来源核对：[Lichtman 原预印本](https://arxiv.org/abs/2211.09641)证明存在无穷多 \(p\) 使 \(p-1\) 无大于约 \(p^{0.2844}\) 的素因子。；[Erdős Problem 821](https://www.erdosproblems.com/821)记录由此得到的最佳 totient 重数指数 \(0.71568\ldots\) 及开放状态。
- 时间记账：所在批次墙钟时间按题数均摊约 62.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/821)；既有候选答案（按不可信材料审计）

### #824

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(x)$ count the number of integers $1\leq a<b<x$ such that $(a,b)=1$ and $\sigma(a)=\sigma(b)$, where $\sigma$ is the sum of divisors function. Is it true that $h(x)>x^{2-o(1)}$?
- 题意摘要：令 h(x) 为满足 1≤a<b<x、gcd(a,b)=1 且 σ(a)=σ(b) 的无序整数对数。问题问：是否存在 ε(x)→0，使所有充分大的 x 都有 h(x)>x^{2-ε(x)}。
- 状态核对：仍为开放题；已知 h(x)/x→∞，远弱于近二次下界。未采用候选答案中关于“典型 σ-值”的附加结论，因为它不是当前路线所需且未在给定材料中核实。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：从乘法公式构造碰撞。若 q 与 p=3q+2 都是素数，则 σ(2q)=3(q+1)=p+1=σ(p)，且 q>2 时 gcd(2q,p)=1。因此每个这样的 q 给出一对 (2q,3q+2)。尝试再把这一线性素数族扩展成多参数族，以获得大量独立碰撞。
- 局部结论：对每个满足 q、3q+2 均为素数的 q>2，(a,b)=(2q,3q+2) 是合法碰撞。；该一参数族即使按 Dickson 猜想有约 x/(log x)^2 个成员，也至多贡献 x^{1+o(1)} 对，数量级上不可能单独推出 x^{2-o(1)}。；已知结果仅保证 h(x)=x·L(x)，其中 L(x)→∞；不能从中推出任何固定的 x^{1+δ} 下界。
- 第一阻塞点：第一处未闭合步骤是证明 q 与 3q+2 同时为素数无穷多；这是未解决的二元线性素数问题。更根本地，即使补上该步骤，一参数构造仍只有近线性规模，无法达到目标。
- 下一步：系统搜索恒等式 σ(Au)=σ(Bv)，要求产生至少两个自由参数且自动保持 gcd(Au,Bv)=1；先对小的互素种子 A,B 枚举其素数线性因子条件，并严格计算所得参数族在盒中的维数。
- 来源核对：截至 2026-07-05，题目页仍标为 OPEN，并记录 Pollack–Pomerance 的 h(x)/x→∞：[Erdős Problems #824](https://www.erdosproblems.com/824)。；Pollack–Pomerance 论文书目信息及研究范围已核对：[Some Problems of Erdős on the Sum-of-Divisors Function](https://doi.org/10.1090/btran/10)。
- 时间记账：所在批次墙钟时间按题数均摊约 67.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/824)；既有候选答案（按不可信材料审计）

### #826

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many $n$ such that, for all $k\geq 1$,\[\tau(n+k)\ll k?\]
- 题意摘要：量词应读作：是否存在一个绝对常数 C>0，使集合 {n∈N: 对每个整数 k≥1，τ(n+k)≤Ck} 为无限集；C 不能依赖 n 或 k。
- 状态核对：仍开放。形式化文件确实把 ∃C 放在无限集量词之外。2026 年新增部分结果把右端推进到 k^C，但尚未得到线性 k。候选答案只谈 ω 版本，现已不完整。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先用初等除数界消去无限尾部，再把问题视为随 n 增长的有限联立筛问题：构造无限多个 n，使前 n−1 个移位分别满足 τ(n+k)≤Ck；尝试从最新的 k^C 构造中降低指数。
- 局部结论：对任意 n，若 k≥n，则 n+k≤2k，故 τ(n+k)≤2√(n+k)≤2√(2k)<3k。因而尾部可用统一常数 3 自动控制。；所以对固定 n，只需检查有限区间 1≤k<n；困难完全在于让同一个 C 对无限多个 n 有效。；单个最紧约束 k=1 并非障碍：取 n=p−1、p 为任意素数，则 τ(n+1)=2；真正问题是同时控制不断增长的移位集合。
- 第一阻塞点：现有有限维筛法不能用固定损失同时控制 k=1,2,…,n−1；普通平均值或并合界会随 n 损失，而所需 C 必须绝对。最新结果仍只给 τ(n+k)≪k^C，降到指数 1 的步骤未闭合。
- 下一步：逐引理检查 Lau 的 k^C 证明，定位指数 C 来自哪一项筛损失；首先检验该损失是否只作用于 k<n 的某个稀疏子集，以及能否借上述统一尾界把参数截断后降至 1。
- 来源核对：本地形式化陈述为 ∃C>0, {n | ∀k≥1, τ(n+k)≤Ck}.Infinite：[826.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/826.lean)。；截至 2026-07-02，题目仍标为 OPEN；页面记录 Lau 已证明 τ(n+k)≪k^C：[Erdős Problems #826](https://www.erdosproblems.com/826)。
- 时间记账：所在批次墙钟时间按题数均摊约 67.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/826)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/826.lean`；既有候选答案（按不可信材料审计）

### #827

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_k$ be minimal such that if $n_k$ points in $\mathbb{R}^2$ are in general position then there exists a subset of $k$ points such that all $\binom{k}{3}$ triples determine circles of different radii. Determine $n_k$.
- 题意摘要：按原始含义，“一般位置”至少指无三点共线、无四点共圆。n_k 是使任意 n_k 点都含有 k 点子集、且该子集所有三点组的有限外接圆半径两两不同的最小整数。若“一般位置”只表示无三点共线，则共圆点集立即使 k≥4 时 n_k 不存在。
- 状态核对：精确值及紧渐近仍开放。已确认 Erdős 的原 O(k^5) 最大集论证漏掉 R(ABX)=R(CDX) 型冲突，不能复述。候选答案称 O(k^5 log k) 为“最佳已发表界”缺少充分核对；下面独立给出更强的 O(k^5) 概率删点论证。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：把两个不同三点组具有相同半径称为冲突，按其并集大小 j=4,5,6 分类计数。随机以概率 p=n^{-4/5} 保留每点，再从每个残留冲突删去一点。
- 局部结论：无四点共圆蕴含 M4=O(n^3)：固定公共边和半径，至多有两个相应圆，每圆至多再含一个给定点集中的点。；固定点 a 和半径 ρ，以其余点为顶点、以 {b,c} 表示 R(abc)=ρ 的图最大度至多 2，故边数至多 n−1；从而 M5=O(n^4)。同理固定 ρ 的三点组数 tρ≤n(n−1)/3，故 M6≤∑ρ binom(tρ,2)<n^5/36。；取 p=n^{-4/5}，则期望保留点数为 n^{1/5}，期望冲突数至多 n^{-1/5}+1+n^{1/5}/36。逐冲突删点后仍可留下至少 (35/36)n^{1/5}−1−n^{-1/5} 个点。因此例如 n=(3k)^5 足以给出 k 点，故 n_k≤(3k)^5。
- 第一阻塞点：该路线只给上界，完全没有与 k^5 匹配的坏构型下界；目前第一处无法闭合的是构造一般位置点集，使每个显著大于 n^{1/5} 的子集都含等半径冲突。故不能由此“确定 n_k”。
- 下一步：把等半径冲突视为顶点数为 n、边大小 4至6 的超图，计算其可能的独立数下界是否可由局部度进一步提升；首项可检验任务是严格求 M6 的最大共度并试用局部引理或容器法改进 n^{1/5}。
- 来源核对：原论文明确把一般位置写为“无三点共线、无四点共圆”，并指出 Erdős 论证漏掉的冲突类型：[Martínez–Roldán-Pensado](https://arxiv.org/abs/1402.6276)。；截至 2026-06-24，题目仍为 OPEN；题目页现记录上述 O(k^5) 概率改进，但说明评论未经正式验证：[Erdős Problems #827](https://www.erdosproblems.com/827)。
- 时间记账：所在批次墙钟时间按题数均摊约 67.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/827)；既有候选答案（按不可信材料审计）

### #828

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for any $a\in\mathbb{Z}$, there are infinitely many $n$ such that\[\phi(n) \mid n+a?\]
- 题意摘要：量词是：对每个固定整数 a，集合 {n∈N_{>0}: φ(n) 整除整数 n+a} 都应为无限集；所选 n 可依赖 a，不要求一个统一序列同时服务所有 a。
- 状态核对：整体仍开放。候选答案从“2φ(n)=n+1 的无穷性困难”推断 a=1 的原问题困难，这不能作为严格归约，因为 φ(n)|n+1 还允许商大于 2；该逻辑缺口不予沿用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先建立可证明的负参数族，再研究 a=1 的保解递推。若 2φ(n)=n+1 且 p=n+2 为素数并且 p∤n，则令 N=np，尝试证明 N 仍满足商为 2。
- 局部结论：若 a=−m、φ(m)|m，且 p∤m 为素数，则 N=mp 满足 φ(N)=φ(m)(p−1) | m(p−1)=N−m=N+a；随 p 变化得到无限多解。特别覆盖 m=1 及满足 φ(m)|m 的偶 3-光滑数。；a=0 时 N=2^j 给出无限多解。；若 2φ(n)=n+1 且 n+2 为素数，则 φ(n(n+2))=φ(n)(n+1)=(n+1)^2/2，而 n(n+2)+1=(n+1)^2，故新数仍满足 2φ(N)=N+1。该递推严格产生 1,3,15,255,65535,…，但仅在每一步 n+2 为素数时继续。
- 第一阻塞点：无法证明递推中 n+2 出现无穷多个素数；而且即使该商为 2 的子族终止，也不能排除商 3、4、…产生无限多解。因此该路线既未证明 a=1，也未反证它。
- 下一步：对一般商 t=(n+a)/φ(n) 推导乘入新素数 p 后保持整除的完整同余条件，并计算哪些 (n,t,p) 转移无需假设单个巨大数为素数；先验证是否存在可迭代且由 Dirichlet 定理保证素数的算术级数转移。
- 来源核对：截至 2026-07-05，题目仍标为 OPEN，并注明为 Graham 猜想：[Erdős Problems #828](https://www.erdosproblems.com/828)。；本地形式化文件确认量词为 ∀a:ℤ, Set.Infinite {n:ℕ | φ(n)∣n+a}：[828.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/828.lean)。
- 时间记账：所在批次墙钟时间按题数均摊约 67.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/828)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/828.lean`；既有候选答案（按不可信材料审计）

### #829

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{N}$ be the set of cubes. Is it true that\[1_A\ast 1_A(n) \ll (\log n)^{O(1)}?\]
- 题意摘要：令 A={m^3:m∈N_{>0}}。卷积 r(n)=(1_A*1_A)(n) 是满足 c^3+d^3=n 的有序正整数对 (c,d) 数。问题问是否存在绝对常数 B、C，使所有充分大的 n 都有 r(n)≤C(log n)^B。
- 状态核对：仍开放。候选答案中的除数界可以独立核实，但它只给 n^{o(1)}，不能把“每个 ε 的 n^ε 界”误读成统一多对数界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：利用 c^3+d^3=(c+d)(c^2−cd+d^2)。令 s=c+d；对每个除数 s|n，把 d=s−c 代入并用二次方程及其判别式筛选可行 s，试图证明可行除数远少于 τ(n)。
- 局部结论：固定 s|n 后，c 满足 3c^2−3sc+s^2=n/s，因此至多有两个整数解；故 r(n)≤2τ(n)。；更精确地，判别式 Δ_s=12n/s−3s^2 必须是非负完全平方，且根还须满足正性与整除条件。因此 r(n) 不超过满足这一平方条件的除数数目的两倍。；由经典最大阶除数界 τ(n)=exp(O(log n/loglog n))=n^{o(1)}，得到 r(n)=n^{o(1)}；这仍显著弱于 (log n)^{O(1)}。
- 第一阻塞点：第一处无法闭合的是证明平方条件 Δ_s=□ 的可行除数 s 只有多对数个。直接用 τ(n) 不可能完成，因为 τ(n) 对高度合成数可超过任意固定对数幂；必须实质利用该判别式条件。
- 下一步：实现严格的“除数—判别式证书”枚举，对高度合成 n 和已知多表示两立方和的 n 统计可行 s；随后检验方程 4n=s(s^2+3y^2) 在 Eisenstein 整数分解中是否给出每个素因子的独立选择，明确哪类素因子真正增加表示数。
- 来源核对：截至 2026-07-04，题目仍标为 OPEN，并记录 Mahler、Stewart 的无穷多 n 下界：[Erdős Problems #829](https://www.erdosproblems.com/829)。；除数分解后每个 s 至多两个解的论证也可在近期论文中交叉核对：[Maynard, Sums of three positive cubes](https://doi.org/10.1112/jlms.70554)。；Stewart 的 11/13 下界来源已核对：[Cubic Thue Equations with Many Solutions](https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/rnn040.pdf)。
- 时间记账：所在批次墙钟时间按题数均摊约 67.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/829)；既有候选答案（按不可信材料审计）

### #830

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：We say that $a,b\in \mathbb{N}$ are an amicable pair if $\sigma(a)=\sigma(b)=a+b$. Are there infinitely many amicable pairs? If $A(x)$ counts the number of amicable $1\leq a\leq b\leq x$ then is it true that\[A(x)>x^{1-o(1)}?\]
- 题意摘要：对所有实数阈值 x，A(x) 计数满足 1≤a≤b≤x 且 σ(a)=σ(b)=a+b 的无序友爱数对。问题分别问：此类数对是否无限；以及是否存在 ε(x)→0，使充分大 x 有 A(x)>x^{1-ε(x)}。
- 状态核对：截至核验时官方页仍标为 open。候选答案没有证明。须纠正其中一处引文：官方记录的 Pomerance 后期上界指数为 (1/2+o(1))√(log x·log log x)，不是候选所写的 √(log x·log log log x)。此外，Pomerance 论文常计数“属于友爱对的整数”，与题目的完整数对计数不可无说明地混同。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：检验 Thābit 参数族。令 p=3·2^{n-1}-1，q=3·2^n-1，r=9·2^{2n-1}-1。若三者均为素数，则取 a=2^n pq、b=2^n r。
- 局部结论：由素因子互异及乘法性，σ(a)=(2^{n+1}-1)(p+1)(q+1)=(2^{n+1}-1)·9·2^{2n-1}。；同理 σ(b)=(2^{n+1}-1)(r+1)，而 r+1=9·2^{2n-1}；直接展开还得 p q+r=9·2^{n-1}(2^{n+1}-1)，故 σ(a)=σ(b)=a+b。；n=2 给出 p=5、q=11、r=71，从而得到 (220,284)。已知上界 x·exp(-o(log x)) 本身仍是 x^{1-o(1)} 量级，故不反驳所问下界。
- 第一阻塞点：要从该路线推出无限性，必须证明上述三个指数型表达式同时为素数的 n 有无穷多个；现有筛法不能闭合这一素性步骤。即使该子族无限，也还远不足以推出 A(x)>x^{1-o(1)}。
- 下一步：对该参数族先做可检验的局部筛查：逐素数 ℓ 求 n 模 ord_ℓ(2) 时 p、q、r 被 ℓ 整除的剩余类，判断是否存在覆盖同余障碍；若无，再量化到 n≤N 的同时素数频率并与 Bateman–Horn 型启发式比较。
- 来源核对：官方状态及上界已核对：https://www.erdosproblems.com/830；Pomerance 原文版本已定位：https://math.dartmouth.edu/~carlp/amicablesv3.pdf
- 时间记账：所在批次墙钟时间按题数均摊约 35.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/830)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/830.lean`；既有候选答案（按不可信材料审计）

### #831

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be maximal such that in any $n$ points in $\mathbb{R}^2$ (with no three on a line and no four on a circle) there are at least $h(n)$ many circles of different radii passing through three points. Estimate $h(n)$.
- 题意摘要：对每个满足无三点共线、无四点共圆的 n 点集 P，令 R(P) 为其三点所定外接圆半径的不同取值数；则 h(n)=min_{|P|=n}R(P)。要求估计 h(n)。
- 状态核对：官方页仍标为 open。候选答案的线性下界可以独立严格验证，但它只是下界，不能据此断言真实阶为 Θ(n)。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：固定半径 ρ，设 T_ρ 为外接半径等于 ρ 的三点组数；按“三角形—边”关联双计数，控制单一半径的重数。
- 局部结论：固定点对 {A,B} 与半径 ρ，圆心至多有两个选择；每个这样的圆因“无四点共圆”至多再含 P 中一个点。因此该点对属于至多两个半径为 ρ 的三角形。；故 3T_ρ≤2·C(n,2)，即 T_ρ≤(2/3)C(n,2)。；所有 C(n,3) 个三点组按半径分组，遂有 R(P)≥C(n,3)/((2/3)C(n,2))=(n-2)/2，因而 h(n)≥⌈(n-2)/2⌉。
- 第一阻塞点：该计数允许几乎每个点对对同一半径贡献两次，但这些局部极值能否在一个平面点集中同时实现没有得到控制；因此无法把单半径重数从 O(n²) 降至 o(n²)，也没有满足一般位置条件的 O(n) 半径构造。
- 下一步：把下一目标具体化为：证明或反驳存在绝对 δ>0，使每个固定 ρ 都有 T_ρ≤(2/3-δ)C(n,2)；先对 n≤10 的符号/数值一般位置构型枚举固定半径三角形的最大重数，寻找可加强的局部禁形。
- 来源核对：题目量词与开放状态已核对：https://www.erdosproblems.com/831
- 时间记账：所在批次墙钟时间按题数均摊约 35.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/831)；既有候选答案（按不可信材料审计）

### #836

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$ and $G$ be a $r$-uniform hypergraph with chromatic number $3$ (that is, there is a $3$-colouring of the vertices of $G$ such that no edge is monochromatic). Suppose any two edges of $G$ have a non-empty intersection. Must $G$ contain $O(r^2)$ many vertices? Must there be two edges which meet in $\gg r$ many vertices?
- 题意摘要：对每个 r≥2，G 是 r-一致、两两相交且 χ(G)=3 的超图；标准含义是存在恰当三染色但不存在二染色。问题一问是否总有 |V(G)|=O(r²)，问题二问是否必有不同边 E,F 满足 |E∩F|≥c r，其中 c>0 为绝对常数。
- 状态核对：第一问已有 Alon 反例，故是否定的；第二问仍开放，已知保证仅为 Ω(r/log r)。原题括号只解释了“可三染色”，但任意相交超图本来就可三染色，所以必须连同 χ=3 的“不可二染色”含义使用。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：独立重建 Alon 构造。取 |X|=2r-2；Y 对应 X 的无序等分 {A,X\A}。边包括所有 X 的 r-子集，以及每个 |A|=r-1 对应的 A∪{y_A}。
- 局部结论：两类边确实两两相交：两个 r-子集因 2r>|X| 相交；r-子集与 A 因 r+(r-1)>|X| 相交；若两个 (r-1)-集不交，它们互补并共享同一 y。；该超图不可二染色：为避免 X 内单色 r-集，X 的两个色类必须各为 r-1；对应这一等分的 y 无论取哪一色，都会使其中一个 A∪{y} 单色。另一方面平分着色 X、给 Y 第三色即为恰当三染色。；|V|=2r-2+(1/2)C(2r-2,r-1)=Θ(4^r/√r)，严格否定 O(r²)。此构造本身含有交为 r-1 的两条 r-子集边，因此不反驳第二问。
- 第一阻塞点：试图由“相交且不可二染色”直接推出线性交集时，只能调用 Erdős–Lovász 的 Ω(r/log r) 结论；把对数损失消除需要新的结构控制。Alon 构造没有揭示反例方向，因为它已有 r-1 大交。
- 下一步：在最小不可二染色子超图中，计算边迹族 {F∩E:F∈G}（固定 E）必须满足的覆盖条件；下一项明确任务是验证“若所有迹大小<c r，则随机二染色可扩张”的局部引理估计能否把现有 r/log r 改善哪怕到 r/(log r−log log r)。
- 来源核对：Alon 构造及 Ω(r/log r) 已核对：https://www.erdosproblems.com/836；原始论文书目信息及后续背景已核对：https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/LargeEdgeIntersection.html
- 时间记账：所在批次墙钟时间按题数均摊约 35.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/836)；既有候选答案（按不可信材料审计）

### #837

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ and $A_k\subseteq [0,1]$ be the set of $\alpha$ such that there exists some $\beta(\alpha)>\alpha$ with the property that, if $G_1,G_2,\ldots$ is a sequence of $k$-uniform hypergraphs with\[\liminf \frac{e(G_n)}{\binom{\lvert G_n\rvert}{k}} >\alpha\]then there exist subgraphs $H_n\subseteq G_n$ such that $\lvert H_n\rvert \to \infty$ and\[\liminf \frac{e(H_n)}{\binom{\lvert H_n\rvert}{k}} >\beta,\]and further that this property does not necessarily hold if $>\alpha$ is replaced by $\geq \alpha$. What is $A_3$?
- 题意摘要：对固定 k，α∈A_k 要同时满足：存在仅依赖 α 的 β>α，使每个全局密度 liminf>α 的 k-图序列都含顶点数趋于无穷、密度 liminf>β 的子图序列；但把前提严格不等号改为 liminf≥α 后，该结论允许失败。求 A_3。等价术语是“α 是 jump，但不是 strong jump”。
- 状态核对：精确 A_3 仍未知。候选答案关于 0 和 (0,2/9) 的结论与强跳理论相符，但“2/9 不 strong”需以其为遗传性质/Turán 密度边界来论证，不能仅称其为自然候选。另有 2026 年新结果：4/9 已被证明是 3-图 non-jump，故明确有 4/9∉A_3。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先处理可直接闭合的端点 α=0，再用 jump/strong-jump 分类缩小集合，并以最新的 4/9 非跳结果排除一个具体值。
- 局部结论：Erdős 的跳跃定理给出 0 是 3-图 jump：正的固定全局密度可强迫某个统一正密度增量；而在 ≥0 前提下取空 3-图序列，任何 β>0 都失败，故 0∈A_3。；已知每个 0<α<3!/3³=2/9 都是 strong jump，因此不满足第二条，故 A_3∩(0,2/9)=∅。；2/9 是非 strong-jump 边界，所以 2/9∈A_3 当且仅当 2/9 本身是 jump；这一点仍未解决。最新构造证明 4/9 是 non-jump，故 4/9∉A_3。
- 第一阻塞点：要判定某个非 strong-jump 的 α 是否属于 A_3，还必须另证它是 jump；遗传性质密度只处理第二条，不能提供第一条。特别是在 2/9 处，现有 Lagrangian/Turán 方法尚不能给出统一密度间隙。
- 下一步：针对 α=2/9，枚举小型 3-图 F 并严格计算其 Lagrangian；检验能否找到有限族 ℱ，使 π(ℱ)≤2/9 且每个 F∈ℱ 的 Lagrangian统一大于 2/9，从而满足 Frankl–Rödl 的有限证书型 jump 判据。
- 来源核对：官方定义与状态：https://www.erdosproblems.com/837；jump 定义及已知区间：https://arxiv.org/abs/1004.3733；strong jump 与遗传密度机制：https://arxiv.org/abs/1403.1220；2026 年 4/9 非跳结果：https://arxiv.org/abs/2605.13567
- 时间记账：所在批次墙钟时间按题数均摊约 35.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/837)；既有候选答案（按不可信材料审计）

### #838

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that any $n$ points in $\mathbb{R}^2$, with no three on a line, determine at least $f(n)$ different convex subsets. Estimate $f(n)$ - in particular, does there exist a constant $c$ such that\[\lim \frac{\log f(n)}{(\log n)^2}=c?\]
- 题意摘要：对一般位置 n 点集 P，F(P) 是所有处于凸位置的子集 Q⊆P 的数目，即 Q 的每一点都是 conv(Q) 的顶点；f(n)=min_{|P|=n}F(P)。问题问其增长，特别是 log f(n)/(log n)² 是否收敛到常数。
- 状态核对：官方仍标为 open，并记录 f(n)=exp(Θ((log n)²))。候选答案的双计数路线可验证；其中常数必须注明对数底。以下统一用 log₂。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：把 Erdős–Szekeres 数 ES(k)=2^{k+o(k)} 代入凸子集双计数。任取 m=⌊√n⌋，每个 m-点子集含 k=(1/2-o(1))log₂n 个凸位置点。
- 局部结论：计数二元组 (M,Q)，其中 |M|=m、Q⊆M 为凸 k-集。每个 M 至少贡献一个 Q，而固定 Q 至多属于 C(n-k,m-k) 个 M，故凸 k-集数至少为 C(n,m)/C(n-k,m-k)=∏_{i<k}(n-i)/(m-i)≥(n/m)^k。；取 m=√n 得 log₂f(n)≥(1/4-o(1))(log₂n)²；一般取 m=n^a 得常数 a(1-a)，在此单尺度路线中最大值正是 1/4。；由 ES(k)≥2^{k-2}+1，存在 n 点构型无大小超过 log₂n+O(1) 的凸子集；故 f(n)≤Σ_{j≤log₂n+O(1)}C(n,j)=2^{(1+o(1))(log₂n)²}。
- 第一阻塞点：上下常数仍为 1/4 与 1。双计数只使用“每个 m-子集至少含一个凸 k-集”，完全忽略这些见证之间的重叠结构；单尺度优化无法超过 1/4，也无法建立近似次乘法来证明极限存在。
- 下一步：检验多尺度双计数：取 n^{a_1}<⋯<n^{a_s} 的嵌套随机子集，记录同一凸 Q 被多少层重复见证；先对 s=2 推导精确熵优化式，判断是否能严格超过 1/4，或证明该类方法存在 1/4 屏障。
- 来源核对：官方状态与经典 Θ((log n)²) 界：https://www.erdosproblems.com/838；Suk 的 ES(k)=2^{k+o(k)} 定理：https://arxiv.org/abs/1604.08657
- 时间记账：所在批次墙钟时间按题数均摊约 35.5 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/838)；既有候选答案（按不可信材料审计）

### #839

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1\leq a_1<a_2<\cdots$ be a sequence of integers such that no $a_i$ is the sum of consecutive $a_j$ for $j<i$. Is it true that\[\limsup \frac{a_n}{n}=\infty?\]Or even\[\lim \frac{1}{\log x}\sum_{a_n<x}\frac{1}{a_n}=0?\]
- 题意摘要：设严格递增整数列 A={a_n}。对每个 i，不存在 1≤r≤s<i 使 a_i=∑_{j=r}^s a_j。问题问：(I) 是否所有这类 A 都满足 limsup_n a_n/n=∞；甚至 (II) 是否所有这类 A 都满足 (1/log x)∑_{a_n<x}1/a_n→0。
- 状态核对：截至核查日期仍为开放题。旧候选中的稠密分块构造不成立：若当前块首项为 m_k，则“前块某个后缀之和+m_k”可能正好是当前块中稍后的选中项，构成跨块连续和。另其所谓“素数具有正对数密度”也是错误的；素数的该归一化量约为 log log x/log x→0。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：反设 (I) 失败，即 a_n≤Cn 最终成立，等价地计数函数 A(x) 具有正的下渐近密度。先只使用长度为 2 的连续和 b_j=a_j+a_{j+1}，试图由 A 与这些和的互斥性推出密度矛盾。
- 局部结论：b_j 严格递增，且 {b_j}∩A=∅：若 b_j=a_i，则 b_j>a_{j+1}，故 i>j+1，恰为被禁止的连续和。；若 B={b_j}，则 B(x)≥A(x/2)-1，因此 A(x)+A(x/2)≤x+O(1)。所以正下密度 δ 必须满足 δ+δ/2≤1，即 δ≤2/3。；(II) 严格蕴含 (I)：若 A(t)≥δt 最终成立，则分部求和给出 ∑_{a<x}1/a=A(x)/x+∫_1^x A(t)t^{-2}dt≥δ log x+O(1)，不可能趋于零。
- 第一阻塞点：长度为 2 的和只排除一个与 A 不交的集合，所得 δ≤2/3 不矛盾。若同时加入不同长度的连续和，这些和集之间可能大量重合；目前没有可证明的重叠上界足以迫使 δ=0。
- 下一步：对 S_r={a_j+⋯+a_{j+r-1}} 先检验最小的非平凡情形 r=2,3：证明或反驳在 a_n≤Cn 假设下 |S_2∪S_3∩[1,x]|≥(c(C)+o(1))x，并量化等式 a_j+a_{j+1}=a_k+a_{k+1}+a_{k+2} 的重数。
- 来源核对：官方状态及 Freud 19/36 背景已核对：https://www.erdosproblems.com/839；独立检查了旧候选分块构造的跨块连续和漏洞。
- 时间记账：所在批次墙钟时间按题数均摊约 54.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/839)；既有候选答案（按不可信材料审计）

### #840

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be the size of the largest quasi-Sidon subset $A\subset\{1,\ldots,N\}$, where we say that $A$ is quasi-Sidon if\[\lvert A+A\rvert=(1+o(1))\binom{\lvert A\rvert}{2}.\]How does $f(N)$ grow?
- 题意摘要：对随 N→∞ 变化的集合族 A_N⊂[N]，若 |A_N+A_N|=(1+o(1))·binom(|A_N|,2)，称其渐近 quasi-Sidon；f(N) 是此类集合可达到的最大规模。问题要求确定 f(N) 的增长，尤其 √N 前的最佳常数。
- 状态核对：仍开放。已知 (2/√3+o(1))√N≤f(N)，Pikhurko 给出上界 (c_P+o(1))√N，其中 c_P=(1/4+1/(π+2)^2)^(-1/2)=1.863…；常数缺口未闭合。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建 Erdős–Freud 的反射 Sidon 下界，并以和的三个区间逐类计数；同时检查最朴素的容积上界。
- 局部结论：取强 Sidon 集 B⊂[1,N/3]，|B|=m=(1+o(1))√(N/3)，令 A=B∪(N−B)，则 |A|=2m=(2/√3+o(1))√N。；B+B、N+(B−B)、2N−(B+B) 位于依次分离的区间。Sidon 性给出前后两类各 m(m+1)/2 个和，中间差分类有 m(m−1)+1 个值，故 |A+A|=2m²+1=(1+o(1))binom(2m,2)。下界构造因而严格成立。；仅由 A+A⊂[2,2N] 可得 (1+o(1))|A|²/2≤2N，从而 |A|≤(2+o(1))√N；这重建了基础上界，但达不到 Pikhurko 常数。
- 第一阻塞点：改进常数必须利用和在 [2,2N] 中的非均匀分布以及加法能量约束；单纯的值域计数在常数 2 处已经饱和，无法推出 1.863，更不能确定真正常数。
- 下一步：把 A 按位置切成 q 个等长区间，建立各块间不同和的二次规划；先对 q=2,3 精确求最优值，并核验其连续极限能否复现 Pikhurko 的 (π+2) 常数。
- 来源核对：官方已知界：https://www.erdosproblems.com/840；Pikhurko 原论文定理 3：https://opikhurko.warwick.ac.uk/E/Pikhurko06dm.pdf
- 时间记账：所在批次墙钟时间按题数均摊约 54.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/840)；既有候选答案（按不可信材料审计）

### #846

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{R}^2$ be an infinite set for which there exists some $\epsilon>0$ such that in any subset of $A$ of size $n$ there are always at least $\epsilon n$ with no three on a line. Is it true that $A$ is the union of a finite number of sets where no three are on a line?
- 题意摘要：存在固定 ε>0，使 A⊂R² 的每个有限子集 B 都含有 |C|≥ε|B| 的子集 C，且 C 中无三个不同点共线。问题问是否必存在固定有限数 r，使 A 可分成 r 个无三点共线的集合。
- 状态核对：结论为假，且已有 Lean 验证。旧候选称其开放，已被新状态和正式反例推翻。本地文件仍显示 `sorry`，但指向含完整证明的固定提交；因此本地快照本身不能作为可重放证明对象。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建无限完全图 K_∞ 的几何编码。选择增长足够快（或满足相应代数独立条件）的实数 x_i；对每条边 {i,j} 放置点 p_ij=(x_i+x_j, x_i²+x_ix_j+x_j²)，选择参数以保证三个编码点共线当且仅当对应三条边组成三角形。
- 局部结论：若 {i,j},{j,k},{k,i} 构成三角形，令 T=x_i+x_j+x_k、P=x_ix_j+x_jx_k+x_kx_i，则三个点均满足 y=Tx−P，故必共线；快速增长参数排除了其他边型造成的偶然共线。；任取 n 个编码点，对应一个有 n 条边的有限图。随机二分顶点所得割的期望边数为 n/2，故存在至少 n/2 条边的二分子图；二分图无三角形，相应点集中无三点共线。因此假设以 ε=1/2 成立。；若这些点可由 r 个无三点共线集覆盖，给每条边选一个包含其编码点的颜色，便得到 K_∞ 的有限边着色且无单色三角形；无限 Ramsey 定理给出单色三角形，矛盾。
- 第一阻塞点：无；关键的“仅三角形产生共线”需通过参数的递归快速增长来避免有限多个非零行列式方程，这正是正式证明中闭合的退化排除步骤。
- 下一步：若需机器级复核，应检出官方标注的提交 2404258180688283e5141021c75464dc2acfb798，并在 Lean 4.22 环境编译，而不能编译当前含 `sorry` 的本地快照后声称完成验证。
- 来源核对：官方反例状态、构造摘要及 Lean 提交链接：https://www.erdosproblems.com/forum/thread/846；官方问题页：https://www.erdosproblems.com/846；已检查本地 FormalConjectures/ErdosProblems/846.lean，确认当前文件仅为带 `sorry` 的陈述快照。
- 时间记账：所在批次墙钟时间按题数均摊约 54.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/846)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/846.lean`；既有候选答案（按不可信材料审计）

### #847

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{N}$ be an infinite set for which there exists some $\epsilon>0$ such that in any subset of $A$ of size $n$ there is a subset of size at least $\epsilon n$ which contains no three-term arithmetic progression. Is it true that $A$ is the union of a finite number of sets which contain no three-term arithmetic progression?
- 题意摘要：存在固定 ε>0，使无限集 A⊂N 的每个有限子集 B 都含有 |C|≥ε|B| 的无非平凡三项等差数列子集。问题问 A 是否必能由有限多个无三项等差数列集覆盖，等价于其三项等差超图是否有限可着色。
- 状态核对：结论为假。Reiher–Rödl–Sales 已给出反例。旧候选的核心论证正确；论文的强形式允许 k=3 时 μ<2/3，而官方页和本地 Lean 注释只陈述了足够使用的较弱范围 μ<1/2，二者不影响反例。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：直接把 RRS24 的构造解释为三均匀超图：顶点为 X⊂N，边为 X 内的非平凡三项等差数列。用其“μ-fractional property”和对任意有限着色的 van der Waerden 性质分别核对假设与否定结论。
- 局部结论：取任意固定 0<μ<1/2。RRS24 给出 X，使每个有限 Y⊂X 都有 |Z|≥μ|Y| 且 Z 无三项等差数列，所以原假设成立，可取 ε=μ。；同一 X 的任意有限着色均含单色三项等差数列，因此其三项等差超图的色数为无穷。；若 X=⋃_{i=1}^r X_i 且各 X_i 无三项等差数列，给每个元素选择一个包含它的 X_i 作为颜色，就得到无单色三项等差数列的 r-着色，与上一条矛盾。
- 第一阻塞点：无；结论直接由已发表定理推出。需注意覆盖集不必互不相交，但“为每点选择一个所属颜色”即可把覆盖转成着色。
- 下一步：形式核验时应补齐本地 847.lean 中仍为 `sorry` 的定理，并统一注释中的 μ<1/2 与论文强范围 μ<2/3；数学否定结论本身不依赖这一区别。
- 来源核对：RRS24 期刊论文及定理摘要：https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12987；官方状态：https://www.erdosproblems.com/847；已核对本地 847.lean 的量词、覆盖形式及 `sorry` 状态。
- 时间记账：所在批次墙钟时间按题数均摊约 54.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/847)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/847.lean`；既有候选答案（按不可信材料审计）

### #849

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for every integer $t\geq 1$, there is some integer $a$ such that\[\binom{n}{k}=a\](with $1\leq k\leq n/2$) has exactly $t$ solutions?
- 题意摘要：定义 M(a)=#{(n,k)∈N²:1≤k≤n/2 且 binom(n,k)=a}。问题问对每个整数 t≥1，是否存在整数 a 使 M(a)=t。由于固定 n 时 binom(n,k) 在 1≤k≤n/2 上严格递增，本地 Lean 只计数满足“存在 k”的 n 与原题计数 (n,k) 等价。
- 状态核对：仍开放，且普遍猜测答案为否；没有已知 M(a)≥5 的例子。旧候选对 t≤4 的例子可独立核实，但不能外推到任意 t。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：沿“小重数完全分类”路线，逐一验证 a=2,6,120,3003，并利用每条固定 k 列的单调性及中央二项式下界排除遗漏。
- 局部结论：M(2)=1；M(6)=2，对应 (6,1),(4,2)。对 k≥3，最小允许值 binom(6,3)=20，故无遗漏。；M(120)=3，对应 (120,1),(16,2),(10,3)。k=4 时 binom(8,4)=70<120<126=binom(9,4)，而 k≥5 时 binom(2k,k)≥252，故恰为三个。；M(3003)=4，对应 (3003,1),(78,2),(15,5),(14,6)。k=3,4 分别由相邻值夹住；k≥7 时 binom(2k,k)≥binom(14,7)=3432，故恰为四个。
- 第一阻塞点：要得到 t=5，必须让至少五条不同的 k-列在同一整数相交；固定两列的相等式已是高亏格或稀疏丢番图问题，现有单调性只说明每列至多贡献一次，不能制造第五次碰撞，也不能证明绝对上界。
- 下一步：建立经认证的碰撞图：在明确界限 n≤N_0 内枚举 binom(n,k)，记录同值的不同 k，并重点搜索由 k=1,2 与三条内部列组成的五重碰撞；同时输出完整哈希证书，使“界内无 t=5”成为可独立检验的有限结论。
- 来源核对：官方状态与 t≤4、内部区域定理背景：https://www.erdosproblems.com/849；已核对本地 849.lean；注意其按 n 计数，但由半三角中的严格单调性与原题等价。
- 时间记账：所在批次墙钟时间按题数均摊约 54.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/849)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/849.lean`；既有候选答案（按不可信材料审计）

### #850

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Can there exist two distinct integers $x$ and $y$ such that $x,y$ have the same prime factors, $x+1,y+1$ have the same prime factors, and $x+2,y+2$ also have the same prime factors?
- 题意摘要：按官方语境，量词应解释为：是否存在不同的正整数 x,y，使得对 j=0,1,2，x+j 与 y+j 的素因子集合完全相同，即 rad(x+j)=rad(y+j)。先前候选的 (-4,2) 只利用了题面未明说正性；人工评审已指出官方有意让读者从语境推断正整数，因此它不是本问题的反例。
- 状态核对：截至核查时仍为开放问题；官方还记录了强 Baker-ABC 假设下不存在这种正整数对。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：设 y>x、D=y-x，并记 R_j=rad(x+j)=rad(y+j)。尝试把条件归约为三个相邻的 S-unit 条件，再用根基乘积的下界逼迫 D 过大。
- 局部结论：对每个 j∈{0,1,2}，任意 p|R_j 同时整除 x+j 和 y+j，故 p|D；因此 lcm(R_0,R_1,R_2)|D。；R_1 与 R_0,R_2 均互素，而 gcd(R_0,R_2)∈{1,2}，所以 R_0R_1R_2/gcd(R_0,R_2) 整除 D，特别地不超过 D。；三组素数支撑除可能公共素数 2 外互不相交；同时 y,y+1,y+2 分别也是对应支撑上的 S-unit。这把问题归约为三个彼此耦合的 S-unit 方程。
- 第一阻塞点：路线首次失闭于所需的不等式：无条件下无法证明 rad(x)rad(x+1)rad(x+2)/gcd(rad(x),rad(x+2))>y-x。相邻整数可能具有很小的根基；正是强 ABC 型输入才可排除这种长期异常。
- 下一步：固定 D，利用 R_j|D 枚举 D 的三个近乎互斥素数子集，并把 (x,x+1,x+2) 写成相应 S-unit；先对给定 ω(D) 建立可计算的 S-unit 上界，检查能否排除所有小 ω(D) 情形。
- 来源核对：官方页面仍标为 OPEN，并明确给出强 Baker-ABC 下的否定结果：[Erdős Problem 850](https://www.erdosproblems.com/850)。；已明确吸收人工评审：不采用负整数候选反例。
- 时间记账：所在批次墙钟时间按题数均摊约 50.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/850)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/850.lean`；既有候选答案（按不可信材料审计）

### #851

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$. Is there some $r\ll_\epsilon 1$ such that the density of integers of the form $2^k+n$, where $k\geq 0$ and $n$ has at most $r$ prime divisors, is at least $1-\epsilon$?
- 题意摘要：对每个 ε>0，须存在只依赖 ε 的整数 r，使集合 A_r={N∈N:∃k≥0, N=2^k+m 且 ω(m)≤r} 具有自然密度 d≥1-ε。这里 ω 是不同素因子的个数；r 不得依赖密度截断 X。
- 状态核对：已获肯定解决；先前候选把它称为开放题已经过时。官方页面现记录 Price 的筛法证明，并记录 Green–Sawhney 的高矩版本给出 r≪log(1/ε)/loglog(1/ε)。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建二矩筛法。给定大 X，取固定参数 z,t；只计数 m=N-2^k 中不被任何 z≤p≤X^(1/t) 的素数整除者，定义其表示数 R_X(N)。用筛法基本引理估计 R_X 的一、二阶矩，再由 Chebyshev 不等式控制 R_X(N)=0 的比例。
- 局部结论：这种筛剩的 m≤X 的素因子要么小于 z，要么大于 X^(1/t)，故 ω(m)≤π(z)+t；因此可取 r=π(z)+t，与 X 无关。；Mertens 乘积给出每个 k 的筛剩概率约 ∏_{z≤p≤X^(1/t)}(1-1/p)≈t log z/log X；约 log_2 X 个 k 相加，平均表示数 λ量级为 t log z。；若基本引理及非对角奇异级数平均能给出 Var(R_X)≪λ+o(λ²)，则 Chebyshev 立即给出无表示者比例≪1/λ+o(1)；依次增大 t,z 即可使其小于 ε。
- 第一阻塞点：在这次受限重建中，第一处尚未逐项闭合的是非对角二阶矩：需证明由 p|(2^k-2^l)、即 ord_p(2)|(k-l) 产生的奇异乘积在 k≠l 上平均为 1+o(1)。官方讨论称这由控制小乘法阶素数完成，但完整引理及误差常数未在输入中给出。
- 下一步：逐行核对 Price 证明中关于 ord_p(2) 的平均奇异级数引理，并确认其误差对先取 z,t、后令 X→∞ 的量词次序一致；这是把本重建升级为完整证明的唯一关键检查。
- 来源核对：官方页面明确标为 PROVED，并概述证明及定量改进：[Erdős Problem 851](https://www.erdosproblems.com/851)。；官方讨论给出二矩证明的筛区间、方差目标及乘法阶障碍：[851 discussion](https://www.erdosproblems.com/forum/thread/851)。；形式化页面确认对象采用 primeFactors.card，即不同素因子数：[Formal Conjectures 851](https://google-deepmind.github.io/formal-conjectures/FormalConjectures/ErdosProblems/851.html)。
- 时间记账：所在批次墙钟时间按题数均摊约 50.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/851)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/851.lean`；既有候选答案（按不可信材料审计）

### #852

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d_n=p_{n+1}-p_n$, where $p_n$ is the $n$th prime. Let $h(x)$ be maximal such that for some $n<x$ the numbers $d_n,d_{n+1},\ldots,d_{n+h(x)-1}$ are all distinct. Estimate $h(x)$. In particular, is it true that\[h(x) >(\log x)^c\]for some constant $c>0$, and\[h(x)=o(\log x)?\]
- 题意摘要：对实数 x（实质取整数部分），h(x) 是所有起点 n<x 中，使连续间隙 d_n,…,d_{n+h-1} 两两不同的最大长度。问题要求估计其增长，特别询问是否存在固定 c>0 使最终 h(x)>(log x)^c，以及是否 h(x)=o(log x)。
- 状态核对：仍开放；官方只确认 Brun 筛推出 h(x)→∞。先前候选的 h(x)≈C log x 是生日悖论启发，不是证明，尤其不能据此否定 o(log x)。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：尝试把存在长无重复块转成对短距离等间隙碰撞的计数问题。将前 N 个间隙分成互不相交的长度 m 块；若没有长度 m 的无重复块，则每块都贡献一对相等间隙。
- 局部结论：若 h(N)<m，则至少存在 floor(N/m) 对指标 (i,j)，满足 1≤j-i<m 且 d_i=d_j；可从互不相交的 m-块各选一对，故这些对互异。；因此，只要能证明短程碰撞数 C_m(N)=#{(i,j):i≤N,0<j-i<m,d_i=d_j}<floor(N/m)，便严格推出 h(N)≥m。；对固定 m，官方所述 Brun 筛结果足以导出某处存在长度 m 的无重复块，从而 h(x)→∞；但该结论没有给出随 x 的有效多对数速率。
- 第一阻塞点：当 m 随 N 增长时，需要对 d_i=d_j、j-i<m 的四素数相关式作一致上界，同时还要保留“相邻素数”条件。现有固定维 Brun 筛的常数随 m 恶化，无法证明 C_m(N)=o(N/m) 于 m=(log N)^c。
- 下一步：先做最小的定量目标：从一份明确的 Brun 上界追踪维数依赖，求出该碰撞法能无条件支持的最大 m=m(N)；即使只得到 logloglog N 级别，也会是可验证的改进。
- 来源核对：官方页面确认开放状态、精确量词及唯一列出的结论 h(x)→∞：[Erdős Problem 852](https://www.erdosproblems.com/852)。
- 时间记账：所在批次墙钟时间按题数均摊约 50.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/852)；既有候选答案（按不可信材料审计）

### #853

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d_n=p_{n+1}-p_n$, where $p_n$ is the $n$th prime. Let $r(x)$ be the smallest even integer $t$ such that $d_n=t$ has no solutions for $n\leq x$. Is it true that $r(x)\to \infty$? Or even $r(x)/\log x \to \infty$?
- 题意摘要：r(x) 是在前 x 个素数间隙 d_1,…,d_⌊x⌋ 中没有出现的最小正偶数。第一问是 r(x)→∞；第二问要求更强的 r(x)/log x→∞。
- 状态核对：两问仍开放。先前候选关于 (log x)^2 的说法仅为首次出现启发式，不能当作局部定理。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：先作精确逻辑归约，再尝试用 Hardy–Littlewood 型素数组计数固定偶数 t 的连续素数间隙：计数 p,p+t 为素数，并以有限容斥排除 p+1,…,p+t-1 中的素数。
- 局部结论：r(x) 单调不减，且 r(x)>T 当且仅当前 x 个间隙已经包含每个不超过 T 的正偶数。；所以 r(x)→∞ 等价于：每个固定正偶数 t 至少一次成为连续素数之差；这比要求每个 t 出现无穷多次的 Polignac 猜想弱。；r(x)/log x→∞ 等价于：对每个固定 A>0，充分大 x 时，每个偶数 t≤A log x 都已在 n≤x 处出现；这揭示了第二问所需的是对增长中的 t 的一致首次出现估计。
- 第一阻塞点：固定 t 的容斥需要足够强的 Hardy–Littlewood 素数多元组渐近；无条件筛法有奇偶障碍，甚至不能对任意指定 t 保证一次连续素数间隙。第二问还要求该渐近对 t≤A log x 一致，障碍更强。
- 下一步：在定量 Hardy–Littlewood 假设下完整执行固定 t 的有限容斥，并明确所需的一致误差；随后检查该误差是否足以同时覆盖所有 t≤A log x。
- 来源核对：官方页面截至核查仍标为 OPEN，且强调 t 必须为偶数：[Erdős Problem 853](https://www.erdosproblems.com/853)。
- 时间记账：所在批次墙钟时间按题数均摊约 50.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/853)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/853.lean`；既有候选答案（按不可信材料审计）

### #854

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_k$ denote the $k$th primorial, i.e. the product of the first $k$ primes. If $1=a_1<a_2<\cdots a_{\phi(n_k)}=n_k-1$ is the sequence of integers coprime to $n_k$, then estimate the smallest even integer not of the form $a_{i+1}-a_i$. Are there\[\gg \max_i (a_{i+1}-a_i)\]many even integers of the form $a_{j+1}-a_j$?
- 题意摘要：令 P_k=∏_{i≤k}p_i，按大小排列区间 [1,P_k-1] 中与 P_k 互素的整数 a_i。记 D_k={a_{i+1}-a_i} 为不同的内部连续间隙值，M_k=max D_k。第一问估计最小缺失正偶数 m_k=min(2N\D_k)；第二问自然解释为是否 |D_k|≫M_k，即出现的不同偶间隙值有正比例于最大间隙那么多。
- 状态核对：仍开放。必须区分连续间隙 a_{i+1}-a_i 与任意差 a_j-a_i；后者的论证不回答本题。先前候选引用的精确 Ziller 界未由输入或官方页面验证，因此本筛查不把它当作已知定理。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：使用 primorial wheel 的递推。由 P_k 升到 qP_k（q=p_{k+1}）时，把每个旧剩余类复制到 q 个区块，再删去其中唯一被 q 整除的复制；研究旧间隙的保留以及删除点造成的相邻间隙合并。
- 局部结论：设 a<b 是模 P_k 的一个内部连续互素对。它的 q 个平移复制中，至多一个复制删去左端、至多一个删去右端；故至少 q-2 个复制两端均保留，且中间不会插入新互素数。因此 D_k⊆D_{k+1}。；由此 m_k 单调不减，且 |D_k| 单调不减。这是对第一缺失值和不同间隙数的严格结构性约束。；新层出现但旧层没有的间隙，只能由删除 q 的倍数把若干相邻旧 wheel 间隙合并而成；因此第二问可归约为控制这些连续和产生了多少不同值以及最大值增长多快。
- 第一阻塞点：递推只保证旧间隙保留，却没有给出新增不同值的数量与新最大间隙 M_{k+1} 的可比控制；合并可能制造很大的 M_{k+1} 而只增加少量不同值。因此无法从 D_k⊆D_{k+1} 推出 |D_k|≫M_k，也不能估计 m_k 的量级。
- 下一步：把一次 wheel 更新写成可核验的“删除位置—连续和”公式，并计算每个长度 L 的合并和有多少互异值；首个目标是证明 |D_{k+1}\D_k| 相对于 M_{k+1}-M_k 的非平凡下界。
- 来源核对：官方页面确认题目只涉及连续 totative gaps，并仍标为 OPEN：[Erdős Problem 854](https://www.erdosproblems.com/854)。；官方讨论特别指出把连续间隙误换成任意差是不正确的：[854 discussion](https://www.erdosproblems.com/forum/thread/854)。
- 时间记账：所在批次墙钟时间按题数均摊约 50.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/854)；既有候选答案（按不可信材料审计）

### #856

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $f_k(N)$ be the maximum value of $\sum_{n\in A}\frac{1}{n}$, where $A$ ranges over all subsets of $\{1,\ldots,N\}$ which contain no subset of size $k$ with the same pairwise least common multiple. Estimate $f_k(N)$.
- 题意摘要：固定整数 k≥3。对每个 N，在所有 A⊆{1,…,N} 中取调和权重 Σ_{a∈A}1/a 的最大值；限制是不存在 k 个互异元素 a₁,…,a_k，使所有二元组的 lcm(a_i,a_j) 相同。要求估计 N→∞ 时的 f_k(N)。
- 状态核对：仍为开放题。候选答案不是证明；其中引用的 arXiv:2512.20055 首次提交于 2025-12-23，晚于冻结日期 2025-08-31，不能作为该日期状态的依据。不过该预印本现可独立核验，并支持官方页面后来加入的幂次上下界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：先重建 Erdős 的双计数上界，再检查与 sunflower 的平方自由编码。若 t=ap 且 p 为素数，对固定 t 至多有 k−1 个这样的 a∈A；否则 a_i=t/p_i 给出 k 个互异素数 p_i，且 lcm(t/p_i,t/p_j)=t。于是对 (a,p) 求和得到经典上界。另一方面，取素数 q₁,…,q_r，并把集合 S⊆[r] 编码为 n_S=∏_{i∉S}q_i；则 lcm(n_{S_i},n_{S_j}) 相同等价于 S_i∩S_j 相同，给出精确的 sunflower→LCM 归约。
- 局部结论：严格得到 (Σ_{a∈A}1/a)(Σ_{p<N}1/p)≤(k−1)Σ_{t<N²}1/t，故 f_k(N)≪_k log N/loglog N。；取 A 为不超过 N 的全部素数时不可能出现三个、从而不可能出现 k 个等 pairwise-LCM 元素，所以 f_k(N)≥Σ_{p≤N}1/p=loglog N+O(1)。；平方自由补集编码严格保持“pairwise lcm 相等”与“pairwise intersection 相等”，确认 856 与弱 sunflower 问题之间不是仅有类比，而有直接有限模型归约。
- 第一阻塞点：编码后各 n_S 的权重 1/n_S 差异很大；仅知道 sunflower-free 家族的基数，不能直接推出所需的调和权重幂次。第一处未闭合步骤是设计素数分桶并同时控制乘积≤N、权重近似均匀和组合容量损失。
- 下一步：固定一个 r 维 sunflower-free 家族，采用 r 个短素数区间进行分桶，明确计算所得总权重及最大元素；检验优化区间参数后能否重现预印本中的指数 log μ_k^S。
- 来源核对：[Erdős Problems #856](https://www.erdosproblems.com/856)：核对题面、开放状态及经典双计数上界。；[Tang–Zhang 预印本](https://arxiv.org/abs/2512.20055)：核对提交日期、μ_k^S 定义为 limsup，以及所述 LCM 幂次界；候选答案把 limsup 写成已证明存在的极限，不准确。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/856)；既有候选答案（按不可信材料审计）

### #857

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $m=m(n,k)$ be minimal such that in any collection of sets $A_1,\ldots,A_m\subseteq \{1,\ldots,n\}$ there must exist a sunflower of size $k$ - that is, some collection of $k$ of the $A_i$ which pairwise have the same intersection. Estimate $m(n,k)$, or even better, give an asymptotic formula.
- 题意摘要：固定 n 及 k≥3；对象是 2^[n] 中互异集合组成的族。m(n,k) 是保证任意大小至少为 m 的集合族都含 k 个互异成员、且任意两者交集相同的最小整数。因此若 F_k(n) 表示最大 k-sunflower-free 族大小，则 m(n,k)=F_k(n)+1。
- 状态核对：开放。形式化文件使用 Set (Set (Fin n))，明确排除了多重集歧义。候选答案声称容量极限存在，但相关 Tang–Zhang 文献实际将 μ_k^S 定义为 limsup；其“tensor-power argument”不能直接用于非均匀弱 sunflower 家族。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：检验候选答案的分块下界。把前 r(k−1) 个点分为 r 块，每块大小 k−1，令 s=⌈(k−1)/2⌉，取所有在每块恰选 s 个点、在剩余坐标取固定图样的集合。若 k 个成员构成 sunflower，则在每一块内，它们的 s-子集也有相同的两两交。
- 局部结论：在一个大小 k−1 的块内，k 个 s-子集若两两交相同，则它们必全相同：若有重复，等势性立即迫使全部相同；若全异，则相对公共核的 k 个非空花瓣互不相交，需要至少 k 个底点，矛盾。；逐块应用上一结论，k 个全局集合只能完全相同，故构造确实无 k-sunflower。于是 F_k(n)≥binom(k−1,⌈(k−1)/2⌉)^⌊n/(k−1)⌋。；对 k=3，一手文献给出 F_3(n)≤3nΣ_{j≤n/3}binom(n,j)≤(3/2^(2/3))^{(1+o(1))n}。
- 第一阻塞点：分块构造只给出下界。试图用普通直积证明 F_k(n+m)≥F_k(n)F_k(m)时会卡住：一个投影中的 k 个坐标可有重复但不全相同，并仍满足 pairwise-intersection 条件；因此候选答案的容量极限存在性并未由所称张量论证闭合。更关键的上界改进正是开放的弱 sunflower 障碍。
- 下一步：先构造或排除上述直积失效的最小显式例子；随后只用 μ_k^S:=limsup F_k(n)^(1/n) 表述指数容量，避免未经证明的极限断言。
- 来源核对：[Erdős Problems #857](https://www.erdosproblems.com/857)：核对开放状态及 k=3 上界。；[Naslund–Sawin 原论文](https://arxiv.org/abs/1606.09575)：核对 3nΣ_{j≤n/3}binom(n,j) 上界。；本地形式化题面 857.lean：确认对象是集合族而非可重复的序列。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/857)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/857.lean`；既有候选答案（按不可信材料审计）

### #858

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \{1,\ldots,N\}$ be such that there is no solution to $at=b$ with $a,b\in A$ and the smallest prime factor of $t$ is $>a$. Estimate the maximum of\[\frac{1}{\log N}\sum_{n\in A}\frac{1}{n}.\]
- 题意摘要：对每个 N，最大化 M(N)=Σ_{n∈A}1/n，其中 A⊆[N]，且不存在互异 a,b∈A 与 t>1 满足 b=at、P⁻(t)>a。题目要求 M(N)/log N 的定量渐近，而非研究单个固定无限集合。
- 状态核对：已解决。必须吸收人工评审：候选答案只凭有限 DP 数值声称收敛，未证明定量渐近，而且给出的约 0.620 不是正确显式常数。当前证明给出 c=0.6187712111…，并证明 M(N)=(c+o(1))log N。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建已知证明骨架。定义 a≺b 当 b=at 且 P⁻(t)>a。按素因子非降序写 n=p₁⋯p_r，祖先恰为满足 p_{j+1}>p₁⋯p_j 的前缀积；故偏序的 Hasse 图是一棵以 1 为根的树。对子树最优值 F_N(a) 使用 Bellman 递推，再证明最优策略最终是阈值前沿。
- 局部结论：祖先前缀判据严格推出每个 n>1 有唯一父节点 π(n)，所以候选答案的森林/树结构与 Bellman 递推 F_N(a)=max{1/a,Σ_{b child of a}F_N(b)}是正确的局部部分。；当 a>N^(1/4) 时，a 的孩子只能是 ap 或 apq，其中 p,q>a 为素数；这些孩子大于 N^(1/2)，因而是叶子。继续收益遂化为素数和与半素数和 P_N(a)+Q_N(a)，并随 a 单调递减。；已知证明由此得到阈值 K_N=N^{α₂+o(1)}。其中 Φ(u)=log((1−u)/u)+∫_u^{(1−u)/2}log((1−u−v)/v)dv/v，α₂∈(1/4,1/3) 满足 Φ(α₂)=1，且 c=1/2+∫_{α₂}^{1/2}(1−Φ(u))du=0.6187712111…。
- 第一阻塞点：本次重建中第一项未逐行重新证明的是半素数贡献 Q_N(a) 到 Φ(u) 的一致素数调和 Riemann 和极限；这需要在 u∈[1/4,1/3] 上控制双素数和的统一误差。该步骤在现有解答中有明确引理，故是重建缺口，不是问题仍开放。
- 下一步：逐行核验解答中的“polynomial intervals 上一致 Mertens”及 prime-harmonic Riemann sum 两个引理，尤其检查端点 u=1/3 和由 K_N=N^{α₂+o(1)} 推出最终积分常数时的统一误差。
- 来源核对：[Erdős Problems #858](https://www.erdosproblems.com/858)：核对 solved 状态及正确常数约 0.618。；[完整渐近证明 PDF](https://www.ulam.ai/research/erdos858-asymptotic.pdf)：核对祖先判据、Bellman 递推、阈值前沿和显式常数公式。；明确否定候选答案的 0.620+o(1)：有限数值稳定不能代替渐近证明，且数值与现解不符。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/858)；既有候选答案（按不可信材料审计）

### #859

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $t\geq 1$ and let $d_t$ be the density of the set of integers $n\in\mathbb{N}$ for which $t$ can be represented as the sum of distinct divisors of $n$. Do there exist constants $c_1,c_2>0$ such that\[d_t \sim \frac{c_1}{(\log t)^{c_2}}\]as $t\to \infty$?
- 题意摘要：对每个固定整数 t≥1，令 A_t 为所有正整数 n，使 t 能写成 n 的若干互异正因数之和；d_t 是 A_t 的自然密度。问题询问是否存在与 t 无关的 c₁,c₂>0，使 d_t∼c₁/(log t)^{c₂}。
- 状态核对：开放。Erdős 已证明每个 d_t 存在并有两个对数幂界；候选答案进一步断言可取显式指数 1、2，但官方材料并未支持这一具体数值，所引 Scribd 也不是可靠的一手核验，因此不采纳。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：从表示的有限性直接重建密度存在。令 W_t={lcm(S): S⊆{1,…,t}，S 中元素互异且 Σ_{d∈S}d=t}。由于每个被选因数都≤t，有 n∈A_t 当且仅当存在 L∈W_t 使 L|n。
- 局部结论：W_t 是有限集，且每个 L 都整除 Q_t=lcm(1,…,t)；因此 A_t 是有限个倍数集合的并，事实上以 Q_t 为周期，自然密度必存在。；可由有限容斥得到精确公式 d_t=Σ_{∅≠J⊆W_t}(−1)^{|J|+1}/lcm(J)，相同 L 应先去重。；因 {t} 本身是一种表示，t∈W_t，故所有 t 的倍数属于 A_t，从而 d_t≥1/t>0。
- 第一阻塞点：周期/容斥公式的周期 Q_t 约为 exp(t)，且 W_t 的重叠结构高度依赖 t；它没有给出 d_t 随 t 的正则变化。第一处无法闭合的是证明 log d_t/loglog t 收敛到常数，更不用说控制归一化常数 c₁；现有对数幂夹逼不足以排除振荡。
- 下一步：利用容斥公式精确计算一段连续 t 的 d_t，检验有效指数 −log d_t/loglog t 是否稳定，或是否沿素数、光滑数等子序列产生可证分离；若能证明两个子序列极限不同，即可反驳所问渐近式。
- 来源核对：[Erdős Problems #859](https://www.erdosproblems.com/859)：核对开放状态及仅声明存在某些正指数 c₃,c₄。；本地形式化题面 859.lean：核对自然密度量词及 c₁,c₂ 为统一常数。；候选答案关于显式 1/log t 与 1/(log t)² 的说法未获可靠一手来源支持，故未复述为已知定理。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/859)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/859.lean`；既有候选答案（按不可信材料审计）

### #860

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be such that, for any $m\geq 1$, in the interval $(m,m+h(n))$ there exist distinct integers $a_i$ for $1\leq i\leq \pi(n)$ such that $p_i\mid a_i$, where $p_i$ denotes the $i$th prime. Estimate $h(n)$.
- 题意摘要：对每个 n，h(n) 是满足如下性质的最小统一区间长度 H：对每个整数 m≥1，开区间 (m,m+H) 内可为每个 p_i≤n 选择一个整数 a_i，要求 p_i|a_i，且所有 a_i 两两不同。量词顺序是先固定 n、H，再对所有 m 要求存在一次匹配。
- 状态核对：开放。官方记录的窗口为 h(n)/n→∞ 与 h(n)≪n^{3/2}/√log n；候选答案只是复述这些结果，没有推进证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把问题写成二分图匹配：左侧为素数 p≤n，右侧为区间 I=(m,m+H)∩ℤ，若 p|a 就连边。Hall 定理把问题等价地归约为：对每个素数子集 S⊆{p≤n}，区间内至少有 |S| 个整数可被 S 中某个素数整除。然后尝试从单点 Hall 障碍和大素数子集开始估计。
- 局部结论：取最大素数 p≤n。若 H≤p，可把开区间放在两个相邻 p 的倍数之间，使其中没有 p 的倍数；因此按整数长度约定 h(n)>p，特别地 h(n)≥(1−o(1))n。；完整问题严格等价于所有 S 的 Hall 不等式 |{a∈I:∃p∈S,p|a}|≥|S|；这指出困难不在单个素数，而在许多素数的倍数于短区间中碰撞。；若只检查单点条件，每个 p≤n 有一个倍数，仅需 H大于约 n；Ruzsa 的 h(n)/n→∞ 表明真正的极端障碍必来自规模趋于无穷的 S。
- 第一阻塞点：对给定 S，容斥估计 union_{p∈S}{a∈I:p|a} 时，误差依赖区间起点 m，且不同素数的倍数可集中碰撞；无法得到对所有 m、所有 S 都足够强的统一下界。这正是从线性尺度推进到已知 n^{3/2}/√log n 上界的首个实质缺口。
- 下一步：固定 n,H，对所有连续区间用程序计算最坏 Hall deficiency，并记录造成缺陷的素数集合 S；检验极端 S 是否集中在某个大素数区间。若是，下一步可只对该尺度建立筛法型统一并集下界。
- 来源核对：[Erdős Problems #860](https://www.erdosproblems.com/860)：核对开放状态、Erdős–Pomerance 上界及 Ruzsa 超线性下界。；候选答案中的“Erdős–Selfridge 仅为 infinitely many n”并非官方题面所说；官方直接写 h(n)>(3−o(1))n，因此未采用其额外限定。
- 时间记账：所在批次墙钟时间按题数均摊约 55.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/860)；既有候选答案（按不可信材料审计）

### #863

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$ and let $A\subseteq \{1,\ldots,N\}$ be a set of maximal size such that there are at most $r$ solutions to $n=a+b$ with $a\leq b$ for any $n$. (That is, $A$ is a $B_2[r]$ set.) Similarly, let $B\subseteq \{1,\ldots,N\}$ be a set of maximal size such that there are at most $r$ solutions to $n=a-b$ for any $n$. If $\lvert A\rvert\sim c_rN^{1/2}$ as $N\to \infty$ and $\lvert B\rvert \sim c_r'N^{1/2}$ as $N\to \infty$ then is it true that $c_r\neq c_r'$ for $r\geq 2$? Is it true that $c_r'<c_r$?
- 题意摘要：固定整数 r≥2。令 F_r(N) 为 A⊆[N] 中满足每个 n 的无序表示 n=a+b（a≤b）至多 r 次时的最大基数；令 D_r(N) 为 B⊆[N] 中满足每个正差 n=a-b（所以 a>b）至多 r 次时的最大基数。假设 F_r(N)∼c_r√N、D_r(N)∼c'_r√N，问是否对每个 r≥2 都有 c'_r<c_r。
- 状态核对：已证明为真。正式页面给出的充分比较是 c'_r≤√r，而非旧候选所声称且本题并不需要的 c'_r=√r；后者未由所查材料核实。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建“差集上界＋和集构造下界”。差集一侧采用 Erdős–Turán 型短差计数，得到 D_r(N)≤(√r+o(1))√N。和集一侧使用 Cilleruelo–Ruzsa–Trujillo 构造，令 q=⌊r/2⌋，得到 F_r(N)≥((r+q)/√(r+2q)+o(1))√N。随后直接比较常数。
- 局部结论：正式陈述只约束正差 n≥1，故 n=0 不参与计数；旧候选的“需修正归一化”在当前正式版本中多余。；由上述两个已知界，c'_r≤√r 且 c_r≥(r+q)/√(r+2q)。；因 q≥1，(r+q)^2-r(r+2q)=q^2>0，故 √r<(r+q)/√(r+2q)，从而严格得到 c'_r<c_r。
- 第一阻塞点：若要求完全自足地重证，则第一处缺口是短差加权计数中把粗界 √(2rN) 改进为 (√r+o(1))√N，以及 CRT02 构造本身；但引用这些已发表结果后，最后的严格比较已经闭合。
- 下一步：逐行核对 CRT02 构造采用的是“a≤b 的无序表示至多 r”这一相同规范，并独立写出 Erdős–Turán 短差引理。
- 来源核对：Erdős Problems #863（2026-04-24 更新）：https://www.erdosproblems.com/863；正式页面明确列出 c'_r≤√r、CRT 构造下界及严格比较；未采纳旧候选关于 c'_r=√r 和固定 r 下 c_r 存在性未解决的旁支结论
- 时间记账：所在批次墙钟时间按题数均摊约 66.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/863)；既有候选答案（按不可信材料审计）

### #864

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subseteq \{1,\ldots N\}$ be a set such that there exists at most one $n$ with more than one solution to $n=a+b$ (with $a\leq b\in A$). Estimate the maximal possible size of $\lvert A\rvert$ - in particular, is it true that\[\lvert A\rvert \leq (1+o(1))\frac{2}{\sqrt{3}}N^{1/2}?\]
- 题意摘要：对每个 N，求满足下列条件的 A⊆[N] 的最大基数：至多存在一个整数 n，使无序和表示数 r_A(n)=|{(a,b):a,b∈A,a≤b,a+b=n}| 超过 1。特别问最大值是否至多 (2/√3+o(1))√N。
- 状态核对：截至所查页面仍开放。已明确吸收人工评审：旧候选从 a+b=c+d 推出 a+d=b+c 是错误恒等式，因此“删去一个元素即成 Sidon 集”及常数 1 的结论全部无效。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：下界采用镜像 Sidon 构造；上界先尝试只按表示数计数，以确定这种朴素路线的真实极限。取 Sidon 集 B⊆[1,N/3]，令 A=B∪(N-B)。同侧和分别落在低区与高区；交叉和为 N+(b-b')，Sidon 性保证非零差唯一，而 b=b' 全部集中在唯一例外和 n=N。
- 局部结论：镜像构造给出合法集合 |A|=(2/√3+o(1))√N，从而目标常数至少为 2/√3。；若 m=|A|，例外和有 t 个表示，则这些表示使用互不重叠的元素（至多另有一个对角表示），故 t≤⌈m/2⌉。；不同和的数目至少 m(m+1)/2-(t-1)，而和只落在 2,…,2N；因此 m(m+1)/2-⌈m/2⌉+1≤2N-1，只能推出 m≤2√N+O(1)。
- 第一阻塞点：第一处无法闭合的是把常数 2 降到 2/√3：单纯控制例外和的重数 t 会丢失不同表示之间的序结构，无法提供所需额外约 m²/8 的碰撞或空位。旧候选试图用错误等式制造第二个碰撞，正是在此处失败。
- 下一步：建立并计算“按较小端点排序的例外匹配”所诱导的差集交叉关系；先检验能否证明至少 (m²/8-O(m)) 个潜在和被迫落在表示集之外。
- 来源核对：Erdős Problems #864：https://www.erdosproblems.com/864；页面确认开放及 Erdős–Freud 的镜像 Sidon 下界；人工评审指出的代数错误已独立复算并排除
- 时间记账：所在批次墙钟时间按题数均摊约 66.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/864)；既有候选答案（按不可信材料审计）

### #865

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：There exists a constant $C>0$ such that, for all large $N$, if $A\subseteq \{1,\ldots,N\}$ has size at least $\frac{5}{8}N+C$ then there are distinct $a,b,c\in A$ such that $a+b,a+c,b+c\in A$.
- 题意摘要：存在绝对常数 C>0，使得对所有充分大的 N及每个 A⊆[N]，若 |A|≥5N/8+C，则 A 中存在两两不同的 a,b,c，且 a+b、a+c、b+c 也都属于 A。
- 状态核对：数学命题已由 Cipollini 证明，得到 f_3(N)≤5N/8+O(1)，结合标准构造即 f_3(N)=5N/8+O(1)。但“完整无条件 Lean 验证”需谨慎表述：所查本地 FormalConjectures 文件及其主仓链接仍含 sorry；arXiv 摘要只声称一个较早的条件化归约无 sorry。另有独立 Aristotle 仓库，网站据此标记 PROVED (LEAN)。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：重建新证明的折叠路线。选 h≈N/2，考察 A∩[1,2h] 中模 h 重复出现的剩余类 B；无目标三元组时，B 满足循环弱无和约束。进一步记录既能以不绕回、又能以绕回方式表示为两个不同 B 元素之和的剩余类 C。核心折叠引理控制 |B|-|C|≤h/4+O(1)，再将 C 对应到 A 的空折叠坐标，结合上下两层计数得到 |A|≤5N/8+O(1)。
- 局部结论：标准无构型例为约 [N/8,N/4]∪[N/2,N]，基数为 5N/8+O(1)，故主系数不能降低。；若 A 无所求三元组，则对任何互异 x,y∈A，只要 x+y∈A，就不能再有第三个 z∈A 同时满足 x+z,y+z∈A；即由 A 定义的“和仍在 A”图是三角形自由的。；Cipollini 的自足证明给出 f_3(N)≤5N/8+O(1)，因此与构造合并后原命题成立。
- 第一阻塞点：在自行重建中，第一处需要引用而尚未在此完全展开的是折叠引理 |B|-|C|≤h/4+O(1) 及其两个边界情形。它正是从一般三角形自由界跨越到 5/8 的关键。
- 下一步：逐条形式化折叠引理的定义与注入映射，并区分 h略大于、略小于 N/2 两种收尾；同时审计独立 Lean 仓库是否无额外假设且最终定理与原量词完全一致。
- 来源核对：Erdős Problems #865：https://www.erdosproblems.com/865；Cipollini, arXiv:2606.29361：https://arxiv.org/abs/2606.29361；独立形式化仓库：https://github.com/mrricky22/erdos-865-lean；本地 865.lean 的主定理仍为 `by sorry`，不能单凭该文件称已验证
- 时间记账：所在批次墙钟时间按题数均摊约 66.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/865)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/865.lean`；既有候选答案（按不可信材料审计）

### #866

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $g_k(N)$ be minimal such that if $A\subseteq \{1,\ldots,2N\}$ has $\lvert A\rvert \geq N+g_k(N)$ then there exist integers $b_1,\ldots,b_k$ such that all $\binom{k}{2}$ pairwise sums are in $A$ (but the $b_i$ themselves need not be in $A$). Estimate $g_k(N)$.
- 题意摘要：固定 k≥3。g_k(N) 是使下述性质成立的最小整数 g：每个 A⊆[2N] 只要 |A|≥N+g，就存在 k 个两两不同的正整数 b_1,…,b_k，使所有 i<j 的和 b_i+b_j 均属于 A；b_i 本身无需属于 A。求 g_k(N) 的阶。互异性虽在摘录句中省略，却由原问题传统、人工评审及全部已知结果共同强制。
- 状态核对：一般问题开放；k=3,4,5,6 已有强结果。旧候选令所有 b_i 相等，直接违反互异性，故 g_k(N)=1 的结论无效。若允许重复，问题确会退化，这也反证那不是预期陈述。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：尝试把问题化为 A 中元素的三角参数化。对 k=3，若选到互异 x,y,z∈A 且 x+y+z 为偶数，则线性方程 b_1+b_2=x、b_1+b_3=y、b_2+b_3=z 有唯一解 b_1=(x+y-z)/2、b_2=(x+z-y)/2、b_3=(y+z-x)/2。由此把 g_3 的问题归约为选择适当奇偶性并保证解为互异正整数；高 k 则对应在“pair-sum 图”中寻找 K_k。
- 局部结论：上述线性反演严格成立；且 x,y,z 两两不同时，所得 b_i 也两两不同。；仅用奇偶抽屉不能完成证明：它保证整数性，却不保证三个 b_i>0；正性等价于 x+y>z、x+z>y、y+z>x。；已知基准为 g_3(N)=2、g_4(N)=O(1)（现有显式上界 2032）、g_5(N)≈log N、g_6(N)≈N^{1/2}；这些结果立即排除旧候选的统一常数答案。
- 第一阻塞点：当前具体三角参数化路线的第一处缺口是：由 |A|≥N+2 严格抽取满足正确奇偶性及三角不等式的三个互异元素。若把 b_i 允许为任意有符号整数，正性障碍消失并会改变问题，因此必须先从原始 CES75 核定 b_i 的定义域。
- 下一步：先完整重证 k=3：按 A 在 [1,N]、[N+1,2N] 及奇偶类中的分布分类，寻找满足三角不等式的 x,y,z；这既可验证量词规范，也可作为高 k 图论归约的单元测试。
- 来源核对：Erdős Problems #866：https://www.erdosproblems.com/866；页面列出 g_3=2、g_4≤2032、g_5≈log N、g_6≈√N 及一般界；人工评审明确指出 b_i 必须互异；旧候选的重复取值法已排除；仍需查 CES75 原文以消除“integers”是否默认正整数的措辞歧义
- 时间记账：所在批次墙钟时间按题数均摊约 66.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/866)；既有候选答案（按不可信材料审计）
- 深度项目：仓库深挖把首个未决案例定位为 k=7：Lean 已验证 $g_7(N)=O(N^{7/8})$；自然语言证明并经独立审计、但尚未 Lean 化的结果为，充分大 N 时 $g_7(N)>\frac1{16}N^{2/3}$。项目明确不声称 #866 已解决；当前核心是必须保留配置结构的逆定理，例如暴露二次因子或精确控制 $R_{10}$ 的碰撞商。 [证据](/home/biostar/work/projects/amra/projects/erdos-866-ai-continuation-20260505/proof/current_focus.md)

### #868

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：If $A$ is an additive basis of order $2$, and $1_A\ast 1_A(n)\to \infty$ as $n\to \infty$, then must $A$ contain a minimal additive basis of order $2$? (i.e. such that deleting any element creates infinitely many $n\not\in A+A$) What if $1_A\ast 1_A(n) >\epsilon \log n$ (for all large $n$, for arbitrary fixed $\epsilon>0$)?
- 题意摘要：A⊆ℕ 是二阶渐近加法基，且有序卷积 r_A(n)=(1_A*1_A)(n) 趋于无穷。问 A 是否必含一个二阶最小渐近基 B，即任删 b∈B 后都有无穷多个大整数不再属于 (B\{b})+(B\{b})。第二问把增长加强为：对某个任意预先给定的 ε>0，充分大 n 时 r_A(n)>εlog n。
- 状态核对：两问均已被 Larsen–Larsen 的反例否定：存在某个绝对常数 c>0 及基 A，使 r_A(n)>c log n 最终成立，但 A 不含任何最小二阶子基。这里一个固定 c 的反例足以否定“对任意 ε 都保证”的命题，但不表示对所有大 ε 都存在反例；事实上 Erdős–Nathanson 对系数大于 1/log(4/3) 有正定理。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：按已知反例机制重建目标条件：把 A 分块构造成高度冗余的二阶基，每个大 n 在约 log n 个尺度上各获得表示，从而 r_A(n)≥c log n；同时安排任何仍为基的子集都含有一个可删除而不破坏渐近基性的冗余元素，因此不存在极小子基。
- 局部结论：若 r_A(n)>c log n 最终成立，则自动有 r_A(n)→∞，故同一构造同时否定第一问。；同一构造对每个 0<ε<c 都满足 r_A(n)>εlog n，足以否定“任意固定 ε>0 均能推出正结论”。；这与 Erdős–Nathanson 的正阈值不冲突：当系数超过 (log(4/3))^{-1}≈3.476 时，已知必含最小子基，所以反例常数 c 必位于允许区间内。
- 第一阻塞点：在本次受限重建中，第一处尚未自足闭合的是分块构造的两项同时估计：逐个 n 给出 c log n 个表示，以及对任意子基证明存在可删元素。可访问页面只给出结论，链接论文为 PDF，未能抽取其详细引理。
- 下一步：下载并逐页核查 Larsen–Larsen 论文：明确块的端点、常数 c、表示计数是否为有序卷积，并把“无最小子基”的量词写成对所有 B⊆A 的可删元素命题。
- 来源核对：Erdős Problems #868：https://www.erdosproblems.com/868；Larsen–Larsen 论文仓库：https://github.com/Larsen-Daniel/Erdos-868/blob/main/868.pdf；本地 868.lean 只编码状态且各定理仍含 sorry，不能充当反例构造的形式验证；正式页面明确记载存在 c>0、r_A(n)>c log n 且无最小子基
- 时间记账：所在批次墙钟时间按题数均摊约 66.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/868)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/868.lean`；既有候选答案（按不可信材料审计）

### #869

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：If $A_1,A_2$ are disjoint additive bases of order $2$ (i.e. $A_i+A_i$ contains all large integers) then must $A=A_1\cup A_2$ contain a minimal additive basis of order $2$ (one such that deleting any element creates infinitely many $n\not\in A+A$)?
- 题意摘要：量词为：对任意两个互不相交的集合 A₁,A₂⊆ℕ，若各自都是二阶渐近基，即存在 N_i 使每个 n≥N_i 属于 A_i+A_i，是否必存在 B⊆A₁∪A₂，使 B 是二阶渐近基，且每个 b∈B 都满足 B\{b} 漏掉无穷多个整数？否定它须构造 A=A₁⊔A₂，同时 A 不含任何这种 B。
- 状态核对：已否定。旧候选称“仍开放”已经过时，不能采用。官方页面现称 Larsen 构造了反例，并更强地实现了“表示数趋于无穷、可分成两个基、含最小基”三种性质的任意组合。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `high`
- 尝试路线：重建反例的块构造路线：取迅速增长的关卡 N_j，先造在普通整数上表示充分、但在 N_j 处表示被精确控制的基；在每个关卡加入有限“补丁对”，并把补丁分配给 A₁、A₂，使两色各自覆盖所有充分大的整数。同时令关卡依次检验 A 的有限子集，使任意候选子基 B 若仍为基，就可继续删除某个元素而仍为基，从而排除最小子基。
- 局部结论：仅有 A=A₁⊔A₂ 已立即给出 r_A(n)≥r_{A₁}(n)+r_{A₂}(n)≥2（充分大 n），但常数冗余远不足以推出最小子基。；若关卡构造能证明：每个基 B⊆A 删除某个元素后仍是基，则 A 确实不含最小基；这是反例所需的精确否定条件。；官方公布的更强独立性结果中特取“可分成两个基=true、含最小基=false”，即直接给出本题反例。
- 第一阻塞点：在本次受限重建中，第一处尚未独立闭合的是块间隔参数的同时选择：必须逐项验证补丁不会产生新的跨块表示、两种颜色仍覆盖所有大整数，并且对不可数目虽仅连续统、但需由可数有限模式编码的所有 B⊆A 都实现可删除性。不能用“对候选逐个枚举”草率代替该论证。
- 下一步：逐引理审计 Larsen 文稿中的关卡编码：固定一个有限模式，明确写出它如何迫使候选 B 出现非本质元素，并检查该性质在后续所有块加入后仍保持。
- 来源核对：[Erdős Problems #869](https://www.erdosproblems.com/869) 当前明确标为 DISPROVED，并记录三种性质相互独立。；反例文稿入口为 [Larsen 的 Erdos-869 仓库](https://github.com/Larsen-Daniel/Erdos-869/blob/main/869.pdf)；本次只能核对官方结论和文稿入口，未完成逐页证明审计。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/869)；既有候选答案（按不可信材料审计）

### #870

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 3$ and $A$ be an additive basis of order $k$. Does there exist a constant $c=c(k)>0$ such that if $r(n)\geq c\log n$ for all large $n$ then $A$ must contain a minimal basis of order $k$? (Here $r(n)$ counts the number of representations of $n$ as the sum of at most $k$ elements from $A$.)
- 题意摘要：闭合量词为：是否对每个整数 k≥3，都存在仅依赖 k 的 c(k)>0，使得对每个 k 阶渐近基 A，若存在 N₀ 使所有 n≥N₀ 都有 r_A(n)≥c(k)log n 个“至多 k 项”表示，则 A 含有一个按包含关系最小的 k 阶渐近子基 B？
- 状态核对：官方仍列为 open。页面虽有一份声称对所有 k≥3 给出反例的评论稿，但评论未经核实，且已有读者指出其中存在可疑步骤；因此不能把它升级为已解决。旧候选的状态判断基本符合冻结状态，但其“超图匹配困难”只是概述，不是证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试把 k=2 的删除/SDR 方法推广为有限超图选择。对每个大 n，以 A 中大小至多 k、和为 n 的子集（连同重数资料）为超边；希望选出 B⊆A，使每个 n 保留一条边，同时每个 b∈B 对无穷多个 n 是所有剩余边的必经点。可先按 a₁,a₂,… 贪心删除：若删除 a_j 后仍为 k 阶基便删除，否则保留。
- 局部结论：在任一最小子基 B 中，每个 b∈B 必有无穷多个 n，使 n 在 B 中的每个至多 k 项表示都使用 b；否则删去 b 只造成有限多个例外，B\{b} 仍是渐近基。；有限阶段的贪心删除严格保持“是渐近基”，因为每一步只在删除后仍为基时才删除。；表示下界 c log n 保证每个表示超图的边数多，但不控制不同表示的重叠或最大余度；所有表示可能集中经过很少的元素。
- 第一阻塞点：第一处断裂发生在取无限交 B=⋂_j B_j：各有限阶段的覆盖阈值可能趋于无穷，故极限 B 未必仍覆盖任何给定尾部。直接套局部引理也失败，因为仅有边数下界，没有控制超边依赖度或共同核心，无法得到统一的保留概率。
- 下一步：检验一个明确的附加命题：若再假设每个 n 的表示超图最大点度至多 αr(n)，其中 α<1 仅依赖 k，能否用局部引理构造保持所有大 n 可表示的稀疏子基；先为有限区间 [N,2N] 写出完整概率估计。
- 来源核对：[Erdős Problems #870](https://www.erdosproblems.com/870) 仍标为 OPEN，并记录 k=2 的阈值定理。；[讨论页](https://www.erdosproblems.com/forum/thread/870) 有未经验证的反例声明；页面同时明确提示评论不保证正确，故未作为定理采用。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/870)；既有候选答案（按不可信材料审计）

### #871

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $A$ be an additive basis of order $2$ with $1_A*1_A(n)\to\infty$. Must $A$ split into two disjoint additive bases of order $2$?
- 题意摘要：量词为：对每个二阶渐近基 A，若有序卷积 r_A(n)=1_A*1_A(n) 满足对每个 T，存在 N_T 使 n≥N_T⇒r_A(n)≥T，是否必存在分割 A=A₀⊔A₁，使 A₀、A₁ 各自都是二阶渐近基？答案是否定的。
- 状态核对：已由反例否定，官方记录 Lean 验证。不能把早先“对每个固定 t 有 r_A(n)≥t 的不可分基”直接当作本题反例，因为固定 t 不推出 r_A(n)→∞；新构造的关键正是让 t 随关卡缓慢增长。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 Erdős–Nathanson/Larsen 的稀疏关卡路线：构造基础集 B，使 r_B(n) 在关卡 N_j 为零、在关卡外趋于无穷；再仅为 N_j 加入有限补丁对 x,N_j−x。令补丁数 t_j→∞，从而 r_A(N_j)→∞；同时安排补丁索引 F_j 枚举越来越大的有限模式，使任意二染色 A=A₀⊔A₁ 都有一种颜色在无穷多个 N_j 上没有同色表示。
- 局部结论：若 r_B(n) 在非关卡处趋于无穷，且后续只向 B 添加元素，则 A 在非关卡处的表示数也趋于无穷。；若 N_j 的全部 A-表示恰为 t_j 个预设补丁对且 t_j→∞，则关卡处也有 r_A(N_j)→∞；合并两部分即可得到全局 r_A(n)→∞。；对任意分割，只要某一颜色在无穷多个关卡没有同色补丁对，该颜色就漏掉无穷多个 N_j，因而不是渐近基；这足以排除分割成两个基。
- 第一阻塞点：独立重建中首先未闭合的是“全部表示恰为预设补丁对”：需用增长条件排除旧块—新块及两个不同补丁块之间意外和为 N_j，并同时证明关卡外的表示下界。正式结果已有 Lean 验证，但这里没有把数千行形式化证明重新展开。
- 下一步：抽取 Lean 证明中对应基础集 B 的核心引理，核对三项接口：关卡零表示、关卡外下界、加入补丁后的表示分类；这比直接审阅最终二染色结论更可检验。
- 来源核对：[Erdős Problems #871](https://www.erdosproblems.com/871) 标为 DISPROVED (LEAN)，并说明它是固定 t 构造的小幅强化。；[讨论页的证明梗概](https://www.erdosproblems.com/forum/thread/871) 明确描述了关卡 N_j、基础集 B、缓慢增长的补丁数及有限子集枚举机制。；本地 cohort 未附 871.lean；因此核对了官方形式化标记和公开梗概，但未在本地重新编译 Lean 文件。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/871)

### #872

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Consider the two-player game in which players alternately choose integers from $\{2,3,\ldots,n\}$ to be included in some set $A$ (the same set for both players) such that no $a\mid b$ for $a\neq b\in A$. The game ends when no legal move is possible. One player wants the game to last as long as possible, the other wants the game to end quickly. How long can the game be guaranteed to last for? At least $\epsilon n$ moves? (For $\epsilon>0$ and $n$ sufficiently large.) At least $(1-\epsilon)\frac{n}{2}$ moves?
- 题意摘要：在整除比较图 G_n（顶点 {2,…,n}，a,b 相邻当且仅当一者整除另一者）上，两人轮流把顶点加入同一个独立集 A；无法再加入时 A 为极大原始集。需分别指定谁先手，定义最优对弈终局长度 v_n：Prolonger 最大化、Shortener 最小化。问题问是否存在绝对 ε>0 使 v_n≥εn，以及是否对每个 ε>0 最终有 v_n≥(1−ε)n/2。
- 状态核对：总体线性下界仍开放，而且原题未指定先手。旧候选漏掉了较新的部分结果：在 Prolonger 先手的约定下，官方现记录 Shortener 可迫使长度至多 (23/48+o(1))n，故“任意 ε 下接近 n/2”已为否；这不解决是否有 Ω(n) 下界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试为 Prolonger 建立收费策略：优先选择 (n/2,n] 中尚合法的数；每当候选 x 被 Shortener 先前一步阻挡，就把 x 记账到某个与 x 可比的短方元素。若每个短方元素只能阻挡 O(1) 个候选，就会得到线性局数。
- 局部结论：终局必含每个素数 p∈(n/2,n]：区间内 p 的唯一可比顶点就是 p 本身。因此任何对局长度至少 π(n)−π(n/2)=(1+o(1))n/(2log n)。；更一般地，对每个 p∈[√n,n]，极大性要求 A 含一个 p 的倍数；不同此类素数不能由同一个 a≤n 覆盖，故 |A|≥π(n)−π(√n−1)=(1+o(1))n/log n。；所有合法 A 都是反链，而 {⌊n/2⌋+1,…,n} 是大小约 n/2 的反链；由整数整除反链的标准极值结论，绝对上限为 ⌊n/2⌋。
- 第一阻塞点：收费映射不能做到有界多对一：Shortener 选择一个小整数 d 后，可同时阻挡约 n/(2d) 个位于 (n/2,n] 的倍数。因此“守住上半区间”的直接策略只恢复素数级下界，无法推出 εn。
- 下一步：把候选限制为具有大最小素因子的上半区间整数，并计算单个合法短方落子可覆盖多少候选；目标是验证能否选择密度 δ>0 的候选族，使每个整除邻域与该族交于 O(1) 个点。
- 来源核对：[Erdős Problems #872](https://www.erdosproblems.com/872) 仍标为 OPEN，但记录了 Prolonger 先手时的 (23/48+o(1))n 上界及素数下界。；[讨论页](https://www.erdosproblems.com/forum/thread/872) 明确区分先手约定，并提示该上界的 Lean 形式化只覆盖了核心策略性质，不能据此夸大为整题形式化解决。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/872)；既有候选答案（按不可信材料审计）

### #873

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{a_1<a_2<\cdots\}\subseteq \mathbb{N}$ and let $F(A,X,k)$ count the number of $i$ such that\[[a_i,a_{i+1},\ldots,a_{i+k-1}] < X,\]where the left-hand side is the least common multiple. Is it true that, for every $\epsilon >0$, there exists some $k$ such that\[F(A,X,k)<X^\epsilon?\]
- 题意摘要：对象是任意严格递增无限序列 A={a₁<a₂<⋯}⊆ℕ。F(A,X,k) 是满足 lcm(a_i,…,a_{i+k−1})<X 的起点 i 数。自然闭合量词为：对每个 A、每个 ε>0，存在整数 k=k(A,ε)，使对所有充分大的实数 X 有 F(A,X,k)<X^ε。若要求所有 X>0，也与渐近版本基本等价，因为可再增大 k 消除有限的小 X 区间。
- 状态核对：仍开放。已知统一结果 F(A,X,3)≪X^{1/3}log X。旧候选的单调性 F_k≤F_3 正确，但只重复 1/3 指数，未触及随 k 改善。检查本地 Lean 文件发现其形式为 ∃k∀X>0，并用 StrictMono a；这比原文表面上更强，但可由增大 k 吸收有限 X，故不是实质性偏差。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试利用滑动窗口：若一个 k-窗口是好窗口，则其中每个连续三元组的最小公倍数也小于 X。因此好 k-窗口对应于三元好起点集合 S_X={i:lcm(a_i,a_{i+1},a_{i+2})<X} 中一段长度 k−2 的连续整数。希望用已知 |S_X|≪X^{1/3}log X 控制长连续段的起点数。
- 局部结论：严格有 F(A,X,k)≤F(A,X,3)，因为每个好 k-窗口的前三项构成好三元组。；更精确地，F(A,X,k) 等于至多 S_X 中长度至少 k−2 的连续游程所贡献的起点数；因此若能统一控制 S_X 的游程长度或数量，就会得到随 k 改善。；若渐近结论对 k₀ 和 X≥X₀ 成立，取 M=#{i:a_i<X₀} 并令 k>max(k₀,M)，则 X≤X₀ 时没有好 k-窗口，而 X≥X₀ 时 F_k≤F_{k₀}；故可升级为所有 X>0 的版本。
- 第一阻塞点：第一处无法闭合的是：已知三元组计数界只控制 |S_X|，完全不控制其聚集。S_X 可能在现有估计允许的范围内形成一段很长的连续游程，此时改取更大 k 几乎不降低起点数。需要新的算术引理排除这种聚集，不能仅靠集合计数。
- 下一步：证明或反驳一个具体游程命题：若连续 L 个三元组均有 lcm<X，则这 L+2 个严格递增整数是否必迫使 L≤X^{C/k}（或产生一个具有异常多因子的整数 m<X）；先对 L=4,5 做素数指数向量的穷尽归约。
- 来源核对：[Erdős Problems #873](https://www.erdosproblems.com/873) 仍标为 OPEN，并记录三元组的匹配量级 X^{1/3}log X。；已读取本地 [873.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/873.lean)，确认其使用 StrictMono、∃k∀X>0 和扩展自然数计数；定理本身仍为 sorry，不能视作形式化证明。
- 时间记账：所在批次墙钟时间按题数均摊约 44.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/873)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/873.lean`；既有候选答案（按不可信材料审计）

### #875

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{a_1<a_2<\cdots\}\subset \mathbb{N}$ be an infinite set such that the sets\[S_r = \{ a_1+\cdots +a_r : a_1<\cdots<a_r\in A\}\]are disjoint for distinct $r\geq 1$. How fast can such a sequence grow? How small can $a_{n+1}-a_n$ be? In particular, for which $c$ is it possible that $a_{n+1}-a_n\leq n^{c}$?
- 题意摘要：对象为无限递增集 A={a_1<a_2<…}⊂ℕ。要求任意两个有限子集 X,Y⊂A，只要 |X|≠|Y|，就有 ∑X≠∑Y；等价于各阶不同元素和集 S_r 两两不交。问题询问增长和逐点间隙，特别是哪些 c 允许最终满足 a_{n+1}-a_n≤n^c。
- 状态核对：截至给定日期仍为 open。有限极值定理能给必要条件，但不能直接控制逐点间隙。旧候选把计数函数下界误微分成间隙界，这是关键错误。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：截断 A_N=A∩[1,N] 仍可容许。应用 Deshouillers–Freiman 的有限定理 |A_N|≤2√(N+1/4)-1，再与假设的逐点间隙上界求和比较；构造方向则审查已知 A(x)≫x^{5-2√6} 能推出什么。
- 局部结论：令 N=a_n，有限定理给 n≤2√(a_n+1/4)-1，故 a_n≥n(n+2)/4，特别是 a_n≫n²。；若最终 a_{j+1}-a_j≤j^c，则 a_n=O(n^{c+1})；与 a_n≫n² 比较，严格推出必要条件 c≥1。；设 α=5-2√6。已知构造的 A(x)≫x^α 只推出 a_n≪n^{1/α}=n^{5+2√6}，因而粗略地 gap≤a_{n+1}；至多可据此得到每个 c>5+2√6 时最终 gap≤n^c，不能得到旧候选声称的 c=4+2√6。
- 第一阻塞点：第一处断裂是由 a_n≪n^d 推出 a_{n+1}-a_n≪n^{d-1}；一般递增序列完全不满足这种“离散求导”规则。现有计数函数界没有排除孤立的大跳跃。
- 下一步：直接检查 Erdős–Nicolas–Sárközy 构造的递归/分块参数，计算每个块内最大空档及相邻块之间的跳跃；这是判断其是否产生某个明确 gap 指数的可检验任务。
- 来源核对：[Deshouillers–Freiman 原文](https://www.numdam.org/article/AST_1999__258__141_0.pdf)明确给出充分大 N 时的有限极值定理。；[Erdős–Nicolas–Sárközy 论文记录](https://www.numdam.org/item/JTNB_1991__3_1_55_0/)确认无限构造满足 A(x)≫x^{5-2√6}；该陈述本身没有逐点 gap 估计。
- 时间记账：所在批次墙钟时间按题数均摊约 52.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/875)；既有候选答案（按不可信材料审计）

### #876

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{a_1<a_2<\cdots\}\subset \mathbb{N}$ be an infinite sum-free set - that is, there are no solutions to\[a=b_1+\cdots+b_r\]with $b_1<\cdots<b_r<a\in A$. How small can $a_{n+1}-a_n$ be? Is it possible that $a_{n+1}-a_n<n$?
- 题意摘要：对象为无限递增 A={a_n}⊂ℕ，且不存在 a=b_1+⋯+b_r，其中 b_1<⋯<b_r<a 均属 A；即没有一项是若干个互异较小项之和。问题询问逐点 gap，并问能否最终有 a_{n+1}-a_n<n。若按“对所有 n”逐字解释，则 n=1 时 gap≥1 已立即否定，故开放题只能理解为充分大 n。
- 状态核对：研究性解释下仍为 open。已报道 Graham 构造达到 gap<n^{1+o(1)}，但这不含常数为 1 的严格线性界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：用 Łuczak–Schoen 的截断计数上界转化为 a_n 的必要增长，再把目标 gap<n 求和，检查两者是否矛盾；同时区分全局计数密度与逐点 gap。
- 局部结论：由 A(N)≪(N log N)^{1/2}，代入 N=a_n 可严格反演为 a_n≫n²/log n。；若最终 a_{j+1}-a_j<j，则 a_n≤n²/2+O(n)；它与 a_n≫n²/log n 完全相容，因此现有密度上界不能否定目标。；零渐近密度只推出平均间隙 a_n/n→∞，并因此排除最终有界的全部间隙；它不提供某个指定位置的 gap 下界。
- 第一阻塞点：要构造 gap<n，必须同时保证每个新项都避开此前所有互异子集和。计数函数较大或 a_n=O(n² polylog n) 均不能保证无单个大空档；这正是从密度构造转到逐点覆盖时的第一处缺口。
- 下一步：重建 Graham 的分块/模构造，明确其 n^{o(1)} 因子的来源；逐项列出哪些参数若改进到常数 1 即可给 gap<n，并检查块边界是否为唯一损失。
- 来源核对：[Deshouillers–Erdős–Melfi 原论文页面](https://www.sciencedirect.com/science/article/pii/S0012365X98003227)确认定义是“互异较小项之和”，并只宣称多项式增长及 a_{n+1}/a_n→1。；[Łuczak–Schoen 论文档案](https://eudml.org/doc/207449)与题目官方上下文相符；其结论是计数函数界，不是逐点 gap 界。
- 时间记账：所在批次墙钟时间按题数均摊约 52.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/876)；既有候选答案（按不可信材料审计）

### #878

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $n=\prod_{1\leq i\leq t} p_i^{k_i}$ is the factorisation of $n$ into distinct primes then let\[f(n)=\sum p_i^{\ell_i},\]where $\ell_i$ is chosen such that $n\in [p_i^{\ell_i},p_i^{\ell_i+1})$. Furthermore, let\[F(n)=\max \sum_{i=1}^t a_i\]where the maximum is taken over all $a_1,\ldots,a_t\leq n$ such that $(a_i,a_j)=1$ for $i\neq j$ and all prime factors of each $a_i$ are prime factors of $n$. Is it true that, for almost all $n$,\[f(n)=o(n\log\log n)\]and\[F(n) \gg n\log\log n?\]Is it true that\[\max_{n\leq x}f(n)\sim \frac{x\log x}{\log\log x}?\]Is it true that (for all $x$, or perhaps just for all large $x$)\[\max_{n\leq x}f(n)=\max_{n\leq x}F(n)?\]Find an asymptotic formula for the number of $n<x$ such that $f(n)=F(n)$. Find an asymptotic formula for\[H(x)=\sum_{n<x}\frac{f(n)}{n}.\]Is it true that\[H(x) \ll x\log\log\log\log x?\]
- 题意摘要：对每个 n，令 P_p(n)=p^{⌊log_p n⌋}（p|n），则 f(n)=∑_{p|n}P_p(n)。若 t=ω(n)，F(n) 是 t 个两两互素、均≤n、且只使用 n 的素因子的整数之和的最大值。问题同时询问：f 的几乎处处小量、F 的几乎处处下界、max f 的渐近、max f=max F、f=F 的计数渐近，以及 H(x)=∑_{n<x}f(n)/n 的渐近和四重对数上界。
- 状态核对：整组仍为 open，部分结论已知。旧候选的 H(x)=Θ(x) 与 Erdős 已证的无界 limsup 及 H(x) 的迭代对数上下界直接冲突，不能采纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先建立 H 的正确重排，再用官方已知 H(x)≪x log log log x 做密度一的 Markov 推导；同时检查旧候选声称的“收敛素数级数”。
- 局部结论：恒等式 P_p(pm)=pP_p(m) 正确，因此 H(x)=∑_{p<x}S_p(x/p)，其中 S_p(y)=∑_{m<y}p^{⌊log_p m⌋}/m；按区间 [p^k,p^{k+1}) 分块也是正确的。；旧候选随后称主项绝对收敛是错误的：写 y=p^Ku、1≤u<p 后，主项含 x·log u/(pu)。当 u 保持在常数量级时它是 ≍x/p，而非 O(x log p/p²)，故不能对 p 作绝对收敛求和。；利用已知 H(x)≪x log log log x：对 n∈[√x,x] 且 f(n)≥εn log log n 的集合应用 Markov，所得比例 ≪log log log x/log log x→0；加上 n<√x，严格推出 f(n)=o(n log log n) 对几乎所有 n 成立。
- 第一阻塞点：分块公式中的相位 u_p(x)={x/p 在 p-adic 对数尺度中的尾数}随 p、x 强烈相关；若不能控制许多素数同时落入高贡献相位，就无法把公式化为点态渐近，也无法解决四重对数上界。F 的典型下界还需要把约 log log n 个互不相交的素因子组分别组合成接近 n 的平滑数。
- 下一步：对 dyadic 素数区间分组，严格估计满足 p^k≤x/p<p^kU 的素数数目；先尝试把 Erdős 的 x log log log x 上界中贡献最大的 k、p 区域缩小到四重对数规模。
- 来源核对：[Erdős 1984 原文](https://www.renyi.hu/~p_erdos/1984-16.pdf)给出 H 的迭代对数上下界、F 的典型行为设想及相关极值问题，明确排除 H(x)=O(x)。；定义审查：F 可等价看成把 P(n) 分成若干非空支持块、每块取不超过 n 的最大该块平滑数，其余 t-r 个槽填 1；这一等价需保留“空槽为 1”，旧候选写法在此点基本正确。
- 时间记账：所在批次墙钟时间按题数均摊约 52.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/878)；既有候选答案（按不可信材料审计）

### #879

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Call a set $S\subseteq \{1,\ldots,n\}$ admissible if $(a,b)=1$ for all $a\neq b\in S$. Let\[G(n) = \max_{S\subseteq \{1,\ldots,n\}} \sum_{a\in S}a\]and\[H(n)=\sum_{p<n}p+ n\pi(n^{1/2}).\]Is it true that\[G(n) >H(n)-n^{1+o(1)}?\]Is it true that, for every $k\geq 2$, if $n$ is sufficiently large then the admissible set which maximises $G(n)$ contains at least one integer with at least $k$ prime factors?
- 题意摘要：S⊂{1,…,n} admissible 意味着任意不同 a,b∈S 有 gcd(a,b)=1；G(n) 最大化 ∑_{a∈S}a。H(n)=∑_{p<n}p+nπ(√n)。问题一问 H(n)-G(n) 是否为 n^{1+o(1)} 上界；问题二问对每个固定 k≥2，充分大 n 的每个最大化集合是否含有一个至少有 k 个素因子的元素（“素因子”是否计重数宜回查原文）。
- 状态核对：两问总体 open；已知 H(n)-n^{3/2-o(1)}<G(n)<H(n)、(H-G)/n→∞，且第二问 k=2 已知。旧候选的 n∑1/p 启发不是证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：采用素数资源匹配：从基准集合 {1}∪{p<n} 出发，把两个不同素数 p,q 删除并加入 pq≤n；对多个互不相交的配对同时进行，精确计算收益并比较 H。
- 局部结论：若选取两两不交的素数对 (p,q_p)，且 pq_p≤n，则 S={1}∪(所有 p<n，删去每对端点)∪{pq_p} 仍两两互素。；该构造的和精确为 1+∑_{r<n}r+∑_p(pq_p-p-q_p)。因此要逼近 H，需给几乎所有 p≤√n 指派互异 q_p，使 pq_p接近 n，同时控制牺牲项 q_p。；这把第一问具体归约为一个带权素数匹配问题；单独对每个 p 使用“n/p 附近存在素数”不够，因为还必须保证 q_p 互异且不与其他端点冲突。
- 第一阻塞点：第一处无法闭合的是同时匹配：无条件素数分布结果不足以在所有尺度 n/p 的短区间中，为约 π(√n) 个小素数找到互异的近最优 q_p。题中所述“plausible but hopeless”假设正用于跨越此处。
- 下一步：先做有限但严格的 Hall 条件：限定 p≤n^θ，并用可用的素数短区间定理估计任意子集的候选 q 邻域；计算可无条件达到的 θ 及由此得到的 H-G 指数。
- 来源核对：[Erdős 1984 原文](https://www.renyi.hu/~p_erdos/1984-16.pdf)第末部分记录 G、H、条件性 n^{1+ε} 结论及“含多个素因子”问题。；[问题历史页](https://www.erdosproblems.com/history/879)核对了现列无条件界与 k=2 的已知情形。；旧候选对 H 为上界的朴素“给每个小素数收费 n”论证还会遇到 1、端点素数及重复收费细节；可解释数量级，但不足以独立重建严格的 G(n)<H(n)。
- 时间记账：所在批次墙钟时间按题数均摊约 52.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/879)；既有候选答案（按不可信材料审计）

### #881

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset\mathbb{N}$ be an additive basis of order $k$ which is minimal, in the sense that if $B\subset A$ is any infinite set then $A\backslash B$ is not a basis of order $k$. Must there exist an infinite $B\subset A$ such that $A\backslash B$ is a basis of order $k+1$?
- 题意摘要：按标准解释，k≥1，A⊂ℕ 是渐近加法基：每个充分大整数恰为 k 个 A 元素之和（允许重复）。假设对每个无限 B⊂A，A∖B 都不再是 k 阶渐近基。问是否存在某个无限 B⊂A，使 A∖B 成为 k+1 阶渐近基。
- 状态核对：仍为 open。局部 Lean 文件采用相同的渐近基解释，但形式量词写成所有 k:ℕ，包含非标准的 k=0，并以 answer(sorry) 包装，故不能视为已形式化解决。旧候选的 k=1 特例可以修正为严格证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先解决 k=1；再尝试通过逐步删除 b_j，同时为每个足够大整数保留一个 (k+1)-表示。检查最小性假设是否提供所需的表示冗余。
- 局部结论：k=1 时 A 必为余有限集。取 N_0 使 [N_0,∞)⊂A，保留 N_0,N_0+1，并在其后选无限 B⊂A 且相邻元素距离>1。令 C=A∖B。；对充分大 n，n-N_0 与 n-(N_0+1) 是相邻且均落在 A 中；B 至多含其一，故另一项属于 C，而 N_0 或 N_0+1 也属于 C。于是 n∈C+C，严格证明 k=1 时答案为是。；A 是 k 阶基必蕴含 A 是 k+1 阶基：固定 a_0∈A，对充分大 n，将 n-a_0 表成 k 项之和即可。但该论证在删除元素后不自动保留。
- 第一阻塞点：递归删除需要每个目标整数有避开新删元素的 (k+1)-表示；题设只说明任何无限删除会破坏 k 阶性质，完全不给表示数下界。甚至一个元素可能承担某一同余类的全部表示，因此第一步删除就可能破坏所有有限阶基。
- 下一步：研究附加引理：若每个 a∈A 都不是任何阶的 essential element，能否用对角法选无限 B，使 A∖B 仍为 k+1 阶基；若能，再检验题设的“无限删除最小性”是否迫使或允许消除 essential elements。
- 来源核对：[官方问题页](https://www.erdosproblems.com/881)仍列为 open，且未登记部分解。；本地形式化文件 [881.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/881.lean:23)核对了渐近基及无限删除量词；其中 theorem 仍含 sorry。；需注意旧候选所谓“k=1 时最小性自动成立”仅对余有限 A 正确：删除无限 B 后剩余不再余有限；其二阶构造则需明确把问题解释为渐近基。
- 时间记账：所在批次墙钟时间按题数均摊约 52.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/881)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/881.lean`；既有候选答案（按不可信材料审计）

### #883

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For $A\subseteq \{1,\ldots,n\}$ let $G(A)$ be the graph with vertex set $A$, where two integers are joined by an edge if they are coprime. Is it true that if\[\lvert A\rvert >\lfloor\tfrac{n}{2}\rfloor+\lfloor\tfrac{n}{3}\rfloor-\lfloor\tfrac{n}{6}\rfloor\]then $G(A)$ contains all odd cycles of length $\leq \frac{n}{3}+1$? Is it true that, for every $\ell\geq 1$, if $n$ is sufficiently large and\[\lvert A\rvert >\lfloor\tfrac{n}{2}\rfloor+\lfloor\tfrac{n}{3}\rfloor-\lfloor\tfrac{n}{6}\rfloor\]then $G(A)$ must contain a complete $(1,\ell,\ell)$ triparite graph on $2\ell+1$ vertices?
- 题意摘要：令 T(n)=⌊n/2⌋+⌊n/3⌋−⌊n/6⌋。第一问量词是：对每个 n 及每个 A⊆[n]，若 |A|>T(n)，则对每个奇整数 3≤r≤n/3+1，互素图 G(A) 含 C_r。第二问是：对每个固定 ℓ≥1，是否存在 N(ℓ)，使 n≥N(ℓ) 及同一密度条件推出 K_{1,ℓ,ℓ}。
- 状态核对：第一问仍开放；第二问已由 Sárközy 解决，且得到 ℓ≫log n/loglog n。旧候选写成 log n/logloglog n，与官方资料冲突，不能采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：取极值障碍 B={m≤n:2|m 或 3|m}，则 |B|=T(n)。由 |A|>|B| 得 |A\B|>|B\A|，故 A 中必有与 6 互素的顶点。尝试围绕这些“越界”顶点建立两个大互素邻接类，再用二部交替路径闭成奇圈；已知 K_{1,L,L} 定理正实现了这一路线的较弱版本。
- 局部结论：等号处 A=B 确实无三角形：三角形不可能完全落在偶数类或 3 的倍数类，而 6 的倍数与另外两类都不能同时互素，因此阈值严格性必要。；若 G(A) 含 K_{1,L,L}，则对每个 1≤r≤L 可取单点部顶点及两大部各 r 个顶点，得到 C_{2r+1}。故 Sárközy 定理直接给出长度至 ≫log n/loglog n 的全部奇圈。；Erdős–Sárközy 已给出某个绝对 c>0，使全部奇圈长度≤cn；因此困难不是获得线性范围，而是把常数严格推进到题设端点约 1/3。
- 第一阻塞点：第一处无法闭合的是：仅由 |A|−T(n)≥1，无法证明某个与 6 互素的顶点具有足够均匀的两个互素邻接类，更无法保证它们之间有长度约 n/3 的交替路径；现有定理的常数损失正发生在这种筛法—扩张估计中。
- 下一步：精确抽取 ErSa97 中决定 c 的筛法常数，逐项追踪损失，并检验是否能在目标长度 r≤n/3+1 时建立所需的二部路径扩张不等式。
- 来源核对：[官方 #883 页面](https://www.erdosproblems.com/883)确认第一问开放、第二问及 L≫log n/loglog n 的定量结论。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/883)；既有候选答案（按不可信材料审计）

### #884

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is it true that, for any $n$, if $d_1<\cdots <d_t$ are the divisors of $n$, then\[\sum_{1\leq i<j\leq t}\frac{1}{d_j-d_i} \ll 1+\sum_{1\leq i<t}\frac{1}{d_{i+1}-d_i},\]where the implied constant is absolute?
- 题意摘要：设 1=d₁<⋯<d_t=n 为 n 的全部正因子，P(n)=∑_{i<j}(d_j−d_i)^{-1}，S(n)=∑_{i<t}(d_{i+1}−d_i)^{-1}。原命题等价于存在绝对 C，使所有 n 都满足 P(n)≤C(1+S(n))；其否定是比值 P(n)/(1+S(n)) 无界。
- 状态核对：已无条件否证：官方页记载 Tao 在 Hardy–Littlewood 素数组猜想下否证，Larsen 随后无条件否证。旧候选称“无条件仍未解决”，现已过时。需特别说明：所给本地 884.lean 中 `erdos_884` 和条件定理均为 `by sorry`，所以该文件只有形式化陈述，不是本地可核验的无 sorry Lean 证书。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：重建反例所需的基本机制。记相邻间隙 g_k=d_{k+1}−d_k。由 Cauchy–Schwarz，1/(d_j−d_i)≤(∑_{k=i}^{j−1}1/g_k)/(j−i)²。对 i<j 求和，得到 P(n)≪(log t)S(n)。因此若能构造一长段近等距因子，同时不让其余相邻倒数和过大，便可使此对数因子真实出现；Tao 的近邻素数乘积构造及 Larsen 的无条件替代正沿此方向。
- 局部结论：上述求和中，一个固定 g_k^{-1} 的系数至多 ∑_{h≤t}h/h²=H_t，因此严格得到 P(n)≤H_t S(n)，至多差一个无关端点约定。；若有 M 个连续因子，其相邻间隙都在 [Δ,2Δ]，则该块对 P 的贡献 ≫M log M/Δ，而对 S 的贡献仅 ≍M/Δ；这是比值发散的具体局部模型。；官方状态确认存在无条件 n_m 使 P(n_m)/(1+S(n_m))→∞，故原绝对常数命题为假。
- 第一阻塞点：本次受限重建中第一处未独立闭合的是 Larsen 的核心无条件构造引理：须同时证明近等距因子块存在，并控制该块之外所有相邻因子对 S(n) 的贡献。仅有一般间隙不等式不能产生这种 n。
- 下一步：取得 Larsen 手稿正文后，把其核心构造拆成“因子块下界”和“全局相邻和上界”两个可计算命题；随后核对最新形式化仓库是否真有不含 `sorry` 的证明，而非仅有 `answer(False)` 陈述。
- 来源核对：[官方 #884 页面](https://www.erdosproblems.com/884)明确记为 DISPROVED，并指向 Larsen 无条件反例。；[Tao 的条件反例论文](https://terrytao.wordpress.com/wp-content/uploads/2025/09/erdos-884.pdf)给出近邻素数乘积机制及一般 P≪(log τ(n))S 上界。；本地 `FormalConjectures/ErdosProblems/884.lean` 的相关定理正文仍是 `by sorry`，不能充当内核验证证据。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/884)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/884.lean`；既有候选答案（按不可信材料审计）

### #885

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For integer $n\geq 1$ we define the factor difference set of $n$ by\[D(n) = \{\lvert a-b\rvert : n=ab\}.\]Is it true that, for every $k\geq 1$, there exist integers $N_1<\cdots<N_k$ such that\[\lvert \cap_i D(N_i)\rvert \geq k?\]
- 题意摘要：对每个整数 k≥1，要求存在严格递增的正整数 N₁<⋯<N_k，以及至少 k 个互异非负整数 d，使每个 d 对所有 i 都属于 D(N_i)；即每个 N_i 都有因子对差 d。
- 状态核对：一般 k 仍开放；已知 k≤4。形式化文件用含 k 个元素的 Finset 代替递增列，这是等价的，但所有研究定理仍为 `sorry`。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把因子差条件化为平方条件。若 b=a+d、N=ab，则 N=a(a+d)，等价于 4N+d²=(2a+d)²。因此问题可归约为寻找互异 N_i、d_j，使矩阵关系 y_{ij}²−d_j²=4N_i 对全部 i,j 成立。尝试通过固定 d_j，求多个平移后同时为平方的 N_i。
- 局部结论：严格等价式为 d∈D(N) ⇔ 存在整数 y>d、y≡d (mod 2)，使 y²−d²=4N。它同时编码正因子及奇偶条件。；旧候选的 k=2 例子正确：D(8)∩D(120)含 {2,7}。；旧候选的三元组也可逐项验算：1040、2660、5520 均对应因子差 32、67、256，因此确实给出 k=3 的实例。
- 第一阻塞点：第一处无法闭合的是从有限列推广到任意 k：加入一个新差 d 会要求所有既定 N_i+d²/4 同时为平方，形成越来越多的二次曲线交；没有参数化能同时保留 k 个 N_i 和 k 个差，直接迭代通常进入高亏格曲线。
- 下一步：固定已验证的 k=4 参数族，消元得到“加入第五个公共差”所对应的显式曲线；计算其亏格、局部可解性及有理点搜索，从而检验这条递推路线在 k=5 是否已经阻塞。
- 来源核对：[官方 #885 页面](https://www.erdosproblems.com/885)确认一般问题开放及 k=2,3,4 的已知结果。；本地 885.lean 的 Finset 量词与原递增列等价，但证明均为占位 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/885)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/885.lean`；既有候选答案（按不可信材料审计）

### #886

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\epsilon>0$. Is it true that, for all large $n$, the number of divisors of $n$ in $(n^{1/2},n^{1/2}+n^{1/2-\epsilon})$ is $O_\epsilon(1)$?
- 题意摘要：精确量词为：对每个固定 ε>0，存在只依赖 ε 的整数 K(ε) 和 N(ε)，使所有 n≥N(ε) 在开区间 (√n,√n+n^{1/2−ε}) 内至多有 K(ε) 个正因子。
- 状态核对：仍开放，但可直接证明 ε≥1/4 的范围；真正未决区间是 0<ε<1/4。旧候选援引 Letendre 得 ε>1/4，结论虽较弱地正确，但无需该新论文。另一个重要修正是：当前官方资料及 Lean 文件把“四个因子”例子的窗口写为 16n^{1/4}，不是 n^{1/4}。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令窗口长度 H=n^{1/2−ε}，写成 H=C_n n^{1/4}，其中 C_n=n^{1/4−ε}。应用 Erdős–Rosenfeld 的凸性估计：固定 C>0 时，充分大的 n 在 [√n,√n+C n^{1/4}] 内至多有 1+C² 个因子。
- 局部结论：若 ε≥1/4，则 C_n≤1；取固定 C=1，充分大 n 的因子数至多 2。因此该参数范围严格成立。；若 ε≥1/2，窗口长度≤1，开区间内至多含一个整数，故可取 K(ε)=1。；若 d>√n 且 d|n，令 e=n/d、r=d−e，则 r为正整数，(d+e)²−r²=4n，且 d−√n<r<2(d−√n)。因此短区间因子问题也可转写为短范围内平方判别式 4n+r²。
- 第一阻塞点：当 0<ε<1/4 时，C_n=n^{1/4−ε}→∞，凸性估计只给 1+C_n²=1+n^{1/2−2ε}，不再是 O_ε(1)。第一处缺口正是消除这个随 n 增长的 C_n² 因子。
- 下一步：利用 4n+r²=y² 表示，把三个以上近邻解之间的差分恒等式写出，检验能否证明 r 序列出现随解数超线性增长的高阶有限差分；若成立可突破单纯凸性界。
- 来源核对：[官方 #886 页面](https://www.erdosproblems.com/886)确认开放状态、1+C² 上界及 16n^{1/4} 的四因子例。；本地 886.lean 与当前官方页同样写明常数 16；输入中的旧 official_context 已被后续资料修正。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/886)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/886.lean`；既有候选答案（按不可信材料审计）

### #887

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an absolute constant $K$ such that, for every $C>0$, if $n$ is sufficiently large then $n$ has at most $K$ divisors in $(n^{1/2},n^{1/2}+C n^{1/4})$.
- 题意摘要：量词次序是 ∃绝对整数 K，∀C>0，∃N(C)，∀n≥N(C)，区间 (√n,√n+C n^{1/4}) 内的正因子数≤K。K 不得依赖 C，但起始点 N 可以依赖 C。
- 状态核对：一般情形仍开放。已知对每个固定 C 有上界 1+C²；平方 n 的情形有绝对上界 5。四因子构造说明任何候选 K 至少为 4。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把每个上方因子 d 配对到下方整数 e=n/d，得到双曲线 xy=n 上、距对角线 O(Cn^{1/4}) 的整点。Erdős–Rosenfeld 的凸性/整点面积论证给出点数≤1+C²；尝试检查其中 C² 是否可由乘积结构进一步压成绝对常数。
- 局部结论：固定 C 时已有严格结论 t≤1+C²，所以本题只差对 C 的一致性，而不是对每个窗口分别证明有界。；若 n为平方，Chan 的更大对称窗口 √n±n^{1/4}(log n)^{1/7} 内至多有 5 个因子；对每个固定 C，该窗口最终包含题设单侧窗口，故平方子族可取绝对 K=5。；已知无限多个 n 在 C=1 的窗口内有至少四个因子，因此若全局 K 存在，必有 K≥4。
- 第一阻塞点：凸性路线的第一处不可闭合步骤是将每一对相邻双曲线整点贡献的正整数行列式下界汇总时，所得可用总面积为 Θ(C²)；现有论证没有额外互素性或整除约束把允许的 Θ(C²) 个格点压到 O(1)。
- 下一步：枚举并符号化连续三个配对点 (d_i,n/d_i)，研究其 2×2 行列式之间因同一乘积 n 产生的整除关系；目标是证明只有 O(1) 个行列式可取小值，否则构造参数族以测试反例方向。
- 来源核对：[官方 #887 页面](https://www.erdosproblems.com/887)确认开放、1+C² 上界、四因子下界及 Chan 的平方情形结果。；本地 887.lean 正确表达 ∃K∀C∃N(C) 的量词次序，但各定理仍为 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 62.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/887)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/887.lean`；既有候选答案（按不可信材料审计）

### #888

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：What is the size of the largest $A\subseteq \{1,\ldots,n\}$ such that if $a\leq b\leq c\leq d\in A$ are such that $abcd$ is a square then $ad=bc$?
- 题意摘要：令 F(n) 为满足下述条件的 A⊆{1,…,n} 的最大基数：允许 a,b,c,d 重复，且对每个 a≤b≤c≤d∈A，若 abcd 为平方，则必须 ad=bc。已解决的是数量级 F(n)≍n log log n/log n，并非逐个 n 的精确公式。
- 状态核对：2026-05-28 的 solved 状态与官方页面一致。旧候选的精确公式错误：含≥7个互异素因子的某些元素还能加入，故“素数加平方自由半素数”并非极值。人工评审指出的平方核错误也确实致命：全局替换 x↦κ(x)既不保持大小次序，也不能推出所需等式；例如 {3,5,126,210} 的核集 {3,5,14,210} 会产生新的坏四元组。正确证明只在固定平方部分 k² 的层内约化。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建已知上下界。下界取全部素数和平方自由半素数。上界把每个 x 唯一写成 k²s，并对固定 k 考察平方自由层 A_k；随后将 s=cpq 按两个最大素因子 p,q 的二进尺度编码为以核 c 着色的二部图。刚性条件禁止同一个 C4 同时出现在两种颜色中，再用着色 Kővári–Sós–Turán 型估计求和。
- 局部结论：素数与平方自由半素数组成可行集：四个至多含两个素因子的平方自由数乘积为平方时，其支持形成四边欧拉多重图；除重边外只能形成四环，因而存在一对相对边乘积相等，排序后即 ad=bc。Landau 计数给出 F(n)≫n log log n/log n。；固定 k 后，A_k={s:k²s∈A} 保持次序和可行性，所以 F(n)≤∑_{k≤√n}G(⌊n/k²⌋)，其中 G 是平方自由情形的极值；这避开了旧候选的全局平方核错误。；若不同核 c≠d 的同一素数矩形 p,q×r,s 在两色中均完整，则 cpr,cqs,dps,dqr 的乘积为平方，而三种两两配对均不可能等积；排序后违反条件。因此每个 C4 至多属于一种颜色。
- 第一阻塞点：本次受限重建中，第一处未逐行复核的是对所有二进块求和的解析估计，特别是平方自由小核 c 的加权和界；公开证明用 Mertens/Chebyshev 型估计将三项分别控制为 O(n log log n/log n)、O(n/log n)、O(n/log n)。这是已有证明中的闭合步骤，而非问题仍开放。
- 下一步：逐行核验公开稿 Lemma 7.2 的小核加权和及端点范围，并把“固定平方部分分层”明确写入形式化版本；不要形式化错误的全局核映射。
- 来源核对：[官方问题页](https://www.erdosproblems.com/888)确认正确结论是 F(n)≍n log log n/log n。；[公开证明稿](https://www.ulam.ai/research/erdos888.pdf)给出固定平方部分约化、着色 C4 引理和二进求和。；[讨论页](https://www.erdosproblems.com/forum/thread/888)明确记录精确公式及全局平方核约化的反例。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/888)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/888.lean`；既有候选答案（按不可信材料审计）

### #889

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For $k\geq 0$ and $n\geq 1$ let $v(n,k)$ count the prime factors of $n+k$ which do not divide $n+i$ for $0\leq i<k$. Equivalently, $v(n,k)$ counts the number of prime factors of $n+k$ which are $>k$. Is it true that\[v_0(n)=\max_{k\geq 0}v(n,k)\to \infty\]as $n\to \infty$?
- 题意摘要：对每个 n≥1、k≥0，v(n,k) 是 n+k 的互异素因子中未整除任何 n+i（0≤i<k）者的数目；等价地，它计数 p>k 的素因子。问题问：对每个 R，是否存在 N_R，使所有 n≥N_R 都有某个 k≥0 满足 v(n,k)≥R？
- 状态核对：仍开放。旧候选正确区分了 limsup 无界、几乎处处增长与所问的全体 n 极限；后两者不能替代一致结论。官方记录的已知一致界仍仅为 n≥17 时 v_0(n)≥2。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试把问题归约为二项式系数的大素因子计数。固定 K，研究连续乘积 P_K(n)=∏_{j=0}^K(n+j)=K!·C(n+K,K)。
- 局部结论：若 p∣n+k 且 p∣n+i、i<k，则 p∣k−i，故 p≤k；反之若 p≤k 且 p∣n+k，取 i=k−p 即见 p 已出现。因此题述两个定义严格等价。；每个 p>K 至多整除区间 n,…,n+K 中的一项，故 ∑_{k=0}^K v(n,k)=ω_{>K}(P_K(n))=ω_{>K}(C(n+K,K))。；于是 v_0(n)≥ω_{>K}(C(n+K,K))/(K+1)。若能对每个固定 R、所有充分大 n 选择 K，使右侧≥R，原命题即得证。
- 第一阻塞点：需要一致地证明某个可选 K 下 C(n+K,K) 含至少 R(K+1) 个互异的、超过 K 的素因子。仅由该二项式系数很大不能推出互异素因子多，因为少数素数可带很高指数；现有初等估值不足以排除这种集中。
- 下一步：计算并制表 M_R(n)=max_K ω_{>K}(C(n+K,K))/(K+1) 的最坏 n，观察最佳 K 的尺度；理论上先检验能否用 p-adic 估值上界加 Chebyshev 函数得到随 R 增长的统一下界。
- 来源核对：[官方问题页](https://www.erdosproblems.com/889)确认开放状态、定义及 v_0(n)≥2（n≥17）。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/889)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/889.lean`；既有候选答案（按不可信材料审计）

### #890

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $\omega(n)$ counts the number of distinct prime factors of $n$, then is it true that, for every $k\geq 1$,\[\liminf_{n\to \infty}\sum_{0\leq i<k}\omega(n+i)\leq k+\pi(k)?\]Is it true that\[\limsup_{n\to \infty}\left(\sum_{0\leq i<k}\omega(n+i)\right) \frac{\log\log n}{\log n}=1?\]
- 题意摘要：按输入原文，固定每个 k≥1，令 S_k(n)=∑_{i=0}^{k-1}ω(n+i)。它同时询问 liminf S_k(n)≤k+π(k)，以及 limsup S_k(n)·log log n/log n=1。注意官方页面在 2026 年已把第一问更正为 ∑ω_k(n+i)，其中 ω_k 只数大于 k 的素因子。
- 状态核对：输入中的第一问不是开放命题，而是错误版本，可严格反驳；修正版仍开放。第二问对 k=1 是经典定理，对 k≥2 仍开放。因此该复合问题不能整体宣称解决。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：第一问直接按小素数对每个长度 k 区间的强制贡献计数；第二问用单项最大阶给出上下界，检查该路线能否达到常数 1。
- 局部结论：对每个素数 p≤k，任意 k 个连续整数中至少有 ⌊k/p⌋ 个被 p 整除，故 S_k(n)≥∑_{p≤k}⌊k/p⌋，对所有 n 成立。；取 k=26，右侧为 13+8+5+3+2+2+1+1+1=36，而 26+π(26)=35。因此输入第一问的答案为否。；设 L_k=limsup S_k(n)log log n/log n。由 S_k(n)≥ω(n)及 ω 的经典最大阶得 L_k≥1；逐项使用同一最大阶得 L_k≤k。该方法只给 1≤L_k≤k。
- 第一阻塞点：第二问要把上界常数从 k 降到 1，必须证明相邻 k 个整数不可能同时贡献接近各自最大阶的许多互异素因子。互素性只说明这些素因子大多不重叠，反而不能控制它们的总数；在此处路线停止。
- 下一步：后续应以更正后的第一问 ∑ω_k 为正式对象；对第二问先集中 k=2，研究 ω(n(n+1)) 的最大阶，尝试通过小素数分配及乘积大小建立严格小于 2 的常数界。
- 来源核对：[官方问题页](https://www.erdosproblems.com/890)明确说明原始 ω、k+π(k) 版本有误，并给出修正后的 ω_k 版本。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/890)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/890.lean`；既有候选答案（按不可信材料审计）

### #891

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $2=p_1<p_2<\cdots$ be the primes and $k\geq 2$. Is it true that, for all sufficiently large $n$, there must exist an integer in $[n,n+p_1\cdots p_k)$ with $>k$ many prime factors?
- 题意摘要：令 P_k=p_1⋯p_k，k≥2 固定；按官方上下文，“prime factors”指互异素因子。问题问是否存在 N_k，使每个 n≥N_k 的半开区间 [n,n+P_k) 都含某个 m 满足 ω(m)>k。若按重数 Ω 计数则结论平凡，但不是本题意图。
- 状态核对：仍开放，甚至 k=2、长度6时未知。旧候选关于 Ω 的旁支正确，但不能用于解决正式的 ω 版本。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：从区间中唯一的 P_k 倍数入手，设 m=P_kt，尝试证明若整个区间内均有 ω≤k，则 t 必须极端光滑，再利用邻项制造矛盾。
- 局部结论：每个长度 P_k 的半开区间恰含一个 P_k 的倍数 m。；若该区间是反例，则 ω(m)≤k；但 P_k 已含 k 个互异素数，所以 t=m/P_k 的所有素因子都属于 {p_1,…,p_k}，即 m 本身是 p_k-smooth。；特别地，k=2 的每个反例六元区间都必须含一个形如 2^a3^b 的6倍数；所以反例起点只能落在这些光滑数附近的有限六种相对位置。
- 第一阻塞点：Pólya 的光滑数间隙定理不能排除孤立的 2^a3^b 或一般 p_k-smooth 倍数附近出现坏区间；还需同时利用其余 P_k−1 个邻数的 ω≤k 条件。目前没有严格机制把这些邻项条件转化为不可能的 S-unit 方程组。
- 下一步：先做 k=2 的可检验任务：枚举每个 m=2^a3^b 附近六种区间位置，记录哪一个偏移 r 的 m+r 被迫含至少三个互异素因子；尝试把剩余无限族归约为有限组 S-unit 方程或覆盖同余类。
- 来源核对：[官方问题页](https://www.erdosproblems.com/891)确认 distinct-prime 解释、k=2 未知及 Schinzel 的加长区间结果。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/891)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/891.lean`；既有候选答案（按不可信材料审计）

### #892

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a necessary and sufficient condition for a sequence of integers $b_1<b_2<\cdots$ that ensures there exists a primitive sequence $a_1<a_2<\cdots$ (i.e. no element divides another) with $a_n \ll b_n$ for all $n$? In particular, is this always possible if there are no non-trivial solutions to $(b_i,b_j)=b_k$?
- 题意摘要：给定任意严格递增正整数列 b_n，要求刻画何时存在严格递增原始列 a_n（任意两项互不整除）和一个与 n 无关的常数 C，使 a_n≤Cb_n 对所有 n 成立。特别问：若方程 gcd(b_i,b_j)=b_k 没有“非平凡”解，是否总能做到。
- 状态核对：仍开放，且“非平凡”必须按原文约定排除由 k=i 或 k=j 等产生的平凡解；若连这些也禁止，则 b_n 本身已原始，取 a_n=b_n 即可。旧候选提及的额外充分性文献未在给定官方材料中得到核对，本筛查不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `medium`
- 尝试路线：先严格传递原始集的已知必要稀疏性，再尝试用素数列构造一个可验证的充分情形，最后检查 gcd 条件是否足以强迫该增长。
- 局部结论：若 a_n≤Cb_n，则 b_n≥a_n/C，因此 1/(b_n log b_n)≪1/(a_n log a_n)；原始集定理遂给出 ∑1/(b_n log b_n)<∞。；同理，b_n<x 蕴含 a_n<Cx 且 1/b_n≤C/a_n，所以原始集的倒数和估计推出 ∑_{b_n<x}1/b_n=o(log x/√log log x)。；存在一个简单充分区间：若 b_n≫n log n，则取 a_n 为第 n 个素数；由 p_n≍n log n 得 a_n≪b_n，且素数列原始。
- 第一阻塞点：要处理特别问，必须从三元 gcd-避免条件推出足够的全局稀疏性或直接构造匹配。该条件允许 gcd(b_i,b_j) 落在序列之外，也允许许多共享因子；目前无法严格推出 b_n≫n log n，亦无法证明每个尺度中有足够多可分配的互不整除整数。
- 下一步：定义 B(x) 为满足该 gcd-避免条件的 B⊆[2,x] 的最大规模，先用整数规划计算小 x 极值与结构；检验是否存在 B(x)≪x/log x 或至少官方两项必要倒数界。若这种有限极值已明显超出素数尺度，应转向 Hall 匹配而非第 n 个素数构造。
- 来源核对：[官方问题页](https://www.erdosproblems.com/892)确认开放状态及两项必要条件，并未给出一般充分条件。
- 时间记账：所在批次墙钟时间按题数均摊约 59.4 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/892)；既有候选答案（按不可信材料审计）

### #893

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $\tau(n)$ counts the divisors of $n$ then let\[f(n)=\sum_{1\leq k\leq n}\tau(2^k-1).\]Does $f(2n)/f(n)$ tend to a limit?
- 题意摘要：令 \(f(n)=\sum_{1\le k\le n}\tau(2^k-1)\)。问题询问实数序列 \(f(2n)/f(n)\) 是否收敛；现已知它无上界，故不可能趋于有限实数，但是否趋于扩展实数 \(+\infty\) 仍未解决。
- 状态核对：截至核对到的 arXiv v4（2026-02-03），Kovač–Luca 无条件证明 \(\limsup f(2n)/f(n)=\infty\)，而整体趋于 \(+\infty\) 仍为有条件结论。旧候选结论正确，但“较小函数的倍增比趋于无穷直接强迫原比值出现尖峰”不是充分论证；正确桥梁是反设原比值一致有界后作二进迭代。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建无界性反证。Bang–Zsigmondy 对每个 \(d\mid k\)、除 \(d=1,6\) 外给出 \(2^k-1\) 的不同原始素因子，因此先建立单项下界；再假设 \(f(2n)\le C f(n)\)，沿 \(n=2^j\) 迭代，并在二进区间内选高度合成指标制造超过任意指数函数的单项。
- 局部结论：原始素因子互异，故 \(\omega(2^k-1)\ge \tau(k)-2\)，从而 \(\tau(2^k-1)\ge 2^{\omega(2^k-1)}\ge 2^{\tau(k)-2}\)。；若从某处起 \(f(2n)/f(n)\le C\)，则迭代给出 \(f(2^j)\le C_0C^j\)。；取不超过 \(2^j\) 的最大高度合成数 \(N_j\)；记录值性质给出 \(N_j>2^{j-1}\)，且经典最大除数阶估计使 \(2^{\tau(N_j)-2}\) 比 \(C^j\) 增长更快。结合第一条与 \(f(2^j)\ge\tau(2^{N_j}-1)\) 得到矛盾，因此该比值无界。
- 第一阻塞点：无界只保证任意高的子序列峰值，不能排除峰值之间反复降回有界区间；现有下界没有控制分母 \(f(n)\) 或相邻记录峰之间的间距和衰减。
- 下一步：检验论文的具体充分条件：枚举“记录型 Mersenne 指标” \(N\)，计算 \(\tau(2^N+1)/N\)，并尝试证明该量沿所有记录指标趋于无穷；这会通过 \(2^{2N}-1=(2^N-1)(2^N+1)\) 闭合整体发散路线。
- 来源核对：[Kovač–Luca, arXiv:2506.04883 v4](https://arxiv.org/abs/2506.04883)：摘要及 Corollary 2 明确给出无界性，整体发散仅为有条件结论。；本地 Lean 文件把“趋于 \(+\infty\)”列为 research open，把无界变体列为 research solved；与论文状态一致。
- 时间记账：所在批次墙钟时间按题数均摊约 51.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/893)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/893.lean`；既有候选答案（按不可信材料审计）

### #896

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Estimate the maximum of $F(A,B)$ as $A,B$ range over all subsets of $\{1,\ldots,N\}$, where $F(A,B)$ counts the number of $m$ such that $m=ab$ has exactly one solution (with $a\in A$ and $b\in B$).
- 题意摘要：对任意 \(A,B\subseteq[1,N]\)，令 \(r_{A,B}(m)=|\{(a,b)\in A\times B:ab=m\}|\)，并令 \(F(A,B)=|\{m:r_{A,B}(m)=1\}|\)。目标是估计 \(M(N)=\max_{A,B}F(A,B)\)。表示按有序角色 \(A\times B\) 计数。
- 状态核对：按给定 cohort 的 solved 状态重建现有两侧估计；这里“solved”并不表示已知精确渐近式，两界之间仍有较大对数间隙。旧候选的上下界路线可严格成立。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `5/10`；置信度 `high`
- 尝试路线：下界取大素数集合 \(A\)，并从 \(B\) 排除所有含这些素因子的整数，以强制乘积表示唯一；上界把唯一表示乘积注入 \(N\times N\) 乘法表的不同条目集合，再调用 Ford 的乘法表数量级。
- 局部结论：取 \(A=\{p\text{ prime}:N/\log N\le p\le N\}\)，则素数定理给出 \(|A|=(1+o(1))N/\log N\)。若 \(B\) 是不被任何 \(p\in A\) 整除的 \(b\le N\)，则 \(N\sum_{p\in A}1/p=o(N)\)，故 \(|B|=(1+o(1))N\)。；若 \(pb=p'b'\) 且 \(p\ne p'\)，则素数性迫使 \(p\mid b'\)，与 \(b'\in B\) 矛盾。因此全部 \(|A||B|\) 对应不同且唯一的乘积，给出 \(M(N)\ge(1+o(1))N^2/\log N\)。；每个被 \(F\) 计数的 \(m\) 都是乘法表中的不同条目，故 \(F(A,B)\le|\{ab:a,b\le N\}|\)。Ford 的定理遂给出 \(M(N)\ll N^2/((\log N)^\delta(\log\log N)^{3/2})\)，其中 \(\delta=1-(1+\log\log2)/\log2\)。
- 第一阻塞点：乘法表上界完全丢掉了“恰有一个来自 \(A\times B\) 的表示”这一额外结构；现有路线不能把 Ford 上界降到下界的 \(N^2/\log N\) 量级。
- 下一步：研究对固定 \(A,B\) 的能量 \(E(A,B)=\sum_m r_{A,B}(m)^2\)，尝试把大量乘法表条目具有多个因子分解这一事实转化为 \(|\{m:r(m)=1\}|\) 的更强上界；第一项可检验任务是对分 dyadic 因子区间的 \(r(m)\) 建立二阶矩界。
- 来源核对：[Ford, Annals of Mathematics 168 (2008)](https://annals.math.princeton.edu/2008/168-2/p01)：给出区间因子分布结果，包含经典乘法表问题所需数量级。；下界构造已逐项独立核对；它不依赖把官方评论本身当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 51.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/896)；既有候选答案（按不可信材料审计）

### #901

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $m(n)$ be minimal such that there is an $n$-uniform hypergraph with $m(n)$ edges which is $3$-chromatic. Estimate $m(n)$.
- 题意摘要：\(m(n)\) 是所有有限 \(n\)-一致超图中，色数恰为 \(3\) 者的最少边数。等价地，可先最小化没有 Property B（不存在使每条边双色的红蓝染色）的边数。
- 状态核对：问题仍开放。当前一般渐近界为 \(\Omega(2^n\sqrt{n/\log n})\le m(n)\le O(n^22^n)\)；猜测量级为 \(n2^n\)。旧候选的主界与一手来源一致。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先严格核对“3-色”与“非2-可染”的等价化；随后分别尝试最基本的随机染色下界，以及在 \(v\asymp n^2\) 个顶点上随机抽边的上界。
- 局部结论：从边数最少的非2-可染超图 \(H\) 删除一边 \(e\)，所得超图可2-染；在该染色中 \(e\) 必为单色。把 \(e\) 的一个顶点改成第三色，不会使其他边变成单色，所以 \(\chi(H)=3\)。因此两种极值定义确实相同。；随机独立红蓝染色中，每条 \(n\)-边单色的概率为 \(2^{1-n}\)。若边数 \(m<2^{n-1}\)，单色边期望小于1，故存在适当2-染色；于是 \(m(n)\ge2^{n-1}\)。；取 \(v\asymp n^2\)。对任一顶点二染色，单色 \(n\)-子集所占比例在平衡染色处最小，且为 \(\Omega(2^{-n})\)。独立抽取 \(C n^22^n\) 条边后，该染色全部合格的概率至多 \(e^{-cCn^2}\)；对至多 \(2^v\) 个染色作并合界，取足够大 \(C\) 即得到非2-可染超图，重建 \(m(n)=O(n^22^n)\)。
- 第一阻塞点：简单期望法只产生 \(2^{n-1}\)；要得到最佳下界，必须严格分析依赖的单色边事件及重染过程。这里尚未重建 Radhakrishnan–Srinivasan 算法中产生 \(\sqrt{n/\log n}\) 增益的坏事件计数。
- 下一步：选定该随机重染算法的阈值参数，逐类列出“初始单色边、危险边、重染冲突”事件，并验证其总失败概率在 \(m\le c2^n\sqrt{n/\log n}\) 时小于1。
- 来源核对：[Radhakrishnan–Srinivasan, RSA 2000](https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291098-2418%28200001%2916%3A1%3C4%3A%3AAID-RSA2%3E3.0.CO%3B2-2)：论文摘要确认其改进 Beck 下界及2-染色算法。；[Grill–Linzmayer, arXiv:2403.05674](https://arxiv.org/abs/2403.05674)：确认截至该文一般最佳渐近下界和仍未改进的 \(O(n^22^n)\) 上界。
- 时间记账：所在批次墙钟时间按题数均摊约 51.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/901)；既有候选答案（按不可信材料审计）

### #902

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be minimal such that there is a tournament (a complete directed graph) on $f(n)$ vertices such that every set of $n$ vertices is dominated by at least one other vertex. Estimate $f(n)$.
- 题意摘要：定义顶点 \(x\notin S\)“支配”集合 \(S\) 为 \(x\to s\) 对所有 \(s\in S\) 成立。\(f(n)\) 是存在一个 \(N\)-顶点锦标赛、使每个恰含 \(n\) 个顶点的集合都有至少一个外部支配者时的最小 \(N\)。
- 状态核对：问题开放。经典量级夹在 \(\Omega(n2^n)\) 与 \(O(n^22^n)\) 之间。旧候选所写更精确下界 \((n+2)2^{n-1}-1\) 与官方的 \(n2^n\ll f(n)\) 相容，但其中“短的双重支配矛盾”未展开，不能视为已核验；本次只闭合较弱的 \(2^{n+1}-1\) 归纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：上界使用随机锦标赛和对所有 \(n\)-集的并合界；下界考察任意顶点的入邻域所诱导的锦标赛，把性质从 \(n\) 递降到 \(n-1\)。
- 局部结论：固定 \(n\)-集 \(S\) 无支配者的概率为 \((1-2^{-n})^{N-n}\)。因此失败概率至多 \(\binom Nn(1-2^{-n})^{N-n}\)；取 \(N=(\log2+o(1))n^22^n\) 即使其小于1，得到该常数级随机上界。；若锦标赛具有性质 \(S_n\)，对任一顶点 \(v\)，其入邻域 \(I(v)=\{x:x\to v\}\) 的诱导锦标赛具有 \(S_{n-1}\)：对 \(A\subset I(v)\)、\(|A|=n-1\)，支配 \(A\cup\{v\}\) 的顶点仍在 \(I(v)\)。；故每个顶点入度至少 \(f(n-1)\)。平均入度为 \((N-1)/2\)，所以 \(f(n)\ge2f(n-1)+1\)；由 \(f(1)=3\) 得 \(f(n)\ge2^{n+1}-1\)。
- 第一阻塞点：该单顶点入邻域归纳每层只贡献因子2，不能产生额外的线性因子 \(n\)。旧候选声称的加强性质 \(S(n,1)\Rightarrow S(n-1,n+1)\) 未给出证明，本次无法严格闭合。
- 下一步：直接重建 Szekeres–Szekeres 的加强引理：对固定 \((n-1)\)-集 \(A\)，分析其共同支配者集合的内部锦标赛，证明其大小的必要下界；先在 \(n=2,3\) 上穷举检查候选常数 \(n+1\) 是否准确，再写归纳。
- 来源核对：[Erdős Problems #902](https://www.erdosproblems.com/latex/902) 明列 \(2^{n+1}-1\le f(n)\ll n^22^n\) 及 Szekeres–Szekeres 的 \(n2^n\ll f(n)\)。；随机上界和较弱递归下界均已独立逐式核对，不依赖旧候选未展开的加强引理。
- 时间记账：所在批次墙钟时间按题数均摊约 51.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/902)；既有候选答案（按不可信材料审计）

### #906

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an entire non-zero function $f:\mathbb{C}\to \mathbb{C}$ such that, for any infinite sequence $n_1<n_2<\cdots$, the set\[\{ z: f^{(n_k)}(z)=0 \textrm{ for some }k\geq 1\}\]is everywhere dense?
- 题意摘要：字面陈述只要求非零整函数 \(f\)；但本地形式化及官方语境实际要求超越整函数。对每个严格递增 \((n_k)\)，要求 \(\bigcup_k Z(f^{(n_k)})\) 在 \(\mathbb C\) 稠密。
- 状态核对：字面版本被任一非零多项式平凡肯定解决：高阶导数恒为零。人工评审已指出这只是网站已注明的退化解，不能回答推定的超越版本；旧候选不得作为开放题解答复述。本地 Lean 明确加入了 `Transcendental`，故真正筛查对象应是该加强版本。Barth–Schneider 1972 的量词不同，不能直接引用为解。
- 初步判定：`partial`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `high`
- 尝试路线：先把“任意无限子序列”转化为逐圆盘的余有限条件，再尝试用多项式逐块逼近构造超越整函数：第 \(j\) 阶段令一段新的导数阶数分别在前 \(j\) 个有理圆盘中出现简单零，并要求以后扰动在相应圆周上足够小，以由 Rouché 定理保存这些零。
- 局部结论：对任一非空开圆盘 \(U\)，令 \(A_U=\{n:Z(f^{(n)})\cap U\ne\varnothing\}\)。原条件等价于每个 \(A_U\) 余有限：若补集无限，取其严格递增枚举即反例；反之任一无限序列都最终落入 \(A_U\)。只需检查可数有理圆盘基。；若不要求超越性，任一非零多项式 \(P\) 都成立，因为 \(P^{(n)}\equiv0\) 对所有 \(n>\deg P\)。这也说明题面缺失超越条件会使问题退化。；若能证明有限阶段插值引理——在给定紧圆盘上任意小地扰动，同时让指定有限段的每个导数在指定有限组圆盘各有简单零——则可用对角过程得到整函数极限；额外安排无穷多个非零 Taylor 系数即可保证超越性。
- 第一阻塞点：所需有限阶段插值引理尚未证明：同一个高次扰动的多个连续导数必须同时满足许多零条件，同时又要在旧紧集上极小。Barth–Schneider 只是在给定离散集合上为某些由构造选择的导数阶插零，量词不足以保证“每个充分大的阶数、每个圆盘”。
- 下一步：先处理单圆盘有限段版本：给定圆盘 \(U\)、整数区间 \([L,M]\)、紧集 \(K\) 与 \(\varepsilon>0\)，检验是否存在多项式 \(Q\) 满足 \(\sup_K|Q|<\varepsilon\)，且每个 \(Q^{(n)}\)（\(L\le n\le M\)）在 \(U\) 有简单零；成功后再研究多圆盘同步及对角稳定性。
- 来源核对：本地 `906.lean` 明确要求 `Transcendental (Polynomial ℂ) f`，排除了多项式退化解。；[Barth–Schneider 1972 的可查摘要](https://www.researchgate.net/publication/238868008_On_a_Problem_of_Erdos_Concerning_the_Zeros_of_the_Derivatives_of_an_Entire_Function) 陈述的是：对离散集列 \(S_k\)，存在阶数列 \(n_k\) 与超越整函数使 \(f^{(n_k)}\) 在 \(S_k\) 消失；这不是本题的全称子序列性质。；Erdős Problems 的相关 Problem 229 也把 Barth–Schneider 的结果表述为上述较弱量词结构，支持“不能直接套用”的判断。
- 时间记账：所在批次墙钟时间按题数均摊约 51.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/906)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/906.lean`；既有候选答案（按不可信材料审计）

### #911

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\hat{R}(G)$ denote the size Ramsey number, the minimal number of edges $m$ such that there is a graph $H$ with $m$ edges that is Ramsey for $G$. Is there a function $f$ such that $f(x)/x\to \infty$ as $x\to \infty$ such that, for all large $C$, if $G$ is a graph with $n$ vertices and $e\geq Cn$ edges then\[\hat{R}(G) > f(C) e?\]
- 题意摘要：问是否存在函数 f（与 G、n 无关），满足 f(C)/C→∞，且对所有充分大的 C 及每个有限图 G（v(G)=n，e(G)=e≥Cn），都有二色 size-Ramsey 数 \hat R(G)>f(C)e。
- 状态核对：截至核查时官方仍列为 open。旧候选的最小度核归约本身正确，但把它称为问题的“核心等价形式”不正确：该归约不能保留与原图边数 e 可比的分母。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试删去度数 <C 的顶点，得到 C-core G'。若删去 r 个顶点，则删去的边数 <Cr，故剩余非空且 e(G')>e-Cr≥C(n-r)，从而 δ(G')≥C。又因 G'⊆G，单调性给出 \hat R(G)≥\hat R(G')。
- 局部结论：任何满足 e(G)≥Cn 的图都含有非空子图 G'，满足 δ(G')≥C 且 e(G')≥C|V(G')|。；若主图 H 的边数少于 2e(G)-1，可把其边近乎均分为红蓝两色，使两色均少于 e(G) 条边；故 \hat R(G)≥2e(G)-1。；核心可能损失 Θ(C) 的边数比例：取约 3C 个顶点组成团，并加入 Θ(C²) 个各连接 C-1 个核心顶点的外围点，可保持 e≥Cv，而删核过程会去掉外围点贡献的 Θ(C³) 条边，只留下 Θ(C²) 条核心边。
- 第一阻塞点：由 \hat R(G') 的下界只能得到相对于 e(G') 的估计；由于 e(G')/e(G) 可为 O(1/C)，不能推出所需的 \hat R(G)>f(C)e(G)。这正是该路线第一处断裂。旧候选引用的 Δ(G)τ(G)/2 下界即使成立，也至多给常数倍 e，不能修复这一损失。
- 下一步：检验能否证明一个“多核”版本：从任意 e≥Cn 的 G 中抽取边不交子图 G_j，使 Σe(G_j)≥c e，并且每个 δ(G_j)≥cC；若成立，再研究 size-Ramsey 下界能否对这些子图作可加聚合。
- 来源核对：[Erdős Problem 911 官方题页](https://www.erdosproblems.com/911)仍标为 open，且未登记部分解。；独立核对了删点过程、size-Ramsey 单调方向以及分母损失；未采用旧候选中未经本轮来源核实的完全二部图数量级断言。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/911)；既有候选答案（按不可信材料审计）

### #912

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If\[n! = \prod_i p_i^{k_i}\]is the factorisation into distinct primes then let $h(n)$ count the number of distinct exponents $k_i$. Prove that there exists some $c>0$ such that\[h(n) \sim c \left(\frac{n}{\log n}\right)^{1/2}\]as $n\to \infty$.
- 题意摘要：对每个 n，将 n! 中各素因子的正指数 v_p(n!) 收集成集合，h(n) 是该集合的基数。要求证明存在与 n 无关的常数 c>0，使 h(n)/(n/\log n)^{1/2}→c。
- 状态核对：仍为 open；已知 Erdős–Selfridge 只证明 h(n)\asymp\sqrt{n/\log n}，Cramér–Poisson 启发预测 c=\sqrt{2\pi}。本地 Lean 文件也把 Θ 结论列为 solved、渐近等价列为 open。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：令 K=\sqrt{n/\log n}。对 p>\sqrt n，Legendre 公式化为 v_p(n!)=⌊n/p⌋；因此 k 出现当且仅当区间 I_k=(n/(k+1),n/k] 含素数。把 k 按 k/K 缩放，尝试证明固定窗口 εK≤k≤MK 内的占用指标具有确定极限。
- 局部结论：设 B_n={⌊n/p⌋:p>√n 为素数}，则 |h(n)-|B_n||≤π(√n)=o(K)。这里差值只来自 p≤√n 的指数，允许与 B_n 重合。；小端 k<εK 至多贡献 εK 个值；大端 k>MK 的占用数至多 π(n/(MK))=O(K/M)。因此先令 n→∞、再令 ε↓0、M↑∞，两端均可忽略。；在 Cramér 模型中，k=tK 时 |I_k|/\log(n/k)→2/t²，故占用概率预测为 1-e^{-2/t²}；积分 ∫₀^∞(1-e^{-2/t²})dt=√(2π)。这只是启发，不是证明。
- 第一阻塞点：第一处无法闭合的是固定临界窗口内的均匀占用渐近：需要控制长度约为平均素数间距的移动区间 I_k 是否含素数，并足够精确地处理相关性。PNT、通常短区间定理或有限阶筛估计均不给出所需 Poisson 空区间概率。旧候选的下界段还调用了未精确陈述的素数近对筛估计；这可支持已知 \asymp 结果，但不能当作所求渐近的证明。
- 下一步：对固定 0<ε<M，尝试证明各阶阶乘矩 Σ_{εK≤k≤MK}(π(I_k))_r 的统一渐近，并明确所需 Hardy–Littlewood 素数元组输入；先检查 r=1、2 是否能无条件达到足够误差。
- 来源核对：[Erdős Problem 912 官方题页](https://www.erdosproblems.com/912)明确记录 open、已知 Θ 级结果及 c=√(2π) 的启发。；[本地 Lean 陈述](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/912.lean)与自然语言主命题一致。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/912)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/912.lean`；既有候选答案（按不可信材料审计）

### #913

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many $n$ such that if\[n(n+1) = \prod_i p_i^{k_i}\]is the factorisation into distinct primes then all exponents $k_i$ are distinct?
- 题意摘要：问是否有无穷多个 n∈ℕ，使映射 p↦v_p(n(n+1)) 在所有整除 n(n+1) 的素数上单射；即全部出现的正指数两两不同。因 gcd(n,n+1)=1，这同时要求 n 与 n+1 内部无重复指数，且两者的指数集合互不相交。
- 状态核对：官方仍列为 open。旧候选给出的 Mersenne 素数条件是正确但更强的条件路线；官方建议的 8p²-1 路线更直接，并已在本地 Lean 文件中形式化为条件定理。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：取奇素数 p，并假设 q=8p²-1 也是素数，令 n=q。则 n+1=8p²=2³p²，而 q、p、2 两两不同，所以 n(n+1)=q¹p²2³，指数恰为 {1,2,3}。
- 局部结论：每个满足 p 与 8p²-1 均为素数的奇素数 p 都产生一个合格的 n=8p²-1。；映射 p↦8p²-1 严格递增，故若这样的 p 有无穷多个，就得到无穷多个不同的 n。；素数对多项式 x 与 8x²-1 没有固定素因子这一显然局部障碍；因此该条件与 Bateman–Horn 型启发相容，但这不构成无穷性证明。
- 第一阻塞点：必须证明无穷多个素数 p 使二次值 8p²-1 同时为素数；这是二维素数值问题，现有筛法的奇偶障碍阻止把“几乎素数”提升为素数。旧候选提到一般“special numbers”的密度并不能控制相邻整数，因此不推进此断点。
- 下一步：对多项式族 {x,8x²-1} 明确计算局部根数与 Bateman–Horn 奇异乘积，并用 Selberg 筛严格证明候选对数的 O(X/(log X)²) 上界；这可检验局部可容许性及预期尺度，但不会误称解决无穷性。
- 来源核对：[Erdős Problem 913 官方题页](https://www.erdosproblems.com/913)记录该条件构造并仍标为 open。；[本地 Lean 文件中的 conditional 定理](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/913.lean)严格实现了此归约；其中排除 p=2 后得到指数 1、2、3。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/913)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/913.lean`；既有候选答案（按不可信材料审计）

### #917

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 4$ and $f_k(n)$ be the largest number of edges in a graph on $n$ vertices which has chromatic number $k$ and is critical (i.e. deleting any edge reduces the chromatic number). Is it true that\[f_k(n) \gg_k n^2?\]Is it true that\[f_6(n)\sim n^2/4?\]More generally, is it true that, for $k\geq 6$,\[f_k(n) \sim \frac{1}{2}\left(1-\frac{1}{\lfloor k/3\rfloor}\right)n^2?\]
- 题意摘要：固定 k≥4，f_k(n) 是所有 n 顶点、χ(G)=k、且对每条边 e 都有 χ(G-e)<k 的图中最大边数。题目含三问：是否对每个固定 k 有 f_k(n)≥c_kn²；是否 f_6(n)∼n²/4；以及对所有 k≥6 是否具有给定的统一渐近常数。
- 状态核对：这是混合状态：第一问 Toft 已证为真；第二问仍开放；第三问在 k≡1,2 mod 3 时已被 Stiebitz 反例否定，在 k≡0 mod 3 时仍开放。因此不能笼统称整题“open”。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `7/10`；置信度 `high`
- 尝试路线：重建 k=3r 的 Dirac–Erdős 构造。取 r 个长度同为奇数 m 的环并作完全 join。join 的色数可加，故 χ=3r；逐类检查内部边和跨部边删除后均可用 3r-1 色着色。
- 局部结论：删去某个环内边后，该奇环变成二部路径，该部分色数由 3 降为 2；故内部边临界。删去跨环边 uv 后，分别给两个奇环作“指定顶点独占第三色”的三染色，并让 u、v 共用该色，其余色盘分离；故跨边也临界。；总顶点数 N=rm，边数为 C(r,2)m²+rm=½(1-1/r)N²+N。对 k=6 即 r=2，得到 f_6(N)≥N²/4+N；加入孤立点可把该下界以 O(N) 损失推广到所有充分大的 N。；Stiebitz 对 k≢0 mod 3 的无穷子序列给出严格更大的二次系数，因此足以反驳所提渐近；这不是仅仅“尚无上界”。
- 第一阻塞点：对 k=6，构造只证明 liminf f_6(n)/n²≥1/4；缺少把任意 6-色边临界图压到 (1/4+o(1))n² 的结构定理。现有一般上界仍明显大于 1/4。
- 下一步：针对 k=6 检验一个稳定性命题：若边临界 6-色图有 ≥(1/4+ε)n² 条边，是否必含可迫使某条边非临界的四部稠密结构；先用正则化把问题归约到有限 reduced graph，并枚举其允许的临界着色模式。
- 来源核对：[Erdős Problem 917 官方题页](https://www.erdosproblems.com/917)记录 Toft 定理、Dirac 构造、Stiebitz 反例及 Luo–Ma–Yang 上界。；独立核算了 join 构造的色数、逐边临界性和边数公式；旧候选给出的 k=6 上界系数 337/900 与官方公式相符。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/917)；既有候选答案（按不可信材料审计）

### #918

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a graph with $\aleph_2$ vertices and chromatic number $\aleph_2$ such that every subgraph on $\aleph_1$ vertices has chromatic number $\leq\aleph_0$? Is there a graph with $\aleph_{\omega+1}$ vertices and chromatic number $\aleph_1$ such that every subgraph on $\aleph_\omega$ vertices has chromatic number $\leq\aleph_0$?
- 题意摘要：第一问要求一个大小及色数均为 ℵ₂ 的图，而每个恰有 ℵ₁ 个顶点的子图均可数着色。第二问要求大小 ℵ_{ω+1}、色数 ℵ₁，且每个恰有 ℵ_ω 个顶点的子图均可数着色。这里 ω 是第一无限序数。对“≤ℵ₀”，检查诱导子图即可，因为任意同顶点集子图的色数不超过诱导子图。
- 状态核对：第一问在大基数相对一致性意义下独立：L 中有正例，而 Foreman–Laver 给出与 GCH 相容的无例模型。第二问在 L 等满足 CH_{ℵω}+□_{ℵω} 的模型中有正例，但相应可数界紧致性的负模型是否一致仍未解决，故不能把第二问也宣称已独立。
- 初步判定：`independent`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：采用非紧致性机制而非尝试 ZFC 构造：用 coherent C-sequence/□ 构造大图，使全图的捕获性质迫使高色数，而每个真小子图只接触 C-sequence 的有界初段，从而可数着色；反方向使用大基数强迫得到向下反射，排除第一类图。
- 局部结论：“恰有 ℵ₁（或 ℵω）顶点的子图可数着色”自动推出所有更小子图可数着色：把顶点集扩充到指定基数后限制其可数着色即可。因此第一问正是 E(ℵ₀,ℵ₂)。；在 V=L 中，每个正则非弱紧 κ 都有大小 κ 的 (ℵ₀,κ)-chromatic 图；取 κ=ℵ₂ 得第一问正例。相对大基数，Foreman–Laver 模型中不存在这种图，给出第一问的相对独立性机制。；若 λ=ℵω 满足 2^λ=λ⁺ 与 □_λ，Rinot 的定理对 μ=ℵ₁ 给出大小 λ⁺ 的 (ℵ₀,μ)-chromatic 图，因而满足第二问；特别地 L 中为真。
- 第一阻塞点：第二问若要得到相对独立性，还需构造一个模型，使“所有 ℵω 大小子图可数着色”推出全图可数着色。已知 Shelah 紧致性模型只处理上界 ℵ_n（1≤n<ω）；文献明确指出 n=0 即可数界仍开放。这是第一处不能闭合之处。
- 下一步：把第二问精确改写为 ℵ_{ω+1} 处的 n=0 色数反射，并核查较新的紧致性文献是否已解决 Shelah 1990 留下的 n=0 情形；若未解决，则尝试分析现有大基数迭代中哪一步依赖 n≥1。另应修正本地 Lean 陈述：它写成“∀序数 ω”的全局命题，而非固定第一无限序数 ω。
- 来源核对：[Erdős Problem 918 官方题页](https://www.erdosproblems.com/918)仍把组合问题列为 open。；[Lambie-Hanson–Rinot, Reflection on the coloring and chromatic numbers](https://arxiv.org/abs/1708.06929)的 Definition 1.3、Results 2.1–2.2 记录了 L 中正例、Foreman–Laver 负模型、Rinot 的 □+CH 构造及 n=0 未决点。；[本地 Lean 陈述](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/918.lean)的第二部分错误地量化所有 Ordinal ω，强于原题且不忠实。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/918)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/918.lean`；既有候选答案（按不可信材料审计）

### #919

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a graph $G$ with vertex set $\omega_2^2$ and chromatic number $\aleph_2$ such that every subgraph whose vertices have a lesser type has chromatic number $\leq \aleph_0$? What if instead we ask for $G$ to have chromatic number $\aleph_1$?
- 题意摘要：把顶点集理解为序数积 $V=\omega_2\cdot\omega_2$，带其自然良序。要求存在图 $G$，使 $\chi(G)=\aleph_2$（第二问改为 $\aleph_1$），且对每个 $A\subseteq V$，只要 $\operatorname{otp}(A)<\omega_2^2$，就有 $\chi(G[A])\le\aleph_0$。这里限制的是序型，不只是基数，也不只限于初始段。
- 状态核对：截至核对日官方仍列 OPEN。先前候选把第二坐标不等号反向称为“等价”，这是错误的：良序 $\omega_1$ 没有全局逆序同构。官方背景中按“两坐标同向递增”直读的图也不能满足小序型条件，因为对角线已经给出反例；因此不能把那段文字直接当作目标性质的证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `medium`
- 尝试路线：尝试用分块过滤 $V=\bigcup_{\xi<\omega_2}B_\xi$，其中 $B_\xi=\omega_2\cdot\xi$，逐段构造相容的可数着色。假设目标图存在，则每个 $G[B_\xi]$ 都可数着色；若能把这些着色沿 $\omega_2$ 长链相容化，便会推出整个图可数着色，从而否定两种目标。
- 局部结论：目标性质确实推出每个真初始段 $B_\xi$ 可数着色，且推出每一行以及少于 $\omega_2$ 行的任意较小序型并集可数着色。；对背景中同向图 $H$，集合 $D=\{(\alpha,\alpha):\alpha<\omega_2\}$ 的序型为 $\omega_2<\omega_2^2$，而 $H[D]$ 是 $K_{\omega_2}$；故该直接类比至多证明 $\chi(H)=\aleph_2$，绝不满足题目的可数局部条件。；即使每个 $B_\xi$ 有某个可数着色，也不能自动选成相容系统；限制一个后期着色未必等于先前选定着色。
- 第一阻塞点：第一处无法闭合的是“局部可数着色的相容化”。在长度 $\omega_2$ 的极限阶段，没有紧致性原理保证可数色着色能同时延拓；这正是可能产生非反射色数的地方。
- 下一步：把问题编码为着色空间的逆系统：对 $\xi<\eta$ 研究 $\mathrm{Col}_\omega(G[B_\eta])\to\mathrm{Col}_\omega(G[B_\xi])$。下一项可检验任务是证明某个可操作的延拓条件足以产生共尾相容支，或构造满足所有局部条件但无相容支的候选系统；同时回查原始 [Er69b] 的准确边定义，消除官方摘要中的符号歧义。
- 来源核对：[Erdős Problems #919](https://www.erdosproblems.com/919) 于 2026 年抓取版本仍标 OPEN，并明确使用“lesser type”。；独立核算发现：若边真定义为两坐标同时递增，则对角线是较小序型的 $\aleph_2$-团；这与目标局部条件冲突，故该摘要不能未经原文核对直接使用。
- 时间记账：所在批次墙钟时间按题数均摊约 63.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/919)；既有候选答案（按不可信材料审计）

### #920

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g_k(n)$ denote the largest possible chromatic number of a graph with $n$ vertices which contains no $K_k$. Is it true that, for $k\geq 4$,\[g_k(n) \gg \frac{n^{1-\frac{1}{k-1}}}{(\log n)^c}\]for some constant $c>0$?
- 题意摘要：对每个固定整数 $k\ge4$，令 $g_k(n)$ 为所有 $n$ 顶点、$K_k$-free 图的最大色数。问题问是否存在依赖于 $k$ 的常数 $c_k>0$ 与 $C_k>0$，使充分大 $n$ 满足 $g_k(n)\ge C_k n^{1-1/(k-1)}/(\log n)^{c_k}$。
- 状态核对：输入中的 OPEN 状态已经过期。Bradač 的 arXiv v3（2026-06-16）证明了足够强的 off-diagonal Ramsey 下界；官方关联问题 #986 已于 2026-06-21 标为 PROVED。由标准反演可肯定回答 #920，虽然 #920 页面本身尚未同步改状态。先前候选只处理 $k=4$、称 $k\ge5$ 未知，现已失效。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：使用 Bradač 定理：固定 $k\ge3$，令 $a=2k-4$，则 $R(k,t)\ge C_k t^{k-1}/(\log t)^a$。选择最小的 $t=t(n)$ 使右端至少为 $n$；相应 Ramsey 构造给出一个至少 $n$ 顶点的 $K_k$-free 图且独立数小于 $t$，取任意 $n$ 个顶点后仍有 $\alpha<t$。
- 局部结论：由 $\chi(G)\alpha(G)\ge |V(G)|$ 得 $g_k(n)\ge n/t(n)$。；对上述最小 $t(n)$ 作单调反演，得到 $t(n)=O_k\!\left(n^{1/(k-1)}(\log n)^{a/(k-1)}\right)$。；因此 $g_k(n)\gg_k n^{1-1/(k-1)}/(\log n)^{(2k-4)/(k-1)}$；可取 $c_k=(2k-4)/(k-1)=2(k-2)/(k-1)>0$。
- 第一阻塞点：归约本身已闭合；剩余风险只在于所引用的是尚未同行评审的 2026 年 arXiv v3，而不是归约中的数学缺口。
- 下一步：更新 cohort 状态为“known resolution（依赖 Bradač 2026 v3）”，并让形式化文件把 research open 改为 solved；形式化时需补齐 Ramsey 下界到渐近 $\gg$ 记号的单调反演引理。
- 来源核对：[Bradač, Off-diagonal Ramsey numbers, arXiv:2605.28793v3](https://arxiv.org/abs/2605.28793v3) 明载 $R(s,t)\ge\Omega(t^{s-1}/(\log t)^{2s-4})$。；[Erdős Problems #986](https://www.erdosproblems.com/986) 已标 PROVED，并记录同一下界及其与 #920 的关系。；[Erdős Problems #920](https://www.erdosproblems.com/920) 仍标 OPEN，属于页面同步滞后；其旧备注已说明 #986 的肯定答案足以推出本题。
- 时间记账：所在批次墙钟时间按题数均摊约 63.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/920)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/920.lean`；既有候选答案（按不可信材料审计）

### #928

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha,\beta\in (0,1)$ and let $P(n)$ denote the largest prime divisor of $n$. Does the density of integers $n$ such that $P(n)<n^{\alpha}$ and $P(n+1)<(n+1)^\beta$ exist?
- 题意摘要：固定任意实数 $\alpha,\beta\in(0,1)$，令 $A=\{n\ge2:P(n)<n^\alpha,\ P(n+1)<(n+1)^\beta\}$。问题问自然密度 $\lim_{x\to\infty}x^{-1}|A\cap[1,x]|$ 是否存在；预期值是 $\rho(1/\alpha)\rho(1/\beta)$。
- 状态核对：截至最新官方核对仍为 OPEN。无条件已知的是对数密度等于预期乘积；在 friable Elliott–Halberstam 假设下自然密度成立。先前候选的总体状态判断正确，但对数密度本身不能经一般 Tauber 型论证自动升级为自然密度。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试把 Teräväinen 的对数平均结论升级为普通平均。设 $a_n=1_A(n)$，已知 $(\log x)^{-1}\sum_{n\le x}a_n/n\to\delta$。把整数按乘法短区间 $[X,(1+\eta)X]$ 分块；若能对固定小 $\eta$ 一致证明这些区间内 $a_n$ 的普通平均趋于 $\delta$，分块求和即可得到自然密度。
- 局部结论：若自然密度存在，则由 Abel 分部求和必等于已知对数密度 $\delta=\rho(1/\alpha)\rho(1/\beta)$；所以未知的只有存在性，不是可能的极限值。；若对每个固定 $\lambda>1$ 有 $|A\cap[X,\lambda X]|/((\lambda-1)X)\to\delta$，则把 $[1,x]$ 分成几何块可严格推出自然密度为 $\delta$。；单变量边缘事件各有 Dickman 密度，但这只控制两个指标的均值，不能控制移位乘积 $1_{P(n)<n^\alpha}1_{P(n+1)<(n+1)^\beta}$ 的普通平均。
- 第一阻塞点：第一处缺口是缺少对短乘法区间一致的、非对数加权的二元 friable 相关估计。已知对数平均允许稀疏但很长的异常区间，不能排除普通平均振荡。
- 下一步：固定一个可计算的 $\lambda$（例如 $2$），尝试证明 dyadic 相关式 $\sum_{X<n\le2X}a_n=\delta X+o(X)$。具体应先把两个平滑性指标用 Buchstab/Dickman 分解成模算术级数计数，明确所需分布水平；这会精确显示 Wang 所用 friable Elliott–Halberstam 假设出现在哪一步。
- 来源核对：[Teräväinen, On binary correlations of multiplicative functions](https://arxiv.org/abs/1710.01195) 的应用包括连续平滑数猜想的对数平均版本。；[Wang, Three conjectures on $P^+(n)$ and $P^+(n+1)$](https://www.sciencedirect.com/science/article/pii/S0022314X21000196) 在 friable Elliott–Halberstam 假设下得到自然密度。；[Erdős Problems #928](https://www.erdosproblems.com/928) 仍列 OPEN，并给出同样的无条件及条件性界线。
- 时间记账：所在批次墙钟时间按题数均摊约 63.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/928)；既有候选答案（按不可信材料审计）

### #929

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ be large and let $S(k)$ be the minimal $x$ such that there is a positive density set of $n$ where\[n+1,n+2,\ldots,n+k\]are all divisible by primes $\leq x$. Estimate $S(k)$ - in particular, is it true that $S(k)\geq k^{1-o(1)}$?
- 题意摘要：对整数 $k\ge2$，$S(k)$ 是最小阈值 $x$，使满足“每个 $n+i$（$1\le i\le k$）至少有一个不超过 $x$ 的素因子”的整数 $n$ 形成正自然密度集合。问其增长量级，特别是否 $S(k)\ge k^{1-o(1)}$。
- 状态核对：截至最新官方核对仍为 OPEN。先前候选正确识别了 primorial/Jacobsthal 结构，但其声称的上界 $S(k)\ll (k/\log k)(\log_2k)^2/\log_3k$ 与官方引用的最佳界不一致，不能接受；最新官方给出的是 $S(k)\ll k\log_3k/(\log_2k\log_4k)$。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 $Q_x=\prod_{p\le x}p$，并定义 $L(x)$ 为最长的连续整数串长度，使串中每个整数都与 $Q_x$ 不互素。先精确归约到覆盖问题，再尝试用筛法给 $L(x)$ 作上界。
- 局部结论：条件只依赖 $n\bmod Q_x$。因此只要有一个可行剩余类，就有密度至少 $1/Q_x$；反之无可行剩余类时密度为零。故“正密度”等价于“存在一个长度 $k$ 的被筛空区间”。；精确地，$S(k)=\min\{x:L(x)\ge k\}$；若采用 Jacobsthal 函数的常见定义“相邻互素整数最大间距”，则 $L(x)=j(Q_x)-1$，须保留这个 $-1$。；已知 Rosser/Jacobsthal 型筛界 $L(x)\le x^{2+o(1)}$ 立即反演为 $S(k)\ge k^{1/2-o(1)}$。另有平凡构造：取 $n\equiv1\pmod{(k+1)!}$，则 $n+i$ 被 $i+1\le k+1$ 的某个素因子整除，故 $S(k)\le k+1$。
- 第一阻塞点：要得到猜想，必须把覆盖长度上界从 $L(x)\le x^{2+o(1)}$ 强化到 $L(x)\le x^{1+o(1)}$。普通筛的二次损失正发生在控制剩余未覆盖类之间相关性时；现有论证不能排除不同小素数剩余类高度协调。
- 下一步：在精确覆盖模型中计算最优剩余类族：对每个 $p\le x$ 选择一个类 $a_p\pmod p$ 覆盖 $[1,L]$。下一项可检验任务是对中等 $x$ 用整数规划求最大 $L(x)$，并检验未覆盖点的二阶矩是否支持 $L(x)\le x(\log x)^{O(1)}$；理论上则定位 Rosser 筛中导致平方指数的单个估计。
- 来源核对：[Erdős Problems #929](https://www.erdosproblems.com/929) 仍标 OPEN，记录 $S(k)>k^{1/2-o(1)}$ 及当前较强上界。；[Ford–Green–Konyagin–Maynard–Tao, Long gaps between primes](https://www.ams.org/jams/2018-31-01/S0894-0347-2017-00876-2/S0894-0347-2017-00876-2.pdf) 给出产生官方 $S(k)$ 上界的长素数间隔构造。；已独立核对周期性归约和 $j(Q_x)$ 的一单位偏移；先前候选给出的更强反演上界没有从所引公式推出。
- 时间记账：所在批次墙钟时间按题数均摊约 63.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/929)；既有候选答案（按不可信材料审计）

### #930

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for every $r$, there is a $k$ such that if $I_1,\ldots,I_r$ are disjoint intervals of consecutive integers, all of length at least $k$, then\[\prod_{1\leq i\leq r}\prod_{m\in I_i}m\]is not a perfect power?
- 题意摘要：量词为：对每个固定正整数 $r$，是否存在 $k=k(r)$，使任意 $r$ 个两两不交的正整数闭区间 $I_i$，只要每个含至少 $k$ 个连续整数，其总乘积都不是 $M^\ell$（$M\in\mathbb N$、$\ell>1$）。正整数条件必需，否则含 $0$ 的区间立即给出零次退化。
- 状态核对：截至最新官方核对仍为 OPEN；$r=1$ 由 Erdős–Selfridge 解决。形式化文件也明确要求区间左端正、$r>0$。先前候选列出的具体小长度构造未由输入评审或官方页核实，本筛查不采用它们。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：假设总乘积 $N$ 是完全幂。取素数 $q\mid\ell$，则对每个素数 $p$ 都有 $\sum_{i=1}^r v_p(P_i)\equiv0\pmod q$，其中 $P_i=\prod_{m\in I_i}m$。尝试对每个区间使用 Erdős–Selfridge 的加强版：对给定 $q$，找到 $p_i\ge |I_i|$ 使 $v_{p_i}(P_i)\not\equiv0\pmod q$，再寻找只在一个区间贡献的素数。
- 局部结论：只需排除素指数完全幂：若 $N=M^\ell$ 且素数 $q\mid\ell$，则 $N=(M^{\ell/q})^q$。；若 $p\ge|I_i|$，因为区间直径为 $|I_i|-1<p$，故 $p$ 在该区间至多整除一个元素；这把 $v_p(P_i)$ 限制为单个整数的 $p$-进赋值。；对 $r=1$，Erdős–Selfridge 正是产生某个 $p$ 使 $q\nmid v_p(P_1)$，立即矛盾；对多个区间，相同素数可在远隔区间再次出现。
- 第一阻塞点：第一处无法闭合的是跨区间消去：即使每一行向量 $(v_p(P_i)\bmod q)_p$ 非零，也可能有这些行之和为零。区间不交只控制同一区间内的大素数重复，不能阻止同一大素数出现在多个相距很远的区间。
- 下一步：按区间端点排序，尝试证明一个“枢轴素数”引理：当所有长度超过 $k(r)$ 时，某个 $p$ 的赋值向量在 $\mathbb F_q^r$ 中具有最后一个非零坐标且总坐标和非零。若该引理失败，下一步应搜索实现零和赋值矩阵的两个长区间，从而判断障碍是真实反例机制还是仅为证明技术不足。
- 来源核对：[Erdős Problems #930](https://www.erdosproblems.com/930) 仍标 OPEN，只确认 $r=1$ 及小长度限制的必要性。；[Erdős–Selfridge 原论文](https://combinatorica.hu/~p_erdos/1975-46.pdf) 是单区间赋值论证的来源。；本地形式化文件 `ErdosProblems/930.lean` 将完全幂定义为 $m^\ell$、$\ell>1$，并明确区间左端为正；其加强变体也记录了单区间存在 $p\ge k$ 且指数不被给定 $\ell$ 整除。
- 时间记账：所在批次墙钟时间按题数均摊约 63.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/930)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/930.lean`；既有候选答案（按不可信材料审计）

### #931

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k_1\geq k_2\geq 3$. Are there only finitely many $n_2\geq n_1+k_1$ such that\[\prod_{1\leq i\leq k_1}(n_1+i)\textrm{ and }\prod_{1\leq j\leq k_2}(n_2+j)\]have the same prime factors?
- 题意摘要：对每一组固定整数 $k_1\ge k_2\ge3$，问满足 $n_1,n_2\in\mathbb N$、$n_2\ge n_1+k_1$ 且两段乘积 $A=\prod_{i=1}^{k_1}(n_1+i)$、$B=\prod_{j=1}^{k_2}(n_2+j)$ 具有完全相同素因子集合的数对 $(n_1,n_2)$ 是否有限。等价地，问 $\operatorname{rad}(A)=\operatorname{rad}(B)$ 的此类数对是否有限。
- 状态核对：截至核查时官方仍标为 open。输入中的 AlphaProof 例子只否定“所有解都满足 $n_2>2(n_1+k_1)$”的无例外版本，不否定有限性。另需注意：本地 Lean 陈述写成“对充分大的 $k_1$”，弱于自然语言中的“对每个固定 $k_1$”，存在形式化量词偏差。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：固定第一段并令 $S$ 为 $A$ 的素因子集合。共同素因子条件迫使 $n_2+1,\ldots,n_2+k_2$ 全是 $S$-unit；特别是 $x=n_2+1$ 与 $x+1=n_2+2$ 是相邻正 $S$-unit。应用固定有限 $S$ 的 $S$-unit 方程有限性，尝试先证明每个固定 $n_1$ 的纤维有限，再寻求对随 $n_1$ 变化的 $S$ 作统一控制。
- 局部结论：对固定 $(k_1,k_2,n_1)$，满足条件的 $n_2$ 只有有限多个：相邻两项给出 $S$-unit 方程 $(x+1)-x=1$，固定 $S$ 时解有限。；若 $p>k_1$，则 $p$ 在第一段中至多整除一个因子；同理，若 $p>k_2$，它在第二段中至多整除一个因子。这把大素数的支持匹配化为两段中单个同余类的匹配，但不控制指数。；例 $(n_1,k_1,n_2,k_2)=(0,10,13,3)$ 确实满足支持均为 $\{2,3,5,7\}$ 及间隔条件。
- 第一阻塞点：第一处缺口是把“每个固定 $S$ 的有限性”统一化。这里 $S=\operatorname{Supp}(A)$ 随 $n_1$ 变化，其大小及素数高度均无界；标准 $S$-unit 有限性不给出足以排除无穷多个不同 $S$ 的统一界。
- 下一步：固定最小情形 $(k_1,k_2)=(3,3)$，计算并证明大素数 $p>3$ 在两段中的唯一位置对应关系，尝试把三个同余关系消元为一个次数固定的 Thue–Mahler 型方程；首先检验所得系数集是否仍随 $n_1$ 无界。
- 来源核对：[Erdős Problems #931](https://www.erdosproblems.com/931) 于 2025-09-30 编辑后仍标 open，且记录两个有限反例。；已直接检查本地 `931.lean`：其主定理使用 `∀ᵉ (k₁ : ℕ)`，并非自然语言所暗示的所有固定 $k_1$。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/931)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/931.lean`；既有候选答案（按不可信材料审计）

### #932

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p_k$ denote the $k$th prime. For infinitely many $r$ there are at least two integers $p_r<n<p_{r+1}$ all of whose prime factors are $<p_{r+1}-p_r$.
- 题意摘要：令 $p_r,p_{r+1}$ 为相邻素数、$g_r=p_{r+1}-p_r$。断言存在无穷多个指标 $r$，使开区间 $(p_r,p_{r+1})$ 至少含两个不同整数 $m$，且每个素因子均严格小于 $g_r$，即 $P^+(m)<g_r$。
- 状态核对：官方当前仍标 open。旧候选对“至少一个”的 $2^a$ 构造基本正确，但它不能推进“同一间隙至少两个”的核心要求。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先用 $m=2^a$ 重建一数版本，再尝试在同一素数间隙加入第二个显式光滑数。若 $2^a$ 所处间隙长度为 $g$，模 $3$ 排除该间隙为以 $2^a$ 为中点的孪生素数间隙，从而 $g\ge4$，故 $2^a$ 合格。第二个候选若取另一幂或固定小素数的乘积，则必须同时证明两候选之间没有素数。
- 局部结论：对每个 $a\ge3$，包含 $2^a$ 的相邻素数间隙满足 $g\ge4$：若 $g=2$，两端只能是 $2^a-1,2^a+1$，其中一个被 $3$ 整除且大于 $3$。因此 $P^+(2^a)=2<g$。；不同的 $2^a$ 最终落在无穷多个不同素数间隙中，因为每个有限间隙只含有限多个整数；故“至少一个”版本确有无穷多个 $r$。；小例子可严格核验：$(7,11)$ 中 $8,9$ 均为 $4$-smooth（素因子严格小于 $4$）；$(23,29)$ 中 $24,25,27$ 均满足 $P^+<6$。
- 第一阻塞点：第一处缺口是保证第二个光滑数与 $2^a$ 位于同一实际素数间隙。构造两个相近光滑数并不足够，还需排除它们之间的所有素数；现有初等同余或光滑数估计不能提供这种素数空区间。
- 下一步：计算检验所有已知成功间隙中的两个最小 $g_r$-smooth 数之差，并测试它们是否常来自固定形状（如相邻 $S$-units 或两个小素数幂）；若发现稳定形状，再把任务化为“该形状能否嵌入已知的大素数间隙构造”。
- 来源核对：[Erdős Problems #932](https://www.erdosproblems.com/932) 当前仍标 open，并记录“一数版本指标集密度为零”。；本地 `932.lean` 的集合基数条件确为至少 $2$，并使用严格不等式 `maxPrimeFac < gap`。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/932)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/932.lean`；既有候选答案（按不可信材料审计）

### #933

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $n(n+1)=2^k3^lm$, where $(m,6)=1$, then is it true that\[\limsup_{n\to \infty} \frac{2^k3^l}{n\log n}=\infty?\]
- 题意摘要：对每个正整数 $n$，唯一写成 $n(n+1)=2^{k(n)}3^{l(n)}m$ 且 $(m,6)=1$；即 $k=v_2(n(n+1))$、$l=v_3(n(n+1))$。问题是 $2^k3^l/(n\log n)$ 是否沿某个 $n\to\infty$ 的子列无界。
- 状态核对：截至当前官方仍标 open。旧候选的 LTE 计算可核实，但只能给固定常数，不能证明 limsup 无穷。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：系统分析纯二次幂子列 $n=2^a$。当 $a$ 为奇数时，LTE 给出 $v_3(2^a+1)=1+v_3(a)$，故比值可显式计算；再判断能否通过改变指数 $a$ 放大该比值。
- 局部结论：取 $a=3^r$、$n=2^{3^r}$，有 $k=3^r$ 且 $l=r+1$，因此比值精确等于 $3/\log2$，确实大于 $1$。；更一般地，若 $a=3^rb$、$a$ 为奇数且 $3\nmid b$，则该子列上的比值为 $3/(b\log2)$。；因此在整个纯二次幂路线 $n=2^a$ 中，选择额外的因子 $b$ 只会减小比值；Steinerberger 子列已达到此路线的最大常数，不能产生无界性。
- 第一阻塞点：第一处缺口是同时让 $n$ 或 $n+1$ 的 $2$-部分贡献约 $n$，并使另一项的 $3$-部分比 $\log n$ 大任意倍。LTE 构造把 $3$-进指数增长锁定为 $\log_3 a$，恰好只补偿分母中的 $a$，无法产生额外无界因子。
- 下一步：考察 $n=2^a u$ 且 $n+1\equiv0\pmod{3^b}$ 的最小正解，计算其大小相对于 $2^a3^b$；可检验的目标是寻找序列满足最小 CRT 代表元 $n=o(2^a3^b/\log n)$，或证明该双模路线存在不可逾越的常数界。
- 来源核对：[Erdős Problems #933](https://www.erdosproblems.com/933) 当前仍标 open，并明确记录 $n=2^{3^r}$、$k=3^r$、$l=r+1$。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/933)；既有候选答案（按不可信材料审计）

### #934

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h_t(d)$ be minimal such that every graph $G$ with $h_t(d)$ edges and maximal degree $\leq d$ contains two edges whose shortest path between them has length $\geq t$. Estimate $h_t(d)$.
- 题意摘要：固定整数 $t,d$。两条边的距离取其端点间最短顶点距离；令 $h_t(d)$ 为最小边数阈值，使每个最大度至多 $d$、边数达到该阈值的图都含距离至少 $t$ 的两条边。等价地，$h_t(d)-1$ 是满足 $\Delta(G)\le d$ 且线图 $L(G)$ 直径至多 $t$ 的最大边数。
- 状态核对：总体估计问题仍开放，但已有严格的一般上界 $h_t(d)\le\tfrac32d^t+1$，以及 $t=1,2$ 和部分 $t=3$ 的强结果。旧候选给出的奇数 $d$ 的 $h_2(d)$ 精确公式未被输入的官方材料支持，本次不采纳；其“端点距离”和线图直径的等价性没有偏移错误，因为对不同边有 $d_{L(G)}(e,f)=d_G(e,f)+1$。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：重建初等球计数。若不存在距离至少 $t$ 的边对，则 $\operatorname{diam}L(G)\le t$。固定一条边 $e$；在线图距离恰为 $i$ 的边至多 $2(d-1)^i$，因为可从 $e$ 的两个端点分别沿非回溯边延伸。对 $0\le i\le t$ 求和。
- 局部结论：严格得到 $|E(G)|\le1+2\sum_{i=1}^t(d-1)^i$，因而 $h_t(d)\le2d^t+O_t(d^{t-1})$；这重建了经典的 $2d^t$ 量级上界。；论文的改进定理把常数 $2$ 降到 $3/2$：$h_t(d)\le\tfrac32d^t+1$。；当 $d=q+1$ 且 $q$ 为素数幂时，射影平面的点—线关联图有最大度 $d$、$d^3-d^2+d$ 条边及线图直径 $3$，故 $h_3(d)\ge d^3-d^2+d+1$。
- 第一阻塞点：初等球计数把从不同端点生成的非回溯分支视为互异，不能利用直径条件强迫的大量交叠；要把首项常数从 $2$ 降到猜想的 $1+o(1)$，必须定量控制两侧 BFS 层之间的碰撞。该交叠估计正是当前路线中首个不能自行闭合的步骤。
- 下一步：先在 $t=3$ 写出两端 BFS 层的双计数，按奇圈 $C_7$ 是否存在分情；检验无 $C_7$ 情形中交叠项能否直接恢复论文所述精确型界，再定位一般图中奇圈造成的损失。
- 来源核对：[Erdős Problems #934](https://www.erdosproblems.com/934) 于 2025-10-28 编辑后仍列出 $\tfrac32d^t+1$ 上界及相关猜想。；Cambie 等人的原始论文摘要明确陈述：超过 $1.5\Delta^t$ 条边会迫使线图直径大于 $t$。[arXiv:2103.11898](https://arxiv.org/abs/2103.11898)
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/934)；既有候选答案（按不可信材料审计）

### #935

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any integer $n=\prod p^{k_p}$ let $Q_2(n)$ be the powerful part of $n$, so that\[Q_2(n) = \prod_{\substack{p\\ k_p\geq 2}}p^{k_p}.\]Is it true that, for every $\epsilon>0$ and $\ell\geq 1$, if $n$ is sufficiently large then\[Q_2(n(n+1)\cdots(n+\ell))<n^{2+\epsilon}?\]If $\ell\geq 2$ then is\[\limsup_{n\to \infty}\frac{Q_2(n(n+1)\cdots(n+\ell))}{n^2}\]infinite? If $\ell\geq 2$ then is\[\lim_{n\to \infty}\frac{Q_2(n(n+1)\cdots(n+\ell))}{n^{\ell+1}}=0?\]
- 题意摘要：固定 $\ell\ge1$，令 $P_{n,\ell}=\prod_{i=0}^{\ell}(n+i)$，$Q_2(P)$ 保留 $P$ 中指数至少 $2$ 的完整素数幂。三问分别是：(一) 对每个 $\epsilon>0$ 是否最终有 $Q_2(P_{n,\ell})<n^{2+\epsilon}$；(二) 对每个 $\ell\ge2$，$Q_2(P_{n,\ell})/n^2$ 的 limsup 是否无穷；(三) 对每个 $\ell\ge2$，$Q_2(P_{n,\ell})/n^{\ell+1}$ 是否趋于零。
- 状态核对：输入状态已过时。官方页面 2026-02-08 更新：第二问已由 Pell 方程构造肯定解决；第一问（除平凡的 $\ell=1$）与第三问仍开放，第三问在 ABC 猜想下成立。旧候选称第二问开放，必须弃用。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建第二问的已知证明。取 Pell 方程 $x_j^2-8y_j^2=1$ 的解并令 $n_j=8y_j^2$，则 $n_j$ 和 $n_j+1=x_j^2$ 都是 powerful。再选 $j_t=(3\cdot5^{t-1}-1)/2$；由 $\alpha=3+\sqrt8$ 的恒等式及二项归纳得到 $5^t\mid n_{j_t}+2$。
- 局部结论：因此 $Q_2(n_{j_t}(n_{j_t}+1)(n_{j_t}+2))\ge n_{j_t}(n_{j_t}+1)5^t$。又 $\log n_{j_t}=O(5^{t-1})$，故该量至少为常数倍的 $n_{j_t}^2\log n_{j_t}$，第二问对 $\ell=2$ 成立；增加后续因子只会增大 $Q_2$，所以对所有 $\ell\ge2$ 成立。；对固定 $\ell$，$Q_2(\prod_i(n+i))$ 与 $\prod_iQ_2(n+i)$ 只相差由 $p\le\ell$ 且分别以一次幂落在多个因子中的贡献，故二者之比受仅依赖 $\ell$ 的常数控制。；第一问若成立，则第三问成立：选 $0<\epsilon<\ell-1$，便有 $Q_2(P_{n,\ell})/n^{\ell+1}<n^{\epsilon-(\ell-1)}\to0$。此外 $\ell=1$ 的第一问由 $Q_2(n(n+1))\le n(n+1)<n^{2+\epsilon}$ 平凡成立。
- 第一阻塞点：对仍开放的第一、三问，第一处缺口是无条件控制多个相邻整数各自的大平方幂部分。跨项共享素数只能来自 $p\le\ell$，可吸收到常数中；真正未闭合的是证明 $\prod_{i=0}^{\ell}Q_2(n+i)\le n^{2+o(1)}$，这需要超出现有无条件根基估计的统一界。
- 下一步：把固定 $\ell$ 的“乘积的 powerful part”和“各因子 powerful part 的乘积”之间的常数写成显式 $C_\ell$ 并严格证明；随后对 $\ell=2$ 枚举平方因子分解 $n+i=a_i b_i^2$，检验是否能把目标归约为三元曲线族的统一整数点高度界。
- 来源核对：[Erdős Problems #935](https://www.erdosproblems.com/935) 现明确记录第二问由 $x^2-8y^2=1$ 的构造肯定解决，并称第三问在 ABC 下成立。；[关联问题 #367 的讨论](https://www.erdosproblems.com/forum/thread/367) 给出了 $n_j=8y_j^2$、指标 $j_t$、$5^t\mid n_{j_t}+2$ 及 $\gg n_j^2\log n_j$ 的具体推导。；需纠正输入中的日期：#935 官方页面最后编辑日期为 2026-02-08，晚于给定的 2025-09-04 状态快照。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/935)；既有候选答案（按不可信材料审计）

### #936

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are\[2^n\pm 1\]and\[n!\pm 1\]powerful (i.e. if $p\mid m$ then $p^2\mid m$) for only finitely many $n$?
- 题意摘要：对四个序列分别问：是否各自仅有有限多个正整数 n，使 2^n-1、2^n+1、n!-1 或 n!+1 为 powerful，即每个素因子的指数至少为 2。本地 Lean 用 EventuallyNotPowerful 表示“从某处起均非 powerful”，与有限性等价；自然数减法的初始截断不影响最终性。
- 状态核对：无条件仍为开放；abc 猜想下四种情形均已知为肯定。旧候选的 abc 主线正确，但只能给条件证明，不能冒充开放题解答。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：沿 abc 路线独立检查。若 M powerful，则 rad(M)≤M^{1/2}。对 2^n±1 使用三元组 (2^n,1,2^n±1)；对 n!±1 使用 (n!,1,n!+1) 或 (n!-1,1,n!)，并结合 log rad(n!)=θ(n)=O(n) 与 log(n!)∼n log n。
- 局部结论：若 2^n±1 powerful，abc 给出 2^n≪(2·(2^n±1)^{1/2})^{1+ε}；固定 ε<1 后指数系数 (1+ε)/2<1，故 n 有界。；若 n!±1 powerful，abc 给出约 log(n!)≤(1+ε)(O(n)+(1/2)log(n!))+O(1)；固定 ε<1 后与 log(n!)∼n log n 矛盾，故 n 有界。；n!+1=x² 是 powerful 子情形；因此无条件解决 powerful 的有限性确会推出 Brocard–Ramanujan 方程解的有限性，但这只是难度障碍，不是反向证明。
- 第一阻塞点：第一处无法无条件闭合的是调用 abc 的 radical 上界；现有方法没有相应的无条件强度。
- 下一步：把上述四个推导写成统一引理：若 rad(u_n)=e^{o(log v_n)} 且 |u_n-v_n|=1，则 abc 排除 v_n±1 powerful；逐项核对互素性与 ε 的可选范围。
- 来源核对：[Erdős Problems #936](https://www.erdosproblems.com/936) 仍标 OPEN，并明确记录两类 abc 条件结果。；[CrowdMath, Applications of the abc conjecture to powerful numbers](https://arxiv.org/abs/2005.07321) 核对了指数序列的条件路线。；[Cushing–Pascoe, Powerful numbers and the ABC-conjecture](https://arxiv.org/abs/1611.01192) 核对了阶乘附近 powerful 数的条件路线。；已读取本地 936.lean；四个变体确实分别量化四个序列。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/936)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/936.lean`；既有候选答案（按不可信材料审计）

### #938

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A=\{n_1<n_2<\cdots\}$ be the sequence of powerful numbers (if $p\mid n$ then $p^2\mid n$). Are there only finitely many three-term progressions of consecutive terms $n_k,n_{k+1},n_{k+2}$?
- 题意摘要：令 n_1<n_2<⋯ 枚举全部正 powerful 数。问题问满足 n_k+n_{k+2}=2n_{k+1} 的指标 k 是否只有有限多个；“consecutive terms”要求两个开区间内都没有其他 powerful 数，并非三个连续整数。
- 状态核对：仍开放。旧候选列出的前两个例子经重新枚举核实，但其到 10^12 的完整数据未提供代码或证书，不能采信为已核对事实。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：利用唯一表示 m=a²b³（b squarefree），把三项等差条件化为 b_1³a_1²+b_3³a_3²=2b_2³a_2²；再检查齐次缩放能否产生无限多个“连续项”反例。
- 局部结论：(1728,1764,1800) 确为连续 powerful 项且公差 36；分解分别为 2^6·3^3、2²·3²·7²、2³·3²·5²。；(6912,7056,7200) 也经完整枚举至 7200 核实为连续项三项等差数列。；若一个 powerful 三项等差数列整体乘 t²，仍是 powerful 三项等差数列；但当 t 足够大时，区间 (t²x,t²y) 的平方根长度 t(√y-√x)>1，必插入一个平方即 powerful 数。因此齐次缩放不能产生无限多个“连续项”例子。
- 第一阻塞点：固定 squarefree 三元组后所得二次曲面可参数化，但“中间不存在任何 c²d³”是同时涉及所有 squarefree d 的排除条件；第一处缺口是无法对这些插入点作统一控制。全局计数 Q(x)=C√x+O(x^{1/3}) 也不能控制如此短的局部间隙。
- 下一步：对每个已知原始三元组计算缩放 t 保持连续性的显式上界；随后按 b_i 的 dyadic 区间枚举二次方程解，测试是否能把插入平方的论证推广为对大参数必有某个 powerful 插入点。
- 来源核对：[Erdős Problems #938](https://www.erdosproblems.com/938) 当前仍标 OPEN。；已读取本地 938.lean，确认对象是全部 powerful 数枚举中的相邻三项。；本地完整枚举至 7200 独立核实了两个小例子及其相邻性。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/938)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/938.lean`；既有候选答案（按不可信材料审计）

### #939

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$. An $r$-powerful number $n$ is one such that if $p\mid n$ then $p^r\mid n$. If $r\geq 4$ then can the sum of $r-2$ coprime $r$-powerful numbers ever be itself $r$-powerful? Are there at most finitely many such solutions? Are there infinitely many triples of coprime $3$-powerful numbers $a,b,c$ such that $a+b=c$?
- 题意摘要：这里包含三个问题：(i) 对每个 r≥4，是否存在恰有 r−2 个、全体 gcd 为 1 的 r-powerful 正整数，其和仍 r-powerful；(ii) 对各 r 是否至多有限个此类解；(iii) 是否有无限多个全体 gcd 为 1 的 3-powerful 三元组 a+b=c。本地 Finset.Coprime 表示联合 gcd 为 1，不表示两两互素。
- 状态核对：混合状态：第三问已知肯定；r=5、7、8 已知存在例子。冻结日期之后，官方页又记录了 r≥6 的无限构造，因此第二问在 r≥6 已被否定，第一问只剩 r=4 的普遍存在缺口；总体页面仍标 OPEN。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建两条路线：先直接验算 r=5 与 3-powerful 示例；再检查新构造 (X+Y)^r=(X−Y)^r+Σ_{j odd}2·C(r,j)X^{r−j}Y^j，并把 j=3 项拆成若干正系数项。
- 局部结论：例 2³·3⁵·73³+271³=919³ 的恒等式、3-powerful 性及联合 gcd=1 均已独立验算；Nitaj、Cohn、Walsh 的结果给出无限族，故第三问已有已知肯定答案。；r=5 恒等式 3⁷·61⁵=2⁸·3¹⁰·5⁷+2¹²·23⁶+11⁵·13⁵ 已验算；各项均 5-powerful且三项联合 gcd=1。旧候选说“前两项共享 2”是正确的，故不能改称两两互素。；对 r≥6，令 t=⌊r/2⌋−2，把 j=3 的系数 2C(r,3) 拆成 t 个互异正整数 v_l；取 X=q^r、Y=B^r，其中 B 含所有系数素因子、q∤B 为充分大的素数。各项均 r-powerful，(X−Y)^r 与其余项联合 gcd 为 1，且随 q 得无限多个不同解；充分大 q 还保证各拆分项互异。
- 第一阻塞点：该构造要求 r≥6；r=5 虽有孤立例子但未产生无限族，r=4 的 a+b=c 存在性仍无法闭合。对 r=4，abc 可条件性推出原始解有限：rad(abc)≤(abc)^{1/4}≤c^{3/4}，但这既不证明存在也不是无条件结果。
- 下一步：优先处理剩余核心 r=4：枚举 squarefree 核并把 a+b=c 转成有限高度的加权四次幂/高亏格曲线族；先复核已报道的 max(a,b)>10^14 计算界是否有可审计代码与完备性证明。
- 来源核对：[Erdős Problems #939](https://www.erdosproblems.com/939) 记录已知第三问、r=5/7/8 例子及 2026 年 r≥6 无限构造。；[讨论页中的明确二项式构造](https://www.erdosproblems.com/forum/thread/939) 已逐项检查项数、powerful 性和联合 gcd。；[Walsh 预印本](https://arxiv.org/abs/2404.03970) 提供第三问的替代构造。；本地 939.lean 明确定义联合 coprime，并已形式化核验显示的 r=5 示例。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/939)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/939.lean`；既有候选答案（按不可信材料审计）

### #940

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 3$. A number $n$ is $r$-powerful if for every prime $p$ which divides $n$ we have $p^r\mid n$. Are there infinitely many integers which are not the sum of at most $r$ many $r$-powerful numbers? Does the set of integers which are the sum of at most $r$ $r$-powerful numbers have density $0$?
- 题意摘要：对每个固定 r≥3，令 S_r 为可表示成至多 r 个非负 r-powerful 整数之和的整数集合。分别问 N\S_r 是否无限，以及 S_r 的自然密度是否为 0。第二问肯定会推出第一问肯定，反之不然。
- 状态核对：两问仍开放；尤其 r=3 时，甚至至多三个立方数之和的集合是否密度 0 也未知。旧候选的临界计数观察正确，但没有解决 k=r。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用直接计数路线。设 F_r(x) 为不超过 x 的 r-powerful 数个数，使用标准估计 F_r(x)=O_r(x^{1/r})，再数 k 元有序表示。
- 局部结论：对每个 k<r，至多 k 个 r-powerful 数之和的不同取值数不超过 O_r(x^{k/r})=o(x)，故这些子集合密度 0。；对 k=r，朴素计数只有 O_r(F_r(x)^r)=O_r(x)，恰好失去任何密度节省；这精确定位了 Erdős“简单计数”不能闭合之处。；每个立方都是 3-powerful，所以“三个立方之和”集合包含于 S_3；若能证明 S_3 密度 0，便立即解决较小的三个立方取值集密度问题。
- 第一阻塞点：第一处缺口是临界 r 元和中缺少 o(x) 的节省。需要证明大量表示碰撞，或用筛法排除正比例的目标整数；仅知道 F_r(x)=O(x^{1/r}) 不够。也不能从“预计平均表示数小”直接推出非表示数无限。
- 下一步：计算截断集合 A=F_r∩[1,x] 的 r 重加法能量 E_r(A)，测试 Cauchy–Schwarz 是否能从非平凡能量下界推出 |rA|=o(x)；先在 r=3 上寻找来自共同 squarefree 核的系统性碰撞。
- 来源核对：[Erdős Problems #940](https://www.erdosproblems.com/940) 仍标 OPEN，并明确记载 Schinzel 指出的计数错误及三个立方障碍。；已读取本地 940.lean；主要形式化陈述只编码密度问题，另有最终覆盖问题的变体。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/940)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/940.lean`；既有候选答案（按不可信材料审计）

### #942

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ count the number of powerful (if $p\mid m$ then $p^2\mid m$) integers in $[n^2,(n+1)^2)$. Estimate $h(n)$. In particular is there some constant $c>0$ such that\[h(n) < (\log n)^{c+o(1)}\]and, for infinitely many $n$,\[h(n) >(\log n)^{c-o(1)}?\]
- 题意摘要：h(n) 是半开区间 [n²,(n+1)²) 内 powerful 正整数的个数。问题要求存在同一个常数 c>0，使最终一致上界 h(n)<log(n)^{c+o(1)}，同时无限多个 n 满足 h(n)>log(n)^{c−o(1)}；这是最大阶数量级问题，不是平均值问题。
- 状态核对：仍开放。冻结上下文只给出指数 1/3 的无限次下界；2026 年官方页已纳入优化结果 h(n)≫log n/(loglog n·logloglog n)，所以旧候选的“目前只能推出 c≥1/3”已经过时。其关于完整固定值分布和猜测 c=1 的若干陈述也不能替代统一上界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：从唯一表示 m=a²b³（b squarefree）出发，把 h(n) 视为薄曲线 a²b³≈n² 附近的整数点数；先做可完全验证的分区计数，再与已知同时逼近下界比较。
- 局部结论：固定 b 时区间中至多一个 a；固定 a 时也至多一个 b。又由 a²b³<(n+1)² 可知 a≤(n+1)^{2/5} 或 b≤(n+1)^{2/5}，故初等地 h(n)≤2(n+1)^{2/5}+O(1)。；望远镜求和与 powerful 数计数 Q(x)∼[ζ(3/2)/ζ(3)]√x 给出 (1/N)Σ_{n<N}h(n)→ζ(3/2)/ζ(3)；这说明平均值有界，但完全不控制最大尖峰。；后续优化下界为 h(n)≫log n/(loglog n·logloglog n)=(log n)^{1−o(1)} 无限次成立。因此若题设的匹配指数 c 存在，必有 c≥1；同时下界一侧已经可取 c=1。
- 第一阻塞点：第一处无法闭合的是把整数点上界从 n 的正幂降到 log n 的幂。唯一表示加逐变量计数只给 n^{2/5}；更精细的近曲线技术目前仍给 n^{6/25+ε} 量级，离所需 polylog 上界很远。
- 下一步：对 a,b 在临界尺度 a≈b≈n^{2/5} 作 dyadic 分块，复核 Filaseta–Trifonov 型近曲线计数的适用条件；明确找出若要达到 (log n)^{1+o(1)}，哪一个分块必须获得超出现有除差法的节省。
- 来源核对：[Erdős Problems #942](https://www.erdosproblems.com/942) 当前仍标 OPEN，并已记录 2026 年优化下界。；[官方讨论页](https://www.erdosproblems.com/forum/thread/942) 给出优化构造概要、初等 n^{2/5} 上界及近曲线方法的 n^{6/25+ε} 声称；其中后两项尚主要是讨论材料，未当作开放题解答。；已读取本地 942.lean，确认量词要求同一个 c、最终上界和无限次下界。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/942)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/942.lean`；既有候选答案（按不可信材料审计）

### #943

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be the set of powerful numbers (if $p\mid n$ then $p^2\mid n$). Is it true that\[1_A\ast 1_A(n)=n^{o(1)}\]for every $n$?
- 题意摘要：令 A 为正 powerful 数集，即每个素因子在素因数分解中的指数至少为 2。这里 * 是加法卷积；R(n)=(1_A*1_A)(n)=#{(a,b)∈A²:a+b=n}，计有序表示。问题是是否对每个 ε>0，所有充分大的 n 都有 R(n)≤n^ε。
- 状态核对：仍为开放题。先前候选把 * 误作 Dirichlet 卷积并用 τ(n) 控制，人工评审指出的错误属实；该论证与本题无关。本地 Lean 定义也明确使用 antidiagonal n，即 a+b=n。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：使用 powerful 数的唯一表示 m=u²v³，其中 v 无平方因子。按立方部分 v≤Y 或 v>Y 分割每个加法表示；小立方部分归约为方程 v³u²+w³z²=n，大立方部分直接计数。
- 局部结论：立方部分 v>Y 的 powerful 数 m≤n 至多为 O(√(n/Y))，因为 Σ_{v>Y}⌊√(n/v³)⌋≪√n·Σ_{v>Y}v^{-3/2}。；因此 R(n)≤R_{≤Y}(n)+O(√(n/Y))，其中 R_{≤Y} 只涉及至多 Y² 个方程 v³u²+w³z²=n。；这把原问题具体归约为：对随 n、Y 变化的平方自由系数 v,w，控制上述二元二次方程解数的总和，而不是逐个方程的粗界。
- 第一阻塞点：第一处缺口是无法证明 Σ_{v,w≤Y}#{(u,z):v³u²+w³z²=n}=n^{o(1)}，且逐个套固定二次型的表示数估计并不在系数增长时给出所需的一致总界。
- 下一步：先检验平均化命题：对 Y=n^δ，能否利用模素数筛法证明上述 Y² 个椭圆方程的解数总和 ≪n^{o(1)}+n^{1/2}Y^{-1/2}；应特别记录系数 gcd 和退化情形。
- 来源核对：[Erdős Problems #943](https://www.erdosproblems.com/943) 仍标为 open。；本地 943.lean 使用 sumRep Powerful n；Convolution.lean 定义 sumRep 为对 a+b=n 的有序对计数。
- 时间记账：所在批次墙钟时间按题数均摊约 77.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/943)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/943.lean`；既有候选答案（按不可信材料审计）

### #944

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：A critical vertex, edge, or set of edges, is one whose deletion lowers the chromatic number. Let $k\geq 4$ and $r\geq 1$. Must there exist a graph $G$ with chromatic number $k$ such that every vertex is critical, yet every critical set of edges has size $>r$?
- 题意摘要：量词是：对每个整数 k≥4、r≥1，是否存在有限简单图 G，满足 χ(G)=k；对每个顶点 v，χ(G-v)<k；并且凡 E₀⊆E(G) 使 χ(G-E₀)<k，都有 |E₀|>r。等价地，删除任意至多 r 条边仍保持 k-色数。
- 状态核对：整体仍开放，但已知对所有 k≥5、r≥1 为真；唯一未决的是 k=4，甚至 r=1。先前候选的状态划分与最新官方说明一致。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：针对遗留的 k=4,r=1，尝试从 4-vertex-critical 图出发，以 Ore/Hajós 型组合或边替换消除关键边，同时保持每个顶点关键；先把关键边条件改写成 3-着色约束。
- 局部结论：若 G 是 4-vertex-critical，则 χ(G-v)=3 且 δ(G)≥3。；边 e=uv 关键当且仅当 G-e 可 3-着色；在这种着色中必有 u、v 同色，否则该着色也会着色 G。；所以 r=1 要求一个顶点删除后可 3-着色、但任意边删除后仍为 4-色的图；任意 r≥1 的肯定答案都首先必须解决这一情形。
- 第一阻塞点：Ore/Hajós 组合可以控制色数，却没有证明“每个顶点仍关键”与“每条边均非关键”同时保存；连接接口附近的边可能新变成关键边。这是路线中的第一处未闭合步骤。
- 下一步：对所有较小的 4-critical 图做 SAT/nauty 枚举，逐边检验 χ(G-e)=4，并追踪 Ore 组合中接口边的着色证书；目标是找出可组合的最小局部模块或证明该组合操作必失败。
- 来源核对：[Erdős Problems #944](https://www.erdosproblems.com/944) 明载 k≥5 已由 Skottová–Steiner解决，k=4,r=1 仍开放。；本地 944.lean 的全称量词与 IsCriticalEdges 定义方向和上述重述一致。
- 时间记账：所在批次墙钟时间按题数均摊约 77.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/944)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/944.lean`；既有候选答案（按不可信材料审计）

### #945

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F(x)$ be the maximal $k$ such that there exist $n+1,\ldots,n+k\leq x$ with $\tau(n+1),\ldots,\tau(n+k)$ all distinct (where $\tau(m)$ counts the divisors of $m$). Estimate $F(x)$. In particular, is it true that\[F(x) \leq (\log x)^{O(1)}?\]In other words, is there a constant $C>0$ such that, for all large $x$, every interval $[x,x+(\log x)^C]$ contains two integers with the same number of divisors?
- 题意摘要：F(x) 是所有 k 中最大者，使某个连续整数块 n+1,…,n+k≤x 的 τ 值两两不同。问题是是否存在绝对常数 C，使 F(x)≤(log x)^C 对充分大 x 成立；等价地，每个相应长度的短区间都出现两个 τ 值相同的整数。
- 状态核对：仍开放。当前记录的无条件上界为 exp(O((log x)^{1/3+o(1)}))，尚非多对数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：不用短区间分布，先按整数的素因子指数型分类：若 m=∏p_i^{a_i}，则 τ(m)=∏(a_i+1)，只依赖指数多重集。用整数分拆数控制 m≤x 可能产生的 τ 值总数。
- 局部结论：将 a_i 降序排列并令 Ω(m)=Σa_i，则 Ω(m)≤log₂x；每种指数多重集是某个 N≤log₂x 的整数分拆。；因此 #{τ(m):m≤x}≤Σ_{N≤log₂x}p(N)=exp(O(√log x))。；若长度 k 的连续块中 τ 值两两不同，则 k 不超过上述全局值域大小，故得到严格但较弱的 F(x)≤exp(O(√log x))。
- 第一阻塞点：分拆计数把每种指数型都视为可能产生新 τ 值，损失过大；要得到 (log x)^C，必须证明不同指数分拆在乘积 ∏(a_i+1) 上发生极大量碰撞，现有路线没有这种多重性下界。
- 下一步：计算并证明受约束乘积分拆计数：统计可写成 ∏(a_i+1)、且最小实现数 ∏p_i^{a_i}≤x 的不同整数，先尝试把现有 exp(O((log x)^{1/3+o(1)})) 的分层参数完整重建。
- 来源核对：[Erdős Problems #945](https://www.erdosproblems.com/945) 给出 Erdős–Mirsky 界、Beker 改进及两个条件性 O((log x)²) 结论。；本地 945.lean 确认 F(x) 采用连续区间上的 τ 单射定义。
- 时间记账：所在批次墙钟时间按题数均摊约 77.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/945)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/945.lean`；既有候选答案（按不可信材料审计）

### #948

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Is there a function $f(n)$ and a $k$ such that in any $k$-colouring of the integers there exists a sequence $a_1<\cdots$ such that $a_n<f(n)$ for infinitely many $n$ and the set\[\left\{ \sum_{i\in S}a_i : \textrm{finite }S\right\}\]does not contain all colours?
- 题意摘要：原命题量词为：是否存在一个函数 f:ℕ→ℕ 和某个有限颜色数 k，使对每个 k-着色 c，都存在同一个无限严格递增序列 (a_n)，满足 a_n<f(n) 对无穷多个 n 成立，且其所有有限非空子集和 FS(a_n) 至少遗漏一种颜色。其否定是：对每个 f、k，存在一个 k-着色，使任何满足该无穷次界限的序列之 FS 集都出现全部 k 种颜色。
- 状态核对：输入记录在 2026-07-06 更新为 solved，结论是否定答案。旧候选称“仍开放”已过时。网页主体缓存到 2026-04-10 尚显示 open，但 2026-06-21 的讨论已发布反例，并报告 Lean 形式化及独立审阅通过。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `medium`
- 尝试路线：重建其广义 Galvin 路线：给定 f，递归选择足够快增长的 2-adic 阈值并定义整数层级 c_f(m)，再以 c_{f,k}(m)=c_f(m) mod k 着色。对任何无限多次满足 a_n<f(n) 的递增序列，用有限前缀、同余抽屉原理和 2-adic 估值选择子集和，使其层级逐次跨过全部 k 个余数。
- 局部结论：k=2 时“遗漏一种颜色”等同于 FS 单色，Galvin 原来的 2-adic 着色已经否定这一情形。；完整反例加强为：对任意给定 f 和任意有限 k，都能预先构造一个着色；着色不依赖随后选择的序列。；只要求 a_n<f(n) 无穷多次仍足以反复抽取有限块；这些块的子集和层级覆盖 k 个连续整数，模 k 后即覆盖全部颜色。
- 第一阻塞点：本次独立重建尚未严格闭合“层级跨越引理”：需要逐项核对阈值递归如何保证所选子集和的 c_f 值恰好覆盖连续层级。可访问的讨论只给出机制摘要，Overleaf 正文未能抓取；因此这里不冒充重新完成了整篇证明。该缺口由外部 Lean 形式化和人工审阅覆盖，但仍是本次筛查的首个独立审计缺口。
- 下一步：取得公开 LaTeX 与 Lean 源码后，逐行核对层级定义、有限和是否排除空集、k=1 边界以及“无穷多 n”到可用有限块的量词转换，并在本地重新编译 Lean 文件。
- 来源核对：[Erdős Problems #948 讨论](https://www.erdosproblems.com/forum/thread/948?embed=1) 于 2026-06-21 报告否定证明及 Lean 形式化，随后两位评论者报告筛查和同行核对通过。；[网页主体的旧缓存](https://www.erdosproblems.com/948) 最后编辑于 2026-04-10，故其 open 标签早于 cohort 的 2026-07-06 状态更新。
- 时间记账：所在批次墙钟时间按题数均摊约 77.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/948)；既有候选答案（按不可信材料审计）

### #949

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $S\subset \mathbb{R}$ be a set containing no solutions to $a+b=c$. Must there be a set $A\subseteq \mathbb{R}\backslash S$ of cardinality continuum such that $A+A\subseteq \mathbb{R}\backslash S$?
- 题意摘要：对每个任意集合 S⊆ℝ，若不存在 a,b,c∈S 满足 a+b=c（允许 a=b），是否必存在 A⊆ℝ∖S，满足 |A|=𝔠 且对所有 x,y∈A 都有 x+y∉S。
- 状态核对：一般情形仍开放；Sidon 特例已有肯定证明，并已在本地 Lean 文件中形式化。先前候选的两个局部结论可成立，但 Sidon 构造需分开处理 |S|<𝔠 与 |S|=𝔠，不能无条件写成 |S|=𝔠。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先用 Zorn 取极大 A，使 A∩S=∅ 且 (A+A)∩S=∅；再由极大性分析不能加入的新点。对 Sidon 且 |S|=𝔠 的情形，固定 0≠a∈S 并取 A=((S∖{a})-a/2)∖S。
- 局部结论：极大性给出 ℝ⊆S∪(S/2)∪A∪⋃_{a∈A}(S-a)。若 |S|<𝔠 且 |A|<𝔠，右侧基数仍小于 𝔠，矛盾；故小于连续统的任意 S 都有合适的 A，甚至不需 sum-free。；若 S 是 Sidon、|S|=𝔠，则 ((S∖{a})-a/2)∩S 至多一点：两组不同交点会给出交叉和的两种 Sidon 表示。因此上述 A 仍有基数 𝔠。；若 x=s₁-a/2、y=s₂-a/2 且 x+y=s₃∈S，则 s₁+s₂=a+s₃；Sidon 性迫使无序对 {s₁,s₂}={a,s₃}，与 s₁,s₂≠a 矛盾，故 A+A 与 S 不交。
- 第一阻塞点：当 |S|=𝔠 且只假设 sum-free 时，极大性覆盖式中的单个集合 S 已有连续统基数，基数计数立即失效；sum-free 本身也不提供 Sidon 构造所需的和表示唯一性。这是该路线的第一处缺口。
- 下一步：检验能否从任意连续统大小的 sum-free S 中抽取连续统大小的 Sidon 子集并保持平移构造对整个 S 的避让；若不能，构造使 (S-S) 或 (S-S-S)/2=ℝ 的 sum-free 候选以测试该策略的极限。
- 来源核对：[Erdős Problems #949](https://www.erdosproblems.com/949) 仍将一般情形列为 open，并记录 Sidon 特例的肯定证明。；本地 949.lean 包含 Sidon 特例的完整形式化证明，明确分为 #S<𝔠 的 Zorn 情形与 #S=𝔠 的平移构造情形。
- 时间记账：所在批次墙钟时间按题数均摊约 77.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/949)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/949.lean`；既有候选答案（按不可信材料审计）

### #950

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[f(n) = \sum_{p<n}\frac{1}{n-p}.\]Is it true that\[\liminf f(n)=1\]and\[\limsup f(n)=\infty?\]Is it true that $f(n)=o(\log\log n)$ for all $n$?
- 题意摘要：对每个整数 n，令 f(n)=∑_{p<n}(n-p)^{-1}，其中 p 遍历普通素数。问题分别问：当 n→∞ 时是否 liminf f(n)=1、limsup f(n)=∞，以及是否存在对所有充分大整数 n 一致成立的 f(n)/log log n→0。
- 状态核对：冻结日期及目前官方页面均标为 open。先验候选的 O(log log n) 方向基本可修正为严格论证，但它完全不能推出小 o。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：采用已知一、二阶矩并结合 Brun–Titchmarsh 的 dyadic 分块。由 ∑_{n<x}f(n)∼x 和 ∑_{n<x}f(n)^2∼x，直接展开 ∑(f(n)-1)^2=o(x)。另一方面按 d=n-p∈[2^j,2^{j+1}) 分块；除首尾块外，Brun–Titchmarsh 给该长度 2^j 区间内素数个数 O(2^j/j)，故每块贡献 O(1/j)。
- 局部结论：f(n)→1 依自然密度成立：对每个 ε>0，满足 |f(n)-1|≥ε 的 n≤x 只有 o(x) 个。因而存在子序列 f(n_k)→1，严格得到 liminf f≤1≤limsup f。；正确处理靠近 0 的末端块和 d=1 后，可得一致上界 f(n)=O(log log n)。先验候选的结论可保留，但区间端点及末块需要单独说明。；二阶矩还给出 #{n≤x:f(n)≥T}≤(1+o(1))x/T²。
- 第一阻塞点：Brun–Titchmarsh 每个 dyadic 块只给 O(1/j)，其隐常数不随 j 衰减；求和只能得到 O(log log n)，无法得到 o(log log n)。矩信息也只控制密度为 1 的典型 n，不能排除稀疏子序列上的极小值或任意大值。这是该路线第一处不能闭合三项猜想之处。
- 下一步：检验能否对大多数 dyadic 尺度建立统一节省：证明对每个 ε>0，所有充分大 n 都有 ∑_{j≤log₂n}2^{-j}(π(n-2^j)-π(n-2^{j+1}))≤ε log log n；先在可计算范围记录最坏 n 及贡献最大的尺度，以判断障碍来自少数短区间还是跨尺度累积。
- 来源核对：[官方题页](https://www.erdosproblems.com/950)目前仍标为 OPEN，并记录两矩渐近式及相应的短区间素数条件。；未把 Hardy–Littlewood 等启发式当作证明，也未从平均结论误推逐点结论。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/950)；既有候选答案（按不可信材料审计）

### #951

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1<a_1<\cdots$ be a sequence of real numbers such that\[\left\lvert \prod_i a_i^{k_i}-\prod_j a_j^{\ell_j}\right\rvert \geq 1\]for every distinct pair of non-negative finitely supported integer tuples $k_i,\ell_j\geq 0$. Is it true that\[\#\{ a_i \leq x\} \leq \pi(x)?\]
- 题意摘要：对象是严格递增实数列 1<a₁<a₂<⋯。对任意两个不同的有限支撑向量 k,ℓ∈ℕ₀^(ℕ)，要求相应乘积相差至少 1。问题中的 x 量词存在原始歧义：字面版问每个 x 是否 P(x):=#{i:a_i≤x}≤π(x)，本地 Lean 文件则形式化为对所有充分大 x。
- 状态核对：冻结时标为 open。现有官方页面明确指出“所有 x”与“充分大 x”并非同一问题：前者已有冻结日期之后出现的有限反例路线，后者仍被视为 open。因此不能不加区分地给单一结论。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先利用 1-分离把所有广义整数按大小嵌入普通整数格，再考察其 Dirichlet 级数；同时核对整数生成元这一可完全证明的特例。
- 局部结论：零向量与单生成元比较给 a_i≥2；两个单生成元比较给 |a_i-a_j|≥1，因此 P(x)≤⌊x⌋-1。不同乘积相等也被排除，所以乘法半群是自由的。；若 b 遍历全部广义整数，则其从 1 起两两相距至少 1，故对 s>1 有 ∑_b b^{-s}≤ζ(s)，即 ∏_i(1-a_i^{-s})^{-1}≤ζ(s)。这是一个严格的 Euler 乘积约束，但尚弱于 P(x)≤π(x)。；若所有 a_i 都是整数，则结论成立：把 a_i≤x 写成由 p≤x 给出的素指数向量。任何整数线性关系拆成正负部分都会产生两个相等乘积，故这些向量在 ℤ^{π(x)} 中线性无关，数量至多 π(x)。
- 第一阻塞点：实数情形没有有限秩的“素指数空间”；log a_i 可在 ℝ 的无限维 ℚ-向量结构中独立。Euler 乘积不等式只提供类似 Mertens 的加权约束，不能推出逐点的 π(x) 上界。这是整数特例向实数推广时的第一处断裂。
- 下一步：必须先固定量词版本。对冻结版最有价值的可检验任务是：对某个具体 X，用区间算术认证超过 π(X) 个生成元在所有低高度乘积间 1-分离，再用明确的 Diophantine 下界覆盖高高度乘积；若研究渐近版，则需构造无限多个违例 X，而单个有限反例不够。
- 来源核对：[官方题页](https://www.erdosproblems.com/951)目前仍标 OPEN，但明确说明“所有 x”已有有限反例，而“充分大 x”仍未解决。该信息晚于冻结日期，故只用于澄清量词，不能倒填为冻结时已知结果。；本地 951.lean 的主定理使用 eventually atTop，即只问所有充分大 x；它并不忠实表达字面上的“每个 x”。；先验候选的整数特例已独立核对，秩论证正确。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/951)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/951.lean`；既有候选答案（按不可信材料审计）

### #952

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there an infinite sequence of distinct Gaussian primes $x_1,x_2,\ldots$ such that\[\lvert x_{n+1}-x_n\rvert \ll 1?\]
- 题意摘要：问是否存在常数 C<∞及单射 x:ℕ→ℤ[i]，使每个 x_n 都是 Gaussian prime，且所有 n 都满足 |x_{n+1}-x_n|≤C。等价地，某个固定半径邻接图是否含无限射线；由于该图局部有限，这也等价于存在无限连通分支。
- 状态核对：冻结时及目前官方页面均标为 open；这是 Gordon–Motzkin 的 Gaussian moat 问题，而非 Erdős 原创。Lean 文件用 norm<C，其中 norm 是平方模且 C:ℤ，这与原题的欧氏距离常数版等价到更换常数，但形式略不自然。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：尝试用 Gaussian CRT 构造大块无素数区域，再判断它能否升级为封闭的无素数环带。对任意有限圆盘偏移集 F，给每个 z∈F 分配互异 Gaussian 素因子 π_z，解 w≡-z (mod π_z)，并在同余类中取足够大的 w。
- 局部结论：上述 CRT 构造严格给出任意大半径的 Gaussian-prime-free 圆盘：每个 w+z 都有指定非平凡因子，且取 w 足够大可排除其与该因子互为伴随。；因此 Gaussian 素数中存在任意大的局部空洞；这说明任何正面证明都不能依赖统一相对稠密性。；局部有限图中的无限连通分支可由 König 引理抽出一条无重复无限射线，所以图论重述成立；但“原点附近分支有限”本身不能排除远处存在另一无限分支。
- 第一阻塞点：CRT 圆盘不是围绕原点的闭合环带，路径可以绕过它。要否定固定 C 的无限路径，需要构造厚度>C、拓扑上分离内外区域的完整无素数闭曲线或环带；现有逐点同余条件无法同时把未知半径的一整圈格点协调为这种屏障。
- 下一步：固定小整数 C，形式化一个有限“环带证书”：列出一条格点闭曲线，使其 C-邻域内每个 Gaussian 整数都有显式非平凡因子，并用有限图搜索验证该曲线确实分离内外。成功只能排除该 C，但可检验 CRT 屏障路线的可扩展性。
- 来源核对：[官方题页](https://www.erdosproblems.com/952)目前仍标 OPEN，并注明 Erdős本人判断答案很可能是否定的；该判断只是启发式。；先验候选关于特定计算 moat 的数字未在本轮独立核验，故不作为局部结论使用。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/952)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/952.lean`；既有候选答案（按不可信材料审计）

### #953

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \{ x\in \mathbb{R}^2 : \lvert x\rvert <r\}$ be a measurable set with no integer distances, that is, such that $\lvert a-b\rvert \not\in \mathbb{Z}$ for any distinct $a,b\in A$. How large can the measure of $A$ be?
- 题意摘要：对给定 r>0，令 M(r) 为所有可测 A⊂B(0,r) 的面积上确界，条件是任意不同 a,b∈A 的距离不属于正整数。问题要求确定 M(r) 的增长阶或更精确界。
- 状态核对：冻结时为 open，输入记录 c r^0.26≲M(r)≲O(r)。目前题页仍标 OPEN，但有冻结日期之后的 M(r)≪r^{1/2} 声称，尚未被题库正式接纳；本筛查不把该声称当定理。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：沿任意固定方向作一维切片。若 S⊂ℝ 不含非零整数距离，把 S∩[m,m+1) 平移到 [0,1)；不同 m 所得集合互不相交，因此 |S|≤1。再对水平切片使用 Fubini。
- 局部结论：每个水平截面 A_y 的一维测度至多 1，故 |A|=∫|A_y|dy≤2r。更精确地，|A|≤∫_{-r}^r min(1,2√(r²-y²))dy。；当 0<r≤1/2 时，开圆盘内任意两点距离严格小于 1，因此整个 B(0,r) 都可取，精确得到 M(r)=πr²。；切片论证对任意方向均成立，但简单地对方向平均仍只恢复线性量级，不能自动产生幂次改进。
- 第一阻塞点：单方向切片只利用同一直线上的整数距离，完全忽略不同切片之间的大量禁距关系；即使对方向平均，也缺少把各方向的一维占用约束转化为次线性面积界的正定核或能量不等式。这是从 O(r) 改进时的第一处缺口。
- 下一步：验证一个明确的 Fourier–Bessel 子目标：构造径向正定核 K，其 Fourier 变换非负、K(m)在所有正整数半径处具有适当负性，并计算对 1_A 的能量不等式是否能推出 M(r)≪r^{1/2}。每个符号条件和截断误差都可独立数值及解析核验。
- 来源核对：[官方题页](https://www.erdosproblems.com/953)仍标 OPEN；页面现记录冻结后改进的下界 ≫_ε r^{1/2-ε}。；[讨论页](https://www.erdosproblems.com/forum/thread/953)含冻结后 M(r)≪r^{1/2} 的投稿声称及已指出的写作错误；未完成独立重建前不能据此宣称问题已解决。；先验候选的水平切片上界已独立复核，正确。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/953)；既有候选答案（按不可信材料审计）

### #954

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1=a_1<a_2<\cdots$ be the sequence of integers defined by $a_1=1$ and $a_{k+1}$ is the smallest integer $n$ for which the number of solutions to $a_i+a_j \leq n$ (with $i\leq j\leq k$) is less than $n-k$. Is the number of solutions to $a_i+a_j \leq x$ equal to $x+O(x^{1/4+o(1)})$?
- 题意摘要：输入采用去掉零元的编号：1=a₁<a₂<⋯，a_{k+1} 是使正指标旧对数 T_k(n):=#{1≤i≤j≤k:a_i+a_j≤n}<n-k 的最小 n。原题的计数结论必须把 a₀=0 及对 (0,j) 也算入；令 N(x)=#{0≤i≤j, j≥1:a_i+a_j≤x}，问题问 N(x)=x+O(x^{1/4+o(1)})。若结论也只数正指标对，就不是官方开放题。
- 状态核对：冻结时及目前官方页面均标为 open。人工评审指出先验候选漏掉 a₀=0，完全正确；其 N(a_k)=a_k-k 及由此声称反例的论证不能复述。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：研究离散差值 D(x)=N(x)-x，并利用贪心定义精确计算每次加入新 a_{k+1} 前后的值。设 a=a_{k+1}。由最小性，T_k(a-1)≥a-1-k；由定义及整数性，T_k(a)≤a-k-1。单调性迫使两者都等于 a-k-1。
- 局部结论：在 x=a_{k+1} 时，旧正指标对有 a-k-1 个，旧零对有 k 个，新零对 (0,k+1) 有一个，故严格得到 N(a_{k+1})=a_{k+1}，而不是先验候选的 a_{k+1}-(k+1)。；同理 N(a_{k+1}-1)=a_{k+1}-1。若 a_k≤x<a_{k+1}，贪心最小性给 T_k(x)≥x-k，故 N(x)=T_k(x)+k≥x。这重建了官方所说的全局下界。；令 r(t)=#{(i,j):a_i+a_j=t}（含零指标），则 D(t)-D(t-1)=r(t)-1；每个区间 [a_k,a_{k+1}-1] 的两端 D=0，且内部 D≥0。因此目标等价于控制这些非负“桥”的最大高度为 x^{1/4+o(1)}。
- 第一阻塞点：贪心规则只规定桥何时首次回到 0，并不直接限制中间某个 t 上许多和 a_i+a_j 的聚集。缺少对表示函数 r(t) 的四阶能量或最大局部累积 ∑(r(t)-1) 的上界；这正是无法由端点恒等式推出 O(x^{1/4+o(1)}) 的第一步。
- 下一步：生成前若干项并逐区间计算 H_k=max_{a_k≤x<a_{k+1}}D(x)，同时计算加法能量 E_k=#{a_i+a_j=a_u+a_v≤a_{k+1}}；检验能否严格建立 H_k^4≲x^{1+o(1)}E_k的归一化版本，再寻找由贪心性质控制 E_k 的组合引理。
- 来源核对：[官方题页](https://www.erdosproblems.com/954)明确使用 a₀=0，并要求计数 0≤i≤j、j≥1；也记录 N(x)≥x。；输入中的 n-k 递推与加入 k 个旧零对后的官方递推相容，但最终计数若省略零对就会改变问题。；已明确吸收人工评审：先验候选的所谓 √x 反例源于漏计全部 (0,j)，结论无效。
- 时间记账：所在批次墙钟时间按题数均摊约 55.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/954)；既有候选答案（按不可信材料审计）

### #955

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[s(n)=\sigma(n)-n=\sum_{\substack{d\mid n\\ d<n}}d\]be the sum of proper divisors function. If $A\subset \mathbb{N}$ has density $0$ then $s^{-1}(A)$ must also have density $0$.
- 题意摘要：断言为：对任意固定集合 A⊆N，若其渐近密度 lim_{y→∞}|A∩[1,y]|/y=0，则集合 {n∈N:s(n)∈A} 也具有渐近密度 0；不是关于随 x 变化的集合 A_x 的一致命题。
- 状态核对：截至冻结日期仍为 EGPS 开放猜想。先前候选正确判断未解决，但列举了官方材料未包含的特殊集合，且没有给出证明筛查；这些不能当作解答。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试把 n≤x 按 s(n)≤εn 与 s(n)>εn 分割，再在后一部分利用 A 的稀疏性和 divisor-sum fiber 上界。
- 局部结论：若 p(n) 是 n 的最小素因子，则对合数 n 有 s(n)≥n/p(n)。因此 s(n)≤εn 蕴含 p(n)≥1/ε。；由有限筛，limsup_{x→∞}x⁻¹#{n≤x:s(n)≤εn}≤∏_{p<1/ε}(1−1/p)，该上界随 ε↓0 趋于 0；故“小 aliquot sum”部分可严格忽略。；对其余 n≤x，有 εx<s(n)≪x log log x。因此目标归结为控制落入 A∩[εx,O(x log log x)] 的纤维总和；PPT 定理在该截断集合大小至多 x^{1/2+o(1)} 时确实给出 o(x)。
- 第一阻塞点：密度零只给 |A∩[1,O(x log log x)]|=o(x log log x)，可能远大于 x^{1/2+o(1)}。现有路线缺少足够一致的纤维估计，不能排除 A 选择许多异常大纤维；这正是第一处无法闭合的步骤。
- 下一步：检验一个明确的加强命题：是否能对所有 B⊆[εx,O(x log log x)] 证明 ∑_{a∈B}#{n≤x:s(n)=a}=o(x)+Oε(|B|/log log x)；先在 B 位于单个 dyadic 区间时测试。
- 来源核对：[官方问题页](https://www.erdosproblems.com/955)确认一般情形开放，并记录 PPT 的 x^{1/2+o(1)} 稀疏集结论。；未采信先前候选中没有在官方材料或原论文中核对的“回文数、缺失数字”等扩展。
- 时间记账：所在批次墙钟时间按题数均摊约 53.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/955)；既有候选答案（按不可信材料审计）

### #956

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $C,D\subseteq \mathbb{R}^2$ then the distance between $C$ and $D$ is defined by\[\delta(C,D)=\inf_{\substack{c\in C\\ d\in D}}\| c-d\|.\]Let $h(n)$ be the maximal number of unit distances between disjoint convex translates. That is, the maximal $m$ such that there is a compact convex set $C\subset \mathbb{R}^2$ and a set $X$ of size $n$ such that all $(C+x)_{x\in X}$ are disjoint and there are $m$ pairs $x_1,x_2\in X$ such that\[\delta(C+x_1,C+x_2)=1.\]Determine $h(n)$ - in particular, prove that there exists a constant $c>0$ such that $h(n)>n^{1+c}$ for all large $n$.
- 题意摘要：h(n) 是在同一个紧凸集 C 的 n 个两两不相交平移 C+x（x∈X）中，距离恰为 1 的无序平移对的最大数；要求特别证明存在固定 c>0，使所有充分大的 n 都有 h(n)>n^{1+c}。
- 状态核对：按冻结日期为开放题，已知 h(n)≪n^{4/3}。2026 年以后出现了相关新稿和网页评论，但尚不足以把题中“所有充分大 n”按本次冻结状态改判为已解决。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `medium`
- 尝试路线：令 D=C−C，把问题化为差向量落在欧氏平行体的边界，再尝试从平面单位距离构造取得下界。
- 局部结论：严格恒等式为 δ(C+x,C+y)=dist(y−x,D)，且平移不相交等价于 y−x∉D。；因此距离为 1 等价于 y−x∈∂(D+B_2)，问题成为带有差集避碰约束的自平移关联问题。；取 C 为单点即得 h(n)≥U(n)。2026 年的一篇新稿证明某个固定 δ>0 及无穷多个 n 满足 U(n)≥n^{1+δ}，因而至少沿一个无穷子序列有 h(n)≥n^{1+δ}。
- 第一阻塞点：无穷子序列不能推出“所有充分大 n”：添加远离的孤立平移只保证 h(N+t)≥h(N)，除非还能控制相邻构造规模的增长。现有数域塔构造没有在此路线中给出所需的多项式稠密规模序列。
- 下一步：从新单位距离构造中提取点数 n_j 的显式增长率，检验能否证明 n_{j+1}≤n_j^K；若能，则填充法可把子序列指数下界降指数后推广到所有大 n。
- 来源核对：[官方讨论页](https://www.erdosproblems.com/forum/thread/956)仍标为开放，并警告评论中的 Θ(n^{4/3}) 声称未经核验。；[2026 单位距离预印本](https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf)只明言固定指数下界对无穷多个 n 成立。；先前候选声称“两条凸曲线的不同平移至多交两点”是错误的：例如圆角正方形边界作适当水平平移会共享线段；故其伪圆证明不能照录。
- 时间记账：所在批次墙钟时间按题数均摊约 53.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/956)；既有候选答案（按不可信材料审计）

### #959

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A\subset \mathbb{R}^2$ be a set of size $n$ and let $\{d_1,\ldots,d_k\}$ be the set of distinct distances determined by $A$. Let $f(d)$ be the number of times the distance $d$ is determined, and suppose the $d_i$ are ordered such that\[f(d_1)\geq f(d_2)\geq \cdots \geq f(d_k).\]Estimate\[\max (f(d_1)-f(d_2)),\]where the maximum is taken over all $A$ of size $n$.
- 题意摘要：对每个 n 点集 A，把所有无序点对距离的 multiplicity 降序为 f(d_1)≥f(d_2)≥…；所求 M(n)=max_{|A|=n}(f(d_1)−f(d_2))，最大值同时允许点集及最常见距离变化。
- 状态核对：冻结状态为开放；当前可核对的范围是 Ω(n log n)≤M(n)≤O(n^{4/3})。先前候选的这两个界与文献一致，但并未估定正确阶。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把最常见距离缩放成单位距离，以上界约化到单位距离图；下界采用 Clemen–Dumitrescu–Liu 的可指定高 multiplicity 构造。
- 局部结论：对任意 A，f(d_1)−f(d_2)≤f(d_1)≤U(n)，故 Spencer–Szemerédi–Trotter 上界给 M(n)=O(n^{4/3})。；CDL 构造对 r=1 给出某个 n 点集满足 f(d_1)−f(d_2)≥c n log n，故 M(n)=Ω(n log n)。；新的超线性单位距离构造本身不能改善此差值下界：它只保证某个距离出现很多次，未保证第二大 multiplicity 显著较小。
- 第一阻塞点：单位距离上界完全丢弃了减项 f(d_2)。要改进它，必须证明一个稳定性结论：距离图接近 U(n) 条边时，另一种距离也必有很多边；目前路线没有这种双距离关联定理。
- 下一步：先检验可证的门槛版本：给定 f(d_1)≥n^{4/3−η}，能否由高能量或圆关联稳定性推出 f(d_2)≥n^{4/3−Cη}；即使弱指数也会直接改进差值上界。
- 来源核对：[CDL 原始预印本](https://arxiv.org/abs/2505.04283)的摘要明确给出 f(d_r)−f(d_{r+1})=Ω(n log n/r)，适用 1≤r≤log n。；[官方问题页](https://www.erdosproblems.com/959)仍将精确估计列为开放问题。
- 时间记账：所在批次墙钟时间按题数均摊约 53.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/959)；既有候选答案（按不可信材料审计）

### #960

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $r,k\geq 2$ be fixed. Let $A\subset \mathbb{R}^2$ be a set of $n$ points with no $k$ points on a line. Determine the threshold $f_{r,k}(n)$ such that if there are at least $f_{r,k}(n)$ many ordinary lines (lines containing exactly two points) then there is a set $A'\subseteq A$ of $r$ points such that all $\binom{r}{2}$ many lines determined by $A'$ are ordinary. Is it true that $f_{r,k}(n)=o(n^2)$, or perhaps even $\ll n$?
- 题意摘要：固定 r,k。对满足每条直线至多含 k−1 个点的 n 点集 A，定义普通线图 G_A：顶点为 A，两点相连当且仅当它们所张直线在整个 A 中恰含这两点。f_{r,k}(n) 是边数达到多少即可强迫 G_A 含 K_r 的阈值。
- 状态核对：已被否证：对每个固定 r≥3、k≥4，存在无 K_r 的普通线图却有 n²/12−O(n) 条边，所以 f_{r,k}(n) 不是 o(n²)。先前候选只给 Θ(n) 的三次曲线构造，并错误地把线性上界继续当作开放可能；必须弃用。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 2026 年反例：在实非奇异三次曲线的 7m 阶循环子群 C 中，令 H 为指数 7 子群，并取 A_0=C\H，即六个非零模 7 余类。
- 局部结论：Bézout 定理保证一条直线至多与该三次曲线相交三次，故 A_0 无四点共线，因而满足所有 k≥4 的限制。；若 x∈C_i、y∈C_{−i}，第三交点 −x−y 位于被删去的 H，故 xy 在 A_0 中为普通线；三个相反余类对共贡献 3m² 条普通线。；逐项检查普通边的模 7 类型可将 G_{A_0} 二染色，所以它无 K_3，进而无任何 K_r（r≥3）。对 n=6m+s 加回至多五个特选 H 点，仍二部且普通线数至少 n²/12−(10/3)n。
- 第一阻塞点：该反例路线已经闭合；它不确定 f_{r,k}(n) 的精确二次常数，只留下 n²/12−O(n) 与 Turán 上界 (1−1/(r−1))n²/2+O(1) 之间的差距。
- 下一步：下一项可检验任务是针对首个参数 r=3,k=4，求普通线图无三角形时可达到的最佳二次密度，先判断 1/12 是否能由其他模数余类构造提高。
- 来源核对：[官方问题页](https://www.erdosproblems.com/forum/thread/960?order=newest)记录 f_{r,k}(n)≥n²/12−O(n) 并标为 DISPROVED。；[原始预印本](https://arxiv.org/pdf/2604.06609)定理 2.1 给出显式界 n²/12−(10/3)n，并证明补点后的普通线图仍为二部图。
- 时间记账：所在批次墙钟时间按题数均摊约 53.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/960)；既有候选答案（按不可信材料审计）

### #961

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(k)$ be the minimal $n$ such that every set of $n$ consecutive integers $>k$ contains an integer divisible by a prime $>k$. Estimate $f(k)$.
- 题意摘要：对每个正整数 k，f(k) 是最小正整数 L，使任意起点 m≥k+1 的连续块 {m,…,m+L−1} 中都有一个整数含素因子 p>k。等价地，若最长的全体素因子均≤k 的连续整数串长度为 R(k)，则 f(k)=R(k)+1。
- 状态核对：开放。已知上界 f(k)≪(k/log k)(log log log k/log log k)，猜测至多为 log k 的固定幂。先前候选声称“正确阶应为 (log k)²”及给出 Rankin 型下界，但没有提供可核对来源；本次不将其作为已知结论。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试由短区间内素因子的唯一归属来重建 Sylvester–Schur 上界，并用素数间隙给出可直接验证的下界机制。
- 局部结论：Sylvester–Schur 引理断言任意 k 个连续且均大于 k 的整数之积含素因子 >k，因此严格得到 f(k)≤k。；若 p<q 是相邻素数且 k≤p<q≤2k，则 p+1,…,q−1 全为合数且小于等于 2k；其中任何素因子都≤k。因此这是长度 q−p−1 的 k-smooth 串，得到 f(k)≥q−p。；对长度 L≤k 的假定 k-smooth 区间，每个素数 p∈(L,k] 至多整除其中一个数。这给出“较大素因子可指派到唯一项”的结构约束。
- 第一阻塞点：唯一指派不足以限制区间长度：一个区间元素可同时吸收多个 p∈(L,k]，而 p≤L 的高次幂又可分布到多个元素。若无关于这些素因子乘积或二项式系数估值的全局不等式，不能从该路线推出多对数上界。
- 下一步：固定 L=C(log k)^C，计算并界定区间乘积中来自 p≤L 的总 p-adic 贡献，再检验剩余的 p∈(L,k] 是否能通过“每素数至多命中一项”与每项大小联合产生矛盾。
- 来源核对：[官方问题页](https://www.erdosproblems.com/961)确认经典上界和多对数猜测。；本地 Lean 文件正确使用 m≥k+1 和 `smoothNumbers (k+1)` 表示素因子≤k；但主猜想仍含 `answer(sorry)`，不能视为形式化证明。；先前候选的素数间隙论证仅在明确满足 k≤p<q≤2k 时成立；已补上这一缺失量词。
- 时间记账：所在批次墙钟时间按题数均摊约 53.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/961)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/961.lean`；既有候选答案（按不可信材料审计）

### #962

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k(n)$ be the maximal $k$ such that there exists $m\leq n$ such that each of the integers\[m+1,\ldots,m+k\]are divisible by at least one prime $>k$. Estimate $k(n)$.
- 题意摘要：对每个正整数 n，k(n) 是所有整数 k 中的最大者，使得存在整数 m≤n，并且对每个 1≤i≤k，m+i 都有某个素因子 >k；等价地，区间 (m,m+k] 不含 k-smooth 数。目标是估计 k(n)，尤其控制 log k(n)。
- 状态核对：截至官方页面 2026-04-03 更新仍为开放。已记录 Tang 下界 log k(n)≥(1/√2−o(1))√(log n log log n)，以及 Tao 上界 k(n)≤(1+o(1))√n。先前候选把 Tao 路线说成“指定素数必为最大素因子”，这一点没有必要且未充分论证；真正需要证明的是该倍数的所有素因子均 <k。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：核对 Tao 的上界。固定 ε>0，反设 k≥(1+ε)√n。由素数定理，在 (√n,(1+δ)√n) 中选素数 p，其中 0<δ<ε。因 k>p，任意长度为 k 的整数区间都含 p 的倍数 N=m+i。又 N≤n+k。写 N=pr，则 r≤(n+k)/p=(1+o(1))√n<k；同时 p<k。因此 N 的每个素因子不是 p 就整除 r，全部小于 k，与定义矛盾。于是对每个 ε>0，充分大 n 有 k(n)<(1+ε)√n。
- 局部结论：条件严格等价于 P⁺(m+i)>k（1≤i≤k），即所给区间无 k-smooth 数。；上述论证严格给出 k(n)≤(1+o(1))√n；关键只用短乘法区间中存在素数及“长度 ≥p 的区间含 p 的倍数”。；若欲把上界降到 n^{1/2-c}，同一“找一个合适素数的倍数”路线失效：此时区间长度 k 可能小于所有约 √n 的素数，不能保证命中其倍数。
- 第一阻塞点：第一处不能闭合的是从“排除 k>(1+ε)√n”推进到题目预期的次多项式上界；需要证明每个候选长区间都含某个 k-smooth 数，而现有单素数倍数论证在 k≪√n 时没有覆盖保证。
- 下一步：对固定 k、m，把区间内各素数 p>k 至多贡献一个倍数这一事实写成筛上界；检验能否由 Σ_{p>k, p|(m+1)…(m+k)}1 覆盖 k 个位置推出关于 m、k 的新限制，并与 Erdős 的 exp(−(log n)^c)√n 上界比较。
- 来源核对：[Erdős Problems #962](https://www.erdosproblems.com/962) 核实开放状态及当前上下界。；[问题讨论中 Tao 的原始上界说明](https://www.erdosproblems.com/forum/thread/962) 核实具体倍数论证。
- 时间记账：所在批次墙钟时间按题数均摊约 40.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/962)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/962.lean`；既有候选答案（按不可信材料审计）

### #963

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the maximal $k$ such that in any set $A\subset \mathbb{R}$ of size $n$ there is a subset $B\subseteq A$ of size $\lvert B\rvert\geq k$ which is dissociated that is, the sums $\sum_{b\in S}b$ are distinct for all $S\subseteq B$. Estimate $f(n)$ - in particular, is it true that\[f(n)\geq \lfloor \log_2 n\rfloor?\]
- 题意摘要：令 d(A) 为有限实数集 A 所含最大耗散子集的大小，其中 B 耗散是指映射 S↦Σ_{b∈S}b 在 2^B 上单射。则 f(n)=min_{A⊂R, |A|=n}d(A)。问题是估计 f(n)，特别问对所有 n 是否 f(n)≥⌊log₂n⌋。
- 状态核对：官方页面截至 2026-01-23 仍标为开放，只确认 Erdős 的贪心下界。先前候选引用的未来预印本及论坛草图不作为已验证结论；这里仅保留可独立核查的论证。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：取 A 中一个按包含极大的耗散集 B，记 r=|B|。若 a∈A\B，则 B∪{a} 不耗散，故存在不同子集具有相同和。由于 B 本身耗散，该关系中 a 的系数必为 ±1；移项得 a=Σ_{b∈B}ε_b b，ε_b∈{−1,0,1}。因此 A 包含于 B 的三进制有符号张成中，故 n≤3^r。
- 局部结论：严格得到 r≥⌈log₃n⌉，从而 f(n)≥⌈log₃n⌉，略强于题面所引的 ⌊log₃n⌋。；耗散性等价于不存在非零的 {−1,0,1}-系数线性关系。；取 A={1,…,n}，若 B⊂A 耗散且 |B|=r，则 2^r 个不同整数子集和都落在 [0,rn]，所以 2^r≤rn+1，进而 f(n)≤log₂n+O(log log n)。因此 f(n)=Θ(log n)。
- 第一阻塞点：要把底数 3 改成 2，必须把最大耗散集的 {−1,0,1}-张成中可能容纳的 A 元素数从 3^r 降到约 2^r；仅凭极大性无法排除三类系数模式，且耗散性只保证子集和唯一，并不保证所有有符号和唯一。
- 下一步：对小 r 穷举可实现的有符号关系型（按有理线性同构归类），检验命题：若 B 是 A 中最大耗散集，则 |A|≤2^{r+1} 或某个更接近 2^r 的界；先从 r≤5 寻找反例或可归纳结构。
- 来源核对：[Erdős Problems #963](https://www.erdosproblems.com/963) 核实量词、开放状态和贪心下界。
- 时间记账：所在批次墙钟时间按题数均摊约 40.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/963)；既有候选答案（按不可信材料审计）

### #965

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：For every two-colouring of $\mathbb R$, must there be $A\subseteq\mathbb R$ of cardinality $\aleph_1$ such that all $a+b$ with distinct $a,b\in A$ have one colour?
- 题意摘要：原命题量化为：对每个二染色 F:R→{0,1}，是否存在 |A|=ℵ₁，使所有不同 a,b∈A 的和 a+b 同色？否定它只需构造一个二染色，使每个基数 ℵ₁ 的 A 的两两不同元素之和同时出现两色。
- 状态核对：已被无条件否证，不应再尝试证明原命题。Soukup–Weiss 与 Komjáth 独立在 ZFC 中构造反例；结论更强，适用于任意不可数 A 及任意固定 N≥2 的 N 项互异和。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 Soukup–Weiss 路线：先在 Cantor 空间的有限子集 [2^ω]^{<ω} 上构造染色 f，使任意不可数族 X 的 N 个不同成员之并集可取得两色。构造使用首次分歧位置 Δ、选出实现最大 Δ 的规范二元组 π(a)，再以 Sierpiński 染色给 f(a)=g(π(a))。随后取 R 在 Q 上的 Hamel 基并以 2^ω 编号，把实数映到其有限支撑；经 Δ-system/抽稀，使所选实数之和的支撑等于支撑之并，从而令 F(r)=f(supp(r))。取 N=2 即得原问题的反例。
- 局部结论：文献定理直接给出：存在 F:R→2，使每个不可数 X⊂R 的互异二元和集合 F''{x+y:x≠y∈X}=2。；由于 |A|=ℵ₁ 必为不可数，该定理立即否定题面中的全称命题，不依赖连续统假设。；Hamel 支撑归约解释了为何有限集合的“并”染色足以产生实数加法染色；Δ-system 抽稀负责控制公共支撑和系数抵消。
- 第一阻塞点：在本次受限重建中，第一处不自行完全展开的是核心有限集染色定理：从任意不可数 X⊂[2^ω]^{<ω} 抽出规范形，并证明可选择两对成员使 Sierpiński 颜色相反。该步骤在 Soukup–Weiss 定理 3.1 中已有完整证明，因此不构成已知结论的缺口。
- 下一步：逐行形式化文献 Lemma 2.1 与 Theorem 3.1 的 N=2 特例，特别核验“支撑之和等于支撑之并”的抽稀步骤及共同根上的系数处理。
- 来源核对：[Erdős Problems #965](https://www.erdosproblems.com/965) 核实无条件否证状态及独立作者。；[Soukup–Weiss, Sums and anti-Ramsey colourings of R](https://danieltsoukup.github.io/academic/finset_colouring.pdf) 核实 Lemma 2.1、Theorem 3.1 和 Corollary 3.2 的 ZFC 构造。
- 时间记账：所在批次墙钟时间按题数均摊约 40.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/965)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/965.lean`

### #968

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $u_n=p_n/n$, where $p_n$ is the $n$th prime. Does the set of $n$ such that $u_n<u_{n+1}$ have positive density?
- 题意摘要：设 p_n 为第 n 个素数、u_n=p_n/n。问题是集合 I={n∈N:u_n<u_{n+1}} 是否具有正下密度，即是否存在 c>0，使所有充分大 N 都有 |I∩[1,N]|≥cN。
- 状态核对：截至官方页面 2026-03-31 仍开放。已知反向不等式 u_n>u_{n+1} 的指标集有正密度，但这不蕴含正向集合也有正密度。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：令 g_n=p_{n+1}−p_n。直接化简得 u_{n+1}>u_n 当且仅当 ng_n>p_n，即 g_n>p_n/n。再尝试利用 Erdős–Prachar 的总变差估计。若 N=π(x)，则 Σ_{n<N}(u_{n+1}−u_n)=u_N−u_1=O(log x)，而 Σ_{n<N}|u_{n+1}−u_n|≍(log x)^2。因此正变差总量 V_+(x) 与负变差总量 V_−(x) 都为 Θ((log x)^2)。
- 局部结论：题目严格等价于问超过阈值 p_n/n∼log p_n−1 的素数间隙是否占正比例。；总变差估计与望远镜恒等式推出正向跳跃的总质量 V_+(x)≍(log x)^2，故 u_{n+1}>u_n 至少发生无穷多次。；上述质量结论本身不能给正密度：少量异常大的素数间隙原则上可以承载全部正变差。
- 第一阻塞点：第一处无法闭合的是把 V_+(x)≍(log x)^2 转换为正向指标数 ≫π(x)。这要求对单次正跳跃或稀疏大间隙的总贡献作足够强的均匀可积性控制；现有最大间隙上界只会给远弱于线性的计数。
- 下一步：按 dyadic 层分解 g_n/(p_n/n)：分别估计 2^j<g_n/(p_n/n)≤2^{j+1} 对 V_+ 的贡献；检验现有大筛或 Selberg 筛尾界是否能证明任意 o(π(x)) 个最大间隙贡献 o((log x)^2)。
- 来源核对：[Erdős Problems #968](https://www.erdosproblems.com/968) 核实正下密度解释、开放状态及 Erdős–Prachar 总变差结论。
- 时间记账：所在批次墙钟时间按题数均摊约 40.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/968)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/968.lean`；既有候选答案（按不可信材料审计）

### #969

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $Q(x)$ count the number of squarefree integers in $[1,x]$. Determine the order of magnitude in the error term in the asymptotic\[Q(x)=\frac{6}{\pi^2}x+E(x).\]
- 题意摘要：Q(x)=|{n≤x:n 无平方素因子}|，并定义 E(x)=Q(x)−x/ζ(2)。问题要求 E(x) 的真实数量级，而不只是证明某个上界。
- 状态核对：仍为开放；已知无条件上界为 Walfisz 型 x^{1/2−o(1)}，且有 x^{1/4} 级别的下方振荡；即使假设 RH，真实数量级也未知。人工评审正确指出先前候选只重证 O(√x)，遗漏 PNT 给出的 o(√x) 及更强的已知上界；故不能把 O(√x) 称为答案。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：从 μ²(n)=Σ_{d²|n}μ(d) 得 Q(x)=Σ_{d≤√x}μ(d)⌊x/d²⌋。这立即给 E(x)=O(√x)。为吸收 PNT 的改进，令 M(t)=Σ_{d≤t}μ(d)=o(t)。固定 η>0，把 d≤η√x 与其余部分分开：前段逐项处理仅为 O(η√x)；后段中 ⌊x/d²⌋ 只取 O_η(1) 个整数值，每一取值区间上的 μ 和是两个 M 值之差，因而为 o(√x)。尾和 xΣ_{d>√x}μ(d)/d² 由分部求和也是 o(√x)。先令 x→∞、再令 η→0，得到 E(x)=o(√x)。
- 局部结论：恒等式 Q(x)=Σ_{d≤√x}μ(d)⌊x/d²⌋ 严格给出初等界 E(x)=O(√x)。；使用与素数定理等价的 M(t)=o(t)，按上述双极限分割可严格改进为 E(x)=o(√x)。；Dirichlet 级数 Σ μ²(n)n^{-s}=ζ(s)/ζ(2s) 表明若 E(x)=O(x^{1/4})，经 Mellin/Abel 求和会迫使 1/ζ(2s) 在 Re(s)>1/4 所需的解析性，从而排除 ζ 在 Re(s)>1/2 的零；配合对称性可推出 RH。
- 第一阻塞点：第一处无法闭合的是由 M(t)=o(t) 得到 Walfisz 型显式节省，更遑论 x^{1/4} 量级。简单 Möbius 截断无法控制取整误差中的精细相关；需要 ζ 的零点零区、指数和及优化的双曲分割。
- 下一步：从 Perron 公式作用于 ζ(s)/ζ(2s) 出发，明确移动积分线时 1/ζ(2s) 的零点零区所允许的轮廓，并复算 Walfisz 指数型因子；这可检验当前路线能否超越抽象的 o(√x)。
- 来源核对：[Erdős Problems #969](https://www.erdosproblems.com/969) 核实开放状态、PNT 改进、Walfisz 上界、x^{1/4} 下界及 RH 条件结果。
- 时间记账：所在批次墙钟时间按题数均摊约 40.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/969)；既有候选答案（按不可信材料审计）

### #970

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(k)$ be Jacobsthal's function, defined to as the minimal $m$ such that, if $n$ has at most $k$ prime factors, then in any set of $m$ consecutive integers there exists an integer coprime to $n$. Determine the order of magnitude of $h(k)$. In particular, is it true that\[h(k) \ll k^2?\]
- 题意摘要：令 \(\omega(n)\) 为不同素因子数，\(j(n)\) 为每个长度 \(m\) 的连续整数块均含与 \(n\) 互素整数的最小 \(m\)。题目等价于研究 \(h(k)=\max_{\omega(n)\le k}j(n)\)，并问是否存在绝对常数 \(C\) 使所有 \(k\) 都有 \(h(k)\le Ck^2\)。
- 状态核对：按冻结资料仍开放；已知 \(h(k)\ll(k\log k)^2\)。旧候选把 FGKMT 的区间筛下界换元成 \(k(\log k)^2\log_3k/\log_2k\)，与题给官方下界不一致，故不采纳该未经核清的增强式。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先从覆盖同余类构造下界。取不同素数 \(q_1,\ldots,q_k\)，由中国剩余定理选择 \(N\) 满足 \(N+i\equiv0\pmod{q_i}\)（\(1\le i\le k\)），并令 \(n=\prod q_i\)。于是 \(N+1,\ldots,N+k\) 均不与 \(n\) 互素。
- 局部结论：幂次不影响互素性，故极值中可把 \(n\) 换成其平方自由核。；上述 CRT 构造严格给出 \(j(n)\ge k+1\)，从而 \(h(k)\ge k+1\)。；\(h(k)\) 随 \(k\) 单调不减；问题的困难在于对任意选择的至多 \(k\) 个素数和任意平移给出统一上界。
- 第一阻塞点：要得到 \(O(k^2)\)，必须证明长度 \(Ck^2\) 的区间不可能被每个素数各一个剩余类完全覆盖；直接容斥含有高阶交项，当前筛法只能留下对数损失。
- 下一步：把 Iwaniec 上界所用筛权重写成关于 \(\sum_{p\mid n}1/p\) 的显式不等式，逐项定位产生两个 \(\log k\) 因子的估计，并检验其中一个能否在“大素因子/小素因子”分拆后消除。
- 来源核对：冻结题面所引 Iwaniec 1978 与 FGKMT 2018 的结论彼此相容，但不支持旧候选给出的增强换元。；核对了 [FGKMT 论文页面](https://www.ams.org/jams/2018-31-01/S0894-0347-2017-00876-2/)。
- 时间记账：所在批次墙钟时间按题数均摊约 56.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/970)；既有候选答案（按不可信材料审计）

### #971

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p(a,d)$ be the least prime congruent to $a\pmod{d}$. Does there exist a constant $c>0$ such that, for all large $d$,\[p(a,d) > (1+c)\phi(d)\log d\]for $\gg \phi(d)$ many values of $a$?
- 题意摘要：应量化为：是否存在绝对常数 \(c,\delta>0\) 和 \(d_0\)，使每个 \(d\ge d_0\) 至少有 \(\delta\varphi(d)\) 个约化剩余类 \(a\bmod d\) 满足其最小同余素数 \(p(a,d)>(1+c)\varphi(d)\log d\)。
- 状态核对：在线页面在 2026 年仍标为开放。Erdős 只证明了对无穷多个模数成立，不能把该量词改成“所有充分大的 \(d\)”。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：令 \(x=(1+c)\varphi(d)\log d\)，并令 \(N_a=\#\{p\le x:p\equiv a\pmod d\}\)。目标正是证明正比例的 \(a\) 满足 \(N_a=0\)。先计算横跨剩余类的一阶矩。
- 局部结论：有精确恒等式 \(\sum_{(a,d)=1}N_a=\#\{p\le x:(p,d)=1\}=\pi(x)-O(\omega(d))\)。；由素数定理及 \(\log\varphi(d)\sim\log d\)，平均值为 \(\varphi(d)^{-1}\sum_aN_a\sim1+c\)。；因此单靠一阶矩至多给出“被占用类数不超过素数总数”；因平均值大于 1，这不能推出任何空类，更不能推出正比例空类。
- 第一阻塞点：需要控制 \(\sum_a(N_a)_r\) 的若干高阶阶乘矩；展开后变成对间距为 \(d\) 的素数 \(r\)-元组作关于 \(d\) 的统一渐近。这正是目前无条件方法不能闭合之处。
- 下一步：先做最小可检验环节：对 \(r=2\) 数值及理论地研究 \(\sum_aN_a(N_a-1)\)，并明确现有大筛或 Selberg 筛能否在所有 \(d\) 上给出足以配合 Brun 截断的常数级上、下界。
- 来源核对：[Erdős 问题 971](https://www.erdosproblems.com/971) 当前仍列为 OPEN。；页面讨论给出的 Poisson 推导明确依赖统一 Hardy–Littlewood 素数元组假设，不能当作无条件证明。
- 时间记账：所在批次墙钟时间按题数均摊约 56.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/971)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/971.lean`；既有候选答案（按不可信材料审计）

### #972

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\alpha>1$ be irrational. Are there infinitely many primes $p$ such that $\lfloor p\alpha\rfloor$ is also prime?
- 题意摘要：量词是：对每一个固定的无理数 \(\alpha>1\)，是否存在无穷多个素数 \(p\)，使整数 \(\lfloor\alpha p\rfloor\) 也为素数；不是“几乎所有 \(\alpha\)”或允许 \(\alpha\) 随 \(p\) 改变。
- 状态核对：按冻结资料仍开放。旧候选的几乎处处结果即使准确，也不能解决“每个无理数”的量词。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：把 Vinogradov 的素数上等分布用于固定有限筛。给定平方自由 \(Q\)，条件 \(\lfloor\alpha p\rfloor\equiv r\pmod Q\) 等价于 \(\{\alpha p/Q\}\in[r/Q,(r+1)/Q)\)。因 \(\alpha/Q\) 无理，可在素数上对这些区间应用等分布。
- 局部结论：对每个固定 \(Q\)，有 \(\#\{p\le X:(\lfloor\alpha p\rfloor,Q)=1\}=(\varphi(Q)/Q+o_{\alpha,Q}(1))\pi(X)\)。；因此对任意固定有限素数集合 \(S\)，存在无穷多个素数 \(p\)，使 \(\lfloor\alpha p\rfloor\) 不被 \(S\) 中任何素数整除。；特别地，奇偶障碍并不存在：除有限例外，约一半素数 \(p\) 使 \(\lfloor\alpha p\rfloor\) 为奇数。
- 第一阻塞点：判定 \(\lfloor\alpha p\rfloor\) 为素数要求筛去增长到约 \(\sqrt{\alpha X}\) 的素数；Vinogradov 的定性等分布只对固定模数有效，且普通筛在维数一处遭遇奇偶性障碍，不能产生素数下界。
- 下一步：对一类有明确丢番图型界的 \(\alpha\)（先取二次无理数）证明 \(Q\) 随 \(X\) 增长时的素数指数和一致估计，量化固定有限筛可推进到的最大筛水平。
- 来源核对：冻结题面所引 Vinogradov 定理只给 \(\{p\alpha\}\) 的等分布，不给两个数同时为素数。；未采用旧候选中“几乎处处”结论来替代原题的全称量词。
- 时间记账：所在批次墙钟时间按题数均摊约 56.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/972)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/972.lean`；既有候选答案（按不可信材料审计）
- 深度项目：深度来源审计的第一阻塞点是精确的外部解析数论定理：对每个固定无理数 $\alpha>1$，需证明 $\#\{p<X:p,\lfloor\alpha p\rfloor\ \text{均为素数}\}\gg_\alpha X/(\log X)^2$（或等价相关下界）。普通的 Beatty 序列素数渐近不能替代这个双素数相关。 [证据](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-03/state.json)

### #973

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does there exist a constant $C>1$ such that, for every $n\geq 2$, there exists a sequence $z_i\in \mathbb{C}$ with $z_1=1$ and $\lvert z_i\rvert \geq 1$ for all $1\leq i\leq n$ with\[\max_{2\leq k\leq n+1}\left\lvert \sum_{1\leq i\leq n}z_i^k\right\rvert < C^{-n}?\]
- 题意摘要：问是否存在一个与 \(n\) 无关的 \(C>1\)，使每个 \(n\ge2\) 都能选取 \(z_1=1\)、全部 \(|z_i|\ge1\)，且连续的 \(n\) 个幂和 \(S_k=\sum_i z_i^k\)（\(k=2,\ldots,n+1\)）均小于 \(C^{-n}\)。
- 状态核对：在线页面在 2026 年仍开放。旧候选正确区分了 \(|z_i|\le1\) 的已知构造与本题，但漏掉了当前页面已记录的 Turán 定量下界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先检验能否令这些幂和精确为零。把相同的 \(z_i\) 合并为不同非零值 \(\lambda_1,\ldots,\lambda_r\)，重数为 \(m_j\)。若 \(S_2,\ldots,S_{r+1}=0\)，则向量 \((m_j\lambda_j^2)_j\) 被 Vandermonde 矩阵 \((\lambda_j^{k})_{0\le k<r}\) 消去。
- 局部结论：Vandermonde 行列式非零，故所有 \(m_j\lambda_j^2=0\)，矛盾；因此窗口中的幂和不可能全部精确为零。；Turán 定理给出 \(\max_{2\le k\le n+1}|S_k|\ge n\bigl(n/(2e(n+1))\bigr)^n\)。；若所求常数存在，则固定的 \(C\ge2e\) 不可能满足要求；因此任何可行常数必须严格小于 \(2e\)。这一下界本身不否定某个较小 \(C>1\)。
- 第一阻塞点：Vandermonde 论证只排除精确零点；当 \(\lambda_i\) 接近或模长很大时，矩阵条件数失控，无法反推出与配置无关的指数下界或构造指数小上界。
- 下一步：固定一个候选结构（例如把 \(z_i\) 设为某个多项式的根），用 Newton 恒等式把 \(S_2,\ldots,S_{n+1}\) 写成系数递推，并检验已知 \(|z_i|\le1\) 极值多项式的倒数根是否能在保持 \(z_1=1\) 时给出上界。
- 来源核对：[Erdős 问题 973 讨论页](https://www.erdosproblems.com/forum/thread/973) 给出了上述 Turán 下界。；[问题 973 历史页](https://www.erdosproblems.com/history/973) 明确区分 \(|z_i|\le1\)、\(\max|z_i|=1\) 与本题 \(|z_i|\ge1\) 三种条件。
- 时间记账：所在批次墙钟时间按题数均摊约 56.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/973)；既有候选答案（按不可信材料审计）

### #975

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f\in \mathbb{Z}[x]$ be an irreducible non-constant polynomial such that $f(n)\geq 1$ for all large $n\in\mathbb{N}$. Does there exist a constant $c=c(f)>0$ such that\[\sum_{n\leq X} \tau(f(n))\sim cX\log X,\]where $\tau$ is the divisor function?
- 题意摘要：对每个固定的不可约非常数多项式 \(f\in\mathbb Z[x]\)，且 \(f(n)\ge1\) 对充分大自然数 \(n\) 成立，问是否存在依赖于 \(f\) 的正常数 \(c(f)\)，使 \(\sum_{n\le X}\tau(f(n))/(X\log X)\to c(f)\)。
- 状态核对：按冻结资料一般次数仍开放；一次与不可约二次已知。\(\asymp_fX\log X\) 只确定数量级，不能推出比值收敛。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：采用除数双曲线法。定义 \(\rho_f(d)=\#\{a\bmod d:f(a)\equiv0\pmod d\}\)，先只数 \(d\le X\) 的小除数：\(T(X)=\sum_{n\le X}\sum_{d\le X,\,d\mid f(n)}1\)。交换求和后逐个同余类计数。
- 局部结论：有 \(T(X)=X\sum_{d\le X}\rho_f(d)/d+O(\sum_{d\le X}\rho_f(d))\)。；利用不可约多项式根密度的标准 Dirichlet 级数结论，\(\sum_{d\le X}\rho_f(d)/d=A_f\log X+O_f(1)\)、\(\sum_{d\le X}\rho_f(d)=O_f(X)\)，其中 \(A_f>0\)；故 \(T(X)=A_fX\log X+O_f(X)\)。；这严格解释了一个正的 \(X\log X\) 主项来源，并给出相应截断和的渐近；二次情形中 \(\sqrt{f(n)}\asymp X\)，截断恰接近双曲线分界。
- 第一阻塞点：若 \(r=\deg f\ge3\)，完整除数配对要求控制 \(X<d\le |f(n)|^{1/2}\asymp X^{r/2}\) 的“中等除数”。逐模数计数的误差总和远大于 \(X\log X\)，而简单除数切换又变成高次数曲线上的整点问题；这是首次无法闭合处。
- 下一步：先对一个具体三次不可约多项式（如 \(x^3+2\)）把中等区间按二进制块分解，证明除去 \(d\) 接近 \(X^{3/2}\) 的末端块后其贡献是否具有稳定常数；这可直接检验障碍集中在哪些尺度。
- 来源核对：冻结题面所列 van der Corput、Erdős、Hooley 结果分别支持一般上下界及二次渐近。；旧候选的局部密度启发式本身不足以处理 \(d>X\) 的中等除数，故未把 Euler 乘积启发式当作证明。
- 时间记账：所在批次墙钟时间按题数均摊约 56.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/975)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/975.lean`；既有候选答案（按不可信材料审计）

### #976

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f\in \mathbb{Z}[x]$ be an irreducible polynomial of degree $d\geq 2$. Let $F_f(n)$ be maximal such that there exists $1\leq m\leq n$ with $f(m)$ is divisible by a prime $\geq F_f(n)$. Equivalently, $F_f(n)$ is the greatest prime divisor of\[\prod_{1\leq m\leq n}f(m).\]Estimate $F_f(n)$. In particular, is it true that $F_f(n)\gg n^{1+c}$ for some constant $c>0$? Or even $\gg n^d$?
- 题意摘要：固定任意不可约多项式 f∈ℤ[x]，deg f=d≥2。对每个 n，F_f(n)=max_{1≤m≤n}P⁺(f(m))；问题要求对所有充分大 n 估计它，并问是否存在依赖于 f 的 c>0 使 F_f(n)≫_f n^{1+c}，乃至 F_f(n)≫_f n^d。不可约性保证 f(m)≠0。
- 状态核对：冻结状态为 open；现有一般结果只保证超线性下界，尚无统一的固定幂增益。先前候选把“下界为 n^{1+o(1)}”误写成等式 F_f(n)=n^{1+o(1)}：这不能由下界及 F_f(n)≪n^d 推出；其精确指数 2−log4 也未由给定官方材料支持，故不采纳。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：反设所有 f(1),…,f(n) 的素因子均≤y，比较 Q_n=∏_{m≤n}|f(m)| 的解析大小与逐素数的 p-adic 估值。对 p∤a_d disc(f)，Hensel 引理给出模 p^a 至多 d 个根，因而 #{m≤n:p^a∣f(m)}≤d(n/p^a+1)。目标是把 log Q_n=∑_{p≤y}v_p(Q_n)log p 的上界压到与 dn log n 矛盾。
- 局部结论：由 f(m)=a_dm^d+O_f(m^{d-1})，严格有 log Q_n=dn log n+O_f(n)。；平凡但最优尺度的上界为 F_f(n)≤max_{m≤n}|f(m)|≪_f n^d。；对所有不除 a_d disc(f) 的素数 p，v_p(Q_n)≤∑_{a≥1}d(n/p^a+1)；其中主项至多 dn/(p−1)，坏素数只有有限多个。
- 第一阻塞点：把各素数的“+1”误差求和时，必须控制 p^a∣f(m) 的稀疏高次幂事件；粗求和的误差足以吞掉目标固定幂增益。Hensel 根数界本身只能启动经典 Chebyshev 型方法，不能闭合 y≥n^{1+c}。
- 下一步：证明或否定一个明确的平均估值引理：对 n<p≤n^{1+c}，估计 ∑_{p}#{m≤n:p∣f(m)}log p，并单独控制 p²∣f(m) 的贡献；先检验该估计是否已经需要超出现有筛法的分布水平。
- 来源核对：[Erdős Problem 976](https://www.erdosproblems.com/976) 当前仍列为 open，并记录 Tenenbaum 仅证明 n exp((log n)^c) 型一般下界。；未采纳讨论区或先前候选中未经原论文核实的更精确指数。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/976)；既有候选答案（按不可信材料审计）

### #978

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f\in \mathbb{Z}[x]$ be an irreducible polynomial of degree $k>2$ (and suppose that $k\neq 2^l$ for any $l\geq 1$). Does the set of integers $n$ for which $f(n)$ is $(k-1)$-power-free have positive density? Are there infinitely many $n$ for which $f(n)$ is $(k-2)$-power-free? In particular, does\[n^4+2\]represent infinitely many squarefree numbers?
- 题意摘要：固定不可约 f∈ℤ[x]，次数 k>2 且 k 不是 2 的幂。第一问：使 f(n) 不被任何 p^{k−1} 整除的正整数 n 是否有正密度。第二问：使 f(n) 不被任何 p^{k−2} 整除的 n 是否无穷多。特例另问 n⁴+2 是否取无穷多个平方自由值。
- 状态核对：第一问已有 Hooley 渐近公式；带必要局部条件的第二问在 k≥9 已知。可是输入中的第二问缺少“无固定 p^{k−2} 因子”条件，按字面其实为假；真正开放的是补上局部条件后的低次数情形，尤其 n⁴+2。先前候选虽提到局部条件，却仍把原句直接概括成开放，遗漏了这一逻辑缺陷。
- 初步判定：`malformed`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先用有限素数筛：令 ρ_f(p^r)=#{a mod p^r:f(a)≡0}。小素数限制产生密度 ∏_{p≤z}(1−ρ_f(p^r)/p^r)，难点是排除 p>z。与此同时直接寻找固定幂因子反例，检验原第二问的量词。
- 局部结论：取 f(x)=x(x−1)(x−2)(x−3)(x−4)+8。五个连续整数之积被 120 整除，故 8∣f(n) 对所有 n 成立；于是没有任何 f(n) 是 3-power-free。其次数 5 不是 2 的幂。；该 f 模 3 化为 x⁵−x⁴−x³+x²−1；它与 x³−x、x⁹−x 的最大公因式均为 1，且整除 x^{3⁵}−x，故模 3 不可约，从而 f 在 ℤ[x] 中不可约。这严格反驳输入第二问的字面版本。；对 g(x)=x⁴+2，p=2 时 p²从不整除 g(n)；对奇素数 p，模 p²至多有4个根。因此局部 Euler 乘积 ∏_p(1−ρ_g(p²)/p²) 收敛到正数，小素数筛确实给出正的候选密度。
- 第一阻塞点：对 n⁴+2，有限素数筛之后仍需证明 #{n≤X:存在 p>z 且 p²∣n⁴+2}=o(X)，并按 X→∞ 后 z→∞ 的顺序一致控制。初等并集界在大素数区间过弱；这正是平方自由四次多项式的开放缺口。
- 下一步：把大平方因子写成 n⁴+2=p²m，分 p≤X^{1−δ} 与 p>X^{1−δ} 两段；前段检验筛余项，后段转化为曲面整数点计数，并明确现有 determinant method 在哪一指数上不足。
- 来源核对：[Erdős Problem 978](https://www.erdosproblems.com/978) 记录第一问由 Hooley 解决、第二问在 k≥9 由 Browning解决，而 n⁴+2 仍开放。；检查了本地形式化文件；其修正版显式加入 ∀p∃n，使 p^{k−2}∤f(n) 的必要局部条件，并将无此条件的版本标为假。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/978)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/978.lean`；既有候选答案（按不可信材料审计）

### #979

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$, and let $f_k(n)$ count the number of solutions to\[n=p_1^k+\cdots+p_k^k,\]where the $p_i$ are prime numbers. Is it true that $\limsup f_k(n)=\infty$?
- 题意摘要：对每个固定 k≥2，f_k(n) 计数由 k 个素数的 k 次幂之和等于 n 的表示；按本地形式化，表示按素数多重集计数，即不区分排列。问题是：对每个 k，是否对任意 R 都存在任意大的 n 使 f_k(n)≥R。
- 状态核对：总问题仍 open；k=2 有 Erdős 的公开证明，官方材料称 k=3 也成立但证明未发表。未发表断言不能当作可重建的已核证明。先前候选关于 k=2 的定量增长率没有在所核材料中得到支持，故只保留无界性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试最直接的平均值/加法能量路线。取所有不超过 X 的素数构成 k 元多重集，每个多重集给出一个不超过 kX^k 的和。若平均表示数趋于无穷即可完成；若不行，则考察等和关系的二阶矩 E=∑_n f_k(n)^2。
- 局部结论：若 L=π(X)，候选多重集数 T=binom(L+k−1,k)∼L^k/k!，而可能的和至多 kX^k 个；故平均值仅为 T/(kX^k)≈1/(k!k(log X)^k)，趋于0，朴素抽屉原理完全无效。；能量恒等式 E=∑_n f_k(n)^2 计数方程 ∑p_i^k=∑q_i^k；并有 max_n f_k(n)≥E/T。；只计入对角解得到 E≥T，因而仅推出 max f_k(n)≥1；要证明无界，必须构造 E/T→∞ 的大量非平凡等和素数解。
- 第一阻塞点：第一处无法闭合的是产生足够多的非对角等幂和关系，同时保证所有变量为素数。一般的 Waring–Goldbach 渐近研究“许多变量”，这里变量数恰等于指数 k，平均密度太低，不能直接提供这种能量增益。
- 下一步：先固定 k=3，计算并分类恒等式 a³+b³+c³=d³+e³+f³ 的参数族；检验是否存在具有三个独立线性素数参数、可由已知素数元组筛法处理的族。若参数维数不足以使 E/T 增长，则该路线可明确淘汰。
- 来源核对：[Erdős Problem 979](https://www.erdosproblems.com/979) 列为 open，并只确认 k=2 的公开结果及 k=3 的未发表声明。；本地 Lean 定义使用 Multiset，确认形式化版本不把同一组素数的排列重复计数。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/979)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/979.lean`；既有候选答案（按不可信材料审计）

### #983

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n\geq 2$ and $\pi(n)<k\leq n$. Let $f(k,n)$ be the smallest integer $r$ such that in any $A\subseteq \{1,\ldots,n\}$ of size $\lvert A\rvert=k$ there exist primes $p_1,\ldots,p_r$ such that at least $r$ many $a\in A$ are only divisible by primes from $\{p_1,\ldots,p_r\}$. Is it true that\[2\pi(n^{1/2})-f(\pi(n)+1,n)\to \infty\]as $n\to \infty$? In general, estimate $f(k,n)$, particularly when $\pi(n)+1<k=o(n)$.
- 题意摘要：按输入原文，f(k,n) 是最小 r，使每个 k 元集合 A⊆[n] 都存在一个含 r 个素数的集合 S，且至少 r 个 a∈A 的全部素因子都在 S 中。问题问输入这个“≥r”版本在 k=π(n)+1 时是否满足 2π(√n)−f→∞，并要求估计 π(n)+1<k=o(n) 的情形。
- 状态核对：输入与当前官方/经典定义存在关键差异：经典版本要求严格多于 r 个元素。官方给出的 2π(√n) 主项属于“>r”版本，不能直接移植。先前候选进一步声称 Pomerance 已证明猜想为假，但当前官方页仍列为 open，所核材料也未支持该断言，故明确拒绝。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把每个 a映到其素因子支持 E_a，形成以不超过 n 的素数为顶点的超图。输入条件是在某个 r 顶点集 S 中至少完整包含 r 条超边；这是寻找最小“边数≥顶点数”的局部子超图。再与经典“边数>顶点数”版本比较。
- 局部结论：函数确实有定义：取 S 为 A 中全部元素所用的素数集合，则 |S|≤π(n)<k=|A|，所以至少 |S| 个元素被 S 支持。；若记 f_≥、f_> 为两个版本，则逐点有 f_≥(k,n)≤f_>(k,n)；并且二者都随 k 增大而不增。；由经典 Erdős–Straus 结果只能推出 f_≥(π(n)+1,n)≤2π(√n)+o_A(√n/(log n)^A)；这是一侧上界，既不推出所问差趋于∞，也不排除它。
- 第一阻塞点：要得到发散差值，必须对每个 A 找到规模比 2π(√n) 少一个发散量的“边数≥顶点数”子超图。Hall 定理直接给出的只是全局亏缺；它不控制最小亏缺证书的大小。经典构造针对严格“>”阈值，也不能提供所需的下界反例。
- 下一步：先在平方自由半素数子类中把问题化成普通图：计算最大 girth/最小含圈子图在顶点数≤π(n)、边数 k 下的极值，并检查乘积约束 pq≤n 如何限制可实现图；这会直接检验“≥r”版本是否比经典主项低一个发散量。
- 来源核对：[Erdős Problem 983](https://www.erdosproblems.com/983) 当前明确使用“>r”，仍列为 open，并记录 Erdős–Straus 主项。；[983 讨论页](https://www.erdosproblems.com/forum/thread/983) 也明确指出严格与非严格版本的差异；未见经审稿确认的 Pomerance 反例。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/983)；既有候选答案（按不可信材料审计）

### #985

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is it true that, for every prime $p$, there is a prime $q<p$ which is a primitive root modulo $p$?
- 题意摘要：字面量词是：对每个素数 p，存在素数 q<p，使 q mod p 的乘法阶恰为 p−1。也就是每个素数模数都在自身以下拥有一个素数原根。
- 状态核对：字面陈述被 p=2 立即反驳，因为不存在素数 q<2；通常研究版本排除 p=2，只问所有奇素数，此版本仍开放。本地形式化也显式加入 p≠2。先前候选在这一点上的校正正确。
- 初步判定：`counterexample`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：对奇素数 p，使用乘法特征标展开原根指示函数，再对 q<p 的素数求和。若主项压过所有非主特征标的素数和，就能证明存在素数原根。
- 局部结论：p=2 给出严格反例，因此输入的全称命题按字面为假。；对 x∈𝔽_p^×，原根指示函数可写为 φ(p−1)/(p−1)·∑_{d∣p−1}μ(d)/φ(d)∑_{ordχ=d}χ(x)。对 q<p 的素数求和后，主项量级约为 φ(p−1)π(p)/(p−1)。；群论本身只给出模 p 有 φ(p−1) 个整数剩余类是原根；它不能保证这些类中有一个代表恰为小于 p 的素数。
- 第一阻塞点：需要对所有 d∣p−1 同时控制 ∑_{q<p,q prime}χ(q)，误差还要小于约 p·φ(p−1)/((p−1)log p)。现有无条件特征和工具在长度恰为 p、且要统一累加许多特征时不足以保证正性；这正是从“整数原根”到“素数原根”的断点。
- 下一步：把上述特征展开完整写成显式误差界，并分别代入 GRH 下的素数特征和估计与无条件 Burgess/Vaughan 型估计，确定后者距离主项还差哪个 p 指数；同时有限检查小奇素数只用于排除边界，不冒充渐近证明。
- 来源核对：[Erdős Problem 985](https://www.erdosproblems.com/985) 的研究意图是奇素数版本，并记录相关 Artin 原根结果，但未给出无条件解答。；本地形式化陈述明确要求 p≠2、q<p 且 orderOf(q)=p−1，验证了 p=2 是被有意排除的退化情形。
- 时间记账：所在批次墙钟时间按题数均摊约 68.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/985)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/985.lean`；既有候选答案（按不可信材料审计）

### #986

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：For any fixed $k\geq 3$,\[R(k,n) \gg \frac{n^{k-1}}{(\log n)^c}\]for some constant $c=c(k)>0$.
- 题意摘要：对每个固定整数 k≥3，存在 c(k)>0、C_k>0、n_0(k)，使所有 n≥n_0(k) 都有 R(K_k,K_n)≥C_k n^{k-1}/(log n)^{c(k)}；等价地，要构造具有约 n^{k-1}/polylog(n) 个顶点、无 K_k 且独立数小于 n 的图。
- 状态核对：输入把状态更新为 proved（2026-06-21），但附带的 official_context 仍只列出 k=3、4，旧候选据此声称 k≥5 开放，显然已经过时。材料没有给出 2026 年一般 k 证明的作者、定理或论文，且外部核验因网络故障失败，故不能把状态标签本身当作已核对证明。
- 初步判定：`blocked`；证明尝试：`failed`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试从随机图/无 K_k 过程重建。令 N≈n^{k-1}/polylog(n)，为压低独立数需取边密度大致 p≳(log n)/n；再控制 K_k。直接 G(N,p) 加逐个删除 K_k 的路线要求 N^k p^{k choose 2}=O(N)，只能支持 N至多约 p^{-k/2}，远达不到 n^{k-1}。无 K_k 过程虽能改进，但材料所列一般结果仍只有 n^{(k+1)/2} 量级。
- 局部结论：Ramsey 下界严格等价于上述 K_k-free、α(G)<n 的图构造问题。；在 p≈(log n)/n 的独立性阈值上，朴素随机图加删点法至多给出 N≈n^{k/2}/polylog(n)，不能证明目标指数 k−1。；k=3、4 可由材料所列 Spencer 与 Mattheus–Verstraete 结果覆盖；旧候选关于 k≥5 仍开放的结论不能沿用。
- 第一阻塞点：第一处无法闭合之处是缺少更新后的一般 k 构造及其关键伪随机/相关性估计；现有输入甚至未给出该证明的引用，无法独立重建或检查其量词是否确实覆盖每个固定 k。
- 下一步：取得 2026-06-21 状态更新对应的论文或官方变更记录，首先核对主定理是否给出对每个固定 k 的 n^{k−1}/polylog(n) 下界，再逐项检查构造规模、K_k-free 性和独立数估计。
- 来源核对：已核对输入内部：current_status 与旧 official_context、旧候选存在时间性冲突。；两次尝试访问官方页面均因网络工具故障失败，因此未独立核实 2026 年证明来源。
- 时间记账：所在批次墙钟时间按题数均摊约 54.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/986)；既有候选答案（按不可信材料审计）

### #987

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $x_1,x_2,\ldots \in (0,1)$ be an infinite sequence and let\[A_k=\limsup_{n\to \infty}\left\lvert \sum_{j\leq n} e(kx_j)\right\rvert,\]where $e(x)=e^{2\pi ix}$. Is it true that\[\limsup_{k\to \infty} A_k=\infty?\]Is it possible for $A_k=o(k)$?
- 题意摘要：给任意无限序列 x_j∈(0,1)，定义 S_n(k)=∑_{j≤n}e(kx_j) 与 A_k=limsup_{n→∞}|S_n(k)|。第一问是是否对每个序列都有 limsup_{k→∞}A_k=∞；第二问是是否存在某个序列满足 A_k/k→0。
- 状态核对：“proved”只能解释为第一问已证；输入背景明确说第二问 A_k=o(k) 仍开放。旧候选的紧致性证明思路基本可修复，但它直接写平均值≤4(C+1)^2 时漏掉了 k<k_0 的有限项。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：反设存在 C、k_0 使 A_k≤C（k≥k_0）。对每个 K，截去足够长的前缀，使尾序列对 k_0≤k≤K 的所有部分和都≤B:=2(C+1)。取 K→∞ 的对角紧致极限 y_j，得到对每个 k≥k_0、n≥1，|∑_{j≤n}e(ky_j)|≤B。固定 n，对 k≤L 的平方模作 Cesàro 平均；有限个 k<k_0 的贡献除以 L 后趋零，其余由 B^2 控制。另一方面展开平方并用字符正交，极限等于 #{(i,j):y_i=y_j}≥n。取 n>B^2 矛盾。
- 局部结论：上述修正后的论证严格推出：不存在最终有界的 A_k，故 limsup_{k→∞}A_k=∞。；极限平均只识别完全相等的 y_i,y_j；至少有 n 个对角项，因此无需假设极限点彼此不同。；Clunie 的 A_k≫√k（无穷多个 k）与 A_k=o(k) 逻辑相容，所以它不解决第二问。
- 第一阻塞点：这条紧致性—正交路线只给无界性，不产生 A_k 与具体 k 的足够定量关系；因而不能判定是否可构造 A_k=o(k) 的序列。
- 下一步：检验能否把对角抽取改成带显式 K、n 关系的有限维估计，并与候选分块构造的上界同时比较；最低目标是明确得到某个可追踪的 A_k 下界而不只是不定量矛盾。
- 来源核对：依据输入所列 Clunie 结果核对：第一问已有更强的无穷多次 √k 下界。；已独立检查并修正旧候选平均平方时遗漏低频项的问题。
- 时间记账：所在批次墙钟时间按题数均摊约 54.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/987)；既有候选答案（按不可信材料审计）

### #990

- 当前状态：`disproved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $f=a_0+\cdots+a_dx^d\in \mathbb{C}[x]$ be a polynomial. Is it true that, if $f$ has roots $z_1,\ldots,z_d$ with corresponding arguments $\theta_1,\ldots,\theta_d\in [0,2\pi]$, then for all intervals $I\subseteq [0,2\pi]$\[\left\lvert (\# \theta_i \in I) - \frac{\lvert I\rvert}{2\pi}d\right\rvert \ll \left(n\log M\right)^{1/2},\]where $n$ is the number of non-zero coefficients of $f$ and\[M=\frac{\lvert a_0\rvert+\cdots +\lvert a_d\rvert}{(\lvert a_0\rvert\lvert a_d\rvert)^{1/2}}.\]
- 题意摘要：对次数 d 的复多项式 f=∑_{j=0}^d a_jx^j，n 为非零系数数目，要求对所有角区间 I 有零点辐角计数偏差 O(√(n log M))，其中 M=(∑|a_j|)/√(|a_0a_d|)。经典定理只保证 O(√(d log M))。该表达式在通常数学意义下还隐含 a_0a_d≠0。
- 状态核对：输入标为 disproved (Lean)，与声称仍开放的旧候选冲突，故旧候选不可采用。但材料没有提供 Lean 定理、反例多项式或其非退化条件，无法核对它是真实数学反例还是形式化边界情形。特别是若未假设 a_0≠0，则 M 在通常实数数学中没有定义，零点 0 也没有辐角。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：先检查自然稀疏候选 f=(x^m−1)^r。它有 n=r+1、M=2^r，某些射线上的角计数偏差可达 O(r)，而 √(n log M)=Θ(r)，故该族只达到常数比例，不能推翻命题。再检查二项式 x^d−1，其辐角均匀，偏差仅 O(1)。这说明不能仅靠高重数或大次数得到反例。
- 局部结论：由三角不等式和 AM–GM，在 a_0a_d≠0 时 M≥2，因此 log M≥log 2，右端为实数且非退化。；族 (x^m−1)^r 的射线重数增长恰被 log M=r log2 补偿，不能作为反例。；若 Lean 反例使用 a_0=0、arg(0) 或除以零的全定义约定，它只暴露原陈述缺失非退化假设，不能直接反驳标准的 Erdős–Turán式命题。
- 第一阻塞点：第一处无法闭合的是缺少实际 Lean witness。没有系数、区间及随参数发散的偏差/√(n log M) 比值，就无法重建“disproved”；也无法排除形式化语义与通常数学语义不一致。
- 下一步：提取 Lean 文件中的最小反例及全部假设，手算 a_0a_d、n、M、零点辐角和偏差；若为退化反例，再给命题补上 a_0a_d≠0、零点非零等条件并重新测试。
- 来源核对：已独立否定两个最直接的稀疏候选族作为反例的可能。；由于网络故障且输入未附 Lean 代码，disproved (Lean) 状态尚未完成语义级核验。
- 时间记账：所在批次墙钟时间按题数均摊约 54.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/990)；既有候选答案（按不可信材料审计）

### #992

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $x_1<x_2<\cdots$ be an infinite sequence of integers. Is it true that, for almost all $\alpha \in [0,1]$, the discrepancy\[D(N)=\max_{I\subseteq [0,1]} \lvert \#\{ n\leq N : \{ \alpha x_n\}\in I\} - \lvert I\rvert N\rvert\]satisfies\[D(N) \ll N^{1/2}(\log N)^{o(1)}?\]Or even\[D(N)\ll N^{1/2}(\log\log N)^{O(1)}?\]
- 题意摘要：量词是：对每个严格递增整数序列 (x_n)，是否对几乎处处 α 存在依赖于 α及该序列的常数，使未归一化区间差异 D(N) 分别满足 √N(log N)^{o(1)} 或 √N(loglog N)^{O(1)} 的最终上界。
- 状态核对：输入状态为 disproved。旧候选给出的 Berkes–Philipp 型路线若引用准确，确实同时否定两个问句；但其“绝对常数 c”并非完成否定所必需，关键是存在一个固定序列，对几乎处处 α 无穷多次达到 √(N log N) 量级。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `medium`
- 尝试路线：采用已知反例定理：构造严格递增整数序列 (x_n)，使对几乎处处 α，归一化 discrepancy D_N^* 无穷多次满足 ND_N^*≥c√(N log N)。按定义 ND_N^*=D(N)，于是直接比较增长因子。
- 局部结论：若 D(N)≥c√(N log N) 无穷多次，则不可能有 D(N)≪√N(log N)^{ε(N)} 且 ε(N)→0，因为其比值至少为 (log N)^{1/2−ε(N)}→∞。；对每个固定 C，(log N)^{1/2}/(loglog N)^C→∞，所以同一反例也排除 √N(loglog N)^{O(1)}。；归一化 discrepancy 与题中未归一化 D(N) 相差恰好因子 N；旧候选在这一换算上是正确的。
- 第一阻塞点：若要求从头重建反例，第一处缺口是证明所构造整数频率块对几乎所有 α 产生近独立的大偏差事件；这需要反例论文中的块构造和度量概率估计，输入未提供。
- 下一步：核对原始反例定理的精确量词，尤其是下界是否对几乎处处 α、是否为无穷多个 N，以及使用的是星差异还是全区间差异；随后逐块复核二阶矩/近独立估计。
- 来源核对：已独立核对从 √(N log N) 下界到两个否定答案的渐近推导。；反例定理本身目前仅由输入候选指向，因网络故障未查到原文定理编号。
- 时间记账：所在批次墙钟时间按题数均摊约 54.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/992)；既有候选答案（按不可信材料审计）

### #995

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_1<n_2<\cdots$ be a lacunary sequence of integers and $f\in L^2([0,1])$. Estimate the growth of, for almost all $\alpha$,\[\sum_{1\leq k\leq N}f(\{ \alpha n_k\}).\]For example, is it true that, for almost all $\alpha$,\[\sum_{1\leq k\leq N}f(\{ \alpha n_k\})=o(N\sqrt{\log\log N})?\]
- 题意摘要：设 (n_k) 为 Hadamard lacunary 整数序列，即存在 q>1 使 n_{k+1}/n_k≥q；对任意 f∈L²([0,1])，研究 S_N(α)=∑_{k≤N}f({αn_k}) 对几乎处处 α 的增长。示例问题问：是否对每一对 ((n_k),f) 都有 S_N=o(N√loglog N) 几乎处处。
- 状态核对：仍为开放。旧候选误写了“f∈L^{[0,1]}”，但其主要状态判断合理。题面不要求 f 零均值；这不构成问题，因为均值项 N∫f=o(N√loglog N)。official_context 中重复的双重求和显然是排版错误，应按单和理解。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先中心化 f=μ+g。尝试仅用 L²估计：因 α↦{n_kα} 保测度，Minkowski 给出 ||∑_{k≤N}g(n_kα)||₂≤N||g||₂。Chebyshev 在阈值 N√loglog N 处只给异常集测度 O(1/loglog N)，沿 N=2^r 仍不可求和，因此 Borel–Cantelli不能推出目标。稀疏性若要改进此估计，必须控制 Fourier 频率碰撞 mn_k=m'n_l；一般 L²函数含任意高频，碰撞不能直接忽略。
- 局部结论：中心化严格化简为 S_N=Nμ+T_N，且固定 μ 满足 Nμ=o(N√loglog N)。；若 f∈L∞，则 |S_N|≤N||f||∞，所以目标对所有 α 都成立；困难仅来自无界 L²尾部。；Erdős 的反例下界为 N(loglog N)^{1/2−ε} 以下的尺度，不能否定 N(loglog N)^{1/2} 的小 o 结论；旧候选在此逻辑关系上应保留这种区分。
- 第一阻塞点：第一处无法闭合的是把粗糙的 N²级二阶矩降到足以使异常概率可求和的尺度。仅凭 lacunarity，L²函数的高频 Fourier 支撑会造成跨 k 的精确频率碰撞，标准正交性并不自动适用。
- 下一步：固定一个截断参数 H，令 g=P_H+r_H，其中 P_H 是 Fourier 截断；先精确计数 h n_k=h'n_l（|h|,|h'|≤H）的解以取得 P_H 的二阶矩，再选择 H=H(N)，检验 L²尾项 r_H 是否能通过最大不等式而非 Minkowski 控制。
- 来源核对：已核对中心化、L∞特例及 Erdős 下界与目标尺度之间的逻辑关系。；未把旧候选所称的正则函数 LIL 当作一般 L²结论；该路线需要额外正则性。
- 时间记账：所在批次墙钟时间按题数均摊约 54.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/995)；既有候选答案（按不可信材料审计）

### #996

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $n_1<n_2<\cdots$ be a lacunary sequence of integers, and let $f\in L^2([0,1])$. Let $f_n$ be the $n$th partial sum of the Fourier series of $f(x)$. Is there an absolute constant $C>0$ such that, if\[\| f-f_n\|_2 \ll \frac{1}{(\log\log\log n)^{C}}\]then\[\lim_{N\to\infty}\frac{1}{N}\sum_{k\leq N}f(\{\alpha n_k\})=\int_0^1 f(x)\mathrm{d}x\]for almost every $\alpha$?
- 题意摘要：命题量词是：是否存在绝对常数 C>0，使得对每个整数 Hadamard–lacunary 序列 n_1<n_2<…（通常指 n_{k+1}/n_k≥q>1）及每个 f∈L²([0,1])，若 Fourier 截断误差满足 ‖f-f_n‖₂≪(log log log n)^{-C}，则对几乎处处 α，有 N^{-1}∑_{k≤N}f({αn_k})→∫f。隐含常数通常可依赖 f 和序列，但 C 不可依赖它们。
- 状态核对：按冻结状态仍为开放题。旧候选关于已知 log-log 结果的概述与官方背景相符，但没有提供证明进展；其“存在任意 L^p 反例”等额外断言未由输入文献支持，故不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先对三角多项式严格证明结论，再尝试用 Fourier 尾部逼近。若 P(x)=∑_{|h|≤M}c_he(hx)，对每个 h≠0，X_k(α)=e(hn_kα)在 L²(α) 中正交，故 E|N^{-1}∑_{k≤N}X_k|²=1/N。取 N=j² 后由 Chebyshev–Borel–Cantelli 得子序列几乎处处收敛；P 有界，平方之间的差为 O(1/j)，于是全序列收敛。随后写 f=P_M+r_M，试图控制 N^{-1}∑r_M(n_kα)。
- 局部结论：对任意严格递增整数序列，而不只 lacunary 序列，任意三角多项式 P 都满足 N^{-1}∑_{k≤N}P({αn_k})→∫P，几乎处处 α。；每个映射 α↦{n_kα}保持 Lebesgue 测度，故 ‖r_M(n_k·)‖₂=‖r_M‖₂。；仅用三角不等式只能得到 ‖N^{-1}∑r_M(n_k·)‖₂≤‖r_M‖₂；这没有随 N 衰减，不能完成极限交换。
- 第一阻塞点：第一处无法闭合的是尾项的几乎处处最大估计：需要一个对 lacunary dilates 的定量不等式，把 sup_N 的坏集概率与 Fourier 尾误差联系起来，并且其损失必须弱到可由 triple-log 衰减求和。现有朴素 L² 估计完全看不到该速率。
- 下一步：为 dyadic 指标块 2^j<N≤2^{j+1} 明确计算尾项的二阶矩，按共振方程 hn_k=h'n_l 分类；检验能否证明一个带至多 (log j)^A 损失的块最大不等式，并判断给定 triple-log 尾界能否选取截断 M_j 使坏集概率可求和。
- 来源核对：官方背景中的 KSZ、Erdős、Matsuyama 阈值已作为已知边界使用。；本地 996.lean 不忠实于原题：fourierPartial 的求和项误用 fourierCoeff f k 而非 fourierCoeff f i；假设也写成部分和范数而非 ‖f-f_k‖₂，不能视为原题形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 62.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/996)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/996.lean`；既有候选答案（按不可信材料审计）

### #997

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Call $x_1,x_2,\ldots \in (0,1)$ well-distributed if, for every $\epsilon>0$, if $k$ is sufficiently large then, for all $n>0$ and intervals $I\subseteq [0,1]$,\[\lvert \# \{ n<m\leq n+k : x_m\in I\} - \lvert I\rvert k\rvert < \epsilon k.\]Is it true that, for every $\alpha$, the sequence $\{ \alpha p_n\}$ is not well-distributed, if $p_n$ is the sequence of primes?
- 题意摘要：对每个实数 α，令 p_n 为第 n 个素数，问序列 x_n={αp_n} 是否必定不满足如下统一滑窗性质：对每个 ε>0，存在 K，使所有 k≥K、所有起点 n 及所有区间 I⊆[0,1] 都有 |#{n<m≤n+k:x_m∈I}-|I|k|<εk。
- 状态核对：冻结状态“proved (Lean)”应接受。旧候选称全称命题仍开放，已被 2026 年 APSSV26 定理 4.1 推翻；CLLW24 确实只证明了存在一个坏的无理 α。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建 APSSV26 路线。对有理 α=a/q，除有限多个例外素数外，{αp_n}落在有限集合中，取避开它的小区间即否定良分布。对无理 α，使用 Dirichlet 有理逼近，并调用 Banks–Freiberg–Turnage-Butterbaugh 关于连续素数簇的推论：可找到任意长的一段连续素数，使相应的 {αp} 全部落入一个统一的窄区间。若该区间宽度为 δ<1，取稍大的 I，则某个任意长滑窗中命中比例为 1，而期望比例仅 |I|；固定 ε<(1-|I|)/2 即与良分布矛盾。
- 局部结论：有理 α 的情形是初等的，并且涵盖 α∈ℤ。；只要对任意 K 能找到 K 个连续素数，其 α-倍的分数部分落在某个长度 δ<1 的区间，就足以否定良分布；不需要分析所有区间。；APSSV26 的素数簇输入与 Dirichlet 逼近恰好产生上述任意长坏滑窗，因此得到“对每个实数 α”。
- 第一阻塞点：重建证明时第一个非初等步骤是 APSSV26 定理 4.2，即由 Maynard–Tao/Banks–Freiberg–Turnage-Butterbaugh 推出的连续素数簇结论；它不能由初等 Dirichlet 逼近独立推出。不过这是已发表证明明确引用的定理输入，不是未闭合猜测。
- 下一步：若需完全审计，逐项核对 APSSV26 定理 4.2 的参数依赖，并在 Lean 证明中确认所取区间端点、窗口索引和 ε 与论文一致。
- 来源核对：APSSV26, Theorem 4.1–4.2：https://arxiv.org/html/2603.29961；CLLW24, Theorem 1.1：https://arxiv.org/abs/2406.19491；本地 997.lean 的命题确为 ∀α, ¬IsWellDistributed；但仓库正文仍以 sorry 占位，真正形式证明由文件中的外部 Lean 链接承载。
- 时间记账：所在批次墙钟时间按题数均摊约 62.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/997)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/997.lean`；既有候选答案（按不可信材料审计）

### #1002

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any $0<\alpha<1$, let\[f(\alpha,n)=\frac{1}{\log n}\sum_{1\leq k\leq n}(\tfrac{1}{2}-\{ \alpha k\}).\]Does $f(\alpha,n)$ have an asymptotic distribution function? In other words, is there a non-decreasing function $g$ such that $g(-\infty)=0$, $g(\infty)=1$, and\[\lim_{n\to \infty}\lvert \{ \alpha\in (0,1): f(\alpha,n)\leq c\}\rvert=g(c)?\]
- 题意摘要：令 α 按 (0,1) 上 Lebesgue 测度随机，F_n(α)=(log n)^{-1}∑_{k=1}^n(1/2-{kα})。问题要求存在单调 g，端点极限为 0、1，并且对每个实数 c 都有 μ{α:F_n(α)≤c}→g(c)。这比通常只要求在 g 的连续点收敛略强。β=0 是固定起点。
- 状态核对：按冻结状态开放。Kesten 的结果随机化了 (α,β)，不能通过令 β=0 得到本题；旧候选给出的具体尺度常数未在官方背景中出现，本次不采用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试从精确对称性和紧性入手。对除有限个有理点外的 α，有 {k(1-α)}=1-{kα}，从而 F_n(1-α)=-F_n(α)。此外每个 α↦{kα}均匀分布，所以 ∫F_n(α)dα=0。接着计划用连分数/Ostrowski 展开，把锯齿函数的 Birkhoff 和分解为收敛分母块，再证明 F_n 的分布族紧。
- 局部结论：每个 n>1 的推前分布关于 0 对称；由于 F_n 在有限个分割区间上具有非零斜率，单点原像为零测集，故其分布无原子，并有 G_n(c)=1-G_n(-c)。；∫_0^1F_n(α)dα=0。；若存在逐点分布极限 g，则必满足 g(c)=1-g(-c)，特别是 g(0)=1/2。
- 第一阻塞点：第一处无法闭合的是紧性：均值为零和对称性都不能排除质量逃向 ±∞。需要证明例如 sup_n μ(|F_n|>A)→0，或一个统一的 E|∑_{k≤n}(1/2-{kα})|≪log n 型估计。Kesten 对 β 平均后的 Cauchy 定律只控制 β-平均，不能给出固定切片 β=0 的这种界。
- 下一步：用 Ostrowski 展开对一个完整收敛分母块应用 Denjoy–Koksma，再对 α 的连分数数字分层；具体检验能否证明 μ(|S_n(α)|>A log n)≤C/A，且常数与 n 无关。该尾界一旦成立即可先得到子序列弱极限，再研究唯一性。
- 来源核对：官方背景仅确认 Kesten 对随机 (α,β) 的 Cauchy 型极限。；本地 1002.lean 基本忠实地表达了固定 β=0 及对所有 c 收敛的命题。
- 时间记账：所在批次墙钟时间按题数均摊约 62.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1002)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1002.lean`；既有候选答案（按不可信材料审计）

### #1003

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many solutions to $\phi(n)=\phi(n+1)$, where $\phi$ is the Euler totient function?
- 题意摘要：问集合 {n∈ℕ:φ(n)=φ(n+1)} 是否无限；不是只问是否存在一个解。若 ℕ 包含 1，则 n=1 也是解。
- 状态核对：按冻结状态仍开放。旧候选正确地区分了“已找到许多解”和“证明无限多”，但计算数量及后续改进不参与本次证明判断。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试先排除容易产生无限族的素数情形，再寻求固定因子参数化。若 n=p 为奇素数，则 φ(n)=p-1；而 n+1 为偶数。对 p>3，有 φ(p+1)≤(p+1)/2<p-1，所以只有 p=3 可行。若 n+1=q为奇素数，则 n为偶数且 φ(n)≤n/2<q-1，故不可能。随后尝试令 n=ap、n+1=bq，其中 a,b固定而 p,q为素数，把等式化为线性素数条件。
- 局部结论：除 n=3 外，解的 n 不可能是素数。；对任何解，n+1 不可能是奇素数；因此所有 n>3 的解中 n 与 n+1 都是合数。；在 n=ap、n+1=bq 且 p∤a、q∤b 的模型中，条件精确化为 φ(a)(p-1)=φ(b)(q-1) 与 ap+1=bq，两条线性关系。
- 第一阻塞点：消去 p、q 后，要使固定 a,b 产生无穷多个候选，线性系数必须满足很强的兼容关系；最直接的系数匹配退化为要求相邻 a,b 具有相同的 φ(m)/m 型数据，没有得到非平凡基族。即使找到兼容参数，仍需同时证明两条线性式无穷多次取素数，这通常达到未解决的素数元组难度。
- 下一步：系统枚举小 a,b，求解上述两条线性关系并筛出确实形成一参数整数族者；对每个族计算局部同余障碍。若无无障碍族，则可明确否定这条固定因子参数化路线；若有，则把结论准确表述为某个 Dickson/Schinzel 型条件命题。
- 来源核对：官方 EPS87 上界只说明解集非常稀疏，不能推出有限。；Ford 的结果解决某些偶移位 k，但其论文明确把 k=1 的无穷性保留为未决：https://www.ford126.web.illinois.edu/wwwpapers/phink.pdf；本地 1003.lean 忠实表达 Set.Infinite {n | φ n = φ(n+1)}。
- 时间记账：所在批次墙钟时间按题数均摊约 62.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1003)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1003.lean`；既有候选答案（按不可信材料审计）

### #1004

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $c>0$. If $x$ is sufficiently large then does there exist $n\leq x$ such that the values of $\phi(n+k)$ are all distinct for $1\leq k\leq (\log x)^c$, where $\phi$ is the Euler totient function?
- 题意摘要：量词为：对每个固定 c>0，是否存在 x₀(c)，使每个实数/整数 x≥x₀ 都能找到 n≤x，使 φ(n+1),…,φ(n+K) 两两不同，其中 K=⌊(log x)^c⌋。题目没有要求 n+K≤x。
- 状态核对：按冻结状态开放。旧候选声称无条件证明所有 c<2，但其关键的统一结构项估计及 c(k)≪k^{-1+o(1)} 没有给出可核对的一手依据；不能据此宣布这一范围已解决。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：采用碰撞计数和并合界。令 P_k(X)=#{m≤X:φ(m)=φ(m+k)}。长度 L 的起点 n 若为坏点，则存在 1≤i<j≤L；置 k=j-i、m=n+i。每个固定的 (m,k) 最多对应 L-k 个起点，故坏起点数 B(x,L)≤∑_{k=1}^{L-1}(L-k)P_k(x+L)。因此若能证明右端小于 x（更稳健地为 o(x)），便存在所需好起点。
- 局部结论：上述并合界是确定性的，不依赖 φ 的统计假设。；足够条件是 ∑_{k<L}(L-k)P_k(x+L)=o(x)。；若可统一证明 P_k(x)≪x/[k(log x)^2]·(log x)^{o(1)}，则右端 ≪xLlog L/(log x)^2·(log x)^{o(1)}，形式上确可覆盖每个固定 c<2；但该前提正是必须核验的核心，而非已在本题输入中给出的事实。
- 第一阻塞点：第一处无法严格闭合的是对所有 k≤(log x)^c 的 P_k(x) 给出足够强且统一的上界，尤其是可能来自参数化/结构化解的部分。EPS87 在官方背景中给出的只是最长无重复段的反向上界，不能直接代入上述并合界；旧候选也没有证明其结构项具有所声称的 1/k 衰减。
- 下一步：直接查验 Pollack–Pomerance–Treviño 原定理中 P_0(x;k) 的定义、奇偶限制、k 的一致范围及乘法因子 c(k)；随后计算 ∑_{k≤L}(L-k)c(k)，而不是逐项粗略替换为 1/k。这个求和量是否为 O(Llog L·(log L)^{o(1)}) 将决定 c<2 路线能否成立。
- 来源核对：官方 1004 背景只给 EPS87 对已有无重复段长度的上界，未给旧候选使用的 P_k 估计。；本地 1004.lean 忠实表达 ∀c>0、最终对每个 x 存在 n≤x；同时确认没有 n+K≤x 的附加条件。；旧候选的“c<2 已证”在完成结构项原文核验前按未证主张处理。
- 时间记账：所在批次墙钟时间按题数均摊约 62.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1004)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1004.lean`；既有候选答案（按不可信材料审计）

### #1005

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $\frac{a_1}{b_1},\frac{a_2}{b_2},\ldots$ be the Farey fractions of order $n\geq 4$. Let $f(n)$ be the largest integer such that if $1\leq k<l\leq k+f(n)$ then $\frac{a_k}{b_k}$ and $\frac{a_l}{b_l}$ are similarly ordered - in other words,\[(a_k-a_l)(b_k-b_l)\geq 0.\]Estimate $f(n)$ - in particular, is there a constant $c>0$ such that $f(n)=(c+o(1))n$ for all large $n$?
- 题意摘要：固定 n≥4，将所有既约 Farey 分数 0≤a/b≤1、b≤n 按数值严格递增列为 a_i/b_i。f(n) 是使得对所有索引 k<l 且 l-k≤f(n)，都有 (a_k-a_l)(b_k-b_l)≥0 的最大整数；问题要求估计 f(n)，并问 f(n)/n 是否收敛到正常数。
- 状态核对：截至所给日期仍开放。已知 (1/12-o(1))n≤f(n)≤n/4+O(1)，故只能断言 f(n)=Θ(n)，不能断言极限存在或常数为 1/4。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把第一次“逆序”化为短 Farey 区间中的点数问题。若 a/b<c/d 却不相似，则必有 a<c、b>d。令 x=c-a≥1、y=b-d≥1，则 cb-ad=xb+ay≥b，因此 c/d-a/b=(cb-ad)/(bd)≥1/d≥1/n。若能证明每个由这种逆序端点产生的区间都含有至少 (1/12-o(1))n 个 Farey 间隔，即得下界。
- 局部结论：数值次序排除了 a>c、b<d，故不相似恰等价于分子严格上升而分母严格下降。；若 D(n)=min{l-k:(a_k-a_l)(b_k-b_l)<0}，则严格地有 f(n)=D(n)-1。；任一坏对端点之间的数值距离至少 1/n；这把问题归约为长度约 1/n 的特殊区间内 Farey 点的统一下界。
- 第一阻塞点：第一处缺口是：区间长度≥1/n 本身不足以直接给出所需的统一 Farey 点数下界，尤其端点位置和互素条件会造成显著非均匀性。必须利用端点同时满足 b>d、a<c 的额外算术结构；简单套用全局 Farey 密度不严格。
- 下一步：证明或计算检验如下局部命题：对所有坏对 a/b<c/d，区间 (a/b,c/d) 内阶 n Farey 分数数目是否至少 n/12-O(n^{2/3})；若失败，记录使计数最小的端点参数 (a,b,c,d)，以识别 1/4 上界构造的结构。
- 来源核对：官方状态及界已由 [Erdős Problems #1005](https://www.erdosproblems.com/1005) 核对。；van Doorn 预印本摘要明确给出 (1/12-o(1))n 的下界及小于 n/4+5 的坏对构造：[arXiv:2509.00121](https://arxiv.org/abs/2509.00121)。；先前候选关于更精细的分模公式未在本次筛查中重建，故不采纳为已核对结论。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1005)；既有候选答案（按不可信材料审计）

### #1011

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f_r(n)$ be minimal such that every graph on $n$ vertices with $\geq f_r(n)$ edges and chromatic number $\geq r$ contains a triangle. Determine $f_r(n)$.
- 题意摘要：对固定整数 r，f_r(n) 是最小边数阈值：每个恰有 n 个顶点、边数至少 f_r(n)、且 χ(G)≥r 的图都含三角形。等价地，若 M_r(n) 是满足 |V|=n、K_3-free、χ≥r 的图的最大边数，则 f_r(n)=M_r(n)+1。
- 状态核对：一般 r 仍开放。已知 r=2,3 的精确式；当前官方资料给出 r=4 的公式仅保证 n≥150。先前候选写成 n≥90，与当前官方记录冲突，不能沿用。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：沿 Simonovits 的“距二部图的顶点删除数”归约。定义 τ_2(G)=min{|S|:G-S 为二部图}，以及 g(r)=min{τ_2(G):G 无三角形且 χ(G)≥r}。尝试先控制 g(r)，再代入 Simonovits 稳定性公式 f_r(n)=n²/4-g(r)n/2+O_r(1)。
- 局部结论：阈值定义严格给出 f_r(n)=M_r(n)+1；这也解释所有精确公式末尾的 +1。；若 τ_2(G)=t，则 χ(G)≤t+2；因此 χ(G)≥r 蕴含 τ_2(G)≥r-2，从而 g(r)≥r-2。；若 H 是达到 h_3(r) 的三角形自由 r-色图，则删去至多 |V(H)|-2 个顶点即可留下二部图，故 g(r)≤h_3(r)-2。
- 第一阻塞点：第一处无法自行闭合的是 Simonovits 稳定性步骤：仅由 τ_2(G)≥g(r) 不能直接推出极值边数的精确线性修正 −g(r)n/2；需要分类近 Mantel 极值图并证明所有异常核心只贡献 O_r(1)。
- 下一步：对 r=5 做有限核心筛查：枚举或利用已知 5-临界三角形自由图，计算其 τ_2，寻找达到 g(5) 的最小核心；随后检验相应 Simonovits 扩张是否产生 n²/4-g(5)n/2+O(1) 条边。
- 来源核对：[Erdős Problems #1011](https://www.erdosproblems.com/1011) 核实了一般状态、Simonovits 公式、g(r)=Θ(r²log r) 的当前界及 n≥150 的 r=4 结论。；先前候选的 n≥90 门槛未通过当前官方记录核对，已明确剔除。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1011)；既有候选答案（按不可信材料审计）

### #1013

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h_3(k)$ be the minimal $n$ such that there exists a triangle-free graph on $n$ vertices with chromatic number $k$. Find an asymptotic for $h_3(k)$, and also prove\[\lim_{k\to \infty}\frac{h_3(k+1)}{h_3(k)}=1.\]
- 题意摘要：h_3(k) 是存在一个恰有 n 个顶点、无三角形且色数恰等于 k 的图时，最小的这种 n。要求求其渐近式，并无条件证明 h_3(k+1)/h_3(k)→1。
- 状态核对：仍开放，但输入中的背景已过时：当前资料给出 (1/2-o(1))k²log k≤h_3(k)≤(1+o(1))k²log k。先前候选声称常数 1/4 与 4，现已不是最佳界；其“删最大颜色类”论证也不能保证剩余色数恰为 k。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试用临界子图与 Mycielski 构造控制相邻项。取 h_3(k+1) 阶的最小图，它必为顶点临界；反向则从达到 h_3(k) 的图应用 Mycielski 构造。再检查现有两侧渐近界能否把因子 2 压到 1。
- 局部结论：最小阶 (k+1)-色图是顶点临界的；删任一顶点后色数至多 k，而加回一个顶点至多增加一种颜色，故剩余色数恰为 k。因此 h_3(k)≤h_3(k+1)-1。；Mycielski 构造保持无三角形并把色数从 k 提到 k+1，顶点数从 n 变为 2n+1，故 h_3(k+1)≤2h_3(k)+1。；结合当前上下界只能得到相邻比值最终夹在 1 与约 2 之间；全局 Θ(k²log k) 本身不能排除稀疏的大跳跃。
- 第一阻塞点：第一处缺口是缺少“近乎不增加一倍顶点”的升色构造，或等价的局部平滑性定理。已有常数相差 2 的全局界无法控制单步振荡，因此不能推出所求极限。
- 下一步：检验强化的局部构造命题：给定最小 k-临界三角形自由图 G，是否能通过加入 o(|V(G)|) 个顶点和适当边得到三角形自由 (k+1)-色图；先对已知小型临界图计算最少扩张量，寻找结构性障碍。
- 来源核对：[Erdős Problems #1013](https://www.erdosproblems.com/1013) 核实开放状态及更新后的 (1/2-o(1)) 与 (1+o(1)) 常数。；同页讨论明确指出 h_3 与最大三角形自由色数函数互为离散逆函数，也指出先前 Ramsey 推导方向曾被写反。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1013)；既有候选答案（按不可信材料审计）

### #1014

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $R(k,l)$ be the Ramsey number, so the minimal $n$ such that every graph on at least $n$ vertices contains either a $K_k$ or an independent set on $l$ vertices. Prove, for fixed $k\geq 3$, that\[\lim_{l\to \infty}\frac{R(k,l+1)}{R(k,l)}=1.\]
- 题意摘要：固定整数 k≥3。R(k,l) 是使每个至少有该数量顶点的图都含 K_k 或 l 点独立集的最小整数。证明当 l→∞ 时，R(k,l+1)/R(k,l)→1；k 固定而 l 变化。
- 状态核对：状态已更新为 proved (Lean)。应重建新证明，而不是重复旧背景中的“开放”。人工评审指出先前候选假设了 k≥4 时未知的下界 R(k,l)≫l^{k-1}/(log l)^{k-2}；该错误已吸收，以下改用实际证明所需的弱得多的概率下界。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：重建依赖随机选择（DRC）证明。令 N=R(k,l+1)-1，并取无 K_k、独立数≤l 的临界图 G。先由任一顶点的非邻域推出 δ(G)≥R(k,l+1)-R(k,l)-1。设 s=⌈k/2⌉、t=⌊k/2⌋，对 G 用 DRC；若相对跳跃不小，就得到大集合 U，使每个 s-子集有至少 R(t,l+1) 个公共邻点。
- 局部结论：临界图的最小度界是严格的：G-N[v] 既无 K_k，也不能有 l 点独立集，否则连同 v 得到 l+1 点独立集。；DRC 所得 U 不能含 K_s：否则其公共邻域中由 R(t,l+1) 的定义得到 K_t 或 (l+1)-独立集；后者被 G 排除，前者与 K_s 合成 K_k。因此 |U|<R(s,l+1)。；取 DRC 参数 q=k²，配合 Erdős–Szekeres 上界 R(s,l+1)=O_k(l^{s-1})、R(t,l+1)=O_k(l^{t-1})，以及有效的概率下界 R(k,l)≫_k(l/log l)^{k/2}，DRC 误差两项均为 o(1)，从而 (R(k,l+1)-R(k,l)-1)/(R(k,l+1)-1)→0，等价于目标比值趋于 1。
- 第一阻塞点：在重建层面，唯一非初等输入是标准 DRC 引理及概率下界 R(k,l)≫_k(l/log l)^{k/2}；二者均在正式证明中明确陈述。不存在先前候选所需的、对 k≥4 未知的“近最优”下界。
- 下一步：逐项形式核对 DRC 不等式中 q=k² 时的指数：验证 l^{q(t-1)}/N^{q-s+1}=o(1)，并将这一步与 Lean 文件中的自然数取整及小参数 k=3 边界对应起来。
- 来源核对：官方页面已标记 [Erdős Problems #1014](https://www.erdosproblems.com/1014) 为 PROVED (LEAN)，并给出更强的幂次误差。；三页正式证明 [On the Ratio of R(k,l) and R(k,l+1)](https://cdn.openai.com/pdf/6dc7175d-d9e7-4b8d-96b8-48fe5798cd5b/Ramsey.pdf) 明确采用临界图、DRC 与 R(k,l)≫_k(l/log l)^{k/2}。；官方讨论页链接了 Lean 形式化；但页面数据库字段仍显示“Formalised statement? No”，应视为元数据尚未同步，而非推翻已链接的形式化记录。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1014)；既有候选答案（按不可信材料审计）

### #1016

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be minimal such that there is a graph on $n$ vertices with $n+h(n)$ edges which contains a cycle on $k$ vertices, for all $3\leq k\leq n$. Estimate $h(n)$. In particular, is it true that\[h(n) \geq \log_2n+\log_*n-O(1),\]where $\log_*n$ is the iterated logarithmic function?
- 题意摘要：h(n) 是最小非负整数，使得存在一个恰有 n 个顶点和 n+h(n) 条边的简单图，并且对每个整数 3≤k≤n 都至少含一个 k-圈。问题要求估计 h(n)，特别问是否有 h(n)≥log_2 n+log_*n-O(1)。
- 状态核对：仍开放。已知 log_2(n-1)-1≤h(n)≤log_2 n+log_*n+O(1)，甚至 h(n)-log_2 n→∞ 尚未证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：从任一极小边数的泛圈图选择一个 Hamilton 圈 C。其余 h 条边全是 C 的弦。沿 Griffin/Bondy 的弦子集计数路线：按一个圈使用的弦集合编码所有圈，使用标准引理把总圈数控制在 2^{h+1}-1，再与泛圈性要求的至少 n-2 个不同长度比较。
- 局部结论：Hamilton 圈已经占 n 条边，所以图恰可写为一个固定 n-圈加 h 条弦。；弦计数引理给出总圈数至多 2^{h+1}-1；泛圈性至少要求 n-2 个圈，故 2^{h+1}-1≥n-2。；因此严格得到 h(n)≥log_2(n-1)-1，并与已知上界合并得 h(n)=(1+o(1))log_2 n。
- 第一阻塞点：第一处无法加强之处是计数只利用“至少 n-2 个圈”，完全忽略这些圈的长度必须逐一覆盖。要多得到 log_*n，必须证明接近饱和 2^{h+1} 的弦集合编码不可能同时产生连续的全部圈长；现有粗计数看不见这种加法结构。
- 下一步：研究近等号情形：对固定 Hamilton 圈上的 h 条弦，计算每个弦子集可产生的圈长集合，验证若覆盖长度区间 [3,n]，是否必有至少 log_*n-O(1) 个弦子集发生编码碰撞或产生重复长度；这正可把粗计数提升所需的迭代对数项。
- 来源核对：[Erdős Problems #1016](https://www.erdosproblems.com/1016) 核实开放状态、上下界及“差值趋于无穷仍未知”。；Griffin 的 [Minimal Pancyclicity](https://arxiv.org/abs/1312.0274) 是官方所引下界证明来源；本筛查仅使用其弦计数引理，不把候选答案中的高层二进制构造描述当作完整上界证明。
- 时间记账：所在批次墙钟时间按题数均摊约 55.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1016)；既有候选答案（按不可信材料审计）

### #1017

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n,k)$ be such that every graph on $n$ vertices and $k$ edges can be partitioned into at most $f(n,k)$ edge-disjoint complete graphs. Estimate $f(n,k)$ for $k>n^2/4$.
- 题意摘要：令 \(\operatorname{cp}(G)\) 为把 \(E(G)\) 分割成边互不相交的完全子图所需的最少块数；自然的精确定义是 \(f(n,k)=\max\{\operatorname{cp}(G):|V(G)|=n,|E(G)|=k\}\)。问题要求估计所有 \(k>n^2/4\) 时的最坏值。
- 状态核对：截至官方页最近更新仍为开放问题。旧候选关于一般图的 \(-m/3+o(n^2)\) 改进未获所给官方材料支持，本次不采纳；其声称整个 \(K_4\)-free 范围均为精确等式，也缺少全范围下界。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：取 \(q=\lfloor n^2/4\rfloor\)、\(k=q+m\)。先严格处理 \(K_4\)-free 子类：此时分割块只能是边或三角形，把问题归约为最大边不交三角形数 \(\nu_\triangle(G)\)。再尝试将该归约推广到含 \(K_4\) 的一般图。
- 局部结论：若 \(G\) 无 \(K_4\)，则 \(\operatorname{cp}(G)=k-2\nu_\triangle(G)\)：任取 \(t\) 个边不交三角形可得到 \(k-2t\) 块；反之任何分割中的三角形都形成这种打包。；Győri–Keszegh 的定理给出 \(\nu_\triangle(G)\ge m\)，故 \(\operatorname{cp}(G)\le q-m\)。；在 \(m\le\lfloor\lceil n/2\rceil/2\rfloor\) 时，从平衡完全二部图出发，在一侧加入大小 \(m\) 的匹配；所得图无 \(K_4\)，每个三角形恰含一条匹配边，故 \(\nu_\triangle=m\)，从而该范围确有 \(\operatorname{cp}=q-m\)。
- 第一阻塞点：第一处断裂发生在推广到一般图：一旦出现 \(K_4\) 或更大团，\(\operatorname{cp}(G)\) 不再由三角形打包数表达；一个 \(K_r\) 块一次覆盖 \(\binom r2\) 条边，现有 \(K_4\)-free 定理不能控制这些块与剩余图之间的联合最优化。
- 下一步：检验如下稳定性子任务：固定小常数 \(m\)，证明或反驳每个满足 \(e(G)=q+m\) 且 \(\operatorname{cp}(G)\) 接近 \(q\) 的图，都可通过不增加 \(\operatorname{cp}\) 的局部变换化为 \(K_4\)-free 图；先对 \(m=1,2\) 穷举局部构型。
- 来源核对：[官方条目：仍为 open，并记载 EGP 及 Győri–Keszegh 定理](https://www.erdosproblems.com/1017)
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1017)；既有候选答案（按不可信材料审计）

### #1021

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Is it true that, for every $k\geq 3$, there is a constant $c_k>0$ such that\[\mathrm{ex}(n,G_k) \ll n^{3/2-c_k},\]where $G_k$ is the bipartite graph between $\{y_1,\ldots,y_k\}$ and $\{z_1,\ldots,z_{\binom{k}{2}}\}$, with each $z_j$ joined to a unique pair of $y_i$?
- 题意摘要：对每个固定整数 \(k\ge3\)，\(G_k\) 是把 \(K_k\) 每条边各细分一次所得的二部图。需证明存在依赖于 \(k\) 的 \(C_k<\infty,c_k>0\)，使所有 \(n\) 都有 \(\mathrm{ex}(n,G_k)\le C_kn^{3/2-c_k}\)。
- 状态核对：已解决。官方页确认 Conlon–Lee 可取 \(c_k=6^{-k}\)，Janzer 改进为 \(c_k=1/(4k-6)\)。旧候选的核心结论正确。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建 Janzer 定理的直接应用：先识别 \(G_k\) 为 \(K_k\) 的 1-细分，再将 Janzer 对该图族的极值上界代入。
- 局部结论：每个细分点 \(z_{ij}\) 仅邻接 \(y_i,y_j\)，故 \(G_k\) 确为 \(K_k\) 的 1-细分。；任意两个 \(y\)-顶点只有一个共同的 \(z\)-邻点，故 \(G_k\) 无 \(C_4\)；细分点一侧最大度为 2。；Janzer 的定理直接给出 \(\mathrm{ex}(n,G_k)=O_k(n^{3/2-1/(4k-6)})\)，因此取 \(c_k=1/(4k-6)>0\) 即得原命题。
- 第一阻塞点：若要求从头证明而非调用已知定理，第一处未在本筛查中重建的是 Janzer 的核心计数/均匀化引理：必须从平均度约 \(n^{1/2+1/(4k-6)}\) 推出一个 \(K_k\) 的规范细分。
- 下一步：逐条核对 Janzer 论文主定理的参数约定（其 \(H_t\) 是否恰为每边细分一次）及常数对 \(k\) 的依赖；摘要已与所需陈述完全吻合。
- 来源核对：[官方条目及两个指数](https://www.erdosproblems.com/1021)；[Janzer：Improved bounds for the extremal number of subdivisions](https://arxiv.org/abs/1809.00468)
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1021)；既有候选答案（按不可信材料审计）

### #1022

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is there a constant $c_t$, where $c_t\to \infty$ as $t\to \infty$, such that if $\mathcal{F}$ is a finite family of finite sets, all of size at least $t$, and for every set $X$ there are $<c_t\lvert X\rvert$ many $A\in \mathcal{F}$ with $A\subseteq X$, then $\mathcal{F}$ has chromatic number $2$ (in other words, has property B)?
- 题意摘要：按通常约定量词为：是否存在一列正数 \((c_t)\) 且 \(c_t\to\infty\)，使得对每个 \(t\) 和每个边大小至少 \(t\) 的有限超图 \(\mathcal F\)，若每个非空顶点集 \(X\) 所含超边数小于 \(c_t|X|\)，则 \(\mathcal F\) 可二染色且无单色边。若字面允许 \(X=\varnothing\)，则 \(0<0\) 永远不成立，命题会平凡真；显然不是原意。
- 状态核对：输入称“proved (Lean)”，但当前官方页内部矛盾：页眉写 affirmative/Lean，正文明确写命题为假并引用 Wood 反例，而且又显示没有形式化链接。数学上应判定为已被反例否定；无法从页面核实 Lean 声称。人工评审指出旧候选需修正是正确的。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：修补并独立核对旧候选的两层构造。取 \(|\Gamma|=3t\)。对每对有序 \(t\)-子集 \(A,B\subseteq\Gamma\) 加顶点 \(v_{A,B}\) 及边 \(A\cup\{v\},B\cup\{v\}\)；再对 \(t\)-子集 \(Q\subseteq\Gamma,R\subseteq V\) 加 \(w_{Q,R}\) 及边 \(Q\cup\{w\},R\cup\{w\}\)。
- 局部结论：每条边大小均为 \(t+1\ge t\)。把每条边指向其新顶点 \(v\) 或 \(w\)，每个新顶点至多被两条边指向；故每个 \(X\) 所含边数至多 \(2|X|\)。；若 \(\Gamma\) 两色各至少 \(t\) 个，选异色的 \(t\)-集 \(A,B\)，无论 \(v_{A,B}\) 取何色都会产生单色边。；否则某色在 \(\Gamma\) 中至少 \(2t+1\) 个。取两个不交的同色 \(t\)-集，可强迫至少 \(t\) 个不同的第一层顶点为反色，组成 \(R\)；再取同色的 \(t\)-集 \(Q\subseteq\Gamma\)，顶点 \(w_{Q,R}\) 无论取何色都产生单色边。因此该超图不可二染色。
- 第一阻塞点：旧候选的首个实际错误是：构造只为 \(|Q|=t\) 定义 \(w_{Q,R}\)，证明却取了 \(|Q|=2t\)。上述证明改取任意同色 \(t\)-集 \(Q\) 后闭合。另须明确排除空集 \(X\)。
- 下一步：核查所谓 Lean 形式化仓库及其实际定理方向；数学反例本身已闭合。由于 \(c_t\to\infty\) 必有某个大 \(t\) 满足 \(c_t>2\)，上述 \(\le2|X|<c_t|X|\) 即否定原意下的命题。
- 来源核对：[官方当前页：正文给出 Wood 反例，但元数据互相矛盾](https://www.erdosproblems.com/1022)；[Wood：任意 r≥2 存在色数 3 的 2-degenerate r-uniform 超图](https://arxiv.org/abs/1310.2972)
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1022)；既有候选答案（按不可信材料审计）

### #1029

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $R(k)$ is the Ramsey number for $K_k$, the minimal $n$ such that every $2$-colouring of the edges of $K_n$ contains a monochromatic copy of $K_k$, then\[\frac{R(k)}{k2^{k/2}}\to \infty.\]
- 题意摘要：令 \(R(k)=R(k,k)\)。命题断言：对每个固定 \(M>0\)，存在 \(k_0\)，使所有 \(k\ge k_0\) 都有 \(R(k)>M k2^{k/2}\)。
- 状态核对：截至官方当前页仍为开放问题。旧候选只陈述状态，没有形成证明路线；其 Spencer 常数界与官方材料一致。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：检验最直接的随机二染色路线。对 \(K_N\) 各边独立等概率染色，令 \(X\) 为单色 \(K_k\) 数，则 \(\mathbb E X=2\binom Nk2^{-\binom k2}\)。令 \(N=c(k)k2^{k/2}\)，检查一阶矩能否容许 \(c(k)\to\infty\)。
- 局部结论：由 \(\binom Nk\le(eN/k)^k\)，有 \(\mathbb EX\le2(e\sqrt2\,c(k))^k\)。所以一阶矩仅在 \(c<1/(e\sqrt2)\) 时直接给出构造，恢复经典常数量级。；Spencer 的依赖控制把常数提高到 \(\sqrt2/e\)，但仍只证明比值有正常数下界。；若 \(c(k)\to\infty\)，上述期望上界本身指数爆炸；因此“证明不存在单色团”的简单并合界在所需尺度上失效。
- 第一阻塞点：第一处无法闭合的是把“单色 \(K_k\) 的期望很大”转化为仍存在零个坏事件的染色；标准局部引理只能利用有限依赖，重叠团簇的累积贡献在 \(c(k)\to\infty\) 时没有足够小的活动度。
- 下一步：计算坏事件簇展开中由两 个 \(K_k\) 交叠 \(j\) 个顶点产生的总贡献，并检验是否存在随 \(k\) 增长的截断阶数，使聚合局部引理仍收敛；这是对随机路线明确可证伪的下一步。
- 来源核对：[官方条目：open；经典界与 Spencer 界](https://www.erdosproblems.com/1029)
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1029)；既有候选答案（按不可信材料审计）

### #1030

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $R(k,l)$ is the Ramsey number then prove the existence of some $c>0$ such that\[\lim_k \frac{R(k+1,k)}{R(k,k)}> 1+c.\]
- 题意摘要：以 \(R(s,t)\) 表示每个红蓝染色必含红 \(K_s\) 或蓝 \(K_t\) 的最小阶数。要求存在绝对常数 \(c>0\)，使 \(R(k+1,k)/R(k,k)\) 的极限存在且大于 \(1+c\)；通常核心意图至少是证明该比值最终与 1 隔开。
- 状态核对：官方当前页仍列为开放。旧候选中的加点构造可以严格成立，并实际给出 \(R(k+1,k)-R(k,k)\ge k-1\)；这只比官方列出的较弱“平凡界” \(k-2\) 多 1，不接近所需乘法界。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：从一个阶为 \(r-1\)、同时无红蓝 \(K_k\) 的极值染色出发，其中 \(r=R(k,k)\)。加入 \(k-1\) 个新顶点 \(B\)，令 \(B\) 内全蓝、旧新之间全红。
- 局部结论：蓝 \(K_k\) 不能跨越新旧部分；旧部分没有蓝 \(K_k\)，而 \(|B|=k-1\)，故不存在蓝 \(K_k\)。；红团在 \(B\) 中至多取一个顶点，旧部分的红团至多为 \(K_{k-1}\)，故不存在红 \(K_{k+1}\)。；由此得到 \(R(k+1,k)\ge R(k,k)+k-1\)，即差至少 \(k-1\)。该推导自足，但除以指数增长的 \(R(k,k)\) 后附加项趋于 0。
- 第一阻塞点：第一处断裂是尝试把新顶点数由 \(k-1\) 提升到 \(\Omega(R(k,k))\)：单个全蓝新块必须小于 \(k\)，而使用多个块或非单色块时，跨块红边会与旧图中的大量红 \((k-1)\)-团组合；现有构造没有控制这些团的数量和交叠。
- 下一步：把一般扩张写成约束系统：对旧染色中的每个红 \(K_k\)、蓝 \(K_{k-1}\) 记录一个禁模式，先证明“若这些禁模式的最大共度不超过 \(D_k\)，则可加入 \(\varepsilon R(k,k)\) 个顶点”的条件引理；随后检查已知 Ramsey multiplicity 界是否足以给出所需 \(D_k\)。
- 来源核对：[官方条目：open；列出 k−2 与 2k−5 的已知差值界](https://www.erdosproblems.com/1030)
- 时间记账：所在批次墙钟时间按题数均摊约 51.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1030)；既有候选答案（按不可信材料审计）

### #1032

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：We say that a graph is $4$-chromatic critical if it has chromatic number $4$, and removing any edge decreases the chromatic number to $3$. Is there, for arbitrarily large $n$, a $4$-chromatic critical graph on $n$ vertices with minimum degree $\gg n$?
- 题意摘要：量词为：是否存在绝对常数 $c>0$，以及无界的一列整数 $n$，使每个相应的 $n$ 上都有简单图 $G_n$，满足 $\chi(G_n)=4$、对每条边 $e$ 都有 $\chi(G_n-e)=3$，且 $\delta(G_n)\ge cn$。并非要求每个充分大的 $n$ 都存在。
- 状态核对：冻结状态及当前官方页均为 open；已知构造仅达到 $\delta\gg n^{1/3}$。候选答案没有解决问题，其独立集检查成立，但只给出假设常数 $c\le3/4$。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：尝试把固定的 4-染色临界图作等比例独立集 blow-up，以获得线性最小度，再从稠密 blow-up 中抽取边极小的 4-染色子图。第一步确实保持色数：各簇取一个代表即得到原图。但若每个簇至少有两个顶点，删除任意一条 blow-up 边后仍可避开其端点选代表，留下原 4-染色图，因此 blow-up 本身绝不边临界。再取边极小子图虽可恢复临界性，却没有机制保持线性最小度。
- 局部结论：对每条边 $uv$，任一 $G-uv$ 的 3-染色都必须令 $u,v$ 同色，否则它也是 $G$ 的 3-染色。；没有孤立点的 4-边临界图满足 $\delta(G)\ge3$：先由删除一条邻边得到 $G-v$ 的 3-染色；若 $d(v)\le2$，总有一种颜色可赋给 $v$，矛盾。；任意 4-色图有大小至少 $n/4$ 的独立集；取其中顶点得 $\delta(G)\le3n/4$，故可能的线性常数至多 $3/4$。
- 第一阻塞点：从稠密 4-色图中取边极小的 4-色子图时，顶点度可能从 $\Theta(n)$ 降到常数；尚无可用的不变量阻止这种坍缩。
- 下一步：对具体的高对称 blow-up，计算所有边极小 4-色生成子图的最小度；先检验能否证明其中必有度 $O(n^{1/3})$ 或构造出反例。这是可有限验证的小规模整数规划任务。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1032)仍列为 OPEN，并记录 Simonovits–Toft 的 $n^{1/3}$ 构造。
- 时间记账：所在批次墙钟时间按题数均摊约 54.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1032)；既有候选答案（按不可信材料审计）

### #1033

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $h(n)$ be such that every graph on $n$ vertices with $>n^2/4$ many edges contains a triangle whose vertices have degrees summing to at least $h(n)$. Estimate $h(n)$. In particular, is it true that\[h(n)\geq (2(\sqrt{3}-1)-o(1))n?\]
- 题意摘要：精确定义为 $h(n)=\min_G\max_{uvw\in K_3(G)}(d(u)+d(v)+d(w))$，其中最小值遍历所有 $n$ 顶点且 $e(G)>n^2/4$ 的简单图。问题问其渐近值，特别是否下界达到 $(2(\sqrt3-1)-o(1))n$。
- 状态核对：冻结状态和当前官方页均为 open；已知 $\frac{21}{16}n\le h(n)\le2(\sqrt3-1)n+O(1)$。候选构造本质正确，但参数化较绕；官方参数化可更直接核算。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建上界构造。令 $m=\lfloor n^2/4\rfloor+1$，分割 $V=K\sqcup L$，$|K|=k=cn+O(1)$、$|L|=l=n-k$，先放入完整二部图，再在 $K$ 内放一个三角形自由、近正则的二部图 $H$，边数 $q=m-kl$、最大度至多 $\lceil2q/k\rceil$。当 $q\le k^2/4$ 时该 $H$ 存在。所有三角形恰含 $H$ 的一条边和 $L$ 的一个顶点。
- 局部结论：任一三角形的度数和至多 $k+2l+2\lceil2q/k\rceil=(c^{-1}+3c-2)n+O(1)$。；函数 $c^{-1}+3c-2$ 在 $c=1/\sqrt3$ 处取最小值 $2(\sqrt3-1)$。；此时 $q/k^2\to(1-\sqrt3/2)^2<1/4$，故内部三角形自由图的容量条件严格满足；上界构造闭合。
- 第一阻塞点：上界路线不能推出猜想所需下界。第一处缺口是：Mantel 稳定性只能说明近极值图接近二部图，却不能保证某条内部边的两个端点同时具有足够大的跨部度，从而达到目标三角形度数和。
- 下一步：证明或反驳如下局部稳定性命题：在最大割 $A\cup B$ 中，若 $e(G)>n^2/4$ 且所有内部边 $uv\subset A$ 都满足 $d(u)+d(v)+\max_{w\in N(u)\cap N(v)\cap B}d(w)<\alpha n$，则 $\alpha\ge2(\sqrt3-1)-o(1)$。可先把它写成部大小、内部度和缺边数的有限优化问题。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1033)给出同一构造、常数计算以及 Fan 的 $21/16$ 下界。
- 时间记账：所在批次墙钟时间按题数均摊约 54.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1033)；既有候选答案（按不可信材料审计）

### #1035

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Is there a constant $c>0$ such that every graph on $2^n$ vertices with minimum degree $>(1-c)2^n$ contains the $n$-dimensional hypercube $Q_n$?
- 题意摘要：量词为：是否存在与维数 $n$ 无关的绝对常数 $c>0$，使对每个 $n$，每个恰有 $N=2^n$ 个顶点且 $\delta(G)>(1-c)N$ 的简单图都含有一个非诱导子图 $Q_n$。
- 状态核对：冻结状态及当前官方页均为 open。候选答案的 Sauer–Spencer 基线方向正确，但只得到随 $n$ 衰减的容许缺边比例，不能回答原题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：令 $F=\overline G$。若能把 $F$ 与 $Q_n$ 在同一 $N$ 点集上边不交放置，就得到 $Q_n\subseteq G$。应用 Sauer–Spencer packing 条件 $2\Delta(F)\Delta(Q_n)<N$，并用 $\Delta(Q_n)=n$。
- 局部结论：由 $\delta(G)>N-N/(2n)$ 得 $\Delta(F)<N/(2n)$，故 $2\Delta(F)n<N$，从而 $Q_n$ 可嵌入 $G$。；因此无条件基线为 $u_n\ge N/(2n)$（忽略严格不等式造成的整数取整），即 $c_n\asymp1/n$。；该归约说明困难不在平均边数，而在能否利用 $Q_n$ 的特殊分层结构，突破一般 packing 定理对 $\Delta(Q_n)=n$ 的损失。
- 第一阻塞点：一般 packing 的局部交换论证每次可能牵涉 $n\Delta(F)$ 个冲突；若 $\Delta(F)=cN$，此量远超 $N$。没有利用超立方体坐标结构消去因子 $n$ 的严格步骤。
- 下一步：检验随机仿射标号 $x\mapsto Ax+b$（而非任意随机排列）下坏立方体边的依赖结构，计算能否用局部引理在 $\Delta(F)=cN$ 时同时避开全部坏边；首先精确估计一条坏边影响多少坐标边事件。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1035)仍列为 OPEN。；[Sauer–Spencer 原论文页面](https://www.sciencedirect.com/science/article/pii/0095895678900059)对应 1978 年 edge-disjoint placement 定理。
- 时间记账：所在批次墙钟时间按题数均摊约 54.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1035)；既有候选答案（按不可信材料审计）

### #1038

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Determine the infimum and supremum of\[\lvert \{ x\in \mathbb{R} : \lvert f(x)\rvert < 1\}\rvert\]as $f\in \mathbb{R}[x]$ ranges over all non-constant monic polynomials, all of whose roots are real and in the interval $[-1,1]$.
- 题意摘要：遍历所有次数任意但至少为一的首一实多项式 $f$，要求其全部根（计重数）都在 $[-1,1]$；分别求实数集 $S_f=\{x:|f(x)|<1\}$ 的 Lebesgue 测度之下确界与上确界。
- 状态核对：问题整体仍 open，因为下确界未知；上确界已知为 $2\sqrt2$。当前记录为 $2^{4/3}-1\le\inf |S_f|\le1.835\ldots$。候选答案有一处明确错误：对 $f=x^2-1$，$S_f$ 不是整段 $(-\sqrt2,\sqrt2)$，而是删去 $0$；测度结论仍正确。其“强烈证据表明真值约为 1.835”没有所给来源支持，不应采纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先重建上确界的极值例，再尝试用根移动到端点证明一般上界。对 $f=x^2-1$，严格解不等式得到 $0<x^2<2$，故 $S_f=(-\sqrt2,0)\cup(0,\sqrt2)$，测度为 $2\sqrt2$。对一般 $f=\prod(x-r_i)$，固定 $x$ 时把根移向端点会单调改变某些因子，却会在不同 $x$ 区域以相反方向改变乘积，因此逐点端点化不能直接比较整个次水平集的测度。
- 局部结论：边界集 $\{|f|=1\}$ 是有限集，所以把 $<1$ 攏为 $\le1$ 不改变测度。；极值例 $x^2-1$ 严格给出 $\sup |S_f|\ge2\sqrt2$；漏掉单点 $0$ 不影响测度。；对 $f_m=(x+1)(x-1)^m$，在 $(-1,1)$ 上函数模为 $(x+1)(1-x)^m$，其唯一内部极大点为 $x=(1-m)/(m+1)$；当该极大值超过 $1$ 时，内部会出现被排除区间，这解释了为何该族可使测度低于 $2$。
- 第一阻塞点：根端点化缺少保持或增大 $|S_f|$ 的整体重排不等式；因此无法从极值例独立闭合对任意根配置的 $2\sqrt2$ 上界，更无法推出下确界的精确值。
- 下一步：对单根变分 $r_i\mapsto r_i+t$，在所有横截边界点 $x_j(t)$ 满足 $|f_t(x_j)|=1$ 时，显式计算 $d|S_{f_t}|/dt$；检验内部临界点是否只能在成对根合并或根到达 $\pm1$ 时出现。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1038)记录 $\sup=2\sqrt2$ 及当前下确界区间。；[Erdős–Herzog–Piranian 原论文扫描件](https://users.renyi.hu/~p_erdos/1958-05.pdf)核对了问题来源。
- 时间记账：所在批次墙钟时间按题数均摊约 54.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1038)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1038.lean`；既有候选答案（按不可信材料审计）

### #1039

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)=\prod_{i=1}^n(z-z_i)\in \mathbb{C}[z]$ with $\lvert z_i\rvert \leq 1$ for all $i$. Let $\rho(f)$ be the radius of the largest disc which is contained in $\{z: \lvert f(z)\rvert< 1\}$. Determine the behaviour of $\rho(f)$. In particular, is it always true that $\rho(f)\gg 1/n$?
- 题意摘要：对每个次数 $n$ 及每个首一多项式 $f(z)=\prod_{i=1}^n(z-z_i)$（所有 $|z_i|\le1$），令 $\rho(f)$ 为开集 $\{|f|<1\}$ 所含圆盘半径的上确界。核心一致量词是：是否存在绝对常数 $c>0$，对所有 $n,f$ 均有 $\rho(f)\ge c/n$。
- 状态核对：按冻结日期 2025-12-26，应记为 open，已发表/预印本基线是 $\rho(f)\gg1/(n\sqrt{\log n})$。但 2026 年 5 月论坛出现一个声称证明 $\rho(f)\ge(\log2-o(1))/n$ 的乘积论证，并有人工审读及 Lean 尝试；官方页仍标 OPEN，故这里只评为“很有希望的冻结后候选”，不擅自宣告解决。候选旧答案在冻结时点正确，但现在遗漏了这一后续信号。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `medium`
- 尝试路线：复核冻结后的具体路线。固定 $0<c<\log2$，反设每个 $B(z_j,c/n)$ 都不包含于 $\{|f|<1\}$，则可选 $w_j$ 满足 $|w_j-z_j|<c/n$ 且 $|f(w_j)|\ge1$。若能证明乘积不等式 $\prod_j|f(w_j)|\le(((1+\varepsilon)^n-1)^n)$，其中 $\varepsilon=c/n$，则右端小于 $(e^c-1)^n<1$，与左端至少 $1$ 矛盾。于是某个以零点为圆心、半径 $c/n$ 的圆盘完全落在次水平集中。
- 局部结论：一旦上述乘积不等式成立，对任意 $c<\log2$ 都严格推出 $\rho(f)\ge c/n$；量词和极限步骤没有额外缺口。；例 $f(z)=z^n-1$ 给出 $\rho(f)\le\pi/(2n)$，所以最坏情形的量级不可能优于 $1/n$。；冻结时已可靠核验的一般下界为 $c_0/(n\sqrt{\log n})$，与上例只差 $\sqrt{\log n}$。
- 第一阻塞点：本次独立筛查尚未从头证明核心乘积不等式；逐因子粗估只给出 $[\varepsilon(2+\varepsilon)^{n-1}]^n$，远远不够。所需改进依赖所有零点间距离的全局乘积结构，不能以论坛中的“已有证明”代替审稿。
- 下一步：逐行重建并形式核验引理：若 $|z_i|\le1$ 且 $|w_i-z_i|\le\varepsilon$，则 $\prod_i\prod_j|w_i-z_j|\le((1+\varepsilon)^n-1)^n$；重点检查重根、$\varepsilon=0$、严格/非严格边界及 Hadamard/Vandermonde 步骤。
- 来源核对：[官方问题页及讨论](https://www.erdosproblems.com/forum/thread/1039)仍显示 OPEN，同时载有冻结后的乘积论证、审读意见和形式化声称。；[KLR 2025 预印本](https://arxiv.org/abs/2503.18270)明确给出 $1/(n\sqrt{\log n})$ 级下界。
- 时间记账：所在批次墙钟时间按题数均摊约 54.8 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1039)；既有候选答案（按不可信材料审计）

### #1040

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $F\subseteq \mathbb{C}$ be a closed infinite set, and let $\mu(F)$ be the infimum of\[\lvert \{ z: \lvert f(z)\rvert < 1\}\rvert,\]as $f$ ranges over all polynomials of the shape $\prod (z-z_i)$ with $z_i\in F$. Is $\mu(F)$ determined by the transfinite diameter of $F$? In particular, is $\mu(F)=0$ whenever the transfinite diameter of $F$ is $\geq 1$?
- 题意摘要：对每个闭无限集 F⊆ℂ，令 μ(F) 为所有有限次数、首一且零点（允许重复）均在 F 中的多项式 p(z)=∏(z-z_i)之集合 {|p|<1} 的平面面积下确界。问题包括：(i) 是否存在仅依赖横截直径 ρ(F) 的函数 Φ 使 μ(F)=Φ(ρ(F))；(ii) 对每个 ρ(F)≥1 的 F，是否必有 μ(F)=0。
- 状态核对：输入的 open 状态需要细分：第一问已有反例；第二问对无界 F、cap(F)>1 的紧集，以及若干 cap(F)=1 的正则紧集已成立，但一般不规则的单位容量紧集仍未闭合。旧候选的无界论证错误地假定 F 同时含 ±R；可改成固定 a∈F 并取 |b-a|→∞。其更严重错误是把 KLR 的 C² 边界定理误报成任意单位容量紧集定理。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：先构造同容量反例。取 F₁={0}∪{1/n:n≥1}。任意零点在 F₁⊂[0,1] 的 p 都在圆盘 D(1/2,1/2) 上满足每个 |z-z_i|<1，故 μ(F₁)≥π/4。取 R=4 及 F₂={0,R}∪{1/n}∪{R+1/n}；两集均为可数紧集，故容量为 0。对 q(z)=z(z-R)，令 u=(z-R/2)²，则面积换元给出 |{|q|<1}|=∫_{|u-R²/4|<1}(2|u|)⁻¹dA(u)≤2π/(R²-4)=π/6。因此 μ(F₂)≤π/6<μ(F₁)，否定第一问。再对无界 F 使用相距趋于无穷的 a,b∈F 及同一二次估计，得到 μ(F)=0。
- 局部结论：μ 并不由横截直径唯一决定；容量同为 0 的 F₁、F₂ 已给出严格分离 μ(F₁)≥π/4>π/6≥μ(F₂)。；若 F 无界，则选固定 a∈F 和 |b_k-a|→∞；p_k=(z-a)(z-b_k) 的单位次水平集面积至多 2π/(|b_k-a|²-4)，故 μ(F)=0。；2026 年预印本给出任意紧集 cap(F)>1 时的肯定结果；cap(F)=1 时，KLR 目前覆盖有 C² 光滑边界等正则情形。
- 第一阻塞点：第一处不能闭合的是一般紧集 cap(F)=1：把平衡测度离散化为零点经验测度，并不能在无边界正则性时推出单位次水平集面积趋于 0；KLR 定理明确要求足够光滑，不能直接套用。
- 下一步：检验单位容量的一类最小非正则模型（例如正容量 Cantor 集或边界含尖点的满紧集）：构造离散平衡测度 p_n，并估计 m({U_{ν_n}<0})；首要检查能否由能量收敛升级为该负势集合的面积收敛。
- 来源核对：[Erdős Problems #1040](https://www.erdosproblems.com/1040) 记录第一问的容量零反例，并仍将总体问题列为 open。；[KLR 预印本](https://arxiv.org/abs/2503.18270) 的 Theorem 6 只处理闭包具有 C² 光滑边界的单位容量集合；旧候选扩大了量词。；[Ghosh–Ramachandran 2026](https://arxiv.org/abs/2604.03036) 声称解决任意紧集容量严格大于 1 的情形。
- 时间记账：所在批次墙钟时间按题数均摊约 53.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1040)；既有候选答案（按不可信材料审计）

### #1044

- 当前状态：`solved (Lean)`（冻结清单状态：`open`）
- 精确题面：Let $f(z)=\prod_{i=1}^n(z-z_i)\in\mathbb{C}[x]$ where $\lvert z_i\rvert\leq 1$ for all $i$. If $\Lambda(f)$ is the maximum of the lengths of the boundaries of the connected components of\[\{ z: \lvert f(z)\rvert<1\}\]then determine the infimum of $\Lambda(f)$.
- 题意摘要：量词是对所有次数 n≥1 以及所有零点满足 |z_i|≤1 的首一多项式 f。对 {|f|<1} 的每个连通分支 U 取边界长度，并令 Λ(f)=max_U length(∂U)；求跨全部次数和全部 f 的 inf Λ(f)。
- 状态核对：已解决，值为 2，且有限次数时不取到。旧候选结论正确，但其“取包含 0 的分支”不可靠：当所有 |z_i|=1 时可能有 |f(0)|=1，因而 0 不属于 {|f|<1}。正确引用是 Pommerenke 定理保证存在某个分支，而非指定包含 0 的分支。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：下界路线：Pommerenke 1961 的 Theorem 3 对此零点约束推出存在分支 U，使 diam(∂U)>1。多项式引理线的分支边界为有限可求长闭曲线；沿边界连接一对实现直径的点，两向弧长各至少该直径，故 length(∂U)≥2 diam(∂U)>2。上界取 f_n(z)=z^n-1。每瓣边界满足 r^n=2cos(nθ)，|θ|≤π/(2n)，直接积分得到 L_n=(2^{1/n}/n)B(1/(2n),1/2)→2。
- 局部结论：每个固定 admissible f 都有 Λ(f)>2。；对 f_n=z^n-1，各瓣全等，且 Λ(f_n)=(2^{1/n}/n)B(1/(2n),1/2)→2。；合并得 inf_f Λ(f)=2；严格下界说明没有有限次数多项式达到 2。
- 第一阻塞点：重建证明本身已闭合；唯一非初等输入是需核对 Pommerenke Theorem 3 的精确归一化确实给出 diam(∂U)>1。官方解答和 Tang 的注记采用的正是这一版本。
- 下一步：若要求完全自足或重新形式化，应把 Pommerenke Theorem 3 的归一化陈述录入，并证明引理线分支边界的可求长性及 length≥2diam；随后核验 Beta 积分极限。
- 来源核对：[Erdős Problems #1044](https://www.erdosproblems.com/1044) 记录 Tang 的答案 2。；[讨论页的证明提要](https://www.erdosproblems.com/forum/thread/1044) 明确使用 Pommerenke Theorem 3 保证“存在某个分支”边界直径大于 1，并记录 Lean 形式化链接。；当前本地 cohort 中未找到 1044.lean，故本轮无法从本地文件独立执行内核检查。
- 时间记账：所在批次墙钟时间按题数均摊约 53.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1044)；既有候选答案（按不可信材料审计）

### #1049

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $t>1$ be a rational number. Is\[\sum_{n=1}^\infty\frac{1}{t^n-1}=\sum_{n=1}^\infty \frac{\tau(n)}{t^n}\]irrational, where $\tau(n)$ counts the divisors of $n$?
- 题意摘要：对每个有理数 t>1，问实数 S(t)=∑_{n≥1}1/(t^n-1) 是否无理。等式右端的量词同样是 n≥1，τ(n) 为正因子个数；需先证明两级数收敛且相等，再研究每个有理 t，而不只是整数 t。
- 状态核对：截至核查仍为 open；整数 t≥2 是 Erdős 1948 的已知子情形。本地 Lean 文件也把一般定理标为 research open，且证明体仍是 sorry，不能视为形式证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：令 t=a/b，a>b≥1 且 gcd(a,b)=1。由正项 Tonelli 展开 1/(t^n-1)=∑_{k≥1}t^{-nk}，按 m=nk 重排得到 S=∑_{m≥1}τ(m)(b/a)^m。尝试以 a^N 清除前 N 项分母：若 S=p/q，则 I_N=q a^N(S-S_N) 是正整数。希望证明 I_N<1，但首个尾项已给 I_N≥qτ(N+1)b^{N+1}/a；当 b≥2 时反而指数增长，所以最直接的清分母—小尾项路线在第一步即失败。
- 局部结论：Lambert 恒等式严格成立：绝对（事实上正项）收敛允许按乘积 m=nk 重排，系数恰为 τ(m)。；对 t=a/b，a^N S_N∈ℤ；若 S∈ℚ，便得到一列正整数 q a^N(S-S_N)。；当分母 b>1 时，上述整数的首尾项下界呈 b^N 级增长，说明 Erdős 的整数基数方法不能仅靠机械清分母推广。
- 第一阻塞点：需要在某些特殊 N 上制造算术抵消或更合适的分母，使“非零整数”同时趋于 0；普通分母 a^N 无法做到。对 b>1，分子 b^n 引入的增长正是首个严格障碍。
- 下一步：把 Erdős 1948 对整数基数的“长零块/除数函数同余”步骤逐行改写为 t=a/b：选择具有受控小素数倍数结构的 N，计算长度 L 的窗口 τ(N+j)b^{N+j} mod a^L，检验是否能同时控制进位与窗口后的尾项。
- 来源核对：[Erdős Problems #1049](https://www.erdosproblems.com/1049) 仍列为 open，并只记录整数 t≥2 的 Erdős 定理。；本地 [1049.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1049.lean) 的一般结论为 `answer(sorry)` 且证明为 `sorry`；Lambert 恒等式条目也尚未填证。
- 时间记账：所在批次墙钟时间按题数均摊约 53.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1049)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1049.lean`；既有候选答案（按不可信材料审计）

### #1051

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Is it true that if $a_1<a_2<\cdots$ is a sequence of integers with\[\liminf a_n^{1/2^n}>1\]then\[\sum_{n=1}^\infty \frac{1}{a_na_{n+1}}\]is irrational?
- 题意摘要：对每个严格递增整数序列 a_1<a_2<⋯，若 liminf_{n→∞}a_n^{1/2^n}>1，则断言 S=∑_{n≥1}1/(a_na_{n+1}) 无理。条件隐含最终 a_n>0；删除有限个初项只使 S 改变一个有理数，故可归约到正整数序列。
- 状态核对：已肯定解决，并有 Lean 形式化记录。旧候选称其仍开放已过时；其附带的“Q_N=∏a_k 后尾项是整数”论证也有错误：Q_N 只清除部分和，若假设 S=p/q，则 qQ_NS 与 qQ_NS_N 都是整数才可得尾部整数，这一点可以成立，但候选声称的 Q_N(S-S_N)<2/a_{N+1} 并不由 a_{n+1}≥a_n²直接得到，因为 Q_N 含全部早期因子，所给估计未经证明。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：用 2026 年 Barreto–Kang–Kim–Kovač–Zhang 定理归约。设 φ=(1+√5)/2。由 liminf a_n^{1/2^n}>1，可取 c>1，使充分大 n 有 log a_n≥2^n log c。因此 log a_n/φ^n≥(2/φ)^nlog c→∞，即 a_n^{1/φ^n}→∞。严格递增正整数又给 a_n≥n，从而满足该定理所需的多项式下界；应用其 d=2 情形即得 S 无理。
- 局部结论：原假设严格强于临界增长条件 limsup a_n^{1/φ^n}=∞，因为 2/φ>1。；严格递增正整数自动满足 a_na_{n+1}≥n(n+1)，所以论文中的辅助下界无需另加假设。；有限平移到正整数尾序列只改变总和一个有理数，不影响无理性；故原量词得到肯定答案。
- 第一阻塞点：数学重建在引用 2026 年主定理后闭合。本地快照中的 erdos_1051 定理体仍写 `by sorry`，因此本轮不能仅凭该本地文件完成 Lean 内核复核；“proved (Lean)”依赖官方链接所指的外部形式化。
- 下一步：下载官方链接对应的无 `sorry` Lean 提交，核验其 GrowthCondition 对整数实幂的定义、有限移位到正数序列的处理，以及所用定理是否与论文 d=2 版本完全同量词。
- 来源核对：[Erdős Problems #1051](https://www.erdosproblems.com/1051) 标为 PROVED (LEAN)，并记录 Aletheia 与后续推广。；[BKKKZ 论文](https://arxiv.org/abs/2601.21442) 给出 φ 临界增长定理；正文明确说明 d=2 推出原问题。；本地 [1051.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1051.lean) 的注释与上述来源一致，但当前文件本身保留 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 53.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1051)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1051.lean`；既有候选答案（按不可信材料审计）

### #1052

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：A unitary divisor of $n$ is $d\mid n$ such that $(d,n/d)=1$. A number $n\geq 1$ is a unitary perfect number if it is the sum of its unitary divisors (aside from $n$ itself). Are there only finite many unitary perfect numbers?
- 题意摘要：对所有 n≥1，单位因子是满足 d|n 且 gcd(d,n/d)=1 的 d；单位完全数满足所有真单位因子之和等于 n。问题是集合 {n≥1:n 为单位完全数} 是否有限。若 n=∏_{i=1}^r p_i^{α_i}，单位因子在每个完整素数幂上作二选一，因此条件等价于 ∏_{i=1}^r(1+p_i^{α_i})=2n。
- 状态核对：仍为 open，已知五例且无奇数例。旧候选的总体状态与乘积公式正确；其更细的历史性有限性断言本轮未从原论文逐条核验，因此不作为证明依赖。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：令 x_i=p_i^{α_i} 并按 x_1<⋯<x_r 排序；方程化为 ∏(1+1/x_i)=2。先固定 r 做递归有界化：若已选 x_1,…,x_{j-1}，令 P=∏_{i<j}(1+1/x_i)<2、k=r-j+1。因余下 x_i≥x_j，有 2/P=∏_{i≥j}(1+1/x_i)≤(1+1/x_j)^k，故 x_j≤((2/P)^{1/k}-1)^{-1}。于是固定 r 时每个 x_j 依次落在有限区间，只有有限多个解。另若 n 为奇数，则左端每个 1+p_i^{α_i} 均为偶数；比较 2-adic 赋值先得 r=1，再由 1+p^α=2p^α 得 p^α=1，矛盾。
- 局部结论：单位完全方程严格等价于 ∏(1+p_i^{α_i})=2∏p_i^{α_i}，或 ∏(1+1/x_i)=2。；不存在奇单位完全数；上述 2-adic 论证同时覆盖所有奇 n>1，而 n=1 可直接排除。；对每个固定的不同素因子数 r，单位完全数只有有限多个；递归上界给出一个可实际枚举的有限盒。
- 第一阻塞点：这条路线的第一处全局障碍是无法给 r=ω(n) 一个统一上界。固定 r 的有限盒随 r 增大，不能推出所有 r 的并集有限；乘积方程本身也允许越来越多、越来越大的因子使乘积逼近 2。
- 下一步：把乘积方程与奇偶性结合，建立素数幂间的有向整除图：若奇 x_i，则 2|x_i+1；继续追踪每个奇素数 ℓ|x_i+1 必须由右端某个 x_j 承担。先计算并证明在无环或有界入度假设下 r 的显式上界，再定位无限 Pratt 型链是否是唯一剩余情形。
- 来源核对：[Erdős Problems #1052](https://www.erdosproblems.com/1052) 仍列为 open，并记录五个已知例及不存在奇数例。；本地 [1052.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1052.lean) 正确形式化真单位因子与有限性命题，但主定理和一般偶性定理在该快照中仍含 `sorry`；前三个小例有可执行证明。
- 时间记账：所在批次墙钟时间按题数均摊约 53.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1052)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1052.lean`；既有候选答案（按不可信材料审计）
- 深度项目：现有计算只给有界盒证据。第一阻塞点是全局旋量因子尾部定理或可执行证书：给出显式截止 B，并证明每个奇 3-Higgs 素数 $p>B$ 的 $\Phi_{4p}(2)$ 都有一个非 3-Higgs 素因子，再附上 $p\le B$ 的完整有限见证表；固定范围计算本身不能控制素因子总数。 [证据](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-02/state.json)

### #1053

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Call a number $k$-perfect if $\sigma(n)=kn$, where $\sigma(n)$ is the sum of the divisors of $n$. Must $k=o(\log\log n)$?
- 题意摘要：量词应理解为：对任意满足 \(\sigma(n_j)=k_jn_j\) 且 \(n_j\to\infty\) 的序列，是否必有 \(k_j/\log\log n_j\to0\)。这里 \(k=\sigma(n)/n\) 随 \(n\) 变化；若仅固定一个 \(k\)，结论当然成立。
- 状态核对：按冻结日期仍为开放问题。Grönwall 定理只给 \(k\le (e^\gamma+o(1))\log\log n\)，不能推出 little-o；候选答案正确地区分了这两者，但没有利用 \(k\)-perfect 方程的额外刚性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试利用素因子“闭包”。写 \(n=\prod_p p^{a_p}\)。由乘法性，\(k=\prod_{p\mid n}(1+p^{-1}+\cdots+p^{-a_p})\)。同时对每个 \(p\mid n\) 比较 \(\sigma(n)=kn\) 两端的 \(p\)-进赋值，希望证明：若很多小素数使乘积接近 Mertens 上界，则各个 \(\sigma(q^{a_q})\) 的素因子会迫使 \(n\) 含有大量额外素因子，从而让 \(\log\log n\) 比产生 \(k\) 所需的尺度更大。
- 局部结论：无条件有 \(k\le\prod_{p\mid n}(1-1/p)^{-1}\)，结合标准最大阶定理得到 \(k=O(\log\log n)\)。；因 \(p\nmid\sigma(p^{a_p})\)，方程给出精确关系 \[a_p+v_p(k)=\sum_{q\mid n,\ q\ne p}v_p\!\left(\sigma(q^{a_q})\right).\] 因而 \(n\) 中每个素数幂必须由其他素数幂的除数和“供给”。；若存在反例序列使 \(k\ge c\log\log n\)，则其素因子集合必须在调和权重 \(\sum_{p\mid n}1/p\) 意义下接近极值；稀疏或只含大素数的集合不可能产生这种序列。
- 第一阻塞点：第一处无法闭合的是把上述赋值关系转化为统一的“闭包成本”下界。目前没有证明表明近极值的小素数集合必迫使 \(\log n\) 增长到足以得到 \(k=o(\log\log n)\)；这正是一般最大阶论没有提供的信息。
- 下一步：先做可检验的有限版本：给定 \(y\)，从包含全部 \(p\le y\) 的素数集合出发，迭代加入所有 \(\sigma(p^a)\) 的素因子，并计算最小可能的 \(\log n\)；检验能否猜出形如 \(\log n\ge\exp((1+\eta)y)\) 的闭包成本引理。
- 来源核对：[Erdős Problems #1053](https://www.erdosproblems.com/1053) 在冻结记录及当前页面均列为 open。；[Grönwall 定理的 AMS 综述](https://www.ams.org/bull/2013-50-04/S0273-0979-2013-01423-X/S0273-0979-2013-01423-X.pdf)明确给出 \(\limsup\sigma(n)/(n\log\log n)=e^\gamma\)。
- 时间记账：所在批次墙钟时间按题数均摊约 65.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1053)；既有候选答案（按不可信材料审计）

### #1054

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the minimal integer $m$ such that $n$ is the sum of the $k$ smallest divisors of $m$ for some $k\geq 1$. Is it true that $f(n)=o(n)$? Or is this true only for almost all $n$, and $\limsup f(n)/n=\infty$?
- 题意摘要：对每个可表示的 \(N\)，\(f(N)\) 是最小的 \(m\ge1\)，使得对某个 \(k\ge1\)，\(N\) 等于 \(m\) 的前 \(k\) 个最小正因子之和。问题分三层：全体 \(N\) 上是否 \(f(N)=o(N)\)；是否存在密度一集合，在其上该 little-o 成立；以及是否 \(\limsup f(N)/N=\infty\)。此外 \(f(2),f(5)\) 未定义，甚至尚未无条件证明所有 \(N\ge6\) 均在定义域。
- 状态核对：冻结状态 open 是因为定义域和 limsup 部分仍未解决；但前两个 little-o 命题已有反证。候选答案关于密度后果基本正确。需校正：本地 Lean 的第三部分引入密度一集合 \(A\)，却在 limsup 表达式中完全未使用 \(A\)，并非原题的可靠形式化。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：重建 Tao 的计数路线。令 \(\sigma_j(m)\) 为删去 \(m\) 的 \(j\) 个最大因子后其余因子之和。若 \(f(N)=m\)，则对某个 \(j\)，\(N=\sigma_j(m)\)。使用已证明的平均估计 \(\sum_j\sum_{m\le x}\sigma_j(m)\ll x^2\)，再用 Markov 不等式和二进分块计数小比值事件。
- 局部结论：若 \(N\ge Cx\) 且 \(f(N)\le x\)，则存在 \((m,j)\) 满足 \(m\le x\) 且 \(\sigma_j(m)\ge Cx\)。因此这类 \(N\) 的个数至多 \(O(x/C)\)。；取 \(x=\delta t\)、\(C=(2\delta)^{-1}\)，得到 \(\#\{N\in[t/2,t]:f(N)\le\delta N\}\ll\delta^2t\)；二进求和后 \(\#\{N\le X:f(N)\le\delta N\}\ll\delta^2X\)。；选择足够小的固定 \(\delta\)，上一估计同时否定全体上的 \(f(N)=o(N)\) 和任何密度一子集上的 \(f(N)/N\to0\)。更一般地，对任意 \(g(N)=o(N)\)，集合 \(\{N:f(N)\le g(N)\}\) 的上密度为零。
- 第一阻塞点：该路线不能推出大的比值实际无界：密度估计只说明“小比值很稀少”，并不排除 \(f(N)/N\) 被某个有限常数整体控制。第一处缺口正是从密度上界跨到 \(\limsup=\infty\)。
- 下一步：固定 \(A>0\)，尝试证明存在任意大的可表示 \(N\) 满足：对所有 \(m\le AN\) 和所有删尾参数 \(j\)，均有 \(\sigma_j(m)\ne N\)。这是直接对应 \(\limsup>A\) 的有限目标；应先独立核验候选的“正下密度”新主张，冻结 cohort 中不能把评论区声明当成定理。
- 来源核对：[官方页](https://www.erdosproblems.com/1054)记录 Tao 的 \(\ll\delta^2\) 上密度估计及定义域问题。；[讨论页中的推导](https://www.erdosproblems.com/forum/thread/1054)给出了从双重平均估计到二进区间计数的具体步骤。；本地形式化 [1054.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1054.lean) 的 part iii 存在未使用 \(A\) 的量词错误。
- 时间记账：所在批次墙钟时间按题数均摊约 65.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1054)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1054.lean`；既有候选答案（按不可信材料审计）

### #1055

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：A prime $p$ is in class $1$ if the only prime divisors of $p+1$ are $2$ or $3$. In general, a prime $p$ is in class $r$ if every prime factor of $p+1$ is in some class $\leq r-1$, with equality for at least one prime factor. Are there infinitely many primes in each class? If $p_r$ is the least prime in class $r$, then how does $p_r^{1/r}$ behave?
- 题意摘要：应先把类别解释为唯一的最小递归层级：若 \(p+1\) 的素因子全在基础集合 \(\{2,3\}\)，则 \(p\) 属第1类；否则 \(\operatorname{cl}(p)=1+\max_{q\mid p+1}\operatorname{cl}(q)\)。问题问：对每个固定 \(r\ge1\)，第 \(r\) 类是否含无穷多个素数；并问最小者 \(p_r\) 的 \(r\) 次根趋于无穷、保持有界，还是有其他行为。
- 状态核对：冻结状态为 open。候选答案中“每类至少一个”的总体思路可修复，但单凭 Dirichlet 只得到类别严格上升，并不直接得到恰为下一类。另一个重要问题是本地 Lean 定义没有排除低类重复：例如按该谓词，\(5\) 同时满足第1类和第2类条件，与官方 \(p_2=13\) 冲突。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试用递归素因子树研究 \(p_r\)。若 \(p\) 属第 \(r+1\) 类，则 \(p+1\) 有一个第 \(r\) 类素因子 \(q\)。沿这些见证因子向下得到长度 \(r\) 的链，并利用整除关系给出指数级下界；再考察能否用 Dirichlet 在同余类 \(-1\pmod q\) 中制造无限多同层素数。
- 局部结论：对任何第 \(r+1\) 类素数 \(p\)，存在第 \(r\) 类素数 \(q\mid p+1\)，故 \(p+1\ge2q\)，从而 \(p_{r+1}\ge2p_r-1\)。；由 \(p_2=13\) 和递推式，\(p_r-1\ge12\cdot2^{r-2}\)（\(r\ge2\)），所以严格得到 \(\liminf p_r^{1/r}\ge2\)。这只排除了低于2的指数尺度。；取任一已知类别为 \(s\) 的素数 \(q\)，Dirichlet 定理给出无穷多 \(p\equiv-1\pmod q\)；这些 \(p\) 的类别至少为 \(s+1\)。结合类别递归的无跳级性，可证明类别无界并推出每一类非空，但不能推出每一类无限。
- 第一阻塞点：在同余类 \(p\equiv-1\pmod q\) 中，\((p+1)/q\) 的其他素因子可能具有任意高类别，使 \(p\) 跳到更高层。现有素数分布定理无法同时控制这些额外因子的递归类别，因此归纳证明“第 \(r+1\) 类无限”在此首次断裂。
- 下一步：先修正形式化定义：加入“此前各类均不成立”或直接定义唯一 rank；随后对固定 \(r=1,2\) 做筛法实验，计数满足 \(p+1\) 的所有非基础素因子类别恰不超过 \(r-1\) 的素数，检验是否能归约为某个明确的光滑移位素数估计。
- 来源核对：[官方页](https://www.erdosproblems.com/1055)确认序列始于 \(2,13,37,73,1021\)，并记录 Erdős 与 Selfridge 的相反猜测。；本地 [1055.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1055.lean) 的递归谓词会产生类别重叠，不能直接作为官方序列的形式化。
- 时间记账：所在批次墙钟时间按题数均摊约 65.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1055)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1055.lean`；既有候选答案（按不可信材料审计）

### #1056

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$. Does there exist a prime $p$ and consecutive intervals $I_1,\ldots,I_k$ such that\[\prod_{n\in I_i}n \equiv 1\pmod{p}\]for all $1\leq i\leq k$?
- 题意摘要：量词是：对每个整数 \(k\ge2\)，是否存在某个素数 \(p\) 及恰好 \(k\) 个非空、两两相邻的整数区间 \(I_1,\ldots,I_k\)，使每段内全部整数的乘积均模 \(p\) 等于1。\(p\) 和区间均可依赖于 \(k\)。
- 状态核对：冻结状态 open。候选答案的阶乘余数归约是有效的，但必须先说明总区间不跨越 \(p\) 的倍数；其列举的四组阶乘余数及 \(3011,52163\) 的素性已用独立有限计算核验。有限例子不能解决全称量词。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：设相邻端点为 \(c_0<c_1<\cdots<c_k\)，其中 \(I_i=[c_{i-1}+1,c_i]\)。由于任一段含 \(p\) 的倍数都会使乘积为0，整个连续块不能含这种倍数，且长度小于 \(p\)。整体平移一个 \(p\) 的倍数后可令 \(0\le c_0<\cdots<c_k<p\)。于是每段条件等价于 \(c_i!\equiv c_{i-1}!\pmod p\)。路线转化为寻找阶乘映射的高重数纤维。
- 局部结论：原问题严格等价于：对每个 \(k\ge2\)，存在素数 \(p\) 和 \(0\le c_0<\cdots<c_k<p\)，使 \(c_0!\equiv\cdots\equiv c_k!\pmod p\)。；Wilson 定理给出 \(0!=1!=(p-2)!\equiv1\pmod p\)，故任意奇素数 \(p\ge5\) 已给出 \(k=2\) 的解。；独立计算确认：模17时 \(0!,1!,5!,11!,15!\equiv1\)，所以实际上得到 \(k=4\)；模23时有六个相应端点，得到 \(k=5\)。候选所列模3011的11个端点和模52163的13个端点也全部核验为余数1。
- 第一阻塞点：鸽巢原理只保证某个阶乘余数出现约一次，不能保证最大纤维随 \(p\) 无界；阶乘序列又不是独立随机样本。第一处缺口是证明存在素数序列 \(p\) 使映射 \(n\mapsto n!\bmod p\) 的最大纤维趋于无穷。
- 下一步：实现可复核搜索：逐素数计算全部阶乘余数的最大重数 \(M(p)\)，寻找 \(M(p)\ge k+1\) 的最小见证，并统计尾分布；理论上下一步检验二阶矩 \(\sum_a \binom{|\{n:n!=a\}|}{2}\) 是否能通过同余 \(\prod_{j=m+1}^n j\equiv1\) 获得无界下界。
- 来源核对：[官方页](https://www.erdosproblems.com/1056)确认一般问题开放，并给出 \(k=2,3\) 的经典见证。；本地 [1056.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1056.lean)使用严格递增边界，准确表达非空相邻区间。；已独立逐项计算候选列出的四组阶乘余数，并试除确认 \(17,23,3011,52163\) 均为素数。
- 时间记账：所在批次墙钟时间按题数均摊约 65.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1056)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1056.lean`；既有候选答案（按不可信材料审计）

### #1057

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $C(x)$ count the number of Carmichael numbers in the interval $[1,x]$. Is it true that $C(x)=x^{1-o(1)}$?
- 题意摘要：\(C(x)\) 计数不超过实数 \(x\) 的 Carmichael 合数。问题问 \(C(x)=x^{1-o(1)}\)，即 \(\log C(x)/\log x\to1\)；因 \(C(x)\le x\)，等价于对每个固定 \(\varepsilon>0\)，充分大时 \(C(x)\ge x^{1-\varepsilon}\)。
- 状态核对：冻结状态 open。候选答案正确指出这是下界问题，但把 Harman 指数写成了 \(0.3336704\)；原文所用乘积是 \(0.7039\cdot0.4736=0.33336704\)。冻结材料中的 \(0.33336704\) 才是应保留的数值。冻结日期之后 Lichtman 的 \(0.3389\) 更新不能倒写进 cohort 的当时状态。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试重建 AGP 型 Korselt—零和构造。选取整数 \(L\)，收集许多形如 \(p=d+1\) 的素数，其中 \(d\mid L\)。在有限群 \((\mathbb Z/L\mathbb Z)^\times\) 中，从这些素数中寻找乘积同余1的子集；对子集 \(S\) 令 \(n=\prod_{p\in S}p\)。随后通过控制子集大小和素数尺寸来计数不同的 \(n\le x\)。
- 局部结论：若各 \(p\in S\) 互异、\(p-1\mid L\)，且 \(n=\prod_{p\in S}p\equiv1\pmod L\)，则 \(n\) 平方自由且对每个 \(p\mid n\) 有 \(p-1\mid n-1\)；只要 \(|S|\ge2\)，Korselt 判据严格推出 \(n\) 是 Carmichael 数。；因此解析数论部分与组合部分可以分离：前者制造大量 \(L\)-控制的移位素数，后者只需在有限阿贝尔群中制造大量乘积为单位元的子集。；Pomerance 预测式中的损失指数为 \(\log\log\log x/\log\log x=o(1)\)，故该更精确启发式确实蕴含 \(C(x)=x^{1-o(1)}\)，但不构成证明。
- 第一阻塞点：要达到指数 \(1-o(1)\)，必须在可选的除数 \(d\mid L\) 中证明数量近乎最优的 \(d+1\) 为素数，并保证零和子集产生近乎 \(x\) 次幂数量的不同且不超界乘积。现有关于大模数算术级数及光滑移位素数的分布不足；这是路线中第一处真正的解析障碍。
- 下一步：把目标参数化：给定 \(y\)，取由小素数组成的 \(L\)，明确计算需要多少个 \(d\mid L\) 满足 \(d+1\) 为素数，才能经有限群零和引理得到 \(x^{1-\varepsilon}\) 个乘积；随后将所需素数计数强度与 Bombieri–Vinogradov/Lichtman 型可用模数范围逐项比较。
- 来源核对：[Erdős Problems #1057](https://www.erdosproblems.com/1057)确认问题开放、Korselt 判据及已知下界路线。；[AGP 原论文页面](https://annals.math.princeton.edu/1994/193-3/p06)确认1994年无穷性论文及书目信息。；[Lichtman 预印本](https://arxiv.org/abs/2211.09641)确实声明由光滑移位素数改进 Carmichael 数下界，但属于冻结日期之后应单列的进展。；数值 \(0.33336704\) 可由 \(0.7039\cdot0.4736\) 直接复算；候选的 \(0.3336704\) 是数字次序错误。
- 时间记账：所在批次墙钟时间按题数均摊约 65.2 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1057)；既有候选答案（按不可信材料审计）

### #1059

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many primes $p$ such that $p-k!$ is composite for each $k$ such that $1\leq k!<p$?
- 题意摘要：求证是否存在无穷多个素数 p，使得对每个满足 1≤k!<p 的整数 k，正整数 p-k! 都是合数。这里需要同时处理随 p 无界增长的全部 k，而非预先固定有限多个阶乘。
- 状态核对：截至 2026-07 官方页面仍标为 open。旧候选中的“固定 m”论证有效，但不能推出原命题。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先固定 m，为每个 1≤k≤m 选取互异素数 q_k>m，并由 CRT 取 a≡k! (mod q_k)，Q=∏q_k。因 q_k∤k!，有 gcd(a,Q)=1；Dirichlet 定理给出无穷多个素数 p≡a (mod Q)。充分大的此类 p 满足 q_k∣p-k! 且 p-k!>q_k，故前 m 个差均为合数。再尝试令 m 随 p 增长并要求 m!<p≤(m+1)!。
- 局部结论：对每个固定 m，确有无穷多个素数 p，使 p-k! 对全部 1≤k≤m 均为合数。；CRT 类是 Dirichlet 可用的既约剩余类，因为每个 q_k>m≥k，故 q_k∤k!。；若坚持每个条件使用互异 q_k>m，则 Q>m^m，而 (m+1)!约为 exp(m log m-m)，模数已大于目标阶乘区间的尺度，Dirichlet 的无穷性不给出该区间内的素数。
- 第一阻塞点：第一处缺口是无法把固定 m 的算术级数结果统一化为 m=m(p)：现有方法既不能保证该剩余类在 (m!,(m+1)!] 中含素数，也不能用足够少的模数同时覆盖所有阶乘差。
- 下一步：检验“复用小素因子”的覆盖问题：对给定 m，寻找尽量小的 Q 和既约类 a，使每个 k≤m 都有某个 q∣Q 满足 a≡k! (mod q)，并计算最小 log Q 是否能降到 log(m!)-Ω(m)。
- 来源核对：[官方题页：仍标为 OPEN，并列出 101、211](https://www.erdosproblems.com/1059)
- 时间记账：所在批次墙钟时间按题数均摊约 39.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1059)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1059.lean`；既有候选答案（按不可信材料审计）

### #1060

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ count the number of solutions to $k\sigma(k)=n$, where $\sigma(k)$ is the sum of divisors of $k$. Is it true that $f(n)\leq n^{o(\frac{1}{\log\log n})}$? Perhaps even $\leq (\log n)^{O(1)}$?
- 题意摘要：令 f(n)=#{k∈N:kσ(k)=n}。问题问当 n→∞ 时是否 log f(n)=o(log n/loglog n)，甚至是否存在绝对常数 C 使 f(n)≤(log n)^C。
- 状态核对：截至 2026-07 官方页面仍标为 open。旧候选给出的除数函数上界正确，但只到 O(1/loglog n) 指数。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：把每个解 k 注入 n 的因子集合：kσ(k)=n 立即给出 k∣n。进一步利用 σ(k)≥k+1（k>1），将候选限制到 k<√n，再尝试从素因子指数结构获得比 τ(n) 更强的纤维界。
- 局部结论：严格有 f(n)≤τ(n)。经典最大阶估计遂给出 f(n)≤exp((log 2+o(1))log n/loglog n)。；除 k=1 的平凡情形外，n=kσ(k)≥k(k+1)，所以所有解均满足 k<√n。；给定 k∣n 后，方程等价于 σ(k)=n/k；因此问题是 σ 在 n 的因子格上的单值水平集大小，而非任意因子计数。
- 第一阻塞点：第一处缺口是尚无统一机制证明同一 n 的大量因子不能同时满足 σ(k)=n/k；限制 k<√n 至多约减半 τ(n)，不改变其最大阶指数。
- 下一步：对高度合成型 n=∏p_i^{a_i} 做可复现实验：枚举其全部因子 k，按 kσ(k) 分纤维，比较最大纤维与 τ(n)，并检查碰撞是否必须包含可识别的素数幂交换结构。
- 来源核对：[官方题页：OPEN，题意及 Guy B11](https://www.erdosproblems.com/1060)
- 时间记账：所在批次墙钟时间按题数均摊约 39.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1060)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1060.lean`；既有候选答案（按不可信材料审计）

### #1061

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：How many solutions are there to\[\sigma(a)+\sigma(b)=\sigma(a+b)\]with $a+b\leq x$, where $\sigma$ is the sum of divisors function? Is it $\sim cx$ for some constant $c>0$?
- 题意摘要：令 N(x) 计数正整数对 (a,b) 满足 a+b≤x 且 σ(a)+σ(b)=σ(a+b)。题目问其增长阶，特别是否 N(x)∼cx。若把解视为无序对，常数应相应减半。
- 状态核对：官方页面截至 2026-07 仍标为 open。论坛出现 arXiv:2606.25849 的“已解决”声明，但页面明确未验证，故不能据此改判。旧候选的线性族有效；其余增长断言只是启发式。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：取 (a,b)=(n,2n)，并限制 gcd(n,6)=1。乘法性给出 σ(2n)=3σ(n)、σ(3n)=4σ(n)，所以 σ(n)+σ(2n)=σ(3n)。随后尝试由不同本原解缩放，累加出渐近式。
- 局部结论：每个 gcd(n,6)=1 的 n 都给出解 (n,2n)，交换坐标又给出 (2n,n)。；因此按有序对计数，N(x)≥2·#{n≤x/3:(n,6)=1}=2x/9+O(1)；按无序对则为 x/9+O(1)。；更一般地，若 (u,v) 是解且 gcd(d,uv(u+v))=1，则 (du,dv) 仍是解，因为三个 σ 值都同乘 σ(d)。
- 第一阻塞点：第一处缺口是不同本原解的缩放族会重叠，而且没有得到本原解的可控计数或尾部上界；因此既不能推出 cx 渐近，也不能严格推出 xlog x。
- 下一步：以 gcd(a,b)=1 定义本原解，计算其计数 P(y)，并验证恒等式型分解 N(x)=∑_d P_d(x/d) 中互素限制的准确形式；首要测试是 P(y) 是否线性及缩放族重叠是否唯一。
- 来源核对：[官方题页：目前仍为 OPEN](https://www.erdosproblems.com/1061)；[论坛：未验证的 2026 解决声明及谨慎说明](https://www.erdosproblems.com/forum/thread/1061)
- 时间记账：所在批次墙钟时间按题数均摊约 39.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1061)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1061.lean`；既有候选答案（按不可信材料审计）

### #1062

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the size of the largest subset $A\subseteq \{1,\ldots,n\}$ such that there are no three distinct elements $a,b,c\in A$ such that $a\mid b$ and $a\mid c$. How large can $f(n)$ be? Is $\lim f(n)/n$ irrational?
- 题意摘要：f(n) 是 A⊆{1,…,n} 的最大大小，要求不存在三个互异 a,b,c∈A 使 a∣b 且 a∣c；等价地，每个选中的 a 至多整除 A 中一个严格大于它的元素。问题还询问 lim f(n)/n 及其无理性。
- 状态核对：官方仍标为 open，并记录 Lebensold 的 0.6725n≤f(n)≤0.6736n。2026 年论坛有“极限存在且可计算”的未正式核验稿，但无理性仍未处理；旧候选把极限存在也直接称为未知，已不是完整的最新材料。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `medium`
- 尝试路线：把问题写成有向整除图上的诱导子图约束：所选顶点的严格向外度至多 1。先取顶端区间 A={⌊n/3⌋+1,…,n}，再尝试由 f(n+m) 的拼接建立极限。
- 局部结论：该区间大小为 n-⌊n/3⌋=⌈2n/3⌉。；若 a>n/3，则 ≤n 的严格倍数至多只有 2a，故此区间满足限制，严格得到 f(n)≥⌈2n/3⌉。；单点扩张给出 f(n)≤f(n+1)≤f(n)+1，但这不足以保证 f(n)/n 收敛。
- 第一阻塞点：拼接最先失败于跨区间整除边：两个分别最优的集合平移或并置后，小区间元素可能整除多个新区间元素，因而得不到所需的次可加/次可乘关系。即使先证明极限存在，也没有路线证明该常数无理。
- 下一步：独立审核论坛稿所用 McNew 局部整除图统计定理：明确截断参数、边界顶点比例及误差交换次序，先验证其是否真的推出 f(n)=cn+o(n)，再单独研究 c 的算术性质。
- 来源核对：[官方题页：OPEN 及 Lebensold 界](https://www.erdosproblems.com/1062)；[论坛：极限存在的未核验部分结果及官方谨慎回应](https://www.erdosproblems.com/forum/thread/1062)
- 时间记账：所在批次墙钟时间按题数均摊约 39.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1062)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1062.lean`；既有候选答案（按不可信材料审计）

### #1063

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $k\geq 2$ and define $n_k\geq 2k$ to be the least value of $n$ such that $n-i$ divides $\binom{n}{k}$ for all but one $0\leq i<k$. Estimate $n_k$.
- 题意摘要：对每个 k≥2，n_k 是最小的 n≥2k，使 k 个数 n,n-1,…,n-k+1 中恰有一个不整除 C(n,k)，其余 k-1 个均整除；目标是估计 n_k 随 k 的增长。
- 状态核对：截至 2026-07 仍为 open。人工评审指出旧候选错误地断言 p²>k 时 v_p(C(n,k))∈{0,1}；这确实错误，因为分子区间可含任意高次 p 幂。因此其常数 C 和次指数渐近结论全部撤销。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `medium`
- 尝试路线：改走确定性的 p-adic 路线。上界取 n=kL，L=lcm(2,…,k-1)，逐素数比较 C(n,k) 与 n-i 的赋值；下界则设唯一失败项 d_e=n-e，对每个 p^a∥k 比较 k 个连续整数在各 p-adic 层级上的计数。
- 局部结论：严格上界：n_k≤k·lcm(2,…,k-1)=exp((1+o(1))k)。事实上对 n=kL、1≤i<k，可逐层验证 v_p(C(n,k))≥v_p(n-i)=v_p(i)，故 n-i∣C(n,k)；已知至少一项失败，唯一失败项只能是 n。；可推出下界 n_k≥max(2k,∏_{p^a∥k}p^{a+⌊log_p(k/2)⌋})。令 M=max_i v_p(n-i)、S=v_p(C(n,k))；因 p,…,p^a 各层在长度 k 的分子块与 k! 中恰好抵消，而更高每层净贡献至多 1，故 S≤M-a。；由于 p^t≤k/2（t=⌊log_p(k/2)⌋），区间内至少两个数被 p^t 整除；至少一个不是失败项，所以 S≥t，进而 M≥a+t。最大赋值项必须是唯一失败项 d_e，故上述各素数幂同时整除 d_e≤n_k。
- 第一阻塞点：这些确定性上下界之间仍有巨大空隙：下界强烈依赖 k 的因子结构，通常远低于 exp(ck)，而上界约 exp(k)。没有论证能把唯一失败条件转化为统一的指数级下界或更小上界。
- 下一步：先形式化并逐例验证下界中的关键引理 S≤M-v_p(k)，尤其覆盖 p^r≤k 且 r>v_p(k) 时区间可有两个 p^r 倍数的情形；随后计算 k≤100 的下界比值 log n_k/k，寻找应按 k 的素因子结构分层表述的估计。
- 来源核对：[官方题页：OPEN、已知小值及 LCM 上界](https://www.erdosproblems.com/1063)；[论坛：2026 年提出的 p-adic 下界；本文已独立复核其层级计数](https://www.erdosproblems.com/forum/thread/1063)
- 时间记账：所在批次墙钟时间按题数均摊约 39.7 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1063)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1063.lean`；既有候选答案（按不可信材料审计）

### #1065

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Are there infinitely many primes $p$ such that $p=2^kq+1$ for some prime $q$ and $k\geq 0$? Or $p=2^k3^lq+1$?
- 题意摘要：第一问量化为：集合 \(\{p\in\mathbb N:p\text{ prime},\ \exists q,k\in\mathbb N,\,q\text{ prime},\ p=2^kq+1\}\) 是否无限。第二问把等式改为 \(p=2^k3^\ell q+1\)，其中 \(k,\ell\ge0\)。参数不要求固定。
- 状态核对：官方页面截至近期仍标为 open。旧候选正确指出与 Sophie Germain 素数有关，但“每个固定 \((k,\ell)\) 都应有无穷多解”漏掉了 \(k=0\) 的奇偶障碍。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `2/10`；置信度 `high`
- 尝试路线：固定乘子 \(A=2^k3^\ell\)，把问题化为同时要求两个线性式 \(q\) 与 \(Aq+1\) 为素数，并检查能否用二维筛法得到下界。
- 局部结论：若 \(k=0\)，则除 \(q=2\) 外 \(q\) 为奇数，\(3^\ell q+1\) 为大于 2 的偶数；故该层至多给出 \(p=3^\ell\cdot2+1\) 为素数的零散解。特别地第一问的 \(k=0\) 只有 \((p,q)=(3,2)\)。；对每个固定 \(k\ge1,\ell\ge0\)，线性式组 \(n,\ 2^k3^\ell n+1\) 是 admissible：模 2 取 \(n\equiv1\)，模任意奇素数至多排除两个剩余类。因而没有局部同余障碍。；第二族包含第一族（取 \(\ell=0\)）；所以第一问若为是，则第二问必为是，但反向并不显然。
- 第一阻塞点：二维奇偶筛只能有效控制乘积或给出上界，不能证明 \(q\) 与 \(Aq+1\) 同时为素数；即使固定 \(k=1,\ell=0\)，这已经是未解决的 Sophie Germain 素数问题。允许 \(k\) 变化尚未产生可求和的正下界。
- 下一步：对截断范围 \(k\le K(x)\) 建立带常数的一致上、下界筛模型，检验不同 \(k\) 的候选集合重叠是否可能让“可变 \(k\)”避开固定乘子的 parity barrier；首个可核验目标是证明相应筛余项对 \(k\le c\log x\) 一致。
- 来源核对：[Erdős Problems #1065](https://www.erdosproblems.com/1065) 仍标为 OPEN。；本地 Lean 文件准确量化了 \(p,q,k,\ell\in\mathbb N\)，两个定理均仍含 `sorry`，未提供证明。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1065)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1065.lean`；既有候选答案（按不可信材料审计）

### #1066

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a graph given by $n$ points in $\mathbb{R}^2$, where any two distinct points are at least distance $1$ apart, and we draw an edge between two points if they are distance $1$ apart. Let $g(n)$ be maximal such that any such graph always has an independent set on at least $g(n)$ vertices. Estimate $g(n)$, or perhaps $\lim \frac{g(n)}{n}$.
- 题意摘要：对每个满足点间距至少 1 的 \(n\) 点集 \(P\subset\mathbb R^2\)，以恰好相距 1 的点对为边；\(g(n)=\min_P\alpha(G(P))\)。问题要求估计 \(g(n)\)，尤其询问 \(g(n)/n\) 的极限。
- 状态核对：仍为 open；官方记录界为 \(8n/31\le g(n)\le5n/16\)，整数取整需另行处理。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：先从几何嵌入证明平面性，再用着色得到可独立复核的线性下界；同时用远距离并置证明极限存在。
- 局部结论：两条单位边若在内部横截，取交点到两条边上最近的端点；相应两段长度之和不超过 1，且非退化横截时两端点距离严格小于 1，违背最小点距。因此直线嵌入无交叉，\(G(P)\) 平面。；由四色定理，\(\alpha(G(P))\ge\lceil n/4\rceil\)，故 \(g(n)\ge\lceil n/4\rceil\)。这只重建基础界，未达到 \(8/31\)。；把分别实现 \(g(n),g(m)\) 的配置放得足够远，可得 \(g(n+m)\le g(n)+g(m)\)。由 Fekete 引理，\(\lim_{n\to\infty}g(n)/n=\inf_n g(n)/n\) 存在。
- 第一阻塞点：要超过 \(n/4\)，仅靠平面性和四色分割不够；必须利用硬币接触图的局部几何。尝试按度数放电时，尚不能严格推出足够多低度顶点或一个使独立集达到 \(8n/31\) 的可闭合递推。
- 下一步：重建 Swanepoel 的 \(8/31\) 放电不等式：逐类列出度 \(3,4,5,6\) 顶点及三角面约束，并逐项验证总电荷恒等式和每条局部转移规则。
- 来源核对：[Erdős Problems #1066](https://www.erdosproblems.com/1066) 给出当前记录 \(8/31\) 与 \(5/16\)，并仍标为 OPEN。；旧候选关于次可加性及极限存在的论证成立；但“总能找到度至多 3 的顶点”需要硬币图专门引理，不能只由一般平面性推出。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1066)；既有候选答案（按不可信材料审计）

### #1068

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Does every graph with chromatic number $\aleph_1$ contain a countable subgraph which is infinitely connected?
- 题意摘要：对任意顶点类型 \(V\) 和简单图 \(G\)，若 \(\chi(G)=\aleph_1\)，是否存在可数顶点集 \(S\subseteq V\)，使诱导图 \(G[S]\) 中任意两顶点间都有无穷多条两两内部顶点不交的路径。
- 状态核对：仍为 open。这里是顶点不交路径；已知排除“不一定存在不可数的无限连通子图”的反例并未处理所问的可数子图。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：先抽取一个可数、染色数无限的子图，再尝试用有限分离集递归分解其高色数部分，逼出无限顶点连通块。
- 局部结论：由紧致性：若所有有限子图的染色数有统一有限上界 \(r\)，则整个图可 \(r\)-染色。因此 \(\chi(G)=\aleph_1\) 蕴含对每个 \(r<\omega\) 存在有限子图 \(H_r\) 满足 \(\chi(H_r)>r\)。；令 \(H=\bigcup_rH_r\)，则 \(H\) 是可数子图且 \(\chi(H)=\aleph_0\)。所以至少总能抽取可数的无限色数子图。；对可数图中的两点，若不存在无穷多条内部顶点不交路径，则无限版 Menger 定理给出一个有限顶点分离集；故目标可改写为寻找一个可数子图，其中删除任意有限顶点集后仍保持任意两点连通。
- 第一阻塞点：把 \(H\) 沿有限分离集递归拆分时，高染色数可以分散在可数多个有限色块中；“整体为无限色数”不能保证某一个后继块仍为无限色数。例如不交并 \(\bigsqcup_nK_n\) 已显示这一直接归纳原则失败。
- 下一步：检验能否加强可数抽取，使所得 \(H\) 具有“删除任意有限集合后仍为无限色数”的临界性；具体先证明或反驳：每个染色数 \(\aleph_0\) 的可数图都含这样的诱导子图。若反例存在，再识别 \(\aleph_1\) 母图能否排除它。
- 来源核对：[Erdős Problems #1068](https://www.erdosproblems.com/1068) 截至 2026 年仍标为 OPEN，并明确采用无限顶点连通定义。；[Bowler–Pitz](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i1p23) 只构造了无不可数无限连通子图的不可数色图，没有否定可数版本。；本地 Lean 陈述与上述全称量词一致，但定理仍含 `sorry`。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1068)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1068.lean`；既有候选答案（按不可信材料审计）

### #1070

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be maximal such that, given any $n$ points in $\mathbb{R}^2$, there exist $f(n)$ points such that no two are distance $1$ apart. Estimate $f(n)$. In particular, is it true that $f(n)\geq n/4$?
- 题意摘要：对任意 \(n\) 点集 \(P\subset\mathbb R^2\)，令单位距离图以距离恰为 1 的点对为边；\(f(n)=\min_{|P|=n}\alpha(G(P))\)。原问题特别问是否对所有 \(n\) 都有 \(f(n)\ge n/4\)。
- 状态核对：冻结输入标为 open，但此后出现重要进展：2026-06-26 的 Dúcz–Varga 预印本声称构造有限单位距离图满足 \(\alpha(G)/|V(G)|<1/4\)，从而否定特别问题。总的渐近估计仍开放；该结果目前是新预印本。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `8/10`；置信度 `medium`
- 尝试路线：重建“有限低独立比图即为反例”的归约，并核查新论文从 29 点几何分数着色证书经两次 blow-up 得到有限图的路线。
- 局部结论：同 1066，远距离并置给出 \(f(n+m)\le f(n)+f(m)\)，故 \(\lim f(n)/n=\inf f(n)/n\) 存在。；Moser spindle 有 7 个顶点且 \(\alpha=2\)，故 \(f(7t)\le2t\)。旧候选给出的 \(2/7\) 上界路线正确，但已不是最新渐近信息。；若新预印本的有限图 \(G\) 有 \(N\) 个顶点且 \(\alpha(G)<N/4\)，则直接有 \(f(N)\le\alpha(G)<N/4\)；并置复制还给出 \(\lim f(n)/n\le\alpha(G)/N<1/4\)。
- 第一阻塞点：论文的关键严格步骤是：29 点图的巨大几何分数着色线性规划具有一个有理对偶证书，且 amenability 与离散立方 blow-up 确实产生有限单位距离图并保持所需独立比。正文给出归约并引用补充证书，但本次筛查没有逐条机器核验约 49 万个约束，因此只能把它记为有明确证书的新反例路线，而非在此独立重证。
- 下一步：下载作者补充材料，写独立校验器：精确有理数验证 GFCN 对偶向量的全部约束，再逐条核对两次 blow-up 定理的参数选择确实给出严格 \(<1/4\)。
- 来源核对：[Dúcz–Varga 预印本](https://arxiv.org/abs/2606.28157) 的 Theorem 1 明确声称存在 \(\alpha(G)/|V(G)|<1/4\) 的有限平面单位距离图。；[Erdős Problems #1070](https://www.erdosproblems.com/1070) 主页面已收录此前的 \((1/4+o(1))n\) 上界；讨论区记录了 2026 年的新反例声称，但页面状态尚未完全更新。；旧候选遗漏了 \(f(n)\le(1/4+o(1))n\) 及此后的严格反例，故其“\(n/4\) 仍开放”已过时。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1070)；既有候选答案（按不可信材料审计）

### #1071

- 当前状态：`proved (Lean)`（冻结清单状态：`open`）
- 精确题面：Are there a finite set of unit line segments in the unit square, no two of which intersect, which are maximal with respect to this property? Is there a region $R$ with a maximal set of disjoint unit line segments that is countably infinite?
- 题意摘要：第一问要求单位正方形中存在一个有限的、两两“不相交”的单位线段族，且不能再加入任何允许的单位线段。第二问要求某个区域 \(R\) 中存在可数无穷的极大族。这里“线段”究竟取开线段还是闭线段、端点相交是否允许，是结论的关键组成部分。
- 状态核对：官方状态为 proved (Lean)，两问均记为肯定。但本地陈述、官方自然语言及所链接 Lean 工件之间存在显著语义错位，必须分别核对，不能接受旧候选。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `6/10`；置信度 `high`
- 尝试路线：先审查旧候选的平移反证，再把极大性改写为 blocking 性质，并比对 Danzer/后续构造与 Lean 中采用的线段定义。
- 局部结论：旧候选的核心步骤“有限个两两不交线段为紧集，故相互距离正”只对闭且严格不交的线段成立。官方及外部 Lean 构造使用开线段 \((0,1)\)；两个不交开线段可以距离为 0，故不能选统一的正 \(\delta\)。旧候选据此回答第一问“否”是错误的。；对开线段族 \(S\)，极大性等价于：每条位于区域中的允许单位开线段都与某个 \(s\in S\) 相交。外部 Lean 工件把这个 blocking 等价命题形式化，并构造了由两个递归序列及一条极限线段组成的可数族。；旧候选的圆盘构造不能证明第二问：其开圆盘直径为 1，却不包含端点距离恰为 1 的线段；写出的直径端点也不在圆盘中。此外该 \(R\) 不连通，而本地 Lean 陈述要求 `IsOpen R ∧ IsConnected R`。
- 第一阻塞点：无法把当前链接工件直接认作本地两条定理的完整证明：本地第一问用闭 `segment` 并允许交点仅落在端点集合，且文件本身仍为 `sorry`；链接的 `Erdos1071.lean` 实际证明的是单位正方形中“可数”个开线段的极大族，不是显示的有限 `Finset` 定理。第二问本地又只要求端点属于 \(R\)，没有要求整段包含于 \(R\)。因此已知几何结论可信，但“该本地形式化精确验证了所列陈述”尚未由所给工件闭合。
- 下一步：做一次定理—工件审计：为两问固定开/闭线段与端点接触约定；把 Danzer 的有限 blocking 构造坐标化；随后检查外部 Lean 最终 theorem 的类型是否逐字蕴含本地 `erdos_1071.parts.i/ii`，不一致则修正本地陈述或证明链接。
- 来源核对：[Erdős Problems #1071](https://www.erdosproblems.com/1071) 明确记载第一问由 Danzer 肯定解决，并记录单位正方形中的可数极大构造。；[链接的 Lean 工件](https://raw.githubusercontent.com/plby/lean-proofs/main/src/v4.24.0/ErdosProblems/Erdos1071.lean) 定义 `IsUnitSegment` 为 `openSegment`，文件头称证明了单位正方形中的可数极大族。；本地 `1071.lean` 两个 theorem 仍以 `by sorry` 结束；其 `SegmentsDisjoint` 和区域包含条件也与外部工件不同。故“proved (Lean)”的元数据不能替代逐类型核对。
- 时间记账：所在批次墙钟时间按题数均摊约 61.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1071)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1071.lean`；既有候选答案（按不可信材料审计）

### #1072

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For any prime $p$, let $f(p)$ be the least integer such that $f(p)!+1\equiv 0\pmod{p}$. Is it true that there are infinitely many $p$ for which $f(p)=p-1$? Is it true that $f(p)/p\to 0$ for almost all $p$?
- 题意摘要：对每个素数 p，令 f(p)=min{n≥0:p∣n!+1}。问：(i) 满足 f(p)=p−1 的素数是否无限；(ii) 是否存在相对素数集密度为 1 的集合 P，使沿 p∈P、p→∞ 有 f(p)/p→0。
- 状态核对：截至核查时官方仍列为 open。先前候选的 Poisson 模型只是启发式；关于“所有余数的平均分布”的猜想不能推出固定余数 −1 随 p 变化的密度。其“约 1/e 正密度”还与 Erdős–Hardy–Subbarao 猜测该集合为 o(π(x)) 明显不同，二者均未获证明。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：用 Wilson 定理把早期命中 −1 转换为另一端的阶乘符号条件，再尝试对素数平均命中数。对奇素数 p，若 1≤n≤p−2，置 k=p−1−n，则由 n!·∏_{j=n+1}^{p-1}j≡−1 得到 n!≡−1 当且仅当 k!≡(−1)^k。因而问题可改写为控制随 p 变化的短阶乘同余。
- 局部结论：Wilson 定理严格给出 f(p)≤p−1；形式化定义允许 n=0，故 f(2)=0，而奇素数不受此端点影响。；对奇素数 p，f(p)=p−1 等价于不存在 1≤k≤p−2 使 k!≡(−1)^k (mod p)。；两个相邻指标 n,n+1≤p−2 不可能同时满足 n!≡(n+1)!≡−1 (mod p)，否则 n+1≡1 (mod p)，矛盾。
- 第一阻塞点：要处理第二问，必须证明对除 o(π(x)) 个素数外，区间 n≤εp 内至少有一次命中；上述对称关系和“不相邻”性质不给出任何命中的存在性。反向计算 p∣n!+1 又需控制巨大且高度相关的阶乘数的素因子，第一矩或 Poisson 猜测不足以闭合。
- 下一步：固定 ε>0，研究 X_p(ε)=#{n≤εp:p∣n!+1}：先求可证明的素数平均一阶矩与二阶矩；若能得到 ΣX_p≫π(x) 且 ΣX_p²=O(π(x))，即可检验正比例命中，但要推出“几乎全部”还需更强的零值估计。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1072)仍标为 OPEN，并记载 Erdős–Hardy–Subbarao 的 o(x/log x) 猜测。；核对了本地 Lean 陈述：f 以自然数下确界定义，“almost all”明确形式化为相对素数密度 1 的子集上的极限。
- 时间记账：所在批次墙钟时间按题数均摊约 70.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1072)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1072.lean`；既有候选答案（按不可信材料审计）

### #1073

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A(x)$ count the number of composite $u<x$ such that $n!+1\equiv 0\pmod{u}$ for some $n$. Is it true that $A(x)\leq x^{o(1)}$?
- 题意摘要：A(x) 计数所有 u<x，要求 u 为合数且存在某个自然数 n 使 u∣n!+1。问题是是否对每个 δ>0 最终都有 A(x)≤x^δ，即 A(x)=x^{o(1)}。
- 状态核对：官方仍列为 open，且未登记部分解。先前候选的两个初等观察正确，但尚未形成计数路线。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `8/10`；置信度 `high`
- 尝试路线：按见证 n 的大小分割。令 P⁻(u) 为 u 的最小素因子，并取参数 y。若见证 n<y，则 u 是某个 n!+1 的因子；若 n≥y，则 u 是 y-rough 合数。于是尝试以除数估计处理前段、筛法处理后段。
- 局部结论：若 u∣n!+1，则 gcd(u,n!)=1，故每个素因子 q∣u 都满足 q>n，即 n<P⁻(u)。；因 u 为合数，u≥P⁻(u)^2>(n)^2；特别地，任何 u<x 的见证必有 n<√x。；对任意 y，有 A(x)≤Σ_{n<y}τ(n!+1)+#{u<x:u 为合数且 P⁻(u)>y}。这是严格的覆盖上界，虽会重复计数。
- 第一阻塞点：标准筛法对第二项至多给出约 x/log y 的量级；而利用一般最大除数函数估计，第一项随 y 增长过快。不存在一个 y 能由这两个无结构上界推出 x^{o(1)}。缺失的是同余 u∣n!+1 对 y-rough 数的额外强排斥，而非普通粗糙数计数。
- 下一步：对固定 u 研究不同见证 n 的相容性：由 m!≡n!≡−1 (mod u) 推出 ∏_{j=n+1}^{m}j≡1 (mod u)。下一步可检验能否对给定 y-rough u 将可能的 n<√u 限制为 u^{o(1)} 个，并结合大筛控制至少一个见证的 u。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1073)仍标为 OPEN，且注明没有已登记的部分或完整解。；本地 Lean 文件确认 n 是无额外上界的自然数存在量词，u 同时要求 Composite 与 u<x。
- 时间记账：所在批次墙钟时间按题数均摊约 70.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1073)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1073.lean`；既有候选答案（按不可信材料审计）

### #1074

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $S$ be the set of all $m\geq 1$ such that there exists a prime $p\not\equiv 1\pmod{m}$ such that $m!+1\equiv 0\pmod{p}$. Does\[\lim \frac{\lvert S\cap [1,x]\rvert}{x}\]exist? What is it? Similarly, if $P$ is the set of all primes $p$ such that there exists an $m$ with $p\not\equiv 1\pmod{m}$ such that $m!+1\equiv 0\pmod{p}$, then does\[\lim \frac{\lvert P\cap [1,x]\rvert}{\pi(x)}\]exist? What is it?
- 题意摘要：S 包含所有 m≥1，使 m!+1 有某个素因子 p 不满足 p≡1 (mod m)；问 S 的自然密度是否存在及其值。P 包含所有素数 p，使对某个 m≥1 有 p∣m!+1 且 p≢1 (mod m)；问 P 在素数中的相对密度是否存在及其值。
- 状态核对：两个密度问题仍 open；已知的是 S、P 均无限。先前候选用“8∈S”声称 S 无限是逻辑错误，一个例子只能证明非空；无限性须使用 Erdős–Hardy–Subbarao 的论证。其把各素因子模 m 独立均匀处理也忽略了乘积 m!+1≡1 (mod m) 带来的强条件。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `9/10`；置信度 `high`
- 尝试路线：从补集入手。若 m∉S，则 m!+1 的每个素因子均为 1 mod m；展开这些因子在模 m² 下的乘积，尝试得到补集元素必须满足的附加同余。对 P 则把 Wilson 的平凡解与真正见证分开。
- 局部结论：任意 p∣m!+1 都有 p>m。因此 m∉S 当且仅当 m!+1 的每个素因子都满足 p≡1 (mod m)；特别地，若 m!+1 本身为素数，则 m∉S。；对合数 m≥6，有 m²∣m!。若 m∉S，写 m!+1=∏p_i^{e_i}、p_i=1+ma_i，则模 m² 展开得到 Σe_i a_i≡0 (mod m)。这是补集分解必须满足的非平凡约束。；对素数 p，任何见证 m 都满足 m<p；且 p∈P 当且仅当存在 m<p，m!≡−1 (mod p) 且 m∤p−1。Wilson 解 m=p−1 总被条件排除。
- 第一阻塞点：上述模 m² 条件只约束某一个随 m 急剧增长的整数 m!+1 的未知素因子；Dirichlet 定理或固定模数的素数等分布不能用于证明这种分解模式在 m 上稀少。对 P，同样缺少控制固定目标 −1 在阶乘轨道中命中的跨素数统计。
- 下一步：先处理可检验的低复杂度补集：假设 m!+1 只有一个或两个不同素因子，用 Σe_i a_i≡0 (mod m) 联合大小条件 p_i>m 分类；目标是证明这类例外的计数为 o(x)，再判断该约束能否推广到有界 Ω(m!+1) 的情形。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1074)确认两个密度问题仍 OPEN，并明确记载 S、P 均已知无限。；本地 Lean 陈述确认 S 要求 m≥1；P 的见证也明确要求 m≥1，并分别形式化自然密度与相对素数密度。
- 时间记账：所在批次墙钟时间按题数均摊约 70.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1074)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1074.lean`；既有候选答案（按不可信材料审计）

### #1075

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 3$. There exists $c_r>r^{-r}$ such that, for any $\epsilon>0$, if $n$ is sufficiently large, the following holds. Any $r$-uniform hypergraph on $n$ vertices with at least $(1+\epsilon)(n/r)^r$ many edges contains a subgraph on $m$ vertices with at least $c_rm^r$ edges, where $m=m(n)\to \infty$ as $n\to \infty$.
- 题意摘要：固定 r≥3，要求存在仅依赖 r 的 c_r>r^{-r}，使对每个 ε>0，充分大的 n 上，任何 e(G)≥(1+ε)(n/r)^r 的 r-一致超图都含一个顶点数 m=m(n)→∞ 的子图 H，满足 e(H)≥c_rm^r。关键量词是 c_r 不得依赖 ε。
- 状态核对：官方仍列为 open。候选将其联系到边界 jump 问题在归一化上基本合理，但“完全等同”还需用抽样与对角化核对 m→∞ 的量词，不能仅凭术语视为已解决。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：尝试随机抽取 m 个顶点实现局部增密。若 S 是均匀随机 m-子集，则 E[e(G[S])]=e(G)(m)_r/(n)_r。再用平衡完全 r-部图检查阈值是否可能提高。
- 局部结论：随机抽样严格保证存在 m-顶点诱导子图满足 e(G[S])≥(1+ε)r^{-r}m^r(1−O_r(1/m+1/n))。因此若允许常数依赖 ε，可立即取得增量。；平衡完全 r-部图有约 (n/r)^r 条边；其任意 m 顶点诱导子图的边数至多 ∏_{i=1}^r m_i≤(m/r)^r，故 r^{-r} 是真实的结构性边界。；在标准密度 e/\binom{v}{r} 下，边界对应 α=r!/r^r；若原命题成立，再对所得 m→∞ 子图抽取足够大的固定 t，可得到密度严格大于 α 的 t-顶点子图。
- 第一阻塞点：抽样所得增量是 εr^{-r}，当 ε→0 时消失；没有步骤把任意微小的全局超额放大为仅依赖 r 的固定间隙 c_r−r^{-r}>0。平衡 r-部例子还表明这种放大必须利用“超过阈值”的边的特殊聚集，而平均度本身看不见该聚集。
- 下一步：建立并检验一个稳定性二分引理：若 G 不接近平衡完全 r-部结构，则直接找到固定密度增量；若接近，则证明超过 (n/r)^r 的边必在某个 m→∞ 的顶点块中产生固定增量。先在 r=3、假设存在给定三分划且仅加入非横截边的模型中验证。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1075)仍标为 OPEN，并只记录 Erdős 在较强全局密度假设下取得 c_r=r^{-r}。
- 时间记账：所在批次墙钟时间按题数均摊约 70.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1075)；既有候选答案（按不可信材料审计）

### #1083

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $d\geq 3$, and let $f_d(n)$ be the minimal $m$ such that every set of $n$ points in $\mathbb{R}^d$ determines at least $m$ distinct distances. Estimate $f_d(n)$ - in particular, is it true that\[f_d(n)=n^{\frac{2}{d}-o(1)}?\]
- 题意摘要：固定 d≥3，f_d(n) 是所有 n 点集合所确定的非零两点距离数的最小值。问其渐近量级，特别是对每个固定 d 是否有 log f_d(n)/log n→2/d，即 f_d(n)=n^{2/d-o(1)}。
- 状态核对：官方仍列为 open，并记录 f_3(n)≫n^{3/5}、d≥4 时 f_d(n)≫_d n^{2/d-c/d²}。候选把目标说成 Θ(n^{2/d}) 比题目的 n^{2/d-o(1)} 更强，不能视为等价；其额外精确奇偶维指数未由所给官方材料支持，故不采用。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `10/10`；置信度 `high`
- 尝试路线：先重建格点上界，再尝试距离能量法。令 M_t 为距离 t 出现的无序点对数，D 为不同距离数，Q=Σ_t M_t²；Cauchy–Schwarz 给 D≥\binom n2²/Q。
- 局部结论：取边长 k 的整数格 P={0,…,k−1}^d，n=k^d。平方距离是 1 到 d(k−1)² 间的整数，故 D≤d(k−1)²=O_d(n^{2/d})；非完全 d 次幂可取适当子集，仍得同阶上界。；能量恒等式严格给出 D≥\binom n2²/Q；若能证明 Q≤n^{4−2/d+o(1)}，便可得到所求下界。；但在 d≥4，可在两个互相正交的二维圆上放置各约 n/2 个点，并选半径使所有跨圆点对距离相同；于是某个 M_t=Θ(n²)，从而 Q=Θ(n⁴)。所以所需的无权能量上界实际上为假，而非仅仅尚未证明。
- 第一阻塞点：普通二阶距离能量被 Lenz 型配置中的一个高重数距离完全支配，无法推出任何接近 n^{2/d} 的普适下界。必须剥离高重数的低维结构并递归处理剩余点对；这正是当前维数递推/关联几何方法仍留下固定指数缺口之处。
- 下一步：对距离按 M_t≤n^{2−η} 与 M_t>n^{2−η} 截断：低重数部分用能量估计，高重数部分尝试证明点集集中在少数正交球面或低维代数簇上，再归约到较低维 distinct-distance 问题。先在 d=4 的两圆 Lenz 模型上验证该分解能恢复 Ω(n^{1/2}) 个距离。
- 来源核对：[官方问题页](https://www.erdosproblems.com/1083)确认问题仍 OPEN，并列出格点上界及当前记录的 Solymosi–Vu 型下界。
- 时间记账：所在批次墙钟时间按题数均摊约 70.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1083)；既有候选答案（按不可信材料审计）

### #1084

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f_d(n)$ be minimal such that in any collection of $n$ points in $\mathbb{R}^d$, all of distance at least $1$ apart, there are at most $f_d(n)$ many pairs of points which are distance $1$ apart. Estimate $f_d(n)$.
- 题意摘要：对固定 d,n，令 P⊂R^d，|P|=n，且任意不同 x,y∈P 满足 ‖x-y‖≥1。f_d(n) 是所有这类 P 的单位距离无序点对数的最大值。等价地，它是 n 个内部不交、半径 1/2 的球的最大接触数。
- 状态核对：冻结状态为 open；二维子问题其实已有 Harborth 精确公式，但一般维数估计仍未解决。输入背景中的特殊值“9n²+6n”有误：代入 Harborth 公式应为 f_2(3n²+3n+1)=9n²+3n；例如 n=1 的七点六角簇有 12 条接触边。候选答案正确识别了接触数问题，但其一般“边界损失”公式不能据此视为完整答案。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：采用接触图路线。以 P 为顶点，距离 1 的点对为边。每个顶点的邻点在以它为中心的单位球面上，且彼此距离至少 1，所以度数至多 kissing number τ_d。下界取近立方整数格盒。
- 局部结论：握手引理严格给出 f_d(n)≤τ_d n/2，因而对固定 d 有 f_d(n)=O_d(n)。；若 n=m^d，格点盒 {0,…,m−1}^d 恰有 d(m−1)m^{d−1}=dn−d n^{(d−1)/d} 条单位边；调整各边长可推广为 f_d(n)≥dn−O_d(n^{(d−1)/d})。；因此可严格得到 dn−O_d(n^{(d−1)/d})≤f_d(n)≤τ_d n/2，特别是 f_d(n)=Θ_d(n)。这只是粗阶估计，不解决最佳首项或边界常数。
- 第一阻塞点：要从局部度上界 τ_d n/2 推出统一的负边界项，必须证明有限最密接触结构中有足够多的“边界球”缺少邻居；纯握手引理不提供这种全局几何信息。
- 下一步：先在 d=3 对有限 fcc 格簇建立离散等周不等式：把接触缺额 6n−E 精确写成格点边界泛函，并检验其最小值是否为 Θ(n^{2/3})；这可计算小规模簇并与已知 0.926 常数比较。
- 来源核对：[Erdős Problems #1084](https://www.erdosproblems.com/1084) 确认接触数解释、Harborth 公式及三维已知上界；该页面也显示输入中的二维特殊值系数存在笔误。；[Bezdek–Khan 接触数综述](https://arxiv.org/abs/1601.00145) 可用于核对高维接触数结果，但未把候选答案中的具体常数公式当作已独立证明的结论。
- 时间记账：所在批次墙钟时间按题数均摊约 43.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1084)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean`；既有候选答案（按不可信材料审计）
- 深度项目：深度运行已对水平射线穿越、水平边块的终端线段包含和终端可见性得到声明级无 `sorryAx` 的局部 Lean 结果。下一节点是可见极大水平边块的同侧切触/异侧穿越奇偶分类，随后仍需路径不变性和全局 Jordan 分割；整文件的占位符总数不能替代声明级审计。 [证据](/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/runs/erdos1084-polygonal-ray-crossing-parity/erdos1084-polygonal-ray-crossing-parity-supervised-4h/proof_lab/round-011/summary.md)

### #1085

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f_d(n)$ be minimal such that, in any set of $n$ points in $\mathbb{R}^d$, there exist at most $f_d(n)$ pairs of points which distance $1$ apart. Estimate $f_d(n)$.
- 题意摘要：对固定 d,n，f_d(n)=max_{P⊂R^d, |P|=n}|{{x,y}⊂P:‖x−y‖=1}|；题面“minimal such that every set has at most”即此最大值。这里没有最小间距限制，故与 1084 不同。
- 状态核对：按 2025-10-17 冻结状态为 open。二维、三维仍是核心开放情形；d≥4 的二次主项可以严格重建。当前网页含冻结日期之后的二维更新，未把它倒灌进本 cohort。候选答案列出的 d=4 精确分段式未在本次证明路线中核验，故不采纳。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：对 d≥4 走 Lenz 构造加 Erdős–Stone 路线。令 p=⌊d/2⌋：下界把点均匀放在 p 个两两正交二维子空间中的半径 1/√2 圆上；上界证明单位距离图不含 K_{p+1}(3)，再应用极值图论。
- 局部结论：不同正交圆上的任意两点满足 ‖x−y‖²=1/2+1/2=1，因此均衡分配给出 t_p(n)=((p−1)/(2p))n²+O(1) 条跨部单位边。；若单位距离图含 K_{p+1}(3)，每一部的三个点不能共线：否则另一部任一点须同时与三个不同共线点等距，这是不可能的。故每部的差向量空间维数至少 2。；对不同两部 A,B，由四点恒等式及全部跨边等长可得 (a−a′)·(b−b′)=0。因此 p+1 个至少二维的差空间两两正交，要求 d≥2(p+1)，与 p=⌊d/2⌋ 矛盾。Erdős–Stone 遂给出 f_d(n)≤((p−1)/(2p)+o(1))n²。
- 第一阻塞点：这条路线只封闭了 d≥4 的二次主项。d=2,3 的单位距离图没有适用的固定有限色数禁图结构；直接的点—圆或点—球关联界分别停在约 n^{4/3}、n^{3/2} 的障碍附近。
- 下一步：对 d=3 明确写出点—单位球关联的富球分层，逐层核算 Clarkson 等方法中产生 n^{3/2}β(n) 的那一项，检查是否能利用所有球同半径这一特殊性削弱最富层。
- 来源核对：[Erdős Problems #1085](https://www.erdosproblems.com/1085) 核对了 Lenz 主项、Erdős–Stone 上界以及奇偶维精化。；候选答案所述三维 295/197 指数未纳入冻结结论，因为本次没有从原论文完整重建其适用条件。
- 时间记账：所在批次墙钟时间按题数均摊约 43.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1085)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1085.lean`；既有候选答案（按不可信材料审计）

### #1086

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(n)$ be minimal such that any set of $n$ points in $\mathbb{R}^2$ contains the vertices of at most $g(n)$ many triangles with the same area. Estimate $g(n)$.
- 题意摘要：按非退化解释，对 P⊂R²，|P|=n，令 M(P)=max_{A>0}#{三元子集 T⊂P:area(T)=A}，则 g(n)=max_{|P|=n}M(P)。整体缩放把任意 A>0 化为 1，因此等价于最大单位面积三角形数；若允许 A=0，n 个共线点会给出 C(n,3)，不符合官方等价表述。
- 状态核对：冻结状态为 open；已知 Ω(n²log log n)≤g(n)≤O(n^{20/9})。候选答案只是复述这些界，没有解决缺口。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：尝试把单位面积条件化为加权点线关联。对每个无序基边 {p,q}，第三点 r 必须落在两条平行于 pq、距直线 pq 为 2/‖p−q‖ 的直线上。把这些直线保留重数组成多重集 L。
- 局部结论：若 T(P) 是 P 中单位面积三角形数，则严格有 3T(P)=I(P,L)：每个三角形以三条边分别作基边被计数三次。；若这些约 n² 条候选线互不重合，Szemerédi–Trotter 给出 I(P,L)=O(n²)，从而 T(P)=O(n²)。所以超二次例子必然依赖大量候选线重合。；固定候选线 ℓ 后，产生 ℓ 的基边必须位于某条平行于 ℓ 的支撑线上，并具有由两平行线间距唯一决定的长度；故线的重数归约为平行线上固定距离点对的计数。
- 第一阻塞点：第一处断点是控制候选线的重数分布。单条 ℓ 的重数可能很大，直接用“最大重数×Szemerédi–Trotter”丢失过多；需要同时控制不同平行支撑线上的等距点对，而这正是现有证明中最深的部分。
- 下一步：定义 N_k 为重数位于 [k,2k) 的候选直线数，先证明一个可检验的分层界，例如 N_k=O(n^α/k^β)，再代入加权关联和式 Σ_k k·I(P,L_k)；首要工作是用固定距离点对界验证 β>1 是否可能。
- 来源核对：[Erdős Problems #1086](https://www.erdosproblems.com/1086) 核对冻结界及问题的正面积解释。；[Raz–Sharir 原论文摘要](https://arxiv.org/abs/1501.00379) 明确给出 O(n^{20/9})，支持候选答案中的最佳已知上界。
- 时间记账：所在批次墙钟时间按题数均摊约 43.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1086)；既有候选答案（按不可信材料审计）

### #1087

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be minimal such that every set of $n$ points in $\mathbb{R}^2$ contains at most $f(n)$ many sets of four points which are 'degenerate' in the sense that some pair are the same distance apart. Estimate $f(n)$ - in particular, is it true that $f(n)\leq n^{3+o(1)}$?
- 题意摘要：正确极值解释是 f(n)=max_{P⊂R², |P|=n}D_4(P)，其中 D_4(P) 计数四元子集 S⊂P，使其六条边中至少两条长度相等，即 S 只确定少于六种距离。原题“minimal upper bound”与该最大值等价，但措辞确有歧义。
- 状态核对：冻结状态为 open。候选答案提出的现代分解是有效方向，但其引用 arXiv:1211.1776 实际是“distinct distance subsets”论文，并非 Pach–Tardos 原论文；因此引用链需要纠正。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：按相等的两条线段是否共享端点分解。共享端点产生等腰三角形；端点互异则产生四个不同点组成的等距线段对。令 T_iso(P) 为等腰三元组数，F_dis(P) 为端点全异的有序等距线段对数。
- 局部结论：每个退化四元集至少有一种上述见证，故 D_4(P)≤(n−3)T_iso(P)+C·F_dis(P)，其中 C 只吸收排序约定；重复计数不妨碍上界。；Guth–Katz 的等距四元组估计给出 F_dis(P)=O(n³log n)，所以“不共享端点”部分已经是 n^{3+o(1)}。；代入 Pach–Tardos 的 T_iso(P)=O(n^{2.136+ε}) 可得 D_4(P)=O(n^{3.136+ε})。这确实改进经典 n^{7/2}，但没有证明目标 n^{3+o(1)}。
- 第一阻塞点：分解在共享端点部分首次失效：任一等腰三角形可与约 n 个第四点组合，因此现有路线若不利用严重重叠，就要求 T_iso(P)≤n^{2+o(1)}；当前一般界达不到这一点。不能把 Guth–Katz 的四点估计直接用于含重复端点的情形来消掉该因子。
- 下一步：研究等腰见证的重叠：令 a(S) 为四元集 S 内的等腰三角形数，双计数 Σ_S a(S)=(n−3)T_iso(P)，并分别估计 a(S)=1 与 a(S)≥2 的层；检验多重见证四元集是否可由圆、垂直平分线关联给出 O(n³polylog n) 界。
- 来源核对：[Erdős Problems #1087 讨论页](https://www.erdosproblems.com/forum/thread/1087) 确认题面量词和“少于六种距离”的解释存在措辞问题。；[Guth–Katz, Annals](https://annals.math.princeton.edu/2015/181-1/p02) 支持 O(n³log n) 等距四元组界。；[Pach–Tardos 论文记录](https://infoscience.epfl.ch/entities/publication/f31dbed1-398c-477f-b359-08f4dda9a243) 用于纠正候选答案的间接引用；[arXiv:1211.1776](https://arxiv.org/abs/1211.1776) 本身是 Charalambides 的不同距离子集论文。
- 时间记账：所在批次墙钟时间按题数均摊约 43.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1087)；既有候选答案（按不可信材料审计）

### #1088

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f_d(n)$ be the minimal $m$ such that any set of $m$ points in $\mathbb{R}^d$ contains a set of $n$ points such that any two determined distances are distinct. Estimate $f_d(n)$. In particular, is it true that, for fixed $n\geq 3$,\[f_d(n)=2^{o(d)}?\]
- 题意摘要：f_d(n) 是最小整数 m，使每个 m 点集 P⊂R^d 都含有 n 点子集 Q，且 Q 的 C(n,2) 个无序点对距离两两不同。问题询问固定 n≥3、d→∞ 时是否 log f_d(n)=o(d)。
- 状态核对：冻结状态为 open；n=3 已知 f_d(3)=d²/2+O(d)，故该特例为肯定。n≥4 的次指数问题未解决。候选答案的恒重 0–1 向量下界可以独立核验，但它只给多项式下界，不能反驳次指数猜想。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：构造全局只有少数距离的集合。固定 t=C(n,2)−1；当 d+1≥t 时，在 R^{d+1} 的仿射超平面 Σx_i=t 中取所有重量为 t 的 0–1 向量。该超平面维数 d，可等距嵌入 R^d。
- 局部结论：对两个不同重量 t 向量 x,y，有 ‖x−y‖²=2(t−|supp(x)∩supp(y)|)，所以整个集合至多出现 t 种非零距离。；任意 n 点若所有点对距离不同，就需要 C(n,2)=t+1 种距离；因此上述集合不含目标 n 点子集。；故 f_d(n)≥C(d+1,t)+1=Ω_n(d^{C(n,2)−1})。n=3 时 t=2，得到正确的二次量级下界。
- 第一阻塞点：此路线只利用“整个坏集合的距离种数少”，而一般不含彩虹 K_n 的距离着色仍可能使用很多颜色。要得次指数上界，需要证明任何足够大的欧氏距离着色都含彩虹 K_n；普通 Ramsey 定理不适用，因为颜色数不受控，且必须使用欧氏距离矩阵的秩至多 d+2 等代数约束。
- 下一步：先处理 n=4：把“无六种不同距离的四点集”写成若干距离相等多项式的并，尝试用距离矩阵秩约束和超图容器证明最大坏集为 exp(o(d))；第一项可检验任务是界定一个点参与多少个类型固定的等距冲突三元组或四元组。
- 来源核对：[Erdős Problems #1088](https://www.erdosproblems.com/1088) 核对了量词、Erdős–Straus 指数上界声明、d=1 及 n=3 的已知结果。；[Charalambides 不同距离子集论文](https://arxiv.org/abs/1211.1776) 只处理平面或球面上的大不同距离子集，不能直接推出固定 n、高维 d 的次指数结论。
- 时间记账：所在批次墙钟时间按题数均摊约 43.9 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1088)；既有候选答案（按不可信材料审计）

### #1089

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $g_d(n)$ be minimal such that every collection of $g_d(n)$ points in $\mathbb{R}^d$ determines at least $n$ many distinct distances. Estimate $g_d(n)$. In particular, does\[\lim_{d\to \infty}\frac{g_d(n)}{d^{n-1}}\]exist?
- 题意摘要：固定整数 n≥2、维数 d。令 g_d(n) 为使任意 g_d(n) 个不同点组成的有限集 X⊂R^d 至少产生 n 种非零两点距离的最小整数。等价地，若 M_s(d) 是 R^d 中至多产生 s 种距离的点集最大大小，则 g_d(n)=M_{n-1}(d)+1；问题尤其询问固定 n、d→∞ 时的极限。
- 状态核对：已解决。旧候选的主结论正确，但下界构造只需“至多 k 种距离”；其声称“恰有 k 种”在 d+1<2k 时不成立。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：令 s=n-1。上界采用 Bannai–Bannai–Stanton 的多项式法定理 M_s(d)≤C(d+s,s)。下界取 R^{d+1} 中所有重量为 s 的 0-1 向量；它们位于仿射超平面 Σx_i=s≅R^d，任意两点的平方距离为 2(s−|A∩B|)，故至多有 s 个非零距离。
- 局部结论：该构造给出 M_s(d)≥C(d+1,s)，因而 C(d+1,n−1)+1≤g_d(n)。；Bannai–Bannai–Stanton 定理给出 g_d(n)≤C(d+n−1,n−1)+1。；两端均为 d^{n−1}/(n−1)!+O_n(d^{n−2})，故 g_d(n)=d^{n−1}/(n−1)!+O_n(d^{n−2})，极限为 1/(n−1)!。
- 第一阻塞点：若要求完全自足重建，第一处未在此闭合的是 BBS 上界中的维数引理：插值多项式虽易构造，但必须利用其特殊径向结构，把所在函数空间的维数压到 C(d+s,s)，不能粗略使用全部次数≤2s的多项式空间。该步骤是已发表定理，不是新猜测。
- 下一步：逐行重建 BBS 的线性无关与维数计算，特别核对非球面 s-distance 集无需额外一般位置假设。
- 来源核对：当前题页明确记录相同双边界与极限：[Erdős Problems #1089](https://www.erdosproblems.com/1089)。；BBS 定理的公开摘要明确给出 |X|≤C(d+s,s)：[Bannai–Bannai–Stanton 论文记录](https://experts.umn.edu/en/publications/an-upper-bound-for-the-cardinality-of-an-s-distance-subset-in-rea/)。
- 时间记账：所在批次墙钟时间按题数均摊约 60.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1089)；既有候选答案（按不可信材料审计）

### #1091

- 当前状态：`solved`（冻结清单状态：`open`）
- 精确题面：Let $G$ be a $K_4$-free graph with chromatic number $4$. Must $G$ contain an odd cycle with at least two diagonals? More generally, is there some $f(r)\to \infty$ such that every graph with chromatic number $4$, in which every subgraph on $\leq r$ vertices has chromatic number $\leq 3$, contains an odd cycle with at least $f(r)$ diagonals?
- 题意摘要：第一问量化所有有限简单图 G：若 χ(G)=4 且 G 不含 K4，是否存在一条奇圈 C，使 G 中至少两条不属于 C 的边连接 C 上非相邻顶点。第二问询问是否存在 f:N→R、f(r)→∞，使每个 χ(G)=4 且所有至多 r 个顶点的子图均可 3-着色的 G，都含有至少 f(r) 条对角线的奇圈。
- 状态核对：两问现均已解决：第一问肯定，第二问否定。旧候选正确报告 Voss，却把第二问误报为开放；这与 2026-04-09 的状态更新冲突。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：第一问重建 Voss 路线：取 4-critical 子图，利用其最小度≥3及 K4-free 条件，在最长奇圈/耳分解中排除所有奇圈至多一条弦的情形。第二问采用 2026 年显式反例 G_m：以五边形块组成毛毛虫式块树，再加一个特殊顶点；叶块着色强迫沿脊柱传播，造成不可 3-着色，同时块树结构限制圈的弦数。
- 局部结论：反例 G_m 是 K4-free 且 χ(G_m)=4；删去任一边后所得图为 2-degenerate，故每个真子图均可 3-着色。；若取 |V(G_m)|>r，则每个至多 r 个顶点的子图都是真子图，因而满足局部 3-可着色条件。；每个圈至多有 10 条弦：不经过特殊顶点的圈局限于单个五边形；经过它的圈在块树中只访问一条路径，至多贡献两个端叶块及两个端脊块的弦。因此任何 f(r)→∞ 最终超过10，与 G_m 矛盾。
- 第一阻塞点：第一问的自足证明在 Voss 的核心结构引理处停止：需严格证明 K4-free 的 4-critical 图不可能所有奇圈都至多一条弦。第二问则已有可逐项核验的完整显式构造；本筛查未重抄其全部顶点标签和邻接表。
- 下一步：独立复核 G_m 的邻接表，并用小 m 程序枚举验证 χ=4、K4-free、删边后 2-degenerate 及最大弦数≤10；同时从 Voss 原文提取核心结构引理。
- 来源核对：题页已更新为“第一问 Voss 肯定、第二问显式反例否定”：[Erdős Problems #1091](https://www.erdosproblems.com/1091)。；反例论文给出构造、叶块着色强迫、真子图 2-degenerate 和每圈至多10弦的证明：[Alexeev–Putterman–Sawhney–Sellke–Valiant, §4](https://arxiv.org/html/2604.06609#S4)。
- 时间记账：所在批次墙钟时间按题数均摊约 60.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1091)；既有候选答案（按不可信材料审计）

### #1092

- 当前状态：`disproved`（冻结清单状态：`open`）
- 精确题面：Let $f_r(n)$ be maximal such that, if a graph $G$ has the property that every subgraph $H$ on $m$ vertices is the union of a graph with chromatic number $r$ and a graph with $\leq f_r(m)$ edges, then $G$ has chromatic number $\leq r+1$. Is it true that $f_2(n) \gg n$? More generally, is $f_r(n)\gg_r n$?
- 题意摘要：对固定 r≥2，把 d_r(H) 定义为删去最少多少条边可使 H 的色数≤r。所问阈值函数 f_r 应满足：若某有限图 G 的每个 m 顶点子图 H 都有 d_r(H)≤f_r(m)，则 χ(G)≤r+1；问题问是否存在 c_r>0、N，使所有 m≥N 均有 f_r(m)≥c_rm。
- 状态核对：线性下界已被否定，且对每个固定 r≥2 都是否定。人工评审指出旧候选未处理精确增长率和 r 依赖，这一批评必须吸收：直接写 d_r≤d_2 还没有处理 f_r(m) 只在“大 m”线性、而小 m 的阈值未知这一量词缺口；一般 r 的规范归约还应使用 join。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：使用 Rödl 定理：任意 ε>0、q，存在 χ(X)≥q 的图 X，使每个子图 J⊂X 满足 d_2(J)≤ε|V(J)|。对一般 r 取 G=X∨K_{r−2}。对子图 H，令 S=V(H)∩V(X)、T 为其余顶点；删去至多 ε|S| 条边使 H[S] 二分，再给 T 中每点一个独立颜色，合计至多 2+|T|≤r 色。
- 局部结论：由 join 恒等式 χ(G)=χ(X)+r−2；取 χ(X)>3 即有 χ(G)>r+1。；每个 H⊂G 均满足 d_r(H)≤ε|S|≤ε|V(H)|。；若假设 f_r(m)≥cm 仅对 m≥N 成立，取 ε<min(c,1/N)。当 m<N 时，d_r(H)<1，整数性给出 d_r(H)=0；当 m≥N 时，d_r(H)<cm≤f_r(m)。故 G 满足全部局部条件却 χ(G)>r+1，矛盾。
- 第一阻塞点：归约本身已闭合；唯一外部核心是 Rödl 定理的精确统一形式——同一个有限 X 的每个任意子图 J（不只是诱导子图）均满足 d_2(J)≤ε|V(J)|。此外，“f_r(n)=o(n)”若按普通函数极限理解，比“不存在正线性下界”更强，不能仅凭上述反证随意互换。
- 下一步：回到 Rödl 1982 的 K*(n,k) 构造，逐项核对定理是否确实量化所有任意子图，并把结论精确表述为 f_r(n)≱c_rn，而非未经证明的完整渐近等式。
- 来源核对：当前题页记录 Rödl 反例并称其否定所有固定 r：[Erdős Problems #1092](https://www.erdosproblems.com/1092)。；一般 r 的 join 归约及小 m 修补有完整证明：[A note on Erdős Problem 1092](https://www.ulam.ai/research/erdos1092.pdf)。；本地 Lean 文件并非忠实形式化：它把删边后的目标写成 r+1 而非 r，把统一预算写成常数 k，并用 n=o(f_r(n)) 表示问题；故不能作为该反例的形式核验。
- 时间记账：所在批次墙钟时间按题数均摊约 60.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1092)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1092.lean`；既有候选答案（按不可信材料审计）

### #1093

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For $n\geq 2k$ we define the deficiency of $\binom{n}{k}$ as follows. If $\binom{n}{k}$ is divisible by a prime $p\leq k$ then the deficiency is undefined. Otherwise, the deficiency is the number of $0\leq i<k$ such that $n-i$ is $k$-smooth, that is, divisible only by primes $\leq k$. Are there infinitely many binomial coefficients with deficiency $1$? Are there only finitely many with deficiency $>1$?
- 题意摘要：量化所有整数对 (n,k)，其中 k≥1、n≥2k。仅当每个素数 p≤k 都不整除 C(n,k) 时定义 deficiency；其值是区间 {n−k+1,…,n} 中 k-smooth 数的个数。问题分别问 deficiency=1 的整数对是否无限，以及 deficiency≥2 的整数对是否有限；k 随样例变化。
- 状态核对：两问均仍开放。旧候选的 gcd(C(n,k),k!)=1 等价改写正确，但所列状态和计算样例不是证明。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用 Kummer与 S-unit 归约。good 条件等价于对每个 p≤k，k 与 n−k 的 p 进制相加无进位，也等价于所有 a≥1 均有 n mod p^a≥k mod p^a。若 deficiency≥2，取两个不同的 k-smooth 数 x>y 位于末端 k 区间，令 Δ=x−y<k；则 Δ 也为 k-smooth。除以 g=gcd(x,y)，得到互素正整数 A=y/g、B=Δ/g、C=x/g，满足 A+B=C，且 ABC 的全部素因子≤k。
- 局部结论：good 条件可完全转化为一族无进位同余约束，可用于精确筛除候选 (n,k)。；deficiency≥2 必然产生一个 primitive S-unit 方程 A+B=C，其中 S={p:p≤k}；这是真正的丢番图归约，而非仅凭稀有性作启发。；结合已知 ELS93 定理，任何 deficiency≥1 的样例满足 n≪2^k√k；因此每个固定 k 只有有限多个 n，但这不控制 k→∞。
- 第一阻塞点：第一处无法闭合的是把随 k 增长的 S-unit 方程统一控制到只剩有限多个 k。固定 S 的有限性定理常数强烈依赖 S；现有 n≪2^k√k 也仍允许每个 k 有大量候选。故该归约既不能证明 deficiency≥2 全局有限，也不能构造无限多个 deficiency=1 样例。
- 下一步：实现联合筛查：枚举 primitive k-smooth 解 A+B=C，并同时施加所有 p≤k 的 Kummer 无进位条件；先复现已知 deficiency≥2 清单，再测量可能支持统一高度界的参数（如 C/Δ 与 rad(ABC)）。
- 来源核对：当前题页仍列两问为开放，并记录 ELS93 的 n≪2^k√k：[Erdős Problems #1093](https://www.erdosproblems.com/1093)。；本地 Lean 陈述把“undefined”放在集合的 good 条件中处理，主量词基本忠实；但没有证明内容。
- 时间记账：所在批次墙钟时间按题数均摊约 60.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1093)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1093.lean`；既有候选答案（按不可信材料审计）

### #1094

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：For all $n\geq 2k$ the least prime factor of $\binom{n}{k}$ is $\leq \max(n/k,k)$, with only finitely many exceptions.
- 题意摘要：量化整数 k≥1、n≥2k。令 P(n,k) 为 C(n,k) 的最小素因子；断言违反 P(n,k)≤max(n/k,k) 的整数对 (n,k) 只有有限多个。这里“有限多个例外”是全局同时量化 n、k，而非每个固定 k 分别有限。
- 状态核对：仍为开放猜想。旧候选只是准确报告状态、例外表和固定 k 的已知事实，没有形成证明尝试。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：尝试以 Kummer 条件和 deficiency 分区。若 (n,k) 是反例，则 P(n,k)>k，所以它是 good binomial coefficient；于是对每个 p≤k，k+(n−k) 的 p 进制相加无进位。再分 2k≤n<k² 与 n≥k²：前一区间目标是迫使某个 p≤k 整除二项式；后一区间还须得到更强的 P(n,k)≤n/k。
- 局部结论：任何反例都满足 good 条件，即 gcd(C(n,k),k!)=1，并受全部 Kummer 无进位约束。；在 n≥k² 区域，若 q>k 是某个分子项 n−i 的素因子，则 q不会被 k! 抵消，故 q|C(n,k)；反例条件进一步迫使 q>n/k。；因此每个非 k-smooth 的分子项都必须含有一个大于 n/k 的素因子；由于该素因子大于区间长度 k，它至多整除这 k 个连续整数中的一个。官方所述 ELS 结构结论进一步把反例限制到 deficiency≥1。
- 第一阻塞点：直接乘积分子项的路线在这里停止：知道每个非光滑项拥有一个彼此分离的素因子 q>n/k，并不足以与 ∏(n−i)=k!C(n,k) 矛盾；其余小因子仍可按复杂方式分配。特别是不能从“固定 k 时最终成立”推出全局仅有限例外，缺少的是对 k 一致的阈值。
- 下一步：先独立重建 ELS 的关键结构引理“deficiency=0 ⇒ P(n,k)≤n/k”，将大素因子的唯一归属与小素因子估值写成严格乘积不等式；随后量化该证明中随 k 增长的常数，检查能否覆盖 n≥k² 或更大统一区域。
- 来源核对：当前记录仍把全局有限例外断言列为开放，并明确指出反例只能来自正 deficiency：[Erdős Problems #1094](https://www.erdosproblems.com/1094)。；本地 Lean 陈述使用 Nat 整除 n/k；因最小素因子为整数，minFac>⌊n/k⌋与实数不等式 minFac>n/k 等价，主命题基本忠实。
- 时间记账：所在批次墙钟时间按题数均摊约 60.3 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1094)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1094.lean`；既有候选答案（按不可信材料审计）

### #1095

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $g(k)>k+1$ be the smallest $n$ such that all prime factors of $\binom{n}{k}$ are $>k$. Estimate $g(k)$.
- 题意摘要：对每个整数 k，g(k) 是满足 n>k+1 且对每个素数 p≤k 都有 p∤C(n,k) 的最小 n；问题要求估计 k→∞ 时的增长，而不是仅证明 g(k) 存在。
- 状态核对：截至所给更新时间仍开放。候选答案正确列出已知界和启发式，但没有形成证明尝试，不能视为解答。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：采用 Lucas 定理，把所有小素数条件转成有限的同余筛。对 p≤k 取 e_p=floor(log_p k)+1，使 p^{e_p}>k。若 k=Σ_{j<e_p}k_jp^j，则 p∤C(n,k) 当且仅当 n 的前 e_p 个 p 进制数字满足 n_j≥k_j。因此条件仅依赖 n mod p^{e_p}；再用 CRT 合并。
- 局部结论：令 Q_k=∏_{p≤k}p^{e_p}=lcm(1,…,k)·∏_{p≤k}p。所有可行 n 构成模 Q_k 的若干剩余类。；模 p^{e_p} 的可行剩余类数恰为 r_p=∏_{j<e_p}(p-k_j)，故整体可行类密度为 ρ_k=∏_{p≤k}r_p/p^{e_p}。这给出了一个明确、可计算的有限筛模型。；n=Q_k-1 在每个底 p 下的前 e_p 位全为 p-1，故对所有 p≤k 均满足 Lucas 条件。于是 g(k)≤Q_k-1，且由素数定理 log Q_k=ψ(k)+θ(k)=(2+o(1))k。这虽弱于文献中的 exp((1+o(1))k)，但推导是自足的。
- 第一阻塞点：要达到猜测尺度 log g(k)≈k/log k，必须证明结构高度相关的 CRT 可行类在远小于 Q_k 的初始区间内出现。把首次命中简单视为约 1/ρ_k 只是随机均匀性假设；目前路线中没有控制这些剩余类位置或相关性的定理，这是第一处不能闭合之处。
- 下一步：对增长的 k 精确计算 ρ_k、最小可行正代表及其比值 g(k)ρ_k，并按素数区间分解 log ρ_k；检验“首次命中≈1/ρ_k”究竟在哪些 k 上失效，再尝试把失效归结为少数素数的数字约束。
- 来源核对：已独立核对 Lucas/Kummer 条件：候选答案中的“不进位”表述正确，但没有处理首次同时命中的难点。；官方记录仍给出 Konyagin 下界 g(k)≫exp(c(log k)^2) 与启发式 log g(k)≈k/log k：https://www.erdosproblems.com/1095
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1095)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1095.lean`；既有候选答案（按不可信材料审计）

### #1096

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：Let $1<q<1+\epsilon$ and consider the set of numbers of the shape $\sum_{i\in S}q^i$ (for all finite $S$), ordered by size as $0=x_1<x_2<\cdots$. Is it true that, provided $\epsilon>0$ is sufficiently small, $x_{k+1}-x_k \to 0$?
- 题意摘要：对象是 X(q)={Σ_{i∈S}q^i:S⊂Z_{≥0} 有限} 的严格递增枚举。命题量词为：是否存在 ε_0>0，使每个 1<q<1+ε_0 都满足 x_{k+1}-x_k→0。
- 状态核对：已证明。官方页面于 2026 年更新：Erdős–Komornik 已对 1<q<sqrt(q_1)≈1.175 证明结论。候选答案引用 Akiyama–Komornik 的较后、较强定理，可推出更大的显式区间，但遗漏了最早解决路线。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `10/10`；置信度 `high`
- 尝试路线：重建较强的谱方法：记 L_1(q)=limsup_k(x_{k+1}-x_k)。Akiyama–Komornik 的谱定理断言，若 1<q≤2^{1/3} 且 q 非 Pisot，则 L_1(q)=0。再消去该区间内的 Pisot 例外。
- 局部结论：最小 Pisot 数是满足 z^3=z+1 的实根 q_0≈1.3247，而 2^{1/3}≈1.2599<q_0；故 (1,2^{1/3}] 内不存在 Pisot 数。端点 2^{1/3} 本身也非 Pisot，因为其非实共轭的模大于 1。；因此谱定理在每个 1<q≤2^{1/3} 上给出 L_1(q)=0。；各间隙非负，所以 limsup 为 0 立即推出普通极限为 0。可取 ε_0=2^{1/3}-1；原问题因而得到肯定答案。
- 第一阻塞点：本次受限重建没有从头证明 Akiyama–Komornik 的关键谱定理；其核心是由差谱在 0 附近的聚点构造对所有足够大位置都有效的细网，而不能只由 liminf 间隙为 0 直接推出 limsup 为 0。若禁止引用该定理，证明在这里停止。
- 下一步：逐引理核对 Akiyama–Komornik Theorem 1.4(i) 的端点、非 Pisot 假设及 X_1/L_1 记号，并与 Erdős–Komornik 1998 年较小区间的原证明逐项对照。
- 来源核对：官方状态及最早解决区间：https://www.erdosproblems.com/1096；Akiyama–Komornik 原论文条目：https://arxiv.org/abs/1103.4508；1998 年相关原始论文书目信息：https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/83/3/110099/on-the-sequence-of-numbers-of-the-form-q-nq-n-i-0-1
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1096)；既有候选答案（按不可信材料审计）

### #1097

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be a set of $n$ integers. How many distinct $d$ can occur as the common difference of a three-term arithmetic progression in $A$? Are there always $O(n^{3/2})$ many such $d$?
- 题意摘要：对 |A|=n，令 D(A)={d>0:存在 a，使 a,a+d,a+2d∈A}，并令 f(n)=max_{|A|=n}|D(A)|。问题一是确定 f(n) 的量级；问题二是是否 f(n)=O(n^{3/2})。
- 状态核对：精确指数仍开放，但 O(n^{3/2}) 子猜想已经为已知构造否定。目前记录为 n^{1.77898…-o(1)}≤f(n)≪n^{11/6}。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：把三项等差数列编码成受限和差集。令 G={(x,z)∈A×A:(x+z)/2∈A}。则受限和集只有至多 n 个值，而受限差集编码所有公差；反向则把任意 G⊂B×C 的边 (b,c) 编成三项等差数列 (2b,b+c,2c)。
- 局部结论：沿 G 有 A+_G A⊂{2a:a∈A}，故 |A+_G A|≤n；同时 A-_G A 含有每个 ±2d，因此 |D(A)|≤|A-_G A|/2。Katz–Tao 的受限和差估计遂给出 |D(A)|≪n^{11/6}。；反向令 E=2B∪(B+_G C)∪2C，则 |E|≤|B|+|C|+|B+_G C|≤3N；每条边产生 (2b,b+c,2c)，其公差为 c-b。因此对 f(n) 的任意指数上界都会给出同指数的受限和差集上界，至多损失常数和 d=0。；已知受限和差集构造经上述反向编码给出 f(n)≥n^{1.77898…-o(1)}，故不存在普适 O(n^{3/2}) 上界。
- 第一阻塞点：编码本身闭合，但它只把问题精确归约到算术 Kakeya/受限和差指数。要改进 11/6，必须加强 Katz–Tao 的组合链估计；当前路线没有排除造成重复中间顶点的高能量配置，这就是首个实质障碍。
- 下一步：将 Katz–Tao 11/6 证明写成各次 Cauchy–Schwarz 后的显式纤维计数，定位等号近似成立的配置；随后检查三项 AP 来源的图 G 是否具有一般二部图没有的对称性，可否在其中一步获得幂次节省。
- 来源核对：官方当前指数与等价性：https://www.erdosproblems.com/1097；Katz–Tao 原论文：https://arxiv.org/abs/math/9906097；候选答案中 A+_G A⊂2A 的写法有歧义：这里必须解释成对角伸缩集 {2a:a∈A}，不能解释成通常的和集 A+A。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1097)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1097.lean`；既有候选答案（按不可信材料审计）

### #1100

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $1=d_1<\cdots<d_{\tau(n)}=n$ are the divisors of $n$, then let $\tau_\perp(n)$ count the number of $i$ for which $(d_i,d_{i+1})=1$. Is it true that $\tau_\perp(n)/\omega(n)\to \infty$ for almost all $n$? Is it true that\[\tau_\perp(n)< \exp((\log n)^{o(1)})\]for all $n$? Let\[g(k) = \max_{\omega(n)=k}\tau_\perp(n),\]where $\omega(n)$ counts the number of distinct prime divisors of $n$, and $n$ is restricted to squarefree integers. Determine the growth of $g(k)$.
- 题意摘要：对 n 的正因子递增序列 d_1<…<d_{τ(n)}，τ_⊥(n) 统计相邻且互素的对数。问题分别问：几乎所有 n 是否有 τ_⊥(n)/ω(n)→∞；是否对所有 n 有 τ_⊥(n)<exp((log n)^{o(1)})；以及在 n 限制为含 k 个素因子的平方自由数时，g(k)=max τ_⊥(n) 的增长。
- 状态核对：三项精细问题仍开放；已知 Erdős–Simonovits 给出 (sqrt(2)+o(1))^k<g(k)<(2-c)^k。讨论页还指出这两个界的证明并未出现在被引用的 1981 年短文中，故不应把书目陈述冒充已重建证明。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `medium`
- 尝试路线：先严格完成平方自由情形的子集和模型。若 n=∏_{j=1}^kp_j，令 x_j=log p_j；因子对应子集 S，大小次序对应 Σ_{j∈S}x_j 的次序，而两个因子互素当且仅当对应子集不交。再验证该模型的反向可实现性。
- 局部结论：实际素数权重的 2^k 个子集和两两不同，因为不同子集给出不同整数乘积；故 τ_⊥(n) 正是该线性次序中相邻不交子集对的数目。；反之，对任意正的、子集和无相等关系的权重 y_1,…,y_k，取 T→∞，并由素数定理在 exp(Ty_j) 附近选取不同素数 p_j，则 log p_j/T→y_j。有限多个严格子集和不等式最终全部保持。因此每种一般位置的权重次序都可由素数实现。；所以 g(k) 精确等于：在所有正的一般位置权重下，最大化布尔格 2^{[k]} 的子集和次序中相邻不交对的数目。立即有 k≤g(k)≤2^k-1；文献中的上下界进一步说明 log g(k)=Θ(k)。
- 第一阻塞点：要从线性泛函诱导的特殊次序推出 g(k)≤(2-c)^k，不能只数全部不交对子；后者共有约 3^k 个，甚至比所需界更弱。必须利用“相邻子集和之间没有第三个子集和”的几何约束来排除正比例的候选边，本次尝试尚未建立这种排除引理。
- 下一步：把每个相邻不交对 (S,T) 写成开锥不等式 Σ_Sx<Σ_Ux<Σ_Tx 不存在解的条件，并按 |S∪T| 分层；先用线性规划对 k≤10 枚举可实现次序，寻找能导致固定比例禁边的局部模式。
- 来源核对：官方讨论及对缺失证明的提醒：https://www.erdosproblems.com/forum/thread/1100；候选答案把模型称为“等价”但未证明任意一般位置权重可由素数对数实现；上面的素数定理近似补上了这一缺口。；没有采用讨论区中已被反例否定的候选上界 τ_⊥≤binom(k,2)+1。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1100)；既有候选答案（按不可信材料审计）

### #1101

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $u=\{u_1<u_2<\cdots\}$ is a sequence of integers such that $(u_i,u_j)=1$ for all $i\neq j$ and $\sum \frac{1}{u_i}<\infty$ then let $\{a_1<a_2<\cdots\}$ be the sequence of integers which are not divisible by any of the $u_i$. For any $x$ define $t_x$ by\[u_1\cdots u_{t_x}\leq x< u_1\cdots u_{t_x}u_{t_x+1}.\]We call such a sequence $u_i$ good if, for all $\epsilon>0$, if $x$ is sufficiently large then\[\max_{a_k<x} (a_{k+1}-a_k) < (1+\epsilon)t_x \prod_{i}\left(1-\frac{1}{u_i}\right)^{-1}.\]Is there a good sequence such that $u_n< n^{O(1)}$? Is there a good sequence such that $u_n\leq e^{o(n)}$?
- 题意摘要：量词是：u_i 为递增、两两互素的整数序列且 Σ1/u_i<∞；a_k 枚举不被任何 u_i 整除的正整数；t_x 由前缀乘积夹住 x。所谓 good 要求对每个 ε>0，所有充分大的 x 都有最大间隙小于 (1+ε)t_x/δ，其中 δ=∏_i(1-1/u_i)。问题问是否存在多项式增长或至少 e^{o(n)} 增长的 good 序列。
- 状态核对：两问仍开放。已知某些增长很快的素数子序列是 good；Erdős 预期多项式增长不存在、次指数增长存在。候选答案关于“双指数已经足够”等定量说法没有给出可核原证明，本筛查不采用。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：以 CRT 构造长的 B-free 空段，并把自然测试例 u_i=p_i^2 的 t_x 与 squarefree 间隙尺度精确比较，以判断 good 上界需要补足什么。
- 局部结论：因 Σ1/u_i<∞，无穷乘积 δ=∏(1-1/u_i) 收敛到正数。；令 U_t=∏_{i≤t}u_i。CRT 可解 N+j≡0 mod u_j（1≤j≤t），故 N+1,…,N+t 全部被某个 u_i 整除。取合适的正代表并平移 U_t，可在 x≈2U_t、且最终 t_x=t 的尺度制造长度 t 的空段。这个自足论证得到正确量级 t，但没有达到普适筛下界中的常数 δ^{-1}。；对 u_i=p_i^2，有 δ=∏_p(1-p^{-2})=6/π^2，且 log U_t=2θ(p_t)∼2t log t，所以 t_x∼log x/(2log log x)。good 将要求最大平方自由数间隙至多 (π^2/12+o(1))log x/log log x；CRT 只给出约 (1/2)log x/log log x 的空段。
- 第一阻塞点：证明 prime-square 序列 good 等价于在每个位置、以接近 π^2/12 的常数控制平方自由数空隙。普通 CRT 只负责制造空隙，不能证明每个更长区间含平方自由数；初等筛在长度约 log x/log log x 时的余项大于主项。这是当前路线第一处无法闭合的步骤。
- 下一步：先对有限模积 U_t 精确计算圆法/容斥余项：对长度 L=(δ^{-1}+η)t 的每个区间，统计未被 p_i^2（i≤t）覆盖的位置；确定失败是否来自小素数周期结构还是尾部 p_i^2，并据此测试可否为稀疏但 e^{o(i)} 的 u_i 设计均匀覆盖引理。
- 来源核对：官方开放状态、普适下界及 prime-square 测试例：https://www.erdosproblems.com/forum/thread/1101；没有沿用候选答案中未核实的具体增长率或短区间文献断言；它们并不能闭合 good 所需的近最优常数上界。
- 时间记账：所在批次墙钟时间按题数均摊约 57.6 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1101)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1101.lean`；既有候选答案（按不可信材料审计）

### #1103

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $A$ be an infinite sequence of integers such that every $n\in A+A$ is squarefree. How fast must $A$ grow?
- 题意摘要：按通常含义取正整数序列 A={a_1<a_2<…}；要求对所有 i,j（包括 i=j），a_i+a_j 均为平方自由数。若严格允许任意整数，应另外规定负数的平方自由性并说明向哪个方向“增长”。问题是确定 a_j 的最低增长率及可构造的最低上界。
- 状态核对：仍开放。已知 j^{15/11-o(1)}≪a_j，而存在 a_j<exp(5j/log j) 的序列；是否存在多项式增长序列未知。先前候选给出的已知窗口基本符合题面，但不是问题的解决。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：尝试从每个模 p²的局部禁配条件出发做筛。令 S_p 为 A 在 Z/p²Z 中占据的剩余类。平方自由条件给出 0∉S_p+S_p，即 S_p∩(-S_p)=∅；再尝试用大筛把所有 p 的限制合并成 A∩[1,N] 的上界。
- 局部结论：由 2a_i 平方自由，严格得到每个 a_i 本身平方自由且为奇数。；模4考察任意两项：若同时出现 1、3 两类，其和被4整除；故整个 A 必全落在同一个模4剩余类中。；对奇素数 p，S_p∩(-S_p)=∅，故 |S_p|≤(p²-1)/2；剩余类0也不可能出现。
- 第一阻塞点：第一处断点是把各模 p²的“至多约一半剩余类”限制合并成强于平凡量级的全局计数界。普通大筛没有利用 S_p 与加法对偶 -S_p 的细结构，无法由上述局部结论推出 N^{11/15+o(1)}，更不能排除多项式增长。
- 下一步：选定 P=N^θ，完整重建 Konyagin有限筛中从成对同余计数到 |A∩[1,N]|≪N^{11/15+o(1)} 的关键能量不等式，并逐项检查它是否允许对角和 2a。
- 来源核对：[van Doorn–Tao 预印本](https://arxiv.org/abs/2512.01087)的摘要明确覆盖所有 a+a′ 平方自由时的增长问题。；[Erdős Problems 1103](https://www.erdosproblems.com/latex/1103)列出 a_j>0.24j^{4/3}、Konyagin 的 j^{15/11-o(1)} 下界及 exp(5j/log j) 构造。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1103)；既有候选答案（按不可信材料审计）

### #1104

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(n)$ be the maximum possible chromatic number of a triangle-free graph on $n$ vertices. Estimate $f(n)$.
- 题意摘要：对每个 n，f(n) 是所有恰有 n 个顶点且不含三角形的有限简单图 G 的 χ(G) 的最大值；目标是 n→∞ 时估计 f(n)，尤其确定 sqrt(n/log n) 前的常数。
- 状态核对：数量级已知，但最佳已知常数区间仍为 1-o(1) 与 2+o(1)，故精确渐近仍开放。本地 Lean 文件只陈述“存在 c₁≤1、c₂≥2”的较弱 eventual bounds，且证明均为 sorry，不能视为形式验证。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `7/10`；置信度 `high`
- 尝试路线：走 Ramsey 反演路线。利用 R(3,k) 的构造取得无三角形且 α(G)<k 的图，再用 χ(G)≥|V(G)|/α(G)；上界方向则在每个诱导子图中反复取由 Ramsey 上界保证的大独立集并贪心删除。
- 局部结论：若 R(3,k)>N，则存在 N 顶点三角形自由图且 α<k，因此 χ>N/k；必要时添加孤立点可转成恰有 n 个顶点。；由 R(3,k)≥(1/2+o(1))k²/log k，取 k=(1+o(1))sqrt(n log n)，得到 f(n)≥(1-o(1))sqrt(n/log n)。；仅用 R(3,k)≍k²/log k 并逐次删除独立集，已足以严格推出 f(n)=Θ(sqrt(n/log n))，但不能自动得到最优上界常数2。
- 第一阻塞点：首个不能闭合之处是上界常数：朴素 Ramsey反演只控制每一步可删除独立集的量级，累积损失不足以推出 Davies–Illingworth 的 2+o(1)，更无法把2降到1。先前候选中“χ≥n/α”的使用正确，但由一次 Ramsey估计直接声称锐利上界并不成立。
- 下一步：把贪心删除写成递推 T(m)≤1+T(m-c sqrt(m log m)) 并精确求和，记录所得常数；再与 Davies–Illingworth 的局部着色引理逐项比较，定位常数2所需的额外结构。
- 来源核对：[Hefty–Horn–King–Pfender](https://www.arxiv.symmetricfunctions.com/paper/2510.19718v2)陈述 R(3,k)≥(1/2+o(1))k²/log k。；本地 1104.lean 的定义确为 Fin n 上三角形自由图的最大色数，但两个变体均保留 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1104)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1104.lean`；既有候选答案（按不可信材料审计）

### #1105

- 当前状态：`proved`（冻结清单状态：`open`）
- 精确题面：The anti-Ramsey number $\mathrm{AR}(n,G)$ is the maximum possible number of colours in which the edges of $K_n$ can be coloured without creating a rainbow copy of $G$ (i.e. one in which all edges have different colours). Let $C_k$ be the cycle on $k$ vertices. Is it true that\[\mathrm{AR}(n,C_k)=\left(\frac{k-2}{2}+\frac{1}{k-1}\right)n+O(1)?\]Let $P_k$ be the path on $k$ vertices and $\ell=\lfloor\frac{k-1}{2}\rfloor$. If $n\geq k\geq 5$ then is $\mathrm{AR}(n,P_k)$ equal to\[\max\left(\binom{k-2}{2}+1, \binom{\ell-1}{2}+(\ell-1)(n-\ell+1)+\epsilon\right)\]where $\epsilon=1$ if $k$ is odd and $\epsilon=2$ otherwise?
- 题意摘要：固定 k。第一问断言当 n→∞ 时，无彩虹 C_k 的 K_n 边着色所能使用的最大颜色数为 ((k-2)/2+1/(k-1))n+O_k(1)。第二问对所有 n≥k≥5，要求 AR(n,P_k) 等于题给两个显式构造值的最大值。
- 状态核对：当前状态为已证明，需重建两条彼此独立的文献路线。明确吸收人工评审意见：Yuan 只解决路径，不能据此宣称周期已解；周期部分由 Montellano–Ballesteros–Neumann-Lara 的另一篇论文解决。先前候选给出的周期“便利精确公式”未获得本次逐项核验，故不复述。
- 初步判定：`known_resolution`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：采用代表图法：从每种颜色选一条边形成代表图；若代表图含目标 G，就得到彩虹 G。因此无彩虹着色的每个代表图均为 G-free。周期部分结合论文的反周期结构定理；路径部分结合连通 P_k-free 图的极值分类，并与两个显式着色构造匹配。
- 局部结论：代表图法严格把颜色数转化为一个同边数的禁图问题；这是两个已知证明的共同入口。；路径第一构造：K_{k-2} 内各边异色，其余边共用一个新颜色，颜色数为 binom(k-2,2)+1，且彩虹 P_k 不可能容纳所需的 k-1 条互异边。；周期论文确实对所有 n≥k≥3确定了强制彩虹 C_k 的阈值；其推论给出题述线性主项。Yuan 的 Theorem 1 则逐项给出题述路径公式。
- 第一阻塞点：作为已知证明重建，剩余未在本次筛查中展开的第一处技术步骤，是代表图各连通分量的完整结构分类：仅凭 ex(n,C_k) 或 ex(n,P_k) 的粗界得不到周期中的 1/(k-1) 修正项，也得不到路径公式的两个分支。该步骤由两篇论文分别完成，而非一个初等推论。
- 下一步：直接抄录并核验周期论文主定理中 h(n,k) 与本题 AR(n,C_k) 的“相差1”约定，再对 k=3、4及 n=k 做边界检查；路径公式则核验奇偶 ε 构造及自然数截断。
- 来源核对：[周期论文页面](https://www.researchgate.net/publication/226536214_An_Anti-Ramsey_Theorem_on_Cycles)明确称确定所有 n≥p≥3 的 h(n,p)，并以推论证明 Erdős–Simonovits–Sós 猜想。；[Yuan 预印本](https://arxiv.org/abs/2102.00807)的 Theorem 1 与题述路径公式一致。；[更新后的 1105 条目](https://www.erdosproblems.com/latex/1105)分别列出周期论文与 Yuan 路径结果；本地 Lean 文件也分成 parts.i、parts.ii，但仍是 sorry。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1105)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1105.lean`；既有候选答案（按不可信材料审计）

### #1106

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p(n)$ denote the partition function of $n$ and let $F(n)$ count the number of distinct prime factors of\[\prod_{1\leq k\leq n}p(k).\]Does $F(n)\to \infty$ with $n$? Is $F(n)>n$ for all sufficiently large $n$?
- 题意摘要：令 p(k) 为分拆数，F(n)=|⋃_{1≤k≤n}{q:q为素数且q∣p(k)}|。第一问是 lim_{n→∞}F(n)=∞；第二问是是否存在 N，使所有 n≥N 都有 F(n)>n。
- 状态核对：第一问已有肯定证明，第二问仍开放，所以整题标为 open 是合理的。先前候选用 Ono 定理证明第一问的逻辑有效；其中计算阈值与 OEIS 数据不构成第二问证明。本地 Lean 把第一问仍标 research open，且 answer(sorry)，状态已落后于题面资料。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：先用“每个素数至少整除某个分拆数”证明发散；再尝试从 Hardy–Ramanujan 的 log p(k)≍sqrt(k) 和乘积大小估计推出 F(n)>n。
- 局部结论：F(n) 单调不减，因为其素因子集合随 n 取并集扩大。；给定 M，取 M 个不同素数 q_i。Ono 的结果（对 q≥5；2∣p(2)、3∣p(3)）给出下标 m_i 使 q_i∣p(m_i)。令 N=max m_i，则 F(N)≥M；由单调性严格推出 F(n)→∞。；设 Q_n=∏_{k≤n}p(k)，由 log p(k)≍sqrt(k) 得 log Q_n≍n^{3/2}；但这只控制带重数的总素因子质量，不能控制不同素因子数。
- 第一阻塞点：第二路线首先断在指数上：即使 Q_n 只有很少几个不同素因子，它们也可带任意高指数；Q_n 的巨大尺寸本身不给出 F(n) 的线性下界。必须控制 v_q(p(k)) 的总和或证明大量新素数出现，目前没有这种强度。
- 下一步：对固定素数 q，尝试建立可检验的统一估计 Σ_{k≤n}v_q(p(k))≤B_q(n)，并计算若对 q≤exp(Csqrt n) 有何种平均 B_q(n) 才足以强迫 F(n)>n；这会明确量化现有方法差多少。
- 来源核对：[Ono 原论文](https://arxiv.org/abs/math/0008140)证明每个素模数都有无穷多个分拆同余；2和3可由 p(2)=2、p(3)=3补齐。；题面所引 Schinzel–Wirsing 的已知结果仅为 F(n)≫log n，远不足以推出 F(n)>n。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1106)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1106.lean`；既有候选答案（按不可信材料审计）

### #1107

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $r\geq 2$. A number $n$ is $r$-powerful if for every prime $p$ which divides $n$ we have $p^r\mid n$. Is every large integer the sum of at most $r+1$ many $r$-powerful numbers?
- 题意摘要：量词是：对每个固定整数 r≥2，是否存在 N_r，使每个 n≥N_r 都能写成 s≤r+1 个正 r-powerful 数之和；r-powerful 指每个整除该数的素数 p 都满足 p^r整除它。通常1因无素因子而被允许。
- 状态核对：r=2 已由 Heath-Brown 证明；一般 r≥3 仍开放。先前候选所列有限计算只能作为实验，不能推出例外有限。
- 初步判定：`partial`；证明尝试：`heuristic_route`；可行性 `3/10`；置信度 `medium`
- 尝试路线：先缩小到完全 r 次幂：每个 m^r 都是 r-powerful，故可调用 Waring 型结果取得某个仅依赖 r 的有限加数上界；随后尝试用圆法把加数数目压到临界值 r+1。
- 局部结论：任意完全 r 次幂都是 r-powerful，因此 Waring 定理至少给出：对每个固定 r，所有充分大整数是至多 G(r) 个 r-powerful 数之和。；当 r=2，目标恰为三个平方满数之和，Heath-Brown 的定理完成该特例。；若只使用完全 r 次幂，r+1 个变量处于非常稀疏的临界范围；经典 Waring 主定理所需变量数一般大于 r+1，因此该降级路线不能直接回答原题。
- 第一阻塞点：第一处无法闭合的是圆法的 minor-arc 界：r-powerful 数到 x 仅约 x^{1/r} 量级，r+1重卷积刚到可能覆盖整数的临界密度；现有的完全 r 次幂指数和估计不足以给出所有大整数的正主项。还必须同时证明各模数的局部密度不消失。
- 下一步：先对 r=3 明确计算立方满数在 q^t 模下的和集，检查四重和是否对小素数幂全部覆盖；若无局部障碍，再建立截断生成函数 S(α)=Σ_{m≤x,3-full}e(αm) 的二阶或四阶矩数值/理论界。
- 来源核对：题面与本地 1107.lean 均把一般 r 命题和 r=2 的已解决变体分开；Lean 证明仍为 sorry。；Heath-Brown 的已知结果只覆盖 r=2，不能外推到 r≥3。
- 时间记账：所在批次墙钟时间按题数均摊约 57.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1107)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1107.lean`；既有候选答案（按不可信材料审计）

### #1108

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let\[A = \left\{ \sum_{n\in S}n! : S\subset \mathbb{N}\textrm{ finite}\right\}.\]If $k\geq 2$, then does $A$ contain only finitely many $k$th powers? Does it contain only finitely many powerful numbers?
- 题意摘要：令 \(A=\{\sum_{n\in S}n!:S\subseteq\mathbb N\text{ 有限}\}\)，其中同一指标至多使用一次，Lean 版本允许 \(0!,1!\) 分别出现。问题分别问：(i) 对每个固定的 \(k\ge2\)，集合 \(\{x\in A:\exists y\in\mathbb N,\ x=y^k\}\) 是否有限；(ii) \(A\) 中满足每个素因子的指数至少为 2 的数是否有限。
- 状态核对：截至核查时仍开放。固定项数 \(|S|=r\) 时已有 Brindza–Erdős 的有界性，但原题允许 \(r\) 随元素增长。先前候选主要罗列计算结果，没有形成证明；这些有限列表不能证明有限性。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `3/10`；置信度 `high`
- 尝试路线：取非空 \(S\) 的最小指标 \(m\)，写 \(x=\sum_{n\in S}n!=m!U\)。利用所有 \(n>m\) 的 \(n!/m!\) 都被 \(m+1\) 整除，研究 \(U\) 在 \(m+1\) 的素因子处的赋值。
- 局部结论：严格有 \(U\equiv1\pmod{m+1}\)，故 \(\gcd(U,m+1)=1\)。；若 \(x=y^k\)，则对每个素数 \(\ell\mid m+1\)，必须有 \(k\mid v_\ell(m!)\)。；特别地，若 \(m\) 为奇数且 \((m+1)/2\) 为素数 \(\ell\)，则 \(v_\ell(x)=v_\ell(m!)=1\)，所以 \(x\) 既非任何 \(k\ge2\) 次幂，也非 powerful。
- 第一阻塞点：该同余只控制 \(m+1\) 的素因子；例如 \(m+1\) 为素数时，这些素数大于 \(m\)，所得条件完全空泛。尚无法证明所有充分大的最小指标 \(m\) 都产生某个指数为 1 或不被 \(k\) 整除的素因子，也无法控制无界的项数。
- 下一步：检验能否把论证扩展到多个连续模数 \(m+j\)：对给定 \(k\)，计算并证明哪些短区间必含素数 \(\ell\) 使 \(v_\ell(m!)\not\equiv0\pmod k\)，同时追踪较小阶乘项是否破坏相应同余。
- 来源核对：当前问题页仍标为 OPEN：https://www.erdosproblems.com/1108；本地 1108.lean 确认量词是 \(\forall k\ge2\)，且 powerful 的定义为 \(p\mid n\Rightarrow p^2\mid n\)。；Brindza–Erdős 结果仅固定求和项数，不能直接覆盖原题。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1108)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1108.lean`；既有候选答案（按不可信材料审计）

### #1109

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(N)$ be the size of the largest subset $A\subseteq \{1,\ldots,N\}$ such that every $n\in A+A$ is squarefree. Estimate $f(N)$. In particular, is it true that $f(N)\leq N^{o(1)}$, or even $f(N) \leq (\log N)^{O(1)}$?
- 题意摘要：\(f(N)\) 是所有 \(A\subseteq[1,N]\cap\mathbb Z\) 中的最大基数，条件是对每个有序或无序对 \(a,a'\in A\)，包括 \(a=a'\)，整数 \(a+a'\) 均无平方素因子。问题要求估计 \(f(N)\)，尤其问是否 \(f(N)=N^{o(1)}\)，甚至是否有固定 \(C\) 使 \(f(N)\le(\log N)^C\)。
- 状态核对：仍开放；已知 \((\log N)^2\log\log N\ll f(N)\ll N^{11/15+o(1)}\)。先前候选给出的奇偶与模 4 必要条件正确，但没有把它们推进为所问上界。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `6/10`；置信度 `high`
- 尝试路线：对每个素数平方 \(p^2\) 限制 \(A\) 所占剩余类，再用中国剩余定理做一个初等乘积筛。
- 局部结论：由对角和 \(2a\) 无平方因子，所有 \(a\in A\) 都是奇数且本身无平方因子；模 4 下所有元素必须同属 \(1\) 或 \(3\) 这一类。；对奇素数 \(p\)，若 \(R_p\) 是 \(A\bmod p^2\) 的支撑，则 \(0\notin R_p\)，且不能同时有 \(r,-r\in R_p\)，故 \(|R_p|\le(p^2-1)/2\)。；取前 \(s\) 个素数并令 \(M=\prod_{j\le s}p_j^2\le N\)，CRT 给出 \(|A|\le (N/M+1)M/2^s\le2N/2^s\)。用标准素数乘积估计可得初等但较弱的 \(f(N)\le N\exp[-c\log N/\log\log N]=o(N)\)。
- 第一阻塞点：每个模 \(p^2\) 只损失约一半剩余类；在保持乘积模数 \(M\le N\) 时只能使用约 \(\log N/\log\log N\) 个素数，因此该独立 CRT 路线停在 \(N^{1-o(1)}\)，远达不到 \(N^{o(1)}\)，甚至弱于 Konyagin 的已知指数界。
- 下一步：在小规模数据上检验不同 \(p^2\) 的支撑是否存在额外相关性，例如同时达到近半支撑的集合是否会迫使另一素数平方出现禁和；若能证明跨模数的非乘积型损失，再尝试嵌入大筛。
- 来源核对：当前汇总及 Konyagin 界：https://www.erdosproblems.com/1109；问题页的有限计算也把候选元素先限制为奇平方自由数，与上述对角论证一致。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1109)；既有候选答案（按不可信材料审计）

### #1110

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $p>q\geq 2$ be two coprime integers. We call $n$ representable if it is the sum of integers of the form $p^kq^l$, none of which divide each other. If $\{p,q\}\neq \{2,3\}$ then what can be said about the density of non-representable numbers? Are there infinitely many coprime non-representable numbers?
- 题意摘要：固定互素整数 \(p>q\ge2\)。可表示数是某个有限和 \(n=\sum p^{a_i}q^{b_i}\)，其中 \(a_i,b_i\ge0\)，且任意两个求和项在整除关系下不可比较。问题在 \(\{p,q\}\ne\{2,3\}\) 时询问非表示数的密度，并问是否有无穷多个与 \(pq\) 互素的非表示数。
- 状态核对：一般问题仍开放。输入的 official_context 有一处方向性错误：Yu–Chen 证明的是指定参数范围内“可表示数”密度为 0，因而“非表示数”密度为 1；先前候选在这一点上反而是正确的。
- 初步判定：`partial`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：重建 \((p,q)=(2,3)\) 的强归纳，并精确定位它为何不能直接推广；同时把不可整除条件转为指数格点中的反链条件。
- 局部结论：两项 \(p^aq^b,p^{a'}q^{b'}\) 不可比较，当按 \(a\) 递增排列时其 \(b\) 必须严格递减；表示式对应 \(\mathbb N^2\) 中的有限反链。；对 \((2,3)\)，若 \(n=2m\) 就把 \(m\) 的表示整体乘 2；若 \(n\) 为奇数，取最大 \(3^j\le n\)，表示偶数 \(n-3^j\) 且令其各项均为偶数。因为 \(n-3^j<2\cdot3^j\)，这些项既不整除 \(3^j\)，也不被 \(3^j\) 整除。这严格重建了特例归纳。；已知 Yu–Chen 范围为：\(q>3\)，或 \(q=3,p>6\)，或 \(q=2,p>10\) 时可表示数密度 0；与 \(pq\) 互素的非表示数除可能的 \((5,2),(9,2),(5,3)\) 外均已知无穷（已排除 \((3,2)\) 特例）。
- 第一阻塞点：归纳的首要失败发生在选取单项修正余数：一般 \(n-q^j\) 未必被 \(p\) 整除；即使 \(p=2\)，当 \(q>3\) 时余数上界 \((q-1)q^j\) 也不再排除某个表示项被 \(q^j\) 整除。因此不能保持反链条件。
- 下一步：对三个遗留互素问题 \((5,2),(9,2),(5,3)\)，逐一枚举模 \(p^u q^v\) 的反链和，并寻找一个与 \(pq\) 互素且在提升 \((u,v)\mapsto(u+1,v+1)\) 时保持不可表示的剩余类。
- 来源核对：Yu–Chen 论文页明确写明 representable numbers 的渐近密度为零：https://www.sciencedirect.com/science/article/pii/S0022314X21003358；更新后的问题页亦使用正确方向，并列出参数范围：https://www.erdosproblems.com/1110；因此不能复述输入 official_context 中“非表示数密度零”的错误。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1110)；既有候选答案（按不可信材料审计）

### #1111

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：If $G$ is a finite graph and $A,B$ are disjoint sets of vertices then we call $A,B$ anticomplete if there are no edges between $A$ and $B$. If $t,c\geq 1$ then there exists $d\geq 1$ such that if $\chi(G)\geq d$ and $\omega(G)<t$ then there are anticomplete sets $A,B$ with $\chi(A)\geq \chi(B)\geq c$.
- 题意摘要：量词为：对每一对整数 \(t,c\ge1\)，是否存在只依赖于 \((t,c)\) 的 \(d\)，使每个有限图 \(G\) 若 \(\chi(G)\ge d\) 且 \(\omega(G)<t\)，就含两个不交且彼此无边的顶点集 \(A,B\)，并满足 \(\chi(G[A])\ge\chi(G[B])\ge c\)。交换名称后，结论等价于两边色数都至少 \(c\)。
- 状态核对：一般情形仍开放；\(c=2,3\) 已知。Nguyen–Scott–Seymour 2024 得到一边色数大、另一边最小度大的替代结论，但未解决原命题。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：尝试从 Nguyen–Scott–Seymour 的结论出发，把 \(A\) 的大最小度升级为大色数，再与已经满足 \(\chi(B)\ge c\) 的一边配对。
- 局部结论：\(c=1\) 可直接取 \(d=t\)：若 \(\chi(G)\ge t>\omega(G)\)，则 \(G\) 不是完全图，故有两个不相邻顶点，分别作为 \(A,B\)。；NSS 定理确实给出 anticomplete 的 \(A,B\)，其中 \(\chi(B)\ge c\) 且 \(\delta(G[A])\ge C\)，这里 \(C\) 可预先任意指定。；仅靠 \(\delta(G[A])\ge C\) 与 \(\omega(G[A])<t\) 不能推出 \(\chi(G[A])\ge c\)：当 \(t\ge3\) 时，\(K_{C,C}\) 有任意大最小度、团数 2，却只有色数 2。
- 第一阻塞点：第一处断裂正是“高最小度推出高色数”；即使把 NSS 参数取得任意大，该推论仍被完全二部图否定。必须利用 \(A\) 在原高色数图中的额外生成结构，而不能只使用其最小度和团数。
- 下一步：阅读并抽取 NSS 构造中 \(A\) 的额外性质，检验其是否排除大型二部型结构；一个具体测试是判断构造出的 \(A\) 是否还具有某种局部色数或受限退化数下界。
- 来源核对：当前问题页及已知 \(c=2,3\) 界：https://www.erdosproblems.com/1111；NSS 论文书目信息及摘要：https://collaborate.princeton.edu/en/publications/on-a-problem-of-el-zahar-and-erd%C5%91s/；先前候选没有误称 NSS 已解决原题，但其所述额外“一边色数 3”路线未由本次核查来源确认，故未采用。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1111)；既有候选答案（按不可信材料审计）

### #1112

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $1\leq d_1<d_2$ and $k\geq 3$. Does there exist an integer $r$ such that if $B=\{b_1<\cdots\}$ is a lacunary sequence of positive integers with $b_{i+1}\geq rb_i$ then there exists a sequence of positive integers $A=\{a_1<\cdots\}$ such that\[d_1\leq a_{i+1}-a_i\leq d_2\]for all $i\geq 1$ and $(kA)\cap B=\emptyset$, where $kA$ is the $k$-fold sumset?
- 题意摘要：对每个固定参数 \(1\le d_1<d_2\)、\(k\ge3\)，问是否存在常数整数 \(r\)，使对每个满足 \(b_{i+1}\ge rb_i\) 的无限正整数序列 \(B\)，都能找到无限递增正整数序列 \(A\)，其每个相邻差落在 \([d_1,d_2]\)，且所有恰由 \(k\) 个 \(A\) 中元素组成的和均避开 \(B\)。
- 状态核对：不能作统一肯定回答：\((d_1,d_2,k)=(2,3,3)\) 已有反例，故 \(r_3(2,3)\) 不存在；其他一般参数的分类仍开放。先前候选对此判断正确。
- 初步判定：`counterexample`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：直接把 Bollobás–Hegyvári–Jin 的变比率反例归约成任意固定比率 \(r\) 的反例，核对其量词是否真正否定所求 \(r\)。
- 局部结论：已知定理断言：对任意递增整数序列 \(r_i\)，存在 \(B\) 满足 \(b_{i+1}\ge r_i b_i\)，且每个相邻差为 2 或 3 的无限序列 \(A\) 都满足 \(3A\cap B\ne\varnothing\)。；给定任意候选常数 \(r\)，取严格递增的 \(r_i=r+i\)。所得 \(B\) 自动满足 \(b_{i+1}\ge rb_i\)，但不存在避开 \(B\) 的允许序列 \(A\)。；因此量词严格推出：不存在 \(r_3(2,3)\)。这是否定一般全称肯定答案的真实反例，而非仅仅计算证据。
- 第一阻塞点：该构造目前只严格否定特定参数；从 \(3A\cap B\ne\varnothing\) 不能直接推出 \(kA\cap B\ne\varnothing\)（\(k>3\)），也不能在缩放后自动保持任意给定的间隙区间 \([d_1,d_2]\)。因此无法据此完成全部参数分类。
- 下一步：首先检验 BHJ 构造对仿射变换 \(A\mapsto uA+v\) 的稳定性，明确哪些 \([d_1,d_2]\) 可由 \([2,3]\) 转移；同时单独检查增加求和项数时能否相应平移或扩张 \(B\)。
- 来源核对：当前问题页明确给出变比率反例及 \(r_3(2,3)\) 不存在：https://www.erdosproblems.com/1112；BHJ 论文书目与机构记录：https://digitalcommons.memphis.edu/facpubs/5256/；“一般问题开放”应理解为其他参数的存在性分类开放，不能覆盖掉已经解决的否定参数。
- 时间记账：所在批次墙钟时间按题数均摊约 58.0 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1112)；既有候选答案（按不可信材料审计）

### #1113

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：A positive odd integer $m$ such that none of $2^km+1$ are prime for $k\geq 0$ is called a Sierpinski number. We say that a set of primes $P$ is a covering set for $m$ if every $2^km+1$ is divisible by some $p\in P$. Are there Sierpinski numbers with no finite covering set of primes?
- 题意摘要：问是否存在正奇数 m，使得对每个 k≥0，N_k=m2^k+1 都是合数，但不存在有限素数集 P 满足：对每个 k，至少一个 p∈P 整除 N_k。
- 状态核对：截至所给状态日期仍开放。候选 m=734110615000775^4 已知是 Sierpiński 数，但“无有限覆盖”只有证据，没有证明；先前候选对此区分基本正确。
- 初步判定：`promising`；证明尝试：`rigorous_partial`；可行性 `4/10`；置信度 `high`
- 尝试路线：把问题归约为最小素因子的无界性，并检验第四幂候选的代数分解机制。记 q_k=P^-(m2^k+1)。对 m=a^4 及 k=4t+2，令 y=a2^t，则 m2^k+1=4y^4+1=(2y^2-2y+1)(2y^2+2y+1)，所以该无限子序列确为合数。
- 局部结论：对 Sierpiński 数 m，存在有限覆盖集当且仅当序列 P^-(m2^k+1) 有界：有限覆盖立即给出上界；反之，取不超过该上界的全部素数即得有限覆盖。；固定奇素数 p。若 p∤m，则 p∣m2^k+1 等价于 2^k≡-m^{-1} (mod p)，故可行的 k 构成模 ord_p(2) 的一个剩余类，或为空；若 p∣m，则它不整除任何 m2^k+1。；第四幂分解只证明 k≡2 (mod 4) 时有随 t 增长的非平凡因子，并不推出最小素因子增长。
- 第一阻塞点：第一处缺口是：无法证明对任意有限素数集 P，都存在 t 使得两个因子 2y^2±2y+1 均避开 P。各个 p 给出的周期性坏剩余类可能由有限多个 p 覆盖全部 t；因子的数值增长不能排除固定小素因子轮流出现。
- 下一步：对候选 a=734110615000775，逐个计算每个小素数 p 在 k 上对应的剩余类，并对界 B 严格验证存在 k 使 P^-(a^4·2^k+1)>B；同时寻找能证明这些坏类不可能形成有限覆盖的结构性条件。有限个 B 的计算只是证据，不是最终证明。
- 来源核对：[Erdős Problems #1113](https://www.erdosproblems.com/1113) 明确记录开放状态及候选第四幂。；[Filaseta–Finch–Kozek 论文](https://www.whittier.edu/sites/default/files/media/academics/math/Kozek_Sierpinski_JNTdraft%282008%29.pdf) 明言证明任何例子不能来自有限覆盖仍超出其方法。
- 时间记账：所在批次墙钟时间按题数均摊约 68.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1113)；本地 Lean：`/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1113.lean`；既有候选答案（按不可信材料审计）

### #1117

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f(z)$ be an entire function which is not a monomial. Let $\nu(r)$ count the number of $z$ with $\lvert z\rvert=r$ such that $\lvert f(z)\rvert=\max_{\lvert z\rvert=r}\lvert f(z)\rvert$. (This is a finite quantity if $f$ is not a monomial.) Is it possible for\[\limsup \nu(r)=\infty?\]Is it possible for\[\liminf \nu(r)=\infty?\]
- 题意摘要：固定一个非单项式整函数 f。ν_f(r) 是圆 |z|=r 上达到最大模 M_f(r) 的点数。第一问要求存在 f 使 limsup_{r→∞}ν_f(r)=∞；第二问要求存在 f 使对每个 N，某个 R 后所有 r≥R 都有 ν_f(r)≥N。
- 状态核对：第一问已由 Herzog–Piranian 肯定解决；第二问仍开放。因此整题标为 open，但不能把第一问也当作未解决。
- 初步判定：`partial`；证明尝试：`known_theorem`；可行性 `3/10`；置信度 `high`
- 尝试路线：从显式块 g_d(z)=1+z^d 出发：在任意 r>0 上，|g_d(re^{iθ})| 的最大值恰在 e^{idθ}=1 时达到，故 ν_{g_d}(r)=d。尝试把 d→∞ 的块粘贴到依次外移的环带，以构造单个整函数。该思路解释了已知 limsup 构造，也与近似最大模论文的拼接路线相符。
- 局部结论：单个块 g_d 在每个圆上恰有 d 个最大模点，说明“大量最大点”本身没有局部解析障碍。；Herzog–Piranian 已构造一个整函数满足 ν(n)=n（每个正整数半径），从而严格推出 limsup_{r→∞}ν(r)=∞。；若只把各环带上的模型控制到一致误差 ε，则至多得到许多彼此分离的近最大弧；连续函数完全可能在这些弧中只有一个真正的全局最大点。
- 第一阻塞点：第一处无法闭合之处是误差稳定性：条件“某点等于全圆最大值”不是在一致近似下稳定的。粘贴误差会打破 g_d 的 d 重旋转对称性，而跨越所有大半径维持越来越高的精确对称性正是 liminf 问题的核心困难。
- 下一步：寻找带严格比较余量的解析块：在每个大圆上预先指定 N 个点，并证明它们的模完全相等且严格压过其余圆周；随后检验这种等值约束能否在 Hörmander/整函数逼近步骤中被精确插值保留，而不只是 ε-保留。
- 来源核对：[Erdős Problems #1117](https://www.erdosproblems.com/1117) 记录第一问肯定、第二问开放。；[Glücksam–Pardo-Simón](https://arxiv.org/abs/2208.11154) 明确记载 Herzog–Piranian 的 ν(n)=n，并说明其近似构造不能保证真正最大点数趋于无穷。
- 时间记账：所在批次墙钟时间按题数均摊约 68.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1117)；既有候选答案（按不可信材料审计）

### #1119

- 当前状态：`independent`（冻结清单状态：`open`）
- 精确题面：Let $\aleph_0<\mathfrak m<\mathfrak c$. If a family of entire functions takes at most $\mathfrak m$ distinct values at every fixed $z_0$, must the family have cardinality at most $\mathfrak m$?
- 题意摘要：固定无限基数 ℵ₀<m<c。命题问：对每个整函数族 F，若对每个 z∈C 都有 |{f(z):f∈F}|≤m，是否必有 |F|≤m？临界情形是 m^+=c。
- 状态核对：该命题在临界情形独立于 ZFC；并非所有参数区间都独立。当 m^+<c 时，ZFC 已能证明肯定答案。
- 初步判定：`independent`；证明尝试：`known_theorem`；可行性 `9/10`；置信度 `high`
- 尝试路线：先重建非临界证明，再说明临界处为何必须使用模型论。反设 F 含 m^+ 个不同整函数。对每对 f≠g，零点集 {z:f(z)=g(z)} 可数；全部坏点的并集大小至多 (m^+)^2·ℵ₀=m^+。若 m^+<c，可在并集外取 z，此时这 m^+ 个函数在 z 处两两取不同值，矛盾。
- 局部结论：上述论证严格证明：m^+<c 时必有 |F|≤m。解析部分只使用非零整函数的零点集离散、因而可数。；临界情形 m^+=c 时，坏点并集的基数上界也是 c，不能再从 C 中选出遗漏点；这正是初等论证失效的第一处。；当 c=ℵ₂、m=ℵ₁ 时，Kumar–Shelah 给出肯定答案的模型；Schilhan–Weinert 给出另一个具有大小 c 的 Wetzel 族的模型，其中每点值集小于 c，故答案为否。
- 第一阻塞点：这里不是尚待补上的 ZFC 技巧：在 m^+=c 时，肯定与否定模型都已构造。任何继续尝试无条件 ZFC 证明都会与独立性结果冲突。
- 下一步：若需完整核对，应逐项审计两种 forcing 扩张：验证保留 c=ℵ₂，并把“每点少于 c 个值”的 Wetzel 族准确对应为本题 m=ℵ₁ 的逐点上界；同时核对肯定模型排除了所有大小 c 的此类函数族。
- 来源核对：[Erdős Problems #1119](https://www.erdosproblems.com/1119) 明确给出 m^+<c 的正结论及 c=ℵ₂ 临界情形的两个相反模型。；[Kumar–Shelah](https://www.impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/239/3/92174/on-a-question-about-families-of-entire-functions) 的结果表述为在 ZFC+¬CH 下该类 continuum-sized 函数族的存在不可判定。；[Schilhan–Weinert](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.12918) 构造与 c=ℵ₂ 相容的 Wetzel 族。
- 时间记账：所在批次墙钟时间按题数均摊约 68.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1119)

### #1120

- 当前状态：`open`（冻结清单状态：`open`）
- 精确题面：Let $f\in \mathbb{C}[z]$ be a monic polynomial of degree $n$, all of whose roots satisfy $\lvert z\rvert\leq 1$. Let\[E= \{ z : \lvert f(z)\rvert \leq 1\}.\]What is the shortest length of a path in $E$ joining $z=0$ to $\lvert z\rvert =1$?
- 题意摘要：对每个满足条件的次数 n 首一多项式 f，先定义 ℓ(f) 为 E={|f|≤1} 内从 0 到单位圆任一点的可求长曲线长度下确界；研究对象应是最坏值 L_n=sup_f ℓ(f)，而不是 inf_f ℓ(f)。
- 状态核对：最坏情形 L_n 的增长仍开放。先前候选给出的“答案 1”只计算了 inf_f ℓ(f)，并非官方语境中的主要极值问题；这一量词误读必须明确排除。Clunie–Netanyahu 的未刊交流结果保证每个 f 都存在所需路径。
- 初步判定：`blocked`；证明尝试：`rigorous_partial`；可行性 `5/10`；置信度 `high`
- 尝试路线：尝试从包含 0 的子水平集分支出发，先做可严格验证的度量基例，再考虑沿 |f| 的下降线或分支树控制内在距离。由于 f(0)=(-1)^n∏a_j，故 |f(0)|≤1，起点确在 E 中。
- 局部结论：任何从 0 到 |z|=1 的可求长曲线长度至少为 1，因此 ℓ(f)≥1。；f(z)=z^n 时 E 是闭单位圆盘，ℓ(f)=1；这只证明 inf_f ℓ(f)=1 以及 L_n≥1。；n=1 时 f(z)=z-a、|a|≤1，E是以 a 为圆心的单位闭盘。取 a 的方向上的单位圆点（a=0 时任取），从 0 到该点的径向线段留在 E，故 L_1=1。相同论证也适用于 f=(z-a)^n。
- 第一阻塞点：第一处缺口是从拓扑连通性到长度控制：即使已知 0 所在的 E 分支接触单位圆，也没有得到其内在最短路长度的 n-依赖上界。沿梯度线可能靠近临界点或狭窄通道并产生很大绕行，现有局部估计不能排除这一点。
- 下一步：先解决可检验的 n=2 子问题：把 f=(z-a)(z-b) 归一化到中点坐标，分类 Cassini 卵形线的连通情形，并显式估计包含 0 的分支到单位圆的内在距离；这可产生 L_2 的严格上界或具体反例形状。
- 来源核对：[Erdős Problems #1120](https://www.erdosproblems.com/1120) 明确说明路径存在、平凡下界为 1，而目标是 degree n 下的最坏情形。；未发现 Clunie–Netanyahu 个人通信证明的公开原文，因此这里只采用官方页面记录的定理结论，没有伪造其证明细节。
- 时间记账：所在批次墙钟时间按题数均摊约 68.1 秒；批次硬上限 1800 秒。
- 来源：[官方题页](https://www.erdosproblems.com/1120)；既有候选答案（按不可信材料审计）
