# #679: Lau weight mass versus the far-shift exceptional set

Date: 2026-07-23

This note answers a precise splice question: does Lau's positive-probability
construction already yield enough *unweighted* integers to force an
intersection with the far-good set proved in this round?  The answer from
the published parameters is no.  In addition, Lau's near conclusion is
\(C\log k\), not the #679 threshold, so even a successful intersection at
this stage would still not close the problem.

## 1. Exact weight and total mass in Lau v2

Lau uses

\[
 \nu(n)=1_{x\le n\le2x}1_{W\mid n}
 \prod_{k=1}^{K}
 \left(\sum_{\substack{(d,P(w))=1\\d\mid n+k}}
 \mu(d)\widetilde\eta\left({\log d\over\log R_k}\right)
 \right)^2,
\]

where

\[
 K=(\log x)^{1/1000},\qquad w=0.15\log x,
 \qquad W=\prod_{p\le w}p^4,
 \qquad R_k=x^{1/(100k^{50})}.                      \tag{1}
\]

Lemma 6.2 in the v2 TeX (labelled
`lem:mainpropB`, equation `eqn:probabilitydenominator`) gives

\[
 Z:=\sum_n\nu(n)
 =(1+o(1)){x\over W\prod_{k\le K}\log R_k}
 \left(c_0{W\over\varphi(W)}\right)^K.             \tag{2}
\]

The prime number theorem gives \(\log W=4\vartheta(w)
=(0.6+o(1))\log x\).  Moreover

\[
 \sum_{k\le K}\log\log R_k=O(K\log_2x)=o(\log x)
\]

and

\[
 K\log(W/\varphi(W))=O(K\log_3x)=o(\log x).
\]

Consequently

\[
 \boxed{Z=x^{0.4+o(1)}.}                           \tag{3}
\]

## 2. A pointwise weight bound and an unweighted count

In Lau's source, \(\eta:\mathbb R\to[0,1]\) is supported on \([-1,1]\)
and \(\widetilde\eta(u)=e^{-u}\eta(u)\).  Since here
\(u=\log d/\log R_k\ge0\), the support has \(d\le R_k\) and
\(|\widetilde\eta(u)|\le1\).  Hence, without using cancellation,

\[
 \left|\sum_d\mu(d)\widetilde\eta(\log d/\log R_k)\right|
 \le R_k.
\]

This first gives the crude bound

\[
 \max_n\nu(n)\le\prod_{k\le K}R_k^2
 \le x^{\beta},
 \qquad
 \beta={1\over50}\sum_{k=1}^{\infty}k^{-50}
 ={\zeta(50)\over50}=0.020000\ldots .               \tag{4}
\]

There is, however, a sharper elementary hybrid bound.  Every inner sum is
also bounded by the number of divisors of \(n+k\).  Since
\(K=(\log x)^{1/1000}=o(x)\) and \(n\in[x,2x]\), one has \(n+k\le3x\)
for every \(k\le K\) on the support for large \(x\).  The standard uniform
divisor bound gives

\[
 \tau(n+k)\le x^{C/\log_2x}
\]

for an absolute constant \(C\).  Therefore

\[
 {\log\max_n\nu(n)\over\log x}
 \le2\sum_{k\le K}
 \min\left\{{1\over100k^{50}},{C\over\log_2x}\right\}.
\]

Split at \(J=(\log_2x/(100C))^{1/50}\).  The contribution of \(k\le J\)
is \(O(J/\log_2x)\), and that of \(k>J\) is
\(O(\sum_{k>J}k^{-50})\).  Both are
\(O((\log_2x)^{-49/50})\).  Consequently

\[
 \boxed{\max_n\nu(n)
 \le x^{O((\log_2x)^{-49/50})}=x^{o(1)}.}            \tag{5}
\]

Lau's union bound leaves a fixed positive probability of the proved
\(C\log k\) event (indeed the displayed \(6/(\pi^2k^2)\) bounds leave at
least \(6/\pi^2+o(1)\)).  Combining this with (3) and (5) extracts the
unweighted lower bound

\[
 \boxed{
 \#\{n\in[x,2x]: n\text{ satisfies Lau's proved }C\log k
       \text{ conclusion}\}
 \ge x^{0.4-o(1)}.}                                  \tag{6}
\]

The same calculation applies to the minus-shift version after the paper's
stated sign change.

## 3. Why this does not meet the new far theorem

The far-bad set from this round has cardinality at most

\[
 {x\over\log x}
 \exp\left\{-{\varepsilon\over4}
                   (\log_2x)^{D_\varepsilon}\right\}
 =x^{1-o(1)}.                                       \tag{7}
\]

In this display one may take the optimized explicit value
\(D_\varepsilon=2(1+\varepsilon)/\varepsilon\); any larger fixed value
above the critical \((1+\varepsilon)/\varepsilon\) gives the same
\(x^{1-o(1)}\) comparison.

Although (7) has density tending rapidly to zero, its exponent on the
\(x\)-scale is still \(1-o(1)\), much larger than the guaranteed
\(0.4-o(1)\) exponent in (6).  Cardinality therefore does not
force even Lau's set to meet the far-good set.

Equivalently, (3) and (5) only give the maximal density-ratio estimate

\[
 M_x=x\max_n{\nu(n)\over Z}
 \le x^{0.6+o(1)},                                  \tag{8}
\]

whereas the far saving is merely
\(\exp\{-c_\varepsilon(\log_2x)^{D_\varepsilon}\}=x^{-o(1)}\).
Thus the bounded-density transfer is still quantitatively vacuous.

There are two logically separate missing inputs:

1. Lau proves \(C\log k\), which is weaker than
   \((1+\varepsilon)\log k/\log_2k\) in the near range;
2. even if an exact near event of fixed positive Lau-weight probability
   were available, the published total-mass/max-weight bounds alone would
   not make it avoid the far exceptional set.

A viable splice must prove the far large-deviation estimate directly under
the near-shift weight, or provide a substantially flatter/more numerous
exact-near construction.  Neither is present in Lau v2 or proved here.

A tempting intermediate step is to count far-bad endpoints first on the
basic progression \(W\mid n\), whose cardinality is \(x^{0.4+o(1)}\).
Writing \(n=Wa\) turns the relevant values into the growing-coefficient
linear forms \(Wa-k\), with \(W=x^{0.6+o(1)}\).  The checked
arithmetic-progression Sathe--Selberg result of Spiro is uniform only for
moduli bounded by a fixed power of \(\log x\), so it does not cover this
modulus.  Fan's sifted-set Hardy--Ramanujan theorem concerns prime factors
of the running integer in a set defined by boundedly many forbidden
residue classes; it does not directly estimate \(\omega(Wa-k)\) with
growing \(W,k\).  Thus no progression-restricted far estimate is imported
here.

For completeness, a full-text audit of the v2 TeX found no estimate for
\(\sum_n\nu(n)^2\), no sharper pointwise bound for \(\nu\), and no direct
unweighted support-cardinality lemma.  Thus the paper does not contain a
hidden second-moment input that upgrades (6) enough to change this
comparison.

The almost-all short-interval obstruction proved from Goudout in this
round does not repair the splice.  Its exceptional endpoint set is only
known here to be \(o(x)\), which can still contain all
\(x^{0.4+o(1)}\) points in Lau's basic progression \(W\mid n\).  A useful
weighted version would need either an exceptional bound below the
\(x^{0.4}\) scale or uniform local-\(\omega\) information in the highly
nonuniform sieve measure (whose modulus already has size
\(W=x^{0.6+o(1)}\)).  Neither follows from Goudout's unweighted theorem.
