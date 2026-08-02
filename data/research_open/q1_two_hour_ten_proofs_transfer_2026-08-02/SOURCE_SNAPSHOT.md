# ten-proofs source snapshot

Frozen: 2026-08-02 HKT

- Repository: https://github.com/openai/ten-proofs/tree/main
- Commit: `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`
- Main paper: https://cdn.openai.com/pdf/ten-proofs-oai.pdf
  - SHA-256: `64b900d5fae6fe22f2ae1b8e3b712d20055194a6c81cf343a2455e5898ac7dd6`
- Reasoning walkthroughs: https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf
  - SHA-256: `13b95999f060c0be2142089cfb8b17b75e9231c3c1f3fa0980445ff1b35f0b3b`
- Toolchain: Lean `v4.32.0`, pinned mathlib manifest.
- The ten theorem-facing Lean modules contain no textual `sorry` token.
  The separate `ComparatorChallenges/` exercises deliberately contain holes
  and are not being counted as theorem-facing certificates.
- `MulticolorTriangleRamsey.lean` compiled locally after fetching the pinned
  mathlib cache.
- Full command `lake build All`: **PASS**, `8666` jobs, including all ten
  theorem-facing modules and the aggregate `All` target under Lean 4.32.0.
  The longest modules (`QuantumParallelRepetition`, `ConnesRigidity`,
  `GapCVP`, and `MetricCodes`) were compiled rather than accepted from a
  theorem-project cache.

The GitHub connector failed during initial orientation, so the public web
pages and this clean local shallow clone were used as the documented fallback.
