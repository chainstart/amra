from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from amra.discovery.opg_coloring_search import (
    EdgeGraph,
    _atomic_json,
    file_sha256,
)
from amra.discovery.opg611_orbit_cuts import (
    orbit_lift_packing_block_clause,
)
from amra.discovery.opg611_symmetry import (
    Permutation,
    UnitArcSymmetryPlan,
    add_pack_color_minimum_order_clauses,
    build_unit_arc_symmetry_plan,
    dreadnaut_automorphism_generators,
    is_missing_graph_automorphism,
    unit_arc_clauses,
    verify_unit_arc_symmetry_plan,
)
from amra.discovery.opg_directed_cycles_search import (
    IncrementalSolver,
    OrientationModel,
    _load_n16_catalogue,
    _save_unsat_proof,
    build_orientation_model,
    decode_orientation,
    directed_short_cycles,
    extract_cycle_packing,
    orientation_master_cnf,
    pack_four_cycles_cnf,
    packing_block_clause,
    solve_incremental_once,
    strong_connectivity_cut,
    verify_orientation,
    violated_four_cycle_dominator_constraints,
)


HARD_SEARCH_SCHEMA = "amra.opg611.n16.hard-search.v1"


@dataclass(frozen=True)
class NovelPackingBatch:
    clauses: tuple[tuple[int, ...], ...]
    examined: int
    exhausted: bool


def novel_short_cycle_packing_clauses(
    model: OrientationModel,
    arcs: Sequence[tuple[int, int]],
    known: set[tuple[int, ...]],
    *,
    limit: int = 1_024,
    scan_limit: int = 262_144,
    cycle_offset: int = 0,
    deadline: float | None = None,
) -> NovelPackingBatch:
    """Return a small globally novel batch of short four-cycle packings.

    The original search adds as many as 65,536 clauses after every master
    model.  This separator remembers clauses across models and stops after a
    solver-friendly batch.  ``known`` is updated only for returned clauses.
    """

    if limit < 1:
        raise ValueError("limit must be positive")
    if scan_limit < limit:
        raise ValueError("scan_limit must be at least limit")
    cycles = directed_short_cycles(model.vertex_count, arcs)
    if cycles:
        offset = cycle_offset % len(cycles)
        cycles = cycles[offset:] + cycles[:offset]
    masks = tuple(
        sum(1 << vertex for vertex in {item for arc in cycle for item in arc})
        for cycle in cycles
    )
    clauses: list[tuple[int, ...]] = []
    local_seen: set[tuple[int, ...]] = set()
    examined = 0
    stopped = False

    def extend(start: int, used: int, chosen: tuple[int, ...]) -> None:
        nonlocal examined, stopped
        if stopped:
            return
        if deadline is not None and time.monotonic() >= deadline:
            stopped = True
            return
        if len(chosen) == 4:
            examined += 1
            clause = tuple(
                sorted(
                    set(
                        packing_block_clause(
                            model,
                            tuple(cycles[index] for index in chosen),
                        )
                    )
                )
            )
            if clause not in known and clause not in local_seen:
                local_seen.add(clause)
                clauses.append(clause)
                if len(clauses) >= limit:
                    stopped = True
            if examined >= scan_limit:
                stopped = True
            return
        for index in range(start, len(cycles)):
            if masks[index] & used:
                continue
            extend(index + 1, used | masks[index], chosen + (index,))
            if stopped:
                return

    extend(0, 0, ())
    known.update(clauses)
    return NovelPackingBatch(
        tuple(clauses),
        examined,
        exhausted=not stopped,
    )


def _phase_totals() -> dict[str, float]:
    return {
        "setup_seconds": 0.0,
        "master_solve_seconds": 0.0,
        "four_cycle_seconds": 0.0,
        "residual_cut_seconds": 0.0,
        "short_packing_seconds": 0.0,
        "packing_oracle_seconds": 0.0,
        "proof_seconds": 0.0,
    }


def _hard_engine_identity() -> dict[str, object]:
    source_paths = (
        Path(__file__).resolve(),
        Path(
            str(
                importlib.import_module(
                    "amra.discovery.opg_coloring_search"
                ).__file__
            )
        ).resolve(),
        Path(
            str(
                importlib.import_module(
                    "amra.discovery.opg_directed_cycles_search"
                ).__file__
            )
        ).resolve(),
        Path(
            str(
                importlib.import_module(
                    "amra.discovery.opg_directed_cycles_residual_cuts"
                ).__file__
            )
        ).resolve(),
        Path(
            str(
                importlib.import_module(
                    "amra.discovery.opg611_symmetry"
                ).__file__
            )
        ).resolve(),
        Path(
            str(
                importlib.import_module(
                    "amra.discovery.opg611_orbit_cuts"
                ).__file__
            )
        ).resolve(),
    )
    return {
        "schema": HARD_SEARCH_SCHEMA,
        "sources": [
            {"path": str(source), "sha256": file_sha256(source)}
            for source in source_paths
        ],
    }


def search_missing_graph_hard(
    missing_graph: EdgeGraph,
    *,
    catalogue_index: int | None = None,
    timeout_seconds: float,
    max_cegar_iterations: int,
    initial_unit_literals: Sequence[int] = (),
    symmetry_plan: UnitArcSymmetryPlan | None = None,
    automorphism_generators: Sequence[Permutation] = (),
    short_batch_size: int = 1_024,
    short_seed_count: int = 4,
    short_scan_limit: int = 262_144,
    residual_batch_size: int = 2,
    residual_scan_limit: int = 10_000,
    proof_directory: Path | None = None,
    progress_path: Path | None = None,
) -> dict[str, object]:
    """Second-generation targeted search for an OPG-611 hard instance."""

    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("timeout_seconds must be positive")
    if (
        not isinstance(max_cegar_iterations, int)
        or isinstance(max_cegar_iterations, bool)
        or max_cegar_iterations <= 0
    ):
        raise ValueError("max_cegar_iterations must be positive")
    if (
        not isinstance(short_batch_size, int)
        or isinstance(short_batch_size, bool)
        or short_batch_size <= 0
    ):
        raise ValueError("short_batch_size must be positive")
    if (
        not isinstance(short_seed_count, int)
        or isinstance(short_seed_count, bool)
        or short_seed_count <= 0
    ):
        raise ValueError("short_seed_count must be positive")
    if (
        not isinstance(short_scan_limit, int)
        or isinstance(short_scan_limit, bool)
        or short_scan_limit <= 0
    ):
        raise ValueError("short_scan_limit must be positive")
    if (
        not isinstance(residual_batch_size, int)
        or isinstance(residual_batch_size, bool)
        or residual_batch_size < 0
    ):
        raise ValueError("residual_batch_size must be nonnegative")
    if (
        not isinstance(residual_scan_limit, int)
        or isinstance(residual_scan_limit, bool)
        or residual_scan_limit <= 0
    ):
        raise ValueError("residual_scan_limit must be positive")
    if (
        catalogue_index is not None
        and (
            not isinstance(catalogue_index, int)
            or isinstance(catalogue_index, bool)
            or catalogue_index < 0
        )
    ):
        raise ValueError("catalogue_index must be nonnegative")
    if (
        missing_graph.vertex_count != 16
        or len(missing_graph.edges) != 8
        or len(set(missing_graph.edges)) != 8
    ):
        raise ValueError(
            "hard runner requires a simple 16-vertex, eight-edge missing graph"
        )
    if max(missing_graph.degrees, default=0) > 7:
        raise ValueError(
            "hard runner requires max missing degree at most seven; "
            "the exceptional catalogue graph is handled by the core search"
        )
    if initial_unit_literals and symmetry_plan is None:
        raise ValueError(
            "initial orientation units require a verified symmetry plan"
        )
    started = time.monotonic()
    timings = _phase_totals()
    model = build_orientation_model(missing_graph)
    master = orientation_master_cnf(model)
    automorphism_generators = tuple(automorphism_generators)
    if any(
        not is_missing_graph_automorphism(missing_graph, generator)
        for generator in automorphism_generators
    ):
        raise ValueError("invalid automorphism generator")
    effective_seed_limit = (
        min(short_seed_count, short_batch_size)
        if automorphism_generators
        else short_batch_size
    )
    if short_scan_limit < effective_seed_limit:
        raise ValueError(
            "short_scan_limit must cover at least one requested seed batch"
        )
    if symmetry_plan is not None:
        if not verify_unit_arc_symmetry_plan(missing_graph, symmetry_plan):
            raise ValueError("invalid unit-arc symmetry plan")
        planned_literals = tuple(
            clause[0] for clause in unit_arc_clauses(model, symmetry_plan)
        )
        if initial_unit_literals and tuple(initial_unit_literals) != planned_literals:
            raise ValueError("explicit units disagree with the symmetry plan")
        initial_unit_literals = planned_literals
    for literal in initial_unit_literals:
        if not 0 < abs(literal) <= len(model.allowed_edges):
            raise ValueError(f"invalid initial orientation literal: {literal}")
        master.add(literal)
    timings["setup_seconds"] = time.monotonic() - started
    engine_identity = _hard_engine_identity()
    search_config = {
        "catalogue_index": catalogue_index,
        "timeout_seconds": float(timeout_seconds),
        "max_cegar_iterations": int(max_cegar_iterations),
        "short_batch_size": int(short_batch_size),
        "short_seed_count": int(short_seed_count),
        "short_scan_limit": int(short_scan_limit),
        "residual_batch_size": int(residual_batch_size),
        "residual_scan_limit": int(residual_scan_limit),
        "proofs": proof_directory is not None,
    }
    timings["setup_seconds"] = time.monotonic() - started
    strong_cuts = 0
    four_cycle_cuts = 0
    residual_cuts = 0
    packing_cuts = 0
    packing_batches = 0
    packing_clauses_examined = 0
    orbit_lifted_cuts = 0
    master_solves = 0
    master_models = 0
    known_four_cycles: set[tuple[tuple[int, int], ...]] = set()
    known_packing_clauses: set[tuple[int, ...]] = set()
    known_residual_packings: set[tuple[tuple[int, ...], ...]] = set()
    residual_cut_records: list[dict[str, object]] = []

    def payload(status: str) -> dict[str, object]:
        return {
            "schema": HARD_SEARCH_SCHEMA,
            "status": status,
            "config": search_config,
            "missing_graph6": missing_graph.encoding,
            "solver": os.environ.get("AMRA_PYSAT_SOLVER", "glucose42"),
            "master_variables": master.variable_count,
            "master_clauses": len(master.clauses),
            "symmetry_units": list(initial_unit_literals),
            "symmetry_plan": (
                symmetry_plan.as_dict() if symmetry_plan is not None else None
            ),
            "automorphism_generators": [
                list(generator) for generator in automorphism_generators
            ],
            "strong_connectivity_semantics": {
                "separator": "sink strongly-connected-component cut",
                "fixed_degree_outcut_identity": (
                    "a(S,V-S)=7|S|-binom(|S|,2)+e_H(S)"
                ),
                "automatic_for_this_graph": max(missing_graph.degrees) <= 7,
            },
            "strong_cuts": strong_cuts,
            "four_cycle_cuts": four_cycle_cuts,
            "residual_cuts": residual_cuts,
            "residual_cut_records": list(residual_cut_records),
            "packing_cuts": packing_cuts,
            "packing_batches": packing_batches,
            "packing_clauses_examined": packing_clauses_examined,
            "orbit_lifted_cuts": orbit_lifted_cuts,
            "master_solves": master_solves,
            "master_models": master_models,
            "elapsed_seconds": time.monotonic() - started,
            "wall_scope": (
                "search function from master construction through CEGAR; "
                "excludes CLI catalogue/automorphism setup and optional proof"
            ),
            "timings": dict(timings),
            "hard_engine": engine_identity,
        }

    def write_progress(phase: str) -> None:
        if progress_path is None:
            return
        snapshot = payload("running")
        snapshot["phase"] = phase
        snapshot["telemetry_only_not_resumable"] = True
        for key in (
            "automorphism_generators",
            "residual_cut_records",
            "symmetry_plan",
        ):
            snapshot.pop(key, None)
        _atomic_json(progress_path, snapshot)

    write_progress("ready")
    with IncrementalSolver(master) as master_solver:
        while (
            strong_cuts + four_cycle_cuts + residual_cuts + packing_cuts
            < max_cegar_iterations
        ):
            remaining = timeout_seconds - (time.monotonic() - started)
            if remaining <= 0:
                return payload("timeout")
            master_solves += 1
            write_progress("master_solve")
            phase_started = time.monotonic()
            result = master_solver.solve(remaining)
            timings["master_solve_seconds"] += time.monotonic() - phase_started
            if result.status == "unsat":
                answer = payload("excluded")
                if proof_directory is not None:
                    stem = (
                        f"hard-missing-{missing_graph.encoding.encode().hex()}-"
                        f"{time.time_ns()}"
                    )
                    answer["search_elapsed_seconds"] = answer["elapsed_seconds"]
                    phase_started = time.monotonic()
                    try:
                        manifest = _save_unsat_proof(
                            proof_directory,
                            stem,
                            master,
                            answer,
                        )
                    except Exception as error:
                        timings["proof_seconds"] += (
                            time.monotonic() - phase_started
                        )
                        answer["post_search_proof_seconds"] = timings[
                            "proof_seconds"
                        ]
                        answer["total_elapsed_seconds"] = (
                            time.monotonic() - started
                        )
                        answer["timings"] = dict(timings)
                        answer["status"] = (
                            "excluded_pending_proof_verification"
                        )
                        answer["proof_error"] = (
                            f"{type(error).__name__}: {error}"
                        )
                        return answer
                    timings["proof_seconds"] += time.monotonic() - phase_started
                    answer["post_search_proof_seconds"] = timings[
                        "proof_seconds"
                    ]
                    answer["total_elapsed_seconds"] = (
                        time.monotonic() - started
                    )
                    answer["timings"] = dict(timings)
                    manifest["hard_search_search_elapsed_seconds"] = answer[
                        "search_elapsed_seconds"
                    ]
                    manifest["hard_search_total_elapsed_seconds"] = answer[
                        "total_elapsed_seconds"
                    ]
                    manifest["hard_search_timings_after_proof"] = dict(timings)
                    _atomic_json(proof_directory / f"{stem}.json", manifest)
                    answer["proof"] = manifest
                    if manifest.get("proof_status") != "independently_verified":
                        answer["status"] = (
                            "excluded_pending_proof_verification"
                        )
                return answer
            if result.status != "sat":
                return payload(result.status)

            master_models += 1
            arcs = decode_orientation(model, result.assignment)
            if not verify_orientation(model, arcs):
                raise RuntimeError("invalid orientation returned by SAT solver")

            connectivity = strong_connectivity_cut(model, arcs)
            if connectivity is not None:
                raise RuntimeError(
                    "fixed-degree outcut identity predicted strong connectivity"
                )

            phase_started = time.monotonic()
            old_known_count = len(known_four_cycles)
            four_cycle_clauses = violated_four_cycle_dominator_constraints(
                master,
                model,
                arcs,
                known_four_cycles,
            )
            timings["four_cycle_seconds"] += time.monotonic() - phase_started
            if four_cycle_clauses:
                for clause in four_cycle_clauses:
                    master_solver.add_clause(clause)
                four_cycle_cuts += len(known_four_cycles) - old_known_count
            if time.monotonic() - started >= timeout_seconds:
                return payload("timeout")

            # Imported lazily so this runner remains usable while the
            # independently tested mathematical separator evolves.
            phase_started = time.monotonic()
            from amra.discovery.opg_directed_cycles_residual_cuts import (
                separate_residual_degree_cuts,
            )

            before = len(master.clauses)
            triple_residual = separate_residual_degree_cuts(
                master,
                model,
                arcs,
                known_residual_packings,
                pack_sizes=(3,),
                limit=residual_batch_size,
                consideration_limit=residual_scan_limit,
                traversal_limit=residual_scan_limit,
            )
            pair_residual = separate_residual_degree_cuts(
                master,
                model,
                arcs,
                known_residual_packings,
                pack_sizes=(2,),
                limit=residual_batch_size,
                consideration_limit=residual_scan_limit,
                traversal_limit=residual_scan_limit,
            )
            new_residual_clauses = master.clauses[before:]
            timings["residual_cut_seconds"] += time.monotonic() - phase_started
            if new_residual_clauses:
                for clause in new_residual_clauses:
                    master_solver.add_clause(clause)
                added = triple_residual.cuts + pair_residual.cuts
                residual_cuts += len(added)
                residual_cut_records.extend(
                    {
                        "packing_key": [list(cycle) for cycle in cut.packing_key],
                        "packing_size": cut.packing_size,
                        "selected_vertices": list(cut.selected_vertices),
                        "threshold": cut.threshold,
                        "trigger_literals": list(cut.trigger_literals),
                        "first_auxiliary_variable": cut.first_auxiliary_variable,
                        "last_auxiliary_variable": cut.last_auxiliary_variable,
                        "clause_count": len(cut.clauses),
                    }
                    for cut in added
                )
            if time.monotonic() - started >= timeout_seconds:
                return payload("timeout")

            phase_started = time.monotonic()
            batch = novel_short_cycle_packing_clauses(
                model,
                arcs,
                known_packing_clauses,
                limit=effective_seed_limit,
                scan_limit=short_scan_limit,
                cycle_offset=packing_batches * 17,
                deadline=started + timeout_seconds,
            )
            packing_clauses = list(batch.clauses)
            for seed in batch.clauses if automorphism_generators else ():
                remaining_orbit_budget = (
                    short_batch_size - len(packing_clauses)
                )
                if remaining_orbit_budget <= 0:
                    break
                lifted = orbit_lift_packing_block_clause(
                    model,
                    seed,
                    automorphism_generators,
                    known_packing_clauses,
                    limit=remaining_orbit_budget,
                    deadline=started + timeout_seconds,
                )
                packing_clauses.extend(lifted)
                orbit_lifted_cuts += len(lifted)
            timings["short_packing_seconds"] += time.monotonic() - phase_started
            packing_clauses_examined += batch.examined
            if packing_clauses:
                for clause in packing_clauses:
                    master.add(*clause)
                    master_solver.add_clause(clause)
                packing_cuts += len(packing_clauses)
                packing_batches += 1
                if time.monotonic() - started >= timeout_seconds:
                    return payload("timeout")
                write_progress("cuts_added")
                continue
            if time.monotonic() - started >= timeout_seconds:
                return payload("timeout")

            phase_started = time.monotonic()
            packing = pack_four_cycles_cnf(model.vertex_count, arcs)
            add_pack_color_minimum_order_clauses(
                packing.cnf, model.vertex_count
            )
            packing_remaining = timeout_seconds - (time.monotonic() - started)
            if packing_remaining <= 0:
                return payload("timeout")
            pack_result = solve_incremental_once(packing.cnf, packing_remaining)
            timings["packing_oracle_seconds"] += time.monotonic() - phase_started
            if pack_result.status == "unsat":
                if four_cycle_clauses or new_residual_clauses:
                    raise RuntimeError(
                        "necessary-condition separator disagrees with PACK4"
                    )
                # Color ordering is an equisatisfiable PACK4 symmetry break,
                # but a claimed counterexample is independently replayed
                # against the original, unstrengthened packing oracle.
                original_packing = pack_four_cycles_cnf(
                    model.vertex_count, arcs
                )
                verification_remaining = timeout_seconds - (
                    time.monotonic() - started
                )
                verification_status = "timeout"
                if verification_remaining > 0.01:
                    phase_started = time.monotonic()
                    verification_result = solve_incremental_once(
                        original_packing.cnf,
                        verification_remaining,
                    )
                    timings["packing_oracle_seconds"] += (
                        time.monotonic() - phase_started
                    )
                    verification_status = verification_result.status
                if verification_status == "sat":
                    raise RuntimeError(
                        "PACK4 color symmetry changed satisfiability"
                    )
                answer = payload("candidate")
                answer.update(
                    {
                        "arcs": [list(arc) for arc in arcs],
                        "outdegrees": [
                            sum(1 for source, _ in arcs if source == vertex)
                            for vertex in range(model.vertex_count)
                        ],
                        "packing_variables": packing.cnf.variable_count,
                        "packing_clauses": len(packing.cnf.clauses),
                        "independent_packing_status": verification_status,
                        "independent_packing_variables": (
                            original_packing.cnf.variable_count
                        ),
                        "independent_packing_clauses": len(
                            original_packing.cnf.clauses
                        ),
                    }
                )
                if verification_status != "unsat":
                    answer["status"] = (
                        "candidate_pending_independent_verification"
                    )
                    return answer
                if proof_directory is not None:
                    stem = (
                        "hard-candidate-"
                        f"{missing_graph.encoding.encode().hex()}-"
                        f"{time.time_ns()}"
                    )
                    answer["search_elapsed_seconds"] = answer["elapsed_seconds"]
                    phase_started = time.monotonic()
                    try:
                        manifest = _save_unsat_proof(
                            proof_directory,
                            stem,
                            original_packing.cnf,
                            answer,
                        )
                    except Exception as error:
                        timings["proof_seconds"] += (
                            time.monotonic() - phase_started
                        )
                        answer["post_search_proof_seconds"] = timings[
                            "proof_seconds"
                        ]
                        answer["total_elapsed_seconds"] = (
                            time.monotonic() - started
                        )
                        answer["timings"] = dict(timings)
                        answer["status"] = (
                            "candidate_pending_proof_verification"
                        )
                        answer["proof_error"] = (
                            f"{type(error).__name__}: {error}"
                        )
                        return answer
                    timings["proof_seconds"] += time.monotonic() - phase_started
                    answer["post_search_proof_seconds"] = timings[
                        "proof_seconds"
                    ]
                    answer["total_elapsed_seconds"] = (
                        time.monotonic() - started
                    )
                    answer["timings"] = dict(timings)
                    manifest["hard_search_search_elapsed_seconds"] = answer[
                        "search_elapsed_seconds"
                    ]
                    manifest["hard_search_total_elapsed_seconds"] = answer[
                        "total_elapsed_seconds"
                    ]
                    manifest["hard_search_timings_after_proof"] = dict(timings)
                    _atomic_json(proof_directory / f"{stem}.json", manifest)
                    answer["proof"] = manifest
                    if manifest.get("proof_status") != "independently_verified":
                        answer["status"] = (
                            "candidate_pending_proof_verification"
                        )
                return answer
            if pack_result.status != "sat":
                return payload(f"packing_{pack_result.status}")
            cycles = extract_cycle_packing(arcs, packing, pack_result.assignment)
            clause = tuple(sorted(set(packing_block_clause(model, cycles))))
            if clause in known_packing_clauses:
                raise RuntimeError(
                    "packing oracle returned a clause already active in the master"
                )
            lifted_clauses = orbit_lift_packing_block_clause(
                model,
                clause,
                automorphism_generators,
                known_packing_clauses,
                limit=short_batch_size,
                deadline=started + timeout_seconds,
            )
            if not lifted_clauses:
                if time.monotonic() - started >= timeout_seconds:
                    return payload("timeout")
                raise RuntimeError("packing orbit lift made no progress")
            for lifted_clause in lifted_clauses:
                master.add(*lifted_clause)
                master_solver.add_clause(lifted_clause)
            packing_cuts += len(lifted_clauses)
            orbit_lifted_cuts += max(0, len(lifted_clauses) - 1)
            write_progress("packing_oracle_cut_added")
    return payload("iteration_limit")


def _catalogue_graph(index: int) -> EdgeGraph:
    catalogue = _load_n16_catalogue()
    if not 0 <= index < len(catalogue):
        raise ValueError(f"catalogue index outside 0..{len(catalogue) - 1}")
    return catalogue[index]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Targeted second-generation OPG-611 hard-instance search."
    )
    parser.add_argument("--catalogue-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--max-cegar-iterations", type=int, default=1_000_000)
    parser.add_argument("--short-batch-size", type=int, default=1_024)
    parser.add_argument("--short-seed-count", type=int, default=4)
    parser.add_argument("--short-scan-limit", type=int, default=262_144)
    parser.add_argument("--residual-batch-size", type=int, default=2)
    parser.add_argument("--residual-scan-limit", type=int, default=10_000)
    parser.add_argument("--no-symmetry", action="store_true")
    parser.add_argument("--no-orbit-lift", action="store_true")
    parser.add_argument("--proofs", action="store_true")
    arguments = parser.parse_args(argv)
    graph = _catalogue_graph(arguments.catalogue_index)
    arguments.output.mkdir(parents=True, exist_ok=True)
    generators = (
        ()
        if arguments.no_symmetry and arguments.no_orbit_lift
        else dreadnaut_automorphism_generators(graph)
    )
    symmetry_plan = (
        None
        if arguments.no_symmetry
        else build_unit_arc_symmetry_plan(graph, generators)
    )
    result = search_missing_graph_hard(
        graph,
        catalogue_index=arguments.catalogue_index,
        timeout_seconds=arguments.wall_seconds,
        max_cegar_iterations=arguments.max_cegar_iterations,
        symmetry_plan=symmetry_plan,
        automorphism_generators=(
            () if arguments.no_orbit_lift else generators
        ),
        short_batch_size=arguments.short_batch_size,
        short_seed_count=arguments.short_seed_count,
        short_scan_limit=arguments.short_scan_limit,
        residual_batch_size=arguments.residual_batch_size,
        residual_scan_limit=arguments.residual_scan_limit,
        proof_directory=(arguments.output / "proofs") if arguments.proofs else None,
        progress_path=arguments.output / "progress.json",
    )
    _atomic_json(arguments.output / "result.json", result)
    console_result = {
        key: value
        for key, value in result.items()
        if key
        not in {
            "automorphism_generators",
            "residual_cut_records",
            "symmetry_plan",
        }
    }
    terminal_progress = dict(console_result)
    terminal_progress["phase"] = "terminal"
    terminal_progress["telemetry_only_not_resumable"] = True
    _atomic_json(arguments.output / "progress.json", terminal_progress)
    print(json.dumps(console_result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
