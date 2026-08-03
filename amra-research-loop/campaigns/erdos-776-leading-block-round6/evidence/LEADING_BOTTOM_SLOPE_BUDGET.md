# Leading-block / bottom-transfer slope budget

## Scoped lemma

Fix a rank `n`, integer lower digits `A,B`, and suppose a proposed one-step local switch admits the exact
affine-in-`q` bookkeeping

```text
gamma = C(B,2)-C(A+1,2)+2-(4-delta)q+v,
B_next = C(B,2)-alpha*q-beta,
```

where `alpha,delta,beta,v` are fixed for this switch (they do not vary with
`q`).  Suppose its claimed canonical continuation implies

```text
B_next < q-c_n
```

for a fixed `c_n`.  Then

```text
gamma < (alpha+delta-3)q + (beta+v+2-c_n).       (1)
```

Indeed, the recurrence gives `C(B,2)=B_next+alpha*q+beta`; substitute this
and discard the nonpositive term `-C(A+1,2)`.  The strict canonical bound
then gives (1).

The actual odd K4,r9 parameters are unbounded (`q_next=4q-4`).  Therefore
`alpha+delta<3` makes the right side negative on every sufficiently late
actual strip.  Any switch which is nonnegative on arbitrarily large actual
strips and canonically continues must satisfy

```text
alpha+delta >= 3.                                (2)
```

For a leading-only switch (`alpha=0`), its surplus coefficient must improve
by at least three, from `-4` to at least `-1`.  For a bottom-only switch
(`delta=0`), the transfer must subtract at least `3q` in the stated sign
convention.  Mixed switches can share this budget.

## Equality and legality boundary

At `alpha+delta=3`, (1) retains the constant
`beta+v+2-c_n`; slope cancellation alone does not prove nonnegative surplus.
More importantly, this lemma does not prove that any pair with budget at
least three is realizable by canonical Macaulay words.  Such a realization
must supply exact before/after words, the Pascal identity, all digit-order
inequalities, and a suffix persistence theorem.

The original round-four/round-five interface has `alpha=delta=0` and hence
budget zero, recovering its strict asymptotic failure.  Fixed `O(1)` changes
to digits or transfer constants change only the constant in (1), not the
budget.

## Research consequence

This is a search-space cut: exact enumeration should begin at combined
budget three and should test canonical legality before deeper computation.
It is not a legal-switch construction, public threshold improvement, or
closure of Erdos-776.
