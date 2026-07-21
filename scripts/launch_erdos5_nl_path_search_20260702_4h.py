#!/usr/bin/env python3
"""Launch parallel 4h natural-language proof-path searches for five Erdos targets."""

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
    / "erdos5_nl_path_search_20260702_4h"
)

TIME_BUDGET_SECONDS = 4 * 60 * 60
WALL_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
ROUND_TIME_BUDGET_SECONDS = 45 * 60


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


GLOBAL_INSTRUCTIONS = """
Mode: AMRA supervised natural-language proof-lab / proof-path search.

Hard constraints for this run:

- Do not edit Lean files.
- Do not start Lean, Lake, or any full Lean build/check/compile.
- Do not switch into Lean formalizer mode.
- Work only in natural language proof search, source-route extraction,
  dependency analysis, and theorem-contract design.
- Small Python/text/source inspections are allowed only if they sharpen a
  proof route; experiments are evidence, not proof.
- Aim at the original Erdos target, not only a local helper. If a helper is
  proposed, explain exactly how it reduces the original target.
- Classify every major dependency as proved locally, source theorem,
  standard theorem, plausible new lemma, computation, false, or unknown.
- Return a ranked continuation target and a freeze package for unpromising
  branches.
"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "erdos212-rational-distance-density-route",
        "problem_id": "formal-conjectures-erdos-212",
        "title": "Erdos 212 rational-distance dense set",
        "final_target_theorem": "Erdos212.erdos_212",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/212.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212_sources.md",
            "artifacts/open_problem_screening/latest/followup_five_20260618_2h/runs/erdos212-post-endpoint-source-audit/erdos212-post-endpoint-source-audit-2h/summary.md",
            "artifacts/open_problem_screening/latest/guided_prooflab_next_20260613_2h/runs/erdos212-real-plane-endpoint-route/erdos212-real-plane-endpoint-route-2h/summary.md",
            "artifacts/open_problem_screening/latest/next_round_slots_20260613_2h/runs/erdos212-rational-distance-containment-source/erdos212-rational-distance-containment-source-2h-2/summary.md",
        ),
        "statement": f"""
# Erdos 212: dense rational-distance set

{GLOBAL_INSTRUCTIONS}

Original target:

Does there exist a dense subset of the Euclidean plane such that all pairwise
distances are rational? The local work has already proved downstream
conditional wrappers from a Bombieri-Lang-style rational-distance-set
containment consequence.

This 4h run should search broadly for the best next proof path:

1. Compare the construction route, unconditional obstruction route, and
   conditional algebraic-geometry route.
2. Audit whether the current local contract
   `BombieriLangConsequenceForRationalDistanceSets` is exactly source-faithful.
3. Identify any route that could move the original problem without simply
   restating Bombieri-Lang.
4. If the conditional route remains best, produce the exact source theorem
   contract needed, including line/circle exceptions and finite exceptional
   sets.
5. Return a recommendation: continue conditional source formalization, search
   for construction, or freeze as source-theorem dependent.
""",
    },
    {
        "priority": 2,
        "slug": "erdos972-beatty-prime-pair-route",
        "problem_id": "formal-conjectures-erdos-972",
        "title": "Erdos 972 Beatty prime pairs",
        "final_target_theorem": "Erdos972.erdos_972",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/972.lean",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos972.lean",
            "artifacts/open_problem_screening/latest/new_candidate_nl_attack_20260612_2h/runs/erdos-972-beatty-prime-pairs/erdos-972-beatty-prime-pairs-prooflab-2h/summary.md",
            "artifacts/open_problem_screening/latest/eight_next_round_20260612_1h/runs/erdos-972-unbounded-count-bridge/erdos-972-unbounded-count-bridge-1h/summary.md",
        ),
        "statement": f"""
# Erdos 972: Beatty prime pairs

{GLOBAL_INSTRUCTIONS}

Original target:

For every irrational `alpha > 1`, prove there are infinitely many primes `p`
such that `floor(alpha * p)` is also prime. Local AMRA work already has
count-to-infinite bridge lemmas; the analytic lower bound is the real blocker.

This 4h run should search broadly for viable proof routes:

1. Separate full irrational-alpha target from special-alpha and conditional
   distribution-hypothesis targets.
2. Identify the strongest plausible analytic theorem that would imply the
   initial-segment lower bound for prime pairs.
3. Decide whether the next AMRA step should be a raw-statement-aligned
   conditional theorem, a special case, or a literature-source theorem.
4. Look for semantic risks around `Nat.floor (alpha * p)` and positivity.
5. Return a ranked route list with dependencies and a precise next theorem
   contract.
""",
    },
    {
        "priority": 3,
        "slug": "erdos1084-triangular-contact-route",
        "problem_id": "formal-conjectures-erdos-1084",
        "title": "Erdos 1084 triangular planar contact number",
        "final_target_theorem": "erdos_1084.variants.triangular_optimal_d2",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/final_lean/02_erdos_1084_triangular_d2.lean",
            "artifacts/open_problem_screening/latest/nl_continue_5_20260527/runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-continue-4h/summary.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-8h/summary.md",
        ),
        "statement": f"""
# Erdos 1084: triangular d=2 optimum

{GLOBAL_INSTRUCTIONS}

Original target:

For `N = 3 n^2 + 3 n + 1`, prove the planar maximum number of unit distances
among `N` separated points is `9 n^2 + 3 n`. Local work has the triangular
floor arithmetic artifact, but not the full geometric/contact-number route.

This 4h run should search broadly for proof paths:

1. Decompose the theorem into lower construction, upper Harborth contact
   formula, and arithmetic specialization.
2. Check whether a self-contained lower construction for the triangular lattice
   patch is feasible as natural-language proof.
3. Identify the exact external source theorem needed for the upper bound and
   whether it matches the raw `f 2 N` definition.
4. Find any route that avoids the full Harborth theorem for triangular `N`.
5. Return the best next theorem contract and explain whether the source-file
   restoration step is only bookkeeping or mathematically substantive.
""",
    },
    {
        "priority": 4,
        "slug": "erdos1052-unitary-perfect-route",
        "problem_id": "formal-conjectures-erdos-1052",
        "title": "Erdos 1052 unitary perfect numbers",
        "final_target_theorem": "erdos_1052",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1052.lean",
            "data/banks/unitary_perfect_track.yaml",
            "projects/erdos-1052-shortlist-20260421/proof/current_focus.md",
            "projects/erdos-1052-shortlist-20260421/idea/proof_path_assessment.json",
            "projects/erdos-1052-shortlist-20260421/proof/proof_plan.json",
            "projects/odd-unitary-perfect-exclusion-20260425/proof/current_focus.md",
            "projects/1052-campaign-20260425/proof/current_focus.md",
        ),
        "statement": f"""
# Erdos 1052: finiteness of unitary perfect numbers

{GLOBAL_INSTRUCTIONS}

Original target:

Prove the set of unitary perfect numbers is finite. Local assets include
formal conjecture definitions, odd-unitary-perfect exclusion material, and a
q=5 ancestry-obstruction research thread. Some local notes mention Goto-style
global bounds; treat those claims as unverified until audited.

This 4h run should search broadly for proof paths:

1. Audit whether a credible full finiteness route exists in the local notes.
2. Separate solid foundation work from speculative q=5 ancestry branches.
3. Evaluate the Goto-bound route: exact theorem statement, source status, and
   whether it genuinely implies finiteness under the local definition.
4. Identify one theorem-level next target that materially advances the main
   finiteness problem rather than only proving examples.
5. Return branch labels: continue, conditionally formalize, source-audit first,
   or freeze.
""",
    },
    {
        "priority": 5,
        "slug": "erdos866-g6-sidon-ces75-route",
        "problem_id": "formal-conjectures-erdos-866",
        "title": "Erdos 866 g6 / Sidon / CES75 route",
        "final_target_theorem": "erdos866_g6_sqrt_upper",
        "contexts": existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ProofNotes.md",
            "projects/erdos-866-ai-continuation-20260505/proof/current_focus.md",
            "projects/erdos-866-ai-continuation-20260505/idea/proof_path_assessment.json",
            "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/erdos866-g6-sidon-and-upper/erdos866-g6-sidon-and-upper-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/next_round_16_80_866_a357513_20260609/runs/erdos866-g6-sqrt-upper-wrapper/erdos866-g6-sqrt-upper-wrapper-supervised-2h/summary.md",
        ),
        "statement": f"""
# Erdos 866: g6, Sidon lower route, and CES75 upper route

{GLOBAL_INSTRUCTIONS}

Original target:

Clarify the viable route for the `gFun 6 n = O(sqrt n)` / Sidon / CES75
thread. Existing work has a source-facing CES75 Theorem 4 statement and a
bridge from that statement to a `gFun 6` square-root upper bound; the source
fact itself and lower Sidon construction remain key blockers.

This 4h run should search broadly for proof paths:

1. Audit whether the CES75 source theorem is exactly strong enough for the
   current `HasPairwiseSums` / interval statement.
2. Compare the upper-source route with the finite Sidon square-root lower route.
3. Identify stale/dangerous routes, especially dyadic-transfer arguments
   without an affine transfer lemma.
4. Produce a precise natural-language proof dependency graph from CES75 to the
   target and from Sidon construction to the lower bound.
5. Return one next theorem contract and a freeze list of routes not worth
   continuing.
""",
    },
]


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# Erdos 5 NL Path Search 2026-07-02",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target time budget: {manifest['time_budget_seconds_per_target']} seconds",
        "",
        "These are parallel AMRA `run-campaign-loop --mode proof-lab` runs.",
        "They are natural-language proof-path searches only; Lean execution and",
        "Lean formalizer mode are explicitly disallowed in each statement.",
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
        "3",
        "--proof-audits",
        "1",
        "--proof-attempt-timeout",
        "1200",
        "--proof-audit-timeout",
        "420",
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
        f"{target['slug']}-prooflab-4h",
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
                "ARA_PROOF_LAB_BACKEND_MAX_MEMORY_MB": "3072",
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
                "context_count": len(target["contexts"]),
                "time_budget_seconds": TIME_BUDGET_SECONDS,
                "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
                "mode": "proof-lab",
                "lean_policy": "no Lean execution; no Lean formalizer",
                "command": command,
            }
        )

    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
        "lean_policy": "natural-language proof-path search only; no Lean execution or formalizer mode",
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
                        "context_count": target["context_count"],
                    }
                    for target in result["targets"]
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
