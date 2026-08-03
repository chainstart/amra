# Gamma-four feedback collapses the multi-cap residual to two variables

## Scope and verdict

This note gives an exact reduction for the relaxed multi-cap chamber with
`s>=3`.  It does not use the dyadic congruence and is therefore also valid for
every actual legal state.  The reduction is proved; the final two-variable
binomial inequality stated below is still a conjectural kernel.  A bounded
check is evidence for that kernel, not an infinite proof.

Use the notation of `MULTI_CAP_DISCRETE_CONVEXITY_REDUCTION.md`:

```text
alpha = C(a,2)+e,             0 <= e < a,
beta  = alpha+sr+C(s,2)-1 = C(A,2)+E,   0 <= E < A,
p     = C(a+1,3)+C(e+1,2)-C(r,2),
v     = C(A,3)+C(E,2)-C(r,2)+C(a,2)+e-1.
```

Assume `p,v>0`, `beta<=C(r,2)`, `gamma4=v-p-C(r,2)<=-1`, and `s>=3`.
Let `c=top_3(p)`, let `D(a,c)` be the least `D>=c+2` satisfying

```text
C(D,4)-C(c+1,4) >= C(a+1,3),
```

and let `A_*(a,c)` be the least `T>=a+2` satisfying

```text
C(c,3)+C(T,3)-C(a+1,3) >= C(D(a,c),3).
```

The already audited upstream carry gap gives `A>=a+s`.

## 1. Feedback from gamma4

Direct cancellation gives

```text
gamma4 = C(A,3)-C(a+1,3)+C(E,2)-C(e,2)+C(a,2)-1-C(r,2).
```

Thus `gamma4<=-1` implies

```text
C(r,2) >= C(A,3)-C(a+1,3)+C(E,2)-C(e,2)+C(a,2).
```

Because `E>=0`, `e<=a-1`, and `A>=a+s`,

```text
C(r,2) >= C(a+s,3)-C(a+1,3)+a-1.
```

For every `s>=3` the right side is at least its value at `s=3`, namely

```text
C(r,2) >= (a+1)^2+a-1 = a^2+3a.                 (G)
```

This is the missing feedback in the earlier top-only estimate: fake cells
with `r` only just above `a` cannot satisfy `gamma4<0`.

## 2. A second lower bound from the p-cell

Since `c=top_3(p)`, one has `p<C(c+1,3)`.  The exact formula for `p` gives

```text
C(r,2) > C(a+1,3)-C(c+1,3).                     (P)
```

Define `rho(a,c)` as the least integer `r` satisfying both (G) and (P).
Equivalently,

```text
rho(a,c) = max(
  min {r : C(r,2) >= a^2+3a},
  min {r : C(r,2) > C(a+1,3)-C(c+1,3)}).
```

Finally define

```text
B(a,c) = top_2(C(a,2)+3*rho(a,c)+2).
```

Indeed `s>=3`, `e>=0`, and `r>=rho(a,c)` imply

```text
beta >= C(a,2)+3*rho(a,c)+2,
```

so monotonicity of the rank-two top index proves `A>=B(a,c)`.

## 3. Exact remaining kernel

Consequently, the following pure two-variable statement closes every relaxed
`s>=3` multi-cap cell:

> For all integers `a>=2` and `3<=c<=a`, `B(a,c)>=A_*(a,c)`.

There are no longer any variables `r,s,e,E`, no actual-state residue, and no
endpoint type in this kernel.  If it is proved, then `A>=A_*`, the audited
top-only branch gives `v>=C(D(a,c),3)`, and hence the desired cap inequality.

The accompanying independent checker verifies the proved identities on exact
relaxed states and tests the two-variable kernel on a declared finite box.
Finite success must not be promoted to a theorem.

## 4. Next proof attempt

Pascal's identity rewrites both implicit thresholds as adjacent interval sums:

```text
C(D,4)-C(c+1,4) = sum_{i=c+1}^{D-1} C(i,3),
C(B,3)-C(a+1,3) = sum_{i=a+1}^{B-1} C(i,2),
C(D,3)-C(c,3)   = sum_{i=c}^{D-1} C(i,2).
```

Thus `D` is the first right endpoint for which the first consecutive sum is
at least `C(a+1,3)`, and the kernel asks that the second consecutive sum
dominate the third.  This is the useful form for an induction in `a` or in the
deficit `a-c`; it removes all top-index notation except `B`.

There is also an explicit, search-free upper certificate.  Put

```text
q0 = ceil(C(a+1,3)/C(c+1,3)),   D0=c+1+q0.
```

The first displayed sum contains `q0` terms, each at least `C(c+1,3)`, so
`D<=D0`.  It is consequently sufficient to prove

```text
C(c,3)+C(B,3)-C(a+1,3) >= C(D0,3).              (Q)
```

On the high-half chamber `2c>=a`, `q0<=9`; hence (Q) has only nine polynomial
subchambers after the ceiling is replaced by adjacent inequalities.  The
The coarse certificate (Q) itself fails at 13 small pairs, all with `a<=16`,
although the exact kernel succeeds there.  Nevertheless the entire high-half
chamber can be closed by a finite exact base and nine polynomial branches.

## 5. Infinite closure of the high-half chamber

First, (G) alone implies `B>=a+4`.  Indeed, if `rho=rho(a,c)`, then
`C(rho,2)>=a^2+3a`.  If `3rho<=4a+3`, then

```text
C(rho,2) <= ((4a+3)/3)((4a+3)/3-1)/2 < a^2+3a,
```

a contradiction.  Hence `3rho>=4a+4`, and

```text
C(a,2)+3rho+2 >= C(a,2)+4a+6 = C(a+4,2).
```

Now assume `2c>=a` and put `q=q0`.  The comparison

```text
9 C(c+1,3)-C(a+1,3) >= 9 C(c+1,3)-C(2c+1,3)
                         = c(c^2-7)/6 >= 0
```

shows `1<=q<=9`.  Since `B>=a+4`, (Q) follows from

```text
E_q(a,c) = C(c,3)+C(a+4,3)-C(a+1,3)-C(c+q+1,3) >= 0.   (E)
```

For `q=1`, the defining upper inequality forces `c=a`.  For `q=2`, the
defining strict lower inequality forces `c<=a-1`, and direct factorization
gives

```text
6 E_2 = 9(a-c+1)(a+c+2) > 0.
```

For `q=3,...,8`, use `(q-1)C(c+1,3)<C(a+1,3)`.  The following table gives a
rational `lambda`.  For `a>=69`, the displayed nonnegative domain polynomial
proves `c<=lambda*a`; since `E_q` decreases with `c`, the final polynomial is
a lower bound for `E_q(a,c)`.

| q | lambda | 6 times domain margin | lower bound for E_q |
|---|---:|---:|---:|
| 3 | 4/5 | `3a(a-5)(a+5)/125` | `a(11a+65)/50` |
| 4 | 7/10 | `a(29a^2-1100)/1000` | `(11a^2-30a-240)/40` |
| 5 | 2/3 | `5a(a-3)(a+3)/27` | `(a^2-21a-96)/6` |
| 6 | 3/5 | `2a(a-5)(a+5)/25` | `(6a^2-150a-775)/25` |
| 7 | 14/25 | `a(839a^2-36875)/15625` | `(307a^2-11175a-65000)/1250` |
| 8 | 8/15 | `a(209a^2-9225)/3375` | `(11a^2-615a-4000)/50` |

Here the domain margin is

```text
(q-1)(lambda*a+1)(lambda*a)(lambda*a-1)
 -(a+1)a(a-1).
```

All entries in the last two columns are positive at `a=69` and increasing
thereafter.  This proves (E) for `q=3,...,8`.

For `q=9`, the strict lower inequality is
`8C(c+1,3)<C(a+1,3)`.  Together with `2c>=a`, direct substitution at the least
integer strictly above `a/2` shows that this is possible only when `a` is even
and `c=a/2`.  Then

```text
E_9(a,a/2) = (a^2-62a-464)/4 >= 0
```

for the first possible `a>=69`, namely even `a>=70`.

The finite base `3<=a<=68`, `max(3,ceil(a/2))<=c<=a` is checked by exact integer
evaluation of the original `D`, `A_*`, and `B`, not by the coarse `D0`
certificate.  It has 1,219 pairs and no kernel failure.  Therefore

> `B(a,c)>=A_*(a,c)` for every `a>=3` and `2c>=a`.

This is an infinite partial theorem.  It reduces the unresolved two-variable
kernel to the strict low-half chamber `2c<a`.

## 6. A fourth-root certificate for the low-half chamber

Put

```text
X=(c+1)^4+4(a+1)^3,
L=max(c+2, 3+ceil(X^(1/4))).
```

This is another search-free upper bound for `D`.  Indeed,

```text
C(L,4)       >= (L-3)^4/24,
C(c+1,4)     <= (c+1)^4/24,
C(a+1,3)     <= (a+1)^3/6,
```

so the definition of `L` gives
`C(L,4)-C(c+1,4)>=C(a+1,3)`, hence `D<=L`.  Therefore the low-half kernel
would follow from the explicit inequality

```text
C(c,3)+C(B(a,c),3)-C(a+1,3) >= C(L,3).          (R)
```

The independent bounded guard through `a=1000` finds that (R) fails only at

```text
(a,c)=(7,3),(8,3),(9,3),(9,4),(10,3),(10,4).
```

The exact kernel succeeds at all six points, and (R) succeeds at every tested
low-half pair with `a>=11`.  This is not an infinite proof of eventual
success.  It does, however, replace the requested vague “fourth-root-scale
bound” by a precise integer certificate.  The remaining task is now to combine
the p-branch inequality

```text
C(rho,2)>C(a+1,3)-C(c+1,3)
```

and the definition of `B` with (R), ideally after raising away the single
fourth root.  Only the six displayed exact base cases should then remain.

The most economical next step is therefore:

1. prove the explicit low-half inequality (R) for `a>=11` by pairing its
   fourth-root bound with the p-branch lower bound on `rho`;
2. avoid returning to five endpoint types, since gamma-four feedback has
   already eliminated all lower canonical digits from the unresolved part.

Update: `LOW_HALF_ADJACENT_SUM_KERNEL.md` subsequently proves the entire
strict low-half chamber by a sharper quartic-root/adjacent-step split and an
exact finite base.  Thus the open status in this section is superseded.
