# Erdős #596 — R002标准准入

日期：2026-07-23

结论：`RIGOROUS_INFINITE_SUBCLASS_CLASSIFICATION__ORIGINAL_STILL_OPEN`

## 原题

对有限图 \(G_1,G_2\)，寻找满足下列两条的有序对：

1. 对每个有限 \(r\)，存在 \(G_1\)-free 图 \(H\)，使
   \(H\to(G_2)^2_r\)；
2. 每个 \(G_1\)-free 图的边都可用可数种颜色染色而无单色 \(G_2\)。

官网只明确列出 \((C_4,C_6)\) 这一正例，完整分类仍为 `OPEN`。

## 本轮定理：固定 \(G_1=C_4\) 的全部含圈目标

**定理。** 若 \(F\) 是有限且含圈的图，则 \((C_4,F)\) 满足#596的两条性质，
当且仅当

\[
\operatorname{girth}(F)\ge5,
\]

即 \(F\) 同时不含 \(C_3\) 和 \(C_4\)。

### 充分性

若 \(\operatorname{girth}(F)>4\)，Nešetřil–Rödl 定理对每个有限颜色数
\(r\) 给出一个 \(\operatorname{girth}(H)>4\) 的有限图 \(H\)，满足

\[
H\to(F)^2_r.
\]

特别地 \(H\) 是 \(C_4\)-free，第一条成立。

Erdős–Hajnal 的 Theorem 10 说明每个（允许任意基数的）\(C_4\)-free
图都有 type \(\omega\) 的边分解，且每个分量图均无圈。原文把任意无圈图
称为 “tree”，按现代术语应译为 forest；该结论本身已经是边分割，不需要
先取重叠覆盖再重新分配。因为 \(F\) 含圈，每个颜色类都不含 \(F\)，
第二条成立。

### 必要性：含 \(C_4\)

若 \(F\) 含 \(C_4\)，任何 \(C_4\)-free 宿主都不含 \(F\)，所以第一条甚至
对一种颜色也不可能成立。

### 必要性：含三角形

在任意 \(C_4\)-free 图 \(H\) 中，一条边不可能属于两个不同三角形：若
\(uvx\) 与 \(uvy\) 是不同三角形，则

\[
x-u-y-v-x
\]

是一个四边形。因此 \(H\) 中所有三角形两两边不交。良序 \(E(H)\)，对每个
三角形把其最小边染红、另外两条染蓝，其余边染红；边不交性保证这个任意
基数宿主上的定义无冲突，且得到一个没有单色三角形的二染色。
若 \(F\) 含三角形，就不可能出现单色 \(F\)。于是第一条在 \(r=2\) 已失败。

按最短圈长度写成互斥的
\(\operatorname{girth}(F)=3\)、\(=4\)、\(\ge5\) 三类，便穷尽所有
含圈有限图，定理得证。

## 新颖性与边界

核心 Ramsey 输入不是本轮新定理；Reiher–Rödl 的论文明确把
\(C_4\)-free 版本列为旧的 Nešetřil–Rödl Theorem 2.1。该定理按原文处理
\(r\ge2\)，而 \(r=1\) 直接取 \(H=F\)。本轮新增的是把它与#596第二条及
上面的必要性论证合成一个精确的无限子类刻画。

该推论似乎尚未写入#596官网，但未完成系统新颖性检索，不声称可单独发表，
更不声称解决任意 \(G_1\) 的完整分类。

上述定理已由独立反向审计逐项核对原始量词，并通过至6点全部标号简单图的
初等分支反例搜索；审计结论为 `PASS_WITH_PRECISION_CORRECTIONS`。详见
`../qa_596/AUDIT.md`。机器枚举只用于防错，不替代两个外部结构定理。

## 后续 closing lemma

最自然的下一步不是重复 \(C_6\)，而是抽象出：

> 若一个遗传图类 \(\mathcal C=\operatorname{Forb}(G_1)\) 的所有成员均可
> 可数分解进某个类 \(\mathcal D\)，并且 \(\mathcal C\) 对所有
> \(F\notin\mathcal D\) 具有有限色 Ramsey 保存性，则刻画这些 \(F\)。

对 \(C_4\) 而言，\(\mathcal D\) 是森林。推广到其他 \(G_1\) 需要同时知道
无限分解理想和有限 Ramsey age；这仍远离原题完整分类。因此闭合距离保持3，
但本题准入结果标记为“实质子类推进”。

## 来源

- https://www.erdosproblems.com/596
- https://www.erdosproblems.com/latex/596
- https://arxiv.org/abs/2308.15589
- https://www.math.uni-hamburg.de/en/personen/reiher/artikel/girth-final.pdf
- P. Erdős and A. Hajnal, *On decomposition of graphs*, Acta Math. Acad.
  Sci. Hungar. 18 (1967), 359–377.
