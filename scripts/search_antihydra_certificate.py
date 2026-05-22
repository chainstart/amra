#!/usr/bin/env python3
"""Search for Antihydra prefix-inequality certificate candidates.

This is an experimental helper for the Beaver Math Olympiad Antihydra target.
It does not claim an infinite proof by itself.  It works on the exact
odd-block acceleration from the natural-language proof attack and tries to
find finite potential tables that explain the observed trajectory.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "proof_attack" / "antihydra_certificate"


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 expects a positive integer")
    return (n & -n).bit_length() - 1


@dataclass(frozen=True)
class Block:
    index: int
    y: int
    odd_run: int
    even_run: int
    next_y: int
    credit_before: int
    credit_after: int

    @property
    def min_credit_inside(self) -> int:
        return self.credit_before - self.odd_run


def next_odd_block(y: int) -> tuple[int, int, int]:
    """Return (odd_run, even_run, next_odd_start) for odd block start y."""
    if y % 2 == 0:
        raise ValueError("odd block must start at an odd value")
    odd_run = v2(y - 1)
    z = 1 + pow(3, odd_run) * ((y - 1) // (1 << odd_run))
    if z % 2 != 0:
        raise AssertionError("odd block did not end at an even value")
    even_run = v2(z)
    next_y = pow(3, even_run) * (z // (1 << even_run))
    if next_y % 2 != 1:
        raise AssertionError("even block did not end at an odd value")
    return odd_run, even_run, next_y


def iter_blocks(limit: int) -> list[Block]:
    # Starting sequence: 8, 12, 18 are even, then first odd block starts at 27.
    y = 27
    credit = 6
    blocks: list[Block] = []
    for index in range(limit):
        odd_run, even_run, next_y = next_odd_block(y)
        after = credit - odd_run + 2 * even_run
        blocks.append(
            Block(
                index=index,
                y=y,
                odd_run=odd_run,
                even_run=even_run,
                next_y=next_y,
                credit_before=credit,
                credit_after=after,
            )
        )
        y = next_y
        credit = after
    return blocks


def block_key(y: int, *, bits: int, include_v2_plus: bool = True) -> tuple[int, ...]:
    modulus = 1 << bits
    key: list[int] = [y % modulus, v2(y - 1)]
    if include_v2_plus:
        key.append(v2(y + 1))
    return tuple(key)


def build_observed_constraints(blocks: Iterable[Block], *, bits: int) -> tuple[set[tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...], int, int]]]:
    states: set[tuple[int, ...]] = set()
    edges: list[tuple[tuple[int, ...], tuple[int, ...], int, int]] = []
    for block in blocks:
        src = block_key(block.y, bits=bits)
        dst = block_key(block.next_y, bits=bits)
        states.add(src)
        states.add(dst)
        # Constraint: F(src) >= F(dst) + odd_run - 2*even_run and F(src) >= odd_run.
        edges.append((src, dst, block.odd_run - 2 * block.even_run, block.odd_run))
    return states, edges


def solve_potential(
    states: set[tuple[int, ...]],
    edges: list[tuple[tuple[int, ...], tuple[int, ...], int, int]],
    *,
    max_iterations: int | None = None,
) -> tuple[dict[tuple[int, ...], int] | None, str]:
    potential = {state: 0 for state in states}
    for src, _dst, _weight, odd_run in edges:
        potential[src] = max(potential[src], odd_run)

    max_iterations = max_iterations or max(1, len(states) * 3)
    for _ in range(max_iterations):
        changed = False
        for src, dst, weight, odd_run in edges:
            required = max(odd_run, potential[dst] + weight)
            if required > potential[src]:
                potential[src] = required
                changed = True
        if not changed:
            return potential, "solved"

    return None, "positive_cycle_or_iteration_limit"


def summarize(blocks: list[Block]) -> dict[str, object]:
    odd_runs = Counter(block.odd_run for block in blocks)
    even_runs = Counter(block.even_run for block in blocks)
    min_credit_block = min(blocks, key=lambda block: block.min_credit_inside)
    max_odd_block = max(blocks, key=lambda block: block.odd_run)
    return {
        "block_count": len(blocks),
        "min_credit_inside": min_credit_block.min_credit_inside,
        "min_credit_block": asdict(min_credit_block),
        "max_odd_run": max_odd_block.odd_run,
        "max_odd_run_block": asdict(max_odd_block),
        "odd_run_counts_top": odd_runs.most_common(20),
        "even_run_counts_top": even_runs.most_common(20),
        "final_credit": blocks[-1].credit_after if blocks else 6,
        "final_odd_start_digits": len(str(blocks[-1].next_y)) if blocks else 2,
    }


def write_report(
    *,
    output_dir: Path,
    blocks: list[Block],
    bit_results: list[dict[str, object]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "amra.antihydra_certificate_search.v1",
        "summary": summarize(blocks),
        "bit_results": bit_results,
        "sample_blocks": [asdict(block) for block in blocks[:20]],
        "tail_blocks": [asdict(block) for block in blocks[-20:]],
        "interpretation": (
            "Observed-potential tables are empirical certificates for the sampled trajectory only. "
            "A full proof needs a finite quotient whose transition coverage is proved for all reachable odd-block states."
        ),
    }
    (output_dir / "certificate_search.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Antihydra Certificate Search",
        "",
        payload["interpretation"],
        "",
        "## Trajectory Summary",
        "",
    ]
    for key, value in payload["summary"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Observed Potential Tables", ""])
    lines.append("| Bits | States | Edges | Status | Initial potential | Max potential | Colliding keys |")
    lines.append("| ---: | ---: | ---: | --- | ---: | ---: | ---: |")
    for item in bit_results:
        lines.append(
            f"| {item['bits']} | {item['state_count']} | {item['edge_count']} | {item['status']} | "
            f"{item.get('initial_potential', '')} | {item.get('max_potential', '')} | {item['collision_count']} |"
        )
    lines.extend(
        [
            "",
            "## Next Proof Obligation",
            "",
            "Find a quotient and potential whose transition table covers every reachable odd-block state, not only sampled states.",
            "The required inequalities are `F(q) >= odd_run(q)` and `F(q) - odd_run(q) + 2*even_run(q) >= F(q')`.",
        ]
    )
    (output_dir / "certificate_search.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=int, default=10000)
    parser.add_argument("--min-bits", type=int, default=8)
    parser.add_argument("--max-bits", type=int, default=20)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    blocks = iter_blocks(max(1, args.blocks))
    bit_results: list[dict[str, object]] = []
    initial_key_by_bits: dict[int, tuple[int, ...]] = {}
    for bits in range(args.min_bits, args.max_bits + 1):
        states, edges = build_observed_constraints(blocks, bits=bits)
        potential, status = solve_potential(states, edges)
        initial = block_key(27, bits=bits)
        initial_key_by_bits[bits] = initial
        keyed_transitions: dict[tuple[int, ...], set[tuple[int, int, tuple[int, ...]]]] = defaultdict(set)
        for src, dst, weight, odd_run in edges:
            keyed_transitions[src].add((weight, odd_run, dst))
        collisions = sum(1 for variants in keyed_transitions.values() if len(variants) > 1)
        item: dict[str, object] = {
            "bits": bits,
            "state_count": len(states),
            "edge_count": len(edges),
            "status": status,
            "collision_count": collisions,
        }
        if potential is not None:
            item["initial_potential"] = potential.get(initial)
            item["max_potential"] = max(potential.values()) if potential else 0
            item["states_above_initial_credit"] = sum(1 for value in potential.values() if value > 6)
        bit_results.append(item)

    write_report(output_dir=args.output_dir, blocks=blocks, bit_results=bit_results)
    print(args.output_dir / "certificate_search.md")
    print(json.dumps({"summary": summarize(blocks), "bit_results": bit_results}, indent=2)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
