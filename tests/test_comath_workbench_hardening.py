import json
from pathlib import Path

from ara_math.cli import main
from ara_math.comath_benchmarks import run_local_benchmark_suite
from ara_math.comath_capabilities import refine_intake_project, run_comath_evaluation
from ara_math.comath_source_audit import build_source_query_plan, run_source_audit_loop
from ara_math.coordinator import comath_paths


def test_source_query_plan_uses_goal_terms(tmp_path: Path) -> None:
    project_dir = tmp_path / "query-plan"
    refine_intake_project(
        project_dir,
        goal="Prove a dense block theorem for additive combinatorics.",
        project_name="Query Plan",
    )

    plan = build_source_query_plan(project_dir, rounds=3)

    assert plan["rounds"] == 3
    assert len(plan["queries"]) == 3
    assert any("dense" in query["query"] for query in plan["queries"])
    assert (project_dir / "comath" / "source_audit" / "query_plan.json").exists()


def test_source_audit_loop_persists_inventory_confidence_and_dashboard(tmp_path: Path) -> None:
    project_dir = tmp_path / "source-loop"
    refine_intake_project(project_dir, goal="Prove a source audit loop theorem.", project_name="Source Loop")

    report = run_source_audit_loop(
        project_dir,
        rounds=2,
        backend="fake",
        allow_search=False,
        max_parallel_rounds=2,
        run_name="source-loop-smoke",
    )
    paths = comath_paths(project_dir)
    inventory = json.loads((paths.root / "source_audit" / "source_inventory.json").read_text(encoding="utf-8"))
    confidence = json.loads((paths.root / "source_audit" / "citation_confidence.json").read_text(encoding="utf-8"))
    state = json.loads(paths.project_state.read_text(encoding="utf-8"))
    source_ws = next(item for item in state["workstreams"] if item["workstream_id"] == "source-literature-audit")
    dashboard = paths.dashboard.read_text(encoding="utf-8")

    assert report["executed_rounds"] == 2
    assert len(inventory["items"]) == 2
    assert confidence["max_confidence"] >= confidence["threshold"]
    assert source_ws["metadata"]["latest_source_audit_loop"]["loop_id"] == "source-loop-smoke"
    assert "## Source Audit Loop" in dashboard


def test_local_benchmark_suite_runs_all_fake_regressions(tmp_path: Path) -> None:
    report = run_local_benchmark_suite(tmp_path / "benchmarks", suite_name="hardening-smoke")

    assert report["status"] == "passed"
    assert report["passed"] == report["total"] == 3
    assert (tmp_path / "benchmarks" / "hardening-smoke" / "benchmark_report.json").exists()


def test_hardening_cli_smoke(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "cli-hardening"
    refine_intake_project(project_dir, goal="Prove a hardening CLI theorem.", project_name="CLI Hardening")

    audit_exit = main(
        [
            "--json",
            "run-comath-source-audit-loop",
            "--project",
            str(project_dir),
            "--rounds",
            "1",
            "--backend",
            "fake",
            "--no-search",
            "--run-name",
            "cli-source-audit",
        ]
    )
    audit_payload = json.loads(capsys.readouterr().out)
    bench_exit = main(
        [
            "--json",
            "run-comath-benchmarks",
            "--output-root",
            str(tmp_path / "cli-benchmarks"),
            "--suite-name",
            "cli-hardening-suite",
        ]
    )
    bench_payload = json.loads(capsys.readouterr().out)
    evaluation = run_comath_evaluation(project_dir)
    statuses = {item["capability"]: item["status"] for item in evaluation["report"]["checks"]}

    assert audit_exit == 0
    assert bench_exit == 0
    assert audit_payload["executed_rounds"] == 1
    assert bench_payload["status"] == "passed"
    assert statuses["source_audit_loop"] == "implemented"
    assert statuses["specialist_memory_resume"] == "implemented"
