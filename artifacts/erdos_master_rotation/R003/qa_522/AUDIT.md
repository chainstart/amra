# Erdős #522 独立二审

## 最终判定

**`VERIFIED_CLOSED`**

截至 2026-07-23，Erdős Problems 题页仍标为 `OPEN`；这只是官网登记状态。
本二审对 Przemek Chojecki 于 2026-04-27 公开的署名修订稿
[`erdos522-final.pdf`](https://www.ulam.ai/research/erdos522-final.pdf)
逐项重算后，没有发现缺失的概率量词、不可求和的异常概率、错误的协方差
比较、Nazarov--Nishry--Sodin（下称 NNS）输入错用、Jensen 符号错误或边界
零点遗漏。该稿证明了更强的结论
\[
 R_n=\frac n2+O_\omega(n^{399/400})\qquad\text{a.s.}
\]
因此在“公开署名证明稿的数学内容是否闭合原命题”这一层面，#522 可以判为
已闭合。

此结论不等于“已经同行评审”或“已经形式化”。检索到的公开载体是作者在
Erdős Problems 讨论区链接的署名 PDF；本二审没有把官网状态、作者自评或
数值实验当作证明依据。

## 1. 原题量词与修订稿是否一致

Erdős 原文（1961 重印稿，第 252 页，V.2.2）先固定一列独立 Rademacher
函数 \(\epsilon_k(t)\)，再问其第 \(n\) 个部分和
\[
 P_n(z)=\sum_{k=0}^{n}\epsilon_k(t)z^k
\]
的单位圆内根数是否对几乎所有 \(t\) 满足 \(R_n/n\to 1/2\)。这要求所有
\(n\) 共享同一条无限随机符号序列，而不只是每个 \(n\) 各自抽一组同分布
系数。

修订稿从同一列 \((\epsilon_k)_{k\geq0}\) 定义全部 \(P_n\)，并证明一个共同
概率一事件上的全序列估计。官网现行题面把根数定义在闭圆盘
\(\{|z|\leq1\}\)；修订稿也逐重数统计闭圆盘根，因而量词和边界约定均覆盖
现行 #522。旧文“unit circle/inside”若按开圆盘理解，修订稿的闭圆盘结论
仍更强。

## 2. Lemma 2.2：块插值重算

修订稿取
\[
 \rho_n=1-n^{-401/400},\qquad \tau_n=\rho_n^{-1},\qquad
 N_j=\lfloor j^4\rfloor .
\]
令 \(m=N_j\leq n<N_{j+1}\)，则
\[
 \Delta=n-m=O(m^{3/4}).
\]
对 \(r_N\equiv1,\rho_N,\tau_N\) 三种固定类型，后两者满足
\[
 \left|\frac{d}{dN}\log r_N\right|\ll N^{-801/400},
 \qquad
 |\log r_n-\log r_m|\ll m^{-501/400}.
\]
因此在 \(0\leq k\leq m\) 上
\[
 (r_n/r_m)^k=1+O(m^{-101/400})
             =1+O(m^{-1/4}).
\]

又因三种半径上 \(r_N^k\asymp1\) 且
\(\sigma_N(r_N)^2=\sum_{k\leq N}r_N^{2k}\asymp N\)，
\[
\begin{aligned}
 |\sigma_n(r_n)^2-\sigma_m(r_m)^2|
 &\ll \sum_{k\leq m}k\,m^{-501/400}+(n-m)\\
 &=O(m^{299/400})+O(m^{3/4})
  =O(m^{3/4}),
\end{aligned}
\]
故 \(\sigma_m(r_m)/\sigma_n(r_n)=1+O(m^{-1/4})\)。归一化系数
\(a_{N,k}(r)=r^k/\sigma_N(r)\) 因而给出
\[
 \sum_{k\leq m}|a_{n,k}(r_n)-a_{m,k}(r_m)|^2=O(m^{-1/2}),
\]
尾部则为
\[
 \sum_{m<k\leq n}a_{n,k}(r_n)^2
 \ll \frac{n-m}{m}=O(m^{-1/4}).
\]
合并后正是 Lemma 2.2 的 \(O(m^{-1/4})\) 平方距离；同一
\(\epsilon_k\) 乘在相同 Fourier 位上，Parseval 与 Cauchy--Schwarz 给出
\[
 \int|F_{n,r_n}-F_{m,r_m}|\,d\mu=O(m^{-1/8}).
\]
三条半径序列均合法，包括 \(r_n=\tau_n>1\)；此处只涉及有限 Fourier 和，
且 \(\tau_n^n=\exp(O(n^{-1/400}))\asymp1\)。

## 3. Proposition 3.3：二维及四维协方差

写
\[
 B_{n,r}(t)=\sum_{k=0}^na_{n,k}(r)^2e^{ikt}.
\]
几何级数恒等式和 \(\sigma_n(r)^2\asymp n\) 给出
\[
 |B_{n,r}(t)|\ll n^{-1}\operatorname{dist}(t,2\pi\mathbb Z)^{-1}
 \ll n^{-1/2}
\]
只要距离至少为 \(n^{-1/2}\)。该估计在
\([\rho_n,\tau_n]\) 上一致。

单点实二维向量的协方差确为
\[
 \frac12I_2+\frac12
 \begin{pmatrix}
 \Re B(2\theta)&\Im B(2\theta)\\
 \Im B(2\theta)&-\Re B(2\theta)
 \end{pmatrix}.
\]
两点四维向量的对角块分别使用 \(B(2\theta),B(2\phi)\)，非对角块由
\(D=B(\theta-\phi)\)、\(S=B(\theta+\phi)\) 组成：
\[
 \frac12
 \begin{pmatrix}
 \Re(D+S)&\Im(S-D)\\
 \Im(D+S)&\Re(D-S)
 \end{pmatrix}.
\]
所以排除
\[
 2\theta,\ 2\phi,\ \theta-\phi,\ \theta+\phi
\]
距 \(2\pi\mathbb Z\) 小于 \(n^{-1/2}\) 的四条带后，协方差在算子范数下为
\(\frac12I_4+O(n^{-1/2})\)。四条坏带的总
\(\mu\times\mu\) 测度是 \(O(n^{-1/2})\)，没有遗漏对角退化集。

每个 Lindeberg 加项的三阶矩总和为
\[
 O\!\left(\sum_k a_{n,k}^3\right)=O(n^{-1/2}).
\]
对 \(H(z,w)=h(z)h(w)\)，
\(\|H\|_{C^3}+\operatorname{Lip}H
\ll(\|h\|_{C^3}+\|h\|_\infty)^2\)。在好集上先做逐项
Lindeberg 替换，再把协方差接近的 Gaussian 与两个独立标准复 Gaussian
耦合；在坏集上用 \(\|h\|_\infty^2\)。积分后得到稿中的二阶矩式，结合
单点均值式即得
\[
 \operatorname{Var}\!\left(\int h(F_{n,r})\,d\mu\right)
 \ll(\|h\|_{C^3}+\|h\|_\infty)^2n^{-1/2}.
\]
附带脚本直接重构并比较了上述 \(4\times4\) 协方差矩阵。

## 4. NNS 输入适用性

NNS 原文 Corollary 1.2 的假设是：\(f\) 属于 Rademacher Fourier 子空间，
\(\|f\|_{L^2(\Omega\times\mathbb T)}=1\)，且 \(p\geq1\)。其结论为
\[
 \int_{\Omega\times\mathbb T}|\log|f||^p\leq(Cp)^{6p}.
\]
它允许任意复数 \(\ell^2(\mathbb Z)\) 系数。修订稿的
\[
 F_{n,r}(\theta)=\sum_{k=0}^na_{n,k}(r)\epsilon_ke^{ik\theta},
 \qquad \sum_ka_{n,k}(r)^2=1
\]
正是有限、正频率的特例。\(r=\rho_n,1,\tau_n\) 只改变确定性归一化系数，
不改变 Rademacher 独立性或 \(L^2\) 归一化，故外半径 \(\tau_n>1\) 也可
直接使用该定理。

Lemma 4.3 取 \(q_n=\lfloor\log n\rfloor\)，用 \(p=2q_n\) 后得到
\[
 \mathbb P\!\left\{\int|\log|F_{n,r_n}||^2>
 (\log n)^{20}\right\}
 \leq\left(\frac{C^{12}}{(\log n)^8}\right)^{q_n},
\]
该级数可求和。因此这里的 NNS 输入既不是点态小球估计，也没有错误地把
期望积分换成逐样本一致界。

## 5. Borel--Cantelli、小值集与去截断

修订稿固定
\[
 \eta=\frac1{100},\qquad\beta=\frac1{200},\qquad N_j\asymp j^4.
\]
所有关键指数独立复算如下：

| 环节 | 指数 | 所需条件 | 结果 |
|---|---:|---:|---|
| 平滑量端点异常概率 | \(N_j^{2\beta+6\eta-1/2}\) | \(4(2\beta+6\eta-\tfrac12)<-1\) | \(-43/25<-1\) |
| 小值端点异常概率 | \(N_j^{10\eta-1/2}\) | \(4(10\eta-\tfrac12)<-1\) | \(-8/5<-1\) |
| 块内 Lipschitz 误差 | \(N_j^{\eta-1/8}\) | \(\eta-\tfrac18<-2\eta\) | \(-23/200<-1/50\) |
| Gaussian 小值截断 | \(M^{-2}\log M\) | \(2\eta>\beta\) | 成立 |
| Cauchy--Schwarz 去截断 | \((\log n)^{10}M^{-1}\) | \(\eta>\beta\) | 成立 |

其中 \(M=N_j^\eta\)。对小值光滑指示函数 \(\chi_M\)，复 Gaussian 在零点
附近有有界二维密度，故 \(\mathbb E\chi_M(G)=O(M^{-2})\)，不是
\(O(M^{-1})\)。Chebyshev、上表第二行和块插值共同给出
\[
 \mu\{|F_{n,r_n}|\leq2M^{-1}\}=O(M^{-2})
\]
对所有充分大的 \(n\) 同时成立。

对平滑截断 \(\Lambda_M\)，异常集包含在小值集与
\(\{|F|>M\}\) 中；后者由确定性的
\(\int|F|^2\,d\mu=1\) 得到测度 \(O(M^{-2})\)。再结合 Lemma 4.3 的
对数二阶矩，
\[
 \int_{\mathrm{异常集}}|\log|F||\,d\mu
 \ll_\omega(\log n)^{10}M^{-1}=o(N_j^{-\beta}).
\]
因此
\[
 L_n(r_n)=\int\log|F_{n,r_n}|\,d\mu
 =\mathbb E\log|G|+O_\omega(n^{-\beta})
\]
在三种半径类型上分别成立；取三个概率一事件的有限交仍是概率一事件。

## 6. 三半径 Jensen、闭圆盘与外半径代换

内侧 Jensen 给出
\[
 R_n(-\log\rho_n)\geq
 \int\log|P_n(e^{i\theta})|\,d\mu-
 \int\log|P_n(\rho_ne^{i\theta})|\,d\mu,
\]
所以控制 \(r=1,\rho_n\) 产生下界。

上界只在固定的同一个 \(n\) 定义
\[
 Q_n(z)=z^nP_n(1/z).
\]
它不对 \((Q_n)_n\) 做任何块插值，而使用精确恒等式
\[
 Q_n(e^{i\theta})=e^{in\theta}P_n(e^{-i\theta}),\qquad
 Q_n(\rho_ne^{i\theta})
 =\rho_n^ne^{in\theta}P_n(\tau_ne^{-i\theta}).
\]
由此 \(Q_n\) 的 Jensen 差完全改写成已由 Proposition 4.5 控制的同一前缀
过程 \(P_n\) 在 \(1,\tau_n\) 上的对数积分。

因为 \(P_n(0),Q_n(0)\neq0\) 且 \(P_n\) 的次数恰为 \(n\)，倒数映射把
\(Q_n\) 的 \(|z|<1\) 根逐重数对应到 \(P_n\) 的 \(|z|>1\) 根。对每个
\(t<1\)，
\[
 N_{Q_n}(t)\leq n-R_n.
\]
单位圆上的根已计入 \(R_n\)，但不计入右侧的严格外部根，所以上式精确处理
闭圆盘边界，无需假设单位圆上没有根。

最后
\[
\frac{\log\sigma_n(1)-\log\sigma_n(\rho_n)}{-\log\rho_n}
=\frac n2+O(n^{399/400})
\]
及其 \(\tau_n\) 对偶式均由二阶 Taylor 展开和
\(\sigma_n(\tau_n)^2=\tau_n^{2n}\sigma_n(\rho_n)^2\) 得到。
对数积分误差除以
\(-\log\rho_n\asymp n^{-401/400}\) 后为
\[
 n^{401/400-\beta}=n^{399/400}.
\]
上下 Jensen 挤压因此给出所声明的全序列强律。

## 7. 旧稿跨 \(n\) 耦合缺口：独立确认

2026-04-20 旧稿定义
\[
 Q_n(z)=\sum_{k=0}^n\epsilon_{n-k}z^k
\]
并以“每个固定 \(n\)，\(Q_n\) 与 \(P_n\) 同分布”为由，把对 \(P_n\) 的
块插值结论移给整列 \((Q_n)_n\)。这不成立：一维边缘同分布并不保留跨
\(n\) 的联合耦合。

在 \(r=1\) 时令
\[
 q_n(\theta)=\frac1{\sqrt{n+1}}
\sum_{k=0}^n\epsilon_{n-k}e^{ik\theta}.
\]
若 \(m>n\)，则 Parseval 和
\(\mathbb E[\epsilon_{n-k}\epsilon_{m-k}]=0\) 给出
\[
\begin{aligned}
\mathbb E\int|q_m-q_n|^2\,d\mu
&=\mathbb E\|q_m\|_2^2+\mathbb E\|q_n\|_2^2
 -2\Re\mathbb E\langle q_m,q_n\rangle\\
&=1+1-0=2.
\end{aligned}
\]
它与旧稿所需的趋零块距离矛盾。该缺口对旧稿是致命的，因为旧稿上界依赖
\(Q_n\) 对全部 \(n\) 的几乎处处控制；固定 \(n\) 的同分布不能补上。
附带脚本对一个有限符号立方体精确枚举，复核交叉项总和为零。

修订稿第 6 节的外半径恒等式正好删除了这一步，所以旧稿缺口没有迁移到
修订稿。

## 8. 判定边界与建议登记

- 数学判定：`VERIFIED_CLOSED`。
- 证据类型：公开、署名、可下载的完整证明稿。
- 官网登记：审计时仍为 `OPEN`。
- 尚未由本二审确认的事项：同行评审、期刊发表、独立形式化。
- 建议中央记录（由主线程决定）：将“数学闭合”与“发表/形式化状态”分栏，
  不应因官网尚未更新而把证明判成未完成，也不应把本二审冒充期刊审稿。

本目录的 `verify_522_audit.py` 复核精确指数、旧稿耦合交叉项、三半径倒数
恒等式、\(\sigma\) 对偶式及四维协方差公式。它是审计证书，不替代上述
解析证明。
