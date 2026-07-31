# Route E: the \(2/9\) joint-endpoint sensitivity theorem

This directory independently audits the simultaneously saturated
rich-line Szemerédi--Trotter and target-service constraints at the live
\(2/9\) endpoint.

The outcome is conditional, not an endpoint exclusion:

- target service alone has an exact finite saturation model;
- no unconditional power saving is claimed;
- one concrete joint saving
  \[
  RNu^4
  \le
  t^{-\delta+o(1)}MQ(ML)^2
  \]
  improves the matching threshold by exactly \(\delta/18\), throughout
  the audited range \(0<\delta<16/5\).

Files:

- `CONDITIONAL_JOINT_ENDPOINT_THEOREM.md`: proof, coefficient audit,
  finite obstruction, and claim boundary;
- `verify_joint_endpoint_saving.py`: exact rational certificates and
  the finite service-saturation model;
- `test_verify_joint_endpoint_saving.py`: regression tests.

Reproduce with:

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_e
python3 verify_joint_endpoint_saving.py
pytest -q test_verify_joint_endpoint_saving.py
```
