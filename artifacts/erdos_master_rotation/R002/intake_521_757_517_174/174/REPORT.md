# Erdős #174 — Euclidean Ramsey 集的 spherical/subtransitive 判别

结论：`OPEN__AUDIT_RETAIN__COOLDOWN`

## 原题量词

固定有限集 \(A\subset\mathbb R^n\)。称 \(A\) 为 Ramsey 集，如果

\[
\forall k\ge1\ \exists d=d(A,k)\ \forall
\chi:\mathbb R^d\to\{1,\ldots,k\},
\]

都存在一个与 \(A\) 全等的子集，其所有点具有同一颜色。原题要求刻画全部这样
的有限 \(A\)。维数 \(d\) 可以依赖 \(A,k\)，但必须对该 \(k\) 的所有染色统一。

官网在 2026-07-23 仍标 `OPEN`（最后编辑 2025-10-16）。

## 当前理论边界

- Erdős--Graham--Montgomery--Rothschild--Spencer--Straus 证明：
  Ramsey \(\Rightarrow\) spherical。
- Graham 猜想所有 spherical 集都是 Ramsey。
- Leader--Russell--Walters（LRW）提出竞争猜想：Ramsey 当且仅当
  subtransitive，即可嵌入某个有限传递集。
- “subtransitive \(\Rightarrow\) Ramsey”本身并非一般定理。Kříž 的现有定理
  要求传递集有可解群传递作用；不能把任意传递集当成已知 Ramsey。
- Behague（arXiv:2510.15677v3，2025-12-04）证明几乎全部已知 Ramsey 例子
  实际是 subsoluble，可能例外仅120胞体和600胞体。该结果加强了现有例子的
  统一解释，但没有刻画所有 Ramsey 集。

## 路线一：最小显式试金石——LRW cyclic kite

取超越数 \(-1<a<1\)，\(b=\sqrt{1-a^2}\)，并令

\[
Q_a=\{(-1,0),(1,0),(a,b),(a,-b)\}.
\]

四点均在单位圆上。按 LRW 的记号取
\[
z=(-1,0),\quad y=(1,0),\quad x=(a,b),\quad w=(a,-b).
\]
则
\[
w=z-1(x-z)+(a+1)(y-z).
\]
参数为 \(\alpha=-1\ne1\)、\(\beta=a+1\)，而 \(\beta\) 超越于
\(\mathbb Q(\alpha)=\mathbb Q\)。LRW 定理因此证明 \(Q_a\) 不能嵌入任何有限
传递集。

这四点构成 cyclic/right kite，但在超越 \(a\ne0\) 时没有一对对边平行，故不是
已知 Ramsey 的等腰梯形。证明 \(Q_a\) Ramsey 会直接否定“Ramsey iff
subtransitive”；证明它非 Ramsey 则给竞争猜想最强的显式证据。因此它是比
泛泛研究所有球面集更合适的最小判别对象。

## 路线二：两轨道 Kříž 路线及其严格失败点

关于 \(x\)-轴的反射在 \(Q_a\) 上有三个轨道：
\[
\{(-1,0)\},\quad\{(1,0)\},\quad\{(a,b),(a,-b)\}.
\]
加入 \((-a,\pm b)\) 后，坐标轴反射群 \(C_2\times C_2\) 在六点集上只有两个
轨道。这看似可套 Kříž 的“两轨道”加强。

但 Kříž 加强的前提仍是该有限集本身为传递集，只是某个可解子群在其上至多有
两个轨道；Behague 的 Question 6.2 也明确保留这一前提。上述六点集只有两条
坐标轴反射轨道，并未变成传递集。若能把 \(Q_a\) 放入任何有限传递集，又会直接
违背 LRW 定理。因此该捷径严格失效，不是证明。

一个足以打开正向局面的新 closing lemma 是：

> **三轨道球面引理。** 每个有限球面集，只要有一个可解等距群作用且至多有
> 三个轨道，就是 Ramsey。

它会立即覆盖 \(Q_a\) 的反射作用。当前没有该引理的证明；它也明显超出 Kříž
现有定理，不能作为黑箱引用。

## 路线三：证否所需的统一染色

非球面必要性证明使用仿射依赖
\(\sum\lambda_i a_i=0,\sum\lambda_i=0\) 中的非零二次缺陷
\(\sum\lambda_i\|a_i\|^2\)，再给平方范数有限染色。对球面集，这个缺陷恒为0，
所以该标准染色机制在 \(Q_a\) 上正好退化。

要证明 \(Q_a\) 非 Ramsey，必须给出一个固定颜色数 \(k\)，并对每个维数 \(d\)
构造一个 \(\mathbb R^d\) 的 \(k\)-染色，统一避开 \(Q_a\)。只在某个固定
维数做 SAT 或格点染色不能满足原题否定的量词，因此不登记为推进。

## 原路线审计

1. spherical 只是必要条件，不是已知充分条件；
2. subtransitive 也不是一般已知充分条件；
3. 已知 Ramsey 类几乎都 subsoluble，故不可能包含 LRW 已证非
   subtransitive 的 \(Q_a\)；
4. “有限维找不到单色副本”或“有限网格可染”均不能证否。

## 调度与发表判断

保留为高价值判别题，但冷却至少三个宏周期。重新开启条件是出现：

- 三轨道球面引理的真实组合机制；
- 对 \(Q_a\) 的固定颜色数、全维统一避免染色；
- 或超越现有 subtransitive/subsoluble 框架的新 Ramsey 闭包定理。

决定 LRW kite 的 Ramsey 性会是重要论文成果；本轮只完成了试金石、量词和失败
路线的精确审计，没有二区级新定理。

## 来源

- https://www.erdosproblems.com/174
- https://arxiv.org/abs/1012.1350
- https://arxiv.org/abs/1012.5468
- https://arxiv.org/abs/2510.15677

