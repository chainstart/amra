"""Residual-degree cuts for the OPG-611 directed-cycle search.

Let ``D`` have outdegree seven at every vertex and let ``C_1, ..., C_t`` be
vertex-disjoint directed cycles, where ``1 <= t <= 3``.  Put
``S = V(C_1) union ... union V(C_t)``.  If every vertex outside ``S`` sends at
most ``2t`` arcs into ``S``, then

    delta^+(D - S) >= 7 - 2t = 5, 3, 1.

The known ``k=3`` and ``k=2`` cases of the Bermond--Thomassen conjecture (and
the elementary minimum-outdegree-one case) then supply ``3, 2, 1`` additional
cycles.  Consequently, an OPG-611 counterexample must have an outside vertex
that sends at least ``2t + 1`` arcs into ``S``.

This module encodes that implication without changing the main search module.
It also provides a lazy separator for pairs and triples of directed triangles
and directed four-cycles.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import TYPE_CHECKING, Iterable, Sequence

from amra.discovery.opg_coloring_search import CNF

if TYPE_CHECKING:
    from amra.discovery.opg_directed_cycles_search import OrientationModel

__all__ = [
    "PackingKey",
    "ResidualCutEncoding",
    "ResidualSeparationResult",
    "ResidualWitness",
    "add_residual_degree_cut",
    "canonical_directed_cycle",
    "canonical_packing_key",
    "orientation_has_residual_witness",
    "residual_cross_arc_count_identity",
    "residual_witness_is_automatic",
    "separate_residual_degree_cuts",
    "separate_residual_short_cycle_violations",
]


Arc = tuple[int, int]
DirectedCycle = tuple[Arc, ...]
CycleKey = tuple[int, ...]
PackingKey = tuple[CycleKey, ...]


@dataclass(frozen=True)
class ResidualWitness:
    """A reified threshold witness for one vertex outside the cycle packing."""

    vertex: int
    variable: int
    arc_literals: tuple[int, ...]


@dataclass(frozen=True)
class ResidualCutEncoding:
    """The clauses and auxiliary variables added for one canonical packing."""

    packing_key: PackingKey
    packing_size: int
    selected_vertices: tuple[int, ...]
    threshold: int
    trigger_literals: tuple[int, ...]
    witnesses: tuple[ResidualWitness, ...]
    clauses: tuple[tuple[int, ...], ...]
    first_auxiliary_variable: int | None
    last_auxiliary_variable: int | None


@dataclass(frozen=True)
class ResidualSeparationResult:
    """Summary of one lazy separation pass."""

    cuts: tuple[ResidualCutEncoding, ...]
    considered_packings: int
    duplicate_packings: int
    automatically_satisfied_packings: int
    currently_satisfied_packings: int
    inapplicable_spanning_packings: int
    limit_reached: bool

    @property
    def records(self) -> tuple[ResidualCutEncoding, ...]:
        """Generated cut records, in deterministic separation order."""

        return self.cuts

    @property
    def keys(self) -> tuple[PackingKey, ...]:
        """Canonical packing keys for the generated cuts."""

        return tuple(cut.packing_key for cut in self.cuts)

    @property
    def generated_clauses(self) -> tuple[tuple[int, ...], ...]:
        """All new CNF clauses, ready to add to an incremental solver."""

        return tuple(clause for cut in self.cuts for clause in cut.clauses)


def _new_variable(cnf: CNF) -> int:
    cnf.variable_count += 1
    return cnf.variable_count


def _add_literal_equivalence(cnf: CNF, output: int, literal: int) -> None:
    """Encode ``output iff literal`` for a possibly signed input literal."""

    cnf.add(-output, literal)
    cnf.add(output, -literal)


def _add_and_equivalence(
    cnf: CNF, output: int, first: int, second: int
) -> None:
    """Encode ``output iff (first and second)`` for signed literals."""

    cnf.add(-output, first)
    cnf.add(-output, second)
    cnf.add(output, -first, -second)


def _add_or_equivalence(
    cnf: CNF, output: int, first: int, second: int
) -> None:
    """Encode ``output iff (first or second)`` for signed literals."""

    cnf.add(output, -first)
    cnf.add(output, -second)
    cnf.add(-output, first, second)


def _add_threshold_reification(
    cnf: CNF,
    literals: Sequence[int],
    threshold: int,
) -> int:
    """Return a variable equivalent to ``sum(literals) >= threshold``.

    The dynamic-programming state ``state[i, j]`` means that at least ``j`` of
    the first ``i`` signed literals are true.  Every state is encoded by a
    full Tseitin equivalence, so the auxiliary encoding has an extension for
    every assignment of the input literals and cannot constrain them by
    itself.
    """

    values = tuple(literals)
    if not 1 <= threshold <= len(values):
        raise ValueError("threshold must lie between one and the input length")
    previous: dict[int, int] = {}
    for index, literal in enumerate(values, start=1):
        current: dict[int, int] = {}
        for count in range(1, min(index, threshold) + 1):
            state = _new_variable(cnf)
            current[count] = state
            if index == 1:
                _add_literal_equivalence(cnf, state, literal)
            elif count == 1:
                _add_or_equivalence(cnf, state, previous[1], literal)
            elif count == index:
                _add_and_equivalence(cnf, state, previous[count - 1], literal)
            else:
                # state[i,j] iff state[i-1,j] or
                #                    (state[i-1,j-1] and literal[i]).
                same_count = previous[count]
                one_less = previous[count - 1]
                cnf.add(-same_count, state)
                cnf.add(-one_less, -literal, state)
                cnf.add(-state, same_count, one_less)
                cnf.add(-state, same_count, literal)
        previous = current
    return previous[threshold]


def canonical_directed_cycle(cycle: Sequence[Arc]) -> CycleKey:
    """Canonicalize a simple directed cycle up to cyclic rotation.

    Reversal is deliberately *not* identified: it is a different directed
    cycle and has different orientation literals.
    """

    arcs = tuple(cycle)
    if len(arcs) < 2:
        raise ValueError("a directed cycle must contain at least two arcs")
    successor: dict[int, int] = {}
    predecessors: dict[int, int] = {}
    for source, target in arcs:
        if source == target:
            raise ValueError("a directed cycle cannot contain a loop")
        if source in successor or target in predecessors:
            raise ValueError("cycle arcs do not give unique successors/predecessors")
        successor[source] = target
        predecessors[target] = source
    vertices = set(successor)
    if vertices != set(predecessors) or len(vertices) != len(arcs):
        raise ValueError("cycle arcs do not have the same source and target set")
    start = min(vertices)
    order: list[int] = []
    vertex = start
    while vertex not in order:
        order.append(vertex)
        vertex = successor.get(vertex, -1)
        if vertex == -1:
            raise ValueError("cycle arcs are disconnected")
    if vertex != start or len(order) != len(vertices):
        raise ValueError("cycle arcs do not form one simple directed cycle")
    return tuple(order)


def canonical_packing_key(
    cycles: Sequence[Sequence[Arc]],
) -> PackingKey:
    """Canonicalize a vertex-disjoint cycle packing globally."""

    keys = tuple(sorted(canonical_directed_cycle(cycle) for cycle in cycles))
    used: set[int] = set()
    for key in keys:
        vertices = set(key)
        if used & vertices:
            raise ValueError("residual cuts require vertex-disjoint cycles")
        used.update(vertices)
    return keys


def _cycle_from_key(key: CycleKey) -> DirectedCycle:
    return tuple(
        (key[index], key[(index + 1) % len(key)])
        for index in range(len(key))
    )


def _packing_vertices(key: PackingKey) -> tuple[int, ...]:
    return tuple(sorted(vertex for cycle in key for vertex in cycle))


def residual_cross_arc_count_identity(
    model: OrientationModel,
    selected_vertices: Iterable[int],
    *,
    required_outdegree: int = 7,
) -> int:
    """Return the forced number of arcs from ``R=V-S`` into ``S``.

    In an orientation with fixed outdegree ``d`` at every vertex,

    ``a(R,S) = d|R| - |E(K_R - H[R])|
             = d|R| - C(|R|,2) + e_H(R)``.

    The returned integer is an identity only under the fixed-outdegree master
    constraints.  The function itself is purely structural.
    """

    if required_outdegree < 0:
        raise ValueError("required_outdegree must be nonnegative")
    selected = frozenset(selected_vertices)
    if any(
        not isinstance(vertex, int)
        or isinstance(vertex, bool)
        or not 0 <= vertex < model.vertex_count
        for vertex in selected
    ):
        raise ValueError("selected vertices must belong to the orientation model")
    residual = frozenset(range(model.vertex_count)) - selected
    residual_size = len(residual)
    missing_inside = sum(
        left in residual and right in residual
        for left, right in model.missing_edges
    )
    return (
        required_outdegree * residual_size
        - comb(residual_size, 2)
        + missing_inside
    )


def residual_witness_is_automatic(
    model: OrientationModel,
    cycles: Sequence[Sequence[Arc]],
) -> bool:
    """Whether the cut-arc identity forces a residual witness by averaging."""

    key = canonical_packing_key(cycles)
    packing_size = len(key)
    if not 1 <= packing_size <= 3:
        raise ValueError("residual-degree cuts support one to three cycles")
    selected = _packing_vertices(key)
    residual_size = model.vertex_count - len(selected)
    if residual_size <= 0:
        return False
    cross_arcs = residual_cross_arc_count_identity(
        model,
        selected,
        required_outdegree=7,
    )
    return cross_arcs > 2 * packing_size * residual_size


def add_residual_degree_cut(
    cnf: CNF,
    model: OrientationModel,
    cycles: Sequence[Sequence[Arc]],
) -> ResidualCutEncoding:
    """Add the exact witness implication for one cycle packing.

    The projection onto orientation variables is

    ``all cycle arcs -> exists x outside S, |N^+(x) intersect S| >= 2t+1``.

    A witness is omitted when the underlying graph gives the outside vertex
    fewer than ``2t+1`` available neighbours in ``S``.
    """

    if cnf.variable_count < len(model.allowed_edges):
        raise ValueError("CNF does not contain all orientation variables")
    key = canonical_packing_key(cycles)
    packing_size = len(key)
    if not 1 <= packing_size <= 3:
        raise ValueError("residual-degree cuts support one to three cycles")
    selected = _packing_vertices(key)
    selected_set = frozenset(selected)
    if len(selected) == model.vertex_count:
        raise ValueError("the residual-degree implication needs an outside vertex")
    if any(
        not 0 <= vertex < model.vertex_count
        for vertex in selected
    ):
        raise ValueError("cycle vertices must belong to the orientation model")

    canonical_cycles = tuple(_cycle_from_key(cycle) for cycle in key)
    trigger_literals: list[int] = []
    for cycle in canonical_cycles:
        for source, target in cycle:
            literal = model.arc_literal(source, target)
            if literal is None:
                raise ValueError("a trigger cycle uses a missing edge")
            trigger_literals.append(literal)

    threshold = 2 * packing_size + 1
    clause_start = len(cnf.clauses)
    variable_start = cnf.variable_count + 1
    witnesses: list[ResidualWitness] = []
    for outside in range(model.vertex_count):
        if outside in selected_set:
            continue
        arc_literals = tuple(
            literal
            for target in selected
            if (literal := model.arc_literal(outside, target)) is not None
        )
        if len(arc_literals) < threshold:
            continue
        witness = _add_threshold_reification(cnf, arc_literals, threshold)
        witnesses.append(
            ResidualWitness(
                vertex=outside,
                variable=witness,
                arc_literals=arc_literals,
            )
        )

    cnf.add(
        *(-literal for literal in trigger_literals),
        *(witness.variable for witness in witnesses),
    )
    variable_end = cnf.variable_count
    first_auxiliary = variable_start if variable_end >= variable_start else None
    last_auxiliary = variable_end if first_auxiliary is not None else None
    return ResidualCutEncoding(
        packing_key=key,
        packing_size=packing_size,
        selected_vertices=selected,
        threshold=threshold,
        trigger_literals=tuple(trigger_literals),
        witnesses=tuple(witnesses),
        clauses=tuple(cnf.clauses[clause_start:]),
        first_auxiliary_variable=first_auxiliary,
        last_auxiliary_variable=last_auxiliary,
    )


def orientation_has_residual_witness(
    model: OrientationModel,
    arcs: Iterable[Arc],
    cycles: Sequence[Sequence[Arc]],
) -> bool:
    """Check the residual witness condition directly in one orientation."""

    key = canonical_packing_key(cycles)
    packing_size = len(key)
    if not 1 <= packing_size <= 3:
        raise ValueError("residual-degree cuts support one to three cycles")
    selected = frozenset(_packing_vertices(key))
    arc_set = frozenset(arcs)
    threshold = 2 * packing_size + 1
    return any(
        sum((outside, target) in arc_set for target in selected) >= threshold
        for outside in range(model.vertex_count)
        if outside not in selected
    )


def _validate_current_orientation(
    model: OrientationModel,
    arcs: Sequence[Arc],
    *,
    required_outdegree: int | None,
) -> None:
    arc_set = set(arcs)
    if len(arc_set) != len(arcs):
        raise ValueError("current orientation contains duplicate arcs")
    if any(
        source == target
        or not 0 <= source < model.vertex_count
        or not 0 <= target < model.vertex_count
        for source, target in arc_set
    ):
        raise ValueError("current orientation contains an invalid arc")
    for left, right in model.allowed_edges:
        if ((left, right) in arc_set) == ((right, left) in arc_set):
            raise ValueError("current arcs are not a full orientation of the model")
    if len(arc_set) != len(model.allowed_edges):
        raise ValueError("current orientation contains an arc on a missing edge")
    if required_outdegree is not None:
        outdegrees = [0] * model.vertex_count
        for source, _ in arc_set:
            outdegrees[source] += 1
        if any(degree != required_outdegree for degree in outdegrees):
            raise ValueError("cut-identity prefilter needs the fixed outdegree")


def separate_residual_degree_cuts(
    cnf: CNF,
    model: OrientationModel,
    arcs: Sequence[Arc],
    known_keys: set[PackingKey] | None = None,
    *,
    pack_sizes: Sequence[int] = (2, 3),
    limit: int = 256,
    consideration_limit: int = 100_000,
    traversal_limit: int = 1_000_000,
    use_cut_identity_prefilter: bool = True,
) -> ResidualSeparationResult:
    """Separate violated residual cuts for short two/three-cycle packings.

    ``known_keys`` is a caller-owned global registry.  Keys are invariant
    under cycle rotation and packing order.  Generated cuts and structurally
    automatic packings enter the registry; a currently satisfied but
    nonautomatic packing does not, because a later orientation can violate the
    same trigger.

    ``limit`` bounds generated cuts, ``consideration_limit`` bounds complete
    packings inspected, and ``traversal_limit`` bounds all DFS nodes (including
    prefixes that cannot be extended).  If the identity prefilter is disabled,
    the caller remains responsible for using these mathematically valid cuts
    only with the OPG-611 fixed-outdegree-seven master constraints.
    """

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError("limit must be a nonnegative integer")
    if (
        not isinstance(consideration_limit, int)
        or isinstance(consideration_limit, bool)
        or consideration_limit < 1
    ):
        raise ValueError("consideration_limit must be a positive integer")
    if (
        not isinstance(traversal_limit, int)
        or isinstance(traversal_limit, bool)
        or traversal_limit < 1
    ):
        raise ValueError("traversal_limit must be a positive integer")
    sizes = tuple(pack_sizes)
    if (
        not sizes
        or len(set(sizes)) != len(sizes)
        or any(size not in (2, 3) for size in sizes)
    ):
        raise ValueError("pack_sizes must be distinct values from {2, 3}")
    _validate_current_orientation(
        model,
        arcs,
        required_outdegree=(7 if use_cut_identity_prefilter else None),
    )
    registry = known_keys if known_keys is not None else set()
    if limit == 0:
        return ResidualSeparationResult((), 0, 0, 0, 0, 0, True)

    # A local import keeps this module safe to import from a future hard-runner
    # integration inside opg_directed_cycles_search itself.
    from amra.discovery.opg_directed_cycles_search import directed_short_cycles

    arc_set = frozenset(arcs)
    cycle_keys = tuple(
        sorted(
            {
                canonical_directed_cycle(cycle)
                for cycle in directed_short_cycles(model.vertex_count, arcs)
            }
        )
    )
    cycle_masks = tuple(
        sum(1 << vertex for vertex in key) for key in cycle_keys
    )

    cuts: list[ResidualCutEncoding] = []
    considered = 0
    duplicates = 0
    automatic = 0
    satisfied = 0
    spanning = 0
    stopped_at_limit = False
    stopped_at_consideration_limit = False
    visited_nodes = 0

    def inspect(chosen: tuple[int, ...]) -> None:
        nonlocal considered, duplicates, automatic, satisfied, spanning
        nonlocal stopped_at_consideration_limit
        if considered >= consideration_limit:
            stopped_at_consideration_limit = True
            return
        key = tuple(cycle_keys[index] for index in chosen)
        considered += 1
        if key in registry:
            duplicates += 1
            return
        cycles = tuple(_cycle_from_key(cycle) for cycle in key)
        selected = _packing_vertices(key)
        if len(selected) == model.vertex_count:
            spanning += 1
            return
        if (
            use_cut_identity_prefilter
            and residual_witness_is_automatic(
                model,
                cycles,
            )
        ):
            registry.add(key)
            automatic += 1
            return
        threshold = 2 * len(key) + 1
        selected_set = frozenset(selected)
        if any(
            sum((outside, target) in arc_set for target in selected_set)
            >= threshold
            for outside in range(model.vertex_count)
            if outside not in selected_set
        ):
            satisfied += 1
            return
        cut = add_residual_degree_cut(cnf, model, cycles)
        registry.add(key)
        cuts.append(cut)

    def extend(
        target_size: int,
        start: int,
        used_vertices: int,
        chosen: tuple[int, ...],
    ) -> None:
        nonlocal stopped_at_limit, visited_nodes
        if visited_nodes >= traversal_limit:
            stopped_at_limit = True
            return
        visited_nodes += 1
        if (
            len(cuts) >= limit
            or stopped_at_consideration_limit
            or stopped_at_limit
        ):
            stopped_at_limit = True
            return
        if len(chosen) == target_size:
            inspect(chosen)
            return
        needed = target_size - len(chosen)
        last_start = len(cycle_keys) - needed
        for index in range(start, last_start + 1):
            if cycle_masks[index] & used_vertices:
                continue
            extend(
                target_size,
                index + 1,
                used_vertices | cycle_masks[index],
                chosen + (index,),
            )
            if (
                len(cuts) >= limit
                or stopped_at_consideration_limit
                or stopped_at_limit
            ):
                stopped_at_limit = True
                return

    for packing_size in sizes:
        extend(packing_size, 0, 0, ())
        if (
            len(cuts) >= limit
            or stopped_at_consideration_limit
            or stopped_at_limit
        ):
            stopped_at_limit = True
            break

    return ResidualSeparationResult(
        cuts=tuple(cuts),
        considered_packings=considered,
        duplicate_packings=duplicates,
        automatically_satisfied_packings=automatic,
        currently_satisfied_packings=satisfied,
        inapplicable_spanning_packings=spanning,
        limit_reached=stopped_at_limit,
    )


def separate_residual_short_cycle_violations(
    cnf: CNF,
    model: OrientationModel,
    arcs: Sequence[Arc],
    *,
    packing_sizes: Sequence[int] = (2, 3),
    limit: int = 256,
    consideration_limit: int = 100_000,
    traversal_limit: int = 1_000_000,
    known_packings: set[PackingKey] | None = None,
    use_cut_identity_prefilter: bool = True,
    required_outdegree: int = 7,
) -> ResidualSeparationResult:
    """Compatibility spelling for early hard-runner integrations.

    New integrations should use :func:`separate_residual_degree_cuts`.
    OPG-611 residual cuts are specific to fixed outdegree seven.
    """

    if required_outdegree != 7:
        raise ValueError("OPG-611 residual cuts require fixed outdegree seven")
    return separate_residual_degree_cuts(
        cnf,
        model,
        arcs,
        known_packings,
        pack_sizes=packing_sizes,
        limit=limit,
        consideration_limit=consideration_limit,
        traversal_limit=traversal_limit,
        use_cut_identity_prefilter=use_cut_identity_prefilter,
    )
