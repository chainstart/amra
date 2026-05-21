from __future__ import annotations

import re
from pathlib import Path
from typing import Any


NO_EXTERNAL_SOURCE_FEATURES: tuple[str, ...] = (
    "browser_use",
    "browser_use_external",
    "in_app_browser",
)

WEB_SEARCH_TRANSCRIPT_PATTERN = re.compile(r"(?im)^\s*web search\s*:")


def apply_codex_source_policy(command: list[str], *, enable_search: bool) -> None:
    """Apply Codex feature flags for the requested external-source policy."""

    if enable_search:
        command.append("--search")
        return
    for feature in NO_EXTERNAL_SOURCE_FEATURES:
        command.extend(["--disable", feature])


def closed_book_policy_prompt() -> str:
    return "\n".join(
        [
            "External source policy: CLOSED-BOOK BENCHMARK.",
            "Do not use web search, browser tools, online solution pages, papers, forums, or network fetches.",
            "Do not look up known answers, official solutions, editorials, or discussion threads.",
            "Use only the supplied statement/context, local theorem-proving workspace, installed math tools, and computations you run locally.",
            "Python, SymPy, Z3, Lean, CAS tools, finite searches, SMT checks, and local mathlib/source inspection are allowed.",
            "If a route needs outside literature or a known solution, stop and report the blocker instead of searching.",
        ]
    )


def open_research_policy_prompt() -> str:
    return "\n".join(
        [
            "External source policy: OPEN RESEARCH.",
            "Web/source/literature search is enabled for this run. Record any external source you rely on in durable notes.",
        ]
    )


def source_policy_prompt(*, enable_search: bool) -> str:
    return open_research_policy_prompt() if enable_search else closed_book_policy_prompt()


def detect_external_source_violations(*texts: str) -> list[str]:
    violations: list[str] = []
    for text in texts:
        for match in WEB_SEARCH_TRANSCRIPT_PATTERN.finditer(text or ""):
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.start())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end].strip()
            if line and line not in violations:
                violations.append(line[:500])
    return violations


def mark_policy_violation(
    *,
    report: dict[str, Any],
    output_path: Path,
    stdout: str,
    stderr: str,
    enable_search: bool,
) -> dict[str, Any]:
    if enable_search:
        return report
    last_message = output_path.read_text(encoding="utf-8", errors="ignore") if output_path.exists() else ""
    violations = detect_external_source_violations(stdout, stderr, last_message)
    if not violations:
        return report
    report = {**report}
    report["status"] = "policy_violation"
    report["policy_violations"] = violations
    violation_path = output_path.parent.parent / "external_source_policy_violation.md"
    violation_path.parent.mkdir(parents=True, exist_ok=True)
    violation_path.write_text(
        "\n".join(
            [
                "# External Source Policy Violation",
                "",
                "This closed-book benchmark episode attempted to use an external source.",
                "",
                "## Detected Transcript Lines",
                "",
                *[f"- `{line}`" for line in violations],
                "",
                "The episode output should not be treated as a valid benchmark result.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    report["policy_violation_path"] = str(violation_path)
    return report
