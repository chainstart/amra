#!/usr/bin/env python3
"""Launch 2h supervised main-direction attacks for the two unfinished true-open tracks."""

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
ARA_ANALYSIS = (
    Path("/home/biostar/work/projects/ara")
    / "projects"
    / "wowii19-formal-paper-20260608"
    / "analysis"
    / "other_open_problem_main_theorem_directions_20260608.md"
)
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "true_open_main_direction_20260608_2h"
)

TIME_BUDGET_SECONDS = 2 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 35 * 60


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
        "MemoryMax=6G",
        "-p",
        "MemorySwapMax=8G",
        "-p",
        "CPUQuota=150%",
    ]


def nice_prefix(extra_seconds: int = 600) -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + extra_seconds}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


GENERAL_STATEMENT = """
# General supercongruence normalized summand and harmonic bridge

Root original theorem:

```lean
theorem general_supercongruence (m : Nat) :
  exists exceptions : Finset Nat, forall p, p.Prime ->
    p notin exceptions -> u m (p - 1) = (0 : ZMod (p ^ 4))
```

This round must stay aligned with the original theorem. Do not spend the run on
another isolated binomial recurrence. Existing verified product expansions are
inputs.

Main goal for this 2h round:

1. Derive a Lean-ready normalized `ZMod (p ^ 4)` summand theorem for the actual
   `n = p - 1` summand, substituting `t = k - 1` in the upper-binomial
   expansion.
2. Combine the lower and upper binomial expansions before expanding products.
   The expected reduced summand shape is:
   `p^2 / k^(2*m+3) - 2*p^3 / k^(2*m+4)` modulo `p^4`.
3. Identify and, if feasible, prove the exact harmonic-sum vanishing lemmas
   needed outside a finite exception set depending on `m`.
4. Record the bridge obligations from the FormalConjectures definition of `u`
   and its rational numerator convention back to the normalized ZMod sum.

Concrete preferred outputs:

- A precise theorem statement for `general_supercongruence_normalized_zmod_sum`
  or a sharper equivalent.
- A precise theorem statement for the harmonic vanishing lemma used by that
  normalized theorem.
- Lean proof progress only where the statement is stable and directly serves
  the original theorem.
"""


CHVATAL_STATEMENT = """
# Chvatal rank-three counting mainline

Root original theorem:

```lean
theorem exists_maximal_star :
  forall F : Finset (Finset alpha), Decreasing F ->
    exists x : alpha, forall G, G subset F -> Intersecting G ->
      G.card <= {A in F | x in A}.card
```

The full arbitrary-rank theorem remains too broad for direct Lean attack. This
round should target the rank-three main theorem, which is the next meaningful
bounded-rank step after the verified rank-two theorem.

Preferred main theorem:

```lean
theorem exists_maximal_star_rank_three
    (F : Finset (Finset alpha)) (hdec : Decreasing F)
    (hrank : forall A in F, A.card <= 3) :
    exists x : alpha, forall G, G subset F -> Intersecting G ->
      G.card <= {A in F | x in A}.card
```

Main goal for this 2h round:

1. Organize the proof by transversal number: tau=1, tau=2, tau=3.
2. Reuse the verified rank-two theorem for tau=2.
3. For tau=3, use the existing verified structural lemma
   `rank_three_tau_three_trace_graph_degree_le_two`.
4. Focus on the missing global counting/injection lemma converting degree-at-most-two
   trace graphs into a star bound.

Concrete preferred outputs:

- A precise theorem statement for `rank_three_tau_three_trace_graph_count_le_star`
  or a sharper equivalent.
- A proof skeleton for `exists_maximal_star_rank_three` showing exactly where the
  counting lemma plugs in.
- Lean proof progress only after the counting lemma interface is coherent.
"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "general-supercongruence-normalized-summand",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence normalized summand and harmonic bridge",
        "mode": "proof-lab",
        "statement": GENERAL_STATEMENT,
        "final_target_theorem": "OeisA357513.general_supercongruence",
        "initial_target_theorem": "",
        "workspace": None,
        "target_file": None,
        "build_command": "lake build",
        "contexts": existing(
            ARA_ANALYSIS,
            "data/research_open/raw/formal_conjectures/FormalConjectures/OEIS/357513.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_continuation/runs/general-p-add-choose-factor/general-p-add-choose-factor-2h/summary.md",
        ),
    },
    {
        "priority": 2,
        "slug": "chvatal-rank-three-counting-mainline",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal rank-three counting mainline",
        "mode": "proof-lab",
        "statement": CHVATAL_STATEMENT,
        "final_target_theorem": "exists_maximal_star_rank_three",
        "initial_target_theorem": "",
        "workspace": None,
        "target_file": None,
        "build_command": "lake build",
        "contexts": existing(
            ARA_ANALYSIS,
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "artifacts/open_problem_screening/latest/true_open_next_round_20260608_continuation/runs/chvatal-rank-three-degree/chvatal-rank-three-degree-2h/summary.md",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, str(target["statement"]))

    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]
    cmd = [
        *resource_prefix(),
        *nice_prefix(),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
        "--backend",
        "codex",
        "--closed-book",
        "--source-first",
        "--mode",
        str(target["mode"]),
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
        "420",
        "--formalizer-attempts",
        "3",
        "--formalizer-attempt-timeout",
        "900",
        "--formalizer-build-timeout",
        "240",
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
        f"{target['slug']}-2h",
        "--reasoning-effort",
        "high",
    ]
    if target["final_target_theorem"]:
        cmd += ["--final-target-theorem", str(target["final_target_theorem"])]
    if target["initial_target_theorem"]:
        cmd += ["--initial-target-theorem", str(target["initial_target_theorem"])]
    if target["workspace"]:
        cmd += ["--workspace", str(target["workspace"])]
    if target["target_file"]:
        cmd += ["--target-file", str(target["target_file"])]
    if target["build_command"]:
        cmd += ["--build-command", str(target["build_command"])]
    for context in target["contexts"]:
        cmd += ["--context-file", context]

    return {
        **target,
        "statement_file": str(statement_file),
        "log_path": str(log_path),
        "output_root": str(output_root),
        "command": cmd,
    }


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
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
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
    return {
        "priority": target["priority"],
        "slug": target["slug"],
        "problem_id": target["problem_id"],
        "mode": target["mode"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "command": target["command"],
    }


def main() -> int:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launches = [start_target(target) for target in prepared]
    manifest = {
        "created_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "lean_heavy_process_cap": 2,
        "targets": launches,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
