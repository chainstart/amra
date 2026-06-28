#!/usr/bin/env python3
"""Launch the 2026-06-11 two-hour main-proposition push for five targets."""

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
    / "main_push_5_20260611_2h"
)

MANUAL_AUDIT = (
    "artifacts/open_problem_screening/latest/"
    "manual_main_push_5_20260611.md"
)
STOP_SNAPSHOT = (
    "artifacts/open_problem_screening/latest/"
    "proof_campaign_stop_snapshot_20260610_1615.md"
)
ID80_CERT_NOTE = (
    "artifacts/open_problem_screening/latest/"
    "id80_ckko_certificate_integration_20260610.md"
)
PREV_ROOT = (
    "artifacts/open_problem_screening/latest/"
    "retarget_after_freeze_20260610_2h"
)
PREV_SECOND_ROOT = (
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
            "slug": "wowii16-source-bound-from-radius-witness-data",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 source bound from central interval witness data",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "conjecture16_source_bound_from_central_interval_witness_data",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 source bound from central interval witness data

Already Lean-verified and not to be redone:

- `central_interval_container_radius_witness`
- `central_interval_compatible_extension_radius_witness`
- `wowii16_radius_induced_bipartite_witness`
- `conjecture16_from_maxIndepNeighborsCard_radius_bridge`

Main objective: move toward the original WOWII Conjecture 16 statement by
connecting the explicit central-interval witness data to the source-facing
radius inequality.

Target theorem name:

```lean
theorem conjecture16_source_bound_from_central_interval_witness_data
```

The theorem should consume the same explicit data as
`wowii16_radius_induced_bipartite_witness`, add the necessary relation between
the local `radius : Nat` and `G.radius.toNat`, use the produced bipartite
witness plus
`card_le_largestInducedBipartiteSubgraphSize_of_induce_isBipartite`, and then
apply `conjecture16_from_maxIndepNeighborsCard_radius_bridge`.

If the full source-facing wrapper is still too broad, add one exact helper
whose conclusion is:

```lean
2 * (((radius : Real) - 1)) + (sourceMaxIndepNeighborsCard G : Real) <= b G
```

Do not create a theorem that merely restates the existing witness wrapper.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                STOP_SNAPSHOT,
                f"{PREV_ROOT}/runs/wowii16-radius-induced-bipartite-witness/"
                "wowii16-radius-induced-bipartite-witness-1h/lean_formalizer/"
                "round-001-wowii16-radius-induced-bipartite-witness/summary.md",
                f"{PREV_SECOND_ROOT}/runs/wowii16-connected-dist-radius-lean/"
                "wowii16-connected-dist-radius-lean-1h/lean_formalizer/"
                "round-011-central-interval-compatible-extension-radius-witness/"
                "summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii198a-diam-three-six-bipartite-witness",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a diameter-three six-vertex bipartite witness",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "all_eccent_eq_diam_diam_eq_three_forces_six_le_largestInducedBipartiteSubgraphSize",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a diameter-three branch

Already Lean-verified and not to be redone:

- `all_eccent_eq_diam_large_diam_forces_diam_add_three_le_largestInducedBipartiteSubgraphSize`
- `b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_three`

Main target:

```lean
lemma all_eccent_eq_diam_diam_eq_three_forces_six_le_largestInducedBipartiteSubgraphSize
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hecc : forall v : alpha, (G.eccent v).toNat = G.diam)
    (hdiam : G.diam = 3) :
    6 <= largestInducedBipartiteSubgraphSize G
```

This is the current first theorem-level blocker for the `b = diam + 2`
small-diameter branch.  Use a diametral geodesic `a-b-c-d`, extract distance-3
witnesses from the interior vertices using `hecc`, and construct a concrete
six-vertex induced bipartite witness.  If the lemma is false, return a precise
counterexample with connectedness, diameter 3, all eccentricities 3, and
largest induced bipartite size at most 5.

Do not run another proof-lab route-discovery pass on the same lemma.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                STOP_SNAPSHOT,
                f"{PREV_ROOT}/runs/wowii198a-diam-le-three-branch-route/"
                "wowii198a-diam-le-three-branch-route-1h/supervisor/"
                "round-004/decision.md",
                f"{PREV_SECOND_ROOT}/runs/wowii198a-diam-two-branch-large-diam-exclusion/"
                "wowii198a-diam-two-branch-large-diam-exclusion-1h/lean_formalizer/"
                "round-004-b-eq-diam-add-two-all-eccent-eq-diam-forces-diam-le-three/"
                "summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-vieta-descent-to-components-unique",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals Vieta descent to component uniqueness",
            "statement": """
# Crystals Vieta descent to component uniqueness

Already Lean-verified and not to be redone:

- `odd_vieta_d_lt_two_mul_se`
- `odd_vieta_outer_d_step`

Main objective: move from the local odd Vieta arithmetic to the original
`crystals_components_unique` theorem.

This round is proof-lab, not Lean editing.  It must identify the exact next
source-faithful Lean theorem that converts `IsCrystalWithComponents n a b` and
`IsCrystalWithComponents n c d` into the Vieta equation/descent setup already
formalized in `07_crystals_odd_vieta_descent.lean`.

Acceptable outputs:

- a Lean-ready bridge theorem from the crystal divisibility hypotheses to the
  odd Vieta descent variables and measure;
- an explicit counterexample/source mismatch;
- a freeze package naming the first missing number-theoretic bridge.

Do not rediscover `odd_vieta_d_lt_two_mul_se` or `odd_vieta_outer_d_step`.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/crystals-odd-vieta-d-lt-two-se-lean/"
                "crystals-odd-vieta-d-lt-two-se-lean-1h/lean_formalizer/"
                "round-003-odd-vieta-outer-d-step/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "independent-domination80-real-ckko-certificate",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-independent-domination-80",
            "title": "Independent domination 80 trusted CKKO certificate",
            "statement": """
# Independent domination 80 trusted CKKO certificate

Already integrated and not to be redone:

- `CkkoCorollary13LeanCertificate`
- `ckko_corollary13_source_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated`
- downstream `_of_certificate` wrappers

The current AMRA file does not contain a full formalization of the CKKO paper.
The next useful work is source-certificate assimilation only.

Acceptable outputs:

- a trusted Lean proof/import that constructs
  `CkkoCorollary13LeanCertificate`;
- a precise external-formalization/import plan with exact module names and
  theorem statements;
- a freeze result saying no such trusted Lean certificate is available.

Do not add an axiom, local surrogate, proof sketch, or another downstream
adapter.  Do not retry the CKKO graph proof in proof-lab.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                ID80_CERT_NOTE,
                STOP_SNAPSHOT,
                f"{PREV_SECOND_ROOT}/runs/independent-domination80-ckko-source-certificate/"
                "independent-domination80-ckko-source-certificate-1h/supervisor/"
                "round-021/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/IndependentDomination80.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-strict-prove-refute-or-unsupported",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 strict prove-refute-or-unsupported triage",
            "statement": """
# WOWII200 strict prove/refute/unsupported triage

The ordinary proof route is unhealthy.  Frozen routes include:

- zero-deficit connector
- raw graph6 plumbing
- separator-only
- Hall/capacity
- pointwise multiplicity
- Posa endpoint
- minimal separator
- `noncut_deficit_slot_injection`
- bounded certificate schemas without an independent order ceiling

This round has exactly three acceptable outcomes:

1. a genuine all-orders theorem mechanism for
   `no_large_full_deficit_counterexample`, with explicit domain, codomain,
   capacity, and coverage;
2. an explicit full-hypothesis counterexample to
   `deficit_counterexample_order_le_nine`;
3. a corrected weaker target proving that the current order-bound objective is
   unsupported by the available formal/source assets.

If no concrete map, certificate-completeness theorem, or counterexample is
available, report that directly.  Do not produce another renamed charging,
separator, graph6, or certificate wrapper.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                STOP_SNAPSHOT,
                f"{PREV_ROOT}/runs/wowii200-prove-or-refute-full-deficit-objective/"
                "wowii200-prove-or-refute-full-deficit-objective-1h/supervisor/"
                "round-009/decision.md",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LocalGirthInducedTreeBound.lean",
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
        "previous_second_run_root": str(REPO / PREV_SECOND_ROOT),
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
