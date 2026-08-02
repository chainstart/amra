# OPG-1757 transfer-round research log

Date: 2026-08-02 (HKT)

- **20:10--20:17** — Read `SpherePacking.lean`, `MetricCodes.lean`,
  `EhrhartVolumeInequality.lean` and the corresponding official walkthrough
  chapters.  Extracted relaxation/normalization, complete dual/Gram
  certificate, and endpoint/scale-limit patterns.
- **20:17** — Froze `TEN_PROOFS_METHOD_TRANSFER.md` before the 20:30 method
  milestone.
- **20:18--20:27** — Reconstructed the four old common-base sums.  Identified
  the corrected logarithmic height `deg_s-beta_shift`; discovered that the
  old budgets 30/36 had omitted the shift loss.
- **20:27--20:32** — Proved the two complete-channel identities.  Derived the
  positive fixed-index certificate and the two-positive-term page transition.
  Wrote `COMPLETE_LOG_LAYER_THEOREM.md` and its verifier.
- **20:32--20:39** — Tightened the single-threshold quantifiers and the
  low/gap/high integer splice.  Added `CLAIM_LEDGER.md` and `README.md`.
- **20:39** — Completed exact extended stress scan: 89,340 coefficients, 90
  parameters per object, largest `s=10000`, largest `d=2219`; recorded only as
  corroboration.
- **20:40--20:53** — Made the new gap threshold effective.  Split at
  `k=1000`, derived exact fixed-index error bounds and monotone rational
  growing-index bounds, and obtained the 117-digit upper bound in
  `EFFECTIVE_GAP_BOUND.md`.
- **20:53--20:55** — Full local regression: `2 passed`; static firewall and
  wording check; prepared `AUDIT_HANDOFF.md` for author-swap review.

Current mathematical status: new logarithmic gap **proved with an explicit
threshold**; candidate transports **proved eventually complete** after
splicing the old high theorem, but that combined threshold remains
ineffective.  Universal finite-parameter transports, the universal
third-active row, and OPG-1757 remain **OPEN**.
