#!/usr/bin/env python3
"""Merge the 80-status, 24-conflict, and 23-route audits into one report."""

from __future__ import annotations

import json
import os
import re
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
INITIAL_ROOT = REPO_ROOT / "artifacts/erdos_630_initial_analysis"
FOLLOWUP_ROOT = REPO_ROOT / "artifacts/erdos_followup_20260719"
REPORT_PATH = REPO_ROOT / "docs/erdos_80_24_23_followup_audit.zh.md"

OPEN_CONFLICT_IDS = [
    "129", "180", "335", "520", "545", "550", "563", "575", "612", "638", "654",
    "655", "701", "786", "796", "836", "890", "917", "918", "920", "935", "985",
    "1070", "1112",
]
PRIORITY_IDS = [
    "952", "1083", "1039", "25", "117", "143", "148", "256", "301", "325", "332",
    "377", "539", "635", "679", "686", "776", "788", "827", "934", "950", "963",
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


def clean(value: Any) -> str:
    printable = "".join(
        character if ord(character) >= 32 and ord(character) != 127 else " "
        for character in str(value or "")
    )
    return re.sub(r"\s+", " ", printable).strip()


def multiline(value: Any) -> str:
    raw = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    printable = "".join(
        character if character == "\n" or (ord(character) >= 32 and ord(character) != 127) else " "
        for character in raw
    )
    paragraphs = ["\n".join(line.rstrip() for line in part.splitlines()).strip() for part in re.split(r"\n\s*\n", printable)]
    return "\n\n".join(part for part in paragraphs if part)


def table(value: Any) -> str:
    return clean(value).replace("|", r"\|")


def linked_title(evidence: dict[str, Any]) -> str:
    title = clean(evidence.get("title") or evidence.get("url") or "未命名证据")
    url = clean(evidence.get("url"))
    if url.startswith("file://"):
        url = url[len("file://"):]
    return f"[{title}]({url})" if url else title


def evidence_bucket(evidence: dict[str, Any]) -> str:
    kind = clean(evidence.get("type")).lower()
    state = clean(evidence.get("publication_state")).lower()
    title = clean(evidence.get("title")).lower()
    if "lean" in kind or "formal" in kind or "lean" in state or (
        "lean" in title and "official" not in kind
    ):
        return "公开 Lean/形式证明"
    if any(token in kind for token in ("peer_reviewed", "published_paper", "published_monograph", "published_or_archived")):
        return "已发表论文/专著"
    if "同行评审" in state or "正式发表" in state:
        return "已发表论文/专著"
    if any(token in kind for token in ("preprint", "manuscript", "research_revision", "accepted_proof_claim")):
        return "预印本/公开手稿"
    if any(token in state for token in ("预印本", "未评审", "手稿", "研究稿", "arxiv", "overleaf")):
        return "预印本/公开手稿"
    if any(token in kind for token in ("code", "verifier", "certificate", "experiment")):
        return "公开代码/计算证书"
    if "official" in kind or "官方" in state:
        return "官方记录"
    return "其他公开证据"


def load_entries(path: Path) -> list[dict[str, Any]]:
    payload = read_json(path, default={})
    return payload.get("entries", []) if isinstance(payload, dict) else []


def main() -> int:
    cohort_payload = read_json(INITIAL_ROOT / "cohort.json", default={})
    cohort = cohort_payload.get("problems", [])
    cohort_by_id = {row["problem_id"]: row for row in cohort}
    nonopen_expected = [row["problem_id"] for row in cohort if row.get("current_status") != "open"]

    nonopen_entries = load_entries(FOLLOWUP_ROOT / "audit_nonopen_a.json") + load_entries(
        FOLLOWUP_ROOT / "audit_nonopen_b.json"
    )
    nonopen_by_id = {str(row.get("problem_id")): row for row in nonopen_entries}
    conflict_entries = load_entries(FOLLOWUP_ROOT / "audit_open_conflicts.json")
    conflicts_by_id = {str(row.get("problem_id")): row for row in conflict_entries}

    proof_payloads: dict[str, dict[str, Any]] = {}
    for path in (FOLLOWUP_ROOT / "proof_routes/results").glob("*.json"):
        payload = read_json(path, default={})
        if payload.get("analysis", {}).get("problem_id") == path.stem:
            proof_payloads[path.stem] = payload
    independent_verifications = {
        "1039": read_json(
            FOLLOWUP_ROOT / "proof_routes/1039_independent_verification.json", default={}
        ),
        "776": read_json(
            FOLLOWUP_ROOT / "proof_routes/776_independent_verification.json", default={}
        ),
        "788": read_json(
            FOLLOWUP_ROOT / "proof_routes/788_independent_verification.json", default={}
        ),
        "827": read_json(
            FOLLOWUP_ROOT / "proof_routes/827_independent_verification.json", default={}
        ),
        "934": read_json(
            FOLLOWUP_ROOT / "proof_routes/934_independent_verification.json", default={}
        ),
        "950": read_json(
            FOLLOWUP_ROOT / "proof_routes/950_independent_verification.json", default={}
        ),
        "963": read_json(
            FOLLOWUP_ROOT / "proof_routes/963_independent_verification.json", default={}
        ),
        "1063": read_json(
            FOLLOWUP_ROOT / "proof_routes/1063_independent_verification.json", default={}
        ),
    }

    nonopen_missing = [problem_id for problem_id in nonopen_expected if problem_id not in nonopen_by_id]
    nonopen_unexpected = sorted(set(nonopen_by_id) - set(nonopen_expected), key=int)
    conflict_missing = [problem_id for problem_id in OPEN_CONFLICT_IDS if problem_id not in conflicts_by_id]
    conflict_unexpected = sorted(set(conflicts_by_id) - set(OPEN_CONFLICT_IDS), key=int)
    proof_missing = [problem_id for problem_id in PRIORITY_IDS if problem_id not in proof_payloads]
    proof_unexpected = sorted(set(proof_payloads) - set(PRIORITY_IDS), key=int)

    closure_counts = Counter(row.get("closure_verdict", "missing") for row in nonopen_entries)
    conflict_counts = Counter(row.get("audit_verdict", "missing") for row in conflict_entries)
    proof_counts = Counter(
        payload.get("analysis", {}).get("conclusion", "missing")
        for payload in proof_payloads.values()
    )
    evidence_types = Counter(
        evidence.get("type", "missing")
        for row in nonopen_entries + conflict_entries
        for evidence in row.get("evidence", [])
        if isinstance(evidence, dict)
    )
    nonopen_evidence_buckets = Counter()
    for row in nonopen_entries:
        buckets = {
            evidence_bucket(evidence)
            for evidence in row.get("evidence", [])
            if isinstance(evidence, dict)
        }
        if len(buckets) > 1:
            buckets.discard("官方记录")
        nonopen_evidence_buckets.update(buckets)
    total_proof_seconds = sum(float(payload.get("elapsed_seconds", 0)) for payload in proof_payloads.values())
    max_proof_seconds = max(
        (float(payload.get("elapsed_seconds", 0)) for payload in proof_payloads.values()), default=0
    )

    lines = [
        "# Erdős 80 项状态证据、24 项开放冲突与 23 条证明路线复核",
        "",
        f"> 生成日期：{time.strftime('%Y-%m-%d', time.gmtime())}。开放题的新证明或反例默认按待独立审稿候选处理；若已有可复现机器证书，则另行明确标注其证据层级。",
        "",
        "## 核验口径",
        "",
        (
            "本报告不把数据库标签、论坛评论或 FormalConjectures 中的题面占位符当成证明。"
            "论文类证据必须核对原文定理的量词和题面版本；预印本单独标注、不能伪装成已同行评审论文；"
            "Lean 类证据必须区分题面形式化与证明代码，并检查 `sorry`、额外公理、依赖缺口和声明匹配。"
        ),
        "本轮所谓“80 道非 open”是冻结 cohort 中 `status != open` 的机械集合；其中 `falsifiable` 只表示可由有限计算判定，并不自动表示已经证真或证否，故可能被审计为尚未闭合。",
        "状态元数据取自 [teorth/erdosproblems](https://github.com/teorth/erdosproblems) 固定提交 `aab2deceb51aee0ef28c17d8d194249cbee13d7a`；官网 [FAQ](https://www.erdosproblems.com/faq) 明确提醒数据库未必实时反映全部文献。"
        "[FormalConjectures](https://github.com/google-deepmind/formal-conjectures) 是题面形式化/基准集合，仓库说明本就允许没有证明；本轮只把独立可检查的证明文件或证明包计作 Lean 证据。",
        "静态快照核查：38 个带 `(Lean)` 状态的条目中，当前 FormalConjectures 上游能匹配到 26 个同号题面文件；26 个全部仍含 `sorry`，其中 18 个仅通过 `formal_proof` 注解指向外部证明。因此 benchmark 文件本身一律不计作闭合证书。",
        "",
        "闭合判定含义：",
        "",
        "- `closed_verified`：本轮已找到并核对足以闭合精确题面的证据链。",
        "- `closed_scope_caveat`：主体结论可信，但版本、子问、定义、形式化声明或仅有未评审/条件化证据等存在必须保留的说明。",
        "- `evidence_incomplete`：官方标签可能正确，但公开证据或可复现检查不足，不能独立确认。",
        "- `status_or_statement_mismatch`：状态、字面题面与实际解决对象之间有实质错配。",
        "",
        "## 覆盖与结构质检",
        "",
        "| 工作流 | 预期 | 已完成 | 缺失 | cohort 外结果 |",
        "|---|---:|---:|---:|---:|",
        f"| 已非开放状态证据 | {len(nonopen_expected)} | {len(nonopen_by_id)} | {len(nonopen_missing)} | {len(nonopen_unexpected)} |",
        f"| 官方开放冲突 | {len(OPEN_CONFLICT_IDS)} | {len(conflicts_by_id)} | {len(conflict_missing)} | {len(conflict_unexpected)} |",
        f"| 优先证明路线 | {len(PRIORITY_IDS)} | {len(proof_payloads)} | {len(proof_missing)} | {len(proof_unexpected)} |",
        "",
        f"证明路线累计代理墙钟时间 {total_proof_seconds / 3600:.2f} 小时；单题最长 {max_proof_seconds:.1f} 秒，硬上限 7200 秒。",
        "",
    ]

    if nonopen_missing or conflict_missing or proof_missing:
        lines.extend(
            [
                "> 当前文档仍是进行中快照。缺失 ID："
                f"非开放 `{','.join(nonopen_missing) or '无'}`；"
                f"开放冲突 `{','.join(conflict_missing) or '无'}`；"
                f"证明路线 `{','.join(proof_missing) or '无'}`。",
                "",
            ]
        )

    lines.extend(
        [
            "## 核心结论摘要",
            "",
            (
                "80 条机械意义上的非 `open` 记录中，本轮判为 "
                f"`closed_verified` {closure_counts.get('closed_verified', 0)} 条、"
                f"`closed_scope_caveat` {closure_counts.get('closed_scope_caveat', 0)} 条、"
                f"`evidence_incomplete` {closure_counts.get('evidence_incomplete', 0)} 条、"
                f"`status_or_statement_mismatch` {closure_counts.get('status_or_statement_mismatch', 0)} 条。"
            ),
            "",
            "- #114、#488 的 `falsifiable` 不是闭合状态；#358 的现有公开稿有作者已承认、尚待修订的具体缺口；#948 的公开 Lean 源码已在独立 Mathlib v4.28.0 环境编译并通过公理审计，现改判为精确闭合。",
            "- #690 的原普遍单峰猜想已有同行评审反例；所有 k 的完整分类另由 2026 年 arXiv v1 与有限验证器支持，仍保留未评审解析论证的证据层级说明。",
            "- #783 的 `SOLVED` 对应后来修订的渐近版本，不等同于冻结题面的逐个有限 n 精确分类；#1022 的数学与 Lean 证据都在证明否命题，官网 `PROVED (LEAN)` 方向应为 `DISPROVED (LEAN)`。",
            "- 24 条官网仍 `OPEN` 的冲突中，12 条只是字面错误版本已被反驳而意图版本仍开放；#520 的上轮结论引用了不存在的新版，已撤销；#920 很可能是状态同步滞后；#550、#1070 只有近期预印本/计算证书级的新声称。",
            "- #1039 的公开候选解已在两个独立克隆中通过 3316-job Lean 构建，并通过逐式数学复核，得到 log(2)/n≤rho_n≤pi/(2n)；官网主体更新时间早于该材料，仍显示 OPEN/claimed solution。",
            "- #776 得到候选新定理 g(2r+3,r)≤2r−1（r≥4），从而 n₀(r)≥2r+3；证明已由第二位代理逐步复核，并独立重跑 r=4,5 的全部 Z3 轨道和覆盖引理穷举，但它仍是未发表、待外部同行评审的新结果，不是 #776 的完整解答。",
            "- #934 的旧 t=3 精确/渐近路线已被 O₄=KG(7,3) 及其射影平面放大严格证伪；q=7 给出 Δ=32、31920 条坏图边，超过旧猜想允许的 31777 条。该反例已通过独立数学审计和程序重放；原问题的新最优常数上界仍开放。",
            "- #963 经独立核分类审阅与程序重放，严格计算机辅助建立 F(3)=13；同时核实渐近界 f(n)≥(1−o(1))log₂n 已由 KoishiChan 于 2025-12-05 在官方论坛公开，本轮修补了 Γ 与短区间端点。主页仍标 OPEN，且该证明尚无论文、预印本或 Lean 版本。",
            "- #1063 得到并独立复核新下界 D(k)|d_e、primorial 子序列超多项式增长及 k≥3 的 LCM 上界修复；它把候选稀疏化为 n=mD(k)+e，但尚未控制 m，故严格改进统一渐近上界的目标仍开放。",
            "",
        ]
    )

    lines.extend(
        [
            "## 第一部分：80 道已非开放题的证据闭合审计",
            "",
            "### 判定分布",
            "",
            "| 判定 | 数量 |",
            "|---|---:|",
        ]
    )
    for verdict, count in sorted(closure_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {table(verdict)} | {count} |")
    lines.extend(
        [
            "",
            "证据层级按题计数（可重叠；同一题可同时有论文、预印本和 Lean）：",
            "",
            "| 证据层级 | 题数 |",
            "|---|---:|",
        ]
    )
    for bucket, count in sorted(
        nonopen_evidence_buckets.items(), key=lambda pair: (-pair[1], pair[0])
    ):
        lines.append(f"| {table(bucket)} | {count} |")
    lines.extend(["", "### 总表", "", "| # | 官方状态 | 证据类型 | 闭合判定 | 核心结论 |", "|---:|---|---|---|---|"])
    for problem_id in nonopen_expected:
        row = nonopen_by_id.get(problem_id, {})
        types = sorted(
            {evidence_bucket(item) for item in row.get("evidence", []) if isinstance(item, dict)}
        )
        if len(types) > 1 and "官方记录" in types:
            types.remove("官方记录")
        lines.append(
            f"| {problem_id} | {table(cohort_by_id[problem_id].get('current_status'))} | "
            f"{table(', '.join(types) or 'pending')} | {table(row.get('closure_verdict', 'pending'))} | "
            f"{table(row.get('closure_reason_zh', '尚未完成'))} |"
        )

    lines.extend(["", "### 逐题证据记录", ""])
    for problem_id in nonopen_expected:
        problem = cohort_by_id[problem_id]
        row = nonopen_by_id.get(problem_id)
        lines.extend(
            [
                f"#### #{problem_id}",
                "",
                f"- 官方状态：`{problem.get('current_status')}`",
                f"- 精确题面：{clean(problem.get('statement'))}",
            ]
        )
        if not row:
            lines.extend(["- 审计状态：`pending`", ""])
            continue
        lines.extend(
            [
                f"- 范围解释：{clean(row.get('statement_scope_zh'))}",
                f"- 闭合判定：`{clean(row.get('closure_verdict'))}`",
                f"- 判定理由：{clean(row.get('closure_reason_zh'))}",
                f"- Lean 审计：{clean(row.get('lean_audit_zh'))}",
                f"- 尚存不确定性：{clean(row.get('remaining_uncertainty_zh'))}",
                "- 证据：",
                "",
            ]
        )
        evidence_rows = row.get("evidence", [])
        if not evidence_rows:
            lines.append("  - 未找到可独立检查的公开证据。")
        for evidence in evidence_rows:
            lines.append(
                f"  - `{clean(evidence.get('type'))}` {linked_title(evidence)}；"
                f"发表状态：{clean(evidence.get('publication_state'))}；"
                f"核验：{clean(evidence.get('inspection_zh'))}"
            )
        lines.append("")

    lines.extend(
        [
            "## 第二部分：24 道官方仍开放但初筛冲突的核验",
            "",
            "### 判定分布",
            "",
            "| 判定 | 数量 |",
            "|---|---:|",
        ]
    )
    for verdict, count in sorted(conflict_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {table(verdict)} | {count} |")
    lines.extend(
        [
            "",
            "判定口径：`literal_false_intended_open` 表示冻结字面版已假、但维护者意图中的修正版仍开放；"
            "`still_open_correct` 表示初筛没有发现足以更新状态的新证据；"
            "`initial_analysis_wrong` 表示上轮分析本身有误；"
            "`recent_claim_unverified` 表示只有近期预印本或计算声称，尚不足以确认官方闭合；"
            "`likely_status_stale` 表示已有较强的新闭合证据、官网很可能尚未同步；"
            "`independence_scope_mismatch` 表示独立性/形式系统结论与原数学题范围不一致。",
            "",
            "### 总表",
            "",
            "| # | 审计判定 | 为何仍开放/是否应更新 |",
            "|---:|---|---|",
        ]
    )
    for problem_id in OPEN_CONFLICT_IDS:
        row = conflicts_by_id.get(problem_id, {})
        lines.append(
            f"| {problem_id} | {table(row.get('audit_verdict', 'pending'))} | "
            f"{table(row.get('reason_official_open_zh', '尚未完成'))} |"
        )

    lines.extend(["", "### 逐题冲突记录", ""])
    for problem_id in OPEN_CONFLICT_IDS:
        problem = cohort_by_id[problem_id]
        row = conflicts_by_id.get(problem_id)
        initial = read_json(INITIAL_ROOT / "results" / f"{problem_id}.json", default={}).get(
            "analysis", {}
        )
        lines.extend(
            [
                f"#### #{problem_id}",
                "",
                f"- 官方题面：{clean(problem.get('statement'))}",
                f"- 上轮初筛：`{clean(initial.get('verdict'))}`；{clean(initial.get('status_note_zh'))}",
            ]
        )
        if not row:
            lines.extend(["- 审计状态：`pending`", ""])
            continue
        lines.extend(
            [
                f"- 字面命题：{clean(row.get('literal_statement_zh'))}",
                f"- 当前预期开放范围：{clean(row.get('intended_or_current_open_scope_zh'))}",
                f"- 上轮声称：{clean(row.get('initial_claim_zh'))}",
                f"- 审计判定：`{clean(row.get('audit_verdict'))}`",
                f"- 闭合评估：{clean(row.get('closure_assessment_zh'))}",
                f"- 官方仍开放原因：{clean(row.get('reason_official_open_zh'))}",
                f"- 下一核验动作：{clean(row.get('next_verification_zh'))}",
                "- 证据：",
                "",
            ]
        )
        for evidence in row.get("evidence", []):
            lines.append(
                f"  - `{clean(evidence.get('type'))}` {linked_title(evidence)}；"
                f"发表状态：{clean(evidence.get('publication_state'))}；"
                f"核验：{clean(evidence.get('inspection_zh'))}"
            )
        if not row.get("evidence"):
            lines.append("  - 未找到可独立检查的公开证据。")
        lines.append("")

    lines.extend(
        [
            "## 第三部分：23 条优先路线的最长两小时续攻",
            "",
            "### 结论分布",
            "",
            "| 结论 | 数量 |",
            "|---|---:|",
        ]
    )
    for conclusion, count in sorted(proof_counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(f"| {table(conclusion)} | {count} |")
    lines.extend(
        [
            "",
            "`route_advanced` 表示得到严格的新引理、界或更窄的下一定理；"
            "`route_refuted` 表示预定路线的核心目标被反例击穿；"
            "`route_blocked` 表示复核后没有越过首个明确障碍；"
            "`candidate_full_proof`/`candidate_counterexample` 只在精确量词闭合时使用，仍须看随附的独立审阅与证据层级。",
            "",
            "### 总表",
            "",
            "| # | 用时 | 结论 | 下一精确定理/任务 |",
            "|---:|---:|---|---|",
        ]
    )
    for problem_id in PRIORITY_IDS:
        payload = proof_payloads.get(problem_id, {})
        item = payload.get("analysis", {})
        lines.append(
            f"| {problem_id} | {float(payload.get('elapsed_seconds', 0)):.1f} 秒 | "
            f"{table(item.get('conclusion', 'pending'))} | {table(item.get('next_theorem_zh', '尚未完成'))} |"
        )

    lines.extend(["", "### 逐题续攻记录", ""])
    for problem_id in PRIORITY_IDS:
        problem = cohort_by_id[problem_id]
        initial = read_json(INITIAL_ROOT / "results" / f"{problem_id}.json", default={}).get(
            "analysis", {}
        )
        payload = proof_payloads.get(problem_id)
        lines.extend(
            [
                f"#### #{problem_id}",
                "",
                f"- 精确题面：{clean(problem.get('statement'))}",
                f"- 上轮下一步：{clean(initial.get('next_action_zh'))}",
            ]
        )
        if not payload:
            lines.extend(["- 续攻状态：`pending`", ""])
            continue
        item = payload["analysis"]
        lines.extend(
            [
                f"- 用时：{float(payload.get('elapsed_seconds', 0)):.1f} 秒（硬上限 {int(payload.get('hard_timeout_seconds', 7200))} 秒）",
                f"- 路线目标：{clean(item.get('route_goal_zh'))}",
                f"- 结论：`{clean(item.get('conclusion'))}`；完整解声明：`{clean(item.get('full_solution_claim'))}`；置信度：`{clean(item.get('confidence'))}`",
                "- 实际尝试：",
                "",
            ]
        )
        verification = independent_verifications.get(problem_id, {})
        if verification:
            if verification.get("build"):
                build = verification.get("build", {})
                lines.extend(
                    [
                        f"- 独立机器核验：`{clean(verification.get('verdict'))}`；"
                        f"提交 `{clean(verification.get('commit'))}`；"
                        f"`{clean(build.get('command'))}` 退出码 {int(build.get('exit_code', -1))}，"
                        f"共 {int(build.get('jobs', 0))} 个构建任务。",
                        f"- 机器核验范围：{clean(verification.get('scope_check_zh'))}",
                        f"- 独立数学复核：{clean(verification.get('independent_math_review_zh'))}",
                        f"- 机器证据层级：{clean(verification.get('evidence_level_zh'))}",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"- 独立复核：`{clean(verification.get('verdict'))}`；"
                        f"范围：{clean(verification.get('verified_scope'))}",
                        f"- 复核方式：{clean(verification.get('review_mode'))}",
                        f"- 证据边界：{clean(verification.get('caveat_zh'))}",
                        "",
                    ]
                )
        for attempt in item.get("attempts", []):
            lines.append(
                f"  - **{clean(attempt.get('label_zh'))}**（`{clean(attempt.get('outcome'))}`）："
                f"{clean(attempt.get('method_zh'))}；推导：{clean(attempt.get('derivation_zh'))}"
            )
        lines.extend(["", "- 严格推进："])
        for progress in item.get("rigorous_progress_zh", []):
            lines.append(f"  - {clean(progress)}")
        if not item.get("rigorous_progress_zh"):
            lines.append("  - 未得到可独立陈述的严格推进。")
        lines.extend(["", "- 路线证伪/边界检查："])
        for check in item.get("falsification_checks_zh", []):
            lines.append(f"  - {clean(check)}")
        if not item.get("falsification_checks_zh"):
            lines.append("  - 未记录。")
        lines.extend(["", "- 可复现计算："])
        for artifact in item.get("computational_artifacts", []):
            artifact_path = clean(artifact.get("artifact_path"))
            linked_path = f"[{artifact_path}]({artifact_path})" if artifact_path else "未给路径"
            lines.append(
                f"  - {linked_path}：{clean(artifact.get('description_zh'))}；"
                f"命令 `{clean(artifact.get('reproduce_command'))}`；结果：{clean(artifact.get('result_zh'))}"
            )
        if not item.get("computational_artifacts"):
            lines.append("  - 本轮未产生计算产物。")
        lines.extend(
            [
                "",
                f"- 第一阻塞点：{clean(item.get('blocking_step_zh'))}",
                f"- 下一精确定理：{clean(item.get('next_theorem_zh'))}",
                "- 研究记录：",
                "",
                multiline(item.get("proof_note_zh")),
                "",
                "- 一手来源：",
                "",
            ]
        )
        for source in item.get("sources_checked", []):
            lines.append(
                f"  - {linked_title(source)}；一手来源：`{str(bool(source.get('primary_source'))).lower()}`；"
                f"核验：{clean(source.get('verified_claim_zh'))}"
            )
        if not item.get("sources_checked"):
            lines.append("  - 本轮没有成功核对一手来源。")
        lines.append("")

    atomic_write_text(REPORT_PATH, "\n".join(lines).rstrip() + "\n")
    summary = {
        "schema_version": "amra.erdos_80_24_23_followup_report.v1",
        "nonopen": {
            "expected": len(nonopen_expected),
            "completed": len(nonopen_by_id),
            "missing": nonopen_missing,
            "unexpected": nonopen_unexpected,
            "closure_verdicts": dict(closure_counts),
            "evidence_buckets_by_problem": dict(nonopen_evidence_buckets),
        },
        "open_conflicts": {
            "expected": len(OPEN_CONFLICT_IDS),
            "completed": len(conflicts_by_id),
            "missing": conflict_missing,
            "unexpected": conflict_unexpected,
            "audit_verdicts": dict(conflict_counts),
        },
        "proof_routes": {
            "expected": len(PRIORITY_IDS),
            "completed": len(proof_payloads),
            "missing": proof_missing,
            "unexpected": proof_unexpected,
            "conclusions": dict(proof_counts),
            "total_elapsed_seconds": round(total_proof_seconds, 3),
            "max_elapsed_seconds": round(max_proof_seconds, 3),
        },
        "evidence_record_types": dict(evidence_types),
        "formal_conjectures_snapshot": {
            "repository": "https://github.com/google-deepmind/formal-conjectures",
            "commit": "c252a41054125b5fd9c8356e2137cd9b55337657",
            "lean_status_count": 38,
            "matching_problem_files": 26,
            "matching_files_with_sorry": 26,
            "matching_files_with_formal_proof_link": 18,
            "warning": "Benchmark statement files containing sorry are not proof evidence.",
        },
        "erdos_metadata_snapshots": {
            "current_repository": "https://github.com/teorth/erdosproblems",
            "current_commit": "aab2deceb51aee0ef28c17d8d194249cbee13d7a",
            "prior_repository": "https://github.com/neelsomani/gpt-erdos",
            "prior_commit": "21b48ae6b97279e9fe6781e3744e1cdd835e2cc1",
        },
        "independent_verifications": independent_verifications,
        "report_path": str(REPORT_PATH),
    }
    atomic_write_json(FOLLOWUP_ROOT / "report_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
