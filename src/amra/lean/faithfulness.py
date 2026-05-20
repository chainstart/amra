from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from amra.lean.contract import compare_lean_declaration_headers


FAITHFULNESS_REPORT_SCHEMA_VERSION = "amra.nl_lean_faithfulness.report.v1"
FAITHFULNESS_CHECK_SCHEMA_VERSION = "amra.nl_lean_faithfulness.check.v1"
FAITHFULNESS_BLOCKER_SCHEMA_VERSION = "amra.nl_lean_faithfulness.blocked_evidence.v1"

VERIFIED_DECLARATION_STATUSES = {"lean_verified", "verified", "passed", "trusted"}

MISMATCH_TAXONOMY = {
    "faithfully_modeled",
    "informal_only",
    "blocked_formalization_gap",
    "lean_statement_mismatch",
    "missing_formal_statement",
    "missing_lean_declaration",
    "missing_natural_language_obligation",
    "ambiguous_lean_declaration",
    "budget_guarded",
    "proof_search_unresolved",
    "unsupported_bundle",
}


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _text_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [
        line.strip().lstrip("-").strip()
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def _check(
    *,
    check_id: str,
    kind: str,
    status: str,
    taxonomy: str,
    severity: str,
    message: str,
    **extra: Any,
) -> dict[str, Any]:
    payload = {
        "schema_version": FAITHFULNESS_CHECK_SCHEMA_VERSION,
        "check_id": check_id,
        "kind": kind,
        "status": status,
        "taxonomy": taxonomy if taxonomy in MISMATCH_TAXONOMY else "unsupported_bundle",
        "severity": severity,
        "message": message,
    }
    payload.update({key: value for key, value in extra.items() if value not in (None, "", [], {})})
    return payload


def _blocked_evidence(
    *,
    evidence_id: str,
    source: str,
    taxonomy: str,
    message: str,
    **extra: Any,
) -> dict[str, Any]:
    payload = {
        "schema_version": FAITHFULNESS_BLOCKER_SCHEMA_VERSION,
        "evidence_id": evidence_id,
        "source": source,
        "taxonomy": taxonomy if taxonomy in MISMATCH_TAXONOMY else "blocked_formalization_gap",
        "message": message,
    }
    payload.update({key: value for key, value in extra.items() if value not in (None, "", [], {})})
    return payload


def _formal_statements(metadata: Mapping[str, Any], sketches_payload: Mapping[str, Any]) -> list[dict[str, str]]:
    statements: list[dict[str, str]] = []
    problem_yaml = metadata.get("problem_yaml") if isinstance(metadata.get("problem_yaml"), Mapping) else {}
    direct = str(metadata.get("formal_statement") or problem_yaml.get("formal_statement") or "").strip()
    nested = problem_yaml.get("metadata") if isinstance(problem_yaml.get("metadata"), Mapping) else {}
    nested_statement = str(nested.get("formal_statement") or "").strip()
    for source, statement in (
        ("problem_metadata.formal_statement", direct),
        ("problem_metadata.problem_yaml.metadata.formal_statement", nested_statement),
    ):
        if statement and statement not in {item["statement"] for item in statements}:
            statements.append({"source": source, "statement": statement})
    sketches = sketches_payload.get("sketches") if isinstance(sketches_payload.get("sketches"), list) else []
    for index, sketch in enumerate(sketches):
        if not isinstance(sketch, Mapping):
            continue
        statement = str(sketch.get("formal_statement") or sketch.get("lean_statement") or "").strip()
        if statement and statement not in {item["statement"] for item in statements}:
            statements.append({"source": f"natural_language_proof_sketches[{index}]", "statement": statement})
    return statements


def _natural_language_obligations(metadata: Mapping[str, Any], sketches_payload: Mapping[str, Any]) -> list[dict[str, str]]:
    obligations: list[dict[str, str]] = []
    statement = str(metadata.get("statement") or "").strip()
    if statement:
        obligations.append({"source": "problem_metadata.statement", "statement": statement})
    sketches = sketches_payload.get("sketches") if isinstance(sketches_payload.get("sketches"), list) else []
    for index, sketch in enumerate(sketches):
        if not isinstance(sketch, Mapping):
            continue
        summary = str(sketch.get("summary") or "").strip()
        if not summary:
            continue
        source = str(sketch.get("path") or sketch.get("claim_id") or f"sketch-{index + 1}")
        obligations.append({"source": source, "statement": summary})
    return obligations


def _verified_declarations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    declarations = payload.get("declarations") if isinstance(payload.get("declarations"), list) else []
    verified: list[dict[str, Any]] = []
    for declaration in declarations:
        if not isinstance(declaration, Mapping):
            continue
        status = str(declaration.get("status") or "lean_verified").strip().lower()
        if status not in VERIFIED_DECLARATION_STATUSES:
            continue
        name = str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or "").strip()
        if not name:
            continue
        verified.append({**dict(declaration), "full_name": name})
    return verified


def _build_status(build_report: Mapping[str, Any]) -> str:
    best_audit = build_report.get("best_audit") if isinstance(build_report.get("best_audit"), Mapping) else {}
    return str(best_audit.get("build_status") or build_report.get("status") or "").strip().lower()


def _result_bundle_checks(bundle_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    metadata = _read_json(bundle_dir / "problem_metadata.json", {})
    if not isinstance(metadata, Mapping):
        metadata = {}
    sketches_payload = _read_json(bundle_dir / "natural_language_proof_sketches.json", {})
    if not isinstance(sketches_payload, Mapping):
        sketches_payload = {}
    declarations_payload = _read_json(bundle_dir / "verified_declarations.json", {})
    if not isinstance(declarations_payload, Mapping):
        declarations_payload = {}
    build_report = _read_json(bundle_dir / "lean_build_report.json", {})
    if not isinstance(build_report, Mapping):
        build_report = {}

    obligations = _natural_language_obligations(metadata, sketches_payload)
    formal_statements = _formal_statements(metadata, sketches_payload)
    declarations = _verified_declarations(declarations_payload)
    checks: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    if not obligations and declarations:
        checks.append(
            _check(
                check_id="missing-natural-language-obligation",
                kind="nl_obligation_presence",
                status="warning",
                taxonomy="missing_natural_language_obligation",
                severity="warning",
                message="Lean declarations are present, but no natural-language theorem obligation was exported.",
                lean_declarations=[item["full_name"] for item in declarations],
            )
        )
    if obligations and not formal_statements:
        checks.append(
            _check(
                check_id="missing-formal-statement",
                kind="nl_to_formal_statement",
                status="warning",
                taxonomy="missing_formal_statement",
                severity="warning",
                message="Natural-language obligations exist, but no exact Lean formal statement was recorded for comparison.",
                natural_language_obligation_count=len(obligations),
                lean_declaration_count=len(declarations),
            )
        )
        if not declarations:
            checks.append(
                _check(
                    check_id="informal-only",
                    kind="nl_to_lean_declaration",
                    status="informal_only",
                    taxonomy="informal_only",
                    severity="info",
                    message="The bundle contains natural-language proof evidence but no Lean-verified declaration.",
                    natural_language_obligation_count=len(obligations),
                )
            )

    for index, formal in enumerate(formal_statements, start=1):
        expected = formal["statement"]
        source = formal["source"]
        if not declarations:
            check_id = f"formal-statement-{index}-missing-lean"
            checks.append(
                _check(
                    check_id=check_id,
                    kind="formal_statement_to_verified_declaration",
                    status="blocked_formalization_gap",
                    taxonomy="missing_lean_declaration",
                    severity="info",
                    message="An exact Lean formal statement was recorded, but no Lean-verified declaration is available.",
                    expected_formal_statement=expected,
                    formal_statement_source=source,
                )
            )
            blocked.append(
                _blocked_evidence(
                    evidence_id=check_id,
                    source="verified_declarations.json",
                    taxonomy="blocked_formalization_gap",
                    message="No Lean-verified declaration is available for the recorded formal statement.",
                    expected_formal_statement=expected,
                )
            )
            continue

        comparisons: list[dict[str, Any]] = []
        for declaration in declarations:
            actual = str(declaration.get("statement") or declaration.get("header") or "").strip()
            if not actual:
                comparisons.append(
                    {
                        "declaration": declaration["full_name"],
                        "matched": False,
                        "missing_statement": True,
                    }
                )
                continue
            comparison = compare_lean_declaration_headers(
                actual_header=actual,
                expected_header=expected,
                target_theorem=str(declaration.get("name") or declaration.get("lean_name") or declaration["full_name"]),
            )
            comparisons.append(
                {
                    "declaration": declaration["full_name"],
                    "matched": bool(comparison.get("matched")),
                    "expected_normalized": comparison.get("expected_normalized", ""),
                    "actual_normalized": comparison.get("actual_normalized", ""),
                }
            )
        matches = [comparison for comparison in comparisons if comparison.get("matched")]
        if len(matches) == 1:
            checks.append(
                _check(
                    check_id=f"formal-statement-{index}-matched",
                    kind="formal_statement_to_verified_declaration",
                    status="faithfully_modeled",
                    taxonomy="faithfully_modeled",
                    severity="info",
                    message="The recorded Lean formal statement matches one Lean-verified declaration.",
                    formal_statement_source=source,
                    expected_formal_statement=expected,
                    lean_declaration=matches[0]["declaration"],
                    expected_normalized=matches[0].get("expected_normalized", ""),
                    actual_normalized=matches[0].get("actual_normalized", ""),
                )
            )
        elif len(matches) > 1:
            checks.append(
                _check(
                    check_id=f"formal-statement-{index}-ambiguous",
                    kind="formal_statement_to_verified_declaration",
                    status="warning",
                    taxonomy="ambiguous_lean_declaration",
                    severity="warning",
                    message="The recorded formal statement matches multiple Lean-verified declarations.",
                    matching_declarations=[item["declaration"] for item in matches],
                    expected_formal_statement=expected,
                )
            )
        else:
            checks.append(
                _check(
                    check_id=f"formal-statement-{index}-mismatch",
                    kind="formal_statement_to_verified_declaration",
                    status="model_mismatch",
                    taxonomy="lean_statement_mismatch",
                    severity="error",
                    message="No Lean-verified declaration matches the recorded formal statement.",
                    formal_statement_source=source,
                    expected_formal_statement=expected,
                    comparisons=comparisons,
                )
            )

    build_status = _build_status(build_report)
    if build_status and build_status not in {"passed", "verified", "success"}:
        diagnostics = build_report.get("diagnostics") if isinstance(build_report.get("diagnostics"), list) else []
        blocked.append(
            _blocked_evidence(
                evidence_id="lean-build-status",
                source="lean_build_report.json",
                taxonomy="blocked_formalization_gap",
                message=f"Lean build status is `{build_status}`.",
                diagnostics=[str(item) for item in diagnostics[:20]],
            )
        )
    for index, line in enumerate(_text_lines(bundle_dir / "unresolved_blockers.md"), start=1):
        if line.lower() == "none recorded.":
            continue
        blocked.append(
            _blocked_evidence(
                evidence_id=f"unresolved-blocker-{index}",
                source="unresolved_blockers.md",
                taxonomy="blocked_formalization_gap",
                message=line,
            )
        )
    for index, record in enumerate(_read_jsonl(bundle_dir / "proof_attempt_ledger.jsonl"), start=1):
        status = str(record.get("status") or "").strip().lower()
        state = str(record.get("proof_loop_state") or "").strip().lower()
        if status == "blocked" or state == "blocked_formalization_gap":
            blocked.append(
                _blocked_evidence(
                    evidence_id=f"proof-attempt-ledger-{index}",
                    source="proof_attempt_ledger.jsonl",
                    taxonomy="blocked_formalization_gap",
                    message=str(record.get("summary") or "Formalization attempt is blocked."),
                    attempt_id=str(record.get("attempt_id") or ""),
                    blockers=record.get("blockers") if isinstance(record.get("blockers"), list) else [],
                )
            )

    context = {
        "problem_id": str(metadata.get("problem_id") or ""),
        "natural_language_obligation_count": len(obligations),
        "formal_statement_count": len(formal_statements),
        "lean_verified_declaration_count": len(declarations),
        "lean_build_status": build_status or "missing",
    }
    return checks, blocked, context


def _proof_stability_checks(bundle_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    report = _read_json(bundle_dir / "proof_stability_report.json", {})
    if not isinstance(report, Mapping):
        report = {}
    checks: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    cases = report.get("cases") if isinstance(report.get("cases"), list) else []
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, Mapping):
            continue
        case_id = str(case.get("case_id") or f"case-{index}")
        taxon = str(case.get("failure_taxon") or "unknown").strip()
        canonical_status = str(case.get("canonical_status") or "").strip()
        proof_result = case.get("proof_loop_result") if isinstance(case.get("proof_loop_result"), Mapping) else {}
        result_report = proof_result.get("report") if isinstance(proof_result.get("report"), Mapping) else proof_result
        proof_loop_state = str(result_report.get("proof_loop_state") or "").strip()
        if taxon == "budget_exhausted":
            taxonomy = "budget_guarded"
            status = "budget_guarded"
            message = "Deterministic budget controls stopped the case before unbounded proof search."
        elif taxon == "none" and proof_loop_state == "lean_verified_declaration":
            taxonomy = "faithfully_modeled"
            status = "faithfully_modeled"
            message = "Deterministic mixed proof case reached a Lean-verified declaration state."
        elif taxon == "none" and proof_loop_state == "informal_claim":
            taxonomy = "informal_only"
            status = "informal_only"
            message = "Deterministic natural-language case remained an informal proof obligation."
        elif taxon == "blocked_formalization_gap" or canonical_status == "blocked":
            taxonomy = "blocked_formalization_gap"
            status = "blocked_formalization_gap"
            message = "Deterministic case records blocked formalization evidence."
            diagnostics = result_report.get("diagnostics") if isinstance(result_report.get("diagnostics"), list) else []
            blocked.append(
                _blocked_evidence(
                    evidence_id=f"proof-stability-{case_id}",
                    source=f"cases/{case_id}/result.json",
                    taxonomy=taxonomy,
                    message=diagnostics[0] if diagnostics else message,
                    case_id=case_id,
                    diagnostics=[str(item) for item in diagnostics],
                )
            )
        else:
            taxonomy = "proof_search_unresolved"
            status = "warning"
            message = "Deterministic case did not provide a faithful Lean declaration or explicit formalization blocker."
        checks.append(
            _check(
                check_id=f"proof-stability-{case_id}",
                kind="proof_stability_case",
                status=status,
                taxonomy=taxonomy,
                severity="info" if taxonomy != "proof_search_unresolved" else "warning",
                message=message,
                case_id=case_id,
                case_kind=str(case.get("case_kind") or ""),
                route=str(case.get("route") or ""),
                canonical_status=canonical_status,
                failure_taxon=taxon,
                proof_loop_state=proof_loop_state,
            )
        )
    context = {
        "suite_id": str(report.get("suite_id") or ""),
        "proof_stability_status": str(report.get("status") or "missing"),
        "case_count": len(cases),
        "llm_calls": int(report.get("llm_calls") or 0),
        "live_model_calls": bool(report.get("live_model_calls")),
    }
    return checks, blocked, context


def _bundle_kind(bundle_dir: Path) -> str:
    if (bundle_dir / "proof_stability_report.json").is_file():
        return "proof_stability_report"
    if (bundle_dir / "problem_metadata.json").is_file() or (bundle_dir / "artifact_manifest.json").is_file():
        return "amra_result_bundle"
    return "unsupported"


def _taxonomy_counts(checks: list[Mapping[str, Any]], blocked: list[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in [*checks, *blocked]:
        taxonomy = str(item.get("taxonomy") or "unsupported_bundle")
        counts[taxonomy] = counts.get(taxonomy, 0) + 1
    return dict(sorted(counts.items()))


def _render_summary(report: Mapping[str, Any]) -> str:
    lines = [
        "# AMRA NL/Lean Faithfulness Audit",
        "",
        f"- Status: `{report['status']}`",
        f"- Bundle kind: `{report['bundle_kind']}`",
        f"- Checks: `{report['check_count']}`",
        f"- Blocked formalization evidence records: `{report['blocked_formalization_evidence_count']}`",
        "",
        "## Taxonomy Counts",
        "",
    ]
    for taxonomy, count in report["taxonomy_counts"].items():
        lines.append(f"- `{taxonomy}`: {count}")
    lines.append("")
    return "\n".join(lines)


def audit_faithfulness_bundle(
    *,
    bundle: Path,
    output_dir: Path | None = None,
    write_artifacts: bool = True,
) -> dict[str, Any]:
    """Audit whether exported Lean declarations faithfully model NL obligations."""

    bundle_dir = bundle.expanduser().resolve()
    kind = _bundle_kind(bundle_dir)
    if kind == "amra_result_bundle":
        checks, blocked, context = _result_bundle_checks(bundle_dir)
    elif kind == "proof_stability_report":
        checks, blocked, context = _proof_stability_checks(bundle_dir)
    else:
        checks = [
            _check(
                check_id="unsupported-bundle",
                kind="bundle_detection",
                status="unsupported",
                taxonomy="unsupported_bundle",
                severity="error",
                message="The input directory is neither an AMRA result bundle nor a proof-stability report directory.",
            )
        ]
        blocked = []
        context = {}

    error_count = sum(1 for check in checks if check.get("severity") == "error")
    status = "failed" if error_count else "passed"
    report = {
        "schema_version": FAITHFULNESS_REPORT_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "status": status,
        "bundle_kind": kind,
        "bundle_dir": str(bundle_dir),
        "mismatch_taxonomy": sorted(MISMATCH_TAXONOMY),
        "taxonomy_counts": _taxonomy_counts(checks, blocked),
        "check_count": len(checks),
        "error_count": error_count,
        "warning_count": sum(1 for check in checks if check.get("severity") == "warning"),
        "blocked_formalization_evidence_count": len(blocked),
        "checks": checks,
        "blocked_formalization_evidence": blocked,
        "context": context,
    }
    if output_dir is not None and write_artifacts:
        output_dir = output_dir.expanduser().resolve()
        _write_json(output_dir / "faithfulness_report.json", report)
        _write_json(
            output_dir / "blocked_formalization_evidence.json",
            {
                "schema_version": "amra.nl_lean_faithfulness.blocked_evidence_list.v1",
                "generated_at": report["generated_at"],
                "bundle_dir": str(bundle_dir),
                "blocked_formalization_evidence": blocked,
            },
        )
        (output_dir / "faithfulness_summary.md").write_text(_render_summary(report), encoding="utf-8")
        report = {
            **report,
            "report_path": str(output_dir / "faithfulness_report.json"),
            "blocked_formalization_evidence_path": str(output_dir / "blocked_formalization_evidence.json"),
            "summary_path": str(output_dir / "faithfulness_summary.md"),
        }
    return report


__all__ = [
    "FAITHFULNESS_BLOCKER_SCHEMA_VERSION",
    "FAITHFULNESS_CHECK_SCHEMA_VERSION",
    "FAITHFULNESS_REPORT_SCHEMA_VERSION",
    "MISMATCH_TAXONOMY",
    "audit_faithfulness_bundle",
]
