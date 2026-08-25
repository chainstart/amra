# Independent audit: Round 4 LTJ diagonal loss

## Verdict

**PASS at the stated scoped status.**  The author note proves the exact
aligned-loss recurrence and all-parameter diagonal domination on the actual
zero-seed orbits.  It also proves an all-parameter canonical-plateau no-go
for every positive propagated-loss bound that depends only on the diagonal
gap.  It does **not** prove LTJ, H1--H2, the rank-eight entry, or Erdős #776.

The surviving route is narrower after this audit: it must use actual-orbit
canonical position or effective suffix-separator data.

## Blind protocol and integrity

The blind reconstruction was frozen before the Round 4 evidence or verifier
was opened.  Its recorded SHA-256 verifies as

```text
f5be6adda2dba8f5521292ce5dff93891b09e61df1b60eba1e4cc86bb0690df7
```

The reconstruction independently identified the required sign checks, the
exact rank-four LTJ threshold, the plateau obstruction, and the strict scope
boundary.  Unblinding resolves its deliberately undefined notation as

```text
partial_q = KK_q,
U_q = the Macaulay upper adjoint,
S_q(x) = x + U_q(x),
x_q = E_q^(V),
y_(q+1) = E_(q+1)^(V+1).
```

## Exact recurrence and signs

At the aligned top rank `q=V-26`, both zero seeds vanish, so `L_q=0`.
Pascal's identity and the two adjacent orbit recurrences give exactly

```text
L_(q-1) = T_q + P_q,
T_q = U_(q-1)(V + partial_q(x_q)) - x_q - 1,
P_q = partial_(q+1)(S_q(x_q)) - partial_(q+1)(y_(q+1)).
```

For `h=floor(V/q)`, numerical-shadow subadditivity gives
`partial_q(x_q+h)<=partial_q(x_q)+V`.  Macaulay adjunction therefore gives
`T_q>=h-1>=0` throughout the actual range `5<=q<=V-26`.  If `L_q>=0`, then
`y_(q+1)<=S_q(x_q)` and monotonicity gives `P_q>=0`.  Downward induction is
therefore noncircular and proves

```text
E_(q+1)^(V+1) <= S_q(E_q^V).
```

No separator, LTJ assumption, or rank-six target cap enters this argument.

## LTJ threshold and boundary cases

With `B=B_2(V)=C(a,2)+b`, `0<=b<a`, and
`k=partial_3(Z_3(V))=B-V`, the adjacent condition is

```text
B_2(V+1) <= B+a
iff partial_3(Z_3(V+1)) <= k+a-1
iff Z_3(V+1) <= U_2(k+a-1).
```

Since `L_4=S_2(B)-Z_3(V+1)`, this is exactly

```text
L_4 >= S_2(B)-U_2(B-V+a-1).
```

The derivation includes `b=0` and plateau endpoints and has no off-by-one.
Diagonal domination supplies only `L_4>=0`; the right side above can be
positive, so the displayed equivalence is not a proof of LTJ.

## Plateau obstruction

For `q>=1`, `A>=q+2`, and `1<=L<=A-q-1`, put

```text
x=C(A-1,q),  S_q(x)=C(A,q+1),  y=S_q(x)-L.
```

The canonical expansion of `C(A,q)-1` gives

```text
U_q(C(A,q)-1)=C(A,q+1)-(A-q).
```

Adjunction and monotonicity then force
`partial_(q+1)(y)=C(A,q)=partial_(q+1)(S_q(x))`, so `P_q=0` although the
gap is positive.  The permitted plateau length is unbounded.  This refutes
gap-only strictly positive lower bounds, but says nothing about where the
actual zero-seed orbit lies inside its plateau.

## Reproduction and classification

Under the OpenMath memory guard, the Round 4 verifier returned `PASS`, checked
two full aligned recurrence instances and 2,114 plateau guards, and retained
the finite `125<=V<=2000` scan only as falsifier evidence.  The source hash was

```text
99855d134b004f06e1696cf11cf7648f2b54717b3be39d4fa6a60aae0e3f1c4b
```

Classification:

- actual diagonal domination: proved, all parameters in the stated orbit;
- gap-only propagated-loss mechanism: refuted, all parameters;
- exact LTJ threshold: proved as an equivalence only;
- LTJ, H1--H2, rank-eight entry, and exact `n_0(r)`: open;
- promotion: rejected; continue `survivor_deepening` with actual plateau
  position or suffix data.
