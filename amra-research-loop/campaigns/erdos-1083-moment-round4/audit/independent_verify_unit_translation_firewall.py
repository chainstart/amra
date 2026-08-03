#!/usr/bin/env python3
"""Independent exact audit of the round-four unit-translation firewall.

This implementation was written from the stated identities and geometry; it
does not import or execute the author checker.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path


Poly = dict[int, Fraction]


def polynomial(terms: dict[int, int]) -> Poly:
    return {degree: Fraction(coefficient) for degree, coefficient in terms.items() if coefficient}


def multiply(left: Poly, right: Poly) -> Poly:
    answer: dict[int, Fraction] = {}
    for i, a in left.items():
        for j, b in right.items():
            answer[i + j] = answer.get(i + j, Fraction()) + a * b
    return {i: a for i, a in answer.items() if a}


def derivative(poly: Poly) -> Poly:
    return {degree - 1: coefficient * degree for degree, coefficient in poly.items() if degree}


def exponent_mask(poly: Poly) -> tuple[int, ...]:
    assert all(coefficient == 1 for coefficient in poly.values())
    return tuple(sorted(poly))


def normalized_laurent(poly: Poly, unit: Fraction) -> tuple[tuple[int, str], ...]:
    shifted = {Fraction(degree) + unit: coefficient for degree, coefficient in poly.items()}
    minimum = min(shifted)
    coefficient = shifted[minimum]
    return tuple(sorted((int(degree - minimum), str(value / coefficient)) for degree, value in shifted.items()))


def squarefree_decomposition(value: Fraction) -> tuple[Fraction, int]:
    """Return coefficient, squarefree radicand for sqrt(value)."""
    assert value > 0
    combined = value.numerator * value.denominator
    square = 1
    squarefree = 1
    divisor = 2
    while divisor * divisor <= combined:
        exponent = 0
        while combined % divisor == 0:
            combined //= divisor
            exponent += 1
        square *= divisor ** (exponent // 2)
        if exponent % 2:
            squarefree *= divisor
        divisor += 1
    if combined > 1:
        squarefree *= combined
    return Fraction(square, value.denominator), squarefree


def canonical_target_distance(
    first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]
) -> tuple[str, str, int]:
    tau, z = first
    sigma, w = second
    rational = tau + sigma + (z - w) ** 2
    coefficient, radicand = squarefree_decomposition(tau * sigma)
    radical_coefficient = -2 * coefficient
    if radicand == 1:
        rational += radical_coefficient
        radical_coefficient = Fraction()
    return str(rational), str(radical_coefficient), radicand


def exact_block(translation: Fraction, starts: dict[int, tuple[int, ...]]) -> dict[str, object]:
    source = (translation, translation + 1)
    assert all(Fraction(-1) <= x <= 1 for x in source)
    targets: list[tuple[Fraction, Fraction]] = []
    row_spectra = {}
    row_tau_min = {}
    for scalar, positions in starts.items():
        z = Fraction(scalar, 2)
        labels = []
        taus = []
        for position in positions:
            tau = Fraction(100 + position) - scalar * translation - (1 + z * z)
            assert tau > 0
            taus.append(tau)
            targets.append((tau, z))
            # With p_x=(0,sqrt(1-x^2),x), q=(sqrt(tau),0,-z),
            # ||p_x-q||^2=tau+1+z^2+2zx.
            labels.extend(tau + 1 + z * z + scalar * x for x in source)
        row_spectra[str(scalar)] = [str(item) for item in sorted(labels)]
        row_tau_min[str(scalar)] = str(min(taus))
    expected = [str(Fraction(x)) for x in range(100, 112)]
    assert all(labels == expected for labels in row_spectra.values())
    target_labels = {
        canonical_target_distance(first, second)
        for first, second in combinations(targets, 2)
    }
    return {
        "translation": str(translation),
        "source": [str(item) for item in source],
        "source_in_unit_interval": True,
        "target_count": len(targets),
        "positive_tangent_squares": True,
        "minimum_tau_by_scalar": row_tau_min,
        "row_spectra": row_spectra,
        "target_pair_occurrences": len(targets) * (len(targets) - 1) // 2,
        "distinct_target_target_labels": len(target_labels),
    }


def main() -> None:
    one = polynomial({0: 1})
    G = polynomial({0: 1, 1: 1})
    F0 = polynomial({0: 1, 2: 1})
    R1 = one
    R3 = polynomial({0: 1, 1: -1, 2: 1})
    H1 = R3
    H2 = polynomial({0: 1, 1: 1, 2: 1})
    H3 = polynomial({0: 1, 2: -1, 4: 1})
    B = polynomial({0: 1, 4: 1, 8: 1})
    Q1 = B
    Q3 = multiply(H2, H3)

    assert multiply(multiply(H1, H2), H3) == B
    assert multiply(R1, Q1) == B
    assert multiply(R3, Q3) == B
    assert multiply(G, R1) == polynomial({0: 1, 1: 1})
    assert multiply(G, R3) == polynomial({0: 1, 3: 1})

    GB = multiply(G, B)
    F0Q1 = multiply(F0, Q1)
    F0Q3 = multiply(F0, Q3)
    masks = {
        "GB": exponent_mask(GB),
        "F0Q1": exponent_mask(F0Q1),
        "F0Q3": exponent_mask(F0Q3),
    }
    assert masks == {
        "GB": (0, 1, 4, 5, 8, 9),
        "F0Q1": (0, 2, 4, 6, 8, 10),
        "F0Q3": (0, 1, 2, 6, 7, 8),
    }

    vectors = {"row_1": (1, 1, 1), "row_3": (0, 1, 1)}
    assert multiply(multiply(H1, H2), H3) == Q1
    assert multiply(H2, H3) == Q3

    units = {
        "G": lambda t: t,
        "F0": lambda t: 2 * t,
        "B": lambda t: -3 * t,
        "R1": lambda t: Fraction(),
        "R3": lambda t: 2 * t,
        "Q1": lambda t: -3 * t,
        "Q3": lambda t: -5 * t,
    }
    polynomials = {"G": G, "F0": F0, "B": B, "R1": R1, "R3": R3, "Q1": Q1, "Q3": Q3}
    translations = (Fraction(), Fraction(-1, 4))
    normalized = {
        str(t): {name: normalized_laurent(poly, units[name](t)) for name, poly in polynomials.items()}
        for t in translations
    }
    assert normalized[str(translations[0])] == normalized[str(translations[1])]

    # A normalized logarithmic derivative is the rational function P'/P;
    # numerator and denominator are identical after unit removal. Full
    # Laurent logarithmic derivatives differ by u/x, exactly the lost datum.
    normalized_log_data = {
        name: {
            "numerator": sorted((degree, str(value)) for degree, value in derivative(poly).items()),
            "denominator": sorted((degree, str(value)) for degree, value in poly.items()),
        }
        for name, poly in polynomials.items()
    }

    # Row lambda uses the complement start mask shifted by -lambda*t and the
    # scalar source lambda*X_t. Their Minkowski sum is {0,...,11}.
    starts = {1: masks["F0Q1"], 2: masks["GB"], 3: masks["F0Q3"]}
    scalar_copy_checks = {}
    for t in translations:
        rows = {}
        for scalar, positions in starts.items():
            source_copy = (scalar * t, scalar * (t + 1))
            complement = tuple(Fraction(position) - scalar * t for position in positions)
            spectrum = sorted({left + right for left in source_copy for right in complement})
            assert spectrum == [Fraction(i) for i in range(12)]
            rows[str(scalar)] = {
                "scalar_source": [str(item) for item in source_copy],
                "complement_unit": str(-scalar * t),
                "spectrum": [str(item) for item in spectrum],
            }
        scalar_copy_checks[str(t)] = rows

    blocks = {str(t): exact_block(t, starts) for t in translations}
    assert blocks["0"]["distinct_target_target_labels"] == 127
    assert blocks["-1/4"]["distinct_target_target_labels"] == 145

    exponents = {
        "q": Fraction(13, 18),
        "U": Fraction(5, 6),
        "qU": Fraction(14, 9),
        "all_target_pair_capacity": 2 * Fraction(14, 9),
        "target_label_goal": Fraction(3),
        "capacity_minus_goal": 2 * Fraction(14, 9) - 3,
    }
    assert exponents["q"] + exponents["U"] == exponents["qU"]
    assert exponents["all_target_pair_capacity"] == Fraction(28, 9)
    assert exponents["capacity_minus_goal"] == Fraction(1, 9)

    payload = {
        "schema": "amra.erdos1083.moment_round4.independent_audit.v1",
        "author_checker_imported": False,
        "factorization": {
            "B_equals_H1H2H3": True,
            "B_equals_R1Q1_equals_R3Q3": True,
            "boolean_vectors": {name: list(vector) for name, vector in vectors.items()},
            "paired_positive_masks": {name: list(mask) for name, mask in masks.items()},
        },
        "normalized_data": {
            "translation_blocks_equal_after_unit_removal": True,
            "normalized_laurent_polynomials": normalized,
            "normalized_root_multiplicity_data_equal": True,
            "normalized_log_derivative_data": normalized_log_data,
            "lost_unit_vectors": {
                str(t): {name: str(function(t)) for name, function in units.items()}
                for t in translations
            },
        },
        "common_X_scalar_copies": scalar_copy_checks,
        "translation_blocks": blocks,
        "unit_firewall": {
            "normalized_unit_blind_determination_refuted": True,
            "relative_unit_aware_route_refuted": False,
            "reason": "The pair changes the common source translation and is distinguished by retained units; it does not exhibit many relative unit vectors after one common X is fixed.",
        },
        "capacity_ledger": {name: str(value) for name, value in exponents.items()},
        "capacity_precision": "28/9 is an all-target pair capacity. A fibre implication additionally needs an actual occurrence domain of size t^(28/9-o(1)); the upper bound |targets|<=qU alone is insufficient.",
        "required_fibre": "< t^(1/9-epsilon+o(1)) on that same actual all-target occurrence domain to obtain >t^(3+epsilon-o(1)) labels",
        "public_exponent_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_name("independent_unit_translation_audit.json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
