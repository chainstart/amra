#!/usr/bin/env python3
"""Exact Farey-cell integration for the sawtooth sums in Erdős #1002."""

from fractions import Fraction
from math import gcd, log


def farey(order: int):
    a, b, c, d = 0, 1, 1, order
    yield Fraction(0)
    while c <= order:
        yield Fraction(c, d)
        multiplier = (order + b) // d
        a, b, c, d = c, d, multiplier * c - a, multiplier * d - b


def statistics(n: int):
    breakpoints = list(farey(n))
    slope = n * (n + 1) // 2
    intercept = Fraction(n, 2)
    mean = Fraction(0)
    second_moment = Fraction(0)
    absolute_mean = 0.0
    tails = {a: 0.0 for a in (1, 2, 4, 8, 16)}

    for left, right in zip(breakpoints, breakpoints[1:]):
        width = right - left
        s_left = float(intercept - slope * left)
        s_right = float(intercept - slope * right)
        mean += intercept * width - Fraction(slope, 2) * (right**2 - left**2)
        second_moment += (
            intercept**2 * width
            - intercept * slope * (right**2 - left**2)
            + Fraction(slope**2, 3) * (right**3 - left**3)
        )
        if s_left * s_right <= 0:
            absolute_mean += (s_left**2 + s_right**2) / (2 * slope)
        else:
            absolute_mean += abs((s_left + s_right) * float(width) / 2)

        for a in tails:
            threshold = a * log(n)
            if s_left > threshold:
                tails[a] += max(
                    0.0, min(float(width), (s_left - threshold) / slope)
                )
            if s_right < -threshold:
                tails[a] += max(
                    0.0, min(float(width), (-threshold - s_right) / slope)
                )

        if right < 1:
            # At a reduced fraction p/q, exactly floor(n/q) of the floor
            # functions jump.
            intercept += n // right.denominator

    covariance_formula = sum(
        Fraction(gcd(k, ell) ** 2, k * ell)
        for k in range(1, n + 1)
        for ell in range(1, n + 1)
    ) / 12
    assert mean == 0
    assert second_moment == covariance_formula
    assert second_moment >= Fraction(n, 12)  # diagonal terms alone
    return {
        "farey_cells": len(breakpoints) - 1,
        "absolute_mean": absolute_mean,
        "absolute_mean_over_log_n": absolute_mean / log(n),
        "second_moment": float(second_moment),
        "tails": tails,
    }


expected = {
    64: (1260, 1.7191609543587907, 14.866077012953117),
    128: (5022, 2.104718319420048, 30.587030796338166),
    256: (19948, 2.5395639812071353, 62.385413480517066),
}
results = {}
for n, (cells, absolute_mean, second_moment) in expected.items():
    result = statistics(n)
    assert result["farey_cells"] == cells
    assert abs(result["absolute_mean"] - absolute_mean) < 1e-12
    assert abs(result["second_moment"] - second_moment) < 1e-12
    results[n] = result

print("PASS #1002:", results)
