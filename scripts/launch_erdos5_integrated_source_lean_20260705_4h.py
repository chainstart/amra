#!/usr/bin/env python3
"""Integrated five-target Erdos follow-up with source search and Lean queue.

This 2026-07-05 launcher intentionally attacks all five targets:
- #866: downstream local wrapper after accepting the CES75 k=5 source certificate.
- #212: exact projective-variety Weak Lang conditional package.
- #1052: Maciejewski/certificate archive and Phi_(4p)(2) tail cutoff audit.
- #972: Li-Pan/citation-chain search for all-irrational Beatty prime-pair bounds.
- #1084: Harborth/Bezdek-Khan provenance audit and local source wrapper if accepted.

Source/proof-lab runs use AMRA `run-campaign-loop --search`.  Lean promotions
are enabled, but the inherited strict gate admits only local wrappers,
local glue, or finite certificates; external source theorem placeholders stay
in source/proof-lab.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
BASE_PATH = REPO / "scripts/launch_erdos5_supervised_queue_20260704_4h.py"
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos5_integrated_source_lean_20260705_4h"
PREV_MAIN = REPO / "artifacts/open_problem_screening/latest/erdos5_866_mainline_20260704_4h"
PREV_TIERED = REPO / "artifacts/open_problem_screening/latest/erdos5_tiered_followup_20260704_4h"
PREV_QUEUE = REPO / "artifacts/open_problem_screening/latest/erdos5_supervised_queue_20260704_4h"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("erdos5_queue_20260704", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base launcher: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.configure(module.load_base())


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def configure(base: Any) -> Any:
    base.RUN_ROOT = RUN_ROOT
    base.TIME_BUDGET_SECONDS = 4 * 60 * 60
    base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60
    base.LEAN_SLOT_LIMIT = 2
    base.MAX_SOURCE_CYCLES_PER_TARGET = 4
    base.MAX_PROMOTIONS_PER_TARGET = 2

    by_slug = {target["slug"]: target for target in base.TARGETS}

    by_slug["erdos866-g6-ces75"].update(
        {
            "initial_target": "CES75K5CertificateFeedsEvenCountDichotomyWrapper",
            "statement": """\
# Erdos #866: consume accepted CES75 k=5 certificate and build downstream wrapper

Do not re-discover the CES75 k=5 source certificate.  The previous supervised
run judged `CES75K5EvenSequenceCorollarySourceCertificate` source content closed
as an external Choi-Erdos-Szemeredi 1975 certificate:
Lemma A/corollary at `k = 5`, existential `n0(5)`, strict
`32 * N^(31/32)` threshold, sorted duplicate-free `Finset Z` transfer, six
distinct witnesses, and the direct/lower-tail/reflected-tail uses.

This round should attack the first downstream node:
`CES75K5CertificateFeedsEvenCountDichotomyWrapper`.  Treat the k=5 certificate
as a source theorem assumption and prove or specify the local wrapper that
feeds:
- direct branch `N = n`;
- lower tail `N = 20*t`;
- reflected upper tail `x -> 2*n + 2 - x` with witness pullback.

If this wrapper is local Lean glue, explicitly request queued Lean promotion.
Use only small single-file Lean checks; no full build.

Primary source to cite/check if needed:
https://users.renyi.hu/~p_erdos/1975-39.pdf
""",
            "source_contexts": existing(
                PREV_MAIN / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-14/summary.md",
                PREV_MAIN / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-14/supervisor/round-002/decision.md",
                PREV_TIERED / "source_runs/erdos866-g6-ces75/erdos866-g6-ces75-source-cycle-07/summary.md",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260703.lean",
            ),
        }
    )
    by_slug["erdos866-g6-ces75"]["lean"].update(
        {
            "fallback_target": "CES75K5CertificateFeedsEvenCountDichotomyWrapper",
            "contexts": existing(
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260704.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosFiveQueue20260703.lean",
                "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            ),
        }
    )

    by_slug["erdos212-rational-distance-density"].update(
        {
            "initial_target": "ProjectiveVarietyWeakLangConditionalRationalDistanceNondensityPackage",
            "statement": """\
# Erdos #212: exact conditional source package, not premature freeze

Use web/paper search and source audit.  Finalize the exact conditional theorem:
assuming Weak Lang/Bombieri-Lang for every projective variety of general type
over every number field, with singular varieties handled by desingularization
or big-canonical convention, every rational-distance set `S subset R^2` is not
Zariski dense in `P^2_C`; if `S` is infinite, all but at most 4 points lie on a
real affine line or all but at most 3 points lie on a real affine circle.

Audit source chain:
- ABT arXiv:1901.02616, especially Definition 2.1, Conjecture 2.2,
  Proposition 3.6;
- Shaffaf arXiv:1501.00159, Lemma 2 and Theorems 1-2;
- Solymosi-de Zeeuw arXiv:0806.3095, Theorems 2.1/2.2.

Do not re-promote the already verified local bridge.  If a genuinely new local
finite-exception wrapper appears, request Lean promotion; otherwise produce the
source theorem/spec package.
""",
            "source_contexts": existing(
                PREV_MAIN / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-01/summary.md",
                PREV_MAIN / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-01/supervisor/round-007/decision.md",
                PREV_QUEUE / "source_runs/erdos212-rational-distance-density/erdos212-rational-distance-density-source-cycle-04/summary.md",
            ),
        }
    )

    by_slug["erdos1052-unitary-perfect"].update(
        {
            "initial_target": "MaciejewskiCertificateAndPhi4pTailCutoffAudit",
            "statement": """\
# Erdos #1052: Maciejewski archive/certificate and Phi_(4p)(2) tail audit

Use web/paper search.  Do not merely restate the obstruction.  Search for the
arXiv paper and any linked ancillary material, repository, factor/primality
transcripts, verifier scripts, or machine-checkable certificates.

Current required audit:
- Maciejewski arXiv:2605.20475 and any ancillary files;
- whether any material gives an explicit global cutoff `B` for the statement:
  every odd 3-Higgs prime `p > B` has a non-3-Higgs prime divisor of
  `Phi_(4*p)(2)`;
- finite verifier obligations for `p <= B`;
- distinguish bounded-box evidence from a theorem closing the global tail.

If a finite certificate/verifier architecture is found, request Lean or
executable-certificate promotion only for the local verifier obligations.
""",
            "source_contexts": existing(
                PREV_MAIN / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-01/summary.md",
                PREV_MAIN / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-01/supervisor/round-002/decision.md",
                PREV_TIERED / "source_runs/erdos1052-unitary-perfect/erdos1052-unitary-perfect-source-cycle-03/summary.md",
            ),
        }
    )

    by_slug["erdos972-beatty-prime-pair"].update(
        {
            "initial_target": "BeattyPrimePairLiPanCitationChainAudit",
            "statement": """\
# Erdos #972: Beatty prime-pair Li-Pan/citation-chain audit

Use web/paper search, not Lean first.  Search Li-Pan and cited-by/citation-chain
sources for an exact theorem proving for every irrational `alpha > 1`:

`#{p < X | Prime p and Prime floor(alpha*p)} >>_alpha X/(log X)^2`

or an equivalent positive `Lambda(p) Lambda(floor(alpha*p))` correlation with
the same floor convention, strong enough to imply infinitely many witnesses.

Known nearby material includes results on primes in Beatty sequences,
Piatetski-Shapiro primes in intersections of Beatty sequences, and almost-all
alpha results.  Do not accept those unless the hypotheses match all irrational
`alpha > 1` and the prime-indexed floor form.

If a matching analytic theorem is found, package it as a source theorem and
connect it to the verified conditional Lean bridge.  If not, produce a checked
source-freeze package listing exact mismatch.
""",
            "source_contexts": existing(
                PREV_MAIN / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-01/summary.md",
                PREV_MAIN / "source_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-source-cycle-01/supervisor/round-001/decision.md",
                PREV_QUEUE / "lean_runs/erdos972-beatty-prime-pair/erdos972-beatty-prime-pair-lean-promotion-01/summary.md",
            ),
        }
    )

    by_slug["erdos1084-harborth-triangular"].update(
        {
            "initial_target": "HarborthBezdekKhanProvenanceAndUnitDistNumWrapper",
            "statement": """\
# Erdos #1084: Harborth/Bezdek-Khan provenance and local unitDistNum wrapper

Use web/paper search.  Do not freeze before auditing provenance.

Tasks:
- obtain/check Harborth, "Loesung zu Problem 664A", Elem. Math. 29 (1974),
  14-15 if available;
- audit Bezdek-Khan arXiv:1601.00145 / journal version, especially the contact
  number theorem and whether it cites Harborth's planar formula;
- verify theorem payload:
  `forall n >= 2, c(n,2) = floor(3*n - sqrt(12*n - 3))`, or at least the needed
  upper bound;
- verify convention: finite non-overlapping congruent planar disks, unordered
  touching pairs, center distance 2 for unit disks;
- connect to local `unitDistNum`: 1-separated point sets, unordered center
  pairs at distance 1, scaling `x -> 2*x`.

If source provenance is accepted, request Lean promotion only for the local
source-to-`unitDistNum` wrapper or any remaining arithmetic bridge.
""",
            "source_contexts": existing(
                PREV_MAIN / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-01/summary.md",
                PREV_MAIN / "source_runs/erdos1084-harborth-triangular/erdos1084-harborth-triangular-source-cycle-01/supervisor/round-001/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
            ),
        }
    )
    by_slug["erdos1084-harborth-triangular"]["lean"].update(
        {
            "fallback_target": "HarborthBezdekKhanProvenanceAndUnitDistNumWrapper",
            "contexts": existing(
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260703/Erdos1084Queue.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/ErdosFiveQueue20260704/Erdos1084Queue.lean",
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
        "policy": "all five targets; proof-lab uses --search; Lean queue enabled only for local wrappers/certificates",
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
        "mode": "integrated five-target source search plus strict two-slot Lean queue",
        "lean_slot_limit": base.LEAN_SLOT_LIMIT,
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
