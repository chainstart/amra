# Final freeze manifest

Freeze prepared: 2026-08-02 22:06 HKT  
Hard research deadline: 2026-08-02 22:09:56 HKT

## Repository state

- AMRA research baseline:
  `669bbad1908e7ab7d8382a8b508e67757006e90c`.
- AMRA freeze-time HEAD:
  `02c7c07fb38ddcccdd38e86ff474681fac53cfd1`; this is an unrelated local
  `Add standalone AMRA research loop skill` commit made at 21:18:54 while
  this campaign was running.
- AMRA tracked worktree: clean.  The six-hour and two-hour research packages
  are untracked; this campaign did not commit or push them.
- ten-proofs snapshot:
  `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`, clean.

## Final top-level artifacts

| Artifact | SHA-256 |
|---|---|
| `FINAL_REPORT.md` | `1295883d154aec04481acef1b3d860a55443137b408bc5122b8c90bfe1aad54e` |
| `FINAL_CLAIM_LEDGER.md` | `4b1ecabe23f5956a1b2e6cedb537ee6d9b5bfd4ad382dd582fde7023af0cb5e7` |
| `REGRESSION_REPORT.md` | `9080d1a32e0b5641acc743443ee8b50fda304f73f8152b6bc136e903262439df` |
| `TEN_PROOFS_METHOD_ATLAS.md` | `fbd748d4e14925ec8a30147c121dc4fae00a0f48397061557d342aea1587430f` |
| `SOURCE_SNAPSHOT.md` | `b1025fe89660fb3322fb2b32ce62c8a782868914b8a352aa803a40a3e04ae2bc` |

## Admission state

- OPG high-range effectivity: **PROMOTE**.
- #1083 fixed-source global scalar theorem: **PROMOTE**.
- #776 fixed-`c=2` cap-depth closure: **PROMOTE**.
- All other headline lane packages: independent `PASS` or
  `PASS_AFTER_REPAIR` as recorded in `FINAL_CLAIM_LEDGER.md`.
- OPG-1757, Erdős #1083, Erdős #776, and Erdős #809: **all OPEN**.

## Final regression state

- ten-proofs `lake build All`: **PASS**, 8666 jobs.
- current two-hour suite: **25 passed**.
- prior six-hour suite: **151 passed**.
- all six independent cross-audit/certificate commands listed in
  `REGRESSION_REPORT.md`: **PASS/PROMOTE** in their declared scopes.
- `git diff --check`: **PASS**.
- generated `__pycache__` and `.pytest_cache` directories in the two research
  packages: **absent at freeze**.
