import unittest

from verify_even_second_active_universal import (
    audit_four_layer_recurrence,
    audit_tail_induction,
)


class EvenSecondActiveUniversalTests(unittest.TestCase):
    def test_four_layer_recurrence(self) -> None:
        result = audit_four_layer_recurrence()
        self.assertEqual(result["initial_kernel_positive_monomials"], 112)
        self.assertEqual(result["layer4_positive_monomials"], 59)
        self.assertEqual(result["layer_growth_positive_monomials"], 52)

    def test_tail_induction(self) -> None:
        result = audit_tail_induction()
        self.assertEqual(result["boundary_polynomial_monomials"], 31)
        self.assertEqual(result["base_values"], 4)
        self.assertEqual(result["direct_recurrence_coefficients"], 105)


if __name__ == "__main__":
    unittest.main()
