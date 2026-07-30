"""Exact one-defect survey for the OPG-1757 false-twin frontier.

Start with the fixed nine-vertex frontier graph, append ``t`` independent
false twins with the recorded five-vertex neighbourhood, and finally append
one defect vertex adjacent to an arbitrary subset of the nine base vertices.
This module certifies the inherited near-critical edge pair only.

The final defect vertex need not be retained in the partition state.  If a
base partition has ``c`` selected neighbours in one block, an acyclic star
may choose none or exactly one of them.  Thus the exact number of valid
incident-edge subsets is the product of ``1+c`` over blocks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

from amra.discovery.opg_coloring_search import decode_graph6
from amra.discovery.opg_uniform_forest_twin_transfer import (
    COUNT_CHANNEL_NAMES,
    DEFAULT_FALSE_TWIN_BASE_GRAPH6,
    DEFAULT_FALSE_TWIN_EDGE_PAIR,
    DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
    KRYLOV_ORDER,
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
    _interpolate_exponential_polynomial,
    build_krylov_recurrence_certificate,
)


DEFECT_SURVEY_SCHEMA = "amra.opg1757.false-twin-terminal-defect.v1"


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _validated_defect_neighbourhood(
    vertex_count: int,
    neighbourhood: Sequence[int],
) -> tuple[int, ...]:
    value = tuple(neighbourhood)
    if any(
        type(vertex) is not int or not 0 <= vertex < vertex_count
        for vertex in value
    ):
        raise ValueError("defect neighbourhood contains an invalid vertex")
    if tuple(sorted(set(value))) != value:
        raise ValueError(
            "defect neighbourhood must be a sorted set of base vertices"
        )
    return value


def terminal_star_subset_multiplier(
    partition: Sequence[int],
    neighbourhood: Sequence[int],
) -> int:
    """Count acyclic choices among the terminal defect's incident edges."""

    base_partition = tuple(partition)
    if any(type(label) is not int or label < 0 for label in base_partition):
        raise ValueError("partition labels must be non-negative integers")
    neighbours = _validated_defect_neighbourhood(
        len(base_partition), neighbourhood
    )
    block_counts: dict[int, int] = {}
    for vertex in neighbours:
        label = base_partition[vertex]
        block_counts[label] = block_counts.get(label, 0) + 1
    multiplier = 1
    for count in block_counts.values():
        multiplier *= count + 1
    return multiplier


def terminal_defect_count_vector(
    distribution: Mapping[Partition, CountVector],
    neighbourhood: Sequence[int],
) -> CountVector:
    """Apply the terminal-star linear functional to four count channels."""

    totals = [0, 0, 0, 0]
    for partition, vector in distribution.items():
        if len(vector) != 4 or any(type(value) is not int for value in vector):
            raise ValueError("distribution must contain four integer channels")
        multiplier = terminal_star_subset_multiplier(
            partition, neighbourhood
        )
        for channel, value in enumerate(vector):
            totals[channel] += multiplier * value
    return tuple(totals)


def _count_closed_forms(
    initial_values: Sequence[CountVector],
) -> tuple[ExponentialPolynomial, ...]:
    if len(initial_values) != KRYLOV_ORDER:
        raise FalseTwinCertificateError(
            "terminal defect needs exactly five Krylov projections"
        )
    sequences = tuple(
        _interpolate_exponential_polynomial(
            name,
            [row[channel] for row in initial_values],
        )
        for channel, name in enumerate(COUNT_CHANNEL_NAMES)
    )
    # This checks the symbolic annihilator and the exact divisibility needed
    # for every non-negative integer t, not merely the five interpolation
    # points.
    for sequence in sequences:
        _closed_form_payload(sequence)
    return sequences


def _sequence_record(sequence: ExponentialPolynomial) -> dict[str, object]:
    return {
        "power_base": sequence.power_base,
        "denominator": sequence.denominator,
        "polynomial_coefficients": list(
            sequence.polynomial_coefficients
        ),
    }


def _neighbourhood_from_mask(mask: int, vertex_count: int) -> tuple[int, ...]:
    return tuple(
        vertex for vertex in range(vertex_count) if mask & (1 << vertex)
    )


def build_terminal_defect_survey() -> dict[str, object]:
    """Certify all ``2^9`` base-only terminal-defect neighbourhoods."""

    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    base_certificate = build_krylov_recurrence_certificate(
        DEFAULT_FALSE_TWIN_BASE_GRAPH6,
        DEFAULT_FALSE_TWIN_EDGE_PAIR,
        DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
    )
    if (
        base_certificate["krylov_recurrence"][
            "nonzero_residual_coordinates"
        ]
        != 0
    ):
        raise FalseTwinCertificateError(
            "base false-twin Krylov certificate did not close"
        )

    distributions = [
        _combine_forced_distributions(
            graph, DEFAULT_FALSE_TWIN_EDGE_PAIR
        )
    ]
    transition_cache = {}
    for _ in range(KRYLOV_ORDER - 1):
        distributions.append(
            _advance_false_twin_distribution(
                distributions[-1],
                DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
                transition_cache,
            )
        )

    records = []
    degree_histogram: dict[str, int] = {}
    minimum_coefficient: int | None = None
    for mask in range(1 << graph.vertex_count):
        neighbourhood = _neighbourhood_from_mask(
            mask, graph.vertex_count
        )
        initial_values = tuple(
            terminal_defect_count_vector(
                distribution, neighbourhood
            )
            for distribution in distributions
        )
        count_sequences = _count_closed_forms(initial_values)
        margin = _derive_margin_closed_form(count_sequences)
        margin_payload = _closed_form_payload(margin)
        coefficients = margin.polynomial_coefficients
        if any(coefficient <= 0 for coefficient in coefficients):
            raise FalseTwinCertificateError(
                "terminal defect has a non-positive margin coefficient: "
                f"{neighbourhood} -> {coefficients}"
            )
        for twin_count, direct in enumerate(initial_values):
            evaluated = tuple(
                sequence.evaluate(twin_count)
                for sequence in count_sequences
            )
            if evaluated != direct:
                raise FalseTwinCertificateError(
                    "terminal-defect closed form misses an initial value"
                )
        derived_margin = _derive_margin_closed_form(count_sequences)
        if derived_margin != margin:
            raise FalseTwinCertificateError(
                "terminal-defect margin derivation is unstable"
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
        records.append(
            {
                "mask": mask,
                "neighbourhood": list(neighbourhood),
                "neighbourhood_size": len(neighbourhood),
                "initial_count_vectors_t0_through_t4": [
                    list(row) for row in initial_values
                ],
                "count_closed_forms": {
                    sequence.name: _sequence_record(sequence)
                    for sequence in count_sequences
                },
                "margin": {
                    **_sequence_record(margin),
                    "polynomial_degree": degree,
                    "all_coefficients_strictly_positive": True,
                    "symbolic_annihilator_residual_coefficients": (
                        margin_payload[
                            "symbolic_recurrence_residual_coefficients"
                        ]
                    ),
                },
            }
        )

    module_path = Path(__file__).resolve()
    transfer_path = module_path.with_name(
        "opg_uniform_forest_twin_transfer.py"
    )
    return {
        "schema": DEFECT_SURVEY_SCHEMA,
        "status": "certified",
        "construction": {
            "base_graph6": graph.encoding,
            "repeated_false_twin_neighbourhood": list(
                DEFAULT_FALSE_TWIN_NEIGHBOURHOOD
            ),
            "repeated_false_twin_count": "arbitrary integer t >= 0",
            "terminal_defect_neighbourhood_domain": (
                "every subset of the nine base vertices"
            ),
            "terminal_defect_may_join_repeated_twins": False,
            "inherited_edge_pair": list(DEFAULT_FALSE_TWIN_EDGE_PAIR),
            "inherited_edge_pair_endpoints": [
                list(graph.edges[index])
                for index in DEFAULT_FALSE_TWIN_EDGE_PAIR
            ],
        },
        "proof": {
            "terminal_star_multiplier": (
                "product over base-partition blocks C of "
                "(1 + |C intersect R|)"
            ),
            "linearity": (
                "the terminal-star count is a fixed linear projection of "
                "v_t, so (T-6I)^5 v_0=0 gives the same order-five "
                "recurrence for every projected count sequence"
            ),
            "margin_identity": (
                "forest_count_e*forest_count_f - "
                "forest_count*forest_count_ef"
            ),
            "positivity": (
                "each exact margin equals 36^t P_R(t)/d_R; every d_R "
                "and every coefficient of every P_R are strictly positive"
            ),
            "base_krylov_residual_sha256": base_certificate[
                "krylov_recurrence"
            ]["residual_vector_sha256"],
        },
        "summary": {
            "neighbourhood_count": len(records),
            "expected_neighbourhood_count": 1 << graph.vertex_count,
            "all_margin_coefficients_strictly_positive": True,
            "minimum_margin_polynomial_coefficient": minimum_coefficient,
            "margin_polynomial_degree_histogram": degree_histogram,
            "selected_inherited_pair_is_never_a_counterexample": True,
            "all_edge_pairs_checked": False,
            "defects_joining_repeated_twins_checked": False,
            "whole_graph_family_counterexample_exhaustion_claimed": False,
        },
        "implementation": [
            {
                "path": str(module_path),
                "sha256": _file_sha256(module_path),
            },
            {
                "path": str(transfer_path),
                "sha256": _file_sha256(transfer_path),
            },
        ],
        "records": records,
    }


def verify_terminal_defect_survey(payload: object) -> None:
    if not isinstance(payload, dict):
        raise FalseTwinCertificateError(
            "terminal-defect survey must be a JSON object"
        )
    if (
        payload.get("schema") != DEFECT_SURVEY_SCHEMA
        or payload.get("status") != "certified"
    ):
        raise FalseTwinCertificateError(
            "terminal-defect survey schema/status is invalid"
        )
    expected = build_terminal_defect_survey()
    if _canonical_json_bytes(payload) != _canonical_json_bytes(expected):
        raise FalseTwinCertificateError(
            "terminal-defect survey differs from exact recomputation"
        )


def write_terminal_defect_survey(
    path: Path,
    payload: object,
) -> None:
    verify_terminal_defect_survey(payload)
    _atomic_write_json(path, payload)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Certify all base-only terminal defects of the OPG-1757 "
            "false-twin frontier."
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
            payload = build_terminal_defect_survey()
            write_terminal_defect_survey(arguments.output, payload)
            result = {
                "status": "certified",
                "output": str(arguments.output),
                "neighbourhood_count": payload["summary"][
                    "neighbourhood_count"
                ],
            }
        else:
            payload = json.loads(
                arguments.certificate.read_text(encoding="utf-8")
            )
            verify_terminal_defect_survey(payload)
            result = {
                "status": "verified",
                "certificate": str(arguments.certificate),
                "neighbourhood_count": payload["summary"][
                    "neighbourhood_count"
                ],
            }
    except (
        FalseTwinCertificateError,
        OSError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ) as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
