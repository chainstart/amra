# #679: an ultra-small-tilt window with vanishing nonzero Fourier energy

Date: 2026-07-22

This strengthens the round-8 zero-mode construction at the parameter level.
It does not yet transfer the weight to an \(X\)-interval.

## Parameters

Let \(B=B(X)\to\infty\) satisfy

\[
 B=o(L_3),
\]

and set

\[
 H=\left\lfloor e^{B L_2}\right\rfloor=(\log X)^{B+o(1)},
 \qquad z=e^{L_1/L_2},
\]

\[
 L=\sum_{H<p\le z}{1\over p},qquad
 a={C L_1\over H L},qquad t=1-a,                     \tag{1}
\]

where \(C>1\) is fixed.  Since

\[
 \log\log H=L_3+\log B+o(1),
\]

Mertens gives

\[
 L=L_2-2L_3-\log B+o(1)\sim L_2.                     \tag{2}
\]

The assumptions imply \(H<z\), \(a=o(1)\), and collision freedom for the
\(H\) consecutive shifts.

## Zero-mode exponent

The main zero-mode term is now exact by design:

\[
 HaL=C L_1.                                            \tag{3}
\]

Uniformly for the shifts \(K\le k<K+H\),

\[
 r(k)\ll_\varepsilon {B L_2\over L_3+\log B}.
\]

Thus, for \(R=\sum_{j<H}r(K+j)\),

\[
 R\log(1/t)
 \ll aH{B L_2\over L_3+\log B}
 ={C L_1B\over L_3+\log B}=o(L_1).                    \tag{4}
\]

As in round 8,

\[
 -\log(t^{-R}\mu)\ge HaL-R\log(1/t)
 =(C-o(1))L_1,
\]

so the complete-period good-class density remains

\[
 \boxed{\delta\le X^{-C+o(1)}.}                       \tag{5}
\]

## Fourier energy collapses to the zero mode

The exact local variance identity yields

\[
 \log{M_2\over\mu^2}
 \ll Ha^2L
 ={C^2L_1^2\over HL}.                                 \tag{6}
\]

Since \(H=e^{BL_2}\), the right side is

\[
 \varepsilon_X:=
 \exp\{-(B-2+o(1))L_2\}=o(1).                         \tag{7}
\]

Moreover the total Bernoulli conductor-activation probability satisfies

\[
 \sum_p\beta_p\ll Ha^2L=O(\varepsilon_X).
\]

Consequently, under normalized Fourier energy,

\[
 \boxed{\mathbb P_2(C(h)>1)=O(\varepsilon_X),
 \qquad {M_2\over\mu^2}=1+O(\varepsilon_X).}          \tag{8}
\]

This is strictly stronger than the round-8 polylogarithmic variance bound.
It also changes the full-conductor ledger: for primes away from the lower
endpoint,

\[
 p\beta_p=(1+o(1))Ha^2
 ={C^2L_1^2\over HL^2}=o(1),                           \tag{9}
\]

so the single full-conductor layer no longer makes \(QP_Q\) explode.

## Growing-moment amplification

The good event is independent of the chosen Markov moment.  Let
\(q=q(X)\ge1\) satisfy

\[
 qa=o(1),qquad {B\over L_3}=o(1).
\]

Using \(W^q\) instead of \(W\),

\[
 1-t^q=qa+O(q^2a^2),
\]

and the same threshold ledger gives

\[
 -\log\{t^{-qR}\mathbb E_QW^q\}
 \ge qC L_1\left(1-O(qa)-O\left({B\over L_3}\right)\right). \tag{10}
\]

Hence

\[
 \boxed{\delta\le X^{-qC(1-o(1))}.}                   \tag{11}
\]

If additionally \(q^2\varepsilon_X=o(1)\), then the normalized nonzero
Fourier energy of \(W^q\) is still \(O(q^2\varepsilon_X)=o(1)\).  There is a
wide range of growing \(q\) satisfying both conditions.  Thus the complete-
period good set is not merely \(X^{-C}\)-sparse: this window proves
superpolynomial sparsity while keeping the relative Fourier variance
asymptotic to one.

## Why (8) still does not transfer

Raw interval Parseval multiplies the nonzero energy in (8), or its
\(q^2\varepsilon_X\) analogue, by \(Q/N\), while

\[
 \log Q=(1+o(1))z=\exp\{L_1/L_2+o(1)\}.
\]

The decay in (7), even after any admissible growing-moment amplification, is
far too small to absorb this factor.  Degree tails beyond \(\asymp L_2\) gain
\(\exp\{-\Theta(BL_2^2)\}\), still only \(X^{-o(1)}\).  Thus (8) removes a
misleading local obstruction but does not prove the required signed aggregate
tail or the one-sided interval bound.

There is also a direct Rényi check.  Energy-only summation over conductor
layers generates the local factor

\[
 \sqrt{1-\beta_p}+\sqrt{p\beta_p}.
\]

Although \(p\beta_p=o(1)\), the logarithm of the product has size at least

\[
 \sum_{H<p\le z}\sqrt{p\beta_p}
 \asymp \{\pi(z)-\pi(H)\}a\sqrt H,
\]

which is enormous because \(\pi(z)\) dominates every polylogarithm.  Hence
the disappearance of the single full-conductor blow-up must not be confused
with control of the aggregate Rényi-\(1/2\) entropy.

Strict status: **stronger zero-mode/energy parameter theorem; interval
transfer open; original #679 open**.
