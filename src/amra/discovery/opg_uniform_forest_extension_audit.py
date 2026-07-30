"""Independent, fail-closed audit of the frozen OPG-1757 n=12 beam.

The production extension search counts forests by a deletion-contraction
recurrence.  This auditor does not import that search or its counter.  It
instead aggregates base-graph forests by their final vertex partition.  For a
fixed neighbour set ``S`` of the new vertex, a base forest with component
blocks ``B`` has exactly

    product(1 + |B intersect S|)

acyclic completions by star edges.  The same identity, with one or two star
edges forced, recovers every edge and edge-pair count of an extension.

The frozen beam artifact is screened over all 1,012 labelled neighbour sets.
Seven separately persisted all-pair analyses are then replayed over all 3,861
of their edge pairs.  Runtime-only ``states`` and ``elapsed_seconds`` fields
are type checked but are not expected to agree with the independent dynamic
program.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cmp_to_key
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy


AUDIT_SCHEMA = "amra.opg1757.n12-labelled-extension.audit.v1"
BEAM_SCHEMA = "amra.opg1757.labelled-extension.v1"
SEED_GRAPH6 = "J?`bM~^PyN?"
SEED_ORDER = 11
EXTENSION_ORDER = 12
INHERITED_EDGE_INDEXES = (0, 2)
MINIMUM_NEIGHBOURS = 2
MAXIMUM_NEIGHBOURS = 5
EXPECTED_LABELLED_EXTENSIONS = 1_012
EXPECTED_TOP_K = 30
EXPECTED_BEAM_SHA256 = (
    "3f37c2dc79d2b642955c3639d41fbfc7ff9e6174518101778759381c68513e7a"
)

DISCOVERY_DIRECTORY = Path(__file__).resolve().parent
EXPECTED_SOURCE_SHA256 = {
    "artifact_producer": (
        DISCOVERY_DIRECTORY / "opg_uniform_forest_extensions.py",
        "57d97df6af87589bb4304fb26dd2ee1ad68f9305f01433deed8de92ea3b49e35",
    ),
    "forest_counting_dependency": (
        DISCOVERY_DIRECTORY / "opg_uniform_forest_search.py",
        "878bbdc1ea971567e7208c8516a520fbe42a21a36a43151d5fdb337bee6aa001",
    ),
    "graph6_dependency": (
        DISCOVERY_DIRECTORY / "opg_coloring_search.py",
        "3366e14bb9dde8c5f519b96c011377140ad49f5672aab421fcd3938bf9f9619c",
    ),
    "all_pair_analysis_producer": (
        DISCOVERY_DIRECTORY / "opg_uniform_forest_analysis.py",
        "7cb875148a867725fce80fb9eed06be6b23c274ec15938aef6f92a7171e381fd",
    ),
}


@dataclass(frozen=True)
class _FrozenAnalysis:
    filename: str
    label_index: int
    sha256: str


FROZEN_ANALYSES = (
    _FrozenAnalysis(
        "top-closest-all-pairs.json",
        1006,
        "c68dd63b07653a3bcc8b960cdf35d9bdaed7bacbe2305c51d4b81ea3190b0385",
    ),
    _FrozenAnalysis(
        "top-871-all-pairs.json",
        871,
        "7d1f470f8060fa97e7a19530c36a84a8fbfd7c70177c962563f3deae5ec0cee7",
    ),
    _FrozenAnalysis(
        "top-976-all-pairs.json",
        976,
        "a39ad40f1fb08015a7b956d8a44ef44a7f706a6f20eb121fe28bb2a48dc084e4",
    ),
    _FrozenAnalysis(
        "top-535-all-pairs.json",
        535,
        "e108252b06bf49cc523e04d9cd6f6e98faeb0c87533bdcecdfc5e44318337dd0",
    ),
    _FrozenAnalysis(
        "top-699-all-pairs.json",
        699,
        "a401145dcd3a4ea3375738134d7fc5da350e47bc9670110d7621e7a3f4df06f6",
    ),
    _FrozenAnalysis(
        "top-314-all-pairs.json",
        314,
        "824c5d28888a1fb5cd8569d86c3054d2fe962af514ac5c4575bc281c9782b2ab",
    ),
    _FrozenAnalysis(
        "top-1008-all-pairs.json",
        1008,
        "60d646cc868a67d166365212f6e870f95dc14205af251392c46c1d0dca0e64fa",
    ),
)


class ExtensionAuditError(ValueError):
    """Raised when any frozen input or independently replayed fact disagrees."""


@dataclass(frozen=True)
class _Graph:
    vertex_count: int
    edges: tuple[tuple[int, int], ...]
    graph6: str


@dataclass(frozen=True)
class _Extension:
    label_index: int
    neighbours: tuple[int, ...]
    graph: _Graph


@dataclass(frozen=True)
class _InheritedReplay:
    extension: _Extension
    forest_count: int
    forest_count_e: int
    forest_count_f: int
    forest_count_ef: int

    @property
    def left_product(self) -> int:
        return self.forest_count * self.forest_count_ef

    @property
    def right_product(self) -> int:
        return self.forest_count_e * self.forest_count_f

    @property
    def margin(self) -> int:
        return self.right_product - self.left_product

    @property
    def ratio(self) -> Fraction:
        return Fraction(self.left_product, self.right_product)


@dataclass(frozen=True)
class _AllPairReplay:
    extension: _Extension
    forest_count: int
    edge_forest_counts: tuple[int, ...]
    pair_forest_counts: tuple[tuple[int, ...], ...]


Partition = tuple[int, ...]
PartitionDistribution = dict[Partition, int]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ExtensionAuditError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_frozen_json(path: Path, expected_sha256: str) -> Mapping[str, object]:
    if path.is_symlink() or not path.is_file():
        raise ExtensionAuditError(f"frozen artifact is missing or redirected: {path}")
    actual_sha256 = _file_sha256(path)
    if actual_sha256 != expected_sha256:
        raise ExtensionAuditError(
            f"frozen artifact SHA-256 mismatch for {path.name}: "
            f"{actual_sha256}"
        )
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ExtensionAuditError(f"cannot read strict JSON from {path}") from error
    if not isinstance(payload, Mapping):
        raise ExtensionAuditError(f"artifact is not a JSON object: {path}")
    return payload


def _verify_source_hashes() -> dict[str, str]:
    actual: dict[str, str] = {}
    for role, (path, expected_sha256) in EXPECTED_SOURCE_SHA256.items():
        if path.is_symlink() or not path.is_file():
            raise ExtensionAuditError(
                f"frozen source is missing or redirected for {role}: {path}"
            )
        digest = _file_sha256(path)
        if digest != expected_sha256:
            raise ExtensionAuditError(
                f"frozen source SHA-256 mismatch for {role}: {digest}"
            )
        actual[role] = digest
    return actual


def _require_exact(actual: object, expected: object, field: str) -> None:
    if type(actual) is not type(expected):
        raise ExtensionAuditError(
            f"{field} has type {type(actual).__name__}, "
            f"expected {type(expected).__name__}"
        )
    if isinstance(expected, dict):
        assert isinstance(actual, dict)
        if set(actual) != set(expected):
            raise ExtensionAuditError(f"{field} has an unexpected key set")
        for key in expected:
            _require_exact(actual[key], expected[key], f"{field}.{key}")
        return
    if isinstance(expected, list):
        assert isinstance(actual, list)
        if len(actual) != len(expected):
            raise ExtensionAuditError(f"{field} has an unexpected length")
        for index, (actual_item, expected_item) in enumerate(
            zip(actual, expected)
        ):
            _require_exact(
                actual_item,
                expected_item,
                f"{field}[{index}]",
            )
        return
    if actual != expected:
        raise ExtensionAuditError(
            f"{field} is {actual!r}, expected {expected!r}"
        )


def _require_positive_runtime_fields(
    record: Mapping[str, object],
    field: str,
) -> None:
    states = record.get("states")
    if type(states) is not int or states <= 0:
        raise ExtensionAuditError(f"{field}.states must be a positive integer")
    elapsed = record.get("elapsed_seconds")
    if (
        isinstance(elapsed, bool)
        or not isinstance(elapsed, (int, float))
        or not math.isfinite(float(elapsed))
        or float(elapsed) <= 0
    ):
        raise ExtensionAuditError(
            f"{field}.elapsed_seconds must be positive and finite"
        )


def _decode_compact_graph6(graph6: str) -> _Graph:
    """Decode compact graph6 locally, including exact length and zero padding."""

    if not isinstance(graph6, str) or not graph6:
        raise ExtensionAuditError("graph6 must be a nonempty string")
    try:
        values = [ord(character) - 63 for character in graph6]
    except TypeError as error:
        raise ExtensionAuditError("graph6 must contain characters") from error
    if any(not 0 <= value <= 63 for value in values):
        raise ExtensionAuditError("graph6 contains an out-of-range character")
    vertex_count = values[0]
    if vertex_count > 62:
        raise ExtensionAuditError("only compact graph6 order <= 62 is accepted")
    edge_bit_count = vertex_count * (vertex_count - 1) // 2
    expected_length = 1 + (edge_bit_count + 5) // 6
    if len(values) != expected_length:
        raise ExtensionAuditError("graph6 has a noncanonical payload length")
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    if any(bits[edge_bit_count:]):
        raise ExtensionAuditError("graph6 has nonzero padding bits")
    edges: list[tuple[int, int]] = []
    position = 0
    for right in range(1, vertex_count):
        for left in range(right):
            if bits[position]:
                edges.append((left, right))
            position += 1
    return _Graph(vertex_count, tuple(edges), graph6)


def _encode_compact_graph6(
    vertex_count: int,
    edges: Iterable[tuple[int, int]],
) -> str:
    normalized = tuple(edges)
    if (
        type(vertex_count) is not int
        or not 0 <= vertex_count <= 62
        or len(set(normalized)) != len(normalized)
        or any(
            type(left) is not int
            or type(right) is not int
            or not 0 <= left < right < vertex_count
            for left, right in normalized
        )
    ):
        raise ExtensionAuditError("cannot encode a non-simple compact graph6")
    edge_set = set(normalized)
    bits = [
        int((left, right) in edge_set)
        for right in range(1, vertex_count)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(vertex_count + 63) + "".join(payload)


def _enumerate_extensions(seed: _Graph) -> tuple[_Extension, ...]:
    if seed.vertex_count != SEED_ORDER:
        raise ExtensionAuditError("the frozen seed does not have order eleven")
    extensions: list[_Extension] = []
    label_index = 0
    for size in range(MINIMUM_NEIGHBOURS, MAXIMUM_NEIGHBOURS + 1):
        for neighbours in combinations(range(seed.vertex_count), size):
            edges = seed.edges + tuple(
                (vertex, seed.vertex_count) for vertex in neighbours
            )
            encoding = _encode_compact_graph6(seed.vertex_count + 1, edges)
            replay = _decode_compact_graph6(encoding)
            if replay.edges != edges:
                raise ExtensionAuditError(
                    "local graph6 extension round trip changed edge order"
                )
            extensions.append(
                _Extension(label_index, neighbours, replay)
            )
            label_index += 1
    if (
        label_index != EXPECTED_LABELLED_EXTENSIONS
        or len({item.graph.graph6 for item in extensions})
        != EXPECTED_LABELLED_EXTENSIONS
    ):
        raise ExtensionAuditError("the deterministic label enumeration is open")
    return tuple(extensions)


def _merge_partition(
    partition: Partition,
    left: int,
    right: int,
) -> Partition | None:
    left_bit = 1 << left
    right_bit = 1 << right
    left_index = -1
    right_index = -1
    for index, block in enumerate(partition):
        if block & left_bit:
            left_index = index
        if block & right_bit:
            right_index = index
    if left_index < 0 or right_index < 0:
        raise ExtensionAuditError("partition lost a vertex")
    if left_index == right_index:
        return None
    if left_index > right_index:
        left_index, right_index = right_index, left_index
    blocks = list(partition)
    merged = blocks[left_index] | blocks[right_index]
    blocks.pop(right_index)
    blocks.pop(left_index)
    blocks.append(merged)
    blocks.sort()
    return tuple(blocks)


def _partition_distribution(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    required_edge_indexes: tuple[int, ...] = (),
) -> PartitionDistribution:
    """Aggregate forests by final component partition using a forward DP."""

    if (
        len(set(required_edge_indexes)) != len(required_edge_indexes)
        or any(
            type(index) is not int or not 0 <= index < len(edges)
            for index in required_edge_indexes
        )
    ):
        raise ExtensionAuditError("invalid required edge set")
    partition: Partition = tuple(1 << vertex for vertex in range(vertex_count))
    for edge_index in required_edge_indexes:
        merged = _merge_partition(partition, *edges[edge_index])
        if merged is None:
            return {}
        partition = merged

    distribution: PartitionDistribution = {partition: 1}
    required = set(required_edge_indexes)
    for edge_index, edge in enumerate(edges):
        if edge_index in required:
            continue
        updated = dict(distribution)
        for state, multiplicity in distribution.items():
            merged = _merge_partition(state, *edge)
            if merged is not None:
                updated[merged] = updated.get(merged, 0) + multiplicity
        distribution = updated
    return distribution


class _BasePartitionReplay:
    """Vectorized star weights over one independently generated base DP."""

    def __init__(self, seed: _Graph) -> None:
        self.seed = seed
        self.total_distribution = _partition_distribution(
            seed.vertex_count,
            seed.edges,
        )
        self.partitions = tuple(self.total_distribution)
        self.partition_indexes = {
            partition: index
            for index, partition in enumerate(self.partitions)
        }
        self.total_coefficients = numpy.fromiter(
            self.total_distribution.values(),
            dtype=numpy.int64,
            count=len(self.total_distribution),
        )
        labels = numpy.empty(
            (len(self.partitions), seed.vertex_count),
            dtype=numpy.uint8,
        )
        for row, partition in enumerate(self.partitions):
            for component, block in enumerate(partition):
                for vertex in range(seed.vertex_count):
                    if block & (1 << vertex):
                        labels[row, vertex] = component
        self.labels = labels

    def aligned_coefficients(
        self,
        distribution: Mapping[Partition, int],
    ) -> numpy.ndarray:
        coefficients = numpy.zeros(
            len(self.partitions),
            dtype=numpy.int64,
        )
        for partition, multiplicity in distribution.items():
            try:
                index = self.partition_indexes[partition]
            except KeyError as error:
                raise ExtensionAuditError(
                    "conditional DP produced a partition absent from total DP"
                ) from error
            coefficients[index] = multiplicity
        return coefficients

    def sparse_dot(
        self,
        distribution: Mapping[Partition, int],
        weights: numpy.ndarray,
    ) -> numpy.ndarray:
        if weights.ndim == 1:
            matrix = weights.reshape(1, -1)
        elif weights.ndim == 2:
            matrix = weights
        else:
            raise ExtensionAuditError("star-weight array has invalid rank")
        if matrix.shape[1] != len(self.partitions):
            raise ExtensionAuditError("star-weight array has invalid width")
        try:
            indexes = numpy.fromiter(
                (
                    self.partition_indexes[partition]
                    for partition in distribution
                ),
                dtype=numpy.int64,
                count=len(distribution),
            )
        except KeyError as error:
            raise ExtensionAuditError(
                "conditional DP produced a partition absent from total DP"
            ) from error
        coefficients = numpy.fromiter(
            distribution.values(),
            dtype=numpy.int64,
            count=len(distribution),
        )
        return matrix[:, indexes] @ coefficients

    def star_weights(
        self,
        neighbours: tuple[int, ...],
        forced: tuple[int, ...] = (),
    ) -> numpy.ndarray:
        """Count acyclic star completions, optionally forcing star edges."""

        if (
            len(set(neighbours)) != len(neighbours)
            or tuple(sorted(neighbours)) != neighbours
            or not MINIMUM_NEIGHBOURS <= len(neighbours) <= MAXIMUM_NEIGHBOURS
            or any(not 0 <= vertex < self.seed.vertex_count for vertex in neighbours)
            or len(set(forced)) != len(forced)
            or any(vertex not in neighbours for vertex in forced)
            or len(forced) > 2
        ):
            raise ExtensionAuditError("invalid star-neighbour or forced set")
        selected = self.labels[:, list(neighbours)]
        forced_positions = [neighbours.index(vertex) for vertex in forced]
        valid = numpy.ones(len(self.partitions), dtype=numpy.bool_)
        if len(forced_positions) == 2:
            valid &= (
                selected[:, forced_positions[0]]
                != selected[:, forced_positions[1]]
            )

        weights = numpy.ones(len(self.partitions), dtype=numpy.int64)
        forced_labels = [
            selected[:, position] for position in forced_positions
        ]
        remaining_positions = [
            position
            for position, vertex in enumerate(neighbours)
            if vertex not in forced
        ]
        for offset, position in enumerate(remaining_positions):
            component = selected[:, position]
            blocked = numpy.zeros(len(self.partitions), dtype=numpy.bool_)
            for forced_label in forced_labels:
                blocked |= component == forced_label
            if offset:
                previous = remaining_positions[:offset]
                first_in_component = numpy.all(
                    selected[:, previous] != component[:, None],
                    axis=1,
                )
            else:
                first_in_component = numpy.ones(
                    len(self.partitions),
                    dtype=numpy.bool_,
                )
            component_size = (
                numpy.count_nonzero(
                    selected[:, remaining_positions] == component[:, None],
                    axis=1,
                )
                + 1
            )
            weights *= numpy.where(
                valid & ~blocked & first_in_component,
                component_size,
                1,
            )
        weights *= valid
        return weights


def _replay_all_inherited_screens(
    seed: _Graph,
    extensions: tuple[_Extension, ...],
    base: _BasePartitionReplay,
) -> tuple[_InheritedReplay, ...]:
    first, second = INHERITED_EDGE_INDEXES
    distributions = (
        base.total_distribution,
        _partition_distribution(seed.vertex_count, seed.edges, (first,)),
        _partition_distribution(seed.vertex_count, seed.edges, (second,)),
        _partition_distribution(
            seed.vertex_count,
            seed.edges,
            (first, second),
        ),
    )
    coefficients = numpy.stack(
        [base.aligned_coefficients(distribution) for distribution in distributions]
    )
    replayed: list[_InheritedReplay] = []
    for extension in extensions:
        weights = base.star_weights(extension.neighbours)
        counts = coefficients @ weights
        replayed.append(
            _InheritedReplay(
                extension,
                *(int(value) for value in counts),
            )
        )
    return tuple(replayed)


def _replay_selected_all_pairs(
    seed: _Graph,
    selected: tuple[_Extension, ...],
    base: _BasePartitionReplay,
) -> tuple[_AllPairReplay, ...]:
    """Replay every pair in selected star extensions from base partitions."""

    total_weights = numpy.stack(
        [base.star_weights(item.neighbours) for item in selected]
    )
    forced_one = [
        tuple(
            base.star_weights(item.neighbours, (vertex,))
            for vertex in item.neighbours
        )
        for item in selected
    ]
    forced_two = [
        {
            pair: base.star_weights(item.neighbours, pair)
            for pair in combinations(item.neighbours, 2)
        }
        for item in selected
    ]

    base_edge_count = len(seed.edges)
    forest_counts = total_weights @ base.total_coefficients
    edge_counts = [
        numpy.zeros(
            base_edge_count + len(item.neighbours),
            dtype=numpy.int64,
        )
        for item in selected
    ]
    pair_counts = [
        numpy.zeros(
            (
                base_edge_count + len(item.neighbours),
                base_edge_count + len(item.neighbours),
            ),
            dtype=numpy.int64,
        )
        for item in selected
    ]

    for selected_index, item in enumerate(selected):
        for star_index, _vertex in enumerate(item.neighbours):
            edge_counts[selected_index][base_edge_count + star_index] = int(
                forced_one[selected_index][star_index]
                @ base.total_coefficients
            )
        for first_star, second_star in combinations(
            range(len(item.neighbours)),
            2,
        ):
            vertices = (
                item.neighbours[first_star],
                item.neighbours[second_star],
            )
            count = int(
                forced_two[selected_index][vertices]
                @ base.total_coefficients
            )
            first_index = base_edge_count + first_star
            second_index = base_edge_count + second_star
            pair_counts[selected_index][first_index, second_index] = count
            pair_counts[selected_index][second_index, first_index] = count

    for edge_index in range(base_edge_count):
        distribution = _partition_distribution(
            seed.vertex_count,
            seed.edges,
            (edge_index,),
        )
        inherited_counts = base.sparse_dot(distribution, total_weights)
        for selected_index, item in enumerate(selected):
            edge_counts[selected_index][edge_index] = int(
                inherited_counts[selected_index]
            )
            for star_index, _vertex in enumerate(item.neighbours):
                count = int(
                    base.sparse_dot(
                        distribution,
                        forced_one[selected_index][star_index],
                    )[0]
                )
                star_edge_index = base_edge_count + star_index
                pair_counts[selected_index][edge_index, star_edge_index] = count
                pair_counts[selected_index][star_edge_index, edge_index] = count

    for first, second in combinations(range(base_edge_count), 2):
        distribution = _partition_distribution(
            seed.vertex_count,
            seed.edges,
            (first, second),
        )
        counts = base.sparse_dot(distribution, total_weights)
        for selected_index, count in enumerate(counts):
            pair_counts[selected_index][first, second] = int(count)
            pair_counts[selected_index][second, first] = int(count)

    results = []
    for selected_index, item in enumerate(selected):
        matrix = pair_counts[selected_index]
        results.append(
            _AllPairReplay(
                item,
                int(forest_counts[selected_index]),
                tuple(int(value) for value in edge_counts[selected_index]),
                tuple(
                    tuple(int(value) for value in row)
                    for row in matrix
                ),
            )
        )
    return tuple(results)


def _compare_inherited(
    left: _InheritedReplay,
    right: _InheritedReplay,
) -> int:
    comparison = (
        left.left_product * right.right_product
        - right.left_product * left.right_product
    )
    if comparison:
        return -1 if comparison > 0 else 1
    if left.extension.label_index < right.extension.label_index:
        return -1
    if left.extension.label_index > right.extension.label_index:
        return 1
    return 0


def _inherited_count_table_sha256(
    replayed: Sequence[_InheritedReplay],
) -> str:
    """Bind every independently replayed four-count record in label order."""

    digest = hashlib.sha256()
    for item in replayed:
        record = {
            "label_index": item.extension.label_index,
            "neighbours": list(item.extension.neighbours),
            "graph6": item.extension.graph.graph6,
            "forest_count": item.forest_count,
            "forest_count_e": item.forest_count_e,
            "forest_count_f": item.forest_count_f,
            "forest_count_ef": item.forest_count_ef,
        }
        digest.update(
            json.dumps(
                record,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("ascii")
        )
        digest.update(b"\n")
    return digest.hexdigest()


def _all_pair_count_table_sha256(replay: _AllPairReplay) -> str:
    """Bind N, every N_e, and every distinct-pair N_ef for one graph."""

    digest = hashlib.sha256()
    digest.update(
        (
            f"{replay.extension.label_index}|"
            f"{replay.extension.graph.graph6}|{replay.forest_count}\n"
        ).encode("ascii")
    )
    for edge_index, count in enumerate(replay.edge_forest_counts):
        digest.update(f"e|{edge_index}|{count}\n".encode("ascii"))
    for first, second in combinations(
        range(len(replay.edge_forest_counts)),
        2,
    ):
        count = replay.pair_forest_counts[first][second]
        digest.update(f"p|{first}|{second}|{count}\n".encode("ascii"))
    return digest.hexdigest()


def _validate_beam(
    payload: Mapping[str, object],
    extensions: tuple[_Extension, ...],
    replayed: tuple[_InheritedReplay, ...],
) -> dict[str, object]:
    expected_keys = {
        "attempted",
        "candidate",
        "elapsed_seconds",
        "evaluated",
        "inherited_edge_indexes",
        "inherited_edges",
        "label_enumeration",
        "next_label_index",
        "pair_screening",
        "pending_inherited_violation",
        "schema",
        "seed_graph6",
        "seed_order",
        "status",
        "timeout_records",
        "timeouts",
        "top_evaluations",
    }
    if set(payload) != expected_keys:
        raise ExtensionAuditError("beam artifact has an unexpected key set")
    seed = _decode_compact_graph6(SEED_GRAPH6)
    exact_header: dict[str, object] = {
        "schema": BEAM_SCHEMA,
        "status": "complete",
        "seed_graph6": SEED_GRAPH6,
        "seed_order": SEED_ORDER,
        "inherited_edge_indexes": list(INHERITED_EDGE_INDEXES),
        "inherited_edges": [
            list(seed.edges[index]) for index in INHERITED_EDGE_INDEXES
        ],
        "attempted": EXPECTED_LABELLED_EXTENSIONS,
        "evaluated": EXPECTED_LABELLED_EXTENSIONS,
        "next_label_index": EXPECTED_LABELLED_EXTENSIONS,
        "timeouts": 0,
        "timeout_records": [],
        "candidate": None,
        "pending_inherited_violation": None,
        "label_enumeration": {
            "kind": "fixed-seed-labelled-one-vertex-extension",
            "extension_vertex": SEED_ORDER,
            "neighbour_subset_size_range": [
                MINIMUM_NEIGHBOURS,
                MAXIMUM_NEIGHBOURS,
            ],
            "expected_labelled_extensions": EXPECTED_LABELLED_EXTENSIONS,
            "label_index_range": [0, EXPECTED_LABELLED_EXTENSIONS - 1],
            "isomorphism_deduplicated": False,
            "possible_isomorphic_duplicate_label_range": [
                0,
                EXPECTED_LABELLED_EXTENSIONS - 1,
            ],
            "nonisomorphic_exhaustion_claimed": False,
        },
        "pair_screening": {
            "screened_before_trigger": "inherited edge pair only",
            "full_pair_trigger": "inherited left_product > right_product",
            "all_pairs_checked_for_nontriggering_extensions": False,
            "counterexample_exhaustion_claimed": False,
        },
    }
    for field, expected in exact_header.items():
        _require_exact(payload.get(field), expected, f"beam.{field}")
    elapsed = payload.get("elapsed_seconds")
    if (
        isinstance(elapsed, bool)
        or not isinstance(elapsed, (int, float))
        or not math.isfinite(float(elapsed))
        or float(elapsed) <= 0
    ):
        raise ExtensionAuditError(
            "beam.elapsed_seconds must be positive and finite"
        )

    top = payload.get("top_evaluations")
    if not isinstance(top, list) or len(top) != EXPECTED_TOP_K:
        raise ExtensionAuditError(
            f"beam must persist exactly {EXPECTED_TOP_K} top evaluations"
        )
    ranked = sorted(replayed, key=cmp_to_key(_compare_inherited))
    expected_top = ranked[:EXPECTED_TOP_K]
    record_keys = {
        "elapsed_seconds",
        "forest_count",
        "forest_count_e",
        "forest_count_ef",
        "forest_count_f",
        "graph6",
        "label_index",
        "left_product",
        "margin",
        "neighbours",
        "ratio_denominator",
        "ratio_numerator",
        "right_product",
        "states",
    }
    for rank, (raw_record, replay) in enumerate(zip(top, expected_top), start=1):
        if not isinstance(raw_record, Mapping) or set(raw_record) != record_keys:
            raise ExtensionAuditError(
                f"beam top rank {rank} has an unexpected key set"
            )
        ratio = replay.ratio
        exact_record: dict[str, object] = {
            "label_index": replay.extension.label_index,
            "neighbours": list(replay.extension.neighbours),
            "graph6": replay.extension.graph.graph6,
            "forest_count": replay.forest_count,
            "forest_count_e": replay.forest_count_e,
            "forest_count_f": replay.forest_count_f,
            "forest_count_ef": replay.forest_count_ef,
            "left_product": replay.left_product,
            "right_product": replay.right_product,
            "margin": replay.margin,
            "ratio_numerator": ratio.numerator,
            "ratio_denominator": ratio.denominator,
        }
        for field, expected in exact_record.items():
            _require_exact(
                raw_record.get(field),
                expected,
                f"beam.top_evaluations[{rank - 1}].{field}",
            )
        _require_positive_runtime_fields(
            raw_record,
            f"beam.top_evaluations[{rank - 1}]",
        )

    if len(extensions) != len(replayed):
        raise ExtensionAuditError("inherited replay lost a labelled extension")
    strict = sum(item.margin > 0 for item in replayed)
    equal = sum(item.margin == 0 for item in replayed)
    violations = sum(item.margin < 0 for item in replayed)
    closest = ranked[0]
    return {
        "enumerated": len(extensions),
        "evaluated": len(replayed),
        "neighbour_size_histogram": {
            str(size): sum(
                len(item.neighbours) == size for item in extensions
            )
            for size in range(MINIMUM_NEIGHBOURS, MAXIMUM_NEIGHBOURS + 1)
        },
        "base_partition_states": None,
        "strict_inherited_pair_count": strict,
        "equality_inherited_pair_count": equal,
        "violation_inherited_pair_count": violations,
        "top_k_records_verified": EXPECTED_TOP_K,
        "exact_four_count_table_sha256": _inherited_count_table_sha256(
            replayed
        ),
        "closest_label_index": closest.extension.label_index,
        "closest_margin": closest.margin,
        "closest_ratio": {
            "numerator": closest.ratio.numerator,
            "denominator": closest.ratio.denominator,
        },
    }


def _edge_block_labels(graph: _Graph) -> tuple[int, ...]:
    """Independent Tarjan replay of the graphic-matroid edge blocks."""

    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(graph.vertex_count)
    ]
    for edge_index, (left, right) in enumerate(graph.edges):
        adjacency[left].append((right, edge_index))
        adjacency[right].append((left, edge_index))
    discovered = [-1] * graph.vertex_count
    low = [0] * graph.vertex_count
    stack: list[int] = []
    blocks: list[list[int]] = []
    clock = 0

    def visit(vertex: int, parent_edge: int) -> None:
        nonlocal clock
        discovered[vertex] = low[vertex] = clock
        clock += 1
        for other, edge_index in adjacency[vertex]:
            if edge_index == parent_edge:
                continue
            if discovered[other] < 0:
                stack.append(edge_index)
                visit(other, edge_index)
                low[vertex] = min(low[vertex], low[other])
                if low[other] >= discovered[vertex]:
                    block: list[int] = []
                    while stack:
                        popped = stack.pop()
                        block.append(popped)
                        if popped == edge_index:
                            break
                    blocks.append(block)
            elif discovered[other] < discovered[vertex]:
                stack.append(edge_index)
                low[vertex] = min(low[vertex], discovered[other])

    for root in range(graph.vertex_count):
        if discovered[root] >= 0:
            continue
        visit(root, -1)
        if stack:
            blocks.append(list(stack))
            stack.clear()
    labels = [-1] * len(graph.edges)
    for block_index, block in enumerate(blocks):
        for edge_index in block:
            if labels[edge_index] >= 0:
                raise ExtensionAuditError(
                    "independent edge-block replay duplicated an edge"
                )
            labels[edge_index] = block_index
    if any(label < 0 for label in labels):
        raise ExtensionAuditError(
            "independent edge-block replay lost an edge"
        )
    return tuple(labels)


@dataclass(frozen=True)
class _StrictPair:
    first: int
    second: int
    forest_count_e: int
    forest_count_f: int
    forest_count_ef: int
    left_product: int
    right_product: int

    @property
    def margin(self) -> int:
        return self.right_product - self.left_product


def _compare_strict_pairs(left: _StrictPair, right: _StrictPair) -> int:
    comparison = (
        left.left_product * right.right_product
        - right.left_product * left.right_product
    )
    if comparison:
        return -1 if comparison > 0 else 1
    if left.margin != right.margin:
        return -1 if left.margin < right.margin else 1
    left_identity = (left.first, left.second)
    right_identity = (right.first, right.second)
    if left_identity < right_identity:
        return -1
    if left_identity > right_identity:
        return 1
    return 0


def _decimal_ratio(numerator: int, denominator: int) -> str:
    with localcontext() as context:
        context.prec = 24
        return format(Decimal(numerator) / Decimal(denominator), ".20f")


def _expected_all_pair_semantics(
    replay: _AllPairReplay,
) -> dict[str, object]:
    graph = replay.extension.graph
    labels = _edge_block_labels(graph)
    strict: list[_StrictPair] = []
    equality_pairs = 0
    structural_equalities = 0
    within_block_equalities = 0
    violations = 0
    for first, second in combinations(range(len(graph.edges)), 2):
        pair_count = replay.pair_forest_counts[first][second]
        left_product = replay.forest_count * pair_count
        right_product = (
            replay.edge_forest_counts[first]
            * replay.edge_forest_counts[second]
        )
        if left_product == right_product:
            equality_pairs += 1
            if labels[first] == labels[second]:
                within_block_equalities += 1
            else:
                structural_equalities += 1
        elif left_product > right_product:
            violations += 1
        else:
            strict.append(
                _StrictPair(
                    first,
                    second,
                    replay.edge_forest_counts[first],
                    replay.edge_forest_counts[second],
                    pair_count,
                    left_product,
                    right_product,
                )
            )
    strict.sort(key=cmp_to_key(_compare_strict_pairs))
    top_records = []
    for pair in strict[:20]:
        top_records.append(
            {
                "edge_indexes": [pair.first, pair.second],
                "edge_e": list(graph.edges[pair.first]),
                "edge_f": list(graph.edges[pair.second]),
                "block_ids": [labels[pair.first], labels[pair.second]],
                "forest_count": replay.forest_count,
                "forest_count_e": pair.forest_count_e,
                "forest_count_f": pair.forest_count_f,
                "forest_count_ef": pair.forest_count_ef,
                "left_product": pair.left_product,
                "right_product": pair.right_product,
                "margin": pair.margin,
                "left_over_right": _decimal_ratio(
                    pair.left_product,
                    pair.right_product,
                ),
                "relative_gap": _decimal_ratio(
                    pair.margin,
                    pair.right_product,
                ),
            }
        )
    pair_count = len(graph.edges) * (len(graph.edges) - 1) // 2
    return {
        "mode": "single_graph",
        "graph6": graph.graph6,
        "vertices": graph.vertex_count,
        "edges": len(graph.edges),
        "edge_block_count": len(set(labels)),
        "pair_count": pair_count,
        "strict_pair_count": len(strict),
        "equality_pair_count": equality_pairs,
        "structural_equality_pair_count": structural_equalities,
        "within_block_equality_pair_count": within_block_equalities,
        "violation_pair_count": violations,
        "top_strict_pairs": top_records,
    }


def _validate_analysis_artifact(
    payload: Mapping[str, object],
    replay: _AllPairReplay,
    filename: str,
) -> dict[str, int]:
    expected_keys = {
        "mode",
        "graph6",
        "vertices",
        "edges",
        "edge_block_count",
        "pair_count",
        "strict_pair_count",
        "equality_pair_count",
        "structural_equality_pair_count",
        "within_block_equality_pair_count",
        "violation_pair_count",
        "states",
        "elapsed_seconds",
        "top_strict_pairs",
    }
    if set(payload) != expected_keys:
        raise ExtensionAuditError(
            f"{filename} has an unexpected key set"
        )
    _require_positive_runtime_fields(payload, filename)
    semantics = _expected_all_pair_semantics(replay)
    for field, expected in semantics.items():
        _require_exact(payload.get(field), expected, f"{filename}.{field}")
    return {
        "label_index": replay.extension.label_index,
        "edges": len(replay.extension.graph.edges),
        "pair_count": int(semantics["pair_count"]),
        "strict_pair_count": int(semantics["strict_pair_count"]),
        "equality_pair_count": int(semantics["equality_pair_count"]),
        "violation_pair_count": int(semantics["violation_pair_count"]),
        "top_strict_records_verified": len(
            semantics["top_strict_pairs"]  # type: ignore[arg-type]
        ),
    }


def audit_n12_labelled_extension_campaign(
    beam_path: Path,
    *,
    analysis_directory: Path | None = None,
) -> dict[str, object]:
    """Audit the frozen beam and its seven frozen representative analyses."""

    beam_path = Path(beam_path)
    analysis_directory = (
        beam_path.parent
        if analysis_directory is None
        else Path(analysis_directory)
    )
    source_hashes = _verify_source_hashes()
    beam = _read_frozen_json(beam_path, EXPECTED_BEAM_SHA256)
    analyses = {
        frozen.label_index: _read_frozen_json(
            analysis_directory / frozen.filename,
            frozen.sha256,
        )
        for frozen in FROZEN_ANALYSES
    }

    seed = _decode_compact_graph6(SEED_GRAPH6)
    if seed.graph6 != SEED_GRAPH6 or seed.vertex_count != SEED_ORDER:
        raise ExtensionAuditError("local seed replay disagrees with frozen seed")
    extensions = _enumerate_extensions(seed)
    by_label = {item.label_index: item for item in extensions}
    base = _BasePartitionReplay(seed)
    inherited = _replay_all_inherited_screens(seed, extensions, base)
    beam_summary = _validate_beam(beam, extensions, inherited)
    beam_summary["base_partition_states"] = len(base.partitions)

    selected = tuple(
        by_label[frozen.label_index] for frozen in FROZEN_ANALYSES
    )
    all_pair_replays = _replay_selected_all_pairs(seed, selected, base)
    all_pair_summaries = []
    inherited_by_label = {
        item.extension.label_index: item for item in inherited
    }
    for frozen, replay in zip(FROZEN_ANALYSES, all_pair_replays):
        if replay.extension.label_index != frozen.label_index:
            raise ExtensionAuditError("selected all-pair replay order drifted")
        inherited_replay = inherited_by_label[frozen.label_index]
        first, second = INHERITED_EDGE_INDEXES
        cross_check = (
            replay.forest_count,
            replay.edge_forest_counts[first],
            replay.edge_forest_counts[second],
            replay.pair_forest_counts[first][second],
        )
        expected_cross_check = (
            inherited_replay.forest_count,
            inherited_replay.forest_count_e,
            inherited_replay.forest_count_f,
            inherited_replay.forest_count_ef,
        )
        if cross_check != expected_cross_check:
            raise ExtensionAuditError(
                f"all-pair replay lost inherited counts at label {frozen.label_index}"
            )
        all_pair_summaries.append(
            {
                "filename": frozen.filename,
                "artifact_sha256": frozen.sha256,
                **_validate_analysis_artifact(
                    analyses[frozen.label_index],
                    replay,
                    frozen.filename,
                ),
                "exact_all_pair_count_table_sha256": (
                    _all_pair_count_table_sha256(replay)
                ),
                "inherited_counts_cross_checked": True,
            }
        )

    total_pairs = sum(
        int(item["pair_count"]) for item in all_pair_summaries
    )
    strict_pairs = sum(
        int(item["strict_pair_count"]) for item in all_pair_summaries
    )
    equalities = sum(
        int(item["equality_pair_count"]) for item in all_pair_summaries
    )
    violations = sum(
        int(item["violation_pair_count"]) for item in all_pair_summaries
    )
    return {
        "schema": AUDIT_SCHEMA,
        "campaign_complete": True,
        "beam_artifact": {
            "path": str(beam_path.resolve()),
            "sha256": EXPECTED_BEAM_SHA256,
        },
        "source_sha256": {
            **source_hashes,
            "independent_auditor": _file_sha256(Path(__file__).resolve()),
        },
        "independent_method": {
            "base_forest_state": "final component partition",
            "base_partition_states": len(base.partitions),
            "star_completion_identity": (
                "product over base-forest blocks B of "
                "(1 + |B intersect neighbour_set|)"
            ),
            "conditional_counts": (
                "force zero, one, or two base edges before the forward "
                "partition dynamic program; force star edges by excluding "
                "their occupied blocks from the completion product"
            ),
            "production_counter_imported": False,
        },
        "labelled_extension_replay": beam_summary,
        "representative_all_pair_replay": {
            "artifacts_verified": len(all_pair_summaries),
            "pair_count": total_pairs,
            "strict_pair_count": strict_pairs,
            "equality_pair_count": equalities,
            "violation_pair_count": violations,
            "persisted_top_strict_records_verified": sum(
                int(item["top_strict_records_verified"])
                for item in all_pair_summaries
            ),
            "graphs": all_pair_summaries,
        },
        "scope": {
            "seed_graph6": SEED_GRAPH6,
            "fixed_seed": True,
            "labelled_one_vertex_extensions_only": True,
            "extension_vertex": SEED_ORDER,
            "neighbour_subset_size_range": [
                MINIMUM_NEIGHBOURS,
                MAXIMUM_NEIGHBOURS,
            ],
            "labelled_extensions": EXPECTED_LABELLED_EXTENSIONS,
            "isomorphism_deduplicated": False,
            "nonisomorphic_order_12_exhaustion": False,
            "inherited_pair_screened_for_every_label": list(
                INHERITED_EDGE_INDEXES
            ),
            "all_pairs_screened_for_every_label": False,
            "all_pairs_replayed_for_representative_labels": [
                frozen.label_index for frozen in FROZEN_ANALYSES
            ],
        },
        "residual_trust_boundary": [
            (
                "The producer artifact did not embed source hashes; this audit "
                "externally freezes the exact observed producer and dependency "
                "files but cannot prove their historical process identity."
            ),
            (
                "The 1,012 labels may contain isomorphic duplicates and are "
                "not the nonisomorphic order-12 graph catalogue."
            ),
            (
                "Only the inherited edge pair is replayed for all 1,012 "
                "extensions; all pairs are replayed only for seven persisted "
                "representatives."
            ),
            (
                "Runtime state counts and elapsed times are bound by artifact "
                "hash and type checked, but are not reproduced by the "
                "independent partition dynamic program."
            ),
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Independently audit the frozen OPG-1757 n=12 labelled-extension "
            "beam and seven all-pair representative analyses."
        )
    )
    parser.add_argument("beam", type=Path)
    parser.add_argument("--analysis-directory", type=Path)
    arguments = parser.parse_args(argv)
    result = audit_n12_labelled_extension_campaign(
        arguments.beam,
        analysis_directory=arguments.analysis_directory,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
