# Erdős #1083 six-hour campaign: claim ledger

Date: 2026-08-01

| Claim | Status | Evidence / boundary |
|---|---|---|
| Erdős #1083 is solved | **OPEN / NOT CLAIMED** | No global few-distance contradiction or improved exponent is proved. |
| The exact direct-tiling transverse-rank theorem is stable under an unspecified \(o(SU)\) common-spectrum error | **REFUTED** | APPROXIMATE_STABILITY_COUNTEREXAMPLE.md, Theorem 2 |
| There are endpoint-sized near-common spectra with pairwise transverse rank tending to infinity | **PROVED / CONSTRUCTED** | \(t=m^{72}\), \(k=m\), uniform symmetric-difference ratio \(<2(m+1)/m^2\) |
| The construction can be optimized to \(t^{1/18-o(1)}\) transverse spaces with \(o(1)\) relative error | **PROVED / CONSTRUCTED** | Primitive directions \((p,q)\), Theorem 1 and Corollary 2 in SHARP_FOLNER_TRADEOFF_AND_REPAIRED_TARGET.md |
| Every row in the counterexample is exactly injective and has exactly \(SU\) values | **PROVED** | Directional block partition plus remote-block completion |
| The construction respects \(S=t^{7/9}\), \(U=t^{5/6}\), and \(|V|=SU=t^{29/18}\) exactly | **PROVED** | Equations (1.1)--(1.2) |
| The tangent-square union satisfies the endpoint cap \(|\bigcup T_i|\le t\) | **PROVED** | \(|\bigcup T_i|\le kU=m^{61}<m^{72}=t\) |
| In the optimized primitive-direction family the tangent sets are pairwise disjoint and have union \(t^{8/9-o(1)}\) | **PROVED** | Coefficient separation in \(\mathbb Q(\sqrt2)\), equations (3.3)--(3.7) |
| The \(m\) rational dilation spaces are pairwise transverse | **PROVED** | \(W_r=\mathbb Q(1+r\sqrt2)\); coefficient comparison |
| The construction has positive tangent squares and genuine nonaligned reverse-circle rows | **PROVED** | Section 4 and exact algebraic verifier |
| The construction realizes a full \(t^{13/18}\)-row endpoint spectral block | **NO / NOT CLAIMED** | It gives \(k=t^{1/72}\) transverse representatives, sufficient to refute bounded-rank qualitative stability but far fewer than the critical block row count. |
| The construction controls all distances in the resulting Euclidean configuration | **NO / NOT CLAIMED** | The geometry firewall lists uncontrolled cross-row and target-target distances. |
| Stability below the boundary scale \(\sqrt{S/U}=t^{-1/36}\) is false | **OPEN** | The present construction has this scale for finitely many slopes and \(t^{-1/72}\) for its growing family; it gives no lower-scale counterexample. |
| Strong tangent multiplicity or full-block density restores two-cluster rigidity | **OPEN / REFORMULATED TARGET** | These are precisely the inputs discarded by the counterexample. |
| A full \(q=t^{13/18}\) block forces either \(t^{10/9}\) transverse ordered pairs on one tangent or one fixed row--tangent pair shared with \(t^{5/9}\) nontransverse partners | **PROVED** | Strengthened tangent-transversality dichotomy, Theorem 3 |
| Two transverse rows sharing one tangent square have same-tangent cells intersecting in at most one distance label | **PROVED / SHARP** | FIXED_TANGENT_TRANSVERSE_RIGIDITY.md, Theorem 1 |
| A pairwise transverse fixed-tangent support of \(n\) rows determines at least \(nS^2/(S+n-1)\) anchor labels | **PROVED** | Linear-edge packing, Theorem 2 |
| The guaranteed fixed-tangent support already fills the \(SU\) common spectrum | **REFUTED BY EXPONENT AUDIT** | It yields \(t^{4/3}\), short of \(t^{29/18}\) by \(t^{5/18}\). |
| Either branch of the tangent-transversality dichotomy closes #1083 | **OPEN** | Mixed-tangent cycle extraction and bounded-denominator ruled-chart conversion remain unproved. |
| Pigeonholed fixed-difference coincidence records project injectively to \((z,z',x,x')\) | **REFUTED AS STATED** | Two explicit dimension-three hypercube records have one projection; dimension-six multiplicity reaches 16. |
| Some fixed difference supports \(q(q-1)SU/\Sigma_\mu\) distinct projected tuples, where \(\Sigma_\mu=\sum_\delta\max_{z\ne z'}r_{T_z,T_{z'}}(\delta)\) | **PROVED / REPAIRED** | Difference-multiplicity argument in LEGACY_FIXED_DIFFERENCE_COUNT_CORRECTION.md |
| The inherited final \(t^{19/18}\) distinct projected-tuple lower bound survives | **PROVED / REPROVED** | \(\Sigma_\mu\le\sum_\delta r_{T_*}(\delta)=R^2\); no \(U\)-loss is needed. |
| In the transverse-heavy branch, one nonzero difference supports \(t^{8/9+o(1)}\) distinct ordered transverse row pairs | **PROVED** | TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md; zero-difference removal plus global \(\mu\)-budget |
| The fixed nonzero-difference transverse graph has a row of degree \(t^{1/6+o(1)}\) | **PROVED** | Average the \(t^{8/9}\) ordered edges over \(q=t^{13/18}\) rows. |
| The fixed nonzero-difference transverse graph contains a cycle of length at most ten | **PROVED** | Moore/BFS bound; fifth-power degree exponent \(5/6>13/18\). |
| Every such short cycle yields either a nontrivial \(X-X\)-coefficient height relation or a coherent closed \(\pm\delta\) arithmetic-potential walk | **PROVED** | Telescoping identity in BOUNDED_TRANSVERSE_CYCLE_THEOREM.md |
| A coherent short cycle is impossible under adjacent transversality | **REFUTED** | Explicit \(++--\) four-cycle with heights \(\sqrt5,2,\sqrt3,-2\) |
| Coherent cycles of length at most ten have 36 orientation types up to cyclic relabelling and reversal | **PROVED / EXHAUSTIVE FINITE** | Counts \(2,4,9,21\) for lengths \(4,6,8,10\) |
| Every coherent cycle lies on at most six integer potential levels and each level--source pair occurs at most twice | **PROVED** | Quadratic potential normal form in COHERENT_CYCLE_CLASSIFICATION_AND_MODEL.md |
| The fixed nonzero-difference transverse graph contains \(t^{8/9+o(1)}\) pairwise edge-disjoint cycles of length at most ten | **PROVED** | Greedy short-cycle deletion plus the girth bound \(e(H)\le n(n^{1/5}+1)\); exponent margin \(8/9-13/15=1/45\) |
| Either \(t^{8/9+o(1)}\) bounded noncoherent height relations occur, or one coherent orientation type repeats \(t^{8/9+o(1)}\) times | **PROVED** | MANY_BOUNDED_CYCLES_DICHOTOMY.md; pigeonhole over the 36 coherent signatures |
| Two fixed rows are joined by \(t^{16/9+o(1)}\) simple length-15 paths in the fixed-difference graph | **PROVED** | Minimum-degree pruning and exact simple-path multiplication in SHARED_ENDPOINT_PATH_ENERGY.md |
| After fixing both endpoint source labels and the signed orientation sum, \(t^{2/9+o(1)}\) such paths remain | **PROVED** | Divide by \(16S^2\), with \(S^2=t^{14/9}\) |
| A pair of paths in that bundle either has the same internal-defect vector or gives a homogeneous height relation on at most 28 rows | **PROVED** | Exact subtraction of the two telescoped path identities |
| In the zero-common-defect branch, midpoint amplification produces \(t^{1/72+o(1)}\) coherent length-5 paths with the same lifted endpoints and orientation word | **PROVED** | Four iterations of \(N\mapsto(N/q)^{1/2}\) from a length-80 bundle of exponent \(199/18\) |
| Those coherent paths force either a lifted-row hub or an internally vertex-disjoint coherent theta graph with \(t^{1/144+o(1)}\) arms | **PROVED** | Incidence threshold and greedy packing in COHERENT_THETA_AMPLIFICATION.md |
| Two paths with the same nonzero defect vector but different source transitions at a defect row force a noncoherent simple cycle of length at most 160 | **PROVED** | Equal-label half-edge pairing obstruction in DEFECT_TRANSITION_TRICHOTOMY.md |
| In the transition-aligned common-defect branch, one coherent gap compresses to \(t^{1/10+o(1)}\) paths of length at most six with fixed lifted endpoints | **PROVED** | Fixed defect spine, weighted gap energy, and at most 13 row checkpoints; worst exponent \(2201/20160>1/10\) |
| The full common-defect branch forces either a noncoherent bounded cycle or a coherent lifted-row hub/theta graph with \(t^{1/20+o(1)}\) arms | **PROVED** | Defect transition trichotomy plus short-path incidence packing |
| The bounded-cycle network already contradicts the few-distance hypothesis | **OPEN / NOT CLAIMED** | Conversion from many edge-disjoint local charts to one global distance-budget contradiction remains missing. |

The machine verifier is a finite and symbolic certificate for the
explicit construction.  The all-parameter assertions are proved in
the manuscript file; enumeration is not used as a substitute for
their proofs.
