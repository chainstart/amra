# OPG-1757：完全分裂图的两轨道 Rayleigh 证书与一般 \(s\) 低次数层

日期：2026-07-29

## 0. 结论先行

本轮得到四个严格、可复算但强度不同的结果。

**定理 A（有限核心、任意页数）。** 令

\[
S_{s,r}=K_s\vee\overline{K_r},\qquad 3\le s\le 7,\quad r\ge0.
\]

给每条 \(K_s\) 内的核心边统一活动度 \(\alpha>0\)，给每条
核心--独立点边（下称 spoke）统一活动度 \(\beta>0\)。则对
\(S_{s,r}\) 的任意两条不同边 \(e,f\)，加权随机森林满足

\[
\mathbb P(e,f)\le \mathbb P(e)\mathbb P(f).
\]

这里 \(r\) 没有枚举上界；证书一次覆盖全部整数 \(r\ge0\)。

**定理 B（任意核心、最难轨道的稳定低次数层）。** 对任意
\(s\ge4\)，取两条不相邻核心边 \(e=01,f=23\)。把其
Rayleigh 分子的正因子规范化多项式记作 \(P_s(\alpha,\beta,t)\)，其中
\(t=r\)。则

\[
[\alpha^2\beta^d]P_s\ge0
\quad\text{对 }4\le d\le24
\]

有更强的系数证书：令 \(u=s-4\)，每一层都能写成

\[
[\alpha^2\beta^d]P_s
=
\sum_{k,q}c_{d,k,q}
   \binom tk\binom uq,
\qquad c_{d,k,q}\in\mathbb Z_{\ge0}.
\]

**定理 C（下一核心次数层）。** 同一轨道和规范化下，

\[
[\alpha^3\beta^d]P_s
=
\sum_{k,q}c^{(3)}_{d,k,q}\binom tk\binom uq,
\qquad c^{(3)}_{d,k,q}\in\mathbb Z_{\ge0},
\quad 2\le d\le24.
\]

这两个结果真正对全部 \(s\ge4,r\ge0\) 成立，不是用有限个 \(s\) 猜测
趋势；有限差分为何严格见第 5 节。

**定理 D（全次数首个页汇总层与 TP2 障碍）。** 若把
\(P_s^{(2)}=\sum_n\binom tnB_n(s,\beta)\)，则

\[
B_0=B_1=0,\qquad
B_2=4\beta^4(1+2\beta)^{2s-6}(1+s\beta)^{2s-8}.
\]

所以第一个非零 \(t\)-Newton 层已对任意 \(s\) 和全部 \(\beta\) 次数
证明为正；第二个非零层 \(B_3\) 也有全次数正闭式。但逐 \((j,k)\)
的更强 TP2 命题为假，精确公式与障碍见第 5.7 节。

**固定页推进。** 后续轮次已经依次关闭 \(B_4,B_5,B_6,B_7\) 的
全 \(s\) 逐系数非负性。一般 \(k\) 的 determinant 公因子、交替闭式、
\(\beta^4\) 首项和精确次数
\(\deg_\beta K_k=4(k-2)\) 也已证明；\(K_k\) 的前四个低端系数已有
显式非负公式，且
\(\min\deg_\beta F_k=2(k-2)\) 已一般证明。尚未证明的是一般 \(k\)
其余中间系数正性和 \(F_k\) 统一正性。

必须同时强调边界：

- 定理 A 只有两个轨道活动度 \((\alpha,\beta)\)，**不是**每条边可独立
  取权的完整多变量 I-Rayleigh 定理；
- 定理 B/C 只覆盖一个边对轨道、\(\alpha^2,\alpha^3\) 两层和
  上述有限 \(\beta\) 范围，不是任意 \(s\) 的完整结论；
- 当前成果是严谨的新论文胚胎，但单独还不足以稳妥宣称中科院 1 区成果。

## 1. 定义和需要证明的量

写加权森林生成多项式为

\[
Z_G(\mathbf y)
=
\sum_{F\subseteq E(G),\,F\ {\rm forest}}
\prod_{a\in F}y_a.
\]

\(Z_e\)、\(Z_f\)、\(Z_{ef}\) 分别表示包含相应指定边的森林权重和，
并且包含指定边自己的活动度。边负相关等价于

\[
\Delta_G(e,f):=Z_eZ_f-Z_GZ_{ef}\ge0.
\]

完全分裂图的自同构群在所用两轨道赋权下把边对分成：

1. 两条相邻核心边；
2. 两条不相邻核心边（\(s\ge4\)）；
3. 核心边与 incident spoke；
4. 核心边与 nonincident spoke；
5. 同一独立点上的两条 spoke；
6. 不同独立点、同一核心端点的两条 spoke；
7. 不同独立点、不同核心端点的两条 spoke。

\(s=3\) 没有第 2 类，故有六类；\(s\ge4\) 有七类。覆盖这些代表元即覆盖
全部不同边对。

## 2. 核心分区 transfer

### 2.1 状态

处理完核心边和若干独立点后，只记录 \(s\) 个核心顶点当前的连通分区
\(\pi\)。状态数是 Bell 数：

\[
B_3=5,\ B_4=15,\ B_5=52,\ B_6=203,\ B_7=877.
\]

若一个新独立点选择 spoke 端点集合 \(M\subseteq[s]\)，则这一步保持无环
当且仅当 \(M\) 在 \(\pi\) 的每个块中至多取一个顶点。合法时，把 \(M\)
所命中的分区块合并；贡献权重 \(\beta^{|M|}\)。

### 2.2 核心向量不需要枚举 \(2^{\binom s2}\)

给定需要强制出现的核心森林 \(A\)，考虑目标分区 \(\pi\)。若 \(A\) 有边
跨越 \(\pi\) 的不同块，或在某块内成环，则该状态系数为零。

否则，对每个块 \(B\in\pi\)，设 \(A|_B\) 的连通块大小为
\(q_1,\ldots,q_c\)。Cayley--Moon 含指定森林的生成树公式给出

\[
\#\{K_{|B|}\text{ 的生成树包含 }A|_B\}
=
|B|^{c-2}\prod_{i=1}^c q_i.
\]

因此核心初始向量的该状态系数为

\[
\alpha^{s-|\pi|}
\prod_{B\in\pi}
\left(
 |B|^{c_B-2}\prod_i q_{B,i}
\right).
\]

代码用此闭式替代了核心边子集枚举。作为检查，\(\alpha=1\) 时得到
\(K_3,\ldots,K_7\) 的森林数

\[
7,\ 38,\ 291,\ 2932,\ 36961.
\]

### 2.3 nilpotent 分解

记一个不强制 spoke 的独立点 transfer 为 \(U_s(\beta)\)。空集和 \(s\)
个单点选择都不改变核心分区，所以每个对角元都是

\[
\lambda=1+s\beta.
\]

令

\[
N=U_s-\lambda I.
\]

\(N\) 的每个非零转移都至少合并两个当前分区块，故严格减少块数。因此

\[
N^s=0
\]

并且对任意整数 \(n\ge0\)，有精确恒等式

\[
U_s^n
=
\lambda^n
\sum_{j=0}^{s-1}
\binom nj\frac{N^j}{\lambda^j}.
\]

这就是“一次符号计算覆盖所有 \(r\)”的原因。强制一个或两个指定 spoke
的页用 \(T_M\) 表示：仍枚举该页的全部合法端点集，但要求其包含强制集合
\(M\)。

## 3. 七个轨道的精确计数和正因子

对一个边对轨道，先把含指定边的一个或两个独立点放在最前面处理，剩余普通
独立点数记为 \(t\)：

| 轨道 | \(t\) |
|---|---:|
| 核心--核心 | \(r\) |
| 核心--spoke；同页 spoke--spoke | \(r-1\) |
| 异页 spoke--spoke | \(r-2\) |

每个 \(Z,Z_e,Z_f,Z_{ef}\) 都是一个核心向量、零至两个 \(T_M\) 与
\(U_s^{t+c}\) 的矩阵表达式。提出共同的 \(\lambda^{2t+m}>0\) 后，四项的
\(\lambda\) 次数由代码自动对齐；同页两 spoke 的 \(ZZ_{ef}\) 项会比
\(Z_eZ_f\) 多一个显式 \(\lambda\)，这一点已包含在证书中。

把剩余有理式乘以正分母，可取规范化分母

\[
\begin{array}{c|c}
\text{轨道类型}&\text{分母}\\ \hline
\text{核心--核心}&(1+s\beta)^{2s-4}\\
\text{核心--spoke}&(1+s\beta)^{2s-3}\\
\text{spoke--spoke}&(1+s\beta)^{2s-2}.
\end{array}
\]

例如核心--核心的最低 \(\alpha\) 层中：

- 无强制核心边的状态有 \(s\) 个块，最高 \(N\) 次数为 \(s-1\)；
- 强制一条核心边的状态有 \(s-1\) 个块，最高次数为 \(s-2\)；
- 强制两条不相邻核心边的状态有 \(s-2\) 个块，最高次数为 \(s-3\)。

所以 \(Z_eZ_f\) 的最大分母次数是 \(2(s-2)\)，而
\(ZZ_{ef}\) 是 \((s-1)+(s-3)\)，两者都恰为 \(2s-4\)。

## 4. 定理 A 的 Newton 系数证书

对每个固定 \(s\) 和轨道，程序把正分母后的分子精确展开为

\[
P_{s,\mathrm{orbit}}(\alpha,\beta,t)
=
\sum_{i,j,k}c_{i,j,k}
\alpha^i\beta^j\binom tk.
\]

从普通 \(t^k\) 基到 \(\binom tk\) 基使用整数前向差分：

\[
p(t)=\sum_k\Delta^kp(0)\binom tk.
\]

证书逐行保存所有非零 \(c_{i,j,k}\)。所有保存系数均严格为正，因此对
\(\alpha,\beta>0\) 和整数 \(t\ge0\)，分子非负。

汇总如下：

| \(s\) | 状态数 | 边对轨道 | Newton 非零行 | 普通幂基负系数 |
|---:|---:|---:|---:|---:|
| 3 | 5 | 6 | 174 | 0 |
| 4 | 15 | 7 | 634 | 3 |
| 5 | 52 | 7 | 1570 | 7 |
| 6 | 203 | 7 | 3150 | 13 |
| 7 | 877 | 7 | 5542 | 20 |

普通幂基负项全部集中在“不相邻核心边”轨道。这说明普通单项式系数正性
不是正确证明基底；Newton 基不是装饰，而是消除真实符号障碍所必需。

## 5. 定理 B/C：任意 \(s\) 的
\(\alpha^2\beta^{4\ldots24}\) 与
\(\alpha^3\beta^{2\ldots24}\) 层

### 5.1 为什么只需三个 block-size profile

取 \(e=01,f=23\)。在 \(\alpha^2\) 层，四个计数只可能使用最少的强制
核心边，故三个相关核心状态分别是

\[
\begin{aligned}
z &: (1,1,\ldots,1),\\
e &: (2,1,\ldots,1),\\
ef&: (2,2,1,\ldots,1).
\end{aligned}
\]

在 profile \((w_1,\ldots,w_m)\) 上，一次 \(N\) 转移选择若干不同当前块，
从第 \(i\) 块选择实际 spoke 端点有 \(w_i\) 种，因此该转移重数是
\(\prod_{i\in M}w_i\)，目标 profile 把这些块大小替换为其总和。于是无需
保留块内标签，profile transfer 仍精确计算
\(\sum_\pi(N^jv)_\pi\)。

### 5.2 有限插值为何是严格恒等式

令 \(u=s-4\)。在 \(N^j\) 的 \(\beta^d\) 项中，有 \(j\) 个有序页端点集，
总 spoke incidence 恰为 \(d\)。除四个标记核心顶点外，这一记录至多涉及
\(d\) 个匿名核心顶点。

按它恰好使用 \(q\) 个匿名顶点分类。固定抽象 incidence pattern 后，从
\(u\) 个匿名顶点中嵌入该 pattern 的数目是
\(\binom uq\) 乘一个与 \(u\) 无关的整数。因此每个 chain sum 都具有形式

\[
\sum_{q=0}^d a_q\binom uq,
\]

是 \(u\) 的次数至多 \(d\) 的多项式。用
\(u=0,1,\ldots,d\) 的 \(d+1\) 个**精确整数**值即可唯一确定它；这不是
数值拟合。实现统一使用 \(u=0,\ldots,D\)，其中 \(D\) 是目标最大
\(\beta\) 次数。

\(t\) 方向不依赖插值：\(U^t\) 的 nilpotent 恒等式直接给出
\(\binom tj\)。因每个 \(N\)-页至少有两个 spoke，
\(\beta^d\) 层的 \(t\)-Newton 次数至多 \(\lfloor d/2\rfloor\)。

### 5.3 规范化与有限 \(s\) 证书是同一个分子

在 \(\alpha^2\) 层，提出实际计数的共同正因子 \(\lambda^{2t}\) 后，剩余
差是

\[
R_e^2-R_zR_{ef}.
\]

定义

\[
P_s^{(2)}(\beta,t)
=
\lambda^{2s-4}(R_e^2-R_zR_{ef}),
\qquad \lambda=1+s\beta.
\]

第 3 节的最大 nilpotent 阶数说明乘数恰是核心--核心有限 \(s\) 证书使用的
分母，不是另选一个会混合 \(\beta\) 层的任意正因子。

进一步的独立符号检查对 \(s=4,5,6\) 直接从 raw margin 乘
\((1+s\beta)^{2s-4}\)，所得分母严格为 1；逐项抽取
\(\alpha^2\beta^4,\ldots,\alpha^2\beta^{12}\)，全部与一般 \(s\) profile
公式相同。

### 5.4 前三层显式公式

低三层已经能简洁写出：

\[
[\alpha^2\beta^4]P_s
=4\binom t2,
\]

\[
[\alpha^2\beta^5]P_s
=8(s^2-2s-6)\binom t2,
\]

以及

\[
\begin{aligned}
[\alpha^2\beta^6]P_s
={}&4(2s^4-9s^3-12s^2+44s+84)\binom t2\\
&+12(s^2+s-18)\binom t3.
\end{aligned}
\]

把 \(s=u+4\) 后，这些 \(s\)-多项式再次具有非负 Newton 系数。例如
\(\beta^6\binom t2\) 的 \(u\)-Newton 行是

\[
(16,500,1240,840,192),
\]

而 \(\beta^6\binom t3\) 的行是

\[
(24,120,24).
\]

普通幂基的第一个稳定负项

\[
-2\alpha^2\beta^4t
\]

并非反例，因为它与 \(+2\alpha^2\beta^4t^2\) 精确合成

\[
4\alpha^2\beta^4\binom t2.
\]

第一版 JSON 给出 \(d=7,\ldots,12\) 的所有双 Newton 行；没有负系数。
观察到的消失规律是：

- 所有行的 \(t\)-阶至少为 2；
- \(d=7,\ldots,10\) 的 \(u^0\)-Newton 行消失；
- \(d=11,12\) 的 \(u^0,u^1\)-Newton 行消失。

在该范围内，最小 \(u\)-阶为
\(\lfloor(d-3)/4\rfloor\)。这与固定 \(u\) 时该
\(\alpha^2\) 分子的最高 \(\beta\) 次数每增加一个匿名核心顶点便增加 4
相符。

### 5.5 扩展到 \(\beta^{24}\) 和 \(\alpha^3\)

为避免高次符号插值，扩展程序直接在严格次数界所需的整数网格上求最终层，
再作二维前向差分。一个 \(\beta^m\) chain record 至多涉及 \(m\)
个匿名核心顶点；若另外 \(\ell\) 次来自规范化因子，则其系数
\(\binom{2s-4-j-k}{\ell}s^\ell\) 的 \(s\)-次数为 \(2\ell\)。
因此总 \(\beta^d\) 下，\(\alpha^2\) 层的安全 \(u\)-次数界是 \(2d\)；
在 \(\alpha^3\) 层，额外一条核心边至多再引入两个匿名顶点，故界为
\(2d+2\)。每个 \(N\)-页至少使用两条 spoke，故 \(t\)-次数至多
\(\lfloor d/2\rfloor\)。相应的有限网格因此唯一确定整个多项式。

\(\alpha^3\) 的初始 profile 不是猜测，而是把一条可选核心边加入最小
profile 后逐类计数。写 \(E_0,Z_0,EF_0\) 为第 5.1 节三个最小向量，
则

\[
\begin{aligned}
E_1={}&2(s-2)(3,1,\ldots)+\binom{s-2}{2}(2,2,1,\ldots),\\
Z_1={}&\binom s2(2,1,\ldots),\\
EF_1={}&4(4,1,\ldots)+4(s-4)(3,2,1,\ldots)\\
&+\binom{s-4}{2}(2,2,2,1,\ldots).
\end{aligned}
\]

于是规范化后的 \(\alpha^3\) 层严格为

\[
2E_0E_1-Z_0EF_1-Z_1EF_0.
\]

最终证书统计为：

| 层 | \(\beta\) 范围 | 双 Newton 非零行 | 负行 |
|---|---:|---:|---:|
| \(\alpha^2\) | \(4\ldots24\) | 2156 | 0 |
| \(\alpha^3\) | \(2\ldots24\) | 2872 | 0 |

最低两层尤其简单：

\[
[\alpha^3\beta^2]P_s=4\binom t1,\qquad
[\alpha^3\beta^3]P_s=
\left(40+56u+16\binom u2\right)\binom t1.
\]

### 5.6 全次数正递推及剩余的符号缺口

设 profile \(p\) 中大小为 \(w\) 的块有 \(c_w\) 个。令
\(V^{(j)}_p(x)\) 记录做完 \(j\) 个 nilpotent 页后落在 \(p\) 的
spoke 次数生成函数。若下一页从大小 \(w\) 的块中选择 \(k_w\) 个，
\(K=\sum_wk_w\ge2\)，则严格递推是

\[
V^{(j+1)}_{\operatorname{merge}(p,\mathbf k)}(x)
\mathrel{+}=
V^{(j)}_p(x)
\prod_w\binom{c_w}{k_w}w^{k_w}x^K.
\]

它逐项非负，并且一次给出所有 \(\beta\) 次数；程序的“按块大小聚合”
正是此式。若 \(A_{p,j}(x)=\sum_qV^{(j)}_q(x)\)，则全部
\(\alpha^2\) 层的精确生成恒等式为

\[
\sum_{j,k\ge0}\binom tj\binom tk
(1+sx)^{2s-4-j-k}
\left(A_{E,j}A_{E,k}-A_{Z,j}A_{EF,k}\right).
\]

因此全次数问题已收缩为：证明这个 profile-transfer 核关于
\((Z,E,EF)\) 的二阶 minor 在 \(t,u\) 双 Newton 基中非负。正递推本身
尚未消除括号内的减法，故不能把 \(d\le24\) 外推为所有 \(d\)；但连续
21 层及下一 \(\alpha\) 层均无负行，为“核的离散全正性”提供了明确、
可证伪的主猜想。首个尚未控制层现在是
\(\alpha^2\beta^{25}\) 和 \(\alpha^3\beta^{25}\)；\(\alpha^4\) 及更高层
也仍待一般化。

### 5.7 TP2 强命题的严格障碍与正确的汇总层级

把三个初始 profile 依次编号为 \(i=0,1,2\)，并令

\[
A_{i,j}(\beta)=\sum_d a_{i,j,d}\beta^d
\]

为从第 \(i\) 个 profile 出发，作用 \(N^j\) 后对全部终态求和的生成
多项式。再定义

\[
R_i(s,t,\beta)
=
\sum_{j\ge0}\binom tj\frac{A_{i,j}(\beta)}{\lambda^j}.
\]

则全次数缺口精确等价于证明

\[
P_s^{(2)}
=
\lambda^{2s-4}\left(R_1^2-R_0R_2\right)\ge0.
\]

因此目标确实是 profile 收缩序列 \(R_0,R_1,R_2\) 的系数对数凹。
但是，把它加强为每个固定 \((j,k)\) 的 TP2 是错误的。

**障碍定理。** 对每个 \(s\ge4\)，固定 \((j,k)=(0,1)\) 后的对称
minor 严格满足

\[
2A_{1,0}A_{1,1}-A_{0,0}A_{2,1}-A_{0,1}A_{2,0}
=-\beta^4(1+\beta)^{s-4}.
\]

尤其它从 \(\beta^4\) 起逐项为负。更强的“逐终态 profile”命题更早
失败：最小反例是 \(s=4,j=0,k=1,\beta^2\)，终态对

\[
((1,1,1,1),(4))
\]

的系数为 \(-4\)。因此不存在保持有序 nilpotent 页数 \((j,k)\) 或同时
保持两个终态 profile 的逐层正注入。

同样，这排除了一个常见但过强的 Lindström 方案：若
\((A_{i,j})\) 本身来自保持 \(j\) 与 \(\beta\) 分级、边权逐项非负的
平面路径网络，则 LGV 引理会把上述二阶 minor 写成不交路径族的非负和，
与显式负式矛盾。该 no-go 不排除先忘掉两条路径各自的 \(j,k\)，按页集合
并集大小 \(n\) 汇总后再构造网络；后者正是仍可能成立的版本。

证明只需一页的 elementary-symmetric 生成函数。令
\(q=1+\beta\)、\(a=1+2\beta\)。包含空集和单点选择的一页多项式分别是

\[
q^s,\qquad aq^{s-2},\qquad a^2q^{s-4}.
\]

从每个式子减去共同的不合并项 \(\lambda=1+s\beta\)，便得到
\(A_{0,1},A_{1,1},A_{2,1}\)。由于

\[
q^2-a=\beta^2,
\]

直接展开即得上述负恒等式。另一方面，对角 minor 恰为

\[
A_{1,1}^2-A_{0,1}A_{2,1}
=\lambda\beta^4(1+\beta)^{s-4}.
\]

乘上各自的规范化幂后，\((0,1)+(1,0)\) 层与 \((1,1)\) 层分别为

\[
-\lambda^{2s-5}\beta^4(1+\beta)^{s-4},
\qquad
+\lambda^{2s-5}\beta^4(1+\beta)^{s-4}.
\]

又因

\[
\binom t1^2=\binom t1+2\binom t2,
\]

它们在 \(t\)-Newton 一阶精确抵消。这给出一个严格的代数
sign-reversing cancellation identity：负层必须与“两条链使用同一活动页”的 overlap
记录配对。它尚不是全次数的组合注入，但明确说明成功注入必须允许改变
\((j,k)\)，同时保存两链活动页集合的并集，而不能分别保存活动页数。

一般地，

\[
\binom tj\binom tk
=
\sum_{h=0}^{\min(j,k)}
\frac{(j+k-h)!}{h!(j-h)!(k-h)!}
\binom t{j+k-h}.
\]

这个汇总层级已经能给出一个新的全次数闭式，而不只是障碍。写

\[
P_s^{(2)}=\sum_{n\ge0}\binom tn B_n(s,\beta).
\]

上述抵消证明 \(B_0=B_1=0\)。第一个非零层对所有 \(s\ge4\) 满足

\[
\boxed{
B_2(s,\beta)
=4\beta^4(1+2\beta)^{2s-6}(1+s\beta)^{2s-8}.
}
\]

证明只需完整处理两个实际页。若收缩后各核心块大小为
\(\mathbf w=(w_1,\ldots,w_m)\)，令 \(X_i=1+2w_i\beta\)。一个 spoke
森林可以让每个块不连页、只连第一页或只连第二页；至多一个块能同时连
两个页，否则两个这样的块形成四环。因此两页森林多项式恰为

\[
H(\mathbf w)
=
\prod_iX_i
+\beta^2\sum_iw_i^2\prod_{\ell\ne i}X_\ell.
\]

分别代入

\[
(1^s),\qquad(2,1^{s-2}),\qquad(2,2,1^{s-4})
\]

并直接约去公因子，得到

\[
H_1^2-H_0H_2=4\beta^4(1+2\beta)^{2s-6}.
\]

实际两页 determinant 与规范化 \(P_s^{(2)}\) 相差
\(\lambda^{2s-8}\)，即得方框公式。因此至少第一个非零
\(t\)-Newton 层已经对任意 \(s\) 和全部 \(\beta\) 次数严格解决。

三页也能完整处理。此时令

\[
X_i=1+3w_i\beta,\quad
S_2=\sum_i\frac{w_i^2}{X_i},\quad
S_3=\sum_i\frac{w_i^3}{X_i},\quad
S_4=\sum_i\frac{w_i^4}{X_i^2}.
\]

多页连接块在三个页上诱导一个森林：可以有一个连接三个页的块，或至多
两个分别连接不同页对的块。故精确枚举为

\[
H^{(3)}(\mathbf w)
=
\prod_iX_i
\left(1+3\beta^2S_2+\beta^3S_3
+3\beta^4(S_2^2-S_4)\right).
\]

令 \(x=1+3\beta\)、\(z=1+2\beta\)，并写

\[
K_s
=1+12\beta+(6s+30)\beta^2
+28s\beta^3+6s^2\beta^4.
\]

代入三个 profile 后得到

\[
(H^{(3)}_1)^2-H^{(3)}_0H^{(3)}_2
=12\beta^4x^{2s-8}K_s.
\]

由于 \(P_s^{(2)}(3)=3B_2+B_3\)，当 \(s\ge5\) 时

\[
\boxed{
B_3
=12\beta^4\lambda^{2s-10}
\left(x^{2s-8}K_s-z^{2s-6}\lambda^2\right).
}
\]

\(s=4\) 的约简式是 \(B_3=24\beta^6\)。

还需说明方框内的差为何逐项为正。令 \(m=2s-8\)，则
\(\lambda=1+(m/2+4)\beta\)，并把 \(K_s\) 写作 \(K_m\)。令

\[
L_m=x^mK_m-z^{m+2}\lambda^2.
\]

对偶数 \(m\ge2\)，用 \(x=z+\beta\) 展开前三项，严格得到

\[
L_m
=z^{m-2}E_m
+\sum_{r=3}^m\binom mr\beta^rz^{m-r}K_m,
\]

其中

\[
\begin{aligned}
E_m={}&
\frac{m^2+18m+8}{4}\beta^2
+(7m^2+42m+24)\beta^3\\
&+\frac{3m^3+82m^2+314m+208}{2}\beta^4\\
&+\frac{(m+8)(17m^2+62m+48)}{2}\beta^5\\
&+\frac{(m+8)^2(3m^2+9m+8)}{4}\beta^6.
\end{aligned}
\]

右边每一项都系数非负，且非零层严格为正。\(m=0\) 时直接有
\(L_0=2\beta^2(1+4\beta)^2\)，恰好约去方框公式中的
\(\lambda^{-2}\)。因此 \(B_3\) 也已对任意 \(s\ge4\) 和全部
\(\beta\) 次数证明为正。

令 \(B_n(s,\beta)\) 为按此式汇总到 \(\binom tn\) 的系数。新的完整小
参数审计对每个 \(4\le s\le12\) 展开了整个 \(\beta\) 多项式，而不只是
截断前缀：一个从 \(b\) 个块出发的 \(j\)-页记录次数至多
\((b-1)+j\)，故规范化总次数安全界为 \(4s-8\)，统一取
\(\beta^{0\ldots40}\) 已覆盖 \(s\le12\)。

所得 1140 个非零 \(B_n\) 系数全部严格为正，而且支撑精确是

\[
2\le n\le2s-5,\qquad 2n\le d\le4s-10.
\]

这把最可信的全次数猜想收缩为：

> 对每个 \(s\ge4\)，先按活动页并集大小 \(n\) 汇总后，
> \(B_n(s,\beta)\) 系数非负。

它比错误的逐 \((j,k)\) TP2 弱，但若证明，已经足以推出全部
\(r\ge0\) 的 \(\alpha^2\) 层。当前尚无对任意 \(s\) 的
Lindström 网络或显式注入；有限 \(s\) 全展开不能替代该证明。

### 5.8 四页闭式、二部树组分递推与剩余障碍

固定实际页数 \(n\) 后，可以反过来处理收缩核心块，只记录 \(n\) 个页
当前的连通分区。大小为 \(w\) 的核心块选择 \(k\) 个不同页分量时，贡献
\(w^k\beta^k\) 并合并这些分量。权 1 块的转移满足

\[
U_1=(1+n\beta)I+N,\qquad N^n=0.
\]

因此任意符号个权 1 块只需 Bell 数 \(B_n\) 个状态和 \(n\) 个
nilpotent 项。四页只有 \(B_4=15\) 个状态，精确计算给出

\[
D_4:=\big(H_1^{(4)}\big)^2-H_0^{(4)}H_2^{(4)}
=24\beta^4(1+4\beta)^{2s-10}K_s^{(4)},
\]

其中

\[
\begin{aligned}
K_s^{(4)}={}&1+28\beta+(14s+288)\beta^2
+(292s+1264)\beta^3\\
&+(75s^2+1918s+2008)\beta^4
+(968s^2+4064s)\beta^5\\
&+(160s^3+3072s^2)\beta^6
+1024s^3\beta^7+128s^4\beta^8.
\end{aligned}
\]

这个实际四页 determinant 本身已经显然逐项为正。由于

\[
P_s^{(2)}(4)=6B_2+4B_3+B_4,
\]

令 \(\lambda=1+s\beta\)，可抽出

\[
\boxed{
\begin{aligned}
B_4={}&24\beta^4\lambda^{2s-12}L_s^{(4)},\\
L_s^{(4)}={}&
(1+4\beta)^{2s-10}K_s^{(4)}
-2\lambda^2(1+3\beta)^{2s-8}K_s\\
&+\lambda^4(1+2\beta)^{2s-6}.
\end{aligned}}
\]

边界情形为

\[
B_4|_{s=4}=0,\qquad
B_4|_{s=5}
=288\beta^8(75\beta^2+40\beta+7).
\]

方框是对所有 \(s\) 的严格闭式。它是三个不同指数底
\((1+4\beta),(1+3\beta),(1+2\beta)\) 的离散二阶差，中项带负号；
简单展开任一单项会重新引入负系数。第 5.9 节进一步通过合并递推的
初始三层解决了这个障碍，并完成全 \(s\) 逐系数正证明。

针对这个精确公式做了两级反例审计：

- \(s=5,\ldots,12\) 的整个 \(B_4\) 多项式与独立
  \(t\)-Newton transfer 逐项相同，共 136 个非零正系数；
- 用整数卷积完整展开 \(L_s^{(4)}\) 的每一个系数，对
  \(5\le s\le500\) 未发现负项；每个 \(s\) 的非零支撑恰为
  \(\beta^4,\ldots,\beta^{2s-2}\)。

第二项是针对闭式的有限反例搜索，不是无界 \(s\) 证明。

还有一个不依赖固定页 transfer 的一般组分公式。设一个连通二部树分量
包含核心块集合 \(I\) 和页集合 \(J\)，
\(a=|I|\ge1,b=|J|\ge1,W_I=\sum_{i\in I}w_i\)。加权 Matrix--Tree
公式给出

\[
\tau(I,J)
=
\beta^{a+b-1}b^{a-1}W_I^{b-1}\prod_{i\in I}w_i.
\]

若 \(\Phi(P,Q)\) 是核心块集 \(P\)、页集 \(Q\) 上的全森林多项式，固定
最小页 \(q\in Q\)，按含 \(q\) 的分量分解得到严格递推

\[
\Phi(P,Q)
=
\Phi(P,Q\setminus\{q\})
+\sum_{\substack{\varnothing\ne I\subseteq P\\q\in J\subseteq Q}}
\tau(I,J)\,
\Phi(P\setminus I,Q\setminus J),
\qquad
\Phi(P,\varnothing)=1.
\]

该递推逐项无减法，也给出一般 \(n\) 的 exponential/set-partition
公式。但它不能直接证明所需 determinant：\(H_1^2-H_0H_2\) 把两份
独立组分分解交叉相减，不同 \((I,J)\) 分拆之间没有保持 profile 合并的
逐项序。算法上固定页方法需要 \(B_n\) 个状态，而 Bell 数超指数增长；
组分递推则面对核心和页子集。除非找到按活动页并集 \(n\) 的
sign-reversing involution 或 TP 核，这两个正递推本身都不能消除
\(B_4\) 及一般 \(B_n\) 的符号差。这是本轮明确留下的结构性障碍。

### 5.9 \(B_4\) 统一正性的逐系数递推证明

第四轮首先尝试只证明 \(B_4(\beta)\ge0\)，而不要求逐系数正。把第 5.8
节括号三项记为

\[
A=(1+4\beta)^{2s-10}K_s^{(4)},\quad
B=\lambda^2(1+3\beta)^{2s-8}K_s,\quad
C=\lambda^4(1+2\beta)^{2s-6}.
\]

最自然的平方/AM--GM 充分条件 \(AC\ge B^2\) 是假的：在最小参数
\(s=5\) 时，\(AC-B^2\) 的 \(\beta^4\) 系数精确为 \(-60\)，且该差
在正 \(\beta\) 上确可为负。因此不能用

\[
A+C\ge2\sqrt{AC}\ge2B
\]

完成证明。

虽然该加强路线失败，较弱的目标本身可以通过一个对 \(s\) 的正递推
完成。进一步写

\[
K_s^{(4)}=\sum_{r=0}^8a_r(s)\beta^r,\qquad
K_s=\sum_{r=0}^4c_r(s)\beta^r,\qquad m=2s-10,
\]

并约定越界二项式系数为零，则其 \(\beta^d\) 系数是显式三项和

\[
\begin{aligned}
\ell_{s,d}={}&
\sum_{r=0}^8a_r(s)4^{d-r}\binom m{d-r}\\
&-2\sum_{q=0}^2\binom2q s^q
\sum_{r=0}^4c_r(s)3^{d-q-r}
\binom{m+2}{d-q-r}\\
&+\sum_{q=0}^4\binom4q s^q2^{d-q}
\binom{m+4}{d-q}.
\end{aligned}
\]

所有越界幂--二项式乘积按零处理。符号回归逐项核验了这个公式。它给出

\[
\ell_{s,0}=\cdots=\ell_{s,3}=0,\qquad
\ell_{s,4}
=(s-4)(s^3+6s^2-10s-141)>0.
\]

新的结论是这个更强的系数命题成立：

\[
\ell_{s,d}\ge0
\quad(s\ge5,\ 4\le d\le2s-2).
\]

具体地，令 \(z=1+2\beta\)、\(m=2s-10\)，并定义

\[
\begin{aligned}
D_s&=K^{(4)}_{s+1}-K^{(4)}_s,\\
H_s&=(1+4\beta)^2\lambda_s^2K^{(3)}_s
 -(1+3\beta)^2\lambda_{s+1}^2K^{(3)}_{s+1},\\
E_s&=(1+2\beta)^2\lambda_{s+1}^4
 -(1+4\beta)^2\lambda_s^4.
\end{aligned}
\]

直接相减有

\[
R_s:=L_{s+1}-(1+4\beta)^2L_s
=(1+4\beta)^{m+2}D_s
+2(1+3\beta)^{m+2}H_s+z^{m+4}E_s.
\]

按 \(1+4\beta=z+2\beta\)、\(1+3\beta=z+\beta\) 展开，并把
初始 \(r=0,1,2\) 三层合并，严格得到

\[
R_s=z^mI_s+
\sum_{r=3}^{m+2}\binom{m+2}{r}\beta^rz^{m+2-r}A_{s,r},
\]

其中

\[
A_{s,r}=Q_s+(2^r-1)D_s,\qquad Q_s=D_s+2H_s.
\]

令 \(n=s-5\)。完全展开表明

\[
D_s=\beta^2d_n(\beta),\quad
Q_s=\beta^2q_n(\beta),\quad
I_s=2\beta^4i_n(\beta),
\]

而 \(d_n,q_n,i_n\) 的每个 \(\beta^j n^k\) 系数都是非负整数。
三个多项式的完整七行系数表列在
`B4_UNIFORM_POSITIVITY.md`，并由符号回归逐项核验。因此

\[
R_s\ge_{\mathrm{coeff}}0\qquad(s\ge5).
\]

基例也有显式正分解

\[
L_5=12\beta^4(1+5\beta)^2(7+40\beta+75\beta^2).
\]

由

\[
L_{s+1}=(1+4\beta)^2L_s+R_s
\]

归纳得到 \(L_s\ge_{\mathrm{coeff}}0\) 对全部整数 \(s\ge5\) 成立，
从而 \(B_4\ge0\) 的全 \(s\)、全 \(\beta\ge0\) 证明闭合。完整恒等式、
正系数表、AM--GM no-go 与独立核验单列在
`B4_UNIFORM_POSITIVITY.md`。

### 5.10 五页闭式与 \(B_5\) 统一正性定理

第五轮把固定页状态从 15 个扩展到 Bell 数 \(B_5=52\) 个。相同的
nilpotent 转移严格给出

\[
D_5
=40\beta^4(1+5\beta)^{2s-12}K_s^{(5)},
\]

其中 \(K_s^{(5)}\) 是次数 12 的显式正系数多项式，完整公式列在
`B5_FIVE_PAGE.md`。利用

\[
P_s^{(2)}(5)=10B_2+10B_3+5B_4+B_5
\]

并代入前三个已证闭式，得到对 \(s\ge7\)

\[
B_5=40\beta^4\lambda^{2s-14}F_s,
\]

\[
\begin{aligned}
F_s={}&(1+5\beta)^{2s-12}K_s^{(5)}
-3\lambda^2(1+4\beta)^{2s-10}K_s^{(4)}\\
&+3\lambda^4(1+3\beta)^{2s-8}K_s^{(3)}
-\lambda^6(1+2\beta)^{2s-6}.
\end{aligned}
\]

边界精确约简为

\[
B_5|_{s=5}=12000\beta^{10},
\]

\[
B_5|_{s=6}
=1440\beta^{10}
(54000\beta^4+44352\beta^3+15408\beta^2+2600\beta+181).
\]

五页闭式及边界已经与独立 \(t\)-Newton transfer 在
\(s=5,\ldots,9\) 的 45 个非零系数逐项一致。进一步完整展开
\(6\le s\le200\) 的每个 \(F_s\)，未发现负系数，支撑恰为
\(\beta^6,\ldots,\beta^{2s}\)。

有限审计之后，第六轮完成了无界证明。关键不是直接证明整个候选余项。
写

\[
F_s=G_s+(3C_s-D_s),
\]

其中

\[
G_s=(1+5\beta)^{2s-12}K_s^{(5)}
-3\lambda^2(1+4\beta)^{2s-10}K_s^{(4)}.
\]

第二括号严格分解为

\[
3C_s-D_s
=\lambda^4\left[
2(1+3\beta)^{2s-8}K_s^{(3)}
+\big((1+3\beta)^{2s-8}K_s^{(3)}
-\lambda^2(1+2\beta)^{2s-6}\big)
\right],
\]

最后一项就是已经证明的 \(B_3\) 正括号。因此该部分逐系数非负。

对 \(G_s\)，只需控制次数 \(d\ge14\) 的截断尾部 \(T_s\)。令

\[
\Delta_s=K_{s+1}^{(5)}-K_s^{(5)},\qquad
H_s=(1+5\beta)^2\lambda_s^2K_s^{(4)}
 -(1+4\beta)^2\lambda_{s+1}^2K_{s+1}^{(4)}
\]

以及 \(N=2s-10\)。则

\[
G_{s+1}-(1+5\beta)^2G_s
=(1+4\beta)^{N-1}I_s
+\sum_{r=2}^{N}\binom Nr\beta^r(1+4\beta)^{N-r}\Delta_s,
\]

\[
I_s=(1+4\beta)(\Delta_s+3H_s)+N\beta\Delta_s.
\]

令 \(n=s-8\)。完全展开证明

\[
\Delta_s\ge_{\mathrm{coeff}}0,\qquad
I_s=\beta^2\sum_{j=0}^{11}i_j(n)\beta^j
\ge_{\mathrm{coeff}}0,
\]

其中每个 \(i_j(n)\) 的单项式系数均为非负整数，完整表见
`B5_UNIFORM_POSITIVITY_ATTEMPT.md`。截断只影响递推的
\(\beta^{14},\beta^{15}\) 两个边界系数；它们分别化为
\((n+3)(n+4)\) 与 \((n+2)(n+3)(n+4)\) 乘正系数多项式。正基例是

\[
T_8
=817713831936\beta^{14}
+1067728633856\beta^{15}
+611683139584\beta^{16}.
\]

所以全部 \(d\ge14\) 系数归纳为非负。剩余
\(d=6,\ldots,13\) 由四项二项式精确公式化为 \(s-6\) 的显式
正系数多项式，\(d<6\) 恒为零。由此得到

\[
\boxed{F_s\ge_{\mathrm{coeff}}0\quad\text{对全部整数 }s\ge6,}
\]

从而 \(B_5\) 的全 \(s\) 逐系数非负性已经成为定理。

最初的候选余项仍定义为

\[
R_s^{(5)}=F_{s+1}-(1+5\beta)^2F_s.
\]

但按 \(1+2\beta\) 单层展开会留下精确负单项
\(-576(s-6)^8\beta^{12}\)，相邻层也不能逐项消去。上述分离
\(B_3\) 括号和截断尾部的做法绕开了这个错误的过强中间目标。有限
\(s\le200\) 审计仍只作为回归；无界结论来自符号恒等式和有限正系数表。

### 5.11 六页闭式与 \(B_6\) 统一正性定理

第七轮把固定页状态扩展到 Bell 数 \(B_6=203\)。三个 profile 分别先
抽出

\[
(1+6\beta)^{s-5},\quad
(1+6\beta)^{s-7},\quad
(1+6\beta)^{s-9},
\]

避免直接展开符号指数。剩余普通多项式 determinant 严格给出

\[
D_6=60\beta^4(1+6\beta)^{2s-14}K_s^{(6)},
\]

其中 \(K_s^{(6)}\) 是次数 16 的显式正系数多项式，完整公式见
`B6_SIX_PAGE.md`。二项式反演后，对 \(s\ge8\)

\[
B_6=60\beta^4\lambda^{2s-16}F_s^{(6)},
\]

\[
\begin{aligned}
F_s^{(6)}={}&u_6^{2s-14}K_s^{(6)}
-4\lambda^2u_5^{2s-12}K_s^{(5)}
+6\lambda^4u_4^{2s-10}K_s^{(4)}\\
&-4\lambda^6u_3^{2s-8}K_s^{(3)}
+\lambda^8u_2^{2s-6}.
\end{aligned}
\]

两个边界是

\[
B_6|_{s=6}
=1244160\beta^{12}(60\beta^2+22\beta+3),
\]

\[
\begin{aligned}
B_6|_{s=7}=7200\beta^{12}(&112001848\beta^6
+112001848\beta^5+50848378\beta^4\\
&+13220592\beta^3+2059813\beta^2+181174\beta+7019).
\end{aligned}
\]

\(s=6,\ldots,9\) 的 36 个非零系数已与独立 pooled transfer
逐项一致。完整展开 \(7\le s\le200\) 的 \(F_s^{(6)}\) 和
\(7\le s\le199\) 的候选递推余项均未发现负系数；前者支撑恰为
\(\beta^8,\ldots,\beta^{2s+2}\)。这些仍是有限审计。

复用 \(B_5\) 的剥离思想，写五项为 \(A-4B+6C-4D+E\)。后三项严格
分解为

\[
6C-4D+E=3(C-2D+E)+2(D-E)+3C,
\]

其中前两括号分别是已证 \(B_4,B_3\) 正括号。因此只剩

\[
G_s=A-4B.
\]

其递推 \(G_{s+1}-u_6^2G_s\) 在 \(s\ge15\) 时可通过合并前三层得到
正分解，但 \(G_s\) 的负次数没有固定在 \(d<18\)：精确地，
\(s=100\) 时 \([\beta^{18}]G_s<0\)，\(s=500\) 时
\([\beta^{19}]G_s<0\)。所以 \(B_5\) 使用的固定尾部截断不能直接复制。

第八轮通过把界面改到 \(d=20\) 解决了该障碍。具体地：

- \(d=8,\ldots,19\) 的 \([\beta^d]F_s^{(6)}\) 全部化为
  \(n=s-7\) 的显式正因式；
- 对 \(T_s=\sum_{d\ge20}[\beta^d]G_s\beta^d\)，从 \(s=15\) 起把
  \(G_{s+1}-u_6^2G_s\) 的 \(r=0,1,2\) 三层合并，得到
  \(\beta^2\sum_{j=0}^{16}i_j(s-15)\beta^j\)，每个 \(i_j\) 都是
  正系数多项式；
- 截断仅产生 \(d=20,21\) 两个边界项，两者分别因式分解为正线性因子
  乘次数 14 的正系数多项式；
- \(T_{15}\) 的 13 个系数严格为正，\(s=7,\ldots,14\) 的早期尾部
  由有限精确公式核验。

因此

\[
\boxed{F_s^{(6)}\ge_{\mathrm{coeff}}0\qquad(s\ge7),}
\]

结合 \(s=6\) 边界式，\(B_6\) 的统一逐系数非负性已经闭合。完整低度
因式、三层合并表和截断边界见 `B6_UNIFORM_POSITIVITY.md`。

### 5.12 一般固定页骨架与七页闭式

第九轮首先抽象固定页转移。对 \(k\) 个页和 profile
\((2^h,1^{s-2h})\)，\(h=0,1,2\)，nilpotent 阶数 \(N_k^k=0\)
严格给出

\[
H_h^{(k)}
=(1+k\beta)^{s-2h-k+1}A_h^{(k)}(s,\beta).
\]

因此一般 determinant 的指数模式已经证明：

\[
D_k=2k(k-1)\beta^4
(1+k\beta)^{2s-2k-2}K_k(s,\beta),
\qquad K_k(s,0)=1.
\]

其中 \(\beta^4\) 首项来自两个不同页的有序选择。活动页并集的二项式
反演进一步给出一般 \((k-2)\) 阶交替闭式

\[
B_k=2k(k-1)\beta^4\lambda^{2s-2k-4}F_k,
\]

\[
F_k=
\sum_{j=2}^{k}
(-1)^{k-j}\binom{k-2}{j-2}
\lambda^{2(k-j)}
(1+j\beta)^{2s-2j-2}K_j.
\]

这两个恒等式是一般定理。第十一轮又把
\(\deg_\beta K_k=4(k-2)\) 升级为一般定理；但对一般 \(k\)，
\(K_k\) 的全部中间系数非负、\(F_k\) 从
\(\beta^{2(k-2)}\) 开始且统一非负，目前仍只是由
\(k=2,\ldots,7\) 支持的猜想。下面证明的 \(B_7\) 只关闭 \(k=7\)
实例，不把有限多个实例提升成一般正性结论。

作为 877 状态的下一实例，精确计算得到

\[
D_7=84\beta^4(1+7\beta)^{2s-16}K_s^{(7)},
\]

其中 \(K_s^{(7)}\) 次数 20，全部 \(s,\beta\) 单项式系数非负。对
\(s\ge9\)

\[
\begin{aligned}
B_7=84\beta^4\lambda^{2s-18}\big(&
u_7^{2s-16}K_7
-5\lambda^2u_6^{2s-14}K_6
+10\lambda^4u_5^{2s-12}K_5\\
&-10\lambda^6u_4^{2s-10}K_4
+5\lambda^8u_3^{2s-8}K_3
-\lambda^{10}u_2^{2s-6}\big).
\end{aligned}
\]

\(s=7,8\) 的边界正式列在 `FIXED_PAGE_GENERAL_STRUCTURE.md`。
\(s=7,\ldots,10\) 的 44 个系数与独立 pooled transfer 全同；
原先 \(8\le s\le120\) 的扫描显示支撑从 \(\beta^{10}\) 开始，
并提示了正确阈值。本轮把有限证据升级为无界证明：

\[
10C-10D+5E-F
=6(C-3D+3E-F)+8(D-2E+F)+3(E-F)+4C,
\]

右边前三个括号分别由 \(B_5,B_4,B_3\) 的既有定理控制。令
\(G_s=A-5B\)，则：

- \(F_s\) 的固定次数 \(10\le d\le25\) 化为 \(n=s-8\) 的十六个
  显式非负因式；
- 对 \(T_s=\sum_{d\ge26}[\beta^d]G_s\beta^d\)，从 \(s=26\) 起将
  \(G_{s+1}-u_7^2G_s\) 的前三层合并为
  \(\beta^2\sum_{j=0}^{20}i_j(s-26)\beta^j\)，每个 \(i_j\) 都是
  正系数多项式；
- 截断边界 \(d=26,27\) 均分解为正线性因子乘次数 17 的正系数
  多项式；
- \(T_{26}\) 的 31 个系数严格为正，\(s=8,\ldots,25\) 由有限精确
  二项式公式核验。

因此

\[
\boxed{F_s^{(7)}\ge_{\mathrm{coeff}}0\qquad(s\ge8),}
\]

结合 \(s=7\) 边界式，\(B_7\) 的统一逐系数非负性已经闭合。完整
证明、全部低度因式和尾部证书见 `B7_UNIFORM_POSITIVITY.md`。

### 5.13 一般 \(k\) 的分量正和与端点定理

第十一轮不再扩展到 4140 状态的 \(B_8\)，而是直接处理一般固定页数。
若 \(C_h\) 是含 \(h\) 个权 2 核心块、\(s-2h\) 个权 1 核心块的
集合，\(P\) 是 \(k\) 个页，则固定页森林多项式有逐连通分量正和

\[
H_h^{(k)}
=\sum_{\Pi\in\mathcal P(C_h\sqcup P)}
\prod_{B\in\Pi}\tau(B\cap C_h,B\cap P),
\]

其中含核心集合 \(I\) 和页集合 \(J\) 的非平凡分量权为

\[
\tau(I,J)=
\beta^{|I|+|J|-1}|J|^{|I|-1}
\left(\sum_{i\in I}w_i\right)^{|J|-1}\prod_{i\in I}w_i.
\]

每个森林由其连通分量产生唯一集合分区，因此这是无抵消的逐对象公式。
低次数端暂时忽略成圈约束，边槽生成函数满足

\[
E_1(z)^2=E_0(z)E_2(z),\qquad
E_h(z)=(1+2z)^{kh}(1+z)^{k(s-2h)}.
\]

两侧边槽逐槽保权对应。三条边以内自动无圈，四次唯一坏对象为四圈；
四圈总权的 profile 二阶差为

\[
C_0+C_2-2C_1=2k(k-1).
\]

这把原来的“有序页对计数断言”升级为逐对象缺陷双射证明。

高次数端把恰有 \(c=1,2,3\) 个连通分量的森林按各分量获得的权 2
块、权 1 块和页数写成 multinomial 正和。由此规范化多项式 \(A_h\)
的最高两层在 \(A_1^2-A_0A_2\) 中相消，而下一层严格为

\[
[\beta^{4k-4}](A_1^2-A_0A_2)
=4k^{2k-4}(k-1)s^{2k-4}.
\]

结合低端四圈缺陷，得到一般端点定理

\[
\boxed{
\deg_\beta K_k=4(k-2),\quad
K_k(s,0)=1,\quad
[\beta^{4(k-2)}]K_k=2k^{2k-5}s^{2k-4}.
}
\]

这里 \(A_h\) 的普通多项式推导取稳定范围 \(s\ge k+3\)；负指数的
实际小 \(s\) 边界仍须像 \(B_5,B_6,B_7\) 那样单列。完整证明见
`GENERAL_K_POSITIVITY_ATTACK.md`。它同时记录了全系数证明
尚未闭合的严格障碍：保持 nilpotent 层或终态 profile 的 TP2 minor
在最小实例已有系数 \(-4\)，求和后固定层对仍为
\(-\beta^4(1+\beta)^{s-4}\)。因此成功的交换尾或 Lindström 模型
必须跨层、跨终态汇总，不能逐层构造。

### 5.14 一般 \(K_k\) 的低端项与 \(F_k\) 首次支撑

第十二轮继续把四圈缺陷扩展到五、六边循环子集。记 \(C_h,R_h,S_h\)
为 profile \(h\) 的四、五、六边坏对象总权。五边对象含唯一四圈；
六边对象由“四圈加两边”开始容斥，对每个 \(K_{2,3}\) 或
\(K_{3,2}\) theta 多计两次，并补回不含四圈的无弦六圈。三个核心、
三个页上的无向六圈恰有 6 个。把这些对象逐类求和，再严格反演
\((1+k\beta)^{2s-2k-2}\)，得到一般闭式

\[
\boxed{
\begin{aligned}
[\beta^0]K_k&=1,\\
[\beta^1]K_k&=2(k-2)(k+3),\\
[\beta^2]K_k
&=(k-2)\left((k+3)s+2k^3+7k^2-9k-60\right),\\
[\beta^3]K_k
&=\frac{2(k-2)}3\left(A_ks+(k-3)B_k\right),
\end{aligned}}
\]

其中

\[
A_k=3k^3+11k^2-11k-105,\qquad
B_k=2k^4+13k^3+18k^2-96k-300.
\]

令 \(k=m+3\)，第三式括号变成

\[
ms+6s+2m^3+25m^2+87m+30,
\]

所以前三项对所有 \(k\ge2\) 显式非负。这不是从
\(K_2,\ldots,K_7\) 插值得到的公式；直接六边子集枚举独立核验了
四圈、theta 和六圈容斥。

第四式也一般非负，因为

\[
A_{m+3}=3m^3+38m^2+136m+42,\qquad
B_{m+3}=2m^4+37m^3+243m^2+579m+87.
\]

七边层的 motif 交叠已经包含四圈加三边、theta 加一边、共享单边的
两个四圈和六圈加一边。为避免手工容斥漏项，使用只保留
\(\beta^{\le7}\) 的页分区稀疏转移。七边森林对至多提及七个页标签和
七个核心标签；三步反卷积后，分子关于 \(k,s\) 的次数分别至多
8、7。因此 \(k=0,\ldots,8\)、\(s=4,\ldots,11\) 的
\(9\times8\) 精确网格唯一决定一般二元多项式，使第四式成为严格
有限差分恒等式，而非经验拟合。

另一方面，两个 nilpotent 链分别有 \(j,q\) 个活动页并重叠
\(\ell\) 页时，Newton 汇总阶为 \(r=j+q-\ell\)。每个活动页纯合并
至少贡献两条 spoke，故

\[
d\ge2(j+q)=2(r+\ell)\ge2r.
\]

因此 \(B_r\) 在 \(\beta^{2r}\) 前逐对象为空，而不是靠交替项偶然
消去。结合一般交替闭式中的 \(\beta^4\) 因子：

\[
\boxed{\min\deg_\beta F_k=2(k-2)}
\]

在 \(\mathbb Q[s][\beta]\) 中严格成立。等号层只允许
\(\ell=0\) 且每个页恰合并两个核心分量。若 \(\Phi_h(x)\) 是
profile \(h\) 的加权完全图森林多项式，则全部阶乘精确约去后

\[
[\beta^{2(k-2)}]F_k
=\frac{k!}{2k(k-1)}
[x^k](\Phi_1^2-\Phi_0\Phi_2).
\]

该式是次数 \(2k-4\)、首一的 \(s\)-多项式，因而不恒为零。它对
每个允许边界 \(s\) 的一般正性仍等价于完全图森林 determinant 的
相应系数正性，本轮没有把 \(k\le7\) 的正实例冒充一般证明。完整
推导见 `GENERAL_K_LOW_COEFFICIENTS.md`。

第十三轮进一步识别出 \(\Phi_h\) 的原图含义：若 \(Z\) 是完全图
\(K_s\) 的均匀森林多项式，\(e,f\) 是两条不相邻边，则

\[
x^2(\Phi_1^2-\Phi_0\Phi_2)=Z_eZ_f-ZZ_{ef}.
\]

因此首次 \(F_k\) 系数逐点正性正是完全图森林 Rayleigh difference
的一个固定总边数系数问题，不能借用尚未证明的一般 I-Rayleigh
猜想。以 \(s_0=\max(k,4)\) 展开

\[
[\beta^{2(k-2)}]F_k
=\sum_q a_{k,q}\binom{s-s_0}{q},
\]

加权 Cayley 分量递推对 \(2\le k\le12\) 得到全部
\(a_{k,q}\ge0\)，且最高项为 \((2k-4)!\)。唯一负的形式值是
\(k=s=3\) 时 \(-6\)，但不相邻核心边要求 \(s\ge4\)，故不构成
允许域反例。一般正注入仍未闭合，详细边界见
`GENERAL_F_LEADING_POSITIVITY_AUDIT.md`。

### 5.15 八边层与指定匹配分量 EGF

第十四轮首先把 profile 完全图森林写成指定匹配的双类型分量 EGF。
令 \(U\) 为纯权 1 树分量 EGF，\(A,B\) 分别为含一个、两个指定权 2
收缩块的树分量 EGF；加权 Cayley 公式逐项给出

\[
\Phi_0=s![v^s]e^U,\qquad
\Phi_1=(s-2)![v^{s-2}]e^UA,\qquad
\Phi_2=(s-4)![v^{s-4}]e^U(A^2+B).
\]

这给出任意指定匹配大小 \(h\) 的统一分量递推，并解释最高 Newton
系数：规范化首次系数是首一 \(2k-4\) 次多项式，所以最高
\(\binom{s-s_0}{2k-4}\) 系数必为 \((2k-4)!\)。但三个不同的
\(v\)-抽取阶以及带负号的 \(B\) 项仍阻止把全部中间系数直接写成
正和；一般正性没有被冒称解决。

随后把稀疏页分区转移推进到八边层。八边森林对至多使用八个页标签和
八个核心标签；结合已经证明的 \(n_4,\ldots,n_7\) 次数界，第四步
反卷积后的 \(n_8\) 满足
\(\deg_k n_8\le10,\deg_s n_8\le8\)。因此
\(k=0,\ldots,10,\ s=4,\ldots,12\) 的 \(11\times9\) 精确网格唯一
决定一般恒等式，而不是无界拟合。结果为

\[
\boxed{[\beta^4]K_k=\frac{k-2}{6}P_k(s),}
\]

\[
\begin{aligned}
P_k(s)={}&4k^7+12k^6+12k^5s-73k^5+46k^4s-507k^4\\
&+3k^3s^2-105k^3s+54k^3+12k^2s^2-1036k^2s\\
&+6672k^2-6ks^2-531ks+5868k-135s^2+7110s-37800.
\end{aligned}
\]

令 \(k=m+3,s=k+t\) 后，\(P_k(s)\) 的全部 \(m,t\) 单项式系数为
正，故该系数在 \(k\ge3,s\ge k\) 严格正；\(k=2\) 为零。直接边子集
枚举在 \((2,4),(3,4),(3,5),(4,4)\) 独立重建八次以下森林层，并与
保存的 \(K_3,\ldots,K_7\) 公式交叉核验。

### 5.16 首次 \(F_k\) 系数的 rooted-tree 单和

第十五轮令 \(z=vx\)，用 \(R=ze^R\) 把指定匹配 EGF 化成

\[
U=(R-R^2/2)/x,\qquad A=e^{2R},\qquad
B=4xe^{4R}/(1-R).
\]

Lagrange 反演进一步给出显式有限核

\[
\begin{aligned}
E_{c,d}(s)
&=\sum_{r=0}^d
\frac{(-1)^r\binom{c}{r}s^{d-r}}{2^r(d-r)!},\\
D_{c,d}(s)&=E_{c,d}(s)-E_{c,d-1}(s),
\end{aligned}
\]

以及

\[
\begin{aligned}
[x^j]\Phi_0&=(s)_jD_{s-j,j},\\
[x^j]\Phi_1&=(s-2)_jD_{s-2-j,j},\\
[x^j]\Phi_2
&=(s-4)_jD_{s-4-j,j}
+4(s-4)_{j-1}E_{s-3-j,j-1}.
\end{aligned}
\]

因此 \(C_k=[x^k](\Phi_1^2-\Phi_0\Phi_2)\) 成为一个严格有限
Laguerre 单卷积。这是任意 \(k,s\) 的闭式，不再需要 Bell-state
枚举。

统一在 base-4 Newton 基展开

\[
c_k(s)=\sum_q b_{k,q}\binom{s-4}{q}.
\]

由于 \(\deg\Phi_1\le s-2\)、\(\deg\Phi_0\le s-1\)、
\(\deg\Phi_2\le s-3\)，且总次数 \(2s-4\) 的生成树乘积由
\[
(2s^{s-3})^2=s^{s-2}(4s^{s-4})
\]
严格相消，故 \(C_k(s)=0\) 对 \(k>2s-5\)。这一般性地证明

\[
b_{k,q}=0\qquad
q<\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

用上述 Lagrange 闭式精确审计 \(2\le k\le30\)，所有 base-4
Newton 系数非负，首个非零位置恰为
\(\lfloor(k-2)/2\rfloor\)。后两个观察仍只是有限证据。逐拆分正性
确实失败：\((k,s)=(3,4)\) 的对称卷积项是 \((-16,20)\)；在
\((4,4),(5,5),(6,6)\) 分别为
\((0,-64,64),(0,-1000,1100),(0,-16848,1728,20304)\)。
所以潜在注入必须跨边数拆分汇总，最自然的对象基是“四个标记端点加
\(q\) 个活动普通点”。

### 5.17 base-4 活动森林对与最小交换障碍

第十六轮把 base-4 有限差分直接解释为活动标签容斥。消去正负两侧
共有对象后，正侧是 \(e=01\) 只在红森林、\(f=23\) 在蓝森林；负侧
是 \(e,f\) 都在蓝森林且 \(e\) 不在红森林。除标记边外总计 \(k\)
个边副本，而 \(q\) 个新增普通点必须都在红蓝并中有正度。

最朴素的 fundamental-cycle swap 在最小可能顶点数和总计四个边副本
处已经发生碰撞：

\[
\begin{aligned}
(\{02,12\},\{01,23\})
&\longmapsto(\{01,12\},\{02,23\}),\\
(\{12\},\{01,02,23\})
&\longmapsto(\{01,12\},\{02,23\}).
\end{aligned}
\]

第一行交换基本圈边 \(02\)，第二行直接移动 \(01\)。更强地，固定
未着色并多重图为每条边恰出现一次的简单 \(K_4\) 时，负侧有 4 种
合法着色，正侧只有 2 种。因此任何保持并图的 canonical
alternating-chain 注入都不可能存在；失败不只是 tie-breaking
选择不佳。

在总边副本数 6 的完整 \(K_4\) 审计中，这个 \(-2\) 缺口恰由两个
\(+1\) 并图补平：分别把 cross perfect matching
\(\{02,13\}\)、\(\{03,12\}\) 在红蓝两侧各使用一次。由此建立了一个
四对象局部修复表：每个 matching 的两个负 cross-tree 分别映到同一
简单并图正着色和双重 matching 正着色。该表保持边数和活动顶点，
但外部边可能使新增 matching 边成圈，所以没有冒称为一般注入。

下一条明确的目标是 outside-stable \(K_4\) repair 引理：收缩公共
外部分量后执行上述二选一修复；若形成外部单色圈，则沿 canonical
第一条外边继续，并证明终止和反向唯一恢复。

### 5.18 outside-stable \(K_4\) repair

第十七轮证明上一节的外部稳定性实际上不需要 alternating chain。
饱和负 \(K_4\) 对象的每一种颜色在四个端点上的局部边都是一棵生成
树 \(T\)。令 \(H\) 为同色全部外部边。若 \(T\cup H\) 是森林，则
\(H\) 的每个连通分量至多含一个端点；否则 \(H\) 中的两端点路径与
\(T\) 中路径组成圈。因此把 \(T\) 换成四对象修复表中的任意另一棵
端点树 \(T'\) 后，\(T'\cup H\) 仍是森林。

原计划的链势函数

\[
\mu(H)=\sum_Q\max\{|Q\cap\{0,1,2,3\}|-1,0\}
\]

已被源对象无圈性强制为零，故链在第零步终止。逆映射由目标局部重数
唯一确定：简单 \(K_4\) 目标恢复缺 matching 较小边的源，双重
matching 目标恢复缺较大边的源，全部外部边保持不变。这把裸
\(K_4\) 修复升级成任意外部顶点数的一般局部引理。

\(q=0,1,2,3\) 的独立枚举分别得到 \(1,5,34,299\) 个合法外部森林和
\(1,5,26,141\) 个收缩分量状态，所有替换的非法数均为零。当前真正
剩余的全局障碍是：把所有负对象可逆地分入直接移动、一次基本圈交换、
饱和 \(K_4\) repair 和其他首次冲突类，并保证四类像集互斥。

五顶点全部森林对的固定并图审计进一步定位了下一障碍。要求唯一外点
活动后，共有 42 个负多于正的并图；最小未被饱和 repair 覆盖的状态
在 \(q=1,k=5\)。其简单并图是把 \(K_4\) 的 terminal edge \(13\)
细分成路径 \(1-4-3\)，正侧着色 10 个、负侧 12 个。下一条可执行
引理因此是 series-subdivision \(K_4\) repair：压缩二边路径并保留
可逆 path-color tag，修复后再展开，同时证明与未细分修复像集互斥。

OPG 方向从当前局部引理、首次系数一般正性、完整
\(\alpha^2\) 层到全部边对/C-Gårding 强化的论文依赖图，单列于
`OPG_PUBLICATION_DEPENDENCY_2026-07-30.md`。

### 5.19 五顶点正规形与完整有限注入

第十八轮核清上一节的“42 类”：它们不是都位于 \(k=5\)。在唯一外点
活动时，\(k=5\) 有 12 个亏损并图，\(k=6\) 有 30 个。按独立交换
\(e=01\)、\(f=23\) 两端点的四元对称群取正规形，分别得到 5 和 11
个轨道。

\(k=5\) 的五个轨道具体为两类饱和 \(K_4\) 加悬挂边、一类单边细分
\(K_4\)，以及两类三叉 \(Y\)-replacement。后两类中同一活动点同时
替代两条 incident terminal edges，所以“压缩一条二边路径”的单一
path-color tag 无法覆盖全部 12 类。

尽管一般 tag 尚未闭合，全部 \(q=1,k=5\) 层已经有精确有限注入：

\[
|\mathcal P|=2240,\qquad |\mathcal N|=2140.
\]

以着色边副本的删除数为距离，距离 1 的候选图有 1140 个负对象为
孤点，故一步移动不可能覆盖；允许距离至多 2 后存在覆盖全部 2140
个负对象的确定性匹配，其中 239 对距离 1，1901 对距离 2。保存证书
给出每个排序负对象的唯一正像索引。这个 Hall 匹配会跨正规形重排像，
证明有限层正性但不是一般等变注入。

下一目标相应升级为 rooted terminal-network repair：tag 同时容纳
path 型与两类 \(Y\) 型，并从像的首个 terminal-network block 唯一
恢复，同时避开饱和 \(K_4\) repair 的像。

### 5.20 规则轨道压缩与 same-support tree 障碍

第十九轮把 \(q=1,k=5\) 的有限注入约束为更可解释的两类操作：直接
移动 \(e\)，或红蓝两色各删一条、各加一条的 balanced exchange。
该限制下仍能覆盖全部 2140 个负对象，得到 594 个直接移动和 1546 个
balanced exchange。删/加着色边副本在端点对称群下仅有 22 个规则
轨道，从而把 2140 条对象级匹配压缩成小型规则表。

但把 outside-stability 进一步强制为“每种颜色前后连通分量划分相同”
会失败。这个条件保证改变分量是同一局部支撑上的树替换，因而可直接
使用 terminal-tree replacement 引理；相应候选图却有 150 个孤立
负对象，最大匹配仅 1790。孤点类型为：

\[
146\ \text{个 }Y\text{-replacement},\qquad
4\ \text{个 single-edge subdivision}.
\]

第一个最小失败对象为

\[
R=\{02,03,04,12\},\qquad B=\{01,23,24\}.
\]

其红分量覆盖五点，蓝分量是
\(\{0,1\}\sqcup\{2,3,4\}\)，在“直接移动或同分量树替换”规则下没有
任何正候选。故一般 path/\(Y\) tag 必须显式记录至少一个颜色的局部
分量合并/拆分，不能只依赖同支撑树替换。

### 5.21 首次分量桥修复与新的 Hall 障碍

第二十轮把 150 个 same-support 孤点进一步统一。记
\(A=\{0,1\}\)、\(C=\{2,3,4\}\)。这些对象的蓝森林均为标记边
\(E=01\) 加上 \(C\) 内的一棵树，红森林为五点生成树。红色
\(0\)--\(1\) 路径恰有两条 \(A\)--\(C\) 割边；任选其一 \(x\)，作
\[
(R,B)\mapsto(R-x+E,\;B-E+x).
\]
像中 \(x\) 是唯一蓝色 \(A\)--\(C\) 边，所以该交换可由像唯一
逆转。每个源恰有两个选择，共 300 个互不碰撞的候选像。源对象在
端点对称下有 42 个轨道（41 个 \(Y\)、1 个细分 \(K_4\)），但交换
标签仅有 terminal bridge 与 active-vertex bridge 两类；300 个候选
分别为 200 与 100 个。选择字典序首边得到 150 个互异像。

该 bridge repair 与 \(q=1\) 的 32 个 saturated-repair 像交数为零：
bridge 像恰有一条蓝色 \(A\)--\(C\) 边，而 saturated 像至少有两条
从 \(A\) 出发的 terminal-cross 边。

新的精确障碍在 tree repair 一侧。300 个 bridge 候选像全部属于
same-support tree repair 的 2150 个候选像；把它们加入候选图后，
最大匹配仍为 1790。交替路给出的 Hall 见证为 900 个源只有 550 个
邻像，亏损 350，并包含全部 150 个 bridge 源。因此下一步不能只是
为孤点增加局部规则，而需证明 coupled first-component
alternating-chain routing：把冲突的 tree 源继续路由到 tree 像域
之外的 90 个正对象，同时保留可恢复的首转移标记。

### 5.22 三轨道最小扩域与 350 条可逆交替链

第二十一轮首先核清 90 个 tree 像域外目标并不能单独修复 Hall 亏损。
这 90 个正对象均为 \(Y\)-replacement，形成 27 个端点轨道。全部
balanced exchange 给出 1224 条入边，但把这些边加入后最大匹配仅由
1790 增至 1844，即只实现 54 次新增匹配。

有效扩域只需三类 \(E\leftrightarrow x\) 基本圈换色：
`core-cross`、`E-active`、`F-active`。对应候选边数为
\(1560,830,320\)。加入三类后的候选图有 8844 条边，覆盖全部 2240
个正目标，并存在大小 2140 的满源匹配。任意两类中的最佳组合只能
达到 2108；进一步对基图外全部 21 个 balanced 规则轨道逐一、逐对
穷举，最佳单轨道为 2018，最佳双轨道为 2110。因此三个规则轨道是
达到满匹配的严格最小扩域。

从第 20 轮的 1790 匹配开始，确定性最短交替路算法产生 350 条增广
链，其长度分布为
\[
2^{168},\ 3^{112},\ 4^{47},\ 5^{14},\
6^{6},\ 7^{2},\ 8^{1}.
\]
89 条链终止于 tree 像域外目标，261 条终止于像域内尚未使用的目标。
最终 2140 个像按规则分为 1590 个 base、295 个 core-cross、203 个
E-active、52 个 F-active，四组像两两不交，尚余 100 个正对象。

证书保存全部 350 条有序链。顺序重放得到最终匹配，逆序重放严格恢复
基匹配，因此这不再是无结构的 Hall 存在性证书，而是长度至多 8 的
有限可逆路由。当前剩余缺口是把该路由一般化到任意 \(q,k\)：需要
定义首活动块的下降势，并证明交替链统一终止及标签可恢复。

### 5.23 静态势反例与 \(q=2\) 第四规则

第二十二轮发现，Round21 的确定性最短链冲突图在 \(q=1,k=5\) 已有
源二环 \(1054\to1174\to1054\)。两端具有相同首活动点、相同红蓝
component partition 和相同粗粒度 merge tag，并在两个增广阶段竞争
同一正像 903。因此任何 source-only 静态势都不能沿**当前 Round21
确定性逐冲突路由**严格下降。这不排除改换路由、整链势、非严格势
加 tie-breaker 或全局 Hall 证明；匹配阶段/BFS 层只是候选修复坐标。

对 \(q=2,k=1,\ldots,7\) 的全部森林对进行了精确匹配审计。三类
fundamental swap 的匹配数依次为
\[
2,115,1583,10692,43488,111960,172536,
\]
加入第四类 active-active swap \(E\leftrightarrow45\) 后变为
\[
2,115,1585,10730,43648,112196,172768.
\]
完整 balanced 匹配数为相应负对象数
\[
2,115,1585,10730,43648,112200,172800.
\]

在当前 base 加 fundamental swap 的嵌套规则族中，最小失败是
\(q=2,k=3\)：三规则图存在 \(8>6\) 的 Hall 见证。
八个 Hall 源均有 active-active 逃逸边，第四规则用两条长度 3 的
增广链闭合。首个证书对象为
\[
(R,B)=(\{04,15,45\},\{01,23\})
\mapsto
(\{01,04,15\},\{23,45\}).
\]

第四规则仍不足以覆盖 \(k=6,7\)，亏损分别为 4、32。候选第五规则
active handoff \(24\to25\) 可闭合 \(k=6\)，但在 \(k=7\) 不增加
匹配。因此当前逐冲突方案的一条候选修订是 phase-aware 势：外层
未匹配源数每次增广下降，内层 BFS 距离沿最短交替链下降。这不排除
改换路由、整链势、非严格势加 tie-breaker 或全局 Hall 证明。四规则
图的 \(k=6,7\) 亏损仍需分类；当前 handoff 已闭合 \(k=6\)，但不
改善 \(k=7\)。

### 5.24 \(k=7\) 单签名 completion 与 outside-stability 反例

\(q=2,k=7\) 四规则图的残余 Hall 见证为 \(2272>2240\)，亏损 32。
离开该 Hall 邻域的 full-balanced 边有 20 个签名轨道。加入单个
`core-cross → active-active` 签名 \(02\to45\) 后，最大匹配即从
172768 达到 172800；故相对于四规则基图，新增轨道数的最小值为 1。
该轨道新增 55296 条边并涉及 26496 个正像，32 条最短增广链最长为
10。

该候选并非局部可逆的一般规则：候选目标最大入度为 4，像能识别新增
蓝边 \(45\)，却不能唯一恢复被删的 core-cross 边，仍需 \(x\)-tag
或全局匹配。它也不是 outside-stable。取第 3 个活动点 6 并保持红色
外边 \(06,16\) 不变，证书源红森林
\(\{02,03,04,05,06,16\}\) 无圈，而 \(03\to45\) 后的像红边含三角
圈 \(01,06,16\)。

有限层上两个轨道互补：\(24\to25\) handoff 闭合 \(k=6\) 而不改善
\(k=7\)；\(02\to45\) 闭合 \(k=7\) 而不改善 \(k=6\)。二者联合
闭合当前嵌套规则族的 \(q=2,k\le7\)，但不能据此主张一般
outside-stable repair。

`OUTSIDE_STABILITY_CHARACTERIZATION.md` 给出了这里的一般必要充分
条件：局部森林替换对任意外部森林安全，当且仅当目标在边界上的连通
分区细化源分区；若替换及其局部逆都要求无条件外部稳定，则前后分区
必须相同。上述三角形正是目标合并了源中两个红色边界分量后，由一条
外部二边路径生成的必然见证。

## 6. 独立核验和文件

实现与证书：

- `complete_split_rayleigh.py`：有限 \(s\)、全部 \(r\)、全部边对轨道；
- `complete_split_rayleigh_certificate.json`：\(s=3,\ldots,6\) 全行；
- `complete_split_rayleigh_s7_certificate.json`：\(s=7\) 全行；
- `general_s_disjoint_low_degree.py`：任意 \(s\) 的双 Newton profile 算法；
- `general_s_disjoint_alpha2_beta4_12_certificate.json`：定理 B 全行；
- `general_s_disjoint_extended.py`：高次数二维有限差分和
  \(\alpha^3\) profile 算法；
- `general_s_disjoint_alpha2_beta4_24_alpha3_beta2_24_certificate.json`：
  定理 B/C 扩展全行；
- `tp2_barrier_search.py`：逐 profile、逐 \((j,k)\) 和
  \(t\)-Newton 汇总三级 TP2 审计；
- `tp2_barrier_certificate.json`：障碍反例及 \(s=4,\ldots,12\)
  全 \(\beta\) 多项式证书；
- `fixed_page_union_formula.py`：固定页分区转移、四页闭式和快速
  \(B_4\) 反例扫描；
- `fixed_page_union_certificate.json`：四页三个 profile、determinant、
  \(B_4\) 行和 \(s\le500\) 审计摘要；
- `B4_UNIFORM_POSITIVITY.md`：\(B_4\) 统一正性的逐系数递推证明与
  AM--GM 失败路线；
- `verify_b4_uniform_positivity.py`、`b4_uniform_positivity_audit.json`：
  系数三项和、正递推分解、首项公式和 AM--GM no-go 的符号回归；
- `five_page_union_formula.py`、`five_page_union_certificate.json`：
  52 状态五页行列式、\(B_5\) 闭式和 \(s\le200\) 递推审计；
- `B5_FIVE_PAGE.md`：五页推导、边界值与统一正性证明入口；
- `B5_UNIFORM_POSITIVITY_ATTEMPT.md`：\(B_5\) 的全 \(s\) 尾部正递推
  证明；
- `verify_b5_uniform_positivity.py`、`b5_uniform_positivity_audit.json`：
  四项系数式、低度正多项式与截断尾部符号证书；
- `six_page_union_formula.py`、`six_page_union_certificate.json`：
  203 状态六页 determinant、\(B_6\) 闭式与有限审计；
- `B6_SIX_PAGE.md`：六页推导、边界式及统一证明入口；
- `B6_UNIFORM_POSITIVITY.md`：固定低度与 \(d\ge20\) 尾部递推证明；
- `verify_b6_uniform_positivity.py`、`b6_uniform_positivity_audit.json`：
  五项系数式、三层合并与截断边界符号证书；
- `FIXED_PAGE_GENERAL_STRUCTURE.md`：一般固定页公因子、交替闭式与
  严格区分的猜想；
- `seven_page_union_formula.py`、`seven_page_union_certificate.json`：
  877 状态七页 determinant、\(B_7\) 闭式与有限审计；
- `B7_UNIFORM_POSITIVITY.md`：七页低度因式、正括号剥离与
  \(d\ge26\) 截断尾部递推证明；
- `verify_b7_uniform_positivity.py`、`b7_uniform_positivity_audit.json`：
  六项系数式、三层合并、截断边界和早期基例的独立符号证书；
- `GENERAL_K_POSITIVITY_ATTACK.md`：一般 \(A_h\) 的连通分量正和、
  \(\beta^4\) 四圈缺陷双射、\(K_k\) 精确次数及 TP2 障碍；
- `verify_general_k_extremal_coefficients.py`、`general_k_extremal_audit.json`：
  不依赖 Bell-state 的 1、2、3 分量端点审计；
- `GENERAL_K_LOW_COEFFICIENTS.md`：四至八边坏环/稀疏审计、\(K_k\) 前五项、
  Newton overlap 支撑定理与首次系数提取式；
- `verify_general_k_low_coefficients.py`、`general_k_low_coefficients_audit.json`：
  直接边子集、符号反演、保存核和最小 mask 完全图的四重审计；
- `GENERAL_F_LEADING_POSITIVITY_AUDIT.md`：首次 \(F_k\) 系数的完全图
  Rayleigh 等价、rooted-tree/Lagrange 单和、base-4 Newton 支撑和
  未闭合注入障碍；
- `verify_f_leading_lagrange.py`、`f_leading_lagrange_audit.json`：
  rooted-tree 恒等式、profile 单和、\(k\le30\) base-4 Newton
  证书和逐拆分符号障碍；
- `verify_f_leading_swap_obstruction.py`、
  `f_leading_swap_obstruction_audit.json`：最小基本圈交换碰撞、
  固定并图 \(K_4\) 的 \(4>2\) 障碍及四对象局部修复表；
- `verify_f_leading_k4_outside_stability.py`、
  `f_leading_k4_outside_stability_audit.json`：terminal-tree
  replacement 引理、\(q\le3\) 外部状态枚举和显式逆映射；
- `OPG_PUBLICATION_DEPENDENCY_2026-07-30.md`：从当前引理到首次系数、
  完整 \(\alpha^2\) 层、全部边对和论文层级的依赖图；
- `verify_f_leading_series_subdivision.py`、
  `f_leading_series_subdivision_audit.json`：42 个五顶点亏损并图的
  16 个正规形、\(q=1,k=5\) 的 2140 对有限注入及距离证书；
- `verify_f_leading_first_active_potential.py`、
  `f_leading_first_active_potential_audit.json`：静态势二环、
  \(q=2,k\le7\) 三/四规则最大匹配和最小 \(8>6\) Hall 见证；
- `test_complete_split_rayleigh.py`：独立测试。

最终静态文件 SHA-256：

```text
8f74890a20ea336b527a84655758ef5af31c9464807a5a489ada9e70c134ccd5  complete_split_rayleigh_certificate.json
31869af595b5e87a736339b6d793ee37d9e92264d2b06a86143f1e750154290e  complete_split_rayleigh_s7_certificate.json
3a608684c9d87f926adcffe352eeff329af96e22ed1084eac03d6e701662d63d  general_s_disjoint_alpha2_beta4_12_certificate.json
7f77dd9d911311d47402d67fbb1593a03b1589586f5d11bbcc74d06fd2ad6f59  general_s_disjoint_alpha2_beta4_24_alpha3_beta2_24_certificate.json
38c6b2c9706aa8e5f5a2c43fff35aafa50148de973ff19315748ad531f3ab650  tp2_barrier_certificate.json
71f4804248f92984aa973ee057ef3a6f5683f23b6b9a1d2cb6f2bc7c40b11cc5  fixed_page_union_certificate.json
8f35d42b2592ba4ca0e37beca577a0e4d3e08118a6569398e5b082779f42c589  b4_uniform_positivity_audit.json
4fa6c427e0bee20b0281ace3beeeb2b7f542858e434fd4e7cf5d59f4b1f5c644  five_page_union_certificate.json
ea84ac6f5911a183cb4b8e82f10afd51873ca06769aaca8ecdb233b499833007  b5_uniform_positivity_audit.json
8c879a6918d9b570f84264dcd7a0a88e78a08d62aa989fc51538bacba3071d99  six_page_union_certificate.json
f1cd7be72392ebc57c433f317d8f1924b78353c82173b8cfeae62369b0e96fe7  b6_uniform_positivity_audit.json
f0733c87f65fa08167ffd89771b3b64f03adcd56023f49e4f550408bbfbc9495  seven_page_union_certificate.json
8d5238659d3852bb86b64bf132811e72fbac11757ad19da756a98ec952c7831a  b7_uniform_positivity_audit.json
1daa8d899a69dcb036582fc9b3d41421737fad656ae16378ccd122fac1738e5d  general_k_extremal_audit.json
e5a76dfd0e2632237473fbbd4113c0aff7b39bc01ec193d6bfb90e2cf44a1d86  general_k_low_coefficients_audit.json
454ac9849dd9f35c3d689daa5b106c1fd4ee7159a6f35b9b87948f9e47c95cc6  f_leading_lagrange_audit.json
408d1fb26105b2d76e5524f7a0217dc7d3f344cc0080bcd044dc68a8bab1fa46  f_leading_swap_obstruction_audit.json
cfa2d954930c6e021f7a2bfd27fdd321903d84a8886656887b1b0754e5f67388  f_leading_k4_outside_stability_audit.json
8b38ddab872ec045c1170aa94dc7190c2a97db9a59de29881b441ede5d0a9100  f_leading_series_subdivision_audit.json
28d47f0e106a73b33001be108c3a5b7180b9ec0dc093cd2b8484fef786d67c2e  f_leading_first_active_potential_audit.json
```

测试覆盖：

1. 对 \(S_{3,2}\)、\(\alpha=2,\beta=3\)，独立枚举全部 \(2^9\) 个边子集；
   六个边对轨道的 \(Z,Z_e,Z_f,Z_{ef}\) 与 transfer 逐项完全相同；
2. 每个 JSON 行重构回普通多项式，再转回 Newton 行；
3. 每个轨道和一般 \(s\) 行表的 digest 独立复算；
4. 从 profile transfer 重新推导 \(\beta^4,\beta^5,\beta^6\)，与静态
   \(d\le12\) 证书前缀相同；
5. 上述 \(s=4,5,6\) raw-margin 规范化交叉验证。
6. 新 \(\alpha^2\) 行逐行复现旧 \(d\le12\) 证书；
7. 对 \(s=4,5\)，直接从完整 Bell-state 符号 margin 抽取
   \(\alpha^{2,3}\beta^{4\ldots8}\)，逐项等于新 profile 证书；
8. 独立重新生成 \(\alpha^{2,3}\beta^{4\ldots6}\) 前缀。
9. 逐 \(s=4,\ldots,10\) 核验两个一页 barrier 闭式恒等式；
10. 复算最小逐 profile 反例及其 \(-4\) 系数；
11. 核验 \(s=4,\ldots,12\) 的全部 \(B_n\) 行、digest 和精确三角支撑；
12. 独立重新生成 \(s=4,5,\beta^{0\ldots10}\) 汇总前缀。
13. 独立枚举三页连接块，核验 \(B_3\) determinant 闭式及
    \(m=0,2,\ldots,16\) 的正余项恒等式。
14. 从 15 个页分区状态重新推导四页 determinant；
15. 对 \(s=5,\ldots,9\) 独立比对 \(B_4\) 闭式与汇总 transfer；
16. 审计 \(s\le500\) 的完整 bracket 支撑，并重新计算
    \(s=5,\ldots,30\) 前缀。
17. 独立核验 \(\ell_{s,d}\) 三项和、首个非零系数和
    \(s=5,\beta^4\) 的 \(-60\) AM--GM 反例；
18. 逐项核验
    \(R_s=L_{s+1}-(1+4\beta)^2L_s\) 与正层分解，并核验 \(L_5\)
    的正基例；
19. 核验五页证书摘要、\(B_5\) 两个边界值、\(F_s\) 支撑及候选
    \(s\)-递推余项；
20. 核验 \(B_5\) 四项系数式、低度 \(s-6\) 正多项式、合并首两层
    的 \(I_s\) 表、截断边界与 \(T_8\) 基例；
21. 核验六页证书摘要、\(B_6\) 边界、括号支撑及候选递推余项；
22. 核验 \(B_6\) 低度正因式、三层合并 \(I_s\)、\(d=20,21\)
    截断边界、\(T_{15}\) 与早期尾部基例；
23. 核验七页证书摘要、\(B_7\) 边界、括号支撑与候选递推余项。
24. 核验 \(B_7\) 低度正因式、三层合并 \(I_s\)、\(d=26,27\)
    截断边界、\(T_{26}\)、早期尾部基例与静态 digest。
25. 用 component-set-partition 独立重建一般 \(k\) 的 1、2、3
    分量层，核验四圈缺陷、最高系数、精确次数和静态 digest。
26. 直接枚举至多六边子集并核验 \(K_k\) 前三项，以严格二维次数界
    核验第四、第五项；另直接枚举四个小参数的八边以下森林层，
    复算一般交替式低次消去、完全图提取式及 \(k\le12\) 的允许
    Newton 基。
27. 逐项核验 rooted-tree 三个 EGF 恒等式、Lagrange profile 单和、
    \(k=2,\ldots,7\) 的符号首次系数、\(k=2,\ldots,30\) 的 base-4
    Newton 行和 87 个独立 Cayley-DP 交叉点。
28. 穷举四端点全部森林对，复现最小 fundamental-cycle swap 碰撞、
    固定简单 \(K_4\) 并图的正负着色数 \(2<4\)、两个 \(+1\) 盈余
    并图和四对象局部修复表。
29. 核验 terminal-tree replacement 的 \(q=0,1,2,3\) 收缩状态、
    四类显式逆映射和零非法外部替换；另穷举五顶点森林对，认证
    \(q=1,k=5\) subdivided-\(K_4\) 的 \(10<12\) 最小未覆盖状态。
30. 将 42 个五顶点亏损并图压缩为 16 个端点对称正规形，核验
    \(k=5,6\) 的 \(12+30\) 完整覆盖；复算 \(q=1,k=5\) 的
    2240/2140 对象集、一步孤点和距离至多 2 的 2140 对显式注入。
31. 将 \(q=1,k=5\) 的注入约束为 594 个直接移动和 1546 个每色
    各一次 remove/add 的平衡交换，并压缩成 22 个端点对称规则轨道；
    核验 same-support tree 候选图的 6940 条边、150 个孤立负对象、
    最大匹配 1790，以及首个三臂 \(Y\) 孤立正规形。
32. 对 150 个孤点核验每个恰有两个首次分量桥交换、300 个候选像
    的最大入度为 1、terminal/active bridge 数 \(200+100\)，并验证
    与 32 个 saturated-repair 像零相交；同时认证 300 个 bridge 像
    全落在 2150 个 tree-repair 像域内，以及 \(900>550\) 的 Hall
    亏损见证。
33. 分类 \(900/550\) Hall 见证的 231/139 个端点轨道，验证 90 个
    tree 外目标只能把匹配增至 1844；穷举 21 个额外规则轨道的全部
    单轨道和双轨道扩域，认证三类 fundamental swap 为最小满匹配
    扩域；顺向和逆向重放 350 条长度至多 8 的交替链，并复算最终
    2140 个互异像及两个 SHA-256。
34. 复现 \(q=1,k=5\) 冲突图的源二环；穷举 \(q=2,k=1,\ldots,7\)
    的最多 177984 个正对象和 172800 个负对象，核验三类、加入
    active-active 第四类及完整 balanced 图的逐层最大匹配；认证
    \(q=2,k=3\) 的 \(8>6\) Hall 见证和两条长度 3 增广链，并测试
    active handoff 在 \(k=6\) 闭合、在 \(k=7\) 零增益。
35. 提取 \(q=2,k=7\) 四规则图的 \(2272>2240\) Hall 见证和 20
    个逃逸签名轨道；核验单签名 \(02\to45\) 的 55296 条新增边、
    26496 个目标、32 条长度至多 10 的增广链和 172800 满匹配；
    同时复现目标入度 4 的局部逆障碍及 \(q=3\) 外部扩展产生三角圈
    的 outside-stability 反例。

最终本地测试命令为

```bash
pytest -q data/research_open/q1_eight_hour_campaign_2026-07-29/opg1757/test_complete_split_rayleigh.py
```

第四轮正递推专项测试与最终完整回归均已通过。
加入一般 \(k\) 低端与支撑证书后的完整结果为
`31 passed in 174.50s`。

## 7. 与已有工作的边界

### 7.1 不能再主张为新的操作

独立搜索报告 `agent_search/REPORT.md` 已核清：

- Huang 的任意异质正权约化覆盖桥、度二串联链和平行边；
- Wagner 证明 I-Rayleigh 对 2-sum 闭合，1-sum 直接因解；
- Erickson 已证明全部 series-parallel 图的森林 Rayleigh difference 为
  正单项式乘平方和。

因此叶星、平行二边路径束、series/parallel、1-sum、2-sum 不是本项目的
新全边对闭包。真正尚未被这些定理覆盖的局部操作是假孪生顶点复制；本轮
689,650 个随机多权边对和 15,671,751 个单活动度二次式都没有给出反例，
但也没有证明闭包。

### 7.2 Fang--Ma 2026 的 Gårding 边界

Fang--Ma, *Gårding Polynomials*, arXiv:2604.27755v2，Theorem 12.3
覆盖：

- series-parallel matroid；
- uniform matroid；
- 删除一个基的 uniform matroid及其 2-sum 闭包；
- 至多六个元素的 matroid。

除低参数偶合外，本报告的 \(M(S_{s,r})\) 不落入这些已覆盖类：

- \(S_{s,r}\) 含 \(K_4\) minor，通常不是 series-parallel；
- 它有许多三角 circuit，不是 uniform 或只删一个基的 uniform；
- 对非低参数它是 3-connected graphic matroid，不能作非平凡 2-sum；
- 边数也超过 6。

低参数 \(K_3\)、\(K_4\) 当然分别由 cycle/uniform 或“至多六元素”覆盖。

Fang--Ma 的 Conjecture 14.16 仍把任意图的 unrooted SFGF Rayleigh 列为
猜想，Problem 14.17 询问 graphic matroid 是否 C-Gårding。因此当前完全
分裂图族的完整多变量 C-Gårding 并未被该文献解决。

按 Proposition 13.9 尝试递归判据时，需要对某条边证明

\[
\xi_e(M)=C_{M\setminus e}-C_{M/e}
\ \triangleleft\ C_{M\setminus e}.
\]

删除一条边后完整分裂对称性立即破坏，本轮没有证明这个 domination 条件。
对 \(S_{3,2}\)、\(S_{3,3}\)、\(K_5\) 共 7500 个随机整数仿射线做 MRS
探针没有找到 C-Gårding 反例，但这只是探索性负结果，不能作为
C-Gårding 证据。

### 7.3 专门检索到的邻近计数工作

检索发现完整二部/完整多部/完整分裂图已有多种生成树、含固定森林生成树、
rooted forest polynomial 和森林渐近计数公式，例如：

- Dudley Stark, *The asymptotic number of spanning forests of complete
  bipartite labelled graphs*, Discrete Math. 313 (2013);
- Ewan Kummel, *Forest Generating Functions of Directed Graphs*,
  Portland State University dissertation (2023);
- 完全分裂图和完全多部图中“包含指定森林的生成树”的 Moon-type/
  determinant 公式。

截至本轮定向检索，没有发现与定理 A 相同的“两轨道正权、全部 \(r\)、
全部边对”结论，也没有发现定理 B 的双 Newton 层证书。但这不是正式的
优先权保证；投稿前必须做 MathSciNet/zbMATH/Scopus 级系统复核。

主要原始来源：

- D. G. Wagner, arXiv:math/0602648；
- A. Erickson, arXiv:1008.3660；
- X. Huang, arXiv:2311.00965；
- H. Fang and B. Ma, arXiv:2604.27755v2；
- G. Grimmett and S. Winkler, arXiv:math/0302185。

## 8. 一般 \(s\) 的额外精确公式

若一个连通分量含 \(a\ge1\) 个核心顶点和 \(b\ge0\) 个独立顶点，其加权
生成树枚举为

\[
\tau_{a,b}
=
\beta^b a^{b-1}(\alpha a+\beta b)^{a-1}.
\]

证明可由加权 Laplacian 的三个特征空间直接得到：

- 核心差分特征值 \(\alpha a+\beta b\)，重数 \(a-1\)；
- 独立点差分特征值 \(\beta a\)，重数 \(b-1\)；
- quotient 的非零特征值给出剩余因子。

因而全森林生成函数有精确 EGF

\[
Z_{s,r}
=
s!r![x^sy^r]\,
\exp\left(
y+\sum_{a\ge1,b\ge0}
\tau_{a,b}\frac{x^a}{a!}\frac{y^b}{b!}
\right).
\]

这里单独的 \(y\) 表示孤立独立点分量。该式为一般 \(s\) 的全局证明提供
另一条入口；困难不在 \(Z\) 本身，而在把七种 marked edge-pair 计数的差
写成显然非负形式。

## 9. 论文价值和下一步

当前最诚实的判断是：

- 定理 A、B 和 C 都是可审计的数学进展；
- 它们足以成为后续论文的核心技术 lemma 和计算证书章节；
- 但“\(s\le7\)”加一个低次数层，还不是稳妥的中科院 1 区主定理。

最有希望的三条升级路线按优先级为：

1. **完成 \(\alpha^2\) 全次数。** 令 \(F_k\) 表示把 \(k\) 对核心顶点
   收缩后的带 profile 完全二部森林枚举；当前差正是
   \(F_1^2-F_0F_2\)。寻找 profile 收缩序列的系数对数凹或显式注入，
   可一次覆盖所有 \(d\)。
2. **从 \(\alpha^2\) 归纳到全部 \(\alpha\) 层。** 固定
   \(\alpha^i\) 只涉及有限种含 \(i\) 条核心森林边的 block profile；
   需要证明相应 transfer kernel 的二阶 minor 总非负，而不是逐 \(s\)
   枚举 Bell 状态。
3. **完整多变量 C-Gårding/I-Rayleigh。** 若能验证 Fang--Ma 的递归
   domination 条件，结论将远强于本报告的两轨道正权，也是更符合 1 区
   期望的结果。

若上述路线出现障碍，次优但仍有价值的是对假孪生复制建立完整多变量
transfer 正分解；它是本轮文献核查后唯一未被现有串并联/2-sum 理论覆盖的
自然闭包候选。
