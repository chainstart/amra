# Erdős #811：平衡六着色中彩虹 \(C_6\) 的谱充分条件

## 目标与矩阵分解

对 \(K_n\) 的平衡六边着色，令 \(A_i\) 为第 \(i\) 色邻接矩阵，
\(q=(n-1)/6\)。每个 \(A_i\) 都是 \(q\)-正则，且
\(\sum_iA_i=J-I\)。写

\[
 A_i=\frac qnJ+B_i.
\]

则 \(B_i\mathbf1=0\)，并令
\(\lambda_i=\|B_i\|_{\mathrm{op}}\)，即第 \(i\) 色所有非平凡特征值
绝对值的最大值。

## 彩虹闭游走下界

对每个颜色排列 \(\sigma\in S_6\)，

\[
\operatorname{tr}(A_{\sigma(1)}\cdots A_{\sigma(6)})
\]

计数依次使用这六种颜色的有根、有向闭六步游走。因为
\(JB_i=B_iJ=0\)，乘积没有混合项，故

\[
\operatorname{tr}(A_{\sigma(1)}\cdots A_{\sigma(6)})
=q^6+\operatorname{tr}
(B_{\sigma(1)}\cdots B_{\sigma(6)}).
\]

所有 \(B_i\) 在 \(\mathbf1^\perp\) 上作用，维数为 \(n-1\)，于是

\[
\left|\operatorname{tr}
(B_{\sigma(1)}\cdots B_{\sigma(6)})\right|
\le(n-1)\prod_{i=1}^6\lambda_i.
\]

令 \(T\) 为全部 720 个排列的总数，则

\[
 T\ge720\left(q^6-(n-1)\prod_i\lambda_i\right). \tag{1}
\]

颜色两两不同保证六条边也两两不同。不是简单 \(C_6\) 的闭游走在
\(v_0,\ldots,v_5\) 中还有一次顶点相等；选择一对相等位置至多 15 种，
其余至多 \(n^5\) 种。因此退化游走总数不超过 \(15n^5\)。由此得到可直接
使用的充分条件

\[
\boxed{
720\left(q^6-(n-1)\prod_i\lambda_i\right)>15n^5
}
\quad\Longrightarrow\quad
\text{存在彩虹 }C_6. \tag{2}
\]

特别地，若存在固定 \(\theta<1\) 使所有颜色满足

\[
\lambda_i\le
\theta\,\frac q{(n-1)^{1/6}},
\]

则 (2) 对充分大 \(n\) 成立。

## 含义与阻塞

这把 \(C_6\) 挑战严格缩小到具有大非平凡谱的颜色类：任何反例序列中，至少
一个颜色必须有

\[
\lambda_i\gtrsim q\,n^{-1/6}\asymp n^{5/6}.
\]

平衡性本身允许不连通的团并，从而允许 \(\lambda_i=q\)；所以谱条件不能从
原假设自动推出。下一步应对“大谱颜色”做逆结构分析，再与六个颜色的分解
\(\sum_iB_i=-I+J/n\) 联用。该充分条件是严格的路线推进，但属于短小的标准
谱估计，不足以单独支撑 Q2 论文；完整分类及无条件 \(C_6\) 仍开放。
