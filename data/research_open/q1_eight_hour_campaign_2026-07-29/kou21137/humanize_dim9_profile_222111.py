#!/usr/bin/env python3
"""Grouped deletion audit for profile (2,2,2,1,1,1).

The original formula included filtered associativity, layer surjectivity,
cube-projection bijectivity, a noncommuting-cube witness, and one
circle-product cube root.  This audit verifies that only leading graded
associativity and the witness are needed.  The companion tensor lemma is
the human proof of that reduced contradiction.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess

import search_dim9_algebra_profiles as source


def solve(solver: str, lines: list[str], timeout: int) -> str:
    try:
        completed = subprocess.run(
            [solver, "-in"],
            input="\n".join(lines + ["(check-sat)"]) + "\n",
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    if not completed.stdout.splitlines():
        return "error"
    return completed.stdout.splitlines()[0].strip()


def build_groups():
    formula, ledger = source.build_smt2()
    lines = formula.strip().splitlines()
    base_end = 3 + 2 * ledger["structure_variables"]
    associativity_end = base_end + ledger["associativity"]
    surjectivity_end = associativity_end + ledger["surjectivity"]
    projection_end = (
        surjectivity_end + ledger["projection_bijection"]
    )
    noncommuting_index = projection_end
    root_declarations_end = (
        noncommuting_index + 1 + 2 * ledger["root_variables"]
    )
    closure_end = (
        root_declarations_end + ledger["pair_closure_equations"]
    )

    model = source.FilteredModel(source.PROFILE)
    metadata = []
    for left, left_degree in model.basis:
        for middle, middle_degree in model.basis:
            for right, right_degree in model.basis:
                minimum_degree = (
                    left_degree + middle_degree + right_degree
                )
                if minimum_degree > model.top_degree:
                    continue
                for output_degree in range(
                    minimum_degree, model.top_degree + 1
                ):
                    for output_name in model.by_degree[output_degree]:
                        metadata.append(
                            (
                                left,
                                middle,
                                right,
                                output_name,
                                left_degree,
                                middle_degree,
                                right_degree,
                                output_degree,
                            )
                        )

    associativity = lines[base_end:associativity_end]
    leading_associativity = [
        assertion
        for assertion, item in zip(associativity, metadata)
        if item[7] == item[4] + item[5] + item[6]
    ]
    groups = {
        "domain": lines[:base_end],
        "all_associativity": associativity,
        "leading_associativity": leading_associativity,
        "surjectivity": lines[
            associativity_end:surjectivity_end
        ],
        "projection_bijection": lines[
            surjectivity_end:projection_end
        ],
        "noncommuting": [lines[noncommuting_index]],
        "root_declarations": lines[
            noncommuting_index + 1:root_declarations_end
        ],
        "closure_equations": lines[root_declarations_end:closure_end],
    }
    return groups, ledger


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="z3")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()
    if shutil.which(args.solver) is None:
        raise SystemExit(f"solver not found: {args.solver}")

    groups, ledger = build_groups()

    def query(*names: str) -> list[str]:
        output: list[str] = []
        for name in names:
            output.extend(groups[name])
        return output

    statuses = {
        "canonical": solve(
            args.solver,
            query(
                "domain",
                "all_associativity",
                "surjectivity",
                "projection_bijection",
                "noncommuting",
                "root_declarations",
                "closure_equations",
            ),
            args.timeout,
        ),
        "without_closure_root": solve(
            args.solver,
            query(
                "domain",
                "all_associativity",
                "surjectivity",
                "projection_bijection",
                "noncommuting",
            ),
            args.timeout,
        ),
        "graded_core": solve(
            args.solver,
            query(
                "domain", "leading_associativity", "noncommuting"
            ),
            args.timeout,
        ),
        "graded_without_associativity": solve(
            args.solver,
            query("domain", "noncommuting"),
            args.timeout,
        ),
        "graded_without_noncommuting": solve(
            args.solver,
            query("domain", "leading_associativity"),
            args.timeout,
        ),
    }
    print(
        "DIM9_222111_GROUPED_DELETION|"
        + "|".join(f"{name}={status}" for name, status in statuses.items())
    )
    active_text = " ".join(
        groups["leading_associativity"] + groups["noncommuting"]
    )
    active_variables = set(
        re.findall(r"m_[A-Za-z0-9_]+", active_text)
    )
    print(
        "DIM9_222111_REDUCED_CORE|"
        f"declared_structure_variables={ledger['structure_variables']}|"
        f"active_leading_variables={len(active_variables)}|"
        f"leading_associativity={len(groups['leading_associativity'])}|"
        "surjectivity=0|projection_bijection=0|root_variables=0|"
        "closure_equations=0|noncommuting=1"
    )
    expected = {
        "canonical": "unsat",
        "without_closure_root": "unsat",
        "graded_core": "unsat",
        "graded_without_associativity": "sat",
        "graded_without_noncommuting": "sat",
    }
    if statuses != expected:
        return 1
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
