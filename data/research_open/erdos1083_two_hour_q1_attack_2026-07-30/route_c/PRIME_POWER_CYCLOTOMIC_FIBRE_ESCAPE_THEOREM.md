# Erdős #1083: prime-power cyclotomic fibre escape

Date: 2026-07-30

## 0. Outcome and status

The prime-order partial-fibre theorem extends to every angular order
\[
m=p^a,\qquad p\ge 7\text{ prime},\quad a\ge 1.
\]
This includes a genuinely composite family.  The algebraic reason is
that every nonzero rational relation among the \(m\)-th roots of unity
uses at least \(p\) roots, whereas equality of two selected squared
distances uses at most five.  Kneser's theorem replaces
Cauchy--Davenport and records the exact loss caused by periodic angular
supports.

For equal nonempty angular fibre size \(S\ge2\), the unconditional
consequence is
\[
\boxed{
 |\Delta^2(P)|
 \ge
 \frac{p-1}{2p}|P|.
}
\tag{1}
\]
The constant is sharp: one fibre supported on the order-\(p\)
subgroup is a regular \(p\)-gon and has exactly \((p-1)/2\) nonzero
distances.
If every anchored difference set is aperiodic, the stronger prime-like
bound survives:
\[
\boxed{
 |\Delta^2(P)|\ge\left(1-\frac1S\right)|P|.
}
\tag{2}
\]

This closes the prime-power part of the composite-order gap left by the
prime theorem.  It is a rigorous structured-family exclusion theorem,
not an unconditional improvement of the \(N^{3/5}\) bound in dimension
three.  General low-distance sets have not yet been proved to contain
the coaxial fibres assumed below.

## 1. Configuration and notation

Fix \(m=p^a\), where \(p\ge7\) is prime.  Identify angular indices with
\(G=\mathbb Z/m\mathbb Z\).  Let \({\cal R}\subset\mathbb R_{>0}\) be
a finite set of distinct radii satisfying
\[
r^2\in\mathbb Q\qquad(r\in{\cal R}).
\tag{3}
\]
For each \(r\), let \({\cal Z}_r\subset\mathbb R\) be a nonempty finite
set, put \(z_r^-=\min{\cal Z}_r\), and assume
\[
(z-z_r^-)^2\in\mathbb Q
\qquad(z\in{\cal Z}_r).
\tag{4}
\]
At each occupied radius-height pair choose an arbitrary nonempty set
\[
{\cal A}_{r,z}\subseteq G.
\tag{5}
\]
Define
\[
P=
\left\{
\left(
r\cos\frac{2\pi j}{m},
r\sin\frac{2\pi j}{m},
z
\right):
r\in{\cal R},\ z\in{\cal Z}_r,\ j\in{\cal A}_{r,z}
\right\}.
\tag{6}
\]

For each \(r,z\), put
\[
{\cal D}_{r,z}
=
{\cal A}_{r,z}-{\cal A}_{r,z_r^-}\subseteq G
\tag{7}
\]
and let \(q_{r,z}\) be the number of nonzero unoriented classes
\[
\{d,-d\},\qquad d\in G\setminus\{0\},
\tag{8}
\]
which meet \({\cal D}_{r,z}\).  Since \(m\) is odd, each class in (8)
has exactly two elements.

Write
\[
H_{r,z}=\operatorname{Stab}({\cal D}_{r,z})
=
\{h\in G:{\cal D}_{r,z}+h={\cal D}_{r,z}\}
\tag{9}
\]
and
\[
L_{r,z}
=
|{\cal A}_{r,z}+H_{r,z}|
+|{\cal A}_{r,z_r^-}+H_{r,z}|
-|H_{r,z}|.
\tag{10}
\]

## 2. Short rational relations at prime-power order

### Lemma 1 (relation-space basis)

Let \(\zeta=e^{2\pi i/m}\) and \(q=p^{a-1}\).  The rational relations
among
\[
1,\zeta,\ldots,\zeta^{m-1}
\tag{11}
\]
form a \(q\)-dimensional vector space with basis
\[
\sum_{k=0}^{p-1}\zeta^{\,u+kq}=0,
\qquad 0\le u<q.
\tag{12}
\]
Consequently, every nonzero rational relation among the powers in
(11) has support at least \(p\).

#### Proof

The \(q\) relations in (12) hold because \(\zeta^q\) is a primitive
\(p\)-th root of unity.  Their supports are disjoint, so they are
linearly independent.  On the other hand,
\[
\dim_{\mathbb Q}\ker
\left[
\mathbb Q^m\longrightarrow\mathbb Q(\zeta),\
(c_j)\longmapsto\sum_jc_j\zeta^j
\right]
=m-\varphi(m)
=p^a-(p-1)p^{a-1}
=q.
\tag{13}
\]
Thus (12) is a basis.  In any linear combination of these basis
relations, the coefficients are constant on each disjoint coset
\[
\{u,u+q,\ldots,u+(p-1)q\}.
\]
If the relation is nonzero, at least one such coset contributes all
\(p\) of its elements to the support. \(\square\)

### Corollary 2 (five-term rigidity)

For \(p\ge7\), a rational relation among the powers in (11) supported
on at most five exponents is the zero relation.

The threshold is intrinsic to this argument.  For \(p=5\), each
relation in (12) itself has support five, so five-term rigidity is
false.

## 3. Main theorem

### Theorem 3 (prime-power partial-fibre escape)

The nonzero squared-distance set of \(P\) satisfies
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{r\in{\cal R}}\sum_{z\in{\cal Z}_r}q_{r,z}.
}
\tag{14}
\]
Moreover,
\[
\boxed{
q_{r,z}
\ge
\left\lceil\frac{L_{r,z}-1}{2}\right\rceil,
}
\tag{15}
\]
and hence
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{r,z}
\left\lceil\frac{L_{r,z}-1}{2}\right\rceil.
}
\tag{16}
\]

#### Proof

For \(1\le d\le(m-1)/2\), put
\[
a_d=2-\zeta^d-\zeta^{-d}.
\tag{17}
\]
Every nonzero sign class meeting \({\cal D}_{r,z}\) has a unique
representative \(d\) in this interval.  Select one such representative
from each of the \(q_{r,z}\) classes.  By (7), two points in the
corresponding anchor and fibre realize the nonzero squared distance
\[
\lambda(r,z,d)
=r^2a_d+(z-z_r^-)^2.
\tag{18}
\]

We show that all selected labels (18), across all radii, heights, and
sign classes, are distinct.  Suppose
\[
r^2a_d+(z-z_r^-)^2
=
s^2a_e+(w-z_s^-)^2.
\tag{19}
\]
After expanding \(a_d,a_e\), this is a rational relation among the
\(m\)-th roots of unity supported inside
\[
\{0,d,m-d,e,m-e\},
\tag{20}
\]
a set of size at most five.  Corollary 2 says every coefficient in the
collected relation is zero.

If \(d\ne e\), uniqueness of the representatives makes
\(\{d,m-d\}\) and \(\{e,m-e\}\) disjoint.  The coefficient of
\(\zeta^d\) is then \(-r^2\ne0\), a contradiction.  Thus \(d=e\).
The same coefficient gives \(r^2=s^2\), and positivity of the radii
gives \(r=s\).  The constant coefficient then gives
\[
(z-z_r^-)^2=(w-z_r^-)^2.
\]
Both heights lie above the common anchor \(z_r^-\), so \(z=w\).
This proves injectivity and (14).

It remains to count classes.  Kneser's theorem applied to
\({\cal A}_{r,z}-{\cal A}_{r,z_r^-}\) and its stabilizer (9) gives
\[
|{\cal D}_{r,z}|\ge L_{r,z}.
\tag{21}
\]
After zero is discarded, every sign class contains at most two
elements.  Therefore
\[
q_{r,z}
\ge
\left\lceil
\frac{|{\cal D}_{r,z}|-1}{2}
\right\rceil
\ge
\left\lceil
\frac{L_{r,z}-1}{2}
\right\rceil,
\tag{22}
\]
which proves (15)--(16). \(\square\)

## 4. Consequences

### Corollary 4 (equal fibre size, arbitrary periodicity)

Suppose every angular fibre has the same cardinality \(S\ge2\).  Then
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{p-1}{2p}|P|.
}
\tag{23}
\]

#### Proof

Fix one anchored difference set and write \(H=H_{r,z}\),
\(h=|H|\).  If \(H=\{0\}\), Kneser's theorem gives
\[
|{\cal D}_{r,z}|\ge2S-1,
\]
and hence \(q_{r,z}\ge S-1\ge (p-1)S/(2p)\).

Suppose \(H\ne\{0\}\).  Every nontrivial subgroup of
\(\mathbb Z/p^a\mathbb Z\) has order at least \(p\), so \(h\ge p\).
Put \(c=\lceil S/h\rceil\).  Each of
\({\cal A}_{r,z}+H\) and
\({\cal A}_{r,z_r^-}+H\) is a union of at least \(c\) \(H\)-cosets.
Therefore
\[
L_{r,z}\ge(2c-1)h,\qquad S\le ch.
\tag{24}
\]
By (15),
\[
\begin{aligned}
\frac{q_{r,z}}S
&\ge
\frac{(2c-1)h-1}{2ch}\\
&\ge
\frac{h-1}{2h}
\ge
\frac{p-1}{2p}.
\end{aligned}
\tag{25}
\]
Since
\[
|P|=S\sum_r|{\cal Z}_r|,
\]
summing over the fibres proves (23). \(\square\)

The constant in (23) is attained by taking one radius, one height, and
one coset of the unique order-\(p\) subgroup as the angular support.
The resulting point set is a regular \(p\)-gon.

### Corollary 5 (aperiodic anchored differences)

Suppose every fibre has size \(S\ge2\) and
\[
\operatorname{Stab}({\cal D}_{r,z})=\{0\}
\qquad\text{for all }r,z.
\tag{26}
\]
Then
\[
\boxed{
|\Delta^2(P)|
\ge
\left(1-\frac1S\right)|P|.
}
\tag{27}
\]

#### Proof

Now (10) gives \(L_{r,z}=2S-1\), so (15) gives
\(q_{r,z}\ge S-1\).  Sum over all fibres. \(\square\)

Condition (26) automatically forces \(2S-1\le m\); otherwise the
Kneser lower bound could not fit inside \(G\).

### Corollary 6 (complete fibres)

If every fibre equals \(G\), then
\[
q_{r,z}=\frac{m-1}{2}
\]
and
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{m-1}{2m}|P|.
}
\tag{28}
\]

### Corollary 7 (base-field extension)

Let \(K\subset\mathbb R\) be a characteristic-zero field such that
\(\Phi_{p^a}\) is irreducible over \(K\).  If the rationality
conditions (3)--(4) are replaced by
\[
r^2\in K,\qquad (z-z_r^-)^2\in K,
\tag{29}
\]
then Theorem 3 and Corollaries 4--6 remain valid.

#### Proof

An equality (19) gives a polynomial \(f\in K[X]\) of degree below
\(m\), supported on at most five exponents, with \(f(\zeta)=0\).
Irreducibility implies
\[
f(X)=h(X)\Phi_{p^a}(X),
\qquad
\deg h<p^{a-1}.
\tag{30}
\]
Here
\[
\Phi_{p^a}(X)
=1+X^{p^{a-1}}+\cdots+X^{(p-1)p^{a-1}}.
\tag{31}
\]
For each nonzero coefficient \(h_u\), the resulting \(p\) monomials
occupy the single residue class \(u\bmod p^{a-1}\); distinct
coefficients of \(h\) occupy distinct residue classes.  Hence no two
such \(p\)-term blocks overlap or cancel.  Thus every nonzero product
in (30) has support at least \(p\ge7\), contradicting the five-term support of
\(f\).  Hence \(f=0\), and the proof of Theorem 3 applies
coefficientwise. \(\square\)

## 5. Sharpness, scope, and the remaining 1083 bridge

The factor in (23) cannot in general be replaced by the prime-order
factor \(1-1/S\).  If \(A=B=H\) is a subgroup of odd order \(S\), then
\[
A-B=H
\quad\text{and}\quad
q=\frac{S-1}{2}.
\tag{32}
\]
Thus the stabilizer loss in (15) is real.

The theorem removes two features that were previously bundled into the
prime hypothesis:

1. algebraic injection survives because prime-power root relations have
   minimum support \(p\); and
2. additive expansion survives with the exact Kneser stabilizer loss.

It does not extend to arbitrary composite \(m\).  For example, order
eight has the cross-radius collision
\[
a_2=2,\qquad a_4=4,\qquad 1\cdot a_2=\tfrac12a_4.
\tag{33}
\]
Nor does this theorem extract a prime-power angular orbit from an
arbitrary point set.

For Erdős #1083, the still-missing implication is an inverse theorem of
the form
\[
\boxed{
\text{critical cross-plane distance reuse}
\Longrightarrow
\begin{cases}
\text{a large anchored prime-power fibre},\\
\text{a bounded-complexity chart},\\
\text{or another directly expanding Euclidean structure}.
\end{cases}
}
\tag{34}
\]
The present theorem makes the first terminal in (34) rigorous for all
prime-power angular orders with least prime \(p\ge7\).

## 6. Verification

`verify_prime_power_cyclotomic_escape.py` performs exact rational
quotient-ring checks for orders \(7,49,121\), including:

- the \(p^{a-1}\) disjoint relation basis and its support threshold;
- selected-label injection across radii and heights;
- periodic and aperiodic Kneser ledgers; and
- the failure of five-term rigidity at \(p=5\).

`test_verify_prime_power_cyclotomic_escape.py` turns these checks into a
regression test.  The finite audit checks the algebra and indexing; the
unbounded assertions are proved above.
