# #679: uniform exceptional-phase anti-clustering is false

Date: 2026-07-22

The candidate-to-run reduction does not permit a black box uniform over all
CRT starts. In fact the full CRT period contains runs of the required
subpower length on which every canonical weight is \(X^{-o(1)}\) or larger.

## Proposition

Let

\[
 H=\lfloor L_1^2\rfloor,\qquad
 Y=\lfloor e^{L_2\sqrt{L_3}}\rfloor,
\]

where \(L_j=\log_jX\), in particular \(L_4=\log_4X\),
and let

\[
 W_0(m)=\prod_{H<p\le z}
 \{1-a\,1_{m\bmod p\in[0,H-1]}\},
 \qquad a={CL_1\over HL},
\]

with \(L=\sum_{H<p\le z}p^{-1}\sim L_2\). There is a residue
\(B_0\bmod Q\), \(Q=\prod_{H<p\le z}p\), such that

\[
 \boxed{W_0(B_0+\ell)\ge X^{-o(1)}
        \quad(1\le\ell\le Y).}                       \tag{1}
\]

The \(o(1)\) is uniform over the displayed run.

## Proof

For every prime \(p>Y+H\), choose \(B_0\bmod p\) so that the interval
\(B_0+[1,Y]\) misses the forbidden block \([0,H-1]\bmod p\). This is
possible because the union of forbidden choices for \(B_0\) has size at
most \(Y+H-1<p\).

For the remaining primes \(H<p\le Y+H\), choose \(B_0\bmod p\)
independently and uniformly. For a fixed \(1\le\ell\le Y\), the load

\[
 Z_\ell=\#\{H<p\le Y+H:B_0+\ell\bmod p\in[0,H-1]\}
\]

is a sum of independent Bernoulli variables and has mean

\[
 \Lambda=H\sum_{H<p\le Y+H}{1\over p}
 =\left({1\over2}+o(1)\right)H L_4.                  \tag{2}
\]

Here
\(\log\log Y=L_3+\tfrac12L_4+o(1)\) and
\(\log\log H=L_3+\log2+o(1)\). A standard Chernoff bound gives

\[
 \mathbb P(Z_\ell>3\Lambda)\le e^{-c\Lambda}
\]

for an absolute \(c>0\). Since
\(\Lambda\asymp L_1^2L_4\gg\log Y=L_2\sqrt{L_3}\), a union bound over all
\(Y\) values of \(\ell\) is less than one. Hence choices exist for which

\[
 \max_{\ell\le Y}Z_\ell=O(HL_4).                    \tag{3}
\]

Combine those local choices, and the avoiding choices for \(p>Y+H\), by
CRT. Equations (2)--(3) and \(a=O_C(L_1/(HL_2))=o(1)\) imply, uniformly in
\(\ell\),

\[
 -\log W_0(B_0+\ell)
 \le(1+o(1))aZ_\ell
 =O_C\left({L_1L_4\over L_2}\right)=o(L_1),
\]

which proves (1).

## Consequence for interval phases

Fix any \(s\) with \(1\le s\le N\), and put
\(A_\ell=B_0+\ell-s\). Then \(B_0+\ell\in(A_\ell,A_\ell+N]\), so for every
fixed \(q\),

\[
 \sum_{m\in(A_\ell,A_\ell+N]}W_0(m)^q
 \ge W_0(B_0+\ell)^q=X^{-o(1)}.                      \tag{4}
\]

Thus the full CRT period really contains \(Y\) consecutive exceptional
interval starts. A theorem saying that *every* length-\(Y\) block of starts
contains a fixed-power-good phase is false.

This does not construct such a run with representatives of size
\(A\asymp X\): the CRT representative may be anywhere in the enormous
period \(Q\). Hence the candidate-to-run reduction remains useful only if
the missing anti-clustering theorem exploits the self-consistent size and
location of the actual dyadic starts.

Strict status: **rigorous arbitrary-start anti-clustering counterexample;
no counterexample to the original Erdős statement and no closure**.
