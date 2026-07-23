# Erdős #517 — Fabry-gap 整函数的有限纤维

结论：`OPEN__ROUTE_ERROR_AUDITED__COOLDOWN`

## 原题量词

设

\[
f(z)=\sum_{k=1}^{\infty}a_kz^{n_k}
\]

是整函数，其中 \(n_1<n_2<\cdots\) 为整数且每个 \(a_k\ne0\)。假设

\[
\frac{n_k}{k}\longrightarrow\infty .
\]

问题问：是否对每个 \(w\in\mathbb C\)，集合
\(\{z\in\mathbb C:f(z)=w\}\) 都是无限集？

官网在 2026-07-23 仍标 `OPEN`（最后编辑 2025-12-29）。这是 Fejér--Pólya
猜想；不能把“每个值至少取一次”“除至多一个例外值”“没有亏值”与题面要求的
“每个值取无限次”混为一谈。

## 已知边界刷新

- 若 \(\sum_k1/n_k<\infty\)（Fejér gaps），Biernacki 已证明每个值取无限次；
  Murai 进一步证明没有有限亏值。
- 若 \(f\) 为有限阶，Pólya 在
  \(\limsup(n_{k+1}-n_k)=\infty\) 下已证明结论。本题假设蕴含这个 limsup
  条件：若尾部间隙有界，则 \(n_k=O(k)\)。
- 因而真正未解决区间是无限阶、\(\sum1/n_k=\infty\) 的 Fabry-gap 函数。
  \(n_k\asymp k\log k\) 是典型边界。

## 重要路线审计：亏值归约不成立

旧材料
`artifacts/math_scout/active-math-scout-balanced-20260501-0831/problems/0028-517/probe_output.md`
写道，原题“等价于”证明 Fabry-gap 整函数没有有限亏值。这不正确。

Murai 1983 的第5节显式构造了一个 Fabry-gap 整函数 \(g_\infty\)，满足

\[
\delta(0,g_\infty)=1.
\]

所以“Fabry gaps \(\Rightarrow\) 无有限亏值”本身为假。亏量1只说明零点相对
Nevanlinna 增长极少，并不说明完全没有零点，更不反驳原猜想。该加强命题不能
作为 closing lemma。

## 路线一：\(Pe^g\) 支撑刚性

若某个值 \(w\) 只被取有限次（计重数），则

\[
f-w=P e^g,
\]

其中 \(P\ne0\) 为多项式，\(g\) 为整函数。证明方式是把有限零点连同重数放入
\(P\)，剩余的无零整函数在单连通平面上有整对数。

另一方面，\(f-w\) 的非零 Taylor 指数计数函数为 \(o(N)\)。因此一个真正等价
的硬核是：

> **稀疏支撑有限零点引理。** 非多项式整函数若 Taylor 支撑的自然密度为0，
> 则它有无限多个零点。

等价的因子形式是：不存在 \(P e^g\)（\(P\ne0\) 为多项式，\(g\) 为非恒定
整函数）的 Taylor 支撑具有零密度。

该表述精确，但本轮没有证明它；在一般超越 \(g\) 下，指数展开的全局复相消去
正是困难所在。把它仅仅重命名为“支撑定理”并没有缩短闭合距离。

## 路线二：Rouché 主项/主簇

若能在无穷多个圆周上找到一个 Taylor 单项严格压过其余项和 \(|w|\)，Rouché
定理会立即产生趋于无穷的 \(w\)-点数。Fejér-gap 证明可利用可求和稀疏性获得
类似控制，但 bare Fabry 条件不保证相邻间隙趋于无穷。

例如可取成对指数

\[
n_{2j-1}=j!,\qquad n_{2j}=j!+1
\]

（删去有限个初项），仍有 \(n_k/k\to\infty\)，但无穷多相邻间隙等于1。
因此“每个大指数都孤立，从而单项支配”的路线量词错误。要继续这条路，必须先
证明一个允许任意相邻簇的主簇 Rouché 引理，并统一控制簇内多项式在圆周上的
最小模；本轮未得到这种控制。

## 可以重新开启的 closing lemma

只有以下两类新输入足以重开：

1. 一个真正的 Taylor-support 刚性定理，排除 \(Pe^g\) 的零密度支撑，且不借用
   已被 Murai 反例否定的“无亏值”加强；
2. 一个 Fabry 主簇引理：对每个 \(w\)，给出无穷多个截断层及闭曲线，使
   \(f-w\) 与一个零点数趋于无穷的有限主簇可用 Rouché 比较。

## 调度与发表判断

本题先做路线审计，然后冷却至少三个宏周期。当前 closing lemma 与原题的核心
几乎等价，没有独立机制；继续做有限系数实验不会改变这一点。

若将 \(Pe^g\) 支撑刚性证明到覆盖一般超越 \(g\)，会直接闭合原题并具有很高
论文价值；若只覆盖有限阶或 Fejér gaps，则主要重现已知范围。当前报告不构成
可发表的新定理。

## 来源

- https://www.erdosproblems.com/517
- https://www.erdosproblems.com/history/517
- https://doi.org/10.5802/aif.930
- https://www.numdam.org/article/AIF_1983__33_3_39_0.pdf

