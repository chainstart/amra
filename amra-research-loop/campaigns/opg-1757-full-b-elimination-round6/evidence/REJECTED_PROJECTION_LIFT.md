# Rejected projection-lift path

The last numerical path candidate used the rational lift

```text
b=M A,        M=10^6,        P=A b+C=M A^2+C.
```

Its proposed base vertices were

```text
(1,1,1,1),
(1,-7/4,2,7/8),
(-3/5,-41/10,4/5,-5/2),
(-7/5,-5,-3,-5).
```

Exact univariate root counting rejects the first lifted segment.  Although
`P` is positive at both endpoints, its degree-ten restriction has exactly
two roots in the open parameter interval `(0,1)`.  The segment therefore
touches or crosses `P=0` and is not contained in the positive component.

This preserves the topology firewall from the earlier ledger: coarse path
sampling and positive endpoint checks are insufficient near narrow walls.
The later `GARDING_PRT_COMPONENT_FIREWALL.md` settles the endpoint question:
the negative-`xi` endpoint is outside the distinguished component because a
positive `a`-ray reaches `P<0` (and because `partial_a P<0` there).  This does
not establish complete-component domination, and no OPG-1757 conclusion
changes.

Reproduce with

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/opg-1757-full-b-elimination-round6/evidence/audit_wall/reject_projection_wall_path.py
```
