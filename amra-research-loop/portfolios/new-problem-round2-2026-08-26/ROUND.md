# New-problem round 2: Erdős 377 admission

This round excludes the frozen Erdős 25 route and every target already frozen
in the 2026-08-24 and 2026-08-25 discovery portfolios.  The first local-index
screen compared Erdős 124, 538, 709, and 859, but its novelty label for 538 was
wrong because it had not searched every 2026-08-25 portfolio.

The initial choice of Erdős 538 was aborted during the repository-wide novelty
audit: the 2026-08-25 portfolios already contain a squarefree rank-two theorem
and a later dynamic proof-claim exclusion.  Only 38 guarded search seconds were
spent before termination; the aborted campaign is retained as an audit trail.

Erdős 377 is the corrected selection.  It is untouched by prior campaigns and
has an exact Kummer-theorem representation: a prime `p` fails to divide
`binomial(2n,n)` exactly when doubling `n` in base `p` has no carry.  This gives
both a fast exact falsifier and a direct multiscale proof interface.  Erdős 319
has no bounded verifier for its proper-subsum minimality condition; Erdős 374
requires simultaneous exclusion of all shorter factorial-parity relations;
Erdős 686 has an externally active elliptic-curve/square branch.

The corrected admission budget is 5400 guarded search seconds, not counting
the aborted duplicate pilot.  A longer round is earned only if a precise
all-parameter scale inequality survives digit, residue and adversarial CRT
falsification.

## Outcome

The corrected campaign passed a full mechanism admission round but did not
close the public problem.  Ten of twelve mechanisms were killed.  The exact
finite scan found a late new record at `n=1293081501` with reciprocal sum
`1.18050255777032...`, independently replayed by direct Legendre valuations,
and established the finite maximum through two billion.  The large-prime tail
above `sqrt(2n)` was proved uniformly bounded.  The remaining small-prime core
requires a genuinely many-base pointwise rigidity theorem compatible with the
EGRS infinite two-base construction; no precise version survived strongly
enough to earn an automatic extension.  The campaign is therefore frozen and
the next round should switch targets.
