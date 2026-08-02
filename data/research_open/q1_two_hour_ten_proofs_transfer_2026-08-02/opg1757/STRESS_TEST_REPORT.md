# OPG-1757 complete log-layer stress report

Date: 2026-08-02

Status: **PASS; CORROBORATION ONLY**.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -u stress_complete_log_layer.py
```

Exact output:

```text
OPG COMPLETE LOG-LAYER EXTENDED STRESS: PASS
odd_sufficient {'parameters': 90, 'coefficients': 22419, 'largest_s': 10000, 'largest_d': 2219}
odd_page {'parameters': 90, 'coefficients': 22419, 'largest_s': 10000, 'largest_d': 2219}
even_sufficient {'parameters': 90, 'coefficients': 22251, 'largest_s': 10000, 'largest_d': 2219}
even_page {'parameters': 90, 'coefficients': 22251, 'largest_s': 10000, 'largest_d': 2219}
grand_total_coefficients: 89340
role: CORROBORATION_ONLY
source_sha256: a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
status_original_opg1757: OPEN
```

The parameter set consists of every integer `23<=s<=96` and

```text
100, 112, 128, 160, 200, 250, 320, 400, 512, 750,
1000, 1500, 2000, 3000, 5000, 10000.
```

For each parameter, the scan uses exact Python integers and checks every
coefficient in

\[
 31\le d<241\log s
\]

that lies in the corresponding natural bulk range, for all four certificate
sums.  The endpoint is implemented as `ceil(241*log(s))-1`, the largest
integer strictly below the real threshold (up to the ordinary floating-point
evaluation used only to choose the scan range).

This finite computation is not used in the proof of the eventual theorem.
In particular, it does not establish positivity for unscanned parameters,
and it does not prove the original OPG-1757 proposition.  The separate
effective threshold in `EFFECTIVE_GAP_BOUND.md` comes from analytic error
majorants and exact rational inequalities, not from this scan.
