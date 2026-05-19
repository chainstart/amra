from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from amra.core.models import ProblemRecord


TEXT_TEMPLATE_SUFFIXES = {".lean", ".md", ".toml", ".txt", ".json"}
VALID_DELIVERABLE_MODES = {"auto", "research_report", "formalization_note", "paper_candidate"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "math-project"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def replace_template_tokens(root: Path, replacements: dict[str, str]) -> None:
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix not in TEXT_TEMPLATE_SUFFIXES and file_path.name != "lean-toolchain":
            continue
        text = file_path.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(f"{{{{{key}}}}}", value)
        file_path.write_text(text, encoding="utf-8")


def copy_template_tree(template_root: Path, destination: Path, replacements: dict[str, str]) -> None:
    shutil.copytree(template_root, destination, dirs_exist_ok=True)
    replace_template_tokens(destination, replacements)


def record_event(project_dir: Path, stage: str, event: str, details: dict[str, Any] | None = None) -> None:
    append_jsonl(
        project_dir / "pipeline_events.jsonl",
        {
            "ts": utc_now_iso(),
            "stage": stage,
            "event": event,
            "details": details or {},
        },
    )


def update_pipeline_status(
    project_dir: Path,
    *,
    stage: str,
    status: str,
    details: dict[str, Any] | None = None,
) -> None:
    payload = {
        "updated_at": utc_now_iso(),
        "stage": stage,
        "status": status,
        "details": details or {},
    }
    write_json(project_dir / "pipeline_status.json", payload)


def load_project_manifest(project_dir: Path) -> dict[str, Any]:
    manifest = read_json(project_dir / "project_manifest.json")
    if not manifest:
        raise FileNotFoundError(f"Missing project manifest in {project_dir}")
    return manifest


def deliverable_override_path(project_dir: Path) -> Path:
    return project_dir / "idea" / "deliverable_override.json"


def normalize_deliverable_override(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    raw_payload = payload or {}
    mode = str(raw_payload.get("mode", "auto")).strip() or "auto"
    if mode not in VALID_DELIVERABLE_MODES:
        raise ValueError(f"Invalid deliverable override mode: {mode}")
    return {
        "mode": mode,
        "reason": str(raw_payload.get("reason", "")).strip(),
        "updated_at": str(raw_payload.get("updated_at", "")).strip(),
    }


def load_deliverable_override(project_dir: Path) -> dict[str, Any]:
    return normalize_deliverable_override(read_json(deliverable_override_path(project_dir), default={}))


def set_deliverable_override(project_dir: Path, *, mode: str, reason: str = "") -> dict[str, Any]:
    payload = normalize_deliverable_override(
        {
            "mode": mode,
            "reason": reason,
            "updated_at": utc_now_iso(),
        }
    )
    write_json(deliverable_override_path(project_dir), payload)
    return payload


def create_project_workspace(
    *,
    repo_root: Path,
    projects_root: Path,
    project_name: str,
    problem: ProblemRecord,
) -> Path:
    project_slug = slugify(project_name)
    project_dir = projects_root / project_slug
    if project_dir.exists():
        raise FileExistsError(f"Project already exists: {project_dir}")

    for relative_dir in ("idea", "proof", "formal", "writing", "artifacts"):
        (project_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    template_root = repo_root / "src" / "ara_math" / "templates" / "lean_project"
    copy_template_tree(
        template_root,
        project_dir / "formal",
        {
            "PROJECT_NAME": project_name,
            "PROJECT_SLUG": project_slug,
            "TARGET_STATEMENT": problem.statement,
        },
    )

    manifest = {
        "project_name": project_name,
        "project_slug": project_slug,
        "track": "math",
        "created_at": utc_now_iso(),
        "problem": problem.to_dict(),
    }
    write_json(project_dir / "project_manifest.json", manifest)
    write_json(
        project_dir / "idea" / "problem_context.json",
        {
            **problem.to_dict(),
            "exact_statement_status": "placeholder",
            "exact_statement_source": "",
            "last_context_update": utc_now_iso(),
        },
    )
    write_text(
        project_dir / "idea" / "exact_statement.md",
        "\n".join(
            [
                f"# Exact Statement for {problem.title}",
                "",
                "<!-- ARA_MATH_PLACEHOLDER_EXACT_STATEMENT -->",
                "Replace this file with the exact mathematical statement from the authoritative source before claiming proof progress.",
                "",
                "Current placeholder:",
                "",
                problem.statement,
                "",
            ]
        )
        + "\n",
    )
    write_json(
        project_dir / "idea" / "references.json",
        {
            "generated_at": utc_now_iso(),
            "references": problem.references,
        },
    )
    write_json(
        project_dir / "idea" / "proof_path_assessment.json",
        {
            "generated_at": utc_now_iso(),
            "status": "not_generated",
            "problem_id": problem.problem_id,
            "proof_path_hypothesis": [],
            "blockers": [],
        },
    )
    write_json(
        project_dir / "idea" / "literature_foundations.json",
        {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "historical_foundations": [],
            "references": problem.references,
        },
    )
    write_json(
        project_dir / "idea" / "reference_snapshots.json",
        {
            "generated_at": utc_now_iso(),
            "project_name": project_name,
            "problem_id": problem.problem_id,
            "source_count": 0,
            "snapshot_count": 0,
            "skipped_source_count": 0,
            "snapshots": [],
            "skipped_sources": [],
        },
    )
    write_json(
        project_dir / "idea" / "literature_evidence.json",
        {
            "counts": {
                "known_results": 0,
                "proof_ingredients": 0,
                "modern_tools": 0,
                "open_gaps": 0,
            },
            "source_attribution_count": 0,
            "sources": [],
            "known_results": [],
            "proof_ingredients": [],
            "modern_tools": [],
            "open_gaps": [],
        },
    )
    write_json(
        project_dir / "idea" / "statement_recovery.json",
        {
            "status": "not_run",
            "statement": "",
            "source": "",
            "score": 0,
        },
    )
    write_text(
        project_dir / "idea" / "literature_digest.md",
        "# Literature Digest\n\nNo literature harvest has been run yet.\n",
    )
    write_json(
        project_dir / "idea" / "math_idea_ledger.json",
        {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "themes": [],
            "route_hypotheses": [],
            "reusable_assets": [],
            "status": "seeded",
        },
    )
    write_json(
        deliverable_override_path(project_dir),
        {
            "mode": "auto",
            "reason": "",
            "updated_at": utc_now_iso(),
        },
    )
    research_notes_lines = [
        f"# Research Notes for {problem.title}",
        "",
        "## Known Context",
        "",
        problem.notes or "No additional notes yet.",
        "",
        "## Hypotheses",
        "",
    ]
    research_notes_lines.extend(
        [f"- {item}" for item in problem.hypotheses] if problem.hypotheses else ["- No hypotheses recorded yet."]
    )
    research_notes_lines.extend(
        [
            "",
            "## Next Sources To Read",
            "",
        ]
    )
    research_notes_lines.extend(
        [f"- {item}" for item in problem.references] if problem.references else ["- Add source links here."]
    )
    research_notes_lines.append("")
    write_text(
        project_dir / "idea" / "research_notes.md",
        "\n".join(research_notes_lines) + "\n",
    )
    write_json(
        project_dir / "proof" / "claim_registry.json",
        {
            "generated_at": utc_now_iso(),
            "claims": [],
        },
    )
    write_json(
        project_dir / "proof" / "proof_plan.json",
        {
            "generated_at": utc_now_iso(),
            "tasks": [],
            "notes": ["Plan has not been generated yet."],
        },
    )
    write_json(
        project_dir / "proof" / "counterexample_search_contract.json",
        {
            "generated_at": utc_now_iso(),
            "status": "not_started",
            "search_contract": "",
            "assumptions": [],
            "outputs": [],
            "command": [],
            "working_directory": "",
            "timeout_sec": 0,
            "auto_run_allowed": False,
            "expected_output_paths": [],
            "last_run_status": "",
        },
    )
    write_text(
        project_dir / "proof" / "current_focus.md",
        "# Current Focus\n\n- No proof-search agenda has been generated yet.\n",
    )
    write_text(
        project_dir / "writing" / "manuscript.md",
        "\n".join(
            [
                f"# {problem.title}",
                "",
                "## Abstract",
                "",
                "## Introduction",
                "",
                "## Exact Statement",
                "",
                "## Preliminaries",
                "",
                "## Main Results",
                "",
                "## Formalization Status",
                "",
                "## Formalization Notes",
                "",
                "## Discussion",
                "",
            ]
        )
        + "\n",
    )
    write_text(
        project_dir / "writing" / "reviewer_notes.md",
        "# Reviewer Notes\n\nNo review has been generated yet.\n",
    )
    update_pipeline_status(
        project_dir,
        stage="workspace",
        status="created",
        details={"project_name": project_name, "problem_id": problem.problem_id},
    )
    record_event(
        project_dir,
        stage="workspace",
        event="project_created",
        details={"project_name": project_name, "problem_id": problem.problem_id},
    )
    return project_dir


def init_comath_project(
    project_dir: Path,
    *,
    project_name: str | None = None,
    original_goal: str | None = None,
) -> Any:
    from ara_math.coordinator import initialize_comath_project

    return initialize_comath_project(project_dir, project_name=project_name, original_goal=original_goal)


def project_dashboard(project_dir: Path) -> str:
    from ara_math.coordinator import render_project_dashboard

    return render_project_dashboard(project_dir)
