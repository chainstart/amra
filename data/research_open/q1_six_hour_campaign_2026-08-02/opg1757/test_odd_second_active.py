import unittest

from verify_odd_second_active import (
    audit_bases_and_finite_recurrence,
    audit_fixed_kernel,
    audit_top_remainders,
)


class OddSecondActiveTests(unittest.TestCase):
    def test_fixed_kernel(self) -> None:
        self.assertEqual(audit_fixed_kernel(), 57)

    def test_top_remainders(self) -> None:
        identities, shifted, exceptional = audit_top_remainders()
        self.assertEqual(identities, 4)
        self.assertEqual(shifted, 20)
        self.assertEqual(exceptional, 10)

    def test_bases_and_recurrence(self) -> None:
        self.assertGreater(audit_bases_and_finite_recurrence(10), 0)


if __name__ == "__main__":
    unittest.main()
