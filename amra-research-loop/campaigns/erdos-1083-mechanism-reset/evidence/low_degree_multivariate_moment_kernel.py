#!/usr/bin/env python3
"""Exact low-degree moment kernels on the Phi6 union support."""

from itertools import combinations
from math import comb, log2
import json


def multiindices(coordinates, max_degree):
    def build(position, remaining, prefix):
        if position == coordinates - 1:
            yield tuple(prefix + [remaining])
            return
        for value in range(remaining + 1):
            yield from build(position + 1, remaining - value, prefix + [value])

    for degree in range(max_degree + 1):
        yield from build(0, degree, [])


def parity_rows(d, L):
    active = L + 1
    assert active <= d // 2
    positive = {}
    negative = {}
    for size in range(active + 1):
        for chosen in combinations(range(active), size):
            point = [0] * (d + 1)  # y,x_1,...,x_d; keep y=0.
            for index in chosen:
                point[index + 1] = 1
            coefficient = (-1) ** (active - size)
            (positive if coefficient > 0 else negative)[tuple(point)] = 1
    return positive, negative


def moment(row, alpha):
    total = 0
    for point, coefficient in row.items():
        value = 1
        for coordinate, exponent in zip(point, alpha):
            value *= coordinate**exponent
        total += coefficient * value
    return total


def verify_parity_certificate(d, L):
    positive, negative = parity_rows(d, L)
    indices = tuple(multiindices(d + 1, L))
    assert len(indices) == comb(d + 1 + L, L)
    assert all(moment(positive, alpha) == moment(negative, alpha) for alpha in indices)
    assert len(positive) == len(negative) == 2**L
    origin = (0,) * (d + 1)
    assert (origin in positive) != (origin in negative)
    assert all(sum(point[1:]) <= d // 2 for point in positive | negative)
    return {
        "d": d,
        "L": L,
        "feature_count": len(indices),
        "positive_support_size": len(positive),
        "negative_support_size": len(negative),
        "positive_contains_origin": origin in positive,
        "negative_contains_origin": origin in negative,
        "all_moments_equal": True,
    }


def equal_augmentation_signed_certificate(d=8, L=3):
    positive, negative = parity_rows(d, L)
    common_negative_atom = (1,) + (0,) * d
    common_debt = 2**L - 2
    positive[common_negative_atom] = -common_debt
    negative[common_negative_atom] = -common_debt
    indices = tuple(multiindices(d + 1, L))
    assert common_debt > 0
    assert sum(positive.values()) == sum(negative.values()) == 2
    assert all(moment(positive, alpha) == moment(negative, alpha) for alpha in indices)
    origin = (0,) * (d + 1)
    assert (origin in positive) != (origin in negative)
    return {
        "d": d,
        "L": L,
        "common_negative_atom": list(common_negative_atom),
        "common_negative_coefficient": -common_debt,
        "augmentation_of_each_row": 2,
        "support_size_of_each_row": len(positive),
        "positive_row_contains_origin": origin in positive,
        "negative_row_contains_origin": origin in negative,
        "all_total_degree_at_most_L_moments_equal": True,
        "support_encoding": (
            "apart from the common y=1 debt atom, the two supports are the "
            "opposite parity classes of {0,1}^{L+1} in x_1,...,x_(L+1)"
        ),
    }


def phi6_row_linear_fingerprint(d, chosen):
    # Q_A=(1+Y)prod_(i in A)(1-X_i+X_i^2).
    # Augmentation is 2.  Its first moment in X_i is 2 for i in A and 0
    # otherwise; the Y first moment is 1.
    return (2, 1, *(2 if index in chosen else 0 for index in range(d)))


def main():
    exact_certificates = []
    for d in (4, 6, 8, 10, 12):
        for L in range(d // 2):
            exact_certificates.append(verify_parity_certificate(d, L))

    structured_fingerprints = []
    for d in range(2, 11):
        k = d // 2
        fingerprints = {
            phi6_row_linear_fingerprint(d, frozenset(chosen))
            for chosen in combinations(range(d), k)
        }
        assert len(fingerprints) == comb(d, k)
        structured_fingerprints.append({
            "d": d,
            "row_count": comb(d, k),
            "distinct_degree_at_most_one_fingerprints": len(fingerprints),
        })

    dimension_ledgers = []
    for d in (16, 32, 64, 128, 256):
        k = d // 2
        union_atoms = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        choices = {
            "constant_3": 3,
            "floor_log2_d": int(log2(d)),
            "twice_floor_log2_d": 2 * int(log2(d)),
        }
        entries = {}
        for label, L in choices.items():
            features = comb(d + 1 + L, L)
            entries[label] = {
                "L": L,
                "features": features,
                "kernel_dimension_lower_bound": max(0, union_atoms - features),
                "feature_to_union_ratio": features / union_atoms,
            }
        dimension_ledgers.append({"d": d, "union_atoms": union_atoms, "cases": entries})

    print(json.dumps({
        "schema": "amra.erdos1083.low-degree-multivariate-moment-kernel-check.v1",
        "exact_parity_certificates": exact_certificates,
        "equal_augmentation_signed_certificate": equal_augmentation_signed_certificate(),
        "structured_phi6_degree_one_fingerprints": structured_fingerprints,
        "dimension_ledgers": dimension_ledgers,
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
