from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections import deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Protocol, Sequence

from amra.discovery.opg_coloring_search import (
    CNF,
    EdgeGraph,
    locate_tool,
    nauty_environment,
)


Permutation = tuple[int, ...]
_CYCLE = re.compile(r"\(([^()]*)\)")


class OrientationLiteralModel(Protocol):
    vertex_count: int
    missing_edges: frozenset[tuple[int, int]]

    def arc_literal(self, source: int, target: int) -> int | None: ...


@dataclass(frozen=True)
class UnitArcSymmetry:
    """A WLOG direction choice certified by an explicit automorphism.

    ``left < right`` and the unit clause fixes the allowed edge as
    ``right -> left``.  ``witness`` fixes every endpoint used by preceding
    units and swaps ``left`` with ``right``.
    """

    left: int
    right: int
    witness: Permutation

    @property
    def forced_arc(self) -> tuple[int, int]:
        return (self.right, self.left)

    def as_dict(self) -> dict[str, object]:
        return {
            "edge": [self.left, self.right],
            "forced_arc": [self.right, self.left],
            "witness_permutation": list(self.witness),
        }


@dataclass(frozen=True)
class UnitArcSymmetryPlan:
    vertex_count: int
    missing_edges: frozenset[tuple[int, int]]
    units: tuple[UnitArcSymmetry, ...]
    initial_generator_count: int
    residual_generators: tuple[Permutation, ...]

    @property
    def fixed_vertices(self) -> frozenset[int]:
        return frozenset(
            vertex
            for unit in self.units
            for vertex in (unit.left, unit.right)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": "amra.opg611.unit-arc-symmetry.v1",
            "vertex_count": self.vertex_count,
            "missing_edges": [list(edge) for edge in sorted(self.missing_edges)],
            "initial_generator_count": self.initial_generator_count,
            "units": [unit.as_dict() for unit in self.units],
            "residual_generators": [
                list(permutation) for permutation in self.residual_generators
            ],
        }


def identity_permutation(vertex_count: int) -> Permutation:
    return tuple(range(vertex_count))


def inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for vertex, image in enumerate(permutation):
        inverse[image] = vertex
    return tuple(inverse)


def compose_permutations(
    left: Permutation, right: Permutation
) -> Permutation:
    """Return ``left ∘ right`` for image-list permutations."""

    if len(left) != len(right):
        raise ValueError("cannot compose permutations of different degrees")
    return tuple(left[right[vertex]] for vertex in range(len(left)))


def validate_permutation(
    permutation: Permutation, vertex_count: int
) -> None:
    if len(permutation) != vertex_count:
        raise ValueError("permutation has the wrong degree")
    if set(permutation) != set(range(vertex_count)):
        raise ValueError("permutation is not a bijection")


def is_missing_graph_automorphism(
    missing_graph: EdgeGraph, permutation: Permutation
) -> bool:
    validate_permutation(permutation, missing_graph.vertex_count)
    image = {
        tuple(sorted((permutation[left], permutation[right])))
        for left, right in missing_graph.edges
    }
    return image == set(missing_graph.edges)


def _normalise_generators(
    generators: Sequence[Permutation], vertex_count: int
) -> tuple[Permutation, ...]:
    identity = identity_permutation(vertex_count)
    seen = {identity}
    normalised: list[Permutation] = []
    for generator in generators:
        validate_permutation(generator, vertex_count)
        for candidate in (generator, inverse_permutation(generator)):
            if candidate in seen:
                continue
            seen.add(candidate)
            normalised.append(candidate)
    return tuple(normalised)


def ordered_pair_swap_witness(
    generators: Sequence[Permutation],
    left: int,
    right: int,
    vertex_count: int,
) -> Permutation | None:
    """Find a generated permutation interchanging ``left`` and ``right``.

    Only the orbit of an ordered pair is explored, so the queue contains at
    most ``vertex_count * (vertex_count - 1)`` states even when the full
    automorphism group is enormous.
    """

    if not (0 <= left < vertex_count and 0 <= right < vertex_count):
        raise ValueError("ordered-pair endpoint is outside the permutation")
    if left == right:
        raise ValueError("ordered-pair endpoints must be distinct")
    generators = _normalise_generators(generators, vertex_count)
    identity = identity_permutation(vertex_count)
    queue = deque([((left, right), identity)])
    seen = {(left, right)}
    while queue:
        pair, word = queue.popleft()
        if pair == (right, left):
            return word
        for generator in generators:
            image = (generator[pair[0]], generator[pair[1]])
            if image in seen:
                continue
            seen.add(image)
            queue.append(
                (
                    image,
                    compose_permutations(generator, word),
                )
            )
    return None


def point_stabilizer_generators(
    generators: Sequence[Permutation],
    fixed_vertex: int,
    vertex_count: int,
) -> tuple[Permutation, ...]:
    """Compute generators of a point stabilizer by Schreier's lemma."""

    if not 0 <= fixed_vertex < vertex_count:
        raise ValueError("fixed vertex is outside the permutation")
    generators = _normalise_generators(generators, vertex_count)
    identity = identity_permutation(vertex_count)

    # transversal[image] maps fixed_vertex to image
    transversal: dict[int, Permutation] = {fixed_vertex: identity}
    queue = deque([fixed_vertex])
    while queue:
        image = queue.popleft()
        representative = transversal[image]
        for generator in generators:
            next_image = generator[image]
            if next_image in transversal:
                continue
            transversal[next_image] = compose_permutations(
                generator, representative
            )
            queue.append(next_image)

    schreier: list[Permutation] = []
    for image, representative in transversal.items():
        for generator in generators:
            next_image = generator[image]
            candidate = compose_permutations(
                inverse_permutation(transversal[next_image]),
                compose_permutations(generator, representative),
            )
            if candidate != identity:
                schreier.append(candidate)
    stabilizer = _normalise_generators(schreier, vertex_count)
    if any(
        generator[fixed_vertex] != fixed_vertex
        for generator in stabilizer
    ):
        raise RuntimeError("Schreier generator does not fix the base point")
    return stabilizer


def pointwise_stabilizer_generators(
    generators: Sequence[Permutation],
    fixed_vertices: Sequence[int],
    vertex_count: int,
) -> tuple[Permutation, ...]:
    stabilizer = _normalise_generators(generators, vertex_count)
    for vertex in fixed_vertices:
        stabilizer = point_stabilizer_generators(
            stabilizer, vertex, vertex_count
        )
    return stabilizer


def _locate_dreadnaut() -> Path:
    override = os.environ.get("AMRA_DREADNAUT")
    if override and Path(override).is_file():
        return Path(override)
    try:
        sibling = locate_tool("geng").resolve().parent / "dreadnaut"
    except FileNotFoundError:
        sibling = Path()
    if sibling.is_file():
        return sibling
    for name in ("dreadnaut", "nauty-dreadnaut"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise FileNotFoundError("required tool is unavailable: dreadnaut")


def _dreadnaut_graph_input(missing_graph: EdgeGraph) -> str:
    adjacency = [[] for _ in range(missing_graph.vertex_count)]
    for left, right in missing_graph.edges:
        if left == right:
            raise ValueError("missing graph must be loopless")
        adjacency[left].append(right)
        adjacency[right].append(left)
    rows = [
        f"{vertex}: {' '.join(map(str, sorted(neighbours)))};"
        for vertex, neighbours in enumerate(adjacency)
    ]
    return (
        f"n={missing_graph.vertex_count} l=100000 g\n"
        + "\n".join(rows)
        + "\n+a x q\n"
    )


def _parse_dreadnaut_generators(
    output: str, vertex_count: int
) -> tuple[Permutation, ...]:
    generators: list[Permutation] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line.startswith("("):
            continue
        permutation = list(range(vertex_count))
        cycles = _CYCLE.findall(line)
        if not cycles:
            raise ValueError("could not parse dreadnaut automorphism")
        for body in cycles:
            cycle = tuple(int(item) for item in body.split())
            if len(cycle) < 2:
                continue
            for source, target in zip(cycle, cycle[1:] + cycle[:1]):
                permutation[source] = target
        candidate = tuple(permutation)
        validate_permutation(candidate, vertex_count)
        generators.append(candidate)
    return tuple(generators)


def dreadnaut_automorphism_generators(
    missing_graph: EdgeGraph,
    *,
    executable: Path | None = None,
) -> tuple[Permutation, ...]:
    """Return deterministic nauty generators for ``Aut(missing_graph)``."""

    tool = (executable or _locate_dreadnaut()).resolve()
    process = subprocess.run(
        [str(tool)],
        input=_dreadnaut_graph_input(missing_graph),
        capture_output=True,
        text=True,
        check=False,
        timeout=30.0,
        env=nauty_environment(),
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"dreadnaut exited with {process.returncode}: "
            f"{process.stderr.strip()}"
        )
    generators = _parse_dreadnaut_generators(
        process.stdout, missing_graph.vertex_count
    )
    if any(
        not is_missing_graph_automorphism(missing_graph, generator)
        for generator in generators
    ):
        raise RuntimeError("dreadnaut returned a non-automorphism")
    return generators


def verify_unit_arc_symmetry_plan(
    missing_graph: EdgeGraph, plan: UnitArcSymmetryPlan
) -> bool:
    if plan.vertex_count != missing_graph.vertex_count:
        return False
    if plan.missing_edges != frozenset(missing_graph.edges):
        return False
    fixed: set[int] = set()
    for unit in plan.units:
        if not 0 <= unit.left < unit.right < plan.vertex_count:
            return False
        if (unit.left, unit.right) in plan.missing_edges:
            return False
        if not is_missing_graph_automorphism(
            missing_graph, unit.witness
        ):
            return False
        if unit.witness[unit.left] != unit.right:
            return False
        if unit.witness[unit.right] != unit.left:
            return False
        if any(unit.witness[vertex] != vertex for vertex in fixed):
            return False
        fixed.update((unit.left, unit.right))
    return all(
        is_missing_graph_automorphism(missing_graph, generator)
        and all(generator[vertex] == vertex for vertex in fixed)
        for generator in plan.residual_generators
    )


def build_unit_arc_symmetry_plan(
    missing_graph: EdgeGraph,
    generators: Sequence[Permutation] | None = None,
    *,
    max_units: int | None = None,
) -> UnitArcSymmetryPlan:
    """Build a sequential, certificate-carrying WLOG direction plan."""

    if max_units is not None and max_units < 0:
        raise ValueError("max_units must be nonnegative")
    vertex_count = missing_graph.vertex_count
    initial = tuple(
        dreadnaut_automorphism_generators(missing_graph)
        if generators is None
        else generators
    )
    if any(
        not is_missing_graph_automorphism(missing_graph, generator)
        for generator in initial
    ):
        raise ValueError("generator is not an automorphism of the missing graph")
    stabilizer = _normalise_generators(initial, vertex_count)
    missing_edges = frozenset(missing_graph.edges)
    units: list[UnitArcSymmetry] = []

    while max_units is None or len(units) < max_units:
        selected: UnitArcSymmetry | None = None
        for left, right in combinations(range(vertex_count), 2):
            if (left, right) in missing_edges:
                continue
            witness = ordered_pair_swap_witness(
                stabilizer, left, right, vertex_count
            )
            if witness is None:
                continue
            selected = UnitArcSymmetry(left, right, witness)
            break
        if selected is None:
            break
        units.append(selected)
        stabilizer = pointwise_stabilizer_generators(
            stabilizer,
            (selected.left, selected.right),
            vertex_count,
        )

    plan = UnitArcSymmetryPlan(
        vertex_count=vertex_count,
        missing_edges=missing_edges,
        units=tuple(units),
        initial_generator_count=len(initial),
        residual_generators=stabilizer,
    )
    if not verify_unit_arc_symmetry_plan(missing_graph, plan):
        raise RuntimeError("constructed an invalid unit-arc symmetry plan")
    return plan


def unit_arc_clauses(
    model: OrientationLiteralModel, plan: UnitArcSymmetryPlan
) -> tuple[tuple[int, ...], ...]:
    if model.vertex_count != plan.vertex_count:
        raise ValueError("orientation model and symmetry plan orders differ")
    if model.missing_edges != plan.missing_edges:
        raise ValueError("orientation model and symmetry plan graphs differ")
    clauses: list[tuple[int, ...]] = []
    for unit in plan.units:
        literal = model.arc_literal(unit.left, unit.right)
        if literal is None:
            raise ValueError("symmetry unit refers to a missing edge")
        clauses.append((-literal,))
    return tuple(clauses)


def add_unit_arc_clauses(
    cnf: CNF,
    model: OrientationLiteralModel,
    plan: UnitArcSymmetryPlan,
) -> tuple[tuple[int, ...], ...]:
    clauses = unit_arc_clauses(model, plan)
    for clause in clauses:
        cnf.add(*clause)
    return clauses


def pack_color_minimum_order_clauses(
    vertex_count: int,
    *,
    color_count: int = 4,
) -> tuple[tuple[int, ...], ...]:
    """Break the interchangeable PACK4 colors by ordering their minima.

    This uses the selection-variable layout of ``pack_four_cycles_cnf``:
    ``y[color, vertex] = color * vertex_count + vertex + 1``.  For adjacent
    colors it encodes

    ``min(V_color) < min(V_(color+1))``.

    PACK4 already makes every color nonempty and the color classes
    vertex-disjoint, so their minima are distinct.  Exactly one of the
    ``color_count!`` relabellings of any packing satisfies these clauses.
    """

    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if color_count <= 0:
        raise ValueError("color_count must be positive")

    def selected(vertex: int, color: int) -> int:
        return color * vertex_count + vertex + 1

    return tuple(
        (
            -selected(vertex, color + 1),
            *(selected(earlier, color) for earlier in range(vertex)),
        )
        for color in range(color_count - 1)
        for vertex in range(vertex_count)
    )


def add_pack_color_minimum_order_clauses(
    cnf: CNF,
    vertex_count: int,
    *,
    color_count: int = 4,
) -> tuple[tuple[int, ...], ...]:
    if cnf.variable_count < vertex_count * color_count:
        raise ValueError("CNF does not contain all PACK color variables")
    clauses = pack_color_minimum_order_clauses(
        vertex_count, color_count=color_count
    )
    for clause in clauses:
        cnf.add(*clause)
    return clauses
