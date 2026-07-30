# Translation-hyperbola energy and the one-dimensional capacity barrier

## Purpose

The translated Latin SAT core left one genuine loophole: a deliberately
resonant translation set might give one cross edge many compatible partners.
This note identifies the exact additive quantity controlling that loophole,
proves capacity bounds, disposes of arithmetic and geometric progressions,
and constructs a real resonant set showing that a pointwise bounded-degree
claim would be false.

The conclusion is narrow.  One-dimensional translation-product amplification
is excluded for low additive-energy sets, fixed rational arithmetic
progressions, and difference-Sidon sets.  It is not excluded for arbitrary
translation sets.  A resonant set can give a single edge linear degree,
although the present construction does not give the large *average* degree
required by the global exponent ledger.

## 1. Exact compatibility equation

Fix one base rectangle service and write its two signed vertical gaps as
\(X\) and \(Y\).  Give the endpoints of a first cross edge translations
\(s,\delta\in A\), and those of a proposed opposite cross edge translations
\(\gamma,\beta\in A\).  Put

\[
u=s-\beta,\qquad v=\gamma-\delta.
\]

Subtracting the base Gram equation gives exactly

\[
F_{X,Y}(u,v)=u^2-v^2+2Xu-2Yv=0.                           \tag{1}
\]

Equivalently,

\[
(u+X)^2-(v+Y)^2=X^2-Y^2,                                  \tag{2}
\]

or

\[
(u-v+X-Y)(u+v+X+Y)=(X-Y)(X+Y).                            \tag{3}
\]

For a genuine base service the original radial blocks are distinct, so
\(X\ne\pm Y\).  The right side of (3) is nonzero.  For each fixed \(u\)
there are at most two possible \(v\)'s, and conversely.

Let

\[
r_A(t)=|\{(a,b)\in A^2:a-b=t\}|.
\]

Summing over all \(n^2=|A|^2\) choices of the first cross edge gives

\[
H_{X,Y}(A)
 =\sum_{F_{X,Y}(u,v)=0}r_A(u)r_A(v)
 =\sum_{s,\delta\in A}d(s,\delta),                         \tag{4}
\]

where

\[
d(s,\delta)=
\sum_{\beta,\gamma\in A}
1_{F_{X,Y}(s-\beta,\gamma-\delta)=0}.
\]

Thus \(H_{X,Y}(A)/n^2\), not the maximum degree of one edge, is the
average compatibility gain relevant to service amplification.

## 2. Capacity lemma

Write \(E_+(A)=\sum_t r_A(t)^2\), and

\[
\mu_*(A)=\max_{t\ne0}r_A(t).
\]

The exclusion of \(t=0\) is essential: \(r_A(0)=n\) for every set and is
not evidence of resonance.

**Translation-hyperbola capacity lemma.**  If \(X\ne\pm Y\), then

\[
H_{X,Y}(A)\le 2E_+(A),                                    \tag{5}
\]

and

\[
H_{X,Y}(A)
\le n^2+2\mu_*(A)n^2+\mu_*(A)n
\le n^2+3\mu_*(A)n^2.                                    \tag{6}
\]

For (5), apply \(r(u)r(v)\le(r(u)^2+r(v)^2)/2\) and use the fact that every
coordinate occurs on the conic at most twice.  For (6), isolate the
solution \((0,0)\), whose contribution is \(n^2\).  Among terms with
\(v\ne0\), use \(r(v)\le\mu_*\) and at most two \(v\)'s per \(u\).  On
\(v=0\), the only possible nontrivial root is \(u=-2X\), contributing at
most \(n\mu_*\).

Consequently, if the average degree is \(D\), then

\[
E_+(A)\ge \frac12Dn^2,\qquad
\mu_*(A)\ge\frac{D-1}{2+1/n}.                             \tag{7}
\]

Average degree \(n^{2/5}\) therefore forces

\[
E_+(A)\ge\tfrac12n^{12/5}
\]

and a nonzero difference represented \(\Omega(n^{2/5})\) times.  Any
successful one-dimensional resonant amplification must enter a genuinely
high additive-energy / popular-overlap regime.

## 3. Arithmetic progressions

Let \(A=a_0+h\{0,1,\ldots,n-1\}\), where \(h,X,Y\) are fixed rationals and
\(h\ne0\).  Choose an integer \(D\) clearing their denominators.  For
differences \(u=hk\), \(v=h\ell\), equation (3) becomes \(PQ=N\), where

\[
P=D(h(k-\ell)+X-Y),\quad
Q=D(h(k+\ell)+X+Y),\quad
N=D^2(X^2-Y^2)\ne0.
\]

The integers \(P,Q\) determine \((k,\ell)\).  Hence the number of supported
difference pairs is bounded by the signed-divisor count of the fixed
nonzero integer \(N\), independently of \(n\).  Since every weight is at
most \(n^2\),

\[
H_{X,Y}(A)=O_{h,X,Y}(n^2),\qquad
\frac{H_{X,Y}(A)}{n^2}=O_{h,X,Y}(1).                       \tag{8}
\]

For \(A=\{0,\ldots,n-1\}\), \(X=2,Y=1\), once \(n\ge5\) the only supported
difference pairs are

\[
(0,0),\ (0,-2),\ (-4,0),\ (-4,-2).
\]

The exact totals

\[
H(5)=48,\quad H(10)=288,\quad H(20)=1368,\quad H(50)=9408
\]

have average tending to \(4\).  APs do not produce a power gain.

## 4. Geometric progressions and difference-Sidon sets

If every nonzero ordered difference has multiplicity at most one, then

\[
E_+(A)=n^2+n(n-1)=2n^2-n,
\]

so (5) gives \(H_{X,Y}(A)<4n^2\).  Geometric progressions
\(A=\{1,g,\ldots,g^{n-1}\}\), \(g\ge2\), have this property: the
\(g\)-adic valuation identifies the smaller exponent, then the gap is
determined.  Their average partner degree is below four.

## 5. Strictly convex sets: the honest gap

The classical estimate \(E_+(A)\ll n^{5/2}\) for a strictly convex
sequence, inserted into (5), gives only

\[
\frac{H_{X,Y}(A)}{n^2}\ll n^{1/2}.
\]

This does not exclude the target \(n^{2/5}\).  A stronger incidence
estimate specialized to (2) would be needed.

As falsification evidence, exact enumeration for
\(A=\{0^2,1^2,\ldots,(n-1)^2\}\), \(3\le n\le10\), with \(X=2,Y=1\)
gives maximum partner degree \(2\) and \(H=n^2+n\).  This supports bounded
behavior for one model family but is not a theorem for all convex sets.

## 6. Explicit resonance: pointwise bounds are false

Put \(R=X^2-Y^2\).  Equation (2) has the parametrisation

\[
u(t)+X=\frac12\left(t+\frac Rt\right),\qquad
v(t)+Y=\frac12\left(t-\frac Rt\right).
\]

For distinct generic nonzero \(t_1,\ldots,t_r\), set

\[
A=\{0\}\cup\{-u(t_j):1\le j\le r\}
       \cup\{v(t_j):1\le j\le r\}.
\]

The fixed first edge \((s,\delta)=(0,0)\) has the \(r\) partners
\((\beta,\gamma)=(-u(t_j),v(t_j))\), plus its trivial partner.  Generically
\(|A|=2r+1\), so one edge has linear degree.

For the exact \(q=3\) SAT base service,

\[
X=-\frac32,\qquad Y=\frac{\sqrt{12285}}2,\qquad R=-3069,
\]

the parameters \(t=1,\ldots,r\) give \(|A|=2r+1\) and fixed-edge degree at
least \(r+1\), verified symbolically for \(r=3,5,8\).

Thus no universal pointwise \(O(1)\) partner bound is possible.  But this
star supplies only \(r\) extra incidences against the baseline \(n^2\)
total.  It does not establish growing average degree.  Turning a resonant
star into a dense resonant network is the remaining obstruction.

## 7. Decision for the proof campaign

The one-dimensional route now has a precise decision tree:

1. Low additive energy, AP, GP, or a difference-Sidon set: ruled out.
2. A few designed resonances: high maximum degree is possible, but no
   growing average has been obtained.
3. Any successful construction must have
   \(E_+(A)\gtrsim n^{12/5}\) and a nonzero overlap
   \(|A\cap(A+t)|\gtrsim n^{2/5}\).
4. Strictly convex sets remain a real technical gap: the generic energy
   input misses the desired average-degree exponent by \(1/10\).

The next productive question is whether (1) can be dense on a high-energy
set with a popular nonzero difference, or whether such overlap forces a
degeneracy incompatible with \(X\ne\pm Y\).

## Reproducibility

```bash
python3 verify_translation_hyperbola_energy.py
pytest -q test_verify_translation_hyperbola_energy.py
```

The verifier checks (4)--(6), AP totals and supported solutions,
difference-Sidon energy, convex-square samples, the exponent ledger, and
the exact algebraic resonant-star witnesses.
