from __future__ import annotations

import itertools
import os
import platform
import random
import signal
import subprocess
import threading
import time
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping


NAUTY_BIN = Path(
    "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-geng"
)
NAUTY_PLANARG = NAUTY_BIN.with_name("nauty-planarg")
NAUTY_LABELG = NAUTY_BIN.with_name("nauty-labelg")
NAUTY_LD = ":".join(
    (
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib",
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib/x86_64-linux-gnu",
    )
)
EXECUTOR_ID = "amra.second_batch_graphs"
EXECUTOR_VERSION = "v2"


class _PredicateTimeout(RuntimeError):
    pass


_PREDICATE_DEADLINE: ContextVar[float | None] = ContextVar(
    "second_batch_graph_predicate_deadline", default=None
)


def _check_predicate_deadline() -> None:
    deadline = _PREDICATE_DEADLINE.get()
    if deadline is not None and time.monotonic() >= deadline:
        # Do not let an expired budget poison later predicates if SIGALRM
        # interrupts the context manager while it is restoring its state.
        _PREDICATE_DEADLINE.set(None)
        raise _PredicateTimeout


@contextmanager
def _predicate_budget(deadline: float) -> Iterable[None]:
    if time.monotonic() >= deadline:
        raise _PredicateTimeout
    token = _PREDICATE_DEADLINE.set(deadline)
    use_signal = (
        threading.current_thread() is threading.main_thread()
        and hasattr(signal, "setitimer")
    )
    previous_handler: Any = None
    previous_timer = (0.0, 0.0)
    signal_installed = False
    started = time.monotonic()
    try:
        if use_signal:
            previous_handler = signal.getsignal(signal.SIGALRM)
            previous_timer = signal.getitimer(signal.ITIMER_REAL)

            def expire(_signum: int, _frame: Any) -> None:
                _PREDICATE_DEADLINE.set(None)
                raise _PredicateTimeout

            signal.signal(signal.SIGALRM, expire)
            signal_installed = True
            signal.setitimer(
                signal.ITIMER_REAL,
                max(0.000_001, deadline - time.monotonic()),
            )
        yield
    finally:
        try:
            if signal_installed:
                signal.setitimer(signal.ITIMER_REAL, 0)
        finally:
            try:
                if signal_installed:
                    signal.signal(signal.SIGALRM, previous_handler)
                    remaining, interval = previous_timer
                    if remaining > 0:
                        elapsed = time.monotonic() - started
                        signal.setitimer(
                            signal.ITIMER_REAL,
                            max(0.000_001, remaining - elapsed),
                            interval,
                        )
            finally:
                _PREDICATE_DEADLINE.reset(token)


@dataclass(frozen=True)
class Graph:
    n: int
    mask: int
    g6: str = ""

    @property
    def edges(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            edge
            for bit, edge in enumerate(_edge_pairs(self.n))
            if self.mask & (1 << bit)
        )

    @property
    def adjacency(self) -> tuple[int, ...]:
        rows = [0] * self.n
        for left, right in self.edges:
            rows[left] |= 1 << right
            rows[right] |= 1 << left
        return tuple(rows)

    def certificate(self) -> dict[str, Any]:
        return {
            "vertex_count": self.n,
            "edge_mask": self.mask,
            "edges": [list(edge) for edge in self.edges],
            "adjacency_rows": list(self.adjacency),
            **({"graph6": self.g6} if self.g6 else {}),
        }


def _spec(
    source_id: str,
    title: str,
    premise: str,
    conclusion: str,
    kind: str,
    *,
    max_vertices: int = 6,
    parameters: Mapping[str, Any] | None = None,
    deep_parameters: Mapping[str, Any] | None = None,
    targeted: bool = True,
    deterministic_deep: bool = False,
    deep_launches: int | None = None,
    supported_max_vertices: int | None = None,
    deep_max_vertices: int | None = None,
    claim_scope: str = "full_claim",
    scope_limitation: str = (
        "The full finite claim semantics are checked, subject to the configured "
        "graph-order and case bounds."
    ),
    source_statement: str | None = None,
    deep_search_role: str | None = None,
    frontier_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    problem_id = f"unsolvedmath-{source_id.lower()}"
    supported = supported_max_vertices or max_vertices + 2
    screen_bounds = {
        "max_vertices": max_vertices,
        "max_cases": 10_000,
        **dict(parameters or {}),
    }
    strategies = ["exact-small"]
    if targeted:
        strategies.append("targeted")
    elif deterministic_deep:
        strategies.append("deep-exact")
    spec = {
        "problem_id": problem_id,
        "source_id": source_id,
        "title": title,
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "kind": kind,
        "strategies": strategies,
        "default_bounds": screen_bounds,
        "screen_bounds": screen_bounds,
        "supports_deep": targeted or deterministic_deep,
        "deep_search_role": (
            deep_search_role
            or (
                "complete_nonisomorphic_graph_enumeration"
                if deterministic_deep
                else "seeded_stratified_adversarial_graph_search"
            )
        ),
        "frontier_provenance": {
            "screen_max_vertices": max_vertices,
            "deep_max_vertices": min(
                deep_max_vertices or max_vertices + 2, supported
            ),
            **dict(frontier_provenance or {}),
        },
        "deep_bounds": {
            **screen_bounds,
            "max_vertices": min(
                deep_max_vertices or max_vertices + 2, supported
            ),
            "max_cases": 100_000,
            **dict(deep_parameters or {}),
        },
        "launches": (
            int(deep_launches)
            if deep_launches is not None
            else (3 if targeted else 1)
        ),
        "supported_max_vertices": supported,
        "claim_scope": claim_scope,
        "scope_limitation": scope_limitation,
        "model_contract": {
            "objects": "finite simple graphs, with any auxiliary finite data stated below",
            "premise": premise,
            "conclusion": conclusion,
            "counterexample": f"{premise} and NOT ({conclusion})",
            "acceptance": (
                "The finite premise and failed conclusion are recomputed from the "
                "serialized adjacency certificate by a same-executor replay. This "
                "is a consistency check, not independent verification."
            ),
            "limitations": (
                "No candidate in a finite corpus is not a proof of the unbounded claim."
            ),
        },
    }
    if deterministic_deep:
        spec["deep_strategies"] = ["deep-exact"]
        spec["deep_launches"] = 1
    elif deep_launches is not None:
        spec["deep_launches"] = int(deep_launches)
    if source_statement:
        spec["source_statement"] = source_statement
        spec["model_contract"]["source_statement"] = source_statement
    return spec


_SPECS = (
    _spec(
        "OPG-127",
        "4-flow conjecture",
        "G is bridgeless and has no Petersen minor; the screen restricts |V(G)|<10, where the minor exclusion is automatic",
        "G has a nowhere-zero 4-flow",
        "flow4",
        max_vertices=8,
        supported_max_vertices=9,
        claim_scope="restricted_family",
        scope_limitation=(
            "Only graphs with fewer than ten vertices are supported, where Petersen-"
            "minor exclusion follows automatically from graph order."
        ),
    ),
    _spec(
        "OPG-128",
        "3-flow conjecture",
        "G is 4-edge-connected",
        "G has a nowhere-zero 3-flow",
        "flow3",
        max_vertices=7,
    ),
    _spec(
        "OPG-412",
        "Mapping planar graphs to odd cycles",
        "G is planar and has girth at least 4k for one of k in {2,3,4,5}",
        "G has a graph homomorphism to the cycle C_(2k+1)",
        "planar_odd_cycle_hom",
        max_vertices=7,
        parameters={"k_values": [2, 3, 4, 5]},
        deep_parameters={"k_values": [2, 3, 4, 5]},
        supported_max_vertices=40,
        deep_max_vertices=40,
        deep_launches=1,
        claim_scope="restricted_family",
        scope_limitation=(
            "The finite search tests k=2,3,4,5. The already-settled k=1 case is "
            "deliberately excluded; a witness for any tested k refutes the full claim."
        ),
        source_statement=(
            "Every planar graph of girth at least 4k has a homomorphism to "
            "C_(2k+1)."
        ),
        deep_search_role="multi_k_unknown_band_planar_core_subdivision_search",
        frontier_provenance={
            "tested_k_values": [2, 3, 4, 5],
            "excluded_settled_k_values": [1],
            "positive_odd_girth_threshold": "6k+1",
            "target_odd_girth_band": ["4k+1", "6k-1"],
            "deep_structural_corpus_size_at_order_40": 2_584,
            "deep_core_families": [
                "three-path theta",
                "four-path theta",
                "K4 subdivision",
                "triangular-prism subdivision",
                "cube subdivision",
                "octahedral subdivision",
                "wheel subdivisions W4,W5,W6",
            ],
            "derived_search_lower_bound": {
                "target_minimum_order": "6k",
                "derivation": (
                    "A nonbipartite theta core with all cycles of length at "
                    "least 4k needs three paths totaling at least 6k+1 edges, "
                    "hence at least 6k vertices."
                ),
            },
            "source": "arXiv:2402.02689",
        },
    ),
    _spec(
        "OPG-143",
        "Petersen coloring conjecture",
        "G is cubic and bridgeless",
        "the edges of G map to Petersen edges and every incident triple maps to an incident Petersen triple",
        "petersen_coloring",
        max_vertices=10,
    ),
    _spec(
        "OPG-154",
        "Jorgensen's Conjecture",
        "G is 6-connected and has no K6 minor",
        "deleting some vertex makes G planar",
        "jorgensen",
        max_vertices=10,
        supported_max_vertices=13,
        deep_max_vertices=13,
    ),
    _spec(
        "OPG-161",
        "Hamiltonian paths and cycles in vertex transitive graphs",
        "G is connected and vertex-transitive",
        "G has a Hamiltonian path",
        "vertex_transitive_hamiltonian",
        max_vertices=10,
    ),
    _spec(
        "OPG-171",
        "Strong colorability",
        "G is a finite graph and q=2 Delta(G)",
        "for every partition into blocks of size at most q, a proper q-coloring is injective on each block",
        "strong_colorability",
        max_vertices=7,
    ),
    _spec(
        "OPG-1757",
        "Negative association in uniform forests",
        "G is a finite simple graph and e,f are distinct edges of G",
        "#F_ef * #F <= #F_e * #F_f for the uniform family F of all forests of G",
        "uniform_forest_negative_association",
        max_vertices=5,
        supported_max_vertices=9,
        deep_max_vertices=9,
        source_statement=(
            "Let G be a finite graph, let e,f in E(G), and let F be the edge set "
            "of a forest chosen uniformly at random from all forests of G. Then "
            "P(e in F | f in F) <= P(e in F)."
        ),
        scope_limitation=(
            "The edge pair is required to be distinct, as in pairwise negative "
            "association; graphs with fewer than two edges are vacuous cases."
        ),
        deep_search_role="dense_nine_vertex_frontier_sampling",
        frontier_provenance={
            "known_verified_edge_ceiling_at_nine": 18,
            "deep_edge_range_at_nine": [19, 22],
            "source": "arXiv:math/0302185",
        },
    ),
    _spec(
        "OPG-335",
        "Reed's omega, delta, and chi conjecture",
        "G is a finite simple graph",
        "chi(G) <= ceil((Delta(G)+1+omega(G))/2)",
        "reed",
        max_vertices=8,
    ),
    _spec(
        "OPG-36907",
        "Bounding the chromatic number of triangle-free graphs with fixed maximum degree",
        "G is triangle-free",
        "chi(G) <= ceil(Delta(G)/2)+2",
        "triangle_free_chromatic",
        max_vertices=9,
    ),
    _spec(
        "OPG-37038",
        "Domination in cubic graphs",
        "G is 3-connected and cubic",
        "the domination number is at most ceil(|V(G)|/3)",
        "cubic_domination",
        max_vertices=12,
    ),
    _spec(
        "OPG-37182",
        "Odd cycles and low oddness",
        "G is connected, bridgeless, cubic, and every cycle in every 2-factor is odd",
        "the minimum number of odd cycles in a 2-factor is at most two",
        "oddness",
        max_vertices=12,
        claim_scope="restricted_family",
        scope_limitation=(
            "Connectedness is explicit in this model to exclude trivial disjoint "
            "unions and capture the intended oddness conjecture."
        ),
    ),
    _spec(
        "OPG-37379",
        "Forcing a $K_6$-minor",
        "G has minimum degree at least seven, or G is 7-connected",
        "G has a K6 minor",
        "forcing_k6_minor",
        max_vertices=10,
    ),
    _spec(
        "OPG-385",
        "Barnette's Conjecture",
        "G is 3-connected, cubic, planar, and bipartite",
        "G has a Hamiltonian cycle",
        "barnette",
        max_vertices=12,
    ),
    _spec(
        "OPG-638",
        "Jones' conjecture",
        "G is a finite simple planar graph",
        "cc(G) <= 2 cp(G), where cp is maximum vertex-disjoint cycle packing and cc is minimum feedback vertex set",
        "planar_cycle_packing",
        max_vertices=6,
        supported_max_vertices=9,
        deep_max_vertices=9,
        deep_launches=1,
        deep_search_role="complete_nonisomorphic_planar_enumeration",
        frontier_provenance={
            "deep_planar_graph_count_through_order_nine": 87_834,
            "enumeration": "all nonisomorphic simple planar graphs through order 9",
        },
        source_statement=(
            "For every planar graph G, cc(G) <= 2 cp(G), where cp(G) is the "
            "maximum number of vertex-disjoint cycles and cc(G) is the minimum "
            "size of a vertex set whose deletion makes G acyclic."
        ),
    ),
    _spec(
        "OPG-434",
        "Weak pentagon problem",
        "G is cubic and triangle-free",
        "G has a map from its edges to five colors for which each color complement is bipartite; properness is not imposed",
        "weak_pentagon",
        max_vertices=10,
        claim_scope="explicit_subclaim",
        scope_limitation=(
            "The local source says only 'color the edges ... by five colors' and "
            "does not state properness; this model uses an arbitrary edge-to-color map."
        ),
    ),
    _spec(
        "OPG-46475",
        "Strong edge colouring conjecture",
        "G is a finite simple graph",
        "the strong chromatic index obeys the stated parity-dependent bound in Delta",
        "strong_edge_coloring",
        max_vertices=8,
    ),
    _spec(
        "OPG-46583",
        "Decomposing a connected graph into paths.",
        "G is simple and connected",
        "E(G) partitions into at most floor((n+1)/2) nonempty simple paths",
        "path_decomposition",
        max_vertices=7,
    ),
    _spec(
        "OPG-46584",
        "Decomposing an eulerian graph into cycles.",
        "G is simple, connected, and every degree is even",
        "E(G) partitions into at most floor((n-1)/2) simple cycles",
        "cycle_decomposition",
        max_vertices=7,
    ),
    _spec(
        "OPG-46613",
        "Partition of a cubic 3-connected graphs into paths of length 2.",
        "G is cubic, 3-connected, and |V(G)| is divisible by 3",
        "V(G) partitions into three-vertex paths",
        "p3_partition",
        max_vertices=12,
    ),
    _spec(
        "OPG-480",
        "r-regular graphs are not uniquely hamiltonian.",
        "G is r-regular for r>2",
        "G does not have exactly one undirected Hamiltonian cycle",
        "regular_hamiltonian",
        max_vertices=10,
    ),
    _spec(
        "OPG-543",
        "The intersection of two perfect matchings",
        "G is bridgeless and cubic",
        "two perfect matchings have an intersection containing no odd edge cut",
        "matching_intersection",
        max_vertices=12,
    ),
    _spec(
        "OPG-56230",
        "2-colouring a graph without a monochromatic maximum clique",
        "G has at least one edge and has no induced odd cycle of length at least five",
        "G has a two-vertex-coloring with no monochromatic maximum clique",
        "max_clique_two_color",
        max_vertices=9,
        scope_limitation=(
            "The source's 'non-empty' condition is interpreted as having at least "
            "one edge, excluding the trivial one-vertex obstruction."
        ),
    ),
    _spec(
        "OPG-60001",
        "Cycles in Graphs of Large Chromatic Number",
        "chi(G)>k for the bounded integer k",
        "G has at least ceil((k+1)(k-1)!/2) simple cycles whose length is divisible by k",
        "modular_cycles",
        max_vertices=9,
        parameters={"k": 3},
        claim_scope="restricted_family",
        scope_limitation="The bounded model fixes the conjecture parameter to k=3.",
    ),
    _spec(
        "OPG-60027",
        "3-Decomposition Conjecture",
        "G is connected and cubic",
        "E(G) partitions into a spanning tree, a vertex-disjoint cycle family, and a matching",
        "three_decomposition",
        max_vertices=12,
    ),
    _spec(
        "OPG-60029",
        "Cycle Double Covers Containing Predefined 2-Regular Subgraphs",
        "G is 2-connected and cubic, S is 2-regular, and G-E(S) is connected",
        "G has a cycle double cover containing every cycle of S",
        "prescribed_cycle_double_cover",
        max_vertices=10,
    ),
    _spec(
        "OPG-60046",
        "3-Edge-Coloring Conjecture",
        "G is connected, cubic, has more than two vertices, and is 3-edge-colorable",
        "for some edge e, suppressing the two degree-2 vertices of G-e yields a 3-edge-colorable cubic multigraph",
        "edge_color_after_deletion",
        max_vertices=10,
    ),
    _spec(
        "OPG-60055",
        "Chromatic number of $\\frac{3}{3}$-power of graph",
        "Delta(G)>=2",
        "chi((G^(1/3))^3) <= 2 Delta(G)+1",
        "fractional_power",
        max_vertices=7,
    ),
    _spec(
        "OPG-804",
        "Edge Reconstruction Conjecture",
        "G and H are nonisomorphic simple graphs with at least four edges",
        "their multisets of edge-deleted unlabeled subgraphs differ",
        "edge_reconstruction",
        max_vertices=7,
        targeted=False,
        deterministic_deep=True,
    ),
    _spec(
        "OPG-815",
        "Total Colouring Conjecture",
        "G is a finite simple graph",
        "the total chromatic number is at most Delta(G)+2",
        "total_coloring",
        max_vertices=8,
    ),
    _spec(
        "OPG-60039",
        "Sidorenko's Conjecture",
        "H is a finite simple bipartite graph and G is a finite simple graph with at least one vertex",
        "hom(H,G) * |V(G)|^(2|E(H)|) >= (2|E(G)|)^|E(H)| * |V(G)|^|V(H)|",
        "sidorenko",
        max_vertices=4,
        parameters={"max_h_vertices": 4, "max_g_vertices": 4},
        deep_parameters={"max_h_vertices": 12, "max_g_vertices": 6},
        supported_max_vertices=8,
        deep_max_vertices=6,
        source_statement=(
            "For every bipartite graph H and graph G, hom(H,G) is at least "
            "(2|E(G)|/|V(G)|^2)^|E(H)| |V(G)|^|V(H)|."
        ),
        scope_limitation=(
            "The target G must have at least one vertex so the displayed density "
            "is defined; H may have zero vertices, zero edges, and isolated vertices."
        ),
        deep_search_role="known_family_filtered_bipartite_source_sampling",
        frontier_provenance={
            "filtered_known_positive_source_families": [
                "forest",
                "complete_bipartite",
                "even_cycle",
                "hypercube",
                "universal_vertex_to_opposite_side",
            ],
            "deep_source_order": 12,
            "deep_target_order": 6,
            "universal_vertex_family_source": "arXiv:1209.0184",
        },
    ),
    _spec(
        "OPG-729",
        "Seagull problem",
        "G has no independent set of size three",
        "G has a complete minor of order at least ceil(|V(G)|/2)",
        "seagull_minor",
        max_vertices=6,
        supported_max_vertices=16,
        deep_max_vertices=16,
        deep_launches=1,
        source_statement=(
            "Every n-vertex graph with no independent set of size three has "
            "a complete graph on at least n/2 vertices as a minor."
        ),
        deep_search_role="triangle_free_complement_ramsey_frontier_search",
        frontier_provenance={
            "known_positive_order_ceiling": 12,
            "known_positive_derivation": (
                "alpha(G)<=2 implies chi(G)>=ceil(n/2); for n<=12 the target "
                "is at most six, and Hadwiger's conjecture is proved through t=6."
            ),
            "deep_order_range": [13, 16],
            "deep_canonical_corpus_size": 25_706,
            "deep_canonical_strata": {
                "n13_edges20_to22_min3_max4": 16_988,
                "n14_edges21_to22_min3_max4": 5_072,
                "n15_edges23_min3_max4": 2_854,
                "n16_cubic": 792,
            },
            "complement_model": (
                "canonical connected triangle-free near-regular complements, "
                "stratified by order and edge count"
            ),
            "sources": [
                "arXiv:2206.00186",
                "doi:10.1007/BF01202354",
            ],
        },
    ),
)

SECOND_BATCH_GRAPH_SPECS: tuple[dict[str, Any], ...] = _SPECS
_SPEC_BY_ID: dict[str, dict[str, Any]] = {
    spec["problem_id"]: spec for spec in SECOND_BATCH_GRAPH_SPECS
}


UNREGISTERED_SECOND_BATCH_GRAPH_IDS: tuple[str, ...] = tuple(
    f"unsolvedmath-{source.lower()}"
    for source in (
        "OPG-59911",
        "OPG-130",
        "OPG-165",
        "OPG-182",
        "OPG-48232",
        "OPG-49795",
        "OPG-611",
        "OPG-47282",
        "OPG-46443",
        "OPG-47028",
        "OPG-46460",
        "OPG-46359",
        "OPG-1793",
        "OPG-37316",
        "OPG-46167",
        "OPG-46279",
        "OPG-46533",
        "OPG-46606",
        "OPG-47651",
        "OPG-48264",
        "OPG-485",
        "OPG-49573",
        "OPG-52197",
        "OPG-550",
        "OPG-59994",
        "OPG-59997",
        "OPG-636",
        "OPG-135",
        "OPG-138",
        "OPG-348",
        "OPG-401",
        "OPG-2226",
    )
)


@lru_cache(maxsize=None)
def _edge_pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for right in range(1, n) for left in range(right))


@lru_cache(maxsize=None)
def _edge_indexes(n: int) -> dict[tuple[int, int], int]:
    return {edge: bit for bit, edge in enumerate(_edge_pairs(n))}


def _mask_from_edges(n: int, edges: Iterable[tuple[int, int]]) -> int:
    indexes = _edge_indexes(n)
    mask = 0
    for left, right in edges:
        mask |= 1 << indexes[(min(left, right), max(left, right))]
    return mask


def _decode_graph6(value: str) -> Graph:
    value = value.strip()
    if value.startswith(">>graph6<<"):
        value = value[10:]
    if not value or ord(value[0]) > 126:
        raise ValueError("unsupported graph6 record")
    n = ord(value[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("only compact graph6 orders up to 62 are supported")
    bits: list[int] = []
    for char in value[1:]:
        number = ord(char) - 63
        bits.extend((number >> shift) & 1 for shift in range(5, -1, -1))
    mask = 0
    for bit, _ in enumerate(_edge_pairs(n)):
        if bit < len(bits) and bits[bit]:
            mask |= 1 << bit
    return Graph(n=n, mask=mask, g6=value)


def _encode_graph6(graph: Graph) -> str:
    if graph.n > 62:
        raise ValueError("compact graph6 encoder supports at most 62 vertices")
    bits = [
        int(bool(graph.mask & (1 << bit)))
        for bit in range(len(_edge_pairs(graph.n)))
    ]
    while len(bits) % 6:
        bits.append(0)
    encoded = [chr(graph.n + 63)]
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        encoded.append(chr(value + 63))
    return "".join(encoded)


@lru_cache(maxsize=None)
def _is_planar(graph: Graph) -> bool:
    if not NAUTY_PLANARG.is_file():
        raise FileNotFoundError(str(NAUTY_PLANARG))
    deadline = _PREDICATE_DEADLINE.get()
    timeout = None if deadline is None else max(0.000_001, deadline - time.monotonic())
    try:
        completed = subprocess.run(
            [str(NAUTY_PLANARG), "-q"],
            input=_encode_graph6(graph) + "\n",
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        raise _PredicateTimeout from error
    return bool(completed.stdout.strip())


@lru_cache(maxsize=None)
def _canonical_graph6(graph: Graph) -> str:
    if not NAUTY_LABELG.is_file():
        return f"{graph.n}:{_canonical_mask(graph)}"
    deadline = _PREDICATE_DEADLINE.get()
    timeout = (
        None
        if deadline is None
        else max(0.000_001, deadline - time.monotonic())
    )
    try:
        completed = subprocess.run(
            [str(NAUTY_LABELG), "-q"],
            input=_encode_graph6(graph) + "\n",
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        raise _PredicateTimeout from error
    return completed.stdout.strip()


@lru_cache(maxsize=None)
def _planar_unlabeled_corpus(max_vertices: int) -> tuple[Graph, ...]:
    corpus: list[Graph] = []
    for order in range(1, max_vertices + 1):
        generated = subprocess.run(
            [str(NAUTY_BIN), "-q", str(order)],
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
        )
        planar = subprocess.run(
            [str(NAUTY_PLANARG), "-q"],
            input=generated.stdout,
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
        )
        corpus.extend(
            _decode_graph6(line)
            for line in planar.stdout.splitlines()
            if line.strip()
        )
    return tuple(corpus)


def _delete_vertex(graph: Graph, deleted: int) -> Graph:
    remaining = [vertex for vertex in range(graph.n) if vertex != deleted]
    renumber = {vertex: index for index, vertex in enumerate(remaining)}
    edges = [
        (renumber[left], renumber[right])
        for left, right in graph.edges
        if deleted not in {left, right}
    ]
    return Graph(graph.n - 1, _mask_from_edges(graph.n - 1, edges))


def _nauty_env() -> dict[str, str]:
    env = dict(os.environ)
    env["LD_LIBRARY_PATH"] = ":".join(
        item for item in (NAUTY_LD, env.get("LD_LIBRARY_PATH", "")) if item
    )
    return env


def _iter_nauty_graphs(max_vertices: int) -> Iterable[Graph]:
    if not NAUTY_BIN.is_file():
        raise FileNotFoundError(str(NAUTY_BIN))
    for n in range(1, max_vertices + 1):
        process = subprocess.Popen(
            [str(NAUTY_BIN), "-q", str(n)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=_nauty_env(),
        )
        try:
            assert process.stdout is not None
            for line in process.stdout:
                if line.strip():
                    yield _decode_graph6(line)
            return_code = process.wait()
            if return_code:
                stderr = process.stderr.read() if process.stderr else ""
                raise RuntimeError(f"nauty-geng failed ({return_code}): {stderr}")
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def _relabel_graph(graph: Graph, permutation: list[int]) -> Graph:
    return Graph(
        graph.n,
        _mask_from_edges(
            graph.n,
            (
                (permutation[left], permutation[right])
                for left, right in graph.edges
            ),
        ),
    )


def _complete_graph(n: int) -> Graph:
    return Graph(n, (1 << len(_edge_pairs(n))) - 1)


def _cycle_graph(n: int) -> Graph:
    if n < 3:
        return Graph(n, 0)
    return Graph(
        n,
        _mask_from_edges(
            n, ((vertex, (vertex + 1) % n) for vertex in range(n))
        ),
    )


def _complement_graph(graph: Graph) -> Graph:
    full_mask = (1 << len(_edge_pairs(graph.n))) - 1
    return Graph(graph.n, full_mask ^ graph.mask)


def _complete_multipartite(part_sizes: list[int]) -> Graph:
    n = sum(part_sizes)
    parts: list[list[int]] = []
    start = 0
    for size in part_sizes:
        parts.append(list(range(start, start + size)))
        start += size
    return Graph(
        n,
        _mask_from_edges(
            n,
            (
                (left, right)
                for first, second in itertools.combinations(parts, 2)
                for left in first
                for right in second
            ),
        ),
    )


def _random_density_graph(n: int, probability: float, rng: random.Random) -> Graph:
    return Graph(
        n,
        _mask_from_edges(
            n,
            (edge for edge in _edge_pairs(n) if rng.random() < probability),
        ),
    )


def _random_bipartite_graph(n: int, rng: random.Random) -> Graph:
    order = list(range(n))
    rng.shuffle(order)
    cut = rng.randint(1, n - 1) if n > 1 else n
    probability = rng.choice((0.3, 0.5, 0.7, 0.9))
    return Graph(
        n,
        _mask_from_edges(
            n,
            (
                (left, right)
                for left in order[:cut]
                for right in order[cut:]
                if rng.random() < probability
            ),
        ),
    )


def _random_regular_graph(
    n: int, degree: int, rng: random.Random
) -> Graph | None:
    if degree < 0 or degree >= n or n * degree % 2:
        return None
    if degree == 0:
        return Graph(n, 0)
    if degree == n - 1:
        return _complete_graph(n)
    for _ in range(200):
        stubs = [vertex for vertex in range(n) for _ in range(degree)]
        rng.shuffle(stubs)
        edges: set[tuple[int, int]] = set()
        valid = True
        for offset in range(0, len(stubs), 2):
            left, right = stubs[offset : offset + 2]
            edge = (min(left, right), max(left, right))
            if left == right or edge in edges:
                valid = False
                break
            edges.add(edge)
        if valid:
            return Graph(n, _mask_from_edges(n, edges))
    return None


def _random_cubic_bipartite_graph(
    max_vertices: int, rng: random.Random
) -> Graph | None:
    possible = [n for n in range(6, max_vertices + 1, 2)]
    if not possible:
        return None
    n = rng.choice(possible)
    half = n // 2
    for _ in range(100):
        matchings: list[tuple[int, int]] = []
        used: set[tuple[int, int]] = set()
        valid = True
        for _color in range(3):
            targets = list(range(half, n))
            rng.shuffle(targets)
            matching = [(left, targets[left]) for left in range(half)]
            if any(edge in used for edge in matching):
                valid = False
                break
            used.update(matching)
            matchings.extend(matching)
        if valid:
            return Graph(n, _mask_from_edges(n, matchings))
    return None


def _random_eulerian_graph(n: int, rng: random.Random) -> Graph:
    if n < 3:
        return Graph(n, 0)
    base = _cycle_graph(n).mask
    for _ in range(rng.randint(1, max(1, n))):
        size = rng.randint(3, n)
        vertices = rng.sample(range(n), size)
        cycle = _mask_from_edges(
            n,
            (
                (vertices[index], vertices[(index + 1) % size])
                for index in range(size)
            ),
        )
        candidate = base ^ cycle
        if candidate and _connected(Graph(n, candidate)):
            base = candidate
    return Graph(n, base)


def _dense_high_connectivity_graph(n: int, rng: random.Random) -> Graph:
    graph = _complete_graph(n)
    removable = list(_edge_pairs(n))
    rng.shuffle(removable)
    maximum_removed_degree = max(0, min(2, n - 2))
    removed_degrees = [0] * n
    mask = graph.mask
    edge_indexes = {edge: bit for bit, edge in enumerate(_edge_pairs(n))}
    for edge in removable:
        left, right = edge
        if (
            removed_degrees[left] >= maximum_removed_degree
            or removed_degrees[right] >= maximum_removed_degree
            or rng.random() >= 0.35
        ):
            continue
        mask &= ~(1 << edge_indexes[edge])
        removed_degrees[left] += 1
        removed_degrees[right] += 1
    return Graph(n, mask)


def _petersen_graph() -> Graph:
    return Graph(
        10,
        _mask_from_edges(
            10,
            [(i, (i + 1) % 5) for i in range(5)]
            + [(i, i + 5) for i in range(5)]
            + [(5 + i, 5 + ((i + 2) % 5)) for i in range(5)],
        ),
    )


def _generalized_petersen_graph(order: int, step: int) -> Graph:
    if order < 3 or not 1 <= step < order / 2:
        raise ValueError("generalized Petersen parameters must give a simple cubic graph")
    edges = {
        (min(vertex, (vertex + 1) % order), max(vertex, (vertex + 1) % order))
        for vertex in range(order)
    }
    edges.update((vertex, order + vertex) for vertex in range(order))
    edges.update(
        (
            min(order + vertex, order + (vertex + step) % order),
            max(order + vertex, order + (vertex + step) % order),
        )
        for vertex in range(order)
    )
    return Graph(2 * order, _mask_from_edges(2 * order, edges))


def _prism_graph(cycle_order: int) -> Graph:
    n = 2 * cycle_order
    return Graph(
        n,
        _mask_from_edges(
            n,
            [
                (
                    layer * cycle_order + vertex,
                    layer * cycle_order + (vertex + 1) % cycle_order,
                )
                for layer in range(2)
                for vertex in range(cycle_order)
            ]
            + [(vertex, cycle_order + vertex) for vertex in range(cycle_order)],
        ),
    )


def _ladder_graph(column_count: int) -> Graph:
    n = 2 * column_count
    edges = [
        (row * column_count + column, row * column_count + column + 1)
        for row in range(2)
        for column in range(column_count - 1)
    ]
    edges.extend(
        (column, column_count + column)
        for column in range(column_count)
    )
    return Graph(n, _mask_from_edges(n, edges))


def _chorded_even_cycle(order: int) -> Graph:
    if order < 6 or order % 2:
        raise ValueError("chorded even cycle order must be even and at least six")
    cycle = _cycle_graph(order)
    chord = (0, 3)
    return Graph(
        order,
        cycle.mask | _mask_from_edges(order, [chord]),
    )


def _apex_icosahedron_graph() -> Graph:
    """The cone over the icosahedral graph: a 13-vertex Jorgensen premise witness."""
    apex = 0
    top = 1
    upper = list(range(2, 7))
    lower = list(range(7, 12))
    bottom = 12
    base_edges = (
        [(top, vertex) for vertex in upper]
        + [(bottom, vertex) for vertex in lower]
        + [
            (upper[index], upper[(index + 1) % 5])
            for index in range(5)
        ]
        + [
            (lower[index], lower[(index + 1) % 5])
            for index in range(5)
        ]
        + [
            (upper[index], lower[index])
            for index in range(5)
        ]
        + [
            (upper[index], lower[(index - 1) % 5])
            for index in range(5)
        ]
    )
    return Graph(
        13,
        _mask_from_edges(
            13,
            base_edges + [(apex, vertex) for vertex in range(1, 13)],
        ),
    )


def _rook_graph(order: int) -> Graph:
    n = order * order
    return Graph(
        n,
        _mask_from_edges(
            n,
            (
                (first, second)
                for first, second in _edge_pairs(n)
                if divmod(first, order)[0] == divmod(second, order)[0]
                or divmod(first, order)[1] == divmod(second, order)[1]
            ),
        ),
    )


def _strongly_regular_graph(max_vertices: int, rng: random.Random) -> Graph:
    choices: list[Graph] = []
    if max_vertices >= 5:
        choices.append(_cycle_graph(5))
    if max_vertices >= 10:
        choices.append(_petersen_graph())
    for order in (2, 3):
        if order * order <= max_vertices:
            choices.append(_rook_graph(order))
    for part_size in range(2, max_vertices + 1):
        for part_count in range(2, max_vertices // part_size + 1):
            choices.append(_complete_multipartite([part_size] * part_count))
    if not choices:
        return _complete_graph(max_vertices)
    graph = rng.choice(choices)
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


def _vertex_transitive_graph(max_vertices: int, rng: random.Random) -> Graph:
    choices = [_complete_graph(n) for n in range(1, max_vertices + 1)]
    choices.extend(_cycle_graph(n) for n in range(3, max_vertices + 1))
    if max_vertices >= 4:
        choices.extend(
            _complete_multipartite([part_size] * part_count)
            for part_size in range(2, max_vertices + 1)
            for part_count in range(2, max_vertices // part_size + 1)
        )
    if max_vertices >= 10:
        choices.append(_petersen_graph())
    graph = rng.choice(choices)
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


def _structured_graph(max_vertices: int, rng: random.Random) -> Graph:
    choices: list[Graph] = []
    for n in range(1, max_vertices + 1):
        choices.append(_complete_graph(n))
        if n >= 3:
            choices.append(_cycle_graph(n))
        for left in range(1, n):
            choices.append(_complete_multipartite([left, n - left]))
        if n >= 4 and n % 2 == 0:
            choices.append(_complete_multipartite([2] * (n // 2)))
    if max_vertices >= 10:
        choices.append(_petersen_graph())
    for order in (2, 3):
        if order * order <= max_vertices:
            choices.append(_rook_graph(order))
    graph = rng.choice(choices)
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


def _planar_cycle_family(max_vertices: int, rng: random.Random) -> Graph:
    choices: list[Graph] = []
    for order in range(3, max_vertices + 1):
        choices.append(_cycle_graph(order))
    for n in range(4, max_vertices + 1):
        choices.append(
            Graph(
                n,
                _mask_from_edges(
                    n,
                    [(0, vertex) for vertex in range(1, n)]
                    + [
                        (vertex, 1 + vertex % (n - 1))
                        for vertex in range(1, n)
                    ],
                ),
            )
        )
    for order in range(3, max_vertices // 2 + 1):
        choices.append(_prism_graph(order))
    if max_vertices >= 6:
        for first in range(3, max_vertices - 2):
            second = max_vertices - first
            if second < 3:
                continue
            choices.append(
                Graph(
                    max_vertices,
                    _mask_from_edges(
                        max_vertices,
                        list(_cycle_graph(first).edges)
                        + [
                            (left + first, right + first)
                            for left, right in _cycle_graph(second).edges
                        ],
                    ),
                )
            )
    if not choices:
        return Graph(max_vertices, 0)
    graph = rng.choice(choices)
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


def _theta_graph(path_lengths: Iterable[int]) -> Graph:
    lengths = tuple(int(length) for length in path_lengths)
    if len(lengths) < 3 or any(length < 2 for length in lengths):
        raise ValueError("a theta graph needs at least three paths of length two")
    edges: list[tuple[int, int]] = []
    next_vertex = 2
    for length in lengths:
        previous = 0
        for _ in range(length - 1):
            current = next_vertex
            next_vertex += 1
            edges.append((previous, current))
            previous = current
        edges.append((previous, 1))
    return Graph(next_vertex, _mask_from_edges(next_vertex, edges))


def _subdivide_graph(
    base: Graph, path_lengths: Iterable[int]
) -> Graph:
    lengths = tuple(int(length) for length in path_lengths)
    if len(lengths) != len(base.edges) or any(length < 1 for length in lengths):
        raise ValueError("one positive path length is required for every edge")
    edges: list[tuple[int, int]] = []
    next_vertex = base.n
    for (left, right), length in zip(base.edges, lengths):
        previous = left
        for _ in range(length - 1):
            current = next_vertex
            next_vertex += 1
            edges.append((previous, current))
            previous = current
        edges.append((previous, right))
    return Graph(next_vertex, _mask_from_edges(next_vertex, edges))


def _planar_odd_cycle_frontier_graph(
    max_vertices: int, index: int, rng: random.Random
) -> Graph:
    feasible_k = [k for k in (2, 3, 4, 5) if 6 * k <= max_vertices]
    if not feasible_k:
        return _cycle_graph(max_vertices)
    k = feasible_k[index % len(feasible_k)]
    family_index = (index // len(feasible_k)) % 4
    candidates: list[tuple[str, Callable[[], Graph]]] = []

    def theta_three() -> Graph:
        # Even, even, odd path lengths put the odd-girth in the unresolved band.
        lengths = [2 * k, 2 * k, 2 * k + 1]
        spare_pairs = max(0, (max_vertices - 6 * k) // 2)
        lengths[1] += 2 * rng.randint(0, spare_pairs)
        rng.shuffle(lengths)
        return _theta_graph(lengths)

    candidates.append(("theta3", theta_three))

    if 8 * k - 1 <= max_vertices:
        def theta_four() -> Graph:
            lengths = [2 * k, 2 * k, 2 * k, 2 * k + 1]
            spare_pairs = max(
                0, (max_vertices - (8 * k - 1)) // 2
            )
            for _ in range(rng.randint(0, spare_pairs)):
                lengths[rng.choice((1, 2))] += 2
            rng.shuffle(lengths)
            return _theta_graph(lengths)

        candidates.append(("theta4", theta_four))

    k4_length = (4 * k + 2) // 3
    k4_extra = int(k4_length % 2 == 0)
    k4_order = 4 + 6 * (k4_length - 1) + k4_extra
    if k4_order <= max_vertices:
        def subdivided_k4() -> Graph:
            base = _complete_graph(4)
            lengths = [k4_length] * len(base.edges)
            if k4_extra:
                lengths[rng.randrange(len(lengths))] += 1
            spare_pairs = max(0, (max_vertices - k4_order) // 2)
            for _ in range(rng.randint(0, spare_pairs)):
                lengths[rng.randrange(len(lengths))] += 2
            return _subdivide_graph(base, lengths)

        candidates.append(("subdivided_k4", subdivided_k4))

    cube_order = 8 + 12 * (k - 1) + 1
    if cube_order <= max_vertices:
        def subdivided_cube() -> Graph:
            base = _prism_graph(4)
            lengths = [k] * len(base.edges)
            lengths[rng.randrange(len(lengths))] += 1
            spare_pairs = max(0, (max_vertices - cube_order) // 2)
            for _ in range(rng.randint(0, spare_pairs)):
                lengths[rng.randrange(len(lengths))] += 2
            return _subdivide_graph(base, lengths)

        candidates.append(("subdivided_cube", subdivided_cube))

    _, construct = candidates[family_index % len(candidates)]
    graph = construct()
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


def _k4_subdivision_key(lengths: tuple[int, ...]) -> tuple[int, ...]:
    edges = _edge_pairs(4)
    by_edge = dict(zip(edges, lengths))
    representations = []
    for permutation in itertools.permutations(range(4)):
        transformed = {
            (
                min(permutation[left], permutation[right]),
                max(permutation[left], permutation[right]),
            ): by_edge[(left, right)]
            for left, right in edges
        }
        representations.append(tuple(transformed[edge] for edge in edges))
    return min(representations)


def _canonical_unique_graphs(graphs: Iterable[Graph]) -> tuple[Graph, ...]:
    materialized = list(graphs)
    if not materialized:
        return ()
    if NAUTY_LABELG.is_file():
        completed = subprocess.run(
            [str(NAUTY_LABELG), "-q"],
            input="\n".join(_encode_graph6(graph) for graph in materialized)
            + "\n",
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
        )
        labels = [
            line.strip()
            for line in completed.stdout.splitlines()
            if line.strip()
        ]
        if len(labels) != len(materialized):
            raise RuntimeError("nauty-labelg changed the graph record count")
    else:
        labels = [
            f"{graph.n}:{graph.mask}" for graph in materialized
        ]
    unique: list[Graph] = []
    seen: set[str] = set()
    for graph, label in zip(materialized, labels):
        if label not in seen:
            seen.add(label)
            unique.append(graph)
    return tuple(unique)


def _wheel_graph(rim_order: int) -> Graph:
    rim = _cycle_graph(rim_order)
    hub = rim_order
    return Graph(
        rim_order + 1,
        _mask_from_edges(
            rim_order + 1,
            list(rim.edges)
            + [(hub, vertex) for vertex in range(rim_order)],
        ),
    )


@lru_cache(maxsize=None)
def _odd_cycle_structural_corpus(max_vertices: int) -> tuple[Graph, ...]:
    graphs: list[Graph] = []
    seen_theta: set[tuple[int, tuple[int, ...]]] = set()
    for path_count in (3, 4):
        for k in (2, 3, 4, 5):
            for lengths in itertools.combinations_with_replacement(
                range(2 * k, max_vertices + 1), path_count
            ):
                order = sum(lengths) - path_count + 2
                if order > max_vertices or lengths[0] + lengths[1] < 4 * k:
                    continue
                odd_cycles = [
                    left + right
                    for left, right in itertools.combinations(lengths, 2)
                    if (left + right) % 2
                ]
                if not odd_cycles or min(odd_cycles) > 6 * k - 1:
                    continue
                key = (path_count, lengths)
                if key not in seen_theta:
                    seen_theta.add(key)
                    graphs.append(_theta_graph(lengths))

    k4_edges = _edge_pairs(4)
    seen_k4: set[tuple[int, ...]] = set()
    triangle_edge_sets = [
        tuple(
            (min(left, right), max(left, right))
            for left, right in itertools.combinations(vertices, 2)
        )
        for vertices in itertools.combinations(range(4), 3)
    ]
    four_cycle_edge_sets = [
        tuple(
            (
                min(cycle[index], cycle[(index + 1) % 4]),
                max(cycle[index], cycle[(index + 1) % 4]),
            )
            for index in range(4)
        )
        for cycle in (
            (0, 1, 2, 3),
            (0, 1, 3, 2),
            (0, 2, 1, 3),
        )
    ]
    for k in (2, 3, 4, 5):
        base_length = (4 * k + 2) // 3
        for increments in itertools.product(range(4), repeat=6):
            lengths = tuple(
                base_length + increment for increment in increments
            )
            if 4 + sum(length - 1 for length in lengths) > max_vertices:
                continue
            by_edge = dict(zip(k4_edges, lengths))
            cycle_lengths = [
                sum(by_edge[edge] for edge in cycle)
                for cycle in triangle_edge_sets + four_cycle_edge_sets
            ]
            if min(cycle_lengths) < 4 * k:
                continue
            odd_cycles = [length for length in cycle_lengths if length % 2]
            if not odd_cycles or min(odd_cycles) > 6 * k - 1:
                continue
            key = _k4_subdivision_key(lengths)
            if key in seen_k4:
                continue
            seen_k4.add(key)
            graphs.append(_subdivide_graph(_complete_graph(4), key))

    planar_cores = (
        _prism_graph(3),
        _prism_graph(4),
        _complete_multipartite([2, 2, 2]),
        _wheel_graph(4),
        _wheel_graph(5),
        _wheel_graph(6),
    )
    for core in planar_cores:
        core_edges = core.edges
        edge_index = {edge: index for index, edge in enumerate(core_edges)}
        core_cycles = [
            tuple(
                edge_index[
                    (
                        min(cycle[index], cycle[(index + 1) % len(cycle)]),
                        max(cycle[index], cycle[(index + 1) % len(cycle)]),
                    )
                ]
                for index in range(len(cycle))
            )
            for cycle in _cycles(core)
        ]
        core_girth = min(map(len, core_cycles))
        for k in (2, 3, 4, 5):
            base_length = (4 * k + core_girth - 1) // core_girth
            base_order = core.n + len(core_edges) * (base_length - 1)
            spare = max_vertices - base_order
            if spare < 0:
                continue
            for pattern in range(1 << len(core_edges)):
                if pattern.bit_count() > spare:
                    continue
                lengths = tuple(
                    base_length + int(bool(pattern & (1 << index)))
                    for index in range(len(core_edges))
                )
                cycle_lengths = [
                    sum(lengths[index] for index in cycle)
                    for cycle in core_cycles
                ]
                if min(cycle_lengths) < 4 * k:
                    continue
                odd_cycles = [
                    length for length in cycle_lengths if length % 2
                ]
                if not odd_cycles or min(odd_cycles) > 6 * k - 1:
                    continue
                graphs.append(_subdivide_graph(core, lengths))
    return _canonical_unique_graphs(graphs)


def _mycielski_graph(graph: Graph) -> Graph:
    n = graph.n
    apex = 2 * n
    edges = list(graph.edges)
    for left, right in graph.edges:
        edges.extend(((n + left, right), (n + right, left)))
    edges.extend((n + vertex, apex) for vertex in range(n))
    return Graph(2 * n + 1, _mask_from_edges(2 * n + 1, edges))


def _add_false_twin(graph: Graph, source: int) -> Graph:
    edges = list(graph.edges)
    edges.extend(
        (neighbor, graph.n)
        for neighbor in range(graph.n)
        if graph.adjacency[source] & (1 << neighbor)
    )
    return Graph(graph.n + 1, _mask_from_edges(graph.n + 1, edges))


def _cycle_five_blowup(n: int, rng: random.Random) -> Graph:
    sizes = [1] * 5
    for _ in range(n - 5):
        sizes[rng.randrange(5)] += 1
    parts: list[list[int]] = []
    start = 0
    for size in sizes:
        parts.append(list(range(start, start + size)))
        start += size
    edges = [
        (left, right)
        for index in range(5)
        for left in parts[index]
        for right in parts[(index + 1) % 5]
    ]
    return Graph(n, _mask_from_edges(n, edges))


def _random_maximal_triangle_free_graph(
    n: int, rng: random.Random, *, seeded_cycle: bool
) -> Graph:
    adjacency = [0] * n
    if seeded_cycle:
        for left, right in _cycle_graph(n).edges:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    pairs = list(_edge_pairs(n))
    rng.shuffle(pairs)
    for left, right in pairs:
        if adjacency[left] & (1 << right):
            continue
        if adjacency[left] & adjacency[right]:
            continue
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    edges = [
        (left, right)
        for left, right in _edge_pairs(n)
        if adjacency[left] & (1 << right)
    ]
    return Graph(n, _mask_from_edges(n, edges))


def _seagull_frontier_graph(
    max_vertices: int, index: int, rng: random.Random
) -> Graph:
    minimum = 13
    if max_vertices < minimum:
        return _complete_graph(max_vertices)
    n = minimum + index % (max_vertices - minimum + 1)
    family = (index // (max_vertices - minimum + 1)) % 4
    if family == 0:
        triangle_free = _cycle_five_blowup(n, rng)
    elif family == 1:
        triangle_free = _mycielski_graph(_cycle_graph(5))
        while triangle_free.n < n:
            triangle_free = _add_false_twin(
                triangle_free, rng.randrange(triangle_free.n)
            )
        if triangle_free.n > n:
            triangle_free = _random_maximal_triangle_free_graph(
                n, rng, seeded_cycle=False
            )
    else:
        triangle_free = _random_maximal_triangle_free_graph(
            n, rng, seeded_cycle=family == 3
        )
    graph = _complement_graph(triangle_free)
    permutation = list(range(graph.n))
    rng.shuffle(permutation)
    return _relabel_graph(graph, permutation)


@lru_cache(maxsize=None)
def _seagull_canonical_groups(
    max_vertices: int,
) -> tuple[tuple[Graph, ...], ...]:
    configurations = (
        (13, "20:22", 3, 4),
        (14, "21:22", 3, 4),
        (15, "23", 3, 4),
        (16, "24", 3, 3),
    )
    groups: list[tuple[Graph, ...]] = []
    for order, edge_range, minimum_degree, maximum_degree in configurations:
        if order > max_vertices:
            continue
        completed = subprocess.run(
            [
                str(NAUTY_BIN),
                "-q",
                "-t",
                "-c",
                f"-d{minimum_degree}",
                f"-D{maximum_degree}",
                str(order),
                edge_range,
            ],
            capture_output=True,
            text=True,
            env=_nauty_env(),
            check=True,
        )
        groups.append(
            tuple(
                _complement_graph(_decode_graph6(line))
                for line in completed.stdout.splitlines()
                if line.strip()
            )
        )
    return tuple(groups)


def _uniform_forest_frontier_graph(rng: random.Random) -> Graph:
    n = 9
    cycle_edges = set(_cycle_graph(n).edges)
    chords = [
        edge for edge in _edge_pairs(n) if edge not in cycle_edges
    ]
    rng.shuffle(chords)
    target_edges = rng.randint(19, 22)
    edges = cycle_edges | set(chords[: target_edges - len(cycle_edges)])
    return Graph(n, _mask_from_edges(n, edges))


_CUBIC_KINDS = {
    "petersen_coloring",
    "cubic_domination",
    "oddness",
    "barnette",
    "weak_pentagon",
    "p3_partition",
    "matching_intersection",
    "three_decomposition",
    "prescribed_cycle_double_cover",
    "edge_color_after_deletion",
}
_HIGH_CONNECTIVITY_KINDS = {
    "flow3",
    "modular_orientation",
    "jorgensen",
    "forcing_k6_minor",
}
_TRIANGLE_FREE_KINDS = {
    "triangle_free_chromatic",
    "barnette",
    "weak_pentagon",
}
_REGULAR_KINDS = {
    "vertex_transitive_hamiltonian",
    "regular_hamiltonian",
    "strongly_regular_core",
    "r_graph_coloring",
}


def _premise_matched_graph(
    kind: str, max_vertices: int, rng: random.Random
) -> Graph:
    if kind == "uniform_forest_negative_association" and max_vertices >= 9:
        return _uniform_forest_frontier_graph(rng)
    if kind in _CUBIC_KINDS:
        if kind == "oddness" and max_vertices >= 10:
            generalized = [
                (order, step)
                for order in range(5, max_vertices // 2 + 1)
                for step in range(2, (order - 1) // 2 + 1)
            ]
            if generalized and rng.random() < 0.5:
                graph = _generalized_petersen_graph(
                    *rng.choice(generalized)
                )
            else:
                graph = _petersen_graph()
        elif kind == "barnette" and max_vertices >= 8:
            even_orders = list(range(4, max_vertices // 2 + 1, 2))
            graph = _prism_graph(rng.choice(even_orders))
        elif kind in {"cubic_domination", "p3_partition"} and max_vertices >= 6:
            possible_orders = [
                order
                for order in range(3, max_vertices // 2 + 1)
                if kind != "p3_partition" or (2 * order) % 3 == 0
            ]
            graph = _prism_graph(rng.choice(possible_orders))
        elif kind == "weak_pentagon" and max_vertices >= 8:
            graph = _prism_graph(rng.randint(4, max_vertices // 2))
        elif max_vertices >= 10 and kind in {
            "petersen_coloring",
            "matching_intersection",
            "prescribed_cycle_double_cover",
        } and rng.random() < 0.25:
            graph = _petersen_graph()
        elif kind in {
            "three_decomposition",
            "edge_color_after_deletion",
        } and max_vertices >= 6 and rng.random() < 0.65:
            graph = _prism_graph(rng.randint(3, max_vertices // 2))
        elif kind in _TRIANGLE_FREE_KINDS and rng.random() < 0.55:
            graph = _random_cubic_bipartite_graph(max_vertices, rng)
        else:
            possible = [n for n in range(4, max_vertices + 1, 2)]
            graph = (
                _random_regular_graph(rng.choice(possible), 3, rng)
                if possible
                else None
            )
        if graph is not None:
            return graph
    if kind in _TRIANGLE_FREE_KINDS:
        return _random_bipartite_graph(rng.randint(1, max_vertices), rng)
    if kind == "jorgensen" and max_vertices >= 13:
        return _apex_icosahedron_graph()
    if kind in _HIGH_CONNECTIVITY_KINDS:
        minimum = min(6, max_vertices)
        return _dense_high_connectivity_graph(
            rng.randint(minimum, max_vertices), rng
        )
    if kind == "cycle_decomposition":
        return _random_eulerian_graph(rng.randint(1, max_vertices), rng)
    if kind == "planar_odd_cycle_hom":
        n = rng.randint(3, max_vertices) if max_vertices >= 3 else max_vertices
        return _cycle_graph(n)
    if kind == "planar_cycle_packing":
        return _planar_cycle_family(max_vertices, rng)
    if kind == "flow4":
        n = rng.randint(3, max_vertices) if max_vertices >= 3 else max_vertices
        return _random_eulerian_graph(n, rng)
    if kind == "modular_cycles":
        return _dense_high_connectivity_graph(max_vertices, rng)
    if kind == "strongly_regular_core":
        return _strongly_regular_graph(max_vertices, rng)
    if kind == "vertex_transitive_hamiltonian":
        return _vertex_transitive_graph(max_vertices, rng)
    if kind == "regular_hamiltonian":
        possible = [
            (n, degree)
            for n in range(4, max_vertices + 1)
            for degree in range(3, n)
            if n * degree % 2 == 0
        ]
        if possible:
            for _ in range(20):
                graph = _random_regular_graph(*rng.choice(possible), rng)
                if graph is not None:
                    return graph
    if kind in _REGULAR_KINDS:
        if rng.random() < 0.45:
            return _structured_graph(max_vertices, rng)
        n = rng.randint(3, max_vertices) if max_vertices >= 3 else max_vertices
        possible = [
            degree
            for degree in range(2, min(6, n))
            if n * degree % 2 == 0
        ]
        if possible:
            graph = _random_regular_graph(n, rng.choice(possible), rng)
            if graph is not None:
                return graph
    if kind in {"path_decomposition", "fractional_power"}:
        n = rng.randint(2, max_vertices) if max_vertices >= 2 else max_vertices
        graph = _random_density_graph(n, rng.choice((0.25, 0.5, 0.75)), rng)
        if n and not _connected(graph):
            return _cycle_graph(n) if n >= 3 else _complete_graph(n)
        return graph
    return _structured_graph(max_vertices, rng)


def _random_regular_family(max_vertices: int, rng: random.Random) -> Graph:
    choices = [
        (n, degree)
        for n in range(3, max_vertices + 1)
        for degree in range(2, n)
        if n * degree % 2 == 0
    ]
    if choices:
        for _ in range(20):
            graph = _random_regular_graph(*rng.choice(choices), rng)
            if graph is not None:
                return graph
    return _structured_graph(max_vertices, rng)


def _case_random(seed: int, index: int, salt: int) -> random.Random:
    mixed = (
        int(seed) * 0x9E3779B185EBCA87
        + int(index) * 0xC2B2AE3D27D4EB4F
        + salt
    ) & ((1 << 64) - 1)
    return random.Random(mixed)


def _planar_target_family(graph: Graph) -> str:
    edge_count = len(graph.edges)
    if graph.n >= 3 and edge_count == 3 * graph.n - 6:
        return "triangulation"
    if (
        graph.n >= 4
        and _is_bipartite(graph)
        and edge_count >= 2 * graph.n - 4
    ):
        return "quadrangulation"
    connected = _connected(graph)
    has_cut_vertex = connected and graph.n >= 3 and any(
        not _connected(graph, 1 << vertex)
        for vertex in range(graph.n)
    )
    if not connected or has_cut_vertex:
        return "clique_sum_or_gadget"
    if edge_count >= max(graph.n, 2 * graph.n - 3):
        return "feedback_pressure"
    return "general_planar"


@lru_cache(maxsize=None)
def _planar_targeted_corpus(
    max_vertices: int, seed: int
) -> tuple[Graph, ...]:
    groups: dict[str, list[Graph]] = {
        "triangulation": [],
        "quadrangulation": [],
        "clique_sum_or_gadget": [],
        "feedback_pressure": [],
        "general_planar": [],
    }
    for graph in _planar_unlabeled_corpus(max_vertices):
        groups[_planar_target_family(graph)].append(graph)
    labels = tuple(groups)
    for index, label in enumerate(labels):
        _case_random(seed, index, 0x504C414E4152).shuffle(groups[label])
    ordered: list[Graph] = []
    for batch in itertools.zip_longest(
        *(groups[label] for label in labels)
    ):
        ordered.extend(graph for graph in batch if graph is not None)
    return tuple(ordered)


def _iter_targeted_graphs(
    spec: Mapping[str, Any],
    max_vertices: int,
    seed: int,
    count: int,
    *,
    start: int = 0,
) -> Iterable[Graph]:
    """Yield a reproducible mixture with premise-biased and global exploration."""
    if spec["kind"] == "planar_odd_cycle_hom":
        corpus = _odd_cycle_structural_corpus(max_vertices)
        order = list(range(len(corpus)))
        _case_random(seed, 0, 0x4F44444359434C45).shuffle(order)
        for rank in range(start, min(start + count, len(order))):
            graph = corpus[order[rank]]
            permutation = list(range(graph.n))
            _case_random(
                seed, rank, 0x4F444452454C4142
            ).shuffle(permutation)
            yield _relabel_graph(graph, permutation)
        return
    if spec["kind"] == "seagull_minor":
        groups = [list(group) for group in _seagull_canonical_groups(max_vertices)]
        for index, group in enumerate(groups):
            _case_random(
                seed, index, 0x53454147554C4C
            ).shuffle(group)
        ordered = [
            graph
            for layer in itertools.zip_longest(*groups)
            for graph in layer
            if graph is not None
        ]
        yield from ordered[start : start + count]
        return
    if spec["kind"] == "planar_cycle_packing":
        corpus = _planar_targeted_corpus(max_vertices, int(seed))
        yield from corpus[start : start + count]
        return
    if (
        spec["kind"] == "uniform_forest_negative_association"
        and max_vertices >= 9
    ):
        for index in range(start, start + count):
            rng = _case_random(seed, index, 0x4752415048)
            yield _uniform_forest_frontier_graph(rng)
        return
    densities = (0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95)
    for index in range(start, start + count):
        rng = _case_random(seed, index, 0x4752415048)
        family = index % 10
        if family == 5:
            n = rng.randint(1, max_vertices)
            yield _random_density_graph(n, rng.choice(densities), rng)
        elif family == 6:
            yield _structured_graph(max_vertices, rng)
        elif family == 7:
            yield _random_regular_family(max_vertices, rng)
        elif family == 8:
            yield _random_bipartite_graph(rng.randint(1, max_vertices), rng)
        elif family == 9:
            n = rng.randint(1, max_vertices)
            if (index // 10) % 2:
                yield _dense_high_connectivity_graph(n, rng)
            else:
                yield _random_eulerian_graph(n, rng)
        else:
            yield _premise_matched_graph(spec["kind"], max_vertices, rng)


def _iter_sidorenko_exact_pairs(
    max_h_vertices: int,
    max_g_vertices: int,
) -> Iterable[tuple[Graph, Graph]]:
    sources = itertools.chain(
        (Graph(0, 0),),
        (
            graph
            for graph in _iter_nauty_graphs(max_h_vertices)
            if _is_bipartite(graph)
        ),
    )
    for source in sources:
        for target in _iter_nauty_graphs(max_g_vertices):
            yield source, target


def _four_cycle_count(graph: Graph) -> int:
    opposite_pair_counts = 0
    for left, right in itertools.combinations(range(graph.n), 2):
        common = (
            graph.adjacency[left] & graph.adjacency[right]
        ).bit_count()
        opposite_pair_counts += common * (common - 1) // 2
    return opposite_pair_counts // 2


def _sidorenko_has_universal_to_opposite(source: Graph) -> bool:
    components = _bipartition_components(source)
    if components is None or len(components) != 1:
        return False
    left, right = components[0]
    adjacency = source.adjacency
    return any(
        adjacency[vertex].bit_count() == len(right)
        for vertex in left
    ) or any(
        adjacency[vertex].bit_count() == len(left)
        for vertex in right
    )


def _sidorenko_filtered_family(source: Graph) -> str | None:
    """Name elementary known-positive shapes excluded from deep sampling."""
    sides = _bipartition_sizes(source)
    if sides is None:
        return "disconnected"
    if sides[0] <= 4:
        return "small_bipartition_side"
    edge_count = len(source.edges)
    cycle_rank = edge_count - source.n + 1
    if cycle_rank <= 0:
        return "tree"
    if cycle_rank == 1:
        return "single_cycle_or_unicyclic"
    if edge_count == sides[0] * sides[1]:
        return "complete_bipartite"
    if _sidorenko_has_universal_to_opposite(source):
        return "universal_to_opposite"
    degrees = [row.bit_count() for row in source.adjacency]
    branch_vertices = [degree for degree in degrees if degree > 2]
    if min(degrees, default=0) == 2 and len(branch_vertices) == 2:
        return "theta"
    if (
        source.n % 2 == 0
        and edge_count == 3 * source.n // 2 - 2
        and sorted(degrees)
        == [2] * 4 + [3] * (source.n - 4)
        and _four_cycle_count(source) >= source.n // 2 - 1
    ):
        return "ladder"
    if cycle_rank < 3:
        return "low_cycle_rank"
    return None


def _sidorenko_partition_sizes(
    max_vertices: int, index: int
) -> tuple[int, int] | None:
    if max_vertices < 10:
        return None
    if max_vertices >= 12 and index % 5 == 4:
        return 6, 6
    if max_vertices >= 11 and index % 2:
        return 5, 6
    return 5, 5


def _sidorenko_general_source(
    max_vertices: int, index: int, rng: random.Random
) -> Graph:
    partition = _sidorenko_partition_sizes(max_vertices, index)
    if partition is None:
        return _random_bipartite_graph(max_vertices, rng)
    left_size, right_size = partition
    order = left_size + right_size
    densities = (0.42, 0.5, 0.58, 0.66, 0.74)
    probability = densities[index % len(densities)]
    for _attempt in range(2_000):
        graph = Graph(
            order,
            _mask_from_edges(
                order,
                (
                    (left, left_size + right)
                    for left in range(left_size)
                    for right in range(right_size)
                    if rng.random() < probability
                ),
            ),
        )
        degrees = [row.bit_count() for row in graph.adjacency]
        if (
            _sidorenko_filtered_family(graph) is None
            and len(set(degrees)) >= 3
        ):
            permutation = list(range(order))
            rng.shuffle(permutation)
            return _relabel_graph(graph, permutation)
    raise RuntimeError("failed to construct a general Sidorenko source")


def _iter_sidorenko_targeted_pairs(
    max_h_vertices: int,
    max_g_vertices: int,
    seed: int,
    count: int,
    *,
    start: int = 0,
) -> Iterable[tuple[Graph, Graph]]:
    densities = (0.05, 0.2, 0.4, 0.6, 0.8, 0.95)
    for index in range(start, start + count):
        rng = _case_random(seed, index, 0x5349444F52454E4B)
        if max_h_vertices >= 10:
            source = _sidorenko_general_source(
                max_h_vertices, index, rng
            )
        else:
            source = _random_bipartite_graph(
                rng.randint(1, max_h_vertices), rng
            )
        if index % 4 == 3:
            target = _structured_graph(max_g_vertices, rng)
        else:
            target = _random_density_graph(
                rng.randint(1, max_g_vertices),
                rng.choice(densities),
                rng,
            )
        yield source, target


def _connected(graph: Graph, removed: int = 0) -> bool:
    alive = ((1 << graph.n) - 1) & ~removed
    if not alive:
        return True
    seen = alive & -alive
    frontier = seen
    adjacency = graph.adjacency
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        additions = adjacency[bit.bit_length() - 1] & alive & ~seen
        seen |= additions
        frontier |= additions
    return seen == alive


@lru_cache(maxsize=None)
def _vertex_connectivity_at_least(graph: Graph, value: int) -> bool:
    if graph.n <= value or min(map(int.bit_count, graph.adjacency), default=0) < value:
        return False
    for size in range(value):
        for vertices in itertools.combinations(range(graph.n), size):
            removed = sum(1 << vertex for vertex in vertices)
            if not _connected(graph, removed):
                return False
    return True


def _connected_subsets(graph: Graph) -> list[int]:
    subsets = []
    for subset in range(1, 1 << graph.n):
        _check_predicate_deadline()
        start = subset & -subset
        seen = start
        frontier = start
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            additions = graph.adjacency[bit.bit_length() - 1] & subset & ~seen
            seen |= additions
            frontier |= additions
        if seen == subset:
            subsets.append(subset)
    return subsets


def _has_shallow_complete_minor(graph: Graph, order: int) -> bool:
    """Search exact minor models whose branch sets have one or two vertices."""
    subsets = [1 << vertex for vertex in range(graph.n)]
    subsets.extend(
        (1 << left) | (1 << right) for left, right in graph.edges
    )
    neighborhoods = []
    for subset in subsets:
        neighborhood = 0
        vertices = subset
        while vertices:
            bit = vertices & -vertices
            vertices ^= bit
            neighborhood |= graph.adjacency[bit.bit_length() - 1]
        neighborhoods.append(neighborhood)
    compatibility = [0] * len(subsets)
    for left in range(len(subsets)):
        for right in range(left + 1, len(subsets)):
            if (
                not subsets[left] & subsets[right]
                and neighborhoods[left] & subsets[right]
            ):
                compatibility[left] |= 1 << right
                compatibility[right] |= 1 << left

    def visit(candidates: int, chosen: int) -> bool:
        _check_predicate_deadline()
        needed = order - chosen
        if needed == 0:
            return True
        if candidates.bit_count() < needed:
            return False
        while candidates:
            if candidates.bit_count() < needed:
                return False
            bit = candidates & -candidates
            candidates ^= bit
            index = bit.bit_length() - 1
            if visit(candidates & compatibility[index], chosen + 1):
                return True
        return False

    return visit((1 << len(subsets)) - 1, 0)


def _has_complete_minor(graph: Graph, order: int) -> bool:
    if graph.n < order:
        return False
    if _has_shallow_complete_minor(graph, order):
        return True
    connected = sorted(
        (
            subset
            for subset in _connected_subsets(graph)
            if subset.bit_count() <= graph.n - order + 1
        ),
        key=lambda subset: (subset.bit_count(), subset),
    )
    neighborhoods: dict[int, int] = {}
    for subset in connected:
        neighborhood = 0
        vertices = subset
        while vertices:
            bit = vertices & -vertices
            vertices ^= bit
            neighborhood |= graph.adjacency[bit.bit_length() - 1]
        neighborhoods[subset] = neighborhood

    def adjacent(left: int, right: int) -> bool:
        return bool(neighborhoods[left] & right)

    def visit(chosen: tuple[int, ...], minimum: int) -> bool:
        _check_predicate_deadline()
        if len(chosen) == order:
            return True
        used = 0
        for subset in chosen:
            used |= subset
        needed = order - len(chosen)
        if graph.n - used.bit_count() < needed:
            return False
        for index in range(minimum, len(connected)):
            subset = connected[index]
            if subset & used or any(not adjacent(subset, other) for other in chosen):
                continue
            if visit(chosen + (subset,), index + 1):
                return True
        return False

    return visit((), 0)


@lru_cache(maxsize=None)
def _vertex_transitive(graph: Graph) -> bool:
    if not _connected(graph):
        return False
    adjacency = graph.adjacency
    degrees = tuple(row.bit_count() for row in adjacency)
    if len(set(degrees)) != 1:
        return False

    def has_automorphism(target: int) -> bool:
        mapping = [-1] * graph.n
        inverse = [-1] * graph.n
        mapping[0] = target
        inverse[target] = 0

        def visit(mapped_count: int) -> bool:
            _check_predicate_deadline()
            if mapped_count == graph.n:
                return True
            unmapped = [vertex for vertex in range(graph.n) if mapping[vertex] < 0]
            source = max(
                unmapped,
                key=lambda vertex: (
                    sum(
                        mapping[other] >= 0
                        for other in range(graph.n)
                        if adjacency[vertex] & (1 << other)
                    ),
                    degrees[vertex],
                ),
            )
            for image in range(graph.n):
                if inverse[image] >= 0 or degrees[image] != degrees[source]:
                    continue
                if any(
                    (
                        bool(adjacency[source] & (1 << other))
                        != bool(adjacency[image] & (1 << mapping[other]))
                    )
                    for other in range(graph.n)
                    if mapping[other] >= 0
                ):
                    continue
                mapping[source] = image
                inverse[image] = source
                if visit(mapped_count + 1):
                    return True
                mapping[source] = -1
                inverse[image] = -1
            return False

        return visit(1)

    return all(has_automorphism(target) for target in range(1, graph.n))


def _bridgeless(graph: Graph) -> bool:
    if not _connected(graph):
        return False
    for edge in graph.edges:
        if not _connected(Graph(graph.n, graph.mask & ~(1 << _edge_pairs(graph.n).index(edge)))):
            return False
    return True


def _edge_connectivity(graph: Graph) -> int:
    if not _connected(graph):
        return 0
    best = len(graph.edges)
    all_vertices = (1 << graph.n) - 1
    for side in range(1, 1 << max(0, graph.n - 1)):
        complement = all_vertices ^ side
        if not complement:
            continue
        cut = sum(
            bool(side & (1 << left)) != bool(side & (1 << right))
            for left, right in graph.edges
        )
        best = min(best, cut)
    return best


def _is_bipartite(graph: Graph, edge_mask: int | None = None) -> bool:
    allowed = graph.mask if edge_mask is None else edge_mask
    adjacency = Graph(graph.n, allowed).adjacency
    colors = [-1] * graph.n
    for root in range(graph.n):
        if colors[root] >= 0:
            continue
        colors[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            neighbors = adjacency[vertex]
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                other = bit.bit_length() - 1
                if colors[other] < 0:
                    colors[other] = 1 - colors[vertex]
                    stack.append(other)
                elif colors[other] == colors[vertex]:
                    return False
    return True


def _colorable(graph: Graph, color_count: int) -> bool:
    if color_count <= 0:
        return graph.n == 0
    adjacency = graph.adjacency
    order = sorted(
        range(graph.n), key=lambda vertex: adjacency[vertex].bit_count(), reverse=True
    )
    colors = [-1] * graph.n

    def visit(index: int, used: int) -> bool:
        _check_predicate_deadline()
        if index == graph.n:
            return True
        vertex = order[index]
        unavailable = {
            colors[other]
            for other in range(graph.n)
            if colors[other] >= 0 and adjacency[vertex] & (1 << other)
        }
        for color in range(min(color_count, used + 1)):
            if color in unavailable:
                continue
            colors[vertex] = color
            if visit(index + 1, max(used, color + 1)):
                return True
            colors[vertex] = -1
        return False

    return visit(0, 0)


def _chromatic_number(graph: Graph) -> int:
    for colors in range(1, graph.n + 1):
        if _colorable(graph, colors):
            return colors
    return graph.n


def _cliques(graph: Graph) -> list[int]:
    result = []
    for subset in range(1, 1 << graph.n):
        _check_predicate_deadline()
        vertices = [v for v in range(graph.n) if subset & (1 << v)]
        if all(
            graph.adjacency[left] & (1 << right)
            for left, right in itertools.combinations(vertices, 2)
        ):
            result.append(subset)
    return result


def _cycles(graph: Graph) -> list[tuple[int, ...]]:
    found: set[tuple[int, ...]] = set()
    adjacency = graph.adjacency
    for start in range(graph.n):
        stack = [(start, (start,), 1 << start)]
        while stack:
            _check_predicate_deadline()
            vertex, path, used = stack.pop()
            neighbors = adjacency[vertex]
            for nxt in range(start, graph.n):
                if not neighbors & (1 << nxt):
                    continue
                if nxt == start and len(path) >= 3:
                    reverse = (start,) + tuple(reversed(path[1:]))
                    found.add(min(path, reverse))
                elif not used & (1 << nxt):
                    stack.append((nxt, path + (nxt,), used | (1 << nxt)))
    return sorted(found, key=lambda item: (len(item), item))


@lru_cache(maxsize=None)
def _girth(graph: Graph) -> int:
    best = 10**9
    adjacency = graph.adjacency
    for root in range(graph.n):
        _check_predicate_deadline()
        distances = [-1] * graph.n
        parents = [-1] * graph.n
        distances[root] = 0
        queue = [root]
        position = 0
        while position < len(queue):
            vertex = queue[position]
            position += 1
            if 2 * distances[vertex] + 1 >= best:
                continue
            neighbors = adjacency[vertex]
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                other = bit.bit_length() - 1
                if distances[other] < 0:
                    distances[other] = distances[vertex] + 1
                    parents[other] = vertex
                    queue.append(other)
                elif parents[vertex] != other:
                    best = min(
                        best,
                        distances[vertex] + distances[other] + 1,
                    )
    return best


def _hom_to_cycle(graph: Graph, order: int) -> bool:
    if graph.n == 0:
        return True
    if order < 3:
        return not graph.edges

    adjacency_lists = [
        [other for other in range(graph.n) if row & (1 << other)]
        for row in graph.adjacency
    ]
    branch_vertices = [
        vertex
        for vertex, neighbors in enumerate(adjacency_lists)
        if len(neighbors) != 2
    ]
    branch_index = {
        vertex: index for index, vertex in enumerate(branch_vertices)
    }
    visited_edges: set[tuple[int, int]] = set()
    paths: list[tuple[int, int, int]] = []

    def edge_key(left: int, right: int) -> tuple[int, int]:
        return min(left, right), max(left, right)

    for start in branch_vertices:
        for neighbor in adjacency_lists[start]:
            first_edge = edge_key(start, neighbor)
            if first_edge in visited_edges:
                continue
            visited_edges.add(first_edge)
            previous, current = start, neighbor
            length = 1
            while current not in branch_index:
                first, second = adjacency_lists[current]
                following = second if first == previous else first
                visited_edges.add(edge_key(current, following))
                previous, current = current, following
                length += 1
            paths.append(
                (branch_index[start], branch_index[current], length)
            )

    # Components containing only degree-two vertices are cycles.
    for left, right in graph.edges:
        initial = edge_key(left, right)
        if initial in visited_edges:
            continue
        visited_edges.add(initial)
        previous, current = left, right
        length = 1
        while current != left:
            first, second = adjacency_lists[current]
            following = second if first == previous else first
            visited_edges.add(edge_key(current, following))
            previous, current = current, following
            length += 1
        differences = {
            (length - 2 * backward) % order
            for backward in range(length + 1)
        }
        if 0 not in differences:
            return False

    if not branch_vertices:
        return True

    directed_constraints: list[tuple[int, int, frozenset[int]]] = []
    component_adjacency = [set() for _ in branch_vertices]
    for left, right, length in paths:
        differences = frozenset(
            (length - 2 * backward) % order
            for backward in range(length + 1)
        )
        if left == right:
            if 0 not in differences:
                return False
            continue
        directed_constraints.append((left, right, differences))
        directed_constraints.append(
            (
                right,
                left,
                frozenset((-difference) % order for difference in differences),
            )
        )
        component_adjacency[left].add(right)
        component_adjacency[right].add(left)

    all_colors = (1 << order) - 1
    domains = [all_colors] * len(branch_vertices)
    unseen = set(range(len(branch_vertices)))
    while unseen:
        root = min(unseen)
        domains[root] = 1
        stack = [root]
        unseen.remove(root)
        while stack:
            vertex = stack.pop()
            for other in component_adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)

    incoming: list[list[int]] = [[] for _ in branch_vertices]
    for index, (_left, right, _differences) in enumerate(
        directed_constraints
    ):
        incoming[right].append(index)

    def propagate(
        current: list[int], initial_queue: Iterable[int]
    ) -> list[int] | None:
        queue = list(initial_queue)
        queued = set(queue)
        position = 0
        while position < len(queue):
            _check_predicate_deadline()
            constraint_index = queue[position]
            position += 1
            queued.discard(constraint_index)
            left, right, differences = directed_constraints[
                constraint_index
            ]
            revised = 0
            colors = current[left]
            while colors:
                bit = colors & -colors
                colors ^= bit
                color = bit.bit_length() - 1
                if any(
                    current[right]
                    & (1 << ((color + difference) % order))
                    for difference in differences
                ):
                    revised |= bit
            if revised == current[left]:
                continue
            if not revised:
                return None
            current[left] = revised
            for incoming_index in incoming[left]:
                if incoming_index not in queued:
                    queued.add(incoming_index)
                    queue.append(incoming_index)
        return current

    def visit(current: list[int]) -> bool:
        _check_predicate_deadline()
        propagated = propagate(current, range(len(directed_constraints)))
        if propagated is None:
            return False
        undecided = [
            index
            for index, domain in enumerate(propagated)
            if domain.bit_count() > 1
        ]
        if not undecided:
            return True
        vertex = min(undecided, key=lambda item: propagated[item].bit_count())
        choices = propagated[vertex]
        while choices:
            bit = choices & -choices
            choices ^= bit
            narrowed = propagated.copy()
            narrowed[vertex] = bit
            if visit(narrowed):
                return True
        return False

    return visit(domains)


def _bounded_k_values(parameters: Mapping[str, Any]) -> tuple[int, ...]:
    raw = parameters.get("k_values")
    if raw is None:
        raw = [parameters.get("k", 1)]
    values = tuple(sorted({int(value) for value in raw if int(value) > 0}))
    return values


def _has_independent_triple(graph: Graph) -> bool:
    for first, second, third in itertools.combinations(range(graph.n), 3):
        if not (
            graph.adjacency[first] & (1 << second)
            or graph.adjacency[first] & (1 << third)
            or graph.adjacency[second] & (1 << third)
        ):
            return True
    return False


def _perfect_matchings(graph: Graph) -> list[int]:
    if graph.n % 2:
        return []
    edge_bits = {
        edge: 1 << index for index, edge in enumerate(_edge_pairs(graph.n))
    }
    result: list[int] = []

    def visit(unmatched: int, chosen: int) -> None:
        _check_predicate_deadline()
        if unmatched == 0:
            result.append(chosen)
            return
        bit = unmatched & -unmatched
        vertex = bit.bit_length() - 1
        neighbors = graph.adjacency[vertex] & unmatched
        while neighbors:
            other_bit = neighbors & -neighbors
            neighbors ^= other_bit
            other = other_bit.bit_length() - 1
            edge = (min(vertex, other), max(vertex, other))
            visit(unmatched ^ bit ^ other_bit, chosen | edge_bits[edge])

    visit((1 << graph.n) - 1, 0)
    return result


def _two_factor_cycle_lengths(graph: Graph, matching: int) -> list[int]:
    remaining = graph.mask & ~matching
    factor = Graph(graph.n, remaining)
    seen = 0
    lengths = []
    for root in range(graph.n):
        if seen & (1 << root):
            continue
        length = 0
        stack = [root]
        seen |= 1 << root
        while stack:
            vertex = stack.pop()
            length += 1
            neighbors = factor.adjacency[vertex] & ~seen
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                seen |= bit
                stack.append(bit.bit_length() - 1)
        lengths.append(length)
    return lengths


def _contains_odd_edge_cut(graph: Graph, edge_set: int) -> bool:
    for subset in range(1, 1 << max(0, graph.n - 1)):
        cut = 0
        for index, (left, right) in enumerate(_edge_pairs(graph.n)):
            if not graph.mask & (1 << index):
                continue
            if bool(subset & (1 << left)) != bool(subset & (1 << right)):
                cut |= 1 << index
        if cut.bit_count() % 2 and cut & edge_set == cut:
            return True
    return False


def _cycle_edge_mask(graph: Graph, cycle: tuple[int, ...]) -> int:
    return _mask_from_edges(
        graph.n,
        (
            (cycle[index], cycle[(index + 1) % len(cycle)])
            for index in range(len(cycle))
        ),
    )


def _paths(graph: Graph) -> list[tuple[int, ...]]:
    found: set[tuple[int, ...]] = set()
    for start in range(graph.n):
        stack = [(start, (start,), 1 << start)]
        while stack:
            _check_predicate_deadline()
            vertex, path, used = stack.pop()
            if len(path) >= 2:
                found.add(min(path, tuple(reversed(path))))
            available = graph.adjacency[vertex] & ~used
            while available:
                bit = available & -available
                available ^= bit
                stack.append((bit.bit_length() - 1, path + (bit.bit_length() - 1,), used | bit))
    return sorted(found)


def _hamiltonian_cycle_count(graph: Graph, limit: int = 2) -> int:
    if graph.n < 3:
        return 0
    count = 0

    def visit(path: tuple[int, ...], used: int) -> bool:
        nonlocal count
        _check_predicate_deadline()
        if len(path) == graph.n:
            if graph.adjacency[path[-1]] & 1 and path[1] < path[-1]:
                count += 1
            return count >= limit
        available = graph.adjacency[path[-1]] & ~used
        while available:
            bit = available & -available
            available ^= bit
            if visit(path + (bit.bit_length() - 1,), used | bit):
                return True
        return False

    visit((0,), 1)
    return count


def _has_hamiltonian_path(graph: Graph) -> bool:
    def visit(vertex: int, used: int) -> bool:
        _check_predicate_deadline()
        if used.bit_count() == graph.n:
            return True
        available = graph.adjacency[vertex] & ~used
        while available:
            bit = available & -available
            available ^= bit
            if visit(bit.bit_length() - 1, used | bit):
                return True
        return False

    return any(visit(start, 1 << start) for start in range(graph.n))


def _exact_cover_exists(universe: int, sets: list[int], max_sets: int) -> bool:
    by_bit: dict[int, list[int]] = {}
    for item in sets:
        bits = item
        while bits:
            bit = bits & -bits
            bits ^= bit
            by_bit.setdefault(bit, []).append(item)

    def visit(remaining: int, used: int) -> bool:
        _check_predicate_deadline()
        if remaining == 0:
            return True
        if used >= max_sets:
            return False
        bit = remaining & -remaining
        return any(
            visit(remaining ^ item, used + 1)
            for item in by_bit.get(bit, [])
            if item & remaining == item
        )

    return visit(universe, 0)


def _edge_conflict_graph(graph: Graph, *, strong: bool, total: bool = False) -> Graph:
    items = graph.n + len(graph.edges) if total else len(graph.edges)
    conflicts = []
    edge_list = list(graph.edges)
    if total:
        conflicts.extend(graph.edges)
        for vertex, edge_index in itertools.product(range(graph.n), range(len(edge_list))):
            if vertex in edge_list[edge_index]:
                conflicts.append((vertex, graph.n + edge_index))
        for first, second in itertools.combinations(range(len(edge_list)), 2):
            if set(edge_list[first]) & set(edge_list[second]):
                conflicts.append((graph.n + first, graph.n + second))
    else:
        for first, second in itertools.combinations(range(len(edge_list)), 2):
            endpoints = set(edge_list[first]) | set(edge_list[second])
            adjacent = len(endpoints) < 4
            if strong and not adjacent:
                adjacent = any(
                    graph.adjacency[left] & (1 << right)
                    for left in edge_list[first]
                    for right in edge_list[second]
                )
            if adjacent:
                conflicts.append((first, second))
    return Graph(items, _mask_from_edges(items, conflicts))


def _nowhere_zero_flow(graph: Graph, modulus_bound: int) -> bool:
    # Tutte's equivalence lets existence be checked over the finite group Z_k.
    values = tuple(range(1, modulus_bound))
    edges = list(graph.edges)

    @lru_cache(maxsize=None)
    def visit(index: int, balances: tuple[int, ...]) -> bool:
        _check_predicate_deadline()
        if index == len(edges):
            return all(value == 0 for value in balances)
        left, right = edges[index]
        for value in values:
            updated = list(balances)
            updated[left] = (updated[left] + value) % modulus_bound
            updated[right] = (updated[right] - value) % modulus_bound
            if visit(index + 1, tuple(updated)):
                return True
        return False

    return visit(0, (0,) * graph.n)


def _modular_orientation(graph: Graph, k: int) -> bool:
    modulus = 2 * k + 1
    edges = list(graph.edges)

    @lru_cache(maxsize=None)
    def visit(index: int, balances: tuple[int, ...]) -> bool:
        _check_predicate_deadline()
        if index == len(edges):
            return all(value % modulus == 0 for value in balances)
        left, right = edges[index]
        for sign in (-1, 1):
            updated = list(balances)
            updated[left] = (updated[left] + sign) % modulus
            updated[right] = (updated[right] - sign) % modulus
            if visit(index + 1, tuple(updated)):
                return True
        return False

    return visit(0, (0,) * graph.n)


def _edge_coloring(graph: Graph, colors: int) -> bool:
    return _colorable(_edge_conflict_graph(graph, strong=False), colors)


def _overfull_parameter(graph: Graph) -> int:
    best = 0
    for subset in range(1, 1 << graph.n):
        _check_predicate_deadline()
        order = subset.bit_count()
        denominator = order // 2
        if denominator == 0:
            continue
        edge_count = sum(
            bool(subset & (1 << left)) and bool(subset & (1 << right))
            for left, right in graph.edges
        )
        best = max(best, (edge_count + denominator - 1) // denominator)
    return best


def _multigraph_edge_colorable(
    vertices: set[int], edges: list[tuple[int, int]], colors: int
) -> bool:
    if any(left == right for left, right in edges):
        return False
    assigned = [-1] * len(edges)
    order = sorted(
        range(len(edges)),
        key=lambda index: sum(
            bool(set(edges[index]) & set(other))
            for other_index, other in enumerate(edges)
            if other_index != index
        ),
        reverse=True,
    )

    def visit(position: int) -> bool:
        _check_predicate_deadline()
        if position == len(order):
            return True
        index = order[position]
        unavailable = {
            assigned[other]
            for other in range(len(edges))
            if assigned[other] >= 0 and set(edges[index]) & set(edges[other])
        }
        for color in range(colors):
            if color in unavailable:
                continue
            assigned[index] = color
            if visit(position + 1):
                return True
        assigned[index] = -1
        return False

    return visit(0)


def _suppressed_after_edge_deletion(
    graph: Graph, deleted_edge: tuple[int, int]
) -> tuple[set[int], list[tuple[int, int]]]:
    vertices = set(range(graph.n))
    edges = list(graph.edges)
    edges.remove(deleted_edge)
    for vertex in deleted_edge:
        incident = [edge for edge in edges if vertex in edge]
        if len(incident) != 2:
            return vertices, edges
        neighbors = [
            right if left == vertex else left
            for left, right in incident
        ]
        for edge in incident:
            edges.remove(edge)
        vertices.remove(vertex)
        edges.append((neighbors[0], neighbors[1]))
    return vertices, edges


def _petersen_coloring(graph: Graph) -> bool:
    petersen = Graph(
        10,
        _mask_from_edges(
            10,
            [(i, (i + 1) % 5) for i in range(5)]
            + [(i, i + 5) for i in range(5)]
            + [(5 + i, 5 + ((i + 2) % 5)) for i in range(5)],
        ),
    )
    target_edges = list(petersen.edges)
    incident_targets = [
        {
            index
            for index, edge in enumerate(target_edges)
            if vertex in edge
        }
        for vertex in range(10)
    ]
    edges = list(graph.edges)
    at_vertex = [
        [index for index, edge in enumerate(edges) if vertex in edge]
        for vertex in range(graph.n)
    ]
    labels = [-1] * len(edges)

    def visit(index: int) -> bool:
        _check_predicate_deadline()
        if index == len(edges):
            return all(
                any(set(labels[item] for item in group) == target for target in incident_targets)
                for group in at_vertex
            )
        for label in range(len(target_edges)):
            labels[index] = label
            valid = True
            for group in at_vertex:
                assigned = {labels[item] for item in group if labels[item] >= 0}
                if not any(assigned <= target for target in incident_targets):
                    valid = False
                    break
            if valid and visit(index + 1):
                return True
        labels[index] = -1
        return False

    return visit(0)


def _set_partitions(n: int, max_block: int) -> Iterable[tuple[tuple[int, ...], ...]]:
    blocks: list[list[int]] = []

    def visit(vertex: int) -> Iterable[tuple[tuple[int, ...], ...]]:
        _check_predicate_deadline()
        if vertex == n:
            yield tuple(tuple(block) for block in blocks)
            return
        for block in blocks:
            if len(block) < max_block:
                block.append(vertex)
                yield from visit(vertex + 1)
                block.pop()
        blocks.append([vertex])
        yield from visit(vertex + 1)
        blocks.pop()

    yield from visit(0)


def _strongly_colorable(graph: Graph) -> bool:
    delta = max(map(int.bit_count, graph.adjacency), default=0)
    q = 2 * delta
    if graph.n <= q:
        return True
    for partition in _set_partitions(graph.n, q):
        extra = list(graph.edges)
        for block in partition:
            extra.extend(itertools.combinations(block, 2))
        conflict = Graph(graph.n, _mask_from_edges(graph.n, extra))
        if not _colorable(conflict, q):
            return False
    return True


def _weak_pentagon_coloring(graph: Graph) -> bool:
    edges = list(graph.edges)
    edge_indexes = {edge: index for index, edge in enumerate(edges)}
    odd_cycles = [
        {
            edge_indexes[
                (
                    min(cycle[index], cycle[(index + 1) % len(cycle)]),
                    max(cycle[index], cycle[(index + 1) % len(cycle)]),
                )
            ]
            for index in range(len(cycle))
        }
        for cycle in _cycles(graph)
        if len(cycle) % 2
    ]
    if not odd_cycles:
        return True
    if any(len(cycle) < 5 for cycle in odd_cycles):
        return False
    order = sorted(
        range(len(edges)),
        key=lambda edge: sum(edge in cycle for cycle in odd_cycles),
        reverse=True,
    )
    colors = [-1] * len(edges)

    def visit(position: int, used_colors: int) -> bool:
        _check_predicate_deadline()
        if position == len(order):
            return all({colors[edge] for edge in cycle} == set(range(5)) for cycle in odd_cycles)
        edge = order[position]
        for color in range(min(5, used_colors + 1)):
            colors[edge] = color
            feasible = True
            for cycle in odd_cycles:
                present = {colors[item] for item in cycle if colors[item] >= 0}
                remaining = sum(colors[item] < 0 for item in cycle)
                if 5 - len(present) > remaining:
                    feasible = False
                    break
            if feasible and visit(position + 1, max(used_colors, color + 1)):
                return True
        colors[edge] = -1
        return False

    return visit(0, 0)


def _induced_odd_hole(graph: Graph) -> bool:
    for cycle in _cycles(graph):
        if len(cycle) < 5 or len(cycle) % 2 == 0:
            continue
        induced_edges = sum(
            bool(graph.adjacency[left] & (1 << right))
            for left, right in itertools.combinations(cycle, 2)
        )
        if induced_edges == len(cycle):
            return True
    return False


def _max_clique_two_colorable(graph: Graph) -> bool:
    cliques = _cliques(graph)
    maximum = max((item.bit_count() for item in cliques), default=0)
    maximum_cliques = [item for item in cliques if item.bit_count() == maximum]
    all_vertices = (1 << graph.n) - 1
    for red in range(1 << graph.n):
        if all(red & clique not in {0, clique} for clique in maximum_cliques):
            return True
        if red == all_vertices:
            break
    return False


def _fractional_three_power(graph: Graph) -> Graph:
    edges: list[tuple[int, int]] = []
    next_vertex = graph.n
    for left, right in graph.edges:
        first, second = next_vertex, next_vertex + 1
        next_vertex += 2
        edges.extend(((left, first), (first, second), (second, right)))
    subdivision = Graph(next_vertex, _mask_from_edges(next_vertex, edges))
    powered_edges = []
    for source in range(next_vertex):
        distances = {source: 0}
        queue = [source]
        for vertex in queue:
            if distances[vertex] == 3:
                continue
            neighbors = subdivision.adjacency[vertex]
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                other = bit.bit_length() - 1
                if other not in distances:
                    distances[other] = distances[vertex] + 1
                    queue.append(other)
        powered_edges.extend(
            (source, target)
            for target, distance in distances.items()
            if source < target and 1 <= distance <= 3
        )
    return Graph(next_vertex, _mask_from_edges(next_vertex, powered_edges))


def _domination_number(graph: Graph) -> int:
    all_vertices = (1 << graph.n) - 1
    closed = tuple(row | (1 << vertex) for vertex, row in enumerate(graph.adjacency))
    for size in range(graph.n + 1):
        for selected in itertools.combinations(range(graph.n), size):
            covered = 0
            for vertex in selected:
                covered |= closed[vertex]
            if covered == all_vertices:
                return size
    return graph.n


def _has_p3_partition(graph: Graph) -> bool:
    sets = []
    for center in range(graph.n):
        neighbors = [
            vertex
            for vertex in range(graph.n)
            if graph.adjacency[center] & (1 << vertex)
        ]
        sets.extend(
            (1 << center) | (1 << left) | (1 << right)
            for left, right in itertools.combinations(neighbors, 2)
        )
    return _exact_cover_exists((1 << graph.n) - 1, list(set(sets)), graph.n // 3)


def _has_path_decomposition(graph: Graph, limit: int) -> bool:
    path_masks = [_mask_from_edges(graph.n, zip(path, path[1:])) for path in _paths(graph)]
    return _exact_cover_exists(graph.mask, list(set(path_masks)), limit)


def _has_cycle_decomposition(graph: Graph, limit: int) -> bool:
    cycle_masks = [_cycle_edge_mask(graph, cycle) for cycle in _cycles(graph)]
    return _exact_cover_exists(graph.mask, cycle_masks, limit)


def _is_tree_edge_set(graph: Graph, edge_set: int) -> bool:
    if edge_set.bit_count() != graph.n - 1:
        return False
    return _connected(Graph(graph.n, edge_set))


def _three_decomposition(graph: Graph) -> bool:
    edge_bits = [
        1 << index
        for index in range(len(_edge_pairs(graph.n)))
        if graph.mask & (1 << index)
    ]
    for chosen in itertools.combinations(edge_bits, graph.n - 1):
        _check_predicate_deadline()
        tree = 0
        for bit in chosen:
            tree |= bit
        if not _is_tree_edge_set(graph, tree):
            continue
        rest = graph.mask & ~tree
        sub = rest
        while True:
            cycle_part = sub
            matching_part = rest & ~sub
            cycle_degrees = Graph(graph.n, cycle_part).adjacency
            matching_degrees = Graph(graph.n, matching_part).adjacency
            if all(row.bit_count() in {0, 2} for row in cycle_degrees) and all(
                row.bit_count() <= 1 for row in matching_degrees
            ):
                return True
            if sub == 0:
                break
            sub = (sub - 1) & rest
    return False


def _cycle_double_cover(
    graph: Graph, required_cycles: tuple[int, ...] = ()
) -> bool:
    cycles = [_cycle_edge_mask(graph, cycle) for cycle in _cycles(graph)]
    coverage = [0] * len(_edge_pairs(graph.n))
    for cycle in required_cycles:
        if cycle not in cycles:
            return False
        for bit in range(len(coverage)):
            if cycle & (1 << bit):
                coverage[bit] += 1
    if any(value > 2 for value in coverage):
        return False

    @lru_cache(maxsize=None)
    def visit(state: tuple[int, ...]) -> bool:
        _check_predicate_deadline()
        coverage[:] = state
        target_bit = next(
            (
                bit
                for bit in range(len(coverage))
                if graph.mask & (1 << bit) and coverage[bit] < 2
            ),
            None,
        )
        if target_bit is None:
            return all(
                coverage[bit] == 2
                for bit in range(len(coverage))
                if graph.mask & (1 << bit)
            )
        for cycle in cycles:
            if not cycle & (1 << target_bit):
                continue
            touched = [bit for bit in range(len(coverage)) if cycle & (1 << bit)]
            if any(coverage[bit] >= 2 for bit in touched):
                continue
            for bit in touched:
                coverage[bit] += 1
            updated = tuple(coverage)
            if visit(updated):
                return True
            coverage[:] = state
        return False

    return visit(tuple(coverage))


def _canonical_mask(graph: Graph) -> int:
    best = graph.mask
    for permutation in itertools.permutations(range(graph.n)):
        _check_predicate_deadline()
        candidate = _mask_from_edges(
            graph.n,
            ((permutation[left], permutation[right]) for left, right in graph.edges),
        )
        best = min(best, candidate)
    return best


def _edge_deck(graph: Graph) -> tuple[int, ...]:
    result = []
    for bit in range(len(_edge_pairs(graph.n))):
        if graph.mask & (1 << bit):
            result.append(_canonical_mask(Graph(graph.n, graph.mask & ~(1 << bit))))
    return tuple(sorted(result))


def _strongly_regular_parameters(graph: Graph) -> tuple[int, int, int] | None:
    degrees = [row.bit_count() for row in graph.adjacency]
    if not degrees or len(set(degrees)) != 1:
        return None
    adjacent_common = set()
    nonadjacent_common = set()
    for left, right in itertools.combinations(range(graph.n), 2):
        common = (graph.adjacency[left] & graph.adjacency[right]).bit_count()
        if graph.adjacency[left] & (1 << right):
            adjacent_common.add(common)
        else:
            nonadjacent_common.add(common)
    if len(adjacent_common) != 1 or len(nonadjacent_common) != 1:
        return None
    return degrees[0], next(iter(adjacent_common)), next(iter(nonadjacent_common))


def _endomorphism_images(graph: Graph) -> list[set[int]]:
    images: list[set[int]] = []
    mapping = [-1] * graph.n
    order = sorted(range(graph.n), key=lambda v: graph.adjacency[v].bit_count(), reverse=True)

    def visit(index: int) -> None:
        _check_predicate_deadline()
        if index == graph.n:
            images.append(set(mapping))
            return
        vertex = order[index]
        for target in range(graph.n):
            valid = True
            for earlier in order[:index]:
                if graph.adjacency[vertex] & (1 << earlier):
                    if not graph.adjacency[target] & (1 << mapping[earlier]):
                        valid = False
                        break
            if valid:
                mapping[vertex] = target
                visit(index + 1)
        mapping[vertex] = -1

    visit(0)
    return images


def _core_is_graph_or_complete(graph: Graph) -> bool:
    images = _endomorphism_images(graph)
    minimum = min(map(len, images), default=graph.n)
    if minimum == graph.n:
        return True
    for image in images:
        if len(image) != minimum:
            continue
        if all(
            graph.adjacency[left] & (1 << right)
            for left, right in itertools.combinations(image, 2)
        ):
            return True
    return False


def _r_graph(graph: Graph) -> int | None:
    degrees = [row.bit_count() for row in graph.adjacency]
    if not degrees or len(set(degrees)) != 1:
        return None
    r = degrees[0]
    for subset in range(1, 1 << graph.n):
        _check_predicate_deadline()
        if subset.bit_count() % 2 == 0:
            continue
        cut = sum(
            bool(subset & (1 << left)) != bool(subset & (1 << right))
            for left, right in graph.edges
        )
        if cut < r:
            return None
    return r


def _uniform_forest_violation(graph: Graph) -> dict[str, Any] | None:
    edges = list(graph.edges)
    edge_count = len(edges)
    if edge_count < 2:
        return None
    total = 0
    containing = [0] * edge_count
    containing_pair = [
        [0] * edge_count
        for _ in range(edge_count)
    ]
    for selected in range(1 << edge_count):
        _check_predicate_deadline()
        parent = list(range(graph.n))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        present: list[int] = []
        acyclic = True
        for index, (left, right) in enumerate(edges):
            if not selected & (1 << index):
                continue
            left_root = find(left)
            right_root = find(right)
            if left_root == right_root:
                acyclic = False
                break
            parent[left_root] = right_root
            present.append(index)
        if not acyclic:
            continue
        total += 1
        for index in present:
            containing[index] += 1
        for first, second in itertools.combinations(present, 2):
            containing_pair[first][second] += 1
            containing_pair[second][first] += 1
    for first, second in itertools.combinations(range(edge_count), 2):
        left_value = containing_pair[first][second] * total
        right_value = containing[first] * containing[second]
        if left_value > right_value:
            return {
                "edge_e": list(edges[first]),
                "edge_f": list(edges[second]),
                "forest_count": total,
                "forest_count_e": containing[first],
                "forest_count_f": containing[second],
                "forest_count_ef": containing_pair[first][second],
                "left_integer_product": left_value,
                "right_integer_product": right_value,
            }
    return None


def _acyclic_after_vertex_deletion(graph: Graph, removed: int) -> bool:
    parent = list(range(graph.n))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in graph.edges:
        _check_predicate_deadline()
        if removed & (1 << left) or removed & (1 << right):
            continue
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def _cycle_packing_number(cycle_masks: tuple[int, ...]) -> int:
    @lru_cache(maxsize=None)
    def visit(index: int, used_vertices: int) -> int:
        _check_predicate_deadline()
        if index == len(cycle_masks):
            return 0
        best = visit(index + 1, used_vertices)
        cycle = cycle_masks[index]
        if not cycle & used_vertices:
            best = max(best, 1 + visit(index + 1, used_vertices | cycle))
        return best

    return visit(0, 0)


def _planar_cycle_parameters(graph: Graph) -> tuple[int, int]:
    cycle_masks = tuple(
        sorted(
            {
                sum(1 << vertex for vertex in cycle)
                for cycle in _cycles(graph)
            },
            key=lambda item: (item.bit_count(), item),
        )
    )
    packing = _cycle_packing_number(cycle_masks)
    feedback = graph.n
    for size in range(graph.n + 1):
        for vertices in itertools.combinations(range(graph.n), size):
            _check_predicate_deadline()
            removed = sum(1 << vertex for vertex in vertices)
            if _acyclic_after_vertex_deletion(graph, removed):
                feedback = size
                return packing, feedback
    return packing, feedback


def _bipartition_components(
    graph: Graph,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...] | None:
    colors = [-1] * graph.n
    components: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    adjacency = graph.adjacency
    for root in range(graph.n):
        if colors[root] >= 0:
            continue
        colors[root] = 0
        queue = [root]
        vertices: list[int] = []
        for vertex in queue:
            vertices.append(vertex)
            neighbors = adjacency[vertex]
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                other = bit.bit_length() - 1
                if colors[other] < 0:
                    colors[other] = 1 - colors[vertex]
                    queue.append(other)
                elif colors[other] == colors[vertex]:
                    return None
        components.append(
            (
                tuple(vertex for vertex in vertices if colors[vertex] == 0),
                tuple(vertex for vertex in vertices if colors[vertex] == 1),
            )
        )
    return tuple(components)


def _homomorphism_count(source: Graph, target: Graph) -> int:
    if source.n == 0:
        return 1
    if target.n == 0:
        return 0
    source_adjacency = source.adjacency
    target_adjacency = target.adjacency
    components = _bipartition_components(source)
    if components is not None:
        enumerated: list[int] = []
        factored: list[int] = []
        for left, right in components:
            if len(left) <= len(right):
                enumerated.extend(left)
                factored.extend(right)
            else:
                enumerated.extend(right)
                factored.extend(left)
        positions = [-1] * source.n
        for index, vertex in enumerate(enumerated):
            positions[vertex] = index
        all_targets = (1 << target.n) - 1
        total = 0
        for images in itertools.product(
            range(target.n), repeat=len(enumerated)
        ):
            _check_predicate_deadline()
            extensions = 1
            for vertex in factored:
                common = all_targets
                neighbors = source_adjacency[vertex]
                while neighbors and common:
                    bit = neighbors & -neighbors
                    neighbors ^= bit
                    position = positions[bit.bit_length() - 1]
                    common &= target_adjacency[images[position]]
                extensions *= common.bit_count()
                if not extensions:
                    break
            total += extensions
        return total

    order = sorted(
        range(source.n),
        key=lambda vertex: source_adjacency[vertex].bit_count(),
        reverse=True,
    )
    mapping = [-1] * source.n

    def visit(index: int) -> int:
        _check_predicate_deadline()
        if index == source.n:
            return 1
        vertex = order[index]
        count = 0
        for image in range(target.n):
            if all(
                mapping[other] < 0
                or not source_adjacency[vertex] & (1 << other)
                or target_adjacency[image] & (1 << mapping[other])
                for other in order[:index]
            ):
                mapping[vertex] = image
                count += visit(index + 1)
        mapping[vertex] = -1
        return count

    return visit(0)


def _sidorenko_violation(source: Graph, target: Graph) -> dict[str, Any] | None:
    if target.n == 0 or not _is_bipartite(source):
        return None
    homomorphisms = _homomorphism_count(source, target)
    source_edges = len(source.edges)
    target_edges = len(target.edges)
    left_value = homomorphisms * target.n ** (2 * source_edges)
    right_value = (2 * target_edges) ** source_edges * target.n ** source.n
    if left_value <= right_value:
        if left_value == right_value:
            return None
        return {
            "homomorphism_count": homomorphisms,
            "source_edge_count": source_edges,
            "target_edge_count": target_edges,
            "left_integer_product": left_value,
            "right_integer_product": right_value,
        }
    return None


def _bipartition_sizes(graph: Graph) -> tuple[int, int] | None:
    components = _bipartition_components(graph)
    if graph.n == 0 or components is None or len(components) != 1:
        return None
    left, right = components[0]
    counts = (len(left), len(right))
    return min(counts), max(counts)


def _sidorenko_known_frontier_exceeded(source: Graph) -> bool:
    sides = _bipartition_sizes(source)
    if source.n < 10 or sides is None or sides[0] < 5:
        return False
    return _sidorenko_filtered_family(source) is None


def _counterexample(
    spec: Mapping[str, Any], graph: Graph, parameters: Mapping[str, Any]
) -> dict[str, Any] | None:
    kind = spec["kind"]
    adjacency = graph.adjacency
    degrees = [row.bit_count() for row in adjacency]
    delta = max(degrees, default=0)
    detail: dict[str, Any] = {}
    premise = False
    conclusion = True

    if kind == "flow4":
        premise = graph.n < 10 and _bridgeless(graph)
        conclusion = not premise or _nowhere_zero_flow(graph, 4)
    elif kind == "flow3":
        premise = _edge_connectivity(graph) >= 4
        conclusion = not premise or _nowhere_zero_flow(graph, 3)
    elif kind == "modular_orientation":
        k = int(parameters.get("k", 1))
        premise = k > 0 and _edge_connectivity(graph) >= 4 * k
        conclusion = not premise or _modular_orientation(graph, k)
        detail["k"] = k
    elif kind == "petersen_coloring":
        premise = graph.n > 0 and set(degrees) == {3} and _bridgeless(graph)
        conclusion = not premise or _petersen_coloring(graph)
    elif kind == "jorgensen":
        sufficiently_connected = _vertex_connectivity_at_least(graph, 6)
        apex_vertices = (
            [
                vertex
                for vertex in range(graph.n)
                if _is_planar(_delete_vertex(graph, vertex))
            ]
            if sufficiently_connected
            else []
        )
        # Any apex graph is K6-minor-free: the other five branch sets would
        # otherwise give a K5 minor in its planar vertex deletion.
        excludes_minor = bool(apex_vertices) or (
            sufficiently_connected and not _has_complete_minor(graph, 6)
        )
        premise = sufficiently_connected and excludes_minor
        conclusion = not premise or bool(apex_vertices)
        detail["apex_vertices"] = apex_vertices
    elif kind == "vertex_transitive_hamiltonian":
        premise = _vertex_transitive(graph)
        conclusion = not premise or _has_hamiltonian_path(graph)
    elif kind == "strong_colorability":
        premise = delta >= 1
        conclusion = not premise or _strongly_colorable(graph)
    elif kind == "uniform_forest_negative_association":
        premise = True
        violation = _uniform_forest_violation(graph)
        conclusion = violation is None
        if violation is not None:
            detail.update(violation)
    elif kind == "goldberg":
        premise = True
        overfull = _overfull_parameter(graph)
        bound = max(delta + 1, overfull)
        conclusion = _edge_coloring(graph, bound)
        detail.update({"overfull_parameter": overfull, "bound": bound})
    elif kind == "reed":
        premise = True
        omega = max((item.bit_count() for item in _cliques(graph)), default=0)
        chi = _chromatic_number(graph)
        bound = (delta + 1 + omega + 1) // 2
        conclusion = chi <= bound
        detail.update({"chromatic_number": chi, "clique_number": omega, "bound": bound})
    elif kind == "triangle_free_chromatic":
        premise = not any(len(cycle) == 3 for cycle in _cycles(graph))
        chi = _chromatic_number(graph) if premise else 0
        bound = (delta + 1) // 2 + 2
        conclusion = not premise or chi <= bound
        detail.update({"chromatic_number": chi, "bound": bound})
    elif kind == "cubic_domination":
        premise = set(degrees) == {3} and _vertex_connectivity_at_least(graph, 3)
        domination = _domination_number(graph) if premise else 0
        bound = (graph.n + 2) // 3
        conclusion = not premise or domination <= bound
        detail.update({"domination_number": domination, "bound": bound})
    elif kind == "oddness":
        cubic_bridgeless = (
            _connected(graph)
            and set(degrees) == {3}
            and _bridgeless(graph)
        )
        matchings = _perfect_matchings(graph) if cubic_bridgeless else []
        factor_lengths = [
            _two_factor_cycle_lengths(graph, matching)
            for matching in matchings
        ]
        premise = cubic_bridgeless and bool(factor_lengths) and all(
            all(length % 2 for length in lengths)
            for lengths in factor_lengths
        )
        oddness = min(
            (sum(length % 2 for length in lengths) for lengths in factor_lengths),
            default=0,
        )
        conclusion = not premise or oddness <= 2
        detail["oddness"] = oddness
    elif kind == "forcing_k6_minor":
        premise = min(degrees, default=0) >= 7 or _vertex_connectivity_at_least(
            graph, 7
        )
        conclusion = not premise or _has_complete_minor(graph, 6)
    elif kind == "barnette":
        premise = (
            set(degrees) == {3}
            and _vertex_connectivity_at_least(graph, 3)
            and _is_planar(graph)
            and _is_bipartite(graph)
        )
        conclusion = not premise or _hamiltonian_cycle_count(graph, 1) >= 1
    elif kind == "planar_cycle_packing":
        premise = _is_planar(graph)
        packing, feedback = (
            _planar_cycle_parameters(graph) if premise else (0, 0)
        )
        conclusion = not premise or feedback <= 2 * packing
        detail.update(
            {
                "cycle_packing_number": packing,
                "feedback_vertex_number": feedback,
                "bound": 2 * packing,
            }
        )
    elif kind == "planar_odd_cycle_hom":
        girth = _girth(graph)
        eligible = (
            [
                k
                for k in _bounded_k_values(parameters)
                if girth >= 4 * k
            ]
            if _is_planar(graph)
            else []
        )
        premise = bool(eligible)
        conclusion = True
        for k in eligible:
            if not _hom_to_cycle(graph, 2 * k + 1):
                conclusion = False
                detail.update(
                    {
                        "k": k,
                        "girth": girth,
                        "target_cycle_order": 2 * k + 1,
                        "tested_k_values": list(
                            _bounded_k_values(parameters)
                        ),
                    }
                )
                break
    elif kind == "seagull_minor":
        premise = not _has_independent_triple(graph)
        target_order = (graph.n + 1) // 2
        conclusion = (
            not premise or _has_complete_minor(graph, target_order)
        )
        detail.update(
            {
                "target_complete_minor_order": target_order,
                "vertex_count": graph.n,
            }
        )
    elif kind == "weak_pentagon":
        premise = set(degrees) == {3} and not any(len(cycle) == 3 for cycle in _cycles(graph))
        conclusion = not premise or _weak_pentagon_coloring(graph)
    elif kind == "strong_edge_coloring":
        premise = True
        bound = (
            (5 * delta * delta) // 4
            if delta % 2 == 0
            else (5 * delta * delta - 2 * delta + 1) // 4
        )
        conclusion = _colorable(_edge_conflict_graph(graph, strong=True), bound)
        detail["bound"] = bound
    elif kind == "path_decomposition":
        premise = _connected(graph)
        bound = (graph.n + 1) // 2
        conclusion = not premise or _has_path_decomposition(graph, bound)
        detail["bound"] = bound
    elif kind == "cycle_decomposition":
        premise = _connected(graph) and all(degree % 2 == 0 for degree in degrees)
        bound = (graph.n - 1) // 2
        conclusion = not premise or _has_cycle_decomposition(graph, bound)
        detail["bound"] = bound
    elif kind == "p3_partition":
        premise = (
            graph.n % 3 == 0
            and set(degrees) == {3}
            and _vertex_connectivity_at_least(graph, 3)
        )
        conclusion = not premise or _has_p3_partition(graph)
    elif kind == "regular_hamiltonian":
        premise = bool(degrees) and len(set(degrees)) == 1 and degrees[0] > 2
        count = _hamiltonian_cycle_count(graph, 2) if premise else 0
        conclusion = not premise or count != 1
        detail["hamiltonian_cycle_count_capped_at_two"] = count
    elif kind == "matching_intersection":
        premise = set(degrees) == {3} and _bridgeless(graph)
        matchings = _perfect_matchings(graph) if premise else []
        conclusion = not premise or any(
            not _contains_odd_edge_cut(graph, first & second)
            for first in matchings
            for second in matchings
        )
        detail["perfect_matching_count"] = len(matchings)
    elif kind == "max_clique_two_color":
        premise = bool(graph.edges) and not _induced_odd_hole(graph)
        conclusion = not premise or _max_clique_two_colorable(graph)
    elif kind == "modular_cycles":
        k = int(parameters.get("k", 3))
        chi = _chromatic_number(graph)
        premise = k > 0 and chi > k
        count = sum(len(cycle) % k == 0 for cycle in _cycles(graph))
        bound = ((k + 1) * _factorial(k - 1) + 1) // 2
        conclusion = not premise or count >= bound
        detail.update({"k": k, "chromatic_number": chi, "cycle_count": count, "bound": bound})
    elif kind == "three_decomposition":
        premise = _connected(graph) and set(degrees) == {3}
        conclusion = not premise or _three_decomposition(graph)
    elif kind == "prescribed_cycle_double_cover":
        premise = set(degrees) == {3} and _vertex_connectivity_at_least(graph, 2)
        conclusion = True
        bad_s = None
        if premise:
            two_regular = []
            sub = graph.mask
            while sub:
                rows = Graph(graph.n, sub).adjacency
                if all(row.bit_count() in {0, 2} for row in rows) and any(
                    row.bit_count() == 2 for row in rows
                ):
                    two_regular.append(sub)
                sub = (sub - 1) & graph.mask
            for selected in two_regular:
                if not _connected(Graph(graph.n, graph.mask & ~selected)):
                    continue
                required = tuple(
                    _cycle_edge_mask(graph, cycle)
                    for cycle in _cycles(Graph(graph.n, selected))
                    if _cycle_edge_mask(graph, cycle) & selected
                    == _cycle_edge_mask(graph, cycle)
                )
                if not _cycle_double_cover(graph, required):
                    conclusion = False
                    bad_s = selected
                    break
        detail["prescribed_2_regular_edge_mask"] = bad_s
    elif kind == "edge_color_after_deletion":
        premise = (
            graph.n > 2
            and _connected(graph)
            and set(degrees) == {3}
            and _edge_coloring(graph, 3)
        )
        conclusion = not premise
        if premise:
            for deleted_edge in graph.edges:
                vertices, multiedges = _suppressed_after_edge_deletion(
                    graph, deleted_edge
                )
                if _multigraph_edge_colorable(vertices, multiedges, 3):
                    conclusion = True
                    break
    elif kind == "fractional_power":
        premise = delta >= 2
        powered = _fractional_three_power(graph) if premise else Graph(0, 0)
        bound = 2 * delta + 1
        conclusion = not premise or _colorable(powered, bound)
        detail.update({"powered_vertex_count": powered.n, "bound": bound})
    elif kind == "total_coloring":
        premise = True
        bound = delta + 2
        conclusion = _colorable(_edge_conflict_graph(graph, strong=False, total=True), bound)
        detail["bound"] = bound
    elif kind == "strongly_regular_core":
        parameters_value = _strongly_regular_parameters(graph)
        premise = parameters_value is not None
        conclusion = not premise or _core_is_graph_or_complete(graph)
        detail["strongly_regular_parameters"] = parameters_value
    elif kind == "r_graph_coloring":
        r = _r_graph(graph)
        premise = r is not None
        conclusion = not premise or _edge_coloring(graph, int(r) + 1)
        detail["r"] = r
    else:
        raise AssertionError(f"unimplemented registered model: {kind}")

    if premise and not conclusion:
        return detail
    return None


@lru_cache(maxsize=None)
def _factorial(value: int) -> int:
    result = 1
    for item in range(2, value + 1):
        result *= item
    return result


def _semantic_premise_check(
    spec: Mapping[str, Any], graph: Graph, parameters: Mapping[str, Any]
) -> bool:
    """Recheck the natural-language premise independently from search routing."""
    kind = spec["kind"]
    degrees = [row.bit_count() for row in graph.adjacency]
    delta = max(degrees, default=0)
    if kind == "flow4":
        return graph.n < 10 and _bridgeless(graph)
    if kind == "flow3":
        return _edge_connectivity(graph) >= 4
    if kind == "modular_orientation":
        k = int(parameters.get("k", 1))
        return k > 0 and _edge_connectivity(graph) >= 4 * k
    if kind == "petersen_coloring":
        return graph.n > 0 and set(degrees) == {3} and _bridgeless(graph)
    if kind == "jorgensen":
        if not _vertex_connectivity_at_least(graph, 6):
            return False
        if any(
            _is_planar(_delete_vertex(graph, vertex))
            for vertex in range(graph.n)
        ):
            return True
        return not _has_complete_minor(graph, 6)
    if kind == "vertex_transitive_hamiltonian":
        return _vertex_transitive(graph)
    if kind == "strong_colorability":
        return delta >= 1
    if kind == "uniform_forest_negative_association":
        return True
    if kind in {"goldberg", "reed", "strong_edge_coloring", "total_coloring"}:
        return graph.n >= 1
    if kind == "triangle_free_chromatic":
        return not any(len(cycle) == 3 for cycle in _cycles(graph))
    if kind == "cubic_domination":
        return set(degrees) == {3} and _vertex_connectivity_at_least(graph, 3)
    if kind == "oddness":
        if (
            not _connected(graph)
            or set(degrees) != {3}
            or not _bridgeless(graph)
        ):
            return False
        factors = [
            _two_factor_cycle_lengths(graph, matching)
            for matching in _perfect_matchings(graph)
        ]
        return (
            bool(factors)
            and all(all(length % 2 for length in factor) for factor in factors)
        )
    if kind == "forcing_k6_minor":
        return min(degrees, default=0) >= 7 or _vertex_connectivity_at_least(
            graph, 7
        )
    if kind == "barnette":
        return (
            set(degrees) == {3}
            and _vertex_connectivity_at_least(graph, 3)
            and _is_planar(graph)
            and _is_bipartite(graph)
        )
    if kind == "planar_cycle_packing":
        return _is_planar(graph)
    if kind == "planar_odd_cycle_hom":
        if not _is_planar(graph):
            return False
        girth = _girth(graph)
        return any(
            girth >= 4 * k for k in _bounded_k_values(parameters)
        )
    if kind == "seagull_minor":
        return not _has_independent_triple(graph)
    if kind == "weak_pentagon":
        return set(degrees) == {3} and not any(
            len(cycle) == 3 for cycle in _cycles(graph)
        )
    if kind == "path_decomposition":
        return _connected(graph)
    if kind == "cycle_decomposition":
        return _connected(graph) and all(degree % 2 == 0 for degree in degrees)
    if kind == "p3_partition":
        return (
            graph.n % 3 == 0
            and set(degrees) == {3}
            and _vertex_connectivity_at_least(graph, 3)
        )
    if kind == "regular_hamiltonian":
        return bool(degrees) and len(set(degrees)) == 1 and degrees[0] > 2
    if kind == "matching_intersection":
        return set(degrees) == {3} and _bridgeless(graph)
    if kind == "max_clique_two_color":
        return bool(graph.edges) and not _induced_odd_hole(graph)
    if kind == "modular_cycles":
        k = int(parameters.get("k", 3))
        return k > 0 and _chromatic_number(graph) > k
    if kind == "three_decomposition":
        return _connected(graph) and set(degrees) == {3}
    if kind == "prescribed_cycle_double_cover":
        return set(degrees) == {3} and _vertex_connectivity_at_least(graph, 2)
    if kind == "edge_color_after_deletion":
        return (
            graph.n > 2
            and _connected(graph)
            and set(degrees) == {3}
            and _edge_coloring(graph, 3)
        )
    if kind == "fractional_power":
        return delta >= 2
    if kind == "strongly_regular_core":
        return _strongly_regular_parameters(graph) is not None
    if kind == "r_graph_coloring":
        return _r_graph(graph) is not None
    raise AssertionError(f"missing semantic premise checker for {kind}")


def _budget_dict(budget: Any, defaults: Mapping[str, Any]) -> dict[str, Any]:
    if hasattr(budget, "as_dict"):
        raw = dict(budget.as_dict())
    elif isinstance(budget, Mapping):
        raw = dict(budget)
    else:
        raise TypeError("budget must be a StrategyBudget or mapping")
    parameters = dict(defaults)
    parameters.update(dict(raw.get("parameters") or {}))
    for key in defaults:
        if key in raw and raw[key] is not None:
            parameters[key] = raw[key]
    parameters["time_seconds"] = int(raw.get("time_seconds", parameters.get("time_seconds", 30)))
    parameters["max_cases"] = int(raw.get("max_cases") or parameters.get("max_cases", 10_000))
    parameters["max_vertices"] = int(parameters.get("max_vertices", 6))
    for key in ("max_h_vertices", "max_g_vertices"):
        if key in parameters:
            parameters[key] = int(parameters[key])
    if (
        parameters["time_seconds"] <= 0
        or parameters["max_cases"] <= 0
        or parameters["max_vertices"] <= 0
        or any(
            int(parameters[key]) <= 0
            for key in ("max_h_vertices", "max_g_vertices")
            if key in parameters
        )
    ):
        raise ValueError("time_seconds, max_cases, and max_vertices must be positive")
    return parameters


@lru_cache(maxsize=1)
def _tool_versions() -> dict[str, str]:
    nauty = "unavailable"
    if NAUTY_BIN.is_file():
        completed = subprocess.run(
            [str(NAUTY_BIN), "-help"],
            capture_output=True,
            text=True,
            env=_nauty_env(),
        )
        lines = [
            line.strip()
            for line in (completed.stderr or completed.stdout).splitlines()
            if line.strip()
        ]
        nauty = lines[0] if lines else "nauty-geng present"
    return {
        "python": platform.python_version(),
        "nauty_geng": nauty,
        "executor": EXECUTOR_VERSION,
    }


def _result(
    spec: Mapping[str, Any],
    *,
    outcome: str,
    candidate: dict[str, Any] | None,
    checked_cases: int,
    stop_reason: str,
    next_case: int,
    strategy_id: str,
    bounds: Mapping[str, Any],
    generated_cases: int | None = None,
    premise_cases: int = 0,
    replayed_cases: int = 0,
    checkpoint_extra: Mapping[str, Any] | None = None,
    metrics_extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    generated = checked_cases if generated_cases is None else generated_cases
    checkpoint_payload = {
        "next_case": next_case,
        "strategy_id": strategy_id,
        "bounds": dict(bounds),
        **dict(checkpoint_extra or {}),
    }
    metrics = {
        "generated_cases": generated,
        "premise_cases": premise_cases,
        "replayed_cases": replayed_cases,
    }
    if spec.get("kind") == "sidorenko":
        metrics.update(
            {
                "pair_cases": generated,
                "premise_pair_cases": premise_cases,
            }
        )
    metrics.update(dict(metrics_extra or {}))
    return {
        "outcome": outcome,
        "candidate": candidate,
        "checked_cases": checked_cases,
        "stop_reason": stop_reason,
        "checkpoint": checkpoint_payload,
        "model_contract": dict(spec["model_contract"]),
        "tool_versions": _tool_versions(),
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "strategy_id": strategy_id,
        "bounds": dict(bounds),
        "metrics": metrics,
    }


def _serialize_edge_reconstruction_state(
    decks: Mapping[tuple[int, tuple[int, ...]], Graph],
    replay_next_case: int,
) -> dict[str, Any]:
    return {
        "edge_reconstruction_state": {
            "version": 1,
            "replay_next_case": replay_next_case,
            "decks": [
                {
                    "vertex_count": order,
                    "canonical_edge_deck": list(deck),
                    "representative_edge_mask": graph.mask,
                }
                for (order, deck), graph in sorted(decks.items())
            ],
        }
    }


def _load_edge_reconstruction_state(
    checkpoint: Mapping[str, Any] | None,
    start: int,
) -> tuple[dict[tuple[int, tuple[int, ...]], Graph], int]:
    try:
        raw = dict((checkpoint or {}).get("edge_reconstruction_state") or {})
        if raw.get("version") != 1:
            return {}, 0
        replay_next = int(raw.get("replay_next_case", 0))
        if not 0 <= replay_next <= start:
            return {}, 0
        decks: dict[tuple[int, tuple[int, ...]], Graph] = {}
        for entry in raw.get("decks") or []:
            order = int(entry["vertex_count"])
            deck = tuple(int(item) for item in entry["canonical_edge_deck"])
            graph = Graph(order, int(entry["representative_edge_mask"]))
            decks[(order, deck)] = graph
    except (KeyError, TypeError, ValueError, OverflowError):
        return {}, 0
    return decks, replay_next


def _run_sidorenko_search(
    spec: Mapping[str, Any],
    pairs: Iterable[tuple[Graph, Graph]],
    *,
    start: int,
    maximum: int,
    deadline: float,
    strategy_id: str,
    internal_strategy: str,
    cursor_offset: int,
    bounds: Mapping[str, Any],
    progress: Callable[[dict[str, Any], int], None] | None,
) -> dict[str, Any]:
    checked = 0
    next_case = start
    premise_cases = 0
    max_h_order_seen = 0
    max_g_order_seen = 0
    max_h_edge_count_seen = 0
    known_frontier_exceeded = False
    filtered_family_source_cases = 0
    general_source_cases = 0

    def frontier_metrics() -> dict[str, Any]:
        return {
            "max_h_order_seen": max_h_order_seen,
            "max_g_order_seen": max_g_order_seen,
            "max_h_edge_count_seen": max_h_edge_count_seen,
            "known_frontier_exceeded": known_frontier_exceeded,
            "filtered_family_source_cases": filtered_family_source_cases,
            "general_source_cases": general_source_cases,
        }

    for cursor, (source, target) in enumerate(pairs, start=cursor_offset):
        if cursor < start:
            if time.monotonic() >= deadline:
                return _result(
                    spec,
                    outcome="inconclusive",
                    candidate=None,
                    checked_cases=checked,
                    stop_reason="time_budget_exhausted_during_prefix_skip",
                    next_case=start,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    premise_cases=premise_cases,
                    metrics_extra=frontier_metrics(),
                )
            continue
        if checked >= maximum:
            return _result(
                spec,
                outcome="inconclusive",
                candidate=None,
                checked_cases=checked,
                stop_reason="max_cases_exhausted",
                next_case=next_case,
                strategy_id=strategy_id,
                bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=frontier_metrics(),
            )
        if time.monotonic() >= deadline:
            return _result(
                spec,
                outcome="inconclusive",
                candidate=None,
                checked_cases=checked,
                stop_reason="time_budget_exhausted",
                next_case=next_case,
                strategy_id=strategy_id,
                bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=frontier_metrics(),
            )
        max_h_order_seen = max(max_h_order_seen, source.n)
        max_g_order_seen = max(max_g_order_seen, target.n)
        max_h_edge_count_seen = max(
            max_h_edge_count_seen, len(source.edges)
        )
        known_frontier_exceeded = (
            known_frontier_exceeded
            or _sidorenko_known_frontier_exceeded(source)
        )
        if _sidorenko_filtered_family(source) is None:
            general_source_cases += 1
        else:
            filtered_family_source_cases += 1
        try:
            with _predicate_budget(deadline):
                semantic_premise = (
                    target.n > 0 and _is_bipartite(source)
                )
                detail = _sidorenko_violation(source, target)
                direct_detail = None
                direct_premise = False
                if detail is not None:
                    serialized_source = Graph(source.n, source.mask)
                    serialized_target = Graph(target.n, target.mask)
                    direct_premise = (
                        serialized_target.n > 0
                        and _is_bipartite(serialized_source)
                    )
                    direct_detail = _sidorenko_violation(
                        serialized_source, serialized_target
                    )
        except _PredicateTimeout:
            return _result(
                spec,
                outcome="inconclusive",
                candidate=None,
                checked_cases=checked,
                stop_reason="predicate_time_budget_exhausted",
                next_case=cursor,
                strategy_id=strategy_id,
                bounds=bounds,
                generated_cases=checked + 1,
                premise_cases=premise_cases,
                metrics_extra=frontier_metrics(),
            )
        checked += 1
        next_case = cursor + 1
        premise_cases += int(semantic_premise)
        if detail is not None:
            if direct_detail is None or not direct_premise:
                return _result(
                    spec,
                    outcome="inconclusive",
                    candidate=None,
                    checked_cases=checked,
                    stop_reason="candidate_failed_semantic_verification",
                    next_case=next_case,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    premise_cases=premise_cases,
                    metrics_extra=frontier_metrics(),
                )
            candidate = {
                "bipartite_graph_h": source.certificate(),
                "target_graph_g": target.certificate(),
                "predicate_details": detail,
                "direct_verification": {
                    "accepted": True,
                    "engine": "same_executor_sidorenko_integer_replay.v1",
                    "semantic_premise_rechecked": direct_premise,
                    "details": direct_detail,
                },
            }
            return _result(
                spec,
                outcome="candidate",
                candidate=candidate,
                checked_cases=checked,
                stop_reason="candidate_found",
                next_case=next_case,
                strategy_id=strategy_id,
                bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=frontier_metrics(),
            )
        if progress and checked % 100 == 0:
            progress({"next_case": next_case}, checked)
    outcome = (
        "no_candidate"
        if internal_strategy == "exact-small"
        else "inconclusive"
    )
    stop_reason = (
        "finite_bound_exhausted"
        if internal_strategy == "exact-small"
        else "targeted_sample_exhausted"
    )
    return _result(
        spec,
        outcome=outcome,
        candidate=None,
        checked_cases=checked,
        stop_reason=stop_reason,
        next_case=next_case,
        strategy_id=strategy_id,
        bounds=bounds,
        premise_cases=premise_cases,
        metrics_extra=frontier_metrics(),
    )


def _run_edge_reconstruction(
    spec: Mapping[str, Any],
    graphs: Iterable[Graph],
    *,
    start: int,
    maximum: int,
    deadline: float,
    strategy_id: str,
    bounds: Mapping[str, Any],
    progress: Callable[[dict[str, Any], int], None] | None,
    checkpoint: Mapping[str, Any] | None,
) -> dict[str, Any]:
    decks, replay_next = _load_edge_reconstruction_state(checkpoint, start)
    checked = 0
    next_case = start
    premise_cases = 0
    replayed = 0

    def checkpoint_state() -> dict[str, Any]:
        return _serialize_edge_reconstruction_state(decks, replay_next)

    for cursor, graph in enumerate(graphs):
        if cursor < start:
            if time.monotonic() >= deadline:
                return _result(
                    spec,
                    outcome="inconclusive",
                    candidate=None,
                    checked_cases=0,
                    stop_reason="time_budget_exhausted_during_prefix_skip",
                    next_case=start,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    generated_cases=0,
                    replayed_cases=replayed,
                    checkpoint_extra=checkpoint_state(),
                )
            if cursor < replay_next:
                continue
            candidate = None
            try:
                with _predicate_budget(deadline):
                    if len(graph.edges) >= 4:
                        key = (graph.n, _edge_deck(graph))
                        other = decks.get(key)
                        if (
                            other is not None
                            and _canonical_mask(other) != _canonical_mask(graph)
                        ):
                            candidate = {
                                "graph_a": other.certificate(),
                                "graph_b": graph.certificate(),
                                "canonical_edge_deck": list(key[1]),
                                "verification": {
                                    "direct": (
                                        _edge_deck(other) == _edge_deck(graph)
                                    ),
                                    "nonisomorphic": (
                                        _canonical_mask(other)
                                        != _canonical_mask(graph)
                                    ),
                                },
                            }
                        decks[key] = graph
            except _PredicateTimeout:
                return _result(
                    spec,
                    outcome="inconclusive",
                    candidate=None,
                    checked_cases=0,
                    stop_reason="predicate_time_budget_exhausted",
                    next_case=start,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    generated_cases=0,
                    replayed_cases=replayed,
                    checkpoint_extra=checkpoint_state(),
                )
            replay_next = cursor + 1
            replayed += 1
            if candidate is not None:
                return _result(
                    spec,
                    outcome="candidate",
                    candidate=candidate,
                    checked_cases=0,
                    stop_reason="candidate_found_during_replay",
                    next_case=cursor + 1,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    generated_cases=0,
                    premise_cases=0,
                    replayed_cases=replayed,
                    checkpoint_extra=checkpoint_state(),
                )
            continue
        if checked >= maximum:
            return _result(
                spec, outcome="inconclusive", candidate=None, checked_cases=checked,
                stop_reason="max_cases_exhausted", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases, replayed_cases=replayed,
                checkpoint_extra=checkpoint_state(),
            )
        if time.monotonic() >= deadline:
            return _result(
                spec, outcome="inconclusive", candidate=None, checked_cases=checked,
                stop_reason="time_budget_exhausted", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases, replayed_cases=replayed,
                checkpoint_extra=checkpoint_state(),
            )
        eligible = len(graph.edges) >= 4
        candidate = None
        try:
            with _predicate_budget(deadline):
                if eligible:
                    key = (graph.n, _edge_deck(graph))
                    other = decks.get(key)
                    if (
                        other is not None
                        and _canonical_mask(other) != _canonical_mask(graph)
                    ):
                        candidate = {
                            "graph_a": other.certificate(),
                            "graph_b": graph.certificate(),
                            "canonical_edge_deck": list(key[1]),
                            "verification": {
                                "direct": _edge_deck(other) == _edge_deck(graph),
                                "nonisomorphic": (
                                    _canonical_mask(other)
                                    != _canonical_mask(graph)
                                ),
                            },
                        }
                    decks[key] = graph
        except _PredicateTimeout:
            return _result(
                spec,
                outcome="inconclusive",
                candidate=None,
                checked_cases=checked,
                stop_reason="predicate_time_budget_exhausted",
                next_case=cursor,
                strategy_id=strategy_id,
                bounds=bounds,
                generated_cases=checked + 1,
                premise_cases=premise_cases,
                replayed_cases=replayed,
                checkpoint_extra=checkpoint_state(),
            )
        checked += 1
        next_case = cursor + 1
        replay_next = next_case
        premise_cases += int(eligible)
        if candidate is not None:
            return _result(
                spec, outcome="candidate", candidate=candidate, checked_cases=checked,
                stop_reason="candidate_found", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases, replayed_cases=replayed,
                checkpoint_extra=checkpoint_state(),
            )
        if progress and checked % 100 == 0:
            progress({"next_case": next_case}, checked)
    return _result(
        spec, outcome="no_candidate", candidate=None, checked_cases=checked,
        stop_reason="finite_bound_exhausted", next_case=next_case,
        strategy_id=strategy_id, bounds=bounds,
        premise_cases=premise_cases, replayed_cases=replayed,
        checkpoint_extra=checkpoint_state(),
    )


def run_second_batch_graph_search(
    problem_id: str,
    *,
    strategy_id: str,
    budget: Any,
    seed: int,
    checkpoint: Mapping[str, Any] | None = None,
    progress: Callable[[dict[str, Any], int], None] | None = None,
) -> dict[str, Any]:
    aliases = {spec["source_id"]: key for key, spec in _SPEC_BY_ID.items()}
    normalized = aliases.get(problem_id, problem_id)
    if normalized not in _SPEC_BY_ID:
        raise KeyError(f"second-batch graph executor is not registered for {problem_id}")
    spec = _SPEC_BY_ID[normalized]
    strategy_aliases = {
        "screen-exact": "exact-small",
        "deep-diversified": "targeted",
        "deep-exact": "exact-small",
    }
    internal_strategy = strategy_aliases.get(strategy_id, strategy_id)
    if internal_strategy not in spec["strategies"]:
        raise ValueError(
            f"strategy {strategy_id!r} is not supported for {normalized}; "
            f"choose from {spec['strategies']}"
        )
    defaults = (
        spec["deep_bounds"]
        if internal_strategy in {"targeted", "deep-exact"}
        else spec["default_bounds"]
    )
    bounds = _budget_dict(budget, defaults)
    start = int((checkpoint or {}).get("next_case", 0))
    maximum = int(bounds["max_cases"])
    deadline = time.monotonic() + int(bounds["time_seconds"])
    max_vertices = int(bounds["max_vertices"])

    if max_vertices > int(spec["supported_max_vertices"]):
        return _result(
            spec,
            outcome="inconclusive",
            candidate=None,
            checked_cases=0,
            stop_reason="unsupported_exact_bound",
            next_case=start,
            strategy_id=strategy_id,
            bounds=bounds,
            generated_cases=0,
        )

    if spec["kind"] == "sidorenko":
        max_h_vertices = int(bounds.get("max_h_vertices", max_vertices))
        max_g_vertices = int(bounds.get("max_g_vertices", max_vertices))
        pairs = (
            _iter_sidorenko_exact_pairs(max_h_vertices, max_g_vertices)
            if internal_strategy == "exact-small"
            else _iter_sidorenko_targeted_pairs(
                max_h_vertices,
                max_g_vertices,
                int(seed),
                maximum,
                start=start,
            )
        )
        return _run_sidorenko_search(
            spec,
            pairs,
            start=start,
            maximum=maximum,
            deadline=deadline,
            strategy_id=strategy_id,
            internal_strategy=internal_strategy,
            cursor_offset=(
                0 if internal_strategy == "exact-small" else start
            ),
            bounds=bounds,
            progress=progress,
        )

    if internal_strategy == "exact-small":
        cursor_offset = 0
        try:
            graphs: Iterable[Graph] = _iter_nauty_graphs(max_vertices)
        except FileNotFoundError:
            return _result(
                spec, outcome="inconclusive", candidate=None, checked_cases=0,
                stop_reason="nauty_unavailable", next_case=start,
                strategy_id=strategy_id, bounds=bounds,
            )
    else:
        cursor_offset = start
        graphs = _iter_targeted_graphs(
            spec,
            max_vertices,
            int(seed),
            maximum,
            start=start,
        )

    if spec["kind"] == "edge_reconstruction":
        return _run_edge_reconstruction(
            spec, graphs, start=start, maximum=maximum, deadline=deadline,
            strategy_id=strategy_id, bounds=bounds, progress=progress,
            checkpoint=checkpoint,
        )

    checked = 0
    next_case = start
    premise_cases = 0
    parameters = dict(bounds)
    max_graph_order_seen = 0
    max_graph_edge_count_seen = 0
    known_frontier_exceeded = False
    frontier_premise_cases = 0

    def search_metrics() -> dict[str, Any]:
        if spec["kind"] not in {
            "uniform_forest_negative_association",
            "planar_odd_cycle_hom",
            "seagull_minor",
        }:
            return {}
        return {
            "max_graph_order_seen": max_graph_order_seen,
            "max_graph_edge_count_seen": max_graph_edge_count_seen,
            "known_frontier_exceeded": known_frontier_exceeded,
            "frontier_premise_cases": frontier_premise_cases,
        }

    for cursor, graph in enumerate(graphs, start=cursor_offset):
        if cursor < start:
            if time.monotonic() >= deadline:
                return _result(
                    spec,
                    outcome="inconclusive",
                    candidate=None,
                    checked_cases=checked,
                    stop_reason="time_budget_exhausted_during_prefix_skip",
                    next_case=start,
                    strategy_id=strategy_id,
                    bounds=bounds,
                    premise_cases=premise_cases,
                    metrics_extra=search_metrics(),
                )
            continue
        if checked >= maximum:
            return _result(
                spec, outcome="inconclusive", candidate=None, checked_cases=checked,
                stop_reason="max_cases_exhausted", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=search_metrics(),
            )
        if time.monotonic() >= deadline:
            return _result(
                spec, outcome="inconclusive", candidate=None, checked_cases=checked,
                stop_reason="time_budget_exhausted", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=search_metrics(),
            )
        if spec["kind"] in {
            "uniform_forest_negative_association",
            "planar_odd_cycle_hom",
            "seagull_minor",
        }:
            edge_count = len(graph.edges)
            max_graph_order_seen = max(max_graph_order_seen, graph.n)
            max_graph_edge_count_seen = max(
                max_graph_edge_count_seen, edge_count
            )
        if spec["kind"] == "uniform_forest_negative_association":
            known_frontier_exceeded = (
                known_frontier_exceeded
                or (graph.n >= 9 and edge_count > 18)
            )
        direct_detail = None
        direct_semantic_premise = False
        try:
            with _predicate_budget(deadline):
                semantic_premise = _semantic_premise_check(
                    spec, graph, parameters
                )
                detail = _counterexample(spec, graph, parameters)
                if detail is not None:
                    serialized = Graph(graph.n, graph.mask)
                    direct_detail = _counterexample(spec, serialized, parameters)
                    direct_semantic_premise = _semantic_premise_check(
                        spec, serialized, parameters
                    )
        except _PredicateTimeout:
            return _result(
                spec,
                outcome="inconclusive",
                candidate=None,
                checked_cases=checked,
                stop_reason="predicate_time_budget_exhausted",
                next_case=cursor,
                strategy_id=strategy_id,
                bounds=bounds,
                generated_cases=checked + 1,
                premise_cases=premise_cases,
                metrics_extra=search_metrics(),
            )
        checked += 1
        next_case = cursor + 1
        premise_cases += int(semantic_premise)
        is_frontier_premise = semantic_premise and (
            (
                spec["kind"] == "planar_odd_cycle_hom"
                and graph.n >= 12
            )
            or (
                spec["kind"] == "seagull_minor"
                and graph.n >= 13
            )
        )
        frontier_premise_cases += int(is_frontier_premise)
        known_frontier_exceeded = (
            known_frontier_exceeded or is_frontier_premise
        )
        if detail is not None:
            if direct_detail is None or not direct_semantic_premise:
                return _result(
                    spec, outcome="inconclusive", candidate=None, checked_cases=checked,
                    stop_reason="candidate_failed_semantic_verification",
                    next_case=next_case, strategy_id=strategy_id, bounds=bounds,
                    premise_cases=premise_cases,
                    metrics_extra=search_metrics(),
                )
            candidate = {
                "graph": graph.certificate(),
                "predicate_details": detail,
                "direct_verification": {
                    "accepted": True,
                    "engine": "same_executor_serialized_adjacency_replay.v1",
                    "semantic_premise_rechecked": direct_semantic_premise,
                    "details": direct_detail,
                },
            }
            return _result(
                spec, outcome="candidate", candidate=candidate, checked_cases=checked,
                stop_reason="candidate_found", next_case=next_case,
                strategy_id=strategy_id, bounds=bounds,
                premise_cases=premise_cases,
                metrics_extra=search_metrics(),
            )
        if progress and checked % 100 == 0:
            progress({"next_case": next_case}, checked)

    outcome = "no_candidate" if internal_strategy == "exact-small" else "inconclusive"
    stop_reason = (
        "finite_bound_exhausted"
        if internal_strategy == "exact-small"
        else "targeted_sample_exhausted"
    )
    return _result(
        spec, outcome=outcome, candidate=None, checked_cases=checked,
        stop_reason=stop_reason, next_case=next_case,
        strategy_id=strategy_id, bounds=bounds,
        premise_cases=premise_cases,
        metrics_extra=search_metrics(),
    )


__all__ = [
    "SECOND_BATCH_GRAPH_SPECS",
    "UNREGISTERED_SECOND_BATCH_GRAPH_IDS",
    "run_second_batch_graph_search",
]
