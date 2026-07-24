# Erdős #949：一般情形的精确图模型与可闭合子空间核

## 问题重写

给定 sum-free \(S\subset\mathbb R\)，在顶点集

\[
V=\mathbb R\setminus(S\cup S/2)
\]

上连边 \(xy\) 当且仅当 \(x+y\in S\)。原题恰好要求该图存在基数
\(\mathfrak c\) 的独立集。去掉 \(S/2\) 是必要的，因为独立集还必须满足
\(2x\notin S\)。

这个重写同时解释了为什么朴素超限贪心无效：选入一个 \(a\) 后会禁止整个
平移 \(S-a\)，在困难核 \(|S|=\mathfrak c\) 中单步就可能排除
\(\mathfrak c\) 个候选点，普通“每步只删少于连续统个点”的递归前提不成立。

## 可严格闭合的线性包络子类

令 \(V_S=\operatorname{span}_{\mathbb Q}S\)。若
\(|S|=\mathfrak c\) 且 \(V_S\ne\mathbb R\)，取任意
\(x\notin V_S\) 并令

\[
A=x+V_S.
\]

则 \(|A|=|V_S|=\mathfrak c\)，且 \(A\cap S=\varnothing\)。又

\[
A+A=2x+V_S.
\]

若 \(2x+v\in S\subseteq V_S\)，则 \(2x\in V_S\)，继而
\(x\in V_S\)，矛盾。因此 \((A+A)\cap S=\varnothing\)。结合初轮已证
\(|S|<\mathfrak c\) 的 Zorn 情形，唯一未覆盖的线性核为

\[
|S|=\mathfrak c,\qquad
\operatorname{span}_{\mathbb Q}S=\mathbb R. \tag{1}
\]

这个子类结论甚至不使用 sum-free；它只用 \(S\subset V_S\) 和
\(V_S\) 是真 \(\mathbb Q\)-子空间。

## 被排除的捷径

不能把一般图 Ramsey 定理直接用于上述图。事实上，取一个
\(\mathbb Q\)-线性无关的连续统集 \(X\)，令

\[
S=\{x+y:x,y\in X,\ x\ne y\}.
\]

由线性无关性，两个 \(S\) 元素之和不可能仍是两个互异 \(X\) 元素之和，
所以 \(S\) 是 sum-free；但 \(X\) 在上述和图中形成连续统团。故
“sum-free 强迫图无大团，再由无限 Ramsey 得大独立集”的路线在最早一步
即失败。

## 判定

本轮把硬核精确压缩到 (1)，并给出了一个针对图论捷径的结构反例，但没有
处理满线性包络情形。下一步应利用 sum-free 对平移族
\(\{S-a:a\in A\}\) 的交叠约束，而不是只做基数计数。原题仍开放；这些是
路线清障，不是 Q2 级结果。
