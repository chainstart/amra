#!/usr/bin/env python3
"""Round-6 focused #866/#1084/#212 attack.

This launcher continues from `erdos3_866_1084_212_round5_20260709_4h`.

Frontier:
- #866: promote the next local CES75 final-window wrapper, eliminating the
  abstract `hfiber` hypothesis using the verified fiber-cardinality lemma.
- #1084: stop retrying the unconditional original Lean theorem; source-audit
  Harborth's contact-number theorem in the exact two-separated convention.
- #212: continue source-only work on the scaled ABT resolution transport node.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round5_20260709_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round6_20260709_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round5_20260709_4h"
PREV4 = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round4_20260708_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_round5", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base launcher: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.configure(module.load_base())


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def source_constraints_round6() -> str:
    return """\
Execution policy for this round-6 focused campaign:
- Attack only Erdos #866, #1084, and #212.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite bookkeeping.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: the next executable target is local Lean glue that removes `hfiber`
  from the final-window six-witness wrapper using the verified fiber lemma.
- #1084: do not retry unconditional Lean closure.  Certify or reject the exact
  Harborth two-separated contact-number source theorem.
- #212: source-only at the scaled ABT resolution transport node.  No Lean
  promotion unless the supervisor isolates a purely local finite-union wrapper.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 30 * 60
    base.LEAN_ROUND_SECONDS = 40 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 10
    base.MAX_PROMOTIONS_PER_TARGET = 4
    base.source_hard_constraints = source_constraints_round6

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "ces75_final_window_extend_four_to_six_without_hfiber",
            "final_target": "ces75_final_window_extend_four_to_six_without_hfiber",
            "statement": """\
# Erdos #866: remove `hfiber` from the final-window six-witness wrapper

Already Lean-verified in `ErdosProblem866Core.lean`:
- `ces75_final_window_pair_exists_paper_window`;
- `ces75_final_window_fiber_card_le_eight`;
- `ces75_final_window_extend_four_to_six_paper_window`.

Next local Lean target:

```lean
theorem ces75_final_window_extend_four_to_six_without_hfiber
    (A C M : Finset Int) (b : Fin 4 -> Int) (z : Int) (t : Nat)
    (hb4_inj : Function.Injective b)
    (hb4_sum : forall i j : Fin 4, i < j -> b i + b j ∈ A)
    (hzA : z ∈ A)
    (hCcard : 8 * t < C.card)
    (hMcard : M.card <= t)
    (hCdistinct :
      forall x, x ∈ C -> x != z - x and
        forall i : Fin 4, x != b i and z - x != b i)
    (hcover :
      forall x, x ∈ C ->
        (exists i : Fin 4, b i + x ∉ A or b i + (z - x) ∉ A) ->
          exists y, y ∈ M and exists i : Fin 4,
            y = b i + x or y = b i + (z - x)) :
    HasPairwiseSums A 6 := by
```

Proof plan:
- apply `ces75_final_window_extend_four_to_six_paper_window`;
- supply the old `hfiber` argument by
  `intro y hy; exact ces75_final_window_fiber_card_le_eight C b z y`;
- keep the statement otherwise identical to the existing paper-window wrapper.

After this verifies, the next source target is the actual CES75 candidate-window
cardinality/coverage package, not the final `gFun` bridge.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/supervisor/round-001/decision.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "target_file": REPO / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "fallback_target": "ces75_final_window_extend_four_to_six_without_hfiber",
            "contexts": existing(
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "Erdos1084.HarborthTwoSeparatedContactUpperGe4Source",
            "final_target": "Erdos1084.HarborthTwoSeparatedContactUpperGe4Source",
            "statement": """\
# Erdos #1084: source-certify Harborth in the exact Lean convention

Do not spend this round trying to prove the unconditional original theorem
`erdos_1084.variants.triangular_optimal_d2`.  The local Lean glue and the
conditional wrapper already exist; the first blocker is the external source
theorem:

```lean
def HarborthTwoSeparatedContactUpperGe4Source : Prop :=
  ∀ (N : Nat), 4 ≤ N → ∀ (s : Finset (R^2)),
    s.card = N →
    Metric.IsSeparated' 2 (s : Set (R^2)) →
    contactDistTwoNum s ≤ Nat.floor (3 * (N : R) - Real.sqrt (12 * (N : R) - 3))
```

Round-6 source task:
- use the local Harborth 1974 PDF locator and the Bezdek--Khan arXiv source note;
- decide whether Bezdek--Khan Theorem 3.1, with Harborth 1974 provenance, is an
  accepted external certificate for this exact proposition;
- explicitly normalize the conventions: unit congruent disks, center separation
  `>= 2`, contacts at center distance `2`, unordered contact count, and range
  `N >= 4`;
- if any convention mismatch remains, report it precisely.

Do not request Lean promotion unless a genuine local wrapper around an already
accepted source certificate is isolated.  Do not add axioms, opaque constants,
or an unconditional proof term for the external source theorem.
""",
            "source_contexts": existing(
                "artifacts/source_papers/harborth75/harborth_1974_source_locator.md",
                "artifacts/source_papers/harborth75/text/LsungzuProblem664AElem.Math.29197414-15.txt",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-08/summary.md",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-08/supervisor/round-004/decision.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-02/supervisor/round-001/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "target_file": REPO / "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "fallback_target": "Erdos1084.HarborthTwoSeparatedContactUpperGe4Source",
            "contexts": existing(
                "artifacts/source_papers/harborth75/harborth_1974_source_locator.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-02/supervisor/round-001/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ActualABTScaledResolutionTransportSource",
            "final_target": "ActualABTScaledResolutionTransportSource",
            "statement": """\
# Erdos #212: source-close scaled ABT resolution transport

Continue proof-lab/source mode only:

```lean
theorem ActualABTScaledResolutionTransportSource : Prop
```

The first blocker is the scaled-ABT transport certificate needed before the
compactified object package can be treated as stable:
- audit the coordinate change `Y = sqrt(k) * y`;
- identify the scaled surface `V_k(a_j,b_j)` with ABT's unscaled Section 5
  surface `V(a_j, sqrt(k) * b_j)` over `C`;
- transport ABT's singularity list and the blowup/resolution map to
  `B_k -> V_k`;
- explicitly invoke blowup functoriality under isomorphism of closed centers;
- record the transported infinity points `[1 : ± i/sqrt(k) : 0]`.

Use ABT arXiv:1901.02616 as the primary source.  Use Shaffaf arXiv:1501.00159
only as comparison if the ABT-direct route fails.  Do not run Lean/lake or
request promotion unless a purely local finite-union bookkeeping theorem is
isolated.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-001/decision.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-09/supervisor/round-001/decision.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/proof_lab/round-002/attempts/attempt_001_output.md",
                PREV4 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-08/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "target_file": REPO / "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "fallback_target": "ActualABTScaledResolutionTransportSource",
            "contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )

    return base


def launch(base: Any) -> dict[str, Any]:
    base.prepare_targets()
    for sub in ("logs", "source_statements", "lean_statements", "source_runs", "lean_runs"):
        (base.RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": base.utc_now(),
        "run_root": str(base.RUN_ROOT),
        "time_budget_seconds": base.TIME_BUDGET_SECONDS,
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
        "max_source_cycles_per_target": base.MAX_SOURCE_CYCLES_PER_TARGET,
        "max_promotions_per_target": base.MAX_PROMOTIONS_PER_TARGET,
        "policy": (
            "round6 #866 without_hfiber wrapper, #1084 Harborth source "
            "certificate, #212 scaled ABT transport; strict two-slot Lean gate"
        ),
        "targets": [
            {
                "slug": target["slug"],
                "problem": target["problem"],
                "final_target": target["final_target"],
                "initial_target": target["initial_target"],
                "lean_workspace": str(target["lean"]["workspace"]),
                "lean_target_file": str(target["lean"]["target_file"]),
                "lean_build_command": base.single_file_build_command(
                    Path(target["lean"]["workspace"]), Path(target["lean"]["target_file"])
                ),
            }
            for target in base.TARGETS
        ],
    }
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    scheduler_log = base.RUN_ROOT / "logs/scheduler.log"
    with scheduler_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, __file__, "--worker"],
            cwd=REPO,
            env=base.process_env(),
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    payload = {
        "run_root": str(base.RUN_ROOT),
        "scheduler_pid": proc.pid,
        "scheduler_log": str(scheduler_log),
        "manifest_path": str(base.RUN_ROOT / "manifest.json"),
        "queue_status_path": str(base.RUN_ROOT / "queue_status.json"),
        "mode": "round6 #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
        "max_source_cycles_per_target": base.MAX_SOURCE_CYCLES_PER_TARGET,
        "max_promotions_per_target": base.MAX_PROMOTIONS_PER_TARGET,
    }
    base.write_text(base.RUN_ROOT / "scheduler.pid", str(proc.pid))
    base.write_json(base.RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    base = configure(load_base())
    if "--worker" in sys.argv:
        base.run_worker()
        return
    print(json.dumps(launch(base), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
