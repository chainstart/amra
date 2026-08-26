import ErdosProblem451

/-!
Parameter-margin lemmas for the large-`n` part of the van Doorn--Tang proof.

The fixed exponent is still the upstream `theta = 21/40`.  Instead of baking a
particular upper-range constant into the estimates, the two logarithmic error
terms are controlled by explicit strict margins `q₁ > 1` and `q₃ > 1`.
-/

noncomputable section

open scoped BigOperators Nat
open Finset Filter

/-- The balanced first Konyagin term is below `log(k)^(-q)` whenever its exact
exponent budget has the corresponding strict logarithmic margin. -/
lemma large_term1_le_margin (q : ℝ) (k r : ℕ) (hk : 1 < k) (hr3 : 3 ≤ r)
    (hlog1 : 1 < Real.log k)
    (hmargin : q * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - theta) * Real.log k) :
    (k : ℝ) ^ ((theta - 1) / (3 * (r : ℝ) - 2)) ≤
      (Real.log k) ^ (-q) := by
  have hden : 0 < 3 * (r : ℝ) - 2 := by
    have : (3 : ℝ) ≤ r := by exact_mod_cast hr3
    linarith
  rw [Real.rpow_def_of_pos (by positivity)]
  rw [show (Real.log k) ^ (-q) =
      Real.exp (Real.log (Real.log k) * (-q)) by
    rw [Real.rpow_def_of_pos (by linarith : 0 < Real.log k)]]
  apply Real.exp_le_exp.mpr
  rw [show Real.log (k : ℝ) * ((theta - 1) / (3 * (r : ℝ) - 2)) =
      (Real.log k * (theta - 1)) / (3 * (r : ℝ) - 2) by ring]
  rw [div_le_iff₀ hden]
  nlinarith

/-- For `r ≥ 4`, the third Konyagin term is below `log(k)^(-q)` under the
explicit margin `4 q r loglog(k) ≤ log(k)`. -/
lemma large_term3_le_margin (q : ℝ) (k : ℕ) (n : ℤ) (r : ℕ) (hk : 1 < k)
    (hn0 : 0 < n) (hr4 : 4 ≤ r) (hlog1 : 1 < Real.log k)
    (hmin : (k : ℝ) ^ (((r : ℝ) - 1) + theta) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ))
    (hrk : ((r : ℝ) + 1) ≤ (k : ℝ) ^ (theta / (r : ℝ)))
    (hmargin : 4 * q * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k) :
    (((r : ℝ) + 1) * lamLarge k n r / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹) ≤
      (Real.log k) ^ (-q) := by
  have h_base : ((r + 1 : ℝ) * lamLarge k n r / k) <
      (k : ℝ) ^ (2 / (r : ℝ) - 1) := by
    have h_mul : ((r + 1 : ℝ) * lamLarge k n r) <
        (k : ℝ) ^ (2 / (r : ℝ)) := by
      refine lt_of_le_of_lt
        (mul_le_mul_of_nonneg_right hrk (Real.rpow_nonneg (by positivity) _)) ?_
      convert mul_lt_mul_of_pos_left
        (lamLarge_lt k n r hn0 hk (by omega) hmin)
        (Real.rpow_pos_of_pos (Nat.cast_pos.mpr hk.le) _) using 1
      rw [← Real.rpow_add (by positivity)]
      congr 1
      field_simp
      ring
    convert (div_lt_div_iff_of_pos_right (by positivity : 0 < (k : ℝ))).2 h_mul using 1
    rw [Real.rpow_sub_one (by positivity)]
  refine le_trans (Real.rpow_le_rpow (by unfold lamLarge; positivity) h_base.le
    (by positivity)) ?_
  rw [← Real.rpow_mul (by positivity), mul_comm]
  rw [Real.rpow_def_of_pos (by positivity)]
  rw [show (Real.log k) ^ (-q) =
      Real.exp (Real.log (Real.log k) * (-q)) by
    rw [Real.rpow_def_of_pos (by linarith : 0 < Real.log k)]]
  apply Real.exp_le_exp.mpr
  field_simp
  nlinarith [show (r : ℝ) ≥ 4 by norm_cast]

/-- At the exceptional order `r=3`, retain a power saving rather than forcing
the growing-order logarithmic envelope. -/
lemma large_term3_r3_le_frontier (k : ℕ) (n : ℤ) (hk : 1 < k) (hn0 : 0 < n)
    (hmin : (k : ℝ) ^ (((3 : ℝ) - 1) + theta) <
      (n : ℝ) * (Nat.factorial (3 - 1) : ℝ))
    (hrk : ((3 : ℝ) + 1) ≤ (k : ℝ) ^ (theta / (3 : ℝ))) :
    (((3 : ℝ) + 1) * lamLarge k n 3 / (k : ℝ)) ^ ((2 * (3 : ℝ))⁻¹) ≤
      (k : ℝ) ^ (-(1 : ℝ) / 18) := by
  have h_base : (((3 : ℝ) + 1) * lamLarge k n 3 / k) <
      (k : ℝ) ^ (2 / (3 : ℝ) - 1) := by
    have h_mul : (((3 : ℝ) + 1) * lamLarge k n 3) <
        (k : ℝ) ^ (2 / (3 : ℝ)) := by
      calc
        ((3 : ℝ) + 1) * lamLarge k n 3 ≤
            (k : ℝ) ^ (theta / (3 : ℝ)) * lamLarge k n 3 :=
          mul_le_mul_of_nonneg_right hrk (by unfold lamLarge; positivity)
        _ < (k : ℝ) ^ (theta / (3 : ℝ)) *
            (k : ℝ) ^ ((2 - theta) / (3 : ℝ)) :=
          mul_lt_mul_of_pos_left (lamLarge_lt k n 3 hn0 hk (by norm_num) hmin)
            (Real.rpow_pos_of_pos (Nat.cast_pos.mpr hk.le) _)
        _ = (k : ℝ) ^ (2 / (3 : ℝ)) := by
          rw [← Real.rpow_add (by positivity)]
          congr 1
          ring
    convert (div_lt_div_iff_of_pos_right (by positivity : 0 < (k : ℝ))).2 h_mul using 1
    rw [Real.rpow_sub_one (by positivity)]
  refine le_trans (Real.rpow_le_rpow (by unfold lamLarge; positivity) h_base.le
    (by positivity)) ?_
  rw [← Real.rpow_mul (by positivity)]
  norm_num

/-- Parameterized large-range asymptotic estimate.  The fixed constants in the
old proof are replaced by two explicit strict margins `q₁>1` and `q₃>1`. -/
lemma large_asym_of_margins (q₁ q₃ C : ℝ) (hq₁ : 1 < q₁) (hq₃ : 1 < q₃)
    (hC : 0 < C) : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ, ∀ r : ℕ,
    3 ≤ r → 0 < n →
    (k : ℝ) ^ (((r : ℝ) - 1) + theta) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ) →
    q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - theta) * Real.log k →
    ((r : ℝ) + 1) ≤ (k : ℝ) ^ (theta / (r : ℝ)) →
    4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k →
    (r : ℝ) ≤ Real.log k →
    1 < Real.log k →
    c₆ * (k : ℝ) ^ theta *
        (2 * (k : ℝ) ^ ((theta - 1) / (3 * (r : ℝ) - 2)) +
          (((r : ℝ) + 1) * lamLarge k n r / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹)) +
      2 * (r : ℝ) * lamLarge k n r ≤
        C * (k : ℝ) ^ theta / Real.log k := by
  obtain ⟨k₀, hk₀⟩ : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
      2 * c₆ * (k : ℝ) ^ theta * (Real.log k) ^ (-q₁) +
      c₆ * (k : ℝ) ^ theta *
        ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) +
      2 * (k : ℝ) ^ ((2 - theta) / 3) * (Real.log k) ≤
        C * (k : ℝ) ^ theta / Real.log k := by
    obtain ⟨k₁, hk₁⟩ := Filter.eventually_atTop.mp
      (poly_log_lt_logpow (2 * c₆) theta (-q₁) (by linarith)
        (C / 3) (by linarith))
    obtain ⟨k₂a, hk₂a⟩ := Filter.eventually_atTop.mp
      (poly_log_lt_logpow c₆ theta (-q₃) (by linarith)
        (C / 6) (by linarith))
    obtain ⟨k₂b, hk₂b⟩ := Filter.eventually_atTop.mp
      (poly_log_lt c₆ (theta - 1 / 18) 0 theta (by norm_num)
        (C / 6) (by linarith))
    obtain ⟨k₃, hk₃⟩ := Filter.eventually_atTop.mp
      (poly_log_lt (2 : ℝ) ((2 - theta) / 3) 1 theta
        (by norm_num [theta]) (C / 3) (by linarith))
    refine ⟨max k₁ (max (max k₂a (k₂b + 2)) k₃), fun k hk => ?_⟩
    have hk₁' : k₁ ≤ k := by omega
    have hk₂a' : k₂a ≤ k := by omega
    have hk₂b' : k₂b ≤ k := by omega
    have hk₃' : k₃ ≤ k := by omega
    have h₁ := hk₁ k hk₁'
    have h₂a := hk₂a k hk₂a'
    have h₂b := hk₂b k hk₂b'
    have h₃ := hk₃ k hk₃'
    rw [Real.rpow_one] at h₃
    have hkpos : (0 : ℝ) < k := by norm_cast; omega
    rw [Real.rpow_zero, mul_one] at h₂b
    have hpow : c₆ * (k : ℝ) ^ theta * (k : ℝ) ^ (-(1 : ℝ) / 18) =
        c₆ * (k : ℝ) ^ (theta - 1 / 18) := by
      rw [mul_assoc, ← Real.rpow_add hkpos]
      congr 2
      ring
    rw [mul_add, hpow]
    calc
      2 * c₆ * (k : ℝ) ^ theta * (Real.log k) ^ (-q₁) +
          (c₆ * (k : ℝ) ^ theta * (Real.log k) ^ (-q₃) +
            c₆ * (k : ℝ) ^ (theta - 1 / 18)) +
          2 * (k : ℝ) ^ ((2 - theta) / 3) * Real.log k ≤
          C / 3 * (k : ℝ) ^ theta / Real.log k +
            C / 6 * (k : ℝ) ^ theta / Real.log k +
            C / 6 * (k : ℝ) ^ theta / Real.log k +
            C / 3 * (k : ℝ) ^ theta / Real.log k := by
              linarith
      _ = C * (k : ℝ) ^ theta / Real.log k := by ring
  refine ⟨k₀ + 2, fun k hk n r hr hn hmin hmargin₁ hrk hmargin₃ hrlog hlog1 => ?_⟩
  apply le_trans ?_ (hk₀ k (by omega))
  have hterm3 :
      (((r : ℝ) + 1) * lamLarge k n r / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹) ≤
        (Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18) := by
    rcases hr.eq_or_lt with rfl | hr4
    · exact (large_term3_r3_le_frontier k n (by omega) hn (by simpa using hmin)
        (by exact_mod_cast hrk)).trans (le_add_of_nonneg_left (by positivity))
    · exact (large_term3_le_margin q₃ k n r (by omega) hn hr4 hlog1
        (by convert hmin using 1) (by exact_mod_cast hrk) hmargin₃).trans
          (le_add_of_nonneg_right (by positivity))
  have hterm1 := large_term1_le_margin q₁ k r (by omega) hr
    hlog1 hmargin₁
  have hlam : lamLarge k n r < (k : ℝ) ^ ((2 - theta) / 3) := by
    refine lt_of_lt_of_le (lamLarge_lt k n r hn (by omega) hr hmin) ?_
    exact Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega) (by
      rw [div_le_div_iff₀] <;>
        nlinarith [show (r : ℝ) ≥ 3 by norm_cast, theta_pos, theta_lt_one])
  have hadd : 2 * (r : ℝ) * lamLarge k n r ≤
      2 * (k : ℝ) ^ ((2 - theta) / 3) * Real.log k := by
    have hrnonneg : (0 : ℝ) ≤ r := by positivity
    have hlamnonneg : 0 ≤ lamLarge k n r := by unfold lamLarge; positivity
    nlinarith [mul_le_mul_of_nonneg_left hlam.le hrnonneg,
      mul_le_mul_of_nonneg_right hrlog hlamnonneg]
  have hc6 : 0 ≤ c₆ := c₆_pos.le
  have hbracket :
      2 * (k : ℝ) ^ ((theta - 1) / (3 * (r : ℝ) - 2)) +
          (((r : ℝ) + 1) * lamLarge k n r / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹) ≤
        2 * (Real.log k) ^ (-q₁) +
          ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) :=
    add_le_add (mul_le_mul_of_nonneg_left hterm1 zero_le_two) hterm3
  calc
    c₆ * (k : ℝ) ^ theta *
          (2 * (k : ℝ) ^ ((theta - 1) / (3 * (r : ℝ) - 2)) +
            (((r : ℝ) + 1) * lamLarge k n r / (k : ℝ)) ^ ((2 * (r : ℝ))⁻¹)) +
        2 * (r : ℝ) * lamLarge k n r ≤
      c₆ * (k : ℝ) ^ theta *
          (2 * (Real.log k) ^ (-q₁) +
            ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18))) +
        2 * (k : ℝ) ^ ((2 - theta) / 3) * Real.log k :=
      add_le_add
        (mul_le_mul_of_nonneg_left hbracket
          (mul_nonneg hc6 (Real.rpow_nonneg (Nat.cast_nonneg _) _))) hadd
    _ = 2 * c₆ * (k : ℝ) ^ theta * (Real.log k) ^ (-q₁) +
        c₆ * (k : ℝ) ^ theta *
          ((Real.log k) ^ (-q₃) + (k : ℝ) ^ (-(1 : ℝ) / 18)) +
        2 * (k : ℝ) ^ ((2 - theta) / 3) * Real.log k := by ring

/-- A reusable strict-margin certificate for the least-order argument.  It is
the exact interface needed to turn a real upper-range constant `c` into the
parameterized Konyagin estimate. -/
def HasLargeMarginCertificate (c q₁ q₃ : ℝ) : Prop :=
  ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (1 / 2) * (k : ℝ) ^ (2 + theta) < (n : ℝ) →
    (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
    ∃ r : ℕ,
      3 ≤ r ∧
      (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - theta) ∧
      (n : ℝ) * (Nat.factorial r : ℝ) ≤ (k : ℝ) ^ ((r : ℝ) + theta) ∧
      (k : ℝ) ^ (((r : ℝ) - 1) + theta) <
        (n : ℝ) * (Nat.factorial (r - 1) : ℝ) ∧
      q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - theta) * Real.log k ∧
      ((r : ℝ) + 1) ≤ (k : ℝ) ^ (theta / (r : ℝ)) ∧
      4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k ∧
      (r : ℝ) ≤ Real.log k ∧
      1 < Real.log k

/-- The large range follows from any strict-margin certificate, uniformly in
the real constant `c`. -/
lemma case_large_of_margin_certificate (c q₁ q₃ : ℝ) (hq₁ : 1 < q₁)
    (hq₃ : 1 < q₃) (hcert : HasLargeMarginCertificate c q₁ q₃) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      (1 / 2) * (k : ℝ) ^ (2 + theta) < (n : ℝ) →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧
        (p : ℝ) < (k : ℝ) + 3 * (k : ℝ) ^ theta ∧
        (p : ℤ) ∣ Pprod k n := by
  obtain ⟨C, hC, kb, hb⟩ := bhp
  obtain ⟨ka, hasym⟩ := large_asym_of_margins q₁ q₃ C hq₁ hq₃ hC
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
  have hkpow : (k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + theta) := by
    have hpowe : (k : ℝ) ^ (2 + theta) =
        (k : ℝ) ^ 2 * (k : ℝ) ^ theta := by
      rw [show (2 + theta : ℝ) = (2 : ℕ) + theta by norm_num,
        Real.rpow_add (by linarith), Real.rpow_natCast]
    have hone : (1 : ℝ) ≤ (k : ℝ) ^ theta :=
      Real.one_le_rpow hkR.le theta_pos.le
    rw [hpowe]
    have hk2R : (2 : ℝ) ≤ k := by exact_mod_cast hk2
    nlinarith [mul_nonneg (sq_nonneg (k : ℝ)) (by linarith :
      (0 : ℝ) ≤ (k : ℝ) ^ theta - 1)]
  have hknR : (k : ℝ) < (n : ℝ) := lt_of_le_of_lt hkpow hlow
  have hkn : (k : ℤ) < n := by exact_mod_cast hknR
  have hn0 : 0 < n := lt_trans (by exact_mod_cast hk1) hkn
  obtain ⟨r, hr3, hrle, hub, hmin, hm1, hrk, hm3, hrlog, hlog1⟩ :=
    hrdata k hkr n hlow hhigh
  have hraw := large_card_raw k n r hk1' hn0 hr3 hrle hkn hub
  have hbnd := hasym k hka n r hr3 hn0 hmin hm1 hrk hm3 hrlog hlog1
  have hbhp : C * (k : ℝ) ^ theta / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ theta) : ℝ) := hb k hkb
  exact konyagin_finish k n hk1 C hbhp (lt_of_lt_of_le hraw hbnd)

/-- Full source range, still ending first in the source interval
`(k,k+3k^theta)`, from a strict-margin certificate. -/
theorem main_theorem_of_margin_certificate_short (c q₁ q₃ : ℝ)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃)
    (hcert : HasLargeMarginCertificate c q₁ q₃) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧
        (p : ℝ) < (k : ℝ) + 3 * (k : ℝ) ^ theta ∧
        (p : ℤ) ∣ Pprod k n := by
  obtain ⟨k1, h1⟩ := case_small
  obtain ⟨k2, h2⟩ := case_medium
  obtain ⟨k3, h3⟩ := case_mediumlarge
  obtain ⟨k4, h4⟩ := case_large_of_margin_certificate c q₁ q₃ hq₁ hq₃ hcert
  refine ⟨max (max k1 k2) (max k3 k4), ?_⟩
  intro k hk n hn1 hn2
  have hk1 : k1 ≤ k := by omega
  have hk2 : k2 ≤ k := by omega
  have hk3 : k3 ≤ k := by omega
  have hk4 : k4 ≤ k := by omega
  by_cases c1 : (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 - theta)
  · exact h1 k hk1 n hn1 c1
  · push_neg at c1
    by_cases c2 : (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2
    · exact h2 k hk2 n c1 c2
    · push_neg at c2
      by_cases c3 : (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + theta)
      · exact h3 k hk3 n c2 c3
      · push_neg at c3
        exact h4 k hk4 n c3 hn2

/-- A strict-margin certificate gives the exact `(k,2k)` conclusion used in
Erdős problem 451, for an arbitrary real upper-range constant `c`. -/
theorem main_theorem_of_margin_certificate (c q₁ q₃ : ℝ)
    (hq₁ : 1 < q₁) (hq₃ : 1 < q₃)
    (hcert : HasLargeMarginCertificate c q₁ q₃) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  obtain ⟨k₁, hmain⟩ :=
    main_theorem_of_margin_certificate_short c q₁ q₃ hq₁ hq₃ hcert
  obtain ⟨k₂, hpow⟩ := Filter.eventually_atTop.mp
    (eventually_le_rpow (1 - theta) 3 (by norm_num [theta]))
  refine ⟨max (max k₁ k₂) 2, ?_⟩
  intro k hk n hn hupper
  have hk₁ : k₁ ≤ k := by omega
  have hk₂ : k₂ ≤ k := by omega
  have hkpos : (0 : ℝ) < k := by norm_cast; omega
  obtain ⟨p, hp, hpk, hpupper, hpdvd⟩ := hmain k hk₁ n hn hupper
  refine ⟨p, hp, hpk, ?_, hpdvd⟩
  have hscale : 3 * (k : ℝ) ^ theta ≤ (k : ℝ) := by
    calc
      3 * (k : ℝ) ^ theta ≤ (k : ℝ) ^ (1 - theta) * (k : ℝ) ^ theta :=
        mul_le_mul_of_nonneg_right (hpow k hk₂)
          (Real.rpow_nonneg (Nat.cast_nonneg k) _)
      _ = (k : ℝ) := by
        rw [← Real.rpow_add hkpos]
        ring_nf
        rw [Real.rpow_one]
  linarith

/-- Reference order with an arbitrary real coefficient `a`. -/
def r0Param (a : ℝ) (k : ℕ) : ℕ :=
  ⌈a * Real.log k / Real.log (Real.log k)⌉₊

/-- The parameterized reference order is eventually squeezed between
`a log(k)/loglog(k)` and `b log(k)/loglog(k)` for every `0<a<b`. -/
lemma r0Param_sandwich (a b : ℝ) (ha : 0 < a) (hab : a < b) :
    ∀ᶠ k : ℕ in Filter.atTop,
      1 ≤ r0Param a k ∧
      a * Real.log k / Real.log (Real.log k) ≤ (r0Param a k : ℝ) ∧
      (r0Param a k : ℝ) ≤ b * Real.log k / Real.log (Real.log k) := by
  have hba : 0 < b - a := sub_pos.mpr hab
  have hX := tendsto_log_div_loglog_atTop.eventually_ge_atTop
    (max 1 (1 / (b - a)))
  filter_upwards [hX] with k hk
  have hXpos : 0 < Real.log k / Real.log (Real.log k) :=
    lt_of_lt_of_le zero_lt_one (le_trans (le_max_left _ _) hk)
  have hargpos : 0 < a * Real.log k / Real.log (Real.log k) := by
    have : a * (Real.log k / Real.log (Real.log k)) =
        a * Real.log k / Real.log (Real.log k) := by ring
    rw [← this]
    positivity
  have hlower : a * Real.log k / Real.log (Real.log k) ≤
      (r0Param a k : ℝ) := by
    exact Nat.le_ceil _
  have hceil : (r0Param a k : ℝ) <
      a * Real.log k / Real.log (Real.log k) + 1 := by
    exact Nat.ceil_lt_add_one hargpos.le
  have hgap : 1 ≤ (b - a) *
      (Real.log k / Real.log (Real.log k)) := by
    have hxgap : 1 / (b - a) ≤
        Real.log k / Real.log (Real.log k) := le_trans (le_max_right _ _) hk
    rw [div_le_iff₀ hba] at hxgap
    nlinarith
  have hupper : (r0Param a k : ℝ) ≤
      b * Real.log k / Real.log (Real.log k) := by
    have haform : a * Real.log k / Real.log (Real.log k) =
        a * (Real.log k / Real.log (Real.log k)) := by ring
    have hbform : b * Real.log k / Real.log (Real.log k) =
        b * (Real.log k / Real.log (Real.log k)) := by ring
    rw [hbform]
    nlinarith
  exact ⟨Nat.ceil_pos.mpr hargpos, hlower, hupper⟩

/-- `log k` is eventually below the derivative-admissibility power used by
Theorem 4.1. -/
lemma eventually_log_le_half_rpow :
    ∀ᶠ k : ℕ in Filter.atTop,
      Real.log k ≤ (1 / 2) * (k : ℝ) ^ (1 - theta) := by
  have hsmall := isLittleO_log_rpow_atTop
    (show (0 : ℝ) < 1 - theta by norm_num [theta])
  rw [Asymptotics.isLittleO_iff] at hsmall
  obtain ⟨x₀, hx₀⟩ := Filter.eventually_atTop.mp
    (hsmall (show (0 : ℝ) < 1 / 2 by norm_num))
  refine Filter.eventually_atTop.mpr ⟨⌈x₀⌉₊ + 2, fun k hk => ?_⟩
  have hxk : x₀ ≤ (k : ℝ) := by
    have hceil : x₀ ≤ (⌈x₀⌉₊ : ℝ) := Nat.le_ceil x₀
    exact hceil.trans (by exact_mod_cast (show ⌈x₀⌉₊ ≤ k by omega))
  have hk2 : 2 ≤ k := by omega
  have h := hx₀ k hxk
  rw [Real.norm_of_nonneg (Real.log_nonneg (by norm_cast; omega)),
    Real.norm_of_nonneg (Real.rpow_nonneg (Nat.cast_nonneg _) _)] at h
  exact h

/-- All geometric and logarithmic margin bounds for the parameterized
reference order. -/
lemma r0Param_eventual_bounds (a b q₁ q₃ : ℝ) (ha : 0 < a) (hab : a < b)
    (hbtheta : b < theta) (hm1 : 3 * q₁ * b < 1 - theta)
    (hm3 : 4 * q₃ * b < 1) (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) :
    ∀ᶠ k : ℕ in Filter.atTop,
      1 ≤ r0Param a k ∧
      (r0Param a k : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - theta) ∧
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - theta) * Real.log k ∧
      ((r0Param a k : ℝ) + 1) ≤
        (k : ℝ) ^ (theta / (r0Param a k : ℝ)) ∧
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) ≤ Real.log k ∧
      (r0Param a k : ℝ) ≤ Real.log k ∧
      1 < Real.log k := by
  have htheta1 : theta < 1 := theta_lt_one
  have hb0 : 0 < b := ha.trans hab
  have hb1 : b < 1 := hbtheta.trans htheta1
  have hsand := r0Param_sandwich a b ha hab
  have hM := (Real.tendsto_log_atTop.comp
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)).eventually_ge_atTop
      (max 1 b)
  have hL := (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop
    (max 2 (1 / (1 - b)))
  filter_upwards [hsand, hM, hL, eventually_log_le_half_rpow]
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
      (1 / 2) * (k : ℝ) ^ (1 - theta) := hRlog.trans hkpow
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    calc
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
          (b * Real.log k / Real.log (Real.log k)) *
            Real.log (Real.log k) :=
        mul_le_mul_of_nonneg_right hRb hMpos.le
      _ = b * Real.log k := by field_simp
  have hmargin1 :
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        (1 - theta) * Real.log k := by
    have hthree : (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) ≤
        3 * ((r0Param a k : ℝ) * Real.log (Real.log k)) := by
      nlinarith
    calc
      q₁ * (3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k) =
          q₁ * ((3 * (r0Param a k : ℝ) - 2) * Real.log (Real.log k)) := by ring
      _ ≤ q₁ * (3 * ((r0Param a k : ℝ) * Real.log (Real.log k))) :=
        mul_le_mul_of_nonneg_left hthree (by linarith)
      _ ≤ q₁ * (3 * (b * Real.log k)) :=
        mul_le_mul_of_nonneg_left
          (mul_le_mul_of_nonneg_left hRM (by norm_num)) (by linarith)
      _ = (3 * q₁ * b) * Real.log k := by ring
      _ ≤ (1 - theta) * Real.log k :=
        mul_le_mul_of_nonneg_right hm1.le hLpos.le
  have hmargin3 :
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) ≤ Real.log k := by
    calc
      4 * q₃ * (r0Param a k : ℝ) * Real.log (Real.log k) =
          (4 * q₃) * ((r0Param a k : ℝ) * Real.log (Real.log k)) := by ring
      _ ≤ (4 * q₃) * (b * Real.log k) :=
        mul_le_mul_of_nonneg_left hRM (by positivity)
      _ = (4 * q₃ * b) * Real.log k := by ring
      _ ≤ 1 * Real.log k := mul_le_mul_of_nonneg_right hm3.le hLpos.le
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
      theta * Real.log k / (r0Param a k : ℝ) := by
    apply (le_div_iff₀ hRpos).2
    calc
      Real.log (Real.log k) * (r0Param a k : ℝ) =
          (r0Param a k : ℝ) * Real.log (Real.log k) := by ring
      _ ≤ b * Real.log k := hRM
      _ ≤ theta * Real.log k :=
        mul_le_mul_of_nonneg_right hbtheta.le hLpos.le
  have hLrpow : Real.log k ≤
      (k : ℝ) ^ (theta / (r0Param a k : ℝ)) := by
    have hkpos : (0 : ℝ) < k := by
      by_contra h
      have hkzero : (k : ℝ) = 0 := le_antisymm (le_of_not_gt h) (Nat.cast_nonneg k)
      rw [hkzero, Real.log_zero] at hLpos
      linarith
    calc
      Real.log k = Real.exp (Real.log (Real.log k)) := by
        rw [Real.exp_log hLpos]
      _ ≤ Real.exp (theta * Real.log k / (r0Param a k : ℝ)) :=
        Real.exp_le_exp.mpr harg
      _ = (k : ℝ) ^ (theta / (r0Param a k : ℝ)) := by
        rw [Real.rpow_def_of_pos hkpos]
        congr 1
        ring
  exact ⟨hR1, hRpow, hmargin1, hRplus.trans hLrpow, hmargin3, hRlog, by linarith⟩

/-- The parameterized reference order absorbs both the upper range
`exp(c log²(k)/loglog(k))` and the factorial whenever `c<a<b`. -/
lemma r0Param_eventual_admissible (c a b : ℝ) (ha : 0 < a) (hca : c < a)
    (hab : a < b) :
    ∀ᶠ k : ℕ in Filter.atTop, ∀ n : ℤ, 0 < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      (n : ℝ) * (Nat.factorial (r0Param a k) : ℝ) ≤
        (k : ℝ) ^ ((r0Param a k : ℝ) + theta) := by
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
  have hM1 : 1 ≤ Real.log (Real.log k) := le_trans (le_max_left _ _) hkM
  have hbM : b ≤ Real.log (Real.log k) := le_trans (le_max_right _ _) hkM
  have hMpos : 0 < Real.log (Real.log k) := by linarith
  have hXnonneg : 0 ≤ Real.log k / Real.log (Real.log k) := by positivity
  have hXleL : Real.log k / Real.log (Real.log k) ≤ Real.log k := by
    rw [div_le_iff₀ hMpos]
    nlinarith
  have hb0 : 0 < b := ha.trans hab
  have hratio : b * Real.log k / Real.log (Real.log k) ≤ Real.log k := by
    rw [div_le_iff₀ hMpos]
    simpa [mul_comm] using mul_le_mul_of_nonneg_left hbM hLpos.le
  have hRlog : (r0Param a k : ℝ) ≤ Real.log k := hRb.trans hratio
  have hRM : (r0Param a k : ℝ) * Real.log (Real.log k) ≤
      b * Real.log k := by
    calc
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
          (b * Real.log k / Real.log (Real.log k)) *
            Real.log (Real.log k) :=
        mul_le_mul_of_nonneg_right hRb hMpos.le
      _ = b * Real.log k := by field_simp
  have hgap0 : b ≤ (a - c) *
      (Real.log k / Real.log (Real.log k)) := by
    rw [div_le_iff₀ hac] at hkX
    nlinarith
  have hgap : b * Real.log k ≤
      (a - c) * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by
    have := mul_le_mul_of_nonneg_right hgap0 hLpos.le
    calc
      b * Real.log k ≤
          ((a - c) * (Real.log k / Real.log (Real.log k))) * Real.log k := this
      _ = (a - c) * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by ring
  have haR : a * ((Real.log k) ^ 2 / Real.log (Real.log k)) ≤
      (r0Param a k : ℝ) * Real.log k := by
    have := mul_le_mul_of_nonneg_right hRa hLpos.le
    calc
      a * ((Real.log k) ^ 2 / Real.log (Real.log k)) =
          (a * Real.log k / Real.log (Real.log k)) * Real.log k := by ring
      _ ≤ (r0Param a k : ℝ) * Real.log k := this
  have hbudget : c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
      (r0Param a k : ℝ) * Real.log (Real.log k) ≤
        (r0Param a k : ℝ) * Real.log k := by
    calc
      c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
          (r0Param a k : ℝ) * Real.log (Real.log k) ≤
        c * ((Real.log k) ^ 2 / Real.log (Real.log k)) + b * Real.log k :=
          by nlinarith [hRM]
      _ ≤ a * ((Real.log k) ^ 2 / Real.log (Real.log k)) := by
        nlinarith
      _ ≤ (r0Param a k : ℝ) * Real.log k := haR
  have hlogn : Real.log (n : ℝ) ≤
      c * (Real.log k) ^ 2 / Real.log (Real.log k) := by
    exact Real.log_le_iff_le_exp (by positivity) |>.2 hupper
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
        (r0Param a k : ℝ) * Real.log k + theta * Real.log k := by
    have htheta_nonneg : 0 ≤ theta * Real.log k :=
      mul_nonneg theta_pos.le hLpos.le
    calc
      Real.log (n : ℝ) + Real.log (Nat.factorial (r0Param a k) : ℝ) ≤
          c * ((Real.log k) ^ 2 / Real.log (Real.log k)) +
            (r0Param a k : ℝ) * Real.log (Real.log k) := by
              apply add_le_add _ hfac
              simpa [div_eq_mul_inv, mul_assoc] using hlogn
      _ ≤ (r0Param a k : ℝ) * Real.log k := hbudget
      _ ≤ (r0Param a k : ℝ) * Real.log k + theta * Real.log k :=
        le_add_of_nonneg_right htheta_nonneg
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

/-- Strict parameter inequalities produce the reusable least-order
certificate.  The chosen order is the least `r` satisfying the Konyagin
factorial inequality; the reference order `r0Param a k` is used only to prove
that this set is nonempty and to transfer the asymptotic margins. -/
lemma hasLargeMarginCertificate_of_parameters (c a b q₁ q₃ : ℝ)
    (ha : 0 < a) (hca : c < a) (hab : a < b)
    (hbtheta : b < theta) (hm1 : 3 * q₁ * b < 1 - theta)
    (hm3 : 4 * q₃ * b < 1) (hq₁ : 1 < q₁) (hq₃ : 1 < q₃) :
    HasLargeMarginCertificate c q₁ q₃ := by
  obtain ⟨kb, hb⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_bounds a b q₁ q₃ ha hab hbtheta hm1 hm3 hq₁ hq₃)
  obtain ⟨kp, hp⟩ := Filter.eventually_atTop.mp
    (r0Param_eventual_admissible c a b ha hca hab)
  refine ⟨max (max kb kp) 2, ?_⟩
  intro k hk n hlow hupper
  have hkb : kb ≤ k := by omega
  have hkp : kp ≤ k := by omega
  have hk2 : 2 ≤ k := by omega
  have hkpos : (0 : ℝ) < k := by norm_cast; omega
  have hn0 : 0 < n := by
    have hpow0 : (0 : ℝ) ≤ (k : ℝ) ^ (2 + theta) := by positivity
    have : (0 : ℝ) < (n : ℝ) := lt_of_le_of_lt (by positivity) hlow
    exact_mod_cast this
  have hP0 : (n : ℝ) * (Nat.factorial (r0Param a k) : ℝ) ≤
      (k : ℝ) ^ ((r0Param a k : ℝ) + theta) := hp k hkp n hn0 hupper
  let hExists : ∃ r : ℕ, (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + theta) := ⟨r0Param a k, hP0⟩
  let r : ℕ := Nat.find hExists
  have hrle0 : r ≤ r0Param a k := Nat.find_min' hExists hP0
  have hspec : (n : ℝ) * (Nat.factorial r : ℝ) ≤
      (k : ℝ) ^ ((r : ℝ) + theta) := Nat.find_spec hExists
  have hb0 := hb k hkb
  have hr3 : 3 ≤ r := by
    by_contra hrnot
    have hr : r < 3 := Nat.lt_of_not_ge hrnot
    have hcases : r = 0 ∨ r = 1 ∨ r = 2 := by omega
    rcases hcases with h0 | h1 | h2
    · rw [h0] at hspec
      norm_num at hspec
      have hfactor : (k : ℝ) ^ (2 + theta) =
          (k : ℝ) ^ theta * (k : ℝ) ^ 2 := by
        rw [show (2 + theta : ℝ) = theta + 2 by ring,
          Real.rpow_add hkpos]
        norm_num
      rw [hfactor] at hlow
      have hkpow2 : (2 : ℝ) ≤ (k : ℝ) ^ 2 := by
        have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk2
        nlinarith [sq_nonneg ((k : ℝ) - 2)]
      have hprod : 0 ≤ (k : ℝ) ^ theta * ((k : ℝ) ^ 2 - 2) :=
        mul_nonneg (Real.rpow_nonneg (Nat.cast_nonneg k) _) (sub_nonneg.mpr hkpow2)
      nlinarith
    · rw [h1] at hspec
      norm_num at hspec
      have hfactor : (k : ℝ) ^ (2 + theta) =
          (k : ℝ) ^ (1 + theta) * (k : ℝ) := by
        rw [show (2 + theta : ℝ) = (1 + theta) + 1 by ring,
          Real.rpow_add hkpos]
        norm_num
      rw [hfactor] at hlow
      have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk2
      have hprod : 0 ≤ (k : ℝ) ^ (1 + theta) * ((k : ℝ) - 2) :=
        mul_nonneg (Real.rpow_nonneg (Nat.cast_nonneg k) _) (sub_nonneg.mpr hkR)
      nlinarith
    · rw [h2] at hspec
      norm_num at hspec
      nlinarith
  have hrpos : (0 : ℝ) < r := by exact_mod_cast (show 0 < r by omega)
  have hmin : (k : ℝ) ^ (((r : ℝ) - 1) + theta) <
      (n : ℝ) * (Nat.factorial (r - 1) : ℝ) := by
    have hrsub : r - 1 < r := Nat.sub_lt (by omega) zero_lt_one
    have hnot := Nat.find_min hExists hrsub
    push_neg at hnot
    convert hnot using 2
    rw [Nat.cast_sub (by omega)]
    norm_num
  have hrcast : (r : ℝ) ≤ (r0Param a k : ℝ) := by exact_mod_cast hrle0
  have hrle : (r : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (1 - theta) :=
    hrcast.trans hb0.2.1
  have hmargin1 : q₁ * (3 * (r : ℝ) - 2) * Real.log (Real.log k) ≤
      (1 - theta) * Real.log k := by
    have hMnonneg : 0 ≤ Real.log (Real.log k) :=
      (Real.log_pos hb0.2.2.2.2.2.2).le
    have hbase : 3 * (r : ℝ) - 2 ≤ 3 * (r0Param a k : ℝ) - 2 := by
      nlinarith
    exact (mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hbase (le_trans zero_le_one hq₁.le)) hMnonneg).trans
        hb0.2.2.1
  have hrk : (r : ℝ) + 1 ≤ (k : ℝ) ^ (theta / (r : ℝ)) := by
    calc
      (r : ℝ) + 1 ≤ (r0Param a k : ℝ) + 1 := by linarith
      _ ≤ (k : ℝ) ^ (theta / (r0Param a k : ℝ)) := hb0.2.2.2.1
      _ ≤ (k : ℝ) ^ (theta / (r : ℝ)) := by
        apply Real.rpow_le_rpow_of_exponent_le (by norm_cast; omega)
        exact div_le_div_of_nonneg_left theta_pos.le hrpos hrcast
  have hmargin3 : 4 * q₃ * (r : ℝ) * Real.log (Real.log k) ≤ Real.log k := by
    have hMnonneg : 0 ≤ Real.log (Real.log k) :=
      (Real.log_pos hb0.2.2.2.2.2.2).le
    exact (mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hrcast (by positivity)) hMnonneg).trans
        hb0.2.2.2.2.1
  have hrlog : (r : ℝ) ≤ Real.log k := hrcast.trans hb0.2.2.2.2.2.1
  exact ⟨r, hr3, hrle, hspec, hmin, hmargin1, hrk, hmargin3,
    hrlog, hb0.2.2.2.2.2.2⟩

/-- Every constant below the exact BHP frontier admits auxiliary coefficients
with strict slack in both analytic error terms. -/
lemma exists_frontier_parameters (c : ℝ) (hc : 0 < c) (hcfront : c < 19 / 120) :
    ∃ a b q₁ q₃ : ℝ,
      0 < a ∧ c < a ∧ a < b ∧ b < theta ∧
      1 < q₁ ∧ 3 * q₁ * b < 1 - theta ∧
      1 < q₃ ∧ 4 * q₃ * b < 1 := by
  let f : ℝ := 19 / 120
  let a : ℝ := (c + f) / 2
  let b : ℝ := (a + f) / 2
  have hf : f = 19 / 120 := rfl
  have hfpos : 0 < f := by norm_num [f]
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
  have hbtheta : b < theta := by
    exact hbf.trans (by norm_num [f, theta])
  have hthree : 3 * b < 1 - theta := by
    have : 3 * f = 1 - theta := by norm_num [f, theta]
    nlinarith
  have hfour : 4 * b < 1 := by
    have : 4 * f < (1 : ℝ) := by norm_num [f]
    nlinarith
  have hratio1 : 1 < (1 - theta) / (3 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa [mul_assoc] using hthree
  obtain ⟨q₁, hq₁, hq₁u⟩ := exists_between hratio1
  have hm1 : 3 * q₁ * b < 1 - theta := by
    have := (lt_div_iff₀ (by positivity : 0 < 3 * b)).1 hq₁u
    nlinarith
  have hratio3 : 1 < 1 / (4 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa using hfour
  obtain ⟨q₃, hq₃, hq₃u⟩ := exists_between hratio3
  have hm3 : 4 * q₃ * b < 1 := by
    have := (lt_div_iff₀ (by positivity : 0 < 4 * b)).1 hq₃u
    nlinarith
  exact ⟨a, b, q₁, q₃, ha, hca, hab, hbtheta, hq₁, hm1, hq₃, hm3⟩

/-- **Parameterized BHP frontier for Erdős problem 451.**  For every fixed
real `c < 19/120`, all sufficiently large `k` and every integer in the stated
exponential range have a prime divisor of the consecutive product in
`(k,2k)`.  The sole number-theoretic oracle is the upstream BHP input at
`theta = 21/40`. -/
theorem erdos451_bhp_frontier (c : ℝ) (hc : 0 < c) (hcfront : c < 19 / 120) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  obtain ⟨a, b, q₁, q₃, ha, hca, hab, hbtheta, hq₁, hm1, hq₃, hm3⟩ :=
    exists_frontier_parameters c hc hcfront
  exact main_theorem_of_margin_certificate c q₁ q₃ hq₁ hq₃
    (hasLargeMarginCertificate_of_parameters c a b q₁ q₃
      ha hca hab hbtheta hm1 hm3 hq₁ hq₃)

#print axioms large_term1_le_margin
#print axioms large_term3_le_margin
#print axioms large_asym_of_margins
#print axioms main_theorem_of_margin_certificate
#print axioms erdos451_bhp_frontier

end
