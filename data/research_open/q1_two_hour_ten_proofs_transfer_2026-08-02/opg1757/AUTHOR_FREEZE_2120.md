# OPG-1757 author freeze at 21:20 HKT

Date: 2026-08-02

Freeze status: **AUTHOR VERSION COMPLETE; READY FOR INDEPENDENT AUDIT**.

## 1. Frozen mathematical claim

Let

```text
S_gap =
557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374.
```

This integer has exactly **117 decimal digits**.  For every integer
`s >= S_gap` and every integer `d` satisfying

```text
31 <= d < 241 log(s),
```

the two actual candidate third-active transport coefficients are strictly
positive.  This is the effective form of the new logarithmic-gap theorem.

The threshold is not a numerical guess and does not come from the stress
scan.  In `effective_gap_bound.py`, the pinned exact recurrence is split at
transport index `K=1000`.  For every fixed index below `K`, exact integer
arithmetic constructs a sufficient bound
`floor(E_k/L_k)+1`.  The maximum is attained by the odd page certificate at
`k=999` and is the displayed 117-digit integer.  It dominates the other
three fixed-index maxima, their binomial-error requirements, the shifted
positivity starts, and the geometry threshold `242^2=58564`.  For
`k>=1000`, exact `Fraction` comparisons certify four monotone error sums
strictly below `1/2`; no decimal approximation is used in a decisive test.

The recurrence source from which all kernels are reconstructed is

```text
/home/biostar/work/projects/amra/data/research_open/q1_six_hour_campaign_2026-08-02/opg1757/third_active_transport_recurrence_attack.py
SHA-256 a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
```

Both certificate programs abort if this source hash changes.

## 2. Exact integer splice with the old results

For an integer coefficient degree `d` in the natural support
`0 <= d <= 2s-4`, the eventual proof uses exactly these three cases:

1. `0 <= d <= 30`: the old universal low-column theorem;
2. `31 <= d < 241 log(s)`: the new effective gap theorem;
3. `241 log(s) <= d <= 2s-4`: the old logarithmic-boundary theorem,
   including its already-proved bulk/top-band splice.

There is no missing integer endpoint.  Cases 1 and 2 meet at consecutive
integers 30 and 31.  For any real `x=241 log(s)`, the integers in case 2 are
exactly

```text
31 <= d <= ceil(x)-1,
```

which is also the endpoint convention used by the verification scripts.
Every remaining integer `d>=31` obeys `d>=x` and is in case 3; equality, if
it occurs, belongs to case 3 because its lower inequality is non-strict.
After enlarging the eventual threshold so the logarithmic layer is inside
the natural bulk ranges, these cases cover the full support.

Consequently, the two candidate third-active transports are
coefficientwise strictly positive for all sufficiently large `s`.

## 3. Ineffectivity and open-problem firewall

The 117-digit number is an effective threshold **only for case 2**.  The
old theorem used in case 3 has an ineffective eventual threshold.  Hence
the combined `S_transport` exists but remains **ineffective**: it is invalid
to report the 117-digit `S_gap` as an effective threshold for the complete
transport.

This author freeze does not prove positivity for every finite stable `s`, a
universal third-active-row theorem, later rows, arbitrary-host transfer, or
the original OPG-1757 proposition.  All of those claims remain **OPEN**.

## 4. Complete verification rerun

All commands below were rerun from this directory on 2026-08-02 immediately
before the freeze, with bytecode generation disabled.

### Unit tests

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
..                                                                       [100%]
2 passed in 24.43s
```

### Structural and complete-channel certificate

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 verify_complete_log_layer.py
OPG COMPLETE LOG-LAYER FINITE DATA: PASS
source_sha256: a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
odd_sufficient {'top_monomials': 25, 'strictly_lower_monomials': 710}
even_sufficient {'top_monomials': 36, 'strictly_lower_monomials': 1222}
odd_page {'top_monomials': 21, 'strictly_lower_monomials': 525}
even_page {'top_monomials': 31, 'strictly_lower_monomials': 949}
p6 {'first_positive_degree': 8, 'checked_positive_sufficient_leads': 65, 'checked_positive_page_leads': 65, 'page_transition_constant': 4/125}
p7 {'first_positive_degree': 10, 'checked_positive_sufficient_leads': 65, 'checked_positive_page_leads': 65, 'page_transition_constant': 49/2160}
corroborating_scan_coefficients: 2540
scan_role: CORROBORATION_ONLY
status_eventual_gap_theorem: PROVED_IN_COMPANION_NOTE
status_original_opg1757: OPEN
```

### Effective certificate

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 effective_gap_bound.py
OPG COMPLETE LOG-LAYER EFFECTIVE BOUND: PASS
source_sha256: a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
k_cutoff: 1000
geometry_threshold: 58564
odd_sufficient threshold: 84084178721600836612491482881224005603079639962 (k=999; max Q=1012986)
even_sufficient threshold: 103990364851545016369295143433465885138144397960117967018 (k=999; max Q=1014984)
odd_page threshold: 557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374 (k=999; max Q=1007967)
even_page threshold: 559330005252417606463492302337154032928086116534685423818097225862646092302799175753733844066084675514273958813224 (k=999; max Q=1009961)
growing bounds at k=1000: odd sufficient ~10^-25.154; even sufficient ~10^-2.477; odd page ~10^-67.668; even page ~10^-42.472
S_gap_effective_digits: 117
status_original_opg1757: OPEN
```

The four displayed scientific-notation values are output summaries only;
the program's comparisons use the underlying exact rational numbers.

### Extended finite stress scan

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 stress_complete_log_layer.py
OPG COMPLETE LOG-LAYER EXTENDED STRESS: PASS
odd_sufficient: 22419 coefficients
odd_page: 22419 coefficients
even_sufficient: 22251 coefficients
even_page: 22251 coefficients
grand_total_coefficients: 89340
largest_s: 10000
largest_d: 2219
role: CORROBORATION_ONLY
source_sha256: a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
status_original_opg1757: OPEN
```

The stress scan is corroboration only and is not used to infer the eventual
theorem or the effective threshold.

## 5. Frozen artifact manifest

The embedded manifest covers every author artifact that existed immediately
before this freeze note.  The freeze note itself is necessarily excluded
from its own embedded hash manifest.

```text
7eee8939f234352f26283a3b4d6bdb14b49e2f01992e855c547b42861f0616da  AUDIT_HANDOFF.md
bb6e35ca886d5f506c6638c55b408682afafde762f1c76bca4012f7a583899f4  CLAIM_LEDGER.md
cbf9435c9a7d3641c3ca9ab0a02e9025ff2ee3d700254afc47296f4b02e75ccd  COMPLETE_LOG_LAYER_THEOREM.md
58412261a9e19dd98d5426eccc77d078dcbcd96cc37ce97d19153e16b4b8aead  EFFECTIVE_GAP_BOUND.md
31bb2853937a21a68b170bed55dbd3104ad4fd3f43e7f48e222040f1eef7df2d  README.md
5829cff6657129aa254fcc3b0155ea7ec8351f7ef47c3d88a88d596d1b585a38  RESEARCH_LOG.md
ae06ac328bb99e31b01a4364709418239db27027cc4ed2b35db40036d10aeff5  STRESS_TEST_REPORT.md
1a4f68d8de14d176b8b6a1b751befea4ce93ac6a02fb462d484744f0f88c06bb  TEN_PROOFS_METHOD_TRANSFER.md
f3e43a61088ec9706e8a8deead17bab0f03e144ad67f12a145a5c8c87600138e  effective_gap_bound.py
b886f51654201f0605b88c74f1d755e84e768b8de702156a79a294c44675f82e  stress_complete_log_layer.py
601a6c1511496b90101129f174d903c7069d81ef65dd6e90c199e6d53dedf47d  test_complete_log_layer.py
653c52c9dd6c2d9fa2fc30a21fe4336c728510c70fdaa76f4352afd2403cccd1  test_effective_gap_bound.py
37c9b5b4c21e0ef478443c8e9c012b07747754979e5397e57760b2729a01bdf1  verify_complete_log_layer.py
```

No `__pycache__` directory was present at freeze time.
