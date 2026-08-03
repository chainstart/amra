# A literal budget-three Macaulay switch

## Result and boundary

The necessary affine budget `alpha+delta>=3` from round six is sharp at the
level of a real greedy Macaulay transition.  On the actual odd `K=4,r=9`
member `j=1231`, the transition from rank 11 to rank 12 has a legal bottom
switch with

```text
alpha=3, delta=0,
gamma_11<0<gamma_12.
```

This is an exact existence result for the formerly empty legal-witness slot.
It does not give a uniform choice over all strips, a pre-rank-42 theorem for
all states, suffix persistence, or the public Erdős-776 bound.

## Universal one-wall identity

At resulting rank `m`, put

```text
t=q-(5m-16).
```

The stable B-side word would end in

```text
C(t,2)+B_m.
```

If

```text
3t+3 <= B_m < 4t+6,
```

then Pascal's identity gives, exactly,

```text
C(t,2)+B_m = C(t+3,2)+R,
R = B_m-3t-3,
0 <= R < t+3.
```

The preceding rank-three top is `t+4`, so `t+3` is the largest possible
legal rank-two top.  Thus this is not an alternative expansion: it is the
unique greedy canonical word.  Using

```text
B_m=C(B_(m-1),2)-(20(m-1)-52)
```

reduces the residual to

```text
R=C(B_(m-1),2)-3q-(5m-21).
```

Consequently the switch derives the round-six coefficient `alpha=3`
directly from an exact word identity.  Since the leading H/q staircase is
unchanged, `delta=0`.  Canonical ordering also explains sharpness inside
this one-wall class: a bottom shift by four would collide with the preceding
rank-three top, so the maximal legal bottom budget before a higher carry is
three.

## Actual witness

Take

```text
j=1231,
h=112*2^(j-1),
q=(2h+4)/3,
b=q+4,
tau=4q-2.
```

These obey the original dyadic identities

```text
2h=3q-4,
C(b-1,2)+2-(C(q,2)+9)=2h,
C(b,2)+1-(C(q,2)+9)=tau.
```

Direct greedy expansion of the uncompressed orbit verifies:

1. both rank-11 words are the round-four stable words;
2. `gamma_11<0`;
3. the rank-12 x-word remains stable;
4. the rank-12 y-word replaces its last two terms by
   `(t+3,2),(R,1)` and is strictly canonical;
5. `gamma_12>0`.

Here `q` has 1237 bits, `gamma_11` has 1231 bits in absolute value, and
`gamma_12` has 2474 bits.  The verifier records hashes rather than printing
the large witness integers.

Run with the campaign resource bound:

```bash
ulimit -Sv 3145728
timeout 180s python3 \
  amra-research-loop/campaigns/erdos-776-budget3-switch-round7/evidence/verify_actual_budget_three_switch.py
```

The broader bounded probes find the same literal budget-three wall at
resulting ranks 12, 14, 17, and 21 among the wall representatives through
rank 22.  No higher carry appears in that finite range.  These additional
rows remain finite search evidence only; no recurrence or frequency theorem
for the wall budgets is claimed.
