# Explicit K4,r9 recovery-rank bound

## Theorem

For every actual odd K4,r9 member indexed by `j>=1`, there is a nonnegative
surplus by rank

```text
p(j)=2+ceil(log_2(j+4)).
```

Equivalently, the first recovery rank is `O(log j)=O(log log q_j)`.  This is
a member-dependent bound and therefore agrees with round four's theorem
that no one finite rank works for every member.

## 1. Taxed squaring lower bound

Round eight gives `B_n>=20n` for every `n>=5`.  Hence

```text
B_(n+1)-B_n^2/4
 =B_n^2/4-B_n/2-(20n-52)
 >=100n^2-30n+52>0.
```

Thus

```text
B_(n+1)>=B_n^2/4.                              (1)
```

Since `B_5=1625>2^10`, induction in (1) yields

```text
B_n >= 2^(2+2^(n-2))             for n>=5.    (2)
```

Indeed, doubling the exponent and subtracting two maps
`2+2^(n-2)` exactly to `2+2^(n-1)`.

## 2. Comparison with the actual strip

For odd `j`,

```text
q_j=(224*2^(j-1)+4)/3 < 2^(j+6).               (3)
```

Put `p=2+ceil(log_2(j+4))`.  Then

```text
2^(p-2)>=j+4,
2+2^(p-2)>=j+6.
```

Equations (2)--(3) give

```text
B_p>=2^(j+6)>q_j.                              (4)
```

## 3. Recovery by rank p

The exact bases `j=1,3` already recover at rank four, below `p(j)=5`.
The member `j=5` recovers at rank five, below `p(j)=6`.  For `j>=7`, rank
five is stable and the round-eight stable-or-first-wall theorem applies.

Follow the negative stable loop.  If it recovers before rank `p`, the claim
is done.  Otherwise (4) implies

```text
B_p>q_j>q_j-(5p-16),
```

so the loop has met its first B-wall no later than rank `p`.  Round eight
proves every such first wall strictly positive, independently of carry
depth.  Therefore the first recovery rank is at most `p(j)`.

## 4. Boundary

The bound tends to infinity and so does not give a uniform rank, much less
rank 42 for every strip.  It is proved only on the actual K4,r9 odd family.
No all-orbit reduction, suffix persistence, or public antichain threshold
improvement follows.
