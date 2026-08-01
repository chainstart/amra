# OPG-1757 six-hour attack

The principal result is
`UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md`.  It replaces the previous
conditional uniform-height ledger by a complete all-profile proof and
upgrades the simultaneous growing-deficit window to every fixed positive
constant strictly below \(1/3\).

`CLAIM_LEDGER.md` separates proved, open, and out-of-scope statements.
`verify_uniform_height_envelope.py` is a reproducible regression
certificate; finite checks in that script are not used as substitutes
for the all-parameter inequalities in the theorem.

POLYNOMIAL_GROWING_DEFICIT_WINDOW.md is the bold continuation: it
combines the uniform endpoint height with the inherited all-order
filtered-ring lemma in a candidate proof of a deliberately coarse
power-width window.
It remains marked pending independent cross-audit until the final
campaign red-team block.

`QUANTIFIER_CHAIN_SELF_AUDIT.md` checks the integer endpoints,
strictness, normalization, root threshold, and window implication line
by line.  `POLYNOMIAL_WINDOW_BLIND_AUDIT_MAP.md` is the compact
dependency map for a different agent's independent reconstruction.

`BASE4_NEWTON_GLOBAL_ATTACK.md` records a higher-risk route toward full
base-four Newton positivity, including an exact profile EGF and the
precise global sign-convolution barrier.  Its companion probe is finite
evidence only and is not part of the polynomial-window proof.
`verify_second_active_newton_probe.py` separately checks the next active
order through \(q=31\).  The same file now contains a static certificate
for an exact odd-parity recurrence proof candidate; that candidate remains
pending independent audit, while the even-parity scan is finite evidence.
`SECOND_ACTIVE_NEWTON_RECURRENCE_ATTACK.md` isolates the two homogenized
transport recurrences.  Its odd recurrence is reduced to a fixed positive
kernel plus four explicit top coefficients; its even recurrence remains
conjectural.

Run its ordinary and extended falsification certificates with

    PYTHONDONTWRITEBYTECODE=1 python3 verify_polynomial_window_bounds.py
    PYTHONDONTWRITEBYTECODE=1 python3 \
      verify_polynomial_window_bounds.py --extended-endpoints
