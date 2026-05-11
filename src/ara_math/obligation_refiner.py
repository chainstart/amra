from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ara_math.coordinator import (
    add_workstream,
    comath_paths,
    load_project_state,
    render_project_dashboard,
    save_project_state,
)
from ara_math.workspace import append_jsonl, slugify, write_json, write_text
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord, WorkstreamStatus, utc_now_iso


_INACTIVE_VALUES = {"", "-", "none", "no", "n/a", "na", "empty", "no blockers", "no blocker"}
_GENERIC_ACTION_PATTERNS = (
    "route through review gate",
    "review gate before promotion",
    "before promotion",
    "promote after review",
)


@dataclass(frozen=True, slots=True)
class ObligationCandidate:
    obligation_id: str
    title: str
    goal: str
    kind: WorkstreamKind
    role_id: str
    source_action: str
    source_blockers: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    priority: int
    tags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "title": self.title,
            "goal": self.goal,
            "kind": self.kind.value,
            "role_id": self.role_id,
            "source_action": self.source_action,
            "source_blockers": list(self.source_blockers),
            "acceptance_criteria": list(self.acceptance_criteria),
            "priority": self.priority,
            "tags": list(self.tags),
        }


def _clean_item(value: str) -> str:
    text = re.sub(r"\s+", " ", value.strip())
    text = text.strip(" -\t\r\n")
    return text


def _is_inactive(value: str) -> bool:
    return _clean_item(value).lower() in _INACTIVE_VALUES


def split_action_items(text: str) -> list[str]:
    if _is_inactive(text):
        return []
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\n\s*(?:[-*]|\d+[.)])\s+", "\n", normalized)
    raw_items = re.split(r"\n+|;\s*", normalized)
    items: list[str] = []
    seen: set[str] = set()
    for raw_item in raw_items:
        item = _clean_item(raw_item)
        if not item or _is_inactive(item):
            continue
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(item)
    return items


def normalize_blocker_key(text: str) -> str:
    item = _clean_item(text)
    if not item:
        return ""
    prefix = item.split(":", 1)[0].strip()
    if 2 <= len(prefix) <= 80 and re.search(r"[A-Za-z]", prefix):
        return prefix
    return slugify(item)[:80]


def _is_actionable(action: str, blockers: list[str]) -> bool:
    lowered = action.lower()
    if any(pattern in lowered for pattern in _GENERIC_ACTION_PATTERNS):
        return bool(blockers) and any(token in lowered for token in ("prove", "source", "lean", "compute", "construct"))
    if blockers:
        return True
    return bool(
        re.search(
            r"\b(write|construct|prove|derive|formalize|implement|search|audit|verify|compute|certify|repair|"
            r"majorant|bellman|candidate|lemma|theorem|lean|source|paper|certificate|bound|concavity|gluing)\b",
            lowered,
        )
    )


def _kind_for_action(action: str, blockers: list[str]) -> WorkstreamKind:
    action_lowered = action.lower()
    all_lowered = " ".join([action, *blockers]).lower()
    if re.search(r"\b(lean|lake build|theorem prover|formaliz|declaration|placeholder|sorry)\b", action_lowered):
        return WorkstreamKind.LEAN
    if re.search(r"\b(source|paper|literature|arxiv|doi|theorem statement|citation|reference|assumption audit)\b", action_lowered):
        return WorkstreamKind.SOURCE
    if re.search(r"\b(compute|computation|numerical|symbolic|certificate|script|sage|python|verify data)\b", action_lowered):
        return WorkstreamKind.COMPUTE
    if re.search(r"\b(prove|construct|derive|candidate|lemma|majorant|bellman|bound|concavity|gluing)\b", action_lowered):
        return WorkstreamKind.PROOF
    if re.search(r"\b(lean|lake build|theorem prover|formaliz|declaration|placeholder|sorry)\b", all_lowered):
        return WorkstreamKind.LEAN
    if re.search(r"\b(source|paper|literature|arxiv|doi|theorem statement|citation|reference|assumption audit)\b", all_lowered):
        return WorkstreamKind.SOURCE
    if re.search(r"\b(compute|computation|numerical|symbolic|certificate|script|sage|python|verify data)\b", all_lowered):
        return WorkstreamKind.COMPUTE
    if re.search(r"\b(review|audit proof|check validity)\b", all_lowered) and not re.search(
        r"\b(prove|construct|derive|candidate|lemma|majorant|bellman)\b", all_lowered
    ):
        return WorkstreamKind.REVIEW
    return WorkstreamKind.PROOF


def _role_for_kind(kind: WorkstreamKind) -> str:
    return {
        WorkstreamKind.PROOF: "theory_builder",
        WorkstreamKind.LEAN: "lean_formalizer",
        WorkstreamKind.SOURCE: "source_auditor",
        WorkstreamKind.COMPUTE: "computational_explorer",
        WorkstreamKind.REVIEW: "proof_reviewer",
    }[kind]


def _tags_for_action(action: str, kind: WorkstreamKind) -> tuple[str, ...]:
    lowered = action.lower()
    tags = {kind.value, "generated-obligation"}
    for token in (
        "bellman",
        "bmo",
        "frontier",
        "piecewise",
        "majorant",
        "concavity",
        "gluing",
        "boundary",
        "source",
        "lean",
        "certificate",
    ):
        if token in lowered:
            tags.add(token)
    return tuple(sorted(tags))


def _priority_for_action(action: str, blockers: list[str], kind: WorkstreamKind) -> int:
    action_lowered = action.lower()
    blocker_lowered = " ".join(blockers).lower()
    priority = 20
    if blockers:
        priority = 10
    if re.search(r"\b(piecewise|majorant|bellman candidate)\b", action_lowered):
        priority = min(priority, 3)
    elif re.search(r"\b(prove|construct|derive|candidate|lemma|bound|concavity|gluing)\b", action_lowered) and re.search(
        r"\b(critical|global|top blocker|blocking|missing|cannot approve|unsound)\b",
        blocker_lowered,
    ):
        priority = min(priority, 5)
    elif re.search(r"\b(critical|global|top blocker|blocking|missing|cannot approve|unsound)\b", blocker_lowered):
        priority = min(priority, 8)
    if kind == WorkstreamKind.LEAN:
        priority = max(priority, 12)
    if kind == WorkstreamKind.REVIEW:
        priority = max(priority, 30)
    return priority


def _title_for_action(action: str, kind: WorkstreamKind) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", action)
    text = _clean_item(text).rstrip(".")
    if len(text) > 96:
        text = text[:93].rstrip() + "..."
    prefix = {
        WorkstreamKind.PROOF: "Proof obligation",
        WorkstreamKind.LEAN: "Lean obligation",
        WorkstreamKind.SOURCE: "Source obligation",
        WorkstreamKind.COMPUTE: "Computation obligation",
        WorkstreamKind.REVIEW: "Review obligation",
    }[kind]
    return f"{prefix}: {text}"


def _acceptance_criteria(action: str, blockers: list[str], kind: WorkstreamKind) -> tuple[str, ...]:
    criteria = [
        "Produce an artifact that directly addresses the source action rather than only restating the blocker.",
        "If the obligation cannot be closed, record a strictly narrower blocker with the failed route or missing lemma named.",
    ]
    for blocker in blockers[:5]:
        blocker_key = normalize_blocker_key(blocker)
        if blocker_key:
            criteria.append(f"Reviewer closes or strictly narrows blocker `{blocker_key}`.")
    if kind == WorkstreamKind.PROOF:
        criteria.append("Provide a certifiable proof step, candidate definition, or lemma chain that can be reviewed independently.")
    elif kind == WorkstreamKind.LEAN:
        criteria.append("Lean artifacts build successfully and do not assume the target obligation as a hypothesis.")
    elif kind == WorkstreamKind.SOURCE:
        criteria.append("Primary-source theorem statements, hypotheses, and unresolved assumption mismatches are recorded.")
    elif kind == WorkstreamKind.COMPUTE:
        criteria.append("A reproducible manifest or certificate verifies the requested computation and states its scope.")
    elif kind == WorkstreamKind.REVIEW:
        criteria.append("Review decision names every remaining open source, logic, Lean, or computation debt item.")
    return tuple(criteria)


def _candidate_id(action: str, kind: WorkstreamKind) -> str:
    code_tokens = re.findall(r"`([^`]{2,80})`", action)
    if code_tokens:
        stem = "-".join(slugify(token) for token in code_tokens[:2])
        action_slug = slugify(action)
        if action_slug and stem not in action_slug:
            stem = f"{stem}-{action_slug[:40]}"
    else:
        stem = slugify(action)
    return f"obligation-{kind.value}-{stem[:84]}".rstrip("-")


def candidates_from_specialist_output(
    parsed_output: dict[str, Any],
    *,
    source_role_id: str = "",
    source_run_id: str = "",
    source_workstream_id: str = "",
) -> list[ObligationCandidate]:
    fields = parsed_output.get("fields", {}) if isinstance(parsed_output.get("fields"), dict) else {}
    blockers = [_clean_item(str(item)) for item in parsed_output.get("blockers", []) if not _is_inactive(str(item))]
    action_texts: list[str] = []
    for field_name in ("next_actions", "next_action", "actions", "todo", "todos"):
        value = str(fields.get(field_name, "")).strip()
        if value:
            action_texts.extend(split_action_items(value))
    if not action_texts:
        action_texts = [f"Resolve blocker: {blocker}" for blocker in blockers]

    candidates: list[ObligationCandidate] = []
    seen_ids: set[str] = set()
    for action in action_texts:
        if not _is_actionable(action, blockers):
            continue
        kind = _kind_for_action(action, blockers)
        candidate = ObligationCandidate(
            obligation_id=_candidate_id(action, kind),
            title=_title_for_action(action, kind),
            goal=_goal_text(action, blockers, source_role_id, source_run_id, source_workstream_id),
            kind=kind,
            role_id=_role_for_kind(kind),
            source_action=action,
            source_blockers=tuple(blockers),
            acceptance_criteria=_acceptance_criteria(action, blockers, kind),
            priority=_priority_for_action(action, blockers, kind),
            tags=_tags_for_action(action, kind),
        )
        if candidate.obligation_id in seen_ids:
            continue
        seen_ids.add(candidate.obligation_id)
        candidates.append(candidate)
    return candidates


def _goal_text(
    action: str,
    blockers: list[str],
    source_role_id: str,
    source_run_id: str,
    source_workstream_id: str,
) -> str:
    lines = [
        "# Generated Proof Obligation",
        "",
        "## Source Action",
        "",
        action,
        "",
    ]
    if blockers:
        lines.extend(["## Source Blockers", "", *[f"- {blocker}" for blocker in blockers], ""])
    source_parts = []
    if source_role_id:
        source_parts.append(f"role `{source_role_id}`")
    if source_run_id:
        source_parts.append(f"run `{source_run_id}`")
    if source_workstream_id:
        source_parts.append(f"workstream `{source_workstream_id}`")
    if source_parts:
        lines.extend(["## Generated From", "", ", ".join(source_parts) + ".", ""])
    return "\n".join(lines).rstrip() + "\n"


def _merge_strings(existing: list[Any], additions: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value in [*existing, *additions]:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        merged.append(text)
    return merged


def _merge_generated_from(existing: list[Any], reference: dict[str, str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for item in [*existing, reference]:
        if not isinstance(item, dict):
            continue
        record = {
            "role_id": str(item.get("role_id", "")),
            "run_id": str(item.get("run_id", "")),
            "workstream_id": str(item.get("workstream_id", "")),
            "output_path": str(item.get("output_path", "")),
        }
        key = (record["role_id"], record["run_id"], record["workstream_id"], record["output_path"])
        if key in seen:
            continue
        seen.add(key)
        records.append(record)
    return records


def _metadata_priority(value: Any, fallback: int) -> int:
    try:
        return int(value or fallback)
    except (TypeError, ValueError):
        return fallback


def _write_obligation_files(project_dir: Path, workstream: WorkstreamRecord) -> None:
    paths = comath_paths(project_dir)
    workstream_dir = paths.workstream_dir(workstream.workstream_id)
    write_json(workstream_dir / "status.json", workstream.to_dict())
    write_text(workstream_dir / "goal.md", workstream.goal.rstrip() + "\n")
    criteria = [str(item) for item in workstream.metadata.get("acceptance_criteria", [])]
    if criteria:
        write_text(
            workstream_dir / "acceptance_criteria.md",
            "# Acceptance Criteria\n\n" + "\n".join(f"- {item}" for item in criteria) + "\n",
        )
    blocker_lines = [f"- {blocker}" for blocker in workstream.blockers] or ["- No blockers recorded."]
    write_text(workstream_dir / "blockers.md", "# Blockers\n\n" + "\n".join(blocker_lines) + "\n")


def materialize_obligations_from_specialist_run(
    project_dir: Path,
    *,
    parsed_output: dict[str, Any],
    source_role_id: str = "",
    source_run_id: str = "",
    source_workstream_id: str = "",
    output_path: str = "",
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    candidates = candidates_from_specialist_output(
        parsed_output,
        source_role_id=source_role_id,
        source_run_id=source_run_id,
        source_workstream_id=source_workstream_id,
    )
    if not candidates:
        return {"created": [], "updated": [], "candidates": []}

    created: list[str] = []
    updated: list[str] = []
    reference = {
        "role_id": source_role_id,
        "run_id": source_run_id,
        "workstream_id": source_workstream_id,
        "output_path": output_path,
    }
    paths = comath_paths(project_dir)

    for candidate in candidates:
        state = load_project_state(project_dir)
        existing = state.get_workstream(candidate.obligation_id)
        metadata = {
            "generated_by": "obligation_refiner",
            "generated_from": [reference],
            "source_action": candidate.source_action,
            "source_blockers": list(candidate.source_blockers),
            "acceptance_criteria": list(candidate.acceptance_criteria),
            "scheduler_priority": candidate.priority,
            "executor": "llm_specialist",
            "specialist_task": candidate.goal,
            "role_id": candidate.role_id,
            "obligation_kind": candidate.kind.value,
            "tags": list(candidate.tags),
        }
        if existing is None:
            workstream = WorkstreamRecord(
                workstream_id=candidate.obligation_id,
                kind=candidate.kind,
                goal=_goal_with_acceptance(candidate),
                owner=candidate.role_id,
                blockers=list(candidate.source_blockers),
                metadata=metadata,
            )
            add_workstream(project_dir, workstream)
            _write_obligation_files(project_dir, workstream)
            created.append(candidate.obligation_id)
        else:
            existing.kind = candidate.kind
            existing.goal = _goal_with_acceptance(candidate)
            existing.owner = candidate.role_id
            existing.blockers = _merge_strings(existing.blockers, list(candidate.source_blockers))
            existing.metadata["generated_by"] = "obligation_refiner"
            existing.metadata["generated_from"] = _merge_generated_from(
                list(existing.metadata.get("generated_from", [])),
                reference,
            )
            existing.metadata["source_action"] = candidate.source_action
            existing.metadata["source_blockers"] = _merge_strings(
                list(existing.metadata.get("source_blockers", [])),
                list(candidate.source_blockers),
            )
            existing.metadata["acceptance_criteria"] = _merge_strings(
                list(existing.metadata.get("acceptance_criteria", [])),
                list(candidate.acceptance_criteria),
            )
            existing.metadata["scheduler_priority"] = min(
                _metadata_priority(existing.metadata.get("scheduler_priority"), candidate.priority),
                candidate.priority,
            )
            existing.metadata["executor"] = "llm_specialist"
            existing.metadata["specialist_task"] = candidate.goal
            existing.metadata["role_id"] = candidate.role_id
            existing.metadata["obligation_kind"] = candidate.kind.value
            existing.metadata["tags"] = _merge_strings(list(existing.metadata.get("tags", [])), list(candidate.tags))
            if existing.status == WorkstreamStatus.NEEDS_REVIEW and candidate.source_blockers:
                existing.status = WorkstreamStatus.REVISION
            existing.updated_at = utc_now_iso()
            state.upsert_workstream(existing)
            save_project_state(project_dir, state)
            _write_obligation_files(project_dir, existing)
            updated.append(candidate.obligation_id)

        append_jsonl(
            paths.workstream_dir(candidate.obligation_id) / "messages.jsonl",
            {
                "ts": utc_now_iso(),
                "type": "obligation_refined",
                "source_role_id": source_role_id,
                "source_run_id": source_run_id,
                "source_workstream_id": source_workstream_id,
                "priority": candidate.priority,
            },
        )

    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "obligations_refined",
            "source_role_id": source_role_id,
            "source_run_id": source_run_id,
            "source_workstream_id": source_workstream_id,
            "created": created,
            "updated": updated,
        },
    )
    render_project_dashboard(project_dir)
    return {
        "created": created,
        "updated": updated,
        "candidates": [candidate.to_dict() for candidate in candidates],
    }


def _goal_with_acceptance(candidate: ObligationCandidate) -> str:
    lines = [candidate.goal.rstrip(), "", "## Acceptance Criteria", ""]
    lines.extend(f"- {item}" for item in candidate.acceptance_criteria)
    return "\n".join(lines).rstrip() + "\n"
