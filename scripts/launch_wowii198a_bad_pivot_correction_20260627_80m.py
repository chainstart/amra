#!/usr/bin/env python3
"""Launch an 80m correction run for WOWII198a bad-pivot repair."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
BASE_PATH = REPO / "scripts" / "launch_main_target_four_20260627_2h.py"
spec = importlib.util.spec_from_file_location("main_target_four_base", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load base launcher from {BASE_PATH}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.PREVIOUS = base.LATEST / "main_target_three_20260627_next_2h"
base.RUN_ROOT = base.LATEST / "wowii198a_bad_pivot_correction_20260627_70m"
base.TIME_BUDGET_SECONDS = 70 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60


def build_targets() -> list[dict[str, Any]]:
    current = base.PREVIOUS / "runs" / "wowii198a-left-first-crossing-lean" / "wowii198a-left-first-crossing-lean-2h"
    previous = (
        base.LATEST
        / "main_target_three_20260627_followup_2h"
        / "runs"
        / "wowii198a-bad-pivot-descent-lean"
        / "wowii198a-bad-pivot-descent-lean-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii198a-bad-pivot-extremal-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_suffix_retention_bad_pivot_descent",
            "mode": "lean-formalizer",
            "round_time_budget": 2400,
            "formalizer_attempts": 6,
            "formalizer_attempt_timeout": 1600,
            "formalizer_build_timeout": 1200,
            "lean_heavy": True,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "completed": [
                "exists_terminal_set_endpoint_avoiding_pair",
                "terminalPathPairWeightedMeasure_lt_of_commonCard_lt",
                "not_mem_dropUntil_of_mem_dropUntil_reverse_on_isPath",
                "terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained",
                "terminal_set_fan_splice_descent_left_of_hsep_of_first_crossing_not_retained",
            ],
            "statement": f"""
# WOWII198a correction: repair the bad-pivot extremal package

Final target: `conjecture198a`.

Current real first build blocker:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

The earlier `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`
formalizer loop was stopped because every attempt failed before reaching that
target.  The Lean file currently fails inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent` at the two residual
containment branches around lines 4589 and 4676:
`exact hpair_measure_min` is being used where Lean needs membership in the old
common-support-with-`x`-erased set.

Required output:
- Repair `terminal_set_fan_left_suffix_retention_bad_pivot_descent` so the
  target file builds.
- Do not mark this target or
  `terminal_set_fan_left_suffix_retention_alt_intersections_control` as already
  completed; this run is specifically to certify them.
- Replace the two arbitrary residual containment steps with the intended
  order-extremal bad-pivot or weighted-measure argument.
- If the current arbitrary-`z` statement is too strong, introduce a proved
  order-extremal helper and adjust the downstream use so the same parent
  `terminal_set_fan_left_suffix_retention_alt_intersections_control` remains
  available without weakening the final chain.
- The acceptable chain is:
  repaired bad-pivot package ->
  `terminal_set_fan_left_suffix_retention_alt_intersections_control` ->
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt` ->
  left splice descent -> mirrored right splice -> two-fan theorem ->
  longest-path missed-vertex contradiction -> Chvatal-Erdos traceability ->
  `conjecture198a`.
- Run and pass:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Do not broaden to the splice wrapper and do not continue first-crossing until
this bad-pivot target has a verified proof.  If the target statement is
mathematically false, return a concrete finite/order obstruction and the exact
replacement statement required to keep the chain to `conjecture198a`.
""",
            "contexts": base.existing(
                current / "lean_formalizer/round-001-terminal-set-fan-left-first-crossing-uncrossing-commoncard-lt/summary.md",
                current / "lean_formalizer/round-002-terminal-set-fan-left-first-crossing-uncrossing-commoncard-lt/attempts/attempt_002/attempt_report.json",
                current / "lean_formalizer/round-002-terminal-set-fan-left-first-crossing-uncrossing-commoncard-lt/attempts/attempt_002/backend_last_message.txt",
                current / "supervisor/round-001/decision.md",
                previous / "summary.md",
                previous / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-bad-pivot-descent/summary.md",
                previous / "proof_lab/round-005/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_formalizer_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_proof_notes.md",
                "amra_library/formal/proof_notes/wowii198a_left_first_crossing_round008.md",
                "amra_library/formal/proof_notes/wowii198a_left_first_crossing_round010.md",
                base.RESOURCES,
            ),
        }
    ]


base.build_targets = build_targets


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (base.RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [base.prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": base.utc_now(),
        "run_root": str(base.RUN_ROOT),
        "time_budget_seconds": base.TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": base.HARD_TIMEOUT_SECONDS,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "final_target": target["final_target"],
                "initial_target": target.get("initial_target", ""),
                "mode": target.get("mode", ""),
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "context_count": len(target.get("contexts", [])),
                "completed": target.get("completed", []),
                "command": target["command"],
            }
            for target in targets
        ],
    }
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    driver_log = base.RUN_ROOT / "logs" / "driver.log"
    with driver_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--driver"],
            cwd=base.REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    base.write_text(base.RUN_ROOT / "pids" / "driver.pid", str(proc.pid))
    manifest["driver_pid"] = proc.pid
    manifest["driver_log"] = str(driver_log)
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    return manifest


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--driver":
        base.run_driver()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
