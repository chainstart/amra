# Independent audit: all-rank leading coefficient and sign

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

The identities
\[
e_r=-6(r-1)c_{r-1}
\]
and
\[
(-1)^nA_n>0
\]
correctly upgrade the ordinary-symbol degree bound to
\[
\deg P_r=3r,\qquad
(-1)^r[d^{3r}]P_r(d)>0
\]
for every \(r\ge0\).  The direction of the log-convexity and
convolution inequalities is correct.

## 1. Defect-four Bell closure

For one phase jet of index \(p\ge2\), its pole defect relative to the
\(p=1\) baseline is
\[
(p-1)+\mathbf1_{2\mid p}.
\]
Thus defect at most four permits only:

- \(p=2,3\), with at most two occurrences;
- \(p=4,5\), with at most one occurrence; and
- amplitude derivative order at most five.

These are exactly the bounds enumerated by
`verify_md2_laurent_identity.py`.  Gamma rank \(k\) lowers the
available integral rank by \(k\), so it has baseline defect at least
\(3k\).  Therefore only Gamma rank one can occur through defect four:
its constant jet enters defect three and its linear \(W\)-jet enters
defect four.  Gamma ranks at least two cannot contribute.

For the small endpoint \(r=2\), some symbolic configurations have a
formally negative \(p=1\) multiplicity.  Their falling-factorial
ratio contains a zero factor, so they vanish automatically; they do
not create spurious small-rank contributions.

The 24 main and five exceptional configurations give four cancelled
layers followed by
\[
\frac{e_r}{K_r}
=-\frac{36r(r-1)}
{(6r-7)(6r-5)(6r-1)}
=-6(r-1)\frac{c_{r-1}}{K_r}.
\]
This verifies both the constant and sign in
\[
e_r=-6(r-1)c_{r-1}.
\]

## 2. Highest central layer

Every central-recurrence contribution with determinant rank \(a<n\)
has pole order at most
\[
3a-5+2(n-a)<3n-5.
\]
Hence only the undifferentiated \(G_n(1/2,t)\) term reaches the
highest Laurent layer.  With
\[
c_r=[W^{-3r}]C_{0,r},\quad
d_r=[W^{-(3r-2)}]\delta_r,\quad
e_r=[W^{-(3r-4)}]\varepsilon_r,
\]
the complete rank convolution gives
\[
A_n=\sum_{a+b=n}(d_ad_b-c_ae_b).
\]
Substitution of the formula for \(e_b\) is exactly
\[
A_n=[z^n]\left(D(z)^2+6zC(z)\theta C(z)\right).
\]
No derivative or lower determinant rank can cancel this layer.

The leading coefficient of the depth polynomial is therefore
\[
[d^{3r}]P_r(d)=\frac{A_{r+2}}{2(3r)!}.
\]
The factor \(1/2\) comes from the symbol formula and \(t^{-4}\) has
value one at the pole \(t=1\).

## 3. Sign substitution

Define
\[
p_r=(-1)^{r+1}c_r>0,\qquad
q_r=(-1)^rd_r=\frac{6r}{6r-5}p_r>0.
\]
Then
\[
C(-z)=1-P(z),\qquad D(-z)=Q(z),
\]
and consequently
\[
(-1)^nA_n
=[z^n]\left(Q(z)^2+6z(1-P(z))\theta P(z)\right).
\]
With \(m=n-1\), symmetry of the convolution gives
\[
[z^m]P\theta P=\frac m2[z^m]P^2,
\]
so
\[
(-1)^nA_n
=[z^n]Q^2+6mp_m-3m[z^m]P^2.
\]

## 4. Log-convexity and convolution direction

The successive ratio is
\[
\rho_r=\frac{p_{r+1}}{p_r}
=\frac{(6r+3)(6r+1)(6r-1)}
{9(2r+2)(2r+1)}.
\]
Its exact increment is
\[
\rho_{r+1}-\rho_r
=\frac{36r^2+108r+37}{6(r+1)(r+2)}>0.
\]
Thus \(p_r\) is strictly log-convex, not log-concave.

For fixed \(m\), put \(f_a=p_ap_{m-a}\).  When
\(1\le a<(m-1)/2\),
\[
\frac{f_{a+1}}{f_a}
=\frac{\rho_a}{\rho_{m-a-1}}\le1.
\]
Hence the products decrease from the endpoint toward the centre, and
the endpoint product \(p_1p_{m-1}\) is the maximum.  The inequality
direction used in the theorem is therefore correct:
\[
[z^m]P^2
\le(m-1)p_1p_{m-1}.
\]
Moreover
\[
\frac{(m-1)p_1p_{m-1}}{p_m}
=\frac{3(m-1)(2m)(2m-1)}
{2(6m-3)(6m-5)(6m-7)}
<\frac12
\quad(m\ge2).
\]
The strict inequality follows by pairing the three numerator factors
with \(6m-3\), \(6m-5\), and \(6m-7\), respectively.  Therefore
\[
[z^m]P^2<\frac12p_m.
\]
Substitution gives
\[
(-1)^nA_n
>[z^n]Q^2+\frac92mp_m>0.
\]
For \(n=2\), \(m=1\) and the \(P^2\) coefficient is zero, so the same
conclusion holds separately.

## 5. Scope of the certificates

`verify_leading_coefficient_sign_identity.py` checks the two rational
identities used in the ratio and endpoint bounds with symbolic
\(r,m\).  Its finite rank records are redundant.

`verify_md2_laurent_identity.py` performs the finite-defect Bell
enumeration with the rank left symbolic.  That is an all-rank
identity because the valuation argument proves that configurations
outside the enumerated defect set cannot reach the relevant Laurent
layer.  It is not an interpolation from low ranks.
