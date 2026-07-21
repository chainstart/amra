#!/usr/bin/env python3
"""Run and render a resumable first-pass analysis of the frozen 630-problem Erdős cohort.

The repository's ``erdos_open_shortlist_refreshed.yaml`` is treated as a frozen
cohort, not as a claim that every entry is still open.  Current status metadata
and exact statements are supplied from explicit source snapshots.  Prior LLM
candidate solutions are included as untrusted material for an independent
audit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BANK = REPO_ROOT / "data/banks/erdos_open_shortlist_refreshed.yaml"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "artifacts/erdos_630_initial_analysis"
DEFAULT_REPORT = REPO_ROOT / "docs/erdos_630_initial_proof_paths.zh.md"

# These entries were no longer present in the January 2026 GPT-Erdos open
# snapshot.  The statements below were checked directly against
# erdosproblems.com on 2026-07-19.
DIRECT_STATEMENTS: dict[str, dict[str, str]] = {
    "205": {
        "latex": (
            r"Is it true that all sufficiently large $n$ can be written as $2^k+m$ for some "
            r"$k\geq 0$, where $\Omega(m)<\log\log m$? What about "
            r"$\Omega(m)<\epsilon\log\log m$, or another more slowly growing bound?"
        ),
        "additional_text": (
            "The current official page records a negative answer: infinitely many n force every "
            "n-2^k to have many prime factors. The odd-counterexample variant remains open."
        ),
    },
    "401": {
        "latex": (
            r"Is there $f(r)\to\infty$ such that, for infinitely many $n$, there are $a_1,a_2$ "
            r"with $a_1+a_2>n+f(r)\log n$ and "
            r"$a_1!a_2!\mid n!2^n3^n\cdots p_r^n$?"
        ),
        "additional_text": "The current official page records an affirmative proof and a Lean-verified status.",
    },
    "729": {
        "latex": (
            r"For every constant $C>0$, are there infinitely many $a,b,n$ with "
            r"$a+b>n+C\log n$ such that the denominator of $n!/(a!b!)$ contains only "
            r"primes bounded in terms of $C$?"
        ),
        "additional_text": "The current official page records an affirmative proof verified in Lean.",
    },
    "871": {
        "latex": (
            r"Let $A$ be an additive basis of order $2$ with "
            r"$1_A*1_A(n)\to\infty$. Must $A$ split into two disjoint additive bases of order $2$?"
        ),
        "additional_text": "The current official page records a counterexample and a Lean-verified disproof.",
    },
    "965": {
        "latex": (
            r"For every two-colouring of $\mathbb R$, must there be $A\subseteq\mathbb R$ of "
            r"cardinality $\aleph_1$ such that all $a+b$ with distinct $a,b\in A$ have one colour?"
        ),
        "additional_text": "The current official page records an unconditional negative answer.",
    },
    "1119": {
        "latex": (
            r"Let $\aleph_0<\mathfrak m<\mathfrak c$. If a family of entire functions takes at "
            r"most $\mathfrak m$ distinct values at every fixed $z_0$, must the family have "
            r"cardinality at most $\mathfrak m$?"
        ),
        "additional_text": "The current official page records independence from ZFC in the critical case.",
    },
}

VERDICTS = {
    "promising",
    "partial",
    "known_resolution",
    "counterexample",
    "blocked",
    "malformed",
    "independent",
}

RESOLUTION_STYLE_VERDICTS = {"known_resolution", "counterexample", "independent"}
UNRESOLVED_STYLE_VERDICTS = {"promising", "partial", "blocked", "malformed"}

# A few members of the frozen cohort already have substantially deeper work in
# this repository than the uniform 630-problem pass.  Keep those conclusions
# visible in the single report without overwriting the independently generated
# first-pass record.
DEEP_REPOSITORY_NOTES: dict[str, dict[str, str]] = {
    "866": {
        "path": "projects/erdos-866-ai-continuation-20260505/proof/current_focus.md",
        "note_zh": (
            "仓库深挖把首个未决案例定位为 k=7：Lean 已验证 "
            "$g_7(N)=O(N^{7/8})$；自然语言证明并经独立审计、但尚未 Lean 化的结果为，"
            "充分大 N 时 $g_7(N)>\\frac1{16}N^{2/3}$。项目明确不声称 #866 已解决；"
            "当前核心是必须保留配置结构的逆定理，例如暴露二次因子或精确控制 "
            "$R_{10}$ 的碰撞商。"
        ),
    },
    "212": {
        "path": (
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/"
            "runs/erdos212-quadratic-to-irreducible-cubic/"
            "erdos212-quadratic-to-irreducible-cubic-supervised-4h/proof_lab/round-026/summary.md"
        ),
        "note_zh": (
            "深度运行已 Lean 验证反演所得不可约三次曲线、无限有理距离零点集的传递以及"
            "射影参数化双射。第一未闭合点是多项式到 $\\operatorname{RatFunc}(\\mathbb R)$ "
            "参数化的反向核包含/精确核等式，之后才可能建立函数域有理性与属层面的结论；"
            "这些局部定理不能改写为整题已解。"
        ),
    },
    "1084": {
        "path": (
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h/"
            "runs/erdos1084-polygonal-ray-crossing-parity/"
            "erdos1084-polygonal-ray-crossing-parity-supervised-4h/proof_lab/round-011/summary.md"
        ),
        "note_zh": (
            "深度运行已对水平射线穿越、水平边块的终端线段包含和终端可见性得到"
            "声明级无 `sorryAx` 的局部 Lean 结果。下一节点是可见极大水平边块的"
            "同侧切触/异侧穿越奇偶分类，随后仍需路径不变性和全局 Jordan 分割；"
            "整文件的占位符总数不能替代声明级审计。"
        ),
    },
    "972": {
        "path": (
            "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/"
            "source_runs/erdos972-beatty-prime-pair/"
            "erdos972-beatty-prime-pair-source-cycle-03/state.json"
        ),
        "note_zh": (
            "深度来源审计的第一阻塞点是精确的外部解析数论定理：对每个固定无理数 "
            "$\\alpha>1$，需证明 $\\#\\{p<X:p,\\lfloor\\alpha p\\rfloor\\ "
            "\\text{均为素数}\\}\\gg_\\alpha X/(\\log X)^2$（或等价相关下界）。"
            "普通的 Beatty 序列素数渐近不能替代这个双素数相关。"
        ),
    },
    "1052": {
        "path": (
            "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h/"
            "source_runs/erdos1052-unitary-perfect/"
            "erdos1052-unitary-perfect-source-cycle-02/state.json"
        ),
        "note_zh": (
            "现有计算只给有界盒证据。第一阻塞点是全局旋量因子尾部定理或可执行证书："
            "给出显式截止 B，并证明每个奇 3-Higgs 素数 $p>B$ 的 "
            "$\\Phi_{4p}(2)$ 都有一个非 3-Higgs 素因子，再附上 $p\\le B$ 的完整有限见证表；"
            "固定范围计算本身不能控制素因子总数。"
        ),
    },
}


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


def git_head(path: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


def load_jsonl_by_number(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[str(row["number"])] = row
    return rows


def build_cohort(
    *,
    bank_path: Path,
    metadata_root: Path,
    prior_root: Path,
    output_dir: Path,
) -> list[dict[str, Any]]:
    bank = yaml.safe_load(bank_path.read_text(encoding="utf-8"))
    frozen = [row for row in bank if row.get("open_problem") is True]
    if len(frozen) != 630:
        raise RuntimeError(f"Expected frozen cohort of 630 entries, found {len(frozen)}")

    current_rows = yaml.safe_load((metadata_root / "data/problems.yaml").read_text(encoding="utf-8"))
    current = {str(row["number"]): row for row in current_rows}
    exact = load_jsonl_by_number(prior_root / "data/unsolved.jsonl")
    manifest_rows = read_json(prior_root / "data/solutions/manifest.json", default=[])
    manifest = {str(row["number"]): row for row in manifest_rows}
    formal_root = (
        REPO_ROOT
        / "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems"
    )

    cohort: list[dict[str, Any]] = []
    for frozen_row in frozen:
        problem_id = str(frozen_row["problem_id"])
        statement_row = exact.get(problem_id) or DIRECT_STATEMENTS.get(problem_id)
        if not statement_row:
            raise RuntimeError(f"No exact statement recovered for Erdős #{problem_id}")
        current_row = current.get(problem_id, {})
        status = current_row.get("status", {}).get("state", "missing")
        formal_file = formal_root / f"{problem_id}.lean"
        candidate_path = prior_root / "data/solutions" / problem_id / "candidate_solution.md"
        review = manifest.get(problem_id, {})
        cohort.append(
            {
                "problem_id": problem_id,
                "title": frozen_row.get("title", f"Erdős Problem #{problem_id}"),
                "domain": frozen_row.get("domain", "unknown"),
                "tags": current_row.get("tags", frozen_row.get("tags", [])),
                "frozen_status": frozen_row.get("metadata", {}).get("status_state", "open"),
                "current_status": status,
                "current_status_last_update": current_row.get("status", {}).get("last_update", ""),
                "current_formalized": current_row.get("formalized", {}).get("state", "unknown"),
                "prize": current_row.get("prize", frozen_row.get("metadata", {}).get("prize", "")),
                "statement": str(statement_row.get("latex", "")).strip(),
                "official_context": str(statement_row.get("additional_text", "")).strip(),
                "official_url": f"https://www.erdosproblems.com/{problem_id}",
                "formal_conjecture_file": str(formal_file) if formal_file.exists() else "",
                "prior_candidate_file": str(candidate_path) if candidate_path.exists() else "",
                "prior_review": {
                    "prior_solution": review.get("prior_solution"),
                    "manually_verified": review.get("solution_manually_verified"),
                    "formally_verified": review.get("solution_formally_verified"),
                    "reason": review.get("solution_manual_review_reason", ""),
                    "reviewer": review.get("solution_manual_reviewer", ""),
                },
            }
        )

    cohort.sort(key=lambda row: int(row["problem_id"]))
    payload = {
        "schema_version": "amra.erdos_630_cohort.v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "bank_path": str(bank_path),
        "metadata_source": "https://github.com/teorth/erdosproblems",
        "metadata_commit": git_head(metadata_root),
        "statement_and_prior_source": "https://github.com/neelsomani/gpt-erdos",
        "statement_and_prior_commit": git_head(prior_root),
        "problem_count": len(cohort),
        "problems": cohort,
    }
    atomic_write_json(output_dir / "cohort.json", payload)
    return cohort


def analysis_schema() -> dict[str, Any]:
    item = {
        "type": "object",
        "properties": {
            "problem_id": {"type": "string"},
            "statement_summary_zh": {"type": "string"},
            "status_note_zh": {"type": "string"},
            "attempted_route_zh": {"type": "string"},
            "partial_deductions_zh": {"type": "array", "items": {"type": "string"}},
            "blocking_step_zh": {"type": "string"},
            "next_action_zh": {"type": "string"},
            "verdict": {"type": "string", "enum": sorted(VERDICTS)},
            "proof_attempt_status": {
                "type": "string",
                "enum": [
                    "rigorous_partial",
                    "heuristic_route",
                    "known_theorem",
                    "failed",
                    "not_applicable",
                ],
            },
            "feasibility_score": {"type": "integer", "minimum": 0, "maximum": 10},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            "source_checks_zh": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "problem_id",
            "statement_summary_zh",
            "status_note_zh",
            "attempted_route_zh",
            "partial_deductions_zh",
            "blocking_step_zh",
            "next_action_zh",
            "verdict",
            "proof_attempt_status",
            "feasibility_score",
            "confidence",
            "source_checks_zh",
        ],
        "additionalProperties": False,
    }
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"analyses": {"type": "array", "items": item}},
        "required": ["analyses"],
        "additionalProperties": False,
    }


def compact(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    head = text[: int(limit * 0.72)]
    tail = text[-int(limit * 0.28) :]
    return head + "\n\n[中间内容因上下文预算截断]\n\n" + tail


def problem_prompt_payload(problem: dict[str, Any], prior_char_limit: int) -> dict[str, Any]:
    prior_text = ""
    candidate_path = problem.get("prior_candidate_file")
    if candidate_path and Path(candidate_path).exists():
        prior_text = compact(Path(candidate_path).read_text(encoding="utf-8"), prior_char_limit)
    return {
        "problem_id": problem["problem_id"],
        "current_status": problem["current_status"],
        "status_last_update": problem["current_status_last_update"],
        "domain": problem["domain"],
        "tags": problem["tags"],
        "exact_statement": problem["statement"],
        "official_context": compact(problem["official_context"], 9000),
        "official_url": problem["official_url"],
        "local_formal_statement": problem["formal_conjecture_file"],
        "untrusted_prior_candidate": prior_text,
        "prior_candidate_review": problem["prior_review"],
    }


def build_prompt(batch: list[dict[str, Any]], prior_char_limit: int) -> str:
    payload = [problem_prompt_payload(problem, prior_char_limit) for problem in batch]
    return (
        "你是一名审慎的数学研究员，正在对一个冻结的 Erdős 问题 cohort 做逐题初步证明筛查。\n\n"
        "对下面每一道题分别做一次真实但受限的证明尝试。目标不是写泛泛的研究建议，而是：\n"
        "1. 准确重述量词和对象；2. 尝试一条具体证明、反例或归约路线；\n"
        "3. 写出在该路线下确实能推出的1至3个局部结论；\n"
        "4. 指出第一处无法严格闭合的数学步骤；5. 给出下一项可检验任务。\n\n"
        "`untrusted_prior_candidate` 是其他模型以前生成的候选答案，只能当作待审稿材料。必须独立检查；"
        "若人工评审指出错误，要明确吸收该错误，不能复述错误论证。不得因为文字像证明就宣称解决开放题。\n"
        "若 current_status 已非 open，应改为重建并核对已知证明/反例路线；若状态为 independent，说明独立性机制而非尝试 ZFC 证明。\n"
        "输出必须覆盖输入中的每一个 problem_id，使用简洁中文，数学符号可保留 LaTeX。"
        "可行性分数衡量‘沿当前具体路线取得可验证进展’的可能性，不是问题的重要性。\n\n"
        "输入：\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def normalize_result(item: dict[str, Any], expected_id: str) -> dict[str, Any]:
    if str(item.get("problem_id", "")) != expected_id:
        raise ValueError(f"Result ID {item.get('problem_id')!r} does not match {expected_id}")
    if item.get("verdict") not in VERDICTS:
        raise ValueError(f"Invalid verdict for #{expected_id}: {item.get('verdict')!r}")
    item["problem_id"] = expected_id
    return item


def invoke_batch(
    *,
    batch: list[dict[str, Any]],
    output_dir: Path,
    schema_path: Path,
    timeout_sec: int,
    model: str,
    reasoning_effort: str,
    prior_char_limit: int,
) -> dict[str, Any]:
    ids = [problem["problem_id"] for problem in batch]
    batch_slug = f"{ids[0]}-{ids[-1]}-{len(ids)}"
    batch_dir = output_dir / "batches" / batch_slug
    batch_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(batch, prior_char_limit)
    atomic_write_text(batch_dir / "prompt.txt", prompt)
    raw_output = batch_dir / "raw_result.json"
    command = [
        "codex",
        "-s",
        "read-only",
        "-a",
        "never",
        "exec",
        "--ephemeral",
        "-C",
        str(REPO_ROOT),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(raw_output),
    ]
    if model:
        command.extend(["--model", model])
    if reasoning_effort:
        command.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
    command.append(prompt)

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=timeout_sec,
            check=False,
        )
        backend_status = "completed" if completed.returncode == 0 else "failed"
        atomic_write_text(batch_dir / "stdout.log", completed.stdout)
        atomic_write_text(batch_dir / "stderr.log", completed.stderr)
    except subprocess.TimeoutExpired as exc:
        backend_status = "timeout"
        atomic_write_text(batch_dir / "stdout.log", str(exc.stdout or ""))
        atomic_write_text(batch_dir / "stderr.log", str(exc.stderr or ""))
    elapsed = round(time.monotonic() - started, 3)

    parsed = read_json(raw_output, default={})
    returned = {
        str(item.get("problem_id", "")): item
        for item in parsed.get("analyses", [])
        if isinstance(item, dict)
    }
    saved: list[str] = []
    errors: list[str] = []
    per_problem_elapsed = round(elapsed / max(1, len(batch)), 3)
    for problem_id in ids:
        try:
            item = normalize_result(returned[problem_id], problem_id)
            payload = {
                "schema_version": "amra.erdos_initial_analysis.v1",
                "problem_id": problem_id,
                "backend_status": backend_status,
                "batch_elapsed_seconds": elapsed,
                "allocated_elapsed_seconds": per_problem_elapsed,
                "analysis": item,
            }
            atomic_write_json(output_dir / "results" / f"{problem_id}.json", payload)
            saved.append(problem_id)
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"#{problem_id}: {exc}")
    atomic_write_json(
        batch_dir / "batch_status.json",
        {
            "ids": ids,
            "backend_status": backend_status,
            "elapsed_seconds": elapsed,
            "saved": saved,
            "errors": errors,
        },
    )
    return {"ids": ids, "status": backend_status, "elapsed": elapsed, "saved": saved, "errors": errors}


def chunks(rows: list[dict[str, Any]], size: int) -> Iterable[list[dict[str, Any]]]:
    for index in range(0, len(rows), size):
        yield rows[index : index + size]


def run_analyses(
    *,
    cohort: list[dict[str, Any]],
    output_dir: Path,
    workers: int,
    batch_size: int,
    timeout_sec: int,
    model: str,
    reasoning_effort: str,
    prior_char_limit: int,
    limit: int | None,
    selected_ids: set[str],
) -> None:
    result_dir = output_dir / "results"
    complete_ids = {
        path.stem
        for path in result_dir.glob("*.json")
        if read_json(path, default={}).get("analysis", {}).get("problem_id") == path.stem
    }
    pending = [
        problem
        for problem in cohort
        if problem["problem_id"] not in complete_ids
        and (not selected_ids or problem["problem_id"] in selected_ids)
    ]
    if limit is not None:
        pending = pending[:limit]
    if not pending:
        return

    schema_path = output_dir / "analysis.schema.json"
    atomic_write_json(schema_path, analysis_schema())
    lock = threading.Lock()
    completed_batches = 0
    total_batches = (len(pending) + batch_size - 1) // batch_size
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(
                invoke_batch,
                batch=batch,
                output_dir=output_dir,
                schema_path=schema_path,
                timeout_sec=timeout_sec,
                model=model,
                reasoning_effort=reasoning_effort,
                prior_char_limit=prior_char_limit,
            ): [row["problem_id"] for row in batch]
            for batch in chunks(pending, batch_size)
        }
        for future in as_completed(futures):
            completed_batches += 1
            try:
                result = future.result()
            except Exception as exc:  # keep other shards running
                result = {"ids": futures[future], "status": "exception", "saved": [], "errors": [str(exc)]}
            with lock:
                progress = {
                    "completed_batches_this_run": completed_batches,
                    "total_batches_this_run": total_batches,
                    "last_batch": result,
                    "saved_result_count": len(list(result_dir.glob("*.json"))),
                }
                atomic_write_json(output_dir / "progress.json", progress)
                print(json.dumps(progress, ensure_ascii=False), flush=True)


def clean_inline(text: str) -> str:
    # JSON can legally carry escaped C0 controls, and a few model-produced
    # LaTeX fragments contained them where a backslash command was intended.
    # Repair the finite set observed in this run, then ensure no binary control
    # bytes reach the Markdown report.
    repaired = str(text)
    for corrupted, replacement in {
        "\x00ldots": r"\ldots",
        "\x00\\ldots": r"\ldots",
        "\x1f\\ldots": r"\ldots",
        "\x02ldots": r"\ldots",
        "\x08igl": r"\bigl",
        "\x0bepsilon": r"\epsilon",
        "\x1balpha": r"\alpha",
        "\x03a\\mid": r"a\mid",
        "\x07ell": r"\ell",
        "\x003e0": r"\ge 0",
    }.items():
        repaired = repaired.replace(corrupted, replacement)
    printable = "".join(
        character if ord(character) >= 32 and ord(character) != 127 else " "
        for character in repaired
    )
    return re.sub(r"\s+", " ", printable).strip()


def markdown_escape(text: str) -> str:
    return clean_inline(text).replace("|", r"\|")


def render_report(*, output_dir: Path, report_path: Path) -> dict[str, Any]:
    cohort_payload = read_json(output_dir / "cohort.json", default={})
    cohort = cohort_payload.get("problems", [])
    cohort_by_id = {problem["problem_id"]: problem for problem in cohort}
    result_payloads = {
        path.stem: read_json(path, default={}) for path in (output_dir / "results").glob("*.json")
    }
    current_statuses = Counter(problem["current_status"] for problem in cohort)
    analyses = {
        problem_id: payload.get("analysis", {})
        for problem_id, payload in result_payloads.items()
        if payload.get("analysis", {}).get("problem_id") == problem_id
    }
    verdicts = Counter(item.get("verdict", "missing") for item in analyses.values())
    proof_attempt_statuses = Counter(
        item.get("proof_attempt_status", "missing") for item in analyses.values()
    )
    confidences = Counter(item.get("confidence", "missing") for item in analyses.values())
    scores = Counter(int(item.get("feasibility_score", 0)) for item in analyses.values())

    expected_ids = set(cohort_by_id)
    result_ids = set(result_payloads)
    unexpected_ids = sorted(result_ids - expected_ids, key=int)
    missing_ids = sorted(expected_ids - set(analyses), key=int)
    required_fields = set(
        analysis_schema()["properties"]["analyses"]["items"]["required"]
    )
    field_errors: dict[str, list[str]] = {}
    backend_issue_ids: list[str] = []
    for problem_id in sorted(expected_ids & result_ids, key=int):
        payload = result_payloads[problem_id]
        item = payload.get("analysis", {})
        missing_fields = sorted(required_fields - set(item))
        if missing_fields:
            field_errors[problem_id] = missing_fields
        if payload.get("backend_status") != "completed":
            backend_issue_ids.append(problem_id)

    current_open_resolution_flags = sorted(
        (
            problem_id
            for problem_id, item in analyses.items()
            if cohort_by_id.get(problem_id, {}).get("current_status") == "open"
            and item.get("verdict") in RESOLUTION_STYLE_VERDICTS
        ),
        key=int,
    )
    non_open_unresolved_flags = sorted(
        (
            problem_id
            for problem_id, item in analyses.items()
            if cohort_by_id.get(problem_id, {}).get("current_status") != "open"
            and item.get("verdict") in UNRESOLVED_STYLE_VERDICTS
        ),
        key=int,
    )
    allocated_times = [
        float(payload.get("allocated_elapsed_seconds", 0) or 0)
        for payload in result_payloads.values()
    ]
    batch_times = [
        float(payload.get("batch_elapsed_seconds", 0) or 0)
        for payload in result_payloads.values()
    ]
    total_allocated_seconds = sum(allocated_times)
    max_allocated_seconds = max(allocated_times, default=0.0)
    max_batch_seconds = max(batch_times, default=0.0)

    def official_problem_links(problem_ids: list[str]) -> str:
        if not problem_ids:
            return "无"
        return "、".join(
            f"[#{problem_id}]({cohort_by_id[problem_id]['official_url']})"
            for problem_id in problem_ids
        )

    lines = [
        "# Erdős 冻结 630 题逐题初步证明路径",
        "",
        f"> 生成日期：{time.strftime('%Y-%m-%d', time.gmtime())}。这是初步研究筛查，不是 630 道题已被证明的声明。",
        "",
        "## 范围与方法",
        "",
        (
            f"本文覆盖仓库 `erdos_open_shortlist_refreshed.yaml` 中冻结的 {len(cohort)} 条记录。"
            "该清单是历史 cohort；状态按当前 Erdős Problems 数据库快照重新核对。"
            "每题输入精确题面、官方背景、现有 Lean 文件（如有）以及一份不可信的既有候选答案，"
            "再进行独立的浅层证明/反例/归约审计。每题所在的代理批次硬超时不超过30分钟；"
            "条目中的秒数是批次墙钟时间按题数均摊，并非单题独占计时。"
        ),
        "",
        (
            "- 当前元数据来源：[teorth/erdosproblems]"
            f"(https://github.com/teorth/erdosproblems)，提交 "
            f"`{cohort_payload.get('metadata_commit', 'unknown')}`"
        ),
        (
            "- 题面与既有候选来源：[neelsomani/gpt-erdos]"
            f"(https://github.com/neelsomani/gpt-erdos)，提交 "
            f"`{cohort_payload.get('statement_and_prior_commit', 'unknown')}`"
        ),
        f"- 已完成独立探测：{len(analyses)}/{len(cohort)}",
        "- 判定含义：`promising` 表示找到值得继续验证的具体路线；`partial` 表示有严格局部推进；"
        "  `blocked` 表示尚未越过开放核心；其他判定用于已知解、反例、病题或独立性。",
        (
            "- 严格免责声明：凡当前官方状态仍为 `open` 的题，本文中的“完整证明”、"
            "“反例”或“独立性”都只算待复核候选；未经独立专家审稿，不改变官方状态。"
        ),
        "",
        "## 状态总览",
        "",
        "| 当前状态 | 数量 |",
        "|---|---:|",
    ]
    for status, count in sorted(current_statuses.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {markdown_escape(status)} | {count} |")
    lines.extend(["", "## 初筛结论分布", "", "| 初筛判定 | 数量 |", "|---|---:|"])
    for verdict, count in sorted(verdicts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {markdown_escape(verdict)} | {count} |")

    lines.extend(
        [
            "",
            "## 结构质检与冲突清单",
            "",
            "| 检查项 | 结果 |",
            "|---|---:|",
            f"| cohort 覆盖 | {len(analyses)}/{len(cohort)} |",
            f"| 待处理题目 | {len(missing_ids)} |",
            f"| cohort 外结果 | {len(unexpected_ids)} |",
            f"| 必填字段错误 | {len(field_errors)} |",
            f"| 后端非完成状态 | {len(backend_issue_ids)} |",
            f"| 批次累计运行时（按题均摊求和） | {total_allocated_seconds / 3600:.2f} 小时 |",
            f"| 最长单批墙钟时间 | {max_batch_seconds:.1f} 秒 |",
            f"| 最大单题均摊时间 | {max_allocated_seconds:.1f} 秒 |",
            "",
            (
                f"- **官方仍为 open、但初筛给出解答型判定（{len(current_open_resolution_flags)} 条）**："
                f"{official_problem_links(current_open_resolution_flags)}。"
            ),
            (
                f"- **官方已非 open、但初筛仍呈未闭合/题面错配（{len(non_open_unresolved_flags)} 条）**："
                f"{official_problem_links(non_open_unresolved_flags)}。"
            ),
            "",
            (
                "以上是人工复核队列，不是结构错误，也不是状态改写。常见原因包括题面按字面可反驳、"
                "官方保留的是修正版、元数据更新时间差、或 Lean 形式化题面与当前自然语言版本不一致。"
            ),
        ]
    )

    ranked = sorted(
        (
            item
            for problem_id, item in analyses.items()
            if cohort_by_id.get(problem_id, {}).get("current_status") == "open"
            and item.get("verdict") in {"promising", "partial"}
        ),
        key=lambda item: (-int(item.get("feasibility_score", 0)), int(item["problem_id"])),
    )
    high_priority = [item for item in ranked if int(item.get("feasibility_score", 0)) >= 8]
    lines.extend(
        [
            "",
            "## 当前开放题中的优先续攻路线",
            "",
            (
                f"下表只保留官方仍为 `open`、初筛为 `promising/partial` 且可行性至少 8/10 的 "
                f"{len(high_priority)} 条路线。分数只是下一步是否具体可检验，不代表接近完整解决。"
            ),
            "",
            "| # | 分数 | 判定 | 下一项可检验任务 |",
            "|---:|---:|---|---|",
        ]
    )
    for item in high_priority:
        lines.append(
            f"| {item['problem_id']} | {item.get('feasibility_score', 0)} | "
            f"{markdown_escape(item.get('verdict', ''))} | {markdown_escape(item.get('next_action_zh', ''))} |"
        )

    lines.extend(
        [
            "",
            "## 仓库既有深度项目补充",
            "",
            "这五题已有多轮专项证明或形式化工作；以下结论优先于均匀首轮，但仍不构成整题解决声明。",
            "",
        ]
    )
    for problem_id, note in DEEP_REPOSITORY_NOTES.items():
        note_path = REPO_ROOT / note["path"]
        lines.extend(
            [
                f"### #{problem_id} 深度补充",
                "",
                note["note_zh"],
                "",
                f"证据：[仓库记录]({note_path})",
                "",
            ]
        )

    lines.extend(["", "## 逐题记录", ""])
    for problem in cohort:
        problem_id = problem["problem_id"]
        payload = result_payloads.get(problem_id, {})
        item = analyses.get(problem_id)
        lines.extend(
            [
                f"### #{problem_id}",
                "",
                f"- 当前状态：`{problem['current_status']}`（冻结清单状态：`{problem['frozen_status']}`）",
                f"- 精确题面：{clean_inline(problem['statement'])}",
            ]
        )
        if not item:
            lines.extend(
                [
                    "- 初步判定：`pending`",
                    "- 说明：独立证明探测尚未完成；精确题面和状态核对已经完成。",
                    f"- 来源：[官方题页]({problem['official_url']})",
                    "",
                ]
            )
            continue
        deductions = item.get("partial_deductions_zh", [])
        deduction_text = "；".join(clean_inline(value) for value in deductions) or "未得到可独立核验的局部结论"
        source_checks = item.get("source_checks_zh", [])
        source_check_text = "；".join(clean_inline(value) for value in source_checks) or "未记录额外来源核对"
        allocated = payload.get("allocated_elapsed_seconds", 0)
        source_bits = [f"[官方题页]({problem['official_url']})"]
        if problem.get("formal_conjecture_file"):
            source_bits.append(f"本地 Lean：`{problem['formal_conjecture_file']}`")
        if problem.get("prior_candidate_file"):
            source_bits.append("既有候选答案（按不可信材料审计）")
        lines.extend(
            [
                f"- 题意摘要：{clean_inline(item.get('statement_summary_zh', ''))}",
                f"- 状态核对：{clean_inline(item.get('status_note_zh', ''))}",
                (
                    f"- 初步判定：`{item.get('verdict', '')}`；证明尝试："
                    f"`{item.get('proof_attempt_status', '')}`；可行性 `{item.get('feasibility_score', 0)}/10`；"
                    f"置信度 `{item.get('confidence', '')}`"
                ),
                f"- 尝试路线：{clean_inline(item.get('attempted_route_zh', ''))}",
                f"- 局部结论：{deduction_text}",
                f"- 第一阻塞点：{clean_inline(item.get('blocking_step_zh', ''))}",
                f"- 下一步：{clean_inline(item.get('next_action_zh', ''))}",
                f"- 来源核对：{source_check_text}",
                f"- 时间记账：所在批次墙钟时间按题数均摊约 {allocated:.1f} 秒；批次硬上限 1800 秒。",
                f"- 来源：{'；'.join(source_bits)}",
            ]
        )
        deep_note = DEEP_REPOSITORY_NOTES.get(problem_id)
        if deep_note:
            deep_path = REPO_ROOT / deep_note["path"]
            lines.append(
                f"- 深度项目：{clean_inline(deep_note['note_zh'])} [证据]({deep_path})"
            )
        lines.append("")

    atomic_write_text(report_path, "\n".join(lines).rstrip() + "\n")
    summary = {
        "cohort_count": len(cohort),
        "completed_count": len(analyses),
        "pending_count": len(cohort) - len(analyses),
        "current_statuses": dict(current_statuses),
        "verdicts": dict(verdicts),
        "proof_attempt_statuses": dict(proof_attempt_statuses),
        "confidences": dict(confidences),
        "scores": {str(score): count for score, count in sorted(scores.items())},
        "quality_audit": {
            "missing_ids": missing_ids,
            "unexpected_ids": unexpected_ids,
            "field_errors": field_errors,
            "backend_issue_ids": backend_issue_ids,
            "current_open_resolution_flags": current_open_resolution_flags,
            "non_open_unresolved_flags": non_open_unresolved_flags,
            "total_allocated_seconds": round(total_allocated_seconds, 3),
            "max_allocated_seconds": round(max_allocated_seconds, 3),
            "max_batch_seconds": round(max_batch_seconds, 3),
        },
        "high_priority_open_ids": [item["problem_id"] for item in high_priority],
        "report_path": str(report_path),
    }
    atomic_write_json(output_dir / "report_summary.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK)
    parser.add_argument("--metadata-root", type=Path, required=True)
    parser.add_argument("--prior-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--timeout-per-batch", type=int, default=1800)
    parser.add_argument("--model", default="")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--prior-char-limit", type=int, default=14000)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--ids", default="", help="Comma-separated problem IDs; empty means all pending entries.")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.render_only:
        summary = render_report(output_dir=args.output_dir, report_path=args.report)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    cohort = build_cohort(
        bank_path=args.bank.resolve(),
        metadata_root=args.metadata_root.resolve(),
        prior_root=args.prior_root.resolve(),
        output_dir=args.output_dir.resolve(),
    )
    if not args.prepare_only:
        selected_ids = {value.strip() for value in args.ids.split(",") if value.strip()}
        run_analyses(
            cohort=cohort,
            output_dir=args.output_dir.resolve(),
            workers=args.workers,
            batch_size=max(1, args.batch_size),
            timeout_sec=min(1800, max(1, args.timeout_per_batch)),
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            prior_char_limit=max(1000, args.prior_char_limit),
            limit=args.limit,
            selected_ids=selected_ids,
        )
    summary = render_report(output_dir=args.output_dir.resolve(), report_path=args.report.resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
