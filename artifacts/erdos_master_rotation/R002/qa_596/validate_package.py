#!/usr/bin/env python3
"""Validate the self-contained #596 QA package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "AUDIT.md",
    "RESULT.json",
    "SOURCE_MANIFEST.json",
    "TIMING.json",
    "elementary_counterexample_search.json",
    "verify_elementary_branches.py",
    "validate_package.py",
    "SHA256SUMS",
}


def load_json(name: str) -> dict[str, object]:
    with (ROOT / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    present = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    missing = EXPECTED - present
    extras = present - EXPECTED
    if missing:
        errors.append(f"missing files: {sorted(missing)}")
    if extras:
        errors.append(f"unexpected files: {sorted(extras)}")

    result = load_json("RESULT.json")
    sources = load_json("SOURCE_MANIFEST.json")
    timing = load_json("TIMING.json")
    search = load_json("elementary_counterexample_search.json")

    if result.get("verdict") != "PASS_WITH_PRECISION_CORRECTIONS":
        errors.append("unexpected audit verdict")
    if result.get("theorem_valid") is not True:
        errors.append("theorem_valid is not true")
    if result.get("fatal_error_found") is not False:
        errors.append("fatal_error_found is not false")
    if search.get("passed") is not True or search.get("counterexample_count") != 0:
        errors.append("counterexample search did not pass cleanly")
    if search.get("max_order") != 6:
        errors.append("counterexample search max_order is not 6")
    source_ids = {entry.get("id") for entry in sources.get("sources", [])}
    required_source_ids = {
        "official_problem_596",
        "reiher_rodl_girth_ramsey",
        "nesetril_rodl_1987",
        "erdos_hajnal_1967",
    }
    if not required_source_ids <= source_ids:
        errors.append("source manifest is incomplete")
    if timing.get("finished_at") is None:
        errors.append("final timing has not been recorded")

    sums_path = ROOT / "SHA256SUMS"
    if sums_path.exists():
        recorded: dict[str, str] = {}
        pattern = re.compile(r"^([0-9a-f]{64})  (.+)$")
        for line in sums_path.read_text(encoding="utf-8").splitlines():
            match = pattern.fullmatch(line)
            if not match:
                errors.append(f"malformed checksum line: {line!r}")
                continue
            recorded[match.group(2)] = match.group(1)
        expected_hashed = EXPECTED - {"SHA256SUMS"}
        if set(recorded) != expected_hashed:
            errors.append(
                "checksum file list differs: "
                f"expected={sorted(expected_hashed)}, got={sorted(recorded)}"
            )
        for name, expected_digest in recorded.items():
            path = ROOT / name
            if path.exists() and sha256(path) != expected_digest:
                errors.append(f"checksum mismatch: {name}")

    payload = {
        "schema_version": "amra.erdos596.qa_validation.v1",
        "passed": not errors,
        "errors": errors,
        "checked_files": sorted(EXPECTED),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
