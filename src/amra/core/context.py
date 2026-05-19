from __future__ import annotations

from pathlib import Path

from amra.core.workspace import load_project_manifest, read_json, read_text, utc_now_iso, write_json, write_text


EXACT_STATEMENT_PLACEHOLDER = "ARA_MATH_PLACEHOLDER_EXACT_STATEMENT"


def read_exact_statement(project_dir: Path) -> str:
    return read_text(project_dir / "idea" / "exact_statement.md")


def has_exact_statement(project_dir: Path) -> bool:
    statement = read_exact_statement(project_dir)
    if not statement.strip():
        return False
    return EXACT_STATEMENT_PLACEHOLDER not in statement


def set_exact_statement(project_dir: Path, statement_text: str, source: str = "") -> dict:
    cleaned = statement_text.strip()
    if not cleaned:
        raise ValueError("Exact statement text cannot be empty.")

    write_text(project_dir / "idea" / "exact_statement.md", cleaned + "\n")
    context = read_json(project_dir / "idea" / "problem_context.json", default={})
    manifest = load_project_manifest(project_dir)
    problem = manifest.get("problem", {})
    context.update(problem)
    context["exact_statement_status"] = "provided"
    context["exact_statement_source"] = source
    context["last_context_update"] = utc_now_iso()
    write_json(project_dir / "idea" / "problem_context.json", context)
    return context


def build_context_audit(project_dir: Path) -> dict:
    manifest = load_project_manifest(project_dir)
    context = read_json(project_dir / "idea" / "problem_context.json", default={})
    references = read_json(project_dir / "idea" / "references.json", default={"references": []})
    snapshots = read_json(project_dir / "idea" / "reference_snapshots.json", default={})
    recovery = read_json(project_dir / "idea" / "statement_recovery.json", default={})
    evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
    statement = read_exact_statement(project_dir)
    recovered_statement = str(recovery.get("statement", "")).strip()
    return {
        "problem_id": manifest["problem"]["problem_id"],
        "has_exact_statement": has_exact_statement(project_dir),
        "has_recovered_statement": bool(recovered_statement),
        "statement_length": len(statement.strip()),
        "reference_count": len(references.get("references", [])),
        "literature_snapshot_count": int(snapshots.get("snapshot_count", 0) or 0),
        "literature_evidence_count": sum(int(value) for value in (evidence.get("counts") or {}).values()),
        "exact_statement_status": context.get("exact_statement_status", "unknown"),
        "exact_statement_source": context.get("exact_statement_source", ""),
        "statement_recovery_status": recovery.get("status", ""),
        "recovered_statement": recovered_statement,
    }
