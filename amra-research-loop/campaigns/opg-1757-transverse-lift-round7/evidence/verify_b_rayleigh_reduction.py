#!/usr/bin/env python3
"""Exact b=w04 Rayleigh reduction for OPG-1757 round 7 (stdlib only)."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json

from verify_c_zero_fibre import (
    EDGES,
    EDGE_INDEX,
    VERTICES,
    ZERO8,
    add,
    canonical,
    derivative,
    is_forest,
    multiply,
    original_variable,
    pair_polynomial,
    reconstruct_original,
    restrict_original_zero,
)


def one_plus(edge):
    return add({ZERO8: 1}, original_variable(edge))


def power(poly, exponent):
    result = {ZERO8: 1}
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def term_count(poly):
    return len(poly)


def total_degree(poly):
    return max(map(sum, poly)) if poly else -1


def terminal_partition(chosen, terminals=(0, 3, 4)):
    """Return the connectivity partition induced on the three terminals."""
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in chosen:
        adjacency[left].append(right)
        adjacency[right].append(left)

    labels = []
    for terminal in terminals:
        stack, seen = [terminal], {terminal}
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        labels.append(frozenset(seen.intersection(terminals)))

    if all(label == frozenset({terminal}) for label, terminal in zip(labels, terminals)):
        return "t"
    if labels[0] == labels[1] == frozenset({0, 3}) and labels[2] == frozenset({4}):
        return "x03"
    if labels[0] == labels[2] == frozenset({0, 4}) and labels[1] == frozenset({3}):
        return "y04"
    if labels[1] == labels[2] == frozenset({3, 4}) and labels[0] == frozenset({0}):
        return "z34"
    if all(label == frozenset(terminals) for label in labels):
        return "u"
    raise AssertionError((chosen, labels))


def reconstruct_terminal_states(excluded_edges):
    """Enumerate complement polynomials by the {0,3,4} forest partition."""
    active_edges = tuple(edge for edge in EDGES if edge not in excluded_edges)
    states = {name: {} for name in ("t", "x03", "y04", "z34", "u")}
    forest_count = 0
    for size in range(len(active_edges) + 1):
        for chosen in combinations(active_edges, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            chosen_set = set(chosen)
            exponent = tuple(
                int(edge in active_edges and edge not in chosen_set)
                for edge in EDGES
            )
            state = terminal_partition(chosen)
            states[state][exponent] = states[state].get(exponent, 0) + 1
    return states, forest_count


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)

    b_edge = (0, 4)
    c_edge = (1, 2)
    x01_edge, x02_edge = (0, 1), (0, 2)
    x13_edge, x23_edge = (1, 3), (2, 3)
    x14_edge, x24_edge = (1, 4), (2, 4)

    # P=A*b+C and xi=D*b+E in the original edge coordinate b=w04.
    a_slope = derivative(deletion, (b_edge,))
    c_zero = restrict_original_zero(deletion, b_edge)
    d_slope = derivative(connectivity, (b_edge,))
    e_zero = restrict_original_zero(connectivity, b_edge)
    delta = add(multiply(a_slope, e_zero), multiply(d_slope, c_zero), -1)
    assert (term_count(a_slope), term_count(c_zero), term_count(d_slope), term_count(e_zero)) == (
        81,
        47,
        34,
        24,
    )
    assert term_count(delta) == 178 and total_degree(delta) == 12
    assert all(coefficient > 0 for coefficient in delta.values())

    # The graph with b deleted is a four-branch two-terminal book.  If q0,
    # q3,q4 are the three length-two path disconnected-state polynomials,
    # its cospanning polynomial A has a four-term state-sum compression.
    q0 = pair_polynomial(x01_edge, x02_edge)
    q3 = pair_polynomial(x13_edge, x23_edge)
    q4 = pair_polynomial(x14_edge, x24_edge)
    c = original_variable(c_edge)
    expected_a = add(
        multiply(multiply(q0, q3), q4),
        multiply(
            c,
            add(
                add(multiply(q0, q3), multiply(q0, q4)),
                add(multiply(q3, q4), multiply(multiply(q0, q3), q4)),
            ),
        ),
    )
    assert a_slope == expected_a

    # Refine the two marked pages by their one-hub attachment states.  This
    # compresses the 34-term D polynomial without a symbolic factorizer.
    x01, x02 = original_variable(x01_edge), original_variable(x02_edge)
    x13, x23 = original_variable(x13_edge), original_variable(x23_edge)
    p_sum = add(x01, x02)
    r_sum = add(x13, x23)
    aligned = add(multiply(x01, x13), multiply(x02, x23))
    expected_d = add(
        multiply(
            multiply(c, q4),
            add(add(p_sum, r_sum), aligned),
        ),
        multiply(add(c, q4), multiply(p_sum, r_sum)),
    )
    assert d_slope == expected_d

    # A second, graph-native compression classifies every forest after
    # deleting h=03 and b=04 by the connectivity partition it induces on
    # terminals {0,3,4}.  This does not trust the formulas for A,C,D,E.
    states, state_forest_count = reconstruct_terminal_states({b_edge})
    t = states["t"]
    x = states["x03"]
    y = states["y04"]
    z = states["z34"]
    u = states["u"]
    assert state_forest_count == 81
    assert tuple(map(term_count, (t, x, y, z, u))) == (23, 12, 12, 12, 22)
    assert a_slope == add(add(add(add(t, x), y), z), u)
    assert add(a_slope, d_slope, -1) == add(add(t, y), z)
    assert c_zero == add(add(t, x), z)
    assert add(c_zero, e_zero, -1) == t
    partition_delta = add(
        multiply(add(x, z), add(y, z)),
        multiply(t, add(z, u, -1)),
    )
    assert delta == partition_delta

    # Three exact coordinate-wall factorizations of the seven-variable
    # Rayleigh determinant.
    x01_square = power(x01, 2)
    x02_square = power(x02, 2)
    x13_square = power(x13, 2)
    x23_square = power(x23, 2)
    x14, x24 = original_variable(x14_edge), original_variable(x24_edge)
    x14_square = power(x14, 2)
    x24_square = power(x24, 2)
    c_square = power(c, 2)

    expected_c_wall = multiply(
        multiply(
            multiply(x01_square, x02_square),
            multiply(add(x13, x23), add(x14, x24)),
        ),
        multiply(q3, q4),
    )
    delta_c_wall = restrict_original_zero(delta, c_edge)
    assert delta_c_wall == expected_c_wall

    expected_x01_wall = multiply(
        multiply(
            multiply(c_square, x02_square),
            multiply(x13_square, x14_square),
        ),
        multiply(one_plus(x23_edge), one_plus(x24_edge)),
    )
    delta_x01_wall = restrict_original_zero(delta, x01_edge)
    assert delta_x01_wall == expected_x01_wall

    expected_x02_wall = multiply(
        multiply(
            multiply(c_square, x01_square),
            multiply(x23_square, x24_square),
        ),
        multiply(one_plus(x13_edge), one_plus(x14_edge)),
    )
    delta_x02_wall = restrict_original_zero(delta, x02_edge)
    assert delta_x02_wall == expected_x02_wall

    records = {
        "A": a_slope,
        "C": c_zero,
        "D": d_slope,
        "E": e_zero,
        "Delta_b": delta,
        "Delta_b_at_c_zero": delta_c_wall,
        "Delta_b_at_x01_zero": delta_x01_wall,
        "Delta_b_at_x02_zero": delta_x02_wall,
        "partition_t": t,
        "partition_x03": x,
        "partition_y04": y,
        "partition_z34": z,
        "partition_u": u,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.b-rayleigh-reduction.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
        },
        "b_fibre": {
            "P": "A*b+C",
            "xi": "D*b+E",
            "Delta_b": "A*E-D*C",
            "term_counts": {"A": 81, "C": 47, "D": 34, "E": 24, "Delta_b": 178},
            "Delta_b_total_degree": 12,
            "Delta_b_original_coefficients_strictly_positive": True,
        },
        "book_compression": {
            "A": "q0*q3*q4+c*(q0*q3+q0*q4+q3*q4+q0*q3*q4)",
            "D": "c*q4*(p_sum+r_sum+aligned)+(c+q4)*p_sum*r_sum",
        },
        "three_terminal_partition": {
            "term_counts": {"t": 23, "x03": 12, "y04": 12, "z34": 12, "u": 22},
            "A": "t+x03+y04+z34+u",
            "A-D": "t+y04+z34",
            "C": "t+x03+z34",
            "C-E": "t",
            "Delta_b": "(x03+z34)*(y04+z34)+t*(z34-u)",
        },
        "coordinate_walls": {
            "c=0": "x01^2*x02^2*(x13+x23)*(x14+x24)*q3*q4",
            "x01=0": "c^2*x02^2*x13^2*x14^2*(1+x23)*(1+x24)",
            "x02=0": "c^2*x01^2*x23^2*x24^2*(1+x13)*(1+x14)",
        },
        "records": {
            name: {
                "terms": term_count(poly),
                "total_degree": total_degree(poly),
                "sha256": digest(poly),
            }
            for name, poly in records.items()
        },
        "scope": "exact b-fibre and coordinate-wall ledger; global Delta_b sign remains open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
