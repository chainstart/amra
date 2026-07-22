# Erdős #679 第九轮：固定二次对数窗口与条件化 stopping-line 接口

日期：2026-07-22（Asia/Hong_Kong）

状态：**原题仍开放；未得到区间传递；未达到 SCI 二区主结果门槛。**

## 1. 目标与结论边界

第八轮把负向路线压缩为 CRT 权重

\[
 W(n)=\prod_{H<p\le z}\{1-aX_p(n)\}
\]

的单边区间估计。这里 \(X_p\) 表示 \(n\) 落入模 \(p\) 的 \(H\) 个禁余数之一。
完整周期零频已足够小，但仍缺

\[
 \sum_{n\in I}W(n)\le N\mu X^{o(1)},\qquad N\asymp X. \tag{1}
\]

本轮没有证明 (1)。新进展有两项：

1. 参数可简化到固定 \(H=(\log X)^2\)，同时完整周期好类密度变为超多项式小，
   相对非零 Fourier 能量趋于零；
2. stopping-line 高导子尾可严格化为条件后缀问题，全部 crossing 前沿的绝对
   代价仅为 \(X^{o(1)}\)。

第二项说明剩余障碍是任意仿射变换后缀在较短区间上的统一相对上界，而不是前沿
子集数本身。

## 2. 最强严格参数定理

记 \(L_1=\log X,L_2=\log_2X,L_3=\log_3X\)，取

\[
 H=\lfloor(\log X)^2\rfloor,\quad z=\exp(L_1/L_2),
\quad L=\sum_{H<p\le z}p^{-1},
\]
\[
 a={CL_1\over HL},\quad t=1-a,\quad C>1.               \tag{2}
\]

Mertens 公式及阈值核对给出

\[
 L=L_2-2L_3-\log2+o(1),\qquad HaL=CL_1,
\]
\[
 R\log(1/t)\le(2C+o_\varepsilon(1)){L_1\over L_3}
              =o(L_1).                                \tag{3}
\]

所有选取素数都大于 \(H\)，所以连续 \(H\) 个平移在每个局部模数上无碰撞。
完整 CRT 周期好类比例因而满足

\[
 \delta\le X^{-C+o(1)}.                                \tag{4}
\]

精确局部二阶矩进一步给出

\[
 \log{M_2\over\mu^2}=O(Ha^2L)=O_C(1/L_2),\qquad
 \mathbb P_2(C(h)>1)=O_C(1/L_2).                       \tag{5}
\]

取 \(q=\lfloor L_3\rfloor\)，则 \(qa=o(1)\)、\(q^2/L_2=o(1)\)，并有

\[
 \boxed{\delta\le X^{-CL_3(1-o(1))}},                  \tag{6}
\]

而 \(W^q\) 的相对非零 Fourier 能量仍只有

\[
 O_C(L_3^2/L_2)=o(1).                                  \tag{7}
\]

所以第八轮的辅助条件 \(B\to\infty\) 不是必要条件；固定 \(B=2\) 已足够。
完整推导及 QA 见 fixed_exponent_tilt_refinement.md 与
ROUND9_INTERNAL_QA.md。

关键限制是：(5)--(7) 都是完整周期相对能量陈述。全模数仍满足

\[
 \log Q=(1+o(1))z=\exp(L_1/L_2+o(1)),
\]

故一般 Parseval 的 \(Q/X\) 损失不能由 (7) 吸收。

## 3. stopping-line 的新定量化

对 \(W^q\) 写

\[
 b=1-(1-a)^q,\quad x_p=H/p,\quad
 m_p=1-bx_p,\quad d_p=-b(X_p-x_p).
\]

局部绝对比率满足

\[
 \rho_p={\mathbb E|d_p|\over m_p}
 \le {3bH\over p},\qquad \sum_p\rho_p=O_C(qL_1).       \tag{8}
\]

将素数递减排序，在选中导子首次超过 \(D=X^\kappa\) 时停止。每个 crossing
导子 \(c\) 满足 \(D<c\le Dz=X^{\kappa+o(1)}\)。初等对称多项式界给出

\[
 \log\!\sum_{c(T)\le X^\kappa z}\prod_{p\in T}\rho_p
 =O_C\!\left({L_1L_3\over L_2}\right)=o(L_1).          \tag{9}
\]

因此全部 stopping 前沿即使取绝对值，也只付 \(X^{o(1)}\)。

同一估计还把严格可传递的截断范围从第八轮的
\(\kappa<2/3\) 推到任意固定 \(\kappa<1\)。若
\(W_{\le X^\kappa}\) 表示只保留 \(c(T)\le X^\kappa\) 的 ANOVA 项，则
（以下对 \(q=1\) 以及本轮 \(q=\lfloor L_3\rfloor\) 均成立）

\[
 \boxed{
 \sum_{n\in I}W_{\le X^\kappa}(n)
 =N\mu\{1+O(X^{-1+\kappa+o(1)})\}.
 }                                                     \tag{9a}
\]

证明只用每个非空项的均值为零、周期为 \(c(T)\)，以及一个残缺周期的绝对值
不超过 \(c(T)\) 倍精确周期 \(L^1\) 均值。这是完整的截断区间定理，但不是
正权全和的区间定理。

还可令截断点随 \(X\) 逼近区间长度。置
\(\Phi=L_1L_3/L_2\)，并显式取

\[
 D=X\exp(-2\Phi)=X^{1-2L_3/L_2}.
\]

仍满足 \(Dz<X\)，并且

\[
 \boxed{
 \sum_{n\in I}W_{\le D}(n)
 =N\mu\{1+O(e^{-\Phi})\}.
 }                                                     \tag{9b}
\]

所以未处理部分可进一步压缩到距离 \(X\) 仅一个
\(X^{O(L_3/L_2)}\) 因子的极高导子尾。

固定 \(r\bmod c\)，写 \(n=r+c\ell\)。因 \(c\) 与所有后缀素数互素，乘以
\(c\) 在每个后缀模数上是置换；原来的 \(H\) 个禁余数精确变成另外 \(H\)
个互异禁余数。因此后缀严格变成长度 \(N/c\) 的同类权重，而不是近似模型。

若这种任意禁余数后缀在长度 \(M\) 区间上的最坏相对上界记为
\(A(M)\ge1\)，按 crossing 导子条件化并使用周期 \(L^1\) 范数可得

\[
 \boxed{
 {|\text{高导子尾}|\over N\mu}
 \le X^{-1+\kappa+o(1)}
 +X^{o(1)}
  \sup_{M=X^{1-\kappa+o(1)}}A(M).
 }                                                     \tag{10}
\]

低导子非零项也由同一绝对比率控制为 \(X^{-1+\kappa+o(1)}\)。完整证明见
stopping_line_conditional_suffix.md；有限模型中的恒等式由
verify_stopping_line.py 穷举验证。

(10) 是本轮最接近闭合的接口：若能对实际继承的起点相位证明
\(A(M)=M^{o(1)}\)，则 (1) 成立，再结合 (6) 即给出原题第一问的负答。

但把该输入扩大为“对所有起点、所有任意禁余数集统一”是严格不可能的。对任意
有限后缀，在每个素数处选一个允许余数，CRT 给出
\(W_{\rm suf}(\ell_0)=1\) 的 all-inactive 类。取包含 \(\ell_0\) 的长度 \(M\)
区间就有

\[
 A(M)\ge(M\mu_{\rm suf})^{-1}.                         \tag{11}
\]

第一层递归的放大家族包含
\(\mu_{\rm suf}=X^{-qC+o(q)}\)、\(M=X^{1-\kappa+o(1)}\) 的顶端后缀，
所以 (11) 远大于 \(M^{o(1)}\)。后续证明必须保留
由原区间和 crossing residue 共同决定的起点相位，不能调用任意平移黑箱。

采用 (9b) 的 moving cutoff 时，最短后缀区间尺度可进一步写成

\[
 M=\exp\{(2+o(1))\Phi\},\qquad \log z=o(\Phi),
\]

而前沿代价为 \(e^{(1/2+o_C(1))\Phi}=X^{o(1)}\)。这仍未消除 (11)，但给出了下一轮
带端点、带相位递推应使用的最窄严格尺度。

当前不能把 (10) 自身当作该输入。直接递归会使区间长度比剩余素数质量下降得更快；
终端尺度的平凡界 \(A\le\mu_{\rm suf}^{-1}\) 会返还全部指数。前沿因子只是次幂
而非多项式收缩，尚不能吸收这个损失。

## 4. 排除或收窄的路线

### 4.1 分块传递加标量 Hölder

即便乐观假设每个 \(X^{O(1)}\)-模数块的所需矩都可传递，广义 Hölder 仅保留

\[
 O(aH)=O(L_1/L_2)=o(L_1)
\]

的零频指数。因此逐块黑箱传递再只组合标量平均值不能闭合。

### 4.2 低导子平方和主函数

若平方根多项式只含 \(c(S)\le D_0\)，其 all-inactive 点的 Christoffel 核
\(K(D_0)<D_0^2\)。保持平方后导子不超过 \(X^\kappa\) 迫使
\(D_0\le X^{\kappa/2}\)，任何此类 SOS 主函数均值至少 \(X^{-\kappa}\)，
远大于所需 \(X^{-C+o(1)}\)。这不排除一般有符号主函数。

### 4.3 常规多项式层级 Selberg 分母

对任意容许增长矩，乐观软密度 Selberg 分母在 \(D=X^\theta\) 上满足

\[
 \log G_q(D)
 \ll {L_1\over BL_2}\log\{O(qBL_2)\}=o(qL_1),
\]

而完整周期目标指数是 \((qC+o(q))L_1\)。标准多项式层级分母路线指数级不足。
随机 thinning/fundamental-lemma 审计得到同一维数失配；有限 minimax LP
则表明不能据此声称所有非 SOS 有符号主函数都失败。

## 5. 可复核计算

所有有限计算均单线程、低优先级运行。

stopping-line 恒等式命令：

    taskset -c 1 nice -n 10 python artifacts/erdos_campaign_20260722_round9_6h/work/679/verify_stopping_line.py

参数为 \(H=2,t=0.7\)，素数 \(3,5,7,11,13\)，全模数 \(15015\)，四个
cutoff、两种排序、全部余数。最大误差 \(2.220\times10^{-16}\)，PASS。

有符号低导子 minimax LP 命令：

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 taskset -c 1 nice -n 10 python artifacts/erdos_campaign_20260722_round9_6h/work/679/minimax_majorant_probe.py

十个 Bernoulli 坐标、全部 1024 个模式。最优均值与精确均值之比随 cutoff 从
\(1.612845\) 降至 \(1\)。这只是有限反例筛查，不是渐近证明。不稳定的对称
二项式 LP 输出已丢弃，未作为证据。

## 6. 外部状态与文献

2026-07-22 重新核对 https://www.erdosproblems.com/679 ：页面仍标为
**OPEN**，且第一问没有评论区声称的部分或完整解。

Olivier Ramaré 的 *The weighted large sieve through Parseval*
（https://arxiv.org/abs/2605.29470）当前已撤稿；arXiv 记录注明发现
“Important miscalculation”，且当前无 PDF。本轮未使用该稿任何结论。

## 7. 严格结论与下一步

本轮没有证明 (1) 或原题，没有推翻已接受证明，没有得到可直接投稿 SCI 二区的
原题主定理，也没有用有限计算替代渐近证明。

最值得继续的路线是保留 stopping 状态中的三个变量——当前区间长度、当前后缀
素数端点、继承的起点相位——建立带相位的更新方程。必须证明 crossing 核在后缀
零频质量尚大时带来真实收缩，或证明继承相位下终端大素数后缀的单边界；仅取
\(\sup A(M)\) 会丢掉这项信息并触发 (11) 的严格反例。

严格最终状态：**完整周期参数定理显著加强；前沿熵已压到次幂；
条件后缀区间定理仍缺；Erdős #679 继续开放。**

## 8. 资源与冻结

统一计费区间为 2026-07-22 14:42:16--16:12:16（Asia/Hong_Kong），
共 5400 秒。环境观察到 8 个逻辑 CPU；本流所有有限计算固定单核
（taskset -c 1，理论占用上限 12.5%），并使用 nice -n 10；LP 的 BLAS
线程也固定为 1。16:12:16 后未新增证明内容，只完成终态字段、清单与校验和。
