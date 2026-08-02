# OPG-1757 baseline freeze

Freeze time: 2026-08-02 10:39 HKT.

## Source digests

```text
043b2f27a49e22386c8b8ab2a42e9a111502da3a0c6caf856b2a2fb340a5368f  UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md
e1a9affd05fbd24659a7775826109f697c37ba1796aa07ae4f91cfc3403336af  POLYNOMIAL_GROWING_DEFICIT_WINDOW.md
2594afa7ff25bba6b55537aa4394cc4e0a71a044445e2b53afda5c53e6b618ec  POLYNOMIAL_WINDOW_RED_TEAM.md
9aa6c5bbed178e1c39a55637c3fde003ed3d1e861d4aa40d5062cbc1028623db  verify_polynomial_window_bounds.py
5ba459bbd3bfc6ea3d1bdec9f5de783f25baaeb9733d4d7c6ca2a371d5c1faff  verify_uniform_height_envelope.py
7a3611e29b557a2b45abee30a6816261f016ff7ea9a77736c55ec050fff4dcfa  verify_base4_newton_probe.py
25baa4eeb5a46a4048c7bc6f1e5eea43d936686ff50cfa04dfc5a6c8e78c644c  verify_second_active_newton_probe.py
```

Paths are relative to
`q1_six_hour_campaign_2026-07-31/opg1757/`.

## Replayed evidence

```text
9 passed

OPG POLYNOMIAL WINDOW BOUNDS CERTIFICATE: PASS
exact_profile_coefficients: 99
newton_reconstructions: 1001
constant_chain_values: 7440
falling_coefficients: 881548
window_exponent: 67
exact_q6_endpoint_losses: 1008
exact_q6_layer_losses: 156

OPG BASE-FOUR NEWTON PROBE: PASS
layer_newton_positive_zero_negative: (364, 91, 0)
active_endpoint_positive_zero_negative: (5695, 4385, 0)

OPG SECOND-ACTIVE NEWTON PROBE: PASS
positive_coefficients_through_q31: 1023
positive_transport_remainders_through_s20: 616
odd_kernel_positive_monomials: 57
odd_top_shift_positive_monomials: 20
odd_top_positive_boundary_values: 10
```

These are finite regression/falsification records only.  The source
claims retain their previous statuses until reconstructed in this lane.
