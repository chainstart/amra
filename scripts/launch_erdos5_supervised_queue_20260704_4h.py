#!/usr/bin/env python3
"""2026-07-04 continuation for the five Erdos supervised queue."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos5_supervised_queue_20260703_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260704_4h"
PREV_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260703_4h"

COMPLETED_PROMOTIONS = {
    "ShaffafSolymosiDeZeeuwContainmentForRationalDistanceSetsAssumingBombieriLang",
    "beatty_prime_pair_vonMangoldt_hypothesis_source_contract",
    "ces75_theorem4_even_count_case_reduction_from_source",
}


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos5_queue_base_20260703", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base launcher: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def text_has_any(text: str, patterns: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def make_strict_promotion_gate(base: Any):
    deny_patterns = (
        "not lean",
        "not a lean",
        "do not run lean",
        "do not promote",
        "do not queue lean",
        "do not allocate formalizer",
        "source mode, not lean",
        "proof-lab/source mode, not lean",
        "source theorem, not a lean promotion target",
        "stop this lean",
        "stop this promotion",
        "no trusted lean",
        "no imported lean proof",
        "missing accepted provenance",
        "source-blocked",
    )
    allow_patterns = (
        "promote only the local wrapper",
        "local wrapper",
        "local glue",
        "local certificate",
        "lean formalizer",
        "run the next round as a lean",
        "run next round as a lean",
        "formalizer/certificate",
        "queued promotion",
    )

    def strict_promotion_request_from_report(report: dict[str, Any], target: dict[str, Any]) -> dict[str, Any] | None:
        decisions = list(report.get("supervisor_decisions") or [])
        latest_decision = decisions[-1] if decisions else {}
        requeue = dict(latest_decision.get("requeue") or {})
        control_action = str(latest_decision.get("control_action") or "")
        instructions = str(latest_decision.get("next_work_direction") or "")
        theorem = (
            str(requeue.get("next_target_theorem") or "").strip()
            or str(latest_decision.get("target_theorem") or "").strip()
            or str(report.get("current_target_theorem") or "").strip()
            or str(target["lean"].get("fallback_target") or "").strip()
        )
        if not theorem or theorem in COMPLETED_PROMOTIONS:
            return None
        text = " ".join(
            [
                control_action,
                instructions,
                str(latest_decision.get("decision") or ""),
                str(report.get("stop_reason") or ""),
                theorem,
            ]
        )
        if text_has_any(text, deny_patterns):
            return None
        if "source" in theorem.lower() and "of_source" not in theorem and "wrapper" not in text.lower():
            return None
        if not text_has_any(text, allow_patterns):
            return None
        return {
            "target_slug": target["slug"],
            "problem": target["problem"],
            "target_theorem": theorem,
            "source_report_path": report.get("summary_path") or report.get("run_dir") or "",
            "stop_reason": report.get("stop_reason") or "",
            "control_action": control_action,
            "decision_path": latest_decision.get("decision_path") or "",
            "instructions": instructions,
        }

    return strict_promotion_request_from_report


def source_constraints_v2() -> str:
    return """\
Execution policy for this campaign:
- Use AMRA `run-campaign-loop` with global supervisor every round.
- Natural-language/source proof-lab work may proceed freely across all five problems.
- Lean promotion is allowed only for genuinely local wrappers, local glue, or finite
  certificates. Source theorem placeholders must stay in proof-lab/source mode.
- If the next node is an external source theorem, the supervisor should keep the
  controller in proof-lab/source mode and state the exact source or certificate blocker.
- Do not run Lean inside the source/proof-lab stage.
- Do not run `lake build`, `lake update`, `lake exe cache get`, aggregate imports, or
  whole-project Lean checks.
- The main theorem remains the target; stage theorems are valuable only when they shorten
  the path to the original Erdos statement.
"""


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.MAX_SOURCE_CYCLES_PER_TARGET = 6
    base.MAX_PROMOTIONS_PER_TARGET = 2
    base.source_hard_constraints = source_constraints_v2
    base.promotion_request_from_report = make_strict_promotion_gate(base)

    by_slug = {target["slug"]: target for target in base.TARGETS}
    amra_dir = base.AMRA_FORMAL / "AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704"
    fc_dir = base.FORMAL_CONJECTURES / "FormalConjectures/ErdosProblems/ErdosFiveQueue20260704"

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "BombieriLangConditionalRationalDistanceNondensityPackage",
            "statement": """\
# Erdos #212: conditional rational-distance nondensity package

上一轮已经 Lean 验证了 `ShaffafSolymosiDeZeeuwContainmentForRationalDistanceSetsAssumingBombieriLang`。
本轮不要重复这个 bridge。目标是 source-audit 精确条件：Shaffaf 与
Solymosi-de Zeeuw 给出的有限例外/线或圆覆盖定理，是否足以在 Bombieri-Lang
或弱 Bombieri-Lang 假设下推出原题的非稠密结论。

只在发现新的本地拓扑/有限例外 wrapper 时请求 Lean promotion；外部代数几何定理
必须保持 source theorem blocker。
""",
            "source_contexts": base.existing(
                PREV_ROOT / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-01/summary.md",
                PREV_ROOT / "lean_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-lean-promotion-01/summary.md",
                "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos212-rational-distance-density-route/erdos212-rational-distance-density-route-prooflab-4h/supervisor/round-004/decision.md",
            ),
        }
    )
    by_slug["erdos212-rational-distance-density"]["lean"].update(
        {
            "target_file": amra_dir / "Erdos212.lean",
            "fallback_target": "BombieriLangConditionalRationalDistanceNondensityPackage",
            "seed": """\
import AmraLibrary.OpenProblemBatches.ErdosFiveQueue20260703.Erdos212

namespace AmraErdosFiveQueue20260704
namespace Erdos212

/- 2026-07-04 continuation file.  Do not reprove the already verified
   Bombieri-Lang conditional containment bridge; add only new local wrappers. -/

end Erdos212
end AmraErdosFiveQueue20260704
""",
            "contexts": base.existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260703/Erdos212.lean"
            ),
        }
    )

    by_slug["erdos972-beatty-prime-pair"].update(
        {
            "initial_target": "BeattyPrimePairLowerBoundSourceOrFreeze",
            "statement": """\
# Erdos #972: Beatty prime-pair source lower bound

上一轮已经 Lean 验证了条件 bridge：
`beatty_prime_pair_vonMangoldt_hypothesis_source_contract`。本轮不要重复该条件
定理。主攻源定理：对每个 irrational `α > 1`，是否存在可引用的
Beatty prime-pair 下界或 von Mangoldt 相关估计，足以推出无限多
`p` 且 `⌊αp⌋` 也为素数。

若没有精确源定理，输出 freeze package；只有新的本地“下界 -> 无限性” wrapper
才允许 Lean promotion。
""",
            "source_contexts": base.existing(
                PREV_ROOT / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-01/summary.md",
                PREV_ROOT / "lean_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-lean-promotion-01/summary.md",
                "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos972-beatty-prime-pair-route/erdos972-beatty-prime-pair-route-prooflab-4h/supervisor/round-004/decision.md",
            ),
        }
    )
    by_slug["erdos972-beatty-prime-pair"]["lean"].update(
        {
            "target_file": amra_dir / "Erdos972.lean",
            "fallback_target": "BeattyPrimePairLowerBoundSourceOrFreeze",
            "seed": """\
import AmraLibrary.OpenProblemBatches.ErdosFiveQueue20260703.Erdos972

namespace AmraErdosFiveQueue20260704
namespace Erdos972

/- 2026-07-04 continuation file.  The analytic Beatty prime-pair lower bound
   remains a source theorem unless a new local wrapper is identified. -/

end Erdos972
end AmraErdosFiveQueue20260704
""",
            "contexts": base.existing(
                "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260703/Erdos972.lean"
            ),
        }
    )

    by_slug["erdos1052-unitary-perfect"].update(
        {
            "initial_target": "UPNSeedClosureBoundSourceOrFiniteCertificate",
            "statement": """\
# Erdos #1052: unitary perfect finiteness source/certificate search

上一轮明确冻结了无来源的 `threeHiggs_phi4p_eventual_failure` 和
`UPN_seed_closure_bound` Lean promotion。当前第一阻塞是：没有具体源定理或有限证书
证明全局 2-adic seed/exponent bound。

本轮只做 source/certificate 攻关：寻找可引用定理、可计算有限证书方案，或证明
该 exact-balance 路线应冻结。除非先给出具体 citation/bound/verifier obligations，
不要请求 Lean promotion。
""",
            "source_contexts": base.existing(
                PREV_ROOT / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-03/summary.md",
                PREV_ROOT / "lean_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-lean-promotion-02/summary.md",
                "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos1052-unitary-perfect-route/erdos1052-unitary-perfect-route-prooflab-4h/supervisor/round-002/decision.md",
            ),
        }
    )
    by_slug["erdos1052-unitary-perfect"]["lean"].update(
        {
            "target_file": fc_dir / "Erdos1052Queue.lean",
            "fallback_target": "UPNSeedClosureBoundSourceOrFiniteCertificate",
            "seed": """\
import FormalConjectures.ErdosProblems.ErdosFiveQueue20260703.Erdos1052Queue

namespace Erdos1052

/- 2026-07-04 continuation file.  Lean work is blocked until a concrete source
   theorem or finite certificate for the global seed bound is supplied. -/

end Erdos1052
""",
            "contexts": base.existing(
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1052Queue.lean"
            ),
        }
    )

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "CES75EvenCountDichotomySourceExistsStatement",
            "statement": """\
# Erdos #866: CES75 even-count dichotomy source certification

上一轮 Lean 已验证本地 wrapper：
`ces75_theorem4_even_count_case_reduction_from_source`。主命题还差外部 CES75
dichotomy source theorem。当前目标不是再证 wrapper，而是把 CES75 原文中的
even-count dichotomy 源定理认证到精确形状：常数 `cCES/Nces`、`24 < cCES`、
strict residual endpoint、central-even filter、direct six-witness alternative。

只有发现新的纯本地 glue theorem 才请求 Lean promotion；不要把 CES75 源定理本身
当作 Lean promotion 目标。
""",
            "source_contexts": base.existing(
                PREV_ROOT / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-02/summary.md",
                PREV_ROOT / "lean_runs/erdos866-g6-ces75/erdos866-g6-ces75-lean-promotion-02/summary.md",
                "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos866-ces75-corollary-source-cert-phase2/erdos866-ces75-corollary-source-cert-phase2-4h/summary.md",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "target_file": base.ERDOS866_FORMAL / "MathProject/ErdosFiveQueue20260704.lean",
            "fallback_target": "CES75EvenCountDichotomySourceExistsStatement",
            "seed": """\
import MathProject.ErdosFiveQueue20260703

namespace MathProject

/- 2026-07-04 continuation file.  Do not restate the already verified local
   wrapper unless a genuinely smaller glue theorem is identified. -/

end MathProject
""",
            "contexts": base.existing(
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260703.lean"
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "HarborthContactNumberSourceImportMechanism",
            "statement": """\
# Erdos #1084: Harborth source/import mechanism

上一轮最终冻结：缺 Harborth/Bezdek-Khan 平面接触数定理在本地 `unitDistNum`
约定下的可信 Lean import/source theorem 机制。不要再把
`HarborthUnitDistNumUpperGe4Source` 或 `harborth_unitDistNum_upper_ge4` 直接提升
Lean，除非先提供独立形式化或可接受的 source-theorem 机制。

本轮主攻 source/import governance：精确列出 theorem payload、缩放 bridge、contact
edge counting convention，以及 AMRA 中可接受的导入方式。若无机制，输出 freeze
package 和后续外部任务。
""",
            "source_contexts": base.existing(
                PREV_ROOT / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-03/summary.md",
                PREV_ROOT / "lean_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-lean-promotion-02/summary.md",
                "artifacts/open_problem_screening/latest/erdos2_phase2_light_lean_20260702/runs/erdos1084-harborth-package-phase2/erdos1084-harborth-package-phase2-4h/summary.md",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "target_file": fc_dir / "Erdos1084Queue.lean",
            "fallback_target": "HarborthContactNumberSourceImportMechanism",
            "seed": """\
import FormalConjectures.ErdosProblems.ErdosFiveQueue20260703.Erdos1084Queue

namespace Erdos1084

/- 2026-07-04 continuation file.  Lean is blocked until the Harborth source
   theorem is independently formalized or accepted through a source-theorem mechanism. -/

end Erdos1084
""",
            "contexts": base.existing(
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean"
            ),
        }
    )
    return base


def launch(base: Any) -> dict[str, Any]:
    base.prepare_targets()
    for sub in ("logs", "source_statements", "lean_statements", "source_runs", "lean_runs"):
        (base.RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": base.utc_now(),
        "run_root": str(base.RUN_ROOT),
        "time_budget_seconds": base.TIME_BUDGET_SECONDS,
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
        "promotion_gate": "strict: only local wrappers/certificates; source theorem placeholders stay source-only",
        "targets": [
            {
                "slug": target["slug"],
                "problem": target["problem"],
                "final_target": target["final_target"],
                "initial_target": target["initial_target"],
                "lean_workspace": str(target["lean"]["workspace"]),
                "lean_target_file": str(target["lean"]["target_file"]),
                "lean_build_command": base.single_file_build_command(Path(target["lean"]["workspace"]), Path(target["lean"]["target_file"])),
            }
            for target in base.TARGETS
        ],
    }
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    scheduler_log = base.RUN_ROOT / "logs/scheduler.log"
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
        "run_root": str(base.RUN_ROOT),
        "scheduler_pid": proc.pid,
        "scheduler_log": str(scheduler_log),
        "manifest_path": str(base.RUN_ROOT / "manifest.json"),
        "queue_status_path": str(base.RUN_ROOT / "queue_status.json"),
        "source_target_count": len(base.TARGETS),
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
        "mode": "5 supervised proof-lab campaigns plus strict queued lean-formalizer promotions",
    }
    base.write_text(base.RUN_ROOT / "scheduler.pid", str(proc.pid))
    base.write_json(base.RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    base = configure(load_base())
    if "--worker" in sys.argv:
        base.run_worker()
        return
    print(json.dumps(launch(base), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
