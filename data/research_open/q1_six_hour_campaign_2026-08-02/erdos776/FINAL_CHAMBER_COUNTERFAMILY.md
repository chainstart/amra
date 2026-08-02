# The final-chamber counterfamily and its rank-six recovery

Date: 2026-08-02

## 1. Result and scope

The strict rank-five bridge (NB), equivalently (2.13) of
`NEGATIVE_INITIAL_CHAMBERS.md`, is false even on the actual dyadic lattice.
More precisely, the last conditional chamber

\[
(R,S)=(--),\qquad(P,Q)=(++)
\]

contains an infinite family with \(\gamma _5<0\).  The family is nevertheless
strictly positive at rank six.  It therefore refutes the proposed fixed
rank-five bridge, **not** Erdős #776 and not the adaptive-seed strategy.

## 2. An actual dyadic family

Fix

\[
K=6,\qquad r=10,\qquad u=r+K-1=15.
\tag{2.1}
\]

For every integer \(s\ge2\) with \(s\equiv2\pmod4\), put

\[
h=224\,2^s,
\qquad
q=\frac{2h-2}{5}=\frac{448\,2^s-2}{5},
\qquad
b=q+6,
\qquad
n=\binom q2+10.
\tag{2.2}
\]

These parameters are integral.  Indeed, \(448\equiv3\pmod5\), and

\[
3\,2^s\equiv2\pmod5
\quad\Longleftrightarrow\quad
s\equiv2\pmod4.
\tag{2.3}
\]

They also lie on the original, rather than relaxed, lattice.  Since
\(b-1=q+5\),

\[
\binom{b-1}{2}+2-n
=\binom{q+5}{2}+2-\binom q2-10
=5q+2
=2h.
\tag{2.4}
\]

Moreover \(q\ge358\), so

\[
0\le r<q,
\qquad
0\le u<q+1,
\qquad
b<h,
\qquad
h\ge224,
\qquad
b\ge31.
\tag{2.5}
\]

Here \(b<h\) follows directly from
\(b=(2h+28)/5<h\).  Finally,

\[
n+b-1=\binom{q+1}{2}+15,
\tag{2.6}
\]

so exactly one rank-two promotion occurs, and the tax is

\[
\tau=\binom b2+1-n=2h+b-2=6q+6.
\tag{2.7}
\]

Thus every condition used below, including the dyadic condition, is
literal.

## 3. The two canonical levels

The first raw tails are

\[
R=\binom{r+1}{2}-Kq-\binom K2=40-6q,
\qquad
S=R+\binom u2-\binom r2-1=99-6q.
\tag{3.1}
\]

Both are negative throughout (2.2).  After the two single-wall borrows,

\[
\begin{aligned}
\alpha
 &=\binom{q-1}{2}+R
  =\binom{q-7}{2}+\binom{13}{1},\\
\beta
 &=\binom q2+S
  =\binom{q-6}{2}+\binom{78}{1}.
\end{aligned}
\tag{3.2}
\]

These are literal rank-two canonical words for \(q\ge85\), in particular
at every point relevant to the rank-five failure.  Hence

\[
x_0=\binom{q-1}{3}+\alpha,
\qquad
y_0=\binom q3+\beta.
\tag{3.3}
\]

The next raw tails are

\[
\begin{aligned}
P&=U_2(\alpha)-\tau+1
 =\binom{q-8}{3}+\binom{q-14}{2}+\binom41,\\
Q&=U_2(\beta)-\tau
 =\binom{q-7}{3}+\binom{q-13}{2}+\binom{2934}{1}.
\end{aligned}
\tag{3.4}
\]

The second word is canonical precisely in the displayed stable form once
\(q\ge2948\); the first already is canonical in this range.  Both tails
are positive, so

\[
X_1=\binom{q-1}{4}+P,
\qquad
Y_1=\binom q4+Q.
\tag{3.5}
\]

Consequently every point with \(q\ge2948\) is literally in the combined
chamber

\[
\boxed{(--)\longrightarrow(++).}
\tag{3.6}
\]

All four low blocks in (3.2)--(3.5) are nonnegative and strictly below
their displayed caps, so there is no suppressed extra wall crossing.

## 4. Exact rank-three through rank-five surpluses

The first surplus is immediate from the one-promotion formula:

\[
\boxed{\gamma _3=44-6q.}
\tag{4.1}
\]

Raising (3.2) gives

\[
U_2(\beta)-U_2(\alpha)
=\binom{q-7}{2}+2925.
\]

Since \(\alpha+\tau=\binom{q-1}{2}+46\), exact leading-block
cancellation yields

\[
\boxed{\gamma _4=2906-6q.}
\tag{4.2}
\]

For \(q\ge2948\), raising the literal words (3.4) and cancelling the
adjacent full blocks gives

\[
\boxed{
\gamma _5
=\binom{2934}{2}-6q-16
=4\,302\,695-6q.}
\tag{4.3}
\]

Thus

\[
\gamma _5<0
\quad\Longleftrightarrow\quad
q\ge717\,116.
\tag{4.4}
\]

On the dyadic subsequence (2.2), the first few \(q\)'s are

\[
358,\quad5734,\quad91750,\quad1\,468\,006
\]

at \(s=2,6,10,14\), respectively.  Hence the first rank-five failure is
at \(s=14\).  Its complete integer data are

\[
\begin{aligned}
h&=3\,670\,016,& b&=1\,468\,012,\\
q&=1\,468\,006,& n&=1\,077\,520\,074\,025,
\end{aligned}
\tag{4.5}
\]

and

\[
(\gamma _3,\gamma _4,\gamma _5)
=(-8\,807\,992,-8\,805\,130,-4\,505\,341).
\tag{4.6}
\]

Equations (2.2)--(4.6) give infinitely many actual dyadic counterexamples
to (NB): every \(s\equiv2\pmod4\) with \(s\ge14\) works.

## 5. Exact rank-six repair

Set

\[
P_2=U_3(P)-\tau+1,
\qquad
Q_2=U_3(Q)-\tau.
\tag{5.1}
\]

Direct Pascal subtraction gives

\[
P_2=
\binom{q-8}{4}
+\binom{q-15}{3}
+\binom{q-22}{2}
+\binom{q-132}{1},
\tag{5.2}
\]

and

\[
Q_2=
\binom{q-7}{4}
+\binom{q-14}{3}
+\binom{q-20}{2}
+\binom{4\,302\,600}{1}.
\tag{5.3}
\]

The second displayed word becomes canonical exactly when

\[
q-20>4\,302\,600,
\qquad\text{i.e.}\qquad q\ge4\,302\,621.
\tag{5.4}
\]

In this stable range, one more exact cancellation gives

\[
\begin{aligned}
\gamma _6
&=U_4(Q_2)-U_4(P_2)-P_2-\tau\\
&=\binom{4\,302\,600}{2}+104q-8421\\
&=\boxed{9\,256\,181\,220\,279+104q}>0.
\end{aligned}
\tag{5.5}
\]

The first dyadic parameter in this stable range is \(s=18\), where
\(q=23\,488\,102\).  The four earlier legal residue-class values are a
finite exact base:

| \(s\) | \(q\) | \(\gamma _4\) | \(\gamma _5\) | \(\gamma _6\) |
|---:|---:|---:|---:|---:|
| 2 | 358 | 758 | 370137 | 42058239 |
| 6 | 5734 | -31498 | 4268291 | 4252643571 |
| 10 | 91750 | -547594 | 3752195 | 28677939989 |
| 14 | 1468006 | -8805130 | -4505341 | 3088969555650 |

At \(s=14\), where (5.3) has not yet stabilized, the exact last word is

\[
Q_2=
\binom{1467999}{4}
+\binom{1467992}{3}
+\binom{1467988}{2}
+\binom{1366627}{1},
\tag{5.6}
\]

which supplies the fourth positive value in the table without extrapolating
the stable formula.  The complete table and (5.5) are checked with two
independent Macaulay implementations in
`verify_final_chamber_counterfamily.py`.

Therefore \(\gamma _6>0\) on the whole dyadic family (2.2).  The exact
adaptive repair is

\[
p(s)=
\begin{cases}
4,&s=2,\\
5,&s=6,10,\\
6,&s\ge14,
\end{cases}
\qquad(s\equiv2\pmod4).
\tag{5.7}
\]

## 6. Consequence for the campaign

The following statements are now **refuted**:

1. the relaxed-lattice implication (NB)/(2.13);
2. uniform positivity of the conditional \((--)\to(++)\) chamber at
   rank five;
3. the claim that every initial no-borrow negative point seeds by rank
   five.

The family does not contradict a variable-rank or rank-six repair: it is
uniformly positive at rank six.  The one-promotion and one-wall
exhaustiveness questions also cease to matter for this refutation, because
the displayed family independently satisfies all of those premises.  They
remain relevant only to any future positive classification of the rest of
the lattice.

The original Erdős #776 construction and the global uniform adaptive-seed
theorem remain open.
