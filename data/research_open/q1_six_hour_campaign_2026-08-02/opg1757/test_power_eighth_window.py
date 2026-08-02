import unittest

from verify_power_eighth_window import (
    audit_falling_factors,
    audit_geometric_majorant,
    audit_profile_egf,
    audit_sharpened_endpoint,
    audit_window_constant,
)


class PowerEighthWindowTests(unittest.TestCase):
    def test_profile_egf(self) -> None:
        self.assertGreater(audit_profile_egf(7), 0)

    def test_sharpened_endpoint(self) -> None:
        self.assertGreater(audit_sharpened_endpoint(30), 0)

    def test_falling_factors(self) -> None:
        self.assertGreater(audit_falling_factors(12), 0)

    def test_geometric_majorant(self) -> None:
        self.assertGreater(audit_geometric_majorant(50), 0)

    def test_window_constant(self) -> None:
        self.assertEqual(audit_window_constant(), 8)


if __name__ == "__main__":
    unittest.main()
