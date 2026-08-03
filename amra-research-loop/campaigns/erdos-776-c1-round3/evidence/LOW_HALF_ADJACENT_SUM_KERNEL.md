# Erdos-776: low-half adjacent-sum kernel

Date: 2026-08-03

Status: **proved for every integer `a>=3, 3<=c<=a` with `2c<a`**.

Scope: this closes the strict low-half part of the two-variable kernel in
`MULTI_CAP_GAMMA4_FEEDBACK_REDUCTION.md`.  Together with that note's audited
high-half theorem it proves `B(a,c)>=A_*(a,c)` for the full two-variable
kernel.  It does not by itself close the actual dyadic theorem or public
Erdos-776 statement; the upstream reduction applies to the relaxed `s>=3`
multi-cap branch.

## 1. Definitions and adjacent-sum target

Let

```text
Delta = C(a+1,3)-C(c+1,3),
rho_p = min {r: C(r,2)>Delta},
rho   = max(rho_p, min {r: C(r,2)>=a^2+3a}),
B     = top_2(C(a,2)+3rho+2).
```

Let `D` be the least integer `D>=c+2` satisfying

```text
C(D,4)-C(c+1,4)>=C(a+1,3).
```

It suffices to prove

```text
C(B,3)-C(a+1,3) >= C(D,3)-C(c,3).              (1)
```

Indeed, (1) is exactly the defining inequality for `B>=A_*(a,c)` after
moving `C(c,3)` to the left.  Both sides are consecutive adjacent sums.

## 2. Uniform lower bound for the B-side

Assume `2c<a`.  Since `c<a/2` and `a>=3`,

```text
Delta > (a^3-a)/6-a^3/48
      = (7a^3-8a)/48
      >= a^3/8.
```

The strict triangular inequality for `rho_p` implies

```text
rho >= rho_p > a^(3/2)/2.                       (2)
```

For `a>=2401`, put `t=floor(4sqrt(a)/3)`.  Then

```text
C(a+t,2)-C(a,2)
 <= (4/3)a^(3/2)+(8/9)a
 <= (3/2)a^(3/2)
 < 3rho+2.
```

Therefore `B>=a+t`.  Since `sqrt(a)>=49>12`,

```text
t-1 >= (4/3)sqrt(a)-2 >= (7/6)sqrt(a).
```

The left side of (1) consequently satisfies

```text
C(B,3)-C(a+1,3)
 >= (t-1) C(a+1,2)
 >= (7/12) a^(5/2).                             (3)
```

## 3. Fourth-root chamber: c<=a^(3/4)

Put

```text
R4=C(c+1,4)+C(a+1,3),
d0=3+ceil((24R4)^(1/4)).
```

Because `C(d0,4)>=(d0-3)^4/24>=R4`, this is a search-free quartic-root
certificate

```text
D<=d0.                                           (4)
```

It also sharpens the earlier certificate `D<=h+3`, where
`h=ceil(((c+1)^4+4(a+1)^3)^(1/4))`, because the quantity `24R4` under the
present fourth root is at most that earlier radicand.

If `c<=a^(3/4)`, then

```text
R4 <= c^4/24+a^3/6 <= 5a^3/24.
```

Using `5^(1/4)<3/2` and `a^(3/4)>=343` at `a>=2401`, (4) gives

```text
D < 4+(3/2)a^(3/4) < (8/5)a^(3/4).
```

Hence

```text
C(D,3)-C(c,3)
 < D^3/6
 < (256/375)a^(9/4).                            (5)
```

Since `a^(1/4)>=7`, the bound (3) is larger than (5).

## 4. Adjacent-step chamber: c>a^(3/4)

Set

```text
q=ceil(C(a+1,3)/C(c+1,3)).
```

The adjacent fourth-binomial sum gives `D<=c+1+q`.  Write
`R=(a/c)^3`.  Since `c>=3`,

```text
C(a+1,3)/C(c+1,3)
 = (a^3-a)/(c^3-c)
 < (9/8)R.
```

Also `c<a/2` gives `R>8`, while `c>a^(3/4)` gives `R<c`.  Therefore

```text
q+1 < (9/8)R+2 < (11/8)R,
D < c+(11/8)R < (19/8)c.                        (6)
```

There are at most `q+1` terms in the right adjacent sum of (1), and every
term is below `D^2/2`.  Thus (6) yields

```text
C(D,3)-C(c,3)
 < (3971/1024) a^3/c
 < (3971/1024) a^(9/4).                         (7)
```

At `a>=2401`, (3) dominates (7), because

```text
(7/12)a^(1/4) >= 49/12 > 3971/1024.
```

This proves (1) analytically for every low-half pair with `a>=2401`.

## 5. Exact finite base

An independent integer verifier checks the original definitions of `rho`,
`B`, `D`, and `A_*`, using binary searches rather than either analytic
majorant.  On

```text
3<=a<=2400,  3<=c,  2c<a,
```

it checks 1,434,006 pairs and finds no failure.  The minimum gap is zero,
first attained at

```text
(a,c,rho,D,B,A_*)=(8,3,14,9,12,12).
```

Combining the finite base with Sections 2--4 proves

```text
B(a,c)>=A_*(a,c)
```

for the entire strict low-half chamber.  No finite observation is used for
the infinite tail.
