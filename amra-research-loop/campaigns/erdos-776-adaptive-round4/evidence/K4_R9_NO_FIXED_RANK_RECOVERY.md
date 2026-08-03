# K4,r9 has no uniform fixed recovery rank

## Theorem

For every fixed integer `R>=4`, there is an actual odd member of the K4,r9
dyadic family whose surpluses `gamma_3,...,gamma_R` are all strictly negative.

This refutes every proposed uniform fixed-rank recovery bound on this orbit,
including a uniform pre-rank-42 surplus seed obtained only by waiting along
the same orbit.  It does not itself refute the public antichain statement,
which may require a different construction or interface.

## Stable words

Let `q=(2h+4)/3`, `tau=4q-2`, and `H=5q/2`; odd `j` makes `q` even.  Define

```text
A_4=25, B_4=58,
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).
```

For each fixed `n>=4` and all sufficiently large actual `q`, the direct
rank-`n` words are

```text
x_n: (H,n), (q-1,n-1), (q-6,n-2), ...,
     (q-(5n-19),3), (q-(5n-15),2), (A_n,1),

y_n: (H+1,n), (q,n-1), (q-5,n-2), ...,
     (q-(5n-20),3), (q-(5n-16),2), (B_n,1).
```

All constants are finite positive integers by induction.  The base values
satisfy `A_4=25=4*4+9` and `B_4=58>=4*4+9`.  If either current constant is at
least `4n+9`, then its next recurrence is bounded below by the A-side value,

```text
C(4n+9,2)-(20n-49) - (4(n+1)+9)
 = 2(4n^2+5n+36)>0.
```

(The B-side subtracts three less.)  Hence `A_n,B_n>=4n+9` for all `n>=4`.
For any finite `R`, the finitely many strict
canonical requirements reduce to lower bounds such as
`q-(5n-15)>A_n`; the actual recurrence `q_(j+2)=4q_j-4` is unbounded, so one
odd `j` satisfies every requirement through `R`.  The displayed words are
then nonnegative tails, so no hidden borrow invalidates the recurrence.

## Inductive Pascal step

Raising the word and subtracting `tau` preserves every leading term.  At the
bottom, with `d=5n-15`, the x-side identity is

```text
C(q-d,3)+C(A_n,2)-4q+3
 = C(q-d-1,3)+C(q-d-5,2)+A_(n+1).
```

The y identity uses `d=5n-16`, subtracts `4q-2`, and produces `B_(n+1)`.
These exact polynomial identities prove the stable-word induction.

Aligned Pascal cancellation gives

```text
gamma_n = C(B_n,2)-C(A_n+1,2)+2-4q
        = B_(n+1)-A_(n+1)-A_n-1-4q.            (*)
```

For fixed `R`, the constants in (*) are finite.  Taking the same actual `q`
larger than all finitely many quarter-constants makes every
`gamma_4,...,gamma_R` negative; `gamma_3=23-4q` is negative as well.

The quantifiers are

```text
for every fixed R, there exists one odd j_R such that the same member j_R
has gamma_3,...,gamma_R all negative.
```

They do **not** assert the existence of one finite member negative at every
rank.  Equivalently, the first-recovery ranks within this family have no
uniform finite upper bound.

The first constants reproduce the audited orbit:

```text
(A_5,B_5)=(269,1625),
(A_6,B_6)=(35995,1319452),
(A_7,B_7)=(647801944,870476130358).
```

The exact symbolic and multi-rank arithmetic guards are in
`verify_k4r9_no_fixed_rank.py`.  No bounded absence claim is used in the
theorem.
