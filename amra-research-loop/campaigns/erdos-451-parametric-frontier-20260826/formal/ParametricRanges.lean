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

end
