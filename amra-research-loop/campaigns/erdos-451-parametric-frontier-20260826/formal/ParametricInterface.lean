import FrontierLemmas

/-!
A theta-parameterized interface around the fixed-exponent upstream proof.

The upstream analytic theorem `konyagin_application` is already parameterized
by its exponent, but `bhp`, `badSet`, and all four range lemmas use the global
constant `theta = 21/40`.  This file extracts the exponent-independent prime
pigeonhole bridge and the exact four-range composition contract.  It does not
postulate a short-prime theorem at new exponents.
-/

noncomputable section

open scoped BigOperators Nat
open Finset Filter

/-- Abstract short-prime input at exponent `ϑ`.  This is a definition, not an
axiom. -/
def PrimeIntervalInput (ϑ : ℝ) : Prop :=
  ∃ C : ℝ, 0 < C ∧ ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k →
    C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ)

/-- The sole upstream number-theoretic axiom has exponent exactly `21/40`. -/
lemma bhp_primeIntervalInput : PrimeIntervalInput theta := bhp

/-- Bad integers for an arbitrary exponent. -/
def badSetAt (ϑ : ℝ) (k : ℕ) (n : ℤ) : Finset ℤ :=
  (Finset.Ioo (k : ℤ) ((k : ℤ) + ⌊(k : ℝ) ^ ϑ⌋ + 2)).filter
    (fun m : ℤ => (m : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ ∧
      |(n : ℝ) / (m : ℝ) - round ((n : ℝ) / (m : ℝ))| <
        1 / (k : ℝ) ^ (1 - ϑ))

/-- The old fixed bad set is definitionally the new one at `theta`. -/
lemma badSetAt_theta (k : ℕ) (n : ℤ) : badSetAt theta k n = badSet k n := rfl

/-- The elementary divisor bridge is valid for every nonnegative exponent;
no short-prime theorem is used here. -/
lemma dvd_from_far_at (ϑ : ℝ) (hϑ0 : 0 ≤ ϑ) (k : ℕ) (n : ℤ) (p : ℕ)
    (hk1 : 1 ≤ k) (hp0 : 0 < p)
    (hkp : (k : ℝ) < p) (hpk : (p : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ)
    (hfar : 1 / (k : ℝ) ^ (1 - ϑ) ≤
      |(n : ℝ) / (p : ℝ) - round ((n : ℝ) / (p : ℝ))|) :
    (p : ℤ) ∣ Pprod k n := by
  set i := n % (p : ℤ)
  set j := i.toNat
  have hj : (j : ℤ) = i := by
    exact Int.toNat_of_nonneg <| Int.emod_nonneg _ <| by positivity
  have h_frac : (p : ℝ) / (k : ℝ) ^ (1 - ϑ) ≤
      min (i : ℝ) ((p : ℝ) - i) := by
    have h_frac : |(n : ℝ) / p - round ((n : ℝ) / p)| =
        min ((i : ℝ) / p) (1 - (i : ℝ) / p) := by
      have hfract : Int.fract ((n : ℝ) / p) = (i : ℝ) / p := by
        rw [Int.fract_eq_iff]
        field_simp
        norm_cast
        exact ⟨by norm_num; exact Int.emod_nonneg _ (by positivity),
          Int.emod_lt_of_pos _ (by positivity), n / p,
          by linarith [Int.emod_add_mul_ediv n p]⟩
      rw [← hfract, abs_sub_round_eq_min]
    convert mul_le_mul_of_nonneg_left hfar (Nat.cast_nonneg p) using 1 <;>
      push_cast [h_frac] <;> ring_nf
    rw [mul_min_of_nonneg _ _ (by positivity), mul_sub, mul_one,
      mul_left_comm, mul_inv_cancel₀ (by positivity), mul_one]
  have h_i_bounds : 1 ≤ i ∧ i ≤ k := by
    have hratio : (p : ℝ) / (k : ℝ) ^ (1 - ϑ) > (k : ℝ) ^ ϑ := by
      rw [gt_iff_lt, lt_div_iff₀ (by positivity)]
      rw [← Real.rpow_add (by positivity)]
      have hpexp : ϑ + (1 - ϑ) = 1 := by ring
      rw [hpexp, Real.rpow_one]
      exact hkp
    constructor <;> norm_num at *
    · exact Int.le_of_lt_add_one (by
        rw [← @Int.cast_lt ℝ]
        push_cast
        have hkpow : (1 : ℝ) ≤ (k : ℝ) ^ ϑ :=
          Real.one_le_rpow (by exact_mod_cast hk1) hϑ0
        linarith)
    · exact Int.le_of_lt_add_one (by
        rw [← @Int.cast_lt ℝ]
        push_cast
        linarith)
  convert dvd_Pprod_of_factor k n (p : ℤ) j _ _ using 1
  · grind
  · exact ⟨n / p, by linarith [Int.emod_add_mul_ediv n p]⟩

/-- Generic pigeonhole step: a strict bad-count bound below the actual prime
count produces a divisor in the same short interval. -/
lemma exists_far_prime_at (ϑ : ℝ) (hϑ0 : 0 ≤ ϑ) (k : ℕ) (n : ℤ)
    (hk1 : 1 ≤ k)
    (hcount : ((badSetAt ϑ k n).card : ℝ) <
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ)) :
    ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧
      (p : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ ∧ (p : ℤ) ∣ Pprod k n := by
  norm_cast at *
  contrapose! hcount
  refine' le_trans (Finset.card_le_card _) _
  exact Finset.image (fun m : ℤ => m)
    (Finset.filter (fun m : ℤ => (m : ℝ) < (k : ℝ) + (k : ℝ) ^ ϑ ∧
      |(n : ℝ) / m - round ((n : ℝ) / m)| < 1 / (k : ℝ) ^ (1 - ϑ))
      (Finset.Ioo (k : ℤ) ((k : ℤ) + ⌊(k : ℝ) ^ ϑ⌋ + 2)))
  · intro p hp
    simp_all +decide
    refine ⟨?_, ?_⟩
    · linarith [show ⌈(k : ℝ) ^ ϑ⌉ ≤ ⌊(k : ℝ) ^ ϑ⌋ + 1 by
        exact Int.ceil_le_floor_add_one _]
    · exact Classical.not_not.1 fun h =>
        hcount (Int.natAbs p) hp.2.2.1
          (by linarith [abs_of_pos hp.2.1])
          (by simpa [abs_of_pos hp.2.1] using hp.2.2.2.2)
          (by
            simpa [abs_of_pos hp.2.1] using
              (dvd_from_far_at ϑ hϑ0 k n (Int.natAbs p) hk1
                (by linarith [abs_of_pos hp.2.1])
                (by simpa [abs_of_pos hp.2.1] using hp.2.2.2.1)
                (by simpa [abs_of_pos hp.2.1] using hp.2.2.2.2)
                (by simpa [abs_of_pos hp.2.1] using h)))
  · unfold badSetAt
    aesop

/-- Quantitative version of the generic Konyagin/BHP finishing step. -/
lemma konyagin_finish_at (ϑ : ℝ) (hϑ0 : 0 ≤ ϑ) (k : ℕ) (n : ℤ)
    (hk1 : 1 ≤ k) (C : ℝ)
    (hprime : C * (k : ℝ) ^ ϑ / Real.log k ≤
      (primeCard (k : ℝ) ((k : ℝ) + (k : ℝ) ^ ϑ) : ℝ))
    (hcard : ((badSetAt ϑ k n).card : ℝ) <
      C * (k : ℝ) ^ ϑ / Real.log k) :
    ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧
      (p : ℝ) < (k : ℝ) + 3 * (k : ℝ) ^ ϑ ∧ (p : ℤ) ∣ Pprod k n := by
  obtain ⟨p, hp, hpk, hpb, hdvd⟩ :=
    exists_far_prime_at ϑ hϑ0 k n hk1 (lt_of_lt_of_le hcard hprime)
  refine ⟨p, hp, hpk, ?_, hdvd⟩
  have : (0 : ℝ) ≤ (k : ℝ) ^ ϑ := Real.rpow_nonneg (by positivity) _
  linarith

/-- The exact conclusion produced before shrinking the source interval to
`(k,2k)`. -/
def SourceIntervalConclusion (ϑ : ℝ) (k : ℕ) (n : ℤ) : Prop :=
  ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧
    (p : ℝ) < (k : ℝ) + 3 * (k : ℝ) ^ ϑ ∧ (p : ℤ) ∣ Pprod k n

/-- Exact reusable contract for the four source-paper ranges.  Producing this
package from `PrimeIntervalInput ϑ` is the substantive parameterization still
missing from the fixed-exponent upstream development. -/
structure ParametricRangePackage (ϑ c : ℝ) : Prop where
  small : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    2 * (k : ℤ) < n →
    (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 - ϑ) →
    SourceIntervalConclusion ϑ k n

  medium : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (1 / 2) * (k : ℝ) ^ (2 - ϑ) < (n : ℝ) →
    (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2 →
    SourceIntervalConclusion ϑ k n
  mediumlarge : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (k : ℝ) ^ 2 / (Real.log k) ^ 2 < (n : ℝ) →
    (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ) →
    SourceIntervalConclusion ϑ k n
  large : ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
    (1 / 2) * (k : ℝ) ^ (2 + ϑ) < (n : ℝ) →
    (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
    SourceIntervalConclusion ϑ k n

/-- What a genuinely theta-parametric replay of Sections 2--6 must construct
from the abstract short-prime input. -/
def ParametricRangeBuilder (ϑ c : ℝ) : Prop :=
  PrimeIntervalInput ϑ → ParametricRangePackage ϑ c

/-- Pure range composition, fully parameterized in `ϑ` and `c`. -/
theorem source_interval_of_rangePackage (ϑ c : ℝ)
    (pkg : ParametricRangePackage ϑ c) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      SourceIntervalConclusion ϑ k n := by
  obtain ⟨k1, h1⟩ := pkg.small
  obtain ⟨k2, h2⟩ := pkg.medium
  obtain ⟨k3, h3⟩ := pkg.mediumlarge
  obtain ⟨k4, h4⟩ := pkg.large
  refine ⟨max (max k1 k2) (max k3 k4), ?_⟩
  intro k hk n hn hupper
  have hk1 : k1 ≤ k := by omega
  have hk2 : k2 ≤ k := by omega
  have hk3 : k3 ≤ k := by omega
  have hk4 : k4 ≤ k := by omega
  by_cases c1 : (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 - ϑ)
  · exact h1 k hk1 n hn c1
  · push_neg at c1
    by_cases c2 : (n : ℝ) ≤ (k : ℝ) ^ 2 / (Real.log k) ^ 2
    · exact h2 k hk2 n c1 c2
    · push_neg at c2
      by_cases c3 : (n : ℝ) ≤ (1 / 2) * (k : ℝ) ^ (2 + ϑ)
      · exact h3 k hk3 n c2 c3
      · push_neg at c3
        exact h4 k hk4 n c3 hupper

/-- For every `ϑ<1`, the source interval is eventually contained in `(k,2k)`.
This layer is independent of any prime theorem. -/
theorem main_of_rangePackage (ϑ c : ℝ) (hϑ1 : ϑ < 1)
    (pkg : ParametricRangePackage ϑ c) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  obtain ⟨k1, hmain⟩ := source_interval_of_rangePackage ϑ c pkg
  obtain ⟨k2, hpow⟩ := Filter.eventually_atTop.mp
    (eventually_le_rpow (1 - ϑ) 3 (sub_pos.mpr hϑ1))
  refine ⟨max (max k1 k2) 2, ?_⟩
  intro k hk n hn hupper
  have hk1 : k1 ≤ k := by omega
  have hk2 : k2 ≤ k := by omega
  have hkpos : (0 : ℝ) < k := by norm_cast; omega
  obtain ⟨p, hp, hpk, hpupper, hpdvd⟩ := hmain k hk1 n hn hupper
  refine ⟨p, hp, hpk, ?_, hpdvd⟩
  have hscale : 3 * (k : ℝ) ^ ϑ ≤ (k : ℝ) := by
    calc
      3 * (k : ℝ) ^ ϑ ≤ (k : ℝ) ^ (1 - ϑ) * (k : ℝ) ^ ϑ :=
        mul_le_mul_of_nonneg_right (hpow k hk2)
          (Real.rpow_nonneg (Nat.cast_nonneg k) _)
      _ = (k : ℝ) := by
        rw [← Real.rpow_add hkpos]
        ring_nf
        rw [Real.rpow_one]
  exact lt_of_lt_of_le hpupper (by linarith)

/-- Arithmetic feasibility of the strict-margin parameters throughout the
natural theorem's range `2/5 < ϑ < 3/5`.  This part of the abstract frontier is
fully formal and uses no prime input. -/
lemma exists_frontier_parameters_at (ϑ c : ℝ) (hϑlo : 2 / 5 < ϑ)
    (hϑhi : ϑ < 3 / 5) (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3) :
    ∃ a b q₁ q₃ : ℝ,
      0 < a ∧ c < a ∧ a < b ∧ b < ϑ ∧
      1 < q₁ ∧ 3 * q₁ * b < 1 - ϑ ∧
      1 < q₃ ∧ 4 * q₃ * b < 1 := by
  let f : ℝ := (1 - ϑ) / 3
  let a : ℝ := (c + f) / 2
  let b : ℝ := (a + f) / 2
  have hϑ1 : ϑ < 1 := hϑhi.trans (by norm_num)
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
  have hm1 : 3 * q₁ * b < 1 - ϑ := by
    have := (lt_div_iff₀ (by positivity : 0 < 3 * b)).1 hq₁u
    nlinarith
  have hratio3 : 1 < 1 / (4 * b) := by
    rw [lt_div_iff₀ (by positivity)]
    simpa using hfour
  obtain ⟨q₃, hq₃, hq₃u⟩ := exists_between hratio3
  have hm3 : 4 * q₃ * b < 1 := by
    have := (lt_div_iff₀ (by positivity : 0 < 4 * b)).1 hq₃u
    nlinarith
  exact ⟨a, b, q₁, q₃, ha, hca, hab, hbϑ, hq₁, hm1, hq₃, hm3⟩

/-- Exact abstract-`PI(ϑ)` frontier interface.  It is deliberately explicit
that the remaining mathematical obligation is a construction of the four
range package from `PrimeIntervalInput ϑ`; no such construction is postulated
as an axiom here. -/
theorem parametric_frontier_interface (ϑ c : ℝ) (hϑlo : 2 / 5 < ϑ)
    (hϑhi : ϑ < 3 / 5) (hc : 0 < c) (hcfront : c < (1 - ϑ) / 3)
    (hPI : PrimeIntervalInput ϑ) (build : ParametricRangeBuilder ϑ c) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n := by
  have hϑ1 : ϑ < 1 := by nlinarith
  have _ := exists_frontier_parameters_at ϑ c hϑlo hϑhi hc hcfront
  exact main_of_rangePackage ϑ c hϑ1 (build hPI)

/-- Current fixed-exponent results instantiate the exact generic range
contract for every `0<c<19/120`. -/
lemma fixed_bhp_rangePackage (c : ℝ) (hc : 0 < c) (hcfront : c < 19 / 120) :
    ParametricRangePackage theta c := by
  obtain ⟨a, b, q₁, q₃, ha, hca, hab, hbtheta, hq₁, hm1, hq₃, hm3⟩ :=
    exists_frontier_parameters c hc hcfront
  refine ⟨case_small, case_medium, case_mediumlarge, ?_⟩
  exact case_large_of_margin_certificate c q₁ q₃ hq₁ hq₃
    (hasLargeMarginCertificate_of_parameters c a b q₁ q₃
      ha hca hab hbtheta hm1 hm3 hq₁ hq₃)

/-- The already verified `19/120` theorem is a corollary of the generic
range-composition interface. -/
theorem erdos451_bhp_frontier_via_interface (c : ℝ) (hc : 0 < c)
    (hcfront : c < 19 / 120) :
    ∃ k₀ : ℕ, ∀ k : ℕ, k₀ ≤ k → ∀ n : ℤ,
      2 * (k : ℤ) < n →
      (n : ℝ) ≤ Real.exp (c * (Real.log k) ^ 2 / Real.log (Real.log k)) →
      ∃ p : ℕ, p.Prime ∧ (k : ℝ) < p ∧ (p : ℝ) < 2 * (k : ℝ) ∧
        (p : ℤ) ∣ Pprod k n :=
  main_of_rangePackage theta c theta_lt_one (fixed_bhp_rangePackage c hc hcfront)

#print axioms bhp_primeIntervalInput
#print axioms dvd_from_far_at
#print axioms exists_far_prime_at
#print axioms konyagin_finish_at
#print axioms source_interval_of_rangePackage
#print axioms main_of_rangePackage
#print axioms exists_frontier_parameters_at
#print axioms parametric_frontier_interface
#print axioms erdos451_bhp_frontier_via_interface

end
