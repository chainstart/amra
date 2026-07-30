#!/usr/bin/env python3
"""Exact check of the odd-prime Frobenius branch with nonabelian kernel."""

import unittest


MODULUS = 7
KERNEL = tuple(
    (a, b, c)
    for a in range(MODULUS)
    for b in range(MODULUS)
    for c in range(MODULUS)
)
IDENTITY = (0, 0, 0)


def kernel_mul(left, right):
    """Multiply coordinates in UT_3(F_7)."""
    a, b, c = left
    d, e, f = right
    return (
        (a + d) % MODULUS,
        (b + e) % MODULUS,
        (c + f + a * e) % MODULUS,
    )


def kernel_inv(value):
    a, b, c = value
    return (-a % MODULUS, -b % MODULUS, (-c + a * b) % MODULUS)


def alpha(value, exponent=1):
    """The order-three automorphism (a,b,c) -> (2a,2b,4c)."""
    scalar = pow(2, exponent % 3, MODULUS)
    central_scalar = scalar * scalar % MODULUS
    a, b, c = value
    return (
        scalar * a % MODULUS,
        scalar * b % MODULUS,
        central_scalar * c % MODULUS,
    )


GROUP = tuple((value, exponent) for value in KERNEL for exponent in range(3))


def group_mul(left, right):
    value, exponent = left
    other, other_exponent = right
    return (
        kernel_mul(value, alpha(other, exponent)),
        (exponent + other_exponent) % 3,
    )


def group_inv(element):
    value, exponent = element
    return alpha(kernel_inv(value), -exponent), -exponent % 3


def group_pow(element, exponent):
    result = (IDENTITY, 0)
    for _ in range(exponent):
        result = group_mul(result, element)
    return result


def conjugate(element, by):
    return group_mul(group_mul(group_inv(by), element), by)


class NonabelianFrobeniusKernelRegression(unittest.TestCase):
    def test_ut3_semidirect_c3(self) -> None:
        # K is visibly nonabelian.
        x = (1, 0, 0)
        y = (0, 1, 0)
        self.assertNotEqual(kernel_mul(x, y), kernel_mul(y, x))

        # Alpha is an order-three automorphism, and both nonidentity powers
        # act fixed-point-freely.
        for left in KERNEL:
            self.assertEqual(alpha(alpha(alpha(left))), left)
            for right in KERNEL:
                self.assertEqual(
                    alpha(kernel_mul(left, right)),
                    kernel_mul(alpha(left), alpha(right)),
                )
        for exponent in (1, 2):
            self.assertEqual(
                [value for value in KERNEL if alpha(value, exponent) == value],
                [IDENTITY],
            )

        # The raw cube-value set is exactly the Frobenius kernel.
        cube_values = {group_pow(element, 3) for element in GROUP}
        embedded_kernel = {(value, 0) for value in KERNEL}
        self.assertEqual(cube_values, embedded_kernel)

        # Every element outside the kernel has its full kernel coset as its
        # conjugacy class, the exact Camina condition used by the theorem.
        for element in GROUP:
            if element[1] == 0:
                continue
            conjugacy_class = {conjugate(element, by) for by in GROUP}
            expected_coset = {(value, element[1]) for value in KERNEL}
            self.assertEqual(conjugacy_class, expected_coset)


if __name__ == "__main__":
    unittest.main()
