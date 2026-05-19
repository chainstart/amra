import json
from pathlib import Path

from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_memory import record_failed_route, upsert_claim
from ara_math.models import ProblemRecord
from ara_math.problem_bank import save_problem_bank


def test_portfolio_campaign_writes_durable_resume_pack(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
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
                problem_id="needs-source",
                title="Needs Source",
                source="unit",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                metadata={"statement_quality": "placeholder"},
            ),
        ],
        bank_path,
    )
    runner = PortfolioCampaignRunner(repo_root=tmp_path)

    result = runner.run_portfolio_campaign(
        bank=bank_path,
        run_name="data layer unit",
        scout_limit=2,
        promote_top=1,
        attack_budget=120,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    ranking = json.loads((campaign_dir / "ranking.json").read_text(encoding="utf-8"))
    resume_pack = (campaign_dir / "resume_pack.md").read_text(encoding="utf-8")

    assert result["resume_pack"] == "artifacts/portfolio_campaigns/data-layer-unit/resume_pack.md"
    assert ranking["schema_version"] == "amra.ranking.v1"
    assert (campaign_dir / "problems" / "exact-promote" / "evaluation" / "difficulty.json").exists()
    assert "## Promotion Queue" in resume_pack
    assert "`exact-promote`" in resume_pack
    assert "## Parked Or Source Recovery Queue" in resume_pack


def test_portfolio_campaign_records_budget_gate_and_abandon_policy(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
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
                problem_id="no-source-abandon",
                title="No Source Abandon",
                source="",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="general",
                tags=[],
                metadata={"statement_quality": "placeholder"},
            ),
        ],
        bank_path,
    )
    runner = PortfolioCampaignRunner(repo_root=tmp_path)

    result = runner.run_portfolio_campaign(
        bank=bank_path,
        run_name="policy unit",
        scout_limit=2,
        promote_top=1,
        attack_budget=0,
    )

    campaign_dir = tmp_path / result["campaign_dir"]
    ranking = json.loads((campaign_dir / "ranking.json").read_text(encoding="utf-8"))["ranking"]
    by_problem = {item["problem_id"]: item for item in ranking}
    resume_pack = (campaign_dir / "resume_pack.md").read_text(encoding="utf-8")

    assert by_problem["exact-promote"]["budget_gate"]["long_budget_allowed"] is True
    assert by_problem["exact-promote"]["decision_policy"]["resume_pack_required_before_retry"] is True
    assert by_problem["no-source-abandon"]["recommendation"] == "abandon"
    assert by_problem["no-source-abandon"]["decision_policy"]["abandonment_eligible"] is True
    assert by_problem["no-source-abandon"]["long_budget_allowed"] is False
    assert "Do not spend attack budget on abandoned or source-recovery targets" in resume_pack


def test_initialize_problem_project_writes_memory_resume_and_indexes(tmp_path: Path) -> None:
    runner = PortfolioCampaignRunner(repo_root=tmp_path)
    project = tmp_path / "projects" / "problem-init"

    result = runner.initialize_problem_project(project=project, problem_id="problem-init", state="scouted")

    problem_index = json.loads((tmp_path / "artifacts" / "global_memory" / "problem_index.json").read_text(encoding="utf-8"))
    resume_pack = (project / "resume_pack.md").read_text(encoding="utf-8")

    assert result["state"]["state"] == "scouted"
    assert (project / "memory" / "claim_ledger.json").exists()
    assert (project / "memory" / "route_ledger.json").exists()
    assert (project / "memory" / "failed_routes.json").exists()
    assert (project / "memory" / "evidence_index.json").exists()
    assert result["resume_pack"] == str(project / "resume_pack.md")
    assert problem_index["problems"][0]["problem_id"] == "problem-init"
    assert "Problem: `problem-init`" in resume_pack


def test_evaluate_problem_refreshes_resume_pack_and_global_indexes(tmp_path: Path) -> None:
    runner = PortfolioCampaignRunner(repo_root=tmp_path)
    project = tmp_path / "projects" / "problem-eval"
    runner.initialize_problem_project(project=project, problem_id="problem-eval", state="active_attack")
    upsert_claim(project, {"claim_id": "main", "statement_nl": "Main claim.", "status": "hypothesis"})
    record_failed_route(
        project,
        {
            "route_id": "route-main",
            "failure_mode": "counterexample_candidate",
            "resume_condition": "The candidate is refuted.",
        },
    )

    report = runner.evaluate_problem(project=project, run_name="eval-1")

    failed_index = json.loads((tmp_path / "artifacts" / "global_memory" / "failed_route_index.json").read_text(encoding="utf-8"))
    resume_pack = (project / "resume_pack.md").read_text(encoding="utf-8")

    assert report["recommendation"] == "counterexample_review"
    assert report["failed_route_count"] == 1
    assert (project / "runs" / "eval-1" / "difficulty.json").exists()
    assert len(failed_index["failed_routes"]) == 1
    assert "counterexample_candidate" in resume_pack
    assert "Do not repeat this route unless the resume condition is met." in resume_pack
