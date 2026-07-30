#!/usr/bin/env python3
"""Independently classify the KOU-21.137 SmallGroups search.

GAP supplies only raw catalogue Cayley tables.  This standard-library Python
program recomputes the exact exponent and all square-set predicates directly
from those tables.  It checks the group-table axioms needed to detect corrupt
transport, and performs a full associativity audit for every table.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import BinaryIO, Iterable

import numpy as np


SCHEMA = "amra.kou21137.smallgroups-classification.v1"
EXPECTED_COUNTS = {
    1: 1,
    2: 1,
    4: 2,
    8: 5,
    16: 14,
    32: 51,
    64: 267,
    128: 2328,
}
EXPECTED_TOTAL = sum(EXPECTED_COUNTS.values())


class AuditFailure(RuntimeError):
    """Raised whenever the scan cannot prove that its scope is complete."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _multiply(table: list[list[int]], left: int, right: int) -> int:
    return table[left][right]


def _find_identity(table: list[list[int]]) -> int:
    size = len(table)
    target = list(range(size))
    candidates = [
        index
        for index, row in enumerate(table)
        if row == target
        and all(table[left][index] == left for left in range(size))
    ]
    if len(candidates) != 1:
        raise AuditFailure(f"expected one identity, found {candidates}")
    return candidates[0]


def _inverses(table: list[list[int]], identity: int) -> list[int]:
    size = len(table)
    result: list[int] = []
    for element in range(size):
        candidates = [
            other
            for other in range(size)
            if table[element][other] == identity
            and table[other][element] == identity
        ]
        if len(candidates) != 1:
            raise AuditFailure(
                f"element {element} has {len(candidates)} two-sided inverses"
            )
        result.append(candidates[0])
    return result


def _element_order(
    table: list[list[int]], identity: int, element: int
) -> int:
    size = len(table)
    value = identity
    for order in range(1, size + 1):
        value = table[value][element]
        if value == identity:
            return order
    raise AuditFailure(f"element {element} did not return to the identity")


def _is_closed(
    table: list[list[int]], subset: set[int], inverses: list[int]
) -> bool:
    if not subset:
        return False
    if any(inverses[element] not in subset for element in subset):
        return False
    return all(
        table[left][right] in subset
        for left in subset
        for right in subset
    )


def _is_nonabelian(table: list[list[int]], subset: Iterable[int]) -> bool:
    values = list(subset)
    return any(
        table[left][right] != table[right][left]
        for left in values
        for right in values
    )


def _subgroup_generated(
    table: list[list[int]],
    identity: int,
    inverses: list[int],
    generators: Iterable[int],
) -> set[int]:
    subgroup = {identity, *generators}
    changed = True
    while changed:
        changed = False
        snapshot = tuple(subgroup)
        additions = {inverses[element] for element in snapshot}
        additions.update(
            table[left][right]
            for left in snapshot
            for right in snapshot
        )
        old_size = len(subgroup)
        subgroup.update(additions)
        changed = len(subgroup) != old_size
    return subgroup


def _commutator(
    table: list[list[int]], inverses: list[int], left: int, right: int
) -> int:
    # [left,right] = left^-1 right^-1 left right.
    value = table[inverses[left]][inverses[right]]
    value = table[value][left]
    return table[value][right]


def _full_associativity_check(table: list[list[int]]) -> None:
    """Check every triple, using NumPy only as a vectorized array engine."""
    size = len(table)
    array = np.asarray(table, dtype=np.uint8)
    indices = np.arange(size, dtype=np.intp)
    # At the largest audited order this materializes two 128^3 uint8
    # arrays, about 4 MiB in total, while checking every ordered triple.
    left_associated = array[array[:, :, None], indices[None, None, :]]
    right_associated = array[indices[:, None, None], array[None, :, :]]
    if not np.array_equal(left_associated, right_associated):
        mismatch = np.argwhere(left_associated != right_associated)[0]
        left, middle, right = map(int, mismatch)
        raise AuditFailure(
            "associativity failure at "
            f"({left},{middle},{right})"
        )


def _table_digest(table: list[list[int]]) -> str:
    digest = hashlib.sha256()
    for row in table:
        digest.update(bytes(row))
    return digest.hexdigest()


def audit_table(
    order: int, catalogue_id: int, table: list[list[int]]
) -> dict[str, object]:
    if len(table) != order or any(len(row) != order for row in table):
        raise AuditFailure(
            f"SmallGroup({order},{catalogue_id}) has wrong table dimensions"
        )
    expected_entries = set(range(order))
    for row_index, row in enumerate(table):
        if set(row) != expected_entries:
            raise AuditFailure(
                f"SmallGroup({order},{catalogue_id}) row {row_index} "
                "is not a permutation"
            )
    for column in range(order):
        if {table[row][column] for row in range(order)} != expected_entries:
            raise AuditFailure(
                f"SmallGroup({order},{catalogue_id}) column {column} "
                "is not a permutation"
            )

    identity = _find_identity(table)
    inverses = _inverses(table, identity)
    orders = [
        _element_order(table, identity, element)
        for element in range(order)
    ]
    exponent = math.lcm(*orders)
    square_values = {table[element][element] for element in range(order)}
    square_closed = _is_closed(table, square_values, inverses)
    square_values_nonabelian = _is_nonabelian(table, square_values)
    hit = exponent == 8 and square_closed and square_values_nonabelian

    _full_associativity_check(table)
    result: dict[str, object] = {
        "order": order,
        "catalogue_id": catalogue_id,
        "table_sha256": _table_digest(table),
        "identity_index_zero_based": identity,
        "exponent": exponent,
        "element_order_histogram": {
            str(key): value
            for key, value in sorted(Counter(orders).items())
        },
        "square_value_count": len(square_values),
        "square_values_form_subgroup": square_closed,
        "square_values_nonabelian": square_values_nonabelian,
        "hit": hit,
        "full_associativity_checked": True,
    }

    if square_values_nonabelian or hit:
        generated = _subgroup_generated(
            table, identity, inverses, square_values
        )
        result["square_generated_subgroup_size"] = len(generated)

    if hit:
        centre = {
            element
            for element in range(order)
            if all(
                table[element][other] == table[other][element]
                for other in range(order)
            )
        }
        commutators = {
            _commutator(table, inverses, left, right)
            for left in range(order)
            for right in range(order)
        }
        derived = _subgroup_generated(
            table, identity, inverses, commutators
        )
        frattini = _subgroup_generated(
            table,
            identity,
            inverses,
            square_values | commutators,
        )
        square_order_histogram = Counter(orders[value] for value in square_values)
        result.update(
            {
                "centre_size": len(centre),
                "derived_subgroup_size": len(derived),
                "frattini_subgroup_size": len(frattini),
                "derived_equals_square_values": derived == square_values,
                "frattini_equals_square_values": frattini == square_values,
                "quotient_by_squares_order": order // len(square_values),
                "square_subgroup_element_order_histogram": {
                    str(key): value
                    for key, value in sorted(square_order_histogram.items())
                },
            }
        )
    return result


def _parse_meta(line: str) -> dict[str, str]:
    parts = line.split("|")
    if parts[0] != "META":
        raise AuditFailure(f"expected META line, got {line!r}")
    metadata: dict[str, str] = {}
    for field in parts[1:]:
        if "=" not in field:
            raise AuditFailure(f"malformed META field {field!r}")
        key, value = field.split("=", 1)
        metadata[key] = value
    return metadata


def _run_gap_crosscheck(
    gap_binary: Path,
    gap_root: Path,
    script: Path,
    output_path: Path,
) -> tuple[str, dict[int, dict[str, int]], list[tuple[int, int]]]:
    completed = subprocess.run(
        [str(gap_binary), "-l", str(gap_root), "-q", str(script)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise AuditFailure(
            "GAP predicate cross-check failed: "
            + completed.stderr.decode("utf-8", "replace")
        )
    output_path.write_bytes(completed.stdout)
    summaries: dict[int, dict[str, int]] = {}
    hits: list[tuple[int, int]] = []
    saw_done = False
    for raw_line in completed.stdout.decode("utf-8").splitlines():
        if raw_line.startswith("HIT|"):
            parts = raw_line.split("|")
            hits.append((int(parts[1]), int(parts[2])))
        elif raw_line.startswith("SUMMARY|"):
            parts = raw_line.split("|")
            order = int(parts[1])
            values: dict[str, int] = {}
            for field in parts[2:]:
                key, value = field.split("=", 1)
                values[key] = int(value)
            summaries[order] = values
        elif raw_line == "DONE":
            saw_done = True
    if not saw_done:
        raise AuditFailure("GAP predicate cross-check did not reach DONE")
    return hashlib.sha256(completed.stdout).hexdigest(), summaries, hits


def run_scan(args: argparse.Namespace) -> dict[str, object]:
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / "all_cayley_tables.txt.gz"
    certificate_path = output_dir / "classification_certificate.json"
    crosscheck_path = output_dir / "gap_predicate_crosscheck.txt"

    process = subprocess.Popen(
        [
            str(args.gap_binary),
            "-l",
            str(args.gap_root),
            "-q",
            str(args.exporter),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1024 * 1024,
    )
    if process.stdout is None or process.stderr is None:
        raise AuditFailure("failed to open GAP pipes")

    stream_digest = hashlib.sha256()
    records: list[dict[str, object]] = []
    declared_counts: dict[int, int] = {}
    metadata: dict[str, str] | None = None
    current: tuple[int, int, int] | None = None
    rows: list[list[int]] = []
    cell_count = 0
    gap_table_sha256: str | None = None
    saw_header = False
    saw_done = False

    with archive_path.open("wb") as archive_handle:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=archive_handle, mtime=0
        ) as compressed:
            for raw_line in process.stdout:
                stream_digest.update(raw_line)
                compressed.write(raw_line)
                line = raw_line.decode("ascii").rstrip("\n")
                if line == "AMRA_KOU21137_CAYLEY_V2":
                    if saw_header:
                        raise AuditFailure("duplicate exporter header")
                    saw_header = True
                elif line.startswith("META|"):
                    metadata = _parse_meta(line)
                elif line.startswith("COUNT|"):
                    _, order_text, count_text = line.split("|")
                    declared_counts[int(order_text)] = int(count_text)
                elif line.startswith("BEGIN|"):
                    if current is not None:
                        raise AuditFailure("nested BEGIN")
                    _, order_text, id_text, size_text = line.split("|")
                    current = (
                        int(order_text),
                        int(id_text),
                        int(size_text),
                    )
                    order = current[0]
                    rows = [[-1] * order for _ in range(order)]
                    cell_count = 0
                    gap_table_sha256 = None
                elif line.startswith("ROW|"):
                    if current is None:
                        raise AuditFailure("ROW outside a group")
                    fields = line.split("|")
                    row_number = int(fields[1]) - 1
                    order = current[0]
                    if not 0 <= row_number < order:
                        raise AuditFailure("ROW coordinate out of range")
                    if len(fields) != order + 2:
                        raise AuditFailure("wrong number of ROW entries")
                    if any(value != -1 for value in rows[row_number]):
                        raise AuditFailure("duplicate ROW coordinate")
                    values = [int(value) - 1 for value in fields[2:]]
                    if any(value < 0 or value >= order for value in values):
                        raise AuditFailure("ROW value out of range")
                    rows[row_number] = values
                    cell_count += order
                elif line.startswith("TABLE_SHA256|"):
                    if current is None:
                        raise AuditFailure("TABLE_SHA256 outside a group")
                    if gap_table_sha256 is not None:
                        raise AuditFailure("duplicate TABLE_SHA256")
                    _, gap_table_sha256 = line.split("|")
                    # GAP 4.12.1's HexSHA256 omits leading zero nybbles
                    # (for example, it emits 63 characters for a digest
                    # beginning in 0).  Restore the conventional fixed-width
                    # representation before comparing with hashlib.
                    if (
                        not 1 <= len(gap_table_sha256) <= 64
                        or any(
                            character not in "0123456789abcdef"
                            for character in gap_table_sha256
                        )
                    ):
                        raise AuditFailure("malformed GAP TABLE_SHA256")
                    gap_table_sha256 = gap_table_sha256.zfill(64)
                elif line.startswith("END|"):
                    if current is None:
                        raise AuditFailure("END outside a group")
                    _, order_text, id_text = line.split("|")
                    order, catalogue_id, size = current
                    if (
                        int(order_text) != order
                        or int(id_text) != catalogue_id
                        or size != order
                    ):
                        raise AuditFailure("mismatched END")
                    if cell_count != order * order:
                        raise AuditFailure(
                            f"incomplete table: {cell_count} cells"
                        )
                    if gap_table_sha256 is None:
                        raise AuditFailure("missing GAP table digest")
                    record = audit_table(order, catalogue_id, rows)
                    if record["table_sha256"] != gap_table_sha256:
                        raise AuditFailure(
                            "GAP/Python multiplication-table hash mismatch "
                            f"at SmallGroup({order},{catalogue_id})"
                        )
                    records.append(record)
                    current = None
                    rows = []
                    cell_count = 0
                    gap_table_sha256 = None
                elif line.startswith("DONE|"):
                    _, total_text = line.split("|")
                    if int(total_text) != EXPECTED_TOTAL:
                        raise AuditFailure("wrong DONE total")
                    saw_done = True
                elif line:
                    raise AuditFailure(f"unknown exporter line {line[:80]!r}")

    stderr = process.stderr.read().decode("utf-8", "replace")
    return_code = process.wait()
    if return_code != 0:
        raise AuditFailure(f"GAP exporter failed: {stderr}")
    if stderr.strip():
        raise AuditFailure(f"GAP exporter wrote to stderr: {stderr}")
    if current is not None:
        raise AuditFailure("truncated final group")
    if not saw_header or not saw_done or metadata is None:
        raise AuditFailure("incomplete exporter envelope")
    if declared_counts != EXPECTED_COUNTS:
        raise AuditFailure(
            f"catalogue counts {declared_counts} != {EXPECTED_COUNTS}"
        )
    if len(records) != EXPECTED_TOTAL:
        raise AuditFailure(
            f"processed {len(records)} groups, expected {EXPECTED_TOTAL}"
        )

    per_order: dict[int, dict[str, int]] = {}
    for order, expected_count in EXPECTED_COUNTS.items():
        order_records = [
            record for record in records if record["order"] == order
        ]
        per_order[order] = {
            "groups": len(order_records),
            "exponent_eight": sum(
                record["exponent"] == 8 for record in order_records
            ),
            "square_subgroup": sum(
                record["exponent"] == 8
                and record["square_values_form_subgroup"]
                for record in order_records
            ),
            "nonabelian_square_values": sum(
                record["exponent"] == 8
                and record["square_values_nonabelian"]
                for record in order_records
            ),
            "hits": sum(record["hit"] for record in order_records),
        }
        if per_order[order]["groups"] != expected_count:
            raise AuditFailure(f"incomplete order {order}")

    crosscheck_sha256, gap_summaries, gap_hits = _run_gap_crosscheck(
        args.gap_binary,
        args.gap_root,
        args.crosscheck,
        crosscheck_path,
    )
    if gap_summaries != per_order:
        raise AuditFailure(
            f"GAP/Python summary disagreement: {gap_summaries} != {per_order}"
        )
    python_hits = [
        (int(record["order"]), int(record["catalogue_id"]))
        for record in records
        if record["hit"]
    ]
    if gap_hits != python_hits:
        raise AuditFailure(
            f"GAP/Python hit disagreement: {gap_hits} != {python_hits}"
        )

    certificate: dict[str, object] = {
        "schema": SCHEMA,
        "claim": (
            "Complete SmallGroups classification through order 128 for "
            "finite 2-groups of exponent exactly 8 whose square values form "
            "a nonabelian subgroup."
        ),
        "scope": {
            "orders": list(EXPECTED_COUNTS),
            "catalogue_counts": {
                str(key): value for key, value in EXPECTED_COUNTS.items()
            },
            "total_groups": EXPECTED_TOTAL,
        },
        "software": metadata,
        "methods": {
            "enumerator": (
                "GAP SmallGroups catalogue; raw multiplication tables only"
            ),
            "primary_semantics": (
                "Python/NumPy, recomputed from Cayley tables"
            ),
            "crosscheck": "independent GAP group predicates",
            "full_associativity": (
                "all n^3 triples for every one of the 2669 groups"
            ),
            "array_engine": f"NumPy {np.__version__}",
        },
        "per_order_summary": {
            str(key): value for key, value in per_order.items()
        },
        "hits": [
            record for record in records if bool(record["hit"])
        ],
        "all_group_outcomes": records,
        "artifacts": {
            "raw_decompressed_stream_sha256": stream_digest.hexdigest(),
            "raw_gzip_sha256": _sha256_file(archive_path),
            "gap_crosscheck_sha256": crosscheck_sha256,
            "exporter_sha256": _sha256_file(args.exporter),
            "verifier_sha256": _sha256_file(Path(__file__).resolve()),
            "crosscheck_script_sha256": _sha256_file(args.crosscheck),
        },
        "result": {
            "no_hit_below_128": all(
                not record["hit"]
                for record in records
                if int(record["order"]) < 128
            ),
            "order_128_hit_ids": [
                int(record["catalogue_id"])
                for record in records
                if record["order"] == 128 and record["hit"]
            ],
        },
    }
    serialized = (
        json.dumps(
            certificate,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    certificate_path.write_bytes(serialized)
    return {
        "certificate": str(certificate_path),
        "certificate_sha256": hashlib.sha256(serialized).hexdigest(),
        "archive": str(archive_path),
        "hits": python_hits,
        "per_order_summary": per_order,
    }


def build_parser() -> argparse.ArgumentParser:
    script_dir = Path(__file__).resolve().parent
    default_gap_base = (
        Path.home() / ".cache/amra/tools/gap-4.12.1/usr"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gap-binary",
        type=Path,
        default=default_gap_base / "lib/x86_64-linux-gnu/gap/gap",
    )
    parser.add_argument(
        "--gap-root",
        type=Path,
        default=default_gap_base / "share/gap",
    )
    parser.add_argument(
        "--exporter",
        type=Path,
        default=script_dir / "enumerate_smallgroups_tables.g",
    )
    parser.add_argument(
        "--crosscheck",
        type=Path,
        default=script_dir / "gap_predicate_crosscheck.g",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_dir / "artifacts",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for path_name in (
        "gap_binary",
        "gap_root",
        "exporter",
        "crosscheck",
    ):
        path = getattr(args, path_name)
        if not path.exists():
            raise AuditFailure(f"missing {path_name}: {path}")
    summary = run_scan(args)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        print(f"FAIL-CLOSED: {error}", file=sys.stderr)
        raise SystemExit(1)
