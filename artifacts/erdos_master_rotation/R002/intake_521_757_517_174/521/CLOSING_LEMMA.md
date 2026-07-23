# #521 条件闭合证书

设 \(Z_n=N_{g_n}((-1,1))\)，其中
\(g_n(x)=x^nf_n(1/x)\)。

假设对每个有理数 \(\eta>0\)，

\[
\sum_j\Pr\left(\max_{2^j\le n<2^{j+1}}
|Z_n-Z_{2^j}|>\eta j\right)<\infty. \tag{M}
\]

则原题成立，证明如下。

1. 固定 \(j\) 时，\(g_{2^j}\) 与普通 Kac 多项式 \(f_{2^j}\) 同分布。
2. Can--Nguyen 的下尾为 \(O(n^{-c})\)，全根数上尾为
   \(O(\exp(-c\sqrt{\log n}))\)。在 \(n=2^j\) 上，两者分别为
   \(O(e^{-c'j})\) 与 \(O(e^{-c'\sqrt j})\)，均可求和。
3. 结合根数期望渐近式和 Borel--Cantelli，
   \(Z_{2^j}/(j\log2)\to1/\pi\) 几乎处处。
4. 对每个有理 \(\eta>0\)，再次由 (M) 和 Borel--Cantelli，几乎处处从某个
   \(j\) 起，整个 dyadic 块内
   \(|Z_n-Z_{2^j}|\le\eta j\)。
5. 先令 \(j\to\infty\)，再令有理 \(\eta\downarrow0\)，得到
   \(Z_n/\log n\to1/\pi\)。
6. 倒数变换把 \(Z_n\) 与 \(f_n\) 在 \(|x|>1\) 的根数对应。端点
   \(x=\pm1\) 总贡献至多2，不影响 \(\log n\) 归一化。
7. 与 Do 已证明的 \([-1,1]\) 内根强律相加，得到
   \(R_n/\log n\to2/\pi\) 几乎处处。

本文件证明的是条件蕴含，不声称 (M) 已证。

