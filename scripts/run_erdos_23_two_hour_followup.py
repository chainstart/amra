#!/usr/bin/env python3
"""Run resumable, source-aware proof attacks on the 23 priority Erdős routes.

Each problem receives its own Codex session and workspace.  The two-hour value
is a hard ceiling, not a target that must be exhausted.  Results are stored as
schema-validated JSON so interrupted runs can resume without repeating closed
shards.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
INITIAL_ROOT = REPO_ROOT / "artifacts/erdos_630_initial_analysis"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts/erdos_followup_20260719/proof_routes"
PRIORITY_IDS = [
    "952",
    "1083",
    "1039",
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


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def output_schema() -> dict[str, Any]:
    source = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "url": {"type": "string"},
            "primary_source": {"type": "boolean"},
            "verified_claim_zh": {"type": "string"},
        },
        "required": ["title", "url", "primary_source", "verified_claim_zh"],
        "additionalProperties": False,
    }
    attempt = {
        "type": "object",
        "properties": {
            "label_zh": {"type": "string"},
            "method_zh": {"type": "string"},
            "derivation_zh": {"type": "string"},
            "outcome": {
                "type": "string",
                "enum": ["advanced", "blocked", "refuted", "inconclusive"],
            },
        },
        "required": ["label_zh", "method_zh", "derivation_zh", "outcome"],
        "additionalProperties": False,
    }
    computation = {
        "type": "object",
        "properties": {
            "artifact_path": {"type": "string"},
            "description_zh": {"type": "string"},
            "reproduce_command": {"type": "string"},
            "result_zh": {"type": "string"},
        },
        "required": [
            "artifact_path",
            "description_zh",
            "reproduce_command",
            "result_zh",
        ],
        "additionalProperties": False,
    }
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "problem_id": {"type": "string"},
            "statement_scope_zh": {"type": "string"},
            "route_goal_zh": {"type": "string"},
            "sources_checked": {"type": "array", "items": source},
            "attempts": {"type": "array", "items": attempt},
            "rigorous_progress_zh": {"type": "array", "items": {"type": "string"}},
            "falsification_checks_zh": {"type": "array", "items": {"type": "string"}},
            "computational_artifacts": {"type": "array", "items": computation},
            "blocking_step_zh": {"type": "string"},
            "next_theorem_zh": {"type": "string"},
            "conclusion": {
                "type": "string",
                "enum": [
                    "route_advanced",
                    "route_blocked",
                    "route_refuted",
                    "candidate_full_proof",
                    "candidate_counterexample",
                ],
            },
            "full_solution_claim": {
                "type": "string",
                "enum": [
                    "none",
                    "candidate_requires_independent_review",
                    "machine_checked_exact_scope_closure_evidence",
                ],
            },
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "proof_note_zh": {"type": "string"},
        },
        "required": [
            "problem_id",
            "statement_scope_zh",
            "route_goal_zh",
            "sources_checked",
            "attempts",
            "rigorous_progress_zh",
            "falsification_checks_zh",
            "computational_artifacts",
            "blocking_step_zh",
            "next_theorem_zh",
            "conclusion",
            "full_solution_claim",
            "confidence",
            "proof_note_zh",
        ],
        "additionalProperties": False,
    }


def load_inputs() -> dict[str, dict[str, Any]]:
    cohort_payload = read_json(INITIAL_ROOT / "cohort.json", default={})
    cohort = {
        row["problem_id"]: row for row in cohort_payload.get("problems", [])
    }
    inputs: dict[str, dict[str, Any]] = {}
    for problem_id in PRIORITY_IDS:
        initial = read_json(INITIAL_ROOT / "results" / f"{problem_id}.json", default={})
        if problem_id not in cohort or not initial.get("analysis"):
            raise RuntimeError(f"Missing initial material for Erdős #{problem_id}")
        inputs[problem_id] = {
            "cohort": cohort[problem_id],
            "initial": initial["analysis"],
        }
    return inputs


def build_prompt(problem_id: str, payload: dict[str, Any], work_dir: Path) -> str:
    cohort = payload["cohort"]
    initial = payload["initial"]
    return (
        "你正在对一条 Erdős 开放问题优先路线做一次真实的、最长两小时的续攻。"
        "两小时是硬上限；若路线被严格反驳或已得到清晰的下一定理，可以提前结束。\n\n"
        "这不是泛泛的研究建议任务。请实际推导、检查边界情形、尝试反例、搜索并核对一手文献；"
        "适合计算的路线应编写并运行小程序或证书。先尝试证伪初始路线，再推进幸存部分。"
        "不得把相似定理、特例、启发式或模型生成文字写成完整证明。只有当精确题面的全部量词"
        "逐项闭合时，才可使用 candidate_full_proof/candidate_counterexample，而且仍必须标为待独立审稿。\n\n"
        "实时检索只采用一手来源：论文正文、期刊/DOI 页面、arXiv、作者仓库或可检查的 Lean 代码。"
        "给出定理编号或精确命题范围；找不到就明确说找不到。可以读取整个仓库 "
        f"{REPO_ROOT}，但不要修改仓库源码或 FormalConjectures。若需创建计算脚本、表格或草稿，"
        f"只能写入本题工作目录 {work_dir}，并在 computational_artifacts 中给出可复现命令。\n\n"
        "输出使用中文，保留必要 LaTeX。proof_note_zh 应是一份自洽的数学研究记录，包含关键公式，"
        "而不只是其他字段的重复。\n\n"
        "输入材料（旧分析是不可信的起点，必须独立复核）：\n"
        + json.dumps(
            {
                "problem_id": problem_id,
                "current_status": cohort.get("current_status"),
                "exact_statement": cohort.get("statement"),
                "official_context": cohort.get("official_context"),
                "official_url": cohort.get("official_url"),
                "domain": cohort.get("domain"),
                "tags": cohort.get("tags"),
                "formal_conjecture_file": cohort.get("formal_conjecture_file"),
                "initial_attempt": initial,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def invoke_problem(
    *,
    problem_id: str,
    payload: dict[str, Any],
    output_root: Path,
    schema_path: Path,
    timeout_sec: int,
    model: str,
    reasoning_effort: str,
    run_schema_version: str = "amra.erdos_priority_two_hour.v1",
) -> dict[str, Any]:
    work_dir = output_root / "work" / problem_id
    run_dir = output_root / "runs" / problem_id
    work_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(problem_id, payload, work_dir)
    atomic_write_text(run_dir / "prompt.txt", prompt)
    raw_result = run_dir / "raw_result.json"
    command = [
        "codex",
        "--search",
        "-s",
        "workspace-write",
        "-a",
        "never",
    ]
    if model:
        command.extend(["--model", model])
    if reasoning_effort:
        command.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
    command.extend(
        [
            "exec",
            "--ephemeral",
            "-C",
            str(work_dir),
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(raw_result),
            prompt,
        ]
    )

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=work_dir,
            text=True,
            capture_output=True,
            timeout=timeout_sec,
            check=False,
        )
        backend_status = "completed" if completed.returncode == 0 else "failed"
        atomic_write_text(run_dir / "stdout.log", completed.stdout)
        atomic_write_text(run_dir / "stderr.log", completed.stderr)
    except subprocess.TimeoutExpired as exc:
        backend_status = "timeout"
        atomic_write_text(run_dir / "stdout.log", str(exc.stdout or ""))
        atomic_write_text(run_dir / "stderr.log", str(exc.stderr or ""))
    elapsed = round(time.monotonic() - started, 3)

    item = read_json(raw_result, default={})
    if item.get("problem_id") != problem_id:
        return {
            "problem_id": problem_id,
            "backend_status": backend_status,
            "elapsed_seconds": elapsed,
            "saved": False,
            "error": f"missing or mismatched structured result: {item.get('problem_id')!r}",
        }
    wrapped = {
        "schema_version": run_schema_version,
        "problem_id": problem_id,
        "backend_status": backend_status,
        "elapsed_seconds": elapsed,
        "hard_timeout_seconds": timeout_sec,
        "analysis": item,
    }
    atomic_write_json(output_root / "results" / f"{problem_id}.json", wrapped)
    return {
        "problem_id": problem_id,
        "backend_status": backend_status,
        "elapsed_seconds": elapsed,
        "saved": True,
        "conclusion": item.get("conclusion"),
    }


def render_summary(output_root: Path) -> dict[str, Any]:
    results = {}
    for path in (output_root / "results").glob("*.json"):
        payload = read_json(path, default={})
        if path.stem in PRIORITY_IDS and payload.get("analysis", {}).get("problem_id") == path.stem:
            results[path.stem] = payload
    pending = [problem_id for problem_id in PRIORITY_IDS if problem_id not in results]
    summary = {
        "schema_version": "amra.erdos_priority_two_hour_summary.v1",
        "expected_count": len(PRIORITY_IDS),
        "completed_count": len(results),
        "pending_ids": pending,
        "conclusions": dict(
            Counter(payload["analysis"].get("conclusion", "missing") for payload in results.values())
        ),
        "solution_claims": dict(
            Counter(
                payload["analysis"].get("full_solution_claim", "missing")
                for payload in results.values()
            )
        ),
        "total_elapsed_seconds": round(
            sum(float(payload.get("elapsed_seconds", 0)) for payload in results.values()), 3
        ),
        "max_elapsed_seconds": round(
            max((float(payload.get("elapsed_seconds", 0)) for payload in results.values()), default=0),
            3,
        ),
        "result_ids": [problem_id for problem_id in PRIORITY_IDS if problem_id in results],
    }
    atomic_write_json(output_root / "summary.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout-per-problem", type=int, default=7200)
    parser.add_argument("--ids", default="", help="Comma-separated subset; empty means all pending.")
    parser.add_argument("--model", default="")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--render-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    if args.render_only:
        print(json.dumps(render_summary(output_root), ensure_ascii=False, indent=2))
        return 0

    inputs = load_inputs()
    requested = {value.strip() for value in args.ids.split(",") if value.strip()}
    complete = {
        path.stem
        for path in (output_root / "results").glob("*.json")
        if read_json(path, default={}).get("analysis", {}).get("problem_id") == path.stem
    }
    pending = [
        problem_id
        for problem_id in PRIORITY_IDS
        if problem_id not in complete and (not requested or problem_id in requested)
    ]
    schema_path = output_root / "proof_followup.schema.json"
    atomic_write_json(schema_path, output_schema())
    lock = threading.Lock()
    completed_this_run = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(
                invoke_problem,
                problem_id=problem_id,
                payload=inputs[problem_id],
                output_root=output_root,
                schema_path=schema_path,
                timeout_sec=min(7200, max(1, args.timeout_per_problem)),
                model=args.model,
                reasoning_effort=args.reasoning_effort,
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
                atomic_write_json(output_root / "progress.json", progress)
                print(json.dumps(progress, ensure_ascii=False), flush=True)

    print(json.dumps(render_summary(output_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
