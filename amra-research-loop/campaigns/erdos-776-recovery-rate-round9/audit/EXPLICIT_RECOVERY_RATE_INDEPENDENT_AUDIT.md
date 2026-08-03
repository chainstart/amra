# Independent audit: explicit K4,r9 recovery rate

## Verdict

Pass, with fixed-family scope only.  For every actual odd member `j>=1`,
the first nonnegative surplus is attained no later than

```text
p(j)=2+ceil(log_2(j+4)).
```

This is a member-dependent upper bound.  It does not give a uniform rank,
recovery by rank 42, an adjacent-orbit theorem, suffix persistence, or a
public Erdős-776 improvement.

## Blind reconstruction

I reconstructed the arithmetic before comparing with the author verifier.
The stable constants obey

```text
B_4=58,
B_(n+1)=C(B_n,2)-(20n-52),
B_5=1625>2^10.
```

The round-eight induction gives `B_n>=20n` for `n>=5`.  Under this
hypothesis,

```text
B_(n+1)-B_n^2/4
 = B_n^2/4-B_n/2-20n+52
 >= 100n^2-30n+52 > 0.
```

Thus `B_(n+1)>=B_n^2/4`.  If `E_n=2+2^(n-2)`, then
`2E_n-2=E_(n+1)`, so the base at rank five and induction prove

```text
B_n>=2^(2+2^(n-2))  for n>=5.                 (1)
```

For odd `j`, exact divisibility gives

```text
q_j=(224*2^(j-1)+4)/3=(112*2^j+4)/3.
```

Since `112*2^j+4<192*2^j`, one has
`q_j<2^(j+6)`.  Integer-only evaluation of the ceiling is

```text
ceil(log_2(j+4))=(j+3).bit_length().
```

Consequently `2^(p(j)-2)>=j+4`, hence the exponent in (1) at rank
`p(j)` is at least `j+6`.  Therefore

```text
B_(p(j))>=2^(2+2^(p(j)-2))>=2^(j+6)>q_j.      (2)
```

The exact small members recover at ranks `4,4,5` for `j=1,3,5`, below
their bounds `5,5,6`.  For `j>=7`, rank five is stable.  If recovery has
not occurred earlier, (2) makes the round-eight stable inequality
`B_m<q_j-(5m-16)` impossible by `m=p(j)`.  Hence its audited
stable-or-first-wall theorem gives a strictly positive wall no later than
that rank.  This establishes the claimed full-prefix bound; it is not an
extrapolation from the finite scan.

## Quantifier compatibility

The fact that `p(j)` tends to infinity does **not** by itself prove that
the actual first-recovery ranks are unbounded.  That lower-bound statement
comes independently from round four:

```text
for every fixed R, there exists one actual odd j_R whose surpluses are
negative simultaneously through R.
```

The two results are compatible: round nine gives `forall j exists p<=p(j)`;
round four rules out `exists R forall j p<=R`.  No single member is claimed
to remain negative forever.

## Machine checks

The independent verifier reproduced the recurrence bounds through rank 18,
checked 50,001 integer-ceiling/exponent rows, checked exact `q_j` arithmetic
on a dense prefix and sparse witnesses through `j=1,000,001`, and directly
replayed the first 101 odd greedy orbits.  It returned

```text
PASS independent explicit recovery-rate audit
B5=1625 ceiling_rows=50001 raw_members=101
bases=[(1, 4, 5), (3, 4, 5), (5, 5, 6)] last=(201, 9, 10)
```

It was run under 3 GiB / 180 s.  SHA-256 of the independent verifier:
`c389d93329f7ef1c3500981b895d9ba4160196b2fd794cf01c023e919f43ebf2`.
After blind reconstruction, the distinct author verifier also passed under
the same resource bound.

External novelty and priority were not checked, so they remain uncertain.
