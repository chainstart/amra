#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import os
import re
import shlex
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from amra.core.workspace import slugify, utc_now_iso, write_json, write_text
from amra.lean.contract import extract_lean_declaration_header
from amra.proof.campaign_loop import CampaignLoopRunner


DEFAULT_PROOFBENCH_CSV = REPO_ROOT / "data/benchmarks/external/raw/imo_bench/imobench/proofbench.csv"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "benchmark_runs/imo_proofbench_campaigns"
DEFAULT_SOLVED_MANIFEST = REPO_ROOT / "benchmark_runs/imo_proofbench_parallel_5/manifest.json"
MATHLIB_REV = "v4.26.0"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.26.0"


CURATED_TARGETS: dict[str, str] = {
    "PB-Advanced-012": """
import Mathlib

namespace IMOProofBenchPBAdvanced012

/-!
Formal target for PB-Advanced-012.

Natural statement: If p is prime and a,b are positive integers such that
p^n = a^4 + b^4 for some n >= 2, then n >= 5.
-/

theorem pb_advanced_012_main
    (p a b n : Nat)
    (hp : Nat.Prime p)
    (ha : 0 < a)
    (hb : 0 < b)
    (hn : 2 <= n)
    (h : p ^ n = a ^ 4 + b ^ 4) :
    5 <= n := by
  sorry

end IMOProofBenchPBAdvanced012
""".strip()
    + "\n",
    "PB-Advanced-024": """
import Mathlib

namespace IMOProofBenchPBAdvanced024

/-!
Formal target for PB-Advanced-024.

The theorem packages both parts of the original problem: every admissible
function has at most two possible values of P(a)+P(-a), and the bound two is
attainable.
-/

def PBAdvanced024Condition (P : Rat -> Rat) : Prop :=
  forall a b : Rat,
    (P (b - P a) + a - P b) * (P (a + P (b - P a)) - b) = 0

def PBAdvanced024Values (P : Rat -> Rat) : Set Rat :=
  {x | exists a : Rat, x = P a + P (-a)}

theorem pb_advanced_024_main :
    (forall P : Rat -> Rat,
      PBAdvanced024Condition P ->
        Set.Finite (PBAdvanced024Values P) /\\ (PBAdvanced024Values P).ncard <= 2) /\\
    (exists P : Rat -> Rat,
      PBAdvanced024Condition P /\\ (PBAdvanced024Values P).ncard = 2) := by
  sorry

end IMOProofBenchPBAdvanced024
""".strip()
    + "\n",
}


@dataclass(frozen=True)
class ProofBenchProblem:
    problem_id: str
    problem: str
    solution: str
    grading_guidelines: str
    category: str
    level: str
    short_answer: str
    source: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "ProofBenchProblem":
        return cls(
            problem_id=row.get("Problem ID", "").strip(),
            problem=row.get("Problem", "").strip(),
            solution=row.get("Solution", "").strip(),
            grading_guidelines=row.get("Grading guidelines", "").strip(),
            category=row.get("Category", "").strip(),
            level=row.get("Level", "").strip(),
            short_answer=row.get("Short Answer", "").strip(),
            source=row.get("Source", "").strip(),
        )

    @property
    def slug(self) -> str:
        return slugify(self.problem_id).replace("-", "_")

    def to_json(self) -> dict[str, str]:
        return {
            "problem_id": self.problem_id,
            "problem": self.problem,
            "solution": self.solution,
            "grading_guidelines": self.grading_guidelines,
            "category": self.category,
            "level": self.level,
            "short_answer": self.short_answer,
            "source": self.source,
        }


@dataclass(frozen=True)
class PreparedProblem:
    record: ProofBenchProblem
    problem_dir: Path
    workspace: Path
    statement_path: Path
    reference_path: Path
    target_file: Path
    target_theorem: str
    expected_header_path: Path
    context_paths: list[Path]


def _clean_lean_identifier(value: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", value)
    if not parts:
        return "IMOProofBenchProblem"
    return "IMOProofBench" + "".join(part[:1].upper() + part[1:] for part in parts)


def module_name_for_problem(problem_id: str) -> str:
    return _clean_lean_identifier(problem_id)


def theorem_name_for_problem(problem_id: str) -> str:
    return slugify(problem_id).replace("-", "_") + "_main"


def load_proofbench(path: Path) -> list[ProofBenchProblem]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [ProofBenchProblem.from_row(row) for row in csv.DictReader(handle)]


def load_solved_problem_ids(manifest_paths: list[Path]) -> set[str]:
    solved: set[str] = set()
    for path in manifest_paths:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for entry in list(payload.get("problems") or []):
            problem_id = str(entry.get("problem_id") or "").strip()
            if problem_id:
                solved.add(problem_id)
    return solved


def select_problems(
    records: list[ProofBenchProblem],
    *,
    problem_ids: list[str],
    level: str,
    categories: list[str],
    limit: int,
    exclude_ids: set[str],
) -> list[ProofBenchProblem]:
    by_id = {record.problem_id: record for record in records}
    if problem_ids:
        missing = [problem_id for problem_id in problem_ids if problem_id not in by_id]
        if missing:
            raise ValueError(f"Unknown ProofBench problem id(s): {', '.join(missing)}")
        return [by_id[problem_id] for problem_id in problem_ids]

    selected: list[ProofBenchProblem] = []
    category_set = {category.strip().lower() for category in categories if category.strip()}
    for record in records:
        if record.problem_id in exclude_ids:
            continue
        if level and record.level.lower() != level.lower():
            continue
        if category_set and record.category.lower() not in category_set:
            continue
        selected.append(record)
        if limit > 0 and len(selected) >= limit:
            break
    return selected


def _write_statement(record: ProofBenchProblem, path: Path) -> None:
    write_text(
        path,
        "\n".join(
            [
                f"# {record.problem_id}",
                "",
                f"- Category: {record.category}",
                f"- Level: {record.level}",
                f"- Source: {record.source}",
                "",
                "## Problem",
                "",
                record.problem,
                "",
            ]
        ),
    )


def _write_reference(record: ProofBenchProblem, path: Path) -> None:
    write_text(
        path,
        "\n".join(
            [
                f"# Reference Material for {record.problem_id}",
                "",
                "This file contains ProofBench reference material. Use it only when the",
                "campaign is configured to allow reference-assisted formalization.",
                "",
                "## Short Answer",
                "",
                record.short_answer or "<empty>",
                "",
                "## Reference Solution",
                "",
                record.solution or "<empty>",
                "",
                "## Grading Guidelines",
                "",
                record.grading_guidelines or "<empty>",
                "",
            ]
        ),
    )


def _write_lake_project(workspace: Path, module_name: str) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    write_text(
        workspace / "lakefile.lean",
        "\n".join(
            [
                "import Lake",
                "open Lake DSL",
                "",
                f"package {module_name} where",
                "",
                "require mathlib from git",
                f'  "https://github.com/leanprover-community/mathlib4" @ "{MATHLIB_REV}"',
                "",
                "@[default_target]",
                f"lean_lib {module_name}",
                "",
            ]
        ),
    )
    write_text(workspace / "lean-toolchain", LEAN_TOOLCHAIN + "\n")
    manifest = REPO_ROOT / "benchmark_runs/imo_proofbench_parallel_5/lean/lake-manifest.json"
    if manifest.exists():
        shutil.copyfile(manifest, workspace / "lake-manifest.json")
    cached_packages = REPO_ROOT / "benchmark_runs/imo_proofbench_parallel_5/lean/.lake/packages"
    local_lake = workspace / ".lake"
    local_packages = local_lake / "packages"
    if cached_packages.exists() and not local_packages.exists():
        local_lake.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(cached_packages.resolve(), local_packages, target_is_directory=True)
        except FileExistsError:
            pass


def _curated_source_for(record: ProofBenchProblem, module_name: str, target_theorem: str) -> str:
    source = CURATED_TARGETS.get(record.problem_id)
    if source is None:
        raise ValueError(
            f"No curated Lean target scaffold for {record.problem_id}. "
            "Pass explicit curated ids or add a target scaffold before running formalization."
        )
    source = source.replace(module_name_for_problem(record.problem_id), module_name)
    source = re.sub(r"(?m)^theorem\s+[A-Za-z_][A-Za-z0-9_']*", f"theorem {target_theorem}", source, count=1)
    return source


def _write_target_scaffold(
    *,
    record: ProofBenchProblem,
    workspace: Path,
    module_name: str,
    target_theorem: str,
) -> tuple[Path, Path]:
    source = _curated_source_for(record, module_name, target_theorem)
    module_dir = workspace / module_name
    target_file = module_dir / "Main.lean"
    write_text(target_file, source)
    write_text(workspace / f"{module_name}.lean", f"import {module_name}.Main\n")
    header = extract_lean_declaration_header(source, target_theorem)
    if not header:
        raise ValueError(f"Could not extract expected target header for {record.problem_id}.")
    expected_header_path = workspace.parent / "expected_target_header.lean"
    write_text(expected_header_path, str(header["header"]).strip() + "\n")
    return target_file.relative_to(workspace), expected_header_path


def prepare_problem(
    *,
    record: ProofBenchProblem,
    run_root: Path,
    include_reference: bool,
) -> PreparedProblem:
    problem_dir = run_root / "problems" / record.slug
    input_dir = problem_dir / "input"
    reference_dir = problem_dir / "reference"
    workspace = problem_dir / "lean"
    module_name = module_name_for_problem(record.problem_id)
    target_theorem = theorem_name_for_problem(record.problem_id)

    write_json(input_dir / "problem.json", record.to_json())
    statement_path = input_dir / "statement.md"
    reference_path = reference_dir / "reference_solution_and_rubric.md"
    _write_statement(record, statement_path)
    _write_reference(record, reference_path)
    _write_lake_project(workspace, module_name)
    target_file, expected_header_path = _write_target_scaffold(
        record=record,
        workspace=workspace,
        module_name=module_name,
        target_theorem=target_theorem,
    )
    context_paths = [reference_path] if include_reference else []
    context_paths.append(expected_header_path)
    write_json(
        problem_dir / "campaign_seed.json",
        {
            "problem_id": record.problem_id,
            "level": record.level,
            "category": record.category,
            "workspace": str(workspace),
            "target_file": str(target_file),
            "target_theorem": target_theorem,
            "statement_path": str(statement_path),
            "reference_path": str(reference_path),
            "expected_header_path": str(expected_header_path),
            "reference_context_enabled": include_reference,
        },
    )
    return PreparedProblem(
        record=record,
        problem_dir=problem_dir,
        workspace=workspace,
        statement_path=statement_path,
        reference_path=reference_path,
        target_file=target_file,
        target_theorem=target_theorem,
        expected_header_path=expected_header_path,
        context_paths=context_paths,
    )


def _configure_runner(runner: CampaignLoopRunner, *, model: str | None, reasoning_effort: str | None) -> None:
    if model:
        runner.proof_lab_runner.backend_model = model
        runner.lean_formalizer_runner.backend_model = model
        runner.global_supervisor.backend_model = model
    if reasoning_effort:
        runner.proof_lab_runner.backend_reasoning_effort = reasoning_effort
        runner.lean_formalizer_runner.backend_reasoning_effort = reasoning_effort
        runner.global_supervisor.backend_reasoning_effort = reasoning_effort


def _effective_supervisor_backend(args: argparse.Namespace) -> str:
    supervisor_backend = str(getattr(args, "supervisor_backend", "auto") or "auto")
    if supervisor_backend == "auto":
        return args.backend
    return supervisor_backend


def run_prepared_problem(prepared: PreparedProblem, args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    runner = CampaignLoopRunner(repo_root=REPO_ROOT)
    _configure_runner(runner, model=args.model, reasoning_effort=args.reasoning_effort)
    statement = prepared.statement_path.read_text(encoding="utf-8")
    report = runner.run(
        statement=statement,
        context_paths=prepared.context_paths,
        workspace=prepared.workspace,
        final_target_theorem=prepared.target_theorem,
        initial_target_theorem=prepared.target_theorem,
        target_file=prepared.target_file,
        build_command=shlex.split(args.build_command),
        backend=args.backend,
        mode=args.mode,
        rounds=args.rounds,
        time_budget_sec=args.time_budget_per_problem,
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
        output_root=prepared.problem_dir / "runs",
        run_name="campaign",
        max_stalled_rounds=args.max_stalled_rounds,
        round_time_budget_sec=args.round_time_budget,
        expected_target_header=prepared.expected_header_path.read_text(encoding="utf-8"),
        supervisor_backend=_effective_supervisor_backend(args),
        supervisor_on_stall=not args.no_supervisor_on_stall,
        supervisor_every_rounds=args.supervisor_every_rounds,
        supervisor_timeout_sec=args.supervisor_timeout,
        math_tools_profile=args.math_tools_profile,
        install_missing_math_tools=not args.no_install_missing_math_tools,
        run_math_tool_smoke=not args.no_math_tool_smoke,
    )
    payload = {
        "problem_id": prepared.record.problem_id,
        "level": prepared.record.level,
        "category": prepared.record.category,
        "status": report.get("status"),
        "stop_reason": report.get("stop_reason"),
        "run_dir": report.get("run_dir"),
        "summary_path": report.get("summary_path"),
        "workspace": str(prepared.workspace),
        "target_file": str(prepared.target_file),
        "target_theorem": prepared.target_theorem,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "campaign_report": report,
    }
    write_json(prepared.problem_dir / "campaign_result.json", payload)
    return payload


def _new_run_root(output_root: Path, run_name: str | None) -> Path:
    base = slugify(run_name or f"imo-proofbench-campaign-{utc_now_iso()}")
    output_root.mkdir(parents=True, exist_ok=True)
    candidate = output_root / base
    if not candidate.exists():
        return candidate
    suffix = 2
    while True:
        candidate = output_root / f"{base}-{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def write_state(path: Path, payload: dict[str, Any]) -> None:
    write_json(path, payload)


def run_campaign(args: argparse.Namespace) -> dict[str, Any]:
    records = load_proofbench(args.proofbench_csv)
    solved = load_solved_problem_ids(args.exclude_solved_manifest) if args.exclude_solved else set()
    selected = select_problems(
        records,
        problem_ids=args.problem_id,
        level=args.level,
        categories=args.category,
        limit=args.limit,
        exclude_ids=solved,
    )
    if not selected:
        raise ValueError("No ProofBench problems selected.")

    run_root = _new_run_root(args.output_root, args.run_name)
    run_root.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_problem(record=record, run_root=run_root, include_reference=not args.hide_reference) for record in selected]
    config = {
        "generated_at": utc_now_iso(),
        "run_root": str(run_root),
        "proofbench_csv": str(args.proofbench_csv),
        "backend": args.backend,
        "mode": args.mode,
        "level": args.level,
        "selected_problem_ids": [record.problem_id for record in selected],
        "exclude_solved": args.exclude_solved,
        "excluded_problem_ids": sorted(solved),
        "parallelism": args.parallelism,
        "rounds": args.rounds,
        "time_budget_per_problem": args.time_budget_per_problem,
        "supervisor_backend": _effective_supervisor_backend(args),
        "supervisor_on_stall": not args.no_supervisor_on_stall,
        "supervisor_every_rounds": args.supervisor_every_rounds,
        "supervisor_timeout": args.supervisor_timeout,
        "math_tools_profile": args.math_tools_profile,
        "install_missing_math_tools": not args.no_install_missing_math_tools,
        "run_math_tool_smoke": not args.no_math_tool_smoke,
        "include_reference": not args.hide_reference,
        "model": args.model or "",
        "reasoning_effort": args.reasoning_effort or "",
    }
    write_json(run_root / "manifest.json", config)
    state: dict[str, Any] = {
        **config,
        "status": "prepared" if args.dry_run else "running",
        "problems": [
            {
                "problem_id": item.record.problem_id,
                "level": item.record.level,
                "category": item.record.category,
                "problem_dir": str(item.problem_dir),
                "workspace": str(item.workspace),
                "target_theorem": item.target_theorem,
                "status": "prepared" if args.dry_run else "queued",
            }
            for item in prepared
        ],
        "results": [],
    }
    write_state(run_root / "state.json", state)
    if args.dry_run:
        return state

    results: list[dict[str, Any]] = []
    by_id = {item.record.problem_id: item for item in prepared}
    status_by_id = {item.record.problem_id: "queued" for item in prepared}
    max_workers = max(1, min(args.parallelism, len(prepared)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_id = {
            executor.submit(run_prepared_problem, item, args): item.record.problem_id
            for item in prepared
        }
        for problem_id in future_to_id.values():
            status_by_id[problem_id] = "running"
        state = {
            **config,
            "status": "running",
            "updated_at": utc_now_iso(),
            "problems": [
                {
                    "problem_id": item.record.problem_id,
                    "level": item.record.level,
                    "category": item.record.category,
                    "problem_dir": str(item.problem_dir),
                    "workspace": str(item.workspace),
                    "target_theorem": item.target_theorem,
                    "status": status_by_id[item.record.problem_id],
                }
                for item in prepared
            ],
            "results": results,
        }
        write_state(run_root / "state.json", state)
        for future in concurrent.futures.as_completed(future_to_id):
            problem_id = future_to_id[future]
            try:
                result = future.result()
                results.append(result)
                status_by_id[problem_id] = str(result.get("status") or "completed")
            except Exception as exc:  # pragma: no cover - exercised by real campaigns.
                item = by_id[problem_id]
                result = {
                    "problem_id": problem_id,
                    "status": "error",
                    "error": repr(exc),
                    "problem_dir": str(item.problem_dir),
                    "workspace": str(item.workspace),
                }
                results.append(result)
                status_by_id[problem_id] = "error"
                write_json(item.problem_dir / "campaign_result.json", result)
            state = {
                **config,
                "status": "running",
                "updated_at": utc_now_iso(),
                "problems": [
                    {
                        "problem_id": item.record.problem_id,
                        "level": item.record.level,
                        "category": item.record.category,
                        "problem_dir": str(item.problem_dir),
                        "workspace": str(item.workspace),
                        "target_theorem": item.target_theorem,
                        "status": status_by_id[item.record.problem_id],
                    }
                    for item in prepared
                ],
                "results": results,
            }
            write_state(run_root / "state.json", state)

    final_status = "verified" if results and all(result.get("status") == "verified" for result in results) else "partial"
    final_state = {
        **config,
        "status": final_status,
        "completed_at": utc_now_iso(),
        "problems": [
            {
                "problem_id": item.record.problem_id,
                "level": item.record.level,
                "category": item.record.category,
                "problem_dir": str(item.problem_dir),
                "workspace": str(item.workspace),
                "target_theorem": item.target_theorem,
                "status": status_by_id[item.record.problem_id],
            }
            for item in prepared
        ],
        "results": sorted(results, key=lambda result: str(result.get("problem_id") or "")),
    }
    write_json(run_root / "state.json", final_state)
    write_json(run_root / "summary.json", final_state)
    write_text(run_root / "summary.md", render_summary(final_state))
    return final_state


def render_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# IMO-ProofBench Campaign Summary",
        "",
        f"- Status: {payload.get('status')}",
        f"- Backend: {payload.get('backend')}",
        f"- Mode: {payload.get('mode')}",
        f"- Run root: `{payload.get('run_root')}`",
        f"- Time budget per problem: {payload.get('time_budget_per_problem')} seconds",
        "",
        "## Problems",
        "",
    ]
    for result in list(payload.get("results") or []):
        lines.append(
            "- `{problem_id}`: {status} ({stop_reason}) -> `{summary_path}`".format(
                problem_id=result.get("problem_id"),
                status=result.get("status"),
                stop_reason=result.get("stop_reason") or result.get("error") or "",
                summary_path=result.get("summary_path") or "",
            )
        )
    if not payload.get("results"):
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run an automated AMRA campaign over selected Google DeepMind IMO-ProofBench problems."
    )
    parser.add_argument("--proofbench-csv", type=Path, default=DEFAULT_PROOFBENCH_CSV)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--problem-id", action="append", default=[], help="Explicit ProofBench id. Repeatable.")
    parser.add_argument("--level", default="IMO-hard")
    parser.add_argument("--category", action="append", default=[], help="Optional category filter. Repeatable.")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--exclude-solved", action="store_true")
    parser.add_argument("--exclude-solved-manifest", type=Path, action="append", default=[DEFAULT_SOLVED_MANIFEST])
    parser.add_argument("--hide-reference", action="store_true", help="Do not pass ProofBench reference solution as context.")
    parser.add_argument("--backend", choices=("codex", "none"), default="codex")
    parser.add_argument("--mode", choices=("auto", "hybrid", "proof-lab", "lean-formalizer"), default="hybrid")
    parser.add_argument("--parallelism", type=int, default=2)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--time-budget-per-problem", type=int, default=14_400)
    parser.add_argument("--round-time-budget", type=int, default=0)
    parser.add_argument("--proof-attempts", type=int, default=4)
    parser.add_argument("--proof-audits", type=int, default=2)
    parser.add_argument("--proof-attempt-timeout", type=int, default=900)
    parser.add_argument("--proof-audit-timeout", type=int, default=450)
    parser.add_argument("--proof-grounding-timeout", type=int, default=600)
    parser.add_argument("--formalizer-attempts", type=int, default=10)
    parser.add_argument("--formalizer-attempt-timeout", type=int, default=1800)
    parser.add_argument("--formalizer-build-timeout", type=int, default=600)
    parser.add_argument("--max-stalled-rounds", type=int, default=0)
    parser.add_argument(
        "--supervisor-backend",
        choices=("auto", "codex", "none"),
        default="auto",
        help="Global read-only strategy reviewer backend. auto follows --backend.",
    )
    parser.add_argument(
        "--no-supervisor-on-stall",
        action="store_true",
        help="Disable automatic global strategy review when a formalizer round stalls.",
    )
    parser.add_argument(
        "--supervisor-every-rounds",
        type=int,
        default=2,
        help="Run the global supervisor every N rounds. 0 leaves only stall-triggered review.",
    )
    parser.add_argument("--supervisor-timeout", type=int, default=900)
    parser.add_argument(
        "--math-tools-profile",
        choices=("essential", "extended", "full"),
        default="essential",
        help="Install/check this AMRA math tool profile before each proof campaign.",
    )
    parser.add_argument(
        "--no-install-missing-math-tools",
        action="store_true",
        help="Disable automatic installation of missing math tools in the selected profile.",
    )
    parser.add_argument(
        "--no-math-tool-smoke",
        action="store_true",
        help="Skip math tool smoke checks after install/availability detection.",
    )
    parser.add_argument("--build-command", default="lake build")
    parser.add_argument("--source-first", action="store_true")
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--model", default=None)
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_campaign(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
