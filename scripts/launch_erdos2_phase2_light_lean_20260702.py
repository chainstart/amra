#!/usr/bin/env python3
"""Launch phase-2 direct proof-lab runs for two Erdos targets.

This intentionally avoids AMRA campaign-loop/supervisor promotion.  It launches
exactly two direct run-ai-proof-lab jobs with read-only Codex backends and
statements that forbid full Lean/Lake builds.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import time


PROJECT = pathlib.Path("/home/biostar/work/projects/amra")
RUN_ROOT = PROJECT / "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702"
MAX_SLOTS = 2
TIME_BUDGET_SECONDS = 4 * 60 * 60
WALL_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60


COMMON_CONSTRAINTS = """\
Hard constraints:
- Direct `run-ai-proof-lab` only. Do not invoke campaign-loop, supervisor
  promotion, or lean_formalizer stages.
- There are exactly two active slots in this launcher. Do not spawn child proof
  campaigns or extra parallel agents.
- Do not edit repository files.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, `AmraLibrary.lean`, or whole-project Lean checks.
- Lean is allowed only for tiny local probes: `#check`, `#print`, small local
  theorem-shape scratch files, or a single existing target file if it is already
  cheap. If the command would compile a broad dependency tree, skip it and say
  so explicitly.
- Classify every dependency as proved local, small Lean probe, source theorem,
  standard bridge, plausible lemma, unknown, or false.
"""


TARGETS = [
    {
        "slug": "erdos866-ces75-corollary-source-cert-phase2",
        "title": "Erdos 866: source-certify exact CES75 corollary contract",
        "statement": f"""\
# Erdos 866: source-certify exact CES75 corollary contract

{COMMON_CONSTRAINTS}

Current audited state:
The existing `gFun 6` route is structurally right but not closed. The remaining
fatal gap is the exact CES75 Lemma A/Theorem 4 corollary in the `Finset ℤ`
convention. Local assets already cover the final-window lemma and the
`CES75Theorem4... ↔ gFun 6` bridge.

Target for this slot:
Extract/source-certify the one theorem contract behind
`ces75_theorem4_even_count_case_reduction_source`.

Required deliverable:
1. Give the exact corollary as it should be cited from CES75, including whether
   constants are fixed, existential, or enlarged: `K`, `cCES`, `Nces`.
2. Decide the endpoint at the middle range: strict `< n/100` or `≤ n/100`.
3. State how a sequence/multiset formulation in the paper transfers to the
   current duplicate-free `Finset ℤ` convention, or identify this as the next
   source gap.
4. Separate local glue from source theorem: `m ≤ t`, `cCES * sqrt n < t`,
   central-even half-supply, direct outside-middle six-witness alternative.
5. End with one Lean-facing theorem package that can be added later without
   reopening the whole route.
""",
        "context": [
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos866-ces75-source-contract-light-lean/erdos866-ces75-source-contract-light-lean-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos866-ces75-source-contract-light-lean/erdos866-ces75-source-contract-light-lean-4h/audits/audit_attempt_002_output.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos866-ces75-source-contract-light-lean/erdos866-ces75-source-contract-light-lean-4h/grounding/source_grounding_output.md",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
        ],
    },
    {
        "slug": "erdos1084-harborth-package-phase2",
        "title": "Erdos 1084: Harborth source theorem and bridge package",
        "statement": f"""\
# Erdos 1084: Harborth source theorem and bridge package

{COMMON_CONSTRAINTS}

Current audited state:
All attempts agree that the first missing step is not local floor arithmetic or
a weak asymptotic upper bound. It is the Harborth planar contact-number theorem
as a source-backed theorem in the exact local `unitDistNum` convention, plus a
small radius-`1/2` disk-center bridge.

Target for this slot:
Produce a Lean-facing theorem package for closing the `N ≥ 4` upper branch.

Required deliverable:
1. State the imported/source theorem for congruent disk contact numbers,
   including scaling from unit disks to radius-`1/2` disks.
2. State the local bridge lemma(s): `Metric.IsSeparated' 1` center set ->
   non-overlapping radius-`1/2` disks, and tangency/contact edges ->
   unordered `unitDistNum` pairs.
3. Decide whether the lower/existence side should be bundled now or split as
   `harborth_unitDistNum_lower_ge4`.
4. Use only tiny local Lean inspection if cheap; otherwise use source and
   theorem-contract work only.
5. End with the exact next theorem package to formalize and a freeze list.
""",
        "context": [
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos1084-harborth-upper-contract-light-lean/erdos1084-harborth-upper-contract-light-lean-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos1084-harborth-upper-contract-light-lean/erdos1084-harborth-upper-contract-light-lean-4h/audits/audit_attempt_001_output.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos1084-harborth-upper-contract-light-lean/erdos1084-harborth-upper-contract-light-lean-4h/grounding/source_grounding_output.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/final_lean/02_erdos_1084_triangular_d2.lean",
        ],
    },
]


def abspaths(paths: list[str]) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for raw in paths:
        p = PROJECT / raw
        if p.exists():
            out.append(p)
    return out


def main() -> int:
    if len(TARGETS) > MAX_SLOTS:
        raise RuntimeError(f"Refusing to launch {len(TARGETS)} targets; MAX_SLOTS={MAX_SLOTS}")

    for sub in ["statements", "logs", "pids", "runs"]:
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "AMRA_SKIP_TOOL_SMOKE": "1",
        }
    )

    launched = []
    for idx, target in enumerate(TARGETS, start=1):
        statement_path = RUN_ROOT / "statements" / f"{idx:02d}-{target['slug']}.md"
        statement_path.write_text(target["statement"], encoding="utf-8")

        output_root = RUN_ROOT / "runs" / target["slug"]
        log_path = RUN_ROOT / "logs" / f"{idx:02d}-{target['slug']}.log"
        cmd = [
            "/usr/bin/timeout",
            f"{WALL_TIMEOUT_SECONDS}s",
            "nice",
            "-n",
            "10",
            "ionice",
            "-c2",
            "-n7",
            "/usr/bin/python3",
            "run.py",
            "run-ai-proof-lab",
            "--statement-file",
            str(statement_path),
            "--backend",
            "codex",
            "--search",
            "--source-first",
            "--attempts",
            "4",
            "--audits",
            "2",
            "--time-budget",
            str(TIME_BUDGET_SECONDS),
            "--attempt-timeout",
            "1200",
            "--audit-timeout",
            "600",
            "--grounding-timeout",
            "600",
            "--math-tools-profile",
            "essential",
            "--no-install-missing-math-tools",
            "--no-math-tool-smoke",
            "--output-root",
            str(output_root),
            "--run-name",
            f"{target['slug']}-4h",
            "--reasoning-effort",
            "high",
        ]
        for context_path in abspaths(target["context"]):
            cmd.extend(["--context-file", str(context_path)])

        log_fh = log_path.open("w", encoding="utf-8")
        proc = subprocess.Popen(cmd, cwd=PROJECT, env=env, stdout=log_fh, stderr=subprocess.STDOUT)
        (RUN_ROOT / "pids" / f"{idx:02d}-{target['slug']}.pid").write_text(f"{proc.pid}\n", encoding="utf-8")
        launched.append(
            {
                "slug": target["slug"],
                "pid": proc.pid,
                "log_path": str(log_path),
                "statement_path": str(statement_path),
            }
        )
        time.sleep(1)

    manifest = {
        "run_root": str(RUN_ROOT),
        "max_slots": MAX_SLOTS,
        "mode": "direct run-ai-proof-lab phase2",
        "lean_policy": "tiny local probes only; no full Lean/Lake build",
        "launched": launched,
    }
    (RUN_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
