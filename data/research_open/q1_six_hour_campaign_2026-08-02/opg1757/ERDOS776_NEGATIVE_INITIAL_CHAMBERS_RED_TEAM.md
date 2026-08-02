# Red-team audit: Erdős #776 negative initial chambers

Audit opened: 2026-08-02 12:35 HKT
Auditor: OPG-1757 lane, independent of the Erdős #776 author lane

## Verdict

**PASS AFTER REPAIR**, limited to the exact reduction, no-borrow
legality, and Lemma 2.1.  The sign assertion (2.13) remains **OPEN**.

No counterexample was found to Proposition 1.1, equations (2.1)--(2.9),
or Lemma 2.1.  The rank-five sign implication (2.13) is still open, as
the author states.  It must not be promoted from the finite scan.

The first audited version omitted one written proof guard: the low blocks
in (2.7) and (2.9) had to be shown to remain below their next Macaulay
caps.  Section 2 supplied the missing inequalities.  They have since been
incorporated into the author note, and the stale research-log reference
to (2.10) has been corrected to (2.13).  Both repairs were rechecked.

The audited source hashes are:

- NEGATIVE_INITIAL_CHAMBERS.md:
  f3fbe57cbed14cf870b338e04998bd783bf1640d20daee62b094bedf5602a046;
- NO_BORROW_GATE_FREEZE.md:
  7d49d0a0a328c27e0ffe6e5c5c6a91c7f92ef33560095933b2f6a6890cf66c02;
- verify_negative_initial_chambers.py:
  555a168e126615aa425469379dd17a9ba55f53e945aecbb2db44d08f646af481.

The repaired NEGATIVE_INITIAL_CHAMBERS.md passed under final hash
d0ca5fb4edccdc7f1333282949f9b6b9a88a756b5b2c6ef035896aceb6db9a9f.

## 1. Independent reconstruction

Put

\[
c=h+b-2,\quad T=2h+b-3,\quad \tau=T+1,
\]

\[
n=\binom{b-1}{2}+2-2h,\quad m=b-1,\quad
H=\binom b2+1.
\]

Then \(\tau=H-n\).  In the initial no-borrow chamber,

\[
x_3=\binom c3+n,\qquad y_3=\binom{c+1}{3}+n+m.
\]

Writing

\[
z=U_2(n),\quad w=U_2(n+m),\quad \Delta=w-z
\]

and applying one exact Macaulay raise gives

\[
x_4=\binom c4+(z-T),\qquad
y_4=\binom{c+1}{4}+(w-\tau).
\]

Thus the author's variables are exactly

\[
x_0=z-T=n+z-H+1,\qquad
y_0=w-\tau=x_0+\Delta-1,
\]

and cancellation of the two leading Pascal terms gives

\[
\gamma_3=\Delta-H.
\]

Superadditivity gives

\[
\Delta\ge U_2(m)\ge U_2(30)=57,
\]

so \(y_0-x_0=\Delta-1>0\).  Hence the three stated sign states are
exhaustive, the reverse asymmetric state is impossible, and equality
belongs on the non-borrowing side.

The relaxed lattice is also exact.  Solving the definition of \(n\)
for \(h\) gives (2.6), including its parity condition.  Conversely,
every point of (2.6) reconstructs an admissible integral \(h\).
The lower bound \(b\ge31\) follows from

\[
448\le2h\le\binom{b-1}{2}+2.
\]

## 2. No-borrow cap legality

For a \(p\)-canonical integer \(N<\binom ap\), every upper index in its
canonical word is below \(a\), and therefore

\[
U_p(N)<\binom a{p+1}.
\tag{A}
\]

The two initial residuals are legally below their caps because direct
subtraction gives

\[
\binom c2-n=\frac{(h-1)(2b+h)}2>0,
\]

\[
\binom{c+1}{2}-(n+m)
=\frac{(h-1)(2b+h+2)}2>0.
\]

Consequently (A) gives

\[
z<\binom c3,\qquad w<\binom{c+1}{3}.
\]

If \(x_0\ge0\), then \(y_0>x_0\ge0\), while

\[
0\le x_0=z-T<\binom c3,\qquad
0\le y_0=w-\tau<\binom{c+1}{3}.
\]

Thus both displays in (2.4) are legal rank-four canonical
concatenations.  Raising them and cancelling the leading Pascal terms
proves, with no hidden borrow,

\[
\gamma_4=U_3(y_0)-U_3(x_0)-x_0-\tau.
\]

At the next row,

\[
X_1=U_3(x_0)-T,\qquad Y_1=U_3(y_0)-\tau.
\]

If \(X_1,Y_1\ge0\), (A) again gives

\[
X_1<\binom c4,\qquad Y_1<\binom{c+1}{4}.
\]

Therefore the rank-five concatenations are legal and the same Pascal
cancellation proves

\[
\gamma_5=U_4(Y_1)-U_4(X_1)-X_1-\tau.
\]

This closes the legality dependency behind (2.7)--(2.9).  It does not
prove the sign of \(\gamma_5\).

The two tax cancellations were also rechecked:

\[
x_0+\tau=U_2(n)+1,\qquad
X_1+\tau=U_3(x_0)+1.
\]

They give (2.9a)--(2.9b) exactly.

## 3. Uniformity audit of Lemma 2.1

For each fixed \(j\), the estimate

\[
U_j(N)=c_jN^{1+1/j}+O(N)
\]

has constants depending only on \(j\).  It is therefore uniform over
the lattice.  Also \(n\ge0\) gives

\[
h\le\frac12\binom{b-1}{2}+1,
\]

so every sequence with \(h\to\infty\) has \(b\to\infty\).

Assume along such a sequence that the antecedent of Lemma 2.1 holds and
\(X_1\le0\).  Then \(U_3(x_0)<\tau=O(b^2)\), whence

\[
x_0=O(b^{3/2}).
\]

Since

\[
n+U_2(n)=x_0+H-1=\Theta(b^2),
\]

fixed-rank asymptotics give

\[
n=\Theta(b^{4/3}).
\]

Here \(m=b-1=o(n)\), so the rank-two increment has the uniform scale

\[
\Delta=U_2(n+m)-U_2(n)
=\Theta(m\sqrt n)=\Theta(b^{5/3}).
\]

The \(O(n+m)\) error is \(O(b^{4/3})\), strictly below the displayed
main scale.  Hence

\[
d=\Delta-1=\Theta(b^{5/3}),\qquad
y_0=\Theta(b^{5/3}),
\]

and therefore

\[
U_3(y_0)=\Theta(b^{20/9}).
\]

In contrast, \(X_1\le0\) implies
\(U_3(x_0)+x_0+\tau=O(b^2)\).  Equation (2.7) would force
\(\gamma_4>0\), contradicting the antecedent.  This proves \(X_1>0\)
uniformly for sufficiently large \(h\).

For the other block, \(x_0\ge0\) already implies
\(n=\Omega(b^{4/3})\).  Upper-shift superadditivity gives

\[
\Delta\ge U_2(b-1),
\]

so \(d\to\infty\) uniformly.  A second use at rank three gives

\[
Y_1-X_1
=U_3(x_0+d)-U_3(x_0)-1
\ge U_3(d)-1>0
\]

eventually.  Together with \(X_1>0\), this proves \(Y_1>0\).
The sequential contradiction argument therefore has the advertised
uniform quantifier; no \(b\)-dependent threshold was smuggled in.

## 4. Independent exact falsification

The audit used a separately written greedy combinadic engine, rather than
calling the author verifier.

On every relaxed point with \(31\le b\le150\), it reconstructed the full
rank-three through rank-five orbit from the large canonical integers.
Among 246,955 points with \(\gamma_3<0\), the sign-state census was

\[
(20,393,\ 4,957,\ 221,605)
\]

for double borrow, \(x\)-only borrow, and no borrow.  Every cap bound and
every instance of (2.7)--(2.9) agreed exactly.  There were 36 no-borrow
points with \(\gamma_4<0\); all had legal \(X_1,Y_1\) and positive
\(\gamma_5\).

A separate dimensionless scan of all 10,209,264 relaxed lattice points
with \(31\le b\le500\) found 1,320 antecedents of (2.13).  It found:

- no \(X_1\le0\) or \(Y_1\le0\);
- no zero or negative \(\gamma_5\);
- no departure from the observed one-promotion rank-two chart.

The smallest \(\gamma_5\) in this larger relaxed scan was \(4222\), at

\[
(b,h,n)=(47,238,561),\qquad
(X_1,Y_1)=(40405,46310).
\]

A targeted attack on the first excluded chart parameterized every exact
two-promotion state with `q<=2000` and `4<=K<=40`.  Of 730,573 legal
states, 729,100 had `x0>=0`; none had `gamma4<0`.  The smallest was

\[
\gamma_4=73
\quad\text{at}\quad(q,K,a,b,h,x_0,y_0)
=(15,20,7,35,225,1,252).
\]

This is further evidence that the open antecedent may force one
promotion, but it is not a proof for unbounded `q,K` or for three and
later promotions.

Finally, a one-promotion root-window attack covered
`5<=q<=5000`, `4<=K<=50`.  For every `(q,K)` it tested the endpoints
and every integer `r` within six units of either sign wall `R=0` or
`S=0`.  Among 3,091,321 legal candidate states, 24,226 satisfied the
full antecedent of (2.13).  None had an illegal next block or
`gamma5<=0`; the same global minimum `4222` reappeared.  This is a
targeted falsifier, not an exhaustive scan over all `r`.

There is also a concrete proof-route warning.  Superadditivity alone only
gives

\[
\gamma_4\ge U_3(d)-U_2(n)-1.
\]

That lower bound is not positive on the multi-promotion charts.  In an
exact scan with `q<=300`, `K<=60`, its two-promotion minimum was
`-3,788,386` at `(q,K,r)=(300,7,299)`, even though the actual
`gamma4` there is positive.  Its three-promotion minimum was `-8,291`
at `(q,K,r)=(55,60,54)`.  The scan contained 229,757 legal
two-promotion and 2,716 legal three-promotion states with `x0>=0`; their
actual minimum `gamma4` values were respectively 69 and 124, with no
negative case.  Any universal exclusion of multiple promotions must
retain the large-leading-block increment

\[
U_3(x_0+d)-U_3(x_0),
\]

not replace it by `U3(d)`.

There is a second, all-parameter route obstruction: the one-promotion
antecedent does not confine \(K\) to a bounded list.

Fix any integer \(K\ge4\).  For each sufficiently large \(q\), choose
the least \(r_0\) for which

\[
R(r_0)=\binom{r_0+1}{2}-Kq-\binom K2\ge0,
\]

and use either \(r_0\) or \(r_0+1\) to meet the lattice parity.  Then

\[
r=\sqrt{2Kq}+O(1),\qquad R=O(\sqrt q),
\]

\[
S=R+(K-1)r+\binom{K-1}{2}-1=O(\sqrt q)>0.
\]

For large \(q\), \(u=r+K-1<q+1\), so this is exactly one rank-two
promotion, and \(R,S\) are legally in the \(++\) chamber.  Moreover,

\[
\gamma_3=(K-1)r-K(q+1)<0,\qquad
x_0=\binom q3+R>0.
\]

Using the exact \(++\) formula (B) below,

\[
\begin{aligned}
\gamma_4
&=U_2(S)-U_2(R)-\binom r2-1\\
&\le O(q^{3/4})-Kq+O(\sqrt q)<0.
\end{aligned}
\]

Finally,

\[
2h=\binom{q+K-1}{2}+2-\binom q2-r
=(K-1)q+O(\sqrt q),
\]

so \(h>b=q+K\) for every fixed \(K\ge4\) and all sufficiently large
\(q\).  Thus every fixed \(K\ge4\) has infinitely many relaxed-lattice
points entering the open antecedent.  Any proof of (2.13) must be
uniform in unbounded \(K\); a finite-\(K\) classification cannot close
the gate.

The computational statements above are finite falsification results
only; the fixed-\(K\) obstruction in this paragraph is an asymptotic
proof.

## 5. Exact remaining gate

The first unproved assertion is still precisely

\[
\gamma_3<0,\qquad x_0\ge0,\qquad\gamma_4<0
\quad\Longrightarrow\quad
U_4(Y_1)-U_4(X_1)-X_1-\tau>0.
\]

The observed assertion that this antecedent always causes exactly one
rank-two promotion is also open.  Conditional on that chart, the author's
coordinates were independently checked:

\[
\gamma_3=(K-1)r-K(q+1),
\]

\[
x_0=\binom q3+R,\qquad
y_0=\binom{q+1}{3}+S,
\]

with

\[
R=\binom{r+1}{2}-Kq-\binom K2,\qquad
S=R+\binom{r+K-1}{2}-\binom r2-1.
\]

All are exact identities, but none proves that the chart is exhaustive
or that \(\gamma_5>0\).  Erdős #776 therefore remains open.

Conditional on one promotion and at most one rank-three wall in each
low block, the next split is also exact.  Put

\[
A=\binom{q-1}{2}+R,\qquad B=\binom q2+S.
\]

The three possible sign chambers give

\[
\begin{array}{c|l}
R< S<0&
\gamma_4=U_2(B)-U_2(A)-\binom{q-1}{2}-\binom r2-1,\\[1mm]
R<0\le S&
\gamma_4=\binom{q-1}{3}+U_2(S)-U_2(A)-\binom r2-1,\\[1mm]
0\le R<S&
\gamma_4=U_2(S)-U_2(R)-\binom r2-1.
\end{array}
\tag{B}
\]

All 219 antecedents through \(b=250\) satisfy the required single-wall
caps; their chamber census is \(168,1,50\), and every value in (B)
matches the direct orbit.  Formula (B) is a useful next reduction, but
its stated cap premise has not yet been proved on the unbounded lattice.
