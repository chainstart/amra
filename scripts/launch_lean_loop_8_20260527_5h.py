#!/usr/bin/env python3
"""Launch a resource-capped 8-problem Lean campaign queue with source support lanes."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
FORMAL = REPO / "amra_library" / "formal"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "lean_loop_8_20260527_5h"
TARGET_SOURCE_DIR = FORMAL / "AmraLibrary" / "OpenProblemBatches" / "LeanLoop20260527FiveHour"
TIME_BUDGET_SECONDS = 5 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 600
LEAN_ROUND_SECONDS = 45 * 60
SOURCE_ROUND_SECONDS = 60 * 60
SOURCE_CONCURRENCY = 3


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


def read_existing(path: str) -> str:
    p = REPO / path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def resource_prefix(*, lean: bool) -> list[str]:
    if shutil.which("systemd-run"):
        if lean:
            return [
                "systemd-run",
                "--user",
                "--scope",
                "-p",
                "MemoryMax=16G",
                "-p",
                "MemorySwapMax=20G",
                "-p",
                "CPUQuota=200%",
            ]
        return [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=8G",
            "-p",
            "MemorySwapMax=10G",
            "-p",
            "CPUQuota=250%",
        ]
    return []


def nice_prefix() -> list[str]:
    command = ["timeout", f"{HARD_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def clean_target_workspace() -> None:
    TARGET_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for path in TARGET_SOURCE_DIR.glob("*.lean"):
        path.unlink()


def seed_independent_odd() -> str:
    return r"""
import Mathlib.Tactic

namespace IndependentDominationLeanLoop20260527

theorem cko_odd_floor_scale_nat (D : ℕ) (hOdd : Odd D) :
    4 * ((D + 2) ^ 2 / 4) = (D + 1) * (D + 3) := by
  sorry

end IndependentDominationLeanLoop20260527
"""


def seed_erdos_triangular() -> str:
    return r"""
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace Erdos1084

noncomputable def triangularCount (n : ℕ) : ℕ :=
  3 * n ^ 2 + 3 * n + 1

theorem triangular_harborth_floor_eval (n : ℕ) :
    Nat.floor
        (3 * (triangularCount n : ℝ) -
          Real.sqrt (12 * (triangularCount n : ℝ) - 3))
      = 9 * n ^ 2 + 3 * n := by
  sorry

end Erdos1084
"""


def seed_triangle(n: int) -> str:
    return rf"""
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic

namespace TriangleDissectionLeanLoop20260527

variable (EquilateralCongruentTriangleTilingPossible : ℕ → Prop)

theorem not_equilateral_congruent_triangle_tiling_possible_{n}
    (beeson_prime_exclusion_for_faithful_equilateral_tilings :
      ∀ N : ℕ, 3 < N → Nat.Prime N → ¬ EquilateralCongruentTriangleTilingPossible N) :
    ¬ EquilateralCongruentTriangleTilingPossible {n} := by
  sorry

end TriangleDissectionLeanLoop20260527
"""


def seed_exists_maximal_star() -> str:
    helper = read_existing("artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/01_exists_maximal_star.lean")
    return helper + r"""

namespace ChvatalRankTwoLeanLoop20260527

open Classical

variable {α : Type} [Fintype α] [DecidableEq α] [Nonempty α]

def Decreasing (F : Finset (Finset α)) : Prop :=
  ∀ A B : Finset α, B ⊆ A → A ∈ F → B ∈ F

def Intersecting (F : Finset (Finset α)) : Prop :=
  ∀ A ∈ F, ∀ B ∈ F, A ∩ B ≠ ∅

theorem exists_maximal_star_rank_two
    (F : Finset (Finset α)) (hdec : Decreasing F)
    (hrank : ∀ A ∈ F, A.card ≤ 2) :
    ∃ x : α, ∀ G, G ⊆ F → Intersecting G →
      G.card ≤ { A ∈ F | x ∈ A }.card := by
  sorry

end ChvatalRankTwoLeanLoop20260527
"""


def seed_wowii19() -> str:
    helper = read_existing("artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/02_wowii_conjecture19.lean")
    return helper + r"""

namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α] [Nonempty α]

theorem exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from
    {G : SimpleGraph α} (hG : G.Connected) (v : α) :
    ∃ s : Finset α,
      (G.induce (s : Set α)).IsBipartite ∧
        (G.diam : ℝ) + (indepNeighborsCard G v : ℝ) ≤ (s.card : ℝ) := by
  sorry

end SimpleGraph
"""


def seed_antihydra() -> str:
    helper = read_existing("artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/03_antihydra.lean")
    return helper + r"""

namespace BeaverMathOlympiadLeanLoop20260527

theorem beaver_math_olympiad_problem_2_antihydra
    (a : ℕ → ℕ) (b : ℕ → ℤ)
    (a_ini : a 0 = 8)
    (a_rec : ∀ n, a (n + 1) = (3 * a n) / 2)
    (b_ini : b 0 = 0)
    (b_rec : ∀ n, b (n + 1) = if a n % 2 = 0 then b n + 2 else b n - 1) :
    ∀ n, b n ≥ 0 := by
  sorry

end BeaverMathOlympiadLeanLoop20260527
"""


def seed_independent_even() -> str:
    return r"""
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace IndependentDominationLeanLoop20260527

variable {Graph Vertex : Type}
variable (HasNoIsolated : Graph → Prop)
variable (BoundedDegreeBy : Graph → ℕ → Prop)
variable (IsNIndepDominatingSet : Graph → Finset Vertex → Prop)

theorem ckko_corollary_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated :
    (∀ G : Graph, ∀ Delta m : ℕ,
      HasNoIsolated G →
      BoundedDegreeBy G Delta →
      0 < m →
      Delta ≤ m →
      ∃ S : Finset Vertex, IsNIndepDominatingSet G S) →
    ∀ G : Graph, ∀ Delta m : ℕ,
      HasNoIsolated G →
      BoundedDegreeBy G Delta →
      0 < m →
      Delta ≤ m →
      ∃ S : Finset Vertex, IsNIndepDominatingSet G S := by
  sorry

end IndependentDominationLeanLoop20260527
"""


LEAN_TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "independent-domination-odd",
        "problem_id": "formal-conjectures-independentdominationodd",
        "target_theorem": "cko_odd_floor_scale_nat",
        "seed": seed_independent_odd,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/02-independent-domination-odd.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-odd/independent-domination-odd-nl-continue-4h/report.json",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-odd/independent-domination-odd-nl-continue-4h/supervisor/round-051/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos-1084-triangular-d2",
        "problem_id": "formal-conjectures-erdos-1084-variants-triangular-optimal-d2",
        "target_theorem": "Erdos1084.triangular_harborth_floor_eval",
        "seed": seed_erdos_triangular,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/03-erdos-1084-triangular-d2.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-continue-4h/report.json",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-continue-4h/supervisor/round-049/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
        ),
    },
    {
        "priority": 3,
        "slug": "triangle-dissection-13",
        "problem_id": "triangle-dissection-13",
        "target_theorem": "not_equilateral_congruent_triangle_tiling_possible_13",
        "seed": lambda: seed_triangle(13),
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/04-triangle-dissection-13.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-13/triangle-dissection-13-nl-continue-4h/report.json",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-13/triangle-dissection-13-nl-continue-4h/supervisor/round-041/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/633.lean",
            "/home/biostar/work/projects/formal-math/erdos-634-triangle/README.md",
        ),
    },
    {
        "priority": 4,
        "slug": "triangle-dissection-17",
        "problem_id": "triangle-dissection-17",
        "target_theorem": "not_equilateral_congruent_triangle_tiling_possible_17",
        "seed": lambda: seed_triangle(17),
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/05-triangle-dissection-17.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-17/triangle-dissection-17-nl-continue-4h/report.json",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-17/triangle-dissection-17-nl-continue-4h/supervisor/round-040/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/633.lean",
            "/home/biostar/work/projects/formal-math/erdos-634-triangle/README.md",
        ),
    },
    {
        "priority": 5,
        "slug": "antihydra",
        "problem_id": "formal-conjectures-beaver-math-olympiad-problem-2-antihydra",
        "target_theorem": "beaver_math_olympiad_problem_2_antihydra",
        "initial_target": "antihydra_block_credit_nonnegative",
        "seed": seed_antihydra,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/10-antihydra.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/supervisor/round-329/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/runs/antihydra/antihydra-lean-4h/report.json",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Other/BeaverMathOlympiad.lean",
        ),
    },
    {
        "priority": 6,
        "slug": "wowii-conjecture19",
        "problem_id": "formal-conjectures-conjecture19",
        "target_theorem": "exists_diam_add_indepNeighborsCard_bipartite_witness_of_diam_geodesic_from",
        "seed": seed_wowii19,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/08-wowii-conjecture19.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/supervisor/round-322/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/runs/wowii-conjecture19/wowii-conjecture19-lean-4h/report.json",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture19.lean",
        ),
    },
    {
        "priority": 7,
        "slug": "exists-maximal-star",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "target_theorem": "exists_maximal_star_rank_two",
        "seed": seed_exists_maximal_star,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/09-exists-maximal-star.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/exists-maximal-star/exists-maximal-star-nl-8h/supervisor/round-364/decision.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/runs/exists-maximal-star/exists-maximal-star-lean-4h/report.json",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
        ),
    },
    {
        "priority": 8,
        "slug": "independent-domination-even",
        "problem_id": "formal-conjectures-independentdominationeven",
        "target_theorem": "ckko_corollary_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated",
        "seed": seed_independent_even,
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/01-independent-domination-even.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-even/independent-domination-even-nl-continue-4h/report.json",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-even/independent-domination-even-nl-continue-4h/supervisor/round-031/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
        ),
    },
]


SOURCE_TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "source-ckko-independent-domination",
        "statement": "Source-certify Cho-Kim-Kim-Oum Corollary 1.3 and write a Lean theorem contract for the independent domination even/odd campaigns.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/01-independent-domination-even.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/02-independent-domination-odd.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-even/independent-domination-even-nl-continue-4h/supervisor/round-031/decision.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-odd/independent-domination-odd-nl-continue-4h/supervisor/round-051/decision.md",
        ),
    },
    {
        "priority": 2,
        "slug": "source-harborth-erdos1084",
        "statement": "Source-certify the Harborth/contact-number theorem needed for the Erdos 1084 triangular d=2 specialization and write the narrow Lean theorem contract.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/03-erdos-1084-triangular-d2.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-continue-4h/supervisor/round-049/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
        ),
    },
    {
        "priority": 3,
        "slug": "source-beeson-triangle-dissection",
        "statement": "Source-certify Beeson prime exclusion for faithful equilateral triangle tilings and align it with the FormalConjectures Erdos633 predicate for N=13 and N=17.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/04-triangle-dissection-13.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/05-triangle-dissection-17.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-13/triangle-dissection-13-nl-continue-4h/supervisor/round-041/decision.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/triangle-dissection-17/triangle-dissection-17-nl-continue-4h/supervisor/round-040/decision.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/633.lean",
            "/home/biostar/work/projects/formal-math/erdos-634-triangle/README.md",
        ),
    },
]


def prepare_lean_targets() -> list[dict[str, Any]]:
    (RUN_ROOT / "targets").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "seed_lean").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "final_lean").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "logs").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "runs").mkdir(parents=True, exist_ok=True)
    clean_target_workspace()
    prepared: list[dict[str, Any]] = []
    for target in LEAN_TARGETS:
        target_file = TARGET_SOURCE_DIR / f"{target['priority']:02d}_{target['slug'].replace('-', '_')}.lean"
        seed_file = RUN_ROOT / "seed_lean" / target_file.name
        final_file = RUN_ROOT / "final_lean" / target_file.name
        statement_file = RUN_ROOT / "targets" / f"{target['priority']:02d}-{target['slug']}.md"
        seed_text = target["seed"]()
        write_text(seed_file, seed_text)
        write_text(
            statement_file,
            "\n".join(
                [
                    f"# Lean Loop 5h: {target['slug']}",
                    "",
                    f"Problem id: `{target['problem_id']}`",
                    f"Target theorem: `{target['target_theorem']}`",
                    f"Budget: {TIME_BUDGET_SECONDS} seconds; serial Lean lane; `LEAN_NUM_THREADS=1`.",
                    "",
                    "Use the supplied prior summaries and source contexts. Close the target without `sorry`, `admit`, `axiom`, `constant`, or `opaque` placeholders. Do not trigger full-library builds during exploration.",
                    "",
                ]
            ),
        )
        build_command = f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {target_file}"
        cmd = [
            *resource_prefix(lean=True),
            *nice_prefix(),
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
            str(target["target_theorem"]),
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
            str(LEAN_ROUND_SECONDS),
            "--formalizer-attempts",
            "3",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "420",
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
            f"{target['slug']}-lean-5h",
            "--reasoning-effort",
            "high",
        ]
        if target.get("initial_target"):
            cmd += ["--initial-target-theorem", str(target["initial_target"])]
        for context in target["contexts"]:
            cmd += ["--context-file", context]
        prepared.append(
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "target_theorem": target["target_theorem"],
                "initial_target": target.get("initial_target"),
                "target_file": str(target_file),
                "seed_lean_file": str(seed_file),
                "final_lean_file": str(final_file),
                "statement_file": str(statement_file),
                "build_command": build_command,
                "log_path": str(RUN_ROOT / "logs" / f"lean-{target['priority']:02d}-{target['slug']}.log"),
                "output_root": str(RUN_ROOT / "runs" / target["slug"]),
                "run_name": f"{target['slug']}-lean-5h",
                "command": cmd,
                "contexts": list(target["contexts"]),
            }
        )
    return prepared


def prepare_source_targets() -> list[dict[str, Any]]:
    (RUN_ROOT / "source_statements").mkdir(parents=True, exist_ok=True)
    prepared: list[dict[str, Any]] = []
    for target in SOURCE_TARGETS:
        statement_file = RUN_ROOT / "source_statements" / f"{target['priority']:02d}-{target['slug']}.md"
        write_text(
            statement_file,
            "\n".join(
                [
                    f"# Source Contract Support: {target['slug']}",
                    "",
                    target["statement"],
                    "",
                    "Output a source-grounded Leanization contract with exact theorem names, assumptions, references, and the first formal blocker.",
                ]
            ),
        )
        cmd = [
            *resource_prefix(lean=False),
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
            str(SOURCE_ROUND_SECONDS),
            "--proof-attempts",
            "1",
            "--proof-audits",
            "1",
            "--proof-attempt-timeout",
            "1800",
            "--proof-audit-timeout",
            "600",
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
            str(RUN_ROOT / "source_runs" / target["slug"]),
            "--run-name",
            f"{target['slug']}-source-5h",
            "--reasoning-effort",
            "high",
        ]
        for context in target["contexts"]:
            cmd += ["--context-file", context]
        prepared.append(
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "statement_file": str(statement_file),
                "log_path": str(RUN_ROOT / "logs" / f"source-{target['priority']:02d}-{target['slug']}.log"),
                "output_root": str(RUN_ROOT / "source_runs" / target["slug"]),
                "run_name": f"{target['slug']}-source-5h",
                "command": cmd,
                "contexts": list(target["contexts"]),
            }
        )
    return prepared


def prepare() -> dict[str, Any]:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    lean_targets = prepare_lean_targets()
    source_targets = prepare_source_targets()
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "mode": "resource_capped_lean_loop_8",
        "time_budget_seconds_per_campaign": TIME_BUDGET_SECONDS,
        "resource_policy": {
            "lean_lane": "serial, LEAN_NUM_THREADS=1, OMP_NUM_THREADS=1, systemd MemoryMax=16G, CPUQuota=200%",
            "source_lane": f"parallel up to {SOURCE_CONCURRENCY}, systemd MemoryMax=8G",
            "build_policy": "single-file lake env lean during exploration; full lake build is not used by this launcher",
        },
        "lean_targets": lean_targets,
        "source_targets": source_targets,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    return manifest


def start_source_jobs(source_targets: list[dict[str, Any]], status: dict[str, Any]) -> list[dict[str, Any]]:
    active: list[dict[str, Any]] = []
    for target in source_targets[:SOURCE_CONCURRENCY]:
        item = {
            "slug": target["slug"],
            "started_at": utc_now(),
            "status": "running",
            "log_path": target["log_path"],
            "output_root": target["output_root"],
        }
        with Path(target["log_path"]).open("ab") as log:
            proc = subprocess.Popen(
                target["command"],
                cwd=REPO,
                env=os.environ.copy(),
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        item["pid"] = proc.pid
        item["_proc"] = proc
        status["source_targets"].append({k: v for k, v in item.items() if k != "_proc"})
        active.append(item)
    return active


def poll_source_jobs(active: list[dict[str, Any]], status: dict[str, Any]) -> None:
    for item in active:
        proc = item["_proc"]
        rc = proc.poll()
        if rc is None or item.get("finished_at"):
            continue
        item["finished_at"] = utc_now()
        item["returncode"] = rc
        item["status"] = "completed" if rc == 0 else "failed"
    status["source_targets"] = [{k: v for k, v in item.items() if k != "_proc"} for item in active]


def run_worker() -> None:
    manifest = json.loads((RUN_ROOT / "manifest.json").read_text(encoding="utf-8"))
    status_path = RUN_ROOT / "queue_status.json"
    env = os.environ.copy()
    env["LEAN_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    status: dict[str, Any] = {
        "started_at": utc_now(),
        "status": "running",
        "resource_policy": manifest["resource_policy"],
        "lean_targets": [],
        "source_targets": [],
    }
    write_json(status_path, status)
    active_sources = start_source_jobs(manifest["source_targets"], status)
    write_json(status_path, status)
    for target in manifest["lean_targets"]:
        poll_source_jobs(active_sources, status)
        clean_target_workspace()
        target_file = Path(target["target_file"])
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(Path(target["seed_lean_file"]).read_text(encoding="utf-8"), encoding="utf-8")
        item = {
            "slug": target["slug"],
            "problem_id": target["problem_id"],
            "target_theorem": target["target_theorem"],
            "started_at": utc_now(),
            "status": "running",
            "log_path": target["log_path"],
            "output_root": target["output_root"],
            "target_file": target["target_file"],
            "seed_lean_file": target["seed_lean_file"],
            "final_lean_file": target["final_lean_file"],
        }
        status["lean_targets"].append(item)
        write_json(status_path, status)
        with Path(target["log_path"]).open("ab") as log:
            proc = subprocess.run(
                target["command"],
                cwd=REPO,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        if target_file.exists():
            Path(target["final_lean_file"]).write_text(target_file.read_text(encoding="utf-8"), encoding="utf-8")
        item["finished_at"] = utc_now()
        item["returncode"] = proc.returncode
        item["status"] = "completed" if proc.returncode == 0 else "failed"
        poll_source_jobs(active_sources, status)
        write_json(status_path, status)
        clean_target_workspace()
    while any(item["_proc"].poll() is None for item in active_sources):
        poll_source_jobs(active_sources, status)
        write_json(status_path, status)
        time.sleep(30)
    poll_source_jobs(active_sources, status)
    status["finished_at"] = utc_now()
    status["status"] = "completed"
    write_json(status_path, status)


def launch() -> dict[str, Any]:
    manifest = prepare()
    scheduler_log = RUN_ROOT / "logs" / "scheduler.log"
    scheduler_log.parent.mkdir(parents=True, exist_ok=True)
    with scheduler_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, __file__, "--worker"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    (RUN_ROOT / "scheduler.pid").write_text(f"{proc.pid}\n", encoding="ascii")
    payload = {
        "run_root": str(RUN_ROOT),
        "scheduler_pid": proc.pid,
        "scheduler_log": str(scheduler_log),
        "manifest_path": str(RUN_ROOT / "manifest.json"),
        "queue_status_path": str(RUN_ROOT / "queue_status.json"),
        "lean_target_count": len(manifest["lean_targets"]),
        "source_target_count": len(manifest["source_targets"]),
        "resource_policy": manifest["resource_policy"],
    }
    write_json(RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    if "--worker" in sys.argv:
        run_worker()
        return
    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
