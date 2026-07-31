# Claim ledger — Erdős #809 line

| ID | Claim | Status | Evidence / boundary |
|---|---|---|---|
| 809-C1 | Erdős #809 is solved for \(C_7\). | **OPEN / NOT CLAIMED** | BCM26 Case 1 can have minimum degree linearly below \(n/2\); this campaign does not control that range. |
| 809-C2 | Every \(n\)-vertex sequence with \(e>\lfloor n^2/4\rfloor\) and \(\delta\ge n/2-o(n)\) requires \(n^2/8-o(n^2)\) colours in every rainbow-\(C_7\) edge-colouring. | **PROVED** | `NEAR_DIRAC_C7_THEOREM.md`, Theorem A. |
| 809-C3 | Failure of one exact-four-edge path in a graph with \(\delta=N/2-o(N)\) forces \(o(N^2)\) edit distance from balanced two-clique or complete-bipartite structure. | **PROVED** | `FOUR_PATH_OBSTRUCTION_STABILITY.md`; quantified error \(O((N-2\delta+1)N)\). |
| 809-C4 | The R003 no-three-step branch with empty common neighbourhood forces enough colours. | **PROVED** | It yields two half-sized, internally \(1-o(1)\)-dense blocks; Lemma 3.1 gives \(n^2/8-o(n^2)\) pairwise compatible edges. |
| 809-C5 | Near-complete-bipartite graphs under the near-Dirac and Mantel-surplus assumptions force enough colours without requiring either side to be independent. | **PROVED** | `MAXCUT_CORE_HUB_THEOREM.md`; maximum-cut normalisation plus generalized core/hub family. |
| 809-C6 | The ten generalized core/hub templates cover core/core, hub/hub, cross-hub, and mixed pairs including same-row and same-column degeneracies. | **PROVED** | Human templates in `MAXCUT_CORE_HUB_THEOREM.md`; independent 14-vertex brute-force guard covers all 496 pairs in a family with core and hub rows, while deliberately adding internal edges to the nominal \(B\)-side. |
| 809-C7 | A distance-two same-colour pair always gives the stated no-three-step certificate after the distance-zero/one cases are excluded. | **PROVED** | `NEAR_DIRAC_C7_THEOREM.md`, Lemma 2.3; 728 finite splices checked. |
| 809-C8 | Theorem A closes the BCM-style \(k=3\) Case-2 induction step after the density cutoff is chosen below the uniform near-Dirac modulus. | **PROVED** | `BCM_CASE2_INTERFACE.md`; Corollary 1 plus equations (21)--(27). This does not claim identity with BCM26's unpublished argument. |
| 809-C8a | The remaining BCM Case 1 reduces exactly to a no-three-step certificate at good-edge distance two or disjoint outer neighbourhoods at good-edge distance three. | **PROVED** | `CASE1_OBSTRUCTION_REDUCTION.md`, Proposition 3. The parameterized colour bound inside those profiles remains open. |
| 809-C8b | For two induced edges, common membership in a \(C_7\) is equivalent to a vertex-disjoint endpoint linkage by paths of lengths two and three. | **PROVED** | `CASE1_SECOND_ATTACK.md`, Lemma 1; the finite guard independently checks 684 induced edge pairs. |
| 809-C8c | Under the fixed-\(s\) Case-1 contract, \(\sum_\gamma(|M_\gamma|-1)_+=o(n^2)\). | **OPEN / UNIQUE CLOSURE TARGET** | This total linkage-defect estimate would convert the good-edge count into the full colour bound.  Bounded-congestion charging is missing. |
| 809-C8d | Counting only the two inherited dense interiors reaches the BCM target for every fixed \(s\). | **FALSE** | Even under favourable colour separation, the guaranteed bound falls below the target for \(s>(1-\sqrt{4/5})/2\). |
| 809-C9 | The new results are globally novel and sufficient by themselves for a Q1 journal. | **UNVERIFIED** | Search found BCM26 as the closest direct work, but no exhaustive MathSciNet/zbMATH citation-chain audit or external graph-theory review has been performed. |
| 809-C10 | Finite verification proves the asymptotic theorem. | **FALSE / GUARDED** | `VERIFICATION.md` explicitly limits computation to identities, templates, and arithmetic. |

## Strongest safe abstract sentence

> We prove that every graph sequence with more than the Mantel number of
> edges and minimum degree \(n/2-o(n)\) has maximal \(C_7\) anti-Ramsey
> number at least \(n^2/8-o(n^2)\); the proof establishes a new stability
> dichotomy for exact-four-path obstructions and a maximum-cut core/hub
> theorem for the near-bipartite branch.

This sentence is safe only as a statement of the local proof package.  The
word “new” requires literature clearance before external use.
