from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ara_math.artifact_graph import ArtifactGraph, load_artifact_graph, save_artifact_graph
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
    ProjectState,
    ProjectStatus,
    ReviewDecision,
    ReviewKind,
    ReviewRecord,
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
) -> list[WorkstreamRecord]:
    state = load_project_state(project_dir)
    closed_or_ready = {
        item.workstream_id
        for item in state.workstreams
        if item.status in {WorkstreamStatus.APPROVED, WorkstreamStatus.NEEDS_REVIEW}
    }
    candidates = [
        item
        for item in state.workstreams
        if item.status == WorkstreamStatus.PLANNED and all(dep in closed_or_ready for dep in item.dependencies)
    ]
    candidates.sort(key=lambda item: item.workstream_id)
    if limit is None:
        return candidates
    return candidates[:limit]


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

    lines.extend(["", "## Phase 1 Notes", "", "- LLM workstream execution and review-gate enforcement are not integrated yet.", ""])
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
