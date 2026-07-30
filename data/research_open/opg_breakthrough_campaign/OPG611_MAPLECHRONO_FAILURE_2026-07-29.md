# OPG-611 `maplechrono` hard-run failure note

Date: 2026-07-29 (Asia/Hong_Kong)

The experimental hard run

```text
artifacts/opg_breakthrough/hard-six-hour/idx-052-maple-r64-18000s
```

did not produce a mathematical result.  Its last durable telemetry was:

```text
status=running
phase=master_solve
solver=maplechrono
master_models=2
master_solves=3
packing_cuts=2048
residual_cuts=256
elapsed_seconds=3599.071154121979
```

At `2026-07-29 12:41:08 HKT`, the WSL kernel log recorded:

```text
python3[1770654]: segfault ... in
pysolvers.cpython-312-x86_64-linux-gnu.so ... signal 11
WSL ... Capturing crash for pid: 1769156
```

The worker exited without a result or proof artifact.  It must therefore not
be classified as a timeout, exclusion, candidate, or negative search result.
The original directory is retained unchanged for forensic inspection.

A fresh retry was started with the previously stable `glucose42` backend and
a new output directory:

```text
artifacts/opg_breakthrough/hard-six-hour/idx-052-g42-r64-retry-14500s
```

No state or clauses from the crashed process were reused.
