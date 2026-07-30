# OPG-145 搜索范围与二连通归约审计

审计日期：2026-07-29

## 结论先行

1. 仓库采用的命题与原问题一致：对每个有限简单图 \(G\)，若
   \(\Delta=\Delta(G)\)，则
   \[
   a'(G)\leq \Delta+2,
   \]
   即存在 proper edge-colouring，使每个圈至少使用三种颜色。由于染色是
   proper 的，“每个圈至少三色”与“没有双色圈”等价。
2. `Delta <= 4` 是安全的已知正例层，但引用链必须完整。Basavaraju--Chandran
   (2009) 单独只对 \(m\leq 2n-1\) 给出 \(\Delta+2\) 界；它覆盖
   \(\Delta=4\) 的非 4-正则连通图。4-正则缺口由后续结果补上，最终
   Wang--Ma--Shu--Wang (2019) 明确证明每个 4-正则简单图都满足
   \(a'(G)\leq6\)。结合早已解决的次三次情形，才得到全部
   \(\Delta\leq4\)。
3. `3-sparse` 过滤与文献定义逐字等价，而且过滤方向正确。文献中的
   3-sparse 指每条边至少有一个端点度数至多 3；代码
   `all(min(deg[u], deg[v]) <= 3 for uv in E)` 正是这个条件。Anto--Basavaraju--
   Kulamarva 的 Corollary 1 给出任意 3-sparse 简单图
   \(a'(G)\leq\Delta+2\)，没有额外的连通性假设。
4. “最小顶点数反例可限制到 `geng -C -d2`”可以严格证明，归约没有数学缺口。
   更强地，任意反例都包含一个本身仍是反例的非平凡二连通 block。
5. 但是当前实际命令还有 `-D5`，随后又只保留 `Delta == 5`。所以十阶计算
   **不能**表述为“全部 10 顶点简单图已验证”；它严格覆盖的是
   “10 顶点、二连通、最大度恰为 5”这一层，其中 3-sparse 子层由定理覆盖，
   其余子层由计算覆盖。最大度 \(6,7,8,9\) 完全不在该命令的目录中。

## 1. 精确命题及代码模型

本地问题快照给出的原文是：

> Every simple graph with maximum degree \(\Delta\) has a proper
> \((\Delta+2)\)-edge-colouring so that every cycle contains edges of at least
> three distinct colours.

该陈述可在
[`problem_details.jsonl`](../raw/unsolvedmath/problem_details.jsonl) 的
`OPG-145` 记录和
[Open Problem Garden 的可追溯镜像](https://mlelarge.github.io/graph-conjectures/op/acyclic_edge_coloring/)
中核对。Alon--Sudakov--Zaks 原论文将有限简单图、proper edge-colouring、
无双色圈以及 \(a'(G)\) 的定义写在论文首页，并在 Conjecture 1 明确写出
\(a'(G)\leq\Delta(G)+2\) for all graphs \(G\)
（[作者版 PDF](https://web.math.princeton.edu/~nalon/PDFS/asz2.pdf)，
[DOI](https://doi.org/10.1002/jgt.1010)）。

仓库的形式化合同

```text
G is a finite simple graph of maximum degree Delta.
G has a proper (Delta+2)-edge-coloring with no bichromatic cycle.
```

与上述命题等价。这里“\((\Delta+2)\)-edge-colouring”按通常含义是使用一个
大小为 \(\Delta+2\) 的颜色集合，不要求每种颜色都实际出现。

历史归属方面，Fiamčík 在 1978 年已提出这一方向；原始条目的权威书目信息为：
J. Fiamčík, *The acyclic chromatic class of a graph*, Mathematica Slovaca
28(2), 139--145 (1978)
（[EuDML 记录与全文](https://eudml.org/doc/34025)）。Alon--Sudakov--Zaks
(2001) 独立给出现在通常引用的 Conjecture 1。

## 2. `Delta <= 4` 的精确适用范围

### 2.1 2009 年结果不能被单独扩大

Basavaraju--Chandran 证明：

> 若 \(G\) 连通、\(\Delta(G)\leq4\)，且
> \(m\leq2n-1\)，则 \(a'(G)\leq\Delta(G)+2\)。

论文摘要还只推出任意 \(\Delta\leq4\) 图的较弱界 \(a'(G)\leq7\)，并没有
单独解决所有 4-正则图的 6 色问题。来源：

- M. Basavaraju and L. S. Chandran, *Acyclic edge coloring of graphs with
  maximum degree 4*, Journal of Graph Theory 61(3), 192--209 (2009),
  [DOI](https://doi.org/10.1002/jgt.20376)，
  [arXiv:0801.1744](https://arxiv.org/abs/0801.1744)。

若连通图满足 \(\Delta=4\) 但不是 4-正则图，则度数和严格小于 \(4n\)，且为
偶数，故 \(2m\leq4n-2\)，即 \(m\leq2n-1\)。因此 2009 年定理准确覆盖了
非 4-正则部分。

### 2.2 4-正则缺口及最终结论

后续论文证明每个 4-正则简单图都有 acyclic 6-edge-colouring：

- W. Wang, Y. Ma, Q. Shu and Y. Wang, *Acyclic Edge Coloring of
  4-Regular Graphs (II)*, Bulletin of the Malaysian Mathematical Sciences
  Society 42, 2047--2054 (2019),
  [期刊页与摘要](https://link.springer.com/article/10.1007/s40840-017-0592-7)，
  [DOI](https://doi.org/10.1007/s40840-017-0592-7)。

期刊摘要明确说“confirm the conjecture for graphs with \(\Delta=4\)”；
正文 Theorem 1 是“若 \(G\) 4-正则，则 \(a'(G)\leq6\)”。作者较早的完整
4-正则声明也可在
[arXiv:1209.2471](https://arxiv.org/abs/1209.2471) 核对。

\(\Delta\leq3\) 的 \(\Delta+2\) 界早已成立；Alon--Sudakov--Zaks 原论文
第 1.1 节已明确说明 \(\Delta=3\) 情形成立。于是：

- 次三次图：至多 5 色；
- 非 4-正则且 \(\Delta=4\)：2009 年定理给出至多 6 色；
- 4-正则图：2019 年定理给出至多 6 色；
- 不连通图：逐分量染色并复用同一颜色集合。

因此代码把最大度至多 4 的图作为已知正例过滤是安全的。

## 3. 3-sparse 定理与代码谓词

Anto--Basavaraju--Kulamarva 定义：

\[
G\text{ is 3-sparse}
\quad\Longleftrightarrow\quad
\forall uv\in E(G),\ \min\{d_G(u),d_G(v)\}\leq3.
\]

其 Corollary 1 是：

\[
G\text{ 3-sparse}\quad\Longrightarrow\quad
a'(G)\leq\Delta(G)+2.
\]

论文开头声明所有图均为有限、简单、无向图；Corollary 1 本身不要求连通。
来源：

- N. Anto, M. Basavaraju and S. Kulamarva, *Acyclic edge coloring of
  3-sparse graphs*, Discrete Mathematics 349(9), article 115135 (2026),
  [DOI](https://doi.org/10.1016/j.disc.2026.115135)，
  [arXiv:2501.11281](https://arxiv.org/abs/2501.11281)。

代码中的

```python
return all(min(degrees[left], degrees[right]) <= 3
           for left, right in graph.edges)
```

与定义完全一致。其否定是“存在一条边，两端度数都至少为 4”，所以搜索保留
`not is_three_sparse(graph)` 的方向也正确。

## 4. block 拼接定理

下面给出无需假定猜想成立的纯结构引理。

### 引理

令 \(G\) 为有限简单图，\(k\geq\Delta(G)\)。若 \(G\) 的每个 block 都有一个
使用至多 \(k\) 色的 acyclic edge-colouring，则 \(G\) 也有这样的染色。

### 证明

先逐连通分量处理；不同分量可以复用同一个 \(k\)-色集合。对一个连通分量，
把它的 block--cut tree 任选根。根 block 先任取一个给定的 acyclic
\(k\)-edge-colouring。

假设一个尚未加入的子 block \(B\) 与已染色部分恰在其父割点 \(v\) 相交。
记已染色部分在 \(v\) 使用的颜色集合为 \(T\)，\(B\) 自己的染色在 \(v\)
使用的颜色集合为 \(S\)。properness 给出

\[
|T|+|S|
\leq d_G(v)
\leq\Delta(G)
\leq k.
\]

因此可把 \(B\) 的整个 \(k\)-色集合做一个全局置换，使置换后的 \(S\) 与
\(T\) 不交；任意从 \(S\) 到 \([k]\setminus T\) 的单射都可以扩充成整个
\([k]\) 的置换。这样拼接后在 \(v\) 仍 proper，其他顶点的 properness 不变。

图中的每个简单圈完全包含在某一个 block 内。因此，不同 block 拼接不会产生
新的双色圈。沿 block--cut tree 重复上述过程即得 \(G\) 的 acyclic
\(k\)-edge-colouring。桥 block \(K_2\) 只需一种颜色，孤立点无边可染。
\(\square\)

### 推论 1：任意反例含有二连通反例 block

令 \(k=\Delta(G)+2\)。若 \(G\) 的每个非平凡 block \(B\) 都满足原猜想，则

\[
a'(B)\leq\Delta(B)+2\leq\Delta(G)+2=k.
\]

由引理可把所有 block 拼成 \(G\) 的 acyclic \(k\)-edge-colouring，与 \(G\)
是反例矛盾。所以任何反例都含有一个 block \(B\)，它本身满足
\[
a'(B)>\Delta(B)+2.
\]
桥和孤立点显然不可能是这样的 block，故 \(B\) 是非平凡二连通简单图。

### 推论 2：最小顶点数反例可取 `-C -d2`

若取顶点数最少的反例 \(G\)，推论 1 迫使 \(G\) 自身就是该二连通 block；
否则会得到顶点数更少的反例。非平凡二连通图至少有 3 个顶点且最小度至少 2。
因此限制到 biconnected 且 \(\delta\geq2\) 没有损失。

也可以直接看出叶点为何不可能出现在最小反例中：删除叶点 \(x\) 后先染色
\(G-x\)，再给叶边 \(xv\) 选择一个在 \(v\) 未使用的颜色。该边不在任何圈中，
所以不会新造双色圈。使用 \(k=\Delta(G)+2\) 色时，\(v\) 处至少还有
\[
k-(d_G(v)-1)\geq3
\]
种颜色可选。

### 推论 3：固定 `Delta = 5` 时仍可用该归约

若 \(G\) 是一个最大度 5、不可 acyclic 7-edge-colour 的图，则 block 拼接
引理说明某个 block \(B\) 也不可用 7 色。若 \(\Delta(B)\leq4\)，上一节的
已知定理反而给出 \(a'(B)\leq6\)，矛盾。因此坏 block 必有
\(\Delta(B)=5\)，且是二连通图。

所以，对固定 \(\Delta=5\) 的**累计阶数搜索**，只枚举二连通图是严格无损的。
这里不需要把各 block 的染色“想当然地”同时重命名；上面按 block--cut tree
逐个附着、每次对整个子 block 做一个颜色置换，才是完整论证。

## 5. `geng` 命令的准确语义

当前搜索器执行

```text
geng -q -C -d2 -D5 n
```

随后只保留

```text
maximum_degree == 5 and not 3_sparse
```

本机固定的 nauty 2.8.8 `geng -help` 与
[nauty 2.8.x 手册](https://manpages.ubuntu.com/manpages/noble/man1/nauty-geng.1.html)
给出：

- `-C`：只输出 biconnected graphs；
- `-d2`：最小度下界 2；
- `-D5`：最大度上界 5；
- 默认 `graph6` 目录是简单图目录。

对本任务的 \(n\geq7\)，`-C` 已蕴含 \(\delta\geq2\)，所以 `-d2` 是冗余但
安全的显式约束。真正限制结论范围的是 `-D5`。

## 6. 十阶计算究竟证明了哪一层

独立审计文件
[`audit-all-v2.json`](../../../artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json)
记录：

- `geng -C -d2 -D5 10` 四分片共生成 734,900 个图；
- 其中 692,136 个是 \(\Delta=5\) 且非 3-sparse，保存的 7 色见证全部重放；
- 42,764 个因 \(\Delta\leq4\) 或 3-sparse 而进入已知正例层；
- 聚合文件 SHA-256 为
  `06aaf69f91322275a664456bfae00324f3d1f863bace3e2d2ca45539932d540a`。

因此，单看十阶审计，可安全写：

> 所有 10 顶点二连通简单图中，最大度恰为 5 的图都满足
> \(a'(G)\leq7\)；非 3-sparse 部分由逐图见证覆盖，3-sparse 部分由已发表
> 定理覆盖。

若再接受 7--9 阶目录的完整性与见证重放，则可加上一个很小的严格基例，得到
固定 \(\Delta=5\) 的累计结论。顶点数小于 6 时不可能有最大度 5；对 6 个顶点，
任意最大度 5 的简单图是 \(K_6\) 的子图。下面给出 \(K_6\) 的显式 acyclic
7-edge-colouring（顶点为 \(0,\ldots,5\)）：

| 颜色 | 边 |
| --- | --- |
| 1 | \(01,25,34\) |
| 2 | \(15,24\) |
| 3 | \(14,23\) |
| 4 | \(04,12\) |
| 5 | \(03,45\) |
| 6 | \(02,35\) |
| 7 | \(05,13\) |

每一色是 matching。颜色 2--7 所遗漏的六个无序顶点对两两不同，故任意两者的并
不可能是一个 4-圈；颜色 1 与颜色 2--7 中任一色的四个端点内都只有一条颜色 1 的边，
故也不可能形成双色 4-圈，而另一颜色只有两条边，不能形成更长的双色圈。因此
该染色 acyclic；限制到任意子图后仍 acyclic。

于是，在 7--9 阶已完整闭合这一计算前提下，可写：

> 不存在顶点数至多 10、最大度恰为 5 的反例。

但无论如何都**不能**从当前命令写出：

> 不存在 10 顶点简单图反例。

因为最大度 \(6\) 至 \(9\) 的十阶二连通简单图没有被 `-D5` 生成。要得到
“全部图到 10 阶”的边界，必须另外完整覆盖这些最大度层，或为它们提供独立的
已知定理；`Delta <= 4`、3-sparse 和 block 归约都不能填补这个缺口。

最后还要区分“单阶”与“累计阶”：

- 搜完**仅仅** \(n=10\) 的二连通图，不能单独排除一个 10 顶点非二连通反例；
  它只保证该反例若存在，则含有一个阶数小于 10 的坏 block。
- 搜完所有相关二连通层直到 \(n=10\)，并严格闭合较小阶基例，才可通过 block
  归约排除所有不超过 10 顶点的对应图。

这一区分是范围表述所必需的，不是生成器或染色判定器的实现问题。
