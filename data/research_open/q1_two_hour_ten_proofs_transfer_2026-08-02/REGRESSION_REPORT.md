# Regression and reproducibility report

Freeze date: 2026-08-02 HKT  
AMRA research baseline: `669bbad1908e7ab7d8382a8b508e67757006e90c`  
AMRA freeze-time HEAD: `02c7c07fb38ddcccdd38e86ff474681fac53cfd1`
(an unrelated local skill commit created during the research window)  
ten-proofs commit: `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`

## Aggregate results

| Check | Result |
|---|---|
| `lake build All` in the frozen ten-proofs clone | **PASS — 8666 jobs** |
| Two-hour campaign `pytest` suite | **PASS — 25 tests in final rerun, 44.92 s** |
| Previous six-hour campaign regression | **PASS — 151 tests in 514.28 s** |
| OPG main independent audit | **PASS** |
| OPG high-range effectivity audit | **PROMOTE** |
| #1083 main independent audit | **PASS_AFTER_REPAIR** |
| #1083 global fixed-source structure verifier | **PASS** |
| #776 root independent audit | **PASS_AFTER_REPAIR** |
| #776 fixed-`c=2` cap-depth audit | **PROMOTE** |
| #809 independent audit | **PASS_AFTER_REPAIR** |

The Lean rerun was cache-backed but replayed the aggregate target successfully.
The theorem-facing snapshot was also scanned separately from the intentionally
incomplete `ComparatorChallenges/` exercises.

## Independent executable outputs

### OPG-1757

`cross_audit_by_erdos776.py` independently rebuilt the source spectra,
complete-channel exponential generating functions, four effective gap
thresholds, and exact rational growing-index tails.  It returned:

```text
INDEPENDENT OPG1757 CROSS-AUDIT: PASS
spectra: (25,710), (36,1222), (21,525), (31,949)
complete first positive degrees/values: (8,2), (10,2), (8,8), (10,10)
S_gap_digits: 117
```

`cross_audit_high_range_by_erdos776.py` did not import the author certificate.
It rebuilt 80, 120, 68, and 105 lower monomials, exact rational norms, exact
integer thresholds, and the transitive four-component source digest:

```text
INDEPENDENT OPG HIGH-RANGE EFFECTIVITY AUDIT: PROMOTE
thresholds: 102,
  182963662611742278515145357606424176862843,
  75,
  1494048895141509478550315587139453832856
dominated_by_S_gap: True
```

### Erdős #1083

`cross_audit_by_opg1757_independent.py` reconstructed 270 factorial/edit
cases, 3,780 collision ledgers, 227 popular-difference cases, 156 Fourier
masks, the full-transverse debt-one family, and both hostile quantifier
counterexamples.  It returned `PASS_AFTER_REPAIR` after the live proof added
`S>=1` and the signed-residual hypothesis.

`verify_second_scalar_global_structure.py` returned:

```json
{"galois_group_order":48,"original_problem_proved":false,"pass":true,
 "primitive_unordered_gcd_guards_le_60":1101,
 "unbounded_claim_computational_only":false}
```

The unbounded coprimality quantifier comes from the written Galois pair-flip
proof, not from those 1,101 finite guards.

### Erdős #776

`root_independent_audit.py` uses a direct linear Macaulay decomposition and
does not import the author verifier.  It returned:

```text
atlas rows: 85,278; nonpositive gamma4: 0; minimum: 69
second-level positive: 85,276; residual exact values: 354, 489
multi-cap small-domain rows: 252,730
boundary identity rows: 10,033
shallow finite-base rows: 20; minimum: 186
pass: true; original_problem_proved: false
```

The late `CRITICAL_ELLIPSE_FINAL_SCRATCH.md` passed an author-swap audit.
`critical_ellipse_cross_audit_by_opg1757.py` independently reconstructed the
least-cap inequalities and 36,892 canonical rows (35,674 with `m>=3`, 1,218
in the rigid `m=2` phase), returning `PROMOTE`.  The unbounded conclusion is
the written bad-sequence argument, not finite extrapolation.

### Erdős #809

`verify_cross_audit_by_erdos1083.py` did not import the author verifier.  It
returned:

```text
scalar profiles: 13,313,069
feasible profile instances: 26,165,382
sharp graph rows: 18; repeated classes: 144; reserve pairs: 1,245
pass: true; original_problem_proved: false
```

## Key frozen hashes

| Artifact | SHA-256 |
|---|---|
| `opg1757/CLAIM_LEDGER.md` | `950b4aeebe13e9005d2b1201ede456276df38fae1d934e06f64f85833d64822c` |
| `opg1757/HIGH_RANGE_CROSS_AUDIT_BY_ERDOS776.md` | `c5c99cf29ffb500f76fbc8b02300d53bb604e7130666c759429685839fd63a32` |
| `opg1757/cross_audit_high_range_by_erdos776.py` | `bf982323a57370440cab9fad55643267b5f06709325425dbaebe2fa2f27fb0a8` |
| `erdos1083/CLAIM_LEDGER.md` | `05480185a7389cd53f38473ccdd4be095d584fa05540b5b6075cf54ecfda02c7` |
| `erdos1083/SECOND_SCALAR_FINAL_SCRATCH.md` | `77563e1a25c4852102371e96d45c06cd1c2db8a0293316839c827fb0ba149218` |
| `erdos1083/CROSS_AUDIT_BY_OPG1757.md` | `4b4038d68ab02b418797eb6f1ad497822f02809e72ca08eae904271baf3dcda8` |
| `erdos776/MULTI_PROMOTION_NO_BORROW_ATLAS.md` | `0e7e522e4952fe82e5e19f841dd6964850eae7ae0915b5642c4e8e294903171d` |
| `erdos776/root_independent_audit.py` | `a146efdc38b669da0ea7cdeebe10ab323e5e853c447cae41b79eba13ce2f0be9` |
| `erdos776/CRITICAL_ELLIPSE_FINAL_SCRATCH.md` | `2b9c73899945c499f1e7327d2e6a273ffb502e18d513f889eca1cd23bda41d92` |
| `erdos776/CRITICAL_ELLIPSE_CROSS_AUDIT_BY_OPG1757.md` | `46df0f4f22c7633b9e3e485735689af7ab14609e4a18debc29b4a75eceacef8e` |
| `erdos776/critical_ellipse_cross_audit_by_opg1757.py` | `a3655037425067f05750a5fe9b24404be1d525c6ffe51c4216258b5c2a9bc0c8` |
| `erdos809/MAXIMUM_WITNESS_NEAR_SHARP_STABILITY.md` | `4eb83fbe8d3ecaa030215a157d530f09e8f26c2ff7c203c56ca3a0f4bfb153da` |
| `erdos809/verify_cross_audit_by_erdos1083.py` | `2b255afd299c7c64d685a2c3b10746a5aa7e4b3172b1225f800d72b0d63952fe` |

The top-level report and ledger hashes are recorded only after the last audit
repair, in the final freeze manifest, to avoid a self-invalidating hash list.
