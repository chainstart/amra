# Verification receipt

Date: 2026-08-27

## Author-side replay

Command:

```text
python3 amra-research-loop/campaigns/erdos-786-grid-transversal-barrier-20260827/evidence/verify_grid_transversal.py
```

Result:

```text
PASS: grid algebra, marginals, transversal bound, counterexamples, and height guards
```

The replay exhausts the `d=m=3` grid atlas and every deletion subset, checks
the exact marginals for `d=3,m=4`, verifies a signed `K_(2,3)` minimality
example, checks the false universal binomial shortcut, and evaluates a finite
instance of the dense-atlas inequalities.  It does not infer the
all-parameter theorem or the prime-number-theorem asymptotic.

Package tests:

```text
python3 -m pytest -q amra-research-loop/tests
........                                                                 [100%]
8 passed in 0.09s
```

## Frozen hashes before independent audit

```text
SURVIVOR_DEEPENING.md  1eaa15ddd19c7fe538d06ddb56f4220df71fc152a5576a454e90d7804f139adb
verify_grid_transversal.py  a60bfb9d5f2a84cc824266803ef1fd5e3499356ac44552e1af28be2fabde5765
decisive_lemma.json  2f7e20429b73c4c9c8d5ab8ae6b52f825ea82da1ee42f7fd1dc43a18a4d18e3c
```

This is an author-side receipt only.  It is not an independent
reconstruction and does not satisfy the campaign audit gate.
