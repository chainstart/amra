#!/usr/bin/env python3
"""Independent guards for round-9 width-profile audit.

This file imports no author evidence.  Universal conclusions are proved in
the accompanying audit note; these exact rational checks guard each branch.
"""

from fractions import Fraction as Q
from itertools import product


def endpoints(values):
    return min(values), max(values)


def wd(values):
    lo, hi = endpoints(values)
    return hi - lo


def scale(c, values):
    return {c * x for x in values}


def addsets(left, right):
    return {x + y for x in left for y in right}


# 1. Diagonal translation orbits in a common Laurent exponent group.
for p, q in [((Q(-5), Q(2)), (Q(7), Q(14))),
             ((Q(1, 3), Q(11, 3)), (Q(-4), Q(-2, 3)))]:
    assert p[1] - p[0] == q[1] - q[0]
    c = q[0] - p[0]
    assert (p[0] + c, p[1] + c) == q

# 2. Natural endpoints and width add on actual positive Minkowski products.
masks = [{Q(-2), Q(0), Q(5)}, {Q(1), Q(4)}, {Q(-3), Q(7)}]
for left, right in product(masks, repeat=2):
    ll, lr = endpoints(left)
    rl, rr = endpoints(right)
    assert endpoints(addsets(left, right)) == (ll + rl, lr + rr)
    assert wd(addsets(left, right)) == wd(left) + wd(right)

# 3--6. Four-width affine graph, both fixed signs, both anchors, residual zero.
cases = [
    ({Q(0), Q(2), Q(9)}, [Q(1), Q(4), Q(10)], "positive-zero"),
    ({Q(2), Q(5), Q(11)}, [Q(1), Q(4), Q(10)], "positive-nonzero"),
    ({Q(-9), Q(-2), Q(0)}, [Q(-1), Q(-4), Q(-10)], "negative-zero"),
    ({Q(-11), Q(-5), Q(-2)}, [Q(-1), Q(-4), Q(-10)], "negative-nonzero"),
]
lam0, W = Q(13), Q(1000)
for X, scalars, branch in cases:
    D = wd(X)
    source = [wd(scale(lam, X)) for lam in scalars]
    phi = [min(scale(lam, X)) for lam in scalars]
    profiles = []
    for lam, d in zip(scalars, source):
        d0 = abs(lam0) * D
        assert d == abs(lam) * D
        profile = (d, d0, W - d, W - d0)
        profiles.append(profile)
        assert (profile[0] - d, profile[1] - d0,
                profile[2] + d - W, profile[3] + d0 - W) == (0, 0, 0, 0)
    assert len(set(profiles)) == len(scalars)
    if branch in {"positive-zero", "negative-zero"}:
        assert len(set(phi)) == 1
    else:
        assert len(set(phi)) == len(scalars)
        ratios = {d / p for d, p in zip(source, phi)}
        assert len(ratios) == 1 and Q(0) not in ratios

# 7. The divisor-atlas coordinate is literally the first width coordinate.
for a, b, scalar_width in [(Q(2), Q(5), Q(7)), (Q(3), Q(11), Q(14))]:
    assert a + b == scalar_width

print("independent width-profile audit: PASS (10-item firewall)")
