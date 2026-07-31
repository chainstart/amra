# Eight-hour research plan and milestone log — #809

The blocks below are the planned research allocation, not a fabricated
wall-clock claim.  Work was organized to make every block independently
auditable.

| block | planned objective | delivered milestone |
|---|---|---|
| H0--H1 | Reconstruct the exact #809 quantifiers and the BCM26 \(k=3\) failure point. | Confirmed the missing instance is \(C_7\); R004 closes only the near-split branch and Case 1 remains global. |
| H1--H2.5 | Close the R003 near-two-clique/no-three-step branch. | Proved internal minimum degree \(|P|-o(n)\), a dense \(C_7\)-embedding lemma, and an \(n^2/8-o(n^2)\) compatible family. |
| H2.5--H4 | Red-team failure of robust exact-four paths. | Proved the quantified exact-four-path obstruction stability lemma, including adjacency-symmetry/type-product bounds. |
| H4--H5.5 | Close both outputs of the stability lemma. | Closed near-two-clique directly; generalized R004 to near-bipartite graphs using maximum-cut normalization. |
| H5.5--H6.5 | Integrate a global theorem in the near-Dirac regime. | Proved Theorem A with an exhaustive \(L_4(2)\)/failure split. |
| H6.5--H7.5 | Independent finite guards and adversarial boundary cases. | Five tests pass; 33,864 small graphs and 212,888 obstructed profiles checked; non-independent core/hub model brute-forced. |
| H7.5--H8 | Claim audit, publication boundary, next target. | Added `CLAIM_LEDGER.md`, `VERIFICATION.md`, and `FINAL_REPORT.md`; original #809 remains explicitly open. |

## Stop/go decision

The line passes the “substantial theorem” milestone but not the “original
problem solved” milestone.

- **Go** for an expert proof audit and a quantitative BCM Case-2 interface.
- **Go** for a targeted attack on the linearly low-minimum-degree Case 1.
- **Stop** any attempt to market the current package as a proof of #809.
