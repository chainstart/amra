import Mathlib

/- Independent repair/reconstruction of the finite triangle probe. -/

theorem audit_triangle_scaled_random_cluster_rayleigh_identity
    (x y z q : ℝ) :
    (1 + y + z + q * y * z) * (1 + x + z + q * x * z) -
        (1 + x + y + z + x * y + x * z + y * z + q * x * y * z) *
          (1 + q * z) =
      z * (1 - q) * (1 + z) := by
  ring

theorem audit_triangle_scaled_random_cluster_rayleigh_nonnegative
    (x y z q : ℝ) (hz : 0 ≤ z) (_hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    0 ≤
      (1 + y + z + q * y * z) * (1 + x + z + q * x * z) -
        (1 + x + y + z + x * y + x * z + y * z + q * x * y * z) *
          (1 + q * z) := by
  rw [audit_triangle_scaled_random_cluster_rayleigh_identity]
  have h_one_sub_q : 0 ≤ 1 - q := by linarith
  have h_one_add_z : 0 ≤ 1 + z := by linarith
  exact mul_nonneg (mul_nonneg hz h_one_sub_q) h_one_add_z
