import Mathlib

/- Algebraic kernel of the weighted cactus-block proof. -/

theorem cycle_block_rayleigh_identity (R M : ℝ) :
    R * R - (R - M) * R = R * M := by
  ring

theorem cactus_same_cycle_rayleigh_nonnegative
    (H R M : ℝ) (hR : 0 ≤ R) (hM : 0 ≤ M) :
    0 ≤ H^2 * (R * R - (R - M) * R) := by
  rw [cycle_block_rayleigh_identity]
  positivity

theorem distinct_block_rayleigh_zero
    (A A_e B B_f H : ℝ) :
    (A_e * B * H) * (A * B_f * H) -
        (A * B * H) * (A_e * B_f * H) = 0 := by
  ring
