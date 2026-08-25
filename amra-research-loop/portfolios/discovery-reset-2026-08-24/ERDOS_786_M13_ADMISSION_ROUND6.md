# Erdős #786 M13 admission audit, Round 6

## Decision

Do not initialize a successor campaign from `M786G-13` in this round.

The periodic baseline

\[
B_Q=\{1\}\cup\{n:Q\mid n\}
\]

is explicit and noncircular.  The required residual transversals `T_k` are
not.  The Round 4 artifact proves `CR.1`: if a sequence of sublinear residual
transversals with summable prefix-Carleson recourse is supplied, it yields the
desired coherent deletion set.  It does not select that sequence or prove its
recourse estimate.

## Candidate selector audit

| candidate | admission result | reason |
|---|---|---|
| arbitrary or lexicographically first optimum | fail | merely solves the finite transversal problem separately at every scale; no adjacent-scale structure follows |
| nested optimums | fail | nestedness is a stronger unproved coherence hypothesis |
| optimum minimizing change from `T_k` | fail | puts recourse in the objective but gives no summable prefix bound |
| restriction of a pre-existing infinite transversal | fail | circularly assumes the global object being constructed |

Without a selector there is no well-defined first pair `T_k,T_{k+1}` to
falsify, no proposed sequence `rho_k`, and hence no executable kill test with
the stated mathematical scope.  `MC.1` and `CR.2` remain exact obstructions
to density-one and endpoint-only recourse formulations, respectively, but
neither refutes the repaired prefix-Carleson mechanism.

## Reopening gate

Reconsider `M786G-13` only when all three items exist together:

1. an explicit arithmetic rule selecting `T_k` from the `B_Q`-residual
   hypergraph;
2. a precise all-parameter prefix-Carleson rate claim for that rule; and
3. a finite executable falsifier for the first claimed inequality.

Until then the mechanism is a legitimate conditional interface but not an
admitted research campaign.  This audit neither refutes `M786G-13` nor changes
the open status of Erdős #786.
