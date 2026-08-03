# Independent audit: K4,r9 has no uniform fixed recovery rank

## Verdict

The theorem reconstructs independently from the original K4,r9 Macaulay
orbit.  For every fixed integer `R>=4`, one can choose a sufficiently late
actual odd member `j_R` such that

```text
gamma_3(j_R), ..., gamma_R(j_R) < 0
```

simultaneously and every transition through that prefix has a legal
nonnegative canonical next state.  Hence the first positive-surplus ranks in
this fixed `(k,r)=(4,9)` orbit have no uniform finite upper bound.  In
particular, the `R=42` instance refutes a uniform pre-rank-42 seed obtained
only by waiting for a positive surplus along this orbit.

The quantifiers are `for every R there exists j_R`.  They are not `there
exists one j which works for every R`.  Thus the audit does not certify one
finite state that never recovers, and it does not refute the public antichain
statement by other constructions.

## Reconstruction from the raw orbit

For actual odd `j`, start with

```text
h=112*2^(j-1), q=(2h+4)/3, b=q+4, H=5q/2, tau=4q-2
```

and the original rank-3 values

```text
x=C(h+b-2,3)+C(b-1,2)+2-2h,
y=C(h+b-1,3)+C(b,2)+2-2h.
```

Greedy expansion gives the raw rank-3 words

```text
x_3=[(H,3),(q,2),(9,1)],
y_3=[(H+1,3),(q+1,2),(12,1)].
```

Define `A_4=25`, `B_4=58`.  The independently reconstructed stable rank-n
words (`n>=4`) are

```text
x_n: (H,n),(q-1,n-1),(q-6,n-2),...,
     (q-(5n-19),3),(q-(5n-15),2),(A_n,1),

y_n: (H+1,n),(q,n-1),(q-5,n-2),...,
     (q-(5n-20),3),(q-(5n-16),2),(B_n,1).
```

Directly raising the two rank-3 words and subtracting `tau` supplies the
`n=4` base.  No rank-7 or rank-8 formula is assumed in this derivation.

## Inductive transition

Assume the displayed rank-n words are strict canonical words.  All terms
except the last two carry forward by Pascal.  On the x side put
`d=5n-15`.  The remaining identity is

```text
C(q-d,3)+C(A_n,2)-4q+3
 = C(q-d-1,3)+C(q-d-5,2)
   + C(A_n,2)-(20n-49).
```

On the y side use `d=5n-16` and subtract `4q-2`; the corresponding constant
is `C(B_n,2)-(20n-52)`.  Therefore

```text
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).
```

These are polynomial identities, not observations from a bounded table.
The first values reproduce the independently audited lower cells:

```text
(A_5,B_5)=(269,1625),
(A_6,B_6)=(35995,1319452),
(A_7,B_7)=(647801944,870476130358),
(A_8,B_8)=(209823679001188505,378864346761083666538815).
```

The constants remain positive.  More precisely, `A_n,B_n>=4n+9`: the base
holds at `n=4`, and the smaller induction margin is

```text
C(4n+9,2)-(20n-49)-(4(n+1)+9)
 = 2(4n^2+5n+36) > 0.
```

For a fixed `R`, only finitely many constant-order conditions such as
`q-(5n-15)>A_n` and `q-(5n-16)>B_n` occur.  Taking q above their maximum
makes every displayed word through `R+1` strict canonical, and the transition
identities make all next states nonnegative.

## Surplus and quantifiers

Aligned cancellation in the independently reconstructed words yields

```text
gamma_n = C(B_n,2)-C(A_n+1,2)+2-4q
        = B_(n+1)-A_(n+1)-A_n-1-4q       (n>=4),
gamma_3 = 23-4q.
```

For fixed `R`, every non-q term here is one finite integer.  Choose q larger
than the finite maximum of the canonical thresholds and all relevant
quarter-constants.  Then every `gamma_3,...,gamma_R` is negative.  Finally,
the actual odd-member recurrence

```text
q_(j+2)=4q_j-4
```

is unbounded, so an actual odd `j_R` exceeds this single finite threshold.
This completes the universal-in-R proof without computing the enormous
`R=42` constants explicitly.

## Machine cross-check

The independent checker constructs the original x and y integers, performs
greedy Macaulay expansion, and advances the raw orbit.  It selected the
actual odd member `j=2477` and verified ranks 3 through 12 simultaneously:
all stable words through rank 13 matched, all tested surpluses were negative,
and all next states were nonnegative.  This bounded replay is a cross-check;
the all-fixed-R conclusion comes from the induction and unbounded-q argument
above.

Both author and independent checkers passed with

```text
ulimit -v 3145728; timeout 180s python3 <checker>
```

The independent checker SHA-256 is
`8cba5acde5aaaad2a4af222a17641b2525c3c4a62f90514d98c6f2088733fc5a`.
Lean was not needed.

## Statement, mechanism, and promotion review

The decisive statement matches the proved quantifiers and parameter range.
It strictly kills `M406-uniform-fixed-parameter-recovery` and the
same-orbit uniform waiting component of `M412-rank42-seed-composition`.
It supports the K4,r9 instance of `M405` and `M407` but not their universal
extensions.

`M410-infinite-nonrecovery-counterfamily` must retain its literal stronger
meaning: one actual family/state with an all-rank negative recurrence.  The
present diagonal theorem does not prove that claim; M410 may survive only as
an open strengthening, never as a restatement of this result.  Likewise the
theorem says nothing decisive about finite recovery of each individual
state, so `M411` remains unresolved/frozen.

The result is a standalone decisive no-uniform-bound lemma for the adaptive
route, but it supplies no alternative public construction, no global seed
composition, and no improved antichain threshold, main term, or exponent.
Public promotion is rejected.  No external priority search was performed,
so novelty/priority remains uncertain.
