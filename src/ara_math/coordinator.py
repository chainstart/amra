from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ara_math.artifact_graph import ArtifactGraph, DependencyRelation, load_artifact_graph, save_artifact_graph
from ara_math.review_gate import (
    DEFAULT_REVIEW_KINDS,
    ReviewGateReport,
    evaluate_workstream_review_gate,
    normalize_review_kind,
)
from ara_math.uncertainty import (
    FailedRouteRecord,
    UncertaintyItem,
    UncertaintyLedger,
    append_failed_route_jsonl,
    load_failed_routes_jsonl,
    load_uncertainty_ledger,
    save_uncertainty_ledger,
    SourceDebtStatus,
    UncertaintyKind,
)
from ara_math.workspace import (
    append_jsonl,
    read_json,
    read_text,
    record_event,
    slugify,
    write_json,
    write_text,
)
from ara_math.workstreams import (
    ClaimRecord,
    ClaimStatus,
    DependencyStatus,
    ProjectState,
    ProjectStatus,
    ReviewDecision,
    ReviewKind,
    ReviewRecord,
    WorkstreamKind,
    WorkstreamRecord,
    WorkstreamStatus,
    utc_now_iso,
)


@dataclass(frozen=True, slots=True)
class CoMathPaths:
    project_dir: Path

    @property
    def root(self) -> Path:
        return self.project_dir / "comath"

    @property
    def project_state(self) -> Path:
        return self.root / "project_state.json"

    @property
    def dashboard(self) -> Path:
        return self.root / "project_dashboard.md"

    @property
    def artifact_graph(self) -> Path:
        return self.root / "artifact_graph.json"

    @property
    def uncertainty_ledger(self) -> Path:
        return self.root / "uncertainty_ledger.json"

    @property
    def failed_routes(self) -> Path:
        return self.root / "failed_routes.jsonl"

    @property
    def messages(self) -> Path:
        return self.root / "messages.jsonl"

    @property
    def workstreams(self) -> Path:
        return self.root / "workstreams"

    def workstream_dir(self, workstream_id: str) -> Path:
        return self.workstreams / workstream_id


def comath_paths(project_dir: Path) -> CoMathPaths:
    return CoMathPaths(Path(project_dir))


def _project_defaults(project_dir: Path, project_name: str | None, original_goal: str | None) -> tuple[str, str, str]:
    manifest = read_json(project_dir / "project_manifest.json", default={}) or {}
    manifest_problem = manifest.get("problem", {}) if isinstance(manifest.get("problem"), dict) else {}
    name = project_name or str(manifest.get("project_name") or manifest.get("project_slug") or project_dir.name)
    project_id = str(manifest.get("project_slug") or slugify(name))
    exact_statement = read_text(project_dir / "idea" / "exact_statement.md", default="").strip()
    problem_statement = str(manifest_problem.get("statement", "")).strip()
    goal = (original_goal or exact_statement or problem_statement or "").strip()
    return project_id, name, goal


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def _load_project_state(path: Path) -> ProjectState:
    return ProjectState.from_dict(read_json(path))


def load_project_state(project_dir: Path) -> ProjectState:
    paths = comath_paths(Path(project_dir))
    if not paths.project_state.exists():
        return initialize_comath_project(Path(project_dir))
    return _load_project_state(paths.project_state)


def save_project_state(project_dir: Path, state: ProjectState) -> None:
    write_json(comath_paths(Path(project_dir)).project_state, state.to_dict())


def initialize_comath_project(
    project_dir: Path,
    *,
    project_name: str | None = None,
    original_goal: str | None = None,
) -> ProjectState:
    project_dir = Path(project_dir)
    paths = comath_paths(project_dir)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.workstreams.mkdir(parents=True, exist_ok=True)
    _touch(paths.messages)
    _touch(paths.failed_routes)

    if paths.project_state.exists():
        state = _load_project_state(paths.project_state)
    else:
        project_id, name, goal = _project_defaults(project_dir, project_name, original_goal)
        state = ProjectState(
            project_id=project_id,
            project_name=name,
            original_goal=goal,
            metadata={"phase": "schema_and_dashboard"},
        )
        save_project_state(project_dir, state)

    graph_changed = False
    if paths.artifact_graph.exists():
        graph = load_artifact_graph(paths.artifact_graph)
    else:
        graph = ArtifactGraph(
            graph_id=f"{state.project_id}-artifact-graph",
            metadata={"project_id": state.project_id},
        )
        graph_changed = True
    if not graph.get_node("original-theorem"):
        graph.record_claim(
            claim_id="original-theorem",
            title="Original theorem",
            statement=state.original_goal,
            metadata={"root": True},
        )
        graph_changed = True
    if graph_changed:
        save_artifact_graph(paths.artifact_graph, graph)

    ledger_changed = False
    if paths.uncertainty_ledger.exists():
        ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    else:
        ledger = UncertaintyLedger(
            ledger_id=f"{state.project_id}-uncertainty-ledger",
            metadata={"project_id": state.project_id},
        )
        ledger_changed = True
    jsonl_routes = load_failed_routes_jsonl(paths.failed_routes)
    known_fingerprints = {route.fingerprint for route in ledger.failed_routes}
    for route in jsonl_routes:
        if route.fingerprint not in known_fingerprints:
            ledger.failed_routes.append(route)
            known_fingerprints.add(route.fingerprint)
            ledger_changed = True
    if ledger_changed:
        save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    render_project_dashboard(project_dir, state=state, graph=graph, ledger=ledger)
    record_event(project_dir, stage="comath", event="comath_initialized", details={"project_id": state.project_id})
    return state


def add_workstream(project_dir: Path, workstream: WorkstreamRecord) -> WorkstreamRecord:
    state = load_project_state(project_dir)
    paths = comath_paths(Path(project_dir))
    state.upsert_workstream(workstream)
    save_project_state(project_dir, state)

    workstream_dir = paths.workstream_dir(workstream.workstream_id)
    (workstream_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (workstream_dir / "reviews").mkdir(parents=True, exist_ok=True)
    if not (workstream_dir / "goal.md").exists():
        write_text(workstream_dir / "goal.md", workstream.goal.rstrip() + "\n")
    write_json(workstream_dir / "status.json", workstream.to_dict())
    if not (workstream_dir / "report.md").exists():
        write_text(workstream_dir / "report.md", f"# {workstream.workstream_id}\n\nNo report has been written yet.\n")
    if not (workstream_dir / "blockers.md").exists():
        blocker_lines = [f"- {blocker}" for blocker in workstream.blockers] or ["- No blockers recorded."]
        write_text(workstream_dir / "blockers.md", "# Blockers\n\n" + "\n".join(blocker_lines) + "\n")
    _touch(workstream_dir / "messages.jsonl")

    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "workstream_added",
            "workstream_id": workstream.workstream_id,
            "kind": workstream.kind.value,
        },
    )
    render_project_dashboard(project_dir)
    return workstream


def update_workstream_status(
    project_dir: Path,
    workstream_id: str,
    status: WorkstreamStatus | str,
    *,
    blocker: str | None = None,
) -> WorkstreamRecord:
    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is None:
        raise KeyError(f"Unknown workstream: {workstream_id}")
    target_status = WorkstreamStatus.coerce(status)
    if target_status == WorkstreamStatus.APPROVED:
        payload = review_workstream_gate(project_dir, workstream_id)
        return WorkstreamRecord.from_dict(payload["workstream"])

    workstream.mark_status(target_status, blocker=blocker)
    state.upsert_workstream(workstream)
    save_project_state(project_dir, state)
    write_json(comath_paths(Path(project_dir)).workstream_dir(workstream_id) / "status.json", workstream.to_dict())
    render_project_dashboard(project_dir)
    return workstream


def _next_review_round_id(reviews_dir: Path) -> str:
    round_numbers: list[int] = []
    if reviews_dir.exists():
        for child in reviews_dir.iterdir():
            if child.is_dir() and child.name.startswith("round-"):
                suffix = child.name.removeprefix("round-")
                if suffix.isdigit():
                    round_numbers.append(int(suffix))
    next_number = (max(round_numbers) + 1) if round_numbers else 1
    return f"round-{next_number:03d}"


def _review_kinds(values: list[ReviewKind | str] | None) -> list[ReviewKind]:
    kinds: list[ReviewKind] = []
    seen: set[str] = set()
    aliases = {
        "strategy": ReviewKind.GLOBAL.value,
        "global_strategy": ReviewKind.GLOBAL.value,
        "repro": ReviewKind.COMPUTATION.value,
        "compute": ReviewKind.COMPUTATION.value,
        "reproducibility": ReviewKind.COMPUTATION.value,
    }
    for value in values or [ReviewKind.LOGIC]:
        normalized = str(value).strip().lower().replace("-", "_")
        raw_value = value if isinstance(value, ReviewKind) else aliases.get(normalized, normalized)
        kind = normalize_review_kind(raw_value)
        if kind.value in seen:
            continue
        kinds.append(kind)
        seen.add(kind.value)
    return kinds


def review_workstream_placeholder(
    project_dir: Path,
    workstream_id: str,
    *,
    reviewers: list[ReviewKind | str] | None = None,
    decision: ReviewDecision | str = ReviewDecision.PENDING,
    reviewer: str = "local-state",
    notes: str = "",
) -> dict[str, Any]:
    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is None:
        raise KeyError(f"Unknown workstream: {workstream_id}")

    paths = comath_paths(Path(project_dir))
    kinds = _review_kinds(reviewers)
    decision_value = ReviewDecision.coerce(decision)
    reviews_root = paths.workstream_dir(workstream_id) / "reviews"
    round_id = _next_review_round_id(reviews_root)
    review_dir = reviews_root / round_id
    review_dir.mkdir(parents=True, exist_ok=True)

    records: list[ReviewRecord] = []
    for kind in kinds:
        review = ReviewRecord(
            review_id=f"{workstream_id}:{round_id}:{kind.value}",
            kind=kind,
            target_id=workstream_id,
            decision=decision_value,
            reviewer=reviewer,
            notes=notes,
            metadata={"mode": "state_only", "round_id": round_id},
        )
        state.upsert_review(review)
        records.append(review)
        note_lines = [
            f"# {kind.value.replace('_', ' ').title()} Review",
            "",
            f"- Workstream: `{workstream_id}`",
            f"- Decision: `{decision_value.value}`",
            "- Mode: state-only placeholder",
            "",
            "No automated reviewer was invoked for this placeholder review.",
            "",
        ]
        if notes.strip():
            note_lines.extend(["## Notes", "", notes.strip(), ""])
        write_text(review_dir / f"{kind.value}_review.md", "\n".join(note_lines))

    workstream.mark_status(WorkstreamStatus.NEEDS_REVIEW)
    state.upsert_workstream(workstream)
    state.status = ProjectStatus.REVIEW_GATE
    state.updated_at = utc_now_iso()
    save_project_state(project_dir, state)
    write_json(paths.workstream_dir(workstream_id) / "status.json", workstream.to_dict())

    decision_payload = {
        "round_id": round_id,
        "workstream_id": workstream_id,
        "mode": "state_only",
        "decision": decision_value.value,
        "reviewers": [kind.value for kind in kinds],
        "review_ids": [record.review_id for record in records],
        "notes": notes,
        "generated_at": utc_now_iso(),
    }
    write_json(review_dir / "decision.json", decision_payload)
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "workstream_review_placeholder",
            "workstream_id": workstream_id,
            "round_id": round_id,
            "reviewers": [kind.value for kind in kinds],
            "decision": decision_value.value,
        },
    )
    render_project_dashboard(project_dir)
    return {
        "project_dir": str(project_dir),
        "workstream_id": workstream_id,
        "round_id": round_id,
        "review_dir": str(review_dir),
        "mode": "state_only",
        "decision": decision_value.value,
        "reviews": [record.to_dict() for record in records],
        "workstream": workstream.to_dict(),
    }


_GATE_BLOCKER_PREFIX = "[review-gate] "


def _review_gate_markdown(report: ReviewGateReport, kind: ReviewKind, notes: str) -> str:
    decision = next(item for item in report.review_decisions if item.kind == kind)
    blockers_by_id = {blocker.blocker_id: blocker for blocker in report.blockers}
    lines = [
        f"# {kind.value.replace('_', ' ').title()} Review Gate",
        "",
        f"- Workstream: `{report.workstream_id}`",
        f"- Decision: `{decision.decision.value}`",
        "- Mode: local review gate",
        "",
    ]
    if decision.blocker_ids:
        lines.extend(["## Blockers", ""])
        for blocker_id in decision.blocker_ids:
            blocker = blockers_by_id[blocker_id]
            lines.append(f"- `{blocker.code}`: {blocker.message}")
        lines.append("")
    else:
        lines.extend(["No local blockers were found for this review dimension.", ""])
    if notes.strip():
        lines.extend(["## Notes", "", notes.strip(), ""])
    return "\n".join(lines)


def review_workstream_gate(
    project_dir: Path,
    workstream_id: str,
    *,
    reviewers: list[ReviewKind | str] | None = None,
    reviewer: str = "local-review-gate",
    notes: str = "",
    require_existing_reviews: bool = False,
) -> dict[str, Any]:
    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is None:
        raise KeyError(f"Unknown workstream: {workstream_id}")

    paths = comath_paths(Path(project_dir))
    graph = load_artifact_graph(paths.artifact_graph)
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    kinds = _review_kinds(reviewers) if reviewers else list(DEFAULT_REVIEW_KINDS)
    report = evaluate_workstream_review_gate(
        state=state,
        workstream=workstream,
        graph=graph,
        ledger=ledger,
        project_dir=Path(project_dir),
        required_review_kinds=kinds,
        require_existing_reviews=require_existing_reviews,
    )

    reviews_root = paths.workstream_dir(workstream_id) / "reviews"
    round_id = _next_review_round_id(reviews_root)
    review_dir = reviews_root / round_id
    review_dir.mkdir(parents=True, exist_ok=True)

    review_records: list[ReviewRecord] = []
    for decision in report.review_decisions:
        record = ReviewRecord(
            review_id=f"{workstream_id}:{round_id}:{decision.kind.value}",
            kind=decision.kind,
            target_id=workstream_id,
            decision=decision.decision,
            reviewer=reviewer,
            blocker_ids=decision.blocker_ids,
            notes=decision.notes,
            metadata={"mode": "review_gate", "round_id": round_id},
        )
        state.upsert_review(record)
        review_records.append(record)
        write_text(review_dir / f"{decision.kind.value}_review.md", _review_gate_markdown(report, decision.kind, notes))

    workstream.mark_status(report.workstream_status)
    workstream.blockers = [item for item in workstream.blockers if not item.startswith(_GATE_BLOCKER_PREFIX)]
    if not report.approved:
        workstream.blockers.extend(f"{_GATE_BLOCKER_PREFIX}{blocker.message}" for blocker in report.blockers)
    workstream.metadata["latest_review_gate"] = {
        "round_id": round_id,
        "decision": report.decision.value,
        "approved": report.approved,
        "blocker_count": len(report.blockers),
        "generated_at": report.generated_at,
    }
    state.upsert_workstream(workstream)
    state.status = ProjectStatus.REVIEW_GATE
    state.updated_at = utc_now_iso()
    save_project_state(project_dir, state)
    write_json(paths.workstream_dir(workstream_id) / "status.json", workstream.to_dict())

    decision_payload = {
        "round_id": round_id,
        "workstream_id": workstream_id,
        "mode": "review_gate",
        "decision": report.decision.value,
        "approved": report.approved,
        "reviewers": [decision.kind.value for decision in report.review_decisions],
        "review_ids": [record.review_id for record in review_records],
        "notes": notes,
        "report": report.to_dict(),
        "generated_at": utc_now_iso(),
    }
    write_json(review_dir / "decision.json", decision_payload)
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "workstream_review_gate",
            "workstream_id": workstream_id,
            "round_id": round_id,
            "decision": report.decision.value,
            "approved": report.approved,
            "blocker_count": len(report.blockers),
        },
    )
    render_project_dashboard(project_dir)
    return {
        "project_dir": str(project_dir),
        "workstream_id": workstream_id,
        "round_id": round_id,
        "review_dir": str(review_dir),
        "mode": "review_gate",
        "decision": report.decision.value,
        "approved": report.approved,
        "reviews": [record.to_dict() for record in review_records],
        "workstream": workstream.to_dict(),
        "report": report.to_dict(),
    }


def record_uncertainty_item(project_dir: Path, item: UncertaintyItem) -> UncertaintyItem:
    paths = comath_paths(Path(project_dir))
    initialize_comath_project(Path(project_dir))
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    ledger.upsert_item(item)
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)
    render_project_dashboard(project_dir, ledger=ledger)
    return item


def record_failed_route(
    project_dir: Path,
    *,
    route_id: str,
    summary: str,
    failure_reason: str,
    owner_workstream_id: str = "",
    claim_id: str = "",
    metadata: dict[str, Any] | None = None,
) -> FailedRouteRecord:
    paths = comath_paths(Path(project_dir))
    initialize_comath_project(Path(project_dir))
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    existing = ledger.find_failed_route(summary)
    route = ledger.add_failed_route(
        route_id=route_id,
        summary=summary,
        failure_reason=failure_reason,
        owner_workstream_id=owner_workstream_id,
        claim_id=claim_id,
        metadata=metadata,
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)
    if existing is None:
        append_failed_route_jsonl(paths.failed_routes, route)
    render_project_dashboard(project_dir, ledger=ledger)
    return route


def select_next_workstreams(
    project_dir: Path,
    *,
    limit: int | None = None,
    include_revision: bool = True,
) -> list[WorkstreamRecord]:
    state = load_project_state(project_dir)
    paths = comath_paths(Path(project_dir))
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    closed_or_ready = {
        item.workstream_id
        for item in state.workstreams
        if item.status in {WorkstreamStatus.APPROVED, WorkstreamStatus.NEEDS_REVIEW}
    }
    eligible_statuses = {WorkstreamStatus.PLANNED}
    if include_revision:
        eligible_statuses.add(WorkstreamStatus.REVISION)
    candidates = [
        item
        for item in state.workstreams
        if item.status in eligible_statuses and all(dep in closed_or_ready for dep in item.dependencies)
    ]
    candidates.sort(key=lambda item: _workstream_schedule_key(item, ledger))
    if limit is None:
        return candidates
    return candidates[:limit]


_BOTTLENECK_KIND_ORDER = {
    WorkstreamKind.SOURCE: 0,
    WorkstreamKind.LEAN: 1,
    WorkstreamKind.PROOF: 2,
    WorkstreamKind.COMPUTE: 3,
    WorkstreamKind.REVIEW: 4,
}

_UNCERTAINTY_KIND_TO_WORKSTREAM = {
    "source_debt": WorkstreamKind.SOURCE,
    "statement_drift": WorkstreamKind.SOURCE,
    "theorem_debt": WorkstreamKind.PROOF,
    "unresolved_assumption": WorkstreamKind.PROOF,
    "computation_debt": WorkstreamKind.COMPUTE,
    "stalled_workstream": WorkstreamKind.REVIEW,
}


def _active_bottleneck_item(ledger: UncertaintyLedger) -> UncertaintyItem | None:
    blockers = ledger.blocking_items()
    if not blockers:
        return None
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    blockers.sort(key=lambda item: (severity_rank.get(item.severity.lower(), 4), item.created_at, item.item_id))
    return blockers[0]


def _active_bottleneck_kind(ledger: UncertaintyLedger) -> WorkstreamKind | None:
    blocker = _active_bottleneck_item(ledger)
    if blocker is None:
        return None
    return _UNCERTAINTY_KIND_TO_WORKSTREAM.get(blocker.kind.value)


def _workstream_schedule_key(workstream: WorkstreamRecord, ledger: UncertaintyLedger) -> tuple[int, int, int, int, str, str]:
    bottleneck = _active_bottleneck_item(ledger)
    bottleneck_kind = _active_bottleneck_kind(ledger)
    owner_rank = 0 if bottleneck is not None and bottleneck.owner_workstream_id == workstream.workstream_id else 1
    bottleneck_rank = 0 if bottleneck_kind is not None and workstream.kind == bottleneck_kind else 1
    status_rank = 0 if workstream.status == WorkstreamStatus.REVISION else 1
    kind_rank = _BOTTLENECK_KIND_ORDER.get(workstream.kind, 99)
    return (owner_rank, bottleneck_rank, status_rank, kind_rank, workstream.created_at, workstream.workstream_id)


def _normalized_blockers(values: list[Any]) -> tuple[str, ...]:
    normalized: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text:
            continue
        if "] " in text and text.startswith("["):
            text = text.split("] ", 1)[1].strip()
        normalized.append(text)
    return tuple(sorted(set(normalized)))


def _run_blocker_signature(run: dict[str, Any]) -> tuple[str, ...]:
    blockers = run.get("blockers", [])
    if not isinstance(blockers, list):
        blockers = [blockers]
    return _normalized_blockers(blockers)


def _consecutive_stalled_run_count(workstream: WorkstreamRecord) -> int:
    runs = workstream.metadata.get("runner_runs", [])
    if not isinstance(runs, list) or not runs:
        return 0
    latest = runs[-1] if isinstance(runs[-1], dict) else {}
    latest_signature = _run_blocker_signature(latest)
    if not latest_signature:
        return 0
    count = 0
    for raw_run in reversed(runs):
        run = raw_run if isinstance(raw_run, dict) else {}
        status = str(run.get("workstream_status") or run.get("status") or "").strip().lower()
        if status not in {"revision", "escalated", "failed", "blocked"} and not run.get("blockers"):
            break
        if _run_blocker_signature(run) != latest_signature:
            break
        count += 1
    return count


def should_freeze_workstream(workstream: WorkstreamRecord, *, stalled_run_threshold: int = 2) -> bool:
    if stalled_run_threshold <= 0:
        return False
    if workstream.status != WorkstreamStatus.REVISION:
        return False
    return _consecutive_stalled_run_count(workstream) >= stalled_run_threshold


def freeze_workstream(
    project_dir: Path,
    workstream_id: str,
    *,
    reason: str,
    loop_id: str = "",
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    paths = comath_paths(project_dir)
    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is None:
        raise KeyError(f"Unknown workstream: {workstream_id}")

    freeze_dir = paths.workstream_dir(workstream_id) / "freeze_package"
    freeze_dir.mkdir(parents=True, exist_ok=True)
    package = {
        "generated_at": utc_now_iso(),
        "loop_id": loop_id,
        "workstream_id": workstream_id,
        "reason": reason,
        "goal": workstream.goal,
        "status_before_freeze": workstream.status.value,
        "blockers": list(workstream.blockers),
        "run_dirs": list(workstream.run_dirs),
        "artifact_paths": list(workstream.artifact_paths),
        "latest_runner": workstream.metadata.get("latest_runner", {}),
        "stalled_run_count": _consecutive_stalled_run_count(workstream),
    }
    write_json(freeze_dir / "freeze.json", package)
    write_text(
        freeze_dir / "summary.md",
        "\n".join(
            [
                f"# Freeze Package: {workstream_id}",
                "",
                f"- Reason: {reason}",
                f"- Previous status: `{workstream.status.value}`",
                f"- Stalled run count: `{package['stalled_run_count']}`",
                "",
                "## Blockers",
                "",
                *([f"- {blocker}" for blocker in workstream.blockers] or ["- No blockers recorded."]),
                "",
            ]
        ),
    )

    workstream.mark_status(WorkstreamStatus.FROZEN, blocker=f"[scheduler] Frozen: {reason}")
    workstream.metadata["freeze_package"] = {
        "path": str(freeze_dir),
        "reason": reason,
        "loop_id": loop_id,
        "generated_at": package["generated_at"],
    }
    state.upsert_workstream(workstream)
    if all(item.status in {WorkstreamStatus.APPROVED, WorkstreamStatus.NEEDS_REVIEW, WorkstreamStatus.FROZEN} for item in state.workstreams):
        state.status = ProjectStatus.FROZEN
    state.updated_at = utc_now_iso()
    save_project_state(project_dir, state)
    write_json(paths.workstream_dir(workstream_id) / "status.json", workstream.to_dict())

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    route = ledger.add_failed_route(
        route_id=f"{workstream_id}-frozen-{slugify(package['generated_at'])}",
        summary=workstream.goal,
        failure_reason=reason,
        owner_workstream_id=workstream_id,
        metadata={"loop_id": loop_id, "freeze_package": str(freeze_dir)},
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)
    append_failed_route_jsonl(paths.failed_routes, route)
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "workstream_frozen",
            "workstream_id": workstream_id,
            "reason": reason,
            "loop_id": loop_id,
            "freeze_package": str(freeze_dir),
        },
    )
    record_event(
        project_dir,
        stage="comath",
        event="workstream_frozen",
        details={"workstream_id": workstream_id, "reason": reason, "loop_id": loop_id},
    )
    render_project_dashboard(project_dir, ledger=ledger)
    return {"workstream": workstream.to_dict(), "freeze_package": package, "freeze_dir": str(freeze_dir)}


def _freeze_stalled_workstreams(
    project_dir: Path,
    *,
    loop_id: str,
    stalled_run_threshold: int,
) -> list[dict[str, Any]]:
    state = load_project_state(project_dir)
    frozen: list[dict[str, Any]] = []
    for workstream in list(state.workstreams):
        if should_freeze_workstream(workstream, stalled_run_threshold=stalled_run_threshold):
            frozen.append(
                freeze_workstream(
                    project_dir,
                    workstream.workstream_id,
                    reason=f"Repeated non-decreasing blockers across {stalled_run_threshold} scheduler runs.",
                    loop_id=loop_id,
                )
            )
    return frozen


def _loop_report_dir(project_dir: Path, run_name: str | None) -> tuple[str, Path]:
    loop_id = slugify(run_name or f"loop-{utc_now_iso()}")
    return loop_id, comath_paths(project_dir).root / "loop_runs" / loop_id


def run_comath_loop(
    project_dir: Path,
    *,
    max_workstreams: int = 1,
    time_budget_seconds: int = 300,
    executor: Any | None = None,
    executor_name: str | None = None,
    executor_options: dict[str, Any] | None = None,
    per_workstream_options: dict[str, dict[str, Any]] | None = None,
    repo_root: Path | None = None,
    freeze_stalled_after: int = 2,
    run_name: str | None = None,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    loop_id, report_dir = _loop_report_dir(project_dir, run_name)
    report_dir.mkdir(parents=True, exist_ok=True)
    started_at = utc_now_iso()
    deadline = time.monotonic() + max(0, time_budget_seconds)
    executed: list[dict[str, Any]] = []
    frozen: list[dict[str, Any]] = []
    stop_reason = "max_workstreams_reached"

    state = load_project_state(project_dir)
    state.status = ProjectStatus.WORKSTREAMS_RUNNING
    state.updated_at = utc_now_iso()
    save_project_state(project_dir, state)
    render_project_dashboard(project_dir)

    while len(executed) < max_workstreams:
        frozen.extend(_freeze_stalled_workstreams(project_dir, loop_id=loop_id, stalled_run_threshold=freeze_stalled_after))
        if time_budget_seconds > 0 and time.monotonic() >= deadline:
            stop_reason = "time_budget_exhausted"
            break
        candidates = select_next_workstreams(project_dir, limit=1)
        if not candidates:
            stop_reason = "no_ready_workstreams"
            break
        workstream = candidates[0]
        options = dict(executor_options or {})
        options.update((per_workstream_options or {}).get(workstream.workstream_id, {}))
        result = execute_workstream(
            project_dir,
            workstream.workstream_id,
            executor=executor,
            executor_name=executor_name,
            options=options,
            repo_root=repo_root,
        )
        executed.append(result)
        render_project_dashboard(project_dir)

    if len(executed) >= max_workstreams:
        stop_reason = "max_workstreams_reached"

    state = load_project_state(project_dir)
    open_candidates = select_next_workstreams(project_dir)
    if open_candidates:
        state.status = ProjectStatus.WORKSTREAMS_RUNNING
    elif state.workstreams and all(item.status == WorkstreamStatus.FROZEN for item in state.workstreams):
        state.status = ProjectStatus.FROZEN
    elif any(item.status == WorkstreamStatus.NEEDS_REVIEW for item in state.workstreams):
        state.status = ProjectStatus.REVIEW_GATE
    elif any(item.status == WorkstreamStatus.APPROVED for item in state.workstreams):
        state.status = ProjectStatus.PARTIAL
    state.updated_at = utc_now_iso()
    save_project_state(project_dir, state)

    report = {
        "project_dir": str(project_dir),
        "loop_id": loop_id,
        "started_at": started_at,
        "completed_at": utc_now_iso(),
        "max_workstreams": max_workstreams,
        "time_budget_seconds": time_budget_seconds,
        "stop_reason": stop_reason,
        "executed_count": len(executed),
        "frozen_count": len(frozen),
        "executed": executed,
        "frozen": frozen,
        "state": state.to_dict(),
        "dashboard_path": str(comath_paths(project_dir).dashboard),
    }
    write_json(report_dir / "report.json", report)
    write_text(
        report_dir / "summary.md",
        "\n".join(
            [
                f"# CoMath Loop Run: {loop_id}",
                "",
                f"- Stop reason: `{stop_reason}`",
                f"- Executed workstreams: `{len(executed)}`",
                f"- Frozen workstreams: `{len(frozen)}`",
                f"- Dashboard: `{comath_paths(project_dir).dashboard}`",
                "",
            ]
        ),
    )
    append_jsonl(
        comath_paths(project_dir).messages,
        {
            "ts": utc_now_iso(),
            "type": "comath_loop_completed",
            "loop_id": loop_id,
            "stop_reason": stop_reason,
            "executed_count": len(executed),
            "frozen_count": len(frozen),
            "report_path": str(report_dir / "report.json"),
        },
    )
    render_project_dashboard(project_dir)
    return report


def execute_workstream(
    project_dir: Path,
    workstream_id: str,
    *,
    executor: Any | None = None,
    executor_name: str | None = None,
    options: dict[str, Any] | None = None,
    repo_root: Path | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    from ara_math.comath_runners import execute_workstream as _execute_workstream

    return _execute_workstream(
        project_dir,
        workstream_id,
        executor=executor,
        executor_name=executor_name,
        options=options,
        repo_root=repo_root,
        **kwargs,
    )


def execute_next_workstreams(
    project_dir: Path,
    *,
    limit: int | None = None,
    executor_options: dict[str, dict[str, Any]] | None = None,
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    from ara_math.comath_runners import execute_next_workstreams as _execute_next_workstreams

    return _execute_next_workstreams(
        project_dir,
        limit=limit,
        executor_options=executor_options,
        repo_root=repo_root,
    )


CES75_ERDOS866_PROJECT = "erdos-866-ai-continuation-20260505"
CES75_DENSE_BLOCKER_ID = "source-dense-central-block-source-debt"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_ces75_project_dir(repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    return root / "projects" / CES75_ERDOS866_PROJECT


def _upsert_claim_record(state: ProjectState, claim: ClaimRecord) -> None:
    for index, existing in enumerate(state.claims):
        if existing.claim_id == claim.claim_id:
            if not claim.created_at:
                claim.created_at = existing.created_at
            state.claims[index] = claim
            state.updated_at = utc_now_iso()
            return
    state.add_claim(claim)


def _write_workstream_template(paths: CoMathPaths, workstream: WorkstreamRecord, detail_lines: list[str]) -> None:
    workstream_dir = paths.workstream_dir(workstream.workstream_id)
    report_path = workstream_dir / "report.md"
    if report_path.exists() and "Bootstrap Template" not in report_path.read_text(encoding="utf-8"):
        return
    write_text(
        report_path,
        "\n".join(
            [
                f"# Bootstrap Template: {workstream.workstream_id}",
                "",
                f"- Kind: `{workstream.kind.value}`",
                f"- Goal: {workstream.goal}",
                "",
                "## Initial Focus",
                "",
                *detail_lines,
                "",
            ]
        ),
    )


def bootstrap_ces75_erdos866_workstreams(
    project_dir: Path | None = None,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Initialize the active CES75/Erdos866 project with safe CoMath workstreams.

    This function intentionally writes only under the project's `comath/`
    directory and leaves the existing Lean workspace untouched.
    """

    repo_root = repo_root or _repo_root()
    project_dir = Path(project_dir) if project_dir is not None else _default_ces75_project_dir(repo_root)
    original_goal = (
        "Close Erdos 866 through the CES75 Theorem 4 six-witness source route, "
        "with dense central block source debt explicit."
    )
    initialize_comath_project(project_dir, project_name="CES75 / Erdos 866 CoMath", original_goal=original_goal)
    paths = comath_paths(project_dir)

    context_paths = [
        str(repo_root / "artifacts" / "design" / "ai_comath_migration_plan_20260510.md"),
        str(repo_root / "artifacts" / "literature" / "ces75" / "theorem4_formalization_plan_20260510.md"),
        str(repo_root / "artifacts" / "literature" / "ces75" / "theorem4_source_corrections_20260510.md"),
        str(project_dir / "formal" / "MathProject" / "MainClaim.lean"),
    ]
    workstreams = [
        WorkstreamRecord(
            workstream_id="source-dense-central-block",
            kind=WorkstreamKind.SOURCE,
            goal="Prove or source-certify the dense central block theorem from the CES75 hypotheses.",
            claim_ids=["dense-central-block-source"],
            blockers=["Dense central block source theorem is not source-certified."],
            metadata={
                "executor": "source_literature",
                "bottleneck": "source_debt",
                "context_paths": context_paths,
                "source_target": "CES75 central even count and dyadic subinterval extraction",
            },
        ),
        WorkstreamRecord(
            workstream_id="lean-current-final-window",
            kind=WorkstreamKind.LEAN,
            goal="Preserve and clean the existing final-window, dyadic, and six-witness Lean chain.",
            claim_ids=["lean-final-window-chain"],
            blockers=["Lean chain must remain aligned with the unapproved CES75 source theorem."],
            metadata={
                "executor": "lean_formalization",
                "workspace": str(project_dir / "formal"),
                "target_file": "MathProject/MainClaim.lean",
                "target_theorem": "erdos866_g6_sqrt_order_of_CES75_theorem4_integer_source",
                "context_paths": context_paths,
            },
        ),
        WorkstreamRecord(
            workstream_id="source-audit-ces75-theorem4",
            kind=WorkstreamKind.SOURCE,
            goal="Align CES75 Theorem 4 source text, corrected OCR, and the Lean source statement exactly.",
            claim_ids=["ces75-theorem4-source-alignment"],
            blockers=["CES75 Theorem 4 source text and Lean statement alignment is pending."],
            metadata={
                "executor": "source_literature",
                "bottleneck": "source_alignment",
                "context_paths": context_paths,
                "source_target": "Choi--Erdos--Szemeredi Theorem 4, pp. 41-42",
            },
        ),
        WorkstreamRecord(
            workstream_id="global-review",
            kind=WorkstreamKind.REVIEW,
            goal="Verify that the dependency graph closes the original Erdos 866 statement without hiding source debt.",
            dependencies=[
                "source-dense-central-block",
                "lean-current-final-window",
                "source-audit-ces75-theorem4",
            ],
            claim_ids=["global-erdos866-closure"],
            blockers=["Global closure is blocked until source and Lean workstreams are approved."],
            metadata={"reviewers": ["logic", "source", "lean", "global"], "context_paths": context_paths},
        ),
    ]
    for workstream in workstreams:
        add_workstream(project_dir, workstream)

    state = load_project_state(project_dir)
    state.top_blocker_id = CES75_DENSE_BLOCKER_ID
    state.metadata["bootstrap_template"] = {
        "name": "ces75_erdos866",
        "generated_at": utc_now_iso(),
        "source": "artifacts/design/ai_comath_migration_plan_20260510.md",
    }
    for claim in [
        ClaimRecord(
            claim_id="dense-central-block-source",
            title="Dense central block source theorem",
            statement="CES75 source route must prove or cite the central even count and dense dyadic subinterval block.",
            status=ClaimStatus.HYPOTHESIS,
            owner_workstream_id="source-dense-central-block",
            source_status="external_theorem_needed",
        ),
        ClaimRecord(
            claim_id="lean-final-window-chain",
            title="Current final-window Lean chain",
            statement="Existing final-window, dyadic, and six-witness Lean chain in MathProject/MainClaim.lean.",
            status=ClaimStatus.LEAN_STUBBED,
            owner_workstream_id="lean-current-final-window",
            source_status="source_formalization_needed",
        ),
        ClaimRecord(
            claim_id="ces75-theorem4-source-alignment",
            title="CES75 Theorem 4 source alignment",
            statement="Theorem 4 source text, corrected OCR, and Lean source statement must match.",
            status=ClaimStatus.HYPOTHESIS,
            owner_workstream_id="source-audit-ces75-theorem4",
            source_status="source_formalization_needed",
        ),
        ClaimRecord(
            claim_id="global-erdos866-closure",
            title="Global Erdos 866 closure",
            statement="The dependency graph closes the original Erdos 866 statement without stronger hidden assumptions.",
            status=ClaimStatus.ROUTE_CANDIDATE,
            owner_workstream_id="global-review",
            dependency_ids=[
                "dense-central-block-source",
                "lean-final-window-chain",
                "ces75-theorem4-source-alignment",
            ],
        ),
    ]:
        _upsert_claim_record(state, claim)
    save_project_state(project_dir, state)

    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(
        claim_id="dense-central-block-source",
        title="Dense central block source theorem",
        statement="Source-certify the central even count and dyadic subinterval extraction used by CES75.",
        status=ClaimStatus.HYPOTHESIS,
        workstream_id="source-dense-central-block",
        metadata={"source_debt_status": SourceDebtStatus.EXTERNAL_THEOREM_NEEDED.value},
    )
    graph.record_claim(
        claim_id="lean-final-window-chain",
        title="Current final-window Lean chain",
        statement="Preserve the already engineered final-window/dyadic/six-witness Lean chain.",
        status=ClaimStatus.LEAN_STUBBED,
        workstream_id="lean-current-final-window",
    )
    graph.record_claim(
        claim_id="ces75-theorem4-source-alignment",
        title="CES75 Theorem 4 source alignment",
        statement="Align source text, OCR corrections, and Lean statement exactly.",
        status=ClaimStatus.HYPOTHESIS,
        workstream_id="source-audit-ces75-theorem4",
    )
    graph.record_claim(
        claim_id="global-erdos866-closure",
        title="Global Erdos 866 closure",
        statement="Close the original theorem through approved source and Lean dependencies.",
        status=ClaimStatus.ROUTE_CANDIDATE,
        workstream_id="global-review",
    )
    graph.record_lean_declaration(
        node_id="lean-final-window-mainclaim",
        lean_name="erdos866_g6_sqrt_order_of_CES75_theorem4_integer_source",
        path=str(project_dir / "formal" / "MathProject" / "MainClaim.lean"),
        claim_id="lean-final-window-chain",
        workstream_id="lean-current-final-window",
        metadata={"do_not_mutate": True},
    )
    graph.record_source(
        node_id="ces75-theorem4-formalization-plan",
        label="CES75 Theorem 4 formalization plan",
        path=str(repo_root / "artifacts" / "literature" / "ces75" / "theorem4_formalization_plan_20260510.md"),
        metadata={"workstream_id": "source-audit-ces75-theorem4"},
    )
    graph.record_source(
        node_id="ces75-theorem4-source-corrections",
        label="CES75 Theorem 4 source corrections",
        path=str(repo_root / "artifacts" / "literature" / "ces75" / "theorem4_source_corrections_20260510.md"),
        metadata={"workstream_id": "source-audit-ces75-theorem4"},
    )
    for source_id, target_id, status, rationale in [
        ("dense-central-block-source", "original-theorem", DependencyStatus.PENDING, "Key source blocker for Erdos 866 closure."),
        ("lean-final-window-chain", "dense-central-block-source", DependencyStatus.PENDING, "Lean chain must not hide dense-block source debt."),
        ("ces75-theorem4-source-alignment", "dense-central-block-source", DependencyStatus.PENDING, "Theorem 4 alignment controls the dense block source claim."),
        ("global-erdos866-closure", "lean-final-window-chain", DependencyStatus.PENDING, "Global review needs Lean chain status."),
        ("global-erdos866-closure", "ces75-theorem4-source-alignment", DependencyStatus.PENDING, "Global review needs source statement alignment."),
        ("global-erdos866-closure", "original-theorem", DependencyStatus.PENDING, "Global closure must connect to original theorem."),
    ]:
        graph.add_edge(
            source_id=source_id,
            target_id=target_id,
            relation=DependencyRelation.DEPENDS_ON,
            status=status,
            rationale=rationale,
        )
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    ledger.upsert_item(
        UncertaintyItem(
            item_id=CES75_DENSE_BLOCKER_ID,
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Dense central block theorem is the current source-level blocker",
            description=(
                "The CES75 route needs the central even count and dense dyadic subinterval "
                "source theorem proved or source-certified before the Lean chain can be promoted."
            ),
            owner_workstream_id="source-dense-central-block",
            claim_id="dense-central-block-source",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
            severity="critical",
            metadata={"dashboard_priority": True},
        )
    )
    ledger.upsert_item(
        UncertaintyItem(
            item_id="ces75-theorem4-source-audit",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="CES75 Theorem 4 source text must be aligned with the Lean statement",
            description="Corrected OCR and page-image interpretation must match the Lean source statement exactly.",
            owner_workstream_id="source-audit-ces75-theorem4",
            claim_id="ces75-theorem4-source-alignment",
            source_debt_status=SourceDebtStatus.SOURCE_FORMALIZATION_NEEDED,
            severity="high",
        )
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    templates = {
        "source-dense-central-block": [
            "- Certify the central even count line and dyadic subinterval extraction.",
            "- Decide whether the current Lean dense interval theorem is a source theorem, a formalization target, or a stronger local substitute.",
        ],
        "lean-current-final-window": [
            "- Treat `formal/MathProject/MainClaim.lean` as preserved state.",
            "- Do not rewrite the Lean proof file during bootstrap.",
        ],
        "source-audit-ces75-theorem4": [
            "- Compare CES75 Theorem 4 source text, source corrections, and Lean statement names.",
            "- Record any hidden strengthening before review.",
        ],
        "global-review": [
            "- Check that every dependency path reaches `original-theorem` through approved source and Lean workstreams.",
            "- Reject closure if dense central block source debt remains open.",
        ],
    }
    state = load_project_state(project_dir)
    for workstream in state.workstreams:
        if workstream.workstream_id in templates:
            _write_workstream_template(paths, workstream, templates[workstream.workstream_id])

    render_project_dashboard(project_dir, ledger=ledger)
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "ces75_erdos866_bootstrap",
            "workstream_ids": [workstream.workstream_id for workstream in workstreams],
            "top_blocker_id": CES75_DENSE_BLOCKER_ID,
        },
    )
    record_event(
        project_dir,
        stage="comath",
        event="ces75_erdos866_bootstrap",
        details={"top_blocker_id": CES75_DENSE_BLOCKER_ID},
    )
    return {
        "project_dir": str(project_dir),
        "dashboard_path": str(paths.dashboard),
        "top_blocker_id": CES75_DENSE_BLOCKER_ID,
        "workstreams": [workstream.to_dict() for workstream in load_project_state(project_dir).workstreams],
    }


def _md_cell(value: Any) -> str:
    text = str(value).replace("\n", " ").strip()
    text = text.replace("|", "\\|")
    return text or "-"


def _truncate(value: str, length: int = 120) -> str:
    text = " ".join(value.split())
    if len(text) <= length:
        return text
    return text[: length - 3].rstrip() + "..."


def _counts_text(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{key}: {counts[key]}" for key in sorted(counts))


def _top_blocker(state: ProjectState, ledger: UncertaintyLedger) -> UncertaintyItem | None:
    if state.top_blocker_id:
        item = ledger.get_item(state.top_blocker_id)
        if item:
            return item
    blockers = ledger.blocking_items()
    if not blockers:
        return None
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    blockers.sort(key=lambda item: (severity_rank.get(item.severity.lower(), 4), item.created_at, item.item_id))
    return blockers[0]


def render_project_dashboard(
    project_dir: Path,
    *,
    state: ProjectState | None = None,
    graph: ArtifactGraph | None = None,
    ledger: UncertaintyLedger | None = None,
    write: bool = True,
) -> str:
    project_dir = Path(project_dir)
    paths = comath_paths(project_dir)
    if state is None:
        if not paths.project_state.exists():
            state = initialize_comath_project(project_dir)
        else:
            state = load_project_state(project_dir)
    graph = graph or load_artifact_graph(paths.artifact_graph)
    ledger = ledger or load_uncertainty_ledger(paths.uncertainty_ledger)

    blocker = _top_blocker(state, ledger)
    lines = [
        f"# CoMath Dashboard: {state.project_name}",
        "",
        f"- Generated: {utc_now_iso()}",
        f"- Project status: `{state.status.value}`",
        f"- Workstreams: {len(state.workstreams)}",
        f"- Claims: {len(state.claims)}",
        f"- Reviews: {len(state.reviews)}",
        "",
        "## Original Goal",
        "",
        state.original_goal.strip() or "No original goal recorded.",
        "",
        "## Current Original-Theorem Blocker",
        "",
    ]
    if blocker is None:
        lines.append("- No open CoMath blockers recorded.")
    else:
        source_status = f"; source debt: `{blocker.source_debt_status.value}`" if blocker.source_debt_status else ""
        lines.append(
            f"- `{blocker.item_id}` ({blocker.kind.value}{source_status}): {_truncate(blocker.title)}"
        )
        if blocker.owner_workstream_id:
            lines.append(f"- Owner: `{blocker.owner_workstream_id}`")
        if blocker.description:
            lines.append(f"- Detail: {_truncate(blocker.description, 180)}")
    lines.extend(["", "## Workstreams", ""])
    if state.workstreams:
        lines.extend(["| Workstream | Kind | Status | Goal | Blockers |", "| --- | --- | --- | --- | --- |"])
        for workstream in sorted(state.workstreams, key=lambda item: item.workstream_id):
            lines.append(
                "| "
                + " | ".join(
                    [
                        _md_cell(workstream.workstream_id),
                        _md_cell(workstream.kind.value),
                        _md_cell(workstream.status.value),
                        _md_cell(_truncate(workstream.goal, 80)),
                        _md_cell(len(workstream.blockers)),
                    ]
                )
                + " |"
            )
    else:
        lines.append("- No workstreams have been added.")

    unresolved_edges = graph.unresolved_edges()
    lines.extend(
        [
            "",
            "## Artifact Graph",
            "",
            f"- Nodes: {len(graph.nodes)} ({_counts_text(graph.counts_by_kind())})",
            f"- Edges: {len(graph.edges)}",
            f"- Unresolved dependency edges: {len(unresolved_edges)}",
            "",
            "## Uncertainty Ledger",
            "",
            f"- Open items: {len(ledger.open_items())}",
            f"- Items by kind: {_counts_text(ledger.counts_by_kind())}",
            f"- Failed routes: {len(ledger.failed_routes)}",
        ]
    )
    open_items = ledger.open_items()
    if open_items:
        lines.extend(["", "| Item | Kind | Status | Owner | Title |", "| --- | --- | --- | --- | --- |"])
        for item in sorted(open_items, key=lambda entry: entry.item_id):
            lines.append(
                "| "
                + " | ".join(
                    [
                        _md_cell(item.item_id),
                        _md_cell(item.kind.value),
                        _md_cell(item.status.value),
                        _md_cell(item.owner_workstream_id),
                        _md_cell(_truncate(item.title, 80)),
                    ]
                )
                + " |"
            )

    if ledger.failed_routes:
        lines.extend(["", "## Failed Routes", "", "| Route | Owner | Reason |", "| --- | --- | --- |"])
        for route in sorted(ledger.failed_routes, key=lambda entry: entry.route_id):
            lines.append(
                "| "
                + " | ".join(
                    [
                        _md_cell(route.route_id),
                        _md_cell(route.owner_workstream_id),
                        _md_cell(_truncate(route.failure_reason, 100)),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## CoMath Notes",
            "",
            "- Local runner wrappers, scheduler state, and review-gate records are persisted under `comath/`.",
            "- External LLM execution is only used when a selected runner is explicitly configured to use it.",
            "",
        ]
    )
    dashboard = "\n".join(lines)
    if write:
        write_text(paths.dashboard, dashboard)
    return dashboard


def project_dashboard(project_dir: Path) -> str:
    return render_project_dashboard(project_dir)


def init_comath_project(
    project_dir: Path,
    *,
    project_name: str | None = None,
    original_goal: str | None = None,
) -> ProjectState:
    return initialize_comath_project(project_dir, project_name=project_name, original_goal=original_goal)


@dataclass(slots=True)
class CoMathCoordinator:
    project_dir: Path

    def initialize(self, *, project_name: str | None = None, original_goal: str | None = None) -> ProjectState:
        return initialize_comath_project(self.project_dir, project_name=project_name, original_goal=original_goal)

    def load_state(self) -> ProjectState:
        return load_project_state(self.project_dir)

    def save_state(self, state: ProjectState) -> None:
        save_project_state(self.project_dir, state)

    def add_workstream(self, workstream: WorkstreamRecord) -> WorkstreamRecord:
        return add_workstream(self.project_dir, workstream)

    def update_workstream_status(
        self,
        workstream_id: str,
        status: WorkstreamStatus | str,
        *,
        blocker: str | None = None,
    ) -> WorkstreamRecord:
        return update_workstream_status(self.project_dir, workstream_id, status, blocker=blocker)

    def review_workstream_placeholder(
        self,
        workstream_id: str,
        *,
        reviewers: list[ReviewKind | str] | None = None,
        decision: ReviewDecision | str = ReviewDecision.PENDING,
        reviewer: str = "local-state",
        notes: str = "",
    ) -> dict[str, Any]:
        return review_workstream_placeholder(
            self.project_dir,
            workstream_id,
            reviewers=reviewers,
            decision=decision,
            reviewer=reviewer,
            notes=notes,
        )

    def review_workstream_gate(
        self,
        workstream_id: str,
        *,
        reviewers: list[ReviewKind | str] | None = None,
        reviewer: str = "local-review-gate",
        notes: str = "",
        require_existing_reviews: bool = False,
    ) -> dict[str, Any]:
        return review_workstream_gate(
            self.project_dir,
            workstream_id,
            reviewers=reviewers,
            reviewer=reviewer,
            notes=notes,
            require_existing_reviews=require_existing_reviews,
        )

    def record_uncertainty(self, item: UncertaintyItem) -> UncertaintyItem:
        return record_uncertainty_item(self.project_dir, item)

    def record_failed_route(
        self,
        *,
        route_id: str,
        summary: str,
        failure_reason: str,
        owner_workstream_id: str = "",
        claim_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> FailedRouteRecord:
        return record_failed_route(
            self.project_dir,
            route_id=route_id,
            summary=summary,
            failure_reason=failure_reason,
            owner_workstream_id=owner_workstream_id,
            claim_id=claim_id,
            metadata=metadata,
        )

    def select_next_workstreams(self, *, limit: int | None = None) -> list[WorkstreamRecord]:
        return select_next_workstreams(self.project_dir, limit=limit)

    def run_loop(
        self,
        *,
        max_workstreams: int = 1,
        time_budget_seconds: int = 300,
        executor: Any | None = None,
        executor_name: str | None = None,
        executor_options: dict[str, Any] | None = None,
        per_workstream_options: dict[str, dict[str, Any]] | None = None,
        repo_root: Path | None = None,
        freeze_stalled_after: int = 2,
        run_name: str | None = None,
    ) -> dict[str, Any]:
        return run_comath_loop(
            self.project_dir,
            max_workstreams=max_workstreams,
            time_budget_seconds=time_budget_seconds,
            executor=executor,
            executor_name=executor_name,
            executor_options=executor_options,
            per_workstream_options=per_workstream_options,
            repo_root=repo_root,
            freeze_stalled_after=freeze_stalled_after,
            run_name=run_name,
        )

    def bootstrap_ces75_erdos866(self, *, repo_root: Path | None = None) -> dict[str, Any]:
        return bootstrap_ces75_erdos866_workstreams(self.project_dir, repo_root=repo_root)

    def execute_workstream(
        self,
        workstream_id: str,
        *,
        executor: Any | None = None,
        executor_name: str | None = None,
        options: dict[str, Any] | None = None,
        repo_root: Path | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return execute_workstream(
            self.project_dir,
            workstream_id,
            executor=executor,
            executor_name=executor_name,
            options=options,
            repo_root=repo_root,
            **kwargs,
        )

    def execute_next_workstreams(
        self,
        *,
        limit: int | None = None,
        executor_options: dict[str, dict[str, Any]] | None = None,
        repo_root: Path | None = None,
    ) -> list[dict[str, Any]]:
        return execute_next_workstreams(
            self.project_dir,
            limit=limit,
            executor_options=executor_options,
            repo_root=repo_root,
        )

    def render_dashboard(self) -> str:
        return render_project_dashboard(self.project_dir)
