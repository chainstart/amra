#!/usr/bin/env python3
"""Run five supervised Erdos campaigns with a two-slot Lean promotion queue.

Policy:
- Five AMRA `run-campaign-loop` proof-lab campaigns run in parallel with a
  global supervisor every round.
- Those source/proof-lab campaigns are intentionally started without executable
  formalizer config, so a supervisor Lean-promotion decision becomes a durable
  requeue request instead of silently entering Lean inside that process.
- This scheduler watches the requeue requests and launches at most two
  `lean-formalizer` campaigns at a time.
- Formalizer build commands are single-file `lake env lean ...` checks only.
"""

from __future__ import annotations

import json
import os
import shlex
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260703_4h"
AMRA_FORMAL = REPO / "amra_library/formal"
FORMAL_CONJECTURES = REPO / "data/research_open/raw/formal_conjectures"
ERDOS866_FORMAL = REPO / "projects/erdos-866-ai-continuation-20260505/formal"

TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
LEAN_SLOT_LIMIT = 2
SOURCE_ROUND_SECONDS = 45 * 60
LEAN_ROUND_SECONDS = 40 * 60
MAX_SOURCE_CYCLES_PER_TARGET = 3
MAX_PROMOTIONS_PER_TARGET = 2


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_text_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        write_text(path, text)


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def rel_to_workspace(path: Path, workspace: Path) -> str:
    return str(path.resolve().relative_to(workspace.resolve()))


def single_file_build_command(workspace: Path, target_file: Path) -> str:
    rel = rel_to_workspace(target_file, workspace)
    return " ".join(
        [
            "env",
            "LEAN_NUM_THREADS=1",
            "OMP_NUM_THREADS=1",
            "lake",
            "env",
            "lean",
            shlex.quote(rel),
        ]
    )


def command_prefix(seconds: int, *, lean: bool) -> list[str]:
    seconds = max(60, min(HARD_TIMEOUT_SECONDS, seconds))
    prefix = ["/usr/bin/timeout", f"{seconds}s", "nice", "-n", "10"]
    if lean and shutil_which("ionice"):
        prefix += ["ionice", "-c2", "-n7"]
    elif shutil_which("ionice"):
        prefix += ["ionice", "-c2", "-n7"]
    return prefix


def shutil_which(name: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / name
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def source_hard_constraints() -> str:
    return """\
Execution policy for this campaign:
- Use AMRA `run-campaign-loop` with global supervisor every round.
- Natural-language/source proof-lab work may proceed freely.
- If the supervisor judges that a Lean formalizer/certificate round is needed,
  request promotion explicitly; the external controller will put it into the
  global Lean queue.
- Do not attempt to run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate
  imports, or whole-project Lean checks.
- The main theorem remains the target; stage theorems are valuable only when
  they shorten the path to the original Erdos statement.
"""


def lean_hard_constraints() -> str:
    return """\
Queued Lean-promotion policy:
- This formalizer job was started only after acquiring one of the two global
  Lean slots.
- Use only the configured single-file verifier command. Do not run `lake build`,
  `lake update`, `lake exe cache get`, aggregate imports, or whole-project Lean
  checks.
- Keep edits inside the configured target file/workspace.
- If the promoted theorem is actually a source theorem rather than a local Lean
  lemma, stop with a precise blocker instead of inventing assumptions.
"""


def target_file_amra(name: str) -> Path:
    return AMRA_FORMAL / "AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260703" / name


def target_file_formal_conjectures(name: str) -> Path:
    return FORMAL_CONJECTURES / "FormalConjectures/ErdosProblems/ErdosFiveQueue20260703" / name


def target_file_866() -> Path:
    return ERDOS866_FORMAL / "MathProject/ErdosFiveQueue20260703.lean"


TARGETS: list[dict[str, Any]] = [
    {
        "slug": "erdos212-rational-distance-density",
        "problem": "Erdos #212",
        "final_target": "Erdos212.erdos_212",
        "initial_target": "shaffaf_solymosi_de_zeeuw_containment_for_rational_distance_sets",
        "statement": """\
# Erdos #212: rational-distance dense set obstruction

Current state:
The unconditional route is frozen unless the Shaffaf/Solymosi-de Zeeuw finite
exception containment theorem is source-certified in a form strong enough for
the original problem. Construction-only attempts have been unpromising.

This round:
Keep the original Erdos #212 statement as the main objective. Attack the exact
source theorem and transfer package needed to turn the known rational-distance
containment result into the nondensity conclusion. If this becomes Lean-ready,
ask the supervisor for promotion so the controller queues it.
""",
        "source_contexts": existing(
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos212-rational-distance-density-route/erdos212-rational-distance-density-route-prooflab-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos212-rational-distance-density-route/erdos212-rational-distance-density-route-prooflab-4h/proof_lab/round-003/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos212-rational-distance-density-route/erdos212-rational-distance-density-route-prooflab-4h/supervisor/round-004/decision.md",
            "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212_sources.md",
        ),
        "lean": {
            "workspace": AMRA_FORMAL,
            "target_file": target_file_amra("Erdos212.lean"),
            "fallback_target": "shaffaf_solymosi_de_zeeuw_containment_for_rational_distance_sets",
            "seed": """\
import AmraLibrary.OpenProblemBatches.NewCandidates20260612.Erdos212

namespace AmraErdosFiveQueue20260703
namespace Erdos212

/- Queued promotion file for Erdos #212.  Add only local transfer lemmas here;
   external rational-distance containment theorems must remain explicit source
   assumptions/contracts. -/

end Erdos212
end AmraErdosFiveQueue20260703
""",
            "contexts": existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos212_sources.md",
            ),
        },
    },
    {
        "slug": "erdos972-beatty-prime-pair",
        "problem": "Erdos #972",
        "final_target": "Erdos972.erdos_972",
        "initial_target": "beatty_prime_pair_vonMangoldt_conditional_route_contract",
        "statement": """\
# Erdos #972: Beatty prime-pair infinitude

Current state:
The unconditional all-irrational route is frozen until a real analytic lower
bound for Beatty prime pairs is source-certified. Existing Lean-local material
only closes conditional bridges from an eventual lower bound to infinitude.

This round:
Attack the source/analytic route: identify the weakest credible theorem that
would imply infinitely many primes p with floor(αp) prime for irrational α>1.
If the output is a local conditional bridge rather than the analytic theorem,
ask for Lean promotion; otherwise keep it as a source blocker.
""",
        "source_contexts": existing(
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos972-beatty-prime-pair-route/erdos972-beatty-prime-pair-route-prooflab-4h/proof_lab/round-003/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos972-beatty-prime-pair-route/erdos972-beatty-prime-pair-route-prooflab-4h/supervisor/round-004/decision.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos972-beatty-prime-pair-route/erdos972-beatty-prime-pair-route-prooflab-4h/lean_formalizer/round-004-beatty-prime-pair-vonmangoldt-conditional-route-contract/summary.md",
        ),
        "lean": {
            "workspace": AMRA_FORMAL,
            "target_file": target_file_amra("Erdos972.lean"),
            "fallback_target": "beatty_prime_pair_vonMangoldt_conditional_route_contract",
            "seed": """\
import AmraLibrary.OpenProblemBatches.NewCandidates20260612.Erdos972

namespace AmraErdosFiveQueue20260703
namespace Erdos972

/- Queued promotion file for Erdos #972.  Local work should package conditional
   counting-to-infinitude bridges; the analytic lower bound itself must remain
   a named source theorem/contract. -/

end Erdos972
end AmraErdosFiveQueue20260703
""",
            "contexts": existing("amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos972.lean"),
        },
    },
    {
        "slug": "erdos1052-unitary-perfect",
        "problem": "Erdos #1052",
        "final_target": "Erdos1052.erdos_1052",
        "initial_target": "unitaryPerfect_twoAdicExponent_supplier_bound",
        "statement": """\
# Erdos #1052: finiteness of unitary perfect numbers

Current state:
Fixed-omega/Goto-only routes are insufficient for the original finiteness
claim. The current promising but high-risk blocker is a global supplier bound
for the 2-adic exponent or equivalent structural restriction.

This round:
Attack only the source/math package that could give a global finiteness route.
Classify whether the next node is a genuine source theorem, a computable local
number-theory lemma, or a false route. If a local Lean lemma is identified, ask
for promotion; otherwise keep the source blocker explicit.
""",
        "source_contexts": existing(
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos1052-unitary-perfect-route/erdos1052-unitary-perfect-route-prooflab-4h/proof_lab/round-002/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos1052-unitary-perfect-route/erdos1052-unitary-perfect-route-prooflab-4h/supervisor/round-002/decision.md",
        ),
        "lean": {
            "workspace": FORMAL_CONJECTURES,
            "target_file": target_file_formal_conjectures("Erdos1052Queue.lean"),
            "fallback_target": "unitaryPerfect_twoAdicExponent_supplier_bound",
            "seed": """\
import FormalConjectures.ErdosProblems.1052

namespace Erdos1052

/- Queued promotion file for Erdos #1052.  Do not weaken `erdos_1052` by adding
   unproved global assumptions; source-level finiteness theorems must remain
   explicit contracts. -/

end Erdos1052
""",
            "contexts": existing("data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1052.lean"),
        },
    },
    {
        "slug": "erdos866-g6-ces75",
        "problem": "Erdos #866",
        "final_target": "ces75_theorem4_integer_six_witness_upper_source_iff_g6upper_sqrt_bound",
        "initial_target": "ces75_theorem4_even_count_case_reduction_source",
        "statement": """\
# Erdos #866: CES75 source corollary to gFun 6

Current state:
The bridge to `gFun 6` and the final-window lemma are already local assets. The
missing node is the exact CES75 even-count corollary/source contract and the
small wrapper from that contract into the existing bridge.

This round:
Attack the original gFun route through the CES75 source theorem. The supervisor
may promote only local wrapper/counting lemmas; the CES75 dichotomy itself must
stay a named source theorem unless a real proof is found.
""",
        "source_contexts": existing(
            "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos866-ces75-corollary-source-cert-phase2/erdos866-ces75-corollary-source-cert-phase2-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos866-ces75-source-contract-light-lean/erdos866-ces75-source-contract-light-lean-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos866-g6-sidon-ces75-route/erdos866-g6-sidon-ces75-route-prooflab-4h/proof_lab/round-006/summary.md",
        ),
        "lean": {
            "workspace": ERDOS866_FORMAL,
            "target_file": target_file_866(),
            "fallback_target": "ces75_theorem4_even_count_case_reduction_source",
            "seed": """\
import MathProject.ErdosProblem866Core
import MathProject.GeneratedClaims
import MathProject.MainClaim

namespace MathProject

/- Queued promotion file for Erdos #866.  Prove only local wrappers/glue here;
   CES75 source dichotomies must remain explicit assumptions/contracts unless
   the source theorem itself is being formalized. -/

end MathProject
""",
            "contexts": existing(
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
            ),
        },
    },
    {
        "slug": "erdos1084-harborth-triangular",
        "problem": "Erdos #1084",
        "final_target": "Erdos1084.erdos_1084.variants.triangular_optimal_d2",
        "initial_target": "Erdos1084.harborth_unitDistNum_upper_ge4",
        "statement": """\
# Erdos #1084: triangular lattice contact number in d=2

Current state:
Triangular floor arithmetic is done. The real blocker is Harborth's planar
contact-number theorem translated into the local `unitDistNum` convention,
plus the small radius-1/2 disk-center bridge.

This round:
Keep the original triangular optimal statement in view. Supervisor may promote
the bridge/local package to Lean, but must not spend Lean effort reproving
Harborth from scratch.
""",
        "source_contexts": existing(
            "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos1084-harborth-package-phase2/erdos1084-harborth-package-phase2-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos2_light_lean_prooflab_20260702_4h/runs/erdos1084-harborth-upper-contract-light-lean/erdos1084-harborth-upper-contract-light-lean-4h/summary.md",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/final_lean/02_erdos_1084_triangular_d2.lean",
        ),
        "lean": {
            "workspace": FORMAL_CONJECTURES,
            "target_file": target_file_formal_conjectures("Erdos1084Queue.lean"),
            "fallback_target": "Erdos1084.harborth_unitDistNum_upper_ge4",
            "seed": """\
import FormalConjectures.ErdosProblems.1084

namespace Erdos1084

/- Queued promotion file for Erdos #1084.  Local work should package
   Harborth-as-source plus the radius-1/2 center/contact bridge; do not attempt
   to reprove Harborth's theorem from scratch. -/

end Erdos1084
""",
            "contexts": existing(
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
                "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/final_lean/02_erdos_1084_triangular_d2.lean",
            ),
        },
    },
]


def prepare_targets() -> None:
    for target in TARGETS:
        lean = target["lean"]
        write_text_if_missing(Path(lean["target_file"]), str(lean["seed"]))


def source_statement(target: dict[str, Any], cycle: int, extra_note: str = "") -> str:
    return "\n".join(
        [
            target["statement"].strip(),
            "",
            source_hard_constraints(),
            "",
            f"Problem: {target['problem']}",
            f"Final target theorem label: `{target['final_target']}`",
            f"Current stage target: `{target['initial_target']}`",
            f"Source cycle: {cycle}",
            "",
            extra_note.strip(),
            "",
            "Required output each round:",
            "- current first blocker relative to the original theorem;",
            "- whether the next node is source theorem, local Lean glue, false route, or frozen;",
            "- if Lean is appropriate, an explicit formalization target for queued promotion.",
        ]
    )


def lean_statement(target: dict[str, Any], theorem: str, source_report: Path | None) -> str:
    return "\n".join(
        [
            f"# Queued Lean promotion: {target['problem']}",
            "",
            target["statement"].strip(),
            "",
            lean_hard_constraints(),
            "",
            f"Promoted theorem: `{theorem}`",
            f"Source report: `{source_report or ''}`",
            "",
            "Do not close by adding axioms, constants, opaque declarations, or new trusted assumptions.",
            "If the theorem requires an external mathematical source theorem, encode only the local wrapper and report the source theorem as the blocker.",
        ]
    )


def process_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "AMRA_SKIP_TOOL_SMOKE": "1",
        }
    )
    return env


def launch_process(command: list[str], *, log_path: Path, env: dict[str, str]) -> subprocess.Popen[bytes]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = log_path.open("ab")
    return subprocess.Popen(
        command,
        cwd=REPO,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


def stop_process(proc: subprocess.Popen[bytes]) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def latest_report(output_root: Path) -> Path | None:
    reports = [p for p in output_root.glob("*/report.json") if p.is_file()]
    if not reports:
        reports = [p for p in output_root.rglob("report.json") if p.is_file()]
    if not reports:
        return None
    return max(reports, key=lambda p: p.stat().st_mtime)


def read_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def latest_summary_for_report(report_path: Path | None) -> Path | None:
    if report_path is None:
        return None
    summary = report_path.parent / "summary.md"
    return summary if summary.exists() else None


def promotion_request_from_report(report: dict[str, Any], target: dict[str, Any]) -> dict[str, Any] | None:
    decisions = list(report.get("supervisor_decisions") or [])
    latest_decision = decisions[-1] if decisions else {}
    requeue = dict(latest_decision.get("requeue") or {})
    control_action = str(latest_decision.get("control_action") or "")
    stop_reason = str(report.get("stop_reason") or "")
    theorem = (
        str(requeue.get("next_target_theorem") or "").strip()
        or str(latest_decision.get("target_theorem") or "").strip()
        or str(report.get("current_target_theorem") or "").strip()
        or str(target["lean"].get("fallback_target") or "").strip()
    )
    requested = bool(requeue.get("required")) or stop_reason == "supervisor_missing_formalizer_config"
    requested = requested or "lean" in control_action or "formalizer" in control_action
    if not requested or not theorem:
        return None
    return {
        "target_slug": target["slug"],
        "problem": target["problem"],
        "target_theorem": theorem,
        "source_report_path": report.get("summary_path") or report.get("run_dir") or "",
        "stop_reason": stop_reason,
        "control_action": control_action,
        "decision_path": latest_decision.get("decision_path") or "",
        "instructions": latest_decision.get("next_work_direction") or "",
    }


def source_command(target: dict[str, Any], *, statement_path: Path, output_root: Path, run_name: str, seconds: int, contexts: list[str]) -> list[str]:
    cmd = [
        *command_prefix(seconds + 600, lean=False),
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
        str(max(60, seconds)),
        "--round-time-budget",
        str(SOURCE_ROUND_SECONDS),
        "--proof-attempts",
        "2",
        "--proof-audits",
        "1",
        "--proof-attempt-timeout",
        "1200",
        "--proof-audit-timeout",
        "600",
        "--proof-grounding-timeout",
        "600",
        "--initial-target-theorem",
        str(target["initial_target"]),
        "--final-target-theorem",
        str(target["final_target"]),
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
        run_name,
        "--reasoning-effort",
        "high",
    ]
    for context in contexts:
        if Path(context).exists() and not str(context).endswith(".lean"):
            cmd += ["--context-file", context]
    return cmd


def lean_command(
    target: dict[str, Any],
    *,
    theorem: str,
    statement_path: Path,
    output_root: Path,
    run_name: str,
    seconds: int,
    contexts: list[str],
) -> list[str]:
    lean = target["lean"]
    workspace = Path(lean["workspace"])
    target_file = Path(lean["target_file"])
    build_command = single_file_build_command(workspace, target_file)
    cmd = [
        *command_prefix(seconds + 600, lean=True),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_path),
        "--workspace",
        str(workspace),
        "--target-file",
        str(target_file),
        "--build-command",
        build_command,
        "--backend",
        "codex",
        "--search",
        "--mode",
        "lean-formalizer",
        "--rounds",
        "999",
        "--time-budget",
        str(max(60, seconds)),
        "--round-time-budget",
        str(LEAN_ROUND_SECONDS),
        "--formalizer-attempts",
        "3",
        "--formalizer-attempt-timeout",
        "1200",
        "--formalizer-build-timeout",
        "600",
        "--initial-target-theorem",
        theorem,
        "--final-target-theorem",
        theorem,
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
        str(output_root),
        "--run-name",
        run_name,
        "--reasoning-effort",
        "high",
    ]
    for context in contexts:
        if Path(context).exists():
            cmd += ["--context-file", context]
    return cmd


def serializable_job(job: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in job.items() if k != "proc"}


def update_status(status_path: Path, status: dict[str, Any], active_sources: list[dict[str, Any]], active_lean: list[dict[str, Any]], queue: list[dict[str, Any]]) -> None:
    payload = dict(status)
    payload["updated_at"] = utc_now()
    payload["active_sources"] = [serializable_job(item) for item in active_sources]
    payload["active_lean"] = [serializable_job(item) for item in active_lean]
    payload["promotion_queue"] = list(queue)
    write_json(status_path, payload)


def run_worker() -> None:
    prepare_targets()
    env = process_env()
    deadline = time.monotonic() + TIME_BUDGET_SECONDS
    status_path = RUN_ROOT / "queue_status.json"
    status: dict[str, Any] = {
        "started_at": utc_now(),
        "status": "running",
        "run_root": str(RUN_ROOT),
        "policy": {
            "source_parallelism": len(TARGETS),
            "lean_slot_limit": LEAN_SLOT_LIMIT,
            "source_mode": "run-campaign-loop proof-lab with supervisor every round",
            "lean_mode": "queued run-campaign-loop lean-formalizer",
            "build_policy": "single-file lake env lean only",
        },
        "completed_sources": [],
        "completed_lean": [],
        "events": [],
    }
    active_sources: list[dict[str, Any]] = []
    active_lean: list[dict[str, Any]] = []
    promotion_queue: list[dict[str, Any]] = []
    queued_keys: set[tuple[str, str]] = set()
    source_cycles: dict[str, int] = {target["slug"]: 0 for target in TARGETS}
    promotions_started: dict[str, int] = {target["slug"]: 0 for target in TARGETS}
    target_by_slug = {target["slug"]: target for target in TARGETS}

    def remaining_seconds() -> int:
        return max(0, int(deadline - time.monotonic()))

    def start_source(target: dict[str, Any], extra_contexts: list[str] | None = None, extra_note: str = "") -> None:
        if remaining_seconds() < 300:
            return
        slug = target["slug"]
        source_cycles[slug] += 1
        cycle = source_cycles[slug]
        statement_path = RUN_ROOT / "source_statements" / f"{slug}-cycle-{cycle:02d}.md"
        output_root = RUN_ROOT / "source_runs" / slug
        run_name = f"{slug}-source-cycle-{cycle:02d}"
        log_path = RUN_ROOT / "logs" / f"source-{slug}-cycle-{cycle:02d}.log"
        contexts = list(target.get("source_contexts") or []) + list(extra_contexts or [])
        write_text(statement_path, source_statement(target, cycle, extra_note=extra_note))
        cmd = source_command(
            target,
            statement_path=statement_path,
            output_root=output_root,
            run_name=run_name,
            seconds=remaining_seconds(),
            contexts=contexts,
        )
        proc = launch_process(cmd, log_path=log_path, env=env)
        job = {
            "kind": "source",
            "slug": slug,
            "cycle": cycle,
            "pid": proc.pid,
            "started_at": utc_now(),
            "statement_path": str(statement_path),
            "output_root": str(output_root),
            "run_name": run_name,
            "log_path": str(log_path),
            "proc": proc,
        }
        active_sources.append(job)
        status["events"].append({"time": utc_now(), "event": "source_started", "slug": slug, "cycle": cycle, "pid": proc.pid})

    def start_lean(request: dict[str, Any]) -> None:
        if remaining_seconds() < 600:
            return
        slug = request["target_slug"]
        target = target_by_slug[slug]
        promotions_started[slug] += 1
        idx = promotions_started[slug]
        theorem = str(request["target_theorem"])
        source_report_path = Path(str(request.get("source_report_path") or ""))
        if source_report_path.is_dir():
            source_report = source_report_path / "report.json"
        elif source_report_path.name == "summary.md":
            source_report = source_report_path.parent / "report.json"
        else:
            source_report = source_report_path if source_report_path.exists() else None
        source_summary = latest_summary_for_report(source_report)
        statement_path = RUN_ROOT / "lean_statements" / f"{slug}-promotion-{idx:02d}.md"
        output_root = RUN_ROOT / "lean_runs" / slug
        run_name = f"{slug}-lean-promotion-{idx:02d}"
        log_path = RUN_ROOT / "logs" / f"lean-{slug}-promotion-{idx:02d}.log"
        contexts = list(target["lean"].get("contexts") or [])
        if source_report and source_report.exists():
            contexts.append(str(source_report))
        if source_summary and source_summary.exists():
            contexts.append(str(source_summary))
        decision_path = str(request.get("decision_path") or "")
        if decision_path and Path(decision_path).exists():
            contexts.append(decision_path)
        write_text(statement_path, lean_statement(target, theorem, source_report))
        cmd = lean_command(
            target,
            theorem=theorem,
            statement_path=statement_path,
            output_root=output_root,
            run_name=run_name,
            seconds=remaining_seconds(),
            contexts=contexts,
        )
        proc = launch_process(cmd, log_path=log_path, env=env)
        job = {
            "kind": "lean",
            "slug": slug,
            "promotion_index": idx,
            "pid": proc.pid,
            "started_at": utc_now(),
            "target_theorem": theorem,
            "statement_path": str(statement_path),
            "output_root": str(output_root),
            "run_name": run_name,
            "log_path": str(log_path),
            "source_request": request,
            "proc": proc,
        }
        active_lean.append(job)
        status["events"].append({"time": utc_now(), "event": "lean_started", "slug": slug, "promotion": idx, "pid": proc.pid, "target_theorem": theorem})

    for target in TARGETS:
        start_source(target)
    update_status(status_path, status, active_sources, active_lean, promotion_queue)

    try:
        while time.monotonic() < deadline:
            for job in list(active_sources):
                proc = job["proc"]
                rc = proc.poll()
                if rc is None:
                    continue
                active_sources.remove(job)
                report_path = latest_report(Path(job["output_root"]))
                report = read_json(report_path)
                job_done = serializable_job(job)
                job_done.update(
                    {
                        "finished_at": utc_now(),
                        "returncode": rc,
                        "report_path": str(report_path or ""),
                        "summary_path": str(latest_summary_for_report(report_path) or ""),
                        "stop_reason": report.get("stop_reason") or "",
                        "status": report.get("status") or ("completed" if rc == 0 else "failed"),
                    }
                )
                status["completed_sources"].append(job_done)
                target = target_by_slug[job["slug"]]
                request = promotion_request_from_report(report, target)
                if request:
                    key = (request["target_slug"], request["target_theorem"])
                    if key not in queued_keys and promotions_started[request["target_slug"]] < MAX_PROMOTIONS_PER_TARGET:
                        queued_keys.add(key)
                        promotion_queue.append(request)
                        status["events"].append({"time": utc_now(), "event": "promotion_queued", **request})
                elif source_cycles[job["slug"]] < MAX_SOURCE_CYCLES_PER_TARGET and remaining_seconds() > 1800:
                    extra_contexts = [p for p in [job_done.get("report_path"), job_done.get("summary_path")] if p]
                    start_source(
                        target,
                        extra_contexts=extra_contexts,
                        extra_note=(
                            "The previous supervised source cycle did not pass the promotion gate. "
                            "Continue in proof-lab/source mode, use the prior report as context, "
                            "and request Lean promotion only for a genuinely local wrapper/certificate."
                        ),
                    )
                status["events"].append({"time": utc_now(), "event": "source_finished", "slug": job["slug"], "cycle": job["cycle"], "returncode": rc})

            for job in list(active_lean):
                proc = job["proc"]
                rc = proc.poll()
                if rc is None:
                    continue
                active_lean.remove(job)
                report_path = latest_report(Path(job["output_root"]))
                report = read_json(report_path)
                job_done = serializable_job(job)
                job_done.update(
                    {
                        "finished_at": utc_now(),
                        "returncode": rc,
                        "report_path": str(report_path or ""),
                        "summary_path": str(latest_summary_for_report(report_path) or ""),
                        "stop_reason": report.get("stop_reason") or "",
                        "status": report.get("status") or ("completed" if rc == 0 else "failed"),
                    }
                )
                status["completed_lean"].append(job_done)
                status["events"].append({"time": utc_now(), "event": "lean_finished", "slug": job["slug"], "promotion": job["promotion_index"], "returncode": rc})
                if (
                    source_cycles[job["slug"]] < MAX_SOURCE_CYCLES_PER_TARGET
                    and remaining_seconds() > 1800
                    and str(report.get("status") or "") != "verified"
                ):
                    extra_contexts = [p for p in [job_done.get("report_path"), job_done.get("summary_path")] if p]
                    start_source(
                        target_by_slug[job["slug"]],
                        extra_contexts=extra_contexts,
                        extra_note=f"Previous queued Lean promotion `{job['target_theorem']}` finished with status `{job_done['status']}` and stop reason `{job_done['stop_reason']}`. Reassess the main route before requesting any further promotion.",
                    )

            while promotion_queue and len(active_lean) < LEAN_SLOT_LIMIT and remaining_seconds() > 600:
                request = promotion_queue.pop(0)
                start_lean(request)

            update_status(status_path, status, active_sources, active_lean, promotion_queue)
            if not active_sources and not active_lean and not promotion_queue:
                break
            time.sleep(20)
    finally:
        if time.monotonic() >= deadline:
            status["events"].append({"time": utc_now(), "event": "deadline_reached"})
        for job in active_sources + active_lean:
            stop_process(job["proc"])
            status["events"].append({"time": utc_now(), "event": "terminated_at_shutdown", "slug": job["slug"], "kind": job["kind"], "pid": job["pid"]})
        active_sources.clear()
        active_lean.clear()
        status["finished_at"] = utc_now()
        status["status"] = "completed"
        update_status(status_path, status, active_sources, active_lean, promotion_queue)


def launch() -> dict[str, Any]:
    prepare_targets()
    for sub in ("logs", "source_statements", "lean_statements", "source_runs", "lean_runs"):
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "targets": [
            {
                "slug": target["slug"],
                "problem": target["problem"],
                "final_target": target["final_target"],
                "initial_target": target["initial_target"],
                "lean_workspace": str(target["lean"]["workspace"]),
                "lean_target_file": str(target["lean"]["target_file"]),
                "lean_build_command": single_file_build_command(Path(target["lean"]["workspace"]), Path(target["lean"]["target_file"])),
            }
            for target in TARGETS
        ],
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    scheduler_log = RUN_ROOT / "logs/scheduler.log"
    with scheduler_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, __file__, "--worker"],
            cwd=REPO,
            env=process_env(),
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    payload = {
        "run_root": str(RUN_ROOT),
        "scheduler_pid": proc.pid,
        "scheduler_log": str(scheduler_log),
        "manifest_path": str(RUN_ROOT / "manifest.json"),
        "queue_status_path": str(RUN_ROOT / "queue_status.json"),
        "source_target_count": len(TARGETS),
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "mode": "5 supervised proof-lab campaigns plus queued lean-formalizer promotions",
    }
    write_text(RUN_ROOT / "scheduler.pid", str(proc.pid))
    write_json(RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    if "--worker" in sys.argv:
        run_worker()
        return
    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
