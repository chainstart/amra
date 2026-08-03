# Every actual K4,r9 member recovers at or before its first wall

## Theorem

For every actual odd member of the `K=4,r=9` dyadic family, some finite
Macaulay surplus is nonnegative.  More precisely, after the finite base, run
the round-four stable recurrence until either a stable surplus is
nonnegative or the B-side lower tail first crosses its canonical wall.  In
the second case the surplus at that first wall is strictly positive.

Combined with round four, this gives the sharp quantifier picture on this
fixed family:

```text
every member has a finite recovery rank,
but the recovery ranks have no uniform finite upper bound.
```

This is an all-`j` theorem for one actual family.  It is not an all-state
pre-rank-42 seed theorem and supplies no public suffix composition.

## 1. Stable constants

Use the audited recurrence

```text
A_4=25, B_4=58,
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).
```

For every `n>=6`,

```text
B_n >= 30 A_n,
A_n>A_(n-1)>0.
```

We also use the uniform linear bound

```text
A_n,B_n>=20n for n>=5.
```

It holds at rank five.  Substitution of `A_n=20n` into the smaller A-side
recurrence leaves

```text
C(20n,2)-(20n-49)-20(n+1)=200n^2-50n+29>0,
```

and the B-side subtracts three less.  Monotonicity gives the induction.

The first inequality holds at `n=6`:

```text
B_6=1319452 >= 30*35995=1079850.
```

If `B_n>=30A_n`, monotonicity of `C(x,2)` gives

```text
B_(n+1)-30A_(n+1)
 >= C(30A_n,2)-30C(A_n,2)+580n-1418
 = 435A_n^2+580n-1418 >0.
```

The growth of `A_n` follows immediately from the same recurrence and the
base `A_5=269`.  In particular both sequences are unbounded.

## 2. First-wall dichotomy

Fix an actual parameter `q=q_j`; its tax is `tau=4q-2`.  Suppose rank
`m-1>=5` is still in the stable cell and has negative surplus.  Put

```text
t=q-(5m-16).
```

The exact stable identity one rank earlier is

```text
gamma_(m-1)
 =B_m-A_m-A_(m-1)-1-4q <0.                 (1)
```

If `B_m<t`, then `A_m<B_m<t`, so both next words remain stable.  We either
obtain `gamma_m>=0`, or repeat.

If `B_m>=t`, the B-side reaches its first wall.  From (1),

```text
B_m<4q+A_m+A_(m-1)+1<4q+2A_m+1.
```

Together with `B_m>=30A_m`, this yields

```text
A_m+1<q/6.                                   (2)
```

The preceding stable B-tail also gives

```text
B_(m-1)<q-(5m-21).
```

Since `m>=6` and `B_(m-1)>=20(m-1)`, this implies

```text
q>25m-41>2(5m-16),
t>q/2.                                       (3)
```

## 3. The wall is positive, including higher carries

Let `U_m` denote the rank-`m` Macaulay raise.  This function is monotone in
its integer argument: greedy binomial intervals are ordered, and induction
below the leading interval preserves that order.  Explicitly, within one
leading interval the leading raised block is fixed and monotonicity reduces
to rank `m-1`.  At an interval boundary, the canonical expansion of
`C(a+1,m)-1` is

```text
C(a,m)+C(a-1,m-1)+...+C(a-m+1,1),
```

whose raise is strictly below `C(a+1,m+1)`, the raise of the next integer.
Induction from rank one proves monotonicity on the entire nonnegative
integer domain.

At the minimum wall value `B_m=t`, the nominal bottom

```text
C(t,2)+t
```

is the legal canonical block `C(t+1,2)`; its preceding rank-three top is
`t+4`.  Therefore, for every `B_m>=t`, including any carry beyond the
rank-two one-wall class, monotonicity gives

```text
gamma_m
 >= C(t,2)-C(A_m+1,2)+2-4q.                 (4)
```

Actual `q` is even.  By (2)--(3),

```text
C(t,2) >= C(q/2+1,2)=q^2/8+q/4,
C(A_m+1,2) < q^2/72.
```

Thus the right side of (4) is greater than

```text
q^2/9 - 15q/4 + 2 >0,
```

already for `q>=34`; all relevant actual rows have `q>=1196`.  Hence every
first wall recovers strictly.  This argument makes the round-eight
`higher-carry` narrow window harmless rather than needing to exclude it.

## 4. Termination and finite base

The actual base values are

```text
q_1=76, q_3=300, q_5=1196.
```

Direct exact calculation gives rank-four recovery at `j=1,3` and the
literal rank-five wall recovery at `j=5`.  For `j>=7`, rank five is stable.

If no stable surplus becomes nonnegative, the stable loop cannot continue
forever: `B_m` is strictly increasing and unbounded while `q` is fixed, so
eventually `B_m>=q-(5m-16)` and the first-wall argument applies.  This
proves the theorem for every odd `j`.

## 5. Evidence boundary

`verify_all_j_first_wall_recovery.py` checks every displayed recurrence and
inequality, independently replays the finite base, and scans the first 200
odd members through rank 18 as a guard.  The universal force is the natural
proof above, not that bounded scan.

The theorem does not provide:

- a recovery rank bounded by 42;
- a switch for every other `(K,r)` family or every public adjacent orbit;
- persistence after recovery;
- a changed public Erdős-776 main term or exponent.
