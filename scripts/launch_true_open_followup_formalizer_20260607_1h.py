#!/usr/bin/env python3
"""Launch narrow 1h Lean formalizer follow-ups for the two unfinished true-open tracks."""

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
SOURCE_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_targeted_attack_20260607_2h"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_followup_formalizer_20260607_1h"

TIME_BUDGET_SECONDS = 60 * 60
ATTEMPT_TIMEOUT_SECONDS = 15 * 60
BUILD_TIMEOUT_SECONDS = 4 * 60


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


def resource_prefix() -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    return [
        "systemd-run",
        "--user",
        "--scope",
        "-p",
        "MemoryMax=6G",
        "-p",
        "MemorySwapMax=8G",
        "-p",
        "CPUQuota=150%",
    ]


def nice_prefix(extra_seconds: int = 300) -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + extra_seconds}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


CHVATAL_HEADER = """theorem rank_three_tau_three_trace_graph_raw_excess_bound
    {β : Type*} [DecidableEq β]
    (H : Fin 3 → Finset (Finset β)) (K : Fin 3 → Finset β)
    (hedge : ∀ i e, e ∈ H i → e.card = 2)
    (hHne : ∀ i, (H i).Nonempty)
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
    2 * (∑ i : Fin 3, (H i).card) + ∑ i : Fin 3, (K i).card
      ≤ 9 + ∑ i : Fin 3, ((H i).biUnion fun e => e).card"""

GENERAL_HEADER = """lemma zmod_p_minus_one_choose_factor_expansion_mod_p4
    (p k : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p - 1).choose k : R)) =
      (-1 : R) ^ k *
        Finset.prod (Finset.Icc 1 k)
          (fun j => 1 - (p : R) * (j : R)⁻¹)"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "chvatal-raw-excess-formalizer",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal raw-excess trace graph formalizer",
        "target_theorem": "rank_three_tau_three_trace_graph_raw_excess_bound",
        "header": CHVATAL_HEADER,
        "statement": "\n".join(
            [
                "# Chvatal raw-excess follow-up formalizer",
                "",
                "Prove exactly the following theorem. Do not attack the full Chvatal theorem in this run.",
                "",
                "```lean",
                CHVATAL_HEADER,
                "```",
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
        "build_command": "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        "contexts": existing(
            SOURCE_ROOT / "chvatal_next_formalizer_target_20260607.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-full-main-theorem-attack"
            / "chvatal-full-main-theorem-attack-targeted-2h"
            / "supervisor"
            / "round-007"
            / "decision.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-full-main-theorem-attack"
            / "chvatal-full-main-theorem-attack-targeted-2h"
            / "proof_lab"
            / "round-006"
            / "attempts"
            / "attempt_001_output.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-full-main-theorem-attack"
            / "chvatal-full-main-theorem-attack-targeted-2h"
            / "proof_lab"
            / "round-006"
            / "attempts"
            / "attempt_002_output.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "general-supercongruence-p4-binomial-formalizer",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence p^4 binomial formalizer",
        "target_theorem": "zmod_p_minus_one_choose_factor_expansion_mod_p4",
        "header": GENERAL_HEADER,
        "statement": "\n".join(
            [
                "# General supercongruence p^4 follow-up formalizer",
                "",
                "Prove exactly the following lemma. Keep the modulus as `p ^ 4`.",
                "",
                "```lean",
                GENERAL_HEADER,
                "```",
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
        "build_command": "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
        "contexts": existing(
            SOURCE_ROOT / "general_supercongruence_next_formalizer_target_20260607.md",
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-p4-semantic-bridge"
            / "general-supercongruence-p4-semantic-bridge-targeted-2h"
            / "supervisor"
            / "round-017"
            / "decision.md",
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-p4-semantic-bridge"
            / "general-supercongruence-p4-semantic-bridge-targeted-2h"
            / "proof_lab"
            / "round-017"
            / "summary.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
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
        *resource_prefix(),
        *nice_prefix(),
        sys.executable,
        "run.py",
        "run-lean-formalizer",
        "--workspace",
        str(target["workspace"]),
        "--statement-file",
        str(statement_file),
        "--target-theorem",
        str(target["target_theorem"]),
        "--target-file",
        str(target["target_file"]),
        "--expected-target-header-file",
        str(header_file),
        "--backend",
        "codex",
        "--closed-book",
        "--attempts",
        "3",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--attempt-timeout",
        str(ATTEMPT_TIMEOUT_SECONDS),
        "--build-timeout",
        str(BUILD_TIMEOUT_SECONDS),
        "--build-command",
        str(target["build_command"]),
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-1h",
        "--reasoning-effort",
        "high",
        "--max-stalled-attempts",
        "2",
        "--rollback-failed-attempts",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
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
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_CPU_SECONDS": "1200",
            "ARA_MATH_MAX_LOAD_PER_CPU": "6.0",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "20",
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
        "source_root": str(SOURCE_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "attempt_timeout_seconds": ATTEMPT_TIMEOUT_SECONDS,
        "build_timeout_seconds": BUILD_TIMEOUT_SECONDS,
        "mode": "narrow Lean formalizer follow-up",
        "resource_policy": {
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "lean": "two Lean formalizer tracks only; LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
            "rollback": "rollback_failed_attempts enabled",
            "external_search": "disabled via --closed-book",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
