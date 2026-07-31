# Claim ledger — Erdős #809 breakthrough campaign

Date: 2026-07-31

| ID | Claim | Status | Evidence / boundary |
|---|---|---|---|
| 809-Z1 | For a zero-shore missing pair \(bc\subset B\), every distinct pair in \(N_B(b)\widehat\times N_B(c)\) is missing in \(G[B]\). | **PROVED** | Otherwise it is the middle edge of a three-edge \(b\)-to-\(c\) shore path. |
| 809-Z2 | The star-plus-neighbourhood set \(\mathcal K(bc)\) in (3) consists only of missing \(B\)-edges. | **PROVED** | `NINTH_ATTACK_RESERVE_HALL.md`, Lemma 3.1. |
| 809-Z2a | Its size is at least \(\bar d_B(b)+\bar d_B(c)-1+\binom{\min(d_B(b),d_B(c))}{2}\). | **PROVED** | The two missing stars meet only in \(bc\); the forced rectangle is disjoint and has the stated minimum. |
| 809-Z3 | If the zero-shore defect tokens have an SDR in their reserves after the nonempty-shore base charges are removed, then \(D_B\le M_B\). | **PROVED** | Exact Hall injection, Theorem 4.1. |
| 809-Z4 | Failure of that charge produces the compressed Hall-deficiency certificate (7). | **PROVED** | Hall's theorem; tokens with the same base pair have identical lists. |
| 809-Z4a | A Hall-deficient token set simultaneously has fewer than \(T+|C_+|\) incident missing-star edges and fewer than \(T+|C_+|\) forced neighbourhood-rectangle edges. | **PROVED** | Both unions are contained in the deficient reserve union; Corollary 4.4. |
| 809-Z5 | The balanced three-clique-chain obstruction satisfies the reserve matching with \(D_B=M_B=k^2\). | **PROVED / TESTED** | Every token sees the full missing block \(U\times W\); tests cover \(3\le k\le30\). |
| 809-Z6 | The unbalanced three-hub obstruction satisfies the reserve matching. | **PROVED / TESTED** | For \(g\) active groups, Hall margin is \(u(w-g)+g\ge0\); 117 regression instances pass. |
| 809-Z7 | The full fixed-\(s\) maximum-degree contract always admits a root choice giving the reserve matching or an aligned complete core. | **OPEN — BOLD PRIMARY TARGET** | This is the reserve-expansion conjecture.  Finite falsification and known families support it but do not prove it. |
| 809-Z8 | The reserve-Hall theorem alone closes all repeated good colours. | **FALSE AS STATED / GUARDED** | It controls the outer-\(B\) defect \(D_B\); the outer-\(A\) residue \(R_A=D_A-D_B\) still needs \(R_A\le S_m\) or another charge. |
| 809-Z9 | Erdős #809 is solved. | **OPEN / NOT CLAIMED** | The universal reserve-expansion theorem, the \(R_A\) interface, and the other BCM witness branches remain open. |

## Decision

The old objective “make zero-shore congestion \(o(n^2)\)” is retired.
The exact next object is Hall expansion of the forced outside reserves.
This uses the global unused missing-edge supply and automatically pays
the two strongest full-contract counterfamilies that defeated the
moment approach.
