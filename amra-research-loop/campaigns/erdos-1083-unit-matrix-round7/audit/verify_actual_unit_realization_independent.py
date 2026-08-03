#!/usr/bin/env python3
"""Independent exact audit of actual aggregate and raw unit matrices."""
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

def aggregate(m):
    # columns g,f,b,r_1..r_m,q_1..q_m
    n = 3 + 2*m
    rows = []
    f0 = [0]*n; f0[1] = 1; rows.append(f0)
    pa0 = [0]*n; pa0[0] = pa0[2] = 1; rows.append(pa0)
    for j in range(m):
        fj = [0]*n; fj[0] = fj[3+j] = 1; rows.append(fj)
        paj = [0]*n; paj[1] = paj[3+m+j] = 1; rows.append(paj)
        ident = [0]*n; ident[2] = 1; ident[3+j] = ident[3+m+j] = -1
        rows.append(ident)
        assert s.Matrix([pa0, f0, fj, paj]).T * s.Matrix([1,1,-1,-1]) == s.Matrix(ident)
    return s.Matrix(rows)

for m in range(1, 13):
    M = aggregate(m)
    r = 2*m + 2
    assert M.rank() == r and M.cols-r == 1
    # Explicit triangular maximal minor: retain F0, PA0 and all Fj, PAj
    # rows, and delete the g column.  This avoids a combinatorial minor scan.
    product_rows = [0,1] + [2+3*j for j in range(m)] + [3+3*j for j in range(m)]
    product_minor = M.extract(product_rows, range(1, M.cols))
    assert abs(product_minor.det()) == 1
    gauge = s.Matrix([1,0,-1] + [-1]*m + [0]*m)
    assert M*gauge == s.zeros(M.rows,1)
    S = smith_normal_form(M, domain=ZZ)
    assert all(abs(S[i,i]) == 1 for i in range(r))

    # Retain F0, every Fj, and every identity row only.
    keep = [0] + [2+3*j for j in range(m)] + [4+3*j for j in range(m)]
    Ms = M.extract(keep, range(M.cols))
    assert Ms.rank() == 2*m+1 and M.cols-Ms.rank() == 2
    shift = s.Matrix([0,0,1] + [0]*m + [1]*m)
    assert Ms*shift == s.zeros(Ms.rows,1)
    assert M*shift != s.zeros(M.rows,1)

for k in range(2, 11):
    for split in range(1, k):
        source = [1,0] + [int(i < split) for i in range(k)]
        f0 = [0,1] + [0]*k
        comp = [0,1] + [int(i >= split) for i in range(k)]
        common = [1,0] + [1]*k
        R = s.Matrix([source,f0,comp,common])
        assert R.rank() == 3 and len(R.nullspace()) == k-1
        # Projection h -> (sum_all,sum_R,sum_Q) has rank two and kernel k-2.
        H = s.Matrix([[1]*k,
                      [int(i < split) for i in range(k)],
                      [int(i >= split) for i in range(k)]])
        assert H.rank() == 2 and len(H.nullspace()) == k-2

print("actual aggregate unit realization independent audit: PASS")
