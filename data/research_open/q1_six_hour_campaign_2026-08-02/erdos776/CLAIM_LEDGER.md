# Claim ledger

| Claim | Status | Evidence / dependency |
|---|---|---|
| The inherited synchronized rank-four/rank-five bridge has been independently reconstructed, including quantifiers, borrow states, endpoints, and proof/verifier agreement | **AUDIT IN PROGRESS** | `MOVING_BRIDGE_BLIND_AUDIT.md` |
| The fixed rank-six seed works uniformly | **REFUTED (INHERITED)** | Infinite family \(b=L/2+5\) from the 2026-07-31 campaign |
| Any fixed post-carry rank works uniformly | **REFUTED (INHERITED)** | Paired-tail recurrence on \(b=L/2+5\) |
| Every negative offset \(b-L/2<0\) seeds by rank five | **REFUTED** | The symbolic family \(b=5\) first fails at \(j=17\), with \(\gamma_5=-3051947\) |
| No fixed rank handles the omitted negative half-strip | **PROVED** | `LEFT_OFFSET_FIVE_OBSTRUCTION.md`, fixed-\(b=5\) canonical recurrence |
| On \(b=5\), the exact first seed has rank \(\log_2\log h+O(1)\) for sufficiently large \(h\) | **PROVED** | Stable recurrence plus explicit cap-overflow lower bound |
| On the negative-side double-borrow chamber, the pre-cap constants are strictly minimized at \(b=5\) | **PROVED** | `NEGATIVE_PRECAP_ATLAS.md`, symbolic moving-\(b\) recurrence and monotonicity |
| If that negative-side chamber stays pre-cap through the \(b=5\) candidate, it seeds by \(\log_2\log h+O(1)\) | **PROVED** | Uniform canonicality plus offset monotonicity |
| At a first negative-side cap with \(p\ge4\), neither low block can cross two rank-three walls | **PROVED** | Previous-row canonicality gives the strict gaps (3.7)--(3.8) in `NEGATIVE_PRECAP_ATLAS.md` |
| In the double-borrow chamber, every first cap with \(p\ge4\) is immediately positive for sufficiently large \(h\) | **PROVED** | `NEGATIVE_CAP_RECOVERY.md`, gap invariant plus exhaustive one-wall signs |
| In the double-borrow chamber, an initial negative cap satisfies \(\gamma_3<0\Rightarrow\gamma_4>0\) | **PROVED** | Four exact formulas (3.6), (3.9)--(3.11), independently verified |
| Every moving \(b\ge5\) in the double-borrow chamber seeds by \(\log_2\log h+O(1)\) | **PROVED for sufficiently large \(h\)** | Pre-cap monotonicity plus the two cap-recovery propositions |
| Every negative-offset point in the initial \(x\)-only borrow chamber seeds by rank four | **PROVED** | `NEGATIVE_INITIAL_CHAMBERS.md`; \(q\ge2\) seeds at rank three and the exact \(q=1\) boundary seeds at rank four |
| The no-borrow coordinates, two-level cap legality, tax cancellations, and eventual \(X_1,Y_1>0\) lemma are correct | **PROVED / INDEPENDENT AUDIT PASSED AFTER REPAIR** | `ERDOS776_NEGATIVE_INITIAL_CHAMBERS_RED_TEAM.md`; the strict \(\gamma_5\) sign is explicitly excluded from this audit status |
| Conditional on one rank-two promotion and at most one rank-three wall per low block, \(\gamma_4\) has the exact three-chamber formulas (B) | **PROVED CONDITIONAL NORMAL FORM / INDEPENDENTLY CHECKED** | 219 antecedents through \(b=250\) split \(168/1/50\) and agree pointwise; unbounded single-wall exhaustiveness remains open |
| Under one promotion and two one-wall normalizations, \(\gamma_5\) has one unified full-leading-block identity and the finite chart has exactly six combined chambers through \(b=250\) | **PROVED CONDITIONAL IDENTITY / FINITE CENSUS** | `ONE_PROMOTION_RANK_FIVE_CHART.md`; all 219 identities pass; the six counts are \(164,3,1,1,31,19\) |
| The full-block loss obeys deficit superadditivity and the vertical Lipschitz bound \(\Lambda_{j,A+1}(E)-\Lambda_{j,A}(E)\le E\) | **PROVED / BLIND AUDIT PASSED** | Independently reconstructed from the greedy Macaulay definition in `FINAL_CHAMBER_COUNTERFAMILY_BLIND_AUDIT.md` |
| The rank-two and rank-three convolution lifts hold for every parameter in their stated ranges | **PROVED / BLIND AUDIT PASSED** | Independent engine reproduced the finite minima and rational analytic-tail anchors/derivative slack |
| Five conditional chambers other than \((--)\to(++)\) have \(\gamma_5>0\) uniformly | **PROVED CONDITIONAL / BLIND AUDIT PASSED** | Independent routing and the complete `q<=215` base reproduced all five theorem rows |
| The conditional chamber \((--)\to(++)\) has \(\gamma_5>0\) uniformly | **REFUTED ON THE ACTUAL DYADIC LATTICE / BLIND AUDIT PASSED** | Independent engine verifies \(K=6,r=10,s\equiv2\pmod4,s\ge14\) and \(\gamma_5=4302695-6q<0\) |
| The no-borrow implication (NB)/(2.13) is true | **REFUTED / BLIND AUDIT PASSED** | The family independently passes the full antecedent, dyadic lattice, one promotion, both one-wall legality conditions, and canonical caps |
| The final-chamber counterfamily recovers uniformly at rank six | **PROVED FOR THIS FAMILY / BLIND AUDIT PASSED** | Independent engine treats the nonstable `s=14` word exactly and proves the stable \(s\ge18\) formula; no extrapolation across the cap |
| The open no-borrow antecedent can be reduced to finitely many fixed values of \(K=b-q\) | **REFUTED AS A PROOF ROUTE** | For every fixed \(K\ge4\), an all-parameter \(q\to\infty\) construction gives infinitely many relaxed one-promotion antecedents with \(\gamma_3,\gamma_4<0\) |
| Every initial no-borrow negative point seeds by rank five | **REFUTED** | The actual dyadic final-chamber family has \(\gamma_3,\gamma_4,\gamma_5<0\) for every \(s\ge14\) in its residue class |
| One-promotion and two one-wall normalizations exhaust the full no-borrow antecedent | **OPEN / CLASSIFICATION TARGET** | Exhaustiveness is not needed for the counterfamily, which directly satisfies both premises; it remains relevant to the complementary lattice |
| Every pre-cap positive offset seeds no later than the \(k=5\) adaptive candidate, up to a bounded cap-recovery delay | **OPEN / TARGET** | Fixed-offset monotonicity is inherited, but moving cap crossings remain |
| A uniform adaptive-rank diagonal seed exists on every strip | **OPEN** | The double-borrow and \(x\)-only negative chambers are closed; the rank-five no-borrow route is refuted but its counterfamily recovers at rank six; the complementary no-borrow lattice and positive-side cap transitions remain |
| The rank-42 capacity theorem holds for every \(M\ge67\) | **OPEN** | Inherited consequence of a uniform legal diagonal seed |
| Erdős #776 is solved | **OPEN / NOT CLAIMED** | No complete construction theorem in this directory |
