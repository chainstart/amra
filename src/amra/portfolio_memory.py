from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROBLEM_STATES = {
    "unseen",
    "scouted",
    "promising",
    "active_attack",
    "formalization_ready",
    "verified",
    "library_harvested",
    "parked",
    "frozen",
    "counterexample_suspected",
    "needs_source",
}
CLAIM_STATUSES = {
    "hypothesis",
    "sketch",
    "route_supported",
    "needs_review",
    "review_rejected",
    "lean_stubbed",
    "lean_partial",
    "lean_verified",
    "counterexample_suspected",
    "false",
    "obsolete",
}
ROUTE_STATUSES = {"new", "promising", "blocked", "failed", "superseded", "completed"}
FAILURE_MODES = {
    "counterexample_candidate",
    "lean_statement_mismatch",
    "missing_mathlib_api",
    "proof_gap",
    "combinatorial_case_explosion",
    "modeling_too_weak",
    "resource_timeout",
    "source_gap",
    "formalization_blocked",
}
FAILURE_CLASSES_BY_MODE = {
    "counterexample_candidate": "logical",
    "lean_statement_mismatch": "formalization",
    "missing_mathlib_api": "formalization",
    "proof_gap": "logical",
    "combinatorial_case_explosion": "resource",
    "modeling_too_weak": "modeling",
    "resource_timeout": "resource",
    "source_gap": "source",
    "formalization_blocked": "formalization",
}
CONSOLIDATION_SCHEMA_VERSION = "amra.memory_consolidation.v1"
FAILED_ROUTE_RETRIEVAL_SCHEMA_VERSION = "amra.failed_route_retrieval.v1"
VERIFIED_DECLARATIONS_SCHEMA_VERSION = "amra.verified_declarations.v1"

PRIVATE_ARTIFACT_NAMES = {"prompt.txt", "context_bundle.md"}
CONSOLIDATION_JSON_NAMES = {
    "claim_updates.json",
    "claims.json",
    "route_updates.json",
    "routes.json",
    "route_candidates.json",
    "proof_route_scaffold.json",
    "failed_route_updates.json",
    "failed_routes.json",
    "review.json",
    "review_report.json",
    "report.json",
    "state.json",
    "attempt_report.json",
    "after_audit.json",
    "before_audit.json",
    "initial_audit.json",
    "best_audit.json",
    "build_report.json",
    "after_build.json",
    "focus_contract.json",
    "proof_state.json",
    "verified_declarations.json",
}
CONSOLIDATION_TEXT_NAMES = {
    "proof_package.md",
    "formalizer_handoff.md",
    "proof_notes.md",
    "partial_lemmas.md",
    "verified_lean_declarations.md",
    "failed_routes.md",
    "blockers.md",
    "counterexample_report.md",
    "review.md",
    "review_notes.md",
    "summary.md",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def project_memory_dir(project_dir: Path) -> Path:
    return project_dir / "memory"


def state_history_path(project_dir: Path) -> Path:
    return project_dir / "state_history.jsonl"


def resume_pack_path(project_dir: Path) -> Path:
    return project_dir / "resume_pack.md"


def claim_ledger_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "claim_ledger.json"


def claim_history_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "claim_history.jsonl"


def route_ledger_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "route_ledger.json"


def route_history_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "route_history.jsonl"


def failed_routes_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "failed_routes.json"


def failed_route_history_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "failed_route_history.jsonl"


def evidence_index_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "evidence_index.json"


def consolidation_report_path(project_dir: Path) -> Path:
    return project_memory_dir(project_dir) / "consolidation_report.json"


def verified_declarations_path(project_dir: Path) -> Path:
    return project_dir / "verified_declarations.json"


def normalize_problem_state(state: str) -> str:
    normalized = str(state).strip()
    if normalized not in PROBLEM_STATES:
        raise ValueError(f"Unknown AMRA problem state: {state}")
    return normalized


def normalize_claim_status(status: str) -> str:
    normalized = str(status).strip()
    if normalized not in CLAIM_STATUSES:
        raise ValueError(f"Unknown AMRA claim status: {status}")
    return normalized


def normalize_route_status(status: str) -> str:
    normalized = str(status).strip()
    if normalized not in ROUTE_STATUSES:
        raise ValueError(f"Unknown AMRA route status: {status}")
    return normalized


def normalize_failure_mode(mode: str) -> str:
    normalized = str(mode).strip()
    if normalized not in FAILURE_MODES:
        raise ValueError(f"Unknown AMRA failed route mode: {mode}")
    return normalized


def load_claim_ledger(project_dir: Path) -> dict[str, Any]:
    return read_json(
        claim_ledger_path(project_dir),
        {"schema_version": "amra.claim_ledger.v1", "updated_at": None, "claims": []},
    )


def load_route_ledger(project_dir: Path) -> dict[str, Any]:
    return read_json(
        route_ledger_path(project_dir),
        {"schema_version": "amra.route_ledger.v1", "updated_at": None, "routes": []},
    )


def load_failed_routes(project_dir: Path) -> dict[str, Any]:
    return read_json(
        failed_routes_path(project_dir),
        {"schema_version": "amra.failed_routes.v1", "updated_at": None, "failed_routes": []},
    )


def load_evidence_index(project_dir: Path) -> dict[str, Any]:
    return read_json(
        evidence_index_path(project_dir),
        {"schema_version": "amra.evidence_index.v1", "updated_at": None, "evidence": []},
    )


def _upsert(items: list[dict[str, Any]], key: str, value: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    replaced = False
    updated: list[dict[str, Any]] = []
    for item in items:
        if str(item.get(key, "")) == value:
            updated.append({**item, **payload})
            replaced = True
        else:
            updated.append(item)
    if not replaced:
        updated.append(payload)
    return updated


def _problem_id_for_project(project_dir: Path, fallback: str | None = None) -> str:
    state = read_json(project_dir / "state.json", {})
    candidate = fallback or state.get("problem_id") or project_dir.name
    return str(candidate).strip()


def _relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)


def _find_item(items: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    for item in items:
        if str(item.get(key, "")) == value:
            return item
    return None


def _dedupe_sequence(items: list[Any]) -> list[Any]:
    seen: set[str] = set()
    deduped: list[Any] = []
    for item in items:
        marker = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(item)
    return deduped


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, set):
        values = sorted(value, key=str)
    elif isinstance(value, (list, tuple, set)):
        values = list(value)
    else:
        values = [value]
    return _dedupe_sequence([str(item).strip() for item in values if str(item).strip()])


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    normalized: list[dict[str, Any]] = []
    for item in values:
        if isinstance(item, dict):
            normalized.append(dict(item))
        elif str(item).strip():
            normalized.append({"path": str(item).strip()})
    return normalized


def _normalize_evidence(value: Any) -> list[dict[str, Any]]:
    return _dedupe_sequence(_dict_list(value))


def _evidence_paths(value: Any) -> list[str]:
    paths: list[str] = []
    for item in _dict_list(value):
        candidate = item.get("path") or item.get("evidence_path") or item.get("source")
        if candidate:
            paths.append(str(candidate).strip())
    return _dedupe_sequence([path for path in paths if path])


def _json_fingerprint(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def _ensure_memory_files(project_dir: Path) -> None:
    memory_dir = project_memory_dir(project_dir)
    memory_dir.mkdir(parents=True, exist_ok=True)
    if not claim_ledger_path(project_dir).exists():
        write_json(claim_ledger_path(project_dir), load_claim_ledger(project_dir))
    if not route_ledger_path(project_dir).exists():
        write_json(route_ledger_path(project_dir), load_route_ledger(project_dir))
    if not failed_routes_path(project_dir).exists():
        write_json(failed_routes_path(project_dir), load_failed_routes(project_dir))
    if not evidence_index_path(project_dir).exists():
        write_json(evidence_index_path(project_dir), load_evidence_index(project_dir))


def append_state_transition(
    project_dir: Path,
    *,
    problem_id: str,
    state: str,
    reason: str = "",
    evidence: list[str] | None = None,
) -> dict[str, Any]:
    state_path = project_dir / "state.json"
    project_dir.mkdir(parents=True, exist_ok=True)
    previous = read_json(state_path, {})
    history = read_jsonl(state_history_path(project_dir))
    previous_state = str(previous.get("state") or (history[-1].get("state") if history else "unseen"))
    normalized_state = normalize_problem_state(state)
    changed_at = utc_now_iso()
    event = {
        "schema_version": "amra.problem_state_transition.v1",
        "problem_id": problem_id,
        "state": normalized_state,
        "previous_state": previous_state,
        "changed_at": changed_at,
        "sequence": len(history) + 1,
        "reason": reason,
        "evidence": _string_list(evidence),
    }
    payload = {
        "schema_version": "amra.problem_state.v1",
        "problem_id": problem_id,
        "state": normalized_state,
        "previous_state": previous_state,
        "updated_at": changed_at,
        "reason": reason,
        "evidence": _string_list(evidence),
        "history_path": str(state_history_path(project_dir)),
    }
    write_json(state_path, payload)
    append_jsonl(state_history_path(project_dir), event)
    return payload


def initialize_memory(project_dir: Path, *, problem_id: str | None = None) -> dict[str, str]:
    project_dir.mkdir(parents=True, exist_ok=True)
    _ensure_memory_files(project_dir)
    if not resume_pack_path(project_dir).exists():
        write_resume_pack(project_dir, problem_id=problem_id)
    return {
        "claim_ledger": str(claim_ledger_path(project_dir)),
        "route_ledger": str(route_ledger_path(project_dir)),
        "failed_routes": str(failed_routes_path(project_dir)),
        "evidence_index": str(evidence_index_path(project_dir)),
        "resume_pack": str(resume_pack_path(project_dir)),
    }


def upsert_claim(project_dir: Path, claim: dict[str, Any]) -> dict[str, Any]:
    _ensure_memory_files(project_dir)
    claim_id = str(claim.get("claim_id", "")).strip()
    if not claim_id:
        raise ValueError("claim_id is required")
    ledger = load_claim_ledger(project_dir)
    existing = _find_item(list(ledger.get("claims", [])), "claim_id", claim_id) or {}
    merged = {**existing, **claim}
    status = normalize_claim_status(str(merged.get("status", "hypothesis")))
    now = utc_now_iso()
    proof_evidence = _string_list(merged.get("proof_evidence"))
    counterexample_evidence = _string_list(merged.get("counterexample_evidence"))
    evidence = _normalize_evidence(merged.get("evidence"))
    evidence.extend({"type": "proof", "path": path} for path in proof_evidence)
    evidence.extend({"type": "counterexample", "path": path} for path in counterexample_evidence)
    payload = {
        **merged,
        "claim_id": claim_id,
        "problem_id": _problem_id_for_project(project_dir, str(merged.get("problem_id", "")) or None),
        "status": status,
        "dependencies": _string_list(merged.get("dependencies")),
        "evidence": _normalize_evidence(evidence),
        "proof_evidence": proof_evidence,
        "counterexample_evidence": counterexample_evidence,
        "reusable": bool(merged.get("reusable", False)),
        "created_at": existing.get("created_at") or now,
        "updated_at": now,
    }
    ledger["claims"] = _upsert(list(ledger.get("claims", [])), "claim_id", claim_id, payload)
    ledger["updated_at"] = now
    write_json(claim_ledger_path(project_dir), ledger)
    append_jsonl(
        claim_history_path(project_dir),
        {
            "schema_version": "amra.claim_history_event.v1",
            "event": "claim_upsert",
            "claim_id": claim_id,
            "problem_id": payload["problem_id"],
            "status": status,
            "changed_at": now,
            "payload": payload,
        },
    )
    _update_evidence_index(project_dir)
    return payload


def _attempt_marker(attempt: dict[str, Any]) -> str:
    material = {key: value for key, value in attempt.items() if key not in {"recorded_at", "updated_at"}}
    return str(attempt.get("attempt_id") or attempt.get("run_id") or _json_fingerprint(material))


def _merge_attempt_history(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [dict(item) for item in existing]
    markers = [_attempt_marker(item) for item in merged]
    for attempt in incoming:
        normalized = dict(attempt)
        marker = _attempt_marker(normalized)
        if marker in markers:
            merged[markers.index(marker)] = {**merged[markers.index(marker)], **normalized}
        else:
            merged.append(normalized)
            markers.append(marker)
    return merged


def upsert_route(project_dir: Path, route: dict[str, Any]) -> dict[str, Any]:
    _ensure_memory_files(project_dir)
    route_id = str(route.get("route_id") or route.get("name") or "").strip()
    if not route_id:
        raise ValueError("route_id or name is required")
    ledger = load_route_ledger(project_dir)
    existing = _find_item(list(ledger.get("routes", [])), "route_id", route_id) or {}
    merged = {**existing, **route}
    status = normalize_route_status(str(merged.get("status", "new")))
    now = utc_now_iso()
    incoming_attempts = _dict_list(route.get("attempt_history") or route.get("attempts"))
    if route.get("attempt"):
        incoming_attempts.extend(_dict_list(route.get("attempt")))
    for attempt in incoming_attempts:
        attempt.setdefault("recorded_at", now)
    attempt_history = _merge_attempt_history(_dict_list(existing.get("attempt_history")), incoming_attempts)
    payload = {
        **merged,
        "route_id": route_id,
        "problem_id": _problem_id_for_project(project_dir, str(merged.get("problem_id", "")) or None),
        "target_claim": str(merged.get("target_claim", "")).strip(),
        "status": status,
        "required_dependencies": _string_list(merged.get("required_dependencies") or merged.get("dependencies")),
        "blocker": str(merged.get("blocker", "")).strip(),
        "attempt_history": attempt_history,
        "evaluator_verdict": dict(merged.get("evaluator_verdict") or {}),
        "continuation_cost_estimate": merged.get("continuation_cost_estimate"),
        "created_at": existing.get("created_at") or now,
        "updated_at": now,
    }
    ledger["routes"] = _upsert(list(ledger.get("routes", [])), "route_id", route_id, payload)
    ledger["updated_at"] = now
    write_json(route_ledger_path(project_dir), ledger)
    append_jsonl(
        route_history_path(project_dir),
        {
            "schema_version": "amra.route_history_event.v1",
            "event": "route_upsert",
            "route_id": route_id,
            "problem_id": payload["problem_id"],
            "status": status,
            "changed_at": now,
            "attempt_count": len(attempt_history),
            "payload": payload,
        },
    )
    return payload


def _failed_route_fingerprint(payload: dict[str, Any]) -> str:
    if payload.get("fingerprint"):
        return str(payload["fingerprint"]).strip()
    material = {
        "problem_id": payload.get("problem_id", ""),
        "route_id": payload.get("route_id", ""),
        "failed_assertion": payload.get("failed_assertion", ""),
        "approach": payload.get("approach") or payload.get("summary", ""),
        "failure_mode": payload.get("failure_mode", ""),
    }
    return _json_fingerprint(material)


def _merge_failed_route(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    evidence = _dedupe_sequence(_normalize_evidence(existing.get("evidence")) + _normalize_evidence(incoming.get("evidence")))
    evidence_paths = _dedupe_sequence(
        _string_list(existing.get("evidence_paths"))
        + _string_list(incoming.get("evidence_paths"))
        + _evidence_paths(existing.get("evidence"))
        + _evidence_paths(incoming.get("evidence"))
    )
    return {
        **existing,
        **incoming,
        "recorded_at": existing.get("recorded_at") or incoming.get("recorded_at"),
        "last_seen_at": incoming.get("last_seen_at") or incoming.get("recorded_at") or existing.get("last_seen_at"),
        "evidence": evidence,
        "evidence_paths": evidence_paths,
    }


def record_failed_route(project_dir: Path, failed_route: dict[str, Any]) -> dict[str, Any]:
    _ensure_memory_files(project_dir)
    route_id = str(failed_route.get("route_id") or failed_route.get("name") or "").strip()
    if not route_id:
        raise ValueError("route_id or name is required")
    ledger = load_failed_routes(project_dir)
    existing_items = list(ledger.get("failed_routes", []))
    merged_input = dict(failed_route)
    failure_mode = normalize_failure_mode(str(merged_input.get("failure_mode", "proof_gap")))
    now = utc_now_iso()
    payload = {
        **merged_input,
        "route_id": route_id,
        "problem_id": _problem_id_for_project(project_dir, str(merged_input.get("problem_id", "")) or None),
        "status": "failed",
        "failure_mode": failure_mode,
        "failure_class": str(merged_input.get("failure_class") or FAILURE_CLASSES_BY_MODE[failure_mode]),
        "resume_condition": str(merged_input.get("resume_condition", "")).strip(),
        "evidence": _normalize_evidence(merged_input.get("evidence")),
        "evidence_paths": _string_list(merged_input.get("evidence_paths"))
        + _string_list([merged_input.get("evidence_path")] if merged_input.get("evidence_path") else []),
        "recorded_at": now,
        "last_seen_at": now,
    }
    payload["fingerprint"] = _failed_route_fingerprint(payload)
    existing = _find_item(existing_items, "fingerprint", payload["fingerprint"])
    final_payload = _merge_failed_route(existing or {}, payload)
    if existing is None:
        ledger["failed_routes"] = existing_items + [final_payload]
    else:
        ledger["failed_routes"] = _upsert(existing_items, "fingerprint", payload["fingerprint"], final_payload)
    ledger["updated_at"] = now
    write_json(failed_routes_path(project_dir), ledger)
    append_jsonl(
        failed_route_history_path(project_dir),
        {
            "schema_version": "amra.failed_route_history_event.v1",
            "event": "failed_route_recorded",
            "route_id": route_id,
            "problem_id": final_payload["problem_id"],
            "fingerprint": final_payload["fingerprint"],
            "failure_mode": failure_mode,
            "deduped": existing is not None,
            "recorded_at": now,
            "payload": final_payload,
        },
    )
    _update_evidence_index(project_dir)
    return final_payload


def _update_evidence_index(project_dir: Path) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = []
    problem_id = _problem_id_for_project(project_dir)
    for claim in load_claim_ledger(project_dir).get("claims", []):
        for item in _normalize_evidence(claim.get("evidence")):
            evidence.append({"problem_id": problem_id, "owner_type": "claim", "owner_id": claim.get("claim_id"), **item})
    for failed_route in load_failed_routes(project_dir).get("failed_routes", []):
        for path in _string_list(failed_route.get("evidence_paths")):
            evidence.append(
                {
                    "problem_id": problem_id,
                    "owner_type": "failed_route",
                    "owner_id": failed_route.get("fingerprint"),
                    "path": path,
                    "type": failed_route.get("failure_mode", "proof_gap"),
                }
            )
        for item in _normalize_evidence(failed_route.get("evidence")):
            evidence.append(
                {
                    "problem_id": problem_id,
                    "owner_type": "failed_route",
                    "owner_id": failed_route.get("fingerprint"),
                    **item,
                }
            )
    payload = {
        "schema_version": "amra.evidence_index.v1",
        "updated_at": utc_now_iso(),
        "evidence": _dedupe_sequence(evidence),
    }
    write_json(evidence_index_path(project_dir), payload)
    return payload


def load_verified_declarations(project_dir: Path) -> dict[str, Any]:
    return read_json(
        verified_declarations_path(project_dir),
        {
            "schema_version": VERIFIED_DECLARATIONS_SCHEMA_VERSION,
            "updated_at": None,
            "problem_id": _problem_id_for_project(project_dir),
            "declarations": [],
        },
    )


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def _skip_consolidation_artifact(path: Path, project_dir: Path) -> bool:
    if path.name in PRIVATE_ARTIFACT_NAMES:
        return True
    if ".lake" in path.parts or ".locks" in path.parts:
        return True
    if path.resolve(strict=False) == (project_dir / "state.json").resolve(strict=False):
        return True
    if _is_under(path, project_memory_dir(project_dir)):
        return True
    return False


def _safe_read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _slug(value: str, *, fallback: str = "item") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or fallback


def _label_key(label: str) -> str:
    aliases = {
        "claim": "claim_id",
        "claim id": "claim_id",
        "claim-id": "claim_id",
        "claim status": "status",
        "route": "route_id",
        "route id": "route_id",
        "route-id": "route_id",
        "route status": "status",
        "failure mode": "failure_mode",
        "failed assertion": "failed_assertion",
        "resume condition": "resume_condition",
        "target claim": "target_claim",
        "core idea": "core_idea",
        "lean declaration": "lean_name",
        "declaration": "lean_name",
        "review status": "review_status",
    }
    normalized = re.sub(r"[_-]+", " ", label.strip().lower())
    return aliases.get(normalized, normalized.replace(" ", "_"))


def _parse_label_blocks(text: str, *, primary_keys: set[str]) -> list[dict[str, str]]:
    label_re = re.compile(r"^\s*(?:[-*]\s*)?`?([A-Za-z][A-Za-z _-]{1,48})`?\s*:\s*(.*?)\s*$")
    blocks: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        match = label_re.match(line)
        if not match:
            continue
        key = _label_key(match.group(1))
        value = match.group(2).strip().strip("`")
        if key in primary_keys and current.get(key):
            blocks.append(current)
            current = {}
        current[key] = value
    if current:
        blocks.append(current)
    return blocks


def _first_heading_or_line(text: str, fallback: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.startswith("#"):
            return cleaned.lstrip("#").strip() or fallback
        if not cleaned.startswith(("-", "*")):
            return cleaned
    return fallback


def _claim_status_from_artifact(value: Any, *, verified: bool = False, default: str = "sketch") -> str:
    if verified:
        return "lean_verified"
    raw = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "verified": "lean_verified",
        "lean_verified": "lean_verified",
        "proved_candidate": "route_supported",
        "proof_candidate": "route_supported",
        "route_supported": "route_supported",
        "partial": "sketch",
        "sketch": "sketch",
        "blocked": "needs_review",
        "failed": "needs_review",
        "review_rejected": "review_rejected",
        "rejected": "review_rejected",
        "counterexample": "counterexample_suspected",
        "counterexample_suspected": "counterexample_suspected",
        "false": "false",
    }
    candidate = mapping.get(raw, raw or default)
    return normalize_claim_status(candidate if candidate in CLAIM_STATUSES else default)


def _route_status_from_artifact(value: Any, *, verified: bool = False, default: str = "new") -> str:
    if verified:
        return "completed"
    raw = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "verified": "completed",
        "completed": "completed",
        "proved_candidate": "promising",
        "proof_candidate": "promising",
        "partial": "promising",
        "progress": "promising",
        "blocked": "blocked",
        "failed": "failed",
        "counterexample_suspected": "failed",
        "rejected": "blocked",
    }
    candidate = mapping.get(raw, raw or default)
    return normalize_route_status(candidate if candidate in ROUTE_STATUSES else default)


def _failure_mode_from_artifact(value: Any, *texts: Any) -> str:
    raw = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if raw in FAILURE_MODES:
        return raw
    text = " ".join(str(item or "") for item in texts).lower()
    if "counterexample" in text:
        return "counterexample_candidate"
    if "statement mismatch" in text or "header mismatch" in text or "does not match" in text:
        return "lean_statement_mismatch"
    if "mathlib" in text or "unknown constant" in text or "api" in text:
        return "missing_mathlib_api"
    if "timeout" in text or "resource" in text or "time budget" in text:
        return "resource_timeout"
    if "source" in text or "provenance" in text or "exact statement" in text:
        return "source_gap"
    if "formal" in text or "lean" in text or "target theorem" in text:
        return "formalization_blocked"
    if "model" in text or "invariant" in text:
        return "modeling_too_weak"
    if "case explosion" in text or "combinatorial" in text:
        return "combinatorial_case_explosion"
    return "proof_gap"


def _source_evidence(path: Path, repo_root: Path | None, artifact_type: str) -> dict[str, str]:
    root = repo_root or path.parent
    return {"type": artifact_type, "path": _relative_path(path, root)}


def _payload_list(payload: dict[str, Any], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        items = value if isinstance(value, list) else [value]
        for item in items:
            if isinstance(item, dict):
                records.append(dict(item))
            elif str(item).strip():
                records.append({key.rstrip("s"): str(item).strip()})
    return records


def _json_claim_updates(path: Path, payload: dict[str, Any], *, repo_root: Path | None) -> list[dict[str, Any]]:
    records = _payload_list(payload, ("claims", "claim_updates", "amra_claims"))
    if payload.get("claim_id") and path.name not in {"state.json", "report.json", "attempt_report.json"}:
        records.append(payload)
    claims: list[dict[str, Any]] = []
    for item in records:
        claim_id = str(item.get("claim_id") or item.get("id") or "").strip()
        if not claim_id:
            continue
        evidence = _normalize_evidence(item.get("evidence"))
        evidence.append(_source_evidence(path, repo_root, "memory_consolidation"))
        claims.append(
            {
                **item,
                "claim_id": claim_id,
                "statement_nl": str(item.get("statement_nl") or item.get("statement") or item.get("title") or "").strip(),
                "status": _claim_status_from_artifact(item.get("status"), default="hypothesis"),
                "evidence": evidence,
            }
        )
    return claims


def _json_route_updates(path: Path, payload: dict[str, Any], *, repo_root: Path | None) -> list[dict[str, Any]]:
    records = _payload_list(payload, ("routes", "route_updates", "amra_routes", "route_candidates", "candidates"))
    if payload.get("route_id") and path.name not in {"state.json", "report.json", "attempt_report.json"}:
        records.append(payload)
    routes: list[dict[str, Any]] = []
    for item in records:
        route_id = str(item.get("route_id") or item.get("id") or item.get("name") or "").strip()
        if not route_id:
            continue
        routes.append(
            {
                **item,
                "route_id": route_id,
                "target_claim": str(item.get("target_claim") or item.get("claim_id") or "").strip(),
                "core_idea": str(item.get("core_idea") or item.get("title") or item.get("summary") or "").strip(),
                "status": _route_status_from_artifact(item.get("status"), default="new"),
                "attempt": {
                    "attempt_id": str(item.get("attempt_id") or _slug(_relative_path(path, repo_root or path.parent))),
                    "artifact": _relative_path(path, repo_root or path.parent),
                    "source": "memory_consolidation",
                },
            }
        )
    return routes


def _json_failed_route_updates(path: Path, payload: dict[str, Any], *, repo_root: Path | None) -> list[dict[str, Any]]:
    if path.name == "failed_routes.json" and "memory" in path.parts:
        return []
    records = _payload_list(payload, ("failed_routes", "failed_route_updates", "amra_failed_routes"))
    if payload.get("failure_mode") and (payload.get("route_id") or payload.get("name")):
        records.append(payload)
    failed: list[dict[str, Any]] = []
    for item in records:
        route_id = str(item.get("route_id") or item.get("name") or item.get("id") or "").strip()
        if not route_id:
            continue
        text = json.dumps(item, ensure_ascii=False)
        failed.append(
            {
                **item,
                "route_id": route_id,
                "failure_mode": _failure_mode_from_artifact(item.get("failure_mode"), text),
                "failed_assertion": str(item.get("failed_assertion") or item.get("assertion") or item.get("summary") or "").strip(),
                "approach": str(item.get("approach") or item.get("core_idea") or item.get("description") or "").strip(),
                "resume_condition": str(item.get("resume_condition") or "").strip(),
                "evidence": _normalize_evidence(item.get("evidence")) + [_source_evidence(path, repo_root, "failed_route_artifact")],
            }
        )
    return failed


def _report_verified(payload: dict[str, Any]) -> bool:
    status = str(payload.get("status") or "").strip().lower()
    best_audit = payload.get("best_audit") if isinstance(payload.get("best_audit"), dict) else {}
    final_observation = payload.get("final_observation") if isinstance(payload.get("final_observation"), dict) else {}
    return (
        status == "verified"
        or bool(payload.get("verified"))
        or bool(best_audit.get("verified"))
        or bool(final_observation.get("contract_satisfied") and status == "verified")
    )


def _report_blockers(payload: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for source in (
        payload,
        payload.get("best_audit") if isinstance(payload.get("best_audit"), dict) else {},
        payload.get("final_observation") if isinstance(payload.get("final_observation"), dict) else {},
    ):
        blockers.extend(_string_list(source.get("blockers") if isinstance(source, dict) else None))
    return _dedupe_sequence(blockers)


def _report_targets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    best_audit = payload.get("best_audit") if isinstance(payload.get("best_audit"), dict) else {}
    direct_target = payload.get("target") if isinstance(payload.get("target"), dict) else {}
    if direct_target.get("found") or direct_target.get("name"):
        targets.append(dict(direct_target))
    audit_target = best_audit.get("target") if isinstance(best_audit.get("target"), dict) else {}
    if audit_target.get("found") or audit_target.get("name"):
        targets.append(dict(audit_target))
    target_name = str(payload.get("target_theorem") or audit_target.get("name") or "").strip()
    if target_name and not any(str(item.get("name") or item.get("full_name") or "") == target_name for item in targets):
        targets.append(
            {
                "name": target_name,
                "full_name": target_name,
                "kind": "theorem",
                "path": payload.get("target_file") or audit_target.get("path") or "",
                "relative_path": audit_target.get("relative_path") or str(payload.get("target_file") or ""),
                "line": audit_target.get("line") or 0,
                "found": bool(audit_target.get("found") or _report_verified(payload)),
            }
        )
    final_observation = payload.get("final_observation") if isinstance(payload.get("final_observation"), dict) else {}
    target_reports = final_observation.get("target_reports") if isinstance(final_observation.get("target_reports"), dict) else {}
    for target, report in target_reports.items():
        if isinstance(report, dict) and report.get("found"):
            targets.append({"name": str(target), "full_name": str(report.get("full_name") or target), **report})
    return targets


def _json_report_updates(path: Path, payload: dict[str, Any], *, repo_root: Path | None) -> dict[str, list[dict[str, Any]]]:
    is_report = path.name in {"report.json", "state.json", "attempt_report.json", "after_audit.json", "best_audit.json", "initial_audit.json"}
    if not is_report:
        return {"claims": [], "routes": [], "failed_routes": [], "verified_declarations": []}
    if path.name == "state.json" and "runs" not in path.parts and "attempts" not in path.parts:
        return {"claims": [], "routes": [], "failed_routes": [], "verified_declarations": []}

    verified = _report_verified(payload)
    status = str(payload.get("status") or ("verified" if payload.get("verified") else "")).strip()
    blockers = _report_blockers(payload)
    targets = _report_targets(payload)
    target_names = [str(item.get("name") or item.get("full_name") or "").strip() for item in targets if str(item.get("name") or item.get("full_name") or "").strip()]
    if not target_names:
        target_names = _string_list(payload.get("attack_targets"))
    if not target_names and payload.get("claim_id"):
        target_names = [str(payload["claim_id"]).strip()]
    claims: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    failed_routes: list[dict[str, Any]] = []
    declarations: list[dict[str, Any]] = []
    evidence = [_source_evidence(path, repo_root, "run_report")]

    for target in target_names:
        claim_id = str(payload.get("claim_id") or target).strip()
        claims.append(
            {
                "claim_id": claim_id,
                "kind": "lean_declaration",
                "statement_nl": str(payload.get("statement") or payload.get("expected_target_header") or target).strip(),
                "status": _claim_status_from_artifact(status, verified=verified, default="lean_partial"),
                "evidence": evidence,
                "lean_name": target,
            }
        )
        route_id = str(payload.get("route_id") or f"lean:{target}").strip()
        routes.append(
            {
                "route_id": route_id,
                "target_claim": claim_id,
                "core_idea": f"Lean formalization of `{target}`.",
                "status": _route_status_from_artifact(status, verified=verified, default="blocked" if blockers else "promising"),
                "blocker": "; ".join(blockers),
                "attempt": {
                    "attempt_id": str(payload.get("run_name") or payload.get("run_dir") or _slug(_relative_path(path, repo_root or path.parent))),
                    "run_dir": str(payload.get("run_dir") or path.parent),
                    "artifact": _relative_path(path, repo_root or path.parent),
                    "progress_velocity": payload.get("progress_velocity"),
                    "status": status,
                },
            }
        )
    if verified:
        for target in targets:
            name = str(target.get("full_name") or target.get("name") or "").strip()
            if not name:
                continue
            declarations.append(
                {
                    "name": str(target.get("name") or name).strip(),
                    "full_name": name,
                    "lean_name": name,
                    "kind": str(target.get("kind") or "theorem"),
                    "path": str(target.get("path") or payload.get("target_file") or ""),
                    "relative_path": str(target.get("relative_path") or payload.get("target_file") or ""),
                    "line": int(target.get("line") or 0),
                    "source_report": _relative_path(path, repo_root or path.parent),
                    "status": "lean_verified",
                }
            )
    elif blockers or str(payload.get("stop_reason") or "").strip():
        route_id = str(payload.get("route_id") or (f"lean:{target_names[0]}" if target_names else f"run:{path.parent.name}"))
        failed_routes.append(
            {
                "route_id": route_id,
                "failure_mode": _failure_mode_from_artifact(payload.get("failure_mode"), status, blockers, payload.get("stop_reason")),
                "failed_assertion": "; ".join(blockers) or str(payload.get("stop_reason") or "Run did not verify."),
                "approach": str(payload.get("next_action") or payload.get("global_reassessment_reason") or "").strip(),
                "resume_condition": str(payload.get("resume_condition") or "A new blocker-specific lemma or corrected Lean statement is available.").strip(),
                "evidence": evidence,
            }
        )
    return {"claims": claims, "routes": routes, "failed_routes": failed_routes, "verified_declarations": declarations}


def _text_claim_updates(path: Path, text: str, *, repo_root: Path | None) -> list[dict[str, Any]]:
    blocks = _parse_label_blocks(text, primary_keys={"claim_id"})
    claims: list[dict[str, Any]] = []
    for block in blocks:
        claim_id = str(block.get("claim_id") or "").strip()
        if not claim_id:
            continue
        claims.append(
            {
                "claim_id": claim_id,
                "statement_nl": block.get("statement") or block.get("statement_nl") or "",
                "status": _claim_status_from_artifact(block.get("status"), default="sketch"),
                "evidence": [_source_evidence(path, repo_root, "proof_note")],
            }
        )
    if claims:
        return claims
    if path.name == "proof_package.md" or (path.parent.name == "sketches" and path.suffix == ".md"):
        stripped = text.strip()
        if stripped:
            claims.append(
                {
                    "claim_id": "main",
                    "statement_nl": _first_heading_or_line(stripped, "Main proof sketch")[:500],
                    "status": "route_supported" if "proof:" in stripped.lower() or "proof sketch" in stripped.lower() else "sketch",
                    "evidence": [_source_evidence(path, repo_root, "proof_output")],
                }
            )
    return claims


def _text_route_updates(path: Path, text: str, *, repo_root: Path | None) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    for block in _parse_label_blocks(text, primary_keys={"route_id"}):
        route_id = str(block.get("route_id") or "").strip()
        if not route_id:
            continue
        routes.append(
            {
                "route_id": route_id,
                "target_claim": str(block.get("target_claim") or block.get("claim_id") or "").strip(),
                "core_idea": str(block.get("core_idea") or block.get("approach") or block.get("summary") or "").strip(),
                "status": _route_status_from_artifact(block.get("status"), default="promising"),
                "blocker": str(block.get("blocker") or "").strip(),
                "attempt": {
                    "attempt_id": _slug(_relative_path(path, repo_root or path.parent)),
                    "artifact": _relative_path(path, repo_root or path.parent),
                    "source": "proof_note",
                },
            }
        )
    return routes


def _text_failed_route_updates(path: Path, text: str, *, repo_root: Path | None) -> list[dict[str, Any]]:
    lowered_name = path.name.lower()
    if lowered_name not in {"failed_routes.md", "blockers.md", "counterexample_report.md"} and "failed route" not in text.lower():
        return []
    failed: list[dict[str, Any]] = []
    for block in _parse_label_blocks(text, primary_keys={"route_id"}):
        route_id = str(block.get("route_id") or "").strip()
        if not route_id:
            continue
        failed.append(
            {
                "route_id": route_id,
                "failure_mode": _failure_mode_from_artifact(block.get("failure_mode"), text),
                "failed_assertion": str(block.get("failed_assertion") or block.get("blocker") or "").strip(),
                "approach": str(block.get("approach") or block.get("core_idea") or block.get("summary") or "").strip(),
                "resume_condition": str(block.get("resume_condition") or "").strip(),
                "evidence": [_source_evidence(path, repo_root, "failed_route_note")],
            }
        )
    if failed:
        return failed
    stripped = text.strip()
    if stripped and lowered_name in {"failed_routes.md", "counterexample_report.md"}:
        title = _first_heading_or_line(stripped, path.stem)
        failed.append(
            {
                "route_id": _slug(title),
                "failure_mode": _failure_mode_from_artifact("counterexample_candidate" if lowered_name == "counterexample_report.md" else "", stripped),
                "failed_assertion": title[:500],
                "approach": stripped[:1000],
                "resume_condition": "Only resume if a materially new lemma, source correction, or counterexample review changes the route.",
                "evidence": [_source_evidence(path, repo_root, "failed_route_note")],
            }
        )
    return failed


def _text_verified_declarations(path: Path, text: str, *, repo_root: Path | None) -> list[dict[str, Any]]:
    if path.name != "verified_lean_declarations.md":
        return []
    declarations: list[dict[str, Any]] = []
    declaration_re = re.compile(r"\b(theorem|lemma)\s+(`[^`]+`|[A-Za-z_][A-Za-z0-9_'.!?]*)")
    for match in declaration_re.finditer(text):
        raw = match.group(2).strip("`")
        declarations.append(
            {
                "name": raw,
                "full_name": raw,
                "lean_name": raw,
                "kind": match.group(1),
                "source_report": _relative_path(path, repo_root or path.parent),
                "status": "lean_verified",
            }
        )
    for block in _parse_label_blocks(text, primary_keys={"lean_name"}):
        name = str(block.get("lean_name") or block.get("name") or "").strip()
        if not name:
            continue
        declarations.append(
            {
                "name": name,
                "full_name": name,
                "lean_name": name,
                "kind": str(block.get("kind") or "theorem"),
                "source_report": _relative_path(path, repo_root or path.parent),
                "status": "lean_verified",
            }
        )
    return declarations


def _review_updates(path: Path, payload_or_text: Any, *, repo_root: Path | None) -> dict[str, list[dict[str, Any]]]:
    if isinstance(payload_or_text, dict):
        text = json.dumps(payload_or_text, ensure_ascii=False)
        status = str(payload_or_text.get("review_status") or payload_or_text.get("status") or payload_or_text.get("verdict") or "").lower()
        claim_ids = _string_list(payload_or_text.get("claim_ids") or payload_or_text.get("claim_id"))
        route_ids = _string_list(payload_or_text.get("route_ids") or payload_or_text.get("route_id"))
        note = str(payload_or_text.get("summary") or payload_or_text.get("notes") or payload_or_text.get("reason") or "")
    else:
        text = str(payload_or_text)
        blocks = _parse_label_blocks(text, primary_keys={"claim_id", "route_id"})
        status = ""
        claim_ids = []
        route_ids = []
        note = _first_heading_or_line(text, "review note")
        for block in blocks:
            status = status or str(block.get("review_status") or block.get("status") or "")
            claim_ids.extend(_string_list(block.get("claim_id")))
            route_ids.extend(_string_list(block.get("route_id")))
    lowered = status.lower().replace(" ", "_").replace("-", "_")
    if not (status or "review" in path.parts or "review" in path.name):
        return {"claims": [], "routes": [], "failed_routes": []}
    claims: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    failed_routes: list[dict[str, Any]] = []
    evidence = [_source_evidence(path, repo_root, "review_note")]
    approved = lowered in {"approved", "accepted", "pass", "passed", "reviewed", "checkpoint_verified"}
    rejected = lowered in {"rejected", "review_rejected", "failed", "needs_changes", "request_changes"}
    for claim_id in _dedupe_sequence(claim_ids):
        claims.append(
            {
                "claim_id": claim_id,
                "status": "route_supported" if approved else "review_rejected" if rejected else "needs_review",
                "review_status": status,
                "evidence": evidence,
            }
        )
    for route_id in _dedupe_sequence(route_ids):
        routes.append(
            {
                "route_id": route_id,
                "status": "promising" if approved else "blocked" if rejected else "new",
                "blocker": note if rejected else "",
                "evaluator_verdict": {"review_status": status, "source": _relative_path(path, repo_root or path.parent)},
                "attempt": {
                    "attempt_id": _slug(_relative_path(path, repo_root or path.parent)),
                    "artifact": _relative_path(path, repo_root or path.parent),
                    "source": "review_note",
                },
            }
        )
        if rejected:
            failed_routes.append(
                {
                    "route_id": route_id,
                    "failure_mode": _failure_mode_from_artifact("", text),
                    "failed_assertion": note,
                    "approach": "",
                    "resume_condition": "Reviewer feedback has been addressed by a materially different route.",
                    "evidence": evidence,
                }
            )
    return {"claims": claims, "routes": routes, "failed_routes": failed_routes}


def _declaration_key(declaration: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(declaration.get("problem_id") or ""),
        str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or ""),
        str(declaration.get("header") or declaration.get("declaration_line") or ""),
    )


def _merge_verified_declarations(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [dict(item) for item in existing]
    keys = [_declaration_key(item) for item in merged]
    for item in incoming:
        key = _declaration_key(item)
        if not any(part for part in key):
            continue
        if key in keys:
            index = keys.index(key)
            merged[index] = {**merged[index], **item}
        else:
            merged.append(dict(item))
            keys.append(key)
    return sorted(merged, key=lambda item: (str(item.get("problem_id", "")), str(item.get("full_name") or item.get("name") or "")))


def _infer_repo_root(project_dir: Path) -> Path:
    for parent in (project_dir, *project_dir.parents):
        if parent.name == "artifacts":
            return parent.parent
    if project_dir.parent.name == "projects":
        return project_dir.parent.parent
    return project_dir.parent


def consolidate_project_memory(
    project_dir: Path,
    *,
    repo_root: Path | None = None,
    problem_id: str | None = None,
) -> dict[str, Any]:
    """Merge durable AMRA run artifacts into ledgers, resume memory, and indexes."""

    project_dir = project_dir.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve() if repo_root is not None else _infer_repo_root(project_dir)
    resolved_problem_id = _problem_id_for_project(project_dir, problem_id)
    _ensure_memory_files(project_dir)

    claim_updates: list[dict[str, Any]] = []
    route_updates: list[dict[str, Any]] = []
    failed_route_updates: list[dict[str, Any]] = []
    verified_declarations: list[dict[str, Any]] = []
    artifact_paths: list[str] = []

    for path in sorted(project_dir.rglob("*")):
        if not path.is_file() or _skip_consolidation_artifact(path, project_dir):
            continue
        if path.suffix == ".json" and path.name in CONSOLIDATION_JSON_NAMES:
            payload = _safe_read_json(path)
            if not payload:
                continue
            artifact_paths.append(_relative_path(path, repo_root or project_dir))
            claim_updates.extend(_json_claim_updates(path, payload, repo_root=repo_root))
            route_updates.extend(_json_route_updates(path, payload, repo_root=repo_root))
            failed_route_updates.extend(_json_failed_route_updates(path, payload, repo_root=repo_root))
            report_updates = _json_report_updates(path, payload, repo_root=repo_root)
            claim_updates.extend(report_updates["claims"])
            route_updates.extend(report_updates["routes"])
            failed_route_updates.extend(report_updates["failed_routes"])
            verified_declarations.extend(report_updates["verified_declarations"])
            if _report_verified(payload) or path.name == "verified_declarations.json":
                verified_declarations.extend(_payload_list(payload, ("verified_declarations", "declarations")))
            if path.name == "verified_declarations.json":
                verified_declarations.extend(_payload_list(payload, ("declarations", "verified_declarations")))
            if "review" in path.parts or "review" in path.name:
                review = _review_updates(path, payload, repo_root=repo_root)
                claim_updates.extend(review["claims"])
                route_updates.extend(review["routes"])
                failed_route_updates.extend(review["failed_routes"])
        elif path.suffix == ".md" and (path.name in CONSOLIDATION_TEXT_NAMES or "review" in path.parts or path.parent.name == "sketches"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if not text.strip():
                continue
            artifact_paths.append(_relative_path(path, repo_root or project_dir))
            claim_updates.extend(_text_claim_updates(path, text, repo_root=repo_root))
            route_updates.extend(_text_route_updates(path, text, repo_root=repo_root))
            failed_route_updates.extend(_text_failed_route_updates(path, text, repo_root=repo_root))
            verified_declarations.extend(_text_verified_declarations(path, text, repo_root=repo_root))
            if "review" in path.parts or "review" in path.name:
                review = _review_updates(path, text, repo_root=repo_root)
                claim_updates.extend(review["claims"])
                route_updates.extend(review["routes"])
                failed_route_updates.extend(review["failed_routes"])

    claims: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    failed_routes: list[dict[str, Any]] = []
    for claim in claim_updates:
        claim.setdefault("problem_id", resolved_problem_id)
        claims.append(upsert_claim(project_dir, claim))
    for route in route_updates:
        route.setdefault("problem_id", resolved_problem_id)
        routes.append(upsert_route(project_dir, route))
    for failed_route in failed_route_updates:
        failed_route.setdefault("problem_id", resolved_problem_id)
        failed_routes.append(record_failed_route(project_dir, failed_route))

    existing_declarations = list(load_verified_declarations(project_dir).get("declarations", []))
    normalized_declarations: list[dict[str, Any]] = []
    for declaration in verified_declarations:
        name = str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or "").strip()
        if not name:
            continue
        normalized_declarations.append(
            {
                **declaration,
                "problem_id": resolved_problem_id,
                "name": str(declaration.get("name") or name).strip(),
                "full_name": name,
                "lean_name": str(declaration.get("lean_name") or name).strip(),
                "status": "lean_verified",
            }
        )
    merged_declarations = _merge_verified_declarations(existing_declarations, normalized_declarations)
    if merged_declarations:
        write_json(
            verified_declarations_path(project_dir),
            {
                "schema_version": VERIFIED_DECLARATIONS_SCHEMA_VERSION,
                "updated_at": utc_now_iso(),
                "problem_id": resolved_problem_id,
                "declarations": merged_declarations,
            },
        )

    evidence_index = _update_evidence_index(project_dir)
    resume_pack = write_resume_pack(project_dir, problem_id=resolved_problem_id)
    indexes = update_global_memory(repo_root, project_dir=project_dir, problem_id=resolved_problem_id)
    payload = {
        "schema_version": CONSOLIDATION_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "project_dir": str(project_dir),
        "problem_id": resolved_problem_id,
        "artifact_count": len(_dedupe_sequence(artifact_paths)),
        "artifacts": _dedupe_sequence(artifact_paths),
        "claim_update_count": len(claims),
        "route_update_count": len(routes),
        "failed_route_update_count": len(failed_routes),
        "verified_declaration_count": len(merged_declarations),
        "claims": [claim.get("claim_id") for claim in claims],
        "routes": [route.get("route_id") for route in routes],
        "failed_route_fingerprints": [route.get("fingerprint") for route in failed_routes],
        "verified_declarations": [item.get("full_name") or item.get("name") for item in merged_declarations],
        "evidence_index": evidence_index_path(project_dir).as_posix(),
        "resume_pack": resume_pack["path"],
        "indexes": indexes,
    }
    write_json(consolidation_report_path(project_dir), payload)
    return payload


def retrieve_failed_routes(
    project_dir: Path,
    *,
    query: str = "",
    route_id: str = "",
    failure_mode: str = "",
    limit: int = 10,
) -> dict[str, Any]:
    routes = list(load_failed_routes(project_dir).get("failed_routes", []))
    query_tokens = [token for token in re.findall(r"[A-Za-z0-9_]+", query.lower()) if len(token) > 1]
    wanted_route = route_id.strip().lower()
    wanted_mode = failure_mode.strip()
    scored: list[tuple[int, dict[str, Any]]] = []
    for route in routes:
        blob = json.dumps(route, ensure_ascii=False).lower()
        score = 0
        if wanted_route and wanted_route == str(route.get("route_id", "")).lower():
            score += 100
        elif wanted_route and wanted_route in blob:
            score += 50
        if wanted_mode and wanted_mode == str(route.get("failure_mode", "")):
            score += 40
        if query_tokens:
            score += sum(8 for token in query_tokens if token in blob)
        if not query_tokens and not wanted_route and not wanted_mode:
            score = 1
        if score > 0:
            scored.append((score, route))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("last_seen_at") or item[1].get("recorded_at") or ""), str(item[1].get("route_id", ""))))
    selected = [{"score": score, **route} for score, route in scored[: max(0, int(limit))]]
    return {
        "schema_version": FAILED_ROUTE_RETRIEVAL_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "problem_id": _problem_id_for_project(project_dir),
        "query": query,
        "route_id": route_id,
        "failure_mode": failure_mode,
        "limit": max(0, int(limit)),
        "match_count": len(scored),
        "failed_routes": selected,
    }


def render_failed_route_prompt_block(
    project_dir: Path,
    *,
    query: str = "",
    route_id: str = "",
    failure_mode: str = "",
    limit: int = 5,
) -> str:
    retrieval = retrieve_failed_routes(
        project_dir,
        query=query,
        route_id=route_id,
        failure_mode=failure_mode,
        limit=limit,
    )
    lines = ["## Failed Route Memory", ""]
    routes = retrieval["failed_routes"]
    if not routes:
        lines.append("- No matching failed routes.")
        return "\n".join(lines) + "\n"
    for route in routes:
        lines.append(
            f"- `{route.get('route_id')}` failure_mode=`{route.get('failure_mode')}` fingerprint=`{route.get('fingerprint')}`"
        )
        if route.get("failed_assertion"):
            lines.append(f"  - Failed assertion: {route['failed_assertion']}")
        if route.get("approach") or route.get("summary"):
            lines.append(f"  - Approach: {route.get('approach') or route.get('summary')}")
        lines.append(f"  - Resume only if: {route.get('resume_condition') or 'no resume condition recorded'}")
        lines.append("  - Do not repeat this route unless the resume condition is met.")
    return "\n".join(lines) + "\n"


consolidate_memory = consolidate_project_memory
consolidate_portfolio_memory = consolidate_project_memory
retrieve_failed_route_memory = retrieve_failed_routes
render_failed_route_memory = render_failed_route_prompt_block
failed_route_prompt_block = render_failed_route_prompt_block


def _merge_index_items(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
    key_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    merged = [dict(item) for item in existing]
    keys = [tuple(str(item.get(field, "")) for field in key_fields) for item in merged]
    for item in incoming:
        key = tuple(str(item.get(field, "")) for field in key_fields)
        if key in keys:
            index = keys.index(key)
            merged[index] = {**merged[index], **item}
        else:
            merged.append(dict(item))
            keys.append(key)
    return sorted(merged, key=lambda item: tuple(str(item.get(field, "")) for field in key_fields))


def _global_root(repo_root: Path) -> Path:
    return repo_root / "artifacts" / "global_memory"


def update_global_memory(repo_root: Path, *, project_dir: Path, problem_id: str) -> dict[str, str]:
    global_root = _global_root(repo_root)
    state = read_json(project_dir / "state.json", {})
    claims = [
        {**claim, "problem_id": problem_id, "project_dir": str(project_dir)}
        for claim in load_claim_ledger(project_dir).get("claims", [])
    ]
    routes = [
        {**route, "problem_id": problem_id, "project_dir": str(project_dir)}
        for route in load_route_ledger(project_dir).get("routes", [])
    ]
    failed = [
        {**failed_route, "problem_id": problem_id, "project_dir": str(project_dir)}
        for failed_route in load_failed_routes(project_dir).get("failed_routes", [])
    ]
    verified_declarations = [
        {**declaration, "problem_id": problem_id, "project_dir": str(project_dir)}
        for declaration in load_verified_declarations(project_dir).get("declarations", [])
    ]
    now = utc_now_iso()
    existing_problem_index = read_json(
        global_root / "problem_index.json",
        {"schema_version": "amra.problem_index.v1", "updated_at": None, "problems": []},
    )
    existing_claim_index = read_json(
        global_root / "claim_index.json",
        {"schema_version": "amra.claim_index.v1", "updated_at": None, "claims": []},
    )
    existing_failed_route_index = read_json(
        global_root / "failed_route_index.json",
        {"schema_version": "amra.failed_route_index.v1", "updated_at": None, "failed_routes": []},
    )
    existing_theorem_asset_index = read_json(
        global_root / "theorem_asset_index.json",
        {
            "schema_version": "amra.theorem_asset_index.v1",
            "updated_at": None,
            "routes": [],
            "verified_claims": [],
            "verified_declarations": [],
        },
    )
    problem_record = {
        "problem_id": problem_id,
        "project_dir": str(project_dir),
        "state": state.get("state", "unseen"),
        "updated_at": state.get("updated_at"),
        "claim_count": len(claims),
        "route_count": len(routes),
        "failed_route_count": len(failed),
        "verified_declaration_count": len(verified_declarations),
    }
    write_json(
        global_root / "problem_index.json",
        {
            "schema_version": "amra.problem_index.v1",
            "updated_at": now,
            "problems": _merge_index_items(
                list(existing_problem_index.get("problems", [])),
                [problem_record],
                ("problem_id",),
            ),
        },
    )
    write_json(
        global_root / "claim_index.json",
        {
            "schema_version": "amra.claim_index.v1",
            "updated_at": now,
            "claims": _merge_index_items(list(existing_claim_index.get("claims", [])), claims, ("problem_id", "claim_id")),
        },
    )
    write_json(
        global_root / "failed_route_index.json",
        {
            "schema_version": "amra.failed_route_index.v1",
            "updated_at": now,
            "failed_routes": _merge_index_items(
                list(existing_failed_route_index.get("failed_routes", [])),
                failed,
                ("problem_id", "fingerprint"),
            ),
        },
    )
    verified_claims = [claim for claim in claims if claim.get("status") == "lean_verified"]
    write_json(
        global_root / "theorem_asset_index.json",
        {
            "schema_version": "amra.theorem_asset_index.v1",
            "updated_at": now,
            "routes": _merge_index_items(
                list(existing_theorem_asset_index.get("routes", [])),
                routes,
                ("problem_id", "route_id"),
            ),
            "verified_claims": _merge_index_items(
                list(existing_theorem_asset_index.get("verified_claims", [])),
                verified_claims,
                ("problem_id", "claim_id"),
            ),
            "verified_declarations": _merge_index_items(
                list(existing_theorem_asset_index.get("verified_declarations", [])),
                verified_declarations,
                ("problem_id", "full_name"),
            ),
        },
    )
    append_jsonl(
        global_root / "difficulty_history.jsonl",
        {
            "problem_id": problem_id,
            "project_dir": str(project_dir),
            "state": state.get("state", "unseen"),
            "claim_count": len(claims),
            "route_count": len(routes),
            "failed_route_count": len(failed),
            "verified_declaration_count": len(verified_declarations),
            "recorded_at": now,
        },
    )
    return {
        "problem_index": str(global_root / "problem_index.json"),
        "claim_index": str(global_root / "claim_index.json"),
        "failed_route_index": str(global_root / "failed_route_index.json"),
        "theorem_asset_index": str(global_root / "theorem_asset_index.json"),
        "difficulty_history": str(global_root / "difficulty_history.jsonl"),
    }


def _format_evidence(evidence: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for item in evidence:
        label = str(item.get("type") or "evidence")
        path = str(item.get("path") or item.get("source") or "").strip()
        parts.append(f"{label}: {path}" if path else label)
    return "; ".join(parts) if parts else "none"


def render_resume_pack(project_dir: Path, *, problem_id: str | None = None) -> str:
    resolved_problem_id = _problem_id_for_project(project_dir, problem_id)
    state = read_json(project_dir / "state.json", {"state": "unseen", "reason": ""})
    claims = sorted(load_claim_ledger(project_dir).get("claims", []), key=lambda item: str(item.get("claim_id", "")))
    routes = sorted(load_route_ledger(project_dir).get("routes", []), key=lambda item: str(item.get("route_id", "")))
    failed_routes = sorted(
        load_failed_routes(project_dir).get("failed_routes", []),
        key=lambda item: (str(item.get("route_id", "")), str(item.get("fingerprint", ""))),
    )
    lines = [
        "# AMRA Resume Pack",
        "",
        "## Problem State",
        "",
        f"- Problem: `{resolved_problem_id}`",
        f"- State: `{state.get('state', 'unseen')}`",
        f"- Current reason: {state.get('reason') or 'none'}",
        "",
        "## Claims",
        "",
    ]
    if not claims:
        lines.append("- None.")
    for claim in claims:
        dependencies = _string_list(claim.get("dependencies"))
        lines.append(
            f"- `{claim.get('claim_id')}` status=`{claim.get('status', 'hypothesis')}` reusable={'yes' if claim.get('reusable') else 'no'}"
        )
        if claim.get("statement_nl"):
            lines.append(f"  - Statement: {claim['statement_nl']}")
        lines.append(f"  - Dependencies: {', '.join(dependencies) if dependencies else 'none'}")
        lines.append(f"  - Evidence: {_format_evidence(_normalize_evidence(claim.get('evidence')))}")
    lines.extend(["", "## Routes", ""])
    if not routes:
        lines.append("- None.")
    for route in routes:
        verdict = route.get("evaluator_verdict") or {}
        verdict_text = json.dumps(verdict, ensure_ascii=False, sort_keys=True) if verdict else "none"
        attempts = _dict_list(route.get("attempt_history"))
        lines.append(
            f"- `{route.get('route_id')}` status=`{route.get('status', 'new')}` target=`{route.get('target_claim') or 'none'}`"
        )
        if route.get("core_idea"):
            lines.append(f"  - Core idea: {route['core_idea']}")
        lines.append(f"  - Blocker: {route.get('blocker') or 'none'}")
        lines.append(f"  - Attempt count: {len(attempts)}")
        lines.append(f"  - Evaluator verdict: {verdict_text}")
    lines.extend(["", "## Failed Routes", ""])
    if not failed_routes:
        lines.append("- None.")
    for failed_route in failed_routes:
        resume_condition = failed_route.get("resume_condition") or "no resume condition recorded"
        lines.append(
            f"- `{failed_route.get('route_id')}` failure_mode=`{failed_route.get('failure_mode')}` fingerprint=`{failed_route.get('fingerprint')}`"
        )
        if failed_route.get("failed_assertion"):
            lines.append(f"  - Failed assertion: {failed_route['failed_assertion']}")
        if failed_route.get("approach") or failed_route.get("summary"):
            lines.append(f"  - Approach: {failed_route.get('approach') or failed_route.get('summary')}")
        lines.append(f"  - Failure class: {failed_route.get('failure_class') or 'unknown'}")
        lines.append(f"  - Evidence: {', '.join(_string_list(failed_route.get('evidence_paths'))) or 'none'}")
        lines.append(f"  - Resume only if: {resume_condition}")
        lines.append("  - Do not repeat this route unless the resume condition is met.")
    return "\n".join(lines) + "\n"


def write_resume_pack(project_dir: Path, *, problem_id: str | None = None) -> dict[str, Any]:
    project_dir.mkdir(parents=True, exist_ok=True)
    content = render_resume_pack(project_dir, problem_id=problem_id)
    path = resume_pack_path(project_dir)
    path.write_text(content, encoding="utf-8")
    return {
        "schema_version": "amra.resume_pack.v1",
        "problem_id": _problem_id_for_project(project_dir, problem_id),
        "path": str(path),
        "bytes": len(content.encode("utf-8")),
    }
