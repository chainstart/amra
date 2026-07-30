# Erdős #1083: partial cyclotomic fibre escape

Date: 2026-07-30

## 0. Outcome

The complete regular polygons in
`CYCLOTOMIC_TENSOR_ESCAPE_THEOREM.md` are not needed.  The same
cyclotomic independence argument survives when the angular support
changes arbitrarily from height to height.  The only synchronization
retained is that, at a fixed radius, every height is compared with one
anchored height layer.

For equal angular fibre size \(S\le (p+1)/2\), the resulting lower
bound is
\[
\boxed{
|\Delta^2(P)|\ge \left(1-\frac1S\right)|P|.
}
\tag{1}
\]
Thus a prime cyclotomic model cannot reach the \(N^{3/5+o(1)}\)
distance scale by deleting angles, permuting the angular supports
between heights, or using different height sets at different radii.

This is an exclusion theorem for a structured family, not an
unconditional improvement for Erdős #1083.  The inherited
common-axis branch has not been proved to contain the anchored
cyclotomic fibres assumed below.

## 1. Arbitrary angular supports

Let \(p\ge7\) be an odd prime and identify the angular indices with
\(\mathbb F_p\).  Let \({\cal R}\subset\mathbb R_{>0}\) be a finite
set of distinct radii satisfying
\[
r^2\in\mathbb Q\qquad(r\in{\cal R}).
\tag{2}
\]
For each \(r\), let \({\cal Z}_r\subset\mathbb R\) be a nonempty
finite set, put \(z_r^-=\min{\cal Z}_r\), and assume
\[
(z-z_r^-)^2\in\mathbb Q
\qquad
(z\in{\cal Z}_r).
\tag{3}
\]
At every occupied radius-height pair choose an arbitrary nonempty set
\[
{\cal A}_{r,z}\subseteq\mathbb F_p.
\tag{4}
\]
Define
\[
\boxed{
P=
\left\{
\left(
r\cos\frac{2\pi j}{p},
r\sin\frac{2\pi j}{p},
z
\right):
r\in{\cal R},\ z\in{\cal Z}_r,\ j\in{\cal A}_{r,z}
\right\}.
}
\tag{5}
\]
There is no requirement that the sets in (4) agree, be translates,
or be arithmetic progressions.

For each \(r,z\), let
\[
{\cal D}_{r,z}
=
{\cal A}_{r,z}-{\cal A}_{r,z_r^-}
\subseteq\mathbb F_p.
\tag{6}
\]
Write \(q_{r,z}\) for the number of equivalence classes
\[
\{d,-d\},\qquad d\in\mathbb F_p^\times,
\tag{7}
\]
which meet \({\cal D}_{r,z}\).

### Theorem 1 (partial-fibre escape)

The nonzero squared-distance set of (5) satisfies
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{r\in{\cal R}}\sum_{z\in{\cal Z}_r}q_{r,z}.
}
\tag{8}
\]
Consequently, if
\[
a_r=|{\cal A}_{r,z_r^-}|,
\qquad
s_{r,z}=|{\cal A}_{r,z}|,
\tag{9}
\]
then
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{r,z}
\left\lceil
\frac{\min(p,a_r+s_{r,z}-1)-1}{2}
\right\rceil .
}
\tag{10}
\]

### Proof

Put
\[
\zeta=e^{2\pi i/p},
\qquad
a_d=2-\zeta^d-\zeta^{-d}
\quad
\left(1\le d\le\frac{p-1}{2}\right).
\tag{11}
\]
Every nonzero sign class in (7) has a unique representative in
\(\{1,\ldots,(p-1)/2\}\).  For each class counted by \(q_{r,z}\),
choose this representative \(d\).  By (6), there are
\[
i\in{\cal A}_{r,z_r^-},
\qquad
j\in{\cal A}_{r,z}
\]
with \(j-i\equiv d\) or \(-d\pmod p\).  The corresponding two points
of \(P\) have squared distance
\[
\lambda(r,z,d)
=r^2a_d+(z-z_r^-)^2.
\tag{12}
\]

We claim that all selected values in (12) are different.  If
\[
r^2a_d+(z-z_r^-)^2
=s^2a_e+(w-z_s^-)^2,
\tag{13}
\]
then
\[
\begin{aligned}
0={}&
2r^2-2s^2+(z-z_r^-)^2-(w-z_s^-)^2\\
&-r^2(\zeta^d+\zeta^{-d})
+s^2(\zeta^e+\zeta^{-e})
\end{aligned}
\tag{14}
\]
is a rational relation among
\(1,\zeta,\ldots,\zeta^{p-1}\), supported on at most
\[
\{0,d,p-d,e,p-e\}.
\]
The only rational relation among these \(p\) powers is a scalar
multiple of
\[
1+\zeta+\cdots+\zeta^{p-1}=0.
\tag{15}
\]
Because the support in (14) has size at most five and \(p\ge7\),
all its coefficients vanish.

The representatives \(d,e\) lie in
\([1,(p-1)/2]\).  If \(d\ne e\), their two exponent pairs are
disjoint, and the coefficient at \(\zeta^d\) is
\(-r^2\ne0\), a contradiction.  Hence \(d=e\).  The same coefficient
then gives \(r^2=s^2\), so positivity and distinctness of the radii
give \(r=s\).  The constant coefficient gives
\[
(z-z_r^-)^2=(w-z_r^-)^2.
\]
Both \(z,w\ge z_r^-\), hence \(z=w\).  This proves injectivity and
(8).

It remains to estimate \(q_{r,z}\).  Cauchy--Davenport gives
\[
|{\cal D}_{r,z}|
\ge
\min(p,a_r+s_{r,z}-1).
\tag{16}
\]
After possibly deleting zero, every sign class contains at most two
elements.  Therefore
\[
q_{r,z}
\ge
\left\lceil
\frac{|{\cal D}_{r,z}|-1}{2}
\right\rceil,
\tag{17}
\]
and (10) follows from (16). \(\square\)

## 2. Linear-distance corollaries

### Corollary 2 (equal fibre size below half the polygon)

Suppose every angular fibre has the same cardinality \(S\), where
\[
2\le S\le\frac{p+1}{2}.
\tag{18}
\]
Then
\[
|P|=S\sum_r|{\cal Z}_r|
\]
and (10) gives
\[
\boxed{
|\Delta^2(P)|
\ge
(S-1)\sum_r|{\cal Z}_r|
=
\left(1-\frac1S\right)|P|.
}
\tag{19}
\]

The supports may be chosen independently at every height.  In
particular, random deletions or height-dependent rotations do not
evade the conclusion.

### Corollary 3 (complete fibres)

If every angular fibre is all of \(\mathbb F_p\), then
\[
q_{r,z}=\frac{p-1}{2}
\]
and Theorem 1 recovers
\[
|\Delta^2(P)|
\ge
\frac{p-1}{2}\sum_r|{\cal Z}_r|
=
\frac{p-1}{2p}|P|.
\tag{20}
\]

Thus the earlier complete-polygon theorem is one endpoint of the
partial-fibre statement.  The apparently smaller constant in (20)
comes from the fact that a full \(p\)-gon has only
\((p-1)/2\) unoriented chord lengths.

### Theorem 4 (base-field extension)

Let \(K\subset\mathbb R\) be a field of characteristic zero and assume
that the cyclotomic polynomial
\[
\Phi_p(X)=1+X+\cdots+X^{p-1}
\tag{21}
\]
is irreducible over \(K\).  In Theorem 1, replace the rationality
conditions (2)--(3) by
\[
r^2\in K,\qquad (z-z_r^-)^2\in K.
\tag{22}
\]
Then every conclusion (8)--(10), and hence Corollaries 2--3, remains
valid.

#### Proof

Only the injectivity argument changes.  An equality of two selected
labels again gives (14), now as a relation with coefficients in \(K\).
Its left side is a polynomial \(f(\zeta)\), where
\[
f\in K[X],\qquad \deg f\le p-1,
\]
and the support of \(f\) is contained in
\(\{0,d,p-d,e,p-e\}\).  Since the minimal polynomial of \(\zeta\)
over \(K\) is \(\Phi_p\), either \(f=0\) or
\(f=c\Phi_p\) for some \(c\in K\).  The latter is impossible:
\(\Phi_p\) has all \(p\) coefficients nonzero, whereas \(f\) is
supported on at most five exponents and \(p\ge7\).  Thus all
coefficients of \(f\) vanish.  The original proof now gives, in
order,
\[
d=e,\qquad r^2=s^2,\qquad r=s,\qquad z=w.
\]
The Cauchy--Davenport part is independent of the coefficient field.
\(\square\)

For a number field \(K\), irreducibility in (21) is equivalent to
\[
K\cap\mathbb Q(\zeta_p)=\mathbb Q.
\tag{23}
\]
In particular, it holds for all but finitely many primes \(p\).
For completeness, put
\[
K_{\rm ab}=K\cap\mathbb Q^{\rm ab}.
\]
This is a finite abelian extension of \(\mathbb Q\), so
Kronecker--Weber gives an integer \(m\) with
\(K_{\rm ab}\subseteq\mathbb Q(\zeta_m)\).  Since
\(\mathbb Q(\zeta_p)/\mathbb Q\) is abelian, the intersection
\(K\cap\mathbb Q(\zeta_p)\) is contained in \(K_{\rm ab}\).  If
\(p\nmid m\), then
\[
\mathbb Q(\zeta_p)\cap\mathbb Q(\zeta_m)=\mathbb Q:
\]
indeed, any nontrivial subfield of the prime-conductor field has
conductor divisible by \(p\), whereas every subfield of
\(\mathbb Q(\zeta_m)\) has conductor supported on the primes dividing
\(m\).  Thus (23) holds for every prime \(p\nmid m\), leaving only
finitely many possible exceptions.

Thus the linear-distance escape is not a peculiarity of rational
radius and height data: it persists over every fixed real number
field for all sufficiently large prime angular orders.

### Corollary 5 (unequal fibres)

For arbitrary fibre sizes, put
\[
N=\sum_{r,z}s_{r,z}.
\]
Then the explicit lower bound (10) remains valid without a common
size.  In particular, whenever
\[
a_r+s_{r,z}\le p+1
\]
for every \(r,z\),
\[
|\Delta^2(P)|
\ge
\sum_{r,z}
\left\lceil\frac{a_r+s_{r,z}-2}{2}\right\rceil.
\tag{24}
\]
This exposes the only loss caused by using one anchored layer:
fibres much larger than their anchor are charged only through the
sum of the two cardinalities.

## 3. Exact scope and remaining gap

The rational-base version of the theorem requires:

1. angular coordinates from one prime \(p\)-th root-of-unity group;
2. rational squared radii and rational anchored squared height
   differences, or more generally values in a real field over which
   \(\Phi_p\) is irreducible; and
3. one nonempty anchor layer at the minimum height of each radius.

It does **not** require complete polygons, common angular supports,
common height sets, equal fibre sizes, or arithmetic progressions.

The primality assumption is essential to this formulation.  For
angular group \(\mathbb Z/8\mathbb Z\), the support
\[
\{0,2,4,6\}
\]
is a square: it has only two nonzero chord lengths, whereas the
prime-group formula \(S-1\) would predict three.  Algebraically,
if \(a_d=2-\zeta_8^d-\zeta_8^{-d}\), then
\[
a_2=2,\qquad a_4=4,\qquad 1\cdot a_2=\frac12a_4.
\]
Thus both the Cauchy--Davenport step and the selected-label
injectivity can fail at composite order.  A composite-order version
would require a Kneser stabilizer loss and a separate chord-character
independence hypothesis.

The argument does not prove that a general low-distance point set
contains even one large prime-cyclotomic fibre.  Its precise role in
the critical proof tree is to eliminate a broader candidate for the
high-degree obstruction:
\[
\boxed{
\text{growing cyclotomic degree plus angular desynchronization}
\not\Rightarrow
\text{few Euclidean distances}
}
\]
inside the anchored coaxial model.

To convert this exclusion into an exponent improvement, one still
needs an inverse theorem forcing either such an anchored fibre, a
low-complexity number-field chart, or another directly expandable
Euclidean structure.

## 4. Verification

`verify_partial_cyclotomic_fibre_escape.py` uses exact rational
coefficient vectors modulo \(\Phi_p\).  Its test cases have:

- different angular sets at every height;
- unequal angular fibre sizes;
- different height counts at different radii; and
- nonintegral rational squared radii and height differences.

The verifier checks the exact difference-class count, the
Cauchy--Davenport lower bound, and injectivity of every selected label.
These finite checks audit the indexing; the unbounded result is the
proof above.
