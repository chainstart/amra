# AMRA Local Math Library

This directory stores reusable Lean modules for mathematics that is not
yet available in upstream mathlib, or that needs to be staged before a
mathlib PR. AMRA projects add this library to their Lean
search path during guarded verification when they import it.

Code promoted here must be reusable, source-attributed, Lean-verified,
and free of `sorry`, `axiom`, `constant`, `opaque`, `admit`, and
placeholder markers before it is treated as a trusted premise.
