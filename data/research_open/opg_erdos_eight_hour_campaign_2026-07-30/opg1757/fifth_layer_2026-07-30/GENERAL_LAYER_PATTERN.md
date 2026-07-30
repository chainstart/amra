# General component-layer pattern and the remaining induction gap

Date: 2026-07-30

## 1. Exact falling-factorial structure

Put
\[
(x)_{\underline r}=x(x-1)\cdots(x-r+1).
\]
For every fixed \(r\ge0\), the finite Liu--Chow formulas imply that
there are rational polynomials \(A_r,B_r\) such that
\[
\boxed{
\mathcal C_{2r+3}(n)
=(n-4)_{\underline r}A_r(n)n^{2n-4r-8},
}                                                       \tag{1}
\]
\[
\boxed{
\mathcal C_{2r+4}(n)
=(n-4)_{\underline r}B_r(n)n^{2n-4r-10}.
}                                                       \tag{2}
\]
Moreover,
\[
\deg A_r=3r,\qquad \deg B_r=3r+2,
\]
and both have positive leading coefficient.

The subsequent finite-product \(u^3\) calculation now sharpens this
to the exact leading two terms
\[
A_r(n)=\frac4{(2r)!}\left(
n^{3r}+\frac{r(r+23)}2n^{3r-1}+O_r(n^{3r-2})
\right),
\]
\[
B_r(n)=\frac4{(2r+1)!}\left(
n^{3r+2}+\frac{r^2+23r+8}{2}n^{3r+1}
+O_r(n^{3r})
\right).
\]
This is proved for all \(r\) by finite-product elementary symmetric
sums and binomial moments, not inferred by interpolation.  See
`../sixth_layer_2026-07-30/LEADING_TWO_COEFFICIENTS_LEMMA.md`.

### Why the falling factor is forced

The support bounds are
\[
W_{1,c}=0\ (c>n-1),\qquad
W_{2,c}=0\ (c>n-2).
\]
Thus \(\mathcal C_t(n)=0\) for \(t>2n-2\).  For \(r\ge2\), this supplies
the roots
\[
n=4,5,\ldots,r+2
\]
in (1)--(2); the list is empty when \(r=0,1\).

For \(r\ge1\), the final root is \(n=r+3\); the relevant totals are
\(2n-3\) and \(2n-2\).  At total \(2n-2\),
\[
\mathcal C_{2n-2}=W_{1,n-1}^2-W_{0,n}W_{2,n-2}
=1-1=0.
\]
At total \(2n-3\), write \(M=\binom n2\).  The necessary top counts are
\[
W_{1,n-1}=1,\quad W_{1,n-2}=M-1,
\]
\[
W_{0,n}=1,\quad W_{0,n-1}=M,
\]
\[
W_{2,n-2}=1,\quad W_{2,n-3}=M-2.
\]
Therefore
\[
\mathcal C_{2n-3}=2(M-1)-M-(M-2)=0.
\]
These \(r\) integer roots force \((n-4)_{\underline r}\).

The normalized determinant
\[
n^{2t+2-2n}\mathcal C_t(n)
\]
is a rational polynomial, directly from the finite component formulas.
The fixed-\(t\) asymptotic
\[
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}+O_t(n^{2n-9})
\]
then gives the stated degrees and positive leading coefficients.

For \(3\le t\le12\), direct factorization shows something stronger:
after removing \((n-4)_{\underline r}\), the remainder has all positive
coefficients when shifted to the first nonzero integer \(n=r+4\).
This has now been verified for \(0\le r\le4\), but is not yet proved
uniformly in \(r\).

## 2. Exact general Newton template

Let \(d=q-q_0\) be the active depth and put
\[
n=n_0+d,\qquad n_0=q_0+4.
\]
Newton inversion is
\[
\frac{2a_{k,q_0+d}}{(k-2)!}
=\sum_{\ell=0}^{d}
(-1)^\ell\binom{n-4}{\ell}
\mathcal C_{t_d-2\ell}(n-\ell),                     \tag{3}
\]
where
\[
t_d=3+2d\quad(k\ {\rm odd}),\qquad
t_d=4+2d\quad(k\ {\rm even}).
\]

The falling factors align exactly:
\[
\binom{n-4}{\ell}
(n-\ell-4)_{\underline{d-\ell}}
=\frac{(n-4)_{\underline d}}{\ell!}.                 \tag{4}
\]
Consequently (3) becomes, in the odd case,
\[
\boxed{
\frac{2a_{k,q_0+d}}{(k-2)!(n-4)_{\underline d}}
=\sum_{\ell=0}^{d}
\frac{(-1)^\ell}{\ell!}
A_{d-\ell}(n-\ell)
(n-\ell)^{E_d+2\ell},
}                                                       \tag{5}
\]
with \(E_d=2n-4d-8\).  In the even case, replace \(A\) by \(B\) and
use \(E_d=2n-4d-10\).

Formula (5) explains all exact layers:

- \(d=0\): one term;
- \(d=1\): one adjacent gap;
- \(d=2\): one adjacent gap plus a final positive term;
- \(d=3\): two adjacent gaps;
- \(d=4\): two adjacent gaps plus a final positive term.
- \(d=5\): three adjacent gaps;
- \(d=6\): three adjacent gaps plus a final positive term.

## 3. Adjacent-gap mechanism

Pair the terms \(\ell=2j\) and \(\ell=2j+1\).  Once the common base
exponent is nonnegative, the pair is positive if the corresponding
remainder polynomials satisfy an inequality of the form
\[
(2j+1)R_{d-2j}(x)
>
R_{d-2j-1}(x-1)(x-1)^2,                             \tag{6}
\]
after the rational normalizations in \(R=A\) or \(B\) are included.
The factor \(2j+1\) comes from the adjacent factorials in (5).

For depths \(d\le6\), every needed version of (6) either becomes a
positive-coefficient shifted polynomial or admits a simple strengthened
ratio bound such as
\[
\left(1-\frac1n\right)^E\le\frac1{1+E/n}.
\]
This yields all-\(k\) positivity after finitely many exact boundary
values.

For fixed \(d\), the degree drop
\[
\deg R_{d-\ell}-\deg R_{d-\ell-1}=3
\]
while the base contributes only two powers.  Hence each negative term
is smaller than its preceding positive term by \(O_d(n^{-1})\).  This
recovers eventual positivity at every fixed depth.

## 4. What is still missing for induction

Equations (1)--(6) reduce an all-depth theorem to a precise algebraic
problem, but they do not solve it.  The missing input is a recurrence
or coefficientwise representation proving, uniformly in \(r\), that:

1. \(A_r(n)\) and \(B_r(n)\) are positive throughout the admissible
   region \(n\ge r+4\); and
2. every adjacent gap in (6) stays positive after the necessary base
   ratio is restored.

Positive leading coefficients prove only eventual positivity.  They
do not control the largest real root as \(r\) grows.  The fifth-layer
even first gap illustrates the issue: the crude ratio bound by \(1\)
produces a polynomial that remains negative over a substantial initial
range, although the exact gap is positive.  A sharper Bernoulli bound
repairs this fixed layer, but no uniform version has yet been proved.

Accordingly, the present work proves:

- all-\(k\) positivity for active depths \(0,1,2,3,4,5,6\); and
- eventual positivity for every fixed depth.

It does **not** yet justify arbitrary-depth positivity or a range
\(d\le c\sqrt{k}\).  Such a result requires uniform coefficient/root
bounds for \(A_r,B_r\), or a direct positive combinatorial
interpretation of the adjacent gaps.
