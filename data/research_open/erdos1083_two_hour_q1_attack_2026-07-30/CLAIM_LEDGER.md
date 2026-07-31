# Erdős #1083 two-hour attack: claim ledger

Date: 2026-07-30.

## 1. Main problem

| Claim | Status | Evidence boundary |
|---|---|---|
| \(f_3(N)\gg N^{3/5+\delta}\) for some fixed \(\delta>0\) | **OPEN** | No route in this package converts the structural matching into a global distance gain. |
| Erdős #1083 is solved | **FALSE AS A DESCRIPTION OF THIS WORK** | The current problem asks for \(N^{2/3-o(1)}\) in dimension three; no exponent above \(3/5\) is proved here. |
| The recognized arbitrary-set baseline remains \(f_3(N)\gg N^{3/5}\) | **VERIFIED AS OF 2026-07-30** | Current Erdős Problems page plus targeted 2025--2026 literature search. |

## 2. Route B: strongest result

| Claim | Status | Evidence |
|---|---|---|
| Fixed-\(A\) reverse circles linearize to distinct lines under \((u,z)\mapsto(z,(u-A)^2+z^2)\), with point-map multiplicity at most two | **PROVED / independently checked** | `route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md`; exact finite verifier. |
| \(I(P_\alpha,\mathcal C)\ll Q^{2/3}R^{1/3}N^{2/3}+RQ+N\) for \(R\) signed centre columns | **PROVED / independently checked** | Fixed-column Szemerédi--Trotter plus Hölder. |
| Fixed-\(A\) target service obeys \(\sum_C\mu(C)\le\min\{L,K_A\}|X_A|\) | **PROVED** | Both \((q,d)\) and \((q,b)\) determine at most one normalized circle. |
| Euclidean hub is impossible for every fixed \(\kappa<2/9\) | **PROVED / independent audit PASS** | Secondary signed-line dyadic layer, rich-line count, target capacity, fixed-column linearization, and inherited general point--circle bound. |
| At least \(t^{1-o(1)}\) labels support rich plane-pair matchings of size \(t^{2/9-\varepsilon-o(1)}\) | **PROVED / structural** | Apply the inherited matching-or-hub theorem at \(\kappa=2/9-\varepsilon\). |
| The scalar method can exclude \(\kappa=2/9\) | **NOT PROVED** | An exact exponent ledger satisfies every scalar inequality used. |
| The \(2/9\) matching theorem improves the global \(3/5\) distance exponent | **NOT PROVED** | Route A shows why matching cells alone do not retain enough endpoint compatibility. |
| \(RNu^4\le t^{-\delta+o(1)}MQ(ML)^2\) holds for some fixed \(\delta>0\) | **OPEN / precise next target** | Target service alone has an exact saturation model; simultaneous source-incidence compatibility remains unproved. |
| The joint saving above would move the matching threshold to \(2/9+\delta/18\) | **PROVED CONDITIONALLY / exact coefficient audit** | `route_e/CONDITIONAL_JOINT_ENDPOINT_THEOREM.md`. |

The earlier \(9/41\) theorem remains correct but is superseded by the
\(2/9\) result.  The conditional \(9/41\) energy note is retained only
as a diagnostic for its parameter-line subsystem.

## 3. Route C: arithmetic structured family

| Claim | Status | Evidence |
|---|---|---|
| Signed five-term cyclotomic rigidity holds when \(\gcd(m,6)=1\) | **PROVED / independent audit PASS** | Mann's theorem plus exclusion of the all-ones pentagon relation by coefficient signs. |
| \(\gcd(m,6)=1\) is the exact threshold for universal selected-label injection | **PROVED / independent audit PASS** | Explicit chord collisions for orders divisible by \(2\) or \(3\). |
| The coaxial fibre distance bound \(|\Delta^2(P)|\ge\sum q_{r,z}\) holds for the rational data in the theorem | **PROVED / independent audit PASS** | Label injection plus Kneser. |
| Equal fibres obey the sharp constant \((\ell-1)/(2\ell)\) | **PROVED / independently checked** | Equality on the regular order-\(\ell\) subgroup. |
| The theorem extends to \(K\subset\mathbb R\) when \(\Phi_m\) stays irreducible over \(K\) | **PROVED / independent audit PASS** | Linear-disjointness/basis argument; sampled over \(\mathbb Q(\sqrt2)\). |
| The arithmetic theorem alone advances arbitrary-set #1083 | **NO** | No extraction theorem forces such a fibre in the critical matching branch. |

## 4. Route A and endpoint barriers

| Claim | Status | Evidence |
|---|---|---|
| A four-plane equal-distance equation is linearly equivalent to \(A\cdot B=0\), rank six and signature \((3,3)\) | **PROVED / exact verifier** | `route_a/FOUR_PLANE_MATCHING_COEFFICIENT_AUDIT.md`. |
| Distinct matching cells force distinct cosine coefficients or chord lengths | **FALSE** | Explicit real and rational countermodels. |
| Matching-selected cells retain the full \(t^{13}\) global energy | **FALSE** | Sharp internal-energy ledger. |
| Label cardinality or one-slope finite-translation non-invariance alone gives a power saving at the old endpoint | **FALSE AS A METHOD CLAIM** | Exact interval service model. |
| Ordinary one-step sum-product on the cross-centre formula reaches the \(t^3\) distance budget | **NO** | The available unconditional exponents are far below \(3\); a genuinely coupled multi-height/multi-slope theorem is still needed. |

## 5. Verification status

At the time of this ledger:

```text
pytest -q data/research_open/erdos1083_two_hour_q1_attack_2026-07-30
54 passed
```

All proof-generating scripts use exact rational or exact cyclotomic
quotient arithmetic where applicable.  The computations are
falsification and exponent certificates; the all-parameter theorems rest
on the written proofs.

## 6. Publication boundary

The \(2/9\) result is the only theorem in this two-hour package with a
credible path to a substantial discrete-geometry paper.  It is not yet
safe to call it a Chinese Academy Q1 result because:

1. the global \(3/5\) exponent is unchanged;
2. the theorem is formulated at an intermediate critical branch;
3. priority for the combined weighted argument has only received a
   targeted, not exhaustive, literature audit.

The six-coprime theorem is mathematically clean but currently has the
scope of a supporting theorem or specialized short note.

An independent paper-readiness red team found no new fatal gap in the
strict conditional \(2/9\) argument, but identified a packaging
blocker: the two-hour directory does not itself contain the upstream
critical-codegree and matching-or-hub proofs.  A submission must either
import that complete dependency chain or state the critical codegree
as an explicit hypothesis and present the result as a conditional
inverse theorem.

The second option has now been implemented as
`route_h/SELF_CONTAINED_CONDITIONAL_THEOREM.md`: it proves the complete
matching-or-hub and \(2/9\) hub-exclusion chain while exposing the cell
cap and critical pair-codegree as assumptions.  It closes the local
exposition gap for a conditional theorem, not the general #1083
reduction or the Q1 significance gap.
