# Direct common-start correlations: the rank-three affine reduction and a fixed-`D` no-go theorem

## Status and scope

This note deepens the direct common-start branch in `survivor_deepening`.
It contains two unconditional natural proofs (using the standard unconditional
bounded-prime-clusters theorem):

1. an exact rank-three row/2D-rotation formula; and
2. a counterexample to the proposed all-interval correlation estimate with
   absolute fixed polynomial loss `D`.

The counterexample is to the **termwise support-correlation bridge**, not to
Erdos 451.  It does not rule out cancellation between different Fourier
supports or an argument tailored to the single final counting expression.

Throughout, let

```text
p_i = k+b_i,        0<b_i<k,
G_{p_i}(s) = p_i 1_[0,b_i)(s mod p_i)-b_i.
```

Thus `G_p` is `k` on the common-start interval and `-(p-k)` outside it,
and its mean over `Z/pZ` is zero.

## 1. Exact rank-three row formula

Let `p_1<p_2<p_3` and put

```text
Delta_2=p_2-p_1,       Delta_3=p_3-p_1.
```

Write a complete `p_1`-row as `s=j p_1+u`, `0<=u<p_1`, and set

```text
x_j = j Delta_2 mod p_2,
y_j = j Delta_3 mod p_3.
```

For residues `x mod p_2`, `y mod p_3`, define subsets of the row

```text
A       = {0<=u<p_1 : u<b_1},
B_x     = {0<=u<p_1 : u-x mod p_2 lies in [0,b_2)},
C_y     = {0<=u<p_1 : u-y mod p_3 lies in [0,b_3)}.
```

Use the exact cell counts

```text
N_2=|B_x|,       N_3=|C_y|,
N_12=|A intersect B_x|,       N_13=|A intersect C_y|,
N_23=|B_x intersect C_y|,
N_123=|A intersect B_x intersect C_y|.
```

Then the complete-row correlation is exactly

```text
R_j := sum_{u=0}^{p_1-1}
          G_{p_1}(j p_1+u)G_{p_2}(j p_1+u)G_{p_3}(j p_1+u)

     = p_2 p_3 [p_1 N_123-b_1 N_23]
       -p_2 b_3 [p_1 N_12-b_1 N_2]
       -b_2 p_3 [p_1 N_13-b_1 N_3],                 (1)
```

where every count on the right is evaluated at `(x_j,y_j)` as applicable.

### Proof

Use `G_{p_i}=p_i 1_i-b_i` and expand the three factors.  The eight cells
give

```text
p_1p_2p_3 N_123 - p_1p_2b_3 N_12 - p_1b_2p_3 N_13
- b_1p_2p_3 N_23 + b_1p_2b_3 N_2 + b_1b_2p_3 N_3
+ p_1b_2b_3 |A| - b_1b_2b_3 p_1.
```

The last two terms cancel because `|A|=b_1`, and regrouping proves (1).
No asymptotic estimate is used.

Since `Delta_i` is nonzero modulo the prime `p_i`, the row phases

```text
j -> (j Delta_2 mod p_2, j Delta_3 mod p_3)          (2)
```

form one full 2D CRT orbit of period `p_2p_3`.  Splitting an arbitrary
integer interval into complete `p_1`-rows leaves at most two fragments, of
total contribution less than `4k^4`.  Consequently rank three is reduced
exactly to partial sums of (1) along (2), plus this explicit endpoint error.

## 2. What the formula says about the direct and affine routes

Define

```text
Phi_2(x) = sum_{u<p_1} G_{p_1}(u) 1_{B_x}(u)
         = p_1N_12-b_1N_2,

Phi_3(y) = sum_{u<p_1} G_{p_1}(u) 1_{C_y}(u)
         = p_1N_13-b_1N_3,

H(x,y)   = sum_{u<p_1} G_{p_1}(u)1_{B_x}(u)1_{C_y}(u)
         = p_1N_123-b_1N_23.
```

Then (1) is

```text
R_j=p_2p_3H(x_j,y_j)-p_2b_3Phi_2(x_j)-b_2p_3Phi_3(y_j).   (3)
```

The leading term cannot be tensorized from the rank-two theorem.  To see
the exact affine reduction, partition the row indices as `j=a+t p_2`.
For fixed `a`, `x_j` is frozen, whereas

```text
y_j = y_a+t[p_2 Delta_3] mod p_3.                    (4)
```

The step in (4) is invertible modulo `p_3`.  Moreover

```text
p_3H(x,y)-b_3Phi_2(x)
 = sum_{u<p_1}G_{p_1}(u)1_{B_x}(u)
      [p_3 1_{C_y}(u)-b_3].                          (5)
```

Thus each fixed-`a` slice is a one-dimensional **affine-phase correlation**
between a phase-truncated first factor and the moving `p_3` interval.  There
are `p_2` such starting phases.  Taking absolute values slice by slice pays
this extra factor, and the first factor in (5) is neither a common-start
`G_p` nor a centered function by itself.  The lower-rank correction terms in
(3) perform the necessary centering.

Therefore direct rank three already creates an affine discrepancy problem.
This narrows the claimed independence of the two upper-bound branches:

- the direct and absorbed approaches both require estimates uniform in an
  affine starting phase once rank exceeds two;
- they are not literally the same arithmetic problem.  The direct slopes in
  (4) are made from prime differences and products, while the absorbed route
  has inverse-binomial/Vandermonde phases;
- in particular, the proved rank-two common-start theorem supplies no simple
  tensor induction for (3).

## 3. A Fourier prefix lemma

Let `(a_s)` be a real, mean-zero, `Q`-periodic sequence and define

```text
ahat(ell)=(1/Q) sum_{s=0}^{Q-1} a_s exp(-2 pi i ell s/Q).
```

For a centered integer frequency `ell` with `0<|ell|<Q/2`, Abel summation
gives

```text
max_{0<=T<Q} |sum_{s=0}^{T-1}a_s|
 >= |ahat(ell)|/|1-exp(-2 pi i ell/Q)|
 >= |ahat(ell)| Q/(2 pi |ell|).                      (6)
```

Indeed, if `S_T=sum_{s=0}^T a_s`, then `S_{Q-1}=0` and

```text
sum_{s=0}^{Q-1}a_s z^s=(1-z)sum_{T=0}^{Q-2}S_Tz^T.
```

Taking absolute values proves (6).

## 4. Exact bounded-cluster resonance

Fix a rank `r>=2`.  The unconditional bounded-prime-clusters theorem says
that some `B_r` admits infinitely many intervals containing at least `r`
primes.  One precise input is Maynard's theorem
`liminf_n (p_{n+m}-p_n)<infinity` for every fixed `m` (J. Maynard,
*Small gaps between primes*, Annals of Mathematics 181 (2015), DOI
`10.4007/annals.2015.181.1.7`).  There are only finitely many offset patterns
inside an interval of length `B_r`; after passing to an infinite subsequence,
select primes

```text
p_i=x+d_i,       0=d_1<d_2<...<d_r<=B_r,             (7)
```

with the same offsets `d_i` and with `x` tending to infinity.

Put

```text
L       = product_{i<j}(d_j-d_i),
F(X)    = product_i(X-d_i),
h_i     = L/F'(d_i),
epsilon = (-1)^(r+1).                                (8)
```

Every `h_i` is a fixed nonzero integer.  Partial fractions give the exact
identity

```text
sum_i h_i/(x+d_i)
 = epsilon L/product_i(x+d_i) = epsilon L/Q.          (9)
```

where `Q=product_i p_i`.  This is an order-`r` resonance, not a numerical
near coincidence.  The sign is worth making explicit: the standard weights
`1/F'(d_i)` give `epsilon/Q`.  Equivalently, using the reversed denominator
`product_{j ne i}(d_j-d_i)` absorbs `epsilon` and makes the right side
positive.

Choose once and for all an irrational `alpha` with `1/2<alpha<1`, let
`k=floor(alpha x)`, and put `rho=1-alpha`.  For all sufficiently large `x`,
every selected prime lies in `(k,2k)`, while

```text
b_i/p_i=(p_i-k)/p_i -> rho.
```

Because `rho` is irrational, `sin(pi h_i rho)` is nonzero for every `i`.
The normalized local Fourier coefficient of `G_{p_i}` at `h_i` is exactly

```text
(1/p_i)sum_{u mod p_i}G_{p_i}(u)exp(-2 pi i h_i u/p_i)
 =sum_{u=0}^{b_i-1}exp(-2 pi i h_i u/p_i),            (10)
```

and hence

```text
(1/p_i)|sum_{u=0}^{b_i-1}exp(-2 pi i h_i u/p_i)|
 -> |sin(pi h_i rho)|/(pi |h_i|)>0.                  (11)
```

Let `a_s=product_i G_{p_i}(s)`.  The CRT and (9) factor its global Fourier
coefficient at the signed integer frequency `epsilon L`:

```text
|ahat(epsilon L)|
 = product_i |sum_{u=0}^{b_i-1}exp(-2 pi i h_i u/p_i)|
 >= eta_r Q                                                    (12)
```

for some constant `eta_r>0` and all sufficiently large members of the
subsequence.  The sequence has mean zero because the CRT makes its local
coordinates independent and every `G_{p_i}` has mean zero.  In the Abel
step, the unnormalized exponential sum is exactly
`Q*ahat(epsilon L)`.  Its upper bound is
`Q |1-exp(-2 pi i epsilon L/Q)| max_T|S_T|`; the two factors `Q` cancel,
leaving (6), and
`|1-exp(-2 pi i epsilon L/Q)|<=2 pi L/Q`.  Thus applying (6) to (12)
proves

```text
max_{0<=T<Q}|sum_{s=0}^{T-1} product_iG_{p_i}(s)|
 >= eta_r Q^2/(2 pi L) = Omega_r(k^(2r)).             (13)
```

The same lower bound, with half the constant, holds on an interval starting
at `s=k`: deleting the first `k` terms costs at most `k^(r+1)`, negligible
against (13).  Also the maximizing endpoint is at most `Q=O_r(k^r)`, so the
witness interval has only polynomial length for each fixed `r`.

## 5. Fixed polynomial loss is impossible

> **Fixed-`D` no-go theorem.**  There are no absolute constants `C,D` such
> that, for every `k`, every nonempty set `S` of primes in `(k,2k)`, and
> every integer interval `J`,
>
> ```text
> |sum_{s in J} product_{p in S}G_p(s)|
> <= k^(|S|+D) C^|S|.                                 (14)
> ```

To prove this, choose an integer `r>D` and use (13).  Its left side is at
least a positive rank-dependent constant times `k^(2r)`, whereas the right
side of (14) is `C^r k^(r+D)`.  Their ratio tends to infinity along the
infinite prime-cluster subsequence.

More precisely, any rank-`r` theorem of this form, even with an arbitrary
prefactor depending only on `r`, requires extra polynomial exponent
`D_r>=r`.  At rank three the construction gives `Omega(k^6)`, so a uniform
rank-three estimate needs at least `D_3=3`; the earlier rank-two coherent-row
example is the `D_2>=2` instance of the same phenomenon.

This also audits the recursion ledger.  A termwise support proof that pays
`k^(D_r)` with `D_r>=r` has logarithmic loss at least

```text
r log k.
```

At the natural full rank `r=Theta(k/log k)`, this is `Theta(k)`, not `o(k)`.
Thus the proposed absolute-value summation over support correlations cannot
prove `n_k=exp(o(k))`.

The last ledger statement concerns a uniform rank-by-rank recursion.  The
bounded-cluster proof fixes `r` before sending `k` to infinity and does not
assert a single growing-rank prime cluster.  What it rigorously excludes is
every uniform fixed-`D` estimate (14), and hence every recursion whose only
ledger is that estimate.  It leaves open mechanisms using cancellation
between supports, the entire combined counting function, or additional
scale-dependent structure not present in (14).

## 6. Consequence for the campaign

- The exact rank-three row formula is now closed.
- Rank three is an affine-phase problem after slicing, not a tensor product
  of the common-start rank-two theorem.
- The all-interval support-correlation conjecture with fixed `D` is refuted,
  and the implied termwise recursive ledger is `exp(Omega(k))`.
- This does not change the public upper bound for Erdos 451.  The remaining
  direct route must exploit cancellation between supports or a more global
  identity; proving another termwise bound of the form (14) is no longer a
  valid target.

## 7. Exact arithmetic sanity replay

As a check on transcription (not as evidence for the universal theorems), a
standard-library `Fraction` replay verified (1) on all `13*17=221` rows for
`k=10`, `(p_1,p_2,p_3)=(11,13,17)`, and verified (9) exactly for the offset
patterns `(0,2,6)` and `(0,4,6,10)` at two base points each.  It ran under
the shared memory guard as unit
`openmath-task-20260826-174144-179158.scope` and returned `PASS` with no
floating-point arithmetic.  The proofs above do not depend on this finite
replay.
