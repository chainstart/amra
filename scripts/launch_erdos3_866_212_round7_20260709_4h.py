#!/usr/bin/env python3
"""Round-7 focused #866/#212 continuation.

This launcher continues from `erdos3_866_1084_212_round6_20260709_4h`.

Frontier:
- #866: promote the next local CES75 final-window wrapper where the paper's
  `10t` candidate count feeds the missing-set final-window wrapper.
- #212: continue source-only work downstream of the scaled ABT transport
  certificate at `ActualCompactifiedSplitSurfaceObjectsSource`.

#1084 is intentionally omitted from active cycling in this round.  Round 6
froze it at source-governance level: the Harborth/Bezdek--Khan theorem matches
the Lean convention at source-note level, but no trusted source-admission or
verified Harborth transcription policy exists yet.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round6_20260709_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_212_round7_20260709_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round6_20260709_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_round6", BASE_PATH)
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


def source_constraints_round7() -> str:
    return """\
Execution policy for this round-7 focused campaign:
- Attack only Erdos #866 and #212.
- #1084 is frozen/source-certified only until a trusted source-admission
  policy, verified Harborth OCR/manual audit, or full formal proof route exists.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across both active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite bookkeeping.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: the next executable target is the local `10t` candidate wrapper
  `ces75_final_window_extend_four_to_six_with_ten_t_choices`; after that,
  the next source target is constructing the actual CES75 candidate window `C`
  and missing set `M`, not the final `gFun` bridge.
- #212: source-only at `ActualCompactifiedSplitSurfaceObjectsSource`; no Lean
  promotion unless the supervisor isolates a purely local finite-union or
  bookkeeping certificate.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 30 * 60
    base.LEAN_ROUND_SECONDS = 40 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 40
    base.MAX_PROMOTIONS_PER_TARGET = 4
    base.source_hard_constraints = source_constraints_round7

    by_slug = {target["slug"]: target for target in base.TARGETS}

    erdos866 = by_slug["erdos866-g6-ces75"]
    erdos866.update(
        {
            "initial_target": "ces75_final_window_extend_four_to_six_with_ten_t_choices",
            "final_target": "ces75_final_window_extend_four_to_six_with_ten_t_choices",
            "statement": """\
# Erdos #866: connect CES75's `10t` final-window count to six witnesses

Already Lean-verified in `ErdosProblem866Core.lean`:
- `ces75_final_window_pair_exists_paper_window`;
- `ces75_final_window_fiber_card_le_eight`;
- `ces75_final_window_pair_exists_without_hfiber`;
- `ces75_final_window_extend_four_to_six_without_hfiber`.
- `ces75_final_window_extend_four_to_six_with_missing_set`.

Next local Lean target:

```lean
theorem ces75_final_window_extend_four_to_six_with_ten_t_choices
    (A C M : Finset Int) (b : Fin 4 -> Int) (z : Int) (t : Nat)
    (hb4_inj : Function.Injective b)
    (hb4_sum : forall i j : Fin 4, i < j -> b i + b j ∈ A)
    (hzA : z ∈ A)
    (htpos : 0 < t)
    (hCcard10 : 10 * t <= C.card)
    (hMcard : M.card <= t)
    (hCdistinct :
      forall x, x ∈ C -> x != z - x and
        forall i : Fin 4, x != b i and z - x != b i)
    (hMleft :
      forall x, x ∈ C -> forall i : Fin 4, b i + x ∉ A -> b i + x ∈ M)
    (hMright :
      forall x, x ∈ C -> forall i : Fin 4,
        b i + (z - x) ∉ A -> b i + (z - x) ∈ M) :
    HasPairwiseSums A 6 := by
```

Proof plan:
- derive `8 * t < C.card` from `0 < t` and `10 * t <= C.card`;
- apply `ces75_final_window_extend_four_to_six_with_missing_set`;
- keep all source-level final-window hypotheses explicit.

After this verifies, do not attack the `gFun` bridge.  The real next source
target is the actual CES75 final-window package: define the candidate window
`C`, define the missing set `M`, prove `M.card <= t`, prove
`10*t <= C.card`, prove `0 < t`, and discharge the two missing-set membership
hypotheses from the paper's opposite-parity/final-window construction.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/ces75_final_window_candidate_package_certificate.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/supervisor/round-001/decision.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704_source_notes.md",
            ),
        }
    )
    erdos866["lean"].update(
        {
            "target_file": REPO / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "fallback_target": "ces75_final_window_extend_four_to_six_with_ten_t_choices",
            "contexts": existing(
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                "artifacts/source_papers/ces75/ces75_final_window_candidate_package_certificate.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )

    erdos212 = by_slug["erdos212-rational-distance-density"]
    erdos212.update(
        {
            "initial_target": "ActualCompactifiedSplitSurfaceObjectsSource",
            "final_target": "ActualCompactifiedSplitSurfaceObjectsSource",
            "statement": """\
# Erdos #212: package the compactified split surface objects

Round 6 repaired the source-level scaled ABT transport certificate.  Treat
`ActualABTScaledResolutionTransportSource` as frozen source input.

Continue proof-lab/source mode only:

```lean
theorem ActualCompactifiedSplitSurfaceObjectsSource : Prop
```

Required package:
- define `X0 := B_k = Bl_{Z_k}(V_k)`;
- define `ν : B_k -> V_k`, with `Z_k := Sing(V_k)_red`;
- identify the exceptional locus `ν⁻¹(Z_k)`;
- state the projection diagram through `π_k`;
- record the boundary/infinity bad-locus data using the transported points
  `[1 : ± i/sqrt(k) : 0]`;
- carry forward source reliance on ABT arXiv:1901.02616 and Stacks Tags
  `01OF`, `0806`.

Do not run Lean/lake and do not request promotion unless a purely local
finite-union or bookkeeping theorem is isolated.
""",
            "source_contexts": existing(
                "artifacts/source_papers/abt/abt_scaled_resolution_transport_source_certificate.md",
                "artifacts/source_papers/abt/abt_compactified_split_surface_objects_source_certificate.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-005/decision.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    erdos212["lean"].update(
        {
            "target_file": REPO / "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "fallback_target": "ActualCompactifiedSplitSurfaceObjectsSource",
            "contexts": existing(
                "artifacts/source_papers/abt/abt_scaled_resolution_transport_source_certificate.md",
                "artifacts/source_papers/abt/abt_compactified_split_surface_objects_source_certificate.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-005/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )

    base.TARGETS = [erdos866, erdos212]
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
            "round7 #866 ten-t final-window wrapper and #212 compactified split "
            "surface source packaging; #1084 frozen at source governance"
        ),
        "frozen": {
            "erdos1084-harborth-triangular": (
                "Round 6 supervisor froze this route until a trusted source "
                "admission policy, verified Harborth transcription, or full "
                "formal proof route is available."
            )
        },
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
        "mode": "round7 #866/#212 proof-lab plus strict two-slot Lean queue",
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
