# Final claim ledger — ten-proofs transfer round

Date: 2026-08-02  
Research window: 20:09:56--22:09:56 HKT  
Source snapshot: `openai/ten-proofs@94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`

## Verdict

All four original public problems remain **OPEN**.  The entries below are
stage theorems, exact route obstructions, or finite falsifiers.  None is being
promoted across an unproved interface to the corresponding public problem.

Admission required a written proof, an explicit scope firewall, and an
author-swap reconstruction.  Computation is a proof only for an explicitly
finite census; in an unbounded theorem it is a regression guard rather than
the source of the quantifier.

## Admitted results

| ID | Result | Final status | Exact boundary |
|---|---|---|---|
| OPG-T1 | Complete equal-height aggregation gives the sufficient core `2y^2(y-(1+x)^2)^(p-2)` and page core `2(p-2)x^2(1+x)y^2(y-(1+x)^2)^(p-3)`; after `y=e^(2x)` all relevant fixed-index leading coefficients are positive. | **PROVED / INDEPENDENT AUDIT PASS** | Third-active complete-split transport model only. |
| OPG-T2 | Both actual third-active candidate transports are coefficientwise positive for every `s` at least the displayed 117-digit threshold. | **PROVED, EFFECTIVE EVENTUAL / TWO INDEPENDENT AUDITS PASS** | Not positivity for every finite `s`; not later rows or arbitrary hosts; OPG-1757 remains open. |
| 1083-T1 | The integer potential `delta(q)=1/2 sum_g q(g)(q(g)-1)` bounds mask-edit distance by `2 delta(q)` and gives the exact ordered-autocorrelation and stable-collision ledgers. | **PROVED / PASS AFTER TWO QUANTIFIER REPAIRS** | Needs `S>=1`; the minimum-debt normal form needs `q` signed.  Outer Euclidean extraction is absent. |
| 1083-T2 | The aperiodic mask `P=1+x+x^3+x^5+x^6` has no torsion zero but has torsion-character minimum `O(1/n)` and infinitely often `O(1/n^2)`; an exact signed quotient realizes co-vanishing on the actual residual interface. | **PROVED ROUTE OBSTRUCTION / AUDITED** | Refutes uniform conditioning from aperiodicity, not Erdős #1083. |
| 1083-T3 | For all distinct positive `r,s`, `gcd(P(x^r),P(x^s))=1`.  Thus different absolute scales of this fixed source admit no integral common complement of augmentation `5C` for `1<=C<5`. | **PROVED, UNBOUNDED FIXED-SOURCE THEOREM / INDEPENDENT PROMOTE** | The Galois pair-flip proof supplies the unbounded step.  It says nothing universal about other sources; #1083 remains open. |
| 776-T1 | Exact promotion identities, cap transport, and a second canonical remainder hold unboundedly; an 85,278-state census has minimum `gamma_4=69`, with the stronger bound positive in 85,276 states and two explicitly positive residual rows. | **PROVED IDENTITIES + EXACT FINITE CENSUS / INDEPENDENT AUDIT PASS** | The census is a falsifier, not an extrapolation. |
| 776-T2 | For every fixed promotion count `c>=3`, all sufficiently large `q` points seed at rank four. | **PROVED UNBOUNDED ASYMPTOTIC SLICE / AUDITED** | Threshold may depend on fixed `c`; growing `c` is open. |
| 776-T3 | Any fixed-`c=2` bad sequence lies in `k=O(q^(1/3))`, `u=O(q^(2/3))`, `k+u->infinity`, and obeys `limsup(2k/q^(1/3)+(u/q^(2/3))^2)<=3^(2/3)`. | **PROVED LOCALIZATION / INDEPENDENT AUDIT PASS** | This localization alone does not prove positivity; 776-T4 subsequently closes the cap for fixed `c=2`. |
| 776-T4 | Every fixed-`c=2` relaxed no-borrow point has `gamma_4>0` for all sufficiently large `q`; with 776-T2, every fixed `c>=2` is covered. | **PROVED UNBOUNDED ASYMPTOTIC SLICE / INDEPENDENT PROMOTE** | Exact cap-depth analysis closes the T3 cap.  Threshold depends on fixed `c`; growing promotion counts and the adaptive bridge remain open. |
| 809-T1 | In the standing rainbow-`C_7`, `L_4(2)`, minimum-degree-at-least-three normal form, each colour graph is already an induced matching, with a full independent edge-flip gauge.  Bare two-colour labels are therefore vacuous. | **PROVED ROUTE OBSTRUCTION / INDEPENDENT AUDIT PASS** | A useful invariant must also fix endpoints before the Hall deficit is seen and carry reserve provenance. |
| 809-T2 | The exact parity remainder yields quantitative near-sharp stability, parameter localization, and sharp repeated-`2K_2` families whose whole defect is paid by actual reserve. | **PROVED CONDITIONAL STABILITY / INDEPENDENT AUDIT PASS** | The repeated-colour family is in the audited `L_4(2)` class for `g>=5`; `g=4` is only a graph/colour boundary row.  General label-reserve Hall, other witness branches, and Erdős #809 remain open. |

## Audit decisions

| Author lane | Independent auditor | Decision | Material repair |
|---|---|---|---|
| OPG-1757 main theorem | Erdős #776 lane | **PASS** | None. |
| OPG-1757 high-range effectivity | Erdős #776 lane | **PROMOTE** | Added a transitive four-component source digest before promotion. |
| Erdős #1083 main package | OPG-1757 lane | **PASS_AFTER_REPAIR** | Added `S>=1`; restricted the `delta=1` normal form to signed residuals. |
| Erdős #1083 fixed-source scalar theorem | OPG-1757 lane | **PROMOTE** | One missing display delimiter only. |
| Erdős #776 | Root independent reconstruction | **PASS_AFTER_REPAIR** | Removed a false association between two separately valid phases. |
| Erdős #776 fixed-`c=2` cap closure | OPG-1757 lane | **PROMOTE** | No repair; independent canonical enumeration and symbolic reconstruction passed. |
| Erdős #809 | Erdős #1083 lane | **PASS_AFTER_REPAIR** | TeX command typo only; no mathematical change. |

## Explicit OPG threshold

Both complete candidate transports are positive for every

```text
s >= 557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374
```

The independently reconstructed high-range threshold is only

```text
182963662611742278515145357606424176862843
```

so it is dominated by the displayed gap threshold.

## Public-problem firewall

- OPG-1757 still needs universal finite-`s`, later-row, and arbitrary-host
  interfaces.
- Erdős #1083 still needs a power-large simultaneous bound and the outer
  Euclidean near-extremal extraction.
- Erdős #776 still needs to control growing promotion counts and prove the
  adaptive bridge from the relaxed no-borrow theorem.
- Erdős #809 still needs the fixed-endpoint label-reserve Hall theorem and
  the untreated maximum-witness branches.
