import Mathlib

/-!
An exact finite-host probe for survivor M008.

After the random-cluster scaling `v_e = q * x_e` and division by `q^3`,
the triangle polynomial is

  1 + x + y + z + xy + xz + yz + qxyz.

The displayed identity is its Rayleigh difference in `x,y`.  This verifies
the route on one host only; it is not a proof of OPG-1757.
-/

theorem triangle_scaled_random_cluster_rayleigh_identity
    (x y z q : ℝ) :
    (1 + y + z + q * y * z) * (1 + x + z + q * x * z) -
        (1 + x + y + z + x * y + x * z + y * z + q * x * y * z) *
          (1 + q * z) =
      z * (1 - q) * (1 + z) := by
  ring

theorem triangle_scaled_random_cluster_rayleigh_nonnegative
    (x y z q : ℝ) (hz : 0 ≤ z) (_hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    0 ≤
      (1 + y + z + q * y * z) * (1 + x + z + q * x * z) -
        (1 + x + y + z + x * y + x * z + y * z + q * x * y * z) *
          (1 + q * z) := by
  rw [triangle_scaled_random_cluster_rayleigh_identity]
  have h_one_sub_q : 0 ≤ 1 - q := by linarith
  have h_one_add_z : 0 ≤ 1 + z := by linarith
  exact mul_nonneg (mul_nonneg hz h_one_sub_q) h_one_add_z
