from __future__ import annotations

import re
import shutil
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from amra.core.models import ProblemRecord
from amra.problem_banks.registry import load_problem_bank
from amra.infra.runtime import env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.evaluation.scouting import assess_problem_readiness
from amra.core.workspace import read_json, read_text, slugify, utc_now_iso, write_json, write_text


RECOMMENDATION_ORDER = {
    "promote": 0,
    "formalize_known": 1,
    "defer_source": 2,
    "defer_route": 3,
    "freeze": 4,
    "unknown": 5,
}


def _extract_field(text: str, label: str) -> str:
    pattern = rf"(?im)^\s*(?:[-*]\s*)?{re.escape(label)}\s*:\s*(.+?)\s*$"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def _normalize_choice(value: str, allowed: set[str], default: str) -> str:
    normalized = value.strip().lower().replace(" ", "_").replace("-", "_")
    normalized = re.sub(r"[^a-z0-9_]+", "", normalized)
    return normalized if normalized in allowed else default


def _parse_probe_output(text: str) -> dict[str, Any]:
    score_text = _extract_field(text, "Feasibility score")
    score_match = re.search(r"\d+(?:\.\d+)?", score_text)
    feasibility_score = float(score_match.group(0)) if score_match else 0.0
    feasibility_score = max(0.0, min(10.0, feasibility_score))
    recommendation = _normalize_choice(
        _extract_field(text, "Recommendation"),
        {"promote", "formalize_known", "defer_source", "defer_route", "freeze"},
        "unknown",
    )
    effort = _normalize_choice(
        _extract_field(text, "Estimated proof effort"),
        {"trivial", "small", "medium", "large", "research_program", "not_assessable"},
        "not_assessable",
    )
    blocker = _normalize_choice(
        _extract_field(text, "Primary blocker"),
        {
            "exact_statement",
            "source_provenance",
            "key_lemma",
            "open_core",
            "formalization",
            "certificate",
            "computation",
            "unknown",
        },
        "unknown",
    )
    proof_status = _normalize_choice(
        _extract_field(text, "Proof attempt status"),
        {"rigorous_partial", "heuristic_route", "failed", "known_theorem", "no_statement"},
        "failed",
    )
    return {
        "feasibility_score": feasibility_score,
        "recommendation": recommendation,
        "estimated_proof_effort": effort,
        "primary_blocker": blocker,
        "proof_attempt_status": proof_status,
        "next_investment": _extract_field(text, "Next investment"),
    }


class MathScoutRunner:
    """Actively probe open problems with short mathematical proof attempts.

    Passive scouting ranks by metadata and local assets. This runner is the
    next stage: it asks the backend to recover the exact statement if needed,
    try a shallow proof route, identify the real blocker, and estimate whether
    the problem deserves a full project.
    """

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.backend_max_memory_mb = env_int("ARA_MATH_SCOUT_BACKEND_MAX_MEMORY_MB", 4096)
        self.backend_max_cpu_seconds = env_int("ARA_MATH_SCOUT_BACKEND_MAX_CPU_SECONDS", 600)
        self.backend_max_processes = env_int("ARA_MATH_SCOUT_BACKEND_MAX_PROCESSES", 2048)
        self.backend_niceness = env_int("ARA_MATH_SCOUT_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_MATH_SCOUT_MODEL", env_str("ARA_MATH_BACKEND_MODEL", ""))
        self.backend_reasoning_effort = env_str(
            "ARA_MATH_SCOUT_REASONING_EFFORT",
            env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "medium"),
        )
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _candidate_rows(
        self,
        *,
        bank_path: Path,
        scout_report_path: Path | None,
    ) -> list[dict[str, Any]]:
        problems_by_id = {problem.problem_id: problem for problem in load_problem_bank(bank_path) if problem.open_problem}
        if scout_report_path and scout_report_path.exists():
            scout_report = read_json(scout_report_path, default={})
            rows: list[dict[str, Any]] = []
            seen: set[str] = set()
            for candidate in scout_report.get("top_candidates", []) + scout_report.get("shortlist_candidates", []):
                problem_id = str(candidate.get("problem_id", "")).strip()
                if not problem_id or problem_id in seen or problem_id not in problems_by_id:
                    continue
                seen.add(problem_id)
                rows.append({"problem": problems_by_id[problem_id], "passive_assessment": candidate})
            return rows

        rows = []
        for problem in problems_by_id.values():
            rows.append({"problem": problem, "passive_assessment": assess_problem_readiness(problem)})
        rows.sort(key=lambda item: (-int(item["passive_assessment"].get("score", 0)), str(item["problem"].problem_id)))
        return rows

    def _select_rows(
        self,
        rows: list[dict[str, Any]],
        *,
        selection_mode: str,
        exclude_problem_ids: set[str],
    ) -> list[dict[str, Any]]:
        filtered = [row for row in rows if str(row["problem"].problem_id) not in exclude_problem_ids]
        if selection_mode != "domain_balanced":
            return filtered
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in filtered:
            grouped[str(row["problem"].domain)].append(row)
        for domain_rows in grouped.values():
            domain_rows.sort(
                key=lambda item: (-int(item["passive_assessment"].get("score", 0)), str(item["problem"].problem_id))
            )
        domains = sorted(
            grouped,
            key=lambda domain: (
                -int(grouped[domain][0]["passive_assessment"].get("score", 0)),
                -len(grouped[domain]),
                domain,
            ),
        )
        ordered: list[dict[str, Any]] = []
        index = 0
        while True:
            advanced = False
            for domain in domains:
                if index < len(grouped[domain]):
                    ordered.append(grouped[domain][index])
                    advanced = True
            if not advanced:
                break
            index += 1
        return ordered

    def _problem_context(self, problem: ProblemRecord, passive_assessment: dict[str, Any]) -> str:
        payload = {
            "problem_id": problem.problem_id,
            "title": problem.title,
            "source": problem.source,
            "domain": problem.domain,
            "tags": problem.tags,
            "statement": problem.statement,
            "notes": problem.notes,
            "references": problem.references,
            "hypotheses": problem.hypotheses,
            "recommended_strategy": problem.recommended_strategy,
            "metadata": problem.metadata,
            "passive_assessment": {
                "score": passive_assessment.get("score"),
                "readiness_tier": passive_assessment.get("readiness_tier"),
                "investment_class": passive_assessment.get("investment_class"),
                "blocker_class": passive_assessment.get("blocker_class"),
                "recommended_next_action": passive_assessment.get("recommended_next_action"),
                "shallow_reasoning": passive_assessment.get("shallow_reasoning", []),
                "local_assets": passive_assessment.get("local_assets", []),
                "local_literature_signal": passive_assessment.get("local_literature_signal", {}),
            },
        }
        return str(payload)

    def _build_prompt(self, *, problem: ProblemRecord, passive_assessment: dict[str, Any]) -> str:
        return "\n".join(
            [
                "You are running an active mathematical broad-scouting probe for ARA Math.",
                "",
                "This is not metadata triage. You must make a shallow but real mathematical attempt:",
                "- Recover or restate the exact problem if the bank statement is a placeholder.",
                "- Try to prove the claim or reduce it to a known theorem, finite certificate, computation, or named missing lemma.",
                "- If the problem is too hard, explain the precise mathematical obstruction, not just that it is open.",
                "- Estimate the resources needed for a serious attack: literature, theorem proving, computation, Lean formalization.",
                "- Prefer rigorous partial deductions over broad commentary.",
                "- Do not claim a proof unless the dependency chain is explicit and checkable.",
                "",
                "Problem context:",
                "",
                "```text",
                self._problem_context(problem, passive_assessment),
                "```",
                "",
                "Output exactly these labeled fields, then a concise analysis:",
                "",
                "Feasibility score: <0-10>",
                "Recommendation: <promote|formalize_known|defer_source|defer_route|freeze>",
                "Estimated proof effort: <trivial|small|medium|large|research_program|not_assessable>",
                "Primary blocker: <exact_statement|source_provenance|key_lemma|open_core|formalization|certificate|computation|unknown>",
                "Proof attempt status: <rigorous_partial|heuristic_route|failed|known_theorem|no_statement>",
                "Next investment: <one concrete next task>",
                "",
                "Then include:",
                "## Exact statement recovered or still missing",
                "## Shallow proof attempt",
                "## Main obstruction",
                "## Resource estimate",
                "## Why this should be promoted or not",
            ]
        ).strip() + "\n"

    def _invoke_backend(
        self,
        *,
        backend: str,
        run_dir: Path,
        prompt: str,
        output_path: Path,
        timeout_sec: int,
        enable_search: bool,
    ) -> dict[str, Any]:
        if backend == "none":
            output_path.write_text("No active math-scout backend selected.\n", encoding="utf-8")
            return {"status": "skipped", "backend": backend, "returncode": 0, "elapsed_seconds": 0.0}
        backend_bin = shutil.which(backend)
        if not backend_bin:
            output_path.write_text(f"Backend `{backend}` is not available.\n", encoding="utf-8")
            return {"status": "unavailable", "backend": backend, "returncode": None, "elapsed_seconds": 0.0}
        if backend != "codex":
            output_path.write_text(f"Backend `{backend}` is not implemented for math-scout runs.\n", encoding="utf-8")
            return {"status": "unsupported", "backend": backend, "returncode": None, "elapsed_seconds": 0.0}

        command = [backend_bin, "-s", "read-only", "-a", "never"]
        if enable_search:
            command.append("--search")
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        resolved_run_dir = run_dir.resolve()
        resolved_output_path = output_path.resolve()
        command.extend(["exec", "-C", str(resolved_run_dir), "--output-last-message", str(resolved_output_path), prompt])

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=resolved_run_dir,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            if not output_path.exists():
                output_path.write_text("Timed out before producing a final backend message.\n", encoding="utf-8")
            return {
                "status": "timeout",
                "backend": backend,
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "stdout_tail": str(exc.stdout or exc.output or "")[-4000:],
                "stderr_tail": str(exc.stderr or "")[-4000:],
            }

        if not output_path.exists():
            output_path.write_text((completed.stdout + "\n\nSTDERR\n" + completed.stderr).strip() + "\n", encoding="utf-8")
        return {
            "status": "completed" if completed.returncode == 0 else "failed",
            "backend": backend,
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        }

    def _rank_key(self, entry: dict[str, Any]) -> tuple[float, int, str]:
        parsed = entry.get("parsed_probe", {})
        recommendation = str(parsed.get("recommendation", "unknown"))
        feasibility = float(parsed.get("feasibility_score", 0.0))
        return (-feasibility, RECOMMENDATION_ORDER.get(recommendation, 5), str(entry.get("problem_id", "")))

    def run(
        self,
        *,
        bank_path: Path,
        scout_report_path: Path | None = None,
        backend: str = "codex",
        problem_limit: int | None = None,
        start_index: int = 0,
        time_budget_sec: int = 3600,
        timeout_per_problem_sec: int = 300,
        output_path: Path | None = None,
        run_name: str | None = None,
        run_dir: Path | None = None,
        enable_search: bool = True,
        selection_mode: str = "ranked",
        exclude_problem_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        run_slug = slugify(run_name or f"math-scout-{utc_now_iso()}")
        run_dir = Path(run_dir) if run_dir is not None else self.repo_root / "artifacts" / "math_scout" / run_slug
        problem_root = run_dir / "problems"
        problem_root.mkdir(parents=True, exist_ok=True)
        output = output_path or (run_dir / "report.json")

        rows = self._select_rows(
            self._candidate_rows(bank_path=bank_path, scout_report_path=scout_report_path),
            selection_mode=selection_mode,
            exclude_problem_ids={str(item) for item in (exclude_problem_ids or [])},
        )
        rows = rows[start_index:]
        if problem_limit is not None:
            rows = rows[:problem_limit]

        existing = read_json(output, default={})
        existing_entries = existing.get("entries", []) if existing else []
        entries = [entry for entry in existing_entries if str(entry.get("problem_id", ""))]
        processed_ids = {str(entry.get("problem_id", "")) for entry in entries}
        started = time.monotonic()
        stop_reason = "completed"

        for offset, row in enumerate(rows, start=start_index):
            if time.monotonic() - started >= time_budget_sec:
                stop_reason = "time_budget_exhausted"
                break
            problem: ProblemRecord = row["problem"]
            if problem.problem_id in processed_ids:
                continue
            headroom = (
                {"status": "ready", "skipped": True, "reason": "backend_none"}
                if backend == "none"
                else wait_for_system_headroom(
                    min_available_memory_mb=self.min_available_memory_mb,
                    max_load_per_cpu=1.5,
                    max_wait_seconds=self.wait_max_seconds,
                    poll_seconds=self.wait_poll_seconds,
                )
            )
            if headroom["status"] != "ready":
                stop_reason = "system_guard_blocked"
                break

            passive_assessment = row["passive_assessment"]
            problem_dir = problem_root / f"{offset:04d}-{slugify(problem.problem_id)}"
            problem_dir.mkdir(parents=True, exist_ok=True)
            prompt = self._build_prompt(problem=problem, passive_assessment=passive_assessment)
            prompt_path = problem_dir / "prompt.txt"
            output_md = problem_dir / "probe_output.md"
            write_text(prompt_path, prompt)
            try:
                backend_report = self._invoke_backend(
                    backend=backend,
                    run_dir=problem_dir,
                    prompt=prompt,
                    output_path=output_md,
                    timeout_sec=max(1, timeout_per_problem_sec),
                    enable_search=enable_search,
                )
            except Exception as exc:
                if not output_md.exists():
                    write_text(output_md, f"Scout backend raised {type(exc).__name__}: {exc}\n")
                backend_report = {
                    "status": "error",
                    "backend": backend,
                    "returncode": None,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            probe_text = read_text(output_md)
            parsed_probe = _parse_probe_output(probe_text)
            entry = {
                "problem_id": problem.problem_id,
                "title": problem.title,
                "position": offset,
                "domain": problem.domain,
                "tags": problem.tags,
                "passive_score": passive_assessment.get("score", 0),
                "passive_investment_class": passive_assessment.get("investment_class", ""),
                "passive_blocker_class": passive_assessment.get("blocker_class", ""),
                "parsed_probe": parsed_probe,
                "backend_report": backend_report,
                "artifacts": {
                    "prompt": str(prompt_path),
                    "probe_output": str(output_md),
                },
            }
            entries.append(entry)
            processed_ids.add(problem.problem_id)
            ranked = sorted(entries, key=self._rank_key)
            write_json(
                output,
                {
                    "schema_version": "ara_math.math_scout_report.v1",
                    "generated_at": utc_now_iso(),
                    "status": "running",
                    "bank_path": str(bank_path),
                    "scout_report_path": str(scout_report_path) if scout_report_path else "",
                    "backend": backend,
                    "run_dir": str(run_dir),
                    "problem_limit": problem_limit,
                    "start_index": start_index,
                    "timeout_per_problem_sec": timeout_per_problem_sec,
                    "selection_mode": selection_mode,
                    "excluded_problem_ids": sorted(str(item) for item in (exclude_problem_ids or [])),
                    "entries": entries,
                    "ranked_candidates": ranked[:50],
                    "processed_problem_count": len(entries),
                    "stop_reason": stop_reason,
                },
            )

        ranked = sorted(entries, key=self._rank_key)
        payload = {
            "schema_version": "ara_math.math_scout_report.v1",
            "generated_at": utc_now_iso(),
            "status": "completed" if stop_reason == "completed" else "partial",
            "bank_path": str(bank_path),
            "scout_report_path": str(scout_report_path) if scout_report_path else "",
            "backend": backend,
            "run_dir": str(run_dir),
            "problem_limit": problem_limit,
            "start_index": start_index,
            "timeout_per_problem_sec": timeout_per_problem_sec,
            "selection_mode": selection_mode,
            "excluded_problem_ids": sorted(str(item) for item in (exclude_problem_ids or [])),
            "entries": entries,
            "ranked_candidates": ranked[:50],
            "processed_problem_count": len(entries),
            "stop_reason": stop_reason,
        }
        write_json(output, payload)
        return payload
