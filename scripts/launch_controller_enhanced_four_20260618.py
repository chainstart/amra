#!/usr/bin/env python3
"""Launch the controller-enhanced follow-up for the four active math targets.

Assessment:
- WOWII16: freeze the current two-shell/component-flip route; no executable
  Lean target is justified.
- WOWII198a: continue the strengthened component-attachment Lean certificate.
- Erdos1: freeze the false separator route and formalize its finite
  counterexample certificate in a scratch file.
- Crystals: certify the AB bridge by Lean before AB-Z work.
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
PREVIOUS = LATEST / "manual_selected_20260618_2h"
RUN_ROOT = LATEST / "controller_enhanced_four_20260618_2h"

TIME_BUDGET_SECONDS = 2 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
LEAN_SLOT_LIMIT = 2


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


def command_prefix() -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        command += [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=6G",
            "-p",
            "MemorySwapMax=8G",
            "-p",
            "CPUQuota=120%",
        ]
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def common_args(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
    args = [
        *command_prefix(),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
        "--backend",
        "codex",
        "--search",
        "--source-first",
        "--mode",
        "lean-formalizer",
        "--workspace",
        str(FORMAL),
        "--target-file",
        target["target_file"],
        "--initial-target-theorem",
        target["target_theorem"],
        "--build-command",
        target["build_command"],
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        "3600",
        "--formalizer-attempts",
        "2",
        "--formalizer-attempt-timeout",
        "1800",
        "--formalizer-build-timeout",
        "900",
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
    if target.get("final_target_theorem"):
        args += ["--final-target-theorem", target["final_target_theorem"]]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    for completed in target.get("completed", []):
        args += ["--completed-target-theorem", completed]
    return args


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii198a-component-certificate-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "target_theorem": "exists_two_separated_component_attachments_to_longest_path_support",
            "final_target_theorem": "conjecture198a",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "completed": [
                "b_eq_four_connected_forces_indepNum_le_three",
                "diam_two_all_ecc_two_forces_delete_connected",
                "source_bound_b_eq_diam_add_one_forces_hamiltonian",
                "source_bound_b_eq_diam_add_two_forces_reduced_branch",
            ],
            "statement": """
# WOWII198a component certificate continuation

Continue Lean formalization on:

```lean
lemma exists_two_separated_component_attachments_to_longest_path_support
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha,
      ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w,
      q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support) :
    ∃ x y : alpha, ∃ ii jj : ℕ, ∃ q : G.Walk x y,
      0 < ii ∧
      ii + 1 < jj ∧
      jj < p.length ∧
      x ∉ p.support ∧
      y ∉ p.support ∧
      G.Adj x (p.getVert ii) ∧
      G.Adj y (p.getVert jj) ∧
      q.IsPath ∧
      v ∈ q.support ∧
      (∀ z : alpha, z ∈ q.support → z ∉ p.support)
```

Do not continue the vacuous helper
`exists_internally_disjoint_first_entry_prefixes_to_path_support`.
Repair the component certificate directly. First replace the invalid
`hqPrefixMeet` block by preserving outside endpoints `x,y`; then prove
`jL + 1 < jR` by longest-path splicing. Leave
`exists_four_independent_vertices_of_longest_path_missed_vertex` untouched until
this certificate verifies.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/wowii198a-component-attachments/wowii198a-component-attachments-2h/report.json",
                PREVIOUS
                / "runs/wowii198a-component-attachments/wowii198a-component-attachments-2h/supervisor/round-007/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "erdos1-separator-counterexample-lean",
            "problem_id": "erdos-problem-1",
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1SeparatorCounterexample.lean"
            ),
            "target_theorem": "upperCone_separator_lowerClosure_card_gt_half_counterexample_n5_r3",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1SeparatorCounterexample.lean"
            ),
            "statement": """
# Erdos1 separator route counterexample certificate

The original Erdos1 problem is not refuted. Freeze only the false intermediate
separator route and formalize the finite counterexample certificate in a scratch
Mathlib-only file.

Target:

```lean
theorem upperCone_separator_lowerClosure_card_gt_half_counterexample_n5_r3 :
  ∃ X M : Finset (Finset (Fin 5)),
    (∀ s ∈ X, s.card = 5 - 3) ∧
    (∀ m ∈ M, 5 - 3 < m.card) ∧
    (∀ t, (∃ s ∈ X, s ⊆ t) → t.card = 5 →
      ∃ m ∈ M, m ⊆ t) ∧
    M.card < X.card ∧
    ¬ 2 ^ (5 - 1) <
      (Finset.univ.filter fun u : Finset (Fin 5) =>
        ∃ p, (∃ s ∈ X, s ⊆ p) ∧
          (∀ m ∈ M, ¬ m ⊆ p) ∧ u ⊆ p).card
```

Use the explicit witness over `Fin 5`:
`X = {{0,1},{0,2},{0,3},{0,4}}` and
`M = {{0,1,2},{0,1,3},{0,2,3}}`.
Prove the separator by `t.card = 5 -> t = Finset.univ`; prove the filtered
lower-closure cardinal is exactly `16`; close `not 16 < 16`.
Do not import or edit the existing Erdos1 route file.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/erdos1-separator-prooflab/erdos1-separator-prooflab-2h/report.json",
                PREVIOUS
                / "runs/erdos1-separator-prooflab/erdos1-separator-prooflab-2h/supervisor/round-022/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-ab-bridge-lean",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "target_theorem": "odd_cross_halfShift_gap_AB_from_edges",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "statement": """
# Crystals AB bridge certificate

Do Lean formalization, not proof-lab route search. Add or verify the bridge:

```lean
lemma odd_cross_halfShift_gap_AB_from_edges
    (r s h u Y : Nat)
    (hr : 1 ≤ r) (hs : 1 ≤ s)
    (hY : h * u + 1 = 2 * Y)
    (hYu : 3 ≤ h * u)
    (hAmod : (Y + r * u) ∣ (Y + h * s - 1) ^ 2)
    (hBmod : (Y + h * s) ∣ (Y + r * u - 1) ^ 2)
    (hABcop : Nat.Coprime (Y + r * u) (Y + h * s)) :
    (Y + r * u) * (Y + h * s) ∣
      (2 * Y + r * u + h * s - 1) ^ 2
```

It should close by:

```lean
exact odd_cross_halfShift_gap_modular_product
  r s h u Y hr hs hY hYu hAmod hBmod hABcop
```

After this verifies, move to extended AB-Z search/descent. Do not attack
`odd_cross_halfShift_gap_AB_Z_escape` before this bridge is certified.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/crystals-abz-escape-prooflab/crystals-abz-escape-prooflab-2h/report.json",
                PREVIOUS
                / "runs/crystals-abz-escape-prooflab/crystals-abz-escape-prooflab-2h/supervisor/round-009/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
            ),
        },
    ]


FROZEN = [
    {
        "slug": "wowii16-two-shell-prooflab",
        "problem_id": "wowii-conjecture16",
        "decision": "freeze_current_route",
        "reason": (
            "The two-shell/component-flip route still lacks placeholder-free "
            "SourceShell/TargetShell, concrete X/Y/C definitions, and the "
            "collision-to-diameter step for the actual maximal pair L R. "
            "No Lean formalizer round is justified."
        ),
        "next_admissible_work": (
            "Only restart if a finite counterexample certificate for the "
            "remaining separator schemas or an exact collision-to-diameter "
            "lemma for B := (L union R) minus A is produced."
        ),
        "evidence": existing(
            PREVIOUS
            / "runs/wowii16-two-shell-prooflab/wowii16-two-shell-prooflab-2h/report.json",
            PREVIOUS
            / "runs/wowii16-two-shell-prooflab/wowii16-two-shell-prooflab-2h/supervisor/round-010/decision.md",
        ),
    }
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])
    command = common_args(target, statement_file, output_root)
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
    pending = [prepare_target(target) for target in build_targets()]
    active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "frozen": FROZEN,
        "pending": [target["slug"] for target in pending],
        "active_lean": [],
        "completed": [],
    }
    write_driver_status(status)
    while pending or active:
        while pending and len(active) < LEAN_SLOT_LIMIT:
            target = pending.pop(0)
            proc = start_process(target)
            active.append((target, proc))
        still_active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
        for target, proc in active:
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
        active = still_active
        status["pending"] = [target["slug"] for target in pending]
        status["active_lean"] = active_status(active)
        status["completed"] = completed
        write_driver_status(status)
        if pending or active:
            time.sleep(20)
    status["finished_at"] = utc_now()
    write_driver_status(status)


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [prepare_target(target) for target in build_targets()]
    assessment = {
        "generated_at": utc_now(),
        "frozen": FROZEN,
        "continued": [
            {
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "target_theorem": target["target_theorem"],
                "target_file": target["target_file"],
            }
            for target in targets
        ],
    }
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "assessment": assessment,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "workspace": str(FORMAL),
                "target_file": target["target_file"],
                "target_theorem": target["target_theorem"],
                "final_target_theorem": target.get("final_target_theorem", ""),
                "context_count": len(target.get("contexts", [])),
                "completed": target.get("completed", []),
                "command": target["command"],
            }
            for target in targets
        ],
    }
    write_json(RUN_ROOT / "assessment.json", assessment)
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
