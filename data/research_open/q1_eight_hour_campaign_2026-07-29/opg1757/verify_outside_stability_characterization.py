#!/usr/bin/env python3
"""Finite falsification audit for the outside-stability criterion."""

from itertools import combinations


def is_forest(vertex_count: int, edges: tuple[tuple[int, int], ...]) -> bool:
    parent = list(range(vertex_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def forest_edge_sets(vertex_count: int) -> tuple[frozenset[tuple[int, int]], ...]:
    edges = tuple(combinations(range(vertex_count), 2))
    forests = []
    for mask in range(1 << len(edges)):
        selected = tuple(
            edge for index, edge in enumerate(edges) if mask & (1 << index)
        )
        if is_forest(vertex_count, selected):
            forests.append(frozenset(selected))
    return tuple(forests)


def component_labels(
    boundary_size: int, edges: frozenset[tuple[int, int]]
) -> tuple[int, ...]:
    parent = list(range(boundary_size))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[left_root] = right_root
    return tuple(find(vertex) for vertex in range(boundary_size))


def target_refines_source(
    source_labels: tuple[int, ...], target_labels: tuple[int, ...]
) -> bool:
    for left, right in combinations(range(len(source_labels)), 2):
        if (
            target_labels[left] == target_labels[right]
            and source_labels[left] != source_labels[right]
        ):
            return False
    return True


def audit_boundary(boundary_size: int) -> dict[str, int]:
    local_forests = forest_edge_sets(boundary_size)
    # One new external vertex already realizes every necessity witness
    # u--w--v.  We enumerate all external forests on this enlarged set.
    external_forests = forest_edge_sets(boundary_size + 1)
    label_cache = {
        forest: component_labels(boundary_size, forest)
        for forest in local_forests
    }

    stable_pairs = 0
    checked_contexts = 0
    for source in local_forests:
        for target in local_forests:
            predicted = target_refines_source(
                label_cache[source], label_cache[target]
            )
            observed = True
            local_support = source | target
            for external in external_forests:
                if local_support & external:
                    continue
                checked_contexts += 1
                if not is_forest(
                    boundary_size + 1, tuple(source | external)
                ):
                    continue
                if not is_forest(
                    boundary_size + 1, tuple(target | external)
                ):
                    observed = False
                    break
            if observed != predicted:
                raise AssertionError(
                    "outside-stability mismatch: "
                    f"boundary={boundary_size}, source={sorted(source)}, "
                    f"target={sorted(target)}, predicted={predicted}, "
                    f"observed={observed}"
                )
            stable_pairs += int(observed)

    return {
        "boundary": boundary_size,
        "local_forests": len(local_forests),
        "pairs": len(local_forests) ** 2,
        "stable_pairs": stable_pairs,
        "checked_contexts": checked_contexts,
    }


def main() -> None:
    for boundary_size in range(1, 5):
        result = audit_boundary(boundary_size)
        print(
            "OUTSIDE_STABILITY"
            f"|boundary={result['boundary']}"
            f"|local_forests={result['local_forests']}"
            f"|pairs={result['pairs']}"
            f"|stable_pairs={result['stable_pairs']}"
            f"|checked_contexts={result['checked_contexts']}"
        )


if __name__ == "__main__":
    main()
