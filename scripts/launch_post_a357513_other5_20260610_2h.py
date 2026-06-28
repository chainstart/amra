#!/usr/bin/env python3
"""Launch a two-hour post-A357513 follow-up round for the other five targets."""

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
    / "post_a357513_other5_20260610_2h"
)

READINESS = (
    "artifacts/open_problem_screening/latest/"
    "a357513_paper_readiness_20260610.md"
)
MANUAL_AUDIT = (
    "artifacts/open_problem_screening/latest/"
    "manual_other5_post_a357513_audit_20260610.md"
)
PREV_ROOT = "artifacts/open_problem_screening/latest/post_a357513_other5_20260610_1h"


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
            "slug": "wowii198a-source-bound-two-value-split",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a source bound two-value split",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "source_bound_forces_b_eq_diam_add_one_or_two",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a source-bound branch split

Do not revisit verified chain, splicing, Hamiltonian, or `b = diam + 1` branch
wrappers.  They are already Lean-verified.

Current target:

```lean
lemma source_bound_forces_b_eq_diam_add_one_or_two
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (hb : ((b G : Nat) : Real) <= 2 + averageEccentricity G) :
    b G = G.diam + 1 \\/ b G = G.diam + 2
```

Use `diam_add_one_le_b` and `averageEccentricity_le_diam` if available.  The
proof should only establish the integer branch split from the source inequality.
If coercions differ locally, align the statement to the existing declarations
while preserving this exact mathematical content.
""",
            "contexts": existing(
                READINESS,
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii198a-chain-to-walk-bridge/"
                "wowii198a-chain-to-walk-bridge-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii198a-chain-to-walk-bridge/"
                "wowii198a-chain-to-walk-bridge-1h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-graph-bridge-spec",
            "kind": "proof-lab",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 graph bridge specification",
            "statement": """
# WOWII16 graph bridge specification

The residue-card and full three-residue interval lemmas are already Lean
verified.  Do not rerun them and do not send `centralIntervalGraphBridgeToConjecture16`
to Lean until its source-faithful declaration is precise.

Proof-lab objective: synthesize the exact graph-level bridge from the abstract
central interval package to the source theorem.  The declaration must specify:

- central geodesic interval data;
- the functions `p`, `z`, and `pred`;
- the container `P`;
- how the hypotheses of `centralIntervalFullIndexCardLeThreeContainer` are
  obtained;
- how `P` yields an induced bipartite witness counted by `b G`;
- the final inequality needed for WOWII16.

End with one Lean-ready declaration or explain the missing source definition.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii16-residue-card-lean/"
                "wowii16-residue-card-lean-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii16-residue-card-lean/"
                "wowii16-residue-card-lean-1h/supervisor/round-012/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "independent-domination80-ckko-source-wrapper",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-independent-domination-80",
            "title": "Independent domination 80 CKKO source wrapper",
            "statement": """
# Independent domination 80 CKKO source wrapper

Do not repeat the source audit.  No source mismatch was found.  The missing
object is the trusted source theorem/wrapper for CKKO Corollary 1.3.

Return a source-formalization plan with the exact Lean declaration:

```lean
theorem ckko_corollary13_source_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (Delta : Nat) (hDelta : 0 < Delta)
    (hMax : G.maxDegree <= Delta)
    (hIso : 0 < G.minDegree) :
    let m := ((Delta + 2)^2) / 4
    exists S : Finset V,
      G.IsNIndepDominatingSet S.card S /\\
      m * S.card <= (m - Delta) * Fintype.card V
```

Then specify exactly how it specializes to `Delta := G.maxDegree` to obtain
`CkkoLargeDegreeWitness G`.  Do not edit Lean in this proof-lab track and do
not add axioms/sorries.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/independent-domination80-ckko-source-audit/"
                "independent-domination80-ckko-source-audit-1h/summary.md",
                f"{PREV_ROOT}/runs/independent-domination80-ckko-source-audit/"
                "independent-domination80-ckko-source-audit-1h/supervisor/round-008/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/IndependentDomination80.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-no-odd-vieta-descent",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals no odd Vieta descent",
            "statement": """
# Crystal components odd-q Vieta descent

Do not return to broad divisor enumeration or discriminant-only arguments.

Current blocker:

```lean
lemma no_odd_vieta_descent
    (r s d e : Nat)
    (hr : 1 <= r) (hs : 1 <= s)
    (hd : Odd d) (he : Odd e)
    (h : r * d ^ 2 + s * e ^ 2 = 2 * r * s * d * e + 1) :
    False
```

Produce a clean written proof or the smallest exact counterexample.  If proving,
use well-founded descent on `d+e`: handle `r*s = 1`, exclude boundary equalities
`d = s*e` and `e = r*d`, prove the middle region contradiction, then use the
Vieta replacement in the two outer regions.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/crystals-admissible-shifted-factor-product/"
                "crystals-admissible-shifted-factor-product-1h/summary.md",
                f"{PREV_ROOT}/runs/crystals-admissible-shifted-factor-product/"
                "crystals-admissible-shifted-factor-product-1h/supervisor/round-004/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-noncut-deficit-bridge",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 noncut deficit structural bridge",
            "statement": """
# WOWII200 noncut deficit structural bridge

Do not edit Lean and do not promote a theorem.  Treat the `geng` manifest as
finite evidence, not proof.

Current target:

`noncut_deficit_sum_ge_card`

Focus on one of two repairs:

1. give a checkable charging/injection proof of
   `sum_{v in V \\ cutVertices(G)} (M - lambda(v)) >= |V|`
   under connected + nontraceable + short-girth + path-1-tough + saturated
   hypotheses; or
2. state a bounded-classification lemma with explicit hypotheses reducing every
   equality-counterexample to the verified 17 graph6 survivors.

Do not restart separator, Hall/capacity, pointwise multiplicity, or pure Posa
endpoint routes.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii200-saturated-survivor-manifest/"
                "wowii200-saturated-survivor-manifest-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii200-saturated-survivor-manifest/"
                "wowii200-saturated-survivor-manifest-1h/supervisor/round-005/decision.md",
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
        "paper_readiness": str(REPO / READINESS),
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
