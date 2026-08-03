#!/usr/bin/env python3
"""Exact first proof attempts for M809C-05, M809C-08 and M809C-11."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


def phi(n, e):
    return sp.Rational(e, 2) + sp.Rational(n, 2) * sp.sqrt(
        sp.Rational(e) - sp.Rational(n * n, 4)
    )


def max_matching(left, neighbourhoods):
    owner = {}

    def augment(u, seen):
        for v in neighbourhoods[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in owner or augment(owner[v], seen):
                owner[v] = u
                return True
        return False

    return sum(augment(u, set()) for u in left)


def hall_deficiency(left, neighbourhoods):
    worst = 0
    witnesses = []
    for size in range(len(left) + 1):
        for subset in combinations(left, size):
            neighbours = set().union(*(neighbourhoods[u] for u in subset)) if subset else set()
            deficit = len(subset) - len(neighbours)
            if deficit > worst:
                worst = deficit
                witnesses = [subset]
            elif deficit == worst and deficit > 0:
                witnesses.append(subset)
    return worst, witnesses


# M809C-05: at the exact threshold e=floor(n^2/4)+1 and odd n,
# e-n^2/4=3/4.  Therefore Phi=e/2+n*sqrt(3)/4 and S_m is irrational
# for every integer |B|.  It cannot be the cardinality of an unweighted set.
odd_rows = []
for n in range(5, 20, 2):
    e = n * n // 4 + 1
    value_phi = sp.simplify(phi(n, e))
    assert sp.simplify(sp.Rational(e) - sp.Rational(n*n, 4) - sp.Rational(3, 4)) == 0
    for b_size in range(n + 1):
        slack = sp.simplify(e - sp.binomial(b_size, 2) - value_phi)
        assert slack.is_rational is False
    odd_rows.append({
        "n": n,
        "e": e,
        "Phi": str(value_phi),
        "S_m_form": f"integer - ({str(value_phi)})",
        "unweighted_cardinality_possible": False,
    })

# The inherited n=14 tight/paid pair is an integrality-compatible warning,
# not the irrationality witness: Phi=32 and S_m=15 when |B|=3.
n14_phi = sp.simplify(phi(14, 50))
n14_slack = sp.simplify(50 - sp.binomial(3, 2) - n14_phi)
assert n14_phi == 32
assert n14_slack == 15

# M809C-08: exact ledger insufficiency.  The mixed high anchors themselves
# give I_mix distinct compatible colours, but R_A>S_m does not force either
# I_mix or the internal-low channel to reach Phi.  The n=14 numerical scale
# admits the following exact integer ledger profile.
outer_profile = {
    "Phi": 32,
    "S_m": 15,
    "e_internal_low": 8,
    "I_mix": 8,
    "N_int": 0,
}
outer_profile["R_A"] = (
    outer_profile["e_internal_low"]
    + outer_profile["I_mix"]
    - outer_profile["N_int"]
)
assert outer_profile["R_A"] > outer_profile["S_m"]
assert outer_profile["e_internal_low"] < outer_profile["Phi"]
assert outer_profile["I_mix"] < outer_profile["Phi"]

# M809C-11: exact typed Hall boundary.  Three demands and two actual B atoms
# have Hall deficiency one even if arbitrary A-owner counts are large.  One
# genuinely new slack carrier with an explicit owner edge removes the deficit.
demands = ("c1", "c2", "c3")
tight_neighbourhoods = {u: frozenset(("bc", "cz")) for u in demands}
tight_deficiency, tight_witnesses = hall_deficiency(demands, tight_neighbourhoods)
assert tight_deficiency == 1
assert max_matching(demands, tight_neighbourhoods) == 2

paid_neighbourhoods = dict(tight_neighbourhoods)
paid_neighbourhoods["c3"] = frozenset(("bc", "cz", "s1"))
paid_deficiency, paid_witnesses = hall_deficiency(demands, paid_neighbourhoods)
assert paid_deficiency == 0
assert max_matching(demands, paid_neighbourhoods) == 3

result = {
    "schema": "amra.erdos809.conversion-round2.survivor-first-attempts.v1",
    "M809C-05": {
        "outcome": "refuted_in_exact_unweighted_cardinality_form",
        "all_parameter_argument": (
            "For odd n and e=floor(n^2/4)+1, e-n^2/4=3/4, so "
            "Phi=e/2+n*sqrt(3)/4 and S_m=e-C(|B|,2)-Phi is irrational. "
            "No finite unweighted set can have cardinality S_m."
        ),
        "finite_guard": odd_rows,
        "n14_pair": {"Phi": 32, "S_m": 15, "role": "carrier-provenance warning only"},
        "repair": "weighted nonnegative atoms with total mass S_m, or an integer floor/ceiling ledger with an exact error term"
    },
    "M809C-08": {
        "outcome": "conditional_survivor",
        "proved_channel": (
            "The I_mix unique high internal anchors are injective by colour "
            "and pairwise C7-compatible; I_mix>=ceil(Phi) closes directly."
        ),
        "exact_remaining_identity": "R_A=e(G[A_<q*])+I_mix-N_int",
        "ledger_counterprofile": outer_profile,
        "scope": (
            "The profile proves only that the identity and thresholds do not "
            "imply the direct exit.  It is not asserted graph-realizable."
        ),
        "missing_lemma": (
            "A cross-channel compatibility theorem combining internal-low "
            "edges and mixed-high anchors, or a direct graph proof R_A<=S_m."
        )
    },
    "M809C-11": {
        "outcome": "proved_conditional_bookkeeping",
        "theorem": (
            "For an explicitly given typed carrier universe and legal "
            "neighbourhoods, all demands can be paid iff every demand subset "
            "has at least as many distinct legal carriers; maximum unpaid "
            "demand equals max_T(|T|-|N(T)|)."
        ),
        "tight_instance": {
            "matching_rank": 2,
            "hall_deficiency": tight_deficiency,
            "deficient_sets": [list(x) for x in tight_witnesses],
            "A_owner_count_is_irrelevant_without_arcs": 3,
        },
        "after_one_owned_slack_arc": {
            "matching_rank": 3,
            "hall_deficiency": paid_deficiency,
            "deficient_sets": [list(x) for x in paid_witnesses],
        },
        "boundary": "Hall proves allocation after carriers and arcs exist; it creates neither."
    },
    "global_result": (
        "M809C-05 requires repair to weighted atoms; M809C-08 retains the "
        "only graph-specific direct exit; M809C-11 is an exact conditional "
        "host whose missing inputs are precisely the conversion/slack maps."
    ),
    "public_problem_changed": False,
    "main_term_changed": False,
}

output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
