# Round-10 dependency and novelty preflight

Date: 2026-08-06

## Scope

This is a preflight audit, not an independent reconstruction. The reviewer
had already read the author proof before replaying it, so the campaign's
blind-reconstruction gate remains unsatisfied.

The claim under review is only the fixed-family theorem

```text
j_R=11*2^(R-4)-5,  R>=5  =>  rho(j_R)=R+1,
p(j_R)=R+2.
```

It is not a theorem about every adjacent orbit, suffix persistence, the
rank-42 interface, or the public threshold `n_0(r)`.

## Dependency replay

The following commands passed on 2026-08-06:

```sh
cd ../erdos-776-wall-selection-round8
python3 evidence/verify_all_j_first_wall_recovery.py

cd ../erdos-776-recovery-rate-round9
python3 evidence/verify_explicit_recovery_bound.py

cd ../erdos-776-rate-sharpness-round10
python3 evidence/verify_exact_recovery_subsequence.py
```

The replay confirms the displayed recurrences, finite bases, exponent
comparisons, and sampled regression guards. The universal force still comes
from the natural proofs: the finite verifier ranges do not prove the all-`R`
quantifier.

The all-`R` inequalities were also checked line by line:

- `B_5<2^11` and `B_(n+1)<B_n^2` imply
  `B_R^2<2^(11*2^(R-4))`;
- the exact strip formula gives `q_(j_R)>2^(11*2^(R-4))`, hence strict
  stable negativity through rank `R`;
- the round-eight first-wall theorem covers every carry branch at `R+1`;
- in the stable branch, the ratio cone and the lower bound for `B_(R+2)`
  give `D_(R+1)>4q_(j_R)`;
- `2^(R-1)<j_R+4<2^R` gives `p(j_R)=R+2`.

No contradiction was found. This is an author-chain replay, not evidence
level 2 independent reconstruction.

## External novelty boundary

The public context changed before this campaign was created. Yixin He and
Quanyu Tang, *An Erdős--Trotter problem on antichains with multiplicity r on
each occurring level*, arXiv:2602.09803v2 (21 March 2026), proves

```text
2r+2 <= n_0(r) <= 2r+2 log_2 r + O(log_2 log_2 r),
n_0(r)=2r+o(r),
```

and determines `n_0(2)=3`, `n_0(3)=8`.

Primary source:

- https://arxiv.org/abs/2602.09803
- https://arxiv.org/pdf/2602.09803

The paper's searchable text contains no occurrence of "Macaulay",
"Kruskal", or "shadow". That supports, but does not prove, separation from
the local recovery-dynamics theorem. A complete novelty search for the exact
`K4,r9` recurrence and its recovery rank was not completed; priority is
therefore uncertain.

## Publication decision

The round-10 result must not be presented as solving Erdős #776 or improving
the currently known main term. A possible paper requires a different title
and contract: exact recovery dynamics for a specified Macaulay orbit,
including the all-member upper bound, the explicit sharp subsequence, and a
self-contained derivation of the recurrence from the combinatorial model.

Before promotion, a reviewer who has not read the author proof must rebuild
the recurrence semantics, the arbitrary-carry wall theorem, and the
all-`R` sharp subsequence. External priority remains uncertain until a
targeted literature search for this recurrence is complete.
