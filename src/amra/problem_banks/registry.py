from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ara_math.erdos_status import refresh_erdos_problem_record
from amra.core.models import ProblemRecord


REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = REPO_ROOT / "data"
DEFAULT_BANK_PATH = DATA_ROOT / "problem_bank.yaml"
DEFAULT_BANK_REGISTRY_PATH = DATA_ROOT / "bank_registry.yaml"


def _infer_domain(tags: list[str]) -> str:
    normalized = {tag.strip().lower() for tag in tags}
    if "geometry" in normalized:
        return "geometry"
    if "graph theory" in normalized:
        return "graph_theory"
    if "analysis" in normalized:
        return "analysis"
    if "ramsey theory" in normalized:
        return "ramsey_theory"
    if "combinatorics" in normalized or "additive combinatorics" in normalized:
        return "combinatorics"
    return "number_theory"


def _normalize_bank_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": str(entry["name"]),
        "path": str(entry["path"]),
        "description": str(entry.get("description", "")).strip(),
        "category": str(entry.get("category", "custom")).strip() or "custom",
        "problem_count": int(entry.get("problem_count", 0)),
        "provenance": str(entry.get("provenance", "")).strip(),
        "focus_tags": [str(item) for item in entry.get("focus_tags", [])],
        "synced_at": str(entry.get("synced_at", "")).strip(),
    }


def load_problem_bank(path: Path | str | None = None) -> list[ProblemRecord]:
    bank_path = Path(path) if path else DEFAULT_BANK_PATH
    payload = yaml.safe_load(bank_path.read_text(encoding="utf-8")) or []
    return [ProblemRecord.from_dict(item) for item in payload]


def save_problem_bank(problems: list[ProblemRecord], path: Path | str) -> Path:
    bank_path = Path(path)
    bank_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = [problem.to_dict() for problem in problems]
    bank_path.write_text(
        yaml.safe_dump(serializable, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return bank_path


def load_bank_registry(path: Path | str | None = None) -> list[dict[str, Any]]:
    registry_path = Path(path) if path else DEFAULT_BANK_REGISTRY_PATH
    if not registry_path.exists():
        return []
    payload = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or []
    return [_normalize_bank_entry(entry) for entry in payload]


def save_bank_registry(entries: list[dict[str, Any]], path: Path | str | None = None) -> Path:
    registry_path = Path(path) if path else DEFAULT_BANK_REGISTRY_PATH
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    normalized = [_normalize_bank_entry(entry) for entry in entries]
    registry_path.write_text(
        yaml.safe_dump(normalized, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return registry_path


def resolve_bank_path(
    *,
    bank_name: str | None = None,
    bank_path: Path | str | None = None,
    registry_path: Path | str | None = None,
) -> Path:
    if bank_path:
        return Path(bank_path)
    if bank_name:
        for entry in load_bank_registry(registry_path):
            if entry["name"] == bank_name:
                return Path(entry["path"])
        raise KeyError(f"Registered bank '{bank_name}' was not found.")
    return DEFAULT_BANK_PATH


def get_problem(problem_id: str, path: Path | str | None = None) -> ProblemRecord:
    for problem in load_problem_bank(path):
        if problem.problem_id == problem_id:
            return problem
    raise KeyError(f"Problem '{problem_id}' was not found in the problem bank.")


def normalize_erdos_problem_entry(entry: dict[str, Any]) -> ProblemRecord:
    number = str(entry["number"])
    tags = [str(tag) for tag in entry.get("tags", [])]
    formalized = str(entry.get("formalized", {}).get("state", "unknown"))
    comments = str(entry.get("comments", "")).strip()
    status_state = str(entry.get("status", {}).get("state", "open"))
    statement = (
        f"Erdős problem #{number}. "
        "Detailed statement should be imported from the full problem source before theorem work begins."
    )
    notes_parts = []
    if comments:
        notes_parts.append(comments)
    notes_parts.append(f"Imported from local Erdős metadata. Status: {status_state}.")
    return ProblemRecord(
        problem_id=number,
        title=f"Erdős Problem #{number}",
        source="Erdős Problems",
        statement=statement,
        domain=_infer_domain(tags),
        tags=tags,
        open_problem=status_state == "open",
        formalized=formalized,
        notes=" ".join(notes_parts).strip(),
        references=[f"https://www.erdosproblems.com/{number}"],
        hypotheses=[
            "The exact problem statement must be recovered from the authoritative source before proof search."
        ],
        recommended_strategy=[
            "Recover the exact statement and known results.",
            "Classify the task as formalization-first, finite search, or mixed strategy.",
        ],
        metadata={
            "source_catalog": "erdosproblems",
            "status_state": status_state,
            "prize": str(entry.get("prize", "no")),
            "oeis": [str(item) for item in entry.get("oeis", [])],
            "comments": comments,
            "statement_quality": "placeholder",
        },
    )


def import_erdos_problem_catalog(
    source: Path | str,
    output: Path | str,
    *,
    open_only: bool = False,
) -> Path:
    source_path = Path(source)
    entries = yaml.safe_load(source_path.read_text(encoding="utf-8")) or []
    normalized: list[ProblemRecord] = []
    for entry in entries:
        status_state = str(entry.get("status", {}).get("state", "open"))
        if open_only and status_state != "open":
            continue
        normalized.append(normalize_erdos_problem_entry(entry))
    normalized.sort(key=lambda item: int(item.problem_id) if item.problem_id.isdigit() else item.problem_id)
    return save_problem_bank(normalized, output)


def import_erdos_open_problems(source: Path | str, output: Path | str) -> Path:
    return import_erdos_problem_catalog(source, output, open_only=True)


def refresh_erdos_problem_bank(
    bank_path: Path | str,
    *,
    output_path: Path | str | None = None,
    problem_id: str | None = None,
) -> dict[str, Any]:
    source_path = Path(bank_path)
    destination = Path(output_path) if output_path else source_path
    refreshed: list[ProblemRecord] = []
    updated: list[dict[str, str]] = []
    closed_count = 0
    likely_solved_count = 0

    for problem in load_problem_bank(source_path):
        if problem_id and problem.problem_id != problem_id:
            refreshed.append(problem)
            continue
        updated_problem = refresh_erdos_problem_record(problem)
        refreshed.append(updated_problem)
        status_state = str((updated_problem.metadata or {}).get("status_state", "")).strip()
        remote = (updated_problem.metadata or {}).get("remote_status", {})
        if status_state != str((problem.metadata or {}).get("status_state", "")).strip() or updated_problem.open_problem != problem.open_problem:
            updated.append(
                {
                    "problem_id": updated_problem.problem_id,
                    "status_state": status_state,
                    "open_problem": "yes" if updated_problem.open_problem else "no",
                    "official_status": str(remote.get("official_status", "")),
                }
            )
        if not updated_problem.open_problem:
            closed_count += 1
        if status_state == "likely_solved_preprint":
            likely_solved_count += 1

    save_problem_bank(refreshed, destination)
    return {
        "input_bank": str(source_path),
        "output_bank": str(destination),
        "problem_count": len(refreshed),
        "updated_problem_count": len(updated),
        "closed_problem_count": closed_count,
        "likely_solved_preprint_count": likely_solved_count,
        "updated_problems": updated[:25],
    }
