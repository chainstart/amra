#!/usr/bin/env python3
"""Audit the small UNSAT core behind profile (3,1,1,1,1,1,1).

This is not needed for the final mathematical exclusion: the companion
human lemma proves cube commutativity directly.  It records how the original
500-associativity/21-surjectivity solver result was localized before that
lemma was found.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess

import cegis_dim9_profile_2111121 as engine


PROFILE = (3, 1, 1, 1, 1, 1, 1)
RELEVANT_MAX_DEGREE = 5

# A deletion-minimal subset of one Z3-produced core.  "Deletion-minimal"
# means that removing any one listed assertion makes this subset SAT; it
# does not claim globally minimum cardinality.
ARCHIVED_CORE = (
    "surj_03",
    "witness",
    "surj_12",
    "surj_11",
    "assoc_456",
    "assoc_444",
    "assoc_432",
    "assoc_378",
    "assoc_360",
    "assoc_313",
    "assoc_295",
    "assoc_290",
    "assoc_194",
    "assoc_155",
    "assoc_145",
    "assoc_075",
    "assoc_015",
    "assoc_000",
)


def build_blocks():
    engine.PROFILE = PROFILE
    engine.RELEVANT_MAX_DEGREE = RELEVANT_MAX_DEGREE
    model, lines, ledger = engine.build_core()
    base_end = 3 + 2 * ledger["structure_variables"]
    associativity_end = base_end + ledger["associativity"]
    surjectivity_end = associativity_end + ledger["surjectivity"]

    assertions = {
        f"assoc_{index:03d}": line
        for index, line in enumerate(lines[base_end:associativity_end])
    }
    assertions.update(
        {
            f"surj_{index:02d}": line
            for index, line in enumerate(
                lines[associativity_end:surjectivity_end]
            )
        }
    )
    assertions["witness"] = lines[-1]
    background = lines[:base_end] + lines[surjectivity_end:-1]
    return model, lines, ledger, assertions, background


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


def associativity_metadata(model):
    metadata = []
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
    return metadata


def surjectivity_metadata(model):
    metadata = []
    for target_degree in range(2, model.top_degree + 1):
        for left_degree in range(1, target_degree):
            metadata.append(
                (left_degree, target_degree - left_degree, target_degree)
            )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="z3")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--skip-deletion-check",
        action="store_true",
        help="do not rerun the 18 one-assertion deletions",
    )
    args = parser.parse_args()
    if shutil.which(args.solver) is None:
        raise SystemExit(f"solver not found: {args.solver}")

    model, full, ledger, assertions, background = build_blocks()
    associativity_names = [
        f"assoc_{index:03d}" for index in range(ledger["associativity"])
    ]
    surjectivity_names = [
        f"surj_{index:02d}" for index in range(ledger["surjectivity"])
    ]
    witness = ["witness"]

    def query(names):
        return background + [assertions[name] for name in names]

    statuses = {
        "full": solve(args.solver, full, args.timeout),
        "without_associativity": solve(
            args.solver,
            query(surjectivity_names + witness),
            args.timeout,
        ),
        "without_surjectivity": solve(
            args.solver,
            query(associativity_names + witness),
            args.timeout,
        ),
        "without_witness": solve(
            args.solver,
            query(associativity_names + surjectivity_names),
            args.timeout,
        ),
        "archived_core": solve(
            args.solver, query(list(ARCHIVED_CORE)), args.timeout
        ),
    }
    print(
        "DIM9_CORE_ABLATION|"
        + "|".join(f"{name}={value}" for name, value in statuses.items())
    )

    deletion_statuses = []
    if not args.skip_deletion_check:
        for removed in ARCHIVED_CORE:
            remaining = [name for name in ARCHIVED_CORE if name != removed]
            deletion_statuses.append(
                solve(args.solver, query(remaining), args.timeout)
            )
    deletion_minimal = (
        not args.skip_deletion_check
        and deletion_statuses
        and all(status == "sat" for status in deletion_statuses)
    )
    deletion_label = (
        "skipped"
        if args.skip_deletion_check
        else str(bool(deletion_minimal)).lower()
    )
    print(
        "DIM9_CORE|"
        f"assertions={len(ARCHIVED_CORE)}|"
        f"associativity={sum(n.startswith('assoc_') for n in ARCHIVED_CORE)}|"
        f"surjectivity={sum(n.startswith('surj_') for n in ARCHIVED_CORE)}|"
        "witness=1|"
        f"deletion_minimal={deletion_label}"
    )

    assoc_meta = associativity_metadata(model)
    surj_meta = surjectivity_metadata(model)
    for name in ARCHIVED_CORE:
        if name.startswith("assoc_"):
            index = int(name.split("_")[1])
            left, middle, right, output, ld, md, rd, od = assoc_meta[index]
            print(
                "CORE_ASSOC|"
                f"name={name}|triple={left},{middle},{right}|"
                f"degrees={ld},{md},{rd}->{od}|output={output}"
            )
        elif name.startswith("surj_"):
            index = int(name.split("_")[1])
            left_degree, right_degree, target_degree = surj_meta[index]
            print(
                "CORE_SURJ|"
                f"name={name}|split={left_degree}+{right_degree}"
                f"->{target_degree}"
            )

    expected = {
        "full": "unsat",
        "without_associativity": "sat",
        "without_surjectivity": "unsat",
        "without_witness": "sat",
        "archived_core": "unsat",
    }
    if statuses != expected:
        return 1
    if not args.skip_deletion_check and not deletion_minimal:
        return 1
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
