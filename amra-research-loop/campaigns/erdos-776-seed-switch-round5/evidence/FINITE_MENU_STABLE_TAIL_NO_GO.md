# Finite-menu stable-tail reset no-go

## Theorem and exact scope

Fix a rank bound `R>=4` and a finite menu `S` of q-independent pairs
`(A_4,B_4)`.  For each pair, iterate

```text
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).
```

Retain the menu choices for which these constants stay nonnegative and the
same K4,r9 `H/q` staircase is intended through rank `R`.  Then one actual
odd K4,r9 member simultaneously has negative surplus through `R` for every
retained menu choice.

This is a no-go for a **fixed finite menu of q-independent lower-tail
resets**.  It does not cover a reset whose digits grow with `q`, a switch of
the leading `H/q` blocks, or a menu whose size/content grows with `q`.

## Proof

For one menu pair the stable rank-`n` words have the same leading staircase
as in round four and lower digits `A_n,B_n`.  The bottom Pascal identities
are independent of the starting constants, so the displayed recurrence is
unchanged.  Aligned cancellation gives

```text
gamma_n = C(B_n,2)-C(A_n+1,2)+2-4q.             (1)
```

For fixed `R` and a fixed finite menu, every constant in (1) is a fixed
integer.  There are also only finitely many canonical inequalities, of the
form

```text
q-(5n-15)>A_n,   q-(5n-16)>B_n.
```

Take one `Q` larger than all their right sides and all quarter-constants in
(1), across every retained menu choice and `4<=n<=R`.  The actual odd-strip
sequence

```text
q_(j+2)=4q_j-4
```

is unbounded, so choose an odd `j` with `q_j>Q`.  Every menu word is then
canonical, its next states are nonnegative sums of binomial terms, and all
its surpluses `gamma_4,...,gamma_R` are negative.  The inherited
`gamma_3=23-4q` is negative as well.

The same choice of `j` works for the whole menu.  Specializing `R=42`
rules out a fixed finite constant-tail menu as a uniform pre-rank-42 repair.
A fixed finite-state controller with finitely many q-independent outputs and
reset times unrolls through `R` to such a finite menu, so it is covered too.

## Consequence for route design

The obstruction identifies the information that a viable switch must add:
at least one of its lower digits or available choices must scale with `q`,
or it must alter the leading staircase.  Merely adding more fixed constants,
fixed reset times, or randomizing over finitely many of them cannot change
the coefficient `-4` in (1).

This does not settle Erdos-776 and supplies no public threshold improvement.
