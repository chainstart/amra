# The one-promotion rank-five chamber chart

Date: 2026-08-02

## 1. Scope and triangular coordinates

This note is conditional on the remaining no-borrow antecedent of
`NEGATIVE_INITIAL_CHAMBERS.md` and on exactly one rank-two promotion.  It
does not assert that the one-promotion chart is exhaustive on the unbounded
lattice.

Write

\[
n=\binom q2+r,\qquad 0\le r<q,\qquad b=q+K,
\tag{1.1}
\]

and suppose

\[
n+b-1=\binom{q+1}{2}+u,\qquad
u=r+K-1,\qquad 0\le u<q+1.
\tag{1.2}
\]

Then

\[
\tau=Kq+\binom K2+1-r,
\qquad
\gamma_3=(K-1)r-K(q+1),
\tag{1.3}
\]

and the rank-four low blocks are

\[
x_0=\binom q3+R,\qquad
y_0=\binom{q+1}{3}+S,
\tag{1.4}
\]

where

\[
R=\binom{r+1}{2}-Kq-\binom K2,
\qquad
S=R+\binom u2-\binom r2-1.
\tag{1.5}
\]

In particular \(R<S\) on the open antecedent.  The three observed
rank-three tail chambers are \((--),(-+),(++)\).

## 2. A unified first normalization

Put

\[
\epsilon_x=\mathbf 1_{R<0},\qquad
\epsilon_y=\mathbf 1_{S<0},
\tag{2.1}
\]

and define

\[
\begin{aligned}
a&=q-\epsilon_x,
&\alpha&=R+\epsilon_x\binom{q-1}{2},\\
g&=1+\epsilon_x-\epsilon_y,
&\beta&=S+\epsilon_y\binom q2.
\end{aligned}
\tag{2.2}
\]

Assume the displayed borrow crosses at most one rank-three wall, namely

\[
0\le\alpha<\binom a2,
\qquad
0\le\beta<\binom{a+g}{2}.
\tag{2.3}
\]

Literal Pascal subtraction then gives the single formula

\[
\boxed{
x_0=\binom a3+\alpha,
\qquad
y_0=\binom{a+g}{3}+\beta.}
\tag{2.4}
\]

The leading gap is \(g=1\) in chambers \((--),(++)\), but \(g=2\) in
the asymmetric chamber \((-+)\).  This gap must be retained at the next
rank.

## 3. The second normalization and exact \(\gamma_5\)

Define the raw rank-five tails

\[
P=U_2(\alpha)-\tau+1,
\qquad
Q=U_2(\beta)-\tau.
\tag{3.1}
\]

Let

\[
\delta_x=\mathbf 1_{P<0},\qquad
\delta_y=\mathbf 1_{Q<0},
\tag{3.2}
\]

and put

\[
\begin{aligned}
A&=a-\delta_x,
&p&=P+\delta_x\binom{a-1}{3},\\
B&=a+g-\delta_y,
&v&=Q+\delta_y\binom{a+g-1}{3}.
\end{aligned}
\tag{3.3}
\]

Assume again that at most one wall is crossed:

\[
0\le p<\binom A3,
\qquad
0\le v<\binom B3.
\tag{3.4}
\]

Then

\[
X_1=\binom A4+p,
\qquad
Y_1=\binom B4+v.
\tag{3.5}
\]

### Theorem 3.1 (unified rank-five identity)

Under (1.1)--(3.4), the exact next surplus is

\[
\boxed{
\begin{aligned}
\gamma_5={}&
 \binom B5-\binom A5-\binom A4
 +U_3(v)-U_3(p)-U_2(\alpha)-1\\
&\quad-\delta_x\binom{a-1}{3}.
\end{aligned}}
\tag{3.6}
\]

#### Proof

Equations (2.4) and (3.1) give

\[
X_1=\binom a4+P,
\qquad
Y_1=\binom{a+g}{4}+Q.
\]

The one-wall normalizations (3.2)--(3.4) give (3.5), hence

\[
U_4(X_1)=\binom A5+U_3(p),
\qquad
U_4(Y_1)=\binom B5+U_3(v).
\]

Substitute these identities and \(X_1=\binom A4+p\) into

\[
\gamma_5=U_4(Y_1)-U_4(X_1)-X_1-\tau.
\]

Finally (3.1) and (3.3) give

\[
p+\tau=U_2(\alpha)+1
 +\delta_x\binom{a-1}{3},
\]

which proves (3.6). \(\square\)

The leading correction

\[
\binom B5-\binom A5-\binom A4
\tag{3.7}
\]

cannot be dropped.  In particular, when \(B=A\) it equals
\(-\binom A4\).  This dangerous case would require
\(g+\delta_x-\delta_y=0\).  It does **not** occur in any of the six
finite chambers below: the only reverse-tail state starts from
\((-+)\), where \(g=2\), and hence still has \(B=A+1\).

## 4. Six reachable finite chambers

An exact scan of the full relaxed lattice through \(b=250\), restricted
only after forming the antecedent, finds 219 points.  Every point has
exactly one rank-two promotion and crosses at most one wall at each of the
two normalizations above.  The combined chamber census is

| first tails \((R,S)\) | second tails \((P,Q)\) | \(g\) | count | minimum \(\gamma_5\) | minimizer \((q,K,r;b,h)\) |
|---|---:|---:|---:|---:|---:|
| \(--\) | \(++\) | 1 | 164 | 13241 | \((81,8,0;89,295)\) |
| \(--\) | \(--\) | 1 | 3 | 4222 | \((34,13,0;47,238)\) |
| \(--\) | \(-+\) | 1 | 1 | 4923 | \((35,13,0;48,244)\) |
| \(-+\) | \(+-\) | 2 | 1 | 78157 | \((214,4,41;218,303)\) |
| \(++\) | \(--\) | 1 | 31 | 37452 | \((165,4,36;169,232)\) |
| \(++\) | \(-+\) | 1 | 19 | 48826 | \((166,4,37;170,233)\) |

For these six rows the leading correction (3.7) is completely explicit:

| transition | \(B-A\) | value of (3.7) |
|---|---:|---:|
| \((--)\to(++)\) | 1 | \(0\) |
| \((--)\to(--)\) | 1 | \(0\) |
| \((--)\to(-+)\) | 2 | \(\binom{A+1}{4}\) |
| \((-+)\to(+-)\) | 1 | \(0\) |
| \((++)\to(--)\) | 1 | \(0\) |
| \((++)\to(-+)\) | 2 | \(\binom{A+1}{4}\) |

Thus the unique reversed second tail is not itself a negative
leading-block event.  The two \((-+)\) second chambers instead retain a
strictly positive quartic reservoir; all other observed rows retain an
exactly cancelling adjacent-block increment.

The fourth row is important: the first asymmetric chamber has leading gap
two and reaches \(P\ge0>Q\).  Thus a recursive argument that assumes the
same three tail signs at every level silently omits a legal state.

The census and all 219 instances of (3.6) are checked independently in
`verify_one_promotion_rank_five_chart.py`.  This is finite falsifier
evidence, not a universal positivity proof.

## 5. Subsequent status of the sign problem

Formula (3.6) preserves the full leading-block increment that is lost in
the insufficient bound

\[
U_3(x_0+d)-U_3(x_0)\ge U_3(d).
\]

Five of the six rows are subsequently proved positive in
`LEADING_BLOCK_DEFICIT_THEOREM.md`.  The sixth is genuinely negative:
`FINAL_CHAMBER_COUNTERFAMILY.md` gives infinitely many actual dyadic points
with \(K=6,r=10\) in \((--)\to(++)\) and

\[
\gamma_5=4\,302\,695-6q<0.
\]

The same family is positive at rank six.  Therefore the rank-five bridge
is refuted, not Erdős #776.  The one-promotion and two one-wall premises
remain open only as global classification questions; the counterfamily
itself satisfies them directly.
