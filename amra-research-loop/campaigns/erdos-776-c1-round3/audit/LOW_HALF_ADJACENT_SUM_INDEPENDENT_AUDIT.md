# Independent audit: low-half adjacent-sum kernel

Verdict: **pass**.  The theorem

```text
B(a,c) >= A_*(a,c),       a>=3, 3<=c, 2c<a,
```

reconstructs from the original integer definitions.  Combined with the
separately audited high-half theorem, this closes the full two-variable kernel.
The conclusion remains scoped to the relaxed `s>=3` multi-cap branch and does
not promote the public Erdos-776 statement.

## 1. Uniform B-side lower bound

For `2c<a`,

```text
Delta = C(a+1,3)-C(c+1,3)
      > (a^3-a)/6-a^3/48
      = (7a^3-8a)/48
      >= a^3/8.
```

The last inequality is `a(a^2-8)>=0`, valid for integer `a>=3`.  If
`rho_p<=a^(3/2)/2`, then `C(rho_p,2)<rho_p^2/2<=a^3/8<Delta`, contradicting
the strict defining inequality.  Therefore `rho>=rho_p>a^(3/2)/2` with the
strict sign intact.

For `a>=2401`, let `t=floor(4sqrt(a)/3)`.  The exact rank-two increment obeys

```text
C(a+t,2)-C(a,2) = at+C(t,2)
 <= (4/3)a^(3/2)+(8/9)a
 <= (3/2)a^(3/2)
 < 3rho+2.
```

The middle inequality only needs `sqrt(a)>=16/3`.  Thus `B>=a+t`.  Also
`t-1>=4sqrt(a)/3-2>=7sqrt(a)/6` because `sqrt(a)>=49>12`.  Pascal summation
then gives

```text
C(B,3)-C(a+1,3)
 >= (t-1)C(a+1,2)
 >= (7/12)a^(5/2).
```

No real-to-integer direction is reversed here.

## 2. Chamber `c<=a^(3/4)`

Let `R4=C(c+1,4)+C(a+1,3)`, `x=(24R4)^(1/4)`, and
`d0=3+ceil(x)`.  The candidate is in the required domain `d0>=c+2`:

```text
24R4 >= (c+1)c(c-1)(c-2) > (c-2)^4,
```

so `ceil(x)>=c-1`.  Moreover

```text
C(d0,4)>=(d0-3)^4/24>=R4,
```

hence `D<=d0`.  In this chamber `R4<=5a^3/24`; using
`5^(1/4)<3/2`, `ceil(x)<x+1`, and `a^(3/4)>=343>40` gives

```text
D < (8/5)a^(3/4),
C(D,3)-C(c,3) < (256/375)a^(9/4).
```

The B-side dominates because `a^(1/4)>=7` and
`49/12>256/375`.

## 3. Chamber `c>a^(3/4)`

Set `q=ceil(C(a+1,3)/C(c+1,3))` and `R=(a/c)^3`.  The adjacent fourth-rank
sum gives `D<=c+1+q`.  Since `c>=3`,

```text
C(a+1,3)/C(c+1,3)
 = (a^3-a)/(c^3-c) < (9/8)R.
```

Here `R>8` follows from `2c<a`, while `R<c` follows from
`c>a^(3/4)`.  Therefore the ceiling strictness is

```text
q+1 < (9/8)R+2 < (11/8)R,
D < c+(11/8)R < (19/8)c.
```

The right adjacent sum has at most `q+1` terms, each below `D^2/2`, so

```text
C(D,3)-C(c,3)
 < (q+1)D^2/2
 < (3971/1024)a^3/c
 < (3971/1024)a^(9/4).
```

The coefficient is exact: `3971=11*19^2`.  The B-side dominates because
`49/12>3971/1024`.  Thus the infinite tail `a>=2401` is proved without a
finite extrapolation.

## 4. Independent exact finite base

The independent verifier imports no author code.  It uses a predecessor-top
formula for the triangular thresholds and fresh binary searches for `D` and
`A_*`.  Under the 3-GiB/180-second wrapper it exhausts

```text
3<=a<=2400, 3<=c, 2c<a
```

and independently computes the pair count as

```text
sum_{a=3}^{2400} max(0,floor((a-1)/2)-2) = 1,434,006.
```

It finds zero failures and the lexicographically first minimum

```text
(gap,a,c,rho,D,B,A_*)=(0,8,3,14,9,12,12).
```

The author verifier also passes.  Its final guard
`2401**0.75` uses a floating-point value, but this is not a proof dependency:
the independent audit replaces it by the exact identities
`2401=7^4`, `2401^3=343^4`, and `343>40`.

## 5. Scope consequence

This audit supports changing the scoped base-retaining rank-five decisive
lemma from `conditional` to `proved`: the prior reduction gives `A>=B`, the
high- and low-half theorems give `B>=A_*`, and the audited top-only implication
then gives the required multi-cap inequality.  It does not settle the separate
`(--)->(++)` branch, seed/suffix composition, or the public problem.

Artifact SHA-256:

- author note: `cca74f4b51833676868efa2af6f468823adfc018741f5741ede1b99cf959143c`
- author JSON: `837abd0384ab1a269b01ce77b7fd2f19bc914816b2998a4f1dbbe725b5799533`
- author verifier: `e595f86910712637140349b7af9c44f7b24b077bd2543d089e33439e6b744595`
- independent verifier: `b66e1b0352bbbc4e25cbc1b8d0268bedf6a2222b3e1b6dd7caad72dbb541f040`
- independent JSON: `2e3d98fba578cf744cf6fac0c757968a9229386b30163402746bc8775a8557aa`

