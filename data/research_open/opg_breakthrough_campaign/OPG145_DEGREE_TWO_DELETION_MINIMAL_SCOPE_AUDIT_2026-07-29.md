# OPG-145 十一阶二度点与 deletion-minimal 结构审计

日期：2026-07-29

## 结论

设 \(G\) 是一个 11 顶点有限简单图，满足
\(\Delta(G)=5\)，并假设 \(G\) 不能 acyclic 7-edge-colour。边数
\(m=23\) 对下面的归约不起作用。

1. 不能因为 \(G\) 按顶点数最小，就直接把 Wang--Zhang 的
   \(\kappa\)-deletion-minimal 引理用于 \(G\)。按顶点数最小只排除了
   更少顶点的坏图，并不保证同阶的 \(G-e\) 可染。
2. 安全做法是先在 \(G\) 的子图中选取一个按 proper-subgraph inclusion
   极小的非 7-可染子图 \(H\)。已审计的
   \(|V|\leq10,\Delta=5\) 边界和已知的 \(\Delta\leq4\) 正例定理共同
   迫使 \(H\) 仍有全部 11 个顶点且 \(\Delta(H)=5\)。这才使 \(H\)
   成为可合法套用文献引理的 7-deletion-minimal 图。
3. 若只采用本地二度点延拓引理和 Wang--Zhang Lemma 3，则拟议的中间
   必要条件是安全的：\(G\) 中每个二度点 \(z\) 的两个邻点 \(x,y\)
   必须相邻、都为 5 度；而且 \(x,y\) 除 \(z\) 外的所有邻点在 \(G\)
   中度数均至少 4。
4. 这条“其余邻点均至少 4”不是 item (B) 单独、直接给出的。
   最直接的来源是 Lemma 3(A)。也可以把 Lemma 3 的主句与 item (B)
   组合，以反证法排除“恰有三个 \(4^+\)-邻点”，再推出至少四个。
5. Wang--Zhang Lemma 4 实际上给出更强结论：在
   \(\kappa\geq\Delta(H)+2\) 的 \(\kappa\)-deletion-minimal 图中，
   二度点的每个邻点度数至少
   \(\kappa-\Delta(H)+4\)。代入
   \((\kappa,\Delta(H))=(7,5)\) 得至少 6，与
   \(\Delta(H)=5\) 矛盾。因此，在接受这条已发表结构引理的前提下，
   **所有 11 顶点、最大度 5、含二度点的图都不可能是反例**；无需把
   \(\delta=2\) 层继续交给 SAT 搜索。

最后一条比拟议的局部过滤严格更强。拟议条件仍是一个正确的中间推论，
但最终范围结论应写成“整个二度点层已排除”，而不是“只需搜索其中一个
残余局部型”。

## 1. 使用的前提

以下前提必须逐条保留，不能隐去量词。

### F1：十阶有限边界

已认证的历史 \(n=7,8,9\) 运行、\(K_6\) 基例、block 拼接归约和
十阶独立审计共同给出：

> 每个至多 10 个顶点、最大度恰为 5 的有限简单图都有 acyclic
> 7-edge-colouring。

认证范围和 provenance 边界见：

- [`OPG145_7_9_HISTORY_AUDIT_2026-07-29.md`](OPG145_7_9_HISTORY_AUDIT_2026-07-29.md)；
- [`OPG145_SCOPE_AUDIT_2026-07-29.md`](OPG145_SCOPE_AUDIT_2026-07-29.md)；
- [`audit-all-v2.json`](../../../artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json)。

若最大度至多 4，则已有文献定理给出
\(a'(X)\leq\Delta(X)+2\leq6\)。因此本报告实际可使用的合并前提是：

\[
 |V(X)|\leq10,\quad \Delta(X)\leq5
 \quad\Longrightarrow\quad a'(X)\leq7.
\tag{F1}
\]

### F2：本地二度点延拓

本地独立证明见
[`OPG145_DEGREE_TWO_EXTENSION_AUDIT_2026-07-29.md`](OPG145_DEGREE_TWO_EXTENSION_AUDIT_2026-07-29.md)。
本报告只用其中两条：

1. 若二度点 \(z\) 的邻点 \(x,y\) 不相邻，则抑制
   \[
   z,\qquad (X-z)+xy
   \]
   后的任意 acyclic 7-edge-colouring 都能延拓回 \(X\)。
2. 若 \(x,y\) 相邻且
   \[
   d_X(x)+d_X(y)\leq 9,
   \]
   则 \(X-z\) 的任意 acyclic 7-edge-colouring 都能用共同缺色
   延拓回 \(X\)。

第二条中的 9 来自相邻情形的
\(d_X(x)+d_X(y)\leq k+2\)，这里 \(k=7\)。

### F3：Wang--Zhang 的精确定义和结构引理

来源是 Tao Wang 和 Yaqiong Zhang，
*Acyclic edge coloring of graphs*，Discrete Applied Mathematics 167
(2014), 290--303；可核对
[arXiv:1302.2405v4](https://arxiv.org/abs/1302.2405) 和
[期刊 DOI](https://doi.org/10.1016/j.dam.2013.12.001)。

文献定义：

> \(H\) 是 \(\kappa\)-deletion-minimal，当且仅当
> \(\Delta(H)\leq\kappa\)、\(a'(H)>\kappa\)，并且每个 proper
> subgraph \(J\subsetneq H\) 都满足 \(a'(J)\leq\kappa\)。

本报告使用的原文结论为：

- Lemma 1：每个 \(\kappa\)-deletion-minimal 图都是 2-connected。
- Lemma 3：若 \(v\) 邻接二度点 \(v_0\)，且
  \(N(v_0)=\{w,v\}\)，则 \(v\) 至少邻接
  \[
  \kappa-d(w)+1
  \]
  个度数至少
  \[
  \kappa-d(v)+2
  \]
  的顶点。
- Lemma 3(A)：若再有
  \(\kappa\geq d(v)+1\) 和 \(wv\in E(H)\)，则上述“至少”数量
  提高为
  \[
  \kappa-d(w)+2,
  \]
  且 \(d(v)\geq\kappa-d(w)+3\)。
- Lemma 3(B)：若
  \(\kappa\geq\Delta(H)+2\)，且 \(v\) **恰好**邻接
  \[
  \kappa-\Delta(H)+1
  \]
  个度数至少
  \[
  \kappa-\Delta(H)+2
  \]
  的顶点，则 \(v\) 的二度邻点数至多
  \[
  d(v)+\Delta(H)-\kappa-3,
  \]
  并且
  \[
  d(v)\geq\kappa-\Delta(H)+4.
  \]
- Lemma 4：若
  \(\kappa\geq\Delta(H)+2\)，则二度点的每个邻点度数至少
  \[
  \kappa-\Delta(H)+4.
  \]

特别重要的是，Lemma 3(B) 有一个“恰好多少个高阶邻点”的前件；它不是
无条件的邻域分类。

## 2. 从十一阶候选安全地取得 deletion-minimal 子图

反设 \(G\) 是 11 顶点、\(\Delta(G)=5\) 且
\(a'(G)>7\)。在所有仍满足 \(a'(H)>7\) 的子图
\(H\subseteq G\) 中，按 proper-subgraph inclusion 选一个极小者。
有限性保证这样的 \(H\) 存在。

由选择方式，

\[
a'(H)>7,\qquad
\forall J\subsetneq H,\quad a'(J)\leq7.
\]

又因为 \(\Delta(H)\leq\Delta(G)=5\leq7\)，所以 \(H\) 确实是
文献定义下的 7-deletion-minimal 图。这里的选择同时允许删边和删点，
不能只在诱导子图或只在删点子图中取极小。

若 \(|V(H)|\leq10\)，则：

- \(\Delta(H)=5\) 时与 (F1) 的已认证有限边界矛盾；
- \(\Delta(H)\leq4\) 时与已知 \(\Delta\leq4\) 正例定理矛盾。

所以

\[
|V(H)|=11,\qquad V(H)=V(G).
\tag{2.1}
\]

同理，\(\Delta(H)\leq4\) 不可能，故

\[
\Delta(H)=5.
\tag{2.2}
\]

这一步是连接“按顶点数边界”和“deletion-minimal 文献引理”的必要桥梁。
一般而言，即使 \(G\) 是最小阶坏图，\(G-e\) 仍与 \(G\) 同阶并可能仍坏，
所以不能省略 \(H\) 的提取而直接声称 \(G\) deletion-minimal。

## 3. 二度点在 \(H\) 中不会消失

设 \(z\) 是 \(G\) 的一个二度点。由 (2.1)，\(z\in V(H)\)，且

\[
d_H(z)\leq d_G(z)=2.
\]

Wang--Zhang Lemma 1 说明 \(H\) 2-connected，因而最小度至少 2。
所以

\[
d_H(z)=2.
\tag{3.1}
\]

因此 \(H\) 保留了 \(G\) 中 \(z\) 的两条边。若
\[
N_G(z)=\{x,y\},
\]
则也有
\[
N_H(z)=\{x,y\}.
\tag{3.2}
\]

这排除了一个常见漏洞：不能让极小坏子图简单地删除二度点或删除它的一条
边，然后仍把 \(G\) 的局部结构强加给 \(H\)。

## 4. 相邻的两个五度邻点

### 4.1 邻点必须相邻

若 \(xy\notin E(H)\)，构造简单抑制图
\[
H^\ast=(H-z)+xy.
\]

它有 10 个顶点，且加入 \(xy\) 只是恢复 \(x,y\) 因删除 \(z\) 而各自
损失的一个度数，所以
\[
\Delta(H^\ast)\leq5.
\]
由 (F1)，\(H^\ast\) 有 acyclic 7-edge-colouring；由 (F2) 的抑制
引理，该染色无条件延拓到 \(H\)，与 \(a'(H)>7\) 矛盾。因此

\[
xy\in E(H)\subseteq E(G).
\tag{4.1}
\]

### 4.2 两个邻点都必须是五度点

\(H-z\) 有 10 个顶点且最大度至多 5，所以由 (F1) 有 acyclic
7-edge-colouring。若
\[
d_H(x)+d_H(y)\leq9,
\]
则 (F2) 的相邻共同缺色引理把任意这样的染色延拓到 \(H\)，仍得矛盾。
故
\[
d_H(x)+d_H(y)\geq10.
\]
结合 \(\Delta(H)=5\)，得到
\[
d_H(x)=d_H(y)=5.
\tag{4.2}
\]

又因为 \(H\subseteq G\) 且 \(\Delta(G)=5\)，(4.2) 还迫使
\[
d_G(x)=d_G(y)=5,\qquad
N_H(x)=N_G(x),\quad N_H(y)=N_G(y).
\tag{4.3}
\]

所以从 \(H\) 得到的端点邻域信息可以安全转回原候选 \(G\)。

## 5. “其余邻点均至少四度”的正确推导

### 5.1 直接使用 item (A)

在 \(H\) 中令
\[
v=x,\qquad v_0=z,\qquad w=y,\qquad\kappa=7.
\]

由 (4.1)--(4.2)，
\[
xy\in E(H),\quad d_H(x)=d_H(y)=5,\quad
7\geq d_H(x)+1.
\]
Lemma 3(A) 的全部前件成立，故 \(x\) 至少邻接
\[
\kappa-d_H(y)+2=7-5+2=4
\]
个度数至少
\[
\kappa-d_H(x)+2=7-5+2=4
\]
的顶点。

\(x\) 总共只有 5 个邻点，其中 \(z\) 是二度点。因此 \(x\) 除 \(z\)
外的全部四个邻点都为 \(4^+\)-顶点。交换 \(x,y\) 得到同一结论。
再用 (4.3) 和子图中度数不超过超图中度数，结论传回 \(G\)：

\[
\begin{aligned}
&N_G(x)\setminus\{z\}\subseteq
 \{u:d_G(u)\geq4\},\\
&N_G(y)\setminus\{z\}\subseteq
 \{u:d_G(u)\geq4\}.
\end{aligned}
\tag{5.1}
\]

### 5.2 item (B) 到底能推出什么

把 \((\kappa,\Delta(H))=(7,5)\) 代入 Lemma 3(B)，其前件变为：

> \(x\) 恰好邻接 \(7-5+1=3\) 个度数至少
> \(7-5+2=4\) 的顶点。

只有在这个“恰好三个”的前件成立时，item (B) 才给出

\[
\#\{\text{\(x\) 的二度邻点}\}
\leq d_H(x)+5-7-3=d_H(x)-5
\tag{5.2}
\]
以及
\[
d_H(x)\geq7-5+4=6.
\tag{5.3}
\]

(5.3) 已直接违反 \(\Delta(H)=5\)；而在已知 \(d_H(x)=5\) 后，
(5.2) 也声称 \(x\) 没有二度邻点，与 \(xz\in E(H)\) 矛盾。因此
item (B) 的准确作用是：

\[
x\text{ 不可能恰有三个 }4^+\text{-邻点}.
\tag{5.4}
\]

另一方面，Lemma 3 的主句在
\[
d_H(y)=d_H(x)=5
\]
时只先给出 \(x\) 至少有
\[
7-5+1=3
\]
个 \(4^+\)-邻点。把“至少三个”和 (5.4) 结合，并注意 \(x\) 除二度点
\(z\) 外最多只有四个邻点，才得到“恰有四个”，进而得到 (5.1)。

所以如下两种写法需要区分：

- **安全且直接：** Lemma 3(A) 推出至少四个；
- **安全但需组合：** Lemma 3 主句给至少三个，item (B) 排除恰好三个；
- **不安全：** 声称 item (B) 本身无条件断言所有其余邻点均为 \(4^+\)。

## 6. 更强的 Lemma 4 完全排除二度点层

前面的局部分类已足以证明用户提出的残余条件。但同一篇论文紧接着给出的
Lemma 4 更强。

对 7-deletion-minimal 图 \(H\)，由 (2.2)
\[
\kappa=7=\Delta(H)+2.
\]
若 \(z\) 是二度点，Lemma 4 要求其每个邻点的度数至少
\[
\kappa-\Delta(H)+4=7-5+4=6.
\]
这与 \(\Delta(H)=5\) 矛盾。因此 \(H\) 不含二度点；但 (3.1) 又说明
原候选 \(G\) 的任意二度点在 \(H\) 中仍是二度点。矛盾。

于是得到范围定理：

> **范围定理。** 假设 (F1) 的十阶认证边界及 Wang--Zhang Lemma 1
> 和 Lemma 4。则每个 11 顶点、最大度 5、含二度点的有限简单图都有
> acyclic 7-edge-colouring。

这个证明没有使用 \(m=23\)，所以覆盖所有边数。它也没有声称 OPG-145
一般猜想已经解决；它只排除了指定的十一阶、最大度 5、含二度点层。

## 7. 信任边界与搜索建议

1. 本报告逐项核对了 arXiv v4 和期刊元数据中的
   \(\kappa\)-deletion-minimal 定义、Lemma 1、Lemma 3(A)/(B) 和
   Lemma 4，并独立完成了参数代入、极小子图桥接和从 \(H\) 到 \(G\)
   的度数传递。
2. 本报告没有从头形式化重证 Wang--Zhang Lemma 3 和 Lemma 4 中较长的
   换色论证；最终排除 \(\delta=2\) 层依赖这篇已发表论文的结构引理。
3. 若暂时只愿意采用 Lemma 3(A)，不采用更强 Lemma 4，则 (5.1) 仍是
   安全的残余搜索过滤条件。
4. 若接受 Lemma 4，则十一阶 \(\Delta=5\) 搜索可严格限制为
   \(\delta\geq3\)。已有的 \(\delta=2\) 计算可以保留为经验性独立复核，
   但不再是闭合该范围所必需的主证据。
5. 不能把这项归约扩大到尚未有低一阶完整边界的任意阶数：若极小坏子图
   能删去原图的二度点并落在同样未知的阶数，局部信息未必能从极小子图
   传回原图。这里之所以安全，关键正是 (F1) 迫使 \(H\) 保留全部
   11 个顶点。
