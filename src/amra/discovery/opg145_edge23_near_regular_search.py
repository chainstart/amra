"""Exact OPG-145 search on the ``n=11, m=23, 4<=degree<=5`` layer.

Every graph in this frozen catalogue has degree sequence ``(5, 5, 4^9)``.
The campaign is split into sixteen independently counted shards and is
separately provenance-bound from both the full edge-23 and edge-24 layers.

The hardened dense runner is adapted only inside a process-local lock.  In
addition to freezing its schemas and identity, this wrapper replaces the base
catalogue validator so every generated and replayed graph is checked against
the exact near-regular degree sequence.  All base globals are restored on
every exit path.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
import math
from pathlib import Path
import threading
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg_coloring_search as coloring_search


CHECKPOINT_SCHEMA = "amra.opg145.n11-m23-d4-d5-16.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-m23-d4-d5-16.event.v1"
CAMPAIGN = "opg145_n11_edge23_near_regular_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
MINIMUM_DEGREE = 4
MAXIMUM_DEGREE = 5
DEGREE_SEQUENCE = (5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4)
COLOR_COUNT = 7
SHARD_COUNT = 16
EXPECTED_BY_SHARD: tuple[int, ...] = (
    880,
    449,
    664,
    517,
    425,
    602,
    906,
    629,
    451,
    437,
    492,
    507,
    611,
    536,
    463,
    417,
)
EXPECTED_TOTAL = 8_986

if len(EXPECTED_BY_SHARD) != SHARD_COUNT:
    raise RuntimeError(
        "the frozen near-regular denominator table is incomplete"
    )
if sum(EXPECTED_BY_SHARD) != EXPECTED_TOTAL:
    raise RuntimeError(
        "the frozen near-regular denominator total is inconsistent"
    )

_DELEGATION_LOCK = threading.Lock()


@dataclass(frozen=True)
class NearRegularSearchConfig:
    """The only configurable values for one frozen near-regular shard."""

    shard_index: int
    expected_generated: int
    per_instance_seconds: float
    minimum_edges: int = field(default=EDGE_COUNT, init=False)
    maximum_edges: int = field(default=EDGE_COUNT, init=False)

    def validate(self) -> None:
        if type(self.shard_index) is not int or not (
            0 <= self.shard_index < SHARD_COUNT
        ):
            raise ValueError(
                f"shard index must lie in 0..{SHARD_COUNT - 1}"
            )
        expected = EXPECTED_BY_SHARD[self.shard_index]
        if (
            type(self.expected_generated) is not int
            or self.expected_generated != expected
        ):
            raise ValueError(
                "the frozen near-regular denominator for shard "
                f"{self.shard_index}/{SHARD_COUNT} is {expected}"
            )
        if (
            not isinstance(self.per_instance_seconds, (int, float))
            or isinstance(self.per_instance_seconds, bool)
            or not math.isfinite(float(self.per_instance_seconds))
            or self.per_instance_seconds <= 0
        ):
            raise ValueError(
                "per_instance_seconds must be finite and positive"
            )

    @property
    def shard(self) -> tuple[int, int]:
        return self.shard_index, SHARD_COUNT

    @property
    def edge_range(self) -> str:
        return f"{EDGE_COUNT}:{EDGE_COUNT}"


def config_for_shard(
    shard_index: int, per_instance_seconds: float
) -> NearRegularSearchConfig:
    if type(shard_index) is not int or not 0 <= shard_index < SHARD_COUNT:
        raise ValueError(f"shard index must lie in 0..{SHARD_COUNT - 1}")
    return NearRegularSearchConfig(
        shard_index=shard_index,
        expected_generated=EXPECTED_BY_SHARD[shard_index],
        per_instance_seconds=per_instance_seconds,
    )


def _validate_near_regular_graph(
    graph: coloring_search.EdgeGraph,
    config: NearRegularSearchConfig,
) -> None:
    """Reject any record outside the exact mathematical catalogue."""

    config.validate()
    if (
        graph.vertex_count != ORDER
        or len(graph.edges) != EDGE_COUNT
        or tuple(sorted(graph.degrees, reverse=True)) != DEGREE_SEQUENCE
    ):
        raise RuntimeError(
            "catalogue graph violates n=11, m=23, degree sequence "
            "(5,5,4^9)"
        )


def _runtime_provenance() -> dict[str, object]:
    base_provenance = dense_search._runtime_provenance()
    toolchain = base_provenance.get("toolchain")
    if not isinstance(toolchain, Mapping):
        raise RuntimeError("the base runner returned no frozen toolchain")
    paths = (
        ("near_regular_wrapper", Path(__file__).resolve()),
        ("dense_base_runner", Path(dense_search.__file__).resolve()),
        ("shared_coloring", Path(coloring_search.__file__).resolve()),
    )
    return {
        "implementation": {
            "aggregate_sha256": coloring_search.implementation_fingerprint(
                *(path for _, path in paths)
            ),
            "files": [
                {
                    "role": role,
                    "path": str(path),
                    "sha256": coloring_search.file_sha256(path),
                }
                for role, path in paths
            ],
        },
        "toolchain": toolchain,
    }


def build_identity(config: NearRegularSearchConfig) -> dict[str, object]:
    config.validate()
    provenance = _runtime_provenance()
    toolchain = provenance["toolchain"]
    assert isinstance(toolchain, Mapping)
    geng = toolchain.get("geng")
    if not isinstance(geng, Mapping) or not geng.get("path"):
        raise RuntimeError("the frozen toolchain has no geng executable")
    canonical_command = [
        "geng",
        "-q",
        "-C",
        "-d4",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{config.shard_index}/{SHARD_COUNT}",
    ]
    denominator_manifest = {
        "method": (
            "independent_per_shard_graph6_line_count_with_nonquiet_u_"
            "total_crosscheck"
        ),
        "per_shard_catalogue_command_canonical": [
            "geng",
            "-q",
            "-C",
            "-d4",
            "-D5",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
            "i/16",
        ],
        "per_shard_count_operation": "count_stdout_graph6_records",
        "total_count_command_canonical": [
            "geng",
            "-C",
            "-d4",
            "-D5",
            "-u",
            str(ORDER),
            f"{EDGE_COUNT}:{EDGE_COUNT}",
        ],
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): count
            for index, count in enumerate(EXPECTED_BY_SHARD)
        },
        "total": EXPECTED_TOTAL,
    }
    actual_command = [str(geng["path"]), *canonical_command[1:]]
    return {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard": [config.shard_index, SHARD_COUNT],
        "expected_generated": config.expected_generated,
        "expected_denominator_manifest": denominator_manifest,
        "color_count": COLOR_COUNT,
        "known_positive_filter": "is_three_sparse",
        "catalogue_command": actual_command,
        "catalogue_command_canonical": canonical_command,
        "per_instance_seconds": config.per_instance_seconds,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": ORDER,
            "edge_count": EDGE_COUNT,
            "minimum_degree": MINIMUM_DEGREE,
            "maximum_degree": MAXIMUM_DEGREE,
            "degree_sequence_descending": list(DEGREE_SEQUENCE),
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
        **provenance,
    }


@contextmanager
def _near_regular_delegate_context() -> Iterator[None]:
    with _DELEGATION_LOCK:
        original_checkpoint_schema = dense_search.CHECKPOINT_SCHEMA
        original_event_schema = dense_search.EVENT_SCHEMA
        original_build_identity = dense_search.build_identity
        original_validator = dense_search._validate_catalogue_graph
        dense_search.CHECKPOINT_SCHEMA = CHECKPOINT_SCHEMA
        dense_search.EVENT_SCHEMA = EVENT_SCHEMA
        dense_search.build_identity = build_identity  # type: ignore[assignment]
        dense_search._validate_catalogue_graph = (  # type: ignore[assignment]
            _validate_near_regular_graph
        )
        try:
            yield
        finally:
            dense_search._validate_catalogue_graph = original_validator
            dense_search.build_identity = original_build_identity
            dense_search.EVENT_SCHEMA = original_event_schema
            dense_search.CHECKPOINT_SCHEMA = original_checkpoint_schema


def run_near_regular_search(
    config: NearRegularSearchConfig,
    *,
    wall_seconds: float,
    output: Path,
    max_cases: int = 0,
) -> dict[str, object]:
    config.validate()
    with _near_regular_delegate_context():
        return dense_search.run_dense_search(
            config,  # type: ignore[arg-type]
            wall_seconds=wall_seconds,
            output=output,
            max_cases=max_cases,
        )


def parse_shard(value: str) -> int:
    try:
        left_text, right_text = value.split("/", 1)
        left, right = int(left_text), int(right_text)
    except (AttributeError, TypeError, ValueError) as error:
        raise argparse.ArgumentTypeError("shard must have form i/16") from error
    if (
        right != SHARD_COUNT
        or not 0 <= left < SHARD_COUNT
        or value != f"{left}/{right}"
    ):
        raise argparse.ArgumentTypeError(
            "shard must have canonical form i/16 with 0<=i<16"
        )
    return left


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Exact resumable OPG-145 n=11,m=23,degree 4:5 search in sixteen "
            "frozen shards."
        )
    )
    parser.add_argument("--shard", type=parse_shard, required=True)
    parser.add_argument("--per-instance-seconds", type=float, default=300.0)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        config = config_for_shard(
            arguments.shard, arguments.per_instance_seconds
        )
        result = run_near_regular_search(
            config,
            wall_seconds=arguments.wall_seconds,
            output=arguments.output,
            max_cases=arguments.max_cases,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] in ("complete", "paused_budget") else 2


if __name__ == "__main__":
    raise SystemExit(main())
