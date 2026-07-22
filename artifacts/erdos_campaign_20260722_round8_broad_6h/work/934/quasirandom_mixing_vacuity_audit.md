# Erdős #934：quasirandom mixing 推导复核与空门槛否决

日期：2026-07-22（Asia/Hong_Kong）

## 1. 结论

Babai--Nikolov--Pyber（BNP）的卷积混合不等式确实能作用于本轮的左右缺陷
normal form，并严格推出

\[
rc\le\frac{N^2}{D}.                               \tag{1}
\]

这里 \(N=|K|\)、\(r=|A|\)、\(c=|K\setminus AA^{-1}|\)，而 \(D\) 是
\(K\) 的最小非平凡复不可约表示维数。卷积方向、归一化和参数定义均已复核。

但从 (1) 到 \(253/225\) 常数所需的充分条件 \(D\ge11r\) 在本问题中永远
不可能成立。已有普适界 \(N\le2r^2-3r+2\)，而表示维数平方和立即给

\[
D\le\sqrt{N-1}<\sqrt2\,r<11r.                    \tag{2}
\]

因此这不是新上界，更不是 Q2 候选，而是一条已严格否决的空门槛路线。
同理，“若 \(D/r\to\infty\)”在该参数区间也是空命题。

## 2. normal form、对偶包含与卷积方向

使用

\[
U=AA^{-1},\quad V=A^{-1}A,\quad
C=K\setminus U,\quad D'=K\setminus V,
\]

其中 \(1\in A\)、\(|A|=r\)、\(|C|=|D'|=c\)，缺陷条件为

\[
A^{-1}CA\subseteq V.                              \tag{3}
\]

由 (3) 还得到对偶包含

\[
\boxed{AD'A^{-1}\subseteq U}.                     \tag{4}
\]

否则若 \(adb^{-1}\in C\)，其中 \(a,b\in A,d\in D'\)，则
\(d=a^{-1}(adb^{-1})b\in A^{-1}CA\subseteq V\)，矛盾。取 \(1\in A\) 得

\[
AD'\subseteq U,\qquad CA\subseteq V.              \tag{5}
\]

原坐标中的 \(BD\cap CB=\varnothing\) 归一化后恰为

\[
\boxed{AD'\cap CA=\varnothing}.                   \tag{6}
\]

也可直接验证：若 \(ad=cb\)，则 \(d=a^{-1}cb\in V\)，矛盾。

## 3. 未归一化卷积的逐行核对

定义

\[
(f*g)(x)=\sum_{y\in K}f(y)g(y^{-1}x),
\]

并令

\[
F=1_A*1_{D'},\qquad G=1_C*1_A.
\]

于是 \(\operatorname{supp}F=AD'\)、\(\operatorname{supp}G=CA\)，故由 (6)

\[
\langle F,G\rangle=0.                             \tag{7}
\]

两者平均值均为 \(\mu=rc/N\)。写 \(1_X^0=1_X-|X|/N\)，则

\[
F-\mu=1_A^0*1_{D'}^0,\qquad
G-\mu=1_C^0*1_A^0.                                \tag{8}
\]

对 \(D\)-quasirandom 有限群，未归一化 BNP 不等式为

\[
\|f*g\|_2\le\sqrt{N/D}\,\|f\|_2\|g\|_2            \tag{9}
\]

（均值零条件已由 (8) 满足）。又

\[
\|1_X^0\|_2^2=|X|\left(1-\frac{|X|}{N}\right)\le|X|,
\]

故

\[
\|F-\mu\|_2,\ \|G-\mu\|_2\le\sqrt{Nrc/D}.         \tag{10}
\]

由 (7)--(10) 及 Cauchy--Schwarz，

\[
\frac{r^2c^2}{N}
=-\langle F-\mu,G-\mu\rangle
\le\frac{Nrc}{D},
\]

即得 (1)。这也等价于把 BNP 的标准二集合 product-growth corollary
分别用于两个不交乘积集 \(AD'\)、\(CA\)；mixing 步本身不是新定理。

## 4. \(11r\) 的形式代数正确，但假设为空

设

\[
a=r^2-r+1,\qquad\gamma=\frac{253}{225}.
\]

因 \(c=N-|U|\ge N-a\)，若 \(N\ge\gamma r^2\)，则 (1) 给

\[
D\le\frac{N^2}{r(N-a)}.                            \tag{11}
\]

又 \(N\le2r^2-3r+2=2a-r<2a\)，而 \(x^2/(x-a)\) 在 \(a<x<2a\)
上递减，所以

\[
D\le\frac{\gamma^2r^3}{(\gamma-1)r^2+r-1}<11r.    \tag{12}
\]

最后一个不等式等价于

\[
\left(11(\gamma-1)-\gamma^2\right)r^2+11r-11
=\frac{5291}{50625}r^2+11r-11>0.                  \tag{13}
\]

所以条件命题“\(D\ge11r\Rightarrow N<\gamma r^2\)”的代数没有错。致命
问题是正则表示给

\[
1+D^2\le\sum_{\rho\in\widehat K}(\dim\rho)^2=N,
\]

从而 (2) 成立，前提没有实例。

## 5. 定向一手文献查重

1. Babai--Nikolov--Pyber, *Product Growth and Mixing in Finite Groups*，
   作者公开稿 <https://people.cs.uchicago.edu/~laci/papers/bnp-soda08.pdf>：
   Theorem 2.1 是 (9) 的概率分布版本，product-growth corollary 直接包含
   本轮 mixing 步。
2. Gowers, *Quasirandom Groups*，
   <https://arxiv.org/abs/0710.3877>：核对最小表示维数与 product mixing
   背景；没有本题的左右缺陷 normal form。
3. Cambie--Cames van Batenburg--de Joannis de Verclos--Kang,
   *Maximising line subgraphs of diameter at most \(t\)*，
   <https://arxiv.org/abs/2103.11898>：核对 \(h_t\) 定义和
   \(3\Delta^t/2\) 上界；全文没有 Cayley/quasirandom 分支。
4. Kumar--Mohar--Pragada, *An improved bound for the strong clique index of
   graphs*, <https://arxiv.org/abs/2607.02698>：核对 \(253/225\) 背景；
   全文没有 Cayley/quasirandom 分支。
5. van Dam--Jazaeri, *On bipartite distance-regular Cayley graphs with small
   diameter*, <https://arxiv.org/abs/2109.13849>：涉及二部 Cayley 图与
   difference sets，但不是这里的 line-graph diameter-3 缺陷条件。

检索未发现完全相同的 normal form 表述；但因数值后果由 (2) 判定为空，
它无论如何不能担当论文主定理。

## 6. 保留下来的非空结构

(4)--(6) 是非空且严格的。特别对每个 \(c\in C,d\in D'\)，

\[
(A\cup cA)^{-1}(A\cup cA)=V,\qquad
(A\cup Ad)(A\cup Ad)^{-1}=U,                      \tag{14}
\]

且两个并集都是不交并。这表明 proper defect 会让同一个左右差集容纳一个
大小翻倍的集合。下一步应研究这种“差集不增长扩张”的稳定子/能量结构，
而不是提高 quasirandom 参数。

## 7. 状态

- mixing 归一化与卷积方向：**PASS**；
- \(D\ge11r\Rightarrow253/225\) 形式代数：**PASS，但前提不可能**；
- 文献定位：BNP 标准推论，非独立 mixing 定理；
- 路线结论：**VACUOUS_ROUTE_REJECTED**；
- #934 一般问题仍开放，不触发 Q2 早停。
