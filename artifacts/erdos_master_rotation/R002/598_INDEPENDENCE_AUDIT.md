# Erdős #598 — R002独立性候选核验

日期：2026-07-23

终态：`RELATIVE_INDEPENDENCE_CANDIDATE__PRIMARY_TRANSFER_AUDIT_REQUIRED`

## 分割关系重述

令 \(\kappa=\mathfrak c^+\)。原题问是否对每个无限基数 \(\lambda\) 都有

\[
\lambda\nrightarrow[\kappa]^\omega_\kappa,
\]

即存在 \(c:[\lambda]^\omega\to\kappa\)，使每个
\(X\in[\lambda]^\kappa\) 都看到全部 \(\kappa\) 种颜色。

\(\lambda<\kappa\) 时要求真空；\(\lambda=\kappa\) 的ZFC正构造可由
\(E^\kappa_\omega\) 的平稳集分割得到。真正问题是所有 \(\lambda>\kappa\)。

## 反方向的一条严格传递链

Garti–Hayut的已发表论文证明：

1. I1嵌入产生Magidor基数 \(\lambda\)；
2. Proposition 1.10给出一个forcing extension，使 \(\lambda\) 仍为Magidor，
   且第一个正分割基数 \(\alpha_M=\aleph_2\)；
3. 其证明同时使用 \(\alpha_M>2^{\aleph_0}\)，故该模型中
   \(\mathfrak c=\aleph_1\)，于是 \(\kappa=\mathfrak c^+=\aleph_2\)。

所以模型中

\[
\lambda\rightarrow[\lambda]^{\omega\text{-bd}}_\kappa.
\]

给定任意 \(c:[\lambda]^\omega\to\kappa\)，限制到有界可数集，得到
\(A\in[\lambda]^\lambda\) 及一个在 \([A]^{\omega\text{-bd}}\) 上缺失的颜色。
取某个 \(\beta<\lambda\) 使 \(|A\cap\beta|\ge\kappa\)，再取
\(X\in[A\cap\beta]^\kappa\)。则 \([X]^\omega\) 全部有界，故同一颜色仍缺失：

\[
\lambda\rightarrow[\kappa]^\omega_\kappa.
\]

这在该模型中否定原题的全称断言。

## 另一方向尚需核验

2026-05的MathOverflow讨论给出如下路线：

- 若某个 \(\lambda\rightarrow[\kappa]^\omega_\kappa\)，则推出相应有限指数
  分割关系；
- 把它转写为带一元谓词结构的适当初等子模型；
- 对 \(L_\lambda\) 做传递坍缩，得到非平凡初等嵌入，从而推出 \(0^\sharp\)
  存在；
- 因此在 \(V=L\) 中所有所需负分割关系成立。

这会与上面的I1相对一致性模型合起来证明原题相对大基数独立。但本轮尚未把
“可数指数推出有限指数”以及初等子模型等价逐条对照Jech/Kanamori原定理，
所以不能把独立性记成已闭合。

## 结论

#598不应继续沿普通组合构造深攻；它应转入resolution audit，闭合距离降为1，
目标是核完 \(V=L\) 方向和“大小为 \(\kappa\)”而非“序型为 \(\kappa\)”
的定义一致性。当前结果是强独立性候选，不是已发表的#598专门证明。

## 来源

- https://www.erdosproblems.com/598
- https://mathoverflow.net/questions/511508/on-erd%C5%91s-problem-598
- https://doi.org/10.2969/jmsj/07017327
