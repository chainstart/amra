# Four-problem Q1 campaign: final research report

Date: 2026-07-30

## Executive outcome

The eight-hour parallel campaign completed its four proof attacks, midpoint
reallocation, second attacks on the two strongest routes, independent audits,
regression checks, literature boundary, and publication triage.

\[
\boxed{\text{None of the four named open problems is solved.}}
\]

The strongest closed result is the #809 near-Dirac \(C_7\) anti-Ramsey
theorem.  It is a genuine manuscript-grade unbounded theorem, but novelty
and scope risks currently make it a Q2 candidate / Q1 seed rather than a
secure Q1 headline.  #776 has the highest immediate upside: one remaining
all-\(V\) residual lemma would close the present \(n_0(r)\le2r+5\) route and
answer the bounded-error direction highlighted by He--Tang.  OPG and #1083
produced audited unbounded auxiliary or structural theorems, not a headline
resolution.

## Work allocation actually used

| Window | Work performed | Decision |
|---|---|---|
| H0--H0.5 | Froze public statements, quantifiers, overclaim firewall, and primary-source boundary. | All four lines admitted. |
| H0.5--H4 | Four parallel proof attacks, exact verifiers, and claim ledgers. | Every line produced a real theorem or exact reduction. |
| H4--H4.5 | Independent red-team review of the first open inference. | Freeze #1083 and OPG; concentrate the second half on #809 and #776. |
| H4.5--H7 | #809 fixed-\(s\) Case-1 attack; #776 Lipschitz, moving-block, and reverse rank-18 attacks. | Both routes reduced to one sharp all-parameter lemma; neither was closed. |
| H7--H8 | Independent audits, regression, literature comparison, publication triage, and unified ledger. | No named-problem or guaranteed-Q1 claim permitted. |

The schedule is an allocation of parallel research effort, not a claim that
eight hours of wall time can force an open problem to yield.

## Results by problem

### Erdős #1083

Let \(|X|=S\), let every \(T_\lambda\) be contained in one
\(R\)-element real set, and let the nonzero dilates \(\lambda\) be distinct.
The campaign proves the exact distinct-dilate energy budget
\[
\sum_\lambda E^+(T_\lambda,\lambda X)
\le S\sum_\lambda |T_\lambda|
+
R(R-1)S(S-1),
\]
and uses it inside the audited critical hub to force a synchronized network
of pairwise nonaligned congruent circles.  At the endpoint it obtains
\(t^{35/18-o(1)}\) labels of row degree \(t^{13/18-o(1)}\), together with
\(t^{17/6-o(1)}\) row pairs sharing
\(t^{2/9-\varepsilon-o(1)}\) labels.

This is a useful inverse-structure theorem.  It neither excludes the hub nor
handles the separate matching branch, so it does not improve the recognized
\(3/5\) exponent.

**Minimum next theorem:** one critical endpoint expansion theorem giving a
fixed saving in both the synchronized-hub and plane-pair-matching inputs.

### OPG-1757

For arbitrary \(k,s\ge4\), the fixed-page determinant kernel satisfies
\[
[\beta^r]K_k(s,\beta)>0,\qquad 0\le r\le8.
\]
The new ranks \(5,\ldots,8\) are proved by degree-bounded exact polynomial
identities, not finite parameter extrapolation.  A second theorem gives the
dominant-zero law for the leading long-recurrence layer, including
\(1.961<\rho<1.962\) and an explicit geometric error.

These are strong technical components.  The pooled inversion, all kernel
depths, full complete-split Rayleigh layer, and arbitrary-host transfer
remain open.

**Minimum next manuscript theorem:** all-depth pooled complete-split
positivity.  Even that would still require a separate Rayleigh-preserving
transfer to solve the named arbitrary-host OPG.

### Erdős #809

The campaign proves
\[
e(G)>\lfloor n^2/4\rfloor,\qquad
\delta(G)\ge n/2-o(n)
\Longrightarrow
\text{at least }n^2/8-o(n^2)\text{ colours}
\]
whenever every \(C_7\) is rainbow.  The proof supplies exact-four-path
stability, closes the near-two-clique branch, and removes the independent-side
hypothesis from the near-bipartite core/hub branch.

The second attack unifies the two remaining Case-1 profiles: two induced
edges lie on a common \(C_7\) exactly when one endpoint pairing supports
vertex-disjoint paths of lengths two and three.  If \(M_\gamma\) is the set
of good edges of colour \(\gamma\), the remaining named-problem target is
\[
\sum_\gamma (|M_\gamma|-1)_+=o(n^2).
\]
It also proves that counting only the two inherited dense interiors cannot
reach the target once
\[
s>\frac{1-\sqrt{4/5}}2=0.0527864045\ldots.
\]
Thus a successful proof must charge edges incident with the linear
separator/bad block with bounded congestion.

**Minimum next theorem:** the displayed linkage-defect estimate.

### Erdős #776

The first attack proves the all-parameter implication
\[
D_{16}\le
\binom{V-12}{16}+\binom{V-13}{15}+V-1
\Longrightarrow
D_8<\binom{V-11}{8}
\qquad(V\ge175),
\]
and closes \(40\le V\le174\) by two independent exact engines.  This replaces
the inherited degree-six rank-eight residual condition with a linear
rank-16 condition.

The second attack proves diagonal suspension between adjacent parameter
orbits and shows that the proposed one-Lipschitz residual estimate is exactly
a sharp rank-17 shadow-loss inequality.  A conditional 14-term moving-block
theorem shows that an all-block \(O(\log\log V)\) entry-rank potential would
close the gate; the inherited first-carry theorem does not control those
later chart changes.

A separate reverse rank-18 audit proves that the reverse zero-basin at rank
\(q\) is exactly \([D_q,E_q-1]\).  Consequently the observed reverse
trajectory to zero is equivalent to, rather than a proof of, the candidate
rank-18 lower barrier.  It exposes a sharp forward target: preserve three
consecutive defect-two canonical digits and one further unit as a sufficient
way to dominate the required colex threshold across every borrow chart.
Domination does not require the actual orbit to have those literal digits.

**Minimum next theorem:** for every \(V\ge175\),
\[
D^{[V]}_{16}
\le\binom{V-12}{16}+\binom{V-13}{15}+V-1.
\]

## Verification

The final local regression was:

| Line | Result |
|---|---|
| #1083 | `6 passed`; exact energy, geometry, and endpoint fractions |
| OPG | `4 passed`; all-parameter identity and spectral certificates |
| #809 | `5 passed`; plus 240 random graphs, 684 induced edge pairs, and exact linkage/crossover guards |
| #776 | rank-16 verifier `PASS`; independent finite bridge on \(40\le V\le174\); reverse guard `PASS` with dual-engine agreement through \(V=100\), contiguous checks through \(V=500\), and selected checks to \(V=1000\) |

The written proofs carry the unbounded claims.  Computation supplies
identity checks, finite bridge cases, and falsifier evidence only.

## Publication verdict

Current readiness is
\[
\boxed{\#809\;>\;\#776\;>\;\mathrm{OPG}\;>\;\#1083.}
\]

- #809 is the only present manuscript-grade unbounded theorem nucleus.
- #776 would jump to the strongest result if its one all-\(V\) residual lemma
  were proved.
- OPG and #1083 should remain components of larger, problem-specific papers.
- The four unrelated topics should not be combined into one external paper.

No mathematical audit can guarantee a journal quartile.  Before external
submission, #809 still needs a full prescribed-path novelty search, a
self-contained rewrite of inherited inputs, and an external graph-theory
proof review.

## Recommended next allocation

1. Put the primary proof budget on #809's bounded-congestion
   linkage-defect lemma, because it is the only missing branch after a
   manuscript-grade theorem.
2. Run a parallel high-risk/high-reward #776 program on the all-borrow
   colex-domination invariant exposed by the reverse rank-18 audit.
3. Freeze further fixed-rank OPG coefficient computation and #1083 local
   endpoint counting until a genuinely infinite-depth or two-branch
   expansion mechanism is proposed.

The independent publication assessment is in
`PUBLICATION_TRIAGE_RED_TEAM.md`; every public-facing claim should be checked
against `CLAIM_LEDGER.md`.
