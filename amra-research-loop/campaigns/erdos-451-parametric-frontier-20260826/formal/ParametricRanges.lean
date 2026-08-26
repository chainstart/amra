import ParametricInterface

/-! Substantive variable-theta reconstructions of the source-paper ranges. -/

noncomputable section

open scoped BigOperators Nat
open Finset Filter

namespace ParametricML

/-- Medium-large Konyagin scale at an arbitrary exponent. -/
def lamML (ϑ : ℝ) (k : ℕ) (n : ℤ) : ℝ :=
  Real.sqrt ((k : ℝ) ^ (2 + ϑ) / (2 * (n : ℝ))) * Real.log k

/-- `n`-free upper envelope for the medium-large scale. -/
def lamUB (ϑ : ℝ) (k : ℕ) : ℝ :=
  (1 / Real.sqrt 2) * (k : ℝ) ^ (ϑ / 2) * (Real.log k) ^ 2

/-- `n`-free Konyagin bound in the medium-large range. -/
def gML (ϑ : ℝ) (k : ℕ) : ℝ :=
  c₆ * (k : ℝ) ^ ϑ *
    (((k : ℝ) ^ (ϑ - 1) * (Real.log k) ^ 2) ^ ((1 : ℝ) / 3) +
      (Real.log k) ^ (-(2 : ℝ)) +
      (3 * lamUB ϑ k / (k : ℝ)) ^ ((1 : ℝ) / 4)) +
    4 * lamUB ϑ k

lemma lamML_ge_one (ϑ : ℝ) (k : ℕ) (n : ℤ) (hk : 3 ≤ k) (hnpos : 0 < n)
    (hn : (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ)) :
    1 ≤ lamML ϑ k n := by
  refine one_le_mul_of_one_le_of_one_le (Real.le_sqrt_of_sq_le ?_) ?_
  · rw [le_div_iff₀] <;> first | positivity | linarith
  · exact Real.le_log_iff_exp_le (by positivity) |>.2
      (le_trans Real.exp_one_lt_d9.le (by norm_num; linarith [show (k : ℝ) ≥ 3 by norm_cast]))

lemma lamML_le_lamUB (ϑ : ℝ) (k : ℕ) (n : ℤ) (hk : 2 ≤ k)
    (hn : (k : ℝ) ^ 2 / (Real.log k) ^ 2 < (n : ℝ)) :
    lamML ϑ k n ≤ lamUB ϑ k := by
  have hsqrt : Real.sqrt ((k : ℝ) ^ (2 + ϑ) / (2 * (n : ℝ))) ≤
      (1 / Real.sqrt 2) * (k : ℝ) ^ (ϑ / 2) * Real.log k := by
    have hsq : (k : ℝ) ^ (2 + ϑ) / (2 * (n : ℝ)) ≤
        (k : ℝ) ^ ϑ * (Real.log k) ^ 2 / 2 := by
      rw [div_le_iff₀] <;>
        norm_num [Real.rpow_add (by positivity : 0 < (k : ℝ))] at *
      · rw [div_lt_iff₀] at hn <;>
          nlinarith [show 0 < (k : ℝ) ^ ϑ by positivity,
            show 0 < (Real.log k) ^ 2 by
              exact sq_pos_of_pos <| Real.log_pos <| Nat.one_lt_cast.mpr hk]
      · exact_mod_cast hn.trans_le' (div_nonneg (sq_nonneg _) (sq_nonneg _))
    convert Real.sqrt_le_sqrt hsq using 1
    norm_num [Real.sqrt_div_self]
    ring_nf
    rw [Real.sqrt_mul (by positivity), Real.sqrt_sq (by positivity),
      Real.sqrt_eq_rpow, Real.sqrt_eq_rpow, ← Real.rpow_mul (by positivity)]
    ring
  unfold lamML lamUB
  convert mul_le_mul_of_nonneg_right hsqrt
    (Real.log_nonneg <| Nat.one_le_cast.mpr <| by linarith) using 1
  ring

lemma lamML_sq (ϑ : ℝ) (k : ℕ) (n : ℤ) (hn0 : 0 < n) :
    (lamML ϑ k n) ^ 2 =
      (k : ℝ) ^ (2 + ϑ) / (2 * (n : ℝ)) * (Real.log k) ^ 2 := by
  unfold lamML
  rw [mul_pow, Real.sq_sqrt (by positivity)]

/-- Konyagin's theorem at `r=2`, now uniformly for every `0<ϑ<1`. -/
lemma ml_card_bound (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (k : ℝ) ^ 2 / (Real.log k) ^ 2 < (n : ℝ) →
      (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ) →
      ((badSetAt ϑ k n).card : ℝ) < gML ϑ k := by
  obtain ⟨k₀, hk₀⟩ : ∃ k₀ : ℕ, ∀ k ≥ k₀,
      2 ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) ∧
      (Real.log k) ^ 2 < k ∧ 3 ≤ k := by
    obtain ⟨k₁, hk₁⟩ : ∃ k₁ : ℕ, ∀ k ≥ k₁,
        2 ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) := by
      have hevent := eventually_le_rpow (1 - ϑ) 4 (sub_pos.mpr hϑ1)
      exact Filter.eventually_atTop.mp (hevent.mono fun k hk => by linarith)
    obtain ⟨k₂, hk₂⟩ : ∃ k₂ : ℕ, ∀ k ≥ k₂,
        (Real.log k) ^ 2 < k := Filter.eventually_atTop.mp log_sq_lt_self
    refine ⟨max k₁ (max k₂ 3), ?_⟩
    intro k hk
    exact ⟨hk₁ k (le_trans (le_max_left _ _) hk),
      hk₂ k (le_trans (le_max_of_le_right (le_max_left _ _)) hk),
      le_trans (le_max_of_le_right (le_max_right _ _)) hk⟩
  refine ⟨k₀ + 3, ?_⟩
  intro k hk n hn₁ hn₂
  have hKon : ((badSetAt ϑ k n).card : ℝ) <
      c₆ * (k : ℝ) ^ ϑ *
        (((n : ℝ) * ((2 : ℕ)!) * (lamML ϑ k n) ^ 2 /
            (k : ℝ) ^ (2 + 1)) ^ ((1 : ℝ) / 3) +
          ((k : ℝ) ^ ((2 : ℝ) + ϑ) /
            ((n : ℝ) * ((2 : ℕ)!) * (lamML ϑ k n) ^ 2)) ^ 1 +
          ((3 * lamML ϑ k n) / (k : ℝ)) ^ ((1 : ℝ) / 4)) +
        2 * (2 : ℝ) * lamML ϑ k n := by
    convert konyagin_application (lamML ϑ k n) ϑ
      (lamML_ge_one ϑ k n (by linarith [hk₀ k (by linarith)])
        (by exact_mod_cast hn₁.trans_le' (div_nonneg (sq_nonneg _) (sq_nonneg _))) hn₂)
      hϑ0 hϑ1 n k 2 (by
        rw [div_lt_iff₀] at hn₁
        · exact_mod_cast (by
            nlinarith [hk₀ k (by linarith),
              show (k : ℝ) ≥ 3 by norm_cast; linarith] : (k : ℝ) < n)
        · exact sq_pos_of_pos <| Real.log_pos <| Nat.one_lt_cast.mpr <|
            by linarith [hk₀ k (by linarith)])
      (by norm_num) (hk₀ k (by linarith)).1 using 1
    norm_num [Nat.factorial]
  have hT1 : ((n : ℝ) * ((2 : ℕ)!) * (lamML ϑ k n) ^ 2 /
      (k : ℝ) ^ (2 + 1)) ^ ((1 : ℝ) / 3) =
      ((k : ℝ) ^ (ϑ - 1) * (Real.log k) ^ 2) ^ ((1 : ℝ) / 3) := by
    have hbase : (n : ℝ) * ((2 : ℕ)!) * (lamML ϑ k n) ^ 2 =
        (k : ℝ) ^ (2 + ϑ) * (Real.log k) ^ 2 := by
      rw [lamML_sq]
      ring_nf
      · simp +decide [mul_comm, show n ≠ 0 by
          rintro rfl
          exact absurd hn₁ (by norm_num; positivity)]
      · exact_mod_cast hn₁.trans_le' (div_nonneg (sq_nonneg _) (sq_nonneg _))
    rw [hbase, mul_div_right_comm]
    rw [← Real.rpow_natCast, ← Real.rpow_sub (by norm_cast; linarith)]
    ring_nf
  have hT2 : ((k : ℝ) ^ ((2 : ℝ) + ϑ) /
      ((n : ℝ) * ((2 : ℕ)!) * (lamML ϑ k n) ^ 2)) ^ 1 =
      (Real.log k) ^ (-(2 : ℝ)) := by
    rw [show (n : ℝ) * 2! * lamML ϑ k n ^ 2 =
        (k : ℝ) ^ (2 + ϑ) * (Real.log k) ^ 2 by
      rw [lamML_sq]
      ring_nf
      · by_cases hn : n = 0 <;> simp_all +decide [mul_comm]
        exact absurd hT1 (ne_of_lt
          (Real.rpow_pos_of_pos
            (mul_pos (Real.rpow_pos_of_pos (Nat.cast_pos.mpr (by linarith)) _)
              (sq_pos_of_pos (Real.log_pos
                (Nat.one_lt_cast.mpr (by linarith [hk₀ k (by linarith)]))))) _))
      · exact_mod_cast hn₁.trans_le' (div_nonneg (sq_nonneg _) (sq_nonneg _))]
    norm_cast
    norm_num
    rw [← div_div, div_self
      (ne_of_gt (Real.rpow_pos_of_pos (Nat.cast_pos.mpr (by linarith)) _)), one_div]
  have hT3 : ((3 * lamML ϑ k n) / (k : ℝ)) ^ ((1 : ℝ) / 4) ≤
      (3 * lamUB ϑ k / (k : ℝ)) ^ ((1 : ℝ) / 4) := by
    gcongr
    · exact div_nonneg
        (mul_nonneg zero_le_three
          (show 0 ≤ lamML ϑ k n from
            mul_nonneg (Real.sqrt_nonneg _) (Real.log_natCast_nonneg _)))
        (Nat.cast_nonneg _)
    · have h := lamML_le_lamUB ϑ k n (by linarith) hn₁
      gcongr
  have hLast : 2 * (2 : ℝ) * lamML ϑ k n ≤ 4 * lamUB ϑ k := by
    have h := lamML_le_lamUB ϑ k n (by linarith) hn₁
    norm_num at *
    linarith
  unfold gML
  nlinarith [show 0 < c₆ * (k : ℝ) ^ ϑ by
    exact mul_pos
      (lt_of_lt_of_le (by norm_num) (show (256 : ℝ) ≤ c₆ by
        unfold c₆ C₀_const B_const K_const c₉
        norm_num))
      (Real.rpow_pos_of_pos (Nat.cast_pos.mpr (by linarith)) _)]

/-- The variable-theta medium-large envelope is negligible relative to any
positive short-prime constant. -/
lemma ml_rhs_le (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (C : ℝ) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      gML ϑ k ≤ C * (k : ℝ) ^ ϑ / Real.log k := by
  obtain ⟨k₁, hk₁⟩ : ∃ k₁ : ℕ, ∀ k : ℕ, k₁ ≤ k →
      c₆ * (k : ℝ) ^ ϑ *
          ((k : ℝ) ^ (ϑ - 1) * (Real.log k) ^ 2) ^ ((1 : ℝ) / 3) ≤
        C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
    have hevent : ∀ᶠ k : ℕ in Filter.atTop,
        c₆ * (k : ℝ) ^ ((4 * ϑ - 1) / 3 : ℝ) *
            (Real.log k) ^ (2 / 3 : ℝ) ≤
          C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
      exact poly_log_lt c₆ ((4 * ϑ - 1) / 3) (2 / 3) ϑ
        (by linarith) (C / 4) (by linarith)
    obtain ⟨k₁, hk₁⟩ := Filter.eventually_atTop.mp hevent
    refine ⟨k₁ + 2, fun k hk => le_trans ?_ (hk₁ k (by omega))⟩
    norm_num [Real.rpow_def_of_pos, show k > 0 by omega]
    ring_nf
    norm_num
    rw [Real.mul_rpow (by positivity) (by positivity), ← Real.exp_mul]
    ring_nf
    norm_num [Real.exp_add, Real.exp_neg, Real.exp_mul,
      Real.exp_log (show 0 < (k : ℝ) by norm_cast; omega)]
    ring_nf
    norm_num
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity)]
    ring_nf
    norm_num [← Real.rpow_mul (Nat.cast_nonneg _),
      ← Real.rpow_neg (Nat.cast_nonneg _)]
    ring_nf
    norm_num
    rw [show (ϑ * (4 / 3) : ℝ) = ϑ + ϑ * (1 / 3) by ring,
      Real.rpow_add (by norm_cast; omega)]
    ring_nf
    norm_num
  obtain ⟨k₂, hk₂⟩ : ∃ k₂ : ℕ, ∀ k : ℕ, k₂ ≤ k →
      c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-(2 : ℝ)) ≤
        C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
    exact Filter.eventually_atTop.mp
      (poly_log_lt_eq c₆ ϑ (C / 4) (by linarith))
  obtain ⟨k₃, hk₃⟩ : ∃ k₃ : ℕ, ∀ k : ℕ, k₃ ≤ k →
      c₆ * (k : ℝ) ^ ϑ *
          (3 * (1 / Real.sqrt 2) * (k : ℝ) ^ (ϑ / 2) *
            (Real.log k) ^ 2 / (k : ℝ)) ^ (1 / 4 : ℝ) ≤
        C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
    have hevent := poly_log_lt
      (c₆ * (3 * (1 / Real.sqrt 2)) ^ (1 / 4 : ℝ))
      ((9 * ϑ - 2) / 8) (1 / 2) ϑ (by linarith)
      (C / 4) (by linarith)
    obtain ⟨k₃, hk₃⟩ := Filter.eventually_atTop.mp hevent
    refine ⟨k₃ + 2, ?_⟩
    intro k hk
    convert hk₃ k (by omega) using 1
    rw [Real.div_rpow (by positivity) (by positivity),
      Real.mul_rpow (by positivity) (by positivity),
      Real.mul_rpow (by positivity) (by positivity)]
    ring_nf
    rw [← Real.rpow_mul (by positivity), ← Real.rpow_natCast,
      ← Real.rpow_mul (by positivity)]
    ring_nf
    rw [show (-1 / 4 + ϑ * (9 / 8) : ℝ) =
      ϑ + ϑ * (1 / 8) - 1 / 4 by ring]
    norm_num [Real.rpow_add (by norm_cast; omega : 0 < (k : ℝ)),
      Real.rpow_sub (by norm_cast; omega : 0 < (k : ℝ))]
    ring
  obtain ⟨k₄, hk₄⟩ : ∃ k₄ : ℕ, ∀ k : ℕ, k₄ ≤ k →
      4 * (1 / Real.sqrt 2) * (k : ℝ) ^ (ϑ / 2) * (Real.log k) ^ 2 ≤
        C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
    have hevent : ∀ᶠ k : ℕ in Filter.atTop,
        4 * (1 / Real.sqrt 2) * (k : ℝ) ^ (ϑ / 2) * (Real.log k) ^ 2 ≤
          C / 4 * (k : ℝ) ^ ϑ / Real.log k := by
      convert poly_log_lt (4 * (1 / Real.sqrt 2)) (ϑ / 2) 2 ϑ
        (by nlinarith) (C / 4) (by linarith) using 1 <;> norm_num
    exact Filter.eventually_atTop.mp hevent
  refine ⟨max k₁ (max k₂ (max k₃ k₄)), ?_⟩
  intro k hk
  simp only [max_le_iff] at hk
  unfold gML lamUB
  convert add_le_add
    (add_le_add (add_le_add (hk₁ k hk.1) (hk₂ k hk.2.1))
      (hk₃ k hk.2.2.1))
    (hk₄ k hk.2.2.2) using 1 <;> ring_nf

/-- A complete nontrivial variable-theta range: the medium-large part follows
from the abstract prime interval input for every `0<ϑ<1`. -/
theorem case_mediumlarge (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (k : ℝ) ^ 2 / (Real.log k) ^ 2 < (n : ℝ) →
      (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ) →
      SourceIntervalConclusion ϑ k n := by
  obtain ⟨C, hC, kb, hb⟩ := hPI
  obtain ⟨k1, hk1card⟩ := ml_card_bound ϑ hϑ0 hϑ1
  obtain ⟨k2, hk2rhs⟩ := ml_rhs_le ϑ hϑ0 hϑ1 C hC
  refine ⟨max (max kb k1) (max k2 2), ?_⟩
  intro k hk n hlow hhigh
  have hkb : kb ≤ k := le_trans (le_trans (le_max_left _ _) (le_max_left _ _)) hk
  have hki1 : k1 ≤ k := le_trans (le_trans (le_max_right _ _) (le_max_left _ _)) hk
  have hki2 : k2 ≤ k := le_trans (le_trans (le_max_left _ _) (le_max_right _ _)) hk
  have hk1 : 1 ≤ k := by omega
  have hprime : C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ) := hb k hkb
  have hcard : ((badSetAt ϑ k n).card : ℝ) <
      C * (k : ℝ) ^ ϑ / Real.log k :=
    lt_of_lt_of_le (hk1card k hki1 n hlow hhigh) (hk2rhs k hki2)
  exact konyagin_finish_at ϑ hϑ0.le k n hk1 C hprime hcard

#print axioms lamML_ge_one
#print axioms ml_card_bound
#print axioms ml_rhs_le
#print axioms case_mediumlarge

end ParametricML

namespace ParametricSmall

/-- Variable-theta excess-width bound used to move the short-prime interval. -/
lemma excess_le (ϑ : ℝ) (hϑ0 : 0 ≤ ϑ) (hϑ1 : ϑ ≤ 1)
    (k N : ℕ) (hk : 1 ≤ k) (hkN : (k : ℝ) ≤ (N : ℝ))
    (hNk : (N : ℝ) ≤ (k : ℝ) + 2 * (k : ℝ) ^ ϑ + 1) :
    (N : ℝ) ^ ϑ - (k : ℝ) ^ ϑ ≤
      (3 : ℝ) ^ ϑ * (k : ℝ) ^ (ϑ * ϑ) := by
  have hsub : (N : ℝ) ^ ϑ - (k : ℝ) ^ ϑ ≤ ((N : ℝ) - k) ^ ϑ := by
    rw [sub_le_iff_le_add']
    convert Real.rpow_add_le_add_rpow _ _ _ _ using 1 <;> norm_num
    · exact_mod_cast hkN
    · exact hϑ0
    · exact hϑ1
  refine le_trans hsub ?_
  refine le_trans (Real.rpow_le_rpow (sub_nonneg.mpr hkN)
    (show (N : ℝ) - k ≤ 3 * (k : ℝ) ^ ϑ by
      linarith [show (1 : ℝ) ≤ (k : ℝ) ^ ϑ by
        exact Real.one_le_rpow (by exact_mod_cast hk) hϑ0]) hϑ0) ?_
  rw [Real.mul_rpow (by positivity) (by positivity),
    ← Real.rpow_mul (by positivity)]

/-- The abstract prime count eventually beats the excess width uniformly in
the shifted base. -/
lemma count_beats_excess (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (C : ℝ) (hC : 0 < C) :
    ∀ᶠ k : ℕ in Filter.atTop, ∀ N : ℕ, (k : ℝ) ≤ (N : ℝ) →
      (N : ℝ) ≤ (k : ℝ) + 2 * (k : ℝ) ^ ϑ + 1 →
      (N : ℝ) ^ ϑ - (k : ℝ) ^ ϑ + 2 <
        C * (N : ℝ) ^ ϑ / Real.log N := by
  have step1 : ∀ᶠ k : ℕ in atTop,
      (3 : ℝ) ^ ϑ * (k : ℝ) ^ (ϑ * ϑ) + 3 ≤
        (C / 2) * (k : ℝ) ^ ϑ / Real.log k := by
    have hA : ∀ᶠ k : ℕ in Filter.atTop,
        (3 : ℝ) ^ ϑ * (k : ℝ) ^ (ϑ * ϑ) ≤
          (C / 4) * (k : ℝ) ^ ϑ / Real.log k := by
      have hevent := poly_log_lt ((3 : ℝ) ^ ϑ) (ϑ * ϑ) 0 ϑ
        (by nlinarith) (C / 4) (by positivity)
      simpa using hevent
    have hB : ∀ᶠ k : ℕ in Filter.atTop,
        3 ≤ (C / 4) * (k : ℝ) ^ ϑ / Real.log k := by
      have hevent := poly_log_lt (3 : ℝ) 0 0 ϑ hϑ0
        (C / 4) (by positivity)
      simpa using hevent
    filter_upwards [hA, hB] with k hk₁ hk₂
    ring_nf at *
    linarith
  filter_upwards [step1, Filter.eventually_ge_atTop 4] with k hkA hk4
  intro N hkN hNk
  have hNle : (N : ℝ) ≤ 4 * (k : ℝ) := by
    linarith [show (k : ℝ) ^ ϑ ≤ k by
      exact le_trans
        (Real.rpow_le_rpow_of_exponent_le (by norm_cast; linarith) hϑ1.le)
        (by norm_num), show (k : ℝ) ≥ 4 by norm_cast]
  have hlog : Real.log (N : ℝ) ≤ 2 * Real.log (k : ℝ) := by
    erw [← Real.log_pow]
    gcongr
    · norm_cast at *
      linarith
    · norm_cast at *
      nlinarith
  have hlogNpos : 0 < Real.log (N : ℝ) := by
    exact Real.log_pos <| by norm_cast at *; linarith
  have hexp : (N : ℝ) ^ ϑ - (k : ℝ) ^ ϑ + 2 <
      (C / 2) * (k : ℝ) ^ ϑ / Real.log k := by
    have hwidth := excess_le ϑ hϑ0.le hϑ1.le k N (by omega) hkN hNk
    linarith
  have hrhs : (C / 2) * (k : ℝ) ^ ϑ / Real.log k ≤
      C * (N : ℝ) ^ ϑ / Real.log N := by
    rw [div_le_div_iff₀] <;> try positivity
    · have hpowers : (k : ℝ) ^ ϑ * Real.log N ≤
          2 * (N : ℝ) ^ ϑ * Real.log k := by
        have hpow : (k : ℝ) ^ ϑ ≤ (N : ℝ) ^ ϑ :=
          Real.rpow_le_rpow (by positivity) hkN hϑ0.le
        nlinarith [Real.rpow_pos_of_pos (by positivity : 0 < (k : ℝ)) ϑ]
      nlinarith
    · exact Real.log_pos <| by norm_cast; linarith
  exact hexp.trans_le hrhs

/-- Abstract `PI(ϑ)` supplies a prime in every shifted length-`k^ϑ` window
whose base lies in `[k,k+2k^ϑ]`. -/
lemma exists_prime_in_window (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ a : ℝ,
      (k : ℝ) ≤ a → a ≤ (k : ℝ) + 2 * (k : ℝ) ^ ϑ →
      ∃ p : ℕ, p.Prime ∧ a < (p : ℝ) ∧
        (p : ℝ) < a + (k : ℝ) ^ ϑ := by
  obtain ⟨C, hC, k₀, hk₀⟩ := hPI
  obtain ⟨k₁, hk₁⟩ := Filter.eventually_atTop.mp
    (count_beats_excess ϑ hϑ0 hϑ1 C hC)
  refine ⟨max (max k₀ k₁) 2, ?_⟩
  intro k hk a ha₁ ha₂
  set N := ⌈a⌉₊ with hN
  have hN₁ : (k : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast ha₁.trans (Nat.le_ceil _)
  have hN₂ : (N : ℝ) ≤ (k : ℝ) + 2 * (k : ℝ) ^ ϑ + 1 := by
    exact (Nat.ceil_lt_add_one (by linarith)).le.trans (by linarith)
  have hN₃ : (N : ℝ) < a + 1 := by
    exact Nat.ceil_lt_add_one (by
      linarith [show (k : ℝ) ≥ 2 by norm_cast; linarith [le_max_right (max k₀ k₁) 2]])
  have hN₄ : (k : ℝ) ≤ N := by exact_mod_cast hN₁
  have hprimeN : C * (N : ℝ) ^ ϑ / Real.log N ≤
      primeCard (N : ℝ) ((N : ℝ) + (N : ℝ) ^ ϑ) := by
    exact hk₀ N (by
      norm_cast at *
      linarith [Nat.le_max_left (max k₀ k₁) 2,
        Nat.le_max_right (max k₀ k₁) 2,
        Nat.le_max_left k₀ k₁, Nat.le_max_right k₀ k₁])
  have hcarddiff : primeCard (N : ℝ) (a + (k : ℝ) ^ ϑ) ≥
      primeCard (N : ℝ) ((N : ℝ) + (N : ℝ) ^ ϑ) -
        ((N : ℝ) ^ ϑ - (k : ℝ) ^ ϑ + 2) := by
    have hmono : primeCard (N : ℝ) ((N : ℝ) + (N : ℝ) ^ ϑ) ≤
        primeCard (N : ℝ) (a + (k : ℝ) ^ ϑ) +
          ((N : ℝ) + (N : ℝ) ^ ϑ - (a + (k : ℝ) ^ ϑ) + 1) := by
      convert primeCard_le_add (N : ℝ) (a + (k : ℝ) ^ ϑ)
        (N + (N : ℝ) ^ ϑ) _ using 1
      exact add_le_add (Nat.le_ceil _)
        (Real.rpow_le_rpow (by linarith) (by linarith) hϑ0.le)
    linarith
  have hcardpos : 0 < primeCard (N : ℝ) (a + (k : ℝ) ^ ϑ) := by
    exact_mod_cast (by
      linarith [hk₁ k (by
        linarith [le_max_left (max k₀ k₁) 2,
          le_max_right (max k₀ k₁) 2, le_max_left k₀ k₁,
          le_max_right k₀ k₁]) N hN₄ hN₂] :
        (0 : ℝ) < primeCard (N : ℝ) (a + k ^ ϑ))
  obtain ⟨p, hp, hpN, hpupper⟩ := exists_prime_of_primeCard_pos _ _ hcardpos
  exact ⟨p, hp, by
    linarith [Nat.le_ceil a, show (p : ℝ) ≥ N by exact_mod_cast hpN.le], hpupper⟩

/-- A complete variable-theta small range derived only from abstract
`PrimeIntervalInput ϑ`. -/
theorem case_small (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 - ϑ) →
      SourceIntervalConclusion ϑ k n := by
  obtain ⟨kw, hw⟩ := exists_prime_in_window ϑ hϑ0 hϑ1 hPI
  refine ⟨max kw 2, ?_⟩
  intro k hk n hn1 hn2
  set m := (n - 1).natAbs / k
  have hm : (m : ℤ) * k ≤ n - 1 ∧ n - 1 < ((m + 1) : ℤ) * k := by
    norm_num +zetaDelta at *
    constructor <;> nlinarith
      [Int.mul_ediv_add_emod (|n - 1|) k,
        Int.emod_nonneg (|n - 1|) (by linarith : (k : ℤ) ≠ 0),
        Int.emod_lt_of_pos (|n - 1|) (by linarith : (k : ℤ) > 0),
        abs_of_nonneg (by linarith : 0 ≤ n - 1)]
  have hm_ge2 : 2 ≤ m := by
    exact Nat.le_div_iff_mul_le (by linarith [le_max_right kw 2]) |>.2
      (by cases abs_cases (n - 1) <;> nlinarith [le_max_right kw 2])
  have hm_lt : (m : ℝ) < (1 / 2) * (k : ℝ) ^ (1 - ϑ) := by
    rw [show (2 - ϑ : ℝ) = 1 - ϑ + 1 by ring, Real.rpow_add] at * <;>
      norm_num at *
    · nlinarith [(by norm_cast : (2 : ℝ) * k < n),
        (by norm_cast : (m : ℝ) * k < n ∧ n ≤ (m + 1) * k)]
    · linarith
  have hkey : (2 * (m : ℝ) - 1) * (k : ℝ) ^ ϑ < (k : ℝ) := by
    have hkey : (2 * (m : ℝ) - 1) * (k : ℝ) ^ ϑ <
        (k : ℝ) ^ (1 - ϑ) * (k : ℝ) ^ ϑ :=
      mul_lt_mul_of_pos_right (by linarith)
        (Real.rpow_pos_of_pos
          (Nat.cast_pos.mpr (by linarith [Nat.le_max_right kw 2])) _)
    convert hkey using 1
    rw [← Real.rpow_add'] <;> norm_num
  by_cases hcase : (n : ℝ) <
      (m : ℝ) * k + (m : ℝ) * (k : ℝ) ^ ϑ
  · have hkw : kw ≤ k := by
      linarith [Nat.le_max_left kw 2, Nat.le_max_right kw 2]
    have hbaseLower : (k : ℝ) ≤
        k + (m : ℝ) / (m - 1) * (k : ℝ) ^ ϑ := by
      exact le_add_of_nonneg_right
        (mul_nonneg
          (div_nonneg (Nat.cast_nonneg _)
            (sub_nonneg.mpr (Nat.one_le_cast.mpr (by linarith))))
          (Real.rpow_nonneg (Nat.cast_nonneg _) _))
    have hbaseUpper : (k : ℝ) + (m : ℝ) / (m - 1) * (k : ℝ) ^ ϑ ≤
        (k : ℝ) + 2 * (k : ℝ) ^ ϑ := by
      gcongr
      rw [div_le_iff₀] <;>
        linarith [show (m : ℝ) ≥ 2 by norm_cast]
    obtain ⟨p, hpprime, hpbounds⟩ := hw k hkw
      (k + (m : ℝ) / (m - 1) * (k : ℝ) ^ ϑ) hbaseLower hbaseUpper
    refine ⟨p, hpprime, ?_, ?_, ?_⟩
    · exact lt_of_le_of_lt
        (le_add_of_nonneg_right <| mul_nonneg
          (div_nonneg (Nat.cast_nonneg _)
            (sub_nonneg.mpr <| Nat.one_le_cast.mpr <| by linarith))
          (Real.rpow_nonneg (Nat.cast_nonneg _) _)) hpbounds.1
    · refine lt_of_lt_of_le hpbounds.2 ?_
      rw [div_mul_eq_mul_div, add_div', div_add', div_le_iff₀] <;>
        nlinarith only [show (m : ℝ) ≥ 2 by norm_cast,
          show (k : ℝ) ^ ϑ > 0 by
            exact Real.rpow_pos_of_pos
              (Nat.cast_pos.mpr <| by linarith [Nat.le_max_right kw 2]) _, hkey]
    · apply dvd_Pprod_of_mem k n p ((m - 1) * p)
      · rw [← @Int.cast_lt ℝ]
        push_cast
        nlinarith [show (m : ℝ) ≥ 2 by norm_cast,
          show (k : ℝ) ≥ 2 by norm_cast; linarith [Nat.le_max_right kw 2],
          Real.rpow_pos_of_pos
            (show (k : ℝ) > 0 by norm_cast; linarith [Nat.le_max_right kw 2]) ϑ,
          mul_div_cancel₀ (m : ℝ)
            (show (m - 1 : ℝ) ≠ 0 by
              linarith [show (m : ℝ) ≥ 2 by norm_cast])]
      · rcases m with (_ | _ | m) <;> norm_num at *
        rw [← @Int.cast_lt ℝ] at *
        push_cast at *
        nlinarith [mul_div_cancel₀ ((m : ℝ) + 1 + 1)
          (by linarith : (m : ℝ) + 1 ≠ 0)]
      · exact dvd_mul_left _ _
  · obtain ⟨p, hpprime, hpbounds⟩ : ∃ p : ℕ, p.Prime ∧
        (k : ℝ) < p ∧ p < (k : ℝ) + (k : ℝ) ^ ϑ := by
      exact hw k (le_trans (le_max_left _ _) hk) k (by norm_num)
        (by linarith [Real.rpow_nonneg (Nat.cast_nonneg k) ϑ])
    refine ⟨p, hpprime, hpbounds.1, ?_, ?_⟩
    · grind +splitIndPred
    · have hkpowpos : 0 < (k : ℝ) ^ ϑ :=
        Real.rpow_pos_of_pos
          (Nat.cast_pos.mpr (by linarith [Nat.le_max_right kw 2])) _
      apply dvd_Pprod_of_mem k n p ((m : ℤ) * p)
        (by nlinarith [show (m : ℤ) ≥ 2 by norm_cast,
          show (p : ℤ) ≥ k + 1 by exact_mod_cast hpbounds.1])
        (by exact_mod_cast (by
          nlinarith [show (m : ℝ) ≥ 2 by norm_cast, hkpowpos] :
            (m : ℝ) * p < n))
        (by exact dvd_mul_left _ _)

#print axioms excess_le
#print axioms count_beats_excess
#print axioms exists_prime_in_window
#print axioms case_small

end ParametricSmall

namespace ParametricMed

def medWindow (ϑ : ℝ) (k : ℕ) : Finset ℤ :=
  (Finset.Ioo (k : ℤ) ((k : ℤ) + ⌊(k : ℝ) ^ ϑ⌋ + 2)).filter
    (fun m : ℤ => (m : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ)

def medFiber (ϑ : ℝ) (k : ℕ) (n : ℤ) (h : ℤ) : Finset ℤ :=
  (medWindow ϑ k).filter (fun m : ℤ =>
    |(n : ℝ) / (m : ℝ) - (h : ℝ)| < 1 / (k : ℝ) ^ (1 - ϑ))

def medJ (ϑ : ℝ) (k : ℕ) (n : ℤ) : Finset ℤ :=
  Finset.Icc ⌊(n : ℝ) / ((k : ℝ) + (k : ℝ) ^ ϑ)⌋
    ⌈(n : ℝ) / (k : ℝ)⌉

lemma badSet_subset_biUnion (ϑ : ℝ) (k : ℕ) (n : ℤ)
    (hk1 : 1 ≤ k) (hn : 0 < n) :
    badSetAt ϑ k n ⊆ (medJ ϑ k n).biUnion (medFiber ϑ k n) := by
  intro m hm
  simp_all +decide
  refine ⟨round ((n : ℝ) / m), ?_, ?_⟩ <;>
    simp_all +decide [medJ, medFiber]
  · have hmbounds : (k : ℝ) < m ∧
        m < (k : ℝ) + (k : ℝ) ^ ϑ := by
      exact ⟨mod_cast Finset.mem_Ioo.mp
          (Finset.mem_filter.mp hm).1 |>.1,
        (Finset.mem_filter.mp hm).2.1⟩
    constructor <;> rw [round_eq] <;>
      norm_num [Int.floor_le, Int.le_ceil] at *
    · exact Int.floor_mono <| le_add_of_le_of_nonneg
        (div_le_div_of_nonneg_left (by positivity)
          (by linarith [show (k : ℝ) ≥ 1 by norm_cast]) (by linarith))
        (by positivity)
    · refine Int.le_of_lt_add_one (Int.floor_lt.mpr ?_)
      norm_num +zetaDelta at *
      linarith [show (n : ℝ) / m < (n : ℝ) / k by
        gcongr <;> linarith,
        Int.le_ceil ((n : ℝ) / k)]
  · unfold badSetAt at hm
    unfold medWindow at *
    aesop

lemma medJ_card_le (ϑ : ℝ) (k : ℕ) (n : ℤ)
    (hk1 : 1 ≤ k) (hn : 0 < n) :
    ((medJ ϑ k n).card : ℝ) ≤
      3 + (n : ℝ) / (k : ℝ) ^ (2 - ϑ) := by
  have hcei : (medJ ϑ k n).card ≤
      (⌈(n : ℝ) / k⌉ -
        ⌊(n : ℝ) / (k + (k : ℝ) ^ ϑ)⌋ + 1) := by
    simp +decide [medJ]
    constructor <;>
      linarith [show ⌊(n : ℝ) / (k + k ^ ϑ)⌋ ≤
        ⌈(n : ℝ) / k⌉ from
          Int.floor_le_ceil _ |> le_trans <| Int.ceil_mono <| by
            gcongr
            linarith [Real.rpow_nonneg (Nat.cast_nonneg k) ϑ]]
  have hceilfloor : (⌈(n : ℝ) / k⌉ : ℝ) < (n : ℝ) / k + 1 ∧
      (⌊(n : ℝ) / (k + (k : ℝ) ^ ϑ)⌋ : ℝ) >
        (n : ℝ) / (k + (k : ℝ) ^ ϑ) - 1 :=
    ⟨Int.ceil_lt_add_one _, Int.sub_one_lt_floor _⟩
  have hdiff : (n : ℝ) / k -
      (n : ℝ) / (k + (k : ℝ) ^ ϑ) ≤
      (n : ℝ) / (k : ℝ) ^ (2 - ϑ) := by
    rw [Real.rpow_sub] <;> norm_num
    · field_simp
      nlinarith only [show (k : ℝ) ≥ 1 by norm_cast,
        show (k : ℝ) ^ ϑ ≥ 0 by positivity]
    · linarith
  push_cast [← @Int.cast_le ℝ] at *
  linarith

lemma medFiber_card_le (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 - ϑ) < (n : ℝ) → ∀ h : ℤ,
      ((medFiber ϑ k n h).card : ℝ) ≤
        1 + 8 * (k : ℝ) ^ (1 + ϑ) / (n : ℝ) := by
  obtain ⟨k₀, hk₀⟩ : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      8 ≤ (k : ℝ) ^ (1 - ϑ) := by
    exact Filter.eventually_atTop.mp
      (eventually_le_rpow (1 - ϑ) 8 (sub_pos.mpr hϑ1))
  refine ⟨k₀ + 2, ?_⟩
  intro k hk n hn h
  norm_num at *
  by_cases hempty : medFiber ϑ k n h = ∅
  · norm_num [hempty]
    exact add_nonneg zero_le_one (div_nonneg (by positivity)
      (by exact_mod_cast (by
        linarith [show (0 : ℝ) ≤ k ^ (2 - ϑ) by positivity] :
          (0 : ℝ) ≤ n)))
  · obtain ⟨m₀, hm₀⟩ : ∃ m₀ ∈ medFiber ϑ k n h,
        (k : ℝ) < m₀ ∧ (m₀ : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ ∧
        |(n : ℝ) / m₀ - (h : ℝ)| < 1 / (k : ℝ) ^ (1 - ϑ) := by
      obtain ⟨m₀, hm₀⟩ := Finset.nonempty_of_ne_empty hempty
      refine ⟨m₀, hm₀, ?_⟩
      simp_all +decide [medFiber, medWindow]
      exact_mod_cast hm₀.1.1.1
    have hnRpos : (0 : ℝ) < n :=
      lt_of_le_of_lt (by positivity) hn
    have hhge : (h : ℝ) ≥ (n : ℝ) / (2 * (k : ℝ)) := by
      have hhrough : (h : ℝ) >
          (n : ℝ) / ((k : ℝ) + (k : ℝ) ^ ϑ) - 1 := by
        have hdiv : (n : ℝ) / m₀ >
            (n : ℝ) / ((k : ℝ) + (k : ℝ) ^ ϑ) := by
          gcongr
          · linarith [hm₀.2.1,
              show (0 : ℝ) < k by norm_cast; linarith]
          · exact hm₀.2.2.1
        linarith [abs_lt.mp hm₀.2.2.2,
          show (1 : ℝ) / k ^ (1 - ϑ) ≤ 1 by
            exact div_le_self zero_le_one <|
              Real.one_le_rpow (by norm_cast; linarith) (by linarith)]
      have hgap : (n : ℝ) / ((k : ℝ) + (k : ℝ) ^ ϑ) -
          (n : ℝ) / (2 * (k : ℝ)) ≥ 1 := by
        rw [div_sub_div, ge_iff_le, le_div_iff₀]
        · have hkexp : (k : ℝ) ^ (2 - ϑ) ≥ 8 * (k : ℝ) := by
            have hkpow := hk₀ k (by linarith)
            exact le_trans
              (mul_le_mul_of_nonneg_right hkpow (Nat.cast_nonneg _))
              (by
                rw [← Real.rpow_add_one (by norm_cast; linarith)]
                ring_nf
                norm_num)
          rw [Real.rpow_sub] at * <;> norm_num at *
          · nlinarith [show (k : ℝ) ^ ϑ > 0 by
              exact Real.rpow_pos_of_pos
                (Nat.cast_pos.mpr (by linarith)) _,
              show (k : ℝ) ^ ϑ ≤ k by
                exact le_trans
                  (Real.rpow_le_rpow_of_exponent_le
                    (by norm_cast; linarith) hϑ1.le) (by norm_num),
              mul_div_cancel₀ ((k : ℝ) ^ 2)
                (show (k : ℝ) ^ ϑ ≠ 0 by
                  exact ne_of_gt (Real.rpow_pos_of_pos
                    (Nat.cast_pos.mpr (by linarith)) _))]
          · linarith
          · lia
          · linarith
        · exact mul_pos
            (add_pos_of_pos_of_nonneg (Nat.cast_pos.mpr (by linarith))
              (Real.rpow_nonneg (Nat.cast_nonneg _) _))
            (mul_pos zero_lt_two (Nat.cast_pos.mpr (by linarith)))
        · exact ne_of_gt
            (add_pos_of_pos_of_nonneg (Nat.cast_pos.mpr (by linarith))
              (Real.rpow_nonneg (Nat.cast_nonneg _) _))
        · norm_cast
          linarith
      linarith
    have habs : ∀ m ∈ medFiber ϑ k n h,
        |(m : ℝ) - (n : ℝ) / (h : ℝ)| <
          4 * (k : ℝ) ^ (1 + ϑ) / (n : ℝ) := by
      intro m hm
      have hstep : |(m : ℝ) - (n : ℝ) / (h : ℝ)| ≤
          (m : ℝ) / (h : ℝ) *
            |(n : ℝ) / (m : ℝ) - (h : ℝ)| := by
        have hmpos : 0 < m := by
          have hkm : (k : ℤ) < m :=
            Finset.mem_Ioo.mp
              (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).1 |>.1
          omega
        have hkRpos : (0 : ℝ) < k := by norm_cast; linarith
        have hhRpos : (0 : ℝ) < h :=
          lt_of_lt_of_le (div_pos hnRpos (mul_pos zero_lt_two hkRpos)) hhge
        field_simp
        rw [abs_div, abs_div, abs_of_pos hhRpos,
          abs_of_pos (by exact_mod_cast hmpos : (0 : ℝ) < m)]
        rw [mul_div_cancel₀ _ (by positivity),
          mul_div_cancel₀ _ (by positivity), abs_sub_comm]
      have hmdiv : (m : ℝ) / (h : ℝ) ≤
          4 * (k : ℝ) ^ 2 / (n : ℝ) := by
        have hmle : (m : ℝ) ≤ 2 * (k : ℝ) := by
          have hmupper : (m : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ :=
            (Finset.mem_filter.mp (Finset.mem_filter.mp hm).1).2
          exact_mod_cast Int.le_of_lt_add_one (by
            rw [← @Int.cast_lt ℝ]
            push_cast
            linarith [show (k : ℝ) ^ ϑ ≤ k by
              exact le_trans
                (Real.rpow_le_rpow_of_exponent_le
                  (by norm_cast; linarith) hϑ1.le) (by norm_num)])
        rw [div_le_div_iff₀] <;> norm_num at *
        · rw [div_le_iff₀] at hhge <;>
            nlinarith [show (k : ℝ) ≥ 2 by norm_cast; linarith,
              show (n : ℝ) > 0 by exact lt_of_le_of_lt (by positivity) hn]
        · exact_mod_cast hhge.trans_lt'
            (div_pos (show (0 : ℝ) < n by
              exact lt_of_le_of_lt (by positivity) hn)
              (by norm_cast; linarith))
        · exact_mod_cast hn.trans_le'
            (mul_nonneg (by norm_num)
              (Real.rpow_nonneg (Nat.cast_nonneg _) _))
      have hclose : |(n : ℝ) / (m : ℝ) - (h : ℝ)| <
          1 / (k : ℝ) ^ (1 - ϑ) := (Finset.mem_filter.mp hm).2
      refine lt_of_le_of_lt hstep <| lt_of_le_of_lt
        (mul_le_mul_of_nonneg_right hmdiv (abs_nonneg _)) ?_
      convert mul_lt_mul_of_pos_left hclose
        (show (0 : ℝ) < 4 * k ^ 2 / n by
          exact div_pos (by norm_cast; nlinarith)
            (by exact_mod_cast (by
              linarith [show (0 : ℝ) < n by
                exact lt_of_le_of_lt (by positivity) hn] : (0 : ℝ) < n))) using 1
      ring_nf
      rw [show (1 + ϑ : ℝ) = 2 - (1 - ϑ) by ring,
        Real.rpow_sub] <;> norm_num
      ring
      linarith
    have hcard : ((medFiber ϑ k n h).card : ℝ) ≤
        2 * (4 * (k : ℝ) ^ (1 + ϑ) / (n : ℝ)) + 1 := by
      have hbound := card_int_abs_sub_lt_le ((n : ℝ) / h)
        (4 * (k : ℝ) ^ (1 + ϑ) / n) ?_ (medFiber ϑ k n h)
      · convert hbound using 2
        rw [Finset.filter_true_of_mem habs]
      · exact div_nonneg
          (mul_nonneg zero_le_four
            (Real.rpow_nonneg (Nat.cast_nonneg _) _))
          hnRpos.le
    convert hcard using 1 <;> ring

def gMed (ϑ : ℝ) (k : ℕ) : ℝ :=
  3 + 56 * (k : ℝ) ^ (2 * ϑ - 1) +
    (k : ℝ) ^ ϑ * (Real.log k) ^ (-(2 : ℝ))

lemma med_card_bound (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 - ϑ) < (n : ℝ) →
      (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2 →
      ((badSetAt ϑ k n).card : ℝ) < gMed ϑ k := by
  have hbound : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 - ϑ) < (n : ℝ) →
      (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2 →
      ((badSetAt ϑ k n).card : ℝ) ≤
        (3 + (n : ℝ) / (k : ℝ) ^ (2 - ϑ)) *
          (1 + 8 * (k : ℝ) ^ (1 + ϑ) / (n : ℝ)) := by
    obtain ⟨k₀, hk₀⟩ := medFiber_card_le ϑ hϑ0 hϑ1
    refine ⟨max k₀ 2, ?_⟩
    intro k hk n hn hhigh
    have hk0 : k₀ ≤ k := le_trans (le_max_left _ _) hk
    have hk1 : 1 ≤ k := by linarith [le_max_right k₀ 2]
    have hn0 : 0 < n := by
      exact_mod_cast hn.trans_le'
        (mul_nonneg (by norm_num)
          (Real.rpow_nonneg (Nat.cast_nonneg _) _))
    have hcard : ((badSetAt ϑ k n).card : ℝ) ≤
        ∑ h ∈ medJ ϑ k n, ((medFiber ϑ k n h).card : ℝ) := by
      exact_mod_cast Finset.card_le_card
        (badSet_subset_biUnion ϑ k n hk1 hn0) |>.trans
          Finset.card_biUnion_le
    refine le_trans hcard <| le_trans
      (Finset.sum_le_sum fun x hx => hk₀ k hk0 n hn x) ?_
    have hj := medJ_card_le ϑ k n hk1 hn0
    norm_num at *
    nlinarith [show (0 : ℝ) ≤ 8 * k ^ (1 + ϑ) / n by positivity]
  obtain ⟨k₀, hk₀⟩ := hbound
  refine ⟨max k₀ 2, ?_⟩
  intro k hk n hn hn'
  refine lt_of_le_of_lt (hk₀ k (le_trans (le_max_left _ _) hk) n hn hn') ?_
  unfold gMed
  ring_nf
  norm_num
  have hsimp :
      (n : ℝ) * (k : ℝ) ^ (1 + ϑ) / (k : ℝ) ^ (2 - ϑ) =
          (n : ℝ) * (k : ℝ) ^ (2 * ϑ - 1) ∧
      (k : ℝ) ^ (1 + ϑ) / (n : ℝ) <
          2 * (k : ℝ) ^ (2 * ϑ - 1) ∧
      (n : ℝ) / (k : ℝ) ^ (2 - ϑ) ≤
          (k : ℝ) ^ ϑ * (Real.log k) ^ (-2 : ℝ) := by
    refine ⟨?_, ?_, ?_⟩
    · rw [mul_div_assoc,
        ← Real.rpow_sub (by norm_cast; linarith [le_max_right k₀ 2])]
      ring_nf
    · rw [div_lt_iff₀]
      · have hmul := mul_lt_mul_of_pos_left hn
          (mul_pos zero_lt_two
            (Real.rpow_pos_of_pos
              (Nat.cast_pos.mpr (by linarith [le_max_right k₀ 2]))
              (2 * ϑ - 1)))
        have hkpos : (0 : ℝ) < k := by
          exact_mod_cast lt_of_lt_of_le Nat.zero_lt_two
            (le_trans (le_max_right k₀ 2) hk)
        calc
          (k : ℝ) ^ (1 + ϑ) = (k : ℝ) ^ ((2 * ϑ - 1) + (2 - ϑ)) := by
            congr 1
            ring
          _ = (k : ℝ) ^ (2 * ϑ - 1) * (k : ℝ) ^ (2 - ϑ) := by
            rw [Real.rpow_add hkpos]
          _ = 2 * (k : ℝ) ^ (2 * ϑ - 1) *
                (1 / 2 * (k : ℝ) ^ (2 - ϑ)) := by ring
          _ < 2 * (k : ℝ) ^ (2 * ϑ - 1) * (n : ℝ) := hmul
      · exact lt_of_le_of_lt (by positivity) hn
    · convert div_le_div_of_nonneg_right hn'
        (Real.rpow_nonneg (Nat.cast_nonneg k) _) using 1
      norm_cast
      norm_num
      ring_nf
      rw [show (k : ℝ) ^ ϑ = (k : ℝ) ^ (2 - (2 - ϑ)) by ring_nf,
        Real.rpow_sub] <;> norm_num
      ring
      linarith [le_max_right k₀ 2]
  ring_nf at *
  by_cases hnzero : n = 0 <;>
    simp_all +decide [mul_assoc, mul_comm, mul_left_comm]
  · exact absurd ‹_› (not_lt_of_ge (by positivity))
  · linarith

lemma med_rhs_le (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (C : ℝ) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      gMed ϑ k ≤ C * (k : ℝ) ^ ϑ / Real.log k := by
  have h1 : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      3 ≤ (C / 3) * (k : ℝ) ^ ϑ / Real.log k := by
    have hevent := poly_log_lt 3 0 0 ϑ hϑ0
      (C / 3) (by linarith)
    simpa [Filter.eventually_atTop] using hevent
  have h2 : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      56 * (k : ℝ) ^ (2 * ϑ - 1) ≤
        (C / 3) * (k : ℝ) ^ ϑ / Real.log k := by
    convert poly_log_lt 56 (2 * ϑ - 1) 0 ϑ
      (by linarith) (C / 3) (by linarith) using 1
    norm_num [Filter.eventually_atTop]
  have h3 : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      (k : ℝ) ^ ϑ * (Real.log k) ^ (-(2 : ℝ)) ≤
        (C / 3) * (k : ℝ) ^ ϑ / Real.log k := by
    convert poly_log_lt_eq 1 ϑ (C / 3) (by linarith) using 1
    norm_num [Filter.eventually_atTop]
  refine ⟨max h1.choose (max h2.choose h3.choose), ?_⟩
  intro k hk
  convert add_le_add_three
    (h1.choose_spec k (le_trans (le_max_left _ _) hk))
    (h2.choose_spec k (le_trans
      (le_max_of_le_right (le_max_left _ _)) hk))
    (h3.choose_spec k (le_trans
      (le_max_of_le_right (le_max_right _ _)) hk)) using 1
  ring

theorem case_medium (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 - ϑ) < (n : ℝ) →
      (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2 →
      SourceIntervalConclusion ϑ k n := by
  obtain ⟨C, hC, kb, hb⟩ := hPI
  obtain ⟨k1, hk1card⟩ := med_card_bound ϑ hϑ0 hϑ1
  obtain ⟨k2, hk2rhs⟩ := med_rhs_le ϑ hϑ0 hϑ1 C hC
  refine ⟨max (max kb k1) (max k2 2), ?_⟩
  intro k hk n hlow hhigh
  have hkb : kb ≤ k := le_trans (le_trans (le_max_left _ _) (le_max_left _ _)) hk
  have hki1 : k1 ≤ k := le_trans (le_trans (le_max_right _ _) (le_max_left _ _)) hk
  have hki2 : k2 ≤ k := le_trans (le_trans (le_max_left _ _) (le_max_right _ _)) hk
  have hk1 : 1 ≤ k := by omega
  have hprime : C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ) := hb k hkb
  have hcard : ((badSetAt ϑ k n).card : ℝ) <
      C * (k : ℝ) ^ ϑ / Real.log k :=
    lt_of_lt_of_le (hk1card k hki1 n hlow hhigh) (hk2rhs k hki2)
  exact konyagin_finish_at ϑ hϑ0.le k n hk1 C hprime hcard

#print axioms medFiber_card_le
#print axioms med_card_bound
#print axioms med_rhs_le
#print axioms case_medium

end ParametricMed

/-! ## Large range: theta-parametric balanced scale -/

namespace ParametricLarge

def E1expAt (ϑ : ℝ) (r : ℕ) : ℝ :=
  (1 - ϑ) * (2 * (r : ℝ) - 1) / (3 * (r : ℝ) - 2)

def lamLargeAt (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  ((k : ℝ) ^ ((r : ℝ) + 1 - E1expAt ϑ r) /
    ((n : ℝ) * (Nat.factorial r : ℝ))) ^ ((r : ℝ)⁻¹)

/-- The exact exponent obtained from minimality; no positive `E₁` term is
discarded. -/
def additiveExpAt (ϑ : ℝ) (r : ℕ) : ℝ :=
  ((4 - ϑ) * (r : ℝ) + ϑ - 3) /
    ((r : ℝ) * (3 * (r : ℝ) - 2))

def sharpAddExp (ϑ : ℝ) : ℝ := (9 - 2 * ϑ) / 21

lemma additiveExpAt_eq (ϑ : ℝ) (r : ℕ) (hr3 : 3 ≤ r) :
    additiveExpAt ϑ r =
      ((4 - ϑ) * (r : ℝ) + ϑ - 3) /
        ((r : ℝ) * (3 * (r : ℝ) - 2)) := by
  rfl

lemma additiveExpAt_balanced (ϑ : ℝ) (r : ℕ) (hr3 : 3 ≤ r) :
    (2 - ϑ - E1expAt ϑ r) / (r : ℝ) = additiveExpAt ϑ r := by
  have hrR : (3 : ℝ) ≤ r := by exact_mod_cast hr3
  have hD : 3 * (r : ℝ) - 2 ≠ 0 := by nlinarith
  have hnum :
      2 - ϑ - E1expAt ϑ r =
        ((4 - ϑ) * (r : ℝ) + ϑ - 3) /
          (3 * (r : ℝ) - 2) := by
    unfold E1expAt
    apply (eq_div_iff hD).2
    rw [sub_mul, sub_mul, div_mul_cancel₀ _ hD]
    ring
  unfold additiveExpAt
  rw [hnum, div_div]
  congr 1
  ring

lemma additiveExpAt_le_sharp (ϑ : ℝ) (r : ℕ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hr3 : 3 ≤ r) :
    additiveExpAt ϑ r ≤ sharpAddExp ϑ := by
  rw [additiveExpAt_eq ϑ r hr3]
  have hrR : (3 : ℝ) ≤ r := by exact_mod_cast hr3
  have hr0 : (0 : ℝ) < r := by positivity
  have h3r2 : (0 : ℝ) < 3 * (r : ℝ) - 2 := by nlinarith
  rw [div_le_iff₀ (mul_pos hr0 h3r2)]
  unfold sharpAddExp
  rw [show (9 - 2 * ϑ) / 21 *
      ((r : ℝ) * (3 * (r : ℝ) - 2)) =
      ((9 - 2 * ϑ) * ((r : ℝ) * (3 * (r : ℝ) - 2))) / 21 by ring]
  rw [le_div_iff₀ (by norm_num : (0 : ℝ) < 21)]
  have hcoef : (21 : ℝ) ≤ 27 - 6 * ϑ := by linarith
  have hmul : (3 : ℝ) * 21 ≤
      (r : ℝ) * (27 - 6 * ϑ) :=
    mul_le_mul hrR hcoef (by norm_num) (by norm_num)
  have hbracket : 0 ≤
      (r : ℝ) * (27 - 6 * ϑ) + 7 * ϑ - 21 := by nlinarith
  have hproduct : 0 ≤
      ((r : ℝ) - 3) *
        ((r : ℝ) * (27 - 6 * ϑ) + 7 * ϑ - 21) :=
    mul_nonneg (by linarith) hbracket
  nlinarith

lemma sharpAddExp_lt_theta (ϑ : ℝ) (hϑ : (9 : ℝ) / 23 < ϑ) :
    sharpAddExp ϑ < ϑ := by
  unfold sharpAddExp
  rw [div_lt_iff₀ (by norm_num : (0 : ℝ) < 21)]
  nlinarith

/-- Exact lower endpoint of polynomial absorption for the balanced additive
term. -/
lemma sharpAddExp_lt_theta_iff (ϑ : ℝ) :
    sharpAddExp ϑ < ϑ ↔ (9 : ℝ) / 23 < ϑ := by
  unfold sharpAddExp
  rw [div_lt_iff₀ (by norm_num : (0 : ℝ) < 21)]
  constructor <;> intro h <;> nlinarith

def BalancedLargeExponentFeasible (ϑ : ℝ) : Prop :=
  sharpAddExp ϑ < ϑ

lemma balancedLargeExponentFeasible_iff (ϑ : ℝ) :
    BalancedLargeExponentFeasible ϑ ↔ (9 : ℝ) / 23 < ϑ :=
  sharpAddExp_lt_theta_iff ϑ

lemma balancedLargeExponent_no_go (ϑ : ℝ)
    (hϑ : ϑ ≤ (9 : ℝ) / 23) : ¬ BalancedLargeExponentFeasible ϑ := by
  rw [balancedLargeExponentFeasible_iff]
  exact not_lt_of_ge hϑ

lemma lamLargeAt_pow (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hn0 : 0 < n) (hk0 : 0 < k) (hr1 : 1 ≤ r) :
    (lamLargeAt ϑ k n r) ^ r =
      (k : ℝ) ^ ((r : ℝ) + 1 - E1expAt ϑ r) /
        ((n : ℝ) * (Nat.factorial r : ℝ)) := by
  unfold lamLargeAt
  rw [← Real.rpow_natCast, ← Real.rpow_mul (by positivity)]
  norm_num [show r ≠ 0 by omega]

lemma lamLargeAt_ge_one (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hϑ1 : ϑ < 1) (hn0 : 0 < n) (hk : 1 < k) (hr3 : 3 ≤ r)
    (hub : (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + ϑ)) :
    1 ≤ lamLargeAt ϑ k n r := by
  refine Real.one_le_rpow ?_ ?_
  · rw [one_le_div]
    · refine hub.trans (Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega) ?_)
      unfold E1expAt
      rw [le_sub_comm, div_le_iff₀] <;>
        nlinarith [show (r : ℝ) ≥ 3 by norm_cast]
    · positivity
  · positivity

/-- Minimality gives the exact additive exponent, rather than the coarse
`(2-ϑ)/r` estimate in the fixed upstream file. -/
lemma lamLargeAt_lt_exact (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hn0 : 0 < n) (hk : 1 < k) (hr3 : 3 ≤ r)
    (hmin : (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ)) :
    lamLargeAt ϑ k n r < (k : ℝ) ^ (additiveExpAt ϑ r) := by
  unfold lamLargeAt
  calc
    ((k : ℝ) ^ ((r : ℝ) + 1 - E1expAt ϑ r) /
        ((n : ℝ) * (Nat.factorial r : ℝ))) ^ ((r : ℝ)⁻¹) <
        ((k : ℝ) ^ (2 - E1expAt ϑ r - ϑ)) ^ ((r : ℝ)⁻¹) := by
      apply Real.rpow_lt_rpow
      · positivity
      · rw [div_lt_iff₀ (by positivity)]
        refine lt_of_le_of_lt ?_
          (mul_lt_mul_of_pos_left
            (show (n : ℝ) * r.factorial >
              k ^ ((r : ℝ) - 1 + ϑ) * r from ?_) (by positivity))
        · rw [← mul_assoc, ← Real.rpow_add (by positivity)]
          ring_nf
          exact le_mul_of_one_le_left (by positivity) (by norm_cast; omega)
        · rcases r with _ | r <;> simp_all +decide [Nat.factorial_succ]
          nlinarith [show (k : ℝ) ^ ((r : ℝ) + ϑ) > 0 by positivity]
      · positivity
    _ = (k : ℝ) ^ (additiveExpAt ϑ r) := by
      rw [← Real.rpow_mul (by positivity)]
      congr 1
      rw [show (r : ℝ)⁻¹ = 1 / (r : ℝ) by ring]
      rw [← additiveExpAt_balanced ϑ r hr3]
      ring

lemma lamLargeAt_lt_sharp (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hn0 : 0 < n) (hk : 1 < k)
    (hr3 : 3 ≤ r)
    (hmin : (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ)) :
    lamLargeAt ϑ k n r < (k : ℝ) ^ (sharpAddExp ϑ) := by
  exact (lamLargeAt_lt_exact ϑ k n r hn0 hk hr3 hmin).trans_le
    (Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega)
      (additiveExpAt_le_sharp ϑ r hϑ0 hϑ1 hr3))

/-- Theta-parametric balanced invocation of Konyagin's estimate. -/
lemma large_card_raw_at (ϑ : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (k : ℕ) (n : ℤ) (r : ℕ) (hk : 1 < k) (hn0 : 0 < n) (hr3 : 3 ≤ r)
    (hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ))
    (hkn : (k : ℤ) < n)
    (hub : (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + ϑ)) :
    ((badSetAt ϑ k n).card : ℝ) <
      c₆ * (k : ℝ) ^ ϑ *
        (2 * (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) +
          (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
            ((2 * (r : ℝ))⁻¹)) +
      2 * (r : ℝ) * lamLargeAt ϑ k n r := by
  set l := lamLargeAt ϑ k n r with hl
  have hT1 :
      ((n : ℝ) * (Nat.factorial r : ℝ) * l ^ r /
        (k : ℝ) ^ (r + 1)) ^ ((2 * (r : ℝ) - 1)⁻¹) =
        (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) := by
    have hbase :
        (n : ℝ) * (Nat.factorial r : ℝ) * l ^ r /
          (k : ℝ) ^ (r + 1) =
          (k : ℝ) ^ (-(E1expAt ϑ r)) := by
      have hpow :
          (n : ℝ) * (Nat.factorial r : ℝ) * l ^ r =
            (k : ℝ) ^ ((r : ℝ) + 1 - E1expAt ϑ r) := by
        rw [hl, lamLargeAt_pow ϑ k n r hn0 (by omega) (by omega)]
        rw [mul_div_cancel₀ _ (by positivity)]
      rw [hpow, div_eq_iff (by positivity)]
      rw [← Real.rpow_natCast, ← Real.rpow_add (by positivity)]
      push_cast
      ring_nf
    rw [hbase, ← Real.rpow_mul] <;> norm_num [E1expAt]
    field_simp
    exact congr_arg _ (by
      rw [neg_div', div_eq_div_iff] <;>
        nlinarith [show (r : ℝ) ≥ 3 by norm_cast,
          show (k : ℝ) ≥ 2 by norm_cast])
  have hT2 :
      ((k : ℝ) ^ ((r : ℝ) + ϑ) /
        ((n : ℝ) * (Nat.factorial r : ℝ) * l ^ r)) ^
          (((r : ℝ) - 1)⁻¹) =
        (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) := by
    have hbase :
        (k : ℝ) ^ ((r : ℝ) + ϑ) /
          ((n : ℝ) * (Nat.factorial r : ℝ) * l ^ r) =
          (k : ℝ) ^ (ϑ - 1 + E1expAt ϑ r) := by
      rw [hl, lamLargeAt_pow ϑ k n r hn0 (by omega) (by omega)]
      rw [mul_div_cancel₀ _ (by positivity)]
      rw [← Real.rpow_sub (by positivity)]
      ring_nf
    rw [hbase, ← Real.rpow_mul (by positivity)]
    congr 1
    unfold E1expAt
    rw [← div_eq_mul_inv, div_eq_div_iff] <;>
      nlinarith [show (r : ℝ) ≥ 3 by norm_cast,
        mul_div_cancel₀ ((1 - ϑ) * (2 * (r : ℝ) - 1))
          (by nlinarith [show (r : ℝ) ≥ 3 by norm_cast] :
            (3 * (r : ℝ) - 2) ≠ 0)]
  have hK := @konyagin_application
  change (((Finset.Ioo (k : ℤ) ((k : ℤ) + ⌊(k : ℝ) ^ ϑ⌋ + 2)).filter
      (fun m : ℤ => (m : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ ∧
        |(n : ℝ) / (m : ℝ) - round ((n : ℝ) / (m : ℝ))| <
          1 / (k : ℝ) ^ (1 - ϑ))).card : ℝ) < _
  convert hK l ϑ (lamLargeAt_ge_one ϑ k n r hϑ1 hn0 hk hr3 hub)
    hϑ0 hϑ1 n k r hkn (by omega) hrle using 1
  norm_num [hT1, hT2]
  exact Or.inl (by ring)

/-- A derived coarse bound used only inside the third (non-additive)
Konyagin term.  The additive term below continues to use the exact bound. -/
lemma lamLargeAt_lt_coarse (ϑ : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hϑ1 : ϑ < 1) (hn0 : 0 < n) (hk : 1 < k) (hr3 : 3 ≤ r)
    (hmin : (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ)) :
    lamLargeAt ϑ k n r < (k : ℝ) ^ ((2 - ϑ) / (r : ℝ)) := by
  refine (lamLargeAt_lt_exact ϑ k n r hn0 hk hr3 hmin).trans_le ?_
  apply Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega)
  rw [← additiveExpAt_balanced ϑ r hr3]
  have hE : 0 ≤ E1expAt ϑ r := by
    unfold E1expAt
    apply div_nonneg
    · exact mul_nonneg (sub_nonneg.mpr hϑ1.le)
        (by
          have hrR : (3 : ℝ) ≤ r := by exact_mod_cast hr3
          nlinarith)
    · have : (3 : ℝ) ≤ r := by exact_mod_cast hr3
      nlinarith
  have hrpos : (0 : ℝ) < r := by positivity
  apply (div_le_div_iff_of_pos_right hrpos).2
  linarith

lemma large_term1_le_margin_at (ϑ q : ℝ) (k r : ℕ) (hk : 1 < k)
    (hr3 : 3 ≤ r) (hlog1 : 1 < Real.log k)
    (hmargin : q * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - ϑ) * Real.log k) :
    (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) ≤
      (Real.log k) ^ (-q) := by
  have hden : 0 < 3 * (r : ℝ) - 2 := by
    have : (3 : ℝ) ≤ r := by exact_mod_cast hr3
    linarith
  rw [Real.rpow_def_of_pos (by positivity)]
  rw [show (Real.log k) ^ (-q) =
      Real.exp (Real.log (Real.log k) * (-q)) by
    rw [Real.rpow_def_of_pos (by linarith : 0 < Real.log k)]]
  apply Real.exp_le_exp.mpr
  rw [show Real.log (k : ℝ) * ((ϑ - 1) / (3 * (r : ℝ) - 2)) =
      (Real.log k * (ϑ - 1)) / (3 * (r : ℝ) - 2) by ring]
  rw [div_le_iff₀ hden]
  nlinarith

lemma large_term3_le_margin_at (ϑ q : ℝ) (hϑ1 : ϑ < 1)
    (k : ℕ) (n : ℤ) (r : ℕ) (hk : 1 < k) (hn0 : 0 < n)
    (hr4 : 4 ≤ r) (hlog1 : 1 < Real.log k)
    (hmin : (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ))
    (hrk : ((r : ℝ) + 1) ≤ (k : ℝ) ^ (ϑ / (r : ℝ)))
    (hmargin : 4 * q * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k) :
    (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
        ((2 * (r : ℝ))⁻¹) ≤ (Real.log k) ^ (-q) := by
  have hbase :
      ((r + 1 : ℝ) * lamLargeAt ϑ k n r / k) <
        (k : ℝ) ^ (2 / (r : ℝ) - 1) := by
    have hmul : ((r + 1 : ℝ) * lamLargeAt ϑ k n r) <
        (k : ℝ) ^ (2 / (r : ℝ)) := by
      refine lt_of_le_of_lt
        (mul_le_mul_of_nonneg_right hrk
          (Real.rpow_nonneg (by positivity) _)) ?_
      convert mul_lt_mul_of_pos_left
        (lamLargeAt_lt_coarse ϑ k n r hϑ1 hn0 hk (by omega) hmin)
        (Real.rpow_pos_of_pos (Nat.cast_pos.mpr hk.le) _) using 1
      rw [← Real.rpow_add (by positivity)]
      congr 1
      field_simp
      ring
    convert (div_lt_div_iff_of_pos_right (by positivity : 0 < (k : ℝ))).2 hmul using 1
    rw [Real.rpow_sub_one (by positivity)]
  refine le_trans (Real.rpow_le_rpow
    (by unfold lamLargeAt; positivity) hbase.le (by positivity)) ?_
  rw [← Real.rpow_mul (by positivity), mul_comm]
  rw [Real.rpow_def_of_pos (by positivity)]
  rw [show (Real.log k) ^ (-q) =
      Real.exp (Real.log (Real.log k) * (-q)) by
    rw [Real.rpow_def_of_pos (by linarith : 0 < Real.log k)]]
  apply Real.exp_le_exp.mpr
  field_simp
  nlinarith [show (r : ℝ) ≥ 4 by norm_cast]

lemma large_term3_r3_at (ϑ : ℝ) (hϑ1 : ϑ < 1)
    (k : ℕ) (n : ℤ) (hk : 1 < k) (hn0 : 0 < n)
    (hmin : (k : ℝ) ^ (((3 : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (3 - 1) : ℝ))
    (hrk : ((3 : ℝ) + 1) ≤ (k : ℝ) ^ (ϑ / (3 : ℝ))) :
    (((3 : ℝ) + 1) * lamLargeAt ϑ k n 3 / (k : ℝ)) ^
        ((2 * (3 : ℝ))⁻¹) ≤ (k : ℝ) ^ (-(1 : ℝ) / 18) := by
  have hbase : (((3 : ℝ) + 1) * lamLargeAt ϑ k n 3 / k) <
      (k : ℝ) ^ (2 / (3 : ℝ) - 1) := by
    have hmul : (((3 : ℝ) + 1) * lamLargeAt ϑ k n 3) <
        (k : ℝ) ^ (2 / (3 : ℝ)) := by
      calc
        ((3 : ℝ) + 1) * lamLargeAt ϑ k n 3 ≤
            (k : ℝ) ^ (ϑ / (3 : ℝ)) * lamLargeAt ϑ k n 3 :=
          mul_le_mul_of_nonneg_right hrk (by unfold lamLargeAt; positivity)
        _ < (k : ℝ) ^ (ϑ / (3 : ℝ)) *
            (k : ℝ) ^ ((2 - ϑ) / (3 : ℝ)) :=
          mul_lt_mul_of_pos_left
            (lamLargeAt_lt_coarse ϑ k n 3 hϑ1 hn0 hk (by norm_num) hmin)
            (Real.rpow_pos_of_pos (Nat.cast_pos.mpr hk.le) _)
        _ = (k : ℝ) ^ (2 / (3 : ℝ)) := by
          rw [← Real.rpow_add (by positivity)]
          congr 1
          ring
    convert (div_lt_div_iff_of_pos_right (by positivity : 0 < (k : ℝ))).2 hmul using 1
    rw [Real.rpow_sub_one (by positivity)]
  refine le_trans (Real.rpow_le_rpow
    (by unfold lamLargeAt; positivity) hbase.le (by positivity)) ?_
  rw [← Real.rpow_mul (by positivity)]
  norm_num

/-- Fully theta-parametric large-range asymptotic estimate.  Its additive
term uses `sharpAddExp`, so it remains valid below `theta=1/2`. -/
lemma large_asym_of_margins_at (ϑ q₁ q₃ C : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑ1 : ϑ < 1)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ, ∀ r : ℕ,
    3 ≤ r → 0 < n →
    (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ) →
    q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - ϑ) * Real.log k →
    ((r : ℝ) + 1) ≤ (k : ℝ) ^ (ϑ / (r : ℝ)) →
    4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k →
    (r : ℝ) ≤ Real.log k →
    1 < Real.log k →
    c₆ * (k : ℝ) ^ ϑ *
        (2 * (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) +
          (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
            ((2 * (r : ℝ))⁻¹)) +
      2 * (r : ℝ) * lamLargeAt ϑ k n r ≤
        C * (k : ℝ) ^ ϑ / Real.log k := by
  have hϑ0 : 0 < ϑ := by linarith
  obtain ⟨k₀, hk₀⟩ : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      2 * c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-q₁) +
      c₆ * (k : ℝ) ^ ϑ *
        ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) +
      2 * (k : ℝ) ^ (sharpAddExp ϑ) * Real.log k ≤
        C * (k : ℝ) ^ ϑ / Real.log k := by
    obtain ⟨k₁, hk₁⟩ := Filter.eventually_atTop.mp
      (poly_log_lt_logpow (2 * c₆) ϑ (-q₁) (by linarith)
        (C / 3) (by linarith))
    obtain ⟨k₂a, hk₂a⟩ := Filter.eventually_atTop.mp
      (poly_log_lt_logpow c₆ ϑ (-q₃) (by linarith)
        (C / 6) (by linarith))
    obtain ⟨k₂b, hk₂b⟩ := Filter.eventually_atTop.mp
      (poly_log_lt c₆ (ϑ - 1 / 18) 0 ϑ (by norm_num)
        (C / 6) (by linarith))
    obtain ⟨k₃, hk₃⟩ := Filter.eventually_atTop.mp
      (poly_log_lt (2 : ℝ) (sharpAddExp ϑ) 1 ϑ
        (sharpAddExp_lt_theta ϑ hϑlo) (C / 3) (by linarith))
    refine ⟨max k₁ (max (max k₂a (k₂b + 2)) k₃), fun k hk => ?_⟩
    have h₁ := hk₁ k (by omega)
    have h₂a := hk₂a k (by omega)
    have h₂b := hk₂b k (by omega)
    have h₃ := hk₃ k (by omega)
    rw [Real.rpow_one] at h₃
    have hkpos : (0 : ℝ) < k := by norm_cast; omega
    rw [Real.rpow_zero, mul_one] at h₂b
    have hpow : c₆ * (k : ℝ) ^ ϑ * (k : ℝ) ^ (-(1 : ℝ) / 18) =
        c₆ * (k : ℝ) ^ (ϑ - 1 / 18) := by
      rw [mul_assoc, ← Real.rpow_add hkpos]
      congr 2
      ring
    rw [mul_add, hpow]
    calc
      2 * c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-q₁) +
          (c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-q₃) +
            c₆ * (k : ℝ) ^ (ϑ - 1 / 18)) +
          2 * (k : ℝ) ^ (sharpAddExp ϑ) * Real.log k ≤
          C / 3 * (k : ℝ) ^ ϑ / Real.log k +
            C / 6 * (k : ℝ) ^ ϑ / Real.log k +
            C / 6 * (k : ℝ) ^ ϑ / Real.log k +
            C / 3 * (k : ℝ) ^ ϑ / Real.log k := by linarith
      _ = C * (k : ℝ) ^ ϑ / Real.log k := by ring
  refine ⟨k₀ + 2, fun k hk n r hr hn hmin hm₁ hrk hm₃ hrlog hlog1 => ?_⟩
  apply le_trans ?_ (hk₀ k (by omega))
  have hterm3 :
      (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
          ((2 * (r : ℝ))⁻¹) ≤
        (Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18) := by
    rcases hr.eq_or_lt with rfl | hr4
    · exact (large_term3_r3_at ϑ hϑ1 k n (by omega) hn
        (by simpa using hmin) (by exact_mod_cast hrk)).trans
          (le_add_of_nonneg_left (by positivity))
    · exact (large_term3_le_margin_at ϑ q₃ hϑ1 k n r (by omega) hn hr4
        hlog1 (by convert hmin using 1) (by exact_mod_cast hrk) hm₃).trans
          (le_add_of_nonneg_right (by positivity))
  have hterm1 := large_term1_le_margin_at ϑ q₁ k r (by omega) hr hlog1 hm₁
  have hlam := lamLargeAt_lt_sharp ϑ k n r hϑ0 hϑ1 hn (by omega) hr hmin
  have hadd : 2 * (r : ℝ) * lamLargeAt ϑ k n r ≤
      2 * (k : ℝ) ^ (sharpAddExp ϑ) * Real.log k := by
    have hrnonneg : (0 : ℝ) ≤ r := by positivity
    have hlamnonneg : 0 ≤ lamLargeAt ϑ k n r := by unfold lamLargeAt; positivity
    nlinarith [mul_le_mul_of_nonneg_left hlam.le hrnonneg,
      mul_le_mul_of_nonneg_right hrlog hlamnonneg]
  have hbracket :
      2 * (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) +
          (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
            ((2 * (r : ℝ))⁻¹) ≤
        2 * (Real.log k) ^ (-q₁) +
          ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) :=
    add_le_add (mul_le_mul_of_nonneg_left hterm1 zero_le_two) hterm3
  calc
    c₆ * (k : ℝ) ^ ϑ *
          (2 * (k : ℝ) ^ ((ϑ - 1) / (3 * (r : ℝ) - 2)) +
            (((r : ℝ) + 1) * lamLargeAt ϑ k n r / (k : ℝ)) ^
              ((2 * (r : ℝ))⁻¹)) +
        2 * (r : ℝ) * lamLargeAt ϑ k n r ≤
      c₆ * (k : ℝ) ^ ϑ *
          (2 * (Real.log k) ^ (-q₁) +
            ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18))) +
        2 * (k : ℝ) ^ (sharpAddExp ϑ) * Real.log k :=
      add_le_add
        (mul_le_mul_of_nonneg_left hbracket
          (mul_nonneg c₆_pos.le (Real.rpow_nonneg (Nat.cast_nonneg _) _))) hadd
    _ = 2 * c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-q₁) +
        c₆ * (k : ℝ) ^ ϑ *
          ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) +
        2 * (k : ℝ) ^ (sharpAddExp ϑ) * Real.log k := by ring

lemma eventually_log_le_half_rpow_at (ϑ : ℝ) (hϑ1 : ϑ < 1) :
    ∀ᶠ k : ℕ in Filter.atTop,
      Real.log k ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) := by
  have hsmall := isLittleO_log_rpow_atTop (sub_pos.mpr hϑ1)
  rw [Asymptotics.isLittleO_iff] at hsmall
  obtain ⟨x₀, hx₀⟩ := Filter.eventually_atTop.mp
    (hsmall (show (0 : ℝ) < 1 / 2 by norm_num))
  refine Filter.eventually_atTop.mpr ⟨⌈x₀⌉₊ + 2, fun k hk => ?_⟩
  have hxk : x₀ ≤ (k : ℝ) := by
    exact (Nat.le_ceil x₀).trans (by exact_mod_cast (show ⌈x₀⌉₊ ≤ k by omega))
  have h := hx₀ k hxk
  rw [Real.norm_of_nonneg (Real.log_nonneg (by norm_cast; omega)),
    Real.norm_of_nonneg (Real.rpow_nonneg (Nat.cast_nonneg _) _)] at h
  exact h

/-- Variable-theta reference-order geometry and logarithmic margins. -/
lemma r0Param_eventual_bounds_at (ϑ a b q₁ q₃ : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (ha : 0 < a) (hab : a < b)
    (hbϑ : b < ϑ) (hm₁ : 3 * q₁ * b < 1 - ϑ)
    (hm₃ : 4 * q₃ * b < 1) (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) :
    ∀ᶠ k : ℕ in Filter.atTop,
      1 ≤ r0Param a k ∧
      (r0Param a k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) ∧
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - ϑ) * Real.log k ∧
      ((r0Param a k : ℝ) + 1) ≤
        (k : ℝ) ^ (ϑ / (r0Param a k : ℝ)) ∧
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) ≤ Real.log k ∧
      (r0Param a k : ℝ) ≤ Real.log k ∧
      1 < Real.log k := by
  have hb0 : 0 < b := ha.trans hab
  have hb1 : b < 1 := hbϑ.trans hϑ1
  have hsand := r0Param_sandwich a b ha hab
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop
      (max 1 b)
  have hL := (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop
    (max 2 (1 / (1 - b)))
  filter_upwards [hsand, hM, hL, eventually_log_le_half_rpow_at ϑ hϑ1]
    with k hkR hkM hkL hkpow
  change max 1 b ≤ Real.log (Real.log k) at hkM
  change max 2 (1 / (1 - b)) ≤ Real.log k at hkL
  rcases hkR with ⟨hR1, hRa, hRb⟩
  have hL2 : 2 ≤ Real.log k := le_trans (le_max_left _ _) hkL
  have hLpos : 0 < Real.log k := by linarith
  have hM1 : 1 ≤ Real.log (Real.log k) := le_trans (le_max_left _ _) hkM
  have hbM : b ≤ Real.log (Real.log k) := le_trans (le_max_right _ _) hkM
  have hMpos : 0 < Real.log (Real.log k) := by linarith
  have hXnonneg : 0 ≤ Real.log k / Real.log (Real.log k) := by positivity
  have hXleL : Real.log k / Real.log (Real.log k) ≤ Real.log k := by
    rw [div_le_iff₀ hMpos]
    nlinarith
  have hRleX : (r0Param a k : ℝ) ≤
      Real.log k / Real.log (Real.log k) := by
    have hRb' : (r0Param a k : ℝ) ≤
        b * (Real.log k / Real.log (Real.log k)) := by
      convert hRb using 1 <;> ring
    calc
      (r0Param a k : ℝ) ≤ b * (Real.log k / Real.log (Real.log k)) := hRb'
      _ ≤ 1 * (Real.log k / Real.log (Real.log k)) :=
        mul_le_mul_of_nonneg_right hb1.le hXnonneg
      _ = Real.log k / Real.log (Real.log k) := by ring
  have hRlog : (r0Param a k : ℝ) ≤ Real.log k := hRleX.trans hXleL
  have hRpow : (r0Param a k : ℝ) ≤
      (1 / 2) * (k : ℝ) ^ (1 - ϑ) := hRlog.trans hkpow
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    calc
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
          (b * Real.log k / Real.log (Real.log k)) * Real.log (Real.log k) :=
        mul_le_mul_of_nonneg_right hRb hMpos.le
      _ = b * Real.log k := by field_simp
  have hmargin1 :
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - ϑ) * Real.log k := by
    have hthree : (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        3 * ((r0Param a k : ℝ) * Real.log (Real.log k)) := by nlinarith
    calc
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) =
          q₁ * ((3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k)) := by ring
      _ ≤ q₁ * (3 * ((r0Param a k : ℝ) * Real.log (Real.log k))) :=
        mul_le_mul_of_nonneg_left hthree (by linarith)
      _ ≤ q₁ * (3 * (b * Real.log k)) :=
        mul_le_mul_of_nonneg_left
          (mul_le_mul_of_nonneg_left hRM (by norm_num)) (by linarith)
      _ = (3 * q₁ * b) * Real.log k := by ring
      _ ≤ (1 - ϑ) * Real.log k :=
        mul_le_mul_of_nonneg_right hm₁.le hLpos.le
  have hmargin3 :
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) ≤ Real.log k := by
    calc
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) =
          (4 * q₃) * ((r0Param a k : ℝ) * Real.log (Real.log k)) := by ring
      _ ≤ (4 * q₃) * (b * Real.log k) :=
        mul_le_mul_of_nonneg_left hRM (by positivity)
      _ = (4 * q₃ * b) * Real.log k := by ring
      _ ≤ 1 * Real.log k := mul_le_mul_of_nonneg_right hm₃.le hLpos.le
      _ = Real.log k := by ring
  have hRplus : (r0Param a k : ℝ) + 1 ≤ Real.log k := by
    have hRb' : (r0Param a k : ℝ) ≤
        b * (Real.log k / Real.log (Real.log k)) := by
      convert hRb using 1 <;> ring
    have hRbL : (r0Param a k : ℝ) ≤ b * Real.log k :=
      hRb'.trans (mul_le_mul_of_nonneg_left hXleL hb0.le)
    have hbig : 1 / (1 - b) ≤ Real.log k := le_trans (le_max_right _ _) hkL
    rw [div_le_iff₀ (sub_pos.mpr hb1)] at hbig
    nlinarith
  have hRpos : (0 : ℝ) < r0Param a k := by exact_mod_cast (show 0 < r0Param a k by omega)
  have harg : Real.log (Real.log k) ≤
      ϑ * Real.log k / (r0Param a k : ℝ) := by
    apply (le_div_iff₀ hRpos).2
    calc
      Real.log (Real.log k) * (r0Param a k : ℝ) =
          (r0Param a k : ℝ) * Real.log (Real.log k) := by ring
      _ ≤ b * Real.log k := hRM
      _ ≤ ϑ * Real.log k :=
        mul_le_mul_of_nonneg_right hbϑ.le hLpos.le
  have hLrpow : Real.log k ≤
      (k : ℝ) ^ (ϑ / (r0Param a k : ℝ)) := by
    have hkpos : (0 : ℝ) < k := by
      by_contra h
      have hkzero : (k : ℝ) = 0 := le_antisymm (le_of_not_gt h) (Nat.cast_nonneg k)
      rw [hkzero, Real.log_zero] at hLpos
      linarith
    calc
      Real.log k = Real.exp (Real.log (Real.log k)) := by rw [Real.exp_log hLpos]
      _ ≤ Real.exp (ϑ * Real.log k / (r0Param a k : ℝ)) :=
        Real.exp_le_exp.mpr harg
      _ = (k : ℝ) ^ (ϑ / (r0Param a k : ℝ)) := by
        rw [Real.rpow_def_of_pos hkpos]
        congr 1
        ring
  exact ⟨hR1, hRpow, hmargin1, hRplus.trans hLrpow, hmargin3,
    hRlog, by linarith⟩

/-- The reference order absorbs `exp(c log²/loglog)` and its factorial,
uniformly in theta once theta is positive. -/
lemma r0Param_eventual_admissible_at (ϑ c a b : ℝ) (hϑ0 : 0 < ϑ)
    (ha : 0 < a) (hca : c < a) (hab : a < b) :
    ∀ᶠ k : ℕ in Filter.atTop, ∀ n : ℤ, 0 < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      (n : ℝ) * (Nat.factorial (r0Param a k) : ℝ) ≤
        (k : ℝ) ^ ((r0Param a k : ℝ) + ϑ) := by
  have hac : 0 < a - c := sub_pos.mpr hca
  have hsand := r0Param_sandwich a b ha hab
  have hX := tendsto_log_div_loglog_atTop.eventually_ge_atTop (b / (a - c))
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop
      (max 1 b)
  have hL := (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop 2
  filter_upwards [hsand, hX, hM, hL] with k hkR hkX hkM hkL
  change max 1 b ≤ Real.log (Real.log k) at hkM
  change 2 ≤ Real.log k at hkL
  intro n hn hupper
  rcases hkR with ⟨hR1, hRa, hRb⟩
  have hLpos : 0 < Real.log k := by linarith
  have hbM : b ≤ Real.log (Real.log k) := le_trans (le_max_right _ _) hkM
  have hMpos : 0 < Real.log (Real.log k) := by
    linarith [le_trans (le_max_left _ _) hkM]
  have hb0 : 0 < b := ha.trans hab
  have hratio : b * Real.log k / Real.log (Real.log k) ≤ Real.log k := by
    rw [div_le_iff₀ hMpos]
    simpa [mul_comm] using mul_le_mul_of_nonneg_left hbM hLpos.le
  have hRlog : (r0Param a k : ℝ) ≤ Real.log k := hRb.trans hratio
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    calc
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
          (b * Real.log k / Real.log (Real.log k)) * Real.log (Real.log k) :=
        mul_le_mul_of_nonneg_right hRb hMpos.le
      _ = b * Real.log k := by field_simp
  have hgap0 : b ≤ (a - c) *
      (Real.log k / Real.log (Real.log k)) := by
    rw [div_le_iff₀ hac] at hkX
    nlinarith
  have hgap : b * Real.log k ≤
      (a - c) * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by
    have hh := mul_le_mul_of_nonneg_right hgap0 hLpos.le
    calc
      b * Real.log k ≤
          ((a - c) * (Real.log k / Real.log (Real.log k))) * Real.log k := hh
      _ = (a - c) * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by ring
  have haR : a * ((Real.log k) ^ 2 / Real.log (Real.log k)) ≤
      (r0Param a k : ℝ) * Real.log k := by
    have hh := mul_le_mul_of_nonneg_right hRa hLpos.le
    calc
      a * ((Real.log k) ^ 2 / Real.log (Real.log k)) =
          (a * Real.log k / Real.log (Real.log k)) * Real.log k := by ring
      _ ≤ (r0Param a k : ℝ) * Real.log k := hh
  have hbudget : c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
        (r0Param a k : ℝ) * Real.log k := by
    calc
      c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
          (r0Param a k : ℝ) * Real.log (Real.log k) ≤
        c * ((Real.log k) ^ 2 / Real.log (Real.log k)) + b * Real.log k :=
          by nlinarith [hRM]
      _ ≤ a * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by nlinarith
      _ ≤ (r0Param a k : ℝ) * Real.log k := haR
  have hlogn : Real.log (n : ℝ) ≤
      c * (Real.log k) ^ 2 / Real.log (Real.log k) :=
    Real.log_le_iff_le_exp (by positivity) |>.2 hupper
  have hlogR : Real.log (r0Param a k : ℝ) ≤ Real.log (Real.log k) := by
    gcongr
  have hfac : Real.log (Nat.factorial (r0Param a k) : ℝ) ≤
      (r0Param a k : ℝ) * Real.log (Real.log k) := by
    calc
      Real.log (Nat.factorial (r0Param a k) : ℝ) ≤
          (r0Param a k : ℝ) * Real.log (r0Param a k) := by
        rw [← Real.log_pow]
        gcongr
        norm_cast
        exact Nat.recOn (r0Param a k) (by norm_num) fun m ihm => by
          rw [Nat.factorial_succ, pow_succ']
          exact (Nat.mul_le_mul_left _ ihm).trans (by gcongr; omega)
      _ ≤ (r0Param a k : ℝ) * Real.log (Real.log k) :=
        mul_le_mul_of_nonneg_left hlogR (by positivity)
  have hlogs : Real.log (n : ℝ) +
      Real.log (Nat.factorial (r0Param a k) : ℝ) ≤
        (r0Param a k : ℝ) * Real.log k + ϑ * Real.log k := by
    calc
      Real.log (n : ℝ) + Real.log (Nat.factorial (r0Param a k) : ℝ) ≤
          c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
            (r0Param a k : ℝ) * Real.log (Real.log k) := by
              apply add_le_add _ hfac
              simpa [div_eq_mul_inv, mul_assoc] using hlogn
      _ ≤ (r0Param a k : ℝ) * Real.log k := hbudget
      _ ≤ (r0Param a k : ℝ) * Real.log k + ϑ * Real.log k :=
        le_add_of_nonneg_right (mul_nonneg hϑ0.le hLpos.le)
  rw [← Real.log_le_log_iff (by positivity)
    (Real.rpow_pos_of_pos (by
      by_contra h
      have hkzero : (k : ℝ) = 0 :=
        le_antisymm (le_of_not_gt h) (Nat.cast_nonneg k)
      rw [hkzero, Real.log_zero] at hLpos
      linarith) _),
    Real.log_mul (by positivity) (by positivity),
    Real.log_rpow (by
      by_contra h
      have hkzero : (k : ℝ) = 0 :=
        le_antisymm (le_of_not_gt h) (Nat.cast_nonneg k)
      rw [hkzero, Real.log_zero] at hLpos
      linarith)]
  convert hlogs using 1 <;> ring

def HasLargeMarginCertificateAt (ϑ c q₁ q₃ : ℝ) : Prop :=
  ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
    (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
    ∃ r : ℕ,
      3 ≤ r ∧
      (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) ∧
      (n : ℝ) * (Nat.factorial r : ℝ) ≤ (k : ℝ) ^ ((r : ℝ) + ϑ) ∧
      (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
        (n : ℝ) * (Nat.factorial (r - 1) : ℝ) ∧
      q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - ϑ) * Real.log k ∧
      ((r : ℝ) + 1) ≤ (k : ℝ) ^ (ϑ / (r : ℝ)) ∧
      4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k ∧
      (r : ℝ) ≤ Real.log k ∧
      1 < Real.log k

lemma hasLargeMarginCertificateAt_of_parameters (ϑ c a b q₁ q₃ : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (ha : 0 < a) (hca : c < a) (hab : a < b) (hbϑ : b < ϑ)
    (hm₁ : 3 * q₁ * b < 1 - ϑ) (hm₃ : 4 * q₃ * b < 1)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) :
    HasLargeMarginCertificateAt ϑ c q₁ q₃ := by
  obtain ⟨kb, hb⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_bounds_at ϑ a b q₁ q₃ hϑ0 hϑ1 ha hab hbϑ hm₁ hm₃ hq₁ hq₃)
  obtain ⟨kp, hp⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_admissible_at ϑ c a b hϑ0 ha hca hab)
  refine ⟨max (max kb kp) 2, ?_⟩
  intro k hk n hlow hupper
  have hkb : kb ≤ k := by omega
  have hkp : kp ≤ k := by omega
  have hk2 : 2 ≤ k := by omega
  have hkpos : (0 : ℝ) < k := by norm_cast; omega
  have hn0 : 0 < n := by
    have hpow0 : (0 : ℝ) ≤ (k : ℝ) ^ (2 + ϑ) := by positivity
    have : (0 : ℝ) < (n : ℝ) := lt_of_le_of_lt (by positivity) hlow
    exact_mod_cast this
  have hP0 : (n : ℝ) * (Nat.factorial (r0Param a k) : ℝ) ≤
      (k : ℝ) ^ ((r0Param a k : ℝ) + ϑ) := hp k hkp n hn0 hupper
  let hExists : ∃ r : ℕ, (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + ϑ) := ⟨r0Param a k, hP0⟩
  let r : ℕ := Nat.find hExists
  have hrle0 : r ≤ r0Param a k := Nat.find_min' hExists hP0
  have hspec : (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + ϑ) := Nat.find_spec hExists
  have hb0 := hb k hkb
  have hr3 : 3 ≤ r := by
    by_contra hrnot
    have hr : r < 3 := Nat.lt_of_not_ge hrnot
    have hcases : r = 0 ∨ r = 1 ∨ r = 2 := by omega
    rcases hcases with h0 | h1 | h2
    · rw [h0] at hspec
      norm_num at hspec
      have hfactor : (k : ℝ) ^ (2 + ϑ) =
          (k : ℝ) ^ ϑ * (k : ℝ) ^ 2 := by
        rw [show (2 + ϑ : ℝ) = ϑ + 2 by ring, Real.rpow_add hkpos]
        norm_num
      rw [hfactor] at hlow
      have hkpow2 : (2 : ℝ) ≤ (k : ℝ) ^ 2 := by
        have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk2
        nlinarith [sq_nonneg ((k : ℝ) - 2)]
      have hprod : 0 ≤ (k : ℝ) ^ ϑ * ((k : ℝ) ^ 2 - 2) :=
        mul_nonneg (Real.rpow_nonneg (Nat.cast_nonneg k) _) (sub_nonneg.mpr hkpow2)
      nlinarith
    · rw [h1] at hspec
      norm_num at hspec
      have hfactor : (k : ℝ) ^ (2 + ϑ) =
          (k : ℝ) ^ (1 + ϑ) * (k : ℝ) := by
        rw [show (2 + ϑ : ℝ) = (1 + ϑ) + 1 by ring,
          Real.rpow_add hkpos]
        norm_num
      rw [hfactor] at hlow
      have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk2
      have hprod : 0 ≤ (k : ℝ) ^ (1 + ϑ) * ((k : ℝ) - 2) :=
        mul_nonneg (Real.rpow_nonneg (Nat.cast_nonneg k) _) (sub_nonneg.mpr hkR)
      nlinarith
    · rw [h2] at hspec
      norm_num at hspec
      nlinarith
  have hrpos : (0 : ℝ) < r := by exact_mod_cast (show 0 < r by omega)
  have hmin : (k : ℝ) ^ (((r : ℝ) - 1) + ϑ) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ) := by
    have hrsub : r - 1 < r := Nat.sub_lt (by omega) zero_lt_one
    have hnot := Nat.find_min hExists hrsub
    push_neg at hnot
    convert hnot using 2
    rw [Nat.cast_sub (by omega)]
    norm_num
  have hrcast : (r : ℝ) ≤ (r0Param a k : ℝ) := by exact_mod_cast hrle0
  have hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) :=
    hrcast.trans hb0.2.1
  have hmargin1 : q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - ϑ) * Real.log k := by
    have hMnonneg : 0 ≤ Real.log (Real.log k) :=
      (Real.log_pos hb0.2.2.2.2.2.2).le
    have hbase : 3 * (r : ℝ) - 2 ≤ 3 * (r0Param a k : ℝ) - 2 := by
      nlinarith
    exact (mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hbase (le_trans zero_le_one hq₁.le)) hMnonneg).trans
        hb0.2.2.1
  have hrk : (r : ℝ) + 1 ≤ (k : ℝ) ^ (ϑ / (r : ℝ)) := by
    calc
      (r : ℝ) + 1 ≤ (r0Param a k : ℝ) + 1 := by linarith
      _ ≤ (k : ℝ) ^ (ϑ / (r0Param a k : ℝ)) := hb0.2.2.2.1
      _ ≤ (k : ℝ) ^ (ϑ / (r : ℝ)) := by
        apply Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega)
        exact div_le_div_of_nonneg_left hϑ0.le hrpos hrcast
  have hmargin3 : 4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k := by
    have hMnonneg : 0 ≤ Real.log (Real.log k) :=
      (Real.log_pos hb0.2.2.2.2.2.2).le
    exact (mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hrcast (by positivity)) hMnonneg).trans
        hb0.2.2.2.2.1
  have hrlog : (r : ℝ) ≤ Real.log k := hrcast.trans hb0.2.2.2.2.2.1
  exact ⟨r, hr3, hrle, hspec, hmin, hmargin1, hrk, hmargin3,
    hrlog, hb0.2.2.2.2.2.2⟩

lemma case_large_of_margin_certificate_at (ϑ c q₁ q₃ : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑ1 : ϑ < 1)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) (hPI : PrimeIntervalInput ϑ)
    (hcert : HasLargeMarginCertificateAt ϑ c q₁ q₃) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      SourceIntervalConclusion ϑ k n := by
  have hϑ0 : 0 < ϑ := by linarith
  obtain ⟨C, hC, kb, hb⟩ := hPI
  obtain ⟨ka, hasym⟩ :=
    large_asym_of_margins_at ϑ q₁ q₃ C hϑlo hϑ1 hq₁ hq₃ hC
  obtain ⟨kr, hrdata⟩ := hcert
  refine ⟨max (max kb ka) (max kr 2), ?_⟩
  intro k hk n hlow hhigh
  have hkb : kb ≤ k := by omega
  have hka : ka ≤ k := by omega
  have hkr : kr ≤ k := by omega
  have hk2 : 2 ≤ k := by omega
  have hk1 : 1 ≤ k := by omega
  have hk1' : 1 < k := by omega
  have hkR : (1 : ℝ) < (k : ℝ) := by exact_mod_cast hk1'
  have hkpow : (k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ) := by
    have hpowe : (k : ℝ) ^ (2 + ϑ) =
        (k : ℝ) ^ 2 * (k : ℝ) ^ ϑ := by
      rw [show (2 + ϑ : ℝ) = (2 : ℕ) + ϑ by norm_num,
        Real.rpow_add (by linarith), Real.rpow_natCast]
    have hone : (1 : ℝ) ≤ (k : ℝ) ^ ϑ :=
      Real.one_le_rpow hkR.le hϑ0.le
    rw [hpowe]
    have hk2R : (2 : ℝ) ≤ k := by exact_mod_cast hk2
    nlinarith [mul_nonneg (sq_nonneg (k : ℝ))
      (by linarith : (0 : ℝ) ≤ (k : ℝ) ^ ϑ - 1)]
  have hknR : (k : ℝ) < (n : ℝ) := lt_of_le_of_lt hkpow hlow
  have hkn : (k : ℤ) < n := by exact_mod_cast hknR
  have hn0 : 0 < n := lt_trans (by exact_mod_cast hk1) hkn
  obtain ⟨r, hr3, hrle, hub, hmin, hm₁, hrk, hm₃, hrlog, hlog1⟩ :=
    hrdata k hkr n hlow hhigh
  have hraw := large_card_raw_at ϑ hϑ0 hϑ1 k n r hk1' hn0 hr3 hrle hkn hub
  have hbnd := hasym k hka n r hr3 hn0 hmin hm₁ hrk hm₃ hrlog hlog1
  have hprime : C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ) := hb k hkb
  exact konyagin_finish_at ϑ hϑ0.le k n hk1 C hprime
    (lt_of_lt_of_le hraw hbnd)

lemma rangePackage_of_parameters (ϑ c a b q₁ q₃ : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑ1 : ϑ < 1)
    (ha : 0 < a) (hca : c < a) (hab : a < b) (hbϑ : b < ϑ)
    (hm₁ : 3 * q₁ * b < 1 - ϑ) (hm₃ : 4 * q₃ * b < 1)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) (hPI : PrimeIntervalInput ϑ) :
    ParametricRangePackage ϑ c := by
  have hϑ0 : 0 < ϑ := by linarith
  refine ⟨ParametricSmall.case_small ϑ hϑ0 hϑ1 hPI,
    ParametricMed.case_medium ϑ hϑ0 hϑ1 hPI,
    ParametricML.case_mediumlarge ϑ hϑ0 hϑ1 hPI, ?_⟩
  exact case_large_of_margin_certificate_at ϑ c q₁ q₃ hϑlo hϑ1 hq₁ hq₃ hPI
    (hasLargeMarginCertificateAt_of_parameters ϑ c a b q₁ q₃
      hϑ0 hϑ1 ha hca hab hbϑ hm₁ hm₃ hq₁ hq₃)

/-- Widest strict parameter-feasibility interval needed by the four-range
builder.  The former upper cutoff `3/5` played no role beyond implying
`theta<1`. -/
lemma exists_frontier_parameters_wide (ϑ c : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑhi : ϑ < 1)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    ∃ a b q₁ q₃ : ℝ,
      0 < a ∧ c < a ∧ a < b ∧ b < ϑ ∧
      1 < q₁ ∧ 3 * q₁ * b < 1 - ϑ ∧
      1 < q₃ ∧ 4 * q₃ * b < 1 := by
  let f : ℝ := (1 - ϑ) / 3
  let a : ℝ := (c + f) / 2
  let b : ℝ := (a + f) / 2
  have hfpos : 0 < f := by dsimp [f]; nlinarith
  have hcf : c < f := by simpa [f] using hcfront
  have ha : 0 < a := by dsimp [a]; nlinarith
  have hca : c < a := by dsimp [a]; nlinarith
  have haf : a < f := by dsimp [a]; nlinarith
  have hab : a < b := by
    dsimp [b]
    rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 2)]
    linarith
  have hbf : b < f := by
    dsimp [b]
    rw [div_lt_iff₀ (by norm_num : (0 : ℝ) < 2)]
    linarith
  have hb0 : 0 < b := ha.trans hab
  have hfϑ : f < ϑ := by dsimp [f]; nlinarith
  have hbϑ : b < ϑ := hbf.trans hfϑ
  have hthree : 3 * b < 1 - ϑ := by
    have : 3 * f = 1 - ϑ := by dsimp [f]; ring
    nlinarith
  have hfourf : 4 * f < 1 := by dsimp [f]; nlinarith
  have hfour : 4 * b < 1 := by nlinarith
  have hratio1 : 1 < (1 - ϑ) / (3 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa [mul_assoc] using hthree
  obtain ⟨q₁, hq₁, hq₁u⟩ := exists_between hratio1
  have hm₁ : 3 * q₁ * b < 1 - ϑ := by
    have hh := (lt_div_iff₀ (by positivity : 0 < 3 * b)).1 hq₁u
    nlinarith
  have hratio3 : 1 < 1 / (4 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa using hfour
  obtain ⟨q₃, hq₃, hq₃u⟩ := exists_between hratio3
  have hm₃ : 4 * q₃ * b < 1 := by
    have hh := (lt_div_iff₀ (by positivity : 0 < 4 * b)).1 hq₃u
    nlinarith
  exact ⟨a, b, q₁, q₃, ha, hca, hab, hbϑ, hq₁, hm₁, hq₃, hm₃⟩

/-- Exact feasibility predicate for the balanced four-range parameter class:
the sharp `r=3` additive gap together with the `a,b,q₁,q₃` margin
system used by the least-order proof. -/
def BalancedFourRangeParameters (ϑ c : ℝ) : Prop :=
  BalancedLargeExponentFeasible ϑ ∧
  ∃ a b q₁ q₃ : ℝ,
    0 < a ∧ c < a ∧ a < b ∧ b < ϑ ∧
    1 < q₁ ∧ 3 * q₁ * b < 1 - ϑ ∧
    1 < q₃ ∧ 4 * q₃ * b < 1

/-- Exact endpoint certificate for this accurately delimited method class. -/
theorem balancedFourRangeParameters_iff (ϑ c : ℝ) (hc : 0 < c) :
    BalancedFourRangeParameters ϑ c ↔
      (9 : ℝ) / 23 < ϑ ∧ ϑ < 1 ∧ c < (1 - ϑ) / 3 := by
  constructor
  · rintro ⟨hexp, a, b, q₁, q₃, ha, hca, hab, hbϑ, hq₁, hm₁, hq₃, hm₃⟩
    have hlo : (9 : ℝ) / 23 < ϑ :=
      (balancedLargeExponentFeasible_iff ϑ).1 hexp
    have hb0 : 0 < b := lt_trans hc (hca.trans hab)
    have hq₁0 : 0 < q₁ := by linarith
    have hterm : 0 < 3 * q₁ * b := mul_pos (mul_pos (by norm_num) hq₁0) hb0
    have hhi : ϑ < 1 := by linarith
    have hbq : 3 * b < 3 * q₁ * b := by
      have := mul_lt_mul_of_pos_right hq₁ hb0
      nlinarith
    have hfront : c < (1 - ϑ) / 3 := by
      rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 3)]
      nlinarith
    exact ⟨hlo, hhi, hfront⟩
  · rintro ⟨hlo, hhi, hfront⟩
    refine ⟨(balancedLargeExponentFeasible_iff ϑ).2 hlo, ?_⟩
    exact exists_frontier_parameters_wide ϑ c hlo hhi hc hfront

lemma balancedFourRange_no_go_low (ϑ c : ℝ) (hc : 0 < c)
    (hϑ : ϑ ≤ (9 : ℝ) / 23) : ¬ BalancedFourRangeParameters ϑ c := by
  rw [balancedFourRangeParameters_iff ϑ c hc]
  exact fun h => (not_lt_of_ge hϑ) h.1

lemma balancedFourRange_no_go_high (ϑ c : ℝ) (hc : 0 < c)
    (hϑ : 1 ≤ ϑ) : ¬ BalancedFourRangeParameters ϑ c := by
  rw [balancedFourRangeParameters_iff ϑ c hc]
  exact fun h => (not_lt_of_ge hϑ) h.2.1

/-! ## Adaptive unbalanced logarithmic parameter core

These definitions encode the logarithms of

`U_r = k^(r+1) L^(-Q(2r-1))`,
`V_r = k^(r+ϑ) L^(Q(r-1))`, and `Z=max(nr!,V_r)`.

They isolate the parameter algebra from the analytic Konyagin invocation,
whose existing wrapper above is specialized to the balanced scale. -/

/-- The upstream Konyagin estimate exposed with arbitrary real `lambda>=1`
and the sharp admissible order `r>=2`.  Unlike `large_card_raw_at`, this
wrapper makes no balanced-scale or `nr!<=k^(r+theta)` assumption. -/
lemma large_card_raw_adaptive_at (ϑ lam : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hlam : 1 ≤ lam)
    (k : ℕ) (n : ℤ) (r : ℕ) (hkn : (k : ℤ) < n) (hr2 : 2 ≤ r)
    (hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ)) :
    ((badSetAt ϑ k n).card : ℝ) <
      c₆ * (k : ℝ) ^ ϑ *
        (((n : ℝ) * (Nat.factorial r : ℝ) * lam ^ r /
              (k : ℝ) ^ (r + 1)) ^ ((2 * (r : ℝ) - 1)⁻¹) +
          ((k : ℝ) ^ ((r : ℝ) + ϑ) /
              ((n : ℝ) * (Nat.factorial r : ℝ) * lam ^ r)) ^
            (((r : ℝ) - 1)⁻¹) +
          (((r : ℝ) + 1) * lam / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹)) +
        2 * (r : ℝ) * lam := by
  exact konyagin_application lam ϑ hlam hϑ0 hϑ1 n k r hkn hr2 hrle

/-- Actual adaptive upper stopping scale
`U_r=k^(r+1) log(k)^(-Q(2r-1))`. -/
def adaptiveUAt (Q : ℝ) (k r : ℕ) : ℝ :=
  (k : ℝ) ^ ((r : ℝ) + 1) *
    (Real.log k) ^ (-Q * (2 * (r : ℝ) - 1))

/-- Actual adaptive lower balancing scale
`V_r=k^(r+theta) log(k)^(Q(r-1))`. -/
def adaptiveVAt (ϑ Q : ℝ) (k r : ℕ) : ℝ :=
  (k : ℝ) ^ ((r : ℝ) + ϑ) *
    (Real.log k) ^ (Q * ((r : ℝ) - 1))

/-- The selected powered numerator `Z=max(n r!,V_r)`. -/
def adaptiveZAt (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  max ((n : ℝ) * (Nat.factorial r : ℝ)) (adaptiveVAt ϑ Q k r)

/-- The positive real adaptive Konyagin scale satisfying
`lambda^r=Z/(n r!)`. -/
def adaptiveLambdaAt (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  (adaptiveZAt ϑ Q k n r /
      ((n : ℝ) * (Nat.factorial r : ℝ))) ^ ((r : ℝ)⁻¹)

def adaptiveT1At (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  (adaptiveZAt ϑ Q k n r / (k : ℝ) ^ ((r : ℝ) + 1)) ^
    ((2 * (r : ℝ) - 1)⁻¹)

def adaptiveT2At (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  ((k : ℝ) ^ ((r : ℝ) + ϑ) / adaptiveZAt ϑ Q k n r) ^
    (((r : ℝ) - 1)⁻¹)

def adaptiveT3At (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) : ℝ :=
  (((r : ℝ) + 1) * adaptiveLambdaAt ϑ Q k n r / (k : ℝ)) ^
    ((2 * (r : ℝ))⁻¹)

lemma adaptiveUAt_pos (Q : ℝ) (k r : ℕ) (hk : 1 < k) :
    0 < adaptiveUAt Q k r := by
  unfold adaptiveUAt
  exact mul_pos (Real.rpow_pos_of_pos (by positivity) _)
    (Real.rpow_pos_of_pos (Real.log_pos (by exact_mod_cast hk)) _)

lemma adaptiveVAt_pos (ϑ Q : ℝ) (k r : ℕ) (hk : 1 < k) :
    0 < adaptiveVAt ϑ Q k r := by
  unfold adaptiveVAt
  exact mul_pos (Real.rpow_pos_of_pos (by positivity) _)
    (Real.rpow_pos_of_pos (Real.log_pos (by exact_mod_cast hk)) _)

lemma adaptiveZAt_pos (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) : 0 < adaptiveZAt ϑ Q k n r := by
  exact (adaptiveVAt_pos ϑ Q k r hk).trans_le (le_max_right _ _)

lemma adaptiveLambdaAt_pow (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) (hn : 0 < n) (hr : 1 ≤ r) :
    (adaptiveLambdaAt ϑ Q k n r) ^ r =
      adaptiveZAt ϑ Q k n r /
        ((n : ℝ) * (Nat.factorial r : ℝ)) := by
  have hbase : 0 < adaptiveZAt ϑ Q k n r /
      ((n : ℝ) * (Nat.factorial r : ℝ)) := by
    exact div_pos (adaptiveZAt_pos ϑ Q k n r hk) (by positivity)
  unfold adaptiveLambdaAt
  rw [← Real.rpow_natCast, ← Real.rpow_mul hbase.le]
  norm_num [show r ≠ 0 by omega]

lemma adaptiveLambdaAt_ge_one (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hn : 0 < n) (hr : 1 ≤ r) :
    1 ≤ adaptiveLambdaAt ϑ Q k n r := by
  unfold adaptiveLambdaAt
  refine Real.one_le_rpow ?_ (by positivity)
  rw [one_le_div (by positivity)]
  exact le_max_left _ _

lemma adaptive_mass_mul_lambda_pow (ϑ Q : ℝ)
    (k : ℕ) (n : ℤ) (r : ℕ) (hk : 1 < k) (hn : 0 < n)
    (hr : 1 ≤ r) :
    (n : ℝ) * (Nat.factorial r : ℝ) *
        (adaptiveLambdaAt ϑ Q k n r) ^ r =
      adaptiveZAt ϑ Q k n r := by
  rw [adaptiveLambdaAt_pow ϑ Q k n r hk hn hr]
  field_simp

def adaptiveLogU (Q K M : ℝ) (r : ℕ) : ℝ :=
  ((r : ℝ) + 1) * K - Q * (2 * (r : ℝ) - 1) * M

def adaptiveLogV (ϑ Q K M : ℝ) (r : ℕ) : ℝ :=
  ((r : ℝ) + ϑ) * K + Q * ((r : ℝ) - 1) * M

def adaptiveLogZ (ϑ Q K M logN : ℝ) (r : ℕ) : ℝ :=
  max logN (adaptiveLogV ϑ Q K M r)

def adaptiveLogT1 (ϑ Q K M logN : ℝ) (r : ℕ) : ℝ :=
  (adaptiveLogZ ϑ Q K M logN r - ((r : ℝ) + 1) * K) /
    (2 * (r : ℝ) - 1)

def adaptiveLogT2 (ϑ Q K M logN : ℝ) (r : ℕ) : ℝ :=
  (((r : ℝ) + ϑ) * K - adaptiveLogZ ϑ Q K M logN r) /
    ((r : ℝ) - 1)

def adaptiveLogLambda (ϑ Q K M logN : ℝ) (r : ℕ) : ℝ :=
  (adaptiveLogZ ϑ Q K M logN r - logN) / (r : ℝ)

lemma log_adaptiveUAt (Q : ℝ) (k r : ℕ) (hk : 1 < k) :
    Real.log (adaptiveUAt Q k r) =
      adaptiveLogU Q (Real.log k) (Real.log (Real.log k)) r := by
  have hkR : (1 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hlog : 0 < Real.log (k : ℝ) := Real.log_pos hkR
  unfold adaptiveUAt adaptiveLogU
  rw [Real.log_mul (by positivity)
      (ne_of_gt (Real.rpow_pos_of_pos hlog _)),
    Real.log_rpow (by positivity),
    Real.log_rpow hlog]
  ring

lemma log_adaptiveVAt (ϑ Q : ℝ) (k r : ℕ) (hk : 1 < k) :
    Real.log (adaptiveVAt ϑ Q k r) =
      adaptiveLogV ϑ Q (Real.log k) (Real.log (Real.log k)) r := by
  have hkR : (1 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hlog : 0 < Real.log (k : ℝ) := Real.log_pos hkR
  unfold adaptiveVAt adaptiveLogV
  rw [Real.log_mul (by positivity)
      (ne_of_gt (Real.rpow_pos_of_pos hlog _)),
    Real.log_rpow (by positivity),
    Real.log_rpow hlog]

lemma log_adaptiveZAt (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) (hn : 0 < n) :
    Real.log (adaptiveZAt ϑ Q k n r) =
      adaptiveLogZ ϑ Q (Real.log k) (Real.log (Real.log k))
        (Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) r := by
  have hN : 0 < (n : ℝ) * (Nat.factorial r : ℝ) := by positivity
  have hV := adaptiveVAt_pos ϑ Q k r hk
  by_cases hNV : (n : ℝ) * (Nat.factorial r : ℝ) ≤
      adaptiveVAt ϑ Q k r
  · have hlogNV : Real.log ((n : ℝ) * (Nat.factorial r : ℝ)) ≤
        Real.log (adaptiveVAt ϑ Q k r) :=
      (Real.log_le_log_iff hN hV).2 hNV
    rw [adaptiveZAt, max_eq_right hNV, adaptiveLogZ,
      max_eq_right (by simpa [log_adaptiveVAt ϑ Q k r hk] using hlogNV),
      log_adaptiveVAt ϑ Q k r hk]
  · have hVN : adaptiveVAt ϑ Q k r ≤
        (n : ℝ) * (Nat.factorial r : ℝ) := le_of_not_ge hNV
    have hlogVN : adaptiveLogV ϑ Q (Real.log k)
          (Real.log (Real.log k)) r ≤
        Real.log ((n : ℝ) * (Nat.factorial r : ℝ)) := by
      rw [← log_adaptiveVAt ϑ Q k r hk]
      exact (Real.log_le_log_iff hV hN).2 hVN
    rw [adaptiveZAt, max_eq_left hVN, adaptiveLogZ, max_eq_left hlogVN]

lemma log_adaptiveLambdaAt (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) (hn : 0 < n) :
    Real.log (adaptiveLambdaAt ϑ Q k n r) =
      adaptiveLogLambda ϑ Q (Real.log k) (Real.log (Real.log k))
        (Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) r := by
  have hN : 0 < (n : ℝ) * (Nat.factorial r : ℝ) := by positivity
  have hratio : 0 < adaptiveZAt ϑ Q k n r /
      ((n : ℝ) * (Nat.factorial r : ℝ)) :=
    div_pos (adaptiveZAt_pos ϑ Q k n r hk) hN
  unfold adaptiveLambdaAt adaptiveLogLambda
  rw [Real.log_rpow hratio,
    Real.log_div (adaptiveZAt_pos ϑ Q k n r hk).ne' hN.ne',
    log_adaptiveZAt ϑ Q k n r hk hn]
  ring

lemma log_adaptiveT1At (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) (hn : 0 < n) :
    Real.log (adaptiveT1At ϑ Q k n r) =
      adaptiveLogT1 ϑ Q (Real.log k) (Real.log (Real.log k))
        (Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) r := by
  have hkpos : 0 < (k : ℝ) := by positivity
  have hbase : 0 < adaptiveZAt ϑ Q k n r /
      (k : ℝ) ^ ((r : ℝ) + 1) :=
    div_pos (adaptiveZAt_pos ϑ Q k n r hk)
      (Real.rpow_pos_of_pos hkpos _)
  unfold adaptiveT1At adaptiveLogT1
  rw [Real.log_rpow hbase,
    Real.log_div (adaptiveZAt_pos ϑ Q k n r hk).ne'
      (Real.rpow_pos_of_pos hkpos _).ne',
    log_adaptiveZAt ϑ Q k n r hk hn,
    Real.log_rpow hkpos]
  ring

lemma log_adaptiveT2At (ϑ Q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hk : 1 < k) (hn : 0 < n) :
    Real.log (adaptiveT2At ϑ Q k n r) =
      adaptiveLogT2 ϑ Q (Real.log k) (Real.log (Real.log k))
        (Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) r := by
  have hkpos : 0 < (k : ℝ) := by positivity
  have hbase : 0 < (k : ℝ) ^ ((r : ℝ) + ϑ) /
      adaptiveZAt ϑ Q k n r :=
    div_pos (Real.rpow_pos_of_pos hkpos _)
      (adaptiveZAt_pos ϑ Q k n r hk)
  unfold adaptiveT2At adaptiveLogT2
  rw [Real.log_rpow hbase,
    Real.log_div (Real.rpow_pos_of_pos hkpos _).ne'
      (adaptiveZAt_pos ϑ Q k n r hk).ne', Real.log_rpow hkpos,
    log_adaptiveZAt ϑ Q k n r hk hn]
  ring

/-! ### Scoped location-blind, termwise-nonnegative obstruction

The following definitions are the logarithmic image of one block in the
explicit certificate class from `adaptive_unbalanced_partition_frontier.md`.
Here `logD` is the logarithm of the derivative-size factor, `logLam` is the
logarithm of the freely chosen Konyagin scale, `logDelta` is the logarithm of
the safe approximation threshold, and `logW` is the logarithm of the
rational-denominator parameter.  No assertion is made about certificates
using cross-block cancellation, prime-location-adaptive sparse covers, or a
stronger exponential-sum estimate. -/

def locationBlindLogT1 (logD logLam logW : ℝ) (r : ℕ) : ℝ :=
  (logD + (r : ℝ) * logLam + 2 * logW) /
    (2 * (r : ℝ) - 1)

def locationBlindLogT2
    (logDelta logD logLam logW : ℝ) (r : ℕ) : ℝ :=
  (logDelta + 2 * logW - logD - (r : ℝ) * logLam) /
    ((r : ℝ) - 1)

/-- Exact first-two-term invariant for one location-blind Konyagin block.
It is the logarithm of
`T1^(2r-1) * T2^(r-1) = delta * W^4`; in particular all dependence on the
unbalanced scale `lambda` and on the derivative factor `D` cancels. -/
lemma locationBlind_first_two_log_invariant
    (logDelta logD logLam logW : ℝ) (r : ℕ) (hr2 : 2 ≤ r) :
    (2 * (r : ℝ) - 1) * locationBlindLogT1 logD logLam logW r +
        ((r : ℝ) - 1) *
          locationBlindLogT2 logDelta logD logLam logW r =
      logDelta + 4 * logW := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hden1 : 2 * (r : ℝ) - 1 ≠ 0 := by nlinarith
  have hden2 : (r : ℝ) - 1 ≠ 0 := by nlinarith
  unfold locationBlindLogT1 locationBlindLogT2
  field_simp
  ring

/-- Increasing the denominator parameter cannot weaken the invariant.  This
is the precise `W>=1` monotonicity used by the scoped no-go argument. -/
lemma locationBlind_first_two_invariant_ge_delta_of_W_ge_one
    (logDelta logD logLam : ℝ) (W : ℝ) (r : ℕ)
    (hr2 : 2 ≤ r) (hW : 1 ≤ W) :
    logDelta ≤
      (2 * (r : ℝ) - 1) *
          locationBlindLogT1 logD logLam (Real.log W) r +
        ((r : ℝ) - 1) *
          locationBlindLogT2 logDelta logD logLam (Real.log W) r := by
  rw [locationBlind_first_two_log_invariant logDelta logD logLam
    (Real.log W) r hr2]
  have hlogW : 0 ≤ Real.log W := Real.log_nonneg hW
  linarith

/-- Finite-scale consequence of requiring both nonnegative first terms to
meet separate logarithmic budgets on one block.  The safe-tail input is
written with its genuine extra `loglog(k)` loss:
`log(delta W^4) >= -(1-theta)K-M-C`.

This theorem is only a block lemma for the explicitly named location-blind,
termwise-nonnegative certificate class. -/
lemma locationBlind_termwise_block_budget_obstruction
    (ϑ K M C logDelta logD logLam logW α β : ℝ) (r : ℕ)
    (hr2 : 2 ≤ r)
    (hT1 : locationBlindLogT1 logD logLam logW r ≤ -α * M)
    (hT2 : locationBlindLogT2 logDelta logD logLam logW r ≤ -β * M)
    (hsafe : -(1 - ϑ) * K - M - C ≤ logDelta + 4 * logW) :
    ((2 * (r : ℝ) - 1) * α + ((r : ℝ) - 1) * β) * M ≤
      (1 - ϑ) * K + M + C := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hw1 : 0 ≤ 2 * (r : ℝ) - 1 := by nlinarith
  have hw2 : 0 ≤ (r : ℝ) - 1 := by nlinarith
  have hT1' := mul_le_mul_of_nonneg_left hT1 hw1
  have hT2' := mul_le_mul_of_nonneg_left hT2 hw2
  have hinv := locationBlind_first_two_log_invariant
    logDelta logD logLam logW r hr2
  nlinarith

/-- The actual adaptive `T1,T2` definitions obey the same exact invariant;
the chosen `max` scale and the balancing parameter `Q` disappear. -/
lemma adaptive_first_two_log_invariant
    (ϑ Q K M logN : ℝ) (r : ℕ) (hr2 : 2 ≤ r) :
    (2 * (r : ℝ) - 1) * adaptiveLogT1 ϑ Q K M logN r +
        ((r : ℝ) - 1) * adaptiveLogT2 ϑ Q K M logN r =
      (ϑ - 1) * K := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hden1 : 2 * (r : ℝ) - 1 ≠ 0 := by nlinarith
  have hden2 : (r : ℝ) - 1 ≠ 0 := by nlinarith
  unfold adaptiveLogT1 adaptiveLogT2
  field_simp
  ring

/-- Exact finite-scale obstruction for the actual adaptive first two terms.
If they separately decay like `exp(-alpha*M)` and `exp(-beta*M)`, their
weighted logarithmic budget cannot exceed `(1-theta)K`. -/
lemma adaptive_first_two_budget_obstruction
    (ϑ Q K M logN α β : ℝ) (r : ℕ) (hr2 : 2 ≤ r)
    (hT1 : adaptiveLogT1 ϑ Q K M logN r ≤ -α * M)
    (hT2 : adaptiveLogT2 ϑ Q K M logN r ≤ -β * M) :
    ((2 * (r : ℝ) - 1) * α + ((r : ℝ) - 1) * β) * M ≤
      (1 - ϑ) * K := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hw1 : 0 ≤ 2 * (r : ℝ) - 1 := by nlinarith
  have hw2 : 0 ≤ (r : ℝ) - 1 := by nlinarith
  have hT1' := mul_le_mul_of_nonneg_left hT1 hw1
  have hT2' := mul_le_mul_of_nonneg_left hT2 hw2
  have hinv := adaptive_first_two_log_invariant ϑ Q K M logN r hr2
  nlinarith

/-- Finite-scale endpoint form of the little-`o` obstruction.  Write the two
separate budgets as `log(Ti) <= -M-q`; the common excess `q` is allowed to
depend on the outer scale.  If the endpoint order satisfies
`r*M >= c*K-D*M` and `c >= (1-theta)/3`, then the invariant forces
`(3r-2)q <= (3D+3)M+C`.  Thus the natural proof's extracted sequence with
`q -> infinity`, `r` of order `K/M`, and bounded comparison losses cannot
exist.  The sequence extraction itself is intentionally not asserted here. -/
lemma locationBlind_endpoint_excess_budget
    (ϑ c K M C D q logDelta logD logLam logW : ℝ) (r : ℕ)
    (hr2 : 2 ≤ r) (hK : 0 ≤ K)
    (hfront : (1 - ϑ) / 3 ≤ c)
    (horder : c * K - D * M ≤ (r : ℝ) * M)
    (hT1 : locationBlindLogT1 logD logLam logW r ≤ -M - q)
    (hT2 : locationBlindLogT2 logDelta logD logLam logW r ≤ -M - q)
    (hsafe : -(1 - ϑ) * K - M - C ≤ logDelta + 4 * logW) :
    (3 * (r : ℝ) - 2) * q ≤ (3 * D + 3) * M + C := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hw1 : 0 ≤ 2 * (r : ℝ) - 1 := by nlinarith
  have hw2 : 0 ≤ (r : ℝ) - 1 := by nlinarith
  have hT1' := mul_le_mul_of_nonneg_left hT1 hw1
  have hT2' := mul_le_mul_of_nonneg_left hT2 hw2
  have hinv := locationBlind_first_two_log_invariant
    logDelta logD logLam logW r hr2
  have htheta : 1 - ϑ ≤ 3 * c := by nlinarith
  have hthetaK := mul_le_mul_of_nonneg_right htheta hK
  nlinarith

/-- Direct finite contradiction form of
`locationBlind_endpoint_excess_budget`, still scoped to one selected block of
the location-blind nonnegative certificate class. -/
theorem locationBlind_endpoint_termwise_no_go_of_excess
    (ϑ c K M C D q logDelta logD logLam logW : ℝ) (r : ℕ)
    (hr2 : 2 ≤ r) (hK : 0 ≤ K)
    (hfront : (1 - ϑ) / 3 ≤ c)
    (horder : c * K - D * M ≤ (r : ℝ) * M)
    (hsafe : -(1 - ϑ) * K - M - C ≤ logDelta + 4 * logW)
    (hexcess : (3 * D + 3) * M + C < (3 * (r : ℝ) - 2) * q) :
    ¬ (locationBlindLogT1 logD logLam logW r ≤ -M - q ∧
      locationBlindLogT2 logDelta logD logLam logW r ≤ -M - q) := by
  rintro ⟨hT1, hT2⟩
  have hbound := locationBlind_endpoint_excess_budget
    ϑ c K M C D q logDelta logD logLam logW r hr2 hK hfront horder
      hT1 hT2 hsafe
  linarith

/-- Leading linear-program image of the explicitly delimited certificate
class.  `rho` is the limiting order scale `r loglog(k)/log(k)`, while
`alpha,beta>1` encode the two separate `o(1/log(k))` budgets.  This is a
definition of the scoped parameter class, not of all possible approaches to
Erdos 451. -/
def LocationBlindTermwiseLeadingCertificate (ϑ c : ℝ) : Prop :=
  ∃ ρ α β : ℝ,
    0 < ρ ∧ c ≤ ρ ∧ 1 < α ∧ 1 < β ∧
      (2 * α + β) * ρ ≤ 1 - ϑ

/-- Exact feasibility frontier of the location-blind, termwise-nonnegative
leading certificate class.  This is the kernel form of the LP in equation
(29) of the natural proof; it does not cover cancellation or extra local
prime information. -/
theorem locationBlindTermwiseLeadingCertificate_iff
    (ϑ c : ℝ) (hc : 0 < c) :
    LocationBlindTermwiseLeadingCertificate ϑ c ↔
      c < (1 - ϑ) / 3 := by
  constructor
  · rintro ⟨ρ, α, β, hρ, hcρ, hα, hβ, hbudget⟩
    have hcoef : 3 < 2 * α + β := by nlinarith
    have hscale : 3 * c ≤ 3 * ρ := by nlinarith
    have hstrict : 3 * ρ < (2 * α + β) * ρ := by
      exact mul_lt_mul_of_pos_right hcoef hρ
    rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 3)]
    nlinarith
  · intro hcfront
    have hratio : 1 < (1 - ϑ) / (3 * c) := by
      rw [lt_div_iff₀ (by positivity : 0 < 3 * c)]
      rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 3)] at hcfront
      nlinarith
    obtain ⟨q, hq, hqu⟩ := exists_between hratio
    have hmargin : 3 * q * c < 1 - ϑ := by
      have := (lt_div_iff₀ (by positivity : 0 < 3 * c)).1 hqu
      nlinarith
    refine ⟨c, q, q, hc, le_rfl, hq, hq, ?_⟩
    nlinarith

/-- Endpoint no-go, deliberately scoped to
`LocationBlindTermwiseLeadingCertificate`. -/
theorem locationBlindTermwiseLeadingCertificate_no_go
    (ϑ c : ℝ) (hc : 0 < c) (hfront : (1 - ϑ) / 3 ≤ c) :
    ¬ LocationBlindTermwiseLeadingCertificate ϑ c := by
  intro hcert
  have hlt :=
    (locationBlindTermwiseLeadingCertificate_iff ϑ c hc).1 hcert
  linarith

/-- Concrete BHP specialization of the same scoped leading-certificate
obstruction.  This does not assert a no-go for Erdős 451 itself. -/
theorem locationBlindTermwiseLeadingCertificate_no_go_bhp
    (c : ℝ) (hc : (19 : ℝ) / 120 ≤ c) :
    ¬ LocationBlindTermwiseLeadingCertificate ((21 : ℝ) / 40) c := by
  apply locationBlindTermwiseLeadingCertificate_no_go
  · nlinarith
  · norm_num
    exact hc

/-- The strict parameter system needed by the adaptive stopping rule.  Unlike
the balanced package, it has no artificial `theta>9/23` field. -/
def AdaptiveFrontierParameters (ϑ c : ℝ) : Prop :=
  ∃ Q a : ℝ, 1 < Q ∧ 0 < a ∧ c < a ∧ 3 * Q * a < 1 - ϑ

lemma adaptiveFrontierParameters_of_wide (ϑ c : ℝ)
    (hϑ1 : ϑ < 1) (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    AdaptiveFrontierParameters ϑ c := by
  let f : ℝ := (1 - ϑ) / 3
  let a : ℝ := (c + f) / 2
  have hfpos : 0 < f := by dsimp [f]; nlinarith
  have hcf : c < f := by simpa [f] using hcfront
  have ha : 0 < a := by dsimp [a]; nlinarith
  have hca : c < a := by dsimp [a]; nlinarith
  have haf : a < f := by dsimp [a]; nlinarith
  have hthree : 3 * a < 1 - ϑ := by
    have : 3 * f = 1 - ϑ := by dsimp [f]; ring
    nlinarith
  have hratio : 1 < (1 - ϑ) / (3 * a) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa [mul_assoc] using hthree
  obtain ⟨Q, hQ, hQu⟩ := exists_between hratio
  refine ⟨Q, a, hQ, ha, hca, ?_⟩
  have hh := (lt_div_iff₀ (by positivity : 0 < 3 * a)).1 hQu
  nlinarith

/-- Exact feasibility of the adaptive strict-margin system. -/
theorem adaptiveFrontierParameters_iff (ϑ c : ℝ) (hc : 0 < c) :
    AdaptiveFrontierParameters ϑ c ↔
      ϑ < 1 ∧ c < (1 - ϑ) / 3 := by
  constructor
  · rintro ⟨Q, a, hQ, ha, hca, hm⟩
    have hQa : a < Q * a := by nlinarith
    constructor
    · nlinarith [mul_pos (mul_pos (by norm_num : (0 : ℝ) < 3)
          (lt_trans zero_lt_one hQ)) ha]
    · rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 3)]
      nlinarith
  · rintro ⟨hϑ1, hcfront⟩
    exact adaptiveFrontierParameters_of_wide ϑ c hϑ1 hc hcfront

/-- `V_r<=U_r`: the adaptive scale interval is nonempty whenever the chosen
order stays below its strict logarithmic budget. -/
lemma adaptiveLogV_le_logU (ϑ Q a K M : ℝ) (r : ℕ)
    (hQ : 0 ≤ Q) (hK : 0 < K) (hM : 0 ≤ M)
    (hrM : (r : ℝ) * M ≤ a * K)
    (hmargin : 3 * Q * a < 1 - ϑ) :
    adaptiveLogV ϑ Q K M r ≤ adaptiveLogU Q K M r := by
  have hcoef : Q * (3 * (r : ℝ) - 2) * M ≤
      3 * Q * ((r : ℝ) * M) := by
    nlinarith [mul_nonneg hQ hM]
  have hscaled : 3 * Q * ((r : ℝ) * M) ≤ 3 * Q * (a * K) :=
    mul_le_mul_of_nonneg_left hrM (mul_nonneg (by norm_num) hQ)
  have hstrict : 3 * Q * (a * K) < (1 - ϑ) * K := by
    have := mul_lt_mul_of_pos_right hmargin hK
    nlinarith
  unfold adaptiveLogV adaptiveLogU
  nlinarith

/-- Decisive adaptive selection algebra.  `K=log k`, `M=loglog k`, and
`logN=log(nr!)` in the natural proof.  The upper stopping inequality and
failure at the preceding order imply simultaneous logarithmic budgets for
the first two Konyagin terms and the sharp
`log lambda <= (theta/r) log k + 3Q loglog k` estimate. -/
theorem adaptive_log_selection_budget
    (ϑ Q a K M logN : ℝ) (r : ℕ)
    (hϑ0 : 0 < ϑ) (hQ : 0 ≤ Q) (hK : 0 < K) (hM : 0 ≤ M)
    (hr2 : 2 ≤ r) (hrM : (r : ℝ) * M ≤ a * K)
    (hmargin : 3 * Q * a < 1 - ϑ)
    (hupper : logN ≤ adaptiveLogU Q K M r)
    (hlower : (r : ℝ) * K - Q * (2 * (r : ℝ) - 3) * M ≤ logN) :
    adaptiveLogV ϑ Q K M r ≤ adaptiveLogU Q K M r ∧
    adaptiveLogV ϑ Q K M r ≤ adaptiveLogZ ϑ Q K M logN r ∧
    adaptiveLogZ ϑ Q K M logN r ≤ adaptiveLogU Q K M r ∧
    adaptiveLogT1 ϑ Q K M logN r ≤ -Q * M ∧
    adaptiveLogT2 ϑ Q K M logN r ≤ -Q * M ∧
    adaptiveLogLambda ϑ Q K M logN r ≤
      ϑ / (r : ℝ) * K + 3 * Q * M := by
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hrpos : (0 : ℝ) < r := by positivity
  have hden1 : 0 < 2 * (r : ℝ) - 1 := by nlinarith
  have hden2 : 0 < (r : ℝ) - 1 := by nlinarith
  have hVU := adaptiveLogV_le_logU ϑ Q a K M r hQ hK hM hrM hmargin
  have hVZ : adaptiveLogV ϑ Q K M r ≤
      adaptiveLogZ ϑ Q K M logN r := by
    exact le_max_right _ _
  have hZU : adaptiveLogZ ϑ Q K M logN r ≤
      adaptiveLogU Q K M r := by
    exact max_le hupper hVU
  have hT1 : adaptiveLogT1 ϑ Q K M logN r ≤ -Q * M := by
    unfold adaptiveLogT1
    rw [div_le_iff₀ hden1]
    unfold adaptiveLogU at hZU
    nlinarith
  have hT2 : adaptiveLogT2 ϑ Q K M logN r ≤ -Q * M := by
    unfold adaptiveLogT2
    rw [div_le_iff₀ hden2]
    unfold adaptiveLogV at hVZ
    nlinarith
  have hlamrhs : 0 ≤ ϑ * K + 3 * Q * (r : ℝ) * M := by positivity
  have hVlam : adaptiveLogV ϑ Q K M r ≤
      logN + (ϑ * K + 3 * Q * (r : ℝ) * M) := by
    unfold adaptiveLogV
    nlinarith [mul_nonneg hQ hM]
  have hZlam : adaptiveLogZ ϑ Q K M logN r ≤
      logN + (ϑ * K + 3 * Q * (r : ℝ) * M) := by
    exact max_le (by linarith) hVlam
  have hlam : adaptiveLogLambda ϑ Q K M logN r ≤
      ϑ / (r : ℝ) * K + 3 * Q * M := by
    unfold adaptiveLogLambda
    apply (div_le_iff₀ hrpos).2
    calc
      adaptiveLogZ ϑ Q K M logN r - logN ≤
          ϑ * K + 3 * Q * (r : ℝ) * M := by linarith
      _ = (ϑ / (r : ℝ) * K + 3 * Q * M) * (r : ℝ) := by
        field_simp
  exact ⟨hVU, hVZ, hZU, hT1, hT2, hlam⟩

/-- Actual-real-scale form of `adaptive_log_selection_budget`.  It certifies
the exact positive `lambda`, its powered mass identity, the two balanced
Konyagin budgets, and the minimality upper bound used for the remaining
terms. -/
theorem adaptive_actual_selection_budget
    (ϑ Q a : ℝ) (k : ℕ) (n : ℤ) (r : ℕ)
    (hϑ0 : 0 < ϑ) (hQ : 0 ≤ Q) (hk : 1 < k)
    (hlog1 : 1 ≤ Real.log k) (hn : 0 < n) (hr2 : 2 ≤ r)
    (hrM : (r : ℝ) * Real.log (Real.log k) ≤ a * Real.log k)
    (hmargin : 3 * Q * a < 1 - ϑ)
    (hupper : (n : ℝ) * (Nat.factorial r : ℝ) ≤ adaptiveUAt Q k r)
    (hlower : (r : ℝ) * Real.log k -
        Q * (2 * (r : ℝ) - 3) * Real.log (Real.log k) ≤
      Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) :
    adaptiveVAt ϑ Q k r ≤ adaptiveZAt ϑ Q k n r ∧
    adaptiveZAt ϑ Q k n r ≤ adaptiveUAt Q k r ∧
    1 ≤ adaptiveLambdaAt ϑ Q k n r ∧
    (n : ℝ) * (Nat.factorial r : ℝ) *
        (adaptiveLambdaAt ϑ Q k n r) ^ r = adaptiveZAt ϑ Q k n r ∧
    adaptiveT1At ϑ Q k n r ≤ (Real.log k) ^ (-Q) ∧
    adaptiveT2At ϑ Q k n r ≤ (Real.log k) ^ (-Q) ∧
    adaptiveLambdaAt ϑ Q k n r ≤
      (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q) := by
  have hkR : (1 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hK : 0 < Real.log (k : ℝ) := Real.log_pos hkR
  have hM : 0 ≤ Real.log (Real.log (k : ℝ)) := Real.log_nonneg hlog1
  have hN : 0 < (n : ℝ) * (Nat.factorial r : ℝ) := by positivity
  have hU : 0 < adaptiveUAt Q k r := adaptiveUAt_pos Q k r hk
  have hV : 0 < adaptiveVAt ϑ Q k r := adaptiveVAt_pos ϑ Q k r hk
  have hZ : 0 < adaptiveZAt ϑ Q k n r := adaptiveZAt_pos ϑ Q k n r hk
  have hupperLog : Real.log ((n : ℝ) * (Nat.factorial r : ℝ)) ≤
      adaptiveLogU Q (Real.log k) (Real.log (Real.log k)) r := by
    rw [← log_adaptiveUAt Q k r hk]
    exact (Real.log_le_log_iff hN hU).2 hupper
  obtain ⟨hVUlog, _hVZlog, hZUlog, hT1log, hT2log, hlamlog⟩ :=
    adaptive_log_selection_budget ϑ Q a (Real.log k)
      (Real.log (Real.log k))
      (Real.log ((n : ℝ) * (Nat.factorial r : ℝ))) r
      hϑ0 hQ hK hM hr2 hrM hmargin hupperLog hlower
  have hVU : adaptiveVAt ϑ Q k r ≤ adaptiveUAt Q k r := by
    rw [← Real.log_le_log_iff hV hU, log_adaptiveVAt ϑ Q k r hk,
      log_adaptiveUAt Q k r hk]
    exact hVUlog
  have hZU : adaptiveZAt ϑ Q k n r ≤ adaptiveUAt Q k r := by
    rw [← Real.log_le_log_iff hZ hU,
      log_adaptiveZAt ϑ Q k n r hk hn, log_adaptiveUAt Q k r hk]
    exact hZUlog
  have hT1pos : 0 < adaptiveT1At ϑ Q k n r := by
    unfold adaptiveT1At
    positivity
  have hT2pos : 0 < adaptiveT2At ϑ Q k n r := by
    unfold adaptiveT2At
    positivity
  have hlogpow : 0 < (Real.log k) ^ (-Q) :=
    Real.rpow_pos_of_pos hK _
  have hT1 : adaptiveT1At ϑ Q k n r ≤ (Real.log k) ^ (-Q) := by
    rw [← Real.log_le_log_iff hT1pos hlogpow,
      log_adaptiveT1At ϑ Q k n r hk hn, Real.log_rpow hK]
    exact hT1log
  have hT2 : adaptiveT2At ϑ Q k n r ≤ (Real.log k) ^ (-Q) := by
    rw [← Real.log_le_log_iff hT2pos hlogpow,
      log_adaptiveT2At ϑ Q k n r hk hn, Real.log_rpow hK]
    exact hT2log
  have hlampos : 0 < adaptiveLambdaAt ϑ Q k n r := by
    unfold adaptiveLambdaAt
    positivity
  have hlamRhs : 0 < (k : ℝ) ^ (ϑ / (r : ℝ)) *
      (Real.log k) ^ (3 * Q) := by positivity
  have hlogRhs : Real.log ((k : ℝ) ^ (ϑ / (r : ℝ)) *
        (Real.log k) ^ (3 * Q)) =
      ϑ / (r : ℝ) * Real.log k + 3 * Q * Real.log (Real.log k) := by
    rw [Real.log_mul (Real.rpow_pos_of_pos (by positivity) _).ne'
        (Real.rpow_pos_of_pos hK _).ne',
      Real.log_rpow (by positivity), Real.log_rpow hK]
  have hlam : adaptiveLambdaAt ϑ Q k n r ≤
      (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q) := by
    rw [← Real.log_le_log_iff hlampos hlamRhs,
      log_adaptiveLambdaAt ϑ Q k n r hk hn, hlogRhs]
    exact hlamlog
  exact ⟨le_max_right _ _, hZU,
    adaptiveLambdaAt_ge_one ϑ Q k n r hn (by omega),
    adaptive_mass_mul_lambda_pow ϑ Q k n r hk hn (by omega), hT1, hT2, hlam⟩

/-- Pure least-order constructor for the actual stopping predicate
`n r! <= U_r`.  The conclusion records both the selected upper inequality
and strict failure at the preceding order. -/
theorem exists_min_adaptive_stopping_order (Q : ℝ) (k : ℕ) (n : ℤ)
    (R : ℕ)
    (hR : (n : ℝ) * (Nat.factorial R : ℝ) ≤ adaptiveUAt Q k R)
    (hsmall : ∀ j : ℕ, j < 2 →
      adaptiveUAt Q k j < (n : ℝ) * (Nat.factorial j : ℝ)) :
    ∃ r : ℕ,
      2 ≤ r ∧ r ≤ R ∧
      (n : ℝ) * (Nat.factorial r : ℝ) ≤ adaptiveUAt Q k r ∧
      adaptiveUAt Q k (r - 1) <
        (n : ℝ) * (Nat.factorial (r - 1) : ℝ) := by
  let P : ℕ → Prop := fun j =>
    (n : ℝ) * (Nat.factorial j : ℝ) ≤ adaptiveUAt Q k j
  have hExists : ∃ j : ℕ, P j := ⟨R, hR⟩
  let r : ℕ := Nat.find hExists
  have hrle : r ≤ R := Nat.find_min' hExists hR
  have hrspec : P r := Nat.find_spec hExists
  have hr2 : 2 ≤ r := by
    by_contra h
    have hrlt : r < 2 := Nat.lt_of_not_ge h
    exact (not_lt_of_ge hrspec) (hsmall r hrlt)
  have hrpred : r - 1 < r := Nat.sub_lt (by omega) zero_lt_one
  have hpredNot : ¬ P (r - 1) := Nat.find_min hExists hrpred
  refine ⟨r, hr2, hrle, hrspec, ?_⟩
  exact lt_of_not_ge hpredNot

/-- Strict failure at the preceding stopping order implies exactly the lower
logarithmic inequality consumed by `adaptive_actual_selection_budget`. -/
lemma adaptive_preceding_failure_log_lower (Q : ℝ) (k : ℕ) (n : ℤ)
    (r : ℕ) (hk : 1 < k) (hn : 0 < n) (hr2 : 2 ≤ r)
    (hfail : adaptiveUAt Q k (r - 1) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ)) :
    (r : ℝ) * Real.log k -
        Q * (2 * (r : ℝ) - 3) * Real.log (Real.log k) ≤
      Real.log ((n : ℝ) * (Nat.factorial r : ℝ)) := by
  have hNpred : 0 < (n : ℝ) * (Nat.factorial (r - 1) : ℝ) := by
    positivity
  have hNr : 0 < (n : ℝ) * (Nat.factorial r : ℝ) := by positivity
  have hfac : (Nat.factorial (r - 1) : ℝ) ≤
      (Nat.factorial r : ℝ) := by
    exact_mod_cast Nat.factorial_le (Nat.sub_le r 1)
  have hNmono : (n : ℝ) * (Nat.factorial (r - 1) : ℝ) ≤
      (n : ℝ) * (Nat.factorial r : ℝ) := by
    exact mul_le_mul_of_nonneg_left hfac (by exact_mod_cast hn.le)
  have hlogchain : Real.log (adaptiveUAt Q k (r - 1)) ≤
      Real.log ((n : ℝ) * (Nat.factorial r : ℝ)) := by
    exact (Real.log_le_log_iff (adaptiveUAt_pos Q k (r - 1) hk) hNr).2
      (hfail.le.trans hNmono)
  rw [log_adaptiveUAt Q k (r - 1) hk] at hlogchain
  unfold adaptiveLogU at hlogchain
  rw [Nat.cast_sub (by omega : 1 ≤ r)] at hlogchain
  norm_num at hlogchain ⊢
  convert hlogchain using 1 <;> ring

/-- Uniform eventual domination of the adaptive additive envelope.  This is
the analytic reason the selected scale works for every fixed `theta>0`:
`r>=2` leaves the strict power gap `theta/2`, while `r<=log k` costs only one
extra logarithm. -/
lemma adaptive_additive_envelope_eventual (ϑ Q C : ℝ)
    (hϑ0 : 0 < ϑ) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ r : ℕ,
      2 ≤ r → (r : ℝ) ≤ Real.log k →
      2 * (r : ℝ) *
          ((k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q)) ≤
        C * (k : ℝ) ^ ϑ / Real.log k := by
  obtain ⟨k₀, hk₀⟩ := Filter.eventually_atTop.mp
    (poly_log_lt 2 (ϑ / 2) (3 * Q + 1) ϑ (by linarith)
      C hC)
  refine ⟨k₀ + 2, fun k hk r hr2 hrlog => ?_⟩
  have hk₀' : k₀ ≤ k := by omega
  have hkpos : 0 < (k : ℝ) := by norm_cast; omega
  have hLpos : 0 < Real.log (k : ℝ) := Real.log_pos (by norm_cast; omega)
  have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
  have hexp : ϑ / (r : ℝ) ≤ ϑ / 2 := by
    exact div_le_div_of_nonneg_left hϑ0.le (by norm_num) hrR
  have hkpow : (k : ℝ) ^ (ϑ / (r : ℝ)) ≤
      (k : ℝ) ^ (ϑ / 2) :=
    Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega) hexp
  have hlogpow : 0 ≤ (Real.log k) ^ (3 * Q) :=
    Real.rpow_nonneg hLpos.le _
  have henv : 2 * (r : ℝ) *
        ((k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q)) ≤
      2 * (k : ℝ) ^ (ϑ / 2) * (Real.log k) ^ (3 * Q + 1) := by
    calc
      2 * (r : ℝ) *
          ((k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q)) ≤
          2 * Real.log k *
            ((k : ℝ) ^ (ϑ / 2) * (Real.log k) ^ (3 * Q)) := by
              gcongr
      _ = 2 * (k : ℝ) ^ (ϑ / 2) *
          (Real.log k) ^ (3 * Q + 1) := by
            rw [Real.rpow_add hLpos]
            norm_num
            ring
  exact henv.trans (hk₀ k hk₀')

/-- The actual selected additive term inherits the uniform envelope. -/
lemma adaptive_additive_term_eventual (ϑ Q C : ℝ)
    (hϑ0 : 0 < ϑ) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ, ∀ r : ℕ,
      2 ≤ r → (r : ℝ) ≤ Real.log k →
      adaptiveLambdaAt ϑ Q k n r ≤
        (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q) →
      2 * (r : ℝ) * adaptiveLambdaAt ϑ Q k n r ≤
        C * (k : ℝ) ^ ϑ / Real.log k := by
  obtain ⟨k₀, hk₀⟩ := adaptive_additive_envelope_eventual ϑ Q C hϑ0 hC
  refine ⟨k₀, fun k hk n r hr2 hrlog hlam => ?_⟩
  exact (mul_le_mul_of_nonneg_left hlam (by positivity)).trans
    (hk₀ k hk r hr2 hrlog)

/-- A single pointwise logarithmic estimate for the third Konyagin term,
valid uniformly at `r=2` and every larger stopping order. -/
lemma adaptiveT3At_le_logpow (ϑ Q q : ℝ)
    (k : ℕ) (n : ℤ) (r : ℕ)
    (hϑ0 : 0 < ϑ) (hk : 1 < k) (hn : 0 < n) (hr2 : 2 ≤ r)
    (hlog1 : 1 < Real.log k)
    (hrplus : (r : ℝ) + 1 ≤ Real.log k)
    (hlam : adaptiveLambdaAt ϑ Q k n r ≤
      (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q))
    (hmargin : (1 + 3 * Q) * Real.log (Real.log k) +
        2 * q * (r : ℝ) * Real.log (Real.log k) ≤
      (1 - ϑ / 2) * Real.log k) :
    adaptiveT3At ϑ Q k n r ≤ (Real.log k) ^ (-q) := by
  have hkpos : 0 < (k : ℝ) := by positivity
  have hLpos : 0 < Real.log (k : ℝ) := by linarith
  have hlampos : 0 < adaptiveLambdaAt ϑ Q k n r := by
    unfold adaptiveLambdaAt
    exact Real.rpow_pos_of_pos
      (div_pos (adaptiveZAt_pos ϑ Q k n r hk) (by positivity)) _
  have henvpos : 0 < (k : ℝ) ^ (ϑ / (r : ℝ)) *
      (Real.log k) ^ (3 * Q) := by positivity
  have hlogenv : Real.log ((k : ℝ) ^ (ϑ / (r : ℝ)) *
        (Real.log k) ^ (3 * Q)) =
      ϑ / (r : ℝ) * Real.log k + 3 * Q * Real.log (Real.log k) := by
    rw [Real.log_mul (Real.rpow_pos_of_pos hkpos _).ne'
        (Real.rpow_pos_of_pos hLpos _).ne',
      Real.log_rpow hkpos, Real.log_rpow hLpos]
  have hlamlog : Real.log (adaptiveLambdaAt ϑ Q k n r) ≤
      ϑ / (r : ℝ) * Real.log k + 3 * Q * Real.log (Real.log k) := by
    rw [← hlogenv]
    exact (Real.log_le_log_iff hlampos henvpos).2 hlam
  have hrpos : (0 : ℝ) < r := by positivity
  have hrpluspos : 0 < (r : ℝ) + 1 := by positivity
  have hlogr : Real.log ((r : ℝ) + 1) ≤ Real.log (Real.log k) := by
    exact (Real.log_le_log_iff hrpluspos hLpos).2 hrplus
  have htheta : ϑ / (r : ℝ) * Real.log k ≤ ϑ / 2 * Real.log k := by
    have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
    exact mul_le_mul_of_nonneg_right
      (div_le_div_of_nonneg_left hϑ0.le (by norm_num) hrR) hLpos.le
  have hbasepos : 0 < ((r : ℝ) + 1) *
      adaptiveLambdaAt ϑ Q k n r / (k : ℝ) := by positivity
  have hlogbase :
      Real.log (((r : ℝ) + 1) * adaptiveLambdaAt ϑ Q k n r /
        (k : ℝ)) ≤
      -(1 - ϑ / 2) * Real.log k +
        (1 + 3 * Q) * Real.log (Real.log k) := by
    rw [Real.log_div (mul_pos hrpluspos hlampos).ne' hkpos.ne',
      Real.log_mul hrpluspos.ne' hlampos.ne']
    nlinarith
  have hlogstrong :
      Real.log (((r : ℝ) + 1) * adaptiveLambdaAt ϑ Q k n r /
        (k : ℝ)) ≤
      -2 * q * (r : ℝ) * Real.log (Real.log k) := by
    nlinarith
  have hT3pos : 0 < adaptiveT3At ϑ Q k n r := by
    unfold adaptiveT3At
    positivity
  have hlogpowpos : 0 < (Real.log k) ^ (-q) := by positivity
  rw [← Real.log_le_log_iff hT3pos hlogpowpos]
  unfold adaptiveT3At
  rw [Real.log_rpow hbasepos, Real.log_rpow hLpos]
  have hinvnonneg : 0 ≤ (2 * (r : ℝ))⁻¹ := by positivity
  calc
    (2 * (r : ℝ))⁻¹ *
        Real.log (((r : ℝ) + 1) * adaptiveLambdaAt ϑ Q k n r /
          (k : ℝ)) ≤
        (2 * (r : ℝ))⁻¹ *
          (-2 * q * (r : ℝ) * Real.log (Real.log k)) :=
      mul_le_mul_of_nonneg_left hlogstrong hinvnonneg
    _ = -q * Real.log (Real.log k) := by field_simp

/-- The strict fixed margin `2 q b < 1-theta/2` eventually absorbs the
lower-order `(1+3Q) loglog(k)` loss uniformly for all `r` with
`r loglog(k) <= b log(k)`. -/
lemma adaptive_third_margin_eventual (ϑ Q q b : ℝ)
    (hQ : 0 ≤ Q) (hq : 0 < q)
    (hgap : 2 * q * b < 1 - ϑ / 2) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ r : ℕ,
      (r : ℝ) * Real.log (Real.log k) ≤ b * Real.log k →
      (1 + 3 * Q) * Real.log (Real.log k) +
          2 * q * (r : ℝ) * Real.log (Real.log k) ≤
        (1 - ϑ / 2) * Real.log k := by
  let δ : ℝ := 1 - ϑ / 2 - 2 * q * b
  have hδ : 0 < δ := by dsimp [δ]; linarith
  have hratio := tendsto_log_div_loglog_atTop.eventually_ge_atTop
    ((1 + 3 * Q) / δ)
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop 1
  obtain ⟨k₀, hk₀⟩ := Filter.eventually_atTop.mp (hratio.and hM)
  refine ⟨k₀, fun k hk r hrM => ?_⟩
  rcases hk₀ k hk with ⟨hX, hM1⟩
  change (1 + 3 * Q) / δ ≤ Real.log k / Real.log (Real.log k) at hX
  change 1 ≤ Real.log (Real.log k) at hM1
  have hcoef : (1 + 3 * Q) * Real.log (Real.log k) ≤
      δ * Real.log k := by
    have hXM := mul_le_mul_of_nonneg_right hX (le_trans zero_le_one hM1)
    have hcancel : (Real.log k / Real.log (Real.log k)) *
        Real.log (Real.log k) = Real.log k := by
      field_simp
    calc
      (1 + 3 * Q) * Real.log (Real.log k) =
          δ * (((1 + 3 * Q) / δ) * Real.log (Real.log k)) := by
            field_simp
      _ ≤ δ * ((Real.log k / Real.log (Real.log k)) *
          Real.log (Real.log k)) :=
        mul_le_mul_of_nonneg_left hXM hδ.le
      _ = δ * Real.log k := by rw [hcancel]
  have hrterm : 2 * q * ((r : ℝ) * Real.log (Real.log k)) ≤
      2 * q * (b * Real.log k) :=
    mul_le_mul_of_nonneg_left hrM (by positivity)
  dsimp [δ] at hcoef
  nlinarith

/-- Eventual third-term budget for the actual selected adaptive scale. -/
lemma adaptiveT3At_eventual (ϑ Q q b : ℝ)
    (hϑ0 : 0 < ϑ) (hQ : 0 ≤ Q) (hq : 0 < q)
    (hgap : 2 * q * b < 1 - ϑ / 2) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ, ∀ r : ℕ,
      0 < n → 2 ≤ r → 1 < Real.log k →
      (r : ℝ) + 1 ≤ Real.log k →
      (r : ℝ) * Real.log (Real.log k) ≤ b * Real.log k →
      adaptiveLambdaAt ϑ Q k n r ≤
        (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q) →
      adaptiveT3At ϑ Q k n r ≤ (Real.log k) ^ (-q) := by
  obtain ⟨k₀, hk₀⟩ := adaptive_third_margin_eventual ϑ Q q b hQ hq hgap
  refine ⟨k₀ + 2, fun k hk n r hn hr2 hlog1 hrplus hrM hlam => ?_⟩
  exact adaptiveT3At_le_logpow ϑ Q q k n r hϑ0 (by omega) hn hr2
    hlog1 hrplus hlam (hk₀ k (by omega) r hrM)

/-- Exact rewrite of the upstream arbitrary-`lambda` Konyagin estimate at
the selected actual adaptive scale. -/
lemma large_card_raw_adaptive_selected_at (ϑ Q : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (k : ℕ) (n : ℤ) (r : ℕ) (hkn : (k : ℤ) < n)
    (hn : 0 < n) (hk : 1 < k) (hr2 : 2 ≤ r)
    (hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ)) :
    ((badSetAt ϑ k n).card : ℝ) <
      c₆ * (k : ℝ) ^ ϑ *
        (adaptiveT1At ϑ Q k n r + adaptiveT2At ϑ Q k n r +
          adaptiveT3At ϑ Q k n r) +
        2 * (r : ℝ) * adaptiveLambdaAt ϑ Q k n r := by
  have hraw := large_card_raw_adaptive_at ϑ
    (adaptiveLambdaAt ϑ Q k n r) hϑ0 hϑ1
    (adaptiveLambdaAt_ge_one ϑ Q k n r hn (by omega))
    k n r hkn hr2 hrle
  rw [adaptive_mass_mul_lambda_pow ϑ Q k n r hk hn (by omega)] at hraw
  simpa [adaptiveT1At, adaptiveT2At, adaptiveT3At,
    ← Real.rpow_natCast] using hraw

/-- The three non-additive selected terms are uniformly negligible once
`Q>1` and `q>1`. -/
lemma adaptive_three_terms_eventual (ϑ Q q C : ℝ)
    (hQ : 1 < Q) (hq : 1 < q) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      c₆ * (k : ℝ) ^ ϑ *
        (2 * (Real.log k) ^ (-Q) + (Real.log k) ^ (-q)) ≤
      C * (k : ℝ) ^ ϑ / Real.log k := by
  obtain ⟨k₁, hk₁⟩ := Filter.eventually_atTop.mp
    (poly_log_lt_logpow (2 * c₆) ϑ (-Q) (by linarith)
      (C / 2) (by linarith))
  obtain ⟨k₂, hk₂⟩ := Filter.eventually_atTop.mp
    (poly_log_lt_logpow c₆ ϑ (-q) (by linarith)
      (C / 2) (by linarith))
  refine ⟨max k₁ k₂, fun k hk => ?_⟩
  have h₁ := hk₁ k (by omega)
  have h₂ := hk₂ k (by omega)
  calc
    c₆ * (k : ℝ) ^ ϑ *
        (2 * (Real.log k) ^ (-Q) + (Real.log k) ^ (-q)) =
      (2 * c₆) * (k : ℝ) ^ ϑ * (Real.log k) ^ (-Q) +
        c₆ * (k : ℝ) ^ ϑ * (Real.log k) ^ (-q) := by ring
    _ ≤ C / 2 * (k : ℝ) ^ ϑ / Real.log k +
        C / 2 * (k : ℝ) ^ ϑ / Real.log k := add_le_add h₁ h₂
    _ = C * (k : ℝ) ^ ϑ / Real.log k := by ring

/-- Analytic raw-to-small-count wrapper after the actual adaptive budgets
have been constructed.  It has no lower endpoint restriction on `theta`. -/
lemma adaptive_bad_set_asymptotic_of_budgets (ϑ Q q C : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hQ : 1 < Q)
    (hq : 1 < q) (hC : 0 < C) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ, ∀ r : ℕ,
      (k : ℤ) < n → 0 < n → 2 ≤ r →
      (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) →
      (r : ℝ) ≤ Real.log k →
      adaptiveT1At ϑ Q k n r ≤ (Real.log k) ^ (-Q) →
      adaptiveT2At ϑ Q k n r ≤ (Real.log k) ^ (-Q) →
      adaptiveT3At ϑ Q k n r ≤ (Real.log k) ^ (-q) →
      adaptiveLambdaAt ϑ Q k n r ≤
        (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q) →
      ((badSetAt ϑ k n).card : ℝ) <
        C * (k : ℝ) ^ ϑ / Real.log k := by
  obtain ⟨k₁, hk₁⟩ := adaptive_three_terms_eventual ϑ Q q (C / 2)
    hQ hq (by linarith)
  obtain ⟨k₂, hk₂⟩ := adaptive_additive_term_eventual ϑ Q (C / 2)
    hϑ0 (by linarith)
  refine ⟨max k₁ k₂, fun k hk n r hkn hn hr2 hrle hrlog
    hT1 hT2 hT3 hlam => ?_⟩
  have hk1 : 1 < k := by
    have hrR : (2 : ℝ) ≤ r := by exact_mod_cast hr2
    have hlog2 : (2 : ℝ) ≤ Real.log k := hrR.trans hrlog
    have hkR : (1 : ℝ) < k := by
      by_contra h
      have hk_le : (k : ℝ) ≤ 1 := le_of_not_gt h
      have hlogle : Real.log (k : ℝ) ≤ 0 :=
        Real.log_nonpos (by positivity) hk_le
      linarith
    exact_mod_cast hkR
  have hraw := large_card_raw_adaptive_selected_at ϑ Q hϑ0 hϑ1 k n r
    hkn hn hk1 hr2 hrle
  have hbracket : adaptiveT1At ϑ Q k n r + adaptiveT2At ϑ Q k n r +
      adaptiveT3At ϑ Q k n r ≤
      2 * (Real.log k) ^ (-Q) + (Real.log k) ^ (-q) := by linarith
  have hmain : c₆ * (k : ℝ) ^ ϑ *
      (adaptiveT1At ϑ Q k n r + adaptiveT2At ϑ Q k n r +
        adaptiveT3At ϑ Q k n r) ≤
      C / 2 * (k : ℝ) ^ ϑ / Real.log k := by
    have hc₆ : 0 ≤ c₆ := by
      exact (show (256 : ℝ) ≤ c₆ by
        unfold c₆ C₀_const B_const K_const c₉
        norm_num).trans' (by norm_num)
    exact (mul_le_mul_of_nonneg_left hbracket
      (mul_nonneg hc₆ (Real.rpow_nonneg (Nat.cast_nonneg k) _))).trans
      (hk₁ k (by omega))
  have hadd := hk₂ k (by omega) n r hr2 hrlog hlam
  calc
    ((badSetAt ϑ k n).card : ℝ) <
        c₆ * (k : ℝ) ^ ϑ *
          (adaptiveT1At ϑ Q k n r + adaptiveT2At ϑ Q k n r +
            adaptiveT3At ϑ Q k n r) +
          2 * (r : ℝ) * adaptiveLambdaAt ϑ Q k n r := hraw
    _ ≤ C / 2 * (k : ℝ) ^ ϑ / Real.log k +
        C / 2 * (k : ℝ) ^ ϑ / Real.log k := add_le_add hmain hadd
    _ = C * (k : ℝ) ^ ϑ / Real.log k := by ring

/-- Direct logarithmic form of the preceding conversion, used to build the
actual reference-order witness. -/
lemma adaptive_power_le_U_of_margin (ϑ Q b : ℝ)
    (k R : ℕ) (hk : 1 < k) (hlog1 : 1 ≤ Real.log k)
    (hQ : 0 ≤ Q)
    (hRM : (R : ℝ) * Real.log (Real.log k) ≤ b * Real.log k)
    (hmargin : 2 * Q * b ≤ 1 - ϑ) :
    (k : ℝ) ^ ((R : ℝ) + ϑ) ≤ adaptiveUAt Q k R := by
  have hkpos : 0 < (k : ℝ) := by positivity
  have hK : 0 < Real.log (k : ℝ) := Real.log_pos (by exact_mod_cast hk)
  have hM : 0 ≤ Real.log (Real.log (k : ℝ)) := Real.log_nonneg hlog1
  have hpenalty : Q * (2 * (R : ℝ) - 1) * Real.log (Real.log k) ≤
      (1 - ϑ) * Real.log k := by
    have hfirst : Q * (2 * (R : ℝ) - 1) * Real.log (Real.log k) ≤
        2 * Q * ((R : ℝ) * Real.log (Real.log k)) := by
      nlinarith [mul_nonneg hQ hM]
    have hsecond : 2 * Q * ((R : ℝ) * Real.log (Real.log k)) ≤
        2 * Q * (b * Real.log k) :=
      mul_le_mul_of_nonneg_left hRM (by positivity)
    have hthird : 2 * Q * b * Real.log k ≤
        (1 - ϑ) * Real.log k :=
      mul_le_mul_of_nonneg_right hmargin hK.le
    nlinarith
  rw [← Real.log_le_log_iff (Real.rpow_pos_of_pos hkpos _)
    (adaptiveUAt_pos Q k R hk), Real.log_rpow hkpos,
    log_adaptiveUAt Q k R hk]
  unfold adaptiveLogU
  nlinarith

/-- The reference order `R=r0Param a k` eventually satisfies the actual
adaptive stopping predicate. -/
lemma r0Param_eventual_adaptive_admissible_at
    (ϑ c a b Q : ℝ) (hϑ0 : 0 < ϑ) (ha : 0 < a)
    (hca : c < a) (hab : a < b) (hQ : 0 ≤ Q)
    (hmargin : 2 * Q * b ≤ 1 - ϑ) :
    ∀ᶠ k : ℕ in Filter.atTop, ∀ n : ℤ, 0 < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      (n : ℝ) * (Nat.factorial (r0Param a k) : ℝ) ≤
        adaptiveUAt Q k (r0Param a k) := by
  have hbase := r0Param_eventual_admissible_at ϑ c a b hϑ0 ha hca hab
  have hsand := r0Param_sandwich a b ha hab
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop 1
  have hL := (Real.tendsto_log_atTop.comp
    tendsto_natCast_atTop_atTop).eventually_ge_atTop 1
  filter_upwards [hbase, hsand, hM, hL, Filter.eventually_gt_atTop 1]
    with k hkbase hkR hkM hkL hk
  change 1 ≤ Real.log (Real.log k) at hkM
  intro n hn hupper
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    have hh := mul_le_mul_of_nonneg_right hkR.2.2 (le_trans zero_le_one hkM)
    field_simp at hh ⊢
    exact hh
  exact (hkbase n hn hupper).trans
    (adaptive_power_le_U_of_margin ϑ Q b k (r0Param a k) hk hkL hQ hRM hmargin)

lemma adaptiveUAt_zero (Q : ℝ) (k : ℕ) :
    adaptiveUAt Q k 0 = (k : ℝ) ^ (1 : ℝ) * (Real.log k) ^ Q := by
  norm_num [adaptiveUAt]

lemma adaptiveUAt_one (Q : ℝ) (k : ℕ) :
    adaptiveUAt Q k 1 = (k : ℝ) ^ (2 : ℝ) * (Real.log k) ^ (-Q) := by
  norm_num [adaptiveUAt]

/-- The large-range lower endpoint excludes stopping orders zero and one for
every fixed positive `theta`; no `9/23`-type restriction is used. -/
lemma adaptive_small_orders_fail_eventual (ϑ Q : ℝ) (hϑ0 : 0 < ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
      ∀ j : ℕ, j < 2 →
        adaptiveUAt Q k j < (n : ℝ) * (Nat.factorial j : ℝ) := by
  obtain ⟨k₀, hk₀⟩ := Filter.eventually_atTop.mp
    (((poly_log_lt 1 1 Q (2 + ϑ) (by linarith)
        (1 / 2) (by norm_num)).and
      (poly_log_lt 1 2 (-Q) (2 + ϑ) (by linarith)
        (1 / 2) (by norm_num))).and
      ((Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop 1))
  refine ⟨k₀ + 3, fun k hk n hlow j hj => ?_⟩
  rcases hk₀ k (by omega) with ⟨⟨hzero, hone⟩, hL1⟩
  change 1 ≤ Real.log (k : ℝ) at hL1
  have hdiv : (1 / 2) * (k : ℝ) ^ (2 + ϑ) / Real.log k ≤
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) := by
    exact div_le_self (by positivity) hL1
  have hz : adaptiveUAt Q k 0 ≤
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) := by
    rw [adaptiveUAt_zero]
    have hz' : (k : ℝ) ^ (1 : ℝ) * (Real.log k) ^ Q ≤
        (1 / 2) * (k : ℝ) ^ (2 + ϑ) / Real.log k := by
      simpa using hzero
    exact hz'.trans hdiv
  have ho : adaptiveUAt Q k 1 ≤
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) := by
    rw [adaptiveUAt_one]
    have ho' : (k : ℝ) ^ (2 : ℝ) * (Real.log k) ^ (-Q) ≤
        (1 / 2) * (k : ℝ) ^ (2 + ϑ) / Real.log k := by
      simpa using hone
    exact ho'.trans hdiv
  have hjcases : j = 0 ∨ j = 1 := by omega
  rcases hjcases with rfl | rfl
  · norm_num
    exact hz.trans_lt hlow
  · norm_num
    exact ho.trans_lt hlow

/-- Generic reference-order bounds for the adaptive construction.  Unlike
the balanced predecessor this requires no comparison `b<theta`. -/
lemma r0Param_eventual_adaptive_bounds_at (ϑ a b : ℝ)
    (hϑ1 : ϑ < 1) (ha : 0 < a) (hab : a < b) (hb1 : b < 1) :
    ∀ᶠ k : ℕ in Filter.atTop,
      1 ≤ r0Param a k ∧
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤ b * Real.log k ∧
      (r0Param a k : ℝ) + 1 ≤ Real.log k ∧
      (r0Param a k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) ∧
      1 < Real.log k := by
  have hb0 : 0 < b := ha.trans hab
  have hsand := r0Param_sandwich a b ha hab
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop 1
  have hL := (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop
    (max 2 (1 / (1 - b)))
  filter_upwards [hsand, hM, hL, eventually_log_le_half_rpow_at ϑ hϑ1]
    with k hkR hkM hkL hkpow
  change 1 ≤ Real.log (Real.log k) at hkM
  change max 2 (1 / (1 - b)) ≤ Real.log k at hkL
  have hMpos : 0 < Real.log (Real.log k) := lt_of_lt_of_le zero_lt_one hkM
  have hKpos : 0 < Real.log k := by linarith [le_trans (le_max_left _ _) hkL]
  have hXleK : Real.log k / Real.log (Real.log k) ≤ Real.log k := by
    rw [div_le_iff₀ hMpos]
    nlinarith
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    have hh := mul_le_mul_of_nonneg_right hkR.2.2 hMpos.le
    field_simp at hh ⊢
    exact hh
  have hRleK : (r0Param a k : ℝ) ≤ Real.log k := by
    calc
      (r0Param a k : ℝ) ≤ b * (Real.log k / Real.log (Real.log k)) := by
        convert hkR.2.2 using 1 <;> ring
      _ ≤ Real.log k / Real.log (Real.log k) :=
        mul_le_of_le_one_left (by positivity) hb1.le
      _ ≤ Real.log k := hXleK
  have hRplus : (r0Param a k : ℝ) + 1 ≤ Real.log k := by
    have hbig : 1 / (1 - b) ≤ Real.log k :=
      le_trans (le_max_right _ _) hkL
    rw [div_le_iff₀ (sub_pos.mpr hb1)] at hbig
    have hRbK : (r0Param a k : ℝ) ≤ b * Real.log k := by
      calc
        (r0Param a k : ℝ) ≤ b *
            (Real.log k / Real.log (Real.log k)) := by
          convert hkR.2.2 using 1 <;> ring
        _ ≤ b * Real.log k :=
          mul_le_mul_of_nonneg_left hXleK hb0.le
    nlinarith
  exact ⟨hkR.1, hRM, hRplus, hRleK.trans hkpow,
    lt_of_lt_of_le (by norm_num) (le_trans (le_max_left _ _) hkL)⟩

def AdaptiveAnalyticParameters (ϑ c : ℝ) : Prop :=
  ∃ a b Q q : ℝ,
    0 < a ∧ c < a ∧ a < b ∧ b < (1 - ϑ) / 3 ∧
    1 < Q ∧ 3 * Q * b < 1 - ϑ ∧
    1 < q ∧ 2 * q * b < 1 - ϑ / 2

/-- Feasibility of all analytic adaptive margins on the full natural
window. -/
lemma adaptiveAnalyticParameters_of_wide (ϑ c : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hc : 0 < c)
    (hcfront : c < (1 - ϑ) / 3) :
    AdaptiveAnalyticParameters ϑ c := by
  let f : ℝ := (1 - ϑ) / 3
  let a : ℝ := (c + f) / 2
  let b : ℝ := (a + f) / 2
  have hf : 0 < f := by dsimp [f]; nlinarith
  have hcf : c < f := by simpa [f] using hcfront
  have ha : 0 < a := by dsimp [a]; nlinarith
  have hca : c < a := by dsimp [a]; nlinarith
  have haf : a < f := by dsimp [a]; nlinarith
  have hab : a < b := by dsimp [b]; nlinarith
  have hbf : b < f := by dsimp [b]; nlinarith
  have hb : 0 < b := ha.trans hab
  have hthree : 3 * b < 1 - ϑ := by
    have : 3 * f = 1 - ϑ := by dsimp [f]; ring
    nlinarith
  have hQratio : 1 < (1 - ϑ) / (3 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa [mul_assoc] using hthree
  obtain ⟨Q, hQ, hQu⟩ := exists_between hQratio
  have hQmargin : 3 * Q * b < 1 - ϑ := by
    have := (lt_div_iff₀ (by positivity : 0 < 3 * b)).1 hQu
    nlinarith
  have htwo : 2 * b < 1 - ϑ / 2 := by
    have h2f : 2 * f < 1 - ϑ / 2 := by dsimp [f]; nlinarith
    nlinarith
  have hqratio : 1 < (1 - ϑ / 2) / (2 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa [mul_assoc] using htwo
  obtain ⟨q, hq, hqu⟩ := exists_between hqratio
  have hqmargin : 2 * q * b < 1 - ϑ / 2 := by
    have := (lt_div_iff₀ (by positivity : 0 < 2 * b)).1 hqu
    nlinarith
  exact ⟨a, b, Q, q, ha, hca, hab, hbf, hQ, hQmargin, hq, hqmargin⟩

def HasAdaptiveLargeCertificateAt (ϑ c Q q : ℝ) : Prop :=
  ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
    (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
    ∃ r : ℕ,
      2 ≤ r ∧
      (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) ∧
      (r : ℝ) ≤ Real.log k ∧
      adaptiveT1At ϑ Q k n r ≤ (Real.log k) ^ (-Q) ∧
      adaptiveT2At ϑ Q k n r ≤ (Real.log k) ^ (-Q) ∧
      adaptiveT3At ϑ Q k n r ≤ (Real.log k) ^ (-q) ∧
      adaptiveLambdaAt ϑ Q k n r ≤
        (k : ℝ) ^ (ϑ / (r : ℝ)) * (Real.log k) ^ (3 * Q)

/-- Full actual stopping/selection/budget certificate for the adaptive large
range. -/
lemma hasAdaptiveLargeCertificateAt_of_parameters
    (ϑ c a b Q q : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (ha : 0 < a) (hca : c < a) (hab : a < b)
    (hbf : b < (1 - ϑ) / 3)
    (hQ : 1 < Q) (hQmargin : 3 * Q * b < 1 - ϑ)
    (hq : 1 < q) (hqmargin : 2 * q * b < 1 - ϑ / 2) :
    HasAdaptiveLargeCertificateAt ϑ c Q q := by
  have hb0 : 0 < b := ha.trans hab
  have hb1 : b < 1 := by
    have hf1 : (1 - ϑ) / 3 < 1 := by nlinarith
    exact hbf.trans hf1
  have h2Q : 2 * Q * b ≤ 1 - ϑ := by
    have hQb : 0 < Q * b := mul_pos (lt_trans zero_lt_one hQ) hb0
    nlinarith
  obtain ⟨ke, he⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_adaptive_admissible_at ϑ c a b Q hϑ0 ha hca hab
      (show 0 ≤ Q by linarith [hQ]) h2Q)
  obtain ⟨ks, hs⟩ := adaptive_small_orders_fail_eventual ϑ Q hϑ0
  obtain ⟨kb, hb⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_adaptive_bounds_at ϑ a b hϑ1 ha hab hb1)
  obtain ⟨kt, ht⟩ := adaptiveT3At_eventual ϑ Q q b hϑ0
    (show 0 ≤ Q by linarith [hQ])
    (lt_trans zero_lt_one hq) hqmargin
  refine ⟨max (max ke ks) (max kb kt), fun k hk n hlow hupper => ?_⟩
  have hke : ke ≤ k := by omega
  have hks : ks ≤ k := by omega
  have hkb : kb ≤ k := by omega
  have hkt : kt ≤ k := by omega
  have hbounds := hb k hkb
  have hk1 : 1 < k := by
    have hRpos : (1 : ℝ) ≤ r0Param a k := by exact_mod_cast hbounds.1
    have hlog2 : (2 : ℝ) ≤ Real.log k := by
      linarith [hbounds.2.2.1]
    have hkR : (1 : ℝ) < k := by
      by_contra h
      have hlogle : Real.log (k : ℝ) ≤ 0 :=
        Real.log_nonpos (by positivity) (le_of_not_gt h)
      linarith
    exact_mod_cast hkR
  have hn : 0 < n := by
    have hpow : 0 ≤ (k : ℝ) ^ (2 + ϑ) := by positivity
    have hnR : 0 < (n : ℝ) := lt_of_le_of_lt (by positivity) hlow
    exact_mod_cast hnR
  have hRgood := he k hke n hn hupper
  have hsmall := hs k hks n hlow
  obtain ⟨r, hr2, hrR, hstop, hprev⟩ :=
    exists_min_adaptive_stopping_order Q k n (r0Param a k) hRgood hsmall
  have hrcast : (r : ℝ) ≤ (r0Param a k : ℝ) := by exact_mod_cast hrR
  have hMnonneg : 0 ≤ Real.log (Real.log k) := by
    exact (Real.log_pos hbounds.2.2.2.2).le
  have hrM : (r : ℝ) * Real.log (Real.log k) ≤ b * Real.log k :=
    (mul_le_mul_of_nonneg_right hrcast hMnonneg).trans hbounds.2.1
  have hrplus : (r : ℝ) + 1 ≤ Real.log k := by
    have hrplus0 : (r : ℝ) + 1 ≤ (r0Param a k : ℝ) + 1 := by
      linarith
    exact hrplus0.trans hbounds.2.2.1
  have hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - ϑ) :=
    hrcast.trans hbounds.2.2.2.1
  have hrlog : (r : ℝ) ≤ Real.log k := by
    linarith [hrplus]
  have hlower := adaptive_preceding_failure_log_lower Q k n r hk1 hn hr2 hprev
  obtain ⟨_hVZ, _hZU, _hlam1, _hmass, hT1, hT2, hlam⟩ :=
    adaptive_actual_selection_budget ϑ Q b k n r hϑ0
      (show 0 ≤ Q by linarith [hQ]) hk1
      hbounds.2.2.2.2.le hn hr2 hrM hQmargin hstop hlower
  have hT3 := ht k hkt n r hn hr2 hbounds.2.2.2.2 hrplus hrM hlam
  exact ⟨r, hr2, hrle, hrlog, hT1, hT2, hT3, hlam⟩

lemma case_large_adaptive_at (ϑ c Q q : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hQ : 1 < Q) (hq : 1 < q)
    (hPI : PrimeIntervalInput ϑ)
    (hcert : HasAdaptiveLargeCertificateAt ϑ c Q q) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      SourceIntervalConclusion ϑ k n := by
  obtain ⟨C, hC, kp, hp⟩ := hPI
  obtain ⟨ka, ha⟩ := adaptive_bad_set_asymptotic_of_budgets
    ϑ Q q C hϑ0 hϑ1 hQ hq hC
  obtain ⟨kc, hc⟩ := hcert
  refine ⟨max (max kp ka) (max kc 2), fun k hk n hlow hhigh => ?_⟩
  have hkp : kp ≤ k := by omega
  have hka : ka ≤ k := by omega
  have hkc : kc ≤ k := by omega
  have hk2 : 2 ≤ k := by omega
  have hk1 : 1 ≤ k := by omega
  have hk1' : 1 < k := by omega
  have hkR : (1 : ℝ) < (k : ℝ) := by exact_mod_cast hk1'
  have hkpow : (k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ) := by
    have hpowe : (k : ℝ) ^ (2 + ϑ) =
        (k : ℝ) ^ 2 * (k : ℝ) ^ ϑ := by
      rw [show (2 + ϑ : ℝ) = (2 : ℕ) + ϑ by norm_num,
        Real.rpow_add (by positivity), Real.rpow_natCast]
    have hone : (1 : ℝ) ≤ (k : ℝ) ^ ϑ :=
      Real.one_le_rpow hkR.le hϑ0.le
    rw [hpowe]
    have hk2R : (2 : ℝ) ≤ k := by exact_mod_cast hk2
    nlinarith [mul_nonneg (sq_nonneg (k : ℝ))
      (by linarith : (0 : ℝ) ≤ (k : ℝ) ^ ϑ - 1)]
  have hknR : (k : ℝ) < (n : ℝ) := lt_of_le_of_lt hkpow hlow
  have hkn : (k : ℤ) < n := by exact_mod_cast hknR
  have hn : 0 < n := lt_trans (by exact_mod_cast hk1) hkn
  obtain ⟨r, hr2, hrle, hrlog, hT1, hT2, hT3, hlam⟩ :=
    hc k hkc n hlow hhigh
  have hbad := ha k hka n r hkn hn hr2 hrle hrlog hT1 hT2 hT3 hlam
  have hprime : C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ) := hp k hkp
  exact konyagin_finish_at ϑ hϑ0.le k n hk1 C hprime hbad

lemma adaptiveRangePackage_of_parameters
    (ϑ c a b Q q : ℝ) (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (ha : 0 < a) (hca : c < a) (hab : a < b)
    (hbf : b < (1 - ϑ) / 3)
    (hQ : 1 < Q) (hQmargin : 3 * Q * b < 1 - ϑ)
    (hq : 1 < q) (hqmargin : 2 * q * b < 1 - ϑ / 2)
    (hPI : PrimeIntervalInput ϑ) :
    ParametricRangePackage ϑ c := by
  refine ⟨ParametricSmall.case_small ϑ hϑ0 hϑ1 hPI,
    ParametricMed.case_medium ϑ hϑ0 hϑ1 hPI,
    ParametricML.case_mediumlarge ϑ hϑ0 hϑ1 hPI, ?_⟩
  exact case_large_adaptive_at ϑ c Q q hϑ0 hϑ1 hQ hq hPI
    (hasAdaptiveLargeCertificateAt_of_parameters ϑ c a b Q q hϑ0 hϑ1
      ha hca hab hbf hQ hQmargin hq hqmargin)

/-- Full adaptive builder on the natural exponent window. -/
theorem parametricRangeBuilder_adaptive (ϑ c : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hc : 0 < c)
    (hcfront : c < (1 - ϑ) / 3) :
    ParametricRangeBuilder ϑ c := by
  intro hPI
  obtain ⟨a, b, Q, q, ha, hca, hab, hbf, hQ, hQmargin, hq, hqmargin⟩ :=
    adaptiveAnalyticParameters_of_wide ϑ c hϑ0 hϑ1 hc hcfront
  exact adaptiveRangePackage_of_parameters ϑ c a b Q q hϑ0 hϑ1 ha hca hab
    hbf hQ hQmargin hq hqmargin hPI

/-- Abstract-PI(theta) frontier theorem on the complete natural window
`0<theta<1`. -/
theorem parametric_frontier_adaptive (ϑ c : ℝ)
    (hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1) (hc : 0 < c)
    (hcfront : c < (1 - ϑ) / 3) (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  exact main_of_rangePackage ϑ c hϑ1
    (parametricRangeBuilder_adaptive ϑ c hϑ0 hϑ1 hc hcfront hPI)

/-- Kernel-checked adaptive parameter certificate on the full natural theta
window.  This theorem is deliberately a parameter result, not yet the final
analytic `ParametricRangeBuilder`. -/
theorem adaptive_parameter_certificate_wide (ϑ c : ℝ)
    (_hϑ0 : 0 < ϑ) (hϑ1 : ϑ < 1)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    AdaptiveFrontierParameters ϑ c := by
  exact adaptiveFrontierParameters_of_wide ϑ c hϑ1 hc hcfront

/-- The previously missing builder: all four source ranges, conditional only
on the abstract prime-interval input. -/
theorem parametricRangeBuilder_complete (ϑ c : ℝ)
    (hϑlo : (2 : ℝ) / 5 < ϑ) (hϑhi : ϑ < 3 / 5)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    ParametricRangeBuilder ϑ c := by
  intro hPI
  obtain ⟨a, b, q₁, q₃, ha, hca, hab, hbϑ, hq₁, hm₁, hq₃, hm₃⟩ :=
    exists_frontier_parameters_at ϑ c hϑlo hϑhi hc hcfront
  exact rangePackage_of_parameters ϑ c a b q₁ q₃ (by nlinarith [hϑlo])
    (hϑhi.trans (by norm_num)) ha hca hab hbϑ hm₁ hm₃ hq₁ hq₃ hPI

theorem parametricRangeBuilder_wide (ϑ c : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑhi : ϑ < 1)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    ParametricRangeBuilder ϑ c := by
  intro hPI
  obtain ⟨a, b, q₁, q₃, ha, hca, hab, hbϑ, hq₁, hm₁, hq₃, hm₃⟩ :=
    exists_frontier_parameters_wide ϑ c hϑlo hϑhi hc hcfront
  exact rangePackage_of_parameters ϑ c a b q₁ q₃ hϑlo hϑhi
    ha hca hab hbϑ hm₁ hm₃ hq₁ hq₃ hPI

theorem parametric_frontier_wide (ϑ c : ℝ)
    (hϑlo : (9 : ℝ) / 23 < ϑ) (hϑhi : ϑ < 1)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  exact main_of_rangePackage ϑ c hϑhi
    (parametricRangeBuilder_wide ϑ c hϑlo hϑhi hc hcfront hPI)

/-- Complete abstract-PI(theta) frontier theorem. -/
theorem parametric_frontier_complete (ϑ c : ℝ)
    (hϑlo : (2 : ℝ) / 5 < ϑ) (hϑhi : ϑ < 3 / 5)
    (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3)
    (hPI : PrimeIntervalInput ϑ) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  exact parametric_frontier_interface ϑ c hϑlo hϑhi hc hcfront hPI
    (parametricRangeBuilder_complete ϑ c hϑlo hϑhi hc hcfront)

#print axioms additiveExpAt_eq
#print axioms additiveExpAt_balanced
#print axioms additiveExpAt_le_sharp
#print axioms sharpAddExp_lt_theta
#print axioms sharpAddExp_lt_theta_iff
#print axioms balancedLargeExponent_no_go
#print axioms lamLargeAt_pow
#print axioms lamLargeAt_ge_one
#print axioms lamLargeAt_lt_exact
#print axioms lamLargeAt_lt_sharp
#print axioms large_card_raw_at
#print axioms lamLargeAt_lt_coarse
#print axioms large_term1_le_margin_at
#print axioms large_term3_le_margin_at
#print axioms large_term3_r3_at
#print axioms large_asym_of_margins_at
#print axioms eventually_log_le_half_rpow_at
#print axioms r0Param_eventual_bounds_at
#print axioms r0Param_eventual_admissible_at
#print axioms hasLargeMarginCertificateAt_of_parameters
#print axioms case_large_of_margin_certificate_at
#print axioms rangePackage_of_parameters
#print axioms parametricRangeBuilder_complete
#print axioms parametric_frontier_complete
#print axioms exists_frontier_parameters_wide
#print axioms balancedFourRangeParameters_iff
#print axioms balancedFourRange_no_go_low
#print axioms balancedFourRange_no_go_high
#print axioms large_card_raw_adaptive_at
#print axioms adaptiveFrontierParameters_of_wide
#print axioms adaptiveFrontierParameters_iff
#print axioms adaptiveLogV_le_logU
#print axioms adaptive_log_selection_budget
#print axioms adaptiveLambdaAt_pow
#print axioms adaptiveLambdaAt_ge_one
#print axioms adaptive_mass_mul_lambda_pow
#print axioms locationBlind_first_two_log_invariant
#print axioms locationBlind_first_two_invariant_ge_delta_of_W_ge_one
#print axioms locationBlind_termwise_block_budget_obstruction
#print axioms adaptive_first_two_log_invariant
#print axioms adaptive_first_two_budget_obstruction
#print axioms locationBlind_endpoint_excess_budget
#print axioms locationBlind_endpoint_termwise_no_go_of_excess
#print axioms locationBlindTermwiseLeadingCertificate_iff
#print axioms locationBlindTermwiseLeadingCertificate_no_go
#print axioms locationBlindTermwiseLeadingCertificate_no_go_bhp
#print axioms adaptive_actual_selection_budget
#print axioms exists_min_adaptive_stopping_order
#print axioms adaptive_preceding_failure_log_lower
#print axioms adaptive_additive_term_eventual
#print axioms adaptiveT3At_eventual
#print axioms large_card_raw_adaptive_selected_at
#print axioms adaptive_bad_set_asymptotic_of_budgets
#print axioms r0Param_eventual_adaptive_admissible_at
#print axioms adaptive_small_orders_fail_eventual
#print axioms r0Param_eventual_adaptive_bounds_at
#print axioms adaptiveAnalyticParameters_of_wide
#print axioms hasAdaptiveLargeCertificateAt_of_parameters
#print axioms case_large_adaptive_at
#print axioms adaptiveRangePackage_of_parameters
#print axioms parametricRangeBuilder_adaptive
#print axioms parametric_frontier_adaptive
#print axioms adaptive_parameter_certificate_wide
#print axioms parametricRangeBuilder_wide
#print axioms parametric_frontier_wide

end ParametricLarge

end
