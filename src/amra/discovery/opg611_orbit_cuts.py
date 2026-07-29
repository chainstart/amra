from __future__ import annotations

from collections import deque
from collections.abc import MutableSet, Sequence
import time
from typing import Protocol

from amra.discovery.opg611_symmetry import (
    Permutation,
    inverse_permutation,
    validate_permutation,
)


Clause = tuple[int, ...]


class OrientationModelLike(Protocol):
    vertex_count: int
    missing_edges: frozenset[tuple[int, int]]
    allowed_edges: tuple[tuple[int, int], ...]
    arc_variables: dict[tuple[int, int], int]

    def arc_literal(self, source: int, target: int) -> int | None: ...


def canonical_clause(clause: Sequence[int]) -> Clause:
    """Return the deterministic representation used for global deduplication."""

    if any(literal == 0 for literal in clause):
        raise ValueError("CNF clauses cannot contain literal zero")
    literals = frozenset(clause)
    if any(-literal in literals for literal in literals):
        raise ValueError("packing block clause must not be tautological")
    return tuple(sorted(literals))


def _variable_pairs(
    model: OrientationModelLike,
) -> dict[int, tuple[int, int]]:
    pairs: dict[int, tuple[int, int]] = {}
    for pair, variable in model.arc_variables.items():
        if variable <= 0:
            raise ValueError("orientation variables must be positive")
        if variable in pairs:
            raise ValueError("orientation variable is assigned to two edges")
        if pair not in model.allowed_edges:
            raise ValueError("orientation variable refers to a non-allowed edge")
        pairs[variable] = pair
    if len(pairs) != len(model.allowed_edges):
        raise ValueError("not every allowed edge has an orientation variable")
    return pairs


def verify_missing_graph_automorphism(
    model: OrientationModelLike,
    permutation: Permutation,
) -> None:
    """Raise unless ``permutation`` preserves the missing/allowed partition."""

    validate_permutation(permutation, model.vertex_count)
    missing_image = {
        tuple(sorted((permutation[left], permutation[right])))
        for left, right in model.missing_edges
    }
    if missing_image != set(model.missing_edges):
        raise ValueError("permutation is not an automorphism of the missing graph")
    for left, right in model.allowed_edges:
        image = tuple(sorted((permutation[left], permutation[right])))
        if image not in model.arc_variables:
            raise ValueError("automorphism maps an allowed edge outside the model")


def map_orientation_literal(
    model: OrientationModelLike,
    literal: int,
    permutation: Permutation,
    *,
    variable_pairs: dict[int, tuple[int, int]] | None = None,
) -> int:
    """Map a signed orientation literal under a vertex automorphism.

    A positive variable for ``left < right`` denotes ``left -> right``; its
    negative denotes ``right -> left``.  Mapping the directed condition first,
    then asking ``model.arc_literal`` for its signed representation, handles
    endpoint-order sign flips correctly.
    """

    if literal == 0:
        raise ValueError("CNF literal cannot be zero")
    pairs = variable_pairs if variable_pairs is not None else _variable_pairs(model)
    pair = pairs.get(abs(literal))
    if pair is None:
        raise ValueError("literal is not an orientation variable")
    left, right = pair
    source, target = (left, right) if literal > 0 else (right, left)
    mapped = model.arc_literal(
        permutation[source],
        permutation[target],
    )
    if mapped is None:
        raise ValueError("automorphism maps a literal to a missing edge")
    if abs(mapped) not in pairs:
        raise ValueError("mapped literal is outside the orientation variables")
    return mapped


def map_orientation_clause(
    model: OrientationModelLike,
    clause: Sequence[int],
    permutation: Permutation,
    *,
    variable_pairs: dict[int, tuple[int, int]] | None = None,
) -> Clause:
    pairs = variable_pairs if variable_pairs is not None else _variable_pairs(model)
    source = canonical_clause(clause)
    mapped = canonical_clause(
        tuple(
            map_orientation_literal(
                model,
                literal,
                permutation,
                variable_pairs=pairs,
            )
            for literal in source
        )
    )
    if len(mapped) != len(source):
        raise ValueError("automorphism did not preserve clause length")
    return mapped


def _normalise_generators(
    model: OrientationModelLike,
    generators: Sequence[Permutation],
) -> tuple[Permutation, ...]:
    identity = tuple(range(model.vertex_count))
    seen = {identity}
    normalised: list[Permutation] = []
    for generator in generators:
        verify_missing_graph_automorphism(model, generator)
        for candidate in (generator, inverse_permutation(generator)):
            if candidate in seen:
                continue
            verify_missing_graph_automorphism(model, candidate)
            seen.add(candidate)
            normalised.append(candidate)
    return tuple(normalised)


def orbit_lift_packing_block_clause(
    model: OrientationModelLike,
    packing_block_clause: Sequence[int],
    automorphism_generators: Sequence[Permutation],
    known_clauses: MutableSet[Clause],
    *,
    limit: int,
    deadline: float | None = None,
) -> tuple[Clause, ...]:
    """Add up to ``limit`` novel canonical clauses from an Aut(H) orbit.

    The returned clauses are also inserted into ``known_clauses``.  A later
    call with the same base clause traverses known orbit nodes and continues
    returning previously unseen images, so a finite limit can be used across
    CEGAR rounds without producing duplicates.
    """

    if limit < 0:
        raise ValueError("limit must be nonnegative")
    variable_pairs = _variable_pairs(model)
    generators = _normalise_generators(model, automorphism_generators)
    base = canonical_clause(packing_block_clause)
    # Validate every source literal even when limit is zero or the group is
    # trivial.  This prevents malformed cuts from silently entering `known`.
    for literal in base:
        map_orientation_literal(
            model,
            literal,
            tuple(range(model.vertex_count)),
            variable_pairs=variable_pairs,
        )

    canonical_known = {canonical_clause(clause) for clause in known_clauses}
    if limit == 0:
        return ()

    queue = deque([base])
    explored = {base}
    novel: list[Clause] = []
    while queue and len(novel) < limit:
        if deadline is not None and time.monotonic() >= deadline:
            break
        clause = queue.popleft()
        if clause not in canonical_known:
            canonical_known.add(clause)
            known_clauses.add(clause)
            novel.append(clause)
            if len(novel) >= limit:
                break
        for generator in generators:
            image = map_orientation_clause(
                model,
                clause,
                generator,
                variable_pairs=variable_pairs,
            )
            if image in explored:
                continue
            explored.add(image)
            queue.append(image)
    return tuple(novel)
