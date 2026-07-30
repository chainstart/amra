#!/usr/bin/env python3
"""Arithmetic audit for the metabelian class-2p proof."""

from math import comb
import unittest


class Metabelian2pCoefficientAudit(unittest.TestCase):
    def test_unique_p_adic_exception_and_norm_product(self) -> None:
        for p in (3, 5, 7, 11):
            with self.subTest(p=p):
                exceptional = []
                for k in range(2 * p - 2):
                    coefficient = comb(p * p, k + 1)
                    if coefficient % (p * p):
                        exceptional.append((k, coefficient))
                self.assertEqual(len(exceptional), 1)
                self.assertEqual(exceptional[0][0], p - 1)
                self.assertEqual(exceptional[0][1] % p, 0)
                self.assertNotEqual(exceptional[0][1] % (p * p), 0)

                # Coefficients of sigma_p(1+X)sigma_p(1+Y).
                for i in range(p):
                    for j in range(p):
                        coefficient = comb(p, i + 1) * comb(p, j + 1)
                        if i < p - 1 and j < p - 1:
                            self.assertEqual(coefficient % (p * p), 0)
                        elif i == p - 1 and j == p - 1:
                            self.assertEqual(i + j, 2 * p - 2)
                            self.assertEqual(coefficient, 1)
                        else:
                            self.assertEqual(coefficient % p, 0)


if __name__ == "__main__":
    unittest.main()
