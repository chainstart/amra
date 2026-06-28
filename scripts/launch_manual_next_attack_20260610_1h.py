#!/usr/bin/env python3
"""Launch the 2026-06-10 one-hour manual-followup attack round.

This round follows the manual intervention report from 2026-06-09.  It starts
two Lean-heavy tracks at most and keeps the other targets in proof-lab/source
analysis mode.
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
    / "manual_next_attack_20260610_1h"
)

TIME_BUDGET_SECONDS = 60 * 60
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


def command_prefix(*, lean: bool) -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        if lean:
            command += [
                "systemd-run",
                "--user",
                "--scope",
                "-p",
                "MemoryMax=8G",
                "-p",
                "MemorySwapMax=10G",
                "-p",
                "CPUQuota=120%",
            ]
        else:
            command += [
                "systemd-run",
                "--user",
                "--scope",
                "-p",
                "MemoryMax=5G",
                "-p",
                "MemorySwapMax=7G",
                "-p",
                "CPUQuota=120%",
            ]
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def formal_file(relative: str) -> str:
    return str(FORMAL / relative)


def build_command(relative: str) -> str:
    return f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {relative}"


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
        "450",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "450",
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
    return args


def build_targets() -> list[dict[str, Any]]:
    manual_report = (
        "artifacts/open_problem_screening/latest/priority6_next_attack_20260609_2h/"
        "manual_intervention_20260609.md"
    )
    return [
        {
            "priority": 1,
            "slug": "a357513-source-general-supercongruence-bridge",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-general-supercongruence",
            "title": "A357513 source-facing general_supercongruence bridge",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "target_theorem": "general_supercongruence_source_statement",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "statement": """
# A357513 source-facing bridge

The local theorem is already Lean-verified:

```lean
theorem general_supercongruence_eventual
    (m : ℕ) :
    ∃ exceptions : Finset ℕ, ∀ p, p.Prime →
      p ∉ exceptions →
      ((OeisA357513.u m (p - 1) : ℕ) : ZMod (p ^ 4)) = 0
```

Do not redo the hypergeometric or denominator proof.  The next objective is to
add a source-facing wrapper in the same local namespace, with a theorem name
such as:

```lean
theorem general_supercongruence_source_statement
    (m : ℕ) : ∃ exceptions : Finset ℕ, ∀ p, p.Prime →
      p ∉ exceptions → OeisA357513.u m (p - 1) = (0 : ZMod (p ^ 4))
```

If this exact statement is syntactically impossible because of coercion
direction, use the closest source-faithful theorem and explain the coercion
equivalence in the report.  Build the file cleanly and keep the existing
`general_supercongruence_eventual` theorem intact.
""",
            "contexts": existing(
                manual_report,
                "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii198a-hamiltonian-splicing-from-leftmost-fibers",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a Hamiltonian splicing from leftmost clique fibers",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "hamiltonian_path_from_leftmost_clique_fibers",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII198a Hamiltonian splicing from leftmost clique fibers

Already verified and not to be redone:

- `path_neighbors_subset_of_leftmostEligibleEdge`
- `leftmost_same_edge_fiber_pair_adjacent_of_b_eq_diam_add_one`
- `exists_leftmostEligibleEdge_of_b_eq_diam_add_one`
- `exists_leftmost_edge_assignment_with_clique_fibers_of_b_eq_diam_add_one`

Main target:

```lean
theorem hamiltonian_path_from_leftmost_clique_fibers
```

or a smaller Lean-ready theorem that genuinely constructs the spliced order
needed for the `b = diam + 1` Hamiltonian-path branch.  Use the assignment of
off-path vertices to path edges, same-fiber clique property, and path-neighbor
restriction.  Do not start the `b = diam + 2` branch.

If full Hamiltonian walk construction is too broad, isolate the first exact
Lean obstruction, preferably an ordered-list/splice lemma over the path edge
fibers.
""",
            "contexts": existing(
                manual_report,
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "artifacts/open_problem_screening/latest/priority6_next_attack_20260609_2h/runs/wowii198a-leftmost-global-splicing/wowii198a-leftmost-global-splicing-next-2h/proof_lab/round-009/summary.md",
            ),
        },
        {
            "priority": 3,
            "slug": "wowii16-central-interval-extension",
            "kind": "proof-lab",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 central interval extension after first-step privacy",
            "statement": """
# WOWII16 central interval extension

The local first-step privacy package is Lean-verified:

- `centralIntervalFarApartFirstStepsPrivate`
- `centralIntervalSpacedIndexFirstStepInjective`
- `centralIntervalSpacedIndexFirstStepCardLeContainer`

Do not rediscover those lemmas.  This proof-lab round should return to the
larger central-interval extension for WOWII 16.  Identify the next theorem-level
lemma that uses the card bound to extend from spaced central indices to the
full interval/radius contribution in the original conjecture.

End with one concrete target: either a Lean-ready local theorem or a precise
reason the current abstraction is missing graph/color data.
""",
            "contexts": existing(
                manual_report,
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii16-distance-two-private-choice/wowii16-distance-two-private-choice-next-2h/summary.md",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-fixedM-harmonic-factor-sum-unique",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals fixed-M harmonic factor-pair sum uniqueness",
            "statement": """
# Crystal components: fixed-M harmonic factor-pair uniqueness

Do not return to the broad divisor-only route.  Current first blocker:

```lean
theorem fixedM_sourceHarmonicFactorPair_sum_unique
    (M a b c d L1 L2 w1 w2 : ℕ)
    (ha : 2 ≤ a) (hb : 2 ≤ b)
    (hc : 2 ≤ c) (hd : 2 ≤ d)
    (hL1 : 3 ≤ L1) (hL2 : 3 ≤ L2)
    (hw1 : 3 ≤ w1) (hw2 : 3 ≤ w2)
    (hM1 : a * b + 1 = M)
    (hM2 : c * d + 1 = M)
    (hS1 : M = L1 * (a + b))
    (hS2 : M = L2 * (c + d))
    (hwS1 : a + b = w1 * (L1 + 1))
    (hwS2 : c + d = w2 * (L2 + 1)) :
    a + b = c + d
```

Manual computation found no counterexample for `a,b,c,d <= 5000` and no
rectangle/Vieta counterexample for `L <= 20000`.  This round should either
produce a proof route for the lemma, or find a counterexample with the exact
certificate.  If proved, state the next Lean target and how it closes
`fixedM_vietaDiscriminantCandidate_unique_nontrivial`.
""",
            "contexts": existing(
                manual_report,
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "artifacts/open_problem_screening/latest/priority6_next_attack_20260609_2h/runs/crystals-source-vieta-product/crystals-source-vieta-product-next-2h/proof_lab/round-004/summary.md",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/crystals-recurrence-theta-injectivity/crystals-recurrence-theta-injectivity-next-2h/summary.md",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-finite-structural-certificate-search",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 finite structural certificate search",
            "statement": """
# WOWII200 finite structural certificate search

Freeze the separator-excess route and do not restart low-leaf Hall/capacity or
pointwise multiplicity claims.  The task is not Lean formalization yet.

Run targeted finite structural search for connected nontraceable short-girth
graphs satisfying:

- `largestInducedTreeSize G = M + 1`, where `M = Finset.univ.sup (indepNeighborsCard G)`
- path-1-tough condition `∀ S, numComponentsAfterDelete G S ≤ S.card + 1`

For each example, compute `λ(v) = indepNeighborsCard G v`, deficits
`M - λ(v)`, cut vertices, block tree, longest nonspanning paths, Pósa endpoint
sets, boundaries, outside attachments, and minimal subsets whose deficit sum
reaches `|V|`.

Promote a Lean target only if the search reveals a recurring explicit
certificate with named finite sets and a checkable deficit inequality.  If no
recurring certificate appears, report the smallest pattern and freeze the Pósa
route too.
""",
            "contexts": existing(
                manual_report,
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LocalGirthInducedTreeBound.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
                "artifacts/open_problem_screening/latest/priority6_next_attack_20260609_2h/runs/wowii200-separator-deficit-reselection/wowii200-separator-deficit-reselection-next-2h/proof_lab/round-004/summary.md",
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
            "2700",
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
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
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
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "pending": [target["slug"] for target in lean_pending],
        "active_lean": [],
        "active_other": [],
        "completed": completed,
    }

    for target in proof_targets:
        proc = start_process(target)
        active_other.append((target, proc))
        status["active_other"].append({"slug": target["slug"], "pid": proc.pid, "started_at": utc_now()})
    write_driver_status(status)

    while lean_pending or active_lean or active_other:
        while len(active_lean) < LEAN_SLOT_LIMIT and lean_pending:
            target = lean_pending.pop(0)
            proc = start_process(target)
            active_lean.append((target, proc))
            status["active_lean"].append({"slug": target["slug"], "pid": proc.pid, "started_at": utc_now()})
            status["pending"] = [item["slug"] for item in lean_pending]
            write_driver_status(status)

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

        status["active_lean"] = [
            {"slug": target["slug"], "pid": proc.pid, "started_at": "running"}
            for target, proc in active_lean
        ]
        status["active_other"] = [
            {"slug": target["slug"], "pid": proc.pid, "started_at": "running"}
            for target, proc in active_other
        ]
        status["completed"] = completed
        status["pending"] = [target["slug"] for target in lean_pending]
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
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "manual_report": str(
            REPO
            / "artifacts/open_problem_screening/latest/priority6_next_attack_20260609_2h/"
            / "manual_intervention_20260609.md"
        ),
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
