# Erdős #679: a large-band small-tilt window breaks the old zero-mode barrier

Date: 2026-07-22 (Asia/Hong_Kong)

Status: strict zero-frequency theorem and a new candidate proof window.  The
interval-transfer estimate for this much larger full modulus is not proved,
so #679 remains open.

## 1. Parameters

Write

\[
 L_1=\log X,\qquad L_2=\log_2X,\qquad L_3=\log_3X.
\]

Fix \(C>1\), and set

\[
 H=\left\lfloor\left({L_1\over L_2}\right)^2\right\rfloor,
 \qquad
 z=\exp(L_1/L_2),
 \qquad
 a={C\over\sqrt H},
 \qquad
 t=1-a.                                                \tag{1}
\]

Take the consecutive shifts

\[
 k_j=K+j,\qquad 0\le j<H,
\]

and all primes

\[
 {\cal P}=\{p:H<p\le z\}.
\]

For sufficiently large \(X\), \(0<a<1/2\), every selected prime exceeds
the number of shifts, and the local residue classes are collision-free.

Let

\[
 L=\sum_{H<p\le z}{1\over p}.
\]

Mertens' theorem gives

\[
 \begin{aligned}
 \log\log z&=L_2-L_3,\\
 \log\log H&=L_3+\log2+o(1),
 \end{aligned}
\]

and hence

\[
 \boxed{L=L_2-2L_3-\log2+o(1)\sim L_2.}                \tag{2}
\]

## 2. Complete-period lower-tail theorem

Let

\[
 r(k)=\left\lceil
 (1+\varepsilon){\log k\over\log\log k}
 \right\rceil-1,
\qquad
 R=\sum_{j<H}r(k_j).
\]

For the CRT weight

\[
 W(a)=t^{\sum_{j<H}\nu_j(a)},\qquad
 \nu_j(a)=\#\{p\in{\cal P}:p\mid a-k_j\},
\]

the proportion \(\delta\) of residue classes modulo
\(Q=\prod_{p\in{\cal P}}p\) satisfying all
\(\nu_j(a)\le r(k_j)\) obeys

\[
 \boxed{\delta\le X^{-C+o(1)}.}                        \tag{3}
\]

In particular, choosing any fixed \(C>1\) makes the complete-period
zero-frequency estimate stronger than \(X^{-1}\).  This is the first
parameter window in the campaign where the zero mode itself is strong
enough to force an \(X\)-length interval empty, *if* it can be transferred
to that interval with a tolerable relative error.

### Proof

The exact local mean is

\[
 \mu={1\over Q}\sum_{a\bmod Q}W(a)
 =\prod_{H<p\le z}\left(1-{Ha\over p}\right).
\]

On the good event, \(\sum_j\nu_j(a)\le R\), so

\[
 \delta\le t^{-R}\mu.
\]

Put \(G=-\log(t^{-R}\mu)\).  Since
\(-\log(1-x)\ge x\),

\[
 G\ge HaL-R\log(1/t).                                  \tag{4}
\]

Uniformly for \(K\le k\le K+H\),

\[
 r(k)\le r_{\max}
 ={(2+o(1))(1+\varepsilon)L_2\over L_3}.               \tag{5}
\]

Also

\[
 \sqrt H={L_1\over L_2}\{1+o(1)\},\qquad
 \log(1/t)=a+O(a^2).
\]

Equations (2), (4), and (5) yield

\[
 \begin{aligned}
 HaL
 &=C\sqrt H\,L
  =(C-o(1))L_1,\\
 R\log(1/t)
 &\le Hr_{\max}\{a+O(a^2)\}\\
 &=C\sqrt H\,r_{\max}+O(r_{\max})
  =O_\varepsilon(L_1/L_3)
  =o(L_1).
 \end{aligned}
\]

Thus \(G\ge(C-o(1))\log X\), proving (3).

## 3. Effective Fourier energy remains small

Although the full modulus is enormous, the small tilt makes the Fourier
energy sparse.  The exact variance identity gives

\[
 \log{M_2\over\mu^2}
 \ll Ha^2L=C^2L
 =O_C(L_2),                                            \tag{6}
\]

so

\[
 {M_2\over\mu^2}\le(\log X)^{O_C(1)}.                  \tag{7}
\]

The Bernoulli activation probability at a typical prime is

\[
 \beta_p\asymp {Ha^2\over p}={C^2\over p}.
\]

Consequently

\[
 \mathbb E_2\log C(h)
 \ll C^2\sum_{H<p\le z}{\log p\over p}
 =(C^2+o(1))\log z
 ={(C^2+o(1))L_1\over L_2}.                            \tag{8}
\]

Thus the geometric mean reduced conductor under Fourier energy is only

\[
 \exp\{\mathbb E_2\log C(h)\}
 =X^{C^2/L_2+o(1)}
 =X^{o(1)}.                                            \tag{9}
\]

Equations (3) and (9) show why this window evades the earlier single-band
budget calculation: a very large number of coordinates supplies a
\(\log X\)-sized *linear* small-tilt gain, while the quadratic Fourier
energy cost keeps the typical conductor subpower.

## 4. The unresolved interval-transfer step

The full modulus is

\[
 \log Q=\vartheta(z)-\vartheta(H)
 =(1+o(1))z
 =\exp\{L_1/L_2+o(1)\}.                                \tag{10}
\]

Therefore

\[
 Q=\exp\{X^{1/L_2+o(1)}\},
\]

which is vastly larger than \(X\).  The raw high-conductor Cauchy term
contains \(\sqrt{Q/X}\) and is useless.  The first-overrun transfer theorem
does not apply: it relies on \(Q/X\ll\log X\) and
\(H=(\log X)^{o(1)}\), whereas (1) has
\(H=(\log X)^{2-o(1)}\).

Nor does (9) alone solve the problem.  A small geometric-mean conductor
does not control the contribution of the rare high-conductor frequencies
after multiplication by the full interval Fourier norm.  The needed next
estimate has to keep the actual reduced fraction \(u/c\) and the local
Dirichlet-kernel phases, rather than bounding all discarded frequencies by
\(\sum_h|G_N(h)|^2=QN\).

A clean sufficient target is

\[
 \sum_{h\ne0}\widehat W(h)e(hA/Q)G_N(h)
 =o(N\mu)                                             \tag{11}
\]

uniformly for \(A\asymp X\), \(N\asymp X\).  Since the candidate upper
bound is \(t^{-R}\) times the interval weight, this is equivalent to proving

\[
 \sum_{a\in(A,A+N]}W(a)
 =(1+o(1))N\mu.                                       \tag{12}
\]

Possible interfaces for (12) are a weighted Farey large sieve over the
actual conductor-energy measure, or a direct truncated-conductor
fundamental lemma which controls the rare remainder without the full
modulus \(Q\).

For the negative answer itself, the asymptotic (12) is stronger than
necessary.  Since \(C>1\) is fixed, the same argument closes if one proves
only the uniform one-sided estimate

\[
 \sum_{a\in(A,A+N]}W(a)\le N\mu X^{o(1)}.              \tag{13}
\]

Indeed, (3) then bounds the candidate count by
\(X^{1-C+o(1)}<1\).  The later Farey--ANOVA audit isolates a one-sided signed
high-degree tail estimate that is sufficient for (13), but does not prove
it.

## 5. Stress tests and scope

* The gain (3) is not the optimal Chernoff saddle.  The saddle
  \(t=R/(HL)\) is close to zero and would make the conductor energy far too
  large.  The deliberately nonoptimal tilt \(1-t=C/\sqrt H\) balances
  zero-mode gain against phase-transfer cost.
* The integer ceiling in \(r(k)\) changes (5) by \(O(1)\), negligible
  compared with \(L_2/L_3\).
* The condition \(p>H\) guarantees exact collision freedom even though
  \(H\) is much larger than in round 5.
* Formula (3) is a complete-period density statement only.  It must not be
  reported as an interval count or as a disproof of the existence of
  infinitely many candidates.

Strict conclusion: the old assertion that the zero mode must remain
\(o(\log X)\) is false once one leaves the transferable full-modulus
regime and uses a large band with a small, non-saddle tilt.  The campaign's
leading #679 route is now the one-sided bound (13) (or the stronger
asymptotic (12)), not further optimisation of the complete-period Chernoff
factor.
