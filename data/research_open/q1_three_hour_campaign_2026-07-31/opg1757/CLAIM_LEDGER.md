# OPG-1757 seven-stage claim ledger

Date: 2026-07-31

| Claim | Status | Evidence and scope |
|---|---|---|
| \(P_s^{(2)}(\beta,k)=\lambda^{2s-2k-4}D_k(s,\beta)\) | **PROVED / INHERITED** | Exact nilpotent-page normalization from the previous campaign.  Negative exponents mean exact polynomial divisibility, not a Laurent truncation. |
| \(\deg_\beta D_k=2s+2k-6\) and \([\beta^{2s+2k-6}]D_k=4(k-1)k^{2s-6}s^{2k-4}\) for all \(s\ge4,k\ge2\) | **PROVED / NEW** | Direct 1-, 2-, and 3-component forest calculation in the original bipartite polynomial; it does not invoke the old \(s\ge k+3\) stable-range \(K_k\) argument. |
| \([\beta^{4s-10}]P_s^{(2)}(\beta,k)=4s^{2s-8}(k-1)k^{2s-6}\) for all \(s\ge4,k\ge0\) | **PROVED / NEW** | Follows from the preceding endpoint and exact normalization; \(k=0,1\) vanish. |
| \([\beta^{4s-10}]B_n=4s^{2s-8}n!\bigl({2s-5\brace n}-{2s-6\brace n}\bigr)\) for every \(s\ge4,n\ge0\) | **PROVED / NEW** | Exact Newton inversion and the power-to-Stirling transform. |
| The top-face coefficient is strictly positive exactly for \(2\le n\le2s-5\) | **PROVED / NEW** | \({m+1\brace n}-{m\brace n}=(n-1){m\brace n}+{m\brace n-1}\). |
| \(B_n=0\) for \(n>2s-5\), and the exact nonzero depth range is \(2\le n\le2s-5\) | **PROVED / NEW** | The page-transfer support bound is \(\min\deg_\beta B_n\ge2n\), while the new endpoint gives \(\max\deg_\beta B_n\le4s-10\); the top face proves nonvanishing inside the range. |
| \(B_{2s-5}=4s^{2s-8}(2s-5)!\beta^{4s-10}>_{\rm coeff}0\) | **PROVED / NEW** | The lower and upper degree bounds coincide at the deepest nonzero layer. |
| The displayed three-term formula for \(B_{2s-6}\) is exact and coefficientwise positive for every \(s\ge4\) | **PROVED / NEW** | Binary-merge records become ordinary complete-graph forests; one-extra-spoke records become forests with one ternary hyperedge.  Weighted Cayley component sums close the bottom two coefficients and the Stirling theorem closes the top coefficient. |
| The five-term formula for \(B_{2s-7}\) is exact; it vanishes at \(s=4\) and is coefficientwise strictly positive for every \(s\ge5\) | **PROVED / NEW** | Complete hyperforest excess \(e\le3\), the exact overlap-derivative formula, the denominator-aware Abel lemma, 30 cleared-denominator component identities, and the all-depth top face close all five coefficients.  The independent-audit gap in the former strong interpolation premise has been repaired. |
| The seven-term formula for \(B_{2s-8}\) is exact; it vanishes at \(s=4\) and is coefficientwise strictly positive for every \(s\ge5\) | **PROVED / NEW** | `FOURTH_ATTACK_Q3.md` executes the fixed-deficit reduction at \(q=3\).  All 45 endpoints, 345 Abel certificate values, overlap orders \(0,\ldots,3\), and seven symbolic beta offsets are included.  Positivity follows from coefficientwise-positive expansions after \(s=u+5\). |
| The nine-term formula for \(B_{2s-9}\) is exact; it vanishes at \(s=5\) and is coefficientwise strictly positive for every \(s\ge6\) | **PROVED / NEW** | `FIFTH_ATTACK_Q4.md` executes \(q=4\): 63 endpoints, 588 Abel values, all nine beta offsets, and all overlap orders \(0,\ldots,4\).  After \(s=u+5\), every constant term is zero and every coefficient of \(u,\ldots,u^8\) is positive. |
| The eleven-term formula for \(B_{2s-10}\) is exact; it vanishes at \(s=5\) and is coefficientwise strictly positive for every \(s\ge6\) | **PROVED / NEW** | `SIXTH_ATTACK_Q5.md` executes the full \(84/924\) endpoint route and all overlap orders \(0,\ldots,5\).  Each \(P_r(u+6)\) has eleven strictly positive coefficients. |
| The thirteen-term formula for \(B_{2s-11}\) is exact; it vanishes at \(s=6\) and is coefficientwise strictly positive for every \(s\ge7\) | **PROVED / NEW** | `SEVENTH_ATTACK_Q6.md` executes all \(108\) endpoints, \(1368\) Abel values, and overlap orders \(0,\ldots,6\).  Each \(P_r(u+7)\) has thirteen strictly positive coefficients; an independent sharp-degree certificate checks 208 primitive values. |
| The excess species list through \(e=3\) is exhaustive | **PROVED / NEW** | Excess partitions give: \(e=2\): one 4-edge or two 3-edges; \(e=3\): one 5-edge, a 4-edge plus a 3-edge, or three 3-edges.  Binary edges remain in the contracted ordinary forest. |
| The excess species list through \(e=4\) is exhaustive | **PROVED / NEW** | The five partitions of four give one 6-edge; a 5-edge plus a 3-edge; two 4-edges; a 4-edge plus two 3-edges; or four 3-edges. |
| The excess species list through \(e=5\) is exhaustive | **PROVED / NEW** | The seven partitions of five give all combinations from one 7-edge through five 3-edges; `FIFTH_ATTACK_Q4.md` lists them explicitly. |
| The excess species list through \(e=6\) is exhaustive | **PROVED / NEW** | All eleven partitions of six are present in the exponential contraction formula and are listed in `SIXTH_ATTACK_Q5.md`. |
| The excess species list through \(e=7\) is exhaustive | **PROVED / NEW** | All fifteen partitions of seven are present in the exponential contraction formula used by `verify_seventh_q6.py`; an excess part \(a\) is a hyperedge of size \(a+2\). |
| Exceptional-profile weighted Abel lemma | **PROVED / NEW** | For every fixed exceptional profile \((1^N,v_1,\ldots,v_p)\), \(\mathcal F_c=(\prod v_i)s^{N+p-2c}Q_{\mathbf v,c}(s)\) with \(\deg Q\le2c-2\).  `ABEL_EXCEPTIONAL_PROFILE_LEMMA.md` gives the component EGF, full set-partition recursion, Lagrange extraction, coefficient-preserving pole reduction, and degree ledger. |
| Denominator-aware hyperforest endpoint lemma | **PROVED / NEW** | \(H_{h,e,c}/(2^hs^{s-h-2c-e})=N_{h,e,c}(s)/s^e\) with \(\deg N_{h,e,c}\le2c+3e-2\).  Incidence types use at most \(e+2m\) fresh units and \(m\le e\). |
| The all-\(s\) component endpoint table is exact rather than fitted | **PROVED / PASS** | After clearing \(s^e\), \(2c+3e-1\) points prove one entry.  The main verifier and an independent direct-position engine each check all 180 required values, including \(s=16\) for the three \(e=3,c=1\) entries.  The stronger displayed polynomial degree is now an a posteriori property, not an interpolation assumption. |
| The ordered hyperforest identity \([\beta^{2j+e}]A_{h,j}=j![x^j]\mathcal H_{h,e}\) | **PROVED / PASS** | Contraction gives a weight-preserving bijection; 146 primitive chain endpoints independently agree. |
| The previous component table implies the stated \(C,Q\) formulas | **PROVED / PASS** | `verify_second_deficit.py` now performs the full symbolic simplification, including the \(\lambda^2\) middle coefficient. |
| The component and hyperforest closed forms pass an independent executable audit | **PASS** | `verify_pooled_top_face.py` checks 72 bipartite endpoint pairs, including \(k>s-3\), and the binary/ternary formulas for \(s=4,\ldots,12\). |
| Independent mathematical red-team | **PASS / GAP REPAIRED** | The second audit found the missing proof of the former contraction degree assertion.  The new Abel/pole-reduction proof and 180-value denominator certificate repair it; the independent implementation remains separate from both campaign verifiers. |
| The theorem agrees with the primitive pooled transfer | **PASS / FINITE AUDIT** | All 1140 nonzero primitive coefficients for \(s=4,\ldots,12\) were recomputed; the all-depth top face and both deepest-layer formulas agree exactly.  This finite interior positivity check is not used as an all-\(s\) proof. |
| The complete \(B_{2s-7}\) formula agrees with the primitive pooled transfer | **PASS / FINITE AUDIT** | All five coefficients agree for \(s=5,\ldots,16\), with the exact \(B_1=0\) boundary at \(s=4\); eight second-attack tests and all 15 combined tests pass. |
| The complete \(B_{2s-8}\) formula agrees with non-circular independent engines | **PASS / FINITE AUDIT** | A direct-position contraction engine with an independently implemented labelled-component forest evaluator checks all 345 endpoint values.  The inherited primitive pooling engine checks all seven final coefficients for \(s=5,\ldots,16\), together with \(B_0=0\) at \(s=4\). |
| The complete \(B_{2s-9}\) formula has an independent polynomial-identity certificate | **PROVED / PASS** | The fixed-deficit theorem gives \(\deg R_{4,r}\le r+10\).  The inherited primitive pooling engine independently checks exactly \(r+11\) values for each offset, 135 values total through \(s=24\); hence the nine rational identities follow without trusting the endpoint assembly. |
| The complete \(B_{2s-10}\) formula has an independent polynomial-identity certificate | **PROVED / PASS** | After the boundary factor \((s-4)(s-5)\), the inherited primitive pooling engine checks exactly \(r+11\) values per offset, 176 total through \(s=26\).  This proves all eleven identities without trusting the endpoint assembly. |
| The complete \(B_{2s-11}\) formula has an independent sharp-degree identity certificate | **PROVED / PASS** | The endpoint top-two theorem gives \(\deg R_{6,r}\le12+r\); after \((s-4)(s-5)(s-6)\), only \(10+r\) values are needed.  The inherited primitive pooling engine checks exactly 208 values through \(s=28\), independently of the endpoint assembly. |
| Fixed-depth-deficit finite rational reduction | **PROVED / NEW** | For fixed \(q\ge1\), \(B_{2s-5-q}\) uses \(3(q+2)(q+3)/2\) endpoint types and \(M(q)=(q+2)(q+3)(5q+8)/2\) endpoint values.  For \(q=0\), the exact counts are \(6\) and \(12\).  The normalized offset-\(r\) coefficient has denominator dividing \(s^r\) and cleared numerator degree at most \(2q+r+2\). |
| Endpoint top-two theorem and sharpened coefficient degree | **PROVED / NEW** | The explicit endpoint leading/subleading Laurent terms and transpose cancellation in `../OPG_ENDPOINT_TOP_TWO_THEOREM.md` sharpen the cleared-numerator bound to \(\deg R_{q,r}\le2q+r\).  An independent derivation, EGF audit, transpose audit, and out-of-table \(e=7\) checks pass without reservation. |
| Fixed-deficit boundary-factor theorem | **PROVED / NEW** | For \(F_q(s)=\prod_{j=4}^{\lfloor(q+6)/2\rfloor}(s-j)\), one has \(F_q\mid R_{q,r}\).  `BOUNDARY_FACTOR_THEOREM.md` uses the factorial-free master RHS for negative-depth continuation, so no negative factorial or negative-depth \(B_n\) is defined. |
| Every fixed-depth-deficit layer is coefficientwise positive | **OPEN / NOT CLAIMED** | The finite rational reduction proves computability and degree bounds only.  It does not prove numerator signs or denominator cancellation for arbitrary \(q\). |
| Every coefficient of every \(B_n(s,\beta)\) is nonnegative | **OPEN** | The new results prove the seven deepest layers (including the top face), not arbitrary interior coefficients. |
| Fixed-\((j,q)\) or statewise TP2 can prove the pooled theorem | **FALSE** | The inherited exact obstruction \(-\beta^4(1+\beta)^{s-4}\) remains.  Pooling across active-page unions is essential. |
| The complete disjoint-core \(\alpha^2\) layer for the complete-split family is nonnegative | **OPEN** | Would follow from all \(B_n\ge_{\rm coeff}0\), which is not yet proved. |
| OPG-1757 for arbitrary host graphs is resolved | **OPEN / NOT CLAIMED** | Everything here concerns the complete-split model family and one disjoint-core layer. |
| The new theorem by itself is already a standalone Q1-journal resolution | **NOT ESTABLISHED** | It is a genuine unbounded structural milestone and a plausible substantial paper section.  A Q1-level central result still needs the complete \(\alpha^2\) layer, an all-fixed-codimension theorem, or another comparably broad closure, followed by external novelty review. |

## Literature and priority firewall

- Tang--Zhang, [arXiv:2603.10738](https://arxiv.org/abs/2603.10738),
  studies pairwise negative correlation for uniform spanning subgraphs of
  \(K_n\), including forests with a fixed number of components for
  sufficiently large \(n\).  It does not state this complete-split,
  all-parameter, coefficientwise pooled-kernel theorem.
- Fang--Ma, [arXiv:2604.27755v2](https://arxiv.org/abs/2604.27755),
  proves Rayleigh consequences for Gårding polynomial classes and lists
  series--parallel cycle matroids, uniform matroids, certain modifications,
  and matroids of at most six elements.  No theorem there was found that
  places the present complete-split graphic family in those classes.
- Fang--Ma, [arXiv:2607.16832v1](https://arxiv.org/abs/2607.16832),
  is the newer ideal-Gårding structural preprint.  Its current HTML has no
  occurrence of “forest” or “graphic” and does not instantiate the present
  family.

This is a boundary check against the three closest identified 2026
preprints, not a claim that a full worldwide priority search has been
completed.  The check used the official arXiv records and an independent
OpenAlex fallback search for “complete split graph”, “Rayleigh matroid”,
“forest polynomial”, and “pairwise negative correlation”; the latter
returned Tang--Zhang and Fang--Ma but no additional direct
complete-split theorem.
