# #679: actual-representative route and recent consecutive-factor input

Date: 2026-07-22

This note audits whether a long exceptional CRT phase run can be forced to
have a representative at the self-consistent location \(A\asymp X\). It
also compares the June 2026 theorem of van Doorn--Tang on consecutive
integers free of medium prime factors with the parameters required here.

## 1. What a hypothetical candidate forces

Round 10 permits any

\[
 Y=\exp\{o(L_2L_3)\}
\]

that tends to infinity sufficiently quickly. Its convenient recorded
choice was

\[
 Y=\exp\{L_2\sqrt{L_3}\}.                            \tag{1}
\]

A candidate \(n_0\asymp X\) then forces a consecutive interval of \(Y\)
actual starts, and more directly forces every integer in a comparable
interval immediately below \(n_0\) to have an abnormally small number of
prime factors. The point is the location: the arbitrary CRT construction
only produces such a run somewhere modulo

\[
 Q=\prod_{H<p\le z}p=\exp\{(1+o(1))z\},              \tag{2}
\]

whereas

\[
 X=z^{(1+o(1))L_2}.                                  \tag{3}
\]

Thus \(Q\) is vastly larger than every fixed power of \(X\). A residue
class supplied only by CRT has no reason to possess a representative below
\(2X\).

## 2. The deterministic complete-period contribution is far too small

Across any interval of \(Y\) consecutive integers, a prime \(p\le Y\)
contributes a complete-period lower bound. For the collision-free block of
\(H\) shifts this gives, up to endpoint errors,

\[
 YH\sum_{H<p\le Y}{1\over p}.
\]

With (1), Mertens' formula gives

\[
 \sum_{H<p\le Y}{1\over p}
 =\log\log Y-\log\log H+O(1)=O(L_4).                 \tag{4}
\]

By contrast, the candidate threshold per shift at distance \(Y\) is

\[
 {\log Y\over\log\log Y}
 =(1+o(1)){L_2\over\sqrt{L_3}}.                      \tag{5}
\]

The ratio between (5) and (4) tends to infinity. Therefore exact counting
of the moduli \(p\le Y\), even with no loss at all, cannot contradict the
candidate run. The missing incidence comes from \(Y<p\le z\), where a
length-\(Y\) interval can hit a prescribed residue zero or one times and no
complete-period lower bound exists.

This is a route obstruction, not a construction of an original candidate.

## 3. Comparison with van Doorn--Tang (2026)

Van Doorn and Tang, *Consecutive integers free of certain prime factors*,
arXiv:2606.19863v1 (18 June 2026), prove the following. For all sufficiently
large \(k\) and

\[
 2k<n\le \exp\left\{{\log^2k\over20\log\log k}\right\},
\]

the product \((n-k)\cdots(n-1)\) has a prime factor in
\((k,k+3k^\theta)\), for a fixed admissible
\(2/5<\theta<3/5\). In particular their least exceptional endpoint obeys

\[
 n_k>\exp\left\{{\log^2k\over20\log\log k}\right\}. \tag{6}
\]

Substitution of the exceptional-run length (1) into (6) gives

\[
 \log n_k\gg {L_2^2L_3\over L_3+O(L_4)}
 \asymp L_2^2.                                       \tag{7}
\]

But the required actual endpoint has

\[
 \log n_0\asymp L_1=\exp(L_2),                      \tag{8}
\]

which is exponentially larger than the exponent in (7). Thus (6) does
not reach the self-consistent location in #679. Conversely, solving the
endpoint condition in (6) for a block length that can reach \(n\asymp X\)
requires roughly

\[
 \log k\gg\sqrt{L_1L_2},                             \tag{9}
\]

and then the #679 threshold
\(\log k/\log\log k\) is already enormously larger than the useful
\(L_2/L_3\)-type scale. Enlarging \(k\) to make (6) applicable therefore
destroys the desired prime-factor comparison.

The paper's Konyagin-type argument is consequently a genuine adjacent
result, but it supplies neither the actual-representative theorem nor the
fixed-power signed-tail estimate needed here.

## 4. Boundary

The audited alternatives leave the same precise gap:

* arbitrary CRT phase engineering has enough freedom but no small
  representative;
* deterministic cycling only sees \(O(L_4)\) reciprocal-prime mass;
* the new consecutive-factor theorem reaches endpoints
  \(\exp(O(L_2^2))\), not \(\exp(L_1)\), at the required run length.

Strict status: **the recent theorem does not close the actual-phase gap;
no contradiction to a candidate and no proof of #679 is claimed**.

Primary source checked: https://arxiv.org/abs/2606.19863
