from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from amra.core.models import ProblemRecord
from amra.discovery.counterexample_campaign import classify_claim
from amra.discovery.second_batch_campaign import SECOND_BATCH_FORBIDDEN_RESOLVED
from amra.orchestration.workstreams import utc_now_iso
from amra.problem_banks.registry import load_problem_bank


TARGETABILITY_SCHEMA_VERSION = "amra.counterexample_target_screen.v1"
TARGETABILITY_ENGINE_VERSION = "cets.local.v1"
TARGETABILITY_INVENTORY_FILE = "targetability-inventory.jsonl"
TARGETABILITY_RANKING_FILE = "targetability-ranking.jsonl"
TARGETABILITY_RANKING_CSV_FILE = "targetability-ranking.csv"
TARGETABILITY_SHORTLIST_FILE = "targetability-shortlist.json"
TARGETABILITY_SUMMARY_FILE = "targetability-summary.json"
TARGETABILITY_REPORT_FILE = "TARGETABILITY_REPORT.md"
TARGETABILITY_MANIFEST_FILE = "targetability-manifest.json"

COMPONENT_MAXIMA: dict[str, int] = {
    "resolution_leverage": 20,
    "statement_status_confidence": 15,
    "certificate_verifier_readiness": 20,
    "search_compressibility": 20,
    "boundary_leverage": 10,
    "feedback_quality": 10,
    "local_reuse": 5,
}

DIFFICULTY_PENALTIES: dict[int, int] = {1: 0, 2: 1, 3: 3, 4: 7, 5: 12}

KNOWN_RESOLVED_OVERRIDES: dict[str, str] = {
    **SECOND_BATCH_FORBIDDEN_RESOLVED,
    "unsolvedmath-kou-21.134": (
        "Kourovka Notebook v45 marks both parts resolved with negative answers "
        "(arXiv:1401.0300v45, updated 2026-07-03)"
    ),
    "unsolvedmath-opg-59994": (
        "Mattiolo-Steffen disprove the circular-flow conjecture for "
        "(2t+1)-regular class 1 graphs (J. Graph Theory 2022, "
        "doi:10.1002/jgt.22746; arXiv:2001.02484)"
    ),
    "unsolvedmath-opg-47028": (
        "Guninski gives the non-Hamiltonian 3-diregular oriented graph "
        "Cay(Z_12; {2,3,8}), with 12 <= 4*3+1, disproving Jackson's "
        "conjecture (arXiv:1602.06380; non-Hamiltonicity proved by "
        "Locke-Witte, J. Graph Theory 1999)"
    ),
}

KNOWN_STATEMENT_REPAIR_OVERRIDES: dict[str, str] = {
    "triangle-dissection-13": (
        "The cited Erdos #634 source asks which n admit some triangle tiled "
        "by n congruent triangles; it does not currently substantiate this "
        "stronger equilateral-triangle record or its open status for n=13"
    ),
    "triangle-dissection-17": (
        "The cited Erdos #634 source asks which n admit some triangle tiled "
        "by n congruent triangles; it does not currently substantiate this "
        "stronger equilateral-triangle record or its open status for n=17"
    ),
    "triangle-dissection-19": (
        "Erdos #634 still highlights n=19 for some triangle, while this local "
        "record requires an equilateral outer triangle; recover and cite the "
        "exact stronger statement before modeling"
    ),
    "erdos-825-weird": (
        "Erdos #825's absolute-constant question is proved, while the local "
        "record conflates the stronger C=3 language with the bound "
        "sigma(n)/n<4; recover the exact strengthened claim and status"
    ),
}

_FINITE_OBJECT_CUES: dict[str, tuple[str, ...]] = {
    "graph": (
        "graph",
        "digraph",
        "tree",
        "cycle",
        "clique",
        "matching",
        "coloring",
        "colouring",
        "vertex",
        "edge",
    ),
    "integer": (
        "integer",
        "prime",
        "divisor",
        "divisible",
        "modulo",
        "sequence",
        "tuple",
        "ℕ",
        "ℤ",
    ),
    "finite_algebra": (
        "finite group",
        "group of order",
        "matrix",
        "matrices",
        "permutation",
        "latin square",
        "finite field",
        "polynomial",
        "code",
        "matroid",
    ),
    "finite_family": (
        "finite set",
        "family of sets",
        "configuration",
        "incidence",
        "polytope",
        "lattice",
        "tiling",
        "finset",
        "fintype",
        "decidableeq",
        "decidablerel",
        "zmod",
    ),
}

_EXACT_CHECK_CUES = (
    "determinant",
    "rank",
    "eigenvalue",
    "chromatic",
    "divisib",
    "factor",
    "identity",
    "equation",
    "inequality",
    "diameter",
    "distance",
    "degree",
    "order",
    "permanent",
    "coefficient",
    "card",
    "finset",
    "≠",
    "≤",
    "≥",
)

_FEEDBACK_CUES = (
    "maximum",
    "minimum",
    "largest",
    "smallest",
    "upper bound",
    "lower bound",
    "best possible",
    "at most",
    "at least",
    "ratio",
    "density",
    "number of",
    "size of",
    "length",
    "degree",
    "distance",
    "diameter",
    "eigenvalue",
    "chromatic",
    "cost",
    "error",
    "gap",
    "monotone",
    "monotonic",
    "concave",
    "convex",
    "unimodal",
    "log-concave",
)

_FRONTIER_CUES = (
    "known for",
    "known in",
    "verified for",
    "verified up to",
    "checked up to",
    "special case",
    "special cases",
    "smallest",
    "first unknown",
    "best known",
    "low dimension",
    "dimension 2",
    "dimension 3",
    "dimension 4",
    "for n <",
    "for n <=",
    "for n ≤",
    "except",
    "near equality",
    "equality case",
)

_CONTINUOUS_CUES = (
    "partial differential",
    "smooth manifold",
    "infinite-dimensional",
    "navier-stokes",
    "quantum field",
    "measure space",
    "analytic continuation",
    "tendsto",
    "atTop",
    "volume",
    "measure",
    "ℝ",
    "ℂ",
    "unitary",
    "mathbb{c}",
    "length of the curve",
)

_GLOBAL_LEAN_CUES = (
    "∀ᶠ",
    "∀ᵉ",
    "∃ᶠ",
    "Tendsto",
    "atTop",
    "Infinite",
    "Finite ",
    "Summable",
    "HasSum",
    "Filter.",
    "=O[",
    "=o[",
    "=Θ[",
    "~[",
)

_HIGH_ENTROPY_OBJECT_CUES = (
    "set ℝ",
    "ℝ → ℝ",
    "ℕ → ℝ",
    "function",
    "manifold",
    "measure",
    "variety",
    "scheme",
    "ℂ",
    "unitary",
    "mathbb{c}",
)

_MULTI_PROBLEM_CUES = (
    "collection of conjectures",
    "set of conjectures",
    "family of conjectures",
    "several questions",
    "including the following",
    "in particular, is it true",
    "in particular, does",
)

_PARAMETER_RE = re.compile(
    r"(?:\bfor (?:all|every)\b.{0,60}\b[nkdpqr]\b|"
    r"\b[nkdpqr]\s*(?:>=|≤|<|>)|"
    r"\bdimension\s+\d+|"
    r"\border\s+\d+|"
    r"\(\s*[nkdpqr]\s*:\s*[ℕℤ])",
    re.IGNORECASE,
)

_LEAN_FENCE_RE = re.compile(r"```lean\s*(.*?)```", re.DOTALL | re.IGNORECASE)
_DECLARATION_RE = re.compile(r"\b(theorem|lemma|def)\s+([^\s:(]+)")
_ERDOS_FORMAL_RE = re.compile(r"(?:^|/)ErdosProblems/(\d+)\.lean$")
_ERDOS_UNSOLVED_RE = re.compile(r"^unsolvedmath-ep-(\d+)(?:-|$)")
_SPACE_RE = re.compile(r"\s+")


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    body = "".join(
        json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n"
        for row in rows
    )
    _atomic_write_text(path, body)


def _read_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        problem_id = str(row.get("problem_id", "")).strip()
        if problem_id:
            rows[problem_id] = row
    return rows


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _problem_fingerprint(problem: ProblemRecord) -> str:
    payload = json.dumps(
        {
            "problem_id": problem.problem_id,
            "title": problem.title,
            "statement": problem.statement,
            "metadata": problem.metadata,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return _sha256_text(payload)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _clamp(value: int | float, lower: int, upper: int) -> int:
    return max(lower, min(upper, int(round(value))))


def _normalized_text(value: str) -> str:
    return _SPACE_RE.sub(" ", value).strip()


def _matched_groups(text: str) -> dict[str, list[str]]:
    lowered = text.lower()
    return {
        group: [cue for cue in cues if cue.lower() in lowered]
        for group, cues in _FINITE_OBJECT_CUES.items()
    }


def _extract_lean_declaration(statement: str) -> str:
    match = _LEAN_FENCE_RE.search(statement)
    return match.group(1).strip() if match else statement.strip()


def _split_lean_header(code: str) -> tuple[str, str, str, str, bool]:
    match = _DECLARATION_RE.search(code)
    if not match:
        return "", "", "", code.strip(), False
    declaration_kind, declaration_name = match.group(1), match.group(2)
    depth = 0
    in_string = False
    escaped = False
    start = match.end()
    for index in range(start, len(code)):
        char = code[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char in "([{":
            depth += 1
            continue
        if char in ")]}":
            depth = max(0, depth - 1)
            continue
        if char == ":" and depth == 0 and code[index : index + 2] != ":=":
            header = code[start:index]
            conclusion = code[index + 1 :].strip()
            return (
                declaration_kind,
                declaration_name,
                header,
                conclusion,
                bool(re.search(r"[\(\{\[]", header)),
            )
    return declaration_kind, declaration_name, "", "", False


def _contains_global_semantics(value: str) -> list[str]:
    return [cue for cue in _GLOBAL_LEAN_CUES if cue in value]


def _lean_logical_profile(problem: ProblemRecord) -> dict[str, Any]:
    code = _extract_lean_declaration(problem.statement)
    (
        declaration_kind,
        declaration_name,
        header,
        conclusion,
        has_header_binders,
    ) = (
        _split_lean_header(code)
    )
    answer_wrapper = "answer(sorry)" in code.replace(" ", "")
    global_operators = _contains_global_semantics(conclusion)
    has_exists = bool(re.search(r"∃(?![ᶠ!])", conclusion))
    has_unique_exists = "∃!" in conclusion
    has_forall = bool(re.search(r"∀(?![ᶠᵉ])", conclusion))
    stripped = conclusion.lstrip()
    normalized = _normalized_text(conclusion)
    finite_representation_evidence = [
        cue
        for cue in (
            "Finset",
            "ZMod",
            "Fin ",
            "Matrix",
        )
        if cue in code
    ]
    finite_domain_evidence: list[str] = []
    if "[Fintype" in code and (
        "DecidableEq" in code or "DecidableRel" in code
    ):
        finite_domain_evidence.append("Fintype+Decidable")
    if re.search(r":\s*Fin\s+\d+", code):
        finite_domain_evidence.append("bounded Fin")
    if re.search(r":\s*ZMod\s+\d+", code):
        finite_domain_evidence.append("fixed ZMod")
    high_entropy_binders = [
        cue
        for cue in (" → ", "Set ", "ℝ", "ℂ", "Type", "Measure", "Filter")
        if cue in header
        and not (cue == "Type" and finite_domain_evidence)
    ]
    scalar_assignment_evidence = bool(
        re.search(r":\s*[ℕℤ](?:\s|\)|$)", header)
        or re.search(r"∀[^,]{0,120}:\s*[ℕℤ]", conclusion)
    )
    finitely_checkable_assignment = bool(
        finite_domain_evidence
        or (
            scalar_assignment_evidence
            and not high_entropy_binders
            and not global_operators
        )
        or (
            finite_representation_evidence
            and not high_entropy_binders
            and not global_operators
        )
    )
    blockers: list[str] = []
    needs_elaboration = bool(
        global_operators
        or re.search(r"\bletI?\b", conclusion)
        or any(cue in code for cue in _HIGH_ENTROPY_OBJECT_CUES)
    )

    if declaration_kind == "def":
        claim_kind = "formal_definition"
        route = "not_counterexample"
        quantifier_structure = "non_prop_definition"
        finite_witness: bool | None = False
        negation_shape = "not_applicable"
        blockers.append("the Formal Conjectures record is a definition, not a proposition")
    elif answer_wrapper:
        claim_kind = "answer_query"
        route = "answer_discovery"
        quantifier_structure = "answer_placeholder"
        finite_witness = False
        negation_shape = "recover_answer_before_routing"
        blockers.append("answer(sorry) is an unknown-answer placeholder")
    elif global_operators:
        claim_kind = "global_or_asymptotic_claim"
        route = "formal_modeling"
        quantifier_structure = "global_semantics"
        finite_witness = False
        negation_shape = "global_certificate_required"
        blockers.append(
            "global Lean operators are not refuted by one failed finite instance"
        )
    elif any(cue in conclusion for cue in ("Nonempty", "IsRealizable")):
        claim_kind = "existence_claim"
        route = "witness_discovery"
        quantifier_structure = "hidden_existential_predicate"
        finite_witness = False
        negation_shape = "nonexistence_proof_required"
        needs_elaboration = True
    elif has_unique_exists:
        claim_kind = "mixed_quantifiers"
        route = "subclaim_decomposition"
        quantifier_structure = "unique_existence"
        finite_witness = None
        negation_shape = "nonexistence_or_two_witnesses"
        blockers.append("unique existence has two logically different failure modes")
    elif re.match(r"¬\s*∃", stripped):
        claim_kind = "universal_claim"
        route = "counterexample"
        quantifier_structure = "negative_existence"
        finite_witness = True
        negation_shape = "exists_finite_witness"
    elif re.match(r"¬\s*∀", stripped):
        claim_kind = "negative_universal"
        route = "not_counterexample"
        quantifier_structure = "negative_universal"
        finite_witness = False
        negation_shape = "universal_proof_required"
    elif has_forall and has_exists:
        claim_kind = "mixed_quantifiers"
        route = "subclaim_decomposition"
        quantifier_structure = "forall_exists_or_nested"
        finite_witness = False
        negation_shape = "residual_universal_obligation"
        blockers.append("a failed bounded inner search is not a refutation")
    elif stripped.startswith("∃") or has_exists:
        claim_kind = "existence_claim"
        route = "witness_discovery"
        quantifier_structure = "existential"
        finite_witness = False
        negation_shape = "nonexistence_proof_required"
    elif "↔" in conclusion:
        claim_kind = "equivalence_claim"
        route = "counterexample"
        quantifier_structure = "universal_equivalence"
        finite_witness = True if finitely_checkable_assignment else None
        negation_shape = "truth_value_mismatch"
        needs_elaboration = True
    elif has_forall:
        claim_kind = "universal_claim"
        route = "counterexample"
        quantifier_structure = "universal"
        finite_witness = True if finitely_checkable_assignment else None
        negation_shape = "exists_falsifying_assignment"
    elif has_header_binders:
        claim_kind = "universal_claim"
        route = "counterexample"
        quantifier_structure = "implicit_header_universal"
        finite_witness = True if finitely_checkable_assignment else None
        negation_shape = "exists_falsifying_assignment"
    elif any(cue in conclusion for cue in ("=", "≠", "≤", "≥", "<", ">")):
        claim_kind = "closed_relation"
        route = "formal_modeling"
        quantifier_structure = "closed_or_section_parameter_relation"
        finite_witness = None
        negation_shape = "requires_elaborated_declaration_type"
        needs_elaboration = True
        blockers.append("section parameters may be omitted from the extracted declaration")
    else:
        claim_kind = "unclassified_question"
        route = "formal_modeling"
        quantifier_structure = "unclassified_lean"
        finite_witness = None
        negation_shape = "unknown"
        needs_elaboration = True

    return {
        "claim_kind": claim_kind,
        "route": route,
        "quantifier_structure": quantifier_structure,
        "negation_shape": negation_shape,
        "resolution_scope": "full_claim",
        "finite_witness_sufficient": finite_witness,
        "route_confidence": "exact_syntax_conservative",
        "source_language": "lean4",
        "declaration_kind": declaration_kind,
        "declaration_name": declaration_name
        or str((problem.metadata or {}).get("declaration_name", "")),
        "answer_wrapper": answer_wrapper,
        "header_binders_detected": has_header_binders,
        "header_binder_risks": high_entropy_binders,
        "global_operators": global_operators,
        "finite_domain_evidence": finite_domain_evidence,
        "finite_representation_evidence": finite_representation_evidence,
        "needs_elaboration": needs_elaboration,
        "blockers": blockers,
    }


def _natural_logical_profile(
    problem: ProblemRecord,
    campaign_result: Mapping[str, Any],
) -> dict[str, Any]:
    classification = dict(
        campaign_result.get("classification") or classify_claim(problem)
    )
    claim_kind = str(classification.get("claim_kind", "unclassified_question"))
    statement_lower = problem.statement.lower()
    statement_start = _normalized_text(statement_lower)
    target_parts = re.split(
        r"\b(?:problem|conjecture|question)\b[\s.:;-]*",
        statement_start,
    )
    target_clause = next(
        (part.strip() for part in reversed(target_parts) if part.strip()),
        statement_start,
    )
    enumerated_parts = re.findall(
        r"(?:^|\s|\()([a-d]|\d+)[.)]\s+(?=[a-z])",
        statement_start,
    )
    target_markers = re.findall(
        r"\b(?:problem|conjecture|question)\b",
        statement_start,
    )
    bullet_subclaims = re.findall(
        r"(?m)^\s*-\s+(?:at most|at least|if|for|every|no)\b",
        statement_lower,
    )
    context_dependent = bool(
        re.search(
            r"\bcan the (?:constant|bound|hypothesis|condition)\b",
            target_clause,
        )
        or re.search(r"\b(?:same|analogous) question as\b", target_clause)
    )
    atomicity = (
        "bundled"
        if (
            any(cue in statement_lower for cue in _MULTI_PROBLEM_CUES)
            or len(set(enumerated_parts)) >= 2
            or problem.statement.count("?") >= 2
            or len(target_markers) >= 2
            or len(bullet_subclaims) >= 2
        )
        else ("context_dependent" if context_dependent else "record_level")
    )
    negative_existence = bool(
        re.match(r"(?:there (?:is|are) no|no\b)", target_clause)
        or re.match(
            r"there (?:does not|doesn't) exist\b",
            target_clause,
        )
        or re.search(r"\\neg\s*\\exists|¬\s*∃", problem.statement)
    )
    existence_question = re.search(
        r"\b(?:does there exist|do there exist|is there|are there|can one construct)\b",
        target_clause,
    )
    existential_question_has_outer_universal = False
    if existence_question:
        sentence_start = max(
            target_clause.rfind(".", 0, existence_question.start()),
            target_clause.rfind("?", 0, existence_question.start()),
            target_clause.rfind(";", 0, existence_question.start()),
        )
        question_prefix = target_clause[
            sentence_start + 1 : existence_question.start()
        ]
        existential_question_has_outer_universal = bool(
            re.search(
                r"\b(?:for all|for every|for each|for any|every)\b|∀",
                question_prefix,
            )
        )
    direct_existence = bool(
        (existence_question and not existential_question_has_outer_universal)
        or re.match(
            r"there (?:is|exists) (?:a|an|some) "
            r"(?:(?:absolute|universal|positive) )?"
            r"(?:constant|function|set|sequence|family)\b",
            target_clause,
        )
    )
    direct_classification = bool(
        re.match(
            r"(?:what is|determine|classify|characterize|compute|find all)\b",
            target_clause,
        )
        or re.search(
            r"\bwhat is\b|"
            r"\bhow large must\b|"
            r"\b(?:determine|estimate|give bounds)\b|"
            r"\bfor which\b|"
            r"\bfind (?:the )?(?:smallest|largest|minimum|maximum|all)\b|"
            r"\b(?:optimal strateg|best possible)\w*\b|"
            r"\bunder what conditions\b|"
            r"\bcan (?:we|one) (?:determine|reconstruct|recover)\b|"
            r"\bcan some or all\b|"
            r"\bhow many\b",
            target_clause,
        )
    )
    mixed_quantifiers_detected = bool(
        existential_question_has_outer_universal
        or re.search(
            r"(?:for all|for every|for each|for any|∀)"
            r".{0,300}?"
            r"(?:there (?:is|are|exists?)|∃)",
            target_clause,
        )
        or re.search(
            r"(?:there (?:is|exists)|for) (?:a|an|some) constant"
            r".{0,300}?(?:every|any|for all|for every)",
            target_clause,
        )
        or re.search(
            r"(?:for some|with some) constant\b",
            target_clause,
        )
        or re.search(
            r"for some\s+\$?\\?(?:delta|epsilon|varepsilon|c)\b",
            target_clause,
        )
        or re.search(r"\bembed into (?:a|some) finite group\b", target_clause)
        or re.search(
            r"\b(?:is|be|as) (?:the )?intersection "
            r"(?:hyper)?graph of a family\b",
            target_clause,
        )
        or re.search(r"\bwinning strategy for \$?[a-z]\b", target_clause)
        or re.search(
            r"\bfor every\b.{0,120}\b(?:exist|exists)\b",
            target_clause,
        )
    )
    natural_groups = _matched_groups(
        " ".join((problem.title, problem.statement, " ".join(problem.tags)))
    )
    has_finite_representation = bool(
        any(natural_groups.values())
        or "finite" in statement_lower
        or problem.domain
        in {
            "graph_theory",
            "combinatorics",
            "number_theory",
            "group_theory",
            "computer_science",
        }
    )
    has_nonlocal_semantics = bool(
        any(
            cue in statement_lower
            for cue in (
                "infinitely many",
                "asymptotic",
                "in the limit",
                "almost everywhere",
                "measure zero",
                "smooth function",
                "analytic continuation",
                "infinite set",
                "infinite graph",
                "infinite group",
                "for some constant",
                "there is a constant",
                "locally compact",
                "topological group",
                "finitary permutations",
                "profinite",
                "infinite",
                "all but finitely many",
                "finitely many exception",
                "only finitely many",
                "almost all",
                "for almost all",
                "logarithmic density",
                "natural density",
                "permutation of positive integers",
                "for sufficiently large",
                "sufficiently large",
                "sufficently large",
                "eventually",
                "residually-",
                "pro-$",
                "right-orderable",
                "right-relatively convex",
                "for all large",
                "every large",
                "a large prime",
                "large enough",
                "for every bounded sequence",
                "the sum $ \\sum",
            )
        )
        or any(
            cue.lower() in statement_lower
            for cue in _CONTINUOUS_CUES
        )
        or re.search(
            r"\\?lim(?:inf|sup)?\b|"
            r"\\?infty\b|"
            r"\\?to\s*\\?infty|"
            r"(?:^|[^a-z])o\s*\(|"
            r"\\?(?:theta|sim|asymp)\b|"
            r"\\gg(?:\b|_)|\\ll(?:\b|_)",
            target_clause,
        )
    )
    inferred_finite_witness: bool | None = (
        True
        if has_finite_representation and not has_nonlocal_semantics
        else None
    )
    if direct_classification:
        claim_kind = "classification_or_optimization"
        route = "subclaim_decomposition"
        finite_witness = False
        quantifier_structure = "classification_or_optimization"
        negation_shape = "not_a_single_refutation_contract"
    elif direct_existence:
        claim_kind = "existence_claim"
        route = "witness_discovery"
        finite_witness = False
        quantifier_structure = "existential"
        negation_shape = "nonexistence_proof_required"
    elif negative_existence:
        claim_kind = "universal_claim"
        route = "counterexample"
        finite_witness: bool | None = inferred_finite_witness
        quantifier_structure = "negative_existence"
        negation_shape = "exists_finite_witness"
    elif mixed_quantifiers_detected:
        claim_kind = "mixed_quantifiers"
        route = "subclaim_decomposition"
        finite_witness = False
        quantifier_structure = "mixed"
        negation_shape = "residual_universal_obligation"
    elif claim_kind in {"universal_claim", "equivalence_claim"}:
        route = "counterexample"
        finite_witness = inferred_finite_witness
        quantifier_structure = (
            "universal" if claim_kind == "universal_claim" else "equivalence"
        )
        negation_shape = "exists_falsifying_assignment"
    elif claim_kind == "existence_claim":
        route = "witness_discovery"
        finite_witness = False
        quantifier_structure = "existential"
        negation_shape = "nonexistence_proof_required"
    elif claim_kind == "mixed_quantifiers":
        route = "subclaim_decomposition"
        finite_witness = False
        quantifier_structure = "mixed"
        negation_shape = "residual_universal_obligation"
    elif claim_kind == "classification_or_optimization":
        route = "subclaim_decomposition"
        finite_witness = False
        quantifier_structure = "classification_or_optimization"
        negation_shape = "not_a_single_refutation_contract"
    else:
        route = "formal_modeling"
        finite_witness = None
        quantifier_structure = "unclassified_natural_language"
        negation_shape = "unknown"

    blockers: list[str] = []
    if atomicity == "bundled":
        blockers.append("record bundles multiple conjectures or questions")
    elif atomicity == "context_dependent":
        blockers.append("record depends on an undefined external constant or question")
    return {
        "claim_kind": claim_kind,
        "route": route,
        "quantifier_structure": quantifier_structure,
        "negation_shape": negation_shape,
        "resolution_scope": str(
            campaign_result.get("search_scope") or "full_claim"
        ),
        "finite_witness_sufficient": finite_witness,
        "route_confidence": "inferred_text",
        "source_language": "natural_language",
        "declaration_kind": "",
        "declaration_name": "",
        "answer_wrapper": False,
        "header_binders_detected": False,
        "global_operators": [],
        "finite_domain_evidence": [],
        "finite_representation_evidence": [
            group for group, matches in natural_groups.items() if matches
        ],
        "needs_elaboration": atomicity == "bundled",
        "atomicity": atomicity,
        "blockers": blockers,
    }


def _logical_profile(
    problem: ProblemRecord,
    campaign_result: Mapping[str, Any],
) -> dict[str, Any]:
    quality = str((problem.metadata or {}).get("statement_quality", ""))
    if quality == "formal_lean4" or problem.formalized == "lean4_statement":
        profile = _lean_logical_profile(problem)
        profile["atomicity"] = "record_level"
        return profile
    return _natural_logical_profile(problem, campaign_result)


def _source_url(problem: ProblemRecord) -> str:
    metadata_url = str((problem.metadata or {}).get("source_url", "")).strip()
    if metadata_url:
        return metadata_url
    return problem.references[0] if problem.references else ""


def _canonical_group_id(problem: ProblemRecord) -> str:
    metadata = problem.metadata or {}
    source_file = str(metadata.get("source_file", ""))
    formal_match = _ERDOS_FORMAL_RE.search(source_file)
    if formal_match:
        return f"erdos:{formal_match.group(1)}"
    unsolved_match = _ERDOS_UNSOLVED_RE.match(problem.problem_id)
    if unsolved_match:
        return f"erdos:{unsolved_match.group(1)}"
    catalog = str(metadata.get("source_catalog", "")).strip() or problem.source
    canonical_id = str(
        metadata.get("canonical_source_record_id")
        or metadata.get("source_id")
        or problem.problem_id
    )
    return f"{catalog.lower().replace(' ', '_')}:{canonical_id}"


def _local_status_conflicts(problem: ProblemRecord) -> list[str]:
    metadata = problem.metadata or {}
    conflicts: list[str] = []
    closed_tokens = (
        "closed",
        "solved",
        "proved",
        "proven",
        "disproved",
        "resolved",
        "likely_solved",
    )
    for field in ("status", "detail_status", "index_status", "status_state"):
        value = str(metadata.get(field, "")).strip().lower()
        if value and any(token in value for token in closed_tokens):
            conflicts.append(f"{field}={value}")
    return conflicts


def _statement_integrity_flags(statement: str) -> list[str]:
    flags: list[str] = []
    if any(
        ord(char) < 32 and char not in "\n\r\t"
        for char in statement
    ):
        flags.append("embedded_control_character")
    if re.search(r'"\s*,?\s*"difficulty"\s*:', statement):
        flags.append("embedded_source_json_fragment")
    return flags


def _inventory_decision(
    problem: ProblemRecord,
    *,
    bank_path: Path,
    seen_problem_ids: set[str],
) -> dict[str, Any]:
    metadata = problem.metadata or {}
    quality = str(metadata.get("statement_quality", "")).strip()
    flags = [str(item) for item in metadata.get("source_consistency_flags", [])]
    integrity_flags = _statement_integrity_flags(problem.statement)
    reasons: list[str] = []
    if problem.problem_id in seen_problem_ids:
        status = "excluded_duplicate_record_id"
        reasons.append("problem_id already appeared in an earlier input bank")
    elif problem.problem_id in KNOWN_RESOLVED_OVERRIDES:
        status = "excluded_closed_or_solved"
        reasons.append(KNOWN_RESOLVED_OVERRIDES[problem.problem_id])
    elif problem.problem_id in KNOWN_STATEMENT_REPAIR_OVERRIDES:
        status = "needs_statement_recovery"
        reasons.append(KNOWN_STATEMENT_REPAIR_OVERRIDES[problem.problem_id])
    elif not problem.open_problem or _local_status_conflicts(problem):
        status = "excluded_closed_or_solved"
        reasons.extend(_local_status_conflicts(problem))
    elif metadata.get("duplicate_of"):
        status = "excluded_duplicate"
        reasons.append(f"duplicate_of={metadata['duplicate_of']}")
    elif flags or integrity_flags or metadata.get("source_id_collision"):
        status = "needs_statement_recovery"
        reasons.extend(
            flags
            or integrity_flags
            or ["source_id_collision"]
        )
    elif quality in {"placeholder", "collision_snippet", ""}:
        status = "needs_statement_recovery"
        reasons.append(f"statement_quality={quality or 'unknown'}")
    elif quality in {"problem_list_pointer", "problem_list"}:
        status = "needs_atomic_split"
        reasons.append(f"statement_quality={quality}")
    elif quality not in {"detail_page", "formal_lean4", "curated", "exact", "verified"}:
        status = "needs_statement_recovery"
        reasons.append(f"unsupported statement_quality={quality}")
    else:
        status = "included"
    return {
        "schema_version": TARGETABILITY_SCHEMA_VERSION,
        "problem_id": problem.problem_id,
        "title": problem.title,
        "source": problem.source,
        "source_bank_path": str(bank_path),
        "statement_quality": quality,
        "statement_hash": _sha256_text(problem.statement),
        "canonical_group_id": _canonical_group_id(problem),
        "admission_status": status,
        "included_in_ranking": status == "included",
        "reasons": reasons,
    }


def _difficulty_level(problem: ProblemRecord) -> int | None:
    value = (problem.metadata or {}).get("difficulty_level")
    try:
        level = int(value)
    except (TypeError, ValueError):
        return None
    return level if level in DIFFICULTY_PENALTIES else None


def _frontier_provenance(batch_result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    provenance = batch_result.get("frontier_provenance", [])
    if isinstance(provenance, list):
        return [item for item in provenance if isinstance(item, Mapping) and item]
    if isinstance(provenance, Mapping) and provenance:
        return [provenance]
    return []


def _mapped_campaign_execution(
    problem: ProblemRecord,
    campaign_result: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    if str(campaign_result.get("problem_fingerprint", "")) != _problem_fingerprint(
        problem
    ):
        return None
    execution = campaign_result.get("search_execution")
    if not isinstance(execution, Mapping):
        return None
    if execution.get("outcome") == "domain_scan_not_logically_mapped_to_negation":
        return None
    if execution.get("executions") and not execution.get("deterministic"):
        return None
    if not execution.get("deterministic") or not execution.get("replayable"):
        return None
    if not execution.get("executor_id"):
        return None
    return execution


def _mapped_batch_model(
    problem: ProblemRecord,
    batch_result: Mapping[str, Any],
) -> bool:
    if not batch_result:
        return False
    if str(batch_result.get("statement_hash", "")) != _sha256_text(
        problem.statement
    ):
        return False
    if str(batch_result.get("model_audit_status", "")) != "approved":
        return False
    return str(batch_result.get("claim_scope", "")) in {
        "full_claim",
        "explicit_subclaim",
        "restricted_family",
    }


def _has_structured_frontier(batch_result: Mapping[str, Any]) -> bool:
    structural_tokens = (
        "catalog",
        "corpus",
        "core_famil",
        "derived_",
        "first_unknown",
        "excluded_settled",
        "known_",
        "target_",
        "normal_form",
        "symmetry",
    )
    return any(
        any(token in str(key).lower() for token in structural_tokens)
        for item in _frontier_provenance(batch_result)
        for key in item
    )


def _score_resolution(
    profile: Mapping[str, Any],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    route = str(profile["route"])
    if route == "counterexample":
        score = 20 if profile["source_language"] == "lean4" else 18
        reasons = ["a finite witness is intended to refute the full record-level claim"]
    elif route == "subclaim_decomposition":
        score = 8
        reasons = ["only an audited subclaim can expose finite resolution leverage"]
    elif route == "formal_modeling":
        score = 5
        reasons = ["resolution scope remains unknown until formal modeling"]
    else:
        score = 0
        reasons = ["the current logical route is not finite counterexample search"]
    claim_scope = str(batch.get("claim_scope") or campaign.get("search_scope") or "")
    if claim_scope == "full_claim" and route == "counterexample":
        score = 20
        reasons.append("the existing model explicitly covers the full claim")
    elif claim_scope == "explicit_subclaim":
        score = min(score, 16)
        reasons.append("the executor covers a source-explicit subclaim")
    elif claim_scope == "restricted_family":
        score = min(score, 12)
        reasons.append("the current executor is restricted to a family")
    if profile.get("atomicity") != "record_level":
        score = min(score, 4)
        reasons.append("a non-atomic record cannot be resolved by one witness contract")
    return _clamp(score, 0, 20), reasons


def _score_statement_status(problem: ProblemRecord) -> tuple[int, list[str]]:
    metadata = problem.metadata or {}
    quality = str(metadata.get("statement_quality", ""))
    reasons: list[str] = []
    if quality == "formal_lean4":
        score = 10
        if metadata.get("source_file") and metadata.get("source_revision"):
            score += 3
            reasons.append("Lean source file and revision are pinned")
        if problem.references:
            score += 2
            reasons.append("the formal declaration has source references")
    elif quality == "detail_page":
        score = 8
        if metadata.get("source_page_sha256"):
            score += 3
            reasons.append("the detail page is content-addressed")
        status_values = {
            str(metadata.get(field, "")).strip().lower()
            for field in ("status", "detail_status", "index_status")
            if metadata.get(field)
        }
        if status_values == {"open"}:
            score += 2
            reasons.append("local index and detail status agree")
        if not metadata.get("source_consistency_flags"):
            score += 2
            reasons.append("no source-consistency flags are recorded")
    else:
        score = 5
        reasons.append(f"statement quality is {quality or 'unknown'}")
    return _clamp(score, 0, 15), reasons


def _score_verifier(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    text: str,
    object_groups: Mapping[str, list[str]],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    if str(batch.get("verification_status", "")) == "verified":
        return 20, ["an independently verified candidate already exists"]
    if batch and str(batch.get("model_audit_status", "")) == "approved":
        score = 15
        reasons.append("an audited deterministic statement-specific executor exists")
    elif batch:
        score = 11
        reasons.append("a statement-specific executor is registered")
    elif isinstance(campaign.get("search_execution"), Mapping):
        score = 10
        reasons.append("a deterministic bounded executor already produced evidence")
    elif (
        profile["source_language"] == "lean4"
        and profile.get("finite_witness_sufficient") is True
    ):
        score = 8
        reasons.append("Lean provides an exact target, but not yet a candidate checker")
    else:
        score = {
            "graph_theory": 7,
            "combinatorics": 7,
            "number_theory": 7,
            "group_theory": 7,
            "algebra": 6,
            "geometry": 5,
            "computer_science": 5,
            "topology": 2,
            "partial_differential_equations": 1,
            "mathematical_physics": 1,
            "research_mathematics": 3,
        }.get(problem.domain, 3)
        reasons.append(f"only a {problem.domain} domain baseline is available")
    if sum(bool(matches) for matches in object_groups.values()) >= 2:
        score += 2
        reasons.append("the statement suggests a compact canonical certificate")
    if any(cue.lower() in text.lower() for cue in _EXACT_CHECK_CUES):
        score += 1
        reasons.append("the conclusion exposes an exactly recomputable invariant")
    if profile.get("global_operators"):
        score = min(score, 4)
        reasons.append("global/asymptotic semantics require a nonlocal certificate")
    return _clamp(score, 0, 20), reasons


def _score_compressibility(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    text: str,
    object_groups: Mapping[str, list[str]],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    frontier = _frontier_provenance(batch)
    if frontier and _has_structured_frontier(batch):
        score = 16
        reasons.append("an existing executor records a structured finite frontier")
    elif frontier:
        score = 14
        reasons.append("an executor is implemented, but its frontier is only a bound")
    elif batch:
        score = 14
        reasons.append("a statement-specific search representation is implemented")
    elif isinstance(campaign.get("search_execution"), Mapping):
        score = 12
        reasons.append("a bounded executable representation already exists")
    else:
        represented = sum(bool(matches) for matches in object_groups.values())
        score = {
            "graph_theory": 8,
            "combinatorics": 8,
            "number_theory": 6,
            "group_theory": 8,
            "algebra": 6,
            "geometry": 4,
            "computer_science": 6,
            "research_mathematics": 3,
        }.get(problem.domain, 3)
        score += min(6, represented * 2)
        if represented:
            reasons.append(f"finite-object cues span {represented} representation group(s)")
        if profile.get("finite_domain_evidence"):
            score += 4
            reasons.append(
                "Lean declaration exposes finite/decidable type-class evidence"
            )
        elif profile.get("finite_representation_evidence"):
            score += 2
            reasons.append("the candidate object has a finite textual representation")
    if _PARAMETER_RE.search(text):
        score += 2
        reasons.append("the statement exposes a parameter axis")
    if profile.get("global_operators"):
        score = min(score, 4)
    if any(cue.lower() in text.lower() for cue in _CONTINUOUS_CUES):
        score -= 2
        reasons.append("continuous/global objects resist canonical finite enumeration")
    return _clamp(score, 0, 20), reasons


def _score_boundary(
    problem: ProblemRecord,
    text: str,
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    if _has_structured_frontier(batch):
        return 9, ["the previous campaign records a concrete search frontier"]
    if _frontier_provenance(batch):
        return 3, ["the previous campaign records only a configured search bound"]
    matches = [cue for cue in _FRONTIER_CUES if cue.lower() in text.lower()]
    score = min(8, len(matches) * 2)
    reasons: list[str] = []
    if matches:
        reasons.append("boundary cues: " + ", ".join(matches[:4]))
    if _PARAMETER_RE.search(problem.statement):
        score += 1
        reasons.append("a first parameter axis can be stratified")
    if not reasons:
        reasons.append("no machine-readable first-unknown boundary is recorded")
    return _clamp(score, 0, 10), reasons


def _score_feedback(
    profile: Mapping[str, Any],
    text: str,
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    if batch:
        has_graded_signal = any(
            key in batch
            for key in (
                "premise_hit_rate",
                "objective_margin",
                "residual_signal",
                "score_histogram",
            )
        )
        score = 6 if has_graded_signal else 4
        reasons = [
            (
                "the executor records a graded residual signal"
                if has_graded_signal
                else "the executor currently reports only outcomes and stop reasons"
            )
        ]
    else:
        score = 3 if profile.get("finite_witness_sufficient") is True else 1
        reasons = ["only a binary candidate predicate is currently implied"]
    matches = [cue for cue in _FEEDBACK_CUES if cue.lower() in text.lower()]
    score += min(4, len(matches))
    if matches:
        reasons.append("graded objective cues: " + ", ".join(matches[:5]))
    if any(cue in text.lower() for cue in ("infinitely many", "does there exist")):
        score -= 2
        reasons.append("sparse existence language weakens local feedback")
    return _clamp(score, 0, 10), reasons


def _score_local_reuse(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> tuple[int, list[str]]:
    if batch:
        return 5, ["local model, executor, and prior run artifacts are reusable"]
    if isinstance(campaign.get("search_execution"), Mapping):
        return 4, ["a local bounded executor is reusable"]
    metadata = problem.metadata or {}
    if profile["source_language"] == "lean4":
        return 4, ["the pinned Lean module and imports are available locally"]
    if metadata.get("source_page_sha256"):
        return 2, ["the source snapshot is reusable for modeling"]
    return 1, ["only the bank record is locally reusable"]


def _null_search_penalty(batch: Mapping[str, Any], statement_hash: str) -> int:
    if not batch or batch.get("candidate_fingerprint"):
        return 0
    if str(batch.get("statement_hash", "")) != statement_hash:
        return 0
    checked = int(batch.get("checked_cases") or 0)
    attempts = int(batch.get("attempt_count") or 0)
    if checked <= 0:
        return 0
    return min(
        15,
        round(2 * math.log10(1 + checked)) + min(3, attempts),
    )


def _search_entropy_penalty(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    text: str,
    object_groups: Mapping[str, list[str]],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> int:
    if _has_structured_frontier(batch):
        return 1
    if batch:
        return 4
    if profile.get("global_operators"):
        return 10
    lowered = text.lower()
    if profile.get("header_binder_risks"):
        return 8
    if any(cue.lower() in lowered for cue in _HIGH_ENTROPY_OBJECT_CUES):
        return 9
    if any(cue.lower() in lowered for cue in _CONTINUOUS_CUES):
        return 8
    represented = sum(bool(matches) for matches in object_groups.values())
    if profile.get("finite_domain_evidence"):
        return 1
    if profile.get("finite_representation_evidence"):
        return 3
    if isinstance(campaign.get("search_execution"), Mapping):
        return 3
    if represented >= 2:
        return 3
    if represented == 1 and _PARAMETER_RE.search(text):
        return 5
    return 7


def _verifier_correlation_penalty(batch: Mapping[str, Any]) -> int:
    if not batch:
        return 0
    if str(batch.get("verification_status", "")) == "verified":
        return 0
    if batch.get("candidate_fingerprint"):
        return 5
    return 2


def _score_confidence(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    campaign: Mapping[str, Any],
    batch: Mapping[str, Any],
) -> tuple[float, int]:
    confidence = 0.46
    uncertainty = 9
    if profile["source_language"] == "lean4":
        confidence += 0.12
        uncertainty -= 2
    if (problem.metadata or {}).get("source_page_sha256"):
        confidence += 0.10
        uncertainty -= 1
    if campaign:
        confidence += 0.08
        uncertainty -= 1
    if batch:
        confidence += 0.16
        uncertainty -= 2
    if profile.get("needs_elaboration"):
        confidence -= 0.08
        uncertainty += 2
    return round(max(0.1, min(1.0, confidence)), 2), max(2, uncertainty)


def _eligibility(
    problem: ProblemRecord,
    profile: Mapping[str, Any],
    batch: Mapping[str, Any],
    prior_search_without_candidate: bool,
    score_lower_bound: int,
    verifier_score: int,
) -> dict[str, Any]:
    metadata = problem.metadata or {}
    current_status_verified = bool(
        metadata.get("current_status_verified")
        or metadata.get("current_status_verified_at")
    )
    status_gate: bool | None = True if current_status_verified else None
    finite_gate = profile.get("finite_witness_sufficient")
    checker_gate: bool | None = (
        True
        if batch and str(batch.get("model_audit_status", "")) == "approved"
        else None
    )
    independent_gate: bool | None = (
        True if str(batch.get("verification_status", "")) == "verified" else None
    )
    gates = [
        {
            "gate_id": "current_open_status",
            "result": status_gate,
            "blocking": True,
            "evidence": (
                ["metadata current-status verification"]
                if current_status_verified
                else ["local bank snapshot only"]
            ),
        },
        {
            "gate_id": "finite_refutation",
            "result": finite_gate,
            "blocking": True,
            "evidence": [str(profile.get("quantifier_structure", "unknown"))],
        },
        {
            "gate_id": "deterministic_checker",
            "result": checker_gate,
            "blocking": True,
            "evidence": (
                ["approved batch model"]
                if checker_gate
                else ["no audited checker contract yet"]
            ),
        },
        {
            "gate_id": "independent_verifier",
            "result": independent_gate,
            "blocking": False,
            "evidence": (
                ["independent verification recorded"]
                if independent_gate
                else ["required before candidate promotion"]
            ),
        },
    ]
    route = str(profile["route"])
    if batch.get("candidate_fingerprint"):
        status = "candidate_already_found"
    elif profile.get("atomicity") in {"bundled", "context_dependent"}:
        status = "needs_atomic_split"
    elif route in {
        "witness_discovery",
        "answer_discovery",
        "not_counterexample",
        "subclaim_decomposition",
    }:
        status = "not_counterexample_target"
    elif route == "formal_modeling" or finite_gate is None:
        status = "modeling_candidate"
    elif finite_gate is False:
        status = "not_counterexample_target"
    elif prior_search_without_candidate:
        status = "new_strategy_only"
    elif status_gate is None:
        status = "needs_status_audit"
    elif checker_gate is not True:
        status = "modeling_candidate"
    elif score_lower_bound >= 70 and verifier_score >= 15:
        status = "pilot_ready"
    else:
        status = "modeling_candidate"
    blockers = [
        gate["gate_id"]
        for gate in gates
        if gate["blocking"] and gate["result"] is not True
    ]
    return {"status": status, "gates": gates, "blockers": blockers}


def _decision(
    eligibility: Mapping[str, Any],
    score_lower_bound: int,
) -> dict[str, Any]:
    status = str(eligibility["status"])
    if status == "candidate_already_found":
        tier = "candidate_review"
        action = "review the existing candidate instead of starting a duplicate search"
    elif status == "needs_atomic_split":
        tier = "statement_work"
        action = "split the record into source-explicit atomic claims"
    elif status == "not_counterexample_target":
        tier = "alternate_route"
        action = "route to proof, witness discovery, answer recovery, or decomposition"
    elif status == "modeling_candidate":
        tier = "modeling"
        action = "elaborate the exact negation and implement a deterministic checker"
    elif status == "new_strategy_only":
        tier = "retry_only_with_new_representation"
        action = "do not repeat the prior null search; require a materially new representation"
    elif score_lower_bound >= 70:
        tier = "high_priority_audit"
        action = "audit current status and compile an attack card before a short pilot"
    elif score_lower_bound >= 55:
        tier = "short_pilot_after_audit"
        action = "audit status and checker semantics, then run only a bounded pilot"
    elif score_lower_bound >= 40:
        tier = "checker_investment_only"
        action = "improve the model, boundary, and feedback before allocating search"
    else:
        tier = "park"
        action = "park until new structural information or a better representation appears"
    return {
        "tier": tier,
        "recommended_action": action,
        "blockers": list(eligibility.get("blockers", [])),
    }


def score_problem_targetability(
    problem: ProblemRecord,
    *,
    campaign_result: Mapping[str, Any] | None = None,
    batch_result: Mapping[str, Any] | None = None,
    source_bank_path: Path | str | None = None,
) -> dict[str, Any]:
    campaign = dict(campaign_result or {})
    batch = dict(batch_result or {})
    profile = _logical_profile(problem, campaign)
    scoring_campaign = dict(campaign)
    mapped_campaign_execution = _mapped_campaign_execution(problem, campaign)
    if mapped_campaign_execution is None:
        scoring_campaign.pop("search_execution", None)
    scoring_batch = batch if _mapped_batch_model(problem, batch) else {}
    campaign_checked = int(
        (mapped_campaign_execution or {}).get("checked_cases") or 0
    )
    batch_checked = int(scoring_batch.get("checked_cases") or 0)
    text = " ".join(
        (
            problem.title,
            problem.statement,
            problem.notes,
            " ".join(problem.tags),
        )
    )
    object_groups = _matched_groups(text)
    statement_hash = _sha256_text(problem.statement)

    resolution, resolution_reasons = _score_resolution(
        profile, scoring_campaign, scoring_batch
    )
    statement_status, status_reasons = _score_statement_status(problem)
    verifier, verifier_reasons = _score_verifier(
        problem,
        profile,
        text,
        object_groups,
        scoring_campaign,
        scoring_batch,
    )
    compressibility, compressibility_reasons = _score_compressibility(
        problem,
        profile,
        text,
        object_groups,
        scoring_campaign,
        scoring_batch,
    )
    boundary, boundary_reasons = _score_boundary(
        problem, text, scoring_batch
    )
    feedback, feedback_reasons = _score_feedback(
        profile, text, scoring_batch
    )
    reuse, reuse_reasons = _score_local_reuse(
        problem, profile, scoring_campaign, scoring_batch
    )
    components = {
        "resolution_leverage": resolution,
        "statement_status_confidence": statement_status,
        "certificate_verifier_readiness": verifier,
        "search_compressibility": compressibility,
        "boundary_leverage": boundary,
        "feedback_quality": feedback,
        "local_reuse": reuse,
    }
    gross = sum(components.values())

    difficulty = _difficulty_level(problem)
    difficulty_penalty = (
        DIFFICULTY_PENALTIES[difficulty] if difficulty is not None else 4
    )
    batch_null_penalty = _null_search_penalty(
        scoring_batch, statement_hash
    )
    campaign_null_penalty = (
        min(15, round(2 * math.log10(1 + campaign_checked)) + 1)
        if campaign_checked > 0
        and not (mapped_campaign_execution or {}).get("candidate")
        else 0
    )
    null_penalty = max(batch_null_penalty, campaign_null_penalty)
    entropy_penalty = _search_entropy_penalty(
        problem,
        profile,
        text,
        object_groups,
        scoring_campaign,
        scoring_batch,
    )
    correlation_penalty = _verifier_correlation_penalty(scoring_batch)
    penalties = {
        "difficulty": difficulty_penalty,
        "prior_null_saturation": null_penalty,
        "search_entropy": entropy_penalty,
        "verifier_correlation": correlation_penalty,
    }
    targetability_score = _clamp(gross - sum(penalties.values()), 0, 100)
    evidence_coverage, uncertainty = _score_confidence(
        problem, profile, scoring_campaign, scoring_batch
    )
    lower_bound = _clamp(targetability_score - uncertainty, 0, 100)
    upper_bound = _clamp(targetability_score + uncertainty, 0, 100)
    eligibility = _eligibility(
        problem,
        profile,
        scoring_batch,
        (
            (batch_checked > 0 and not scoring_batch.get("candidate_fingerprint"))
            or (
                campaign_checked > 0
                and not (mapped_campaign_execution or {}).get("candidate")
            )
        ),
        lower_bound,
        verifier,
    )
    decision = _decision(eligibility, lower_bound)
    impact_score = 50 if difficulty is None else difficulty * 20

    positive_reasons = {
        "resolution_leverage": resolution_reasons,
        "statement_status_confidence": status_reasons,
        "certificate_verifier_readiness": verifier_reasons,
        "search_compressibility": compressibility_reasons,
        "boundary_leverage": boundary_reasons,
        "feedback_quality": feedback_reasons,
        "local_reuse": reuse_reasons,
    }
    negative_reasons = [
        f"difficulty penalty={difficulty_penalty}",
        f"search entropy penalty={entropy_penalty}",
    ]
    if null_penalty:
        negative_reasons.append(
            f"prior null-search saturation penalty={null_penalty}"
        )
    if correlation_penalty:
        negative_reasons.append(
            f"same-pipeline verifier correlation penalty={correlation_penalty}"
        )
    negative_reasons.extend(str(item) for item in profile.get("blockers", []))

    metadata = problem.metadata or {}
    return {
        "schema_version": TARGETABILITY_SCHEMA_VERSION,
        "score_model_version": TARGETABILITY_ENGINE_VERSION,
        "target_id": problem.problem_id,
        "problem_id": problem.problem_id,
        "parent_problem_id": None,
        "canonical_group_id": _canonical_group_id(problem),
        "statement_hash": statement_hash,
        "title": problem.title,
        "statement": problem.statement,
        "domain": problem.domain,
        "source": problem.source,
        "source_url": _source_url(problem),
        "source_bank_path": str(source_bank_path or ""),
        "difficulty_level": difficulty,
        "impact_score": impact_score,
        "logical_profile": profile,
        "claim_kind": profile["claim_kind"],
        "route": profile["route"],
        "eligibility": eligibility,
        "eligibility_status": eligibility["status"],
        "score": {
            "gross": gross,
            "penalty_total": sum(penalties.values()),
            "targetability_score": targetability_score,
            "score_lower_bound": lower_bound,
            "score_upper_bound": upper_bound,
            "evidence_coverage": evidence_coverage,
            "features": components,
            "penalties": penalties,
        },
        "cets_score": gross,
        "priority_score": lower_bound,
        "component_scores": components,
        "empirical_history": {
            "checked_cases_without_candidate": (
                (
                    batch_checked
                    if not scoring_batch.get("candidate_fingerprint")
                    else 0
                )
                + (
                    campaign_checked
                    if not (mapped_campaign_execution or {}).get("candidate")
                    else 0
                )
            ),
            "attempts_without_candidate": (
                (
                    int(scoring_batch.get("attempt_count") or 0)
                    if not scoring_batch.get("candidate_fingerprint")
                    else 0
                )
                + (1 if campaign_checked > 0 else 0)
            ),
            "candidate_fingerprint": batch.get("candidate_fingerprint"),
            "stop_reasons": list(batch.get("stop_reasons") or []),
            "campaign_status": campaign.get("status"),
        },
        "decision": decision,
        "explanation": {
            "positive_reasons": positive_reasons,
            "negative_reasons": negative_reasons,
        },
        "evidence": {
            "statement_quality": str(metadata.get("statement_quality", "")),
            "source_consistency_flags": [
                str(item) for item in metadata.get("source_consistency_flags", [])
            ],
            "source_revision": metadata.get("source_revision"),
            "source_file": metadata.get("source_file"),
            "campaign_status": campaign.get("status"),
            "batch_status": batch.get("aggregate_status"),
            "batch_verification_status": batch.get("verification_status"),
            "object_cues": {
                group: matches[:8]
                for group, matches in object_groups.items()
                if matches
            },
        },
    }


def _score_band(score: int) -> str:
    if score >= 70:
        return "70-100"
    if score >= 55:
        return "55-69"
    if score >= 40:
        return "40-54"
    return "0-39"


def _shortlist_rows(
    rows: Sequence[dict[str, Any]],
    *,
    shortlist_size: int,
    max_per_cluster: int,
) -> list[dict[str, Any]]:
    cluster_counts: Counter[str] = Counter()
    shortlist: list[dict[str, Any]] = []
    allowed_statuses = {"needs_status_audit", "pilot_ready"}
    for row in rows:
        if row["route"] != "counterexample":
            continue
        modeling_with_finite_shape = (
            row["eligibility_status"] == "modeling_candidate"
            and row["logical_profile"].get("finite_witness_sufficient") is True
        )
        if (
            row["eligibility_status"] not in allowed_statuses
            and not modeling_with_finite_shape
        ):
            continue
        cluster_id = str(row["canonical_group_id"])
        if cluster_counts[cluster_id] >= max_per_cluster:
            continue
        shortlist.append(row)
        cluster_counts[cluster_id] += 1
        if len(shortlist) >= shortlist_size:
            break
    return shortlist


def _retry_rows(
    rows: Sequence[dict[str, Any]],
    *,
    retry_size: int,
) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row["eligibility_status"] == "new_strategy_only"
    ][:retry_size]


def _render_report(
    *,
    bank_paths: Sequence[Path],
    campaign_dir: Path,
    inventory: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    shortlist: Sequence[Mapping[str, Any]],
    retry_shortlist: Sequence[Mapping[str, Any]],
    generated_at: str,
) -> str:
    admission_counts = Counter(str(row["admission_status"]) for row in inventory)
    route_counts = Counter(str(row["route"]) for row in rows)
    eligibility_counts = Counter(str(row["eligibility_status"]) for row in rows)
    band_counts = Counter(_score_band(int(row["priority_score"])) for row in rows)
    source_counts = Counter(str(row["source"]) for row in rows)
    lines = [
        "# 全题库反例可攻关性筛选",
        "",
        f"生成时间：{generated_at}",
        "",
        "## 范围",
        "",
        *[f"- 输入题库：`{path}`" for path in bank_paths],
        f"- 历史搜索证据：`{campaign_dir}`",
        f"- 输入记录：{len(inventory)}",
        f"- 进入规范化评分：{len(rows)}",
        f"- 自动短名单：{len(shortlist)}",
        f"- 来源分布：`{json.dumps(dict(sorted(source_counts.items())), ensure_ascii=False)}`",
        "",
        "这是一套确定性的选题分诊规则，不是在断言某题必有反例。短名单仍须逐题核对当前开放状态、原题语义和反例证书契约。",
        "",
        "## 评分口径",
        "",
        "| 正向特征 | 最高分 |",
        "| --- | ---: |",
    ]
    for component, maximum in COMPONENT_MAXIMA.items():
        lines.append(f"| `{component}` | {maximum} |")
    lines.extend(
        [
            "",
            "毛分满分 100，再扣除题目难度、既往大规模无候选搜索、无结构搜索熵和验证器相关性。数学影响力单独显示，不进入 targetability 分数；排序使用保守下界。",
            "",
            "## 分流统计",
            "",
            f"- 入库门槛：`{json.dumps(dict(sorted(admission_counts.items())), ensure_ascii=False)}`",
            f"- 研究路由：`{json.dumps(dict(sorted(route_counts.items())), ensure_ascii=False)}`",
            f"- 门槛状态：`{json.dumps(dict(sorted(eligibility_counts.items())), ensure_ascii=False)}`",
            f"- 保守分数档：`{json.dumps(dict(sorted(band_counts.items())), ensure_ascii=False)}`",
            "",
            "## 自动短名单",
            "",
            "| 排名 | 保守分 | 点估计 | 毛分 | 问题 | 来源 | 路由状态 |",
            "| ---: | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in shortlist:
        title = str(row["title"]).replace("|", "\\|")
        score = row["score"]
        lines.append(
            f"| {row['rank']} | {score['score_lower_bound']} | "
            f"{score['targetability_score']} | {score['gross']} | "
            f"`{row['problem_id']}` {title} | {row['source']} | "
            f"{row['eligibility_status']} |"
        )
    lines.extend(
        [
            "",
            "## 已搜索目标：仅限新策略重试",
            "",
            "| 排名 | 保守分 | 已检查案例 | 问题 |",
            "| ---: | ---: | ---: | --- |",
        ]
    )
    for row in retry_shortlist:
        title = str(row["title"]).replace("|", "\\|")
        lines.append(
            f"| {row['rank']} | {row['priority_score']} | "
            f"{row['empirical_history']['checked_cases_without_candidate']} | "
            f"`{row['problem_id']}` {title} |"
        )
    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- `needs_status_audit`：本地题面有潜力，但必须先用权威来源核对截至当前日期仍开放。",
            "- `modeling_candidate`：量词或 checker 尚未充分恢复，只可投入建模。",
            "- `new_strategy_only`：已有无候选搜索历史，除非表示、边界或理论假设发生实质变化，否则不重跑。",
            "- `not_counterexample_target`：转向正见证、证明、答案恢复或子命题拆分。",
            "- Formal Conjectures 中的 `answer(sorry)` 是未知答案占位符，不是已解答，也不按普通等价命题计分。",
            "- `∀ᶠ`、`∀ᵉ`、`∃ᶠ`、极限与渐近命题不会因出现一个失败点就被判为可有限反驳。",
            "",
        ]
    )
    return "\n".join(lines)


def screen_problem_banks_targetability(
    *,
    bank_paths: Sequence[Path],
    campaign_dir: Path,
    output_dir: Path,
    shortlist_size: int = 25,
    max_per_cluster: int = 2,
) -> dict[str, Any]:
    if not bank_paths:
        raise ValueError("at least one bank_path is required")
    if shortlist_size <= 0:
        raise ValueError("shortlist_size must be positive")
    if max_per_cluster <= 0:
        raise ValueError("max_per_cluster must be positive")
    resolved_banks = [Path(path).expanduser().resolve() for path in bank_paths]
    campaign_dir = campaign_dir.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    campaign_results = _read_jsonl(campaign_dir / "results.jsonl")
    batch_results = _read_jsonl(campaign_dir / "BATCH2_STATUS.jsonl")

    inventory: list[dict[str, Any]] = []
    admitted: list[tuple[ProblemRecord, Path]] = []
    seen_problem_ids: set[str] = set()
    for bank_path in resolved_banks:
        for problem in load_problem_bank(bank_path):
            inventory_row = _inventory_decision(
                problem,
                bank_path=bank_path,
                seen_problem_ids=seen_problem_ids,
            )
            inventory.append(inventory_row)
            if inventory_row["included_in_ranking"]:
                admitted.append((problem, bank_path))
            seen_problem_ids.add(problem.problem_id)

    rows = [
        score_problem_targetability(
            problem,
            campaign_result=campaign_results.get(problem.problem_id),
            batch_result=batch_results.get(problem.problem_id),
            source_bank_path=bank_path,
        )
        for problem, bank_path in admitted
    ]
    rows.sort(
        key=lambda row: (
            -int(row["score"]["score_lower_bound"]),
            -int(row["score"]["targetability_score"]),
            -int(row["score"]["gross"]),
            -int(row["impact_score"]),
            str(row["problem_id"]),
        )
    )
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    shortlist = _shortlist_rows(
        rows,
        shortlist_size=shortlist_size,
        max_per_cluster=max_per_cluster,
    )
    retry_shortlist = _retry_rows(rows, retry_size=shortlist_size)
    generated_at = utc_now_iso()
    output_dir.mkdir(parents=True, exist_ok=True)

    input_files: list[dict[str, Any]] = []
    for path in [
        *resolved_banks,
        campaign_dir / "results.jsonl",
        campaign_dir / "BATCH2_STATUS.jsonl",
    ]:
        input_files.append(
            {
                "path": str(path),
                "exists": path.exists(),
                "sha256": _sha256_file(path) if path.exists() else None,
                "size_bytes": path.stat().st_size if path.exists() else None,
            }
        )
    manifest = {
        "schema_version": TARGETABILITY_SCHEMA_VERSION,
        "engine_version": TARGETABILITY_ENGINE_VERSION,
        "generated_at": generated_at,
        "input_files": input_files,
        "rules": {
            "allowed_statement_quality": [
                "detail_page",
                "formal_lean4",
                "curated",
                "exact",
                "verified",
            ],
            "difficulty_penalties": DIFFICULTY_PENALTIES,
            "unknown_difficulty_penalty": 4,
            "known_resolved_overrides": KNOWN_RESOLVED_OVERRIDES,
            "known_statement_repair_overrides": (
                KNOWN_STATEMENT_REPAIR_OVERRIDES
            ),
            "shortlist_size": shortlist_size,
            "max_per_cluster": max_per_cluster,
            "ranking_key": [
                "score_lower_bound desc",
                "targetability_score desc",
                "gross desc",
                "impact_score desc (tie-break only)",
                "problem_id asc",
            ],
        },
    }
    summary = {
        "schema_version": TARGETABILITY_SCHEMA_VERSION,
        "engine_version": TARGETABILITY_ENGINE_VERSION,
        "generated_at": generated_at,
        "bank_paths": [str(path) for path in resolved_banks],
        "campaign_dir": str(campaign_dir),
        "output_dir": str(output_dir),
        "input_record_count": len(inventory),
        "ranked_target_count": len(rows),
        "canonical_group_count": len(
            {str(row["canonical_group_id"]) for row in rows}
        ),
        "shortlist_size": len(shortlist),
        "retry_shortlist_size": len(retry_shortlist),
        "admission_counts": dict(
            Counter(row["admission_status"] for row in inventory)
        ),
        "route_counts": dict(Counter(row["route"] for row in rows)),
        "eligibility_counts": dict(
            Counter(row["eligibility_status"] for row in rows)
        ),
        "priority_band_counts": dict(
            Counter(_score_band(int(row["priority_score"])) for row in rows)
        ),
        "shortlist_problem_ids": [row["problem_id"] for row in shortlist],
        "retry_shortlist_problem_ids": [
            row["problem_id"] for row in retry_shortlist
        ],
        "files": {
            "inventory": str(output_dir / TARGETABILITY_INVENTORY_FILE),
            "ranking_jsonl": str(output_dir / TARGETABILITY_RANKING_FILE),
            "ranking_csv": str(output_dir / TARGETABILITY_RANKING_CSV_FILE),
            "shortlist": str(output_dir / TARGETABILITY_SHORTLIST_FILE),
            "summary": str(output_dir / TARGETABILITY_SUMMARY_FILE),
            "report": str(output_dir / TARGETABILITY_REPORT_FILE),
            "manifest": str(output_dir / TARGETABILITY_MANIFEST_FILE),
        },
    }

    _write_jsonl(output_dir / TARGETABILITY_INVENTORY_FILE, inventory)
    _write_jsonl(output_dir / TARGETABILITY_RANKING_FILE, rows)
    _write_json(
        output_dir / TARGETABILITY_SHORTLIST_FILE,
        {
            "schema_version": TARGETABILITY_SCHEMA_VERSION,
            "engine_version": TARGETABILITY_ENGINE_VERSION,
            "generated_at": generated_at,
            "shortlist": shortlist,
        },
    )
    _write_json(output_dir / TARGETABILITY_SUMMARY_FILE, summary)
    _write_json(output_dir / TARGETABILITY_MANIFEST_FILE, manifest)
    _atomic_write_text(
        output_dir / TARGETABILITY_REPORT_FILE,
        _render_report(
            bank_paths=resolved_banks,
            campaign_dir=campaign_dir,
            inventory=inventory,
            rows=rows,
            shortlist=shortlist,
            retry_shortlist=retry_shortlist,
            generated_at=generated_at,
        ),
    )

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(
        [
            "rank",
            "score_lower_bound",
            "targetability_score",
            "score_upper_bound",
            "gross",
            "penalty_total",
            "problem_id",
            "canonical_group_id",
            "title",
            "source",
            "domain",
            "difficulty_level",
            "impact_score",
            "claim_kind",
            "route",
            "eligibility_status",
            *COMPONENT_MAXIMA,
        ]
    )
    for row in rows:
        score = row["score"]
        writer.writerow(
            [
                row["rank"],
                score["score_lower_bound"],
                score["targetability_score"],
                score["score_upper_bound"],
                score["gross"],
                score["penalty_total"],
                row["problem_id"],
                row["canonical_group_id"],
                row["title"],
                row["source"],
                row["domain"],
                row["difficulty_level"],
                row["impact_score"],
                row["claim_kind"],
                row["route"],
                row["eligibility_status"],
                *(
                    row["component_scores"][component]
                    for component in COMPONENT_MAXIMA
                ),
            ]
        )
    _atomic_write_text(
        output_dir / TARGETABILITY_RANKING_CSV_FILE,
        csv_buffer.getvalue(),
    )
    return summary


def screen_problem_bank_targetability(
    *,
    bank_path: Path,
    campaign_dir: Path,
    output_dir: Path,
    shortlist_size: int = 25,
) -> dict[str, Any]:
    return screen_problem_banks_targetability(
        bank_paths=[bank_path],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
        shortlist_size=shortlist_size,
    )


__all__ = [
    "COMPONENT_MAXIMA",
    "TARGETABILITY_ENGINE_VERSION",
    "TARGETABILITY_INVENTORY_FILE",
    "TARGETABILITY_MANIFEST_FILE",
    "TARGETABILITY_RANKING_CSV_FILE",
    "TARGETABILITY_RANKING_FILE",
    "TARGETABILITY_REPORT_FILE",
    "TARGETABILITY_SCHEMA_VERSION",
    "TARGETABILITY_SHORTLIST_FILE",
    "TARGETABILITY_SUMMARY_FILE",
    "score_problem_targetability",
    "screen_problem_bank_targetability",
    "screen_problem_banks_targetability",
]
