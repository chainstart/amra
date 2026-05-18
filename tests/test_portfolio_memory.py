import json
from pathlib import Path

import pytest

from amra.portfolio_memory import (
    append_state_transition,
    load_claim_ledger,
    load_failed_routes,
    load_route_ledger,
    record_failed_route,
    render_resume_pack,
    update_global_memory,
    upsert_claim,
    upsert_route,
    write_resume_pack,
)


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_problem_lifecycle_state_history_is_append_only(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "problem-1"

    append_state_transition(project, problem_id="problem-1", state="scouted", reason="first pass")
    state = append_state_transition(
        project,
        problem_id="problem-1",
        state="active_attack",
        reason="promoted",
        evidence=["runs/eval/difficulty.json"],
    )

    history = _jsonl(project / "state_history.jsonl")
    snapshot = json.loads((project / "state.json").read_text(encoding="utf-8"))

    assert snapshot["state"] == "active_attack"
    assert state["previous_state"] == "scouted"
    assert [event["state"] for event in history] == ["scouted", "active_attack"]
    assert [event["sequence"] for event in history] == [1, 2]

    with pytest.raises(ValueError):
        append_state_transition(project, problem_id="problem-1", state="made_up")


def test_claim_ledger_upsert_validates_and_preserves_history(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "problem-claim"
    append_state_transition(project, problem_id="problem-claim", state="scouted")

    first = upsert_claim(
        project,
        {
            "claim_id": "main",
            "kind": "theorem",
            "statement_nl": "Every sample object has the target property.",
            "status": "hypothesis",
            "dependencies": ["lemma-a", "lemma-a"],
            "evidence": [{"type": "source", "path": "problem.yaml"}],
            "proof_evidence": ["proof/sketches/main.md"],
            "reusable": True,
        },
    )
    second = upsert_claim(project, {"claim_id": "main", "status": "route_supported"})
    ledger = load_claim_ledger(project)
    history = _jsonl(project / "memory" / "claim_history.jsonl")

    assert first["dependencies"] == ["lemma-a"]
    assert second["statement_nl"] == "Every sample object has the target property."
    assert second["status"] == "route_supported"
    assert ledger["claims"] == [second]
    assert [event["status"] for event in history] == ["hypothesis", "route_supported"]

    with pytest.raises(ValueError):
        upsert_claim(project, {"claim_id": "bad", "status": "almost_true"})


def test_route_attempt_history_and_failed_route_dedup(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "problem-route"
    append_state_transition(project, problem_id="problem-route", state="active_attack")

    upsert_route(
        project,
        {
            "route_id": "induction-route",
            "target_claim": "main",
            "core_idea": "Induct on the extremal cell.",
            "status": "promising",
            "attempt": {"attempt_id": "attempt-1", "run_dir": "runs/attempt-1"},
        },
    )
    route = upsert_route(
        project,
        {
            "route_id": "induction-route",
            "status": "blocked",
            "blocker": "Boundary case remains open.",
            "attempt": {"attempt_id": "attempt-2", "run_dir": "runs/attempt-2"},
            "evaluator_verdict": {"verdict": "continue", "confidence": 0.6},
        },
    )

    failed = record_failed_route(
        project,
        {
            "route_id": "induction-route",
            "failed_assertion": "The boundary case follows from the same invariant.",
            "approach": "Reuse the interior invariant at the boundary.",
            "failure_mode": "proof_gap",
            "evidence_path": "runs/attempt-2/blocker.md",
            "resume_condition": "A separate boundary invariant is found.",
        },
    )
    deduped = record_failed_route(
        project,
        {
            "route_id": "induction-route",
            "failed_assertion": "The boundary case follows from the same invariant.",
            "approach": "Reuse the interior invariant at the boundary.",
            "failure_mode": "proof_gap",
            "evidence_path": "runs/attempt-3/blocker.md",
            "resume_condition": "A separate boundary invariant is found.",
        },
    )

    assert len(route["attempt_history"]) == 2
    assert route["blocker"] == "Boundary case remains open."
    assert route["evaluator_verdict"]["verdict"] == "continue"
    assert failed["fingerprint"] == deduped["fingerprint"]
    assert load_failed_routes(project)["failed_routes"] == [deduped]
    assert deduped["evidence_paths"] == ["runs/attempt-2/blocker.md", "runs/attempt-3/blocker.md"]

    with pytest.raises(ValueError):
        record_failed_route(project, {"route_id": "x", "failure_mode": "unclassified"})


def test_global_indexes_merge_multiple_projects_without_overwriting(tmp_path: Path) -> None:
    repo = tmp_path
    project_a = tmp_path / "projects" / "problem-a"
    project_b = tmp_path / "projects" / "problem-b"

    append_state_transition(project_a, problem_id="problem-a", state="scouted")
    upsert_claim(project_a, {"claim_id": "main-a", "statement_nl": "A", "status": "hypothesis"})
    upsert_route(project_a, {"route_id": "route-a", "target_claim": "main-a", "status": "new"})
    update_global_memory(repo, project_dir=project_a, problem_id="problem-a")

    append_state_transition(project_b, problem_id="problem-b", state="active_attack")
    upsert_claim(project_b, {"claim_id": "main-b", "statement_nl": "B", "status": "lean_verified"})
    upsert_route(project_b, {"route_id": "route-b", "target_claim": "main-b", "status": "completed"})
    record_failed_route(project_b, {"route_id": "route-b", "failure_mode": "resource_timeout"})
    update_global_memory(repo, project_dir=project_b, problem_id="problem-b")

    append_state_transition(project_a, problem_id="problem-a", state="formalization_ready")
    update_global_memory(repo, project_dir=project_a, problem_id="problem-a")

    global_root = repo / "artifacts" / "global_memory"
    problem_index = json.loads((global_root / "problem_index.json").read_text(encoding="utf-8"))
    claim_index = json.loads((global_root / "claim_index.json").read_text(encoding="utf-8"))
    failed_index = json.loads((global_root / "failed_route_index.json").read_text(encoding="utf-8"))
    theorem_index = json.loads((global_root / "theorem_asset_index.json").read_text(encoding="utf-8"))
    difficulty_history = _jsonl(global_root / "difficulty_history.jsonl")

    assert {item["problem_id"] for item in problem_index["problems"]} == {"problem-a", "problem-b"}
    assert {item["claim_id"] for item in claim_index["claims"]} == {"main-a", "main-b"}
    assert [item["route_id"] for item in theorem_index["routes"]] == ["route-a", "route-b"]
    assert [item["claim_id"] for item in theorem_index["verified_claims"]] == ["main-b"]
    assert len(failed_index["failed_routes"]) == 1
    assert [item["problem_id"] for item in difficulty_history] == ["problem-a", "problem-b", "problem-a"]


def test_resume_pack_markdown_is_stable_and_includes_failed_route_guard(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "resume-problem"
    append_state_transition(project, problem_id="resume-problem", state="active_attack", reason="unit test")
    upsert_claim(
        project,
        {
            "claim_id": "main",
            "statement_nl": "The main claim.",
            "status": "route_supported",
            "dependencies": ["helper"],
        },
    )
    upsert_route(
        project,
        {
            "route_id": "route-main",
            "target_claim": "main",
            "status": "blocked",
            "blocker": "Needs a sharper invariant.",
            "attempt": {"attempt_id": "attempt-1"},
        },
    )
    record_failed_route(
        project,
        {
            "route_id": "route-main",
            "failure_mode": "modeling_too_weak",
            "approach": "A weak invariant.",
            "resume_condition": "A stronger invariant is available.",
        },
    )

    first = write_resume_pack(project, problem_id="resume-problem")
    content = render_resume_pack(project, problem_id="resume-problem")
    second = write_resume_pack(project, problem_id="resume-problem")

    assert first["path"] == second["path"]
    assert content == (project / "resume_pack.md").read_text(encoding="utf-8")
    assert "Do not repeat this route unless the resume condition is met." in content
    assert "A stronger invariant is available." in content
    assert "route_supported" in content
