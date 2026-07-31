#!/usr/bin/env python3

import unittest

from verify_fixed_deficit_leading_symbol import (
    marked_one_block_symbolic_audit,
    profile_collapse_audit,
)


class FixedDeficitLeadingSymbolTests(unittest.TestCase):
    def test_marked_one_block_expansion(self) -> None:
        self.assertIn("a**2*v", marked_one_block_symbolic_audit())

    def test_profile_collapse(self) -> None:
        self.assertEqual(profile_collapse_audit(7), 8)


if __name__ == "__main__":
    unittest.main()
