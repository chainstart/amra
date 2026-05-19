from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from amra.portfolio_memory import write_json
from amra.result_bundle import export_amra_result_bundle


KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION = "amra.known_problem_smoke.v1"
PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION = "amra.proof_attempt_ledger.entry.v1"


@dataclass(frozen=True, slots=True)
class KnownProblemFixture:
    problem_id: str
    title: str
    statement: str
    source: str
    formal_statement: str
    lean_module: str
    lean_declaration: str
    lean_source: str
    proof_sketch: str

    @property
    def full_lean_name(self) -> str:
        return f"{self.lean_module}.{self.lean_declaration}"


KNOWN_PROBLEM_FIXTURES: dict[str, KnownProblemFixture] = {
    "imo_2025_p1": KnownProblemFixture(
        problem_id="imo_2025_p1",
        title="AMRA Known-Problem Smoke Fixture",
        statement=(
            "Deterministic AMRA smoke fixture keyed as imo_2025_p1: prove that every natural "
            "number is equal to itself. This fixture exercises proof, Lean, ledger, and bundle "
            "interfaces; it is not the official IMO 2025 Problem 1 statement."
        ),
        source="AMRA deterministic known-problem smoke fixture",
        formal_statement="theorem imo_2025_p1_fixture_identity (n : Nat) : n = n",
        lean_module="AMRA.KnownProblemSmoke",
        lean_declaration="imo_2025_p1_fixture_identity",
        lean_source="""namespace AMRA.KnownProblemSmoke

theorem imo_2025_p1_fixture_identity (n : Nat) : n = n := rfl

end AMRA.KnownProblemSmoke
""",
        proof_sketch=(
            "# Deterministic Known-Problem Proof Sketch\n\n"
            "For an arbitrary natural number `n`, the target proposition is `n = n`. "
            "This is exactly reflexivity of equality, so Lean closes the formal theorem with `rfl`.\n"
        ),
    ),
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _tail(text: str, limit: int = 4000) -> str:
    return text[-limit:] if len(text) > limit else text


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_lean_binary() -> str | None:
    lean = shutil.which("lean")
    if lean:
        return lean
    fallback = Path.home() / ".elan" / "bin" / "lean"
    return str(fallback) if fallback.exists() else None


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    return path


def _run_lean_check(*, lean_file: Path, timeout_seconds: int) -> dict[str, Any]:
    started = time.monotonic()
    generated_at = utc_now_iso()
    lean_binary = _resolve_lean_binary()
    command = [lean_binary or "lean", str(lean_file.name)]
    if lean_binary is None:
        return {
            "schema_version": "amra.lean_build_report.v1",
            "status": "blocked",
            "verification_status": "blocked",
            "command": command,
            "workdir": str(lean_file.parent),
            "generated_at": generated_at,
            "build_seconds": 0.0,
            "returncode": None,
            "sorry_count": 0,
            "diagnostics": ["Lean executable was not found on PATH or in ~/.elan/bin."],
            "stdout_tail": "",
            "stderr_tail": "",
            "summary": "Lean check blocked because the Lean executable is unavailable.",
        }
    try:
        completed = subprocess.run(
            command,
            cwd=lean_file.parent,
            text=True,
            capture_output=True,
            timeout=max(1, timeout_seconds),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return {
            "schema_version": "amra.lean_build_report.v1",
            "status": "timeout",
            "verification_status": "blocked",
            "command": command,
            "workdir": str(lean_file.parent),
            "generated_at": generated_at,
            "build_seconds": round(time.monotonic() - started, 3),
            "returncode": None,
            "sorry_count": 0,
            "diagnostics": [f"Lean check exceeded timeout of {timeout_seconds} second(s)."],
            "stdout_tail": _tail(stdout),
            "stderr_tail": _tail(stderr),
            "summary": "Lean check timed out before the fixture could be verified.",
        }

    lean_text = lean_file.read_text(encoding="utf-8")
    forbidden_counts = {
        "sorry": lean_text.count("sorry"),
        "admit": lean_text.count("admit"),
        "axiom": lean_text.count("axiom"),
        "opaque": lean_text.count("opaque"),
    }
    forbidden_total = sum(forbidden_counts.values())
    diagnostics = [
        line.strip()
        for line in f"{completed.stdout}\n{completed.stderr}".splitlines()
        if line.strip() and ("error:" in line.lower() or "warning:" in line.lower() or "sorry" in line.lower())
    ]
    passed = completed.returncode == 0 and forbidden_total == 0
    status = "passed" if passed else "failed"
    return {
        "schema_version": "amra.lean_build_report.v1",
        "status": status,
        "verification_status": "verified" if passed else "blocked",
        "command": command,
        "workdir": str(lean_file.parent),
        "generated_at": generated_at,
        "build_seconds": round(time.monotonic() - started, 3),
        "returncode": completed.returncode,
        "sorry_count": forbidden_counts["sorry"],
        "forbidden_placeholder_counts": forbidden_counts,
        "diagnostics": diagnostics[-40:],
        "stdout_tail": _tail(completed.stdout),
        "stderr_tail": _tail(completed.stderr),
        "summary": (
            "Lean verified the deterministic fixture declaration."
            if passed
            else "Lean did not verify the deterministic fixture declaration."
        ),
    }


def _project_problem_yaml(fixture: KnownProblemFixture) -> str:
    return "\n".join(
        [
            f"problem_id: {fixture.problem_id}",
            f"title: {fixture.title}",
            "statement: >-",
            f"  {fixture.statement}",
            f"source: {fixture.source}",
            "open_problem: false",
            "formalized: fixture",
            "tags:",
            "  - known_problem_smoke",
            "  - deterministic_fixture",
            "  - lean_verified_when_toolchain_available",
            "metadata:",
            "  official_problem_statement: false",
            "  deterministic_fixture: true",
            f"  formal_statement: \"{fixture.formal_statement}\"",
            "",
        ]
    )


def _write_fixture_project(
    *,
    project_dir: Path,
    fixture: KnownProblemFixture,
    build_report: dict[str, Any],
    status: str,
    ledger_records: list[dict[str, Any]],
) -> dict[str, Path]:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "problem.yaml").write_text(_project_problem_yaml(fixture), encoding="utf-8")
    write_json(
        project_dir / "state.json",
        {
            "schema_version": "amra.problem_state.v1",
            "problem_id": fixture.problem_id,
            "state": "verified" if status == "verified" else "parked",
            "reason": (
                "Deterministic known-problem smoke completed with a Lean-verified fixture declaration."
                if status == "verified"
                else "Deterministic known-problem smoke is blocked at the Lean verification step."
            ),
        },
    )
    proof_dir = project_dir / "proof" / "sketches"
    proof_dir.mkdir(parents=True, exist_ok=True)
    (proof_dir / "known_problem_smoke.md").write_text(fixture.proof_sketch, encoding="utf-8")
    artifacts_dir = project_dir / "artifacts"
    write_json(artifacts_dir / "lean_build_report.json", build_report)
    write_json(
        project_dir / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "problem_id": fixture.problem_id,
            "updated_at": utc_now_iso(),
            "declarations": (
                [
                    {
                        "name": fixture.lean_declaration,
                        "full_name": fixture.full_lean_name,
                        "lean_name": fixture.full_lean_name,
                        "kind": "theorem",
                        "status": "lean_verified",
                        "relative_path": "formal/KnownProblemSmoke.lean",
                        "statement": fixture.formal_statement,
                        "proof_term": "rfl",
                    }
                ]
                if status == "verified"
                else []
            ),
        },
    )
    memory_dir = project_dir / "memory"
    write_json(
        memory_dir / "claim_ledger.json",
        {
            "schema_version": "amra.claim_ledger.v1",
            "updated_at": utc_now_iso(),
            "claims": [
                {
                    "claim_id": "main",
                    "title": fixture.title,
                    "statement_nl": fixture.statement,
                    "status": "lean_verified" if status == "verified" else "lean_partial",
                    "validation_mode": "lean",
                    "evidence_paths": [
                        "proof/sketches/known_problem_smoke.md",
                        "artifacts/lean_build_report.json",
                        "verified_declarations.json",
                    ],
                    "reusable": False,
                }
            ],
        },
    )
    write_json(
        memory_dir / "route_ledger.json",
        {
            "schema_version": "amra.route_ledger.v1",
            "updated_at": utc_now_iso(),
            "routes": [
                {
                    "route_id": "deterministic-reflexivity-route",
                    "target_claim": "main",
                    "status": "completed" if status == "verified" else "blocked",
                    "core_idea": "The fixture theorem is closed by reflexivity of equality.",
                    "attempt_count": 1,
                    "evaluator_verdict": status,
                    "blocker": "" if status == "verified" else build_report.get("summary", "Lean verification blocked."),
                }
            ],
        },
    )
    failed_routes = []
    if status != "verified":
        failed_routes.append(
            {
                "route_id": "deterministic-reflexivity-route",
                "failure_mode": "formalization_blocked",
                "failed_assertion": build_report.get("summary", "Lean verification blocked."),
                "approach": "Run the no-LLM reflexivity fixture through Lean.",
                "resume_condition": "Install Lean or increase the bounded smoke timeout.",
                "evidence_paths": ["artifacts/lean_build_report.json"],
            }
        )
    write_json(
        memory_dir / "failed_routes.json",
        {
            "schema_version": "amra.failed_routes.v1",
            "updated_at": utc_now_iso(),
            "failed_routes": failed_routes,
        },
    )
    write_json(
        memory_dir / "evidence_index.json",
        {
            "schema_version": "amra.evidence_index.v1",
            "updated_at": utc_now_iso(),
            "evidence": [
                {
                    "evidence_id": "lean-fixture-check",
                    "kind": "lean_build_report",
                    "path": "artifacts/lean_build_report.json",
                    "status": build_report.get("status", "unknown"),
                    "claim_id": "main",
                }
            ],
        },
    )
    (project_dir / "writing_brief.md").write_text(
        "\n".join(
            [
                "# AMRA Known-Problem Smoke Writing Brief",
                "",
                f"- Problem ID: `{fixture.problem_id}`",
                f"- Smoke status: `{status}`",
                "- Backend: `deterministic_fixture`; no LLM calls were made.",
                "- This is a fixture theorem for AMRA integration testing, not the official IMO 2025 Problem 1 statement.",
                "- ARA may cite Lean verification only for declarations listed in `verified_declarations.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    ledger_path = _write_jsonl(project_dir / "proof_attempt_ledger.jsonl", ledger_records)
    return {"ledger": ledger_path}


def _ledger_records(
    *,
    fixture: KnownProblemFixture,
    started_at: str,
    finished_at: str,
    status: str,
    build_report: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{fixture.problem_id}-natural-proof-001",
            "problem_id": fixture.problem_id,
            "phase": "natural_language_proof",
            "status": "route_supported",
            "backend": "deterministic_fixture",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "claim_id": "main",
            "summary": "Fixture proof sketch reduces the theorem to reflexivity.",
            "evidence_paths": ["proof/sketches/known_problem_smoke.md"],
        },
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{fixture.problem_id}-lean-001",
            "problem_id": fixture.problem_id,
            "phase": "lean_formalization",
            "status": "lean_verified" if status == "verified" else "blocked",
            "backend": "deterministic_fixture",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "claim_id": "main",
            "lean_build_report": "artifacts/lean_build_report.json",
            "verified_declarations": [fixture.full_lean_name] if status == "verified" else [],
            "blockers": [] if status == "verified" else build_report.get("diagnostics", []),
            "summary": build_report.get("summary", ""),
        },
    ]


def run_known_problem_smoke(
    *,
    problem_id: str,
    output_dir: Path,
    max_seconds: int = 60,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Run a bounded deterministic proof/Formalization smoke and export an AMRA bundle."""

    fixture = KNOWN_PROBLEM_FIXTURES.get(problem_id)
    if fixture is None:
        available = ", ".join(sorted(KNOWN_PROBLEM_FIXTURES))
        raise ValueError(f"Unknown AMRA known-problem smoke fixture: {problem_id}. Available: {available}")
    if max_seconds <= 0:
        raise ValueError("--max-seconds must be positive")

    repo_root = repo_root.expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stale_smoke_report = output_dir / "known_problem_smoke_report.json"
    if stale_smoke_report.exists():
        stale_smoke_report.unlink()
    project_dir = output_dir / "_known_problem_project"
    formal_dir = project_dir / "formal"
    formal_dir.mkdir(parents=True, exist_ok=True)
    lean_file = formal_dir / "KnownProblemSmoke.lean"
    lean_file.write_text(fixture.lean_source, encoding="utf-8")

    started_at = utc_now_iso()
    deadline = time.monotonic() + max_seconds
    lean_timeout = max(1, min(max_seconds, int(deadline - time.monotonic())))
    build_report = _run_lean_check(lean_file=lean_file, timeout_seconds=lean_timeout)
    status = "verified" if build_report.get("verification_status") == "verified" else "blocked"
    finished_at = utc_now_iso()
    ledger_records = _ledger_records(
        fixture=fixture,
        started_at=started_at,
        finished_at=finished_at,
        status=status,
        build_report=build_report,
    )
    paths = _write_fixture_project(
        project_dir=project_dir,
        fixture=fixture,
        build_report=build_report,
        status=status,
        ledger_records=ledger_records,
    )
    bundle = export_amra_result_bundle(
        project=project_dir,
        output_dir=output_dir,
        repo_root=repo_root,
        consolidate=False,
    )
    smoke_report = {
        "schema_version": KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION,
        "problem_id": fixture.problem_id,
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "max_seconds": max_seconds,
        "backend": "deterministic_fixture",
        "llm_calls": 0,
        "project_dir": str(project_dir),
        "bundle_dir": str(output_dir),
        "proof_attempt_ledger": str(paths["ledger"]),
        "bundle_proof_attempt_ledger": str(output_dir / "proof_attempt_ledger.jsonl"),
        "lean_build_report": str(output_dir / "lean_build_report.json"),
        "verified_declarations": [fixture.full_lean_name] if status == "verified" else [],
        "blockers": [] if status == "verified" else build_report.get("diagnostics", []),
        "bundle": bundle,
    }
    write_json(output_dir / "known_problem_smoke_report.json", smoke_report)
    manifest_path = output_dir / "artifact_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["known_problem_smoke"] = {
            "schema_version": KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION,
            "problem_id": fixture.problem_id,
            "status": status,
            "proof_attempt_ledger": "proof_attempt_ledger.jsonl",
            "lean_build_report": "lean_build_report.json",
            "llm_calls": 0,
        }
        report_path = output_dir / "known_problem_smoke_report.json"
        report_record = {
            "path": "known_problem_smoke_report.json",
            "kind": "known_problem_smoke_report",
            "required": False,
            "ara_contract_role": "smoke_run_summary",
            "lean_verified_claim_source": False,
            "bytes": report_path.stat().st_size,
            "sha256": _sha256_file(report_path),
        }
        for collection_name in ("files", "artifacts"):
            collection = [
                item
                for item in manifest.get(collection_name, [])
                if item.get("path") != "known_problem_smoke_report.json"
            ]
            collection.append(report_record)
            manifest[collection_name] = collection
        write_json(manifest_path, manifest)
    return smoke_report


__all__ = [
    "KNOWN_PROBLEM_SMOKE_SCHEMA_VERSION",
    "PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION",
    "KNOWN_PROBLEM_FIXTURES",
    "run_known_problem_smoke",
]
