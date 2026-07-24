# Erdős #323：三项 \(k\) 次幂的 Hua–能量下界

## 目标

令

\[
 f_{k,m}(x)=\#\{n\le x:n=a_1^k+\cdots+a_m^k,\ a_i\ge0\}.
\]

原题在 \(m<k\) 时要求 \(f_{k,m}(x)\gg x^{m/k}\)。初轮的逐变量固定只给
\(x^{1/k}\)。本轮对 \(m=3\) 补上一条严格但仍非终点的经典矩路线。

## 四阶矩

置

\[
S_k(\alpha)=\sum_{1\le a\le X}e(\alpha a^k),\qquad
E_{2s}=\int_0^1|S_k(\alpha)|^{2s}\,d\alpha.
\]

由正交性，\(E_4\) 计数

\[
a^k+b^k=c^k+d^k,\qquad 1\le a,b,c,d\le X.
\]

固定 \(a,c\)，令 \(D=a^k-c^k=d^k-b^k\)。若 \(D=0\)，严格单调性给
\(a=c,d=b\)，共 \(X^2\) 个解。若 \(D\ne0\)，令 \(h=|d-b|\)；则
\(h\mid |D|\)，而对固定符号和 \(h\)，函数
\((b+h)^k-b^k\) 对 \(b\ge1\) 严格递增，所以至多一个 \(b\)。标准除数界
遂给

\[
 E_4\ll_{k,\varepsilon}X^{2+\varepsilon}. \tag{1}
\]

## 八阶矩与插值

对固定 \(k\ge3\)，Hua 引理在 \(j=3\) 给出

\[
 E_8=\int_0^1|S_k(\alpha)|^8\,d\alpha
 \ll_{k,\varepsilon}X^{5+\varepsilon}. \tag{2}
\]

Cauchy–Schwarz 施于
\(|S|^6=(|S|^4|S|^8)^{1/2}\)，由 (1)、(2) 得

\[
 E_6\ll_{k,\varepsilon}X^{7/2+\varepsilon}. \tag{3}
\]

三元组共有 \(X^3\) 个。若 \(r(n)\) 是
\(n=a^k+b^k+c^k\) 的有序表示数，则 (3) 与 Cauchy–Schwarz 给

\[
 |\{a^k+b^k+c^k:1\le a,b,c\le X\}|
 \ge \frac{X^6}{\sum_nr(n)^2}
 \gg_{k,\varepsilon}X^{5/2-\varepsilon}. \tag{4}
\]

取 \(X=\lfloor(x/3)^{1/k}\rfloor\)，得到对每个固定 \(k\ge3\)

\[
 \boxed{f_{k,3}(x)\gg_{k,\varepsilon}
 x^{\,5/(2k)-\varepsilon}.}
\]

特别地，首个被指定的难例 \((k,m)=(4,3)\) 有

\[
 f_{4,3}(x)\gg_\varepsilon x^{5/8-\varepsilon},
\]

严格优于初轮的 \(x^{1/4}\)，但仍低于原题要求的 \(x^{3/4}\)。

## 审慎性与下一断点

这里使用的是经典 Hua 引理的直接组合，极可能属于已有知识而非新论文结果；
没有做完专门的历史优先权检索，故绝不声称新颖性。路线的精确剩余缺口是把
六阶矩从 \(X^{7/2+\varepsilon}\) 降到对角量级
\(X^{3+\varepsilon}\)。对 \((4,3)\) 而言，需要比
\(E_4\)–\(E_8\) 对数凸插值再节省 \(X^{1/2}\)。原题仍开放，闭合距离虽有
定量推进，但没有达到 Q2 候选门槛。
