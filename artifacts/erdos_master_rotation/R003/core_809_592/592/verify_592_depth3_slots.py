#!/usr/bin/env python3
"""Finite guards for the R003 depth-three slot-block proposal for Erdős #592.

This program checks only the finite precedence and address-allocation layer of
the proposal.  In particular, it does *not* formalize T(3), the game G(h,N),
conservative play, critical/decision nodes, or the push-up condition.
"""

from __future__ import annotations

import itertools
import json


TREES = ("S", "T", "U")
TASKS = ("ST", "SU", "TU")
RANKS = (3, 2, 1)

# These are the "smaller levels / larger levels" comparisons printed in
# Hajnal--Larson, Lemma 10.38, Cases 4 and 5.  A task name denotes the
# interaction of the two trees named by its two letters.
SOURCE_CONSTRAINTS = {
    "case4_inside": (
        ("SU", "ST"),  # at S
        ("TU", "ST"),  # at T
        ("TU", "SU"),  # at U
    ),
    "case5_outside": (
        ("ST", "SU"),  # at S
        ("ST", "TU"),  # at T
        ("SU", "TU"),  # at U
    ),
}


def topological_orders(constraints):
    return [
        order
        for order in itertools.permutations(TASKS)
        if all(order.index(left) < order.index(right)
               for left, right in constraints)
    ]


def incident_tasks(tree):
    return tuple(task for task in TASKS if tree in task)


def other_endpoint(task, tree):
    assert tree in task
    return task[1] if task[0] == tree else task[0]


def allocate_certificate(case_name, order, block_size=2):
    """Allocate two nonempty successor-slot blocks down to rank one."""
    task_position = {task: i for i, task in enumerate(order)}
    next_code = 100
    nodes = []
    frontier = [(tree, 3, ()) for tree in TREES]

    while frontier:
        tree, rank, address = frontier.pop(0)
        if rank == 0:
            continue

        local_tasks = sorted(
            incident_tasks(tree), key=lambda task: task_position[task]
        )
        blocks = []
        for task in local_tasks:
            slot_codes = list(
                range(next_code, next_code + 7 * block_size, 7)
            )
            next_code += 7 * block_size
            blocks.append(
                {
                    "task": task,
                    "toward": other_endpoint(task, tree),
                    "slot_codes": slot_codes,
                }
            )

        nodes.append(
            {
                "tree": tree,
                "rank": rank,
                "address": list(address),
                "blocks": blocks,
                "full_label": [
                    code
                    for block in blocks
                    for code in block["slot_codes"]
                ],
            }
        )

        if rank > 1:
            for block in blocks:
                for slot_code in block["slot_codes"]:
                    frontier.append(
                        (
                            tree,
                            rank - 1,
                            address + (slot_code,),
                        )
                    )

    return {
        "case": case_name,
        "global_task_order": list(order),
        "nodes": nodes,
    }


def verify_certificate(certificate, constraints):
    order = tuple(certificate["global_task_order"])
    assert set(order) == set(TASKS) and len(order) == len(TASKS)
    assert all(order.index(left) < order.index(right)
               for left, right in constraints)
    position = {task: i for i, task in enumerate(order)}

    seen_node_keys = set()
    seen_codes = set()
    ranks_by_tree = {tree: set() for tree in TREES}
    pair_block_coarsenings_checked = 0

    for node in certificate["nodes"]:
        tree = node["tree"]
        rank = node["rank"]
        address = tuple(node["address"])
        key = (tree, rank, address)
        assert key not in seen_node_keys
        seen_node_keys.add(key)
        ranks_by_tree[tree].add(rank)

        blocks = node["blocks"]
        assert len(blocks) == 2
        assert {block["task"] for block in blocks} == set(
            incident_tasks(tree)
        )
        assert len(node["full_label"]) >= 2
        assert len(node["full_label"]) == len(set(node["full_label"]))

        local_positions = [position[block["task"]] for block in blocks]
        assert local_positions == sorted(local_positions)
        previous_max = 0
        reconstructed_full_label = []
        for block in blocks:
            slot_codes = block["slot_codes"]
            assert slot_codes
            assert previous_max < slot_codes[0]
            previous_max = slot_codes[-1]
            reconstructed_full_label.extend(slot_codes)
            for code in slot_codes:
                assert code not in seen_codes
                seen_codes.add(code)
            # Definition 10.23 permits a finite set of child indices at a
            # successor node.  The pair coarsening is this nonempty block.
            pair_label = set(slot_codes)
            assert pair_label
            pair_block_coarsenings_checked += 1
        assert reconstructed_full_label == node["full_label"]

    assert all(ranks_by_tree[tree] == set(RANKS) for tree in TREES)

    block_size = len(certificate["nodes"][0]["blocks"][0]["slot_codes"])
    branching = 2 * block_size
    expected_nodes = len(TREES) * (1 + branching + branching ** 2)
    assert len(certificate["nodes"]) == expected_nodes
    assert len(seen_codes) == branching * len(certificate["nodes"])
    return {
        "abstract_nodes": len(certificate["nodes"]),
        "fresh_codes": len(seen_codes),
        "block_size_in_recursive_certificate": block_size,
        "pair_block_coarsenings_checked": pair_block_coarsenings_checked,
        "forecast_ranks_seen_per_tree": {
            tree: sorted(ranks_by_tree[tree], reverse=True)
            for tree in TREES
        },
        "passed": True,
    }


def verify_all_local_block_sizes(order):
    """Exhaust all six oriented block sizes in {1,2,3} at one rank."""
    position = {task: i for i, task in enumerate(order)}
    half_edges = tuple(
        (tree, task)
        for tree in TREES
        for task in incident_tasks(tree)
    )
    checked = 0
    for values in itertools.product((1, 2, 3), repeat=len(half_edges)):
        sizes = dict(zip(half_edges, values))
        next_child = {tree: 1 for tree in TREES}
        allocated = {}
        for task in order:
            for tree in TREES:
                if tree not in task:
                    continue
                size = sizes[(tree, task)]
                start = next_child[tree]
                allocated[(tree, task)] = tuple(range(start, start + size))
                next_child[tree] += size

        for tree in TREES:
            local_tasks = sorted(
                incident_tasks(tree), key=lambda task: position[task]
            )
            left, right = (
                allocated[(tree, task)] for task in local_tasks
            )
            assert left and right and max(left) < min(right)
            assert set(left).isdisjoint(right)
        checked += 1
    assert checked == 3 ** 6
    return checked


def enumerate_orientation_layer():
    """Count all orientations of the three local comparisons.

    Two of the eight arbitrary orientations are cyclic.  They are a guard
    against accidentally treating arbitrary pair-task specifications as
    automatically schedulable; they are not source-derived Cases 4 or 5.
    """
    undirected = (("ST", "SU"), ("ST", "TU"), ("SU", "TU"))
    records = []
    for bits in itertools.product((0, 1), repeat=3):
        constraints = tuple(
            pair if bit == 0 else (pair[1], pair[0])
            for pair, bit in zip(undirected, bits)
        )
        orders = topological_orders(constraints)
        records.append(
            {
                "constraints": [list(item) for item in constraints],
                "satisfiable": bool(orders),
                "orders": [list(order) for order in orders],
            }
        )
    return records


def main():
    cases = {}
    for case_name, constraints in SOURCE_CONSTRAINTS.items():
        orders = topological_orders(constraints)
        assert len(orders) == 1
        certificate = allocate_certificate(case_name, orders[0], block_size=2)
        cases[case_name] = {
            "constraints": [list(item) for item in constraints],
            "topological_orders": [list(order) for order in orders],
            "local_positive_block_size_assignments_checked_per_rank":
                verify_all_local_block_sizes(orders[0]),
            "certificate_summary":
                verify_certificate(certificate, constraints),
        }

    orientation_records = enumerate_orientation_layer()
    satisfiable = sum(item["satisfiable"] for item in orientation_records)
    assert satisfiable == 6

    print(
        json.dumps(
            {
                "claim": (
                    "The source-derived top-level precedence constraints in "
                    "Lemma 10.38 Cases 4 and 5 are acyclic, and a collision-"
                    "free depth-three two-block address skeleton exists."
                ),
                "cases": cases,
                "arbitrary_orientation_guard": {
                    "specifications": len(orientation_records),
                    "acyclic": satisfiable,
                    "cyclic": len(orientation_records) - satisfiable,
                    "interpretation": (
                        "The two cyclic arbitrary orientations are not "
                        "source-derived game positions."
                    ),
                },
                "scope_guard": (
                    "This finite check does not prove the common-extension/"
                    "commutation lemma, game legality, conservative play, "
                    "critical-node compatibility, or push-up."
                ),
                "passed": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
