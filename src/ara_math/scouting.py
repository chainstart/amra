from __future__ import annotations

import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from ara_math.literature import LiteratureHarvester
from ara_math.models import ProblemRecord
from ara_math.problem_bank import load_problem_bank
from ara_math.workspace import read_json, utc_now_iso, write_json


MODERN_TOOL_MAP: dict[str, list[str]] = {
    "computational_search": [
        "bounded exhaustive search with explicit search contracts",
        "certificate-oriented finite verification that can later be mirrored in Lean",
    ],
    "finite_case": [
        "finite-case elimination backed by explicit certificates",
        "SAT or combinatorial search with Lean-checkable postprocessing",
    ],
    "divisors": [
        "multiplicative arithmetic-function lemmas",
        "prime-factor case splits and divisor-sum bounds",
    ],
    "multiplicative_functions": [
        "multiplicativity libraries over divisor sums",
        "prime-power normal forms in Lean",
    ],
    "amicable_numbers": [
        "proper-divisor-sum infrastructure",
        "structural parity and gcd lemmas",
    ],
    "parity": [
        "modular arithmetic and parity obstructions",
    ],
    "geometry": [
        "constraint encodings for admissible configurations",
        "graph-theoretic certificates for geometric impossibility arguments",
    ],
    "additive combinatorics": [
        "density-increment style decomposition",
        "small-case search plus structural lifting",
    ],
    "primes": [
        "prime-factor and congruence lemmas",
        "sieve-inspired bounded elimination",
    ],
    "carmichael_numbers": [
        "squarefree factorization lemmas",
        "criterion-driven decomposition via Korselt-style statements",
    ],
    "weird_numbers": [
        "subset-sum certificates for semiperfectness",
        "search-backed counterexample elimination with explicit bounds",
    ],
}


LOCAL_ERDOS_ASSET_MAP = {
    "633": {
        "project_dir": "erdos-634-triangle",
        "route": [
            "Reuse the triangle-dissection certificate language built for Erdős #634.",
            "Shift from a single finite target to classification lemmas for triangles admitting only square dissection counts.",
        ],
        "ideas": ["finite geometric certificates", "triangle-family classification", "dissection invariants"],
        "linked_banks": ["triangle_dissection_track"],
        "focus_priority": "secondary",
    },
    "1052": {
        "project_dir": "erdos-1052-unitary-perfect",
        "extra_project_dirs": ["unitary-biunitary-perfect-lean4"],
        "route": [
            "Reuse local unitary-divisor theory and odd-unitary-perfect exclusion lemmas.",
            "Separate finiteness arguments from raw search over candidate numbers.",
        ],
        "ideas": ["divisor-sum multiplicativity", "prime-power normal forms", "search-as-certificate"],
        "linked_banks": ["unitary_perfect_track"],
        "focus_priority": "primary",
    },
    "634": {
        "project_dir": "erdos-634-triangle",
        "route": [
            "Formalize known impossibility proofs for n=7 and n=11.",
            "Encode n=19 as a finite certificate or impossibility search problem.",
        ],
        "ideas": ["finite geometric certificates", "graph encodings of dissections"],
        "linked_banks": ["triangle_dissection_track"],
        "focus_priority": "primary",
    },
    "825": {
        "project_dir": "erdos-825-weird",
        "route": [
            "Build weird-number definitions and perform bounded counterexample search.",
            "Use the search data to guide structural lemmas about abundance index.",
        ],
        "ideas": ["counterexample-first scouting", "abundance-index bounds", "subset-sum certificates"],
        "linked_banks": ["weird_numbers_track"],
        "focus_priority": "primary",
    },
}

LITERATURE_SIGNAL_KEYWORDS = {
    "nonexistence": "obstruction_or_nonexistence",
    "no odd": "obstruction_or_nonexistence",
    "bound": "explicit_bound",
    "finitely many": "finiteness_argument",
    "characterization": "classification_result",
    "only ": "classification_result",
    "search": "search_certificate_angle",
    "counterexample": "counterexample_angle",
    "lean": "formalization_asset",
    "formalization": "formalization_asset",
    "theorem": "theorem_narrative",
}

ERDOS_REFERENCE_PATTERN = re.compile(r"(?:问题\s*#|Erd[őo]s\s*#)(\d{1,4})", re.IGNORECASE)
ERDOS_PROJECT_DIR_PATTERN = re.compile(r"erdos-(\d{1,4})(?:-|$)", re.IGNORECASE)
ERDOS_ATTACK_SURFACE_TAGS = {
    "divisors",
    "factorials",
    "primes",
    "geometry",
    "additive basis",
    "arithmetic progressions",
    "additive combinatorics",
}
ERDOS_WEAK_DOMAINS = {"analysis", "ramsey_theory", "set_theory"}
ERDOS_STRONG_DOMAINS = {"number_theory", "geometry", "combinatorics"}


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        cleaned = item.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        output.append(cleaned)
    return output


def _default_formal_math_root() -> Path | None:
    candidate = Path(__file__).resolve().parents[3] / "formal-math"
    if candidate.exists():
        return candidate
    return None


def _is_erdos_problem(problem: ProblemRecord) -> bool:
    metadata = problem.metadata or {}
    source_catalog = str(metadata.get("source_catalog", "")).strip().lower()
    return problem.source == "Erdős Problems" or source_catalog == "erdosproblems"


@lru_cache(maxsize=8)
def _scan_erdos_doc_mentions(formal_math_root_str: str) -> dict[str, dict[str, Any]]:
    root = Path(formal_math_root_str)
    if not root.exists():
        return {}

    candidate_paths: list[Path] = []
    readme_path = root / "README.md"
    if readme_path.exists():
        candidate_paths.append(readme_path)
    docs_root = root / "docs"
    if docs_root.exists():
        candidate_paths.extend(sorted(docs_root.rglob("*.md")))
    for project_dir in sorted(root.glob("erdos-*")):
        if not project_dir.is_dir():
            continue
        candidate_paths.extend(sorted(project_dir.rglob("*.md")))

    mention_map: dict[str, dict[str, Any]] = defaultdict(lambda: {"doc_count": 0, "doc_paths": []})
    for path in candidate_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        numbers = sorted({match.group(1) for match in ERDOS_REFERENCE_PATTERN.finditer(text)})
        if not numbers:
            continue
        for number in numbers:
            entry = mention_map[number]
            entry["doc_count"] += 1
            if len(entry["doc_paths"]) < 8:
                entry["doc_paths"].append(str(path))
    return dict(mention_map)


@lru_cache(maxsize=8)
def _scan_erdos_project_dirs(formal_math_root_str: str) -> dict[str, list[str]]:
    root = Path(formal_math_root_str)
    if not root.exists():
        return {}
    mapping: dict[str, list[str]] = defaultdict(list)
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        match = ERDOS_PROJECT_DIR_PATTERN.match(child.name)
        if not match:
            continue
        mapping[match.group(1)].append(str(child))
    return dict(mapping)


def _extract_erdos_comment(problem: ProblemRecord) -> str:
    metadata = problem.metadata or {}
    comment = str(metadata.get("comments", "")).strip()
    if comment:
        return comment
    notes = problem.notes.strip()
    imported_marker = "Imported from local Erdős metadata."
    if imported_marker in notes:
        return notes.split(imported_marker, 1)[0].strip()
    return ""


def _parse_prize_amount(raw_value: Any) -> int | None:
    value = str(raw_value or "").strip()
    digits = re.findall(r"\d+", value.replace(",", ""))
    if not digits:
        return None
    try:
        return int("".join(digits))
    except ValueError:
        return None


def _problem_statement_is_placeholder(problem: ProblemRecord) -> bool:
    text = problem.statement.lower()
    return "detailed statement should be imported" in text or "recover the exact statement" in text


def _infer_local_assets(problem: ProblemRecord, formal_math_root: Path | None) -> list[dict[str, str]]:
    metadata = problem.metadata or {}
    assets: list[dict[str, str]] = []
    for key in ("local_readme_path", "local_project_dir"):
        value = str(metadata.get(key, "")).strip()
        if value:
            path = Path(value)
            if path.exists():
                assets.append({"kind": key, "path": str(path)})
    if formal_math_root:
        number = problem.problem_id.replace("erdos-", "")
        if number in LOCAL_ERDOS_ASSET_MAP:
            config = LOCAL_ERDOS_ASSET_MAP[number]
            project_dirs = [config["project_dir"], *config.get("extra_project_dirs", [])]
            for project_dir in project_dirs:
                project_path = formal_math_root / project_dir
                project_match = ERDOS_PROJECT_DIR_PATTERN.match(project_path.name)
                is_companion = bool(project_match and project_match.group(1) != number)
                readme_kind = "companion_readme_path" if is_companion else "local_readme_path"
                project_kind = "companion_project_dir" if is_companion else "local_project_dir"
                readme_path = project_path / "README.md"
                if readme_path.exists():
                    assets.append({"kind": readme_kind, "path": str(readme_path)})
                if project_path.exists():
                    assets.append({"kind": project_kind, "path": str(project_path)})
        if _is_erdos_problem(problem):
            project_dir_index = _scan_erdos_project_dirs(str(formal_math_root))
            for project_dir_str in project_dir_index.get(number, []):
                project_path = Path(project_dir_str)
                readme_path = project_path / "README.md"
                if readme_path.exists():
                    assets.append({"kind": "local_readme_path", "path": str(readme_path)})
                assets.append({"kind": "local_project_dir", "path": str(project_path)})
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for asset in assets:
        key = (asset["kind"], asset["path"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(asset)
    return deduped


def _infer_modern_tools(problem: ProblemRecord) -> list[str]:
    tools: list[str] = []
    for tag in problem.tags:
        tools.extend(MODERN_TOOL_MAP.get(tag, []))
    if problem.domain == "number_theory":
        tools.append("Lean formalization over arithmetic lemmas and finite certificates")
    if problem.domain == "geometry":
        tools.append("Lean-checked combinatorial constraints before any continuous geometry search")
    return _dedupe(tools)


def _assess_local_literature(problem: ProblemRecord, local_assets: list[dict[str, str]]) -> dict[str, Any]:
    harvester = LiteratureHarvester()
    source_entries = list(local_assets)
    for reference in problem.references:
        cleaned = str(reference).strip()
        if not cleaned:
            continue
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            continue
        if not Path(cleaned).exists():
            continue
        source_entries.append({"kind": "reference", "path": cleaned})
    deduped_entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in source_entries:
        path = harvester._canonical_source(str(entry.get("path", "")).strip())
        if not path or path in seen:
            continue
        seen.add(path)
        deduped_entries.append({"kind": str(entry.get("kind", "reference")), "source": path})

    if not deduped_entries:
        return {
            "source_count": 0,
            "snapshot_count": 0,
            "skipped_source_count": 0,
            "statement_recoverable": False,
            "candidate_statement_count": 0,
            "best_candidate_statement": "",
            "evidence_signals": [],
            "evidence_summary": [],
        }

    probe = harvester.probe_sources(deduped_entries, problem=problem, allow_network=False)
    evidence = probe["evidence"]
    signals: set[str] = set()
    for snapshot in probe["snapshots"]:
        excerpt = str(snapshot.get("excerpt", "")).lower()
        for needle, label in LITERATURE_SIGNAL_KEYWORDS.items():
            if needle in excerpt:
                signals.add(label)
    if evidence["known_results"]:
        signals.add("known_results_recovered")
    if evidence["proof_ingredients"]:
        signals.add("proof_ingredients_recovered")
    if evidence["modern_tools"]:
        signals.add("modern_tools_recovered")
    if evidence["open_gaps"]:
        signals.add("open_gap_statements_recovered")

    summary: list[str] = []
    if probe["snapshot_count"]:
        summary.append(
            f"Recovered {probe['snapshot_count']} local literature snapshot(s) for readiness analysis."
        )
    if probe["best_candidate"]:
        summary.append("A candidate exact statement can already be recovered from local assets.")
    if signals:
        summary.append("Detected local proof signals: " + ", ".join(sorted(signals)) + ".")

    return {
        "source_count": probe["source_count"],
        "snapshot_count": probe["snapshot_count"],
        "skipped_source_count": probe["skipped_source_count"],
        "statement_recoverable": bool(probe["best_candidate"]),
        "candidate_statement_count": sum(len(snapshot.get("candidate_statements", [])) for snapshot in probe["snapshots"]),
        "best_candidate_statement": str(probe["best_candidate"].get("statement", "")),
        "best_candidate_source": str(probe["best_candidate"].get("source", "")),
        "evidence_signals": sorted(signals),
        "evidence_summary": summary,
        "known_results": evidence["known_results"][:3],
        "proof_ingredients": evidence["proof_ingredients"][:3],
        "modern_tools": evidence["modern_tools"][:3],
        "open_gaps": evidence["open_gaps"][:3],
    }


def _historical_foundations(problem: ProblemRecord, local_assets: list[dict[str, str]]) -> list[str]:
    signals: list[str] = []
    if problem.formalized in {"yes", "partial"}:
        signals.append(f"Existing formalization signal is `{problem.formalized}` in the problem metadata.")
    if problem.references:
        signals.append(f"The bank already records {len(problem.references)} reference(s) for this problem.")
    if problem.notes:
        signals.append(problem.notes)
    if local_assets:
        signals.append("Local formal-math assets exist for this topic, so the track has a nontrivial historical base.")
    return _dedupe(signals)


def _assess_erdos_focus_signal(
    problem: ProblemRecord,
    *,
    formal_math_root: Path | None,
    local_assets: list[dict[str, str]],
) -> dict[str, Any]:
    if not _is_erdos_problem(problem):
        return {
            "number": "",
            "doc_count": 0,
            "doc_paths": [],
            "project_dirs": [],
            "related_banks": [],
            "manual_priority": "",
            "comment": "",
            "focus_notes": [],
        }

    number = problem.problem_id.replace("erdos-", "")
    config = LOCAL_ERDOS_ASSET_MAP.get(number, {})
    doc_signal = {"doc_count": 0, "doc_paths": []}
    project_dirs: list[str] = []
    if formal_math_root:
        doc_signal = _scan_erdos_doc_mentions(str(formal_math_root)).get(number, doc_signal)
        project_dirs = _scan_erdos_project_dirs(str(formal_math_root)).get(number, [])
    comment = _extract_erdos_comment(problem)
    focus_notes: list[str] = []
    if doc_signal["doc_count"]:
        focus_notes.append(
            f"Local formal-math notes mention Erdős #{number} in {doc_signal['doc_count']} markdown file(s)."
        )
    if project_dirs:
        focus_notes.append(
            "A dedicated local Erdős project directory already exists: " + ", ".join(project_dirs[:3]) + "."
        )
    if config.get("focus_priority") == "primary":
        focus_notes.append("Local formal-math strategy notes already treat this as a primary Erdős target.")
    elif config.get("focus_priority") == "secondary":
        focus_notes.append("Local formal-math strategy notes already treat this as a secondary but promising target.")
    if comment:
        focus_notes.append(f"Catalog comment: {comment}.")
    if local_assets and not project_dirs:
        focus_notes.append("Reusable local assets were inferred even though no dedicated Erdős project directory was discovered.")

    return {
        "number": number,
        "doc_count": int(doc_signal["doc_count"]),
        "doc_paths": doc_signal["doc_paths"][:8],
        "project_dirs": project_dirs[:5],
        "related_banks": [str(item) for item in config.get("linked_banks", [])],
        "manual_priority": str(config.get("focus_priority", "")).strip(),
        "comment": comment,
        "focus_notes": _dedupe(focus_notes),
    }


def _infer_blocker_class(
    problem: ProblemRecord,
    *,
    blockers: list[str],
    local_assets: list[dict[str, str]],
    local_literature_signal: dict[str, Any],
) -> str:
    tags = {tag.strip().lower() for tag in problem.tags}
    evidence_signals = set(local_literature_signal.get("evidence_signals", []))
    if _problem_statement_is_placeholder(problem) and not local_literature_signal["statement_recoverable"]:
        return "statement_recovery"
    if not local_assets and len(problem.references) < 2:
        return "source_or_provenance"
    if tags & {"finite_case", "computational_search"} or problem.domain == "geometry":
        return "certificate_or_evaluator"
    if problem.formalized in {"yes", "partial"} or local_assets or "formalization_asset" in evidence_signals:
        return "formalization_infrastructure"
    if blockers:
        return "route_discovery"
    return "proof_route_selection"


def _infer_investment_class(
    problem: ProblemRecord,
    *,
    score: int,
    readiness_tier: str,
    blocker_class: str,
    blockers: list[str],
    local_assets: list[dict[str, str]],
) -> str:
    tags = {tag.strip().lower() for tag in problem.tags}
    if blocker_class == "statement_recovery":
        return "source_recovery"
    if blocker_class == "certificate_or_evaluator":
        return "certificate_pipeline"
    if problem.formalized in {"yes", "partial"} or local_assets:
        return "formalization_project"
    if blocker_class == "source_or_provenance":
        return "source_recovery"
    if score < 4 and len(blockers) >= 2:
        return "freeze_or_defer"
    if readiness_tier == "promising" or tags & ERDOS_ATTACK_SURFACE_TAGS:
        return "proof_route_scout"
    return "light_triage"


def _recommended_next_action(investment_class: str, blocker_class: str) -> str:
    if investment_class == "formalization_project":
        return "Audit local assets and choose one no-sorry checkpoint theorem before another broad proof search."
    if investment_class == "certificate_pipeline":
        return "Define a fail-closed certificate schema and checker obligations before optimizing individual cases."
    if investment_class == "source_recovery":
        return "Recover the exact statement, primary source, and accepted theorem dependencies before proof attack."
    if investment_class == "proof_route_scout":
        return "Run a paper-first route discovery pass and promote only if it yields a narrow first theorem."
    if investment_class == "freeze_or_defer":
        return "Freeze until new literature, assets, or a sharper reduction changes the readiness profile."
    if blocker_class == "route_discovery":
        return "Search for known reductions and split the problem into one verifiable checkpoint."
    return "Keep as a shallow triage candidate and avoid long formalization work for now."


def _shallow_reasoning_summary(
    problem: ProblemRecord,
    *,
    score: int,
    readiness_tier: str,
    blocker_class: str,
    investment_class: str,
    local_assets: list[dict[str, str]],
    local_literature_signal: dict[str, Any],
    erdos_focus_signal: dict[str, Any],
    blockers: list[str],
    opportunities: list[str],
) -> list[str]:
    summary = [
        f"Score {score} puts this candidate in `{readiness_tier}` with investment class `{investment_class}`.",
        f"Current bottleneck is `{blocker_class}`.",
    ]
    if local_assets:
        summary.append(f"{len(local_assets)} local asset(s) are available for immediate audit.")
    elif problem.references:
        summary.append(f"The bank records {len(problem.references)} reference(s), but no local asset was found.")
    else:
        summary.append("No local asset or reference base is present yet.")
    if local_literature_signal["statement_recoverable"]:
        summary.append("A candidate exact statement is recoverable from local literature snapshots.")
    if erdos_focus_signal.get("doc_count"):
        summary.append(
            f"Existing notes mention this Erdős problem in {erdos_focus_signal['doc_count']} markdown file(s)."
        )
    if opportunities:
        summary.append("Strongest positive signal: " + opportunities[0])
    if blockers:
        summary.append("Main risk: " + blockers[0])
    return _dedupe(summary[:6])


def assess_problem_readiness(problem: ProblemRecord, *, formal_math_root: Path | None = None) -> dict[str, Any]:
    if formal_math_root is None:
        formal_math_root = _default_formal_math_root()
    local_assets = _infer_local_assets(problem, formal_math_root)
    local_literature_signal = _assess_local_literature(problem, local_assets)
    erdos_focus_signal = _assess_erdos_focus_signal(
        problem,
        formal_math_root=formal_math_root,
        local_assets=local_assets,
    )
    historical = _historical_foundations(problem, local_assets)
    historical.extend(local_literature_signal["evidence_summary"])
    historical.extend(erdos_focus_signal["focus_notes"])
    historical = _dedupe(historical)
    modern_tools = _infer_modern_tools(problem)
    blockers: list[str] = []
    opportunities: list[str] = []
    proof_path: list[str] = [
        "Recover the exact authoritative statement and confirm the target is worth formalizing.",
        "Audit older proofs, known reductions, or companion theorems before attempting a new result.",
        "Map the problem onto modern toolkits and record a narrow first proof obligation.",
        "Only after a plausible route exists should the system attempt a Lean formalization of the main claim.",
    ]

    if _problem_statement_is_placeholder(problem) and not local_literature_signal["statement_recoverable"]:
        blockers.append("The current bank entry still carries a placeholder statement, so theorem work cannot start yet.")
    if not local_assets and len(problem.references) < 2:
        blockers.append("There are not enough local assets or references yet to justify a serious proof attack.")
    if problem.domain not in {"number_theory", "geometry", "graph_theory"}:
        blockers.append(f"The current ara-math track is weakest in `{problem.domain}`, so readiness is lower.")
    if "finite_case" in problem.tags or "computational_search" in problem.tags:
        opportunities.append("This problem has a finite-search or bounded-search angle that ara-math can exploit early.")
    if problem.formalized in {"yes", "partial"}:
        opportunities.append("Some formalization groundwork already exists, reducing the cost of the Lean stage.")
    if local_assets:
        opportunities.append("Local formal-math assets can seed the literature and theorem-inventory audit.")
    if erdos_focus_signal["related_banks"]:
        opportunities.append(
            "A related ara-math topic bank already exists for this Erdős family, so infrastructure can be reused."
        )
    if erdos_focus_signal["doc_count"]:
        opportunities.append("Local research notes already discuss this Erdős problem, reducing triage uncertainty.")
    if erdos_focus_signal["comment"]:
        opportunities.append("The catalog already exposes a topic-specific comment that can anchor statement recovery.")
    if local_literature_signal["statement_recoverable"]:
        opportunities.append("A concrete statement can already be recovered locally, reducing intake ambiguity.")
    if local_literature_signal["evidence_signals"]:
        opportunities.append("Local references already expose theorem-style signals that can guide the first proof route.")
    if problem.open_problem:
        opportunities.append("Even partial formal progress can generate a publishable report if it sharpens the proof landscape.")

    metadata = problem.metadata or {}
    number = problem.problem_id.replace("erdos-", "")
    if formal_math_root and number in LOCAL_ERDOS_ASSET_MAP:
        proof_path.extend(LOCAL_ERDOS_ASSET_MAP[number]["route"])
    proof_path.extend(problem.recommended_strategy)
    proof_path = _dedupe(proof_path)

    idea_seeds = []
    if formal_math_root and number in LOCAL_ERDOS_ASSET_MAP:
        idea_seeds.extend(LOCAL_ERDOS_ASSET_MAP[number]["ideas"])
    idea_seeds.extend(problem.tags)
    idea_seeds.extend(tool.split(" with ")[0] for tool in modern_tools)
    idea_seeds = _dedupe(idea_seeds)

    score = 0
    score += 3 if problem.open_problem else 0
    score += {"yes": 3, "partial": 2}.get(problem.formalized, 0)
    score += min(len(problem.references), 3)
    score += 3 if local_assets else 0
    score += min(int(local_literature_signal["snapshot_count"]), 2)
    score += 2 if local_literature_signal["statement_recoverable"] else 0
    score += min(len(local_literature_signal["evidence_signals"]), 2)
    if "computational_search" in problem.tags:
        score += 3
    if "finite_case" in problem.tags:
        score += 3
    if "formalization_candidate" in problem.tags:
        score += 2
    if "starter_theorem" in problem.tags:
        score -= 3
    if _problem_statement_is_placeholder(problem):
        score -= 3
    if len(blockers) >= 2:
        score -= 2

    normalized_tags = {tag.strip().lower() for tag in problem.tags}
    if _is_erdos_problem(problem):
        score += min(erdos_focus_signal["doc_count"], 4)
        score += 2 if erdos_focus_signal["project_dirs"] else 0
        score += 2 if erdos_focus_signal["comment"] else 0
        if erdos_focus_signal["manual_priority"] == "primary":
            score += 5
        elif erdos_focus_signal["manual_priority"] == "secondary":
            score += 3
        if erdos_focus_signal["related_banks"]:
            score += 2
        prize_amount = _parse_prize_amount((problem.metadata or {}).get("prize", ""))
        if prize_amount is not None:
            if 0 < prize_amount <= 25:
                score += 2
            elif prize_amount <= 100:
                score += 1
            elif prize_amount >= 1000:
                score -= 1
        if problem.domain in ERDOS_STRONG_DOMAINS:
            score += 1
        if problem.domain in ERDOS_WEAK_DOMAINS:
            score -= 1
        if normalized_tags & ERDOS_ATTACK_SURFACE_TAGS:
            score += 1
        if (
            _problem_statement_is_placeholder(problem)
            and not local_assets
            and not erdos_focus_signal["doc_count"]
            and not erdos_focus_signal["comment"]
        ):
            score -= 2

    if score >= 10:
        readiness_tier = "promising"
    elif score >= 6:
        readiness_tier = "needs_statement_recovery"
    else:
        readiness_tier = "exploratory"
    blocker_class = _infer_blocker_class(
        problem,
        blockers=blockers,
        local_assets=local_assets,
        local_literature_signal=local_literature_signal,
    )
    investment_class = _infer_investment_class(
        problem,
        score=score,
        readiness_tier=readiness_tier,
        blocker_class=blocker_class,
        blockers=blockers,
        local_assets=local_assets,
    )
    recommended_next_action = _recommended_next_action(investment_class, blocker_class)
    shallow_reasoning = _shallow_reasoning_summary(
        problem,
        score=score,
        readiness_tier=readiness_tier,
        blocker_class=blocker_class,
        investment_class=investment_class,
        local_assets=local_assets,
        local_literature_signal=local_literature_signal,
        erdos_focus_signal=erdos_focus_signal,
        blockers=blockers,
        opportunities=opportunities,
    )

    return {
        "problem_id": problem.problem_id,
        "title": problem.title,
        "source": problem.source,
        "domain": problem.domain,
        "open_problem": problem.open_problem,
        "formalized": problem.formalized,
        "tags": problem.tags,
        "score": score,
        "readiness_tier": readiness_tier,
        "investment_class": investment_class,
        "blocker_class": blocker_class,
        "recommended_next_action": recommended_next_action,
        "shallow_reasoning": shallow_reasoning,
        "historical_foundations": historical,
        "modern_toolkit": modern_tools,
        "local_assets": local_assets,
        "proof_path_hypothesis": proof_path,
        "blockers": blockers,
        "opportunities": opportunities,
        "idea_seeds": idea_seeds,
        "reference_count": len(problem.references),
        "statement_quality": str(metadata.get("statement_quality", "curated")),
        "local_literature_signal": local_literature_signal,
        "erdos_focus_signal": erdos_focus_signal,
    }


def scout_problem_bank(
    *,
    bank_path: Path | str,
    formal_math_root: Path | str | None = None,
    top_k: int = 20,
    output_path: Path | str | None = None,
) -> dict[str, Any]:
    bank = load_problem_bank(bank_path)
    formal_root = Path(formal_math_root) if formal_math_root else None
    assessments = [
        assess_problem_readiness(problem, formal_math_root=formal_root)
        for problem in bank
        if problem.open_problem
    ]
    assessments.sort(key=lambda item: (-item["score"], item["problem_id"]))
    top_candidates = assessments[:top_k]
    shortlist = [
        candidate
        for candidate in assessments
        if candidate["score"] >= 4 or candidate["local_assets"] or candidate["readiness_tier"] == "promising"
    ][:top_k]
    theme_counter = Counter()
    for candidate in shortlist or top_candidates:
        theme_counter.update(candidate["idea_seeds"])
    readiness_counter = Counter(candidate["readiness_tier"] for candidate in assessments)
    investment_counter = Counter(candidate["investment_class"] for candidate in assessments)
    blocker_counter = Counter(candidate["blocker_class"] for candidate in assessments)
    domain_counter = Counter(candidate["domain"] for candidate in assessments)
    report = {
        "generated_at": utc_now_iso(),
        "bank_path": str(Path(bank_path)),
        "candidate_count": len(assessments),
        "top_k": top_k,
        "screening_summary": {
            "readiness_tier_counts": dict(readiness_counter.most_common()),
            "investment_class_counts": dict(investment_counter.most_common()),
            "blocker_class_counts": dict(blocker_counter.most_common()),
            "domain_counts": dict(domain_counter.most_common()),
        },
        "shortlist_candidates": [
            {
                "rank": index + 1,
                **candidate,
            }
            for index, candidate in enumerate(shortlist)
        ],
        "top_candidates": [
            {
                "rank": index + 1,
                **candidate,
            }
            for index, candidate in enumerate(top_candidates)
        ],
        "global_idea_themes": [
            {"theme": theme, "count": count}
            for theme, count in theme_counter.most_common(15)
        ],
    }
    if output_path:
        write_json(Path(output_path), report)
    return report


def write_project_intake_artifacts(
    *,
    project_dir: Path,
    problem: ProblemRecord,
    formal_math_root: Path | str | None = None,
) -> dict[str, Any]:
    assessment = assess_problem_readiness(problem, formal_math_root=Path(formal_math_root) if formal_math_root else None)
    literature_report = read_json(project_dir / "idea" / "reference_snapshots.json", default={})
    statement_recovery = read_json(project_dir / "idea" / "statement_recovery.json", default={})
    literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
    blockers = list(assessment["blockers"])
    opportunities = list(assessment["opportunities"])
    historical_foundations = list(assessment["historical_foundations"])
    recovered_statement = str(statement_recovery.get("statement", "")).strip()
    recovered_statement_status = str(statement_recovery.get("status", "")).strip()
    evidence_counts = literature_evidence.get("counts", {})
    evidence_total = sum(int(value or 0) for value in evidence_counts.values())
    has_literature_signal = evidence_total > 0

    placeholder_blocker = "The current bank entry still carries a placeholder statement, so theorem work cannot start yet."
    if recovered_statement:
        blockers = [blocker for blocker in blockers if blocker != placeholder_blocker]
        opportunities.append("Harvested literature already provides a working target statement for theorem planning.")
        historical_foundations.append(f"Recovered statement source: {statement_recovery.get('source', '')}")
    if has_literature_signal:
        opportunities.append("Harvested literature now contributes concrete theorem-style evidence for proof-path design.")
        for item in literature_evidence.get("known_results", [])[:2]:
            historical_foundations.append(f"Known-result evidence: {item['statement']}")
        for item in literature_evidence.get("proof_ingredients", [])[:2]:
            historical_foundations.append(f"Proof-ingredient evidence: {item['statement']}")

    blockers = _dedupe(blockers)
    opportunities = _dedupe(opportunities)
    historical_foundations = _dedupe(historical_foundations)
    readiness_tier = str(assessment["readiness_tier"])
    if recovered_statement and has_literature_signal and readiness_tier == "exploratory":
        readiness_tier = "needs_statement_recovery"
    proof_path_payload = {
        "generated_at": utc_now_iso(),
        "problem_id": problem.problem_id,
        "title": problem.title,
        "readiness_tier": readiness_tier,
        "historical_foundations": historical_foundations,
        "modern_toolkit": assessment["modern_toolkit"],
        "local_assets": assessment["local_assets"],
        "proof_path_hypothesis": assessment["proof_path_hypothesis"],
        "blockers": blockers,
        "opportunities": opportunities,
        "literature": {
            "source_count": int(literature_report.get("source_count", 0)),
            "snapshot_count": int(literature_report.get("snapshot_count", 0)),
            "skipped_source_count": int(literature_report.get("skipped_source_count", 0)),
            "recovered_statement_status": recovered_statement_status,
            "recovered_statement": recovered_statement,
            "recovered_statement_source": str(statement_recovery.get("source", "")),
            "known_results": literature_evidence.get("known_results", [])[:4],
            "proof_ingredients": literature_evidence.get("proof_ingredients", [])[:4],
            "modern_tools": literature_evidence.get("modern_tools", [])[:4],
            "open_gaps": literature_evidence.get("open_gaps", [])[:4],
            "source_attribution_count": int(literature_evidence.get("source_attribution_count", 0)),
        },
        "local_literature_signal": assessment["local_literature_signal"],
    }
    idea_ledger_payload = {
        "generated_at": utc_now_iso(),
        "problem_id": problem.problem_id,
        "title": problem.title,
        "themes": assessment["idea_seeds"],
        "route_hypotheses": assessment["proof_path_hypothesis"],
        "reusable_assets": [asset["path"] for asset in assessment["local_assets"]],
        "literature_signals": assessment["local_literature_signal"]["evidence_signals"],
        "recovered_statement": recovered_statement,
        "literature_known_results": literature_evidence.get("known_results", [])[:4],
        "literature_tools": literature_evidence.get("modern_tools", [])[:4],
        "status": "seeded",
    }
    write_json(project_dir / "idea" / "proof_path_assessment.json", proof_path_payload)
    write_json(project_dir / "idea" / "math_idea_ledger.json", idea_ledger_payload)
    write_json(
        project_dir / "idea" / "literature_foundations.json",
        {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "historical_foundations": historical_foundations,
            "references": problem.references,
            "reference_snapshot_count": int(literature_report.get("snapshot_count", 0)),
            "recovered_statement": recovered_statement,
            "known_results": literature_evidence.get("known_results", [])[:4],
            "proof_ingredients": literature_evidence.get("proof_ingredients", [])[:4],
            "modern_tools": literature_evidence.get("modern_tools", [])[:4],
            "open_gaps": literature_evidence.get("open_gaps", [])[:4],
        },
    )
    return {
        "proof_path_assessment": proof_path_payload,
        "math_idea_ledger": idea_ledger_payload,
    }
