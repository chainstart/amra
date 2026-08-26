# Location-blind subdivision extraction bridge

## Status and exact scope

This note closes the previously explicit bridge from a finite, possibly
`k`-dependent subdivision to the finite endpoint obstruction in
`formal/ParametricRanges.lean`.  The result is a theorem only for the class
defined below: the blocks cover a deterministic tail, their Konyagin
right-hand sides are nonnegative and summed term by term, and two comparison
losses are uniform over all blocks and all sufficiently large `k`.

The number of blocks may grow arbitrarily with `k`; no cardinality bound or
lower bound for an individual block length is assumed.  The theorem does not
cover prime-location-adaptive sparse covers, cross-block cancellation, a
stronger exponential-sum estimate, or a stronger local prime theorem.  It is
not a no-go theorem for Erdos 451.

## 1. Cardinality tail supplied by `PI(theta)`

Fix `0<theta<1`, and write

```text
K=log k,             M=loglog k.
```

Suppose `PI(theta)` supplies at least

```text
m_k=floor(A_theta k^theta/K)                         (1)
```

distinct prime offsets `p-k`, after decreasing the fixed positive constant
`A_theta` if necessary.  Among natural offsets, fewer than `m_k/2` are below
`m_k/2`.  Hence at least `m_k/2` candidates lie in

```text
I_k=[m_k/2,k^theta),                                  (2)
```

and `|I_k|` is asymptotic to `k^theta`.  This is a cardinality argument, not
a local equidistribution assertion.  Lean checks its exact finite form in
`candidate_cardinality_tail` and `candidate_half_mass_tail`.

A location-blind proof cannot discard a deterministic part of (2) and still
deduce from the total count alone that a candidate remains.  The certificate
class therefore partitions all of (2).  If its real cut points are

```text
x_0=m_k/2 < x_1 < ... < x_s=k^theta,
```

the weights `h_j=x_(j+1)-x_j` are positive and telescope to
`H_k=|I_k|`.  The identity for an arbitrary finite number of cuts is
kernel-checked as `interval_partition_length_sum`.

## 2. Exact finite certificate class

For every block `j`, let `r_j>=2`, `lambda_j>=1`, `W_j>=1`, and put

```text
log T1_j=(log D_j+r_j log lambda_j+2log W_j)/(2r_j-1),
log T2_j=(log delta_j+2log W_j-log D_j-r_j log lambda_j)/(r_j-1).
                                                               (3)
```

At a fixed `k`, a
`LocationBlindTermwiseSubdivisionAt(theta,c,K,M,C,D,q,H,s,block)` consists
of an arbitrary nonempty finite set `s` and positive weights `h_j` such that

```text
sum_j h_j=H,                                           (4)
log delta_j+4log W_j >= -(1-theta)K-M-C,              (5)
log T1_j<0  ==>  r_j M >= cK-DM,                      (6)
sum_j h_j(exp(log T1_j)+exp(log T2_j))
    <= H exp(-M-q).                                    (7)
```

Here `C,D` are common to all blocks.  The structure and all four conditions
are definitions in Lean; (5) is the safe-tail loss, (6) is required only
when the first term is actually below one, and (7) is the summed
nonnegative ledger.  No blockwise prime count is assumed.

The source geometry supplies fixed losses in this named architecture once
the raw comparison constants are fixed uniformly over the block family.
Indeed (2) gives

```text
delta_j >> k^(theta-1)/K,
```

uniformly over a location-blind full-tail cover, which is (5) after taking
logs and enlarging one fixed `C`.  For the pinned reciprocal phase,

```text
D_j = n_j r_j!/x_j^(r_j+1)
```

up to fixed comparison factors, with `x_j=k+O(k^theta)` and `n_j=n+O(k)`.
If `log T1_j<0`, then `lambda_j,W_j>=1` imply `log D_j<0`.  At
`n=floor(exp(cK^2/M))`, this gives

```text
r_j M >= cK-DM                                        (8)
```

with a fixed `D`: the `+1` in `r_j+1` costs one `M`, bounded comparison
factors cost `O(M)`, and the source restriction
`r_j=O(k^(1-theta))` makes
`r_j(log x_j-log k)=O(1)`.  Thus (5)--(6) are uniform source consequences
under the explicitly quantified raw comparisons, not block-count assumptions.
The finite implication is now kernel-checked in
`sourceGeometrySubdivision_to_locationBlind`, with `C=-log a` and
`D=5/2+En+ED`; see `evidence/source_geometry_uniform_losses.md`.

## 3. Weighted extraction, with no block-count loss

Let

```text
E_j=exp(log T1_j)+exp(log T2_j)>0.
```

If every `E_j` were larger than `exp(-M-q)`, positivity of the weights and
(4) would make the left side of (7) larger than its right side.  Therefore
some block satisfies

```text
E_j <= exp(-M-q),
log T1_j <= -M-q,      log T2_j <= -M-q.              (9)
```

Lean proves the weighted-average statement as `exists_weighted_cost_le` and
the exact extraction as `locationBlindSubdivision_exists_good_block`.  The
proof is uniform in the finite index set.  Consequently `s=s_k` may have
arbitrary finite cardinality at each `k`, including cardinality tending to
infinity.

If the original total bound is only written as

```text
sum_j h_j E_j=o(H_k/K),                               (10)
```

then its positive normalized average `e_k=(sum h_jE_j)/H_k` obeys
`e_k/e^(-M)->0`.  Defining

```text
q_k=-M-log e_k
```

gives `q_k->infinity` and (7), in fact with equality.  Thus the exact finite
predicate faithfully represents the usual summed little-`o` certificate.

## 4. Endpoint contradiction

The prior block invariant is exact:

```text
(2r_j-1)log T1_j+(r_j-1)log T2_j
  =log delta_j+4log W_j.                              (11)
```

Combining (5), (6), (9), and
`c>=(1-theta)/3` yields the finite excess inequality

```text
(3r_j-2)q <= (3D+3)M+C.                              (12)
```

The new Lean theorem packages extraction and this contradiction without
choosing a limiting block:

> **Finite subdivision endpoint theorem.**  Assume `K>=0`, `M>0`, `q>=0`,
> `c>=(1-theta)/3`, and
>
> ```text
> ((3D+3)M+C)M
>   < (3cK-(3D+2)M)q.                                (13)
> ```
>
> Then no `LocationBlindTermwiseSubdivisionAt` certificate exists.

This is kernel-checked as
`locationBlindTermwiseSubdivision_endpoint_no_go`.

For fixed `C,D`, fixed `c>0`, `K=log k`, `M=loglog k`, and `q_k->infinity`,
(13) holds eventually.  Indeed `K/M^2->infinity`; eventually
`(3D+2)M<=cK`, `q_k>=1`, and

```text
((3D+3)M+C)M < 2cK
                  <= (3cK-(3D+2)M)q_k.               (14)
```

This proves the promised sequence statement:

> **Growing-subdivision barrier.**  Let `0<theta<1` and `c>0` with
> `c>=(1-theta)/3`.  There is no sequence of finite, full-tail,
> location-blind termwise subdivisions satisfying (3)--(6) with fixed
> comparison losses `C,D` and the total little-`o` ledger (10).

The argument does not pass to a limiting index set or require compactness.
It applies the uniform finite kernel theorem separately at each sufficiently
large `k`.

The fixed-exponent LP theorem
`LocationBlindTermwiseLeadingCertificate_iff` remains a useful leading
summary, but it is not the logical extraction target at the equality
endpoint: effective decay exponents can tend down to one.  The exact bridge
at equality is (9)--(14), through the finite excess theorem.

## 5. Why the uniform hypotheses are necessary

The following one-block algebraic examples show that arbitrary growth of the
losses cannot be admitted.  They are counterexamples to weakened abstract
certificate definitions, not constructions of actual prime certificates.

### No uniform order loss

Take one block of weight `H=1`, `r=2`, `lambda=W=1`, and

```text
Q_k=M+q_k+log 2,
log D=-3Q_k,       log delta=-4Q_k.                   (15)
```

Then `log T1=log T2=-Q_k`, so (7) holds exactly.  If
`q_k=o(K)` then the fixed safe bound (5) holds for all large `k`, but choosing
`D_k=cK/M` makes (6) vacuous.  Hence no endpoint theorem is possible if the
order loss may grow like `K/M`.

### No uniform safe-tail loss

For any chosen order `r_k`, take one block with `lambda=W=1` and

```text
log D=-(2r_k-1)Q_k,
log delta=-(3r_k-2)Q_k.                              (16)
```

Again both logs equal `-Q_k` and (7) holds.  A growing

```text
C_k >= (3r_k-2)Q_k-(1-theta)K-M
```

makes (5) automatic, even at the endpoint.  Therefore the safe-tail
comparison must also be uniform.  The genuine PI cardinality tail supplies
precisely that uniformity.

These examples identify the minimal missing assumptions in any purported
barrier for a broader class.  Finite-at-each-scale cardinality is harmless;
uncontrolled geometric/order losses are not.

## 6. Formal evidence boundary

Lean now checks:

- the finite cardinality-tail inequalities;
- telescoping of arbitrary finite interval-partition lengths;
- the exact finite certificate structure;
- positive weighted good-block extraction;
- the full finite endpoint no-go, uniformly in the index set;
- the finite shifted-base inequalities
  `r log(x/k)<=1/2` and `(r+1)(log x-log k)<=3/2`;
- the safe-tail map from a fixed `a` to `C=-log a`;
- the derivative/endpoint comparison map from fixed `En,ED` to
  `D=5/2+En+ED`;
- the complete finite source-family map and finite separation wrapper;
- all earlier block-invariant, endpoint-excess, and LP theorems.

Lean encodes the analytic source comparison as an explicit finite lower
inequality with fixed `ED`; it does not infer that inequality from an
unquantified `asymp`, nor does it encode the limits `K/M^2->infinity` and
`q_k->infinity` as a sequence theorem.  Thus the finite source-to-bridge map
is kernel-checked.  Application to a broader shifted/grouped source remains
conditional on proving its fixed raw constants `a,En,ED`.

The frozen source was fully replayed through `formal/verify_guarded.sh` in
guard unit `openmath-task-20260826-213317-292367.scope` with exit status zero.
Its fresh guarded range build took `113.75s` and peaked at `7,075,568 KiB`
with zero swap; this is the largest per-command replay RSS.  Every new theorem reports only
`[propext, Classical.choice, Quot.sound]`; no `sorryAx` occurs.  The verified
`ParametricRanges.lean` SHA-256 is
`8793c3a76f46ce7e4985e7619bb53eb91ce481391ac52bce343dfc9232f4f7b5`.

Final AMRA validation and strict artifact control passed under guard unit
`openmath-task-20260826-205059-276009.scope`.  The package's five research
loop unit tests passed under
`openmath-task-20260826-204950-275140.scope`.  Final strict JSON parsing
(excluding vendored `.lake` JSON-with-comments), `git diff --check`, source
hash, and no-`sorry` control were included in the final validation unit.
