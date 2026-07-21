#!/usr/bin/env python3
"""Round-5 focused #866/#1084/#212 attack.

This launcher continues from `erdos3_866_1084_212_round4_20260708_4h`.

Frontier:
- #866: continue formalizing the CES75 Theorem 4 final-window paper step, now
  removing one abstract fiber-counting hypothesis from the local core.
- #1084: move the queue-file closure toward the original `1084.lean` theorem or
  produce a precise migration blocker.
- #212: source-close the compactified split-surface object definitions needed
  before the normalization/pullback bad locus can be audited.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round4_20260708_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round5_20260709_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round4_20260708_4h"
PREV_3 = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round3_20260708_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_round4", BASE_PATH)
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


def source_constraints_round5() -> str:
    return """\
Execution policy for this round-5 focused campaign:
- Attack only Erdos #866, #1084, and #212.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite bookkeeping.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: continue formalizing CES75 Theorem 4 itself.  Do not fall back to the
  already accepted source certificate or final `gFun` bridge.
- #1084: the queue-file theorem is closed modulo workspace-wide audit.  The
  next work is original-file migration or a precise audit-scope blocker, not
  another proof of the queue-file wrapper.
- #212: continue proof-lab/source mode at `ActualCompactifiedSplitSurfaceObjectsSource`.
  No Lean promotion unless a purely local finite-union bookkeeping theorem is
  isolated.
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
    base.source_hard_constraints = source_constraints_round5

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "ces75_final_window_fiber_card_le_eight",
            "final_target": "ces75_final_window_fiber_card_le_eight",
            "statement": """\
# Erdos #866: remove the final-window fiber-counting hypothesis

Already Lean-verified:
- `ces75_final_window_pair_exists_paper_window`;
- `ces75_final_window_extend_four_to_six_paper_window`.

Next local Lean target:

```lean
theorem ces75_final_window_fiber_card_le_eight
    (C : Finset Int) (b : Fin 4 -> Int) (z y : Int) :
    ({x ∈ C | exists i : Fin 4,
      y = b i + x or y = b i + (z - x)}).card <= 8 := by
```

Mathematical proof:
- for each `i : Fin 4`, the equation `y = b i + x` has at most one solution
  `x = y - b i`;
- for each `i : Fin 4`, the equation `y = b i + (z - x)` has at most one
  solution `x = z + b i - y`;
- therefore the fiber is contained in an eight-element image indexed by
  `Fin 4 × Bool`.

After this verifies, the next target should be a version of
`ces75_final_window_pair_exists_paper_window` that derives `hfiber` internally,
not the final source certificate or the `gFun` bridge.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/supervisor/round-001/decision.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "target_file": REPO / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "fallback_target": "ces75_final_window_fiber_card_le_eight",
            "contexts": existing(
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2_original_file_port",
            "final_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2",
            "statement": """\
# Erdos #1084: port the queue-file closure toward the original theorem

The queue file now contains:
- `Erdos1084.f_two_one_eq_zero`;
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower`;
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source`;
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source`.

The original file still has:

```lean
theorem erdos_1084.variants.triangular_optimal_d2 :
    f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
  sorry
```

Current task:
- determine the smallest honest way to migrate or mirror the queue-file proof
  into `FormalConjectures/ErdosProblems/1084.lean`;
- keep Harborth as an explicit source hypothesis if needed, or report that the
  original theorem cannot be unconditional without adding the external source
  certificate to the original theorem statement;
- do not redo the triangular lower construction unless copying the existing
  queue-file local lemmas is the only viable migration path;
- if Lean promotion is attempted, target the original theorem in the original
  file and use the queue file as context, with single-file `lake env lean` only.
""",
            "source_contexts": existing(
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/supervisor/round-005/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "target_file": REPO / "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "fallback_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2",
            "contexts": existing(
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/supervisor/round-005/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ActualCompactifiedSplitSurfaceObjectsSource",
            "final_target": "Erdos212.erdos_212",
            "statement": """\
# Erdos #212: compactified split-surface object source audit

Continue proof-lab/source mode only:

```lean
theorem ActualCompactifiedSplitSurfaceObjectsSource : Prop
```

Source-close this node by fixing the actual geometric objects underlying the
normalization-pullback map:
- `X0`;
- normalization/resolution map `nu`;
- projection `pi`;
- compactified map `barPhi`;
- affine map `Phi`;
- exceptional locus `Exc(nu)`;
- chart-failure, boundary-line, and infinity-failure loci.

Decide explicitly whether the route uses the ABT surface `V` directly or
compares it to the Shaffaf split compactification.  Audit finite exceptional
and infinity images using ABT arXiv:1901.02616, Shaffaf arXiv:1501.00159, and
Stacks Project/standard Noetherian finiteness facts.  Do not run Lean unless a
purely local finite-union bookkeeping certificate is isolated.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-08/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-08/supervisor/round-001/decision.md",
                PREV_3 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV_3 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ActualCompactifiedSplitSurfaceObjectsSource",
            "contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-08/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-08/supervisor/round-001/decision.md",
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
        "policy": "round5 #866 CES75 fiber count, #1084 original port, #212 compactified objects; strict two-slot Lean gate",
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
        "mode": "round5 #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
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
