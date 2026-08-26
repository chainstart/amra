# Falsification ledger for the parametric frontier

## The exact two-term invariant

Write the first two bracketed terms in Theorem 4.1 as

\[
A=\left(\frac{nr!\lambda^r}{k^{r+1}}\right)^{1/(2r-1)},\qquad
B=\left(\frac{k^{r+\theta}}{nr!\lambda^r}\right)^{1/(r-1)}.
\]

They obey, for every admissible `n,r,lambda`,

\[
A^{2r-1}B^{r-1}=k^{\theta-1}. \tag{2}
\]

Consequently `A=o(1/log k)` and `B=o(1/log k)` force

\[
(3r-2)\log\log k\leq (1-\theta)\log k-o(r), \tag{3}
\]

and no unbalanced choice of `lambda` can improve the leading exponent.  The
choice

\[
u_r=1-(1-\theta)\frac{2r-1}{3r-2},\qquad
\lambda^r=\frac{k^{r+u_r}}{nr!}
\]

gives exactly

\[
A=B=k^{-(1-\theta)/(3r-2)}. \tag{4}
\]

The exact minimizer of `A+B` differs from equality only by an `r`-dependent
constant ratio (`A/B=(2r-1)/(r-1)`); it has the same `k`-exponent.  This kills
MPF-02.

## The factor-two loss in the inherited order bound

Let `L=log k`, `l=loglog k`, and let `r` be the least positive integer with
`n r! <= k^(r+theta)`.  For fixed `c>0`, `epsilon>0`, and

\[
n\leq \exp(cL^2/l),
\]

put `R=ceil((c+epsilon)L/l)`.  Since

\[
\log(R!)\leq R\log R=O_{c,\epsilon}(L)
             =o(L^2/l),
\]

we have

\[
\log(nR!)- (R+\theta)L
\leq-\epsilon L^2/l+O_{c,\epsilon}(L)<0
\]

for all sufficiently large `k`.  Hence `r<=R`.  The source's
`r<=ceil(2cL/l)` spends a second leading copy of `cL^2/l` on `r!`, although the
factorial is lower order.  MPF-01 therefore survives with author-level natural
proof evidence.

Combining (3) with `r=(c+o(1))L/l` at the endpoint gives the candidate and
certificate barrier

\[
c_*(\theta)=\frac{1-\theta}{3}.
\]

For `theta=21/40`, this is `19/120`, not `19/240`.

## Third term: the old `1/12` restriction is artificial

Minimality of `r` gives

\[
n(r-1)!>k^{r-1+\theta}.
\]

For the balanced `lambda`, this implies

\[
\lambda^r<\frac{k^{1+u_r-\theta}}r,
\quad 0<u_r<1.
\]

Thus for

\[
C=\left(\frac{(r+1)\lambda}{k}\right)^{1/(2r)}
\]

we have

\[
\log C\leq-\frac{L}{2r}+O\left(\frac L{r^2}+\frac{\log r}{r}\right).
\]

When `r~cL/l`, this is

\[
C\leq(\log k)^{-1/(2c)+o(1)}.
\]

The third term would become critical only at `c=1/2`.  In the frozen source
range `theta>2/5`, the first-two-term frontier is `<1/5`, so the third term has
large slack.  Bounded `r` gives an ordinary negative power of `k`.  This kills
MPF-04.

## Additive term

The same minimality inequality gives

\[
r\lambda<r k^{h_\theta(r)},\qquad
h_\theta(r)=\frac{1+(1-\theta)(r-1)/(3r-2)}r.
\]

Both `1/r` and `(r-1)/(r(3r-2))` strictly decrease for `r>=3`; explicitly the
derivative numerator of the latter is `-3r^2+6r-2<0` for `r>=2`.  Hence

\[
\max_{r\geq3}h_\theta(r)=h_\theta(3)=\frac{9-2\theta}{21}<\theta
\]

exactly when `theta>9/23`.  The frozen range `theta>2/5` has uniform endpoint
margin `1/105`; at `theta=21/40` the margin is `41/280`.  Therefore
`r lambda=o(k^theta/log k)` independently of `c` on this range.  This kills
MPF-05.

## Order tradeoff

Increasing `r` improves the third term, but (4) shows it makes the leading
decay `(1-theta)/(3r-2)` strictly worse.  Since the least admissible order
already leaves the third term far below `1/log k`, increasing `r` cannot improve
the joint frontier.  This kills MPF-06.

## Prime blocks

For a finite or polylogarithmic family of comparable blocks with bases
`x_j` comparable to `k` and length comparable to `k^theta`, applying Theorem
4.1 independently produces the same identity (2), up to constants and
`k^(o(1))` factors, on every block.  Both the available prime count and the
leading bad-point bound scale linearly with the number of blocks.  Summing
nonnegative independent upper bounds preserves their normalized lower
envelope and cannot change the leading frontier.  This kills MPF-07, but does
not address a new theorem retaining cross-block cancellation or correlation.

If the block length is `k^beta`, the divisibility threshold is
`k^(beta-1)` and the same calculation changes the frontier to `(1-beta)/3`.
A longer block `beta>theta` is strictly worse, killing MPF-08.  The assumption
PI(theta) gives a count only on the whole `k^theta` scale and does not imply a
count in every shorter subblock.  A distribution with all guaranteed primes in
one member of a proposed subdivision satisfies the input count but defeats the
claimed inference.  Thus MPF-09 is killed as a consequence of PI(theta) alone;
a genuinely stronger prime-distribution theorem is left open.

## Scope of the prospective no-go result

The lower envelope above is a lower bound on the **right-hand side of this
particular upper-bound certificate**, not on the true cardinality `K`.  The
no-go statement can therefore cover only proofs which:

1. apply Theorem 4.1 independently on one or finitely/polylogarithmically many
   comparable blocks;
2. retain all its nonnegative terms;
3. close pigeonhole by proving the resulting total bound is little-o of the
   supplied short-interval prime count.

It does not rule out cancellation, a stronger Konyagin theorem, correlated
multiblock estimates, or any direct estimate of the true `K`.

## Computational evidence status

`work/verify_frontier.py`, run under the OpenMath 34 GiB memory guard, checks
the exact rational substitutions, `theta=21/40` value `19/120`, and rational
samples of the additive monotonicity.  The derivative calculation above, not
the finite sample, proves monotonicity for every real/integer `r>=3`.
