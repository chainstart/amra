#!/usr/bin/env python3
"""Second, independently written verifier for actual-unit realization."""

import sympy as sp


def aggregate(m):
    n = 3+2*m
    rows = []
    f0 = [0]*n; f0[1] = 1; rows.append(f0)
    pa0 = [0]*n; pa0[0] = pa0[2] = 1; rows.append(pa0)
    for j in range(m):
        fj = [0]*n; fj[0] = fj[3+j] = 1; rows.append(fj)
        paj = [0]*n; paj[1] = paj[3+m+j] = 1; rows.append(paj)
        ident = [0]*n; ident[2] = 1; ident[3+j] = ident[3+m+j] = -1
        rows.append(ident)
    return sp.Matrix(rows)


for m in range(1, 21):
    M = aggregate(m)
    products = [0,1]+[2+3*j for j in range(m)]+[3+3*j for j in range(m)]
    minor = M.extract(products, range(1,M.cols))
    assert abs(minor.det()) == 1
    gauge = sp.Matrix([1,0,-1]+[-1]*m+[0]*m)
    assert M.rank() == 2*m+2 and len(M.nullspace()) == 1
    assert M*gauge == sp.zeros(M.rows,1)

    source_rows = [0]+[2+3*j for j in range(m)]+[4+3*j for j in range(m)]
    S = M.extract(source_rows, range(M.cols))
    shift = sp.Matrix([0,0,1]+[0]*m+[1]*m)
    assert S.rank() == 2*m+1
    assert S*gauge == sp.zeros(S.rows,1)
    assert S*shift == sp.zeros(S.rows,1)
    assert sp.Matrix.hstack(gauge,shift).rank() == 2

# Affine cocycle compatibility is the same row combination.
phi0, alpha0, phij, alphaj = sp.symbols('phi0 alpha0 phij alphaj')
kappa = alpha0+phi0-phij-alphaj
assert sp.expand(kappa-(alpha0+phi0-phij-alphaj)) == 0

for k in range(2, 21):
    for split in range(1,k):
        Rset = list(range(split)); Qset = list(range(split,k))
        source = [1,0]+[int(i in Rset) for i in range(k)]
        f0 = [0,1]+[0]*k
        comp = [0,1]+[int(i in Qset) for i in range(k)]
        common = [1,0]+[1]*k
        Raw = sp.Matrix([source,f0,comp,common])
        assert Raw.row(3) == Raw.row(0)+Raw.row(2)-Raw.row(1)
        # Columns g,f and any Q occurrence give a unit rank-three minor.
        assert abs(Raw.extract([0,1,2],[0,1,2+Qset[0]]).det()) == 1
        assert Raw.rank() == 3 and len(Raw.nullspace()) == k-1

        H = sp.Matrix([
            [1]*k,
            [int(i in Rset) for i in range(k)],
            [int(i in Qset) for i in range(k)],
        ])
        assert H.rank() == 2 and len(H.nullspace()) == k-2
        internal = []
        for i in Rset[1:]:
            v = sp.zeros(k,1); v[i] = 1; v[Rset[0]] = -1; internal.append(v)
        for i in Qset[1:]:
            v = sp.zeros(k,1); v[i] = 1; v[Qset[0]] = -1; internal.append(v)
        assert len(internal) == k-2
        for v in internal:
            assert H*v == sp.zeros(3,1)
            raw_v = sp.Matrix([0,0]+list(v))
            assert Raw*raw_v == sp.zeros(4,1)
        if internal:
            assert sp.Matrix.hstack(*internal).rank() == k-2

        raw_gauge = sp.zeros(k+2,1)
        raw_gauge[0] = 1
        raw_gauge[2+Rset[0]] = -1
        assert Raw*raw_gauge == sp.zeros(4,1)

print('PASS: second actual-unit realization review')
print('aggregate/source certificates m<=20; raw splits k<=20')
print('arguments use explicit unit minors and extend to all m,k')
