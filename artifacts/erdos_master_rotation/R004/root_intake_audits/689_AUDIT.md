# Erdős #689：两项完整证明声称的核验边界

## 当前外部状态

官网讨论区截至 2026-07 仍把问题标为 `OPEN`。置顶说明确认已有
Chojecki 与 MalekZ 两项完整证明声称，但管理员因技术细节和 AI 辅助程度，
等待同行评审或 Sawhney、Tao 等专家的细审后才会改状态。

本轮取得并通读了 Chojecki 2026-04-27 的 10 页 working manuscript
《A greedy matching proof of Erdős's two-fold residue-class problem》。
它声称无条件完整证明，而不是条件结果。

## 证明链重放

文稿的逻辑链为：

1. 先取 \(a_2=1,a_3=0\)，并把一个固定有限素数集 \(S\) 切换到非零类；
2. 除 \(o(n/\log n)\) 例外外，剩余 demand 恰为
   \(2^kuq\)，且总量 \((1+o(1))n/\log n\)；
3. 在 \(P>\tau n\) 中选“robust”素数，要求每个旧倍数 \(jP\) 已被
   \(S\) 至少命中两次；通过独立 Bernoulli 和
   \(\sum_{p}1/p=\infty\)，其固定模密度 \(\delta_S\to1\)；
4. 用三素数线性系统 \(q,q',bq'-aq\) 构造三部超图，Green–Tao
   给边数 \(\gg\delta_S\lambda n^2/\log^3n\)；
5. Selberg 二形式上界与系数求和局部因子给
   \(\Delta\ll n/\log^2n\)，贪心匹配因而配对
   \(\gg\delta_S\lambda n/\log n\) 个 demand；
6. 参数满足
   \(\delta_S(1-\tau)+\eta\delta_S\lambda>1\)，剩余 robust 素数逐个
   修补未配对 token。

终局计数

\[
(R-|M|)-(D-2|M|)=R+|M|-D>0
\]

是正确的；切换 robust 素数也确实不会让其旧倍数跌到两次覆盖以下。

## 本轮独立有限核验

对文稿 Lemma 5.1 的 switched-prime kernel 作了逐剩余类枚举，确认

\[
s-2-\frac2s\le K_s(\delta)\le s-2-\frac1s
\]

以及两个归一化上界。也独立复算了 residual-demand 的局部恒等式

\[
\frac{s-2}{s-1}+\sum_{e\ge1}s^{-e}=1.
\]

这些检查支持局部常数不随有限集合 \(S\) 坍缩的核心设计。

## 仍未解除的证明债务

本轮没有找到一个可明确写成反例的错误，但也不能据此宣布闭合。最需要专家
逐行核验的是：

- Lemma 5.3 中把随系数变化的 Selberg singular products 求和后，是否
  真的可以完全按 \(s\in S\) 分解且保持绝对常数；
- Proposition 6.1 对所有有限系数组合求和时，Green–Tao 的误差、固定模
  剩余类和 archimedean 权重是否全部一致；
- MalekZ 新版自己仍把 weighted GTZ moments 与 Kahn rounding 的接口列为
  待核点，尚无同行评审结论可用来交叉封口。

因此台账状态应为
`OPEN_WITH_TWO_FULL_PROOF_CLAIMS; NO_COUNTEREXAMPLE_FOUND_IN_FIRST_PASS`，
而不是 `VERIFIED_CLOSED`。若要改状态，下一轮应由独立解析数论专家对上述
两个 analytic interfaces 作逐公式审计，或等待正式发表。
