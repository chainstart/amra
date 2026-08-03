#!/usr/bin/env python3
r"""Exact orbit specialization for the Fang--Ma moving-edge certificate on K5.

This is routing evidence only.  It computes C_{M\e} and xi_e exactly after
identifying the six edges incident with an endpoint of e as `a` and the three
edges on the other vertices as `b`.  A one-dimensional diagonal scan may kill
the certificate if it finds xi <= 0 while remaining in a rigorously identified
positive interval of C_{M\e}; otherwise it proves nothing about domination on
the full positivity component.
"""

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

import sympy as sp


VERTICES = range(5)
MARKED = (0, 1)
EDGES = [(i, j) for i in VERTICES for j in VERTICES if i < j and (i, j) != MARKED]


def is_forest(edges):
    parent = list(VERTICES)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def connects_marked(edges):
    adj = {v: [] for v in VERTICES}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = {MARKED[0]}
    stack = [MARKED[0]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return MARKED[1] in seen


def monomial_type(complement):
    incident = sum(1 for u, v in complement if u in MARKED or v in MARKED)
    internal = len(complement) - incident
    return incident, internal


f_counts = Counter()
xi_counts = Counter()
for mask in range(1 << len(EDGES)):
    forest = [EDGES[i] for i in range(len(EDGES)) if mask & (1 << i)]
    if not is_forest(forest):
        continue
    complement = [e for e in EDGES if e not in forest]
    kind = monomial_type(complement)
    f_counts[kind] += 1
    if connects_marked(forest):
        xi_counts[kind] += 1

a, b, t = sp.symbols("a b t", real=True)
f = sp.expand(sum(c * a**i * b**j for (i, j), c in f_counts.items()))
xi = sp.expand(sum(c * a**i * b**j for (i, j), c in xi_counts.items()))
f_diag = sp.Poly(sp.expand(f.subs({a: t, b: t})), t)
xi_diag = sp.Poly(sp.expand(xi.subs({a: t, b: t})), t)

# The distinguished diagonal component is the interval to the right of the
# largest real root of f_diag because f_diag is positive for t > 0.
f_roots = sorted(
    [
        float(sp.re(r))
        for r in sp.nroots(f_diag.sqf_part(), maxsteps=200)
        if abs(float(sp.im(r))) < 1e-10
    ]
)
xi_roots = sorted(
    [
        float(sp.re(r))
        for r in sp.nroots(xi_diag.sqf_part(), maxsteps=200)
        if abs(float(sp.im(r))) < 1e-10
    ]
)
largest_f_root = max(f_roots) if f_roots else None

samples = []
if largest_f_root is not None:
    # Rational samples between the largest f-root and zero rigorously check
    # signs after numerical routing.  They do not establish full component
    # geometry off the diagonal.
    for denominator in (2, 4, 8, 16, 32, 64, 128):
        q = Fraction(-1, denominator)
        fv = int(f_diag.eval(q)) if f_diag.eval(q).q == 1 else str(f_diag.eval(q))
        xv = int(xi_diag.eval(q)) if xi_diag.eval(q).q == 1 else str(xi_diag.eval(q))
        samples.append(
            {
                "t": str(q),
                "f": fv,
                "xi": xv,
                "in_distinguished_diagonal_interval": float(q) > largest_f_root,
            }
        )

result = {
    "host": "K5",
    "marked_edge": list(MARKED),
    "orbit_specialization": {
        "a": "six unmarked edges incident with 0 or 1",
        "b": "three edges induced by vertices 2,3,4",
    },
    "C_delete": str(f),
    "xi": str(xi),
    "C_delete_diagonal": str(f_diag.as_expr()),
    "xi_diagonal": str(xi_diag.as_expr()),
    "C_delete_real_roots_numeric": f_roots,
    "xi_real_roots_numeric": xi_roots,
    "distinguished_diagonal_interval": f"t > {largest_f_root}",
    "rational_sign_samples": samples,
    "interpretation": "A negative xi sample only matters when in_distinguished_diagonal_interval is true. The listed negative-t samples are outside t>0 and are neither certificates nor kill evidence; absence of a valid sample is only routing evidence.",
}

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
