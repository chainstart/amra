#!/usr/bin/env python3
"""Render the second four-hour attack on the 22 non-1039 priority routes."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "artifacts/erdos_followup_20260719"
OLD = AUDIT / "proof_routes"
NEW = AUDIT / "proof_routes_round2_4h"
REPORT = ROOT / "docs/erdos_22_four_hour_round2.zh.md"
IDS = [
    "952", "1083", "25", "117", "143", "148", "256", "301", "325", "332",
    "377", "539", "635", "679", "686", "776", "788", "827", "934", "950",
    "963", "1063",
]

# Curated only after checking the exact quantified scope of each result.  None
# of these rows, including #1063, is a complete solution of the corresponding
# open-ended official problem.
HIGHLIGHTS = [
    (
        "1063",
        r"令 $L_k=\operatorname{lcm}(1,\ldots,k-1)$、$p$ 为最小的 $p>k/2$ 素数；证明 "
        r"$n_k\le((2p-k+1)/p)kL_k=o(kL_k)$，并由 BHP 得 $O(k^{0.525}L_k)$。",
        "完整闭合 FormalConjectures 的 better_upper 子定理；官网开放式“Estimate n_k”仍未闭合，且尚非 Lean 或已发表论文。",
    ),
    (
        "963",
        r"把渐近下界定量加强为 $f(n)\ge\log_2n-O((\log\log n)^2)$；另给出 $F(4)\ge27$。",
        r"误差仍发散，不能推出官网逐点猜想 $f(n)\ge\lfloor\log_2n\rfloor$。",
    ),
    (
        "950",
        r"证明局部极值只需检查 $f(p)$、$f(p+1)$，并得无条件 $\limsup f(n)\ge10651/7410$。",
        "三个原极限问题均未解决；更高常数中依赖未评审预印本的部分已单列而未算成熟结论。",
    ),
    (
        "148",
        r"候选新界 $f_5(m,n)\ll_\varepsilon n^\varepsilon(n^2/m)^{446/289}$，继而改善 $F(k)$ 的同底数系数。",
        "是经过内部复核的候选新上界，不是原问题的完整闭合，也尚未发表。",
    ),
    (
        "788",
        r"无条件证明 $f(n)=\Omega(\sqrt{n\log n})$，并精确得到 $f(13)=7,f(14)=8,f(15)=8$。",
        r"原题询问 $f(n)\le n^{1/2+o(1)}$，所以上界方向仍开放。",
    ),
    (
        "776",
        r"对所有 $r\ge4$ 证明 $g(2r+4,r)\le2r$，故 $n_0(r)\ge2r+4$。",
        "这是新的统一下界，不是对阈值的精确确定。",
    ),
    (
        "827",
        r"得到 $n_k\ge(24\sqrt{\log2}+o(1))k^2(\log k)^{-1/2}e^{-4\sqrt{(\log2)(\log k)}}$。",
        "只推进下界；匹配上界和原题整体仍开放。",
    ),
    (
        "325",
        r"证明 $f_{4,3}(x)\gg_\varepsilon x^{0.704143-\varepsilon}$。",
        r"只覆盖 $k=4$ 的部分改进，距离目标 $3/4$ 且其他 $k$ 均有缺口。",
    ),
    (
        "635",
        r"严格确定 $F_2(3000)=1506$、$F_2(5000)=2506$，并给出独立左 Hall 的有限刻画。",
        "拟议的私有邻点定理仍未证明，不能外推为完整渐近解。",
    ),
    (
        "301",
        "证明指定 punctured-box/完整赋值方法类的最优权重常数为 450/403。",
        "这是固定方法类的最优性与障碍证书，并未改善官网原问题的最佳界。",
    ),
    (
        "952",
        "构造并交叉核验步长上界 D=4 的有限 Gaussian moat 证书。",
        "只闭合 D=4 子情形；任意有界步长的原题仍开放。",
    ),
]


def load(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def audit_entries(path: Path) -> list[dict[str, Any]]:
    value = load(path, [])
    return value.get("entries", []) if isinstance(value, dict) else value


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\r", " ")).strip()


def cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def source(source_row: dict[str, Any]) -> str:
    title, url = clean(source_row.get("title")), clean(source_row.get("url"))
    return f"[{title}]({url})" if url.startswith(("https://", "http://")) else title


def main() -> int:
    old = {}
    new = {}
    for problem_id in IDS:
        before = load(OLD / "results" / f"{problem_id}.json", {})
        after = load(NEW / "results" / f"{problem_id}.json", {})
        if before.get("analysis", {}).get("problem_id") == problem_id:
            old[problem_id] = before
        if after.get("analysis", {}).get("problem_id") == problem_id:
            new[problem_id] = after
    reviews = {}
    for path in NEW.glob("*_independent_verification.json"):
        value = load(path, {})
        problem_id = str(value.get("problem_id", ""))
        if problem_id in IDS:
            reviews[problem_id] = value

    missing = [problem_id for problem_id in IDS if problem_id not in new]
    conclusions = Counter(
        value["analysis"].get("conclusion", "missing") for value in new.values()
    )
    claims = Counter(
        value["analysis"].get("full_solution_claim", "missing") for value in new.values()
    )
    backends = Counter(value.get("backend_status", "missing") for value in new.values())
    total = round(sum(float(value.get("elapsed_seconds", 0)) for value in new.values()), 3)
    maximum = round(
        max((float(value.get("elapsed_seconds", 0)) for value in new.values()), default=0),
        3,
    )

    lines = [
        "# Erdős 22 条候选路线第二轮四小时续攻",
        "",
        "> 生成日期：2026-07-19。每题 14,400 秒是硬上限，不是必须耗尽的目标；"
        "本报告只把相对第一轮的新增推导计作推进。",
        "",
        "## 104 条证据问题是否意味着题目全部重开",
        "",
        "不是。这里必须区分“证明有数学缺口”“题目原本就仍开放”和“状态/题面范围标签不精确”。"
        "在本次核验材料覆盖的 80 条机械归入非开放集合记录中，只有 #358 发现了足以使当前公开闭合证明不能完成定理的"
        "明确数学缺口：公开稿的中频论断存在具体参数反例，作者已承诺修订但尚无新版。因此 #358"
        " 目前应视为闭合尚未核实、仍需攻关；这仍不等于定理已被证伪，证明可能可以修补。",
        "",
        "#114、#488 实际一直是 `falsifiable`/OPEN，只是被机械误收进这 80 条，并不存在一份后来被"
        "推翻的闭合证明；#783 的 `SOLVED` 对应后来修订的渐近题面，不等于冻结版本要求的逐个有限"
        "精确分类；#1022 的数学和 Lean 代码证明的是否命题，正确闭合方向应是 `DISPROVED (LEAN)`，"
        "不是重新开放。其余异常主要是题面条件或版本变化、复合题只解决一部分、Lean 把深层输入"
        "公理化、Lean 证明旧题面，或证据尚未同行评审。这些问题降低状态标签或证据成熟度的精度，"
        "但不会自动推翻已有数学证明。",
        "",
        "24 条官网仍 OPEN 的冲突中，没有发现第二个像 #358 那样已定位公式反例且获作者承认的"
        "闭合证明漏洞。#520、#335 是先前分析错误；#638、#701、#918 是形式化或题面范围问题；"
        "#550、#1070 是近期声称的成熟度或复合题范围问题；#920 更像状态同步滞后。",
        "",
        "| 审计集合 | 分类结果 | 对开放性的含义 |",
        "|---|---|---|",
        "| 80 条机械归入非 OPEN | 50 closed_verified；25 closed_scope_caveat；1 evidence_incomplete；4 status_or_statement_mismatch | #358 因现有闭合稿的具体缺口而应暂视为未核实；#114、#488 原本就仍开放；#783 是版本范围差；#1022 应改闭合方向。不能把这四类情形统称为“原证明全部失败” |",
        "| 24 条官网 OPEN 冲突 | 12 literal_false_intended_open；6 still_open_correct；2 initial_analysis_wrong；2 recent_claim_unverified；1 independence_scope_mismatch；1 likely_status_stale | 它们本来就是 OPEN；审计主要澄清为何仍开放或官网是否可能滞后，不存在把 24 份原证明一并推翻的问题 |",
        "",
        "## 覆盖与运行质检",
        "",
        "| 指标 | 数值 |",
        "|---|---:|",
        f"| 预期路线 | {len(IDS)} |",
        f"| 已完成 | {len(new)} |",
        f"| 缺失 | {len(missing)} |",
        f"| 累计题目运行时间（相加） | {total / 3600:.2f} 小时 |",
        f"| 单题最长 | {maximum:.1f} 秒 |",
        "",
    ]
    if missing:
        lines.extend([f"> 进行中快照；缺失 ID：{','.join(missing)}。", ""])
    lines.extend(["### 第二轮结论分布", "", "| 结论 | 数量 |", "|---|---:|"])
    for verdict, count in sorted(conclusions.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {cell(verdict)} | {count} |")
    lines.extend(
        [
            "",
            "route_advanced 只表示得到新的严格中间结论；route_blocked 表示未越过明确障碍；"
            "route_refuted 表示本轮所攻路线被否定。只有精确题面的全部量词闭合时才允许候选"
            "完整证明或候选反例标签。",
            "",
            "### 重点推进及其边界",
            "",
            "> 本轮严格 QA 后没有任何一条被标为官网原题的候选完整证明。#1063 是完整子定理证明，"
            "但因官网题面更开放，按统一标签规则记为 route_advanced。",
            "",
            "| # | 本轮最强推进 | 不能据此声称的范围 | 独立复核 |",
            "|---:|---|---|---|",
        ]
    )
    for problem_id, highlight, boundary in HIGHLIGHTS:
        if problem_id not in new:
            continue
        review = reviews.get(problem_id, {})
        review_status = clean(review.get("verdict")) or "待独立复核"
        lines.append(
            f"| {problem_id} | {cell(highlight)} | {cell(boundary)} | {cell(review_status)} |"
        )
    lines.extend(
        [
            "",
            "## 新增结果总表",
            "",
            "| # | 第一轮 | 第二轮 | 用时 | 最主要新增 |",
            "|---:|---|---|---:|---|",
        ]
    )
    for problem_id in IDS:
        before = old.get(problem_id, {}).get("analysis", {})
        payload = new.get(problem_id)
        if not payload:
            lines.append(f"| {problem_id} | {cell(before.get('conclusion'))} | pending | — | — |")
            continue
        item = payload["analysis"]
        progress = item.get("rigorous_progress_zh", [])
        headline = progress[0] if progress else item.get("blocking_step_zh", "无新增")
        lines.append(
            f"| {problem_id} | {cell(before.get('conclusion'))} | "
            f"{cell(item.get('conclusion'))} | {float(payload.get('elapsed_seconds', 0)):.1f} 秒 | "
            f"{cell(headline)} |"
        )

    lines.extend(["", "## 逐题第二轮记录", ""])
    for problem_id in IDS:
        before = old.get(problem_id, {}).get("analysis", {})
        payload = new.get(problem_id)
        lines.extend(
            [
                f"### #{problem_id}",
                "",
                f"- 第一轮障碍：{clean(before.get('blocking_step_zh'))}",
                f"- 第一轮下一定理：{clean(before.get('next_theorem_zh'))}",
            ]
        )
        if not payload:
            lines.extend(["- 第二轮状态：pending", ""])
            continue
        item = payload["analysis"]
        proof_note = str(item.get("proof_note_zh", "")).strip()
        lines.extend(
            [
                f"- 第二轮用时：{float(payload.get('elapsed_seconds', 0)):.1f} 秒；"
                f"硬上限 {int(payload.get('hard_timeout_seconds', 14400))} 秒；"
                f"后端：{clean(payload.get('backend_status'))}",
                f"- 第二轮目标：{clean(item.get('route_goal_zh'))}",
                f"- 第二轮结论：{clean(item.get('conclusion'))}；"
                f"完整解声明：{clean(item.get('full_solution_claim'))}；"
                f"置信度：{clean(item.get('confidence'))}",
                "",
            ]
        )
        review = reviews.get(problem_id)
        if review:
            review_scope = review.get("verified_scope") or review.get("verified_scope_zh")
            review_caveat = (
                review.get("caveat_zh")
                or review.get("final_caveat_zh")
                or review.get("scope_boundary_zh")
                or review.get("scope_and_remaining_gap_zh")
                or review.get("scope_and_open_status_zh")
                or review.get("bottom_line_zh")
            )
            review_mode = review.get("review_mode") or review.get("bottom_line_zh")
            lines.extend(
                [
                    f"- 独立复核：{clean(review.get('verdict'))}；"
                    f"范围：{clean(review_scope)}",
                    f"- 复核方式：{clean(review_mode)}",
                    f"- 证据边界：{clean(review_caveat)}",
                    "",
                ]
            )
        lines.extend(["#### 第二轮实际尝试", ""])
        for attempt in item.get("attempts", []):
            lines.append(
                f"- **{clean(attempt.get('label_zh'))}**（{clean(attempt.get('outcome'))}）："
                f"{clean(attempt.get('method_zh'))}；{clean(attempt.get('derivation_zh'))}"
            )
        if not item.get("attempts"):
            lines.append("- 未记录可审计尝试。")
        lines.extend(["", "#### 第二轮新增严格进展", ""])
        for progress in item.get("rigorous_progress_zh", []):
            lines.append(f"- {clean(progress)}")
        if not item.get("rigorous_progress_zh"):
            lines.append("- 无。")
        lines.extend(["", "#### 证伪与边界检查", ""])
        for check in item.get("falsification_checks_zh", []):
            lines.append(f"- {clean(check)}")
        if not item.get("falsification_checks_zh"):
            lines.append("- 无。")
        lines.extend(["", "#### 可复现资产", ""])
        for artifact in item.get("computational_artifacts", []):
            artifact_path = clean(artifact.get("artifact_path"))
            label = (
                f"[{artifact_path}]({artifact_path})"
                if artifact_path.startswith("/")
                else artifact_path
            )
            lines.append(
                f"- {label}：{clean(artifact.get('description_zh'))}；"
                f"命令：{clean(artifact.get('reproduce_command'))}；"
                f"结果：{clean(artifact.get('result_zh'))}"
            )
        if not item.get("computational_artifacts"):
            lines.append("- 无新增计算资产。")
        lines.extend(
            [
                "",
                "#### 当前障碍",
                "",
                str(item.get("blocking_step_zh", "")).strip(),
                "",
                "#### 下一精确定理",
                "",
                str(item.get("next_theorem_zh", "")).strip(),
                "",
                "#### 第二轮证明记录",
                "",
                proof_note,
                "",
                "#### 本轮核查来源",
                "",
            ]
        )
        for row in item.get("sources_checked", []):
            lines.append(
                f"- {source(row)}；一手来源：{str(bool(row.get('primary_source'))).lower()}；"
                f"核验：{clean(row.get('verified_claim_zh'))}"
            )
        if not item.get("sources_checked"):
            lines.append("- 无。")
        lines.append("")

    nonopen = audit_entries(AUDIT / "audit_nonopen_a.json") + audit_entries(
        AUDIT / "audit_nonopen_b.json"
    )
    conflicts = audit_entries(AUDIT / "audit_open_conflicts.json")
    summary = {
        "schema_version": "amra.erdos_22_four_hour_round2_report.v1",
        "expected": len(IDS),
        "completed": len(new),
        "missing": missing,
        "conclusions": dict(conclusions),
        "solution_claims": dict(claims),
        "backend_statuses": dict(backends),
        "total_elapsed_seconds": total,
        "max_elapsed_seconds": maximum,
        "result_ids": [problem_id for problem_id in IDS if problem_id in new],
        "independent_verifications": reviews,
        "nonopen_closure_counts": dict(
            Counter(row.get("closure_verdict", "missing") for row in nonopen)
        ),
        "open_conflict_counts": dict(
            Counter(row.get("audit_verdict", "missing") for row in conflicts)
        ),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    NEW.mkdir(parents=True, exist_ok=True)
    (NEW / "report_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
