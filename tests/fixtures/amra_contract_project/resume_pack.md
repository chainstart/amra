# AMRA Resume Pack

## Problem State

- Problem: `amra-contract-fixture`
- State: `active_attack`
- Current reason: Fixture keeps one verified Lean declaration and one unresolved route.

## Claims

- `main` status=`route_supported` reusable=no
  - Statement: Fixture Sketch
  - Dependencies: none
  - Evidence: proof_output: tests/fixtures/amra_contract_project/proof/sketches/main.md
- `sketch-claim` status=`sketch` reusable=no
  - Statement: A sketched claim that is useful for research planning but not Lean verified.
  - Dependencies: none
  - Evidence: none

## Routes

- `route-with-gap` status=`blocked` target=`sketch-claim`
  - Core idea: Reduce the claim to reflexivity after a missing normalization lemma.
  - Blocker: Missing normalization lemma.
  - Attempt count: 0
  - Evaluator verdict: none

## Failed Routes

- `route-with-gap` failure_mode=`proof_gap` fingerprint=`fixture-proof-gap`
  - Failed assertion: The normalization lemma needed by the sketch has not been proved in Lean.
  - Approach: Use the sketch as a guide after the missing lemma exists.
  - Failure class: logical
  - Evidence: proof/sketches/main.md
  - Resume only if: Resume only after a Lean statement for the normalization lemma is available.
  - Do not repeat this route unless the resume condition is met.
