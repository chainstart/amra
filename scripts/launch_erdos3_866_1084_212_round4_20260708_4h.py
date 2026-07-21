#!/usr/bin/env python3
"""Round-4 focused #866/#1084/#212 attack.

This launcher continues from `erdos3_866_1084_212_round3_20260708_4h`.

Frontier:
- #866: move from an accepted CES75 final-window source certificate toward a
  Lean formalization of the paper's final-window combinatorial step.
- #1084: close the singleton edge case `f 2 1 = 0`, then return to the final
  Harborth-source packaging theorem.
- #212: continue source-only algebraic-geometry auditing at the actual
  normalization/pullback bad-locus node.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round3_20260708_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round4_20260708_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round3_20260708_4h"
PREV_2 = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round2_20260708_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_round3", BASE_PATH)
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


def source_constraints_round4() -> str:
    return """\
Execution policy for this round-4 focused campaign:
- Attack only Erdos #866, #1084, and #212.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite bookkeeping.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: the current goal is not to reuse the accepted source certificate, but
  to formalize the CES75 Theorem 4 final-window combinatorial step in Lean.
  Start with the local finite-counting/window extension theorem below.
- #1084: prioritize `Erdos1084.f_two_one_eq_zero`; after it verifies, return
  to the final Harborth-source wrapper.
- #212: continue proof-lab/source mode at `ActualNormalizationPullbackBadLocusSource`;
  no Lean promotion unless a purely local finite-union bookkeeping wrapper is
  isolated.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 25 * 60
    base.LEAN_ROUND_SECONDS = 40 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 8
    base.MAX_PROMOTIONS_PER_TARGET = 4
    base.source_hard_constraints = source_constraints_round4

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "ces75_final_window_extend_four_to_six_paper_window",
            "final_target": "ces75_final_window_extend_four_to_six_paper_window",
            "statement": """\
# Erdos #866: Lean-formalize the CES75 final-window paper step

The previous round closed the source-facing bridge under the accepted CES75
final-window source certificate.  This round should push into the paper theorem
itself, starting with the concrete final-window combinatorial core.

Existing Lean lemma in `MathProject/ErdosProblem866Core.lean`:

```lean
theorem ces75_final_window_pair_exists_paper_window
```

It proves that, under the paper-window counting assumptions, there are suitable
`b5,b6`.  The next Lean target should extend four existing witnesses to six:

```lean
theorem ces75_final_window_extend_four_to_six_paper_window
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
            y = b i + x or y = b i + (z - x))
    (hfiber :
      forall y, y ∈ M ->
        ({x ∈ C | exists i : Fin 4,
          y = b i + x or y = b i + (z - x)}).card <= 8) :
    HasPairwiseSums A 6 := by
```

Expected proof shape:
- call `ces75_final_window_pair_exists_paper_window` to obtain `b5,b6`;
- define a `Fin 6 -> Int` witness extending the four old witnesses;
- prove injectivity by case splitting, using `hb4_inj`, `b5 != b6`, and
  avoidance of the old four `b i`;
- prove all pairwise sums by cases: old-old from `hb4_sum`, old-new from the
  final-window lemma, and new-new from `b5+b6=z` plus `hzA`.

If this theorem is too large, isolate the missing `Fin 6` extension lemma as
the next target, but do not fall back to the already accepted source certificate.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-08/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-08/supervisor/round-003/decision.md",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "target_file": REPO / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "fallback_target": "ces75_final_window_extend_four_to_six_paper_window",
            "contexts": existing(
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-08/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-08/supervisor/round-003/decision.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "Erdos1084.f_two_one_eq_zero",
            "final_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2",
            "statement": """\
# Erdos #1084: singleton edge lemma, then final wrapper

The positive-`n` part is local glue from:
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower`;
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source`.

The next target is the local Lean edge lemma:

```lean
theorem Erdos1084.f_two_one_eq_zero : Erdos1084.f 2 1 = 0 := by
```

Prove directly from `Erdos1084.f` and `unitDistNum`: a one-point finite planar
configuration has no unordered distinct unit-distance pair.  After this closes,
return to:

```lean
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source
    (hHarborth : Erdos1084.HarborthTwoSeparatedContactUpperGe4Source)
    (n : Nat) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
```

Do not re-run the triangular lower construction or the Harborth wrapper.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/summary.md",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/supervisor/round-001/decision.md",
                PREV_2 / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "Erdos1084.f_two_one_eq_zero",
            "contexts": existing(
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/summary.md",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/supervisor/round-001/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ActualNormalizationPullbackBadLocusSource",
            "final_target": "Erdos212.erdos_212",
            "statement": """\
# Erdos #212: actual normalization/pullback bad locus source audit

Continue proof-lab/source mode only:

```lean
theorem ActualNormalizationPullbackBadLocusSource : Prop
```

Required payload:
- name the actual projective/affine normalization-pullback map `Phi`;
- define the bad locus `B subset A^2_C` as the union of indeterminacy,
  chart-failure, boundary-line, infinity-failure, and normalization exceptional
  loci;
- cite and audit the algebraic-geometry finiteness inputs: Noetherian
  irreducible decomposition/Krull dimension over `C[x,y]`, zero-dimensional
  affine algebraic sets are finite, finite intersection with the line at
  infinity, and finite-preimage behavior away from exceptional loci;
- keep Solymosi--de Zeeuw finite exceptions as downstream unless this node
  closes them naturally.

Do not run Lean, `lake`, or re-promote the already verified local wrappers
unless a purely local finite-union bookkeeping theorem is isolated.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-10/supervisor/round-001/decision.md",
                PREV_2 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/summary.md",
                PREV_2 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ActualNormalizationPullbackBadLocusSource",
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
        "policy": "round4 #866 paper-theorem formalization, #1084 edge lemma, #212 bad-locus source; strict two-slot Lean gate",
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
        "mode": "round4 #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
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
