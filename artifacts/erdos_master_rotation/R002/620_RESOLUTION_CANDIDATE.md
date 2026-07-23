# Erdős #620 — R002新预印本闭合核验

日期：2026-07-23

终态：`EXACT_PREPRINT_RESOLUTION_CANDIDATE__INDEPENDENT_QA_REQUIRED`

## 状态变化

官网在本轮访问时仍标为开放，并记录

\[
\sqrt n\,\frac{\sqrt{\log n}}{\log\log n}\ll f(n)
\ll\sqrt n\log n.
\]

但Morris、Sahasrabudhe、Verstraëte于2026-07-17提交预印本
`arXiv:2607.16118v1`，其Theorem 1.1声称对每个固定 \(s\ge2\)

\[
f_{s,s+1}(n)=\Theta(\sqrt{n\log n}).
\]

取 \(s=3\) 后，宿主图无 \(K_4\)，所求子集无 \(K_3\)，逐字等于#620。
因此若论文正确，原题的数量级已经完整闭合。

## 下界核验

Joret–Micek–Reed–Smid已经发表的定理给每个 \(n\) 点图一个

\[
O\!\left(\sqrt{\frac n{\log n}}\right)
\]

色的clique colouring，其中任何非孤立的极大团都不是单色。
在 \(K_{s+1}\)-free 图中，每个 \(K_s\) 都是极大团，所以每个颜色类都
\(K_s\)-free；最大颜色类大小为
\(\Omega(\sqrt{n\log n})\)。该量词转换是完整的。

这也解释了旧下界记录的异常：Shearer本身已给
\(\Omega(\sqrt{n\log n/\log\log n})\)，新预印本明确如此记载。

## 上界结构核验

本轮下载并检查了22页固定版本PDF：

- SHA-256：
  `b2e140d9831b53fb1140735039fd1a02c60c93ec59c0ac5938ae95b4b25835a2`；
- Theorem 3.1明确构造 \(n\) 点 \(K_{s+1}\)-free 图，使每个
  \(C s^3\sqrt{n\log n}\) 点集含 \(K_s\)；
- Lemma 2.3逐字验证删除步骤后的图无 \(K_{s+1}\)；
- Lemma 3.4控制投影大的集合仍无 \(K_s\) 的概率；
- Lemma 3.5统一控制所有 \(k\)-集中的closed edges；
- 最终并集界使用 \(m=16k\log n\)，量级足以覆盖全部集合。

没有发现“非诱导子图”“仅无限子序列”“\(s\) 随 \(n\) 变化”或常数不统一
等题面错配。尚未完成的是对Lemma 3.4、3.5全部概率估计的第二人逐行QA。

## 结论

#620应立即从原创证明池转入已有解核验，闭合距离降为1。当前证据级别是
“五天前的完整预印本候选”，不是已发表论文，也尚未获官网状态更新；在独立
QA完成前不把 `original_problem_closed` 写为真。

## 来源

- https://www.erdosproblems.com/620
- https://arxiv.org/abs/2607.16118
- https://doi.org/10.37236/9659
