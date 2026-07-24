#!/usr/bin/env python3
"""Build and maintain the rotating master ledger for the 630-problem Erdős cohort.

The frozen cohort and its first-pass analyses remain immutable evidence inputs.
This script overlays a portfolio policy and an append-only event log, then
materialises:

* one machine-readable 630-row master ledger;
* the current bounded rotation queue;
* a human-readable Chinese plan and compact all-problem register.

The policy deliberately separates original-problem closure, publication work,
and audits of existing solution claims.  A high first-pass feasibility score is
treated as testability, not as evidence that a problem is close to closure.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = REPO_ROOT / "data/research_open/erdos_rotation/policy.json"
DEFAULT_EVENTS = REPO_ROOT / "data/research_open/erdos_rotation/events.jsonl"
DEFAULT_COHORT_ROOT = REPO_ROOT / "artifacts/erdos_630_initial_analysis"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "artifacts/erdos_master_rotation"
DEFAULT_PLAN_PATH = REPO_ROOT / "docs/erdos_master_rotation_plan.zh.md"
FOLLOWUP_ROOT = REPO_ROOT / "artifacts/erdos_followup_20260719"

ATTACK_PHASES = {"intake", "deep_attack", "independent_qa", "formalization"}
RESET_OUTCOMES = {
    "candidate_closure",
    "closed_verified",
    "closing_lemma_proved",
    "main_order_improved",
    "route_family_eliminated",
    "strict_closure_distance_reduction",
}
STAGNANT_OUTCOMES = {
    "no_progress",
    "budget_exhausted_no_progress",
    "local_only",
    "route_repeated",
    "deep_campaign_saturated",
}

LANE_LIFECYCLE = {
    "closure_core": "active",
    "intake_active": "active",
    "resolution_audit": "active",
    "paper_conversion": "separate_track",
    "resolution_ready": "external_status_wait",
    "finite_resolution": "backlog",
    "statement_audit": "backlog",
    "discovery_high": "backlog",
    "discovery_standard": "backlog",
    "deep_backlog": "backlog",
    "cooldown": "cooldown",
    "closed_watch": "closed",
}

QUEUE_BUDGET_KEYS = {
    "closure_core": "deep_attack_budget_seconds_per_problem",
    "intake": "intake_budget_seconds_per_problem",
    "resolution_audit": "status_audit_budget_seconds_per_problem",
    "paper_conversion": None,
    "status_refresh": "status_audit_budget_seconds_per_problem",
}

QUEUE_COMPLETION_PHASES = {
    "closure_core": {"deep_attack", "independent_qa", "formalization", "decision"},
    "intake": {"intake", "decision"},
    "resolution_audit": {"resolution_audit", "decision"},
    "paper_conversion": {"paper_conversion", "decision"},
    "status_refresh": {"status_refresh", "decision"},
}

EVENT_REQUIRED_FIELDS = {
    "event_id",
    "occurred_at",
    "cycle_id",
    "problem_id",
    "phase",
    "outcome",
    "agent_hours",
    "original_problem_closed",
    "q2_candidate",
    "closure_distance_before",
    "closure_distance_after",
    "summary_zh",
    "blocker_zh",
    "next_action_zh",
    "evidence_paths",
}


def parse_event_time(value: Any) -> datetime:
    """Return an aware UTC timestamp for chronological event ordering."""
    text = str(value)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise RuntimeError(f"invalid occurred_at timestamp: {text}") from error
    if parsed.tzinfo is None:
        raise RuntimeError(f"occurred_at timestamp must include a timezone: {text}")
    return parsed.astimezone(timezone.utc)


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"{path}:{line_number}: invalid JSON: {error}") from error
        missing = EVENT_REQUIRED_FIELDS - set(event)
        extra = set(event) - EVENT_REQUIRED_FIELDS
        if missing or extra:
            raise RuntimeError(
                f"{path}:{line_number}: missing={sorted(missing)} extra={sorted(extra)}"
            )
        try:
            parse_event_time(event["occurred_at"])
        except RuntimeError as error:
            raise RuntimeError(f"{path}:{line_number}: {error}") from error
        event_id = str(event["event_id"])
        if event_id in event_ids:
            raise RuntimeError(f"{path}:{line_number}: duplicate event_id {event_id}")
        event_ids.add(event_id)
        events.append(event)
    return events


def load_initial_analyses(cohort_root: Path) -> dict[str, dict[str, Any]]:
    analyses: dict[str, dict[str, Any]] = {}
    for path in sorted((cohort_root / "results").glob("*.json"), key=lambda item: int(item.stem)):
        payload = read_json(path, default={})
        analysis = payload.get("analysis", {})
        problem_id = str(analysis.get("problem_id", path.stem))
        analyses[problem_id] = analysis
    return analyses


def load_followup_audits() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    nonopen: dict[str, dict[str, Any]] = {}
    for name in ("audit_nonopen_a.json", "audit_nonopen_b.json"):
        payload = read_json(FOLLOWUP_ROOT / name, default={})
        for row in payload.get("entries", []):
            nonopen[str(row.get("problem_id"))] = row

    conflicts: dict[str, dict[str, Any]] = {}
    payload = read_json(FOLLOWUP_ROOT / "audit_open_conflicts.json", default={})
    for row in payload.get("entries", []):
        conflicts[str(row.get("problem_id"))] = row
    return nonopen, conflicts


def normalise_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def cycle_number(cycle_id: Any) -> int | None:
    match = re.fullmatch(r"R([0-9]+)", str(cycle_id or ""))
    return int(match.group(1)) if match else None


def statement_type(statement: str, policy: dict[str, Any]) -> str:
    rules = policy["statement_type_rules"]
    has_binary = any(marker.lower() in statement.lower() for marker in rules["binary_markers"])
    has_open = any(marker.lower() in statement.lower() for marker in rules["open_ended_markers"])
    if has_binary and not has_open:
        return "binary_decision"
    if has_open:
        return "open_ended_estimate"
    if re.search(r"\b(smallest|largest|minimal|maximal|which)\b", statement, re.I):
        return "exact_or_characterisation"
    return "mixed_or_unspecified"


def default_lane(
    cohort_row: dict[str, Any],
    analysis: dict[str, Any],
    *,
    conflict_audit: dict[str, Any] | None,
    legacy_deep_ids: set[str],
) -> str:
    problem_id = str(cohort_row["problem_id"])
    status = normalise_text(cohort_row.get("current_status")).lower()
    verdict = normalise_text(analysis.get("verdict")).lower()
    score = int(analysis.get("feasibility_score", 0))

    if status == "falsifiable":
        return "finite_resolution"
    if status != "open":
        return "closed_watch"
    if conflict_audit or verdict in {"known_resolution", "counterexample", "independent"}:
        return "resolution_audit"
    if verdict == "malformed":
        return "statement_audit"
    if problem_id in legacy_deep_ids:
        return "cooldown"
    if verdict == "blocked" or score <= 4:
        return "deep_backlog"
    if score >= 7 and verdict in {"promising", "partial"}:
        return "discovery_high"
    return "discovery_standard"


def default_closure_distance(
    lane: str,
    assessment_type: str,
    analysis: dict[str, Any],
) -> int:
    if lane in {"closed_watch", "resolution_ready"}:
        return 0
    if lane == "resolution_audit":
        return 1
    if lane == "finite_resolution":
        return 2
    if lane == "statement_audit":
        return 4
    if lane == "cooldown":
        return 4
    if analysis.get("verdict") == "blocked":
        return 5
    if assessment_type == "binary_decision" and int(analysis.get("feasibility_score", 0)) >= 7:
        return 3
    if assessment_type == "open_ended_estimate":
        return 4
    return 3


def default_priority(
    cohort_row: dict[str, Any],
    analysis: dict[str, Any],
    assessment_type: str,
    lane: str,
    closure_distance: int,
) -> int:
    score = int(analysis.get("feasibility_score", 0))
    verdict = normalise_text(analysis.get("verdict")).lower()
    priority = score * 6
    priority += {"promising": 12, "partial": 7, "known_resolution": 10}.get(verdict, 0)
    priority += 8 if assessment_type == "binary_decision" else 0
    priority -= 8 if assessment_type == "open_ended_estimate" else 0
    priority += 2 if analysis.get("confidence") == "high" else 0
    priority += 1 if normalise_text(cohort_row.get("current_formalized")).lower() == "yes" else 0
    priority += max(0, 5 - closure_distance) * 3
    if lane == "cooldown":
        priority -= 20
    if lane == "deep_backlog":
        priority -= 10
    if lane == "closed_watch":
        priority = 0
    return max(0, min(100, priority))


def compact_evidence_paths(row: dict[str, Any] | None) -> list[str]:
    if not row:
        return []
    paths: list[str] = []
    for evidence in row.get("evidence", []):
        if not isinstance(evidence, dict):
            continue
        url = normalise_text(evidence.get("url"))
        if url:
            paths.append(url)
    return paths[:8]


def aggregate_events(
    events: Iterable[dict[str, Any]],
    legacy_ids: set[str],
    legacy_streak: int,
) -> dict[str, dict[str, Any]]:
    aggregates: dict[str, dict[str, Any]] = {}
    by_problem: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        problem_id = event.get("problem_id")
        if problem_id is not None:
            by_problem[str(problem_id)].append(event)

    for problem_id, problem_events in by_problem.items():
        ordered = sorted(
            problem_events,
            key=lambda row: (parse_event_time(row["occurred_at"]), row["event_id"]),
        )
        streak = legacy_streak if problem_id in legacy_ids else 0
        attempts = 0
        hours = 0.0
        latest: dict[str, Any] | None = None
        closure_distance: int | None = None
        closed = False
        q2_candidate = False
        for event in ordered:
            latest = event
            hours += float(event.get("agent_hours", 0))
            if event.get("phase") in ATTACK_PHASES:
                attempts += 1
            outcome = str(event.get("outcome"))
            if outcome in RESET_OUTCOMES:
                streak = 0
            elif outcome in STAGNANT_OUTCOMES:
                streak += 1
            if event.get("closure_distance_after") is not None:
                closure_distance = int(event["closure_distance_after"])
            closed = closed or bool(event.get("original_problem_closed"))
            q2_candidate = q2_candidate or bool(event.get("q2_candidate"))
        aggregates[problem_id] = {
            "attempt_count": attempts,
            "registered_agent_hours": round(hours, 6),
            "no_progress_streak": streak,
            "last_event": latest,
            "event_closure_distance": closure_distance,
            "closed_by_event": closed,
            "q2_candidate": q2_candidate,
        }
    return aggregates


def build_problem_rows(
    *,
    policy: dict[str, Any],
    cohort_root: Path,
    events: list[dict[str, Any]],
    cycle_id: str,
) -> list[dict[str, Any]]:
    cohort_payload = read_json(cohort_root / "cohort.json", default={})
    cohort = cohort_payload.get("problems", [])
    cohort_generated_at = cohort_payload.get("generated_at", "")
    expected = int(policy["cohort"]["expected_problem_count"])
    if len(cohort) != expected:
        raise RuntimeError(f"Expected {expected} cohort problems, found {len(cohort)}")

    analyses = load_initial_analyses(cohort_root)
    if len(analyses) != expected:
        raise RuntimeError(f"Expected {expected} initial analyses, found {len(analyses)}")

    nonopen_audits, conflict_audits = load_followup_audits()
    legacy = policy["legacy_deep_campaign"]
    legacy_ids = set(map(str, legacy["problem_ids"]))
    event_aggregates = aggregate_events(
        events,
        legacy_ids,
        int(legacy["default_no_progress_streak"]),
    )
    overrides = policy.get("manual_overrides", {})

    rows: list[dict[str, Any]] = []
    for cohort_row in sorted(cohort, key=lambda item: int(item["problem_id"])):
        problem_id = str(cohort_row["problem_id"])
        analysis = analyses[problem_id]
        kind = statement_type(str(cohort_row.get("statement", "")), policy)
        nonopen_audit = nonopen_audits.get(problem_id)
        conflict_audit = conflict_audits.get(problem_id)
        lane = default_lane(
            cohort_row,
            analysis,
            conflict_audit=conflict_audit,
            legacy_deep_ids=legacy_ids,
        )
        distance = default_closure_distance(lane, kind, analysis)
        proximity = max(0, 10 - 2 * distance)
        priority = default_priority(cohort_row, analysis, kind, lane, distance)
        override = overrides.get(problem_id, {})
        lane = override.get("lane", lane)
        distance = int(override.get("closure_distance", distance))
        proximity = int(override.get("closure_proximity_score", max(0, 10 - 2 * distance)))
        priority = int(override.get("priority_score", priority))

        event_state = event_aggregates.get(
            problem_id,
            {
                "attempt_count": 0,
                "registered_agent_hours": 0.0,
                "no_progress_streak": (
                    int(legacy["default_no_progress_streak"]) if problem_id in legacy_ids else 0
                ),
                "last_event": None,
                "event_closure_distance": None,
                "closed_by_event": False,
                "q2_candidate": False,
            },
        )
        latest = event_state["last_event"]
        if event_state["event_closure_distance"] is not None:
            distance = int(event_state["event_closure_distance"])
            proximity = max(proximity, max(0, 10 - 2 * distance))
        if event_state["closed_by_event"]:
            lane = "closed_watch"
            distance = 0
            proximity = 10
            priority = 0
        elif "lane" not in override and latest and event_state["no_progress_streak"] >= 2:
            current_cycle = cycle_number(cycle_id)
            last_cycle = cycle_number(latest.get("cycle_id"))
            cooldown_cycles = int(
                policy["rotation_policy"]["cooldown_cycles_after_two_stagnant_deep_rounds"]
            )
            if (
                current_cycle is not None
                and last_cycle is not None
                and 0 <= current_cycle - last_cycle <= cooldown_cycles
            ):
                lane = "cooldown"
                priority = max(0, priority - 20)

        blocker = normalise_text(analysis.get("blocking_step_zh"))
        next_action = normalise_text(analysis.get("next_action_zh"))
        current_target = normalise_text(override.get("current_target_zh") or next_action)
        if latest:
            blocker = normalise_text(latest.get("blocker_zh")) or blocker
            next_action = normalise_text(latest.get("next_action_zh")) or next_action
            current_target = next_action or current_target

        evidence_paths = [
            f"artifacts/erdos_630_initial_analysis/results/{problem_id}.json",
        ]
        if problem_id in legacy_ids:
            evidence_paths.append(legacy["last_evidence_path"])
        evidence_paths.extend(compact_evidence_paths(nonopen_audit))
        evidence_paths.extend(compact_evidence_paths(conflict_audit))
        if latest:
            evidence_paths.extend(latest.get("evidence_paths", []))
        evidence_paths = list(dict.fromkeys(path for path in evidence_paths if path))

        followup: dict[str, Any] = {}
        if nonopen_audit:
            followup["nonopen_closure_verdict"] = nonopen_audit.get("closure_verdict")
            followup["nonopen_summary_zh"] = normalise_text(
                nonopen_audit.get("final_assessment_zh")
                or nonopen_audit.get("summary_zh")
                or nonopen_audit.get("conclusion_zh")
            )
        if conflict_audit:
            followup["open_conflict_verdict"] = conflict_audit.get("audit_verdict")
            followup["open_conflict_summary_zh"] = normalise_text(
                conflict_audit.get("final_assessment_zh")
                or conflict_audit.get("summary_zh")
                or conflict_audit.get("conclusion_zh")
            )

        rows.append(
            {
                "problem_id": problem_id,
                "title": cohort_row.get("title", f"Erdős Problem #{problem_id}"),
                "official_url": cohort_row.get(
                    "official_url", f"https://www.erdosproblems.com/{problem_id}"
                ),
                "domain": cohort_row.get("domain", "unknown"),
                "tags": cohort_row.get("tags", []),
                "prize": cohort_row.get("prize", ""),
                "status_snapshot": {
                    "state": cohort_row.get("current_status", "missing"),
                    "last_update": cohort_row.get("current_status_last_update", ""),
                    "formalized": cohort_row.get("current_formalized", "unknown"),
                    "snapshot_generated_at": cohort_generated_at,
                    "requires_refresh_before_attack": True,
                },
                "statement_type": kind,
                "statement_summary_zh": normalise_text(analysis.get("statement_summary_zh")),
                "initial_assessment": {
                    "verdict": analysis.get("verdict"),
                    "proof_attempt_status": analysis.get("proof_attempt_status"),
                    "feasibility_score": analysis.get("feasibility_score"),
                    "confidence": analysis.get("confidence"),
                    "status_note_zh": normalise_text(analysis.get("status_note_zh")),
                },
                "followup_audit": followup,
                "portfolio": {
                    "lane": lane,
                    "lifecycle_state": LANE_LIFECYCLE[lane],
                    "closure_distance": distance,
                    "closure_proximity_score": proximity,
                    "priority_score": priority,
                    "selection_reason_zh": normalise_text(
                        override.get("selection_reason_zh")
                    ),
                    "current_target_zh": current_target,
                    "blocking_step_zh": blocker,
                    "next_action_zh": next_action,
                    "attempt_count": event_state["attempt_count"],
                    "registered_agent_hours": event_state["registered_agent_hours"],
                    "no_progress_streak": event_state["no_progress_streak"],
                    "legacy_deep_campaign": problem_id in legacy_ids,
                    "legacy_rounds_through": (
                        int(legacy["last_round"]) if problem_id in legacy_ids else None
                    ),
                    "q2_candidate_recorded": event_state["q2_candidate"],
                    "last_event_id": latest.get("event_id") if latest else None,
                    "last_event_at": latest.get("occurred_at") if latest else None,
                    "last_event_cycle_id": latest.get("cycle_id") if latest else None,
                    "last_event_phase": latest.get("phase") if latest else None,
                    "last_event_outcome": latest.get("outcome") if latest else None,
                    "last_event_summary_zh": (
                        normalise_text(latest.get("summary_zh")) if latest else ""
                    ),
                    "evidence_paths": evidence_paths,
                },
            }
        )
    return rows


def stratified_select(
    rows: list[dict[str, Any]],
    *,
    slots: int,
    eligible_lanes: set[str],
    excluded_ids: set[str],
) -> list[str]:
    candidates = [
        row
        for row in rows
        if row["portfolio"]["lane"] in eligible_lanes
        and row["problem_id"] not in excluded_ids
    ]
    by_domain: dict[str, deque[dict[str, Any]]] = {}
    for domain, domain_rows in _group_by(candidates, key=lambda row: row["domain"]).items():
        by_domain[domain] = deque(
            sorted(
                domain_rows,
                key=lambda row: (
                    int(row["portfolio"]["attempt_count"]),
                    int(row["portfolio"]["no_progress_streak"]),
                    -int(row["portfolio"]["priority_score"]),
                    int(row["problem_id"]),
                ),
            )
        )
    selected: list[str] = []
    domains = sorted(
        by_domain,
        key=lambda domain: (
            by_domain[domain][0]["portfolio"]["attempt_count"],
            by_domain[domain][0]["portfolio"]["no_progress_streak"],
            -by_domain[domain][0]["portfolio"]["priority_score"],
            domain,
        ),
    )
    while domains and len(selected) < slots:
        next_domains: list[str] = []
        for domain in domains:
            queue = by_domain[domain]
            if queue and len(selected) < slots:
                selected.append(queue.popleft()["problem_id"])
            if queue:
                next_domains.append(domain)
        domains = next_domains
    return selected


def _group_by(items: Iterable[Any], key: Any) -> dict[Any, list[Any]]:
    grouped: dict[Any, list[Any]] = defaultdict(list)
    for item in items:
        grouped[key(item)].append(item)
    return grouped


def build_queue(
    *,
    policy: dict[str, Any],
    rows: list[dict[str, Any]],
    cycle_id: str,
) -> dict[str, list[dict[str, Any]]]:
    by_id = {row["problem_id"]: row for row in rows}
    forced = policy.get("forced_cycle_queues", {}).get(cycle_id, {})
    resource = policy["resource_policy"]
    rotation = policy["rotation_policy"]
    queue_ids: dict[str, list[str]] = {}

    if forced:
        for queue_name in QUEUE_BUDGET_KEYS:
            queue_ids[queue_name] = list(map(str, forced.get(queue_name, [])))
    else:
        closure = [
            row["problem_id"]
            for row in sorted(
                (row for row in rows if row["portfolio"]["lane"] == "closure_core"),
                key=lambda row: -row["portfolio"]["priority_score"],
            )
        ][: int(rotation["closure_core_slots_per_cycle"])]
        excluded = set(closure)
        intake = stratified_select(
            rows,
            slots=int(rotation["intake_slots_per_cycle"]),
            eligible_lanes={"discovery_high", "discovery_standard"},
            excluded_ids=excluded,
        )
        excluded.update(intake)
        audits = [
            row["problem_id"]
            for row in sorted(
                (row for row in rows if row["portfolio"]["lane"] == "resolution_audit"),
                key=lambda row: -row["portfolio"]["priority_score"],
            )
            if row["problem_id"] not in excluded
        ][: int(rotation["resolution_audit_slots_per_cycle"])]
        queue_ids = {
            "closure_core": closure,
            "intake": intake,
            "resolution_audit": audits,
            "paper_conversion": [],
            "status_refresh": [],
        }

    all_ids = {row["problem_id"] for row in rows}
    seen_research: set[str] = set()
    for queue_name, problem_ids in queue_ids.items():
        missing = set(problem_ids) - all_ids
        if missing:
            raise RuntimeError(f"Queue {queue_name} contains unknown ids: {sorted(missing)}")
        if queue_name in {"closure_core", "intake"}:
            overlap = seen_research & set(problem_ids)
            if overlap:
                raise RuntimeError(f"Active research queue overlap: {sorted(overlap)}")
            seen_research.update(problem_ids)

    queue: dict[str, list[dict[str, Any]]] = {}
    for queue_name, problem_ids in queue_ids.items():
        budget_key = QUEUE_BUDGET_KEYS[queue_name]
        queue[queue_name] = []
        for problem_id in problem_ids:
            row = by_id[problem_id]
            portfolio = row["portfolio"]
            completed_in_cycle = (
                portfolio["last_event_cycle_id"] == cycle_id
                and portfolio["last_event_phase"] in QUEUE_COMPLETION_PHASES[queue_name]
            )
            queue[queue_name].append(
                {
                    "problem_id": problem_id,
                    "domain": row["domain"],
                    "lane": portfolio["lane"],
                    "priority_score": portfolio["priority_score"],
                    "closure_distance": portfolio["closure_distance"],
                    "budget_seconds": int(resource[budget_key]) if budget_key else None,
                    "current_target_zh": portfolio["current_target_zh"],
                    "mandatory_status_refresh": True,
                    "cycle_progress": "completed" if completed_in_cycle else "pending",
                    "latest_outcome": (
                        portfolio["last_event_outcome"] if completed_in_cycle else None
                    ),
                    "attempt_count": portfolio["attempt_count"],
                }
            )
    return queue


def build_cycle_history(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = _group_by(events, key=lambda event: str(event["cycle_id"]))
    history: list[dict[str, Any]] = []
    for cycle_id in sorted(
        grouped,
        key=lambda value: (cycle_number(value) is None, cycle_number(value) or 0, value),
    ):
        cycle_events = grouped[cycle_id]
        history.append(
            {
                "cycle_id": cycle_id,
                "event_count": len(cycle_events),
                "registered_agent_hours": round(
                    sum(float(event.get("agent_hours", 0)) for event in cycle_events),
                    6,
                ),
                "problem_count": len(
                    {
                        str(event["problem_id"])
                        for event in cycle_events
                        if event.get("problem_id") is not None
                    }
                ),
                "phase_counts": dict(
                    sorted(Counter(str(event["phase"]) for event in cycle_events).items())
                ),
                "outcome_counts": dict(
                    sorted(Counter(str(event["outcome"]) for event in cycle_events).items())
                ),
                "original_closures": sorted(
                    {
                        str(event["problem_id"])
                        for event in cycle_events
                        if event.get("problem_id") is not None
                        and event.get("original_problem_closed")
                    },
                    key=int,
                ),
                "q2_candidates": sorted(
                    {
                        str(event["problem_id"])
                        for event in cycle_events
                        if event.get("problem_id") is not None and event.get("q2_candidate")
                    },
                    key=int,
                ),
            }
        )
    return history


def build_statistics(rows: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "problem_count": len(rows),
        "status_counts": dict(sorted(Counter(
            row["status_snapshot"]["state"] for row in rows
        ).items())),
        "lane_counts": dict(sorted(Counter(
            row["portfolio"]["lane"] for row in rows
        ).items())),
        "lifecycle_counts": dict(sorted(Counter(
            row["portfolio"]["lifecycle_state"] for row in rows
        ).items())),
        "domain_counts": dict(sorted(Counter(row["domain"] for row in rows).items())),
        "statement_type_counts": dict(sorted(Counter(
            row["statement_type"] for row in rows
        ).items())),
        "closure_distance_counts": dict(sorted(Counter(
            str(row["portfolio"]["closure_distance"]) for row in rows
        ).items())),
        "event_count": len(events),
        "registered_agent_hours": round(sum(
            float(event.get("agent_hours", 0)) for event in events
        ), 6),
        "problems_with_events": len({
            str(event["problem_id"]) for event in events if event.get("problem_id") is not None
        }),
    }


def table_text(value: Any, limit: int | None = None) -> str:
    text = normalise_text(value).replace("|", r"\|")
    if limit is not None and len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def render_plan(
    *,
    ledger: dict[str, Any],
    policy: dict[str, Any],
) -> str:
    stats = ledger["statistics"]
    effort = ledger["effort_accounting"]
    queue = ledger["current_queue"]
    rows = ledger["problems"]
    lines = [
        "# Erdős 630题轮换攻关总计划与总台账",
        "",
        f"> 台账版本：`{ledger['policy_id']}`；当前周期：`{ledger['cycle_id']}`；"
        f"生成时间：`{ledger['generated_at']}`。",
        "",
        "## 总目标与口径",
        "",
        (
            "本计划覆盖冻结 cohort 的630题。当前快照中550题为 `open`；其余条目进入"
            "闭合证据维护、状态冲突核验或有限判定路线。开放题的主目标始终是精确原命题"
            "的证明或证否；论文级阶段结果、已有解声明核验和形式化工作分别记账，不与原题"
            "闭合混计。"
        ),
        "",
        policy["cohort"]["status_snapshot_warning_zh"],
        "",
        "初筛的 `feasibility_score` 只表示下一步可检验性。调度另设0至5级"
        "`closure_distance`：0为已闭合，1为一条明确闭合引理/证据核验，2为一个有限结构"
        "缺档，3为存在可命名桥梁，4为需要新的全局机制，5为路线被阻断或题面尚不稳定。",
        "",
        "## 轮换制度",
        "",
        "每个题目的生命周期为：状态刷新 → 60至90分钟准入 → 最多4小时深攻 → "
        "独立QA → 晋级、论文转化、冷却或闭合。连续两个深攻周期未减少闭合距离的题进入"
        f"{policy['rotation_policy']['cooldown_cycles_after_two_stagnant_deep_rounds']}个周期冷却；"
        "只改善常数、扩大有限验证或增加条件定理不重置停滞计数。",
        "",
        "晋级深攻必须同时满足：",
        "",
    ]
    lines.extend(f"- {gate}" for gate in policy["promotion_gates"])
    lines.extend(
        [
            "",
            "轮换采用分层轮询而非单一总分排序：不同领域轮流获得准入槽；历史深挖题受到"
            "饱和惩罚；已有解声明进入 `resolution_audit`，不得占用原创证明槽。",
            "",
            "## 规模与资源",
            "",
            f"- 同时研究槽上限：{policy['resource_policy']['max_simultaneous_research_slots']}；"
            f"建议CPU占用不超过WSL资源的"
            f"{int(100 * policy['resource_policy']['recommended_cpu_fraction_ceiling'])}%。",
            f"- 准入预算：每题{policy['resource_policy']['intake_budget_seconds_per_problem'] // 60}分钟；"
            f"深攻预算：每题{policy['resource_policy']['deep_attack_budget_seconds_per_problem'] // 3600}小时；"
            f"独立QA预算：每项{policy['resource_policy']['independent_qa_budget_seconds_per_result'] // 60}分钟。",
            f"- 全池覆盖规划：{policy['rotation_policy']['coverage_note_zh']}",
            "",
            "## 当前总体统计",
            "",
            f"- 总题数：{stats['problem_count']}；状态分布："
            + "、".join(f"`{key}`={value}" for key, value in stats["status_counts"].items())
            + "。",
            "- 任务通道："
            + "、".join(f"`{key}`={value}" for key, value in stats["lane_counts"].items())
            + "。",
            "- 闭合距离："
            + "、".join(f"`{key}`={value}" for key, value in stats["closure_distance_counts"].items())
            + "。",
            f"- 当前追加事件流：{stats['event_count']}条、覆盖"
            f"{stats['problems_with_events']}题、登记{effort['event_agent_hours']:.2f} agent-hours。",
            f"- 连同旧轮次，可直接核算的总投入下界为"
            f"{effort['combined_known_agent_hours_lower_bound']:.2f} agent-hours；"
            f"{effort['legacy_note_zh']}",
            "",
            f"## 当前周期 {ledger['cycle_id']}",
            "",
        ]
    )

    queue_titles = {
        "closure_core": "原题闭合核心",
        "intake": "新题准入",
        "resolution_audit": "已有解声明核验",
        "paper_conversion": "论文转化（独立预算）",
        "status_refresh": "优先状态刷新",
    }
    for queue_name in (
        "closure_core",
        "intake",
        "resolution_audit",
        "paper_conversion",
        "status_refresh",
    ):
        lines.extend(
            [
                f"### {queue_titles[queue_name]}",
                "",
                "| # | 领域 | 闭合距离 | 预算 | 周期进度 | 当前精确目标 |",
                "|---:|---|---:|---:|---|---|",
            ]
        )
        for item in queue.get(queue_name, []):
            budget = (
                "独立计账"
                if item["budget_seconds"] is None
                else f"{item['budget_seconds'] / 3600:g}h"
            )
            lines.append(
                f"| [{item['problem_id']}](https://www.erdosproblems.com/{item['problem_id']}) "
                f"| {table_text(item['domain'])} | {item['closure_distance']} | {budget} "
                f"| {item['cycle_progress']} "
                f"| {table_text(item['current_target_zh'])} |"
            )
        if not queue.get(queue_name):
            lines.append("| — | — | — | — | — | 本周期无任务 |")
        lines.append("")

    lines.extend(
        [
            "## 操作与证据规则",
            "",
            "1. 进入任何研究阶段前刷新官网状态、原论文和最新公开讨论。",
            "2. 每次工作结束向 `events.jsonl` 追加事件；不得覆盖历史结论。",
            "3. 任何闭合候选必须另做题面量词审计、来源审计、独立数学QA和可复现实验/形式检查。",
            "4. 论文级结果进入独立论文通道；它不自动降低原题闭合距离。",
            "5. 下一轮由事件后的闭合距离、停滞计数、领域轮询和冷却期共同生成。",
            "",
            "重建与检查：",
            "",
            "```bash",
            "python3 scripts/manage_erdos_rotation.py build",
            "python3 scripts/manage_erdos_rotation.py validate",
            "```",
            "",
            "## 630题紧凑总台账",
            "",
            "机器可读的完整阻塞点、下一动作、证据路径和事件统计见"
            "`artifacts/erdos_master_rotation/master_ledger.json`。下表用于快速巡检。",
            "",
            "| # | 快照状态 | 领域 | 初筛 | 可检验分 | 题型 | 通道 | 距离 | 历史轮至 | 新事件尝试 | 停滞 |",
            "|---:|---|---|---|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        portfolio = row["portfolio"]
        initial = row["initial_assessment"]
        lines.append(
            f"| [{row['problem_id']}]({row['official_url']}) "
            f"| {table_text(row['status_snapshot']['state'])} "
            f"| {table_text(row['domain'])} "
            f"| {table_text(initial['verdict'])} "
            f"| {initial['feasibility_score']} "
            f"| {table_text(row['statement_type'])} "
            f"| {table_text(portfolio['lane'])} "
            f"| {portfolio['closure_distance']} "
            f"| {portfolio['legacy_rounds_through'] or '—'} "
            f"| {portfolio['attempt_count']} "
            f"| {portfolio['no_progress_streak']} |"
        )
    lines.append("")
    return "\n".join(lines)


def validate_ledger(
    ledger: dict[str, Any],
    *,
    policy: dict[str, Any],
    events: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    expected = int(policy["cohort"]["expected_problem_count"])
    rows = ledger.get("problems", [])
    ids = [str(row.get("problem_id")) for row in rows]
    if len(rows) != expected:
        errors.append(f"problem_count={len(rows)} expected={expected}")
    if len(set(ids)) != len(ids):
        duplicates = sorted(
            problem_id for problem_id, count in Counter(ids).items() if count > 1
        )
        errors.append(f"duplicate_problem_ids={duplicates}")
    if ids != sorted(ids, key=int):
        errors.append("problem rows are not numerically sorted")
    for row in rows:
        portfolio = row.get("portfolio", {})
        lane = portfolio.get("lane")
        if lane not in LANE_LIFECYCLE:
            errors.append(f"#{row.get('problem_id')}: unknown lane {lane}")
        distance = portfolio.get("closure_distance")
        if not isinstance(distance, int) or not 0 <= distance <= 5:
            errors.append(f"#{row.get('problem_id')}: invalid closure_distance {distance}")
        priority = portfolio.get("priority_score")
        if not isinstance(priority, int) or not 0 <= priority <= 100:
            errors.append(f"#{row.get('problem_id')}: invalid priority_score {priority}")
        if not portfolio.get("current_target_zh"):
            errors.append(f"#{row.get('problem_id')}: empty current_target_zh")
    queue = ledger.get("current_queue", {})
    known = set(ids)
    active_seen: set[str] = set()
    for queue_name, items in queue.items():
        for item in items:
            problem_id = str(item.get("problem_id"))
            if problem_id not in known:
                errors.append(f"queue {queue_name}: unknown #{problem_id}")
            if queue_name in {"closure_core", "intake"}:
                if problem_id in active_seen:
                    errors.append(f"duplicate active research #{problem_id}")
                active_seen.add(problem_id)
            if item.get("cycle_progress") not in {"pending", "completed"}:
                errors.append(
                    f"queue {queue_name}: invalid cycle_progress "
                    f"{item.get('cycle_progress')} for #{problem_id}"
                )
    event_ids = [str(event["event_id"]) for event in events]
    if len(event_ids) != len(set(event_ids)):
        errors.append("duplicate event ids")
    return errors


def materialise(
    *,
    policy_path: Path,
    events_path: Path,
    cohort_root: Path,
    output_dir: Path,
    plan_path: Path,
    cycle_id: str | None,
) -> dict[str, Any]:
    policy = read_json(policy_path, default={})
    if not policy:
        raise RuntimeError(f"Cannot read policy: {policy_path}")
    events = load_events(events_path)
    cycle = cycle_id or policy["rotation_policy"]["current_cycle_id"]
    rows = build_problem_rows(
        policy=policy,
        cohort_root=cohort_root,
        events=events,
        cycle_id=cycle,
    )
    queue = build_queue(policy=policy, rows=rows, cycle_id=cycle)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cohort_payload = read_json(cohort_root / "cohort.json", default={})
    ledger = {
        "schema_version": "amra.erdos_master_ledger.v1",
        "generated_at": now,
        "policy_id": policy["policy_id"],
        "cycle_id": cycle,
        "source_snapshot": {
            "cohort_generated_at": cohort_payload.get("generated_at"),
            "metadata_source": cohort_payload.get("metadata_source"),
            "metadata_commit": cohort_payload.get("metadata_commit"),
            "statement_and_prior_source": cohort_payload.get("statement_and_prior_source"),
            "statement_and_prior_commit": cohort_payload.get("statement_and_prior_commit"),
            "policy_path": str(policy_path.relative_to(REPO_ROOT)),
            "events_path": str(events_path.relative_to(REPO_ROOT)),
        },
        "statistics": build_statistics(rows, events),
        "effort_accounting": {
            "event_agent_hours": round(
                sum(float(event.get("agent_hours", 0)) for event in events),
                6,
            ),
            "legacy_campaign_agent_hours_lower_bound": float(
                policy["legacy_deep_campaign"]["registered_agent_hours_lower_bound"]
            ),
            "combined_known_agent_hours_lower_bound": round(
                sum(float(event.get("agent_hours", 0)) for event in events)
                + float(
                    policy["legacy_deep_campaign"]["registered_agent_hours_lower_bound"]
                ),
                2,
            ),
            "legacy_note_zh": policy["legacy_deep_campaign"][
                "registered_hours_note_zh"
            ],
        },
        "cycle_history": build_cycle_history(events),
        "current_queue": queue,
        "problems": rows,
    }
    errors = validate_ledger(ledger, policy=policy, events=events)
    if errors:
        raise RuntimeError("Ledger validation failed:\n- " + "\n- ".join(errors))

    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output_dir / "master_ledger.json", ledger)
    atomic_write_json(
        output_dir / "rotation_queue.json",
        {
            "schema_version": "amra.erdos_rotation_queue.v1",
            "generated_at": now,
            "policy_id": policy["policy_id"],
            "cycle_id": cycle,
            "queues": queue,
        },
    )
    atomic_write_json(
        output_dir / "validation_report.json",
        {
            "schema_version": "amra.erdos_master_validation.v1",
            "validated_at": now,
            "valid": True,
            "errors": [],
            "problem_count": len(rows),
            "unique_problem_count": len({row["problem_id"] for row in rows}),
            "event_count": len(events),
            "queue_counts": {name: len(items) for name, items in queue.items()},
        },
    )
    atomic_write_text(plan_path, render_plan(ledger=ledger, policy=policy))
    return ledger


def record_event(args: argparse.Namespace) -> None:
    policy = read_json(args.policy, default={})
    cohort = read_json(args.cohort_root / "cohort.json", default={})
    known_ids = {str(row["problem_id"]) for row in cohort.get("problems", [])}
    if args.problem is not None and str(args.problem) not in known_ids:
        raise RuntimeError(f"Unknown cohort problem #{args.problem}")
    if args.problem is None and args.phase != "portfolio":
        raise RuntimeError("--problem is required unless --phase portfolio")

    occurred_at = args.occurred_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    event_id = args.event_id or (
        occurred_at.replace(":", "").replace("-", "").replace("+", "_")
        + f"-{args.problem or 'portfolio'}-{args.phase}"
    )
    event = {
        "event_id": event_id,
        "occurred_at": occurred_at,
        "cycle_id": args.cycle or policy["rotation_policy"]["current_cycle_id"],
        "problem_id": str(args.problem) if args.problem is not None else None,
        "phase": args.phase,
        "outcome": args.outcome,
        "agent_hours": float(args.hours),
        "original_problem_closed": bool(args.closed),
        "q2_candidate": bool(args.q2),
        "closure_distance_before": args.distance_before,
        "closure_distance_after": args.distance_after,
        "summary_zh": args.summary,
        "blocker_zh": args.blocker,
        "next_action_zh": args.next_action,
        "evidence_paths": list(args.evidence or []),
    }
    existing = load_events(args.events)
    if event_id in {row["event_id"] for row in existing}:
        raise RuntimeError(f"Duplicate event_id: {event_id}")
    args.events.parent.mkdir(parents=True, exist_ok=True)
    with args.events.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    result.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    result.add_argument("--cohort-root", type=Path, default=DEFAULT_COHORT_ROOT)
    result.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    result.add_argument("--plan-path", type=Path, default=DEFAULT_PLAN_PATH)
    subparsers = result.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="materialise ledger, queue, and plan")
    build_parser.add_argument("--cycle", default=None)

    validate_parser = subparsers.add_parser("validate", help="validate materialised ledger")
    validate_parser.add_argument("--cycle", default=None)

    record_parser = subparsers.add_parser("record", help="append one event and rebuild")
    record_parser.add_argument("--problem")
    record_parser.add_argument("--cycle")
    record_parser.add_argument("--phase", required=True, choices=[
        "portfolio",
        "status_refresh",
        "intake",
        "deep_attack",
        "independent_qa",
        "resolution_audit",
        "paper_conversion",
        "formalization",
        "decision",
    ])
    record_parser.add_argument("--outcome", required=True)
    record_parser.add_argument("--hours", type=float, default=0.0)
    record_parser.add_argument("--closed", action="store_true")
    record_parser.add_argument("--q2", action="store_true")
    record_parser.add_argument("--distance-before", type=int, choices=range(0, 6))
    record_parser.add_argument("--distance-after", type=int, choices=range(0, 6))
    record_parser.add_argument("--summary", required=True)
    record_parser.add_argument("--blocker", default="")
    record_parser.add_argument("--next-action", default="")
    record_parser.add_argument("--evidence", action="append", default=[])
    record_parser.add_argument("--event-id")
    record_parser.add_argument("--occurred-at")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "record":
        record_event(args)
        materialise(
            policy_path=args.policy,
            events_path=args.events,
            cohort_root=args.cohort_root,
            output_dir=args.output_dir,
            plan_path=args.plan_path,
            cycle_id=args.cycle,
        )
        print(f"Recorded event and rebuilt {args.output_dir / 'master_ledger.json'}")
        return 0

    ledger = materialise(
        policy_path=args.policy,
        events_path=args.events,
        cohort_root=args.cohort_root,
        output_dir=args.output_dir,
        plan_path=args.plan_path,
        cycle_id=args.cycle,
    )
    if args.command == "validate":
        policy = read_json(args.policy, default={})
        events = load_events(args.events)
        errors = validate_ledger(ledger, policy=policy, events=events)
        if errors:
            print("\n".join(errors))
            return 1
        print(
            f"PASS: {len(ledger['problems'])} unique problems; "
            f"cycle={ledger['cycle_id']}; events={len(events)}"
        )
    else:
        print(
            f"Built {len(ledger['problems'])}-problem ledger for {ledger['cycle_id']} "
            f"at {args.output_dir}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
