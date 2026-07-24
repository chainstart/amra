# Erdős #1040：容量临界点的准入审计

## 结论先行

- 官网状态：`OPEN`（2026-07-24 抓取）。
- 原题第一问“\(\mu(F)\) 是否只由容量决定”：已被否定；这不是本轮新结果。
- 第二问在 \(\operatorname{cap}K>1\) 时已由 Ghosh--Ramachandran 2026 解决；在
  \(\operatorname{cap}K=1\) 的一般紧集上仍开放。闭包为有界 \(C^2\) 域、区间
  \([-2,2]\) 和 polynomial-generated/periodic 类等已有正结果。
- Pendyala 2026-06 另把单位圆盘/单位圆约束的最小面积锐化到
  \(\Theta(1/\log n)\)。这是 #116 的锐阶结果，不解决任意容量一紧集，但属于本题
  容量一边界必须冻结的最新结果。
- 本轮没有闭合一般临界情形，但得到一个严格的正面估计和一个严格的路线反例：
  1. 对 Fekete 多项式 \(p_n\)，
     \[
     \limsup_n m_2\{|p_n|<1\}\le m_2(\widehat K).
     \]
     因而若 \(K\) 紧、\(\operatorname{cap}K=1\)，且其多项式凸包
     \(\widehat K\) 的平面面积为零，则 \(\mu(K)=0\)。
  2. “零点测度趋于平衡测度 + 对数能量趋于最优”不能推出负势集合面积趋零；
     即使对单位圆盘也有显式反例。

因此，真正首断点不是能量收敛，而是容量一时平衡势在
\(\widehat K\) 上具有零平台，阈值 \(\{U<0\}\) 对无符号的能量/弱收敛不连续。

## 冻结题面和文献边界

对闭无限集 \(F\subset\mathbb C\)，令
\[
 \mu(F)=\inf \operatorname{area}\{z:|p(z)|<1\},
\]
其中下确界遍历所有零点均在 \(F\) 中的首一多项式。问题问它是否只由
transfinite diameter/logarithmic capacity 决定，特别问
\(\operatorname{cap}F\ge1\) 是否推出 \(\mu(F)=0\)。

已核对的当前边界：

1. Krishnapur--Lundberg--Ramachandran 2025 的 Theorem 6 只覆盖“有界
   \(C^2\)-光滑域的闭包且容量一”，不是任意容量一紧集。
2. 该文 Theorem 7 是“lemniscate 在 \(K\) 内面积趋零 \(\Rightarrow\) 零点测度弱收敛”，
   方向不能倒用。
3. Ghosh--Ramachandran 2026 Theorem 3.1 对任意紧集和固定 \(t>1\) 证明
   \(\operatorname{cap}K\ge t\Rightarrow A_n(K)\le e^{-\rho(t)n}\)；论文明确说一般
   capacity-one 情形仍开放。
4. Pendyala 2026 Theorem 1.1 证明
   \[
   c/\log n\le\kappa_n(\overline{\mathbb D},1)
   \le\kappa_n(\mathbb T,1)\le C/\log n.
   \]
   它补上单位圆盘的锐阶，但没有给一般 \(K\) 的 capacity-one 定理。

## 路线 A：零面积多项式凸包

### 命题（一般 hull-area 形式）

若 \(K\subset\mathbb C\) 是紧集，
\(\operatorname{cap}K=1\)，则存在零点全在 \(K\) 的首一 Fekete 多项式 \(p_n\)，使
\[
 \limsup_{n\to\infty}m_2\{z:|p_n(z)|<1\}
 \le m_2(\widehat K).
\]
特别地，若 \(m_2(\widehat K)=0\)，则这些面积趋零，故 \(\mu(K)=0\)。

### 证明

取 \(n\) 个 Fekete 点 \(z_{1,n},\ldots,z_{n,n}\in K\)，令
\[
 p_n(z)=\prod_{j=1}^n(z-z_{j,n}),\qquad
 \nu_n=\frac1n\sum_{j=1}^n\delta_{z_{j,n}}.
\]
对任意非极紧集，Fekete 经验测度弱收敛到平衡测度：
\(\nu_n\Rightarrow\nu_K\)。

令 \(\Omega=\mathbb C\setminus\widehat K\)，即 \(K\) 的无界补域。采用
\[
 U^\nu(z)=\int\log|z-w|\,d\nu(w)
\]
的符号约定，容量一给出
\[
 U^{\nu_K}(z)=g_\Omega(z,\infty)>0\qquad(z\in\Omega).
\]

固定 \(\delta>0\)。所有 lemniscate 都包含在固定有界集合
\(\{d(z,K)<1\}\) 中，因为 \(d(z,K)\ge1\) 时每个因子均至少为一。在紧集
\[
 L_\delta=\{z:d(z,K)\le1,\ d(z,\widehat K)\ge\delta\}
\]
上，核 \((z,w)\mapsto\log|z-w|\) 在 \(L_\delta\times K\) 连续。弱收敛和该函数族
的等度连续性给出
\[
 U^{\nu_n}\longrightarrow U^{\nu_K}
\]
在 \(L_\delta\) 上一致。右侧在 \(L_\delta\) 上有严格正的最小值，所以充分大 \(n\)
时 \(U^{\nu_n}>0\) 于 \(L_\delta\)，即 \(|p_n|>1\)。因此
\[
 \{|p_n|<1\}\subset\{d(z,\widehat K)<\delta\}.
\]
先令 \(n\to\infty\)，再令 \(\delta\downarrow0\)，利用紧集邻域的面积从上连续，
得到
\[
 \limsup_n m_2\{|p_n|<1\}\le m_2(\widehat K).
\]
零面积 hull 的结论立即随之成立。

### 审计

这条证明不要求 Green 函数在边界正则，也不把 Theorem 7 反向使用。零面积推论覆盖
例如容量归一化后的、补集连通的任意零面积 Cantor 型紧集。该推论不覆盖单位圆：
单位圆自身面积为零，但其多项式凸包是单位圆盘，面积为 \(\pi\)；这正是条件写成
\(m_2(\widehat K)=0\) 而不能只写 \(m_2(K)=0\) 的原因。

### 新颖性护栏

上述证明链在本轮范围内是严格的；本轮还补核了 Pendyala 2026-06，但仍没有完成
足以支持“首创”断言的系统新颖性检索。故本报告只把它登记为 `STRICT_PARTIAL`；
在查清潜在论著中的 Fekete lemniscate/hull-area 版本之前，不能把该命题宣传成
新定理或独立可发表成果。

## 路线 B：能量路线的显式反例

令 \(\lambda_s\) 是圆 \(|z|=s\) 上的均匀概率测度，并令
\[
 \nu_j=\left(1-\frac1j\right)\lambda_1+\frac1j\lambda_{e^{-j}}.
\]
对能量 \(I(\nu)=\iint-\log|z-w|\,d\nu(z)d\nu(w)\)，圆测度满足
\[
 I(\lambda_s)=\log(1/s),\qquad I(\lambda_1,\lambda_s)=0\quad(s<1).
\]
从而
\[
 \nu_j\Rightarrow\lambda_1,\qquad I(\nu_j)=\frac1j\longrightarrow0=I(\lambda_1).
\]
但圆测度势满足
\[
 \int\log|z-w|\,d\lambda_s(w)=\log\max(s,|z|),
\]
所以对每个 \(|z|<1\)，
\[
 U^{\nu_j}(z)=\frac1j\log\max(e^{-j},|z|)<0.
\]
于是 \(m_2\{U^{\nu_j}<0\}\ge\pi\) 对所有 \(j\) 成立。

这不是只存在于连续测度层面的现象。令 \(m=j^3\)，
\[
 p_j(z)=\bigl(z^{(j-1)m}-1\bigr)\bigl(z^m-e^{-jm}\bigr).
\]
它的全部 \(jm=j^4\) 个零点互异且在闭单位圆盘中，零点经验测度弱收敛到
\(\lambda_1\)。若 \(\rho_j=1-1/j\) 且 \(|z|\le\rho_j\)，则
\[
 |p_j(z)|
 \le(1+\rho_j^{(j-1)m})(\rho_j^m+e^{-jm}).
\]
由 \(\log(1-1/j)\le-1/j\)，当 \(j\ge2\) 时右侧严格小于
\[
 (1+1/16)(1/16+1/16)=17/128<1.
\]
故
\[
 B(0,1-1/j)\subset\{|p_j|<1\},\qquad
 \liminf_{j\to\infty}m_2\{|p_j|<1\}\ge\pi.
\]

更强地，利用单位根 Vandermonde 乘积，可精确计算这些互异零点的归一化离散能量。
记 \(M=(j-1)m,N=jm,r=e^{-j}\)，则
\[
\prod_{a<b}|z_a-z_b|
=M^{M/2}\,r^{m(m-1)/2}m^{m/2}(1-r^M)^m.
\]
所以归一化的非对角能量等于
\[
\frac{jm(m-1)-M\log M-m\log m-2m\log(1-e^{-jM})}{N(N-1)}
=\frac1j+o(1/j)\to0.
\]
因此弱收敛和近最优离散能量同时存在，仍不能控制阈值集合面积。

## 首断点和后续可行路线

首断点是正号裕量：在 \(\operatorname{cap}K=1\) 时，
\(U^{\nu_K}=0\) 遍及 \(\widehat K\) 的二维平台；\(L^2\)、能量或容量意义的小误差都
允许负号覆盖正面积。要推进一般情形，至少需以下之一：

1. 构造具有一侧势垒 \(U^{\nu_n}\ge-\varepsilon_n\) 且负集有定量小面积的根配置；
2. 把 \(C^2\) 域的根迁移/多项式近似做成对非正则边界稳定的定量定理；
3. 按零平台的面积和边界厚度分层，先覆盖 \(m_2(\widehat K)=0\) 之外的薄正面积类。

单纯继续优化 Fekete 能量不会跨过该断点。

## 闭合与发表级别

- 原题闭合：`NO`；一般 \(\operatorname{cap}=1\) 仍未解决。
- 本轮严格成果：Fekete lemniscate 的 hull-area 上界（零面积 hull 为推论）；
  能量/弱收敛路线的连续与有限多项式双重反例。新颖性尚未确立，只登记为
  `STRICT_PARTIAL`。
- SCI 二区判断：两项单独都更像论文中的方法论章节，不足以稳妥支撑一篇二区论文；
  若能扩展到正面积但薄边界的一大类，或给出非正则根迁移定理，才进入二区候选。
