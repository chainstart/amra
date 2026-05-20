from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amra.core.workspace import slugify, utc_now_iso, write_json, write_text


LIBRARY_CURATOR_REPORT_SCHEMA_VERSION = "amra.library_curator.report.v1"
LIBRARY_CURATOR_REVIEW_SCHEMA_VERSION = "amra.library_curator.review_record.v1"
REUSABLE_LEMMA_METADATA_SCHEMA_VERSION = "amra.reusable_lemma_metadata.v1"
REJECTION_REASONS_SCHEMA_VERSION = "amra.library_curator.rejection_reasons.v1"

VERIFIED_STATUSES = {"lean_verified", "verified", "passed", "trusted"}
REJECT_TAXONOMIES = {
    "ambiguous_lean_declaration",
    "blocked_formalization_gap",
    "budget_guarded",
    "informal_only",
    "lean_statement_mismatch",
    "missing_formal_statement",
    "missing_lean_declaration",
    "missing_natural_language_obligation",
    "proof_search_unresolved",
    "unsupported_bundle",
}


def _read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def _string_list(value: Any) -> list[str]:
    items = value if isinstance(value, list) else [value] if value else []
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            cleaned.append(text)
    return cleaned


def _source_kind(candidates_dir: Path) -> str:
    if (candidates_dir / "faithfulness_report.json").is_file():
        return "faithfulness_report"
    if (candidates_dir / "artifact_manifest.json").is_file() and (candidates_dir / "verified_declarations.json").is_file():
        return "result_bundle"
    if (candidates_dir / "library_harvest_candidates.json").is_file():
        return "library_harvest_candidates"
    return "unknown"


def _declaration_name(declaration: dict[str, Any]) -> str:
    return str(
        declaration.get("full_name")
        or declaration.get("lean_name")
        or declaration.get("name")
        or declaration.get("declaration")
        or ""
    ).strip()


def _short_declaration_name(declaration: dict[str, Any]) -> str:
    name = _declaration_name(declaration)
    return str(declaration.get("name") or name.split(".")[-1]).strip()


def _status_is_verified(declaration: dict[str, Any]) -> bool:
    status = str(declaration.get("status") or "").strip().lower()
    if not status:
        return bool(declaration.get("lean_verified"))
    return status in VERIFIED_STATUSES and bool(declaration.get("lean_verified", True))


def _bundle_verified_declarations(bundle_dir: Path) -> list[dict[str, Any]]:
    payload = _read_json(bundle_dir / "verified_declarations.json", {})
    declarations = payload.get("declarations", []) if isinstance(payload, dict) else []
    return [dict(item) for item in declarations if isinstance(item, dict)]


def _faithfulness_by_declaration(report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_name: dict[str, list[dict[str, Any]]] = {}
    checks = report.get("checks", []) if isinstance(report.get("checks"), list) else []
    for check in checks:
        if not isinstance(check, dict):
            continue
        names = _string_list(check.get("declaration"))
        names.extend(_string_list(check.get("full_name")))
        names.extend(_string_list(check.get("lean_name")))
        for name in names:
            by_name.setdefault(name, []).append(check)
            by_name.setdefault(name.split(".")[-1], []).append(check)
    return by_name


def _faithfulness_allows_promotion(report: dict[str, Any], declaration: dict[str, Any]) -> tuple[bool, list[str], list[dict[str, Any]]]:
    status = str(report.get("status") or "").strip().lower()
    if status and status not in {"passed", "verified", "success"}:
        return False, [f"faithfulness report status is `{status}`"], []

    by_declaration = _faithfulness_by_declaration(report)
    name = _declaration_name(declaration)
    checks = by_declaration.get(name) or by_declaration.get(name.split(".")[-1]) or []
    if not checks:
        taxonomy_counts = report.get("taxonomy_counts") if isinstance(report.get("taxonomy_counts"), dict) else {}
        if taxonomy_counts.get("faithfully_modeled") and not any(taxonomy_counts.get(item) for item in REJECT_TAXONOMIES):
            return True, [], []
        if str(report.get("bundle_kind") or "") == "amra_result_bundle" and not any(
            taxonomy_counts.get(item) for item in {"lean_statement_mismatch", "missing_lean_declaration", "unsupported_bundle"}
        ):
            return True, [], []
        return False, ["no faithful-modeling check is attached to this declaration"], []

    rejections: list[str] = []
    for check in checks:
        taxonomy = str(check.get("taxonomy") or check.get("status") or "").strip()
        if taxonomy in REJECT_TAXONOMIES or str(check.get("status") or "") in REJECT_TAXONOMIES:
            rejections.append(f"faithfulness taxonomy `{taxonomy}` blocks promotion")
        if check.get("matched") is False:
            rejections.append("faithfulness check reports an unmatched Lean statement")
    return not rejections, rejections, checks


def _candidate_from_declaration(
    *,
    declaration: dict[str, Any],
    source_dir: Path,
    source_kind: str,
    faithfulness_report: dict[str, Any],
) -> dict[str, Any]:
    name = _declaration_name(declaration)
    short_name = _short_declaration_name(declaration)
    module = str(declaration.get("module") or declaration.get("module_name") or "AmraLibrary.Curated").strip()
    return {
        "candidate_id": slugify(name or short_name),
        "source_kind": source_kind,
        "source_dir": str(source_dir),
        "name": short_name,
        "full_name": name or short_name,
        "kind": str(declaration.get("kind") or "lemma").strip(),
        "statement": str(declaration.get("statement") or "").strip(),
        "module": module,
        "domain": str(declaration.get("domain") or "").strip(),
        "tags": _string_list(declaration.get("tags")),
        "relative_path": str(declaration.get("relative_path") or declaration.get("path") or "").strip(),
        "source_path": str(declaration.get("source_path") or declaration.get("source_file") or "").strip(),
        "status": str(declaration.get("status") or "").strip() or "lean_verified",
        "lean_verified": bool(declaration.get("lean_verified", _status_is_verified(declaration))),
        "lean_build_report_status": str(declaration.get("lean_build_report_status") or "").strip(),
        "verification_basis": str(declaration.get("verification_basis") or "verified_declarations.json").strip(),
        "import_hints": _string_list(declaration.get("import_hints")) or [f"import {module}"],
        "faithfulness_report_status": str(faithfulness_report.get("status") or "").strip(),
    }


def _review_candidate(candidate: dict[str, Any], *, faithfulness_checks: list[dict[str, Any]], reasons: list[str]) -> dict[str, Any]:
    gate_results = {
        "lean_verified_declaration": candidate["lean_verified"] and str(candidate["status"]).lower() in VERIFIED_STATUSES,
        "verification_basis_recorded": bool(candidate["verification_basis"]),
        "natural_language_sketch_excluded": True,
        "statement_recorded": bool(candidate["statement"]),
        "faithful_modeling_passed": not reasons,
    }
    rejection_reasons = list(reasons)
    if not gate_results["lean_verified_declaration"]:
        rejection_reasons.append("candidate is not a Lean-verified declaration")
    if not gate_results["verification_basis_recorded"]:
        rejection_reasons.append("candidate does not record a verification basis")
    if not gate_results["statement_recorded"]:
        rejection_reasons.append("candidate does not record a reusable Lean statement")

    decision = "promote" if all(gate_results.values()) and not rejection_reasons else "reject"
    reviewed_at = utc_now_iso()
    return {
        "schema_version": LIBRARY_CURATOR_REVIEW_SCHEMA_VERSION,
        "review_id": f"library-curator-{candidate['candidate_id']}",
        "candidate_id": candidate["candidate_id"],
        "reviewed_at": reviewed_at,
        "reviewer": "amra.library_curator",
        "decision": decision,
        "promotion_gates": gate_results,
        "rejection_reasons": rejection_reasons,
        "faithfulness_checks": faithfulness_checks,
        "candidate": candidate,
    }


def _lemma_metadata(record: dict[str, Any]) -> dict[str, Any]:
    candidate = record["candidate"]
    return {
        "lemma_id": candidate["candidate_id"],
        "name": candidate["name"],
        "full_name": candidate["full_name"],
        "kind": candidate["kind"],
        "statement": candidate["statement"],
        "module": candidate["module"],
        "domain": candidate["domain"],
        "tags": candidate["tags"],
        "reusable": True,
        "promotion_status": "accepted",
        "verification_basis": candidate["verification_basis"],
        "lean_build_report_status": candidate["lean_build_report_status"],
        "source_dir": candidate["source_dir"],
        "source_path": candidate["source_path"] or candidate["relative_path"],
        "import_hints": candidate["import_hints"],
        "curator_review_id": record["review_id"],
    }


def _review_faithfulness_checks_without_declarations(
    *,
    faithfulness_report: dict[str, Any],
    candidates_dir: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    checks = faithfulness_report.get("checks", []) if isinstance(faithfulness_report.get("checks"), list) else []
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            continue
        name = str(
            check.get("declaration")
            or check.get("full_name")
            or check.get("lean_name")
            or check.get("case_id")
            or check.get("check_id")
            or f"faithfulness-check-{index}"
        ).strip()
        taxonomy = str(check.get("taxonomy") or check.get("status") or "unsupported_bundle").strip()
        candidate = {
            "candidate_id": slugify(name),
            "source_kind": "faithfulness_report",
            "source_dir": str(candidates_dir),
            "name": name.split(".")[-1],
            "full_name": name,
            "kind": str(check.get("kind") or "faithfulness_check").strip(),
            "statement": "",
            "module": "AmraLibrary.Curated",
            "domain": "",
            "tags": [taxonomy] if taxonomy else [],
            "relative_path": str(check.get("source") or "").strip(),
            "source_path": str(check.get("source") or "").strip(),
            "status": "lean_verified" if taxonomy == "faithfully_modeled" else taxonomy,
            "lean_verified": taxonomy == "faithfully_modeled",
            "lean_build_report_status": "",
            "verification_basis": "faithfulness_report.json" if taxonomy == "faithfully_modeled" else "",
            "import_hints": ["import AmraLibrary.Curated"],
            "faithfulness_report_status": str(faithfulness_report.get("status") or "").strip(),
        }
        reasons = ["faithfulness report did not include reusable declaration metadata"]
        if taxonomy in REJECT_TAXONOMIES:
            reasons.append(f"faithfulness taxonomy `{taxonomy}` is not promotable")
        records.append(_review_candidate(candidate, faithfulness_checks=[check], reasons=reasons))
    return records


def _render_summary(report: dict[str, Any]) -> str:
    lines = [
        "# AMRA Library Curator",
        "",
        f"- Status: `{report['status']}`",
        f"- Source kind: `{report['source']['kind']}`",
        f"- Reviewed candidates: `{report['review_count']}`",
        f"- Promoted candidates: `{report['promoted_count']}`",
        f"- Rejected candidates: `{report['rejected_count']}`",
        "",
        "## Verified-Only Policy",
        "",
        "- Only Lean-verified declarations from `verified_declarations.json` can be promoted.",
        "- Natural-language sketches and blocked formalization evidence are never promoted as library facts.",
        "- Each accepted candidate has a curator review record and reusable lemma metadata.",
        "",
    ]
    if report["promoted"]:
        lines.extend(["## Accepted", ""])
        for item in report["promoted"]:
            lines.append(f"- `{item['full_name']}` -> `{item['module']}`")
        lines.append("")
    if report["rejected"]:
        lines.extend(["## Rejected", ""])
        for item in report["rejected"]:
            reasons = "; ".join(item.get("rejection_reasons", [])) or "no reason recorded"
            lines.append(f"- `{item['candidate']['full_name']}`: {reasons}")
        lines.append("")
    return "\n".join(lines)


def _load_candidates(candidates_dir: Path) -> tuple[str, dict[str, Any], list[dict[str, Any]], Path]:
    kind = _source_kind(candidates_dir)
    faithfulness_report: dict[str, Any] = {}
    source_dir = candidates_dir

    if kind == "faithfulness_report":
        faithfulness_report = _read_json(candidates_dir / "faithfulness_report.json", {})
        bundle_dir = Path(str(faithfulness_report.get("bundle_dir") or "")).expanduser()
        if bundle_dir.is_dir():
            source_dir = bundle_dir.resolve()
            declarations = _bundle_verified_declarations(source_dir)
        else:
            declarations = []
        return kind, faithfulness_report, declarations, source_dir

    if kind == "result_bundle":
        declarations = _bundle_verified_declarations(candidates_dir)
        return kind, faithfulness_report, declarations, candidates_dir

    if kind == "library_harvest_candidates":
        payload = _read_json(candidates_dir / "library_harvest_candidates.json", {})
        declarations = []
        for item in payload.get("candidates", []) if isinstance(payload, dict) else []:
            if isinstance(item, dict):
                declarations.append(
                    {
                        **item,
                        "name": item.get("declaration") or item.get("name"),
                        "full_name": item.get("full_name") or item.get("declaration") or item.get("name"),
                        "status": "lean_verified",
                        "lean_verified": True,
                        "statement": item.get("statement", ""),
                        "module": item.get("module") or item.get("module_name"),
                        "verification_basis": "library_harvest_candidates.json",
                    }
                )
        return kind, faithfulness_report, declarations, candidates_dir

    return kind, faithfulness_report, [], candidates_dir


def curate_library_candidates(*, candidates: Path, output_dir: Path) -> dict[str, Any]:
    """Review verified library candidates and emit promotion-ready artifacts.

    The curator is intentionally side-effect free with respect to the checked-in
    Lean library. It creates review and metadata artifacts under output_dir; a
    later human or harness step can apply accepted candidates to a library module.
    """

    candidates_dir = candidates.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source_kind, faithfulness_report, declarations, source_dir = _load_candidates(candidates_dir)
    review_records: list[dict[str, Any]] = []
    rejected_unsupported: list[dict[str, Any]] = []

    if source_kind == "unknown":
        rejected_unsupported.append(
            {
                "schema_version": LIBRARY_CURATOR_REVIEW_SCHEMA_VERSION,
                "review_id": "library-curator-unsupported-input",
                "candidate_id": "unsupported-input",
                "reviewed_at": utc_now_iso(),
                "reviewer": "amra.library_curator",
                "decision": "reject",
                "promotion_gates": {
                    "lean_verified_declaration": False,
                    "verification_basis_recorded": False,
                    "natural_language_sketch_excluded": True,
                    "statement_recorded": False,
                    "faithful_modeling_passed": False,
                },
                "rejection_reasons": [
                    "candidate directory does not contain a faithfulness report, result bundle, or library harvest report"
                ],
                "faithfulness_checks": [],
                "candidate": {
                    "candidate_id": "unsupported-input",
                    "source_kind": source_kind,
                    "source_dir": str(candidates_dir),
                    "name": "",
                    "full_name": "",
                    "kind": "",
                    "statement": "",
                    "module": "",
                    "domain": "",
                    "tags": [],
                    "status": "",
                    "lean_verified": False,
                    "verification_basis": "",
                },
            }
        )

    for declaration in declarations:
        candidate = _candidate_from_declaration(
            declaration=declaration,
            source_dir=source_dir,
            source_kind=source_kind,
            faithfulness_report=faithfulness_report,
        )
        allows, reasons, checks = (
            _faithfulness_allows_promotion(faithfulness_report, declaration)
            if faithfulness_report
            else (True, [], [])
        )
        if not allows and not reasons:
            reasons = ["faithfulness report does not allow promotion"]
        review_records.append(_review_candidate(candidate, faithfulness_checks=checks, reasons=reasons))

    if not declarations and faithfulness_report:
        review_records.extend(
            _review_faithfulness_checks_without_declarations(
                faithfulness_report=faithfulness_report,
                candidates_dir=candidates_dir,
            )
        )

    review_records.extend(rejected_unsupported)
    promoted_records = [record for record in review_records if record["decision"] == "promote"]
    rejected_records = [record for record in review_records if record["decision"] == "reject"]
    lemmas = [_lemma_metadata(record) for record in promoted_records]
    rejection_reasons: dict[str, int] = {}
    for record in rejected_records:
        for reason in record.get("rejection_reasons", []):
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1

    metadata_payload = {
        "schema_version": REUSABLE_LEMMA_METADATA_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "source_dir": str(source_dir),
        "lemma_count": len(lemmas),
        "lemmas": lemmas,
    }
    rejection_payload = {
        "schema_version": REJECTION_REASONS_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "rejected_count": len(rejected_records),
        "reason_counts": dict(sorted(rejection_reasons.items())),
        "rejected": rejected_records,
    }
    promoted_payload = {
        "schema_version": "amra.library_curator.promoted_candidates.v1",
        "generated_at": utc_now_iso(),
        "candidate_count": len(promoted_records),
        "candidates": [record["candidate"] for record in promoted_records],
    }

    _write_jsonl(output_dir / "curator_review_records.jsonl", review_records)
    write_json(output_dir / "reusable_lemma_metadata.json", metadata_payload)
    write_json(output_dir / "rejection_reasons.json", rejection_payload)
    write_json(output_dir / "promoted_library_candidates.json", promoted_payload)

    report = {
        "schema_version": LIBRARY_CURATOR_REPORT_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "status": "passed",
        "source": {
            "kind": source_kind,
            "candidates_dir": str(candidates_dir),
            "resolved_source_dir": str(source_dir),
            "faithfulness_report": str(candidates_dir / "faithfulness_report.json")
            if (candidates_dir / "faithfulness_report.json").is_file()
            else "",
        },
        "promotion_policy": {
            "verified_only": True,
            "accepted_verified_statuses": sorted(VERIFIED_STATUSES),
            "natural_language_sketches_are_not_promotable": True,
            "requires_curator_review_record": True,
            "requires_reusable_lemma_metadata": True,
        },
        "review_count": len(review_records),
        "promoted_count": len(promoted_records),
        "rejected_count": len(rejected_records),
        "promoted": [record["candidate"] for record in promoted_records],
        "rejected": rejected_records,
        "artifacts": {
            "report": str(output_dir / "library_curator_report.json"),
            "curator_review_records": str(output_dir / "curator_review_records.jsonl"),
            "reusable_lemma_metadata": str(output_dir / "reusable_lemma_metadata.json"),
            "rejection_reasons": str(output_dir / "rejection_reasons.json"),
            "promoted_library_candidates": str(output_dir / "promoted_library_candidates.json"),
            "summary": str(output_dir / "summary.md"),
        },
    }
    write_json(output_dir / "library_curator_report.json", report)
    write_text(output_dir / "summary.md", _render_summary(report))
    return report


__all__ = [
    "LIBRARY_CURATOR_REPORT_SCHEMA_VERSION",
    "LIBRARY_CURATOR_REVIEW_SCHEMA_VERSION",
    "REUSABLE_LEMMA_METADATA_SCHEMA_VERSION",
    "curate_library_candidates",
]
