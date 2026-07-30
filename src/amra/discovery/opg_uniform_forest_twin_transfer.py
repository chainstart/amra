"""Independent transfer DP for a repeated false-twin extension family.

This module is intentionally separate from the recursive deletion-contraction
counter used by the exhaustive OPG-1757 runner.  It processes the base edges
forward while retaining a distribution over partitions of the base vertices.
Each appended false twin is then handled by a transfer that never adds the
twin to the persistent state.

For a current base partition, selecting incident edges from a new twin to a
neighbourhood is acyclic exactly when the selected neighbours lie in distinct
blocks.  After those blocks are merged, the twin can be forgotten.  Different
incident-edge subsets that produce the same base partition are retained as a
transition multiplicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

from amra.discovery.opg_coloring_search import EdgeGraph, decode_graph6


Partition = tuple[int, ...]
PartitionDistribution = dict[Partition, int]
CountVector = tuple[int, int, int, int]
TwinTransition = tuple[tuple[Partition, int], ...]

DEFAULT_FALSE_TWIN_BASE_GRAPH6 = "H?`bM~^"
DEFAULT_FALSE_TWIN_EDGE_PAIR = (0, 2)
DEFAULT_FALSE_TWIN_NEIGHBOURHOOD = (1, 5, 6, 7, 8)
COUNT_CHANNEL_NAMES = (
    "forest_count",
    "forest_count_e",
    "forest_count_f",
    "forest_count_ef",
)
KRYLOV_RECURRENCE_COEFFICIENTS = (
    -7776,
    6480,
    -2160,
    360,
    -30,
    1,
)
KRYLOV_SHIFT = 6
KRYLOV_ORDER = 5
CERTIFICATE_TRANSFER_SAMPLES = (0, 1, 2, 3, 4, 5, 10, 25, 100)
CERTIFICATE_LARGE_T = 10_000


class FalseTwinCertificateError(RuntimeError):
    """Raised when an exact certificate check does not close."""


@dataclass(frozen=True)
class ExponentialPolynomial:
    """An exact sequence ``base**t * polynomial(t) / denominator``."""

    name: str
    power_base: int
    denominator: int
    polynomial_coefficients: tuple[int, ...]

    def numerator(self, twin_count: int) -> int:
        _validate_twin_count(twin_count)
        return self.power_base**twin_count * _evaluate_polynomial(
            self.polynomial_coefficients, twin_count
        )

    def evaluate(self, twin_count: int) -> int:
        numerator = self.numerator(twin_count)
        quotient, remainder = divmod(numerator, self.denominator)
        if remainder:
            raise FalseTwinCertificateError(
                f"{self.name} closed form is nonintegral at t={twin_count}"
            )
        return quotient


@dataclass(frozen=True)
class CertifiedFalseTwinCase:
    case_id: str
    base_graph6: str
    edge_pair: tuple[int, int]
    neighbourhood: tuple[int, ...]
    expected_margin: ExponentialPolynomial
    expected_counts: tuple[ExponentialPolynomial, ...] | None = None


CLOSED_FORM_SEQUENCES = (
    ExponentialPolynomial(
        "forest_count",
        6,
        72,
        (3_896_928, 1_974_866, 366_609, 29_570, 875),
    ),
    ExponentialPolynomial(
        "forest_count_e",
        6,
        144,
        (2_840_544, 1_433_530, 264_867, 21_250, 625),
    ),
    ExponentialPolynomial(
        "forest_count_f",
        6,
        216,
        (4_643_136, 2_259_386, 401_713, 30_970, 875),
    ),
    ExponentialPolynomial(
        "forest_count_ef",
        6,
        432,
        (3_384_288, 1_639_762, 290_147, 22_250, 625),
    ),
)
MARGIN_CLOSED_FORM = ExponentialPolynomial(
    "negative_association_margin",
    36,
    108,
    (2_449_440, 1_424_790, 319_228, 33_749, 1_616, 25),
)
CERTIFIED_FALSE_TWIN_CASES = (
    CertifiedFalseTwinCase(
        "family-a",
        DEFAULT_FALSE_TWIN_BASE_GRAPH6,
        DEFAULT_FALSE_TWIN_EDGE_PAIR,
        DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
        MARGIN_CLOSED_FORM,
        CLOSED_FORM_SEQUENCES,
    ),
    CertifiedFalseTwinCase(
        "family-b",
        "H?`al}~",
        (0, 1),
        (2, 5, 6, 7, 8),
        ExponentialPolynomial(
            "negative_association_margin",
            36,
            243,
            (7_348_320, 4_644_108, 1_126_195, 127_724, 6_449, 100),
        ),
    ),
    CertifiedFalseTwinCase(
        "family-c",
        "H?`Dvnv",
        (0, 1),
        (0, 2, 6, 7, 8),
        ExponentialPolynomial(
            "negative_association_margin",
            36,
            243,
            (7_278_336, 4_602_420, 1_118_455, 127_256, 6_449, 100),
        ),
    ),
)


@dataclass(frozen=True)
class FalseTwinForestCounts:
    """The four exact forest counts for one number of appended false twins."""

    twin_count: int
    forest_count: int
    forest_count_e: int
    forest_count_f: int
    forest_count_ef: int
    active_partitions: int

    @property
    def left_product(self) -> int:
        return self.forest_count * self.forest_count_ef

    @property
    def right_product(self) -> int:
        return self.forest_count_e * self.forest_count_f

    @property
    def margin(self) -> int:
        """Return right-left; a negative value is a counterexample."""

        return self.right_product - self.left_product

    @property
    def violates_negative_association(self) -> bool:
        return self.left_product > self.right_product

    @property
    def ratio(self) -> Fraction:
        return Fraction(self.left_product, self.right_product)

    @property
    def relative_gap(self) -> Fraction:
        """Return ``(right-left)/right`` exactly."""

        return Fraction(self.margin, self.right_product)

    def as_dict(self) -> dict[str, object]:
        ratio = self.ratio
        relative_gap = self.relative_gap
        return {
            "twin_count": self.twin_count,
            "forest_count": self.forest_count,
            "forest_count_e": self.forest_count_e,
            "forest_count_f": self.forest_count_f,
            "forest_count_ef": self.forest_count_ef,
            "left_product": self.left_product,
            "right_product": self.right_product,
            "margin": self.margin,
            "ratio_numerator": ratio.numerator,
            "ratio_denominator": ratio.denominator,
            "relative_gap_numerator": relative_gap.numerator,
            "relative_gap_denominator": relative_gap.denominator,
            "violates_negative_association": (
                self.violates_negative_association
            ),
            "active_partitions": self.active_partitions,
        }


@dataclass(frozen=True)
class FalseTwinTransferScan:
    """Exact scan of a fixed false-twin family."""

    base_graph6: str
    base_vertex_count: int
    base_edge_count: int
    edge_pair: tuple[int, int]
    edge_pair_endpoints: tuple[tuple[int, int], tuple[int, int]]
    neighbourhood: tuple[int, ...]
    counts: tuple[FalseTwinForestCounts, ...]
    cached_partitions: int
    cached_transition_arcs: int
    elapsed_seconds: float

    @property
    def has_violation(self) -> bool:
        return any(
            count.violates_negative_association for count in self.counts
        )

    @property
    def ratios_strictly_increase(self) -> bool:
        return all(
            left.ratio < right.ratio
            for left, right in zip(self.counts, self.counts[1:])
        )

    @property
    def relative_gaps_strictly_decrease(self) -> bool:
        return all(
            left.relative_gap > right.relative_gap
            for left, right in zip(self.counts, self.counts[1:])
        )

    @property
    def minimum_relative_gap(self) -> FalseTwinForestCounts:
        return min(self.counts, key=lambda count: count.relative_gap)

    def as_dict(self) -> dict[str, object]:
        minimum = self.minimum_relative_gap
        return {
            "schema": "amra.opg1757.false-twin-transfer.v1",
            "method": (
                "independent-forward-base-partition-and-forgotten-twin-"
                "transfer-dp"
            ),
            "base_graph6": self.base_graph6,
            "base_vertex_count": self.base_vertex_count,
            "base_edge_count": self.base_edge_count,
            "edge_pair": list(self.edge_pair),
            "edge_pair_endpoints": [
                list(edge) for edge in self.edge_pair_endpoints
            ],
            "neighbourhood": list(self.neighbourhood),
            "max_twins": self.counts[-1].twin_count,
            "has_violation": self.has_violation,
            "ratios_strictly_increase": self.ratios_strictly_increase,
            "relative_gaps_strictly_decrease": (
                self.relative_gaps_strictly_decrease
            ),
            "minimum_relative_gap_at": minimum.twin_count,
            "minimum_relative_gap_numerator": (
                minimum.relative_gap.numerator
            ),
            "minimum_relative_gap_denominator": (
                minimum.relative_gap.denominator
            ),
            "cached_partitions": self.cached_partitions,
            "cached_transition_arcs": self.cached_transition_arcs,
            "elapsed_seconds": self.elapsed_seconds,
            "counts": [count.as_dict() for count in self.counts],
        }


def _validate_twin_count(twin_count: int) -> None:
    if (
        not isinstance(twin_count, int)
        or isinstance(twin_count, bool)
        or twin_count < 0
    ):
        raise ValueError("twin_count must be a non-negative integer")


def _evaluate_polynomial(
    coefficients: Sequence[int],
    value: int,
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def _shift_polynomial(
    coefficients: Sequence[int],
    shift: int,
) -> tuple[int, ...]:
    """Return ascending coefficients of ``P(t + shift)``."""

    result = [0] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        for target_degree in range(degree + 1):
            result[target_degree] += (
                coefficient
                * math.comb(degree, target_degree)
                * shift ** (degree - target_degree)
            )
    return tuple(result)


def _multiply_polynomials(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] += (
                left_coefficient * right_coefficient
            )
    return tuple(result)


def _normalize_fraction_polynomial(
    coefficients: Sequence[Fraction],
) -> tuple[tuple[int, ...], int]:
    denominator = math.lcm(
        *(coefficient.denominator for coefficient in coefficients)
    )
    integer_coefficients = [
        int(coefficient * denominator)
        for coefficient in coefficients
    ]
    common_divisor = denominator
    for coefficient in integer_coefficients:
        common_divisor = math.gcd(
            common_divisor, abs(coefficient)
        )
    return (
        tuple(
            coefficient // common_divisor
            for coefficient in integer_coefficients
        ),
        denominator // common_divisor,
    )


def _interpolate_exponential_polynomial(
    name: str,
    values: Sequence[int],
    *,
    power_base: int = KRYLOV_SHIFT,
) -> ExponentialPolynomial:
    if len(values) != KRYLOV_ORDER:
        raise FalseTwinCertificateError(
            "closed-form interpolation needs exactly five initial values"
        )
    differences = [
        Fraction(value, power_base**twin_count)
        for twin_count, value in enumerate(values)
    ]
    newton_coefficients = []
    while differences:
        newton_coefficients.append(differences[0])
        differences = [
            differences[index + 1] - differences[index]
            for index in range(len(differences) - 1)
        ]

    polynomial = [Fraction(0)] * KRYLOV_ORDER
    binomial_basis = [Fraction(1)]
    for degree, coefficient in enumerate(newton_coefficients):
        for index, basis_coefficient in enumerate(binomial_basis):
            polynomial[index] += coefficient * basis_coefficient
        next_basis = _multiply_polynomials(
            binomial_basis,
            (Fraction(-degree), Fraction(1)),
        )
        binomial_basis = [
            basis_coefficient / (degree + 1)
            for basis_coefficient in next_basis
        ]
    integer_coefficients, denominator = (
        _normalize_fraction_polynomial(polynomial)
    )
    return ExponentialPolynomial(
        name,
        power_base,
        denominator,
        integer_coefficients,
    )


def _derive_count_closed_forms(
    krylov_vectors: Sequence[dict[Partition, CountVector]],
) -> tuple[ExponentialPolynomial, ...]:
    initial_totals = [
        _distribution_totals(vector)
        for vector in krylov_vectors[:KRYLOV_ORDER]
    ]
    return tuple(
        _interpolate_exponential_polynomial(
            name,
            [
                totals[channel]
                for totals in initial_totals
            ],
        )
        for channel, name in enumerate(COUNT_CHANNEL_NAMES)
    )


def _derive_margin_closed_form(
    sequences: Sequence[ExponentialPolynomial],
) -> ExponentialPolynomial:
    if len(sequences) != 4:
        raise FalseTwinCertificateError(
            "margin derivation needs four count sequences"
        )
    rational_polynomials = [
        tuple(
            Fraction(coefficient, sequence.denominator)
            for coefficient in sequence.polynomial_coefficients
        )
        for sequence in sequences
    ]
    right = _multiply_polynomials(
        rational_polynomials[1], rational_polynomials[2]
    )
    left = _multiply_polynomials(
        rational_polynomials[0], rational_polynomials[3]
    )
    difference = [
        right_coefficient - left_coefficient
        for right_coefficient, left_coefficient in zip(right, left)
    ]
    while len(difference) > 1 and difference[-1] == 0:
        difference.pop()
    integer_coefficients, denominator = (
        _normalize_fraction_polynomial(difference)
    )
    return ExponentialPolynomial(
        "negative_association_margin",
        KRYLOV_SHIFT**2,
        denominator,
        integer_coefficients,
    )


def _trim_polynomial(coefficients: Sequence[int]) -> tuple[int, ...]:
    result = list(coefficients)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def _closed_form_recurrence_residual(
    sequence: ExponentialPolynomial,
    recurrence_coefficients: Sequence[int],
) -> tuple[int, ...]:
    """Return the symbolic numerator of an operator on a closed form."""

    residual = [0] * len(sequence.polynomial_coefficients)
    for shift, recurrence_coefficient in enumerate(
        recurrence_coefficients
    ):
        shifted = _shift_polynomial(
            sequence.polynomial_coefficients, shift
        )
        scale = recurrence_coefficient * sequence.power_base**shift
        for degree, coefficient in enumerate(shifted):
            residual[degree] += scale * coefficient
    return tuple(residual)


def _annihilator_coefficients(
    shift: int,
    order: int,
) -> tuple[int, ...]:
    return tuple(
        math.comb(order, index)
        * (-shift) ** (order - index)
        for index in range(order + 1)
    )


def _power_divisibility_threshold(base: int, denominator: int) -> int:
    for exponent in range(65):
        if base**exponent % denominator == 0:
            return exponent
    raise FalseTwinCertificateError(
        f"no audited power-divisibility threshold for {denominator}"
    )


def closed_form_count_vector(twin_count: int) -> CountVector:
    """Evaluate all four certified count formulae exactly."""

    _validate_twin_count(twin_count)
    return _evaluate_count_closed_forms(
        CLOSED_FORM_SEQUENCES, twin_count
    )


def _evaluate_count_closed_forms(
    sequences: Sequence[ExponentialPolynomial],
    twin_count: int,
) -> CountVector:
    if len(sequences) != 4:
        raise FalseTwinCertificateError(
            "exactly four count closed forms are required"
        )
    return tuple(
        sequence.evaluate(twin_count)
        for sequence in sequences
    )


def closed_form_margin(twin_count: int) -> int:
    """Evaluate the certified positive negative-association margin."""

    _validate_twin_count(twin_count)
    return MARGIN_CLOSED_FORM.evaluate(twin_count)


def _canonical_partition(labels: Iterable[int]) -> Partition:
    """Encode a partition by first occurrence, independently of the runner."""

    canonical: dict[int, int] = {}
    result = []
    for label in labels:
        if label not in canonical:
            canonical[label] = len(canonical)
        result.append(canonical[label])
    return tuple(result)


def _merge_two_blocks(
    partition: Partition,
    left_vertex: int,
    right_vertex: int,
) -> Partition | None:
    left_label = partition[left_vertex]
    right_label = partition[right_vertex]
    if left_label == right_label:
        return None
    return _canonical_partition(
        left_label if label == right_label else label
        for label in partition
    )


def _validated_edges(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    if (
        not isinstance(vertex_count, int)
        or isinstance(vertex_count, bool)
        or vertex_count < 0
    ):
        raise ValueError("vertex_count must be a non-negative integer")
    result = []
    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("each edge must be an endpoint pair")
        left, right = edge
        if (
            not isinstance(left, int)
            or isinstance(left, bool)
            or not isinstance(right, int)
            or isinstance(right, bool)
            or not 0 <= left < vertex_count
            or not 0 <= right < vertex_count
        ):
            raise ValueError(f"edge {edge!r} is outside the vertex set")
        result.append((left, right))
    return tuple(result)


def _validated_forced_indexes(
    edge_count: int,
    forced_edge_indexes: Iterable[int],
) -> frozenset[int]:
    values = tuple(forced_edge_indexes)
    if any(
        not isinstance(index, int)
        or isinstance(index, bool)
        or not 0 <= index < edge_count
        for index in values
    ):
        raise ValueError("forced edge index is outside the edge list")
    if len(set(values)) != len(values):
        raise ValueError("forced edge indexes must be distinct")
    return frozenset(values)


def forward_partition_distribution(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
    forced_edge_indexes: Iterable[int] = (),
) -> PartitionDistribution:
    """Count base-edge forests by their final base partition.

    An optional edge has a delete branch and, if its endpoints are currently
    in different blocks, an include branch.  A forced edge has only the
    include branch.  Consequently a forced cyclic set yields an empty
    distribution.
    """

    edge_list = _validated_edges(vertex_count, edges)
    forced = _validated_forced_indexes(
        len(edge_list), forced_edge_indexes
    )
    distribution: PartitionDistribution = {
        tuple(range(vertex_count)): 1
    }
    for edge_index, (left, right) in enumerate(edge_list):
        updated: defaultdict[Partition, int] = defaultdict(int)
        for partition, multiplicity in distribution.items():
            if edge_index not in forced:
                updated[partition] += multiplicity
            merged = _merge_two_blocks(partition, left, right)
            if merged is not None:
                updated[merged] += multiplicity
        distribution = dict(updated)
    return distribution


def _validated_partition(partition: Sequence[int]) -> Partition:
    value = tuple(partition)
    if any(
        not isinstance(label, int)
        or isinstance(label, bool)
        or label < 0
        for label in value
    ):
        raise ValueError("partition labels must be non-negative integers")
    if _canonical_partition(value) != value:
        raise ValueError("partition must use restricted-growth encoding")
    return value


def _validated_neighbourhood(
    vertex_count: int,
    neighbourhood: Iterable[int],
) -> tuple[int, ...]:
    value = tuple(neighbourhood)
    if any(
        not isinstance(vertex, int)
        or isinstance(vertex, bool)
        or not 0 <= vertex < vertex_count
        for vertex in value
    ):
        raise ValueError("neighbourhood contains an invalid base vertex")
    if len(set(value)) != len(value):
        raise ValueError("neighbourhood vertices must be distinct")
    return value


def false_twin_partition_transitions(
    partition: Sequence[int],
    neighbourhood: Iterable[int],
) -> TwinTransition:
    """Return target base partitions and exact edge-subset multiplicities."""

    base_partition = _validated_partition(partition)
    neighbours = _validated_neighbourhood(
        len(base_partition), neighbourhood
    )
    targets: Counter[Partition] = Counter()
    for mask in range(1 << len(neighbours)):
        selected = tuple(
            neighbours[index]
            for index in range(len(neighbours))
            if mask & (1 << index)
        )
        selected_labels = tuple(
            base_partition[vertex] for vertex in selected
        )
        if len(set(selected_labels)) != len(selected_labels):
            continue
        if len(selected_labels) < 2:
            target = base_partition
        else:
            representative = selected_labels[0]
            merged_labels = frozenset(selected_labels[1:])
            target = _canonical_partition(
                representative if label in merged_labels else label
                for label in base_partition
            )
        targets[target] += 1
    return tuple(sorted(targets.items()))


def _advance_false_twin_distribution(
    distribution: dict[Partition, CountVector],
    neighbours: tuple[int, ...],
    transition_cache: dict[Partition, TwinTransition],
) -> dict[Partition, CountVector]:
    updated: dict[Partition, list[int]] = {}
    for partition, vector in distribution.items():
        transitions = transition_cache.get(partition)
        if transitions is None:
            transitions = false_twin_partition_transitions(
                partition, neighbours
            )
            transition_cache[partition] = transitions
        for target, multiplicity in transitions:
            target_vector = updated.setdefault(target, [0, 0, 0, 0])
            for channel, value in enumerate(vector):
                target_vector[channel] += multiplicity * value
    return {
        partition: tuple(vector)
        for partition, vector in updated.items()
    }


def _distribution_totals(
    distribution: dict[Partition, CountVector],
) -> CountVector:
    return tuple(
        sum(vector[channel] for vector in distribution.values())
        for channel in range(4)
    )


def _combine_forced_distributions(
    graph: EdgeGraph,
    edge_pair: tuple[int, int],
) -> dict[Partition, CountVector]:
    first, second = edge_pair
    distributions = (
        forward_partition_distribution(
            graph.vertex_count, graph.edges
        ),
        forward_partition_distribution(
            graph.vertex_count, graph.edges, (first,)
        ),
        forward_partition_distribution(
            graph.vertex_count, graph.edges, (second,)
        ),
        forward_partition_distribution(
            graph.vertex_count, graph.edges, (first, second)
        ),
    )
    partitions = set().union(*(distribution for distribution in distributions))
    return {
        partition: tuple(
            distribution.get(partition, 0)
            for distribution in distributions
        )
        for partition in partitions
    }


def _validated_edge_pair(
    edge_count: int,
    edge_pair: Sequence[int],
) -> tuple[int, int]:
    value = tuple(edge_pair)
    if (
        len(value) != 2
        or any(
            not isinstance(index, int)
            or isinstance(index, bool)
            or not 0 <= index < edge_count
            for index in value
        )
        or value[0] == value[1]
    ):
        raise ValueError("edge_pair must contain two distinct valid indexes")
    return value


def scan_false_twin_family(
    base_graph6: str,
    edge_pair: Sequence[int],
    neighbourhood: Iterable[int],
    *,
    max_twins: int = 100,
) -> FalseTwinTransferScan:
    """Scan ``t=0..max_twins`` exactly with a forgotten-twin transfer.

    Four separate forward base DPs represent no forced edge, forced ``e``,
    forced ``f``, and both forced.  Their weights share the same cached false
    twin transition graph, but are propagated as four independent integer
    channels.
    """

    _validate_twin_count(max_twins)
    started = time.monotonic()
    graph = decode_graph6(base_graph6)
    pair = _validated_edge_pair(len(graph.edges), edge_pair)
    neighbours = _validated_neighbourhood(
        graph.vertex_count, neighbourhood
    )
    distribution = _combine_forced_distributions(graph, pair)
    transition_cache: dict[Partition, TwinTransition] = {}
    records = []

    for twin_count in range(max_twins + 1):
        totals = _distribution_totals(distribution)
        record = FalseTwinForestCounts(
            twin_count,
            totals[0],
            totals[1],
            totals[2],
            totals[3],
            len(distribution),
        )
        if record.right_product <= 0:
            raise RuntimeError("the selected edge pair has zero support")
        records.append(record)
        if twin_count == max_twins:
            break

        distribution = _advance_false_twin_distribution(
            distribution, neighbours, transition_cache
        )

    return FalseTwinTransferScan(
        graph.encoding,
        graph.vertex_count,
        len(graph.edges),
        pair,
        (graph.edges[pair[0]], graph.edges[pair[1]]),
        neighbours,
        tuple(records),
        len(transition_cache),
        sum(
            len(transitions)
            for transitions in transition_cache.values()
        ),
        time.monotonic() - started,
    )


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256_json(value: object) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _distribution_digest(
    distribution: dict[Partition, CountVector],
) -> str:
    rows = [
        [list(partition), list(distribution[partition])]
        for partition in sorted(distribution)
    ]
    return _sha256_json(rows)


def _transition_digest(
    transition_cache: dict[Partition, TwinTransition],
) -> str:
    rows = []
    for source in sorted(transition_cache):
        rows.append(
            [
                list(source),
                [
                    [list(target), multiplicity]
                    for target, multiplicity in transition_cache[source]
                ],
            ]
        )
    return _sha256_json(rows)


def _polynomial_expression(coefficients: Sequence[int]) -> str:
    terms = []
    for degree in range(len(coefficients) - 1, -1, -1):
        coefficient = coefficients[degree]
        if degree == 0:
            term = str(coefficient)
        elif degree == 1:
            term = f"{coefficient}*t"
        else:
            term = f"{coefficient}*t^{degree}"
        terms.append(term)
    return "+".join(terms)


def _closed_form_expression(sequence: ExponentialPolynomial) -> str:
    polynomial = _polynomial_expression(
        sequence.polynomial_coefficients
    )
    return (
        f"{sequence.power_base}^t*({polynomial})/"
        f"{sequence.denominator}"
    )


def _integrality_certificate(
    sequence: ExponentialPolynomial,
) -> dict[str, object]:
    threshold = _power_divisibility_threshold(
        sequence.power_base, sequence.denominator
    )
    remainders = [
        {
            "t": twin_count,
            "numerator_mod_denominator": (
                sequence.numerator(twin_count) % sequence.denominator
            ),
        }
        for twin_count in range(threshold)
    ]
    if any(row["numerator_mod_denominator"] for row in remainders):
        raise FalseTwinCertificateError(
            f"{sequence.name} failed a prethreshold divisibility check"
        )
    return {
        "power_divisibility_from_t": threshold,
        "prethreshold_remainders": remainders,
        "proof": (
            "all listed prethreshold remainders are zero; from the "
            "threshold onward the denominator divides power_base^t"
        ),
        "all_nonnegative_integer_t_integral": True,
    }


def _closed_form_payload(
    sequence: ExponentialPolynomial,
) -> dict[str, object]:
    annihilator_order = len(sequence.polynomial_coefficients)
    annihilator_coefficients = _annihilator_coefficients(
        sequence.power_base, annihilator_order
    )
    residual = _closed_form_recurrence_residual(
        sequence, annihilator_coefficients
    )
    if any(residual):
        raise FalseTwinCertificateError(
            f"{sequence.name} symbolic annihilator check failed"
        )
    return {
        "expression": _closed_form_expression(sequence),
        "power_base": sequence.power_base,
        "denominator": sequence.denominator,
        "polynomial_coefficient_order": "ascending_in_t",
        "polynomial_coefficients": list(
            sequence.polynomial_coefficients
        ),
        "polynomial_degree": len(sequence.polynomial_coefficients) - 1,
        "annihilator": (
            f"(E-{sequence.power_base})^{annihilator_order}"
        ),
        "annihilator_coefficients": list(annihilator_coefficients),
        "symbolic_recurrence_residual_coefficients": list(residual),
        "integrality": _integrality_certificate(sequence),
    }


def _margin_derivation_payload(
    sequences: Sequence[ExponentialPolynomial],
    margin_sequence: ExponentialPolynomial,
) -> dict[str, object]:
    sequence_by_name = {
        sequence.name: sequence for sequence in sequences
    }
    total = sequence_by_name["forest_count"]
    edge_e = sequence_by_name["forest_count_e"]
    edge_f = sequence_by_name["forest_count_f"]
    pair = sequence_by_name["forest_count_ef"]
    right_denominator = edge_e.denominator * edge_f.denominator
    left_denominator = total.denominator * pair.denominator
    if right_denominator != left_denominator:
        raise FalseTwinCertificateError(
            "count products do not share an exact denominator"
        )
    right_polynomial = _multiply_polynomials(
        edge_e.polynomial_coefficients,
        edge_f.polynomial_coefficients,
    )
    left_polynomial = _multiply_polynomials(
        total.polynomial_coefficients,
        pair.polynomial_coefficients,
    )
    difference = tuple(
        right - left
        for right, left in zip(right_polynomial, left_polynomial)
    )
    if right_denominator % margin_sequence.denominator:
        raise FalseTwinCertificateError(
            "margin denominator does not divide the product denominator"
        )
    multiplier = (
        right_denominator // margin_sequence.denominator
    )
    expected = tuple(
        multiplier * coefficient
        for coefficient in margin_sequence.polynomial_coefficients
    )
    if _trim_polynomial(difference) != _trim_polynomial(expected):
        raise FalseTwinCertificateError(
            "closed count formulae do not derive the claimed margin"
        )
    if any(
        coefficient <= 0
        for coefficient in margin_sequence.polynomial_coefficients
    ):
        raise FalseTwinCertificateError(
            "margin polynomial lacks a positive-coefficient proof"
        )
    return {
        **_closed_form_payload(margin_sequence),
        "identity": "forest_count_e*forest_count_f-forest_count*forest_count_ef",
        "common_count_product_denominator": right_denominator,
        "scaled_product_difference_coefficients": list(difference),
        "margin_polynomial_scale_in_common_denominator": multiplier,
        "all_polynomial_coefficients_strictly_positive": True,
        "positivity_domain": "integer t >= 0",
        "positivity_proof": (
            "36^t and the denominator are positive, while every polynomial "
            "coefficient is positive and every t^k is nonnegative"
        ),
    }


def _large_t_audit(
    twin_count: int,
    sequences: Sequence[ExponentialPolynomial],
    margin_sequence: ExponentialPolynomial,
) -> dict[str, object]:
    counts = _evaluate_count_closed_forms(sequences, twin_count)
    recurrence_residuals = []
    for sequence in sequences:
        residual = sum(
            coefficient * sequence.evaluate(twin_count + shift)
            for shift, coefficient in enumerate(
                KRYLOV_RECURRENCE_COEFFICIENTS
            )
        )
        recurrence_residuals.append(residual)
    margin = margin_sequence.evaluate(twin_count)
    margin_identity_residual = (
        counts[1] * counts[2] - counts[0] * counts[3] - margin
    )
    denominator_remainders = [
        sequence.numerator(twin_count) % sequence.denominator
        for sequence in (*sequences, margin_sequence)
    ]
    if (
        any(recurrence_residuals)
        or margin_identity_residual
        or any(denominator_remainders)
        or margin <= 0
    ):
        raise FalseTwinCertificateError(
            f"large-t audit failed at t={twin_count}"
        )
    return {
        "t": twin_count,
        "count_recurrence_residuals": recurrence_residuals,
        "margin_identity_residual": margin_identity_residual,
        "denominator_remainders": denominator_remainders,
        "margin_strictly_positive": True,
        "large_values_omitted": True,
    }


def _matching_certified_case(
    base_graph6: str,
    edge_pair: tuple[int, int],
    neighbourhood: tuple[int, ...],
) -> CertifiedFalseTwinCase | None:
    for case in CERTIFIED_FALSE_TWIN_CASES:
        if (
            case.base_graph6 == base_graph6
            and case.edge_pair == edge_pair
            and case.neighbourhood == neighbourhood
        ):
            return case
    return None


def build_krylov_recurrence_certificate(
    base_graph6: str = DEFAULT_FALSE_TWIN_BASE_GRAPH6,
    edge_pair: Sequence[int] = DEFAULT_FALSE_TWIN_EDGE_PAIR,
    neighbourhood: Iterable[int] = DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
) -> dict[str, object]:
    """Build a deterministic, exact certificate for the false-twin family.

    The certificate is emitted only after checking the vector identity on
    every base partition and all four forced-edge channels, symbolic closed
    form recurrences, denominator divisibility, direct transfer samples
    through ``t=100``, the margin identity, and a large-``t`` audit.
    """

    graph = decode_graph6(base_graph6)
    pair = _validated_edge_pair(len(graph.edges), edge_pair)
    neighbours = _validated_neighbourhood(
        graph.vertex_count, neighbourhood
    )
    distribution = _combine_forced_distributions(graph, pair)
    transition_cache: dict[Partition, TwinTransition] = {}
    krylov_vectors: list[dict[Partition, CountVector]] = []
    sample_evidence = []
    sample_set = frozenset(CERTIFICATE_TRANSFER_SAMPLES)
    maximum_sample = max(CERTIFICATE_TRANSFER_SAMPLES)

    for twin_count in range(maximum_sample + 1):
        if twin_count <= KRYLOV_ORDER:
            krylov_vectors.append(distribution)
        if twin_count in sample_set:
            transfer_counts = _distribution_totals(distribution)
            transfer_margin = (
                transfer_counts[1] * transfer_counts[2]
                - transfer_counts[0] * transfer_counts[3]
            )
            sample_evidence.append(
                {
                    "t": twin_count,
                    "counts": list(transfer_counts),
                    "margin": transfer_margin,
                    "active_partitions": len(distribution),
                    "distribution_sha256": (
                        _distribution_digest(distribution)
                    ),
                }
            )
        if twin_count < maximum_sample:
            distribution = _advance_false_twin_distribution(
                distribution, neighbours, transition_cache
            )

    if len(krylov_vectors) != KRYLOV_ORDER + 1:
        raise FalseTwinCertificateError("incomplete Krylov vector sequence")
    partition_universe = tuple(
        sorted(
            set().union(
                *(set(vector) for vector in krylov_vectors)
            )
        )
    )
    residual_rows = []
    nonzero_coordinates = []
    zero_vector = (0, 0, 0, 0)
    for partition in partition_universe:
        residual = []
        for channel in range(4):
            value = sum(
                coefficient
                * krylov_vectors[shift].get(
                    partition, zero_vector
                )[channel]
                for shift, coefficient in enumerate(
                    KRYLOV_RECURRENCE_COEFFICIENTS
                )
            )
            residual.append(value)
            if value:
                nonzero_coordinates.append(
                    (partition, channel, value)
                )
        residual_rows.append([list(partition), residual])
    if nonzero_coordinates:
        partition, channel, value = nonzero_coordinates[0]
        raise FalseTwinCertificateError(
            "Krylov residual is nonzero at "
            f"{partition}, channel {channel}: {value}"
        )

    count_sequences = _derive_count_closed_forms(krylov_vectors)
    margin_sequence = _derive_margin_closed_form(count_sequences)
    registered_case = _matching_certified_case(
        graph.encoding, pair, neighbours
    )
    if (
        registered_case is not None
        and registered_case.expected_counts is not None
        and count_sequences != registered_case.expected_counts
    ):
        raise FalseTwinCertificateError(
            f"{registered_case.case_id} count formula regression failed"
        )
    if (
        registered_case is not None
        and margin_sequence != registered_case.expected_margin
    ):
        raise FalseTwinCertificateError(
            f"{registered_case.case_id} margin formula regression failed"
        )
    sample_records = []
    for evidence in sample_evidence:
        twin_count = evidence["t"]
        transfer_counts = tuple(evidence["counts"])
        formula_counts = _evaluate_count_closed_forms(
            count_sequences, twin_count
        )
        formula_margin = margin_sequence.evaluate(twin_count)
        if transfer_counts != formula_counts:
            raise FalseTwinCertificateError(
                f"closed counts fail direct transfer at t={twin_count}"
            )
        if evidence["margin"] != formula_margin:
            raise FalseTwinCertificateError(
                f"closed margin fails direct transfer at t={twin_count}"
            )
        sample_records.append(
            {**evidence, "closed_forms_match": True}
        )

    outgoing_multiplicities = [
        sum(multiplicity for _, multiplicity in transitions)
        for transitions in transition_cache.values()
    ]
    if not outgoing_multiplicities:
        raise FalseTwinCertificateError("empty transfer operator")
    closed_forms = {
        sequence.name: _closed_form_payload(sequence)
        for sequence in count_sequences
    }
    margin_payload = _margin_derivation_payload(
        count_sequences, margin_sequence
    )
    large_t_audit = _large_t_audit(
        CERTIFICATE_LARGE_T, count_sequences, margin_sequence
    )

    return {
        "schema": "amra.opg1757.false-twin-krylov-certificate.v1",
        "status": "certified",
        "method": (
            "exact-forward-base-partition-dp-and-forgotten-false-twin-"
            "transfer"
        ),
        "instance": {
            "registered_case_id": (
                registered_case.case_id
                if registered_case is not None
                else None
            ),
            "base_graph6": graph.encoding,
            "base_vertex_count": graph.vertex_count,
            "base_edge_count": len(graph.edges),
            "edge_pair": list(pair),
            "edge_pair_endpoints": [
                list(graph.edges[pair[0]]),
                list(graph.edges[pair[1]]),
            ],
            "neighbourhood": list(neighbours),
        },
        "transfer_operator": {
            "persistent_state": "partition of base vertices only",
            "partition_count": len(transition_cache),
            "arc_count": sum(
                len(transitions)
                for transitions in transition_cache.values()
            ),
            "minimum_outgoing_subset_multiplicity": min(
                outgoing_multiplicities
            ),
            "maximum_outgoing_subset_multiplicity": max(
                outgoing_multiplicities
            ),
            "sha256": _transition_digest(transition_cache),
            "digest_encoding": (
                "canonical compact JSON of sorted source partitions, "
                "targets, and integer multiplicities"
            ),
        },
        "krylov_recurrence": {
            "operator_polynomial": "(E-6)^5",
            "coefficient_convention": (
                "sum(coefficients[j]*v_(t+j), j=0..5)=0"
            ),
            "coefficients": list(
                KRYLOV_RECURRENCE_COEFFICIENTS
            ),
            "verified_at_t": 0,
            "partition_count": len(partition_universe),
            "channel_names": list(COUNT_CHANNEL_NAMES),
            "coordinate_count": len(partition_universe) * 4,
            "nonzero_residual_coordinates": 0,
            "partition_universe_sha256": _sha256_json(
                [list(partition) for partition in partition_universe]
            ),
            "residual_vector_sha256": _sha256_json(residual_rows),
            "vectors": [
                {
                    "t": twin_count,
                    "active_partitions": len(vector),
                    "totals": list(_distribution_totals(vector)),
                    "sha256": _distribution_digest(vector),
                }
                for twin_count, vector in enumerate(krylov_vectors)
            ],
            "all_t_proof": (
                "the transfer is a fixed linear operator T; applying T^t "
                "to (T-6I)^5 v0=0 proves the same recurrence for every "
                "integer t>=0 and for every linear count projection"
            ),
        },
        "closed_forms": closed_forms,
        "closed_form_verification": {
            "initial_match_t": [0, 1, 2, 3, 4],
            "direct_transfer_samples": sample_records,
            "large_t_audit": large_t_audit,
            "uniqueness_proof": (
                "each closed form satisfies the order-5 recurrence and "
                "matches its first five exact transfer values"
            ),
        },
        "margin": margin_payload,
        "conclusion": {
            "claim": (
                "for the recorded inherited edge pair only: "
                "forest_count*forest_count_ef < "
                "forest_count_e*forest_count_f"
            ),
            "holds_for_every_nonnegative_integer_t": True,
            "strict_for_every_nonnegative_integer_t": True,
            "selected_inherited_edge_pair_is_never_a_counterexample": True,
            "all_edge_pairs_checked": False,
            "whole_graph_family_counterexample_exhaustion_claimed": False,
        },
    }


def verify_krylov_recurrence_certificate(
    payload: object,
) -> None:
    """Recompute and strictly compare an exact certificate.

    Unknown, missing, mistyped, or changed fields are rejected.  Comparison
    uses canonical JSON so that JSON booleans cannot masquerade as integers.
    """

    if not isinstance(payload, dict):
        raise FalseTwinCertificateError(
            "certificate payload must be a JSON object"
        )
    if (
        payload.get("schema")
        != "amra.opg1757.false-twin-krylov-certificate.v1"
        or payload.get("status") != "certified"
    ):
        raise FalseTwinCertificateError(
            "certificate schema or status is not certified"
        )
    instance = payload.get("instance")
    if not isinstance(instance, dict):
        raise FalseTwinCertificateError("certificate instance is missing")
    base_graph6 = instance.get("base_graph6")
    edge_pair = instance.get("edge_pair")
    neighbourhood = instance.get("neighbourhood")
    if (
        not isinstance(base_graph6, str)
        or not isinstance(edge_pair, list)
        or not isinstance(neighbourhood, list)
    ):
        raise FalseTwinCertificateError(
            "certificate instance has invalid field types"
        )
    try:
        expected = build_krylov_recurrence_certificate(
            base_graph6, edge_pair, neighbourhood
        )
        supplied_bytes = _canonical_json_bytes(payload)
        expected_bytes = _canonical_json_bytes(expected)
    except FalseTwinCertificateError:
        raise
    except (TypeError, ValueError, OverflowError) as error:
        raise FalseTwinCertificateError(
            f"certificate recomputation failed: {error}"
        ) from error
    if supplied_bytes != expected_bytes:
        raise FalseTwinCertificateError(
            "certificate does not exactly match recomputed evidence"
        )


def build_krylov_certificate_collection() -> dict[str, object]:
    """Build the three registered positive-margin family certificates."""

    cases = [
        {
            "case_id": case.case_id,
            "certificate": build_krylov_recurrence_certificate(
                case.base_graph6,
                case.edge_pair,
                case.neighbourhood,
            ),
        }
        for case in CERTIFIED_FALSE_TWIN_CASES
    ]
    return {
        "schema": (
            "amra.opg1757.false-twin-krylov-certificate-collection.v1"
        ),
        "status": "certified",
        "case_count": len(cases),
        "cases": cases,
        "conclusion": {
            "all_registered_selected_pairs_have_positive_margin_for_all_t": (
                True
            ),
            "claim_scope": (
                "the one recorded inherited edge pair in each registered "
                "false-twin family"
            ),
            "all_edge_pairs_checked": False,
            "whole_graph_family_counterexample_exhaustion_claimed": False,
        },
    }


def verify_krylov_certificate_collection(payload: object) -> None:
    if not isinstance(payload, dict):
        raise FalseTwinCertificateError(
            "certificate collection must be a JSON object"
        )
    if (
        payload.get("schema")
        != "amra.opg1757.false-twin-krylov-certificate-collection.v1"
        or payload.get("status") != "certified"
    ):
        raise FalseTwinCertificateError(
            "certificate collection schema or status is not certified"
        )
    try:
        expected = build_krylov_certificate_collection()
        supplied_bytes = _canonical_json_bytes(payload)
        expected_bytes = _canonical_json_bytes(expected)
    except FalseTwinCertificateError:
        raise
    except (TypeError, ValueError, OverflowError) as error:
        raise FalseTwinCertificateError(
            f"certificate collection recomputation failed: {error}"
        ) from error
    if supplied_bytes != expected_bytes:
        raise FalseTwinCertificateError(
            "certificate collection does not exactly match recomputed evidence"
        )


def _atomic_write_json(path: Path | str, payload: object) -> None:
    output = Path(path)
    parent = output.parent
    parent.mkdir(parents=True, exist_ok=True)
    serialized = (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        dir=parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, output)
        directory_descriptor = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_krylov_recurrence_certificate(
    path: Path | str,
    payload: object,
) -> None:
    """Verify, then atomically replace ``path`` with canonical JSON."""

    verify_krylov_recurrence_certificate(payload)
    _atomic_write_json(path, payload)


def write_krylov_certificate_collection(
    path: Path | str,
    payload: object,
) -> None:
    """Verify, then atomically replace ``path`` with a collection."""

    verify_krylov_certificate_collection(payload)
    _atomic_write_json(path, payload)


def load_and_verify_krylov_recurrence_certificate(
    path: Path | str,
) -> dict[str, object]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FalseTwinCertificateError(
            f"cannot load certificate: {error}"
        ) from error
    verify_krylov_recurrence_certificate(payload)
    return payload


def load_and_verify_krylov_certificate(
    path: Path | str,
) -> dict[str, object]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FalseTwinCertificateError(
            f"cannot load certificate: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise FalseTwinCertificateError(
            "certificate payload must be a JSON object"
        )
    if (
        payload.get("schema")
        == "amra.opg1757.false-twin-krylov-certificate-collection.v1"
    ):
        verify_krylov_certificate_collection(payload)
    else:
        verify_krylov_recurrence_certificate(payload)
    return payload


def _certificate_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build or verify an exact false-twin Krylov certificate."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    certify = commands.add_parser(
        "certify",
        help="build, verify, and atomically write a certificate",
    )
    certify.add_argument("--output", type=Path, required=True)
    certify.add_argument(
        "--base-graph6", default=DEFAULT_FALSE_TWIN_BASE_GRAPH6
    )
    certify.add_argument(
        "--edge-pair",
        type=int,
        nargs=2,
        default=DEFAULT_FALSE_TWIN_EDGE_PAIR,
        metavar=("E", "F"),
    )
    certify.add_argument(
        "--neighbourhood",
        type=int,
        nargs="+",
        default=DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
        metavar="VERTEX",
    )
    certify_collection = commands.add_parser(
        "certify-collection",
        help="build, verify, and atomically write all registered cases",
    )
    certify_collection.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser(
        "verify",
        help="recompute and verify an existing certificate",
    )
    verify.add_argument("certificate", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _certificate_argument_parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "certify":
            payload = build_krylov_recurrence_certificate(
                arguments.base_graph6,
                arguments.edge_pair,
                arguments.neighbourhood,
            )
            write_krylov_recurrence_certificate(
                arguments.output, payload
            )
            summary = {
                "status": "certified",
                "output": str(arguments.output),
                "partition_count": payload["krylov_recurrence"][
                    "partition_count"
                ],
                "coordinate_count": payload["krylov_recurrence"][
                    "coordinate_count"
                ],
            }
        elif arguments.command == "certify-collection":
            payload = build_krylov_certificate_collection()
            write_krylov_certificate_collection(
                arguments.output, payload
            )
            summary = {
                "status": "certified",
                "output": str(arguments.output),
                "case_count": payload["case_count"],
            }
        else:
            payload = load_and_verify_krylov_certificate(
                arguments.certificate
            )
            if "case_count" in payload:
                summary = {
                    "status": "verified",
                    "certificate": str(arguments.certificate),
                    "case_count": payload["case_count"],
                }
            else:
                summary = {
                    "status": "verified",
                    "certificate": str(arguments.certificate),
                    "partition_count": payload["krylov_recurrence"][
                        "partition_count"
                    ],
                    "coordinate_count": payload["krylov_recurrence"][
                        "coordinate_count"
                    ],
                }
    except FalseTwinCertificateError as error:
        parser.error(str(error))
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
