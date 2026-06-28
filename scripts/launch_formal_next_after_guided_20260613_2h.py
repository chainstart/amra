#!/usr/bin/env python3
"""Launch the next 2h mixed AMRA round after guided proof-lab target selection.

Lean-heavy campaigns are capped at two concurrent slots.  Crystals remains
proof-lab only; GRAPH-002 stays frozen.
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
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "formal_next_after_guided_20260613_2h"
)
PREVIOUS = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "guided_prooflab_next_20260613_2h"
)
STRICT_PREVIOUS = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "main_original_plus_next_20260613_1h_strict_slots"
)

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
        "2",
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
            "slug": "wowii198a-chvatal-erdos-traceability",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-conjecture198a",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "target_theorem": "chvatal_erdos_connected_delete_connected_indepNum_le_three_traceable",
            "final_target_theorem": "conjecture198a",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "completed": [
                "b_eq_four_connected_forces_indepNum_le_three",
                "diam_two_all_ecc_two_forces_delete_connected",
                "source_bound_b_eq_diam_add_two_forces_reduced_branch",
                "source_bound_b_eq_diam_add_one_forces_hamiltonian",
            ],
            "statement": """
# WOWII198a traceability bridge

The `Wowii198aLeftmost.lean` file has been cleaned: the `#exit` barriers were
removed and the duplicate reduced-branch block after the second barrier was
discarded.  The file now builds.

Attack this Lean target:

```lean
theorem chvatal_erdos_connected_delete_connected_indepNum_le_three_traceable
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3) :
    ∃ order : List alpha,
      order.Nodup ∧
      (∀ v : alpha, v ∈ order) ∧
      List.IsChain G.Adj order
```

Use a source-faithful Chvatal-Erdos traceability consequence or a specialized
finite longest-path proof.  Once this verifies, the next bridge is
`two_connected_indepNum_le_three_forces_hamiltonian_walk`, obtained by applying
`exists_hamiltonian_walk_of_universal_nodup_chain`.  Do not rework the verified
reduced-branch lemmas or the `b = diam + 1` leftmost-fiber package.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii198a-file-shape-traceability-route/wowii198a-file-shape-traceability-route-2h/report.json",
                PREVIOUS / "runs/wowii198a-file-shape-traceability-route/wowii198a-file-shape-traceability-route-2h/summary.md",
                PREVIOUS / "runs/wowii198a-file-shape-traceability-route/wowii198a-file-shape-traceability-route-2h/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-fixed-color-extra-vertices",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "wowii-conjecture16",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"),
            "target_theorem": "conjecture16_fixed_color_blocking_core_extra_vertices_of_radius_diam_small",
            "final_target_theorem": "conjecture16",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"),
            "completed": [
                "conjecture16_source_bound_of_radius_gt_two_of_diam_large",
                "conjecture16_source_bound_of_radius_toNat_le_two",
            ],
            "statement": """
# WOWII16 fixed-color strict branch

Attack the strict-branch lemma selected by the supervisor:

```lean
theorem conjecture16_fixed_color_blocking_core_extra_vertices_of_radius_diam_small
```

Use maximality contrapositively: if fewer than `2 * (r - 1)` vertices lie in
`(L ∪ R) \\ A`, construct an admissible fixed-color extension `L' R'`
containing `A` with larger union, contradicting maximality.  The construction
must use the metric assumptions `2 < r` and `diam + 1 < 2 * r`.  Do not revive
the frozen central-interval route.  After this lemma verifies, derive
`conjecture16_fixed_color_blocking_core_radius_diam_dichotomy`, then the small
branch and final source wrapper.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii16-fixed-color-dichotomy-route/wowii16-fixed-color-dichotomy-route-2h/report.json",
                PREVIOUS / "runs/wowii16-fixed-color-dichotomy-route/wowii16-fixed-color-dichotomy-route-2h/summary.md",
                PREVIOUS / "runs/wowii16-fixed-color-dichotomy-route/wowii16-fixed-color-dichotomy-route-2h/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "erdos212-formal-endpoint-wrapper",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "erdos-problem-212",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"),
            "target_theorem": "no_erdos_212_formal_statement_of_bombieri_lang",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"),
            "completed": [
                "rational_distance_subset_line_or_circle_union_finset_of_bombieri_lang",
                "no_dense_of_pairwise_rational_distances_of_bombieri_lang",
            ],
            "statement": """
# Erdos #212 endpoint wrapper

Attack the low-risk endpoint wrapper:

```lean
theorem no_erdos_212_formal_statement_of_bombieri_lang
    (hBL : BombieriLangConsequenceForRationalDistanceSets) :
    ¬ ∃ u : Set ℂ,
      Dense u ∧ u.Pairwise (fun z w => dist z w ∈ Set.range Rat.cast)
```

Given `⟨u, hdense, hpair⟩`, prove `PairwiseRationalDistances u`. Equal pairs
use `q = 0`; distinct pairs use `hpair hz hw hne` and unpack
`Set.range Rat.cast`. Then apply
`no_dense_of_pairwise_rational_distances_of_bombieri_lang hBL`.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos212-real-plane-endpoint-route/erdos212-real-plane-endpoint-route-2h/report.json",
                PREVIOUS / "runs/erdos212-real-plane-endpoint-route/erdos212-real-plane-endpoint-route-2h/summary.md",
                PREVIOUS / "runs/erdos212-real-plane-endpoint-route/erdos212-real-plane-endpoint-route-2h/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "erdos1-harper-closed-neighborhood",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "erdos-problem-1",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"),
            "target_theorem": "setFamilyClosedNeighborhood_card_ge_half_cube_add_central_of_card_half",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"),
            "completed": [
                "negativeSignedCut_cubeOuterBoundary_card_le_N",
                "setFamilyClosedNeighborhood_half_cube_ge_central_of_outer",
            ],
            "statement": """
# Erdos #1 Harper closed-neighborhood target

Attack the selected Harper/isoperimetric target:

```lean
theorem setFamilyClosedNeighborhood_card_ge_half_cube_add_central_of_card_half
    (n : ℕ) (𝒜 : Finset (Finset (Fin n)))
    (hn : 0 < n)
    (h𝒜 : 𝒜.card = 2 ^ (n - 1)) :
    2 ^ (n - 1) + Nat.choose n (n / 2) ≤
      (𝒜 ∪ setFamilyOuterBoundary 𝒜).card
```

Formalize or import the special Harper closed-neighborhood result for Boolean
lattice families of cardinality `2^(n-1)`.  Do not redo
`negativeSignedCut_cubeOuterBoundary_card_le_N`.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos1-harper-downstream-target/erdos1-harper-downstream-target-2h/report.json",
                PREVIOUS / "runs/erdos1-harper-downstream-target/erdos1-harper-downstream-target-2h/summary.md",
                PREVIOUS / "runs/erdos1-harper-downstream-target/erdos1-harper-downstream-target-2h/supervisor/round-001/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "crystals-interlaced-product-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "statement": """
# Crystals interlaced product obstruction

Continue proof-lab, not Lean editing.  Current target:

```lean
halfShift_interlaced_product_no_Z_dvd_YsubOne_sq
```

Start from the odd-product identity and rewrite it as the shared common-M
identity `2*A*B - (A+B-1) = 2*Y*Z - (Y+Z-1)`.  Combine `A*B ∣ M^2`,
`Nat.Coprime A B`, interlacing `Y < A,B < Z`, and hypothetical
`Z ∣ (Y - 1)^2`.  Prioritize a prime-valuation contradiction.  If this fails,
run a targeted counterexample search over abstract `(A,B,Y,Z)` and report the
smallest satisfying all hypotheses.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-common-m-interlaced-obstruction/crystals-common-m-interlaced-obstruction-2h/report.json",
                PREVIOUS / "runs/crystals-common-m-interlaced-obstruction/crystals-common-m-interlaced-obstruction-2h/summary.md",
                PREVIOUS / "runs/crystals-common-m-interlaced-obstruction/crystals-common-m-interlaced-obstruction-2h/supervisor/round-001/decision.md",
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


def global_lean_campaign_count() -> int:
    try:
        output = subprocess.check_output(["ps", "-eo", "pid,cmd"], text=True)
    except Exception:
        return 0
    seen: set[str] = set()
    for line in output.splitlines():
        if "run.py run-campaign-loop" not in line:
            continue
        if "--mode lean-formalizer" not in line and "--mode hybrid" not in line:
            continue
        if Path(__file__).name in line:
            continue
        parts = line.strip().split(None, 1)
        if parts:
            seen.add(parts[0])
    return len(seen)


def active_status(active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]]) -> list[dict[str, Any]]:
    return [{"slug": target["slug"], "pid": proc.pid} for target, proc in active]


def write_driver_status(status: dict[str, Any]) -> None:
    status["updated_at"] = utc_now()
    write_json(RUN_ROOT / "driver_status.json", status)


def run_driver() -> None:
    targets = [prepare_target(target) for target in build_targets()]
    proof_targets = [target for target in targets if not target.get("lean_heavy")]
    lean_pending = [target for target in targets if target.get("lean_heavy")]
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
        "frozen": ["graph002-witness-certificate-search"],
    }
    for target in proof_targets:
        active_other.append((target, start_process(target)))
    while lean_pending or active_lean or active_other:
        while (
            lean_pending
            and len(active_lean) < LEAN_SLOT_LIMIT
            and global_lean_campaign_count() < LEAN_SLOT_LIMIT * 2
        ):
            target = lean_pending.pop(0)
            active_lean.append((target, start_process(target)))
            status["pending"] = [item["slug"] for item in lean_pending]
            status["active_lean"] = active_status(active_lean)
            status["active_other"] = active_status(active_other)
            status["global_lean_campaign_count"] = global_lean_campaign_count()
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
        status["global_lean_campaign_count"] = global_lean_campaign_count()
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
        "frozen": ["graph002-witness-certificate-search"],
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
