import json
from pathlib import Path

from ara_math.comath_runners import (
    ClosureWorkstreamExecutor,
    SourceLiteratureWorkstreamExecutor,
    execute_workstream,
)
from ara_math.coordinator import add_workstream, comath_paths, initialize_comath_project
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord, WorkstreamStatus


def _pass_command() -> list[str]:
    return ["python3", "-c", "print('mock lean build passed')"]


def _write_clean_workspace(project_dir: Path) -> Path:
    workspace = project_dir / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem comath_runner_target : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return workspace


def test_proof_strategy_executor_persists_run_state_and_artifacts(tmp_path: Path) -> None:
    project_dir = tmp_path / "proof-project"
    initialize_comath_project(project_dir, project_name="Proof", original_goal="Prove the proof wrapper theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Find a proof strategy.",
        ),
    )

    payload = execute_workstream(
        project_dir,
        "proof-main",
        options={"backend": "none", "attempts": 1, "audits": 0, "run_name": "proof-smoke"},
    )
    paths = comath_paths(project_dir)
    status = json.loads((paths.workstream_dir("proof-main") / "status.json").read_text(encoding="utf-8"))
    state = json.loads(paths.project_state.read_text(encoding="utf-8"))
    workstream = state["workstreams"][0]

    assert payload["result"]["executor"] == "proof_strategy"
    assert status["status"] == WorkstreamStatus.NEEDS_REVIEW.value
    assert Path(workstream["run_dirs"][0]).joinpath("report.json").exists()
    assert any(path.endswith("summary.md") for path in workstream["artifact_paths"])
    assert workstream["metadata"]["latest_runner"]["status"] == "completed"
    assert (paths.workstream_dir("proof-main") / "run_history.jsonl").exists()


def test_lean_formalization_executor_wraps_existing_formalizer(tmp_path: Path) -> None:
    project_dir = tmp_path / "lean-project"
    workspace = _write_clean_workspace(project_dir)
    initialize_comath_project(project_dir, project_name="Lean", original_goal="Prove the Lean wrapper theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="lean-main",
            kind=WorkstreamKind.LEAN,
            goal="Formalize the main theorem.",
        ),
    )

    payload = execute_workstream(
        project_dir,
        "lean-main",
        options={
            "workspace": workspace,
            "target_theorem": "comath_runner_target",
            "target_file": Path("MathProject/MainClaim.lean"),
            "build_command": _pass_command(),
            "backend": "none",
            "attempts": 2,
            "run_name": "lean-smoke",
        },
    )
    workstream = payload["workstream"]

    assert payload["result"]["executor"] == "lean_formalization"
    assert payload["result"]["status"] == "verified"
    assert workstream["status"] == WorkstreamStatus.NEEDS_REVIEW.value
    assert Path(workstream["run_dirs"][0]).joinpath("report.json").exists()
    assert any(path.endswith("initial_audit.json") for path in workstream["artifact_paths"])
    assert workstream["blockers"] == []


class FakeClosureOrchestrator:
    def run_closure_prover(self, *, project_dir: Path, target_theorem: str | None, **_: object) -> dict[str, object]:
        run_dir = project_dir / "proof" / "closure_prover"
        run_dir.mkdir(parents=True)
        status_path = run_dir / "closure_status.json"
        payload = {
            "status": "blocked",
            "target_theorem": target_theorem or "",
            "best_audit": {"blockers": ["Target theorem still contains `sorry`."]},
        }
        status_path.write_text(json.dumps(payload), encoding="utf-8")
        return payload


def test_closure_executor_records_blockers_from_existing_runner_payload(tmp_path: Path) -> None:
    project_dir = tmp_path / "closure-project"
    initialize_comath_project(project_dir, project_name="Closure", original_goal="Close the Lean theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="closure-main",
            kind=WorkstreamKind.COMPUTE,
            goal="Close the target theorem.",
            metadata={"executor": "closure", "target_theorem": "target"},
        ),
    )

    payload = execute_workstream(
        project_dir,
        "closure-main",
        executor=ClosureWorkstreamExecutor(orchestrator=FakeClosureOrchestrator()),
    )
    workstream = payload["workstream"]

    assert payload["result"]["executor"] == "closure"
    assert workstream["status"] == WorkstreamStatus.REVISION.value
    assert any("Target theorem still contains `sorry`." in blocker for blocker in workstream["blockers"])
    assert any(path.endswith("closure_status.json") for path in workstream["artifact_paths"])


class FakeSourceHarvester:
    def harvest(self, *, project_dir: Path, **_: object) -> dict[str, object]:
        evidence_path = project_dir / "idea" / "literature_evidence.json"
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence = {
            "counts": {"known_results": 1, "proof_ingredients": 0, "modern_tools": 0, "open_gaps": 0},
            "source_attribution_count": 1,
            "sources": ["local-note"],
            "known_results": [],
            "proof_ingredients": [],
            "modern_tools": [],
            "open_gaps": [],
        }
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        return {
            "status": "completed",
            "source_count": 1,
            "snapshot_count": 1,
            "recovered_statement": {"status": "candidate_found_existing_statement_kept"},
            "evidence": evidence,
        }


def test_source_literature_executor_writes_run_directory_and_source_artifacts(tmp_path: Path) -> None:
    project_dir = tmp_path / "source-project"
    initialize_comath_project(project_dir, project_name="Source", original_goal="Source-check the theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Check source grounding.",
        ),
    )

    payload = execute_workstream(
        project_dir,
        "source-main",
        executor=SourceLiteratureWorkstreamExecutor(harvester=FakeSourceHarvester()),
        options={"run_name": "source-smoke"},
    )
    workstream = payload["workstream"]

    assert payload["result"]["executor"] == "source_literature"
    assert workstream["status"] == WorkstreamStatus.NEEDS_REVIEW.value
    assert Path(workstream["run_dirs"][0]).joinpath("report.json").exists()
    assert any(path.endswith("literature_evidence.json") for path in workstream["artifact_paths"])
    assert workstream["blockers"] == []
