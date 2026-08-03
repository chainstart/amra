# Independent audit: projection-free multivariate moment no-go

Date: 2026-08-02

Verdict: **the rank lower bound, the Phi6 support counts, and all three
asymptotic exponents pass.  The no-go is valid only for explicit
full-support rank/reconstruction certificates measured by feature-space
dimension.  The union exponent is not an automatic cost of simultaneous
rowwise Hankel reconstruction.**

## 1. Rank lower bound

For a signed atomic row

```text
q=sum_(x in A) c_x[x],  |A|=r,
```

and `m` feature functions, the evaluation matrix `E` has shape `m by r`
and

```text
H_q = E diag(c_x) E^T.
```

Thus `rank(H_q)<=min(m,r)`.  A certificate whose conclusion is
`rank(H_q)=r` necessarily has `m>=r`.  In the rectangular version
`E_F diag(c_x) E_G^T`, both feature dimensions must be at least `r`.
This is an exact linear-algebra lower bound and is independent of signs,
feature degree and projection height.

It is a matrix-dimension statement.  It is not a lower bound on the length
of a tensor, circuit or formula that describes the matrix or proves its
rank.  For example, a Kronecker-factorized exponentially large matrix can
have a short symbolic determinant proof.

## 2. Phi6 counts

For `k=floor(d/2)`, each row

```text
Q_A=(1+Y) product_(i in A)(1-X_i+X_i^2)
```

has two choices for the Y exponent and three choices in each of the `k`
selected X coordinates.  Independent variables prevent collisions, so

```text
r=2*3^k.
```

In the union over all `k`-subsets `A`, an X digit vector occurs exactly
when at most `k` coordinates are nonzero, and each nonzero digit is 1 or 2.
Therefore

```text
R=2 sum_(s=0)^k binomial(d,s) 2^s.
```

The row count is `K=binomial(d,k)`.  Independent enumeration reproduced the
support formula for `2<=d<=10`, including `K=252`, `r=486`, `R=25170` at
`d=10`.

## 3. Exponent ledger

Normalize by `t=K^(9/5)`, equivalently `K=t^(5/9)`.  The central binomial
estimate gives

```text
log_2 K=d-o(d).
```

Consequently

```text
r=t^((5/18)log_2(3)+o(1))
 =t^(0.440267361311...+o(1)).
```

For `T_s=binomial(d,s)2^s`, the terms increase on `0<=s<=k`.  Hence the
truncated sum is between `T_k` and `(k+1)T_k`.  Since

```text
T_k=2^(d/2+O(1)) binomial(d,k)=2^(3d/2-o(d)),
```

we obtain

```text
R=t^(5/6+o(1)).
```

If all `K` full-rank row matrices are charged separately, their dimensions
sum to

```text
K*r=t^(5/9+(5/18)log_2(3)+o(1))
   =t^(0.995822916867...+o(1)).
```

All limits and the finite convergence table were independently reproduced.

## 4. Mandatory scope restriction

Three different tasks must not be conflated.

1. **One row, full support rank.**  Matrix dimension is at least
   `r=2*3^k`.  This already rules out an explicit dense full-rank matrix
   whose dimension is polynomial in the displayed factor count.
2. **Many rows, rowwise full support rank.**  A single generic multivariate
   feature space can in principle be full rank on every row support.  The
   necessary dimension supplied by rank alone is `max_j |supp(Q_j)|=r`,
   not `R`.  Charging `K*r` also presupposes that the row matrices are stored
   or paid for separately.
3. **One aggregate reconstruction on the union.**  If scalar moments must
   distinguish every arbitrary signed coefficient vector on the `R` union
   atoms, the moment map must be injective and needs at least `R` independent
   scalar tests.  If only entries of an `m by m` symmetric moment matrix are
   exposed, the necessary condition is `m(m+1)/2>=R`.  The stronger
   full-union-rank demand requires `m>=R`.

Thus the displayed `R=t^(5/6+o(1))` ledger is correct for task 3, but it is
not forced by the simultaneous rowwise Hankel mechanism in task 2.  The
existing no-go artifact mostly states this distinction, but phrases such as
“common union dimension consumes the native U exponent” must be read as a
comparison for aggregate union reconstruction, not as a theorem about every
projection-free implementation of M1083-09.

Additional limitations are material:

- the injectivity lower bound concerns arbitrary weights on the union; the
  actual Phi6 rows form a highly restricted, compactly factorized family;
- displayed factor count is not the same as support/coefficient or circuit
  complexity of `B`;
- the Phi6 family is an abstract common-divisor obstruction and is not proved
  to satisfy the actual scalar-copy, positivity and Euclidean interfaces;
- rank or certificate size is not the closure contract's exponent-changing
  quantity, namely distinct Euclidean distance labels.

Accordingly the audit accepts the narrow no-go and rejects any broader claim
that all polynomial-size projection-free multivariate certificates are
impossible, or that the `5/6` union cost applies automatically to the actual
exact-block hub.

## 5. Closure decision

No distance-label inequality, fixed gain over the dimension-three `3/5`
exponent, or public-problem conclusion follows.  Promotion remains rejected.
The legal surviving target is a compact low-order multivariate invariant
coupled directly to scalar-copy/positivity geometry or to a ruled-locus
distance theorem, rather than full atom reconstruction.

Reproduction used 512 MiB / 120 second guards for both the author checker and
the independent checker.  Both completed in under one second; no Lean process
was started.
