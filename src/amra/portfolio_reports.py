from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from amra.portfolio_memory import read_json, utc_now_iso


FINAL_REPORT_SCHEMA_VERSION = "amra.portfolio_final_report.v1"


def _relative(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        return str(path)


def _ranking_items(campaign_dir: Path) -> list[dict[str, Any]]:
    payload = read_json(campaign_dir / "ranking.json", {"ranking": []})
    items = payload.get("ranking", payload) if isinstance(payload, dict) else payload
    return [dict(item) for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def _queue_items(path: Path) -> list[dict[str, Any]]:
    payload = read_json(path, {"items": []})
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    return [dict(item) for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def _problem_id(item: dict[str, Any]) -> str:
    return str(item.get("problem_id") or item.get("id") or "").strip()


def _disposition(item: dict[str, Any], promoted_ids: set[str]) -> str:
    problem_id = _problem_id(item)
    recommendation = str(item.get("recommendation") or "").strip().lower()
    risk_flags = {str(flag).strip().lower() for flag in item.get("risk_flags", []) or []}
    if problem_id in promoted_ids:
        return "promoted"
    if recommendation == "freeze" or "strong_counterexample" in risk_flags:
        return "frozen"
    return "parked"


def _reason(item: dict[str, Any], disposition: str) -> str:
    recommendation = str(item.get("recommendation") or "unknown")
    blocker = str(item.get("primary_blocker") or "").strip()
    risk_flags = [str(flag) for flag in item.get("risk_flags", []) or [] if str(flag).strip()]
    exact = bool(item.get("has_exact_statement", False))
    priority = item.get("priority", "unknown")
    shallow = item.get("shallow_proof_signal") if isinstance(item.get("shallow_proof_signal"), dict) else {}
    proof_status = str(shallow.get("proof_attempt_status") or "unknown")
    next_investment = str(shallow.get("next_investment") or "").strip()

    if disposition == "promoted":
        base = (
            f"Promoted because recommendation=`{recommendation}` with priority `{priority}` "
            f"and {'an exact' if exact else 'no exact'} statement recorded."
        )
    elif disposition == "frozen":
        base = (
            f"Frozen because recommendation=`{recommendation}` or the risk flags indicate that "
            "the current target should not receive more proof-search budget."
        )
    else:
        base = (
            f"Parked because recommendation=`{recommendation}` with priority `{priority}` "
            "does not currently justify promotion."
        )

    details: list[str] = []
    if blocker:
        details.append(f"primary blocker `{blocker}`")
    if risk_flags:
        details.append("risk flags " + ", ".join(f"`{flag}`" for flag in risk_flags))
    if proof_status != "unknown":
        details.append(f"proof signal `{proof_status}`")
    if next_investment:
        details.append(f"next investment: {next_investment}")
    if not details:
        return base
    return base + " Evidence: " + "; ".join(details) + "."


def build_portfolio_final_report(campaign_dir: Path, *, repo_root: Path | None = None) -> dict[str, Any]:
    """Build a structured explanation for every campaign problem disposition."""

    campaign_dir = campaign_dir.expanduser().resolve()
    manifest = read_json(campaign_dir / "campaign_manifest.json", {})
    state = read_json(campaign_dir / "campaign_state.json", {})
    ranking = _ranking_items(campaign_dir)
    promotion_queue = _queue_items(campaign_dir / "promotion_queue.json")
    parked_queue = _queue_items(campaign_dir / "parked_queue.json")
    promoted_ids = {_problem_id(item) for item in promotion_queue}
    explanations: list[dict[str, Any]] = []

    for index, item in enumerate(ranking, start=1):
        disposition = _disposition(item, promoted_ids)
        explanations.append(
            {
                "problem_id": _problem_id(item),
                "title": str(item.get("title") or ""),
                "rank": index,
                "disposition": disposition,
                "recommendation": str(item.get("recommendation") or ""),
                "priority": item.get("priority"),
                "primary_blocker": str(item.get("primary_blocker") or ""),
                "risk_flags": [str(flag) for flag in item.get("risk_flags", []) or []],
                "has_exact_statement": bool(item.get("has_exact_statement", False)),
                "reason": _reason(item, disposition),
            }
        )

    return {
        "schema_version": FINAL_REPORT_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "campaign_dir": _relative(campaign_dir, repo_root),
        "campaign_id": str(manifest.get("campaign_id") or state.get("campaign_id") or campaign_dir.name),
        "run_name": str(manifest.get("run_name") or ""),
        "ranked_problem_count": len(ranking),
        "promoted_count": sum(1 for item in explanations if item["disposition"] == "promoted"),
        "parked_count": sum(1 for item in explanations if item["disposition"] == "parked"),
        "frozen_count": sum(1 for item in explanations if item["disposition"] == "frozen"),
        "promotion_queue_count": len(promotion_queue),
        "parked_queue_count": len(parked_queue),
        "explanations": explanations,
        "source_artifacts": {
            "manifest": _relative(campaign_dir / "campaign_manifest.json", repo_root),
            "ranking": _relative(campaign_dir / "ranking.json", repo_root),
            "promotion_queue": _relative(campaign_dir / "promotion_queue.json", repo_root),
            "parked_queue": _relative(campaign_dir / "parked_queue.json", repo_root),
        },
    }


def render_portfolio_final_report(campaign_dir: Path, *, repo_root: Path | None = None) -> str:
    report = build_portfolio_final_report(campaign_dir, repo_root=repo_root)
    lines = [
        f"# AMRA Portfolio Campaign: {report['run_name'] or report['campaign_id']}",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Campaign ID: `{report['campaign_id']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Ranked problems: `{report['ranked_problem_count']}`",
        f"- Promoted: `{report['promoted_count']}`",
        f"- Parked: `{report['parked_count']}`",
        f"- Frozen: `{report['frozen_count']}`",
        "",
        "## Problem Dispositions",
        "",
    ]
    if not report["explanations"]:
        lines.append("- No ranked problems were recorded.")
    for item in report["explanations"]:
        title = f" - {item['title']}" if item["title"] else ""
        lines.append(f"### `{item['problem_id']}`{title}")
        lines.append("")
        lines.append(f"- Disposition: `{item['disposition']}`")
        lines.append(f"- Recommendation: `{item['recommendation'] or 'unknown'}`")
        lines.append(f"- Priority: `{item['priority']}`")
        lines.append(f"- Reason: {item['reason']}")
        if item["primary_blocker"]:
            lines.append(f"- Primary blocker: `{item['primary_blocker']}`")
        if item["risk_flags"]:
            lines.append("- Risk flags: " + ", ".join(f"`{flag}`" for flag in item["risk_flags"]))
        lines.append("")

    lines.extend(
        [
            "## Source Artifacts",
            "",
            "```json",
            json.dumps(report["source_artifacts"], indent=2, ensure_ascii=False, sort_keys=True),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_portfolio_final_report(
    campaign_dir: Path,
    *,
    output_path: Path | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    campaign_dir = campaign_dir.expanduser().resolve()
    output_path = output_path.expanduser().resolve() if output_path is not None else campaign_dir / "final_report.md"
    text = render_portfolio_final_report(campaign_dir, repo_root=repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")
    report = build_portfolio_final_report(campaign_dir, repo_root=repo_root)
    return {
        **report,
        "final_report": _relative(output_path, repo_root),
    }


generate_portfolio_final_report = write_portfolio_final_report


__all__ = [
    "FINAL_REPORT_SCHEMA_VERSION",
    "build_portfolio_final_report",
    "render_portfolio_final_report",
    "write_portfolio_final_report",
    "generate_portfolio_final_report",
]
