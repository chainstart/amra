#!/usr/bin/env python3
"""Launch a 2026-06-12 two-hour Lean push for WOWII198a, WOWII16, and Crystals."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import launch_manual_next_attack_20260610_1h as base


REPO = Path(__file__).resolve().parents[1]
FORMAL = REPO / "amra_library" / "formal"
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "wowii198a_16_crystals_20260612_2h"
)

AUDIT_198A = (
    "artifacts/open_problem_screening/latest/"
    "wowii198a_semantic_open_audit_and_next_directions_20260612.md"
)
PREV_MAIN = "artifacts/open_problem_screening/latest/main_push_5_20260611_2h"


def existing(*paths: str | Path) -> list[str]:
    return base.existing(*paths)


def formal_file(relative: str) -> str:
    return base.formal_file(relative)


def build_command(relative: str) -> str:
    return base.build_command(relative)


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii198a-source-exact-final-theorem",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a source-exact final theorem",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "conjecture198a_amra",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a source-exact final theorem

Main objective: prove the original WOWII198a source statement, not another
local branch lemma.

Source statement:

```lean
theorem conjecture198a (G : SimpleGraph alpha) (h : G.Connected)
    (hb : b G <= 2 + averageEccentricity G) :
    exists a b : alpha, exists p : G.Walk a b, p.IsHamiltonian
```

Add a source-faithful AMRA theorem in
`Wowii198aLeftmost.lean`, before any active `#exit`, with this semantic content:

```lean
theorem conjecture198a_amra
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G) :
    exists u v : alpha, exists p : G.Walk u v, p.IsHamiltonian
```

Already verified and not to be redone:

- `diam_add_one_le_b`
- `averageEccentricity_le_diam`
- `source_bound_forces_all_eccent_eq_diam_of_b_eq_diam_add_two`
- `source_bound_b_eq_diam_add_two_forces_diam_le_two`
- `exists_isDiametralGeodesic`
- `source_bound_b_eq_diam_add_one_forces_hamiltonian`

Required missing source-equivalence work:

1. Prove the exact branch split from the source inequality:

```lean
lemma source_bound_forces_b_eq_diam_add_one_or_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G) :
    b G = G.diam + 1 or b G = G.diam + 2
```

Use `diam_add_one_le_b`, `averageEccentricity_le_diam`, and integer arithmetic
after deriving `G.diam + 1 <= b G` and `b G <= G.diam + 2`.

2. Close or isolate the real blocker in the `b G = G.diam + 2` branch:

```lean
lemma source_bound_b_eq_diam_add_two_forces_hamiltonian
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G)
    (hb2 : b G = G.diam + 2) :
    exists u v : alpha, exists p : G.Walk u v, p.IsHamiltonian
```

The existing `source_bound_b_eq_diam_add_two_forces_diam_le_two` is not enough
by itself. Use the source inequality, the equality `b = diam + 2`, and the
diameter-at-most-two structure; do not claim the final theorem unless this
branch really reaches Hamiltonian path.

3. Finish `conjecture198a_amra` by case-splitting with the branch split and
calling the two branch theorems.

If the final theorem cannot be closed in this round, the report must name the
first remaining theorem whose absence blocks exact equivalence to the source
statement. Do not route to paper writing.
""",
            "contexts": existing(
                AUDIT_198A,
                f"{PREV_MAIN}/runs/wowii198a-diam-three-six-bipartite-witness/"
                "wowii198a-diam-three-six-bipartite-witness-1h/summary.md",
                f"{PREV_MAIN}/runs/wowii198a-diam-three-six-bipartite-witness/"
                "wowii198a-diam-three-six-bipartite-witness-1h/supervisor/"
                "round-013/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-radius-two-source-bound",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 radius-at-most-two source bound",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "conjecture16_source_bound_of_radius_toNat_le_two",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 radius-at-most-two source bound

The central-interval source-data route remains frozen. This round is a narrow
Lean formalization branch.

Target theorem:

```lean
theorem conjecture16_source_bound_of_radius_toNat_le_two
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (hG : G.Connected)
    (hRadius : G.radius.toNat <= 2) :
    letI maxL := (Finset.univ.image (fun v => indepNeighborsCard G v)).max' (by simp)
    letI r := G.radius.toNat
    2 * ((r : Real) - 1) + (maxL : Real) <= b G
```

Reuse `conjecture16_of_radius_toNat_le_one` for `r <= 1`. For `r = 2`, prove
or isolate a local helper constructing an induced bipartite witness with at
least `indepNeighborsCard G v + 2` vertices from a vertex attaining `maxL`,
then transfer through
`card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite`.

Do not reopen the central-interval proof-lab route and do not wrap already
verified theorems without adding the radius-two branch.
""",
            "contexts": existing(
                f"{PREV_MAIN}/runs/wowii16-source-bound-from-radius-witness-data/"
                "wowii16-source-bound-from-radius-witness-data-1h/supervisor/"
                "round-013/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-halfshift-admissible-bridge",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals half-shift admissibility bridge",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "07_crystals_odd_vieta_descent.lean"
            ),
            "target_theorem": "isCrystalWithComponents_halfShift_admissible",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "07_crystals_odd_vieta_descent.lean"
            ),
            "statement": """
# Crystals half-shift admissibility bridge

Stop proof-lab cycling. Add the first source-faithful Lean bridge from
`IsCrystalWithComponents` to the half-shift divisibility setup used by the
already verified odd Vieta descent lemmas.

Target theorem name:

```lean
isCrystalWithComponents_halfShift_admissible
```

Required content:

- transfer parity from `Odd n` and `n = a * b`;
- construct `r, s` with `2 <= r`, `2 <= s`, `a = 2 * r - 1`,
  `b = 2 * s - 1`;
- split out a helper such as
  `halfShift_crystal_dvd_implies_rs_dvd_sq` for the half-shift divisibility
  cancellation;
- preserve and reuse `odd_vieta_d_lt_two_mul_se` and `odd_vieta_outer_d_step`.

After this bridge checks, the next route should return to
`nontrivial_duplicate_crystal_to_odd_vieta`. If the bridge fails, the report
must name the exact algebra/divisibility obstruction rather than returning to
general route discovery.
""",
            "contexts": existing(
                f"{PREV_MAIN}/runs/crystals-vieta-descent-to-components-unique/"
                "crystals-vieta-descent-to-components-unique-1h/supervisor/"
                "round-015/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
    ]


def install_overrides() -> None:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 2 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.build_targets = build_targets


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [base.prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": base.utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": base.TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": base.HARD_TIMEOUT_SECONDS,
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "kind": target["kind"],
                "problem_id": target["problem_id"],
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "workspace": target.get("workspace", ""),
                "target_file": target.get("target_file", ""),
                "target_theorem": target.get("target_theorem", ""),
                "build_command": target.get("build_command", ""),
                "command": target["command"],
            }
            for target in targets
        ],
    }
    base.write_json(RUN_ROOT / "manifest.json", manifest)
    driver_log = RUN_ROOT / "logs" / "driver.log"
    with driver_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--driver"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    base.write_text(RUN_ROOT / "pids" / "driver.pid", str(proc.pid))
    manifest["driver_pid"] = proc.pid
    manifest["driver_log"] = str(driver_log)
    base.write_json(RUN_ROOT / "manifest.json", manifest)
    return manifest


def main() -> None:
    install_overrides()
    if len(sys.argv) > 1 and sys.argv[1] == "--driver":
        base.run_driver()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
