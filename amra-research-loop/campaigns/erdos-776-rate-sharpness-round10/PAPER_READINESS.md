# Paper readiness: exact recovery dynamics on a Macaulay orbit

## Candidate paper claim

The defensible standalone theorem is the fixed-family recovery result:

```text
rho(j) <= 2+ceil(log_2(j+4))
```

for every actual odd member of the specified `K4,r9` family, together with
the explicit subsequence

```text
j_R=11*2^(R-4)-5,  rho(j_R)=R+1,
```

which proves asymptotic sharpness and additive-one sharpness of that bound.

## Changed publication context

He and Tang, arXiv:2602.09803v2 (21 March 2026), already prove

```text
2r+2 <= n_0(r) <= 2r+2 log_2 r + O(log_2 log_2 r),
n_0(r)=2r+o(r).
```

Consequently this campaign cannot be presented as solving Erdős #776,
improving its main term, or establishing the current best threshold. Its
possible novelty lies only in exact nonlinear recovery dynamics for a
specific Macaulay orbit.

## What is currently exact

- the round-eight arbitrary-carry first-wall theorem;
- the round-nine all-member logarithmic recovery bound;
- the round-ten exact sharp subsequence;
- exact recurrence checks and finite regression guards for all three links;
- an external novelty preflight recording the He--Tang result and the
  absence of Macaulay terminology in that paper.

## What still blocks submission

- a self-contained derivation of the `K4,r9` recurrence from the underlying
  antichain/Macaulay model, rather than relying on campaign ancestry;
- a clear definition of `rho`, the stable cell, canonical walls, and the
  relevance of this orbit outside the original failed rank-42 route;
- a targeted literature search for the exact recurrence and first-wall
  dynamics; current priority is uncertain;
- blind independent reconstruction of the recurrence semantics, arbitrary
  carry theorem, and all-`R` exponent argument.

The campaign remains in `independent_audit`. The current preflight is not a
substitute for an auditor who has not read the author proof.

## Suggested paper structure

1. Macaulay-orbit model and exact recurrence.
2. Stable cells, canonical walls, and monotonicity of the raise.
3. Every member recovers, but no uniform rank exists.
4. Explicit `O(log j)` recovery bound.
5. Exact sharp subsequence and additive-one comparison.
6. Computational reproducibility and limitations.
7. Relation to the now-known `n_0(r)=2r+o(r)` theorem.
