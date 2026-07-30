"""Hardened campaign wrapper for the completed OPG-1757 n=9 run.

This module deliberately leaves the v1 auditor and production search
untouched.  It first rejects incomplete or internally open checkpoints, then
invokes the v1 auditor on all four shards.  Finally it checks two contracts
that v1 does not close:

* every shard used the same validated dynamic-dependency hash map; and
* the four frozen ``geng`` slices form exactly the same duplicate-free
  catalogue as a frozen unsharded ``geng -q -c 9 19:36`` invocation.

The forest-count trust boundary remains unchanged: persisted events contain
only the production-selected edge pair, not the full per-graph pair matrix.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Iterator, Mapping, Sequence

import amra.discovery.opg_uniform_forest_run_audit as base_audit


AUDIT_SCHEMA = "amra.opg1757.run_audit.v2"
CAMPAIGN_ORDER = 9
CAMPAIGN_MINIMUM_EDGES = 19
CAMPAIGN_MAXIMUM_EDGES = 36
CAMPAIGN_SHARD_COUNT = 4
CAMPAIGN_EXPECTED_GENERATED = (26_861, 28_101, 37_477, 27_028)
CAMPAIGN_EXPECTED_TOTAL = 119_467
CAMPAIGN_GENG_SHA256 = (
    "9730b53764bdb28ecd2fdf755fafbc76992050f39e5ea19bb7d91433a26583e9"
)
CAMPAIGN_SORTED_CATALOGUE_SHA256 = (
    "b08e12a7a417184b29c66cfe84e9b9a188438da55cc408819c632caf2ec60538"
)


class UniformForestRunAuditV2Error(ValueError):
    """Raised when the hardened campaign audit fails closed."""


@dataclass(frozen=True)
class _Preflight:
    directories: tuple[Path, ...]
    states: tuple[Mapping[str, object], ...]
    tools: tuple[base_audit._ValidatedGeng, ...]
    dependency_hashes: Mapping[str, str]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _require_exact_int(value: object, field: str) -> int:
    if type(value) is not int:
        raise UniformForestRunAuditV2Error(f"{field} must be an integer")
    return value


def _read_state_for_preflight(
    directory: Path,
) -> tuple[int, Mapping[str, object]]:
    state_path = directory / "state.json"
    events_path = directory / "events.jsonl"
    if not state_path.is_file() or not events_path.is_file():
        raise UniformForestRunAuditV2Error(
            f"missing state/events in {directory}"
        )
    if (directory / "candidate.json").exists():
        raise UniformForestRunAuditV2Error(
            f"candidate.json is present in completed null shard {directory}"
        )
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise UniformForestRunAuditV2Error(
            f"cannot read valid state JSON in {directory}"
        ) from error
    if not isinstance(state, dict):
        raise UniformForestRunAuditV2Error(
            f"state must be a JSON object in {directory}"
        )
    shard = state.get("shard")
    if (
        state.get("checkpoint_schema") != 1
        or state.get("problem") != "opg1757"
        or state.get("connected_only") is not True
        or state.get("order") != CAMPAIGN_ORDER
        or state.get("minimum_edges") != CAMPAIGN_MINIMUM_EDGES
        or state.get("maximum_edges") != CAMPAIGN_MAXIMUM_EDGES
        or not isinstance(shard, list)
        or len(shard) != 2
        or type(shard[0]) is not int
        or shard[1] != CAMPAIGN_SHARD_COUNT
        or not 0 <= shard[0] < CAMPAIGN_SHARD_COUNT
    ):
        raise UniformForestRunAuditV2Error(
            f"state is not a frozen OPG-1757 n=9 i/4 shard in {directory}"
        )
    shard_index = int(shard[0])
    if state.get("status") != "complete":
        raise UniformForestRunAuditV2Error(
            f"shard {shard_index} is not complete"
        )
    if state.get("candidate") is not None:
        raise UniformForestRunAuditV2Error(
            f"shard {shard_index} retains a candidate"
        )
    if state.get("hard_queue") != []:
        raise UniformForestRunAuditV2Error(
            f"shard {shard_index} has a nonempty hard queue"
        )
    expected = CAMPAIGN_EXPECTED_GENERATED[shard_index]
    for field in ("generated", "evaluated", "nonviolating", "next_index"):
        actual = _require_exact_int(
            state.get(field),
            f"shard {shard_index} state.{field}",
        )
        if actual != expected:
            raise UniformForestRunAuditV2Error(
                f"shard {shard_index} state.{field} is {actual}, "
                f"expected {expected}"
            )
    for field in ("timeouts", "violations"):
        actual = _require_exact_int(
            state.get(field),
            f"shard {shard_index} state.{field}",
        )
        if actual != 0:
            raise UniformForestRunAuditV2Error(
                f"shard {shard_index} state.{field} is nonzero"
            )
    return shard_index, state


def _preflight_campaign(directories: Sequence[Path]) -> _Preflight:
    """Reject any incomplete shard before invoking the expensive v1 replay."""

    if len(directories) != CAMPAIGN_SHARD_COUNT:
        raise UniformForestRunAuditV2Error(
            f"exactly {CAMPAIGN_SHARD_COUNT} shard directories are required"
        )
    records = [
        (shard, Path(directory), state)
        for directory in directories
        for shard, state in [_read_state_for_preflight(Path(directory))]
    ]
    indexes = [record[0] for record in records]
    if sorted(indexes) != list(range(CAMPAIGN_SHARD_COUNT)):
        raise UniformForestRunAuditV2Error(
            "directories must contain every i/4 shard exactly once"
        )
    records.sort(key=lambda record: record[0])
    ordered_directories = tuple(record[1] for record in records)
    ordered_states = tuple(record[2] for record in records)

    tools: list[base_audit._ValidatedGeng] = []
    for shard_index, state in enumerate(ordered_states):
        try:
            tool = base_audit._validated_geng_tool(state)
        except (OSError, ValueError) as error:
            raise UniformForestRunAuditV2Error(
                f"shard {shard_index} geng validation failed: {error}"
            ) from error
        tools.append(tool)
    executable_hashes = {tool.sha256 for tool in tools}
    if executable_hashes != {CAMPAIGN_GENG_SHA256}:
        raise UniformForestRunAuditV2Error(
            "validated geng executable hash is not the frozen campaign hash"
        )
    dependency_maps = [dict(tool.dependency_hashes) for tool in tools]
    first_dependencies = dependency_maps[0]
    if any(mapping != first_dependencies for mapping in dependency_maps[1:]):
        raise UniformForestRunAuditV2Error(
            "geng dependency SHA-256 maps differ across shards"
        )
    return _Preflight(
        directories=ordered_directories,
        states=ordered_states,
        tools=tuple(tools),
        dependency_hashes=first_dependencies,
    )


def _iter_frozen_catalogue(
    tool: base_audit._ValidatedGeng,
    shard: tuple[int, int] | None,
) -> Iterator[str]:
    """Stream one frozen sharded or unsharded catalogue invocation."""

    environment = os.environ.copy()
    directories = list(tool.library_directories)
    previous = environment.get("LD_LIBRARY_PATH")
    if previous:
        directories.append(previous)
    if directories:
        environment["LD_LIBRARY_PATH"] = os.pathsep.join(directories)
    command = [
        str(tool.path),
        "-q",
        "-c",
        str(CAMPAIGN_ORDER),
        f"{CAMPAIGN_MINIMUM_EDGES}:{CAMPAIGN_MAXIMUM_EDGES}",
    ]
    if shard is not None:
        command.append(f"{shard[0]}/{shard[1]}")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=environment,
        )
    except OSError as error:
        raise UniformForestRunAuditV2Error(
            f"cannot execute frozen geng command: {command}"
        ) from error
    assert process.stdout is not None
    assert process.stderr is not None
    completed_normally = False
    try:
        for raw_line in process.stdout:
            record = raw_line.rstrip("\n")
            if not record:
                raise UniformForestRunAuditV2Error(
                    "geng emitted an empty catalogue record"
                )
            try:
                record.encode("ascii")
            except UnicodeEncodeError as error:
                raise UniformForestRunAuditV2Error(
                    "geng emitted a non-ASCII catalogue record"
                ) from error
            yield record
        stderr = process.stderr.read()
        return_code = process.wait()
        completed_normally = True
        if return_code != 0 or stderr.strip():
            raise UniformForestRunAuditV2Error(
                f"frozen geng invocation failed ({return_code}): "
                f"{stderr.strip()}"
            )
    finally:
        process.stdout.close()
        process.stderr.close()
        if not completed_normally and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def _sorted_catalogue_sha256(records: set[str]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records):
        digest.update(record.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _verify_catalogue_closure(
    tools: Sequence[base_audit._ValidatedGeng],
) -> dict[str, object]:
    if len(tools) != CAMPAIGN_SHARD_COUNT:
        raise UniformForestRunAuditV2Error(
            "catalogue closure requires one validated tool per shard"
        )
    sharded_records: set[str] = set()
    shard_counts: list[int] = []
    for shard_index in range(CAMPAIGN_SHARD_COUNT):
        count = 0
        for record in _iter_frozen_catalogue(
            tools[shard_index],
            (shard_index, CAMPAIGN_SHARD_COUNT),
        ):
            count += 1
            if record in sharded_records:
                raise UniformForestRunAuditV2Error(
                    "duplicate graph6 record across frozen sharded catalogues: "
                    f"{record}"
                )
            sharded_records.add(record)
        expected = CAMPAIGN_EXPECTED_GENERATED[shard_index]
        if count != expected:
            raise UniformForestRunAuditV2Error(
                f"frozen shard {shard_index}/4 emitted {count}, "
                f"expected {expected}"
            )
        shard_counts.append(count)
    if len(sharded_records) != CAMPAIGN_EXPECTED_TOTAL:
        raise UniformForestRunAuditV2Error(
            "combined frozen shard catalogue has the wrong size"
        )

    unsharded_records: set[str] = set()
    unsharded_count = 0
    for record in _iter_frozen_catalogue(tools[0], None):
        unsharded_count += 1
        if record in unsharded_records:
            raise UniformForestRunAuditV2Error(
                "duplicate graph6 record in frozen unsharded catalogue: "
                f"{record}"
            )
        unsharded_records.add(record)
    if unsharded_count != CAMPAIGN_EXPECTED_TOTAL:
        raise UniformForestRunAuditV2Error(
            f"frozen unsharded catalogue emitted {unsharded_count}, "
            f"expected {CAMPAIGN_EXPECTED_TOTAL}"
        )
    if sharded_records != unsharded_records:
        missing = sorted(unsharded_records - sharded_records)
        extra = sorted(sharded_records - unsharded_records)
        raise UniformForestRunAuditV2Error(
            "frozen sharded/unsharded catalogue sets differ: "
            f"missing={len(missing)} sample={missing[:3]}, "
            f"extra={len(extra)} sample={extra[:3]}"
        )

    sharded_digest = _sorted_catalogue_sha256(sharded_records)
    unsharded_digest = _sorted_catalogue_sha256(unsharded_records)
    if (
        sharded_digest != CAMPAIGN_SORTED_CATALOGUE_SHA256
        or unsharded_digest != CAMPAIGN_SORTED_CATALOGUE_SHA256
    ):
        raise UniformForestRunAuditV2Error(
            "sorted catalogue digest does not match the frozen campaign digest"
        )
    return {
        "unsharded_command_contract": [
            str(tools[0].path),
            "-q",
            "-c",
            str(CAMPAIGN_ORDER),
            f"{CAMPAIGN_MINIMUM_EDGES}:{CAMPAIGN_MAXIMUM_EDGES}",
        ],
        "sharded_command_contracts": [
            [
                str(tools[shard_index].path),
                "-q",
                "-c",
                str(CAMPAIGN_ORDER),
                f"{CAMPAIGN_MINIMUM_EDGES}:{CAMPAIGN_MAXIMUM_EDGES}",
                f"{shard_index}/{CAMPAIGN_SHARD_COUNT}",
            ]
            for shard_index in range(CAMPAIGN_SHARD_COUNT)
        ],
        "shard_counts": shard_counts,
        "sharded_count": len(sharded_records),
        "unsharded_count": unsharded_count,
        "sharded_duplicate_count": 0,
        "unsharded_duplicate_count": 0,
        "exact_set_equal": True,
        "exact_multiset_equal": True,
        "sharded_sorted_catalogue_sha256": sharded_digest,
        "unsharded_sorted_catalogue_sha256": unsharded_digest,
        "frozen_sorted_catalogue_sha256": (
            CAMPAIGN_SORTED_CATALOGUE_SHA256
        ),
    }


def audit_uniform_forest_campaign_v2(
    directories: Sequence[Path],
) -> dict[str, object]:
    """Run the v1 audit and close dependency and catalogue-partition gaps."""

    wrapper_path = Path(__file__).resolve()
    base_path = Path(base_audit.__file__).resolve()
    wrapper_hash = _file_sha256(wrapper_path)
    base_hash = _file_sha256(base_path)

    preflight = _preflight_campaign(directories)
    reports = [
        base_audit.audit_uniform_forest_shard(
            directory,
            expected_generated=CAMPAIGN_EXPECTED_GENERATED[shard_index],
        )
        for shard_index, directory in enumerate(preflight.directories)
    ]
    for shard_index, report in enumerate(reports):
        if report.get("schema") != base_audit.AUDIT_SCHEMA:
            raise UniformForestRunAuditV2Error(
                f"v1 report {shard_index} has the wrong schema"
            )
        if report.get("shard") != [shard_index, CAMPAIGN_SHARD_COUNT]:
            raise UniformForestRunAuditV2Error(
                f"v1 report returned the wrong shard at position {shard_index}"
            )
        expected = CAMPAIGN_EXPECTED_GENERATED[shard_index]
        if not (
            report.get("generated")
            == report.get("events_replayed")
            == report.get("nonviolating")
            == expected
            and report.get("violations") == 0
            and report.get("timeouts") == 0
        ):
            raise UniformForestRunAuditV2Error(
                f"v1 report {shard_index} counters do not close"
            )
        if report.get("auditor_sha256") != base_hash:
            raise UniformForestRunAuditV2Error(
                "v1 report does not contain the current base auditor hash"
            )
        if report.get("geng_sha256") != CAMPAIGN_GENG_SHA256:
            raise UniformForestRunAuditV2Error(
                "v1 report does not contain the frozen geng hash"
            )
        report_dependencies = report.get("geng_dependency_sha256")
        if (
            not isinstance(report_dependencies, dict)
            or report_dependencies != dict(preflight.dependency_hashes)
        ):
            raise UniformForestRunAuditV2Error(
                "v1 report dependency map differs from preflight"
            )
    implementation_hashes = {
        str(report.get("search_implementation_sha256"))
        for report in reports
    }
    if (
        len(implementation_hashes) != 1
        or len(next(iter(implementation_hashes))) != 64
    ):
        raise UniformForestRunAuditV2Error(
            "v1 reports disagree on search implementation hash"
        )

    catalogue_closure = _verify_catalogue_closure(preflight.tools)
    if _file_sha256(wrapper_path) != wrapper_hash:
        raise UniformForestRunAuditV2Error(
            "v2 wrapper source changed during the audit"
        )
    if _file_sha256(base_path) != base_hash:
        raise UniformForestRunAuditV2Error(
            "v1 base auditor source changed during the audit"
        )

    residual_boundary = reports[0].get("residual_trust_boundary")
    if not isinstance(residual_boundary, list):
        raise UniformForestRunAuditV2Error(
            "v1 report omitted its residual trust boundary"
        )
    return {
        "schema": AUDIT_SCHEMA,
        "campaign_complete": True,
        "problem": "opg1757",
        "scope": {
            "order": CAMPAIGN_ORDER,
            "edge_range": [
                CAMPAIGN_MINIMUM_EDGES,
                CAMPAIGN_MAXIMUM_EDGES,
            ],
            "connected_only": True,
            "shards": [
                [index, CAMPAIGN_SHARD_COUNT]
                for index in range(CAMPAIGN_SHARD_COUNT)
            ],
        },
        "base_v1_audit": {
            "schema": base_audit.AUDIT_SCHEMA,
            "shards": reports,
            "totals": {
                "generated": sum(
                    int(report["generated"]) for report in reports
                ),
                "events_replayed": sum(
                    int(report["events_replayed"]) for report in reports
                ),
                "nonviolating": sum(
                    int(report["nonviolating"]) for report in reports
                ),
                "violations": 0,
                "timeouts": 0,
            },
        },
        "dependency_closure": {
            "all_four_maps_identical": True,
            "geng_sha256": CAMPAIGN_GENG_SHA256,
            "geng_dependency_sha256": dict(preflight.dependency_hashes),
        },
        "catalogue_closure": catalogue_closure,
        "source_hashes": {
            "wrapper_auditor_path": str(wrapper_path),
            "wrapper_auditor_sha256": wrapper_hash,
            "base_auditor_path": str(base_path),
            "base_auditor_sha256": base_hash,
            "search_implementation_sha256": implementation_hashes.pop(),
        },
        "residual_trust_boundary": residual_boundary,
        "status": (
            "execution_evidence_verified_with_catalogue_closure_and_"
            "counting_trust_boundary"
        ),
    }


def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Harden the completed OPG-1757 n=9 four-shard v1 audit with "
            "dependency-map and unsharded-catalogue closure."
        )
    )
    parser.add_argument(
        "directories",
        nargs=CAMPAIGN_SHARD_COUNT,
        type=Path,
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    try:
        result = audit_uniform_forest_campaign_v2(arguments.directories)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if arguments.output is not None:
        _atomic_write_json(arguments.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
