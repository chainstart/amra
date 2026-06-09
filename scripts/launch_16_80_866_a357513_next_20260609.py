#!/usr/bin/env python3
"""Launch the corrected next round for 16, 80, 866, and A357513.

This launcher runs the WOWII 16 central-interval extension as proof-lab after
the local core Lean certificate, and queues the Lean-heavy targets with at most
two concurrent Lean formalizer campaigns.
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
ERDOS866_FORMAL = REPO / "projects" / "erdos-866-ai-continuation-20260505" / "formal"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "next_round_16_80_866_a357513_20260609"

TIME_BUDGET_SECONDS = 2 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 600
LEAN_SLOT_LIMIT = 2


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
            "MemoryMax=12G",
            "-p",
            "MemorySwapMax=14G",
            "-p",
            "CPUQuota=160%",
        ]
    return [
        "systemd-run",
        "--user",
        "--scope",
        "-p",
        "MemoryMax=6G",
        "-p",
        "MemorySwapMax=8G",
        "-p",
        "CPUQuota=130%",
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
            "slug": "wowii16-central-interval-extension-after-core",
            "kind": "proof-lab",
            "problem_id": "wowii-conjecture16",
            "title": "WOWII 16 central-interval extension after core certificate",
            "statement": """
# WOWII 16 central-interval extension after Lean core certificate

The local prerequisite `centralIntervalDeepPredOffBaseCore` has been added and
compiled in:

`AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean`

Do not rerun proof-lab on that elementary predecessor/depth lemma.

Main objective for this round:

Develop the next natural-language theorem-level route for the general
central-interval extension in WOWII Conjecture 16:

```text
Let P=p_0,...,p_e be a longest v-geodesic, r=rad(G),
delta=2*r-2-e>0, and I={e-r+1,...,r-2}.
Using off-base radius witnesses from the central interval, extract at least
delta off-base vertices compatible with the base two-coloring X0,Y0; or prove
a fixed-color augmenting exchange whenever compatibility fails.
```

Required output:

- A smaller theorem-level statement that genuinely advances the central-interval
  extension beyond `centralIntervalDeepPredOffBaseCore`.
- A proof sketch or exact fatal gap for that statement.
- If the result is Lean-ready, give the exact Lean header and dependencies.

Frozen routes:

- Do not reprove `centralIntervalDeepPredOffBaseCore`.
- Do not return to connected-domination bridges, inclusion-maximality alone,
  predecessor dichotomy, Hall/quota restatements without a new invariant, or
  `centralIntervalDeltaTwoAvailIndependentPair`.
""",
            "contexts": existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/wowii-conjecture16-central-interval/wowii-conjecture16-central-interval-supervised-4h/summary.md",
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/wowii-conjecture16-central-interval/wowii-conjecture16-central-interval-supervised-4h/supervisor/round-038/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            ),
        },
        {
            "priority": 2,
            "slug": "a357513-hypergeometric-summand-expansion",
            "kind": "lean-formalizer",
            "problem_id": "formal-conjectures-general-supercongruence",
            "title": "A357513 general_supercongruence hypergeometric summand expansion",
            "workspace": str(FORMAL),
            "target_file": str(
                FORMAL
                / "AmraLibrary"
                / "OpenProblemBatches"
                / "TrueOpenNextRound20260606"
                / "04_general_supercongruence_zmod_cast.lean"
            ),
            "target_theorem": "zmod_hypergeometric_summand_expansion_mod_p4",
            "build_command": (
                "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/"
                "04_general_supercongruence_zmod_cast.lean"
            ),
            "statement": """
# A357513 / general_supercongruence Lean next target

The original open theorem is `OeisA357513.general_supercongruence`; the numeric
short name is OEIS `A357513`.

Do not attack the original theorem directly. Use the verified binomial bridges
in `OeisA357513NextRound20260606` and prove the next summand-level bridge:

```lean
lemma zmod_hypergeometric_summand_expansion_mod_p4
    (p k m : ℕ) (hp : p.Prime) (hk1 : 1 ≤ k) (hkp : k ≤ p - 1) :
    let R := ZMod (p ^ 4)
    ((((p - 1).choose k : R) ^ 2) *
      (((p - 1 + k).choose k : R) ^ 2) *
      (((k : R) ^ (2 * m + 1))⁻¹)) =
      (p : R) ^ 2 * (((k : R) ^ (2 * m + 3))⁻¹) -
        (2 : R) * (p : R) ^ 3 * (((k : R) ^ (2 * m + 4))⁻¹)
```

Use:

- `zmod_p_minus_one_choose_factor_expansion_mod_p4`
- `zmod_p_minus_one_add_choose_factor_expansion_mod_p4`
- `square_zero_mul_prod_one_add_sq`
- denominator unit facts already in the target file

The intended algebra is: combine the lower and upper binomial expansions,
collapse the paired factors modulo `p^4`, and keep only the `p^2` and `p^3`
terms of `(1 - p/k)^2`. This theorem must remain aligned with the summand of
`u m (p - 1)`.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/true_open_main_proposition_push_20260608_2h/runs/general-upper-binomial-export/general-upper-binomial-export-2h/summary.md",
                "artifacts/open_problem_screening/latest/true_open_main_direction_20260608_2h/manifest.json",
                "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            ),
        },
        {
            "priority": 3,
            "slug": "erdos866-g6-sqrt-upper-wrapper",
            "kind": "lean-formalizer",
            "problem_id": "erdos866",
            "title": "Erdos 866 gFun 6 sqrt upper wrapper",
            "workspace": str(ERDOS866_FORMAL),
            "target_file": str(ERDOS866_FORMAL / "MathProject" / "MainClaim.lean"),
            "target_theorem": "erdos866_g6_sqrt_upper",
            "build_command": "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean MathProject/MainClaim.lean",
            "statement": """
# Erdos 866 Lean wrapper target

This is a formalization-completion task, not natural-language discovery.

Add only the official wrapper:

```lean
theorem erdos866_g6_sqrt_upper :
    ∃ C : ℝ, 0 < C ∧ ∃ N0 : ℕ, ∀ n : ℕ, N0 ≤ n →
      (gFun 6 n : ℝ) ≤ C * Real.sqrt (n : ℝ)
```

The expected proof is:

```lean
exact
  (ces75_theorem4_integer_six_witness_upper_source_iff_g6upper_sqrt_bound).mp
    ces75_theorem4_integer_six_witness_upper_source_fact
```

Do not reopen Sidon lower construction, dyadic transfer, `generalupper`,
positive-witness variants, g5/h5 assets, or existing CES75 bridge/source lemmas.
If the names are not in scope or the source bridge is semantically mismatched,
report that exact mismatch.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/erdos866-g6-sidon-and-upper/erdos866-g6-sidon-and-upper-supervised-4h/summary.md",
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/erdos866-g6-sidon-and-upper/erdos866-g6-sidon-and-upper-supervised-4h/supervisor/round-048/decision.md",
                "artifacts/literature/ces75/theorem4_engineering_decomposition_20260510.md",
            ),
        },
        {
            "priority": 4,
            "slug": "independent-domination80-ckko-source-contract",
            "kind": "lean-formalizer",
            "problem_id": "independent-domination-80",
            "title": "Independent domination 80 source-faithful CKKO contract",
            "workspace": str(FORMAL),
            "target_file": str(
                FORMAL
                / "AmraLibrary"
                / "OpenProblemBatches"
                / "Attack1680866_20260608"
                / "IndependentDomination80.lean"
            ),
            "target_theorem": "ckko_corollary_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated",
            "build_command": (
                "env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "lake env lean AmraLibrary/OpenProblemBatches/Attack1680866_20260608/"
                "IndependentDomination80.lean"
            ),
            "statement": """
# Independent domination 80 Lean/source-faithful CKKO route

Continue Lean formalization. Do not switch back to natural-language proof
discovery unless Lean finds a source/bridge inconsistency.

Current target:

```lean
theorem ckko_corollary_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (Δ : ℕ) (hΔ : 0 < Δ)
    (hMax : G.maxDegree ≤ Δ)
    (hIso : 0 < G.minDegree) :
    let m := ((Δ + 2)^2) / 4
    ∃ S : Finset V,
      G.IsNIndepDominatingSet S.card S ∧
      m * S.card ≤ (m - Δ) * Fintype.card V
```

The current file fails in the large-order CKKO source-bound branch; repair that
branch or introduce a source-faithful CKKO contract that closes it. Do not revive
the false disconnected `(Fintype.card V - 1)` denominator route or the false
half-bound.
""",
            "contexts": existing(
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/independent-domination-80-formalization/independent-domination-80-formalization-supervised-4h/summary.md",
                "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/independent-domination-80-formalization/independent-domination-80-formalization-supervised-4h/supervisor/round-017/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            ),
        },
    ]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])

    command = [*resource_prefix(lean=target["kind"] == "lean-formalizer"), *common_campaign_args(target, statement_file, output_root)]
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
            "ARA_MATH_MAX_LOAD_PER_CPU": "6.0",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "20",
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
