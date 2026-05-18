import json
from pathlib import Path

from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_memory import (
    load_claim_ledger,
    load_failed_routes,
    load_route_ledger,
    render_failed_route_prompt_block,
    retrieve_failed_routes,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _init_project(tmp_path: Path, problem_id: str) -> Path:
    project = tmp_path / "projects" / problem_id
    PortfolioCampaignRunner(repo_root=tmp_path).initialize_problem_project(
        project=project,
        problem_id=problem_id,
        state="active_attack",
    )
    (project / "problem.yaml").write_text(
        "\n".join(
            [
                f"problem_id: {problem_id}",
                "statement: Prove the P6 side-filter multiplicity bound.",
                "source: unit-test-source",
                "references:",
                "  - https://example.test/p6",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return project


def test_consolidates_proof_lean_review_failed_routes_and_global_indexes(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "p6-side-filter")
    (project / "proof" / "sketches" / "p6_side_filter.md").write_text(
        "\n".join(
            [
                "# P6 Side-Filter Route",
                "",
                "Claim ID: main",
                "Statement: The side-filter route would bound multiplicity.",
                "Claim status: sketch",
                "Route ID: p6-side-filter",
                "Target claim: main",
                "Route status: promising",
                "Core idea: Filter each side and count surviving pairs.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (project / "runs" / "p6" / "failed_routes.md").parent.mkdir(parents=True, exist_ok=True)
    (project / "runs" / "p6" / "failed_routes.md").write_text(
        "\n".join(
            [
                "# P6 side-filter multiplicity",
                "",
                "Route ID: p6-side-filter",
                "Failure mode: proof_gap",
                "Failed assertion: Side filters preserve multiplicity after every projection.",
                "Approach: Partition each side by residue filters and multiply counts.",
                "Resume condition: A multiplicity-preserving injection is proved.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    _write_json(
        project / "runs" / "lean" / "report.json",
        {
            "status": "verified",
            "run_name": "lean-p6",
            "target_theorem": "p6_side_filter_multiplicity_bound",
            "target_file": "formal/MathProject/P6.lean",
            "best_audit": {
                "verified": True,
                "build_status": "passed",
                "target": {
                    "found": True,
                    "kind": "theorem",
                    "name": "p6_side_filter_multiplicity_bound",
                    "full_name": "MathProject.p6_side_filter_multiplicity_bound",
                    "relative_path": "MathProject/P6.lean",
                    "line": 7,
                },
            },
        },
    )
    _write_json(
        project / "review" / "route_review.json",
        {
            "status": "reviewed",
            "claim_id": "main",
            "route_id": "p6-side-filter",
            "summary": "Reviewed enough to keep the route memory but not repeat the failed multiplicity step.",
        },
    )

    report = PortfolioCampaignRunner(repo_root=tmp_path).consolidate_problem_memory(project=project)

    claims = load_claim_ledger(project)["claims"]
    routes = load_route_ledger(project)["routes"]
    failed_routes = load_failed_routes(project)["failed_routes"]
    declarations = json.loads((project / "verified_declarations.json").read_text(encoding="utf-8"))
    theorem_index = json.loads((tmp_path / "artifacts" / "global_memory" / "theorem_asset_index.json").read_text(encoding="utf-8"))
    resume_pack = (project / "resume_pack.md").read_text(encoding="utf-8")

    assert report["schema_version"] == "amra.memory_consolidation.v1"
    assert {claim["claim_id"] for claim in claims} >= {"main", "p6_side_filter_multiplicity_bound"}
    assert any(claim["status"] == "lean_verified" for claim in claims)
    assert {route["route_id"] for route in routes} >= {"p6-side-filter", "lean:p6_side_filter_multiplicity_bound"}
    assert failed_routes[0]["route_id"] == "p6-side-filter"
    assert "Side filters preserve multiplicity" in failed_routes[0]["failed_assertion"]
    assert declarations["declarations"][0]["full_name"] == "MathProject.p6_side_filter_multiplicity_bound"
    assert theorem_index["verified_declarations"][0]["full_name"] == "MathProject.p6_side_filter_multiplicity_bound"
    assert "Do not repeat this route unless the resume condition is met." in resume_pack

    retrieval = retrieve_failed_routes(project, query="side filter multiplicity")
    prompt_block = render_failed_route_prompt_block(project, query="side filter multiplicity")

    assert retrieval["failed_routes"][0]["route_id"] == "p6-side-filter"
    assert "A multiplicity-preserving injection is proved." in prompt_block


def test_evaluate_problem_automatically_consolidates_before_scoring(tmp_path: Path) -> None:
    project = _init_project(tmp_path, "auto-consolidate")
    _write_json(
        project / "runs" / "lean" / "report.json",
        {
            "status": "verified",
            "run_name": "lean-auto",
            "target_theorem": "auto_consolidated_target",
            "best_audit": {
                "verified": True,
                "build_status": "passed",
                "target": {"found": True, "kind": "theorem", "name": "auto_consolidated_target"},
            },
        },
    )

    report = PortfolioCampaignRunner(repo_root=tmp_path).evaluate_problem(project=project, run_name="eval")

    theorem_index = json.loads((tmp_path / "artifacts" / "global_memory" / "theorem_asset_index.json").read_text(encoding="utf-8"))

    assert report["claim_count"] >= 1
    assert report["recommendation"] == "promote"
    assert report["memory_consolidation"]["verified_declaration_count"] == 1
    assert theorem_index["verified_declarations"][0]["full_name"] == "auto_consolidated_target"
