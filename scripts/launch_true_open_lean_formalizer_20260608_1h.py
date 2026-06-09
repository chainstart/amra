#!/usr/bin/env python3
"""Launch 1h Lean formalizer runs for the two currently blocked true-open tracks."""

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
SOURCE_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "true_open_main_direction_20260608_2h"
)
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "true_open_lean_formalizer_20260608_1h"
)

TIME_BUDGET_SECONDS = 60 * 60
ATTEMPT_TIMEOUT_SECONDS = 15 * 60
BUILD_TIMEOUT_SECONDS = 4 * 60


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


def nice_prefix(extra_seconds: int = 300) -> list[str]:
    command = ["timeout", f"{TIME_BUDGET_SECONDS + extra_seconds}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


GENERAL_HEADER = """lemma square_zero_mul_prod_one_add_sq
    {R : Type*} [CommRing R] {ι : Type*}
    (s : Finset ι) (q : R) (b : ι → R) (hq : q ^ 2 = 0) :
    q * (∏ x in s, (1 + q * b x)) ^ 2 = q"""


CHVATAL_HEADER = """theorem four_edge_degree_two_crossing_family_card_le_two
    {β : Type} [Fintype β] [DecidableEq β]
    (E J : Finset (Finset β))
    (hEcard : E.card = 4)
    (hEedge : ∀ e ∈ E, e.card = 2)
    (hJedge : ∀ f ∈ J, f.card = 2)
    (hEdeg : ∀ x, ({e ∈ E | x ∈ e}.card ≤ 2))
    (hcross : ∀ f ∈ J, ∀ e ∈ E, (f ∩ e).Nonempty) :
    J.card ≤ 2"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "general-square-zero-product-formalizer",
        "problem_id": "formal-conjectures-general-supercongruence",
        "title": "Generic square-zero finite-product absorption",
        "target_theorem": "square_zero_mul_prod_one_add_sq",
        "header": GENERAL_HEADER,
        "statement": "\n".join(
            [
                "# General supercongruence Lean formalizer target",
                "",
                "Prove exactly the generic square-zero product lemma below.",
                "This is the immediate blocker for `zmod_prefix_pair_product_absorb_square_mod_p4`; do not work on harmonic sums or the rational `u` bridge in this run.",
                "",
                "```lean",
                GENERAL_HEADER,
                "```",
                "",
                "Recommended route: first prove `q * (Finset.prod s (fun x => 1 + q * b x)) = q` by `Finset.induction_on`; use `classical` for decidable equality if needed. In the insert step, expand `q * (P * (1 + q * b a))`, use `hq : q ^ 2 = 0`, and close by `ring`/`simp`. Derive the squared lemma by rewriting `q * P ^ 2 = (q * P) * P` and applying the non-square helper again.",
            ]
        ),
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "04_general_supercongruence_zmod_cast.lean",
        "build_command": "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
        "contexts": existing(
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-normalized-summand"
            / "general-supercongruence-normalized-summand-2h"
            / "summary.md",
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-normalized-summand"
            / "general-supercongruence-normalized-summand-2h"
            / "supervisor"
            / "round-012"
            / "decision.md",
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-normalized-summand"
            / "general-supercongruence-normalized-summand-2h"
            / "proof_lab"
            / "round-012"
            / "grounding"
            / "source_grounding_output.md",
            SOURCE_ROOT
            / "runs"
            / "general-supercongruence-normalized-summand"
            / "general-supercongruence-normalized-summand-2h"
            / "proof_lab"
            / "round-009"
            / "audits"
            / "audit_attempt_001_meta.json",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/04_general_supercongruence_zmod_cast.lean",
        ),
    },
    {
        "priority": 2,
        "slug": "chvatal-four-edge-crossing-formalizer",
        "problem_id": "formal-conjectures-exists-maximal-star",
        "title": "Four-edge degree-two crossing family cardinal bound",
        "target_theorem": "four_edge_degree_two_crossing_family_card_le_two",
        "header": CHVATAL_HEADER,
        "statement": "\n".join(
            [
                "# Chvatal rank-three Lean formalizer target",
                "",
                "Prove exactly the standalone four-edge finite graph lemma below.",
                "This is the immediate blocker for the rank-three tau-three counting route; do not work on the full Chvatal theorem in this run.",
                "",
                "```lean",
                CHVATAL_HEADER,
                "```",
                "",
                "Recommended route: split on `J.Nonempty`; in the nonempty case choose `f ∈ J`, destruct `hJedge f hf` using `Finset.card_eq_two` as `f = {a,b}`, define `Ea := {e ∈ E | a ∈ e}` and `Eb := {e ∈ E | b ∈ e}`, close the checkpoint `E = Ea ∪ Eb`, `Ea.card = 2`, `Eb.card = 2`, `Ea ∩ Eb = ∅`, then show `J ⊆ {f, opposite}` and finish by `Finset.card_le_card`.",
            ]
        ),
        "workspace": REPO / "amra_library" / "formal",
        "target_file": REPO
        / "amra_library"
        / "formal"
        / "AmraLibrary"
        / "OpenProblemBatches"
        / "TrueOpenNextRound20260606"
        / "06_exists_maximal_star_rank_two.lean",
        "build_command": "lake env lean AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        "contexts": existing(
            SOURCE_ROOT
            / "runs"
            / "chvatal-rank-three-counting-mainline"
            / "chvatal-rank-three-counting-mainline-2h"
            / "summary.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-rank-three-counting-mainline"
            / "chvatal-rank-three-counting-mainline-2h"
            / "supervisor"
            / "round-014"
            / "decision.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-rank-three-counting-mainline"
            / "chvatal-rank-three-counting-mainline-2h"
            / "proof_lab"
            / "round-014"
            / "summary.md",
            SOURCE_ROOT
            / "runs"
            / "chvatal-rank-three-counting-mainline"
            / "chvatal-rank-three-counting-mainline-2h"
            / "rounds"
            / "round_011"
            / "stage_goal.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/06_exists_maximal_star_rank_two.lean",
        ),
    },
]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    header_file = RUN_ROOT / "headers" / f"{target['priority']:02d}-{target['slug']}.lean"
    write_text(statement_file, str(target["statement"]))
    write_text(header_file, str(target["header"]))

    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    output_root = RUN_ROOT / "runs" / target["slug"]
    cmd = [
        *resource_prefix(),
        *nice_prefix(),
        sys.executable,
        "run.py",
        "run-lean-formalizer",
        "--workspace",
        str(target["workspace"]),
        "--statement-file",
        str(statement_file),
        "--target-theorem",
        str(target["target_theorem"]),
        "--target-file",
        str(target["target_file"]),
        "--expected-target-header-file",
        str(header_file),
        "--backend",
        "codex",
        "--closed-book",
        "--attempts",
        "4",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--attempt-timeout",
        str(ATTEMPT_TIMEOUT_SECONDS),
        "--build-timeout",
        str(BUILD_TIMEOUT_SECONDS),
        "--build-command",
        str(target["build_command"]),
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-1h",
        "--reasoning-effort",
        "high",
        "--max-stalled-attempts",
        "2",
        "--rollback-failed-attempts",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
    ]
    for context in target["contexts"]:
        cmd += ["--context-file", context]

    return {
        **target,
        "statement_file": str(statement_file),
        "header_file": str(header_file),
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
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_LEAN_FORMALIZER_BACKEND_MAX_CPU_SECONDS": "1200",
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
        "target_theorem": target["target_theorem"],
        "pid": proc.pid,
        "started_at": utc_now(),
        "statement_file": target["statement_file"],
        "header_file": target["header_file"],
        "log_path": target["log_path"],
        "output_root": target["output_root"],
        "command": target["command"],
    }


def main() -> int:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "headers", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_target(target) for target in TARGETS]
    launched = [start_target(target) for target in prepared]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "source_root": str(SOURCE_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "attempt_timeout_seconds": ATTEMPT_TIMEOUT_SECONDS,
        "build_timeout_seconds": BUILD_TIMEOUT_SECONDS,
        "mode": "Lean formalizer only",
        "resource_policy": {
            "memory": "MemoryMax=6G, MemorySwapMax=8G when systemd-run is available",
            "cpu": "CPUQuota=150% when systemd-run is available",
            "lean": "two Lean formalizer tracks only; LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1",
            "rollback": "rollback_failed_attempts enabled",
            "external_search": "disabled via --closed-book",
        },
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    print(json.dumps({"run_root": str(RUN_ROOT), "targets": launched}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
