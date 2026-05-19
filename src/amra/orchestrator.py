from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from amra.amra_library import LegacyAraLibraryManager as AraLibraryManager
from amra.evaluation.convergence import ConvergencePlanner
from amra.core.context import set_exact_statement
from amra.proof.closure import ClosureProverRunner
from amra.evaluation.evaluator import EvaluatorRunner
from amra.lean.formalization import FormalizationPreparer
from amra.lean.executor import LeanExecutor
from amra.sources.literature import LiteratureHarvester
from amra.proof.attack import MathAttackRunner
from amra.math_scout import MathScoutRunner
from amra.proof.planning import MathPlanner
from amra.proof.proof_system import ProofSystemPlanner
from amra.proof.search import ProofSearchRunner
from amra.problem_banks.registry import DEFAULT_BANK_PATH, get_problem, resolve_bank_path
from amra.review.project_review import MathReviewer
from amra.evaluation.scouting import write_project_intake_artifacts
from amra.writing import MathWriter
from amra.core.workspace import (
    create_project_workspace,
    load_project_manifest,
    read_json,
    record_event,
    set_deliverable_override,
    today_utc,
    update_pipeline_status,
    write_json,
)


class MathResearchOrchestrator:
    def __init__(
        self,
        *,
        repo_root: Path | None = None,
        projects_root: Path | None = None,
        bank_path: Path | None = None,
        bank_name: str | None = None,
        formal_math_root: Path | None = None,
        allow_network: bool = False,
    ) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[2]
        self.projects_root = projects_root or (self.repo_root / "projects")
        self.bank_path = bank_path or DEFAULT_BANK_PATH
        self.bank_name = bank_name
        self.formal_math_root = formal_math_root or (self.repo_root.parent / "formal-math")
        self.allow_network = allow_network
        self.planner = MathPlanner()
        self.proof_system_planner = ProofSystemPlanner()
        self.formalization_preparer = FormalizationPreparer()
        self.lean_executor = LeanExecutor()
        self.literature_harvester = LiteratureHarvester(formal_math_root=self.formal_math_root)
        self.ara_library_manager = AraLibraryManager(repo_root=self.repo_root)
        self.math_attack_runner = MathAttackRunner(repo_root=self.repo_root)
        self.math_scout_runner = MathScoutRunner(repo_root=self.repo_root)
        self.proof_search_runner = ProofSearchRunner(repo_root=self.repo_root)
        self.closure_prover_runner = ClosureProverRunner(repo_root=self.repo_root)
        self.evaluator_runner = EvaluatorRunner()
        self.writer = MathWriter()
        self.reviewer = MathReviewer()
        self.convergence_planner = ConvergencePlanner()

    def _problem_bank_candidates(self, manifest: dict[str, Any]) -> list[Path]:
        problem_bank = manifest.get("problem_bank", {})
        candidates = [Path(self.bank_path)]
        bank_hint = str(problem_bank.get("path", "")).strip()
        if bank_hint:
            candidates.append(Path(bank_hint))
        if problem_bank.get("name"):
            try:
                candidates.append(resolve_bank_path(bank_name=str(problem_bank["name"])))
            except KeyError:
                pass
        candidates.append(DEFAULT_BANK_PATH)
        deduped: list[Path] = []
        seen: set[str] = set()
        for candidate in candidates:
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(candidate)
        return deduped

    def _load_problem_for_manifest(self, manifest: dict[str, Any]) -> Any:
        problem_id = str(manifest["problem"]["problem_id"])
        for bank_path in self._problem_bank_candidates(manifest):
            try:
                return get_problem(problem_id, bank_path)
            except KeyError:
                continue
        raise KeyError(f"Problem '{problem_id}' was not found in any known bank for this project.")

    def _write_project_intake(self, project_dir: Path, problem: Any) -> dict[str, Any]:
        return write_project_intake_artifacts(
            project_dir=project_dir,
            problem=problem,
            formal_math_root=self.formal_math_root if self.formal_math_root.exists() else None,
        )

    def _refresh_route_artifacts(self, project_dir: Path, problem: Any) -> dict[str, Any]:
        intake = self._write_project_intake(project_dir, problem)
        literature = self.harvest_literature(project_dir)
        intake = self._write_project_intake(project_dir, problem)
        paper_inventory = read_json(project_dir / "idea" / "paper_inventory.json", default={})
        theorem_inventory = self.planner.build_theorem_inventory(
            problem=problem,
            proof_path_assessment=intake["proof_path_assessment"],
            paper_inventory=paper_inventory,
        )
        proof_path_frameworks = self.planner.build_proof_path_frameworks(
            problem=problem,
            proof_path_assessment=intake["proof_path_assessment"],
            theorem_inventory=theorem_inventory,
        )
        theorem_graph = self.planner.build_theorem_graph(
            problem=problem,
            theorem_inventory=theorem_inventory,
            proof_path_frameworks=proof_path_frameworks,
        )
        route_candidates = self.planner.build_route_candidates(
            problem=problem,
            theorem_inventory=theorem_inventory,
            theorem_graph=theorem_graph,
            proof_path_frameworks=proof_path_frameworks,
            proof_path_assessment=intake["proof_path_assessment"],
        )
        route_scaffold = self.planner.build_route_scaffold(
            problem=problem,
            theorem_inventory=theorem_inventory,
            proof_path_frameworks=proof_path_frameworks,
        )
        route_discovery_brief = self.planner.build_route_discovery_brief(
            problem=problem,
            theorem_inventory=theorem_inventory,
            proof_path_frameworks=proof_path_frameworks,
            route_scaffold=route_scaffold,
            proof_path_assessment=intake["proof_path_assessment"],
        )
        mathematical_blockers = self.planner.build_mathematical_blockers(
            problem=problem,
            theorem_inventory=theorem_inventory,
            route_candidates=route_candidates,
        )
        selected_route_markdown = self.planner.render_selected_route_markdown(
            problem=problem,
            theorem_inventory=theorem_inventory,
            route_candidates=route_candidates,
            mathematical_blockers=mathematical_blockers,
        )
        checkpoint_contract = self.planner.build_checkpoint_contract(
            problem=problem,
            theorem_inventory=theorem_inventory,
            route_candidates=route_candidates,
            route_scaffold=route_scaffold,
        )
        checkpoint_contract_markdown = self.planner.render_checkpoint_contract_markdown(contract=checkpoint_contract)
        write_json(project_dir / "proof" / "theorem_inventory.json", theorem_inventory)
        write_json(project_dir / "proof" / "theorem_graph.json", theorem_graph)
        write_json(project_dir / "proof" / "proof_path_frameworks.json", proof_path_frameworks)
        write_json(project_dir / "proof" / "route_candidates.json", route_candidates)
        write_json(project_dir / "proof" / "proof_route_scaffold.json", route_scaffold)
        write_json(project_dir / "proof" / "route_discovery_brief.json", route_discovery_brief)
        write_json(project_dir / "proof" / "mathematical_blockers.json", mathematical_blockers)
        write_json(project_dir / "proof" / "checkpoint_contract.json", checkpoint_contract)
        (project_dir / "proof" / "selected_route.md").write_text(selected_route_markdown, encoding="utf-8")
        (project_dir / "proof" / "checkpoint_contract.md").write_text(checkpoint_contract_markdown, encoding="utf-8")
        return {
            "intake": intake,
            "literature": literature,
            "theorem_inventory": theorem_inventory,
            "theorem_graph": theorem_graph,
            "proof_path_frameworks": proof_path_frameworks,
            "route_candidates": route_candidates,
            "route_scaffold": route_scaffold,
            "route_discovery_brief": route_discovery_brief,
            "mathematical_blockers": mathematical_blockers,
            "checkpoint_contract": checkpoint_contract,
        }

    def create_project(self, *, problem_id: str, name: str | None = None) -> Path:
        problem = get_problem(problem_id, self.bank_path)
        project_name = name or f"{problem.problem_id}-{today_utc()}"
        project_dir = create_project_workspace(
            repo_root=self.repo_root,
            projects_root=self.projects_root,
            project_name=project_name,
            problem=problem,
        )
        manifest = load_project_manifest(project_dir)
        manifest["problem_bank"] = {
            "path": str(self.bank_path),
            "name": self.bank_name or "",
        }
        write_json(project_dir / "project_manifest.json", manifest)
        self._write_project_intake(project_dir, problem)
        return project_dir

    def plan_project(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        problem = self._load_problem_for_manifest(manifest)
        route_artifacts = self._refresh_route_artifacts(project_dir, problem)
        intake = route_artifacts["intake"]
        literature = route_artifacts["literature"]
        theorem_inventory = route_artifacts["theorem_inventory"]
        theorem_graph = route_artifacts["theorem_graph"]
        proof_path_frameworks = route_artifacts["proof_path_frameworks"]
        route_candidates = route_artifacts["route_candidates"]
        route_scaffold = route_artifacts["route_scaffold"]
        route_discovery_brief = route_artifacts["route_discovery_brief"]
        mathematical_blockers = route_artifacts["mathematical_blockers"]
        checkpoint_contract = route_artifacts["checkpoint_contract"]
        plan = self.planner.build_plan(
            project_name=str(manifest["project_name"]),
            problem=problem,
            proof_path_assessment=intake["proof_path_assessment"],
            theorem_inventory=theorem_inventory,
            proof_path_frameworks=proof_path_frameworks,
            route_candidates=route_candidates,
            mathematical_blockers=mathematical_blockers,
        )
        write_json(project_dir / "proof" / "proof_plan.json", plan.to_dict())
        write_json(
            project_dir / "proof" / "claim_registry.json",
            {
                "generated_at": plan.generated_at,
                "claims": [claim.to_dict() for claim in plan.claims],
            },
        )
        benchmark_report = self.proof_system_planner.build_benchmark_report(
            manifest=manifest,
            proof_path_assessment=intake["proof_path_assessment"],
            theorem_inventory=theorem_inventory,
            theorem_graph=theorem_graph,
            proof_path_frameworks=proof_path_frameworks,
            route_scaffold=route_scaffold,
            route_discovery_brief=route_discovery_brief,
            checkpoint_contract=checkpoint_contract,
        )
        write_json(project_dir / "proof" / "proof_system_benchmark.json", benchmark_report)
        (project_dir / "proof" / "proof_system_benchmark.md").write_text(
            self.proof_system_planner.render_benchmark_markdown(report=benchmark_report),
            encoding="utf-8",
        )
        update_pipeline_status(
            project_dir,
            stage="planning",
            status="completed",
            details={
                "task_count": len(plan.tasks),
                "claim_count": len(plan.claims),
                "readiness_tier": intake["proof_path_assessment"]["readiness_tier"],
                "literature_snapshot_count": literature["snapshot_count"],
                "theorem_inventory_count": int(theorem_inventory.get("entry_count", 0)),
                "theorem_graph_node_count": int(route_artifacts["theorem_graph"].get("node_count", 0)),
                "framework_count": int(proof_path_frameworks.get("framework_count", 0)),
                "route_candidate_count": int(route_candidates.get("candidate_count", 0)),
                "literature_evidence_count": sum(
                    int(value) for value in literature.get("evidence", {}).get("counts", {}).values()
                ),
            },
        )
        record_event(
            project_dir,
            stage="planning",
            event="proof_plan_generated",
            details={
                "task_count": len(plan.tasks),
                "claim_count": len(plan.claims),
                "readiness_tier": intake["proof_path_assessment"]["readiness_tier"],
                "literature_snapshot_count": literature["snapshot_count"],
                "theorem_inventory_count": int(theorem_inventory.get("entry_count", 0)),
                "theorem_graph_node_count": int(route_artifacts["theorem_graph"].get("node_count", 0)),
                "framework_count": int(proof_path_frameworks.get("framework_count", 0)),
                "route_candidate_count": int(route_candidates.get("candidate_count", 0)),
                "literature_evidence_count": sum(
                    int(value) for value in literature.get("evidence", {}).get("counts", {}).values()
                ),
            },
        )
        return plan.to_dict()

    def discover_proof_route(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        problem = self._load_problem_for_manifest(manifest)
        route_artifacts = self._refresh_route_artifacts(project_dir, problem)
        theorem_inventory = route_artifacts["theorem_inventory"]
        theorem_graph = route_artifacts["theorem_graph"]
        route_candidates = route_artifacts["route_candidates"]
        mathematical_blockers = route_artifacts["mathematical_blockers"]
        selected_route_id = str(route_candidates.get("selected_route_id", "")).strip()
        candidate_list = list(route_candidates.get("candidates", []))
        selected_route = next(
            (candidate for candidate in candidate_list if candidate.get("route_id") == selected_route_id),
            candidate_list[0] if candidate_list else {},
        ) or {}
        payload = {
            "generated_at": route_candidates.get("generated_at", ""),
            "project_name": manifest.get("project_name", project_dir.name),
            "problem_id": problem.problem_id,
            "selected_route_id": selected_route_id,
            "selected_route_title": selected_route.get("title", ""),
            "theorem_inventory_count": int(theorem_inventory.get("entry_count", 0)),
            "theorem_graph_node_count": int(theorem_graph.get("node_count", 0)),
            "theorem_graph_edge_count": int(theorem_graph.get("edge_count", 0)),
            "route_candidate_count": int(route_candidates.get("candidate_count", 0)),
            "ready_for_formalization": bool(selected_route.get("ready_for_formalization", False)),
            "primary_mathematical_blocker_count": int(mathematical_blockers.get("blocker_count", 0)),
            "selected_route_markdown_path": str(project_dir / "proof" / "selected_route.md"),
        }
        update_pipeline_status(
            project_dir,
            stage="paper_first_route",
            status="completed",
            details=payload,
        )
        record_event(
            project_dir,
            stage="paper_first_route",
            event="proof_route_discovered",
            details=payload,
        )
        return payload

    def set_project_statement(self, project_dir: Path, statement_text: str, source: str = "") -> dict[str, Any]:
        context = set_exact_statement(project_dir, statement_text, source=source)
        update_pipeline_status(
            project_dir,
            stage="context",
            status="updated",
            details={"exact_statement_source": source},
        )
        record_event(
            project_dir,
            stage="context",
            event="exact_statement_updated",
            details={"exact_statement_source": source},
        )
        return context

    def set_project_deliverable(self, project_dir: Path, *, mode: str, reason: str = "") -> dict[str, Any]:
        override = set_deliverable_override(project_dir, mode=mode, reason=reason)
        update_pipeline_status(
            project_dir,
            stage="deliverable",
            status="updated",
            details={"mode": override["mode"], "reason": override["reason"]},
        )
        record_event(
            project_dir,
            stage="deliverable",
            event="deliverable_override_updated",
            details={"mode": override["mode"], "reason": override["reason"]},
        )
        return override

    def harvest_literature(self, project_dir: Path, *, allow_network: bool | None = None) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        problem = self._load_problem_for_manifest(manifest)
        report = self.literature_harvester.harvest(
            project_dir,
            problem,
            allow_network=self.allow_network if allow_network is None else allow_network,
        )
        update_pipeline_status(
            project_dir,
            stage="literature",
            status="completed",
            details={
                "snapshot_count": report["snapshot_count"],
                "recovered_statement_status": report["recovered_statement"]["status"],
                "literature_evidence_count": sum(int(value) for value in report.get("evidence", {}).get("counts", {}).values()),
                "downloaded_paper_count": int(report.get("paper_inventory", {}).get("downloaded_pdf_count", 0)),
            },
        )
        record_event(
            project_dir,
            stage="literature",
            event="literature_harvested",
            details={
                "snapshot_count": report["snapshot_count"],
                "recovered_statement_status": report["recovered_statement"]["status"],
                "literature_evidence_count": sum(int(value) for value in report.get("evidence", {}).get("counts", {}).values()),
                "downloaded_paper_count": int(report.get("paper_inventory", {}).get("downloaded_pdf_count", 0)),
            },
        )
        return report

    def prepare_formal(self, project_dir: Path) -> dict[str, Any]:
        return self.formalization_preparer.prepare(project_dir)

    def build_lean(self, project_dir: Path, timeout_sec: int | None = None) -> dict[str, Any]:
        report = self.lean_executor.build(project_dir, timeout_sec=timeout_sec)
        write_json(project_dir / "artifacts" / "lean_build_report.json", report.to_dict())
        update_pipeline_status(
            project_dir,
            stage="lean",
            status=report.status,
            details={
                "sorry_count": report.sorry_count,
                "summary": report.summary,
                "reuse_status": report.reuse_report.get("status", ""),
                "reuse_source": report.reuse_report.get("selected_source", ""),
            },
        )
        record_event(
            project_dir,
            stage="lean",
            event="lean_build_completed",
            details={"status": report.status, "sorry_count": report.sorry_count},
        )
        return report.to_dict()

    def init_ara_library(self) -> dict[str, Any]:
        return self.ara_library_manager.ensure_library()

    def list_ara_library(self) -> dict[str, Any]:
        return self.ara_library_manager.inventory()

    def add_ara_library_module(
        self,
        *,
        module_name: str,
        imports: list[str] | None = None,
        title: str = "",
        domain: str = "",
        status: str = "candidate",
        tags: list[str] | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        return self.ara_library_manager.add_module(
            module_name=module_name,
            imports=imports,
            title=title,
            domain=domain,
            status=status,
            tags=tags,
            description=description,
        )

    def promote_to_ara_library(
        self,
        *,
        source_file: Path,
        module_name: str,
        declarations: list[str],
        imports: list[str] | None = None,
        title: str = "",
        domain: str = "",
        status: str = "candidate",
        tags: list[str] | None = None,
        description: str = "",
        source_project: Path | None = None,
    ) -> dict[str, Any]:
        return self.ara_library_manager.promote_declarations(
            source_file=source_file,
            module_name=module_name,
            declarations=declarations,
            imports=imports,
            title=title,
            domain=domain,
            status=status,
            tags=tags,
            description=description,
            source_project=source_project,
        )

    def build_ara_library(self, *, timeout_sec: int | None = None, allow_cold_cache: bool = False) -> dict[str, Any]:
        return self.ara_library_manager.build(timeout_sec=timeout_sec, allow_cold_cache=allow_cold_cache)

    def write_manuscript(self, project_dir: Path) -> dict[str, Any]:
        return self.writer.write_manuscript(project_dir)

    def run_evaluator(self, project_dir: Path, *, timeout_sec: int | None = None, auto: bool = False) -> dict[str, Any]:
        support = self.proof_search_runner._prepare_support_artifacts(project_dir=project_dir, orchestrator=self)
        report = self.evaluator_runner.run(
            project_dir,
            evaluator_plan=support["evaluator_plan"],
            counterexample_contract=support["counterexample_contract"],
            timeout_sec=timeout_sec,
            auto=auto,
        )
        update_pipeline_status(
            project_dir,
            stage="evaluator",
            status=report["status"],
            details={
                "mode": report.get("mode", ""),
                "evaluator_mode": report.get("evaluator_mode", ""),
                "command_source": report.get("command_source", ""),
            },
        )
        record_event(
            project_dir,
            stage="evaluator",
            event="evaluator_completed",
            details={
                "status": report.get("status", ""),
                "mode": report.get("mode", ""),
                "command_source": report.get("command_source", ""),
            },
        )
        return report

    def run_math_attack(
        self,
        project_dir: Path,
        *,
        target: str = "",
        context_paths: list[Path] | None = None,
        evidence_command: list[str] | None = None,
        evidence_cwd: Path | None = None,
        evidence_timeout_sec: int = 120,
        backend: str = "codex",
        iterations: int = 3,
        time_budget_sec: int = 900,
        iteration_timeout_sec: int = 180,
        sleep_seconds: int = 0,
        sleep_mode: str = "adaptive",
        min_sleep_seconds: int | None = None,
        max_sleep_seconds: int | None = None,
        sleep_jitter_seconds: int | None = None,
        launch_spacing_seconds: int | None = None,
        run_name: str | None = None,
        enable_search: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        report = self.math_attack_runner.run(
            project_dir=project_dir,
            target=target,
            context_paths=context_paths,
            evidence_command=evidence_command,
            evidence_cwd=evidence_cwd,
            evidence_timeout_sec=evidence_timeout_sec,
            backend=backend,
            iterations=iterations,
            time_budget_sec=time_budget_sec,
            iteration_timeout_sec=iteration_timeout_sec,
            sleep_seconds=sleep_seconds,
            sleep_mode=sleep_mode,
            min_sleep_seconds=min_sleep_seconds,
            max_sleep_seconds=max_sleep_seconds,
            sleep_jitter_seconds=sleep_jitter_seconds,
            launch_spacing_seconds=launch_spacing_seconds,
            run_name=run_name,
            enable_search=enable_search,
            dry_run=dry_run,
        )
        update_pipeline_status(
            project_dir,
            stage="math_attack",
            status=report["status"],
            details={
                "backend": backend,
                "iterations_completed": report.get("iterations_completed", 0),
                "run_dir": report.get("run_dir", ""),
                "target": report.get("target", ""),
            },
        )
        record_event(
            project_dir,
            stage="math_attack",
            event="math_attack_completed",
            details={
                "status": report["status"],
                "backend": backend,
                "iterations_completed": report.get("iterations_completed", 0),
                "run_dir": report.get("run_dir", ""),
            },
        )
        return report

    def review_project(self, project_dir: Path) -> dict[str, Any]:
        report = self.reviewer.review(project_dir)
        convergence = self.plan_convergence(project_dir)
        report["convergence_phase"] = convergence["phase"]
        report["ready_for_long_run"] = convergence["ready_for_long_run"]
        report["external_requirement_count"] = convergence["external_requirement_count"]
        return report

    def plan_convergence(self, project_dir: Path) -> dict[str, Any]:
        return self.convergence_planner.plan(project_dir)

    def plan_proof_system(self, project_dir: Path) -> dict[str, Any]:
        payload = self.proof_search_runner.plan_execution(project_dir=project_dir, orchestrator=self)
        update_pipeline_status(
            project_dir,
            stage="proof_system",
            status="planned",
            details={
                "search_policy": payload["proof_search_agenda"].get("search_policy", ""),
                "execution_mode": payload["proof_search_agenda"].get("execution_mode", ""),
                "selected_agenda_item_id": payload["proof_search_agenda"].get("selected_item_id", ""),
            },
        )
        record_event(
            project_dir,
            stage="proof_system",
            event="proof_system_planned",
            details={
                "search_policy": payload["proof_search_agenda"].get("search_policy", ""),
                "execution_mode": payload["proof_search_agenda"].get("execution_mode", ""),
                "selected_agenda_item_id": payload["proof_search_agenda"].get("selected_item_id", ""),
            },
        )
        return payload

    def run_proof_search(
        self,
        project_dir: Path,
        *,
        backend: str = "codex",
        max_attempts: int = 3,
        max_runtime_sec: int = 900,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        focus_mode: str = "default",
    ) -> dict[str, Any]:
        payload = self.proof_search_runner.run_project(
            project_dir=project_dir,
            orchestrator=self,
            backend=backend,
            max_attempts=max_attempts,
            max_runtime_sec=max_runtime_sec,
            attempt_timeout_sec=attempt_timeout_sec,
            build_timeout_sec=build_timeout_sec,
            focus_mode=focus_mode,
        )
        update_pipeline_status(
            project_dir,
            stage="proof_search",
            status=payload["status"],
            details={
                "backend": backend,
                "attempts_completed": payload.get("attempts_completed", 0),
                "focus_mode": focus_mode,
            },
        )
        record_event(
            project_dir,
            stage="proof_search",
            event="proof_search_completed",
            details={
                "status": payload["status"],
                "backend": backend,
                "attempts_completed": payload.get("attempts_completed", 0),
                "focus_mode": focus_mode,
            },
        )
        return payload

    def run_closure_prover(
        self,
        project_dir: Path,
        *,
        target_theorem: str | None,
        target_file: Path | None = None,
        backend: str = "codex",
        max_attempts: int = 3,
        max_runtime_sec: int = 900,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        max_stalled_attempts: int = 2,
        rollback_failed_attempts: bool = False,
    ) -> dict[str, Any]:
        payload = self.closure_prover_runner.run(
            project_dir=project_dir,
            orchestrator=self,
            target_theorem=target_theorem,
            target_file=target_file,
            backend=backend,
            max_attempts=max_attempts,
            max_runtime_sec=max_runtime_sec,
            attempt_timeout_sec=attempt_timeout_sec,
            build_timeout_sec=build_timeout_sec,
            max_stalled_attempts=max_stalled_attempts,
            rollback_failed_attempts=rollback_failed_attempts,
        )
        update_pipeline_status(
            project_dir,
            stage="closure_prover",
            status=payload["status"],
            details={
                "backend": backend,
                "target_theorem": target_theorem or "",
                "attempts_completed": payload.get("attempts_completed", 0),
            },
        )
        record_event(
            project_dir,
            stage="closure_prover",
            event="closure_prover_completed",
            details={
                "status": payload["status"],
                "backend": backend,
                "target_theorem": target_theorem or "",
                "attempts_completed": payload.get("attempts_completed", 0),
            },
        )
        return payload

    def run_open_problem_campaign(
        self,
        *,
        scout_report_path: Path,
        limit: int = 3,
        backend: str = "codex",
        max_attempts: int = 2,
        max_runtime_sec: int = 600,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        create_missing: bool = True,
        ) -> dict[str, Any]:
        return self.proof_search_runner.run_campaign(
            orchestrator=self,
            scout_report_path=scout_report_path,
            bank_name=self.bank_name,
            limit=limit,
            backend=backend,
            max_attempts=max_attempts,
            max_runtime_sec=max_runtime_sec,
            attempt_timeout_sec=attempt_timeout_sec,
            build_timeout_sec=build_timeout_sec,
            create_missing=create_missing,
        )

    def _iter_open_projects(self, *, projects_root: Path | None = None) -> list[Path]:
        root = (projects_root or self.projects_root).resolve()
        if not root.exists():
            return []
        project_dirs: list[Path] = []
        for candidate in sorted(root.iterdir()):
            if not candidate.is_dir():
                continue
            manifest_path = candidate / "project_manifest.json"
            if not manifest_path.exists():
                continue
            manifest = read_json(manifest_path, default={})
            if bool((manifest.get("problem") or {}).get("open_problem", False)):
                project_dirs.append(candidate)
        return project_dirs

    def _convergence_candidate_score(
        self,
        *,
        review_report: dict[str, Any],
        convergence_plan: dict[str, Any],
        proof_search_status: dict[str, Any],
    ) -> int:
        score = 0
        review_status = str(review_report.get("status", "")).strip()
        if review_status == "ready_for_human_review":
            score += 40
        elif review_status == "checkpoint_verified":
            score += 30
        elif review_status == "blocked":
            score += 8

        if convergence_plan.get("ready_for_long_run"):
            score += 12
        phase = str(convergence_plan.get("phase", "")).strip()
        if phase in {
            "import_verified_finiteness",
            "strengthen_geometry_shell",
            "fix_quantitative_target",
            "import_quantitative_overlap_bound",
            "import_partial_spectrum_theorem",
            "upgrade_to_density_surrogate",
        }:
            score += 8
        if int(convergence_plan.get("external_requirement_count", 0) or 0) == 0:
            score += 4

        proof_status = str(proof_search_status.get("status", "")).strip()
        if proof_status == "checkpoint":
            score += 9
        elif proof_status == "converged":
            score += 15
        elif proof_status == "exhausted":
            score += 2

        return score

    def run_convergence_campaign(
        self,
        *,
        limit: int = 4,
        backend: str = "auto",
        runtime_multiplier: float = 2.0,
        attempt_multiplier: float = 1.5,
        include_blocked: bool = False,
        include_not_ready: bool = False,
        checkpoint_only: bool = False,
        project_filters: list[str] | None = None,
        model_override: str | None = None,
        reasoning_effort_override: str | None = None,
        rounds: int = 1,
        continue_on_checkpoint: bool = True,
        continue_on_exhausted: bool = False,
    ) -> dict[str, Any]:
        project_filter_set = {item.strip() for item in (project_filters or []) if item and item.strip()}
        candidates: list[dict[str, Any]] = []

        for project_dir in self._iter_open_projects():
            manifest = load_project_manifest(project_dir)
            problem = manifest.get("problem") or {}
            problem_id = str(problem.get("problem_id", "")).strip()
            if project_filter_set and problem_id not in project_filter_set and project_dir.name not in project_filter_set:
                continue

            review_report = self.review_project(project_dir)
            convergence_plan = read_json(project_dir / "artifacts" / "convergence_plan.json", default={})
            proof_search_status = read_json(project_dir / "proof" / "proof_search_status.json", default={})

            review_status = str(review_report.get("status", "")).strip()
            if checkpoint_only and review_status != "checkpoint_verified":
                continue
            if not include_blocked and review_status not in {"checkpoint_verified", "ready_for_human_review"}:
                continue
            if not include_not_ready and not convergence_plan.get("ready_for_long_run", False):
                continue

            candidates.append(
                {
                    "project_dir": project_dir,
                    "project_name": manifest.get("project_name", project_dir.name),
                    "problem_id": problem_id,
                    "review_report": review_report,
                    "convergence_plan": convergence_plan,
                    "proof_search_status": proof_search_status,
                    "score": self._convergence_candidate_score(
                        review_report=review_report,
                        convergence_plan=convergence_plan,
                        proof_search_status=proof_search_status,
                    ),
                }
            )

        candidates.sort(
            key=lambda item: (
                -int(item["score"]),
                str(item["problem_id"]),
                str(item["project_name"]),
            )
        )
        selected = candidates[:limit]

        runner = self.proof_search_runner
        previous_allow_network = self.allow_network
        previous_model = runner.backend_model
        previous_reasoning_effort = runner.backend_reasoning_effort
        previous_backend_cpu_seconds = runner.backend_max_cpu_seconds
        entries: list[dict[str, Any]] = []

        for item in selected:
            project_dir = Path(item["project_dir"])
            round_entries: list[dict[str, Any]] = []
            result: dict[str, Any] = {}
            convergence_plan = item["convergence_plan"]
            for round_index in range(1, max(rounds, 1) + 1):
                convergence_plan = self.plan_convergence(project_dir)
                review_report = read_json(project_dir / "artifacts" / "review_report.json", default={})
                review_status = str(review_report.get("status", "")).strip()
                if review_status == "ready_for_human_review":
                    round_entries.append(
                        {
                            "round": round_index,
                            "status": "skipped",
                            "reason": "project_already_ready_for_human_review",
                        }
                    )
                    break
                if not include_not_ready and not convergence_plan.get("ready_for_long_run", False):
                    round_entries.append(
                        {
                            "round": round_index,
                            "status": "skipped",
                            "reason": "project_not_ready_for_long_run",
                        }
                    )
                    break

                profile = convergence_plan.get("recommended_run_profile", {})
                backend_name = str(profile.get("backend", "codex")).strip() or "codex"
                if backend != "auto":
                    backend_name = backend
                focus_mode = str(profile.get("focus_mode", convergence_plan.get("recommended_focus_mode", "default"))).strip()
                if not focus_mode:
                    focus_mode = "default"

                attempts = max(1, int(math.ceil(float(profile.get("attempts", 1) or 1) * max(attempt_multiplier, 0.1))))
                time_budget_sec = max(
                    60,
                    int(round(float(profile.get("time_budget_sec", 600) or 600) * max(runtime_multiplier, 0.1))),
                )
                attempt_timeout_sec = max(
                    30,
                    int(round(float(profile.get("attempt_timeout_sec", 180) or 180) * max(runtime_multiplier, 0.1))),
                )
                build_timeout_sec = max(
                    30,
                    int(round(float(profile.get("build_timeout_sec", 90) or 90) * max(runtime_multiplier, 0.75))),
                )

                if model_override is not None:
                    runner.backend_model = model_override
                if reasoning_effort_override is not None:
                    runner.backend_reasoning_effort = reasoning_effort_override
                elif profile.get("reasoning_effort"):
                    runner.backend_reasoning_effort = str(profile["reasoning_effort"])
                runner.backend_max_cpu_seconds = max(previous_backend_cpu_seconds, attempt_timeout_sec + 30)
                self.allow_network = previous_allow_network or bool(profile.get("allow_network", False))

                result = self.run_proof_search(
                    project_dir,
                    backend=backend_name,
                    max_attempts=attempts,
                    max_runtime_sec=time_budget_sec,
                    attempt_timeout_sec=attempt_timeout_sec,
                    build_timeout_sec=build_timeout_sec,
                    focus_mode=focus_mode,
                )
                round_entries.append(
                    {
                        "round": round_index,
                        "status": result.get("status", ""),
                        "attempts_completed": result.get("attempts_completed", 0),
                        "elapsed_seconds": result.get("elapsed_seconds", 0.0),
                        "applied_profile": {
                            "backend": backend_name,
                            "attempts": attempts,
                            "time_budget_sec": time_budget_sec,
                            "attempt_timeout_sec": attempt_timeout_sec,
                            "build_timeout_sec": build_timeout_sec,
                            "focus_mode": focus_mode,
                            "model": runner.backend_model,
                            "reasoning_effort": runner.backend_reasoning_effort,
                            "backend_max_cpu_seconds": runner.backend_max_cpu_seconds,
                        },
                    }
                )
                if result.get("status") == "converged":
                    break
                if result.get("status") == "checkpoint" and not continue_on_checkpoint:
                    break
                if result.get("status") == "exhausted" and not continue_on_exhausted:
                    break

            entries.append(
                {
                    "project_dir": str(project_dir),
                    "project_name": item["project_name"],
                    "problem_id": item["problem_id"],
                    "score": item["score"],
                    "review_status": item["review_report"].get("status", ""),
                    "convergence_phase": convergence_plan.get("phase", ""),
                    "ready_for_long_run": convergence_plan.get("ready_for_long_run", False),
                    "rounds_requested": max(rounds, 1),
                    "rounds_completed": len([entry for entry in round_entries if entry.get("status") != "skipped"]),
                    "round_entries": round_entries,
                    "applied_profile": round_entries[-1]["applied_profile"] if round_entries and round_entries[-1].get("applied_profile") else {},
                    "result": result,
                }
            )

        self.allow_network = previous_allow_network
        runner.backend_model = previous_model
        runner.backend_reasoning_effort = previous_reasoning_effort
        runner.backend_max_cpu_seconds = previous_backend_cpu_seconds

        payload = {
            "generated_at": today_utc(),
            "candidate_count": len(candidates),
            "selected_count": len(selected),
            "limit": limit,
            "backend": backend,
            "runtime_multiplier": runtime_multiplier,
            "attempt_multiplier": attempt_multiplier,
            "rounds": max(rounds, 1),
            "continue_on_checkpoint": continue_on_checkpoint,
            "continue_on_exhausted": continue_on_exhausted,
            "entries": entries,
            "candidate_overview": [
                {
                    "problem_id": item["problem_id"],
                    "project_name": item["project_name"],
                    "review_status": item["review_report"].get("status", ""),
                    "convergence_phase": item["convergence_plan"].get("phase", ""),
                    "ready_for_long_run": item["convergence_plan"].get("ready_for_long_run", False),
                    "score": item["score"],
                }
                for item in candidates[: max(limit * 3, 10)]
            ],
        }
        write_json(self.repo_root / "artifacts" / "convergence_campaign.json", payload)
        return payload

    def run_erdos_light_sweep(
        self,
        *,
        backend: str = "codex",
        problem_limit: int | None = None,
        start_index: int = 0,
        max_runtime_sec: int = 3600,
        attempt_timeout_sec: int = 45,
        build_timeout_sec: int = 45,
        create_missing: bool = True,
        allow_backend_without_seed: bool = False,
    ) -> dict[str, Any]:
        return self.proof_search_runner.run_light_sweep(
            orchestrator=self,
            bank_path=self.bank_path,
            bank_name=self.bank_name,
            backend=backend,
            problem_limit=problem_limit,
            start_index=start_index,
            max_runtime_sec=max_runtime_sec,
            attempt_timeout_sec=attempt_timeout_sec,
            build_timeout_sec=build_timeout_sec,
            create_missing=create_missing,
            allow_backend_without_seed=allow_backend_without_seed,
        )

    def run_math_scout(
        self,
        *,
        scout_report_path: Path | None = None,
        backend: str = "codex",
        problem_limit: int | None = None,
        start_index: int = 0,
        time_budget_sec: int = 3600,
        timeout_per_problem_sec: int = 300,
        output_path: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = False,
        selection_mode: str = "ranked",
        exclude_problem_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.math_scout_runner.run(
            bank_path=self.bank_path,
            scout_report_path=scout_report_path,
            backend=backend,
            problem_limit=problem_limit,
            start_index=start_index,
            time_budget_sec=time_budget_sec,
            timeout_per_problem_sec=timeout_per_problem_sec,
            output_path=output_path,
            run_name=run_name,
            enable_search=enable_search,
            selection_mode=selection_mode,
            exclude_problem_ids=exclude_problem_ids,
        )

    def run_pipeline(self, project_dir: Path, timeout_sec: int | None = None) -> dict[str, Any]:
        plan = self.plan_project(project_dir)
        formal = self.prepare_formal(project_dir)
        build_report = self.build_lean(project_dir, timeout_sec=timeout_sec)
        manuscript = self.write_manuscript(project_dir)
        review = self.review_project(project_dir)
        summary = {
            "project_dir": str(project_dir),
            "planning": {
                "task_count": len(plan["tasks"]),
                "claim_count": len(plan["claims"]),
            },
            "formal_preparation": {
                "lean_claim_count": formal["lean_claim_count"],
                "placeholder_claim_count": formal["placeholder_claim_count"],
            },
            "lean": {
                "status": build_report["status"],
                "sorry_count": build_report["sorry_count"],
                "summary": build_report["summary"],
            },
            "writing": {
                "manuscript_path": manuscript["manuscript_path"],
                "claim_count": manuscript["claim_count"],
                "deliverable_type": manuscript["deliverable_type"],
            },
            "review": {
                "status": review["status"],
                "blocker_count": len(review["blockers"]),
                "warning_count": len(review["warnings"]),
                "deliverable_type": review["deliverable_type"],
            },
            "convergence": {
                "phase": review.get("convergence_phase", ""),
                "ready_for_long_run": review.get("ready_for_long_run", False),
                "external_requirement_count": review.get("external_requirement_count", 0),
            },
        }
        write_json(project_dir / "pipeline_results.json", summary)
        record_event(project_dir, stage="pipeline", event="pipeline_completed", details=summary)
        return summary

    def get_status(self, project_dir: Path) -> dict[str, Any]:
        return read_json(project_dir / "pipeline_status.json", default={})
