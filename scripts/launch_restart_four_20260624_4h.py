#!/usr/bin/env python3
"""Launch a 4h restart round for the last active math attack set.

Selection is based on the 2026-06-18 manual and controller summaries:
- Crystals: continue the narrowed Lean target.
- WOWII198a: proof-lab only, resolve the finite Menger/2-fan admission boundary.
- WOWII16: proof-lab only, replace placeholders before any Lean work.
- Erdos1: proof-lab/theorem-design, restart the original route after the
  verified separator-counterexample certificate.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
FORMAL = REPO / "amra_library" / "formal"
LATEST = REPO / "artifacts" / "open_problem_screening" / "latest"
PREVIOUS = LATEST / "crystals_wowii198a_next_20260618_2h"
MANUAL = LATEST / "manual_selected_20260618_2h"
CONTROLLER = LATEST / "controller_enhanced_four_20260618_2h"
RUN_ROOT = LATEST / "restart_four_20260624_4h"

TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
LEAN_SLOT_LIMIT = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def existing(*paths: str | Path) -> list[str]:
    found: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            found.append(str(path))
    return found


def formal_file(relative: str) -> str:
    return str(FORMAL / relative)


def build_command(relative: str) -> str:
    return f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {relative}"


def command_prefix(*, lean: bool) -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        command += [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=7G" if lean else "MemoryMax=4G",
            "-p",
            "MemorySwapMax=9G" if lean else "MemorySwapMax=5G",
            "-p",
            "CPUQuota=130%" if lean else "CPUQuota=100%",
        ]
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def common_args(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
    args = [
        *command_prefix(lean=bool(target.get("lean_heavy"))),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
        "--backend",
        "codex",
        "--search",
        "--source-first",
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--proof-attempts",
        "3",
        "--proof-audits",
        "1",
        "--proof-grounding-timeout",
        "1200",
        "--proof-attempt-timeout",
        "2400",
        "--proof-audit-timeout",
        "900",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "900",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-4h",
        "--reasoning-effort",
        "high",
    ]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    for completed in target.get("completed", []):
        args += ["--completed-target-theorem", completed]
    return args


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "crystals-factor2-obstruction-lean",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "target_theorem": "odd_cross_halfShift_gap_exact_factor2_odd_factor_divisibility_obstruction",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "completed": [
                "odd_cross_halfShift_gap_AB_from_edges",
            ],
            "statement": """
# Crystals factor-2 obstruction continuation

Continue the latest narrowed Lean target from the 2026-06-18 run:

```lean
odd_cross_halfShift_gap_exact_factor2_odd_factor_divisibility_obstruction
```

The previous campaign reduced the halved AB-Z target through scalar/common-M
subclaims to this exact factor-2 odd-factor obstruction. Start by adding the
declaration if it is absent, then split `hExact` into the three strict factor-2
divisibilities and attack the parity/valuation contradiction using `hY`, `hYu`,
`ha`, `hb`, and `hABcop`.

Do not switch back to `odd_cross_halfShift_gap_halved_fourth_edge`, do not
weaken the exact halved Z-derived third divisibility, and do not use the frozen
unhalved contradiction. If the target still stalls, return the smallest named
valuation lemma that directly proves incompatibility of the three factor-2
divisibilities.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/crystals-abz-halved-obstruction-lean/crystals-abz-halved-obstruction-lean-2h/report.json",
                PREVIOUS
                / "runs/crystals-abz-halved-obstruction-lean/crystals-abz-halved-obstruction-lean-2h/supervisor/round-008/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                "amra_library/formal/ara_tool_checks.md",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii198a-menger-admission-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-conjecture198a",
            "statement": """
# WOWII198a finite Menger/2-fan admission boundary

Do proof-lab/source-policy work only. Do not edit Lean and do not retry
`exists_two_internally_disjoint_paths_of_no_singleton_separator` or
`exists_two_internally_disjoint_paths_from_vertex_to_set_of_delete_connected`
as Lean formalizer targets in this round.

Resolve the admission boundary explicitly:

1. Identify the project-approved mechanism, if any, for introducing a sourced
   finite vertex Menger/Fan theorem under the OPEN RESEARCH policy.
2. If admission is allowed, state the exact minimal endpoint-excluding finite
   `k = 2` theorem needed to derive the unchanged endpoint-preserving fan lemma
   for `S := {z | z ∈ p.support}`.
3. If admission is not allowed, split out a separate Lean campaign plan to
   formalize finite vertex Menger/Fan before returning to WOWII198a.

Keep downstream wrappers, the vacuous prefix lemma, and
`exists_four_independent_vertices_of_longest_path_missed_vertex` frozen.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/wowii198a-two-fan-source-grounding/wowii198a-two-fan-source-grounding-2h/report.json",
                PREVIOUS
                / "runs/wowii198a-two-fan-source-grounding/wowii198a-two-fan-source-grounding-2h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/ara_tool_checks.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "wowii16-placeholder-free-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-conjecture16",
            "statement": """
# WOWII16 placeholder-free two-shell route

Continue proof-lab/theorem-design only. The current Lean file does not compile
because the frozen padding route fails, and the two-shell component-flip target
still has placeholder data. Do not run a Lean formalizer on
`Wowii16CentralCore.lean` in this round.

Produce a placeholder-free statement for:

```lean
fixed_color_two_shell_component_flip_separator_or_augment
```

The statement must define or hypothesize exact data for:
- `Outside := Finset.univ \\ (L ∪ R)`;
- source and target shell predicates;
- the alternating graph/state space for component flips;
- separator `C` as a concrete subset of `(L ∪ R) \\ A`;
- candidate shell sets `X` and `Y`;
- the dichotomy: either construct a larger admissible `L' R'`, or prove
  `((L ∪ R) \\ A).card >= X.card + Y.card`.

Audit that all vertices counted by `C` lie in `(L ∪ R) \\ A`, that flips
preserve `A ⊆ L'`, independence, and disjointness, and that the conclusion uses
the actual maximality hypothesis `hMax` for `L R`. If these cannot be made
exact, freeze WOWII16 again.
""",
            "contexts": existing(
                MANUAL / "runs/wowii16-two-shell-prooflab/wowii16-two-shell-prooflab-2h/report.json",
                "artifacts/open_problem_screening/latest/manual_next_target_selection_20260618.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
            ),
        },
        {
            "priority": 4,
            "slug": "erdos1-original-route-replan-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "erdos-problem-1",
            "statement": """
# Erdos1 original problem route restart

The false intermediate separator lemma has already been refuted and its
finite counterexample certificate was verified in the controller run. Do not
spend this round re-proving
`upperCone_separator_lowerClosure_card_gt_half_counterexample_n5_r3`.

Restart the original Erdos1 problem route from the source statement and produce
a replacement theorem-design plan. Required outputs:

1. Identify which part of the old fixed-SCD/crossing, complement-dual boundary,
   or natural permutation first-exit routes is irreparably false.
2. Propose one source-faithful replacement lemma using a known compression,
   LYM, Kruskal-Katona, normalized matching, or Boolean-lattice boundary theorem.
3. Give a finite-search protocol for small `n` that can falsify the replacement
   before Lean work begins.
4. Return exactly one next Lean-executable target only if the finite checks and
   source theorem make it credible.

No Lean formalizer work should be started for Erdos1 unless the replacement
lemma is validated and the local compile baseline issue is explicitly avoided
with a separate scratch file.
""",
            "contexts": existing(
                MANUAL / "runs/erdos1-separator-prooflab/erdos1-separator-prooflab-2h/report.json",
                CONTROLLER
                / "runs/erdos1-separator-counterexample-lean/erdos1-separator-counterexample-lean-2h/report.json",
                "artifacts/open_problem_screening/latest/manual_next_target_selection_20260618.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1SeparatorCounterexample.lean",
            ),
        },
    ]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])
    command = common_args(target, statement_file, output_root)
    if target["kind"] == "proof-lab":
        command += ["--mode", "proof-lab", "--round-time-budget", "5400"]
    else:
        command += [
            "--mode",
            "lean-formalizer",
            "--workspace",
            target["workspace"],
            "--target-file",
            target["target_file"],
            "--initial-target-theorem",
            target["target_theorem"],
            "--build-command",
            target["build_command"],
            "--round-time-budget",
            "5400",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "2400",
            "--formalizer-build-timeout",
            "1200",
        ]
    return {
        **target,
        "statement_file": str(statement_file),
        "output_root": str(output_root),
        "log_path": str(log_path),
        "command": command,
    }


def start_process(target: dict[str, Any]) -> subprocess.Popen[bytes]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "5120",
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "1024",
            "ARA_MATH_MAX_LOAD_PER_CPU": "120",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "5",
        }
    )
    with log_path.open("ab") as log:
        proc = subprocess.Popen(
            target["command"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    write_text(RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid", str(proc.pid))
    return proc


def active_status(active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]]) -> list[dict[str, Any]]:
    return [{"slug": target["slug"], "pid": proc.pid} for target, proc in active]


def write_driver_status(status: dict[str, Any]) -> None:
    status["updated_at"] = utc_now()
    write_json(RUN_ROOT / "driver_status.json", status)


def run_driver() -> None:
    targets = [prepare_target(target) for target in build_targets()]
    lean_pending = [target for target in targets if target.get("lean_heavy")]
    other_pending = [target for target in targets if not target.get("lean_heavy")]
    active_lean: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    active_other: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "pending_lean": [target["slug"] for target in lean_pending],
        "pending_other": [target["slug"] for target in other_pending],
        "active_lean": [],
        "active_other": [],
        "completed": [],
    }
    write_driver_status(status)
    while lean_pending or other_pending or active_lean or active_other:
        while lean_pending and len(active_lean) < LEAN_SLOT_LIMIT:
            target = lean_pending.pop(0)
            active_lean.append((target, start_process(target)))
        while other_pending:
            target = other_pending.pop(0)
            active_other.append((target, start_process(target)))
        for bucket_name, bucket in (("active_lean", active_lean), ("active_other", active_other)):
            still_active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
            for target, proc in bucket:
                code = proc.poll()
                if code is None:
                    still_active.append((target, proc))
                else:
                    completed.append(
                        {
                            "slug": target["slug"],
                            "returncode": code,
                            "completed_at": utc_now(),
                            "log_path": target["log_path"],
                            "output_root": target["output_root"],
                        }
                    )
            if bucket_name == "active_lean":
                active_lean = still_active
            else:
                active_other = still_active
        status["pending_lean"] = [target["slug"] for target in lean_pending]
        status["pending_other"] = [target["slug"] for target in other_pending]
        status["active_lean"] = active_status(active_lean)
        status["active_other"] = active_status(active_other)
        status["completed"] = completed
        write_driver_status(status)
        if lean_pending or other_pending or active_lean or active_other:
            time.sleep(20)
    status["finished_at"] = utc_now()
    write_driver_status(status)


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "kind": target["kind"],
                "problem_id": target["problem_id"],
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "workspace": target.get("workspace", ""),
                "target_file": target.get("target_file", ""),
                "target_theorem": target.get("target_theorem", ""),
                "context_count": len(target.get("contexts", [])),
                "completed": target.get("completed", []),
                "command": target["command"],
            }
            for target in targets
        ],
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    driver_log = RUN_ROOT / "logs" / "driver.log"
    with driver_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--driver"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    write_text(RUN_ROOT / "pids" / "driver.pid", str(proc.pid))
    manifest["driver_pid"] = proc.pid
    manifest["driver_log"] = str(driver_log)
    write_json(RUN_ROOT / "manifest.json", manifest)
    return manifest


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--driver":
        run_driver()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
