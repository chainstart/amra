# #679: a candidate forces a long run of exceptional inherited phases

Date: 2026-07-22

The original property holds for every sufficiently large shift \(k\), not
just for one block. Sliding the block therefore turns one hypothetical
candidate into a long consecutive run of bad interval-start phases. This is
a stronger deterministic interface than excluding one prescribed phase.

## 1. Canonical translated weight

Fix \(X\), the usual \(H=(\log X)^2\), and the prime band \((H,z]\). The
four parameters \(H,z,a,t\) are chosen once from this \(X\) and remain fixed
as \(K\) slides. Define
the canonical weight

\[
 W_0(m)=\prod_{H<p\le z}
 \left(1-a\,1_{m\bmod p\in\{0,1,\ldots,H-1\}}\right). \tag{1}
\]

For a block beginning at \(K\), the weight used on \(n\) is exactly

\[
 W_K(n)=W_0(n-K),                                     \tag{2}
\]

because \(p\mid n-(K+j)\) if and only if
\(n-K\equiv j\pmod p\).

Let \(I=(A,A+N]\subset[X,2X]\), \(N\asymp X\), and put

\[
 S_q(B)=\sum_{m\in(B,B+N]}W_0(m)^q.                  \tag{3}
\]

Translation in (2) gives the exact identity

\[
 \sum_{n\in I}W_K(n)^q=S_q(A-K).                     \tag{4}
\]

## 2. Sliding a hypothetical candidate

Choose explicitly

\[
 Y=\left\lfloor\exp\{L_2\sqrt{L_3}\}\right\rfloor.
                                                               \tag{5}
\]

Then \(Y=X^{o(1)}\), \(Y>H\), and, uniformly for
\(Y\le K\le2Y\) and \(0\le j<H\),

\[
 r(K+j)\le (1+\varepsilon+o(1)){L_2\over\sqrt{L_3}}. \tag{6}
\]

Consequently, with \(R_K=\sum_{j<H}r(K+j)\), for every fixed \(q\),

\[
 qR_K\log(1/t)
 \le (qC(1+\varepsilon)+o(1)){L_1\over\sqrt{L_3}}
 =o(L_1).                                             \tag{7}
\]

Suppose \(n_0\in I\) satisfies the first-question inequalities for every
\(k\ge K_\varepsilon\). Since \(K_\varepsilon\) is fixed after
\(\varepsilon\) is fixed and \(Y\to\infty\), eventually \(Y>K_\varepsilon\).
Also \(Y=X^{o(1)}\), so eventually
\(2Y+H<X\le n_0\). Hence every block with \(Y\le K\le2Y\) lies above
\(K_\varepsilon\) and satisfies \(K+H<n_0\). On each
such block the selected-prime counts are below their thresholds, so

\[
 W_K(n_0)^q\ge t^{qR_K}=X^{-o(1)}.                   \tag{8}
\]

Since this single term occurs in the interval sum (4),

\[
 \boxed{S_q(A-K)\ge X^{-o(1)}
        \quad\hbox{for every integer }Y\le K\le2Y.}  \tag{9}
\]

Thus a candidate forces the consecutive block of \(Y+1\) starts

\[
 [A-2Y,A-Y]\cap\mathbb Z                             \tag{10}
\]

to consist entirely of exceptional inherited phases.

The argument works more generally with
\(Y=\exp\{o(L_2L_3)\}\), provided \(Y\to\infty\) sufficiently fast and
the displayed \(o\)-condition is made uniform. Choice (5) avoids any
ambiguity.

## 3. New sufficient deterministic target

Fix \(q,C,\delta\) with \(qC>1+\delta\). It is now enough to prove:

> Every interval of \(Y+1\) consecutive starts in the relevant dyadic
> range contains a \(B\) for which \(S_q(B)\le X^{-\delta}\).

Indeed, (9) is larger than \(X^{-\delta}\) for large \(X\), giving a
contradiction.

The almost-all-phase theorem proves that the exceptional starts have
polynomially small density over the full CRT period, but a density estimate
alone does not prohibit a run of length \(Y=X^{o(1)}\). In fact
`uniform_anticlustering_counterexample.md` constructs such a run somewhere
modulo \(Q\). Therefore the required local anti-clustering estimate must use
the self-consistent location/size of the actual dyadic starts; it cannot be
uniform over arbitrary CRT phases.

Strict status: **exact quantifier/translation reduction; the required
anti-clustering theorem and Erdős #679 remain open**.
