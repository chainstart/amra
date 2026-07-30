"""Exact high-risk three-star certificate for the OPG-1757 frontier.

The construction starts from the fixed nine-vertex graph ``H?`bM~^`` and
the inherited edge pair with indexes ``(0, 2)``.  It appends

* one base-only star with neighbourhood mask 17, namely ``{0, 4}``;
* one base-only star with neighbourhood mask 36, namely ``{2, 5}``;
* one base-only star with an arbitrary one of all 512 neighbourhoods; and
* ``t`` mutually nonadjacent false twins with neighbourhood
  ``{1, 5, 6, 7, 8}``, for every integer ``t >= 0``.

There are no edges among any of the appended vertices.  Only the inherited
edge pair is certified.  The fixed masks 17 and 36 are the two-star family
that is closest to equality at ``t=10000`` in the complete two-star survey.

All arithmetic in this module is exact.  A forgotten-star transfer propagates
four independent forced-edge channels on partitions of the nine base
vertices.  The third star is a terminal linear functional.  The universal
identity ``(T_S - 6 I)^5 = 0`` follows because every nonidentity part of
``T_S - 6 I`` strictly merges two of the at most five blocks occupied by
``S``.  It is also checked coordinate by coordinate on the concrete
post-two-star distribution.  Consequently five exact values determine every
count for all nonnegative ``t``; a sixth value is retained as an
out-of-interpolation check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Mapping, Sequence

from amra.discovery.opg_coloring_search import decode_graph6
from amra.discovery.opg_uniform_forest_twin_defect import (
    _count_closed_forms,
    terminal_defect_count_vector,
)
from amra.discovery.opg_uniform_forest_twin_transfer import (
    COUNT_CHANNEL_NAMES,
    DEFAULT_FALSE_TWIN_BASE_GRAPH6,
    DEFAULT_FALSE_TWIN_EDGE_PAIR,
    DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
    KRYLOV_RECURRENCE_COEFFICIENTS,
    CountVector,
    ExponentialPolynomial,
    FalseTwinCertificateError,
    Partition,
    _advance_false_twin_distribution,
    _atomic_write_json,
    _canonical_json_bytes,
    _closed_form_payload,
    _combine_forced_distributions,
    _derive_margin_closed_form,
    _distribution_digest,
)


CERTIFICATE_SCHEMA = "amra.opg1757.three-star-high-risk.v1"
FIXED_FIRST_STAR_MASK = 17
FIXED_SECOND_STAR_MASK = 36
BASE_VERTEX_COUNT = 9
NEIGHBOURHOOD_COUNT = 1 << BASE_VERTEX_COUNT
KRYLOV_VECTOR_COUNT = 6
RATIO_SAMPLE_TWIN_COUNTS = (0, 1, 2, 4, 10, 100, 10_000)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _neighbourhood_from_mask(mask: int) -> tuple[int, ...]:
    if type(mask) is not int or not 0 <= mask < NEIGHBOURHOOD_COUNT:
        raise ValueError("mask must be an integer in [0, 512)")
    return tuple(
        vertex
        for vertex in range(BASE_VERTEX_COUNT)
        if mask & (1 << vertex)
    )


def _sequence_record(
    sequence: ExponentialPolynomial,
) -> dict[str, object]:
    payload = _closed_form_payload(sequence)
    return {
        "power_base": sequence.power_base,
        "denominator": sequence.denominator,
        "polynomial_coefficients": list(
            sequence.polynomial_coefficients
        ),
        "polynomial_degree": payload["polynomial_degree"],
        "symbolic_annihilator_residual_coefficients": payload[
            "symbolic_recurrence_residual_coefficients"
        ],
        "all_nonnegative_integer_t_integral": payload["integrality"][
            "all_nonnegative_integer_t_integral"
        ],
    }


def _coordinate_recurrence_audit(
    distributions: Sequence[Mapping[Partition, CountVector]],
) -> dict[str, object]:
    if len(distributions) != KRYLOV_VECTOR_COUNT:
        raise ValueError("six Krylov distributions are required")
    partitions = set().union(*(distribution for distribution in distributions))
    residual_digest = hashlib.sha256()
    nonzero_coordinates = 0
    maximum_absolute_residual = 0
    for partition in sorted(partitions):
        for channel in range(len(COUNT_CHANNEL_NAMES)):
            residual = sum(
                coefficient
                * distributions[shift].get(partition, (0, 0, 0, 0))[
                    channel
                ]
                for shift, coefficient in enumerate(
                    KRYLOV_RECURRENCE_COEFFICIENTS
                )
            )
            residual_digest.update(
                _canonical_json_bytes(
                    [list(partition), channel, str(residual)]
                )
            )
            if residual:
                nonzero_coordinates += 1
                maximum_absolute_residual = max(
                    maximum_absolute_residual, abs(residual)
                )
    if nonzero_coordinates:
        raise FalseTwinCertificateError(
            "the post-two-star Krylov recurrence did not close"
        )
    return {
        "annihilator": "(T_S-6I)^5",
        "recurrence_coefficients_in_ascending_shift": list(
            KRYLOV_RECURRENCE_COEFFICIENTS
        ),
        "partition_count": len(partitions),
        "channel_count": len(COUNT_CHANNEL_NAMES),
        "coordinate_count": len(partitions) * len(COUNT_CHANNEL_NAMES),
        "nonzero_residual_coordinates": nonzero_coordinates,
        "maximum_absolute_residual": maximum_absolute_residual,
        "residual_rows_sha256": residual_digest.hexdigest(),
        "distribution_sha256_t0_through_t5": [
            _distribution_digest(dict(distribution))
            for distribution in distributions
        ],
    }


def _ratio(
    sequences: Sequence[ExponentialPolynomial],
    twin_count: int,
) -> tuple[int, int]:
    counts = tuple(
        sequence.evaluate(twin_count) for sequence in sequences
    )
    numerator = counts[0] * counts[3]
    denominator = counts[1] * counts[2]
    if not 0 <= numerator < denominator:
        raise FalseTwinCertificateError(
            "a sampled inherited-pair ratio is not in [0, 1)"
        )
    common_divisor = math.gcd(numerator, denominator)
    return numerator // common_divisor, denominator // common_divisor


def _build_post_two_star_krylov_vectors(
) -> tuple[dict[Partition, CountVector], ...]:
    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    distribution = _combine_forced_distributions(
        graph, DEFAULT_FALSE_TWIN_EDGE_PAIR
    )
    for mask in (FIXED_FIRST_STAR_MASK, FIXED_SECOND_STAR_MASK):
        distribution = _advance_false_twin_distribution(
            distribution,
            _neighbourhood_from_mask(mask),
            {},
        )
    vectors = [distribution]
    transition_cache = {}
    for _ in range(KRYLOV_VECTOR_COUNT - 1):
        vectors.append(
            _advance_false_twin_distribution(
                vectors[-1],
                DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
                transition_cache,
            )
        )
    return tuple(vectors)


def build_three_star_high_risk_certificate() -> dict[str, object]:
    """Recompute the complete 512-neighbourhood exact certificate."""

    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    if graph.vertex_count != BASE_VERTEX_COUNT or len(graph.edges) != 19:
        raise FalseTwinCertificateError(
            "the fixed OPG-1757 base graph changed"
        )
    if tuple(
        graph.edges[index] for index in DEFAULT_FALSE_TWIN_EDGE_PAIR
    ) != ((0, 4), (2, 5)):
        raise FalseTwinCertificateError(
            "the inherited edge-pair endpoints changed"
        )

    distributions = _build_post_two_star_krylov_vectors()
    recurrence_audit = _coordinate_recurrence_audit(distributions)
    records = []
    degree_histogram: dict[str, int] = {}
    minimum_coefficient: int | None = None
    ratio_maxima: dict[
        int, tuple[int, int, int]
    ] = {}

    for mask in range(NEIGHBOURHOOD_COUNT):
        neighbourhood = _neighbourhood_from_mask(mask)
        direct_values = tuple(
            terminal_defect_count_vector(
                distribution, neighbourhood
            )
            for distribution in distributions
        )
        sequences = _count_closed_forms(direct_values[:5])
        predicted_t5 = tuple(
            sequence.evaluate(5) for sequence in sequences
        )
        if predicted_t5 != direct_values[5]:
            raise FalseTwinCertificateError(
                f"the t=5 holdout failed for third-star mask {mask}"
            )
        margin = _derive_margin_closed_form(sequences)
        margin_payload = _closed_form_payload(margin)
        coefficients = margin.polynomial_coefficients
        if any(coefficient <= 0 for coefficient in coefficients):
            raise FalseTwinCertificateError(
                "a high-risk three-star margin polynomial lacks a "
                f"strictly positive coefficient: mask={mask}, "
                f"coefficients={coefficients}"
            )
        degree = len(coefficients) - 1
        degree_histogram[str(degree)] = (
            degree_histogram.get(str(degree), 0) + 1
        )
        row_minimum = min(coefficients)
        minimum_coefficient = (
            row_minimum
            if minimum_coefficient is None
            else min(minimum_coefficient, row_minimum)
        )

        for twin_count in RATIO_SAMPLE_TWIN_COUNTS:
            numerator, denominator = _ratio(sequences, twin_count)
            incumbent = ratio_maxima.get(twin_count)
            if (
                incumbent is None
                or numerator * incumbent[1]
                > incumbent[0] * denominator
            ):
                ratio_maxima[twin_count] = (
                    numerator,
                    denominator,
                    mask,
                )

        records.append(
            {
                "third_star_mask": mask,
                "third_star_neighbourhood": list(neighbourhood),
                "initial_count_vectors_t0_through_t5": [
                    list(vector) for vector in direct_values
                ],
                "count_closed_forms": {
                    sequence.name: _sequence_record(sequence)
                    for sequence in sequences
                },
                "margin_closed_form": {
                    "power_base": margin.power_base,
                    "denominator": margin.denominator,
                    "polynomial_coefficients": list(coefficients),
                    "polynomial_degree": degree,
                    "symbolic_annihilator_residual_coefficients": (
                        margin_payload[
                            "symbolic_recurrence_residual_coefficients"
                        ]
                    ),
                    "all_coefficients_strictly_positive": True,
                },
                "t5_holdout_matches": True,
            }
        )

    if len(records) != NEIGHBOURHOOD_COUNT:
        raise FalseTwinCertificateError(
            "the third-star neighbourhood enumeration is incomplete"
        )

    module_path = Path(__file__).resolve()
    transfer_path = module_path.with_name(
        "opg_uniform_forest_twin_transfer.py"
    )
    terminal_path = module_path.with_name(
        "opg_uniform_forest_twin_defect.py"
    )
    return {
        "schema": CERTIFICATE_SCHEMA,
        "status": "certified",
        "scope": {
            "base_graph6": graph.encoding,
            "base_vertex_count": graph.vertex_count,
            "base_edge_count": len(graph.edges),
            "inherited_edge_pair_indexes": list(
                DEFAULT_FALSE_TWIN_EDGE_PAIR
            ),
            "inherited_edge_pair_endpoints": [
                list(graph.edges[index])
                for index in DEFAULT_FALSE_TWIN_EDGE_PAIR
            ],
            "fixed_first_star_mask": FIXED_FIRST_STAR_MASK,
            "fixed_first_star_neighbourhood": list(
                _neighbourhood_from_mask(FIXED_FIRST_STAR_MASK)
            ),
            "fixed_second_star_mask": FIXED_SECOND_STAR_MASK,
            "fixed_second_star_neighbourhood": list(
                _neighbourhood_from_mask(FIXED_SECOND_STAR_MASK)
            ),
            "third_star_neighbourhood_domain": (
                "every subset of the nine base vertices"
            ),
            "repeated_false_twin_neighbourhood": list(
                DEFAULT_FALSE_TWIN_NEIGHBOURHOOD
            ),
            "repeated_false_twin_count": "every integer t >= 0",
            "edges_among_all_added_vertices": 0,
            "all_edge_pairs_checked": False,
            "certified_edge_pair": "the inherited edge pair only",
        },
        "method": {
            "base_state": (
                "exact four-channel forward forest distribution on "
                "partitions of the nine base vertices"
            ),
            "first_two_stars": (
                "exact forgotten-star transfers U_{17} and U_{36}"
            ),
            "third_star": (
                "terminal functional product_C(1+|C intersect R|)"
            ),
            "commutation": (
                "all added star vertices are mutually nonadjacent, so their "
                "forgotten-star transfers commute by the contracted "
                "bipartite-forest bijection"
            ),
            "universal_annihilator": (
                "T_S=6I+N_S and every N_S transition strictly merges "
                "two of at most five S-blocks, hence N_S^5=0"
            ),
            "count_form": "C_i(t)=6^t P_i(t)/d_i with degree(P_i)<=4",
            "margin_form": "M(t)=36^t P(t)/d",
            "positivity": (
                "every margin denominator and every ordinary-power "
                "coefficient of every P are strictly positive"
            ),
            "holdout": (
                "the direct t=5 count vector is not used to interpolate "
                "the degree-at-most-four count forms"
            ),
        },
        "krylov_recurrence": recurrence_audit,
        "summary": {
            "third_star_neighbourhood_count": len(records),
            "expected_third_star_neighbourhood_count": (
                NEIGHBOURHOOD_COUNT
            ),
            "all_margin_coefficients_strictly_positive": True,
            "minimum_margin_polynomial_coefficient": minimum_coefficient,
            "margin_polynomial_degree_histogram": degree_histogram,
            "all_t5_holdouts_match": True,
            "selected_inherited_pair_is_never_a_counterexample": True,
            "all_edge_pairs_checked": False,
            "whole_graph_family_counterexample_exhaustion_claimed": False,
        },
        "ratio_sample_maxima": [
            {
                "twin_count": twin_count,
                "third_star_mask": ratio_maxima[twin_count][2],
                "third_star_neighbourhood": list(
                    _neighbourhood_from_mask(
                        ratio_maxima[twin_count][2]
                    )
                ),
                "ratio_numerator": str(
                    ratio_maxima[twin_count][0]
                ),
                "ratio_denominator": str(
                    ratio_maxima[twin_count][1]
                ),
                "relative_gap_numerator": str(
                    ratio_maxima[twin_count][1]
                    - ratio_maxima[twin_count][0]
                ),
                "relative_gap_denominator": str(
                    ratio_maxima[twin_count][1]
                ),
            }
            for twin_count in RATIO_SAMPLE_TWIN_COUNTS
        ],
        "implementation": [
            {
                "path": str(module_path),
                "sha256": _file_sha256(module_path),
            },
            {
                "path": str(transfer_path),
                "sha256": _file_sha256(transfer_path),
            },
            {
                "path": str(terminal_path),
                "sha256": _file_sha256(terminal_path),
            },
        ],
        "records": records,
    }


def verify_three_star_high_risk_certificate(payload: object) -> None:
    """Fail closed by rebuilding and byte-comparing the certificate."""

    if not isinstance(payload, dict):
        raise FalseTwinCertificateError(
            "three-star certificate must be a JSON object"
        )
    if (
        payload.get("schema") != CERTIFICATE_SCHEMA
        or payload.get("status") != "certified"
    ):
        raise FalseTwinCertificateError(
            "three-star certificate schema/status is invalid"
        )
    expected = build_three_star_high_risk_certificate()
    if _canonical_json_bytes(payload) != _canonical_json_bytes(expected):
        raise FalseTwinCertificateError(
            "three-star certificate differs from exact recomputation"
        )


def write_three_star_high_risk_certificate(
    path: Path,
    payload: object,
) -> None:
    """Recompute-verify, then atomically persist a certificate."""

    verify_three_star_high_risk_certificate(payload)
    _atomic_write_json(path, payload)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Certify the high-risk three-star OPG-1757 extension family."
        )
    )
    commands = parser.add_subparsers(dest="command", required=True)
    certify = commands.add_parser("certify")
    certify.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("certificate", type=Path)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "certify":
            payload = build_three_star_high_risk_certificate()
            write_three_star_high_risk_certificate(
                arguments.output, payload
            )
            result = {
                "status": "certified",
                "output": str(arguments.output),
                "third_star_neighbourhood_count": (
                    NEIGHBOURHOOD_COUNT
                ),
            }
        else:
            payload = json.loads(
                arguments.certificate.read_text(encoding="utf-8")
            )
            verify_three_star_high_risk_certificate(payload)
            result = {
                "status": "verified",
                "certificate": str(arguments.certificate),
                "third_star_neighbourhood_count": (
                    NEIGHBOURHOOD_COUNT
                ),
            }
    except (
        FalseTwinCertificateError,
        json.JSONDecodeError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
