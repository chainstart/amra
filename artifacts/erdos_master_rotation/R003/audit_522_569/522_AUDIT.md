# Erdős #522：两版公开证明稿审计

## 结论摘要

- 官网于 2026-07-23 仍标 `OPEN`，评论区列有完整解声明；
- 2026-04-20 的无署名稿 `erdos522.pdf` 有一个致命的跨次数耦合缺口；
- 2026-04-27 署名 Przemek Chojecki 的 `erdos522-final.pdf` 改用同一
  \(P_n\) 的内外半径，确实避开该缺口；
- 对修订稿的量词、Borel--Cantelli 指数、小值控制、对数截断与
  Jensen 挤压逐项复算后，本轮未发现新的致命错误；
- 在独立第二审完成前，状态记为
  `CANDIDATE_COMPLETE_AFTER_PRIMARY_AUDIT`，暂不把中央台账直接改成
  已闭合。

## 旧稿的严格反证

旧稿 Proposition 7 先对前缀多项式
\[
 P_n(z)=\sum_{k=0}^n\epsilon_kz^k
\]
证明块内插值，再声称倒数多项式
\[
 Q_n(z)=\sum_{k=0}^n\epsilon_{n-k}z^k
\]
“对每个固定 \(n\) 与 \(P_n\) 同分布”，所以同样的跨 \(n\) 插值成立。
这个推理不成立：固定 \(n\) 的同分布不保持整个序列的耦合。

在 \(r=1\) 时，对任意 \(m>n\)，Parseval 给出
\[
\mathbb E\int\left|
 {Q_m(e^{i\theta})\over\sqrt{m+1}}-
 {Q_n(e^{i\theta})\over\sqrt{n+1}}
\right|^2\,d\mu=2.
\]
原因是相同 Fourier 位 \(k\) 上使用的是不同且独立的符号
\(\epsilon_{m-k}\) 与 \(\epsilon_{n-k}\)。它不可能满足旧稿所需的
\(O(N_j^{-1/6})\) 块内距离。故旧稿不能推出所有 \(n\) 的上界。

## 修订稿如何修复

修订稿不再对 \(Q_n\) 做块插值。它对同一个前缀过程 \(P_n\) 同时控制
\[
\rho_n=1-n^{-401/400},\quad 1,\quad
\tau_n=\rho_n^{-1}.
\]
三条半径序列的系数都保持同一前缀符号 \(\epsilon_k\)，所以
Lemma 2.2 的块比较合法。最后仅用恒等式
\[
Q_n(\rho_ne^{i\theta})
=\rho_n^ne^{in\theta}P_n(\tau_ne^{-i\theta})
\]
把倒数多项式的 Jensen 上界改写为已控制的外半径 \(P_n(\tau_nz)\)。

## 指数与量词复算

修订稿取
\[
\eta={1\over100},\quad\beta={1\over200},\quad N_j\asymp j^4.
\]

- 平滑可观测量：
  \(4(2\beta+6\eta-\tfrac12)=-1.72<-1\)，故端点偏差可求和；
- 小值集合：
  \(4(10\eta-\tfrac12)=-1.6<-1\)，故 Chebyshev 概率可求和；
- 块插值：
  \(\eta-\tfrac18=-0.115<-2\eta=-0.02\)；
- 截断误差：
  \(M^{-2}\log M=O(N_j^{-\beta})\)，因 \(2\eta>\beta\)；
- 去截断：
  \((\log n)^{10}M^{-1}=o(N_j^{-\beta})\)，因 \(\eta>\beta\)；
- 除以 \(-\log\rho_n\asymp n^{-401/400}\) 后，
  \(n^{-\beta}\) 正好变成 \(n^{399/400}\)。

Nazarov--Nishry--Sodin Corollary 1.2 适用于任意 \(\ell^2\)-归一化的
Rademacher Fourier 系数，包含 \(\rho_n,1,\tau_n\) 三组有限系数。
Jensen 内外挤压也精确处理闭圆盘边界零点。

## 剩余审计动作

需要一个未参与本报告的代理独立复核修订稿，重点重做 Lemma 2.2、
Proposition 3.3 的四维协方差估计和 Theorem 1.1 的外半径代换。通过后可
把 #522 登记为“公开署名证明稿、尚未同行评审/形式化”的数学闭合候选。
