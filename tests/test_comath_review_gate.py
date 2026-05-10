import json
from pathlib import Path

from ara_math.artifact_graph import DependencyRelation, load_artifact_graph, save_artifact_graph
from ara_math.coordinator import (
    add_workstream,
    comath_paths,
    initialize_comath_project,
    review_workstream_gate,
    update_workstream_status,
)
from ara_math.uncertainty import (
    SourceDebtStatus,
    UncertaintyItem,
    UncertaintyKind,
    UncertaintyLedger,
    save_uncertainty_ledger,
)
from ara_math.workstreams import DependencyStatus, WorkstreamKind, WorkstreamRecord, WorkstreamStatus


def _write_clean_lean(project_dir: Path, relative_path: str) -> None:
    path = project_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("theorem clean_gate_target : True := by\n  trivial\n", encoding="utf-8")


def _write_bad_lean(project_dir: Path, relative_path: str) -> None:
    path = project_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "axiom unsafe_bridge : True",
                "theorem bad_gate_target : True := by",
                "  have h : True := by",
                "    admit",
                "  sorry",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_review_gate_approves_clean_workstream_with_full_local_evidence(tmp_path: Path) -> None:
    project_dir = tmp_path / "clean-project"
    initialize_comath_project(project_dir, project_name="Clean", original_goal="Prove the clean theorem.")
    _write_clean_lean(project_dir, "formal/Main.lean")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Close the original theorem.",
            claim_ids=["main-claim"],
            artifact_ids=["main-lean"],
        ),
    )

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(
        claim_id="main-claim",
        title="Main claim",
        statement="Prove the clean theorem.",
        workstream_id="proof-main",
    )
    graph.record_lean_declaration(
        node_id="main-lean",
        lean_name="clean_gate_target",
        path="formal/Main.lean",
        claim_id="main-claim",
        workstream_id="proof-main",
    )
    graph.add_edge(
        source_id="main-claim",
        target_id="original-theorem",
        relation=DependencyRelation.DEPENDS_ON,
        status=DependencyStatus.SATISFIED,
    )
    save_artifact_graph(paths.artifact_graph, graph)

    payload = review_workstream_gate(project_dir, "proof-main")
    status = json.loads((paths.workstream_dir("proof-main") / "status.json").read_text(encoding="utf-8"))
    decision = json.loads(
        (paths.workstream_dir("proof-main") / "reviews" / "round-001" / "decision.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["approved"] is True
    assert payload["decision"] == "approved"
    assert status["status"] == WorkstreamStatus.APPROVED.value
    assert [item["kind"] for item in payload["reviews"]] == ["logic", "source", "lean", "computation", "global"]
    assert {item["decision"] for item in payload["reviews"]} == {"approved"}
    assert decision["report"]["dependency_path"] == ["main-claim", "original-theorem"]


def test_review_gate_blocks_debt_lean_findings_statement_drift_and_missing_path(tmp_path: Path) -> None:
    project_dir = tmp_path / "blocked-project"
    initialize_comath_project(project_dir, project_name="Blocked", original_goal="Prove the blocked theorem.")
    _write_bad_lean(project_dir, "formal/Bad.lean")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Try a risky route.",
            claim_ids=["route-claim"],
            artifact_ids=["bad-lean", "bad-cert"],
            metadata={"statement_alignment": "drift"},
        ),
    )

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(
        claim_id="route-claim",
        title="Drifted route claim",
        statement="A weaker theorem.",
        workstream_id="proof-main",
        metadata={"statement_drift": True},
    )
    graph.record_lean_declaration(
        node_id="bad-lean",
        lean_name="bad_gate_target",
        path="formal/Bad.lean",
        claim_id="route-claim",
        workstream_id="proof-main",
    )
    graph.record_computation_certificate(
        node_id="bad-cert",
        label="Search certificate",
        workstream_id="proof-main",
        metadata={"verified": False},
    )
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = UncertaintyLedger(ledger_id="blocked-ledger")
    for item in [
        UncertaintyItem(
            item_id="source-gap",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Primary theorem has not been source-certified",
            owner_workstream_id="proof-main",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
        ),
        UncertaintyItem(
            item_id="lemma-gap",
            kind=UncertaintyKind.THEOREM_DEBT,
            title="Missing bridge lemma",
            owner_workstream_id="proof-main",
        ),
        UncertaintyItem(
            item_id="drift-gap",
            kind=UncertaintyKind.STATEMENT_DRIFT,
            title="Route proves a weaker theorem",
            owner_workstream_id="proof-main",
        ),
        UncertaintyItem(
            item_id="compute-gap",
            kind=UncertaintyKind.COMPUTATION_DEBT,
            title="Search certificate has not been reproduced",
            owner_workstream_id="proof-main",
        ),
    ]:
        ledger.upsert_item(item)
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    payload = review_workstream_gate(project_dir, "proof-main")
    status = json.loads((paths.workstream_dir("proof-main") / "status.json").read_text(encoding="utf-8"))
    blocker_codes = {item["code"] for item in payload["report"]["blockers"]}
    decisions = {item["kind"]: item["decision"] for item in payload["report"]["review_decisions"]}
    lean_blocker = next(item for item in payload["report"]["blockers"] if item["code"] == "lean_findings")

    assert payload["approved"] is False
    assert payload["decision"] == "needs_revision"
    assert status["status"] == WorkstreamStatus.REVISION.value
    assert {
        "source_debt",
        "theorem_debt",
        "statement_drift",
        "lean_findings",
        "computation_debt",
        "computation_certificate_unverified",
        "missing_original_dependency_path",
    } <= blocker_codes
    assert decisions == {
        "logic": "needs_revision",
        "source": "needs_revision",
        "lean": "needs_revision",
        "computation": "needs_revision",
        "global": "needs_revision",
    }
    assert lean_blocker["metadata"]["counts"]["sorry"] == 1
    assert lean_blocker["metadata"]["counts"]["admit"] == 1
    assert lean_blocker["metadata"]["counts"]["axiom"] == 1


def test_review_gate_can_require_existing_review_decisions(tmp_path: Path) -> None:
    project_dir = tmp_path / "manual-review-project"
    initialize_comath_project(project_dir, project_name="Manual", original_goal="Prove the manual theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Source-check the theorem.",
            claim_ids=["source-claim"],
        ),
    )
    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(claim_id="source-claim", title="Source claim", workstream_id="source-main")
    graph.add_edge(
        source_id="source-claim",
        target_id="original-theorem",
        relation=DependencyRelation.DEPENDS_ON,
        status=DependencyStatus.SATISFIED,
    )
    save_artifact_graph(paths.artifact_graph, graph)

    payload = review_workstream_gate(project_dir, "source-main", require_existing_reviews=True)
    blocker_codes = {item["code"] for item in payload["report"]["blockers"]}

    assert payload["approved"] is False
    assert blocker_codes == {"missing_review_decision"}


def test_status_update_to_approved_is_review_gated(tmp_path: Path) -> None:
    project_dir = tmp_path / "status-update-project"
    initialize_comath_project(project_dir, project_name="Status", original_goal="Prove the status theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="proof-main",
            kind=WorkstreamKind.PROOF,
            goal="Approve without evidence.",
        ),
    )

    workstream = update_workstream_status(project_dir, "proof-main", WorkstreamStatus.APPROVED)

    assert workstream.status == WorkstreamStatus.REVISION
    assert any("No dependency path connects workstream" in blocker for blocker in workstream.blockers)
