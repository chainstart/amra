# Erdős #596 / R002 独立反向审计

- 审计对象：`../intake_536_596_52_949/596_REPORT.md`
- 审计命题：对每个有限、简单且含圈的图 \(F\)，有序对
  \((C_4,F)\) 满足 #596 的两条性质，当且仅当
  \(\operatorname{girth}(F)\geq 5\)。
- 审计方式：不接受原报告结论为前提；分别核对两个外部定理的原始量词，
  重做两个必要性证明，并穷举搜索初等部分的有限反例。
- 结论：**PASS_WITH_PRECISION_CORRECTIONS**。在通常的简单图、ZFC 语境下，
  未发现反例或证明缺口；命题成立。原报告有一处术语/表述应修正，但不影响
  定理：Erdős–Hajnal 的结论本身已经是可数个无圈生成子图的**边分解**，
  且其原文把不含任何 circuit 的图称为 “tree”，即现代通常称的 forest，
  不是“若干可能重叠的连通树覆盖”。

## 0. 与官网量词对齐

#596 官网对有限图 \(G_1,G_2\) 要求：

1. 每个整数 \(n\geq1\) 都有一个不含 \(G_1\) 的图 \(H\)，使任意
   \(n\)-边染色含单色 \(G_2\)；
2. 每个不含 \(G_1\) 的图 \(H\)（这里没有有限性限制）都有一个至多可数
   的边染色而无单色 \(G_2\)。

因此，充分性第一步只需有限色 Ramsey 宿主；第二步必须覆盖任意基数的宿主。
下面的两个外部输入恰好分别满足这两个量词。

## 1. Nešetřil–Rödl 输入

### 权威陈述

Reiher–Rödl, *The Girth Ramsey Theorem*, Theorem 2.1（PDF 文章页 6）
把旧的 Rödl–Nešetřil 图论结论精确重述为：

\[
\forall F\,[\operatorname{girth}(F)>4]\ \forall r\geq2\
\exists H\,[\operatorname{girth}(H)>4\land H\to(F)_r].
\]

同文第 1.2 节明确说明此后的染色均为**边染色**；其箭头甚至要求找到
单色的诱导拷贝，故强于 #596 只需的普通拷贝。Theorem 2.1 说 “every graph
\(F\)”，没有连通性、无孤立点等附加条件，因而也覆盖不连通 \(F\)。
该有限结构 Ramsey 构造给出有限 \(H\)，但 #596 并不要求 \(H\) 有限，
所以即便只用其字面存在量词也足够。\(r=1\) 不在 Theorem 2.1 的写法中，
但取 \(H=F\) 即可；此时 \(F\) 自身 girth \(>4\)，故 \(C_4\)-free。

Theorem 2.1 的原始归属由该文参考文献 [24] 给出：
J. Nešetřil and V. Rödl, *Strong Ramsey theorems for Steiner systems*,
Trans. Amer. Math. Soc. 303 (1987), 183–192,
DOI `10.2307/2000786`。

### 对本命题的推出

在简单图中，\(\operatorname{girth}(H)>4\) 排除长度 3、4 的圈，特别排除
\(C_4\)。因此对每个有限色数都有一个 \(C_4\)-free 的 \(F\)-Ramsey 宿主，
#596 第一条成立。这里没有把完整的现代 Girth Ramsey Theorem 错当成旧结论；
所需的正是明确标为旧结论的 Theorem 2.1（阈值 \(>4\)）。

**核查结果：通过。** 颜色数、目标图、宿主 girth 与边染色四个量词均匹配。

## 2. Erdős–Hajnal 分解输入

### 原文逐项核查

P. Erdős and A. Hajnal, *On decomposition of graphs*, Acta Math. Acad.
Sci. Hungar. 18 (1967), 359–377：

- Definition 1.1（文章页 359）定义 edge-decomposition：所有成员具有同一
  顶点集，边集两两不交，且并为原图全部边。
- §7 开头（文章页 373）约定：没有 circuits 的图称为 tree。故其 “tree”
  不要求连通，按现代术语是 forest。
- Theorem 10（文章页 373；证明在 374）断言：不含 quadrilateral 的图有
  一个 type \(\omega\) 的边分解，所有成员均为上述 “trees”。
- 论文从 Definition 1.1 起以任意基数的顶点集和基数型分解为框架；
  Theorem 10 没有限定图可数。其证明先由前文结果得到
  \(\operatorname{Col}(H)\leq\omega\)，再用 Theorem 9 作可数边分解。
  所以 \(\omega\) 是**边颜色类的数量**，不是顶点数限制。

“quadrilateral” 在此处是四边形子图（不要求诱导）；这正对应 #596 的
\(C_4\)-free。于是任意基数的 \(C_4\)-free 图的边可分成
\((T_i)_{i<\omega}\)，每个 \(T_i\) 无圈。若有限 \(F\) 含圈，则任何
\(T_i\) 都不含 \(F\)，把分解编号当作边颜色就满足 #596 第二条。

**核查结果：通过，但原报告应改写。** 不需要先取重叠覆盖再“分给第一棵树”；
原定理已经给边分割。把原文 tree 译成“森林”最不易误解。

## 3. 含三角形时的全局二染色

令 \(H\) 为任意基数的 \(C_4\)-free 简单图。

1. 若两个不同三角形 \(uvx\) 与 \(uvy\) 共用边 \(uv\)，则
   \(x,u,y,v\) 四点互异，且
   \(x-u-y-v-x\) 的四条边都在 \(H\) 中；这给出一个 \(C_4\)，矛盾。
   所以每条边至多属于一个三角形，等价地，所有三角形两两边不交。
2. 在 ZFC 中良序化 \(E(H)\)。对每个三角形，将其最小边染红、另两边染蓝；
   将不属于三角形的边染红。因三角形边不交，这一定义在全图上无冲突。
3. 每个三角形恰有一红两蓝，故没有单色三角形。若 \(F\) 含三角形，则任何
   单色 \(F\) 都会包含一个单色三角形，矛盾。

故不论候选 \(C_4\)-free 宿主 \(H\) 多大，总存在一个二染色避开 \(F\)；
#596 第一条在 \(n=2\) 即失败。若不想显式使用边的良序，也可对两两不交的
三角形族作选择；两种写法都使用通常 ZFC 背景。

**核查结果：通过。** 原报告的局部规则确实能拼成任意基数宿主上的全局染色；
建议补出“良序取最小边”以消除隐含选择和规则一致性的疑问。

## 4. 含圈有限图的三分法

对有限简单且含圈的 \(F\)，按最短圈长度作互斥分类：

1. \(\operatorname{girth}(F)=3\)：\(F\) 含三角形，第 3 节否定性质 1；
2. \(\operatorname{girth}(F)=4\)：\(F\) 含 \(C_4\)，任何 \(C_4\)-free
   宿主本身不含 \(F\)，性质 1 甚至在 \(n=1\) 失败；
3. \(\operatorname{girth}(F)\geq5\)：第 1 节给性质 1，第 2 节给性质 2。

由于 \(F\) 已假定含圈，其 girth 是有限整数，以上三类穷尽。原报告按
“含 \(C_4\) / 含三角形 / 两者都不含”叙述时前两类可能重叠，但各自的
否定论证都正确；按 girth 写成上述互斥三分法更严整。孤立点、树状分支和
多个连通分支不破坏分类，也不破坏两个外部输入。

**核查结果：通过。**

## 5. 反例搜索

`verify_elementary_branches.py` 独立枚举至 6 个顶点的全部标号简单图，检查：

- 每个含圈图恰落入 girth 3、girth 4、girth 至少 5 的一个类别；
- 每个 \(C_4\)-free 图的不同三角形确实边不交；
- 上述确定性红蓝染色没有单色三角形；
- 没有找到与两个必要性分支相冲突的有限图。

枚举仅是初等引理的回归/反例搜索，不可能替代 Nešetřil–Rödl 或
Erdős–Hajnal 的无限量词证明。机器结果见
`elementary_counterexample_search.json`。

## 6. 最终判定与建议修订

**定理判定：成立。未发现需要立即上报的定理错误。**

原 `596_REPORT.md` 建议只作以下精度修订（本 QA 按要求未改原文件）：

1. 将“可数棵树的并；把重叠覆盖分配”改成“type \(\omega\) 的无圈生成
   子图边分解（原文称 trees，现代称 forests）”。
2. Nešetřil–Rödl 处精确标为 Reiher–Rödl Theorem 2.1，并注明
   \(r\geq2\)，而 \(r=1\) 取 \(H=F\)。
3. 三角形染色处加入全局良序规则。
4. 用 girth \(=3\)、\(=4\)、\(\geq5\) 写互斥三分法。

这些都是表述强化，不改变 `RIGOROUS_INFINITE_SUBCLASS_CLASSIFICATION`
这一数学结论；它也仍不等于 #596 对任意 \(G_1,G_2\) 的完整分类。

## 7. 精确来源

完整 URL、检索时间、下载字节哈希和定位见 `SOURCE_MANIFEST.json`。

- Christian Reiher and Vojtěch Rödl, *The Girth Ramsey Theorem*,
  arXiv:2308.15589；Theorem 2.1、Definition 1.3、§1.2。
- J. Nešetřil and V. Rödl, *Strong Ramsey theorems for Steiner systems*,
  Trans. AMS 303 (1987), 183–192, DOI `10.2307/2000786`。
- P. Erdős and A. Hajnal, *On decomposition of graphs*,
  Acta Math. Acad. Sci. Hungar. 18 (1967), 359–377,
  DOI `10.1007/BF02280296`；Definition 1.1、§7、Theorems 9–10。
- Erdős Problems #596 官方页面（审计时页面原题量词）。

