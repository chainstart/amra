#!/usr/bin/env python3
"""Validate the self-contained R003 Erdős #522 second-audit package."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for name in ("RESULT.json", "SOURCE_MANIFEST.json", "TIMING.json"):
    try:
        json.loads((ROOT / name).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{name}: {exc}")

result = json.loads((ROOT / "RESULT.json").read_text(encoding="utf-8"))
if result.get("verdict") != "VERIFIED_CLOSED":
    fail("unexpected verdict")
if result.get("original_problem_closed_mathematically") is not True:
    fail("closure flag")
if result.get("central_files_modified") is not False:
    fail("central-file guard")
if result.get("git_commit_created") is not False:
    fail("commit guard")

timing = json.loads((ROOT / "TIMING.json").read_text(encoding="utf-8"))
if timing.get("wall_seconds", 0) <= 0:
    fail("nonpositive timing")
if timing.get("total_active_agent_seconds") != timing.get("wall_seconds"):
    fail("single-agent active time must equal wall time")
if timing.get("agents_used") != 1:
    fail("agent count")

check = subprocess.run(
    [sys.executable, str(ROOT / "verify_522_audit.py")],
    check=False,
    capture_output=True,
    text=True,
)
if check.returncode:
    fail(f"verify_522_audit.py:\n{check.stdout}\n{check.stderr}")
try:
    check_result = json.loads(check.stdout)
except json.JSONDecodeError as exc:
    fail(f"verifier output: {exc}")
if check_result.get("status") != "PASS":
    fail("verifier status")

expected = sorted(
    path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS"
)
listed: dict[str, str] = {}
for raw_line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
    digest, name = raw_line.split("  ", 1)
    listed[name] = digest
if sorted(listed) != expected:
    fail(f"checksum file list mismatch: listed={sorted(listed)}, expected={expected}")
for name, expected_digest in listed.items():
    actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if actual != expected_digest:
        fail(f"checksum mismatch: {name}")

print("PASS: R003 independent QA package for Erdős #522")
