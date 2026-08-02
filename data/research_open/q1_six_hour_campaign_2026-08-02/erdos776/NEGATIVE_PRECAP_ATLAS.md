# Negative-offset pre-cap theorem and the remaining cap gate

## 1. Exact paired recurrence before the first moving cap

Let \(h=L/2\), retain the local orbit from (1.1) of
`LEFT_OFFSET_FIVE_OBSTRUCTION.md`, and now allow an integer \(b\ge5\).
The relevant left-hand chamber begins with both signed rank-three tails
negative.  As long as the displayed words remain canonical, define

\[
\begin{aligned}
A_3(b)&=\binom{b+1}{2}-6,&
B_3(b)&=\binom{b+2}{2}-6,\\
A_{p+1}(b)&=\binom{A_p(b)}2+b+6-6p,&
B_{p+1}(b)&=\binom{B_p(b)}2+b+7-6p.
\end{aligned}
\tag{1.1}
\]

### Proposition 1.1 (moving-\(b\) pre-cap normal form)

At every canonical pre-cap row,

\[
\begin{aligned}
x_p={}&\binom{h+b-3}{p}
 +\sum_{r=3}^{p-1}\binom{h+b+3r-3p-3}{r}
 +\binom{h+b+4-3p}{2}+\binom{A_p(b)}1,\\
y_p={}&\binom{h+b-2}{p}
 +\sum_{r=3}^{p-1}\binom{h+b+3r-3p-2}{r}
 +\binom{h+b+5-3p}{2}+\binom{B_p(b)}1.
\end{aligned}
\tag{1.2}
\]

Consequently

\[
\boxed{
\gamma_p(b)=K_p(b)-2h,
\qquad
K_p(b)=\binom{B_p(b)}2-\binom{A_p(b)+1}{2}-(b-2).}
\tag{1.3}
\]

#### Proof

The two initial Pascal normalizations are

\[
\begin{aligned}
x_3&=\binom{h+b-3}{3}+\binom{h+b-5}{2}
     +\binom{A_3(b)}1,\\
y_3&=\binom{h+b-2}{3}+\binom{h+b-4}{2}
     +\binom{B_3(b)}1.
\end{aligned}
\]

If \(d=h+b+4-3p\), the same two-row Pascal subtraction as on \(b=5\)
leaves

\[
\binom{A_p(b)}2+2d-5-(2h+b-3)
=\binom{A_p(b)}2+b+6-6p,
\]

and the adjacent row leaves one more.  This proves (1.1)--(1.2).
All nonconstant terms cancel in the adjacent surplus, leaving (1.3).
(\square)

## 2. The slowest formal left offset is \(b=5\)

### Proposition 2.1 (strict offset monotonicity)

For every \(p\ge3\), \(K_p(b)\) is strictly increasing on the integers
\(b\ge5\).

#### Proof

Put

\[
\alpha=A_p(b+1)-A_p(b),\qquad
\beta=B_p(b+1)-B_p(b).
\]

At rank three, \(\alpha=b+1\), \(\beta=b+2\), and
\(B_3(b)-A_3(b)=b+1\ge6\).  The recurrence gives

\[
\begin{aligned}
\alpha'&=\frac{\alpha(2A_p+\alpha-1)}2+1,\\
\beta'&=\frac{\beta(2B_p+\beta-1)}2+1.
\end{aligned}
\tag{2.1}
\]

Thus \(\beta\ge\alpha>0\) and \(B_p-A_p\ge6\) propagate.  Direct
subtraction gives

\[
\begin{aligned}
K_p(b+1)-K_p(b)
&=\frac{\beta(2B_p+\beta-1)
 -\alpha(2A_p+\alpha+1)}2-1\\
&\ge\alpha(B_p-A_p-1)-1>0.
\end{aligned}
\tag{2.2}
\]

This proves the claim. (\square)

Let \(p_5(h)\) be the candidate rank (4.1) for the fixed \(b=5\)
family.  Combining Proposition 2.1 with the uniform lemma from that file
gives an actual moving-parameter statement.

### Corollary 2.2 (uniform pre-cap upper bound)

Suppose \(b=b(h)\ge5\) lies in the double-borrow left chamber and the
paired words (1.2) remain canonical through rank \(p_5(h)\).  Then a
nonnegative diagonal seed occurs by \(p_5(h)\), where

\[
p_5(h)=\log_2\log h+O(1).
\tag{2.3}
\]

Indeed, (1.3), Proposition 2.1, and the definition of \(p_5(h)\) give

\[
\gamma_{p_5(h)}(b)
=K_{p_5(h)}(b)-2h
\ge K_{p_5(h)}(5)-2h\ge0.
\]

This closes the full pre-cap quantifier on this negative-side chamber.
It does not cover a moving \(b\) whose low constant reaches a canonical
cap before \(p_5(h)\).

## 3. Exact first-wall atlas

The cap obstruction can be stated without ambiguity.  At rank \(p\), put

\[
d=h+b+4-3p,\quad A=A_p(b),\quad B=B_p(b),\quad D=B-A,\quad
\tau=2h+b-2,
\]

and

\[
N_x=\binom d2+A,\qquad N_y=\binom{d+1}{2}+B=N_x+d+D.
\tag{3.1}
\]

The bottom paired blocks in (1.2) are

\[
\binom{d+2}{3}+N_x,\qquad
\binom{d+3}{3}+N_y.
\]

Therefore the first rank-three wall has the following exact states.

1. If \(N_x<\binom{d+2}{2}\) and
   \(N_y<\binom{d+3}{2}\), then

   \[
   \gamma_p=\Phi_\tau(N_x,d+D).
   \tag{3.2}
   \]

2. If only \(y\) crosses, put \(R_y=B-(2d+3)\).  Before the next wall,

   \[
   \gamma_p=\binom{d+3}{3}+U_2(R_y)-S_2(N_x)-\tau.
   \tag{3.3}
   \]

3. If both cross, put

   \[
   R_x=A-(2d+1),\qquad R_y=B-(2d+3).
   \]

   Before the next wall,

   \[
   \gamma_p=\Phi_\tau(R_x,D-2).
   \tag{3.4}
   \]

The orientation “\(x\) crosses but \(y\) does not” is impossible because
\(D\ge6\).  Equations (3.2)--(3.4) follow by literal Pascal normalization;
Lemma 4.6 of the inherited attack makes each fixed carry-count chamber
affine in its triangular remainder.

### Proposition 3.1 (only one rank-three wall at the first cap)

Suppose \(p\ge4\) is the first noncanonical row of (1.2), and \(d\ge3\).
Then each bottom block crosses at most one rank-three wall.  Consequently,
(3.2)--(3.4) are exhaustive at that row; no unlisted multiple-wall state
can occur.

#### Proof

Write \(a=A_{p-1}(b)\) and \(t=B_{p-1}(b)\).  Canonicality at the
preceding row gives the simultaneous integer bounds

\[
a\le d+2,\qquad t\le d+3.
\tag{3.5}
\]

The recurrence one row later is

\[
A=\binom a2+b+12-6p,\qquad
B=\binom t2+b+13-6p.
\tag{3.6}
\]

After one \(x\)-wall the residual is \(A-(2d+1)\).  A second wall
would therefore require

\[
A\ge (2d+1)+\binom{d+3}{2}.
\]

But (3.5)--(3.6) give

\[
\begin{aligned}
&(2d+1)+\binom{d+3}{2}-A\\
&\qquad\ge 3d-b+6p-9
 =3h+2b+3-3p>0.
\end{aligned}
\tag{3.7}
\]

Here the final inequality already follows from \(d\ge3\), since
\(3p\le h+b+1\).  Similarly, a second \(y\)-wall would require
\(B\ge(2d+3)+\binom{d+4}{2}\), whereas

\[
(2d+3)+\binom{d+4}{2}-B
\ge3d-b+6p-7
=3h+2b+5-3p>0.
\tag{3.8}
\]

Thus neither second crossing is reachable. \(\square\)

## 4. Resolution of the cap gate

The all-moving adaptive theorem was reduced, on this chamber, to the
following cap-recovery statement:

> If the first noncanonical row occurs before \(p_5(h)\), then one of its
> finitely parameterized wall normalizations has a nonnegative surplus at
> that row or produces a nonnegative surplus after a uniformly bounded
> number of further rows.

`NEGATIVE_CAP_RECOVERY.md` proves this statement in stronger form.  Every
first cap with \(4\le p\le p_5(h)\) has positive surplus at that same row,
uniformly for sufficiently large \(h\).  At the separate initial row,
\(\gamma_3<0\) implies \(\gamma_4>0\), with four exact formulas covering
all stable-cap orientations.

Consequently Corollary 2.2 is now unconditional on the full moving
double-borrow chamber: every \(b\ge5\) satisfying
\(b^2-b+4<4h\) seeds by \(p_5(h)=\log_2\log h+O(1)\).  This does not cover
the other initial borrow chambers.
