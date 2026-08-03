# Independent audit: gamma-four feedback reduction

Verdict: **pass for the symbolic reduction and the infinite high-half chamber;
the strict low-half two-variable kernel remains open**.

The reconstruction uses the canonical rank-two formulas directly and imports
no campaign checker.  For every accepted relaxed state with `s>=3`, it checks

```text
gamma4 = C(A,3)-C(a+1,3)+C(E,2)-C(e,2)+C(a,2)-1-C(r,2),
A >= a+s,
C(r,2) >= C(a+s,3)-C(a+1,3)+a-1 >= a^2+3a,
C(r,2) > C(a+1,3)-C(c+1,3),
r >= rho(a,c),
A >= B(a,c).
```

These are exact implications, not empirical fits.  They reduce the unresolved
multi-cap interval to the pure discrete inequality

```text
B(a,c) >= A_*(a,c),       a>=3, 3<=c<=a.
```

The bounded guard used `max_r=120` for exact relaxed states and the rectangular
kernel box `3<=a<=1000`, `3<=c<=a`, under a 3-GiB/180-second wrapper.  Results:

```text
exact relaxed s>=3 states checked : 365
kernel pairs checked              : 498,501
kernel failures                   : 0
minimum B-A_*                     : 0 at (a,c,rho,B,A_*)=(6,3,11,10,10)
rho branch counts                 : gamma=3,001, p=495,491, tie=9
high-half explicit-D failures     : 13, last at (a,c)=(16,8)
```

The finite box does not prove the kernel for arbitrary `a`.  In particular,
this audit does not yet promote the relaxed theorem, the actual dyadic theorem,
or the public Erdos-776 claim.

The adjacent-sum rewrite also gives
`D<=c+1+ceil(C(a+1,3)/C(c+1,3))`.  In the finite high-half chamber `2c>=a`,
the resulting explicit certificate has only the 13 small failures reported
above.  The evidence note now supplies an infinite proof for the entire
high-half chamber: gamma feedback gives `B>=a+4`; `q0<=9`; the nine branches
reduce to explicit decreasing quadratics in `c`; six rational `c/a` bounds
close `q0=3,...,8`; and `q0=1,2,9` close directly.  The exact base
`3<=a<=68`, `max(3,ceil(a/2))<=c<=a` has 1,219 pairs and no failure.  The remaining
proof obligation is precisely `2c<a`, where the p-bound controls `rho`.

For that low-half chamber the audited fourth-root construction

```text
L=max(c+2,3+ceil(((c+1)^4+4(a+1)^3)^(1/4)))
```

rigorously gives `D<=L`.  The stronger explicit target certificate using `L`
has exactly six failures in the box `a<=1000`, at `(7,3)`, `(8,3)`, `(9,3)`,
`(9,4)`, `(10,3)`, `(10,4)`, and none for tested `a>=11`.  The exact kernel
passes those six points.  Eventual success of this certificate is still a
conjecture, not a theorem.

Artifacts:

- `verify_gamma4_feedback_reduction.py` SHA-256
  `41b172c2f9dffa02e74c3523efa7949212d61eaccecece43eb84ef9eb530b0e6`
- `GAMMA4_FEEDBACK_REDUCTION_AUDIT.json` SHA-256
  `f1122ce4655e234ae00560ce110b6206edf64aec52231c59db5d3874515c3b68`

Reproduction:

```sh
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 \
  amra-research-loop/scripts/run_bounded.sh python3 -u \
  amra-research-loop/campaigns/erdos-776-c1-round3/audit/verify_gamma4_feedback_reduction.py \
  --max-r 120 --max-a 1000 \
  --output amra-research-loop/campaigns/erdos-776-c1-round3/audit/GAMMA4_FEEDBACK_REDUCTION_AUDIT.json
```
