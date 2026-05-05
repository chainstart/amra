from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path
from typing import Any

from ara_math.banking import sync_local_problem_banks
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import (
    DEFAULT_BANK_PATH,
    import_erdos_open_problems,
    load_bank_registry,
    load_problem_bank,
    refresh_erdos_problem_bank,
    resolve_bank_path,
)
from ara_math.scouting import scout_problem_bank
from ara_math.workspace import today_utc


DELIVERABLE_MODES = ("auto", "research_report", "formalization_note", "paper_candidate")
ARA_LIBRARY_STATUSES = ("candidate", "trusted", "upstream_candidate", "deprecated")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _projects_root() -> Path:
    return _repo_root() / "projects"


def _print(payload: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    if isinstance(payload, str):
        print(payload)
        return
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _selected_bank_path(args: argparse.Namespace) -> Path:
    bank_name = getattr(args, "bank_name", None)
    bank_path = getattr(args, "bank", None)
    if bank_name:
        return resolve_bank_path(bank_name=bank_name)
    return resolve_bank_path(bank_name=bank_name, bank_path=bank_path)


def _add_proof_search_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--focus-mode",
        choices=("default", "route_discovery", "paper_first"),
        default="default",
        help="Route-discovery and paper-first modes prioritize proof-path discovery before local Lean repair.",
    )
    parser.add_argument("--model", default=None, help="Override the proof-search backend model.")
    parser.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")
    parser.add_argument("--backend-max-memory-mb", type=int, default=None)
    parser.add_argument("--backend-max-cpu-seconds", type=int, default=None)
    parser.add_argument("--backend-max-processes", type=int, default=None)
    parser.add_argument("--min-available-memory-mb", type=int, default=None)
    parser.add_argument("--max-load-per-cpu", type=float, default=None)
    parser.add_argument("--system-wait-seconds", type=int, default=None)


def _apply_proof_search_runtime_overrides(orchestrator: MathResearchOrchestrator, args: argparse.Namespace) -> None:
    runner = orchestrator.proof_search_runner
    overrides = {
        "backend_model": getattr(args, "model", None),
        "backend_reasoning_effort": getattr(args, "reasoning_effort", None),
        "backend_max_memory_mb": getattr(args, "backend_max_memory_mb", None),
        "backend_max_cpu_seconds": getattr(args, "backend_max_cpu_seconds", None),
        "backend_max_processes": getattr(args, "backend_max_processes", None),
        "min_available_memory_mb": getattr(args, "min_available_memory_mb", None),
        "max_load_per_cpu": getattr(args, "max_load_per_cpu", None),
        "wait_max_seconds": getattr(args, "system_wait_seconds", None),
    }
    for attr, value in overrides.items():
        if value is not None:
            setattr(runner, attr, value)


def _apply_closure_runtime_overrides(orchestrator: MathResearchOrchestrator, args: argparse.Namespace) -> None:
    runner = orchestrator.closure_prover_runner
    overrides = {
        "backend_model": getattr(args, "model", None),
        "backend_reasoning_effort": getattr(args, "reasoning_effort", None),
        "backend_max_memory_mb": getattr(args, "backend_max_memory_mb", None),
        "backend_max_cpu_seconds": getattr(args, "backend_max_cpu_seconds", None),
        "backend_max_processes": getattr(args, "backend_max_processes", None),
        "min_available_memory_mb": getattr(args, "min_available_memory_mb", None),
        "max_load_per_cpu": getattr(args, "max_load_per_cpu", None),
        "wait_max_seconds": getattr(args, "system_wait_seconds", None),
    }
    for attr, value in overrides.items():
        if value is not None:
            setattr(runner, attr, value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARA Math CLI")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_banks = subparsers.add_parser("list-banks", help="List registered problem banks.")
    list_banks.add_argument("--registry", type=Path, default=None)

    list_problems = subparsers.add_parser("list-problems", help="List available problems.")
    list_problems.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    list_problems.add_argument("--bank-name")

    import_bank = subparsers.add_parser("import-erdos-bank", help="Normalize the local Erdős metadata file.")
    import_bank.add_argument("--source", type=Path, required=True)
    import_bank.add_argument("--output", type=Path, required=True)

    refresh_bank = subparsers.add_parser(
        "refresh-erdos-status",
        help="Refresh Erdős-bank open/solved status using official pages and arXiv solution signals.",
    )
    refresh_bank.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    refresh_bank.add_argument("--bank-name")
    refresh_bank.add_argument("--output", type=Path, default=None)
    refresh_bank.add_argument("--problem-id", default=None)

    sync_banks = subparsers.add_parser("sync-local-banks", help="Generate registered banks from the local formal-math workspace.")
    sync_banks.add_argument("--formal-math-root", type=Path, required=True)
    sync_banks.add_argument("--data-root", type=Path, default=None)
    sync_banks.add_argument("--registry-output", type=Path, default=None)

    init_ara_library = subparsers.add_parser(
        "init-ara-library",
        help="Create the reusable local Lean library for mathlib gaps and staged contributions.",
    )

    add_ara_library = subparsers.add_parser(
        "add-ara-library-module",
        help="Create or register a reusable ARA Lean library module.",
    )
    add_ara_library.add_argument("--module-name", required=True, help="Lean module name, e.g. AraLibrary.NumberTheory.Carmichael.")
    add_ara_library.add_argument("--import", dest="imports", action="append", default=[], help="Lean import to add to the module.")
    add_ara_library.add_argument("--title", default="")
    add_ara_library.add_argument("--domain", default="")
    add_ara_library.add_argument("--status", choices=ARA_LIBRARY_STATUSES, default="candidate")
    add_ara_library.add_argument("--tag", dest="tags", action="append", default=[])
    add_ara_library.add_argument("--description", default="")

    promote_ara_library = subparsers.add_parser(
        "promote-to-ara-library",
        help="Promote selected Lean declarations from a project file into the reusable ARA library.",
    )
    promote_ara_library.add_argument("--source-file", type=Path, required=True)
    promote_ara_library.add_argument("--source-project", type=Path, default=None)
    promote_ara_library.add_argument("--module-name", required=True, help="Lean module name, e.g. AraLibrary.NumberTheory.Carmichael.")
    promote_ara_library.add_argument("--declaration", dest="declarations", action="append", required=True)
    promote_ara_library.add_argument("--import", dest="imports", action="append", default=[], help="Lean import to add to the module.")
    promote_ara_library.add_argument("--title", default="")
    promote_ara_library.add_argument("--domain", default="")
    promote_ara_library.add_argument("--status", choices=ARA_LIBRARY_STATUSES, default="candidate")
    promote_ara_library.add_argument("--tag", dest="tags", action="append", default=[])
    promote_ara_library.add_argument("--description", default="")

    list_ara_library = subparsers.add_parser("list-ara-library", help="List reusable ARA Lean library modules.")

    build_ara_library = subparsers.add_parser("build-ara-library", help="Build the reusable ARA Lean library.")
    build_ara_library.add_argument("--timeout", type=int, default=600)
    build_ara_library.add_argument("--allow-cold-cache", action="store_true")

    new_project = subparsers.add_parser("new-project", help="Create a new math research project.")
    new_project.add_argument("--problem", required=True, help="Problem id from the selected bank.")
    new_project.add_argument("--name", help="Optional explicit project name.")
    new_project.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    new_project.add_argument("--bank-name")
    new_project.add_argument("--projects-root", type=Path, default=_projects_root())

    set_statement = subparsers.add_parser("set-statement", help="Provide the exact mathematical statement for a project.")
    set_statement.add_argument("--project", type=Path, required=True)
    set_statement.add_argument("--statement-file", type=Path, required=True)
    set_statement.add_argument("--source", default="")

    set_deliverable = subparsers.add_parser(
        "set-deliverable",
        help="Override deliverable routing for a project or restore automatic assessment.",
    )
    set_deliverable.add_argument("--project", type=Path, required=True)
    set_deliverable.add_argument("--mode", choices=DELIVERABLE_MODES, required=True)
    set_deliverable.add_argument("--reason", default="")

    plan = subparsers.add_parser("plan", help="Generate a proof plan for a project.")
    plan.add_argument("--project", type=Path, required=True)
    plan.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    plan.add_argument("--bank-name")
    plan.add_argument("--allow-network", action="store_true")

    discover_route = subparsers.add_parser(
        "discover-proof-route",
        help="Run paper-first theorem-graph and route discovery without entering Lean proof repair.",
    )
    discover_route.add_argument("--project", type=Path, required=True)
    discover_route.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    discover_route.add_argument("--bank-name")
    discover_route.add_argument("--allow-network", action="store_true")

    prepare = subparsers.add_parser("prepare-formal", help="Generate Lean claim stubs and formalization artifacts.")
    prepare.add_argument("--project", type=Path, required=True)

    convergence = subparsers.add_parser("plan-convergence", help="Generate a convergence plan and external requirement report.")
    convergence.add_argument("--project", type=Path, required=True)

    proof_system = subparsers.add_parser(
        "plan-proof-system",
        help="Generate proof-system benchmark, verifier-feedback, and best-first search agenda artifacts.",
    )
    proof_system.add_argument("--project", type=Path, required=True)

    run_evaluator = subparsers.add_parser(
        "run-evaluator",
        help="Run a bounded evaluator command or local search script for a project.",
    )
    run_evaluator.add_argument("--project", type=Path, required=True)
    run_evaluator.add_argument("--timeout", type=int, default=None)
    run_evaluator.add_argument("--auto", action="store_true", help="Honor evaluator auto-run gating instead of forcing a manual run.")

    math_attack = subparsers.add_parser(
        "run-math-attack",
        help="Run a math-only single-target attack loop before Lean formalization.",
    )
    math_attack.add_argument("--project", type=Path, required=True)
    math_attack.add_argument("--target", default="", help="Specific theorem, branch, or obstruction to attack.")
    math_attack.add_argument("--context-file", type=Path, action="append", default=[])
    math_attack.add_argument(
        "--evidence-command",
        default="",
        help="Optional local evidence command, parsed with shell-like quoting but run without a shell.",
    )
    math_attack.add_argument("--evidence-cwd", type=Path, default=None)
    math_attack.add_argument("--evidence-timeout", type=int, default=120)
    math_attack.add_argument("--backend", choices=("codex", "none"), default="codex")
    math_attack.add_argument("--iterations", type=int, default=3)
    math_attack.add_argument("--time-budget", type=int, default=900)
    math_attack.add_argument("--iteration-timeout", type=int, default=180)
    math_attack.add_argument("--sleep-seconds", type=int, default=0)
    math_attack.add_argument(
        "--sleep-mode",
        choices=("adaptive", "fixed", "none"),
        default="adaptive",
        help="Pacing between iterations. Adaptive treats --sleep-seconds as a cap and backs off on rate/usage failures.",
    )
    math_attack.add_argument("--min-sleep-seconds", type=int, default=None)
    math_attack.add_argument("--max-sleep-seconds", type=int, default=None)
    math_attack.add_argument("--sleep-jitter-seconds", type=int, default=None)
    math_attack.add_argument(
        "--launch-spacing-seconds",
        type=int,
        default=None,
        help="Optional cross-process minimum spacing between backend launches.",
    )
    math_attack.add_argument("--run-name", default=None)
    math_attack.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    math_attack.add_argument("--dry-run", action="store_true", help="Build artifacts and prompts without invoking the backend.")
    math_attack.add_argument("--model", default=None, help="Override the math-attack backend model.")
    math_attack.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    harvest = subparsers.add_parser("harvest-literature", help="Collect local and remote reference snapshots for a project.")
    harvest.add_argument("--project", type=Path, required=True)
    harvest.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    harvest.add_argument("--bank-name")
    harvest.add_argument("--allow-network", action="store_true")

    build = subparsers.add_parser("build-lean", help="Run `lake build` and audit `sorry` placeholders.")
    build.add_argument("--project", type=Path, required=True)
    build.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    build.add_argument("--bank-name")
    build.add_argument("--timeout", type=int, default=600)
    build.add_argument("--allow-cold-cache", action="store_true")

    proof_search = subparsers.add_parser(
        "run-proof-search",
        help="Run an autonomous proof-search / proof-repair loop for a project.",
    )
    proof_search.add_argument("--project", type=Path, required=True)
    proof_search.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    proof_search.add_argument("--bank-name")
    proof_search.add_argument("--backend", choices=("codex", "none"), default="codex")
    proof_search.add_argument("--attempts", type=int, default=3)
    proof_search.add_argument("--time-budget", type=int, default=900)
    proof_search.add_argument("--attempt-timeout", type=int, default=180)
    proof_search.add_argument("--build-timeout", type=int, default=90)
    proof_search.add_argument("--allow-cold-cache", action="store_true")
    proof_search.add_argument("--allow-network", action="store_true")
    _add_proof_search_runtime_args(proof_search)

    closure_prover = subparsers.add_parser(
        "run-closure-prover",
        help="Run a strict Lean-verified closure loop for one target theorem.",
    )
    closure_prover.add_argument("--project", type=Path, required=True)
    closure_prover.add_argument("--target-theorem", required=False, default=None)
    closure_prover.add_argument("--target-file", type=Path, default=None)
    closure_prover.add_argument("--backend", choices=("codex", "none"), default="codex")
    closure_prover.add_argument("--attempts", type=int, default=3)
    closure_prover.add_argument("--time-budget", type=int, default=900)
    closure_prover.add_argument("--attempt-timeout", type=int, default=180)
    closure_prover.add_argument("--build-timeout", type=int, default=90)
    closure_prover.add_argument("--max-stalled-attempts", type=int, default=2)
    closure_prover.add_argument("--rollback-failed-attempts", action="store_true")
    closure_prover.add_argument("--allow-cold-cache", action="store_true")
    closure_prover.add_argument("--model", default=None, help="Override the closure backend model.")
    closure_prover.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")
    closure_prover.add_argument("--backend-max-memory-mb", type=int, default=None)
    closure_prover.add_argument("--backend-max-cpu-seconds", type=int, default=None)
    closure_prover.add_argument("--backend-max-processes", type=int, default=None)
    closure_prover.add_argument("--min-available-memory-mb", type=int, default=None)
    closure_prover.add_argument("--max-load-per-cpu", type=float, default=None)
    closure_prover.add_argument("--system-wait-seconds", type=int, default=None)

    campaign = subparsers.add_parser(
        "run-open-campaign",
        help="Run proof search across a shortlist of open problems from a scout report.",
    )
    campaign.add_argument("--scout-report", type=Path, required=True)
    campaign.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    campaign.add_argument("--bank-name")
    campaign.add_argument("--backend", choices=("codex", "none"), default="codex")
    campaign.add_argument("--limit", type=int, default=3)
    campaign.add_argument("--attempts", type=int, default=2)
    campaign.add_argument("--time-budget", type=int, default=600)
    campaign.add_argument("--attempt-timeout", type=int, default=180)
    campaign.add_argument("--build-timeout", type=int, default=90)
    campaign.add_argument("--no-create-missing", action="store_true")
    campaign.add_argument("--allow-cold-cache", action="store_true")
    campaign.add_argument("--allow-network", action="store_true")
    _add_proof_search_runtime_args(campaign)

    convergence_campaign = subparsers.add_parser(
        "run-convergence-campaign",
        help="Run longer proof-search cycles on open projects that are already checkpointed or otherwise ready for convergence work.",
    )
    convergence_campaign.add_argument("--projects-root", type=Path, default=_projects_root())
    convergence_campaign.add_argument("--limit", type=int, default=4)
    convergence_campaign.add_argument("--backend", choices=("auto", "codex", "none"), default="auto")
    convergence_campaign.add_argument("--runtime-multiplier", type=float, default=2.0)
    convergence_campaign.add_argument("--attempt-multiplier", type=float, default=1.5)
    convergence_campaign.add_argument("--include-blocked", action="store_true")
    convergence_campaign.add_argument("--include-not-ready", action="store_true")
    convergence_campaign.add_argument("--checkpoint-only", action="store_true")
    convergence_campaign.add_argument("--problem-id", action="append", default=[])
    convergence_campaign.add_argument("--allow-network", action="store_true")
    convergence_campaign.add_argument("--allow-cold-cache", action="store_true")
    convergence_campaign.add_argument("--rounds", type=int, default=1)
    convergence_campaign.add_argument("--stop-on-checkpoint", action="store_true")
    convergence_campaign.add_argument("--continue-on-exhausted", action="store_true")
    _add_proof_search_runtime_args(convergence_campaign)

    light_sweep = subparsers.add_parser(
        "run-erdos-light-sweep",
        help="Run a resumable lightweight proof attempt across every open problem in the selected Erdős bank.",
    )
    light_sweep.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    light_sweep.add_argument("--bank-name")
    light_sweep.add_argument("--backend", choices=("codex", "none"), default="codex")
    light_sweep.add_argument("--problem-limit", type=int, default=None)
    light_sweep.add_argument("--start-index", type=int, default=0)
    light_sweep.add_argument("--time-budget", type=int, default=3600)
    light_sweep.add_argument("--attempt-timeout", type=int, default=45)
    light_sweep.add_argument("--build-timeout", type=int, default=45)
    light_sweep.add_argument("--no-create-missing", action="store_true")
    light_sweep.add_argument("--allow-backend-without-seed", action="store_true")
    light_sweep.add_argument("--allow-network", action="store_true")
    light_sweep.add_argument("--allow-cold-cache", action="store_true")
    _add_proof_search_runtime_args(light_sweep)

    math_scout = subparsers.add_parser(
        "run-math-scout",
        help="Run active shallow mathematical proof probes across a problem bank.",
    )
    math_scout.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    math_scout.add_argument("--bank-name")
    math_scout.add_argument("--scout-report", type=Path, default=None)
    math_scout.add_argument("--backend", choices=("codex", "none"), default="codex")
    math_scout.add_argument("--problem-limit", type=int, default=None)
    math_scout.add_argument("--start-index", type=int, default=0)
    math_scout.add_argument("--time-budget", type=int, default=3600)
    math_scout.add_argument("--timeout-per-problem", type=int, default=300)
    math_scout.add_argument("--output", type=Path, default=None)
    math_scout.add_argument("--run-name", default=None)
    math_scout.add_argument("--selection-mode", choices=("ranked", "domain_balanced"), default="ranked")
    math_scout.add_argument("--exclude-problem", action="append", default=[])
    math_scout.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    math_scout.add_argument("--model", default=None, help="Override the math-scout backend model.")
    math_scout.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    write = subparsers.add_parser("write-manuscript", help="Generate a manuscript blueprint for a project.")
    write.add_argument("--project", type=Path, required=True)

    review = subparsers.add_parser("review-project", help="Run math-specific publishability and proof-gap checks.")
    review.add_argument("--project", type=Path, required=True)

    run = subparsers.add_parser("run", help="Run the current MVP pipeline for a project.")
    run.add_argument("--project", type=Path, required=True)
    run.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    run.add_argument("--bank-name")
    run.add_argument("--timeout", type=int, default=600)
    run.add_argument("--allow-cold-cache", action="store_true")

    status = subparsers.add_parser("status", help="Read the project pipeline status.")
    status.add_argument("--project", type=Path, required=True)

    scout = subparsers.add_parser("scout-bank", help="Score and rank open problems in a bank.")
    scout.add_argument("--bank", type=Path, default=DEFAULT_BANK_PATH)
    scout.add_argument("--bank-name")
    scout.add_argument("--formal-math-root", type=Path, default=None)
    scout.add_argument("--top-k", type=int, default=20)
    scout.add_argument("--output", type=Path, default=None)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-banks":
        _print(load_bank_registry(args.registry), args.json)
        return 0

    if args.command == "list-problems":
        problems = [problem.to_dict() for problem in load_problem_bank(_selected_bank_path(args))]
        _print(problems, args.json)
        return 0

    if args.command == "import-erdos-bank":
        output = import_erdos_open_problems(args.source, args.output)
        _print({"output": str(output)}, args.json)
        return 0

    if args.command == "refresh-erdos-status":
        payload = refresh_erdos_problem_bank(
            _selected_bank_path(args),
            output_path=args.output,
            problem_id=args.problem_id,
        )
        _print(payload, args.json)
        return 0

    if args.command == "sync-local-banks":
        payload = sync_local_problem_banks(
            formal_math_root=args.formal_math_root,
            data_root=args.data_root,
            registry_output=args.registry_output,
        )
        _print(payload, args.json)
        return 0

    if args.command == "init-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.init_ara_library(), args.json)
        return 0

    if args.command == "add-ara-library-module":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(
            orchestrator.add_ara_library_module(
                module_name=args.module_name,
                imports=args.imports,
                title=args.title,
                domain=args.domain,
                status=args.status,
                tags=args.tags,
                description=args.description,
            ),
            args.json,
        )
        return 0

    if args.command == "promote-to-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(
            orchestrator.promote_to_ara_library(
                source_file=args.source_file,
                source_project=args.source_project,
                module_name=args.module_name,
                declarations=args.declarations,
                imports=args.imports,
                title=args.title,
                domain=args.domain,
                status=args.status,
                tags=args.tags,
                description=args.description,
            ),
            args.json,
        )
        return 0

    if args.command == "list-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.list_ara_library(), args.json)
        return 0

    if args.command == "build-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.build_ara_library(timeout_sec=args.timeout, allow_cold_cache=args.allow_cold_cache), args.json)
        return 0

    if args.command == "new-project":
        bank_path = _selected_bank_path(args)
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            projects_root=args.projects_root,
            bank_path=bank_path,
            bank_name=getattr(args, "bank_name", None),
        )
        if args.name:
            project_name = args.name
        else:
            project_name = f"{args.problem}-{today_utc()}"
        project_dir = orchestrator.create_project(problem_id=args.problem, name=project_name)
        _print({"project_dir": str(project_dir)}, args.json)
        return 0

    if args.command == "set-statement":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        statement_text = args.statement_file.read_text(encoding="utf-8")
        _print(orchestrator.set_project_statement(args.project, statement_text, source=args.source), args.json)
        return 0

    if args.command == "set-deliverable":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.set_project_deliverable(args.project, mode=args.mode, reason=args.reason), args.json)
        return 0

    if args.command == "plan":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        _print(orchestrator.plan_project(args.project), args.json)
        return 0

    if args.command == "discover-proof-route":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        _print(orchestrator.discover_proof_route(args.project), args.json)
        return 0

    if args.command == "harvest-literature":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        _print(orchestrator.harvest_literature(args.project), args.json)
        return 0

    if args.command == "prepare-formal":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.prepare_formal(args.project), args.json)
        return 0

    if args.command == "plan-convergence":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.plan_convergence(args.project), args.json)
        return 0

    if args.command == "plan-proof-system":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.plan_proof_system(args.project), args.json)
        return 0

    if args.command == "run-evaluator":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.run_evaluator(args.project, timeout_sec=args.timeout, auto=args.auto), args.json)
        return 0

    if args.command == "run-math-attack":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        if args.model is not None:
            orchestrator.math_attack_runner.backend_model = args.model
        if args.reasoning_effort is not None:
            orchestrator.math_attack_runner.backend_reasoning_effort = args.reasoning_effort
        evidence_command = shlex.split(args.evidence_command) if args.evidence_command.strip() else []
        _print(
            orchestrator.run_math_attack(
                args.project,
                target=args.target,
                context_paths=args.context_file,
                evidence_command=evidence_command,
                evidence_cwd=args.evidence_cwd,
                evidence_timeout_sec=args.evidence_timeout,
                backend=args.backend,
                iterations=args.iterations,
                time_budget_sec=args.time_budget,
                iteration_timeout_sec=args.iteration_timeout,
                sleep_seconds=args.sleep_seconds,
                sleep_mode=args.sleep_mode,
                min_sleep_seconds=args.min_sleep_seconds,
                max_sleep_seconds=args.max_sleep_seconds,
                sleep_jitter_seconds=args.sleep_jitter_seconds,
                launch_spacing_seconds=args.launch_spacing_seconds,
                run_name=args.run_name,
                enable_search=args.search,
                dry_run=args.dry_run,
            ),
            args.json,
        )
        return 0

    if args.command == "build-lean":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _print(orchestrator.build_lean(args.project, timeout_sec=args.timeout), args.json)
        return 0

    if args.command == "run-proof-search":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _apply_proof_search_runtime_overrides(orchestrator, args)
        _print(
            orchestrator.run_proof_search(
                args.project,
                backend=args.backend,
                max_attempts=args.attempts,
                max_runtime_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                build_timeout_sec=args.build_timeout,
                focus_mode=args.focus_mode,
            ),
            args.json,
        )
        return 0

    if args.command == "run-closure-prover":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        orchestrator.closure_prover_runner.lean_executor.allow_cold_cache = args.allow_cold_cache
        _apply_closure_runtime_overrides(orchestrator, args)
        _print(
            orchestrator.run_closure_prover(
                args.project,
                target_theorem=args.target_theorem,
                target_file=args.target_file,
                backend=args.backend,
                max_attempts=args.attempts,
                max_runtime_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                build_timeout_sec=args.build_timeout,
                max_stalled_attempts=args.max_stalled_attempts,
                rollback_failed_attempts=args.rollback_failed_attempts,
            ),
            args.json,
        )
        return 0

    if args.command == "run-open-campaign":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _apply_proof_search_runtime_overrides(orchestrator, args)
        _print(
            orchestrator.run_open_problem_campaign(
                scout_report_path=args.scout_report,
                limit=args.limit,
                backend=args.backend,
                max_attempts=args.attempts,
                max_runtime_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                build_timeout_sec=args.build_timeout,
                create_missing=not args.no_create_missing,
            ),
            args.json,
        )
        return 0

    if args.command == "run-convergence-campaign":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            projects_root=args.projects_root,
            allow_network=args.allow_network,
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _apply_proof_search_runtime_overrides(orchestrator, args)
        _print(
            orchestrator.run_convergence_campaign(
                limit=args.limit,
                backend=args.backend,
                runtime_multiplier=args.runtime_multiplier,
                attempt_multiplier=args.attempt_multiplier,
                include_blocked=args.include_blocked,
                include_not_ready=args.include_not_ready,
                checkpoint_only=args.checkpoint_only,
                project_filters=args.problem_id,
                model_override=args.model,
                reasoning_effort_override=args.reasoning_effort,
                rounds=args.rounds,
                continue_on_checkpoint=not args.stop_on_checkpoint,
                continue_on_exhausted=args.continue_on_exhausted,
            ),
            args.json,
        )
        return 0

    if args.command == "run-erdos-light-sweep":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
            allow_network=args.allow_network,
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _apply_proof_search_runtime_overrides(orchestrator, args)
        _print(
            orchestrator.run_erdos_light_sweep(
                backend=args.backend,
                problem_limit=args.problem_limit,
                start_index=args.start_index,
                max_runtime_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                build_timeout_sec=args.build_timeout,
                create_missing=not args.no_create_missing,
                allow_backend_without_seed=args.allow_backend_without_seed,
            ),
            args.json,
        )
        return 0

    if args.command == "run-math-scout":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
        )
        if args.model is not None:
            orchestrator.math_scout_runner.backend_model = args.model
        if args.reasoning_effort is not None:
            orchestrator.math_scout_runner.backend_reasoning_effort = args.reasoning_effort
        _print(
            orchestrator.run_math_scout(
                scout_report_path=args.scout_report,
                backend=args.backend,
                problem_limit=args.problem_limit,
                start_index=args.start_index,
                time_budget_sec=args.time_budget,
                timeout_per_problem_sec=args.timeout_per_problem,
                output_path=args.output,
                run_name=args.run_name,
                enable_search=args.search,
                selection_mode=args.selection_mode,
                exclude_problem_ids=args.exclude_problem,
            ),
            args.json,
        )
        return 0

    if args.command == "write-manuscript":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.write_manuscript(args.project), args.json)
        return 0

    if args.command == "review-project":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.review_project(args.project), args.json)
        return 0

    if args.command == "run":
        orchestrator = MathResearchOrchestrator(
            repo_root=_repo_root(),
            bank_path=_selected_bank_path(args),
            bank_name=getattr(args, "bank_name", None),
        )
        orchestrator.lean_executor.allow_cold_cache = args.allow_cold_cache
        _print(orchestrator.run_pipeline(args.project, timeout_sec=args.timeout), args.json)
        return 0

    if args.command == "status":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.get_status(args.project), args.json)
        return 0

    if args.command == "scout-bank":
        payload = scout_problem_bank(
            bank_path=_selected_bank_path(args),
            formal_math_root=args.formal_math_root,
            top_k=args.top_k,
            output_path=args.output,
        )
        _print(payload, args.json)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
