#!/usr/bin/env python3
"""Independent bounded audit of the natural min-support profile theorem.

This checker does not import the author verifier.  Finite instances guard the
formulas; the universal proof is recorded in the accompanying audit note.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib
import json


def support_product(left, right):
    """Support and positive coefficient multiplicities of a mask product."""
    out = Counter()
    for a, b in product(left, right):
        out[a + b] += 1
    return out


def natural_profile(X, lam, centre_source, centre_complement, total_min):
    source_min = min(lam * x for x in X)
    leaf_complement_min = total_min - source_min
    return (source_min, centre_source, leaf_complement_min, centre_complement)


def fibres(values):
    return sorted(Counter(values).values())


def main():
    checks = 0

    masks = [
        (Fraction(-4), Fraction(1), Fraction(6)),
        (Fraction(0), Fraction(3)),
        (Fraction(2, 5), Fraction(11, 5), Fraction(17, 5)),
    ]
    for left, right in product(masks, repeat=2):
        prod = support_product(left, right)
        assert min(prod) == min(left) + min(right)
        assert all(c > 0 for c in prod.values())
        checks += 1

    csrc = Fraction(-7, 3)
    ccomp = Fraction(41, 6)
    total = csrc + ccomp

    # Graph and fibre equality, deliberately with repeated scalar values.
    X = (Fraction(-2), Fraction(1), Fraction(7, 2))
    lambdas = (Fraction(3), Fraction(3), Fraction(5), Fraction(-2), Fraction(-2))
    profiles = [natural_profile(X, z, csrc, ccomp, total) for z in lambdas]
    source_units = [p[0] for p in profiles]
    assert len(set(profiles)) == len(set(source_units))
    assert fibres(profiles) == fibres(source_units)
    for p in profiles:
        assert p[0] + p[2] == total
        assert p[2] + p[0] - total == 0
        checks += 1

    positive = tuple(Fraction(n) for n in (1, 4, 9, 15, 28))
    negative = tuple(-n for n in positive)

    # Natural-order zero and nonzero endpoint branches for both signs.
    cases = [
        ((Fraction(0), Fraction(2), Fraction(9)), positive, 1, "positive-zero"),
        ((Fraction(2), Fraction(5), Fraction(9)), positive, len(positive), "positive-nonzero"),
        ((Fraction(-8), Fraction(-1), Fraction(0)), negative, 1, "negative-zero"),
        ((Fraction(-8), Fraction(-1), Fraction(3)), negative, len(negative), "negative-nonzero"),
    ]
    branch_ranges = {}
    for points, scalars, expected, name in cases:
        ps = [natural_profile(points, z, csrc, ccomp, total) for z in scalars]
        assert len(set(ps)) == expected
        endpoint = min(points) if scalars[0] > 0 else max(points)
        for z, p in zip(scalars, ps):
            assert p[0] == z * endpoint
            checks += 1
        branch_ranges[name] = len(set(ps))

    # Normalization firewall only: reversing the order changes min to natural
    # max.  This demonstrates section dependence, not a new actual family.
    X_firewall = (Fraction(0), Fraction(2), Fraction(9))
    natural_units = [min(z * x for x in X_firewall) for z in positive]
    reverse_units = [max(z * x for x in X_firewall) for z in positive]
    assert len(set(natural_units)) == 1
    assert len(set(reverse_units)) == len(positive)
    checks += len(positive)

    result = {
        "schema": "amra.erdos1083.spectrum-conditioning-round8.independent-audit.v1",
        "status": "pass",
        "finite_checks": checks,
        "branch_ranges": branch_ranges,
        "graph_range_equality": True,
        "graph_fibre_multiset_equality": True,
        "residual_identically_zero": True,
        "reverse_order_role": "normalization_firewall_only",
        "legal_power_large_counterfamily_constructed": False,
        "public_exponent_changed": False,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
