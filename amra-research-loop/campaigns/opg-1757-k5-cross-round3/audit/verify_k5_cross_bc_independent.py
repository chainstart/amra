#!/usr/bin/env python3
"""Independent graph-definition reconstruction; imports no author checker."""
import itertools
import sympy as sp

vertices = tuple(range(5))
marked = (0, 3)
missing = (3, 4)
edges = [uv for uv in itertools.combinations(vertices, 2)
         if uv not in {marked, missing}]
a, b, c, d, e = sp.symbols("a b c d e")
weight = {(0,1):a, (0,2):a, (0,4):b, (1,2):c,
          (1,3):d, (2,3):d, (1,4):e, (2,4):e}

def components(selected):
    parent = list(vertices)
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u, v in selected:
        ru, rv = root(u), root(v)
        if ru == rv:
            return None
        parent[ru] = rv
    return root

P = sp.Integer(0)
xi = sp.Integer(0)
forest_count = connected_count = 0
for mask in range(1 << len(edges)):
    selected = {edges[i] for i in range(len(edges)) if (mask >> i) & 1}
    root = components(selected)
    if root is None:
        continue
    forest_count += 1
    complement_weight = sp.prod(weight[uv] for uv in edges if uv not in selected)
    P += complement_weight
    if root(marked[0]) == root(marked[1]):
        connected_count += 1
        xi += complement_weight

assert (forest_count, connected_count) == (128, 58)
slice_sub = {a:1, d:1, e:1}
assert sp.expand(P.subs(slice_sub)) == 54*b*c + 27*b + 32*c + 15
assert sp.expand(xi.subs(slice_sub)) == 22*b*c + 12*b + 16*c + 8
x, y = sp.symbols("x y", real=True)
affine = {b:(x-32)/54, c:y-sp.Rational(1,2)}
assert sp.factor(P.subs(slice_sub).subs(affine)) == x*y - 1
assert sp.factor(54*xi.subs(slice_sub).subs(affine)) == 22*x*y+x+160*y-32
assert sp.factor(x+160/x-10 - ((x-5)**2/x+135/x)) == 0
print("independent K5-e cross (b,c) reconstruction: PASS")
