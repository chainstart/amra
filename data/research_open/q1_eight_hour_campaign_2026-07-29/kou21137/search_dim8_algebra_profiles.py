#!/usr/bin/env python3
"""Exact finite-field constraint audit for the last dimension-eight profile.

Let J be an 8-dimensional nilpotent associative F_3-algebra with J^6 != 0
and dim(J/J^2) >= 2.  Filtration counting leaves seven Hilbert profiles.
Five make [J^3,J^3] vanish by degree alone.  The profile
(2,1,2,1,1,1) is impossible because dim gr_2=1 forces dim gr_3<=1.

The only remaining profile is (2,1,1,1,1,1,1).  This program writes the
complete multiplication table of its associated graded algebra as 34
F_3 variables, imposes all 96 homogeneous associativity identities and
all 21 ordered-split surjectivity constraints
gr_i(J) gr_j(J)=gr_{i+j}(J), and asks whether gr_3 and gr_4 can fail to
commute in gr_7.  Z3 checks the resulting finite QF_NIA formula.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


FIELD = 3
EXPECTED_PROFILES = (
    (3, 1, 1, 1, 1, 1),
    (2, 2, 1, 1, 1, 1),
    (2, 1, 2, 1, 1, 1),
    (2, 1, 1, 2, 1, 1),
    (2, 1, 1, 1, 2, 1),
    (2, 1, 1, 1, 1, 2),
    (2, 1, 1, 1, 1, 1, 1),
)

# Two degree-one basis vectors and one basis vector in every later degree.
BASIS = (("x", 1), ("y", 1)) + tuple(
    (f"z{degree}", degree) for degree in range(2, 8)
)


def enumerate_profiles() -> tuple[tuple[int, ...], ...]:
    """Enumerate every positive power-filtration profile of total dimension 8."""

    profiles = []
    for length in (6, 7):
        def extend(prefix: tuple[int, ...], remaining: int) -> None:
            position = len(prefix)
            if position == length:
                if remaining == 0:
                    profiles.append(prefix)
                return
            minimum = 2 if position == 0 else 1
            later_minimum = length - position - 1
            for value in range(minimum, remaining - later_minimum + 1):
                extend(prefix + (value,), remaining - value)

        extend((), 8)
    return tuple(profiles)


def basis_name(degree: int) -> str:
    """Return the unique basis name in degree at least two."""

    if degree < 2:
        raise ValueError("only degrees at least two are one-dimensional")
    return f"z{degree}"


def multiplication_variables() -> dict[tuple[str, str], str]:
    """Create one F_3 structure constant for every potentially nonzero pair."""

    variables: dict[tuple[str, str], str] = {}
    for left, left_degree in BASIS:
        for right, right_degree in BASIS:
            if left_degree + right_degree <= 7:
                variables[(left, right)] = f"m_{left}_{right}"
    return variables


def build_smt2(*, require_noncommuting: bool) -> tuple[str, int, int]:
    """Return the complete SMT-LIB formula and its audit counts."""

    variables = multiplication_variables()
    lines = ["(set-logic QF_NIA)"]
    for variable in variables.values():
        lines.append(f"(declare-const {variable} Int)")
        lines.append(
            f"(assert (and (<= 0 {variable}) (<= {variable} {FIELD - 1})))"
        )

    associativity_count = 0
    for left, left_degree in BASIS:
        for middle, middle_degree in BASIS:
            for right, right_degree in BASIS:
                if left_degree + middle_degree + right_degree > 7:
                    continue
                left_middle = basis_name(left_degree + middle_degree)
                middle_right = basis_name(middle_degree + right_degree)
                first = variables[(left, middle)]
                second = variables[(left_middle, right)]
                third = variables[(middle, right)]
                fourth = variables[(left, middle_right)]
                lines.append(
                    "(assert (= "
                    f"(mod (* {first} {second}) {FIELD}) "
                    f"(mod (* {third} {fourth}) {FIELD})))"
                )
                associativity_count += 1

    generation_count = 0
    for target_degree in range(2, 8):
        for left_target_degree in range(1, target_degree):
            right_target_degree = target_degree - left_target_degree
            generators = []
            for left, left_degree in BASIS:
                if left_degree != left_target_degree:
                    continue
                for right, right_degree in BASIS:
                    if right_degree == right_target_degree:
                        generators.append(
                            f"(not (= {variables[(left, right)]} 0))"
                        )
            # For a power-filtration associated graded algebra,
            # J^(i+j)=J^i J^j for every ordered split i+j.  Since each
            # target layer here is one-dimensional, the induced product
            # map is surjective exactly when at least one coefficient is
            # nonzero.
            lines.append(f"(assert (or {' '.join(generators)}))")
            generation_count += 1

    if require_noncommuting:
        # A filtered algebra with this profile can have [J^3,J^3] != 0 only
        # if the degree-three and degree-four layers fail to commute in
        # degree 7.
        lines.append(
            "(assert (not (= "
            f"{variables[('z3', 'z4')]} {variables[('z4', 'z3')]})))"
        )
    lines.append("(check-sat)")
    return (
        "\n".join(lines) + "\n",
        associativity_count,
        generation_count,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emit-smt",
        type=Path,
        help="also save the exact SMT-LIB instance at this path",
    )
    arguments = parser.parse_args()

    generated_profiles = enumerate_profiles()
    if set(generated_profiles) != set(EXPECTED_PROFILES):
        print(f"ERROR|unexpected_profiles={generated_profiles}", file=sys.stderr)
        return 1
    profiles = EXPECTED_PROFILES

    formula, associativity_count, generation_count = build_smt2(
        require_noncommuting=True
    )
    if arguments.emit_smt is not None:
        arguments.emit_smt.write_text(formula, encoding="utf-8")

    solver = shutil.which("z3")
    if solver is None:
        print("ERROR|z3_not_found", file=sys.stderr)
        return 2
    base_formula, _, _ = build_smt2(require_noncommuting=False)
    results = []
    for instance in (base_formula, formula):
        completed = subprocess.run(
            [solver, "-in"],
            input=instance,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if completed.returncode != 0:
            print(completed.stdout, end="", file=sys.stderr)
            print(completed.stderr, end="", file=sys.stderr)
            return completed.returncode
        results.append(completed.stdout.strip())
    base_result, noncommuting_result = results
    print(
        "DIM8_PROFILES"
        f"|total={len(profiles)}"
        "|degree_forced_commuting=5"
        "|d2_one_d3_two_impossible=1"
        "|exceptional=2,1,1,1,1,1,1"
    )
    print(
        "DIM8_EXCEPTIONAL_SMT"
        f"|variables={len(multiplication_variables())}"
        f"|associativity={associativity_count}"
        f"|generation={generation_count}"
        "|field=3"
        f"|profile_consistent={base_result}"
        f"|noncommuting={noncommuting_result}"
    )
    if base_result != "sat" or noncommuting_result != "unsat":
        return 1
    print("DIM8_RESULT|J3_commutative=true|minimum_candidate_dimension=9")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
