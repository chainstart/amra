"""Regression tests for transverse Phi_6 switch-cube fibre rigidity."""

import unittest

from verify_phi6_switch_cube_transverse_fiber_rigidity import (
    equality_models_certificate,
    one_dimensional_automaton_certificate,
    rank_two_exhaustion_certificate,
    transverse_projection_certificate,
)


class Phi6SwitchCubeTransverseFiberRigidityTests(unittest.TestCase):
    def test_one_dimensional_forbidden_word_characterization(self) -> None:
        result = one_dimensional_automaton_certificate()
        self.assertEqual(result["words_checked"], sum(2**n - 1 for n in range(1, 13)))
        self.assertFalse(result["equivalence_failures"])
        self.assertTrue(result["pass"])

    def test_rank_two_minimum_and_equality_cases(self) -> None:
        result = rank_two_exhaustion_certificate()
        self.assertEqual(result["masks_checked"], 511)
        self.assertEqual(result["minimum_mass"], 4)
        self.assertEqual(result["equality_cases"], 4)
        self.assertTrue(result["equality_cases_exact"])
        self.assertTrue(result["pass"])

    def test_sharp_equality_models(self) -> None:
        result = equality_models_certificate()
        for record in result["records"]:
            self.assertEqual(record["base_mass"], 2 ** record["rank"])
            self.assertEqual(record["states"], 2 ** record["rank"])
            self.assertTrue(record["all_states_are_masks"])
            self.assertTrue(record["all_state_masses_equal"])
        self.assertTrue(result["pass"])

    def test_transverse_projection_bound_and_endpoint_gap(self) -> None:
        result = transverse_projection_certificate()
        self.assertTrue(result["sharp_C_equals_2_to_k"])
        self.assertTrue(result["sharp_total_identity"])
        self.assertTrue(result["endpoint_full_cube_exceeds_C"])
        self.assertEqual(result["endpoint_projected_fibre_cap"], result["endpoint_C"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
