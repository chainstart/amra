from pathlib import Path

from ara_math.coordinator import (
    CoMathCoordinator,
    add_workstream,
    initialize_comath_project,
    render_project_dashboard,
)
from ara_math.uncertainty import SourceDebtStatus, UncertaintyItem, UncertaintyKind
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord


def test_dashboard_renders_project_status_workstreams_and_blockers(tmp_path: Path) -> None:
    project_dir = tmp_path / "toy-project"
    state = initialize_comath_project(
        project_dir,
        project_name="Toy Project",
        original_goal="Prove every toy integer is balanced.",
    )
    state.top_blocker_id = "source-gap"
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="source-main",
            kind=WorkstreamKind.SOURCE,
            goal="Source-certify the dense central block theorem.",
            blockers=["No exact citation yet."],
        ),
    )
    coordinator = CoMathCoordinator(project_dir)
    coordinator.record_uncertainty(
        UncertaintyItem(
            item_id="source-gap",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Dense central block theorem is not source-certified",
            description="The current route depends on a paper-level theorem whose assumptions are not aligned.",
            owner_workstream_id="source-main",
            claim_id="original-theorem",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
            severity="high",
        )
    )

    dashboard = render_project_dashboard(project_dir)

    assert "# CoMath Dashboard: Toy Project" in dashboard
    assert "Prove every toy integer is balanced." in dashboard
    assert "`source-gap` (source_debt; source debt: `external_theorem_needed`)" in dashboard
    assert "| source-main | source | planned | Source-certify the dense central block theorem. | 1 |" in dashboard
    assert "Local runner wrappers, scheduler state, and review-gate records are persisted" in dashboard
    assert (project_dir / "comath" / "project_dashboard.md").read_text(encoding="utf-8") == dashboard


def test_dashboard_reports_failed_routes_and_empty_state(tmp_path: Path) -> None:
    project_dir = tmp_path / "empty-project"
    coordinator = CoMathCoordinator(project_dir)
    coordinator.initialize(project_name="Empty Project", original_goal="Resolve the empty project.")
    empty_dashboard = coordinator.render_dashboard()

    assert "- No open CoMath blockers recorded." in empty_dashboard
    assert "- No workstreams have been added." in empty_dashboard

    coordinator.record_failed_route(
        route_id="route-001",
        summary="Try to close the theorem by assuming the missing source theorem",
        failure_reason="Moves the burden into unverified source debt.",
        owner_workstream_id="proof-main",
    )
    dashboard = coordinator.render_dashboard()

    assert "## Failed Routes" in dashboard
    assert "| route-001 | proof-main | Moves the burden into unverified source debt. |" in dashboard
