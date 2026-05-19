from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path
from typing import Any

from ara_math.banking import sync_local_problem_banks
from ara_math.campaign_loop import CampaignLoopRunner
from ara_math.comath_benchmarks import run_local_benchmark_suite, run_minimal_real_math_benchmark
from ara_math.comath_capabilities import (
    create_computation_certificate,
    install_specialist_role_contracts,
    refine_intake_project,
    run_comath_evaluation,
    update_theory_memory,
    verify_computation_certificate,
)
from ara_math.comath_source_audit import run_source_audit_loop
from ara_math.comath_specialists import run_specialist, run_specialist_loop
from ara_math.coordinator import (
    add_workstream as comath_add_workstream,
    bootstrap_ces75_erdos866_workstreams,
    comath_paths,
    init_comath_project as comath_init_project,
    project_dashboard as comath_project_dashboard,
    review_workstream_placeholder,
    run_comath_loop as comath_run_loop,
)
from ara_math.goal_campaign import GoalDrivenCampaignRunner, write_goal_manifest_template
from ara_math.focused_attack import FocusedLeanAttackAgent, load_expected_target_headers
from ara_math.orchestrator import MathResearchOrchestrator
from ara_math.problem_bank import (
    DEFAULT_BANK_PATH,
    import_erdos_open_problems,
    load_bank_registry,
    load_problem_bank,
    refresh_erdos_problem_bank,
    resolve_bank_path,
)
from ara_math.lean_formalizer import LeanFormalizerRunner, collect_proof_lab_context_paths
from ara_math.pure_agents import LeanFromNaturalProofAgent, NaturalLanguageTheoremProverAgent, UnifiedProofAgentLoop
from ara_math.proof_lab import AIProofLabRunner
from ara_math.scouting import scout_problem_bank
from ara_math.workstreams import (
    ReviewDecision,
    ReviewKind,
    WorkstreamKind,
    WorkstreamRecord,
    WorkstreamStatus,
)
from ara_math.workspace import slugify, today_utc
from amra.amra_library import AmraLibraryManager
from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_reports import write_portfolio_final_report
from amra.known_problem_smoke import run_known_problem_smoke
from amra.result_bundle import export_amra_result_bundle


DELIVERABLE_MODES = ("auto", "research_report", "formalization_note", "paper_candidate")
ARA_LIBRARY_STATUSES = ("candidate", "trusted", "upstream_candidate", "deprecated")
WORKSTREAM_KINDS = tuple(item.value for item in WorkstreamKind)
WORKSTREAM_STATUSES = tuple(item.value for item in WorkstreamStatus)
REVIEW_DECISIONS = tuple(item.value for item in ReviewDecision)


def _repo_root() -> Path:
    override = os.environ.get("AMRA_REPO_ROOT")
    if override:
        return Path(override).resolve()
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


def _split_csv(values: list[str] | None) -> list[str]:
    parts: list[str] = []
    for value in values or []:
        for item in value.split(","):
            item = item.strip()
            if item:
                parts.append(item)
    return parts


def _default_workstream_id(kind: str, goal: str) -> str:
    goal_slug = slugify(goal)[:48].strip("-") or "workstream"
    return f"{kind}-{goal_slug}"


def _selected_bank_path(args: argparse.Namespace) -> Path:
    bank_name = getattr(args, "bank_name", None)
    bank_path = getattr(args, "bank", None)
    if bank_name:
        return resolve_bank_path(bank_name=bank_name)
    return resolve_bank_path(bank_name=bank_name, bank_path=bank_path)


def _legacy_library_module_name(module_name: str) -> str:
    """Map AMRA-facing module names to the legacy library manager during migration."""
    if module_name == "AmraLibrary" or module_name.startswith("AmraLibrary."):
        return "AraLibrary" + module_name[len("AmraLibrary") :]
    return module_name


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
    parser = argparse.ArgumentParser(
        description="AMRA CLI",
        epilog=(
            "Compatibility: legacy entrypoints 'python3 -m ara_math', "
            "'ara-math', and 'ara_math' are deprecated aliases; use "
            "'python3 -m amra' or 'amra' for new automation."
        ),
    )
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
        help="Deprecated alias for init-amra-library.",
    )

    init_amra_library = subparsers.add_parser(
        "init-amra-library",
        help="Create the reusable local AMRA Lean library for mathlib gaps and staged contributions.",
    )

    add_ara_library = subparsers.add_parser(
        "add-ara-library-module",
        help="Deprecated alias for add-amra-library-module.",
    )
    add_ara_library.add_argument("--module-name", required=True, help="Lean module name, e.g. AraLibrary.NumberTheory.Carmichael.")
    add_ara_library.add_argument("--import", dest="imports", action="append", default=[], help="Lean import to add to the module.")
    add_ara_library.add_argument("--title", default="")
    add_ara_library.add_argument("--domain", default="")
    add_ara_library.add_argument("--status", choices=ARA_LIBRARY_STATUSES, default="candidate")
    add_ara_library.add_argument("--tag", dest="tags", action="append", default=[])
    add_ara_library.add_argument("--description", default="")

    add_amra_library = subparsers.add_parser(
        "add-amra-library-module",
        help="Create or register a reusable AMRA Lean library module.",
    )
    add_amra_library.add_argument("--module-name", required=True, help="Lean module name, e.g. AmraLibrary.NumberTheory.Carmichael.")
    add_amra_library.add_argument("--import", dest="imports", action="append", default=[], help="Lean import to add to the module.")
    add_amra_library.add_argument("--title", default="")
    add_amra_library.add_argument("--domain", default="")
    add_amra_library.add_argument("--status", choices=ARA_LIBRARY_STATUSES, default="candidate")
    add_amra_library.add_argument("--tag", dest="tags", action="append", default=[])
    add_amra_library.add_argument("--description", default="")

    promote_ara_library = subparsers.add_parser(
        "promote-to-ara-library",
        help="Deprecated alias for promote-to-amra-library.",
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

    promote_amra_library = subparsers.add_parser(
        "promote-to-amra-library",
        help="Promote selected Lean declarations from a project file into the reusable AMRA library.",
    )
    promote_amra_library.add_argument("--source-file", type=Path, required=True)
    promote_amra_library.add_argument("--source-project", type=Path, default=None)
    promote_amra_library.add_argument("--module-name", required=True, help="Lean module name, e.g. AmraLibrary.NumberTheory.Carmichael.")
    promote_amra_library.add_argument("--declaration", dest="declarations", action="append", required=True)
    promote_amra_library.add_argument("--import", dest="imports", action="append", default=[], help="Lean import to add to the module.")
    promote_amra_library.add_argument("--title", default="")
    promote_amra_library.add_argument("--domain", default="")
    promote_amra_library.add_argument("--status", choices=ARA_LIBRARY_STATUSES, default="candidate")
    promote_amra_library.add_argument("--tag", dest="tags", action="append", default=[])
    promote_amra_library.add_argument("--description", default="")

    list_ara_library = subparsers.add_parser("list-ara-library", help="Deprecated alias for list-amra-library.")
    list_amra_library = subparsers.add_parser("list-amra-library", help="List reusable AMRA Lean library modules.")

    build_ara_library = subparsers.add_parser("build-ara-library", help="Deprecated alias for build-amra-library.")
    build_ara_library.add_argument("--timeout", type=int, default=600)
    build_ara_library.add_argument("--allow-cold-cache", action="store_true")

    build_amra_library = subparsers.add_parser("build-amra-library", help="Build the reusable AMRA Lean library.")
    build_amra_library.add_argument("--timeout", type=int, default=600)
    build_amra_library.add_argument("--allow-cold-cache", action="store_true")

    portfolio_campaign = subparsers.add_parser(
        "run-portfolio-campaign",
        aliases=["portfolio-campaign"],
        help="Create an AMRA portfolio campaign scaffold over a problem bank.",
    )
    portfolio_campaign.add_argument("--bank", type=Path, required=True)
    portfolio_campaign.add_argument("--run-name", required=True)
    portfolio_campaign.add_argument("--scout-limit", type=int, default=6)
    portfolio_campaign.add_argument("--scout-timeout", type=int, default=600)
    portfolio_campaign.add_argument(
        "--scout-backend",
        choices=("codex", "none"),
        default="none",
        help="Backend for active portfolio scouting probes. Defaults to local artifact generation without an LLM.",
    )
    portfolio_campaign.add_argument("--promote-top", type=int, default=2)
    portfolio_campaign.add_argument(
        "--attack-budget",
        type=int,
        default=0,
        help="Optional bounded active execution budget in seconds for promoted targets. Default 0 only plans assignments.",
    )

    evaluate_problem = subparsers.add_parser(
        "evaluate-problem",
        help="Run the independent read-only AMRA difficulty evaluator for one problem project.",
    )
    evaluate_problem.add_argument("--project", type=Path, required=True)
    evaluate_problem.add_argument("--run-name", required=True)

    harvest_library_candidates = subparsers.add_parser(
        "harvest-library-candidates",
        help="Inspect verified declarations and write AMRA library harvest candidates.",
    )
    harvest_library_candidates.add_argument("--project", type=Path, required=True)
    harvest_library_candidates.add_argument("--module", required=True)

    summarize_portfolio_memory = subparsers.add_parser(
        "summarize-portfolio-memory",
        help="Summarize AMRA portfolio/global memory indexes.",
    )
    summarize_portfolio_memory.add_argument("--campaign", type=Path, default=None)

    write_portfolio_report = subparsers.add_parser(
        "write-portfolio-report",
        help="Write a final AMRA portfolio campaign report explaining promoted, parked, and frozen targets.",
    )
    write_portfolio_report.add_argument("--campaign", type=Path, required=True)
    write_portfolio_report.add_argument("--output", type=Path, default=None)

    export_result_bundle = subparsers.add_parser(
        "export-amra-result-bundle",
        help="Export an ARA-consumable AMRA result bundle for one project.",
    )
    export_result_bundle.add_argument("--project", type=Path, required=True)
    export_result_bundle.add_argument("--output", type=Path, default=None)
    export_result_bundle.add_argument(
        "--no-consolidate",
        action="store_true",
        help="Skip the pre-export AMRA memory consolidation pass.",
    )

    known_problem_smoke = subparsers.add_parser(
        "run-known-problem-smoke",
        help="Run a bounded deterministic known-problem proof/formalization smoke and export an AMRA bundle.",
    )
    known_problem_smoke.add_argument("--problem", required=True, help="Known-problem fixture id, e.g. imo_2025_p1.")
    known_problem_smoke.add_argument("--max-seconds", type=int, default=60)
    known_problem_smoke.add_argument("--out", type=Path, required=True, help="Output directory for the AMRA result bundle.")

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

    init_comath = subparsers.add_parser(
        "init-comath-project",
        help="Create local CoMath state and dashboard files for an existing ARA project.",
    )
    init_comath.add_argument("--project", type=Path, required=True)
    init_comath.add_argument("--project-name", default=None)
    init_comath.add_argument("--original-goal", "--goal", dest="original_goal", default=None)

    intake_comath = subparsers.add_parser(
        "intake-comath-project",
        help="Refine a loose mathematical goal into CoMath workstreams, claims, uncertainty items, and specialist roles.",
    )
    intake_comath.add_argument("--project", type=Path, required=True)
    intake_comath.add_argument("--project-name", default=None)
    goal_group = intake_comath.add_mutually_exclusive_group(required=False)
    goal_group.add_argument("--goal", default="")
    goal_group.add_argument("--goal-file", type=Path, default=None)
    intake_comath.add_argument("--domain", default="")
    intake_comath.add_argument("--context-file", type=Path, action="append", default=[])

    install_specialists = subparsers.add_parser(
        "install-comath-specialists",
        help="Write local CoMath specialist role contracts for the project.",
    )
    install_specialists.add_argument("--project", type=Path, required=True)

    run_specialist_cmd = subparsers.add_parser(
        "run-comath-specialist",
        help="Run one CoMath specialist through fake or Codex CLI ChatGPT backend.",
    )
    run_specialist_cmd.add_argument("--project", type=Path, required=True)
    run_specialist_cmd.add_argument("--role", "--role-id", dest="role_id", required=True)
    run_specialist_cmd.add_argument("--workstream", "--workstream-id", dest="workstream_id", default="")
    run_specialist_cmd.add_argument("--task", default="")
    run_specialist_cmd.add_argument("--backend", choices=("fake", "codex"), default="codex")
    run_specialist_cmd.add_argument("--model", default="", help="Override Codex model; empty uses ~/.codex/config.toml.")
    run_specialist_cmd.add_argument(
        "--reasoning-effort",
        default="",
        help="Override Codex reasoning effort; empty uses ~/.codex/config.toml.",
    )
    run_specialist_cmd.add_argument("--timeout", type=int, default=900)
    run_specialist_cmd.add_argument("--search", action="store_true")
    run_specialist_cmd.add_argument("--run-name", default=None)
    run_specialist_cmd.add_argument("--context-file", type=Path, action="append", default=[])
    run_specialist_cmd.add_argument("--no-resume-memory", action="store_true")

    run_specialist_loop_cmd = subparsers.add_parser(
        "run-comath-specialist-loop",
        help="Run a bounded loop over ready CoMath specialist roles.",
    )
    run_specialist_loop_cmd.add_argument("--project", type=Path, required=True)
    run_specialist_loop_cmd.add_argument(
        "--roles",
        action="append",
        default=[],
        help="Comma-separated role ids. If omitted, ready workstreams with role_id metadata are selected.",
    )
    run_specialist_loop_cmd.add_argument("--backend", choices=("fake", "codex"), default="codex")
    run_specialist_loop_cmd.add_argument("--model", default="", help="Override Codex model; empty uses ~/.codex/config.toml.")
    run_specialist_loop_cmd.add_argument("--reasoning-effort", default="")
    run_specialist_loop_cmd.add_argument("--timeout", type=int, default=900)
    run_specialist_loop_cmd.add_argument("--search", action="store_true")
    run_specialist_loop_cmd.add_argument("--max-specialists", type=int, default=3)
    run_specialist_loop_cmd.add_argument("--max-parallel-specialists", type=int, default=1)
    run_specialist_loop_cmd.add_argument("--run-name", default=None)
    run_specialist_loop_cmd.add_argument("--task", default="")
    run_specialist_loop_cmd.add_argument("--no-resume-memory", action="store_true")

    source_audit_loop_cmd = subparsers.add_parser(
        "run-comath-source-audit-loop",
        help="Run an automatic query-planned CoMath source-auditor loop.",
    )
    source_audit_loop_cmd.add_argument("--project", type=Path, required=True)
    source_audit_loop_cmd.add_argument("--rounds", type=int, default=3)
    source_audit_loop_cmd.add_argument("--backend", choices=("fake", "codex"), default="codex")
    source_audit_loop_cmd.add_argument("--model", default="")
    source_audit_loop_cmd.add_argument("--reasoning-effort", default="")
    source_audit_loop_cmd.add_argument("--timeout", type=int, default=900)
    source_audit_loop_cmd.add_argument("--no-search", action="store_true")
    source_audit_loop_cmd.add_argument("--max-parallel-rounds", type=int, default=1)
    source_audit_loop_cmd.add_argument("--run-name", default=None)
    source_audit_loop_cmd.add_argument("--workstream", "--workstream-id", dest="workstream_id", default="source-literature-audit")
    source_audit_loop_cmd.add_argument("--seed-term", action="append", default=[])

    benchmark_cmd = subparsers.add_parser(
        "run-comath-benchmarks",
        help="Run the local CoMath regression benchmark suite with fake providers.",
    )
    benchmark_cmd.add_argument("--output-root", type=Path, required=True)
    benchmark_cmd.add_argument("--suite-name", default="comath-local-smoke")

    real_benchmark_cmd = subparsers.add_parser(
        "run-comath-minimal-real-benchmark",
        help="Run a tiny real math benchmark through a specialist backend.",
    )
    real_benchmark_cmd.add_argument("--output-root", type=Path, required=True)
    real_benchmark_cmd.add_argument("--suite-name", default="minimal-math-real")
    real_benchmark_cmd.add_argument("--backend", choices=("fake", "codex"), default="codex")
    real_benchmark_cmd.add_argument("--model", default="")
    real_benchmark_cmd.add_argument("--reasoning-effort", default="medium")
    real_benchmark_cmd.add_argument("--timeout", type=int, default=300)

    add_comath_workstream = subparsers.add_parser(
        "add-workstream",
        help="Add or update a local CoMath workstream record.",
    )
    add_comath_workstream.add_argument("--project", type=Path, required=True)
    add_comath_workstream.add_argument("--workstream-id", "--workstream", dest="workstream_id", default=None)
    add_comath_workstream.add_argument("--kind", choices=WORKSTREAM_KINDS, required=True)
    goal_group = add_comath_workstream.add_mutually_exclusive_group(required=True)
    goal_group.add_argument("--goal", default=None)
    goal_group.add_argument("--goal-file", type=Path, default=None)
    add_comath_workstream.add_argument("--status", choices=WORKSTREAM_STATUSES, default=WorkstreamStatus.PLANNED.value)
    add_comath_workstream.add_argument("--owner", default="")
    add_comath_workstream.add_argument("--dependency", dest="dependencies", action="append", default=[])
    add_comath_workstream.add_argument("--claim-id", dest="claim_ids", action="append", default=[])
    add_comath_workstream.add_argument("--artifact-id", dest="artifact_ids", action="append", default=[])
    add_comath_workstream.add_argument("--blocker", dest="blockers", action="append", default=[])

    review_comath_workstream = subparsers.add_parser(
        "review-workstream",
        help="Create state-only placeholder review records for a CoMath workstream.",
    )
    review_comath_workstream.add_argument("--project", type=Path, required=True)
    review_comath_workstream.add_argument("--workstream", "--workstream-id", dest="workstream_id", required=True)
    review_comath_workstream.add_argument(
        "--reviewers",
        action="append",
        default=[],
        help="Comma-separated reviewer kinds, e.g. logic,source,lean.",
    )
    review_comath_workstream.add_argument("--reviewer", default="local-state")
    review_comath_workstream.add_argument("--decision", choices=REVIEW_DECISIONS, default=ReviewDecision.PENDING.value)
    review_comath_workstream.add_argument("--notes", default="")
    review_comath_workstream.add_argument(
        "--state-only",
        action="store_true",
        help="Accepted for clarity; this placeholder command is always state-only.",
    )

    project_dashboard_cmd = subparsers.add_parser(
        "project-dashboard",
        help="Render and print the local CoMath project dashboard.",
    )
    project_dashboard_cmd.add_argument("--project", type=Path, required=True)

    run_comath_loop = subparsers.add_parser(
        "run-comath-loop",
        help="Run a bounded local CoMath scheduler loop over ready workstreams.",
    )
    run_comath_loop.add_argument("--project", type=Path, required=True)
    run_comath_loop.add_argument("--max-workstreams", type=int, default=1)
    run_comath_loop.add_argument("--time-budget", type=int, default=300)
    run_comath_loop.add_argument("--workstream-time-budget", type=int, default=300)
    run_comath_loop.add_argument("--backend", choices=("none", "codex"), default="none")
    run_comath_loop.add_argument("--executor", default=None, help="Optional executor override for all selected workstreams.")
    run_comath_loop.add_argument("--attempts", type=int, default=1)
    run_comath_loop.add_argument("--run-name", default=None)
    run_comath_loop.add_argument("--freeze-stalled-after", type=int, default=2)
    run_comath_loop.add_argument("--max-parallel-workstreams", type=int, default=1)
    run_comath_loop.add_argument("--max-concurrent-llm-calls", type=int, default=1)
    run_comath_loop.add_argument("--max-concurrent-lean-builds", type=int, default=1)
    run_comath_loop.add_argument("--allow-network", action="store_true")
    run_comath_loop.add_argument("--search", action="store_true")

    bootstrap_ces75 = subparsers.add_parser(
        "bootstrap-ces75-comath",
        help="Initialize the active CES75/Erdos866 project with CoMath workstream templates.",
    )
    bootstrap_ces75.add_argument(
        "--project",
        type=Path,
        default=_projects_root() / "erdos-866-ai-continuation-20260505",
    )

    record_compute = subparsers.add_parser(
        "record-computation-certificate",
        help="Run or record a reproducible CoMath computation manifest and certificate.",
    )
    record_compute.add_argument("--project", type=Path, required=True)
    record_compute.add_argument("--workstream", "--workstream-id", dest="workstream_id", required=True)
    record_compute.add_argument(
        "--command",
        dest="compute_command",
        required=True,
        help="Command string parsed with shell-like quoting but run without a shell.",
    )
    record_compute.add_argument("--cwd", type=Path, default=None)
    record_compute.add_argument("--input", dest="input_paths", type=Path, action="append", default=[])
    record_compute.add_argument("--output", dest="output_paths", type=Path, action="append", default=[])
    record_compute.add_argument("--seed", default="")
    record_compute.add_argument("--timeout", type=int, default=120)
    record_compute.add_argument("--no-run", action="store_true")

    verify_compute = subparsers.add_parser(
        "verify-computation-certificate",
        help="Verify a previously recorded CoMath computation manifest.",
    )
    verify_compute.add_argument("--project", type=Path, required=True)
    verify_compute.add_argument("--manifest", type=Path, required=True)
    verify_compute.add_argument("--rerun", action="store_true")
    verify_compute.add_argument("--timeout", type=int, default=None)

    theory_memory = subparsers.add_parser(
        "update-theory-memory",
        help="Record CoMath theory-building memory: conjectures, reusable lemmas, failed hypotheses, and new directions.",
    )
    theory_memory.add_argument("--project", type=Path, required=True)
    theory_memory.add_argument("--conjecture", default="")
    theory_memory.add_argument("--lemma", default="")
    theory_memory.add_argument("--failed-hypothesis", default="")
    theory_memory.add_argument("--novelty-note", default="")
    theory_memory.add_argument("--new-direction", default="")
    theory_memory.add_argument("--owner-workstream", default="theory-building-memory")

    comath_eval = subparsers.add_parser(
        "run-comath-evaluation",
        help="Evaluate a CoMath project against the public AI Co-Mathematician architecture capabilities.",
    )
    comath_eval.add_argument("--project", type=Path, required=True)

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

    proof_lab = subparsers.add_parser(
        "run-ai-proof-lab",
        help="Run the standalone clean-room proof-lab experiment without mutating an ARA project workflow.",
    )
    statement_group = proof_lab.add_mutually_exclusive_group(required=True)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    proof_lab.add_argument("--context-file", type=Path, action="append", default=[])
    proof_lab.add_argument("--backend", choices=("codex", "none"), default="codex")
    proof_lab.add_argument("--attempts", type=int, default=4)
    proof_lab.add_argument("--audits", type=int, default=2)
    proof_lab.add_argument("--time-budget", type=int, default=3600)
    proof_lab.add_argument("--attempt-timeout", type=int, default=600)
    proof_lab.add_argument("--audit-timeout", type=int, default=300)
    proof_lab.add_argument("--source-first", action="store_true", help="Run a source/Lean asset grounding pass before proof attempts.")
    proof_lab.add_argument("--grounding-timeout", type=int, default=300)
    proof_lab.add_argument("--output-root", type=Path, default=None)
    proof_lab.add_argument("--run-name", default=None)
    proof_lab.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    proof_lab.add_argument("--model", default=None, help="Override the proof-lab backend model.")
    proof_lab.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    pure_theorem_agent = subparsers.add_parser(
        "run-pure-theorem-agent",
        help="Run a Codex-episode theorem prover in natural mathematical language.",
    )
    statement_group = pure_theorem_agent.add_mutually_exclusive_group(required=True)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    pure_theorem_agent.add_argument("--workspace", type=Path, default=None)
    pure_theorem_agent.add_argument("--context-file", type=Path, action="append", default=[])
    pure_theorem_agent.add_argument("--backend", choices=("codex", "none"), default="codex")
    pure_theorem_agent.add_argument("--max-steps", type=int, default=16, help="Maximum host-supervised Codex episodes.")
    pure_theorem_agent.add_argument("--time-budget", type=int, default=3600)
    pure_theorem_agent.add_argument("--step-timeout", type=int, default=300, help="Timeout per Codex episode.")
    pure_theorem_agent.add_argument("--command-timeout", type=int, default=120, help="Reserved for compatibility.")
    pure_theorem_agent.add_argument("--output-root", type=Path, default=None)
    pure_theorem_agent.add_argument("--run-name", default=None)
    pure_theorem_agent.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    pure_theorem_agent.add_argument("--model", default=None, help="Override the decision backend model.")
    pure_theorem_agent.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    pure_proof_agent = subparsers.add_parser(
        "run-pure-proof-agent",
        help="Run the unified proof-development loop with shared natural-language, computation, and Lean tools.",
    )
    statement_group = pure_proof_agent.add_mutually_exclusive_group(required=True)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    pure_proof_agent.add_argument("--workspace", type=Path, default=None, help="Optional Lean project root.")
    pure_proof_agent.add_argument("--context-file", type=Path, action="append", default=[])
    pure_proof_agent.add_argument("--target-theorem", default="")
    pure_proof_agent.add_argument("--build-command", default="lake build")
    pure_proof_agent.add_argument("--backend", choices=("codex", "none"), default="codex")
    pure_proof_agent.add_argument("--max-steps", type=int, default=20, help="Maximum host-supervised Codex episodes.")
    pure_proof_agent.add_argument("--time-budget", type=int, default=3600)
    pure_proof_agent.add_argument("--step-timeout", type=int, default=300, help="Timeout per Codex episode.")
    pure_proof_agent.add_argument("--command-timeout", type=int, default=300, help="Host verifier timeout.")
    pure_proof_agent.add_argument("--output-root", type=Path, default=None)
    pure_proof_agent.add_argument("--run-name", default=None)
    pure_proof_agent.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    pure_proof_agent.add_argument("--model", default=None, help="Override the decision backend model.")
    pure_proof_agent.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    pure_lean_agent = subparsers.add_parser(
        "run-pure-lean-agent",
        help="Run a Codex-episode Lean formalizer from a natural-language proof package.",
    )
    pure_lean_agent.add_argument("--workspace", type=Path, required=True, help="Lean project root containing lakefile.lean.")
    proof_package_group = pure_lean_agent.add_mutually_exclusive_group(required=True)
    proof_package_group.add_argument("--proof-package", default=None)
    proof_package_group.add_argument("--proof-package-file", type=Path, default=None)
    statement_group = pure_lean_agent.add_mutually_exclusive_group(required=False)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    pure_lean_agent.add_argument("--build-command", default="lake build")
    pure_lean_agent.add_argument("--backend", choices=("codex", "none"), default="codex")
    pure_lean_agent.add_argument("--max-steps", type=int, default=20, help="Maximum host-supervised Codex episodes.")
    pure_lean_agent.add_argument("--time-budget", type=int, default=3600)
    pure_lean_agent.add_argument("--step-timeout", type=int, default=300, help="Timeout per Codex episode.")
    pure_lean_agent.add_argument("--command-timeout", type=int, default=300, help="Host verifier timeout.")
    pure_lean_agent.add_argument("--output-root", type=Path, default=None)
    pure_lean_agent.add_argument("--run-name", default=None)
    pure_lean_agent.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    pure_lean_agent.add_argument("--model", default=None, help="Override the decision backend model.")
    pure_lean_agent.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    focused_lean_attack = subparsers.add_parser(
        "run-focused-lean-attack",
        help="Run a host-enforced Lean attack on exact required declarations.",
    )
    focused_lean_attack.add_argument("--workspace", type=Path, required=True, help="Lean project root containing lakefile.lean.")
    focused_lean_attack.add_argument(
        "--attack-target",
        action="append",
        required=True,
        default=[],
        help="Required Lean theorem/lemma declaration name. Repeat for multi-target focused attacks.",
    )
    statement_group = focused_lean_attack.add_mutually_exclusive_group(required=False)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    focused_lean_attack.add_argument("--context-file", type=Path, action="append", default=[])
    focused_lean_attack.add_argument(
        "--expected-target-header-file",
        type=Path,
        action="append",
        default=[],
        help="File containing a Lean theorem/lemma header that must match one attack target. Repeatable.",
    )
    focused_lean_attack.add_argument(
        "--allowed-file",
        type=Path,
        action="append",
        default=[],
        help="Lean file that may be changed, relative to the workspace unless absolute. Repeatable.",
    )
    focused_lean_attack.add_argument(
        "--allowed-helper-declaration",
        action="append",
        default=[],
        help="New helper theorem/lemma exempt from wrapper audits. Repeatable.",
    )
    focused_lean_attack.add_argument(
        "--forbid-new-conditional-wrapper",
        action="store_true",
        help="Flag new non-target theorem/lemma headers containing implication arrows unless explicitly allowed.",
    )
    focused_lean_attack.add_argument(
        "--forbid-new-declaration-regex",
        action="append",
        default=[],
        help="Regex for new theorem/lemma names that must not be introduced. Repeatable.",
    )
    focused_lean_attack.add_argument("--build-command", default="lake build")
    focused_lean_attack.add_argument("--backend", choices=("codex", "none"), default="codex")
    focused_lean_attack.add_argument("--max-steps", type=int, default=20, help="Maximum host-supervised Codex episodes.")
    focused_lean_attack.add_argument("--time-budget", type=int, default=3600)
    focused_lean_attack.add_argument("--step-timeout", type=int, default=300, help="Timeout per Codex episode.")
    focused_lean_attack.add_argument("--command-timeout", type=int, default=300, help="Host verifier timeout.")
    focused_lean_attack.add_argument("--output-root", type=Path, default=None)
    focused_lean_attack.add_argument("--run-name", default=None)
    focused_lean_attack.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    focused_lean_attack.add_argument("--model", default=None, help="Override the decision backend model.")
    focused_lean_attack.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")

    lean_formalizer = subparsers.add_parser(
        "run-lean-formalizer",
        help="Run the proof-lab downstream Lean write/verify loop on a Lean workspace.",
    )
    lean_formalizer.add_argument("--workspace", type=Path, required=True, help="Lean project root containing lakefile.lean.")
    statement_group = lean_formalizer.add_mutually_exclusive_group(required=False)
    statement_group.add_argument("--statement", default=None)
    statement_group.add_argument("--statement-file", type=Path, default=None)
    lean_formalizer.add_argument("--target-theorem", default=None)
    lean_formalizer.add_argument("--target-file", type=Path, default=None)
    lean_formalizer.add_argument(
        "--expected-target-header-file",
        type=Path,
        default=None,
        help="Lean theorem/lemma header that the target declaration must match up to whitespace.",
    )
    lean_formalizer.add_argument("--context-file", type=Path, action="append", default=[])
    lean_formalizer.add_argument(
        "--upstream-proof-lab-run",
        type=Path,
        action="append",
        default=[],
        help="Proof-lab run directory; high-signal attempt/audit artifacts are added as context.",
    )
    lean_formalizer.add_argument("--backend", choices=("codex", "none"), default="codex")
    lean_formalizer.add_argument("--attempts", type=int, default=8)
    lean_formalizer.add_argument("--time-budget", type=int, default=3600)
    lean_formalizer.add_argument("--attempt-timeout", type=int, default=900)
    lean_formalizer.add_argument("--build-timeout", type=int, default=300)
    lean_formalizer.add_argument("--build-command", default="lake build")
    lean_formalizer.add_argument("--output-root", type=Path, default=None)
    lean_formalizer.add_argument("--run-name", default=None)
    lean_formalizer.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    lean_formalizer.add_argument("--model", default=None, help="Override the formalizer backend model.")
    lean_formalizer.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")
    lean_formalizer.add_argument(
        "--max-stalled-attempts",
        type=int,
        default=0,
        help="Optional early stop after this many non-improving attempts. 0 disables stall stopping.",
    )
    lean_formalizer.add_argument("--rollback-failed-attempts", action="store_true")

    campaign_loop = subparsers.add_parser(
        "run-campaign-loop",
        help="Run a self-iterating proof campaign loop that alternates proof-lab route discovery and Lean verification.",
    )
    campaign_statement_group = campaign_loop.add_mutually_exclusive_group(required=True)
    campaign_statement_group.add_argument("--statement", default=None)
    campaign_statement_group.add_argument("--statement-file", type=Path, default=None)
    campaign_loop.add_argument("--context-file", type=Path, action="append", default=[])
    campaign_loop.add_argument("--workspace", type=Path, default=None)
    campaign_loop.add_argument("--final-target-theorem", default="")
    campaign_loop.add_argument("--initial-target-theorem", default="")
    campaign_loop.add_argument(
        "--completed-target-theorem",
        action="append",
        default=[],
        help="Theorem name to treat as already verified when selecting later loop targets. Repeatable.",
    )
    campaign_loop.add_argument("--target-file", type=Path, default=None)
    campaign_loop.add_argument("--build-command", default="lake build")
    campaign_loop.add_argument("--backend", choices=("codex", "none"), default="codex")
    campaign_loop.add_argument("--mode", choices=("auto", "hybrid", "proof-lab", "lean-formalizer"), default="auto")
    campaign_loop.add_argument("--rounds", type=int, default=4)
    campaign_loop.add_argument("--time-budget", type=int, default=3600)
    campaign_loop.add_argument("--proof-attempts", type=int, default=4)
    campaign_loop.add_argument("--proof-audits", type=int, default=2)
    campaign_loop.add_argument("--proof-attempt-timeout", type=int, default=600)
    campaign_loop.add_argument("--proof-audit-timeout", type=int, default=300)
    campaign_loop.add_argument("--proof-grounding-timeout", type=int, default=300)
    campaign_loop.add_argument("--formalizer-attempts", type=int, default=8)
    campaign_loop.add_argument("--formalizer-attempt-timeout", type=int, default=900)
    campaign_loop.add_argument("--formalizer-build-timeout", type=int, default=300)
    campaign_loop.add_argument("--source-first", action="store_true")
    campaign_loop.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    campaign_loop.add_argument("--output-root", type=Path, default=None)
    campaign_loop.add_argument("--run-name", default=None)
    campaign_loop.add_argument("--model", default=None, help="Override proof-lab and formalizer backend model.")
    campaign_loop.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")
    campaign_loop.add_argument("--max-stalled-rounds", type=int, default=0)
    campaign_loop.add_argument(
        "--round-time-budget",
        type=int,
        default=0,
        help="Optional per-round wall-clock cap in seconds. 0 uses dynamic scheduling.",
    )

    init_goal_campaign = subparsers.add_parser(
        "init-goal-campaign",
        help="Write a root-goal manifest for a goal-driven proof campaign.",
    )
    init_goal_campaign.add_argument("--output", type=Path, required=True)
    root_statement_group = init_goal_campaign.add_mutually_exclusive_group(required=True)
    root_statement_group.add_argument("--root-statement", default=None)
    root_statement_group.add_argument("--root-statement-file", type=Path, default=None)
    init_goal_campaign.add_argument("--root-target-theorem", default="")
    init_goal_campaign.add_argument("--root-target-file", default="")
    init_goal_campaign.add_argument("--workspace", default="")
    init_goal_campaign.add_argument("--build-command", default="lake build")

    goal_campaign = subparsers.add_parser(
        "run-goal-campaign",
        help="Run a root-goal driven campaign over dependent subgoals.",
    )
    goal_campaign.add_argument("--manifest", type=Path, required=True)
    goal_campaign.add_argument("--context-file", type=Path, action="append", default=[])
    goal_campaign.add_argument("--workspace", type=Path, default=None)
    goal_campaign.add_argument("--build-command", default=None)
    goal_campaign.add_argument("--backend", choices=("codex", "none"), default="codex")
    goal_campaign.add_argument("--mode", choices=("auto", "hybrid", "proof-lab", "lean-formalizer"), default="hybrid")
    goal_campaign.add_argument("--rounds", type=int, default=12)
    goal_campaign.add_argument("--time-budget", type=int, default=7200)
    goal_campaign.add_argument("--child-rounds", type=int, default=2)
    goal_campaign.add_argument("--child-time-budget", type=int, default=1800)
    goal_campaign.add_argument("--child-attempts", type=int, default=6)
    goal_campaign.add_argument("--child-attempt-timeout", type=int, default=900)
    goal_campaign.add_argument("--child-build-timeout", type=int, default=300)
    goal_campaign.add_argument("--gap-review-time-budget", type=int, default=600)
    goal_campaign.add_argument("--gap-review-attempt-timeout", type=int, default=300)
    goal_campaign.add_argument("--search", action="store_true", help="Allow backend web search when supported.")
    goal_campaign.add_argument("--output-root", type=Path, default=None)
    goal_campaign.add_argument("--run-name", default=None)
    goal_campaign.add_argument("--model", default=None, help="Override proof-lab and formalizer backend model.")
    goal_campaign.add_argument("--reasoning-effort", default=None, help="Override backend reasoning effort.")
    goal_campaign.add_argument(
        "--max-goal-runs",
        type=int,
        default=0,
        help="Optional retry cap per goal. 0 leaves retries bounded only by campaign rounds/time.",
    )
    goal_campaign.add_argument("--no-write-back-manifest", action="store_true")
    goal_campaign.add_argument("--no-dynamic-goals", action="store_true")

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
    normalized_argv = list(sys.argv[1:] if argv is None else argv)
    if "--json" in normalized_argv:
        normalized_argv = [item for item in normalized_argv if item != "--json"]
        normalized_argv.insert(0, "--json")
    args = parser.parse_args(normalized_argv)

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

    if args.command == "init-amra-library":
        manager = AmraLibraryManager(repo_root=_repo_root())
        _print(manager.ensure_library(), args.json)
        return 0

    if args.command == "init-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.init_ara_library(), args.json)
        return 0

    if args.command == "add-amra-library-module":
        manager = AmraLibraryManager(repo_root=_repo_root())
        _print(
            manager.add_module(
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

    if args.command == "add-ara-library-module":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(
            orchestrator.add_ara_library_module(
                module_name=_legacy_library_module_name(args.module_name),
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

    if args.command == "promote-to-amra-library":
        manager = AmraLibraryManager(repo_root=_repo_root())
        _print(
            manager.promote_declarations(
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

    if args.command == "promote-to-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(
            orchestrator.promote_to_ara_library(
                source_file=args.source_file,
                source_project=args.source_project,
                module_name=_legacy_library_module_name(args.module_name),
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

    if args.command == "list-amra-library":
        manager = AmraLibraryManager(repo_root=_repo_root())
        _print(manager.inventory(), args.json)
        return 0

    if args.command == "list-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.list_ara_library(), args.json)
        return 0

    if args.command == "build-amra-library":
        manager = AmraLibraryManager(repo_root=_repo_root())
        _print(manager.build(timeout_sec=args.timeout, allow_cold_cache=args.allow_cold_cache), args.json)
        return 0

    if args.command == "build-ara-library":
        orchestrator = MathResearchOrchestrator(repo_root=_repo_root())
        _print(orchestrator.build_ara_library(timeout_sec=args.timeout, allow_cold_cache=args.allow_cold_cache), args.json)
        return 0

    if args.command in {"run-portfolio-campaign", "portfolio-campaign"}:
        runner = PortfolioCampaignRunner(repo_root=_repo_root())
        payload = runner.run_portfolio_campaign(
            bank=args.bank,
            run_name=args.run_name,
            scout_limit=args.scout_limit,
            scout_timeout=args.scout_timeout,
            scout_backend=args.scout_backend,
            promote_top=args.promote_top,
            attack_budget=args.attack_budget,
        )
        report = write_portfolio_final_report(_repo_root() / str(payload["campaign_dir"]), repo_root=_repo_root())
        _print({**payload, "final_report": report["final_report"]}, args.json)
        return 0

    if args.command == "evaluate-problem":
        runner = PortfolioCampaignRunner(repo_root=_repo_root())
        _print(runner.evaluate_problem(project=args.project, run_name=args.run_name), args.json)
        return 0

    if args.command == "harvest-library-candidates":
        runner = PortfolioCampaignRunner(repo_root=_repo_root())
        _print(runner.harvest_library_candidates(project=args.project, module=args.module), args.json)
        return 0

    if args.command == "summarize-portfolio-memory":
        runner = PortfolioCampaignRunner(repo_root=_repo_root())
        _print(runner.summarize_portfolio_memory(campaign=args.campaign), args.json)
        return 0

    if args.command == "write-portfolio-report":
        _print(
            write_portfolio_final_report(
                args.campaign,
                output_path=args.output,
                repo_root=_repo_root(),
            ),
            args.json,
        )
        return 0

    if args.command == "export-amra-result-bundle":
        _print(
            export_amra_result_bundle(
                project=args.project,
                output_dir=args.output,
                repo_root=_repo_root(),
                consolidate=not args.no_consolidate,
            ),
            args.json,
        )
        return 0

    if args.command == "run-known-problem-smoke":
        _print(
            run_known_problem_smoke(
                problem_id=args.problem,
                max_seconds=args.max_seconds,
                output_dir=args.out,
                repo_root=_repo_root(),
            ),
            args.json,
        )
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

    if args.command == "init-comath-project":
        state = comath_init_project(
            args.project,
            project_name=args.project_name,
            original_goal=args.original_goal,
        )
        paths = comath_paths(args.project)
        _print(
            {
                "project_dir": str(args.project),
                "state_path": str(paths.project_state),
                "dashboard_path": str(paths.dashboard),
                "state": state.to_dict(),
            },
            args.json,
        )
        return 0

    if args.command == "intake-comath-project":
        goal = args.goal_file.read_text(encoding="utf-8").strip() if args.goal_file else args.goal
        payload = refine_intake_project(
            args.project,
            goal=goal,
            project_name=args.project_name,
            domain=args.domain,
            context_files=args.context_file,
        )
        _print(payload, args.json)
        return 0

    if args.command == "install-comath-specialists":
        payload = install_specialist_role_contracts(args.project)
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-specialist":
        payload = run_specialist(
            args.project,
            role_id=args.role_id,
            workstream_id=args.workstream_id,
            task=args.task,
            backend=args.backend,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout_seconds=args.timeout,
            allow_search=args.search,
            run_name=args.run_name,
            context_files=args.context_file,
            resume_memory=not args.no_resume_memory,
        )
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-specialist-loop":
        payload = run_specialist_loop(
            args.project,
            roles=_split_csv(args.roles),
            backend=args.backend,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout_seconds=args.timeout,
            allow_search=args.search,
            max_specialists=args.max_specialists,
            max_parallel_specialists=args.max_parallel_specialists,
            run_name=args.run_name,
            task=args.task,
            resume_memory=not args.no_resume_memory,
        )
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-source-audit-loop":
        payload = run_source_audit_loop(
            args.project,
            rounds=args.rounds,
            backend=args.backend,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout_seconds=args.timeout,
            allow_search=not args.no_search,
            max_parallel_rounds=args.max_parallel_rounds,
            run_name=args.run_name,
            workstream_id=args.workstream_id,
            seed_terms=args.seed_term,
        )
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-benchmarks":
        payload = run_local_benchmark_suite(args.output_root, suite_name=args.suite_name)
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-minimal-real-benchmark":
        payload = run_minimal_real_math_benchmark(
            args.output_root,
            suite_name=args.suite_name,
            backend=args.backend,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout_seconds=args.timeout,
        )
        _print(payload, args.json)
        return 0

    if args.command == "add-workstream":
        goal = args.goal if args.goal is not None else args.goal_file.read_text(encoding="utf-8").strip()
        workstream_id = args.workstream_id or _default_workstream_id(args.kind, goal)
        workstream = WorkstreamRecord(
            workstream_id=workstream_id,
            kind=WorkstreamKind.coerce(args.kind),
            goal=goal,
            status=WorkstreamStatus.coerce(args.status),
            owner=args.owner,
            dependencies=args.dependencies,
            claim_ids=args.claim_ids,
            artifact_ids=args.artifact_ids,
            blockers=args.blockers,
        )
        saved = comath_add_workstream(args.project, workstream)
        paths = comath_paths(args.project)
        _print(
            {
                "project_dir": str(args.project),
                "workstream_dir": str(paths.workstream_dir(saved.workstream_id)),
                "dashboard_path": str(paths.dashboard),
                "workstream": saved.to_dict(),
            },
            args.json,
        )
        return 0

    if args.command == "review-workstream":
        reviewers = _split_csv(args.reviewers) or [ReviewKind.LOGIC.value]
        payload = review_workstream_placeholder(
            args.project,
            args.workstream_id,
            reviewers=reviewers,
            decision=args.decision,
            reviewer=args.reviewer,
            notes=args.notes,
        )
        _print(payload, args.json)
        return 0

    if args.command == "project-dashboard":
        dashboard = comath_project_dashboard(args.project)
        if args.json:
            _print(
                {
                    "project_dir": str(args.project),
                    "dashboard_path": str(comath_paths(args.project).dashboard),
                    "dashboard": dashboard,
                },
                args.json,
            )
        else:
            _print(dashboard, args.json)
        return 0

    if args.command == "run-comath-loop":
        payload = comath_run_loop(
            args.project,
            max_workstreams=args.max_workstreams,
            time_budget_seconds=args.time_budget,
            executor_name=args.executor,
            executor_options={
                "backend": args.backend,
                "attempts": args.attempts,
                "time_budget": args.workstream_time_budget,
                "allow_network": args.allow_network,
                "search": args.search,
            },
            repo_root=_repo_root(),
            freeze_stalled_after=args.freeze_stalled_after,
            run_name=args.run_name,
            max_parallel_workstreams=args.max_parallel_workstreams,
            max_concurrent_llm_calls=args.max_concurrent_llm_calls,
            max_concurrent_lean_builds=args.max_concurrent_lean_builds,
        )
        _print(payload, args.json)
        return 0

    if args.command == "bootstrap-ces75-comath":
        payload = bootstrap_ces75_erdos866_workstreams(args.project, repo_root=_repo_root())
        _print(payload, args.json)
        return 0

    if args.command == "record-computation-certificate":
        payload = create_computation_certificate(
            args.project,
            workstream_id=args.workstream_id,
            command=shlex.split(args.compute_command),
            cwd=args.cwd,
            input_paths=args.input_paths,
            output_paths=args.output_paths,
            seed=args.seed,
            timeout_seconds=args.timeout,
            run=not args.no_run,
        )
        _print(payload, args.json)
        return 0

    if args.command == "verify-computation-certificate":
        payload = verify_computation_certificate(
            args.project,
            manifest_path=args.manifest,
            rerun=args.rerun,
            timeout_seconds=args.timeout,
        )
        _print(payload, args.json)
        return 0

    if args.command == "update-theory-memory":
        payload = update_theory_memory(
            args.project,
            conjecture=args.conjecture,
            lemma=args.lemma,
            failed_hypothesis=args.failed_hypothesis,
            novelty_note=args.novelty_note,
            new_direction=args.new_direction,
            owner_workstream_id=args.owner_workstream,
        )
        _print(payload, args.json)
        return 0

    if args.command == "run-comath-evaluation":
        payload = run_comath_evaluation(args.project)
        _print(payload, args.json)
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

    if args.command == "run-ai-proof-lab":
        runner = AIProofLabRunner(repo_root=_repo_root())
        if args.model is not None:
            runner.backend_model = args.model
        if args.reasoning_effort is not None:
            runner.backend_reasoning_effort = args.reasoning_effort
        statement = args.statement if args.statement is not None else args.statement_file.read_text(encoding="utf-8")
        _print(
            runner.run(
                statement=statement,
                context_paths=args.context_file,
                backend=args.backend,
                attempts=args.attempts,
                audits=args.audits,
                time_budget_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                audit_timeout_sec=args.audit_timeout,
                source_first=args.source_first,
                grounding_timeout_sec=args.grounding_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
            ),
            args.json,
        )
        return 0

    if args.command == "run-pure-theorem-agent":
        runner = NaturalLanguageTheoremProverAgent(repo_root=_repo_root())
        statement = args.statement if args.statement is not None else args.statement_file.read_text(encoding="utf-8")
        _print(
            runner.run(
                statement=statement,
                workspace=args.workspace,
                context_paths=args.context_file,
                backend=args.backend,
                max_steps=args.max_steps,
                time_budget_sec=args.time_budget,
                step_timeout_sec=args.step_timeout,
                command_timeout_sec=args.command_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
            ),
            args.json,
        )
        return 0

    if args.command == "run-pure-proof-agent":
        runner = UnifiedProofAgentLoop(repo_root=_repo_root())
        statement = args.statement if args.statement is not None else args.statement_file.read_text(encoding="utf-8")
        _print(
            runner.run(
                statement=statement,
                workspace=args.workspace,
                context_paths=args.context_file,
                build_command=shlex.split(args.build_command),
                target_name=args.target_theorem,
                backend=args.backend,
                max_steps=args.max_steps,
                time_budget_sec=args.time_budget,
                step_timeout_sec=args.step_timeout,
                command_timeout_sec=args.command_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
            ),
            args.json,
        )
        return 0

    if args.command == "run-pure-lean-agent":
        runner = LeanFromNaturalProofAgent(repo_root=_repo_root())
        proof_package = (
            args.proof_package
            if args.proof_package is not None
            else args.proof_package_file.read_text(encoding="utf-8")
        )
        if args.statement is not None:
            statement = args.statement
        elif args.statement_file is not None:
            statement = args.statement_file.read_text(encoding="utf-8")
        else:
            statement = ""
        _print(
            runner.run(
                workspace=args.workspace,
                proof_package=proof_package,
                statement=statement,
                build_command=shlex.split(args.build_command),
                backend=args.backend,
                max_steps=args.max_steps,
                time_budget_sec=args.time_budget,
                step_timeout_sec=args.step_timeout,
                command_timeout_sec=args.command_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
            ),
            args.json,
        )
        return 0

    if args.command == "run-focused-lean-attack":
        runner = FocusedLeanAttackAgent(repo_root=_repo_root())
        if args.statement is not None:
            statement = args.statement
        elif args.statement_file is not None:
            statement = args.statement_file.read_text(encoding="utf-8")
        else:
            statement = ""
        expected_headers = load_expected_target_headers(args.expected_target_header_file, args.attack_target)
        _print(
            runner.run(
                workspace=args.workspace,
                attack_targets=args.attack_target,
                statement=statement,
                context_paths=args.context_file,
                allowed_files=args.allowed_file,
                allowed_helper_declarations=args.allowed_helper_declaration,
                expected_target_headers=expected_headers,
                forbidden_new_declaration_regexes=args.forbid_new_declaration_regex,
                forbid_new_conditional_wrappers=args.forbid_new_conditional_wrapper,
                build_command=shlex.split(args.build_command),
                backend=args.backend,
                max_steps=args.max_steps,
                time_budget_sec=args.time_budget,
                step_timeout_sec=args.step_timeout,
                command_timeout_sec=args.command_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
            ),
            args.json,
        )
        return 0

    if args.command == "run-lean-formalizer":
        runner = LeanFormalizerRunner(repo_root=_repo_root())
        if args.model is not None:
            runner.backend_model = args.model
        if args.reasoning_effort is not None:
            runner.backend_reasoning_effort = args.reasoning_effort
        context_paths = list(args.context_file)
        for proof_lab_run in args.upstream_proof_lab_run:
            context_paths.extend(collect_proof_lab_context_paths(proof_lab_run))
        if args.statement is not None:
            statement = args.statement
        elif args.statement_file is not None:
            statement = args.statement_file.read_text(encoding="utf-8")
        else:
            statement = ""
        expected_target_header = (
            args.expected_target_header_file.read_text(encoding="utf-8")
            if args.expected_target_header_file is not None
            else None
        )
        max_stalled_attempts = args.max_stalled_attempts if args.max_stalled_attempts > 0 else None
        _print(
            runner.run(
                workspace=args.workspace,
                statement=statement,
                context_paths=context_paths,
                target_theorem=args.target_theorem,
                target_file=args.target_file,
                build_command=shlex.split(args.build_command),
                backend=args.backend,
                attempts=args.attempts,
                time_budget_sec=args.time_budget,
                attempt_timeout_sec=args.attempt_timeout,
                build_timeout_sec=args.build_timeout,
                output_root=args.output_root,
                run_name=args.run_name,
                enable_search=args.search,
                max_stalled_attempts=max_stalled_attempts,
                rollback_failed_attempts=args.rollback_failed_attempts,
                expected_target_header=expected_target_header,
            ),
            args.json,
        )
        return 0

    if args.command == "run-campaign-loop":
        runner = CampaignLoopRunner(repo_root=_repo_root())
        if args.model is not None:
            runner.proof_lab_runner.backend_model = args.model
            runner.lean_formalizer_runner.backend_model = args.model
        if args.reasoning_effort is not None:
            runner.proof_lab_runner.backend_reasoning_effort = args.reasoning_effort
            runner.lean_formalizer_runner.backend_reasoning_effort = args.reasoning_effort
        statement = args.statement if args.statement is not None else args.statement_file.read_text(encoding="utf-8")
        _print(
            runner.run(
                statement=statement,
                context_paths=args.context_file,
                workspace=args.workspace,
                final_target_theorem=args.final_target_theorem,
                initial_target_theorem=args.initial_target_theorem,
                completed_target_theorems=args.completed_target_theorem,
                target_file=args.target_file,
                build_command=shlex.split(args.build_command),
                backend=args.backend,
                mode=args.mode,
                rounds=args.rounds,
                time_budget_sec=args.time_budget,
                proof_attempts=args.proof_attempts,
                proof_audits=args.proof_audits,
                proof_attempt_timeout_sec=args.proof_attempt_timeout,
                proof_audit_timeout_sec=args.proof_audit_timeout,
                proof_grounding_timeout_sec=args.proof_grounding_timeout,
                formalizer_attempts=args.formalizer_attempts,
                formalizer_attempt_timeout_sec=args.formalizer_attempt_timeout,
                formalizer_build_timeout_sec=args.formalizer_build_timeout,
                source_first=args.source_first,
                enable_search=args.search,
                output_root=args.output_root,
                run_name=args.run_name,
                max_stalled_rounds=args.max_stalled_rounds,
                round_time_budget_sec=args.round_time_budget,
            ),
            args.json,
        )
        return 0

    if args.command == "init-goal-campaign":
        root_statement = (
            args.root_statement
            if args.root_statement is not None
            else args.root_statement_file.read_text(encoding="utf-8")
        )
        payload = write_goal_manifest_template(
            args.output,
            root_statement=root_statement,
            root_target_theorem=args.root_target_theorem,
            root_target_file=args.root_target_file,
            workspace=args.workspace,
            build_command=shlex.split(args.build_command),
        )
        _print({"manifest_path": str(args.output), "manifest": payload}, args.json)
        return 0

    if args.command == "run-goal-campaign":
        runner = GoalDrivenCampaignRunner(repo_root=_repo_root())
        if args.model is not None:
            runner.campaign_runner.proof_lab_runner.backend_model = args.model
            runner.campaign_runner.lean_formalizer_runner.backend_model = args.model
            runner.proof_lab_runner.backend_model = args.model
        if args.reasoning_effort is not None:
            runner.campaign_runner.proof_lab_runner.backend_reasoning_effort = args.reasoning_effort
            runner.campaign_runner.lean_formalizer_runner.backend_reasoning_effort = args.reasoning_effort
            runner.proof_lab_runner.backend_reasoning_effort = args.reasoning_effort
        _print(
            runner.run(
                manifest_path=args.manifest,
                workspace=args.workspace,
                build_command=shlex.split(args.build_command) if args.build_command else None,
                context_paths=args.context_file,
                backend=args.backend,
                mode=args.mode,
                rounds=args.rounds,
                time_budget_sec=args.time_budget,
                child_rounds=args.child_rounds,
                child_time_budget_sec=args.child_time_budget,
                child_attempts=args.child_attempts,
                child_attempt_timeout_sec=args.child_attempt_timeout,
                child_build_timeout_sec=args.child_build_timeout,
                gap_review_time_budget_sec=args.gap_review_time_budget,
                gap_review_attempt_timeout_sec=args.gap_review_attempt_timeout,
                enable_search=args.search,
                output_root=args.output_root,
                run_name=args.run_name,
                max_goal_runs=args.max_goal_runs,
                write_back_manifest=not args.no_write_back_manifest,
                dynamic_goal_creation=not args.no_dynamic_goals,
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
