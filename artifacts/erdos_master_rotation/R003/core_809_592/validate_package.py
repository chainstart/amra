#!/usr/bin/env python3
"""Re-run finite certificates and verify the R003 #809/#592 package."""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parent


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_json(script):
    completed = subprocess.run(
        ["python3", str(script)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def verify_checksums():
    checksum_path = ROOT / "SHA256SUMS"
    checked = 0
    for raw_line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        digest, relative = raw_line.split("  ", 1)
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, (relative, digest, actual)
        checked += 1
    return checked


def main():
    # Parsing all declared JSON is also a schema/syntax guard.
    json_files = sorted(ROOT.rglob("*.json"))
    for path in json_files:
        load_json(path)

    checks = (
        (
            ROOT / "809" / "verify_809_r003.py",
            ROOT / "809" / "verification.json",
        ),
        (
            ROOT / "592" / "verify_592_depth3_slots.py",
            ROOT / "592" / "verification.json",
        ),
    )
    rerun = []
    for script, expected_path in checks:
        actual = run_json(script)
        expected = load_json(expected_path)
        assert actual == expected, script
        rerun.append(str(script.relative_to(ROOT)))

    checked_hashes = verify_checksums()
    print(
        json.dumps(
            {
                "json_files_parsed": len(json_files),
                "certificates_rerun": rerun,
                "sha256_entries_verified": checked_hashes,
                "passed": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
