#!/usr/bin/env python3
"""Regression tests for the aperiodic small-divisor no-go."""

import unittest

from verify_aperiodic_small_divisor_nogo import run_all


class AperiodicSmallDivisorNoGoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run_all()

    def test_rabin_irreducibility(self) -> None:
        self.assertTrue(self.result["rabin"]["pass"])

    def test_root_geometry(self) -> None:
        self.assertTrue(self.result["root_geometry"]["pass"])

    def test_small_divisor_rate(self) -> None:
        self.assertTrue(self.result["small_divisor"]["pass"])

    def test_signed_escape(self) -> None:
        self.assertTrue(self.result["signed_escape"]["pass"])
        self.assertTrue(self.result["signed_positive_quotient_constructed"])

    def test_scope_firewall(self) -> None:
        self.assertFalse(self.result["power_large_family_constructed"])
        self.assertFalse(self.result["original_problem_proved"])


if __name__ == "__main__":
    unittest.main()
