#!/usr/bin/env python3
"""Independent finite guards for the q=1 derivative and K4 channel.

Uses only integer dictionaries and a disjoint-set forest test. The universal
q=1 sign rests on the natural supermodularity proof, not this enumeration.
"""

from itertools import combinations
import json


def nullity(vertex_count, edges, selected):
    parent = list(range(vertex_count))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rank = 0
    for index in selected:
        x, y = edges[index]
        x, y = find(x), find(y)
        if x != y:
            parent[x] = y
            rank += 1
    return len(selected) - rank


def q1_check(vertex_count):
    edges = list(combinations(range(vertex_count), 2))
    pairs = 0
    bases = 0
    positive = 0
    for e, f in combinations(range(len(edges)), 2):
        remaining = [i for i in range(len(edges)) if i not in (e, f)]
        derivative_sums = [[0, 0], [0, 0]]
        defect_sum = 0
        for mask in range(1 << len(remaining)):
            base = {remaining[j] for j in range(len(remaining)) if mask & (1 << j)}
            values = {}
            for i in range(2):
                for j in range(2):
                    selected = base | ({e} if i else set()) | ({f} if j else set())
                    values[i, j] = nullity(vertex_count, edges, selected)
                    derivative_sums[i][j] += values[i, j]
            defect = values[1, 1] + values[0, 0] - values[1, 0] - values[0, 1]
            assert defect in (0, 1)
            defect_sum += defect
            bases += 1
        s = 1 << len(remaining)
        minus_derivative = -s * (
            derivative_sums[1][0] + derivative_sums[0][1]
            - derivative_sums[1][1] - derivative_sums[0][0]
        )
        assert minus_derivative == s * defect_sum >= 0
        positive += defect_sum
        pairs += 1
    return {"marked_pairs": pairs, "base_subsets": bases, "summed_defect": positive}


def add(left, right, sign=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + sign * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left, right):
    result = {}
    for x, a in left.items():
        for y, b in right.items():
            monomial = tuple(i + j for i, j in zip(x, y))
            result[monomial] = result.get(monomial, 0) + a * b
    return {m: c for m, c in result.items() if c}


def k4_cells():
    edges = [(0, 1), (2, 3), (0, 2), (0, 3), (1, 2), (1, 3)]
    e, f = 0, 1
    remaining = [2, 3, 4, 5]
    cells = [[{}, {}], [{}, {}]]
    for mask in range(16):
        base = {remaining[j] for j in range(4) if mask & (1 << j)}
        monomial = tuple(1 if mask & (1 << j) else 0 for j in range(4))
        for i in range(2):
            for j in range(2):
                selected = base | ({e} if i else set()) | ({f} if j else set())
                if nullity(4, edges, selected) == 0:
                    cells[i][j][monomial] = 1
    return cells


def k4_check():
    cells = k4_cells()
    rayleigh = add(multiply(cells[1][0], cells[0][1]), multiply(cells[1][1], cells[0][0]), -1)
    expected = {
        (2, 0, 0, 2): 1,
        (2, 0, 0, 1): 1,
        (1, 1, 1, 1): -2,
        (1, 0, 0, 2): 1,
        (1, 0, 0, 1): 1,
        (0, 2, 2, 0): 1,
        (0, 2, 1, 0): 1,
        (0, 1, 2, 0): 1,
        (0, 1, 1, 0): 1,
    }
    assert rayleigh == expected
    ad = {(1, 0, 0, 1): 1}
    bc = {(0, 1, 1, 0): 1}
    square = multiply(add(ad, bc, -1), add(ad, bc, -1))
    a_plus_d_plus_one = {(1, 0, 0, 0): 1, (0, 0, 0, 1): 1, (0, 0, 0, 0): 1}
    b_plus_c_plus_one = {(0, 1, 0, 0): 1, (0, 0, 1, 0): 1, (0, 0, 0, 0): 1}
    decomposition = add(add(square, multiply(ad, a_plus_d_plus_one)), multiply(bc, b_plus_c_plus_one))
    assert decomposition == rayleigh
    return {
        "cell_monomial_counts": [[len(cells[i][j]) for j in range(2)] for i in range(2)],
        "rayleigh_terms": len(rayleigh),
        "negative_abcd_coefficient": rayleigh[(1, 1, 1, 1)],
        "complete_channel_decomposition": True,
    }


def main():
    print(json.dumps({
        "q1": {f"K{n}": q1_check(n) for n in range(3, 6)},
        "k4_disjoint": k4_check(),
        "pass": True,
        "scope": "finite guard only"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
