# Independent audit of `C1_TWO_ROW_RECOVERY_NORMAL_FORM`

## Verdict

The normalized formulas for `gamma5` and (on the stated no-borrow side)
`gamma6` pass an independent reconstruction from the raw Macaulay orbit.
No counterexample to the proposed two-row recovery invariant was found.

There are nevertheless two important qualifications.

1. The original search program does not count `gamma5 < 0` together with
   `P < 0` or `V < 0` as a failure.  Such a row violates the candidate before
   `gamma6` can be evaluated, but the program only appends a failure when
   `gamma6 is not None and gamma6 < 0`.  The independent audit counts this
   borrow branch explicitly.  It found zero such rows, so this is a harness
   defect rather than a counterexample in the tested domain.
2. The observed negative box `k <= 17, r <= 46` is not stable.  Already at
   `j=31` there is a negative row with `k=18`, and by `j=40` a small forward
   probe reaches `k=43, r=133`.  Thus the proposed reduction to finitely many
   fibres cannot use the original numerical box.

This audit is finite evidence and a partial inequality reduction.  It does not
close Erdős #776.

## Reconstruction from the raw recurrence

For an actual `c=1` state put

```text
n = C(q,2)+r,                 n+b-1 = C(q+1,2)+u,
H = C(b,2)+1,                 tau = H-n,
z = U_2(n),                   w = U_2(n+b-1),
x0 = n+z-H+1,                 y0 = n+w-H.
```

The raw orbit gives

```text
gamma4 = U_3(y0)-U_3(x0)-x0-tau,
x1 = U_3(x0)-tau+1,           y1 = U_3(y0)-tau,
gamma5 = U_4(y1)-U_4(x1)-x1-tau.
```

On either `++ -> ++` or `-- -> ++`, direct integer comparison in the audit
script verifies

```text
x0 = C(a,3)+alpha,            y0 = C(a+1,3)+beta,
x1 = C(a,4)+p,                y1 = C(a+1,4)+v,
p = U_2(alpha)-tau+1,         v = U_2(beta)-tau.
```

All four tails were also checked to lie below their claimed next caps.  Hence
canonical concatenation and Pascal cancellation give

```text
gamma5 = U_3(v)-U_3(p)-U_2(alpha)-1.
```

If `P=U_3(p)-tau+1` and `V=U_3(v)-tau` are nonnegative, the same independent
full-orbit calculation one rank later gives

```text
gamma6 = U_4(V)-U_4(P)-U_3(p)-1.
```

The script computes the full orbit and the displayed tail identities by
separate code paths and asserts equality; it does not import the author
searcher.

## First `++ -> ++` inequality gate

Let

```text
e = v-p = U_2(beta)-U_2(alpha)-1.
```

The standard Macaulay superadditivity inequality

```text
U_d(s+t) >= U_d(s)+U_d(t)    (s,t >= 0)
```

follows by induction on the canonical binomial expansions, using Pascal's
identity at the first carry.  Therefore, whenever `e >= 0`,

```text
gamma5
  = U_3(p+e)-U_3(p)-U_2(alpha)-1
 >= U_3(e)-U_2(alpha)-1.
```

Consequently the following is a sufficient, `tau`-free first chamber gate:

```text
e >= 0  and  U_3(e) >= U_2(alpha)+1  ==>  gamma5 >= 0.       (G++)
```

All 4,593 audited `++ -> ++` rows satisfy `(G++)`.  Its smallest observed
margin is 80,701, at `(j,q,k,r)=(6,2436,4,145)`; the exact surplus there is
89,319.  The remaining proof task is to establish `(G++)` from the actual
dyadic and first-tail chamber inequalities, or subdivide the cells where it
does not follow.  The finite check is not a proof of that implication.

## Independent search result

The principal scan covered `2 <= j <= 32`, `2 <= k <= 3000`, every compatible
`r <= 3000`, and 51 compatible probes centered at each exact `A=0` and `B=0` wall.
It made 4,092,931 parameter probes and accepted 74,749 target rows:

- 4,593 `++ -> ++` rows;
- 70,156 `-- -> ++` rows;
- 433 rows with `gamma5 < 0`, all recovered at rank six;
- zero `gamma5 < 0` rows with a rank-six borrow;
- zero `gamma5,gamma6` double-negative rows;
- zero asymmetric first-sign sources reaching target `++`.

The negative rows in the principal scan already occupy `4 <= k <= 24` and
`9 <= r <= 58`.  A cheap forward probe with `j <= 40`, `k <= 100`, and
`r <= 200` shows continued growth, reaching `4 <= k <= 43` and
`10 <= r <= 133` at `j=40`.

## Reproduction

```bash
AMRA_MEMORY_KIB=1572864 AMRA_TIMEOUT_SECONDS=900 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-776-adaptive-uniformity/audit/independent_c1_two_row_audit.py
```

Script SHA-256:

```text
be92313e194eb1ac21d56493d02d505d536730f1ea92fe89e813f478a9e42c8f
```
