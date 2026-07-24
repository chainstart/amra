#!/usr/bin/env python3
"""Validate the independent #671 audit metadata and claim guards."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
result = json.loads((ROOT / "RESULT.json").read_text())
timing = json.loads((ROOT / "TIMING.json").read_text())
audit = (ROOT / "AUDIT.md").read_text()
compile_log = (ROOT / "INDEPENDENT_COMPILE.log").read_text()

assert result["cycle_id"] == "R004"
assert timing["cycle_id"] == "R004"
assert timing["task"] == "independent_qa_671"
assert sum(timing["allocations_seconds"].values()) == timing["active_agent_seconds"]
assert timing["active_agent_seconds"] == 420
assert timing["active_agent_hours"] == 0.1166666667
assert result["problem_id"] == 671
assert result["official_status"] == "OPEN"
assert result["outcome"] == "VERIFIED_CLOSED_BY_PUBLIC_LEAN_PROOF"
assert result["original_problem_closed_mathematically"] is True
assert result["answers_first_question"] is True
assert result["answers_second_question"] is True
assert result["original_quantifiers_matched"] is True
assert result["independent_compile_exit_code"] == 0
assert result["sorry_ax_dependency"] is False
assert result["new_amra_proof"] is False
assert result["peer_review_confirmed"] is False
assert result["journal_publication_confirmed"] is False
assert result["api_identifier_replacements"] == 7
assert result["original_source_bytes"] == 125059
assert result["exact_api_compat_bytes"] == 125066
assert result["original_source_sha256"] in compile_log
assert result["exact_api_compat_sha256"] in compile_log
assert "sorryAx" in compile_log
assert "exit code:\n  0" in compile_log
assert len(audit) > 1500

if (ROOT / "SHA256SUMS").exists():
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        expected, filename = line.split("  ", 1)
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == expected

print("PASS: R004 independent #671 Lean audit")
