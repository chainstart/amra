# Independent audit: all-j first-wall recovery on K4,r9

Date: 2026-08-03

Verdict: **the all-odd-member fixed-family theorem passes; freeze without
public Erdős-776 promotion**.

The audit rebuilt the raw dyadic orbit, greedy Macaulay expansion, stable
constants and recurrence inequalities before reading the round-8 verifier.
Its implementation imports no author code.

## 1. Macaulay-raise monotonicity

For fixed rank `d`, write the greedy canonical expansion of `N` and raise
each lower binomial index by one.  The resulting function `U_d(N)` is
nondecreasing on all nonnegative integers.

Inside one leading interval `C(a,d)<=N<C(a+1,d)`, the leading raised block
is fixed and induction reduces monotonicity to rank `d-1` on the remainder.
At the upper boundary,

```text
C(a+1,d)-1
=C(a,d)+C(a-1,d-1)+...+C(a-d+1,1).
```

Raising this word gives strictly less than `C(a+1,d+1)`, the raised value
of the next integer.  Rank one is immediate, so induction covers every
interval and boundary.  An independent dense guard also checks ranks 2--8
and values 0--2999.

This monotonicity compares the actual wall with the minimum wall regardless
of how many higher carries occur; no unproved one-wall exhaustiveness is
used.

## 2. Stable constants and ratio cone

The independently rebuilt recurrences are

```text
A_4=25, B_4=58,
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).
```

At rank six,

```text
A_6=35995, B_6=1319452 >=30A_6.
```

If `B_n>=30A_n`, monotonicity of `C(x,2)` gives the exact induction margin

```text
B_(n+1)-30A_(n+1)
>=435A_n^2+580n-1418>0.
```

The separate linear induction gives `A_n,B_n>=20n` for `n>=5`, and the
A-recurrence gives `A_n>A_(n-1)>0`.  Hence `B_n>=30A_n` holds for every
`n>=6`, not only on the computed prefix; both sequences are unbounded.

## 3. Full-prefix first-wall argument

The small members have exact direct recovery:

```text
j=1: q=76,   rank 4, gamma=1026;
j=3: q=300,  rank 4, gamma=130;
j=5: q=1196, rank 5, gamma=758497.
```

For `j>=7`, `q>=4780` makes the audited rank-five stable words strict.  Now
follow the stable recurrence only while the current surplus is negative.
At a proposed resulting rank `m>=6`, put `t=q-(5m-16)`.

If `B_m<t`, then `A_m<B_m<t`; integrality actually gives the strict x-tail
ordering needed below `t-1`.  The exact recurrence therefore supplies the
next stable words.  If their surplus is nonnegative, recovery has already
occurred; otherwise the invariant repeats.  Thus when `B_m>=t` occurs, it is
the first wall and every earlier rank in the prefix is both stable and
negative.  This is the required minimum-wall full-prefix quantifier, not a
claim inferred from a wall table.

At that wall, the preceding negative identity is

```text
B_m-A_m-A_(m-1)-1-4q<0.
```

Using `B_m>=30A_m` and `A_(m-1)<A_m` gives

```text
28A_m<4q+1,
```

and since every relevant `q>=1196`, this implies the strict inequality

```text
A_m+1<q/6.                                      (1)
```

Previous B-tail stability gives

```text
B_(m-1)<q-(5m-21).
```

Together with `B_(m-1)>=20(m-1)` it yields
`q>25m-41>2(5m-16)`, hence

```text
t>q/2.                                          (2)
```

Both strict inequalities and their parameter ranges therefore check.

## 4. Minimum-wall positivity and termination

At the minimum wall `B_m=t`, the nominal block
`C(t,2)+t=C(t+1,2)` is canonical below the preceding top `t+4`.  Exact
stable-word cancellation gives

```text
gamma_m >= C(t,2)-C(A_m+1,2)+2-4q.
```

Macaulay-raise monotonicity makes this a lower bound for every deeper carry.
Actual `q` is even.  From (1)--(2), `t>=q/2+1` and
`C(A_m+1,2)<q^2/72`, so

```text
gamma_m > q^2/9-15q/4+2>0
```

for all relevant actual `q` (indeed for `q>=34`).  Every first wall after a
negative stable predecessor is therefore strictly positive.

If no earlier stable surplus recovers, the loop must meet such a wall:
`B_m` is increasing and unbounded while `q` is fixed and
`q-(5m-16)` decreases.  This proves `forall odd j exists finite p` with
`gamma_p>=0`.

## 5. Quantifier and publication boundary

Together with round four, the exact conclusion on this one family is

```text
every actual odd K4,r9 member recovers at some finite rank,
but no one finite rank bounds all members.
```

This does not provide recovery by rank 42, cover other `(K,r)` or adjacent
orbits, identify the recovered seed with public capacity, or prove suffix
persistence.  It changes no public threshold, main term or exponent.
External priority remains uncertain, so the correct action is to freeze the
audited fixed-family theorem without public promotion.

## 6. Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-776-wall-selection-round8/audit/verify_all_j_wall_independent.py
```

Result: `PASS`; exact bases, 51 independent raw-member guards, ratio
induction and both strict wall bounds.  SHA-256:
`da3f438c5a609ad03ef47bb43ffdbb8d341b5547ef5733ab3105fffc2192698d`.

After blind reconstruction, the author verifier was run under the same
3 GiB / 180 s bound and passed its 201-member guard.  The implementations
have different hashes.
