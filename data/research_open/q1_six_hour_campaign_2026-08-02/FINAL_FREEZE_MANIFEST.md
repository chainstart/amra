# Final freeze manifest

Date: 2026-08-02

Baseline: `669bbad1908e7ab7d8382a8b508e67757006e90c`

Status: **FOUR AUDITED PACKAGES FROZEN; FOUR PUBLIC PROBLEMS OPEN**

## Final regression

Command:

    PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
      data/research_open/q1_six_hour_campaign_2026-08-02

Window: 16:15:53--16:26:21 HKT

Result: `151 passed in 613.80s (0:10:13)`

The count includes four author-verification tests for the late, explicitly
unadmitted #1083 observation.  It does not change the final claim ledger.

## Summary documents

| File | SHA-256 |
|---|---|
| `README.md` | `f4e63749388b9bfa0e583dd9db1df45d15e2699349ce8b7e5c33f18b688f27f7` |
| `FINAL_REPORT.md` | `0c8fa23b670bf73d7bfa5d0f22d0ee20b23aae2ad45de570e863b3887c7b6334` |
| `FINAL_CLAIM_LEDGER.md` | `d38711b21cd5199d3c82ec9a42fc24a9d0f57119cd00ba16d874d441cf84aa32` |
| `BLIND_AUDIT_RESULTS.md` | `5a4250c61f2f6090a0608c4900e06d98a7ebca8366bfdeaf113b6bac8bd78630` |
| `PUBLICATION_ROADMAP.md` | `dda8fdaf13524bb9a92d7afe316ee2feed3bd43c80f9c1666301204af92fc0b1` |

## OPG-1757 admitted package

| File | SHA-256 |
|---|---|
| `opg1757/THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md` | `08fa2ffba8bf9a88ac88985170914ddaad7b9f64ce692127e0901529540eb2ee` |
| `opg1757/THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY_BLIND_AUDIT.md` | `71fef43e049853c6a956232eb0d7506bac8a5da285f50423e5bab8b6168b64ef` |
| `opg1757/verify_third_active_log_boundary_blind_audit.py` | `de94e71398cb12d11084f6b9ad3327a76630b1b1590e296e2f1a8e4ebe4e8771` |
| `opg1757/test_third_active_log_boundary_blind_audit.py` | `dd0a27879dce52e75b49625212622cbb3451e62e9893ad55de5f95ab6cfb38be` |

## Erdős #1083 admitted package

| File | SHA-256 |
|---|---|
| `erdos1083/CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md` | `8106c8db649bdd24d4001ae88c722876b7515af8742741a134c4b76cf3ee15c3` |
| `erdos1083/FINITE_QUOTIENT_SHADOW_ESCAPE.md` | `8bc2d92c01f98be1597a90062bf64c95155b36caa1579e7db85793e5e8a4429b` |
| `erdos1083/PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md` | `d9f088fc416f082d61f60786c60b31d278bbb3d7c1ad75cb5745f6f08584f34d` |
| `erdos1083/TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md` | `6830869efca2fb6a46353b0ebfed84537d0ba6ebae089bc75dd41931f56d9f72` |
| `erdos1083/SIGNED_SWITCH_BLIND_AUDIT_II.md` | `10bdeddb625c91e0206fd98b6d7c85dfc6393e21a480fdfd0510f3d3225b71e9` |
| `erdos1083/verify_signed_switch_blind_audit_ii.py` | `254580f5c0fc8683e5f69362a9163538ba00cdfc2e153cc1d7dafb29c0d4b84b` |
| `erdos1083/test_signed_switch_blind_audit_ii.py` | `c3bdcabb3146a98d7fc79d82936fc3088dc9e4be75c45f7e25bdf35a04fd0ce2` |

## Erdős #776 admitted package

| File | SHA-256 |
|---|---|
| `erdos776/FINAL_CHAMBER_COUNTERFAMILY.md` | `d80527f53b6a74e523b07e87a03f3f1a36db43b4c3a46fb60e203bd63396dd23` |
| `erdos776/LEADING_BLOCK_DEFICIT_THEOREM.md` | `b94b9c46993e200bc8120260aa008dafc8552a18e35d2c4a18aea434e1f95a9d` |
| `erdos776/FINAL_CHAMBER_COUNTERFAMILY_BLIND_AUDIT.md` | `388a61b6cd588161336a03e63241b6bab83d924d926f43296270d759cadda4dd` |
| `erdos776/verify_final_chamber_counterfamily_blind.py` | `14deb1d50bbb80a639b72c5aa9d85c57fd99b5e215f136d7236f3e4fc231c5ea` |
| `erdos776/test_verify_final_chamber_counterfamily_blind.py` | `f0cfd9752be4ca8a09538379a5a8f6651f2742f868d23f928f67ff6a96b0fbca` |

## Erdős #809 admitted package

| File | SHA-256 |
|---|---|
| `erdos809/MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md` | `5c3e07e97a0b96a14b8c1be63331d3431366399e0c749eaa9d43f62f1e6c9602` |
| `erdos809/MAXIMUM_WITNESS_CANONICAL_HARDNESS_NORMAL_FORM.md` | `5f45b26ff205c0fead1612a60eb1c26cc7f66f1ea2abc32da49e417a2a3d081b` |
| `erdos809/MAXIMUM_WITNESS_SQRT_SPREAD_BLIND_AUDIT.md` | `8edb5b011a498ae6ed37e1d496b2d5241afb1467163b16d2ed149aeef5a1ddf3` |
| `erdos809/verify_maximum_witness_sqrt_spread_blind_audit.py` | `1ee7433e6f6216886af77d350ae9b517f0804d11211664a20df8942f542cf621` |
| `erdos809/test_maximum_witness_sqrt_spread_blind_audit.py` | `89a6b55c6c3266adf5eb22fc19556e78c20fa3fe826db1da347a5df58468d836` |

## Explicitly unadmitted post-audit observation

These files are preserved for the next campaign but have no blind-audit
status and are not used by `FINAL_CLAIM_LEDGER.md`:

| File | SHA-256 |
|---|---|
| `erdos1083/FULL_EUCLIDEAN_INTERVAL_MULTIROW_NO_GO.md` | `0b49747b104f89a2c07696595235764242f57a20ee9711a4c9ecc4b019722833` |
| `erdos1083/verify_full_euclidean_interval_multirow_nogo.py` | `ec9c8a03e85d4b6450575082e4001c6c590bb13c64700c5d091364f375a56b06` |
| `erdos1083/test_full_euclidean_interval_multirow_nogo.py` | `bcbebc8744895feaf49eb1d15928c240d0507cde179058af877718f2769c3df8` |

## Static freeze

- 120 generated `.pyc` files removed; no `__pycache__` directory remains.
- No trailing whitespace, unbalanced display delimiters, known malformed
  math escapes, conflict markers, or nonprinting control characters.
- Repository status contains only the new campaign directory.
- No commit or push was performed.
