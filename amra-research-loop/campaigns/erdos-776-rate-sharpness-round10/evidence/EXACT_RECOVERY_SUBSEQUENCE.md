# Exact logarithmic recovery subsequence

## Theorem

For every integer `R>=5`, define the odd actual index

```text
j_R=11*2^(R-4)-5.
```

The K4,r9 member at `j_R` has exact first recovery rank

```text
rho(j_R)=R+1.
```

Moreover round nine gives `p(j_R)=R+2`.  Hence its `O(log j)` upper rate is
asymptotically sharp, and is within one rank of the truth on this explicit
infinite subsequence.

## Stable negativity through R

The upper recurrence bound `B_(n+1)<B_n^2`, together with
`B_5=1625<2^11`, gives

```text
B_n<2^(11*2^(n-5)).                            (1)
```

Put `E_R=11*2^(R-4)`.  Since `j_R+5=E_R`, the exact strip formula gives

```text
q_(j_R)>2^(j_R+5)=2^E_R.                       (2)
```

Equations (1)--(2) imply `q_(j_R)>B_R^2`.  The constants increase, and
`B_R>=20R` makes `B_R^2>B_R+5R`.  Therefore every stable word through rank
`R` is strictly canonical.  Its surplus constant is less than `B_n^2`, so

```text
gamma_3,...,gamma_R<0.                         (3)
```

Thus `rho(j_R)>R`.

## Recovery at R+1

At rank `R+1`, if the B-tail has reached its first wall, round eight makes
the surplus strictly positive.  Otherwise the word is stable and

```text
gamma_(R+1)=D_(R+1)-4q_(j_R).
```

The ratio cone gives

```text
D_(R+1)=B_(R+2)-A_(R+2)-A_(R+1)-1
        >=(14/15)B_(R+2)-1.
```

Round nine supplies

```text
B_(R+2)>=2^(2+2^R),
q_(j_R)<2^(j_R+6)=2^(E_R+1).
```

Since `2^R=16*2^(R-4)`, the exponent advantage is

```text
(2+2^R)-(E_R+1)=1+5*2^(R-4)>=11.
```

Hence `B_(R+2)>2048q_(j_R)` and `D_(R+1)>4q_(j_R)`.  The stable alternative
also recovers strictly.  Together with (3), this proves `rho(j_R)=R+1`.

Finally `2^(R-1)<E_R-1<2^R`, so

```text
ceil(log2(j_R+4))=R,
p(j_R)=R+2.
```

This remains a sharp-rate theorem for one fixed actual family; it does not
give a rank-42, all-orbit, suffix, or public result.
