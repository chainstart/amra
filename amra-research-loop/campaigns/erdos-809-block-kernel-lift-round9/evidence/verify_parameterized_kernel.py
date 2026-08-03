#!/usr/bin/env python3
"""Exact finite-support verification for the parameterized kernel theorem.

Completeness reduction: a bad C7 contains the four endpoints of one named
repeated-colour pair and only three further vertices.  After fixing indices
1,2 and (when needed) the generic colour index, relabelling therefore uses
at most indices 1,...,6 and at most three R vertices.  The grid below is thus
a complete orbit-support check for all m>=3,r>=0, not a size extrapolation.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = spec_from_file_location("parameter_probe", HERE / "parameter_probe.py")
probe = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(probe)

checked = 0
for m in range(3, 7):
    for r in range(4):
        result = probe.instance(m, r)
        assert result["formula_minus_singleton"] == []
        assert result["singleton_minus_formula"] == []
        assert result["formula_hits_all"]
        assert result["singleton_hits_all"]
        assert set(result["trace_sizes"]) <= {1, 3}
        expected = r * (m + 2) + (m - 2) * (m + 5) // 2
        assert result["formula_count"] == expected
        assert result["singleton_count"] == expected
        checked += 1

# Three explicit protected-cycle branches.  The altered omission sets merely
# keep the displayed edge count; the natural proofs use only the seven named
# edges and hence work for every m>=3 and r>=0.
e = probe.edge
branches = {
    "uw_present": {e("b", "u"), e("b", "w"), e("w", "x3")},
    "bw_present": {e("b", "u"), e("u", "w"), e("w", "x3")},
    "bu_present": {e("b", "w"), e("u", "w"), e("u", "x3")},
}
for omitted in branches.values():
    result = probe.instance(3, 0, omitted)
    assert result["protected_witness"] is not None
    assert 0 in result["trace_sizes"]

print(
    "parameterized block kernel: PASS; "
    f"support representatives={checked}; protected branches={len(branches)}"
)
