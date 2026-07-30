# Square–chord sumset expansion at the critical common-radius slice

Date: 2026-07-30.

## 1. Claim ledger and scope

Let
\[
A_m=\{0^2,1^2,\ldots,(m-1)^2\}
\]
and
\[
x_k=2m^2(1-\cos(k\theta)),\qquad0\le k<S.
\]
Assume the angular points
\[
1,e^{i\theta},\ldots,e^{i(S-1)\theta}
\]
are pairwise distinct, and put \(X_S=\{x_k:0\le k<S\}\).

The main result is an unconditional estimate **inside this exact slice**:
\[
\boxed{
|A_m+X_S|
\ge
\frac{m^2S^2}{2mS+\tau_*(m)S^2},
}
\tag{1}
\]
where
\[
\tau_*(m)=
\max_{1\le n\le(m-1)^2}\tau(n)
\]
and \(\tau\) is the divisor function (take \(\tau_*(1)=1\)).
Consequently
\[
|A_m+X_S|
\gg
\min\left\{mS,\frac{m^2}{\tau_*(m)}\right\}.
\tag{2}
\]
This is strictly stronger than the generic \(m\sqrt S\) scale whenever
\[
m\gg\tau_*(m)\sqrt S
\]
and \(S\to\infty\).  The critical diagonal \(m=S\) lies well inside this
range.

At the critical specialization \(m=S=t^2\),
\[
|A_m+X_S|
\ge\frac{m^2}{\tau_*(m)+2}
=m^{2-o(1)}
=t^{4-o(1)}.
\tag{3}
\]
Inside the full explicit anisotropic construction, where \(N=t^5\),
this is
\[
D\ge |A_m+X_S|-1=N^{4/5-o(1)}.
\tag{4}
\]

This improves the generic convex-sumset scale \(m\sqrt S\) for the
critical square-height model, uniformly in \(\theta\).  It is not an
unconditional improvement of \(f_3(N)\): the inherited proof tree has
not produced the consecutive-height, common-radius, common-progression
rectangle assumed here.

## 2. A general square-translate theorem

The trigonometry is needed only to control repetitions among the \(x_k\).
The additive core is more general.

### Theorem 1

Let \(x_0,\ldots,x_{S-1}\) be real numbers, with every value occurring at
most twice.  Then
\[
\left|
A_m+\{x_0,\ldots,x_{S-1}\}
\right|
\ge
\frac{m^2S^2}{2mS+\tau_*(m)S^2}.
\tag{5}
\]

### Proof

For a real number \(y\), let
\[
r(y)=
\#\{(d,k):0\le d<m,\ 0\le k<S,\ d^2+x_k=y\}.
\]
Then
\[
\sum_y r(y)=mS.
\]
By Cauchy–Schwarz,
\[
(mS)^2
\le
|A_m+\{x_k\}|\,
\sum_y r(y)^2.
\tag{6}
\]

The energy on the right counts
\[
d^2+x_k=e^2+x_l.
\tag{7}
\]
The \(k=l\) terms contribute \(mS\).  If \(k\ne l\) and \(x_k=x_l\),
then (7) forces \(d=e\).  Since every \(x\)-value occurs at most twice,
there are at most \(S\) ordered off-diagonal pairs \((k,l)\) of this
type, and their total contribution is at most another \(mS\).

It remains to consider \(x_k\ne x_l\).  If (7) has a solution, then
\[
n=x_l-x_k=d^2-e^2
\]
is a nonzero integer with \(|n|\le(m-1)^2\).  Factoring
\[
n=(d-e)(d+e)
\tag{8}
\]
shows that, for a fixed ordered pair \((k,l)\), equation (7) has at most
\(\tau(|n|)\le\tau_*(m)\) solutions: a positive divisor of \(|n|\)
determines \(d-e\) and \(d+e\), hence determines \(d,e\).
There are fewer than \(S^2\) ordered layer pairs.  Therefore
\[
\sum_y r(y)^2
\le2mS+\tau_*(m)S^2.
\tag{9}
\]
Combining (6) and (9) proves (5). \(\square\)

The standard maximal-order estimate
\[
\max_{n\le m^2}\tau(n)
=\exp\!\left(
O\!\left(\frac{\log m}{\log\log m}\right)
\right)
=m^{o(1)}
\tag{10}
\]
gives (2)--(4).

### Why the angular hypothesis is sufficient

For points on the unit circle,
\[
\cos(k\theta)=\cos(l\theta)
\]
implies
\[
e^{ik\theta}=e^{il\theta}
\quad\text{or}\quad
e^{ik\theta}=e^{-il\theta}.
\]
The first alternative forces \(k=l\) among the assumed distinct angular
points.  For each \(k\), the second alternative determines at most one
\(l\).  Thus every chord value \(x_k\) occurs at most twice, exactly the
hypothesis of Theorem 1.  This proves (1).

## 3. A strict small-sumset structure theorem

The same energy proof records what an anomalously small sumset would have
to look like.

Let \(R\) be the number of ordered pairs \((k,l)\) such that
\[
k\ne l,\qquad x_k\ne x_l,\qquad
x_l-x_k\in\mathbb Z,\qquad
0<|x_l-x_k|\le(m-1)^2.
\tag{11}
\]
Only these pairs can contribute nontrivial cross-layer collisions, so the
refined energy estimate is
\[
\sum_y r(y)^2\le2mS+\tau_*(m)R.
\tag{12}
\]

### Theorem 2

If
\[
|A_m+X_S|\le K m\sqrt S,
\tag{13}
\]
then
\[
R\ge
\frac{mS}{\tau_*(m)}
\left(\frac{\sqrt S}{K}-2\right).
\tag{14}
\]
In particular, if \(\sqrt S\ge4K\), then
\[
R\ge
\frac{mS^{3/2}}{2K\tau_*(m)}.
\tag{15}
\]
Since \(R\le S^2\), a necessary condition for (13) in this range is
\[
m\le2K\tau_*(m)\sqrt S.
\tag{16}
\]

### Proof

Equation (13) and Cauchy–Schwarz give
\[
\sum_y r(y)^2
\ge\frac{(mS)^2}{Km\sqrt S}
=\frac{mS^{3/2}}K.
\]
Combine this with (12) and rearrange. \(\square\)

Thus, at \(m=S\), a fixed or subpolynomial \(K\) is impossible for all
sufficiently large \(m\).  This conclusion needs no algebraic
classification of the angle.

## 4. Algebraic certificate forced by any nontrivial collision

Put \(c=\cos\theta\), so
\[
x_k=2m^2(1-T_k(c)).
\]
Every pair counted by \(R\) supplies an exact relation
\[
2m^2\bigl(T_k(c)-T_l(c)\bigr)=n,
\qquad
n\in\mathbb Z,\quad0<|n|\le(m-1)^2.
\tag{17}
\]
Consequently \(c\) is a root of the nonzero integer polynomial
\[
P_{k,l,n}(z)
=2m^2(T_k(z)-T_l(z))-n.
\tag{18}
\]
It has degree at most \(S-1\).  The coefficient \(\ell^1\)-norm of
\(T_j\) is below \(3^j\), by the recurrence
\[
\|T_{j+1}\|_1\le2\|T_j\|_1+\|T_{j-1}\|_1.
\]
Hence
\[
H(P_{k,l,n})\le5m^2 3^S.
\tag{19}
\]

Here \(R\) counts ordered pairs.  Reversal identifies at most two of
them, so (15) supplies at least \(R/2\) unordered relations; no
algebraic independence among those relations is asserted.

This gives the requested strict structural conclusion beyond the
unconditional estimate (1):

> In the nontrivial regime \(\sqrt S\ge4K\), any bound at the
> \(Km\sqrt S\) scale forces the many exact Chebyshev relations counted
> in (15).  In particular \(c\) has algebraic degree at most \(S-1\) and
> logarithmic height \(O(S+\log m)\); its minimal polynomial divides
> every relation polynomial in (18).

The height statement uses the naive logarithmic coefficient height of
a primitive minimal polynomial.  It follows from (19) and the standard
factor-height inequality (equivalently, Mignotte's bound); the absolute
logarithmic Weil-height formulation has the same stated upper order
after the usual degree normalization.

Because the problem concerns exact cardinality, the conclusion is exact
algebraicity rather than merely approximate resonance.  A robust
small-neighbourhood version would require a separate Diophantine
approximation argument and is not proved here.

## 5. Four angle classes

### 5.1 Transcendental cosine

If \(c\) is transcendental, no nonconstant polynomial
\[
T_k(c)-T_l(c)-q,\qquad q\in\mathbb Q,
\]
can vanish.  No two distinct layers intersect and no two chord values
coincide.  Therefore the exact value is
\[
\boxed{|A_m+X_S|=mS.}
\tag{20}
\]
In particular, a nonzero algebraic \(\theta\) has transcendental cosine
by Lindemann–Weierstrass and lies in this full-expansion class.

The operative condition is transcendence of \(\cos\theta\), not merely
transcendence of \(\theta\): an angle of the form
\(\arccos(\alpha)\) can be transcendental while \(\alpha\) is algebraic.

### 5.2 High algebraic degree

If
\[
[\mathbb Q(c):\mathbb Q]\ge S,
\]
then the degree-\((S-1)\) relation (18) is impossible.  Again
\[
\boxed{|A_m+X_S|=mS.}
\tag{21}
\]
More generally, any loss from full expansion certifies an algebraic
degree below \(S\).

### 5.3 Roots of unity

Suppose \(e^{i\theta}\) is a root of unity of order \(q\).  Distinctness
of the first \(S\) angular points requires \(q\ge S\).  Chord values can
repeat through the symmetry \(k\leftrightarrow q-k\), but only twice, so
Theorem 1 applies without loss:
\[
|A_m+X_S|
\gg
\min\{mS,m^2/\tau_*(m)\}.
\tag{22}
\]
If the real cyclotomic degree of \(c\) is at least \(S\), (21) gives full
expansion.  In the remaining low-degree cases, any unusually small
sumset still forces the many rational chord-difference relations (17).
Thus root-of-unity resonance does not defeat the critical estimate (3).

### 5.4 General algebraic cosine

For algebraic \(c\) of degree below \(S\), no generic full-expansion claim
is made.  Nevertheless (1) remains unconditional.  If the sumset is at
the convex scale, Theorem 2 forces many integer values among
\[
2m^2(T_k(c)-T_l(c)),
\]
and the minimal polynomial of \(c\) must divide all corresponding
polynomials (18).  Rational cosines are a particularly rigid subcase:
the earlier \(p\)-adic arguments usually give \(m(S-O(\log m))\), but
they are no longer needed to reach the critical exponent.

## 6. Counterexample search and sharp boundary

The proof was pressure-tested against the deliberately resonant choice
\[
x_k=-k^2.
\]
Then \(A_m+\{x_k\}=A_m-A_S\) has many square-difference collisions.  The
same factorization (8) still controls their energy, and the exact verifier
confirms (5).  Thus simple integral resonance does not invalidate the
critical \(m^{2-o(1)}\) bound.

The estimate does rely on bounded multiplicity of the \(x_k\).  If one
drops distinctness of the angular points, all \(x_k\) may coincide and
the union can have only \(m\) elements.  This is the genuine degeneracy
excluded by the setup.  For distinct points, cosine symmetry permits
multiplicity two and no more.

## 7. Can this re-enter the inherited proof?

It immediately eliminates the **explicit critical anisotropic grid** as
a distance extremizer, for every admissible angle, not only rational or
nonresonant angles.

It does not yet close the inherited Erdős branch.  The theorem requires
all of the following on one subfamily:

1. \(m\) circles with one common radius;
2. consecutive, equally spaced heights producing exactly \(A_m\) after
   normalization;
3. the same \(S\)-term angular progression on every circle;
4. \(m=S=N^{2/5+o(1)}\), up to subpolynomial losses.

The inherited correlation analysis has not forced this rectangle.  In
particular, the earlier synchronization audit explicitly says that
aggregate popular angles need not occur on the same fibres, and arbitrary
equal-radius heights need not form a long arithmetic progression.

Therefore the correct implication is:
\[
\text{critical square-height synchronized slice}
\Longrightarrow D\ge N^{4/5-o(1)},
\]
not
\[
f_3(N)\ge N^{4/5-o(1)}.
\]

A viable next bridge would be an extraction theorem producing a long
arithmetic progression of heights and a common angular progression on the
same radius class with only subpolynomial losses.  Without that bridge,
the result is a strong structured-subcase theorem and an obstruction to
the proposed counterexample, not an unconditional exponent improvement.

## 8. Literature boundary

The general semiconvex input used earlier is Ruzsa and Solymosi,
[*Sumsets of Semiconvex Sets*](https://arxiv.org/abs/2008.08021).  It
records the general lower bound of order
\(|A||B|^{1/2}\) and examples limiting improvements without additional
arithmetic structure.  Theorem 1 above uses precisely the extra
factorization
\[
d^2-e^2=(d-e)(d+e)
\]
available for the square set.

A targeted search did not locate this exact bounded-multiplicity
square-translate formulation.  That is not a novelty determination: the
argument is elementary and may appear under additive-energy or divisor
language.  No stand-alone publication claim is made without a broader
literature audit and, more importantly, an inherited-proof extraction
theorem.

## 9. Verification

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_sumset_expansion.py
PYTHONDONTWRITEBYTECODE=1 pytest -q test_verify_sumset_expansion.py
```

The certificate checks:

- four rational nonperiodic cosines;
- three general algebraic quotient fields, including a degree-\(9\)
  full-expansion case;
- four exact cyclotomic fields;
- three adversarial integer square-shift instances.

Current certificate:

```text
e48128e422c757efed9475ed1124b7b4f4cd0542fb2cec36a994ecc9562e502a
```
