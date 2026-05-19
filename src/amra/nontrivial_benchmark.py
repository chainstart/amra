from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amra.amra_library import AmraLibraryManager
from amra.known_problem_smoke import (
    PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
    _run_lean_check,
    _write_jsonl,
    utc_now_iso,
)
from amra.portfolio_memory import write_json
from amra.result_bundle import export_amra_result_bundle


NONTRIVIAL_BENCHMARK_SCHEMA_VERSION = "amra.nontrivial_closed_theorem_benchmark.v1"
NONTRIVIAL_BENCHMARK_CASE_SCHEMA_VERSION = "amra.nontrivial_closed_theorem_case.v1"
DEFAULT_NONTRIVIAL_BENCHMARK_CASE = "sum_first_n_odds"


@dataclass(frozen=True, slots=True)
class NontrivialClosedTheoremCase:
    problem_id: str
    title: str
    statement: str
    source: str
    difficulty: str
    selection_rationale: str
    lean_module: str
    lean_definition: str
    lean_declaration: str
    formal_statement: str
    lean_source: str
    proof_sketch: str

    @property
    def full_definition_name(self) -> str:
        return f"{self.lean_module}.{self.lean_definition}"

    @property
    def full_theorem_name(self) -> str:
        return f"{self.lean_module}.{self.lean_declaration}"


NONTRIVIAL_BENCHMARK_CASES: dict[str, NontrivialClosedTheoremCase] = {
    DEFAULT_NONTRIVIAL_BENCHMARK_CASE: NontrivialClosedTheoremCase(
        problem_id=DEFAULT_NONTRIVIAL_BENCHMARK_CASE,
        title="Sum of the First n Odd Numbers",
        statement=(
            "For every natural number n, the sum of the first n odd positive integers is n squared: "
            "1 + 3 + ... + (2n - 1) = n^2, with the empty sum for n = 0 equal to 0."
        ),
        source="Classical closed theorem; deterministic AMRA nontrivial benchmark case",
        difficulty="medium_school_induction",
        selection_rationale=(
            "Closed, non-fixture theorem with a real induction proof, no external search, and a Lean check "
            "that uses recursive definitions plus arithmetic simplification without requiring mathlib caches."
        ),
        lean_module="AMRA.NontrivialClosedBenchmark",
        lean_definition="oddSum",
        lean_declaration="odd_sum_first_n_odds",
        formal_statement="theorem odd_sum_first_n_odds (n : Nat) : oddSum n = n * n",
        lean_source="""namespace AMRA.NontrivialClosedBenchmark

def oddSum : Nat -> Nat
| 0 => 0
| n + 1 => oddSum n + (2 * n + 1)

theorem odd_sum_first_n_odds (n : Nat) : oddSum n = n * n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp [oddSum, ih, Nat.succ_mul, Nat.mul_succ, Nat.add_assoc, Nat.add_left_comm, Nat.add_comm]

end AMRA.NontrivialClosedBenchmark
""",
        proof_sketch=(
            "# Sum of the First n Odd Numbers\n\n"
            "We prove by induction on `n` that the sum of the first `n` odd positive integers is `n^2`.\n\n"
            "Base case: for `n = 0`, the empty sum is `0`, and `0^2 = 0`.\n\n"
            "Induction step: assume the sum of the first `n` odd positive integers is `n^2`. "
            "The next odd integer is `2n + 1`, so the sum of the first `n + 1` odd positive integers is\n\n"
            "`n^2 + (2n + 1) = (n + 1)^2`.\n\n"
            "This completes the induction and proves the theorem for every natural number `n`.\n"
        ),
    )
}


def select_nontrivial_closed_theorem_case(problem_id: str | None = None) -> NontrivialClosedTheoremCase:
    case_id = problem_id or DEFAULT_NONTRIVIAL_BENCHMARK_CASE
    case = NONTRIVIAL_BENCHMARK_CASES.get(case_id)
    if case is None:
        available = ", ".join(sorted(NONTRIVIAL_BENCHMARK_CASES))
        raise ValueError(f"Unknown AMRA nontrivial closed-theorem benchmark case: {case_id}. Available: {available}")
    return case


def _project_problem_yaml(case: NontrivialClosedTheoremCase) -> str:
    return "\n".join(
        [
            f"problem_id: {case.problem_id}",
            f"title: {case.title}",
            "statement: >-",
            f"  {case.statement}",
            f"source: {case.source}",
            "open_problem: false",
            "formalized: benchmark_verified_when_toolchain_available",
            "tags:",
            "  - nontrivial_closed_theorem_benchmark",
            "  - deterministic",
            "  - induction",
            "  - lean_verified_when_toolchain_available",
            "metadata:",
            f"  schema_version: {NONTRIVIAL_BENCHMARK_CASE_SCHEMA_VERSION}",
            "  deterministic_fixture: false",
            f"  difficulty: {case.difficulty}",
            f"  lean_module: {case.lean_module}",
            f"  lean_declaration: {case.lean_declaration}",
            f"  formal_statement: \"{case.formal_statement}\"",
            f"  selection_rationale: \"{case.selection_rationale}\"",
            "",
        ]
    )


def _verified_declarations_payload(
    *,
    case: NontrivialClosedTheoremCase,
    status: str,
) -> dict[str, Any]:
    declarations: list[dict[str, Any]] = []
    if status == "verified":
        declarations.extend(
            [
                {
                    "name": case.lean_definition,
                    "full_name": case.full_definition_name,
                    "lean_name": case.full_definition_name,
                    "kind": "def",
                    "status": "lean_verified",
                    "relative_path": "ClosedTheoremBenchmark.lean",
                    "statement": "def oddSum : Nat -> Nat",
                    "role": "formal_supporting_definition",
                },
                {
                    "name": case.lean_declaration,
                    "full_name": case.full_theorem_name,
                    "lean_name": case.full_theorem_name,
                    "kind": "theorem",
                    "status": "lean_verified",
                    "relative_path": "ClosedTheoremBenchmark.lean",
                    "statement": case.formal_statement,
                    "proof_method": "Nat induction plus simplification",
                    "dependency_declarations": [case.lean_definition],
                    "role": "main_benchmark_theorem",
                },
            ]
        )
    return {
        "schema_version": "amra.verified_declarations.v1",
        "problem_id": case.problem_id,
        "updated_at": utc_now_iso(),
        "declarations": declarations,
    }


def _ledger_records(
    *,
    case: NontrivialClosedTheoremCase,
    started_at: str,
    finished_at: str,
    status: str,
    build_report: dict[str, Any],
    library_report_path: str,
) -> list[dict[str, Any]]:
    return [
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{case.problem_id}-selection-001",
            "problem_id": case.problem_id,
            "phase": "problem_selection",
            "status": "selected",
            "proof_loop_state": "benchmark_target_selected",
            "backend": "deterministic_benchmark",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "summary": case.selection_rationale,
            "difficulty": case.difficulty,
        },
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{case.problem_id}-natural-proof-001",
            "problem_id": case.problem_id,
            "phase": "natural_language_proof",
            "status": "route_supported",
            "proof_loop_state": "informal_claim",
            "verification_boundary": "natural_language_only",
            "backend": "deterministic_benchmark",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "claim_id": "main",
            "summary": "Induction proof establishes the closed theorem in ordinary mathematical language.",
            "evidence_paths": ["proof/sketches/sum_first_n_odds.md"],
        },
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{case.problem_id}-lean-001",
            "problem_id": case.problem_id,
            "phase": "lean_formalization",
            "status": "lean_verified" if status == "verified" else "blocked",
            "proof_loop_state": "lean_verified_declaration" if status == "verified" else "blocked_formalization_gap",
            "verification_boundary": (
                "verified_declarations.json" if status == "verified" else "unresolved_blockers.md"
            ),
            "faithful_modeling_status": "faithfully_modeled" if status == "verified" else "blocked_formalization_gap",
            "backend": "deterministic_benchmark",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "claim_id": "main",
            "lean_build_report": "artifacts/lean_build_report.json",
            "verified_declarations": (
                [case.full_definition_name, case.full_theorem_name] if status == "verified" else []
            ),
            "blockers": [] if status == "verified" else build_report.get("diagnostics", []),
            "summary": build_report.get("summary", ""),
        },
        {
            "schema_version": PROOF_ATTEMPT_LEDGER_ENTRY_SCHEMA_VERSION,
            "attempt_id": f"{case.problem_id}-library-candidates-001",
            "problem_id": case.problem_id,
            "phase": "library_candidate_detection",
            "status": "candidate_report_written" if status == "verified" else "blocked",
            "backend": "deterministic_benchmark",
            "llm_calls": 0,
            "started_at": started_at,
            "finished_at": finished_at,
            "summary": "AMRA library harvest candidate report emitted for verified benchmark declarations.",
            "evidence_paths": [library_report_path],
        },
    ]


def _review_gate_payload(
    *,
    case: NontrivialClosedTheoremCase,
    status: str,
    build_report: dict[str, Any],
    library_report: dict[str, Any],
) -> dict[str, Any]:
    blockers: list[str] = []
    if status != "verified":
        blockers.append(build_report.get("summary", "Lean verification did not complete."))
    if status == "verified" and library_report.get("candidate_count", 0) < 2:
        blockers.append("Expected both the supporting definition and theorem to be library candidates.")
    decision = "approved" if not blockers else "blocked"
    return {
        "schema_version": "amra.nontrivial_benchmark_review_gate.v1",
        "problem_id": case.problem_id,
        "decision": decision,
        "checks": {
            "closed_problem": True,
            "non_fixture": True,
            "natural_language_proof_artifact": True,
            "lean_verification": status == "verified",
            "library_candidate_report": library_report.get("candidate_count", 0) >= 1,
            "bounded_local_runtime": True,
            "llm_calls": 0,
        },
        "blockers": blockers,
    }


def _write_project(
    *,
    project_dir: Path,
    case: NontrivialClosedTheoremCase,
    build_report: dict[str, Any],
    status: str,
    library_report: dict[str, Any],
    review_gate: dict[str, Any],
    ledger_records: list[dict[str, Any]],
) -> dict[str, Path]:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "problem.yaml").write_text(_project_problem_yaml(case), encoding="utf-8")
    write_json(
        project_dir / "state.json",
        {
            "schema_version": "amra.problem_state.v1",
            "problem_id": case.problem_id,
            "state": "verified" if status == "verified" else "parked",
            "reason": (
                "Nontrivial closed-theorem benchmark completed with a Lean-verified declaration."
                if status == "verified"
                else "Nontrivial closed-theorem benchmark is blocked at Lean verification."
            ),
        },
    )
    proof_dir = project_dir / "proof" / "sketches"
    proof_dir.mkdir(parents=True, exist_ok=True)
    (proof_dir / "sum_first_n_odds.md").write_text(case.proof_sketch, encoding="utf-8")
    write_json(project_dir / "artifacts" / "lean_build_report.json", build_report)
    write_json(project_dir / "verified_declarations.json", _verified_declarations_payload(case=case, status=status))

    memory_dir = project_dir / "memory"
    write_json(
        memory_dir / "claim_ledger.json",
        {
            "schema_version": "amra.claim_ledger.v1",
            "updated_at": utc_now_iso(),
            "claims": [
                {
                    "claim_id": "main",
                    "title": case.title,
                    "statement_nl": case.statement,
                    "status": "lean_verified" if status == "verified" else "lean_partial",
                    "validation_mode": "lean",
                    "evidence_paths": [
                        "proof/sketches/sum_first_n_odds.md",
                        "artifacts/lean_build_report.json",
                        "verified_declarations.json",
                    ],
                    "reusable": True,
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
                    "route_id": "induction-on-n",
                    "target_claim": "main",
                    "status": "completed" if status == "verified" else "blocked",
                    "core_idea": "Induct on n and add the next odd number 2n + 1.",
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
                "route_id": "induction-on-n",
                "failure_mode": "formalization_blocked",
                "failed_assertion": build_report.get("summary", "Lean verification blocked."),
                "approach": "Run the closed induction theorem through the local Lean executable.",
                "resume_condition": "Install Lean or increase the bounded benchmark timeout.",
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
                    "evidence_id": "lean-nontrivial-closed-theorem-check",
                    "kind": "lean_build_report",
                    "path": "artifacts/lean_build_report.json",
                    "status": build_report.get("status", "unknown"),
                    "claim_id": "main",
                },
                {
                    "evidence_id": "library-harvest-candidates",
                    "kind": "library_harvest_candidates",
                    "path": "library_harvest_candidates.json",
                    "status": "ready" if library_report.get("candidate_count", 0) else "blocked",
                    "claim_id": "main",
                },
            ],
        },
    )
    (project_dir / "writing_brief.md").write_text(
        "\n".join(
            [
                "# AMRA Nontrivial Closed-Theorem Benchmark Writing Brief",
                "",
                f"- Problem ID: `{case.problem_id}`",
                f"- Benchmark status: `{status}`",
                "- Backend: `deterministic_benchmark`; no LLM calls were made.",
                "- This is a closed classical theorem selected for end-to-end AMRA bundle testing.",
                "- ARA may cite Lean verification only for declarations listed in `verified_declarations.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_json(project_dir / "library_harvest_candidates.json", library_report)
    write_json(project_dir / "benchmark_review_gate.json", review_gate)
    review_dir = project_dir / "review"
    write_json(review_dir / "library_harvest_candidates.json", library_report)
    write_json(review_dir / "benchmark_review_gate.json", review_gate)
    ledger_path = _write_jsonl(project_dir / "proof_attempt_ledger.jsonl", ledger_records)
    return {"ledger": ledger_path}


def _candidate_report(
    *,
    project_dir: Path,
    repo_root: Path,
    case: NontrivialClosedTheoremCase,
    status: str,
) -> dict[str, Any]:
    if status == "verified":
        report = AmraLibraryManager(repo_root=repo_root).detect_harvest_candidates(
            project=project_dir,
            module="AmraLibrary.NumberTheory.OddSums",
        )
    else:
        report = {
            "schema_version": "amra.library_harvest_candidates.v1",
            "generated_at": utc_now_iso(),
            "project": str(project_dir),
            "module": "AmraLibrary.NumberTheory.OddSums",
            "candidate_count": 0,
            "rejected_count": 0,
            "candidates": [],
            "rejected": [],
        }
    for candidate in report.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        if str(candidate.get("declaration", "")).split(".")[-1] == case.lean_declaration:
            candidate["dependency_declarations"] = [case.lean_definition]
            candidate["library_harvest_note"] = (
                "Promote the supporting definition `oddSum` with this theorem so the theorem remains reusable."
            )
    return {
        **report,
        "benchmark_problem_id": case.problem_id,
        "benchmark_status": status,
        "library_candidate_gate": "ready" if report.get("candidate_count", 0) else "blocked",
    }


def _update_manifest(
    *,
    output_dir: Path,
    case: NontrivialClosedTheoremCase,
    status: str,
    benchmark_report: dict[str, Any],
) -> None:
    manifest_path = output_dir / "artifact_manifest.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["nontrivial_closed_theorem_benchmark"] = {
        "schema_version": NONTRIVIAL_BENCHMARK_SCHEMA_VERSION,
        "problem_id": case.problem_id,
        "status": status,
        "proof_attempt_ledger": "proof_attempt_ledger.jsonl",
        "lean_build_report": "lean_build_report.json",
        "library_harvest_candidates": "library_harvest_candidates.json",
        "benchmark_review_gate": "benchmark_review_gate.json",
        "llm_calls": 0,
        "proof_loop_state": benchmark_report.get("proof_loop_state", {}),
    }
    existing_paths = {item.get("path") for item in manifest.get("files", []) if isinstance(item, dict)}
    for record in [
        {
            "path": "nontrivial_benchmark_report.json",
            "kind": "nontrivial_benchmark_report",
            "required": False,
            "ara_contract_role": "benchmark_run_summary",
            "lean_verified_claim_source": False,
        }
    ]:
        if record["path"] not in existing_paths:
            manifest.setdefault("files", []).append(record)
            manifest.setdefault("artifacts", []).append(record)
    manifest["nontrivial_closed_theorem_benchmark"]["verified_declarations"] = benchmark_report.get(
        "verified_declarations", []
    )
    write_json(manifest_path, manifest)


def run_nontrivial_closed_theorem_benchmark(
    *,
    output_dir: Path,
    problem_id: str | None = None,
    max_seconds: int = 60,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Run a deterministic closed-theorem benchmark and export an AMRA result bundle."""

    if max_seconds <= 0:
        raise ValueError("--max-seconds must be positive")
    case = select_nontrivial_closed_theorem_case(problem_id)
    repo_root = repo_root.expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    project_dir = output_dir / "_nontrivial_closed_theorem_project"
    formal_dir = project_dir / "formal"
    formal_dir.mkdir(parents=True, exist_ok=True)
    lean_file = formal_dir / "ClosedTheoremBenchmark.lean"
    lean_file.write_text(case.lean_source, encoding="utf-8")

    started_at = utc_now_iso()
    deadline = time.monotonic() + max_seconds
    lean_timeout = max(1, min(max_seconds, int(deadline - time.monotonic())))
    build_report = _run_lean_check(lean_file=lean_file, timeout_seconds=lean_timeout)
    status = "verified" if build_report.get("verification_status") == "verified" else "blocked"
    build_report = {
        **build_report,
        "benchmark_problem_id": case.problem_id,
        "verified_target": case.full_theorem_name if status == "verified" else "",
        "summary": (
            "Lean verified the nontrivial closed-theorem benchmark declaration."
            if status == "verified"
            else build_report.get("summary", "Lean did not verify the benchmark declaration.")
        ),
    }
    write_json(project_dir / "artifacts" / "lean_build_report.json", build_report)
    write_json(project_dir / "verified_declarations.json", _verified_declarations_payload(case=case, status=status))
    library_report = _candidate_report(project_dir=project_dir, repo_root=repo_root, case=case, status=status)
    review_gate = _review_gate_payload(
        case=case,
        status=status,
        build_report=build_report,
        library_report=library_report,
    )
    finished_at = utc_now_iso()
    ledger_records = _ledger_records(
        case=case,
        started_at=started_at,
        finished_at=finished_at,
        status=status,
        build_report=build_report,
        library_report_path="library_harvest_candidates.json",
    )
    paths = _write_project(
        project_dir=project_dir,
        case=case,
        build_report=build_report,
        status=status,
        library_report=library_report,
        review_gate=review_gate,
        ledger_records=ledger_records,
    )
    bundle = export_amra_result_bundle(
        project=project_dir,
        output_dir=output_dir,
        repo_root=repo_root,
        consolidate=False,
    )
    verified_declarations = [case.full_definition_name, case.full_theorem_name] if status == "verified" else []
    benchmark_report = {
        "schema_version": NONTRIVIAL_BENCHMARK_SCHEMA_VERSION,
        "problem_id": case.problem_id,
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "max_seconds": max_seconds,
        "backend": "deterministic_benchmark",
        "llm_calls": 0,
        "selection": {
            "candidate_count": len(NONTRIVIAL_BENCHMARK_CASES),
            "selected_problem_id": case.problem_id,
            "difficulty": case.difficulty,
            "rationale": case.selection_rationale,
        },
        "project_dir": str(project_dir),
        "bundle_dir": str(output_dir),
        "proof_attempt_ledger": str(paths["ledger"]),
        "bundle_proof_attempt_ledger": str(output_dir / "proof_attempt_ledger.jsonl"),
        "natural_language_proof": str(project_dir / "proof" / "sketches" / "sum_first_n_odds.md"),
        "lean_file": str(lean_file),
        "lean_build_report": str(output_dir / "lean_build_report.json"),
        "verified_declarations": verified_declarations,
        "proof_loop_state": {
            "informal_claims": 1,
            "lean_verified_declarations": len(verified_declarations),
            "blocked_formalization_gaps": 0 if status == "verified" else 1,
            "model_mismatch": 0,
            "faithful_modeling_status": "faithfully_modeled" if status == "verified" else "blocked_formalization_gap",
        },
        "library_harvest_candidates": str(output_dir / "library_harvest_candidates.json"),
        "library_candidate_count": library_report.get("candidate_count", 0),
        "review_gate": review_gate,
        "blockers": review_gate.get("blockers", []),
        "bundle": bundle,
    }
    write_json(output_dir / "nontrivial_benchmark_report.json", benchmark_report)
    _update_manifest(output_dir=output_dir, case=case, status=status, benchmark_report=benchmark_report)
    return benchmark_report


__all__ = [
    "NONTRIVIAL_BENCHMARK_SCHEMA_VERSION",
    "NONTRIVIAL_BENCHMARK_CASE_SCHEMA_VERSION",
    "DEFAULT_NONTRIVIAL_BENCHMARK_CASE",
    "NONTRIVIAL_BENCHMARK_CASES",
    "NontrivialClosedTheoremCase",
    "select_nontrivial_closed_theorem_case",
    "run_nontrivial_closed_theorem_benchmark",
]
