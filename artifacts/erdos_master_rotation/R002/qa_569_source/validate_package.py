#!/usr/bin/env python3
"""Validate the #569 source-completion QA package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "AUDIT.md",
    "RESULT.json",
    "SEARCH_LOG.md",
    "SOURCE_MANIFEST.json",
    "TIMING.json",
    "SHA256SUMS",
    "validate_package.py",
}


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    files = {path.name for path in ROOT.iterdir() if path.is_file()}
    if files != EXPECTED:
        errors.append(
            f"file set mismatch: missing={sorted(EXPECTED-files)}, "
            f"extra={sorted(files-EXPECTED)}"
        )

    result = load("RESULT.json")
    manifest = load("SOURCE_MANIFEST.json")
    timing = load("TIMING.json")
    if result.get("verdict") != "SOURCE_NOT_OBTAINED":
        errors.append("unexpected verdict")
    for key in (
        "source_obtained",
        "fixed_dissertation_scan_obtained",
        "alternate_formal_all_m_source_obtained",
        "theorem_4_5_directly_verified",
    ):
        if result.get(key) is not False:
            errors.append(f"{key} must be false")
    if manifest.get("primary_full_text_obtained") is not False:
        errors.append("manifest primary_full_text_obtained must be false")
    if timing.get("finished_at") is None or timing.get("elapsed_wall_seconds") is None:
        errors.append("timing is incomplete")

    sums = ROOT / "SHA256SUMS"
    if sums.exists():
        pattern = re.compile(r"^([0-9a-f]{64})  (.+)$")
        recorded: dict[str, str] = {}
        for line in sums.read_text(encoding="utf-8").splitlines():
            match = pattern.fullmatch(line)
            if not match:
                errors.append(f"bad checksum line: {line!r}")
            else:
                recorded[match.group(2)] = match.group(1)
        expected_hashed = EXPECTED - {"SHA256SUMS"}
        if set(recorded) != expected_hashed:
            errors.append("checksum file set mismatch")
        for name, expected in recorded.items():
            path = ROOT / name
            if path.exists() and digest(path) != expected:
                errors.append(f"checksum mismatch: {name}")

    print(
        json.dumps(
            {
                "schema_version": "amra.erdos569.source_qa_validation.v1",
                "passed": not errors,
                "errors": errors,
                "checked_files": sorted(EXPECTED),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
