#!/usr/bin/env python3
"""Round-2 focused #866/#1084/#212 attack.

This launcher continues from `erdos3_866_1084_212_20260708_4h`.

Frontier:
- #866: compose the verified CES75 source chain with the existing `gFun 6`
  square-root bridge.
- #1084: formalize the axial hex-ball lower construction.
- #212: source/spec only for ABT/Shaffaf proper-closed-container after
  normalization and pullback.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_20260708_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round2_20260708_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_20260708_4h"
PREV_2 = REPO / "artifacts/open_problem_screening/latest/erdos2_1084_212_harborth_20260707_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_20260708", BASE_PATH)
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


def source_constraints_round2() -> str:
    return """\
Execution policy for this round-2 focused campaign:
- Attack only Erdos #866, #1084, and #212.  #972 and #1052 remain excluded.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite certificates.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: do not redo `CES75K5DichotomyToIntegerSixWitnessUpperSourceChain`;
  it is verified.  Target only the final composition through the existing
  `gFun 6` bridge.
- #1084: do not re-search Harborth or re-promote the upper wrapper.  Target
  the axial hex-ball lower construction; if the proof route passes audit,
  the supervisor should return `switch_target_needs_formalizer_config` for
  `Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower`.
- #212: do not re-promote `ProjectiveAutomorphismPullbackProperZariskiClosedContainer`.
  The active node is a source/spec theorem, not Lean.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 25 * 60
    base.LEAN_ROUND_SECONDS = 40 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 12
    base.MAX_PROMOTIONS_PER_TARGET = 4
    base.source_hard_constraints = source_constraints_round2

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "CES75FinalWindowSourceImpliesG6UpperSqrtBound",
            "statement": """\
# Erdos #866: compose verified CES75 source chain with the `gFun 6` bridge

Already verified in the previous run:
`CES75K5DichotomyToIntegerSixWitnessUpperSourceChain`.

Existing bridge in `MathProject.MainClaim`:
`ces75_theorem4_integer_six_witness_upper_source_iff_g6upper_sqrt_bound`.

Current target is the final local composition:

```lean
theorem CES75FinalWindowSourceImpliesG6UpperSqrtBound
    (hfinal : CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate) :
    ∃ C : ℝ, 0 < C ∧ ∃ N0 : ℕ, ∀ n : ℕ, N0 ≤ n →
      (gFun 6 n : ℝ) ≤ C * Real.sqrt (n : ℝ) := by
```

Expected proof shape:
- use `CES75K5DichotomyToIntegerSixWitnessUpperSourceChain hfinal
  CES75K5CertificateFeedsEvenCountDichotomyWrapper` to obtain
  `CES75Theorem4IntegerSixWitnessUpperSourceStatement`;
- apply
  `(ces75_theorem4_integer_six_witness_upper_source_iff_g6upper_sqrt_bound.mp ...)`;
- add the minimal import of `MathProject.MainClaim` if needed.

Do not redo the k=5 wrapper, the final-window source certificate, or the
already verified chain.
""",
            "source_contexts": existing(
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/lean_formalizer/round-001-ces75k5dichotomytointegersixwitnessuppersourcechain/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "fallback_target": "CES75FinalWindowSourceImpliesG6UpperSqrtBound",
            "contexts": existing(
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower",
            "statement": """\
# Erdos #1084: formalize axial hex-ball lower construction

The mathematical route has passed proof-lab audit.  This is now a local Lean
construction task, not a source-search task.

Target:

```lean
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
```

Use the axial hex ball
`H n = {(i,j) : ℤ × ℤ | |i| ≤ n ∧ |j| ≤ n ∧ |i+j| ≤ n}`
embedded by
`(i,j) ↦ (i + j/2, (Real.sqrt 3 / 2) * j)`.

Required local certificate lemmas:
- `triangularHexPatch_card`: cardinality `3*n^2 + 3*n + 1`;
- `triangularHexPatch_oneSeparated`: no two distinct embedded points have
  distance below `1`;
- `triangularHexPatch_unitPairs_card`: at least, preferably exactly,
  `9*n^2 + 3*n` unordered unit-distance pairs.

Then package the finite set as a witness for `f 2`.  If no existing API is
available, introduce the smallest local construction interface in the
configured target file.  Supervisor should queue Lean promotion with
`switch_target_needs_formalizer_config`; do not stop after another source-only
replan unless the target file is genuinely unavailable.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-02/proof_lab/round-001/summary.md",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-05/supervisor/round-001/decision.md",
                PREV_2 / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-02/lean_formalizer/round-001-erdos1084-erdos-1084-variants-triangular-optimal-d2-upper-of-twoseparated-contact-source/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower",
            "contexts": existing(
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-02/proof_lab/round-001/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ABTShaffafProperClosedContainerAfterNormalizationPullbackSource",
            "statement": """\
# Erdos #212: exact ABT/Shaffaf proper-closed-container source theorem

This is source/spec work only.  Do not run Lean and do not re-promote the
already verified projective-automorphism pullback wrapper.

Current first blocker:

```lean
-- source/spec theorem only
theorem ABTShaffafProperClosedContainerAfterNormalizationPullbackSource : Prop
```

Required payload:
- universal Weak Lang/Bombieri-Lang over every number field in ABT Def. 2.1 /
  Conj. 2.2 convention;
- ABT arXiv:1901.02616 Thm. 2.4/Hassett input, Prop. 3.6 and Prop. 5.1;
- Shaffaf arXiv:1501.00159 Lemma 2 and Theorems 1-2;
- normalization of two points and return to the original `S ⊂ R^2`;
- use the already verified
  `ProjectiveAutomorphismPullbackProperZariskiClosedContainer` as local glue;
- leave component descent and Solymosi-de Zeeuw finite exceptions as named
  downstream nodes unless they become immediately source-closed.

Produce an auditable source theorem statement with exact assumptions and
remaining downstream dependencies.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-05/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-05/supervisor/round-003/decision.md",
                PREV_2 / "lean_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-lean-promotion-01/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ABTShaffafProperClosedContainerAfterNormalizationPullbackSource",
            "contexts": existing(
                PREV_2 / "lean_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-lean-promotion-01/summary.md",
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
        "policy": "round2 #866/#1084/#212; higher caps; strict two-slot Lean gate",
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
        "mode": "round2 #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
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
