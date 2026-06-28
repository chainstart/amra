#!/usr/bin/env python3
"""Launch the next 2h round for Crystals and WOWII198a.

Directions:
- Crystals: Lean formalizer on the exact halved AB-Z obstruction.
- WOWII198a: proof-lab/source-grounding for a Lean-executable finite
  2-fan/Menger dependency; no Lean editing in this track.
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
PREVIOUS = LATEST / "controller_enhanced_four_20260618_2h"
RUN_ROOT = LATEST / "crystals_wowii198a_next_20260618_2h"

TIME_BUDGET_SECONDS = 2 * 60 * 60
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
            "MemoryMax=6G" if lean else "MemoryMax=4G",
            "-p",
            "MemorySwapMax=8G" if lean else "MemorySwapMax=5G",
            "-p",
            "CPUQuota=120%" if lean else "CPUQuota=100%",
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
        "900",
        "--proof-attempt-timeout",
        "1800",
        "--proof-audit-timeout",
        "600",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "600",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-2h",
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
            "slug": "crystals-abz-halved-obstruction-lean",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "target_theorem": "odd_cross_halfShift_gap_ABZ_halved_factor_obstruction",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "completed": [
                "odd_cross_halfShift_gap_AB_from_edges",
            ],
            "statement": """
# Crystals halved AB-Z obstruction

Run Lean formalizer work only. The AB bridge is already verified and the
unhalved odd-factor route is frozen by the counterexample `(h,u,p,q) =
(3,31,217,39)`.

Add and attack exactly this theorem-level target:

```lean
lemma odd_cross_halfShift_gap_ABZ_halved_factor_obstruction
    (h u H U : Nat)
    (hhodd : Odd h) (huodd : Odd u)
    (hHodd : Odd H) (hUodd : Odd U)
    (hhu : 3 ≤ h * u)
    (hH : h < H) (hU : u < U)
    (hAB :
      ((H * u + 1) / 2) * ((h * U + 1) / 2) ∣
        ((H * u + h * U) / 2) ^ 2)
    (hZ :
      ((H * U + 1) / 2) ∣ ((h * u - 1) / 2) ^ 2) :
    False
```

Preserve the exact halved divisibilities. Use the known unhalved counterexample
as a regression test against weakened Z conditions. If this target is still too
strong, return the smallest precise valuation/descent subclaim needed; do not
fall back to the false unhalved contradiction or broad `AB_Z_escape`.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-ab-bridge-lean/crystals-ab-bridge-lean-2h/report.json",
                PREVIOUS
                / "runs/crystals-ab-bridge-lean/crystals-ab-bridge-lean-2h/supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii198a-two-fan-source-grounding",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-conjecture198a",
            "statement": """
# WOWII198a 2-fan/Menger dependency source grounding

Do not edit Lean in this track. The previous direct formalizer run exposed the
real dependency: an endpoint-preserving finite 2-fan/Menger-style lemma from
vertex-delete connectivity. Direct Lean work on
`exists_two_internally_disjoint_paths_from_vertex_to_set_of_delete_connected`
is frozen until the theorem statement is Lean-executable.

Task:
1. Search the local Lean workspace and mathlib for existing usable theorems
   around `SimpleGraph`, `Walk`, `Connected`, `deleteVerts`, Menger, fan,
   internally disjoint paths, and separator/connectivity lemmas.
2. If a theorem exists, give the exact import/name and a Lean instantiation
   plan for `S = {z | z ∈ p.support}`.
3. If no theorem exists, design the smallest source-backed or locally provable
   substitute statement. It must be specialized enough to prove in this project
   and strong enough to supply:
   - endpoint-preserving paths from `v` to two distinct entries into
     `p.support`;
   - the `hprefixes_meet_only_v` condition;
   - a route to `ii + 1 < jj` via longest-path splicing.
4. Return one concrete next Lean target only if the statement is precise and
   has a realistic proof route. Otherwise freeze WOWII198a formalization until
   an external/source theorem is explicitly admitted by the research policy.

Do not work on the vacuous
`exists_internally_disjoint_first_entry_prefixes_to_path_support`, the
non-separated wrapper, or `exists_four_independent_vertices_of_longest_path_missed_vertex`.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii198a-component-certificate-lean/wowii198a-component-certificate-lean-2h/report.json",
                PREVIOUS
                / "runs/wowii198a-component-certificate-lean/wowii198a-component-certificate-lean-2h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
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
        command += ["--mode", "proof-lab", "--round-time-budget", "3600"]
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
            "3600",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "1800",
            "--formalizer-build-timeout",
            "900",
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
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "3072",
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
            "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "1024",
            "ARA_MATH_MAX_LOAD_PER_CPU": "100",
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
