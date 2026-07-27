from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

from amra.core.models import ProblemRecord
from amra.domain_executors import select_executors_for_problem
from amra.orchestration.workstreams import utc_now_iso
from amra.problem_banks.registry import load_problem_bank


COUNTEREXAMPLE_CAMPAIGN_SCHEMA_VERSION = "amra.counterexample_campaign.v1"
COUNTEREXAMPLE_RESULT_SCHEMA_VERSION = "amra.counterexample_search_result.v1"
COUNTEREXAMPLE_CAMPAIGN_FILE = "campaign.json"
COUNTEREXAMPLE_RESULTS_FILE = "results.jsonl"
COUNTEREXAMPLE_CANDIDATES_FILE = "candidate_counterexamples.json"
COUNTEREXAMPLE_MODELING_QUEUE_FILE = "modeling_queue.jsonl"
COUNTEREXAMPLE_REPORT_FILE = "REPORT.md"
COUNTEREXAMPLE_ENGINE_VERSION = "amra.counterexample_campaign.engine.v2"


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    body = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    _atomic_write_text(path, body)


def _load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        problem_id = str(row.get("problem_id", "")).strip()
        if problem_id:
            records[problem_id] = row
    return records


def _fingerprint_problem(problem: ProblemRecord) -> str:
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
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _fingerprint_search_config(budget: dict[str, int]) -> str:
    payload = json.dumps(
        {"engine_version": COUNTEREXAMPLE_ENGINE_VERSION, "budget": budget},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def classify_claim(problem: ProblemRecord) -> dict[str, Any]:
    text = _normalized_text(f"{problem.title}. {problem.statement}")
    lowered = text.lower()
    cues = {
        "universal": sorted(
            set(
                match.group(0)
                for match in re.finditer(
                    r"\b(?:for every|for all|every|all|any|always|must|never|cannot|no)\b",
                    lowered,
                )
            )
        ),
        "existence": sorted(
            set(
                match.group(0)
                for match in re.finditer(
                    r"\b(?:does there exist|do there exist|is there|are there|there exists|"
                    r"there exist|can one|construct|infinitely many|existence)\b",
                    lowered,
                )
            )
        ),
        "equivalence": sorted(
            set(
                match.group(0)
                for match in re.finditer(
                    r"\b(?:if and only if|iff|equivalent|equals?|same as)\b|(?<![<>])=(?!=)",
                    lowered,
                )
            )
        ),
        "classification": sorted(
            set(
                match.group(0)
                for match in re.finditer(
                    r"\b(?:determine|classify|characterize|compute|what is|find all|"
                    r"minimum|maximum|best possible)\b",
                    lowered,
                )
            )
        ),
    }
    has_universal = bool(cues["universal"])
    has_existence = bool(cues["existence"])
    has_equivalence = bool(cues["equivalence"])
    has_classification = bool(cues["classification"])
    if has_universal and has_existence:
        claim_kind = "mixed_quantifiers"
        falsifiability = "subclaim_decomposition_required"
    elif has_universal:
        claim_kind = "universal_claim"
        falsifiability = "finite_witness_possible_after_modeling"
    elif has_equivalence:
        claim_kind = "equivalence_claim"
        falsifiability = "finite_witness_possible_after_modeling"
    elif has_existence:
        claim_kind = "existence_claim"
        falsifiability = "finite_counterexample_not_sufficient"
    elif has_classification:
        claim_kind = "classification_or_optimization"
        falsifiability = "not_a_single_falsifiable_proposition"
    else:
        claim_kind = "unclassified_question"
        falsifiability = "formalization_required"

    subclaims: list[str] = []
    for part in re.split(r"(?:\n+|(?<=[.;?])\s+|\s+\([a-z0-9]+\)\s+)", problem.statement):
        candidate = _normalized_text(part)
        candidate_lower = candidate.lower()
        if len(candidate) < 20:
            continue
        if re.search(
            r"\b(?:for every|for all|every|all|always|must|never|cannot|if and only if|iff)\b",
            candidate_lower,
        ):
            subclaims.append(candidate)
    return {
        "claim_kind": claim_kind,
        "falsifiability": falsifiability,
        "quantifier_cues": cues,
        "candidate_universal_subclaims": subclaims[:8],
    }


def _witness_contract(domain: str) -> dict[str, Any]:
    contracts = {
        "number_theory": (
            "An explicit integer or integer tuple satisfying every hypothesis and an exact-arithmetic trace "
            "showing failure of the conclusion."
        ),
        "graph_theory": (
            "A finite adjacency list, a deterministic hypothesis checker, and a deterministic computation "
            "of the graph property that violates the conclusion."
        ),
        "combinatorics": (
            "A finite family encoded canonically, with exhaustive checks of the premises and the failed bound "
            "or structural conclusion."
        ),
        "group_theory": (
            "A finite multiplication table or checked presentation, certificates for the group hypotheses, "
            "and a computed violation of the target property."
        ),
        "geometry": (
            "Exact coordinates or a combinatorial incidence structure, with symbolic checks of every "
            "nondegeneracy condition and the failed geometric conclusion."
        ),
        "topology": (
            "A finite triangulation, knot diagram, or presentation plus independently checkable invariants; "
            "the encoding must be proved faithful to the stated topological category."
        ),
        "algebra": (
            "A finite algebraic structure or exact symbolic assignment, including closure/axiom checks and "
            "an exact failed identity or implication."
        ),
        "computer_science": (
            "A finite encoded instance and a deterministic checker for both admissibility and violation; "
            "complexity-class separations cannot be certified by a finite instance alone."
        ),
    }
    return {
        "required_witness": contracts.get(
            domain,
            "A finite canonical object with deterministic premise checks and an independently replayable "
            "verification that the stated conclusion fails.",
        ),
        "acceptance_rule": (
            "Do not promote a witness from candidate to refutation until the natural-language claim has an "
            "audited formal model and a second verifier reproduces the violation."
        ),
    }


def _prime_sieve(limit: int) -> bytearray:
    limit = max(1, int(limit))
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if not sieve[prime]:
            continue
        start = prime * prime
        count = ((limit - start) // prime) + 1
        sieve[start : limit + 1 : prime] = b"\x00" * count
    return sieve


def _completed_result(
    *,
    executor_id: str,
    bounds: dict[str, Any],
    checked_cases: int,
    candidate: dict[str, Any] | None = None,
    unresolved_cases: int = 0,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    if candidate:
        outcome = "candidate_counterexample"
    elif unresolved_cases:
        outcome = "inconclusive_within_bound"
    else:
        outcome = "no_counterexample_within_bound"
    return {
        "executor_id": executor_id,
        "status": "completed",
        "outcome": outcome,
        "bounds": bounds,
        "checked_cases": checked_cases,
        "unresolved_cases": unresolved_cases,
        "candidate": candidate,
        "notes": list(notes or []),
        "deterministic": True,
        "replayable": True,
    }


def _search_goldbach(budget: dict[str, int]) -> dict[str, Any]:
    max_n = max(4, int(budget["max_integer"]))
    if max_n % 2:
        max_n -= 1
    primes = _prime_sieve(max_n)
    checked = 0
    for even in range(4, max_n + 1, 2):
        checked += 1
        if any(primes[p] and primes[even - p] for p in range(2, even // 2 + 1)):
            continue
        return _completed_result(
            executor_id="classical.goldbach_exact_scan.v1",
            bounds={"min_even": 4, "max_even": max_n},
            checked_cases=checked,
            candidate={
                "even_integer": even,
                "verification": "No p in [2,n/2] has both p and n-p prime under the exact sieve.",
            },
        )
    return _completed_result(
        executor_id="classical.goldbach_exact_scan.v1",
        bounds={"min_even": 4, "max_even": max_n},
        checked_cases=checked,
    )


def _search_legendre(budget: dict[str, int]) -> dict[str, Any]:
    max_base = max(1, int(budget["max_square_base"]))
    primes = _prime_sieve((max_base + 1) ** 2)
    for n in range(1, max_base + 1):
        lower = n * n
        upper = (n + 1) * (n + 1)
        if any(primes[value] for value in range(lower + 1, upper)):
            continue
        return _completed_result(
            executor_id="classical.legendre_interval_scan.v1",
            bounds={"min_n": 1, "max_n": max_base, "strict_intervals": True},
            checked_cases=n,
            candidate={
                "n": n,
                "interval": [lower, upper],
                "verification": "Exact sieve contains no prime strictly inside the interval.",
            },
        )
    return _completed_result(
        executor_id="classical.legendre_interval_scan.v1",
        bounds={"min_n": 1, "max_n": max_base, "strict_intervals": True},
        checked_cases=max_base,
    )


def _search_collatz(budget: dict[str, int]) -> dict[str, Any]:
    max_start = max(1, int(budget["max_integer"]))
    max_steps = max(1, int(budget["max_steps"]))
    reaches_one = {1}
    unresolved = 0
    max_observed = 1
    for start in range(1, max_start + 1):
        value = start
        path: list[int] = []
        positions: dict[int, int] = {}
        for _ in range(max_steps):
            max_observed = max(max_observed, value)
            if value in reaches_one:
                reaches_one.update(path)
                break
            if value in positions:
                cycle = path[positions[value] :]
                if 1 not in cycle:
                    return _completed_result(
                        executor_id="classical.collatz_cycle_scan.v1",
                        bounds={"max_start": max_start, "max_steps_per_start": max_steps},
                        checked_cases=start,
                        candidate={
                            "starting_value": start,
                            "nontrivial_cycle": cycle,
                            "verification": "Each adjacent value follows the Collatz map and the final value returns to the first.",
                        },
                    )
                break
            positions[value] = len(path)
            path.append(value)
            value = value // 2 if value % 2 == 0 else 3 * value + 1
        else:
            unresolved += 1
    return _completed_result(
        executor_id="classical.collatz_cycle_scan.v1",
        bounds={"max_start": max_start, "max_steps_per_start": max_steps},
        checked_cases=max_start,
        unresolved_cases=unresolved,
        notes=[f"Maximum intermediate value observed: {max_observed}."],
    )


def _search_gilbreath(budget: dict[str, int]) -> dict[str, Any]:
    term_count = max(2, int(budget["max_sequence_terms"]))
    limit = max(20, int(term_count * (math.log(term_count) + math.log(math.log(term_count))) + 20))
    while True:
        sieve = _prime_sieve(limit)
        primes = [value for value in range(2, limit + 1) if sieve[value]]
        if len(primes) >= term_count:
            break
        limit *= 2
    row = primes[:term_count]
    checked_rows = 0
    while len(row) > 1:
        row = [abs(right - left) for left, right in zip(row, row[1:])]
        checked_rows += 1
        if row[0] == 1:
            continue
        return _completed_result(
            executor_id="classical.gilbreath_difference_scan.v1",
            bounds={"prime_terms": term_count},
            checked_cases=checked_rows,
            candidate={
                "difference_row": checked_rows,
                "first_value": row[0],
                "row_prefix": row[:20],
                "verification": "Row is obtained by repeated adjacent absolute differences of the prime prefix.",
            },
        )
    return _completed_result(
        executor_id="classical.gilbreath_difference_scan.v1",
        bounds={"prime_terms": term_count},
        checked_cases=checked_rows,
    )


def _erdos_straus_witness(n: int) -> tuple[int, int, int] | None:
    x_min = (n + 3) // 4
    x_max = (3 * n) // 4
    for x in range(x_min, x_max + 1):
        numerator = 4 * x - n
        denominator = n * x
        if numerator <= 0:
            continue
        y_min = max(x, (denominator + numerator - 1) // numerator)
        y_max = (2 * denominator) // numerator
        for y in range(y_min, y_max + 1):
            remainder_numerator = numerator * y - denominator
            if remainder_numerator <= 0:
                continue
            remainder_denominator = denominator * y
            if remainder_denominator % remainder_numerator:
                continue
            z = remainder_denominator // remainder_numerator
            if y <= z and 4 * x * y * z == n * (x * y + x * z + y * z):
                return x, y, z
    return None


def _search_erdos_straus(budget: dict[str, int]) -> dict[str, Any]:
    max_n = max(3, int(budget["max_erdos_straus_n"]))
    for n in range(3, max_n + 1):
        if _erdos_straus_witness(n) is not None:
            continue
        return _completed_result(
            executor_id="classical.erdos_straus_exact_scan.v1",
            bounds={"min_n": 3, "max_n": max_n, "ordered_denominators": True},
            checked_cases=n - 2,
            candidate={
                "n": n,
                "verification": (
                    "Exhausted n/4 < x <= 3n/4 and the complete y interval implied by x <= y <= z "
                    "without an exact unit-fraction decomposition."
                ),
            },
        )
    return _completed_result(
        executor_id="classical.erdos_straus_exact_scan.v1",
        bounds={"min_n": 3, "max_n": max_n, "ordered_denominators": True},
        checked_cases=max_n - 2,
    )


def _family_as_lists(members: list[int], universe_size: int) -> list[list[int]]:
    return [
        [element + 1 for element in range(universe_size) if subset & (1 << element)]
        for subset in members
    ]


def _search_union_closed(budget: dict[str, int]) -> dict[str, Any]:
    universe_size = max(1, min(4, int(budget["max_family_universe"])))
    subset_count = 1 << universe_size
    family_count = 1 << subset_count
    union_closed_checked = 0
    for family_mask in range(1, family_count):
        members = [subset for subset in range(subset_count) if family_mask & (1 << subset)]
        if not any(members):
            continue
        if any(
            not (family_mask & (1 << (left | right)))
            for left in members
            for right in members
        ):
            continue
        union_closed_checked += 1
        frequencies = [
            sum(1 for subset in members if subset & (1 << element))
            for element in range(universe_size)
        ]
        if max(frequencies, default=0) * 2 >= len(members):
            continue
        return _completed_result(
            executor_id="classical.union_closed_family_scan.v1",
            bounds={"universe_size": universe_size, "candidate_families": family_count - 1},
            checked_cases=union_closed_checked,
            candidate={
                "family": _family_as_lists(members, universe_size),
                "element_frequencies": frequencies,
                "family_size": len(members),
                "verification": "All pairwise unions belong to the family and every element occurs in fewer than half the sets.",
            },
        )
    return _completed_result(
        executor_id="classical.union_closed_family_scan.v1",
        bounds={"universe_size": universe_size, "candidate_families": family_count - 1},
        checked_cases=union_closed_checked,
    )


@lru_cache(maxsize=None)
def _edge_pairs(vertex_count: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )


@lru_cache(maxsize=None)
def _permutations(vertex_count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.permutations(range(vertex_count)))


def _edge_mask(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    index = {edge: bit for bit, edge in enumerate(_edge_pairs(vertex_count))}
    mask = 0
    for left, right in edges:
        edge = (left, right) if left < right else (right, left)
        mask |= 1 << index[edge]
    return mask


@lru_cache(maxsize=None)
def _canonical_graph_code(vertex_count: int, mask: int) -> int:
    pairs = _edge_pairs(vertex_count)
    present = [pairs[bit] for bit in range(len(pairs)) if mask & (1 << bit)]
    best: int | None = None
    for permutation in _permutations(vertex_count):
        permuted = [
            (
                min(permutation[left], permutation[right]),
                max(permutation[left], permutation[right]),
            )
            for left, right in present
        ]
        code = _edge_mask(vertex_count, permuted)
        if best is None or code < best:
            best = code
    return int(best or 0)


def _delete_graph_vertex(vertex_count: int, mask: int, deleted: int) -> int:
    remaining = [vertex for vertex in range(vertex_count) if vertex != deleted]
    renumber = {vertex: index for index, vertex in enumerate(remaining)}
    edges: list[tuple[int, int]] = []
    for bit, (left, right) in enumerate(_edge_pairs(vertex_count)):
        if not (mask & (1 << bit)) or deleted in {left, right}:
            continue
        edges.append((renumber[left], renumber[right]))
    return _edge_mask(vertex_count - 1, edges)


def _graph_edges(vertex_count: int, mask: int) -> list[list[int]]:
    return [
        [left, right]
        for bit, (left, right) in enumerate(_edge_pairs(vertex_count))
        if mask & (1 << bit)
    ]


def _search_reconstruction(budget: dict[str, int]) -> dict[str, Any]:
    max_vertices = max(3, min(6, int(budget["max_graph_vertices"])))
    checked_unlabeled = 0
    for vertex_count in range(3, max_vertices + 1):
        labeled_count = 1 << len(_edge_pairs(vertex_count))
        representatives = {
            _canonical_graph_code(vertex_count, mask)
            for mask in range(labeled_count)
        }
        decks: dict[tuple[int, ...], int] = {}
        for graph in sorted(representatives):
            checked_unlabeled += 1
            deck = tuple(
                sorted(
                    _canonical_graph_code(
                        vertex_count - 1,
                        _delete_graph_vertex(vertex_count, graph, deleted),
                    )
                    for deleted in range(vertex_count)
                )
            )
            previous = decks.get(deck)
            if previous is None:
                decks[deck] = graph
                continue
            if previous != graph:
                return _completed_result(
                    executor_id="classical.graph_reconstruction_scan.v1",
                    bounds={"min_vertices": 3, "max_vertices": max_vertices},
                    checked_cases=checked_unlabeled,
                    candidate={
                        "vertex_count": vertex_count,
                        "graph_a_edges": _graph_edges(vertex_count, previous),
                        "graph_b_edges": _graph_edges(vertex_count, graph),
                        "canonical_deck": list(deck),
                        "verification": "The graphs have different canonical codes and identical multisets of vertex-deleted canonical codes.",
                    },
                )
    return _completed_result(
        executor_id="classical.graph_reconstruction_scan.v1",
        bounds={"min_vertices": 3, "max_vertices": max_vertices},
        checked_cases=checked_unlabeled,
    )


def _tree_from_prufer(sequence: tuple[int, ...], vertex_count: int) -> list[tuple[int, int]]:
    degree = [1] * vertex_count
    for vertex in sequence:
        degree[vertex] += 1
    edges: list[tuple[int, int]] = []
    for vertex in sequence:
        leaf = next(index for index, value in enumerate(degree) if value == 1)
        edges.append((leaf, vertex))
        degree[leaf] -= 1
        degree[vertex] -= 1
    remaining = [index for index, value in enumerate(degree) if value == 1]
    edges.append((remaining[0], remaining[1]))
    return edges


def _graceful_labeling(vertex_count: int, edges: list[tuple[int, int]]) -> tuple[int, ...] | None:
    required = set(range(1, vertex_count))
    for labels in itertools.permutations(range(vertex_count)):
        differences = {abs(labels[left] - labels[right]) for left, right in edges}
        if differences == required:
            return labels
    return None


def _canonical_tree_code(vertex_count: int, edges: list[tuple[int, int]]) -> str:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    remaining = set(range(vertex_count))
    leaves = [vertex for vertex in remaining if len(adjacency[vertex]) <= 1]
    while len(remaining) > 2:
        next_leaves: list[int] = []
        for leaf in leaves:
            remaining.discard(leaf)
            for neighbor in adjacency[leaf]:
                adjacency[neighbor].discard(leaf)
                if neighbor in remaining and len(adjacency[neighbor]) == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves
    centers = sorted(remaining)
    original_adjacency = [[] for _ in range(vertex_count)]
    for left, right in edges:
        original_adjacency[left].append(right)
        original_adjacency[right].append(left)

    def rooted_code(vertex: int, parent: int) -> str:
        children = sorted(
            rooted_code(neighbor, vertex)
            for neighbor in original_adjacency[vertex]
            if neighbor != parent
        )
        return "(" + "".join(children) + ")"

    return min(rooted_code(center, -1) for center in centers)


def _search_graceful_trees(budget: dict[str, int]) -> dict[str, Any]:
    max_vertices = max(2, min(8, int(budget["max_tree_vertices"])))
    checked_trees = 0
    for vertex_count in range(2, max_vertices + 1):
        representatives: dict[str, list[tuple[int, int]]] = {}
        for sequence in itertools.product(range(vertex_count), repeat=max(0, vertex_count - 2)):
            edges = _tree_from_prufer(sequence, vertex_count)
            canonical = _canonical_tree_code(vertex_count, edges)
            representatives.setdefault(canonical, edges)
        for _, edges in sorted(representatives.items()):
            checked_trees += 1
            labeling = _graceful_labeling(vertex_count, edges)
            if labeling is not None:
                continue
            return _completed_result(
                executor_id="classical.graceful_tree_scan.v1",
                bounds={"min_vertices": 2, "max_vertices": max_vertices},
                checked_cases=checked_trees,
                candidate={
                    "vertex_count": vertex_count,
                    "tree_edges": [list(edge) for edge in edges],
                    "verification": "Exhausted every permutation of labels 0 through |E| without obtaining all edge differences 1 through |E|.",
                },
            )
    return _completed_result(
        executor_id="classical.graceful_tree_scan.v1",
        bounds={"min_vertices": 2, "max_vertices": max_vertices},
        checked_cases=checked_trees,
    )
SearchFunction = Callable[[dict[str, int]], dict[str, Any]]


def _select_builtin_search(problem: ProblemRecord) -> tuple[str, SearchFunction] | None:
    title = problem.title.lower()
    statement = problem.statement.lower()
    if "goldbach" in title and "even integer" in statement and "two prime" in statement:
        return "goldbach", _search_goldbach
    if "legendre" in title and "prime" in statement and "n^2" in statement:
        return "legendre", _search_legendre
    if "collatz" in title:
        return "collatz", _search_collatz
    if "gilbreath" in title and ("difference" in statement or "differences" in statement):
        return "gilbreath", _search_gilbreath
    if "straus" in title and "4/n" in statement.replace(" ", ""):
        return "erdos_straus", _search_erdos_straus
    if ("union-closed" in title or "union closed" in title) and "family" in statement:
        return "union_closed", _search_union_closed
    if (
        "reconstruction conjecture" in title
        and "switching" not in title
        and "edge reconstruction" not in title
        and ("vertex-deleted" in statement or "deleting a vertex" in statement)
    ):
        return "graph_reconstruction", _search_reconstruction
    if "graceful tree" in title:
        return "graceful_tree", _search_graceful_trees
    return None


def run_builtin_counterexample_search(
    problem: ProblemRecord,
    *,
    budget: dict[str, int],
) -> dict[str, Any]:
    """Run the audited built-in search registered for one problem."""

    selected = _select_builtin_search(problem)
    if selected is None:
        raise KeyError(f"No built-in counterexample search is registered for '{problem.problem_id}'.")
    search_template, search = selected
    return {
        "search_template": search_template,
        **search(dict(budget)),
    }


def _is_erdos_problem(problem: ProblemRecord) -> bool:
    metadata = problem.metadata or {}
    source_id = str(metadata.get("source_id", ""))
    return bool(metadata.get("erdos_set_member")) or bool(
        re.fullmatch(r"EP-\d+", source_id, re.IGNORECASE)
    )


class CounterexampleCampaignRunner:
    def _search_one(
        self,
        problem: ProblemRecord,
        *,
        budget: dict[str, int],
        search_config_fingerprint: str,
    ) -> dict[str, Any]:
        generated_at = utc_now_iso()
        fingerprint = _fingerprint_problem(problem)
        metadata = problem.metadata or {}
        classification = classify_claim(problem)
        base = {
            "schema_version": COUNTEREXAMPLE_RESULT_SCHEMA_VERSION,
            "generated_at": generated_at,
            "problem_id": problem.problem_id,
            "source_id": str(metadata.get("source_id", "")),
            "title": problem.title,
            "statement": problem.statement,
            "domain": problem.domain,
            "difficulty_level": metadata.get("difficulty_level"),
            "sets": list(metadata.get("sets", [])),
            "source_url": str(metadata.get("source_url", "")),
            "source_page_sha256": metadata.get("source_page_sha256"),
            "problem_fingerprint": fingerprint,
            "search_config_fingerprint": search_config_fingerprint,
            "engine_version": COUNTEREXAMPLE_ENGINE_VERSION,
            "classification": classification,
            "source_consistency_flags": list(metadata.get("source_consistency_flags", [])),
            "witness_contract": _witness_contract(problem.domain),
            "search_scope": "original_claim",
            "search_execution": None,
            "candidate_counterexamples": [],
            "verification_boundary": (
                "A finite witness may refute the audited formal model. Absence of a witness within a finite "
                "bound does not prove the open claim."
            ),
        }
        if _is_erdos_problem(problem):
            return {
                **base,
                "status": "excluded_erdos",
                "search_scope": "excluded",
                "limitations": ["Excluded because the campaign targets non-Erdos UnsolvedMath records."],
            }
        if metadata.get("duplicate_of"):
            return {
                **base,
                "status": "duplicate_skipped",
                "search_scope": "canonical_record_only",
                "duplicate_of": metadata["duplicate_of"],
                "limitations": ["Search is attached to the canonical duplicate record."],
            }
        if metadata.get("statement_quality") != "detail_page":
            return {
                **base,
                "status": "statement_recovery_required",
                "limitations": [
                    "The exact detail statement was unavailable or the source id collides with another "
                    "problem, so an executable counterexample model is unsafe."
                ],
            }
        if "title_conflict" in metadata.get("source_consistency_flags", []):
            return {
                **base,
                "status": "source_conflict_requires_review",
                "search_scope": "source_reconciliation",
                "limitations": [
                    "The browse-index title and detail-page title identify different problems; choosing either "
                    "claim automatically would make any counterexample certificate unsound."
                ],
            }

        selected = _select_builtin_search(problem)
        if selected:
            search_name, search = selected
            execution = search(budget)
            candidates = [execution["candidate"]] if execution.get("candidate") else []
            status = {
                "candidate_counterexample": "candidate_counterexample",
                "inconclusive_within_bound": "bounded_search_inconclusive",
                "no_counterexample_within_bound": "bounded_search_no_counterexample",
            }[str(execution["outcome"])]
            return {
                **base,
                "status": status,
                "search_template": search_name,
                "search_execution": execution,
                "candidate_counterexamples": candidates,
                "limitations": [
                    "The executable template covers only the recorded finite bound.",
                    "A candidate still requires an independent implementation and an audited match to the source statement.",
                ],
            }

        domain_executions: list[dict[str, Any]] = []
        for executor in select_executors_for_problem(problem):
            try:
                domain_executions.append(executor.run(problem).to_dict())
            except Exception as exc:
                domain_executions.append(
                    {
                        "executor_id": executor.metadata.executor_id,
                        "status": "failed",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
        if domain_executions:
            return {
                **base,
                "status": "bounded_domain_scan_completed",
                "search_scope": "supporting_object_scan",
                "search_execution": {
                    "outcome": "domain_scan_not_logically_mapped_to_negation",
                    "executions": domain_executions,
                },
                "limitations": [
                    "The domain executor enumerates relevant objects but is not yet a verified negation checker for this statement."
                ],
            }

        if classification["candidate_universal_subclaims"]:
            base["search_scope"] = "original_or_universal_subclaim"
        if classification["falsifiability"] == "finite_counterexample_not_sufficient":
            status = "not_finitely_refutable"
            limitation = (
                "The statement is existential or infinitary; finite failure to find a witness cannot refute it. "
                "A proof of nonexistence or a refutable necessary subclaim is required."
            )
        elif classification["falsifiability"] == "not_a_single_falsifiable_proposition":
            status = "decomposition_required"
            limitation = "The record asks for a classification or optimum rather than asserting one proposition."
        else:
            status = "manual_modeling_required"
            limitation = (
                "No sound parser/executor pair is registered for the definitions and quantifiers in this statement."
            )
        return {
            **base,
            "status": status,
            "search_plan": {
                "target_subclaims": classification["candidate_universal_subclaims"],
                "next_step": "Encode premises and conclusion as a deterministic predicate before enumeration.",
                "suggested_bounds": budget,
            },
            "limitations": [limitation],
        }

    def run(
        self,
        *,
        bank_path: Path,
        output_dir: Path,
        resume: bool = True,
        max_problems: int | None = None,
        max_integer: int = 100_000,
        max_steps: int = 10_000,
        max_square_base: int = 2_000,
        max_sequence_terms: int = 1_000,
        max_family_universe: int = 4,
        max_graph_vertices: int = 5,
        max_tree_vertices: int = 7,
        max_erdos_straus_n: int = 500,
    ) -> dict[str, Any]:
        bank_path = bank_path.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        problems = load_problem_bank(bank_path)
        if max_problems is not None:
            problems = problems[: max(0, int(max_problems))]
        budget = {
            "max_integer": max(4, int(max_integer)),
            "max_steps": max(1, int(max_steps)),
            "max_square_base": max(1, int(max_square_base)),
            "max_sequence_terms": max(2, int(max_sequence_terms)),
            "max_family_universe": max(1, int(max_family_universe)),
            "max_graph_vertices": max(3, int(max_graph_vertices)),
            "max_tree_vertices": max(2, int(max_tree_vertices)),
            "max_erdos_straus_n": max(3, int(max_erdos_straus_n)),
        }
        results_path = output_dir / COUNTEREXAMPLE_RESULTS_FILE
        existing = _load_jsonl(results_path) if resume else {}
        search_config_fingerprint = _fingerprint_search_config(budget)
        results: list[dict[str, Any]] = []
        reused = 0
        for index, problem in enumerate(problems, start=1):
            fingerprint = _fingerprint_problem(problem)
            previous = existing.get(problem.problem_id)
            if (
                previous
                and previous.get("problem_fingerprint") == fingerprint
                and previous.get("search_config_fingerprint") == search_config_fingerprint
            ):
                result = previous
                reused += 1
            else:
                result = self._search_one(
                    problem,
                    budget=budget,
                    search_config_fingerprint=search_config_fingerprint,
                )
            results.append(result)
            if index % 25 == 0:
                _write_jsonl(results_path, results)
        _write_jsonl(results_path, results)

        candidates = [
            {
                "problem_id": result["problem_id"],
                "source_id": result["source_id"],
                "title": result["title"],
                "source_url": result["source_url"],
                "search_execution": result["search_execution"],
                "verification_boundary": result["verification_boundary"],
            }
            for result in results
            if result["status"] == "candidate_counterexample"
        ]
        _write_json(output_dir / COUNTEREXAMPLE_CANDIDATES_FILE, candidates)
        incomplete_statuses = {
            "bounded_domain_scan_completed",
            "bounded_search_inconclusive",
            "decomposition_required",
            "manual_modeling_required",
            "not_finitely_refutable",
            "source_conflict_requires_review",
            "statement_recovery_required",
        }

        def modeling_priority(result: dict[str, Any]) -> tuple[int, int, str]:
            status = str(result["status"])
            claim_kind = str(result["classification"]["claim_kind"])
            domain = str(result["domain"])
            score = {
                "source_conflict_requires_review": 5,
                "statement_recovery_required": 6,
                "bounded_domain_scan_completed": 10,
                "universal_claim": 20,
                "equivalence_claim": 25,
                "mixed_quantifiers": 30,
                "unclassified_question": 45,
                "classification_or_optimization": 50,
                "existence_claim": 60,
            }.get(status, {
                "universal_claim": 20,
                "equivalence_claim": 25,
                "mixed_quantifiers": 30,
                "unclassified_question": 45,
                "classification_or_optimization": 50,
                "existence_claim": 60,
            }.get(claim_kind, 50))
            if domain in {"number_theory", "graph_theory", "combinatorics", "computer_science"}:
                score -= 3
            try:
                difficulty = int(result.get("difficulty_level") or 9)
            except (TypeError, ValueError):
                difficulty = 9
            return score, difficulty, str(result["problem_id"])

        modeling_results = sorted(
            (result for result in results if result["status"] in incomplete_statuses),
            key=modeling_priority,
        )
        modeling_queue = [
            {
                "priority": index,
                "problem_id": result["problem_id"],
                "source_id": result["source_id"],
                "title": result["title"],
                "domain": result["domain"],
                "difficulty_level": result.get("difficulty_level"),
                "status": result["status"],
                "claim_kind": result["classification"]["claim_kind"],
                "falsifiability": result["classification"]["falsifiability"],
                "target_subclaims": result["classification"]["candidate_universal_subclaims"],
                "witness_contract": result["witness_contract"],
                "limitations": result.get("limitations", []),
                "source_url": result["source_url"],
            }
            for index, result in enumerate(modeling_results, start=1)
        ]
        _write_jsonl(output_dir / COUNTEREXAMPLE_MODELING_QUEUE_FILE, modeling_queue)
        status_counts = Counter(str(result["status"]) for result in results)
        claim_counts = Counter(
            str(result["classification"]["claim_kind"])
            for result in results
        )
        executor_counts = Counter(
            str((result.get("search_execution") or {}).get("executor_id"))
            for result in results
            if (result.get("search_execution") or {}).get("executor_id")
        )
        campaign = {
            "schema_version": COUNTEREXAMPLE_CAMPAIGN_SCHEMA_VERSION,
            "status": "succeeded",
            "generated_at": utc_now_iso(),
            "bank": str(bank_path),
            "bank_sha256": _sha256_file(bank_path),
            "output_dir": str(output_dir),
            "budget": budget,
            "search_config_fingerprint": search_config_fingerprint,
            "engine_version": COUNTEREXAMPLE_ENGINE_VERSION,
            "resume": resume,
            "counts": {
                "input_problems": len(problems),
                "result_records": len(results),
                "reused_results": reused,
                "executed_builtin_searches": sum(executor_counts.values()),
                "candidate_counterexamples": len(candidates),
                "modeling_queue": len(modeling_queue),
                "statuses": dict(sorted(status_counts.items())),
                "claim_kinds": dict(sorted(claim_counts.items())),
                "executors": dict(sorted(executor_counts.items())),
            },
            "artifacts": {
                "results": str(results_path),
                "candidate_counterexamples": str(output_dir / COUNTEREXAMPLE_CANDIDATES_FILE),
                "modeling_queue": str(output_dir / COUNTEREXAMPLE_MODELING_QUEUE_FILE),
                "report": str(output_dir / COUNTEREXAMPLE_REPORT_FILE),
            },
            "checksums_sha256": {
                "results": _sha256_file(results_path),
                "candidate_counterexamples": _sha256_file(
                    output_dir / COUNTEREXAMPLE_CANDIDATES_FILE
                ),
                "modeling_queue": _sha256_file(
                    output_dir / COUNTEREXAMPLE_MODELING_QUEUE_FILE
                ),
            },
            "interpretation": [
                "candidate_counterexample means a deterministic bounded checker found a witness candidate; it is not yet a published refutation.",
                "bounded_search_no_counterexample means only that the recorded finite range was exhausted.",
                "manual_modeling_required means the source statement was classified and assigned a witness contract but no sound executable predicate is registered.",
            ],
        }
        _write_json(output_dir / COUNTEREXAMPLE_CAMPAIGN_FILE, campaign)
        self._write_report(
            output_dir / COUNTEREXAMPLE_REPORT_FILE,
            campaign,
            results,
            candidates,
        )
        return campaign

    @staticmethod
    def _write_report(
        path: Path,
        campaign: dict[str, Any],
        results: list[dict[str, Any]],
        candidates: list[dict[str, Any]],
    ) -> None:
        counts = campaign["counts"]
        lines = [
            "# UnsolvedMath Counterexample Campaign",
            "",
            f"Generated: {campaign['generated_at']}",
            "",
            "## Scope",
            "",
            f"- Input problems: {counts['input_problems']}",
            f"- Result records: {counts['result_records']}",
            f"- Executed deterministic templates: {counts['executed_builtin_searches']}",
            f"- Candidate counterexamples: {counts['candidate_counterexamples']}",
            f"- Queued for statement-specific modeling: {counts['modeling_queue']}",
            "",
            "## Status Counts",
            "",
        ]
        lines.extend(f"- `{status}`: {count}" for status, count in counts["statuses"].items())
        executed = [
            result
            for result in results
            if (result.get("search_execution") or {}).get("executor_id")
        ]
        lines.extend(
            [
                "",
                "## Executed Searches",
                "",
                "| Source ID | Problem | Executor | Checked | Outcome | Bounds |",
                "| --- | --- | --- | ---: | --- | --- |",
            ]
        )
        lines.extend(
            (
                f"| `{result['source_id']}` | {result['title'].replace('|', '/')} | "
                f"`{result['search_execution']['executor_id']}` | "
                f"{result['search_execution']['checked_cases']} | "
                f"`{result['search_execution']['outcome']}` | "
                f"`{json.dumps(result['search_execution']['bounds'], sort_keys=True)}` |"
            )
            for result in executed
        )
        source_conflicts = [
            result
            for result in results
            if result["status"]
            in {"source_conflict_requires_review", "statement_recovery_required"}
        ]
        lines.extend(
            [
                "",
                "## Source Conflicts",
                "",
                (
                    f"{len(source_conflicts)} records have a missing or ambiguous detail statement because "
                    "the browse index reuses a source id for different titles. They are blocked until the "
                    "intended source statement is reconciled."
                ),
                "",
            ]
        )
        lines.extend(
            f"- `{result['source_id']}`: {result['title']}"
            for result in source_conflicts
        )
        lines.extend(
            [
                "",
                "## Verification Boundary",
                "",
                "A bounded negative search is not a proof of the conjecture. A candidate witness is not a "
                "refutation until the natural-language statement is modeled faithfully and an independent "
                "verifier reproduces every premise and the failed conclusion.",
                "",
                "## Candidates",
                "",
            ]
        )
        if candidates:
            lines.extend(
                f"- `{candidate['problem_id']}`: {candidate['title']}"
                for candidate in candidates
            )
        else:
            lines.append("- None in this bounded pass.")
        _atomic_write_text(path, "\n".join(lines) + "\n")


def run_counterexample_campaign(
    *,
    bank_path: Path,
    output_dir: Path,
    resume: bool = True,
    max_problems: int | None = None,
    **bounds: int,
) -> dict[str, Any]:
    return CounterexampleCampaignRunner().run(
        bank_path=bank_path,
        output_dir=output_dir,
        resume=resume,
        max_problems=max_problems,
        **bounds,
    )


__all__ = [
    "COUNTEREXAMPLE_CAMPAIGN_FILE",
    "COUNTEREXAMPLE_CAMPAIGN_SCHEMA_VERSION",
    "COUNTEREXAMPLE_CANDIDATES_FILE",
    "COUNTEREXAMPLE_ENGINE_VERSION",
    "COUNTEREXAMPLE_MODELING_QUEUE_FILE",
    "COUNTEREXAMPLE_REPORT_FILE",
    "COUNTEREXAMPLE_RESULTS_FILE",
    "COUNTEREXAMPLE_RESULT_SCHEMA_VERSION",
    "CounterexampleCampaignRunner",
    "classify_claim",
    "run_builtin_counterexample_search",
    "run_counterexample_campaign",
]
