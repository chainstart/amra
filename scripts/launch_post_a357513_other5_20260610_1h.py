#!/usr/bin/env python3
"""Launch the post-A357513 follow-up round for the other five targets.

This reuses the existing campaign driver but replaces the target list.  Only
two targets are Lean-heavy; the other tracks stay in proof-lab/source or finite
search mode.
"""

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
    / "post_a357513_other5_20260610_1h"
)

MANUAL_AUDIT = (
    "artifacts/open_problem_screening/latest/"
    "manual_other5_post_a357513_audit_20260610.md"
)
PREV_ROOT = "artifacts/open_problem_screening/latest/manual_next_attack_20260610_1h"


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
            "slug": "wowii198a-chain-to-walk-bridge",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a List.IsChain to Walk support bridge",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "exists_walk_of_nonempty_chain_with_support",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a chain-to-walk bridge

Do not redo the leftmost fiber route.  Already verified:

- `exists_leftmost_ordered_fiber_lists`
- `exists_spliced_order_of_leftmost_ordered_fibers`

The immediate blocker is the generic bridge from a nonempty adjacent list to a
walk with exactly that support:

```lean
lemma exists_walk_of_nonempty_chain_with_support
    (G : SimpleGraph alpha)
    (order : List alpha)
    (hne : order ≠ [])
    (hchain : List.IsChain G.Adj order) :
    ∃ a b : alpha, ∃ p : G.Walk a b,
      p.support = order
```

Prove this helper in `Wowii198aLeftmost.lean`.  Use recursion/induction on the
list: singleton closes with `Walk.nil`; cons over an adjacent head edge closes
with `Walk.cons`.  After this helper verifies, stop; the next stage will use it
to prove `exists_hamiltonian_walk_of_universal_nodup_chain`.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii198a-hamiltonian-splicing-from-leftmost-fibers/"
                "wowii198a-hamiltonian-splicing-from-leftmost-fibers-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii198a-hamiltonian-splicing-from-leftmost-fibers/"
                "wowii198a-hamiltonian-splicing-from-leftmost-fibers-1h/"
                "supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-residue-card-lean",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 residue class card bound",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "centralIntervalResidueAttachCardLeContainer",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 residue-class container card bound

Do not rerun proof-lab discovery.  The route is already specified.

Add and prove:

```lean
lemma centralIntervalResidueAttachCardLeContainer
    {alpha : Type*} [DecidableEq alpha]
    (dist : alpha -> alpha -> Nat) (Adj : alpha -> alpha -> Prop)
    (p z : Nat -> alpha) (pred : alpha -> alpha)
    (commonNeighbor_dist_le_two :
      forall x y a, Adj x a -> Adj a y -> dist x y <= 2)
    (lo hi r : Nat) (P : Finset alpha)
    (hGeod : forall {i j : Nat}, i <= j -> dist (p i) (p j) = j - i)
    (hFirstL : forall i : Nat, Adj (p i) (pred (z i)))
    (hFirstR : forall i : Nat, Adj (pred (z i)) (p i))
    (hPrivateIn : forall i : Nat, i ∈ Finset.Icc lo hi -> pred (z i) ∈ P) :
    ((Finset.Icc lo hi).filter (fun i => i % 3 = r)).card <= P.card
```

Use `T := (Finset.Icc lo hi).filter (fun i => i % 3 = r)`,
`beta := {i : Nat // i ∈ T}`, `idx := Subtype.val`, and `S := T.attach` in
`centralIntervalSpacedIndexFirstStepCardLeContainer`.  Add or inline the helper
that same-residue distinct natural indices differ by more than `2` in the
ordered direction.  Stop after this lemma verifies.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii16-central-interval-extension/"
                "wowii16-central-interval-extension-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii16-central-interval-extension/"
                "wowii16-central-interval-extension-1h/supervisor/round-009/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "independent-domination80-ckko-source-audit",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-independent-domination-80",
            "title": "Independent domination 80 CKKO source witness audit",
            "statement": """
# Independent domination 80 CKKO source witness audit

Do not run a natural-language proof-discovery loop.  The current work is source
formalization.

Audit the source-facing bridge around `CkkoLargeDegreeWitness` in
`IndependentDomination80.lean`.  Check whether the local predicate matches the
external CKKO Corollary 13 hypotheses exactly: no isolated vertices, max-degree
case split, large-degree condition, parity conventions, and the Nat division
`((Delta + 2)^2) / 4`.

Return one of:

- a precise Lean-ready source theorem/wrapper still missing;
- a source mismatch with exact line/statement evidence;
- or confirmation that the remaining task is only to cite/import the CKKO
  theorem as a trusted source lemma.

Do not edit Lean in this proof-lab track.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/IndependentDomination80.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-admissible-shifted-factor-product",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals admissible shifted-factor product injectivity",
            "statement": """
# Crystal components fixed-M arithmetic blocker

Do not return to broad divisor enumeration or the discriminant-only route.

Continue the current immediate target:

```lean
theorem fixedM_admissibleShiftedFactorProduct_injective
    (q1 q2 x1 y1 x2 y2 w1 w2 : Nat)
    (hq1 : 4 <= q1) (hq2 : 4 <= q2)
    (hx1 : 1 <= x1) (hy1 : 1 <= y1)
    (hx2 : 1 <= x2) (hy2 : 1 <= y2)
    (hw1 : 3 <= w1) (hw2 : 3 <= w2)
    (hxy1 : x1 * y1 = q1 * (q1 - 2))
    (hxy2 : x2 * y2 = q2 * (q2 - 2))
    (hsum1 : x1 + y1 = (w1 - 2) * q1 + 2)
    (hsum2 : x2 + y2 = (w2 - 2) * q2 + 2)
    (hprod : w1 * q1 * (q1 - 1) = w2 * q2 * (q2 - 1)) :
    q1 = q2
```

Prove or refute it.  In the strict case `q1 < q2`, derive `w1 > w2` from
`hprod` and focus on the fixed-value expression
`(q - 1) * (2*q - 2 + x + q*(q-2)/x)`.  Return an exact smallest certificate if
the statement is false.  Do not promote to Lean formalization unless the proof
route becomes explicit.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/crystals-fixedM-harmonic-factor-sum-unique/"
                "crystals-fixedm-harmonic-factor-sum-unique-1h/summary.md",
                f"{PREV_ROOT}/runs/crystals-fixedM-harmonic-factor-sum-unique/"
                "crystals-fixedm-harmonic-factor-sum-unique-1h/supervisor/round-004/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-saturated-survivor-manifest",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 saturated survivor finite-search manifest",
            "statement": """
# WOWII200 saturated survivor manifest

Do not edit Lean and do not promote a theorem.  Use the available nauty binary:

```text
/home/biostar/.local/share/micromamba/envs/sage/bin/geng
```

Round 4 reportedly found 17 saturated `n = 8,9` survivors.  Produce a durable
table for those graph6 IDs: exact command, filter counts, `lambda`, deficits,
cut vertices, block tree, longest nonspanning paths, Posa endpoint sets,
boundaries, outside attachments, total deficit, noncut deficit sum, and minimal
deficit-cover subsets.

Then test whether the recurring certificate is exactly
`C = V \\ cutVertices(G)` with `sum_{v in C} (M - lambda(v)) >= |V|`.

Do not restart separator, Hall/capacity, pointwise multiplicity, or pure Posa
endpoint routes.
""",
            "contexts": existing(
                MANUAL_AUDIT,
                f"{PREV_ROOT}/runs/wowii200-finite-structural-certificate-search/"
                "wowii200-finite-structural-certificate-search-1h/summary.md",
                f"{PREV_ROOT}/runs/wowii200-finite-structural-certificate-search/"
                "wowii200-finite-structural-certificate-search-1h/supervisor/round-005/decision.md",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
            ),
        },
    ]


def install_overrides() -> None:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 60 * 60
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
