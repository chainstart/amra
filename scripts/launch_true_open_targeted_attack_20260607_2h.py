#!/usr/bin/env python3
"""Launch a 2 hour targeted supervised attack for the three active true-open tracks."""

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
SOURCE_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_three_tier_20260606_4h"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_targeted_attack_20260607_2h"

TIME_BUDGET_SECONDS = 2 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 35 * 60


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


def nice_prefix(extra_seconds: int = 600) -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + extra_seconds}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "chvatal-full-main-theorem-attack",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal full main theorem",
        "mode": "proof-lab",
        "statement_source": SOURCE_ROOT / "statements" / "04-chvatal-full-main-theorem-attack.md",
        "final_target_theorem": "Chvatal.exists_maximal_star",
        "initial_target_theorem": "",
        "workspace": None,
        "target_file": None,
        "build_command": "lake build",
        "contexts": existing(
            SOURCE_ROOT / "chvatal_full_main_attack_plan_20260607.md",
            SOURCE_ROOT / "chvatal_rank_two_semantic_audit_20260607.md",
            SOURCE_ROOT / "manual_formalizer_round_20260607.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "wowii-conjecture19-bipartite-witness",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII Conjecture 19 bipartite witness",
        "mode": "lean-formalizer",
        "statement_source": SOURCE_ROOT / "statements" / "05-wowii-conjecture19-bipartite-witness-target.md",
        "final_target_theorem": "exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from",
        "initial_target_theorem": "diam_geodesic_neighbor_path_witness_bipartite",
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "05_wowii_conjecture19.lean",
        "build_command": "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
        "contexts": existing(
            SOURCE_ROOT / "wowii_conjecture19_next_formalizer_target_20260607.md",
            SOURCE_ROOT / "manual_formalizer_round_20260607.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
        ),
    },
    {
        "priority": 3,
        "slug": "general-supercongruence-p4-semantic-bridge",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence p^4 semantic bridge",
        "mode": "proof-lab",
        "statement_source": SOURCE_ROOT / "statements" / "06-general-supercongruence-p4-semantic-bridge.md",
        "final_target_theorem": "OeisA357513.general_supercongruence",
        "initial_target_theorem": "",
        "workspace": None,
        "target_file": None,
        "build_command": "lake build",
        "contexts": existing(
            SOURCE_ROOT / "general_supercongruence_semantic_bridge_audit_20260607.md",
            SOURCE_ROOT / "manual_formalizer_round_20260607.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_source = Path(target["statement_source"])
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, statement_source.read_text(encoding="utf-8"))

    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]
    cmd = [
        *resource_prefix(),
        *nice_prefix(),
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
        str(target["mode"]),
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        str(ROUND_TIME_BUDGET_SECONDS),
        "--proof-attempts",
        "2",
        "--proof-audits",
        "1",
        "--proof-attempt-timeout",
        "900",
        "--proof-audit-timeout",
        "360",
        "--proof-grounding-timeout",
        "420",
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
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-targeted-2h",
        "--reasoning-effort",
        "high",
    ]
    if target["final_target_theorem"]:
        cmd += ["--final-target-theorem", str(target["final_target_theorem"])]
    if target["initial_target_theorem"]:
        cmd += ["--initial-target-theorem", str(target["initial_target_theorem"])]
    if target["workspace"]:
        cmd += ["--workspace", str(target["workspace"])]
    if target["target_file"]:
        cmd += ["--target-file", str(target["target_file"])]
    if target["build_command"]:
        cmd += ["--build-command", str(target["build_command"])]
    for context in target["contexts"]:
        cmd += ["--context-file", context]

    return {
        **target,
        "statement_file": str(statement_file),
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
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
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
        "mode": target["mode"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "command": target["command"],
    }


def main() -> None:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "source_root": str(SOURCE_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "mode": "targeted supervised attack",
        "resource_policy": {
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "load_guard": "ARA_MATH_MAX_LOAD_PER_CPU=6.0",
            "lean": "WOWII is the only Lean formalizer track; LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1; max two heavy checks by policy",
            "external_search": "disabled via --closed-book",
        },
        "targets": launched,
    }
    shutil.copyfile(SOURCE_ROOT / "next_attack_queue_20260607.json", RUN_ROOT / "next_attack_queue_20260607.json")
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
