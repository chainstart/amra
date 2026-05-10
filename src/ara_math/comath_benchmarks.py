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
