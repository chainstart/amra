# Erdős #1083: rough-order cyclotomic fibre escape

Date: 2026-07-30

## 0. Outcome and provenance

The rational-coefficient part of
`PRIME_POWER_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md` extends from
prime-power angular order to every
\[
\boxed{\gcd(m,30)=1,\qquad m>1.}
\tag{1}
\]
Equivalently, every prime divisor of \(m\) is at least seven.  The
new algebraic input is a direct corollary of H. B. Mann's classical
theorem on irreducible rational relations between roots of unity; the
Mann theorem itself is not new.

Let \(\ell\) be the least prime divisor of \(m\).  For equal angular
fibre size \(S\ge2\), the resulting sharp uniform bound is
\[
\boxed{
|\Delta^2(P)|\ge\frac{\ell-1}{2\ell}|P|.
}
\tag{2}
\]
The constant is attained by one fibre supported on the order-\(\ell\)
subgroup, which is a regular \(\ell\)-gon.

This is a broader structured-family exclusion theorem for the
Erdős--1083 proof tree.  It does not extract such a fibre from an
arbitrary low-distance set and does not improve the unconditional
\(N^{3/5}\) exponent in dimension three.

## 1. Mann's short-relation consequence

Let
\[
P_k=\prod_{\substack{q\le k\\q\ {\rm prime}}}q.
\tag{3}
\]
Mann's theorem states that if
\[
\sum_{j=1}^s c_j\omega_j=0,\qquad c_j\in\mathbb Q^\times,
\tag{4}
\]
is irreducible, meaning that no nonempty proper subsum vanishes, then
every quotient \(\omega_i/\omega_j\) has order dividing \(P_s\).
See H. B. Mann, *On linear relations between roots of unity*,
Mathematika **12** (1965), 107--117,
[doi:10.1112/S0025579300005210](https://doi.org/10.1112/S0025579300005210).

### Lemma 1 (five-term rigidity at rough order)

Let \(\zeta\) be a primitive \(m\)-th root of unity and assume (1).
If a rational relation
\[
\sum_{e\in E}c_e\zeta^e=0,\qquad c_e\in\mathbb Q^\times,
\tag{5}
\]
has distinct exponents modulo \(m\) and \(|E|\le5\), then \(E\) is
empty.

#### Proof

If (5) is nonempty, choose an irreducible vanishing subsum with
\(s\le5\) terms.  Mann's theorem says that the quotient of any two
roots in this subsum has order dividing
\[
P_s\mid P_5=2\cdot3\cdot5=30.
\]
The same quotient is an \(m\)-th root of unity.  By (1), its order
divides \(\gcd(m,30)=1\), so the quotient is one.  This contradicts
the distinctness of the selected exponents. \(\square\)

For \(m=p^a\), \(p\ge7\), the elementary disjoint-\(p\)-gon relation
basis in `PRIME_POWER_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md` proves the
same lemma without Mann's theorem.

## 2. Configuration

Identify the angular indices with
\(G=\mathbb Z/m\mathbb Z\).  Let
\({\cal R}\subset\mathbb R_{>0}\) be a finite set of distinct radii
with
\[
r^2\in\mathbb Q.
\tag{6}
\]
For each \(r\), let \({\cal Z}_r\subset\mathbb R\) be finite and
nonempty, put \(z_r^-=\min{\cal Z}_r\), and assume
\[
(z-z_r^-)^2\in\mathbb Q
\qquad(z\in{\cal Z}_r).
\tag{7}
\]
Choose arbitrary nonempty angular supports
\({\cal A}_{r,z}\subseteq G\), independently at every radius and
height, and put
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
\tag{8}
\]

Define
\[
{\cal D}_{r,z}
=
{\cal A}_{r,z}-{\cal A}_{r,z_r^-},
\qquad
H_{r,z}=\operatorname{Stab}({\cal D}_{r,z}),
\tag{9}
\]
and let \(q_{r,z}\) be the number of nonzero sign classes
\(\{d,-d\}\) meeting \({\cal D}_{r,z}\).  Since \(m\) is odd, every
nonzero sign class has two elements.  Finally, put
\[
L_{r,z}
=
|{\cal A}_{r,z}+H_{r,z}|
+|{\cal A}_{r,z_r^-}+H_{r,z}|
-|H_{r,z}|.
\tag{10}
\]

## 3. Rough-order escape theorem

### Theorem 2

For the configuration (8),
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{r,z}q_{r,z}
\ge
\sum_{r,z}
\left\lceil\frac{L_{r,z}-1}{2}\right\rceil.
}
\tag{11}
\]

#### Proof

Write \(\zeta=e^{2\pi i/m}\) and
\[
a_d=2-\zeta^d-\zeta^{-d},
\qquad 1\le d\le\frac{m-1}{2}.
\tag{12}
\]
For every nonzero sign class counted by \(q_{r,z}\), select its unique
representative \(d\) in the interval in (12).  The corresponding
anchor-to-fibre pair realizes the squared-distance label
\[
\lambda(r,z,d)
=r^2a_d+(z-z_r^-)^2.
\tag{13}
\]

If two selected labels agree, expansion of (13) gives a rational
relation among powers of \(\zeta\) supported inside
\[
\{0,d,m-d,e,m-e\}.
\tag{14}
\]
Lemma 1 makes this relation identically zero.  If \(d\ne e\), the two
sign pairs are disjoint and the coefficient of \(\zeta^d\) is
\(-r^2\ne0\), a contradiction.  Hence \(d=e\); coefficient comparison
then gives \(r^2=s^2\), so \(r=s\), and finally
\[
(z-z_r^-)^2=(w-z_r^-)^2.
\]
The two heights are at or above the same minimum anchor, hence \(z=w\).
All labels (13) are therefore distinct, proving the first inequality
in (11).

Kneser's theorem gives
\[
|{\cal D}_{r,z}|\ge L_{r,z}.
\tag{15}
\]
Discarding zero and quotienting by sign loses at most a factor two,
so
\[
q_{r,z}
\ge
\left\lceil
\frac{|{\cal D}_{r,z}|-1}{2}
\right\rceil
\ge
\left\lceil
\frac{L_{r,z}-1}{2}
\right\rceil.
\tag{16}
\]
Summing proves (11). \(\square\)

## 4. Sharp uniform consequences

### Corollary 3 (equal fibres)

If every angular fibre has the same size \(S\ge2\), then (2) holds.

#### Proof

Fix \(r,z\), write \(H=H_{r,z}\), and let \(h=|H|\).  If \(H\) is
trivial, Kneser gives
\[
|{\cal D}_{r,z}|\ge2S-1,
\qquad q_{r,z}\ge S-1
\ge\frac{\ell-1}{2\ell}S.
\tag{17}
\]

If \(H\) is nontrivial, every prime divisor of \(h\) divides \(m\),
so \(h\ge\ell\).  Put \(c=\lceil S/h\rceil\).  Both sumsets with
\(H\) in (10) contain at least \(c\) \(H\)-cosets, and therefore
\[
L_{r,z}\ge(2c-1)h,\qquad S\le ch.
\tag{18}
\]
Equations (11) and (18) give
\[
\frac{q_{r,z}}S
\ge
\frac{(2c-1)h-1}{2ch}
\ge
\frac{h-1}{2h}
\ge
\frac{\ell-1}{2\ell}.
\tag{19}
\]
Summing over the \(|P|/S\) fibres proves (2). \(\square\)

To see sharpness, use one radius and one height and take the unique
order-\(\ell\) subgroup of \(G\) as the angular support.  The resulting
regular \(\ell\)-gon has \(\ell\) points and exactly
\((\ell-1)/2\) nonzero distances.

### Corollary 4 (aperiodic fibres)

If every fibre has size \(S\ge2\) and every
\({\cal D}_{r,z}\) is aperiodic, then
\[
\boxed{
|\Delta^2(P)|\ge\left(1-\frac1S\right)|P|.
}
\tag{20}
\]

### Corollary 5 (complete fibres)

If every angular fibre is all of \(G\), then
\[
\boxed{
|\Delta^2(P)|\ge\frac{m-1}{2m}|P|.
}
\tag{21}
\]

## 5. Exact boundary

The arithmetic condition (1) is a sufficient condition matched to the
five-term geometry.  If \(2\), \(3\), or \(5\) divides \(m\), Mann's
theorem no longer rules out a short relation: the embedded regular
\(p\)-gon relation has \(p\le5\) terms.  This observation marks the
limit of the proof, not a claim that the distance injection fails at
every such order.  The special coefficient signs in (14) may permit
further cases; those cases require a separate classification.

There are genuine failures at some excluded orders.  At \(m=8\),
\[
a_2=2,\qquad a_4=4,
\]
so the choices \((r^2,d)=(1,2)\) and
\((s^2,e)=(1/2,4)\) collide.

The coefficient-field extension from the prime-power theorem is not
asserted here.  Mann's theorem in the form used above is rational, and
irreducibility of \(\Phi_m\) over a larger field alone does not give
the same sparse-multiple description for arbitrary composite \(m\).

## 6. Role in the #1083 proof tree

The theorem excludes arbitrary deletions, rotations, and periodic
angular supports throughout every \(30\)-coprime cyclotomic order,
provided the radii and anchored height squares are rational.  Thus the
candidate obstruction
\[
\boxed{
\text{rough composite cyclotomic order plus angular desynchronization}
\not\Rightarrow
\text{few Euclidean distances}
}
\tag{22}
\]
is now eliminated inside the anchored coaxial model.

The missing bridge remains an extraction theorem from critical
cross-plane reuse to one of:

1. a large anchored rough-order fibre;
2. a bounded-complexity coefficient chart; or
3. another Euclidean structure with a direct expansion theorem.

## 7. Verification

`verify_rough_order_cyclotomic_escape.py` uses exact SymPy quotient-ring
arithmetic for the non-prime-power orders \(77,91,143\), checks
selected-label injection across radii and heights, verifies periodic
Kneser sharpness, compares the general quotient representation with the
elementary order-\(49\) representation, and records the \(m=35\)
five-term boundary relation.

`test_verify_rough_order_cyclotomic_escape.py` provides regression
coverage.  These finite checks audit the algebra and indices; Mann's
theorem and the proof above supply the unbounded statement.
