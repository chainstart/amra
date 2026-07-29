from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence


COLORING_CHECKPOINT_SCHEMA = 2


@dataclass(frozen=True)
class EdgeGraph:
    """A loopless graph whose edge identities are significant.

    Repeated endpoint pairs are allowed, which is required for OPG-37271.
    """

    vertex_count: int
    edges: tuple[tuple[int, int], ...]
    encoding: str

    def __post_init__(self) -> None:
        if self.vertex_count < 0:
            raise ValueError("vertex_count must be non-negative")
        for left, right in self.edges:
            if not 0 <= left < right < self.vertex_count:
                raise ValueError(f"invalid loopless normalized edge {(left, right)}")

    @property
    def degrees(self) -> tuple[int, ...]:
        values = [0] * self.vertex_count
        for left, right in self.edges:
            values[left] += 1
            values[right] += 1
        return tuple(values)


@dataclass
class CNF:
    variable_count: int
    clauses: list[tuple[int, ...]]

    def add(self, *literals: int) -> None:
        if not literals:
            raise ValueError("empty clauses must be added explicitly")
        self.clauses.append(tuple(literals))

    def add_empty(self) -> None:
        self.clauses.append(())

    def extend(self, clauses: Iterable[Sequence[int]]) -> None:
        self.clauses.extend(tuple(clause) for clause in clauses)

    def dimacs(self) -> str:
        rows = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return "\n".join(rows) + "\n"


@dataclass(frozen=True)
class SolverResult:
    status: str
    elapsed_seconds: float
    assignment: frozenset[int]
    stdout: str
    stderr: str


def _edge_pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for right in range(1, n) for left in range(right))


def decode_graph6(record: str) -> EdgeGraph:
    value = record.strip()
    if value.startswith(">>graph6<<"):
        value = value[10:]
    if not value:
        raise ValueError("empty graph6 record")
    if value[0] == "~":
        raise ValueError("only compact graph6 orders up to 62 are supported")
    n = ord(value[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("invalid compact graph6 order")
    required_bits = n * (n - 1) // 2
    required_characters = (required_bits + 5) // 6
    if len(value) != 1 + required_characters:
        raise ValueError(
            f"graph6 order {n} requires {required_characters} payload characters"
        )
    bits: list[int] = []
    for char in value[1:]:
        number = ord(char) - 63
        if not 0 <= number < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((number >> shift) & 1 for shift in range(5, -1, -1))
    if any(bits[required_bits:]):
        raise ValueError("graph6 padding bits must be zero")
    edges = tuple(edge for bit, edge in zip(bits[:required_bits], _edge_pairs(n)) if bit)
    return EdgeGraph(n, edges, value)


def decode_multig_text(record: str) -> EdgeGraph:
    fields = [int(item) for item in record.split()]
    if len(fields) < 2:
        raise ValueError("truncated multig -T record")
    n, distinct_edges = fields[:2]
    if len(fields) != 2 + 3 * distinct_edges:
        raise ValueError("invalid multig -T record length")
    edges: list[tuple[int, int]] = []
    for offset in range(2, len(fields), 3):
        left, right, multiplicity = fields[offset : offset + 3]
        if left > right:
            left, right = right, left
        if left == right or multiplicity < 1:
            raise ValueError("the campaign accepts only loopless positive-multiplicity edges")
        edges.extend([(left, right)] * multiplicity)
    return EdgeGraph(n, tuple(edges), record.strip())


def graph_payload(graph: EdgeGraph) -> dict[str, object]:
    return {
        "vertex_count": graph.vertex_count,
        "edge_count": len(graph.edges),
        "edges": [list(edge) for edge in graph.edges],
        "degrees": list(graph.degrees),
        "source_encoding": graph.encoding,
    }


def _variables(
    object_count: int, color_count: int
) -> tuple[CNF, Callable[[int, int], int]]:
    cnf = CNF(object_count * color_count, [])

    def variable(item: int, color: int) -> int:
        return item * color_count + color + 1

    return cnf, variable


def _add_exactly_one(
    cnf: CNF,
    variable: Callable[[int, int], int],
    item: int,
    count: int,
) -> None:
    cnf.add(*(variable(item, color) for color in range(count)))
    for left in range(count):
        for right in range(left + 1, count):
            cnf.add(-variable(item, left), -variable(item, right))


def _incident_edges(graph: EdgeGraph) -> tuple[tuple[int, ...], ...]:
    incident: list[list[int]] = [[] for _ in range(graph.vertex_count)]
    for edge, (left, right) in enumerate(graph.edges):
        incident[left].append(edge)
        incident[right].append(edge)
    return tuple(tuple(row) for row in incident)


def _other_endpoint(graph: EdgeGraph, edge: int, vertex: int) -> int:
    left, right = graph.edges[edge]
    if left == vertex:
        return right
    if right == vertex:
        return left
    raise ValueError("edge is not incident with vertex")


def _canonical_path(edges: Sequence[int]) -> tuple[int, ...]:
    forward = tuple(edges)
    backward = tuple(reversed(edges))
    return min(forward, backward)


def _canonical_cycle(edges: Sequence[int]) -> tuple[int, ...]:
    values = tuple(edges)
    variants = []
    for oriented in (values, tuple(reversed(values))):
        variants.extend(oriented[index:] + oriented[:index] for index in range(len(values)))
    return min(variants)


def four_edge_paths_and_cycles(graph: EdgeGraph) -> tuple[tuple[int, ...], ...]:
    """Return edge-identity sequences for every simple P4 and C4."""

    incident = _incident_edges(graph)
    paths: set[tuple[int, ...]] = set()
    cycles: set[tuple[int, ...]] = set()

    def extend_path(
        vertex: int,
        vertices: tuple[int, ...],
        edge_path: tuple[int, ...],
        used_edges: frozenset[int],
    ) -> None:
        if len(edge_path) == 4:
            paths.add(_canonical_path(edge_path))
            return
        for edge in incident[vertex]:
            if edge in used_edges:
                continue
            other = _other_endpoint(graph, edge, vertex)
            if other in vertices:
                continue
            extend_path(
                other,
                vertices + (other,),
                edge_path + (edge,),
                used_edges | {edge},
            )

    def extend_cycle(
        start: int,
        vertex: int,
        vertices: tuple[int, ...],
        edge_path: tuple[int, ...],
        used_edges: frozenset[int],
    ) -> None:
        depth = len(edge_path)
        for edge in incident[vertex]:
            if edge in used_edges:
                continue
            other = _other_endpoint(graph, edge, vertex)
            if depth == 3:
                if other == start:
                    cycles.add(_canonical_cycle(edge_path + (edge,)))
                continue
            if other in vertices:
                continue
            extend_cycle(
                start,
                other,
                vertices + (other,),
                edge_path + (edge,),
                used_edges | {edge},
            )

    for start in range(graph.vertex_count):
        extend_path(start, (start,), (), frozenset())
        extend_cycle(start, start, (start,), (), frozenset())
    return tuple(sorted(paths | cycles))


def star_edge_coloring_cnf(graph: EdgeGraph, color_count: int = 6) -> CNF:
    cnf, variable = _variables(len(graph.edges), color_count)
    for edge in range(len(graph.edges)):
        _add_exactly_one(cnf, variable, edge, color_count)

    incident = _incident_edges(graph)
    for row in incident:
        for index, first in enumerate(row):
            for second in row[index + 1 :]:
                for color in range(color_count):
                    cnf.add(-variable(first, color), -variable(second, color))

    for sequence in four_edge_paths_and_cycles(graph):
        for first_color in range(color_count):
            for second_color in range(first_color + 1, color_count):
                cnf.add(
                    -variable(sequence[0], first_color),
                    -variable(sequence[1], second_color),
                    -variable(sequence[2], first_color),
                    -variable(sequence[3], second_color),
                )
                cnf.add(
                    -variable(sequence[0], second_color),
                    -variable(sequence[1], first_color),
                    -variable(sequence[2], second_color),
                    -variable(sequence[3], first_color),
                )
    if graph.edges:
        cnf.add(variable(0, 0))
    return cnf


def circular_coloring_cnf(graph: EdgeGraph, modulus: int = 20, distance: int = 7) -> CNF:
    if 2 * distance > modulus:
        raise ValueError("distance must not exceed half of the modulus")
    cnf, variable = _variables(graph.vertex_count, modulus)
    for vertex in range(graph.vertex_count):
        _add_exactly_one(cnf, variable, vertex, modulus)
    for left, right in graph.edges:
        for source, target in ((left, right), (right, left)):
            for color in range(modulus):
                supported = tuple(
                    variable(target, (color + offset) % modulus)
                    for offset in range(distance, modulus - distance + 1)
                )
                cnf.add(-variable(source, color), *supported)
    if graph.vertex_count:
        cnf.add(variable(0, 0))
    return cnf


def proper_edge_coloring_cnf(graph: EdgeGraph, color_count: int) -> CNF:
    cnf, variable = _variables(len(graph.edges), color_count)
    for edge in range(len(graph.edges)):
        _add_exactly_one(cnf, variable, edge, color_count)
    for row in _incident_edges(graph):
        for index, first in enumerate(row):
            for second in row[index + 1 :]:
                for color in range(color_count):
                    cnf.add(-variable(first, color), -variable(second, color))
    if graph.edges:
        cnf.add(variable(0, 0))
    return cnf


def decode_coloring(
    assignment: frozenset[int],
    object_count: int,
    color_count: int,
) -> tuple[int, ...]:
    colors = []
    for item in range(object_count):
        selected = [
            color
            for color in range(color_count)
            if item * color_count + color + 1 in assignment
        ]
        if len(selected) != 1:
            raise ValueError(f"solver model gives {len(selected)} colors to object {item}")
        colors.append(selected[0])
    return tuple(colors)


def verify_circular_coloring(
    graph: EdgeGraph,
    coloring: Sequence[int],
    modulus: int = 20,
    distance: int = 7,
) -> bool:
    if len(coloring) != graph.vertex_count:
        return False
    for left, right in graph.edges:
        difference = (coloring[left] - coloring[right]) % modulus
        if not distance <= difference <= modulus - distance:
            return False
    return True


def verify_proper_edge_coloring(graph: EdgeGraph, coloring: Sequence[int]) -> bool:
    if len(coloring) != len(graph.edges):
        return False
    return all(
        len({coloring[edge] for edge in row}) == len(row)
        for row in _incident_edges(graph)
    )


def bichromatic_cycle(
    graph: EdgeGraph,
    coloring: Sequence[int],
) -> tuple[int, ...] | None:
    if not verify_proper_edge_coloring(graph, coloring):
        raise ValueError("cycle oracle requires a proper edge coloring")
    colors = sorted(set(coloring))
    for first_index, first in enumerate(colors):
        for second in colors[first_index + 1 :]:
            selected = [
                edge for edge, color in enumerate(coloring) if color in {first, second}
            ]
            adjacency: list[list[tuple[int, int]]] = [
                [] for _ in range(graph.vertex_count)
            ]
            for edge in selected:
                left, right = graph.edges[edge]
                adjacency[left].append((right, edge))
                adjacency[right].append((left, edge))
            unseen = set(selected)
            while unseen:
                seed = next(iter(unseen))
                stack = [graph.edges[seed][0]]
                component_vertices: set[int] = set()
                component_edges: set[int] = set()
                while stack:
                    vertex = stack.pop()
                    if vertex in component_vertices:
                        continue
                    component_vertices.add(vertex)
                    for other, edge in adjacency[vertex]:
                        component_edges.add(edge)
                        unseen.discard(edge)
                        if other not in component_vertices:
                            stack.append(other)
                if (
                    component_edges
                    and all(len(adjacency[vertex]) == 2 for vertex in component_vertices)
                ):
                    return tuple(sorted(component_edges))
    return None


def verify_acyclic_edge_coloring(graph: EdgeGraph, coloring: Sequence[int]) -> bool:
    return verify_proper_edge_coloring(graph, coloring) and bichromatic_cycle(
        graph, coloring
    ) is None


def _parse_assignment(output: str) -> frozenset[int]:
    literals: set[int] = set()
    for line in output.splitlines():
        if not line.startswith("v "):
            continue
        for item in line[2:].split():
            literal = int(item)
            if literal > 0:
                literals.add(literal)
    return frozenset(literals)


@lru_cache(maxsize=None)
def locate_tool(name: str) -> Path:
    override = os.environ.get(f"AMRA_{name.upper().replace('-', '_')}")
    if override:
        path = Path(override)
        if path.is_file():
            return path
    cached = {
        "geng": Path(
            "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-geng"
        ),
        "multig": Path(
            "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-multig"
        ),
        "planarg": Path(
            "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-planarg"
        ),
        "cadical": Path("/home/biostar/.cache/amra/tools/sat/usr/bin/cadical"),
        "minisat": Path("/home/biostar/.cache/amra/tools/sat/usr/bin/minisat"),
        "drat-trim": Path(
            "/home/biostar/.cache/amra/tools/drat-trim-src/drat-trim"
        ),
    }.get(name)
    if cached and cached.is_file():
        return cached
    found = shutil.which(name)
    if found:
        return Path(found)
    raise FileNotFoundError(f"required tool is unavailable: {name}")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def implementation_fingerprint(*paths: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.resolve()).encode("utf-8"))
        digest.update(file_sha256(path).encode("ascii"))
    return digest.hexdigest()


def _shared_library_fingerprint(path: Path) -> dict[str, object]:
    process = subprocess.run(
        ["ldd", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=nauty_environment(),
    )
    dependencies: dict[str, dict[str, str]] = {}
    missing: list[str] = []
    for raw_line in process.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "=>" in line:
            soname, target = (part.strip() for part in line.split("=>", 1))
            candidate = target.split("(", 1)[0].strip()
            if candidate == "not found":
                missing.append(soname)
                continue
        else:
            candidate = line.split("(", 1)[0].strip()
            soname = Path(candidate).name
        dependency = Path(candidate)
        if dependency.is_absolute() and dependency.is_file():
            dependencies[soname] = {
                "path": str(dependency),
                "sha256": file_sha256(dependency),
            }
    return {
        "ldd_exit": process.returncode,
        "dependencies": dependencies,
        "missing": sorted(missing),
    }


def toolchain_fingerprint(names: Sequence[str]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for name in names:
        try:
            path = locate_tool(name)
        except FileNotFoundError:
            result[name] = {
                "path": "",
                "sha256": "unavailable",
                "dynamic_linkage": {},
            }
        else:
            result[name] = {
                "path": str(path),
                "sha256": file_sha256(path),
                "dynamic_linkage": _shared_library_fingerprint(path),
            }
    return result


def nauty_environment() -> dict[str, str]:
    environment = dict(os.environ)
    libraries = (
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib",
        "/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/lib/x86_64-linux-gnu",
        "/home/biostar/.cache/amra/tools/sat/usr/lib",
    )
    old = environment.get("LD_LIBRARY_PATH")
    environment["LD_LIBRARY_PATH"] = ":".join(libraries + ((old,) if old else ()))
    return environment


def solve_cnf(cnf: CNF, timeout_seconds: float) -> SolverResult:
    started = time.monotonic()
    try:
        solver = locate_tool("minisat")
    except FileNotFoundError:
        solver = None
    if solver is not None:
        ramdisk = Path("/dev/shm")
        temporary_parent = str(ramdisk) if ramdisk.is_dir() else None
        with tempfile.TemporaryDirectory(
            prefix="amra-opg-cnf-", dir=temporary_parent
        ) as raw_directory:
            directory = Path(raw_directory)
            formula = directory / "instance.cnf"
            model = directory / "model.txt"
            formula.write_text(cnf.dimacs(), encoding="ascii")
            environment = dict(os.environ)
            sat_library = "/home/biostar/.cache/amra/tools/sat/usr/lib"
            old = environment.get("LD_LIBRARY_PATH")
            environment["LD_LIBRARY_PATH"] = (
                sat_library + (f":{old}" if old else "")
            )
            command = [
                str(solver),
                f"-cpu-lim={max(1, int(timeout_seconds))}",
                str(formula),
                str(model),
            ]
            try:
                process = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=max(2.0, timeout_seconds + 2.0),
                    check=False,
                    env=environment,
                )
            except subprocess.TimeoutExpired as error:
                return SolverResult(
                    "timeout",
                    time.monotonic() - started,
                    frozenset(),
                    error.stdout or "",
                    error.stderr or "",
                )
            model_text = model.read_text(encoding="ascii") if model.exists() else ""
        status = "unknown"
        if process.returncode == 10 or model_text.startswith("SAT"):
            status = "sat"
        elif process.returncode == 20 or model_text.startswith("UNSAT"):
            status = "unsat"
        assigned: set[int] = set()
        for item in model_text.split():
            try:
                literal = int(item)
            except ValueError:
                continue
            if literal > 0:
                assigned.add(literal)
        assignment = frozenset(assigned)
        minisat_result = SolverResult(
            status,
            time.monotonic() - started,
            assignment,
            process.stdout,
            process.stderr,
        )
        if status != "unknown":
            return minisat_result
        fallback_seconds = timeout_seconds - minisat_result.elapsed_seconds
        if fallback_seconds <= 0:
            return SolverResult(
                "timeout",
                minisat_result.elapsed_seconds,
                frozenset(),
                minisat_result.stdout,
                minisat_result.stderr,
            )
        cadical_result = solve_cnf_cadical(cnf, fallback_seconds)
        return SolverResult(
            cadical_result.status,
            minisat_result.elapsed_seconds + cadical_result.elapsed_seconds,
            cadical_result.assignment,
            minisat_result.stdout + "\n" + cadical_result.stdout,
            minisat_result.stderr + "\n" + cadical_result.stderr,
        )
    return solve_cnf_cadical(cnf, timeout_seconds)


def solve_cnf_cadical(cnf: CNF, timeout_seconds: float) -> SolverResult:
    started = time.monotonic()
    if timeout_seconds <= 0:
        return SolverResult("timeout", 0.0, frozenset(), "", "")
    solver = locate_tool("cadical")
    command = [str(solver), "-q", "-t", str(max(1, int(timeout_seconds)))]
    try:
        process = subprocess.run(
            command,
            input=cnf.dimacs(),
            capture_output=True,
            text=True,
            timeout=max(2.0, timeout_seconds + 2.0),
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return SolverResult(
            "timeout",
            time.monotonic() - started,
            frozenset(),
            error.stdout or "",
            error.stderr or "",
        )
    status = "unknown"
    combined = process.stdout + "\n" + process.stderr
    if process.returncode == 10 or "s SATISFIABLE" in combined:
        status = "sat"
    elif process.returncode == 20 or "s UNSATISFIABLE" in combined:
        status = "unsat"
    return SolverResult(
        status,
        time.monotonic() - started,
        _parse_assignment(process.stdout),
        process.stdout,
        process.stderr,
    )


def solve_acyclic_edge_coloring(
    graph: EdgeGraph,
    color_count: int,
    timeout_seconds: float,
) -> tuple[
    SolverResult,
    CNF,
    tuple[int, ...] | None,
    int,
    tuple[dict[str, object], ...],
]:
    cnf = proper_edge_coloring_cnf(graph, color_count)
    deadline = time.monotonic() + timeout_seconds
    cut_count = 0
    cut_records: list[dict[str, object]] = []
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return (
                SolverResult("timeout", timeout_seconds, frozenset(), "", ""),
                cnf,
                None,
                cut_count,
                tuple(cut_records),
            )
        result = solve_cnf(cnf, remaining)
        if result.status != "sat":
            return result, cnf, None, cut_count, tuple(cut_records)
        coloring = decode_coloring(result.assignment, len(graph.edges), color_count)
        cycle = bichromatic_cycle(graph, coloring)
        if cycle is None:
            return result, cnf, coloring, cut_count, tuple(cut_records)
        clause = tuple(
            -(edge * color_count + coloring[edge] + 1) for edge in cycle
        )
        cnf.add(*clause)
        cut_records.append(
            {
                "edge_colors": [
                    [edge, coloring[edge]] for edge in cycle
                ],
                "clause": list(clause),
            }
        )
        cut_count += 1


def verify_acyclic_cut_records(
    graph: EdgeGraph,
    color_count: int,
    records: Sequence[dict[str, object]],
) -> bool:
    for record in records:
        if not isinstance(record, dict):
            return False
        raw_edge_colors = record.get("edge_colors")
        raw_clause = record.get("clause")
        if not isinstance(raw_edge_colors, list) or not isinstance(raw_clause, list):
            return False
        try:
            edge_colors = {
                int(edge): int(color) for edge, color in raw_edge_colors
            }
            clause = tuple(int(literal) for literal in raw_clause)
        except (TypeError, ValueError):
            return False
        if len(edge_colors) != len(raw_edge_colors) or len(edge_colors) < 3:
            return False
        if any(
            not 0 <= edge < len(graph.edges) or not 0 <= color < color_count
            for edge, color in edge_colors.items()
        ):
            return False
        expected = tuple(
            -(edge * color_count + edge_colors[edge] + 1)
            for edge in sorted(edge_colors)
        )
        if clause != expected or len(set(edge_colors.values())) != 2:
            return False
        adjacency: dict[int, list[int]] = {}
        for edge in edge_colors:
            left, right = graph.edges[edge]
            adjacency.setdefault(left, []).append(edge)
            adjacency.setdefault(right, []).append(edge)
        if not adjacency or any(len(row) != 2 for row in adjacency.values()):
            return False
        start = next(iter(adjacency))
        seen_vertices = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            row = adjacency[vertex]
            if edge_colors[row[0]] == edge_colors[row[1]]:
                return False
            for edge in row:
                left, right = graph.edges[edge]
                other = right if left == vertex else left
                if other not in seen_vertices:
                    seen_vertices.add(other)
                    stack.append(other)
        if len(seen_vertices) != len(adjacency):
            return False
    return True


def is_three_sparse(graph: EdgeGraph) -> bool:
    degrees = graph.degrees
    return all(min(degrees[left], degrees[right]) <= 3 for left, right in graph.edges)


def _pipeline(
    commands: Sequence[Sequence[str]],
) -> Iterator[str]:
    environment = nauty_environment()
    processes: list[subprocess.Popen[str]] = []
    previous_stdout = None
    try:
        for index, command in enumerate(commands):
            process = subprocess.Popen(
                list(command),
                stdin=previous_stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1,
                env=environment,
            )
            if previous_stdout is not None:
                previous_stdout.close()
            if process.stdout is None:
                raise RuntimeError("failed to open generator output")
            previous_stdout = process.stdout
            processes.append(process)
        assert previous_stdout is not None
        for line in previous_stdout:
            if line.strip() and not line.startswith(">"):
                yield line.rstrip("\n")
        for process in reversed(processes):
            return_code = process.wait()
            if return_code:
                raise RuntimeError(
                    f"generator exited with {return_code}: {' '.join(process.args)}"
                )
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()


def iter_star_multigraphs(
    order: int, lane: str = "cubic"
) -> Iterator[EdgeGraph]:
    geng = str(locate_tool("geng"))
    multig = str(locate_tool("multig"))
    if lane == "cubic":
        minimum = "1" if order == 2 else "2"
        commands = (
            (geng, "-cq", f"-d{minimum}", "-D3", str(order)),
            (multig, "-q", "-r3", "-m3", "-T"),
        )
    elif lane == "all-subcubic":
        commands = (
            (geng, "-cq", "-D3", str(order)),
            (multig, "-q", "-D3", "-m3", "-T"),
        )
    else:
        raise ValueError(f"unknown OPG-37271 lane: {lane}")
    yield from (decode_multig_text(line) for line in _pipeline(commands))


def iter_acyclic_graphs(order: int, shard: tuple[int, int] | None = None) -> Iterator[EdgeGraph]:
    geng = str(locate_tool("geng"))
    command = [geng, "-q", "-C", "-d2", "-D5", str(order)]
    if shard:
        command.append(f"{shard[0]}/{shard[1]}")
    for line in _pipeline((command,)):
        yield decode_graph6(line)


def iter_circular_graphs(order: int, shard: tuple[int, int] | None = None) -> Iterator[EdgeGraph]:
    geng = str(locate_tool("geng"))
    planarg = str(locate_tool("planarg"))
    command = [geng, "-q", "-Ctd2D3", str(order)]
    if shard:
        command.append(f"{shard[0]}/{shard[1]}")
    commands = (command, (planarg, "-q"))
    for line in _pipeline(commands):
        yield decode_graph6(line)


def _is_bipartite(graph: EdgeGraph) -> bool:
    adjacency = [[] for _ in range(graph.vertex_count)]
    for left, right in graph.edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    colors = [-1] * graph.vertex_count
    for start in range(graph.vertex_count):
        if colors[start] >= 0:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if colors[other] < 0:
                    colors[other] = 1 - colors[vertex]
                    stack.append(other)
                elif colors[other] == colors[vertex]:
                    return False
    return True


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _save_unsat_bundle(
    directory: Path,
    problem: str,
    graph: EdgeGraph,
    cnf: CNF,
    result: SolverResult,
    semantic_certificate: dict[str, object] | None = None,
) -> dict[str, object]:
    digest = hashlib.sha256(cnf.dimacs().encode("ascii")).hexdigest()
    bundle = directory / f"{problem}-{int(time.time())}-{digest[:12]}"
    bundle.mkdir(parents=True, exist_ok=False)
    formula = bundle / "formula.cnf"
    proof = bundle / "proof.drat"
    formula.write_text(cnf.dimacs(), encoding="ascii")
    cadical = locate_tool("cadical")
    drat_trim = locate_tool("drat-trim")
    command = [
        str(cadical),
        "-q",
        "--no-binary",
        "--checkproof=true",
        str(formula),
        str(proof),
    ]
    confirmation = subprocess.run(command, capture_output=True, text=True, check=False)
    checker_command = [str(drat_trim), str(formula), str(proof)]
    checker = subprocess.run(
        checker_command,
        capture_output=True,
        text=True,
        check=False,
    )
    independently_verified = (
        checker.returncode == 0 and "VERIFIED" in checker.stdout
    )
    semantic_replay_verified = (
        semantic_certificate is None
        or (
            semantic_certificate.get("independently_replayed") is True
            and semantic_certificate.get("actual_cnf_sha256") == digest
        )
    )
    payload = {
        "problem": problem,
        "graph": graph_payload(graph),
        "cnf_sha256": digest,
        "proof_sha256": file_sha256(proof) if proof.is_file() else None,
        "implementation_sha256": implementation_fingerprint(Path(__file__)),
        "toolchain": toolchain_fingerprint(("cadical", "drat-trim")),
        "cadical_command": command,
        "independent_checker_command": checker_command,
        "screening_elapsed_seconds": result.elapsed_seconds,
        "cadical_confirmation_exit": confirmation.returncode,
        "cadical_confirmation_stdout": confirmation.stdout,
        "cadical_confirmation_stderr": confirmation.stderr,
        "independent_checker_exit": checker.returncode,
        "independent_checker_stdout": checker.stdout,
        "independent_checker_stderr": checker.stderr,
        "proof_checker_status": (
            "independently_verified"
            if independently_verified
            else "independent_verification_failed"
        ),
        "semantic_certificate": semantic_certificate,
        "claim_verification_status": (
            (
                "proof_verified_pending_independent_encoding"
                if semantic_certificate is None
                else "proof_and_lazy_cut_replay_verified_pending_independent_encoding"
            )
            if independently_verified
            and semantic_replay_verified
            else "verification_incomplete"
        ),
    }
    _atomic_json(bundle / "manifest.json", payload)
    return {"bundle": str(bundle), **payload}


def evaluate_coloring_instance(
    problem: str,
    graph: EdgeGraph,
    timeout_seconds: float,
) -> tuple[
    SolverResult,
    CNF,
    tuple[int, ...] | None,
    int,
    tuple[dict[str, object], ...],
]:
    if problem == "opg37271":
        cnf = star_edge_coloring_cnf(graph, 6)
        result = solve_cnf(cnf, timeout_seconds)
        coloring = (
            decode_coloring(result.assignment, len(graph.edges), 6)
            if result.status == "sat"
            else None
        )
        if coloring is not None and not _verify_star_coloring(graph, coloring):
            raise RuntimeError("SAT solver returned an invalid star edge coloring")
        return result, cnf, coloring, 0, ()
    if problem == "opg401":
        cnf = circular_coloring_cnf(graph, 20, 7)
        result = solve_cnf(cnf, timeout_seconds)
        coloring = (
            decode_coloring(result.assignment, graph.vertex_count, 20)
            if result.status == "sat"
            else None
        )
        if coloring is not None and not verify_circular_coloring(graph, coloring):
            raise RuntimeError("SAT solver returned an invalid circular coloring")
        return result, cnf, coloring, 0, ()
    if problem == "opg145":
        result, cnf, coloring, cuts, cut_records = solve_acyclic_edge_coloring(
            graph, 7, timeout_seconds
        )
        if coloring is not None and not verify_acyclic_edge_coloring(graph, coloring):
            raise RuntimeError("SAT solver returned an invalid acyclic edge coloring")
        return result, cnf, coloring, cuts, cut_records
    raise ValueError(f"unsupported coloring problem: {problem}")


def _semantic_certificate(
    problem: str,
    graph: EdgeGraph,
    cnf: CNF,
    cut_records: tuple[dict[str, object], ...],
) -> dict[str, object] | None:
    if problem != "opg145":
        return None
    records_valid = verify_acyclic_cut_records(graph, 7, cut_records)
    replayed = proper_edge_coloring_cnf(graph, 7)
    if records_valid:
        for record in cut_records:
            replayed.add(*(int(literal) for literal in record["clause"]))
    replayed_digest = hashlib.sha256(
        replayed.dimacs().encode("ascii")
    ).hexdigest()
    actual_digest = hashlib.sha256(cnf.dimacs().encode("ascii")).hexdigest()
    formula_matches = (
        records_valid
        and replayed.variable_count == cnf.variable_count
        and replayed.clauses == cnf.clauses
        and replayed_digest == actual_digest
    )
    return {
        "kind": "acyclic_edge_coloring_lazy_cycle_cuts",
        "records": list(cut_records),
        "records_semantically_valid": records_valid,
        "replayed_cnf_sha256": replayed_digest,
        "actual_cnf_sha256": actual_digest,
        "independently_replayed": formula_matches,
    }


def _decode_hard_graph(problem: str, encoding: str) -> EdgeGraph:
    return (
        decode_multig_text(encoding)
        if problem == "opg37271"
        else decode_graph6(encoding)
    )


def run_search(
    problem: str,
    minimum_order: int,
    maximum_order: int,
    wall_seconds: float,
    per_instance_seconds: float,
    output: Path,
    max_cases: int = 0,
    shard: tuple[int, int] | None = None,
    lane: str = "default",
) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    state_path = output / "state.json"
    events_path = output / "events.jsonl"
    tool_names = ["minisat", "cadical", "drat-trim", "geng"]
    if problem == "opg37271":
        tool_names.append("multig")
    elif problem == "opg401":
        tool_names.append("planarg")
    fingerprint = implementation_fingerprint(Path(__file__))
    tools = toolchain_fingerprint(tool_names)
    state: dict[str, object] = {
        "checkpoint_schema": COLORING_CHECKPOINT_SCHEMA,
        "implementation_sha256": fingerprint,
        "toolchain": tools,
        "problem": problem,
        "minimum_order": minimum_order,
        "maximum_order": maximum_order,
        "shard": list(shard) if shard else None,
        "lane": lane,
        "next_order": minimum_order,
        "next_index": 0,
        "generated": 0,
        "eligible": 0,
        "filtered_known_positive": 0,
        "sat": 0,
        "unsat": 0,
        "timeouts": 0,
        "hard_queue": [],
        "status": "running",
    }
    if state_path.exists():
        loaded = json.loads(state_path.read_text(encoding="utf-8"))
        if loaded.get("checkpoint_schema") != COLORING_CHECKPOINT_SCHEMA:
            raise ValueError("legacy checkpoint requires a new output directory")
        identity = (
            loaded.get("problem"),
            loaded.get("shard"),
            loaded.get("lane", "default"),
            loaded.get("implementation_sha256"),
            loaded.get("toolchain"),
        )
        expected = (
            problem,
            list(shard) if shard else None,
            lane,
            fingerprint,
            tools,
        )
        if identity != expected:
            raise ValueError(f"checkpoint identity {identity} does not match {expected}")
        if int(loaded["minimum_order"]) != minimum_order:
            raise ValueError("minimum_order cannot change when resuming a checkpoint")
        if maximum_order < int(loaded["maximum_order"]):
            raise ValueError("maximum_order cannot shrink when resuming a checkpoint")
        state.update(loaded)
        state["maximum_order"] = maximum_order
        state.setdefault("filtered_known_positive", 0)
        if state.get("candidate") is not None or int(state.get("unsat", 0)) > 0:
            state["status"] = "candidate_pending_independent_verification"
            _atomic_json(state_path, state)
            return state
        state["status"] = "running"
    elif events_path.exists() and events_path.stat().st_size:
        raise ValueError(
            "events exist without a checkpoint; use a fresh output directory"
        )

    started = time.monotonic()
    deadline = started + wall_seconds
    total_this_run = 0
    pending_hard = list(state["hard_queue"])
    state["hard_queue"] = []
    for hard_position, hard in enumerate(pending_hard):
        if time.monotonic() >= deadline or (
            max_cases and total_this_run >= max_cases
        ):
            state["hard_queue"] = pending_hard[hard_position:] + list(
                state["hard_queue"]
            )
            state["status"] = "paused_budget"
            _atomic_json(state_path, state)
            return state
        graph = _decode_hard_graph(problem, str(hard["encoding"]))
        budget = min(
            per_instance_seconds,
            max(0.01, deadline - time.monotonic()),
        )
        result, cnf, coloring, cuts, cut_records = evaluate_coloring_instance(
            problem, graph, budget
        )
        total_this_run += 1
        retry_event = {
            "time": time.time(),
            "problem": problem,
            "order": int(hard["order"]),
            "index": int(hard["index"]),
            "encoding": graph.encoding,
            "vertices": graph.vertex_count,
            "edges": len(graph.edges),
            "status": result.status,
            "elapsed_seconds": result.elapsed_seconds,
            "variables": cnf.variable_count,
            "clauses": len(cnf.clauses),
            "lazy_cycle_cuts": cuts,
            "verified_coloring": list(coloring) if coloring is not None else None,
            "retry": True,
        }
        _append_jsonl(events_path, retry_event)
        if result.status == "sat":
            state["sat"] = int(state["sat"]) + 1
            state["timeouts"] = max(0, int(state["timeouts"]) - 1)
        elif result.status == "unsat":
            state["unsat"] = int(state["unsat"]) + 1
            state["timeouts"] = max(0, int(state["timeouts"]) - 1)
            candidate = _save_unsat_bundle(
                output / "candidates",
                problem,
                graph,
                cnf,
                result,
                _semantic_certificate(problem, graph, cnf, cut_records),
            )
            state["candidate"] = candidate
            state["status"] = "candidate_pending_independent_verification"
            state["hard_queue"] = pending_hard[hard_position + 1 :] + list(
                state["hard_queue"]
            )
            _atomic_json(state_path, state)
            return state
        else:
            queue = list(state["hard_queue"])
            queue.append(hard)
            state["hard_queue"] = queue
        _atomic_json(state_path, state)

    if time.monotonic() >= deadline or (
        max_cases and total_this_run >= max_cases
    ):
        state["status"] = "paused_budget"
        _atomic_json(state_path, state)
        return state

    for order in range(int(state["next_order"]), maximum_order + 1):
        resume_index = int(state["next_index"]) if order == int(state["next_order"]) else 0
        if problem == "opg37271":
            graphs = iter_star_multigraphs(
                order, "cubic" if lane == "default" else lane
            )
        elif problem == "opg145":
            graphs = iter_acyclic_graphs(order, shard)
        elif problem == "opg401":
            graphs = iter_circular_graphs(order, shard)
        else:
            raise ValueError(f"unsupported coloring problem: {problem}")

        for index, graph in enumerate(graphs):
            if index < resume_index:
                if time.monotonic() >= deadline or (
                    max_cases and total_this_run >= max_cases
                ):
                    state["status"] = "paused_budget"
                    _atomic_json(state_path, state)
                    return state
                continue
            if time.monotonic() >= deadline or (
                max_cases and total_this_run >= max_cases
            ):
                state["status"] = "paused_budget"
                _atomic_json(state_path, state)
                return state
            state["generated"] = int(state["generated"]) + 1
            total_this_run += 1
            eligible = True
            if problem == "opg145":
                eligible = (
                    max(graph.degrees, default=0) == 5
                    and not is_three_sparse(graph)
                )
            elif problem == "opg401":
                eligible = (
                    max(graph.degrees, default=0) >= 3
                    and not _is_bipartite(graph)
                )
            if not eligible:
                state["filtered_known_positive"] = (
                    int(state["filtered_known_positive"]) + 1
                )
                state["next_order"] = order
                state["next_index"] = index + 1
                if total_this_run % 100 == 0:
                    _atomic_json(state_path, state)
                if (max_cases and total_this_run >= max_cases) or time.monotonic() >= deadline:
                    state["status"] = "paused_budget"
                    _atomic_json(state_path, state)
                    return state
                continue
            state["eligible"] = int(state["eligible"]) + 1
            instance_budget = min(
                per_instance_seconds,
                max(0.01, deadline - time.monotonic()),
            )
            result, cnf, coloring, cuts, cut_records = evaluate_coloring_instance(
                problem, graph, instance_budget
            )

            event = {
                "time": time.time(),
                "problem": problem,
                "order": order,
                "index": index,
                "encoding": graph.encoding,
                "vertices": graph.vertex_count,
                "edges": len(graph.edges),
                "status": result.status,
                "elapsed_seconds": result.elapsed_seconds,
                "variables": cnf.variable_count,
                "clauses": len(cnf.clauses),
                "lazy_cycle_cuts": cuts,
                "verified_coloring": list(coloring) if coloring is not None else None,
            }
            _append_jsonl(events_path, event)
            if result.status == "sat":
                state["sat"] = int(state["sat"]) + 1
            elif result.status == "unsat":
                state["unsat"] = int(state["unsat"]) + 1
                candidate = _save_unsat_bundle(
                    output / "candidates",
                    problem,
                    graph,
                    cnf,
                    result,
                    _semantic_certificate(problem, graph, cnf, cut_records),
                )
                state["candidate"] = candidate
                state["status"] = "candidate_pending_independent_verification"
                state["next_order"] = order
                state["next_index"] = index + 1
                _atomic_json(state_path, state)
                return state
            else:
                state["timeouts"] = int(state["timeouts"]) + 1
                hard = {
                    "order": order,
                    "index": index,
                    "encoding": graph.encoding,
                    "status": result.status,
                }
                hard_queue = list(state["hard_queue"])
                hard_queue.append(hard)
                state["hard_queue"] = hard_queue

            state["next_order"] = order
            state["next_index"] = index + 1
            if total_this_run % 100 == 0:
                _atomic_json(state_path, state)
            if (max_cases and total_this_run >= max_cases) or time.monotonic() >= deadline:
                state["status"] = "paused_budget"
                _atomic_json(state_path, state)
                return state
        state["next_order"] = order + 1
        state["next_index"] = 0
        _atomic_json(state_path, state)

    state["status"] = (
        "complete_with_hard_queue" if state["hard_queue"] else "complete"
    )
    state["elapsed_seconds_last_run"] = time.monotonic() - started
    _atomic_json(state_path, state)
    return state


def _verify_star_coloring(graph: EdgeGraph, coloring: Sequence[int]) -> bool:
    if not verify_proper_edge_coloring(graph, coloring):
        return False
    return all(len({coloring[edge] for edge in sequence}) >= 3 for sequence in four_edge_paths_and_cycles(graph))


def parse_shard(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    left, right = (int(item) for item in value.split("/", 1))
    if right <= 0 or not 0 <= left < right:
        raise argparse.ArgumentTypeError("shard must have form index/count with 0<=index<count")
    return left, right


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Resumable exact first-stage searches for OPG-37271, OPG-145, and OPG-401."
    )
    parser.add_argument("problem", choices=("opg37271", "opg145", "opg401"))
    parser.add_argument("--min-order", type=int, required=True)
    parser.add_argument("--max-order", type=int, required=True)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--per-instance-seconds", type=float, default=30.0)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--shard", type=parse_shard)
    parser.add_argument(
        "--lane",
        choices=("default", "cubic", "all-subcubic"),
        default="default",
        help="OPG-37271 generator lane; ignored by the other problems.",
    )
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    result = run_search(
        arguments.problem,
        arguments.min_order,
        arguments.max_order,
        arguments.wall_seconds,
        arguments.per_instance_seconds,
        arguments.output,
        arguments.max_cases,
        arguments.shard,
        arguments.lane,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
