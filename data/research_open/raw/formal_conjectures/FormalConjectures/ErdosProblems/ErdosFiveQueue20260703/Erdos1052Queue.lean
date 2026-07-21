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

import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Data.Nat.Prime.Basic
import FormalConjectures.Util.Attributes.Basic

/-!
# Queue file for Erdős Problem 1052

*References:*
- [Erdős Problems #1052](https://www.erdosproblems.com/1052)
- [Bounded-box reductions in the Subbarao-Warren problem for unitary perfect numbers]
  (https://arxiv.org/abs/2605.20475) by *Tom Maciejewski*
- [Higgs prime](https://en.wikipedia.org/wiki/Higgs_prime)

The proof-lab route identified the statement below as a source-level blocker, not as local
Lean glue: one still needs a theorem that, for all sufficiently large primes `p`,
`2 ^ (2 * p) + 1` has a prime divisor that is not a `3`-Higgs prime.

External source note for this promotion run: the arXiv source describes this as the remaining
divisor-level obstruction for the `Φ_{4p}(2)` branch and gives bounded-box/frontier results,
not an unconditional finiteness theorem.

Additional source note: the Higgs-prime reference records that infinitude is not known for
any fixed exponent greater than `1`, so this branch cannot currently be discharged by citing
a known finiteness theorem for `3`-Higgs primes.

Source search note, 2026-07-03: a fresh check of arXiv:2605.20475 and the Higgs-prime
reference found the same blocker. The promoted theorem would have the following header if a
formal source proof or rigorous citation were available:

Iteration 2 note, 2026-07-03: rechecking arXiv:2605.20475 again identified this as the
remaining divisor-level task for `Φ_{4p}(2)`, with bounded/frontier and thinness results but
not an unconditional eventual-failure theorem. A small SymPy probe of prime branches
`p ≤ 31` found both early failures and early all-3-Higgs branches, so there is no immediate
small-prime contradiction replacing the needed source theorem.

Iteration 3 note, 2026-07-03: reviewing the proof-lab bundle and supervisor decisions again
left the same blocker. The Lean file contains the proved local wrapper
`threeHiggs_phi4p_eventual_failure_of_source`; promoting the assumption-free theorem below
would require the external divisor-level theorem.

Iteration 4 note, 2026-07-03: the next formalizer pass re-read the proof-lab context and
math-tools report. No finite local lemma or rigorous citation was supplied beyond the
recorded arXiv and Higgs-prime references, so the first blocker remains the external
eventual non-`3`-Higgs prime divisor theorem for `2 ^ (2 * p) + 1`.

Iteration 5 note, 2026-07-03: a live source search again found arXiv:2605.20475, whose
abstract/status text states that Ford thinness is unconditional but not finiteness and that
the remaining task is the divisor-level problem for `Φ_{4p}(2)`. The Higgs-prime reference
was also rechecked for terminology, not as a proof of the eventual branch theorem.

Iteration 6 note, 2026-07-03: the final formalizer iteration re-read the proof-lab bundle,
the math-tools report, arXiv:2605.20475, and the Higgs-prime reference. No new local Lean
lemma, finite certificate, or rigorous citation was found. The exact first blocker remains
the external source theorem asserting eventual existence of a non-`3`-Higgs prime divisor
of `2 ^ (2 * p) + 1` for prime `p`.

Iteration 7 note, 2026-07-03: the next source check again found arXiv:2605.20475 as a
bounded-box/frontier result whose abstract leaves finiteness to a divisor-level problem for
`Φ_{4p}(2)`, and the Higgs-prime reference only supplies terminology and the lack of a known
infinitude theorem for fixed exponent greater than `1`. No cited eventual branch theorem or
finite local certificate was identified.

Iteration 8 note, 2026-07-03: a fresh source search again found arXiv:2605.20475 as the
only relevant source-level result, explicitly stopping short of finiteness and isolating the
`Φ_{4p}(2)` divisor problem. A recursive SymPy check of prime branches `p ≤ 31` again found
mixed behavior: some branches already have a non-`3`-Higgs divisor, while others have all
factored prime divisors passing the recursive `3`-Higgs test. This is finite route evidence
only, not a Lean certificate or source proof of eventual failure.

Iteration 9 note, 2026-07-03: the final supervised Lean pass re-read the proof-lab bundle
and math-tools report, then rechecked the live arXiv and Higgs-prime source entries. The
arXiv abstract still presents the `Φ_{4p}(2)` divisor problem as the remaining task rather
than a proved theorem, and the Higgs-prime entry supplies terminology plus the lack of a
known infinitude result for fixed exponent greater than `1`. No rigorous citation or finite
computable certificate was supplied that could prove the assumption-free theorem below.

Iteration 10 note, 2026-07-03: this formalizer pass re-read the proof-lab bundle and
math-tools report, then rechecked the live arXiv and Higgs-prime source entries. The arXiv
record for arXiv:2605.20475 again describes Ford thinness and finite-frontier evidence, but
not finiteness; it identifies the remaining task as a divisor-level problem for
`Φ_{4p}(2)`. The Higgs-prime reference again supplies only terminology and the statement
that infinitude is not known for fixed exponents greater than `1`. Thus the theorem below
remains an external source theorem rather than local Lean glue.

Iteration 11 note, 2026-07-03: this pass re-read the proof-lab bundle and math-tools report,
then rechecked arXiv:2605.20475 and the Higgs-prime reference. The arXiv abstract still
states that Ford thinness is not finiteness and leaves the remaining task as a divisor-level
problem for the cyclotomic values `Φ_{4p}(2)`. A small SymPy cyclotomic sanity check also
corrected the branch wording: for odd prime `p`, `2 ^ (2 * p) + 1` is `5 * Φ_{4p}(2)`, not
literally `Φ_{4p}(2)`. The extra factor `5` is a `3`-Higgs prime for the finite-witness
definition below, so this correction does not supply the needed non-`3`-Higgs divisor; the
assumption-free theorem remains an external source theorem.

Iteration 12 note, 2026-07-03: this final formalizer iteration re-read the proof-lab bundle
and math-tools report, then rechecked arXiv:2605.20475 and the Higgs-prime reference. The
arXiv entry still states that the paper proves bounded-box/frontier and thinness results but
not finiteness, with the remaining task being a divisor-level problem for `Φ_{4p}(2)`. The
Higgs-prime reference supplies terminology and notes that infinitude is not known for fixed
exponents greater than `1`. No source theorem, finite computable certificate, or local Lean
lemma was supplied that could prove the assumption-free theorem without adding a trusted
assumption.

Iteration 13 note, 2026-07-03: this run again re-read the proof-lab context bundle and
math-tools report, then rechecked the live arXiv:2605.20475 and Higgs-prime entries. The
arXiv abstract still explicitly stops at bounded-box/frontier results plus Ford thinness and
states that the remaining task is a divisor-level problem for `Φ_{4p}(2)`, while the
Higgs-prime entry remains only a terminology/background source. No new rigorous citation or
finite certificate was found that would turn `ThreeHiggsPhi4pEventualFailureSource` into a
provable local Lean theorem.

Iteration 14 note, 2026-07-03: this pass re-read the proof-lab context bundle and
math-tools report, then rechecked arXiv:2605.20475 and the Higgs-prime reference. The arXiv
record still says the paper proves bounded-box/frontier and thinness results, but not
finiteness, and leaves the remaining task as a divisor-level problem for `Φ_{4p}(2)`. The
Higgs-prime reference again supplies terminology and background, not an eventual branch
theorem. Thus the assumption-free theorem below remains blocked on an external source result
or an explicit finite certificate.

Iteration 15 note, 2026-07-03: this final Lean pass re-read the proof-lab bundle and
math-tools report, then repeated the live source check. arXiv:2605.20475 still records only
bounded-box/frontier results, Ford thinness, and a precise remaining divisor-level task for
the `Φ_{4p}(2)` branch. The Higgs-prime reference still supplies the finite-witness
terminology and notes that infinitude is not known for fixed exponents greater than `1`.
No source theorem or finite certificate was found that could prove the assumption-free
target without introducing a new trusted assumption.

Iteration 16 note, 2026-07-03: this pass re-read the proof-lab bundle and math-tools report,
then rechecked arXiv:2605.20475, the Higgs-prime reference, and exact-string web searches
for the promoted theorem shape. The arXiv entry still presents the result as an open
divisor-level target for `Φ_{4p}(2)`, not a proved theorem; the Higgs-prime entry remains
background terminology. No independent citation, local finite certificate, or Lean lemma
was identified that could prove the assumption-free target.

Iteration 17 note, 2026-07-03: this pass again re-read the proof-lab bundle and
math-tools report, then refreshed exact-string searches plus arXiv:2605.20475 and the
Higgs-prime reference. The arXiv abstract still states that Ford thinness is not
finiteness and leaves a divisor-level problem for `Φ_{4p}(2)`; the Higgs-prime page still
only supplies the finite-witness terminology and background. No source theorem, explicit
finite certificate, or smaller theorem-level Lean target was identified.

Iteration 18 note, 2026-07-03: this pass again re-read the proof-lab bundle and
math-tools report, then refreshed the live source check for arXiv:2605.20475 and the
Higgs-prime reference. The arXiv record still says the paper proves bounded-box/frontier
and thinness results but not finiteness, with the remaining task being a divisor-level
problem for `Φ_{4p}(2)`. The Higgs-prime reference remains terminology/background for the
finite-witness predicate, not an eventual branch theorem. No rigorous source theorem,
finite certificate, or local Lean target was found that would prove the assumption-free
statement below.

Iteration 19 note, 2026-07-03: this run re-read the proof-lab context bundle and
math-tools report, then rechecked the live arXiv:2605.20475 and Higgs-prime entries. The
arXiv abstract still presents bounded-box/frontier data and Ford thinness as stopping short
of finiteness, with the remaining task being a divisor-level theorem for `Φ_{4p}(2)`. The
Higgs-prime entry again supplies terminology and background, including that infinitude is
not known for fixed exponents greater than `1`. No cited source theorem, finite certificate,
or smaller theorem-level Lean target was identified.

Iteration 20 note, 2026-07-03: this pass again re-read the proof-lab context bundle and
math-tools report, then rechecked the live arXiv:2605.20475 and Higgs-prime entries. The
arXiv record still says the paper proves bounded-box/frontier results and a thinness bound,
but explicitly not finiteness; it leaves the remaining task as a divisor-level problem for
`Φ_{4p}(2)`. The Higgs-prime reference remains terminology/background and does not supply
an eventual branch theorem. A small SymPy sanity probe for odd primes `3 ≤ p ≤ 31` verified
the corrected identity `2 ^ (2 * p) + 1 = 5 * Φ_{4p}(2)` in those cases and displayed the
corresponding factorizations, but this is route evidence only and not a finite certificate
for the eventual theorem. No source theorem, computable certificate, or smaller local Lean
target was identified.

Iteration 21 note, 2026-07-03: this final pass re-read the proof-lab context bundle and
math-tools report, then refreshed exact source searches and the live arXiv:2605.20475 and
Higgs-prime entries. The arXiv record still presents bounded-box/frontier evidence and
Ford thinness, not finiteness, and names the remaining task as a divisor-level problem for
`Φ_{4p}(2)`. The Higgs-prime reference remains only terminology/background for fixed
exponents greater than `1`. No cited source theorem, finite computable certificate, or
smaller theorem-level Lean target was found, so the theorem below is still blocked on the
external proposition `ThreeHiggsPhi4pEventualFailureSource`.

Iteration 22 note, 2026-07-03: this pass re-read the proof-lab context bundle and
math-tools report, then repeated the live source check for arXiv:2605.20475 and the
Higgs-prime reference. The arXiv record still describes bounded-box/frontier results and
Ford thinness, not a finiteness theorem, and leaves the remaining step as the divisor-level
problem for `Φ_{4p}(2)`. The Higgs-prime reference remains terminology/background and does
not supply an eventual theorem for exponent `3`. No source theorem, explicit finite
certificate, or smaller local Lean target was identified that would prove
`ThreeHiggsPhi4pEventualFailureSource` without adding a trusted assumption.

Iteration 23 note, 2026-07-03: this run re-read the proof-lab context bundle and
math-tools report, then rechecked arXiv:2605.20475, the Higgs-prime reference, and
exact-string searches for the branch statement. The arXiv abstract still says the paper
proves bounded-box/frontier and thinness results, not finiteness, and leaves the remaining
task as a divisor-level problem for `Φ_{4p}(2)`. The Higgs-prime reference remains
terminology/background and does not supply an eventual theorem for exponent `3`. No cited
source theorem, explicit finite certificate, or smaller local Lean theorem was identified.

Iteration 24 note, 2026-07-03: this iteration re-read the proof-lab context bundle and
math-tools report, then repeated live searches for arXiv:2605.20475, the Higgs-prime
reference, and exact branch statements involving `2 ^ (2 * p) + 1` and `Φ_{4p}(2)`. The
arXiv source still classifies the paper's rigorous contribution as bounded-box/frontier
and thinness results, with finiteness left to the divisor-level cyclotomic problem. The
Higgs-prime reference again supplies only terminology/background for fixed exponent `3`.
Thus there is still no rigorous source theorem, explicit finite certificate, or local Lean
lemma that would prove the assumption-free target below.

Iteration 25 note, 2026-07-03: this promotion attempt re-read the proof-lab context bundle
and math-tools report, then refreshed the live source check for arXiv:2605.20475 and the
Higgs-prime reference. The arXiv entry still states that Ford thinness is not finiteness
and leaves the remaining task as a divisor-level problem for `Phi_{4p}(2)`, while the
Higgs-prime reference only supplies the recursive Higgs-prime terminology and the absence
of a known infinitude theorem for fixed exponents greater than `1`. No theorem suitable for
`ThreeHiggsPhi4pEventualFailureSource`, explicit finite certificate, or smaller local Lean
target was identified.

Iteration 26 note, 2026-07-03: this pass re-read the proof-lab context bundle and
math-tools report, then refreshed the live arXiv:2605.20475 and Higgs-prime sources plus
exact branch searches. The arXiv record still marks bounded-box/frontier results and Ford
thinness as rigorous but explicitly not finiteness, with the remaining analytic target being
a divisor-level theorem for `Φ_{4p}(2)`. The Higgs-prime page again supplies the recursive
fixed-exponent terminology and says infinitude is unknown for exponents greater than `1`.
No external theorem, explicit finite certificate, or smaller local Lean theorem was found
that could prove `ThreeHiggsPhi4pEventualFailureSource` without adding a trusted assumption.

Iteration 27 note, 2026-07-03: this final promotion pass re-read the proof-lab context
bundle and math-tools report, then refreshed the live source check for arXiv:2605.20475 and
the Higgs-prime reference. The arXiv source still separates rigorous bounded-box/frontier
and thinness results from the unproved finiteness step, explicitly leaving the remaining
task as a divisor-level problem for `Φ_{4p}(2)`. The Higgs-prime reference still provides
only the recursive fixed-exponent terminology and says infinitude is unknown for exponents
greater than `1`. Thus the displayed assumption-free theorem remains blocked on an
external theorem or explicit finite certificate for `ThreeHiggsPhi4pEventualFailureSource`.

Iteration 28 note, 2026-07-03: this new promotion target was checked against the proof-lab
round-005 summary and supervisor decision. The requested `UPN_seed_closure_bound` contract is
the exact-balance source/certificate theorem
`∃ A, ∀ N, Nat.UnitaryPerfect N → Nat.factorization N 2 > A → False`. The current first
blocker is that no concrete cited theorem or finite certificate proves
`∀ a > A, ¬ ∃ N, Nat.UnitaryPerfect N ∧ Nat.factorization N 2 = a`; the Lean code below only
records the local source proposition and wrapper.

Iteration 29 note, 2026-07-03: this pass re-read the proof-lab bundle and math-tools report,
then refreshed the source check against Erdős Problems #1052, arXiv:2605.20475, and the
Higgs-prime background entry. Erdős Problems #1052 still marks finiteness of unitary perfect
numbers as open; the arXiv source still gives bounded-box/frontier and thinness results,
not a global seed-exponent bound; and the Higgs-prime entry remains terminology/background
rather than a theorem for the needed branch. The Lean-side defect that the promoted name was
missing is repaired below by naming the local source wrapper `UPN_seed_closure_bound`; this
does not prove the assumption-free contract without `UPNSeedClosureBoundSource`.

Iteration 30 note, 2026-07-03: this run re-read the proof-lab context bundle, the
math-tools report, and the round-005 supervisor decision. The live source check again found
Erdős Problems #1052 explicitly open, arXiv:2605.20475 proving bounded-box/frontier and
thinness results but not finiteness, and the Higgs-prime reference only supplying background
terminology plus the absence of a known infinitude theorem for fixed exponents greater than
`1`. Exact-string searches for the promoted Lean names and for a global `2`-adic bound found
no independent source theorem or finite certificate for
`∃ A, ∀ N, Nat.UnitaryPerfect N → Nat.factorization N 2 > A → False`.

```lean
theorem threeHiggs_phi4p_eventual_failure :
  ∃ P : ℕ, ∀ p : ℕ,
    Nat.Prime p →
    P ≤ p →
      ∃ q : ℕ,
        Nat.Prime q ∧ q ∣ 2 ^ (2 * p) + 1 ∧ ¬ IsThreeHiggsPrime q
```
-/

namespace Nat

/--
A proper unitary divisor of `n` is a proper divisor `d` of `n` that is coprime to `n / d`.
This repeats the repository convention in the `Nat` namespace for source-level queue
statements that use `Nat.UnitaryPerfect`.
-/
def properUnitaryDivisors (n : ℕ) : Finset ℕ :=
  {d ∈ Finset.Ico 1 n | d ∣ n ∧ d.Coprime (n / d)}

/--
A natural number is unitary perfect when it is positive and equals the sum of its proper
unitary divisors.
-/
def UnitaryPerfect (n : ℕ) : Prop :=
  ∑ i ∈ properUnitaryDivisors n, i = n ∧ 0 < n

end Nat

namespace Erdos1052

/--
A finite-witness formulation of a `3`-Higgs prime: `q` belongs to a finite set of primes in
which every member `r` has `r - 1` dividing the cube of the product of smaller members.
-/
def IsThreeHiggsPrime (q : ℕ) : Prop :=
  ∃ s : Finset ℕ, q ∈ s ∧
    ∀ r ∈ s, Nat.Prime r ∧ r - 1 ∣ (∏ p ∈ (s.filter fun p => p < r), p) ^ 3

/--
Any prime admitted by the finite-witness `3`-Higgs predicate is prime.
-/
@[category API, AMS 11]
theorem IsThreeHiggsPrime.prime {q : ℕ} (hq : IsThreeHiggsPrime q) : Nat.Prime q := by
  rcases hq with ⟨s, hqs, hs⟩
  exact (hs q hqs).1

/--
A composite or non-prime natural number cannot satisfy the finite-witness `3`-Higgs predicate.
-/
@[category API, AMS 11]
theorem not_isThreeHiggsPrime_of_not_prime {q : ℕ} (hq : ¬ Nat.Prime q) :
    ¬ IsThreeHiggsPrime q := by
  intro h
  exact hq h.prime

/--
Sanity check for the finite-witness definition: the extra `Φ₄(2)` factor in
`2 ^ (2 * p) + 1 = 5 * Φ_{4p}(2)` for odd prime branches is itself `3`-Higgs.
-/
@[category test, AMS 11]
theorem isThreeHiggsPrime_five : IsThreeHiggsPrime 5 := by
  refine ⟨{2, 3, 5}, by decide, ?_⟩
  intro r hr
  simp only [Finset.mem_insert, Finset.mem_singleton] at hr
  rcases hr with rfl | rfl | rfl
  · decide
  · decide
  · decide

/--
The source theorem needed for the queued Erdos #1052 route: eventually every prime branch
`2 ^ (2 * p) + 1` has a prime divisor that is not `3`-Higgs.
-/
def ThreeHiggsPhi4pEventualFailureSource : Prop :=
  ∃ P : ℕ, ∀ p : ℕ,
    Nat.Prime p →
    P ≤ p →
      ∃ q : ℕ,
        Nat.Prime q ∧ q ∣ 2 ^ (2 * p) + 1 ∧ ¬ IsThreeHiggsPrime q

/--
The explicit theorem shape represented by `ThreeHiggsPhi4pEventualFailureSource`.
-/
@[category API, AMS 11]
theorem threeHiggs_phi4p_eventual_failure_source_iff :
    ThreeHiggsPhi4pEventualFailureSource ↔
      ∃ P : ℕ, ∀ p : ℕ,
        Nat.Prime p →
        P ≤ p →
          ∃ q : ℕ,
            Nat.Prime q ∧ q ∣ 2 ^ (2 * p) + 1 ∧ ¬ IsThreeHiggsPrime q := by
  rfl

/--
Local wrapper from the source-level cyclotomic branch theorem to the exact branch-failure
statement needed by the proof-lab route.
-/
@[category API, AMS 11]
theorem threeHiggs_phi4p_eventual_failure_of_source
    (hSource : ThreeHiggsPhi4pEventualFailureSource) :
    ∃ P : ℕ, ∀ p : ℕ,
      Nat.Prime p →
      P ≤ p →
        ∃ q : ℕ,
          Nat.Prime q ∧ q ∣ 2 ^ (2 * p) + 1 ∧ ¬ IsThreeHiggsPrime q := by
  exact hSource

/--
The source theorem needed for the exact-balance route to Erdős #1052: there is a global
bound on the exponent of `2` in any unitary perfect number.
-/
def UPNSeedClosureBoundSource : Prop :=
  ∃ A : ℕ, ∀ N : ℕ,
    Nat.UnitaryPerfect N →
    Nat.factorization N 2 > A →
    False

/--
The explicit theorem shape represented by `UPNSeedClosureBoundSource`.
-/
@[category API, AMS 11]
theorem UPN_seed_closure_bound_source_iff :
    UPNSeedClosureBoundSource ↔
      ∃ A : ℕ, ∀ N : ℕ,
        Nat.UnitaryPerfect N →
        Nat.factorization N 2 > A →
        False := by
  rfl

/--
Local wrapper from the source-level exact-balance theorem to the queued seed-closure bound.
-/
@[category API, AMS 11]
theorem UPN_seed_closure_bound_of_source
    (hSource : UPNSeedClosureBoundSource) :
    ∃ A : ℕ, ∀ N : ℕ,
      Nat.UnitaryPerfect N →
      Nat.factorization N 2 > A →
      False := by
  exact hSource

/--
Local wrapper with the promoted target name. This records the exact Lean implication that
is available without adding a trusted assumption: the assumption-free contract still needs
the external source theorem `UPNSeedClosureBoundSource`.
-/
@[category API, AMS 11]
theorem UPN_seed_closure_bound
    (hSource : UPNSeedClosureBoundSource) :
    ∃ A : ℕ, ∀ N : ℕ,
      Nat.UnitaryPerfect N →
      Nat.factorization N 2 > A →
      False := by
  exact UPN_seed_closure_bound_of_source hSource

end Erdos1052
