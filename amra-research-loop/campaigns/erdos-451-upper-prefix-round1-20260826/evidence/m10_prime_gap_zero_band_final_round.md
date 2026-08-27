# Final round: a prime-gap zero band for the weighted CRT tail

Date: 2026-08-27

Status: **proved, conditional only on the published Baker--Harman--Pintz
short-interval theorem.**  This is a polynomial-prefix theorem for the M10
positive dual.  It is not the density-scale joint-tail estimate and does not
prove Erdős 451 or improve its public exponent.

## 1. Input and notation

Retain the notation of `m10_discrete_spectral_norm_ledger_round3.md`.  Thus

\[
 f_\gamma(\ell)=\prod_i\phi_i(\gamma\ell),
 \qquad 0\leq\phi_i\leq1,
\]

where the product is over all primes `p_i=k+d_i` in `(k,2k)` when
`gamma=1`, and over all primes except `p_0=k+1` after its exact fibre
elimination when `gamma=p_0`.

The exact support calculation already proved in (21m)--(21o) of the ledger
says that, for `N>0`, a prime coordinate can be nonzero only if an integer
`q` satisfies

\[
                    2|N-qp|\leq p-k.                     \tag{1}
\]

For adjacent quotients `q` and `q+1`, put `t=2q+1`.  The open interval

\[
 G_t(N)=\left({2N-k\over t},{2N+k\over t}\right)         \tag{2}
\]

is a gap between their two support intervals.  Every prime in `G_t(N)`
violates (1), for every integer quotient, and hence annihilates
`f_gamma(ell)` when `N=gamma|ell|`.

The external input is Theorem 1 of R. C. Baker, G. Harman, and J. Pintz,
*The difference between consecutive primes, II*, Proc. London Math. Soc.
83 (2001), 532--562, DOI
`10.1112/S0024611501012692`.  With

\[
                         \theta={21\over40},              \tag{3}
\]

it asserts that, for every sufficiently large real `x`, the interval
`[x-x^theta,x]` contains a prime.

## 2. Quotient-gap zero-band theorem

### Theorem 2.1

For every sufficiently large `k`, every real/integer `N` in

\[
             12k\leq N\leq {1\over4}k^{,2-\theta}
                         ={1\over4}k^{59/40}              \tag{4}
\]

has a prime `p` in `(k,2k)` for which (1) fails for every integer `q`.
Moreover this prime lies in

\[
                     {23\over18}k<p<{25\over16}k.         \tag{5}
\]

Consequently

\[
 f_1(\ell)=0
 \quad\hbox{for}\quad
 12k\leq|\ell|\leq {1\over4}k^{59/40},                  \tag{6}
\]

and, if `p_0=k+1` was removed exactly,

\[
 f_{p_0}(\ell)=0
 \quad\hbox{for}\quad
 12\leq|\ell|\leq {k^{59/40}\over4p_0}.                 \tag{7}
\]

#### Proof

The real interval

\[
 \left[{4N\over3k},{3N\over2k}\right]                   \tag{8}
\]

has length `N/(6k)>=2`, so it contains an odd integer `t=2q+1`.
Set

\[
                x={2N\over t},\qquad w={k\over t}.       \tag{9}
\]

Then (8) gives

\[
                 {4k\over3}\leq x\leq{3k\over2}.        \tag{10}
\]

Also `w/x=k/(2N)<=1/24`, and hence

\[
 x-w\geq{4k\over3}{23\over24}={23k\over18}>k,
 \qquad
 x+w\leq{3k\over2}{25\over24}={25k\over16}<2k.         \tag{11}
\]

The upper bound in (4) and the lower bound in (10) give

\[
 w={kx\over2N}\geq {8\over3}k^\theta
     >x^\theta,                                         \tag{12}
\]

where the last inequality uses `x<=3k/2` and `theta<1`.
For large `k`, Baker--Harman--Pintz therefore supplies a prime

\[
                 p\in[x-x^\theta,x]\subset(x-w,x]
                                      \subset G_t(N).    \tag{13}
\]

This prime lies in `(k,2k)` by (11).  To check the support conclusion
directly, write `t=2q+1`.  Since `p` lies between `(2N-k)/t` and
`(2N+k)/t`, both nearest quotients `q,q+1` have
`2|N-jp|>p-k`; every other quotient is farther away.  This proves the first
claim.

For (6), take `N=|ell|`.  For (7), take `N=p_0|ell|`.
The prime from (5) cannot be the deleted `p_0=k+1`, so it is still a
coordinate of the reduced product.  Symmetry of every `phi_i` handles
negative `ell`.  This proves the theorem.  `square`

## 3. Additive-prefix consequence

Let

\[
 R_1=\left\lfloor{k^{59/40}\over4}\right\rfloor,
 \qquad
 R_{p_0}=\left\lfloor{k^{59/40}\over4p_0}\right\rfloor. \tag{14}
\]

The previous undilated argument bounded `|ell|<k` by `O(log k)`.  Bounding
the uncovered transition `k<=|ell|<12k` trivially and using (6) now gives

\[
 \sum_{|\ell|\leq R_1}
  \left(1-{ |\ell|\over h}\right)f_1(\ell)=O(k).         \tag{15}
\]

For the width-one reduced/dilated system, the finitely many frequencies
`|ell|<12` are bounded trivially and (7) gives

\[
 \sum_{|\ell|\leq R_{p_0}}
  \left(1-{ |\ell|\over H}\right)f_{p_0}(\ell)=O(1).    \tag{16}
\]

Both are polynomial additive errors, so they are affordable in (21e) of
the spectral ledger.  This is the first proved moving prefix for the
specific `p_0` dilation and a polynomial enlargement of the undilated
prefix.

## 4. Exact limit of the gain

The desired window is `h=exp(O(k/log k))`, while (14) is only polynomial.
For `N` above `k^(59/40)`, the quotient gaps have length below the available
uniform prime-gap scale.  The theorem gives no information on the remaining
sums

\[
 \sum_{R_1<|\ell|<h}f_1(\ell),\qquad
 \sum_{R_{p_0}<|\ell|<H}f_{p_0}(\ell).                  \tag{17}
\]

Replacing the exponent `21/40` by any published uniform prime-in-short-
interval exponent `theta<1` would change the zero band only to
`N<<k^(2-theta)`, still polynomial.  Thus uniform maximum-prime-gap input,
even conjecturally polylogarithmic gaps, cannot by itself reach the
subexponential density window.  A weighted average theorem across the many
sub-unit quotient gaps remains necessary.

## 5. Finite endpoint audit

`work/m10_round1/prime_gap_zero_band_check.py` uses exact rational endpoints.
Its frozen SHA-256 is
`761cd50f47a4c56103c0c21d61cad13336d3c5d5e576ca44d415d6bf477e6902`.
Under guard unit `openmath-task-20260827-085919-423138.scope`, it checked
278,583 sampled/all frequencies for `k=10000,20000,50000`.  Every selected
odd quotient gap contained an actual prime strictly inside its endpoints,
and that prime failed (1) for all nearest quotients.  Exit status was zero,
maximum RSS was 27,016 KiB, and swaps were zero.  This finite check audits
the algebra and rounding only; the universal asymptotic statement uses the
published theorem.
