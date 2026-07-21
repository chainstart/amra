#!/usr/bin/env python3
"""Focused #1084/#212 follow-up after obtaining the Harborth scan.

This run intentionally excludes #866 because CES75 Theorem 4 source lookup is
now a separate user-side acquisition task.  It also excludes #972/#1052.

The worker still reuses the AMRA proof-lab/source campaign machinery and the
strict two-slot Lean gate inherited from the previous supervised launchers.
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
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos2_1084_212_harborth_20260707_4h"
PREV_3 = REPO / "artifacts/open_problem_screening/latest/erdos3_mainline_20260705_4h"
PREV_5 = REPO / "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h"


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
- Attack only Erdos #1084 and #212.  #866, #972, and #1052 are excluded from
  this budget.
- Use AMRA `run-campaign-loop` with the global supervisor every round.
- Source/proof-lab work may proceed for both active targets.
- Lean promotion is allowed only for genuinely local wrappers, local glue, or
  finite certificates.  External source theorem placeholders stay proof-lab or
  source-only.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- For #1084, treat Harborth 1974 as now found and move to source-to-local
  wrapper work unless the source note itself is contradicted.
- For #212, keep the original rational-distance nondensity theorem as the
  target; stage theorems matter only if they close the conditional source
  package or finite-exception/spec bridge.
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
        "erdos1084-harborth-triangular",
        "erdos212-rational-distance-density",
    }
    base.TARGETS = [target for target in base.TARGETS if target["slug"] in keep]
    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "Harborth1974SourceAcceptedToUnitDistNumWrapper",
            "statement": """\
# Erdos #1084: Harborth source is found; attack source-to-`unitDistNum` wrapper

The Harborth scan supplied by the user is now rendered and summarized in:
`artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md`.

Treat Harborth, solution to Problem 664A, Elemente der Mathematik 29 (1974),
14-15, as the external source for the congruent closed disk contact-number
formula

`B(n) = floor(3*n - sqrt(12*n - 3))`.

This round should not re-search for Harborth.  Attack the local bridge:
- exact convention alignment between Harborth's disks and local 1-separated
  finite point sets;
- unordered contact pairs versus unordered unit-distance pairs;
- scaling from unit disks/contact distance `2` to local unit distance `1`;
- domain restrictions such as `n >= 2`;
- the triangular-number/substitution arithmetic needed by the local Erdos
  #1084 statement.

If this bridge is small and local, request queued Lean promotion.  If the
source note still leaves a convention gap, state the precise gap instead of
freezing the whole target.
""",
            "source_contexts": existing(
                "artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md",
                PREV_3 / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-04/summary.md",
                PREV_5 / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-04/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "Harborth1974SourceAcceptedToUnitDistNumWrapper",
            "contexts": existing(
                "artifacts/source_papers/harborth_1974/harborth_1974_problem_664a_source_note.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ProperClosedPlaneRationalDistanceSetLineCircleFiniteExceptionSourceSpec",
            "statement": """\
# Erdos #212: close the conditional source/spec bridge to the original theorem

Continue source/spec work on the original rational-distance nondensity target.
Do not drift into unrelated ABT or Lang generalities unless they directly feed
the final statement.

Primary objective:
package the theorem that a proper Zariski-closed subset of the complex
projective plane containing an infinite rational-distance set forces, after
finite exceptions, containment in a real affine line or real affine circle.

Required interfaces:
- universal Weak Lang/Bombieri-Lang for projective general-type varieties over
  every number field;
- ABT arXiv:1901.02616 Def. 2.1, Conj. 2.2, Thm. 2.4/Hassett input,
  Prop. 3.6/5.1;
- Shaffaf arXiv:1501.00159 Lemma 2 and Theorems 1-2;
- Solymosi-de Zeeuw arXiv:0806.3095 Theorems 2.1/2.2;
- finite irreducible decomposition, infinite curve-component extraction,
  conjugation descent, and finite intersection of distinct projective plane
  curves;
- exact finite-exception constants: line all but at most 4 points, circle all
  but at most 3 points.

Use Lean only if a genuinely local finite-exception or decomposition wrapper is
ready for small single-file checking.  Otherwise produce the final source
specification and exact remaining blocker.
""",
            "source_contexts": existing(
                PREV_3 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/proof_lab/round-012/summary.md",
                PREV_3 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/supervisor/round-012/decision.md",
                PREV_5 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/proof_lab/round-012/summary.md",
                PREV_5 / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-03/summary.md",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "fallback_target": "ProperClosedPlaneRationalDistanceSetLineCircleFiniteExceptionSourceSpec",
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
        "policy": "focused #1084/#212; Harborth source found; #866 excluded pending CES75 source lookup",
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
        "mode": "focused #1084/#212 proof-lab plus strict two-slot Lean queue",
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
