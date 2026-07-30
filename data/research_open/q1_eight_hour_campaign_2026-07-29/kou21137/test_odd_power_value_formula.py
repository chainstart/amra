#!/usr/bin/env python3
"""Independent p=5 check of the A wr C_p power-value formula."""

import itertools
import unittest


P = 5
IDENTITY = 0


def d10_multiply(left: int, right: int) -> int:
    """Multiply r^i s^j, encoded as 2*i+j, with srs=r^-1."""
    i, j = divmod(left, 2)
    k, ell = divmod(right, 2)
    return 2 * ((i + (k if j == 0 else -k)) % 5) + ((j + ell) % 2)


TABLE = tuple(
    tuple(d10_multiply(left, right) for right in range(10))
    for left in range(10)
)
INVERSE = tuple(
    next(right for right in range(10) if TABLE[left][right] == IDENTITY)
    for left in range(10)
)


def group_power(element: int, exponent: int) -> int:
    result = IDENTITY
    for _ in range(exponent):
        result = TABLE[result][element]
    return result


def wreath_multiply(
    left: tuple[tuple[int, ...], int],
    right: tuple[tuple[int, ...], int],
) -> tuple[tuple[int, ...], int]:
    """Multiply in D_10^5 semidirect C_5 using cyclic coordinate shift."""
    left_base, left_top = left
    right_base, right_top = right
    shifted_right = tuple(
        right_base[(coordinate - left_top) % P] for coordinate in range(P)
    )
    return (
        tuple(
            TABLE[left_base[coordinate]][shifted_right[coordinate]]
            for coordinate in range(P)
        ),
        (left_top + right_top) % P,
    )


def wreath_fifth_power(
    element: tuple[tuple[int, ...], int],
) -> tuple[tuple[int, ...], int]:
    result = ((IDENTITY,) * P, 0)
    for _ in range(P):
        result = wreath_multiply(result, element)
    return result


def conjugacy_classes() -> list[frozenset[int]]:
    unseen = set(range(10))
    classes: list[frozenset[int]] = []
    while unseen:
        element = min(unseen)
        conjugates = frozenset(
            TABLE[TABLE[INVERSE[g]][element]][g] for g in range(10)
        )
        classes.append(conjugates)
        unseen.difference_update(conjugates)
    return classes


class OddPowerFormulaRegression(unittest.TestCase):
    def test_d10_wreath_c5_exact_value_set(self) -> None:
        fifth_values = {
            group_power(element, P) for element in range(10)
        }
        expected = set(itertools.product(fifth_values, repeat=P))
        for conjugacy_class in conjugacy_classes():
            expected.update(itertools.product(conjugacy_class, repeat=P))

        actual: set[tuple[int, ...]] = set()
        for base in itertools.product(range(10), repeat=P):
            for top in range(P):
                power_base, power_top = wreath_fifth_power((base, top))
                self.assertEqual(power_top, 0)
                actual.add(power_base)

        self.assertEqual(len(expected), 7840)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
