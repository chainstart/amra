#!/usr/bin/env python3
"""Launch the next 2h push toward the two true-open main propositions.

This round deliberately avoids re-running targets already verified in
`true_open_next_round_20260608_continuation`.
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
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "true_open_main_proposition_push_20260608_2h"
)
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


GENERAL_HEADER = """lemma zmod_p_minus_one_add_choose_factor_expansion_mod_p4
    (p k : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    (((p - 1 + k).choose k : R)) =
      (p : R) * ((k : R)⁻¹) *
        Finset.prod (Finset.Icc 1 (k - 1))
          (fun j => 1 + (p : R) * (j : R)⁻¹)"""


GENERAL_STATEMENT = f"""
# General supercongruence: upper-binomial exported bridge

This target advances toward `OeisA357513.general_supercongruence` and must not
redo already verified local lemmas.

Already verified in this file:

- `zmod_p_minus_one_choose_factor_expansion_mod_p4`
- `zmod_p_add_choose_factor_expansion_mod_p4_aux`
- `square_zero_mul_prod_one_add_sq`
- `zmod_pair_factor_product_collapse_mod_square`

Next Lean target:

```lean
{GENERAL_HEADER}
```

Recommended route: instantiate the verified shifted auxiliary
`zmod_p_add_choose_factor_expansion_mod_p4_aux` with `t := k - 1`, using
`hk1 : 1 ≤ k` to normalize `(k - 1) + 1 = k` and `p + (k - 1) = p - 1 + k`
under `hkp : k ≤ p - 1`.  Do not attack the full rational numerator theorem in
this round.  After this bridge verifies, the next target should be the
hypergeometric summand expansion modulo `p^4`.
"""


CHVATAL_STATEMENT = """
# Chvatal rank-three main proposition push

Root target remains the bounded-rank step toward Chvatal's conjecture:

```lean
theorem exists_maximal_star_rank_three
    (F : Finset (Finset α)) (hdec : Decreasing F)
    (hrank : ∀ A ∈ F, A.card ≤ 3) :
    ∃ x : α, ∀ G, G ⊆ F → Intersecting G →
      G.card ≤ {A ∈ F | x ∈ A}.card
```

Do not redo these verified Lean targets:

- `exists_maximal_star_rank_two`
- `exists_maximal_star_rank_two_original_quantifier_shape`
- `three_spokes_crossing_edge_contains_center`
- `rank_three_tau_three_trace_graph_degree_le_two`
- `four_edge_degree_two_crossing_family_card_le_two`

The old target `rank_three_tau_three_trace_partition_bound` must not be
formalized: previous proof-lab found its `PT` term false for the intended count.

Main goal for this 2h round:

1. Repair the tau-three trace-counting node with a Lean-ready statement.
2. Prefer the corrected edge-shadow / pair-incidence interface:

```lean
theorem rank_three_tau_three_edge_shadow_sum
    (G : Finset (Finset α)) (E : Finset α)
    (hE : E ∈ G)
    (hEcard : E.card = 3)
    (hrank : ∀ A ∈ G, A.card ≤ 3)
    (hI : Intersecting G)
    (hno_two_cover :
      ∀ a b : α, ¬ ∀ A ∈ G,
        (A ∩ ({a, b} : Finset α)).Nonempty) :
    let D : Finset (Finset α) := G.biUnion fun A => A.powerset
    3 * G.card ≤
      ∑ x in E, ({A ∈ D | x ∈ A}.card)
```

3. If this exact statement is too strong or missing a hypothesis, return the
smallest corrected theorem declaration and a concrete counterexample or proof
sketch.  The next formalizer round should not start until this interface is
coherent.
"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "general-upper-binomial-export",
        "mode": "lean-formalizer",
        "target_theorem": "zmod_p_minus_one_add_choose_factor_expansion_mod_p4",
        "statement": GENERAL_STATEMENT,
        "header": GENERAL_HEADER,
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
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_continuation/runs/general-p-add-choose-factor/general-p-add-choose-factor-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_mixed/runs/general-supercongruence-next-bridge-prooflab/general-supercongruence-next-bridge-prooflab-2h/supervisor/round-017/decision.md",
        ),
    },
    {
        "priority": 2,
        "slug": "chvatal-rank-three-edge-shadow-repair",
        "mode": "proof-lab",
        "target_theorem": "rank_three_tau_three_edge_shadow_sum",
        "statement": CHVATAL_STATEMENT,
        "workspace": None,
        "target_file": None,
        "build_command": "lake build",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_continuation/runs/chvatal-rank-three-degree/chvatal-rank-three-degree-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_targeted_attack_20260607_2h/runs/chvatal-full-main-theorem-attack/chvatal-full-main-theorem-attack-targeted-2h/proof_lab/round-004/summary.md",
            "artifacts/open_problem_screening/latest/true_open_targeted_attack_20260607_2h/runs/chvatal-full-main-theorem-attack/chvatal-full-main-theorem-attack-targeted-2h/supervisor/round-004/decision.md",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, str(target["statement"]))

    header_file = None
    if target["mode"] == "lean-formalizer":
        header_file = RUN_ROOT / "headers" / f"{target['priority']:02d}-{target['slug']}.lean"
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
        target["mode"],
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        "2100",
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
        "--build-command",
        target["build_command"],
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-2h",
        "--reasoning-effort",
        "high",
    ]
    if target["workspace"] is not None:
        cmd += ["--workspace", str(target["workspace"])]
    if target["target_file"] is not None:
        cmd += ["--target-file", str(target["target_file"])]
    if header_file is not None:
        cmd += ["--expected-target-header-file", str(header_file)]
    cmd += ["--final-target-theorem", target["target_theorem"]]
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
        "mode": target["mode"],
        "target_theorem": target["target_theorem"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "header_file": target["header_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "command": target["command"],
    }


def main() -> int:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "headers", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "mode": "main proposition push: one Lean formalizer plus one proof-lab repair track",
        "resource_policy": {
            "external_search": "disabled via --closed-book",
            "lean_heavy_new_parallel": 1,
            "lean_threads": "LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
            "memory_limit": "prlimit --as=22000000000 per launched loop",
            "why_only_one_new_lean": "Existing unrelated campaign may still run a Lean formalizer; this keeps total heavy Lean work within policy.",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
