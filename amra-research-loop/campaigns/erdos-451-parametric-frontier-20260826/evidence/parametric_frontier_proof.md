# Parametric frontier theorem for the van Doorn--Tang method

## Frozen input

Fix

\[
\frac25<\theta<\frac35
\]

and assume `PI(theta)`, the short-prime-interval input used in van Doorn--Tang:
there is a constant `C_theta>0` such that the integer-base intervals needed in
their Sections 2--6 contain at least

\[
C_\theta\frac{x^\theta}{\log x}
\]

primes for all sufficiently large bases `x`.  We use their Theorem 4.1 with an
absolute implied constant.  This dangerous uniformity point was checked against
the pinned public Lean theorem: it uses one explicit `c6`, built from fixed
numeric constants and independent of `r`; see `theorem41_uniformity_audit.md`.
No claim outside the source paper's theta range is made here.

## Theorem A (attaining side)

For every fixed `theta` and `c` satisfying

\[
\frac25<\theta<\frac35,\qquad 0<c<\frac{1-\theta}{3}, \tag{A1}
\]

and `PI(theta)`, there exists `k0=k0(theta,c)` such that, for every integer
`k>=k0` and every integer

\[
2k<n\leq\exp\!\left(c\frac{(\log k)^2}{\log\log k}\right), \tag{A2}
\]

the product `(n-k)(n-k+1)...(n-1)` has a prime divisor

\[
p\in(k,k+3k^\theta). \tag{A3}
\]

In particular, because `theta<1`, after increasing `k0` we have
`k+3k^theta<2k`, so `p in (k,2k)` and

\[
n_k>\exp\!\left(c\frac{(\log k)^2}{\log\log k}\right). \tag{A4}
\]

For `theta=21/40`, Baker--Harman--Pintz supplies the prime input used by the
source paper.  Hence (A4) holds unconditionally for every

\[
c<\frac{1-21/40}{3}=\frac{19}{120}. \tag{A5}
\]

The strict inequality in (A5) means the theorem gives each fixed
`c=19/120-epsilon`, not the endpoint `c=19/120` itself.

## Proof of Theorem A

Only the large-`n` range in Section 6 changes.  The source proofs of the small,
medium, and medium-large ranges use no occurrence of the final constant `c`;
they cover, respectively,

\[
(2k,\tfrac12k^{2-\theta}],\quad
(\tfrac12k^{2-\theta},k^2/\log^2 k],\quad
(k^2/\log^2 k,\tfrac12k^{2+\theta}].
\]

Their hypotheses `2/5<theta<3/5` and `PI(theta)` are retained unchanged, as is
their output interval `(k,k+3k^theta)`.

Assume now

\[
\frac12 k^{2+\theta}<n\leq\exp(cL^2/l),
\qquad L=\log k,\quad l=\log\log k. \tag{A6}
\]

Let `r` be the least positive integer such that

\[
n r!\leq k^{r+\theta}. \tag{A7}
\]

The lower inequality in (A6) makes (A7) false for `r=2`, so `r>=3`.

Choose a fixed `epsilon>0` so small that

\[
3(c+\epsilon)<1-\theta. \tag{A8}
\]

Let `R=ceil((c+epsilon)L/l)`.  Since

\[
\log(R!)\leq R\log R=O_{c,\epsilon}(L)=o(L^2/l),
\]

we get

\[
\log(nR!)-(R+\theta)L
\leq -\epsilon L^2/l+O_{c,\epsilon}(L)<0. \tag{A9}
\]

Thus (A7) holds at `R`, and

\[
3\leq r\leq R\leq(c+\epsilon+o(1))L/l. \tag{A10}
\]

In particular `r<=k^(1-theta)/2` for large `k`, as required by Theorem 4.1.

Define

\[
u_r=1-(1-\theta)\frac{2r-1}{3r-2},\qquad
\lambda^r=\frac{k^{r+u_r}}{nr!}. \tag{A11}
\]

Because

\[
u_r-\theta=(1-\theta)\frac{r-1}{3r-2}>0,
\]

(A7) implies `lambda>=1`.  The first two terms in Theorem 4.1 are exactly

\[
\left(\frac{nr!\lambda^r}{k^{r+1}}\right)^{1/(2r-1)}
=\left(\frac{k^{r+\theta}}{nr!\lambda^r}\right)^{1/(r-1)}
=k^{-(1-\theta)/(3r-2)}. \tag{A12}
\]

By (A8)--(A10), there is a fixed `delta>0` such that both terms in (A12) are

\[
O((\log k)^{-1-\delta})=o(1/\log k), \tag{A13}
\]

uniformly in `n` in (A6).

Minimality of `r` gives

\[
n(r-1)!>k^{r-1+\theta}. \tag{A14}
\]

Combining (A11) and (A14),

\[
\lambda^r<\frac{k^{1+u_r-\theta}}r<k^2. \tag{A15}
\]

For the third term `T3`, this gives

\[
T_3=\left(\frac{(r+1)\lambda}{k}\right)^{1/(2r)}
\leq (r+1)^{1/(2r)}k^{-1/(2r)+1/r^2}. \tag{A16}
\]

If `3<=r<=5`, the right-hand side has a fixed negative power of `k`.  If
`r>=6`, then `-1/(2r)+1/r^2<=-1/(3r)`; also, uniformly for `r<=R`, large `k`
gives `r+1<=k^(1/6)`.  Hence

\[
T_3\leq k^{-1/(4r)}\leq k^{-1/(4R)}
       \leq(\log k)^{-1/(4(c+\epsilon))+o(1)}. \tag{A17}
\]

The frozen range and (A1) give `c<(1-theta)/3<1/5`, and epsilon can also be
chosen with `c+epsilon<1/4`.  Therefore (A17) is `o(1/log k)`.

For the additive term, (A15) gives

\[
r\lambda<r k^{h_\theta(r)},\qquad
h_\theta(r)=\frac{1+(1-\theta)(r-1)/(3r-2)}r. \tag{A18}
\]

The function `h_theta(r)` decreases for `r>=3`: `1/r` decreases, and the
derivative of `(r-1)/(r(3r-2))` has numerator
`-3r^2+6r-2<0`.  Thus

\[
h_\theta(r)\leq h_\theta(3)=\frac{9-2\theta}{21}<\theta, \tag{A19}
\]

where the last inequality follows from `theta>2/5>9/23`.  Since `r=O(L/l)`,
(A18)--(A19) imply

\[
r\lambda=o(k^\theta/\log k). \tag{A20}
\]

Substitution of (A13), (A17), and (A20) in Theorem 4.1 proves that the number
`K` of bad integers in the short interval is `o(k^theta/log k)`.  The source
paper's `PI(theta)` pigeonhole step supplies a prime divisor in its interval.
Together with the unchanged lower ranges, this proves (A3), and hence (A4).

## Theorem B (delimited method barrier)

Define a **termwise blockwise Theorem 4.1 little-o certificate** to be a proof
which:

1. applies Theorem 4.1 with some integer `r>=2` and `lambda>=1` either to the
   source interval or independently to finitely/polylogarithmically many
   comparable shifted intervals whose bases are `asymp k` and lengths are
   `asymp k^theta`;
2. retains its nonnegative right-hand-side terms and sums such independent
   bounds, without cancellation or cross-block correlation;
3. closes the prime pigeonhole step by proving that the resulting normalized
   bound is `o(1/log k)` against the supplied `asymp k^theta/log k` prime count.

Within this class, the supremum of reachable constants is

\[
c_*(\theta)=\frac{1-\theta}{3}. \tag{B1}
\]

More precisely, Theorem A reaches every `c<c_*(theta)`, whereas no such
certificate can work uniformly through the endpoint

\[
n=\left\lfloor\exp(cL^2/l)\right\rfloor
\]

when `c>=c_*(theta)`.

### Proof of the barrier

For one block let `A,B` be as in (2) of the falsification ledger.  If the
certificate is little-o of the prime count, positivity forces

\[
A=o(1/L),\qquad B=o(1/L). \tag{B2}
\]

Since `A<1` eventually and `lambda>=1`,

\[
n r!\lambda^r<k^{r+1}\quad\Longrightarrow\quad n<k^{r+1}. \tag{B3}
\]

At the stated endpoint, (B3) gives

\[
r\geq(c-o(1))L/l. \tag{B4}
\]

On the other hand the exact identity

\[
A^{2r-1}B^{r-1}=k^{\theta-1} \tag{B5}
\]

and (B2) give

\[
(3r-2)(l+q_k)\leq(1-\theta)L,\qquad q_k\longrightarrow\infty, \tag{B6}
\]

after writing `max(A,B)<=e^(-q_k)/L`.  Equations (B4)--(B6) imply
`3c<1-theta`; equality is excluded by the divergent `q_k` term.  This proves
the single-block barrier.

For the stated comparable multiblocks, replacing `k` by bases `asymp k` and
lengths `asymp k^theta` changes (B3)--(B6) only by `O(1)` or `o(L)` terms.
Every independent nonnegative block bound has the same lower envelope; summing
finitely or polylogarithmically many bounds scales that envelope and the
available prime count by the same factor.  It therefore cannot turn the ratio
into little-o at or beyond (B1).

This proves only a barrier for the defined certificate.  It is not a lower
bound for the true `K`, and it leaves open a stronger Konyagin estimate,
cross-block cancellation/correlation, a shorter-scale prime theorem, and all
other methods for Erdős #451.

## Evidence classification and remaining gap

Update: the independent natural-proof audit was subsequently followed by the
kernel-checked construction in `formal/ParametricRanges.lean`.  The earlier
formalization gap described below is therefore historical; the method-class
limitations outside the conditional `PI(theta)` theorem remain unchanged.

This document is an author-verified natural proof (AMRA evidence level 4),
conditional on the named source Theorem 4.1 and `PI(theta)`.  Exact rational
substitutions were replayed under the memory guard, but finite/symbolic replay
does not promote the universal theorem.  A different reviewer must still
reconstruct both Theorem A and the exact scope of Theorem B before any Lean
formalization or promotion.
