#!/usr/bin/env python3
"""Exact minimal adversarial models for round-two typed conversion routes.

These checks kill only the mechanisms in their current carrier-blind or
universally quantified formulations.  They do not refute a future theorem
that adds a graph-specific conversion relation or a proved slack atomization.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path


def max_matching(left, neighbourhoods):
    right_owner = {}

    def augment(u, seen):
        for v in neighbourhoods[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in right_owner or augment(right_owner[v], seen):
                right_owner[v] = u
                return True
        return False

    return sum(augment(u, set()) for u in left)


def coverage_rank(demand_set, owner_neighbourhoods):
    return len(set().union(*(owner_neighbourhoods[u] for u in demand_set)))


# Audited n=14 tight-circuit data, reconstructed at the typed-carrier level.
colours = ("c1", "c2", "c3")
occupied_b = frozenset(("bc", "cz"))
full_reserves = {colour: occupied_b for colour in colours}
owned_a = {"c1": "x1y1", "c2": "x2y2", "c3": "x3y3"}
assert len(set(owned_a.values())) == 3
assert max_matching(colours, full_reserves) == 2
deficit = len(colours) - len(occupied_b)
assert deficit == 1

# M809C-01: there is no actual missing-B atom outside the occupied full
# reserve in the tight graph.  Therefore its claimed conversion matching has
# size zero, not the required deficit one.
external_conversion = {atom: frozenset() for atom in owned_a.values()}
assert max_matching(tuple(external_conversion), external_conversion) == 0

# M809C-02: coherence plus owned diagonals alone gives no absolute congestion
# bound.  For every t the exact typed incidence system can have t distinct A
# owners and one common full-reserve carrier.  Any total map has congestion t.
congestion_rows = []
for t in range(2, 13):
    owners = tuple(f"a{i}" for i in range(t))
    target = {owner: frozenset(("q",)) for owner in owners}
    assert max_matching(owners, target) == 1
    congestion_rows.append({"owners": t, "targets": 1, "forced_congestion": t})

# M809C-03: without an unused carrier or conversion arc the true conditional
# augmenting-path lemma has no trigger and cannot pay the tight circuit.
unused_b = occupied_b - set().union(*full_reserves.values())
assert not unused_b
assert max_matching(colours, full_reserves) == 2

# M809C-04: in the audited tight graph the only candidate new-B transversal is
# empty and the merged whole-rectangle scalar transference still has the
# actual endpoint M_B=2<D_B=3.  The proposed dichotomy does not pay the unit.
assert not set().union(*external_conversion.values())
assert len(occupied_b) == 2 < len(colours)

# M809C-06/07: two outer demands with the same sole putative slack carrier.
# Local one-unit statements pass, but the union rank is one and no disjoint
# injection exists.  The current low-edge ledger contains no theorem ruling
# this owner pattern out.
outer_demands = ("u1", "u2")
slack_neighbourhoods = {"u1": frozenset(("s",)), "u2": frozenset(("s",))}
assert all(coverage_rank((u,), slack_neighbourhoods) == 1 for u in outer_demands)
assert coverage_rank(outer_demands, slack_neighbourhoods) == 1
assert max_matching(outer_demands, slack_neighbourhoods) == 1

# M809C-09: an owned diagonal is a missing A edge.  The internal-low term is a
# set of present A edges.  With no explicit carrier map these typed sets can
# be disjoint even when their scalar sizes are compared.
owned_missing_a = frozenset(("xy",))
present_internal_low = frozenset()
assert owned_missing_a.isdisjoint(present_internal_low)

# M809C-10: the inherited exact normal form permits an outer-A blocker as an
# independent branch datum; no inherited implication supplies a repeated-B
# rectangle.  This minimal typed blocker has one outer demand, zero slack,
# and an empty rectangle family.
outer_blocker = {"demand": frozenset(("u",)), "slack": frozenset(), "rectangles": ()}
assert len(outer_blocker["demand"]) > len(outer_blocker["slack"])
assert not outer_blocker["rectangles"]

# M809C-12: two crossing circuits can share both their only B carrier and
# their only A owner.  Merging produces a larger deficit and no new typed
# carrier; any apparent decrease obtained by counting the owner twice is
# illegal.
circuits = (
    {"colours": frozenset(("c1", "c2")), "B": frozenset(("q",)), "A": frozenset(("a",))},
    {"colours": frozenset(("c2", "c3")), "B": frozenset(("q",)), "A": frozenset(("a",))},
)
assert all(len(circuit["colours"]) - len(circuit["B"]) == 1 for circuit in circuits)
merged_colours = set().union(*(circuit["colours"] for circuit in circuits))
merged_b = set().union(*(circuit["B"] for circuit in circuits))
merged_a = set().union(*(circuit["A"] for circuit in circuits))
assert len(merged_colours) - len(merged_b) == 2
assert len(merged_a) == 1

result = {
    "schema": "amra.erdos809.conversion-round2.minimal-falsification.v1",
    "inherited_exact_graph": {
        "source": "ab4b524 audited n=14 tight instance",
        "colours": list(colours),
        "full_B_reserve": sorted(occupied_b),
        "B_matching_rank": 2,
        "D_B": 3,
        "owned_A_atoms": sorted(owned_a.values()),
        "new_B_atoms_outside_full_reserve": [],
    },
    "tests": {
        "M809C-01": {
            "outcome": "killed",
            "reason": "required conversion matching has size 0 but circuit deficit is 1"
        },
        "M809C-02": {
            "outcome": "killed_in_coherence_only_form",
            "reason": "t distinct owners with one common carrier force congestion t",
            "finite_guard": congestion_rows,
            "all_parameter_model": "owners a_1,...,a_t all have the singleton target {q}"
        },
        "M809C-03": {
            "outcome": "killed_as_closure_mechanism",
            "reason": "the conditional augmenting-path fact has no unused-carrier or conversion-arc trigger on the tight circuit"
        },
        "M809C-04": {
            "outcome": "killed",
            "reason": "no new-B transversal exists and actual merged endpoint remains M_B=2<D_B=3"
        },
        "M809C-06": {
            "outcome": "killed_without_new_slack_geometry",
            "reason": "two uncancelled demands can request one carrier; disjoint-image assertion is not supplied by the colourwise ledger"
        },
        "M809C-07": {
            "outcome": "killed_without_new_slack_geometry",
            "reason": "rho_S({u1,u2})=1<2 although both singleton tests pass"
        },
        "M809C-09": {
            "outcome": "killed_in_direct-charge_form",
            "reason": "owned diagonal is a missing A edge while the internal-low term consists of present A edges; no injection is defined"
        },
        "M809C-10": {
            "outcome": "killed_from_current_normal_form",
            "reason": "a minimal outer-A blocker datum need not contain any repeated-B owned rectangle"
        },
        "M809C-12": {
            "outcome": "killed_as_typed-incidence_recursion",
            "reason": "crossing circuits share their only A and B carriers; merging leaves deficit 2 and only one owner"
        }
    },
    "survivor_boundaries": {
        "M809C-05": "No countermodel to a genuinely new graph-specific S_m atomization was found.",
        "M809C-08": "No graph satisfying the complete hard outer-A gate was found against the direct compatible-edge exit.",
        "M809C-11": "A typed min-max framework remains sound only if explicit conversion and slack ranks are first constructed."
    },
    "scope": (
        "The n=14 statements use inherited independently audited graph evidence. "
        "The remaining models are exact typed-incidence obstructions and kill "
        "claims from current data alone; they do not refute strengthened theorems "
        "that add new graph-specific conversion or slack geometry."
    ),
    "public_problem_changed": False,
    "main_term_changed": False,
}

output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
