#!/usr/bin/env python3
"""Launch the next 2h AMRA round with Lean slots and proof-lab parallelism.

The round follows the latest supervisor state:

* start proof-lab/source-grounding targets immediately;
* run Lean formalizer targets only while the global Lean slot count is below 2;
* keep the already frozen Erdos #972 and 1/3-2/3 routes out of this round.
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
    / "next_round_slots_20260613_2h"
)

TIME_BUDGET_SECONDS = 2 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
LEAN_SLOT_LIMIT = 2

PREVIOUS_ROUND = (
    "artifacts/open_problem_screening/latest/"
    "eight_next_round_20260612_1h"
)


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
        *command_prefix(lean=target["kind"] == "lean-formalizer"),
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
        "--proof-attempt-timeout",
        "900",
        "--proof-audit-timeout",
        "300",
        "--proof-grounding-timeout",
        "420",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "420",
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
    return args


def previous_summary(slug: str) -> str:
    return f"{PREVIOUS_ROUND}/runs/{slug}/{slug}-1h/summary.md"


def previous_decision(slug: str, round_no: int) -> str:
    return (
        f"{PREVIOUS_ROUND}/runs/{slug}/{slug}-1h/"
        f"supervisor/round-{round_no:03d}/decision.md"
    )


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii16-radius-gt-two-diam-large",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 high-radius diameter-large branch",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "target_theorem": "conjecture16_source_bound_of_radius_gt_two_of_diam_large",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16: Lean target outside the frozen radius-two branch

Continue only this theorem-level target:

```lean
theorem conjecture16_source_bound_of_radius_gt_two_of_diam_large
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (hG : G.Connected)
    (hRadius : 2 < G.radius.toNat)
    (hdiam : (2 * G.radius.toNat : Nat) <= G.diam + 1) :
    letI maxL := (Finset.univ.image (fun v => indepNeighborsCard G v)).max' (by simp)
    letI r := G.radius.toNat
    2 * ((r : Real) - 1) + (maxL : Real) <= b G
```

Use the existing WOWII13 bridge:
`conjecture16_from_conjecture13_of_radius_diam_bridge (G := G) hG`.
First isolate the Nat-to-Real arithmetic from `hdiam`, for example by
`exact_mod_cast hdiam`, then normalize casts and close by `linarith`.

Do not reopen `conjecture16_source_bound_of_radius_toNat_le_two`, its support
lemmas, or any central-interval witness route.
""",
            "contexts": existing(
                previous_summary("wowii16-freeze-radius-two-and-retarget"),
                previous_decision("wowii16-freeze-radius-two-and-retarget", 7),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "erdos1-negative-signed-cut-half-card",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-erdos-1",
            "title": "Erdos #1 negative signed cut half-cardinality",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"
            ),
            "target_theorem": "negativeSignedCut_card_eq_half_cube",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"
            ),
            "statement": """
# Erdos #1: Lean target `negativeSignedCut_card_eq_half_cube`

Switch away from the Harper-style boundary target and prove:

```lean
theorem negativeSignedCut_card_eq_half_cube
    (N : ℕ) (A : Finset ℕ) (e : Fin A.card ≃ {a // a ∈ A})
    (hA : IsSumDistinctSet A N) :
    2 * (negativeSignedCut A e).card = 2 ^ A.card := by
```

Pair each Boolean vector `u` with its complement `fun i => !(u i)`, prove the
signed sum of the complement is the negation of the signed sum of `u`, and use
the existing signed-sum facts/no-zero machinery to show exactly one endpoint of
each pair lies in `negativeSignedCut A e`.  Keep the theorem in the `2 * card`
form so the empty-cardinality case is handled cleanly.

Do not reprove the completed boundary-card upper bound, and do not attempt
Harper in this round.
""",
            "contexts": existing(
                previous_summary("erdos1-negative-signed-boundary"),
                previous_decision("erdos1-negative-signed-boundary", 7),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-b-eq-four-indepnum-le-three",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a b=4 implies independence number <= 3",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "target_theorem": "b_eq_four_connected_forces_indepNum_le_three",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a: Lean target `b_eq_four_connected_forces_indepNum_le_three`

Prove the first reduced-branch blocker:

```lean
lemma b_eq_four_connected_forces_indepNum_le_three
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hconn : G.Connected)
    (hb : b G = 4) :
    G.indepNum ≤ 3
```

Use the route from the supervisor: an independent 4-set plus any outside vertex
induces a 5-vertex bipartite subgraph, contradicting `b G = 4`; handle the
case where the independent set is all vertices using connectedness and
nontriviality.  After this, the next target should be
`diam_two_all_ecc_two_forces_delete_connected`.

Keep the Chvatal-Erdos traceability theorem parked unless it is explicitly
accepted/imported as a dependency.
""",
            "contexts": existing(
                previous_summary("wowii198a-diam-two-self-centered-b4"),
                previous_decision("wowii198a-diam-two-self-centered-b4", 5),
                "artifacts/open_problem_screening/latest/wowii198a_semantic_open_audit_and_next_directions_20260612.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-odd-cross-augmented-no-interlacing",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals crossed scalar-normal exclusion",
            "statement": """
# Crystals: proof-lab target `odd_cross_augmented_no_interlacing`

Continue proof-lab, not Lean editing.  Work only on the stated crossed
exclusion lemma with all four `3 <=` bounds.

Introduce quotient witnesses `k l` from `h1 h2`, set
`S = g*u + h*v`, `T = g*v + h*u`, and
`δ = T - S = (g-h)*(v-u) > 0`.  First verify the claimed
quotient-difference identity algebraically; if it is false, replace it with
the exact identity.  Then derive either a contradiction from parity,
positivity, and quotient bounds, or produce an actual counterexample satisfying
oddness, `h < g`, `u < v`, and all four lower bounds.

If proved, explicitly describe the lift back through the gcd crossed
decomposition to `halfShift_scalar_normal_prod_unique`; if refuted, freeze the
scalar-normal route at this lemma.
""",
            "contexts": existing(
                previous_summary("crystals-halfshift-scalar-normal-uniqueness"),
                previous_decision("crystals-halfshift-scalar-normal-uniqueness", 3),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "erdos212-rational-distance-containment-source",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-erdos-212",
            "title": "Erdos #212 source grounding for line-or-circle containment",
            "statement": """
# Erdos #212: proof-lab/source-grounding target

Do not retry completed Lean targets.  The missing blocker is:

```lean
rational_distance_subset_line_or_circle_union_finset
```

The proof-lab must either justify the exact line-or-circle-plus-finset
containment theorem for rational-distance subsets from a cited source, or
replace it with a weaker theorem-level statement that still feeds directly into
`no_dense_of_subset_line_or_circle_union_finset`.  Record any literature or web
source used in durable notes.  If no source-backed containment can be produced,
freeze this route rather than adding local Lean lemmas.
""",
            "contexts": existing(
                previous_summary("erdos-212-exists-real-not-mem-finset"),
                previous_decision("erdos-212-exists-real-not-mem-finset", 7),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
                "sources/open_candidate_screening_20260612/www.erdosproblems.com_212.html",
            ),
        },
        {
            "priority": 6,
            "slug": "graph002-source-ground-clique-cover-or-witness",
            "kind": "proof-lab",
            "problem_id": "unsolvedmath-graph-002",
            "title": "GRAPH-002 source grounding for obstruction or witness route",
            "statement": """
# GRAPH-002: proof-lab/source-grounding target

Do not continue Lean formalizer work on
`gamma_eq_eternalDominationNumber_eq_two_implies_cliqueCoverNumber_eq_two`.

Either produce a cited exact theorem statement for the obstruction
`γ(G)=γ∞(G)=2 -> θ(G)=2`, including clique-cover definitions and all
hypotheses, or abandon that obstruction route and source a concrete
witness/certificate theorem for `γ(G)=γ∞(G)<θ(G)`.  The next Lean target must
have an audit-compatible expected header before it is sent to formalization.

Record durable notes for West's eternal domination page, arXiv:2110.09732,
arXiv:1407.5235, and the finding that known 10-vertex `γ∞<θ` witnesses do not
satisfy `γ=γ∞`.
""",
            "contexts": existing(
                previous_summary("graph002-domination-le-eternal"),
                previous_decision("graph002-domination-le-eternal", 9),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Graph002.lean",
                "sources/open_candidate_screening_20260612/www.unsolvedmath.com_problems_GRAPH-002.html",
                "sources/open_candidate_screening_20260612/dwest.web.illinois.edu_regs_eterndom.html.html",
                "sources/open_candidate_screening_20260612/arxiv.org_abs_2110.09732.html",
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
        command += ["--mode", "proof-lab", "--round-time-budget", "2400"]
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
            "3000",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "420",
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


def global_lean_formalizer_count() -> int:
    try:
        output = subprocess.check_output(["ps", "-eo", "pid,cmd"], text=True)
    except Exception:
        return 0
    count = 0
    for line in output.splitlines():
        parts = line.strip().split(None, 1)
        cmd = parts[1] if len(parts) == 2 else ""
        if "run.py run-campaign-loop" not in cmd or "--mode lean-formalizer" not in cmd:
            continue
        if cmd.startswith("timeout ") or cmd.startswith("systemd-run "):
            continue
        if Path(__file__).name in cmd:
            continue
        count += 1
    return count


def pending_wowii198a_target() -> dict[str, Any]:
    for target in build_targets():
        if target["slug"] == "wowii198a-b-eq-four-indepnum-le-three":
            return {
                **target,
                "priority": 7,
                "slug": "wowii198a-b-eq-four-indepnum-le-three-deferred",
                "title": target["title"] + " deferred slot run",
            }
    raise RuntimeError("WOWII198a target not found")


def run_pending_wowii198a_watcher() -> None:
    target = prepare_target(pending_wowii198a_target())
    status_path = RUN_ROOT / "pending_wowii198a_status.json"
    status: dict[str, Any] = {
        "watcher_pid": os.getpid(),
        "started_at": utc_now(),
        "target": target["slug"],
        "state": "waiting_for_lean_slot",
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "statement_file": target["statement_file"],
        "output_root": target["output_root"],
        "log_path": target["log_path"],
    }
    while global_lean_formalizer_count() >= LEAN_SLOT_LIMIT:
        status["state"] = "waiting_for_lean_slot"
        status["global_lean_formalizer_count"] = global_lean_formalizer_count()
        write_json(status_path, status | {"updated_at": utc_now()})
        time.sleep(60)

    proc = start_process(target)
    status.update(
        {
            "state": "active",
            "pid": proc.pid,
            "launched_at": utc_now(),
            "global_lean_formalizer_count_at_launch": global_lean_formalizer_count(),
        }
    )
    write_json(status_path, status | {"updated_at": utc_now()})
    code = proc.wait()
    status.update(
        {
            "state": "completed",
            "returncode": code,
            "completed_at": utc_now(),
        }
    )
    write_json(status_path, status | {"updated_at": utc_now()})


def active_status(active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]]) -> list[dict[str, Any]]:
    return [{"slug": target["slug"], "pid": proc.pid} for target, proc in active]


def write_driver_status(status: dict[str, Any]) -> None:
    status["updated_at"] = utc_now()
    write_json(RUN_ROOT / "driver_status.json", status)


def run_driver() -> None:
    targets = [prepare_target(target) for target in build_targets()]
    proof_targets = [target for target in targets if target["kind"] == "proof-lab"]
    lean_pending = [target for target in targets if target["kind"] == "lean-formalizer"]
    active_lean: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    active_other: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "excluded_frozen": [
            "erdos-972-unbounded-count-bridge",
            "one-third-two-thirds-count-ratio",
        ],
        "pending": [target["slug"] for target in lean_pending],
        "active_lean": [],
        "active_other": [],
        "completed": completed,
    }

    for target in proof_targets:
        proc = start_process(target)
        active_other.append((target, proc))

    while lean_pending or active_lean or active_other:
        while lean_pending and global_lean_formalizer_count() < LEAN_SLOT_LIMIT:
            target = lean_pending.pop(0)
            proc = start_process(target)
            active_lean.append((target, proc))
            status["pending"] = [item["slug"] for item in lean_pending]
            status["active_lean"] = active_status(active_lean)
            status["active_other"] = active_status(active_other)
            status["global_lean_formalizer_count"] = global_lean_formalizer_count()
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

        status["active_lean"] = active_status(active_lean)
        status["active_other"] = active_status(active_other)
        status["completed"] = completed
        status["pending"] = [target["slug"] for target in lean_pending]
        status["global_lean_formalizer_count"] = global_lean_formalizer_count()
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
        "excluded_frozen": [
            "erdos-972-unbounded-count-bridge",
            "one-third-two-thirds-count-ratio",
        ],
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
                "build_command": target.get("build_command", ""),
                "context_count": len(target.get("contexts", [])),
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
    if len(sys.argv) > 1 and sys.argv[1] == "--pending-wowii198a":
        run_pending_wowii198a_watcher()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
