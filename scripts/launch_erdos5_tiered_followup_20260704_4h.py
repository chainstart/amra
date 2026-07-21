#!/usr/bin/env python3
"""Tiered 2026-07-04 follow-up for the five Erdos source campaigns.

This launcher reuses the strict supervised queue machinery from the 2026-07-04
run, but changes the scheduling policy from equal five-way iteration to a
ranked source plan:

- #866 is the main target.
- #212 is the second target.
- #1052 is an evidence/certificate inventory.
- #972 and #1084 receive only short source/governance checks.

Lean promotion remains limited to two global slots and must pass the strict
local-wrapper/certificate gate inherited from the prior launcher.
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
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_tiered_followup_20260704_4h"
PREV_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260704_4h"

TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
LEAN_SLOT_LIMIT = 2
MAX_PROMOTIONS_PER_TARGET = 1


TIER_PLAN: dict[str, dict[str, Any]] = {
    "erdos866-g6-ces75": {
        "budget_seconds": 2 * 60 * 60,
        "max_cycles": 6,
        "priority": 1,
        "initial_target": "CES75EvenCountDichotomyResidualTailBoundSourceStatement",
    },
    "erdos212-rational-distance-density": {
        "budget_seconds": 60 * 60,
        "max_cycles": 4,
        "priority": 2,
        "initial_target": "ProjectiveVarietyWeakLangConditionalRationalDistanceNondensityPackage",
    },
    "erdos1052-unitary-perfect": {
        "budget_seconds": 40 * 60,
        "max_cycles": 3,
        "priority": 3,
        "initial_target": "unitaryPerfect_certificate_inventory_source",
    },
    "erdos972-beatty-prime-pair": {
        "budget_seconds": 10 * 60,
        "max_cycles": 1,
        "priority": 4,
        "initial_target": "BeattyPrimePairLambdaLambdaLowerBoundSource",
    },
    "erdos1084-harborth-triangular": {
        "budget_seconds": 10 * 60,
        "max_cycles": 1,
        "priority": 5,
        "initial_target": "HarborthContactNumberSourceImportMechanism.external_source_certificate_v2",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_20260704_launcher() -> Any:
    spec = importlib.util.spec_from_file_location("erdos5_queue_20260704", BASE_LAUNCHER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base launcher: {BASE_LAUNCHER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def latest_existing(*paths: str | Path) -> list[str]:
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
    base.LEAN_SLOT_LIMIT = LEAN_SLOT_LIMIT
    base.MAX_PROMOTIONS_PER_TARGET = MAX_PROMOTIONS_PER_TARGET
    base.MAX_SOURCE_CYCLES_PER_TARGET = max(plan["max_cycles"] for plan in TIER_PLAN.values())

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": TIER_PLAN["erdos866-g6-ces75"]["initial_target"],
            "statement": """\
# Erdos #866: CES75 residual-tail source certificate

This is the main target of the tiered follow-up.  The verified local wrapper
`ces75_theorem4_even_count_case_reduction_from_source` must not be repeated.

Current first blocker: source certification of the CES75 residual central-even
dichotomy.  Produce a provenance-stable certificate from the CES75 PDF:
- Lemma A/corollary at `k = 5`;
- Theorem 4 central-even step;
- strict residual endpoint `(t : R) < n / 100`;
- inclusive central filter `40*t <= x <= 2*n - 40*t`;
- lower tail with `N = 20*t`;
- reflected upper tail via `x -> 2*n + 2 - x`;
- direct six-witness branch for `n / 100 <= t`;
- thresholds absorbed into existential `Nces`, while enlarging `cCES` so
  `24 < cCES`.

Do not request Lean promotion unless a genuinely local wrapper/certificate
remains after the CES75 source statement is fixed.
""",
            "source_contexts": latest_existing(
                PREV_ROOT / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-06/summary.md",
                PREV_ROOT / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-06/supervisor/round-001/decision.md",
                PREV_ROOT / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-04/summary.md",
                PREV_ROOT / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-04/supervisor/round-011/decision.md",
                "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos866-ces75-corollary-source-cert-phase2/erdos866-ces75-corollary-source-cert-phase2-4h/summary.md",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": TIER_PLAN["erdos212-rational-distance-density"]["initial_target"],
            "statement": """\
# Erdos #212: projective-variety Weak Lang conditional package

This is the second target of the tiered follow-up.  Do not re-promote the
already verified bridge
`ShaffafSolymosiDeZeeuwContainmentForRationalDistanceSetsAssumingBombieriLang`.

The previous run narrowed the blocker: stop spending effort on the
smooth-projective-to-normal-singular transfer route unless exact AG references
appear.  Instead source-audit the direct Shaffaf/ABT package under the explicit
projective-variety Weak Lang/Bombieri-Lang hypothesis for projective varieties
of general type over number fields:
- Shaffaf normalization over `K = Q(sqrt k)`;
- six non-collinear anchor distance surface of general type;
- rational-distance lift to `K`-points;
- Weak Lang contradiction to Zariski density;
- Solymosi-de Zeeuw line/circle finite-exception collapse.

Current first blocker relative to `Erdos212.erdos_212` is still external Weak
Lang/Bombieri-Lang.  The useful output is a precise conditional source theorem,
not Lean glue.
""",
            "source_contexts": latest_existing(
                PREV_ROOT / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/summary.md",
                PREV_ROOT / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/supervisor/round-005/decision.md",
                PREV_ROOT / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-02/summary.md",
                PREV_ROOT / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-02/supervisor/round-005/decision.md",
            ),
        }
    )

    by_slug["erdos1052-unitary-perfect"].update(
        {
            "initial_target": TIER_PLAN["erdos1052-unitary-perfect"]["initial_target"],
            "statement": """\
# Erdos #1052: unitary perfect certificate inventory

This follow-up is not a proof push.  Treat the exact-balance seed-closure route,
the `threeHiggs_phi4p_eventual_failure` tail, `H_even`, and bare global omega
or 2-adic exponent bounds as frozen unless a new source supplies concrete
cutoffs and verifier obligations.

Current task: inventory importable evidence for `Erdos1052.erdos_1052`.
Identify exact ancillary files, factor/primality transcripts, verifier scripts,
cutoff ranges, and theorem obligations.  Separate bounded-box coverage from the
remaining global tail.  If no explicit cutoff/certificate/source theorem is
found, produce a clean freeze package.
""",
            "source_contexts": latest_existing(
                PREV_ROOT / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-06/summary.md",
                PREV_ROOT / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-06/supervisor/round-001/decision.md",
                PREV_ROOT / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-04/summary.md",
                PREV_ROOT / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-04/supervisor/round-005/decision.md",
            ),
        }
    )

    by_slug["erdos972-beatty-prime-pair"].update(
        {
            "initial_target": TIER_PLAN["erdos972-beatty-prime-pair"]["initial_target"],
            "statement": """\
# Erdos #972: short Beatty prime-pair source check

This is a short frozen-route verification, not a broad attack.  The verified
conditional bridge must not be repeated.

Search only for an exact primary theorem proving, for every irrational
`alpha > 1`, a Beatty prime-pair lower bound such as
`#{p < X | Prime p and Prime floor(alpha*p)} >>_alpha X/(log X)^2`, or an
equivalent positive von Mangoldt/Lambda-Lambda correlation strong enough to
give infinitely many witnesses.  If no such source with matching hypotheses and
floor convention is found, keep the route frozen.
""",
            "source_contexts": latest_existing(
                PREV_ROOT / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-06/summary.md",
                PREV_ROOT / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-06/supervisor/round-001/decision.md",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": TIER_PLAN["erdos1084-harborth-triangular"]["initial_target"],
            "statement": """\
# Erdos #1084: short Harborth source/governance check

This is a short source/governance verification, not a Lean attack.  Do not queue
`Erdos1084.harborth_unitDistNum_upper_ge4`.

The only useful next step is external certification: either obtain/check
Harborth, *Loesung zu Problem 664A*, Elem. Math. 29 (1974), 14-15, or record
explicit AMRA approval that Bezdek-Khan Theorem 3.1 is acceptable provenance for
`forall n >= 2, c(n,2) = floor(3n - sqrt(12n - 3))`, with simple unordered
contact edges for finite non-overlapping congruent planar disks.  Preserve the
scaling bridge `x -> 2x` and the local `unitDistNum` convention.
""",
            "source_contexts": latest_existing(
                PREV_ROOT / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-06/summary.md",
                PREV_ROOT / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-06/supervisor/round-002/decision.md",
            ),
        }
    )

    for target in base.TARGETS:
        target["tier_plan"] = dict(TIER_PLAN[target["slug"]])

    base.TARGETS.sort(key=lambda target: target["tier_plan"]["priority"])
    return base


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


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
    for sub in ("logs", "source_statements", "lean_statements", "source_runs", "lean_runs"):
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)

    env = base.process_env()
    deadline = time.monotonic() + TIME_BUDGET_SECONDS
    status_path = RUN_ROOT / "queue_status.json"
    target_by_slug = {target["slug"]: target for target in base.TARGETS}
    stats: dict[str, dict[str, Any]] = {
        target["slug"]: {
            "cycles_started": 0,
            "spent_seconds": 0,
            "budget_seconds": target["tier_plan"]["budget_seconds"],
            "max_cycles": target["tier_plan"]["max_cycles"],
            "priority": target["tier_plan"]["priority"],
        }
        for target in base.TARGETS
    }
    active_sources: list[dict[str, Any]] = []
    active_lean: list[dict[str, Any]] = []
    promotion_queue: list[dict[str, Any]] = []
    queued_keys: set[tuple[str, str]] = set()
    promotions_started: dict[str, int] = {target["slug"]: 0 for target in base.TARGETS}
    bonus_866_started = False
    status: dict[str, Any] = {
        "started_at": utc_now(),
        "status": "running",
        "run_root": str(RUN_ROOT),
        "tier_plan": TIER_PLAN,
        "policy": {
            "source_mode": "tiered supervised run-campaign-loop proof-lab",
            "lean_mode": "strict queued run-campaign-loop lean-formalizer",
            "lean_slot_limit": LEAN_SLOT_LIMIT,
            "build_policy": "single-file lake env lean only",
            "fallback": "unused wall time is returned to #866 before deadline",
        },
        "target_stats": stats,
        "completed_sources": [],
        "completed_lean": [],
        "events": [],
    }

    def remaining_seconds() -> int:
        return max(0, int(deadline - time.monotonic()))

    def update_status() -> None:
        payload = dict(status)
        payload["updated_at"] = utc_now()
        payload["active_sources"] = [serializable_job(job) for job in active_sources]
        payload["active_lean"] = [serializable_job(job) for job in active_lean]
        payload["promotion_queue"] = list(promotion_queue)
        write_json(status_path, payload)

    def target_seconds_left(slug: str) -> int:
        stat = stats[slug]
        return max(0, int(stat["budget_seconds"] - stat["spent_seconds"]))

    def can_continue(slug: str) -> bool:
        stat = stats[slug]
        return (
            stat["cycles_started"] < stat["max_cycles"]
            and target_seconds_left(slug) >= 180
            and remaining_seconds() >= 300
        )

    def start_source(target: dict[str, Any], *, seconds: int, extra_contexts: list[str] | None = None, extra_note: str = "") -> None:
        slug = target["slug"]
        stats[slug]["cycles_started"] += 1
        cycle = stats[slug]["cycles_started"]
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
            seconds=max(180, seconds),
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

    def start_lean(request: dict[str, Any]) -> None:
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
        source_summary = base.latest_summary_for_report(source_report)
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
        write_text(statement_path, base.lean_statement(target, theorem, source_report))
        cmd = base.lean_command(
            target,
            theorem=theorem,
            statement_path=statement_path,
            output_root=output_root,
            run_name=run_name,
            seconds=remaining_seconds(),
            contexts=contexts,
        )
        proc = base.launch_process(cmd, log_path=log_path, env=env)
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

    for target in base.TARGETS:
        slug = target["slug"]
        seconds = min(target_seconds_left(slug), remaining_seconds())
        start_source(target, seconds=seconds)
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
                stats[job["slug"]]["spent_seconds"] += elapsed
                report_path = base.latest_report(Path(job["output_root"]))
                report = base.read_json(report_path)
                job_done = serializable_job(job)
                job_done.update(
                    {
                        "finished_at": utc_now(),
                        "elapsed_seconds": elapsed,
                        "returncode": rc,
                        "report_path": str(report_path or ""),
                        "summary_path": str(base.latest_summary_for_report(report_path) or ""),
                        "stop_reason": report.get("stop_reason") or "",
                        "status": report.get("status") or ("completed" if rc == 0 else "failed"),
                    }
                )
                status["completed_sources"].append(job_done)
                status["events"].append({"time": utc_now(), "event": "source_finished", "slug": job["slug"], "cycle": job["cycle"], "returncode": rc, "elapsed_seconds": elapsed})
                target = target_by_slug[job["slug"]]
                request = base.promotion_request_from_report(report, target)
                if request:
                    key = (request["target_slug"], request["target_theorem"])
                    if key not in queued_keys and promotions_started[request["target_slug"]] < MAX_PROMOTIONS_PER_TARGET:
                        queued_keys.add(key)
                        promotion_queue.append(request)
                        status["events"].append({"time": utc_now(), "event": "promotion_queued", **request})
                elif can_continue(job["slug"]):
                    seconds = min(target_seconds_left(job["slug"]), remaining_seconds())
                    extra_contexts = [p for p in [job_done.get("report_path"), job_done.get("summary_path")] if p]
                    start_source(
                        target,
                        seconds=seconds,
                        extra_contexts=extra_contexts,
                        extra_note=(
                            "The previous tiered source cycle did not pass the strict promotion gate. "
                            "Continue only on the current first blocker and request Lean promotion only "
                            "for a genuinely local wrapper/certificate."
                        ),
                    )

            for job in list(active_lean):
                proc = job["proc"]
                rc = proc.poll()
                if rc is None:
                    continue
                active_lean.remove(job)
                report_path = base.latest_report(Path(job["output_root"]))
                report = base.read_json(report_path)
                job_done = serializable_job(job)
                job_done.update(
                    {
                        "finished_at": utc_now(),
                        "returncode": rc,
                        "report_path": str(report_path or ""),
                        "summary_path": str(base.latest_summary_for_report(report_path) or ""),
                        "stop_reason": report.get("stop_reason") or "",
                        "status": report.get("status") or ("completed" if rc == 0 else "failed"),
                    }
                )
                status["completed_lean"].append(job_done)
                status["events"].append({"time": utc_now(), "event": "lean_finished", "slug": job["slug"], "promotion": job["promotion_index"], "returncode": rc})

            while promotion_queue and len(active_lean) < LEAN_SLOT_LIMIT and remaining_seconds() > 600:
                start_lean(promotion_queue.pop(0))

            if not active_sources and not active_lean and not promotion_queue:
                if not bonus_866_started and remaining_seconds() > 1800:
                    bonus_866_started = True
                    target = target_by_slug["erdos866-g6-ces75"]
                    status["events"].append({"time": utc_now(), "event": "bonus_mainline_866_started", "remaining_seconds": remaining_seconds()})
                    start_source(
                        target,
                        seconds=remaining_seconds(),
                        extra_note=(
                            "All tiered allocation caps finished before the wall-clock deadline. "
                            "Use the remaining time on the #866 mainline CES75 source certificate."
                        ),
                    )
                else:
                    break

            update_status()
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
        update_status()


def launch() -> dict[str, Any]:
    base = configure_base()
    base.prepare_targets()
    for sub in ("logs", "source_statements", "lean_statements", "source_runs", "lean_runs"):
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "tier_plan": TIER_PLAN,
        "promotion_gate": "strict inherited 20260704 gate: local wrappers/certificates only",
        "targets": [
            {
                "slug": target["slug"],
                "problem": target["problem"],
                "final_target": target["final_target"],
                "initial_target": target["initial_target"],
                "budget_seconds": target["tier_plan"]["budget_seconds"],
                "max_cycles": target["tier_plan"]["max_cycles"],
                "priority": target["tier_plan"]["priority"],
                "lean_workspace": str(target["lean"]["workspace"]),
                "lean_target_file": str(target["lean"]["target_file"]),
                "lean_build_command": base.single_file_build_command(Path(target["lean"]["workspace"]), Path(target["lean"]["target_file"])),
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
        "source_target_count": len(TIER_PLAN),
        "lean_slot_limit": LEAN_SLOT_LIMIT,
        "mode": "tiered supervised proof-lab campaigns plus strict queued lean-formalizer promotions",
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
