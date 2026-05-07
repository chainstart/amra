from __future__ import annotations

from pathlib import Path

from ara_math.campaign_loop import CampaignLoopRunner, extract_first_theorem_name


def _write_workspace(tmp_path: Path, body: str) -> Path:
    workspace = tmp_path / "formal"
    (workspace / "MathProject").mkdir(parents=True)
    (workspace / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject\n", encoding="utf-8")
    (workspace / "MathProject" / "MainClaim.lean").write_text(body, encoding="utf-8")
    return workspace


def test_extract_first_theorem_name_from_markdown() -> None:
    text = """
Formalization target:
```lean
theorem erdos866_g6_lower_from_prime_sidon
    (n p : ℕ) : True := by
  trivial
```
"""

    assert extract_first_theorem_name(text) == "erdos866_g6_lower_from_prime_sidon"


def test_campaign_loop_proof_lab_only_backend_none(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    report = runner.run(
        statement="Prove a theorem-level route.",
        backend="none",
        mode="proof-lab",
        rounds=2,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        output_root=tmp_path / "loops",
        run_name="proof-loop",
    )

    assert report["status"] == "partial"
    assert report["rounds_completed"] == 2
    assert [round_entry["stage"] for round_entry in report["rounds"]] == ["proof_lab", "proof_lab"]
    assert Path(report["summary_path"]).exists()
    first_goal = Path(report["run_dir"]) / "rounds" / "round_001" / "stage_goal.md"
    assert "Loop Discipline" in first_goal.read_text(encoding="utf-8")


def test_campaign_loop_stops_when_final_target_verified(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem final_target : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = CampaignLoopRunner(repo_root=tmp_path)

    report = runner.run(
        statement="Prove final_target.",
        workspace=workspace,
        final_target_theorem="final_target",
        initial_target_theorem="final_target",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=["python3", "-c", "print('mock build passed')"],
        backend="none",
        mode="lean-formalizer",
        rounds=3,
        time_budget_sec=120,
        output_root=tmp_path / "loops",
        run_name="verified-loop",
    )

    assert report["status"] == "verified"
    assert report["stop_reason"] == "final_target_verified"
    assert report["rounds_completed"] == 1
    assert report["rounds"][0]["stage"] == "lean_formalizer"
