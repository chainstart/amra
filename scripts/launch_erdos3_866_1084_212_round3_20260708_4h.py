#!/usr/bin/env python3
"""Round-3 focused #866/#1084/#212 attack.

This launcher continues from `erdos3_866_1084_212_round2_20260708_4h`.

Frontier:
- #866: source-audit and package the CES75 final-window certificate instead of
  re-running the already verified local `gFun 6` Lean bridge.
- #1084: combine the verified triangular lower construction with the Harborth
  upper wrapper into the final triangular-optimal packaging target.
- #212: continue source/spec work at the component-descent node after the
  ABT/Shaffaf proper-closed-container source node.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round2_20260708_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round3_20260708_4h"
PREV = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round2_20260708_4h"
PREV_1 = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_20260708_4h"
PREV_2 = REPO / "artifacts/open_problem_screening/latest/erdos2_1084_212_harborth_20260707_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_866_1084_212_round2", BASE_PATH)
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


def source_constraints_round3() -> str:
    return """\
Execution policy for this round-3 focused campaign:
- Attack only Erdos #866, #1084, and #212.  #972 and #1052 remain excluded.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite bookkeeping.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866: do not re-run `CES75FinalWindowSourceImpliesG6UpperSqrtBound`; it is
  verified.  Focus on the source certificate/final packaging.
- #1084: do not re-run `triangular_optimal_d2_lower`; it is locally complete.
  Target final packaging from lower plus Harborth upper, with any `n = 0`
  edge case isolated explicitly.
- #212: treat `ABTShaffafProperClosedContainerAfterNormalizationPullbackSource`
  as accepted source/spec context.  Continue component descent source mode only
  unless a purely local finite/component wrapper is identified.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 30 * 60
    base.LEAN_ROUND_SECONDS = 35 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 10
    base.MAX_PROMOTIONS_PER_TARGET = 3
    base.source_hard_constraints = source_constraints_round3

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate",
            "statement": """\
# Erdos #866: CES75 final-window source certificate and final packaging

Already Lean-verified in the previous round:

```lean
theorem CES75FinalWindowSourceImpliesG6UpperSqrtBound
    (hfinal : CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate) :
    exists C : Real, 0 < C and exists N0 : Nat, forall n : Nat, N0 <= n ->
      (gFun 6 n : Real) <= C * Real.sqrt (n : Real)
```

Do not re-run that theorem.  The active target is the source certificate:

```lean
-- source/spec theorem only unless the supervisor identifies purely local glue
theorem CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate : Prop
```

Audit the final paragraph of Choi--Erdos--Szemeredi Theorem 4:
- journal page 41 bottom to page 42 top;
- variables `b5,b6`, equation `b5+b6=z5`;
- interval centered at `z5/2`, radius `20*t`;
- parity switch depending on `b1,...,b4`;
- initially `10*t` choices;
- each of four previous `bi` excludes at most `t` choices;
- all pairwise sums remain in `A`.

The expected output is a durable, explicit source certificate and a final
dependency summary: original #866 follows from CES75 final-window source plus
the already verified local Lean bridge.  Request Lean only for a small wrapper
if the source certificate is accepted as an explicit hypothesis.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/lean_formalizer/round-001-ces75finalwindowsourceimpliesg6uppersqrtbound/summary.md",
                PREV / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-01/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "fallback_target": "CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate",
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
            "initial_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source",
            "statement": """\
# Erdos #1084: final packaging from Harborth upper plus triangular lower

Already locally complete:
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower`;
- `Erdos1084.erdos_1084.variants.triangular_optimal_d2_upper_of_twoSeparated_contact_source`;
- `HarborthBezdekKhanSourceCertificateToUnitDistNumWrapper`.

Do not re-run the lower construction.  The active target is the final packaging:

```lean
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source
    (hHarborth : Erdos1084.HarborthTwoSeparatedContactUpperGe4Source)
    (n : Nat) :
    Erdos1084.f 2 (3 * n ^ 2 + 3 * n + 1) = 9 * n ^ 2 + 3 * n := by
```

Expected route:
- for `1 <= n`, combine the verified upper wrapper and lower theorem with
  antisymmetry;
- isolate the `n = 0` edge case explicitly.  If the current local API cannot
  prove `f 2 1 = 0` quickly, introduce/report the smallest missing lemma rather
  than looping on the lower construction;
- if the unconditional theorem is blocked only by `n = 0`, produce a conditional
  `1 <= n` final theorem and a precise edge-case target.

Lean promotion is appropriate only for this small final wrapper or the tiny
`f 2 1 = 0` edge lemma.  Keep the Harborth theorem as an explicit source
hypothesis unless the source certificate itself is being audited.
""",
            "source_contexts": existing(
                "artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/supervisor/round-004/decision.md",
                PREV / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-03/summary.md",
                PREV_2 / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-02/lean_formalizer/round-001-erdos1084-erdos-1084-variants-triangular-optimal-d2-upper-of-twoseparated-contact-source/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2_final_of_harborth_source",
            "contexts": existing(
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/summary.md",
                PREV / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-01/supervisor/round-004/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ProperComplexProjectiveClosedContainerComponentDescentSource",
            "statement": """\
# Erdos #212: component descent after the proper projective closed container

Treat the previous node as source-closed:

```lean
theorem ABTShaffafProperClosedContainerAfterNormalizationPullbackSource : Prop
```

Do not re-promote `ProjectiveAutomorphismPullbackProperZariskiClosedContainer`.
The active target is source/spec only:

```lean
theorem ProperComplexProjectiveClosedContainerComponentDescentSource : Prop
```

Required payload:
- from a proper complex projective Zariski-closed container
  `Z subset P^2_C` for the affine image of `S subset R^2`, extract finitely
  many irreducible affine algebraic curve components covering all non-finite
  affine points of `S`;
- isolate zero-dimensional components as finite leftovers;
- isolate boundary-line/infinity contributions as finite leftovers;
- preserve the link back to real affine points;
- leave Solymosi--de Zeeuw finite exceptions as the next downstream node unless
  the source proof immediately closes it.

Use proof-lab/source mode.  Request Lean only if a purely local finite-union or
finite-leftover bookkeeping wrapper is identified.
""",
            "source_contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/supervisor/round-001/decision.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-11/summary.md",
                PREV_2 / "lean_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-lean-promotion-01/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ProperComplexProjectiveClosedContainerComponentDescentSource",
            "contexts": existing(
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/summary.md",
                PREV / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-12/supervisor/round-001/decision.md",
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
        "policy": "round3 #866/#1084/#212; final packaging plus component descent; strict two-slot Lean gate",
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
        "mode": "round3 #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
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
