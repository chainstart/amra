# ARA Local Math Library

This directory stores reusable Lean modules for mathematics that is not yet
available in upstream mathlib, or that needs to be staged before a future
mathlib PR. ARA projects automatically add this library to their Lean search
path during guarded verification.

Code promoted here should be reusable, source-attributed, and free of `sorry`,
`axiom`, `constant`, `opaque`, `admit`, and placeholder markers before it is
treated as a trusted premise.

## Current Trusted Modules

- `AraLibrary.Geometry.TriangleDissection.Shell`: reusable triangle-dissection
  shell infrastructure extracted from `projects/634-campaign-20260421`; this
  is trusted as carrier/API infrastructure, not as a completed geometry theorem.
- `AraLibrary.NumberTheory.Amicable`: elementary proper-divisor-sum and
  amicable-number definitions, including the verified theorem that prime
  numbers are not amicable.
- `AraLibrary.NumberTheory.Korselt`: reusable Korselt-criterion formalization
  extracted from `projects/korselt-criterion-campaign-20260430`; independently
  verified by `build-ara-library` with `sorry_count=0`.
- `AraLibrary.NumberTheory.PrimeTwoPowers`: shell for numbers of the form
  `p + 2^k + 2^l`, with a verified lower-bound obstruction and small
  exceptional-set consequences.
