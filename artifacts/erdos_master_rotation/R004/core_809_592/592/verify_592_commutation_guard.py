#!/usr/bin/env python3
"""Finite guards for the R004 #592 common-extension audit.

The first check is a minimal counterexample to *symmetric* merging of two
independently legal successor-slot extensions.  The second check records the
source-derived Case 4/5 schedules and verifies that ordered replay, unlike
symmetric merging, has no precedence cycle.

This is an interface counterexample and schedule check, not a decision of the
ordinal partition relation.
"""

from __future__ import annotations

import itertools
import json


TASKS = ("ST", "SU", "TU")
SOURCE_CONSTRAINTS = {
    "case4_inside": (("SU", "ST"), ("TU", "ST"), ("TU", "SU")),
    "case5_outside": (("ST", "SU"), ("ST", "TU"), ("SU", "TU")),
}


def child_index(ordered_children: tuple[int, ...], child: int) -> int:
    """Definition-10.23 successor label: children are indexed from one."""
    return ordered_children.index(child) + 1


def symmetric_merge_counterexample():
    # Two games start with the same successor node and, independently, each
    # creates what is its first child.  Each local clear-pair label is {1}.
    extension_a = (10,)
    extension_b = (20,)
    requested_label_a = {1}
    requested_label_b = {1}
    assert child_index(extension_a, 10) == 1
    assert child_index(extension_b, 20) == 1

    merged = tuple(sorted(set(extension_a) | set(extension_b)))
    actual_a = {child_index(merged, 10)}
    actual_b = {child_index(merged, 20)}
    assert actual_a == {1}
    assert actual_b == {2}
    assert requested_label_b != actual_b

    # Preallocating {2} for B does not repair symmetric legality: before A is
    # present, B's sole child still has index one.  It only becomes legal when
    # replayed after A has crossed a completion barrier.
    preallocated_b = {2}
    assert preallocated_b != {
        child_index(extension_b, 20)
    }
    assert preallocated_b == actual_b

    return {
        "base": "one successor-rank node with no constructed children",
        "extension_A": {
            "new_child_coordinate": 10,
            "locally_required_label": sorted(requested_label_a),
        },
        "extension_B": {
            "new_child_coordinate": 20,
            "locally_required_label": sorted(requested_label_b),
        },
        "merged_children": list(merged),
        "required_after_merge": {
            "A": sorted(actual_a),
            "B": sorted(actual_b),
        },
        "symmetric_merge_preserves_both_histories": False,
        "ordered_replay_A_then_B_uses_labels": [[1], [2]],
        "passed": True,
    }


def verify_successor_pushout_obstruction():
    """Enumerate the exact child-index obstruction beyond the minimal case.

    At a successor-rank node with r already constructed children, each
    independently appended first child has local index r+1.  In a union of k
    distinct appended children, their actual indices are r+1,...,r+k, so no
    label-preserving symmetric pushout can retain more than one of the k local
    histories.  Conversely, preassigning those distinct final labels makes
    every history except the first illegal when viewed on its own.
    """

    certificates = []
    for base_children in range(6):
        base = tuple(range(100, 100 + base_children))
        for extension_count in range(2, 6):
            new_children = tuple(
                1000 + 10 * i for i in range(extension_count)
            )
            local_required = base_children + 1
            for child in new_children:
                local_tree = base + (child,)
                assert child_index(local_tree, child) == local_required

            merged = base + new_children
            merged_indices = tuple(
                child_index(merged, child) for child in new_children
            )
            preserved = sum(
                actual == local_required for actual in merged_indices
            )
            assert merged_indices == tuple(
                range(base_children + 1, base_children + extension_count + 1)
            )
            assert preserved == 1

            preallocated_final_labels_legal_standalone = tuple(
                index == local_required for index in merged_indices
            )
            assert preallocated_final_labels_legal_standalone.count(True) == 1
            certificates.append(
                {
                    "base_child_count": base_children,
                    "independent_extensions": extension_count,
                    "each_local_required_index": local_required,
                    "indices_after_union": list(merged_indices),
                    "locally_preserved_histories": preserved,
                    "all_final_indices_legal_standalone":
                        all(preallocated_final_labels_legal_standalone),
                }
            )

    return {
        "configurations_checked": len(certificates),
        "certificates": certificates,
        "conclusion": (
            "The category of exact successor clear histories has no "
            "label-preserving symmetric pushout for two or more independently "
            "appended children.  Later children must be generated by "
            "pre-coordinated ordered replay."
        ),
        "passed": True,
    }


def topological_orders(constraints):
    return [
        order
        for order in itertools.permutations(TASKS)
        if all(
            order.index(before) < order.index(after)
            for before, after in constraints
        )
    ]


def verify_source_schedules():
    result = {}
    for name, constraints in SOURCE_CONSTRAINTS.items():
        orders = topological_orders(constraints)
        assert len(orders) == 1
        result[name] = {
            "constraints": [list(pair) for pair in constraints],
            "unique_ordered_replay": list(orders[0]),
            "passed": True,
        }
    return result


def verify_limit_successor_interface():
    # Hajnal--Larson Lemma 10.14: a rank-omega limit node has one child;
    # a successor-rank node r has max(r) children.  Definition 10.23 gives
    # these labels different meanings.
    limit_node = {
        "rank": "omega",
        "complete_child_count": 1,
        "label_semantics": "finite set of ranks of splitting nodes below it",
    }
    finite_root_max = 7
    successor_node = {
        "rank": 3,
        "complete_child_count": finite_root_max,
        "label_semantics": "finite set of child indices of partition nodes",
    }
    assert limit_node["complete_child_count"] == 1
    assert successor_node["complete_child_count"] == finite_root_max
    assert (
        limit_node["label_semantics"]
        != successor_node["label_semantics"]
    )
    return {
        "T_omega_limit_root": limit_node,
        "T_3_successor_root_example": successor_node,
        "blind_symbol_substitution_preserves_interface": False,
        "passed": True,
    }


def verify_finite_gamma_root_guard():
    # Definition 10.41: at a limit-rank node, a singleton label is already a
    # signal; labels of size >1 are signals at every rank.  Definition 10.42
    # cannot justify a signal at the root by an earlier limit ancestor, because
    # the root has no proper predecessor.  Hence a locally finite-Gamma-free
    # T(omega) family with omega not in Gamma must have empty root labels.
    gamma = {1, 2, 3}
    rows = []
    for label_size in range(5):
        is_signal = label_size > 1 or label_size == 1
        justified_by_rank = "omega" in gamma
        justified_by_limit_ancestor = False
        allowed = (
            not is_signal
            or justified_by_rank
            or justified_by_limit_ancestor
        )
        assert allowed == (label_size == 0)
        rows.append(
            {
                "root_label_size": label_size,
                "root_is_signal": is_signal,
                "allowed_in_locally_Gamma_free_T_omega": allowed,
            }
        )

    # A coarsening only deletes label entries.  Thus a pair history whose root
    # label is nonempty (the source Cases 4/5 start with d>0) cannot be a
    # coarsening of a finite-Gamma-free full label with empty root label.
    full_root_label = set()
    requested_case45_coarsening = {7}
    assert not requested_case45_coarsening <= full_root_label
    return {
        "Gamma": sorted(gamma),
        "root_label_table": rows,
        "finite_Gamma_free_forces_empty_T_omega_root_label": True,
        "case4_case5_d_positive_coarsening_possible": False,
        "conclusion": (
            "A single finite-Gamma-free T(omega) builder family cannot "
            "retain pair histories with positive root labels, including the "
            "source Case-4/5 d>0 histories.  This blocks the literal "
            "root-coded transplant, but not a redesigned empty-root builder "
            "branch with signals at finite-rank nodes."
        ),
        "passed": True,
    }


def main():
    result = {
        "claim": (
            "Arbitrary independent successor-slot extensions do not merge "
            "symmetrically; the source Cases instead admit unique ordered "
            "replay schedules.  The T(omega) limit root and T(3) successor "
            "root have different branching and label semantics."
        ),
        "minimal_noncommutation_certificate":
            symmetric_merge_counterexample(),
        "successor_pushout_obstruction":
            verify_successor_pushout_obstruction(),
        "source_schedules": verify_source_schedules(),
        "limit_successor_interface": verify_limit_successor_interface(),
        "finite_Gamma_root_guard": verify_finite_gamma_root_guard(),
        "scope_guard": (
            "The counterexample refutes only the naive symmetric-union "
            "lemma.  It does not refute a pre-coordinated ordered-replay "
            "lemma and does not decide Erdős #592."
        ),
        "passed": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
