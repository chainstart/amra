#!/usr/bin/env python3
"""Launch the 2026-06-08 continuation Lean formalizer round."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_next_round_20260608_continuation"
TIME_BUDGET_SECONDS = 2 * 60 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def bounded_prefix(extra_seconds: int = 600) -> list[str]:
    command = [
        "timeout",
        f"{TIME_BUDGET_SECONDS + extra_seconds}s",
        "prlimit",
        "--as=22000000000",
        "--",
        "nice",
        "-n",
        "10",
    ]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


GENERAL_HEADER = """lemma zmod_p_add_choose_factor_expansion_mod_p4_aux
    (p t : ℕ) (hp : p.Prime) (ht : t + 1 ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p + t).choose (t + 1) : R)) =
      (p : R) * (((t + 1 : ℕ) : R)⁻¹) *
        Finset.prod (Finset.Icc 1 t)
          (fun j => 1 + (p : R) * (j : R)⁻¹)"""


CHVATAL_HEADER = """theorem rank_three_tau_three_trace_graph_degree_le_two
    {β : Type*} [DecidableEq β]
    (H : Fin 3 → Finset (Finset β)) (K : Fin 3 → Finset β)
    (hedge : ∀ i e, e ∈ H i → e.card = 2)
    (hcross :
      ∀ i j, i ≠ j →
        ∀ e ∈ H i, ∀ f ∈ H j, (e ∩ f).Nonempty)
    (hKcore : ∀ i x, x ∈ K i → ∀ e ∈ H i, x ∈ e)
    (hno_two :
      let V := fun i => (H i).biUnion fun e => e
      let used := Finset.univ.biUnion fun i : Fin 3 => V i ∪ K i
      ∀ i x, x ∈ used →
        ((K i).erase x).Nonempty ∨
          ∃ j, j ≠ i ∧ ∃ e ∈ H j, x ∉ e) :
    ∀ i x, ({e ∈ H i | x ∈ e}.card ≤ 2)"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "general-p-add-choose-factor",
        "problem_id": "formal-conjectures-general-supercongruence",
        "target_theorem": "zmod_p_add_choose_factor_expansion_mod_p4_aux",
        "header": GENERAL_HEADER,
        "statement": "\n".join(
            [
                "# General supercongruence upper-binomial bridge formalizer",
                "",
                "Prove exactly this next bridge in namespace `OeisA357513NextRound20260606`:",
                "",
                "```lean",
                GENERAL_HEADER,
                "```",
                "",
                "Use the already verified `zmod_unit_denominator_for_range` and lower-binomial bridge.",
                "Do not attempt `OeisA357513.general_supercongruence` directly in this round.",
            ]
        ),
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "04_general_supercongruence_zmod_cast.lean",
        "build_command": "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
        "contexts": existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_mixed/runs/general-supercongruence-next-bridge-prooflab/general-supercongruence-next-bridge-prooflab-2h/supervisor/round-017/decision.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_mixed/runs/general-supercongruence-next-bridge-prooflab/general-supercongruence-next-bridge-prooflab-2h/proof_lab/round-017/summary.md",
        ),
    },
    {
        "priority": 2,
        "slug": "chvatal-rank-three-degree",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "target_theorem": "rank_three_tau_three_trace_graph_degree_le_two",
        "header": CHVATAL_HEADER,
        "statement": "\n".join(
            [
                "# Chvatal rank-three trace graph degree bound formalizer",
                "",
                "Prove exactly this theorem. `three_spokes_crossing_edge_contains_center` is already verified and should be reused.",
                "",
                "```lean",
                CHVATAL_HEADER,
                "```",
                "",
                "Do not attack `Chvatal.exists_maximal_star` directly. This is the next local blocker for the raw-excess route.",
            ]
        ),
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "06_exists_maximal_star_rank_two.lean",
        "build_command": "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_mixed/runs/chvatal-three-spokes-formalizer/chvatal-three-spokes-formalizer-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_mixed/runs/chvatal-three-spokes-formalizer/chvatal-three-spokes-formalizer-2h/lean_formalizer/round-001-three-spokes-crossing-edge-contains-center/summary.md",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/chvatal-smaller-target-reassessment/chvatal-smaller-target-reassessment-2h/proof_lab/round-002/grounding/source_grounding_meta.json",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/chvatal-smaller-target-reassessment/chvatal-smaller-target-reassessment-2h/proof_lab/round-003/audits/audit_attempt_001_meta.json",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    header_file = RUN_ROOT / "headers" / f"{target['priority']:02d}-{target['slug']}.lean"
    write_text(statement_file, str(target["statement"]))
    write_text(header_file, str(target["header"]))

    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]
    cmd = [
        *bounded_prefix(),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
        "--backend",
        "codex",
        "--closed-book",
        "--source-first",
        "--mode",
        "lean-formalizer",
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        "2100",
        "--formalizer-attempts",
        "4",
        "--formalizer-attempt-timeout",
        "900",
        "--formalizer-build-timeout",
        "240",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "540",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--workspace",
        str(target["workspace"]),
        "--target-file",
        str(target["target_file"]),
        "--build-command",
        str(target["build_command"]),
        "--expected-target-header-file",
        str(header_file),
        "--final-target-theorem",
        str(target["target_theorem"]),
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-2h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]
    return {
        **target,
        "statement_file": str(statement_file),
        "header_file": str(header_file),
        "log_path": str(log_path),
        "output_root": str(output_root),
        "command": cmd,
    }


def start_target(target: dict[str, Any]) -> dict[str, Any]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "ARA_MATH_MAX_LOAD_PER_CPU": "6.0",
            "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "2048",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "20",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
        }
    )
    with log_path.open("ab") as log:
        proc = subprocess.Popen(
            target["command"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    write_text(RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid", str(proc.pid))
    return {
        "priority": target["priority"],
        "slug": target["slug"],
        "problem_id": target["problem_id"],
        "target_theorem": target["target_theorem"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "statement_file": target["statement_file"],
        "header_file": target["header_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "command": target["command"],
    }


def main() -> None:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "headers", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "mode": "two-track Lean formalizer continuation",
        "resource_policy": {
            "lean_heavy_max_parallel": 2,
            "lean_threads": "LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
            "memory_limit": "prlimit --as=22000000000 per launched loop",
            "external_search": "disabled via --closed-book",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
