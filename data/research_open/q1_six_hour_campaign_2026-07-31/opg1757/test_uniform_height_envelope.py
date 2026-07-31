import unittest

from verify_uniform_height_envelope import (
    audit_arithmetic,
    audit_atom_budget,
    audit_master_ledger,
    audit_q_zero,
)


class UniformHeightEnvelopeTests(unittest.TestCase):
    def test_atom_budget(self) -> None:
        self.assertGreater(audit_atom_budget(5), 0)

    def test_master_ledger(self) -> None:
        self.assertGreater(audit_master_ledger(10), 0)

    def test_arithmetic(self) -> None:
        self.assertEqual(audit_arithmetic(100), 100)

    def test_q_zero(self) -> None:
        self.assertEqual(audit_q_zero(), 37)


if __name__ == "__main__":
    unittest.main()
