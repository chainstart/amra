import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.IntervalAverage

/-!
Lean side certificate for the public FrontierMath Tier 4 BMO probe.

The final declaration below exposes the original public benchmark as a
supremum over actual real functions on the unit interval. The remaining
Bellman upper bound and stopped-log/cup lower bound are isolated as
function-level propositions over those interval integrals.
-/

namespace AraLibrary.Analysis

noncomputable section

open MeasureTheory
open scoped Interval

theorem bmo_contact_exponent_identity
    (s : ℝ) (hs : s ^ 2 = 3) (hs0 : s ≠ 0) :
    (10 + s / 36) / (s / 6) = 20 * s + (1 / 6 : ℝ) := by
  have hden : s / 6 ≠ 0 := div_ne_zero hs0 (by norm_num)
  apply mul_right_cancel₀ hden
  calc
    ((10 + s / 36) / (s / 6)) * (s / 6) = 10 + s / 36 := by
      exact div_mul_cancel₀ _ hden
    _ = (20 * s + (1 / 6 : ℝ)) * (s / 6) := by
      calc
        10 + s / 36 = (10 / 3) * s ^ 2 + s / 36 := by rw [hs]; norm_num
        _ = (20 * s + (1 / 6 : ℝ)) * (s / 6) := by ring

theorem bmo_contact_cubic_identity
    (s : ℝ) (hs : s ^ 2 = 3) :
    2 * (s / 6) ^ 3 = s / 36 := by
  have hs3 : s ^ 3 = 3 * s := by
    calc
      s ^ 3 = s * s ^ 2 := by ring
      _ = s * 3 := by rw [hs]
      _ = 3 * s := by ring
  calc
    2 * (s / 6) ^ 3 = s ^ 3 / 108 := by ring
    _ = (3 * s) / 108 := by rw [hs3]
    _ = s / 36 := by ring

theorem bmo_contact_value_identity
    (s : ℝ) (hs : s ^ 2 = 3) (hs0 : s ≠ 0) :
    2 * (s / 6) ^ 3 + (s / 6) * Real.exp (-((10 + s / 36) / (s / 6))) =
      s / 36 + (s / 6) * Real.exp (-(20 * s + (1 / 6 : ℝ))) := by
  rw [bmo_contact_cubic_identity s hs, bmo_contact_exponent_identity s hs hs0]

def frontierBMOPublicAnswer : ℝ :=
  1 / (12 * Real.sqrt 3) +
    (Real.sqrt 3 / 6) * Real.exp (-(20 * Real.sqrt 3 + (1 / 6 : ℝ)))

def frontierBMOOriginalSupremumValue : ℝ :=
  frontierBMOPublicAnswer - (1985 / 2 : ℝ)

def frontierBMOOriginalMeanIntegral (f : ℝ → ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, f t

def frontierBMOOriginalSecondMomentIntegral (f : ℝ → ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, (f t) ^ 2

def frontierBMOOriginalObjectiveIntegral (f : ℝ → ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, (f t) ^ 3 + |f t|

def frontierBMOIntervalMean (f : ℝ → ℝ) (a b : ℝ) : ℝ :=
  (∫ t in a..b, f t) / (b - a)

def frontierBMOIntervalVariance (f : ℝ → ℝ) (a b : ℝ) : ℝ :=
  (∫ t in a..b, (f t - frontierBMOIntervalMean f a b) ^ 2) / (b - a)

def frontierBMOOriginalFunctionAdmissible (f : ℝ → ℝ) : Prop :=
  IntervalIntegrable f volume (0 : ℝ) 1 ∧
    IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1 ∧
    IntervalIntegrable (fun t ↦ (f t) ^ 3 + |f t|) volume (0 : ℝ) 1 ∧
    frontierBMOOriginalMeanIntegral f = -10 ∧
    frontierBMOOriginalSecondMomentIntegral f = 100 + (1 / 12 : ℝ) ∧
    ∀ a b : ℝ, 0 ≤ a → a < b → b ≤ 1 →
      IntervalIntegrable
          (fun t ↦ (f t - frontierBMOIntervalMean f a b) ^ 2) volume a b ∧
        frontierBMOIntervalVariance f a b ≤ (1 / 12 : ℝ)

def frontierBMOOriginalFunctionObjectiveSet : Set ℝ :=
  {y : ℝ | ∃ f : ℝ → ℝ,
    frontierBMOOriginalFunctionAdmissible f ∧
      y = frontierBMOOriginalObjectiveIntegral f}

def frontierBMOOriginalFunctionSupremum : ℝ :=
  sSup frontierBMOOriginalFunctionObjectiveSet

def frontierBMOOriginalFunctionBenchmarkValue : ℝ :=
  frontierBMOOriginalFunctionSupremum + (1985 / 2 : ℝ)

def frontierBMOOriginalActualUpperBound : Prop :=
  ∀ y ∈ frontierBMOOriginalFunctionObjectiveSet, y ≤ frontierBMOOriginalSupremumValue

def frontierStoppedLogCupActualLowerBound : Prop :=
  frontierBMOOriginalSupremumValue ∈ frontierBMOOriginalFunctionObjectiveSet

theorem frontierBMOOriginalFunctionBenchmarkValue_eq_publicAnswer_iff :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer ↔
      frontierBMOOriginalFunctionSupremum = frontierBMOOriginalSupremumValue := by
  constructor
  · intro h
    rw [frontierBMOOriginalFunctionBenchmarkValue] at h
    rw [frontierBMOOriginalSupremumValue]
    linarith
  · intro h
    rw [frontierBMOOriginalFunctionBenchmarkValue, h, frontierBMOOriginalSupremumValue]
    ring

theorem frontier_bmo_public_sample_original_unconditional_supremum_iff :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer ↔
      frontierBMOOriginalFunctionSupremum = frontierBMOOriginalSupremumValue :=
  frontierBMOOriginalFunctionBenchmarkValue_eq_publicAnswer_iff

theorem frontierBMOOriginalFunctionSupremum_eq_value_of_actual_bounds
    (frontier_unboundedNonsmoothBellmanUpper :
      frontierBMOOriginalActualUpperBound)
    (frontier_stoppedLogCupOptimizerLower :
      frontierStoppedLogCupActualLowerBound) :
    frontierBMOOriginalFunctionSupremum = frontierBMOOriginalSupremumValue := by
  have hnonempty : frontierBMOOriginalFunctionObjectiveSet.Nonempty :=
    ⟨frontierBMOOriginalSupremumValue, frontier_stoppedLogCupOptimizerLower⟩
  have hbdd : BddAbove frontierBMOOriginalFunctionObjectiveSet :=
    ⟨frontierBMOOriginalSupremumValue, frontier_unboundedNonsmoothBellmanUpper⟩
  have hsup_le :
      frontierBMOOriginalFunctionSupremum ≤ frontierBMOOriginalSupremumValue :=
    csSup_le hnonempty frontier_unboundedNonsmoothBellmanUpper
  have hle_sup :
      frontierBMOOriginalSupremumValue ≤ frontierBMOOriginalFunctionSupremum :=
    le_csSup hbdd frontier_stoppedLogCupOptimizerLower
  exact le_antisymm hsup_le hle_sup

theorem bmo_public_answer_contact_form :
    frontierBMOPublicAnswer =
      2 * (Real.sqrt 3 / 6) ^ 3 +
        (Real.sqrt 3 / 6) *
          Real.exp (-((10 + Real.sqrt 3 / 36) / (Real.sqrt 3 / 6))) := by
  have hs_nonneg : 0 ≤ (3 : ℝ) := by norm_num
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt hs_nonneg
  have hs0 : Real.sqrt 3 ≠ 0 := Real.sqrt_ne_zero'.2 (by norm_num)
  have hcubic : 2 * (Real.sqrt 3 / 6) ^ 3 = 1 / (12 * Real.sqrt 3) := by
    calc
      2 * (Real.sqrt 3 / 6) ^ 3 = Real.sqrt 3 / 36 :=
        bmo_contact_cubic_identity (Real.sqrt 3) hs
      _ = 1 / (12 * Real.sqrt 3) := by
        apply mul_right_cancel₀ hs0
        calc
          (Real.sqrt 3 / 36) * Real.sqrt 3 = (Real.sqrt 3 ^ 2) / 36 := by ring
          _ = 3 / 36 := by rw [hs]
          _ = (1 / (12 * Real.sqrt 3)) * Real.sqrt 3 := by
            field_simp [hs0]
            norm_num
  rw [frontierBMOPublicAnswer, hcubic,
    bmo_contact_exponent_identity (Real.sqrt 3) hs hs0]

/-!
The following definitions are the current proof-obligation scaffold for the
piecewise Bellman candidate produced by the blocker-driven BMO loop. They do
not assert the missing global majorant theorem; they name the payoff, strip,
candidate pieces, and the precise right-tail obstruction for later proof.
-/

def frontierEpsilon : ℝ :=
  Real.sqrt 3 / 6

def frontierA : ℝ :=
  10

def frontierCStar : ℝ :=
  frontierA + 2 * frontierEpsilon ^ 3

def frontierPhi (t : ℝ) : ℝ :=
  t ^ 3 + 2 * max (t - frontierA) 0

def frontierBMOCenteredObjectiveIntegral (g : ℝ → ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, frontierPhi (g t)

def frontierBMOCenteredFunctionAdmissible (g : ℝ → ℝ) : Prop :=
  IntervalIntegrable g volume (0 : ℝ) 1 ∧
    IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1 ∧
    IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1 ∧
    frontierBMOOriginalMeanIntegral g = 0 ∧
    frontierBMOOriginalSecondMomentIntegral g = (1 / 12 : ℝ) ∧
    ∀ a b : ℝ, 0 ≤ a → a < b → b ≤ 1 →
      IntervalIntegrable
          (fun t ↦ (g t - frontierBMOIntervalMean g a b) ^ 2) volume a b ∧
        frontierBMOIntervalVariance g a b ≤ (1 / 12 : ℝ)

def frontierBMOCenteredFunctionObjectiveSet : Set ℝ :=
  {y : ℝ | ∃ g : ℝ → ℝ,
    frontierBMOCenteredFunctionAdmissible g ∧
      y = frontierBMOCenteredObjectiveIntegral g}

def frontierBMOCenteredFunctionSupremum : ℝ :=
  sSup frontierBMOCenteredFunctionObjectiveSet

theorem frontier_centered_objective_pointwise (g : ℝ) :
    (g - 10) ^ 3 + |g - 10| =
      frontierPhi g - 30 * g ^ 2 + 299 * g - 990 := by
  rw [frontierPhi, frontierA]
  by_cases h : 0 ≤ g - 10
  · rw [abs_of_nonneg h, max_eq_left h]
    ring
  · have hle : g - 10 ≤ 0 := le_of_not_ge h
    rw [abs_of_nonpos hle, max_eq_right hle]
    ring

theorem frontier_centering_constant_from_moments
    (objective centeredObjective mean secondMoment : ℝ)
    (hobjective :
      objective = centeredObjective - 30 * secondMoment + 299 * mean - 990)
    (hmean : mean = 0)
    (hsecondMoment : secondMoment = (1 / 12 : ℝ)) :
    objective = centeredObjective - (1985 / 2 : ℝ) := by
  rw [hobjective, hmean, hsecondMoment]
  ring

theorem frontier_centered_objective_integral_shift
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hphi : IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1) :
    frontierBMOOriginalObjectiveIntegral (fun t ↦ g t - 10) =
      frontierBMOCenteredObjectiveIntegral g -
        30 * frontierBMOOriginalSecondMomentIntegral g +
        299 * frontierBMOOriginalMeanIntegral g - 990 := by
  have h30 :
      IntervalIntegrable (fun t ↦ 30 * (g t) ^ 2) volume (0 : ℝ) 1 :=
    hg2.const_mul 30
  have h299 :
      IntervalIntegrable (fun t ↦ 299 * g t) volume (0 : ℝ) 1 :=
    hg.const_mul 299
  have hmain :
      IntervalIntegrable
        (fun t ↦ (frontierPhi (g t) - 30 * (g t) ^ 2) + 299 * g t)
        volume (0 : ℝ) 1 :=
    (hphi.sub h30).add h299
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (990 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOOriginalObjectiveIntegral, frontierBMOCenteredObjectiveIntegral,
    frontierBMOOriginalSecondMomentIntegral, frontierBMOOriginalMeanIntegral]
  calc
    ∫ t in (0 : ℝ)..1, (g t - 10) ^ 3 + |g t - 10| =
        ∫ t in (0 : ℝ)..1,
          ((frontierPhi (g t) - 30 * (g t) ^ 2) + 299 * g t) - 990 := by
      apply intervalIntegral.integral_congr
      intro t _ht
      simpa using frontier_centered_objective_pointwise (g t)
    _ = (∫ t in (0 : ℝ)..1, frontierPhi (g t)) -
          30 * (∫ t in (0 : ℝ)..1, (g t) ^ 2) +
          299 * (∫ t in (0 : ℝ)..1, g t) - 990 := by
      rw [intervalIntegral.integral_sub hmain hconst]
      rw [intervalIntegral.integral_add (hphi.sub h30) h299]
      rw [intervalIntegral.integral_sub hphi h30]
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [intervalIntegral.integral_const]
      norm_num

theorem frontier_centered_objective_integral_shift_of_moments
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hphi : IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral g = 0)
    (hsecondMoment : frontierBMOOriginalSecondMomentIntegral g = (1 / 12 : ℝ)) :
    frontierBMOOriginalObjectiveIntegral (fun t ↦ g t - 10) =
      frontierBMOCenteredObjectiveIntegral g - (1985 / 2 : ℝ) := by
  exact frontier_centering_constant_from_moments
    (frontierBMOOriginalObjectiveIntegral (fun t ↦ g t - 10))
    (frontierBMOCenteredObjectiveIntegral g)
    (frontierBMOOriginalMeanIntegral g)
    (frontierBMOOriginalSecondMomentIntegral g)
    (frontier_centered_objective_integral_shift g hg hg2 hphi)
    hmean hsecondMoment

theorem frontier_centered_objective_shift_mem_original_objectiveSet
    (g : ℝ → ℝ)
    (hshifted : frontierBMOOriginalFunctionAdmissible (fun t ↦ g t - 10))
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hphi : IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral g = 0)
    (hsecondMoment : frontierBMOOriginalSecondMomentIntegral g = (1 / 12 : ℝ)) :
    frontierBMOCenteredObjectiveIntegral g - (1985 / 2 : ℝ) ∈
      frontierBMOOriginalFunctionObjectiveSet := by
  refine ⟨fun t ↦ g t - 10, hshifted, ?_⟩
  exact (frontier_centered_objective_integral_shift_of_moments
    g hg hg2 hphi hmean hsecondMoment).symm

theorem frontier_centered_shift_intervalIntegrable
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ g t - 10) volume (0 : ℝ) 1 := by
  exact hg.sub intervalIntegrable_const

theorem frontier_centered_shift_square_intervalIntegrable
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ (g t - 10) ^ 2) volume (0 : ℝ) 1 := by
  have h20 : IntervalIntegrable (fun t ↦ 20 * g t) volume (0 : ℝ) 1 :=
    hg.const_mul 20
  have hpoly :
      IntervalIntegrable (fun t ↦ (g t) ^ 2 - 20 * g t + 100) volume (0 : ℝ) 1 :=
    (hg2.sub h20).add intervalIntegrable_const
  refine hpoly.congr ?_
  intro t _ht
  ring

theorem frontier_centered_shift_objective_intervalIntegrable
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hphi : IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ (g t - 10) ^ 3 + |g t - 10|)
      volume (0 : ℝ) 1 := by
  have h30 :
      IntervalIntegrable (fun t ↦ 30 * (g t) ^ 2) volume (0 : ℝ) 1 :=
    hg2.const_mul 30
  have h299 :
      IntervalIntegrable (fun t ↦ 299 * g t) volume (0 : ℝ) 1 :=
    hg.const_mul 299
  have hmain :
      IntervalIntegrable
        (fun t ↦ ((frontierPhi (g t) - 30 * (g t) ^ 2) + 299 * g t) - 990)
        volume (0 : ℝ) 1 :=
    ((hphi.sub h30).add h299).sub intervalIntegrable_const
  refine hmain.congr ?_
  intro t _ht
  simpa using (frontier_centered_objective_pointwise (g t)).symm

theorem frontier_centered_mean_integral_shift
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1) :
    frontierBMOOriginalMeanIntegral (fun t ↦ g t - 10) =
      frontierBMOOriginalMeanIntegral g - 10 := by
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (10 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOOriginalMeanIntegral]
  rw [intervalIntegral.integral_sub hg hconst]
  rw [intervalIntegral.integral_const]
  rw [frontierBMOOriginalMeanIntegral]
  norm_num

theorem frontier_centered_mean_integral_shift_of_centered_mean
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral g = 0) :
    frontierBMOOriginalMeanIntegral (fun t ↦ g t - 10) = -10 := by
  rw [frontier_centered_mean_integral_shift g hg, hmean]
  norm_num

theorem frontier_centered_second_moment_integral_shift
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1) :
    frontierBMOOriginalSecondMomentIntegral (fun t ↦ g t - 10) =
      frontierBMOOriginalSecondMomentIntegral g -
        20 * frontierBMOOriginalMeanIntegral g + 100 := by
  have h20 :
      IntervalIntegrable (fun t ↦ 20 * g t) volume (0 : ℝ) 1 :=
    hg.const_mul 20
  have hsum :
      IntervalIntegrable (fun t ↦ (g t) ^ 2 - 20 * g t) volume (0 : ℝ) 1 :=
    hg2.sub h20
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (100 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOOriginalSecondMomentIntegral, frontierBMOOriginalMeanIntegral]
  calc
    ∫ t in (0 : ℝ)..1, (g t - 10) ^ 2 =
        ∫ t in (0 : ℝ)..1, ((g t) ^ 2 - 20 * g t) + 100 := by
      apply intervalIntegral.integral_congr
      intro t _ht
      ring
    _ = (∫ t in (0 : ℝ)..1, (g t) ^ 2) -
          20 * (∫ t in (0 : ℝ)..1, g t) + 100 := by
      rw [intervalIntegral.integral_add hsum hconst]
      rw [intervalIntegral.integral_sub hg2 h20]
      rw [intervalIntegral.integral_const_mul]
      rw [intervalIntegral.integral_const]
      norm_num

theorem frontier_centered_second_moment_integral_shift_of_centered_moments
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral g = 0)
    (hsecondMoment : frontierBMOOriginalSecondMomentIntegral g = (1 / 12 : ℝ)) :
    frontierBMOOriginalSecondMomentIntegral (fun t ↦ g t - 10) =
      100 + (1 / 12 : ℝ) := by
  rw [frontier_centered_second_moment_integral_shift g hg hg2, hmean, hsecondMoment]
  ring

theorem frontier_intervalIntegrable_on_subinterval_of_unit
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    {a b : ℝ} (ha : 0 ≤ a) (hab : a < b) (hb : b ≤ 1) :
    IntervalIntegrable g volume a b := by
  exact hg.mono_set (by
    apply Set.uIcc_subset_uIcc
    · constructor
      · simpa using ha
      · have : a ≤ (1 : ℝ) := by linarith
        simpa using this
    · constructor
      · have : (0 : ℝ) ≤ b := by linarith
        simpa using this
      · simpa using hb)

theorem frontier_intervalMean_shift_sub
    (g : ℝ → ℝ) {a b : ℝ}
    (hg : IntervalIntegrable g volume a b) (hab : a < b) :
    frontierBMOIntervalMean (fun t ↦ g t - 10) a b =
      frontierBMOIntervalMean g a b - 10 := by
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (10 : ℝ)) volume a b :=
    intervalIntegrable_const
  have hne : b - a ≠ 0 := by linarith
  rw [frontierBMOIntervalMean]
  rw [intervalIntegral.integral_sub hg hconst]
  rw [intervalIntegral.integral_const]
  rw [frontierBMOIntervalMean]
  simp only [smul_eq_mul]
  field_simp [hne]

theorem frontier_intervalVariance_shift_sub
    (g : ℝ → ℝ) {a b : ℝ}
    (hg : IntervalIntegrable g volume a b)
    (hvar :
      IntervalIntegrable
        (fun t ↦ (g t - frontierBMOIntervalMean g a b) ^ 2) volume a b)
    (hab : a < b) :
    IntervalIntegrable
        (fun t ↦
          ((g t - 10) - frontierBMOIntervalMean (fun t ↦ g t - 10) a b) ^ 2)
        volume a b ∧
      frontierBMOIntervalVariance (fun t ↦ g t - 10) a b =
        frontierBMOIntervalVariance g a b := by
  have hmean := frontier_intervalMean_shift_sub g hg hab
  have hvar_shift :
      IntervalIntegrable
        (fun t ↦
          ((g t - 10) - frontierBMOIntervalMean (fun t ↦ g t - 10) a b) ^ 2)
        volume a b := by
    refine hvar.congr ?_
    intro t _ht
    rw [hmean]
    ring
  refine ⟨hvar_shift, ?_⟩
  rw [frontierBMOIntervalVariance]
  apply congrArg (fun z : ℝ ↦ z / (b - a))
  apply intervalIntegral.integral_congr
  intro t _ht
  rw [hmean]
  ring

theorem frontier_centered_admissible_shift_variance
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g)
    {a b : ℝ} (ha : 0 ≤ a) (hab : a < b) (hb : b ≤ 1) :
    IntervalIntegrable
        (fun t ↦
          ((g t - 10) - frontierBMOIntervalMean (fun t ↦ g t - 10) a b) ^ 2)
        volume a b ∧
      frontierBMOIntervalVariance (fun t ↦ g t - 10) a b ≤ (1 / 12 : ℝ) := by
  rcases hcentered with ⟨hg, _hg2, _hphi, _hmean, _hsecondMoment, hvariance⟩
  have hgab : IntervalIntegrable g volume a b :=
    frontier_intervalIntegrable_on_subinterval_of_unit g hg ha hab hb
  rcases hvariance a b ha hab hb with ⟨hvar_int, hvar_le⟩
  rcases frontier_intervalVariance_shift_sub g hgab hvar_int hab with
    ⟨hshift_int, hshift_eq⟩
  exact ⟨hshift_int, by rw [hshift_eq]; exact hvar_le⟩

theorem frontier_centered_admissible_shift_original
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g) :
    frontierBMOOriginalFunctionAdmissible (fun t ↦ g t - 10) := by
  rcases hcentered with ⟨hg, hg2, hphi, hmean, hsecondMoment, hvariance⟩
  refine ⟨
    frontier_centered_shift_intervalIntegrable g hg,
    frontier_centered_shift_square_intervalIntegrable g hg hg2,
    frontier_centered_shift_objective_intervalIntegrable g hg hg2 hphi,
    frontier_centered_mean_integral_shift_of_centered_mean g hg hmean,
    frontier_centered_second_moment_integral_shift_of_centered_moments
      g hg hg2 hmean hsecondMoment,
    ?_⟩
  intro a b ha hab hb
  exact frontier_centered_admissible_shift_variance
    g ⟨hg, hg2, hphi, hmean, hsecondMoment, hvariance⟩ ha hab hb

theorem frontier_centered_objective_shift_mem_original_objectiveSet_of_admissible
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g) :
    frontierBMOCenteredObjectiveIntegral g - (1985 / 2 : ℝ) ∈
      frontierBMOOriginalFunctionObjectiveSet := by
  rcases hcentered with ⟨hg, hg2, hphi, hmean, hsecondMoment, hvariance⟩
  exact frontier_centered_objective_shift_mem_original_objectiveSet
    g
    (frontier_centered_admissible_shift_original
      g ⟨hg, hg2, hphi, hmean, hsecondMoment, hvariance⟩)
    hg hg2 hphi hmean hsecondMoment

theorem frontier_original_objective_pointwise_uncenter (x : ℝ) :
    frontierPhi (x + 10) =
      x ^ 3 + |x| + 30 * x ^ 2 + 301 * x + 1000 := by
  rw [frontierPhi, frontierA]
  by_cases h : 0 ≤ x
  · rw [abs_of_nonneg h, max_eq_left]
    · ring
    · ring_nf
      exact h
  · have hx : x ≤ 0 := le_of_not_ge h
    rw [abs_of_nonpos hx, max_eq_right]
    · ring
    · ring_nf
      exact hx

theorem frontier_original_objective_integral_uncenter
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1)
    (hobj : IntervalIntegrable (fun t ↦ (f t) ^ 3 + |f t|) volume (0 : ℝ) 1) :
    frontierBMOCenteredObjectiveIntegral (fun t ↦ f t + 10) =
      frontierBMOOriginalObjectiveIntegral f +
        30 * frontierBMOOriginalSecondMomentIntegral f +
        301 * frontierBMOOriginalMeanIntegral f + 1000 := by
  have h30 :
      IntervalIntegrable (fun t ↦ 30 * (f t) ^ 2) volume (0 : ℝ) 1 :=
    hf2.const_mul 30
  have h301 :
      IntervalIntegrable (fun t ↦ 301 * f t) volume (0 : ℝ) 1 :=
    hf.const_mul 301
  have hleft :
      IntervalIntegrable
        (fun t ↦ (f t) ^ 3 + |f t| + 30 * (f t) ^ 2) volume (0 : ℝ) 1 :=
    hobj.add h30
  have hmain :
      IntervalIntegrable
        (fun t ↦ ((f t) ^ 3 + |f t| + 30 * (f t) ^ 2) + 301 * f t)
        volume (0 : ℝ) 1 :=
    hleft.add h301
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (1000 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOCenteredObjectiveIntegral, frontierBMOOriginalObjectiveIntegral,
    frontierBMOOriginalSecondMomentIntegral, frontierBMOOriginalMeanIntegral]
  calc
    ∫ t in (0 : ℝ)..1, frontierPhi (f t + 10) =
        ∫ t in (0 : ℝ)..1,
          (((f t) ^ 3 + |f t| + 30 * (f t) ^ 2) + 301 * f t) + 1000 := by
      apply intervalIntegral.integral_congr
      intro t _ht
      simpa [add_assoc] using frontier_original_objective_pointwise_uncenter (f t)
    _ = (∫ t in (0 : ℝ)..1, (f t) ^ 3 + |f t|) +
          30 * (∫ t in (0 : ℝ)..1, (f t) ^ 2) +
          301 * (∫ t in (0 : ℝ)..1, f t) + 1000 := by
      rw [intervalIntegral.integral_add hmain hconst]
      rw [intervalIntegral.integral_add hleft h301]
      rw [intervalIntegral.integral_add hobj h30]
      rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rw [intervalIntegral.integral_const]
      norm_num

theorem frontier_original_objective_integral_uncenter_of_moments
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1)
    (hobj : IntervalIntegrable (fun t ↦ (f t) ^ 3 + |f t|) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral f = -10)
    (hsecondMoment :
      frontierBMOOriginalSecondMomentIntegral f = 100 + (1 / 12 : ℝ)) :
    frontierBMOCenteredObjectiveIntegral (fun t ↦ f t + 10) =
      frontierBMOOriginalObjectiveIntegral f + (1985 / 2 : ℝ) := by
  rw [frontier_original_objective_integral_uncenter f hf hf2 hobj, hmean, hsecondMoment]
  ring

theorem frontier_original_mean_integral_uncenter
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1) :
    frontierBMOOriginalMeanIntegral (fun t ↦ f t + 10) =
      frontierBMOOriginalMeanIntegral f + 10 := by
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (10 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOOriginalMeanIntegral]
  rw [intervalIntegral.integral_add hf hconst]
  rw [intervalIntegral.integral_const]
  rw [frontierBMOOriginalMeanIntegral]
  norm_num

theorem frontier_original_mean_integral_uncenter_of_original_mean
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral f = -10) :
    frontierBMOOriginalMeanIntegral (fun t ↦ f t + 10) = 0 := by
  rw [frontier_original_mean_integral_uncenter f hf, hmean]
  norm_num

theorem frontier_original_second_moment_integral_uncenter
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1) :
    frontierBMOOriginalSecondMomentIntegral (fun t ↦ f t + 10) =
      frontierBMOOriginalSecondMomentIntegral f +
        20 * frontierBMOOriginalMeanIntegral f + 100 := by
  have h20 :
      IntervalIntegrable (fun t ↦ 20 * f t) volume (0 : ℝ) 1 :=
    hf.const_mul 20
  have hsum :
      IntervalIntegrable (fun t ↦ (f t) ^ 2 + 20 * f t) volume (0 : ℝ) 1 :=
    hf2.add h20
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (100 : ℝ)) volume (0 : ℝ) 1 :=
    intervalIntegrable_const
  rw [frontierBMOOriginalSecondMomentIntegral, frontierBMOOriginalMeanIntegral]
  calc
    ∫ t in (0 : ℝ)..1, (f t + 10) ^ 2 =
        ∫ t in (0 : ℝ)..1, ((f t) ^ 2 + 20 * f t) + 100 := by
      apply intervalIntegral.integral_congr
      intro t _ht
      ring
    _ = (∫ t in (0 : ℝ)..1, (f t) ^ 2) +
          20 * (∫ t in (0 : ℝ)..1, f t) + 100 := by
      rw [intervalIntegral.integral_add hsum hconst]
      rw [intervalIntegral.integral_add hf2 h20]
      rw [intervalIntegral.integral_const_mul]
      rw [intervalIntegral.integral_const]
      norm_num

theorem frontier_original_second_moment_integral_uncenter_of_original_moments
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral f = -10)
    (hsecondMoment :
      frontierBMOOriginalSecondMomentIntegral f = 100 + (1 / 12 : ℝ)) :
    frontierBMOOriginalSecondMomentIntegral (fun t ↦ f t + 10) =
      (1 / 12 : ℝ) := by
  rw [frontier_original_second_moment_integral_uncenter f hf hf2, hmean, hsecondMoment]
  ring

theorem frontier_original_uncenter_intervalIntegrable
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ f t + 10) volume (0 : ℝ) 1 := by
  exact hf.add intervalIntegrable_const

theorem frontier_original_uncenter_square_intervalIntegrable
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ (f t + 10) ^ 2) volume (0 : ℝ) 1 := by
  have h20 : IntervalIntegrable (fun t ↦ 20 * f t) volume (0 : ℝ) 1 :=
    hf.const_mul 20
  have hpoly :
      IntervalIntegrable (fun t ↦ (f t) ^ 2 + 20 * f t + 100) volume (0 : ℝ) 1 :=
    (hf2.add h20).add intervalIntegrable_const
  refine hpoly.congr ?_
  intro t _ht
  ring

theorem frontier_original_uncenter_phi_intervalIntegrable
    (f : ℝ → ℝ)
    (hf : IntervalIntegrable f volume (0 : ℝ) 1)
    (hf2 : IntervalIntegrable (fun t ↦ (f t) ^ 2) volume (0 : ℝ) 1)
    (hobj : IntervalIntegrable (fun t ↦ (f t) ^ 3 + |f t|)
      volume (0 : ℝ) 1) :
    IntervalIntegrable (fun t ↦ frontierPhi (f t + 10)) volume (0 : ℝ) 1 := by
  have h30 :
      IntervalIntegrable (fun t ↦ 30 * (f t) ^ 2) volume (0 : ℝ) 1 :=
    hf2.const_mul 30
  have h301 :
      IntervalIntegrable (fun t ↦ 301 * f t) volume (0 : ℝ) 1 :=
    hf.const_mul 301
  have hleft :
      IntervalIntegrable
        (fun t ↦ (f t) ^ 3 + |f t| + 30 * (f t) ^ 2) volume (0 : ℝ) 1 :=
    hobj.add h30
  have hmain :
      IntervalIntegrable
        (fun t ↦ ((f t) ^ 3 + |f t| + 30 * (f t) ^ 2) + 301 * f t)
        volume (0 : ℝ) 1 :=
    hleft.add h301
  have hpoly :
      IntervalIntegrable
        (fun t ↦ (((f t) ^ 3 + |f t| + 30 * (f t) ^ 2) + 301 * f t) + 1000)
        volume (0 : ℝ) 1 :=
    hmain.add intervalIntegrable_const
  refine hpoly.congr ?_
  intro t _ht
  simpa [add_assoc] using (frontier_original_objective_pointwise_uncenter (f t)).symm

theorem frontier_intervalMean_shift_add
    (f : ℝ → ℝ) {a b : ℝ}
    (hf : IntervalIntegrable f volume a b) (hab : a < b) :
    frontierBMOIntervalMean (fun t ↦ f t + 10) a b =
      frontierBMOIntervalMean f a b + 10 := by
  have hconst :
      IntervalIntegrable (fun _ : ℝ ↦ (10 : ℝ)) volume a b :=
    intervalIntegrable_const
  have hne : b - a ≠ 0 := by linarith
  rw [frontierBMOIntervalMean]
  rw [intervalIntegral.integral_add hf hconst]
  rw [intervalIntegral.integral_const]
  rw [frontierBMOIntervalMean]
  simp only [smul_eq_mul]
  field_simp [hne]

theorem frontier_intervalVariance_shift_add
    (f : ℝ → ℝ) {a b : ℝ}
    (hf : IntervalIntegrable f volume a b)
    (hvar :
      IntervalIntegrable
        (fun t ↦ (f t - frontierBMOIntervalMean f a b) ^ 2) volume a b)
    (hab : a < b) :
    IntervalIntegrable
        (fun t ↦
          ((f t + 10) - frontierBMOIntervalMean (fun t ↦ f t + 10) a b) ^ 2)
        volume a b ∧
      frontierBMOIntervalVariance (fun t ↦ f t + 10) a b =
        frontierBMOIntervalVariance f a b := by
  have hmean := frontier_intervalMean_shift_add f hf hab
  have hvar_shift :
      IntervalIntegrable
        (fun t ↦
          ((f t + 10) - frontierBMOIntervalMean (fun t ↦ f t + 10) a b) ^ 2)
        volume a b := by
    refine hvar.congr ?_
    intro t _ht
    rw [hmean]
    ring
  refine ⟨hvar_shift, ?_⟩
  rw [frontierBMOIntervalVariance]
  apply congrArg (fun z : ℝ ↦ z / (b - a))
  apply intervalIntegral.integral_congr
  intro t _ht
  rw [hmean]
  ring

theorem frontier_original_admissible_uncenter_variance
    (f : ℝ → ℝ)
    (horiginal : frontierBMOOriginalFunctionAdmissible f)
    {a b : ℝ} (ha : 0 ≤ a) (hab : a < b) (hb : b ≤ 1) :
    IntervalIntegrable
        (fun t ↦
          ((f t + 10) - frontierBMOIntervalMean (fun t ↦ f t + 10) a b) ^ 2)
        volume a b ∧
      frontierBMOIntervalVariance (fun t ↦ f t + 10) a b ≤ (1 / 12 : ℝ) := by
  rcases horiginal with ⟨hf, _hf2, _hobj, _hmean, _hsecondMoment, hvariance⟩
  have hfab : IntervalIntegrable f volume a b :=
    frontier_intervalIntegrable_on_subinterval_of_unit f hf ha hab hb
  rcases hvariance a b ha hab hb with ⟨hvar_int, hvar_le⟩
  rcases frontier_intervalVariance_shift_add f hfab hvar_int hab with
    ⟨hshift_int, hshift_eq⟩
  exact ⟨hshift_int, by rw [hshift_eq]; exact hvar_le⟩

theorem frontier_original_admissible_uncenter_centered
    (f : ℝ → ℝ)
    (horiginal : frontierBMOOriginalFunctionAdmissible f) :
    frontierBMOCenteredFunctionAdmissible (fun t ↦ f t + 10) := by
  rcases horiginal with ⟨hf, hf2, hobj, hmean, hsecondMoment, hvariance⟩
  refine ⟨
    frontier_original_uncenter_intervalIntegrable f hf,
    frontier_original_uncenter_square_intervalIntegrable f hf hf2,
    frontier_original_uncenter_phi_intervalIntegrable f hf hf2 hobj,
    frontier_original_mean_integral_uncenter_of_original_mean f hf hmean,
    frontier_original_second_moment_integral_uncenter_of_original_moments
      f hf hf2 hmean hsecondMoment,
    ?_⟩
  intro a b ha hab hb
  exact frontier_original_admissible_uncenter_variance
    f ⟨hf, hf2, hobj, hmean, hsecondMoment, hvariance⟩ ha hab hb

theorem frontier_original_objective_shift_mem_centered_objectiveSet
    (f : ℝ → ℝ)
    (horiginal : frontierBMOOriginalFunctionAdmissible f) :
    frontierBMOOriginalObjectiveIntegral f + (1985 / 2 : ℝ) ∈
      frontierBMOCenteredFunctionObjectiveSet := by
  rcases horiginal with ⟨hf, hf2, hobj, hmean, hsecondMoment, hvariance⟩
  refine ⟨fun t ↦ f t + 10,
    frontier_original_admissible_uncenter_centered
      f ⟨hf, hf2, hobj, hmean, hsecondMoment, hvariance⟩, ?_⟩
  exact (frontier_original_objective_integral_uncenter_of_moments
    f hf hf2 hobj hmean hsecondMoment).symm

theorem frontier_original_centered_objectiveSet_shift :
    frontierBMOOriginalFunctionObjectiveSet =
      (fun y : ℝ ↦ y - (1985 / 2 : ℝ)) '' frontierBMOCenteredFunctionObjectiveSet := by
  ext y
  constructor
  · intro hy
    rcases hy with ⟨f, horiginal, rfl⟩
    refine ⟨frontierBMOOriginalObjectiveIntegral f + (1985 / 2 : ℝ),
      frontier_original_objective_shift_mem_centered_objectiveSet f horiginal, ?_⟩
    ring
  · intro hy
    rcases hy with ⟨z, hz, rfl⟩
    rcases hz with ⟨g, hcentered, rfl⟩
    exact frontier_centered_objective_shift_mem_original_objectiveSet_of_admissible
      g hcentered

theorem frontier_sSup_image_sub_const
    (S : Set ℝ) (c : ℝ) (hne : S.Nonempty) (hbdd : BddAbove S) :
    sSup ((fun y : ℝ ↦ y - c) '' S) = sSup S - c := by
  have hne_image : ((fun y : ℝ ↦ y - c) '' S).Nonempty := by
    rcases hne with ⟨y, hy⟩
    exact ⟨y - c, y, hy, rfl⟩
  have hbddS : BddAbove S := hbdd
  obtain ⟨M, hM⟩ := hbdd
  have hbdd_image : BddAbove ((fun y : ℝ ↦ y - c) '' S) := by
    refine ⟨M - c, ?_⟩
    intro y hy
    rcases hy with ⟨z, hz, rfl⟩
    exact sub_le_sub_right (hM hz) c
  apply le_antisymm
  · refine csSup_le hne_image ?_
    intro y hy
    rcases hy with ⟨z, hz, rfl⟩
    exact sub_le_sub_right (le_csSup hbddS hz) c
  · have hupper : ∀ z ∈ S, z ≤ sSup ((fun y : ℝ ↦ y - c) '' S) + c := by
      intro z hz
      have hz_image : z - c ∈ ((fun y : ℝ ↦ y - c) '' S) := ⟨z, hz, rfl⟩
      have hz_le : z - c ≤ sSup ((fun y : ℝ ↦ y - c) '' S) :=
        le_csSup hbdd_image hz_image
      linarith
    have hsup_le : sSup S ≤ sSup ((fun y : ℝ ↦ y - c) '' S) + c :=
      csSup_le hne hupper
    linarith

theorem frontier_original_benchmark_eq_centered_supremum_of_set_shift
    (hset :
      frontierBMOOriginalFunctionObjectiveSet =
        (fun y : ℝ ↦ y - (1985 / 2 : ℝ)) '' frontierBMOCenteredFunctionObjectiveSet)
    (hne : frontierBMOCenteredFunctionObjectiveSet.Nonempty)
    (hbdd : BddAbove frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOOriginalFunctionBenchmarkValue =
      frontierBMOCenteredFunctionSupremum := by
  rw [frontierBMOOriginalFunctionBenchmarkValue,
    frontierBMOOriginalFunctionSupremum, frontierBMOCenteredFunctionSupremum,
    hset]
  rw [frontier_sSup_image_sub_const frontierBMOCenteredFunctionObjectiveSet
    (1985 / 2 : ℝ) hne hbdd]
  ring

theorem frontier_original_benchmark_eq_centered_supremum
    (hne : frontierBMOCenteredFunctionObjectiveSet.Nonempty)
    (hbdd : BddAbove frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOOriginalFunctionBenchmarkValue =
      frontierBMOCenteredFunctionSupremum := by
  exact frontier_original_benchmark_eq_centered_supremum_of_set_shift
    frontier_original_centered_objectiveSet_shift hne hbdd

def frontierBMOCenteredActualUpperBound : Prop :=
  ∀ y ∈ frontierBMOCenteredFunctionObjectiveSet, y ≤ frontierBMOPublicAnswer

theorem frontierBMOOriginalActualUpperBound_of_centered_cover
    (hcover : ∀ y ∈ frontierBMOOriginalFunctionObjectiveSet,
      y + (1985 / 2 : ℝ) ∈ frontierBMOCenteredFunctionObjectiveSet)
    (hupper : frontierBMOCenteredActualUpperBound) :
    frontierBMOOriginalActualUpperBound := by
  intro y hy
  have hy_upper : y + (1985 / 2 : ℝ) ≤ frontierBMOPublicAnswer :=
    hupper (y + (1985 / 2 : ℝ)) (hcover y hy)
  rw [frontierBMOOriginalSupremumValue]
  linarith

theorem frontierBMOOriginalActualUpperBound_of_centered_set_shift
    (hset :
      frontierBMOOriginalFunctionObjectiveSet =
        (fun y : ℝ ↦ y - (1985 / 2 : ℝ)) '' frontierBMOCenteredFunctionObjectiveSet)
    (hupper : frontierBMOCenteredActualUpperBound) :
    frontierBMOOriginalActualUpperBound := by
  apply frontierBMOOriginalActualUpperBound_of_centered_cover
  · intro y hy
    rw [hset] at hy
    rcases hy with ⟨z, hz, rfl⟩
    convert hz using 1
    ring
  · exact hupper

theorem frontierBMOOriginalActualUpperBound_of_centered_upper
    (hupper : frontierBMOCenteredActualUpperBound) :
    frontierBMOOriginalActualUpperBound := by
  exact frontierBMOOriginalActualUpperBound_of_centered_set_shift
    frontier_original_centered_objectiveSet_shift hupper

def frontierOmega (eps x1 x2 : ℝ) : Prop :=
  x1 ^ 2 ≤ x2 ∧ x2 ≤ x1 ^ 2 + eps ^ 2

def frontierRadius (eps x1 x2 : ℝ) : ℝ :=
  Real.sqrt (eps ^ 2 + x1 ^ 2 - x2)

def frontierCPlus (eps x1 x2 : ℝ) : ℝ :=
  x1 + frontierRadius eps x1 x2

def frontierDMinus (eps x1 x2 : ℝ) : ℝ :=
  x1 - frontierRadius eps x1 x2

def frontierKL : ℝ :=
  frontierEpsilon * Real.exp (-(frontierCStar / frontierEpsilon))

def frontierKR : ℝ :=
  frontierEpsilon * Real.exp (frontierCStar / frontierEpsilon)

def frontierLeftPiece (x1 x2 : ℝ) : ℝ :=
  let eps := frontierEpsilon
  let r := frontierRadius eps x1 x2
  let C := frontierCPlus eps x1 x2
  (r / eps) * (C - eps) ^ 3 +
    (1 - r / eps) * (C ^ 3 + 3 * C * eps ^ 2 + 2 * eps ^ 3 + frontierKL * Real.exp (C / eps))

def frontierCupAlpha : ℝ :=
  frontierCStar - frontierEpsilon

def frontierCupBeta : ℝ :=
  frontierCStar + frontierEpsilon

def frontierCupDomain (x1 x2 : ℝ) : Prop :=
  frontierCupAlpha ≤ x1 ∧ x1 ≤ frontierCupBeta ∧
    x1 ^ 2 ≤ x2 ∧ x2 ≤ 2 * frontierCStar * x1 - frontierCStar ^ 2 + frontierEpsilon ^ 2

def frontierCupPiece (x1 _x2 : ℝ) : ℝ :=
  ((frontierCupBeta - x1) / (2 * frontierEpsilon)) * frontierPhi frontierCupAlpha +
    ((x1 - frontierCupAlpha) / (2 * frontierEpsilon)) * frontierPhi frontierCupBeta

def frontierRightReflectedPiece (x1 x2 : ℝ) : ℝ :=
  let eps := frontierEpsilon
  let r := frontierRadius eps x1 x2
  let D := frontierDMinus eps x1 x2
  (r / eps) * ((D + eps) ^ 3 + 2 * (D + eps - frontierA)) +
    (1 - r / eps) *
      (D ^ 3 + 3 * D * eps ^ 2 - 2 * eps ^ 3 + 2 * D - 2 * frontierA +
        frontierKR * Real.exp (-(D / eps)))

def frontierRightReflectedConcavityCondition (D : ℝ) : Prop :=
  6 * frontierEpsilon ^ 3 ≤ frontierKR * Real.exp (-(D / frontierEpsilon))

def frontierRightReflectedCutoff : ℝ :=
  frontierCStar + frontierEpsilon * Real.log 2

def frontierRightTailStart : ℝ :=
  frontierCStar + 2 * frontierEpsilon

def frontierRightTailTrace (C : ℝ) : ℝ :=
  C ^ 3 + 3 * C * frontierEpsilon ^ 2 + 2 * frontierEpsilon ^ 3 +
    2 * C - 2 * frontierA

def frontierRightTailTraceDeriv (C : ℝ) : ℝ :=
  3 * C ^ 2 + 3 * frontierEpsilon ^ 2 + 2

def frontierRightTailPiece (x1 x2 : ℝ) : ℝ :=
  let r := frontierRadius frontierEpsilon x1 x2
  let C := frontierCPlus frontierEpsilon x1 x2
  frontierRightTailTrace C - r * frontierRightTailTraceDeriv C

def frontierMajorant (x1 x2 : ℝ) : ℝ :=
  if frontierCPlus frontierEpsilon x1 x2 ≤ frontierCStar then
    frontierLeftPiece x1 x2
  else if frontierCPlus frontierEpsilon x1 x2 ≤ frontierCStar + 2 * frontierEpsilon then
    frontierCupPiece x1 x2
  else
    frontierRightTailPiece x1 x2

theorem frontierEpsilon_pos : 0 < frontierEpsilon := by
  rw [frontierEpsilon]
  positivity

theorem frontierEpsilon_ne_zero : frontierEpsilon ≠ 0 :=
  ne_of_gt frontierEpsilon_pos

theorem frontierEpsilon_sq : frontierEpsilon ^ 2 = (1 / 12 : ℝ) := by
  rw [frontierEpsilon]
  have hs_nonneg : 0 ≤ (3 : ℝ) := by norm_num
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt hs_nonneg
  rw [div_pow, hs]
  norm_num

theorem frontierCStar_eq :
    frontierCStar = 10 + Real.sqrt 3 / 36 := by
  have hs_nonneg : 0 ≤ (3 : ℝ) := by norm_num
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt hs_nonneg
  rw [frontierCStar, frontierA, frontierEpsilon]
  calc
    (10 : ℝ) + 2 * (Real.sqrt 3 / 6) ^ 3 =
        10 + Real.sqrt 3 / 36 := by
      rw [bmo_contact_cubic_identity (Real.sqrt 3) hs]

theorem frontierCStar_sub_epsilon_lt_A :
    frontierCStar - frontierEpsilon < frontierA := by
  rw [frontierCStar]
  nlinarith [frontierEpsilon_pos, frontierEpsilon_sq]

theorem frontierCStar_div_epsilon :
    frontierCStar / frontierEpsilon = 20 * Real.sqrt 3 + (1 / 6 : ℝ) := by
  have hs_nonneg : 0 ≤ (3 : ℝ) := by norm_num
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt hs_nonneg
  have hs0 : Real.sqrt 3 ≠ 0 := Real.sqrt_ne_zero'.2 (by norm_num)
  rw [frontierCStar_eq, frontierEpsilon]
  exact bmo_contact_exponent_identity (Real.sqrt 3) hs hs0

theorem frontierKL_eq_public_weight :
    frontierKL =
      (Real.sqrt 3 / 6) * Real.exp (-(20 * Real.sqrt 3 + (1 / 6 : ℝ))) := by
  rw [frontierKL, frontierCStar_div_epsilon, frontierEpsilon]

theorem frontierCupAlpha_lt_beta :
    frontierCupAlpha < frontierCupBeta := by
  rw [frontierCupAlpha, frontierCupBeta]
  linarith [frontierEpsilon_pos]

theorem frontierCupBeta_sub_alpha :
    frontierCupBeta - frontierCupAlpha = 2 * frontierEpsilon := by
  rw [frontierCupAlpha, frontierCupBeta]
  ring

theorem frontier_two_epsilon_cubed :
    2 * frontierEpsilon ^ 3 = frontierEpsilon / 6 := by
  calc
    2 * frontierEpsilon ^ 3 = 2 * frontierEpsilon * frontierEpsilon ^ 2 := by ring
    _ = 2 * frontierEpsilon * (1 / 12 : ℝ) := by rw [frontierEpsilon_sq]
    _ = frontierEpsilon / 6 := by ring

theorem frontierEpsilon_cube :
    frontierEpsilon ^ 3 = frontierEpsilon / 12 := by
  calc
    frontierEpsilon ^ 3 = frontierEpsilon * frontierEpsilon ^ 2 := by ring
    _ = frontierEpsilon * (1 / 12 : ℝ) := by rw [frontierEpsilon_sq]
    _ = frontierEpsilon / 12 := by ring

theorem frontierEpsilon_fourth :
    frontierEpsilon ^ 4 = (1 / 144 : ℝ) := by
  calc
    frontierEpsilon ^ 4 = frontierEpsilon ^ 2 * frontierEpsilon ^ 2 := by ring
    _ = (1 / 12 : ℝ) * (1 / 12 : ℝ) := by rw [frontierEpsilon_sq]
    _ = (1 / 144 : ℝ) := by norm_num

theorem frontierCupAlpha_le_A :
    frontierCupAlpha ≤ frontierA := by
  exact le_of_lt frontierCStar_sub_epsilon_lt_A

theorem frontierA_le_CupBeta :
    frontierA ≤ frontierCupBeta := by
  rw [frontierCupBeta, frontierCStar]
  nlinarith [frontierEpsilon_pos, frontier_two_epsilon_cubed]

theorem frontierRightReflectedConcavityCondition_def (D : ℝ) :
    frontierRightReflectedConcavityCondition D ↔
      6 * frontierEpsilon ^ 3 ≤ frontierKR * Real.exp (-(D / frontierEpsilon)) := by
  rfl

theorem frontierRightTailStart_beyond_reflected_cutoff :
    frontierRightReflectedCutoff < frontierRightTailStart := by
  rw [frontierRightReflectedCutoff, frontierRightTailStart]
  have hlog : Real.log 2 < (2 : ℝ) := by
    have hlog_one : Real.log 2 < (2 : ℝ) - 1 :=
      Real.log_lt_sub_one_of_pos (by norm_num) (by norm_num)
    linarith
  nlinarith [frontierEpsilon_pos]

theorem frontierRadius_lower_boundary (t : ℝ) :
    frontierRadius frontierEpsilon t (t ^ 2) = frontierEpsilon := by
  rw [frontierRadius]
  have harg : frontierEpsilon ^ 2 + t ^ 2 - t ^ 2 = frontierEpsilon ^ 2 := by
    ring
  rw [harg, Real.sqrt_sq_eq_abs, abs_of_pos frontierEpsilon_pos]

theorem frontierCPlus_lower_boundary (t : ℝ) :
    frontierCPlus frontierEpsilon t (t ^ 2) = t + frontierEpsilon := by
  rw [frontierCPlus, frontierRadius_lower_boundary]

theorem frontierLeftPiece_lower_boundary (t : ℝ) :
    frontierLeftPiece t (t ^ 2) = t ^ 3 := by
  rw [frontierLeftPiece, frontierCPlus_lower_boundary, frontierRadius_lower_boundary]
  field_simp [frontierEpsilon_ne_zero]
  ring

theorem frontierMajorant_left_boundary_eq
    (t : ℝ) (ht : t + frontierEpsilon ≤ frontierCStar) :
    frontierMajorant t (t ^ 2) = t ^ 3 := by
  rw [frontierMajorant, frontierCPlus_lower_boundary]
  rw [if_pos ht, frontierLeftPiece_lower_boundary]

theorem frontierRightTailTrace_boundary_sub (t : ℝ) :
    frontierRightTailTrace (t + frontierEpsilon) -
        frontierEpsilon * frontierRightTailTraceDeriv (t + frontierEpsilon) =
      t ^ 3 + 2 * (t - frontierA) := by
  rw [frontierRightTailTrace, frontierRightTailTraceDeriv]
  ring

theorem frontierPhi_right_of_ge (t : ℝ) (ht : frontierA ≤ t) :
    frontierPhi t = t ^ 3 + 2 * (t - frontierA) := by
  rw [frontierPhi]
  have hnonneg : 0 ≤ t - frontierA := by linarith
  rw [max_eq_left hnonneg]

theorem frontierPhi_left_of_le (t : ℝ) (ht : t ≤ frontierA) :
    frontierPhi t = t ^ 3 := by
  rw [frontierPhi]
  have hnonpos : t - frontierA ≤ 0 := by linarith
  rw [max_eq_right hnonpos]
  ring

theorem frontierMajorant_left_boundary_dominates
    (t : ℝ) (ht : t + frontierEpsilon ≤ frontierCStar) :
    frontierPhi t ≤ frontierMajorant t (t ^ 2) := by
  rw [frontierMajorant_left_boundary_eq t ht]
  have htA : t ≤ frontierA := by
    linarith [ht, frontierCStar_sub_epsilon_lt_A]
  rw [frontierPhi_left_of_le t htA]

theorem frontierCupPiece_lower_boundary_left_residual
    (t : ℝ) (htA : t ≤ frontierA) :
    frontierCupPiece t (t ^ 2) - frontierPhi t =
      (t - frontierCupAlpha) *
        (72 * frontierA * frontierEpsilon -
          36 * frontierA * (t - frontierCupAlpha) +
          30 * frontierEpsilon * (t - frontierCupAlpha) -
          12 * (t - frontierCupAlpha) ^ 2 + 13) / 12 := by
  rw [frontierPhi_left_of_le t htA]
  rw [frontierCupPiece]
  rw [frontierPhi_left_of_le frontierCupAlpha frontierCupAlpha_le_A,
    frontierPhi_right_of_ge frontierCupBeta frontierA_le_CupBeta]
  rw [frontierCupAlpha, frontierCupBeta, frontierCStar, frontierA]
  rw [frontier_two_epsilon_cubed]
  field_simp [frontierEpsilon_ne_zero]
  ring_nf
  rw [frontierEpsilon_cube, frontierEpsilon_fourth, frontierEpsilon_sq]
  ring

theorem frontierCupPiece_lower_boundary_right_residual
    (t : ℝ) (htA : frontierA ≤ t) :
    frontierCupPiece t (t ^ 2) - frontierPhi t =
      (frontierCupBeta - t) *
        (72 * frontierA * frontierEpsilon -
          36 * frontierA * (frontierCupBeta - t) -
          42 * frontierEpsilon * (frontierCupBeta - t) +
          12 * (frontierCupBeta - t) ^ 2 + 13) / 12 := by
  rw [frontierPhi_right_of_ge t htA]
  rw [frontierCupPiece]
  rw [frontierPhi_left_of_le frontierCupAlpha frontierCupAlpha_le_A,
    frontierPhi_right_of_ge frontierCupBeta frontierA_le_CupBeta]
  rw [frontierCupAlpha, frontierCupBeta, frontierCStar, frontierA]
  rw [frontier_two_epsilon_cubed]
  field_simp [frontierEpsilon_ne_zero]
  ring_nf
  rw [frontierEpsilon_cube, frontierEpsilon_fourth, frontierEpsilon_sq]
  ring

theorem frontierCupPiece_lower_boundary_dominates
    (t : ℝ) (hα : frontierCupAlpha ≤ t) (hβ : t ≤ frontierCupBeta) :
    frontierPhi t ≤ frontierCupPiece t (t ^ 2) := by
  by_cases htA : t ≤ frontierA
  · have hu_nonneg : 0 ≤ t - frontierCupAlpha := by linarith
    have hu_le_eps : t - frontierCupAlpha ≤ frontierEpsilon := by
      rw [frontierCupAlpha, frontierCStar]
      have htwo_nonneg : 0 ≤ 2 * frontierEpsilon ^ 3 := by
        rw [frontier_two_epsilon_cubed]
        linarith [frontierEpsilon_pos]
      nlinarith [htA, htwo_nonneg]
    have hneg_le_u : -frontierEpsilon ≤ t - frontierCupAlpha := by
      linarith [hu_nonneg, frontierEpsilon_pos]
    have hu_sq_le : (t - frontierCupAlpha) ^ 2 ≤ frontierEpsilon ^ 2 :=
      sq_le_sq' hneg_le_u hu_le_eps
    have heu_nonneg : 0 ≤ frontierEpsilon * (t - frontierCupAlpha) := by
      exact mul_nonneg (le_of_lt frontierEpsilon_pos) hu_nonneg
    have hbracket :
        0 ≤ 72 * frontierA * frontierEpsilon -
          36 * frontierA * (t - frontierCupAlpha) +
          30 * frontierEpsilon * (t - frontierCupAlpha) -
          12 * (t - frontierCupAlpha) ^ 2 + 13 := by
      rw [frontierA]
      nlinarith [frontierEpsilon_pos, frontierEpsilon_sq, hu_le_eps,
        hu_sq_le, heu_nonneg]
    have hres_nonneg :
        0 ≤ frontierCupPiece t (t ^ 2) - frontierPhi t := by
      rw [frontierCupPiece_lower_boundary_left_residual t htA]
      positivity
    linarith
  · have htA' : frontierA ≤ t := le_of_not_ge htA
    have hw_nonneg : 0 ≤ frontierCupBeta - t := by linarith
    have hw_le : frontierCupBeta - t ≤ 7 * frontierEpsilon / 6 := by
      rw [frontierCupBeta, frontierCStar]
      nlinarith [htA', frontier_two_epsilon_cubed]
    have hew_le :
        frontierEpsilon * (frontierCupBeta - t) ≤
          frontierEpsilon * (7 * frontierEpsilon / 6) :=
      mul_le_mul_of_nonneg_left hw_le (le_of_lt frontierEpsilon_pos)
    have hbracket :
        0 ≤ 72 * frontierA * frontierEpsilon -
          36 * frontierA * (frontierCupBeta - t) -
          42 * frontierEpsilon * (frontierCupBeta - t) +
          12 * (frontierCupBeta - t) ^ 2 + 13 := by
      rw [frontierA]
      nlinarith [frontierEpsilon_pos, frontierEpsilon_sq, hw_nonneg, hw_le, hew_le]
    have hres_nonneg :
        0 ≤ frontierCupPiece t (t ^ 2) - frontierPhi t := by
      rw [frontierCupPiece_lower_boundary_right_residual t htA']
      positivity
    linarith

theorem frontierMajorant_cup_boundary_eq
    (t : ℝ) (hleft : frontierCStar < t + frontierEpsilon)
    (hright : t + frontierEpsilon ≤ frontierCStar + 2 * frontierEpsilon) :
    frontierMajorant t (t ^ 2) = frontierCupPiece t (t ^ 2) := by
  rw [frontierMajorant, frontierCPlus_lower_boundary]
  have hnotLeft : ¬ t + frontierEpsilon ≤ frontierCStar := not_le.mpr hleft
  rw [if_neg hnotLeft, if_pos hright]

theorem frontierMajorant_cup_boundary_dominates
    (t : ℝ) (hleft : frontierCStar < t + frontierEpsilon)
    (hright : t + frontierEpsilon ≤ frontierCStar + 2 * frontierEpsilon) :
    frontierPhi t ≤ frontierMajorant t (t ^ 2) := by
  rw [frontierMajorant_cup_boundary_eq t hleft hright]
  apply frontierCupPiece_lower_boundary_dominates
  · rw [frontierCupAlpha]
    linarith
  · rw [frontierCupBeta]
    linarith

theorem frontierRightTailPiece_boundary (t : ℝ) (ht : frontierA ≤ t) :
    frontierRightTailPiece t (t ^ 2) = frontierPhi t := by
  rw [frontierRightTailPiece, frontierCPlus_lower_boundary,
    frontierRadius_lower_boundary, frontierRightTailTrace_boundary_sub,
    frontierPhi_right_of_ge t ht]

theorem frontierMajorant_right_boundary_eq
    (t : ℝ) (htC : frontierCStar + 2 * frontierEpsilon < t + frontierEpsilon)
    (htA : frontierA ≤ t) :
    frontierMajorant t (t ^ 2) = frontierPhi t := by
  rw [frontierMajorant, frontierCPlus_lower_boundary]
  have hnotLeft : ¬ t + frontierEpsilon ≤ frontierCStar := by
    linarith [frontierEpsilon_pos]
  have hnotMiddle :
      ¬ t + frontierEpsilon ≤ frontierCStar + 2 * frontierEpsilon := by
    exact not_le.mpr htC
  rw [if_neg hnotLeft, if_neg hnotMiddle, frontierRightTailPiece_boundary t htA]

theorem frontierMajorant_right_boundary_dominates
    (t : ℝ) (htC : frontierCStar + 2 * frontierEpsilon < t + frontierEpsilon)
    (htA : frontierA ≤ t) :
    frontierPhi t ≤ frontierMajorant t (t ^ 2) := by
  rw [frontierMajorant_right_boundary_eq t htC htA]

theorem frontierMajorant_boundaryDominates (t : ℝ) :
    frontierPhi t ≤ frontierMajorant t (t ^ 2) := by
  by_cases hleft : t + frontierEpsilon ≤ frontierCStar
  · exact frontierMajorant_left_boundary_dominates t hleft
  · have hleft' : frontierCStar < t + frontierEpsilon := not_le.mp hleft
    by_cases hmiddle : t + frontierEpsilon ≤ frontierCStar + 2 * frontierEpsilon
    · exact frontierMajorant_cup_boundary_dominates t hleft' hmiddle
    · have hright : frontierCStar + 2 * frontierEpsilon < t + frontierEpsilon :=
        not_le.mp hmiddle
      have htA : frontierA ≤ t := by
        have hAβ := frontierA_le_CupBeta
        rw [frontierCupBeta] at hAβ
        linarith [hAβ, hright]
      exact frontierMajorant_right_boundary_dominates t hright htA

theorem frontierOmega_lower_boundary (t : ℝ) :
    frontierOmega frontierEpsilon t (t ^ 2) := by
  rw [frontierOmega]
  constructor
  · rfl
  · nlinarith [sq_nonneg frontierEpsilon]

theorem frontierMajorant_boundary_gap_nonneg (t : ℝ) :
    0 ≤ frontierMajorant t (t ^ 2) - frontierPhi t := by
  have hdom := frontierMajorant_boundaryDominates t
  linarith

theorem frontier_bmo_public_sample_original_unconditional_boundary_support :
    (∀ t : ℝ, frontierOmega frontierEpsilon t (t ^ 2)) ∧
      ∀ t : ℝ, 0 ≤ frontierMajorant t (t ^ 2) - frontierPhi t := by
  exact ⟨frontierOmega_lower_boundary, frontierMajorant_boundary_gap_nonneg⟩

theorem frontier_bmo_public_sample_original_unconditional_boundaryDominates
    (t : ℝ) :
    frontierPhi t ≤ frontierMajorant t (t ^ 2) := by
  exact frontierMajorant_boundaryDominates t

theorem frontierBMOCenteredObjectiveIntegral_le_boundaryMajorantIntegral
    (g : ℝ → ℝ)
    (hphi : IntervalIntegrable (fun t : ℝ ↦ frontierPhi (g t)) volume
      (0 : ℝ) 1)
    (hmajorant : IntervalIntegrable
      (fun t : ℝ ↦ frontierMajorant (g t) ((g t) ^ 2)) volume
        (0 : ℝ) 1) :
    frontierBMOCenteredObjectiveIntegral g ≤
      ∫ t in (0 : ℝ)..1, frontierMajorant (g t) ((g t) ^ 2) := by
  rw [frontierBMOCenteredObjectiveIntegral]
  exact intervalIntegral.integral_mono (by norm_num) hphi hmajorant
    (fun t ↦ frontierMajorant_boundaryDominates (g t))

def frontierCenteredLinearWitness (t : ℝ) : ℝ :=
  t - (1 / 2 : ℝ)

theorem frontierCenteredLinearWitness_intervalIntegral (a b : ℝ) :
    (∫ t in a..b, frontierCenteredLinearWitness t) =
      (b ^ 2 / 2 - b / 2) - (a ^ 2 / 2 - a / 2) := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun t : ℝ ↦ t ^ 2 / 2 - t / 2) (f' := frontierCenteredLinearWitness)]
  · intro x _hx
    unfold frontierCenteredLinearWitness
    convert (((hasDerivAt_id x).pow 2).div_const 2).sub
      ((hasDerivAt_id x).div_const 2) using 1
    simp [id]
  · unfold frontierCenteredLinearWitness
    have hcont : Continuous (fun t : ℝ ↦ t - (1 / 2 : ℝ)) := by
      exact continuous_id.sub continuous_const
    exact hcont.intervalIntegrable a b

theorem frontierCenteredLinearWitness_intervalMean
    (a b : ℝ) (hab : a < b) :
    frontierBMOIntervalMean frontierCenteredLinearWitness a b =
      (a + b) / 2 - (1 / 2 : ℝ) := by
  have hne : b - a ≠ 0 := by linarith
  rw [frontierBMOIntervalMean, frontierCenteredLinearWitness_intervalIntegral]
  field_simp [hne]
  ring

theorem frontierCenteredLinearCenteredSquareIntegral (a b : ℝ) :
    (∫ t in a..b, (t - (a + b) / 2) ^ 2) = (b - a) ^ 3 / 12 := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun t : ℝ ↦ (t - (a + b) / 2) ^ 3 / 3)
    (f' := fun t ↦ (t - (a + b) / 2) ^ 2)]
  · ring
  · intro x _hx
    convert (((hasDerivAt_id x).sub_const ((a + b) / 2)).pow 3).div_const 3
      using 1
    simp [id]
  · have hcont : Continuous (fun t : ℝ ↦ (t - (a + b) / 2) ^ 2) := by
      exact (continuous_id.sub continuous_const).pow 2
    exact hcont.intervalIntegrable a b

theorem frontierCenteredLinearWitness_intervalVariance
    (a b : ℝ) (hab : a < b) :
    frontierBMOIntervalVariance frontierCenteredLinearWitness a b =
      (b - a) ^ 2 / 12 := by
  have hne : b - a ≠ 0 := by linarith
  rw [frontierBMOIntervalVariance,
    frontierCenteredLinearWitness_intervalMean a b hab]
  have hcongr :
      (∫ t in a..b,
          (frontierCenteredLinearWitness t - ((a + b) / 2 - 1 / 2)) ^ 2) =
        ∫ t in a..b, (t - (a + b) / 2) ^ 2 := by
    apply intervalIntegral.integral_congr
    intro t _ht
    unfold frontierCenteredLinearWitness
    ring
  rw [hcongr, frontierCenteredLinearCenteredSquareIntegral]
  field_simp [hne]

theorem frontierCenteredLinearWitness_intervalVarianceIntegrable (a b : ℝ) :
    IntervalIntegrable
      (fun t ↦
        (frontierCenteredLinearWitness t -
          frontierBMOIntervalMean frontierCenteredLinearWitness a b) ^ 2)
      volume a b := by
  have hcont :
      Continuous
        (fun t : ℝ ↦
          (frontierCenteredLinearWitness t -
            frontierBMOIntervalMean frontierCenteredLinearWitness a b) ^ 2) := by
    unfold frontierCenteredLinearWitness
    exact ((continuous_id.sub continuous_const).sub continuous_const).pow 2
  exact hcont.intervalIntegrable a b

theorem frontierCenteredLinearWitness_phiIntervalIntegrable :
    IntervalIntegrable (fun t : ℝ ↦ frontierPhi (frontierCenteredLinearWitness t))
      volume (0 : ℝ) 1 := by
  have hpoly :
      IntervalIntegrable (fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 3) volume
        (0 : ℝ) 1 := by
    have hcont : Continuous (fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 3) := by
      exact (continuous_id.sub continuous_const).pow 3
    exact hcont.intervalIntegrable 0 1
  refine hpoly.congr ?_
  intro t ht
  have htA : t - (1 / 2 : ℝ) ≤ frontierA := by
    rw [frontierA]
    rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1)] at ht
    linarith [ht.2]
  change (t - (1 / 2 : ℝ)) ^ 3 =
    frontierPhi (frontierCenteredLinearWitness t)
  rw [frontierCenteredLinearWitness, frontierPhi_left_of_le _ htA]

theorem frontierCenteredLinearWitness_meanIntegral :
    frontierBMOOriginalMeanIntegral frontierCenteredLinearWitness = 0 := by
  rw [frontierBMOOriginalMeanIntegral,
    frontierCenteredLinearWitness_intervalIntegral]
  norm_num

theorem frontierCenteredLinearWitness_secondMomentIntegral :
    frontierBMOOriginalSecondMomentIntegral frontierCenteredLinearWitness =
      (1 / 12 : ℝ) := by
  rw [frontierBMOOriginalSecondMomentIntegral]
  unfold frontierCenteredLinearWitness
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
    (f := fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 3 / 3)
    (f' := fun t ↦ (t - (1 / 2 : ℝ)) ^ 2)]
  · norm_num
  · intro x _hx
    convert (((hasDerivAt_id x).sub_const (1 / 2 : ℝ)).pow 3).div_const 3
      using 1
    simp [id]
  · have hcont : Continuous (fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 2) := by
      exact (continuous_id.sub continuous_const).pow 2
    exact hcont.intervalIntegrable 0 1

theorem frontierCenteredLinearWitness_objectiveIntegral :
    frontierBMOCenteredObjectiveIntegral frontierCenteredLinearWitness = 0 := by
  rw [frontierBMOCenteredObjectiveIntegral]
  calc
    ∫ t in (0 : ℝ)..1, frontierPhi (frontierCenteredLinearWitness t) =
        ∫ t in (0 : ℝ)..1, (t - (1 / 2 : ℝ)) ^ 3 := by
      apply intervalIntegral.integral_congr
      intro t ht
      have htA : t - (1 / 2 : ℝ) ≤ frontierA := by
        rw [frontierA]
        rw [Set.uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1)] at ht
        linarith [ht.2]
      change frontierPhi (frontierCenteredLinearWitness t) =
        (t - (1 / 2 : ℝ)) ^ 3
      rw [frontierCenteredLinearWitness, frontierPhi_left_of_le _ htA]
    _ = 0 := by
      rw [intervalIntegral.integral_eq_sub_of_hasDerivAt
        (f := fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 4 / 4)
        (f' := fun t ↦ (t - (1 / 2 : ℝ)) ^ 3)]
      · norm_num
      · intro x _hx
        convert (((hasDerivAt_id x).sub_const (1 / 2 : ℝ)).pow 4).div_const 4
          using 1
        simp [id]
      · have hcont : Continuous (fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 3) := by
          exact (continuous_id.sub continuous_const).pow 3
        exact hcont.intervalIntegrable 0 1

theorem frontierCenteredLinearWitness_admissible :
    frontierBMOCenteredFunctionAdmissible frontierCenteredLinearWitness := by
  refine ⟨?_, ?_, frontierCenteredLinearWitness_phiIntervalIntegrable,
    frontierCenteredLinearWitness_meanIntegral,
    frontierCenteredLinearWitness_secondMomentIntegral, ?_⟩
  · unfold frontierCenteredLinearWitness
    have hcont : Continuous (fun t : ℝ ↦ t - (1 / 2 : ℝ)) := by
      exact continuous_id.sub continuous_const
    exact hcont.intervalIntegrable 0 1
  · unfold frontierCenteredLinearWitness
    have hcont : Continuous (fun t : ℝ ↦ (t - (1 / 2 : ℝ)) ^ 2) := by
      exact (continuous_id.sub continuous_const).pow 2
    exact hcont.intervalIntegrable 0 1
  · intro a b ha hab hb
    refine ⟨frontierCenteredLinearWitness_intervalVarianceIntegrable a b, ?_⟩
    rw [frontierCenteredLinearWitness_intervalVariance a b hab]
    have hba_nonneg : 0 ≤ b - a := by linarith
    have hba_le : b - a ≤ 1 := by linarith
    nlinarith

theorem frontierCenteredLinearWitness_mem_objectiveSet :
    0 ∈ frontierBMOCenteredFunctionObjectiveSet := by
  refine ⟨frontierCenteredLinearWitness,
    frontierCenteredLinearWitness_admissible, ?_⟩
  exact frontierCenteredLinearWitness_objectiveIntegral.symm

theorem frontierBMOCenteredFunctionObjectiveSet_nonempty :
    frontierBMOCenteredFunctionObjectiveSet.Nonempty := by
  exact ⟨0, frontierCenteredLinearWitness_mem_objectiveSet⟩

theorem frontierBMOCenteredFunctionObjectiveSet_bddAbove_of_actualUpper
    (hupper : frontierBMOCenteredActualUpperBound) :
    BddAbove frontierBMOCenteredFunctionObjectiveSet := by
  exact ⟨frontierBMOPublicAnswer, hupper⟩

theorem frontierCenteredLinearWitness_originalObjective_mem :
    -(1985 / 2 : ℝ) ∈ frontierBMOOriginalFunctionObjectiveSet := by
  have hmem :=
    frontier_centered_objective_shift_mem_original_objectiveSet_of_admissible
      frontierCenteredLinearWitness frontierCenteredLinearWitness_admissible
  rw [frontierCenteredLinearWitness_objectiveIntegral] at hmem
  norm_num at hmem ⊢
  exact hmem

theorem frontierBMOOriginalFunctionObjectiveSet_nonempty :
    frontierBMOOriginalFunctionObjectiveSet.Nonempty := by
  exact ⟨-(1985 / 2 : ℝ), frontierCenteredLinearWitness_originalObjective_mem⟩

theorem frontierRightTailPiece_exists :
    ∃ B : ℝ → ℝ → ℝ,
      B = frontierRightTailPiece ∧
        frontierRightReflectedCutoff < frontierRightTailStart ∧
        (∀ t : ℝ, frontierA ≤ t → B t (t ^ 2) = frontierPhi t) ∧
        ∀ x1 x2 : ℝ,
          B x1 x2 =
            frontierRightTailTrace (frontierCPlus frontierEpsilon x1 x2) -
              frontierRadius frontierEpsilon x1 x2 *
                frontierRightTailTraceDeriv (frontierCPlus frontierEpsilon x1 x2) := by
  refine ⟨frontierRightTailPiece, rfl, frontierRightTailStart_beyond_reflected_cutoff, ?_, ?_⟩
  · intro t ht
    exact frontierRightTailPiece_boundary t ht
  · intro x1 x2
    rfl

def frontierStoppedLogCupObjective : ℝ :=
  2 * frontierEpsilon ^ 3 + frontierKL

def frontierStoppedLogCupRatio : ℝ :=
  Real.exp (-(frontierCStar / frontierEpsilon))

def frontierStoppedLogCupOptimizer (t : ℝ) : ℝ :=
  if t < frontierStoppedLogCupRatio / 2 then
    frontierCStar + frontierEpsilon
  else if t < frontierStoppedLogCupRatio then
    frontierCStar - frontierEpsilon
  else
    frontierEpsilon * (Real.log (1 / t) - 1)

theorem frontierStoppedLogCupRatio_pos :
    0 < frontierStoppedLogCupRatio := by
  rw [frontierStoppedLogCupRatio]
  positivity

theorem frontierStoppedLogCupRatio_ne_zero :
    frontierStoppedLogCupRatio ≠ 0 :=
  ne_of_gt frontierStoppedLogCupRatio_pos

theorem frontierKL_eq_epsilon_mul_stoppedLogCupRatio :
    frontierKL = frontierEpsilon * frontierStoppedLogCupRatio := by
  rw [frontierKL, frontierStoppedLogCupRatio]

theorem frontierStoppedLogCupRatio_lt_one :
    frontierStoppedLogCupRatio < 1 := by
  rw [frontierStoppedLogCupRatio]
  have hCStar_pos : 0 < frontierCStar := by
    rw [frontierCStar, frontierA]
    have hcube_pos : 0 < 2 * frontierEpsilon ^ 3 := by
      exact mul_pos (by norm_num) (pow_pos frontierEpsilon_pos 3)
    linarith
  have hquot_pos : 0 < frontierCStar / frontierEpsilon :=
    div_pos hCStar_pos frontierEpsilon_pos
  have hneg : -(frontierCStar / frontierEpsilon) < 0 := by
    linarith
  simpa using (Real.exp_lt_exp.mpr hneg)

theorem frontierStoppedLogCupRatio_half_pos :
    0 < frontierStoppedLogCupRatio / 2 := by
  exact div_pos frontierStoppedLogCupRatio_pos (by norm_num)

theorem frontierStoppedLogCupRatio_half_lt_ratio :
    frontierStoppedLogCupRatio / 2 < frontierStoppedLogCupRatio := by
  linarith [frontierStoppedLogCupRatio_pos]

theorem frontierStoppedLogCupOptimizer_left
    {t : ℝ} (ht : t < frontierStoppedLogCupRatio / 2) :
    frontierStoppedLogCupOptimizer t = frontierCStar + frontierEpsilon := by
  rw [frontierStoppedLogCupOptimizer, if_pos ht]

theorem frontierStoppedLogCupOptimizer_middle
    {t : ℝ}
    (hleft : frontierStoppedLogCupRatio / 2 ≤ t)
    (hright : t < frontierStoppedLogCupRatio) :
    frontierStoppedLogCupOptimizer t = frontierCStar - frontierEpsilon := by
  rw [frontierStoppedLogCupOptimizer, if_neg (not_lt.mpr hleft), if_pos hright]

theorem frontierStoppedLogCupOptimizer_tail
    {t : ℝ} (ht : frontierStoppedLogCupRatio ≤ t) :
    frontierStoppedLogCupOptimizer t =
      frontierEpsilon * (Real.log (1 / t) - 1) := by
  have hleft : ¬ t < frontierStoppedLogCupRatio / 2 := by
    exact not_lt.mpr (le_trans (le_of_lt frontierStoppedLogCupRatio_half_lt_ratio) ht)
  have hright : ¬ t < frontierStoppedLogCupRatio := not_lt.mpr ht
  rw [frontierStoppedLogCupOptimizer, if_neg hleft, if_neg hright]

theorem frontierStoppedLogCupOptimizer_zero_value :
    frontierStoppedLogCupOptimizer 0 = frontierCStar + frontierEpsilon := by
  exact frontierStoppedLogCupOptimizer_left
    (by linarith [frontierStoppedLogCupRatio_half_pos])

theorem frontierStoppedLogCupOptimizer_one_value :
    frontierStoppedLogCupOptimizer 1 = -frontierEpsilon := by
  have htail : frontierStoppedLogCupRatio ≤ (1 : ℝ) := by
    exact le_of_lt frontierStoppedLogCupRatio_lt_one
  rw [frontierStoppedLogCupOptimizer_tail htail]
  norm_num

theorem frontierStoppedLogCupObjective_eq_contact_ratio_form :
    frontierStoppedLogCupObjective =
      2 * frontierEpsilon ^ 3 +
        frontierEpsilon * frontierStoppedLogCupRatio := by
  rw [frontierStoppedLogCupObjective, frontierKL_eq_epsilon_mul_stoppedLogCupRatio]

theorem frontierStoppedLogCupObjective_mem_centered_objectiveSet_of_explicit_optimizer
    (hcentered :
      frontierBMOCenteredFunctionAdmissible frontierStoppedLogCupOptimizer)
    (hvalue :
    frontierBMOCenteredObjectiveIntegral frontierStoppedLogCupOptimizer =
        frontierStoppedLogCupObjective) :
    frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet := by
  refine ⟨frontierStoppedLogCupOptimizer, hcentered, ?_⟩
  exact hvalue.symm

theorem frontierRadius_center :
    frontierRadius frontierEpsilon 0 (frontierEpsilon ^ 2) = 0 := by
  rw [frontierRadius]
  have harg : frontierEpsilon ^ 2 + (0 : ℝ) ^ 2 - frontierEpsilon ^ 2 = 0 := by
    ring
  rw [harg, Real.sqrt_zero]

theorem frontierCPlus_center :
    frontierCPlus frontierEpsilon 0 (frontierEpsilon ^ 2) = 0 := by
  rw [frontierCPlus, frontierRadius_center]
  norm_num

theorem frontierMajorant_center_eq_stoppedLogCupObjective :
    frontierMajorant 0 (frontierEpsilon ^ 2) = frontierStoppedLogCupObjective := by
  rw [frontierMajorant, frontierCPlus_center]
  have hleft : (0 : ℝ) ≤ frontierCStar := by
    rw [frontierCStar, frontierA]
    have hcube : 0 ≤ 2 * frontierEpsilon ^ 3 :=
      mul_nonneg (by norm_num) (pow_nonneg (le_of_lt frontierEpsilon_pos) 3)
    linarith
  rw [if_pos hleft, frontierLeftPiece, frontierCPlus_center,
    frontierRadius_center, frontierStoppedLogCupObjective]
  field_simp [frontierEpsilon_ne_zero]
  rw [zero_div, Real.exp_zero]
  ring

theorem frontierStoppedLogCupObjective_eq_publicAnswer :
    frontierStoppedLogCupObjective = frontierBMOPublicAnswer := by
  have hs_nonneg : 0 ≤ (3 : ℝ) := by norm_num
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt hs_nonneg
  have hs0 : Real.sqrt 3 ≠ 0 := Real.sqrt_ne_zero'.2 (by norm_num)
  rw [frontierStoppedLogCupObjective, frontierKL_eq_public_weight, frontierEpsilon]
  rw [← bmo_contact_exponent_identity (Real.sqrt 3) hs hs0]
  exact bmo_public_answer_contact_form.symm

theorem frontierStoppedLogCupObjective_sub_centering_eq_originalSupremumValue :
    frontierStoppedLogCupObjective - (1985 / 2 : ℝ) =
      frontierBMOOriginalSupremumValue := by
  rw [frontierStoppedLogCupObjective_eq_publicAnswer, frontierBMOOriginalSupremumValue]

theorem frontierMajorant_center_eq_publicAnswer :
    frontierMajorant 0 (1 / 12 : ℝ) = frontierBMOPublicAnswer := by
  rw [← frontierEpsilon_sq, frontierMajorant_center_eq_stoppedLogCupObjective,
    frontierStoppedLogCupObjective_eq_publicAnswer]

theorem frontierBMOPublicAnswer_mem_centered_objectiveSet_of_stoppedLogCup
    (hmem : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOPublicAnswer ∈ frontierBMOCenteredFunctionObjectiveSet := by
  rwa [← frontierStoppedLogCupObjective_eq_publicAnswer]

theorem frontierBMOCenteredFunctionSupremum_eq_publicAnswer_of_actual_bounds
    (hupper : frontierBMOCenteredActualUpperBound)
    (hlower : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOCenteredFunctionSupremum = frontierBMOPublicAnswer := by
  have hbdd : BddAbove frontierBMOCenteredFunctionObjectiveSet :=
    frontierBMOCenteredFunctionObjectiveSet_bddAbove_of_actualUpper hupper
  have hpublic_mem :
      frontierBMOPublicAnswer ∈ frontierBMOCenteredFunctionObjectiveSet :=
    frontierBMOPublicAnswer_mem_centered_objectiveSet_of_stoppedLogCup hlower
  have hle : frontierBMOCenteredFunctionSupremum ≤ frontierBMOPublicAnswer := by
    exact csSup_le frontierBMOCenteredFunctionObjectiveSet_nonempty hupper
  have hge : frontierBMOPublicAnswer ≤ frontierBMOCenteredFunctionSupremum := by
    exact le_csSup hbdd hpublic_mem
  exact le_antisymm hle hge

theorem frontier_bmo_public_sample_original_unconditional_sSup_bridge
    (hupper : frontierBMOCenteredActualUpperBound)
    (_hlower : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOCenteredFunctionSupremum := by
  exact frontier_original_benchmark_eq_centered_supremum
    frontierBMOCenteredFunctionObjectiveSet_nonempty
    (frontierBMOCenteredFunctionObjectiveSet_bddAbove_of_actualUpper hupper)

theorem frontier_bmo_public_sample_original_unconditional_from_centered_sSup
    (hupper : frontierBMOCenteredActualUpperBound)
    (hlower : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer := by
  rw [frontier_bmo_public_sample_original_unconditional_sSup_bridge hupper hlower]
  exact frontierBMOCenteredFunctionSupremum_eq_publicAnswer_of_actual_bounds hupper hlower

theorem frontierBMOCenteredActualUpperBound_of_majorant_integral_bound
    (hmajorization :
      ∀ g : ℝ → ℝ, frontierBMOCenteredFunctionAdmissible g →
        frontierBMOCenteredObjectiveIntegral g ≤ frontierMajorant 0 (1 / 12 : ℝ)) :
    frontierBMOCenteredActualUpperBound := by
  intro y hy
  rcases hy with ⟨g, hg, rfl⟩
  exact le_trans (hmajorization g hg) (le_of_eq frontierMajorant_center_eq_publicAnswer)

theorem frontierBMOCenteredActualUpperBound_of_boundaryMajorantIntegral_bound
    (hmajorantIntegrable :
      ∀ g : ℝ → ℝ, frontierBMOCenteredFunctionAdmissible g →
        IntervalIntegrable
          (fun t : ℝ ↦ frontierMajorant (g t) ((g t) ^ 2)) volume
            (0 : ℝ) 1)
    (hmajorantBound :
      ∀ g : ℝ → ℝ, frontierBMOCenteredFunctionAdmissible g →
        (∫ t in (0 : ℝ)..1, frontierMajorant (g t) ((g t) ^ 2)) ≤
          frontierMajorant 0 (1 / 12 : ℝ)) :
    frontierBMOCenteredActualUpperBound := by
  apply frontierBMOCenteredActualUpperBound_of_majorant_integral_bound
  intro g hg
  rcases hg with ⟨hg_int, hg2_int, hphi, hmean, hsecondMoment, hvariance⟩
  have hg_adm :
      frontierBMOCenteredFunctionAdmissible g :=
    ⟨hg_int, hg2_int, hphi, hmean, hsecondMoment, hvariance⟩
  exact le_trans
    (frontierBMOCenteredObjectiveIntegral_le_boundaryMajorantIntegral
      g hphi (hmajorantIntegrable g hg_adm))
    (hmajorantBound g hg_adm)

theorem frontierBMOOriginalActualUpperBound_of_centered_majorant_integral_bound
    (hmajorization :
      ∀ g : ℝ → ℝ, frontierBMOCenteredFunctionAdmissible g →
        frontierBMOCenteredObjectiveIntegral g ≤ frontierMajorant 0 (1 / 12 : ℝ)) :
    frontierBMOOriginalActualUpperBound := by
  exact frontierBMOOriginalActualUpperBound_of_centered_upper
    (frontierBMOCenteredActualUpperBound_of_majorant_integral_bound hmajorization)

theorem frontierStoppedLogCupObjective_mem_centered_objectiveSet_of_optimizer
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g)
    (hvalue : frontierBMOCenteredObjectiveIntegral g = frontierStoppedLogCupObjective) :
    frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet := by
  refine ⟨g, hcentered, ?_⟩
  exact hvalue.symm

theorem frontierStoppedLogCupActualLowerBound_of_centered_optimizer
    (g : ℝ → ℝ)
    (hshifted : frontierBMOOriginalFunctionAdmissible (fun t ↦ g t - 10))
    (hg : IntervalIntegrable g volume (0 : ℝ) 1)
    (hg2 : IntervalIntegrable (fun t ↦ (g t) ^ 2) volume (0 : ℝ) 1)
    (hphi : IntervalIntegrable (fun t ↦ frontierPhi (g t)) volume (0 : ℝ) 1)
    (hmean : frontierBMOOriginalMeanIntegral g = 0)
    (hsecondMoment : frontierBMOOriginalSecondMomentIntegral g = (1 / 12 : ℝ))
    (hvalue : frontierBMOCenteredObjectiveIntegral g = frontierStoppedLogCupObjective) :
    frontierStoppedLogCupActualLowerBound := by
  have hmem :
      frontierBMOCenteredObjectiveIntegral g - (1985 / 2 : ℝ) ∈
        frontierBMOOriginalFunctionObjectiveSet :=
    frontier_centered_objective_shift_mem_original_objectiveSet
      g hshifted hg hg2 hphi hmean hsecondMoment
  rw [frontierStoppedLogCupActualLowerBound]
  convert hmem using 1
  rw [hvalue, frontierStoppedLogCupObjective_sub_centering_eq_originalSupremumValue]

theorem frontierStoppedLogCupActualLowerBound_of_centered_admissible_optimizer
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g)
    (hshifted : frontierBMOOriginalFunctionAdmissible (fun t ↦ g t - 10))
    (hvalue : frontierBMOCenteredObjectiveIntegral g = frontierStoppedLogCupObjective) :
    frontierStoppedLogCupActualLowerBound := by
  rcases hcentered with
    ⟨hg, hg2, hphi, hmean, hsecondMoment, _hvariance⟩
  exact frontierStoppedLogCupActualLowerBound_of_centered_optimizer
    g hshifted hg hg2 hphi hmean hsecondMoment hvalue

theorem frontierStoppedLogCupActualLowerBound_of_centered_optimizer_value
    (g : ℝ → ℝ)
    (hcentered : frontierBMOCenteredFunctionAdmissible g)
    (hvalue : frontierBMOCenteredObjectiveIntegral g = frontierStoppedLogCupObjective) :
    frontierStoppedLogCupActualLowerBound := by
  have hmem :
      frontierBMOCenteredObjectiveIntegral g - (1985 / 2 : ℝ) ∈
        frontierBMOOriginalFunctionObjectiveSet :=
    frontier_centered_objective_shift_mem_original_objectiveSet_of_admissible g hcentered
  rw [frontierStoppedLogCupActualLowerBound]
  convert hmem using 1
  rw [hvalue, frontierStoppedLogCupObjective_sub_centering_eq_originalSupremumValue]

theorem frontierStoppedLogCupActualLowerBound_of_centered_objectiveSet_mem
    (hmem : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierStoppedLogCupActualLowerBound := by
  rcases hmem with ⟨g, hcentered, hvalue⟩
  exact frontierStoppedLogCupActualLowerBound_of_centered_optimizer_value
    g hcentered hvalue.symm

theorem frontier_bmo_public_sample_original_unconditional_from_centered_obligations
    (hupper : frontierBMOCenteredActualUpperBound)
    (hlower : frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet) :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer := by
  exact frontierBMOOriginalFunctionBenchmarkValue_eq_publicAnswer_iff.mpr
    (frontierBMOOriginalFunctionSupremum_eq_value_of_actual_bounds
      (frontierBMOOriginalActualUpperBound_of_centered_upper hupper)
      (frontierStoppedLogCupActualLowerBound_of_centered_objectiveSet_mem hlower))

theorem frontier_bmo_public_sample_original_unconditional_reduction_to_actual_obligations :
    frontierBMOCenteredActualUpperBound →
      frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet →
        frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer := by
  intro hupper hlower
  exact frontier_bmo_public_sample_original_unconditional_from_centered_obligations
    hupper hlower

theorem frontier_bmo_public_sample_original_unconditional_missing_lower_obligation :
    frontierStoppedLogCupObjective = frontierBMOPublicAnswer ∧
      (frontierStoppedLogCupObjective ∈ frontierBMOCenteredFunctionObjectiveSet →
        frontierBMOPublicAnswer ∈ frontierBMOCenteredFunctionObjectiveSet) := by
  refine ⟨frontierStoppedLogCupObjective_eq_publicAnswer, ?_⟩
  intro hmem
  exact frontierBMOPublicAnswer_mem_centered_objectiveSet_of_stoppedLogCup hmem

theorem frontier_bmo_public_sample_original
    (frontier_unboundedNonsmoothBellmanUpper :
      frontierBMOOriginalActualUpperBound)
    (frontier_stoppedLogCupOptimizerLower :
      frontierStoppedLogCupActualLowerBound) :
    frontierBMOOriginalFunctionBenchmarkValue = frontierBMOPublicAnswer := by
  exact frontierBMOOriginalFunctionBenchmarkValue_eq_publicAnswer_iff.mpr
    (frontierBMOOriginalFunctionSupremum_eq_value_of_actual_bounds
      frontier_unboundedNonsmoothBellmanUpper frontier_stoppedLogCupOptimizerLower)

end

end AraLibrary.Analysis
