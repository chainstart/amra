#!/usr/bin/env python3
import json
import sympy as s

e, b = s.symbols("e b", real=True)
A = 24*e**2 + 48*e + 9
C = 24*e**2 + 20*e + 3
D = 5*e**2 + 10*e + 2
E = 5*e**2 + 6*e + 1
P = s.expand(b*A + C)
xi2 = s.expand(b*D + E)
Q = s.expand(E*A - D*C)
alpha = -1 + s.sqrt(10)/4

checks = {
    "determinant_identity": s.expand(A*xi2 - D*P - Q) == 0,
    "Q_exact": Q == 44*e**3 + 94*e**2 + 32*e + 3,
    "A_discriminant": s.discriminant(A, e) == 1440,
    "C_at_alpha": s.simplify(C.subs(e, alpha)) == 22 - 7*s.sqrt(10),
    "Q_discriminant": s.discriminant(Q, e) == -9552,
    "Q_at_alpha": s.simplify(Q.subs(e, alpha)) == (-22 + 7*s.sqrt(10))/8,
    "anchor_P": P.subs({b:1,e:1}) == 128,
    "anchor_xi": 2*xi2.subs({b:1,e:1}) == 58,
    "Q_negative_comparator": Q.subs(e,-2) == -37,
}
assert all(checks.values()), checks
out = {
    "status":"PASS",
    "checks":checks,
    "A_roots":[str(x) for x in s.solve(A,e)],
    "D_roots":[str(x) for x in s.solve(D,e)],
    "Q_numeric_roots":[str(x) for x in s.nroots(Q)],
    "scope":"a=c=d=1, free real (b,e), complete anchor component only"
}
print(json.dumps(out, indent=2))
