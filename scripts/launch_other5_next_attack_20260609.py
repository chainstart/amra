#!/usr/bin/env python3
"""Launch the next attack round for the five non-866 open targets.

This driver intentionally excludes Erdos866 because the current triage route is
frozen until the exact CES75 source fact is supplied. It also reserves one Lean
slot for the already-running IndependentDomination80 formalizer, so this batch
uses at most one additional Lean-heavy process at a time.
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
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "other5_next_attack_20260609_2h"

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


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii16-distance-two-private-choice",
            "kind": "proof-lab",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII 16 distance-two exchange/private-choice route",
            "statement": """
# WOWII 16 distance-two exchange/private-choice route

The Lean certificate `centralIntervalSharedFirstStepIndexGapLeTwo` already
checks in `Wowii16CentralCore.lean`. Do not reprove it.

Main objective for this round:

Develop the next theorem-level natural-language proof route for WOWII 16 after
the shared-first-step gap certificate. Focus on the distance-two
exchange/private-choice step: when central-interval off-base witnesses collide
or become color-incompatible, prove an augmenting exchange or isolate the exact
minimal obstruction.

Required output:

- State the exact smaller lemma that should follow the shared-first-step
  certificate.
- Separate bridge statuses as proved, plausible, false, computational, or
  source theorem.
- If not solved, identify the smallest next Lean-ready certificate target.

Frozen routes: do not redo predecessor-depth, connected domination, bare Hall
quota restatements, or the already-verified shared-first-step certificate.
""",
            "contexts": existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "artifacts/open_problem_screening/latest/wowii16_shared_first_step_lean_20260609c/runs/wowii16-shared-first-step-lean-verify/summary.md",
                "artifacts/open_problem_screening/latest/wowii16_distance_two_nl_20260609_1h/runs/wowii16-distance-two-collision-nl-1h/summary.md",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "wowii200-nontraceable-average-deficit",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture200",
            "title": "WOWII 200 nontraceable average-deficit attack",
            "statement": """
# WOWII 200 nontraceable average-deficit attack

Original target: every finite connected graph satisfying
`largestInducedTreeSize G = ceil(1 + l G)` has a Hamiltonian path.

Do not spend this round on weak restatements of the equality. Treat
`conjecture200_extremal_reduction` as certificate-side packaging. The main
mathematical target is the structural counting blocker:

```lean
theorem nontraceable_extremal_tree_average_le_short_girth
    (G : SimpleGraph alpha) (hconn : G.Connected)
    (hnontraceable : not (exists a b, exists p : G.Walk a b, p.IsHamiltonian))
    (hshort : G.girth <= 4)
    (hT : largestInducedTreeSize G =
        (Finset.univ.sup (indepNeighborsCard G)) + 1) :
    l G <= (Finset.univ.sup (indepNeighborsCard G) : Real) - 1
```

The exact header may be adjusted to AMRA's existing definitions, but do not
weaken the semantic claim. Attack the counting proof: maximum induced tree
saturation, outside-vertex attachment patterns, local-neighborhood independence
deficit, and path-extension obstruction.

Required output:

- Prove the route, find a counterexample family, or isolate a smaller counting
  lemma that materially moves this theorem.
- Keep bounded graph searches as evidence only.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/wowii-conjecture200/wowii-conjecture200-prooflab-2h/summary.md",
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/wowii-conjecture200/wowii-conjecture200-prooflab-2h/supervisor/round-009/decision.md",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LargestInducedTree.lean",
                "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/LocalGirthInducedTreeBound.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-recurrence-theta-injectivity",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystal components recurrence/theta injectivity",
            "statement": """
# Crystal components uniqueness: recurrence/theta injectivity

Original target: Abrate-Barbero-Cerruti-Murru, The Biharmonic mean,
Conjecture 4.5: an odd crystal number has a unique unordered pair of
components.

Do not continue the broad divisor-only route. This round must return to the
source paper, extract the exact recurrence/conic/theta map used to classify
crystal component pairs, and attack product injectivity for that
parameterization.

Main objective:

- Recover the exact classified pair map from the paper.
- State a recurrence-product injectivity lemma that is faithful to the source.
- Either prove/refute that lemma or identify the smallest algebraic blocker.

Bounded searches are allowed as evidence only. Do not claim Theorem 5 alone
settles uniqueness; the missing point is injectivity of the product under the
classification.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/crystals-components-unique/crystals-components-unique-prooflab-2h/summary.md",
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/crystals-components-unique/crystals-components-unique-prooflab-2h/supervisor/round-006/decision.md",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "a357513-odd-p2-inverse-power-sum",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-general-supercongruence",
            "title": "A357513 odd inverse-power p^2 vanishing",
            "workspace": str(FORMAL),
            "target_file": str(
                FORMAL
                / "AmraLibrary"
                / "OpenProblemBatches"
                / "TrueOpenNextRound20260606"
                / "04_general_supercongruence_zmod_cast.lean"
            ),
            "target_theorem": "zmod_p2_mul_inverse_power_sum_odd_eq_zero_mod_p4_of_large",
            "build_command": (
                "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "statement": """
# A357513 / general_supercongruence Lean target

Continue the Lean formalizer on OEIS A357513. The current first blocker is:

```lean
zmod_p2_mul_inverse_power_sum_odd_eq_zero_mod_p4_of_large
```

Use the previous verified bridges:

- `zmod_hypergeometric_summand_expansion_mod_p4`
- `zmod_hypergeometric_sum_expansion_mod_p4`
- the verified even `p^3` inverse-power kill lemma

Prove the odd inverse-power sum with enough `p^2` divisibility. First establish
the auxiliary odd inverse-power vanishing in `ZMod (p ^ 2)` using the pairing
`k -> p-k` and the `hlarge` inequality. Then add the lifting helper from zero
mod `p^2` to `(p : ZMod (p^4))^2 * S = 0`.

Do not reopen the already verified binomial/summand/sum expansion lemmas.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/next_round_16_80_866_a357513_20260609/runs/a357513-hypergeometric-summand-expansion/a357513-hypergeometric-summand-expansion-next-2h/summary.md",
                "artifacts/open_problem_screening/latest/next_round_16_80_866_a357513_20260609/runs/a357513-hypergeometric-summand-expansion/a357513-hypergeometric-summand-expansion-next-2h/state.json",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            ),
        },
        {
            "priority": 5,
            "slug": "wowii198a-leftmost-neighbor-certificate",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII 198a leftmost-neighbor certificate",
            "workspace": str(FORMAL),
            "target_file": str(
                FORMAL
                / "AmraLibrary"
                / "OpenProblemBatches"
                / "VerifiedOpen20260609"
                / "Wowii198aLeftmost.lean"
            ),
            "target_theorem": "path_neighbors_subset_of_leftmostEligibleEdge",
            "build_command": (
                "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/"
                "Wowii198aLeftmost.lean"
            ),
            "statement": """
# WOWII 198a Lean/certificate target

Formalize the first local certificate for the `b = diam + 1` route:

```lean
lemma path_neighbors_subset_of_leftmostEligibleEdge
    (G : SimpleGraph alpha) [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (hconn : G.Connected)
    (P : Fin (G.diam + 1) -> alpha)
    (hP : IsDiametralGeodesic G P)
    (z : alpha)
    (hzP : z notin Set.range P)
    (i : Fin G.diam)
    (hzi : LeftmostEligibleEdge G P z i)
    (j : Fin (G.diam + 1))
    (hzj : G.Adj z (P j))
    (hdel : j.val != i.val + 1) :
    j.val = i.val or j.val = i.val + 2
```

Use Lean's actual syntax and AMRA/mathlib definitions when writing the theorem.
First add minimal local definitions for `IsDiametralGeodesic` and
`LeftmostEligibleEdge`. The leftmost edge predicate must include adjacency to
both `P i` and `P (i+1)` and no smaller eligible consecutive edge. Handle
boundary cases `i = 0` and the last edge without referencing nonexistent path
vertices.

Do not work on the full Hamiltonian splicing or the `b = diam + 2` branch in
this round.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/wowii-conjecture198a/wowii-conjecture198a-prooflab-2h/summary.md",
                "artifacts/open_problem_screening/latest/verified_three_open_attack_20260609_2h_v2/runs/wowii-conjecture198a/wowii-conjecture198a-prooflab-2h/supervisor/round-009/decision.md",
                "artifacts/open_problem_screening/latest/triage_actions_20260609.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
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
        command += [
            "--mode",
            "proof-lab",
            "--round-time-budget",
            "2700",
        ]
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
        "external_lean_slot_reserved_for": "IndependentDomination80",
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
        "external_lean_slot_reserved_for": "IndependentDomination80",
        "excluded": [
            {
                "slug": "erdos866",
                "reason": "frozen until exact CES75 source fact is supplied",
            }
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
