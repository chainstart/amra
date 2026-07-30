#!/usr/bin/env python3
"""Graded SAT probe for the Q-dimension-two branch of (2,2,2,2,1,1,1).

The query deliberately omits filtered higher associativity, the A2-to-J6
cube bijection, full raw-cube closure, and a noncommuting-cube witness.
SAT therefore proves only that the cheap leading identities do not by
themselves give a contradiction.
"""

from __future__ import annotations

import argparse
import itertools
import shutil
import subprocess

import cegis_dim9_profile_2111121 as engine


PROFILE = (2, 2, 2, 2, 1, 1, 1)


def build_query() -> tuple[list[str], dict[str, int]]:
    engine.PROFILE = PROFILE
    engine.RELEVANT_MAX_DEGREE = 5
    model, full_lines, ledger = engine.build_core()
    base_end = 3 + 2 * ledger["structure_variables"]
    associativity_end = base_end + ledger["associativity"]
    surjectivity_end = associativity_end + ledger["surjectivity"]
    associativity = full_lines[base_end:associativity_end]

    metadata: list[tuple[int, int]] = []
    for _, left_degree in model.basis:
        for _, middle_degree in model.basis:
            for _, right_degree in model.basis:
                minimum = left_degree + middle_degree + right_degree
                if minimum > model.top_degree:
                    continue
                for output_degree in range(
                    minimum, model.top_degree + 1
                ):
                    for _ in model.by_degree[output_degree]:
                        metadata.append((minimum, output_degree))
    leading_associativity = [
        assertion
        for assertion, (minimum, output_degree) in zip(
            associativity, metadata
        )
        if minimum == output_degree
    ]
    lines = (
        full_lines[:base_end]
        + leading_associativity
        + full_lines[associativity_end:surjectivity_end]
    )

    constants = engine.FIELD_CONSTANTS

    def constant_vector(
        degree: int, coefficients: tuple[int, ...]
    ) -> dict[str, str]:
        vector = model.zero_vector()
        for name, coefficient in zip(
            model.by_degree[degree], coefficients
        ):
            vector[name] = constants[coefficient]
        return vector

    degree_one_cubes = [
        model.cube(constant_vector(1, coefficients))
        for coefficients in itertools.product(range(3), repeat=2)
    ]
    for first, second in itertools.combinations(degree_one_cubes, 2):
        differences = [
            engine.nonzero(
                engine.ff_add(
                    [
                        first[name],
                        engine.ff_multiply(
                            engine.TWO, second[name]
                        ),
                    ]
                )
            )
            for name in model.by_degree[3]
        ]
        lines.append(f"(assert (or {' '.join(differences)}))")

    derivative_constraints = 0
    for coefficients in itertools.product(range(3), repeat=2):
        value = constant_vector(1, coefficients)
        value_squared = model.product(value, value)
        for direction_name in model.by_degree[2]:
            direction = model.zero_vector()
            direction[direction_name] = engine.ONE
            terms = [
                model.product(value_squared, direction),
                model.product(
                    model.product(value, direction), value
                ),
                model.product(direction, value_squared),
            ]
            for output_name in model.by_degree[4]:
                coordinate = engine.ff_add(
                    [term[output_name] for term in terms]
                )
                lines.append(
                    f"(assert (= {coordinate} {engine.ZERO}))"
                )
                derivative_constraints += 1

    query_ledger = {
        "declared_structure_variables": ledger[
            "structure_variables"
        ],
        "leading_associativity": len(leading_associativity),
        "surjectivity": ledger["surjectivity"],
        "q_bijection": 36,
        "derivative_constraints": derivative_constraints,
    }
    return lines + ["(check-sat)"], query_ledger


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=30)
    arguments = parser.parse_args()
    solver = shutil.which("z3")
    if solver is None:
        print("ERROR|z3_not_found")
        return 2

    lines, ledger = build_query()
    try:
        completed = subprocess.run(
            [solver, "-in"],
            input="\n".join(lines) + "\n",
            check=False,
            capture_output=True,
            text=True,
            timeout=arguments.timeout,
        )
        status = completed.stdout.splitlines()[0].strip()
    except subprocess.TimeoutExpired:
        status = "timeout"
    print(
        "DIM11_Q2_GRADED_PROBE"
        "|profile=2,2,2,2,1,1,1"
        "|graded_only=true"
        "|full_filtered=false"
        "|raw_closure=false"
        f"|structure_variables_declared="
        f"{ledger['declared_structure_variables']}"
        f"|leading_associativity={ledger['leading_associativity']}"
        f"|surjectivity={ledger['surjectivity']}"
        f"|q_bijection={ledger['q_bijection']}"
        f"|derivative_constraints={ledger['derivative_constraints']}"
        f"|result={status}"
    )
    print("DONE")
    return 0 if status == "sat" else 1


if __name__ == "__main__":
    raise SystemExit(main())
