#!/usr/bin/env python3
"""Launch a four-hour supervised proof-lab round for Erdos #866/#1084/#212."""

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
    / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h"
)
TIME_BUDGET_SECONDS = 4 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 45 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def existing(*paths: str) -> list[str]:
    contexts: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            contexts.append(str(path))
    return contexts


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "erdos866-g6-sqrt-lower-sidon",
        "problem_id": "erdos-866",
        "title": "Erdos #866 g6 square-root lower bound",
        "focus": """The CES75 integer-witness upper bound `gFun 6 N = O(sqrt N)` is now Lean-verified. Do not reopen any upper-bound, final-window, even-count, or source-bridge target.

Attack the missing lower direction `gFun 6 N >= c * sqrt N` for all sufficiently large `N` using the last paragraph of CES75 Theorem 4.

Required route:
1. Audit the earlier claim that a finite Sidon square-root lower route was already verified. Accept it only if an actual checked Lean declaration and source file are located; otherwise treat it as unproved.
2. Give an explicit construction, with constants, of a Sidon set `S_N` of size at least `c * sqrt N` in a bounded integer interval. Prefer an Erdos--Turan modular construction if it avoids importing heavy finite geometry. State every use of a prime-existence theorem precisely.
3. Map `S_N` into integers congruent to `2 mod 4` inside `[1,2N]`, and form `A_N` from all odd integers together with that image.
4. Prove that six distinct integer witnesses would contain four odd witnesses and force a nontrivial Sidon collision.
5. Convert the counterexample into a Lean-ready lower-bound statement for `gFun 6`, then state the exact final theorem that combines with the verified upper bound.

The deliverable is a checked mathematical proof with explicit constants and a ranked Lean lemma decomposition. Experiments may test constants but are not proof. Do not add assumptions, source markers, `sorry`, or an existence claim without construction/proof.""",
        "contexts": existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
            "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
            "artifacts/proof_lab/erdos866_sources_20260506/ErdosProblem866.lean",
            "artifacts/open_problem_screening/latest/attack_16_80_866_20260608_4h/runs/erdos866-g6-sidon-and-upper/erdos866-g6-sidon-and-upper-supervised-4h/supervisor/round-048/decision.md",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos1084-harborth-full-proof-route",
        "problem_id": "erdos-1084",
        "title": "Erdos #1084 Harborth contact upper bound",
        "focus": """The local wrappers and triangular-lattice lower construction are available, but the exact upper theorem `Erdos1084.HarborthTwoSeparatedContactUpperGe4Source` remains an external source proposition. Prior rounds froze source admission. Do not retry a source marker, opaque theorem, axiom, or conditional wrapper.

Open a fresh full-proof route for the Harborth contact-number inequality. Reconstruct and audit Harborth's argument from primary or authoritative sources, then decompose it into mathematical lemmas suitable for Lean.

Required route:
1. Verify the exact theorem, range, floor convention, contact-pair convention, and hypotheses against Harborth 1974 and an authoritative modern restatement.
2. Model the contact graph of a finite `2`-separated planar point set and prove the first geometric facts needed by the source proof: straight contact edges do not cross, angular separation at a vertex, and the appropriate planar embedding/outer-boundary facts.
3. Recover the perimeter/boundary estimate that sharpens Euler's planar bound to `floor (3N - sqrt (12N - 3))`.
4. Identify the smallest faithful nontrivial theorem that can be attacked next in Lean without assuming the final Harborth bound.
5. Produce an explicit dependency graph and exact Lean theorem header for that first target.

The deliverable is either a source-complete proof outline with every inequality justified, or a rigorous blocker certificate naming the first unavailable theorem. Do not report source agreement as a proof.""",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round6_20260709_4h/source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round6_20260709_4h/source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-10/supervisor/round-001/decision.md",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/source_statements/02-source-harborth-erdos1084.md",
        ),
    },
    {
        "priority": 3,
        "slug": "erdos212-unconditional-first-obstruction",
        "problem_id": "erdos-212",
        "title": "Erdos #212 unconditional rational-distance obstruction",
        "focus": """The topology lemma `lineOrCircleUnionFinsetClosedProperContainer` and the final theorem conditional on `BombieriLangConsequenceForRationalDistanceSets` are Lean-verified. Do not redo those results and do not treat the Bombieri--Lang consequence as unconditional.

Attack the first genuinely unconditional obstruction toward the original dense rational-distance problem.

Required route:
1. Audit the ABT/Shaffaf--Solymosi--de Zeeuw dependency chain and state exactly which step uses Bombieri--Lang or a stronger conjecture.
2. Search for an unconditional replacement in restricted cases: finite-degree curves, bounded genus, a fixed finite general-position seed, or a quantitatively bounded exceptional set.
3. Reconstruct the associated surface/fibration argument far enough to isolate one unconditional theorem that is both true and strictly advances the original problem.
4. Prove that theorem in full natural-language detail, or give a rigorous impossibility/blocker certificate if it would imply a known open conjecture.
5. Return an exact Lean-ready contract only for an unconditional theorem. Keep conjectural dependencies explicit and separate.

The deliverable is a ranked route package: best unconditional lemma, proof, connection to the original density contradiction, and remaining conjectural dependency. No `True`-elaborating source macro, new trusted assumption, or relabeling of a conditional result is allowed.""",
        "contexts": existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "artifacts/source_papers/abt/abt_bombieri_lang_consequence_source_certificate.md",
            "artifacts/source_papers/abt/abt_closed_proper_plane_image_source_certificate.md",
            "artifacts/source_papers/abt/abt_compactified_split_surface_objects_source_certificate.md",
            "artifacts/source_papers/abt/abt_projection_finite_away_from_bad_locus_source_certificate.md",
            "artifacts/source_papers/abt/abt_scaled_resolution_transport_source_certificate.md",
            "artifacts/open_problem_screening/latest/erdos2_866_212_round9_20260710_4h/runs/erdos212-line-circle-closed-proper-container/erdos212-line-circle-closed-proper-container-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos2_866_212_round9_20260710_4h/runs/erdos212-bombieri-lang-conditional-endgame-strict/erdos212-bombieri-lang-conditional-endgame-strict/summary.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 4h Proof Attack: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `erdos3_866_1084_212_round11_20260710_4h`",
            "",
            "Run policy:",
            "- Use AMRA `run-campaign-loop` in proof-lab mode.",
            "- Invoke the global Codex supervisor after every round.",
            "- Search and source grounding are enabled.",
            "- Prefer proof-level progress and faithful theorem contracts over local bookkeeping.",
            "- Do not fabricate source facts or promote conditional claims as unconditional.",
            "- Tiny Lean probes are allowed only to validate theorem shapes and available APIs.",
            "- End every round with a concrete next theorem or a rigorous freeze/blocker decision.",
            "",
            "Focus:",
            target["focus"],
            "",
        ]
    )


def campaign_command(target: dict[str, Any], statement_path: Path, output_root: Path) -> list[str]:
    command = [
        "/usr/bin/timeout",
        f"{HARD_TIMEOUT_SECONDS}s",
        "nice",
        "-n",
        "10",
    ]
    if shutil.which("ionice"):
        command.extend(["ionice", "-c2", "-n7"])
    command.extend(
        [
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
            str(15 * 60),
            "--proof-audit-timeout",
            str(6 * 60),
            "--proof-grounding-timeout",
            str(8 * 60),
            "--supervisor-backend",
            "codex",
            "--supervisor-every-rounds",
            "1",
            "--supervisor-timeout",
            str(10 * 60),
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
            "--max-stalled-rounds",
            "8",
        ]
    )
    for context in target["contexts"]:
        command.extend(["--context-file", context])
    return command


def process_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "AMRA_SKIP_TOOL_SMOKE": "1",
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "3072",
            "ARA_MATH_MAX_LOAD_PER_CPU": "6.0",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "20",
        }
    )
    return env


def main() -> None:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    launched: list[dict[str, Any]] = []
    env = process_env()
    for target in TARGETS:
        slug = target["slug"]
        statement_path = RUN_ROOT / "statements" / f"{target['priority']:02d}-{slug}.md"
        output_root = RUN_ROOT / "runs" / slug
        log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{slug}.log"
        pid_path = RUN_ROOT / "pids" / f"{target['priority']:02d}-{slug}.pid"
        write_text(statement_path, statement_for(target))
        command = campaign_command(target, statement_path, output_root)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("ab") as log:
            process = subprocess.Popen(
                command,
                cwd=REPO,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        write_text(pid_path, str(process.pid))
        launched.append(
            {
                "priority": target["priority"],
                "slug": slug,
                "problem_id": target["problem_id"],
                "pid": process.pid,
                "started_at": utc_now(),
                "statement_path": str(statement_path),
                "output_root": str(output_root),
                "log_path": str(log_path),
                "command": command,
            }
        )
    plan = """# Round 11 Plan

1. Erdos #866: leave the verified upper route closed and formalize the missing Sidon lower-bound construction and parity contradiction.
2. Erdos #1084: replace the frozen source-admission route with a full Harborth proof reconstruction and select the first faithful geometric Lean lemma.
3. Erdos #212: preserve the verified Bombieri--Lang conditional endgame and isolate/prove the strongest genuinely unconditional next obstruction.
4. Run all three proof-lab campaigns in parallel for at most four hours with global supervisor review every round.
5. Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.
"""
    write_text(RUN_ROOT / "plan.md", plan)
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "mode": "three parallel proof-lab campaigns with global supervisor every round",
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
