# Growing cyclotomic fields at the full critical cross-plane-energy scale

Date: 2026-07-30

## 0. Outcome

The regular-prism family in
`GROWING_CYCLOTOMIC_CHART_EXTRACTION_NOGO.md` shows a local
low-complexity extraction failure, but has only \(t^3\) points and does
not test the full cross-plane value
\(\mathfrak C_{\rm plane}=t^{13-o(1)}\).

This note supplies the missing sharp **abstract representation-tensor
model**.  For every odd prime \(p\), it has
\[
\begin{aligned}
|\mathcal P|&=p^2,\\
|\mathcal D|&=\frac{p-1}{2}p^2=\Theta(p^3),\\
\max_{e,d}W_{e,d}&=p^4,\\
\sum_{e,d}W_{e,d}&=\Theta(p^8),\\
\mathfrak E_{\rm diag}&=\Theta(p^{12}),\\
\mathfrak C_{\rm plane}&=\Theta(p^{13}).
\end{aligned}
\tag{1}
\]
Every label has algebraic degree \((p-1)/2\), the label set is a
disjoint union of complete Galois orbits, and every orbit has
\(\Theta(p^{11})\) cross-plane energy.

Consequently the field-orbit inequality in
`CROSS_PLANE_GALOIS_ORBIT_TRICHOTOMY.md` is power-sharp and in fact
attains exact equality on this model.

This is not a Euclidean realization and not a counterexample to Erdős
#1083.  Its conclusion is methodological:

\[
\boxed{
N=t^5,\ D=t^3,\ \mathfrak C_{\rm plane}=t^{13},
\text{ and complete degree-}t\text{ cyclotomic labels}
}
\]
are mutually consistent as abstract critical data.  Ruling them out
requires a theorem using the Euclidean four-plane quadratic or its
coupling to the rotation reservoir.

## 1. Cyclotomic labels

Let \(p\ge5\) be an odd prime and put
\[
m=\frac{p-1}{2},\qquad
\zeta=e^{2\pi i/p},\qquad
a_d=2-\zeta^d-\zeta^{-d}
\quad(1\le d\le m).
\tag{2}
\]
The \(a_d\)'s are the complete Galois orbit of \(a_1\) in the maximal
real cyclotomic field
\[
L_p=\mathbb Q(\zeta+\zeta^{-1}),
\qquad [L_p:\mathbb Q]=m.
\tag{3}
\]

For
\[
0\le u<p^2,
\]
define
\[
\lambda_{d,u}=5u+a_d.
\tag{4}
\]
Since \(0<a_d<4\), the intervals
\[
(5u,5u+4)
\]
are disjoint.  Hence all \(mp^2\) labels in (4) are distinct.
Translation by the rational integer \(5u\) preserves the generated
field:
\[
\mathbb Q(\lambda_{d,u})=L_p.
\tag{5}
\]
For fixed \(u\), the set
\[
\mathcal O_u=\{\lambda_{d,u}:1\le d\le m\}
\tag{6}
\]
is one complete Galois orbit of size \(m\).  The full label set is the
disjoint union of the \(p^2\) orbits \(\mathcal O_u\).

The coefficient 5 is inessential; it only makes distinctness immediate.
The labels are modeled on a cyclotomic horizontal chord plus an
independent rational vertical contribution.

## 2. The critical tensor

Let the ordered plane-pair vertex set be
\[
\mathcal P=\mathbb F_p^2.
\tag{7}
\]
Index a vertex by \(e=(r,s)\).  Use the labels
\[
\mathcal D=\{(d,u):1\le d\le m,\ 0\le u<p^2\}.
\tag{8}
\]
Define
\[
\boxed{
W_{(r,s),(d,u)}
=
\begin{cases}
p^4,&u\equiv r\pmod p,\\
0,&\text{otherwise}.
\end{cases}
}
\tag{9}
\]

For one row, there are \(p\) choices of \(u\) in its residue class and
\(m\) choices of \(d\).  Thus
\[
\deg(e)=mp,\qquad
\sum_dW_{e,d}=mp^5.
\tag{10}
\]
For one label, \(r\) is fixed and \(s\) is arbitrary.  Hence
\[
k_d=p,\qquad S_d=p^5.
\tag{11}
\]
There are
\[
|\mathcal D|=mp^2
\tag{12}
\]
labels and
\[
mp^3
\tag{13}
\]
supported cells.

## 3. Exact energy ledger

The total representation mass is
\[
\boxed{
\sum_{e,d}W_{e,d}=mp^7=\Theta(p^8).
}
\tag{14}
\]
The individual-pair diagonal energy is
\[
\boxed{
\mathfrak E_{\rm diag}
=mp^3(p^4)^2
=mp^{11}
=\Theta(p^{12}).
}
\tag{15}
\]
The aggregate energy is
\[
\boxed{
\mathfrak E_{\rm all}
=mp^2(p^5)^2
=mp^{12}
=\Theta(p^{13}).
}
\tag{16}
\]
Therefore
\[
\boxed{
\mathfrak C_{\rm plane}
=mp^{11}(p-1)
=\Theta(p^{13}).
}
\tag{17}
\]

Every label has the same codegree:
\[
\boxed{
c_{d,u}
=p(p-1)(p^4)^2
=p^9(p-1)
=\Theta(p^{10}).
}
\tag{18}
\]
Equations (11) and (18) simultaneously attain the critical
heavy-label scales
\[
S_d=p^5,\qquad k_d=p,\qquad c_d=\Theta(p^{10}).
\tag{19}
\]

For one complete Galois orbit,
\[
\boxed{
C(\mathcal O_u)
=m p^9(p-1)
=\Theta(p^{11}).
}
\tag{20}
\]

## 4. Exact saturation of the field-orbit inequality

In the notation of the orbit theorem,
\[
R=m,\qquad
\mathfrak C_R=mp^{11}(p-1),\qquad
H_R=mp^9(p-1).
\tag{21}
\]
Consequently
\[
\boxed{
\frac{R\mathfrak C_R}{H_R}
=\frac{m\cdot mp^{11}(p-1)}
{mp^9(p-1)}
=mp^2
=|\mathcal D|.
}
\tag{22}
\]
Thus the inequality is exactly sharp, not merely sharp in its
exponents.

The mechanism is transparent.  There are \(p^2\) disjoint complete
orbits, every orbit contributes \(m=\Theta(p)\) labels, and every orbit
carries \(\Theta(p^{11})\) energy:
\[
p^2\cdot p=p^3,\qquad
p^2\cdot p^{11}=p^{13}.
\tag{23}
\]
High field degree supplies the factor \(p\) in the number of labels,
but the same factor appears in the energy of one orbit.  It therefore
does not create an exponent gain by itself.

## 5. Relation to the full \(N=p^5\) ledger

The inherited source subsystem has
\[
M=p,\qquad Q=p^3,\qquad S=MQ=p^4,
\tag{24}
\]
and hence \(p^2\) ordered plane-pair types and row mass of order
\(Q^2=p^6\).  Equations (7) and (10) match these exponents.  As in the
split-reservoir construction of
`RULED_STABILITY_EXTRACTION_ATTACK.md`, the remaining ambient mass can
be assigned to an abstract rotation reservoir so that the total point
ledger is \(N=p^5\).

This compatibility is only combinatorial.  The tensor (9) is not
asserted to be realized by Euclidean endpoints, and an arbitrary
rotation reservoir would normally create additional distances.  The
model therefore rules out only deductions from the aggregate ledger,
not deductions using Euclidean geometry.

## 6. The strongest honest conclusion

The critical data force the heavy-label conclusion
\[
c_d\ge p^{10-o(1)},\quad
S_d\ge p^{5-o(1)},\quad
k_d\ge p^{1-o(1)}
\tag{25}
\]
on a positive proportion of the energy.  For complete degree-\(p\)
orbits, a distance improvement follows if every orbit saves a fixed
power over
\[
C(\mathcal O)=p^{11+o(1)}.
\tag{26}
\]

The model proves that (26) is the exact barrier.  A future argument must
show that an actual Euclidean configuration cannot arrange
\(p^2\) cyclotomic orbits, each carrying \(p^{11-o(1)}\) codegree,
unless:

1. their endpoint equations synchronize into a low-complexity weighted
   chord chart;
2. their Galois/translate palette expands beyond \(p^{3+\delta}\)
   distance labels; or
3. their coefficients form a ruled Cartesian family, which can be
   discharged by direct distance expansion.

This is precisely the three-way Euclidean stability lemma stated at the
end of `CROSS_PLANE_GALOIS_ORBIT_TRICHOTOMY.md`.

## 7. Verification

`verify_cross_plane_galois_orbit_trichotomy.py` checks:

* the exact row, label, mass, and energy formulas (10)--(20);
* exact equality in (22);
* distinctness and degree of finite cyclotomic labels for small primes;
* the heavy-label and orbit inequalities.

The finite checks verify the algebra and guard the exponent ledger.  The
arbitrary-prime field statement follows from the standard description
of the maximal real prime cyclotomic field.
