# Erdős #776 / #256：原始 colex 起点的首次 carry 分区与低能量素数分裂的 signed-residue 刚性

日期：2026-07-23（Asia/Hong_Kong）  
统一计费窗口：2026-07-23 06:28:31--08:58:31（9,000 秒）。

> 研究推导已于 2026-07-23 08:41:46 HKT 冻结；此后只作既定回归、排版、
> 清单与哈希校验。所有 finite scan 只作恒等式审计或证伪搜索。

## 0. 原题级结论

本轮目前 **没有闭合 #776 或 #256，也没有改变两题的公开主阶；Q2=false**。

- **#776。** Round11 在 M=75000 否定的是从
  \(C_r={N\choose3}-(N-2)\) 出发的加强候选，而原始 colex 构造从
  \(a_3={N\choose3}-r=C_r+3\) 出发。保留这三个单位后，互补 defect
  与加强候选的差会从 6 严格放大为 \(M+4\)，继而放大到
  \({M-7\choose2}+4M-21\)。这是一个新的全参数增长 slack 接口，说明
  M=75000 反例并未否定原始构造。本轮还用标量轨道 \(x_j\) 将所有
  \(V=M-3\ge7\) 分割成首次 carry 的精确区间，并给出统一 post-carry
  canonical 形式；进一步把整个剩余问题严格压到固定门槛
  \(E_5-F_5\le70500\)，并把大参数段反推成 rank 6 的显式二次下界。
  不过尚未证明该统一门槛，因此尚不能推出
  \(n_0(r)\le2r+5\)。
- **#256。** 把 Round11 的素数范数相容式加强为完整的 signed-residue
  直方图刚性：若奇素数 \(p\) 恰整除 \(m\) 个指数，漏掉 \(s\) 个，且
  \(E(A)<6m\)，则存在 \(t\ge0\) 及一个 signed class \(\{\pm d\}\)，使
  \[
  s-1=t(p-1),\qquad
  \nu_{\{\pm d\}}=2t+1,
  \qquad \nu_{\{\pm a\}}=2t\quad(\{\pm a\}\ne\{\pm d\}).
  \]
  这是全参数条件定理，不是有限观察；其条件也是 two-support 的充分条件，
  并可由 CRT 在任意有限组奇素数上一并实现边缘分布。因此 primitive/marginal
  路线本身已经封口。尚未证明任意指数多重集必出现违反该直方图的高质量
  分裂，所以它没有改善通用 \(f(n)\) 下界。

原题与阶段门槛已在 TARGET_AUDIT.md 固定。下面每一节都明确回译到原题。

## 1. #776：被否定的加强起点不等于原始起点

置

\[
N=r+5,\qquad M=N-2=r+3.
\]

Round7 的显式 colex 区间构造在 \(N\) 点上尝试构造每层
\(2,\ldots,N-3\) 恰有 \(r\) 个成员的反链。其正向容量递推是

\[
a_3={N\choose3}-r,
\qquad a_{p+1}=U_p(a_p)-r.                     \tag{1}
\]

若 (1) 一直非负到 \(p=N-2\)，Round7 的集合级构造便在
\(n=2r+6\) 给出占据全部层 \(2,\ldots,n-2\) 的原题见证；两点悬挂再把
它送到所有 \(n\ge2r+6\)。所以全 \(r\) 证明 (1) 会给

\[
n_0(r)\le2r+5,                                    \tag{2}
\]

并与仓库中已证的 \(n_0(r)\ge2r+5\;(r\ge11)\) 合成该范围内的精确值。

Round11 研究的干净加强起点是

\[
C_r={N-1\choose3}+{N-2\choose2}
   ={N\choose3}-(N-2).
\]

但原始起点严格满足

\[
\boxed{a_3=C_r+3}.                                 \tag{3}
\]

故加强序列在 M=75000 失败，只能说明“把原始三单位安全余量预先删除”的
充分条件失败，不能说明原始 colex 构造失败。

## 2. 原始三单位如何产生增长 slack

沿用 Round11 的基线

\[
A_p={N-1\choose p}+{N-2\choose p-1}.
\]

因 \(a_3=A_3+3\)，其合法 3-canonical 尾项为 \({3\choose1}\)，所以

\[
U_3(a_3)=U_3(A_3)+{3\choose2}=A_4+3.
\]

于是第一次转移后

\[
A_4-a_4=r-3=M-6.                                  \tag{4}
\]

从这里起已进入 Round11 尾补恒等式的合法非负 defect 分支。用互补秩记号
定义原始起点序列 \(E^{[M]}\)：

\[
E^{[M]}_{M-3}=M-6,
\qquad
E^{[M]}_{q-1}=M-3+\operatorname{KK}_q(E^{[M]}_q)
\quad(M-3\ge q\ge4).                              \tag{5}
\]

对照加强起点的序列

\[
D^{[M]}_{M-2}=0,
\qquad
D^{[M]}_{q-1}=M-3+\operatorname{KK}_q(D^{[M]}_q).  \tag{6}
\]

### 定理 1（前三次转移的精确增长余量）

对 \(M\ge14\)，有

\[
\boxed{D_{M-4}-E_{M-4}=6,}                        \tag{7}
\]
\[
\boxed{D_{M-5}-E_{M-5}=M+4,}                      \tag{8}
\]
\[
\boxed{D_{M-6}-E_{M-6}
={M-7\choose2}+4M-21.}                            \tag{9}
\]

更精确地，省略上标 \([M]\)，

\[
D_{M-4}={M-1\choose2}-1,
\qquad E_{M-4}={M-1\choose2}-7,                  \tag{10}
\]

\[
D_{M-5}={M-2\choose3}+{M-4\choose2}+2M-9,
\]
\[
E_{M-5}={M-2\choose3}+{M-4\choose2}+M-13,        \tag{11}
\]

以及

\[
D_{M-6}={M-2\choose4}+{M-4\choose3}+{M-6\choose2}
       +{M-7\choose2}+5M-45,
\]
\[
E_{M-6}={M-2\choose4}+{M-4\choose3}+{M-6\choose2}
       +M-24.                                      \tag{12}
\]

### 证明

\(M-3\) 在 rank \(M-3\) 的 canonical 展开是
\(\sum_{i=1}^{M-3}{i\choose i}\)，而 \(M-6\) 的展开是
\(\sum_{i=4}^{M-3}{i\choose i}\)。逐项降一次下指标并加 \(M-3\)，便得
(10)。把 (10) 各自在 rank \(M-4\) 重新 canonical 展开：加强侧尾部为

\[
{M-4\choose M-5}+{M-6\choose M-6},
\]

原始侧尾部则是从 rank \(M-5\) 到 rank 5 的 \(M-9\) 个对角单位项。
逐项取下影给 (11)。再将 (11) 的线性尾部作同样的贪心 canonical 展开，
得到 (12)。相减即为 (7)--(9)。整个推导只用整数 Pascal 恒等式与
canonical 唯一性。证毕。

这正是本轮要求寻找的“随状态增长的 slack”：它不是把已被否定的固定 28
猜想重新命名。困难在于 \(\operatorname{KK}\) 有长平台，(9) 的二次差值
未必单调保存到 rank 3；本轮尚缺一个能穿越全部 carry 的势函数。

## 3. 原始端点的精确标量接口

Round11 最后两步的尾补消元对 (5) 同样适用，给出

\[
\boxed{
a_{N-2}\ge0
\iff
E^{[M]}_3\le{M-1\choose3}+28.}                   \tag{13}
\]

程序从原始正向递推 (1) 与反向递推 (5) 两端独立计算，在
\(9\le M\le180\) 的 172 个整数点逐点核对 (13)。该范围内
\(E_3-{M-1\choose3}\) 的最大观察值为 4；这只是回归审计，绝不外推为
无限量词证明。

另以 Round11 同一整数 lazy-carry 引擎、但改用原始 seed \(M-6\)，在
加强候选的已知反例点得到

\[
M=75000,\qquad
E^{[75000]}_3={74999\choose3}+5
={74999\choose3}+{3\choose2}+{2\choose1}.         \tag{13a}
\]

同一点加强序列的 excess 为 29，故原始三单位在完整 carry 后仍留下 24
个 defect 差、并以 5 而非 29 抵达 rank 3；相对允许值 28 尚余 23。
计算用单 core 5、nice 10，耗时约 1,193 秒。式 (13a) 是精确有限定点，
只证明 M=75000 没有否定原始构造；它不能证明更大 M 也安全。

### Round11 (10f) 的局部展示公式勘误

独立重算发现 Round11 REPORT.md 在证明 (10f) 的 seed 段写了

\[
D^{[M]}_{M-4}={M-1\choose2},
\qquad D^{[M+1]}_{M-3}={M\choose2}.
\]

两式都应各减 1：

\[
\boxed{
D^{[M]}_{M-4}={M-1\choose2}-1,
\qquad D^{[M+1]}_{M-3}={M\choose2}-1.}            \tag{14}
\]

例如 \(M=30\) 时第一式为 405 而非 406；其 rank-26 canonical 展开是

\[
{28\choose26}+{26\choose25}+{24\choose24},
\]

上升量为 29，所以悬挂后为 434，恰等于
\({30\choose2}-1\)。因此两侧遗漏的是同一个 -1，seed 的悬挂等式仍
成立，Round11 (10f) 的后续传播证明、M=75000 的精确 defect 值、固定
28 候选反例及原题仍开放的结论均不受影响。这里将它定级为**展示公式局部
算术错误**，不是对 Round11 主结论的推翻；冻结档案不回改。

### 二次增长 slack 的等价正向递推

式 (13) 还可改写成一个不以固定 28 为状态量的正向不变量。令

\[
S_2={M-2\choose2}+4,\qquad
S_{j+1}=U_j(S_j)-(M-3)\quad(2\le j\le M-6).       \tag{14a}
\]

只要中间量非负，严格有

\[
S_j={M-1\choose q}-E_q,\qquad q=M-1-j.             \tag{14b}
\]

证明是对尾补恒等式

\[
{M-1\choose q-1}
-\operatorname{KK}_q\!\left({M-1\choose q}-S_j\right)
=U_{M-1-q}(S_j)
\]

逐层应用。初值来自
\[
{M-1\choose M-3}-(M-6)={M-2\choose2}+4.
\]

在末端 \(q=4,j=M-5\)，(13) 等价于

\[
U_{M-5}(S_{M-5})\ge M-31.
\]

再用 Galois 等价以及 \(M-31\) 在 rank \(M-4\) 的对角单位展开，
对 \(M\ge32\) 得到

\[
\boxed{
S_{M-5}\ge
\operatorname{KK}_{M-4}(M-31)
={M-3\choose2}-{28\choose2}
={M-3\choose2}-378.}                              \tag{14c}
\]

所以原始构造真正要保存的是一个主项约为 \(M^2/2\) 的**二次 slack**，
而不是假设某个固定 canonical 前缀永不变化。有限审计在
\(9\le M\le180\) 同时核对 (5)、(13)、(14a)--(14c)，但尚未证明
(14a) 对所有 \(M\) 在每一步非负并最终满足 (14c)。一个可行的 all-\(M\)
carry 势必须直接给这个二次下界。

### 首次 carry 前的精确正规形

二次 slack 还允许把“多出的三个单位”如何放大写成一个与 \(M\) 分离的
标量轨道。置 \(V=M-3\)，并定义

\[
x_3=5,\qquad x_{j+1}={x_j\choose2}-2j+3.          \tag{14d}
\]

只要对 \(3\le i\le j\) 都有

\[
0<x_i<V-2i+5,                                    \tag{14e}
\]

则 \(S_j\) 有如下**精确**的合法 \(j\)-canonical 展开：

\[
\boxed{
S_j={V\choose j}
 +\sum_{k=3}^{j-1}{V-2j+2k\choose k}
 +{V-2j+5\choose2}+{x_j\choose1}.}              \tag{14f}
\]

这里空和按零计。初始式确为

\[
S_3={V\choose3}+{V-1\choose2}+{5\choose1}.
\]

若 (14f) 在 rank \(j\) 成立，逐项上升后，只有末端
\({V-2j+5\choose3}\) 需要用两次 Pascal 恒等式拆成

\[
{V-2j+4\choose3}+{V-2j+3\choose2}+(V-2j+3).
\]

再减去 \(V\)，余下的 rank-1 数恰是
\({x_j\choose2}-2j+3=x_{j+1}\)，从而归纳得到 (14f)。条件
(14e) 正好保证最后一个上指标严格小于前一项的 \(V-2i+5\)，所以没有
暗中越过 canonical carry。

前几项为

\[
x_3,x_4,x_5,x_6,x_7,x_8
=5,7,16,113,6319,19961710.                         \tag{14g}
\]

因此首次非平凡 carry 的位置由显式阈值
\(x_j\ge V-2j+5\) 决定，而不是由一个猜测的固定长度前缀决定。例如
\(V=74997\) 时 (14f) 严格合法到 \(j=7\)，下一步产生约两千万的
rank-1 原始余量并触发重新展开。这提供了一个可行的分段证明路线：在相邻
阈值区间先用 (14f) 精确入射，再对 carry 后的新低秩尾部建立统一势。
本轮尚未完成后半段；尤其 (14g) 的快速增长本身不能代替穿越其余约 \(M\)
层的证明。

事实上 (14d)--(14f) 不只描述某个有限前缀，而是**分类所有参数的首次
carry**。对每个 \(j\ge4\) 定义整数区间

\[
I_j=\left[x_{j-1}+2j-6, x_j+2j-5\right].        \tag{14g1}
\]

这些区间首尾相接：\(I_{j+1}\) 的左端恰为 \(I_j\) 右端加一；由 (14d)
及初值直接归纳 \(x_j\) 严格增长并趋于无穷，故 \(I_j\;(j\ge4)\) 分割
全部 \(V\ge7\)。若 \(V\in I_j\)，则对每个 \(i<j\) 都有 (14e)，而
在 \(i=j\) 首次有 \(x_j\ge V-2j+5\)。所以首次 carry **恰在 rank
\(j\)**，不存在有限扫描留下的参数缝隙。

更强的是，首次 carry 后仍有统一闭式。令

\[
y_j=x_j-(V-2j+5)\ge0.
\]

从 rank \(j-1\) 的合法 (14f) 上升所得的形式恒等式中，把最后三部分用
Pascal 合并：

\[
{V-2j+6\choose3}+{V-2j+5\choose2}+x_j
={V-2j+7\choose3}+y_j.                           \tag{14g2}
\]

在 \(I_j\) 左端，

\[
{V-2j+7\choose2}-y_j=2x_{j-1}+2j-6>0,
\]

而该差随 \(V\) 严格增加。因此 \(y_j\) 的 2-canonical 顶项总是严格
低于 \(V-2j+7\)，并得到整个区间上的合法展开

\[
\boxed{
S_j={V\choose j}
 +\sum_{k=4}^{j-1}{V-2j+2k\choose k}
 +{V-2j+7\choose3}
 +\operatorname{Can}_2(y_j),\qquad V\in I_j.}    \tag{14g3}
\]

所以本轮已经把第一 block 的所有 parameter/carry 分支完全压平；未解决的是
第二及以后 block 的统一势，而不是首次 carry 位置本身。

该分区还严格给出首次 carry 的尺度。由 \(x_5=16\) 起可归纳
\(x_j\ge4j-4\)，并直接从 (14d) 得

\[
\frac{x_j^2}{4}\le x_{j+1}<\frac{x_j^2}{2}\qquad(j\ge5).
\]

因此 \(\log x_j\) 每步约翻倍；若 \(V\in I_j\)，首次 carry rank 满足

\[
j=\log_2\log V+O(1).                             \tag{14g3a}
\]

而 (14g3) 在完全不读取 residual digits 的情况下就给出统一下界

\[
\boxed{S_j-{V\choose j}\ge{V-2j+7\choose3}
       =\left(\frac16+o(1)\right)V^3.}           \tag{14g3b}
\]

因此首次 carry 并没有吃掉原始三单位产生的增长余量：在首个碰撞点仍留下
一个渐近立方的 canonical reservoir。这是 carry 位置无关的严格下界；
困难只在后续约 \(V\) 层可能反复借穿该 reservoir，所以 (14g3b) 仍不能
单独推出末端的二次目标 (14c)。

这里不能用“立方总量大于约 \(V^2\) 的累计扣除”作线性记账：Macaulay
上升依赖当前 rank 与 capped canonical 前缀。即使 \(U_k\) 由不交底集构造
可知是超可加的，把 \({V-2j+7\choose3}\) 从高位前缀中拆成一个独立的
rank-\(j\) 数再应用 \(U_j\)，会重新 canonicalize 并丢掉原来受前缀保护的
大 top；所得无条件界只维持很短的低秩 block。式 (14l)--(14n) 保留 cap
条件，正是为了避免这个错误的“总量守恒”捷径。

这与加强起点中观察到的 \(\log V\) 级前缀是不同机制，也说明为何保留三个
单位会大幅改变 carry 尺度；但“首次更早/更晚”本身仍不决定末端正负。

在任意 \(I_j\) 内，下一层能否继续只从 residual 支付 \(V\) 也由一个标量
断点决定：

\[
U_2(y_j)\ge V
\iff V+\operatorname{KK}_3(V)\le x_j+2j-5.       \tag{14g4}
\]

左侧的 \(V+\operatorname{KK}_3(V)\) 严格递增，故若断点落在 \(I_j\)
内便唯一。下面把包含已计算大参数点的 \(j=8\) 分支完全写开。因为
\(x_7=6319\)、\(x_8=19961710\)，此时

\[
6329\le V\le19961721                              \tag{14h}
\]

时，(14f) 恰好合法到 rank 7，并在 rank 8 首次违反末尾的严格上指标条件。
令

\[
y=19961710-(V-11).
\]

把 rank 8 的最后两项与原始尾量合并，Pascal 恒等式给

\[
{V-10\choose3}+{V-11\choose2}+19961710
={V-9\choose3}+y.                                \tag{14i}
\]

在 (14h) 上有 \(0\le y<{V-9\choose2}\)：右侧差值在左端 \(V=6329\)
已经为 12648，随后严格递增。因此 \(y\) 的 2-canonical 展开的所有上指标
都小于 \(V-9\)，第一次 carry 后的完整合法展开是

\[
\boxed{
S_8={V\choose8}
 +\sum_{k=4}^{7}{V-16+2k\choose k}
 +{V-9\choose3}
 +\operatorname{Can}_2(y).}                     \tag{14j}
\]

这里 \(\operatorname{Can}_2(y)\) 表示其二项式项之和，而非新增数值算子。
式 (14j) 覆盖 \(M=75000\) 以及正在作独立定点复核的更大参数；它把“首次
carry 会怎样”从观察提升为区间恒等式。

下一层是否仍能把减去的 \(V\) 完全放在这个 residual 中，也有一个精确参数
断点。由 Galois 伴随，

\[
U_2(y)\ge V
\iff y\ge\operatorname{KK}_3(V)
\iff V+\operatorname{KK}_3(V)\le19961721.
\]

函数 \(V+\operatorname{KK}_3(V)\) 严格递增，而

\[
V_*:=19840461
 ={492\choose3}+{473\choose2}+{453\choose1},
\quad
\operatorname{KK}_3(V_*)=121260,
\quad V_*+121260=19961721.                       \tag{14j1}
\]

对 \(V_*+1\)，同一 canonical 前两项不变而 rank-1 项加一，所以右端已
严格超过 19961721。故 \(V_*\) 是唯一的精确断点。置

\[
P_9={V\choose9}+\sum_{k=5}^{8}{V-18+2k\choose k}.
\]

于是整个 (14h) 区间在 rank 9 有如下无遗漏的两段正规形：

\[
\boxed{
6329\le V\le V_*:\quad
S_9=P_9+{V-9\choose4}
 +\operatorname{Can}_3\!\left(U_2(y)-V\right),} \tag{14j2}
\]

以及令 \(z=V-U_2(y)>0\)，

\[
\boxed{
V_*<V\le19961721:\quad
S_9=P_9+{V-10\choose4}+{V-11\choose3}
 +\operatorname{Can}_2\!\left({V-11\choose2}-z\right).} \tag{14j3}
\]

第一段中 \(U_2(y)-V<{V-9\choose3}\)，所以 residual 顶项低于
\(V-9\)；第二段用两次 Pascal 展开
\({V-9\choose4}-z\)，且
\(0<z\le V<{V-11\choose2}\)，故同样是合法 canonical 拼接。
这把“下一个参数阈值”定位到精确整数，而非有限扫描猜测。

统一公式也立即越过任何可行的逐点扫描尺度。下一段 \(j=9\) 是

\[
I_9=[19961722,199234923081195],
\]

而 (14g4) 的唯一断点为

\[
V_9^*=199229291300636
 ={106130\choose3}+{45173\choose2}+{43498\choose1},
\]

其 3-shadow 为 5631780559，且两数之和恰为 \(I_9\) 的右端；加一后
严格失败。这些巨大整数由 (14d)、canonical 展开和 Galois 等价逐式给出，
不是用有限点支持渐近外推。

在 (14j2) 的高位前缀保持分离的阶段，可以继续追踪低秩 residual

\[
R_2=y,\qquad R_{\ell+1}=U_\ell(R_\ell)-V,         \tag{14k}
\]

并在它借穿下一项时迭代同类 Pascal 合并。这个 block-carry 递归是比逐层
固定前缀更具体的证明路径，但本轮尚未得到覆盖所有 block 的单调势。

为避免 (14k) 隐含任何未说明的“前缀稳定”假设，可把合法条件写成一个通用
分块引理。若某层有合法分解

\[
S_j=\sum_{i=\ell+1}^{j}{a_i\choose i}+R_\ell,
\]

其中 \(R_\ell\) 的 \(\ell\)-canonical 顶项严格小于 \(a_{\ell+1}\)，且
\(R'_{\ell+1}=U_\ell(R_\ell)-V\ge0\) 的顶项仍严格小于
\(a_{\ell+1}\)，则逐项上升立即给

\[
S_{j+1}=\sum_{i=\ell+1}^{j}{a_i\choose i+1}+R'_{\ell+1}. \tag{14l}
\]

也就是说，只有 residual 变负或其顶项撞上相邻高位时才需要重新做 carry；
两次事件之间的整块历史由 (14k) 精确承担。这一引理本身是 canonical 定义的
直接推论，尚缺的是对历次碰撞后的统一终止/余量估计。

同一 block 还可用 Galois 伴随一次性从另一端会合，而不逐层猜 canonical
digits。固定希望 residual 穿过的最后 rank \(L\ge2\)，反向定义

\[
B_{L+1}^{(L)}=0,
\qquad
B_k^{(L)}=\operatorname{KK}_{k+1}
 \left(V+B_{k+1}^{(L)}\right)\quad(k=L,L-1,\ldots,2). \tag{14m}
\]

逐层使用 \(U_k(x)\ge w\iff x\ge\operatorname{KK}_{k+1}(w)\)，严格得到

\[
\boxed{R_2=y\text{ 能非负走到 }R_{L+1}
\iff y\ge B_2^{(L)}.}                            \tag{14n}
\]

而 \(B_2^{(L)}(V)\) 随 \(V\) 单调，所以在 (14h) 内每个固定 block 长度
都有唯一参数断点
\(V+B_2^{(L)}(V)\le19961721\)。式 (14j1) 是 \(L=2\) 的情形。
再走一层时 \(L=3\)，条件变成

\[
V+\operatorname{KK}_3\!\left(V+\operatorname{KK}_4(V)\right)
\le19961721.                                      \tag{14o}
\]

其精确末点为

\[
V_{**}=19838163
 ={149\choose4}+{90\choose3}+{37\choose2}+{16\choose1}.
\]

这里 \(\operatorname{KK}_4(V_{**})=544317\)，而

\[
V_{**}+544317
 ={497\choose3}+{301\choose2}+{90\choose1},
\]

其 3-shadow 为 123558，恰满足 \(V_{**}+123558=19961721\)；加一后
严格失败。这个反向 block requirement 是目前最接近 carry-independent 势的
接口：它把任意给定 block 压成一个标量门槛，但尚未证明所有 successive
blocks 的门槛在最终 rank 前统一保持，也就仍不能推出 (14c)。

### 把全部剩余 carry 压到 rank 5 的固定常数门槛

还有一个比“逐层保持基线”更直接的末端接口。仍令 \(V=M-3\)，并写

\[
B_q={V+1\choose q}+{V\choose q-1},
\qquad
F_q={V+1\choose q}+{V-1\choose q-1}+{V-2\choose q-2}.
\tag{14p}
\]

三项上指标严格递减，所以这是合法 canonical 展开；两次 Pascal 恒等式又
给出

\[
F_q=B_q-{V-2\choose q-3},
\qquad
\operatorname{KK}_q(F_q)=F_{q-1}.               \tag{14q}
\]

因此 \(F_q\) 是自然的“无税调和屏障”。但它**不是**原 defect 递推的不变
屏障：原递推每层还要加 \(V\)，所以只从 \(E_q\le F_q\) 得到
\(E_{q-1}\le F_{q-1}+V\)。这恰好定位了不能把有限观察
\(S_j\ge{V\choose j}\) 误写成归纳证明的符号缺口。

在 rank 5 定义唯一剩余标量

\[
h(V):=E_5-F_5.                                   \tag{14r}
\]

则对每个 \(V\ge379\)，原始端点条件 (13) 有如下**严格等价归约**：

\[
\boxed{
E_3\le {V+2\choose3}+28
\iff h(V)\le {376\choose2}=70500.}              \tag{14s}
\]

下面逐一核对所有 carry 分支。首先若 \(h\le0\)，由
\(\operatorname{KK}\) 的单调性及 (14q)，

\[
E_4\le V+F_4=B_4+2.
\]

\(B_4+2\) 的合法展开是在
\({V+1\choose4}+{V\choose3}\) 后拼接 2 的 2-canonical 展开，故

\[
E_3\le V+\operatorname{KK}_4(B_4+2)
={V+2\choose3}+\operatorname{KK}_2(2)
={V+2\choose3}+3,
\]

这一分支严格安全。

其次设

\[
0\le h<{V-2\choose2}.                            \tag{14t}
\]

此时 \(h\) 的 2-canonical 顶项严格小于 \(V-2\)，故可以合法拼在
\(F_5\) 的末项 \({V-2\choose3}\) 后。逐项取下影并用

\[
B_4-F_4=V-2
\]

得到精确式

\[
E_4=B_4+d,
\qquad d:=2+\operatorname{KK}_2(h).              \tag{14u}
\]

由 (14t) 有 \(d\le V<{V\choose2}\)，所以 \(d\) 的 2-canonical 顶项
也严格小于 \(V\)，可合法拼在 \(B_4\) 的末项 \({V\choose3}\) 后。再
降一次便有

\[
\boxed{E_3={V+2\choose3}+\operatorname{KK}_2(d).} \tag{14v}
\]

对任意整数 \(w\ge0,t\ge1\)，rank-2 greedy 展开的断点直接给

\[
\operatorname{KK}_2(w)\le t
\iff w\le {t\choose2}.                          \tag{14w}
\]

所以 (14v) 的 excess 不超过 28，严格等价于

\[
d\le{28\choose2}=378
\iff \operatorname{KK}_2(h)\le376
\iff h\le{376\choose2}=70500.                   \tag{14x}
\]

等号也没有遗漏：\(h={376\choose2}\) 时依次得到 \(d=378\) 和最终
excess 28；\(h={376\choose2}+1\) 时依次跳到 379 和 29。因
\({V-2\choose2}\ge{377\choose2}>70501\) 对 \(V\ge379\) 成立，阈值
及其紧邻失败点都确实位于 (14t) 的合法拼接区间。

最后若 \(h\ge{V-2\choose2}\)，则由 (14q)

\[
E_5\ge B_5,
\qquad E_4\ge V+B_4.
\]

因 \(V<{V\choose2}\)，右端仍是把 \(V\) 的 2-canonical 展开合法拼在
\(B_4\) 后；于是单调性给出

\[
E_3-{V+2\choose3}\ge\operatorname{KK}_2(V).
\]

而 \(V\ge379>{28\choose2}\)，由 (14w) 右端至少为 29，故这一整支
严格失败。三支覆盖全部整数 \(h\)，证得 (14s)。

式 (14s) 是本轮得到的最短剩余证明目标：不再需要证明猜测性的全层
\(S_j\ge{V\choose j}\)，只需证明单个统一常数界
\(E_5-F_5\le70500\)。有限精确值例如 \(V=30,50,75,100,150,300\)
时 \(h=-3,-1,2,3,4,4\)；且 (13a) 通过 (14u)--(14v) 反推
\(V=74997\) 时 \(h\le28\)。这些都只是有限证据，尚没有覆盖任意大
\(V\) 的论证；因此 (14s) 是严格 reduction，而不是 #776 的闭合证明。

还可把这个固定门槛精确反推一层，以暴露最小的增长引理。令

\[
g(V):=F_6-E_6.
\]

当 \(0\le g\le{V-2\choose4}\) 时，对 \(F_6\) 的末项
\({V-2\choose4}\) 使用尾补恒等式，严格得到

\[
h(V)=V-U_{V-6}(g).                               \tag{14y}
\]

若 \(g<0\)，则单调性给 \(h\ge V>70500\)，自动失败；若
\(g>{V-2\choose4}\)，则已经借穿整个末项，单调性给
\(h\le V-{V-2\choose3}<70500\)，自动成功（容量等号仍由 (14y)
覆盖）。因此对 \(V\ge70501\)，(14s) 又严格等价于

\[
\boxed{
F_6-E_6\ge
\operatorname{KK}_{V-5}(V-70500)
={V-4\choose2}-{70496\choose2}.}                \tag{14z}
\]

最后一个等号不是渐近估计：\(V-70500\) 在 rank \(V-5\) 的 canonical
展开恰是从 lower rank 70496 到 \(V-5\) 的对角单位项，逐项下降影后求和
即得该二次差。于是大参数部分的未决核心已收缩成 (14z) 这一条显式二次
下界；它仍需要控制此前所有 carry，本轮没有证明。对
\(379\le V\le70500\) 则仍使用 (14s)；若能统一证明 \(F_6-E_6\ge0\)，
这一有限参数带会自动满足 \(h\le V\le70500\)，但该非负性目前也只有有限
精确观察而没有全区间证明。
\(V=70500\) 不被 (14z) 声称覆盖：此时 \(V-70500=0\)，而下影平台
可能使 \(g<0\) 分支在等号附近失去反向严格性；该边界仍由 (14s) 完整
承担。作为索引检查，\(V=70501\) 时 (14z) 的目标为
\(\operatorname{KK}_{70496}(1)=70496\)，恰等于右侧两个二项式之差。

## 4. #256：从范数相容到 signed-residue 完整直方图

令

\[
P_A(z)=\prod_{i=1}^n(1-z^{a_i})=\sum_k c_kz^k,
\qquad E(A)=\sum_kc_k^2.
\]

固定素数 \(p\)，假设恰有 \(m\) 个指数被 \(p\) 整除，另有
\(s=n-m\) 个指数 \(b_1,\ldots,b_s\) 不被 \(p\) 整除，且
\(0<m<n\)。Round9 的整数根重数引理与 Round10 的非平凡分裂至少两
fibres 定理给

\[
E(A)\ge2mS_p(Q_p),\qquad S_p(Q_p)\ge2,             \tag{15}
\]

其中 \(P_A=(1-z^p)^mQ_p\)。若 \(E(A)<6m\)，则整数
\(S_p(Q_p)\) 被迫等于 2。投影到 \(\mathbb Z[C_p]\) 并除去被
\(p\) 整除部分贡献的非零整数常数，得到

\[
H(x):=\prod_{j=1}^s(1-x^{b_j})
=\alpha(x^u-x^v)\quad\text{于 }\mathbb Z[C_p],    \tag{16}
\]

其中 \(\alpha\ne0\)、\(d=u-v\not\equiv0\pmod p\)。Round11 取
圆分域范数已证明

\[
s-1=t(p-1),\qquad |\alpha|=p^t,\qquad t\in\mathbb Z_{\ge0}. \tag{17}
\]

### 定理 2（奇素数低能量分裂的 signed-residue 刚性）

设 \(p\) 为奇素数且上述 \(E(A)<6m\) 成立。对
\(G=(\mathbb Z/p\mathbb Z)^\times/\{\pm1\}\) 中的 signed class
\(C=\{\pm a\}\)，令

\[
\nu_C=\#\{j:b_j\bmod p\in C\}.
\]

则以 \(D=\{\pm d\}\) 记 (16) 两个位置之差的 signed class，有

\[
\boxed{\nu_D=2t+1,
\qquad \nu_C=2t\quad(C\ne D).}                   \tag{18}
\]

### 证明

取 \(\zeta=e^{2\pi i/p}\)，并令

\[
\lambda(C)=\log|1-\zeta^a|\quad(C=\{\pm a\}).
\]

绝对值使定义与符号代表元无关。把 (16) 代入所有 Galois 嵌入
\(\zeta\mapsto\zeta^k\)，并使用 (17)，对每个 \(k\in G\) 得

\[
\sum_{C\in G}\nu_C\lambda(kC)
=t\log p+\lambda(kD).                              \tag{18b}
\]

置 \(h_C=\nu_C-\mathbf1_{C=D}\)。式 (18b) 说乘法群 \(G\) 上的卷积
\(h*\lambda\) 是常函数。现在对 \(G\) 作 Fourier 变换。其字符正好是
模 \(p\) 的**偶 Dirichlet 字符** \(\chi(-1)=1\)。对每个非主偶字符，
经典 log-sine 公式把

\[
\widehat\lambda(\chi)
=\sum_{C\in G}\lambda(C)\overline{\chi(C)}
\]

写成一个非零 Gauss 因子乘 \(L(1,\overline\chi)\)；Dirichlet 的
\(L(1,\chi)\ne0\) 定理保证它不为零。因此 (18b) 的每个非平凡 Fourier
模都给 \(\widehat h(\chi)=0\)。奇字符不下降到商群 \(G\)，也不会出现；
这正是结论只能分类 signed residues 而不能区分 \(+a\) 与 \(-a\) 的原因。

所以 \(h\) 在 \(G\) 上为常数。由

\[
\sum_C h_C=s-1=t(p-1),\qquad |G|=(p-1)/2,
\]

该常数必为 \(2t\)，即得 (18)。证毕。

p=2 时商群只有一个类，Fourier 论证没有非平凡模，(18) 不提供额外
信息；这不是遗漏的小例外。t=0 时 \(s=1\)，(18) 退化为唯一 signed
class 出现一次，也正确。

事实上上述 signed 直方图也**充分**刻画奇素数循环群环中的二项式支撑。
若某个非零 residue 多重集满足 (18)，则每个 signed class 的 \(2t\)
个基本拷贝可两两换向；恒等式

\[
\prod_{a=1}^{p-1}(1-\zeta^a)=p,\qquad
1-\zeta^{-a}=-\zeta^{-a}(1-\zeta^a)
\]

说明所有基本拷贝之积等于 \(p^t\) 乘一个根单位，额外的 \(D\) 类因子
再给 \(1-\zeta^d\)。所以

\[
H(\zeta)=\pm\zeta^u p^t(1-\zeta^d).
\]

两侧在 \(x=1\) 都为零，而差在 \(\zeta\) 处为零；互素的首一多项式
\(x-1\) 与 \(\Phi_p(x)\) 之积为 \(x^p-1\)，故 Gauss 引理给

\[
H(x)=\pm p^t x^u(1-x^d)\quad\text{于 }\mathbb Z[C_p].
\]

结合前向 Fourier 论证得到精确的 iff 分类：

\[
\boxed{
\prod_j(1-x^{b_j})\text{ 在 }\mathbb Z[C_p]\text{ 恰有两个非零位置}
\iff \text{(18) 对某个 signed class }D\text{ 成立}.}       \tag{18a}
\]

因此 (18) 不是仅从范数抽出的弱同余；在 primitive \(p\) 层面，它已经
穷尽所有 two-support residue 模式。仍未被分类的是这些模式如何与被
\(p\) 整除部分的每条 ideal-PTE coefficient fibre 同时实现。
它也给出一个严格 no-go：只研究 primitive 群环投影不可能再排除相容分支，
因为对每个奇素数 \(p\) 和每个 \(t\ge0\)，按 (18) 直接放置 residues
就真实产生 two-support。例如

\[
p=5,\quad (b_j\bmod5)=(1,1,1,2,2)
\quad\Longrightarrow\quad
H(x)=5x^3(1-x)\ \text{于 }\mathbb Z[C_5].
\]

所以下一步必须保留完整 polynomial fibres、合数模联合信息或 Archimedean
范数，不能只继续加强同一个圆分范数等式。

### 多素数边缘直方图的 CRT no-go

甚至把有限多个素数的 (18) **只按一维边缘计数相交**也不会自动产生矛盾。
设 \(\mathcal P\) 是任意有限个奇素数，取 \(n>\max\mathcal P\)。对每个
\(p\in\mathcal P\)，先独立安排一列长为 \(n\) 的模 \(p\) residues：放
\(n-p\) 个 0；在非零部分选一个 distinguished signed class 放 3 个，
其余每个 signed class 各放 2 个。非零项总数恰为

\[
3+2\frac{p-3}{2}=p=1+(p-1),
\]

故它正是 \(t=1\) 的 (18)。把各素数的这些列任意标号后，逐坐标用中国
剩余定理选出正整数 \(a_i\)。于是同一个指数多重集对每个
\(p\in\mathcal P\) 都恰有 \(m_p=n-p>0\) 个可除指数，且外部边缘直方图
完全相容；由 (18a)，每个 primitive \(p\) 投影都真实 two-support。

这个构造没有声称所得多重集低能量；它严格说明的是：**任意有限组 (18) 的
边缘条件本身可同时实现**。所以“把多个 signed histograms 并列后由 CRT
计数矛盾收费”的朴素路线已经封死。合数模路线若要前进，必须保留同一批
指数在多个模上的联合 cell、完整 polynomial coefficient fibres，或另加
能量小这一解析条件；不能只使用各素数的 marginal counts。

### 退化相容分支的精确递归

分类还把 \(t=0\) 分支完全剥离出来。由 (17)，\(t=0\) 当且仅当
\(s=1\)。此时把唯一不被 \(p\) 整除的指数记为 \(b\)，其余指数写为
\(pc_1,\ldots,pc_m\)，并置

\[
B(y)=\prod_{i=1}^m(1-y^{c_i}).
\]

则有

\[
P_A(z)=B(z^p)(1-z^b).
\]

两项 \(B(z^p)\) 与 \(z^bB(z^p)\) 的系数支撑分别落在模 \(p\) 的
0 与 \(b\) 两个不同 residue fibres，绝无抵消，故得到精确递归

\[
\boxed{E(pc_1,\ldots,pc_m,b)=2E(c_1,\ldots,c_m).} \tag{19}
\]

所以低能量相容方向出现一个严格三分支：直方图失衡立即由 (20) 收费；
平衡且 \(t\ge1\) 时必有 \(s=1+t(p-1)\ge p\)，外部指数占据每个 signed
class；而 \(t=0\) 时问题精确降一维且能量翻倍。若某个指数多重集沿嵌套的
“除掉唯一例外、其余同除以一个素数”链走了 \(k\) 次，(19) 给出因子
\(2^k\)，即若末端多重集为 \(A^{(k)}\)，则

\[
\boxed{E(A)=2^kE(A^{(k)})\ge2^k.}                \tag{19a}
\]

另一个立即可用的“近共同素因子”判据是：若 \(p\) 恰漏掉 \(s\) 个指数且
\(1<s<p\)，(18) 不可能成立，故必有 \(E(A)\ge6(n-s)\)；只有 \(s=1\)
会进入 (19) 的剥离分支。当前缺口是证明任意近极值多重集必有足够长的此类
链，或在链中断时必出现一个 \(m\) 足够大的失衡方向；没有这种全称组合
引理，(19)--(19a) 仍只是严格的分支约化，而非 #256 的新通用下界。

### 原题回译与仍缺的全称桥

定理 2 的逆否命题是一个严格收费器：若某个奇素数分裂的外部 signed
residue 直方图不是“一类 \(2t+1\)，其余所有类恰 \(2t\)”的完全平衡形状，
则

\[
E(A)\ge6m,\qquad \|P_A\|_\infty\ge\sqrt{12m}.      \tag{20}
\]

特别是 \(s>1\) 时必须 \(p\le s\)，并且每个非零 signed class 都出现。
这比只记录 \(p-1\mid s-1\) 严格得多。

但 (20) 仍未成为通用 \(f(n)\) 下界：当前没有证明任意近极值多重集都存在
一个 \(m\) 足够大且直方图失衡的素数方向。若所有高质量方向均呈 (18)，
还需在合数模中保留超出一维边缘的联合 cells/完整 fibres，或从另一范数
中收费。故本轮不把条件定理冒充为 \(f(n)\) 的主指数改进。

## 5. 精确计算与有限边界

exact_original_targets.py 是纯整数回归脚本：

- 从原始正向 (1) 与互补递推 (5) 独立核对端点等价 (13)；
- 对每个 \(14\le M\le180\) 核对 (7)--(12)；
- 在 \(h=70500/70501\)、三个 cap 分支及 rank-6 反推门槛两侧作 50 个
  选定整数边界回归；纸面 (14s)、(14z) 承担无限量词；
- 枚举允许重复的 \(3\le n\le7,1\le a_i\le9\)，在 29,866 个非平凡
  素数分裂中找到 89 个 \(E<6m\) 分裂，其中 25 个属于奇素数；(18) 零
  反例。
- 另对 \(p=3,5,7\)、外部 residue 多重集大小 \(1\) 到 \(8\) 穷举
  3,540 个群环乘积；其中 162 个恰有 two-support，与 (18a) 预测的
  162 个逐一相同。
- 首次 carry 分区核对 18 个端点/中点，rank-8 区间核对 5 点，rank-9
  两段核对 7 点；rank-5 常数门槛三分支核对 36 点，rank-6 反推门槛
  核对 14 点，均为零失配。
- \(t=0,s=1\) 的精确能量递归在完整小盒中触发并核对 1,585 次。

这些数字只说明程序与纸面公式相容。定理 1、2 的无限量词分别由 canonical
展开和 Fourier/Dirichlet 论证承担；有限范围不能证明 #776 的 (13) 对所有
\(M\) 的右侧不等式都成立（等价式 (13) 本身已由纸面消元证明），也不能
保证 #256 的任意元组出现收费分裂。

冻结回归命令为

    taskset -c 5 nice -n 10 python3 exact_original_targets.py --max-m 180 --max-exponent 9

于 08:41:57 HKT 左右开始，约 5.1 秒后以退出码 0 返回 “status=PASS”。
另一个单核、nice 10 的 \(M=150000\) lazy-carry spot 尝试运行约
81 分钟后，在 08:41:46 HKT 按冻结要求以 KeyboardInterrupt 终止；
它没有输出完整整数，故**不进入任何有限证据或数学结论**。已完成且可复核
的大参数定点仍只有 (13a) 的 \(M=75000\)。

## 6. 下一断点

1. **#776：** 最短目标是证明 \(V\ge379\) 时
   \(E_5-F_5\le70500\)。对 \(V\ge70501\)，这严格等价于 (14z) 的
   rank-6 二次下界；对 \(379\le V\le70500\)，证明
   \(F_6-E_6\ge0\) 已足够。若这些势不存在，应优先找原始起点反例，而
   不是再证明被否定的加强起点。
2. **#256：** 对两个或更多奇素数同时满足 (18) 的外部指数研究 CRT **联合
   cells 与完整 coefficient fibres**；边缘直方图本身已由上面的 CRT 构造
   证明不会矛盾。若交集分裂仍有 \(m_{pq}>E/6\)，在合数圆分域中重复
   two-fibre 分类。必须最终覆盖任意元组，才可回译为 \(f(n)\) 的新界。

## 7. 来源

- https://www.erdosproblems.com/776
- https://arxiv.org/abs/2602.09803v2
- https://www.erdosproblems.com/256
- Quanyu Tang, DOI 10.1090/proc/17668
- Round7 colex 构造、Round9 整数根重数引理、Round10 two-fibre 引理及
  Round11 圆分范数相容式，均在本仓库对应冻结报告中逐式给出。
