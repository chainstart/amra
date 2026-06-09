#!/usr/bin/env python3
"""Launch the 2026-06-08 mixed next round for three true-open tracks."""

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
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_next_round_20260608_mixed"


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


def bounded_prefix(time_budget_seconds: int, extra_seconds: int = 600) -> list[str]:
    command = [
        "timeout",
        f"{time_budget_seconds + extra_seconds}s",
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


WOWII_HEADER = """theorem wowii19_formal_conjectures_original_shape
    [Fintype α] [DecidableEq α] [Nontrivial α]
    (G : SimpleGraph α) [DecidableRel G.Adj] (h_conn : G.Connected) :
    ⌊(∑ v ∈ Finset.univ, ((eccentricity G v).toNat : ℝ)) / (Fintype.card α : ℝ) +
      sSup (Set.range (indepNeighbors G))⌋ ≤ (b G : ℝ)"""


CHVATAL_HEADER = """lemma three_spokes_crossing_edge_contains_center
    {β : Type*} [DecidableEq β]
    {x : β} {e1 e2 e3 f : Finset β}
    (he1card : e1.card = 2) (he2card : e2.card = 2) (he3card : e3.card = 2)
    (hfcard : f.card = 2)
    (hx1 : x ∈ e1) (hx2 : x ∈ e2) (hx3 : x ∈ e3)
    (h12 : e1 ≠ e2) (h13 : e1 ≠ e3) (h23 : e2 ≠ e3)
    (hcross1 : (e1 ∩ f).Nonempty)
    (hcross2 : (e2 ∩ f).Nonempty)
    (hcross3 : (e3 ∩ f).Nonempty) :
    x ∈ f"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "wowii19-original-wrapper",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII 19 original-shape wrapper",
        "mode": "lean-formalizer",
        "time_budget_seconds": 60 * 60,
        "round_time_budget_seconds": 25 * 60,
        "formalizer_attempts": 4,
        "formalizer_attempt_timeout": 900,
        "formalizer_build_timeout": 240,
        "final_target_theorem": "wowii19_formal_conjectures_original_shape",
        "completed_target_theorems": ["wowii19_distEcc_sSup_indepNeighborsReal"],
        "header": WOWII_HEADER,
        "statement": "\n".join(
            [
                "# WOWII 19 original-shape wrapper",
                "",
                "Close the original-statement bridge inside the AMRA Lean package.",
                "",
                "Target theorem:",
                "```lean",
                WOWII_HEADER,
                "```",
                "",
                "Important context:",
                "- `SimpleGraph.wowii19_distEcc_sSup_indepNeighborsReal` is already Lean-verified.",
                "- The current AMRA package does not provide the raw FormalConjectures names `eccentricity` and `indepNeighbors`; add compatible noncomputable definitions in namespace `SimpleGraph` only if absent.",
                "- Prove the semantic bridges from `(eccentricity G v).toNat` to `vertexEccentricityNat G v` under connected finite graphs, and from `indepNeighbors` to `indepNeighborsReal`.",
                "- Do not reprove the core WOWII 19 inequality; use the verified theorem as the final mathematical input.",
                "- Keep the RHS as `(b G : ℝ)` because AMRA's `b` is the natural-valued largest induced bipartite size.",
            ]
        ),
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "05_wowii_conjecture19.lean",
        "build_command": "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture19.lean",
            "data/research_open/raw/formal_conjectures/FormalConjecturesForMathlib/Combinatorics/SimpleGraph/GraphConjectures/Invariants.lean",
            "data/research_open/raw/formal_conjectures/FormalConjecturesForMathlib/Combinatorics/SimpleGraph/GraphConjectures/Definitions.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
            "artifacts/open_problem_screening/latest/true_open_targeted_attack_20260607_2h/wowii19_original_semantic_audit_20260607.md",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/wowii19-dist-ecc-ssup-bridge/wowii19-dist-ecc-ssup-bridge-2h/summary.md",
        ),
    },
    {
        "priority": 2,
        "slug": "chvatal-three-spokes-formalizer",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal three-spokes finite-set lemma",
        "mode": "lean-formalizer",
        "time_budget_seconds": 2 * 60 * 60,
        "round_time_budget_seconds": 35 * 60,
        "formalizer_attempts": 4,
        "formalizer_attempt_timeout": 900,
        "formalizer_build_timeout": 240,
        "final_target_theorem": "three_spokes_crossing_edge_contains_center",
        "completed_target_theorems": ["exists_maximal_star_rank_two_original_quantifier_shape"],
        "header": CHVATAL_HEADER,
        "statement": "\n".join(
            [
                "# Chvatal three-spokes Lean formalizer",
                "",
                "Do not run another proof-lab reassessment. Prove exactly this finite `Finset` lemma, non-private:",
                "",
                "```lean",
                CHVATAL_HEADER,
                "```",
                "",
                "Proof plan:",
                "- Normalize each card-2 spoke containing `x` as `{x, a}`.",
                "- If `x ∉ f`, each crossing witness must be the corresponding non-`x` endpoint.",
                "- Pairwise distinct spokes force pairwise distinct endpoints.",
                "- A card-2 finset cannot contain three pairwise distinct endpoints.",
                "- After this theorem is verified, the next target is `rank_three_tau_three_trace_graph_degree_le_two`.",
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
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/chvatal-smaller-target-reassessment/chvatal-smaller-target-reassessment-2h/proof_lab/round-020/grounding/source_grounding_meta.json",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/chvatal-smaller-target-reassessment/chvatal-smaller-target-reassessment-2h/supervisor/round-020/decision.md",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/chvatal-smaller-target-reassessment/chvatal-smaller-target-reassessment-2h/summary.md",
        ),
    },
    {
        "priority": 3,
        "slug": "general-supercongruence-next-bridge-prooflab",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence next bridge",
        "mode": "proof-lab",
        "time_budget_seconds": 2 * 60 * 60,
        "round_time_budget_seconds": 35 * 60,
        "proof_attempts": 2,
        "proof_audits": 1,
        "proof_attempt_timeout": 900,
        "proof_audit_timeout": 360,
        "proof_grounding_timeout": 420,
        "final_target_theorem": "OeisA357513.general_supercongruence",
        "statement": "\n".join(
            [
                "# General supercongruence next bridge proof-lab",
                "",
                "Tier-0 target remains `OeisA357513.general_supercongruence`, but do not attack it directly in Lean.",
                "",
                "Already verified local bridge:",
                "- `zmod_p_minus_one_choose_factor_expansion_mod_p4` in `04_general_supercongruence_zmod_cast.lean`.",
                "",
                "This 2h round should identify and mathematically audit the next theorem-level bridge after that lemma.",
                "Preferred next-stage candidates:",
                "1. A full hypergeometric factor expansion for the summand in `u m (p - 1)` over `ZMod (p ^ 4)`.",
                "2. A denominator-clearing bridge connecting rational sums and `Rat.num.natAbs` to a `ZMod (p ^ 4)` statement.",
                "3. An odd harmonic pairing/cancellation lemma over `k` and `p-k`, with exact exception handling.",
                "",
                "Output requirement:",
                "- Produce one Lean-ready next theorem statement with assumptions, proof sketch, and exact source blockers.",
                "- Do not claim the current binomial bridge proves `general_supercongruence`.",
                "- Tiny Lean/API probes are allowed; broad Lean formalizer/lake build is not the point of this track.",
            ]
        ),
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "artifacts/open_problem_screening/latest/true_open_targeted_attack_20260607_2h/general_supercongruence_next_formalizer_target_20260607.md",
            "artifacts/open_problem_screening/latest/true_open_targeted_attack_20260607_2h/runs/general-supercongruence-p4-semantic-bridge/general-supercongruence-p4-semantic-bridge-targeted-2h/proof_lab/round-009/grounding/source_grounding_meta.json",
            "artifacts/open_problem_screening/latest/true_open_three_next_round_20260607_2h/runs/general-supercongruence-p4-binomial/general-supercongruence-p4-binomial-2h/summary.md",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, str(target["statement"]))

    header_file = None
    if target.get("header"):
        header_file = RUN_ROOT / "headers" / f"{target['priority']:02d}-{target['slug']}.lean"
        write_text(header_file, str(target["header"]))

    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]

    cmd = [
        *bounded_prefix(int(target["time_budget_seconds"])),
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
        str(target["time_budget_seconds"]),
        "--round-time-budget",
        str(target["round_time_budget_seconds"]),
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
        f"{target['slug']}-{target['time_budget_seconds'] // 3600}h",
        "--reasoning-effort",
        "high",
    ]

    if target["mode"] == "lean-formalizer":
        cmd += [
            "--workspace",
            str(target["workspace"]),
            "--target-file",
            str(target["target_file"]),
            "--build-command",
            str(target["build_command"]),
            "--formalizer-attempts",
            str(target["formalizer_attempts"]),
            "--formalizer-attempt-timeout",
            str(target["formalizer_attempt_timeout"]),
            "--formalizer-build-timeout",
            str(target["formalizer_build_timeout"]),
        ]
        if header_file is not None:
            cmd += ["--expected-target-header-file", str(header_file)]
    else:
        cmd += [
            "--proof-attempts",
            str(target["proof_attempts"]),
            "--proof-audits",
            str(target["proof_audits"]),
            "--proof-attempt-timeout",
            str(target["proof_attempt_timeout"]),
            "--proof-audit-timeout",
            str(target["proof_audit_timeout"]),
            "--proof-grounding-timeout",
            str(target["proof_grounding_timeout"]),
        ]

    if target.get("final_target_theorem"):
        cmd += ["--final-target-theorem", str(target["final_target_theorem"])]
    for theorem in target.get("completed_target_theorems", []):
        cmd += ["--completed-target-theorem", str(theorem)]
    for context in target["contexts"]:
        cmd += ["--context-file", context]

    return {
        **target,
        "statement_file": str(statement_file),
        "header_file": str(header_file) if header_file else None,
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
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
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
        "mode": target["mode"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "time_budget_seconds": target["time_budget_seconds"],
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
        "mode": "mixed lean-formalizer/proof-lab campaign loop",
        "resource_policy": {
            "lean_heavy_tracks": ["wowii19-original-wrapper", "chvatal-three-spokes-formalizer"],
            "lean_heavy_max_parallel": 2,
            "lean_threads": "LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
            "memory_limit": "prlimit --as=22000000000 per launched loop",
            "load_guard": "ARA_MATH_MAX_LOAD_PER_CPU=6.0",
            "external_search": "disabled via --closed-book",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
