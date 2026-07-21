#!/usr/bin/env python3
"""Focused #866/#1084/#212 follow-up with the new source certificates.

Targets:
- #866: CES75 Theorem 4 final-window source certificate from the downloaded
  Acta Arithmetica PDF.
- #1084: triangular/hexagonal lattice lower-bound construction; Harborth is
  already sourced.
- #212: continue the ABT/Shaffaf/SdZ source/spec chain after the verified local
  projective-automorphism pullback wrapper.

The run keeps the strict two-slot Lean gate and avoids whole-project Lean
builds.  Source/proof-lab work is allowed across all three active targets.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos3_mainline_20260705_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_20260708_4h"
PREV_3 = REPO / "artifacts/open_problem_screening/latest/erdos3_mainline_20260705_4h"
PREV_2 = REPO / "artifacts/open_problem_screening/latest/erdos2_1084_212_harborth_20260707_4h"
PREV_5 = REPO / "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h"
PREV_866 = REPO / "artifacts/open_problem_screening/latest/erdos5_866_mainline_20260704_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos3_mainline_20260705", BASE_PATH)
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


def source_constraints_focused() -> str:
    return """\
Execution policy for this focused campaign:
- Attack only Erdos #866, #1084, and #212.  #972 and #1052 remain excluded.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed across all three active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue,
  arithmetic lemmas, construction certificates, or finite certificates.
- External source theorem placeholders stay proof-lab/source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- #866 should consume the local CES75 PDF/OCR locator; do not ask the user for
  another source copy unless the page-image certificate genuinely conflicts.
- #1084 should not re-search Harborth; the active target is the lower-bound
  triangular/hexagonal construction.
- #212 should not re-promote the verified projective-automorphism pullback
  wrapper; the active route is the remaining ABT/Shaffaf/SdZ chain.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 35 * 60
    base.LEAN_ROUND_SECONDS = 35 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 5
    base.MAX_PROMOTIONS_PER_TARGET = 2
    base.source_hard_constraints = source_constraints_focused

    keep = {
        "erdos866-g6-ces75",
        "erdos1084-harborth-triangular",
        "erdos212-rational-distance-density",
    }
    base.TARGETS = [target for target in base.TARGETS if target["slug"] in keep]
    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "CES75Theorem4FinalWindowParagraphTranscriptionSourceCertificate",
            "statement": """\
# Erdos #866: CES75 Theorem 4 final-window source certificate

The CES75 PDF is now locally available and page-located:
- `artifacts/source_papers/ces75/ces75_theorem4_source_locator.md`
- `artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt`
- rendered page images `artifacts/source_papers/ces75/page-05.png` and
  `artifacts/source_papers/ces75/page-06.png`.

Do not re-prove the already handled k=5 corollary wrapper.  The first target is
the missing source certificate for Theorem 4's final-window paragraph:
- journal page 41 bottom to page 42 top;
- variables `b5,b6`, equation `b5+b6=z5`;
- window centered at `z5/2` with radius `20*t`;
- parity switch: choose even `b5,b6` if `b1,...,b4` are odd, and odd otherwise;
- initially `10*t` possible choices;
- each earlier `bi` excludes at most `t` choices, for four `bi`;
- resulting all pairwise sums `bi+bj` lie in `A`.

After this certificate is closed, connect it to
`CES75Theorem4IntegerSixWitnessUpperSourceStatement` and then to the original
`gFun 6` square-root upper bound through the existing bridge.  Lean promotion is
allowed only for local glue around an already accepted source statement.
""",
            "source_contexts": existing(
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
                "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
                PREV_3 / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-04/summary.md",
                PREV_5 / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV_5 / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-03/summary.md",
                PREV_866 / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-14/summary.md",
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
                "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
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
# Erdos #1084: prove the triangular/hexagonal lattice lower bound

Harborth 1974 is now sourced in
`artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md`.
Do not re-search Harborth and do not re-promote the contact-number upper
wrapper.

The current first blocker toward the original `triangular_optimal_d2` theorem is
the lower construction:

```lean
theorem Erdos1084.erdos_1084.variants.triangular_optimal_d2_lower (n : ℕ) :
    9 * n ^ 2 + 3 * n ≤ f 2 (3 * n ^ 2 + 3 * n + 1) := by
```

Find or define the smallest local construction interface for a triangular or
hexagonal lattice patch:
- point count `3*n^2 + 3*n + 1`;
- 1-separatedness;
- at least `9*n^2 + 3*n` unordered unit-distance pairs;
- packaged as a lower bound for `f 2`.

Lean promotion is appropriate for this lower-bound theorem if a local
construction API is available.  If no usable API exists, report the exact
missing construction interface instead of widening to the final equality.
""",
            "source_contexts": existing(
                "artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md",
                PREV_2 / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-05/summary.md",
                PREV_2 / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-05/supervisor/round-001/decision.md",
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
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
                PREV_2 / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-05/supervisor/round-001/decision.md",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ABTShaffafSdZFiniteExceptionChainAfterPullbackWrapper",
            "statement": """\
# Erdos #212: continue after the verified projective pullback wrapper

The local wrapper
`ProjectiveAutomorphismPullbackProperZariskiClosedContainer` was verified in the
previous run.  Do not re-promote it.

Current target: close the remaining source/spec chain to the original theorem:
- accept/package the ABT/Shaffaf proper-closed-container theorem under
  universal Weak Lang/Bombieri-Lang over every number field;
- include ABT arXiv:1901.02616 Def. 2.1, Conj. 2.2, Thm. 2.4/Hassett input,
  Prop. 3.6 and Prop. 5.1;
- include Shaffaf arXiv:1501.00159 Lemma 2 and Theorems 1-2;
- perform the proper closed subset/component descent from complex projective
  containment to an infinite real curve component;
- apply Solymosi-de Zeeuw arXiv:0806.3095 Theorems 2.1/2.2;
- preserve exact finite-exception constants: line all but at most 4 points,
  circle all but at most 3 points.

Lean is allowed only for a genuinely local downstream wrapper such as component
descent or finite-exception bookkeeping.  ABT/Shaffaf/SdZ themselves remain
external source theorems.
""",
            "source_contexts": existing(
                PREV_2 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-03/summary.md",
                PREV_2 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-03/supervisor/round-006/decision.md",
                PREV_2 / "lean_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-lean-promotion-01/summary.md",
                PREV_5 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/proof_lab/round-012/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ABTShaffafSdZFiniteExceptionChainAfterPullbackWrapper",
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
        "policy": "focused #866/#1084/#212; CES75 and Harborth sources available; strict two-slot Lean gate",
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
        "mode": "focused #866/#1084/#212 proof-lab plus strict two-slot Lean queue",
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
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
