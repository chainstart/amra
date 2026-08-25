# Long proof round 4 — 2026-08-25

This is a time-resident continuation round, not a short mechanism sweep.

- Primary: Erdős #354, 75–90 minutes of guarded exact search and proof work.
- Secondary: Erdős #25, 40–50 minutes of guarded exact search and proof work.
- Audit and packaging: at least 15 minutes after the computational windows.
- Checkpoint cadence: persist evidence at least every 30 minutes of a live attack.
- Early stop: only a complete proof/refutation, an already-existing solution, a
  resource-safety event, or a rigorous no-go covering every admitted mechanism.
- A killed mechanism redirects the remaining time inside the same problem.

All nontrivial computations must run through
`/home/biostar/work/projects/openmath/bin/openmath-memory-guard`.  Productive
search iterations, exact replay, symbolic derivation, and adversarial testing
count as residency; sleeping or idle waiting does not.

## Outcome

The two guarded attacks accumulated 7,123.592 productive seconds before final
replay: 75.00 minutes on #354 and 43.72 minutes on #25.  Together with campaign
construction, proof derivation, replay, and packaging, the round occupied a
little over two hours of sustained work.

- #354 proved an arbitrary-delay no-go and a disjoint residue-core bridge.  An
  exact all-split sparse search then found single-modulus bridge deficits as low
  as -524,291.  The campaign froze behind a dynamic multi-block resume gate.
- #25 proved the exact conditional-layer identity and an unbounded individual
  transient amplifier.  It also certified finite positive-density local
  overshoot, while 10,000 and 100,000 offset searches isolated low-order sparse
  congruence cells as the remaining aggregate obstruction.

Neither public problem was closed.  Mechanical replays passed; independent
mathematical audit and novelty review were deliberately not entered.
