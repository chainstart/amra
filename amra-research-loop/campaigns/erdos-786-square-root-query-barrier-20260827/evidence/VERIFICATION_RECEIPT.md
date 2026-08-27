# Verification receipt

Date: 2026-08-27 (Asia/Hong_Kong)

Environment: Python 3.12.3

Command:

```text
python3 amra-research-loop/campaigns/erdos-786-square-root-query-barrier-20260827/evidence/verify_square_root_query_barrier.py
```

Result: `PASS`.

The replay checked exact constructions for bases 2, 3, and 5 at `A=4`;
the available prime counts in the chosen finite dyadic intervals; product
equality; distinctness; the fixed `(N/b^6,N]` tail; exhaustive support
minimality; controlled-prime avoidance; exact zero-transcript populations;
the shared-seed expectation charge; and sample square-root boundary
instances.  An integer-only budget loop checked bases 2, 3, 5, and 7,
`4<=A<=10`, and `16<=K<=512`.

The finite replay does not prove the universal prime supply.  That step is
the separately declared prime-number-theorem dependency
`pi(2X)-pi(X)~X/log X`.

SHA-256:

* `SURVIVOR_DEEPENING.md`:
  `ad4600edefd7e39d53ee21ddf9ef707c927b11ba251e797c495d8e8e3bf6877c`
* `verify_square_root_query_barrier.py`:
  `2d42c382a7430b06ed212a7e259ef806730018dffe361f2a6d25c18d7b53e082`
