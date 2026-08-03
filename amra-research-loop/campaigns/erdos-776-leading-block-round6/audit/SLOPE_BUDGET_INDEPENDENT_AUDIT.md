# Independent audit: affine slope budget

Auditor: root, independently reconstructing the three-line elimination.

For integer lower digit `A`, `C(A+1,2)=A(A+1)/2>=0`.  Substitution of
`C(B,2)=B_next+alpha*q+beta` into the stated surplus and use of
`B_next<q-c_n` independently gives

```text
gamma < (alpha+delta-3)q+(beta+v+2-c_n).
```

All coefficients except `q` are fixed for the proposed switch.  Since the
actual odd-strip subsequence is unbounded, `alpha+delta<3` makes the right
side strictly negative eventually.  Thus `alpha+delta>=3` is necessary for
an affine switch that remains nonnegative on arbitrarily late actual strips
and has the claimed canonical continuation.

The author statement passes after explicitly recording that `A,B` are
integer digits.  The audit rejects any sufficiency reading: it constructs no
legal Macaulay transition, says nothing decisive at equality, and supplies
no suffix persistence or public composition theorem.  Priority is uncertain.
