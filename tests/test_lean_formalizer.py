from __future__ import annotations

from pathlib import Path

from ara_math.lean_formalizer import LeanFormalizerRunner, collect_proof_lab_context_paths


def _write_workspace(tmp_path: Path, body: str) -> Path:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(body, encoding="utf-8")
    return workspace


def _pass_command() -> list[str]:
    return ["python3", "-c", "print('mock lean build passed')"]


def test_lean_formalizer_verifies_clean_workspace(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem h5upper_log : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove h5upper_log.",
        target_theorem="h5upper_log",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=3,
        output_root=tmp_path / "runs",
        run_name="clean",
    )

    assert report["status"] == "verified"
    assert report["stop_reason"] == "verified_initially"
    assert report["attempts_completed"] == 0
    assert report["best_audit"]["verified"] is True
    assert Path(report["summary_path"]).exists()


def test_lean_formalizer_accepts_multiline_target_declaration(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem h5upper_log",
                "    : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove h5upper_log.",
        target_theorem="h5upper_log",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=1,
        output_root=tmp_path / "runs",
        run_name="multiline",
    )

    assert report["status"] == "verified"
    assert report["best_audit"]["target"]["line"] == 3


def test_lean_formalizer_runs_backend_iterations_when_unverified(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem h5upper_log : True := by",
                "  sorry",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove h5upper_log.",
        target_theorem="h5upper_log",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=2,
        output_root=tmp_path / "runs",
        run_name="unfinished",
    )

    assert report["status"] == "partial"
    assert report["stop_reason"] == "attempts_exhausted"
    assert report["attempts_completed"] == 2
    assert report["best_audit"]["counts"]["sorry"] == 1
    first_attempt = Path(report["run_dir"]) / "attempts" / "attempt_001" / "prompt.txt"
    prompt = first_attempt.read_text(encoding="utf-8")
    assert "write-and-verify stage downstream of ARA Proof Lab" in prompt
    assert "Required verifier command" in prompt
    assert "Each iteration must evaluate the previous state" in prompt


def test_lean_formalizer_can_stop_on_explicit_stall_guard(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem h5upper_log : True := by",
                "  sorry",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove h5upper_log.",
        target_theorem="h5upper_log",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=4,
        max_stalled_attempts=1,
        output_root=tmp_path / "runs",
        run_name="stall",
    )

    assert report["status"] == "partial"
    assert report["stop_reason"] == "stalled"
    assert report["attempts_completed"] == 1


def test_lean_formalizer_reports_global_reassessment_after_no_progress(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem unrelated_helper : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove missing_target.",
        target_theorem="missing_target",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=2,
        output_root=tmp_path / "runs",
        run_name="missing-target",
    )

    assert report["status"] == "partial"
    assert report["needs_global_reassessment"] is True
    assert report["suggested_next_targets"] == ["rerun with backend=codex"]
    summary = Path(report["summary_path"]).read_text(encoding="utf-8")
    assert "Global Reassessment" in summary
    assert "Run a global reassessment" in report["next_action"]


def test_collect_proof_lab_context_paths_prefers_high_signal_outputs(tmp_path: Path) -> None:
    run_dir = tmp_path / "proof_lab_run"
    (run_dir / "grounding").mkdir(parents=True)
    (run_dir / "attempts").mkdir(parents=True)
    (run_dir / "audits").mkdir(parents=True)
    (run_dir / "summary.md").write_text("summary", encoding="utf-8")
    (run_dir / "manual_summary.md").write_text("manual", encoding="utf-8")
    (run_dir / "grounding" / "source_grounding_output.md").write_text("grounding", encoding="utf-8")
    (run_dir / "attempts" / "attempt_001_output.md").write_text("attempt", encoding="utf-8")
    (run_dir / "audits" / "audit_attempt_001_output.md").write_text("audit", encoding="utf-8")

    paths = collect_proof_lab_context_paths(run_dir)
    names = [path.name for path in paths]

    assert "summary.md" in names
    assert "manual_summary.md" in names
    assert "source_grounding_output.md" in names
    assert "attempt_001_output.md" in names
    assert "audit_attempt_001_output.md" in names


def test_lean_formalizer_uses_isolated_workspace_and_reports_velocity(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "formal-problem"
    workspace = project / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem h5upper_log : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runner = LeanFormalizerRunner(repo_root=tmp_path)

    report = runner.run(
        workspace=workspace,
        statement="Prove h5upper_log.",
        target_theorem="h5upper_log",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=_pass_command(),
        backend="none",
        attempts=1,
        output_root=tmp_path / "runs",
        run_name="isolated-formalizer",
        project_dir=project,
        problem_id="formal-problem",
        workspace_run_id="run-a",
        use_isolated_workspace=True,
        merge_to_canonical=True,
        review_status="approved",
    )

    assert report["status"] == "verified"
    assert report["workspace_isolated"] is True
    assert Path(report["workspace"]) == project / "workspaces" / "run-a" / "formal"
    assert report["canonical_workspace"] == str(workspace.resolve())
    assert report["formal_workspace_merge"]["merged"] is True
    assert report["progress_velocity"]["schema_version"] == "amra.progress_velocity.v1"
    summary = Path(report["summary_path"]).read_text(encoding="utf-8")
    assert "Progress Velocity" in summary
