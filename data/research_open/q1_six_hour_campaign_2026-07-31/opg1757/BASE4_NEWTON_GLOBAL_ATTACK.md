# OPG-1757: base-four Newton global attack

Date: 2026-08-01
Status: **CONJECTURAL GLOBAL SIGN; EXACT REDUCTION AND FINITE EVIDENCE**

## 1. The bold target

Put \(m_q=\lfloor q/2\rfloor\).  Exact layers through \(q=6\) suggest

\[
 \boxed{
 C_{q,r}(s)=\sum_{j=m_q}^{2q}\gamma_{q,r,j}
 \binom{s-4}{j},\qquad \gamma_{q,r,j}>0.
 }
\tag{1}
\]

If (1) held for every \(q,r\), it would be far stronger than the current
power-width theorem.  Indeed, every actual nonzero pooled depth has
\(q\le2s-7\), hence \(m_q\le s-4\); the first active term in (1) would
already be strictly positive and all later Newton terms nonnegative.
Thus (1) would settle the entire complete-split pooled disjoint-core
\(\alpha^2\) layer at once.  It is not claimed here.

The zero range in (1) is not conjectural.  The inherited
`BOUNDARY_FACTOR_THEOREM.md`, combined with the later denominator
cancellation \(R_{q,r}=s^rC_{q,r}\), gives

\[
 (s-4)_{\underline{m_q}}\mid C_{q,r}(s).
\tag{2}
\]

Indeed, the inherited theorem gives divisibility of \(R_{q,r}\), and
its factor has only the nonzero roots \(4,5,\ldots\); it is therefore
coprime to \(s^r\).  Euclid's lemma gives (2) in \(\mathbb Q[s]\).

Equivalently,

\[
 \Delta_s^j C_{q,r}(4)=0\qquad(0\le j<m_q).
\tag{3}
\]

Thus the open content is precisely strict positivity at and above the
first active Newton order.

## 2. The first active Newton order is positive for every \(q\)

This first step of the bold target is already a theorem.  Define

\[
 N_{q,j}(z)=\sum_{r=0}^{2q}\Delta^jC_{q,r}(4)z^r.
\tag{3a}
\]

Because of (3), at \(j=m_q\) the forward difference contains only its
last value:

\[
 \Delta^{m_q}C_{q,r}(4)=C_{q,r}(4+m_q).
\tag{3b}
\]

If \(q=2m+1\), then \(s=4+m\) makes the pooled depth equal to \(2\).
Substitution of the inherited exact formula

\[
 B_2(s,\beta)=4\beta^4(1+2\beta)^{2s-6}
 (1+s\beta)^{2s-8}
\]

into the normalization gives the manifestly positive closed form

\[
\boxed{
 N_{2m+1,m}(z)
 =2(m+4+2z)^{2m+2}(1+z)^{2m}.
}
\tag{3c}
\]

If \(q=2m\), the same boundary point has pooled depth \(3\).  The
inherited all-\(s\) coefficientwise positivity theorem for \(B_3\), whose
nonzero support is every degree from \(6\) through \(4s-10\), gives

\[
\boxed{
 N_{2m,m}(z)
 =\frac{s^{2m+6}}{6z^6}B_3(s,z/s)
 >_{\rm coeff}0,qquad s=m+4.
}
\tag{3d}
\]

The quotient in (3d) is a polynomial because \(\beta^6\mid B_3\).  It
also includes \(m=0\), where \(B_3(4,\beta)=24\beta^6\) and
\(N_{0,0}=4\).  Consequently

\[
\boxed{
 \gamma_{q,r,\lfloor q/2\rfloor}>0
 \quad\text{for every }q\ge0, 0\le r\le2q.
}
\tag{3e}
\]

This is an exact all-deficit milestone, not finite extrapolation.  The
next active order has the equally exact reduction

\[
 \gamma_{q,r,m_q+1}
 =C_{q,r}(5+m_q)-(m_q+1)C_{q,r}(4+m_q).
\tag{3f}
\]

Thus its two parity classes are normalized coefficientwise comparisons
of \(B_4\) against \(B_2\), and of \(B_5\) against \(B_3\), respectively.
The inherited separate positivity of \(B_2,\ldots,B_5\) does not by
itself prove these differences positive.  The exact formulas nevertheless
give strong finite evidence: `verify_second_active_newton_probe.py` checks
all 1,023 coefficients in (3f) through \(q=31\), with no zero or negative
case.  This scan is not used as a universal proof.

## 3. Exact profile EGF for the attack

Write \(c=\rho+1\), \(m=e+\rho\), and define the active endpoint

\[
 R^{(\ell)}_{h,e,\rho}(s)
 :=(s-h-m-1)_{\ell}Q_{h,e,\rho+1}(s).
\tag{4}
\]

The four apparently different master shifts are all instances of (4).
Put

\[
 F_h^{(\ell)}(s;x,z)
 :=\sum_{e,\rho\ge0}R^{(\ell)}_{h,e,\rho}(s)
 \{x(1+z)\}^{e+\rho}z^e.
\tag{5}
\]

Summing the exact master formula first over the beta offset and then over
the deficit gives the formal identity

\[
\boxed{
 \sum_{q\ge0}x^{q+1}\sum_r C_{q,r}(s)z^r
 =4\sum_{\ell\ge0}\frac{(xz^2)^\ell}{\ell!}
 \left\{
 (F_1^{(\ell)})^2-F_0^{(\ell)}F_2^{(\ell)}
 \right\}.
}
\tag{6}
\]

Indeed, endpoint conservation gives
\((e+\rho)+(f+\sigma)+\ell=q+1\), while summing the selected
\(\lambda\)-degree gives
\(z^{2\ell+e+f}(1+z)^{e+\rho+f+\sigma}\).  Thus (6) retains every
profile, binomial factor, overlap factorial, marking, and beta offset.

Formula (6) is the cleanest current entry for a sign-preserving proof.
It isolates the only negative operation in the Rayleigh determinant.

## 4. Newton linearization is positive

For any polynomial \(P\), write

\[
 P(s)=\sum_u p_u\binom{s-4}{u},
 \qquad p_u=\Delta^uP(4).
\]

Products in this basis have positive structure constants:

\[
 \binom{x}{u}\binom{x}{v}
 =\sum_{j=\max(u,v)}^{u+v}
 \frac{j!}{(j-u)!(j-v)!(u+v-j)!}\binom{x}{j}.
\tag{7}
\]

Therefore all multiplication and the overlap sum in (6) preserve signs.
The remaining obstacle is a coefficientwise Rayleigh inequality for the
aggregate determinant in (6), not a problem with the Newton product.

The boundary factor makes the same reduction still sharper.  Set

\[
 C_{q,r}(s)=(s-4)_{\underline{m_q}}D_{q,r}(s).
\tag{8}
\]

Then

\[
 \gamma_{q,r,m_q+k}
 =\frac{(m_q+k)!}{k!}
 \Delta^kD_{q,r}(4+m_q).
\tag{9}
\]

Hence (1) is equivalent to ordinary forward-difference positivity of the
reduced quotient starting at its first admissible point.  At that point
the pooled depth is \(2\) for odd \(q\) and \(3\) for even \(q\).

## 5. Exact evidence and the barrier

The frozen exact layers \(q=0,\ldots,6\) contain 455 base-four Newton
coefficients:

- 364 are strictly positive;
- 91 are zero;
- none is negative;
- the zeros are exactly \(j<\lfloor q/2\rfloor\), with no exceptions.

There is an endpoint-level positive cone as well.  Across all 108 frozen
\(q=6\) endpoints and every \(0\le\ell\le6\), the active factors (4)
have 5,695 positive, 4,385 zero, and no negative base-four Newton
coefficients.

This endpoint cone alone is insufficient.  Direct checks find negative
Newton coefficients in individual determinant profiles, in transposed
profile pairs, and even after summing all profiles at a fixed overlap
\(\ell\).  Positivity appears only after the complete overlap/profile
convolution in (6).

The smallest example already forces this conclusion.  At \(q=1,r=2\),
the complete \(\ell=0\) contribution is
\(-4(9s-28)\), whose base-four Newton row is \((-32,-36)\).  The
\(\ell=1\) contribution is \(8(s^2-s-7)\), with row \((40,64,16)\);
only their sum \(4(s-2)(2s-7)\) is Newton-positive.  Thus discarding or
bounding overlaps separately cannot prove (1).

A valid proof therefore needs one of:

1. a sign-preserving injection after the overlap sum;
2. a Gram/sum-of-squares representation of the full determinant kernel;
3. a coefficientwise TP2 theorem for the aggregated active-endpoint
   transform, stronger than pointwise Rayleigh positivity.

`verify_base4_newton_probe.py` reproduces the two exact censuses.  They
are evidence and route selection only, not a proof of (1).
