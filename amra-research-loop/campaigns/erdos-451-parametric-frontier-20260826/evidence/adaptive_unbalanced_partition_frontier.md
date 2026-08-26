# Adaptive unbalanced Konyagin frontier and the enlarged old-architecture barrier

## Status

This note enlarges the old van Doorn--Tang/Konyagin architecture in two
directions:

1. the Konyagin scale `lambda` and derivative order `r` are selected
   adaptively and need not balance the first two terms;
2. the no-go class permits nonuniform prime subintervals, different safe
   residue thresholds, and shifted contiguous factor groups, provided the
   proof still applies the same nonnegative Konyagin estimate independently
   and sums its right-hand sides.

The attaining proof and the delimited barrier below are author-verified
natural proofs, conditional on `PI(theta)`.  They have not yet received a new
blind audit or Lean replay.  The previous kernel-checked theorem on
`9/23<theta<1` remains untouched.

## 1. Result

> **Adaptive unbalanced theorem.**  Let `0<theta<1` and assume
> `PI(theta)`.  For every fixed
>
> ```text
> 0<c<(1-theta)/3,                                    (1)
> ```
>
> all sufficiently large `k` and all integers
>
> ```text
> 2k<n<=exp(c log(k)^2/loglog(k))
> ```
>
> admit a prime divisor of `(n-k)...(n-1)` in
> `(k,k+3k^theta)`, hence in `(k,2k)`.

Thus the natural old-proof parameter region expands strictly from
`9/23<theta<1` to the full interval `0<theta<1`.  At the unconditional BHP
point `theta=21/40`, the constant remains

```text
c<(1-21/40)/3=19/120.                                (2)
```

The author-level barrier lemma in Section 5 shows that (2) cannot be increased
inside the explicitly defined enlarged old architecture.

## 2. Exact adaptive selection

Write

```text
L=log k,       l=log L.
```

Choose fixed real numbers `Q,a` such that

```text
1<Q,       c<a,       3Qa<1-theta.                   (3)
```

This is possible exactly because of (1).  For each integer `r>=1`, put

```text
U_r = k^(r+1) L^(-Q(2r-1)),
V_r = k^(r+theta) L^(Q(r-1)).                         (4)
```

Retain all three already proved lower ranges (small, medium, and
medium-large).  It is enough to treat

```text
n>(1/2)k^(2+theta).                                   (5)
```

Choose `r` to be the least positive integer such that

```text
n r! <= U_r.                                          (6)
```

Such an `r` exists, is at least `2`, and satisfies

```text
r <= R:=ceil(aL/l).                                   (7)
```

Indeed

```text
log(nR!) <= cL^2/l+O_a(L),
log U_R   = (R+1)L-Q(2R-1)l
          = aL^2/l+O_{a,Q}(L),
```

so (6) holds at `R` for large `k`.  On the other hand (5) makes (6)
false at `r=1`, because
`n>k^(2+theta)/2>k^2L^(-Q)` for every fixed `theta>0` and large `k`.
Hence `r>=2`.  From (3), (7), and (4),

```text
V_r<=U_r                                               (8)
```

for all sufficiently large `k`, because (8) is exactly

```text
Q(3r-2)l <= (1-theta)L.                               (9)
```

Equivalently, put `X=nr!/k^(r+theta)` and set

```text
lambda^r=max(1,X^(-1)L^(Q(r-1))),
Z=nr!lambda^r=max(nr!,V_r).                           (10)
```

The pinned theorem permits every real `lambda>=1`; no integrality condition
is imposed on it.  Taking the positive real `r`-th root in (10) therefore
gives an admissible scale.  Equations (6), (8), and (10) give
`V_r<=Z<=U_r`.
For the first two Konyagin terms

```text
A=(nr! lambda^r/k^(r+1))^(1/(2r-1)),
B=(k^(r+theta)/(nr! lambda^r))^(1/(r-1)),             (11)
```

(10) therefore proves the two exact bounds

```text
A<=L^(-Q),       B<=L^(-Q).                           (12)
```

This is deliberately unbalanced when `nr!>V_r`: then `lambda=1`, `A` is
allowed to approach its upper logarithmic budget, and `B` is smaller than
required.  When `nr!<V_r`, only the minimum increase of `lambda` needed for
the second term is made.

## 3. The third and additive terms

The key gain over the balanced construction is a uniform sharper bound on
`lambda`.  If `lambda>1`, minimality in (6), valid uniformly for every
selected `r>=2`, gives

```text
n(r-1)!>U_(r-1)=k^r L^(-Q(2r-3)).
```

Consequently

```text
lambda^r=V_r/(nr!)
 < k^theta L^(Q(3r-4))/r.
```

Indeed the previous order `r-1>=1` failed (6), and multiplying its inequality
by `r` gives the displayed lower bound for `nr!`.  The cases `lambda=1` are
smaller, so uniformly for every selected `r>=2`,

```text
lambda <= k^(theta/r)L^(3Q).                          (13)
```

For the additive term this gives

```text
r lambda /(k^theta/L)
 <= r L^(3Q+1) k^(-theta(1-1/r))
 <= R L^(3Q+1) k^(-theta/2) -> 0.                    (14)
```

Thus the former `r=3` additive endpoint `theta>9/23` was an artifact of
balancing `A=B`; it is not a barrier for the adaptive old architecture.

For the third Konyagin term

```text
C_3=(((r+1)lambda)/k)^(1/(2r)).                       (15)
```

When `r=2`, (13) makes (15) a fixed negative power of `k` times a log power.
For `r>=3`, (7) and (13) give

```text
log C_3
 <= (log(r+1)+3Q l-(1-theta/r)L)/(2r)
 <= -(1-theta/3)L/(2r)+O_Q(l/r)
 <= -((1-theta/3)/(2a)+o(1))l.                       (16)
```

The exponent in (16) is strictly larger than `1`, since (3) implies
`a<(1-theta)/3<(1-theta/3)/2`.  Hence

```text
C_3=o(1/L).                                           (17)
```

Also `r=O(L/l)=o(k^(1-theta))`, so all order hypotheses in the pinned
Konyagin theorem hold.  Substituting (12), (14), and (17) into Theorem 4.1
gives

```text
|badSetAt(theta,k,n)|=o(k^theta/L).                   (18)
```

The `PI(theta)` pigeonhole step and the already proved lower ranges complete
the adaptive theorem.

## 4. Why `r=2` really can extend farther

The fixed balanced proof changed to `r=3` immediately above
`n=(1/2)k^(2+theta)`, because it defined `r` through
`nr!<=k^(r+theta)`.  That switch is not forced by Theorem 4.1.

With `r=2`, `lambda=1`, its first two terms are

```text
(2n/k^3)^(1/3),       k^(2+theta)/(2n).               (19)
```

They are simultaneously small throughout a much wider interior interval;
in particular `r=2` remains useful above `k^(2+theta)`.  The adaptive upper
threshold `U_2=k^3L^(-3Q)` delays the switch until the first term approaches
its allotted logarithmic size.  When the proof moves to `r=3`, minimality of
the **upper** threshold controls `lambda` by `k^(theta/3)` rather than the
coarser `k^(1/3)`.  This is the precise reason the lower theta obstruction
disappears.

No hidden source hypothesis forces `nr!<=k^(r+theta)`: that inequality was
used only by the previous parameter choice to certify `lambda>=1`.  The
pinned theorem itself assumes only

```text
r>=2, lambda>=1, 0<theta<1,
r<=(1/2)k^(1-theta), and k<n,                         (20)
```

all of which are satisfied above.

## 5. Enlarged old-architecture no-go class

Define an **adaptive subdivided Konyagin certificate** as follows.

1. It uses the same length-`k` product, or shifted contiguous subproducts of
   it, and partitions the deterministic candidate tail forced by the total
   `PI(theta)` cardinality into any finite, possibly `k`-dependent family of
   nonuniform intervals.  It may choose a separate order `r_j`, scale
   `lambda_j>=1`, and rational-denominator parameter `W_j>=1` on every
   piece.
2. On each piece it applies the pinned Konyagin estimate to
   `f_j(x)=+-n_j/(x_j+x)`, where `x_j=k+O(k^theta)` and
   `n_j=n+O(k)`, retaining every nonnegative term.
3. The safe approximation threshold must genuinely imply that a prime in
   the piece divides the selected factor group.  The proof sums the
   independent nonnegative block bounds and compares the sum with only the
   supplied total `PI(theta)` prime count by proving that total to be
   `o(k^theta/log k)`.  It uses no cross-block cancellation, no enumeration
   of the actual prime locations to select a sparse cover, and no stronger
   local prime-distribution input.

This class includes balanced or unbalanced `lambda`, arbitrary factorial or
factor-size thresholds used to select `r`, nonbalanced subdivisions of the
prime interval, dyadic `m`-ranges, and variable contiguous groupings of the
`k` product factors.

> **Enlarged architecture barrier.**  No adaptive subdivided Konyagin
> certificate proves the endpoint
>
> ```text
> n=floor(exp(cL^2/l))
> ```
>
> with `c>=(1-theta)/3`.

### Cardinality-tail reduction

After decreasing the positive constant supplied by `PI(theta)` if necessary,
fix it as `C_theta` and put

```text
M_k=floor(C_theta*k^theta/L) asymp k^theta/L.          (21)
```

The supplied interval `(k,k+k^theta)` contains at least `M_k` distinct primes.
There are fewer than `M_k/2` integers,
hence fewer than `M_k/2` primes, at distance less than `M_k/2` from `k`.
Consequently at least `M_k/2` supplied candidates lie in the deterministic
tail

```text
k+M_k/2 <= p < k+k^theta.                             (22)
```

The deterministic tail still has geometric length `asymp k^theta`; this is
the entire region partitioned by the location-blind certificate class above.
For the full length-`k` factor group, a nearest-integer argument that
guarantees a residue in `{1,...,k}` needs a uniform threshold on a block at
least as large as its
smallest possible `(p-k)/p`.  A shorter contiguous group of length `h<=k` is
no better: after shifting its endpoint, the symmetric far-from-integer bridge
requires

```text
delta_j >= (p-h)/p >= (p-k)/p
        >> k^(theta-1)/L.                             (23)
```

Thus changing the factor grouping cannot reduce the leading tail exponent.
Splitting (22) into narrower intervals changes the prefactors but not the
uniform lower scale (23), and the interval lengths still sum to
`asymp k^theta`.  A proof that selects a sparse cover after enumerating the
actual prime positions uses additional local-location information and is
deliberately outside this no-go class.  Likewise, a certificate that discards
a deterministic positive-cardinality subset without prime-location input
cannot infer from `PI(theta)` that the remaining cover contains a candidate;
the definition therefore requires a partition of the whole tail (22).

### Block invariant

For a block `j`, ignore only bounded comparison constants caused by
`x_j/k->1` and `n_j/n->1`, and write its first two normalized terms as

```text
A_j=(D_j lambda_j^(r_j) W_j^2)^(1/(2r_j-1)),
B_j=(delta_j W_j^2/(D_j lambda_j^(r_j)))^(1/(r_j-1)),
D_j asymp n_j r_j!/x_j^(r_j+1).                      (24)
```

They have the exact structural invariant

```text
A_j^(2r_j-1) B_j^(r_j-1)=delta_j W_j^4
                         >> k^(theta-1)/L.            (25)
```

Neither an unbalanced `lambda_j`, a different rule for choosing `r_j`, nor
`W_j>1` improves (25).

The first two terms contribute their block length times `A_j+B_j` to the
summed Konyagin upper bound.  Because all block bounds are nonnegative and the
deterministic-tail block lengths sum to `asymp k^theta`, a total
`o(k^theta/L)` certificate would force a set of blocks carrying `1-o(1)` of
that length to satisfy

```text
A_j+B_j=o(1/L).                                       (26)
```

Choose one such block.  If `A_j<1`, (24), `lambda_j,W_j>=1`, and the endpoint
value of `n_j` imply

```text
r_j >= cL/l-O(1).                                     (27)
```

Writing `max(A_j,B_j)<=exp(-q_k)/L` along these blocks, (26) permits
`q_k->infinity`.  Equations (25)--(27) give

```text
(3r_j-2)(l+q_k) <= (1-theta)L+l+O(1),
r_j >= cL/l-O(1).                                     (28)
```

For `c>(1-theta)/3`, the leading terms in (28) contradict each other.  At
equality, `(3r_j-2)l` already equals `(1-theta)L+O(l)`, including the single
extra `+l` caused by the cardinality tail, while the additional term
`(3r_j-2)q_k` is much larger than `l` because
`r_j asymp L/l` and `q_k->infinity`.  Thus equality is also impossible.

The weighted assertion preceding (26) is elementary: if the
length-weighted average of `A_j+B_j` is `t_k/L` with `t_k->0`, then blocks
with `A_j+B_j>sqrt(t_k)/L` carry at most `sqrt(t_k)` of the total length.
It therefore remains valid for highly nonbalanced partitions and a growing
number of pieces.

### Linear-program form

Set, schematically,

```text
rho=r l/L,       alpha=-log(A)/l,       beta=-log(B)/l.
```

The endpoint and little-o requirements become

```text
rho>=c,       alpha>1,       beta>1,
(2alpha+beta)rho <= 1-theta.                           (29)
```

Since `2alpha+beta>3`, feasibility forces

```text
c<(1-theta)/3.                                        (30)
```

This is the promised linear/convex obstruction for the enlarged method
class.  It is attained by the adaptive construction in Sections 2--3.

## 6. Exact conclusion and remaining scope

- Nonbalanced `lambda` and a delayed `r=2` switch **do** enlarge the
  conditional theta domain from `theta>9/23` to every `theta>0`.
- They do **not** improve the `c` frontier `(1-theta)/3`; hence BHP still
  gives exactly every `c<19/120` within this enlarged old architecture.
- Unequal prime blocks, dyadic `m`-ranges, or shorter product-factor groups
  cannot improve the frontier while only `PI(theta)` is supplied and the
  nonnegative Konyagin bounds are summed independently.
- The barrier does not apply to a stronger Konyagin estimate, cancellation
  between blocks, a prime theorem at a shorter exponent, or a direct estimate
  of the true bad set.  It is not a barrier for Erdős 451 itself.

## 7. Guarded replay

`work/verify_adaptive_unbalanced.py` checks the coefficient identities and
the selected inequalities in log coordinates for 41 values of `n` in each
of three regimes: `theta=21/40`, `theta=1/10`, and `theta=9/10`.  It most
recently ran under guard unit
`openmath-task-20260826-181605-191334.scope` and returned `PASS` with maximum
resident set 12000 KiB, zero swaps, and exit status zero.  The exact timed
command, prior guard unit, script hash, parameters, and scope limitation are
recorded in `evidence/adaptive_unbalanced_replay.json`.  This finite replay is
a transcription check only and is not used to promote the quantified natural
proof to machine-checked status.
