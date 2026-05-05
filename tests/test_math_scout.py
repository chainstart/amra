from __future__ import annotations

import json
from pathlib import Path

from ara_math.math_scout import MathScoutRunner, _parse_probe_output
from ara_math.models import ProblemRecord
from ara_math.problem_bank import save_problem_bank


def test_parse_probe_output_extracts_active_scout_fields() -> None:
    parsed = _parse_probe_output(
        "\n".join(
            [
                "Feasibility score: 7.5",
                "Recommendation: promote",
                "Estimated proof effort: medium",
                "Primary blocker: key_lemma",
                "Proof attempt status: heuristic_route",
                "Next investment: formalize the reduction lemma",
            ]
        )
    )

    assert parsed["feasibility_score"] == 7.5
    assert parsed["recommendation"] == "promote"
    assert parsed["estimated_proof_effort"] == "medium"
    assert parsed["primary_blocker"] == "key_lemma"
    assert parsed["proof_attempt_status"] == "heuristic_route"
    assert parsed["next_investment"] == "formalize the reduction lemma"


def test_math_scout_prompt_requires_real_mathematical_attempt(tmp_path: Path) -> None:
    runner = MathScoutRunner(repo_root=tmp_path)
    problem = ProblemRecord(
        problem_id="probe",
        title="Probe Problem",
        source="test",
        statement="Prove that every object has property P.",
        domain="number_theory",
        references=["https://example.com/probe"],
    )

    prompt = runner._build_prompt(
        problem=problem,
        passive_assessment={
            "score": 1,
            "investment_class": "source_recovery",
            "blocker_class": "statement_recovery",
        },
    )

    assert "This is not metadata triage" in prompt
    assert "Try to prove the claim" in prompt
    assert "Feasibility score:" in prompt
    assert "Resource estimate" in prompt


def test_math_scout_backend_none_writes_report(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="probe",
                title="Probe Problem",
                source="test",
                statement="Prove that every object has property P.",
                domain="number_theory",
                open_problem=True,
                references=["https://example.com/probe"],
            )
        ],
        bank_path,
    )
    output_path = tmp_path / "math_scout_report.json"

    payload = MathScoutRunner(repo_root=tmp_path).run(
        bank_path=bank_path,
        backend="none",
        problem_limit=1,
        output_path=output_path,
        run_name="test-scout",
    )

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["processed_problem_count"] == 1
    assert saved["entries"][0]["problem_id"] == "probe"
    assert saved["entries"][0]["artifacts"]["probe_output"].endswith("probe_output.md")


def test_domain_balanced_selection_interleaves_domains_and_excludes(tmp_path: Path) -> None:
    runner = MathScoutRunner(repo_root=tmp_path)
    rows = [
        {
            "problem": ProblemRecord(problem_id="n1", title="N1", source="test", statement="n1", domain="number_theory"),
            "passive_assessment": {"score": 9},
        },
        {
            "problem": ProblemRecord(problem_id="n2", title="N2", source="test", statement="n2", domain="number_theory"),
            "passive_assessment": {"score": 8},
        },
        {
            "problem": ProblemRecord(problem_id="g1", title="G1", source="test", statement="g1", domain="geometry"),
            "passive_assessment": {"score": 7},
        },
    ]

    selected = runner._select_rows(rows, selection_mode="domain_balanced", exclude_problem_ids={"n1"})

    assert [row["problem"].problem_id for row in selected] == ["n2", "g1"]
