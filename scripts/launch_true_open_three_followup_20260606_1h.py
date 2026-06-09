#!/usr/bin/env python3
"""Launch a 1 hour supervised proof/NL loop for three active true-open tracks."""

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
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_three_followup_20260606_1h"
TIME_BUDGET_SECONDS = 60 * 60
ROUND_TIME_BUDGET_SECONDS = 25 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def existing(*paths: str) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / raw
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


def nice_prefix() -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + 600}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "general-supercongruence-pair-collapse",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence paired factor collapse",
        "focus": """Use the verified lemmas in `04_general_supercongruence_zmod_cast.lean` as completed context.
Current target: `zmod_pair_factor_collapse_mod_square`.
First task: determine the exact Lean statement with the necessary unit/coprimality hypothesis on `k`, because division in `ZMod (p^2)` is not valid for arbitrary `k`.
Allowed: tiny Lean probes only.
Required final output: a Lean-ready theorem declaration plus proof skeleton, or the first exact API/assumption mismatch.""",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/runs/general-supercongruence-zmod-cast/general-supercongruence-zmod-cast-nl-supervised-4h/supervisor/round-155/decision.md",
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/final.md",
            "artifacts/lean_workspaces/general_supercongruence/FormalConjectures/OEIS/357513.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "wowii-conjecture19-diam-witness",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII Conjecture 19 diameter geodesic witness",
        "focus": """Use the verified `path_vertices_erase_one_card_eq_length` helper as completed context.
Current target: `exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from`.
Split before proving: construct the candidate witness set, prove the induced bipartite condition, and prove the cardinal inequality.
Allowed: tiny Lean probes only.
Required final output: the next smallest Lean theorem declaration/proof skeleton, or the first exact obstruction.""",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/runs/wowii-conjecture19-path-helper/wowii-conjecture19-path-helper-nl-supervised-4h/supervisor/round-159/decision.md",
        ),
    },
    {
        "priority": 3,
        "slug": "exists-maximal-star-rank-two-main",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal rank-two main checkpoint",
        "focus": """Use the verified `rank_two_intersecting_no_common_vertex_all_card_two` helper as completed context.
Current target: `exists_maximal_star_rank_two`.
Split by cases: if `G` has a common vertex, star bound is direct; otherwise use the proved card=2 helper and the earlier pairwise-intersecting two-set common-vertex-or-triangle theorem.
Allowed: tiny Lean probes only.
Required final output: a Lean proof skeleton for `exists_maximal_star_rank_two`, or the first exact missing helper/API mismatch.""",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/runs/exists-maximal-star-rank-two-helper/exists-maximal-star-rank-two-helper-nl-supervised-4h/supervisor/round-156/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 1h Follow-up: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `true_open_three_followup_20260606_1h`",
            "",
            "Run policy:",
            "- Use global supervisor every round.",
            "- Proof-lab / natural-language proof planning only.",
            "- Do not use Lean-heavy formalizer or broad `lake build`.",
            "- Tiny `lake env lean` probes are allowed only to check the current theorem shape.",
            "- Do not retarget to already closed helpers.",
            "",
            "Focus:",
            target["focus"],
            "",
        ]
    )


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, statement_for(target))
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
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
        "--search",
        "--source-first",
        "--mode",
        "proof-lab",
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
        "450",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "450",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(RUN_ROOT / "runs" / target["slug"]),
        "--run-name",
        f"{target['slug']}-nl-supervised-1h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]
    return {
        **target,
        "statement_file": str(statement_file),
        "log_path": str(log_path),
        "output_root": str(RUN_ROOT / "runs" / target["slug"]),
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
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "mode": "proof-lab NL supervised",
        "resource_policy": {
            "supervisor": "codex every round, 450s timeout",
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "load_guard": "ARA_MATH_MAX_LOAD_PER_CPU=6.0",
            "lean": "no heavy Lean lane; LEAN_NUM_THREADS=1 for tiny probes only",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
