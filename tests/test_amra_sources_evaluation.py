from __future__ import annotations

import importlib
import json
from pathlib import Path

from amra.evaluation.capabilities import refine_intake_project
from amra.evaluation.evaluator import EvaluatorPlanner
from amra.evaluation.specialists import run_specialist
from amra.problem_banks.sync import _build_local_topic_banks
from amra.scheduler.obligations import candidates_from_specialist_output
from amra.sources.literature import LiteratureHarvester
from amra.sources.source_audit import build_source_query_plan, run_source_audit_loop


def test_sources_evaluation_legacy_modules_alias_canonical_identity() -> None:
    migrated = {
        "ara_math.literature": "amra.sources.literature",
        "ara_math.comath_source_audit": "amra.sources.source_audit",
        "ara_math.comath_capabilities": "amra.evaluation.capabilities",
        "ara_math.comath_specialists": "amra.evaluation.specialists",
        "ara_math.comath_benchmarks": "amra.evaluation.benchmarks",
        "ara_math.evaluator": "amra.evaluation.evaluator",
        "ara_math.obligation_refiner": "amra.scheduler.obligations",
        "ara_math.scouting": "amra.evaluation.scouting",
        "ara_math.strategy": "amra.evaluation.strategy",
        "ara_math.convergence": "amra.evaluation.convergence",
        "ara_math.banking": "amra.problem_banks.sync",
    }

    for legacy_name, canonical_name in migrated.items():
        assert importlib.import_module(legacy_name) is importlib.import_module(canonical_name)


def test_canonical_source_audit_loop_uses_local_fake_provider(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    refine_intake_project(
        project_dir,
        goal="Prove that every integer equals itself.",
        project_name="Source Audit Local",
    )

    plan = build_source_query_plan(project_dir, rounds=2, seed_terms=["integer", "reflexivity"])
    report = run_source_audit_loop(
        project_dir,
        rounds=2,
        backend="fake",
        allow_search=False,
        max_parallel_rounds=2,
        run_name="local-source-audit",
        seed_terms=["integer", "reflexivity"],
    )

    assert plan["rounds"] == 2
    assert report["executed_rounds"] == 2
    assert report["allow_search"] is False
    assert report["source_quality"]["source_count"] == 2
    assert Path(report["source_inventory_path"]).exists()
    assert json.loads(Path(report["citation_confidence_path"]).read_text(encoding="utf-8"))["max_confidence"] >= 0.65


def test_specialist_obligation_and_evaluator_policy_are_canonical(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    refine_intake_project(project_dir, goal="Prove the local benchmark theorem.", project_name="Canonical Evaluation")

    specialist = run_specialist(
        project_dir,
        role_id="source_auditor",
        workstream_id="source-literature-audit",
        backend="fake",
        allow_search=False,
        run_name="canonical-specialist",
        resume_memory=False,
    )
    parsed = specialist["result"]["parsed_output"]
    candidates = candidates_from_specialist_output(
        {
            "fields": {"next_actions": "Audit source theorem statement and record exact hypotheses."},
            "blockers": ["Missing primary source theorem statement."],
        },
        source_role_id="source_auditor",
    )

    plan = EvaluatorPlanner().build_plan(
        manifest={
            "project_name": "Canonical Evaluation",
            "problem": {"problem_id": "local", "tags": ["computational_search"]},
        },
        seed_family="weird_numbers",
        route_scaffold={"first_edit_targets": ["proof/checkpoint.md"]},
        checkpoint_contract={"checkpoint_statement": "Bounded checkpoint"},
        script_inventory=[{"name": "probe.py", "path": str(tmp_path / "probe.py"), "source_root": str(tmp_path)}],
        counterexample_contract={"search_contract": "Search n <= 10.", "auto_run_allowed": False},
    )

    assert candidates
    assert parsed["fields"]["summary"]
    assert plan["evaluator_mode"] == "script_backed_search"
    assert plan["ready_to_run"] is True
    assert plan["auto_run_allowed"] is False


def test_canonical_literature_and_banking_helpers_are_local(tmp_path: Path) -> None:
    note = tmp_path / "local_source.md"
    note.write_text("**Problem Statement**: Prove that every integer n satisfies n = n.\n", encoding="utf-8")
    harvester = LiteratureHarvester()
    snippets = harvester._extract_theorem_snippets("Theorem 1. Every integer n satisfies n = n.\n")
    banks = _build_local_topic_banks(tmp_path)

    assert snippets[0]["kind"] == "theorem"
    assert "unitary_perfect_track" in banks
    assert banks["unitary_perfect_track"]["problems"]
    assert all(problem.metadata.get("statement_quality") for problem in banks["unitary_perfect_track"]["problems"])
