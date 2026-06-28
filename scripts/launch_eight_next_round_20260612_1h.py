#!/usr/bin/env python3
"""Launch a 1h next-round attack for eight current AMRA targets.

Five new candidates are sent to Lean formalizer on small theorem-level targets.
WOWII198a and Crystals return to proof-lab because their blockers are still
mathematical, not Lean syntax.  WOWII16 is not reopened on the completed
radius-two branch; it receives a source-level retarget/freeze review.
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
    / "eight_next_round_20260612_1h"
)

TIME_BUDGET_SECONDS = 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
LEAN_SLOT_LIMIT = 2

NEW_ROUND = (
    "artifacts/open_problem_screening/latest/"
    "new_candidate_nl_attack_20260612_2h"
)
OLD_ROUND = (
    "artifacts/open_problem_screening/latest/"
    "wowii198a_16_crystals_20260612_2h"
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
        f"{target['slug']}-1h",
        "--reasoning-effort",
        "high",
    ]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    return args


def new_summary(slug: str) -> str:
    return f"{NEW_ROUND}/runs/{slug}/{slug}-prooflab-2h/summary.md"


def new_decision(slug: str, round_no: int) -> str:
    return f"{NEW_ROUND}/runs/{slug}/{slug}-prooflab-2h/supervisor/round-{round_no:03d}/decision.md"


def old_summary(slug: str) -> str:
    return f"{OLD_ROUND}/runs/{slug}/{slug}-1h/summary.md"


def old_decision(slug: str, round_no: int) -> str:
    return f"{OLD_ROUND}/runs/{slug}/{slug}-1h/supervisor/round-{round_no:03d}/decision.md"


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "erdos-212-exists-real-not-mem-finset",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-erdos-212",
            "title": "Erdos #212 finite-set escape lemma",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"
            ),
            "target_theorem": "exists_real_not_mem_finset",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean"
            ),
            "statement": """
# Erdos #212: Lean target `exists_real_not_mem_finset`

This is a small Lean formalizer round, not another proof-lab route search.

Target theorem:

```lean
theorem exists_real_not_mem_finset (S : Finset Real) :
    exists x : Real, x notin S
```

Use either the `S.exists_notMem`/`Infinite Real` route or the explicit
`Finset.max'` route from the supervisor notes.  After this verifies, the next
mathematical target is `not_dense_line_or_circle_union_finset`.
""",
            "contexts": existing(
                new_summary("erdos-212-dense-rational-distance-set"),
                new_decision("erdos-212-dense-rational-distance-set", 19),
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "erdos-972-unbounded-count-bridge",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-erdos-972",
            "title": "Erdos #972 conditional unbounded-count bridge",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos972.lean"
            ),
            "target_theorem": "beatty_prime_pair_count_unbounded_of_eventual_lower_bound",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos972.lean"
            ),
            "statement": """
# Erdos #972: conditional count bridge

This is a small Lean formalizer round.  Do not attack the open analytic theorem.

Target theorem shape:

```lean
theorem beatty_prime_pair_count_unbounded_of_eventual_lower_bound
    (C actualCount : Nat -> Nat)
    (hC_unbounded_atTop : forall N X0 : Nat, exists X : Nat, X0 <= X and N <= C X)
    (hLower : forallᶠ X in Filter.atTop, C X <= actualCount X) :
    forall N : Nat, exists X : Nat, N <= actualCount X
```

Unfold the eventual lower bound to a threshold, choose `X` using
`hC_unbounded_atTop N X0`, then close by transitivity.  Do not use the weaker
plain unboundedness hypothesis.
""",
            "contexts": existing(
                new_summary("erdos-972-beatty-prime-pairs"),
                new_decision("erdos-972-beatty-prime-pairs", 15),
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/972.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "one-third-two-thirds-count-ratio",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-1-3-2-3",
            "title": "1/3-2/3 rational count-ratio lemma",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/OneThirdTwoThirds.lean"
            ),
            "target_theorem": "oneThird_twoThirds_count_ratio_Icc",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/OneThirdTwoThirds.lean"
            ),
            "statement": """
# 1/3-2/3: rational count-ratio lemma

This is a small Lean formalizer round.  Do not touch posets or the final
conjecture in this run.

Target theorem:

```lean
theorem oneThird_twoThirds_count_ratio_Icc
    (A T : Nat)
    (hT : 0 < T)
    (hLower : T <= 3 * A)
    (hUpper : 3 * A <= 2 * T) :
    ((A : Rat) / (T : Rat)) in Set.Icc (1 / 3 : Rat) (2 / 3 : Rat)
```

Cast the natural inequalities to `Rat`, use the positive denominator, and close
the two endpoint inequalities with `field_simp` plus linear arithmetic.  After
this verifies, return to `oneThird_twoThirds_certificate_sound`.
""",
            "contexts": existing(
                new_summary("one-third-two-thirds-posets"),
                new_decision("one-third-two-thirds-posets", 23),
                "data/research_open/raw/formal_conjectures/FormalConjectures/Wikipedia/conjecture_1_3_to_2_3.lean",
            ),
        },
        {
            "priority": 4,
            "slug": "graph002-domination-le-eternal",
            "kind": "lean-formalizer",
            "problem_id": "unsolvedmath-graph-002",
            "title": "GRAPH-002 domination <= eternal domination interface",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Graph002.lean"
            ),
            "target_theorem": "dominationNumber_le_eternalDominationNumber",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Graph002.lean"
            ),
            "statement": """
# GRAPH-002: `dominationNumber_le_eternalDominationNumber`

This is a Lean formalizer round for the first certificate-interface lemma.

Add only the minimal definitions needed:

- finite family of guard-state finsets;
- every state has cardinality `k`;
- every state is dominating;
- enough feasibility/nonemptiness to define an eternal domination witness.

Target theorem:

```lean
theorem dominationNumber_le_eternalDominationNumber
```

The theorem should express that extracting one dominating state from an eternal
feasible family gives domination number at most eternal domination number.
Do not add clique-cover machinery, `Graph002Cert`, or graph search in this
round.
""",
            "contexts": existing(
                new_summary("graph-002-eternal-domination"),
                new_decision("graph-002-eternal-domination", 16),
                "sources/open_candidate_screening_20260612/www.unsolvedmath.com_problems_GRAPH-002.html",
                "sources/open_candidate_screening_20260612/dwest.web.illinois.edu_regs_eterndom.html.html",
            ),
        },
        {
            "priority": 5,
            "slug": "erdos1-negative-signed-boundary",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-erdos-1",
            "title": "Erdos #1 negative signed-sum boundary lemma",
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"
            ),
            "target_theorem": "negative_signed_sum_outer_boundary_card_le",
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1.lean"
            ),
            "statement": """
# Erdos #1: negative signed-sum outer boundary lemma

This is a Lean formalizer round on the boundary lemma selected by proof-lab.
Do not attempt the full `Erdos1.erdos_1` theorem.

Target theorem name:

```lean
negative_signed_sum_outer_boundary_card_le
```

Use the proof-lab statement with an enumeration
`e : Fin A.card equivalence {a // a in A}`, local signed sum `L`, and
`F = Finset.univ.filter fun u => L u < 0`.  Helper order:

1. `L u = 2 * positiveSubsetSum u - totalSum`;
2. injectivity of `L` from distinct subset sums;
3. no zero signed values;
4. boundary flip orientation;
5. boundary values lie in `0 < L v` and `L v < 2 * N`;
6. fixed parity;
7. inject boundary into one parity class of integers of size at most `N`.

If the complete lemma is too large for one hour, produce the first verified
helper with the same final theorem contract.
""",
            "contexts": existing(
                new_summary("erdos-1-distinct-subset-sums"),
                new_decision("erdos-1-distinct-subset-sums", 15),
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
            ),
        },
        {
            "priority": 6,
            "slug": "wowii198a-diam-two-self-centered-b4",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-conjecture198a",
            "title": "WOWII198a reduced diam-two self-centered b=4 bridge",
            "statement": """
# WOWII198a: reduced `b = diam + 2` branch

This is proof-lab, not Lean formalizer.  Repeated Lean rounds have not closed
the branch theorem.

Target theorem:

```lean
diam_two_self_centered_b_eq_four_forces_hamiltonian
```

Focus only on the reduced branch: connected finite nontrivial graph,
`G.diam = 2`, all eccentricities are `2`, and `b G = 4`, implies a Hamiltonian
walk/path.  First derive this hypothesis package from the already verified
source-branch lemmas; then either give a constructive Hamiltonian-path proof
skeleton suitable for Lean, or return a concrete counterexample/extra missing
hypothesis.

Do not send another Lean round for
`source_bound_b_eq_diam_add_two_forces_hamiltonian` until this bridge has a
real proof plan.
""",
            "contexts": existing(
                old_summary("wowii198a-source-exact-final-theorem"),
                old_decision("wowii198a-source-exact-final-theorem", 5),
                "artifacts/open_problem_screening/latest/wowii198a_semantic_open_audit_and_next_directions_20260612.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
            ),
        },
        {
            "priority": 7,
            "slug": "crystals-halfshift-scalar-normal-uniqueness",
            "kind": "proof-lab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "title": "Crystals half-shift scalar-normal uniqueness",
            "statement": """
# Crystals: scalar-normal uniqueness blocker

This is proof-lab, not Lean formalizer.  The original requested bridge
`isCrystalWithComponents_halfShift_admissible` is already verified.  The new
blocker is mathematical uniqueness, not a Lean syntax issue.

Produce a complete derivation, or a precise obstruction, for:

from same shifted product
`(2*r-1)*(2*s-1) = (2*x-1)*(2*y-1)` and divisibility hypotheses
`r*s | (r+s-1)^2`, `x*y | (x+y-1)^2`, prove equality of shifted sums or
equality-or-swap of shifted factors.

Name the exact normalized variables, the divisibility transfers, and the final
cancellation step.  If this cannot be proved, report the precise obstruction in
`halfShift_scalar_normal_prod_unique` and do not propose more build-clean
support lemmas.
""",
            "contexts": existing(
                old_decision("crystals-halfshift-admissible-bridge", 6),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
            ),
        },
        {
            "priority": 8,
            "slug": "wowii16-freeze-radius-two-and-retarget",
            "kind": "proof-lab",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII16 freeze completed radius-two branch and retarget",
            "statement": """
# WOWII16: freeze radius-two branch and retarget

This is an outer proof-lab/supervisor task.  Do not reopen the completed
radius-at-most-two branch.

Known status:

`conjecture16_source_bound_of_radius_toNat_le_two` is verified and the
supervisor decision is `freeze_route`.

This round should select the next genuine theorem-level target for WOWII16
outside the completed radius-two branch, or explicitly recommend no further
resource allocation if no source-facing target is ready.  Do not reselect the
radius-two theorem or its support lemmas, and do not reopen the old
central-interval route unless a new theorem-level statement is provided.
""",
            "contexts": existing(
                old_summary("wowii16-radius-two-source-bound"),
                old_decision("wowii16-radius-two-source-bound", 23),
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
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
            "2400",
            "--formalizer-attempts",
            "2",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "360",
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
        if "run.py run-campaign-loop" in line and "--mode lean-formalizer" in line:
            if str(Path(__file__).name) in line:
                continue
            count += 1
    return count


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
        "lean_slot_limit_global": LEAN_SLOT_LIMIT,
        "pending": [target["slug"] for target in lean_pending],
        "active_lean": [],
        "active_other": [],
        "completed": completed,
    }

    for target in proof_targets:
        proc = start_process(target)
        active_other.append((target, proc))
    write_driver_status(status)

    while lean_pending or active_lean or active_other:
        while lean_pending and global_lean_formalizer_count() < LEAN_SLOT_LIMIT:
            target = lean_pending.pop(0)
            proc = start_process(target)
            active_lean.append((target, proc))
            write_driver_status(status)
            time.sleep(3)

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
