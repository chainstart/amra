#!/usr/bin/env python3
"""Exact finite base and arithmetic guards for the low-half kernel theorem."""

from math import comb, isqrt


def C(n, k):
    return comb(n, k) if n >= k else 0


def first_true(predicate, lo, hi):
    while lo < hi:
        mid = (lo+hi)//2
        if predicate(mid):
            hi = mid
        else:
            lo = mid+1
    return lo


def top2(value):
    n = (1+isqrt(1+8*value))//2
    while C(n+1, 2) <= value:
        n += 1
    while C(n, 2) > value:
        n -= 1
    return n


def rho(a, c):
    threshold = max(a*a+3*a, C(a+1, 3)-C(c+1, 3)+1)
    r = (1+isqrt(1+8*threshold))//2
    while C(r, 2) < threshold:
        r += 1
    return r


def D_threshold(a, c):
    target = C(c+1, 4)+C(a+1, 3)
    hi = max(c+2, 4)
    while C(hi, 4) < target:
        hi *= 2
    return first_true(lambda d: C(d, 4) >= target, c+2, hi)


def A_star(a, c, d):
    target = C(d, 3)+C(a+1, 3)-C(c, 3)
    hi = a+2
    while C(hi, 3) < target:
        hi *= 2
    return first_true(lambda t: C(t, 3) >= target, a+2, hi)


checked = 0
minimum_gap = None
minimum = None
for a in range(3, 2401):
    for c in range(3, (a-1)//2+1):
        r = rho(a, c)
        B = top2(C(a, 2)+3*r+2)
        D = D_threshold(a, c)
        astar = A_star(a, c, D)
        gap = B-astar
        assert gap >= 0
        checked += 1
        if minimum_gap is None or gap < minimum_gap:
            minimum_gap = gap
            minimum = (a, c, r, D, B, astar)

assert checked == 1_434_006
assert minimum_gap == 0
assert minimum == (8, 3, 14, 9, 12, 12)

# Exact rational guards for the a>=2401 analytic tail.
assert 3**4 > 5*2**4                         # 5^(1/4)<3/2
assert 4*10 < 343                            # 4<(1/10)*2401^(3/4)
assert 49*1024 > 12*3971                    # large-c comparison
assert 49*375 > 12*256                      # small-c comparison
assert 2401 == 7**4

print("PASS: low-half adjacent-sum kernel")
print("finite base: 1,434,006 pairs, no failures")
print("infinite tail: a>=2401, split at c=a^(3/4)")
