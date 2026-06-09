#!/usr/bin/env python3
"""Launch a 4 hour three-tier supervised proof loop for the three active true-open tracks."""

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
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_three_tier_20260606_4h"
PREV_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_three_followup_20260606_1h"

TIME_BUDGET_SECONDS = 4 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 45 * 60


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
        "slug": "general-supercongruence-product-lift",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence product lift",
        "top_goal": "Original supercongruence theorem from `formal-conjectures-general-supercongruence`.",
        "tier1": "Keep the original theorem as the top-level goal, but route proof work through the paired-factor product expansion modulo `p^2`.",
        "tier2": [
            "Use the closed lemmas `zmod_range_coprime_mod_square` and `zmod_pair_factor_collapse_mod_square` as completed context.",
            "First target: formulate and prove the finite-product version of pair collapse over `k = 1..p-1`.",
            "Second target: connect that product statement to the binomial/supercongruence expression.",
        ],
        "tier3": [
            "Tiny Lean probes may be used for exact `Finset.prod`/`ZMod` APIs.",
            "Do not spend a full round on the raw top theorem unless the product lemma has been closed or explicitly blocked.",
            "Required output each round: closed lemma, exact blocker, or supervisor-directed retarget.",
        ],
        "contexts": existing(
            PREV_ROOT / "manual_followup_20260606_after_1h.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/final.md",
            "artifacts/lean_workspaces/general_supercongruence/FormalConjectures/OEIS/357513.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "wowii-conjecture19-witness-assembly",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII Conjecture 19 witness assembly",
        "top_goal": "`exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from` as the local top theorem for the original Conjecture 19 route.",
        "tier1": "Assemble the diameter-geodesic witness from path vertices plus independent neighbors.",
        "tier2": [
            "Use the closed helpers `path_vertices_erase_one_card_eq_length` and `diam_geodesic_neighbor_path_witness_disjoint`.",
            "First target: prove `diam_geodesic_neighbor_path_witness_card` or the smallest equivalent cardinal lemma.",
            "Second target: prove the induced bipartite condition for the chosen witness.",
        ],
        "tier3": [
            "Tiny Lean probes may be used only for SimpleGraph/Finset API shape.",
            "Supervisor should split any failed raw witness proof into cardinal, disjointness, and bipartite sublemmas.",
            "Required output each round: next theorem declaration/proof patch or exact API obstruction.",
        ],
        "contexts": existing(
            PREV_ROOT / "manual_followup_20260606_after_1h.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
        ),
    },
    {
        "priority": 3,
        "slug": "exists-maximal-star-rank-two-structure",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal rank-two structure theorem",
        "top_goal": "`exists_maximal_star_rank_two` as the local top theorem for the rank-two Chvatal route.",
        "tier1": "Prove the main theorem by the common-vertex branch and the triangle branch.",
        "tier2": [
            "Use the closed helpers `rank_two_intersecting_no_common_vertex_all_card_two`, `exists_star_maximizer`, and `triangle_star_three_of_decreasing`.",
            "First target: prove that a rank-two intersecting family without common vertex contains a triangle of two-element members.",
            "Second target: combine the common-vertex branch and triangle branch against the maximal star center.",
        ],
        "tier3": [
            "Tiny Lean probes may be used for Finset family/cardinality APIs.",
            "Supervisor should reject broad attempts that do not consume the closed helper lemmas.",
            "Required output each round: Lean-ready structural lemma, proof patch, or exact missing hypothesis.",
        ],
        "contexts": existing(
            PREV_ROOT / "manual_followup_20260606_after_1h.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Three-tier Supervised Proof Loop: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `true_open_three_tier_20260606_4h`",
            "",
            "Run policy:",
            "- Keep the original/top theorem as the target, but do not run a blind raw-top proof search.",
            "- Use three-tier routing: top theorem -> structural decomposition -> current Lean/NL sublemma.",
            "- Use global supervisor every round; supervisor may retarget only inside the declared tier structure.",
            "- Proof-lab / natural-language proof planning is the primary loop.",
            "- Lean use is cautious: tiny theorem-shape probes or single-file checks only; no broad `lake build`.",
            "- Heavy Lean concurrency policy: at most two heavy Lean checks may be active globally; each probe uses `LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1`.",
            "- Required final output: exact closed lemma or blocker, current tier, next target, and whether manual intervention is needed.",
            "",
            "Tier 0: top goal",
            target["top_goal"],
            "",
            "Tier 1: decomposition",
            target["tier1"],
            "",
            "Tier 2: current sublemma queue",
            *[f"- {item}" for item in target["tier2"]],
            "",
            "Tier 3: execution constraints",
            *[f"- {item}" for item in target["tier3"]],
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
        "1200",
        "--proof-audit-timeout",
        "450",
        "--proof-grounding-timeout",
        "600",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "600",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(RUN_ROOT / "runs" / target["slug"]),
        "--run-name",
        f"{target['slug']}-three-tier-supervised-4h",
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
        "mode": "three-tier proof-lab NL supervised",
        "tier_policy": {
            "tier0": "original/top theorem retained as target",
            "tier1": "structural decomposition",
            "tier2": "current Lean/NL sublemma queue",
            "tier3": "execution constraints and supervisor retargeting",
        },
        "resource_policy": {
            "supervisor": "codex every round, 600s timeout",
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "load_guard": "ARA_MATH_MAX_LOAD_PER_CPU=6.0",
            "lean": "single-file/tiny probes only; LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1; max two heavy checks by policy",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
