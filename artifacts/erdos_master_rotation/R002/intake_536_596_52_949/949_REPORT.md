# Erdős #949 — R002标准准入

日期：2026-07-23

结论：`OPEN__NEW_PROPER_Q_SPAN_SUBCASE__HARD_KERNEL_IS_SPANNING_CASE`

## 原题

若 \(S\subset\mathbb R\) 是 sum-free，即

\[
(S+S)\cap S=\varnothing,
\]

是否存在 \(|A|=\mathfrak c\) 的 \(A\subset\mathbb R\setminus S\)，使
\((A+A)\cap S=\varnothing\)？

官网仍标 `OPEN`。已知：

- \(|S|<\mathfrak c\) 时，Zorn极大性和基数覆盖给出肯定答案；
- \(S\) 为Sidon集时已有肯定证明及Lean形式化。

## 本轮严格新子情形

**引理。** 若 \(|S|=\mathfrak c\)，但其有理线性包

\[
V=\operatorname{span}_{\mathbb Q}(S)
\]

是 \(\mathbb R\) 的真子空间，则原题答案为肯定。

**证明。** 取 \(x\in\mathbb R\setminus V\)，令

\[
A=x+V.
\]

因为 \(S\subset V\)，而陪集 \(x+V\) 与 \(V\) 不交，所以
\(A\cap S=\varnothing\)。又因 \(V\) 是 \(\mathbb Q\)-线性空间，

\[
A+A=2x+V.
\]

若 \(2x\in V\)，则 \(x=\frac12(2x)\in V\)，矛盾；故
\((A+A)\cap S=\varnothing\)。最后
\(|V|\ge|S|=\mathfrak c\)，同时 \(V\subset\mathbb R\)，所以
\(|A|=|V|=\mathfrak c\)。证毕。

值得注意的是，这个子情形甚至不需要 sum-free 假设。结合已知小基数情形后，
真正未处理的核可严格缩成

\[
|S|=\mathfrak c,\qquad
\operatorname{span}_{\mathbb Q}(S)=\mathbb R.
\]

## 路线一：极大集覆盖

取极大的可容许集 \(A\)。若不能加入 \(x\)，则至少发生

\[
x\in S,\quad 2x\in S,\quad x\in A,\quad
\text{或}\quad x+a\in S\ \text{对某个 }a\in A.
\]

因此

\[
\mathbb R
=S\cup(S/2)\cup A\cup\bigcup_{a\in A}(S-a).
\]

当 \(|S|<\mathfrak c\) 时这给出矛盾；在上述硬核中，单个 \(S\) 和每个
平移都已有连续统大小，基数计数完全饱和。需要的是关于 sum-free 集平移覆盖数
的结构定理，而不是再做一次Zorn论证。

## 路线二：平移 \(t-S\)

固定 \(t\in S\)。集合 \(t-S\) 自动与 \(S\) 不交，因为
\(t-s\in S\) 会与 \(s\in S\) 相加得到 \(t\in S\)。但

\[
(t-s_1)+(t-s_2)\in S
\]

等价于存在 \(s_3\in S\) 使

\[
s_1+s_2+s_3=2t.
\]

普通sum-free只禁止二对一关系，不能排除这个三对一关系。Sidon证明恰好在这里
使用表示唯一性；删除该假设后，平移路线没有剩余控制。

## 调度结论

本轮严格解决了“连续统大小但有理线性包为真子空间”的情形，并把一般问题
压缩到满有理张成的硬核；但这没有给出原题 closing lemma，闭合距离保持3。
下一步只值得攻下面的精确命题：

> 若 \(S\subset\mathbb R\) sum-free、\(|S|=\mathfrak c\) 且
> \(\operatorname{span}_{\mathbb Q}S=\mathbb R\)，证明不存在由少于
> \(\mathfrak c\) 个 \(S\) 的平移连同 \(S/2\) 构成的上述极大性覆盖，
> 或构造一个满足该覆盖的反例。

## 来源

- https://www.erdosproblems.com/949
- https://www.erdosproblems.com/forum/thread/949

