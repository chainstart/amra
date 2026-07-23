# Erdős #141 — R002准入研究

日期：2026-07-23

终态：`CORRECTED_CONDITIONAL_REDUCTION__PARITY_BARRIER__DO_NOT_PROMOTE`

## 当前状态

官网仍标为开放；存在性只验证到 \(k\le10\)，即使 \(k=3\) 是否出现无穷多次
也未知。Green–Tao定理不排除等差数列各项之间还有别的素数。

## 修正后的条件构造

令

\[
d=\prod_{p\le k}p,\qquad
B=\{1\le r<(k-1)d:d\nmid r\}.
\]

对每个 \(r\in B\) 选互异素数 \(q_r>(k-1)d\)。用CRT选 \(b\) 满足

\[
b\equiv1\pmod p\quad(p\le k),\qquad
b\equiv-r\pmod {q_r},
\]

并令

\[
M=d\prod_{r\in B}q_r,\qquad
L_j(t)=Mt+b+jd,\quad0\le j<k.
\]

则每个非AP位置 \(Mt+b+r\) 被 \(q_r\) 整除，对充分大 \(t\) 为合数。
同时线性型系统admissible：

- \(p\le k\) 时 \(p\mid M,d\)，且所有 \(L_j(t)\equiv1\pmod p\)；
- \(p=q_r\) 时，\(|jd-r|<(k-1)d<q_r\) 且 \(jd\ne r\)；
- 其余 \(p>k\) 最多排除 \(k<p\) 个参数剩余类。

因此Schinzel Hypothesis H/Dickson猜想会给无穷多个连续素数AP。

## 对公开论坛版本的核验

2026-02-08论坛贴出的同一路线把
\(M\) 写成仅 \(\prod q_r\)，随后却把 \(Mn\) 在 \(p\le k\) 下当成0。
这一步不成立，论坛紧随其后的评论也指出了问题。把小素数乘积 \(d\) 纳入
\(M\)，并同时规定 \(b\equiv1\pmod p\)，可修复条件定理。

`verify_141_crt_cover.py`对 \(k=3,4\) 构造实际CRT剩余类，逐一核对所有间隙
覆盖、固定模数非零，以及到500的全部素数局部admissibility。

## 准入结论

修补只得到已知的条件结论，最后一步仍是一般素数 \(k\)-元组猜想。有限搜索、
奇异级数计算或更换覆盖模数都不能越过筛法的parity barrier。因此闭合距离
调为5，不进入深攻；只有出现能让全部 \(k\) 个线性型同时取素数的新输入时
才重开。

## 来源

- https://www.erdosproblems.com/141
- https://www.erdosproblems.com/forum/thread/141
- Schinzel–Sierpiński, *Sur certaines hypothèses concernant les nombres premiers*
