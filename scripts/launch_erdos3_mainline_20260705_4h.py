#!/usr/bin/env python3
"""Focused three-target Erdos follow-up after freezing #972/#1052.

Targets:
- #866: move beyond the verified CES75K5 local wrapper toward the original
  `gFun 6` source statement chain.
- #1084: continue Harborth/Bezdek-Khan source provenance and local
  `unitDistNum` wrapper work.
- #212: keep only the conditional Weak-Lang source package/spec line.

The launcher reuses the 2026-07-05 integrated queue machinery, including the
strict two-slot Lean gate.  No #972/#1052 cycles are started in this run.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos5_integrated_source_lean_20260705_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos3_mainline_20260705_4h"
PREV_INTEGRATED = REPO / "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h"
PREV_MAIN = REPO / "artifacts/open_problem_screening/latest/erdos5_866_mainline_20260704_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos5_integrated_20260705", BASE_PATH)
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
- Attack only #866, #1084, and #212.  #972 and #1052 are frozen out of this
  budget unless a later run supplies a new external theorem/certificate.
- Use AMRA `run-campaign-loop` with global supervisor every round.
- Natural-language/source proof-lab work may proceed across the three active
  targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue, or
  finite certificates.  Source theorem placeholders stay proof-lab/source-only.
- If the next node is an external source theorem, stay in proof-lab/source mode
  and name the exact source or certificate blocker.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- The main theorem remains the target; stage theorems are useful only when they
  shorten the path to the original Erdos statement.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.SOURCE_ROUND_SECONDS = 35 * 60
    base.LEAN_ROUND_SECONDS = 35 * 60
    base.MAX_SOURCE_CYCLES_PER_TARGET = 4
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
            "initial_target": "CES75K5DichotomyToIntegerSixWitnessUpperSourceChain",
            "statement": """\
# Erdos #866: consume the verified k=5 wrapper and attack the remaining source chain

The previous run Lean-verified:
`CES75K5CertificateFeedsEvenCountDichotomyWrapper`.

Do not re-promote that theorem.  The next objective is to connect the accepted
k=5 CES75 dichotomy/corollary package to
`CES75Theorem4IntegerSixWitnessUpperSourceStatement`, hence through the already
verified `ces75_theorem4_integer_six_witness_upper_source_iff_g6upper_sqrt_bound`
bridge to the original `gFun 6` square-root upper bound.

Work specifically on:
- direct branch `N = n`;
- lower tail `N = 20*t`;
- reflected upper tail `x -> 2*n + 2 - x`;
- final-window closure from the central-even alternative;
- constants and thresholds needed to produce the source statement
  `∃ K > 0, ∃ N0, ∀ n ≥ N0 ... HasPairwiseSums A 6`.

If a genuinely local wrapper appears, request queued Lean promotion.  If the
next node is still the external CES75 theorem/corollary itself, keep it as a
source theorem and state the exact missing source payload.
""",
            "source_contexts": existing(
                PREV_INTEGRATED / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-01/summary.md",
                PREV_INTEGRATED / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-03/summary.md",
                PREV_MAIN / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-14/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "fallback_target": "CES75K5DichotomyToIntegerSixWitnessUpperSourceChain",
            "contexts": existing(
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "HarborthBezdekKhanSourceCertificateToUnitDistNumWrapper",
            "statement": """\
# Erdos #1084: source certificate plus local `unitDistNum` wrapper

Continue this target; do not treat it as mathematically frozen.  The objective
is not to reprove Harborth from scratch.  Audit and package the external source
payload, then prove any local scaling/counting wrapper if it is small.

Required source audit:
- Harborth, "Loesung zu Problem 664A", Elem. Math. 29 (1974), 14-15;
- Bezdek-Khan arXiv:1601.00145 / journal version and its citation of
  Harborth's planar contact-number formula;
- exact convention for contact number of non-overlapping congruent disks;
- formula or needed upper bound
  `c(n,2) = floor(3*n - sqrt(12*n - 3))` for `n ≥ 2`;
- translation to local `unitDistNum`: 1-separated point sets, unordered pairs
  at distance 1, scaling between disk centers and unit-distance points.

If the source certificate is accepted, request Lean only for the local
source-to-`unitDistNum` wrapper or arithmetic bridge.  Otherwise give the exact
provenance blocker.
""",
            "source_contexts": existing(
                PREV_INTEGRATED / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-04/summary.md",
                PREV_MAIN / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-01/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "HarborthBezdekKhanSourceCertificateToUnitDistNumWrapper",
            "contexts": existing(
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ProjectiveVarietyWeakLangConditionalSourcePackageFinalSpec",
            "statement": """\
# Erdos #212: final conditional source package/spec only

Do not re-promote the previously reported Shaffaf/Solymosi-de Zeeuw Lean bridge.
This run keeps #212 only to consolidate the conditional source package:

- universal Weak Lang/Bombieri-Lang for every projective general-type variety
  over every number field;
- singular general type by desingularization/big-canonical convention;
- ABT arXiv:1901.02616 Def. 2.1, Conj. 2.2, Thm. 2.4/Hassett input,
  Prop. 3.6/5.1;
- Shaffaf arXiv:1501.00159 Lemma 2 and Theorems 1-2;
- Solymosi-de Zeeuw arXiv:0806.3095 Theorems 2.1/2.2;
- finite irreducible decomposition, infinite curve-component extraction, and
  conjugation descent via finite intersection of distinct projective plane
  curves.

This is source theorem/spec work, not Lean, unless a genuinely new local
finite-exception or real-component bookkeeping wrapper appears.
""",
            "source_contexts": existing(
                PREV_INTEGRATED / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/proof_lab/round-012/summary.md",
                PREV_INTEGRATED / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/supervisor/round-012/decision.md",
                PREV_INTEGRATED / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-03/summary.md",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ProjectiveVarietyWeakLangConditionalSourcePackageFinalSpec",
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
        "policy": "focused #866/#1084/#212; #972/#1052 frozen; strict local Lean gate",
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
        "mode": "focused three-target source search plus strict two-slot Lean queue",
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
