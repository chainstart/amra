from __future__ import annotations

import subprocess
from pathlib import Path

from ara_math.campaign_loop import (
    CampaignLoopRunner,
    extract_first_theorem_name,
    extract_formalization_target_from_run,
    supervisor_text_requests_lean_stage,
)
from ara_math.workspace import write_json
from amra.proof.global_supervisor import GlobalProofSupervisor, parse_supervisor_decision


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


def test_campaign_loop_honors_supervisor_forced_next_stage(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    assert (
        runner._choose_stage(
            mode="lean-formalizer",
            round_number=2,
            workspace=tmp_path / "formal",
            current_target_theorem="current_target",
            previous_entry={"supervisor_forced_next_stage": "proof_lab"},
        )
        == "proof_lab"
    )
    assert (
        runner._choose_stage(
            mode="proof-lab",
            round_number=2,
            workspace=tmp_path / "formal",
            current_target_theorem="current_target",
            previous_entry={"supervisor_forced_next_stage": "lean_formalizer"},
        )
        == "lean_formalizer"
    )


def test_campaign_loop_infers_context_lean_file_for_supervisor_switch(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem fresh_target : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = CampaignLoopRunner(repo_root=tmp_path)

    def fake_supervisor_run(**kwargs):
        decision_path = tmp_path / "supervisor-switch.md"
        parsed_path = tmp_path / "supervisor-switch.json"
        decision_path.write_text("Supervisor decision: switch_target\n", encoding="utf-8")
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "switch_target",
            "target_theorem": "fresh_target",
            "controller_action": "switch_target",
            "reason": "the proof-lab found a Lean-ready target",
            "instructions": "switch to the formalizer for fresh_target",
            "route_risk": "low",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Design a route, then let the supervisor switch to Lean if a target is ready.",
        context_paths=[workspace / "MathProject" / "MainClaim.lean"],
        build_command=["python3", "-c", "print('mock build passed')"],
        backend="none",
        mode="proof-lab",
        rounds=2,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        formalizer_attempts=0,
        output_root=tmp_path / "loops",
        run_name="context-inferred-switch",
        supervisor_backend="codex",
        supervisor_every_rounds=1,
        math_tools_profile="essential",
        install_missing_math_tools=False,
        run_math_tool_smoke=False,
    )

    assert report["inferred_formalizer_config"]["workspace"] is True
    assert report["inferred_formalizer_config"]["target_file"] is True
    assert [entry["stage"] for entry in report["rounds"]] == ["proof_lab", "lean_formalizer"]
    assert report["rounds"][0]["supervisor_control_action"] == "switch_target"
    assert report["rounds"][0]["supervisor_forced_next_stage"] == "lean_formalizer"


def test_campaign_loop_stops_supervisor_lean_switch_without_formalizer_config(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    def fake_supervisor_run(**kwargs):
        decision_path = tmp_path / "supervisor-switch-missing-config.md"
        parsed_path = tmp_path / "supervisor-switch-missing-config.json"
        decision_path.write_text("Supervisor decision: switch_target\n", encoding="utf-8")
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "switch_target",
            "target_theorem": "fresh_target",
            "controller_action": "switch_target",
            "reason": "the proof-lab found a Lean-ready target",
            "instructions": "switch to the formalizer for fresh_target",
            "route_risk": "low",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Design a route, then switch to Lean if a target is ready.",
        backend="none",
        mode="proof-lab",
        rounds=2,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        output_root=tmp_path / "loops",
        run_name="missing-config-switch",
        supervisor_backend="codex",
        supervisor_every_rounds=1,
        math_tools_profile="essential",
        install_missing_math_tools=False,
        run_math_tool_smoke=False,
    )

    assert report["stop_reason"] == "supervisor_missing_formalizer_config"
    assert report["rounds_completed"] == 1
    assert report["current_target_theorem"] == "fresh_target"
    assert report["rounds"][0]["supervisor_control_action"] == "switch_target_needs_formalizer_config"
    assert report["rounds"][0]["supervisor_requeue"]["required"] is True
    assert report["supervisor_decisions"][0]["requeue"]["next_mode"] == "lean-formalizer"


def test_campaign_loop_supervisor_continue_can_force_lean_certificate_stage(tmp_path: Path) -> None:
    workspace = _write_workspace(
        tmp_path,
        "\n".join(
            [
                "namespace MathProject",
                "",
                "theorem stable_target : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
    )
    runner = CampaignLoopRunner(repo_root=tmp_path)

    assert supervisor_text_requests_lean_stage("Run the next round as a Lean formalizer/certificate round.")

    def fake_supervisor_run(**kwargs):
        decision_path = tmp_path / "supervisor-continue-lean.md"
        parsed_path = tmp_path / "supervisor-continue-lean.json"
        decision_path.write_text("Supervisor decision: continue_current_target\n", encoding="utf-8")
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "continue_current_target",
            "target_theorem": "stable_target",
            "controller_action": "continue",
            "reason": "route discovery is exhausted and the bridge is ready",
            "instructions": "Run the next round as a Lean formalizer/certificate round, not proof-lab.",
            "route_risk": "low",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Keep the same target, but switch task type when the supervisor requests certification.",
        context_paths=[workspace / "MathProject" / "MainClaim.lean"],
        initial_target_theorem="stable_target",
        build_command=["python3", "-c", "print('mock build passed')"],
        backend="none",
        mode="proof-lab",
        rounds=2,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        formalizer_attempts=0,
        output_root=tmp_path / "loops",
        run_name="continue-forces-lean",
        supervisor_backend="codex",
        supervisor_every_rounds=1,
        math_tools_profile="essential",
        install_missing_math_tools=False,
        run_math_tool_smoke=False,
    )

    assert [entry["stage"] for entry in report["rounds"]] == ["proof_lab", "lean_formalizer"]
    assert report["rounds"][0]["supervisor_control_action"] == "continue_as_lean_formalizer"
    assert report["rounds"][0]["supervisor_forced_next_stage"] == "lean_formalizer"


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


def test_parse_supervisor_decision_extracts_switch_target() -> None:
    decision = parse_supervisor_decision(
        "\n".join(
            [
                "Supervisor decision: switch_target",
                "Reason: the final claim is too broad for the next Lean round.",
                "Next target: `fresh_target`",
                "Formalization target:",
                "```lean",
                "theorem fresh_target : True := by",
                "  trivial",
                "```",
                "Controller action: switch_target",
                "Instructions: prove this helper first.",
                "Route risk: low",
            ]
        )
    )

    assert decision["decision"] == "switch_target"
    assert decision["target_theorem"] == "fresh_target"
    assert decision["controller_action"] == "switch_target"
    assert decision["route_risk"] == "low"


def test_global_supervisor_sends_large_prompt_via_stdin(tmp_path: Path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_run_guarded_command(command, **kwargs):
        captured["command"] = command
        captured["input_text"] = kwargs.get("input_text")
        output_path = Path(command[command.index("--output-last-message") + 1])
        output_path.write_text(
            "\n".join(
                [
                    "Supervisor decision: continue_current_target",
                    "Reason: keep going.",
                    "Next target: <none>",
                    "Formalization target: <unchanged>",
                    "Instructions: continue.",
                    "Route risk: low",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr("amra.proof.global_supervisor.shutil.which", lambda _name: "/usr/bin/codex")
    monkeypatch.setattr("amra.proof.global_supervisor.wait_for_system_headroom", lambda **_kwargs: None)
    monkeypatch.setattr("amra.proof.global_supervisor.run_guarded_command", fake_run_guarded_command)

    long_statement = "Prove this.\n" + ("long context\n" * 20000)
    supervisor = GlobalProofSupervisor(repo_root=tmp_path)
    decision = supervisor.run(
        run_dir=tmp_path / "run",
        statement=long_statement,
        round_number=1,
        current_target_theorem="Current",
        final_target_theorem="Final",
        completed_target_theorems=set(),
        latest_entry={"round": 1, "status": "partial"},
        round_entries=[],
        backend="codex",
        timeout_sec=10,
        enable_search=False,
    )

    command = captured["command"]
    assert isinstance(command, list)
    assert command[-1] == "-"
    assert long_statement not in command
    assert isinstance(captured["input_text"], str)
    assert long_statement in captured["input_text"]
    assert decision["decision"] == "continue_current_target"


def test_campaign_loop_supervisor_can_retarget_after_stall(tmp_path: Path) -> None:
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

    def fake_supervisor_run(**kwargs):
        decision_path = tmp_path / "supervisor-decision.md"
        parsed_path = tmp_path / "supervisor-decision.json"
        decision_path.write_text("Supervisor decision: switch_target\n", encoding="utf-8")
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "switch_target",
            "target_theorem": "fresh_target",
            "controller_action": "switch_target",
            "reason": "missing_final should be split first",
            "instructions": "prove fresh_target before returning to missing_final",
            "route_risk": "medium",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Prove the root theorem, but split it if the current stage is too broad.",
        workspace=workspace,
        final_target_theorem="missing_final",
        initial_target_theorem="missing_final",
        target_file=Path("MathProject/MainClaim.lean"),
        build_command=["python3", "-c", "print('mock build passed')"],
        backend="none",
        mode="hybrid",
        rounds=1,
        time_budget_sec=120,
        formalizer_attempts=1,
        output_root=tmp_path / "loops",
        run_name="supervised-loop",
        supervisor_backend="codex",
    )

    assert report["current_target_theorem"] == "fresh_target"
    assert report["rounds"][0]["supervisor_decision"] == "switch_target"
    assert report["rounds"][0]["supervisor_control_action"] == "switch_target"
    assert report["rounds"][0]["supervisor_target_replaced"] is True
    assert report["supervisor_decisions"][0]["target_theorem"] == "fresh_target"
    assert report["supervisor_decisions"][0]["control_action"] == "switch_target"


def test_campaign_loop_supervisor_freeze_route_stops_current_loop(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)

    def fake_supervisor_run(**kwargs):
        decision_path = tmp_path / "freeze-decision.md"
        parsed_path = tmp_path / "freeze-decision.json"
        decision_path.write_text(
            "\n".join(
                [
                    "Supervisor decision: freeze_route",
                    "Reason: the route has exhausted the theorem-level direction.",
                    "Next target: <none>",
                    "Instructions: stop this route and choose a new one.",
                    "Route risk: high",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "freeze_route",
            "target_theorem": "",
            "controller_action": "stop_campaign",
            "reason": "the route has exhausted the theorem-level direction",
            "instructions": "stop this route and choose a new one",
            "route_risk": "high",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Prove the root theorem, but stop if the route is exhausted.",
        backend="none",
        mode="proof-lab",
        rounds=5,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        output_root=tmp_path / "loops",
        run_name="freeze-loop",
        supervisor_backend="codex",
        supervisor_every_rounds=1,
    )

    assert report["stop_reason"] == "supervisor_freeze_route"
    assert report["rounds_completed"] == 1
    assert report["current_target_theorem"] == ""
    assert report["rounds"][0]["supervisor_decision"] == "freeze_route"
    assert report["rounds"][0]["supervisor_control_action"] == "stop_campaign"
    assert report["rounds"][0]["supervisor_stop_reason"] == "supervisor_freeze_route"
    assert report["supervisor_decisions"][0]["control_action"] == "stop_campaign"


def test_campaign_loop_supervisor_freeze_route_can_replan_next_round(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)
    calls = {"count": 0}

    def fake_supervisor_run(**kwargs):
        calls["count"] += 1
        decision_path = tmp_path / f"freeze-replan-decision-{calls['count']}.md"
        parsed_path = tmp_path / f"freeze-replan-decision-{calls['count']}.json"
        if calls["count"] == 1:
            decision_path.write_text(
                "\n".join(
                    [
                        "Supervisor decision: freeze_route",
                        "Reason: the current target is mis-specified, but a repaired route should be designed.",
                        "Next target: <none>",
                        "Formalization target: <unchanged>",
                        "Controller action: replan_proof_lab",
                        "Instructions: return to route design and repair the theorem statement before Lean work.",
                        "Route risk: high",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            parsed_path.write_text("{}", encoding="utf-8")
            return {
                "decision": "freeze_route",
                "target_theorem": "",
                "controller_action": "replan_proof_lab",
                "reason": "the current target is mis-specified, but a repaired route should be designed",
                "instructions": "return to route design and repair the theorem statement before Lean work",
                "route_risk": "high",
                "decision_path": str(decision_path),
                "parsed_decision_path": str(parsed_path),
                "backend_invocation": {"status": "completed"},
            }
        decision_path.write_text(
            "\n".join(
                [
                    "Supervisor decision: continue_current_target",
                    "Reason: keep designing the repaired theorem statement.",
                    "Next target: <none>",
                    "Formalization target: <unchanged>",
                    "Controller action: continue",
                    "Instructions: continue route design.",
                    "Route risk: medium",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        parsed_path.write_text("{}", encoding="utf-8")
        return {
            "decision": "continue_current_target",
            "target_theorem": "",
            "controller_action": "continue",
            "reason": "keep designing the repaired theorem statement",
            "instructions": "continue route design",
            "route_risk": "medium",
            "decision_path": str(decision_path),
            "parsed_decision_path": str(parsed_path),
            "backend_invocation": {"status": "completed"},
        }

    runner.global_supervisor.run = fake_supervisor_run  # type: ignore[method-assign]
    report = runner.run(
        statement="Repair a mis-specified theorem and choose a valid next target.",
        backend="none",
        mode="proof-lab",
        rounds=2,
        time_budget_sec=120,
        proof_attempts=1,
        proof_audits=0,
        output_root=tmp_path / "loops",
        run_name="freeze-replan-loop",
        supervisor_backend="codex",
        supervisor_every_rounds=1,
    )

    assert report["stop_reason"] == "rounds_exhausted"
    assert report["rounds_completed"] == 2
    assert [entry["stage"] for entry in report["rounds"]] == ["proof_lab", "proof_lab"]
    assert report["rounds"][0]["supervisor_decision"] == "freeze_route"
    assert report["rounds"][0]["supervisor_control_action"] == "freeze_and_replan"
    assert report["rounds"][0]["supervisor_forced_next_stage"] == "proof_lab"
    assert report["rounds"][0]["needs_global_reassessment"] is True
    assert report["supervisor_decisions"][0]["control_action"] == "freeze_and_replan"
    assert "repair the theorem statement" in report["supervisor_decisions"][0]["next_work_direction"]


def test_campaign_loop_carries_supervisor_decision_into_later_context(tmp_path: Path) -> None:
    runner = CampaignLoopRunner(repo_root=tmp_path)
    decision_path = tmp_path / "supervisor" / "decision.md"
    decision_path.parent.mkdir(parents=True)
    decision_path.write_text(
        "Supervisor decision: switch_target\nInstructions: prove `fresh_target` first.\n",
        encoding="utf-8",
    )
    entry = {"round": 1, "supervisor_decision_path": str(decision_path), "run_dir": str(tmp_path / "missing")}

    assert "Prior Round 1 Supervisor Decision" in runner._read_history_snippets([entry])
    assert decision_path in runner._loop_context_paths([], [entry])


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
