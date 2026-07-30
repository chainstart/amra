"""Exact OPG-145 search on one structured ``n=11, m=23`` catalogue.

The catalogue is the output of the no-shell pipeline

``geng -q -C -d3 -D5 11 23:23 i/16 | pickg -q -M6``.

Here ``-M6`` selects graphs with six vertices of maximum degree.  Since the
degree sum is 46, ``-D5`` and the average degree force that maximum to be 5.
The remaining five degrees lie in 3..4 and sum to 16, so every accepted graph
has degree sequence ``(5^6,4,3^4)``.  The runner nevertheless checks that
sequence on every generated and replayed record.

This module only adapts the hardened dense runner inside a process-local lock.
It replaces the catalogue iterator with a two-``Popen`` pipeline, checks both
process return codes, and restores every shared global on all exit paths.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import threading
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg145_dense_search as dense_search
import amra.discovery.opg_coloring_search as coloring_search


CHECKPOINT_SCHEMA = "amra.opg145.n11-m23-d3-d5-M6-16.checkpoint.v1"
EVENT_SCHEMA = "amra.opg145.n11-m23-d3-d5-M6-16.event.v1"
CAMPAIGN = "opg145_n11_edge23_six_degree5_16shard_exact"
ORDER = 11
EDGE_COUNT = 23
MINIMUM_DEGREE = 3
MAXIMUM_DEGREE = 5
MAXIMUM_DEGREE_VERTEX_COUNT = 6
DEGREE_SEQUENCE = (5, 5, 5, 5, 5, 5, 4, 3, 3, 3, 3)
COLOR_COUNT = 7
SHARD_COUNT = 16
EXPECTED_BY_SHARD: tuple[int, ...] = (
    2_596,
    2_438,
    4_962,
    5_919,
    5_559,
    4_929,
    6_066,
    4_019,
    8_232,
    6_123,
    4_133,
    5_839,
    3_217,
    3_446,
    4_048,
    3_170,
)
EXPECTED_TOTAL = 74_696

if len(EXPECTED_BY_SHARD) != SHARD_COUNT:
    raise RuntimeError("the frozen six-degree-5 denominator table is incomplete")
if sum(EXPECTED_BY_SHARD) != EXPECTED_TOTAL:
    raise RuntimeError("the frozen six-degree-5 denominator total is inconsistent")

_DELEGATION_LOCK = threading.Lock()


@dataclass(frozen=True)
class SixDegree5SearchConfig:
    """The only configurable values for one frozen catalogue shard."""

    shard_index: int
    expected_generated: int
    per_instance_seconds: float
    minimum_edges: int = field(default=EDGE_COUNT, init=False)
    maximum_edges: int = field(default=EDGE_COUNT, init=False)

    def validate(self) -> None:
        if type(self.shard_index) is not int or not (
            0 <= self.shard_index < SHARD_COUNT
        ):
            raise ValueError(f"shard index must lie in 0..{SHARD_COUNT - 1}")
        expected = EXPECTED_BY_SHARD[self.shard_index]
        if (
            type(self.expected_generated) is not int
            or self.expected_generated != expected
        ):
            raise ValueError(
                "the frozen six-degree-5 denominator for shard "
                f"{self.shard_index}/{SHARD_COUNT} is {expected}"
            )
        if (
            not isinstance(self.per_instance_seconds, (int, float))
            or isinstance(self.per_instance_seconds, bool)
            or not math.isfinite(float(self.per_instance_seconds))
            or float(self.per_instance_seconds) <= 0
        ):
            raise ValueError("per_instance_seconds must be finite and positive")

    @property
    def shard(self) -> tuple[int, int]:
        return self.shard_index, SHARD_COUNT

    @property
    def edge_range(self) -> str:
        return f"{EDGE_COUNT}:{EDGE_COUNT}"


def config_for_shard(
    shard_index: int, per_instance_seconds: float
) -> SixDegree5SearchConfig:
    if type(shard_index) is not int or not 0 <= shard_index < SHARD_COUNT:
        raise ValueError(f"shard index must lie in 0..{SHARD_COUNT - 1}")
    return SixDegree5SearchConfig(
        shard_index=shard_index,
        expected_generated=EXPECTED_BY_SHARD[shard_index],
        per_instance_seconds=per_instance_seconds,
    )


def _pickg_path_for_geng(geng_path: Path) -> Path:
    """Resolve the nauty sibling used by this frozen two-process pipeline."""

    resolved = geng_path.resolve()
    names = (
        "nauty-pickg" if resolved.name.startswith("nauty-") else "pickg",
        "nauty-pickg",
        "pickg",
    )
    for name in dict.fromkeys(names):
        candidate = resolved.with_name(name)
        if (
            candidate.is_absolute()
            and candidate.is_file()
            and not candidate.is_symlink()
        ):
            return candidate.resolve()
    raise FileNotFoundError(
        f"required pickg sibling is unavailable beside {resolved}"
    )


def _validate_tool_record(name: str, record: Mapping[str, object]) -> None:
    if not record.get("path") or record.get("sha256") == "unavailable":
        raise FileNotFoundError(f"required frozen tool is unavailable: {name}")
    linkage = record.get("dynamic_linkage")
    if not isinstance(linkage, Mapping):
        raise RuntimeError(f"toolchain record for {name} has no linkage map")
    if linkage.get("missing"):
        raise RuntimeError(
            f"toolchain record for {name} has missing libraries: "
            f"{linkage['missing']}"
        )
    dependencies = linkage.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise RuntimeError(
            f"toolchain record for {name} has no dependency hashes"
        )
    for dependency, dependency_record in dependencies.items():
        if (
            not isinstance(dependency_record, Mapping)
            or not dependency_record.get("path")
            or not dependency_record.get("sha256")
        ):
            raise RuntimeError(
                f"incomplete dependency fingerprint for {name}: {dependency}"
            )


def _pickg_fingerprint(geng_record: Mapping[str, object]) -> dict[str, object]:
    raw_geng_path = geng_record.get("path")
    if not isinstance(raw_geng_path, str) or not raw_geng_path:
        raise RuntimeError("the frozen toolchain has no geng path")
    path = _pickg_path_for_geng(Path(raw_geng_path))
    record: dict[str, object] = {
        "path": str(path),
        "sha256": coloring_search.file_sha256(path),
        "dynamic_linkage": coloring_search._shared_library_fingerprint(path),
    }
    _validate_tool_record("pickg", record)
    return record


def _runtime_provenance() -> dict[str, object]:
    """Bind all sources, five base tools, pickg, and dynamic dependencies."""

    base_provenance = dense_search._runtime_provenance()
    raw_toolchain = base_provenance.get("toolchain")
    if not isinstance(raw_toolchain, Mapping):
        raise RuntimeError("the base runner returned no frozen toolchain")
    toolchain = dict(raw_toolchain)
    geng = toolchain.get("geng")
    if not isinstance(geng, Mapping):
        raise RuntimeError("the base runner returned no frozen geng")
    toolchain["pickg"] = _pickg_fingerprint(geng)
    for name, record in toolchain.items():
        if not isinstance(record, Mapping):
            raise RuntimeError(f"malformed frozen tool record: {name}")
        _validate_tool_record(str(name), record)

    paths = (
        ("six_degree5_wrapper", Path(__file__).resolve()),
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


def _denominator_manifest() -> dict[str, object]:
    return {
        "method": "independent_exact_pipeline_graph6_line_count",
        "per_shard_pipeline_canonical": [
            [
                "geng",
                "-q",
                "-C",
                "-d3",
                "-D5",
                str(ORDER),
                f"{EDGE_COUNT}:{EDGE_COUNT}",
                "i/16",
            ],
            ["pickg", "-q", f"-M{MAXIMUM_DEGREE_VERTEX_COUNT}"],
        ],
        "pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "per_shard_count_operation": "count_filtered_stdout_graph6_records",
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "degree_sequence_derivation": (
            "sum(deg)=46; average>4 and D5 force maximum degree 5; "
            "M6 gives six degree-5 vertices; the five remaining degrees "
            "are in 3..4 and sum to 16, hence (4,3,3,3,3)"
        ),
        "shard_count": SHARD_COUNT,
        "per_shard": {
            str(index): count
            for index, count in enumerate(EXPECTED_BY_SHARD)
        },
        "total": EXPECTED_TOTAL,
    }


def build_identity(config: SixDegree5SearchConfig) -> dict[str, object]:
    config.validate()
    provenance = _runtime_provenance()
    toolchain = provenance["toolchain"]
    assert isinstance(toolchain, Mapping)
    geng = toolchain.get("geng")
    pickg = toolchain.get("pickg")
    if not isinstance(geng, Mapping) or not isinstance(pickg, Mapping):
        raise RuntimeError("the frozen two-tool catalogue pipeline is incomplete")
    geng_canonical = [
        "geng",
        "-q",
        "-C",
        "-d3",
        "-D5",
        str(ORDER),
        f"{EDGE_COUNT}:{EDGE_COUNT}",
        f"{config.shard_index}/{SHARD_COUNT}",
    ]
    pickg_canonical = [
        "pickg",
        "-q",
        f"-M{MAXIMUM_DEGREE_VERTEX_COUNT}",
    ]
    geng_command = [str(geng["path"]), *geng_canonical[1:]]
    pickg_command = [str(pickg["path"]), *pickg_canonical[1:]]
    return {
        "campaign": CAMPAIGN,
        "problem": "opg145",
        "order": ORDER,
        "edge_range": [EDGE_COUNT, EDGE_COUNT],
        "generator_degree_range": [MINIMUM_DEGREE, MAXIMUM_DEGREE],
        "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
        "degree_sequence_descending": list(DEGREE_SEQUENCE),
        "shard": [config.shard_index, SHARD_COUNT],
        "expected_generated": config.expected_generated,
        "expected_denominator_manifest": _denominator_manifest(),
        "color_count": COLOR_COUNT,
        "known_positive_filter": "is_three_sparse",
        "catalogue_command": geng_command,
        "catalogue_command_canonical": geng_canonical,
        "catalogue_filter_command": pickg_command,
        "catalogue_filter_command_canonical": pickg_canonical,
        "catalogue_pipeline_transport": "stdout_pipe_two_popen_no_shell",
        "pipeline_environment_contract": {
            "locale": "C",
            "dynamic_library_directories": (
                "recorded_geng_and_pickg_dependency_parents"
            ),
            "removed_variables": ["LD_AUDIT", "LD_PRELOAD"],
        },
        "per_instance_seconds": config.per_instance_seconds,
        "checkpoint_interval_records": 1,
        "event_policy": "one_fsynced_event_per_generated_record",
        "fixed_campaign_contract": {
            "order": ORDER,
            "edge_count": EDGE_COUNT,
            "minimum_degree": MINIMUM_DEGREE,
            "maximum_degree": MAXIMUM_DEGREE,
            "maximum_degree_vertex_count": MAXIMUM_DEGREE_VERTEX_COUNT,
            "degree_sequence_descending": list(DEGREE_SEQUENCE),
            "shard_notation": "i/16",
            "caller_configurable_catalogue": False,
        },
        **provenance,
    }


def _pipeline_environment(
    geng_record: Mapping[str, object],
    pickg_record: Mapping[str, object],
) -> dict[str, str]:
    directories: list[str] = []
    for record in (geng_record, pickg_record):
        linkage = record.get("dynamic_linkage")
        if not isinstance(linkage, Mapping):
            raise RuntimeError("catalogue tool has no linkage map")
        dependencies = linkage.get("dependencies")
        if not isinstance(dependencies, Mapping):
            raise RuntimeError("catalogue tool has no dependency map")
        for dependency in dependencies.values():
            if not isinstance(dependency, Mapping):
                raise RuntimeError("catalogue tool has malformed dependency")
            raw_path = dependency.get("path")
            if not isinstance(raw_path, str) or not raw_path:
                raise RuntimeError("catalogue dependency has no path")
            directory = str(Path(raw_path).parent)
            if directory not in directories:
                directories.append(directory)
    environment = dict(os.environ)
    environment.pop("LD_AUDIT", None)
    environment.pop("LD_PRELOAD", None)
    environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    environment["LC_ALL"] = "C"
    return environment


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _iter_filtered_catalogue_records(command: Sequence[str]) -> Iterator[str]:
    """Stream the exact geng|pickg pipeline and require both clean exits."""

    if (
        len(command) != 8
        or list(command[1:7])
        != ["-q", "-C", "-d3", "-D5", "11", "23:23"]
        or command[7] not in {
            f"{index}/{SHARD_COUNT}" for index in range(SHARD_COUNT)
        }
    ):
        # The exact command is also identity-bound.  This local check catches
        # accidental use outside the delegate before any process is launched.
        raise RuntimeError("geng command does not match the frozen pipeline")
    geng_path = Path(str(command[0])).resolve()
    pickg_path = _pickg_path_for_geng(geng_path)
    geng_record: dict[str, object] = {
        "path": str(geng_path),
        "sha256": coloring_search.file_sha256(geng_path),
        "dynamic_linkage": coloring_search._shared_library_fingerprint(
            geng_path
        ),
    }
    pickg_record: dict[str, object] = {
        "path": str(pickg_path),
        "sha256": coloring_search.file_sha256(pickg_path),
        "dynamic_linkage": coloring_search._shared_library_fingerprint(
            pickg_path
        ),
    }
    environment = _pipeline_environment(geng_record, pickg_record)
    with (
        tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as geng_error,
        tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as pickg_error,
    ):
        geng_process = subprocess.Popen(
            [str(item) for item in command],
            stdout=subprocess.PIPE,
            stderr=geng_error,
            text=True,
            bufsize=1,
            env=environment,
        )
        if geng_process.stdout is None:
            _terminate(geng_process)
            raise RuntimeError("failed to open geng pipeline output")
        try:
            pickg_process = subprocess.Popen(
                [str(pickg_path), "-q", "-M6"],
                stdin=geng_process.stdout,
                stdout=subprocess.PIPE,
                stderr=pickg_error,
                text=True,
                bufsize=1,
                env=environment,
            )
        except BaseException:
            geng_process.stdout.close()
            _terminate(geng_process)
            raise
        geng_process.stdout.close()
        if pickg_process.stdout is None:
            _terminate(pickg_process)
            _terminate(geng_process)
            raise RuntimeError("failed to open pickg pipeline output")

        completed_normally = False
        try:
            for raw_line in pickg_process.stdout:
                record = raw_line.strip()
                if not record or record.startswith(">"):
                    raise RuntimeError(
                        "geng|pickg emitted an unexpected non-graph6 line"
                    )
                yield record
            pickg_return_code = pickg_process.wait()
            geng_return_code = geng_process.wait()
            geng_error.seek(0)
            pickg_error.seek(0)
            geng_stderr = geng_error.read().strip()
            pickg_stderr = pickg_error.read().strip()
            completed_normally = True
            if (
                geng_return_code != 0
                or pickg_return_code != 0
                or geng_stderr
                or pickg_stderr
            ):
                raise RuntimeError(
                    "frozen geng|pickg catalogue failed "
                    f"(geng={geng_return_code}, pickg={pickg_return_code}): "
                    f"geng stderr={geng_stderr!r}; "
                    f"pickg stderr={pickg_stderr!r}"
                )
        finally:
            pickg_process.stdout.close()
            if not completed_normally:
                _terminate(pickg_process)
                _terminate(geng_process)


def _validate_six_degree5_graph(
    graph: coloring_search.EdgeGraph,
    config: SixDegree5SearchConfig,
) -> None:
    config.validate()
    if (
        graph.vertex_count != ORDER
        or len(graph.edges) != EDGE_COUNT
        or tuple(sorted(graph.degrees, reverse=True)) != DEGREE_SEQUENCE
    ):
        raise RuntimeError(
            "catalogue graph violates n=11, m=23, degree sequence "
            "(5^6,4,3^4)"
        )


@contextmanager
def _six_degree5_delegate_context() -> Iterator[None]:
    with _DELEGATION_LOCK:
        names = (
            "CHECKPOINT_SCHEMA",
            "EVENT_SCHEMA",
            "build_identity",
            "_iter_catalogue_records",
            "_validate_catalogue_graph",
        )
        originals = {name: getattr(dense_search, name) for name in names}
        replacements = {
            "CHECKPOINT_SCHEMA": CHECKPOINT_SCHEMA,
            "EVENT_SCHEMA": EVENT_SCHEMA,
            "build_identity": build_identity,
            "_iter_catalogue_records": _iter_filtered_catalogue_records,
            "_validate_catalogue_graph": _validate_six_degree5_graph,
        }
        for name, value in replacements.items():
            setattr(dense_search, name, value)
        try:
            yield
        finally:
            for name, value in originals.items():
                setattr(dense_search, name, value)


def run_six_degree5_search(
    config: SixDegree5SearchConfig,
    *,
    wall_seconds: float,
    output: Path,
    max_cases: int = 0,
) -> dict[str, object]:
    config.validate()
    with _six_degree5_delegate_context():
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
            "Exact resumable OPG-145 n=11,m=23,(5^6,4,3^4) search in "
            "sixteen frozen geng|pickg shards."
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
        result = run_six_degree5_search(
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
