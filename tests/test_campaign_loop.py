from __future__ import annotations

from pathlib import Path

from ara_math.campaign_loop import (
    CampaignLoopRunner,
    extract_first_theorem_name,
    extract_formalization_target_from_run,
)
from ara_math.workspace import write_json


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


def test_extract_first_theorem_name_ignores_prose_theorem_is() -> None:
    text = """
The theorem is mathematically viable. The next formalizer should target exactly
the following theorem-level statement:

```lean
theorem finite_sidon_sqrt_lower :
    True := by
  trivial
```
"""

    assert extract_first_theorem_name(text) == "finite_sidon_sqrt_lower"


def test_extract_formalization_target_prefers_structured_open_target(tmp_path: Path) -> None:
    run_dir = tmp_path / "proof_lab"
    run_dir.mkdir()
    write_json(
        run_dir / "report.json",
        {
            "grounding": {
                "parsed_fields": {
                    "open_continuation_target": "\n".join(
                        [
                            "The exact unsolved node is:",
                            "```lean",
                            "theorem finite_sidon_sqrt_lower :",
                            "    True := by",
                            "  trivial",
                            "```",
                        ]
                    ),
                    "recommended_attack_target": "Next round should prove `finite_sidon_sqrt_lower`.",
                }
            },
            "attempts": [
                {
                    "attempt": 1,
                    "parsed_fields": {
                        "formalization_target": "\n".join(
                            [
                                "```lean",
                                "theorem stale_completed_target : True := by",
                                "  trivial",
                                "```",
                            ]
                        )
                    },
                }
            ],
        },
    )

    assert extract_formalization_target_from_run(run_dir) == "finite_sidon_sqrt_lower"


def test_extract_formalization_target_skips_completed_names(tmp_path: Path) -> None:
    run_dir = tmp_path / "proof_lab"
    run_dir.mkdir()
    write_json(
        run_dir / "report.json",
        {
            "grounding": {
                "parsed_fields": {
                    "open_continuation_target": "\n".join(
                        [
                            "```lean",
                            "theorem completed_target : True := by",
                            "  trivial",
                            "```",
                        ]
                    ),
                    "recommended_attack_target": "Next round should prove `fresh_target`.",
                }
            }
        },
    )

    assert extract_formalization_target_from_run(run_dir, excluded_names={"completed_target"}) == "fresh_target"


def test_campaign_loop_dynamic_round_budget_has_floor(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    assert runner._stage_time_budget(
        stage="lean_formalizer",
        remaining_seconds=43_200,
        rounds_left=100,
        round_time_budget_sec=0,
    ) == 900
    assert runner._stage_time_budget(
        stage="proof_lab",
        remaining_seconds=43_200,
        rounds_left=100,
        round_time_budget_sec=0,
    ) == 600


def test_campaign_loop_hybrid_starts_with_formalizer_when_target_is_known(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    assert (
        runner._choose_stage(
            mode="hybrid",
            round_number=1,
            workspace=tmp_path / "formal",
            current_target_theorem="finite_sidon_sqrt_lower",
            previous_entry=None,
        )
        == "lean_formalizer"
    )


def test_campaign_loop_global_reassessment_after_formalizer_stall(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem existing_helper : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = CampaignLoopRunner(repo_root=tmp_path)

    report = runner.run(
        statement="Prove the root theorem, but split it if the current stage is too broad.",
        workspace=workspace,
        final_target_theorem="missing_final",
        initial_target_theorem="missing_final",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=["python3", "-c", "print('mock build passed')"],
        backend="none",
        mode="hybrid",
        rounds=2,
        time_budget_sec=120,
        formalizer_attempts=1,
        output_root=tmp_path / "loops",
        run_name="reassess-loop",
    )

    assert report["status"] == "partial"
    assert [round_entry["stage"] for round_entry in report["rounds"]] == [
        "lean_formalizer",
        "proof_lab",
    ]
    assert report["rounds"][0]["needs_global_reassessment"] is True
    assessment_path = Path(report["rounds"][0]["global_assessment_path"])
    assert assessment_path.exists()
    assessment = assessment_path.read_text(encoding="utf-8")
    assert "Required Global Decision" in assessment
    second_goal = Path(report["run_dir"]) / "rounds" / "round_002" / "stage_goal.md"
    assert "Prior Round 1 Global Assessment" in second_goal.read_text(encoding="utf-8")


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
        completed_target_theorems=["seeded_done"],
        output_root=tmp_path / "loops",
        run_name="proof-loop",
    )

    assert report["status"] == "partial"
    assert report["completed_target_theorems"] == ["seeded_done"]
    assert report["rounds_completed"] == 2
    assert [round_entry["stage"] for round_entry in report["rounds"]] == ["proof_lab", "proof_lab"]
    assert Path(report["summary_path"]).exists()
    first_goal = Path(report["run_dir"]) / "rounds" / "round_001" / "stage_goal.md"
    first_goal_text = first_goal.read_text(encoding="utf-8")
    assert "Loop Discipline" in first_goal_text
    assert "seeded_done" in first_goal_text


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
