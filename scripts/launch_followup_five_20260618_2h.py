#!/usr/bin/env python3
"""Launch a 2h follow-up round for the five active math propositions.

The launch follows the latest supervisor decisions from
`formal_next_after_guided_20260613_2h`.
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
    / "followup_five_20260618_2h"
)
PREVIOUS = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "formal_next_after_guided_20260613_2h"
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
            "slug": "wowii198a-longest-path-contradiction",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-conjecture198a",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "target_theorem": "longest_path_missed_vertex_contradiction_of_indepNum_le_three",
            "final_target_theorem": "conjecture198a",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "completed": [
                "b_eq_four_connected_forces_indepNum_le_three",
                "diam_two_all_ecc_two_forces_delete_connected",
                "source_bound_b_eq_diam_add_one_forces_hamiltonian",
                "source_bound_b_eq_diam_add_two_forces_reduced_branch",
            ],
            "statement": """
# WOWII198a longest-path missed-vertex contradiction

Continue the Chvatal-Erdos traceability route.  Attack exactly this Lean target:

```lean
lemma longest_path_missed_vertex_contradiction_of_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    {G : SimpleGraph alpha}
    (hconn : G.Connected)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3)
    {a b v : alpha} (p : G.Walk a b)
    (hpPath : p.IsPath)
    (hmax : ∀ u w : alpha, ∀ q : G.Walk u w, q.IsPath → q.support.length ≤ p.support.length)
    (hv : v ∉ p.support)
    (hnot_left : ¬ G.Adj v a)
    (hnot_right : ¬ G.Adj b v) :
    False
```

Use existing maximum-path endpoint non-adjacency helpers and
`exists_path_of_delete_connected_avoiding`; repair that helper only if it
blocks the build.  Prove the actual rotation/independent-set contradiction:
from a missed vertex and deletion-connectivity, build avoiding paths/rotations,
extract an independent set of size at least four if the maximum path is not
spanning, and contradict `SimpleGraph.IsIndepSet.card_le_indepNum`.
Do not touch the reduced-branch or leftmost-fiber packages.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii198a-chvatal-erdos-traceability/wowii198a-chvatal-erdos-traceability-2h/report.json",
                PREVIOUS / "runs/wowii198a-chvatal-erdos-traceability/wowii198a-chvatal-erdos-traceability-2h/summary.md",
                PREVIOUS / "runs/wowii198a-chvatal-erdos-traceability/wowii198a-chvatal-erdos-traceability-2h/supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-metric-count-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "wowii-conjecture16",
            "statement": """
# WOWII16 metric-count proof-lab replan

Do not Lean-edit yet.  Focus only on:

```lean
fixed_color_blocking_core_extra_vertices_metric_count
```

Produce at least two independent route attempts and audit the best route.  The
route must use `hMax` for the actual maximal pair `L R`: assume
`((L ∪ R) \\ A).card < 2 * (G.radius.toNat - 1)`, derive structural constraints
on vertices outside `L ∪ R` from non-extendability, and use
`2 < G.radius.toNat` plus `G.diam + 1 < 2 * G.radius.toNat` to contradict those
constraints or build a larger fixed-color extension.  Do not continue the
frozen single-radius-geodesic padding route, and do not revive the
central-interval route.  End with an exact Lean lemma if a smaller theorem is
found.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii16-fixed-color-extra-vertices/wowii16-fixed-color-extra-vertices-2h/report.json",
                PREVIOUS / "runs/wowii16-fixed-color-extra-vertices/wowii16-fixed-color-extra-vertices-2h/summary.md",
                PREVIOUS / "runs/wowii16-fixed-color-extra-vertices/wowii16-fixed-color-extra-vertices-2h/supervisor/round-008/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-scd-crossing-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "erdos-problem-1",
            "statement": """
# Erdos #1 SCD/crossing proof-lab replan

Do not Lean-edit yet.  Focus only on:

```lean
downClosed_centralLayer_card_le_setFamilyOuterBoundary_card
```

Produce a concrete theorem-level route for the down-closed central-layer bound.
Specify an explicit symmetric-chain decomposition or equivalent crossing/counting
certificate in Lean terms, including exact declarations for:
- the chain object;
- coverage and disjointness;
- the lemma showing each chain crossing from inside `D` to outside `D`
  contributes a distinct outer-boundary vertex;
- the count showing `D.card = 2 ^ (n - 1)` forces at least one crossing for
  each middle-layer chain/member.

Do not revisit `negativeSignedCut_cubeOuterBoundary_card_le_N`, support
transport, disjointness, or permutation invariance.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos1-harper-closed-neighborhood/erdos1-harper-closed-neighborhood-2h/report.json",
                PREVIOUS / "runs/erdos1-harper-closed-neighborhood/erdos1-harper-closed-neighborhood-2h/summary.md",
                PREVIOUS / "runs/erdos1-harper-closed-neighborhood/erdos1-harper-closed-neighborhood-2h/supervisor/round-008/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-product-obstruction-prooflab",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "statement": """
# Crystals product-preserving obstruction proof-lab

Continue proof-lab, not Lean editing.  Current target:

```lean
odd_product_preserving_halfShift_one_sided_obstruction
```

First audit the Round 4 `odd-rectangle-edge-congruence-no-corner-square`
attempt: state the exact congruence lemma it needs in Lean-ready variables, and
check whether it proves the current product-preserving obstruction or only
restates `hleft`.  If viable, produce the precise sublemma and dependency chain.
If not viable, immediately run a targeted counterexample search for the reduced
`(x,y,p,q)` statement ordered by smallest `q`, using only odd `p,q,x,y`,
`3 <= p`, `p < x,y < q`, `x*y = p*q`, `hleft`, and the right divisibility.
Report the smallest witness or the exact missing strengthened hypothesis.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-interlaced-product-prooflab/crystals-interlaced-product-prooflab-2h/report.json",
                PREVIOUS / "runs/crystals-interlaced-product-prooflab/crystals-interlaced-product-prooflab-2h/summary.md",
                PREVIOUS / "runs/crystals-interlaced-product-prooflab/crystals-interlaced-product-prooflab-2h/supervisor/round-004/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
            ),
        },
        {
            "priority": 5,
            "slug": "erdos212-post-endpoint-source-audit",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "erdos-problem-212",
            "statement": """
# Erdos #212 post-endpoint source-faithfulness audit

The conditional endpoint wrapper is verified:

```lean
no_erdos_212_formal_statement_of_bombieri_lang
```

Do not redo it, and do not attempt to prove Bombieri-Lang or the unconditional
open problem.  This round should decide whether any meaningful next theorem
remains for AMRA: a source-faithful final packaging theorem, a bridge to the
FormalConjectures `erdos_212` statement, or a freeze recommendation.  If a
bridge is possible without `answer(sorry)` or axioms, state the exact Lean target.
Otherwise recommend freezing this problem as conditionally formalized and ready
for documentation, not further proof search.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos212-formal-endpoint-wrapper/erdos212-formal-endpoint-wrapper-2h/report.json",
                PREVIOUS / "runs/erdos212-formal-endpoint-wrapper/erdos212-formal-endpoint-wrapper-2h/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
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
