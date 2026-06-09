#!/usr/bin/env python3
"""Launch a 4 hour supervised NL/proof-lab follow-up for six true-open targets."""

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
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_followup_nl_6_20260606_4h"
PREV_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "true_open_next_round_6_20260606"

TIME_BUDGET_SECONDS = 4 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 45 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def existing(*paths: str) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / raw
        if path.exists():
            out.append(str(path))
    return out


def nice_prefix() -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + 600}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


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


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "kothe-radical-source-certificate",
        "problem_id": "formal-conjectures-kotherconjecture-variants-le-kotherradical",
        "title": "Koethe radical source certificate",
        "focus": "Source-audit only. Decide whether nil left ideals are known to lie in the upper nilradical/KotheRadical, whether a nil two-sided cover theorem exists, or whether that bridge is equivalent/stronger than Koethe. Produce one cited certificate target or `source_grounding_unavailable`.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/kothe-radical/kothe-radical-supervised-2h/supervisor/round-053/decision.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/01-kothe-radical.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/kothe-radical/kothe-radical-nl-8h/summary.md",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Wikipedia/Koethe.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "antihydra-certificate-design",
        "problem_id": "formal-conjectures-beaver-math-olympiad-problem-2-antihydra",
        "title": "Antihydra finite certificate design",
        "focus": "Bounded proof-lab certificate design. Define shifted odd-state handoff transition, select a finite quotient, compute and audit the transition/potential table, then return one Lean preservation theorem declaration or the first concrete obstruction.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/antihydra-certificate/antihydra-certificate-supervised-2h/supervisor/round-056/decision.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/10-antihydra.md",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/summary.md",
            "artifacts/open_problem_screening/latest/lean_queue_3_20260527_v3/final_lean/03_antihydra.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Other/BeaverMathOlympiad.lean",
        ),
    },
    {
        "priority": 3,
        "slug": "wowii-conjecture40-done-cardtwo",
        "problem_id": "formal-conjectures-conjecture40",
        "title": "WOWII Conjecture 40 DOne card-two certificate",
        "focus": "Work only on the DOne, |S|=|T|=2, no-Y-defect quotient/certificate around `NoYDefectDOneTwoSTwoTForcesYDeletionCapacity`. Produce a finite obstruction certificate or a minimal counterexample; do not retarget broadly.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/wowii-conjecture40/wowii-conjecture40-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/wowii-conjecture40/wowii-conjecture40-supervised-2h/supervisor/round-074/decision.md",
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-switch-obstruction-2h/summary.md",
            "artifacts/wowii_parallel/round5/conjecture40/conjecture40-endpoint-failure-3h/state.json",
        ),
    },
    {
        "priority": 4,
        "slug": "general-supercongruence-zmod-cast",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "General supercongruence ZMod cast lemma",
        "focus": "Use NL proof-lab with at most tiny Lean smoke probes. First close or precisely type the lemma `((p * p : Nat) : ZMod (p ^ 2)) = 0`; then state the next two paired-product expansion lemmas. Do not attack the full supercongruence.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/general-supercongruence/general-supercongruence-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/general-supercongruence/general-supercongruence-supervised-2h/supervisor/round-077/decision.md",
            "artifacts/focused_lean_attack/general-supercongruence-target-formalization/final.md",
            "artifacts/lean_workspaces/general_supercongruence/FormalConjectures/OEIS/357513.lean",
        ),
    },
    {
        "priority": 5,
        "slug": "wowii-conjecture19-path-helper",
        "problem_id": "formal-conjectures-conjecture19",
        "title": "WOWII Conjecture 19 path helper",
        "focus": "Use the newly inserted `path_vertices_erase_one_card_eq_length` helper as the only first target. Derive the proof plan from `path_index_image_card_eq`; after that, return to the diameter geodesic witness theorem. Report the first Lean API mismatch if proof fails.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/wowii-conjecture19/wowii-conjecture19-lean-supervised-restarted-20260606/supervisor/round-040/decision.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/05_wowii_conjecture19.lean",
            "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
            "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/summary.md",
        ),
    },
    {
        "priority": 6,
        "slug": "exists-maximal-star-rank-two-helper",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Chvatal rank-two helper",
        "focus": "Use `rank_two_intersecting_no_common_vertex_all_card_two` as the only first target. Proof plan: rule out card 0 by self-intersection, rule out card 1 by extracting a common vertex, then finish with card <= 2. After closure, return to `exists_maximal_star_rank_two`.",
        "contexts": existing(
            "artifacts/open_problem_screening/latest/true_open_followup_nl_6_20260606_4h/manual_assessment_20260606.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/exists-maximal-star-rank-two/exists-maximal-star-rank-two-lean-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/true_open_next_round_6_20260606/runs/exists-maximal-star-rank-two/exists-maximal-star-rank-two-lean-supervised-2h/supervisor/round-079/decision.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
            "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised NL Follow-up: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `true_open_followup_nl_6_20260606_4h`",
            "",
            "Run policy:",
            "- Use global supervisor every round.",
            "- Natural-language proof-lab/source/certificate work only.",
            "- Do not run heavy Lean builds; tiny theorem-shape probes are allowed only when they directly answer the current blocker.",
            "- Do not attack the broad final theorem before closing the named first blocker.",
            "- Required final output: exact target/certificate, what changed, first remaining blocker, and whether the next move is source audit, finite certificate, NL proof, tiny Lean probe, or freeze.",
            "",
            "Focused direction:",
            target["focus"],
            "",
        ]
    )


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    write_text(statement_file, statement_for(target))
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
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
        str(RUN_ROOT / "runs" / target["slug"]),
        "--run-name",
        f"{target['slug']}-nl-supervised-4h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]
    return {
        **target,
        "statement_file": str(statement_file),
        "log_path": str(log_path),
        "output_root": str(RUN_ROOT / "runs" / target["slug"]),
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
            "ARA_MATH_MAX_LOAD_PER_CPU": "6.0",
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
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
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
        "previous_run_root": str(PREV_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "mode": "proof-lab NL supervised",
        "resource_policy": {
            "supervisor": "codex every round, 600s timeout",
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "lean": "no heavy Lean lane; LEAN_NUM_THREADS=1 for tiny probes only",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
