# Erdős #679 第十轮：继承相位、固定幂目标与异常相位簇

日期：2026-07-22（Asia/Hong_Kong）

状态：**原题仍开放；没有得到确定性全区间传递；未达到 SCI 二区主结果门槛。**

## 1. 本轮结论

第九轮把未处理部分压到

\[
 D=X\exp(-2\Phi),\qquad \Phi={\log X\log_3X\over\log_2X}
\]

以上的 signed ANOVA 尾。本轮没有证明这个尾在实际二进制区间起点上足够小，
但把缺口进一步分成了三个严格层次：

1. 写出了保留 interval length、suffix endpoint 与 inherited phase 的精确状态及
   primitive Fourier 公式；
2. 把所需估计从“相对完整周期主项”降低为任意固定负幂的加法估计；
3. 无条件证明该固定幂估计对完整 CRT 周期中除多项式稀疏集合外的所有起点成立，
   并证明一个原题候选会迫使一个明确的超多对数长异常相位簇。

剩余缺口因此是确定性的异常相位反聚集，而不是典型相位或完整周期能量。

## 2. 精确继承相位与不可取绝对值的前沿

对 \(I=(A,A+N]\)、crossing conductor \(c<N\) 及 \(r\bmod c\)，置

\[
 L_r=\left\lfloor{A-r\over c}\right\rfloor,
 \quad u_r=r+cL_r.
\]

则 \(u_r\) 恰好遍历 \((A-c,A]\) 中的 \(c\) 个连续整数，变换后的后缀禁集为

\[
 {\cal B}_{p,r,c}=c^{-1}({\cal A}_p-u_r)\pmod p.     \tag{1}
\]

这证明后缀相位来自同一个继承基点，而不是可以独立任取的禁余数集。

另一方面，在 \(z\) 下方可构造次数
\(d=L_2-2L_3+O(1)\) 的窄带 crossing frontiers。若在使用联合
\((r,T)\) 相位前逐前沿取绝对值，则其归一化代价至少为

\[
 X^{qC(1-o(1))}\exp\{L_2+o(L_2)\}.                  \tag{2}
\]

(2) 不是实际 signed tail 的下界；它严格排除的是“先逐 \(T\) 取绝对值、再估
后缀”的架构。敌对 QA 还修复了这里的取整点：次数必须取
\(\lceil\log D/\log z\rceil+1\)，否则极小分数部分可能让辅助带越过 \(z\)。

## 3. 固定负幂已经足够

对固定矩阶 \(q\)，候选事件满足

\[
 1_{\rm good}\le t^{-qR}W^q,
 \qquad t^{-qR}=X^{o(1)}.                             \tag{3}
\]

第九轮低导传递对固定 \(q\) 同样成立，而

\[
 \sum_I{\cal L}_{D,q}=N\mu_q(1+O(e^{-\Phi})),
 \qquad \mu_q=X^{-qC+o(1)}.                          \tag{4}
\]

故只要 \(qC>1\)，证明某个 \(\delta>0\) 下

\[
 \boxed{\left|\sum_I{\cal H}_{D,q}\right|\le X^{-\delta}} \tag{5}
\]

就足以由 (3)--(4) 使区间候选数小于 1。尤其 \(q=1,C>1\) 已足够；并不需要
把 (5) 做到相对于更小的 \(N\mu_q\) 的精度。

若仍取 \(q=\lfloor\eta L_3\rfloor\)，阈值代价精确为
\(X^{2\eta C(1+\varepsilon)+o(1)}\)，故需
\(\delta>2\eta C(1+\varepsilon)\)。固定 \(q\) 是更弱、也更合适的所需输入。

## 4. Primitive Fourier 目标

对一个前沿 \(T\)，令 \(c=\prod_{p\in T}p\)，\(p_*\) 为 terminal prime，
\(\gamma_T\) 为此前未选素数的零模积。若

\[
 h_p(u)\equiv u(c/p)^{-1}\pmod p,
 \qquad D_H(\theta)=\sum_{j<H}e(-j\theta),
\]

则前缀 Fourier 系数精确为

\[
 \widehat g_T(u)=
 \gamma_T{(-b)^{|T|}\over c}e(-uK/c)
 \prod_{p\mid c}D_H(h_p(u)/p)                        \tag{6}
\]

当 \((u,c)=1\)，否则为零。在 \(I=(A,A+N]\) 上，(6) 与

\[
 e(u(A-K)/c)
 \sum_{m\le N}e(um/c)V_{p_*}(A+m)                   \tag{7}
\]

相乘并对 \((T,u)\) 联合求和，恰好等于 (5) 的左端。于是所有非零频率都是
primitive，且区间起点、terminal suffix 与 CRT 逆元没有被分离。

有限核验使用 \(H=2,q=2,c=5\cdot11\)，含一个 skipped prefix prime 和一个
非平凡 suffix；系数最大误差为 \(4.680\times10^{-17}\)，直接相关和与 (6)--(7)
之差为 \(2.419\times10^{-15}\)。这只核验代数恒等式。

## 5. 无条件的“几乎所有继承相位”定理

概率空间必须明确为

\[
 A\sim\operatorname{Unif}(\mathbb Z/Q\mathbb Z),
 \qquad Q=\prod_{H<p\le z}p,                          \tag{8}
\]

而不是对实际二进制起点、素数或候选整数随机化。ANOVA 正交性给出

\[
 {1\over Q}\sum_{A\bmod Q}|{\cal H}_{D,q}(A)|^2
 =\mu_q^2\sum_{c(T)>D}\prod_{p\in T}v_p,
 \quad v_p={\mathbb E d_p^2\over m_p^2}.             \tag{9}
\]

其中 \(\sum_pv_p=O_C(q^2/L_2)\)，而 \(c(T)>D\) 迫使
\(|T|\ge L_2-2L_3+O(1)\)。所以固定 \(q\) 时

\[
 {1\over Q}\sum_A|{\cal H}_{D,q}(A)|^2
 \le\mu_q^2\exp\{-(2+o(1))L_2L_3\}.                \tag{10}
\]

令 \(S_D(A)=\sum_{m\le N}{\cal H}_{D,q}(A+m)\)。只用安全的 Cauchy 界，

\[
 \mathbb E_A|S_D(A)|^2\le N^2\mathbb E_A|{\cal H}_{D,q}(A)|^2. \tag{11}
\]

由 Chebyshev，若 \(qC>1+\delta\)、\(N\le X\)，违反 (5) 的完整 CRT 起点
比例至多

\[
 \boxed{X^{-2(qC-1-\delta)+o(1)}}.                  \tag{12}
\]

当 \(N\asymp X\) 时，结合 (3)--(4)，(12) 之外的每个起点区间内候选数都严格
为零。这是无条件定理。

但 \(Q\) 比任意 \(X^A\) 都大；模 \(Q\) 中密度 \(X^{-\sigma}\) 的集合仍可
包含远长于 \(X\) 的连续区段，也可包含所有实际 dyadic starts。因此 (12) 不能
推出原题。

## 6. 一个候选必迫使长异常相位簇

定义标准平移权 \(W_0\)，则 block start 为 \(K\) 时有

\[
 W_K(n)=W_0(n-K),\qquad
 \sum_{n\in(A,A+N]}W_K(n)^q=S_q(A-K).                \tag{13}
\]

这里 \(H,z,a,t\) 全部由同一个 \(X\) 一次确定，滑动 \(K\) 时没有重新调参。

取

\[
 Y=\exp\{L_2\sqrt{L_3}\}=X^{o(1)}.
\]

原题候选对所有充分大的 \(k\) 均满足阈值，所以可令
\(K\) 遍历 \([Y,2Y]\)。此时阈值总损失仍仅
\(X^{O(1/\sqrt{L_3})}=X^{o(1)}\)，从而同一个候选迫使

\[
 S_q(A-K)\ge X^{-o(1)}\qquad(Y\le K\le2Y).           \tag{14}
\]

量词上，\(K_\varepsilon\) 固定而 \(Y\to\infty\)，且
\(2Y+H<X\le n_0\)，所以这些块最终全部满足
\(K\ge K_\varepsilon\) 与 \(K+H<n_0\)。

即 \([A-2Y,A-Y]\) 中连续 \(Y+1\) 个继承相位全部异常。因此不必证明任意起点
统一界；证明相关 dyadic 范围内每个长度 \(Y\) 的起点块至少含一个满足
\(S_q(B)\le X^{-\delta}\) 的点，也能闭合原题。现有 (12) 只是密度界，不能排除
这种次幂长度聚集。

而且“对任意 CRT 起点排除这种聚集”本身也是假的。对
\(p>Y+H\) 可选局部相位让整段避开禁块；对 \(H<p\le Y+H\) 随机选择局部
相位并用 Chernoff 与 union bound，可使 \(Y\) 个位置的命中数同时只有
\(O(HL_4)\)，其中 \(L_4=\log_4X\)。CRT 合并后得到某个模 \(Q\) 的长度 \(Y\) 段，其每点权重均为
\(X^{-o(1)}\)。该段未必有代表元 \(A\asymp X\)，所以没有反驳原题；它严格
说明缺失的反聚集定理必须利用实际起点的大小/位置，不能是 arbitrary-start
黑箱。

## 7. Kloosterman 文献适用性

[Bettin--Chandee](https://arxiv.org/abs/1502.00769) 的三线性逆模相位、
[Walker](https://arxiv.org/abs/2101.04418) 的筛权相关、
[Fouvry--Radziwiłł](https://arxiv.org/abs/1811.08672) 的非平衡卷积分布以及
[Wright 2026](https://arxiv.org/abs/2604.25177) 的 partially fixed modulus
改进均已逐项核对。它们提供相关相位形状，但不能直接套用：

* 本题的 prime endpoint \(z=X^{o(1)}\) 不是 divisor level；crossing
  conductor 实为 \(X^{1-o(1)}\)；
* 展开包含增长到 \(H\) 个 shifted linear forms；
* suffix 随 terminal prime 改变且未截断；
* 所需结论是整个联合和的 \(X^{-\delta}\)，不是正幂误差。

因此本轮没有引用一个并不覆盖 (7) 的黑箱定理。Kloosterman 分组只保留为条件
路线。

## 8. 最终边界

本轮最强无条件结果是 (12) 的多项式稀疏异常相位定理、(14) 的长异常簇
必要条件，以及“任意 CRT 起点统一反聚集”为假的严格反例。最强条件接口是
(5)，或只针对实际 \(A\asymp X\) 的异常簇反聚集定理。

严格状态：

* Erdős #679 第一问：**OPEN**；
* 确定性完整区间传递：**未证明**；
* 原题证明/证否：**无**；
* Q2 提前停止门槛：**未达到**；
* SCI 二区投稿主结果门槛：**未达到**。

资源上，本流只运行了一次 0.2 秒的纯 Python 有限恒等式核验，使用
`taskset -c 7 nice -n 10` 固定单核；其余均为符号推导与短时文本检查，没有并发或
长期计算。统一计费窗口为 `17:10:18--18:10:18`，严格登记 3,600 秒；
`18:10:18` 后未新增数学内容，仅完成冻结元数据与校验和。
