#!/usr/bin/env python3
"""Dimension-nine algebra-group profile reduction and minimal SMT model.

This is a necessary-condition search, not yet a complete raw-closure
classification.  It enumerates all power-filtration profiles with J^6 != 0,
applies the human degree/rank eliminations, and builds the smallest direct
noncommuting profile (2,2,2,1,1,1).

For that profile the SMT model includes:
  * the complete filtration-preserving multiplication table over F_3;
  * every filtered associativity identity;
  * every ordered-split power-filtration surjectivity condition;
  * bijectivity of the degree-one cube map, forced by raw closure together
    with two noncommuting cubes;
  * noncommutation of the two basis cubes;
  * existence of a cube root for their circle product.

Full raw closure is deliberately not claimed.  The output gives a strict
complexity ledger for the remaining counterexample-guided closure loop.
"""

from __future__ import annotations

import argparse
import itertools
import shutil
import subprocess
import sys
from pathlib import Path


PROFILE = (2, 2, 2, 1, 1, 1)
ZERO = "#b00"
ONE = "#b01"
TWO = "#b10"


def enumerate_profiles() -> tuple[tuple[int, ...], ...]:
    """All dimension-nine profiles with d1>=2 and nonzero layers through 6."""

    profiles: list[tuple[int, ...]] = []

    def extend(
        length: int, prefix: tuple[int, ...], remaining: int
    ) -> None:
        position = len(prefix)
        if position == length:
            if remaining == 0:
                profiles.append(prefix)
            return
        minimum = 2 if position == 0 else 1
        later_minimum = length - position - 1
        for value in range(minimum, remaining - later_minimum + 1):
            extend(length, prefix + (value,), remaining - value)

    for length in (6, 7, 8):
        extend(length, (), 9)
    return tuple(profiles)


def ff_add(terms: list[str]) -> str:
    """Nested addition in F_3 using the SMT helper fadd."""

    terms = [term for term in terms if term != ZERO]
    if not terms:
        return ZERO
    result = terms[0]
    for term in terms[1:]:
        result = f"(fadd {result} {term})"
    return result


def ff_multiply(*terms: str) -> str:
    """Nested multiplication in F_3 using the SMT helper fmul."""

    if ZERO in terms:
        return ZERO
    filtered = [term for term in terms if term != ONE]
    if not filtered:
        return ONE
    result = filtered[0]
    for term in filtered[1:]:
        result = f"(fmul {result} {term})"
    return result


def nonzero(expression: str) -> str:
    return f"(not (= {expression} {ZERO}))"


class FilteredModel:
    """Symbolic multiplication table for one fixed filtered profile."""

    def __init__(self, profile: tuple[int, ...]) -> None:
        self.profile = profile
        self.top_degree = len(profile)
        self.basis: list[tuple[str, int]] = []
        self.by_degree: dict[int, list[str]] = {}
        for degree, dimension in enumerate(profile, 1):
            self.by_degree[degree] = []
            for index in range(dimension):
                name = f"e{degree}_{index}"
                self.basis.append((name, degree))
                self.by_degree[degree].append(name)
        self.degree = dict(self.basis)
        self.products: dict[tuple[str, str], dict[str, str]] = {}
        self.structure_variables: list[str] = []
        for left, left_degree in self.basis:
            for right, right_degree in self.basis:
                target_degree = left_degree + right_degree
                if target_degree > self.top_degree:
                    continue
                entries: dict[str, str] = {}
                for output_degree in range(
                    target_degree, self.top_degree + 1
                ):
                    for output_name in self.by_degree[output_degree]:
                        variable = f"m_{left}_{right}_{output_name}"
                        entries[output_name] = variable
                        self.structure_variables.append(variable)
                self.products[(left, right)] = entries

    def product(
        self, left: dict[str, str], right: dict[str, str]
    ) -> dict[str, str]:
        output: dict[str, list[str]] = {
            name: [] for name, _ in self.basis
        }
        for left_name, left_coefficient in left.items():
            if left_coefficient == ZERO:
                continue
            for right_name, right_coefficient in right.items():
                if (
                    right_coefficient == ZERO
                    or (left_name, right_name) not in self.products
                ):
                    continue
                for target_name, structure_constant in self.products[
                    (left_name, right_name)
                ].items():
                    output[target_name].append(
                        ff_multiply(
                            left_coefficient,
                            right_coefficient,
                            structure_constant,
                        )
                    )
        return {
            name: ff_add(terms) for name, terms in output.items()
        }

    def cube(self, coefficients: dict[str, str]) -> dict[str, str]:
        return self.product(self.product(coefficients, coefficients), coefficients)

    def zero_vector(self) -> dict[str, str]:
        return {name: ZERO for name, _ in self.basis}


def declare_field_variable(lines: list[str], variable: str) -> None:
    lines.append(f"(declare-const {variable} (_ BitVec 2))")
    lines.append(f"(assert (not (= {variable} #b11)))")


def build_smt2() -> tuple[str, dict[str, int]]:
    """Build the QF_BV necessary-condition model and its exact ledger."""

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
                target_degree = left_degree + middle_degree + right_degree
                if target_degree > model.top_degree:
                    continue
                for output_degree in range(
                    target_degree, model.top_degree + 1
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
                condition = f"(or {' '.join(minors)})"
            else:
                raise ValueError("the minimal profile has no larger layer")
            lines.append(f"(assert {condition})")
            surjectivity_count += 1

    # Cubes of all nine degree-one vectors.
    degree_one_cubes: dict[tuple[int, int], dict[str, str]] = {}
    for first, second in itertools.product(range(3), repeat=2):
        vector = model.zero_vector()
        vector["e1_0"] = (ZERO, ONE, TWO)[first]
        vector["e1_1"] = (ZERO, ONE, TWO)[second]
        degree_one_cubes[(first, second)] = model.cube(vector)

    # Raw closure plus noncommuting cubes forces the projected cube image
    # q(A_1) to be all of the two-dimensional A_3.  Since both sets have
    # nine elements, q must be bijective.
    projection_constraints = 0
    for first_key, second_key in itertools.combinations(
        degree_one_cubes, 2
    ):
        first_cube = degree_one_cubes[first_key]
        second_cube = degree_one_cubes[second_key]
        differences = [
            nonzero(
                ff_add(
                    [
                        first_cube[name],
                        ff_multiply(TWO, second_cube[name]),
                    ]
                )
            )
            for name in model.by_degree[3]
        ]
        lines.append(f"(assert (or {' '.join(differences)}))")
        projection_constraints += 1

    x_cube = degree_one_cubes[(1, 0)]
    y_cube = degree_one_cubes[(0, 1)]
    xy = model.product(x_cube, y_cube)
    yx = model.product(y_cube, x_cube)
    commutator_coordinate = ff_add(
        [xy["e6_0"], ff_multiply(TWO, yx["e6_0"])]
    )
    lines.append(f"(assert {nonzero(commutator_coordinate)})")

    # One necessary raw-closure equation:
    # c^3 = x^3 + y^3 + x^3 y^3.
    root_variables: dict[str, str] = {}
    for name, _ in model.basis:
        variable = f"root_{name}"
        root_variables[name] = variable
        declare_field_variable(lines, variable)
    root_cube = model.cube(root_variables)
    circle_product = {
        name: ff_add([x_cube[name], y_cube[name], xy[name]])
        for name, _ in model.basis
    }
    for name, _ in model.basis:
        lines.append(f"(assert (= {root_cube[name]} {circle_product[name]}))")

    lines.append("(check-sat)")
    ledger = {
        "profiles": len(enumerate_profiles()),
        "structure_variables": len(model.structure_variables),
        "root_variables": len(root_variables),
        "associativity": associativity_count,
        "surjectivity": surjectivity_count,
        "projection_bijection": projection_constraints,
        "pair_closure_equations": len(model.basis),
    }
    return "\n".join(lines) + "\n", ledger


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-smt", type=Path)
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="solver timeout in seconds",
    )
    arguments = parser.parse_args()

    formula, ledger = build_smt2()
    if arguments.emit_smt is not None:
        arguments.emit_smt.write_text(formula, encoding="utf-8")

    print(
        "DIM9_PROFILES"
        f"|total={ledger['profiles']}"
        "|length6=21|length7=7|length8=1"
        "|length6_degree_pruned=20"
        "|minimal_direct=2,2,2,1,1,1"
    )
    print(
        "DIM9_MINIMAL_MODEL"
        f"|structure_variables={ledger['structure_variables']}"
        f"|root_variables={ledger['root_variables']}"
        f"|associativity={ledger['associativity']}"
        f"|surjectivity={ledger['surjectivity']}"
        f"|projection_bijection={ledger['projection_bijection']}"
        f"|pair_closure_equations={ledger['pair_closure_equations']}"
        "|full_raw_closure=false"
    )

    solver = shutil.which("z3")
    if solver is None:
        print("DIM9_SOLVER|result=not_run|reason=z3_not_found")
        return 2
    try:
        completed = subprocess.run(
            [solver, "-in"],
            input=formula,
            check=False,
            capture_output=True,
            text=True,
            timeout=arguments.timeout,
        )
    except subprocess.TimeoutExpired:
        print(
            f"DIM9_SOLVER|result=timeout|seconds={arguments.timeout}"
        )
        print("DONE")
        return 0
    if completed.returncode != 0:
        print(completed.stdout, end="", file=sys.stderr)
        print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode
    print(f"DIM9_SOLVER|result={completed.stdout.strip()}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
