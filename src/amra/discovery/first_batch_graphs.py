from __future__ import annotations

import itertools
from functools import lru_cache
from typing import Any, Callable, Iterable


def _spec(
    problem_id: str,
    source_id: str,
    title: str,
    default_bounds: dict[str, int],
    hypothesis: str,
    conclusion: str,
    witness: str,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "source_id": source_id,
        "title": title,
        "default_bounds": default_bounds,
        "model": {
            "hypothesis": hypothesis,
            "conclusion": conclusion,
            "counterexample_condition": f"{hypothesis} and NOT ({conclusion})",
            "witness": witness,
        },
    }


GRAPH_SEARCH_SPECS: dict[str, dict[str, Any]] = {
    "unsolvedmath-opg-47343": _spec(
        "unsolvedmath-opg-47343",
        "OPG-47343",
        "Turan's problem for hypergraphs",
        {"vertices": 6, "max_cases": 0},
        "The 3-uniform hypergraph has the required number of vertices and no forbidden complete subhypergraph.",
        "Its edge count is at most the stated extremal bound.",
        "A sorted list of triples, together with the checked forbidden subsets and edge count.",
    ),
    "unsolvedmath-opg-37305": _spec(
        "unsolvedmath-opg-37305",
        "OPG-37305",
        "Extremal problem on the number of tree endomorphisms",
        {"max_vertices": 8, "max_cases": 0},
        "T is a finite tree on n vertices.",
        "hom(P_n,P_n) <= hom(T,T) <= hom(K_{1,n-1},K_{1,n-1}).",
        "A canonical tree edge list and exact dynamic-programming endomorphism counts.",
    ),
    "unsolvedmath-opg-1808": _spec(
        "unsolvedmath-opg-1808",
        "OPG-1808",
        "Monochromatic reachability or rainbow triangles",
        {"max_vertices": 4, "max_cases": 0},
        "D is a tournament whose arcs use three colors.",
        "D has a rainbow directed triangle or a vertex that reaches every vertex by monochromatic directed paths.",
        "A sorted colored-arc list and exhaustive reachability and triangle tables.",
    ),
    "unsolvedmath-opg-34839": _spec(
        "unsolvedmath-opg-34839",
        "OPG-34839",
        "Double-critical graph conjecture",
        {"max_vertices": 6, "max_cases": 0},
        "G is connected, k-chromatic, and deleting both ends of every edge lowers chi by two.",
        "G is the complete graph K_k.",
        "A noncomplete adjacency list, its exact chromatic number, and all edge-deletion chromatic numbers.",
    ),
    "unsolvedmath-opg-37271": _spec(
        "unsolvedmath-opg-37271",
        "OPG-37271",
        "Star chromatic index of cubic graphs",
        {"max_vertices": 6, "colors": 6, "max_cases": 0},
        "G is a simple graph of maximum degree at most three.",
        "G has a proper six-edge-coloring with no bichromatic four-edge path or cycle.",
        "A canonical graph plus an exhaustive finite CSP failure certificate.",
    ),
    "unsolvedmath-opg-46538": _spec(
        "unsolvedmath-opg-46538",
        "OPG-46538",
        "Three longest paths have a common vertex",
        {"max_vertices": 5, "max_cases": 0},
        "G is a finite connected graph and P1,P2,P3 are longest paths.",
        "P1, P2, and P3 share a vertex.",
        "A canonical graph and three maximum-length paths with empty triple intersection.",
    ),
    "unsolvedmath-opg-46824": _spec(
        "unsolvedmath-opg-46824",
        "OPG-46824",
        "Odd-cycle transversal in triangle-free graphs",
        {"max_vertices": 6, "max_cases": 0},
        "G is a simple triangle-free n-vertex graph.",
        "At most floor(n^2/25) edges can be deleted to make G bipartite.",
        "A canonical graph and the exact value |E|-maxcut.",
    ),
    "unsolvedmath-opg-46837": _spec(
        "unsolvedmath-opg-46837",
        "OPG-46837",
        "Triangle packing versus triangle edge transversal",
        {"max_vertices": 6, "max_cases": 0},
        "The maximum number of edge-disjoint triangles is nu.",
        "There is a triangle edge transversal of size at most 2*nu.",
        "A canonical graph, exact maximum packing, and exact minimum transversal.",
    ),
    "unsolvedmath-opg-47294": _spec(
        "unsolvedmath-opg-47294",
        "OPG-47294",
        "4-connected graphs are not uniquely Hamiltonian",
        {"max_vertices": 6, "max_cases": 0},
        "G is 4-vertex-connected and Hamiltonian.",
        "G has at least two distinct undirected Hamiltonian cycles.",
        "A canonical graph and its complete Hamiltonian-cycle list.",
    ),
    "unsolvedmath-opg-646": _spec(
        "unsolvedmath-opg-646",
        "OPG-646",
        "Seymour's Second Neighbourhood Conjecture",
        {"max_vertices": 5, "max_cases": 0},
        "D is a finite oriented graph.",
        "Some vertex has outdegree at most its number of vertices at directed distance exactly two.",
        "A normalized arc list and exact first and second out-neighbourhoods for every vertex.",
    ),
    "unsolvedmath-opg-700": _spec(
        "unsolvedmath-opg-700",
        "OPG-700",
        "Chords of longest cycles",
        {"max_vertices": 6, "max_cases": 0},
        "G is a finite 3-vertex-connected graph and C is a longest cycle.",
        "Every longest cycle has a chord.",
        "A canonical graph and a chordless cycle whose length equals the exact circumference.",
    ),
    "unsolvedmath-opg-145": _spec(
        "unsolvedmath-opg-145",
        "OPG-145",
        "Acyclic edge-colouring",
        {"max_vertices": 6, "max_cases": 0},
        "G is a finite simple graph of maximum degree Delta.",
        "G has a proper (Delta+2)-edge-coloring with no bichromatic cycle.",
        "A canonical graph plus an exhaustive finite edge-coloring CSP failure certificate.",
    ),
}


@lru_cache(maxsize=None)
def _edge_pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(n), 2))


def _edges(n: int, mask: int) -> list[tuple[int, int]]:
    return [edge for bit, edge in enumerate(_edge_pairs(n)) if mask & (1 << bit)]


def _adjacency(n: int, mask: int) -> list[int]:
    adjacency = [0] * n
    for left, right in _edges(n, mask):
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return adjacency


def _edge_mask(n: int, edges: Iterable[tuple[int, int]]) -> int:
    indexes = {edge: bit for bit, edge in enumerate(_edge_pairs(n))}
    result = 0
    for left, right in edges:
        result |= 1 << indexes[(min(left, right), max(left, right))]
    return result


def _graph_certificate(n: int, mask: int) -> dict[str, Any]:
    return {
        "vertex_count": n,
        "edges": [list(edge) for edge in _edges(n, mask)],
        "adjacency_rows": _adjacency(n, mask),
    }


def _connected_after_removing(adjacency: list[int], removed: int) -> bool:
    alive = ((1 << len(adjacency)) - 1) & ~removed
    if alive == 0:
        return True
    reached = alive & -alive
    frontier = reached
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        new = adjacency[vertex] & alive & ~reached
        reached |= new
        frontier |= new
    return reached == alive


def _vertex_connected(n: int, mask: int, connectivity: int) -> bool:
    if n <= connectivity:
        return False
    adjacency = _adjacency(n, mask)
    if min((row.bit_count() for row in adjacency), default=0) < connectivity:
        return False
    for size in range(connectivity):
        for removed_vertices in itertools.combinations(range(n), size):
            removed = sum(1 << vertex for vertex in removed_vertices)
            if not _connected_after_removing(adjacency, removed):
                return False
    return True


def _is_connected(n: int, mask: int) -> bool:
    return n > 0 and _connected_after_removing(_adjacency(n, mask), 0)


def _chromatic_number(n: int, mask: int, vertices: tuple[int, ...] | None = None) -> int:
    adjacency = _adjacency(n, mask)
    active = tuple(range(n)) if vertices is None else vertices
    if not active:
        return 0
    order = tuple(sorted(active, key=lambda vertex: adjacency[vertex].bit_count(), reverse=True))

    def colorable(color_count: int) -> bool:
        colors = [-1] * n

        def visit(index: int) -> bool:
            if index == len(order):
                return True
            vertex = order[index]
            forbidden = {
                colors[neighbor]
                for neighbor in active
                if colors[neighbor] >= 0 and adjacency[vertex] & (1 << neighbor)
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit(index + 1):
                    return True
                colors[vertex] = -1
            return False

        return visit(0)

    for color_count in range(1, len(active) + 1):
        if colorable(color_count):
            return color_count
    raise AssertionError("Every finite graph has a vertex coloring")


def _cycles(n: int, mask: int) -> list[tuple[int, ...]]:
    adjacency = _adjacency(n, mask)
    found: set[tuple[int, ...]] = set()
    for start in range(n):
        stack: list[tuple[int, tuple[int, ...], int]] = [(start, (start,), 1 << start)]
        while stack:
            vertex, path, used = stack.pop()
            neighbors = adjacency[vertex]
            for nxt in range(start, n):
                if not neighbors & (1 << nxt):
                    continue
                if nxt == start and len(path) >= 3:
                    reverse = (start,) + tuple(reversed(path[1:]))
                    found.add(min(path, reverse))
                elif not used & (1 << nxt):
                    stack.append((nxt, path + (nxt,), used | (1 << nxt)))
    return sorted(found, key=lambda cycle: (len(cycle), cycle))


def _longest_paths(n: int, mask: int) -> list[tuple[int, ...]]:
    adjacency = _adjacency(n, mask)
    best_length = 0
    paths: set[tuple[int, ...]] = set()
    for start in range(n):
        stack = [(start, (start,), 1 << start)]
        while stack:
            vertex, path, used = stack.pop()
            canonical = min(path, tuple(reversed(path)))
            if len(path) > best_length:
                best_length = len(path)
                paths = {canonical}
            elif len(path) == best_length:
                paths.add(canonical)
            available = adjacency[vertex] & ~used
            while available:
                bit = available & -available
                available ^= bit
                nxt = bit.bit_length() - 1
                stack.append((nxt, path + (nxt,), used | bit))
    return sorted(paths)


def _hamiltonian_cycles(n: int, mask: int, limit: int | None = None) -> list[tuple[int, ...]]:
    adjacency = _adjacency(n, mask)
    found: list[tuple[int, ...]] = []

    def visit(path: tuple[int, ...], used: int) -> bool:
        if len(path) == n:
            if adjacency[path[-1]] & 1:
                cycle = path
                if cycle[1] < cycle[-1]:
                    found.append(cycle)
                    return limit is not None and len(found) >= limit
            return False
        available = adjacency[path[-1]] & ~used
        while available:
            bit = available & -available
            available ^= bit
            if visit(path + (bit.bit_length() - 1,), used | bit):
                return True
        return False

    if n:
        visit((0,), 1)
    return found


def _triangle_edge_masks(n: int, mask: int) -> list[int]:
    edge_index = {edge: bit for bit, edge in enumerate(_edge_pairs(n))}
    result = []
    for a, b, c in itertools.combinations(range(n), 3):
        bits = (
            (1 << edge_index[(a, b)])
            | (1 << edge_index[(a, c)])
            | (1 << edge_index[(b, c)])
        )
        if mask & bits == bits:
            result.append(bits)
    return result


def _triangle_packing_number(triangles: list[int]) -> int:
    best = 0

    def visit(index: int, used: int, count: int) -> None:
        nonlocal best
        if count + len(triangles) - index <= best:
            return
        if index == len(triangles):
            best = max(best, count)
            return
        visit(index + 1, used, count)
        if not triangles[index] & used:
            visit(index + 1, used | triangles[index], count + 1)

    visit(0, 0, 0)
    return best


def _triangle_transversal_number(triangles: list[int]) -> int:
    if not triangles:
        return 0
    best = len(triangles)

    def visit(chosen: int, count: int) -> None:
        nonlocal best
        if count >= best:
            return
        uncovered = next((triangle for triangle in triangles if not triangle & chosen), None)
        if uncovered is None:
            best = count
            return
        options = uncovered
        while options:
            bit = options & -options
            options ^= bit
            visit(chosen | bit, count + 1)

    visit(0, 0)
    return best


def _tree_from_prufer(sequence: tuple[int, ...], n: int) -> list[tuple[int, int]]:
    degree = [1] * n
    for vertex in sequence:
        degree[vertex] += 1
    edges = []
    for vertex in sequence:
        leaf = next(index for index, value in enumerate(degree) if value == 1)
        edges.append((leaf, vertex))
        degree[leaf] -= 1
        degree[vertex] -= 1
    final = [index for index, value in enumerate(degree) if value == 1]
    edges.append((final[0], final[1]))
    return edges


def _canonical_tree_code(n: int, edges: list[tuple[int, int]]) -> str:
    adjacency = [set() for _ in range(n)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    remaining = set(range(n))
    leaves = [vertex for vertex in remaining if len(adjacency[vertex]) <= 1]
    while len(remaining) > 2:
        new_leaves = []
        for leaf in leaves:
            remaining.discard(leaf)
            for neighbor in adjacency[leaf]:
                adjacency[neighbor].discard(leaf)
                if neighbor in remaining and len(adjacency[neighbor]) == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves
    original = [[] for _ in range(n)]
    for left, right in edges:
        original[left].append(right)
        original[right].append(left)

    def rooted(vertex: int, parent: int) -> str:
        return "(" + "".join(
            sorted(rooted(child, vertex) for child in original[vertex] if child != parent)
        ) + ")"

    return min(rooted(center, -1) for center in remaining)


def _tree_endomorphisms(n: int, edges: list[tuple[int, int]]) -> int:
    adjacency = [[] for _ in range(n)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)

    def evaluate(vertex: int, parent: int) -> list[int]:
        children = [evaluate(child, vertex) for child in adjacency[vertex] if child != parent]
        counts = [1] * n
        for target in range(n):
            for child_counts in children:
                counts[target] *= sum(child_counts[neighbor] for neighbor in adjacency[target])
        return counts

    return sum(evaluate(0, -1))


def _edge_coloring_exists(
    n: int,
    mask: int,
    color_count: int,
    *,
    star: bool,
) -> bool:
    edges = _edges(n, mask)
    edge_sets = [set(edge) for edge in edges]
    conflicts = [
        {other for other, other_set in enumerate(edge_sets) if index != other and edge_set & other_set}
        for index, edge_set in enumerate(edge_sets)
    ]
    forbidden_sequences: set[tuple[int, ...]] = set()
    cycle_edge_sets: set[tuple[int, ...]] = set()
    edge_index = {edge: index for index, edge in enumerate(edges)}
    for cycle in _cycles(n, mask):
        indexes = tuple(
            sorted(
                edge_index[(min(cycle[index], cycle[(index + 1) % len(cycle)]),
                            max(cycle[index], cycle[(index + 1) % len(cycle)]))]
                for index in range(len(cycle))
            )
        )
        cycle_edge_sets.add(indexes)
        if star and len(cycle) == 4:
            forbidden_sequences.add(indexes)
    if star:
        adjacency = _adjacency(n, mask)
        for start in range(n):
            stack = [(start, (start,), 1 << start)]
            while stack:
                vertex, path, used = stack.pop()
                if len(path) == 5:
                    indexes = tuple(
                        sorted(
                            edge_index[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))]
                            for i in range(4)
                        )
                    )
                    forbidden_sequences.add(indexes)
                    continue
                available = adjacency[vertex] & ~used
                while available:
                    bit = available & -available
                    available ^= bit
                    stack.append((bit.bit_length() - 1, path + (bit.bit_length() - 1,), used | bit))
    forbidden = forbidden_sequences if star else cycle_edge_sets
    colors = [-1] * len(edges)
    order = sorted(range(len(edges)), key=lambda index: len(conflicts[index]), reverse=True)

    def visit(position: int, used_colors: int) -> bool:
        if position == len(order):
            return True
        edge = order[position]
        unavailable = {colors[other] for other in conflicts[edge] if colors[other] >= 0}
        max_color = min(color_count, used_colors + 1)
        for color in range(max_color):
            if color in unavailable:
                continue
            colors[edge] = color
            invalid = False
            for sequence in forbidden:
                if edge not in sequence or any(colors[item] < 0 for item in sequence):
                    continue
                if len({colors[item] for item in sequence}) <= 2:
                    invalid = True
                    break
            if not invalid and visit(position + 1, max(used_colors, color + 1)):
                return True
            colors[edge] = -1
        return False

    return visit(0, 0)


def _bounds(problem_id: str, override: dict[str, int] | None) -> dict[str, int]:
    values = dict(GRAPH_SEARCH_SPECS[problem_id]["default_bounds"])
    if override:
        unknown = set(override) - set(values)
        if unknown:
            raise ValueError(f"Unknown bounds for {problem_id}: {sorted(unknown)}")
        values.update({key: int(value) for key, value in override.items()})
    if any(value < 0 for value in values.values()):
        raise ValueError("Search bounds must be non-negative")
    return values


def _window(
    cases: Iterable[Any],
    bounds: dict[str, int],
    checkpoint: dict[str, Any] | None,
) -> Iterable[tuple[int, Any]]:
    start = int((checkpoint or {}).get("next_case", 0))
    maximum = int(bounds.get("max_cases", 0))
    emitted = 0
    for cursor, case in enumerate(cases):
        if cursor < start:
            continue
        if maximum and emitted >= maximum:
            return
        emitted += 1
        yield cursor, case


def _result(
    problem_id: str,
    bounds: dict[str, int],
    checked: int,
    next_case: int,
    candidate: dict[str, Any] | None,
    *,
    paused: bool = False,
    note: str = "",
) -> dict[str, Any]:
    if candidate is not None:
        status = "bounded_search_candidate"
        outcome = "candidate_counterexample"
    elif paused:
        status = "bounded_search_paused"
        outcome = "paused"
    else:
        status = "bounded_search_no_counterexample"
        outcome = "no_candidate_in_bounded_range"
    notes = [
        note,
        "A finite search without a candidate is not a proof of the original unbounded statement.",
        "Any candidate must be replayed by an independent implementation before promotion.",
    ]
    return {
        "executor_id": f"first_batch.{GRAPH_SEARCH_SPECS[problem_id]['source_id'].lower()}.v1",
        "status": status,
        "outcome": outcome,
        "bounds": bounds,
        "checked_cases": checked,
        "candidate": candidate,
        "notes": [item for item in notes if item],
        "deterministic": True,
        "replayable": True,
        "model_contract": GRAPH_SEARCH_SPECS[problem_id]["model"],
        "checkpoint": {"next_case": next_case},
    }


def _graph_cases(max_vertices: int, minimum: int = 1) -> Iterable[tuple[int, int]]:
    for n in range(minimum, max_vertices + 1):
        for mask in range(1 << len(_edge_pairs(n))):
            yield n, mask


def _search_47343(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    vertices = bounds["vertices"]
    if vertices != 6:
        raise ValueError("The audited finite models for OPG-47343 use exactly six vertices")
    triples = tuple(itertools.combinations(range(vertices), 3))
    four_sets = [
        sum(1 << triples.index(triple) for triple in itertools.combinations(group, 3))
        for group in itertools.combinations(range(vertices), 4)
    ]
    five_sets = [
        sum(1 << triples.index(triple) for triple in itertools.combinations(group, 3))
        for group in itertools.combinations(range(vertices), 5)
    ]
    cases = range(1 << len(triples))
    checked = 0
    next_case = int((checkpoint or {}).get("next_case", 0))
    for cursor, mask in _window(cases, bounds, checkpoint):
        checked += 1
        next_case = cursor + 1
        edge_count = mask.bit_count()
        first_violation = edge_count > 14 and not any(mask & clique == clique for clique in four_sets)
        second_violation = edge_count > 18 and not any(mask & clique == clique for clique in five_sets)
        if first_violation or second_violation:
            candidate = {
                "clause": 1 if first_violation else 2,
                "vertex_count": vertices,
                "hyperedges": [list(triple) for bit, triple in enumerate(triples) if mask & (1 << bit)],
                "edge_count": edge_count,
                "bound": 14 if first_violation else 18,
            }
            return _result("unsolvedmath-opg-47343", bounds, checked, next_case, candidate)
    paused = bool(bounds["max_cases"]) and next_case < (1 << len(triples))
    return _result("unsolvedmath-opg-47343", bounds, checked, next_case, None, paused=paused)


def _search_37305(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def cases() -> Iterable[tuple[int, list[tuple[int, int]], str]]:
        for n in range(2, bounds["max_vertices"] + 1):
            representatives: dict[str, list[tuple[int, int]]] = {}
            for sequence in itertools.product(range(n), repeat=n - 2):
                edges = _tree_from_prufer(sequence, n)
                representatives.setdefault(_canonical_tree_code(n, edges), edges)
            for code, edges in sorted(representatives.items()):
                yield n, edges, code

    all_cases = list(cases())
    checked = 0
    next_case = int((checkpoint or {}).get("next_case", 0))
    for cursor, (n, edges, code) in _window(all_cases, bounds, checkpoint):
        checked += 1
        next_case = cursor + 1
        path = [(index, index + 1) for index in range(n - 1)]
        star = [(0, index) for index in range(1, n)]
        count = _tree_endomorphisms(n, edges)
        low = _tree_endomorphisms(n, path)
        high = _tree_endomorphisms(n, star)
        if count < low or count > high:
            candidate = {
                "vertex_count": n,
                "tree_edges": [list(edge) for edge in sorted(edges)],
                "canonical_tree_code": code,
                "endomorphisms": count,
                "path_endomorphisms": low,
                "star_endomorphisms": high,
            }
            return _result("unsolvedmath-opg-37305", bounds, checked, next_case, candidate)
    paused = bool(bounds["max_cases"]) and next_case < len(all_cases)
    return _result(
        "unsolvedmath-opg-37305", bounds, checked, next_case, None, paused=paused
    )


def _colored_tournament(n: int, code: int) -> tuple[list[int], list[tuple[int, int, int]]]:
    outgoing = [0] * n
    arcs = []
    for left, right in _edge_pairs(n):
        state = code % 6
        code //= 6
        color = state % 3
        source, target = (left, right) if state < 3 else (right, left)
        outgoing[source] |= 1 << target
        arcs.append((source, target, color))
    return outgoing, arcs


def _colored_tournament_counterexample(n: int, code: int) -> dict[str, Any] | None:
    outgoing, arcs = _colored_tournament(n, code)
    arc_color = {(source, target): color for source, target, color in arcs}
    for a, b, c in itertools.combinations(range(n), 3):
        for cycle in ((a, b, c), (a, c, b)):
            if all(outgoing[cycle[i]] & (1 << cycle[(i + 1) % 3]) for i in range(3)):
                colors = {arc_color[(cycle[i], cycle[(i + 1) % 3])] for i in range(3)}
                if len(colors) == 3:
                    return None
    reaches = []
    for source in range(n):
        union = 1 << source
        for color in range(3):
            reached = 1 << source
            frontier = reached
            while frontier:
                bit = frontier & -frontier
                frontier ^= bit
                vertex = bit.bit_length() - 1
                additions = 0
                for arc_source, target, arc_color_value in arcs:
                    if arc_source == vertex and arc_color_value == color:
                        additions |= 1 << target
                additions &= ~reached
                reached |= additions
                frontier |= additions
            union |= reached
        reaches.append(union)
        if union == (1 << n) - 1:
            return None
    return {
        "vertex_count": n,
        "colored_arcs": [list(arc) for arc in sorted(arcs)],
        "monochromatic_reachability_rows": reaches,
    }


def _search_1808(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    cases = (
        (n, code)
        for n in range(1, bounds["max_vertices"] + 1)
        for code in range(6 ** len(_edge_pairs(n)))
    )
    checked = 0
    next_case = int((checkpoint or {}).get("next_case", 0))
    total = sum(6 ** len(_edge_pairs(n)) for n in range(1, bounds["max_vertices"] + 1))
    for cursor, (n, code) in _window(cases, bounds, checkpoint):
        checked += 1
        next_case = cursor + 1
        candidate = _colored_tournament_counterexample(n, code)
        if candidate:
            return _result("unsolvedmath-opg-1808", bounds, checked, next_case, candidate)
    paused = bool(bounds["max_cases"]) and next_case < total
    return _result("unsolvedmath-opg-1808", bounds, checked, next_case, None, paused=paused)


def _search_graphs(
    problem_id: str,
    bounds: dict[str, int],
    checkpoint: dict[str, Any] | None,
    minimum: int,
    evaluator: Callable[[int, int], dict[str, Any] | None],
) -> dict[str, Any]:
    cases = _graph_cases(bounds["max_vertices"], minimum)
    checked = 0
    next_case = int((checkpoint or {}).get("next_case", 0))
    total = sum(1 << len(_edge_pairs(n)) for n in range(minimum, bounds["max_vertices"] + 1))
    for cursor, (n, mask) in _window(cases, bounds, checkpoint):
        checked += 1
        next_case = cursor + 1
        candidate = evaluator(n, mask)
        if candidate:
            return _result(problem_id, bounds, checked, next_case, candidate)
    paused = bool(bounds["max_cases"]) and next_case < total
    return _result(problem_id, bounds, checked, next_case, None, paused=paused)


def _double_critical_candidate(n: int, mask: int) -> dict[str, Any] | None:
    if not _is_connected(n, mask):
        return None
    chromatic = _chromatic_number(n, mask)
    if mask.bit_count() == n * (n - 1) // 2 or chromatic < 3:
        return None
    deletion_counts = {}
    for left, right in _edges(n, mask):
        remaining = tuple(vertex for vertex in range(n) if vertex not in {left, right})
        value = _chromatic_number(n, mask, remaining)
        deletion_counts[f"{left}-{right}"] = value
        if value != chromatic - 2:
            return None
    return {
        **_graph_certificate(n, mask),
        "chromatic_number": chromatic,
        "edge_endpoint_deletion_chromatic_numbers": deletion_counts,
    }


def _search_34839(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    return _search_graphs(
        "unsolvedmath-opg-34839", bounds, checkpoint, 1, _double_critical_candidate
    )


def _search_37271(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        if max((row.bit_count() for row in _adjacency(n, mask)), default=0) > 3:
            return None
        if _edge_coloring_exists(n, mask, bounds["colors"], star=True):
            return None
        return {**_graph_certificate(n, mask), "colors_exhausted": bounds["colors"]}

    return _search_graphs("unsolvedmath-opg-37271", bounds, checkpoint, 1, evaluate)


def _search_46538(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        if not _is_connected(n, mask):
            return None
        paths = _longest_paths(n, mask)
        for triple in itertools.combinations(paths, 3):
            if not set(triple[0]) & set(triple[1]) & set(triple[2]):
                return {
                    **_graph_certificate(n, mask),
                    "longest_path_order": len(paths[0]),
                    "paths": [list(path) for path in triple],
                }
        return None

    return _search_graphs("unsolvedmath-opg-46538", bounds, checkpoint, 1, evaluate)


def _search_46824(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        if _triangle_edge_masks(n, mask):
            return None
        edges = _edges(n, mask)
        max_cut = 0
        for side in range(1 << max(0, n - 1)):
            side <<= 1
            cut = sum(1 for left, right in edges if bool(side & (1 << left)) != bool(side & (1 << right)))
            max_cut = max(max_cut, cut)
        transversal = len(edges) - max_cut
        bound = (n * n) // 25
        if transversal <= bound:
            return None
        return {
            **_graph_certificate(n, mask),
            "minimum_odd_cycle_edge_transversal": transversal,
            "allowed_bound": bound,
        }

    return _search_graphs("unsolvedmath-opg-46824", bounds, checkpoint, 1, evaluate)


def _search_46837(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        triangles = _triangle_edge_masks(n, mask)
        packing = _triangle_packing_number(triangles)
        transversal = _triangle_transversal_number(triangles)
        if transversal <= 2 * packing:
            return None
        return {
            **_graph_certificate(n, mask),
            "triangle_packing_number": packing,
            "triangle_edge_transversal_number": transversal,
        }

    return _search_graphs("unsolvedmath-opg-46837", bounds, checkpoint, 1, evaluate)


def _search_47294(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        if not _vertex_connected(n, mask, 4):
            return None
        cycles = _hamiltonian_cycles(n, mask, limit=2)
        if len(cycles) != 1:
            return None
        return {**_graph_certificate(n, mask), "hamiltonian_cycles": [list(cycles[0])]}

    return _search_graphs("unsolvedmath-opg-47294", bounds, checkpoint, 5, evaluate)


def _oriented_counterexample(n: int, code: int) -> dict[str, Any] | None:
    outgoing = [0] * n
    arcs = []
    for left, right in _edge_pairs(n):
        state = code % 3
        code //= 3
        if state == 1:
            outgoing[left] |= 1 << right
            arcs.append((left, right))
        elif state == 2:
            outgoing[right] |= 1 << left
            arcs.append((right, left))
    rows = []
    for vertex in range(n):
        first = outgoing[vertex]
        second = 0
        remaining = first
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            second |= outgoing[bit.bit_length() - 1]
        second &= ~first & ~(1 << vertex)
        rows.append({"vertex": vertex, "outdegree": first.bit_count(), "second_outdegree": second.bit_count()})
        if first.bit_count() <= second.bit_count():
            return None
    return {"vertex_count": n, "arcs": [list(arc) for arc in sorted(arcs)], "degree_rows": rows}


def _search_646(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    cases = (
        (n, code)
        for n in range(1, bounds["max_vertices"] + 1)
        for code in range(3 ** len(_edge_pairs(n)))
    )
    checked = 0
    next_case = int((checkpoint or {}).get("next_case", 0))
    total = sum(3 ** len(_edge_pairs(n)) for n in range(1, bounds["max_vertices"] + 1))
    for cursor, (n, code) in _window(cases, bounds, checkpoint):
        checked += 1
        next_case = cursor + 1
        candidate = _oriented_counterexample(n, code)
        if candidate:
            return _result("unsolvedmath-opg-646", bounds, checked, next_case, candidate)
    paused = bool(bounds["max_cases"]) and next_case < total
    return _result("unsolvedmath-opg-646", bounds, checked, next_case, None, paused=paused)


def _search_700(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        if not _vertex_connected(n, mask, 3):
            return None
        cycles = _cycles(n, mask)
        if not cycles:
            return None
        circumference = len(cycles[-1])
        adjacency = _adjacency(n, mask)
        for cycle in reversed(cycles):
            if len(cycle) != circumference:
                break
            chord = any(
                adjacency[cycle[i]] & (1 << cycle[j])
                for i in range(len(cycle))
                for j in range(i + 1, len(cycle))
                if (j - i) not in {1, len(cycle) - 1}
            )
            if not chord:
                return {
                    **_graph_certificate(n, mask),
                    "circumference": circumference,
                    "chordless_longest_cycle": list(cycle),
                }
        return None

    return _search_graphs("unsolvedmath-opg-700", bounds, checkpoint, 4, evaluate)


def _search_145(bounds: dict[str, int], checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    def evaluate(n: int, mask: int) -> dict[str, Any] | None:
        delta = max((row.bit_count() for row in _adjacency(n, mask)), default=0)
        colors = delta + 2
        if _edge_coloring_exists(n, mask, colors, star=False):
            return None
        return {**_graph_certificate(n, mask), "maximum_degree": delta, "colors_exhausted": colors}

    return _search_graphs("unsolvedmath-opg-145", bounds, checkpoint, 1, evaluate)


_RUNNERS: dict[str, Callable[[dict[str, int], dict[str, Any] | None], dict[str, Any]]] = {
    "unsolvedmath-opg-47343": _search_47343,
    "unsolvedmath-opg-37305": _search_37305,
    "unsolvedmath-opg-1808": _search_1808,
    "unsolvedmath-opg-34839": _search_34839,
    "unsolvedmath-opg-37271": _search_37271,
    "unsolvedmath-opg-46538": _search_46538,
    "unsolvedmath-opg-46824": _search_46824,
    "unsolvedmath-opg-46837": _search_46837,
    "unsolvedmath-opg-47294": _search_47294,
    "unsolvedmath-opg-646": _search_646,
    "unsolvedmath-opg-700": _search_700,
    "unsolvedmath-opg-145": _search_145,
}


def run_graph_search(
    problem_id: str,
    bounds: dict[str, int] | None = None,
    checkpoint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    aliases = {spec["source_id"]: key for key, spec in GRAPH_SEARCH_SPECS.items()}
    normalized = aliases.get(problem_id, problem_id)
    if normalized not in GRAPH_SEARCH_SPECS:
        raise KeyError(f"Unsupported first-batch graph problem: {problem_id}")
    effective_bounds = _bounds(normalized, bounds)
    return _RUNNERS[normalized](effective_bounds, checkpoint)
