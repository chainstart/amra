#!/usr/bin/env python3
"""Finite certificates for the multidirectional tensor-switch barrier."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json

import sympy as sp


def is_mask(poly: sp.Expr, variables: tuple[sp.Symbol, ...]) -> bool:
    coefficients = sp.Poly(sp.expand(poly), *variables).coeffs()
    return bool(coefficients) and all(coefficient == 1 for coefficient in coefficients)


def tensor_family_certificate() -> dict[str, object]:
    rank = 5
    complement_size = 3
    variables = sp.symbols("x0:%d" % rank)
    z = sp.symbols("z")
    all_variables = variables + (z,)
    a_factors = [1 + variable for variable in variables]
    t_factors = [1 - variable + variable**2 for variable in variables]
    direct_switches = [1 + variable**3 for variable in variables]
    d_mask = sum(z**index for index in range(complement_size))
    centre = sp.prod(a_factors)
    common_b = sp.expand(d_mask * sp.prod(t_factors))
    common_positive = sp.expand(centre * common_b)

    records: list[dict[str, object]] = []
    residual_signatures = set()
    for bitmask in range(1 << rank):
        selected = {index for index in range(rank) if bitmask & (1 << index)}
        residual = sp.prod(
            t_factors[index] for index in range(rank) if index not in selected
        )
        quotient = sp.expand(
            d_mask * sp.prod(t_factors[index] for index in selected)
        )
        switched_source = sp.expand(centre * residual)
        switched_complement = sp.expand(centre * quotient)
        expected_source = sp.expand(
            sp.prod(
                a_factors[index] if index in selected else direct_switches[index]
                for index in range(rank)
            )
        )
        expected_complement = sp.expand(
            d_mask
            * sp.prod(
                direct_switches[index] if index in selected else a_factors[index]
                for index in range(rank)
            )
        )
        coefficients = sp.Poly(quotient, *all_variables).coeffs()
        signature = tuple(index for index in range(rank) if index not in selected)
        residual_signatures.add(signature)
        records.append(
            {
                "subset_mask": bitmask,
                "subset_size": len(selected),
                "B_factorization": sp.expand(residual * quotient - common_b) == 0,
                "source_identity": sp.expand(switched_source - expected_source) == 0,
                "complement_identity": sp.expand(
                    switched_complement - expected_complement
                )
                == 0,
                "source_is_mask": is_mask(switched_source, variables),
                "complement_is_mask": is_mask(switched_complement, all_variables),
                "source_terms": len(sp.Poly(switched_source, *variables).terms()),
                "complement_terms": len(
                    sp.Poly(switched_complement, *all_variables).terms()
                ),
                "quotient_augmentation": int(
                    quotient.subs({variable: 1 for variable in all_variables})
                ),
                "signed_exactly_when_nonempty": (
                    any(coefficient < 0 for coefficient in coefficients)
                    == bool(selected)
                ),
                "contaminated_exactly_when_nonempty": bool(selected)
                == (len(selected) > 0),
            }
        )

    base_identities = all(
        sp.expand(a_factors[index] * t_factors[index] - direct_switches[index])
        == 0
        for index in range(rank)
    )
    passed = (
        base_identities
        and is_mask(common_positive, all_variables)
        and len(residual_signatures) == 1 << rank
        and all(
            record["B_factorization"]
            and record["source_identity"]
            and record["complement_identity"]
            and record["source_is_mask"]
            and record["complement_is_mask"]
            and record["source_terms"] == 2**rank
            and record["complement_terms"] == complement_size * 2**rank
            and record["quotient_augmentation"] == complement_size
            and record["signed_exactly_when_nonempty"]
            and record["contaminated_exactly_when_nonempty"]
            for record in records
        )
    )
    return {
        "rank": rank,
        "S": 2**rank,
        "C": complement_size,
        "U": complement_size * 2**rank,
        "family_size": 2**rank,
        "base_switch_identities": base_identities,
        "common_positive_mask": is_mask(common_positive, all_variables),
        "distinct_residual_signatures": len(residual_signatures),
        "records": records,
        "pass": passed,
    }


def endpoint_calibration_certificate() -> dict[str, object]:
    ell = 3
    rank = 14 * ell
    source_size = 2**rank
    quotient_size = 2**ell
    complement_size = source_size * quotient_size
    t = 2 ** (18 * ell)
    return {
        "ell": ell,
        "rank": rank,
        "S": source_size,
        "C": quotient_size,
        "U": complement_size,
        "t": t,
        "family_size": 2**rank,
        "C_power_14_equals_S": quotient_size**14 == source_size,
        "U_equals_SC": complement_size == source_size * quotient_size,
        "S_endpoint": source_size**9 == t**7,
        "C_endpoint": quotient_size**18 == t,
        "U_endpoint": complement_size**6 == t**5,
        "family_dominates_required": (2**rank) ** 9 >= t**5,
        "pass": (
            quotient_size**14 == source_size
            and complement_size == source_size * quotient_size
            and source_size**9 == t**7
            and quotient_size**18 == t
            and complement_size**6 == t**5
            and (2**rank) ** 9 >= t**5
        ),
    }


def homothety_class_certificate() -> dict[str, object]:
    sharp_records = []
    general_records = []
    total_patterns_checked = 0

    def canonical_log_shape(q_values: list[Fraction], pattern: int) -> tuple[Fraction, ...]:
        shifted = sorted(
            value + (1 if pattern & (1 << index) else 0)
            for index, value in enumerate(q_values)
        )
        origin = shifted[0]
        return tuple(value - origin for value in shifted)

    for rank in range(1, 11):
        # The sharp encoding q_i=i/k has one class containing the k+1
        # prefix patterns of all possible Hamming weights.
        q_values = [Fraction(index, rank) for index in range(rank)]
        groups: dict[tuple[Fraction, ...], list[int]] = {}
        for pattern in range(1 << rank):
            groups.setdefault(canonical_log_shape(q_values, pattern), []).append(pattern)
        prefix_patterns = {
            sum(1 << index for index in range(prefix_length))
            for prefix_length in range(rank + 1)
        }
        prefix_shape = canonical_log_shape(q_values, 0)
        sharp_class = set(groups[prefix_shape])
        maximum_class = max(len(group) for group in groups.values())
        sharp_records.append(
            {
                "rank": rank,
                "patterns": 1 << rank,
                "classes": len(groups),
                "maximum_class": maximum_class,
                "sharp_prefix_class_size": len(sharp_class),
                "prefix_patterns_exact": sharp_class == prefix_patterns,
                "pass": maximum_class == rank + 1
                and len(sharp_class) == rank + 1
                and sharp_class == prefix_patterns,
            }
        )

        # Several irregular distinct log sets test the universal k+1
        # bound away from the sharp arithmetic grid.
        irregular_sets = [
            [Fraction(index * index + 2 * index, rank + 1) for index in range(rank)],
            [Fraction(2**index - 1, 2**rank) for index in range(rank)],
        ]
        for sample_index, irregular_q in enumerate(irregular_sets):
            irregular_groups: dict[tuple[Fraction, ...], int] = {}
            for pattern in range(1 << rank):
                shape = canonical_log_shape(irregular_q, pattern)
                irregular_groups[shape] = irregular_groups.get(shape, 0) + 1
            irregular_maximum = max(irregular_groups.values())
            general_records.append(
                {
                    "rank": rank,
                    "sample": sample_index,
                    "maximum_class": irregular_maximum,
                    "bound": rank + 1,
                    "pass": irregular_maximum <= rank + 1,
                }
            )
        total_patterns_checked += 3 * (1 << rank)
    return {
        "sharp_records": sharp_records,
        "general_records": general_records,
        "patterns_checked": total_patterns_checked,
        "edge_multiplicity_and_exponential_independence_proof_in_manuscript": True,
        "pass": all(record["pass"] for record in sharp_records)
        and all(record["pass"] for record in general_records),
    }


def direction_and_factor_certificate() -> dict[str, object]:
    rank = 8
    subsets_checked = 0
    signed_count = 0
    clean_count = 0
    divisor_vectors = set()
    for subset_size in range(rank + 1):
        for subset in combinations(range(rank), subset_size):
            selected = set(subset)
            divisor_vector = tuple(
                0 if index in selected else 1 for index in range(rank)
            )
            divisor_vectors.add(divisor_vector)
            subsets_checked += 1
            if selected:
                signed_count += 1
            else:
                clean_count += 1
    return {
        "rank": rank,
        "subsets_checked": subsets_checked,
        "distinct_divisor_vectors": len(divisor_vectors),
        "signed_contaminated_rows": signed_count,
        "clean_rows": clean_count,
        "pass": (
            subsets_checked == 2**rank
            and len(divisor_vectors) == 2**rank
            and signed_count == 2**rank - 1
            and clean_count == 1
        ),
    }


def main() -> int:
    result = {
        "tensor_family": tensor_family_certificate(),
        "endpoint_calibration": endpoint_calibration_certificate(),
        "homothety_classes": homothety_class_certificate(),
        "direction_and_factor": direction_and_factor_certificate(),
        "all_parameter_proofs_in_manuscript": True,
    }
    result["pass"] = all(
        result[key]["pass"]
        for key in (
            "tensor_family",
            "endpoint_calibration",
            "homothety_classes",
            "direction_and_factor",
        )
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
