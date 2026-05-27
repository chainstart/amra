#!/usr/bin/env python3
"""Launch a resource-capped serial Lean formalization queue for three targets."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
FORMAL = REPO / "amra_library" / "formal"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "lean_queue_3_20260527_v3"
TARGET_SOURCE_DIR = FORMAL / "AmraLibrary" / "OpenProblemBatches" / "LeanQueue20260527"
TIME_BUDGET_SECONDS = 4 * 60 * 60


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "exists-maximal-star",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "statement": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/09-exists-maximal-star.md",
        "latest_summary": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/exists-maximal-star/exists-maximal-star-nl-8h/proof_lab/round-364/summary.md",
        "latest_decision": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/exists-maximal-star/exists-maximal-star-nl-8h/supervisor/round-364/decision.md",
        "source_context": "data/research_open/raw/formal_conjectures/FormalConjectures/Paper/Chvatal.lean",
        "target_theorem": "pairwise_intersecting_two_sets_common_vertex_or_triangle",
        "lean": r"""import Mathlib

namespace ChvatalLeanBatch20260527

open Classical

variable {α : Type} [Fintype α] [DecidableEq α] [Nonempty α]

def Intersecting (F : Finset (Finset α)) : Prop :=
  ∀ A ∈ F, ∀ B ∈ F, A ∩ B ≠ ∅

theorem pairwise_intersecting_two_sets_common_vertex_or_triangle
    (E : Finset (Finset α))
    (h2 : ∀ A ∈ E, A.card = 2)
    (hI : Intersecting E) :
    (∃ x : α, ∀ A ∈ E, x ∈ A) ∨
      ∃ a b c : α,
        a ≠ b ∧ b ≠ c ∧ a ≠ c ∧
        E = ({ {a, b}, {a, c}, {b, c} } : Finset (Finset α)) := by
  sorry

end ChvatalLeanBatch20260527
""",
    },
    {
        "priority": 2,
        "slug": "wowii-conjecture19",
        "problem_id": "formal-conjectures-conjecture19",
        "statement": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/08-wowii-conjecture19.md",
        "latest_summary": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/proof_lab/round-322/summary.md",
        "latest_decision": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/wowii-conjecture19/wowii-conjecture19-nl-8h/supervisor/round-322/decision.md",
        "source_context": "amra_library/formal/AmraLibrary/Combinatorics/SimpleGraph/GraphConjectures/WowiiConjecture13.lean",
        "target_theorem": "not_adj_neighbor_geodesic_vertex_of_index_ge_three",
        "lean": r"""import AmraLibrary.Combinatorics.SimpleGraph.GraphConjectures.WowiiConjecture13
import Mathlib.Tactic

namespace SimpleGraph

open Classical

variable {α : Type*} [Fintype α] [DecidableEq α]

theorem not_adj_neighbor_geodesic_vertex_of_index_ge_three
    {G : SimpleGraph α} {x y a : α} (p : G.Walk x y)
    (hp : p.length = G.dist x y) {i : ℕ}
    (hi3 : 3 ≤ i) (hi : i ≤ p.length)
    (hxa : G.Adj x a) :
    ¬ G.Adj a (p.getVert i) := by
  sorry

end SimpleGraph
""",
    },
    {
        "priority": 3,
        "slug": "antihydra",
        "problem_id": "formal-conjectures-beaver-math-olympiad-problem-2-antihydra",
        "statement": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/statements/10-antihydra.md",
        "latest_summary": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/proof_lab/round-329/summary.md",
        "latest_decision": "artifacts/open_problem_screening/latest/nl_attack_10_20260526/runs/antihydra/antihydra-nl-8h/supervisor/round-329/decision.md",
        "source_context": "data/research_open/raw/formal_conjectures/FormalConjectures/Other/BeaverMathOlympiad.lean",
        "target_theorem": "handoffS_handoffNext_eq_even_run_len",
        "initial_target": "not_three_dvd_handoffEvenStart_div_two_pow_val",
        "lean": r"""import Mathlib

namespace BeaverMathOlympiadLeanBatch20260527

open Classical

def handoffP (Y : ℕ) : ℕ := padicValNat 2 (Y + 1)

def handoffEvenStart (Y : ℕ) : ℕ :=
  3 ^ handoffP Y * ((Y + 1) / 2 ^ handoffP Y) - 1

def handoffS (Z : ℕ) : ℕ := padicValNat 3 Z

def handoffNext (Y : ℕ) : ℕ :=
  3 ^ padicValNat 2 (handoffEvenStart Y) *
    (handoffEvenStart Y / 2 ^ padicValNat 2 (handoffEvenStart Y))

theorem handoffP_pos_of_odd (Y : ℕ) (hY : Odd Y) :
    0 < handoffP Y := by
  sorry

theorem not_three_dvd_handoffEvenStart (Y : ℕ) (hY : Odd Y) :
    ¬ 3 ∣ handoffEvenStart Y := by
  sorry

theorem not_three_dvd_handoffEvenStart_div_two_pow_val
    (Y : ℕ) (hY : Odd Y) :
    ¬ 3 ∣ handoffEvenStart Y / 2 ^ padicValNat 2 (handoffEvenStart Y) := by
  sorry

theorem handoffS_handoffNext_eq_even_run_len
    (Y : ℕ) (hY : Odd Y) :
    handoffS (handoffNext Y) = padicValNat 2 (handoffEvenStart Y) := by
  sorry

end BeaverMathOlympiadLeanBatch20260527
""",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def existing_contexts(target: dict[str, Any]) -> list[str]:
    contexts: list[str] = []
    for key in ("statement", "latest_summary", "latest_decision", "source_context"):
        path = REPO / str(target[key])
        if path.exists():
            contexts.append(str(path))
    return contexts


def clean_target_workspace() -> None:
    TARGET_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for path in TARGET_SOURCE_DIR.glob("*.lean"):
        path.unlink()


def prepare_targets() -> list[dict[str, Any]]:
    (RUN_ROOT / "targets").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "seed_lean").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "final_lean").mkdir(parents=True, exist_ok=True)
    TARGET_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "logs").mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / "runs").mkdir(parents=True, exist_ok=True)
    clean_target_workspace()
    prepared: list[dict[str, Any]] = []
    for target in TARGETS:
        target_file = TARGET_SOURCE_DIR / f"{target['priority']:02d}_{target['slug'].replace('-', '_')}.lean"
        seed_lean_file = RUN_ROOT / "seed_lean" / target_file.name
        final_lean_file = RUN_ROOT / "final_lean" / target_file.name
        statement_file = RUN_ROOT / "targets" / f"{target['priority']:02d}-{target['slug']}.md"
        seed_lean_file.write_text(str(target["lean"]).rstrip() + "\n", encoding="utf-8")
        statement_file.write_text(
            "\n".join(
                [
                    f"# Lean Formalization Batch: {target['slug']}",
                    "",
                    f"Problem id: `{target['problem_id']}`",
                    f"Target theorem: `{target['target_theorem']}`",
                    "Budget: 4 hours, serial queue, `LEAN_NUM_THREADS=1`.",
                    "",
                    "Use the supplied prior proof-lab summaries as context.  Close the displayed Lean theorem without `sorry`, `admit`, or new axioms.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        build_command = f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {target_file}"
        cmd = [
            "nice",
            "-n",
            "10",
            sys.executable,
            "run.py",
            "run-campaign-loop",
            "--statement-file",
            str(statement_file),
            "--workspace",
            str(FORMAL),
            "--target-file",
            str(target_file),
            "--final-target-theorem",
            str(target["target_theorem"]),
            "--build-command",
            build_command,
            "--backend",
            "codex",
            "--closed-book",
            "--mode",
            "lean-formalizer",
            "--rounds",
            "999",
            "--time-budget",
            str(TIME_BUDGET_SECONDS),
            "--round-time-budget",
            "2400",
            "--formalizer-attempts",
            "4",
            "--formalizer-attempt-timeout",
            "900",
            "--formalizer-build-timeout",
            "300",
            "--proof-attempts",
            "0",
            "--proof-audits",
            "0",
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
            f"{target['slug']}-lean-4h",
            "--reasoning-effort",
            "high",
        ]
        if target.get("initial_target"):
            cmd += ["--initial-target-theorem", str(target["initial_target"])]
        for context in existing_contexts(target):
            cmd += ["--context-file", context]
        prepared.append(
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "target_file": str(target_file),
                "seed_lean_file": str(seed_lean_file),
                "final_lean_file": str(final_lean_file),
                "statement_file": str(statement_file),
                "target_theorem": target["target_theorem"],
                "initial_target": target.get("initial_target"),
                "build_command": build_command,
                "log_path": str(RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"),
                "output_root": str(RUN_ROOT / "runs" / target["slug"]),
                "run_name": f"{target['slug']}-lean-4h",
                "command": cmd,
                "contexts": existing_contexts(target),
            }
        )
    write_json(
        RUN_ROOT / "manifest.json",
        {
            "generated_at": utc_now(),
            "run_root": str(RUN_ROOT),
            "mode": "serial_lean_queue",
            "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
            "resource_policy": "Only one Lean formalization command is run at a time; LEAN_NUM_THREADS=1 and OMP_NUM_THREADS=1.",
            "targets": prepared,
        },
    )
    return prepared


def run_worker() -> None:
    manifest = json.loads((RUN_ROOT / "manifest.json").read_text(encoding="utf-8"))
    targets = manifest["targets"]
    status_path = RUN_ROOT / "queue_status.json"
    env = os.environ.copy()
    env["LEAN_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    status: dict[str, Any] = {
        "started_at": utc_now(),
        "status": "running",
        "resource_policy": manifest["resource_policy"],
        "targets": [],
    }
    write_json(status_path, status)
    for target in targets:
        clean_target_workspace()
        target_file = Path(str(target["target_file"]))
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(Path(str(target["seed_lean_file"])).read_text(encoding="utf-8"), encoding="utf-8")
        item = {
            "slug": target["slug"],
            "problem_id": target["problem_id"],
            "started_at": utc_now(),
            "status": "running",
            "log_path": target["log_path"],
            "output_root": target["output_root"],
            "target_file": target["target_file"],
            "seed_lean_file": target["seed_lean_file"],
            "final_lean_file": target["final_lean_file"],
        }
        status["targets"].append(item)
        write_json(status_path, status)
        with Path(target["log_path"]).open("ab") as log:
            proc = subprocess.run(
                target["command"],
                cwd=REPO,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        if target_file.exists():
            Path(str(target["final_lean_file"])).write_text(target_file.read_text(encoding="utf-8"), encoding="utf-8")
        item["finished_at"] = utc_now()
        item["returncode"] = proc.returncode
        item["status"] = "completed" if proc.returncode == 0 else "failed"
        write_json(status_path, status)
        clean_target_workspace()
    status["finished_at"] = utc_now()
    status["status"] = "completed"
    write_json(status_path, status)


def launch() -> dict[str, Any]:
    prepared = prepare_targets()
    scheduler_log = RUN_ROOT / "logs" / "scheduler.log"
    with scheduler_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, __file__, "--worker"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    (RUN_ROOT / "scheduler.pid").write_text(f"{proc.pid}\n", encoding="ascii")
    payload = {
        "run_root": str(RUN_ROOT),
        "scheduler_pid": proc.pid,
        "scheduler_log": str(scheduler_log),
        "targets": prepared,
    }
    write_json(RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    if "--worker" in sys.argv:
        run_worker()
        return
    print(json.dumps(launch(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
