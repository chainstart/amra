#!/usr/bin/env python3
"""Unit tests for the table-only KOU-21.137 classifier."""

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("verify_smallgroups_classification.py")
SPEC = importlib.util.spec_from_file_location("kou_classifier", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def cyclic_table(order: int) -> list[list[int]]:
    return [
        [(left + right) % order for right in range(order)]
        for left in range(order)
    ]


def dihedral_eight_wreath_c2_table() -> list[list[int]]:
    """Construct D8 wr C2 directly, without asking GAP for predicates."""

    def dihedral_product(
        left: tuple[int, int], right: tuple[int, int]
    ) -> tuple[int, int]:
        left_rotation, left_reflection = left
        right_rotation, right_reflection = right
        sign = -1 if left_reflection else 1
        return (
            (left_rotation + sign * right_rotation) % 4,
            (left_reflection + right_reflection) % 2,
        )

    seed_elements = [
        (rotation, reflection)
        for rotation in range(4)
        for reflection in range(2)
    ]
    elements = [
        (left, right, top)
        for left in seed_elements
        for right in seed_elements
        for top in range(2)
    ]
    positions = {element: index for index, element in enumerate(elements)}

    table: list[list[int]] = []
    for left_seed, right_seed, left_top in elements:
        row: list[int] = []
        for other_left, other_right, right_top in elements:
            if left_top:
                other_left, other_right = other_right, other_left
            product = (
                dihedral_product(left_seed, other_left),
                dihedral_product(right_seed, other_right),
                (left_top + right_top) % 2,
            )
            row.append(positions[product])
        table.append(row)
    return table


class ClassifierTests(unittest.TestCase):
    def test_cyclic_eight_has_exponent_eight_but_abelian_squares(self) -> None:
        result = MODULE.audit_table(8, 1, cyclic_table(8))
        self.assertEqual(result["exponent"], 8)
        self.assertTrue(result["square_values_form_subgroup"])
        self.assertFalse(result["square_values_nonabelian"])
        self.assertFalse(result["hit"])

    def test_corrupt_latin_table_fails_closed(self) -> None:
        table = cyclic_table(8)
        table[0][0] = 1
        with self.assertRaises(MODULE.AuditFailure):
            MODULE.audit_table(8, 1, table)

    def test_nonassociative_positive_candidate_fails_closed(self) -> None:
        # The full production path audits associativity for every table.  This
        # direct check makes the failure contract explicit.
        table = cyclic_table(8)
        table[1], table[2] = table[2], table[1]
        with self.assertRaises(MODULE.AuditFailure):
            MODULE.audit_table(8, 1, table)

    def test_d8_wreath_c2_exercises_positive_invariants(self) -> None:
        result = MODULE.audit_table(
            128, 928, dihedral_eight_wreath_c2_table()
        )
        self.assertTrue(result["hit"])
        self.assertEqual(result["exponent"], 8)
        self.assertEqual(result["square_value_count"], 16)
        self.assertEqual(result["derived_subgroup_size"], 16)
        self.assertEqual(result["frattini_subgroup_size"], 16)
        self.assertTrue(result["derived_equals_square_values"])
        self.assertTrue(result["frattini_equals_square_values"])


if __name__ == "__main__":
    unittest.main()
