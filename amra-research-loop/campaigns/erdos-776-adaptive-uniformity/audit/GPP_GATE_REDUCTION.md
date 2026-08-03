# Reduction of the `(++ -> ++)` gate

Let

```text
e = v-p = U_2(beta)-U_2(alpha)-1.
```

The previous audit reduced `gamma5 >= 0` to

```text
(G++)   e >= 0 and U_3(e) >= U_2(alpha)+1.
```

No counterexample to `(G++)` was found in the moving-boundary search recorded
in `evidence/GPP_MOVING_BOUNDARY_RESULT.json`.  The smallest margin remains
80,701 at `(j,q,k,r)=(6,2436,4,145)`.

## A rigorous further reduction

Write the degree-two Macaulay expansion as

```text
alpha = C(a,2)+s,       0 <= s < a.
```

Then

```text
U_2(alpha)=C(a,3)+C(s,2) < C(a+1,3).
```

In the target chamber `p>=0`, so

```text
U_2(alpha) >= tau-1.
```

For actual states `j>=2`, `h=112*2^(j-1)>=224`, `b>=5`, and
`tau=2h+b-2`.  Hence `U_2(alpha)>=450`.  If `a<=11`, however,
`U_2(alpha)<C(12,3)=220`, a contradiction.  Therefore

```text
a >= 12.                                                    (1)
```

For `a>=12`, direct cancellation gives

```text
C(a-1,4) >= C(a+1,3).
```

Consequently, if one can prove the simpler cubic increment bound

```text
e >= C(a-1,3),                                              (2)
```

then monotonicity and the strict cap above yield

```text
U_3(e) >= C(a-1,4)
       >= C(a+1,3)
       >= U_2(alpha)+1.
```

Thus `(1)+(2)` rigorously imply `(G++)`, and `(2)` also implies `e>=0`.

## Remaining chamber inequality

If also

```text
beta = C(b0,2)+t,       0 <= t < b0,
```

then the unresolved bound `(2)` is exactly

```text
C(b0,3)+C(t,2)-C(a,3)-C(s,2)-1 >= C(a-1,3).                (3)
```

The actual first-tail equation supplies

```text
C(b0,2)+t-C(a,2)-s
  = beta-alpha
  = (k-1)r+C(k-1,2)-1.                                    (4)
```

Equations `(3)-(4)`, together with the dyadic equation and the `gamma4<0`
upper wall, are the exact remaining cell problem.  I did not obtain a
universal derivation of `(3)` from those constraints.  Since no exact
counterexample was found, the honest status is a strict reduction rather than
a proof or disproof of `(G++)`.
