# \(B_4\) 统一非负性：逐系数正递推证明

日期：2026-07-29

## 1. 定理

令

\[
\lambda=1+s\beta,\qquad
m=2s-10,
\]

并定义

\[
\begin{aligned}
K^{(3)}_s={}&
1+12\beta+(6s+30)\beta^2+28s\beta^3+6s^2\beta^4,\\
K^{(4)}_s={}&
1+28\beta+(14s+288)\beta^2+(292s+1264)\beta^3\\
&+(75s^2+1918s+2008)\beta^4
+(968s^2+4064s)\beta^5\\
&+(160s^3+3072s^2)\beta^6
+1024s^3\beta^7+128s^4\beta^8.
\end{aligned}
\]

四页分区转移严格给出

\[
B_4
=24\beta^4\lambda^{2s-12}L_s(\beta),
\]

其中

\[
\boxed{
L_s(\beta)
=(1+4\beta)^mK^{(4)}_s
-2\lambda^2(1+3\beta)^{m+2}K^{(3)}_s
+\lambda^4(1+2\beta)^{m+4}.
}
\]

边界值为

\[
B_4|_{s=4}=0,\qquad
B_4|_{s=5}=288\beta^8(75\beta^2+40\beta+7).
\]

本节证明如下更强结论。

> **定理。** 对每个整数 \(s\ge5\)，\(L_s(\beta)\) 的全部系数非负，
> 且其非零支撑恰为 \(4,\ldots,2s-2\)。因此对
> \(\beta\ge0\)，有 \(B_4\ge0\)。

证明不依赖有限参数扫描，而是使用一个对所有 \(s\) 成立的逐系数正递推。

## 2. 几何平均/平方下界为何失败

写

\[
\begin{aligned}
A&=(1+4\beta)^mK^{(4)}_s,\\
B&=\lambda^2(1+3\beta)^{m+2}K^{(3)}_s,\\
C&=\lambda^4(1+2\beta)^{m+4}.
\end{aligned}
\]

则 \(L_s=A-2B+C\)。最直接的充分条件是

\[
AC\ge B^2,
\]

因为它会给出

\[
A+C\ge2\sqrt{AC}\ge2B.
\]

但这个加强命题为假。约去共同正因子后，它要求

\[
(1+4\beta)^m(1+2\beta)^{m+4}K^{(4)}_s
\ge
(1+3\beta)^{2m+4}(K^{(3)}_s)^2.
\]

在最小参数 \(s=5\) 时，左边减右边的
\(\beta^4\) 系数精确等于

\[
-60.
\]

数值上该差在正 \(\beta\) 也可为负。因此不能通过 AM--GM、平方下界或
对数凸性 \(AC\ge B^2\) 完成证明。需要直接证明较弱的算术中点不等式
\(A+C\ge2B\)。

## 3. 每个系数的显式三项公式

写

\[
K_s^{(4)}=\sum_{r=0}^8a_r(s)\beta^r,\qquad
K_s^{(3)}=\sum_{r=0}^4c_r(s)\beta^r.
\]

采用约定

\[
\binom Nk=0\quad\text{若 }k<0\text{ 或 }k>N.
\]

则对任意整数 \(d\)，方框中多项式的系数是

\[
\boxed{
\begin{aligned}
\ell_{s,d}:=[\beta^d]L_s
={}&
\sum_{r=0}^8
a_r(s)\,4^{d-r}\binom m{d-r}\\
&-2\sum_{q=0}^2\binom2q s^q
\sum_{r=0}^4
c_r(s)\,3^{d-q-r}\binom{m+2}{d-q-r}\\
&+\sum_{q=0}^4
\binom4q s^q\,2^{d-q}\binom{m+4}{d-q}.
\end{aligned}}
\]

其中所有越界指数项按零处理。该式已由
`verify_b4_uniform_positivity.py` 与独立整数卷积逐项核对。

它立即给出

\[
\ell_{s,0}=\ell_{s,1}=\ell_{s,2}=\ell_{s,3}=0
\]

以及首个非零系数

\[
\ell_{s,4}
=(s-4)(s^3+6s^2-10s-141)>0
\qquad(s\ge5).
\]

多项式的非零范围是

\[
4\le d\le2s-2.
\]

下一节证明这个系数命题。

## 4. 对 \(s\) 的逐系数正递推

为缩短公式，记

\[
u_j=1+j\beta,\qquad \lambda_s=1+s\beta,\qquad
m=2s-10,\qquad z=u_2.
\]

定义

\[
\begin{aligned}
D_s&=K^{(4)}_{s+1}-K^{(4)}_s,\\
H_s&=u_4^2\lambda_s^2K^{(3)}_s
    -u_3^2\lambda_{s+1}^2K^{(3)}_{s+1},\\
E_s&=u_2^2\lambda_{s+1}^4-u_4^2\lambda_s^4.
\end{aligned}
\]

从 \(L_s\) 的闭式直接相减，得到恒等式

\[
\begin{aligned}
R_s
&:=L_{s+1}-u_4^2L_s\\
&=u_4^{m+2}D_s+2u_3^{m+2}H_s+u_2^{m+4}E_s.
\end{aligned}
\tag{1}
\]

利用 \(u_4=z+2\beta\)、\(u_3=z+\beta\)，并记

\[
Q_s=D_s+2H_s,\qquad
A_{s,r}=2^rD_s+2H_s=Q_s+(2^r-1)D_s,
\]

式 (1) 的二项式展开可写成

\[
\boxed{
R_s=z^m I_s+
\sum_{r=3}^{m+2}\binom{m+2}{r}
\beta^r z^{m+2-r}A_{s,r},
}
\tag{2}
\]

其中初始三层 \(r=0,1,2\) 被合并为

\[
\begin{aligned}
I_s={}&z^2(Q_s+z^2E_s)
 +(m+2)\beta z(2D_s+2H_s)\\
&+\binom{m+2}{2}\beta^2(4D_s+2H_s).
\end{aligned}
\tag{3}
\]

这一步正是证明的关键：单独的 \(E_s\) 有负系数，但与前两个二项式层
合并后负项完全消失。

令 \(n=s-5\ge0\)。直接代入 \(K_s^{(3)},K_s^{(4)}\) 并整理，得到

\[
D_s=\beta^2\sum_{j=0}^6d_j(n)\beta^j,\qquad
Q_s=\beta^2\sum_{j=0}^6q_j(n)\beta^j,\qquad
I_s=2\beta^4\sum_{j=0}^6i_j(n)\beta^j,
\]

其中

\[
\begin{array}{c|l|l}
j&d_j(n)&q_j(n)\\ \hline
0&14&2(2n+5)\\
1&292&4(n^2+17n+47)\\
2&150n+2743&74n^2+646n+1695\\
3&8(242n+1839)&8(3n^3+76n^2+490n+1145)\\
4&32(15n^2+357n+1511)&4(49n^3+718n^2+3880n+7819)\\
5&1024(3n^2+33n+91)&
8(3n^4+94n^3+1020n^2+4728n+8044)\\
6&128(2n+11)(2n^2+22n+61)&
4(21n^4+440n^3+3480n^2+12320n+16480)
\end{array}
\]

以及

\[
\begin{array}{c|l}
j&i_j(n)\\ \hline
0&(n+7)(2n^2+22n+27)\\
1&2(n^4+32n^3+601n^2+2130n+1974)\\
2&76n^4+1429n^3+15241n^2+42266n+35086\\
3&4(6n^5+201n^4+3462n^3+25238n^2+57629n+42843)\\
4&2(110n^5+2828n^4+36819n^3+194748n^2+371397n+245175)\\
5&8(3n^6+115n^5+2802n^4+26849n^3+107106n^2+170502n+98430)\\
6&2(42n^6+1795n^5+24517n^4+150304n^3+439416n^2+
568736n+279360)
\end{array}
\]

表中每个关于 \(n\) 的单项式系数均为非负整数。因此

\[
D_s\ge_{\rm coeff}0,\qquad
Q_s\ge_{\rm coeff}0,\qquad
I_s\ge_{\rm coeff}0.
\]

又因为 \(r\ge3\)，

\[
A_{s,r}=Q_s+(2^r-1)D_s\ge_{\rm coeff}0.
\]

式 (2) 中的其余因子 \(\binom{m+2}{r}\)、\(\beta^r\) 和
\(z^k=(1+2\beta)^k\) 也都逐系数非负，故

\[
\boxed{R_s\ge_{\rm coeff}0\qquad(s\ge5).}
\]

最后，基例是

\[
L_5=12\beta^4(1+5\beta)^2(7+40\beta+75\beta^2)
\ge_{\rm coeff}0.
\]

由

\[
L_{s+1}=u_4^2L_s+R_s
\]

归纳即得所有 \(s\ge5\) 的 \(L_s\ge_{\rm coeff}0\)，从而完成定理。
首系数公式和最高次项又给出非零支撑恰为
\(4,\ldots,2s-2\)。

## 5. 核验边界

`verify_b4_uniform_positivity.py` 独立实现了：

1. 三项二项式系数公式与直接整数卷积的逐项比较；
2. \(D_s,Q_s,I_s\) 的上表正系数公式；
3. 式 (2) 与直接差
   \(L_{s+1}-(1+4\beta)^2L_s\) 的逐项比较；
4. 基例 \(L_5\) 和 AM--GM 加强命题的 \(-60\) 反例。

有限回归只是防止转录错误；全 \(s\) 结论来自上面的符号恒等式与
非负单项式系数表。
