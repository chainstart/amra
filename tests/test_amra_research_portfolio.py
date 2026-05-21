from __future__ import annotations

import json
from pathlib import Path

from amra.research.portfolio import (
    RESEARCH_CAMPAIGN_SCHEMA_VERSION,
    RESEARCH_PORTFOLIO_SCHEMA_VERSION,
    run_research_portfolio_campaign_fixture,
)


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "research_portfolio_fixture.json"


def test_research_portfolio_campaign_writes_durable_artifacts(tmp_path: Path) -> None:
    result = run_research_portfolio_campaign_fixture(fixture=FIXTURE, output_dir=tmp_path / "campaign", repo_root=tmp_path)

    campaign = tmp_path / "campaign"
    manifest = json.loads((campaign / "campaign_manifest.json").read_text(encoding="utf-8"))
    portfolio = json.loads((campaign / "research_portfolio.json").read_text(encoding="utf-8"))
    ranking = json.loads((campaign / "ranking.json").read_text(encoding="utf-8"))["ranking"]
    promotions = json.loads((campaign / "promotion_candidates.json").read_text(encoding="utf-8"))["candidates"]
    theory_map = json.loads((campaign / "theory_map.json").read_text(encoding="utf-8"))
    artifact_manifest = json.loads((campaign / "artifact_manifest.json").read_text(encoding="utf-8"))
    negative_lines = (campaign / "negative_results.jsonl").read_text(encoding="utf-8").splitlines()

    assert result["schema_version"] == "amra.research_portfolio_campaign_result.v1"
    assert manifest["schema_version"] == RESEARCH_CAMPAIGN_SCHEMA_VERSION
    assert portfolio["schema_version"] == RESEARCH_PORTFOLIO_SCHEMA_VERSION
    assert manifest["live_model_calls"] is False
    assert ranking[0]["object_id"] == "conj-proof-ready"
    assert ranking[0]["recommendation"] == "promote_to_proof"
    assert promotions[0]["object_id"] == "conj-proof-ready"
    assert promotions[0]["verification_boundary"] == "promotion_candidate_not_lean_verified"
    assert len(negative_lines) == 1
    assert json.loads(negative_lines[0])["object_id"] == "negative-counterexample"
    assert "conj-proof-ready" in theory_map["taxonomy"]["conjectures"]
    assert "negative-counterexample" in theory_map["taxonomy"]["failures"]
    assert artifact_manifest["verification_boundary"]["promotion_candidates"] == "not_lean_verified"
    assert "artifact_manifest" in result
    assert (campaign / "objects" / "conj-proof-ready" / "object.json").exists()
    assert (campaign / "objects" / "conj-proof-ready" / "promotion" / "candidate.json").exists()
    assert (campaign / "projects" / "conj-proof-ready" / "object.yaml").exists()
    assert (campaign / "benchmark_reports.jsonl").read_text(encoding="utf-8").strip()


def test_research_portfolio_campaign_schedules_mixed_task_types(tmp_path: Path) -> None:
    run_research_portfolio_campaign_fixture(fixture=FIXTURE, output_dir=tmp_path / "campaign", repo_root=tmp_path)

    portfolio = json.loads((tmp_path / "campaign" / "research_portfolio.json").read_text(encoding="utf-8"))
    tasks = {item["task_id"]: item for item in portfolio["tasks"]}

    assert tasks["task-benchmark-algo"]["recommendation"] == "schedule_bounded_executor"
    assert tasks["task-record-negative"]["recommendation"] == "record_negative_result"
    assert portfolio["scheduling_policy"]["proof_ready_promotes_to_existing_pipeline"] is True
    assert "negative_result_value" in portfolio["scoring_dimensions"]
