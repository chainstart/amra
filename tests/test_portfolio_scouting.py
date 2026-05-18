from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amra.portfolio_campaign import PortfolioCampaignRunner
from ara_math.models import ProblemRecord
from ara_math.problem_bank import save_problem_bank


class FakeScoutRunner:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        run_dir = Path(kwargs["run_dir"])
        output_path = Path(kwargs["output_path"])
        exact_dir = run_dir / "problems" / "0000-exact-promote"
        timeout_dir = run_dir / "problems" / "0001-timeout-probe"
        exact_dir.mkdir(parents=True, exist_ok=True)
        timeout_dir.mkdir(parents=True, exist_ok=True)
        exact_prompt = exact_dir / "prompt.txt"
        exact_output = exact_dir / "probe_output.md"
        timeout_prompt = timeout_dir / "prompt.txt"
        timeout_output = timeout_dir / "probe_output.md"
        exact_prompt.write_text("exact prompt\n", encoding="utf-8")
        exact_output.write_text(
            "\n".join(
                [
                    "Feasibility score: 8",
                    "Recommendation: promote",
                    "Estimated proof effort: small",
                    "Primary blocker: key_lemma",
                    "Proof attempt status: rigorous_partial",
                    "Next investment: formalize the lemma",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        timeout_prompt.write_text("timeout prompt\n", encoding="utf-8")
        timeout_output.write_text("Timed out before producing a final backend message.\n", encoding="utf-8")
        payload = {
            "schema_version": "ara_math.math_scout_report.v1",
            "generated_at": "2026-05-18T00:00:00+00:00",
            "status": "partial",
            "backend": kwargs["backend"],
            "run_dir": str(run_dir),
            "problem_limit": kwargs["problem_limit"],
            "timeout_per_problem_sec": kwargs["timeout_per_problem_sec"],
            "entries": [
                {
                    "problem_id": "exact-promote",
                    "title": "Exact Promote",
                    "position": 0,
                    "domain": "number_theory",
                    "parsed_probe": {
                        "feasibility_score": 8.0,
                        "recommendation": "promote",
                        "estimated_proof_effort": "small",
                        "primary_blocker": "key_lemma",
                        "proof_attempt_status": "rigorous_partial",
                        "next_investment": "formalize the lemma",
                    },
                    "backend_report": {"status": "completed", "backend": kwargs["backend"], "returncode": 0},
                    "artifacts": {"prompt": str(exact_prompt), "probe_output": str(exact_output)},
                },
                {
                    "problem_id": "timeout-probe",
                    "title": "Timeout Probe",
                    "position": 1,
                    "domain": "geometry",
                    "parsed_probe": {
                        "feasibility_score": 0.0,
                        "recommendation": "unknown",
                        "estimated_proof_effort": "not_assessable",
                        "primary_blocker": "unknown",
                        "proof_attempt_status": "failed",
                        "next_investment": "",
                    },
                    "backend_report": {"status": "timeout", "backend": kwargs["backend"], "returncode": None},
                    "artifacts": {"prompt": str(timeout_prompt), "probe_output": str(timeout_output)},
                },
            ],
            "ranked_candidates": [],
            "processed_problem_count": 2,
            "stop_reason": "time_budget_exhausted",
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return payload


class ExplodingScoutRunner:
    def run(self, **_kwargs: Any) -> dict[str, Any]:
        raise TimeoutError("supervisor timed out")


def _write_bank(bank_path: Path) -> None:
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="exact-promote",
                title="Exact Promote",
                source="unit",
                statement="Prove that every integer n satisfies n = n.",
                domain="number_theory",
                tags=["number theory"],
                references=["https://example.test/exact"],
            ),
            ProblemRecord(
                problem_id="timeout-probe",
                title="Timeout Probe",
                source="unit",
                statement="Prove that every triangle has itself as a triangle.",
                domain="geometry",
                tags=["geometry"],
                references=["https://example.test/timeout"],
            ),
        ],
        bank_path,
    )


def test_portfolio_campaign_uses_math_scout_runner_and_probe_artifacts(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    _write_bank(bank_path)
    fake_scout = FakeScoutRunner()

    result = PortfolioCampaignRunner(repo_root=tmp_path, math_scout_runner=fake_scout).run_portfolio_campaign(
        bank=bank_path,
        run_name="scout integration",
        scout_limit=2,
        scout_timeout=42,
        scout_backend="none",
        promote_top=1,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    ranking = json.loads((campaign_dir / "ranking.json").read_text(encoding="utf-8"))["ranking"]
    scout_report = json.loads((campaign_dir / "scout_report.json").read_text(encoding="utf-8"))
    exact_probe = json.loads((campaign_dir / "problems" / "exact-promote" / "probe" / "scout_probe.json").read_text())
    timeout_probe = json.loads((campaign_dir / "problems" / "timeout-probe" / "probe" / "scout_probe.json").read_text())

    assert fake_scout.calls[0]["run_dir"] == campaign_dir / "broad_scout"
    assert fake_scout.calls[0]["timeout_per_problem_sec"] == 21
    assert scout_report["mode"] == "math_scout_runner"
    assert scout_report["processed_problem_count"] == 2
    assert ranking[0]["problem_id"] == "exact-promote"
    assert ranking[0]["shallow_proof_signal"]["recommendation"] == "promote"
    assert ranking[0]["source_quality"]["statement_quality"] == "exact"
    assert "formalization_signal" in ranking[0]
    assert exact_probe["status"] == "completed"
    assert (campaign_dir / "problems" / "exact-promote" / "probe" / "probe_output.md").exists()
    assert timeout_probe["status"] == "timeout"
    timeout_difficulty = json.loads(
        (campaign_dir / "problems" / "timeout-probe" / "evaluation" / "difficulty.json").read_text()
    )
    assert "scout_timeout" in timeout_difficulty["risk_flags"]


def test_portfolio_campaign_writes_valid_artifacts_when_scout_runner_fails(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    _write_bank(bank_path)

    result = PortfolioCampaignRunner(repo_root=tmp_path, math_scout_runner=ExplodingScoutRunner()).run_portfolio_campaign(
        bank=bank_path,
        run_name="scout failure",
        scout_limit=1,
        scout_timeout=5,
        scout_backend="none",
        promote_top=1,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    math_scout_report = json.loads((campaign_dir / "math_scout_report.json").read_text(encoding="utf-8"))
    probe = json.loads((campaign_dir / "problems" / "exact-promote" / "probe" / "scout_probe.json").read_text())
    ranking = json.loads((campaign_dir / "ranking.json").read_text(encoding="utf-8"))["ranking"]

    assert math_scout_report["status"] == "failed"
    assert math_scout_report["stop_reason"] == "scout_runner_exception"
    assert probe["status"] == "not_processed"
    assert probe["scout_error"]["type"] == "TimeoutError"
    assert ranking[0]["problem_id"] == "exact-promote"
