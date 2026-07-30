#!/usr/bin/env python3
"""Strict raw-cube CEGIS for profile (2,1,1,1,1,2,1).

Each SMT candidate is a complete filtered associative F_3-algebra with the
prescribed power-filtration profile and two noncommuting cubes.  A concrete
checker then enumerates all 3^6 cube-relevant inputs.  Every missing circle
product adds a symbolic cube-root constraint for that fixed input pair.

SAT is accepted only after the concrete raw cube set is fully closed.
UNSAT after accumulated necessary closure constraints excludes the profile.
"""

from __future__ import annotations

import argparse
import itertools
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from search_dim9_algebra_profiles import (
    ONE,
    TWO,
    ZERO,
    FilteredModel,
    declare_field_variable,
    ff_add,
    ff_multiply,
    nonzero,
)


PROFILE = (2, 1, 1, 1, 1, 2, 1)
RELEVANT_MAX_DEGREE = 5
FIELD_CONSTANTS = (ZERO, ONE, TWO)


def build_core() -> tuple[FilteredModel, list[str], dict[str, int]]:
    """Complete filtered algebra, associativity, and power-layer constraints."""

    model = FilteredModel(PROFILE)
    lines = [
        "(set-logic QF_BV)",
        "(define-fun fadd ((a (_ BitVec 2)) (b (_ BitVec 2)))"
        " (_ BitVec 2)"
        " (ite (= a #b00) b"
        " (ite (= b #b00) a"
        " (ite (= a b) (ite (= a #b01) #b10 #b01) #b00))))",
        "(define-fun fmul ((a (_ BitVec 2)) (b (_ BitVec 2)))"
        " (_ BitVec 2)"
        " (ite (or (= a #b00) (= b #b00)) #b00"
        " (ite (= a b) #b01 #b10)))",
    ]
    for variable in model.structure_variables:
        declare_field_variable(lines, variable)

    associativity_count = 0
    for left, left_degree in model.basis:
        for middle, middle_degree in model.basis:
            for right, right_degree in model.basis:
                minimum_degree = left_degree + middle_degree + right_degree
                if minimum_degree > model.top_degree:
                    continue
                for output_degree in range(
                    minimum_degree, model.top_degree + 1
                ):
                    for output_name in model.by_degree[output_degree]:
                        left_terms = []
                        for intermediate, first_constant in model.products[
                            (left, middle)
                        ].items():
                            second_constant = model.products.get(
                                (intermediate, right), {}
                            ).get(output_name)
                            if second_constant is not None:
                                left_terms.append(
                                    ff_multiply(
                                        first_constant, second_constant
                                    )
                                )
                        right_terms = []
                        for intermediate, first_constant in model.products[
                            (middle, right)
                        ].items():
                            second_constant = model.products.get(
                                (left, intermediate), {}
                            ).get(output_name)
                            if second_constant is not None:
                                right_terms.append(
                                    ff_multiply(
                                        first_constant, second_constant
                                    )
                                )
                        lines.append(
                            f"(assert (= {ff_add(left_terms)}"
                            f" {ff_add(right_terms)}))"
                        )
                        associativity_count += 1

    surjectivity_count = 0
    for target_degree in range(2, model.top_degree + 1):
        target_dimension = PROFILE[target_degree - 1]
        for left_degree in range(1, target_degree):
            right_degree = target_degree - left_degree
            columns = [
                [
                    model.products[(left, right)][target_name]
                    for target_name in model.by_degree[target_degree]
                ]
                for left in model.by_degree[left_degree]
                for right in model.by_degree[right_degree]
            ]
            if target_dimension == 1:
                condition = (
                    f"(or {' '.join(nonzero(column[0]) for column in columns)})"
                )
            elif target_dimension == 2:
                minors = []
                for first, second in itertools.combinations(columns, 2):
                    determinant = ff_add(
                        [
                            ff_multiply(first[0], second[1]),
                            ff_multiply(TWO, first[1], second[0]),
                        ]
                    )
                    minors.append(nonzero(determinant))
                condition = (
                    f"(or {' '.join(minors)})" if minors else "false"
                )
            else:
                raise ValueError("unexpected layer dimension")
            lines.append(f"(assert {condition})")
            surjectivity_count += 1

    relevant_names = [
        name
        for name, degree in model.basis
        if degree <= RELEVANT_MAX_DEGREE
    ]

    # Genuine Wilson obstruction in the exponent-nine range: two raw cubes
    # fail to commute.  The roots range over every cube-relevant coordinate.
    witness_vectors = []
    for side in ("left", "right"):
        vector = model.zero_vector()
        for name in relevant_names:
            variable = f"witness_{side}_{name}"
            declare_field_variable(lines, variable)
            vector[name] = variable
        witness_vectors.append(vector)
    left_cube = model.cube(witness_vectors[0])
    right_cube = model.cube(witness_vectors[1])
    left_right = model.product(left_cube, right_cube)
    right_left = model.product(right_cube, left_cube)
    commutator_coordinates = [
        nonzero(
            ff_add(
                [
                    left_right[name],
                    ff_multiply(TWO, right_left[name]),
                ]
            )
        )
        for name, _ in model.basis
    ]
    lines.append(f"(assert (or {' '.join(commutator_coordinates)}))")

    ledger = {
        "structure_variables": len(model.structure_variables),
        "associativity": associativity_count,
        "surjectivity": surjectivity_count,
        "relevant_dimension": len(relevant_names),
        "witness_variables": 2 * len(relevant_names),
    }
    return model, lines, ledger


def constant_vector(
    model: FilteredModel,
    relevant_names: list[str],
    coefficients: tuple[int, ...],
) -> dict[str, str]:
    vector = model.zero_vector()
    for name, coefficient in zip(relevant_names, coefficients):
        vector[name] = FIELD_CONSTANTS[coefficient]
    return vector


def add_closure_constraint(
    model: FilteredModel,
    lines: list[str],
    relevant_names: list[str],
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    iteration: int,
) -> None:
    """Require closure for one fixed pair of cube inputs."""

    left_cube = model.cube(
        constant_vector(model, relevant_names, left_source)
    )
    right_cube = model.cube(
        constant_vector(model, relevant_names, right_source)
    )
    product = model.product(left_cube, right_cube)
    target = {
        name: ff_add([left_cube[name], right_cube[name], product[name]])
        for name, _ in model.basis
    }
    root = model.zero_vector()
    for name in relevant_names:
        variable = f"closure_{iteration}_{name}"
        declare_field_variable(lines, variable)
        root[name] = variable
    root_cube = model.cube(root)
    for name, _ in model.basis:
        lines.append(f"(assert (= {root_cube[name]} {target[name]}))")


def solve_structure(
    model: FilteredModel,
    lines: list[str],
    solver: str,
    timeout_seconds: int,
    certificate: Path | None,
) -> tuple[str, dict[str, int], int]:
    query = lines + [
        "(check-sat)",
        f"(get-value ({' '.join(model.structure_variables)}))",
    ]
    formula = "\n".join(query) + "\n"
    if certificate is not None:
        certificate.write_text(formula, encoding="utf-8")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [solver, "-in"],
            input=formula,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return "timeout", {}, round((time.monotonic() - started) * 1000)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    first_line = completed.stdout.splitlines()[0].strip()
    if first_line != "sat":
        return first_line, {}, elapsed_ms
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + completed.stderr)
    assignments = {
        variable: int(bits, 2)
        for variable, bits in re.findall(
            r"\((m_[A-Za-z0-9_]+) #b([01]{2})\)",
            completed.stdout,
        )
    }
    if len(assignments) != len(model.structure_variables):
        raise RuntimeError(
            "incomplete model: "
            f"{len(assignments)} of {len(model.structure_variables)}"
        )
    return "sat", assignments, elapsed_ms


class ConcreteAlgebra:
    """Exact F_3 evaluator for one SMT multiplication table."""

    def __init__(
        self, model: FilteredModel, assignments: dict[str, int]
    ) -> None:
        self.model = model
        self.assignments = assignments
        self.names = [name for name, _ in model.basis]
        self.index = {name: index for index, name in enumerate(self.names)}
        self.product_terms: list[tuple[int, int, int, int]] = []
        for (left, right), outputs in model.products.items():
            for output, variable in outputs.items():
                coefficient = assignments[variable]
                if coefficient:
                    self.product_terms.append(
                        (
                            self.index[left],
                            self.index[right],
                            self.index[output],
                            coefficient,
                        )
                    )

    def multiply(
        self, left: tuple[int, ...], right: tuple[int, ...]
    ) -> tuple[int, ...]:
        output = [0] * len(self.names)
        for left_index, right_index, output_index, coefficient in (
            self.product_terms
        ):
            output[output_index] = (
                output[output_index]
                + coefficient * left[left_index] * right[right_index]
            ) % 3
        return tuple(output)

    def cube(self, value: tuple[int, ...]) -> tuple[int, ...]:
        return self.multiply(self.multiply(value, value), value)

    def circle(
        self, left: tuple[int, ...], right: tuple[int, ...]
    ) -> tuple[int, ...]:
        product = self.multiply(left, right)
        return tuple(
            (left[index] + right[index] + product[index]) % 3
            for index in range(len(self.names))
        )


def decode_source(
    code: int, relevant_dimension: int, algebra_dimension: int
) -> tuple[int, ...]:
    output = [0] * algebra_dimension
    for index in range(relevant_dimension):
        output[index] = code % 3
        code //= 3
    return tuple(output)


def check_raw_closure(
    algebra: ConcreteAlgebra, relevant_dimension: int
) -> tuple[
    int,
    bool,
    tuple[int, tuple[int, ...], tuple[int, ...]] | None,
]:
    """Enumerate all raw cubes and return the first missing circle product."""

    preimage: dict[tuple[int, ...], tuple[int, tuple[int, ...]]] = {}
    for code in range(3**relevant_dimension):
        source = decode_source(
            code, relevant_dimension, len(algebra.names)
        )
        cube = algebra.cube(source)
        preimage.setdefault(cube, (code, source))

    values = sorted(preimage)
    value_set = set(values)
    noncommuting = False
    for left in values:
        for right in values:
            if algebra.multiply(left, right) != algebra.multiply(right, left):
                noncommuting = True
            if algebra.circle(left, right) not in value_set:
                left_code, left_source = preimage[left]
                right_code, right_source = preimage[right]
                packed = left_code * (3**relevant_dimension) + right_code
                return (
                    len(values),
                    noncommuting,
                    (packed, left_source, right_source),
                )
    return len(values), noncommuting, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iterations", type=int, default=40)
    parser.add_argument("--solver-timeout", type=int, default=90)
    parser.add_argument("--certificate-dir", type=Path)
    arguments = parser.parse_args()

    solver = shutil.which("z3")
    if solver is None:
        print("ERROR|z3_not_found", file=sys.stderr)
        return 2
    if arguments.certificate_dir is not None:
        arguments.certificate_dir.mkdir(parents=True, exist_ok=True)

    model, lines, ledger = build_core()
    relevant_names = [
        name
        for name, degree in model.basis
        if degree <= RELEVANT_MAX_DEGREE
    ]
    print(
        "CEGIS_START"
        f"|profile={','.join(str(value) for value in PROFILE)}"
        f"|structure_variables={ledger['structure_variables']}"
        f"|associativity={ledger['associativity']}"
        f"|surjectivity={ledger['surjectivity']}"
        f"|relevant_dimension={ledger['relevant_dimension']}"
        f"|cube_inputs={3 ** ledger['relevant_dimension']}"
        f"|witness_variables={ledger['witness_variables']}"
        f"|max_iterations={arguments.max_iterations}"
        f"|solver_timeout={arguments.solver_timeout}"
    )

    total_smt_ms = 0
    for iteration in range(arguments.max_iterations + 1):
        certificate = None
        if arguments.certificate_dir is not None:
            certificate = (
                arguments.certificate_dir / f"iteration_{iteration:03d}.smt2"
            )
        status, assignments, smt_ms = solve_structure(
            model,
            lines,
            solver,
            arguments.solver_timeout,
            certificate,
        )
        total_smt_ms += smt_ms
        if status == "unsat":
            print(
                "CEGIS_UNSAT"
                f"|iteration={iteration}"
                f"|root_constraints={iteration}"
                f"|smt_ms={smt_ms}"
                f"|total_smt_ms={total_smt_ms}"
            )
            print("DONE")
            return 0
        if status == "timeout":
            print(
                "CEGIS_INCOMPLETE"
                f"|reason=solver_timeout"
                f"|iteration={iteration}"
                f"|root_constraints={iteration}"
                f"|smt_ms={smt_ms}"
                f"|total_smt_ms={total_smt_ms}"
            )
            print("DONE")
            return 3
        if status != "sat":
            raise RuntimeError(f"unexpected solver status: {status}")

        algebra = ConcreteAlgebra(model, assignments)
        checked_at = time.monotonic()
        cube_values, noncommuting, missing = check_raw_closure(
            algebra, ledger["relevant_dimension"]
        )
        check_ms = round((time.monotonic() - checked_at) * 1000)
        if missing is None:
            print(
                "CEGIS_HIT"
                f"|iteration={iteration}"
                f"|root_constraints={iteration}"
                f"|cube_values={cube_values}"
                f"|noncommuting={str(noncommuting).lower()}"
                "|raw_closed=true"
                f"|smt_ms={smt_ms}"
                f"|check_ms={check_ms}"
            )
            if not noncommuting:
                raise RuntimeError("SMT witness was lost in concrete model")
            print("DONE")
            return 0

        packed, left_source, right_source = missing
        base = 3 ** ledger["relevant_dimension"]
        left_code, right_code = divmod(packed, base)
        print(
            "CEGIS_ITER"
            f"|iteration={iteration}"
            f"|root_constraints={iteration}"
            f"|cube_values={cube_values}"
            f"|noncommuting={str(noncommuting).lower()}"
            "|raw_closed=false"
            f"|missing_left={left_code}"
            f"|missing_right={right_code}"
            f"|smt_ms={smt_ms}"
            f"|check_ms={check_ms}"
        )
        add_closure_constraint(
            model,
            lines,
            relevant_names,
            left_source[: ledger["relevant_dimension"]],
            right_source[: ledger["relevant_dimension"]],
            iteration,
        )

    print(
        "CEGIS_INCOMPLETE"
        "|reason=iteration_limit"
        f"|iterations={arguments.max_iterations + 1}"
        f"|root_constraints={arguments.max_iterations + 1}"
        f"|total_smt_ms={total_smt_ms}"
    )
    print("DONE")
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
