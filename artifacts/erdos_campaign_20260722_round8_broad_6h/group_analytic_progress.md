# 第八轮解析/素数组终报：#143、#377、#679、#950

日期：2026-07-22（Asia/Hong_Kong）

统一起点：2026-07-22 08:52:14+08:00  
预算终点：2026-07-22 10:22:14+08:00  
实际冻结：2026-07-22 10:22:57+08:00（边界后仅执行冻结与终态登记）  
登记预算：5,400 秒  
有限核验：单逻辑核，未超过工作流 CPU 限制

## 总结论

四道原题均未闭合，也均未达到本轮 SCI 二区候选主定理的提前冻结门槛。
本组最重要的新进展在 #679：

1. 对“首个刚超过区间长度的素数前缀模数”，约化导体截断严格修复了
   round 7 留下的不完整周期接口；
2. 更换成大移位带与非鞍点小倾斜后，完整周期好类密度可严格压到
   \(X^{-C+o(1)}\)，任意固定 \(C>1\) 均可；
3. 这意味着零频已不再是绝对障碍。若能证明相应区间均值转移，便会否定
   #679 第一问；
4. 标准 dyadic-conductor/Farey large sieve 加 Cauchy 在全导体层严格失效；
   精确 ANOVA 重组又证明实际全导体层极小，所以这是方法损失而非反例；
5. 当前最窄缺口是高导体 ANOVA 层的单侧有符号组合尾；固定的 \(C-1\) 指数余量
   允许 \(X^{o(1)}\) 损失，不必先证明完整渐近式。

这是一条明显更聚焦的证明路径，但关键区间转移尚未证明，因此不得表述为候选
完整证明或 Q2 成果。

## #143

### 旧路线尸检

- round 7 的极值素数支撑截断正确；
- 触发信息单独只能给出最优指数 \(e\)，继续只优化支撑属于已证方法屏障；
- 素数 charge 中 \(1/p\) 的抵消只否定朴素 Tonelli 汇总，不否定局部引理；
- KLL 的有限事件论证给出谐和和 \(o(\log X)\)，不自动推出加权级数收敛。

### 新方向

在同一有理纤维写

\[
 \alpha=\gamma a/q,\qquad\beta=\gamma b/r,
 \qquad(a,q)=(b,r)=1.
\]

严格证明

\[
 \gcd(ar,bq)=\gcd(a,b)\gcd(q,r),
\]

从而

\[
 [\alpha,\beta]
 ={\operatorname{lcm}(q,r)\over\gamma\gcd(a,b)}.
\]

这把 surviving \(E_3\) pair 直接变成分子 GCD 与分母 lcm 耦合的 incidence
问题。另证明了 dyadic 分子区间中

\[
 \#\{(a,b):\gcd(a,b)\ge D\}
 \ll AB/D+(A+B)\log(2\min(A,B))+\min(A,B).
\]

### 失败边界

把该计数直接对分母求和时，lcm 节省变成 \(\gcd(q,r)\) 因子；仍缺一个保留
分母阈值的 primitive-fibre Carleson/GCD-graph 不等式，以及独立的加权闭合
桥。结论：严格局部推进，原题开放。

## #377

### 旧路线尸检

- round 7 的短重叠账本正确；
- 普通二阶导数两项估计在 surviving range 中出现增长项，确为该捷径的已证
  屏障；
- 更早的 Brun--Titchmarsh 区间长度替换是真错误；
- uniform \(O(j^{-2})\) digit-layer 界被固定小素数构造严格否定。

### 新方向

令

\[
 P_n=\prod_{p\le n}p,\qquad
 R_n=\operatorname{rad}\gcd\!\left(\binom{2n}{n},P_n\right).
\]

Euler product 严格给出

\[
 \sum_{\substack{p\le n\\p\nmid\binom{2n}{n}}}{1\over p}
 =
 \log{P_n/\varphi(P_n)\over R_n/\varphi(R_n)}+O(1).
\]

由 Mertens，原题等价于

\[
 {R_n\over\varphi(R_n)}\gg\log n.
\]

同时把 Kummer 条件严格改写为所有素数幂前缀

\[
 n\bmod p^a\le(p^a-1)/2.
\]

### 失败边界

中央二项式系数或其 radical 的大小本身不能迫使小素数 Euler factors 出现；
仍缺针对 distinct small-prime support 的加权下界筛。结论：精确等价接口，
原题开放。

## #679

### 旧路线尸检

round 7 的 CRT Fourier factorisation、Parseval、Bernoulli conductor ledger
均正确；raw \(L^2\) 把所有非零频率混在一起后暴露完整 \(Q/N\)，确实失效，
但不构成对 phase-sensitive conductor splitting 的屏障。

### 定理 A：首个超周期模数的区间转移

令 \(Q=\prod_{H<p\le z}p\) 是首个满足 \(Q>N\) 的素数前缀，
\(N\asymp X\)、\(H=(\log X)^{o(1)}\)、\(t\ge1/2\)。则

\[
 Q/N\ll\log X
\]

且对任意平移的 \(N\) 点区间

\[
 \sum_IW=N\mu(1+o(1)).
\]

证明把 Fourier 能量按 reduced conductor \(C(h)\) 分层。对固定
\(0<\theta<1\)，

\[
 \mathbb P_2(C>X^\eta)\le X^{-\theta\eta+o(1)}.
\]

低导体利用完整短周期 Parseval，高导体能量尾吸收 \(Q/N\)。取
\(\eta=1/2,\theta=3/4\) 得相对误差

\[
 O(X^{-1/4+o(1)}+X^{-3/16+o(1)}).
\]

逐式内部 QA 已复核 \(Q/N\)、Fourier 归一化、任意平移端点及概率测度，结论
PASS_INTERNAL_STRICT_PARTIAL。

### 定理 B：大带小倾斜零频

写 \(L_i=\log_iX\)，取

\[
 H=(L_1/L_2)^2,\qquad z=X^{1/L_2},
\qquad1-t={C\over\sqrt H}
\]

其中固定 \(C>1\)。Mertens 给出

\[
 \sum_{H<p\le z}{1\over p}
 =L_2-2L_3-\log2+o(1).
\]

对全部 \(H\) 个连续移位的必要条件，完整周期好类密度满足

\[
 \delta\le X^{-C+o(1)}.
\]

常数与量词 QA 显示：若相应 \(X\)-长区间满足
\(\sum_IW=(1+o(1))X\mu\)，则候选数为
\(X^{1-C+o(1)}<1\)，从而对每个固定 \(\varepsilon,K\) 最终没有候选。

同时

\[
 \log(M_2/\mu^2)=O_C(L_2),\qquad
 \mathbb E_2\log C(h)=O_C(L_1/L_2),
\]

即 Fourier 能量的典型约化导体仅 \(X^{o(1)}\)。

### Farey 尝试、ANOVA 重组与精确失败边界

对 \(C<c\le2C\) 的 reduced fractions，large sieve 给

\[
 \sum |G_N(u/c)|^2\ll(N+C^2)N.
\]

典型导体块可由此和完整周期消去压到 \(X^{-1+o(1)}\)。但是全导体层
\(c=Q\) 在 energy-only Cauchy 中含

\[
 \sqrt{QP_Q/N},\qquad P_Q=\prod_{p\mid Q}\beta_p.
\]

小倾斜常数为 \(C_0>1\) 时

\[
 \log(QP_Q)
 =(2\log C_0+o(1))\pi(z)>0.
\]

因此只知道 conductor energy tail 不足。但令 \(F_S\) 为约化导体恰由素数集
\(S\) 组成的 Fourier 层，局部 Fourier 反演严格给出

\[
 F_S(n)=\prod_{p\notin S}m_p
        \prod_{p\in S}\{W_p(n)-m_p\}.
\]

由于 \(|W_p(n)-m_p|<a\)，实际全导体层满足

\[
 \left|\sum_{n\in I}F_{\cal P}(n)\right|\le Na^{|\cal P|},
\]

极其微小。这证明上面的 Cauchy 爆炸只是方法损失，而非区间转移失败的证据。

进一步的 cutoff 审计显示：对任意固定 \(\kappa<2/3\)，全部
\(c(S)\le X^\kappa\) 的层可由完整周期估计控制（这包括所有
\(|S|\le\kappa L_2\) 的层）；
但绝对高阶尾

\[
 \sum_{r>\kappa L_2}\binom Mr a^r
\]

因 \(aM\) 极大而失效；即使只取 \((z/2,z]\) 中
\(r=(\kappa+\delta)L_2\) 个素数，所得导体已超过 \(X^\kappa\)，相应绝对组合界
仍达 \(X^{\kappa+\delta+o(1)}\)。Bonferroni 截断则需阶数
\(\asymp\log X\)，对应模数远超区间长度。因此缺口不是零频、典型导体或单独的全导体层，而是下面这个
明确的有符号组合尾估计。若要求完整区间渐近式，一个干净的充分目标是

\[
 \left|\sum_{n\in I}
 \sum_{c(S)>X^\kappa}F_S(n)\right|=o(N\mu).             \tag{*}
\]

本轮未证明 \((*)\)。

不过，否定 #679 第一问并不需要这么强。由于 \(C>1\) 有固定指数余量，只需
较弱的单侧界

\[
 \sum_{n\in I}\sum_{c(S)>X^\kappa}F_S(n)
 \le N\mu X^{o(1)}                                      \tag{**}
\]

便可结合低阶层得到 \(\sum_IW\le N\mu X^{o(1)}\)，继而把候选数压到
\(X^{1-C+o(1)}<1\)。这比先证明渐近式更准确地刻画了闭合原题所需的最弱当前
目标；本轮同样未证明 \((**)\)。

### 严格结论

#679 第一问仍开放。当前最窄下一目标是证明定理 B 权的高导体单侧有符号尾
\((**)\)；现有 dyadic/Farey energy-only 方法不能完成它。
定理 A 与定理 B 均未做外部
独立同行 QA，也未完成文献优先权认证。

## #950

### 旧路线尸检

round 7 的

\[
 \limsup f(n)\ge6931/3705
\]

继续通过数学审计；没有发现其定量交集或极限次序的破绽。

### 新方向和 no-go

令 \(A_n(D)=\#\{p<n:n-p\le D\}\)。严格 Abel 恒等式为

\[
 f(n)={A_n(n-2)\over n-2}
 +\sum_{D=1}^{n-3}{A_n(D)\over D(D+1)}.
\]

等价地，若 \(C_j(n)\) 计数后向 dyadic denominator shell，则

\[
 f(n)\asymp\sum_j{C_j(n)\over2^j}.
\]

另一方面，若一个 prime-tuple 定理只保证 \(k\) 个坐标中至少 \(m+1\) 个为
素数，而不控制坐标，则其 worst-case reciprocal yield 至多

\[
 {m\over k-1}\log(H+1).
\]

当 \(H=O(k\log k)\)、\(m\asymp\log k\) 时该量趋于零。因此 count-only
Maynard 输出不能推出 limsup 无界；必须得到坐标加权或增长的多尺度相关输入。
结论：严格结构归约与方法 no-go，原题开放。

## 核验与文献边界

四个有限核验脚本均在单核运行并通过：

- #143：307,470 个有向有理纤维组合；
- #377：696,607 个 digit/prefix 检查；
- #679：完整 DFT、8 个 ANOVA/约化导体层、导体能量分层及平移区间
  Fourier inversion；
- #950：\(3\le n\le5000\) 的 Abel/dyadic 恒等式及 15 个 tuple no-go 检查。

定向检索只发现一般 weighted-large-sieve/Parseval 文献，例如 Olivier Ramaré
的 2026 预印本
[*The weighted large sieve through Parseval*](https://arxiv.org/abs/2605.29470)；
未发现直接陈述 #679 本轮两个专用定理的来源。该检索不是
穷尽式查重，因此本报告只称其为 campaign-new，不认证论文新颖性或优先权。

最终分级：

- 原题闭合：0；
- 候选完整证明：0；
- Q2 门槛：未达；
- 最值得下一轮集中：#679 大带小倾斜的相位敏感区间转移。

终态：**FROZEN_AT_BUDGET_BOUNDARY**。边界后未开展新证明，仅写入终态、
校验和与账本。
