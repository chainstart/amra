#!/usr/bin/env python3
"""Launch supervised 4 hour campaigns for targets 16, 80, and 866."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
FORMAL = REPO / "amra_library" / "formal"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "attack_16_80_866_20260608_4h"
TARGET_SOURCE_DIR = FORMAL / "AmraLibrary" / "OpenProblemBatches" / "Attack1680866_20260608"

TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 600
NL_ROUND_SECONDS = 45 * 60
LEAN_ROUND_SECONDS = 45 * 60


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


def resource_prefix(*, lean: bool) -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    if lean:
        return [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=14G",
            "-p",
            "MemorySwapMax=18G",
            "-p",
            "CPUQuota=180%",
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
        "CPUQuota=150%",
    ]


def nice_prefix() -> list[str]:
    command = ["timeout", f"{HARD_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def seed_independent_domination_80() -> str:
    return r"""
import Mathlib.Tactic

namespace IndependentDomination80Attack20260608

theorem cko_odd_floor_scale_nat {D : Nat} (hOdd : Odd D) :
    4 * ((D + 2) ^ 2 / 4) = (D + 1) * (D + 3) := by
  sorry

end IndependentDomination80Attack20260608
"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "wowii-conjecture16-central-interval",
        "kind": "proof-lab",
        "problem_id": "wowii-conjecture16",
        "title": "WOWII Conjecture 16 central-interval extension",
        "statement": "\n".join(
            [
                "# Supervised natural-language attack: WOWII Conjecture 16",
                "",
                "Top theorem: for finite connected simple graphs, prove",
                "",
                "```text",
                "b(G) >= 2 * (rad(G) - 1) + mu(G),",
                "mu(G) = max_v alpha(G[N(v)]).",
                "```",
                "",
                "This 4h run must not restart the broad proof search. Attack only the current narrow blocker.",
                "",
                "Completed or usable context:",
                "- The target reduces to prescribed-star extension / fixed-color maximum witness.",
                "- The geodesic-base construction is usable.",
                "- The delta=1 branch has a credible closed natural-language proof.",
                "- The tree case has a credible complete route.",
                "- No counterexample was found in the recorded finite probes.",
                "",
                "Current first blocker:",
                "",
                "```text",
                "General central-interval extension.",
                "Let P=p_0,...,p_e be a longest v-geodesic, r=rad(G),",
                "delta=2*r-2-e>0, and I={e-r+1,...,r-2}.",
                "Using off-base radius witnesses from the central interval,",
                "extract at least delta off-base vertices compatible with the",
                "base two-coloring X0,Y0; or prove an augmenting exchange",
                "for the fixed-color maximum witness whenever compatibility fails.",
                "```",
                "",
                "Supervisor policy:",
                "- If a round only renames Hall/quota/charge lemmas without proving a new invariant, retarget immediately.",
                "- Prefer a minimal theorem that handles delta=2 or a finite family of central intervals before the full delta case.",
                "- Freeze routes that rely on connected domination bridges or inclusion-maximality alone.",
                "- Each round must output: closed lemma, exact fatal gap, or a smaller Lean-ready theorem statement.",
            ]
        ),
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
            "artifacts/wowii_parallel/round3/conjecture16/blockers.md",
            "artifacts/wowii_parallel/round4/conjecture16/conjecture16-natural-proof-loop-4h/proof_package.md",
            "artifacts/wowii_parallel/round4/conjecture16/conjecture16-natural-proof-loop-4h/blocker.md",
            "artifacts/wowii_parallel/round4/conjecture16/conjecture16-natural-proof-loop-4h/counterexample_report.md",
            "artifacts/wowii_parallel/round5/conjecture16/conjecture16-quota-assembly-2h/summary.md",
            "artifacts/wowii_parallel/round5/conjecture16/conjecture16-ambient-blocker-3h/summary.md",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos866-g6-sidon-and-upper",
        "kind": "proof-lab",
        "problem_id": "erdos866",
        "title": "Erdos 866 gFun 6 sqrt lower/upper",
        "statement": "\n".join(
            [
                "# Supervised natural-language attack: Erdos 866, official gFun 6",
                "",
                "Top objective: advance the official integer-witness function `gFun 6` toward sqrt order.",
                "Do not work on stale positive-witness variants and do not redo g5/h5/CES75 assets.",
                "",
                "Completed or usable context:",
                "- `h5upper_log` and `g5_constant_bounds` are already verified.",
                "- `odd_mod4_sidon_no_g6` is recorded as verified.",
                "- `erdos866_g6_sqrt_lower_from_sidon` is recorded as verified.",
                "- The dyadic-transfer route has a fatal gap and is frozen.",
                "",
                "Current first lower blocker:",
                "",
                "```lean",
                "theorem finite_sidon_sqrt_lower :",
                "    exists c : Real, 0 < c /\\ exists N0 : Nat, forall N : Nat, N0 <= N ->",
                "      exists S : Finset Int,",
                "        S <= Finset.Icc (1 : Int) (N : Int) /\\",
                "        IsSidonSet S /\\",
                "        c * Real.sqrt (N : Real) <= (S.card : Real)",
                "```",
                "",
                "Preferred route: prove this through an explicit Erdos-Turan prime Sidon construction, with a source-grounded theorem contract if the construction is too long.",
                "",
                "Parallel source target:",
                "",
                "```lean",
                "theorem erdos866_g6_sqrt_upper :",
                "    exists C : Real, 0 < C /\\ exists N0 : Nat, forall n : Nat, N0 <= n ->",
                "      (gFun 6 n : Real) <= C * Real.sqrt (n : Real)",
                "```",
                "",
                "Supervisor policy:",
                "- If the lower construction becomes purely bibliographic, force an exact source theorem statement and Leanization contract.",
                "- If an upper route relies on dyadic transfer, reject it unless the affine transfer lemma is explicitly proved.",
                "- Do not accept general-k upper bounds such as `generalupper` as resolving gFun 6.",
                "- Each round must say whether it advances lower construction, upper source, or a bridge theorem.",
            ]
        ),
        "contexts": existing(
            "artifacts/proof_lab/erdos866-general-k-attack-8h-20260507/summary.md",
            "artifacts/proof_lab/erdos866-proof-lab-smoke/summary.md",
            "artifacts/campaign_loop/erdos866-g6-lower-packaging-loop-8h-20260507/proof_lab/round-006/summary.md",
            "artifacts/campaign_loop/erdos866-g6-lower-packaging-loop-8h-20260507/lean_formalizer/round-001-erdos866-g6-sqrt-lower-from-sidon/summary.md",
            "artifacts/lean_formalizer/erdos866-g5-official-closure-8h-20260507/summary.md",
            "artifacts/lean_formalizer/erdos866-dense-ces-lean-write-8h-20260507/summary.md",
        ),
    },
    {
        "priority": 3,
        "slug": "independent-domination-80-formalization",
        "kind": "hybrid-lean",
        "problem_id": "independent-domination-80",
        "title": "Independent domination even/odd formalization",
        "target_theorem": "cko_odd_floor_scale_nat",
        "statement": "\n".join(
            [
                "# Supervised Lean/formalization campaign: independent domination 80",
                "",
                "Top bundle objective: formalize the known-theorem route for the even and odd independent domination statements from arXiv 2107.00295.",
                "",
                "Primary next action is Lean work, not more natural-language proof discovery.",
                "",
                "Stage queue:",
                "",
                "1. Prove the local Nat arithmetic lemma:",
                "",
                "```lean",
                "theorem cko_odd_floor_scale_nat {D : Nat} (hOdd : Odd D) :",
                "    4 * ((D + 2) ^ 2 / 4) = (D + 1) * (D + 3)",
                "```",
                "",
                "2. Source-certify/formalize the witness-shaped CKKO Corollary 1.3 contract:",
                "",
                "```lean",
                "theorem ckko_corollary_exists_isNIndepDominatingSet_mul_boundedDegree_no_isolated ...",
                "```",
                "",
                "3. Bridge to `SimpleGraph.indepDominationNumber` using `Nat.sInf_le`, then specialize to even and odd max degree.",
                "",
                "Supervisor policy:",
                "- Do not send this back to natural-language route discovery unless the CKKO contract is source-inconsistent.",
                "- If the formalizer stalls on the odd arithmetic lemma, retarget to a smaller quotient/remainder lemma.",
                "- Once the odd arithmetic lemma verifies, switch target to the witness-shaped CKKO contract or the `sInf` bridge.",
                "- Record exact theorem declarations and keep assumptions source-faithful.",
            ]
        ),
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/2107.00295/IndependentDomination.lean",
            "data/research_open/raw/formal_conjectures/FormalConjecturesForMathlib/Combinatorics/SimpleGraph/GraphConjectures/Domination.lean",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/01-independent-domination-even.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/statements/02-independent-domination-odd.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-even/independent-domination-even-nl-continue-4h/proof_lab/round-031/summary.md",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/independent-domination-odd/independent-domination-odd-nl-continue-4h/proof_lab/round-051/summary.md",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, target["statement"])
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]
    common = [
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
        f"{target['slug']}-supervised-4h",
        "--reasoning-effort",
        "high",
    ]
    if target["kind"] == "hybrid-lean":
        TARGET_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        target_file = TARGET_SOURCE_DIR / "IndependentDomination80.lean"
        write_text(target_file, seed_independent_domination_80())
        build_command = f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {target_file}"
        cmd = [
            *resource_prefix(lean=True),
            *common,
            "--mode",
            "hybrid",
            "--workspace",
            str(FORMAL),
            "--target-file",
            str(target_file),
            "--initial-target-theorem",
            target["target_theorem"],
            "--build-command",
            build_command,
            "--round-time-budget",
            str(LEAN_ROUND_SECONDS),
            "--formalizer-attempts",
            "3",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "420",
        ]
        prepared = {
            **target,
            "statement_file": str(statement_file),
            "target_file": str(target_file),
            "build_command": build_command,
            "log_path": str(log_path),
            "output_root": str(output_root),
            "command": cmd,
        }
    else:
        cmd = [
            *resource_prefix(lean=False),
            *common,
            "--mode",
            "proof-lab",
            "--round-time-budget",
            str(NL_ROUND_SECONDS),
        ]
        prepared = {
            **target,
            "statement_file": str(statement_file),
            "log_path": str(log_path),
            "output_root": str(output_root),
            "command": cmd,
        }
    for context in target["contexts"]:
        prepared["command"] += ["--context-file", context]
    return prepared


def start_target(target: dict[str, Any]) -> dict[str, Any]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
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
    pid_file = RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid"
    write_text(pid_file, str(proc.pid))
    return {
        "priority": target["priority"],
        "slug": target["slug"],
        "problem_id": target["problem_id"],
        "kind": target["kind"],
        "pid": proc.pid,
        "pid_file": str(pid_file),
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "target_file": target.get("target_file", ""),
        "build_command": target.get("build_command", ""),
        "command": target["command"],
    }


def main() -> None:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": {
            "natural_language": NL_ROUND_SECONDS,
            "lean": LEAN_ROUND_SECONDS,
        },
        "mode": "16/866 proof-lab NL, 80 hybrid Lean, global supervisor every round",
        "resource_policy": {
            "supervisor": "codex every round, 600s timeout",
            "nl_memory": "MemoryMax=6G, CPUQuota=150% when systemd-run is available",
            "lean_memory": "MemoryMax=14G, CPUQuota=180% when systemd-run is available",
            "lean_threads": "LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
