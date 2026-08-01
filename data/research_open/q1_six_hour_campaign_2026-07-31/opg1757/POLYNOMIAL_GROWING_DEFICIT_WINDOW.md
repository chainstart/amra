# OPG-1757 candidate: a polynomially growing positive deficit window

Date: 2026-08-01

Status: **PENDING INDEPENDENT CROSS-AUDIT**

## 1. Candidate theorem

Retain

\[
 n=2s-5-q,\qquad
 C_{q,r}(s)=
 \frac{[\beta^{2n+r}]B_n(s,\beta)}
 {n!s^{2s-8-2q+r}}.
\tag{1}
\]

For every \(q\ge1\), every \(0\le r\le2q\), and every integer

\[
\boxed{s\ge2(4096q)^{67},}
\tag{2}
\]

one has

\[
\boxed{C_{q,r}(s)>0.}
\tag{3}
\]

Consequently, for every integer \(s\ge4\), all coefficients in the
natural support of the complete-split pooled disjoint-core
\(\alpha^2\) layer are simultaneously strictly positive throughout the
explicit polynomial window

\[
\boxed{
 0\le q\le\frac{s^{1/67}}{8192}.
}
\tag{4}
\]

The exponent \(1/67\) is deliberately crude.  Its importance is that it
is positive: this changes the proved window from logarithmic over
logarithmic to a power of \(s\).  No fixed-\(q\) scan is used.

The proof combines three already proved all-parameter facts:

1. endpoint polynomiality and the explicit endpoint height from
   UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md;
2. the all-Laurent-order parameter-degree theorem from the preceding
   campaign's LAURENT_DEGREE_LEMMA.md;
3. the exact positive leading symbol
   \[
   L_{q,r}:=[s^{2q}]C_{q,r}
   =\frac4{q!}[z^r](1+2z+2z^2)^q.
   \]

The earlier phrase “fix \(q\)” does not prevent diagonal use with
\(q=q(s)\).  For each integer \(q\), the master formula is an exact
polynomial identity on the explicit stable range \(s\ge6q+4\), and all
bounds below are uniform in \(q\).  Condition (2) implies that stable
range, so the identities may be applied simultaneously to every pair
\((s,q)\) in (4).

## 2. Quantitative endpoint Laurent lemma

Write \(c=\rho+1\), \(m=e+\rho\), and

\[
 Q_{h,e,\rho+1}(s)
 =A_{e,\rho}s^{2m}
 \left(1+\sum_{k\ge1}q_{h,k}(e,\rho)s^{-k}\right),
\qquad
 A_{e,\rho}=\frac1{2^m\rho!e!}.
\tag{5}
\]

Coefficients beyond the polynomial degree are zero.  The filtered-ring
lemma proves

\[
 q_{h,k}\in\mathbb Q[e,\rho],
\qquad \deg q_{h,k}\le2k.
\tag{6}
\]

We now make (6) quantitative.  For every \(k\ge1\), every \(h=0,1,2\),
and all nonnegative \(e,\rho\le q+1\),

\[
\boxed{
 |q_{h,k}(e,\rho)|
 \le W_k(q):=
 [128(k+1)]^{16k}q^{2k}.
}
\tag{7}
\]

To prove this, put \(d=2k\) and first evaluate \(q_{h,k}\) on the
triangular lattice \(e+\rho\le d\).  The coefficient of
\(s^{2m-k}\) in \(Q\) is \(A_{e,\rho}q_{h,k}(e,\rho)\).  The uniform
endpoint theorem gives

\[
 \lVert Q_{h,e,\rho+1}\rVert_1
 \le15(m+1)2^m(2m+4)^{2m}.
\tag{8}
\]

On this lattice,

\[
 A_{e,\rho}^{-1}=2^m\rho!e!
 \le2^d d!,
\]

and hence

\[
\begin{aligned}
 |q_{h,k}(e,\rho)|
 &\le
 15(d+1)2^{2d}d!(2d+4)^{2d}\\
 &\le[64(k+1)]^{12k}
 =:M_k.
\end{aligned}
\tag{9}
\]

The last inequality follows from \(d=2k\),
\(d!\le[2(k+1)]^{2k}\), and
\(15(d+1)\le[4(k+1)]^2\); all bases are enlarged to
\(64(k+1)\), and \(10k+2\le12k\).

For completeness, use bivariate Newton interpolation:

\[
 q_{h,k}(e,\rho)
 =\sum_{i+j\le d}
 \Delta_e^i\Delta_\rho^j q_{h,k}(0,0)
 \binom ei\binom\rho j.
\tag{10}
\]

Every mixed difference in (10) uses only lattice points
\(a+b\le i+j\le d\), so (9) bounds it by \(2^{i+j}M_k\).
There are at most \((d+1)^2\) terms.  At nonnegative
\(e,\rho\le q+1\),

\[
 \left|\binom ei\binom\rho j\right|
 \le(q+1)^{i+j}\le(q+1)^d.
\]

Thus

\[
 |q_{h,k}(e,\rho)|
 \le(d+1)^2 2^dM_k(q+1)^d.
\tag{11}
\]

Since \(q+1\le2q\) and \(d=2k\), enlarging the base in (11) from
\(64\) to \(128\) proves (7).  Explicitly, after removing the factor
\([64(k+1)]^{12k}q^{2k}\), the remaining multiplier is at most
\[
 (2k+1)^2\,2^{4k},
\]
whereas the enlargement to the right side of (7) supplies
\[
 2^{40k}(k+1)^{4k};
\]
the latter dominates for every \(k\ge1\).  This argument is all-\(k\):
the finite
lattice is used as an exact unisolvent set for the proved degree bound,
not as extrapolation.

## 3. The same loss bound for every falling factor

In every master profile,
\[
(e+\rho)+(f+\sigma)+\ell=q+1.
\tag{11a}
\]
Thus the endpoint arguments used in (7) really do satisfy
\(e,\rho,f,\sigma\le q+1\).

Put \(m_1=e+\rho\) and \(m_2=f+\sigma\).  The four falling shifts are
exactly
\[
 m_1+2,\qquad m_2+2,\qquad m_1+1,\qquad m_2+3.
\tag{11b}
\]
Moreover, natural support gives \(2\ell\le r\le2q\), hence
\(\ell\le q\).  Combining this with (11a), every relevant shift
\(A\) obeys
\[
 \ell(A+\ell)\le q(q+4)\le5q^2.
\tag{11c}
\]
Write

\[
 (s-A)_\ell=s^\ell\sum_{i=0}^{\ell}f_i(A,\ell)s^{-i}.
\tag{12}
\]

For \(i\ge1\),

\[
\begin{aligned}
 |f_i(A,\ell)|
 &\le\binom{\ell}{i}(A+\ell)^i\\
 &\le(5q^2)^i\\
 &\le[128(i+1)]^{16i}q^{2i}=W_i(q).
\end{aligned}
\tag{13}
\]

Put \(W_0(q)=1\).  Therefore each of the two endpoint series and each
of the two falling-factor series in a master summand has loss-\(i\)
coefficient bounded by \(W_i(q)\) relative to its leading coefficient.

For total loss \(K\ge1\), sum over the weak compositions
\(i_1+i_2+i_3+i_4=K\).  There are
\(\binom{K+3}{3}\le(K+1)^3\), and
\[
 \prod_{\nu=1}^4(i_\nu+1)^{16i_\nu}
 \le(K+1)^{16K}.
\]
Consequently the relative loss-\(K\) coefficient in either endpoint
product of one fixed profile is at most

\[
\boxed{
 U_K(q):=[256(K+1)]^{20K}q^{2K}.
}
\tag{14}
\]

## 4. Absolute profile mass versus the positive leading symbol

It remains to sum (14) over all endpoint profiles without losing a
factor exponential in \(q\).  Put

\[
 A(z)=1+2z+2z^2,\qquad
 a_{q,r}=[z^r]A(z)^q.
\tag{15}
\]

The leading endpoint weight is

\[
 A_{e,\rho}=\frac1{2^{e+\rho}\rho!e!}.
\]

Let \(y\) mark
\(\rho+e+\sigma+f+\ell=q+1\), and let \(z\) mark the beta offset.
The binomial sum over the selected
\(\lambda=(1+s\beta)\) degree contributes
\((1+z)^{\rho+e+\sigma+f}\).  One endpoint side therefore has EGF

\[
 \exp\left(\frac{y(1+z)}2\right)
 \exp\left(\frac{yz(1+z)}2\right)
 =\exp\left(\frac{y(1+z)^2}{2}\right).
\tag{16}
\]

Equivalently, before collapsing, the complete baseline sum is

\[
\sum_{\ell,\rho,e,\sigma,f\ge0}
\frac{
 y^{\ell+\rho+e+\sigma+f}
 z^{2\ell+e+f}
 (1+z)^{\rho+e+\sigma+f}
}{
 \ell!\,2^{\rho+e+\sigma+f}
 \rho!e!\sigma!f!
}.
\tag{16a}
\]

Thus no restriction from \(a\), \(r\), or the endpoint compositions is
being suppressed.  The two endpoint sides in (16a) give
\(e^{y(1+z)^2}\), and overlaps give \(e^{yz^2}\).  The sum of the
positive leading profile weights is exactly

\[
 [y^{q+1}z^r]e^{yA(z)}
 =\frac{[z^r]A(z)^{q+1}}{(q+1)!}.
\tag{17}
\]

The two determinant products have the same leading absolute weight.
Including their factor \(2\) and the marked-block factor \(4\), the
absolute baseline mass is

\[
 S_{q,r}
 =\frac8{(q+1)!}[z^r]A(z)^{q+1}.
\tag{18}
\]

We compare this with
\[
 L_{q,r}=\frac4{q!}a_{q,r}.
\]
Since

\[
 [z^r]A^{q+1}
 =a_{q,r}+2a_{q,r-1}+2a_{q,r-2},
\tag{19}
\]

it suffices to compare adjacent coefficients.  Interpret \(a_{q,r}\)
as the total weight of words of length \(q\) over \(\{0,1,2\}\), of
digit sum \(r\), with digit weights \(1,2,2\).  Map every word of sum
\(r-1\) to a word of sum \(r\) by incrementing its leftmost coordinate
which is less than two.  Such a coordinate exists for \(r\le2q\).
An image has at most \(q\) possible preimages (one decreased positive
coordinate), and its weight is at least that of every preimage: changing
\(0\) to \(1\) doubles the weight, while changing \(1\) to \(2\)
preserves it.  Hence

\[
 a_{q,r-1}\le q\,a_{q,r},
 \qquad
 a_{q,r-2}\le q^2a_{q,r},
\tag{20}
\]

where negative subscripts mean zero.  Equations (18)--(20) give

\[
\boxed{
 \frac{S_{q,r}}{L_{q,r}}
 \le\frac{2(1+2q+2q^2)}{q+1}
 \le10q.
}
\tag{21}
\]

This coefficientwise comparison is what prevents the profile summation
from reintroducing an exponential loss.

## 5. Root bound

Every master summand has apparent degree

\[
 2(e+\rho)+2(f+\sigma)+2\ell=2q+2.
\tag{22}
\]

The apparent losses zero and one cancel globally.  Write

\[
 C_{q,r}(s)
 =L_{q,r}s^{2q}
 +\sum_{k=1}^{2q}c_{q,r,k}s^{2q-k}.
\tag{23}
\]

The coefficient \(c_{q,r,k}\) occurs at loss
\(K=k+2\) from the apparent degree in (22).  Equations (14) and (21)
therefore imply

\[
 \frac{|c_{q,r,k}|}{L_{q,r}}
 \le10q\,[256(k+3)]^{20(k+2)}q^{2(k+2)}.
\tag{24}
\]

For \(1\le k\le2q\), one has
\(k+2\le3k\), \(k+3\le4k\le8q\).  Enlarging all bases gives the simple
geometric bound

\[
\boxed{
 \frac{|c_{q,r,k}|}{L_{q,r}}
 \le\{(4096q)^{67}\}^{k}.
}
\tag{25}
\]

Indeed, the bracketed factor in (24) costs at most
\((2048q)^{60k}\), the explicit \(q^{2(k+2)}\) costs at most
\((2048q)^{6k}\), and \(10q\le(2048q)^k\).

Let \(X_q=(4096q)^{67}\).  If \(s\ge2X_q\), then

\[
\begin{aligned}
 C_{q,r}(s)
 &\ge L_{q,r}s^{2q}
 \left(1-\sum_{k=1}^{2q}(X_q/s)^k\right)\\
 &>0,
\end{aligned}
\tag{26}
\]

because \(\sum_{k=1}^{2q}2^{-k}=1-2^{-2q}<1\).  This proves (2)--(3).
Finally, (4) implies
\[
 2(4096q)^{67}
 \le2(4096/8192)^{67}s<s,
\]
so (4) follows as well.  The stable combinatorial range
\(s\ge6q+4\) is absorbed by (2); at \(q=0\), the separately audited
identity \(C_{0,0}=4\) applies.

## 6. Scope and optimization firewall

The theorem proves a power-width window only for the complete-split
pooled disjoint-core \(\alpha^2\) layer.  It does not settle other pooled
layers or arbitrary-host OPG-1757.

No optimality is claimed for \(67\).  The large number comes from four
deliberate enlargements: endpoint lattice interpolation, a common bound
for endpoint and falling losses, four-factor convolution, and replacing
\(k\) by \(2q\).  Reducing it is worthwhile only after independent audit
of the qualitative power-width conclusion.

## 7. Audit checklist and exact domains

Until independent cross-audit is complete, the theorem status remains
PENDING.  The proof uses the following interfaces and no others.

1. **All-order endpoint interface.**  The inherited filtered-ring lemma
   applies to every \(k\ge1\), every \(e,\rho\ge0\), and all three
   markings \(h=0,1,2\), with the marking-dependent functional shift
   \(h+2\) already included.  It is used only to obtain (6).  Pooled
   inversion is not silently included in that lemma: the two endpoint
   factors and both pooled falling factors are separately bounded in
   Sections 3--5.
2. **What interpolation controls.**  Equation (10) first bounds Newton
   coefficients from triangular node values and then bounds the
   *point value* \(q_{h,k}(e,\rho)\) at each actual master profile.
   No claim that (11) directly equals a monomial coefficient norm is
   used.  Point-value control is exactly what the product expansion
   requires.
3. **Profile coefficient ratio.**  Equations (17)--(21) are independent
   of \(k\).  They apply for every \(q\ge1\) and every
   \(0\le r\le2q\), including \(r=0,2q\); negative coefficient
   subscripts in (19)--(20) are zero.  The master tail uses
   \(1\le k\le2q\), not merely \(k\le q\).
4. **Constant chain.**  The successive constants are
   \(64\) in the interpolation-node bound, \(128\) for one loss factor,
   \(256\) after four-factor convolution, \(2048\) in the simplified
   tail estimate, and \(4096\) in the final geometric majorant.
   The extra window divisor \(8192=2\cdot4096\) makes (4) strictly
   stronger than (2).
5. **Diagonal quantifier.**  The inherited master formula is available
   for every integer \(q\) with the common explicit condition
   \(s\ge6q+4\).  The proof never invokes an error term whose constant
   depends on a previously fixed \(q\); (2) absorbs the stable condition.

The executable verify_polynomial_window_bounds.py checks each finite
algebraic interface, exact profile mass, both beta boundaries, and all
integer constant inequalities on ranges far beyond those used by the
previous fixed-\(q\) certificates.  Those checks are regression and
falsification aids; the universal proof remains Sections 2--5.
