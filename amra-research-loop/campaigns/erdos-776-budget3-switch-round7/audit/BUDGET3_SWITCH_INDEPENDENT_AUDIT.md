# Independent audit: actual budget-three Macaulay switch

Date: 2026-08-03

Verdict: **the sharp one-wall classification and the single actual
`j=1231` witness pass; freeze without public promotion**.

The audit reconstructed the original `K4,r9` integers, every greedy
Macaulay word through rank 12, both upper shadows and both surplus signs
before reading the round-7 author verifier.  The independent implementation
imports no campaign evidence code.

## 1. Actual orbit and greedy uniqueness

For odd `j=1231`, the reconstruction starts from

```text
h=112*2^(j-1), q=(2h+4)/3, b=q+4, H=5q/2, tau=4q-2,
x=C(h+b-2,3)+C(b-1,2)+2-2h,
y=C(h+b-1,3)+C(b,2)+2-2h.
```

It checks the original dyadic identities and obtains the rank-three words

```text
x_3=(H,3),(q,2),(9,1),
y_3=(H+1,3),(q+1,2),(12,1).
```

At each rank, greedy expansion chooses the unique largest top `a_k` with
`C(a_k,k)` not exceeding the current remainder and then recurses below the
strict ceiling `a_k`.  The defining half-open binomial interval forces
`a_k`; induction forces every later digit.  Thus the rank-12 switch is a
change of the unique canonical cell after an actual wall crossing, not a
choice between two words for one integer.

Using

```text
A_4=25, B_4=58,
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52),
```

the independent raw replay agrees digit-for-digit with both inherited
stable words at rank 11.  The rank-12 x-word also remains stable.

## 2. Exact rank-two wall

At a resulting rank `m`, put `t=q-(5m-16)`.  Moving the rank-two top from
`t` to `t+s` costs

```text
Delta_s=C(t+s,2)-C(t,2)=s*t+s(s-1)/2.
```

The unique greedy rank-two shift is `s` exactly when
`Delta_s<=B_m<Delta_(s+1)`, with residual `B_m-Delta_s` in
`[0,t+s)`.  Hence

```text
s=3 iff 3t+3 <= B_m < 4t+6.
```

The preceding rank-three top in the inherited word is `t+4`.  Therefore
`s=3` retains strict order `t+4>t+3`, while `s=4` gives equality and exits
this one-wall rank-two class through a higher carry.  The theorem's
"maximal budget three" is correct only in this explicitly inherited class;
it is not a no-go for every possible higher-digit switch.

For `m=12,j=1231`, the exact interval holds.  The raw y-word ends in

```text
(t+3,2),(R,1),  R=B_12-3t-3,
```

with `0<=R<t+3`.  Substitution of the stable recurrence gives

```text
R=C(B_11,2)-3q-(5*12-21).
```

Thus the coefficient of `q` is `-3`, so in the round-six convention the
literal bottom switch has `alpha=3`.  No higher staircase digit changes, so
`delta=0`; the sign convention has not been reversed.

## 3. Surplus crossing

For each raw rank state the audit independently computes

```text
gamma_n=U_n(y_n)-U_n(x_n)-x_n-tau,
```

where `U_n` raises every canonical binomial lower index by one.  On the same
actual member it obtains

```text
gamma_11<0<gamma_12.
```

The switch is therefore a legal local immediate-recovery witness, not just
a coefficient table.

## 4. Quantifier and publication firewall

What is proved is existential and local:

```text
there exists one actual odd K4,r9 member j=1231 whose rank 11->12
transition realizes the critical budget and changes the surplus sign.
```

The one-wall interval identity is all-parameter, but the audit does not
prove that every odd member reaches such a wall, that one switch rule works
uniformly, that recovery occurs before rank 42 for every state, or that the
positive seed persists through the suffix construction.  No adjacent-orbit
capacity interface is supplied.  The public Erdős-776 antichain threshold,
main term and exponent are unchanged.  External priority remains uncertain.

## 5. Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-776-budget3-switch-round7/audit/verify_budget3_switch_independent.py
```

Result: `PASS`; `q` has 1237 bits, both signs cross as claimed, and the
independent verifier SHA-256 is
`b98452108a3e85571537ae1fb18b868e96cec28787778b7867ed70e3b25cf55b`.

Only after this reconstruction, both author verifiers were run under the
same 3 GiB / 180 s bound and passed.  Their implementation is distinct from
the independent engine.
