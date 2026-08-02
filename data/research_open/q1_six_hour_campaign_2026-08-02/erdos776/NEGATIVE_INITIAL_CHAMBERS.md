# The remaining negative-offset initial chambers

This note treats the two initial borrow states to the right of the
double-borrow chamber.  Let

\[
c=h+b-2,\qquad T=2h+b-3,\qquad \tau=T+1,
\]

so that

\[
x_3=\binom c3+\binom{b-1}{2}+2-2h,\qquad
y_3=\binom{c+1}{3}+\binom b2+2-2h.
\tag{1.1}
\]

Throughout, \(h\ge224\), \(5\le b<h\), and \(h\) is dyadic as in the
main campaign.

## 1. The asymmetric initial chamber is closed

Suppose

\[
\binom{b-1}{2}+2-2h=-q<0,\qquad
r:=b-1-q\ge0.
\tag{1.2}
\]

Thus only \(x_3\) borrows from its leading rank-three term.  Since
\(1\le q\le b-1\), literal Pascal normalization gives

\[
\boxed{
\gamma_3=
\frac{q(2h+2b-q-7)}2+U_2(r)-(2h+b-2).}
\tag{1.3}
\]

### Proposition 1.1 (asymmetric initial seed)

Every point of (1.2) has a nonnegative seed by rank four.  More precisely,
\(\gamma_3>0\) for \(q\ge2\); if \(q=1\), then \(\gamma_4>0\).

#### Proof

After dropping the nonnegative \(U_2(r)\), the polynomial part of (1.3)
is strictly increasing in \(q\) on \(2\le q\le b-1\), because its forward
difference is \(h+b-q-4\ge h-3\).  At \(q=2\) it equals \(b-7>0\).

It remains to treat \(q=1\).  Then

\[
2h=\binom{b-1}{2}+3,\qquad r=b-2,
\tag{1.4}
\]

and \(\gamma_3=U_2(b-2)-h-2\) need not be positive.  Put

\[
r_y=b-7+U_2(b-2).
\tag{1.5}
\]

The exact rank-four normalization is

\[
\boxed{
\gamma_4=
\binom{c-4}{2}+\binom{r_y}{2}
-\binom{b-9}{2}-\tau>0.}
\tag{1.6}
\]

Indeed, the two rank-two tails entering the final \(U_2\)-difference are

\[
X=\binom{c-5}{2}+(b-10),\qquad
Y=\binom{c-3}{2}+r_y.
\]

Substitution gives (1.6).  After dropping \(\binom{r_y}{2}\), the
remaining exact certificate is

\[
\binom{c-4}{2}-\binom{b-9}{2}-\tau
=\frac{b^4+2b^3-67b^2+284b-1184}{32}.
\tag{1.7}
\]

On writing \(b=x+31\), the coefficients from degree four to degree zero
are

\[
\frac1{32},\quad\frac{63}{16},\quad\frac{5885}{32},
\quad\frac{30265}{8},\quad28948,
\]

so (1.7) is positive for every \(b\ge31\).  The identity and positivity
are checked independently in verify_negative_initial_chambers.py.
\(\square\)

## 2. Exact dimensionless chart for the no-borrow chamber

Now put

\[
n=\binom{b-1}{2}+2-2h\ge0,\qquad m=b-1,\qquad
H=\binom b2+1.
\tag{2.1}
\]

Then

\[
\tau=H-n,\qquad
z=U_2(n),\qquad
\Delta=U_2(n+m)-z,\qquad S=n+z.
\tag{2.2}
\]

The rank-three surplus loses every occurrence of \(h\):

\[
\boxed{\gamma_3=\Delta-H.}
\tag{2.3}
\]

If \(\gamma_3<0\), the rank-four pair is

\[
x_4=\binom c4+x_0,\qquad
y_4=\binom{c+1}{4}+y_0,
\tag{2.4}
\]

where

\[
\boxed{
x_0=S-H+1,\qquad
y_0=S+\gamma_3=x_0+(\Delta-1).}
\tag{2.5}
\]

Thus exactly three sign states are reachable:

1. \(x_0<y_0<0\);
2. \(x_0<0\le y_0\);
3. \(0\le x_0<y_0\).

The reverse asymmetric state is impossible.  Equality belongs to the
non-borrowing side.

The relaxed integral lattice is

\[
\begin{gathered}
b\ge31,\qquad n\ge0,\qquad
n\equiv\binom{b-1}{2}+2\pmod2,\\
h=\frac{\binom{b-1}{2}+2-n}{2}\ge224,\qquad b<h.
\end{gathered}
\tag{2.6}
\]

The low blocks in the following formulas are genuinely below their next
Macaulay caps.  Direct subtraction gives

\[
 \binom c2-n=\frac{(h-1)(2b+h)}2>0,
 \qquad
 \binom{c+1}{2}-(n+m)
 =\frac{(h-1)(2b+h+2)}2>0.
\tag{2.6a}
\]

If \(N<\binom ap\), its \(p\)-canonical word has all upper indices
below \(a\), and hence \(U_p(N)<\binom a{p+1}\).  Applying this to
(2.6a) gives

\[
 U_2(n)<\binom c3,\qquad
 U_2(n+m)<\binom{c+1}{3}.
\tag{2.6b}
\]

Therefore, whenever \(x_0,y_0\ge0\), the two expressions in (2.4) are
legal rank-four canonical concatenations; subtracting \(T\) or \(\tau\)
cannot reach the displayed leading cap.

At a non-borrowing rank-four point \(x_0\ge0\),

\[
\boxed{
\gamma_4=
U_3(y_0)-U_3(x_0)-x_0-\tau.}
\tag{2.7}
\]

If this is negative, formally put

\[
X_1=U_3(x_0)-\tau+1,\qquad
Y_1=U_3(y_0)-\tau.
\tag{2.8}
\]

The same cap argument applies one level later.  From
\(x_0<\binom c3\) and \(y_0<\binom{c+1}{3}\), one has

\[
 U_3(x_0)<\binom c4,\qquad
 U_3(y_0)<\binom{c+1}{4}.
\tag{2.8a}
\]

Thus, if \(X_1,Y_1\ge0\), they are automatically below the two next
caps.  Formula (2.9) then follows from legal canonical concatenation,
not from an implicit no-borrow assumption.

Provided \(X_1,Y_1\ge0\), the next exact target is

\[
\boxed{
\gamma_5=U_4(Y_1)-U_4(X_1)-X_1-\tau.}
\tag{2.9}
\]

The proviso is essential: without it a new high-rank borrow changes
(2.9).  It can nevertheless be discharged uniformly in the asymptotic
range.

Two cancellations put the remaining gate in a self-similar form.  If
\(d=\Delta-1=y_0-x_0\) and
\(e=Y_1-X_1=U_3(y_0)-U_3(x_0)-1\), then

\[
x_0+\tau=U_2(n)+1,
\qquad
\gamma_4=U_3(x_0+d)-U_3(x_0)-U_2(n)-1,
\tag{2.9a}
\]

and

\[
X_1+\tau=U_3(x_0)+1,
\qquad
\gamma_5=U_4(X_1+e)-U_4(X_1)-U_3(x_0)-1.
\tag{2.9b}
\]

Thus \(\gamma_4<0\) is exactly the integer bound
\(U_3(x_0+d)-U_3(x_0)\le U_2(n)\); no \(H\) or \(\tau\) remains in
the strict promotion target.

### Lemma 2.1 (eventual rank-five low-block nonnegativity)

For all sufficiently large \(h\), uniformly on (2.6),

\[
\gamma_3<0,\qquad x_0\ge0,\qquad\gamma_4<0
\quad\Longrightarrow\quad X_1>0,\quad Y_1>0.
\tag{2.10}
\]

#### Proof

For fixed rank \(j\), Macaulay raising has the uniform estimate

\[
U_j(N)=c_jN^{1+1/j}+O(N),\qquad c_j>0.
\tag{2.11}
\]

Equation (2.6) and \(n\ge0\) give

\[
h\le\frac12\binom{b-1}{2}+1.
\]

Consequently \(h\to\infty\) forces \(b\to\infty\), and
\(\tau=2h+b-2=O(b^2)\), uniformly on the lattice.

Suppose toward a contradiction that a sequence in the antecedent has
\(X_1\le0\).  This gives
\(U_3(x_0)<\tau\), hence \(x_0=O(b^{3/2})\).  But

\[
n+U_2(n)=x_0+H-1=\Theta(b^2),
\]

so (2.11) forces \(n=\Theta(b^{4/3})\).  Applying (2.11) at rank two,
with \(m=b-1\), now gives

\[
\Delta=U_2(n+m)-U_2(n)=\Theta(b\sqrt n)
       =\Theta(b^{5/3}).
\]

Thus \(d:=\Delta-1=\Theta(b^{5/3})\),
\(y_0=x_0+d=\Theta(b^{5/3})\), and

\[
U_3(y_0)=\Theta(b^{20/9}),
\]

whereas \(U_3(x_0)+x_0+\tau=O(b^2)\).  Equation (2.7) would then give
\(\gamma_4>0\), a contradiction.  Hence \(X_1>0\).

Finally \(x_0\ge0\) already forces \(n=\Omega(b^{4/3})\).  Standard
Macaulay superadditivity says, for all \(A,D\ge0\),

\[
U_3(A+D)-U_3(A)\ge U_3(D).
\tag{2.12}
\]

This is Lemma 5.4 of the previously audited `FOURTH_ATTACK.md`: if
\(a=U_j(A)\) and \(c=U_j(D)\), Galois adjunction and subadditivity of
the lower shadow give

\[
\operatorname{KK}_{j+1}(a+c)
\le \operatorname{KK}_{j+1}(a)+\operatorname{KK}_{j+1}(c)
\le A+D,
\]

and adjunction once more gives \(a+c\le U_j(A+D)\).  The same lemma at
rank two gives

\[
\Delta=U_2(n+b-1)-U_2(n)\ge U_2(b-1),
\]

so \(d=\Delta-1\to\infty\).  Applying (2.12) with
\((A,D)=(x_0,d)\) yields
\(U_3(y_0)-U_3(x_0)\ge U_3(d)\to\infty\) uniformly.  Therefore

\[
Y_1-X_1=U_3(y_0)-U_3(x_0)-1>0
\]

for sufficiently large \(h\).  Therefore \(Y_1>0\). \(\square\)

Equations (2.1)--(2.9) isolate the final negative-offset initial gate.
The original bounded relaxed-lattice scans found:

- both rank-four borrow states always have \(\gamma_4>0\);
- the no-borrow state can have \(\gamma_4<0\);
- every point in those bounded scans had \(\gamma_5>0\).

Those finite statements were falsifier evidence, not a universal proof.
The proposed no-borrow implication was

\[
\gamma_3<0,\quad x_0\ge0,\quad\gamma_4<0
\quad\Longrightarrow\quad\gamma_5>0
\tag{2.13}
\]

on (2.6).  It is now **refuted** by the actual dyadic family in
`FINAL_CHAMBER_COUNTERFAMILY.md`.  In that family

\[
K=6,\qquad r=10,\qquad
h=224\,2^s,\qquad s\equiv2\pmod4,
\]

and every \(s\ge14\) has

\[
\gamma_3=44-6q<0,\qquad
\gamma_4=2906-6q<0,\qquad
\gamma_5=4\,302\,695-6q<0.
\]

All cap-legality conditions are literal, so this is not a failure of the
formal proviso in (2.9).  The same family has \(\gamma_6>0\) everywhere.
Thus (2.13) and a fixed rank-five seed are false, while the adaptive-seed
problem and the symbolic sign proofs for the two rank-four borrow states
remain open.
