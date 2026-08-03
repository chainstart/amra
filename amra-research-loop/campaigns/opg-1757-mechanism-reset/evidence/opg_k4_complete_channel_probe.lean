import Mathlib

/-!
Exact K4 complete-channel probe for OPG-1757.

Let the marked disjoint edges be 01 and 23, and let `a,b,c,d` be the
activities of 02,03,12,13.  Direct forest enumeration gives the Rayleigh
difference on the left.  Its negative coefficient `-2*a*b*c*d` is absorbed
by the complete square on the right.

This is a finite-host mechanism probe, not the arbitrary-host theorem.
-/

theorem k4_disjoint_forest_rayleigh_complete_channel_identity
    (a b c d : ℝ) :
    a^2 * d^2 + a^2 * d - 2 * a * b * c * d + a * d^2 + a * d +
        b^2 * c^2 + b^2 * c + b * c^2 + b * c =
      (a * d - b * c)^2 + a * d * (a + d + 1) + b * c * (b + c + 1) := by
  ring

theorem k4_disjoint_forest_rayleigh_complete_channel_nonnegative
    (a b c d : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hd : 0 ≤ d) :
    0 ≤ a^2 * d^2 + a^2 * d - 2 * a * b * c * d + a * d^2 + a * d +
        b^2 * c^2 + b^2 * c + b * c^2 + b * c := by
  rw [k4_disjoint_forest_rayleigh_complete_channel_identity]
  positivity
