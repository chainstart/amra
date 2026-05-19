from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SOURCE_QUALITY_SCHEMA_VERSION = "amra.source_quality.v1"
SOURCE_QUALITY_TRUSTED_THRESHOLD = 7.0
SOURCE_QUALITY_USABLE_THRESHOLD = 5.0
SOURCE_QUALITY_RECOVERY_THRESHOLD = 4.0

PLACEHOLDER_STATEMENT_MARKERS = (
    "placeholder",
    "detailed statement should be imported",
    "statement should be imported",
    "authoritative source before claiming proof progress",
    "todo",
    "tbd",
)
LOCAL_SOURCE_TYPES = {"local_path", "local_pdf", "local_directory", "local_text", "local_markdown"}
REMOTE_SOURCE_TYPES = {"remote_url", "remote_html", "remote_text", "remote_pdf"}
CURATED_KINDS = {
    "curated_snapshot",
    "erdos_doc",
    "local_readme_path",
    "local_project_dir",
    "project_paper",
    "local_asset",
    "reference_snapshot",
}
ACADEMIC_HOST_HINTS = (
    "arxiv.org",
    "doi.org",
    "ams.org",
    "cambridge.org",
    "eudml.org",
    "euclid.org",
    "projecteuclid.org",
    "jstor.org",
    "springer.com",
    "link.springer.com",
    "sciencedirect.com",
    "hal.science",
    "zenodo.org",
)


def _clamp(value: float, lower: float = 0.0, upper: float = 10.0) -> float:
    return max(lower, min(upper, value))


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = str(value).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return sorted(value, key=str)
    return [value]


def _string_list(value: Any) -> list[str]:
    return _dedupe([str(item).strip() for item in _as_list(value) if str(item).strip()])


def _is_placeholder_statement(statement: str) -> bool:
    lowered = statement.strip().lower()
    return not lowered or any(marker in lowered for marker in PLACEHOLDER_STATEMENT_MARKERS)


def _looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _looks_like_local_path(value: str) -> bool:
    if not value or _looks_like_url(value):
        return False
    path = Path(value)
    return path.is_absolute() or "/" in value or "\\" in value or bool(path.suffix)


def _academic_url(value: str) -> bool:
    if not _looks_like_url(value):
        return False
    host = urlparse(value).netloc.lower()
    return any(hint in host for hint in ACADEMIC_HOST_HINTS)


def _tier(score: float) -> str:
    if score >= SOURCE_QUALITY_TRUSTED_THRESHOLD:
        return "trusted"
    if score >= SOURCE_QUALITY_USABLE_THRESHOLD:
        return "usable"
    if score >= SOURCE_QUALITY_RECOVERY_THRESHOLD:
        return "weak"
    return "source_debt"


def _source_type_for(source: str, explicit_source_type: str = "") -> str:
    if explicit_source_type:
        return explicit_source_type
    if _looks_like_url(source):
        return "remote_url"
    if _looks_like_local_path(source):
        return "local_path"
    if source:
        return "declared_source"
    return "unknown"


def score_source_record(record: dict[str, Any], *, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Score one source locator without fetching network data.

    The score intentionally favors durable local snapshots and explicit
    provenance fields. Remote URLs can still be usable references, but they do
    not score as trusted unless the project also materialized a local snapshot.
    """

    metadata = metadata or {}
    source = str(record.get("source") or record.get("path") or record.get("local_path") or record.get("source_url") or "").strip()
    kind = str(record.get("kind") or record.get("provider") or "reference").strip()
    status = str(record.get("status") or "").strip()
    source_type = _source_type_for(source, str(record.get("source_type") or "").strip())
    cache_path = str(record.get("cache_path") or record.get("local_path") or "").strip()
    title = str(record.get("title") or "").strip()
    candidate_count = len(_as_list(record.get("candidate_statements")))
    evidence_count = len(_as_list(record.get("evidence_items")))
    theorem_count = int(record.get("theorem_snippet_count") or len(_as_list(record.get("theorem_snippets"))))
    score = 1.5
    trust_reasons: list[str] = []
    source_debt: list[str] = []

    if source:
        score += 1.0
        trust_reasons.append("explicit_source_locator")
    else:
        source_debt.append("missing_source_locator")

    local_snapshot = source_type in LOCAL_SOURCE_TYPES or bool(cache_path)
    live_remote = source_type in REMOTE_SOURCE_TYPES or _looks_like_url(source)
    if local_snapshot:
        score += 2.3
        trust_reasons.append("local_snapshot_available")
    elif live_remote:
        score += 0.4
        trust_reasons.append("remote_locator_recorded")
        source_debt.append("remote_source_without_local_snapshot")

    if kind in CURATED_KINDS or kind.startswith("companion_"):
        score += 1.2
        trust_reasons.append("curated_source_kind")
    elif kind in {"problem_manifest", "reference", "source_audit_round"}:
        score += 0.5

    if status in {"ok", "existing_local_copy", "downloaded_pdf", "saved_landing_snapshot", "declared"}:
        score += 0.8
        trust_reasons.append("source_status_available")
    elif status in {"missing", "fetch_error", "skipped_network_disabled", "local_pdf_without_text", "empty"}:
        score -= 1.0
        source_debt.append(f"source_status_{status}")

    source_catalog = str(metadata.get("source_catalog") or "").strip().lower()
    provenance = str(metadata.get("provenance") or metadata.get("statement_provenance") or "").strip()
    statement_quality = str(metadata.get("statement_quality") or "").strip().lower()
    if source_catalog in {"erdosproblems", "curated", "local_snapshot", "benchmark"}:
        score += 0.8
        trust_reasons.append(f"curated_catalog:{source_catalog}")
    if provenance:
        score += 0.7
        trust_reasons.append("explicit_provenance_metadata")
    if statement_quality in {"exact", "curated", "verified"}:
        score += 0.5
        trust_reasons.append(f"statement_quality:{statement_quality}")
    elif statement_quality in {"placeholder", "unknown", "needs_source"}:
        score -= 0.8
        source_debt.append(f"statement_quality_{statement_quality}")

    if _academic_url(source):
        score += 0.5
        trust_reasons.append("academic_locator")
    if cache_path and _looks_like_local_path(cache_path):
        score += 0.7
        trust_reasons.append("cached_text_snapshot")
    if candidate_count:
        score += min(0.8, candidate_count * 0.16)
        trust_reasons.append("statement_candidates_extracted")
    if evidence_count:
        score += min(0.7, evidence_count * 0.12)
        trust_reasons.append("evidence_items_extracted")
    if theorem_count:
        score += min(0.9, theorem_count * 0.2)
        trust_reasons.append("theorem_snippets_extracted")
    if not title and not source:
        source_debt.append("missing_source_title")

    score = round(_clamp(score), 2)
    return {
        "schema_version": SOURCE_QUALITY_SCHEMA_VERSION,
        "score": score,
        "tier": _tier(score),
        "source": source,
        "kind": kind,
        "source_type": source_type,
        "status": status,
        "local_snapshot": local_snapshot,
        "live_remote": live_remote,
        "explicit_provenance": bool(source or provenance),
        "trust_reasons": _dedupe(trust_reasons),
        "source_debt": _dedupe(source_debt),
    }


def _manifest_source_records(
    *,
    source: str,
    references: list[str],
    metadata: dict[str, Any],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if source:
        records.append({"source": source, "kind": "problem_manifest", "status": "declared"})
    for reference in references:
        records.append({"source": reference, "kind": "reference", "status": "declared"})
    for key in ("local_readme_path", "local_project_dir", "curated_snapshot_path", "snapshot_path"):
        value = str(metadata.get(key, "")).strip()
        if value:
            records.append({"source": value, "kind": key, "status": "declared", "source_type": "local_path"})
    return records


def build_source_quality_audit(
    *,
    problem_id: str,
    statement: str = "",
    statement_source: str = "",
    source: str = "",
    references: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    snapshots: list[dict[str, Any]] | None = None,
    skipped_sources: list[dict[str, Any]] | None = None,
    recovery: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = metadata or {}
    references = _string_list(references)
    snapshots = [dict(item) for item in snapshots or [] if isinstance(item, dict)]
    skipped_sources = [dict(item) for item in skipped_sources or [] if isinstance(item, dict)]
    recovery = dict(recovery or {})
    exact_statement = not _is_placeholder_statement(statement)
    effective_statement_source = (
        str(statement_source).strip()
        or str(recovery.get("source") or "").strip()
        or str(metadata.get("statement_source") or metadata.get("statement_provenance") or "").strip()
        or str(source).strip()
    )

    scored_sources: list[dict[str, Any]] = []
    for record in _manifest_source_records(source=source, references=references, metadata=metadata):
        scored_sources.append(score_source_record(record, metadata=metadata))
    for snapshot in snapshots:
        quality = snapshot.get("source_quality")
        if isinstance(quality, dict) and quality.get("schema_version") == SOURCE_QUALITY_SCHEMA_VERSION:
            scored_sources.append(dict(quality))
        else:
            scored_sources.append(score_source_record(snapshot, metadata=metadata))
    scored_skipped = [score_source_record(item, metadata=metadata) for item in skipped_sources]

    scored_sources = sorted(
        scored_sources,
        key=lambda item: (-float(item.get("score", 0.0)), str(item.get("source", ""))),
    )
    best_score = float(scored_sources[0]["score"]) if scored_sources else 0.0
    statement_score = 0.0
    trust_reasons: list[str] = []
    source_debt: list[str] = []

    if exact_statement:
        statement_score += 1.1
        trust_reasons.append("exact_statement_present")
    else:
        source_debt.append("missing_exact_statement")
    if effective_statement_source:
        statement_score += 0.8
        trust_reasons.append("statement_provenance_recorded")
    else:
        source_debt.append("missing_statement_provenance")
    if references:
        statement_score += min(0.7, len(references) * 0.18)
        trust_reasons.append("manifest_references_recorded")
    if any(item.get("local_snapshot") for item in scored_sources):
        statement_score += 0.6
        trust_reasons.append("local_snapshot_supports_statement")
    if any(item.get("tier") == "trusted" for item in scored_sources):
        statement_score += 0.4
        trust_reasons.append("trusted_source_available")

    for item in scored_sources:
        source_debt.extend(_string_list(item.get("source_debt")))
        trust_reasons.extend(_string_list(item.get("trust_reasons")))
    if not scored_sources:
        source_debt.append("missing_source_inventory")

    score = round(_clamp(best_score + statement_score), 2)
    top_sources = [
        {
            "source": item.get("source", ""),
            "kind": item.get("kind", ""),
            "source_type": item.get("source_type", ""),
            "score": item.get("score", 0.0),
            "tier": item.get("tier", "source_debt"),
            "trust_reasons": _string_list(item.get("trust_reasons"))[:6],
            "source_debt": _string_list(item.get("source_debt"))[:6],
        }
        for item in scored_sources[:8]
    ]
    return {
        "schema_version": SOURCE_QUALITY_SCHEMA_VERSION,
        "problem_id": str(problem_id),
        "score": score,
        "tier": _tier(score),
        "trusted_source_count": sum(1 for item in scored_sources if item.get("tier") == "trusted"),
        "usable_source_count": sum(1 for item in scored_sources if item.get("tier") in {"trusted", "usable"}),
        "source_count": len(scored_sources),
        "skipped_source_count": len(scored_skipped),
        "local_snapshot_count": sum(1 for item in scored_sources if item.get("local_snapshot")),
        "remote_without_snapshot_count": sum(
            1 for item in scored_sources if "remote_source_without_local_snapshot" in _string_list(item.get("source_debt"))
        ),
        "statement_provenance": {
            "has_exact_statement": exact_statement,
            "source": effective_statement_source,
            "recovery_status": str(recovery.get("status") or ""),
            "recovered_statement": str(recovery.get("statement") or "").strip(),
            "candidate_score": recovery.get("score", 0),
        },
        "trust_reasons": _dedupe(trust_reasons)[:12],
        "source_debt": _dedupe(source_debt)[:12],
        "top_sources": top_sources,
        "skipped_sources": [
            {
                "source": item.get("source", ""),
                "status": item.get("status", ""),
                "score": item.get("score", 0.0),
                "tier": item.get("tier", "source_debt"),
                "source_debt": _string_list(item.get("source_debt"))[:6],
            }
            for item in scored_skipped[:8]
        ],
    }


def source_quality_for_problem_record(problem: Any) -> dict[str, Any]:
    metadata = getattr(problem, "metadata", {}) or {}
    return build_source_quality_audit(
        problem_id=str(getattr(problem, "problem_id", "")),
        statement=str(getattr(problem, "statement", "")),
        source=str(getattr(problem, "source", "")),
        references=_string_list(getattr(problem, "references", [])),
        metadata=metadata if isinstance(metadata, dict) else {},
    )


__all__ = [
    "SOURCE_QUALITY_SCHEMA_VERSION",
    "SOURCE_QUALITY_TRUSTED_THRESHOLD",
    "SOURCE_QUALITY_USABLE_THRESHOLD",
    "SOURCE_QUALITY_RECOVERY_THRESHOLD",
    "build_source_quality_audit",
    "score_source_record",
    "source_quality_for_problem_record",
]
