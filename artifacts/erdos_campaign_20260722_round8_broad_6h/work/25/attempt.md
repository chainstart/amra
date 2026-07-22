# Erdős #25 第八轮：路线尸检与 profinite 平移的遍历定理

日期：2026-07-22（Asia/Hong_Kong）

## 结论边界

原题仍未闭合；`full_solution_claim = none`。本轮没有在第七轮的
pairwise-Carleson 和式上继续优化，而改从 profinite 概率空间上的 first-kill
停时出发。得到一个严格的平均平移定理：任意给定系统在几乎每个相容共同
平移下，所得集合甚至有自然密度，且密度就是有限筛密度的极限。

进一步的敌对复核把证明压缩为一个更强的确定性判据：只要无限 survivor
闭集沿指定轨道是 Haar-generic，结论就成立；若该闭集的边界 Haar 测度为
0，则**每个**共同平移都成立。特别地 (d_*=0) 的情形对原题任意指定系统
直接成立。剩余困难只可能出现在正测度、正测度边界的 survivor 集。

这不是原题，因为原题要求每个确定的剩余类系统，亦即必须包括可能异常的
指定平移。新定理把缺口准确定位为“从 Haar 几乎处处轨道升级到每条轨道”的
异常点问题。

## 1. 历轮路线尸检

逐式复核第二至第七轮的接口后，分类如下。

1. 缩放普适性、first-kill 分解、周期单侧调和界、共同 quotient 的单后代
   收费，以及第七轮固定祖先 gcd 和式都未发现逻辑或量词错误。
2. 第三轮的 `(PC)` 与第四轮的 `(HT)` 曾被当作候选充分条件，后续各自有
   显式系统证明它们不是普遍必要条件；它们已在原报告中正确退役，不能再把
   “尚未证明”误写成当前缺口。
3. 第六轮收费只覆盖共同复合 quotient 的单个后代；第七轮又证明裸
   ancestor--descendant 两两收费具有正的逐尺度主项。这里是可证明的结构性
   屏障，不是证明链错误。
4. 第七轮 Shannon 尾引理本身正确，但它是“若能把复用降到熵尺度则闭合”的
   后处理，尚无从任意 cylinder forest 到该熵量的无条件桥。

官网题面仍要求任意严格递增模数和任意指定剩余类；有限计算、随机剩余类或
几乎处处平移都不能替代这个全称量词。

## 2. Profinite first-kill 空间

令 \(\widehat{\mathbb Z}\) 带 Haar 概率 \(\mu\)，把
\(R_i=\{x:x\equiv a_i\pmod {n_i}\}\) 视为其中的 clopen cylinder。写

\[
 B_K=\widehat{\mathbb Z}\setminus\bigcup_{i\le K}R_i,
 \qquad d_K=\mu(B_K),\qquad d_*=\lim_Kd_K,
\]

并记无限 survivor 闭集

\[
 B_\infty=\bigcap_{K\ge1}B_K,\qquad \mu(B_\infty)=d_*.
\]

以及互不相交的 full first-kill atoms

\[
 F_i=B_{i-1}\cap R_i,qquad e_i=\mu(F_i)=d_{i-1}-d_i.
\]

于是对每个 \(K\)，可测尾集

\[
 F_{>K}=\bigcup_{i>K}F_i
\]

满足

\[
 \mu(F_{>K})=\sum_{i>K}e_i=d_K-d_*.                 \tag{1}
\]

对 \(z\in\widehat{\mathbb Z}\)，同时把所有剩余类平移为
\(R_i^{(z)}=z+R_i\)。它们在每个模 \(n_i\) 上相容，而且相应 first-kill
atom 恰为 \(z+F_i\)。令 \(A_z\subset\mathbb N\) 是按原题的激活规则
得到的集合。

## 3. 几乎处处共同平移定理

**定理。** 对 Haar 几乎每个 \(z\in\widehat{\mathbb Z}\)，集合 \(A_z\)
的自然密度存在，并等于 \(d_*\)。因而其对数密度也存在并等于 \(d_*\)。

**证明。** 平移 \(T:x\mapsto x+1\) 在 \(\widehat{\mathbb Z}\) 上遍历：
任一在 \(T\) 下不变的字符必须在稠密循环子群 \(\mathbb Z\) 上平凡，故是
平凡字符。Birkhoff 遍历定理用于 \(1_{B_\infty}\)，得到对 Haar 几乎每个
\(z\) 有

\[
 \lim_{X\to\infty}\frac1X
 \sum_{m\le X}1_{B_\infty}(m-z)=d_*.                \tag{2}
\]

另一方面，有限筛 \(B_K^{(z)}=z+B_K\) 是周期集，对每个 \(z\) 都有自然
密度 \(d_K\)。避开全部 cylinder 的正整数当然不会被任何已激活类删除；
而当 \(m\ge n_K\) 时，前 \(K\) 个类均已激活。因此有夹逼

\[
 (z+B_\infty)\cap\mathbb N\subseteq A_z,
 \qquad
 A_z\cap[n_K,\infty)\subseteq(z+B_K)\cap\mathbb N. \tag{3}
\]

这里第二个包含式中的有限截断不可省略：对 \(m<n_K\)，未激活的前 \(K\)
个类尚不能删除 \(m\)。它不影响任何渐近密度。由 (2)--(3)，

\[
 d_*\le\underline d(A_z)
 \le\overline d(A_z)\le d_K.
\]

令 \(K\to\infty\) 即得
\(\underline d(A_z)=\overline d(A_z)=d_*\)。自然密度存在蕴含同值的对数
密度。证毕。

同一证明给出不含概率量词的判据：对任意指定 \(z\)，只要
\(1_{B_\infty}(m-z)\) 的轨道平均存在且等于 \(d_*\)，就有
\(d(A_z)=d_*\)。又因 \(+1\) 在 \(\widehat{\mathbb Z}\) 上唯一遍历，若
\(\mu(\partial B_\infty)=0\)，则可用内外 clopen 集夹逼
\(1_{B_\infty}\)，其轨道平均对所有起点均收敛到 \(d_*\)。故：

\[
 \boxed{\mu(\partial B_\infty)=0
 \Longrightarrow d(A_z)=d_*\text{ 对每个 }z.}       \tag{4}
\]

当 \(d_*=0\) 时，甚至无需 (2)：(3) 的上界给
\(\overline d(A_z)\le d_K\to0\)，所以任意指定原系统都有自然密度 0。

激活补偿还可写成一个逐点精确式。令

\[
 k(m)=\max\bigl(\{0\}\cup\{i:n_i\le m\}\bigr),\qquad B_0=\widehat{\mathbb Z}.
\]

因模数严格递增，时刻 \(m\) 已激活的类恰为前 \(k(m)\) 个，所以

\[
 1_{A_z}(m)=1_{B_{k(m)}}(m-z),
 \qquad
 1_{A_z}(m)-1_{B_\infty}(m-z)
 =1_{B_{k(m)}\setminus B_\infty}(m-z).             \tag{5}
\]

特别地，Haar 平均下激活 fringe 的有限区间密度精确为

\[
 \int\frac1X\sum_{m\le X}
 1_{B_{k(m)}\setminus B_\infty}(m-z)\,d\mu(z)
 =\frac1X\sum_{m\le X}(d_{k(m)}-d_*)\longrightarrow0. \tag{6}
\]

最后一步只用 \(k(m)\to\infty\) 和 Cesàro。式 (6) 单独给出 Haar-
\(L^1\)（从而依概率）消失；再与 (2)--(3) 结合，也得到 Haar-a.e. \(z\) 的
fringe 自然密度为 0。但对指定 \(z\)，(5) 是一个沿该轨道的
shrinking-target 问题，不能从 (6) 把 Haar 平均直接换成逐点结论。

## 4. 正测度边界与异常轨道确实可以发生

上述 every-orbit 缺口不是纯技术措辞。给定 \(\varepsilon>0\)，枚举全部
正整数为 \(b_1,b_2,\ldots\)，递归选择严格递增模数 \(n_i>b_i\)，并使
\(\sum_i1/n_i<\varepsilon\)。取

\[
 R_i=\{x:x\equiv b_i\pmod{n_i}\}.
\]

则 union bound 给

\[
 \mu(B_\infty)\ge1-\sum_i\frac1{n_i}>1-\varepsilon,
\]

但每个正整数 \(b_i\) 都落入 \(R_i\)，故
\(B_\infty\cap\mathbb N=\varnothing\)。由于 \(\mathbb N\) 在
\(\widehat{\mathbb Z}\) 中稠密，\(B_\infty\) 没有内点；它是闭集，所以
\(\partial B_\infty=B_\infty\) 有正测度。于是 \(z=0\) 轨道上
\(1_{B_\infty}\) 的平均为 0，而 Haar 平均大于 \(1-\varepsilon\)。

这不是原题反例：原激活条件在 \(m=b_i\) 处读取为
“\(m<n_i\) 或不命中该类”；特意取 \(n_i>b_i\) 后第一项为真，所以虽然
\(b_i\notin B_\infty\)，它并不因第 \(i\) 类退出 \(A\)。只有后续同余点
\(b_i+kn_i\)（\(k\ge1\)）才由该类激活删除，且别的类还可能改变每个整数的
最终命运。因此该构造既未证明 \(A\) 无密度，也没有给出对数密度振荡。它严格
证明的只是：不能靠唯一遍历性把
可测 survivor 集的 a.e. 结论无条件升级到指定轨道；激活门槛正通过 (5) 的
shrinking-target fringe 补偿异常轨道，是尚需利用的额外算术信息。

## 5. 对原题的严格含义

该证明使用的不是独立随机选择各个 \(a_i\)，而是单个
\(z\in\widehat{\mathbb Z}\) 的相容共同平移；因此它保留原系统全部 gcd、
quotient 与 ancestor 结构。它表明这些结构在 Haar 典型轨道上已经足够，
真正缺口是排除指定轨道（特别是 \(z=0\)）成为正测度 survivor 集的
Birkhoff 异常点。

遍历定理对有正测度边界的闭集只给几乎处处，不能把 null exceptional set
删除。此前的 quotient
编程引理恰说明指定轨道可在有限尺度表现得极不典型，所以这里是结构性屏障，
不是一句“由遍历性”即可跨过的量词遗漏。

状态：严格平均平移定理；原题 OPEN；NO_Q2。
