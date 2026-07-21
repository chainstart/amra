#!/usr/bin/env python3
"""#866-mainline follow-up for the five Erdos targets.

Scheduling policy:
- #866 runs as the main line until the four-hour wall-clock deadline, restarting
  source/proof-lab cycles whenever the supervisor stops on a source blocker.
- #212 receives one 45-minute conditional-source package pass.
- #1052, #972, and #1084 receive short maintenance/source-governance checks.
- This launcher does not start Lean promotion jobs.  The current expected work
  is source certification and theorem-specification, not local Lean repair.
"""

from __future__ import annotations

import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_LAUNCHER = REPO / "scripts/launch_erdos5_supervised_queue_20260704_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_866_mainline_20260704_4h"
PREV_TIERED = REPO / "artifacts/open_problem_screening/latest/erdos5_tiered_followup_20260704_4h"
PREV_QUEUE = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260704_4h"

TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
MAIN_SLUG = "erdos866-g6-ces75"

PLAN: dict[str, dict[str, Any]] = {
    "erdos866-g6-ces75": {
        "role": "main",
        "budget_seconds": TIME_BUDGET_SECONDS,
        "initial_target": "CES75K5EvenSequenceCorollarySourceCertificate",
    },
    "erdos212-rational-distance-density": {
        "role": "secondary",
        "budget_seconds": 45 * 60,
        "initial_target": "ProjectiveVarietyWeakLangConditionalRationalDistanceNondensityPackage",
    },
    "erdos1052-unitary-perfect": {
        "role": "maintenance",
        "budget_seconds": 15 * 60,
        "initial_target": "unitaryPerfect_certificate_inventory_source",
    },
    "erdos972-beatty-prime-pair": {
        "role": "maintenance",
        "budget_seconds": 10 * 60,
        "initial_target": "BeattyPrimePairLambdaLambdaLowerBoundSource",
    },
    "erdos1084-harborth-triangular": {
        "role": "maintenance",
        "budget_seconds": 10 * 60,
        "initial_target": "HarborthContactNumberSourceImportMechanism.external_source_certificate_v2",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_20260704_launcher() -> Any:
    spec = importlib.util.spec_from_file_location("erdos5_queue_20260704", BASE_LAUNCHER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base launcher: {BASE_LAUNCHER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def configure_base() -> Any:
    launcher = load_20260704_launcher()
    base = launcher.configure(launcher.load_base())
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = TIME_BUDGET_SECONDS
    base.HARD_TIMEOUT_SECONDS = HARD_TIMEOUT_SECONDS
    base.LEAN_SLOT_LIMIT = 0
    base.MAX_PROMOTIONS_PER_TARGET = 0
    base.MAX_SOURCE_CYCLES_PER_TARGET = 999

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": PLAN["erdos866-g6-ces75"]["initial_target"],
            "statement": """\
# Erdos #866: mainline CES75 k=5 even-sequence certificate

This is the main target for the full four-hour follow-up.  Do not repeat the
verified local wrapper `ces75_theorem4_even_count_case_reduction_from_source`.

Current first blocker:
`CES75K5EvenSequenceCorollarySourceCertificate`.

Produce a provenance-stable source certificate from Choi-Erdos-Szemeredi 1975:
- normalize Lemma A/corollary at `k = 5`;
- identify the hidden threshold `n0(5)`;
- justify the bound `32 * N^(31/32)`;
- verify that the six witnesses are distinct;
- translate the paper's strictly increasing positive even sequence convention
  to duplicate-free `Finset Z`;
- state how this smaller certificate feeds the direct branch `n/100 <= t`, the
  lower tail with `N = 20*t`, and the reflected upper tail `x -> 2*n + 2 - x`.

This is source/proof-lab work.  Do not request Lean promotion unless the CES75
source certificate is complete and only a genuinely local wrapper remains.
""",
            "source_contexts": existing(
                PREV_TIERED / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-07/summary.md",
                PREV_TIERED / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-07/supervisor/round-001/decision.md",
                PREV_TIERED / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-06/summary.md",
                PREV_QUEUE / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-06/summary.md",
                "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos866-ces75-corollary-source-cert-phase2/erdos866-ces75-corollary-source-cert-phase2-4h/summary.md",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": PLAN["erdos212-rational-distance-density"]["initial_target"],
            "statement": """\
# Erdos #212: secondary conditional source package

Do not re-promote the already verified bridge
`ShaffafSolymosiDeZeeuwContainmentForRationalDistanceSetsAssumingBombieriLang`.

Write the precise conditional source theorem under the projective-variety Weak
Lang/Bombieri-Lang hypothesis over number fields, with singular varieties
understood by desingularization/general-type convention.  Audit the direct
chain through ABT Proposition 3.6, Shaffaf's normalization/general-type context,
and Solymosi-de Zeeuw Theorems 2.1/2.2 for the line/circle finite-exception
collapse.

The first blocker remains external Weak Lang/Bombieri-Lang; this is source
theorem/spec work, not Lean promotion.
""",
            "source_contexts": existing(
                PREV_TIERED / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-02/summary.md",
                PREV_TIERED / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-02/supervisor/round-002/decision.md",
                PREV_QUEUE / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/summary.md",
            ),
        }
    )

    by_slug["erdos1052-unitary-perfect"].update(
        {
            "initial_target": PLAN["erdos1052-unitary-perfect"]["initial_target"],
            "statement": """\
# Erdos #1052: maintenance certificate inventory

Do not run a broad proof search.  Focus only on whether there is a primary
source or machine-checkable certificate with explicit cutoff `B` for the
`Phi_(4*p)(2)` prime-branch obstruction, plus finite verifier obligations for
`p <= B`.  Record bounded-box evidence separately from the unresolved global
tail.
""",
            "source_contexts": existing(
                PREV_TIERED / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-03/summary.md",
                PREV_TIERED / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-03/supervisor/round-001/decision.md",
            ),
        }
    )

    by_slug["erdos972-beatty-prime-pair"].update(
        {
            "initial_target": PLAN["erdos972-beatty-prime-pair"]["initial_target"],
            "statement": """\
# Erdos #972: maintenance Beatty prime-pair citation-chain check

Do not repeat the verified conditional bridge.  Audit only whether Li-Pan
cited-by/citation-chain sources contain an all-irrational `alpha > 1` Beatty
prime-pair lower bound or an equivalent positive Lambda-Lambda correlation with
the required floor convention.  If not, keep the route frozen.
""",
            "source_contexts": existing(
                PREV_TIERED / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-01/summary.md",
                PREV_TIERED / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-01/supervisor/round-001/decision.md",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": PLAN["erdos1084-harborth-triangular"]["initial_target"],
            "statement": """\
# Erdos #1084: maintenance Harborth provenance check

Do not queue Lean.  The only useful task is external certification: obtain/check
Harborth 1974 directly or record explicit AMRA approval that Bezdek-Khan
Theorem 3.1 is acceptable provenance for the planar contact-number theorem
under the local unordered `unitDistNum` convention and the scaling bridge
`x -> 2*x`.
""",
            "source_contexts": existing(
                PREV_TIERED / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-01/summary.md",
                PREV_TIERED / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-01/supervisor/round-001/decision.md",
            ),
        }
    )

    for target in base.TARGETS:
        target["mainline_plan"] = dict(PLAN[target["slug"]])
    base.TARGETS.sort(key=lambda target: 0 if target["slug"] == MAIN_SLUG else 1)
    return base


def serializable_job(job: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in job.items() if k not in {"proc", "started_monotonic"}}


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


def run_worker() -> None:
    base = configure_base()
    base.prepare_targets()
    for sub in ("logs", "source_statements", "source_runs"):
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)

    env = base.process_env()
    deadline = time.monotonic() + TIME_BUDGET_SECONDS
    status_path = RUN_ROOT / "queue_status.json"
    target_by_slug = {target["slug"]: target for target in base.TARGETS}
    active_sources: list[dict[str, Any]] = []
    source_cycles: dict[str, int] = {target["slug"]: 0 for target in base.TARGETS}
    spent_seconds: dict[str, int] = {target["slug"]: 0 for target in base.TARGETS}
    mainline_contexts: list[str] = []
    status: dict[str, Any] = {
        "started_at": utc_now(),
        "status": "running",
        "run_root": str(RUN_ROOT),
        "plan": PLAN,
        "policy": {
            "source_mode": "AMRA run-campaign-loop proof-lab with supervisor every round",
            "lean_mode": "disabled for this source-certificate round",
            "mainline": MAIN_SLUG,
            "mainline_rule": "restart #866 until hard deadline unless the proof/certificate is completed",
        },
        "completed_sources": [],
        "events": [],
    }

    def remaining_seconds() -> int:
        return max(0, int(deadline - time.monotonic()))

    def update_status() -> None:
        payload = dict(status)
        payload["updated_at"] = utc_now()
        payload["active_sources"] = [serializable_job(job) for job in active_sources]
        payload["source_cycles"] = source_cycles
        payload["spent_seconds"] = spent_seconds
        write_json(status_path, payload)

    def start_source(target: dict[str, Any], seconds: int, extra_contexts: list[str] | None = None, extra_note: str = "") -> None:
        slug = target["slug"]
        source_cycles[slug] += 1
        cycle = source_cycles[slug]
        statement_path = RUN_ROOT / "source_statements" / f"{slug}-cycle-{cycle:02d}.md"
        output_root = RUN_ROOT / "source_runs" / slug
        run_name = f"{slug}-source-cycle-{cycle:02d}"
        log_path = RUN_ROOT / "logs" / f"source-{slug}-cycle-{cycle:02d}.log"
        contexts = list(target.get("source_contexts") or []) + list(extra_contexts or [])
        write_text(statement_path, base.source_statement(target, cycle, extra_note=extra_note))
        cmd = base.source_command(
            target,
            statement_path=statement_path,
            output_root=output_root,
            run_name=run_name,
            seconds=max(300, min(seconds, remaining_seconds())),
            contexts=contexts,
        )
        proc = base.launch_process(cmd, log_path=log_path, env=env)
        job = {
            "kind": "source",
            "slug": slug,
            "cycle": cycle,
            "pid": proc.pid,
            "started_at": utc_now(),
            "started_monotonic": time.monotonic(),
            "budget_seconds": seconds,
            "statement_path": str(statement_path),
            "output_root": str(output_root),
            "run_name": run_name,
            "log_path": str(log_path),
            "proc": proc,
        }
        active_sources.append(job)
        status["events"].append({"time": utc_now(), "event": "source_started", "slug": slug, "cycle": cycle, "pid": proc.pid, "budget_seconds": seconds})

    for target in base.TARGETS:
        slug = target["slug"]
        budget = int(target["mainline_plan"]["budget_seconds"])
        seconds = remaining_seconds() if slug == MAIN_SLUG else min(budget, remaining_seconds())
        start_source(target, seconds)
    update_status()

    try:
        while time.monotonic() < deadline:
            for job in list(active_sources):
                proc = job["proc"]
                rc = proc.poll()
                if rc is None:
                    continue
                active_sources.remove(job)
                elapsed = max(1, int(time.monotonic() - job["started_monotonic"]))
                spent_seconds[job["slug"]] += elapsed
                report_path = base.latest_report(Path(job["output_root"]))
                report = base.read_json(report_path)
                summary_path = base.latest_summary_for_report(report_path)
                job_done = serializable_job(job)
                job_done.update(
                    {
                        "finished_at": utc_now(),
                        "elapsed_seconds": elapsed,
                        "returncode": rc,
                        "report_path": str(report_path or ""),
                        "summary_path": str(summary_path or ""),
                        "stop_reason": report.get("stop_reason") or "",
                        "status": report.get("status") or ("completed" if rc == 0 else "failed"),
                        "current_target_theorem": report.get("current_target_theorem") or "",
                    }
                )
                status["completed_sources"].append(job_done)
                status["events"].append({"time": utc_now(), "event": "source_finished", "slug": job["slug"], "cycle": job["cycle"], "returncode": rc, "elapsed_seconds": elapsed})
                if job["slug"] == MAIN_SLUG:
                    for path in (job_done.get("report_path"), job_done.get("summary_path")):
                        if path:
                            mainline_contexts.append(path)
                    if remaining_seconds() > 600 and str(report.get("status") or "") not in {"verified", "closed_candidate"}:
                        start_source(
                            target_by_slug[MAIN_SLUG],
                            remaining_seconds(),
                            extra_contexts=mainline_contexts[-6:],
                            extra_note=(
                                "Continue the #866 mainline until the four-hour hard deadline. "
                                "The previous cycle stopped before closing the source certificate; "
                                "focus only on `CES75K5EvenSequenceCorollarySourceCertificate`."
                            ),
                        )

            update_status()
            if not active_sources and remaining_seconds() <= 600:
                break
            if not active_sources and remaining_seconds() > 600:
                start_source(
                    target_by_slug[MAIN_SLUG],
                    remaining_seconds(),
                    extra_contexts=mainline_contexts[-6:],
                    extra_note="All side checks have ended; spend all remaining time on the #866 mainline certificate.",
                )
                update_status()
            time.sleep(20)
    finally:
        if time.monotonic() >= deadline:
            status["events"].append({"time": utc_now(), "event": "deadline_reached"})
        for job in active_sources:
            stop_process(job["proc"])
            status["events"].append({"time": utc_now(), "event": "terminated_at_shutdown", "slug": job["slug"], "pid": job["pid"]})
        active_sources.clear()
        status["finished_at"] = utc_now()
        status["status"] = "completed"
        update_status()


def launch() -> dict[str, Any]:
    base = configure_base()
    base.prepare_targets()
    for sub in ("logs", "source_statements", "source_runs"):
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "plan": PLAN,
        "targets": [
            {
                "slug": target["slug"],
                "problem": target["problem"],
                "final_target": target["final_target"],
                "initial_target": target["initial_target"],
                "role": target["mainline_plan"]["role"],
                "budget_seconds": target["mainline_plan"]["budget_seconds"],
            }
            for target in base.TARGETS
        ],
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    scheduler_log = RUN_ROOT / "logs/scheduler.log"
    with scheduler_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, __file__, "--worker"],
            cwd=REPO,
            env=base.process_env(),
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
        "mode": "#866 mainline source loop plus #212 secondary and short maintenance checks",
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
