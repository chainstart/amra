# Erdős #1083: cyclotomic tensor escape

Date: 2026-07-30

## 0. Outcome

The growing-cyclotomic prism in
`GROWING_CYCLOTOMIC_CHART_EXTRACTION_NOGO.md` is a sharp local
obstruction to bounded-degree chart extraction.  It cannot, however,
be enlarged to the global \(N=t^5\) critical scale by stacking full
regular polygons on rational-square radii with rational anchored
height squares.  Such a stack has linearly many distinct distances,
even when its height sets vary from radius to radius.

This is a rigorous exclusion of one natural growing-field extremizer,
not an unconditional improvement for Erdős #1083.  A general critical
configuration has not been proved to contain the synchronized fibres
assumed below.

## 1. Stacked prime-polygon fibres

Let \(p\ge7\) be an odd prime and let
\[
{\cal R}\subset\mathbb R_{>0}
\]
be a finite set of distinct radii such that \(r^2\in\mathbb Q\) for
every \(r\in{\cal R}\).  For each \(r\), let
\({\cal Z}_r\subset\mathbb R\) be a nonempty finite height set.  Write
\[
z_r^-=\min{\cal Z}_r
\]
and assume only
\[
\boxed{(z-z_r^-)^2\in\mathbb Q\qquad(z\in{\cal Z}_r).}
\tag{1}
\]
Put
\[
\boxed{
P({\cal R},p,({\cal Z}_r))
=
\left\{
\left(
r\cos\frac{2\pi j}{p},
r\sin\frac{2\pi j}{p},
z
\right):
r\in{\cal R},\ 0\le j<p,\ z\in{\cal Z}_r
\right\}.
}
\tag{2}
\]
Then
\[
N:=|P|=p\sum_{r\in{\cal R}}|{\cal Z}_r|.
\tag{3}
\]

### Theorem 1 (cyclotomic tensor escape)

The nonzero squared-distance set of (2) satisfies
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{p-1}{2}\sum_{r\in{\cal R}}|{\cal Z}_r|
=
\frac{p-1}{2p}N.
}
\tag{4}
\]
In particular,
\[
|\Delta^2(P)|\ge\left(\frac12-\frac1{2p}\right)N.
\tag{5}
\]

No common height progression or common height count is required.

### Proof

Write
\[
\zeta=e^{2\pi i/p},
\qquad
a_d=2-\zeta^d-\zeta^{-d}
\quad
\left(1\le d\le\frac{p-1}{2}\right).
\tag{6}
\]
For every triple
\[
(r,d,u)\quad\text{with}\quad
r\in{\cal R},\qquad
1\le d\le\frac{p-1}{2},\qquad
u\in{\cal Z}_r,
\]
the set \(P\) contains a genuine point pair on the radius-\(r\)
polygon with angular separation \(d\), one endpoint at height
\(z_r^-\), and the other at height \(u\).
Its squared distance is
\[
\lambda(r,d,u)=r^2a_d+(u-z_r^-)^2.
\tag{7}
\]
It is positive because \(d\ne0\pmod p\).

We prove that the map in (7) is injective.  Suppose
\[
r^2a_d+(u-z_r^-)^2
=s^2a_e+(v-z_s^-)^2.
\tag{8}
\]
After substituting (6), this is the rational linear relation
\[
\begin{aligned}
0={}&
\left(
2r^2-2s^2+(u-z_r^-)^2-(v-z_s^-)^2
\right)\\
&-r^2(\zeta^d+\zeta^{-d})
+s^2(\zeta^e+\zeta^{-e}).
\end{aligned}
\tag{9}
\]
The minimal polynomial of \(\zeta\) over \(\mathbb Q\) is
\[
\Phi_p(X)=1+X+\cdots+X^{p-1}.
\tag{10}
\]
Consequently, the only rational relation among
\(1,\zeta,\ldots,\zeta^{p-1}\) is a scalar multiple of the all-ones
relation.  Relation (8) is supported on at most
\[
\{0,d,p-d,e,p-e\},
\]
which has fewer than \(p\) elements because \(p\ge7\).  Relation (9) must
therefore have every coefficient equal to zero.

If \(d\ne e\), recall that both lie in
\([1,(p-1)/2]\), so the two unordered exponent pairs
\(\{d,p-d\}\) and \(\{e,p-e\}\) are disjoint.  Equation (9) would
then have coefficient \(-r^2\ne0\) at \(\zeta^d\), a contradiction.
Hence \(d=e\).  The coefficient at \(\zeta^d\) now gives
\(r^2=s^2\), and positivity of the radii gives \(r=s\).
The constant coefficient then gives
\[
(u-z_r^-)^2=(v-z_r^-)^2.
\]
Both \(u,v\) are at least \(z_r^-\), so \(u=v\).

Thus (7) supplies exactly
\[
\frac{p-1}{2}\sum_r|{\cal Z}_r|
\]
different nonzero squared distances, proving (4). \(\square\)

## 2. Consequence at the critical parameterization

As a special case, take \(L=|{\cal R}|\) and
\[
{\cal Z}_r=\{0,\delta,\ldots,(H-1)\delta\},
\qquad \delta^2\in\mathbb Q,
\]
at every radius.  Then \(N=pLH\).  Take \(p=t\), \(L=t^2\), and
\(H=t^2\), along prime values of \(t\).
Then
\[
N=t^5,
\]
but Theorem 1 gives
\[
\boxed{
|\Delta^2(P)|\ge\left(\frac12-o(1)\right)t^5,
}
\tag{11}
\]
far above the critical \(t^{3+o(1)}\) distance scale.

The same conclusion holds for every factorization
\[
LH=t^4:
\]
adding only radius layers, only height layers, or any mixture of the
two does not rescue the growing-cyclotomic prism.

## 3. Exact scope

The theorem uses two synchronized hypotheses and one arithmetic
hypothesis:

1. every chosen radius carries the complete regular \(p\)-gon;
2. every angular column at a fixed radius carries the same
   radius-dependent height set \({\cal Z}_r\);
3. the squared radii and anchored squared height differences in (1)
   lie in \(\mathbb Q\).

It does not require the height sets at different radii to agree, to
have equal cardinality, or to be arithmetic progressions.

The rationality can be replaced by a base field \(F\) over which
\(\Phi_p\) remains irreducible and for which the five displayed
characters remain linearly independent, but no such extension is
needed for the stated exclusion.

The theorem does **not** show that the inherited common-axis branch
contains this product.  Its role is narrower and rigorous:

\[
\boxed{
\text{the local prime-prism field obstruction cannot be scaled to }
N=t^5
\text{ by the natural synchronized tensor construction.}
}
\tag{12}
\]

A successful unconditional argument still has to prove either:

- enough synchronization to invoke Theorem 1 (or a robust version);
- a low-complexity weighted chart to invoke the number-field terminal
  theorem; or
- direct distance expansion in configurations lacking both forms of
  structure.

## 4. Verification

`verify_cyclotomic_tensor_escape.py` represents an element of
\(\mathbb Q(\zeta_p)\) by its rational coefficient vector modulo the
single relation
\[
1+\zeta+\cdots+\zeta^{p-1}=0.
\]
For several primes, rational squared-radius sets, and different
radius-dependent anchored height-square sets,
it verifies:

1. the canonical vectors of all labels (7) are distinct; and
2. their count is
   \((p-1)\sum_r|{\cal Z}_r|/2\).

These finite checks audit the indexing and the quotient
representation.  The unbounded statement rests on the proof above.
