#!/usr/bin/env python3
"""Launch a 1h AMRA round for two original main goals plus four next targets.

Lean-heavy campaigns are capped at two concurrent slots.  The two WOWII tasks
use the source/original theorem as the final target; the remaining tasks follow
the latest controller-selected next target.
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
    / "main_original_plus_next_20260613_1h_strict_slots"
)

TIME_BUDGET_SECONDS = 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
LEAN_SLOT_LIMIT = 2
PREVIOUS = REPO / "artifacts" / "open_problem_screening" / "latest" / "next_round_slots_20260613_2h"


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
        f"{target['slug']}-1h",
        "--reasoning-effort",
        "high",
    ]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    for completed in target.get("completed", []):
        args += ["--completed-target-theorem", completed]
    return args


def build_targets() -> list[dict[str, Any]]:
    wowii16_header = """
theorem conjecture16
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (h : G.Connected) :
    letI maxL := (Finset.univ.image (fun v => indepNeighborsCard G v)).max' (by simp)
    letI r := G.radius.toNat
    2 * ((r : ℝ) - 1) + (maxL : ℝ) ≤ b G
"""
    wowii198a_header = """
theorem conjecture198a
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (h : G.Connected)
    (hb : b G ≤ 2 + averageEccentricity G) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian
"""
    return [
        {
            "priority": 1,
            "slug": "wowii198a-original-conjecture198a-main",
            "kind": "hybrid",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-conjecture198a",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "target_theorem": "conjecture198a",
            "final_target_theorem": "conjecture198a",
            "expected_header": wowii198a_header,
            "build_command": build_command("AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"),
            "completed": [
                "b_eq_four_connected_forces_indepNum_le_three",
                "diam_two_all_ecc_two_forces_delete_connected",
                "b_eq_diam_add_two_all_eccent_eq_diam_forces_diam_le_two",
                "source_bound_b_eq_diam_add_two_forces_reduced_branch",
            ],
            "statement": """
# WOWII198a original-main attack

Treat the original source theorem as the final target:

```lean
theorem conjecture198a
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (h : G.Connected)
    (hb : b G ≤ 2 + averageEccentricity G) :
    ∃ a b : alpha, ∃ p : G.Walk a b, p.IsHamiltonian
```

Do not stop at reduced-branch subgoals.  Use the verified branch split and
reduced package.  The active missing bridge is the traceability/Hamiltonian
step for the reduced branch; either import/establish a source-faithful
Chvatal-Erdos style theorem or give a specialized elementary proof.  Keep the
original theorem as the final target throughout this campaign.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii198a-b-eq-four-indepnum-le-three/wowii198a-b-eq-four-indepnum-le-three-2h-2/report.json",
                PREVIOUS / "runs/wowii198a-b-eq-four-indepnum-le-three/wowii198a-b-eq-four-indepnum-le-three-2h-2/proof_lab/round-009/report.json",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-original-conjecture16-main",
            "kind": "hybrid",
            "lean_heavy": True,
            "problem_id": "wowii-conjecture16",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"),
            "target_theorem": "conjecture16",
            "final_target_theorem": "conjecture16",
            "expected_header": wowii16_header,
            "build_command": build_command("AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"),
            "completed": [
                "conjecture16_source_bound_of_radius_gt_two_of_diam_large",
                "conjecture16_source_bound_of_radius_toNat_le_two",
            ],
            "statement": """
# WOWII16 original-main attack

Treat the original source theorem as the final target:

```lean
theorem conjecture16
    {alpha : Type*} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) (h : G.Connected) :
    letI maxL := (Finset.univ.image (fun v => indepNeighborsCard G v)).max' (by simp)
    letI r := G.radius.toNat
    2 * ((r : ℝ) - 1) + (maxL : ℝ) ≤ b G
```

Do not merely report the completed high-radius/large-diameter branch.  Use all
verified branches and identify exactly what remains to close the original
theorem.  If the existing file already contains enough branch coverage, prove
the source-faithful wrapper `conjecture16`; otherwise return to proof-lab and
isolate the missing branch lemma.
""",
            "contexts": existing(
                PREVIOUS / "runs/wowii16-radius-gt-two-diam-large/wowii16-radius-gt-two-diam-large-2h-2/report.json",
                PREVIOUS / "runs/wowii16-radius-gt-two-diam-large/wowii16-radius-gt-two-diam-large-2h-2/supervisor/round-002/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-boundary-card-le-n",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-erdos-1",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"),
            "target_theorem": "negativeSignedCut_cubeOuterBoundary_card_le_N",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"),
            "statement": """
# Erdos #1 next target

Prove the controller-selected Lean target:

```lean
theorem negativeSignedCut_cubeOuterBoundary_card_le_N
    (N : Nat) (A : Finset Nat) (e : Fin A.card ≃ {a // a ∈ A})
    (hA : IsSumDistinctSet A N) :
    (cubeOuterBoundary (negativeSignedCut A e)).card <= N
```

Use the signed-sum range/parity injection route from the last proof-lab report.
Do not revisit the false `negativeSignedCut_card_eq_half_cube` target.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos1-route-replan-after-freeze/erdos1-route-replan-after-freeze-1h/report.json",
                PREVIOUS / "runs/erdos1-route-replan-after-freeze/erdos1-route-replan-after-freeze-1h/proof_lab/round-008/report.json",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "erdos212-bombieri-lang-wrapper",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-erdos-212",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"),
            "target_theorem": "rational_distance_subset_line_or_circle_union_finset_of_bombieri_lang",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"),
            "statement": """
# Erdos #212 next target

Prove the conditional Bombieri-Lang wrapper selected by proof-lab:
`rational_distance_subset_line_or_circle_union_finset_of_bombieri_lang`,
after adding the explicit Prop `BombieriLangConsequenceForRationalDistanceSets`.
Do not retry the unsupported unconditional containment theorem.
""",
            "contexts": existing(
                PREVIOUS / "runs/erdos212-rational-distance-containment-source/erdos212-rational-distance-containment-source-2h-2/report.json",
                PREVIOUS / "runs/erdos212-rational-distance-containment-source/erdos212-rational-distance-containment-source-2h-2/proof_lab/round-015/report.json",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "crystals-gap-z-obstruction",
            "kind": "lean-formalizer",
            "lean_heavy": True,
            "problem_id": "formal-conjectures-crystals-components-unique",
            "workspace": str(FORMAL),
            "target_file": formal_file("AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"),
            "target_theorem": "odd_cross_halfShift_gap_Z_obstruction",
            "build_command": build_command("AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"),
            "statement": """
# Crystals next target

Prove or refute the current obstruction:

```lean
lemma odd_cross_halfShift_gap_Z_obstruction
    (a b h u Y : Nat)
    (ha : 1 <= a) (hb : 1 <= b)
    (hY : h * u + 1 = 2 * Y)
    (hYu : 3 <= h * u)
    (hdiv1 :
      (Y + a * u) * (Y + h * b) ∣
        (2 * Y + a * u + h * b - 1) ^ 2) :
    ¬ (Y + a * u + h * b + 2 * a * b) ∣ (Y - 1) ^ 2
```

If the statement is false, return a concrete counterexample and freeze the
route.  If true, formalize the obstruction using existing half-shift lemmas.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-odd-cross-augmented-no-interlacing/crystals-odd-cross-augmented-no-interlacing-2h-2/report.json",
                PREVIOUS / "runs/crystals-odd-cross-augmented-no-interlacing/crystals-odd-cross-augmented-no-interlacing-2h-2/proof_lab/round-005/report.json",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
            ),
        },
        {
            "priority": 6,
            "slug": "graph002-witness-certificate-search",
            "kind": "proof-lab",
            "lean_heavy": False,
            "problem_id": "unsolvedmath-graph-002",
            "statement": """
# GRAPH-002 next target

Do not continue the KM obstruction Lean route.  The latest audit says primary
KM1 theorem text is missing.  Search for or generate an audit-compatible
concrete witness/certificate route for a graph satisfying
`gamma(G) = gamma_infty(G) < theta(G)`, starting beyond the excluded 10/11
vertex witnesses from arXiv:2110.09732.  End with a concrete certificate target
or freeze this problem if no source/computational route is credible.
""",
            "contexts": existing(
                PREVIOUS / "runs/graph002-source-ground-clique-cover-or-witness/graph002-source-ground-clique-cover-or-witness-2h-2/report.json",
                PREVIOUS / "runs/graph002-source-ground-clique-cover-or-witness/graph002-source-ground-clique-cover-or-witness-2h-2/proof_lab/round-006/report.json",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Graph002.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Graph002_proof_notes.md",
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
        command += ["--mode", "proof-lab", "--round-time-budget", "1800"]
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
            "2100",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "420",
        ]
        if target.get("final_target_theorem"):
            command += ["--final-target-theorem", target["final_target_theorem"]]
        if target.get("expected_header"):
            header_path = RUN_ROOT / "headers" / f"{target['priority']:02d}-{target['slug']}.lean"
            write_text(header_path, target["expected_header"])
            command += ["--expected-target-header-file", str(header_path)]
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
    count = 0
    for line in output.splitlines():
        parts = line.strip().split(None, 1)
        cmd = parts[1] if len(parts) == 2 else ""
        if "run.py run-campaign-loop" not in cmd:
            continue
        if "--mode lean-formalizer" not in cmd and "--mode hybrid" not in cmd:
            continue
        if "timeout " in cmd or "systemd-run " in cmd:
            continue
        if Path(__file__).name in cmd:
            continue
        count += 1
    return count


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
        while (
            lean_pending
            and len(active_lean) < LEAN_SLOT_LIMIT
            and global_lean_campaign_count() < LEAN_SLOT_LIMIT
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
    for subdir in ("headers", "statements", "logs", "pids", "runs"):
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
