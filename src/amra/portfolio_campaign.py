from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ara_math.math_scout import MathScoutRunner
from amra.core.workspace import slugify
from amra.problem_banks.registry import load_problem_bank

from amra.amra_library import AmraLibraryManager
from amra.portfolio_evaluator import PortfolioEvaluator
from amra.portfolio_memory import (
    append_jsonl,
    append_state_transition,
    consolidate_project_memory,
    initialize_memory,
    read_json,
    update_global_memory,
    utc_now_iso,
    write_resume_pack,
    write_json,
)
from amra.portfolio_scheduler import PortfolioAttackScheduler


DEFAULT_CAMPAIGN_ROOT = Path("artifacts") / "portfolio_campaigns"


def _has_exact_statement(problem: Any) -> bool:
    statement = str(getattr(problem, "statement", ""))
    lowered = statement.lower()
    return "placeholder" not in lowered and "detailed statement should be imported" not in lowered


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _scout_backend_status(scout_entry: dict[str, Any] | None) -> str:
    if not scout_entry:
        return "not_processed"
    backend_report = scout_entry.get("backend_report", {})
    if isinstance(backend_report, dict):
        status = str(backend_report.get("status", "")).strip()
        if status:
            return status
    return str(scout_entry.get("status", "unknown")).strip() or "unknown"


def _parsed_probe(scout_entry: dict[str, Any] | None) -> dict[str, Any]:
    parsed = scout_entry.get("parsed_probe", {}) if scout_entry else {}
    return parsed if isinstance(parsed, dict) else {}


def _active_scout_available(scout_entry: dict[str, Any] | None) -> bool:
    status = _scout_backend_status(scout_entry)
    parsed = _parsed_probe(scout_entry)
    recommendation = str(parsed.get("recommendation", "unknown"))
    return status not in {"not_processed", "skipped", "unavailable", "unsupported"} and recommendation != "unknown"


def _score_problem(problem: Any, scout_entry: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = getattr(problem, "metadata", {}) or {}
    tags = [str(item).lower() for item in getattr(problem, "tags", [])]
    references = list(getattr(problem, "references", []) or [])
    exact_statement = _has_exact_statement(problem)
    parsed_probe = _parsed_probe(scout_entry)
    scout_status = _scout_backend_status(scout_entry)
    scout_active = _active_scout_available(scout_entry)
    scout_recommendation = str(parsed_probe.get("recommendation", "unknown"))
    scout_feasibility = float(parsed_probe.get("feasibility_score", 0.0) or 0.0)
    proof_attempt_status = str(parsed_probe.get("proof_attempt_status", "failed"))
    scout_primary_blocker = str(parsed_probe.get("primary_blocker", "unknown"))
    source_quality_score = 2.0 + min(len(references), 3) + (1.0 if exact_statement else 0.0)
    feasibility_score = 4.0
    if exact_statement:
        feasibility_score += 2.0
    if metadata.get("statement_quality") == "placeholder":
        feasibility_score -= 1.5
    if "geometry" in tags or "combinatorics" in tags:
        feasibility_score += 0.5
    formalization_score = 4.0 + (1.5 if getattr(problem, "formalized", "") == "yes" else 0.0)
    if scout_active and scout_recommendation == "formalize_known":
        formalization_score += 1.0
    reusable_asset_score = 2.0 + (1.0 if any(tag in {"number theory", "combinatorics"} for tag in tags) else 0.0)
    risk_score = 4.0 if not exact_statement else 2.0
    risk_flags = [] if exact_statement else ["needs_source"]
    if scout_status == "timeout":
        risk_score += 1.0
        risk_flags.append("scout_timeout")
    elif scout_status in {"failed", "error"}:
        risk_score += 1.0
        risk_flags.append("scout_failure")
    if scout_active and scout_primary_blocker in {"exact_statement", "source_provenance"} and "needs_source" not in risk_flags:
        risk_flags.append("needs_source")
    expected_hours = max(1.0, 8.0 - feasibility_score / 2.0)
    proof_status_bonus = {
        "known_theorem": 2.0,
        "rigorous_partial": 1.5,
        "heuristic_route": 0.75,
        "failed": -1.0,
        "no_statement": -1.5,
    }.get(proof_attempt_status, 0.0)
    recommendation_bonus = {
        "promote": 2.0,
        "formalize_known": 1.25,
        "defer_source": -1.0,
        "defer_route": -0.75,
        "freeze": -2.0,
    }.get(scout_recommendation, 0.0)
    active_scout_delta = (1.5 * scout_feasibility + proof_status_bonus + recommendation_bonus) if scout_active else 0.0
    priority = (
        3.0 * feasibility_score
        + 2.0 * formalization_score
        + 1.5 * reusable_asset_score
        + source_quality_score
        - 2.0 * risk_score
        - expected_hours
        + active_scout_delta
    )
    passive_recommendation = "promote" if priority >= 20 and exact_statement else "source_recover" if not exact_statement else "park"
    recommendation = passive_recommendation
    if scout_active:
        if scout_recommendation == "promote" and exact_statement:
            recommendation = "promote"
        elif scout_recommendation == "formalize_known" and exact_statement:
            recommendation = "formalize_known"
        elif scout_recommendation == "defer_source":
            recommendation = "source_recover"
        elif scout_recommendation == "defer_route":
            recommendation = "park"
        elif scout_recommendation == "freeze":
            recommendation = "freeze"
    primary_blocker = "needs_source" if not exact_statement else ""
    if exact_statement and scout_status == "timeout":
        primary_blocker = "scout_timeout"
    elif exact_statement and scout_status in {"failed", "error"}:
        primary_blocker = "scout_failure"
    elif scout_active and scout_primary_blocker != "unknown":
        primary_blocker = scout_primary_blocker
    return {
        "problem_id": getattr(problem, "problem_id", ""),
        "title": getattr(problem, "title", ""),
        "domain": getattr(problem, "domain", ""),
        "has_exact_statement": exact_statement,
        "feasibility_score": round(feasibility_score, 2),
        "formalization_score": round(formalization_score, 2),
        "reusable_asset_score": round(reusable_asset_score, 2),
        "source_quality_score": round(source_quality_score, 2),
        "shallow_proof_signal_score": round(scout_feasibility, 2),
        "risk_score": round(risk_score, 2),
        "expected_hours_to_result": round(expected_hours, 2),
        "priority": round(priority, 2),
        "primary_blocker": primary_blocker,
        "risk_flags": risk_flags,
        "recommendation": recommendation,
        "source_quality": {
            "score": round(source_quality_score, 2),
            "reference_count": len(references),
            "statement_quality": "exact" if exact_statement else "placeholder",
        },
        "shallow_proof_signal": {
            "score": round(scout_feasibility, 2),
            "recommendation": scout_recommendation,
            "estimated_proof_effort": str(parsed_probe.get("estimated_proof_effort", "not_assessable")),
            "primary_blocker": scout_primary_blocker,
            "proof_attempt_status": proof_attempt_status,
            "next_investment": str(parsed_probe.get("next_investment", "")),
            "backend_status": scout_status,
        },
        "formalization_signal": {
            "score": round(formalization_score, 2),
            "bank_formalized": str(getattr(problem, "formalized", "no")),
            "scout_recommendation": scout_recommendation,
            "scout_primary_blocker": scout_primary_blocker,
        },
    }


@dataclass(frozen=True)
class PortfolioCampaignRunner:
    repo_root: Path
    math_scout_runner: Any | None = None

    def campaign_root(self) -> Path:
        return self.repo_root / DEFAULT_CAMPAIGN_ROOT

    def _get_math_scout_runner(self) -> Any:
        return self.math_scout_runner or MathScoutRunner(repo_root=self.repo_root)

    def run_portfolio_campaign(
        self,
        *,
        bank: Path,
        run_name: str,
        scout_limit: int = 6,
        scout_timeout: int = 600,
        promote_top: int = 2,
        attack_budget: int = 0,
        scout_backend: str = "none",
    ) -> dict[str, Any]:
        campaign_id = slugify(run_name)
        campaign_dir = self.campaign_root() / campaign_id
        campaign_dir.mkdir(parents=True, exist_ok=True)
        problems_dir = campaign_dir / "problems"
        problems_dir.mkdir(parents=True, exist_ok=True)
        all_problems = load_problem_bank(bank)
        scout_limit = max(0, scout_limit)
        generated_at = utc_now_iso()
        math_scout_report_path = campaign_dir / "math_scout_report.json"
        scout_payload = self._run_broad_scout(
            bank=bank,
            campaign_dir=campaign_dir,
            campaign_id=campaign_id,
            run_name=run_name,
            scout_limit=scout_limit,
            scout_timeout=scout_timeout,
            scout_backend=scout_backend,
            output_path=math_scout_report_path,
        )
        scout_entries = self._scout_entries_by_problem(scout_payload)
        problems = self._selected_campaign_problems(all_problems, scout_entries=scout_entries, scout_limit=scout_limit)
        ranking = sorted(
            (_score_problem(problem, scout_entry=scout_entries.get(str(getattr(problem, "problem_id", "")))) for problem in problems),
            key=lambda item: item["priority"],
            reverse=True,
        )
        promotion_queue = [item for item in ranking if item["recommendation"] == "promote"][: max(0, promote_top)]
        parked_queue = [item for item in ranking if item not in promotion_queue]

        manifest = {
            "schema_version": "amra.portfolio_campaign_manifest.v1",
            "campaign_id": campaign_id,
            "run_name": run_name,
            "created_at": generated_at,
            "bank": str(bank),
            "scout_limit": scout_limit,
            "scout_timeout_seconds": scout_timeout,
            "scout_backend": scout_backend,
            "math_scout_report": _relative(math_scout_report_path, self.repo_root),
            "promote_top": promote_top,
            "attack_budget_seconds": attack_budget,
        }
        state = {
            "schema_version": "amra.portfolio_campaign_state.v1",
            "campaign_id": campaign_id,
            "updated_at": generated_at,
            "status": "planned",
            "problem_count": len(problems),
            "promoted_count": len(promotion_queue),
            "parked_count": len(parked_queue),
        }
        scout_report = {
            "schema_version": "amra.scout_report.v1",
            "generated_at": generated_at,
            "mode": "math_scout_runner",
            "status": str(scout_payload.get("status", "unknown")),
            "stop_reason": str(scout_payload.get("stop_reason", "")),
            "backend": scout_backend,
            "math_scout_report": _relative(math_scout_report_path, self.repo_root),
            "processed_problem_count": int(scout_payload.get("processed_problem_count", 0) or 0),
            "problems": ranking,
        }
        evaluator_report = {
            "schema_version": "amra.evaluator_report.v1",
            "generated_at": generated_at,
            "evaluations": ranking,
        }
        active_assignments = PortfolioAttackScheduler(repo_root=self.repo_root).build_active_assignments(
            campaign_dir=campaign_dir,
            promotion_queue=promotion_queue,
            attack_budget_seconds=attack_budget,
            campaign_id=campaign_id,
        )

        for item in ranking:
            problem_dir = problems_dir / str(item["problem_id"])
            for child in ("probe", "evaluation", "promotion", "attack_runs", "formalization_runs", "review"):
                (problem_dir / child).mkdir(parents=True, exist_ok=True)
            scout_entry = scout_entries.get(str(item["problem_id"]))
            probe_artifact = self._write_problem_probe_artifact(
                campaign_dir=campaign_dir,
                problem_dir=problem_dir,
                problem_id=str(item["problem_id"]),
                scout_payload=scout_payload,
                scout_entry=scout_entry,
            )
            item["probe_artifact"] = _relative(probe_artifact, self.repo_root)
            write_json(problem_dir / "evaluation" / "difficulty.json", item)

        write_json(campaign_dir / "campaign_manifest.json", manifest)
        write_json(campaign_dir / "campaign_state.json", state)
        append_jsonl(campaign_dir / "campaign_log.jsonl", {"event": "campaign_created", "at": generated_at, "campaign_id": campaign_id})
        write_json(campaign_dir / "scout_report.json", scout_report)
        write_json(campaign_dir / "evaluator_report.json", evaluator_report)
        write_json(campaign_dir / "ranking.json", {"schema_version": "amra.ranking.v1", "ranking": ranking})
        write_json(campaign_dir / "promotion_queue.json", {"schema_version": "amra.promotion_queue.v1", "items": promotion_queue})
        write_json(campaign_dir / "parked_queue.json", {"schema_version": "amra.parked_queue.v1", "items": parked_queue})
        write_json(campaign_dir / "active_assignments.json", active_assignments)
        self._write_campaign_resume_pack(
            campaign_dir,
            manifest=manifest,
            promotion_queue=promotion_queue,
            parked_queue=parked_queue,
        )
        self._write_final_report(campaign_dir, manifest=manifest, ranking=ranking, promotion_queue=promotion_queue, parked_queue=parked_queue)
        return {
            "schema_version": "amra.portfolio_campaign_result.v1",
            "campaign_id": campaign_id,
            "campaign_dir": _relative(campaign_dir, self.repo_root),
            "manifest": _relative(campaign_dir / "campaign_manifest.json", self.repo_root),
            "ranking": _relative(campaign_dir / "ranking.json", self.repo_root),
            "promotion_queue": _relative(campaign_dir / "promotion_queue.json", self.repo_root),
            "parked_queue": _relative(campaign_dir / "parked_queue.json", self.repo_root),
            "resume_pack": _relative(campaign_dir / "resume_pack.md", self.repo_root),
            "promoted_count": len(promotion_queue),
            "parked_count": len(parked_queue),
        }

    def _run_broad_scout(
        self,
        *,
        bank: Path,
        campaign_dir: Path,
        campaign_id: str,
        run_name: str,
        scout_limit: int,
        scout_timeout: int,
        scout_backend: str,
        output_path: Path,
    ) -> dict[str, Any]:
        runner = self._get_math_scout_runner()
        timeout_per_problem = max(1, scout_timeout // max(1, scout_limit)) if scout_limit else max(1, scout_timeout)
        try:
            scout_kwargs = {
                "bank_path": bank,
                "scout_report_path": None,
                "backend": scout_backend,
                "problem_limit": scout_limit,
                "start_index": 0,
                "time_budget_sec": max(1, scout_timeout),
                "timeout_per_problem_sec": timeout_per_problem,
                "output_path": output_path,
                "run_name": f"{run_name}-broad-scout",
                "run_dir": campaign_dir / "broad_scout",
                "enable_search": False,
                "selection_mode": "ranked",
                "exclude_problem_ids": [],
            }
            try:
                payload = runner.run(**scout_kwargs)
            except TypeError as exc:
                if "run_dir" not in str(exc):
                    raise
                scout_kwargs.pop("run_dir")
                payload = runner.run(**scout_kwargs)
            if not isinstance(payload, dict):
                raise TypeError(f"Scout runner returned {type(payload).__name__}, expected dict.")
            if not output_path.exists():
                write_json(output_path, payload)
            return payload
        except Exception as exc:
            payload = {
                "schema_version": "ara_math.math_scout_report.v1",
                "generated_at": utc_now_iso(),
                "status": "failed",
                "bank_path": str(bank),
                "backend": scout_backend,
                "run_dir": str(campaign_dir / "broad_scout"),
                "problem_limit": scout_limit,
                "timeout_per_problem_sec": timeout_per_problem,
                "entries": [],
                "ranked_candidates": [],
                "processed_problem_count": 0,
                "stop_reason": "scout_runner_exception",
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                "campaign_id": campaign_id,
            }
            write_json(output_path, payload)
            return payload

    def _scout_entries_by_problem(self, scout_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
        entries: dict[str, dict[str, Any]] = {}
        for entry in scout_payload.get("entries", []) or []:
            if not isinstance(entry, dict):
                continue
            problem_id = str(entry.get("problem_id", "")).strip()
            if problem_id and problem_id not in entries:
                entries[problem_id] = entry
        return entries

    def _selected_campaign_problems(
        self,
        problems: list[Any],
        *,
        scout_entries: dict[str, dict[str, Any]],
        scout_limit: int,
    ) -> list[Any]:
        problems_by_id = {str(getattr(problem, "problem_id", "")): problem for problem in problems}
        selected: list[Any] = []
        seen: set[str] = set()
        for problem_id in scout_entries:
            problem = problems_by_id.get(problem_id)
            if problem is None:
                continue
            selected.append(problem)
            seen.add(problem_id)
        for problem in problems:
            problem_id = str(getattr(problem, "problem_id", ""))
            if problem_id in seen:
                continue
            selected.append(problem)
            seen.add(problem_id)
            if len(selected) >= scout_limit:
                break
        return selected[:scout_limit]

    def _write_problem_probe_artifact(
        self,
        *,
        campaign_dir: Path,
        problem_dir: Path,
        problem_id: str,
        scout_payload: dict[str, Any],
        scout_entry: dict[str, Any] | None,
    ) -> Path:
        probe_dir = problem_dir / "probe"
        probe_dir.mkdir(parents=True, exist_ok=True)
        local_artifacts: dict[str, str] = {}
        if scout_entry:
            artifacts = scout_entry.get("artifacts", {})
            if isinstance(artifacts, dict):
                for name, raw_path in artifacts.items():
                    source = Path(str(raw_path))
                    if not source.is_absolute():
                        source = self.repo_root / source
                    destination = probe_dir / Path(str(raw_path)).name
                    if source.exists() and source.is_file():
                        try:
                            if source.resolve() != destination.resolve():
                                shutil.copyfile(source, destination)
                        except FileNotFoundError:
                            pass
                    if destination.exists():
                        local_artifacts[str(name)] = _relative(destination, self.repo_root)
        status = _scout_backend_status(scout_entry)
        payload = {
            "schema_version": "amra.problem_probe_artifact.v1",
            "generated_at": utc_now_iso(),
            "problem_id": problem_id,
            "status": status,
            "math_scout_status": str(scout_payload.get("status", "unknown")),
            "math_scout_stop_reason": str(scout_payload.get("stop_reason", "")),
            "math_scout_report": _relative(campaign_dir / "math_scout_report.json", self.repo_root),
            "scout_entry": scout_entry or {},
            "local_artifacts": local_artifacts,
        }
        error = scout_payload.get("error")
        if error:
            payload["scout_error"] = error
        artifact_path = probe_dir / "scout_probe.json"
        write_json(artifact_path, payload)
        return artifact_path

    def evaluate_problem(self, *, project: Path, run_name: str) -> dict[str, Any]:
        project = project.resolve()
        consolidation = consolidate_project_memory(project, repo_root=self.repo_root)
        evaluator = PortfolioEvaluator(repo_root=self.repo_root)
        payload = evaluator.write_evaluation(project=project, run_name=run_name)
        problem_id = str(payload.get("problem_id") or project.name)
        resume_pack = write_resume_pack(project, problem_id=problem_id)
        indexes = update_global_memory(self.repo_root, project_dir=project, problem_id=problem_id)
        return {**payload, "resume_pack": resume_pack["path"], "indexes": indexes, "memory_consolidation": consolidation}

    def consolidate_problem_memory(self, *, project: Path) -> dict[str, Any]:
        project = project.resolve()
        return consolidate_project_memory(project, repo_root=self.repo_root)

    def consolidate_memory(self, *, project: Path) -> dict[str, Any]:
        return self.consolidate_problem_memory(project=project)

    def harvest_library_candidates(self, *, project: Path, module: str) -> dict[str, Any]:
        project = project.resolve()
        payload = AmraLibraryManager(repo_root=self.repo_root).detect_harvest_candidates(project=project, module=module)
        report_path = project / "review" / "library_harvest_candidates.json"
        write_json(report_path, payload)
        return {**payload, "report_path": str(report_path)}

    def summarize_portfolio_memory(self, *, campaign: Path | None = None) -> dict[str, Any]:
        global_root = self.repo_root / "artifacts" / "global_memory"
        campaign_summary: dict[str, Any] = {}
        if campaign is not None:
            campaign_summary = read_json(campaign / "campaign_state.json", {})
        return {
            "schema_version": "amra.portfolio_memory_summary.v1",
            "generated_at": utc_now_iso(),
            "campaign": campaign_summary,
            "global_memory": {
                "problem_index": str(global_root / "problem_index.json"),
                "claim_index": str(global_root / "claim_index.json"),
                "failed_route_index": str(global_root / "failed_route_index.json"),
                "theorem_asset_index": str(global_root / "theorem_asset_index.json"),
                "difficulty_history": str(global_root / "difficulty_history.jsonl"),
            },
            "available": {
                "problem_index": (global_root / "problem_index.json").exists(),
                "claim_index": (global_root / "claim_index.json").exists(),
                "failed_route_index": (global_root / "failed_route_index.json").exists(),
                "theorem_asset_index": (global_root / "theorem_asset_index.json").exists(),
            },
        }

    def initialize_problem_project(self, *, project: Path, problem_id: str, state: str = "unseen") -> dict[str, Any]:
        project.mkdir(parents=True, exist_ok=True)
        for child in ("proof/sketches", "proof/audits", "proof/blockers", "formal", "runs"):
            (project / child).mkdir(parents=True, exist_ok=True)
        state_payload = append_state_transition(project, problem_id=problem_id, state=state, reason="initialized by AMRA portfolio scaffold")
        memory = initialize_memory(project, problem_id=problem_id)
        resume_pack = write_resume_pack(project, problem_id=problem_id)
        indexes = update_global_memory(self.repo_root, project_dir=project, problem_id=problem_id)
        return {
            "schema_version": "amra.problem_project_init.v1",
            "project": str(project),
            "state": state_payload,
            "memory": memory,
            "resume_pack": resume_pack["path"],
            "indexes": indexes,
        }

    def _write_campaign_resume_pack(
        self,
        campaign_dir: Path,
        *,
        manifest: dict[str, Any],
        promotion_queue: list[dict[str, Any]],
        parked_queue: list[dict[str, Any]],
    ) -> None:
        lines = [
            "# AMRA Portfolio Campaign Resume Pack",
            "",
            "## Campaign",
            "",
            f"- Campaign ID: `{manifest['campaign_id']}`",
            f"- Run name: {manifest['run_name']}",
            f"- Bank: `{manifest['bank']}`",
            f"- Scout limit: `{manifest['scout_limit']}`",
            f"- Attack budget seconds: `{manifest['attack_budget_seconds']}`",
            "",
            "## Promotion Queue",
            "",
        ]
        if not promotion_queue:
            lines.append("- None.")
        for item in sorted(promotion_queue, key=lambda entry: str(entry.get("problem_id", ""))):
            lines.append(
                f"- `{item['problem_id']}` priority={item['priority']} recommendation={item['recommendation']} blocker={item['primary_blocker'] or 'none'}"
            )
        lines.extend(["", "## Parked Or Source Recovery Queue", ""])
        if not parked_queue:
            lines.append("- None.")
        for item in sorted(parked_queue, key=lambda entry: str(entry.get("problem_id", ""))):
            lines.append(
                f"- `{item['problem_id']}` priority={item['priority']} recommendation={item['recommendation']} blocker={item['primary_blocker'] or 'none'}"
            )
        lines.extend(
            [
                "",
                "## Resume Instructions",
                "",
                "- Promote queued problems into isolated problem projects before long proof attempts.",
                "- Check each problem project's `resume_pack.md` before repeating a proof route.",
            ]
        )
        (campaign_dir / "resume_pack.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_final_report(
        self,
        campaign_dir: Path,
        *,
        manifest: dict[str, Any],
        ranking: list[dict[str, Any]],
        promotion_queue: list[dict[str, Any]],
        parked_queue: list[dict[str, Any]],
    ) -> None:
        lines = [
            f"# AMRA Portfolio Campaign: {manifest['run_name']}",
            "",
            f"- Campaign ID: `{manifest['campaign_id']}`",
            f"- Generated: `{manifest['created_at']}`",
            f"- Bank: `{manifest['bank']}`",
            f"- Ranked problems: `{len(ranking)}`",
            f"- Promotion queue: `{len(promotion_queue)}`",
            f"- Parked/source-recovery queue: `{len(parked_queue)}`",
            "",
            "## Top Ranking",
            "",
        ]
        for item in ranking[:10]:
            lines.append(
                f"- `{item['problem_id']}` priority={item['priority']} recommendation={item['recommendation']} blocker={item['primary_blocker'] or 'none'}"
            )
        lines.extend(
            [
                "",
                "## Next Steps",
                "",
                "- Review each `probe/scout_probe.json` before promotion.",
                "- Run independent EvaluatorAgent over durable artifacts.",
                "- Promote only reviewed targets into isolated attack workspaces.",
            ]
        )
        (campaign_dir / "final_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
