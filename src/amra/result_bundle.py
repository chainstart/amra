from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from amra.portfolio_memory import (
    consolidate_project_memory,
    load_claim_ledger,
    load_failed_routes,
    load_route_ledger,
    load_verified_declarations,
    read_json,
    utc_now_iso,
    write_json,
)


RESULT_BUNDLE_SCHEMA_VERSION = "amra.result_bundle.v1"
RESULT_BUNDLE_MANIFEST_SCHEMA_VERSION = "amra.result_bundle_manifest.v1"
PROBLEM_METADATA_SCHEMA_VERSION = "amra.problem_metadata.v1"
PROOF_SKETCHES_SCHEMA_VERSION = "amra.natural_language_proof_sketches.v1"
LIMITATIONS_SCHEMA_VERSION = "amra.result_bundle_limitations.v1"
VERIFIED_DECLARATION_STATUSES = {"lean_verified", "verified", "passed", "trusted"}
NATURAL_LANGUAGE_TRUST_LEVEL = "natural_language_proof_sketch"

BUNDLE_FILE_KINDS = {
    "theorem_statement.md": "theorem_statement",
    "problem_metadata.json": "problem_metadata",
    "proof_summary.md": "proof_summary",
    "natural_language_proof_sketches.json": "natural_language_proof_sketches",
    "lean_build_report.json": "lean_build_report",
    "verified_declarations.json": "lean_verified_declarations",
    "unresolved_blockers.md": "unresolved_blockers",
    "limitations.md": "limitations",
    "artifact_manifest.json": "artifact_manifest",
    "writing_brief.md": "writing_brief",
    "proof_attempt_ledger.jsonl": "proof_attempt_ledger",
    "known_problem_smoke_report.json": "known_problem_smoke_report",
}

LEAN_VERIFIED_DECLARATION_SOURCE = "verified_declarations.json"
NON_VERIFIED_RESEARCH_EVIDENCE_FILES = {
    "proof_summary.md",
    "natural_language_proof_sketches.json",
    "writing_brief.md",
}
OPTIONAL_PROJECT_BUNDLE_FILES = ("proof_attempt_ledger.jsonl",)


def _relative(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        return str(path)


def _infer_repo_root(project_dir: Path) -> Path:
    for parent in (project_dir, *project_dir.parents):
        if parent.name == "projects":
            return parent.parent
        if parent.name == "artifacts":
            return parent.parent
    return project_dir.parent


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple, set)) else [value]
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return cleaned


def _first_nonempty_line(text: str, fallback: str = "") -> str:
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return fallback


def _excerpt(text: str, limit: int = 1600) -> str:
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _problem_metadata(project_dir: Path) -> dict[str, Any]:
    problem = _read_yaml(project_dir / "problem.yaml")
    state = read_json(project_dir / "state.json", {})
    claims = load_claim_ledger(project_dir).get("claims", [])
    first_claim = next((item for item in claims if isinstance(item, dict) and item.get("statement_nl")), {})
    problem_id = str(problem.get("problem_id") or state.get("problem_id") or project_dir.name).strip()
    statement = str(problem.get("statement") or first_claim.get("statement_nl") or "").strip()
    title = str(problem.get("title") or first_claim.get("title") or problem_id).strip()
    return {
        "problem_id": problem_id,
        "title": title,
        "statement": statement,
        "source": str(problem.get("source") or "").strip(),
        "references": _string_list(problem.get("references")),
        "problem_yaml": problem,
    }


def _render_theorem_statement(metadata: dict[str, Any]) -> str:
    lines = [
        f"# {metadata['title'] or metadata['problem_id']}",
        "",
        "## Theorem Statement",
        "",
        metadata["statement"] or "No theorem statement is recorded for this AMRA project.",
        "",
        "## Provenance",
        "",
        f"- Problem ID: `{metadata['problem_id']}`",
    ]
    if metadata["source"]:
        lines.append(f"- Source: {metadata['source']}")
    if metadata["references"]:
        lines.append("- References: " + ", ".join(metadata["references"]))
    lines.append("")
    return "\n".join(lines)


def _problem_metadata_payload(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": PROBLEM_METADATA_SCHEMA_VERSION,
        "problem_id": metadata["problem_id"],
        "title": metadata["title"],
        "statement": metadata["statement"],
        "source": metadata["source"],
        "references": metadata["references"],
        "problem_yaml": metadata["problem_yaml"],
    }


def _load_json_report(path: Path) -> dict[str, Any]:
    payload = read_json(path, {})
    return payload if isinstance(payload, dict) else {}


def _candidate_build_report_paths(project_dir: Path) -> list[Path]:
    direct = [
        project_dir / "artifacts" / "lean_build_report.json",
        project_dir / "lean_build_report.json",
        project_dir / "build_report.json",
        project_dir / "formal" / "build_report.json",
    ]
    run_reports = sorted((project_dir / "runs").rglob("build_report.json")) if (project_dir / "runs").exists() else []
    lean_reports = sorted((project_dir / "runs").rglob("report.json")) if (project_dir / "runs").exists() else []
    return direct + run_reports + lean_reports


def _load_lean_build_report(project_dir: Path, repo_root: Path) -> dict[str, Any]:
    for path in _candidate_build_report_paths(project_dir):
        if not path.exists():
            continue
        payload = _load_json_report(path)
        if not payload:
            continue
        return {
            **payload,
            "source_path": _relative(path, repo_root),
        }
    return {
        "schema_version": "amra.lean_build_report.v1",
        "status": "missing",
        "source_path": "",
        "message": "No Lean build report was found in the AMRA project.",
    }


def _build_report_status(build_report: dict[str, Any]) -> str:
    best_audit = build_report.get("best_audit") if isinstance(build_report.get("best_audit"), dict) else {}
    if best_audit.get("build_status"):
        return str(best_audit["build_status"]).strip().lower()
    return str(build_report.get("status") or "").strip().lower()


def _verified_declarations(
    project_dir: Path,
    *,
    repo_root: Path,
    build_report: dict[str, Any],
    source_payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    payload = source_payload if source_payload is not None else load_verified_declarations(project_dir)
    declarations = payload.get("declarations", []) if isinstance(payload, dict) else []
    verified: list[dict[str, Any]] = []
    for declaration in declarations:
        if not isinstance(declaration, dict):
            continue
        status = str(declaration.get("status") or "lean_verified").strip().lower()
        if status not in VERIFIED_DECLARATION_STATUSES:
            continue
        name = str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or "").strip()
        if not name:
            continue
        verified.append(
            {
                **declaration,
                "name": str(declaration.get("name") or name.split(".")[-1]).strip(),
                "full_name": name,
                "lean_name": str(declaration.get("lean_name") or name).strip(),
                "status": "lean_verified",
                "lean_verified": True,
                "verification_basis": "verified_declarations.json",
                "lean_build_report_status": _build_report_status(build_report) or "unknown",
                "source_path": _relative(project_dir / "verified_declarations.json", repo_root),
            }
        )
    deduped: dict[str, dict[str, Any]] = {}
    for declaration in verified:
        key = str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or "").strip()
        if key and key not in deduped:
            deduped[key] = declaration
    return sorted(deduped.values(), key=lambda item: str(item.get("full_name") or item.get("name") or ""))


def _declaration_key(declaration: dict[str, Any]) -> str:
    return str(declaration.get("full_name") or declaration.get("lean_name") or declaration.get("name") or "").strip()


def _declaration_payload_preserving_recorded_status(
    *,
    before_consolidation: dict[str, Any],
    after_consolidation: dict[str, Any],
) -> dict[str, Any]:
    before = before_consolidation.get("declarations", []) if isinstance(before_consolidation, dict) else []
    after = after_consolidation.get("declarations", []) if isinstance(after_consolidation, dict) else []
    if not isinstance(before, list) or not before:
        return after_consolidation
    if not isinstance(after, list) or not after:
        return before_consolidation
    status_by_key: dict[str, str] = {}
    for item in before:
        if not isinstance(item, dict):
            continue
        key = _declaration_key(item)
        status = str(item.get("status") or "").strip()
        if not key or not status:
            continue
        existing = status_by_key.get(key)
        if existing is None or (existing.lower() in VERIFIED_DECLARATION_STATUSES and status.lower() not in VERIFIED_DECLARATION_STATUSES):
            status_by_key[key] = status
    declarations: list[dict[str, Any]] = []
    for item in after:
        if not isinstance(item, dict):
            continue
        key = _declaration_key(item)
        if key in status_by_key and status_by_key[key]:
            declarations.append({**item, "status": status_by_key[key]})
        else:
            declarations.append(dict(item))
    return {**after_consolidation, "declarations": declarations}


def _sketch_paths(project_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    proof_dir = project_dir / "proof"
    if proof_dir.exists():
        candidates.extend(sorted((proof_dir / "sketches").glob("*.md")) if (proof_dir / "sketches").exists() else [])
        candidates.extend(sorted(proof_dir.glob("*.md")))
    for name in ("proof_package.md", "proof_notes.md", "formalizer_handoff.md"):
        path = project_dir / name
        if path.exists():
            candidates.append(path)
    runs_dir = project_dir / "runs"
    if runs_dir.exists():
        for name in ("proof_package.md", "proof_notes.md", "summary.md"):
            candidates.extend(sorted(runs_dir.rglob(name)))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve(strict=False)
        if resolved in seen or not path.is_file():
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def _natural_language_sketches(project_dir: Path, *, repo_root: Path) -> list[dict[str, Any]]:
    sketches: list[dict[str, Any]] = []
    for path in _sketch_paths(project_dir):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            continue
        sketches.append(
            {
                "path": _relative(path, repo_root),
                "title": _first_nonempty_line(text, path.stem),
                "summary": _excerpt(text),
                "trust_level": NATURAL_LANGUAGE_TRUST_LEVEL,
                "lean_verified": False,
                "verification_status": "not_lean_verified",
                "ara_contract_role": "research_evidence_only",
            }
        )
    claim_sketches: list[dict[str, Any]] = []
    for claim in load_claim_ledger(project_dir).get("claims", []):
        if not isinstance(claim, dict):
            continue
        status = str(claim.get("status") or "").strip()
        if status not in {"sketch", "route_supported", "needs_review", "hypothesis"}:
            continue
        statement = str(claim.get("statement_nl") or "").strip()
        if not statement:
            continue
        claim_sketches.append(
            {
                "claim_id": str(claim.get("claim_id") or ""),
                "title": str(claim.get("claim_id") or "claim"),
                "summary": statement,
                "trust_level": NATURAL_LANGUAGE_TRUST_LEVEL,
                "claim_status": status,
                "lean_verified": False,
                "verification_status": "not_lean_verified",
                "ara_contract_role": "research_evidence_only",
            }
        )
    return sketches + claim_sketches


def _natural_language_sketches_payload(
    *,
    problem_id: str,
    natural_language_sketches: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": PROOF_SKETCHES_SCHEMA_VERSION,
        "problem_id": problem_id,
        "trust_level": NATURAL_LANGUAGE_TRUST_LEVEL,
        "lean_verified": False,
        "verification_status": "not_lean_verified",
        "ara_contract_role": "research_evidence_only",
        "consumption_rule": (
            "These sketches are natural-language research evidence only. "
            f"ARA must not treat them as Lean verified; use `{LEAN_VERIFIED_DECLARATION_SOURCE}` for formal claims."
        ),
        "sketches": natural_language_sketches,
    }


def _render_proof_summary(
    *,
    verified_declarations: list[dict[str, Any]],
    natural_language_sketches: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    failed_routes: list[dict[str, Any]],
) -> str:
    lines = [
        "# Proof Summary",
        "",
        "## Verification Boundary",
        "",
        "Natural-language proof sketches are research evidence only. They are not Lean-verified declarations.",
        "Only declarations listed in `verified_declarations.json` with `status=\"lean_verified\"` are treated as Lean verified.",
        "Detailed sketches are exported separately in `natural_language_proof_sketches.json` and remain non-verified evidence.",
        "",
        "## Lean-Verified Declarations",
        "",
    ]
    if not verified_declarations:
        lines.append("- None recorded.")
    for declaration in verified_declarations:
        lines.append(
            f"- `{declaration['full_name']}` status=`lean_verified` build_status=`{declaration.get('lean_build_report_status', 'unknown')}`"
        )
    lines.extend(["", "## Natural-Language Proof Sketches", ""])
    if not natural_language_sketches:
        lines.append("- None recorded.")
    for sketch in natural_language_sketches:
        source = sketch.get("path") or sketch.get("claim_id") or "inline"
        lines.append(
            f"- `{source}` trust_level=`{sketch['trust_level']}` "
            "lean_verified=`false` details=`natural_language_proof_sketches.json`"
        )
    lines.extend(["", "## Routes", ""])
    if not routes:
        lines.append("- None recorded.")
    for route in routes:
        lines.append(
            f"- `{route.get('route_id', '')}` status=`{route.get('status', 'unknown')}` target=`{route.get('target_claim') or 'none'}`"
        )
        if route.get("core_idea"):
            lines.append(f"  - Core idea: {route['core_idea']}")
        if route.get("blocker"):
            lines.append(f"  - Blocker: {route['blocker']}")
    lines.extend(["", "## Unresolved Blockers", ""])
    if not failed_routes:
        lines.append("- None recorded.")
    for failed in failed_routes:
        lines.append(
            f"- `{failed.get('route_id', '')}` mode=`{failed.get('failure_mode', 'proof_gap')}`: "
            f"{failed.get('failed_assertion') or failed.get('summary') or 'no assertion recorded'}"
        )
    lines.append("")
    return "\n".join(lines)


def _render_writing_brief(
    *,
    project_dir: Path,
    metadata: dict[str, Any],
    verified_declarations: list[dict[str, Any]],
    natural_language_sketches: list[dict[str, Any]],
) -> str:
    existing = project_dir / "writing_brief.md"
    lines = [
        "# AMRA Writing Brief",
        "",
        f"- Problem ID: `{metadata['problem_id']}`",
        f"- Lean-verified declarations: `{len(verified_declarations)}`",
        f"- Natural-language proof sketches: `{len(natural_language_sketches)}`",
        "",
        "## Verification Boundary",
        "",
        "Do not cite a natural-language proof sketch as a Lean-verified theorem. Use the verified declaration list for formal claims.",
        "",
    ]
    if existing.exists():
        lines.extend(["## Existing Writing Brief", "", existing.read_text(encoding="utf-8", errors="ignore").strip(), ""])
    else:
        lines.extend(
            [
                "## Draft",
                "",
                metadata["statement"] or "No theorem statement is recorded.",
                "",
            ]
        )
    return "\n".join(lines)


def _unresolved_blockers(
    *,
    build_report: dict[str, Any],
    verified_declarations: list[dict[str, Any]],
    failed_routes: list[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    build_status = _build_report_status(build_report)
    if build_status not in {"passed", "verified", "success"}:
        blockers.append(f"Lean build report status is `{build_status or 'missing'}`.")
    if not verified_declarations:
        blockers.append("No Lean-verified declarations are recorded in this bundle.")
    for route in failed_routes:
        assertion = str(route.get("failed_assertion") or route.get("summary") or "").strip()
        route_id = str(route.get("route_id") or "unknown-route").strip()
        blockers.append(f"{route_id}: {assertion or 'failed route recorded without an assertion'}")
    return blockers


def _limitations(
    *,
    metadata: dict[str, Any],
    build_report: dict[str, Any],
    verified_declarations: list[dict[str, Any]],
    natural_language_sketches: list[dict[str, Any]],
    blockers: list[str],
) -> list[str]:
    limitations = [
        (
            "Natural-language proof sketches are research evidence only and are not Lean verification evidence."
        )
    ]
    build_status = _build_report_status(build_report)
    if build_status in {"", "missing"}:
        limitations.append("No Lean build report was found for this AMRA project.")
    elif build_status not in {"passed", "verified", "success"}:
        limitations.append(f"Lean build report status is `{build_status}`.")
    sorry_count = build_report.get("sorry_count")
    if isinstance(sorry_count, int) and sorry_count > 0:
        limitations.append(f"Lean build report records `{sorry_count}` sorry placeholder(s).")
    if not verified_declarations:
        limitations.append("No Lean-verified declarations are recorded in this bundle.")
    if natural_language_sketches:
        limitations.append(
            "Proof sketches may guide follow-up writing, but formal claims must be sourced from `verified_declarations.json`."
        )
    if blockers:
        limitations.append("Unresolved blockers remain; see `unresolved_blockers.md`.")
    if not metadata["statement"]:
        limitations.append("No theorem statement is recorded for this AMRA project.")
    return _string_list(limitations)


def _render_blockers(blockers: list[str]) -> str:
    lines = ["# Unresolved Blockers", ""]
    if not blockers:
        lines.append("- None recorded.")
    else:
        lines.extend(f"- {blocker}" for blocker in blockers)
    lines.append("")
    return "\n".join(lines)


def _render_limitations(limitations: list[str]) -> str:
    lines = ["# Limitations", ""]
    if not limitations:
        lines.append("- None recorded.")
    else:
        lines.extend(f"- {limitation}" for limitation in limitations)
    lines.append("")
    return "\n".join(lines)


def _bundle_file_record(path: str) -> dict[str, Any]:
    kind = BUNDLE_FILE_KINDS.get(path, "supporting_artifact")
    record = {
        "path": path,
        "kind": kind,
        "required": path in REQUIRED_BUNDLE_FILES,
    }
    if path == LEAN_VERIFIED_DECLARATION_SOURCE:
        record.update(
            {
                "ara_contract_role": "only_lean_verified_claim_source",
                "lean_verified_claim_source": True,
            }
        )
    elif path == "proof_attempt_ledger.jsonl":
        record.update(
            {
                "ara_contract_role": "proof_attempt_audit_trail",
                "lean_verified_claim_source": False,
            }
        )
    elif path == "known_problem_smoke_report.json":
        record.update(
            {
                "ara_contract_role": "smoke_run_summary",
                "lean_verified_claim_source": False,
            }
        )
    elif path in NON_VERIFIED_RESEARCH_EVIDENCE_FILES:
        record.update(
            {
                "ara_contract_role": "research_evidence_only",
                "lean_verified_claim_source": False,
            }
        )
    return record


def _artifact_manifest(
    *,
    project_dir: Path,
    output_dir: Path,
    repo_root: Path,
    metadata: dict[str, Any],
    build_report: dict[str, Any],
    verified_declarations: list[dict[str, Any]],
    natural_language_sketches: list[dict[str, Any]],
    blockers: list[str],
    limitations: list[str],
    files: list[str],
) -> dict[str, Any]:
    source_artifacts = []
    for path in [
        project_dir / "problem.yaml",
        project_dir / "state.json",
        project_dir / "memory" / "claim_ledger.json",
        project_dir / "memory" / "route_ledger.json",
        project_dir / "memory" / "failed_routes.json",
        project_dir / "verified_declarations.json",
        project_dir / "proof_attempt_ledger.jsonl",
    ]:
        if path.exists():
            source_artifacts.append(_relative(path, repo_root))
    for sketch in natural_language_sketches:
        if sketch.get("path"):
            source_artifacts.append(str(sketch["path"]))
    return {
        "schema_version": RESULT_BUNDLE_MANIFEST_SCHEMA_VERSION,
        "bundle_schema_version": RESULT_BUNDLE_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "project": _relative(project_dir, repo_root),
        "bundle_dir": _relative(output_dir, repo_root),
        "problem_id": metadata["problem_id"],
        "theorem": {
            "title": metadata["title"],
            "statement_present": bool(metadata["statement"]),
            "source": metadata["source"],
            "references": metadata["references"],
        },
        "verification_policy": {
            "natural_language_proof_sketches_are_not_lean_verified": True,
            "verified_declarations_source": LEAN_VERIFIED_DECLARATION_SOURCE,
            "only_lean_verified_claim_source": LEAN_VERIFIED_DECLARATION_SOURCE,
            "natural_language_proof_sketches_source": "natural_language_proof_sketches.json",
            "non_verified_research_evidence_files": sorted(NON_VERIFIED_RESEARCH_EVIDENCE_FILES),
            "accepted_verified_declaration_statuses": sorted(VERIFIED_DECLARATION_STATUSES),
        },
        "lean_build_report_status": _build_report_status(build_report) or "missing",
        "verified_declaration_count": len(verified_declarations),
        "natural_language_proof_sketch_count": len(natural_language_sketches),
        "unresolved_blocker_count": len(blockers),
        "limitation_count": len(limitations),
        "verified_declarations": verified_declarations,
        "natural_language_proof_sketches": natural_language_sketches,
        "unresolved_blockers": blockers,
        "limitations": limitations,
        "source_artifacts": sorted(dict.fromkeys(source_artifacts)),
        "files": [_bundle_file_record(path) for path in files],
        "artifacts": [_bundle_file_record(path) for path in files],
    }


REQUIRED_BUNDLE_FILES = {
    "theorem_statement.md",
    "problem_metadata.json",
    "proof_summary.md",
    "natural_language_proof_sketches.json",
    "lean_build_report.json",
    "verified_declarations.json",
    "unresolved_blockers.md",
    "limitations.md",
    "artifact_manifest.json",
    "writing_brief.md",
}


def _copy_optional_bundle_files(project_dir: Path, output_dir: Path) -> list[str]:
    copied: list[str] = []
    for name in OPTIONAL_PROJECT_BUNDLE_FILES:
        source = project_dir / name
        if not source.is_file():
            continue
        destination = output_dir / name
        if source.resolve(strict=False) != destination.resolve(strict=False):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        copied.append(name)
    return copied


def export_amra_result_bundle(
    *,
    project: Path,
    output_dir: Path | None = None,
    repo_root: Path | None = None,
    consolidate: bool = True,
) -> dict[str, Any]:
    """Export an ARA-consumable AMRA result bundle without upgrading sketches to Lean facts."""

    project_dir = project.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve() if repo_root is not None else _infer_repo_root(project_dir)
    pre_consolidation_declarations = read_json(project_dir / "verified_declarations.json", {})
    if consolidate:
        consolidate_project_memory(project_dir, repo_root=repo_root)
    metadata = _problem_metadata(project_dir)
    output_dir = (
        output_dir.expanduser().resolve()
        if output_dir is not None
        else (repo_root / "amra_result_bundle").resolve()
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    build_report = _load_lean_build_report(project_dir, repo_root)
    declaration_source = _declaration_payload_preserving_recorded_status(
        before_consolidation=pre_consolidation_declarations if isinstance(pre_consolidation_declarations, dict) else {},
        after_consolidation=load_verified_declarations(project_dir),
    )
    verified_declarations = _verified_declarations(
        project_dir,
        repo_root=repo_root,
        build_report=build_report,
        source_payload=declaration_source,
    )
    natural_language_sketches = _natural_language_sketches(project_dir, repo_root=repo_root)
    routes = [dict(item) for item in load_route_ledger(project_dir).get("routes", []) if isinstance(item, dict)]
    failed_routes = [dict(item) for item in load_failed_routes(project_dir).get("failed_routes", []) if isinstance(item, dict)]
    blockers = _unresolved_blockers(
        build_report=build_report,
        verified_declarations=verified_declarations,
        failed_routes=failed_routes,
    )
    limitations = _limitations(
        metadata=metadata,
        build_report=build_report,
        verified_declarations=verified_declarations,
        natural_language_sketches=natural_language_sketches,
        blockers=blockers,
    )

    (output_dir / "theorem_statement.md").write_text(_render_theorem_statement(metadata), encoding="utf-8")
    write_json(output_dir / "problem_metadata.json", _problem_metadata_payload(metadata))
    (output_dir / "proof_summary.md").write_text(
        _render_proof_summary(
            verified_declarations=verified_declarations,
            natural_language_sketches=natural_language_sketches,
            routes=routes,
            failed_routes=failed_routes,
        ),
        encoding="utf-8",
    )
    write_json(output_dir / "lean_build_report.json", build_report)
    write_json(
        output_dir / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "updated_at": utc_now_iso(),
            "problem_id": metadata["problem_id"],
            "declarations": verified_declarations,
        },
    )
    write_json(
        output_dir / "natural_language_proof_sketches.json",
        _natural_language_sketches_payload(
            problem_id=metadata["problem_id"],
            natural_language_sketches=natural_language_sketches,
        ),
    )
    (output_dir / "writing_brief.md").write_text(
        _render_writing_brief(
            project_dir=project_dir,
            metadata=metadata,
            verified_declarations=verified_declarations,
            natural_language_sketches=natural_language_sketches,
        ),
        encoding="utf-8",
    )
    (output_dir / "unresolved_blockers.md").write_text(_render_blockers(blockers), encoding="utf-8")
    (output_dir / "limitations.md").write_text(_render_limitations(limitations), encoding="utf-8")
    _copy_optional_bundle_files(project_dir, output_dir)

    files = sorted(path.name for path in output_dir.iterdir() if path.is_file() and path.name != "artifact_manifest.json")
    manifest = _artifact_manifest(
        project_dir=project_dir,
        output_dir=output_dir,
        repo_root=repo_root,
        metadata=metadata,
        build_report=build_report,
        verified_declarations=verified_declarations,
        natural_language_sketches=natural_language_sketches,
        blockers=blockers,
        limitations=limitations,
        files=files + ["artifact_manifest.json"],
    )
    write_json(output_dir / "artifact_manifest.json", manifest)
    return {
        "schema_version": RESULT_BUNDLE_SCHEMA_VERSION,
        "generated_at": manifest["generated_at"],
        "project": _relative(project_dir, repo_root),
        "bundle_dir": _relative(output_dir, repo_root),
        "artifact_manifest": _relative(output_dir / "artifact_manifest.json", repo_root),
        "required_files": sorted(REQUIRED_BUNDLE_FILES),
        "verified_declaration_count": len(verified_declarations),
        "natural_language_proof_sketch_count": len(natural_language_sketches),
        "unresolved_blocker_count": len(blockers),
        "limitation_count": len(limitations),
    }


write_amra_result_bundle = export_amra_result_bundle
export_result_bundle = export_amra_result_bundle


__all__ = [
    "RESULT_BUNDLE_SCHEMA_VERSION",
    "RESULT_BUNDLE_MANIFEST_SCHEMA_VERSION",
    "PROBLEM_METADATA_SCHEMA_VERSION",
    "PROOF_SKETCHES_SCHEMA_VERSION",
    "LIMITATIONS_SCHEMA_VERSION",
    "VERIFIED_DECLARATION_STATUSES",
    "REQUIRED_BUNDLE_FILES",
    "export_amra_result_bundle",
    "write_amra_result_bundle",
    "export_result_bundle",
]
