# Discrete-convexity reduction for the relaxed multi-cap conjecture

## Status

This note does not close the relaxed `s>=2` conjecture.  It removes the
rank-two lower digit `e` from the interior of every carry cell: a failure, if
one exists, must occur at the first feasible integer point of an explicitly
listed boundary interval.  It also explains algebraically why the infinite
`s=1` counterfamily does not continue to `s=2` under `gamma4<0`.

No additional actual-state parameter scan is used here.

## Lemma 1: affine coordinates inside an upstream carry cell

Fix `r,s,a,A`, put

\[
 R=\binom r2,qquad
 \Delta=sr+\binom s2-1,
\]

and define

\[
 K=\Delta+\binom a2-\binom A2.
\]

If

\[
 \alpha=\binom a2+e,qquad
 \beta=\alpha+\Delta=\binom A2+E,
\]

then throughout the fixed `A` carry cell

\[
 \boxed{E=e+K},qquad 0\le e+K<A.
\]

The second-stage inputs are therefore the explicit functions

\[
 p(e)=\binom{a+1}3+\binom{e+1}2-R,
\]

\[
 v(e)=\binom A3+\binom{e+K}2-R+\binom a2+e-1.
\]

Both formulas follow by substituting
`tau=R-C(a,2)-e+1`.  They contain no Macaulay operator.

## Lemma 2: exact discrete differences

As long as `e` and `e+1` remain in the same fixed `A` cell,

\[
 \boxed{p(e+1)-p(e)=e+1},
\]

\[
 \boxed{v(e+1)-v(e)=e+K+1=E+1>0},
\]

and

\[
 \boxed{\gamma_4(e+1)-\gamma_4(e)=K}.
\]

The last identity also follows from

\[
 U_2(\beta)-U_2(\alpha)
 =\binom A3-\binom a3+\binom{e+K}2-\binom e2,
\]

whose dependence on `e` is affine with slope `K`.

Thus `p` and `v` are discretely convex and strictly increasing, while
`gamma4` is affine inside the cell.  This is the useful convexity statement;
no global monotonicity across an `A` carry is asserted.

## Lemma 3: every fixed `(a,A,c)` problem is an interval endpoint

Fix also a proposed `p` top index `c`.  The allowed integers `e` are exactly
the intersection of the following sets:

\[
 0\le e<a,
\]

\[
 0\le e+K<A,
\]

\[
 \binom c3\le p(e)<\binom{c+1}3,
\]

\[
 v(e)\ge1,
\]

\[
 \binom A2+e+K\le R,
\]

\[
 \gamma_4(e)=v(e)-p(e)-R\le-1.
\]

Each set is an integer interval:

- the first two and the `beta<=R` condition are linear intervals;
- the `p`-cell and `v>=1` conditions are intervals because `p,v` are
  strictly increasing;
- `gamma4<=-1` is an interval because `gamma4` is affine with slope `K`.

Hence their intersection `I(r,s,a,A,c)` is an integer interval.  If it is
nonempty, let

\[
 e_0=\min I(r,s,a,A,c).
\]

The exact desired threshold from the previous note is

\[
 H(a,c)=\binom{D(a,c)}3.
\]

It is constant on this cell, whereas `v(e)` is strictly increasing.
Therefore

\[
 \boxed{v(e)\ge H(a,c)\text{ for every }e\in I
 \iff v(e_0)\ge H(a,c).}
\]

This is a necessary-and-sufficient endpoint reduction, not merely a
sufficient estimate.

## Lemma 4: classification of the possible worst endpoints

Because `e_0` is the first integer in an intersection of intervals, at least
one lower boundary is active there.  Consequently every minimal
counterexample to the relaxed conjecture can be chosen in one of these
families:

1. `e=0`, the lower edge of the `alpha` word;
2. `E=e+K=0`, immediately after a rank-two carry of `beta`;
3. `p(e)>=C(c,3)` for the first time, equivalently the largest attainable
   `rho=C(c+1,3)-p` in that cell;
4. `v(e)>=1` for the first time;
5. when `K<0`, `gamma4(e)<=-1` for the first time.

If `K>=0`, the `gamma4` condition supplies an upper endpoint instead and
cannot create `e_0`.  Upper constraints such as `beta<=R` can kill a cell,
but cannot move its worst point away from the first feasible integer.

Thus the infinite search over lower canonical digits is reduced to five
auditable boundary families.  Rounding means “first time” need not be exact
equality; the overshoot is bounded by the displayed one-step differences
`e+1` or `E+1` and must be retained in a proof.

## Lemma 5: a stronger sufficient endpoint inequality

For any feasible endpoint, the exact target remains

\[
 v(e_0)\ge\binom{D(a,c)}3.
\]

A more elementary but stronger branch is obtained from

\[
 (d-c-1)\binom{c+1}3\ge\binom{a+1}3.
\]

It is enough to establish at the endpoint that

\[
 v(e_0)\ge
 \binom{c+1+m}3,
\]

where

\[
 m=\left\lceil
 \frac{\binom{a+1}3}{\binom{c+1}3}
 \right\rceil.
\]

Indeed this gives `d>=c+1+m`, hence `d-c-1>=m`.  This branch may be useful
for the `e=0` and `E=0` endpoints, but it is stronger than the exact
`D(a,c)` threshold and is not claimed universally.

## Lemma 6: two forced upstream carries and a top-only closure branch

The sign conditions already force two upstream rank-two carries when
`s>=2`.  Indeed `beta>alpha` and `beta<=R` imply `alpha<R`; since
`alpha>=C(a,2)`, this gives `r>a`.  Moreover

\[
 \Delta=sr+\binom s2-1\ge2r\ge2a+2.
\]

If `A<=a+1`, then

\[
 \Delta=\beta-\alpha
 <\binom{a+2}2-\binom a2=2a+1,
\]

a contradiction.  Hence

\[
 \boxed{A\ge a+2.}
\]

This is the precise structural feature absent from the `s=1`
counterfamily, where `A=a+1`.

There is also a useful top-only sufficient branch.  The strict canonical cap
bounds give

\[
 U_2(\beta)\ge\binom A3,qquad
 U_2(\alpha)\le\binom{a+1}3-1.
\]

Therefore

\[
 v-p=U_2(\beta)-U_2(\alpha)-1
 \ge\binom A3-\binom{a+1}3.
\]

Since `p>=C(c,3)`, it follows that

\[
 \boxed{v\ge
 \binom c3+\binom A3-\binom{a+1}3.}
\]

Define `A_*(a,c)` as the least integer `B>=a+2` such that

\[
 \binom c3+\binom B3-\binom{a+1}3
 \ge\binom{D(a,c)}3.
\]

Every cell with `A>=A_*(a,c)` is proved.  A purely input-side sufficient
test for this branch is

\[
 \boxed{\binom a2+sr+\binom s2-1
        \ge\binom{A_*(a,c)}2,}
\]

because `beta>=C(a,2)+Delta`.  Consequently any counterexample must satisfy
the simultaneous narrow-cell conditions

\[
 a+2\le A<A_*(a,c)
\]

and the failure of the displayed input-side test.  The lower digits are
needed only in these residual top cells; all larger upstream carries close
without using `E`, `rho`, or `sigma`.

## Retracted boundary model: audit correction

**The continuation below is retained only as an audit trail and is not a
proved calculation.**  Independent reconstruction gives
`beta=C(r,2)-1+s(s-1)`, not `C(r,2)-1`.  Therefore every `s>=2` member
already violates `beta<=C(r,2)`.  Its subsequent `tau`, `p`, stable-top,
margin and `gamma4` formulas are withdrawn outside `s=1`; none may be used
in the endpoint reduction or as evidence for the relaxed conjecture.

The retracted draft attempted to extend the known `s=1` counterfamily by
setting, for `a>=s`,

\[
 r=a+s+1,qquad e=a-s.
\]

It incorrectly asserted

\[
 \alpha=\binom{a+1}2-s,qquad
 \beta=\binom r2-1,
\]

The displayed `beta` identity is false for `s>=2`; the correct excess is
stated in the audit correction above.  The draft then recorded the following
withdrawn formulas:

\[
 \tau=as+\frac{3s^2+s}{2}+1,
\]

\[
 p=\binom{a+1}3-s(2a+s),
\]

where the second formula records `p` as a deficit from its next cap.  For
large enough `a`, its top indices are

\[
 c=a,qquad d=a+s.
\]

The multi-cap margin in that stable top cell is

\[
 \binom{a+s}4-\binom{a+1}4-\binom{a+1}3.
\]

It is negative for `s=1`, exactly zero for `s=2`, and positive for `s>=3`.
However the rank-four sign is

\[
 \gamma_4=
 \frac{3a^2(s-1)+3as^2-9a+s^3-6s^2-13s}{6}.
\]

In particular,

\[
 \gamma_4=-a-3\quad(s=1),
\]

but

\[
 \gamma_4=\frac{a^2+a-14}{2}>0\quad(s=2,\ a\ge4).
\]

This former conclusion is withdrawn.  The ansatz fails earlier at the
`gamma3` condition, so its putative `s=2` margin and `gamma4` values have no
standing.  The five valid endpoint branches above remain the complete open
task.

## Remaining proof obligation

After the reduction, the relaxed conjecture is equivalent to the following
five-branch endpoint statement:

> For `s>=2`, every nonempty cell `I(r,s,a,A,c)` has
> `v(e_0)>=C(D(a,c),3)`, where `e_0` lies on one of the five boundaries in
> Lemma 4.

The lower digits `e,E,rho,sigma` no longer range freely in the interior.
Lemma 6 removes every cell with `A>=A_*(a,c)`, and the independently checked
upstream-gap sharpening gives `A>=a+s`.  Thus only
`a+s<=A<A_*(a,c)` remains.
What is still missing is a uniform comparison between the quadratic
endpoint formula for `v(e_0)` and the implicitly defined fourth-binomial
threshold `D(a,c)`.  The likely order of attack is:

1. `E=0`, because both the upstream carry and `v` simplify maximally;
2. the first-`p` endpoint, retaining its one-step triangular overshoot;
3. the `K<0`, first-`gamma4` endpoint;
4. show `e=0` and first-`v` either reduce to the preceding branches or are
   empty under `s>=2` and `p>0`.

No finite absence claim is used to discharge any of these branches.
