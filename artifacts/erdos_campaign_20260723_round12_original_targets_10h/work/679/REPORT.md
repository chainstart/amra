# Erdős #679：移动导体、远端临界与候选稀疏性审计

日期：2026-07-23（Asia/Hong_Kong）  
统一计费窗口：2026-07-23 06:28:31--08:58:31（9,000 秒）。

## 0. 原题级结论

本轮没有证明或证否 #679 的第一个问题：

\[
\forall\varepsilon>0\ \exists K_\varepsilon\ \forall N_0\ \exists n>N_0\
\forall\,K_\varepsilon\le k<n:\quad
\omega(n-k)<(1+\varepsilon){\log k\over\log_2k}.
\]

**公开状态仍为 OPEN，原题闭合数为 0。** 已被证否的加常数第二问与本报告
的闭合计数分开。以下均为部分定理、必要条件或方法边界。

## 1. 移动导体的熵最优必要条件（本轮新）

取
\[
H=\lfloor(\log X)^d\rfloor,\quad
z=\exp(\log X/\log_2X),\quad
L=\sum_{H<p\le z}p^{-1},
\]
\[
r_\varepsilon(k)=
\left\lceil(1+\varepsilon){\log k\over\log_2k}\right\rceil-1,\quad
R=\sum_{H\le k<2H}r_\varepsilon(k),\quad \rho={R\over HL}.
\]
则 \(\rho\sim(1+\varepsilon)d/\log_3X\)。完整 ANOVA/Parseval 与
additive large sieve 计算证明：每个原题候选都迫使导体
\[
c(T)>
\exp\left(\left[I(\rho)-{1\over\log_3X}\right]HL\right),\qquad
I(\rho)=1-\rho+\rho\log\rho,
\]
以上的 Fourier 项具有正的 signed 总和，且至少为
\((1-o(1))\rho^R\)。导体系数趋于
\(1-O(\log_4X/\log_3X)\)。这是高导体 signed-tail 的必要条件，
不是尾部上界。

允许每个 shift 采用独立 tilt 后，精确优化器为 \(y_j=r_j/L\)，但相对
aggregate tilt 的增益只有 \(O(H\log_3X/\log_2X)\)，不改变主导 cutoff。
同一 cutoff 的 top-prime 窄带同时饱和总能量、有效 support 与 Farey
间距。因此仅凭这三项不能再取得固定指数增益；coefficient-sensitive
phase cancellation 仍未排除。

## 2. 远端 Hardy--Ramanujan cutoff（本轮新）

令 \(A=1+\varepsilon\)、\(B=\log_2X\)、\(L=\log_3X\)。对任意固定
\[
D>{A\over\varepsilon},\qquad K_X=\exp(B^D)
\]
有
\[
\#\{n\in[X,2X]:\exists\,K_X\le k<n\text{ 违反原题界}\}
\ll_{\varepsilon,D}{X\over\log X}K_X^{-\eta_D/2},
\quad \eta_D=A(1-1/D)-1>0.
\]
可显式取 \(D=2A/\varepsilon\)，saving 为
\(K_X^{-\varepsilon/4}\)。

在临界幂 \(D_0=A/\varepsilon\) 处，固定
\(C_*>(e/\varepsilon)^{D_0}\) 亦可。本轮进一步分类常数边界。置
\[
M=\log_4X,\quad C_0=(e/\varepsilon)^{D_0},\quad
C_X=C_0\exp(3D_0M/L),
\]
\[
K_X^\dagger=\exp(C_XB^{D_0}L^{D_0})+O(1),\qquad
\xi_X^\dagger={AM\over5D_0L^2}.
\]
在 literal equality \(C=C_0\) 时，HR union-bound 超额量的下一项为
\[
-D_0\log\left(1+{M+1-\log\varepsilon\over L}\right)+o(M/L)<0.
\]
采用 \(C_X\) 后则为
\[
{D_0(2M-1+\log\varepsilon)\over L}
+O_\varepsilon(D_0M^2/L^2)>0,
\]
从而
\[
\#\{\text{far-bad endpoints}\}
\ll_\varepsilon {X\over\log X}
{(K_X^\dagger)^{-\xi_X^\dagger}\over\xi_X^\dagger}.
\]
而且
\[
\xi_X^\dagger\log K_X^\dagger
={AC_X\over5D_0}B^{D_0}M L^{D_0-2}\to\infty.
\]
量词为先固定 \(\varepsilon\)，再令 \(X\to\infty\)；
\(C_X/C_0\to1\)，但 cutoff 仍随 \(X\) 增长。负号只分类该
HR union-bound 方法，不是原题边界。

## 3. 低 cutoff 的 block obstruction（本轮新）

直接核对 Goudout 2017 的正式 Theorems 1--2 后得到：

- 若 \(H=e^{CBL}\)、\(C>0\) 固定且 \(AC>1\)，则几乎每个
  \(n\asymp X\) 都在 \(H\le k<2H\) 中出现违反 shift；此处 block
  rare exact level 是实质。
- 对某个无效但趋于无穷的 \(G(X)\)，可沿对角线延伸到
  \(H=e^{G(X)BL}\)；没有声称对任意给定 \(G\) 一致。
- 在 \(H=(\log X)^{1-o(1)}\) 附近的三、四阶展开只定位
  “区间内含 exact level”方法；一个固定 shift 的 normal order 已足以
  造成 almost-all violation，因此它不是更强的 #679 转变定理。

第三阶系数 \(C_3\sim A^3T^3>0\)，下一阶
\(C_4\sim-A^4T^4<0\)，其中 \(T=M+1-\log A\)。符号与所有取整、
Stirling、Euler factor 误差均经独立脚本核验。

## 4. 候选稀疏性：正式二平移与继承结果

固定 \((\varepsilon,K)\)，记候选集为
\({\cal G}_{\varepsilon,K}(X)\subset[X,2X]\)。

逐字使用 Goudout 已正式证明的 **fixed \(b=1\) 二平移 corollary**，
而不使用其“更多 shifts”remark，得到
\[
\boxed{\#{\cal G}_{\varepsilon,K}(X)
\ll_{\varepsilon,K}{X\over(\log X)^{2-o(1)}}.}
\]

本轮还重核早期 campaign 已记录的 Tenenbaum 2018 任意固定维正式定理。
为避开连续因子的 fixed-divisor 陷阱，取
\[
P_r=\prod_{p\le r}p,\qquad Q_j(m)=m-jP_r.
\]
其乘积无固定素因子，故
\[
\#{\cal G}_{\varepsilon,K}(X)
\ll_{\varepsilon,K,r}{X\over(\log X)^{r-o(1)}}.
\]
于是对每个固定 \(C>0\)，候选数为
\(O_{\varepsilon,K,C}(X/(\log X)^C)\)。此项严格标为
**inherited/revalidated，不是 round-12 新成果**。它不推出候选有限。

## 5. Lau 权重质量审计（本轮改进）

Lau v2 的正式公式给出 \(Z=\sum_n\nu(n)=x^{0.4+o(1)}\)。
源文定义 \(\widetilde\eta(u)=e^{-u}\eta(u)\)，其中
\(\eta:\mathbb R\to[0,1]\) 支撑于 \([-1,1]\)，故每个 divisor sum
\[
|S_k(n)|\le\min\{R_k,\tau(n+k)\}.
\]
由 \(k\le K=(\log x)^{1/1000}\)、\(n+k\le3x\) 与统一 divisor bound，
\[
{\log\max\nu\over\log x}
\le2\sum_{k\le K}
\min\left\{{1\over100k^{50}},{C\over\log_2x}\right\}
=O((\log_2x)^{-49/50}).
\]
所以
\[
\boxed{\max\nu=x^{o(1)},\qquad
\#\{\text{Lau 的 }C\log k\text{ 见证}\}\ge x^{0.4-o(1)}.}
\]
这强于旧粗界，但 Lau 的结论仍非 #679 阈值；远端异常集仍可有
\(x^{1-o(1)}\) 个元素，density ratio 只控制到 \(x^{0.6+o(1)}\)，
不能强制相交。Spiro 的 progression 定理仅统一到 polylog modulus，
也不能直接处理 \(W=x^{0.6+o(1)}\)。

## 6. 剩余缺口

Menon 2026 的一般短区间定理只处理 1-bounded multiplicative
functions，不能承载这里 \(z\asymp r/B\gg1\) 的 saddle。primorial
translation、shiftwise tilts、总能量/support/spacing 及 black-box
density splice 也均已到达其可证明边界。

目前最明确的闭合接口是：

1. 在移动熵 cutoff 以上证明 coefficient-sensitive 的 signed
   high-conductor upper bound；或
2. 直接在 Lau 型非均匀近端权重下证明远端大偏差，并同时把
   \(C\log k\) 改进到原题阈值。

本轮没有得到任一接口，故原题仍开放。

## 7. 复现与资源

有限计算只作符号恒等式/误差审计，不作为渐近证据。复现命令为：

    nice -n 10 taskset -c 7 python3 verify_moving_cutoff.py
    nice -n 10 taskset -c 7 python3 verify_goudout_cutoff_series.py
    nice -n 10 taskset -c 7 python3 verify_far_critical_boundary.py

三个输出均为 PASS。正式证据见 INDEPENDENT_QA.md，来源边界见
SOURCE_MANIFEST.json。本任务按统一窗口计费 9,000 秒；CPU 低于 WSL
资源的 50%；原题闭合数为 0。
