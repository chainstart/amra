# Erdős #776: independent audit of the reverse rank-18 barrier

Date: 2026-07-30

## 1. Verdict

Let

\[
\begin{aligned}
H_{18}(V)
&=\binom{V-12}{18}
  +\sum_{i=4}^{17}\binom{V-31+i}{i},\\
\rho(V)&=\binom{V-30}{3}-1,\\
B_{18}(V)&=H_{18}(V)+\rho(V),
\end{aligned}
\]

and run the reverse recurrence

\[
b_{q+1}=U_q(b_q-V).
\]

Throughout this note \(V\ge70\), the range in which the proposed barrier
and all displayed canonical charts are being audited.

Exact computations suggest that \(H_{18}\) reaches the penultimate value
\(V-1\), whereas \(B_{18}\), \(B_{18}-1\), and \(B_{18}+1\) reach \(V\)
and then \(0\).  This audit finds no counterexample to that pattern.

There is, however, **no independent all-\(V\) proof of the barrier here**.
The decisive threshold crossed by the last residual \(\rho(V)\) is exactly
the old rank-18 successive-block condition

\[
z_3(V)\le \binom{V-30}{3}-1.
\]

Thus the endpoint experiment is not new evidence that bypasses the old
unbounded carry problem: at the critical threshold it is a Galois-dual
evaluation of the same inequality.

This audit does prove two all-parameter structural facts:

1. an exact tail-complement normal form with four nontrivial binomial
   terms and one unit term;
2. an adjacent-parameter suspension domination for the complementary
   orbit.

The second fact is only qualitative.  Its exact final-step requirement is
a gap of \(V+1\), which is not supplied by qualitative domination.

## 2. Macaulay notation

If the \(r\)-canonical expansion of \(x\) is

\[
x=\sum_i\binom{a_i}{i},
\]

write

\[
\operatorname{KK}_r(x)=\sum_i\binom{a_i}{i-1},\qquad
U_r(x)=\sum_i\binom{a_i}{i+1},
\]

and

\[
S_r(x)=x+U_r(x)=\sum_i\binom{a_i+1}{i+1}.
\]

The identities used below are

\[
\operatorname{KK}_{r+1}(S_r(x))
=x+\operatorname{KK}_r(x)
\tag{2.1}
\]

and the Galois adjunction

\[
\operatorname{KK}_{r+1}(y)\le x
\quad\Longleftrightarrow\quad
y\le U_r(x).
\tag{2.2}
\]

## 3. Exact tail complement

Put

\[
N=V-11,\qquad R=V-29.
\]

At rank \(q\), set \(r=N-q\) and define the complement

\[
A_r=\binom Nq-b_q.
\]

The standard tail-complement identity gives

\[
\boxed{A_{r-1}=\operatorname{KK}_r(A_r+V).}
\tag{3.1}
\]

Indeed,

\[
b_q-V=\binom Nq-(A_r+V),
\]

and taking \(U_q\) on the left is dual to taking
\(\operatorname{KK}_r\) on the complementary tail.

For the full proposed barrier, Pascal cancellation gives the exact
\(R\)-canonical start

\[
\boxed{
\begin{aligned}
A_R^{[V]}
={}&\binom{V-13}{R}
 +\binom{V-28}{R-1}
 +\binom{V-29}{R-2}\\
&+\binom{V-30}{R-3}+1.
\end{aligned}}
\tag{3.2}
\]

This is a useful simplification, but it does not by itself control the
successive carries in (3.1).

At the penultimate rank \(q=V-13\), equivalently \(r=2\), define

\[
T(V)=\binom{V-11}{2}-V
=\binom{V-13}{2}+(V-25).
\tag{3.3}
\]

Then

\[
b_{V-13}=V
\quad\Longleftrightarrow\quad
A_2=T(V).
\tag{3.4}
\]

If (3.4) holds, the last step is automatic:

\[
A_2+V=\binom{V-11}{2},\qquad
A_1=V-11,\qquad b_{V-12}=0.
\]

By contrast, \(b_{V-13}=V-1\) means \(A_2=T(V)+1\).  Then

\[
A_2+V=\binom{V-11}{2}+1,
\]

whose rank-two lower shadow is \(V-10\); the formal next \(b\)-value is
\(-1\), and the reverse recurrence correctly stops because one cannot
subtract \(V\) from \(V-1\).

## 4. Capacity threshold and exact recovery of the old residual cap

For a proposed rank-two endpoint \(t\), define its maximal capacity lift by

\[
\phi_2(t)=t,\qquad
\phi_r(t)=U_{r-1}(\phi_{r-1}(t))-V
\quad(3\le r\le R),
\]

and put

\[
\Phi_V(t)=\phi_R(t).
\]

Repeated use of (2.2) gives the exact fibre description

\[
A_2=t
\quad\Longleftrightarrow\quad
\Phi_V(t-1)<A_R\le\Phi_V(t),
\tag{4.1}
\]

whenever the displayed capacity lifts are in the valid nonnegative chart.
For the one-sided conclusion needed by the forward barrier,

\[
A_2\le t
\quad\Longleftrightarrow\quad
A_R\le\Phi_V(t).
\tag{4.2}
\]

Now let the shortened zero-seed orbit be

\[
D_{V-12}=0,\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q).
\tag{4.3}
\]

At \(q=V-13\), its complement is exactly \(T(V)\).  Applying the same
tail-complement identity upwards from \(q=V-13\) to \(q=18\) therefore
gives

\[
\boxed{
\Phi_V(T(V))=\binom{V-11}{18}-D_{18}.
}
\tag{4.4}
\]

Write the old rank-18 successive-block residual as

\[
D_{18}=H_{18}(V)+z_3(V).
\tag{4.5}
\]

Let

\[
A_R^B=\binom{V-11}{18}-B_{18}(V),\qquad
A_R^H=\binom{V-11}{18}-H_{18}(V).
\]

Equations (4.4)--(4.5) give the two exact distances from the critical
capacity surface:

\[
\boxed{
\Phi_V(T)-A_R^B=\rho-z_3,
\qquad
A_R^H-\Phi_V(T)=z_3.
}
\tag{4.6}
\]

Consequently,

\[
\boxed{
A_R^B\le\Phi_V(T)
\quad\Longleftrightarrow\quad
z_3(V)\le\rho(V).
}
\tag{4.7}
\]

By (4.2), (4.7) is precisely the assertion that the full reverse barrier
reaches at least the penultimate value \(V\).  This is the useful
one-sided barrier assertion, and it is **exactly equivalent** to the old
rank-18 residual cap.

To locate the exact value \(b_{V-13}=V\), rather than merely
\(b_{V-13}\ge V\), one additionally needs the other side of the same
Galois fibre,

\[
A_R^B>\Phi_V(T-1).
\tag{4.8}
\]

The finite runs satisfy (4.8), but this audit does not use them to claim it
for every \(V\).  In particular, even a future proof of this auxiliary
fibre localization would not prove the decisive inequality (4.7).

Equation (4.6) also explains the observed \(V-1/V\) switch.  Removing the
last residual moves the complementary start upward by exactly \(\rho\).
The amount needed to cross the critical surface is exactly \(z_3\).
Thus adding \(\rho\) crosses the surface if and only if
\(\rho\ge z_3\), which is the old open cap.  The experiment does not
generate that cap; it evaluates it.

## 5. A genuine all-parameter suspension domination

Although it does not close the barrier, the complement start (3.2) has an
exact adjacent-parameter suspension:

\[
\boxed{
A_{R+1}^{[V+1]}=S_R(A_R^{[V]}).
}
\tag{5.1}
\]

Moreover, for every aligned rank in the complementary descent,

\[
\boxed{
A_{r+1}^{[V+1]}\le S_r(A_r^{[V]}).
}
\tag{5.2}
\]

### Proof

Equation (5.1) follows by suspending each of the four displayed nonunit
binomial terms in (3.2), together with \(1=\binom11\).

Assume (5.2) at rank \(r\).  Put

\[
x=A_r^{[V]},\qquad
y=A_{r-1}^{[V]}=\operatorname{KK}_r(x+V).
\]

First,

\[
S_r(x)+V+1\le S_r(x+V).
\tag{5.3}
\]

To see this, the one-set shadow bound gives

\[
\operatorname{KK}_{r+1}(U_r(x)+1)
\le x+r+1\le x+V,
\]

because \(r+1\le V\) on this orbit.  The adjunction (2.2) then yields
\(U_r(x+V)\ge U_r(x)+1\), which is (5.3).

Using monotonicity, (2.1), and (5.3),

\[
\begin{aligned}
A_r^{[V+1]}
&\le
\operatorname{KK}_{r+1}(S_r(x)+V+1)\\
&\le
\operatorname{KK}_{r+1}(S_r(x+V))\\
&=x+V+y.
\end{aligned}
\]

Finally, \(y=\operatorname{KK}_r(x+V)\) and (2.2) imply
\(U_{r-1}(y)\ge x+V\).  Hence

\[
x+V+y\le y+U_{r-1}(y)=S_{r-1}(y),
\]

which is the next instance of (5.2). \(\square\)

## 6. Exact gap recursion and why qualitative domination is insufficient

Define the aligned gap

\[
G_r=S_r(A_r^{[V]})-A_{r+1}^{[V+1]}\ge0.
\]

With \(x,y\) as in the proof, put

\[
\begin{aligned}
P_r&=S_r(x+V)-S_r(x)-(V+1),\\
Q_{r-1}&=U_{r-1}(y)-(x+V),\\
M_r&=S_r(x+V).
\end{aligned}
\]

Both \(P_r\) and \(Q_{r-1}\) are nonnegative.  Direct substitution into
(3.1) gives the exact quantitative recursion

\[
\boxed{
\begin{aligned}
G_{r-1}
={}&Q_{r-1}\\
&+\operatorname{KK}_{r+1}(M_r)
 -\operatorname{KK}_{r+1}
   \bigl(M_r-(P_r+G_r)\bigr).
\end{aligned}}
\tag{6.1}
\]

Thus the qualitative proof records only that two losses are nonnegative.
The endpoint needs a much larger, sharp loss.

Assume the desired endpoint at parameter \(V\), so
\(A_2^{[V]}=T(V)\).  Pascal's identity gives

\[
U_2(T(V+1))=S_2(T(V)).
\tag{6.2}
\]

The next endpoint inequality is therefore

\[
\begin{aligned}
A_2^{[V+1]}\le T(V+1)
&\Longleftrightarrow
A_3^{[V+1]}+V+1\le U_2(T(V+1))\\
&\Longleftrightarrow
\boxed{G_2\ge V+1}.
\end{aligned}
\tag{6.3}
\]

The size \(V+1\) is not an artefact of a loose estimate.  With no gap,

\[
\begin{aligned}
S_2(T(V))+V+1
={}&\binom{V-12}{3}
 +\binom{V-23}{2}+25,
\end{aligned}
\]

and hence

\[
\operatorname{KK}_3(S_2(T(V))+V+1)
=T(V+1)+2.
\tag{6.4}
\]

The shadow overshoot is only \(2\), but the relevant Macaulay plateau has
width \(V+1\).  This is why \(G_2\ge0\) does not come close to proving the
induction.

Selected exact diagnostics decompose the final gap using (6.1):

| \(V\) | \(G_3\) | \(Q_2\) | rank-4 shadow loss | \(G_2\) | required |
|---:|---:|---:|---:|---:|---:|
| 70 | 91 | 1 | 72 | 73 | 71 |
| 100 | 118 | 29 | 101 | 130 | 101 |
| 175 | 208 | 99 | 177 | 276 | 176 |
| 379 | 425 | 294 | 381 | 675 | 380 |

These rows pass (6.3), but no invariant found in this audit bounds either
summand in (6.1) uniformly through all earlier carry changes.

In the same rows the rank-three state has the diagnostic form

\[
A_3^{[V]}
=\binom{V-13}{3}+\binom{V-27}{2}+h(V),
\]

with \(h(70)=16\), \(h(100)=18\), \(h(175)=23\), and \(h(379)=32\).
On this chart,

\[
Q_2=V-h(V)-53.
\]

Proving the required uniform bound on \(h\), however, is just a
lower-rank encoding of the same endpoint cap; the finite persistence of
this chart is not an all-\(V\) proof.

## 7. Finite falsifier checks

An independent ordinary combinadic implementation was used for exact
integer checks.

- For every \(70\le V\le200\), no exception was found to
  \[
  H_{18}\longmapsto V-1,\qquad
  B_{18}-1,B_{18},B_{18}+1\longmapsto V\longmapsto0.
  \]
- The same pattern was checked at the strategic value \(V=379\).
- For example, the critical quantities are:

| \(V\) | \(\rho\) | \(z_3\) | \(B_{18}-D_{18}=\rho-z_3\) |
|---:|---:|---:|---:|
| 70 | 9,879 | 7,868 | 2,011 |
| 100 | 54,739 | 4,655 | 50,084 |
| 175 | 497,639 | 4,335 | 493,304 |
| 379 | 7,023,973 | 4,594 | 7,019,379 |

The positive margins explain why perturbing \(B_{18}\) by \(1\) does not
change these finite endpoints.  They are regression and falsifier data
only, not a finite extrapolation.

## 8. Frozen conclusion and next legitimate target

The reverse rank-18 experiment is useful as a dual coordinate system, but
it has not created a new proof route around the old carry problem:

\[
\text{full reverse barrier crosses the critical endpoint surface}
\quad\Longleftrightarrow\quad
z_3(V)\le\binom{V-30}{3}-1.
\]

The only independent all-\(V\) advance in this note is the structural
suspension domination (5.2) and its exact gap recursion (6.1).  To turn
that into a proof one must establish the sharp quantitative endpoint
loss

\[
G_2(V)\ge V+1
\]

without assuming the old residual cap or a finite list of carry charts.
Until such a bound is proved, the reverse barrier should be recorded as
an exact-equivalence/no-go reformulation, not as closure of Erdős #776.
