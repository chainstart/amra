# Erdős #1002：精确 Farey 实验、二阶矩障碍与 Ostrowski 断点

## 状态、题面与来源范围

官网在 2026-07-23 仍标 `OPEN`。Erdős 1964 年原题固定起点
\(\beta=0\)，令
\[
 S_n(\alpha)=\sum_{k=1}^n\left(\frac12-\{k\alpha\}\right),
 \qquad F_n=S_n/\log n,
\]
并问 \(\alpha\in(0,1)\) 的推前分布是否对每个实数阈值收敛。

Kesten 的 Cauchy 极限定理同时平均 \((\alpha,\beta)\)，不能把
\(\beta\) 直接固定为 0。Frühwirth--Hauke 2024 及
Dolgopyat--Sarig 研究的是时间平均（随机 \(n\)）或 quenched/annealed
时间极限；它们解释了连分数机制，但没有回答本题的“固定 \(n\)、只平均
\(\alpha\)”版本。

## Closing lemmas

原队列提出的第一层目标可精确写成统一弱 \(L^1\) 界：
\[
 \mu\{|S_n|>A\log n\}\le \frac{C}{A}
 \quad(n\ge2,\ A\ge1). \tag{T}
\]
它会给 \(\{F_n\}\) 的紧性和子序列弱极限，但**尚不闭合原题**。完整闭合
还需第二层唯一性 lemma：所有子序列极限相同（最好识别特征函数），且极限
无原子，从而把收敛提升到题目要求的每个 \(c\)。

## 精确 Farey 分段证书

在相邻 Farey 分数（分母至多 \(n\)）之间，
\[
 S_n(\alpha)=C-\frac{n(n+1)}2\alpha
\]
是同斜率线性函数；跨过既约分数 \(p/q\) 时向上跳
\(\lfloor n/q\rfloor\)。因此无需浮点逐项求和，就能对每个 cell 精确
积分。本地脚本以有理数累计均值和二阶矩，只在报告尾概率和绝对一阶矩时
转成浮点。

结果如下：

| \(n\) | Farey cells | \(\int|S_n|\) | \(\int|S_n|/\log n\) |
|---:|---:|---:|---:|
| 64 | 1260 | 1.7191609544 | 0.4133708306 |
| 128 | 5022 | 2.1047183194 | 0.4337809546 |
| 256 | 19948 | 2.5395639812 | 0.4579770452 |

在 \(n=256\) 时，\(A\mu(|S_n|>A\log n)\) 对
\(A=1,2,4,8,16\) 分别约为
\[
 0.08305,\ 0.06986,\ 0.05388,\ 0.05023,\ 0.03821.
\]
它与 (T) 相容，但有限数据不证明统一尾界。完整输出见
`1002_farey_certificate.json`，复算脚本为 `verify_1002_farey.py`。

## 一个严格障碍：二阶矩路线必然失效

令 \(\psi(x)=1/2-\{x\}\)（忽略零测集上的端点）。Fourier 正交给出
\[
 \int_0^1\psi(k\alpha)\psi(\ell\alpha)\,d\alpha
 =\frac{\gcd(k,\ell)^2}{12k\ell}.
\]
故
\[
 \int_0^1 S_n(\alpha)^2\,d\alpha
 =\frac1{12}\sum_{k,\ell\le n}
   \frac{\gcd(k,\ell)^2}{k\ell}\ge\frac n{12}.
\]
脚本对 \(n=64,128,256\) 用 Farey cell 积分与 gcd 公式作了完全相等
核对。于是
\(\mathbb E(F_n^2)\ge n/(12\log^2n)\to\infty\)；Chebyshev/统一
\(L^2\) 不能证明紧性。这不反驳 Cauchy 型弱极限，因为后者本来就没有
有限二阶矩，但它严格排除了一条常见路线。

## Ostrowski--Denjoy--Koksma 的首个断点

Denjoy--Koksma 对每个完整收敛分母块给 \(O(1)\)，但把 \(n\) 作
Ostrowski 展开后，取绝对值只得到由连分数数字之和控制的界。现有一手
文献记载，对几乎处处的 \(\alpha\)，前 \(K\) 个数字满足
\[
 \sum_{j\le K}a_j-\max_{j\le K}a_j
 \sim \frac{K\log K}{\log2},
 \qquad K\asymp\log n.
\]
因此朴素绝对值累加的尺度是 \(\log n\log\log n\)，比 (T) 所需多一个
\(\log\log n\)。必须利用块的符号抵消，并单独处理
\(a_j\asymp\log n\) 的稀有大数字。

官网评论中的启发式递推还有一个可修正的局部符号错误：当
\((p,q)=1\) 时，
\[
 \sum_{k=1}^{q}\left(\frac12-\{pk/q\}\right)=+\frac12,
\]
不是 \(-1/2\)。修正符号并不会消除上述重尾/抵消断点。

## 晋级与发表判断

判定为 `RETAIN_WITH_REFINED_TARGET__NO_CORE_PROMOTION`。精确 Farey
积分器、二阶矩恒等式核验和路线断点有研究辅助价值，但都没有证明新的
渐近界。没有 SCI 二区级结果。下一轮若继续，应直接瞄准弱 \(L^1\)
估计或大 Ostrowski 数字的符号配对，而不是再做普通二阶矩或逐块绝对值
估计。

**Claim guard：** 尾界的小规模证据不等于尾界证明；紧性即使成立也不等于极限唯一。
