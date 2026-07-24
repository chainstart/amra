#!/usr/bin/env python3
"""Independent arithmetic and coupling checks for the R003 audit of Erdős #522."""

from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction
from itertools import product


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


eta = Fraction(1, 100)
beta = Fraction(1, 200)

exponents = {
    "smooth_endpoint_borel_cantelli_in_j": 4
    * (2 * beta + 6 * eta - Fraction(1, 2)),
    "small_value_borel_cantelli_in_j": 4
    * (10 * eta - Fraction(1, 2)),
    "block_lipschitz_error": eta - Fraction(1, 8),
    "small_value_target": -2 * eta,
    "jensen_amplified_log_error": Fraction(401, 400) - beta,
}

require(exponents["smooth_endpoint_borel_cantelli_in_j"] < -1, "smooth BC")
require(exponents["small_value_borel_cantelli_in_j"] < -1, "small-value BC")
require(
    exponents["block_lipschitz_error"] < exponents["small_value_target"],
    "block interpolation must beat the small-value target",
)
require(3 * eta - Fraction(1, 2) < -beta, "one-point bias")
require(3 * eta - Fraction(1, 2) < -2 * eta, "small-value expectation")
require(2 * eta > beta, "Gaussian lower-tail truncation")
require(eta > beta, "Cauchy--Schwarz de-truncation")
require(
    exponents["jensen_amplified_log_error"] == Fraction(399, 400),
    "Jensen exponent",
)


def old_reciprocal_cross_sum(n: int, m: int) -> tuple[int, int]:
    """Enumerate the unnormalised expected inner-product numerator."""
    require(0 <= n < m, "need n < m")
    total = 0
    samples = 0
    for eps in product((-1, 1), repeat=m + 1):
        total += sum(eps[n - k] * eps[m - k] for k in range(n + 1))
        samples += 1
    return total, samples


# A small exact enumeration certifies the cancellation behind E||q_m-q_n||_2^2=2.
old_cross_total, old_samples = old_reciprocal_cross_sum(3, 5)
require(old_cross_total == 0, "old reciprocal cross expectation")
old_expected_l2_square = Fraction(2, 1)


def sigma_square(n: int, r: float) -> float:
    return math.fsum(r ** (2 * k) for k in range(n + 1))


def weights(n: int, r: float) -> list[float]:
    sigma = math.sqrt(sigma_square(n, r))
    return [r**k / sigma for k in range(n + 1)]


def block_l2_square(m: int, n: int, radius_type: str) -> float:
    require(m <= n, "block order")
    if radius_type == "unit":
        rm = rn = 1.0
    elif radius_type == "inner":
        rm = 1.0 - m ** (-401.0 / 400.0)
        rn = 1.0 - n ** (-401.0 / 400.0)
    elif radius_type == "outer":
        rm = 1.0 / (1.0 - m ** (-401.0 / 400.0))
        rn = 1.0 / (1.0 - n ** (-401.0 / 400.0))
    else:
        raise ValueError(radius_type)
    wm = weights(m, rm)
    wn = weights(n, rn)
    common = math.fsum((wn[k] - wm[k]) ** 2 for k in range(m + 1))
    tail = math.fsum(wn[k] ** 2 for k in range(m + 1, n + 1))
    return common + tail


# Numerical sanity check at a complete j^4 block. The theorem is proved
# analytically in AUDIT.md; these values merely make the scale reproducible.
j = 16
block_m = j**4
block_n = (j + 1) ** 4 - 1
block_values = {
    kind: block_l2_square(block_m, block_n, kind)
    for kind in ("unit", "inner", "outer")
}
for kind, value in block_values.items():
    require(value <= 16.0 * block_m ** (-1.0 / 4.0), f"{kind} block scale")


def polynomial(eps: list[int], z: complex) -> complex:
    return sum(c * z**k for k, c in enumerate(eps))


def reciprocal_polynomial(eps: list[int], z: complex) -> complex:
    n = len(eps) - 1
    return sum(eps[n - k] * z**k for k in range(n + 1))


eps = [1, -1, -1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1]
n = len(eps) - 1
rho = 1.0 - n ** (-401.0 / 400.0)
tau = 1.0 / rho
theta = 0.731
lhs = reciprocal_polynomial(eps, rho * cmath.exp(1j * theta))
rhs = (
    rho**n
    * cmath.exp(1j * n * theta)
    * polynomial(eps, tau * cmath.exp(-1j * theta))
)
reciprocal_identity_error = abs(lhs - rhs)
require(reciprocal_identity_error < 1e-10, "outer-radius reciprocal identity")

sigma_reciprocity_error = abs(
    sigma_square(n, tau) - tau ** (2 * n) * sigma_square(n, rho)
)
require(sigma_reciprocity_error < 1e-9, "sigma reciprocity")


def B(n: int, r: float, t: float) -> complex:
    a = weights(n, r)
    return sum(a[k] ** 2 * cmath.exp(1j * k * t) for k in range(n + 1))


def direct_covariance(n: int, r: float, theta: float, phi: float) -> list[list[float]]:
    a = weights(n, r)
    out = [[0.0 for _ in range(4)] for _ in range(4)]
    for k, ak in enumerate(a):
        v = [
            math.cos(k * theta),
            math.sin(k * theta),
            math.cos(k * phi),
            math.sin(k * phi),
        ]
        for row in range(4):
            for col in range(4):
                out[row][col] += ak * ak * v[row] * v[col]
    return out


def formula_covariance(n: int, r: float, theta: float, phi: float) -> list[list[float]]:
    out = [[0.0 for _ in range(4)] for _ in range(4)]
    for offset, angle in ((0, theta), (2, phi)):
        b = B(n, r, 2 * angle)
        out[offset][offset] = 0.5 + 0.5 * b.real
        out[offset][offset + 1] = 0.5 * b.imag
        out[offset + 1][offset] = 0.5 * b.imag
        out[offset + 1][offset + 1] = 0.5 - 0.5 * b.real
    d = B(n, r, theta - phi)
    s = B(n, r, theta + phi)
    off = [
        [(d.real + s.real) / 2, (s.imag - d.imag) / 2],
        [(d.imag + s.imag) / 2, (d.real - s.real) / 2],
    ]
    for row in range(2):
        for col in range(2):
            out[row][col + 2] = off[row][col]
            out[col + 2][row] = off[row][col]
    return out


cov_n = 2048
cov_r = 1.0 / (1.0 - cov_n ** (-401.0 / 400.0))
cov_theta, cov_phi = 0.713, -0.419
cov_direct = direct_covariance(cov_n, cov_r, cov_theta, cov_phi)
cov_formula = formula_covariance(cov_n, cov_r, cov_theta, cov_phi)
covariance_formula_error = max(
    abs(cov_direct[row][col] - cov_formula[row][col])
    for row in range(4)
    for col in range(4)
)
require(covariance_formula_error < 1e-11, "four-dimensional covariance formula")

result = {
    "status": "PASS",
    "exact_exponents": {key: str(value) for key, value in exponents.items()},
    "old_draft": {
        "enumerated_n": 3,
        "enumerated_m": 5,
        "sign_sequences": old_samples,
        "cross_numerator_total": old_cross_total,
        "expected_normalized_l2_square_for_every_m_gt_n": str(
            old_expected_l2_square
        ),
    },
    "block_sanity": {
        "j": j,
        "m": block_m,
        "n": block_n,
        "m_to_minus_one_quarter": block_m ** (-1.0 / 4.0),
        "l2_square": block_values,
    },
    "reciprocal_identity_absolute_error": reciprocal_identity_error,
    "sigma_reciprocity_absolute_error": sigma_reciprocity_error,
    "four_dimensional_covariance_formula_max_error": covariance_formula_error,
}

print(json.dumps(result, indent=2, sort_keys=True))
