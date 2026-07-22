#!/usr/bin/env python3
"""Finite audit of equations (3) and (6) in primitive_phase_target.md."""

import cmath
import math


def e(x):
    return cmath.exp(2j * math.pi * x)


H = 2
K = 4
a = 0.17
q = 2
b = 1.0 - (1.0 - a) ** q
primes = [11, 7, 5, 3]  # decreasing stopping order
T = [11, 5]
pstar = 5
c = math.prod(T)
A = 13
N = 90


def active(p, n):
    return any((n - K - j) % p == 0 for j in range(H))


def d(p, n):
    return -b * (float(active(p, n)) - H / p)


def mzero(p):
    return 1.0 - b * H / p


gamma = math.prod(mzero(p) for p in primes if p >= pstar and p not in T)


def g(n):
    return gamma * math.prod(d(p, n) for p in T)


def suffix(n):
    return math.prod(mzero(p) + d(p, n) for p in primes if p < pstar)


def dh(theta):
    return sum(e(-j * theta) for j in range(H))


def predicted_hat(u):
    if math.gcd(u, c) != 1:
        return 0j
    product = 1 + 0j
    for p in T:
        cp = c // p
        hp = (u * pow(cp, -1, p)) % p
        product *= dh(hp / p)
    return gamma * ((-b) ** len(T)) / c * e(-u * K / c) * product


max_hat_error = 0.0
for u in range(c):
    direct_hat = sum(g(x) * e(-u * x / c) for x in range(c)) / c
    max_hat_error = max(max_hat_error, abs(direct_hat - predicted_hat(u)))

direct_corr = sum(g(n) * suffix(n) for n in range(A + 1, A + N + 1))
fourier_corr = 0j
for u in range(c):
    if math.gcd(u, c) != 1:
        continue
    inner = sum(e(u * ell / c) * suffix(A + ell) for ell in range(1, N + 1))
    product = 1 + 0j
    for p in T:
        cp = c // p
        hp = (u * pow(cp, -1, p)) % p
        product *= dh(hp / p)
    fourier_corr += (
        gamma
        * ((-b) ** len(T))
        / c
        * e(u * (A - K) / c)
        * product
        * inner
    )

print(f"c={c} H={H} K={K} q={q} interval=({A},{A+N}]")
print(f"max_hat_error={max_hat_error:.3e}")
print(f"direct_corr={direct_corr:.16e}")
print(f"fourier_corr_real={fourier_corr.real:.16e}")
print(f"fourier_corr_imag={fourier_corr.imag:.3e}")
print(f"correlation_error={abs(direct_corr-fourier_corr):.3e}")
assert max_hat_error < 1e-12
assert abs(direct_corr - fourier_corr) < 1e-11
