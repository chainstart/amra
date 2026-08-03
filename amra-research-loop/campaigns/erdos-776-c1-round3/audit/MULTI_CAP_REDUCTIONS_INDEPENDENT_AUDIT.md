# Independent audit: multi-cap carry-cell reductions

## Verdict

QUALIFIED PASS.

The complement identities, exact carry-cell coordinates, top-threshold
equivalence, actual-legality bound `s>=3`, infinite `s=1` counterfamily,
fixed-cell differences, interval/five-endpoint reduction, stronger upstream
gap `A>=a+s`, and top-only sufficient branch all reconstruct independently.

The “gamma3-wall and sharp change at s=2” subsection of
`MULTI_CAP_DISCRETE_CONVEXITY_REDUCTION.md` contains an algebraic error.  For
its proposed extension `r=a+s+1,e=a-s`, the asserted
`beta=C(r,2)-1` holds only for `s=1`.  The correct identity is

```text
beta=C(r,2)-1+s(s-1).
```

Thus every `s>=2` member already violates `beta<=C(r,2)`.  The stated
downstream `tau`, `p`, stable-top and `gamma4` formulas for that extension
cannot be used as proved reductions.  This error does not invalidate the
earlier cell lemmas, the five-endpoint reduction, the stronger `A>=a+s`
gap, or the conditional decisive lemma.

The relaxed carry theorem for all `s>=2` remains conjectural.  The reproduced
finite absence of failures for `s=2,3` is not an absence proof, and the public
Erdos-776 status is unchanged.

The verifier is independent of the author boundary-cell checker and rebuilds
all quantities from Macaulay canonical words.

## 1. Canonical-word and complement identities

For a positive integer `N`, write its rank-two Macaulay word uniquely as

```text
N=C(a,2)+e, 0<=e<a,
```

so `U2(N)=C(a,3)+C(e,2)`.  With `s=k-1`, `u=r+s`, and

```text
alpha=C(a,2)+e,
tau=C(r,2)-alpha+1,
beta=alpha+sr+C(s,2)-1,
```

the independent reconstruction gives exactly

```text
beta-alpha=Delta_s(r)=sr+C(s,2)-1.
```

Writing `beta=C(A,2)+E` yields the exact upstream carry interval and
`E=e+K`, where

```text
K=Delta_s(r)+C(a,2)-C(A,2).
```

Substitution into the Macaulay raises gives

```text
p=C(a+1,3)+C(e+1,2)-C(r,2),
v=C(A,3)+C(E,2)-C(r,2)+C(a,2)+e-1.
```

The latter is equivalent to the alternative expression using `u`, because
`tau=C(u,2)-beta`.

If `c=top_3(p)` and `d=top_3(v)`, then

```text
1<=rho=C(c+1,3)-p<=C(c,2),
1<=sigma=C(d+1,3)-v<=C(d,2).
```

Direct subtraction gives the displayed cap-sum identity for `v-p`.  These
are exact identities, not finite observations.

## 2. Exact top threshold

For fixed `a,c`, the function

```text
D -> C(D,4)-C(c+1,4)
```

is strictly increasing for `D>=c+2`.  Hence, with `D(a,c)` defined as in the
certificate, the multi-cap inequality is equivalent to

```text
d>=D(a,c),
v>=C(D(a,c),3),
C(A,3)+C(E,2)-tau>=C(D(a,c),3).
```

The first equivalence uses the definition of `D`; the second is precisely
the defining top-index interval `C(d,3)<=v<C(d+1,3)`.  This reduction is
proved, while the final inequality is the still-unproved target.

## 3. Actual legality and the sharp s=1 obstruction

From

```text
2h=sq+C(s,2)+2-r
```

one obtains:

- `s=1`: `q=2h-2+r`, hence `q+2>h`;
- `s=2`: `q=h+(r-3)/2`, hence `q+3=h+(r+3)/2>h` for actual positive `r`.

Both contradict the required `q+s+1<h`.  Therefore actual legality implies
`s>=3`.  This is a necessary condition only; it does not make every
`s>=3` relaxed tuple legal.

For every `a>=6`, the independent checker substitutes

```text
s=1, r=a+2, e=a-1
```

and obtains the claimed words, `c=a`, `d=a+1`, `gamma3=-2`, and
`gamma4=-a-3`.  The multi-cap margin is exactly `-C(a+1,3)`.  The top-index
claims follow for all `a>=6` because the excesses above `C(a,3)` and
`C(a+1,3)` are nonnegative at `a=6` and increase, while remaining below the
next binomial gaps.  Thus this is an infinite symbolic counterfamily to the
`s=1` relaxation, not merely a sampled family.

## 4. Fixed-cell differences and endpoint reduction

Fix `r,s,a,A`.  Inside this `A` carry cell, `E=e+K`.  Direct finite
difference gives

```text
p(e+1)-p(e)=e+1,
v(e+1)-v(e)=E+1,
gamma4(e+1)-gamma4(e)=K.
```

Thus `p,v` are strictly increasing on the cell and `gamma4` is affine.  For
fixed `c`, every listed feasibility condition is an integer interval:
linear word/cap conditions, monotone preimages for `p` and `v`, and an affine
half-line for `gamma4`.  Their intersection is therefore an integer interval
`I`.  Since `v` is increasing, its threshold holds throughout `I` exactly
when it holds at `e0=min I`.

The lower endpoint of the intersection must be supplied by at least one of:

1. `e=0`;
2. `E=0`;
3. first entry into the fixed `p` top cell;
4. first point with `v>=1`;
5. for `K<0`, first point with `gamma4<=-1`.

All other displayed constraints are upper endpoints.  Integer overshoot at
cases 3--5 must still be retained.  This proves the five-family reduction;
it does not prove any of the five endpoint inequalities.

The checker guards 215,574 reconstructed carry states, 198,810 same-`A`
difference pairs and 3,876 nonempty fixed cells.  Those bounded checks are
implementation evidence; the interval proof above is all-parameter.

## 5. Strong upstream gap and top-only branch

For `s>=2`, `beta>alpha` and `beta<=C(r,2)` imply `r>a`, hence
`r>=a+1`.  Therefore

```text
Delta>=sa+C(s,2)+s-1.
```

If `A<=a+s-1`, strict canonical caps instead give

```text
Delta=beta-alpha
 < C(A+1,2)-C(a,2)
 <=C(a+s,2)-C(a,2)
 =sa+C(s,2).
```

Since `s-1>=1`, these inequalities contradict each other.  The strict
direction is correct, and

```text
A>=a+s.
```

Actual `s>=3` consequently gives `A>=a+3`.

The canonical cap bounds also give

```text
v-p=U2(beta)-U2(alpha)-1
   >=C(A,3)-C(a+1,3).
```

Together with `p>=C(c,3)`, this proves the stated top-only lower bound for
`v`.  Hence all cells with `A>=A_*(a,c)` close, and any remaining candidate
must lie in

```text
a+s<=A<A_*(a,c).
```

The input-side test is also correct: if its left side reaches
`C(A_*,2)`, then `beta>=C(A_*,2)`, forcing the top index `A>=A_*`.

## 6. Refuted gamma3-wall subsection

The proposed continuation sets

```text
r=a+s+1, e=a-s,
alpha=C(a+1,2)-s.
```

Using the already proved complement increment gives, without approximation,

```text
beta=C(r,2)-1+s(s-1),
tau=as+(s^2+3s)/2+1,
p=C(a+1,3)-s(2a+1).
```

The document instead omits `s(s-1)` in `beta` and consequently gives
different `tau` and `p` formulas.  At the smallest concrete instance
`(a,s,r,e)=(2,2,5,0)`, the actual value is

```text
beta=11,
```

whereas `C(r,2)-1=9`.  More generally, for every `s>=2`,

```text
beta>C(r,2),
```

so this family violates `gamma3<0` before `gamma4` is relevant.  The claimed
stable-top margin and `gamma4` formula in that subsection are therefore not
valid consequences of the displayed family.  For `s=1`, the missing term is
zero and the genuine infinite counterfamily remains correct.

## 7. Finite evidence and remaining obligation

The independent checker reproduces exactly the bounded relaxed scan through
`r=180,s=8`:

- `s=1`: 876,058 admissible, 750,926 failures;
- `s=2`: 158,658 admissible, zero observed failures;
- `s=3`: 17,085 admissible, zero observed failures;
- `s=4,...,8`: no admissible state within that cutoff.

This says nothing about unsearched parameters.  In particular, it does not
prove the relaxed `s>=2` carry theorem or the actual dyadic theorem.

The remaining analytic task is a uniform proof of the five endpoint
inequalities inside `a+s<=A<A_*(a,c)`, followed by the other campaign
branches and the public antichain interface.  No public status or main term
changes here.

No Lean was used.  Reproduction was bounded by 3 GiB and 180 seconds.

