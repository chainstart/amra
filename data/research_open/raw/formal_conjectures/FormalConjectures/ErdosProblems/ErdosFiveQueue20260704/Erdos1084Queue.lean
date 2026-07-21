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
- H. Harborth, "Lösung zu Problem 664A", *Elemente der Mathematik* 29 (1974), 14-15
- [Contact numbers for totally separable domains](https://arxiv.org/abs/1601.00145)
  by *Károly Bezdek* and *Muhammad A. Khan*

This file records the local Lean contract needed to use Harborth's planar contact-number
upper bound in the repository's `unitDistNum` convention. The unconditional theorem is
not asserted here: the source-level Harborth theorem is not present in the Lean workspace.

The mathematical source certificate needed upstream is the Harborth/Bezdek--Khan planar
contact-number bound
`c(n, 2) = floor (3 * n - sqrt (12 * n - 3))` for the relevant convention of
non-overlapping congruent disks. Lean only verifies the local wrapper from that source
certificate to the repository's `unitDistNum` formulation.

Source-audit note for this promotion: the campaign supervisor accepted Bezdek--Khan
Theorem 3.1 of arXiv:1601.00145, which states the planar contact-number formula and
cites Harborth's 1974 result, as the external certificate. This file does not assert
that source theorem unconditionally.

Round 2 formalizer note: this wrapper relies only on the local Harborth source note and
keeps the external contact-number theorem as the explicit hypothesis below.
-/

open scoped EuclideanGeometry

namespace Erdos1084

/-- The maximal number of unit-distance pairs among `n` many `1`-separated points in `ℝ^d`. -/
noncomputable def f (d n : ℕ) : ℕ :=
  ⨆ (s : Finset (ℝ^d)) (_ : s.card = n)
    (_ : Metric.IsSeparated' 1 (s : Set (ℝ^d))), unitDistNum s

/--
The number of contact pairs in a finite set of centers when contact distance is `2`.
-/
noncomputable def contactDistTwoNum (s : Finset (ℝ^2)) : ℕ :=
  (s.sym2.filter fun p => dist p.out.1 p.out.2 = 2).card

/--
The source theorem needed for the queued Erdős #1084 promotion: if `s` is a finite
`1`-separated set of `N ≥ 4` points in the Euclidean plane, then its number of unit-distance
pairs is at most `⌊3N - sqrt (12N - 3)⌋`.
-/
def HarborthUnitDistNumUpperGe4Source : Prop :=
  ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
    s.card = N →
    Metric.IsSeparated' 1 (s : Set (ℝ^2)) →
    unitDistNum s ≤ Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))

/--
The external Harborth contact-number source in the disk-center convention: finite
`2`-separated center sets have at most `⌊3N - sqrt (12N - 3)⌋` pairs at distance `2`.
-/
def HarborthTwoSeparatedContactUpperGe4Source : Prop :=
  ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
    s.card = N →
    Metric.IsSeparated' 2 (s : Set (ℝ^2)) →
    contactDistTwoNum s ≤ Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3))

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

/--
The explicit theorem shape represented by `HarborthTwoSeparatedContactUpperGe4Source`.
-/
@[category API, AMS 52]
theorem harborth_twoSeparated_contact_upper_ge4_source_iff :
    HarborthTwoSeparatedContactUpperGe4Source ↔
      ∀ (N : ℕ), 4 ≤ N → ∀ (s : Finset (ℝ^2)),
        s.card = N →
        Metric.IsSeparated' 2 (s : Set (ℝ^2)) →
        contactDistTwoNum s ≤
          Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  rfl

private lemma two_smul_injective : Function.Injective (fun x : ℝ^2 => (2 : ℝ) • x) := by
  intro x y hxy
  have h := congrArg (fun z : ℝ^2 => ((2 : ℝ)⁻¹) • z) hxy
  simpa [smul_smul] using h

private lemma dist_out_eq_of_eq_sym2_mk {p : Sym2 (ℝ^2)} {x y : ℝ^2} (hp : p = s(x, y)) :
    dist p.out.1 p.out.2 = dist x y := by
  have hmk : Sym2.mk p.out = Sym2.mk (x, y) := by
    exact p.out_eq.trans hp
  have hrel : Sym2.Rel (ℝ^2) p.out (x, y) := Sym2.exact hmk
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, h₂⟩ | ⟨h₁, h₂⟩
  · simp [h₁, h₂]
  · simp [h₁, h₂, dist_comm]

private lemma dist_out_sym2_map_two_smul (p : Sym2 (ℝ^2)) :
    dist (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.1
        (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.2 =
      2 * dist p.out.1 p.out.2 := by
  have hmap :
      Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p =
        s((2 : ℝ) • p.out.1, (2 : ℝ) • p.out.2) := by
    have hmap' :
        Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) (Sym2.mk p.out) =
          s((2 : ℝ) • p.out.1, (2 : ℝ) • p.out.2) := by
      cases p.out
      rfl
    exact (congrArg (Sym2.map fun x : ℝ^2 => (2 : ℝ) • x) p.out_eq).symm.trans hmap'
  rw [dist_out_eq_of_eq_sym2_mk hmap]
  simp [dist_smul₀]

private lemma dist_out_sym2_map_two_smul_eq_two_iff (p : Sym2 (ℝ^2)) :
    dist (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.1
        (Sym2.map (fun x : ℝ^2 => (2 : ℝ) • x) p).out.2 = 2 ↔
      dist p.out.1 p.out.2 = 1 := by
  rw [dist_out_sym2_map_two_smul]
  constructor
  · intro h
    have hnonneg : 0 ≤ dist p.out.1 p.out.2 := dist_nonneg
    nlinarith
  · intro h
    nlinarith

private lemma contactDistTwoNum_image_two_smul_eq_unitDistNum (s : Finset (ℝ^2)) :
    contactDistTwoNum (s.image fun x : ℝ^2 => (2 : ℝ) • x) = unitDistNum s := by
  classical
  unfold contactDistTwoNum unitDistNum
  rw [Finset.sym2_image]
  rw [Finset.filter_image]
  rw [Finset.card_image_of_injective _ (Sym2.map.injective two_smul_injective)]
  exact congrArg Finset.card (Finset.filter_congr fun p _ =>
    dist_out_sym2_map_two_smul_eq_two_iff p)

private lemma two_smul_image_isSeparated_two {s : Finset (ℝ^2)}
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    Metric.IsSeparated' 2 ((s.image fun x : ℝ^2 => (2 : ℝ) • x) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated'] at hsep ⊢
  intro x hx y hy hxy
  rw [Finset.mem_coe, Finset.mem_image] at hx hy
  rcases hx with ⟨x₀, hx₀, rfl⟩
  rcases hy with ⟨y₀, hy₀, rfl⟩
  have hxy₀ : x₀ ≠ y₀ := by
    intro h
    apply hxy
    simp [h]
  have hsep₀ := hsep (by simpa using hx₀) (by simpa using hy₀) hxy₀
  have hdist₀ : (1 : ℝ) ≤ dist x₀ y₀ := by
    have hsep₀' : (1 : ENNReal) ≤ edist x₀ y₀ := by
      simpa using hsep₀
    rw [edist_dist, ← ENNReal.ofReal_one] at hsep₀'
    exact (ENNReal.ofReal_le_ofReal_iff dist_nonneg).1 hsep₀'
  rw [edist_dist, dist_smul₀]
  have hreal : (2 : ℝ) ≤ ‖(2 : ℝ)‖ * dist x₀ y₀ := by
    norm_num
    nlinarith
  simpa using (ENNReal.ofReal_le_ofReal hreal)

/--
Local wrapper from the Harborth contact-number source theorem in the `2`-separated
disk-center convention to the repository's `unitDistNum` convention.
-/
@[category API, AMS 52]
theorem harborth_unitDistNum_upper_ge4_of_twoSeparated_contact_source
    (hHarborth : HarborthTwoSeparatedContactUpperGe4Source) :
    HarborthUnitDistNumUpperGe4Source := by
  intro N hN s hcard hsep
  have hcard_image :
      (s.image fun x : ℝ^2 => (2 : ℝ) • x).card = N := by
    rw [Finset.card_image_of_injective _ two_smul_injective, hcard]
  have hcontact :=
    hHarborth N hN (s.image fun x : ℝ^2 => (2 : ℝ) • x) hcard_image
      (two_smul_image_isSeparated_two hsep)
  rwa [contactDistTwoNum_image_two_smul_eq_unitDistNum] at hcontact

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

/--
Promoted conditional theorem for the queued triangular-optimal route. This is the local
Lean wrapper from the accepted Harborth/Bezdek--Khan source certificate to the repository's
`unitDistNum` convention; it deliberately keeps the external source theorem as an explicit
hypothesis.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_of_source
    (hHarborth : Erdos1084.HarborthUnitDistNumUpperGe4Source)
    (N : ℕ) (hN : 4 ≤ N) (s : Finset (ℝ^2))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    unitDistNum s ≤
      Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  exact Erdos1084.harborth_unitDistNum_upper_ge4_of_source hHarborth N hN s hcard hsep

/--
A one-point finite Euclidean configuration has no unordered unit-distance pair.
-/
@[category API, AMS 52]
theorem Erdos1084.unitDistNum_eq_zero_of_card_one {d : ℕ}
    (s : Finset (ℝ^d)) (hcard : s.card = 1) :
    unitDistNum s = 0 := by
  classical
  rw [Finset.card_eq_one] at hcard
  rcases hcard with ⟨x, rfl⟩
  have hdiag :
      dist (Sym2.diag x).out.1 (Sym2.diag x).out.2 = 0 := by
    have hmk : Sym2.mk (Sym2.diag x).out = Sym2.mk (x, x) := by
      simp [Sym2.diag]
    have hrel : Sym2.Rel (ℝ^d) (Sym2.diag x).out (x, x) := Sym2.exact hmk
    rw [Sym2.rel_iff] at hrel
    rcases hrel with ⟨h₁, h₂⟩ | ⟨h₁, h₂⟩ <;> simp [h₁, h₂]
  simp [unitDistNum, hdiag]

/--
A one-point planar configuration has no unordered unit-distance pair.
-/
@[category API, AMS 52]
theorem Erdos1084.f_two_one_eq_zero : Erdos1084.f 2 1 = 0 := by
  classical
  refine le_antisymm ?_ (Nat.zero_le _)
  unfold Erdos1084.f
  refine ciSup_le' ?_
  intro s
  refine ciSup_le' ?_
  intro hcard
  refine ciSup_le' ?_
  intro _hsep
  exact le_of_eq (Erdos1084.unitDistNum_eq_zero_of_card_one s hcard)

private lemma Erdos1084.triangular_harborth_floor (n : ℕ) :
    Nat.floor
      (3 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) -
        Real.sqrt (12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3)) =
        9 * n ^ 2 + 3 * n := by
  have hrad :
      12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3 =
        (((6 * n + 3 : ℕ) : ℝ)) ^ 2 := by
    norm_num [Nat.cast_add, Nat.cast_mul, Nat.cast_pow]
    ring
  have hmain :
      3 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) -
          Real.sqrt (12 * ((3 * n ^ 2 + 3 * n + 1 : ℕ) : ℝ) - 3) =
        ((9 * n ^ 2 + 3 * n : ℕ) : ℝ) := by
    rw [hrad, Real.sqrt_sq_eq_abs, abs_of_nonneg]
    · norm_num [Nat.cast_add, Nat.cast_mul, Nat.cast_pow]
      ring
    · positivity
  rw [hmain, Nat.floor_natCast]

namespace Erdos1084

private noncomputable def triangularPoint (i j : ℤ) : ℝ^2 :=
  !₂[(i : ℝ) + (j : ℝ) / 2, (Real.sqrt 3 / 2) * (j : ℝ)]

private lemma triangularPoint_injective :
    Function.Injective (fun p : ℤ × ℤ => triangularPoint p.1 p.2) := by
  rintro ⟨i, j⟩ ⟨i', j'⟩ h
  have h₀ := congrArg (fun x : ℝ^2 => x 0) h
  have h₁ := congrArg (fun x : ℝ^2 => x 1) h
  simp only [triangularPoint, PiLp.toLp_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Fin.isValue] at h₀ h₁
  have hsqrt_ne : Real.sqrt 3 / 2 ≠ (0 : ℝ) := by positivity
  have hj_real : (j : ℝ) = j' := by
    exact mul_left_cancel₀ hsqrt_ne h₁
  have hj : j = j' := by exact_mod_cast hj_real
  subst hj
  have hi_real : (i : ℝ) = i' := by nlinarith
  have hi : i = i' := by exact_mod_cast hi_real
  subst hi
  rfl

private lemma triangularPoint_dist_east (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint (i + 1) j) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint]

private lemma triangularPoint_dist_north (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint i (j + 1)) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  nlinarith

private lemma triangularPoint_dist_southeast (i j : ℤ) :
    dist (triangularPoint i j) (triangularPoint (i + 1) (j - 1)) = 1 := by
  rw [EuclideanSpace.dist_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  nlinarith

private lemma int_quadratic_ge_one (a b : ℤ) (h : a ≠ 0 ∨ b ≠ 0) :
    (1 : ℤ) ≤ a ^ 2 + a * b + b ^ 2 := by
  have hid : (2 * (a ^ 2 + a * b + b ^ 2) : ℤ) = a ^ 2 + (a + b) ^ 2 + b ^ 2 := by
    ring
  by_cases hb : b = 0
  · subst hb
    rcases h with ha | hbzero
    · ring_nf
      have hpos : (0 : ℤ) < a ^ 2 := sq_pos_of_ne_zero ha
      omega
    · contradiction
  · by_cases hab : a + b = 0
    · have hbpos : (0 : ℤ) < b ^ 2 := sq_pos_of_ne_zero hb
      nlinarith
    · have habpos : (0 : ℤ) < (a + b) ^ 2 := sq_pos_of_ne_zero hab
      have hsq_a : (0 : ℤ) ≤ a ^ 2 := sq_nonneg a
      have hsq_b : (0 : ℤ) ≤ b ^ 2 := sq_nonneg b
      nlinarith

private lemma triangularPoint_dist_sq (i j i' j' : ℤ) :
    dist (triangularPoint i j) (triangularPoint i' j') ^ 2 =
      (((i - i') ^ 2 + (i - i') * (j - j') + (j - j') ^ 2 : ℤ) : ℝ) := by
  rw [EuclideanSpace.dist_sq_eq, Fin.sum_univ_two]
  simp [triangularPoint, Real.dist_eq, sq_abs]
  have hsqrt_sq : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  ring_nf
  rw [hsqrt_sq]
  ring

private lemma triangularPoint_edist_ge_one_of_ne {i j i' j' : ℤ}
    (h : (i, j) ≠ (i', j')) :
    (1 : ENNReal) ≤ edist (triangularPoint i j) (triangularPoint i' j') := by
  have hdiff : i - i' ≠ 0 ∨ j - j' ≠ 0 := by
    by_contra hzero
    push_neg at hzero
    apply h
    ext <;> omega
  have hquad := int_quadratic_ge_one (i - i') (j - j') hdiff
  have hquad_real :
      (1 : ℝ) ≤
        (((i - i') ^ 2 + (i - i') * (j - j') + (j - j') ^ 2 : ℤ) : ℝ) := by
    exact_mod_cast hquad
  have hsq := triangularPoint_dist_sq i j i' j'
  have hdist_nonneg : 0 ≤ dist (triangularPoint i j) (triangularPoint i' j') := dist_nonneg
  rw [edist_dist, ← ENNReal.ofReal_one]
  apply ENNReal.ofReal_le_ofReal
  nlinarith

/--
The axial-coordinate hexagonal ball
`{(i,j) : |i| ≤ n, |j| ≤ n, |i+j| ≤ n}` as a finite set of integer pairs.
-/
private def triangularHexCoords (n : ℕ) : Finset (ℤ × ℤ) :=
  ((Finset.Icc (-(n : ℤ)) (n : ℤ)).product (Finset.Icc (-(n : ℤ)) (n : ℤ))).filter
    fun p => -(n : ℤ) ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ (n : ℤ)

private lemma mem_triangularHexCoords {n : ℕ} {p : ℤ × ℤ} :
    p ∈ triangularHexCoords n ↔
      -(n : ℤ) ≤ p.1 ∧ p.1 ≤ (n : ℤ) ∧
      -(n : ℤ) ≤ p.2 ∧ p.2 ≤ (n : ℤ) ∧
      -(n : ℤ) ≤ p.1 + p.2 ∧ p.1 + p.2 ≤ (n : ℤ) := by
  simp [triangularHexCoords, and_assoc]

/-- The embedded triangular-lattice hexagonal patch. -/
private noncomputable def triangularHexPatch (n : ℕ) : Finset (ℝ^2) :=
  (triangularHexCoords n).image fun p : ℤ × ℤ => triangularPoint p.1 p.2

private lemma triangularHexPatch_card_eq_coords_card (n : ℕ) :
    (triangularHexPatch n).card = (triangularHexCoords n).card := by
  classical
  unfold triangularHexPatch
  rw [Finset.card_image_of_injective _ triangularPoint_injective]

private lemma triangularHexPatch_oneSeparated (n : ℕ) :
    Metric.IsSeparated' 1 ((triangularHexPatch n : Finset (ℝ^2)) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated']
  intro x hx y hy hxy
  rw [Finset.mem_coe, triangularHexPatch, Finset.mem_image] at hx hy
  rcases hx with ⟨p, _hp, rfl⟩
  rcases hy with ⟨q, _hq, rfl⟩
  have hpq : p ≠ q := by
    intro hpq
    apply hxy
    rw [hpq]
  exact triangularPoint_edist_ge_one_of_ne hpq

private abbrev triangularHexPointIndex (n : ℕ) :=
  (Sigma fun k : Fin (n + 1) => Fin (n + k.1 + 1)) ⊕
    (Sigma fun k : Fin n => Fin (n + k.1 + 1))

private def triangularHexPointCoord (n : ℕ) : triangularHexPointIndex n → ℤ × ℤ
  | Sum.inl p => ((-(p.1.1 : ℤ) + (p.2.1 : ℤ)), (-(n : ℤ) + (p.1.1 : ℤ)))
  | Sum.inr p => ((-(n : ℤ) + (p.2.1 : ℤ)), ((n : ℤ) - (p.1.1 : ℤ)))

private lemma triangularHexPointIndex_card_aux (n : ℕ) :
    (∑ k : Fin (n + 1), (n + k.1 + 1)) + (∑ k : Fin n, (n + k.1 + 1)) =
      3 * n ^ 2 + 3 * n + 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1 + 1) => n + 1 + k.1 + 1)]
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1) => n + 1 + k.1 + 1)]
      simp only [Fin.val_castSucc, Fin.val_last]
      have hfirst : (∑ i : Fin (n + 1), (n + 1 + i.1 + 1)) =
          (∑ i : Fin (n + 1), (n + i.1 + 1)) + (n + 1) := by
        simp_rw [show ∀ i : Fin (n + 1),
            n + 1 + i.1 + 1 = (n + i.1 + 1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin (n + 1) => (n + i.1 + 1) + 1) =
          (Finset.univ.sum fun i : Fin (n + 1) => n + i.1 + 1) + (n + 1)
        rw [Finset.sum_add_distrib]
        simp
      have hsecond : (∑ i : Fin n, (n + 1 + i.1 + 1)) =
          (∑ i : Fin n, (n + i.1 + 1)) + n := by
        simp_rw [show ∀ i : Fin n, n + 1 + i.1 + 1 = (n + i.1 + 1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin n => (n + i.1 + 1) + 1) =
          (Finset.univ.sum fun i : Fin n => n + i.1 + 1) + n
        rw [Finset.sum_add_distrib]
        simp
      rw [hfirst, hsecond]
      nlinarith [ih]

private lemma triangularHexPointCoord_injective (n : ℕ) :
    Function.Injective (triangularHexPointCoord n) := by
  intro a b h
  cases a with
  | inl a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexPointCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl
      | inr b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexPointCoord] at h
          have hb_lt : (bk.1 : ℤ) < n := by exact_mod_cast bk.2
          have ha_le : (ak.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ ak.2
          omega
  | inr a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexPointCoord] at h
          have ha_lt : (ak.1 : ℤ) < n := by exact_mod_cast ak.2
          have hb_le : (bk.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ bk.2
          omega
      | inr b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexPointCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl

private lemma triangularHexPointCoord_mem (n : ℕ) (p : triangularHexPointIndex n) :
    triangularHexPointCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      rcases p with ⟨k, v⟩
      rw [mem_triangularHexCoords]
      simp [triangularHexPointCoord]
      omega
  | inr p =>
      rcases p with ⟨k, v⟩
      rw [mem_triangularHexCoords]
      simp [triangularHexPointCoord]
      have hk : (k.1 : ℤ) < n := by exact_mod_cast k.2
      omega

private lemma triangularHexPointCoord_surjective (n : ℕ) :
    ∀ q ∈ triangularHexCoords n, ∃ p : triangularHexPointIndex n,
      triangularHexPointCoord n p = q := by
  rintro ⟨i, j⟩ hq
  rw [mem_triangularHexCoords] at hq
  rcases hq with ⟨hi_low, hi_high, hj_low, hj_high, hij_low, hij_high⟩
  by_cases hj_nonpos : j ≤ 0
  · let kNat : ℕ := Int.toNat (j + (n : ℤ))
    have hk_cast : (kNat : ℤ) = j + (n : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hk_lt : kNat < n + 1 := by
      omega
    let vNat : ℕ := Int.toNat (i + (kNat : ℤ))
    have hv_cast : (vNat : ℤ) = i + (kNat : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hv_lt : vNat < n + kNat + 1 := by
      omega
    refine ⟨Sum.inl ⟨⟨kNat, hk_lt⟩, ⟨vNat, hv_lt⟩⟩, ?_⟩
    simp [triangularHexPointCoord, kNat, vNat, hk_cast]
    omega
  · have hj_pos : 0 < j := by omega
    let kNat : ℕ := Int.toNat ((n : ℤ) - j)
    have hk_cast : (kNat : ℤ) = (n : ℤ) - j := by
      exact Int.toNat_of_nonneg (by omega)
    have hk_lt : kNat < n := by
      omega
    let vNat : ℕ := Int.toNat (i + (n : ℤ))
    have hv_cast : (vNat : ℤ) = i + (n : ℤ) := by
      exact Int.toNat_of_nonneg (by omega)
    have hv_lt : vNat < n + kNat + 1 := by
      omega
    refine ⟨Sum.inr ⟨⟨kNat, hk_lt⟩, ⟨vNat, hv_lt⟩⟩, ?_⟩
    simp [triangularHexPointCoord, kNat, vNat, hk_cast, hv_cast]

private lemma triangularHexPointCoord_image_univ (n : ℕ) :
    Finset.univ.image (triangularHexPointCoord n) = triangularHexCoords n := by
  classical
  ext q
  constructor
  · intro hq
    rw [Finset.mem_image] at hq
    rcases hq with ⟨p, _hp, rfl⟩
    exact triangularHexPointCoord_mem n p
  · intro hq
    rcases triangularHexPointCoord_surjective n q hq with ⟨p, rfl⟩
    exact Finset.mem_image.mpr ⟨p, Finset.mem_univ p, rfl⟩

private lemma triangularHexCoords_card (n : ℕ) :
    (triangularHexCoords n).card = 3 * n ^ 2 + 3 * n + 1 := by
  classical
  rw [← triangularHexPointCoord_image_univ n]
  rw [Finset.card_image_of_injective]
  · simp [triangularHexPointIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexPointIndex_card_aux]
  · exact triangularHexPointCoord_injective n

private lemma triangularHexPatch_card (n : ℕ) :
    (triangularHexPatch n).card = 3 * n ^ 2 + 3 * n + 1 := by
  rw [triangularHexPatch_card_eq_coords_card, triangularHexCoords_card]

private noncomputable def triangularHexPatchRows (n : ℕ) : Finset (ℝ^2) :=
  Finset.univ.image fun p : triangularHexPointIndex n =>
    triangularPoint (triangularHexPointCoord n p).1 (triangularHexPointCoord n p).2

private lemma triangularHexPatchRows_card (n : ℕ) :
    (triangularHexPatchRows n).card = 3 * n ^ 2 + 3 * n + 1 := by
  classical
  unfold triangularHexPatchRows
  rw [Finset.card_image_of_injective]
  · simp [triangularHexPointIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexPointIndex_card_aux]
  · intro a b h
    apply triangularHexPointCoord_injective n
    exact triangularPoint_injective h

private lemma triangularHexPatchRows_oneSeparated (n : ℕ) :
    Metric.IsSeparated' 1 ((triangularHexPatchRows n : Finset (ℝ^2)) : Set (ℝ^2)) := by
  classical
  rw [Metric.IsSeparated']
  intro x hx y hy hxy
  rw [Finset.mem_coe, triangularHexPatchRows, Finset.mem_image] at hx hy
  rcases hx with ⟨p, _hp, rfl⟩
  rcases hy with ⟨q, _hq, rfl⟩
  refine triangularPoint_edist_ge_one_of_ne ?_
  intro hpq
  apply hxy
  have hcoord : triangularHexPointCoord n p = triangularHexPointCoord n q := by
    simpa using hpq
  rw [hcoord]

private abbrev triangularHexEastEdgeIndex (n : ℕ) :=
  (Sigma fun k : Fin (n + 1) => Fin (n + k.1)) ⊕
    (Sigma fun k : Fin n => Fin (n + k.1))

private def triangularHexEastSourceCoord (n : ℕ) : triangularHexEastEdgeIndex n → ℤ × ℤ
  | Sum.inl p => ((-(p.1.1 : ℤ) + (p.2.1 : ℤ)), (-(n : ℤ) + (p.1.1 : ℤ)))
  | Sum.inr p => ((-(n : ℤ) + (p.2.1 : ℤ)), ((n : ℤ) - (p.1.1 : ℤ)))

private def triangularHexEastSourcePointIndex (n : ℕ) :
    triangularHexEastEdgeIndex n → triangularHexPointIndex n
  | Sum.inl p =>
      Sum.inl ⟨p.1, ⟨p.2.1, by omega⟩⟩
  | Sum.inr p =>
      Sum.inr ⟨p.1, ⟨p.2.1, by omega⟩⟩

private def triangularHexEastTargetPointIndex (n : ℕ) :
    triangularHexEastEdgeIndex n → triangularHexPointIndex n
  | Sum.inl p =>
      Sum.inl ⟨p.1, ⟨p.2.1 + 1, by omega⟩⟩
  | Sum.inr p =>
      Sum.inr ⟨p.1, ⟨p.2.1 + 1, by omega⟩⟩

private lemma triangularHexEastSourcePointIndex_coord (n : ℕ)
    (p : triangularHexEastEdgeIndex n) :
    triangularHexPointCoord n (triangularHexEastSourcePointIndex n p) =
      triangularHexEastSourceCoord n p := by
  cases p <;> rfl

private lemma triangularHexEastTargetPointIndex_coord (n : ℕ)
    (p : triangularHexEastEdgeIndex n) :
    triangularHexPointCoord n (triangularHexEastTargetPointIndex n p) =
      ((triangularHexEastSourceCoord n p).1 + 1, (triangularHexEastSourceCoord n p).2) := by
  cases p <;> simp [triangularHexEastTargetPointIndex, triangularHexEastSourceCoord,
    triangularHexPointCoord] <;> ring

private lemma triangularHexEastEdgeIndex_card_aux (n : ℕ) :
    (∑ k : Fin (n + 1), (n + k.1)) + (∑ k : Fin n, (n + k.1)) =
      3 * n ^ 2 + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1 + 1) => n + 1 + k.1)]
      rw [Fin.sum_univ_castSucc (fun k : Fin (n + 1) => n + 1 + k.1)]
      simp only [Fin.val_castSucc, Fin.val_last]
      have hfirst : (∑ i : Fin (n + 1), (n + 1 + i.1)) =
          (∑ i : Fin (n + 1), (n + i.1)) + (n + 1) := by
        simp_rw [show ∀ i : Fin (n + 1), n + 1 + i.1 = (n + i.1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin (n + 1) => (n + i.1) + 1) =
          (Finset.univ.sum fun i : Fin (n + 1) => n + i.1) + (n + 1)
        rw [Finset.sum_add_distrib]
        simp
      have hsecond : (∑ i : Fin n, (n + 1 + i.1)) =
          (∑ i : Fin n, (n + i.1)) + n := by
        simp_rw [show ∀ i : Fin n, n + 1 + i.1 = (n + i.1) + 1 by
          intro i
          omega]
        change (Finset.univ.sum fun i : Fin n => (n + i.1) + 1) =
          (Finset.univ.sum fun i : Fin n => n + i.1) + n
        rw [Finset.sum_add_distrib]
        simp
      rw [hfirst, hsecond]
      nlinarith [ih]

private lemma triangularHexEastSourceCoord_injective (n : ℕ) :
    Function.Injective (triangularHexEastSourceCoord n) := by
  intro a b h
  cases a with
  | inl a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl
      | inr b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hb_lt : (bk.1 : ℤ) < n := by exact_mod_cast bk.2
          have ha_le : (ak.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ ak.2
          omega
  | inr a =>
      rcases a with ⟨ak, av⟩
      cases b with
      | inl b =>
          rcases b with ⟨bk, _bv⟩
          simp [triangularHexEastSourceCoord] at h
          have ha_lt : (ak.1 : ℤ) < n := by exact_mod_cast ak.2
          have hb_le : (bk.1 : ℤ) ≤ n := by exact_mod_cast Nat.le_of_lt_succ bk.2
          omega
      | inr b =>
          rcases b with ⟨bk, bv⟩
          simp [triangularHexEastSourceCoord] at h
          have hk : ak = bk := by
            ext
            omega
          subst hk
          have hv : av = bv := by
            ext
            omega
          subst hv
          rfl

private noncomputable def triangularHexPatchRowsEastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  Finset.univ.image fun p : triangularHexEastEdgeIndex n =>
    s(triangularPoint (triangularHexEastSourceCoord n p).1 (triangularHexEastSourceCoord n p).2,
      triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
        (triangularHexEastSourceCoord n p).2)

private lemma triangularHexPatchRowsEastUnitPairs_card (n : ℕ) :
    (triangularHexPatchRowsEastUnitPairs n).card = 3 * n ^ 2 + n := by
  classical
  unfold triangularHexPatchRowsEastUnitPairs
  rw [Finset.card_image_of_injective]
  · simp [triangularHexEastEdgeIndex, Fintype.card_sum, Fintype.card_sigma,
      triangularHexEastEdgeIndex_card_aux]
  · intro a b h
    have hrel :
        Sym2.Rel (ℝ^2)
          (triangularPoint (triangularHexEastSourceCoord n a).1
              (triangularHexEastSourceCoord n a).2,
            triangularPoint ((triangularHexEastSourceCoord n a).1 + 1)
              (triangularHexEastSourceCoord n a).2)
          (triangularPoint (triangularHexEastSourceCoord n b).1
              (triangularHexEastSourceCoord n b).2,
            triangularPoint ((triangularHexEastSourceCoord n b).1 + 1)
              (triangularHexEastSourceCoord n b).2) :=
      Sym2.exact h
    rw [Sym2.rel_iff] at hrel
    rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
    · apply triangularHexEastSourceCoord_injective n
      exact triangularPoint_injective h₁
    · have hs :
          triangularHexEastSourceCoord n a =
            ((triangularHexEastSourceCoord n b).1 + 1,
              (triangularHexEastSourceCoord n b).2) :=
        triangularPoint_injective h₁
      have ht :
          ((triangularHexEastSourceCoord n a).1 + 1,
              (triangularHexEastSourceCoord n a).2) =
            triangularHexEastSourceCoord n b :=
        triangularPoint_injective h₂
      have hs₁ :
          (triangularHexEastSourceCoord n a).1 =
            (triangularHexEastSourceCoord n b).1 + 1 := congrArg Prod.fst hs
      have ht₁ :
          (triangularHexEastSourceCoord n a).1 + 1 =
            (triangularHexEastSourceCoord n b).1 := congrArg Prod.fst ht
      omega

private lemma triangularHexPatchRowsEastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexPatchRowsEastUnitPairs n ⊆
      (triangularHexPatchRows n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexPatchRowsEastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, _hp, rfl⟩
  have h₁ :
      triangularPoint (triangularHexEastSourceCoord n p).1 (triangularHexEastSourceCoord n p).2 ∈
        triangularHexPatchRows n := by
    unfold triangularHexPatchRows
    refine Finset.mem_image.mpr ⟨triangularHexEastSourcePointIndex n p, Finset.mem_univ _, ?_⟩
    rw [triangularHexEastSourcePointIndex_coord]
  have h₂ :
      triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
          (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatchRows n := by
    unfold triangularHexPatchRows
    refine Finset.mem_image.mpr ⟨triangularHexEastTargetPointIndex n p, Finset.mem_univ _, ?_⟩
    rw [triangularHexEastTargetPointIndex_coord]
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_east]

private lemma triangularHexPatch_east_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1 + 1, p.2) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint (p.1 + 1) p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1 + 1, p.2), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_east]

private lemma triangularHexEastUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)
        (triangularPoint q.1 q.2, triangularPoint (q.1 + 1) q.2) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1 + 1, q.2) := triangularPoint_injective h₁
    have hq : (p.1 + 1, p.2) = q := triangularPoint_injective h₂
    have hp₁ : p.1 = q.1 + 1 := congrArg Prod.fst hp
    have hq₁ : p.1 + 1 = q.1 := congrArg Prod.fst hq
    omega

private lemma triangularHexPatch_north_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1, p.2 + 1) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1)) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint p.1 (p.2 + 1) ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1, p.2 + 1), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_north]

private lemma triangularHexNorthUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))
        (triangularPoint q.1 q.2, triangularPoint q.1 (q.2 + 1)) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1, q.2 + 1) := triangularPoint_injective h₁
    have hq : (p.1, p.2 + 1) = q := triangularPoint_injective h₂
    have hp₂ : p.2 = q.2 + 1 := congrArg Prod.snd hp
    have hq₂ : p.2 + 1 = q.2 := congrArg Prod.snd hq
    omega

private lemma triangularHexPatch_southeast_pair_mem_unitDist {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n)
    (hp' : (p.1 + 1, p.2 - 1) ∈ triangularHexCoords n) :
    s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1)) ∈
      (triangularHexPatch n).sym2.filter
        (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  have h₁ : triangularPoint p.1 p.2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨p, hp, rfl⟩
  have h₂ : triangularPoint (p.1 + 1) (p.2 - 1) ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr ⟨(p.1 + 1, p.2 - 1), hp', rfl⟩
  simp [h₁, h₂, dist_out_eq_of_eq_sym2_mk rfl, triangularPoint_dist_southeast]

private lemma triangularHexSoutheastUnitPair_injective :
    Function.Injective
      (fun p : ℤ × ℤ =>
        s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))) := by
  intro p q hpq
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))
        (triangularPoint q.1 q.2, triangularPoint (q.1 + 1) (q.2 - 1)) :=
    Sym2.exact hpq
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨h₁, _h₂⟩ | ⟨h₁, h₂⟩
  · exact triangularPoint_injective h₁
  · have hp : p = (q.1 + 1, q.2 - 1) := triangularPoint_injective h₁
    have hq : (p.1 + 1, p.2 - 1) = q := triangularPoint_injective h₂
    have hp₁ : p.1 = q.1 + 1 := congrArg Prod.fst hp
    have hq₁ : p.1 + 1 = q.1 := congrArg Prod.fst hq
    omega

private def triangularHexEastSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1 + 1, p.2) ∈ triangularHexCoords n

private def triangularHexNorthSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1, p.2 + 1) ∈ triangularHexCoords n

private def triangularHexSoutheastSources (n : ℕ) : Finset (ℤ × ℤ) :=
  (triangularHexCoords n).filter fun p => (p.1 + 1, p.2 - 1) ∈ triangularHexCoords n

private noncomputable def triangularHexEastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexEastSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) p.2)

private noncomputable def triangularHexNorthUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexNorthSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint p.1 (p.2 + 1))

private noncomputable def triangularHexSoutheastUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  (triangularHexSoutheastSources n).image
    fun p : ℤ × ℤ => s(triangularPoint p.1 p.2, triangularPoint (p.1 + 1) (p.2 - 1))

private lemma triangularHexEastUnitPairs_card (n : ℕ) :
    (triangularHexEastUnitPairs n).card = (triangularHexEastSources n).card := by
  classical
  unfold triangularHexEastUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexEastUnitPair_injective]

private lemma triangularHexNorthUnitPairs_card (n : ℕ) :
    (triangularHexNorthUnitPairs n).card = (triangularHexNorthSources n).card := by
  classical
  unfold triangularHexNorthUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexNorthUnitPair_injective]

private lemma triangularHexSoutheastUnitPairs_card (n : ℕ) :
    (triangularHexSoutheastUnitPairs n).card = (triangularHexSoutheastSources n).card := by
  classical
  unfold triangularHexSoutheastUnitPairs
  rw [Finset.card_image_of_injective _ triangularHexSoutheastUnitPair_injective]

private lemma triangularHexEastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexEastUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexEastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexEastSources, Finset.mem_filter] at hp
  exact triangularHexPatch_east_pair_mem_unitDist hp.1 hp.2

private lemma triangularHexNorthUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexNorthUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexNorthUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexNorthSources, Finset.mem_filter] at hp
  exact triangularHexPatch_north_pair_mem_unitDist hp.1 hp.2

private lemma triangularHexSoutheastUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexSoutheastUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexSoutheastUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, hp, rfl⟩
  rw [triangularHexSoutheastSources, Finset.mem_filter] at hp
  exact triangularHexPatch_southeast_pair_mem_unitDist hp.1 hp.2

private abbrev triangularHexThreeEdgeIndex (n : ℕ) :=
  triangularHexEastEdgeIndex n ⊕
    (triangularHexEastEdgeIndex n ⊕ triangularHexEastEdgeIndex n)

private def triangularHexThreeEdgeSourceCoord (n : ℕ) :
    triangularHexThreeEdgeIndex n → ℤ × ℤ
  | Sum.inl p => triangularHexEastSourceCoord n p
  | Sum.inr (Sum.inl p) =>
      (-(triangularHexEastSourceCoord n p).2,
        (triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2)
  | Sum.inr (Sum.inr p) =>
      ((triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2,
        -(triangularHexEastSourceCoord n p).1)

private def triangularHexThreeEdgeTargetCoord (n : ℕ) :
    triangularHexThreeEdgeIndex n → ℤ × ℤ
  | Sum.inl p =>
      ((triangularHexEastSourceCoord n p).1 + 1, (triangularHexEastSourceCoord n p).2)
  | Sum.inr (Sum.inl p) =>
      (-(triangularHexEastSourceCoord n p).2,
        (triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2 + 1)
  | Sum.inr (Sum.inr p) =>
      ((triangularHexEastSourceCoord n p).1 + (triangularHexEastSourceCoord n p).2 + 1,
        -(triangularHexEastSourceCoord n p).1 - 1)

private lemma triangularHexEastSourceCoord_mem (n : ℕ) (p : triangularHexEastEdgeIndex n) :
    triangularHexEastSourceCoord n p ∈ triangularHexCoords n := by
  rw [← triangularHexEastSourcePointIndex_coord n p]
  exact triangularHexPointCoord_mem n (triangularHexEastSourcePointIndex n p)

private lemma triangularHexEastTargetCoord_mem (n : ℕ) (p : triangularHexEastEdgeIndex n) :
    ((triangularHexEastSourceCoord n p).1 + 1,
        (triangularHexEastSourceCoord n p).2) ∈ triangularHexCoords n := by
  rw [← triangularHexEastTargetPointIndex_coord n p]
  exact triangularHexPointCoord_mem n (triangularHexEastTargetPointIndex n p)

private lemma triangularHexCoord_rotateNorth_mem {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n) :
    (-p.2, p.1 + p.2) ∈ triangularHexCoords n := by
  rw [mem_triangularHexCoords] at hp ⊢
  omega

private lemma triangularHexCoord_rotateSoutheast_mem {n : ℕ} {p : ℤ × ℤ}
    (hp : p ∈ triangularHexCoords n) :
    (p.1 + p.2, -p.1) ∈ triangularHexCoords n := by
  rw [mem_triangularHexCoords] at hp ⊢
  omega

private lemma triangularHexThreeEdgeSourceCoord_mem (n : ℕ)
    (p : triangularHexThreeEdgeIndex n) :
    triangularHexThreeEdgeSourceCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      exact triangularHexEastSourceCoord_mem n p
  | inr p =>
      cases p with
      | inl p =>
          exact triangularHexCoord_rotateNorth_mem (triangularHexEastSourceCoord_mem n p)
      | inr p =>
          exact triangularHexCoord_rotateSoutheast_mem (triangularHexEastSourceCoord_mem n p)

private lemma triangularHexThreeEdgeTargetCoord_mem (n : ℕ)
    (p : triangularHexThreeEdgeIndex n) :
    triangularHexThreeEdgeTargetCoord n p ∈ triangularHexCoords n := by
  cases p with
  | inl p =>
      exact triangularHexEastTargetCoord_mem n p
  | inr p =>
      cases p with
      | inl p =>
          simpa [triangularHexThreeEdgeTargetCoord, add_assoc, add_left_comm, add_comm]
            using triangularHexCoord_rotateNorth_mem (triangularHexEastTargetCoord_mem n p)
      | inr p =>
          simpa [triangularHexThreeEdgeTargetCoord, sub_eq_add_neg, add_assoc, add_left_comm,
            add_comm]
            using triangularHexCoord_rotateSoutheast_mem (triangularHexEastTargetCoord_mem n p)

private lemma triangularHexThreeEdgeIndex_eq_of_source_target_eq (n : ℕ)
    {a b : triangularHexThreeEdgeIndex n}
    (hs : triangularHexThreeEdgeSourceCoord n a = triangularHexThreeEdgeSourceCoord n b)
    (ht : triangularHexThreeEdgeTargetCoord n a = triangularHexThreeEdgeTargetCoord n b) :
    a = b := by
  have hs₁ := congrArg Prod.fst hs
  have hs₂ := congrArg Prod.snd hs
  have ht₁ := congrArg Prod.fst ht
  have ht₂ := congrArg Prod.snd ht
  rcases a with a | a
  · rcases b with b | b
    · exact congrArg Sum.inl (triangularHexEastSourceCoord_injective n hs)
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
  · rcases a with a | a
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · rcases b with b | b
        · have hc : triangularHexEastSourceCoord n a = triangularHexEastSourceCoord n b := by
            simp [triangularHexThreeEdgeSourceCoord] at hs₁ hs₂
            ext <;> omega
          exact congrArg (fun e => Sum.inr (Sum.inl e))
            (triangularHexEastSourceCoord_injective n hc)
        · exfalso
          simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
          omega
    · rcases b with b | b
      · exfalso
        simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
        omega
      · rcases b with b | b
        · exfalso
          simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
          omega
        · have hc : triangularHexEastSourceCoord n a = triangularHexEastSourceCoord n b := by
            simp [triangularHexThreeEdgeSourceCoord] at hs₁ hs₂
            ext <;> omega
          exact congrArg (fun e => Sum.inr (Sum.inr e))
            (triangularHexEastSourceCoord_injective n hc)

private lemma triangularHexThreeEdgeIndex_not_reverse (n : ℕ)
    {a b : triangularHexThreeEdgeIndex n}
    (hs : triangularHexThreeEdgeSourceCoord n a = triangularHexThreeEdgeTargetCoord n b)
    (ht : triangularHexThreeEdgeTargetCoord n a = triangularHexThreeEdgeSourceCoord n b) :
    False := by
  have hs₁ := congrArg Prod.fst hs
  have hs₂ := congrArg Prod.snd hs
  have ht₁ := congrArg Prod.fst ht
  have ht₂ := congrArg Prod.snd ht
  rcases a with a | a <;> rcases b with b | b
  · simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂
    omega
  · rcases b with b | b <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega
  · rcases a with a | a <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega
  · rcases a with a | a <;> rcases b with b | b <;>
      simp [triangularHexThreeEdgeSourceCoord, triangularHexThreeEdgeTargetCoord] at hs₁ hs₂ ht₁ ht₂ <;>
      omega

private noncomputable def triangularHexThreeUnitPairs (n : ℕ) : Finset (Sym2 (ℝ^2)) :=
  Finset.univ.image fun p : triangularHexThreeEdgeIndex n =>
    s(triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
        (triangularHexThreeEdgeSourceCoord n p).2,
      triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
        (triangularHexThreeEdgeTargetCoord n p).2)

private lemma triangularHexThreeUnitPair_injective (n : ℕ) :
    Function.Injective
      (fun p : triangularHexThreeEdgeIndex n =>
        s(triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
            (triangularHexThreeEdgeSourceCoord n p).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
            (triangularHexThreeEdgeTargetCoord n p).2)) := by
  intro a b hab
  have hrel :
      Sym2.Rel (ℝ^2)
        (triangularPoint (triangularHexThreeEdgeSourceCoord n a).1
            (triangularHexThreeEdgeSourceCoord n a).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n a).1
            (triangularHexThreeEdgeTargetCoord n a).2)
        (triangularPoint (triangularHexThreeEdgeSourceCoord n b).1
            (triangularHexThreeEdgeSourceCoord n b).2,
          triangularPoint (triangularHexThreeEdgeTargetCoord n b).1
            (triangularHexThreeEdgeTargetCoord n b).2) :=
    Sym2.exact hab
  rw [Sym2.rel_iff] at hrel
  rcases hrel with ⟨hs, ht⟩ | ⟨hs, ht⟩
  · exact triangularHexThreeEdgeIndex_eq_of_source_target_eq n
      (triangularPoint_injective hs) (triangularPoint_injective ht)
  · exact False.elim <| triangularHexThreeEdgeIndex_not_reverse n
      (triangularPoint_injective hs) (triangularPoint_injective ht)

private lemma triangularHexThreeUnitPairs_card (n : ℕ) :
    (triangularHexThreeUnitPairs n).card = 9 * n ^ 2 + 3 * n := by
  classical
  unfold triangularHexThreeUnitPairs
  rw [Finset.card_image_of_injective]
  · simp [triangularHexThreeEdgeIndex, triangularHexEastEdgeIndex, Fintype.card_sum,
      Fintype.card_sigma, triangularHexEastEdgeIndex_card_aux]
    ring
  · exact triangularHexThreeUnitPair_injective n

private lemma triangularHexThreeUnitPairs_subset_unitDist (n : ℕ) :
    triangularHexThreeUnitPairs n ⊆
      (triangularHexPatch n).sym2.filter (fun q => dist q.out.1 q.out.2 = 1) := by
  classical
  intro q hq
  rw [triangularHexThreeUnitPairs, Finset.mem_image] at hq
  rcases hq with ⟨p, _hp, rfl⟩
  have h₁ :
      triangularPoint (triangularHexThreeEdgeSourceCoord n p).1
          (triangularHexThreeEdgeSourceCoord n p).2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr
      ⟨triangularHexThreeEdgeSourceCoord n p, triangularHexThreeEdgeSourceCoord_mem n p, rfl⟩
  have h₂ :
      triangularPoint (triangularHexThreeEdgeTargetCoord n p).1
          (triangularHexThreeEdgeTargetCoord n p).2 ∈ triangularHexPatch n := by
    unfold triangularHexPatch
    exact Finset.mem_image.mpr
      ⟨triangularHexThreeEdgeTargetCoord n p, triangularHexThreeEdgeTargetCoord_mem n p, rfl⟩
  cases p with
  | inl p =>
      have h₁' :
          triangularPoint (triangularHexEastSourceCoord n p).1
              (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatch n := by
        simpa [triangularHexThreeEdgeSourceCoord] using h₁
      have h₂' :
          triangularPoint ((triangularHexEastSourceCoord n p).1 + 1)
              (triangularHexEastSourceCoord n p).2 ∈ triangularHexPatch n := by
        simpa [triangularHexThreeEdgeTargetCoord] using h₂
      simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
        triangularHexThreeEdgeTargetCoord, triangularPoint_dist_east]
  | inr p =>
      cases p with
      | inl p =>
          have h₁' :
              triangularPoint (-(triangularHexEastSourceCoord n p).2)
                  ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeSourceCoord] using h₁
          have h₂' :
              triangularPoint (-(triangularHexEastSourceCoord n p).2)
                  ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2 + 1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeTargetCoord] using h₂
          simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
            triangularHexThreeEdgeTargetCoord, triangularPoint_dist_north]
      | inr p =>
          have h₁' :
              triangularPoint ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2)
                  (-(triangularHexEastSourceCoord n p).1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeSourceCoord] using h₁
          have h₂' :
              triangularPoint ((triangularHexEastSourceCoord n p).1 +
                    (triangularHexEastSourceCoord n p).2 + 1)
                  (-(triangularHexEastSourceCoord n p).1 - 1) ∈ triangularHexPatch n := by
            simpa [triangularHexThreeEdgeTargetCoord] using h₂
          simp [h₁', h₂', dist_out_eq_of_eq_sym2_mk rfl, triangularHexThreeEdgeSourceCoord,
            triangularHexThreeEdgeTargetCoord, triangularPoint_dist_southeast]

/--
The axial hexagonal triangular-lattice patch contains at least `9n^2 + 3n`
unordered unit-distance pairs.
-/
@[category API, AMS 52]
theorem triangularHexPatch_unitPairs_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ unitDistNum (triangularHexPatch n) := by
  classical
  have hcard_le := Finset.card_le_card (triangularHexThreeUnitPairs_subset_unitDist n)
  rw [triangularHexThreeUnitPairs_card] at hcard_le
  exact hcard_le

private lemma unitDistNum_le_sym2_card {d : ℕ} (s : Finset (ℝ^d)) :
    unitDistNum s ≤ s.sym2.card := by
  unfold unitDistNum
  exact Finset.card_filter_le _ _

/--
A local construction certificate for the triangular/hexagonal patch needed for the lower
bound in Erdős Problem 1084.
-/
def TriangularLowerCertificate (n : ℕ) : Prop :=
  ∃ points : Finset (ℝ^2),
    points.card = 3 * n ^ 2 + 3 * n + 1 ∧
    Metric.IsSeparated' 1 (points : Set (ℝ^2)) ∧
    9 * n ^ 2 + 3 * n ≤ unitDistNum points

private lemma f_lower_of_witness {d N m : ℕ} (s : Finset (ℝ^d))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^d)))
    (hunit : m ≤ unitDistNum s) :
    m ≤ f d N := by
  classical
  unfold f
  refine le_ciSup_of_le ?outer s ?_
  · refine ⟨Nat.choose (N + 1) 2, ?_⟩
    rintro _ ⟨t, rfl⟩
    refine ciSup_le' ?_
    intro ht
    refine ciSup_le' ?_
    intro _htsep
    exact (unitDistNum_le_sym2_card t).trans_eq (by rw [Finset.card_sym2, ht])
  · refine le_ciSup_of_le ?cardBdd hcard ?_
    · refine ⟨unitDistNum s, ?_⟩
      rintro _ ⟨hc, rfl⟩
      exact ciSup_le' fun _ => le_rfl
    · exact le_ciSup_of_le ⟨unitDistNum s, by rintro _ ⟨hs, rfl⟩; exact le_rfl⟩ hsep hunit

/--
The lower-bound packaging step for Erdős Problem 1084: any verified triangular patch with
`3n^2 + 3n + 1` points and at least `9n^2 + 3n` unit-distance pairs gives the desired
lower bound for `f 2`.
-/
@[category API, AMS 52]
theorem erdos_1084.variants.triangular_optimal_d2_lower_of_certificate
    (n : ℕ) (cert : TriangularLowerCertificate n) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
  rcases cert with ⟨points, hcard, hsep, hunit⟩
  exact f_lower_of_witness points hcard hsep hunit

/--
The axial hexagonal triangular-lattice patch with `3n^2 + 3n + 1` points is
`1`-separated and contains at least `9n^2 + 3n` unordered unit-distance pairs.
-/
theorem erdos_1084.variants.triangular_lower_certificate (n : ℕ) :
    TriangularLowerCertificate n := by
  exact ⟨triangularHexPatch n, triangularHexPatch_card n, triangularHexPatch_oneSeparated n,
    triangularHexPatch_unitPairs_lower n⟩

end Erdos1084

open Erdos1084

/--
The triangular-lattice lower construction for Erdős Problem 1084: for
`3n^2 + 3n + 1` planar `1`-separated points, one can realize at least
`9n^2 + 3n` unit-distance pairs.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
  exact Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower_of_certificate n
    (Erdos1084.erdos_1084.variants.triangular_lower_certificate n)

/--
Conditional triangular-lattice upper bound obtained from Harborth's source theorem in the
`2`-separated contact convention.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source
    (hHarborth : Erdos1084.HarborthTwoSeparatedContactUpperGe4Source)
    {n : ℕ} (hn : 1 ≤ n) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) ≤ 9 * n ^ 2 + 3 * n := by
  have hUnit : Erdos1084.HarborthUnitDistNumUpperGe4Source :=
    Erdos1084.harborth_unitDistNum_upper_ge4_of_twoSeparated_contact_source hHarborth
  have hN : 4 ≤ 3 * n ^ 2 + 3 * n + 1 := by
    have hn_sq : 1 ≤ n ^ 2 := by
      nlinarith [Nat.mul_le_mul hn hn]
    nlinarith
  unfold Erdos1084.f
  refine ciSup_le' ?_
  intro s
  refine ciSup_le' ?_
  intro hcard
  refine ciSup_le' ?_
  intro hsep
  have hbound :=
    hUnit (3 * n ^ 2 + 3 * n + 1) hN s hcard hsep
  rwa [Erdos1084.triangular_harborth_floor n] at hbound

/--
Promoted local wrapper for the Harborth/Bezdek--Khan source certificate: assuming the
external source theorem in the explicit `Erdos1084.HarborthUnitDistNumUpperGe4Source`
contract, every finite `1`-separated set of `N ≥ 4` points in the Euclidean plane has at
most `⌊3N - sqrt (12N - 3)⌋` unit-distance pairs.
-/
@[category API, AMS 52]
theorem HarborthBezdekKhanSourceCertificateToUnitDistNumWrapper
    (hHarborth : Erdos1084.HarborthUnitDistNumUpperGe4Source)
    (N : ℕ) (hN : 4 ≤ N) (s : Finset (ℝ^2))
    (hcard : s.card = N)
    (hsep : Metric.IsSeparated' 1 (s : Set (ℝ^2))) :
    unitDistNum s ≤
      Nat.floor (3 * (N : ℝ) - Real.sqrt (12 * (N : ℝ) - 3)) := by
  exact Erdos1084.harborth_unitDistNum_upper_ge4_of_source hHarborth N hN s hcard hsep

/--
Final conditional triangular-lattice optimality wrapper for Erdős Problem 1084 under the
Harborth `2`-separated contact-number source theorem.
-/
@[category API, AMS 52]
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source
    (hHarborth : Erdos1084.HarborthTwoSeparatedContactUpperGe4Source)
    (n : Nat) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  by_cases hn0 : n = 0
  · subst n
    simpa using Erdos1084.f_two_one_eq_zero
  · have hn : 1 ≤ n := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hn0)
    exact le_antisymm
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source
        hHarborth hn)
      (Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower n)
