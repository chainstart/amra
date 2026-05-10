from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from ara_math.comath_capabilities import create_computation_certificate, refine_intake_project, run_comath_evaluation
from ara_math.comath_source_audit import run_source_audit_loop
from ara_math.comath_specialists import load_specialist_memory, run_specialist
from ara_math.workspace import slugify, write_json, write_text
from ara_math.workstreams import utc_now_iso


@dataclass(slots=True)
class BenchmarkResult:
    benchmark_id: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "benchmark_id": self.benchmark_id,
            "status": self.status,
            "details": dict(self.details),
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class MinimalMathProblem:
    problem_id: str
    title: str
    statement: str
    expected_term_groups: tuple[tuple[str, ...], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "title": self.title,
            "statement": self.statement,
            "expected_term_groups": [list(group) for group in self.expected_term_groups],
        }


MINIMAL_REAL_MATH_PROBLEMS: tuple[MinimalMathProblem, ...] = (
    MinimalMathProblem(
        problem_id="sqrt2-irrational",
        title="Irrationality of sqrt(2)",
        statement="Prove that sqrt(2) is irrational.",
        expected_term_groups=(
            ("irrational",),
            ("contradiction", "contradict"),
            ("even",),
        ),
    ),
    MinimalMathProblem(
        problem_id="sum-odd-squares",
        title="Sum of Odd Numbers",
        statement="Prove that 1 + 3 + ... + (2n - 1) = n^2 for every positive integer n.",
        expected_term_groups=(
            ("induction", "inductive"),
            ("n^2", "square"),
            ("odd", "2n - 1", "2n+1"),
        ),
    ),
    MinimalMathProblem(
        problem_id="infinitely-many-primes",
        title="Infinitely Many Primes",
        statement="Prove that there are infinitely many prime numbers.",
        expected_term_groups=(
            ("prime", "primes"),
            ("euclid", "product"),
            ("contradiction", "divides", "remainder"),
        ),
    ),
)


def _run_case(benchmark_id: str, func: Callable[[], dict[str, Any]]) -> BenchmarkResult:
    try:
        details = func()
    except Exception as exc:  # pragma: no cover - exercised by callers as failure data
        return BenchmarkResult(
            benchmark_id=benchmark_id,
            status="failed",
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        )
    return BenchmarkResult(benchmark_id=benchmark_id, status="passed", details=details)


def _matched_term_groups(text: str, groups: tuple[tuple[str, ...], ...]) -> tuple[list[list[str]], list[list[str]]]:
    normalized = text.lower()
    matched: list[list[str]] = []
    missing: list[list[str]] = []
    for group in groups:
        terms = [term.lower() for term in group]
        if any(term in normalized for term in terms):
            matched.append(list(group))
        else:
            missing.append(list(group))
    return matched, missing


def _benchmark_minimal_math_problem(
    project_root: Path,
    problem: MinimalMathProblem,
    *,
    backend: str,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int,
) -> BenchmarkResult:
    project_dir = project_root / problem.problem_id
    refine_intake_project(
        project_dir,
        goal=f"Minimal real math benchmark. {problem.statement}",
        project_name=problem.title,
    )
    statement_path = project_dir / "problem_statement.md"
    write_text(
        statement_path,
        "\n".join(
            [
                f"# {problem.title}",
                "",
                problem.statement,
                "",
                "Benchmark scope: produce an informal but complete elementary proof. "
                "Lean and literature evidence are not required for this benchmark.",
                "",
            ]
        ),
    )
    payload = run_specialist(
        project_dir,
        role_id="ideation_specialist",
        workstream_id="ideation-route-discovery",
        backend=backend,
        model=model,
        reasoning_effort=reasoning_effort,
        timeout_seconds=timeout_seconds,
        allow_search=False,
        run_name=f"{problem.problem_id}-minimal-real-proof",
        task=(
            "Solve this minimal benchmark problem. Give a complete elementary proof route and a concise proof. "
            "This benchmark does not require Lean formalization or literature search; "
            "mark those as not applicable, not blockers.\n\n"
            f"Problem: {problem.statement}"
        ),
        context_files=[statement_path],
        resume_memory=False,
    )
    output_path = Path(payload["output_path"])
    output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    parsed_output = payload.get("result", {}).get("parsed_output", {})
    parsed_fields = parsed_output.get("fields", {})
    required_fields = {"summary", "claims", "evidence", "blockers", "next_actions"}
    missing_fields = sorted(required_fields - set(parsed_fields))
    matched_groups, missing_groups = _matched_term_groups(output, problem.expected_term_groups)
    provider_status = str(payload.get("provider", {}).get("status", ""))
    passed = provider_status == "completed" and not missing_fields and not missing_groups
    return BenchmarkResult(
        benchmark_id=problem.problem_id,
        status="passed" if passed else "failed",
        details={
            "project_dir": str(project_dir),
            "statement": problem.statement,
            "provider_status": provider_status,
            "parsed_status": parsed_output.get("status", ""),
            "prompt_path": payload.get("prompt_path", ""),
            "output_path": payload.get("output_path", ""),
            "result_path": str(
                project_dir
                / "comath"
                / "specialists"
                / "ideation_specialist"
                / "runs"
                / payload["run_id"]
                / "result.json"
            ),
            "has_required_fields": not missing_fields,
            "missing_fields": missing_fields,
            "matched_term_groups": matched_groups,
            "missing_term_groups": missing_groups,
            "output_chars": len(output),
        },
    )


def _benchmark_specialist_memory(project_root: Path) -> dict[str, Any]:
    project_dir = project_root / "specialist-memory"
    refine_intake_project(project_dir, goal="Prove the memory benchmark theorem.", project_name="Memory Benchmark")
    first = run_specialist(
        project_dir,
        role_id="theory_builder",
        workstream_id="theory-building-memory",
        backend="fake",
        run_name="memory-round-1",
    )
    second = run_specialist(
        project_dir,
        role_id="theory_builder",
        workstream_id="theory-building-memory",
        backend="fake",
        run_name="memory-round-2",
    )
    memory = load_specialist_memory(project_dir, "theory_builder")
    prompt = Path(second["prompt_path"]).read_text(encoding="utf-8")
    assert memory["run_count"] == 2
    assert "Previous specialist memory" in prompt
    assert "memory-round-1" in prompt
    return {
        "project_dir": str(project_dir),
        "first_run": first["run_id"],
        "second_run": second["run_id"],
        "memory_path": str(project_dir / "comath" / "specialists" / "theory_builder" / "conversation_state.json"),
    }


def _benchmark_source_audit_loop(project_root: Path) -> dict[str, Any]:
    project_dir = project_root / "source-audit-loop"
    refine_intake_project(project_dir, goal="Prove the source audit benchmark theorem.", project_name="Source Audit Benchmark")
    report = run_source_audit_loop(
        project_dir,
        rounds=2,
        backend="fake",
        allow_search=False,
        max_parallel_rounds=2,
        run_name="source-audit-benchmark",
    )
    assert report["executed_rounds"] == 2
    assert Path(report["source_inventory_path"]).exists()
    assert Path(report["citation_confidence_path"]).exists()
    return {
        "project_dir": str(project_dir),
        "report_path": str(project_dir / "comath" / "source_audit" / "report.json"),
        "max_confidence": report["confidence"]["max_confidence"],
    }


def _benchmark_capability_evaluation(project_root: Path) -> dict[str, Any]:
    project_dir = project_root / "capability-evaluation"
    refine_intake_project(project_dir, goal="Prove the evaluation benchmark theorem.", project_name="Evaluation Benchmark")
    run_specialist(
        project_dir,
        role_id="source_auditor",
        workstream_id="source-literature-audit",
        backend="fake",
        run_name="evaluation-source-specialist",
    )
    run_source_audit_loop(project_dir, rounds=1, backend="fake", allow_search=False, run_name="evaluation-source-loop")
    create_computation_certificate(
        project_dir,
        workstream_id="computation-exploration",
        command=["python3", "-c", "print('benchmark certificate')"],
        cwd=project_dir,
        seed="benchmark",
    )
    evaluation = run_comath_evaluation(project_dir)
    statuses = {item["capability"]: item["status"] for item in evaluation["report"]["checks"]}
    assert statuses["llm_specialist_orchestration"] == "implemented"
    assert statuses["specialist_memory_resume"] == "implemented"
    assert statuses["source_audit_loop"] == "implemented"
    assert statuses["local_benchmark_harness"] in {"partial", "implemented"}
    return {
        "project_dir": str(project_dir),
        "evaluation_path": evaluation["evaluation_path"],
        "statuses": statuses,
    }


def run_local_benchmark_suite(
    output_root: Path,
    *,
    suite_name: str = "comath-local-smoke",
) -> dict[str, Any]:
    output_root = Path(output_root)
    suite_id = slugify(suite_name)
    suite_dir = output_root / suite_id
    project_root = suite_dir / "projects"
    project_root.mkdir(parents=True, exist_ok=True)
    benchmarks = [
        _run_case("specialist_memory_resume", lambda: _benchmark_specialist_memory(project_root)),
        _run_case("source_audit_loop", lambda: _benchmark_source_audit_loop(project_root)),
        _run_case("capability_evaluation", lambda: _benchmark_capability_evaluation(project_root)),
    ]
    passed = sum(1 for item in benchmarks if item.status == "passed")
    report = {
        "suite_id": suite_id,
        "generated_at": utc_now_iso(),
        "output_root": str(output_root),
        "suite_dir": str(suite_dir),
        "status": "passed" if passed == len(benchmarks) else "failed",
        "passed": passed,
        "total": len(benchmarks),
        "benchmarks": [item.to_dict() for item in benchmarks],
    }
    write_json(suite_dir / "benchmark_report.json", report)
    write_text(
        suite_dir / "benchmark_report.md",
        "\n".join(
            [
                f"# CoMath Local Benchmark Suite: {suite_id}",
                "",
                f"- Status: `{report['status']}`",
                f"- Passed: `{passed}/{len(benchmarks)}`",
                "",
                "| Benchmark | Status |",
                "| --- | --- |",
                *[f"| {item.benchmark_id} | {item.status} |" for item in benchmarks],
                "",
            ]
        ),
    )
    return report


def run_minimal_real_math_benchmark(
    output_root: Path,
    *,
    suite_name: str = "minimal-math-real",
    backend: str = "codex",
    model: str = "",
    reasoning_effort: str = "medium",
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    output_root = Path(output_root)
    suite_id = slugify(suite_name)
    suite_dir = output_root / suite_id
    project_root = suite_dir / "projects"
    project_root.mkdir(parents=True, exist_ok=True)
    write_json(
        suite_dir / "problem_set.json",
        {"problems": [problem.to_dict() for problem in MINIMAL_REAL_MATH_PROBLEMS]},
    )
    benchmarks = [
        _benchmark_minimal_math_problem(
            project_root,
            problem,
            backend=backend,
            model=model,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
        )
        for problem in MINIMAL_REAL_MATH_PROBLEMS
    ]
    passed = sum(1 for item in benchmarks if item.status == "passed")
    report = {
        "suite_id": suite_id,
        "generated_at": utc_now_iso(),
        "output_root": str(output_root),
        "suite_dir": str(suite_dir),
        "backend": backend,
        "model": model or "codex_config_default",
        "reasoning_effort": reasoning_effort or "codex_config_default",
        "timeout_seconds": timeout_seconds,
        "problem_set_path": str(suite_dir / "problem_set.json"),
        "status": "passed" if passed == len(benchmarks) else "failed",
        "passed": passed,
        "total": len(benchmarks),
        "benchmarks": [item.to_dict() for item in benchmarks],
    }
    write_json(suite_dir / "benchmark_report.json", report)
    write_text(
        suite_dir / "benchmark_report.md",
        "\n".join(
            [
                f"# Minimal Real Math Benchmark: {suite_id}",
                "",
                f"- Status: `{report['status']}`",
                f"- Backend: `{backend}`",
                f"- Model: `{report['model']}`",
                f"- Reasoning effort: `{report['reasoning_effort']}`",
                f"- Passed: `{passed}/{len(benchmarks)}`",
                "",
                "| Problem | Status | Provider | Output |",
                "| --- | --- | --- | --- |",
                *[
                    (
                        f"| {item.benchmark_id} | {item.status} | "
                        f"{item.details.get('provider_status', '')} | {item.details.get('output_path', '')} |"
                    )
                    for item in benchmarks
                ],
                "",
            ]
        ),
    )
    return report
