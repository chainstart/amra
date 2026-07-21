#!/usr/bin/env python3
"""Run a second, resumable four-hour attack on the 22 non-#1039 priority routes.

This runner deliberately starts from the audited first-round result for each
problem.  It asks each agent for a delta rather than a restatement, preserves
per-problem workspaces, and uses a hard 14,400-second ceiling.
"""

from __future__ import annotations

import argparse
import json
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import run_erdos_23_two_hour_followup as base


REPO_ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_ROOT = REPO_ROOT / "artifacts/erdos_followup_20260719/proof_routes"
DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "artifacts/erdos_followup_20260719/proof_routes_round2_4h"
)
ROUND2_IDS = [
    "952",
    "1083",
    "25",
    "117",
    "143",
    "148",
    "256",
    "301",
    "325",
    "332",
    "377",
    "539",
    "635",
    "679",
    "686",
    "776",
    "788",
    "827",
    "934",
    "950",
    "963",
    "1063",
]
RUN_SCHEMA_VERSION = "amra.erdos_priority_four_hour_round2.v1"
SUMMARY_SCHEMA_VERSION = "amra.erdos_priority_four_hour_round2_summary.v1"
ORIGINAL_BUILD_PROMPT = base.build_prompt


def load_inputs() -> dict[str, dict[str, Any]]:
    base.PRIORITY_IDS = list(ROUND2_IDS)
    inputs = base.load_inputs()
    for problem_id, payload in inputs.items():
        previous = base.read_json(
            PREVIOUS_ROOT / "results" / f"{problem_id}.json", default={}
        )
        if previous.get("analysis", {}).get("problem_id") != problem_id:
            raise RuntimeError(f"Missing audited first-round result for Erdős #{problem_id}")
        payload["previous_round"] = previous
        verification = base.read_json(
            PREVIOUS_ROOT / f"{problem_id}_independent_verification.json", default={}
        )
        if verification:
            payload["independent_verification"] = verification
    return inputs


def build_prompt_round2(
    problem_id: str, payload: dict[str, Any], work_dir: Path
) -> str:
    prompt = ORIGINAL_BUILD_PROMPT(problem_id, payload, work_dir)
    prompt = prompt.replace(
        "一次真实的、最长两小时的续攻", "第二轮真实的、最长四小时的续攻"
    ).replace(
        "两小时是硬上限", "四小时（14400秒）是硬上限"
    )
    previous = payload["previous_round"]
    verification = payload.get("independent_verification")
    return (
        prompt
        + "\n\n第二轮专门要求：\n"
        "1. 第一轮结果已经过结构与部分独立数学审计；把它作为可挑战的起点，不能简单复述。"
        "先攻击其中的 blocking_step_zh 和 next_theorem_zh，并主动寻找能击穿上一轮结论的边界例。\n"
        "2. rigorous_progress_zh 只写本轮新增的严格结论；每项以“[第二轮新增]”或"
        "“[第二轮复核加固]”开头。若没有新增，必须明确写出尝试过的最窄命题、失败位置和"
        "可复现反例，并把 conclusion 设为 route_blocked 或 route_refuted。\n"
        "3. 不得把第一轮已有结论重新包装成新进展。任何更强界必须逐项比较指数、常数和量词；"
        "任何完整证明或反例必须覆盖官网精确题面，而不是只覆盖上一轮 next theorem。\n"
        "4. 可以继续读取第一轮 work 目录，但所有新脚本、证书和草稿只能写入当前第二轮工作目录 "
        f"{work_dir}。计算结果必须给出独立重算或至少两种实现的交叉检查。\n"
        "5. proof_note_zh 必须清楚分为“承接的第一轮事实”“第二轮新增推导”“仍未闭合的缺口”；"
        "来源成熟度和潜在文献优先权要单独说明。\n\n"
        "第一轮已审计结果：\n"
        + json.dumps(previous, ensure_ascii=False, indent=2)
        + (
            "\n\n第一轮独立复核记录：\n"
            + json.dumps(verification, ensure_ascii=False, indent=2)
            if verification
            else ""
        )
    )


def render_summary(output_root: Path) -> dict[str, Any]:
    results: dict[str, dict[str, Any]] = {}
    for path in (output_root / "results").glob("*.json"):
        payload = base.read_json(path, default={})
        if (
            path.stem in ROUND2_IDS
            and payload.get("analysis", {}).get("problem_id") == path.stem
        ):
            results[path.stem] = payload
    pending = [problem_id for problem_id in ROUND2_IDS if problem_id not in results]
    summary = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "expected_count": len(ROUND2_IDS),
        "completed_count": len(results),
        "pending_ids": pending,
        "conclusions": dict(
            Counter(
                payload["analysis"].get("conclusion", "missing")
                for payload in results.values()
            )
        ),
        "solution_claims": dict(
            Counter(
                payload["analysis"].get("full_solution_claim", "missing")
                for payload in results.values()
            )
        ),
        "backend_statuses": dict(
            Counter(payload.get("backend_status", "missing") for payload in results.values())
        ),
        "total_elapsed_seconds": round(
            sum(float(payload.get("elapsed_seconds", 0)) for payload in results.values()), 3
        ),
        "max_elapsed_seconds": round(
            max(
                (float(payload.get("elapsed_seconds", 0)) for payload in results.values()),
                default=0,
            ),
            3,
        ),
        "result_ids": [problem_id for problem_id in ROUND2_IDS if problem_id in results],
    }
    base.atomic_write_json(output_root / "summary.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout-per-problem", type=int, default=14400)
    parser.add_argument("--ids", default="", help="Comma-separated subset; empty means all pending.")
    parser.add_argument("--model", default="")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--render-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.timeout_per_problem <= 14400:
        raise SystemExit("--timeout-per-problem must be between 1 and 14400 seconds")
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    base.PRIORITY_IDS = list(ROUND2_IDS)
    base.build_prompt = build_prompt_round2
    if args.render_only:
        print(json.dumps(render_summary(output_root), ensure_ascii=False, indent=2))
        return 0

    inputs = load_inputs()
    requested = {value.strip() for value in args.ids.split(",") if value.strip()}
    unknown = requested - set(ROUND2_IDS)
    if unknown:
        raise SystemExit(f"Unknown round-two IDs: {sorted(unknown, key=int)}")
    complete = {
        path.stem
        for path in (output_root / "results").glob("*.json")
        if base.read_json(path, default={}).get("analysis", {}).get("problem_id")
        == path.stem
    }
    pending = [
        problem_id
        for problem_id in ROUND2_IDS
        if problem_id not in complete and (not requested or problem_id in requested)
    ]
    schema_path = output_root / "proof_followup.schema.json"
    base.atomic_write_json(schema_path, base.output_schema())
    lock = threading.Lock()
    completed_this_run = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(
                base.invoke_problem,
                problem_id=problem_id,
                payload=inputs[problem_id],
                output_root=output_root,
                schema_path=schema_path,
                timeout_sec=args.timeout_per_problem,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                run_schema_version=RUN_SCHEMA_VERSION,
            ): problem_id
            for problem_id in pending
        }
        for future in as_completed(futures):
            completed_this_run += 1
            try:
                last = future.result()
            except Exception as exc:
                last = {
                    "problem_id": futures[future],
                    "backend_status": "exception",
                    "saved": False,
                    "error": str(exc),
                }
            with lock:
                progress = {
                    "completed_this_run": completed_this_run,
                    "scheduled_this_run": len(pending),
                    "last": last,
                    "saved_total": len(list((output_root / "results").glob("*.json"))),
                }
                base.atomic_write_json(output_root / "progress.json", progress)
                print(json.dumps(progress, ensure_ascii=False), flush=True)

    print(json.dumps(render_summary(output_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
