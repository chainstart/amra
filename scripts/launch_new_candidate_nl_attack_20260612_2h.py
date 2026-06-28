#!/usr/bin/env python3
"""Launch 2h supervised natural-language attacks for five new open candidates."""

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
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "new_candidate_nl_attack_20260612_2h"
)

TIME_BUDGET_SECONDS = 2 * 60 * 60
WALL_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
ROUND_TIME_BUDGET_SECONDS = 35 * 60

SHORTLIST = (
    "artifacts/open_problem_screening/latest/"
    "new_candidate_shortlist_20260612.md"
)
SOURCE_SNAPSHOT_DIR = "sources/open_candidate_screening_20260612"


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
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def resource_prefix() -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    return [
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


def nice_prefix() -> list[str]:
    command = ["timeout", f"{WALL_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "erdos-1-distinct-subset-sums",
        "problem_id": "formal-conjectures-erdos-1",
        "title": "Erdos Problem #1 distinct subset sums",
        "final_target_theorem": "Erdos1.erdos_1",
        "contexts": existing(
            SHORTLIST,
            f"{SOURCE_SNAPSHOT_DIR}/www.erdosproblems.com_1.html",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
        ),
        "statement": """
# Erdos Problem #1: distinct subset sums

Mode: supervised natural-language proof-lab.  Do not edit Lean and do not
start heavy Lean compilation in this run.

Original target:

If `A subset {1, ..., N}` has all subset sums distinct, prove `N >> 2^|A|`.
The local Formal Conjectures target is `Erdos1.erdos_1`.

This is a route-discovery and bridge-building run, not a request to merely
repeat the existing weak `2^n / n` counting bound.

Required focus for this 2h run:

1. Reconstruct the strongest known lower-bound ladder from the source page:
   trivial counting, Erdos-Moser, binomial/central-layer bound, and the gap to
   the full `N >> 2^n` conjecture.
2. Identify the first theorem that would materially move the original target
   inside AMRA.  Prefer a source-faithful theorem around the binomial
   central-layer lower bound or an exact compression/anti-concentration bridge.
3. Classify each bridge as proved, literature-source, plausible, false, or
   Lean-ready.
4. Produce a Leanization plan only after the mathematical statement is stable.

Do not claim the main theorem solved unless the proof genuinely gives a
constant `C > 0` independent of `|A|`.
""",
    },
    {
        "priority": 2,
        "slug": "erdos-212-dense-rational-distance-set",
        "problem_id": "formal-conjectures-erdos-212",
        "title": "Erdos Problem #212 dense rational-distance set",
        "final_target_theorem": "Erdos212.erdos_212",
        "contexts": existing(
            SHORTLIST,
            f"{SOURCE_SNAPSHOT_DIR}/www.erdosproblems.com_212.html",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
        ),
        "statement": """
# Erdos Problem #212: dense rational-distance subset of the plane

Mode: supervised natural-language proof-lab.  Do not edit Lean and do not
start heavy Lean compilation in this run.

Original target:

Does there exist a dense subset of the plane such that all pairwise distances
are rational?  The local Formal Conjectures target is `Erdos212.erdos_212`.

Required focus for this 2h run:

1. Audit the source-faithful alternatives: direct construction, direct
   obstruction, and conditional obstruction via Bombieri-Lang/Tao/Shaffaf.
2. Extract the exact theorem contracts behind the conditional negative route:
   rational-distance set containment in algebraic curves, and finite result
   for rational-distance sets on curves unless line/circle exceptions apply.
3. Decide whether AMRA should attack construction, unconditional obstruction,
   or conditional theorem formalization next.
4. Give a finite-certificate or Lean-support plan only where it moves the
   original dense-set question.

Do not present a conditional Bombieri-Lang consequence as an unconditional
proof of the original problem.
""",
    },
    {
        "priority": 3,
        "slug": "graph-002-eternal-domination",
        "problem_id": "unsolvedmath-graph-002",
        "title": "GRAPH-002 eternal domination vs domination number",
        "final_target_theorem": "",
        "contexts": existing(
            SHORTLIST,
            f"{SOURCE_SNAPSHOT_DIR}/www.unsolvedmath.com_problems_GRAPH-002.html",
            f"{SOURCE_SNAPSHOT_DIR}/dwest.web.illinois.edu_regs_eterndom.html.html",
            f"{SOURCE_SNAPSHOT_DIR}/arxiv.org_abs_2110.09732.html",
        ),
        "statement": """
# GRAPH-002: eternal domination vs domination number

Mode: supervised natural-language proof-lab with light computation allowed.
Do not edit Lean and do not start heavy Lean compilation in this run.

Original target:

Find or refute the existence of a graph with domination number equal to
eternal domination number, both strictly less than the clique covering number:
`gamma(G) = gamma_infty(G) < theta(G)`.

Required focus for this 2h run:

1. Separate the exact GRAPH-002 target from the related solved target
   `gamma_infty(G) < theta(G)` in MacGillivray-Mynhardt-Virgile 2021.
2. Define a source-faithful finite graph search contract for `gamma`,
   `gamma_infty`, and clique cover number.
3. If computation is used, keep it small and record it as evidence unless it
   produces a fully checkable certificate.
4. Identify the first Lean certificate format that could verify a candidate
   graph without trusting the search code.

Do not claim the original question solved by citing examples where only
`gamma_infty < theta` is known.
""",
    },
    {
        "priority": 4,
        "slug": "erdos-972-beatty-prime-pairs",
        "problem_id": "formal-conjectures-erdos-972",
        "title": "Erdos Problem #972 Beatty prime pairs",
        "final_target_theorem": "Erdos972.erdos_972",
        "contexts": existing(
            SHORTLIST,
            f"{SOURCE_SNAPSHOT_DIR}/www.erdosproblems.com_972.html",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/972.lean",
        ),
        "statement": """
# Erdos Problem #972: Beatty prime pairs

Mode: supervised natural-language proof-lab and source/literature scout.
Do not edit Lean and do not start heavy Lean compilation in this run.

Original target:

For every irrational `alpha > 1`, prove there are infinitely many primes `p`
such that `floor(alpha * p)` is also prime.  The local Formal Conjectures target
is `Erdos972.erdos_972`.

Required focus for this 2h run:

1. Verify the formal statement against the source statement and note any
   semantic risks in `Nat.floor (alpha * p)`.
2. Collect the plausible analytic-number-theory route classes: Beatty primes,
   Piatetski-Shapiro/prime values in sequences, sieve/Type I-II estimates, and
   special irrational cases.
3. Run only light numerical scouts if helpful; do not treat experiments as
   proof.
4. Return a realistic next target: a special-alpha theorem, a conditional
   theorem under standard distribution hypotheses, or a precise literature
   bridge.

Do not spend the round trying to directly prove the full theorem in Lean.
""",
    },
    {
        "priority": 5,
        "slug": "one-third-two-thirds-posets",
        "problem_id": "formal-conjectures-1-3-2-3",
        "title": "1/3-2/3 conjecture for finite posets",
        "final_target_theorem": "Conjecture_1_3_to_2_3.conjecture_1_3_to_2_3",
        "contexts": existing(
            SHORTLIST,
            f"{SOURCE_SNAPSHOT_DIR}/mathoverflow.net_questions_322598_open-questions-about-posets.html",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Wikipedia/conjecture_1_3_to_2_3.lean",
        ),
        "statement": """
# 1/3-2/3 conjecture for finite posets

Mode: supervised natural-language proof-lab with light finite enumeration
allowed.  Do not edit Lean and do not start heavy Lean compilation in this run.

Original target:

Every finite non-total poset contains two elements `x, y` such that the
probability that `x` precedes `y` in a uniformly random linear extension lies
between `1/3` and `2/3`.

Required focus for this 2h run:

1. Audit the local Formal Conjectures statement for semantic hazards:
   representation of linear extensions as order homs, denominator
   non-zeroness, and use of `ncard`.
2. Identify known reductions or tractable classes worth formalizing first:
   small height, small width, semiorders, N-free/series-parallel classes, or
   small-cardinality exhaustive certificates.
3. Design a finite-poset enumerator/certificate pipeline that can later produce
   Lean-checkable certificates.
4. Return one theorem-level next target that is broad enough to matter but
   small enough to verify.

Do not use the stale local `unsolvedmath-comb-001` mapping as source evidence.
""",
    },
]


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# New Candidate NL Attack 2026-06-12",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target time budget: {manifest['time_budget_seconds_per_target']} seconds",
        "",
        "These are supervised natural-language proof-lab/scout runs.  They do not",
        "start Lean formalizer mode or heavy Lean compilation.",
        "",
        "| Priority | Slug | PID | Log |",
        "| ---: | --- | ---: | --- |",
    ]
    for target in manifest["targets"]:
        lines.append(
            f"| {target['priority']} | `{target['slug']}` | {target['pid']} | `{target['log_path']}` |"
        )
    return "\n".join(lines) + "\n"


def prepare_command(target: dict[str, Any], statement_path: Path, output_root: Path) -> list[str]:
    command = [
        *resource_prefix(),
        *nice_prefix(),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_path),
        "--backend",
        "codex",
        "--search",
        "--source-first",
        "--mode",
        "proof-lab",
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        str(ROUND_TIME_BUDGET_SECONDS),
        "--proof-attempts",
        "2",
        "--proof-audits",
        "1",
        "--proof-attempt-timeout",
        "900",
        "--proof-audit-timeout",
        "360",
        "--proof-grounding-timeout",
        "450",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "540",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-prooflab-2h",
        "--reasoning-effort",
        "high",
    ]
    if target["final_target_theorem"]:
        command += ["--final-target-theorem", str(target["final_target_theorem"])]
    for context in target["contexts"]:
        command += ["--context-file", context]
    return command


def launch() -> dict[str, Any]:
    statements_dir = RUN_ROOT / "statements"
    logs_dir = RUN_ROOT / "logs"
    pids_dir = RUN_ROOT / "pids"
    runs_dir = RUN_ROOT / "runs"
    for path in [statements_dir, logs_dir, pids_dir, runs_dir]:
        path.mkdir(parents=True, exist_ok=True)

    launched: list[dict[str, Any]] = []
    for target in TARGETS:
        statement_path = statements_dir / f"{target['priority']:02d}-{target['slug']}.md"
        log_path = logs_dir / f"{target['priority']:02d}-{target['slug']}.log"
        pid_path = pids_dir / f"{target['priority']:02d}-{target['slug']}.pid"
        output_root = runs_dir / target["slug"]
        write_text(statement_path, str(target["statement"]))

        command = prepare_command(target, statement_path, output_root)
        env = os.environ.copy()
        env.update(
            {
                "LEAN_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1",
                "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "1024",
                "ARA_MATH_MAX_LOAD_PER_CPU": "100",
                "ARA_MATH_SYSTEM_WAIT_SECONDS": "5",
                "ARA_MATH_BACKEND_MAX_MEMORY_MB": "3072",
                "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
            }
        )
        with log_path.open("ab") as log:
            proc = subprocess.Popen(
                command,
                cwd=REPO,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env=env,
            )
        write_text(pid_path, str(proc.pid))
        launched.append(
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "title": target["title"],
                "pid": proc.pid,
                "started_at": utc_now(),
                "statement_path": str(statement_path),
                "log_path": str(log_path),
                "output_root": str(output_root),
                "time_budget_seconds": TIME_BUDGET_SECONDS,
                "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
                "mode": "proof-lab",
                "command": command,
            }
        )

    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
        "lean_policy": "no new Lean formalizer or heavy Lean compilation",
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    write_text(RUN_ROOT / "README.md", render_readme(manifest))
    return manifest


if __name__ == "__main__":
    result = launch()
    print(
        json.dumps(
            {
                "run_root": result["run_root"],
                "targets": [
                    {
                        "slug": target["slug"],
                        "pid": target["pid"],
                        "log_path": target["log_path"],
                    }
                    for target in result["targets"]
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
