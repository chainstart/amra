import unittest

from verify_even_second_active_partial import (
    certify_fixed_layer_obstruction,
    certify_low_bulk_columns,
    certify_top_six,
)


class EvenSecondActivePartialTests(unittest.TestCase):
    def test_low_bulk_columns(self) -> None:
        result = certify_low_bulk_columns()
        self.assertEqual(result["universal_columns"], 31)
        self.assertEqual(result["positive_shifted_monomials"], 682)

    def test_top_six(self) -> None:
        result = certify_top_six()
        self.assertEqual(result["universal_top_coefficients"], 6)
        self.assertEqual(result["exceptional_values"], 4)
        self.assertEqual(result["boundary_six_coefficients"], 5)

    def test_fixed_layer_obstruction(self) -> None:
        result = certify_fixed_layer_obstruction()
        self.assertEqual(result["universal_delta_identities"], 5)
        self.assertEqual(result["fixed_depth_symbolic_witnesses"], 3)


if __name__ == "__main__":
    unittest.main()
