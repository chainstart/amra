#!/usr/bin/env python3
"""Launch the manually selected 2026-06-18 math attack round.

This round follows `manual_next_target_selection_20260618.md`:
- WOWII198a: Lean formalizer.
- WOWII16, Erdos1, Crystals: proof-lab/theorem-design.
- Erdos212: excluded/frozen.
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
RUN_ROOT = LATEST / "manual_selected_20260618_2h"
PREVIOUS = LATEST / "followup_five_20260618_2h"
MANUAL_REPORT = LATEST / "manual_next_target_selection_20260618.md"

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
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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
        "600",
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
            "slug": "wowii198a-component-attachments",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-conjecture198a",
            "workspace": str(FORMAL),
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
# WOWII198a component attachment formalizer

Run Lean formalization, not broad proof-lab.

The previous run confirmed that the current file fails at two placeholders:
`exists_two_separated_attachments_to_longest_path_support` and
`exists_four_independent_vertices_of_longest_path_missed_vertex`.

Attack the strengthened component certificate first:

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

Use existing helpers:
- `exists_missed_to_right_path_avoiding_left`
- `exists_left_to_missed_path_avoiding_right`
- `exists_first_entry_edge_to_path_support`
- maximum-path endpoint non-adjacency helpers.

Do not retarget the final wrapper yet. After this certificate verifies, the
next stage is `exists_four_independent_vertices_of_longest_path_missed_vertex`.
Do not touch reduced-branch, leftmost-fiber, Hamiltonian-walk, or unrelated
list-conversion declarations.
""",
            "contexts": existing(
                MANUAL_REPORT,
                PREVIOUS
                / "runs/wowii198a-longest-path-contradiction/wowii198a-longest-path-contradiction-2h/report.json",
                PREVIOUS
                / "runs/wowii198a-longest-path-contradiction/wowii198a-longest-path-contradiction-2h/summary.md",
                PREVIOUS
                / "runs/wowii198a-longest-path-contradiction/wowii198a-longest-path-contradiction-2h/supervisor/round-005/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-two-shell-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "wowii-conjecture16",
            "statement": """
# WOWII16 two-shell component-flip theorem design

Do not Lean-edit yet.

The old single-radius-geodesic padding route is frozen and the current Lean file
does not compile at that route. Work only on making the next target
placeholder-free:

```lean
lemma fixed_color_two_shell_component_flip_separator_or_augment
```

The previous supervisor target still had arbitrary placeholder parameters
`C X Y`. Replace them with exact definitions or hypotheses:
- `Outside := Finset.univ \\ (L ∪ R)`;
- source/target shell predicates;
- the alternating graph or state space for component flips;
- separator `C` as a concrete subset of blockers in `(L ∪ R) \\ A`;
- shell candidate sets `X` and `Y` as defined sets, not arbitrary parameters.

Prove or refute that the non-augmenting case gives
`((L ∪ R) \\ A).card ≥ X.card + Y.card`.

Audit requirements:
- every counted separator vertex must lie in `(L ∪ R) \\ A`;
- every augmenting flip must preserve `A ⊆ L'`, independence, and disjointness;
- the contradiction must use the actual maximal pair `L R` through `hMax`.

If a placeholder-free statement cannot be obtained, recommend freezing WOWII16
again rather than launching a Lean formalizer round.
""",
            "contexts": existing(
                MANUAL_REPORT,
                PREVIOUS
                / "runs/wowii16-metric-count-prooflab/wowii16-metric-count-prooflab-2h/report.json",
                PREVIOUS
                / "runs/wowii16-metric-count-prooflab/wowii16-metric-count-prooflab-2h/summary.md",
                PREVIOUS
                / "runs/wowii16-metric-count-prooflab/wowii16-metric-count-prooflab-2h/supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-separator-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "erdos-problem-1",
            "statement": """
# Erdos #1 upper-cone separator theorem design

Do not Lean-edit yet. The current Lean file has baseline compile errors, and
the new separator target is not declared.

Attack or refute the pure Boolean-lattice separator lemma:

```lean
theorem upperCone_separator_lowerClosure_card_gt_half
    (n r : ℕ) (X M : Finset (Finset (Fin n)))
    (hn : 0 < n)
    (hr : 2 * r ≤ n + 1)
    (hXrank : ∀ s ∈ X, s.card = n - r)
    (hMrank : ∀ m ∈ M, n - r < m.card)
    (hsep : ∀ t, (∃ s ∈ X, s ⊆ t) → t.card = n →
      ∃ m ∈ M, m ⊆ t)
    (hsmall : M.card < X.card) :
    2 ^ (n - 1) <
      (Finset.univ.filter fun u : Finset (Fin n) =>
        ∃ p, (∃ s ∈ X, s ⊆ p) ∧
          (∀ m ∈ M, ¬ m ⊆ p) ∧ u ⊆ p).card
```

First do finite counterexample search. If no counterexample appears, identify
the exact compression/Kruskal-Katona/normalized-matching theorem needed. Do not
return to the frozen routes: fixed-SCD one-crossing, complement-dual boundary
transport, permutation first-exit load, support transport, or closed-neighborhood
splitting.
""",
            "contexts": existing(
                MANUAL_REPORT,
                PREVIOUS
                / "runs/erdos1-scd-crossing-prooflab/erdos1-scd-crossing-prooflab-2h/report.json",
                PREVIOUS
                / "runs/erdos1-scd-crossing-prooflab/erdos1-scd-crossing-prooflab-2h/summary.md",
                PREVIOUS
                / "runs/erdos1-scd-crossing-prooflab/erdos1-scd-crossing-prooflab-2h/supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-abz-escape-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "statement": """
# Crystals AB-Z escape proof-lab

Do not Lean-edit yet.

The one-sided product-preserving obstruction is false; do not target
`odd_product_preserving_halfShift_one_sided_obstruction`. The explicit witness
is `(p,q,x,y) = (21,99,63,33)`.

Attack the compressed target:

```lean
theorem odd_cross_halfShift_gap_AB_Z_escape
    (r s h u Y : ℕ)
    (hr : 1 ≤ r) (hs : 1 ≤ s)
    (hhodd : Odd h) (huodd : Odd u)
    (hY : h * u + 1 = 2 * Y)
    (hYu : 3 ≤ h * u)
    (hAB : (Y + r * u) * (Y + h * s) ∣
      (2 * Y + r * u + h * s - 1) ^ 2)
    (hZmod : Y + r * u + h * s + 2 * r * s ∣ (Y - 1) ^ 2) :
    Y = 1
```

Required order:
1. Prove that this AB statement is genuinely implied by the prior three-edge
   target using `hAmod`, `hBmod`, and coprimality.
2. Extend targeted counterexample search beyond the manual local range
   `Y <= 300`, `r,s <= 200`, where no witness was found.
3. If no witness appears, attack the prime-power/common-M descent from `hAB`
   and `hZmod`.
4. If AB-Z is refuted, fall back to `odd_cross_halfShift_gap_no_right_edge` and
   report the smallest witness.
""",
            "contexts": existing(
                MANUAL_REPORT,
                PREVIOUS
                / "runs/crystals-product-obstruction-prooflab/crystals-product-obstruction-prooflab-2h/report.json",
                PREVIOUS
                / "runs/crystals-product-obstruction-prooflab/crystals-product-obstruction-prooflab-2h/summary.md",
                PREVIOUS
                / "runs/crystals-product-obstruction-prooflab/crystals-product-obstruction-prooflab-2h/supervisor/round-005/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
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
        command += ["--mode", "proof-lab", "--round-time-budget", "6600"]
    else:
        command += [
            "--mode",
            target["kind"],
            "--workspace",
            target["workspace"],
            "--target-file",
            target["target_file"],
            "--initial-target-theorem",
            target["target_theorem"],
            "--build-command",
            target["build_command"],
            "--round-time-budget",
            "4200",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "1800",
            "--formalizer-build-timeout",
            "900",
        ]
        if target.get("final_target_theorem"):
            command += ["--final-target-theorem", target["final_target_theorem"]]
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
    proof_targets = [target for target in targets if not target.get("lean_heavy")]
    active_lean: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    active_other: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "pending": [target["slug"] for target in lean_pending],
        "active_lean": [],
        "active_other": [],
        "completed": completed,
    }
    for target in proof_targets:
        active_other.append((target, start_process(target)))
    while lean_pending or active_lean or active_other:
        while lean_pending and len(active_lean) < LEAN_SLOT_LIMIT:
            target = lean_pending.pop(0)
            active_lean.append((target, start_process(target)))
            status["pending"] = [item["slug"] for item in lean_pending]
            status["active_lean"] = active_status(active_lean)
            status["active_other"] = active_status(active_other)
            write_driver_status(status)
            time.sleep(5)
        for bucket_name, bucket in (("active_lean", active_lean), ("active_other", active_other)):
            still_active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
            for target, proc in bucket:
                code = proc.poll()
                if code is None:
                    still_active.append((target, proc))
                    continue
                completed.append(
                    {
                        "slug": target["slug"],
                        "kind": target["kind"],
                        "pid": proc.pid,
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
        status["pending"] = [target["slug"] for target in lean_pending]
        status["active_lean"] = active_status(active_lean)
        status["active_other"] = active_status(active_other)
        status["completed"] = completed
        write_driver_status(status)
        if lean_pending or active_lean or active_other:
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
        "excluded": ["erdos212-post-endpoint-source-audit"],
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
                "final_target_theorem": target.get("final_target_theorem", ""),
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
