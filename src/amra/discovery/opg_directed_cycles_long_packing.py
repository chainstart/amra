from __future__ import annotations

import math
import time
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Sequence

from amra.discovery.opg_directed_cycles_search import (
    OrientationModel,
    packing_block_clause,
)


DirectedCycle = tuple[tuple[int, int], ...]
DirectedPacking = tuple[DirectedCycle, ...]


@dataclass(frozen=True)
class LongPackingBatch:
    """Auditable output of the bounded n=16 long-cycle separator."""

    clauses: tuple[tuple[int, ...], ...]
    packings: tuple[DirectedPacking, ...]
    scan_steps: int
    short_cycle_candidates: int
    long_cycle_candidates: int
    dp_transitions: int
    short_cycles_found: int
    long_cycles_found: int
    packings_examined: int
    known_duplicates: int
    local_duplicates: int
    stop_reason: str
    elapsed_seconds: float

    @property
    def exhausted(self) -> bool:
        return self.stop_reason == "exhausted"

    @property
    def deadline_reached(self) -> bool:
        return self.stop_reason == "deadline"

    @property
    def scan_limit_reached(self) -> bool:
        return self.stop_reason == "scan_limit"

    @property
    def batch_limit_reached(self) -> bool:
        return self.stop_reason == "batch_limit"


@dataclass(frozen=True)
class _Cycle:
    vertices: tuple[int, ...]
    arcs: DirectedCycle
    mask: int

    @property
    def length(self) -> int:
        return len(self.vertices)

    @classmethod
    def from_vertices(cls, vertices: tuple[int, ...]) -> _Cycle:
        arcs = tuple(
            (vertices[index], vertices[(index + 1) % len(vertices)])
            for index in range(len(vertices))
        )
        mask = sum(1 << vertex for vertex in vertices)
        return cls(vertices, arcs, mask)


@dataclass
class _Statistics:
    short_cycle_candidates: int = 0
    long_cycle_candidates: int = 0
    dp_transitions: int = 0
    packings_examined: int = 0
    known_duplicates: int = 0
    local_duplicates: int = 0


class _Budget:
    def __init__(self, scan_limit: int, deadline: float | None) -> None:
        self.scan_limit = scan_limit
        self.deadline = deadline
        self.scan_steps = 0
        self.stop_reason: str | None = None

    def check(self) -> bool:
        if self.stop_reason is not None:
            return False
        if self.deadline is not None and time.monotonic() >= self.deadline:
            self.stop_reason = "deadline"
            return False
        if self.scan_steps >= self.scan_limit:
            self.stop_reason = "scan_limit"
            return False
        return True

    def consume(self) -> bool:
        if not self.check():
            return False
        self.scan_steps += 1
        return True

    def stop(self, reason: str) -> None:
        if self.stop_reason is None:
            self.stop_reason = reason


class _ScanWindow:
    """A local scan allotment that never weakens the global budget."""

    def __init__(self, budget: _Budget, stop_at: int) -> None:
        self.budget = budget
        self.stop_at = min(stop_at, budget.scan_limit)
        self.truncated = False

    def consume(self) -> bool:
        if self.budget.stop_reason is not None:
            return False
        if self.budget.scan_steps >= self.stop_at:
            self.truncated = True
            return False
        return self.budget.consume()


def _validate_inputs(
    model: OrientationModel,
    arcs: Sequence[tuple[int, int]],
    *,
    batch_limit: int,
    scan_limit: int,
    cycle_offset: int,
    deadline: float | None,
) -> frozenset[tuple[int, int]]:
    if model.vertex_count != 16:
        raise ValueError("long packing separator is specific to n=16")
    for name, value in (
        ("batch_limit", batch_limit),
        ("scan_limit", scan_limit),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be positive")
    if not isinstance(cycle_offset, int) or isinstance(cycle_offset, bool):
        raise ValueError("cycle_offset must be an integer")
    if deadline is not None and (
        isinstance(deadline, bool)
        or not isinstance(deadline, (int, float))
        or not math.isfinite(deadline)
    ):
        raise ValueError("deadline must be a finite monotonic timestamp")

    arc_set: set[tuple[int, int]] = set()
    for arc in arcs:
        if (
            len(arc) != 2
            or any(
                not isinstance(vertex, int) or isinstance(vertex, bool)
                for vertex in arc
            )
        ):
            raise ValueError(f"invalid directed arc: {arc!r}")
        source, target = arc
        if (
            source == target
            or not 0 <= source < model.vertex_count
            or not 0 <= target < model.vertex_count
        ):
            raise ValueError(f"invalid directed arc: {arc!r}")
        if model.arc_literal(source, target) is None:
            raise ValueError(f"directed arc uses a missing edge: {arc!r}")
        if arc in arc_set:
            raise ValueError(f"duplicate directed arc: {arc!r}")
        if (target, source) in arc_set:
            raise ValueError(
                "arcs must be an orientation, not an antiparallel digraph"
            )
        arc_set.add(arc)
    return frozenset(arc_set)


def _enumerate_cycles(
    vertices: tuple[int, ...],
    lengths: Sequence[int],
    arc_set: frozenset[tuple[int, int]],
    scanner: _Budget | _ScanWindow,
    statistics: _Statistics,
    *,
    short: bool,
) -> tuple[tuple[_Cycle, ...], bool]:
    cycles: list[_Cycle] = []
    exact_seen: set[tuple[int, tuple[int, ...]]] = set()
    for length in lengths:
        if length > len(vertices):
            continue
        for selected in combinations(vertices, length):
            root = selected[0]
            for tail in permutations(selected[1:]):
                if not scanner.consume():
                    return tuple(cycles), False
                if short:
                    statistics.short_cycle_candidates += 1
                else:
                    statistics.long_cycle_candidates += 1
                order = (root,) + tail
                cycle = _Cycle.from_vertices(order)
                if not all(arc in arc_set for arc in cycle.arcs):
                    continue
                # The mask accelerates disjointness and the cyclic order keeps
                # distinct cycles on the same vertex set distinct.
                key = (cycle.mask, cycle.vertices)
                if key in exact_seen:
                    continue
                exact_seen.add(key)
                cycles.append(cycle)
    return tuple(cycles), True


def _disjoint(cycles: Sequence[_Cycle]) -> bool:
    used = 0
    for cycle in cycles:
        if used & cycle.mask:
            return False
        used |= cycle.mask
    return True


def separate_long_cycle_packings(
    model: OrientationModel,
    arcs: Sequence[tuple[int, int]],
    known: set[tuple[int, ...]],
    *,
    batch_limit: int = 8,
    scan_limit: int = 100_000,
    cycle_offset: int = 0,
    deadline: float | None = None,
) -> LongPackingBatch:
    """Find sound, globally novel PACK4 clauses involving a 5--7-cycle.

    Every directed cycle in an oriented graph has length at least three.
    Hence four vertex-disjoint cycles on 16 vertices have lengths in
    ``3..7``.  If at least one is long, the only possible length shapes are:

    * one 5--7-cycle plus three 3/4-cycles; or
    * two 5-cycles plus two 3-cycles.

    This separator enumerates exactly those shapes.  It is intentionally
    incomplete when a deadline or scan/batch limit is reached, but every
    emitted clause is the ordinary PACK4 packing block clause and is
    therefore sound.  ``known`` is updated only with clauses actually
    returned.

    ``deadline`` is an absolute ``time.monotonic()`` timestamp.  Every
    candidate cycle order, disjoint-packing transition, partition, and
    cycle-pair transition consumes one scan step, so ``scan_steps`` never
    exceeds ``scan_limit``.
    """

    started = time.monotonic()
    arc_set = _validate_inputs(
        model,
        arcs,
        batch_limit=batch_limit,
        scan_limit=scan_limit,
        cycle_offset=cycle_offset,
        deadline=deadline,
    )
    budget = _Budget(scan_limit, deadline)
    statistics = _Statistics()
    clauses: list[tuple[int, ...]] = []
    witnesses: list[DirectedPacking] = []
    local_seen: set[tuple[int, ...]] = set()
    exact_packing_seen: set[
        tuple[tuple[int, tuple[int, ...]], ...]
    ] = set()
    unique_long_cycles: set[tuple[int, tuple[int, ...]]] = set()

    if not budget.check():
        return LongPackingBatch(
            (),
            (),
            budget.scan_steps,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            budget.stop_reason or "deadline",
            time.monotonic() - started,
        )

    short_cycles, short_complete = _enumerate_cycles(
        tuple(range(16)),
        (3, 4),
        arc_set,
        budget,
        statistics,
        short=True,
    )
    if cycle_offset and short_cycles:
        offset = cycle_offset % len(short_cycles)
        short_cycles = short_cycles[offset:] + short_cycles[:offset]

    long_cache: dict[
        tuple[int, tuple[int, ...]], tuple[_Cycle, ...]
    ] = {}

    def long_cycles_on(
        mask: int,
        lengths: tuple[int, ...],
        scanner: _Budget | _ScanWindow,
    ) -> tuple[tuple[_Cycle, ...], bool]:
        key = (mask, lengths)
        cached = long_cache.get(key)
        if cached is not None:
            return cached, True
        vertices = tuple(vertex for vertex in range(16) if mask & (1 << vertex))
        found, complete = _enumerate_cycles(
            vertices,
            lengths,
            arc_set,
            scanner,
            statistics,
            short=False,
        )
        unique_long_cycles.update(
            (cycle.mask, cycle.vertices) for cycle in found
        )
        if complete:
            long_cache[key] = found
        return found, complete

    def emit(cycles: tuple[_Cycle, ...]) -> None:
        if budget.stop_reason is not None:
            return
        if len(cycles) != 4 or not _disjoint(cycles):
            raise RuntimeError("internal long separator packing invariant failed")
        if not any(cycle.length >= 5 for cycle in cycles):
            raise RuntimeError("long separator produced an all-short packing")
        packing_key = tuple(
            sorted((cycle.mask, cycle.vertices) for cycle in cycles)
        )
        if packing_key in exact_packing_seen:
            statistics.local_duplicates += 1
            return
        exact_packing_seen.add(packing_key)
        if not budget.consume():
            return
        statistics.dp_transitions += 1
        statistics.packings_examined += 1
        packing = tuple(cycle.arcs for cycle in cycles)
        clause = tuple(
            sorted(set(packing_block_clause(model, packing)))
        )
        if clause in known:
            statistics.known_duplicates += 1
            return
        if clause in local_seen:
            statistics.local_duplicates += 1
            return
        local_seen.add(clause)
        clauses.append(clause)
        witnesses.append(packing)
        if len(clauses) >= batch_limit:
            budget.stop("batch_limit")

    phase_truncated = False
    if short_complete and budget.stop_reason is None:
        remaining_scan = budget.scan_limit - budget.scan_steps
        first_phase_stop = budget.scan_steps + max(1, remaining_scan // 2)
        one_long_scanner = _ScanWindow(budget, first_phase_stop)

        for selected in combinations(range(len(short_cycles)), 3):
            if not one_long_scanner.consume():
                break
            statistics.dp_transitions += 1
            base = tuple(short_cycles[index] for index in selected)
            if not _disjoint(base):
                continue
            used = base[0].mask | base[1].mask | base[2].mask
            residual_count = 16 - used.bit_count()
            if residual_count < 5:
                continue
            lengths = tuple(range(5, min(7, residual_count) + 1))
            residual_mask = ((1 << 16) - 1) ^ used
            long_cycles, complete = long_cycles_on(
                residual_mask,
                lengths,
                one_long_scanner,
            )
            for long_cycle in long_cycles:
                emit(base + (long_cycle,))
                if budget.stop_reason is not None:
                    break
            if not complete or budget.stop_reason is not None:
                break
        phase_truncated |= one_long_scanner.truncated

    if short_complete and budget.stop_reason is None:
        triangles = tuple(
            cycle for cycle in short_cycles if cycle.length == 3
        )
        for first_index, second_index in combinations(
            range(len(triangles)), 2
        ):
            if not budget.consume():
                break
            statistics.dp_transitions += 1
            first = triangles[first_index]
            second = triangles[second_index]
            if first.mask & second.mask:
                continue
            residual_mask = ((1 << 16) - 1) ^ (first.mask | second.mask)
            residual_vertices = tuple(
                vertex
                for vertex in range(16)
                if residual_mask & (1 << vertex)
            )
            if len(residual_vertices) != 10:
                continue
            anchor = residual_vertices[0]
            for tail in combinations(residual_vertices[1:], 4):
                if not budget.consume():
                    break
                statistics.dp_transitions += 1
                first_vertices = (anchor,) + tail
                first_mask = sum(1 << vertex for vertex in first_vertices)
                second_mask = residual_mask ^ first_mask
                first_longs, first_complete = long_cycles_on(
                    first_mask,
                    (5,),
                    budget,
                )
                if not first_complete:
                    break
                if not first_longs:
                    continue
                second_longs, second_complete = long_cycles_on(
                    second_mask,
                    (5,),
                    budget,
                )
                if not second_complete:
                    break
                for first_long in first_longs:
                    for second_long in second_longs:
                        emit((first, second, first_long, second_long))
                        if budget.stop_reason is not None:
                            break
                    if budget.stop_reason is not None:
                        break
                if budget.stop_reason is not None:
                    break
            if budget.stop_reason is not None:
                break

    if budget.stop_reason is None:
        budget.check()
    if budget.stop_reason is None:
        budget.stop("scan_limit" if phase_truncated else "exhausted")
    known.update(clauses)
    return LongPackingBatch(
        tuple(clauses),
        tuple(witnesses),
        budget.scan_steps,
        statistics.short_cycle_candidates,
        statistics.long_cycle_candidates,
        statistics.dp_transitions,
        len(short_cycles),
        len(unique_long_cycles),
        statistics.packings_examined,
        statistics.known_duplicates,
        statistics.local_duplicates,
        budget.stop_reason,
        time.monotonic() - started,
    )
