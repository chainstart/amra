#!/usr/bin/env python3
"""Bounded exact adversarial probes for Erdős-809 conversion round three."""

from fractions import Fraction
import json


def matching_rank(neighbourhoods: dict[str, set[str]]) -> int:
    owner: dict[str, str] = {}

    def augment(demand: str, seen: set[str]) -> bool:
        for carrier in neighbourhoods[demand]:
            if carrier in seen:
                continue
            seen.add(carrier)
            if carrier not in owner or augment(owner[carrier], seen):
                owner[carrier] = demand
                return True
        return False

    return sum(augment(demand, set()) for demand in neighbourhoods)


def main() -> None:
    # M02: a real-mass carrier polytope need not have an integral assignment.
    # One demand is fractionally covered by two half-capacity actual carriers.
    fractional = {"x_d_c1": Fraction(1, 2), "x_d_c2": Fraction(1, 2)}
    assert sum(fractional.values()) == 1
    assert all(value < 1 for value in fractional.values())

    # M03: Hall feasibility can be exactly tight, leaving no strict surplus to
    # absorb a positive irrational rounding cell.
    tight = {"d1": {"c1"}, "d2": {"c2"}, "d3": {"c3"}}
    assert matching_rank(tight) == 3
    tight_cut_surplus = len(set().union(*tight.values())) - len(tight)
    assert tight_cut_surplus == 0

    # M04 and M06: compatibility of outputs does not imply disjoint witness
    # paths; conversely a conflict representation has no degree bound without
    # a graph theorem.  All certificates may share one bottleneck.
    K = 12
    paths = {f"colour_{i}": {"shared_vertex", f"private_{i}"} for i in range(K)}
    assert len(set.intersection(*(set(path) for path in paths.values()))) == 1
    conflict_degrees = {colour: K - 1 for colour in paths}
    assert min(conflict_degrees.values()) == K - 1

    # M07: the inherited actual three-demand circuit has only the two licensed
    # carriers bc,cz.  Naming three distinct A owners does not create a third.
    circuit = {"d1": {"bc", "cz"}, "d2": {"bc", "cz"}, "d3": {"bc", "cz"}}
    assert matching_rank(circuit) == 2
    proposed_one_step_outputs = {"bc", "cz"}
    occupied = {"bc", "cz"}
    assert not (proposed_one_step_outputs - occupied)

    # M09: a boundary map can have arbitrarily large fibres in rectangular
    # blow-up data unless endpoint uniqueness is separately proved.
    owners = [f"a{i}" for i in range(K)]
    boundary_image = {owner: "shared_B_pair" for owner in owners}
    max_fibre = max(sum(image == target for image in boundary_image.values())
                    for target in set(boundary_image.values()))
    assert max_fibre == K

    # M10: crossing typed circuits can share both an owner and a carrier.  Any
    # operation that duplicates either changes ownership; deleting either
    # incidence changes a demand neighbourhood.  Thus a lossless forest claim
    # needs an additional exchange axiom not present in the representation.
    circuit_one = {"owners": {"a", "x"}, "carriers": {"b", "u"}}
    circuit_two = {"owners": {"a", "y"}, "carriers": {"b", "v"}}
    assert circuit_one["owners"] & circuit_two["owners"] == {"a"}
    assert circuit_one["carriers"] & circuit_two["carriers"] == {"b"}

    print(json.dumps({
        "schema": "amra.erdos809.round3.falsification.v1",
        "tests": {
            "M809R3-02": {
                "outcome": "killed",
                "classification": "fractional mass is not an integral carrier",
                "witness": {key: str(value) for key, value in fractional.items()},
            },
            "M809R3-03": {
                "outcome": "killed",
                "classification": "Hall cuts need not have strict surplus",
                "tight_cut_surplus": tight_cut_surplus,
            },
            "M809R3-04": {
                "outcome": "killed",
                "classification": "compatibility does not provide disjoint path certificates",
                "shared_bottleneck": "shared_vertex",
                "colour_count": K,
            },
            "M809R3-06": {
                "outcome": "killed",
                "classification": "no inherited sublinear conflict-degree bound",
                "conflict_degree": K - 1,
            },
            "M809R3-07": {
                "outcome": "killed",
                "classification": "one-step rectangle output creates no new carrier on inherited actual circuit",
                "matching_rank": 2,
                "demand_count": 3,
            },
            "M809R3-09": {
                "outcome": "killed",
                "classification": "boundary creation map can have unbounded fibre absent a uniqueness theorem",
                "max_fibre": max_fibre,
            },
            "M809R3-10": {
                "outcome": "killed",
                "classification": "lossless uncrossing lacks an exchange axiom",
                "shared_owner": "a",
                "shared_carrier": "b",
            }
        },
        "survivor_ids": ["M809R3-01", "M809R3-05", "M809R3-08"],
        "scope": (
            "Only M809R3-07 uses an inherited graph-realizable circuit. Other "
            "probes kill the stated representation-level implication or expose "
            "a missing hypothesis; they are not counterexamples to the public problem."
        ),
        "public_problem_changed": False,
        "main_term_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
