"""Deterministic proof-loop stability benchmark fixtures."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import yaml

from amra.proof.loops import ProofLoopRegistry, ProofRunRequest, ProofRunResult, normalize_proof_status


PROOF_STABILITY_SUITE_SCHEMA_VERSION = "amra.proof_stability.suite.v1"
PROOF_STABILITY_REPORT_SCHEMA_VERSION = "amra.proof_stability.report.v1"
PROOF_STABILITY_CASE_SCHEMA_VERSION = "amra.proof_stability.case_result.v1"
PROOF_STABILITY_RESUME_SCHEMA_VERSION = "amra.proof_stability.resume_record.v1"

NO_LIVE_BACKENDS = {"none", "fake", "deterministic_fixture"}
FAILURE_TAXONOMY = {
    "none",
    "budget_exhausted",
    "blocked_formalization_gap",
    "partial_proof",
    "proof_search_exhausted",
    "runner_failure",
    "route_selection_regression",
    "status_mismatch",
    "fixture_invalid",
    "unexpected_live_backend",
    "unbounded_budget",
    "unknown_status",
}


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() else "-" for char in value.strip().lower())
    return "-".join(part for part in cleaned.split("-") if part) or "case"


def _positive_int(value: Any, *, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return parsed


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    return value


def load_proof_stability_suite(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("Proof stability suite must be a mapping.")
    if payload.get("schema_version") != PROOF_STABILITY_SUITE_SCHEMA_VERSION:
        raise ValueError(
            "Unsupported proof stability suite schema: "
            f"{payload.get('schema_version')!r}; expected {PROOF_STABILITY_SUITE_SCHEMA_VERSION}."
        )
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Proof stability suite must contain at least one case.")
    return payload


@dataclass(frozen=True, slots=True)
class _CaseBudget:
    max_steps: int
    time_budget_seconds: int
    simulated_steps: int
    simulated_seconds: int

    @property
    def finite(self) -> bool:
        return self.max_steps > 0 and self.time_budget_seconds > 0

    @property
    def exhausted(self) -> bool:
        return self.simulated_steps > self.max_steps or self.simulated_seconds > self.time_budget_seconds

    def to_dict(self) -> dict[str, int]:
        return {
            "max_steps": self.max_steps,
            "time_budget_seconds": self.time_budget_seconds,
            "simulated_steps": self.simulated_steps,
            "simulated_seconds": self.simulated_seconds,
        }


class _FixtureProofRunner:
    def __init__(self, *, route: str, report: Mapping[str, Any]) -> None:
        self.route = route
        self.report = dict(report)

    def __getattr__(self, name: str):
        def _method(**parameters: Any) -> dict[str, Any]:
            payload = {
                "status": self.report.get("status", "completed"),
                "route": self.route,
                "method": name,
                "backend": parameters.get("backend", "none"),
                "llm_calls": 0,
                "live_model_calls": False,
                "deterministic_fixture": True,
                "parameter_keys": sorted(str(key) for key in parameters),
            }
            payload.update(self.report)
            payload["llm_calls"] = 0
            payload["live_model_calls"] = False
            payload["deterministic_fixture"] = True
            return payload

        return _method


def _fixture_registry(fake_report: Mapping[str, Any]) -> ProofLoopRegistry:
    def factory(contract, repo_root: Path) -> _FixtureProofRunner:
        return _FixtureProofRunner(route=contract.route, report=fake_report)

    return ProofLoopRegistry(runner_factory=factory)


def _case_budget(case: Mapping[str, Any], defaults: Mapping[str, Any]) -> _CaseBudget:
    return _CaseBudget(
        max_steps=_positive_int(case.get("max_steps"), default=_positive_int(defaults.get("max_steps"), default=3)),
        time_budget_seconds=_positive_int(
            case.get("time_budget_seconds"),
            default=_positive_int(defaults.get("time_budget_seconds"), default=30),
        ),
        simulated_steps=_positive_int(case.get("simulated_steps"), default=1),
        simulated_seconds=_positive_int(case.get("simulated_seconds"), default=1),
    )


def _failure_taxon(raw_status: str, canonical_status: str, report: Mapping[str, Any]) -> str:
    explicit = str(report.get("failure_taxon", "")).strip()
    if explicit:
        return explicit if explicit in FAILURE_TAXONOMY else "unknown_status"
    if canonical_status in {"verified", "completed", "skipped"}:
        return "none"
    if canonical_status == "partial":
        if raw_status in {"exhausted", "rounds_exhausted", "time_budget_exhausted"}:
            return "proof_search_exhausted"
        return "partial_proof"
    if canonical_status == "blocked":
        return "blocked_formalization_gap"
    if canonical_status == "failed":
        return "runner_failure"
    return "unknown_status"


def _expected(case: Mapping[str, Any]) -> dict[str, str]:
    raw = case.get("expected")
    payload = raw if isinstance(raw, Mapping) else {}
    return {
        "route": str(payload.get("route", case.get("route", ""))).strip(),
        "canonical_status": str(payload.get("canonical_status", "")).strip(),
        "failure_taxon": str(payload.get("failure_taxon", "none")).strip(),
    }


def _case_parameters(case: Mapping[str, Any], *, suite_dir: Path, case_dir: Path) -> dict[str, Any]:
    raw_parameters = case.get("parameters")
    parameters = dict(raw_parameters) if isinstance(raw_parameters, Mapping) else {}
    if case.get("statement") is not None:
        parameters.setdefault("statement", str(case.get("statement")))
    if "backend" in case:
        parameters.setdefault("backend", case.get("backend"))
    else:
        parameters.setdefault("backend", "none")

    for key in ("project_dir", "workspace", "manifest_path", "target_file"):
        if key not in parameters:
            continue
        path = Path(str(parameters[key]))
        parameters[key] = path if path.is_absolute() else (suite_dir / path)

    route = str(case.get("route", "")).strip()
    if route in {"proof_search", "closure", "math_attack"}:
        parameters.setdefault("project_dir", case_dir / "project")
    if route in {"proof_search", "closure"}:
        parameters.setdefault("orchestrator", "deterministic_fixture_orchestrator")
    if route == "focused_attack":
        parameters.setdefault("workspace", case_dir / "workspace")
        parameters.setdefault("attack_targets", ["main"])
    return parameters


def _guarded_case_result(
    *,
    case: Mapping[str, Any],
    case_id: str,
    case_dir: Path,
    budget: _CaseBudget,
    expected: Mapping[str, str],
    failure_taxon: str,
    message: str,
) -> dict[str, Any]:
    canonical_status = "blocked"
    route = str(case.get("route", ""))
    mismatches = []
    if expected.get("route") and expected["route"] != route:
        mismatches.append({"field": "route", "expected": expected["route"], "actual": route})
    if expected.get("canonical_status") and expected["canonical_status"] != canonical_status:
        mismatches.append(
            {"field": "canonical_status", "expected": expected["canonical_status"], "actual": canonical_status}
        )
    if expected.get("failure_taxon", "none") != failure_taxon:
        mismatches.append(
            {"field": "failure_taxon", "expected": expected.get("failure_taxon", "none"), "actual": failure_taxon}
        )
    status = "passed" if not mismatches else "failed"
    result = {
        "schema_version": PROOF_STABILITY_CASE_SCHEMA_VERSION,
        "case_id": case_id,
        "case_kind": str(case.get("kind", "unknown")),
        "route": route,
        "status": status,
        "canonical_status": canonical_status,
        "raw_status": failure_taxon,
        "failure_taxon": failure_taxon,
        "expected": dict(expected),
        "budget": budget.to_dict(),
        "executed": False,
        "llm_calls": 0,
        "live_model_calls": False,
        "mismatches": mismatches,
        "message": message,
    }
    _write_json(case_dir / "result.json", result)
    return result


def _run_case(
    *,
    case: Mapping[str, Any],
    suite_dir: Path,
    output_dir: Path,
    defaults: Mapping[str, Any],
) -> dict[str, Any]:
    case_id = _slug(str(case.get("id", "")))
    if not case_id:
        raise ValueError("Proof stability case is missing id.")
    case_dir = output_dir / "cases" / case_id
    case_dir.mkdir(parents=True, exist_ok=True)

    budget = _case_budget(case, defaults)
    expected = _expected(case)
    backend = str(case.get("backend", "none")).strip() or "none"
    if backend not in NO_LIVE_BACKENDS:
        return _guarded_case_result(
            case=case,
            case_id=case_id,
            case_dir=case_dir,
            budget=budget,
            expected=expected,
            failure_taxon="unexpected_live_backend",
            message=f"Case backend {backend!r} is not allowed in proof stability fixtures.",
        )
    if not budget.finite:
        return _guarded_case_result(
            case=case,
            case_id=case_id,
            case_dir=case_dir,
            budget=budget,
            expected=expected,
            failure_taxon="unbounded_budget",
            message="Case budget must have positive max_steps and time_budget_seconds.",
        )
    if budget.exhausted:
        return _guarded_case_result(
            case=case,
            case_id=case_id,
            case_dir=case_dir,
            budget=budget,
            expected=expected,
            failure_taxon="budget_exhausted",
            message="Deterministic simulated work exceeded the case budget before runner dispatch.",
        )

    fake_report = case.get("fake_report") if isinstance(case.get("fake_report"), Mapping) else {}
    registry = _fixture_registry(fake_report)
    parameters = _case_parameters(case, suite_dir=suite_dir, case_dir=case_dir)
    route = str(case.get("route", "")).strip() or None
    started = time.monotonic()
    try:
        proof_result: ProofRunResult = registry.run(
            ProofRunRequest.from_kwargs(
                repo_root=output_dir,
                route=route,
                request_id=f"proof-stability:{case_id}",
                metadata={
                    "harness_task": "AMRA-PROOF-STABILITY-001",
                    "deterministic_fixture": True,
                },
                **parameters,
            )
        )
        payload = proof_result.to_dict()
        actual_route = proof_result.route
        raw_status = proof_result.raw_status
        canonical_status = proof_result.canonical_status
        failure_taxon = _failure_taxon(raw_status, canonical_status, proof_result.report)
    except Exception as exc:  # pragma: no cover - guarded by regression tests through bad fixtures if needed.
        payload = {"error": str(exc)}
        actual_route = route or ""
        raw_status = "error"
        canonical_status = normalize_proof_status("error")
        failure_taxon = "runner_failure"

    if expected.get("route") and expected["route"] != actual_route:
        failure_taxon = "route_selection_regression"
    mismatches = []
    if expected.get("route") and expected["route"] != actual_route:
        mismatches.append({"field": "route", "expected": expected["route"], "actual": actual_route})
    if expected.get("canonical_status") and expected["canonical_status"] != canonical_status:
        mismatches.append(
            {"field": "canonical_status", "expected": expected["canonical_status"], "actual": canonical_status}
        )
    if expected.get("failure_taxon", "none") != failure_taxon:
        mismatches.append(
            {"field": "failure_taxon", "expected": expected.get("failure_taxon", "none"), "actual": failure_taxon}
        )
    status = "passed" if not mismatches else "failed"
    result = {
        "schema_version": PROOF_STABILITY_CASE_SCHEMA_VERSION,
        "case_id": case_id,
        "case_kind": str(case.get("kind", "unknown")),
        "route": actual_route,
        "status": status,
        "canonical_status": canonical_status,
        "raw_status": raw_status,
        "failure_taxon": failure_taxon,
        "expected": dict(expected),
        "budget": budget.to_dict(),
        "executed": True,
        "llm_calls": 0,
        "live_model_calls": False,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "mismatches": mismatches,
        "proof_loop_result": _json_safe(payload),
    }
    _write_json(case_dir / "result.json", result)
    return result


def _resume_record(
    *,
    suite_id: str,
    case_id: str,
    event: str,
    case_index: int,
    case_count: int,
    result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": PROOF_STABILITY_RESUME_SCHEMA_VERSION,
        "suite_id": suite_id,
        "case_id": case_id,
        "event": event,
        "case_index": case_index,
        "case_count": case_count,
        "next_case_index": min(case_index + 1, case_count),
        "recorded_at": utc_now_iso(),
        "status": result.get("status") if result else "running",
        "canonical_status": result.get("canonical_status") if result else None,
        "failure_taxon": result.get("failure_taxon") if result else None,
        "llm_calls": 0,
    }


def run_proof_stability_benchmark(
    *,
    suite_path: Path,
    output_dir: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Run a bounded, no-live-model proof-loop stability benchmark."""

    suite_path = suite_path.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    suite = load_proof_stability_suite(suite_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    resume_path = output_dir / "proof_stability_resume.jsonl"
    if resume_path.exists():
        resume_path.unlink()

    suite_id = str(suite.get("suite_id", suite_path.stem)).strip() or suite_path.stem
    defaults = suite.get("case_defaults") if isinstance(suite.get("case_defaults"), Mapping) else {}
    budgets = suite.get("budgets") if isinstance(suite.get("budgets"), Mapping) else {}
    max_cases = _positive_int(budgets.get("max_cases"), default=len(suite["cases"]))
    max_total_steps = _positive_int(budgets.get("max_total_steps"), default=100)
    if max_cases <= 0 or max_total_steps <= 0:
        raise ValueError("Suite budgets must define positive max_cases and max_total_steps.")

    selected_cases = suite["cases"][:max_cases]
    case_results: list[dict[str, Any]] = []
    used_steps = 0
    for index, raw_case in enumerate(selected_cases):
        if not isinstance(raw_case, Mapping):
            raise ValueError(f"Proof stability case at index {index} must be a mapping.")
        case_id = _slug(str(raw_case.get("id", f"case-{index + 1}")))
        budget = _case_budget(raw_case, defaults)
        if used_steps + budget.simulated_steps > max_total_steps:
            case_dir = output_dir / "cases" / case_id
            result = _guarded_case_result(
                case=raw_case,
                case_id=case_id,
                case_dir=case_dir,
                budget=budget,
                expected=_expected(raw_case),
                failure_taxon="budget_exhausted",
                message="Suite max_total_steps budget was exhausted before this case.",
            )
        else:
            _append_jsonl(
                resume_path,
                _resume_record(
                    suite_id=suite_id,
                    case_id=case_id,
                    event="case_started",
                    case_index=index,
                    case_count=len(selected_cases),
                ),
            )
            result = _run_case(
                case=raw_case,
                suite_dir=suite_path.parent,
                output_dir=output_dir,
                defaults=defaults,
            )
        used_steps += budget.simulated_steps
        _append_jsonl(
            resume_path,
            _resume_record(
                suite_id=suite_id,
                case_id=case_id,
                event="case_completed",
                case_index=index,
                case_count=len(selected_cases),
                result=result,
            ),
        )
        case_results.append(result)

    route_counts: dict[str, int] = {}
    taxonomy_counts: dict[str, int] = {}
    for result in case_results:
        route_counts[str(result.get("route", ""))] = route_counts.get(str(result.get("route", "")), 0) + 1
        taxon = str(result.get("failure_taxon", "unknown_status"))
        taxonomy_counts[taxon] = taxonomy_counts.get(taxon, 0) + 1

    mixed_case_count = sum(1 for result in case_results if result.get("case_kind") == "mixed")
    failed_cases = [result["case_id"] for result in case_results if result.get("status") != "passed"]
    requirements = suite.get("requirements") if isinstance(suite.get("requirements"), Mapping) else {}
    min_mixed_cases = _positive_int(requirements.get("min_mixed_cases"), default=0)
    requirement_failures = []
    if mixed_case_count < min_mixed_cases:
        requirement_failures.append(
            {
                "requirement": "min_mixed_cases",
                "expected": min_mixed_cases,
                "actual": mixed_case_count,
            }
        )

    status = "passed" if not failed_cases and not requirement_failures else "failed"
    report = {
        "schema_version": PROOF_STABILITY_REPORT_SCHEMA_VERSION,
        "suite_schema_version": suite.get("schema_version"),
        "suite_id": suite_id,
        "status": status,
        "generated_at": utc_now_iso(),
        "repo_root": str(repo_root),
        "suite_path": str(suite_path),
        "output_dir": str(output_dir),
        "resume_records": str(resume_path),
        "case_count": len(case_results),
        "passed_case_count": len([result for result in case_results if result.get("status") == "passed"]),
        "failed_cases": failed_cases,
        "requirement_failures": requirement_failures,
        "route_counts": route_counts,
        "failure_taxonomy": sorted(FAILURE_TAXONOMY),
        "taxonomy_counts": taxonomy_counts,
        "budget": {
            "max_cases": max_cases,
            "max_total_steps": max_total_steps,
            "used_steps": used_steps,
        },
        "mixed_proof_search": {
            "case_count": mixed_case_count,
            "routes": sorted(route for route in route_counts if route in {"proof_search", "closure", "focused_attack"}),
        },
        "llm_calls": 0,
        "live_model_calls": False,
        "cases": case_results,
    }
    _write_json(output_dir / "proof_stability_report.json", report)
    (output_dir / "summary.md").write_text(
        "\n".join(
            [
                "# AMRA Proof Stability Benchmark",
                "",
                f"- Suite: `{suite_id}`",
                f"- Status: `{status}`",
                f"- Cases: {report['passed_case_count']}/{report['case_count']} passed",
                f"- LLM calls: {report['llm_calls']}",
                f"- Resume records: `proof_stability_resume.jsonl`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return report


__all__ = [
    "FAILURE_TAXONOMY",
    "PROOF_STABILITY_CASE_SCHEMA_VERSION",
    "PROOF_STABILITY_REPORT_SCHEMA_VERSION",
    "PROOF_STABILITY_RESUME_SCHEMA_VERSION",
    "PROOF_STABILITY_SUITE_SCHEMA_VERSION",
    "load_proof_stability_suite",
    "run_proof_stability_benchmark",
]
