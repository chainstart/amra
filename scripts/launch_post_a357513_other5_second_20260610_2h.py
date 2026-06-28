#!/usr/bin/env python3
"""Launch the second post-A357513 two-hour round for the other five targets."""

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
    / "post_a357513_other5_second_20260610_2h"
)

MANUAL_AUDIT = (
    "artifacts/open_problem_screening/latest/"
    "manual_other5_post_a357513_second_audit_20260610.md"
)
PREV_ROOT = (
    "artifacts/open_problem_screening/latest/"
    "post_a357513_other5_20260610_2h"
)


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
            "slug": "wowii198a-diam-two-branch-large-diam-exclusion",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a b=diam+2 large-diameter exclusion",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a b=diam+2 large-diameter exclusion

Already Lean-verified and not to be redone:

- `source_bound_forces_b_eq_diam_add_one_or_two`
- `source_bound_forces_averageEccentricity_eq_diam_of_b_eq_diam_add_two`
- `source_bound_forces_all_eccent_eq_diam_of_b_eq_diam_add_two`
- chain/splicing helpers for the `b = diam + 1` branch.

Current target:

```lean
lemma b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb2 : b G = G.diam + 2)
    (hecc : forall v : alpha, (G.eccent v).toNat = G.diam) :
    G.diam <= 3
```

Do not attempt the full Hamiltonian branch.  Prove the large-diameter
contradiction by constructing an induced bipartite witness of cardinality
`G.diam + 3` from a diametral geodesic and an eccentric vertex of an interior
geodesic point.  If the full lemma is too large, add only named helper lemmas
for the bipartite witness construction/cardinality while preserving this
theorem as the audited target.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii198a-source-bound-two-value-split/"
                "wowii198a-source-bound-two-value-split-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii198a-source-bound-two-value-split/"
                "wowii198a-source-bound-two-value-split-1h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-connected-dist-radius-lean",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 connected distance bounded by twice radius",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "connected_dist_le_two_radius_toNat",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 connected distance bounded by twice radius

Do not run more proof-lab on this target.  Add and prove the first missing
radius helper:

```lean
lemma connected_dist_le_two_radius_toNat
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj]
    (hG : G.Connected) (x y : alpha) :
    G.dist x y <= 2 * G.radius.toNat
```

Use `SimpleGraph.dist_le_diam` and `SimpleGraph.ediam_le_two_mul_radius` if the
API path is clean; otherwise use a radius-center triangle proof.  The expected
work is `ENat.toNat` bookkeeping and finite connected side conditions.  After
this helper verifies, the next target should be `no_large_radius_geodesic_interval`.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii16-graph-bridge-spec/"
                "wowii16-graph-bridge-spec-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii16-graph-bridge-spec/"
                "wowii16-graph-bridge-spec-1h/supervisor/round-017/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-odd-vieta-d-lt-two-se-lean",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals odd Vieta inequality",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "07_crystals_odd_vieta_descent.lean"
            ),
            "target_theorem": "odd_vieta_d_lt_two_mul_se",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "07_crystals_odd_vieta_descent.lean"
            ),
            "statement": """
# Crystals odd Vieta inequality

Proof-lab repeatedly converged on this target; do not rediscover the route.
Work in `CrystalsOddVietaDescent20260610` and add:

```lean
lemma odd_vieta_d_lt_two_mul_se
    (r s d e : Nat)
    (hr : 1 <= r) (hs : 1 <= s)
    (hd : Odd d) (he : Odd e)
    (h : r * d ^ 2 + s * e ^ 2 = 2 * r * s * d * e + 1) :
    d < 2 * s * e
```

Prove by contradiction from `hle : 2 * s * e <= d`.  Equality contradicts
`Odd d`.  In the strict case, multiply `2 * s * e < d` by positive `r * d`,
derive `2 * r * s * d * e < r * d ^ 2`, prove `1 <= s * e ^ 2`, and combine
with the equation to get a contradiction.  If Lean fails, report the exact
failed arithmetic subclaim rather than restarting descent discovery.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/crystals-no-odd-vieta-descent/"
                "crystals-no-odd-vieta-descent-1h/summary.md",
                f"{PREV_ROOT}/runs/crystals-no-odd-vieta-descent/"
                "crystals-no-odd-vieta-descent-1h/supervisor/round-023/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "independent-domination80-ckko-source-certificate",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-independent-domination-80",
            "title": "Independent domination 80 CKKO source certificate",
            "statement": """
# Independent domination 80 CKKO source certificate

Do not run natural-language proof discovery.  The source audit found no
semantic mismatch.  The missing object is the trusted source theorem/wrapper:

```lean
theorem ckko_corollary13_source_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (Delta : Nat) (hDelta : 0 < Delta)
    (hMax : G.maxDegree <= Delta)
    (hIso : 0 < G.minDegree) :
    let m := ((Delta + 2)^2) / 4
    exists S : Finset V,
      G.IsNIndepDominatingSet S.card S /\
      m * S.card <= (m - Delta) * Fintype.card V
```

Work in source-certificate mode.  Either identify a trusted import/certificate
mechanism for this exact theorem, or report that no such mechanism exists.  Do
not add axioms, local surrogates, or another CKKO proof sketch.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/independent-domination80-ckko-source-wrapper/"
                "independent-domination80-ckko-source-wrapper-1h/summary.md",
                f"{PREV_ROOT}/runs/independent-domination80-ckko-source-wrapper/"
                "independent-domination80-ckko-source-wrapper-1h/supervisor/round-022/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/IndependentDomination80.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-deficit-counterexample-order-bound",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 deficit counterexample order bound",
            "statement": """
# WOWII200 deficit counterexample order bound

The zero-deficit connector route is frozen.  Do not continue `graph6Of`,
separator-only, Hall/capacity, pointwise multiplicity, or Posa endpoint routes.

Current target:

```lean
theorem deficit_counterexample_order_le_nine
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hnontraceable :
      not (exists a b : alpha, exists p : G.Walk a b, p.IsHamiltonian))
    (hshort : shortGirth G)
    (htough : pathOneTough G)
    (hsat :
      largestInducedTreeSize G =
        (Finset.univ.sup (fun v : alpha => indepNeighborsCard G v)) + 1)
    (hbad :
      (Finset.univ.filter (fun v : alpha => not IsCutVertex G v)).sum
          (fun v =>
            (Finset.univ.sup (fun w => indepNeighborsCard G w))
              - indepNeighborsCard G v)
        < Fintype.card alpha) :
    Fintype.card alpha <= 9
```

Run proof-lab route re-selection.  A valid large-graph proof must give a
concrete noncut-deficit charging/injection with domain, codomain, capacity, and
coverage.  Otherwise produce a corrected bounded-classification theorem or a
full-hypothesis counterexample.  The 17 graph6 survivors are downstream finite
evidence only until this order bound exists.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii200-noncut-deficit-bridge/"
                "wowii200-noncut-deficit-bridge-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii200-noncut-deficit-bridge/"
                "wowii200-noncut-deficit-bridge-1h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
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
        "manual_audit": str(REPO / MANUAL_AUDIT),
        "previous_run_root": str(REPO / PREV_ROOT),
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
