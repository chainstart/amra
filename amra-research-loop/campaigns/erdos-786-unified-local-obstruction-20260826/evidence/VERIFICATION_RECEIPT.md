# Verification receipt

Date: 2026-08-26 (Asia/Hong_Kong)

Environment: Python 3.12.3

Command:

```text
python3 amra-research-loop/campaigns/erdos-786-unified-local-obstruction-20260826/evidence/verify_constant_width_obstruction.py
```

Result: `PASS`.

The replay checked exact constructions for bases 2, 3, and 5; product
equality; pairwise distinctness; strict membership in `(N/b^18,N]`;
avoidance of frozen controlled primes; exhaustive small-support minimality;
the zero-signature union-bound interface; and positive finite survival
probability for representative independent-rounding parameters.  A separate
integer budget loop checked the universal inequalities for `32<=K<=256`
and bases 2, 3, 5, and 7.  These checks guard the symbolic proof and are not
the source of its universal quantifiers.

SHA-256:

* `SURVIVOR_DEEPENING.md`:
  `5970e263ca452701580a7b501dee1c1cf8c388c896a8675b3d018de79c93ca64`
* `verify_constant_width_obstruction.py`:
  `3bb798d8cc21117c26d1f35babddc7402dd59dd74ccea6f04b0b1ac18f2b68d4`
