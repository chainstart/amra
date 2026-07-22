# Erdős #788：来源纠错与固定/缓增秩 GAP 公共证书

日期：2026-07-22（Asia/Hong_Kong）

## 结论边界

原题仍开放。本轮没有证明 \(f(n)\le n^{1/2+o(1)}\)，也没有触发 Q2。
旧路线的主要数学代入成立，但 Sanders 来源的定理编号有一处可复核的错误。
新方向把此前只对一维 AP 的“公共 restricted-sum 证书”推广到任意有限母集，
并对固定秩 2-proper GAP 给出显式线性证书。这使随机构造可以一次排除所有
在固定秩 GAP 中密度严格大于 \(1/2\) 的候选，而无需枚举删点模式。

## 旧路线的敌对审计

题面严格等价于

\[
 f(n)=\min_{B\subset(2n,4n)\cap\mathbb N}
       \bigl(|B|+\alpha(G_B)\bigr),
\]

其中顶点集为 \((n,2n)\cap\mathbb N\)，不同顶点 \(x,y\) 相邻当且仅当
\(x+y\in B\)。旧轮使用
\(B_p\cap(C\mathbin{\hat+}C)=\varnothing\) 描述独立集，开区间端点和
“不同两点”的 restricted 条件均一致。

逐项重读一手定理后结论如下。

1. Shao--Xu Theorems 1.1、1.2 的条件确为
   \(n\ge\max(3,2\varepsilon^{-1/2})\)、缺边至多 \(\varepsilon n^2\)，
   AP 长度上界中的误差确为 \(5\sqrt\varepsilon n\)。取
   \(\Gamma=\{(a,b):a\ne b\}\)、\(\varepsilon=1/s\) 合法。
2. Wang--Tang 的 Theorem D 确实给正规化整数集的二分
   \(l+s-2\)（\(l\le2s-5\)）与 \(3s+o(s)\)
   （\(l\ge2s-4\)）；其 Theorem 1.5 确实覆盖
   \(2s-4\le l\le2s-3\) 并给 \(3s-7\)。所以第七轮固定
   \(3-\delta\) 分支的量词没有越界。
3. Sanders 的定量 restricted/full 比率在任意 Abelian 群上误差指数为
   \(1/3\)，所以第七轮的式 (Q1)--(Q4) 数学上可用；但报告把它标成了
   **Theorem 1.3**。原文 Theorem 1.3 是旧的 \(1/6\) 指数，改进后的
   \(1/3\) 指数是 **Theorem 1.5**。这是明确书目错误，不推翻后续不等式。

因此没有发现让旧分支结论失效的逻辑或适用范围破绽；修正后的剩余缺口仍是
\(|C\hat+C|\) 在临界 \(3|C|\) 以上的高熵候选。

来源：[Shao--Xu](https://arxiv.org/abs/1711.11060)；
[Wang--Tang](https://cdm.ucalgary.ca/article/download/75917/58188/265017)；
[Sanders, Theorems 1.3 and 1.5](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DE03DE700464C1CC8D3C4F845D961018/S0013091506001398a.pdf/threeterm_arithmetic_progressions_and_sumsets.pdf)；
[Erdős Problems #788](https://www.erdosproblems.com/788)。

## 新方向一：任意母集的精确 matching 公式

设 \(P\) 是无 2-torsion 群中的有限集，\(|P|=V\)，固定 \(s\le V\)，
并令 \(m=V-s\)。对和 \(t\) 记

\[
 \nu_P(t)=\#\{\{x,y\}\subset P:x\ne y,\ x+y=t\}.
\]

则有精确恒等式

\[
 \boxed{
 \bigcap_{\substack{C\subseteq P\\|C|=s}}
 (C\mathbin{\hat+}C)
 =\{t:\nu_P(t)>m\}.}
 \tag{1}
\]

证明：对固定 \(t\)，所有边 \(\{x,t-x\}\) 两两不交，构成一个有
\(\nu_P(t)\) 条边的 matching。从 \(P\) 删除 \(m\) 点后仍必留下一条边，
当且仅当 \(m<\nu_P(t)\)。若 \(m\ge\nu_P(t)\)，每条边删一个端点，再任意
补足到 \(m\) 个删点，即构造出不表示 \(t\) 的 \(s\)-集。此前 AP 公式只是
(1) 对一维区间的特例。

这个公式同时说明普遍的半密度硬边界：任何 matching 至多有
\(\lfloor V/2\rfloor\) 条边，所以 \(s\le\lceil V/2\rceil\) 时一般不能
期待非空的“只依赖母集”的证书。

## 新方向二：2-proper GAP 的显式中心证书

令

\[
 \mathcal P=\left\{a+\sum_{i=1}^r x_i d_i:
 0\le x_i<L_i\right\}
 \tag{2}
\]

为 2-proper GAP，即坐标和盒
\(0\le t_i\le2L_i-2\) 到整数和仍为单射。写
\(V=\prod_iL_i\)，并把 \(C\subseteq\mathcal P\) 拉回坐标盒。
对坐标和 \(t=(t_1,\ldots,t_r)\)，有序表示数精确为

\[
 R(t)=\prod_{i=1}^r
 \left(L_i-|t_i-(L_i-1)|\right).                    \tag{3}
\]

对角表示至多一个，故 \(R(t)\ge2m+2\) 蕴含
\(\nu_{\mathcal P}(t)>m\)。令

\[
 \theta=\left(\frac{2m+2}{V}\right)^{1/r},\qquad
 q_i=\lceil\theta L_i\rceil.                         \tag{4}
\]

只要 \(2m+2\le V\)，所有满足

\[
 L_i-|t_i-(L_i-1)|\ge q_i\quad(1\le i\le r)         \tag{5}
\]

的和由 (1) 共同属于每个 \(s\)-点子集的 restricted sumset。这个中心盒
的精确大小是

\[
 \boxed{|F_{\mathcal P,s}|=
 \prod_{i=1}^r\bigl(2(L_i-q_i)+1\bigr).}             \tag{6}
\]

特别地，若固定 \(r\) 和 \(\varepsilon>0\)，且
\(s\ge(1/2+\varepsilon)V\)、\(V\ge2/\varepsilon\)，则

\[
 \theta^r\le1-\varepsilon,
\]

而对每个 \(i\)，
\(2(L_i-q_i)+1\ge(1-\theta)L_i\)。因此

\[
 \boxed{|F_{\mathcal P,s}|\ge
 c_{r,\varepsilon}V,\qquad
 c_{r,\varepsilon}=
 \left(1-(1-\varepsilon)^{1/r}\right)^r>0.}          \tag{7}
\]

这是一条真正的固定秩推广，不假设 \(C\) 本身是 AP，也不枚举
\(\mathcal P\setminus C\) 的 \(\Theta(s)\) 种删点。

## 对随机上界路线的严格推论

固定 \(R\) 与 \(\varepsilon>0\)。在题目顶点区间内，秩至多 \(R\) 的
2-proper GAP 可由 \(a,d_1,\ldots,d_r,L_1,\ldots,L_r\) 描述；去掉
\(L_i=1\) 的冗余维后，每个参数均为 \(O(n)\)，故总数至多
\(O_R(n^{2R+1})\)。

取

\[
 p=\sqrt{\frac{\log n}{n}},\qquad
 s=Dp^{-1}\log n.
\]

令 \(c_*:=\min_{1\le r\le R}c_{r,\varepsilon}>0\)。对每个固定 GAP，
式 (7) 的证书被随机 \(B_p\) 完全漏掉的概率至多

\[
 \exp(-p c_*s)=n^{-c_*D}.
\]

所以当 \(D>(2R+2)/c_*\) 时，并合界证明：以高概率不存在
任何大小 \(s\)、且在某个秩至多 \(R\) 的 2-proper GAP 中密度至少
\(1/2+\varepsilon\) 的独立集。与此同时 Chernoff 给
\(|B_p|=O(\sqrt{n\log n})\)。

固定缺口还可定量放宽为缓慢趋零。若
\(s\ge(1/2+\delta)V\)、\(V\ge2/\delta\)，则

\[
 \theta^r\le1-\delta,
 \qquad
 1-\theta\ge1-(1-\delta)^{1/r}\ge\frac\delta r.
\]

最后一步是凹函数 \(x^{1/r}\) 在 \(x=1\) 的切线界。故对所有
\(1\le r\le R\)，

\[
 |F_{\mathcal P,s}|\ge(\delta/r)^rV
 \ge(\delta/R)^RV.                                  \tag{8}
\]

令 \(\delta=\delta_n\) 且 \(\delta_n^{-R}=n^{o(1)}\)，再取

\[
 s=D(R/\delta_n)^Rp^{-1}\log n.                     \tag{9}
\]

则每个证书的漏选概率至多 \(n^{-D}\)，仍压过
\(O_R(n^{2R+1})\) 个参数，而 (9) 仍为 \(n^{1/2+o(1)}\)。所以该固定秩
结构化分支甚至容许密度从 \(1/2\) 只拉开任意次多项式缺口；不能处理的是真正
\(1/2+o(1)\) 且其倒数损失不再为次多项式的边界，以及根本没有这种容器的
集合。

同一账本也允许秩缓慢增长。令 \(R=R_n\)、\(0<\delta=\delta_n\le1/2\)，
并考虑秩 \(r\le R\)、密度至少 \(1/2+\delta\) 的 2-proper GAP 容器。去掉
冗余边长 1 后，落在题目区间内的每个基点、步长和边长均为 \(O(n)\)，故容器
总数至多 \((Cn)^{2R+1}\)。由 (8)，每个候选的公共证书至少有
\((\delta/R)^R s\) 项。仍取 \(p=\sqrt{\log n/n}\)，但改令

\[
 s=D R(R/\delta)^R p^{-1}\log n.                   \tag{10}
\]

则单个漏选概率至多 \(\exp(-DR\log n)=n^{-DR}\)，固定充分大 \(D\) 后仍压过
全部 \((Cn)^{2R+1}\) 个参数。若

\[
 \log R+R\log(R/\delta)=o(\log n),                 \tag{11}
\]

式 (10) 仍为 \(n^{1/2+o(1)}\)。因此“固定秩”可严格放宽到满足 (11) 的
缓慢增长秩；半密度和容器存在性这两个真正缺口没有改变。

这严格扩大第七轮只排除短 AP 的结构分支，但还不能闭合原题：现有一般
Freiman 型逆定理只保证危险集合落入体积 \(O_K(s)\) 的 bounded-rank GAP，
并不自动给体积小于 \((2-o(1))s\)、2-proper 性和统一的
\(1/2+\varepsilon\) 密度。临界密度 \(1/2\) 又由 (1) 的 matching
上界表明是本证书机制的真实边界，而不是并合界常数。

下一精确桥接命题是：对 \(|C\hat+C|\le K|C|\) 的整数集，证明一个稳定
二分——要么存在体积 \(<(2-\varepsilon)|C|\) 的固定秩 2-proper GAP
容器，要么 \(C\hat+C\) 含有另一个仅有 \(n^{O_K(1)}\) 种可能的线性大
证书。当前没有该稳定二分。

## 结构化分支究竟闭合到哪里

令 \(\mathcal C_{R,\varepsilon}(s,n)\) 为题目顶点区间中所有 \(s\)-集
\(C\)，满足：存在秩至多 \(R\) 的 2-proper GAP \(\mathcal P\) 包含
\(C\)，且 \(|C|\ge(1/2+\varepsilon)|\mathcal P|\)。上面的并合界已经
**完整闭合这个精确定义的分支**：取足够大的常数 \(D(R,\varepsilon)\)，
随机 \(B_p\) 以高概率不含任何来自
\(\mathcal C_{R,\varepsilon}(s,n)\) 的独立集。

但这不等于闭合 Sanders 后剩下的全部结构化候选：

1. Sanders/Wang--Tang 已无条件处理的是
   \(|C\hat+C|<3s-o(s)\)，并把它送入一维 AP；本轮没有改善这个任意集合
   阈值。
2. 一般固定 doubling 的 Freiman 逆定理虽给 bounded-rank、体积
   \(O_K(s)\) 的 progression 容器，却不保证常数小于 2，也不自动保留
   2-proper 的相同体积。因此容器密度可能低于 \(1/2\)。
3. 这个差距不能靠调并合界常数消掉。式 (1) 表明，当
   \(s\le\lceil|\mathcal P|/2\rceil\) 时，任何只依赖整个母集、对所有删点
   模式共同有效的证书必为空。

所以本轮严格新增的是 Sanders 窗口之外一个“高于半密度的 2-proper 盒”
子类（并包含满足 (11) 的缓增秩），而不是一般 \(M\approx3s\) 或全部
bounded-doubling 分支。

## 查重与新颖性边界

式 (1) 只是“固定和的表示图是 matching，最小 vertex cover 等于边数”
的一行推论，应视为标准 matching/folklore，而不是候选论文主定理。式
(3)--(7) 是对 2-proper 盒的显式 tent-count 代入，随机结论又只是参数计数
加 union bound；本轮不对其文献新颖性或优先权作任何声明。

定向检索未找到逐字相同的“全部稠密 GAP 子集的公共 restricted-sum 交集”
表述，但检索不到不构成新颖性证据。近期
[Ouyang 的 bounded-degree relation restricted-sumset 工作](https://arxiv.org/abs/2503.09121)
也使用 matching 术语，不过其对象是在 \(A\times B\) 中删除一个 bounded-
degree relation 后估计单个 restricted sumset；它不是这里对全部删点模式取
交的命题。这个差别只用于防止误引，不足以支持首创性判断。

## 有限核验

`gap_certificate_audit.py` 先对九个指定小盒给出明细，再系统枚举秩 1 至 3、
体积不超过 14 的 31 个盒和全部 285 个“盒--子集大小”实例。逐集合核验
(1)，并核验 (4)--(6) 给出的中心盒确为其子集；半密度以下非空交集为零例。
有限计算只作回归测试，一般证明是上面的 matching 论证。

状态：`route_advanced`；`full_solution_claim = none`；Q2 门槛未达。
