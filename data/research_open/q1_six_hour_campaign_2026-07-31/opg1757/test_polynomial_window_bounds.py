import unittest

from verify_polynomial_window_bounds import (
    audit_constant_chain,
    audit_falling_factors,
    audit_newton_triangle,
    audit_profile_mass,
    audit_window_constant,
)


class PolynomialWindowBoundsTests(unittest.TestCase):
    def test_profile_mass(self) -> None:
        self.assertGreater(audit_profile_mass(7), 0)

    def test_constant_chain(self) -> None:
        self.assertGreater(audit_constant_chain(30), 0)

    def test_newton_triangle(self) -> None:
        self.assertGreater(audit_newton_triangle(7), 0)

    def test_falling_factors(self) -> None:
        self.assertGreater(audit_falling_factors(9), 0)

    def test_window_constant(self) -> None:
        self.assertEqual(audit_window_constant(), 67)


if __name__ == "__main__":
    unittest.main()
