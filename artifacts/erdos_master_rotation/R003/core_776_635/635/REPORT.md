# Erdős #635：R003 固定 valuation 短双圈核与长度无关不变量

研究窗口：2026-07-23 21:03:58--21:47:02 HKT
本题实际 active agent time：1,072 秒（0.2978 agent-hours）
预算上限：14,400 秒；只登记实耗，不登记预算余额。

## 结论

**原题的精确极值部分仍为 OPEN。本轮没有证明或证否 #635。**

本轮在 R002 的固定 \(A=2\) 长度 14 排除之外得到两类严格进展：

1. 完整枚举多个新的固定 valuation 域，共检查
   `734,320,442` 个满足 \(\prod h_i<A^m\) 的奇乘子元组：

   \[
   \begin{array}{c|c}
   A&\text{完整排除的 non-backtracking 圈长度}\\ \hline
   4&2\le m\le9\\
   8&2\le m\le6\\
   16&2\le m\le4\\
   32&2\le m\le3\\
   64&2\le m\le3.
   \end{array}
   \]

   因任意 `theta`、`figure-eight` 或 `dumbbell` 核都含一个长度不超过
   总边数的 non-backtracking 圈，这也完整排除了相应总边数范围内的
   固定 \(A\) 双圈核。
2. 对任意长度的固定 \(A\) 圈证明两个必要不变量：

   \[
   \sum_i p_i=\sum_iq_i,
   \tag{1}
   \]
   \[
   \prod_i\left(1-\frac1{Ap_i}\right)
   =\frac{\prod_i h_i}{A^m}
   =\prod_i\left(1-\frac1{Aq_i}\right).
   \tag{2}
   \]

   严格凹性进一步说明：若两个降序素数多重集在 majorization 次序中可比，
   则 (1)--(2) 强迫它们相同；因此不同多重集的真候选必须出现前缀和
   交叉。

但不变量本身不能闭合：`A=4, h=(1,3,21)` 给出一个整数、无立即回退的
复合闭游走，其两侧分别为

\[
(p_i)=(23,91,121),\qquad(q_i)=(163,41,31).
\]

它同时满足 (1)--(2)。所以继续路线必须实质使用素性或多圈共享路径，而
不能只靠 Euler product、总和或凹性。

**闭合距离仍为 2。** 任意长度/任意 \(A\) 的固定层双圈核以及混合
valuation 核都未被排除或构造；即使完成 semiprime proper-neighbour
Hall，原题还需 prime-square、高阶奇部和邻点合并。

## 1. 问题状态与攻击对象

公开页面的第二个渐近子问

\[
|A|\le(1/2+o_t(1))N
\]

已有肯定答案；官方讨论明确说明，开头精确的 “How large can \(|A|\)
be?” 仍未解决。特别是 \(t=2\) 时，奇数加稀疏的 2 的幂给出
\(N/2+c\log N\) 型现象，当前不知道正确次项。

在 semiprime swap graph 中，固定

\[
x=Apq,\qquad A=2^a,\quad p<q\text{ 为不同奇素数},
\]

一条左边对应两个 proper odd neighbours

\[
q(Ap-1),\qquad p(Aq-1).
\]

固定 \(A\) 时所有不同左标号由 R002 的 valuation 引理自动互不冲突；
所以若出现双圈核，它会直接否定这一 proper-neighbour Hall 子路线。
最小双圈核删叶、压缩度二路径后是 `theta`、`figure-eight` 或
`dumbbell`。

## 2. 固定 \(A\) 乘子枚举为何完整

沿固定 \(A\) 的一个定向闭游走，可选正奇数乘子 \(h_i\) 使

\[
h_ip_i=Ap_{i-1}-1,\qquad
Aq_i=h_iq_{i-1}+1
\tag{3}
\]

（指标循环）。正性给

\[
\prod_{i=1}^m h_i<A^m.
\tag{4}
\]

反过来，固定 \((A,m,h_1,\ldots,h_m)\) 后，两个循环种子被唯一强迫：
其共同分母为

\[
A^m-\prod_i h_i,
\]

分子分别是正向、反向前缀乘积的显式整数和。程序随后逐步验证整除性、
回到种子、所有 \(p_i,q_i\) 的素性、边非退化以及是否立即回退。

由于 (4) 使正奇数组合有限，枚举没有 prime cutoff，也没有隐含的
顶点/标签上界。循环旋转可能被重复计数，但这只增加工作量，不会漏掉圈。

## 3. 完整有限结果

新枚举的汇总如下。`prime` 列包括立即回退；最后一列才是图中可能形成
真圈的闭游走。

| \(A\) | \(m\) 范围 | 乘子元组总数 | prime closed walks | non-backtracking |
|---:|---:|---:|---:|---:|
| 4 | 2--9 | 651,162,191 | 17 | 0 |
| 8 | 2--6 | 76,696,357 | 12 | 0 |
| 16 | 2--4 | 2,308,277 | 11 | 0 |
| 32 | 2--3 | 354,378 | 7 | 0 |
| 64 | 2--3 | 3,799,239 | 6 | 0 |
| **合计** |  | **734,320,442** | **53** | **0** |

从零 non-backtracking 结果严格推出：

\[
\boxed{
\begin{array}{ll}
A=4:&\text{无总边数 }\le9\text{ 的固定层双圈核};\\
A=8:&\text{无总边数 }\le6\text{ 的固定层双圈核};\\
A=16:&\text{无总边数 }\le4\text{ 的固定层双圈核};\\
A=32,64:&\text{无总边数 }\le3\text{ 的固定层双圈核}.
\end{array}}
\tag{5}
\]

继承 R002 的独立证书还给 \(A=2\) 无长度 \(\le14\) 圈，故无总边数
\(\le14\) 的固定 \(A=2\) 双圈核。

## 4. 两个长度无关不变量

### 定理 1

任意满足 (3) 的固定 \(A\) 闭游走都满足 (1)--(2)。

### 证明

由 (3) 的第一个递推，

\[
\frac{h_i}{A}
=\frac{p_{i-1}}{p_i}
\Bigl(1-\frac1{Ap_{i-1}}\Bigr).
\tag{6}
\]

循环相乘，\(p_{i-1}/p_i\) 消去，得到 (2) 的左等号。第二个递推同理给

\[
\frac{h_i}{A}
=\frac{q_i}{q_{i-1}}
\Bigl(1-\frac1{Aq_i}\Bigr),
\tag{7}
\]

从而得到右等号。

再置 \(x_i=Ap_iq_i\)。由 (3)

\[
x_i-p_i=p_i(Aq_i-1)
=q_{i-1}(Ap_{i-1}-1)=x_{i-1}-q_{i-1}.
\]

故 \(x_i-x_{i-1}=p_i-q_{i-1}\)。绕圈求和即得
\(\sum p_i=\sum q_i\)，证明 (1)。同时

\[
d_i=\frac{p_i-q_{i-1}}A\in\mathbb Z,\qquad\sum_i d_i=0,
\tag{8}
\]

其中整除性由 (3) 模 \(A\) 立即得到。证毕。

## 5. 严格凹性与 majorization crossing

令

\[
\phi_A(x)=\log\left(1-\frac1{Ax}\right).
\]

对 \(A\ge2,x>0\)，有

\[
\phi_A''(x)<0.
\]

若降序多重集 \(P=(p_i)\) majorize \(Q=(q_i)\)，Karamata 不等式与
(1)--(2) 给

\[
\sum_i\phi_A(p_i)\le\sum_i\phi_A(q_i),
\]

而两侧由 (2) 相等。严格凹性迫使两个多重集相同。交换 \(P,Q\) 同理。
所以若 \(P,Q\) 不同，二者必须在 majorization 偏序中不可比；其降序前缀
和差必须出现正负交叉。

这是一个长度无关的路径过滤器，但不是完整单调量。下面的复合例子正好有
前缀差 \((-42,8)\)，因此逃过 majorization。

## 6. 两个严格 no-go 证书

### 不变量不足以强迫回退

取

\[
A=4,\quad(h_1,h_2,h_3)=(1,3,21).
\]

式 (3) 给闭游走

\[
P=(23,91,121),\qquad Q=(163,41,31),
\]

其边没有相邻重复，并且

\[
\sum P=\sum Q=235,\qquad
\prod\left(1-\frac1{4p_i}\right)
=\prod\left(1-\frac1{4q_i}\right)=\frac{63}{64}.
\]

但 \(91,121\) 为合数。它证明“只用 (1)--(2) 排除所有闭游走”的路线
不成立；素性不是可最后附加的小条件。

### Euler product 单独甚至不含一阶矩

\[
P=(3,11,43),\qquad Q=(5,5,19)
\]

满足相同 Euler product \(57/64\)，但

\[
\sum P=57\ne29=\sum Q.
\]

同一 \(P\) 与反序 \(Q=(43,11,3)\) 则来自
\(h=(1,1,57)\) 的全素数闭游走，但有立即回退。两例共同说明：
Euler product、总和与 prime multiset 的排列结构都必须同时保留。

## 7. 未闭合节点与下一步

本轮没有：

- 排除任意长度或任意 \(A\) 的固定层双圈核；
- 排除混合 valuation 的三类核；
- 证明 semiprime proper-neighbour Hall；
- 处理 prime-square、高阶奇部或确定原题次项。

首个可判定动作是把 (1)--(2) 应用于两圈共享路径：对 theta 的三条路径
分别相除 Euler product，并用 (8) 比较共享端点增量；目标是证明至少两个
循环的 majorization 方向相容，从而触发第 5 节，或构造一个真正的全素数
crossing core。继续单独增加某个 \(A,m\) 的 cutoff 只会扩大 (5)，不会
解决无限量词。

## 8. 复核

```bash
python3 verify_cycle_invariants.py

taskset -c 6 nice -n 10 \
  python3 run_fixed_A_cycle_audit.py
```

第一项应立即输出 `"status": "PASS"`。完整枚举在本机约 76 秒；它编译
`enumerate_fixed_A_cycles.cpp` 后逐域核对冻结计数与零
non-backtracking 断言。
