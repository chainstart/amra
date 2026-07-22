#!/usr/bin/env python3
"""Exact certificate for the hard-chamber rational-cone barrier in #325."""

from __future__ import annotations

import json

import sympy as sp


T = sp.symbols("T", integer=True, positive=True)
x1, x2, y1, y2 = 158*T + 1, 59*T, 134*T, 133*T
u = sp.expand(x1 + x2 - y1 - y2)
h = sp.expand((x1 - x2) - (y1 - y2))
k = sp.expand((x1 - x2) + (y1 - y2))
w = sp.expand(x1 + x2 + y1 + y2)
v = sp.expand(x1**2 + x2**2 - y1**2 - y2**2)
s = sp.expand(x1**4 + x2**4 - y1**4 - y2**4)

assert 158**4 + 59**4 == 134**4 + 133**4
assert u == 1 - 50*T
assert h == 1 + 98*T
assert v == 1 + 316*T - 7200*T**2
assert s == 1 + 632*T + 149784*T**2 + 15777248*T**3
assert sp.expand(2*v - (h*k + u*w)) == 0

# At the exact homogeneous ray (without the +1 perturbation), the round-7
# hard-fibre coordinates are U=50T, a=48T, p=50T, d=336T, z=7200T^2.
U, a, p, d, z = 50*T, 48*T, 50*T, 336*T, 7200*T**2
assert sp.expand(2*z - (U*d - a*p)) == 0
assert sp.expand(d - 2*U - 236*T) == 0

payload = {
    "schema": "amra.erdos325.round8.quartic_cone_barrier.v1",
    "equal_biquadrate_identity": "158^4+59^4=134^4+133^4",
    "homogeneous_hard_ray": {
        "u": "-50*T",
        "h": "98*T",
        "v": "-7200*T^2",
        "s": "0",
        "U": str(U),
        "a": str(a),
        "p": str(p),
        "d": str(d),
        "z": str(z),
        "fibre_identity": "2*z=U*d-a*p",
    },
    "one_coordinate_perturbation": {
        "tuple": [str(x1), str(x2), str(y1), str(y2)],
        "u": str(u),
        "h": str(h),
        "v": str(v),
        "s": str(s),
        "asymptotic_scales": "|s|~15777248*T^3, |u|~50*T, |v|~7200*T^2",
    },
    "rigorous_scope": (
        "This disproves any uniform coercive hard-chamber estimate "
        "|u|=O(|s|^(1/4)) or |v|=O(|s|^(1/2)); it does not disprove an "
        "average image/fibre estimate."
    ),
    "result": "PASS",
}

print(json.dumps(payload, indent=2, sort_keys=True))
