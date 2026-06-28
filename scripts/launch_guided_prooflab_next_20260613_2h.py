#!/usr/bin/env python3
"""Launch a 2h proof-lab guided round after the strict-slot status review.

This round intentionally keeps the inner campaigns in proof-lab mode for one
long round.  The goal is to repair route selection and produce precise next
Lean targets without letting several campaigns switch into Lean simultaneously.
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
    / "guided_prooflab_next_20260613_2h"
)
PREVIOUS = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "main_original_plus_next_20260613_1h_strict_slots"
)

TIME_BUDGET_SECONDS = 2 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60


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


def command_prefix() -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        command += [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=4G",
            "-p",
            "MemorySwapMax=5G",
            "-p",
            "CPUQuota=100%",
        ]
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii198a-file-shape-traceability-route",
            "problem_id": "formal-conjectures-conjecture198a",
            "statement": """
# WOWII198a proof-lab route repair

Final theorem remains the original source theorem `conjecture198a`:

```lean
theorem conjecture198a
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (h : G.Connected)
    (hb : b G ≤ 2 + averageEccentricity G) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian
```

This run is proof-lab only.  Do not edit Lean and do not ask the formalizer to
retry the final theorem.  First diagnose the file-shape blocker in
`Wowii198aLeftmost.lean`: there are `#exit` barriers and repeated/alternative
sections, so audit-visible targets after those barriers are not available.

Produce a concrete cleanup plan:
- exactly which declarations before/after each `#exit` should be retained,
  moved, renamed, or discarded;
- the first Lean command that should pass after cleanup;
- the exact traceability bridge statement needed to close the reduced branch.

Then attack the mathematics of the bridge:

```lean
theorem two_connected_indepNum_le_three_forces_hamiltonian_walk
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha)
    (hdelete : ∀ x : alpha, ((⊤ : G.Subgraph).deleteVerts ({x} : Set alpha)).Connected)
    (hindep : G.indepNum ≤ 3) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian
```

Choose one executable route: a source-faithful Chvatal-Erdos traceability
theorem with exact Lean hypotheses, or a specialized longest-path proof.  End
with the exact next Lean target and dependencies.  Do not revisit verified
reduced-branch lemmas or the `b = diam + 1` leftmost-fiber package.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii198a-original-conjecture198a-main/wowii198a-original-conjecture198a-main-1h/report.json",
                PREVIOUS / "runs/wowii198a-original-conjecture198a-main/wowii198a-original-conjecture198a-main-1h/summary.md",
                PREVIOUS / "runs/wowii198a-original-conjecture198a-main/wowii198a-original-conjecture198a-main-1h/rounds/round_004/global_assessment.md",
                PREVIOUS / "runs/wowii198a-original-conjecture198a-main/wowii198a-original-conjecture198a-main-1h/supervisor/round-004/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-fixed-color-dichotomy-route",
            "problem_id": "wowii-conjecture16",
            "statement": """
# WOWII16 fixed-color dichotomy route

Final theorem remains the original source theorem `conjecture16`.  Do not retry
the final wrapper, the completed `r ≤ 2` branch, or the completed large-diameter
branch.

Current missing branch:

```lean
theorem conjecture16_source_bound_of_radius_gt_two_of_diam_small
```

The previous supervisor narrowed the real blocker to a fixed-color maximal
induced-bipartite extension dichotomy.  Work only on that theorem-level route:
produce a precise sourced proof or a smaller replacement lemma saying that a
cardinality-maximal fixed-color induced bipartite extension containing a maximum
independent neighborhood either has at least

```lean
SimpleGraph.maxIndepNeighborsCard G + 2 * (G.radius.toNat - 1)
```

vertices, or forces

```lean
G.radius.toNat ≤ 2 ∨ (2 * G.radius.toNat : Nat) ≤ G.diam + 1
```

End with one exact Lean target and the proof skeleton needed to derive
`conjecture16_source_bound_of_radius_gt_two_of_diam_small_of_max_star_extension`,
then `conjecture16_from_radius_gt_two_diam_small_branch`, then the source
wrapper `conjecture16`.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii16-original-conjecture16-main/wowii16-original-conjecture16-main-1h/report.json",
                PREVIOUS / "runs/wowii16-original-conjecture16-main/wowii16-original-conjecture16-main-1h/summary.md",
                PREVIOUS / "runs/wowii16-original-conjecture16-main/wowii16-original-conjecture16-main-1h/rounds/round_004/global_assessment.md",
                PREVIOUS / "runs/wowii16-original-conjecture16-main/wowii16-original-conjecture16-main-1h/supervisor/round-005/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-common-m-interlaced-obstruction",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "statement": """
# Crystals common-M interlaced obstruction

This run is proof-lab/computational route discovery, not Lean editing.

Current target:

```lean
halfShift_common_M_interlaced_Z_obstruction
```

Work from the abstract variables `A B Y Z` and the common-M identity
`M = 2*A*B - (A+B-1)` together with:
- `A*B ∣ M^2`;
- `Z ∣ M^2`;
- `Nat.Coprime A B`;
- the interlacing inequalities;
- `(2*A-1)*(2*B-1) = (2*Y-1)*(2*Z-1)`.

Try to prove a contradiction by bounds or valuations.  If a counterexample is
possible, produce a concrete `(A,B,Y,Z)` and explain how it lifts or does not
lift to the original `a b h u Y` variables.  End with one small Lean target or
a freeze recommendation.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-gap-z-obstruction/crystals-gap-z-obstruction-1h/report.json",
                PREVIOUS / "runs/crystals-gap-z-obstruction/crystals-gap-z-obstruction-1h/summary.md",
                PREVIOUS / "runs/crystals-gap-z-obstruction/crystals-gap-z-obstruction-1h/supervisor/round-003/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
            ),
        },
        {
            "priority": 4,
            "slug": "erdos1-harper-downstream-target",
            "problem_id": "erdos-problem-1",
            "statement": """
# Erdos #1 downstream Harper target selection

The previous Lean target `negativeSignedCut_cubeOuterBoundary_card_le_N` is
verified.  Do not redo it.

Find the next theorem-level step toward the original Erdos #1 statement.  Start
from the verified boundary theorem and the existing local definitions:
`cubeOuterBoundary`, `setFamilyOuterBoundary`,
`setFamilyClosedNeighborhood_half_cube_ge_central_of_outer`, and
`supportFamily_cubeOuterBoundary`.

Decide whether the next Lean target should be the supervisor-suggested
`setFamilyOuterBoundary_card_ge_central_of_card_half`, or a smaller closed
neighborhood Harper/isoperimetric lemma already aligned with the current file.
End with the exact Lean statement and a dependency plan.  Do not start a broad
unconditional proof of Erdos #1 in this run.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos1-boundary-card-le-n/erdos1-boundary-card-le-n-1h/report.json",
                PREVIOUS / "runs/erdos1-boundary-card-le-n/erdos1-boundary-card-le-n-1h/summary.md",
                PREVIOUS / "runs/erdos1-boundary-card-le-n/erdos1-boundary-card-le-n-1h/supervisor/round-002/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "erdos212-real-plane-endpoint-route",
            "problem_id": "erdos-problem-212",
            "statement": """
# Erdos #212 real-plane endpoint route

The conditional Complex-plane wrappers are verified:
- `rational_distance_subset_line_or_circle_union_finset_of_bombieri_lang`;
- `no_dense_of_pairwise_rational_distances_of_bombieri_lang`.

Do not redo those wrappers and do not attack an unconditional Bombieri-Lang
replacement.  Decide whether the next useful formal step is a `ℝ²` /
`EuclideanSpace Real (Fin 2)` transport layer, or whether the current Complex
formalization is already source-faithful enough for the conditional endpoint.

End with one exact Lean target, likely a transport theorem such as
`PairwiseRationalDistancesEuclideanPlane` plus a homeomorphism/isometry bridge
to the existing Complex statement, or recommend freezing until the original
source statement is fixed more precisely.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos212-bombieri-lang-wrapper/erdos212-bombieri-lang-wrapper-1h/report.json",
                PREVIOUS / "runs/erdos212-bombieri-lang-wrapper/erdos212-bombieri-lang-wrapper-1h/summary.md",
                PREVIOUS / "runs/erdos212-bombieri-lang-wrapper/erdos212-bombieri-lang-wrapper-1h/supervisor/round-004/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
            ),
        },
    ]


def command_for(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
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
        "proof-lab",
        "--rounds",
        "1",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        "6600",
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
    return args


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])
    return {
        **target,
        "statement_file": str(statement_file),
        "output_root": str(output_root),
        "log_path": str(log_path),
        "command": command_for(target, statement_file, output_root),
    }


def start_process(target: dict[str, Any]) -> subprocess.Popen[bytes]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
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


def run_driver() -> None:
    targets = [prepare_target(target) for target in build_targets()]
    active = [(target, start_process(target)) for target in targets]
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "mode": "proof-lab-only-one-round",
        "active": active_status(active),
        "completed": completed,
        "frozen": ["graph002-witness-certificate-search"],
    }
    write_json(RUN_ROOT / "driver_status.json", status)
    while active:
        still_active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
        for target, proc in active:
            code = proc.poll()
            if code is None:
                still_active.append((target, proc))
                continue
            completed.append(
                {
                    "slug": target["slug"],
                    "pid": proc.pid,
                    "returncode": code,
                    "completed_at": utc_now(),
                    "log_path": target["log_path"],
                    "output_root": target["output_root"],
                }
            )
        active = still_active
        status["active"] = active_status(active)
        status["completed"] = completed
        write_json(RUN_ROOT / "driver_status.json", status)
        if active:
            time.sleep(20)
    status["finished_at"] = utc_now()
    write_json(RUN_ROOT / "driver_status.json", status)


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "mode": "proof-lab-only-one-round",
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "context_count": len(target.get("contexts", [])),
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
