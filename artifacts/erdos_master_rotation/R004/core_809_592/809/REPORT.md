# Erdős #809 — near-complete-split 坏 hub 三分法

日期：2026-07-24

状态：`NEW_ASYMPTOTIC_SPLIT_BRANCH_LEMMA__ORIGINAL_OPEN`

## 结论

本轮证明了一个新的、可独立使用的渐近引理：若 \(G\) 有一个近半大小的
独立集 \(R\)，其补集为 \(C\)，且

\[
|R|,|C|=(1/2+o(1))n,\qquad
\delta(G)\geq n/2-o(n),\qquad
e(G)>\lfloor n^2/4\rfloor,
\]

则 \(G\) 中存在至少

\[
(1/8-o(1))n^2
\]

条边，两两同处于某个 \(C_7\)。所以任何使每个 \(C_7\) 都是彩虹的
边染色至少使用这么多颜色。该引理完整容纳 R002 的 star-swap 和 R003
的一锚点 fan，并补上了“内部边集中在交叉坏 hub”时的缺口。

这**没有闭合原题 #809**。官网于本轮抓取时仍标为 `OPEN`；本轮证明只
闭合 near-complete-split 结构支。尚无已证归约说明任意 #809 极小反例
必落入该支。BCM 强归纳的稠密 Case 1 可只有
\[
\delta(G)\gtrsim n/2-\sqrt{e-n^2/4},
\]
并不总满足本引理的 \(n/2-o(n)\) 假设；近双团支和归纳接口也未消失。

## 1. 清洗

以下所有 \(o(\cdot)\) 都沿所考察的图序列取值。先把 \(R\) 扩成极大
独立集。若原来的 \(R_0\) 已有 \((1/2-o(1))n\) 个点且交叉缺边为
\(o(n^2)\)，每个新移入 \(R\) 的点都与 \(R_0\) 完全不邻接，故只能
移入 \(o(n)\) 个点。平衡性和交叉近完全性不变。极大性保证

\[
N_R(c)\ne\varnothing\qquad(c\in C).
\]

写 \(a=|C|,\ b=|R|\)。因 \(R\) 独立，对每个 \(z\in R\)，

\[
|C\setminus N(z)|=a-d(z)\leq a-\delta(G)=o(n). \tag{1}
\]

这是后面所有“共同邻点选择”的一致列界。事实上它还自动给出
\(E(C,R)\) 的总缺边数为 \(o(n^2)\)。

为把误差量化，置
\[
\epsilon_n=\max\{(a-\delta(G))/n,1/n\},\quad
\rho_n=\epsilon_n^{1/2},\quad
\tau_n=\epsilon_n^{1/4}.
\]
称一个 \(C\)-行是好的，如果它至多缺 \(\rho_n n\) 条到 \(R\) 的边。
由 (1) 求和，坏行只有 \(O(\rho_n n)=o(n)\) 个，而且
\[
\epsilon_n=o(\rho_n)=o(\tau_n)=o(1). \tag{2}
\]
选择池若有至少 \(\tau_n n\) 个候选点，删去坏行、单列缺点和有限个
禁用顶点后仍非空。

因为 \(e(G)>\lfloor n^2/4\rfloor\)，而
\(|C||R|\leq\lfloor n^2/4\rfloor\)，所以 \(C\) 内有边。固定
\(pq\in E(C)\)，记
\[
Q_p=N_C(p)\setminus\{q\},\quad
Q_q=N_C(q)\setminus\{p\},
\]
\[
h_p=d_C(p),\quad h_q=d_C(q),\quad
I=N_R(p)\cap N_R(q),\quad k=|I|.
\]
取锚点 \(s_p\in N_R(p)\)、\(s_q\in N_R(q)\)。若
\(|Q_p|\geq\tau_n n\)，令
\[
P=Q_p\cap\{\text{好行}\}\cap N_C(s_p);
\]
否则令 \(P=\varnothing\)。类似定义 \(Q\)（中心 \(q\)、锚点
\(s_q\)）。若 \(k<\tau_n n\)，把下面的 core 矩形整体删去。阈值删除
至多损失 \(O(\tau_n n^2)=o(n^2)\)，并由 (1)--(2) 保证每个保留的
hub 有 \(\Omega(\tau_n n)\) 条可选行，每个保留的 core 有
\(\Omega(\tau_n n)\) 个公共列。

## 2. 兼容边族

令 \(U'=P\cup Q\)。构造

\[
\begin{split}
\mathcal H={}&\{xy\in E(C,R):x\in U'\}\\
 &{}\setminus\{xs_p:x\in P\}
 \setminus\{xs_q:x\in Q\},
\end{split}
\]

以及（仅当 \(k\geq\tau_n n\) 时）
\[
\mathcal K
=E\bigl((C_{\rm good}\setminus(U'\cup\{p,q\})),I\bigr).
\]
置 \(\mathcal F=\mathcal H\cup\mathcal K\)。

下面逐案给出同时包含任意两条指定边的简单七圈。小写
\(x,a,c\) 表示 \(C\) 中点，\(y,z,r,s,t\) 表示 \(R\) 中点。所有
未指定的辅助点从大小为 \(\Omega(\tau_n n)\) 或
\((1/2-o(1))n\) 的池中选择，并避开已经出现的有限个点；(1)--(2)
保证所需交叉边同时存在。

### 2.1 两条 core 边

指定边为 \(a_1z_1,a_2z_2\)。

- 行列都不同：取
  \(x\in N_R(a_1)\cap N_R(a_2)\setminus\{z_1,z_2\}\)，用
  \[
  p,q,z_1,a_1,x,a_2,z_2,p.
  \]
- 同行 \(a_1=a_2=a\)：取
  \(x\in I\setminus\{z_1,z_2\}\)，再取
  \(c\in N_C(z_2)\cap N_C(x)\setminus\{p,q,a\}\)，用
  \[
  p,q,z_1,a,z_2,c,x,p.
  \]
- 同列 \(z_1=z_2=z\)：取互异的
  \(x,y\in I\setminus\{z\}\)，分别满足
  \(a_1x,a_2y\in E(G)\)，用
  \[
  p,q,x,a_1,z,a_2,y,p.
  \]

### 2.2 同一个 hub

以 \(p\)-hub 为例；指定边为 \(x_1y_1,x_2y_2\)，且指定列均不等于
\(s_p\)。

- 行列都不同：取 \(c\) 同时邻接 \(y_1,y_2\)，用
  \[
  p,x_1,y_1,c,y_2,x_2,s_p,p.
  \]
- 同行 \(x_1=x_2=x\)：取
  \(x'\in P\setminus\{x\}\) 邻接 \(y_1\)，再取 \(c\) 同时邻接
  \(y_2,s_p\)，用
  \[
  p,x',y_1,x,y_2,c,s_p,p.
  \]
- 同列 \(y_1=y_2=y\)：取
  \(z\in N_R(x_2)\setminus\{y,s_p\}\)，再取 \(c\) 同时邻接
  \(z,s_p\)，用
  \[
  p,x_1,y,x_2,z,c,s_p,p.
  \]

\(q\)-hub 完全对称。同行案正是阈值不可省略的地方：若 hub 只有
0、1、2 条额外内部邻边，本证明不假装存在备用行，而是把整个矩形计入
\(o(n^2)\) 误差。

### 2.3 两个不同 hub

只需考虑 \(x\in P\setminus Q\)、\(t\in Q\setminus P\)；若某行同时
属于 \(P,Q\)，两边可归入同一 hub。指定边为 \(xy,tz\)。

- \(y\ne z\)：取 \(c\) 同时邻接 \(y,z\)，用
  \[
  p,x,y,c,z,t,q,p.
  \]
- \(y=z\)：取
  \(r\in N_R(x)\setminus\{y,s_q\}\)，再取 \(c\) 同时邻接
  \(r,s_q\)，用
  \[
  q,t,y,x,r,c,s_q,q.
  \]

后一模板不需要 \(p,q\) 的任何额外内部邻点，是低度 hub 的边界安全
版本。

### 2.4 一条 core、一条 hub

指定 core 边为 \(az\)，指定 \(p\)-hub 边为 \(xy\)。

- \(z\ne y\)：取 \(t\in N_R(a)\setminus\{y,z\}\)，再取 \(c\)
  同时邻接 \(y,t\)，用
  \[
  p,x,y,c,t,a,z,p.
  \]
- \(z=y\)：取 \(s\in I\setminus\{z\}\)，
  \(t\in N_R(a)\setminus\{z,s\}\)，再取 \(c\) 同时邻接 \(t,s\)，用
  \[
  p,x,z,a,t,c,s,p.
  \]

\(q\)-hub 对称。四大类及其所有同行、同列边界都给出七个互异顶点；
额外弦不妨碍其为一个 \(C_7\) 副本。因此 \(\mathcal F\) 中所有边颜色
互异。

## 3. 计数

记 \(u=|Q_p\cup Q_q|\)。清洗和阈值删除只改变 \(u\) 个
\(o(n)\)，故
\[
|\mathcal F|\geq ub+(a-u)k-o(n^2). \tag{3}
\]
又
\[
u\geq\max(h_p,h_q)-O(1), \tag{4}
\]
且最小度给出
\[
\begin{split}
k
&\geq d_R(p)+d_R(q)-b\\
&\geq 2\delta(G)-b-h_p-h_q\\
&\geq \max\{0,b-h_p-h_q\}-o(n). \tag{5}
\end{split}
\]

令 \(x=\max(h_p,h_q)\)、\(y=\min(h_p,h_q)\)，并用
\(a=b+o(n)\)。式 (3)--(5) 的最坏情形可令 \(u=x\) 及
\(k=\max(0,b-x-y)\)。

- 若 \(x+y\geq b\)，则 \(x\geq b/2\)，hub 已贡献
  \(xb\geq b^2/2\)。
- 若 \(x+y\leq b\) 且 \(x\leq b/2\)，因 \(y\leq x\)，
  \[
  \begin{split}
  xb+(b-x)(b-x-y)
  &\geq xb+(b-x)(b-2x)\\
  &=b^2/2+2(x-b/2)^2\\
  &\geq b^2/2.
  \end{split}
  \]
  \(x\geq b/2\) 时仍由 hub 一项结束。

所以
\[
|\mathcal F|\geq b^2/2-o(n^2)=n^2/8-o(n^2).
\]

## 4. 与原题的接口

R003 的“三步路邻域二分”在 split 支给出独立集
\[
|R|\geq (1/2-3\eta)n-O(1),
\]
其余点到 \(R\) 的交叉缺边为 \(o(n^2)\)，并在
\(\delta=(1/2-\eta)n,\ \eta=o(1)\) 时满足本引理。把该 \(R\)
极大化后，R003 中“交叉坏 hub 可承载全部内部密度”的首断点因此闭合。

但该接口是条件式的：

- BCM Case 1 对一般 \(e\) 的最低度可离 \(n/2\) 线性远；
- R003 的距离 2 证书并未在所有强归纳子问题中产生；
- 证书的另一支是 near-two-clique，而非本引理的 split 图；
- BCM 只说明他们对 \(k=3\) 有更复杂的 Case 2 stability 思路，没有在
  所核读的一手稿中给出可直接引用的完整 \(k=3\) 证明。

因此 `original_closed=false`，不能把局部分支定理升级成 #809 的证明。

## 5. 失败路线：只看 induced matching 不够

若两条同色交叉边不能同处七圈，容易尝试证明每个颜色类在交叉图中是
induced matching，再用“近完全图不能由少量大 induced matchings
分解”计数。这个后半句是假的。Alon--Moitra--Sudakov 构造了
\((1-o(1))\)-稠密图，其边可分解为 \(N^{1+o(1)}\) 个、每个大小
\(N^{1-o(1)}\) 的 induced matchings。随机二分顶点仍给出相应的稠密
二部障碍。故本轮舍弃了这条路线；必须使用内部边 \(pq\) 所提供的
core/hub 七圈几何。

## 6. 机器核验与边界

运行：

```bash
python3 artifacts/erdos_master_rotation/R004/core_809_592/809/verify_809_split_union.py
```

验证器检查 16 个稠密实例及 15 个
\((h_p-1,h_q-1)\in\{0,1,2\}^2\) 或单侧稠密的低度 hub 对抗实例，
逐对验证所给七元组：

1. 有七个互异顶点；
2. 七条圈边都在图中；
3. 两条指定边都在圈上。

共检查 31 个实例、1,022,637 对族内边；十个细分模板类均实际命中。
另在分母 400 的 80,601 个有理点上核对计数最小值恰为 \(1/2\)。

这是模板、顶点互异和代数的有限 guard，不是渐近清洗的有限替代，也不
证明原题。

## 一手来源

- Erdős Problems #809：
  <https://www.erdosproblems.com/809>，本轮快照仍为 `OPEN`。
- Matija Bucić、Patrick Chen、Jie Ma，
  *On a conjecture of Burr, Erdős, Graham and Sós*，
  arXiv:2603.18952v1；核读 Lemma 3.2、Cases 1/2 及文末 \(k=3\)
  边界。
- Noga Alon、Ankur Moitra、Benny Sudakov，
  *Nearly Complete Graphs Decomposable into Large Induced Matchings*，
  JEMS 15 (2013), 1575--1590，DOI `10.4171/JEMS/398`；用于否决
  induced-matching 计数捷径。

## Novelty guard

“新”只表示相对于本仓库 R002/R003 的严格推进：此前断点被一个完整
渐近分支引理替代。本轮没有做足以支持全球首创、同行评审或可发表性的
穷尽文献检索；在外部发表前必须由图论专家独立审稿并扩大检索。
