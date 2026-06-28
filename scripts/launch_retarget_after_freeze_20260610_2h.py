#!/usr/bin/env python3
"""Launch the retargeted post-freeze two-hour round for AMRA targets."""

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
    / "retarget_after_freeze_20260610_2h"
)

MANUAL_AUDIT = (
    "artifacts/open_problem_screening/latest/"
    "manual_retarget_after_freeze_20260610.md"
)
STOPPED_ROOT = (
    "artifacts/open_problem_screening/latest/"
    "post_a357513_other5_second_20260610_2h"
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
            "slug": "wowii16-radius-induced-bipartite-witness",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 radius induced bipartite witness",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "wowii16_radius_induced_bipartite_witness",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 radius induced bipartite witness

The following local bridges are already Lean-verified and must not be redone:

- `connected_dist_le_two_radius_toNat`
- `no_large_radius_geodesic_interval`
- `central_interval_counting_radius_bridge`
- `central_interval_container_radius_witness`
- `central_interval_compatible_extension_radius_witness`

Add and prove the next theorem-level wrapper:

```lean
theorem wowii16_radius_induced_bipartite_witness
```

Work in `AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean`.
The theorem should use the central interval package and the compatible
extension lemma to build the induced bipartite witness needed for the original
WOWII16 lower-bound route.  If the final wrapper is still too broad, add only
one exact helper whose statement contains the missing witness data and whose
output feeds directly into `central_interval_compatible_extension_radius_witness`.
Do not return to `connected_dist_le_two_radius_toNat` or the already verified
central interval lemmas.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{STOPPED_ROOT}/runs/wowii16-connected-dist-radius-lean/"
                "wowii16-connected-dist-radius-lean-1h/lean_formalizer/"
                "round-011-central-interval-compatible-extension-radius-witness/"
                "summary.md",
                f"{STOPPED_ROOT}/runs/wowii16-connected-dist-radius-lean/"
                "wowii16-connected-dist-radius-lean-1h/proof_lab/round-010/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 2,
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

Proof-lab has already converged on this local arithmetic target.  Do not
restart broad divisor or descent discovery.  Work in namespace
`CrystalsOddVietaDescent20260610` and add:

```lean
lemma odd_vieta_d_lt_two_mul_se
    (r s d e : Nat)
    (hr : 1 <= r) (hs : 1 <= s)
    (hd : Odd d) (he : Odd e)
    (h : r * d ^ 2 + s * e ^ 2 = 2 * r * s * d * e + 1) :
    d < 2 * s * e
```

The intended proof is by contradiction from `2 * s * e <= d`.  Equality
contradicts `Odd d`; the strict case should derive
`2 * r * s * d * e < r * d ^ 2` and then contradict the displayed equation
using `1 <= s * e ^ 2`.  If Lean arithmetic blocks the proof, report the exact
failed arithmetic subclaim.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{STOPPED_ROOT}/statements/03-crystals-odd-vieta-d-lt-two-se-lean.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-diam-le-three-branch-route",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a b=diam+2 small-diameter branch",
            "statement": """
# WOWII198a b=diam+2 small-diameter branch

The large-diameter branch is Lean-verified:

- `all_eccent_eq_diam_large_diam_forces_diam_add_three_le_largestInducedBipartiteSubgraphSize`
- `b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three`

Do not redo those lemmas.  Reassess the remaining branch under:

```lean
hb2 : b G = G.diam + 2
hecc : forall v : alpha, (G.eccent v).toNat = G.diam
hdiam : G.diam <= 3
```

Find the first theorem-level move toward the original WOWII198a source
statement.  The output must be either a Lean-ready theorem for the small
diameter branch, a precise counterexample/source mismatch, or a freeze package
naming the missing structural theorem.  Avoid local simplification that does
not move the original conjecture.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{STOPPED_ROOT}/runs/wowii198a-diam-two-branch-large-diam-exclusion/"
                "wowii198a-diam-two-branch-large-diam-exclusion-1h/"
                "lean_formalizer/round-004-b-eq-diam-add-two-all-eccent-eq-diam-forces-diam-le-three/summary.md",
                f"{STOPPED_ROOT}/runs/wowii198a-diam-two-branch-large-diam-exclusion/"
                "wowii198a-diam-two-branch-large-diam-exclusion-1h/proof_lab/round-005/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "wowii200-prove-or-refute-full-deficit-objective",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 prove-or-refute full deficit objective",
            "statement": """
# WOWII200 prove-or-refute full deficit objective

Frozen routes: zero-deficit connector, raw graph6 plumbing, separator-only,
Hall/capacity, pointwise multiplicity, Posa endpoint, minimal separator,
`noncut_deficit_slot_injection`, and bounded certificate schemas without an
independent order ceiling.

Do not reselect any frozen route.  The next round has exactly three acceptable
outcomes:

1. a genuine all-orders theorem mechanism for
   `no_large_full_deficit_counterexample`, with explicit domain, codomain,
   capacity, and coverage;
2. an explicit full-hypothesis counterexample to
   `deficit_counterexample_order_le_nine`;
3. a corrected weaker final target explaining why the current order-bound
   objective is unsupported by the available formal/source assets.

If no concrete map, certificate-completeness theorem, or counterexample is
available, report that directly.  Do not produce another renamed charging or
certificate wrapper.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{STOPPED_ROOT}/runs/wowii200-deficit-counterexample-order-bound/"
                "wowii200-deficit-counterexample-order-bound-1h/proof_lab/round-006/summary.md",
                f"{STOPPED_ROOT}/runs/wowii200-deficit-counterexample-order-bound/"
                "wowii200-deficit-counterexample-order-bound-1h/supervisor/round-006/decision.md",
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
        "stopped_run_root": str(REPO / STOPPED_ROOT),
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

