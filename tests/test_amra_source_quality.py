import json
from pathlib import Path

from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_evaluator import PortfolioEvaluator
from amra.source_quality import build_source_quality_audit, score_source_record
from ara_math.models import ProblemRecord
from ara_math.problem_bank import save_problem_bank


def test_source_quality_prefers_curated_local_snapshot_over_remote_locator(tmp_path: Path) -> None:
    snapshot = tmp_path / "curated_snapshot.md"
    snapshot.write_text("**Problem Statement**: Prove that every integer equals itself.\n", encoding="utf-8")

    local_quality = score_source_record(
        {
            "source": str(snapshot),
            "kind": "curated_snapshot",
            "source_type": "local_path",
            "status": "ok",
            "candidate_statements": [{"statement": "Prove that every integer equals itself."}],
            "evidence_items": [{"kind": "known_result", "statement": "Reflexivity closes the theorem."}],
        },
        metadata={
            "source_catalog": "curated",
            "statement_quality": "exact",
            "statement_provenance": str(snapshot),
        },
    )
    remote_quality = score_source_record(
        {"source": "https://example.test/live-problem", "kind": "reference", "status": "declared"}
    )

    assert local_quality["score"] > remote_quality["score"]
    assert local_quality["tier"] == "trusted"
    assert "local_snapshot_available" in local_quality["trust_reasons"]
    assert "remote_source_without_local_snapshot" in remote_quality["source_debt"]


def test_portfolio_evaluator_exposes_source_quality_and_statement_provenance(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "quality-problem"
    PortfolioCampaignRunner(repo_root=tmp_path).initialize_problem_project(
        project=project,
        problem_id="quality-problem",
        state="scouted",
    )
    source_doc = tmp_path / "fixtures" / "quality_statement.md"
    source_doc.parent.mkdir(parents=True, exist_ok=True)
    source_doc.write_text(
        "**Problem Statement**: Prove that every integer n satisfies n = n.\n",
        encoding="utf-8",
    )
    (project / "problem.yaml").write_text(
        "\n".join(
            [
                "problem_id: quality-problem",
                "statement: Prove that every integer n satisfies n = n.",
                f"source: {source_doc}",
                "references:",
                f"  - {source_doc}",
                "metadata:",
                "  statement_quality: exact",
                f"  statement_provenance: {source_doc}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    audit = build_source_quality_audit(
        problem_id="quality-problem",
        statement="Prove that every integer n satisfies n = n.",
        statement_source=str(source_doc),
        source=str(source_doc),
        references=[str(source_doc)],
        metadata={"statement_quality": "exact", "statement_provenance": str(source_doc)},
        snapshots=[
            {
                "source": str(source_doc),
                "kind": "curated_snapshot",
                "source_type": "local_path",
                "status": "ok",
                "candidate_statements": [{"statement": "Prove that every integer n satisfies n = n."}],
            }
        ],
    )
    (project / "idea").mkdir(parents=True, exist_ok=True)
    (project / "idea" / "source_quality_audit.json").write_text(json.dumps(audit), encoding="utf-8")

    report = PortfolioEvaluator(repo_root=tmp_path).evaluate_project(project=project, run_name="quality-eval")
    source_signal = report["source_signal"]

    assert source_signal["source_quality_tier"] == "trusted"
    assert source_signal["statement_provenance"]["source"] == str(source_doc)
    assert "local_snapshot_available" in source_signal["trust_reasons"]
    assert "projects/quality-problem/idea/source_quality_audit.json" in report["evidence"]


def test_portfolio_campaign_ranking_carries_source_debt_and_trust_reasons(tmp_path: Path) -> None:
    curated = tmp_path / "curated_problem.md"
    curated.write_text("**Problem Statement**: Prove that every integer n satisfies n = n.\n", encoding="utf-8")
    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="curated",
                title="Curated",
                source=str(curated),
                statement="Prove that every integer n satisfies n = n.",
                domain="number_theory",
                references=[str(curated)],
                metadata={"statement_quality": "exact", "statement_provenance": str(curated)},
            ),
            ProblemRecord(
                problem_id="remote-only",
                title="Remote Only",
                source="remote catalog",
                statement="Prove that every integer n satisfies n = n.",
                domain="number_theory",
                references=["https://example.test/live"],
            ),
        ],
        bank_path,
    )

    result = PortfolioCampaignRunner(repo_root=tmp_path).run_portfolio_campaign(
        bank=bank_path,
        run_name="source quality campaign",
        scout_limit=2,
        promote_top=1,
    )
    ranking = json.loads((tmp_path / result["ranking"]).read_text(encoding="utf-8"))["ranking"]
    by_id = {item["problem_id"]: item for item in ranking}

    assert by_id["curated"]["source_quality"]["tier"] == "trusted"
    assert "local_snapshot_available" in by_id["curated"]["source_quality"]["trust_reasons"]
    assert "remote_source_without_local_snapshot" in by_id["remote-only"]["source_quality"]["source_debt"]
