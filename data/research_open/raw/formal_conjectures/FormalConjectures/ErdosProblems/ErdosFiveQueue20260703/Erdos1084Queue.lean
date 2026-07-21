/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

import Mathlib.Analysis.SpecialFunctions.Sqrt
import FormalConjecturesForMathlib.Geometry.Euclidean
import FormalConjecturesForMathlib.Geometry.Metric
import FormalConjecturesForMathlib.Topology.MetricSpace.MetricSeparated
import FormalConjectures.Util.Attributes.Basic

/-!
# Queue file for Erdős Problem 1084

*References:*
- [Erdős Problems #1084](https://www.erdosproblems.com/1084)
- [Contact numbers for totally separable domains](https://arxiv.org/abs/1601.00145)
  by *Károly Bezdek* and *Muhammad A. Khan*

This file records the local Lean contract needed to use Harborth's planar contact-number
upper bound in the repository's `unitDistNum` convention. The unconditional theorem
`harborth_unitDistNum_upper_ge4` is intentionally not asserted here: the source-level
Harborth theorem is not present in the Lean workspace.

The promoted source theorem would have the following theorem header if a formal source proof
were available:

```lean
theorem Erdos1084.HarborthUnitDistNumUpperGe4Source
    (N : ℕ) (hN : 4 ≤ N) (s : Finset (ℝ^2))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    unitDistNum s ≤
      Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))
```

External source note for this promotion run: the only mathematical source theorem being
packaged here is the Harborth/Bezdek--Khan planar contact-number upper bound cited above.
Iteration 2 re-check: no imported Lean proof of this source theorem was found in the workspace,
so the file keeps only the explicit local contract and wrapper below.
Iteration 3 re-check: searching Mathlib and this repository again found no Lean theorem for
Harborth's planar contact-number bound, so the source theorem remains the blocker.
-/

open scoped EuclideanGeometry

namespace Erdos1084

/--
The source theorem needed for the queued Erdos #1084 promotion: if `s` is a finite
`1`-separated set of `N ≥ 4` points in the Euclidean plane, then its number of unit-distance
pairs is at most `⌊3N - sqrt (12N - 3)⌋`.
-/
def HarborthUnitDistNumUpperGe4Source : Prop :=
  ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
    s.card = N →
    Metric.IsSeparated' 1 (s : Set (ℝ^2)) →
    unitDistNum s ≤ Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))

/--
The explicit theorem shape represented by `HarborthUnitDistNumUpperGe4Source`.
-/
@[category API, AMS 52]
theorem harborth_unitDistNum_upper_ge4_source_iff :
    HarborthUnitDistNumUpperGe4Source ↔
      ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
        s.card = N →
        Metric.IsSeparated' 1 (s : Set (ℝ^2)) →
        unitDistNum s ≤
          Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  rfl

end Erdos1084

/--
Local wrapper from a source-level Harborth contact-number theorem to the repository's
`unitDistNum` formulation.
-/
@[category API, AMS 52]
theorem Erdos1084.harborth_unitDistNum_upper_ge4_of_source
    (hHarborth : Erdos1084.HarborthUnitDistNumUpperGe4Source)
    (N : ℕ) (hN : 4 ≤ N) (s : Finset (ℝ^2))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    unitDistNum s ≤
      Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  exact hHarborth N hN s hcard hsep
