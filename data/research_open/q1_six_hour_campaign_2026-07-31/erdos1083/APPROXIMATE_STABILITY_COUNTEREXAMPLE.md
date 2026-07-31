# Erdős #1083: an endpoint Følner counterexample to qualitative direct-tiling stability

Date: 2026-08-01

## 0. Verdict

The qualitative stability statement left open after the exact
direct-tiling rank theorem is false.

More precisely, there are endpoint-sized systems with

\[
 |X|=S=t^{7/9},\qquad |T_i|=U=t^{5/6},\qquad
 |V|=SU=t^{29/18},
\]

and a number \(k=k(t)\to\infty\) of pairwise transverse rational
dilation spaces such that every row map

\[
 T_i\times X\longrightarrow V_i
\]

is exactly injective, while

\[
 |V_i\mathbin\triangle V|=o(SU)
\]

uniformly in \(i\).  The construction also has positive tangent
squares, genuine nonaligned reverse-circle rows, and

\[
 \left|\bigcup_iT_i\right|\le t.
\]

Thus no bound on the transverse rank can follow from only exact row
injectivity, the endpoint cardinalities, the common
tangent-universe cap, and an unspecified \(o(SU)\) common-spectrum
error.

The obstruction is a two-dimensional Følner box.  Long lattice lines
in arbitrarily many primitive directions separately tile all but a
small boundary of the same box.  The exact Laurent-polynomial
divisibility used in the earlier rank theorem is destroyed by that
boundary, even though its relative size tends to zero.

This does **not** refute Erdős #1083.  It does not build an entire
critical hub, does not supply \(t^{13/18}\) rows in one block, and
does not control all pairwise distances after the incidence points
are added.  Its force is precise: it closes the proposed qualitative
stability route and identifies the quantitative scale or extra
structure that any replacement theorem must use.

## 1. Endpoint parameters

Let \(m\ge2\) be an integer and put

\[
 t=m^{72},\quad S=m^{56},\quad U=m^{60},\quad
 L=m^{58},\quad k=m.
\tag{1.1}
\]

Then

\[
 S=t^{7/9},\qquad U=t^{5/6},\qquad
 L^2=m^{116}=SU=t^{29/18}.
\tag{1.2}
\]

Set

\[
 X=\left\{\frac{j}{S-1}:0\le j<S\right\}\subset[0,1].
\tag{1.3}
\]

The normalization in (1.3) is essential for the geometric interface:
the elements of \(X\) are genuine sine values rather than
unrestricted integers.

Work first in the lattice \(\mathbb Z^2\).  Let

\[
 Q_L=\{(a,b):0\le a,b<L\}
\tag{1.4}
\]

and, for \(1\le r\le m\), use the primitive direction

\[
 v_r=(1,r).
\tag{1.5}
\]

Embed the lattice injectively in the reals by

\[
 \iota(a,b)=a+b\sqrt2.
\tag{1.6}
\]

Choose a sufficiently large positive constant \(C\), specified in
Section 4, and define the common spectrum

\[
 V=C+\iota(Q_L).
\tag{1.7}
\]

It has exactly \(L^2=SU\) elements.

## 2. Simultaneous near-tilings of one box

The exact statement being tested is the following.

### Qualitative stability assertion QS (false)

For every endpoint sequence \(S,U\to\infty\) with \(SU<S^3\), suppose
one has a fixed \(S\)-element set \(X\), a fixed \(SU\)-element set
\(V\), and rows

\[
 V_i=A_i\oplus\lambda_iX,\qquad |A_i|=U,
\]

such that

\[
 \max_i |V_i\mathbin\triangle V|=o(SU).
\]

Then the cardinality of any pairwise transverse family of spaces
\(\operatorname{span}_{\mathbb Q}(\lambda_i(X-X))\) is bounded
independently of the endpoint parameter (and, in the hoped-for
version, is at most two).

Theorem 2 below refutes QS even after adding positivity, a genuine
reverse-circle interpretation, and the #1083 tangent-universe cap.
It does not address a stronger assertion with a prescribed error
smaller than the Følner boundary scale, or one with critical
many-row tangent multiplicity.

### Lemma 1 (directional block partition)

Fix \(1\le r<L\).  The maximal lattice strings in \(Q_L\) parallel
to \(v_r=(1,r)\) number

\[
 N_r=(r+1)L-r.
\tag{2.1}
\]

Partition each maximal string, starting at its initial endpoint, into
consecutive blocks of \(S\) points and one terminal remainder of
fewer than \(S\) points.  If \(E_r\) is the total number of remainder
points, then

\[
 0\le E_r<SN_r
\tag{2.2}
\]

and \(S\mid E_r\).

#### Proof

A point of \(Q_L\) is the initial point of a maximal \(v_r\)-string
exactly when its predecessor lies outside \(Q_L\).  This says

\[
 a=0\quad\hbox{or}\quad b<r.
\]

Inclusion--exclusion gives \(L+rL-r=(r+1)L-r\) initial points.  Every
string leaves fewer than \(S\) points after its full \(S\)-blocks,
proving (2.2).  The covered set is a disjoint union of \(S\)-blocks,
while \(|Q_L|=L^2=SU\) is divisible by \(S\); hence \(S\mid E_r\).
\(\square\)

Let \(\mathcal A_r^{\rm core}\subset Q_L\) be the initial points of
all full \(S\)-blocks.  Then

\[
 \mathcal A_r^{\rm core}\oplus
 \{0,v_r,\ldots,(S-1)v_r\}\subset Q_L
\tag{2.3}
\]

has size \(L^2-E_r\).

To keep exactly \(U\) base points, add \(E_r/S\) remote block starts:

\[
 \mathcal A_r^{\rm out}
 =\{(2L+j,2L):0\le j<E_r/S\}.
\tag{2.4}
\]

The \(S\)-blocks based at (2.4) are disjoint from \(Q_L\), disjoint
from one another, and disjoint from the core blocks.  Indeed, equality
of points in two remote blocks first forces equality of their step
indices from the second coordinate, and then equality of the two
start indices from the first coordinate.

Put

\[
 \mathcal A_r=\mathcal A_r^{\rm core}\cup
 \mathcal A_r^{\rm out}.
\tag{2.5}
\]

Then

\[
 |\mathcal A_r|
 =\frac{L^2-E_r}{S}+\frac{E_r}{S}=U,
\tag{2.6}
\]

and the map

\[
 \mathcal A_r\times\{0,\ldots,S-1\}\longrightarrow\mathbb Z^2,
 \qquad (a,j)\longmapsto a+jv_r
\tag{2.7}
\]

is injective.

### Theorem 2 (endpoint qualitative-stability counterexample)

There are real sets \(A_r,V_r,V\), \(1\le r\le k=m\), and nonzero
real dilations \(\lambda_r\) such that

\[
 V_r=A_r\oplus\lambda_rX,\qquad
 |A_r|=U,\qquad |V_r|=|V|=SU,
\tag{2.8}
\]

the spaces

\[
 W_r=\operatorname{span}_{\mathbb Q}
      \bigl(\lambda_r(X-X)\bigr)
\tag{2.9}
\]

are pairwise transverse, and

\[
 \max_{1\le r\le m}
 \frac{|V_r\mathbin\triangle V|}{SU}
 <\frac{2(m+1)}{m^2}.
\tag{2.10}
\]

In particular, the number \(m\to\infty\) of pairwise transverse
spaces is unbounded while the error in (2.10) tends to zero.

#### Proof

Set

\[
 \lambda_r=(S-1)(1+r\sqrt2),
\qquad
 A_r=C+\iota(\mathcal A_r).
\tag{2.11}
\]

For \(x=j/(S-1)\in X\),

\[
 \lambda_rx=j(1+r\sqrt2)=\iota(jv_r).
\tag{2.12}
\]

Thus (2.7) proves the direct decomposition in (2.8).  Its core part
is a subset of (1.7), of size \(SU-E_r\), while its remote part is
disjoint from (1.7), of size \(E_r\).  Therefore

\[
 |V_r\mathbin\triangle V|=2E_r.
\tag{2.13}
\]

By (2.1)--(2.2), \(r\le m\), and \(L/S=m^2\),

\[
 \frac{2E_r}{SU}
 <\frac{2SN_r}{L^2}
 \le \frac{2(r+1)S}{L}
 \le\frac{2(m+1)}{m^2},
\]

which proves (2.10).

Since \(X-X\) contains \(1/(S-1)\),

\[
 W_r=\mathbb Q(1+r\sqrt2).
\tag{2.14}
\]

If \(W_r\cap W_s\ne\{0\}\), then

\[
 \frac{1+r\sqrt2}{1+s\sqrt2}\in\mathbb Q.
\]

Comparing the rational and \(\sqrt2\) coefficients forces \(r=s\).
Thus distinct spaces are transverse.  \(\square\)

## 3. Why this kills the qualitative stability route

The exact direct-tiling rank theorem says that exact common tilings

\[
 V=A_i\oplus\lambda_iX
\]

in pairwise transverse spaces force \(S^k\le|V|\).  At the #1083
endpoint, \(|V|=SU<S^3\), so exact equality permits at most two such
spaces.

Theorem 2 has the strongest possible row-side hypothesis: every row
map is exactly injective and has exactly \(SU\) values.  Only equality
of the row spectra is weakened, by an \(o(SU)\) symmetric difference.
Nevertheless, \(k=m\to\infty\).  Consequently there can be no theorem
of the form QS above, namely

> exact row injectivity + endpoint size + \(o(SU)\) proximity to one
> common spectrum implies bounded transverse rank.

The scale exposed by the construction is

\[
 \frac SL=\sqrt{\frac SU}=t^{-1/36}.
\tag{3.1}
\]

For any fixed number of directions, the relative error is
\(O(\sqrt{S/U})\).  For \(k=m=t^{1/72}\) directions it is
\(O(t^{-1/72})\).  A viable replacement must therefore do at least
one of the following:

1. obtain a quantitatively smaller common-spectrum error than the
   box-boundary scale;
2. exploit the much larger block row count and prove that the rows
   cannot all be organized as Følner near-tilings;
3. exploit strong **actual reuse** inside the tangent sets rather
   than only the cap on their union; or
4. use parabolic height relations involving several rows, which the
   single-row near-tiling statement discards.

This is a strict branch change.  Approximate mask-polynomial
divisibility, without one of these quantitative inputs, cannot close
the endpoint.

## 4. Genuine reverse-circle realization

Set \(\rho=1\) and

\[
 z_r=\frac{S-1}{2}(1+r\sqrt2),
\qquad 2z_r=\lambda_r.
\tag{4.1}
\]

Choose, for example,

\[
 C=10S^2m^2+10.
\tag{4.2}
\]

Every lattice coordinate used in (2.5) is nonnegative, while
\(z_r^2<3S^2m^2\) for \(m\ge2\).  Hence every element of

\[
 T_r=A_r-1-z_r^2
\tag{4.3}
\]

is positive.  Moreover \(|T_r|=U\), and

\[
 1+z_r^2+T_r+2z_rX
 =A_r+\lambda_rX=V_r.
\tag{4.4}
\]

The common tangent-square universe satisfies

\[
 \left|\bigcup_{r=1}^mT_r\right|
 \le mU=m^{61}<m^{72}=t.
\tag{4.5}
\]

Take an anchor source circle of radius one and radial centre \(A>1\)
in the plane \(y=0\).  For each \(x\in X\), use the source point with
sine \(x\).  For every \(\tau\in T_r\), take the target

\[
 q_{r,\tau}=(A,\sqrt\tau,-z_r)
\tag{4.6}
\]

and selected producer label \(1+\tau\).  The reverse circle has
centre \((A,-z_r)\), radius one, and axis

\[
 \{(A,y,-z_r):y\in\mathbb R\}.
\]

All target planes are nonperpendicular, all targets are off-axis,
and the distinct positive heights \(z_r\) give pairwise nonaligned
rows.  Direct Cartesian expansion gives the anchor squared distance

\[
 1+z_r^2+\tau+2z_rx,
\]

which is exactly (4.4).  Thus the counterexample is not merely a
formal set-system construction.

### Geometry firewall

The construction controls anchor-to-target spectra and the producer
incidences.  It does **not** bound:

- distances among the translated incidence points;
- distances among targets;
- distances between a translated incidence point and a target from
  a different producer row; or
- the full number of distance labels in the union configuration.

It therefore is not a few-distance configuration and is not a
counterexample to Erdős #1083.

## 5. What remains genuinely open

The counterexample does not rule out a theorem using the full
critical block size \(t^{13/18}\), a quantitative error below the
Følner boundary scale, or a high-multiplicity tangent-reuse
hypothesis.  Those are now the only credible stability inputs.

A sharp next question is:

> If \(q=t^{13/18+o(1)}\) near-direct rows lie within
> \(o(t^{-1/36}SU)\) of one spectrum, and their \(U\)-element tangent
> sets have union at most \(t^{1+o(1)}\), must a positive proportion
> of the height spaces lie in two rational-intersection clusters, or
> must one obtain a multirow parabolic cycle?

Unlike the disproved qualitative statement, this target contains a
scale that excludes the explicit Følner construction.

## 6. Reproduction

Run:

    python3 verify_approximate_transverse_counterexample.py
    python3 -m unittest -v test_approximate_transverse_counterexample.py

The verifier enumerates small boxes, checks every line partition and
direct representation, audits the symbolic endpoint exponents and
error bound, and checks the algebraic and geometric interfaces.
