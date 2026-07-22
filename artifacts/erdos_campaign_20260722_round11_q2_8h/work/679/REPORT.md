# Erdős #679 第十一轮：增长矩、低导频谱小偏差与超高导数尾

日期：2026-07-22--23（Asia/Hong_Kong）
统一计费窗口：2026-07-22 22:15:18--2026-07-23 00:15:18（7,200 秒）。

## 0. 总判定

本轮得到一个严格的主尺度约化，但 **Erdős #679 第一问仍开放，原题闭合数
为 0，Q2=false**。

第一问询问：对每个固定 \(\varepsilon>0\)，是否存在无穷多个 \(n\)，使得
对所有超过一个只依赖于 \(\varepsilon\) 的固定起点且 \(k<n\) 的整数
\(k\)，都有

\[
 \omega(n-k)<(1+\varepsilon){\log k\over\log\log k}.
\]

本轮继续攻击这一开放的第一问；官网所列较强加法误差版本的既有否定结果
不计入本轮闭合数。

最新来源边界也没有改变这一状态：Lau arXiv:2604.15042v2 的
Theorem 1.3 **无条件**达到 \(C\log k\)，而该文关于“#679 为假”的
Section 7 结论以一个未证短区间密度猜想为前提；官网仍标为 Open。

最强结果是：对每个先固定的 \(0<\eta<1\)，增长 Markov 矩与 primitive
Farey 大筛能在实际区间起点上把全部

\[
 c(T)\le \exp\{(1-\eta)HL\}
 =X^{(1-\eta+o(1))L_1L_2}                         \tag{R1}
\]

的非零 ANOVA 导数的总有符号贡献压到
\(\exp\{-(\eta-o(1))HL\}\)。其中 \(L_j=\log_jX\)、
\(H=\lfloor L_1^2\rfloor\)，
\(L=\sum_{H<p\le z}p^{-1}\sim L_2\)，
\(z=\exp(L_1/L_2)\)。

若一个原题候选落在长度 \(N\asymp X\) 的实际区间内，则余下
\(c(T)>\exp\{(1-\eta)HL\}\) 的**总有符号和**必须为正且至少
\(\exp\{-o(HL)\}\)。本轮没有给出这个超高导数有符号尾的上界，因此
(R1) 不是原题证明或证否。

同一证明对任意先固定的 \(d\ge1\) 也成立：取
\(H=\lfloor L_1^d\rfloor\) 时，截断变为
\[
 \exp\{(1-\eta)HL\}
 =X^{(1-\eta+o(1))L_1^{d-1}L_2},
\]
而候选阈值中的常数 \(2\) 变为 \(d\)。正文为简洁仍以 \(d=2\)
书写；这一鲁棒性使约化能匹配 Lau 短区间模板中的任意固定 \(d\)，但不
提供该模板所需的高-\(\omega\) 密度定理。

## 1. 增长矩与完整周期矩

令

\[
 a={CL_1\over HL},\qquad t=1-a,\qquad
 q=\left\lfloor{s(X)\over a}\right\rfloor,
\]

其中 \(C>0\) 固定，\(s\to\infty\)、\(s=o(L_3)\)。于是

\[
 b_1=1-t^q=1-o(1),\qquad b_2=1-t^{2q}=1-o(1).
\]

固定一个含 \(H\) 个连续平移的块。令 \(X_p(n)\) 表示
\(p\) 是否整除其中某个 \(n-K-j\)（\(0\le j<H\)）；因 \(p>H\)，
它是恰有 \(H\) 个命中余数的 \(0\)--\(1\) 指标。定义

\[
 W(n)=\prod_{H<p\le z}t^{X_p(n)}.
\]

局部命中指标 \(X_p\) 在 \(p>H\) 时恰有 \(H\) 个禁余数。故
\(W^q\) 的完整周期一、二阶矩为

\[
 \mu_q=\prod_{H<p\le z}\left(1-{b_1H\over p}\right),
 \qquad
 M_{2,q}=\prod_{H<p\le z}\left(1-{b_2H\over p}\right). \tag{R2}
\]

在 \(H<p<2H\) 不能错误地逐项使用 \(H/p=o(1)\)。把该段单列：
每个因子至少 \(1-H/p\ge(2H)^{-1}\)，而该段只有
\(O(H/\log H)\) 个素数，故总对数代价 \(O(H)=o(HL)\)。
在 \(p\ge2H\) 上可一致 Taylor 展开，二次误差也是 \(o(HL)\)。
因此

\[
 \log\mu_q=-(1+o(1))HL,\qquad
 \log M_{2,q}=-(1+o(1))HL.                         \tag{R3}
\]

## 2. 新增的低导频谱小偏差

写

\[
 W(n)^q=\sum_TF_T(n),\qquad
 F_T(n)=\prod_{p\notin T}m_p\prod_{p\in T}d_p(n),
\]

其中 \(m_p=1-b_1H/p\)，\(\mathbb E d_p=0\)。Parseval 与 ANOVA
正交性给出

\[
 \sum_T\sum_u^*|\widehat F_T(u)|^2=M_{2,q}.         \tag{R4}
\]

把 (R4) 的每个 \(T\)-能量除以 \(M_{2,q}\)，得到一个坐标独立但
不要求同分布的随机子集。令 \(x_p=H/p\)，则其入选参数精确为

\[
 \theta_p=
 {b_1^2x_p(1-x_p)\over1-(2b_1-b_1^2)x_p}\le x_p.  \tag{R5}
\]

对 \(p\ge2H\)，一致地有

\[
 {\theta_p\over x_p}
 ={b_1^2(1-x_p)\over1-x_p+(1-b_1)^2x_p}
 =1+O(1-b_1)=1+o(1).
\]

低端段的总贡献只有 \(O(H/\log H)\)，所以

\[
 \Lambda:=\sum_p\theta_p=(1+o(1))HL.               \tag{R6}
\]

若固定 \(\alpha>0\) 且 \(c(T)\le e^{\alpha HL}\)，由于每个
\(p>H\)，必有

\[
 |T|\le r_\alpha={\alpha HL\over\log H}
 =(\alpha/2+o(1))H.                                \tag{R7}
\]

这里 \(\log H=2L_2+o(1)\)、\(L\sim L_2\)，因而
\(\Lambda/r_\alpha\asymp L_2\)，并且

\[
 r_\alpha\log(\Lambda/r_\alpha)=O_\alpha(HL_3)=o(HL).
\]

令 \(S=|T|\)。对任意 \(0<y<1\)，非同分布独立性仍精确给出

\[
 \mathbb Ey^S
 =\prod_p(1-\theta_p+\theta_py)
 \le e^{-(1-y)\Lambda}.
\]

在 \(S\le r_\alpha\) 上 \(y^S\ge y^{r_\alpha}\)。取
\(y=r_\alpha/\Lambda\)，得到

\[
 \mathbb P(c(T)\le e^{\alpha HL})
 \le \exp\{-\Lambda+r_\alpha+
 r_\alpha\log(\Lambda/r_\alpha)\}
 =e^{-(1-o(1))HL}.                                 \tag{R8}
\]

将 (R8) 乘以 (R3) 的总能量，便得本轮关键增益

\[
 \boxed{\displaystyle
 \sum_{c(T)\le e^{\alpha HL}}\sum_u^*
 |\widehat F_T(u)|^2
 \le e^{-(2-o(1))HL}.}                             \tag{R9}
\]

累计低导能量的指数 2 即使删去空集也无法改进：对 \(p\ge2H\)，
\[
 v_p={\mathbb E d_p^2\over m_p^2}
 ={H/p\over1-H/p}(1+o(1)),\qquad
 \sum_{p\ge2H}v_p=(1+o(1))HL.
\]
这些单素数分母都低于 \(e^{\alpha HL}\)，其总能量
\(\mu_q^2\sum v_p=e^{-(2+o(1))HL}\)。因此非零累计低导能量的对数
渐近本身就恰为 \(-2HL\)。这只说明能量指数尖锐；单素数项位于远小于
\(e^{\alpha HL}\) 的导数，故不排除按导数分层后改进全局最坏 Farey
间距因子。初步估计只使用总能量 \(e^{-HL}\)，
因而只能到系数 \(1/2\)；(R8)--(R9) 把它严格提升为系数 \(1\)。

## 3. Primitive Farey 大筛达到 (R1)

每个非空 \(F_T\) 的完整导数为
\(c(T)=\prod_{p\in T}p\)。局部零均值使所有非零 Fourier 频率都是
既约分数 \(u/c(T)\)，\((u,c(T))=1\)。不同 \(T\) 对应不同平方自由
分母，故频率列表没有重复。

现在先固定 \(0<\eta<1\)，置 \(\alpha=1-\eta\)，然后才令
\(X\to\infty\)。分母不超过

\[
 {\cal C}_X=e^{(1-\eta)HL}
\]

的不同既约分数圆周间距至少为 \({\cal C}_X^{-2}\)。由 (R9) 和
加法大筛，对任意整数起点的区间 \(I\)、\(|I|=N\asymp X\)，

\[
 \sum_{n\in I}|{\cal E}_{\le{\cal C}}(n)|^2
 \le (N-1+{\cal C}_X^2)e^{-(2-o(1))HL}.
\]

再在物理区间作一次 Cauchy，且 \(\log N=o(HL)\)，得

\[
 \boxed{\displaystyle
 \left|\sum_{n\in I}{\cal E}_{\le{\cal C}}(n)\right|
 \le e^{-(\eta-o(1))HL}.}                          \tag{R10}
\]

这一步直接作用在规定的实际区间，不对完整 CRT 周期中的起点取平均。

## 4. 候选强迫正的超高导数尾

对候选的 \(H\) 个相邻平移，所选素数带的总命中数满足

\[
 T(n)\le R\le
 (2+o_\varepsilon(1))(1+\varepsilon){HL_2\over L_3}.
\]

由于 \(0<t<1\)，

\[
 W(n)^q=t^{qT(n)}\ge t^{qR},\qquad
 t^{-qR}=\exp\{o(HL)\}.                             \tag{R11}
\]

若 \(I\) 中有一个候选，则非负性给
\(\sum_IW^q\ge t^{qR}\)。将这个精确恒等式分成零模、(R10) 的
低导有符号和、以及高导有符号和；零模
\(N\mu_q=e^{-(1+o(1))HL}\)。固定 \(\eta\) 后，前两项都为
\(o(t^{qR})\)，所以

\[
 \boxed{\displaystyle
 \sum_{n\in I}\sum_{c(T)>{\cal C}_X}F_T(n)
 \ge {1\over2}t^{qR}
 =e^{-o(HL)}>0.}                                   \tag{R12}
\]

(R12) 的左边是所有超高 primitive 完整导数的**总有符号和**。它不是
绝对系数和，也不是该尾的上界；所以 (R12) 是候选的必要条件，而不是
矛盾。

## 5. 完整 CRT 周期中的异常相位密度

若 \(A\) 在 \(\mathbb Z/Q\mathbb Z\) 中均匀取值，平移不变性精确给出

\[
 \mathbb E_A\sum_{1\le m\le N}W(A+m)^q=N\mu_q.
\]

含一个局部候选的区间，其左边至少为 \(t^{qR}\)。Markov 不等式与
(R3)、(R11) 因而给

\[
 {1\over Q}\#\left\{A\bmod Q:
 \sum_{m\le N}W(A+m)^q\ge t^{qR}\right\}
 \le Nt^{-qR}\mu_q
 =e^{-(1-o(1))HL}.                                 \tag{R13}
\]

这把第十轮的多项式异常密度强化为 \(HL\) 指数级稀疏。但
\(\log Q\sim z\gg HL\)，允许的异常起点绝对数仍极大；而一个 CRT spike
会让约 \(N\) 个相邻区间起点同时异常。因此 (R13) 仍不能定位
\(A\asymp X\)。

## 6. 其他严格进展

固定矩版本也有两项较小但无条件的推进。

1. Rankin 技巧取 \(1/\log H\) 后，固定 \(q,C\) 的低导绝对质量满足
   \({\cal F}(Y)\le z^{K(q,C)}\)（\(Y\le Xz\)）。因此完整周期传递可
   到 \(D=Nz^{-B(q,C)}\)，停止后的继承后缀长度只剩固定的
   \(z^{O_{q,C}(1)}\)。
2. 利用 primitive 分母不碰撞，对任意先给定的固定 \(A\)，再选固定
   \(q\) 使 \(qC>A+1/2+\delta\)，可在实际区间确定性控制
   \(Nz^{-B}<c(T)\le X^A\)。这不是一个固定 \(q\) 同时控制所有 \(A\)。

增长矩定理已严格包含远大于所有固定 \(X^A\) 的范围，故 (R1) 是本轮
最终主结果。

## 7. 现有 Kloosterman 输入为何仍未闭合

增长矩展开不再有第十轮的 terminal suffix；这是一个真实简化。
精确剩余 Fourier 项含

\[
 {(-b_1)^{|T|}\gamma_T\over c(T)}
 \prod_{p\mid c(T)}
 D_H\!\left({u(c/p)^{-1}\over p}\right),
\]

因此与 Kloosterman 分数有结构联系。不过重新核对
[Bettin--Chandee](https://arxiv.org/abs/1502.00769) 与
[Wright 2026](https://arxiv.org/abs/2604.25177) 后，仍有三项不匹配：

1. 归一化能量下典型 \(|T|=(1+o(1))HL\)，典型
   \(\log c(T)=(1+o(1))H\log z\)，远高于 (R1)，是 many-prime
   ultra-high conductor，而非已陈述的直接三线性盒；
2. Dirichlet 核保留 \(H=(\log X)^2\) 个增长平移，不是固定因子数的
   divisor-bounded convolution；
3. 所需结论是规定 \(A\asymp X\) 上整个联合和
   \(o(e^{-o(HL)})\)，所核文献没有给出这一归一化。

因此没有把相似的相位形状误报成可直接引用的黑箱定理。

还有一个严格的量词障碍。对每个 \(p>H\) 选一个避开其 \(H\) 个禁余数的
类，CRT 给出某个 \(n_0\bmod Q\) 使 \(W(n_0)^q=1\)。把 \(n_0\) 放入
任意长度 \(N\asymp X\) 的区间；由 \(W^q\ge0\)，总矩至少为 1，而
(R10) 与零模估计对任意起点仍成立，所以该区间的超高导有符号和至少
\(1-o(1)\)。因此 **arbitrary-start 的长度-\(X\) 高尾小界本身为假**。
这不反驳所需结论：CRT 给出的代表元通常在巨大周期 \(Q\) 的尺度，而非
与参数自洽的 \(A\asymp X\)。最终定理必须使用这个实际位置限制。

另核对 2026 年
[van Doorn--Tang](https://arxiv.org/abs/2606.19863)：
在本题强迫的 run length
\(Y=e^{L_2\sqrt{L_3}}\) 下，其端点只到 \(e^{\Theta(L_2^2)}\)，
而实际端点为 \(X=e^{L_1}\)，不能覆盖本题量词。

最后核对了 2026 年更新的
[Tao--Teräväinen](https://arxiv.org/abs/2512.01739)。其 Theorem 1.1
证明 #248：存在无穷多个 \(n\) 使所有正整数 \(k\) 都满足
\(\omega(n+k)\le\Omega(n+k)\le Ck\)。但其 Remark 1.2 直接写出
#679 的 \((1+\varepsilon)\log k/\log_2k\) 目标，并明确判断现有方法
尚不能达到。该文的核心同步维数为 \(O(\log_2X)\)，而这里需要处理
\(H=(\log X)^2\) 个平移以及规定 dyadic 起点处的超高导数有符号尾；
因此其 theorem 不能填补 (R12) 后的缺口。这是直接的最新主文献边界，
而不是从题名或摘要作出的推测。

沿该文的前向引用又核对了 2026-06-24 的
[Lau v2](https://arxiv.org/abs/2604.15042)，这是与 #679 最直接的
当前边界。其 Theorem 1.3 无条件证明：存在绝对常数 \(C\) 和无穷多个
\(n\)，使所有 \(1<k<n\) 都满足
\(\omega(n-k)\le\Omega(n-k)\le C\log k\)。原文明确指出，这距离
#679 第一问仍差一个 \(\log\log k\) 因子。该文猜测 \(C\log k\) 的阶
基本最优，并在另一个短区间密度猜想下推出 #679 第一问为假；这些是
条件结论，不能计作证否。它与本轮方向一致，但没有给出 (R12) 的有符号
尾上界。

Lau 的条件论证也给出另一条精确充分路线：若能证明存在常数
\(1\le d<C_0\)，使每个充分大的 \(x\) 的末端区间
\((x-(\log(x/2))^d,x]\) 都含某个
\(\omega(m)\ge C_0\log_2m/\log_3m\) 的整数，则 #679 第一问为假。
这一路线目前仍以未证猜想为前提；van Doorn--Tang 的现有端点范围也不
足以推出它。

这与本轮参数并非偶然相似：\(H=(\log X)^2\) 正对应 \(d=2\)，而候选在
\(k\asymp H\) 处只允许
\((2+o_\varepsilon(1))(1+\varepsilon)L_2/L_3\) 个不同素因子。
所以固定 \(C_0>2(1+\varepsilon)\) 的逐块高-\(\omega\) 结论会直接
证否。这是 Lau 短区间模板的 \(d=2\) 特化；其原猜想只要求存在某个
\(1\le d<C_0\)，并未单独证明或断言 \(d=2\)。本轮频谱约化是在另一
语言下定位同一个局部密度瓶颈。

## 8. 验证、资源与发表边界

有限脚本 **verify_growing_moment.py** 在
\(H=2\)、素数 \(5,7,11\)、\(q=17\) 上核验：

- ANOVA 重构与 Fourier 反演；
- 非 primitive 系数为零；
- Parseval 与精确二阶矩；
- 归一化能量恰为非同分布 product-Bernoulli，且
  \(\theta_p\le H/p\)；
- Farey 间距与有限大筛不等式。

全部通过；最大 Fourier 反演误差为
\(7.19\times10^{-15}\)。这只验证有限代数，不承担渐近证明。
脚本始终使用一个固定 CPU 核、低优先级、单进程；最终重跑与记录输出逐字节
一致。其余均为符号推导。

最终边界：

- 原题证明或证否：**无**；
- 已关闭原题数：**0**；
- 仍缺：对 (R12) 的 ultra-high signed aggregate 给出
  \(o(t^{qR})\) 上界。一个完全精确的充分目标是对每个充分大的
  dyadic \(X\) 证明
  \[
  \sum_{X<n\le2X}{\cal E}_{>\exp((1-\eta)HL)}(n)
  =o(t^{qR});
  \]
- 另一充分路线：证明 Lau 的固定幂短区间高-\(\omega\) 密度猜想；
- Q2 提前停止：**false**；
- 最近已知边界：Lau Theorem 1.3 是无条件 \(C\log k\) 部分结果；
  条件否定不是证否，官网仍为 **OPEN**；
- SCI 二区评价：当前是可复用的结构引理与明确接口，尚不足以作为闭合开放
  问题或改变公认主指数的独立 Q2 主结果。
- 资源冻结：统一硬边界为 2026-07-23 00:15:18 HKT，严格计费
  7,200 秒；边界后仅复跑既定验证并冻结文件，输出逐字节一致，未再新增
  证明或检索。
