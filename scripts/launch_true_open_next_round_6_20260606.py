#!/usr/bin/env python3
"""Launch the next supervised attack round for six unresolved true-open targets.

The launcher deliberately separates natural-language/source proof-lab work
from Lean-heavy work.  At most two Lean-heavy campaign processes are started,
and those processes are resource-capped where systemd-run is available.
"""

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
FORMAL = REPO / "amra_library" / "formal"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_next_round_6_20260606"
LEAN_TARGET_DIR = FORMAL / "AmraLibrary" / "OpenProblemBatches" / "TrueOpenNextRound20260606"

TIME_BUDGET_SECONDS = 2 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 45 * 60
LEAN_ROUND_TIME_BUDGET_SECONDS = 30 * 60
LEAN_MAX_CONCURRENCY = 2


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def existing(*relative_paths: str) -> list[str]:
    paths: list[str] = []
    for raw in relative_paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / raw
        if path.exists():
            paths.append(str(path))
    return paths


def read_existing(relative_path: str) -> str:
    path = REPO / relative_path
    return path.read_text(encoding="utf-8") if path.exists() else ""


def nice_prefix(*, timeout_seconds: int) -> list[str]:
    command = ["timeout", f"{timeout_seconds}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def resource_prefix(*, lean: bool) -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    if lean:
        return [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=10G",
            "-p",
            "MemorySwapMax=12G",
            "-p",
            "CPUQuota=150%",
        ]
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


def statement_for(slug: str, title: str, problem_id: str, focus: str, mode_note: str) -> str:
    return "\n".join(
        [
            f"# Supervised Next Round: {title}",
            "",
            f"Problem id: `{problem_id}`",
            "Batch: `true_open_next_round_6_20260606`",
            "",
            "Run policy:",
            "- Use the global supervisor every round.",
            "- Prefer the smallest theorem-level blocker.",
            "- If the route is false or under-specified, freeze it and produce the exact corrected target.",
            "- Do not claim a main theorem from a sublemma.",
            "",
            "Mode note:",
            mode_note,
            "",
            "Focus:",
            focus,
            "",
            "Required final output:",
            "- Current target theorem or certificate target.",
            "- What was proved, refuted, or narrowed.",
            "- First remaining blocker.",
            "- Whether the next move should be proof-lab, Lean formalization, source audit, or computation certificate.",
        ]
    )


def seed_wowii19() -> str:
    helper = read_existing("artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/02_wowii_conjecture19.lean")
    return helper + r"""

namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α] [Nonempty α]

theorem path_vertices_erase_one_card_eq_length
    {G : SimpleGraph α} {u w : α} (p : G.Walk u w)
    (hpPath : p.IsPath) (hpLen : 1 ≤ p.length) :
    (((Finset.range (p.length + 1)).erase 1).image fun i => p.getVert i).card =
      p.length := by
  sorry

theorem exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from
    {G : SimpleGraph α} (hG : G.Connected) {v y : α} (p : G.Walk v y)
    (hpPath : p.IsPath)
    (hpDist : p.length = G.dist v y)
    (hpDiam : p.length = G.diam) :
    ∃ s : Finset α,
      (G.induce (s : Set α)).IsBipartite ∧
        (G.diam : ℝ) + (indepNeighborsCard G v : ℝ) ≤ (s.card : ℝ) := by
  sorry

end SimpleGraph
"""


def seed_exists_maximal_star() -> str:
    helper = read_existing("artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/01_exists_maximal_star.lean")
    return helper + r"""

namespace ChvatalRankTwoNextRound20260606

open Classical

variable {α : Type} [Fintype α] [DecidableEq α] [Nonempty α]

def Decreasing (F : Finset (Finset α)) : Prop :=
  ∀ A B : Finset α, B ⊆ A → A ∈ F → B ∈ F

def Intersecting (F : Finset (Finset α)) : Prop :=
  ∀ A ∈ F, ∀ B ∈ F, A ∩ B ≠ ∅

theorem rank_two_intersecting_no_common_vertex_all_card_two
    (F G : Finset (Finset α)) (hGF : G ⊆ F)
    (hI : Intersecting G)
    (hrank : ∀ A ∈ F, A.card ≤ 2)
    (hno_common : ¬ ∃ x : α, ∀ A ∈ G, x ∈ A) :
    ∀ A ∈ G, A.card = 2 := by
  sorry

theorem exists_maximal_star_rank_two
    (F : Finset (Finset α)) (hdec : Decreasing F)
    (hrank : ∀ A ∈ F, A.card ≤ 2) :
    ∃ x : α, ∀ G, G ⊆ F → Intersecting G →
      G.card ≤ { A ∈ F | x ∈ A }.card := by
  sorry

end ChvatalRankTwoNextRound20260606
"""


PROOF_LAB_TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "kothe-radical",
        "problem_id": "formal-conjectures-kotherconjecture-variants-le-kotherradical",
        "title": "Koethe radical route grounding",
        "focus": "Stop broad retargeting. Source-ground the exact relation among nil left ideals, two-sided nil covers, and KotheRadical membership; output one Lean-ready theorem chain or freeze the route.",
        "mode_note": "Source-first proof-lab only. No Lean-heavy build in this round.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/01-kothe-radical.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/kothe-radical/kothe-radical-nl-8h/summary.md",
            "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0007-formal-conjectures-kotherconjecture-variants-le-kotherradical/probe_output.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Wikipedia/Koethe.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "antihydra-certificate",
        "problem_id": "formal-conjectures-beaver-math-olympiad-problem-2-antihydra",
        "title": "Antihydra certificate route",
        "focus": "Design the shifted handoff decomposition plus finite quotient/potential certificate. Use computation as certificate design, not as an unchecked proof.",
        "mode_note": "Proof-lab/certificate route only. The prior Lean helper queue is context, but no heavy Lean theorem attack is launched here.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/10-antihydra.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/summary.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/supervisor/round-329/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/03_antihydra.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Other/BeaverMathOlympiad.lean",
        ),
    },
    {
        "priority": 3,
        "slug": "wowii-conjecture40",
        "problem_id": "formal-conjectures-conjecture40",
        "title": "WOWII Conjecture 40 endpoint-switch obstruction",
        "focus": "Attack or refute `MixedEndpointFailureBlockerFamilyLocalizesToYDefectDOne`; preserve all full-capacity/tight-dangerous hypotheses and produce a finite counterexample if the bridge is false.",
        "mode_note": "Proof-lab with counterexample search. No Lean-heavy compilation in this round.",
        "contexts": existing(
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-switch-obstruction-2h/statement.md",
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-switch-obstruction-2h/summary.md",
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-switch-obstruction-2h/state.json",
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-failure-3h/state.json",
        ),
    },
    {
        "priority": 4,
        "slug": "general-supercongruence",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence lemma split",
        "focus": "Do not attack the full theorem blindly. Split the blocker into denominator-cleared binomial expansion mod p^4, harmonic pairing mod p^2, and rational numerator transfer to ZMod.",
        "mode_note": "Source/lemma planning proof-lab only. No Lean-heavy build in this round.",
        "contexts": existing(
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/statement.md",
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/final.md",
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/tmp_mirror/episode3_target_blocker.md",
            "artifacts/lean_workspaces/general_supercongruence/FormalConjectures/OEIS/357513.lean",
        ),
    },
]


LEAN_TARGETS: list[dict[str, Any]] = [
    {
        "priority": 5,
        "slug": "wowii-conjecture19",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII Conjecture 19 witness theorem",
        "focus": "Use the closed geodesic cross-edge lemma and attack the next witness-packaging theorem. If the target is too broad, supervisor must switch to the smallest missing Lean lemma.",
        "target_theorem": "exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from",
        "seed": seed_wowii19,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/08-wowii-conjecture19.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/summary.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/supervisor/round-322/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/02_wowii_conjecture19.lean",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture19.lean",
        ),
    },
    {
        "priority": 6,
        "slug": "exists-maximal-star-rank-two",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal rank-two checkpoint",
        "focus": "Use the completed pairwise-intersecting two-set lemma and attack `exists_maximal_star_rank_two`; supervisor should avoid unrestricted Chvatal unless the rank-two checkpoint closes.",
        "target_theorem": "exists_maximal_star_rank_two",
        "seed": seed_exists_maximal_star,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/09-exists-maximal-star.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/exists-maximal-star/exists-maximal-star-nl-8h/summary.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/exists-maximal-star/exists-maximal-star-nl-8h/supervisor/round-364/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/01_exists_maximal_star.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
        ),
    },
]


def prepare_proof_lab_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(
        statement_file,
        statement_for(target["slug"], target["title"], target["problem_id"], target["focus"], target["mode_note"]),
    )
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    cmd = [
        *resource_prefix(lean=False),
        *nice_prefix(timeout_seconds=TIME_BUDGET_SECONDS + 600),
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
        f"{target['slug']}-supervised-2h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]
    return {
        **target,
        "lane": "proof_lab",
        "statement_file": str(statement_file),
        "log_path": str(log_path),
        "output_root": str(RUN_ROOT / "runs" / target["slug"]),
        "command": cmd,
    }


def prepare_lean_target(target: dict[str, Any]) -> dict[str, Any]:
    LEAN_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    target_file = LEAN_TARGET_DIR / f"{target['priority']:02d}_{target['slug'].replace('-', '_')}.lean"
    seed_file = RUN_ROOT / "seed_lean" / target_file.name
    final_file = RUN_ROOT / "final_lean" / target_file.name
    write_text(seed_file, target["seed"]())
    write_text(target_file, target["seed"]())
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(
        statement_file,
        statement_for(
            target["slug"],
            target["title"],
            target["problem_id"],
            target["focus"],
            "Lean-heavy lane. Single-file build only, LEAN_NUM_THREADS=1, systemd resource cap when available.",
        ),
    )
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    build_command = f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {target_file}"
    cmd = [
        *resource_prefix(lean=True),
        *nice_prefix(timeout_seconds=TIME_BUDGET_SECONDS + 600),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
        "--workspace",
        str(FORMAL),
        "--target-file",
        str(target_file),
        "--final-target-theorem",
        target["target_theorem"],
        "--build-command",
        build_command,
        "--backend",
        "codex",
        "--closed-book",
        "--mode",
        "lean-formalizer",
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        str(LEAN_ROUND_TIME_BUDGET_SECONDS),
        "--formalizer-attempts",
        "2",
        "--formalizer-attempt-timeout",
        "900",
        "--formalizer-build-timeout",
        "360",
        "--proof-attempts",
        "0",
        "--proof-audits",
        "0",
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
        f"{target['slug']}-lean-supervised-2h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]
    return {
        **target,
        "lane": "lean_heavy",
        "statement_file": str(statement_file),
        "target_file": str(target_file),
        "seed_lean_file": str(seed_file),
        "final_lean_file": str(final_file),
        "build_command": build_command,
        "log_path": str(log_path),
        "output_root": str(RUN_ROOT / "runs" / target["slug"]),
        "command": cmd,
    }


def start_target(target: dict[str, Any]) -> dict[str, Any]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab") as log:
        env = os.environ.copy()
        if target["lane"] == "lean_heavy":
            env.update(
                {
                    "LEAN_NUM_THREADS": "1",
                    "OMP_NUM_THREADS": "1",
                    "ARA_MATH_BACKEND_MAX_MEMORY_MB": "6144",
                    "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "4096",
                    "ARA_MATH_MAX_LOAD_PER_CPU": "1.25",
                }
            )
        else:
            env.update(
                {
                    "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
                    "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
                    "ARA_MATH_MAX_LOAD_PER_CPU": "1.5",
                }
            )
        proc = subprocess.Popen(
            target["command"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    pid_path = RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid"
    write_text(pid_path, str(proc.pid))
    return {
        "priority": target["priority"],
        "slug": target["slug"],
        "problem_id": target["problem_id"],
        "lane": target["lane"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "target_file": target.get("target_file"),
        "target_theorem": target.get("target_theorem"),
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "command": target["command"],
    }


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# True Open Next Round 6 2026-06-06",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target budget: {manifest['time_budget_seconds']} seconds",
        "",
        "Resource policy:",
        "- Supervisor enabled for every target: `--supervisor-backend codex --supervisor-every-rounds 1`.",
        f"- Lean-heavy concurrency: {LEAN_MAX_CONCURRENCY}; launched targets are the only Lean-heavy jobs in this batch.",
        "- Lean builds are single-file: `lake env lean <target_file>`, `LEAN_NUM_THREADS=1`, `OMP_NUM_THREADS=1`.",
        "- If `systemd-run` is available, Lean-heavy jobs use `MemoryMax=10G`, `MemorySwapMax=12G`, `CPUQuota=150%`.",
        "",
        "| Priority | Lane | Problem id | PID | Log |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for target in manifest["targets"]:
        lines.append(
            f"| {target['priority']} | `{target['lane']}` | `{target['problem_id']}` | {target['pid']} | `{target['log_path']}` |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)

    prepared = [prepare_proof_lab_target(target) for target in PROOF_LAB_TARGETS]
    lean_prepared = [prepare_lean_target(target) for target in LEAN_TARGETS]
    if len(lean_prepared) > LEAN_MAX_CONCURRENCY:
        raise RuntimeError(f"configured {len(lean_prepared)} Lean-heavy jobs, limit is {LEAN_MAX_CONCURRENCY}")
    prepared.extend(lean_prepared)

    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "lean_round_time_budget_seconds": LEAN_ROUND_TIME_BUDGET_SECONDS,
        "resource_policy": {
            "supervisor": "codex every round, 600s timeout",
            "lean_max_concurrency": LEAN_MAX_CONCURRENCY,
            "lean_memory": "MemoryMax=10G, MemorySwapMax=12G when systemd-run is available",
            "lean_threads": "LEAN_NUM_THREADS=1, OMP_NUM_THREADS=1",
            "lean_build": "single target file only via lake env lean",
            "proof_lab_memory": "MemoryMax=6G when systemd-run is available",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    write_text(RUN_ROOT / "README.md", render_readme(manifest))
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
