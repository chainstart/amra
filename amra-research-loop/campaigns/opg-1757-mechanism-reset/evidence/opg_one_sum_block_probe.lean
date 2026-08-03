import Mathlib

/- Algebraic kernels for the one-sum forest-polynomial factorization. -/

theorem one_sum_same_block_rayleigh
    (A Ae Af Aef H : ℝ) :
    (Ae * H) * (Af * H) - (A * H) * (Aef * H) =
      H^2 * (Ae * Af - A * Aef) := by
  ring

theorem one_sum_different_blocks_rayleigh
    (A Ae B Bf : ℝ) :
    (Ae * B) * (A * Bf) - (A * B) * (Ae * Bf) = 0 := by
  ring
