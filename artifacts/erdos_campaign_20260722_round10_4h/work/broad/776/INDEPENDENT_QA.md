# Erdős #776 第十轮 midpoint/Galois 敌对复核

复核结论：`PASS_WITH_SCOPE_CORRECTION`。

核心 Galois 等价、递推索引及“在任一共同层比较即可认证全部容量”的方向均
正确。需要修正的是证据措辞：有限计算只证明前缀长度曾从 3 增到 4，不能
证明共同前缀无界，也不能把展示出的交错前缀当作全称不变量。

## 1. Macaulay/Galois 方向

采用脚本的定义：若

\[
 x=\sum_i{\alpha_i\choose i},
\]

是 `p`-canonical 展开，则

\[
 U_p(x)=\sum_i{\alpha_i\choose i+1},\qquad
 KK_p(x)=\sum_i{\alpha_i\choose i-1}.
\]

正确的伴随方向确为

\[
 U_p(x)\ge y\quad\Longleftrightarrow\quad
 x\ge KK_{p+1}(y).
\]

它等价于：下影至多含 `x` 个 `p`-集的 colex 尾/初段，最多容纳
`U_p(x)` 个 `(p+1)`-集。小盒穷举 `p=1,...,6`、`x,y=0,...,29` 全部通过；
不等号没有反向，也不需要把 `>=` 改成 `>`。

代入递推逐项为

\[
\begin{aligned}
a_{p+1}\ge b_{p+1}
&\iff U_p(a_p)-r\ge b_{p+1}\\
&\iff U_p(a_p)\ge b_{p+1}+r\\
&\iff a_p\ge KK_{p+1}(b_{p+1}+r)=b_p.
\end{aligned}
\]

所以相邻层等价、进而任一已定义的共同层比较等价于端点比较。这部分严格。

## 2. 递推索引

置 `N=r+5`：

- 正向从 `a_3=C(N,3)-r` 开始；Python 的
  `for rank in range(3,middle)` 最后生成的正是 `a_middle`。
- 反向从 `b_(N-2)=0` 开始；
  `range(N-3,middle-1,-1)` 首先生成 `b_(N-3)`，最后生成
  `b_middle`，没有 off-by-one。
- `3<=p<N-2` 是相邻等价式的正确范围；末端比较为
  `a_(N-2)>=b_(N-2)=0`。

若担心正向量在会合层以后变成负数：一旦会合处有
`a_p>=b_p>=0`，伴随等价会归纳推出 `a_(p+1)>=b_(p+1)>=0`，所以证书
本身同时保证后续递推有定义。脚本到中层前另显式拒绝负数。

## 3. “任一中层即可认证”的精确含义

正确表述是：任选同一个 `p`，从底端算出 `a_p`、从顶端算出 `b_p`；只要
精确整数比较 `a_p>=b_p` 成立，即可认证所有层容量。midpoint 只是把两侧
递推长度平衡，并非伴随定理唯一允许的层。

若改用 canonical 首差作为比较证书，还需保留三个分支：

1. 两侧首个不同 digit 的 lower rank 相同，此时较大的 upper top 确实给出
   较大的整数（hockey-stick 上界控制余尾）；
2. 一侧 canonical 列表是另一侧的真前缀；
3. 首个未配对 digit 的 lower rank 不同。

当前有限脚本只在两侧首差都存在时断言 lower rank 相同及 `a` 的 upper top
更大；受检 `r<=300` 的确都落在这个分支。下一条全称“首差定向”引理若想
单独承担证明，必须把后两个分支排除或纳入陈述。直接比较整数
`a_p>=b_p` 则没有这个措辞风险。

## 4. 第二实现与有限输出

- 将第十轮 canonical/KK 实现与第七轮 `colex_construct_verify.py` 独立实现
  对照，在 ranks `1..9`、`0<=x<1000` 上 canonical digit 与 lower shadow
  完全一致。
- 对 `4<=r<=20`，midpoint 比较与第七轮逐集合物化后的最终 pair capacity
  同时通过。
- 默认脚本重跑仍给 `2<=r<=300` 全 PASS、最小正 gap 14、前缀长度直方图
  `0:2, 1:5, 2:41, 3:251`。
- 额外短时单点检查得到：`r=301,500` 的共同前缀仍为 3；`r=1000` 首次
  看到长度 4，且首差为 `(996,498)` 对 `(626,498)`，整数 gap 为正。

这些结果支持“固定只验前三项不够”，但仍只是有限事实。

## 5. 必须降级的措辞

`ATTEMPT.md` 中“共同 canonical 前缀的长度随 r 增长”若理解为实验趋势可以
保留；“共同前缀无界增长”目前没有证明，必须改成：

> 受检范围已出现长度 4，因此不能假定共同前缀永久由前三项界定；是否随
> `r` 无界增长仍是待证现象。

同理，形式前缀

\[
 {N-1\choose p}+{N-3\choose p-1}+{N-5\choose p-2}+\cdots
\]

及其几何密度 `2/3` 目前只能作为观察到的候选不变量，不能在没有全称 carry
证明时承担结论。

## 6. 最终边界

- Galois 伴随方向：`PASS`。
- 双向递推索引：`PASS`。
- 任一共同层的精确整数比较可认证全部容量：`PASS`。
- finite midpoint rows 与第二实现：`PASS`。
- “共同前缀无界”：`NOT PROVED / TEXTUAL SCOPE CORRECTION REQUIRED`。
- #776 原题闭合：`FALSE`；Q2 停止结果：`FALSE`。
