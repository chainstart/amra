# OPG K5-e cross edge: full `b`-elimination handoff

This is an exploratory handoff, not an audited campaign theorem.

In the full five-variable marked-`03` stabilizer model, both `P` and `xi` are
linear in the singleton-orbit variable `b`.  Write

```text
P=A_b b+C_b,  xi=D_b b+E_b.
```

Exact elimination gives

```text
A_b E_b-D_b C_b = 2 a^2 R(a,c,d,e),
```

where `R` has total degree 10, 41 terms, and every coefficient is a positive
integer.  Consequently this determinant is nonnegative on the nonnegative
orthant and is strict when `a,c,d,e>0`.  Its three audited restrictions are

```text
c=d=e=1:  2a^2(120a^2+48a+5),
a=d=e=1:  2(80c^2+75c+18),
a=c=d=1:  2(44e^3+94e^2+32e+3).
```

This confirms that the three slice certificates are restrictions of one
four-variable determinant.  It does **not** prove positivity on the complete
real distinguished component: negative `c,d,e` can invalidate the
positive-coefficient argument, and the full `A_b=0` barrier topology is not
classified.  The next campaign should study whether the anchor component
forces a sign chamber or admits a second elimination/SOS certificate for
`R`.

Reproduction: `verify_opg_k5_cross_full_b_elimination.py` under the standard
3 GiB / 180 second probe limits.
