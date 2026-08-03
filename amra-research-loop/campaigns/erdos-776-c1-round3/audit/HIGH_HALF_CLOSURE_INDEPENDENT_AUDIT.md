# Independent audit: high-half two-variable kernel closure

Date: 2026-08-03

Verdict: **passed, with the finite-base domain explicitly corrected to 1,219
pairs**.

Scope: `B(a,c)>=A_*(a,c)` for integers `a>=3,3<=c<=a,2c>=a` in the
gamma-four feedback two-variable kernel.  This does not enlarge the upstream
relaxed `s>=3` scope.

## Integer B bound

From `C(rho,2)>=a^2+3a`, the assumption `3rho<=4a+3` would give

```text
C(rho,2) <= ((4a+3)/3)((4a+3)/3-1)/2
           = (8a^2+6a)/9 < a^2+3a.
```

Thus integer rounding gives `3rho>=4a+4`.  Consequently
`C(a,2)+3rho+2>=C(a+4,2)`, and the definition of `top_2` proves `B>=a+4`.

## q branches

For `q=ceil(C(a+1,3)/C(c+1,3))`, the high-half condition gives
`1<=q<=9`.  The certificate `D<=c+q+1` reduces the target to

```text
E_q=C(c,3)+C(a+4,3)-C(a+1,3)-C(c+q+1,3)>=0.
```

Independent expansion gives:

* `q=1` forces `c=a`, where `E_1=(a+1)(a+8)/2>0`.
* `q=2` gives `6E_2=9(a-c+1)(a+c+2)>0`.
* For `q=3,...,8`, the rational bounds are
  `4/5,7/10,2/3,3/5,14/25,8/15`.  In particular the `q=7` value is exactly
  `14/25`.  The verifier reconstructs every domain margin and lower-bound
  polynomial and checks positivity and monotonicity from `a=69` onward.

For `q=9`, parity is essential.  Write `a=2m` or `a=2m+1`.  At the least
high-half integer `c`,

```text
6(8C(m+2,3)-C(2m+2,3)) = 12m(m+1)>0       (a odd),
6(8C(m+2,3)-C(2m+1,3)) = 6m(4m+3)>0       (a even,c>=m+1).
```

Thus `q=9` is impossible there.  For even `a=2m,c=m`,

```text
6(C(2m+1,3)-8C(m+1,3))=6m>0,
```

so this is the only possible `q=9` chamber.  There
`E_9=(a^2-62a-464)/4`, positive from the first tail value `a=70` onward.

## Exact base

The correct base is

```text
3<=a<=68, max(3,ceil(a/2))<=c<=a.
```

It has 1,219 pairs.  Counting 1,221 would include the invalid `c=2` cases
for `a=3,4`.  Independent evaluation of the original `rho,B,D,A_*`
definitions finds no failure.  The high-half closure is valid after making
the domain explicit.

