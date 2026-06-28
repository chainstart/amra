#!/usr/bin/env python3
"""Launch the prioritized six-target next attack round for 2026-06-09.

Lean-heavy formalizer work is capped at two concurrent processes.  The first
two Lean slots go to A357513 and WOWII16; IndependentDomination80 is queued as a
lower-priority Lean follow-up if a slot frees before the 2h wall clock expires.
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
    / "priority6_next_attack_20260609_2h"
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


def nice_prefix() -> list[str]:
    command = ["timeout", f"{HARD_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def resource_prefix(*, lean: bool) -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    if lean:
        return [
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
    return [
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


def common_campaign_args(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
    args = [
        *nice_prefix(),
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
        "1200",
        "--proof-audit-timeout",
        "450",
        "--proof-grounding-timeout",
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
        f"{target['slug']}-next-2h",
        "--reasoning-effort",
        "high",
    ]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    return args


def formal_file(relative: str) -> str:
    return str(FORMAL / relative)


def build_command(relative: str) -> str:
    return f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {relative}"


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "a357513-u-bridge-and-vanishing",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-general-supercongruence",
            "title": "A357513 u bridge and p^4 vanishing",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "target_theorem": "zmod_u_eq_hypergeometric_sum_mod_p4_of_large",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "statement": """
# A357513 / general_supercongruence Lean formalizer

Primary target:

```lean
lemma zmod_u_eq_hypergeometric_sum_mod_p4_of_large
```

The theorem exists in the target file but the current build fails inside the
common-denominator support lemma `rat_term_common_den`. First repair that Lean
bridge without weakening any theorem, then verify the `u` equals
hypergeometric-sum statement. After verification, the supervisor should retarget
to:

```lean
lemma zmod_u_vanish_mod_p4_of_large
```

by combining the verified `zmod_u_eq_hypergeometric_sum_mod_p4_of_large` with
`zmod_hypergeometric_sum_vanish_mod_p4_of_large`.

Do not reopen the already verified binomial expansion, inverse-power vanishing,
or hypergeometric-sum vanishing lemmas except for local rewriting needed by the
current build failure.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/a357513-odd-p2-inverse-power-sum/a357513-odd-p2-inverse-power-sum-next-2h/summary.md",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/a357513-odd-p2-inverse-power-sum/a357513-odd-p2-inverse-power-sum-next-2h/lean_formalizer/round-005-zmod-u-eq-hypergeometric-sum-mod-p4-of-large/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-far-apart-first-steps-private",
            "kind": "lean-formalizer",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 far-apart first steps private certificate",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "target_theorem": "centralIntervalFarApartFirstStepsPrivate",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "Wowii16CentralCore.lean"
            ),
            "statement": """
# WOWII16 Lean formalizer target

Install this exact certificate in namespace `Wowii16CentralCore20260609`:

```lean
lemma centralIntervalFarApartFirstStepsPrivate
    {alpha : Type*}
    (dist : alpha -> alpha -> Nat) (Adj : alpha -> alpha -> Prop)
    (p z : Nat -> alpha) (pred : alpha -> alpha)
    (commonNeighbor_dist_le_two :
      forall x y a, Adj x a -> Adj a y -> dist x y <= 2)
    {i j : Nat}
    (hij : i <= j)
    (hGeod : dist (p i) (p j) = j - i)
    (hFirst_i : Adj (p i) (pred (z i)))
    (hFirst_j : Adj (pred (z j)) (p j))
    (hFar : 2 < j - i) :
    pred (z i) != pred (z j)
```

Use the already proved
`centralIntervalSharedFirstStepIndexGapLeTwo`; assume equality of first steps,
derive `j - i <= 2`, and contradict `hFar`. Do not run another proof-lab pass
or change the existing two verified certificates.
""",
            "contexts": existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii16-distance-two-private-choice/wowii16-distance-two-private-choice-next-2h/summary.md",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii16-distance-two-private-choice/wowii16-distance-two-private-choice-next-2h/proof_lab/round-019/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-leftmost-global-splicing",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a leftmost certificate global splicing",
            "statement": """
# WOWII198a proof-lab: global splicing from leftmost certificates

Do not redo the verified Lean certificates:

- `path_neighbors_subset_of_leftmostEligibleEdge`
- `leftmost_same_edge_fiber_pair_adjacent_of_b_eq_diam_add_one`
- `exists_leftmostEligibleEdge_of_b_eq_diam_add_one`

Next objective: derive the `b = diam + 1` Hamiltonian-path branch from these
certificates. The immediate target should be a theorem-level lemma such as:

```lean
theorem hamiltonian_path_from_leftmost_clique_fibers
```

or, if fully closed, the branch wrapper:

```lean
theorem exists_hamiltonian_path_of_b_eq_diam_add_one_leftmost_certificates
```

Use assignment of each off-path vertex to a leftmost eligible path edge, the
same-fiber clique property, and the path-neighbor restriction to construct the
Hamiltonian path or isolate the exact remaining obstruction. Do not start the
`b = diam + 2` branch in this round.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii198a-leftmost-neighbor-certificate/wowii198a-leftmost-neighbor-certificate-next-2h/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
            ),
        },
        {
            "priority": 4,
            "slug": "crystals-source-vieta-product",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals source Vieta product injectivity",
            "statement": """
# Crystal components uniqueness: source Vieta product injectivity

Current target:

```lean
theorem sourceVietaProduct_injective_nontrivial
```

Keep the source-aligned recurrence/Vieta parameter `A`, the boundary
`A_w(0)=1`, and the necessary nontriviality hypothesis `3 <= A`. Prove or
refute the repaired claim that equality of
`w * A_w(t) * (A_w(t) + 1)` forces equality of nontrivial `A` values.

Do not return to the broad divisor-only route, and do not use the unrestricted
false version that allows the `A=1` boundary collision. If the lemma fails,
return the smallest concrete certificate; otherwise state the next Lean-ready
arithmetic lemma and how it feeds `crystals_components_unique`.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/crystals-recurrence-theta-injectivity/crystals-recurrence-theta-injectivity-next-2h/summary.md",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/crystals-recurrence-theta-injectivity/crystals-recurrence-theta-injectivity-next-2h/proof_lab/round-005/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii200-separator-deficit-reselection",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII200 separator deficit route reselection",
            "statement": """
# WOWII200 proof-lab route reselection

The low-leaf Hall/capacity route is frozen. Do not continue
`extremal_short_girth_low_leaf_capacity_failure_traceable` or pointwise
multiplicity claims.

Return to the Nat structural blocker:

```lean
theorem nontraceable_extremal_tree_nat_deficit_short_girth
```

under connectedness, nontraceability, short girth, and
`largestInducedTreeSize G = (Finset.univ.sup (indepNeighborsCard G)) + 1`.

Choose a new separator / longest-path / path-cover obstruction route that
forces enough vertices with `indepNeighborsCard G v < M` to prove the Nat
deficit bound. If no canonical theorem emerges, run targeted counterexample
search for saturated nontraceable short-girth graphs failing the Nat deficit
inequality and report the smallest structural pattern.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii200-nontraceable-average-deficit/wowii200-nontraceable-average-deficit-next-2h/summary.md",
                "artifacts/open_problem_screening/latest/other5_next_attack_20260609_2h/runs/wowii200-nontraceable-average-deficit/wowii200-nontraceable-average-deficit-next-2h/proof_lab/round-006/summary.md",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LocalGirthInducedTreeBound.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
            ),
        },
        {
            "priority": 6,
            "slug": "independent-domination80-ckko-source-contract",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-independent-domination80",
            "title": "IndependentDomination80 CKKO source contract",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "IndependentDomination80.lean"
            ),
            "target_theorem": (
                "ckko_corollary13_source_indepDominationNumber_mul_maxDegree_"
                "large_no_isolated_of_two_le_maxDegree"
            ),
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "IndependentDomination80.lean"
            ),
            "statement": """
# IndependentDomination80 Lean formalizer follow-up

This is a lower-priority Lean queue item. Treat it as source-contract
formalization, not natural-language proof discovery.

Target:

```lean
theorem ckko_corollary13_source_indepDominationNumber_mul_maxDegree_large_no_isolated_of_two_le_maxDegree
```

Use the existing CKKO source theorem wrappers and no-isolated/max-degree
hypotheses. If the theorem already exists, make the file build cleanly and
promote the downstream wrappers without weakening the semantic contract.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/next_round_16_80_866_a357513_20260609/runs/independent-domination80-ckko-source-contract/independent-domination80-ckko-source-contract-next-2h/summary.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/IndependentDomination80.lean",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
            ),
        },
    ]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])

    command = [
        *resource_prefix(lean=target["kind"] == "lean-formalizer"),
        *common_campaign_args(target, statement_file, output_root),
    ]
    if target["kind"] == "proof-lab":
        command += ["--mode", "proof-lab", "--round-time-budget", "2700"]
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
            "4",
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
            time.sleep(30)

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
        "lean_slot_limit": LEAN_SLOT_LIMIT,
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
