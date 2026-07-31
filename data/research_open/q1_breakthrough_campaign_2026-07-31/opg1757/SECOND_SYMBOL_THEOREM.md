# OPG-1757: the universal second fixed-deficit symbol

Date: 2026-07-31

Status: `PROVED__ALL_Q__ALL_OFFSETS`

## 1. Statement

Put
\[
A(z)=1+2z+2z^2
\]
and
\[
M_q(z)=\sum_{r=0}^{2q}[s^{2q-1}]C_{q,r}(s)z^r.
\]
For every \(q\ge1\),
\[
\boxed{
M_q(z)=\frac4{q!}A(z)^{q-2}\,q\,P_q(z),
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_q(z)={}&4-\frac{2(q-10)}3z-(3q+4)z^2\\
&-2(2q+11)z^3-\frac{2(4q+29)}3z^4.
\end{aligned}
}
\tag{2}
\]
At \(q=1\), the apparent \(A^{-1}\) cancels exactly.  Together with the
leading-symbol theorem, (1) gives the uniform two-term expansion
\[
\sum_{r=0}^{2q}C_{q,r}(s)z^r
=\frac4{q!}A(z)^q s^{2q}
+\frac4{q!}A(z)^{q-2}qP_q(z)s^{2q-1}
+O_q(s^{2q-2}).
\tag{3}
\]

## 2. Endpoint expansion lemma

Write \(\rho=c-1\).  The zero-, one-, and two-marked Lagrange formulas in
`ENDPOINT_POLYNOMIALITY_THEOREM.md` imply
\[
Q_{h,e,c}=A_{e,c}s^{2c+2e-2}
\left(1+\frac{b_{h,e,c}}s
+\frac{g_h(e,\rho)}{s^2}
+\frac{j_h(e,\rho)}{s^3}+O(s^{-4})\right).
\tag{4}
\]
The filtered-ring theorem in `LAURENT_DEGREE_LEMMA.md` proves, at every
relative Laurent order \(k\),

\[
\deg_{e,\rho}q_{h,k}\le2k.
\]

Its coefficient-functional input is
\[
 \frac{(s-a)_d}{s^d}
 =\sum_{k=0}^d(-1)^k
 e_k(a,a+1,\ldots,a+d-1)s^{-k}.
\tag{5a}
\]
Here \(e_k(a,\ldots,a+d-1)\) is a polynomial in \((a,d)\) of total
degree at most \(2k\), while
\[
 \frac{[v^e]v^m e^{v/2}}{[v^e]e^{v/2}}
 =2^m(e)_m
\tag{5b}
\]
has degree \(m\).  The companion lemma gives the termwise filtration for
\(V^\rho\), the marked \(\rho J V^{\rho-1}\) term, the Euler operators,
and normalized \([v^e]\) extraction.  Consequently,
\[
\deg_{e,\rho}g_h\le4,
\qquad
\deg_{e,\rho}j_h\le6.
\tag{5}
\]
Only \(h=0,1,2\) occurs.  Therefore the triangular lattice
\(e+\rho\le6\), for each of the three values of \(h\), uniquely determines
both polynomials.  The already proved exact \(q=6\) endpoint table contains
this lattice and one extra boundary.  The extended verifier checks all
108 values of \(g_h\) and all 108 values of \(j_h\), exactly.  Together
with the proved degree lemma, the finite grid is an all-parameter
polynomial-identity certificate, not extrapolation in \(q\).

The stated unisolvence is elementary: repeated forward differences show
that a bivariate polynomial of total degree at most \(d\) which vanishes
at every nonnegative lattice point \(e+\rho\le d\) is zero.  All expansions
here are coefficientwise identities in formal Laurent series in \(s^{-1}\);
no analytic limit is taken.

The explicit \(g_h\) polynomial has 31 monomials and \(j_h\) has 64;
both are recorded verbatim in `verify_second_symbol_theorem.py`.  Keeping
them in the certificate avoids obscuring the proof with a 95-term display.

## 3. Third-order determinant collapse

Expand each overlap falling factorial through order \(s^{-3}\), insert
(4), form
\[
Q_{1,e,c}Q_{1,f,d}-Q_{0,e,c}Q_{2,f,d},
\]
and average an ordered endpoint pair with its transpose.  All terms of
total profile degree five and six cancel.  The surviving symmetric kernel
\[
K(e,\rho,f,\sigma,\ell)
\]
has total degree only four.  The verifier constructs it by exact rational
algebra; it has 111 nonzero monomials.

Let \(x\) mark
\[
q+1=\rho+e+\sigma+f+\ell,
\]
and let \(z\) mark the beta offset.  The five factorially weighted profile
variables are independent Poisson markers with means
\[
\mu_\rho=\mu_\sigma=\frac{x(1+z)}2,
\quad
\mu_e=\mu_f=\frac{xz(1+z)}2,
\quad
\mu_\ell=xz^2.
\tag{6}
\]
Replacing every ordinary power in \(K\) by its Touchard moment gives the
exact collapse
\[
\boxed{
4\mathbb E K
=-\frac{4x^2}{3}
\left(
8xz^4+12xz^3+9xz^2+2xz+33z^2+6z-12
\right).
}
\tag{7}
\]
The common Poisson exponential is \(e^{xA(z)}\).  Hence
\[
\sum_{q\ge1}M_q(z)x^{q+1}
=e^{xA(z)}\,4\mathbb E K.
\tag{8}
\]
Extracting \([x^{q+1}]\) from (7)--(8) and simplifying gives exactly
(1)--(2).

## 4. Verification and scope

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_second_symbol_theorem.py
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_second_symbol_theorem.py --extended-endpoints
```

The first command proves the degree-four symmetric-kernel and Touchard
moment identities.  The second additionally checks 216 endpoint Laurent
coefficients.  Both pass.

The algebraic collapse and all finite certificates pass.  The companion
`LAURENT_DEGREE_LEMMA.md` supplies the all-parameter step, so this is the
complete second asymptotic symbol.  It does not control all lower Laurent
orders uniformly when \(q\) grows with \(s\).
It therefore does not by itself prove a polynomial- or linear-width
positive window.
