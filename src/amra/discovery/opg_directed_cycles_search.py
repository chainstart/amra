from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
from typing import Iterator, Sequence

from amra.discovery.opg_coloring_search import (
    CNF,
    EdgeGraph,
    SolverResult,
    _shared_library_fingerprint,
    _atomic_json,
    _pipeline,
    decode_graph6,
    file_sha256,
    implementation_fingerprint,
    locate_tool,
    nauty_environment,
    parse_shard,
    solve_cnf_cadical,
    toolchain_fingerprint,
)


CHECKPOINT_SCHEMA = "amra.opg611.n16.checkpoint.v2"
SEARCH_IMPLEMENTATION_SCHEMA = "amra.opg611.n16.sat-cegar.v2"
CATALOGUE_SCHEMA = "amra.opg611.n16.missing-graphs.v1"
EXPECTED_N16_MISSING_GRAPHS = 497


def _json_fingerprint(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _command_version(
    command: Sequence[str],
    *,
    environment: dict[str, str] | None = None,
) -> str:
    try:
        process = subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"unavailable: {type(error).__name__}"
    output = (process.stdout + "\n" + process.stderr).strip()
    return output[:4096] if output else f"exit={process.returncode}; no version output"


@lru_cache(maxsize=None)
def _tool_identity(name: str) -> dict[str, object]:
    binary_identity = toolchain_fingerprint((name,))[name]
    path = Path(str(binary_identity["path"])).resolve()
    if name == "geng":
        version_command = [str(path), "-help"]
        output = _command_version(version_command, environment=nauty_environment())
        match = re.search(r"nauty-([0-9][0-9A-Za-z_.-]*)", str(path))
        version = match.group(1) if match else "unreported"
    elif name == "cadical":
        version_command = [str(path), "--version"]
        output = _command_version(version_command)
        version = output.splitlines()[0] if output else "unreported"
    else:
        version_command = [str(path), "-h"]
        output = _command_version(version_command)
        version = "unreported"
    return {
        "name": name,
        **binary_identity,
        "path": str(path),
        "version": version,
        "version_command": version_command,
        "version_output": output,
    }


@lru_cache(maxsize=1)
def _solver_identity() -> dict[str, object]:
    solver_class = _pysat_solver_class()
    solver_name = os.environ.get("AMRA_PYSAT_SOLVER", "glucose42")
    if solver_class is None:
        return {
            "backend": "cadical-cli",
            "tool": _tool_identity("cadical"),
        }
    solvers_module = importlib.import_module("pysat.solvers")
    native_module = importlib.import_module("pysolvers")
    module_paths = tuple(
        Path(value).resolve()
        for value in (
            getattr(solvers_module, "__file__", None),
            getattr(native_module, "__file__", None),
        )
        if value is not None
    )
    return {
        "backend": "python-sat",
        "solver_name": solver_name,
        "python": {
            "version": sys.version,
            "executable": str(Path(sys.executable).resolve()),
            "sha256": file_sha256(Path(sys.executable).resolve()),
            "dynamic_linkage": _shared_library_fingerprint(
                Path(sys.executable).resolve()
            ),
        },
        "python_sat_version": getattr(
            importlib.import_module("pysat"), "__version__", "unreported"
        ),
        "modules": [
            {
                "path": str(path),
                "sha256": file_sha256(path),
                "dynamic_linkage": (
                    _shared_library_fingerprint(path)
                    if ".so" in path.name
                    else {}
                ),
            }
            for path in module_paths
        ],
    }


@lru_cache(maxsize=1)
def _code_revision() -> dict[str, object]:
    source = Path(__file__).resolve()
    repository = source.parents[3]
    revision = _command_version(
        ["git", "-C", str(repository), "rev-parse", "HEAD"]
    ).splitlines()[0]
    dirty_output = _command_version(
        [
            "git",
            "-C",
            str(repository),
            "status",
            "--porcelain",
            "--",
            str(source.relative_to(repository)),
        ]
    )
    return {
        "git_commit": revision,
        "source_path": str(source),
        "source_sha256": file_sha256(source),
        "source_dirty": bool(dirty_output and not dirty_output.startswith("exit=")),
    }


def _pysat_solver_class():
    try:
        return importlib.import_module("pysat.solvers").Solver
    except ModuleNotFoundError:
        cache = Path("/home/biostar/.cache/amra/python/python-sat")
        if not cache.is_dir():
            return None
        sys.path.insert(0, str(cache))
        try:
            return importlib.import_module("pysat.solvers").Solver
        except ModuleNotFoundError:
            return None


class IncrementalSolver:
    def __init__(self, cnf: CNF) -> None:
        solver_class = _pysat_solver_class()
        self.cnf = cnf
        self.solver_name = os.environ.get("AMRA_PYSAT_SOLVER", "glucose42")
        if self.solver_name not in {"glucose42", "maplechrono", "minisat22"}:
            raise ValueError(
                "AMRA_PYSAT_SOLVER must support interrupt/clear_interrupt"
            )
        self.solver = (
            solver_class(name=self.solver_name, bootstrap_with=cnf.clauses)
            if solver_class is not None
            else None
        )

    def __enter__(self) -> "IncrementalSolver":
        return self

    def __exit__(self, *_: object) -> None:
        if self.solver is not None:
            self.solver.delete()

    def add_clause(self, clause: Sequence[int]) -> None:
        if self.solver is not None:
            self.solver.add_clause(list(clause))

    def solve(self, timeout_seconds: float) -> SolverResult:
        if self.solver is None:
            return solve_cnf_cadical(self.cnf, timeout_seconds)
        started = time.monotonic()
        timer = threading.Timer(max(0.01, timeout_seconds), self.solver.interrupt)
        timer.start()
        try:
            status = self.solver.solve_limited(expect_interrupt=True)
            model = self.solver.get_model() if status is True else None
        finally:
            timer.cancel()
            self.solver.clear_interrupt()
        return SolverResult(
            "sat" if status is True else "unsat" if status is False else "timeout",
            time.monotonic() - started,
            frozenset(literal for literal in (model or ()) if literal > 0),
            "",
            "",
        )


def solve_incremental_once(cnf: CNF, timeout_seconds: float) -> SolverResult:
    with IncrementalSolver(cnf) as solver:
        return solver.solve(timeout_seconds)


@dataclass(frozen=True)
class OrientationModel:
    vertex_count: int
    missing_edges: frozenset[tuple[int, int]]
    allowed_edges: tuple[tuple[int, int], ...]
    arc_variables: dict[tuple[int, int], int]

    def arc_literal(self, source: int, target: int) -> int | None:
        pair = (min(source, target), max(source, target))
        variable = self.arc_variables.get(pair)
        if variable is None:
            return None
        return variable if source < target else -variable


def _new_variable(cnf: CNF) -> int:
    cnf.variable_count += 1
    return cnf.variable_count


def add_at_most(cnf: CNF, literals: Sequence[int], maximum: int) -> None:
    """Forward sequential counter, valid for signed input literals."""

    values = tuple(literals)
    if maximum < 0:
        cnf.add_empty()
        return
    if maximum >= len(values):
        return
    threshold = maximum + 1
    previous: dict[int, int] = {}
    for index, literal in enumerate(values, start=1):
        current: dict[int, int] = {}
        for count in range(1, min(index, threshold) + 1):
            state = _new_variable(cnf)
            current[count] = state
            if count == 1:
                cnf.add(-literal, state)
            elif count - 1 in previous:
                cnf.add(-literal, -previous[count - 1], state)
            if count in previous:
                cnf.add(-previous[count], state)
        previous = current
    cnf.add(-previous[threshold])


def add_exactly(cnf: CNF, literals: Sequence[int], target: int) -> None:
    add_at_most(cnf, literals, target)
    add_at_most(cnf, tuple(-literal for literal in literals), len(literals) - target)


def add_exactly_combinatorial(
    cnf: CNF, literals: Sequence[int], target: int
) -> None:
    """Strong no-auxiliary encoding for the degree-14/15 master rows."""

    values = tuple(literals)
    for selected in combinations(values, target + 1):
        cnf.add(*(-literal for literal in selected))
    for selected in combinations(values, len(values) - target + 1):
        cnf.add(*selected)


def build_orientation_model(missing_graph: EdgeGraph) -> OrientationModel:
    n = missing_graph.vertex_count
    missing = frozenset(missing_graph.edges)
    allowed = tuple(
        pair
        for pair in combinations(range(n), 2)
        if pair not in missing
    )
    variables = {pair: index + 1 for index, pair in enumerate(allowed)}
    return OrientationModel(n, missing, allowed, variables)


def orientation_master_cnf(model: OrientationModel) -> CNF:
    cnf = CNF(len(model.allowed_edges), [])
    for vertex in range(model.vertex_count):
        outgoing = tuple(
            literal
            for other in range(model.vertex_count)
            if other != vertex
            and (literal := model.arc_literal(vertex, other)) is not None
        )
        add_exactly_combinatorial(cnf, outgoing, 7)
    _add_triangle_dominator_constraints(cnf, model)
    return cnf


def _add_triangle_dominator_constraints(cnf: CNF, model: OrientationModel) -> None:
    for triple in combinations(range(model.vertex_count), 3):
        first, second, third = triple
        orientations = (
            ((first, second), (second, third), (third, first)),
            ((second, first), (first, third), (third, second)),
        )
        for directed_triangle in orientations:
            trigger = tuple(
                model.arc_literal(source, target)
                for source, target in directed_triangle
            )
            if any(literal is None for literal in trigger):
                continue
            witnesses: list[int] = []
            for outside in range(model.vertex_count):
                if outside in triple:
                    continue
                domination = tuple(
                    model.arc_literal(outside, target) for target in triple
                )
                if any(literal is None for literal in domination):
                    continue
                witness = _new_variable(cnf)
                witnesses.append(witness)
                for literal in domination:
                    assert literal is not None
                    cnf.add(-witness, literal)
                cnf.add(
                    *(-int(literal) for literal in domination),
                    witness,
                )
            cnf.add(*(-int(literal) for literal in trigger), *witnesses)


def decode_orientation(
    model: OrientationModel, assignment: frozenset[int]
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right) if variable in assignment else (right, left)
        for (left, right), variable in model.arc_variables.items()
    )


def verify_orientation(
    model: OrientationModel, arcs: Sequence[tuple[int, int]]
) -> bool:
    arc_set = set(arcs)
    if len(arc_set) != len(model.allowed_edges):
        return False
    for left, right in model.allowed_edges:
        if ((left, right) in arc_set) == ((right, left) in arc_set):
            return False
    outdegrees = [0] * model.vertex_count
    for source, _ in arcs:
        outdegrees[source] += 1
    return all(degree == 7 for degree in outdegrees)


def _strong_components(
    n: int, arcs: Sequence[tuple[int, int]]
) -> tuple[frozenset[int], ...]:
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]
    for source, target in arcs:
        outgoing[source].append(target)
        incoming[target].append(source)

    seen: set[int] = set()
    order: list[int] = []

    def forward(vertex: int) -> None:
        seen.add(vertex)
        for other in outgoing[vertex]:
            if other not in seen:
                forward(other)
        order.append(vertex)

    for vertex in range(n):
        if vertex not in seen:
            forward(vertex)
    seen.clear()
    components: list[frozenset[int]] = []

    def reverse(vertex: int, component: set[int]) -> None:
        seen.add(vertex)
        component.add(vertex)
        for other in incoming[vertex]:
            if other not in seen:
                reverse(other, component)

    for vertex in reversed(order):
        if vertex in seen:
            continue
        component: set[int] = set()
        reverse(vertex, component)
        components.append(frozenset(component))
    return tuple(components)


def strong_connectivity_cut(
    model: OrientationModel, arcs: Sequence[tuple[int, int]]
) -> tuple[int, ...] | None:
    components = _strong_components(model.vertex_count, arcs)
    if len(components) == 1:
        return None
    arc_set = set(arcs)
    for component in components:
        has_outgoing = any(
            source in component and target not in component
            for source, target in arcs
        )
        if has_outgoing:
            continue
        literals = tuple(
            literal
            for source in component
            for target in range(model.vertex_count)
            if target not in component
            and (literal := model.arc_literal(source, target)) is not None
            and (source, target) not in arc_set
        )
        if not literals:
            return ()
        return literals
    raise RuntimeError("condensation DAG has no sink")


@dataclass(frozen=True)
class PackingEncoding:
    cnf: CNF
    selected_arc_variables: dict[tuple[int, int], int]


def pack_four_cycles_cnf(
    vertex_count: int, arcs: Sequence[tuple[int, int]]
) -> PackingEncoding:
    color_count = 4
    cnf = CNF(vertex_count * color_count, [])

    def selected_vertex(vertex: int, color: int) -> int:
        return color * vertex_count + vertex + 1

    selected_arcs: dict[tuple[int, int], int] = {}
    for color in range(color_count):
        for edge in range(len(arcs)):
            selected_arcs[(color, edge)] = _new_variable(cnf)

    outgoing = [[] for _ in range(vertex_count)]
    incoming = [[] for _ in range(vertex_count)]
    for edge, (source, target) in enumerate(arcs):
        outgoing[source].append(edge)
        incoming[target].append(edge)

    for color in range(color_count):
        cnf.add(*(selected_vertex(vertex, color) for vertex in range(vertex_count)))
        for vertex in range(vertex_count):
            chosen = selected_vertex(vertex, color)
            out_variables = tuple(
                selected_arcs[(color, edge)] for edge in outgoing[vertex]
            )
            in_variables = tuple(
                selected_arcs[(color, edge)] for edge in incoming[vertex]
            )
            cnf.add(-chosen, *out_variables)
            cnf.add(-chosen, *in_variables)
            add_at_most(cnf, out_variables, 1)
            add_at_most(cnf, in_variables, 1)
            for variable in out_variables:
                cnf.add(-variable, chosen)
            for variable in in_variables:
                cnf.add(-variable, chosen)
    for vertex in range(vertex_count):
        for first in range(color_count):
            for second in range(first + 1, color_count):
                cnf.add(
                    -selected_vertex(vertex, first),
                    -selected_vertex(vertex, second),
                )
    return PackingEncoding(cnf, selected_arcs)


def extract_cycle_packing(
    arcs: Sequence[tuple[int, int]],
    encoding: PackingEncoding,
    assignment: frozenset[int],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    cycles = []
    for color in range(4):
        selected = [
            arcs[edge]
            for edge in range(len(arcs))
            if encoding.selected_arc_variables[(color, edge)] in assignment
        ]
        successor = {source: target for source, target in selected}
        if not successor:
            raise ValueError("packing model selected no arc for a color")
        start = next(iter(successor))
        path: list[int] = []
        positions: dict[int, int] = {}
        vertex = start
        while vertex not in positions:
            positions[vertex] = len(path)
            path.append(vertex)
            vertex = successor[vertex]
        cycle_vertices = path[positions[vertex] :]
        cycle = tuple(
            (source, successor[source]) for source in cycle_vertices
        )
        cycles.append(cycle)
    vertex_sets = [
        {vertex for arc in cycle for vertex in arc} for cycle in cycles
    ]
    if any(
        vertex_sets[first] & vertex_sets[second]
        for first in range(4)
        for second in range(first + 1, 4)
    ):
        raise ValueError("packing model returned intersecting cycles")
    return tuple(cycles)


def packing_block_clause(
    model: OrientationModel,
    cycles: Sequence[Sequence[tuple[int, int]]],
) -> tuple[int, ...]:
    literals = []
    for cycle in cycles:
        for source, target in cycle:
            arc = model.arc_literal(source, target)
            if arc is None:
                raise ValueError("packing uses a missing edge")
            literals.append(-arc)
    return tuple(literals)


def directed_short_cycles(
    vertex_count: int,
    arcs: Sequence[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    arc_set = set(arcs)
    cycles: list[tuple[tuple[int, int], ...]] = []
    for vertices in combinations(range(vertex_count), 3):
        first, second, third = vertices
        for order in ((first, second, third), (first, third, second)):
            cycle = tuple(
                (order[index], order[(index + 1) % 3]) for index in range(3)
            )
            if all(arc in arc_set for arc in cycle):
                cycles.append(cycle)
    for vertices in combinations(range(vertex_count), 4):
        first = vertices[0]
        for tail in permutations(vertices[1:]):
            order = (first,) + tail
            cycle = tuple(
                (order[index], order[(index + 1) % 4]) for index in range(4)
            )
            if all(arc in arc_set for arc in cycle):
                cycles.append(cycle)
    return tuple(cycles)


def short_cycle_packing_clauses(
    model: OrientationModel,
    arcs: Sequence[tuple[int, int]],
    *,
    limit: int = 65_536,
) -> tuple[tuple[int, ...], ...]:
    cycles = directed_short_cycles(model.vertex_count, arcs)
    masks = tuple(
        sum(1 << vertex for vertex in {item for arc in cycle for item in arc})
        for cycle in cycles
    )
    clauses: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()

    def extend(start: int, used: int, chosen: tuple[int, ...]) -> None:
        if len(clauses) >= limit:
            return
        if len(chosen) == 4:
            clause = packing_block_clause(
                model, tuple(cycles[index] for index in chosen)
            )
            canonical = tuple(sorted(set(clause)))
            if canonical not in seen:
                seen.add(canonical)
                clauses.append(canonical)
            return
        for index in range(start, len(cycles)):
            if masks[index] & used:
                continue
            extend(index + 1, used | masks[index], chosen + (index,))
            if len(clauses) >= limit:
                return

    extend(0, 0, ())
    return tuple(clauses)


def violated_four_cycle_dominator_constraints(
    cnf: CNF,
    model: OrientationModel,
    arcs: Sequence[tuple[int, int]],
    known_cycles: set[tuple[tuple[int, int], ...]],
    *,
    limit: int = 256,
) -> tuple[tuple[int, ...], ...]:
    arc_set = set(arcs)
    generated: list[tuple[int, ...]] = []
    added_cycles = 0
    for cycle in directed_short_cycles(model.vertex_count, arcs):
        if len(cycle) != 4 or cycle in known_cycles:
            continue
        vertices = tuple(source for source, _ in cycle)
        if any(
            sum((outside, target) in arc_set for target in vertices) >= 3
            for outside in range(model.vertex_count)
            if outside not in vertices
        ):
            continue
        trigger = tuple(
            model.arc_literal(source, target) for source, target in cycle
        )
        if any(literal is None for literal in trigger):
            continue
        witnesses: list[int] = []
        for outside in range(model.vertex_count):
            if outside in vertices:
                continue
            for targets in combinations(vertices, 3):
                domination = tuple(
                    model.arc_literal(outside, target) for target in targets
                )
                if any(literal is None for literal in domination):
                    continue
                witness = _new_variable(cnf)
                witnesses.append(witness)
                for literal in domination:
                    assert literal is not None
                    clause = (-witness, literal)
                    cnf.add(*clause)
                    generated.append(clause)
                clause = (
                    *(-int(literal) for literal in domination),
                    witness,
                )
                cnf.add(*clause)
                generated.append(clause)
        clause = (*(-int(literal) for literal in trigger), *witnesses)
        cnf.add(*clause)
        generated.append(clause)
        known_cycles.add(cycle)
        added_cycles += 1
        if added_cycles >= limit:
            break
    return tuple(generated)


def iter_missing_graphs_n16(
    shard: tuple[int, int] | None = None,
) -> Iterator[EdgeGraph]:
    geng = str(locate_tool("geng"))
    command = [geng, "-q", "16", "8:8"]
    for global_index, line in enumerate(_pipeline((command,))):
        if shard and global_index % shard[1] != shard[0]:
            continue
        yield decode_graph6(line)


def _load_n16_catalogue() -> tuple[EdgeGraph, ...]:
    catalogue = tuple(iter_missing_graphs_n16())
    if len(catalogue) != EXPECTED_N16_MISSING_GRAPHS:
        raise RuntimeError(
            "unexpected n=16 eight-edge catalogue size: "
            f"{len(catalogue)} != {EXPECTED_N16_MISSING_GRAPHS}"
        )
    encodings = tuple(graph.encoding for graph in catalogue)
    if len(set(encodings)) != len(encodings):
        raise RuntimeError("n=16 eight-edge catalogue contains duplicate graph6 rows")
    if any(
        graph.vertex_count != 16 or len(graph.edges) != 8
        for graph in catalogue
    ):
        raise RuntimeError("n=16 catalogue contains an object outside the 16/8 layer")
    return catalogue


def _catalogue_identity(
    catalogue: Sequence[EdgeGraph],
    shard: tuple[int, int] | None,
) -> dict[str, object]:
    selected = tuple(
        (global_index, graph)
        for global_index, graph in enumerate(catalogue)
        if shard is None or global_index % shard[1] == shard[0]
    )
    global_rows = [graph.encoding for graph in catalogue]
    shard_rows = [
        {"catalogue_index": index, "graph6": graph.encoding}
        for index, graph in selected
    ]
    payload: dict[str, object] = {
        "schema": CATALOGUE_SCHEMA,
        "global_count": len(global_rows),
        "global_ordered_sha256": _json_fingerprint(global_rows),
        "shard": list(shard) if shard else None,
        "shard_count": len(shard_rows),
        "shard_ordered_sha256": _json_fingerprint(shard_rows),
    }
    payload["fingerprint"] = _json_fingerprint(payload)
    return payload


def _search_contract(
    catalogue: Sequence[EdgeGraph],
    *,
    per_missing_graph_seconds: float,
    max_cegar_iterations: int,
    proofs: bool,
    shard: tuple[int, int] | None,
) -> dict[str, object]:
    source = Path(__file__).resolve()
    shared_source = Path(
        str(
            importlib.import_module(
                "amra.discovery.opg_coloring_search"
            ).__file__
        )
    ).resolve()
    toolchain: dict[str, object] = {
        "geng": _tool_identity("geng"),
        "solver": _solver_identity(),
    }
    if proofs:
        toolchain["proof_generator"] = _tool_identity("cadical")
        toolchain["proof_checker"] = _tool_identity("drat-trim")
    implementation = {
        "schema": SEARCH_IMPLEMENTATION_SCHEMA,
        "sources": [
            {"path": str(source), "sha256": file_sha256(source)},
            {
                "path": str(shared_source),
                "sha256": file_sha256(shared_source),
            },
        ],
        "fingerprint": implementation_fingerprint(source, shared_source),
    }
    config = {
        "problem": "opg611-k4-n16",
        "vertex_count": 16,
        "missing_edge_count": 8,
        "required_outdegree": 7,
        "shard": list(shard) if shard else None,
        "per_missing_graph_seconds": float(per_missing_graph_seconds),
        "max_cegar_iterations": int(max_cegar_iterations),
        "proofs": bool(proofs),
    }
    config["fingerprint"] = _json_fingerprint(config)
    toolchain_payload = {
        "tools": toolchain,
        "fingerprint": _json_fingerprint(toolchain),
    }
    contract: dict[str, object] = {
        "implementation": implementation,
        "toolchain": toolchain_payload,
        "config": config,
        "catalogue": _catalogue_identity(catalogue, shard),
    }
    contract["fingerprint"] = _json_fingerprint(contract)
    return contract


def _sharded_catalogue(
    catalogue: Sequence[EdgeGraph],
    shard: tuple[int, int] | None,
) -> tuple[tuple[int, EdgeGraph], ...]:
    return tuple(
        (global_index, graph)
        for global_index, graph in enumerate(catalogue)
        if shard is None or global_index % shard[1] == shard[0]
    )


def _save_unsat_proof(
    directory: Path,
    stem: str,
    cnf: CNF,
    metadata: dict[str, object],
) -> dict[str, object]:
    directory.mkdir(parents=True, exist_ok=True)
    formula = directory / f"{stem}.cnf"
    proof = directory / f"{stem}.drat"
    formula.write_text(cnf.dimacs(), encoding="ascii")
    cadical = _tool_identity("cadical")
    checker_tool = _tool_identity("drat-trim")
    command = [
        str(cadical["path"]),
        "-q",
        "--no-binary",
        "--checkproof=true",
        str(formula),
        str(proof),
    ]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    checker_command = [
        str(checker_tool["path"]),
        str(formula),
        str(proof),
    ]
    checker = subprocess.run(
        checker_command,
        capture_output=True,
        text=True,
        check=False,
    )
    independently_verified = (
        process.returncode == 20
        # drat-trim 2.2 returns 1 for an input formula that is already
        # trivially UNSAT because its `sts` variable is never updated, even
        # though it emits the unambiguous `s VERIFIED` status line.
        and checker.returncode in {0, 1}
        and any(
            line.strip() == "s VERIFIED"
            for line in checker.stdout.splitlines()
        )
    )
    manifest = {
        **metadata,
        "proof_manifest_schema": "amra.unsat-proof-manifest.v2",
        "formula_path": str(formula),
        "formula_sha256": file_sha256(formula),
        "proof_path": str(proof),
        "proof_sha256": file_sha256(proof) if proof.is_file() else None,
        "commands": {
            "proof_generator": command,
            "proof_checker": checker_command,
        },
        "tools": {
            "proof_generator": cadical,
            "proof_checker": checker_tool,
        },
        "code_revision": _code_revision(),
        "cadical_exit": process.returncode,
        "cadical_stdout": process.stdout,
        "cadical_stderr": process.stderr,
        "independent_checker_exit": checker.returncode,
        "independent_checker_stdout": checker.stdout,
        "independent_checker_stderr": checker.stderr,
        "proof_status": (
            "independently_verified"
            if independently_verified
            else "independent_verification_failed"
        ),
    }
    _atomic_json(directory / f"{stem}.json", manifest)
    return manifest


def search_missing_graph(
    missing_graph: EdgeGraph,
    *,
    timeout_seconds: float,
    max_cegar_iterations: int,
    proof_directory: Path | None = None,
) -> dict[str, object]:
    model = build_orientation_model(missing_graph)
    master = orientation_master_cnf(model)
    started = time.monotonic()
    strong_cuts = 0
    four_cycle_cuts = 0
    packing_cuts = 0
    known_four_cycles: set[tuple[tuple[int, int], ...]] = set()
    with IncrementalSolver(master) as master_solver:
        while strong_cuts + four_cycle_cuts + packing_cuts < max_cegar_iterations:
            remaining = timeout_seconds - (time.monotonic() - started)
            if remaining <= 0:
                return {
                    "status": "timeout",
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                }
            result = master_solver.solve(remaining)
            if result.status == "unsat":
                payload: dict[str, object] = {
                    "status": "excluded",
                    "missing_graph6": missing_graph.encoding,
                    "master_variables": master.variable_count,
                    "master_clauses": len(master.clauses),
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                    "elapsed_seconds": time.monotonic() - started,
                }
                if proof_directory is not None:
                    payload["proof"] = _save_unsat_proof(
                        proof_directory,
                        f"missing-{missing_graph.encoding.encode().hex()}",
                        master,
                        payload,
                    )
                return payload
            if result.status != "sat":
                return {
                    "status": result.status,
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                }
            arcs = decode_orientation(model, result.assignment)
            if not verify_orientation(model, arcs):
                raise RuntimeError("invalid orientation returned by SAT solver")
            connectivity = strong_connectivity_cut(model, arcs)
            if connectivity is not None:
                clause = connectivity if connectivity else ()
                if clause:
                    master.add(*clause)
                else:
                    master.add_empty()
                master_solver.add_clause(clause)
                strong_cuts += 1
                continue
            old_known_count = len(known_four_cycles)
            four_cycle_clauses = violated_four_cycle_dominator_constraints(
                master,
                model,
                arcs,
                known_four_cycles,
            )
            if four_cycle_clauses:
                for clause in four_cycle_clauses:
                    master_solver.add_clause(clause)
                four_cycle_cuts += len(known_four_cycles) - old_known_count
                continue
            short_clauses = short_cycle_packing_clauses(model, arcs)
            if short_clauses:
                for clause in short_clauses:
                    master.add(*clause)
                    master_solver.add_clause(clause)
                packing_cuts += len(short_clauses)
                continue
            packing = pack_four_cycles_cnf(model.vertex_count, arcs)
            packing_remaining = timeout_seconds - (time.monotonic() - started)
            if packing_remaining <= 0:
                return {
                    "status": "timeout",
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                }
            pack_result = solve_incremental_once(packing.cnf, packing_remaining)
            if pack_result.status == "unsat":
                candidate = {
                    "status": "candidate",
                    "missing_graph6": missing_graph.encoding,
                    "arcs": [list(arc) for arc in arcs],
                    "outdegrees": [
                        sum(1 for source, _ in arcs if source == vertex)
                        for vertex in range(model.vertex_count)
                    ],
                    "packing_variables": packing.cnf.variable_count,
                    "packing_clauses": len(packing.cnf.clauses),
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                    "elapsed_seconds": time.monotonic() - started,
                }
                if proof_directory is not None:
                    candidate["proof"] = _save_unsat_proof(
                        proof_directory,
                        f"candidate-{missing_graph.encoding.encode().hex()}",
                        packing.cnf,
                        candidate,
                    )
                return candidate
            if pack_result.status != "sat":
                return {
                    "status": f"packing_{pack_result.status}",
                    "strong_cuts": strong_cuts,
                    "four_cycle_cuts": four_cycle_cuts,
                    "packing_cuts": packing_cuts,
                }
            cycles = extract_cycle_packing(arcs, packing, pack_result.assignment)
            clause = packing_block_clause(model, cycles)
            master.add(*clause)
            master_solver.add_clause(clause)
            packing_cuts += 1
    return {
        "status": "iteration_limit",
        "strong_cuts": strong_cuts,
        "four_cycle_cuts": four_cycle_cuts,
        "packing_cuts": packing_cuts,
    }


def _attempt_event_id(
    contract_fingerprint: str,
    shard: tuple[int, int] | None,
    catalogue_index: int,
    graph6: str,
    attempt: int,
) -> str:
    return _json_fingerprint(
        {
            "contract_fingerprint": contract_fingerprint,
            "shard": list(shard) if shard else None,
            "catalogue_index": catalogue_index,
            "graph6": graph6,
            "attempt": attempt,
        }
    )


def _load_event_index(
    path: Path,
    *,
    contract_fingerprint: str,
) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    events: dict[str, dict[str, object]] = {}
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError(f"event line {line_number} is not an object")
        if event.get("event_schema") != "amra.opg611.search-event.v2":
            raise ValueError(f"event line {line_number} has an incompatible schema")
        if event.get("contract_fingerprint") != contract_fingerprint:
            raise ValueError(f"event line {line_number} has a foreign contract")
        required = {
            "event_schema",
            "event_id",
            "contract_fingerprint",
            "time",
            "shard",
            "missing_graph_index",
            "catalogue_index",
            "graph6",
            "attempt",
            "attempt_kind",
            "result",
        }
        if set(event) != required:
            raise ValueError(f"event line {line_number} has an invalid schema")
        event_id = event.get("event_id")
        if not isinstance(event_id, str):
            raise ValueError(f"event line {line_number} has no event_id")
        raw_shard = event["shard"]
        if raw_shard is None:
            event_shard = None
        elif (
            isinstance(raw_shard, list)
            and len(raw_shard) == 2
            and all(
                isinstance(item, int) and not isinstance(item, bool)
                for item in raw_shard
            )
            and raw_shard[1] > 0
            and 0 <= raw_shard[0] < raw_shard[1]
        ):
            event_shard = (raw_shard[0], raw_shard[1])
        else:
            raise ValueError(f"event line {line_number} has an invalid shard")
        catalogue_index = event["catalogue_index"]
        local_index = event["missing_graph_index"]
        attempt = event["attempt"]
        graph6 = event["graph6"]
        if (
            not isinstance(catalogue_index, int)
            or isinstance(catalogue_index, bool)
            or catalogue_index < 0
            or not isinstance(local_index, int)
            or isinstance(local_index, bool)
            or local_index < 0
            or not isinstance(attempt, int)
            or isinstance(attempt, bool)
            or attempt < 1
            or not isinstance(graph6, str)
            or not isinstance(event["result"], dict)
        ):
            raise ValueError(f"event line {line_number} has invalid task fields")
        expected_id = _attempt_event_id(
            contract_fingerprint,
            event_shard,
            catalogue_index,
            graph6,
            attempt,
        )
        if event_id != expected_id:
            raise ValueError(f"event line {line_number} has an invalid event_id")
        expected_kind = "initial" if attempt == 1 else "hard_retry"
        if event["attempt_kind"] != expected_kind:
            raise ValueError(f"event line {line_number} has an invalid attempt kind")
        if not isinstance(event["result"].get("status"), str):
            raise ValueError(f"event line {line_number} has no result status")
        prior = events.get(event_id)
        if prior is not None and prior != event:
            raise ValueError(f"conflicting duplicate event_id {event_id}")
        events[event_id] = event
    return events


def _append_event_once(
    path: Path,
    event: dict[str, object],
    event_index: dict[str, dict[str, object]],
) -> None:
    event_id = str(event["event_id"])
    prior = event_index.get(event_id)
    if prior is not None:
        if prior != event:
            raise ValueError(f"conflicting duplicate event_id {event_id}")
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    event_index[event_id] = event


def _validate_checkpoint(
    state: object,
    *,
    contract: dict[str, object],
    sharded_catalogue: Sequence[tuple[int, EdgeGraph]],
    shard: tuple[int, int] | None,
) -> dict[str, object]:
    if not isinstance(state, dict):
        raise ValueError("checkpoint is not a JSON object")
    required = {
        "schema_version",
        "problem",
        "contract",
        "contract_fingerprint",
        "next_missing_graph",
        "processed",
        "attempts",
        "excluded",
        "candidate",
        "hard_queue",
        "status",
        "shard",
    }
    if set(state) != required:
        missing = sorted(required - set(state))
        unexpected = sorted(set(state) - required)
        raise ValueError(
            f"checkpoint schema mismatch; missing={missing}, unexpected={unexpected}"
        )
    if state["schema_version"] != CHECKPOINT_SCHEMA:
        raise ValueError("checkpoint schema version does not match")
    if state["problem"] != "opg611-k4-n16":
        raise ValueError("checkpoint problem does not match")
    if state["shard"] != (list(shard) if shard else None):
        raise ValueError("checkpoint shard does not match")
    if state["contract"] != contract:
        raise ValueError("checkpoint implementation/tool/config/catalogue contract changed")
    if state["contract_fingerprint"] != contract["fingerprint"]:
        raise ValueError("checkpoint contract fingerprint does not match")
    for field in ("next_missing_graph", "processed", "attempts", "excluded"):
        value = state[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"checkpoint field {field} must be a nonnegative integer")
    next_index = int(state["next_missing_graph"])
    if next_index > len(sharded_catalogue):
        raise ValueError("checkpoint cursor is outside the shard catalogue")
    if state["processed"] != next_index:
        raise ValueError("checkpoint processed count does not equal its atomic cursor")
    if state["attempts"] < state["processed"]:
        raise ValueError("checkpoint attempts cannot be smaller than processed")
    if state["excluded"] > state["processed"]:
        raise ValueError("checkpoint excluded count exceeds processed")
    hard_queue = state["hard_queue"]
    if not isinstance(hard_queue, list):
        raise ValueError("checkpoint hard_queue must be a list")
    seen: set[int] = set()
    for entry in hard_queue:
        if not isinstance(entry, dict) or set(entry) != {
            "missing_graph_index",
            "catalogue_index",
            "graph6",
            "status",
            "attempts",
        }:
            raise ValueError("checkpoint hard_queue entry has an invalid schema")
        local_index = entry["missing_graph_index"]
        global_index = entry["catalogue_index"]
        attempts = entry["attempts"]
        if (
            not isinstance(local_index, int)
            or isinstance(local_index, bool)
            or not 0 <= local_index < next_index
            or local_index in seen
        ):
            raise ValueError("checkpoint hard_queue has an invalid local index")
        seen.add(local_index)
        expected_global, expected_graph = sharded_catalogue[local_index]
        if (
            global_index != expected_global
            or entry["graph6"] != expected_graph.encoding
        ):
            raise ValueError("checkpoint hard_queue does not match the catalogue")
        if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
            raise ValueError("checkpoint hard_queue attempt count is invalid")
        if entry["status"] in {"excluded", "candidate"}:
            raise ValueError("resolved result cannot remain in hard_queue")
    candidate = state["candidate"]
    if candidate is not None and not isinstance(candidate, dict):
        raise ValueError("checkpoint candidate must be null or an object")
    resolved = int(state["excluded"]) + len(hard_queue)
    if candidate is None and resolved != int(state["processed"]):
        raise ValueError("checkpoint does not account for every processed graph")
    if candidate is not None and resolved + 1 != int(state["processed"]):
        raise ValueError("candidate checkpoint accounting is inconsistent")
    if state["status"] not in {
        "running",
        "paused_budget",
        "complete",
        "complete_with_hard_queue",
        "candidate_pending_independent_verification",
    }:
        raise ValueError("checkpoint status is invalid")
    if candidate is not None and state["status"] != (
        "candidate_pending_independent_verification"
    ):
        raise ValueError("candidate checkpoint has a non-candidate status")
    if candidate is None and state["status"] == (
        "candidate_pending_independent_verification"
    ):
        raise ValueError("candidate status has no candidate payload")
    if state["status"] == "complete" and (
        next_index != len(sharded_catalogue) or hard_queue
    ):
        raise ValueError("complete checkpoint has unfinished catalogue work")
    if state["status"] == "complete_with_hard_queue" and (
        next_index != len(sharded_catalogue) or not hard_queue
    ):
        raise ValueError("hard-queue completion status is inconsistent")
    return state


def _validate_event_accounting(
    state: dict[str, object],
    event_index: dict[str, dict[str, object]],
    *,
    sharded_catalogue: Sequence[tuple[int, EdgeGraph]],
    shard: tuple[int, int] | None,
) -> None:
    grouped: dict[int, list[dict[str, object]]] = {}
    for event in event_index.values():
        if event["shard"] != (list(shard) if shard else None):
            raise ValueError("event log contains a foreign shard")
        local_index = int(event["missing_graph_index"])
        if not 0 <= local_index < len(sharded_catalogue):
            raise ValueError("event log local index is outside the shard")
        expected_global, expected_graph = sharded_catalogue[local_index]
        if (
            event["catalogue_index"] != expected_global
            or event["graph6"] != expected_graph.encoding
        ):
            raise ValueError("event log task does not match the catalogue")
        grouped.setdefault(local_index, []).append(event)
    for events in grouped.values():
        events.sort(key=lambda item: int(item["attempt"]))
        attempts = [int(event["attempt"]) for event in events]
        if attempts != list(range(1, len(events) + 1)):
            raise ValueError("event log attempts are not contiguous")
        for event in events[:-1]:
            if event["result"]["status"] in {"excluded", "candidate"}:
                raise ValueError("event log retries an already resolved graph")

    cursor = int(state["next_missing_graph"])
    hard_by_index = {
        int(entry["missing_graph_index"]): entry
        for entry in state["hard_queue"]
    }
    applied_attempts = 0
    derived_excluded = 0
    derived_candidates = 0
    pending_events = 0
    for local_index in range(cursor):
        events = grouped.pop(local_index, None)
        if not events:
            raise ValueError("checkpoint has a processed graph with no event")
        hard = hard_by_index.get(local_index)
        if hard is not None:
            hard_attempts = int(hard["attempts"])
            if len(events) not in {hard_attempts, hard_attempts + 1}:
                raise ValueError("hard_queue attempts disagree with the event log")
            applied = events[hard_attempts - 1]
            if (
                applied["result"]["status"] != hard["status"]
                or applied["result"]["status"] in {"excluded", "candidate"}
            ):
                raise ValueError("hard_queue status disagrees with the event log")
            if len(events) == hard_attempts + 1:
                pending_events += 1
            applied_attempts += hard_attempts
            continue
        latest = events[-1]
        status = latest["result"]["status"]
        applied_attempts += len(events)
        if status == "excluded":
            derived_excluded += 1
        elif status == "candidate" and latest["result"] == state["candidate"]:
            derived_candidates += 1
        else:
            raise ValueError("resolved checkpoint disagrees with its latest event")

    for local_index, events in grouped.items():
        if local_index != cursor or len(events) != 1:
            raise ValueError("event log runs ahead of the checkpoint cursor")
        pending_events += 1
    if pending_events > 1:
        raise ValueError("event log has more than one unapplied write-ahead event")
    if applied_attempts != int(state["attempts"]):
        raise ValueError("checkpoint attempt count disagrees with the event log")
    if derived_excluded != int(state["excluded"]):
        raise ValueError("checkpoint excluded count disagrees with the event log")
    expected_candidates = 1 if state["candidate"] is not None else 0
    if derived_candidates != expected_candidates:
        raise ValueError("checkpoint candidate disagrees with the event log")


def run_n16_search(
    output: Path,
    wall_seconds: float,
    per_missing_graph_seconds: float,
    max_cegar_iterations: int,
    max_missing_graphs: int = 0,
    proofs: bool = False,
    shard: tuple[int, int] | None = None,
) -> dict[str, object]:
    if not math.isfinite(wall_seconds) or wall_seconds < 0:
        raise ValueError("wall_seconds must be finite and nonnegative")
    if (
        not math.isfinite(per_missing_graph_seconds)
        or per_missing_graph_seconds <= 0
    ):
        raise ValueError("per_missing_graph_seconds must be finite and positive")
    if (
        not isinstance(max_cegar_iterations, int)
        or isinstance(max_cegar_iterations, bool)
        or max_cegar_iterations <= 0
    ):
        raise ValueError("max_cegar_iterations must be a positive integer")
    if (
        not isinstance(max_missing_graphs, int)
        or isinstance(max_missing_graphs, bool)
        or max_missing_graphs < 0
    ):
        raise ValueError("max_missing_graphs must be a nonnegative integer")
    if shard is not None and (
        len(shard) != 2
        or shard[1] <= 0
        or not 0 <= shard[0] < shard[1]
    ):
        raise ValueError("shard must satisfy 0 <= index < count")
    output.mkdir(parents=True, exist_ok=True)
    state_path = output / "state.json"
    events_path = output / "events.jsonl"
    catalogue = _load_n16_catalogue()
    sharded_catalogue = _sharded_catalogue(catalogue, shard)
    contract = _search_contract(
        catalogue,
        per_missing_graph_seconds=per_missing_graph_seconds,
        max_cegar_iterations=max_cegar_iterations,
        proofs=proofs,
        shard=shard,
    )
    initial_state: dict[str, object] = {
        "schema_version": CHECKPOINT_SCHEMA,
        "problem": "opg611-k4-n16",
        "contract": contract,
        "contract_fingerprint": contract["fingerprint"],
        "next_missing_graph": 0,
        "processed": 0,
        "attempts": 0,
        "excluded": 0,
        "candidate": None,
        "hard_queue": [],
        "status": "running",
        "shard": list(shard) if shard else None,
    }
    if state_path.exists():
        loaded = json.loads(state_path.read_text(encoding="utf-8"))
        state = _validate_checkpoint(
            loaded,
            contract=contract,
            sharded_catalogue=sharded_catalogue,
            shard=shard,
        )
    else:
        if events_path.exists() and events_path.read_text(encoding="utf-8").strip():
            raise ValueError("event log exists without a compatible checkpoint")
        state = initial_state
        _atomic_json(state_path, state)
    event_index = _load_event_index(
        events_path,
        contract_fingerprint=str(contract["fingerprint"]),
    )
    _validate_event_accounting(
        state,
        event_index,
        sharded_catalogue=sharded_catalogue,
        shard=shard,
    )
    if state["candidate"] is not None:
        return state
    state["status"] = "running"
    _atomic_json(state_path, state)

    deadline = time.monotonic() + wall_seconds
    processed_this_run = 0

    def budget_exhausted() -> bool:
        return time.monotonic() >= deadline or (
            bool(max_missing_graphs)
            and processed_this_run >= max_missing_graphs
        )

    def pause() -> dict[str, object]:
        state["status"] = "paused_budget"
        _atomic_json(state_path, state)
        return state

    def run_or_replay(
        local_index: int,
        global_index: int,
        missing_graph: EdgeGraph,
        attempt: int,
    ) -> tuple[dict[str, object], dict[str, object]] | None:
        event_id = _attempt_event_id(
            str(contract["fingerprint"]),
            shard,
            global_index,
            missing_graph.encoding,
            attempt,
        )
        prior = event_index.get(event_id)
        if prior is not None:
            if (
                prior.get("shard") != (list(shard) if shard else None)
                or prior.get("missing_graph_index") != local_index
                or prior.get("catalogue_index") != global_index
                or prior.get("graph6") != missing_graph.encoding
                or prior.get("attempt") != attempt
                or not isinstance(prior.get("result"), dict)
            ):
                raise ValueError(f"event {event_id} does not match its catalogue task")
            return dict(prior["result"]), prior
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        result = search_missing_graph(
            missing_graph,
            timeout_seconds=min(per_missing_graph_seconds, max(0.01, remaining)),
            max_cegar_iterations=max_cegar_iterations,
            proof_directory=(output / "proofs") if proofs else None,
        )
        event: dict[str, object] = {
            "event_schema": "amra.opg611.search-event.v2",
            "event_id": event_id,
            "contract_fingerprint": contract["fingerprint"],
            "time": time.time(),
            "shard": list(shard) if shard else None,
            "missing_graph_index": local_index,
            "catalogue_index": global_index,
            "graph6": missing_graph.encoding,
            "attempt": attempt,
            "attempt_kind": "initial" if attempt == 1 else "hard_retry",
            "result": result,
        }
        _append_event_once(events_path, event, event_index)
        return result, event

    # Retry each unresolved object once at startup.  The write-ahead event ID
    # makes a crash between event append and checkpoint replacement replayable.
    retry_snapshot = [dict(entry) for entry in state["hard_queue"]]
    for queued in retry_snapshot:
        if budget_exhausted():
            return pause()
        local_index = int(queued["missing_graph_index"])
        global_index, missing_graph = sharded_catalogue[local_index]
        attempt = int(queued["attempts"]) + 1
        outcome = run_or_replay(
            local_index,
            global_index,
            missing_graph,
            attempt,
        )
        if outcome is None:
            return pause()
        result, event = outcome
        status = result.get("status")
        if not isinstance(status, str):
            raise RuntimeError("search result has no status")
        queue = [
            entry
            for entry in state["hard_queue"]
            if entry["missing_graph_index"] != local_index
        ]
        state["attempts"] = int(state["attempts"]) + 1
        processed_this_run += 1
        if status == "excluded":
            state["excluded"] = int(state["excluded"]) + 1
        elif status == "candidate":
            state["candidate"] = result
            state["hard_queue"] = queue
            state["status"] = "candidate_pending_independent_verification"
            _atomic_json(output / "candidate.json", event)
            _atomic_json(state_path, state)
            return state
        else:
            queue.append(
                {
                    "missing_graph_index": local_index,
                    "catalogue_index": global_index,
                    "graph6": missing_graph.encoding,
                    "status": status,
                    "attempts": attempt,
                }
            )
        state["hard_queue"] = queue
        _atomic_json(state_path, state)

    for local_index in range(
        int(state["next_missing_graph"]), len(sharded_catalogue)
    ):
        if budget_exhausted():
            return pause()
        global_index, missing_graph = sharded_catalogue[local_index]
        outcome = run_or_replay(local_index, global_index, missing_graph, 1)
        if outcome is None:
            return pause()
        result, event = outcome
        status = result.get("status")
        if not isinstance(status, str):
            raise RuntimeError("search result has no status")
        state["processed"] = int(state["processed"]) + 1
        state["attempts"] = int(state["attempts"]) + 1
        processed_this_run += 1
        state["next_missing_graph"] = local_index + 1
        if status == "excluded":
            state["excluded"] = int(state["excluded"]) + 1
        elif status == "candidate":
            state["candidate"] = result
            state["status"] = "candidate_pending_independent_verification"
            _atomic_json(output / "candidate.json", event)
            _atomic_json(state_path, state)
            return state
        else:
            queue = list(state["hard_queue"])
            queue.append(
                {
                    "missing_graph_index": local_index,
                    "catalogue_index": global_index,
                    "graph6": missing_graph.encoding,
                    "status": status,
                    "attempts": 1,
                }
            )
            state["hard_queue"] = queue
        _atomic_json(state_path, state)

    state["status"] = (
        "complete_with_hard_queue" if state["hard_queue"] else "complete"
    )
    _atomic_json(state_path, state)
    return state


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="OPG-611 k=4 complete-order n=16 SAT/CEGAR search."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--per-missing-graph-seconds", type=float, default=300.0)
    parser.add_argument("--max-cegar-iterations", type=int, default=100_000)
    parser.add_argument("--max-missing-graphs", type=int, default=0)
    parser.add_argument("--proofs", action="store_true")
    parser.add_argument("--shard", type=parse_shard)
    arguments = parser.parse_args(argv)
    result = run_n16_search(
        arguments.output,
        arguments.wall_seconds,
        arguments.per_missing_graph_seconds,
        arguments.max_cegar_iterations,
        arguments.max_missing_graphs,
        arguments.proofs,
        arguments.shard,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
