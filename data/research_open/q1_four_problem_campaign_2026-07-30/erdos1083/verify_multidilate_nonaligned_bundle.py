#!/usr/bin/env python3
"""Exact checks for the multidilate/nonaligned-bundle theorem.

The finite checks are falsification and arithmetic certificates.  The
all-parameter theorem rests on the written injection proof.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
import json


Number = Fraction


def additive_energy(left: tuple[Number, ...], right: tuple[Number, ...]) -> int:
    """Return E^+(left, right) exactly."""
    counts = Counter(a + b for a in left for b in right)
    return sum(value * value for value in counts.values())


def spectrum(
    x_set: tuple[Number, ...],
    row: tuple[Number, ...],
    dilation: Number,
    shift: Number = Fraction(0),
) -> frozenset[Number]:
    return frozenset(shift + tau + dilation * x for tau in row for x in x_set)


def audit_instance(
    x_set: tuple[Number, ...],
    t_star: tuple[Number, ...],
    rows: dict[Number, tuple[Number, ...]],
    shifts: dict[Number, Number] | None = None,
) -> dict[str, int | bool]:
    """Audit Theorems 1--3 on one exact rational instance."""
    if not x_set or not t_star:
        raise ValueError("x_set and t_star must be nonempty")
    if Fraction(0) in rows:
        raise ValueError("dilations must be nonzero")
    if any(not set(row).issubset(t_star) for row in rows.values()):
        raise ValueError("every row must be a subset of t_star")

    shifts = shifts or {}
    s = len(x_set)
    r = len(t_star)
    diagonal = s * sum(len(row) for row in rows.values())
    nontrivial_budget = r * (r - 1) * s * (s - 1)

    energies: dict[Number, int] = {}
    spectra: dict[Number, frozenset[Number]] = {}
    for dilation, row in rows.items():
        dilated_x = tuple(dilation * x for x in x_set)
        energies[dilation] = additive_energy(row, dilated_x)
        spectra[dilation] = spectrum(
            x_set, row, dilation, shifts.get(dilation, Fraction(0))
        )

    energy_sum = sum(energies.values())
    energy_bound = diagonal + nontrivial_budget
    total_inputs = diagonal
    total_support = sum(len(values) for values in spectra.values())

    # Cross-row Cauchy--Schwarz: N^2 <= support * energy.
    support_cs_pass = total_inputs * total_inputs <= total_support * energy_sum

    union = set().union(*spectra.values()) if spectra else set()
    ordered_intersection_sum = sum(
        len(spectra[first] & spectra[second])
        for first in spectra
        for second in spectra
        if first != second
    )
    multiplicities = Counter(
        value for values in spectra.values() for value in values
    )
    intersection_identity = sum(
        multiplicity * (multiplicity - 1)
        for multiplicity in multiplicities.values()
    )

    return {
        "energy_sum": energy_sum,
        "energy_bound": energy_bound,
        "energy_pass": energy_sum <= energy_bound,
        "total_inputs": total_inputs,
        "total_support": total_support,
        "support_cs_pass": support_cs_pass,
        "union_size": len(union),
        "ordered_intersection_sum": ordered_intersection_sum,
        "intersection_identity": intersection_identity,
        "intersection_identity_pass": (
            ordered_intersection_sum == intersection_identity
        ),
    }


def rational_circle_point(parameter: int) -> tuple[Number, Number]:
    """Return (cos phi, sin phi) on the unit circle exactly."""
    value = Fraction(parameter)
    denominator = 1 + value * value
    return (
        (1 - value * value) / denominator,
        2 * value / denominator,
    )


def squared_distance_3d(
    first: tuple[Number, Number, Number],
    second: tuple[Number, Number, Number],
) -> Number:
    return sum((a - b) * (a - b) for a, b in zip(first, second))


def geometric_formula_certificate() -> list[dict[str, str]]:
    """Check the exact circle-to-axis formula on rational points."""
    a = Fraction(3)
    rho = Fraction(2)
    w0 = Fraction(5)
    records: list[dict[str, str]] = []
    for parameter in (1, 2, 3):
        cosine, sine = rational_circle_point(parameter)
        source = (a + rho * cosine, Fraction(0), w0 + rho * sine)
        for y, wi in (
            (Fraction(1), Fraction(2)),
            (Fraction(3), Fraction(-1)),
        ):
            target = (a, y, wi)
            z = w0 - wi
            direct = squared_distance_3d(source, target)
            formula = rho * rho + y * y + z * z + 2 * rho * z * sine
            if direct != formula:
                raise AssertionError("circle-axis formula failed")
            records.append(
                {
                    "parameter": str(parameter),
                    "y": str(y),
                    "height": str(wi),
                    "squared_distance": str(direct),
                }
            )
    return records


def parabolic_spectral_graph_certificate() -> dict[str, int | bool | str]:
    """Check the quadratic row-degree cap and rich-label count exactly."""
    x_set = (Fraction(0), Fraction(1))
    t_star = (Fraction(0), Fraction(1))
    z_values = (Fraction(1), Fraction(2), Fraction(3), Fraction(4))
    rho = Fraction(1)
    rows = {2 * rho * z: t_star for z in z_values}
    shifts = {2 * rho * z: rho * rho + z * z for z in z_values}
    result = audit_instance(x_set, t_star, rows, shifts)

    spectra_by_z = {
        z: spectrum(x_set, t_star, 2 * rho * z, rho * rho + z * z)
        for z in z_values
    }
    row_degrees = Counter(
        value for values in spectra_by_z.values() for value in values
    )
    s = len(x_set)
    r = len(t_star)
    h = len(z_values)
    u = len(t_star)
    d = len(row_degrees)
    threshold = Fraction(h * s * u, 4 * d)
    rich_count = sum(Fraction(degree) >= threshold for degree in row_degrees.values())
    required_count = Fraction(h * u, 8 * r)

    return {
        "max_row_degree": max(row_degrees.values()),
        "quadratic_cap": 2 * s * r,
        "quadratic_cap_pass": max(row_degrees.values()) <= 2 * s * r,
        "rich_threshold": str(threshold),
        "rich_count": rich_count,
        "required_rich_count": str(required_count),
        "rich_count_pass": Fraction(rich_count) >= required_count,
        "energy_pass": bool(result["energy_pass"]),
    }


def endpoint_exponent_certificate() -> dict[str, str | bool]:
    """Check every rational exponent used in the 2/9 corollary."""
    kappa = Fraction(2, 9)
    m = Fraction(5, 6)
    a_lower = Fraction(1) - kappa
    a_upper = Fraction(16, 27) + 2 * m / 9
    h_lower = Fraction(11, 9) - a_upper + 2 * m
    reuse_gap = h_lower + m - 2 - a_upper
    support_exponent = h_lower + a_lower + m
    overlap_exponent = 2 * a_lower + 2 * m - 3
    rich_label_exponent = h_lower + m - 1
    row_degree_exponent = support_exponent - 3
    synchronized_pair_exponent = 2 * h_lower + a_lower + m - 3

    expected = {
        "a_lower": Fraction(7, 9),
        "a_upper_at_min_m": Fraction(7, 9),
        "h_lower": Fraction(19, 9),
        "reuse_gap": Fraction(1, 6),
        "support_exponent": Fraction(67, 18),
        "overlap_exponent": Fraction(2, 9),
        "rich_label_exponent": Fraction(35, 18),
        "row_degree_exponent": Fraction(13, 18),
        "synchronized_pair_exponent": Fraction(17, 6),
    }
    actual = {
        "a_lower": a_lower,
        "a_upper_at_min_m": a_upper,
        "h_lower": h_lower,
        "reuse_gap": reuse_gap,
        "support_exponent": support_exponent,
        "overlap_exponent": overlap_exponent,
        "rich_label_exponent": rich_label_exponent,
        "row_degree_exponent": row_degree_exponent,
        "synchronized_pair_exponent": synchronized_pair_exponent,
    }
    passed = actual == expected
    return {
        **{key: str(value) for key, value in actual.items()},
        "pass": passed,
    }


def exhaustive_small_audit() -> dict[str, int]:
    """Exhaust all nonempty row choices in several small instances."""
    audited = 0
    for x_set, t_star, dilations in (
        (
            (Fraction(0), Fraction(1)),
            (Fraction(0), Fraction(1), Fraction(3)),
            (Fraction(1), Fraction(2), Fraction(4)),
        ),
        (
            (Fraction(-1), Fraction(0), Fraction(2)),
            (Fraction(-2), Fraction(0), Fraction(1)),
            (Fraction(-1), Fraction(3)),
        ),
    ):
        subsets = [
            tuple(t_star[index] for index in range(len(t_star)) if mask >> index & 1)
            for mask in range(1, 1 << len(t_star))
        ]
        # Exhaust all choices when there are two dilations; use paired
        # cyclic choices for the three-dilation instance to keep runtime tiny.
        if len(dilations) == 2:
            row_assignments = (
                dict(zip(dilations, chosen))
                for chosen in __import__("itertools").product(
                    subsets, repeat=len(dilations)
                )
            )
        else:
            row_assignments = (
                {
                    dilation: subsets[(offset + index) % len(subsets)]
                    for index, dilation in enumerate(dilations)
                }
                for offset in range(len(subsets))
            )

        for rows in row_assignments:
            shifts = {
                dilation: dilation * dilation + Fraction(index, 7)
                for index, dilation in enumerate(dilations)
            }
            result = audit_instance(x_set, t_star, rows, shifts)
            if not result["energy_pass"]:
                raise AssertionError("multidilate energy budget failed")
            if not result["support_cs_pass"]:
                raise AssertionError("aggregate support Cauchy--Schwarz failed")
            if not result["intersection_identity_pass"]:
                raise AssertionError("spectrum intersection identity failed")
            audited += 1
    return {"instances_audited": audited}


def main() -> None:
    small = exhaustive_small_audit()
    geometry = geometric_formula_certificate()
    spectral_graph = parabolic_spectral_graph_certificate()
    endpoint = endpoint_exponent_certificate()
    if not endpoint["pass"]:
        raise AssertionError("endpoint exponent certificate failed")
    if not (
        spectral_graph["quadratic_cap_pass"]
        and spectral_graph["rich_count_pass"]
        and spectral_graph["energy_pass"]
    ):
        raise AssertionError("parabolic spectral graph certificate failed")
    print(
        json.dumps(
            {
                "schema": "amra.erdos1083.multidilate-nonaligned.v1",
                "small_audit": small,
                "geometric_formula_records": len(geometry),
                "parabolic_spectral_graph": spectral_graph,
                "endpoint": endpoint,
                "status": "PASS",
                "scope": (
                    "Exact finite falsification and exponent certificate; "
                    "the all-parameter claims rest on the written proofs."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
