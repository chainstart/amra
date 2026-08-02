# Claim ledger: multi-promotion no-borrow attack

Updated: 2026-08-02 20:39 HKT.

| Claim | Status | Evidence / limitation |
|---|---|---|
| The coordinates \(n=\binom q2+r\), \(n+b-1=\binom{q+c}2+u\) imply \(b=cq+\binom c2+u-r+1\) and the two closed rank-two shadow formulas | **PROVED, UNBOUNDED** | Direct subtraction and canonical concatenation; Section 1 of `MULTI_PROMOTION_NO_BORROW_ATLAS.md` |
| The no-borrow rank-four comparator satisfies \(\gamma_4=U_3(y)-U_3(x)-z-1\) | **PROVED, UNBOUNDED** | Exact cancellation \(x+\tau=z+1\) |
| The positive-cap remainder formula (2.2) and the full-cap deficit formula (3.6) are exact | **PROVED, UNBOUNDED** | Canonical concatenation and direct substitution |
| \(\Lambda_{j,A}(D)-\Lambda_{j,A+g}(E)\ge U_j(D-E)-gE\) for \(D\ge E\) | **PROVED, UNBOUNDED** | Telescope the proved one-cap vertical inequality, then apply deficit superadditivity; Lemma 3.1 |
| Every retained state in \(2\le q\le60, 2\le c\le14\) has \(\gamma_4>0\) | **EXACT FINITE CENSUS** | 85,278 states; zero nonpositive values; minimum 69; independent rank-two closed form and greedy engine agree pointwise |
| No retained state in that box has \(c\ge6\) | **FINITE FILTER OUTPUT ONLY** | The loops do include \(6\le c\le14\), but parity/range/\(\gamma_3<0\)/\(x\ge0\) remove all of them.  This says nothing about larger \(q\), larger boxes, or the unbounded lattice. |
| Every multi-promotion no-borrow state has \(\gamma_4>0\) | **OPEN / CLASSIFICATION TARGET** | The finite census is a falsifier, not an extrapolation.  First-level bounds certify 53,343/85,278 frozen states; the stronger second-level bound leaves only two finite residual rows, but this does not prove global phase exhaustiveness. |
| The second-level exact comparator (2.5) and its positive-remainder lower bound (2.6) hold | **PROVED, UNBOUNDED** | One more canonical expansion; (2.6) uses only \(\rho<s\) and retains \(\binom\sigma2\) |
| Bound (2.6) is positive on the frozen atlas except for two rows | **EXACT FINITE CENSUS** | 85,276/85,278 certified; residual exact values are 354 and 489, and their full canonical words are recorded in (5.2)--(5.5) |
| The phase \(c=2,r=q-1,(a,t)=(q-1,q+1),1\le\delta\le q-2\) has \(\gamma_4>0\) | **PROVED CONDITIONAL UNBOUNDED TEMPLATE / FINITE BASE** | Exact shallow loss (5.8) proves \(q\ge90\); all 20 admissible points with \(q<90\) pass, minimum 186 |
| For each fixed promotion count \(c\ge3\), all sufficiently large \(q\) points seed at rank four, uniformly in \(r,u\) | **PROVED, UNBOUNDED ASYMPTOTIC SLICE THEOREM** | Compact normalized tails obey \(g+S-P\ge c-1\); the exact comparator has limiting numerator at least \(c-2-4/27>0\).  The threshold may depend on \(c\). |
| Any unbounded nonpositive sequence with fixed \(c=2\) must satisfy \(r/q\to1,u/q\to0\) | **PROVED ASYMPTOTIC LOCALIZATION, NOT BY ITSELF POSITIVITY** | The normalized limiting numerator is nonnegative for \(c=2\), and can vanish only at \(D=1\), equivalently \((R,U)=(1,0)\).  The later cap-depth row closes this lower-order boundary. |
| On that boundary, writing \(k=q-r\), every unbounded nonpositive sequence has \(k=O(q^{1/3})\), \(u=O(q^{2/3})\), and \(k+u\to\infty\) | **PROVED ASYMPTOTIC LOCALIZATION / ROOT INDEPENDENT AUDIT PASSED** | Exact same-cap loss transport; it does not prove positivity in the remaining critical window |
| Every normalized limit point \(K=\lim k/q^{1/3}\), \(U=\lim u/q^{2/3}\) of such a bad sequence obeys \(2K+U^2\le3^{2/3}\) | **PROVED ASYMPTOTIC LOCALIZATION / ROOT INDEPENDENT AUDIT PASSED** | Rank-two shadow scaling applied to the exact transported deficit; this row alone leaves the cap, which the next row closes |
| Every fixed-`c=2` relaxed no-borrow point has `gamma_4>0` for all sufficiently large `q` | **PROVED UNBOUNDED ASYMPTOTIC SLICE / INDEPENDENT PROMOTE** | Exact least-cap depths reduce any bad sequence to `k=1`, equal correction `h`, then `h=1,2`; both exact polynomial phases have positive normalized limits.  Not uniform for growing `c`; does not prove the adaptive bridge. |
| Every no-borrow negative antecedent has exactly one promotion | **OPEN** | Equivalent to the previous target only after the precise no-borrow hypotheses are retained; must not be assumed. |
| The fixed rank-five bridge proves Erdős #776 | **REFUTED AS A BRIDGE** | An actual dyadic family violates that bridge and recovers at rank six. |
| Erdős #776 is refuted | **NOT CLAIMED** | A bridge counterexample is not a counterexample to the original problem. |
