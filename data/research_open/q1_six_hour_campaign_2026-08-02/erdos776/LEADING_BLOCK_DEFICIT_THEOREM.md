# Leading-block deficit transport and five closed rank-five chambers

Date: 2026-08-02

## 1. Scope

This note continues `ONE_PROMOTION_RANK_FIVE_CHART.md`.  It is conditional
on exactly one rank-two promotion and on the two one-wall normalizations
in that note.  Within that chart it proves the strict rank-five sign in
five of the six observed combined chambers, including the unique reversed
tail.  The sixth chamber is refuted by the actual dyadic family in
`FINAL_CHAMBER_COUNTERFAMILY.md`.  This does not prove that the
one-promotion chart is exhaustive on the unbounded lattice.

Retain the notation

\[
n=\binom q2+r,\qquad b=q+K,\qquad
u=r+K-1,
\tag{1.1}
\]

\[
\tau=Kq+\binom K2+1-r=2h+b-2,
\tag{1.2}
\]

and

\[
R=\binom r2-\tau+1,\qquad
S=\binom u2-\tau.
\tag{1.3}
\]

The hypotheses \(h\ge224\), \(b\ge31\), and \(b<h\) give

\[
\tau\ge477.
\tag{1.4}
\]

Also \(K\ge4\).  Indeed, the one-promotion formula

\[
2h=(K-1)q+\binom{K-1}{2}+2-r
\]

gives \(h<b=q+K\) for \(K\le3\).  Consequently

\[
u\ge r+3,
\qquad
S-R=\binom u2-\binom r2-1\ge3r+2.
\tag{1.5}
\]

## 2. Full-block loss calculus

For integers \(j\ge1\), \(A\ge j\), and
\(0\le d\le\binom Aj\), define the full-block loss

\[
\boxed{
\Lambda_{j,A}(d)
 :=\binom A{j+1}-U_j\!\left(\binom Aj-d\right).}
\tag{2.1}
\]

This is exactly the leading-block increment that is erased by applying
superadditivity only to the small difference of two tails.

### Lemma 2.1 (deficit transport)

For \(0\le E\le D\le\binom Aj\),

\[
\Lambda_{j,A}(D)-\Lambda_{j,A}(E)
 \ge U_j(D-E),
\tag{2.2}
\]

and

\[
\Lambda_{j,A+1}(E)-\Lambda_{j,A}(E)\le E.
\tag{2.3}
\]

In particular,

\[
\boxed{
\Lambda_{j,A}(D)-\Lambda_{j,A+1}(E)
 \ge U_j(D-E)-E.}
\tag{2.4}
\]

Moreover

\[
\boxed{\Lambda_{j,A}(D)\ge U_j(D).}
\tag{2.5}
\]

#### Proof

Put \(C=\binom Aj\).  Superadditivity gives

\[
U_j(C-E)=U_j((C-D)+(D-E))
 \ge U_j(C-D)+U_j(D-E),
\]

which is (2.2).  Taking \(E=0\) gives (2.5).

For (2.3), put \(X=C-E\).  If

\[
X=\sum_i\binom{a_i}{i}
\]

is its \(j\)-canonical word, shift every upper index once:

\[
\sigma X:=\sum_i\binom{a_i+1}{i}.
\]

Pascal's identity gives

\[
U_j(\sigma X)-U_j(X)=X.
\tag{2.6}
\]

Because \(X<\binom Aj\), the lower cost of this diagonal shift obeys

\[
\sigma X-X=\sum_i\binom{a_i}{i-1}
 \le\binom A{j-1}.
\tag{2.7}
\]

The last inequality is sharp at the canonical word immediately below
\(\binom Aj\) and follows from the hockey-stick identity.  Monotonicity
and (2.6)--(2.7) therefore give

\[
U_j\!\left(X+\binom A{j-1}\right)-U_j(X)\ge X.
\]

Since
\(\binom{A+1}{j}-E=X+\binom A{j-1}\), substitution in (2.1) gives
(2.3).  Combining (2.2) and (2.3) proves (2.4). \(\square\)

## 3. Two exact rank-five deficit forms

Use \(A,B,p,v\) from (3.3) of
`ONE_PROMOTION_RANK_FIVE_CHART.md`.

### Proposition 3.1 (adjacent normalized caps)

Suppose \(B=A+1\), and define

\[
p=\binom A3-D,
\qquad
v=\binom{A+1}{3}-E.
\tag{3.1}
\]

Then the unified identity (3.6) becomes

\[
\boxed{
\gamma _5
=\Lambda_{3,A}(D)-\Lambda_{3,A+1}(E)+D-\tau.}
\tag{3.2}
\]

If \(D\ge E\), Lemma 2.1 preserves the full adjacent-block gain and
gives

\[
\boxed{
\gamma _5\ge U_3(G)+G-\tau,
\qquad G=D-E.}
\tag{3.3}
\]

#### Proof

Insert (3.1) into the definition (2.1).  The three full blocks cancel by

\[
\binom{A+1}{4}-\binom A4-\binom A3=0.
\]

This gives (3.2), and (2.4) gives (3.3). \(\square\)

### Proposition 3.2 (two-gap normalized caps)

Suppose \(B=A+2\).  In both such observed chambers
\(\delta_x=1,\delta_y=0\).  Put

\[
D=-P=\tau-1-U_2(\alpha)>0,
\qquad v=Q\ge0.
\tag{3.4}
\]

Then

\[
\boxed{
\gamma _5
=\Lambda_{3,A}(D)+U_3(v)-U_2(\alpha)-1
\ge U_3(D)+U_3(v)-U_2(\alpha)-1.}
\tag{3.5}
\]

#### Proof

Here \(p=\binom A3-D\), and the leading correction in (3.6) is
\(\binom{A+1}{4}\).  The identity

\[
\binom{A+1}{4}-\binom A4-\binom A3=0
\]

again leaves (3.5), with its inequality supplied by (2.5). \(\square\)

## 4. Two all-parameter convolution lifts

The next lemmas are independent of the chamber coordinates.  Their
finite bases are exact bounded lemmas, and their infinite tails are
proved analytically; no unbounded parameter range is replaced by a scan.

### Lemma 4.1 (rank-two split followed by rank three)

For every integer \(w\ge32\), all integers \(x,y\ge0\) with

\[
x+y\ge3w-7
\tag{4.1}
\]

satisfy, on putting

\[
G=U_2(x)+U_2(y)-1,
\]

the strict inequality

\[
\boxed{U_3(G)+G>\binom w2+1.}
\tag{4.2}
\]

#### Proof

For \(32\le w\le421\), monotonicity reduces (4.1) to
\(x+y=3w-7\).  Exact canonical arithmetic checks all 390 values of
\(w\), minimizing over the complete interval \(0\le x\le3w-7\).
The minimum margin in (4.2) is 178, attained at

\[
(w,x,y,G)=(32,40,49,215).
\tag{4.3}
\]

This is the finite base in
`verify_leading_block_deficit_theorem.py`.

It remains to prove every \(w\ge422\).  The leading-binomial definition
of Macaulay raising gives the uniform lower bounds

\[
U_2(N)\ge f_2(N):=
\frac{(\sqrt{2N}-3)_+^3}{6},
\tag{4.4}
\]

\[
U_3(N)\ge f_3(N):=
\frac{((6N)^{1/3}-4)_+^4}{24}.
\tag{4.5}
\]

Both functions are increasing and convex.  The first assertion follows
by taking the leading index \(a\) with
\(\binom a2\le N<\binom{a+1}{2}\), and the second is identical at rank
three.  Convexity follows by differentiation; the positive-part joins
have zero first derivative.

Jensen's inequality and (4.1) give

\[
G\ge M(w):=\frac{(\sqrt{3w-7}-3)^3}{3}-1.
\tag{4.6}
\]

Put

\[
s=\sqrt{3w-7}-3,\qquad
t=(2s^3-6)^{1/3}=(6M(w))^{1/3}.
\]

It is enough to show

\[
F(w):=\frac{(t-4)^4}{24}+M(w)-\binom w2-1>0.
\tag{4.7}
\]

At \(w=422\), the rational lower bounds

\[
s>\frac{812}{25},\qquad t>\frac{1023}{25}
\]

follow respectively from

\[
1259-\left(\frac{887}{25}\right)^2=\frac{106}{625}>0,
\]

\[
2\left(\frac{812}{25}\right)^3-6
-\left(\frac{1023}{25}\right)^3
=\frac{81739}{15625}>0.
\]

They give the exact anchor

\[
F(422)>\frac{51111641}{9375000}>0.
\tag{4.8}
\]

For \(s\ge32\), one has \(t\ge5s/4\), \(t\ge40\), and hence

\[
F'(w)\ge
\frac{437}{5250}s^2-2s-\frac{29}{6}>0.
\tag{4.9}
\]

The right side is positive at \(s=32\), and its derivative is positive
thereafter.  Thus (4.8)--(4.9) prove the complete tail. \(\square\)

### Lemma 4.2 (rank-three split after one rank-two lift)

For every integer \(r\ge32\), if \(D,V\ge0\) and

\[
D+V\ge U_2(3r+2)-1,
\tag{4.10}
\]

then

\[
\boxed{U_3(D)+U_3(V)>\binom r2+1.}
\tag{4.11}
\]

#### Proof

For \(32\le r\le277\), exact minimization over

\[
0\le D\le U_2(3r+2)-1
\]

gives minimum margin 258.  It occurs at

\[
(r,D,V)=(32,188,196).
\tag{4.12}
\]

This is the second finite base in the verifier.

For \(r\ge278\), (4.4) gives

\[
D+V\ge M(r):=
\frac{(\sqrt{6r+4}-3)^3}{6}-1.
\tag{4.13}
\]

Convexity of \(f_3\) gives

\[
U_3(D)+U_3(V)\ge2f_3(M(r)/2).
\]

Write

\[
s=\sqrt{6r+4}-3,\qquad
t=(s^3/2-3)^{1/3}.
\]

It remains to prove

\[
F(r):=\frac{(t-4)^4}{12}-\binom r2-1>0.
\tag{4.14}
\]

At \(r=278\), the rational lower bounds

\[
s>\frac{3789}{100},\qquad t>\frac{3759}{125}
\]

give

\[
F(278)>\frac{2674108561}{2929687500}>0.
\tag{4.15}
\]

For \(s\ge37\), one has \(t\ge3s/4>27\).  Differentiation gives

\[
F'(r)\ge
\left(\frac{450179}{2099520}-\frac16\right)s^2
-s-\frac13>0.
\tag{4.16}
\]

The right side and its derivative are positive at \(s=37\).  This proves
the entire tail. \(\square\)

## 5. Three chamber closures

### Theorem 5.1 (the \((++)\to(--)\) chamber)

Under the hypotheses of the one-promotion rank-five chart, every point in

\[
(R,S)=(++),\qquad(P,Q)=(--)
\]

has \(\gamma _5>0\).

#### Proof

Here \(a=q\), \(A=q-1\), and

\[
D=-P,\qquad E=-Q,\qquad
G=D-E=Q-P.
\]

Since \(\alpha=R\ge0\), (1.3) gives

\[
\tau\le\binom r2+1.
\tag{5.1}
\]

Together with (1.4), this forces \(r\ge32\).  Also

\[
\beta-\alpha=S-R\ge3r+2.
\]

Superadditivity gives

\[
G=U_2(\beta)-U_2(\alpha)-1
 \ge U_2(3r+2)-1>0.
\tag{5.2}
\]

Thus \(D\ge E\).  Apply Lemma 4.1 with
\(w=r,x=3r+2,y=0\), then use (3.3) and (5.1):

\[
\gamma _5\ge U_3(G)+G-\tau>0.
\]

\(\square\)

### Theorem 5.2 (the \((++)\to(-+)\) chamber)

Under the same hypotheses, every point in

\[
(R,S)=(++),\qquad(P,Q)=(-+)
\]

has \(\gamma _5>0\).

#### Proof

Put \(D=-P>0\) and \(V=Q\ge0\).  As above, \(r\ge32\) and
\(\beta-\alpha\ge3r+2\).  Hence

\[
D+V
=U_2(\beta)-U_2(\alpha)-1
\ge U_2(3r+2)-1.
\tag{5.3}
\]

Moreover, \(P<0\) and
\(\tau=\binom r2-\alpha+1\) give

\[
U_2(\alpha)+1\le\binom r2.
\tag{5.4}
\]

Lemma 4.2 and the two-gap formula (3.5) now give

\[
\gamma _5
\ge U_3(D)+U_3(V)-U_2(\alpha)-1>0.
\]

\(\square\)

### Theorem 5.3 (the reversed \((-+)\to(+-)\) chamber)

Under the same hypotheses, every point in

\[
(R,S)=(-+),\qquad(P,Q)=(+-)
\]

has \(\gamma _5>0\).

#### Proof

Here \(a=A=q-1\).  Put

\[
\rho=-R>0,\qquad \beta=S\ge0.
\]

Then

\[
\alpha=\binom A2-\rho,\qquad
\rho+\beta=S-R=\binom u2-\binom r2-1.
\tag{5.5}
\]

Since \(\beta=S=\binom u2-\tau\ge0\), one has
\(\tau\le\binom u2\).  Equations (1.4)--(1.5) imply

\[
u\ge32,
\qquad
\rho+\beta\ge3u-7.
\tag{5.6}
\]

For the adjacent caps in this chamber,

\[
\begin{aligned}
D&=\binom A3-P
  =\Lambda_{2,A}(\rho)+\tau-1,\\
E&=-Q=\tau-U_2(\beta).
\end{aligned}
\]

Consequently

\[
G:=D-E
=\Lambda_{2,A}(\rho)+U_2(\beta)-1
\ge U_2(\rho)+U_2(\beta)-1.
\tag{5.7}
\]

Lemma 4.1, with \(w=u,x=\rho,y=\beta\), gives

\[
U_3(G)+G>\binom u2+1>\tau.
\]

In particular \(D>E\), and (3.3) proves \(\gamma _5>0\).
\(\square\)

### Theorem 5.4 (the \((--)\to(-+)\) chamber)

Under the same hypotheses, every point in

\[
(R,S)=(--),\qquad(P,Q)=(-+)
\]

has \(\gamma _5>0\).

#### Proof

Here

\[
a=q-1,\qquad A=q-2,
\]

and the two-gap variables are

\[
D=-P>0,\qquad V=Q\ge0.
\tag{5.8}
\]

First suppose \(q\ge216\).  Since

\[
\alpha=\binom{q-1}{2}+\binom r2-\tau+1\ge0
\tag{5.9}
\]

and \(r<q\), one has \(\tau<q^2\).  The condition \(P<0\) gives
\(U_2(\alpha)<q^2\).  Applying (4.4) shows

\[
\sqrt{2\alpha}<3+6^{1/3}q^{2/3}\le\frac q3,
\]

and hence

\[
\alpha<\frac{q^2}{18}.
\tag{5.10}
\]

The middle inequality holds for every \(q\ge216\): write
\(q=x^3\), use \(x\ge6\) and \(6^{1/3}<11/6\), and observe that

\[
\frac{x^3}{3}-\frac{11x^2}{6}-3>0.
\]

On the other hand, (5.9) and
\(\tau=Kq+\binom K2+1-r\) give

\[
Kq+\binom K2\ge\binom{q-1}{2}-\alpha.
\tag{5.11}
\]

If \(K<q/3\), the left side of (5.11) is less than
\(7q^2/18\), whereas (5.10) makes the right side greater than

\[
\frac{4q^2}{9}-\frac{3q}{2}+1
\ge\frac{7q^2}{18}.
\]

The last inequality holds already for \(q\ge27\).  Thus

\[
K\ge\frac q3.
\tag{5.12}
\]

Put \(W=\beta-\alpha\).  Equations (1.3) and (5.12) give

\[
\begin{aligned}
W
&=q-2+(K-1)r+\binom{K-1}{2}\\
&\ge q-2+\binom{K-1}{2}
 \ge\frac{q^2}{18}.
\end{aligned}
\tag{5.13}
\]

Since \(r<q\) and \(q\ge216\),

\[
W\ge3(q+r)+2.
\tag{5.14}
\]

Superadditivity at rank two now preserves the large separation:

\[
D+V
=U_2(\beta)-U_2(\alpha)-1
\ge U_2(W)-1
\ge U_2(3(q+r)+2)-1.
\tag{5.15}
\]

Apply Lemma 4.2 with its parameter equal to \(q+r\).  It gives

\[
U_3(D)+U_3(V)>\binom{q+r}{2}+1.
\tag{5.16}
\]

Finally, \(P<0\) and (5.9) give

\[
U_2(\alpha)+1
\le\tau-1
\le\binom{q-1}{2}+\binom r2
<\binom{q+r}{2}+1.
\tag{5.17}
\]

Equations (3.5), (5.16), and (5.17) prove \(\gamma _5>0\) for
every \(q\ge216\).

It remains only to take \(2\le q\le215\).  Here one promotion gives

\[
4\le K\le q+1,\qquad 0\le r\le q-K+1,
\]

so the base is finite without any hidden strip parameter.  Complete exact
canonical enumeration, including the parity and \(h\ge224>b\) conditions,
finds one point in this chamber:

\[
(q,K,r;b,h)=(35,13,0;48,244),
\qquad \gamma _5=4923.
\tag{5.18}
\]

The exhaustive base is checked by
`check_double_negative_to_single_borrow_base`; among 133 negative
antecedents in this complete \(q\)-range, (5.18) is the unique target
point. \(\square\)

### Theorem 5.5 (the \((--)\to(--)\) chamber)

Under the same hypotheses, every point in

\[
(R,S)=(--),\qquad(P,Q)=(--)
\]

has \(\gamma _5>0\).

#### Proof

For \(q\ge216\), the argument (5.9)--(5.14) is unchanged: it uses only
the first \((--)\) chamber and \(P<0\).  Hence

\[
K\ge q/3,
\qquad
W:=\beta-\alpha\ge q^2/18\ge3(q+r)+2.
\tag{5.19}
\]

Now put

\[
D=-P>0,\qquad E=-Q>0.
\]

Their adjacent-cap deficit gap is

\[
G:=D-E
=U_2(\beta)-U_2(\alpha)-1
\ge U_2(W)-1>0.
\tag{5.20}
\]

Lemma 4.1, with parameter \(q+r\) and split \((x,y)=(W,0)\), gives

\[
U_3(G)+G>\binom{q+r}{2}+1.
\tag{5.21}
\]

Since \(\alpha\ge0\), (5.9) also gives

\[
\tau\le\binom{q-1}{2}+\binom r2+1
<\binom{q+r}{2}+1.
\tag{5.22}
\]

Thus \(D>E\), and Proposition 3.1 proves \(\gamma _5>0\).

For \(2\le q\le215\), the same complete enumeration used in Theorem
5.4 finds precisely three target points:

\[
\begin{array}{c|c|c|c|c}
(q,K,r;b,h)&(D,E)&G&D\text{-loss lower bound}&\gamma _5\\ \hline
(34,13,0;47,238)&(515,66)&449&1236&4222\\
(36,14,0;50,274)&(595,120)&475&1274&4599\\
(41,16,0;57,361)&(775,31)&744&2548&9010
\end{array}
\tag{5.23}
\]

The fourth column is the rigorous lower bound
\(U_3(G)+G-\tau\) from (3.3), not the exact surplus.  All three are
strictly positive.  The verifier forms the antecedent before filtering by
the two first-tail signs, checks both one-wall caps, and only then tests
\(P,Q<0\); hence (5.23) is the complete finite base, not an offset-limited
census. \(\square\)

## 6. Exact six-chamber boundary

The status inside the conditional one-promotion/two-one-wall chart is now

| first tails | second tails | status |
|---|---|---|
| \((--)\) | \((++)\) | **REFUTED at rank five** by an infinite actual dyadic family; every point of that family recovers at rank six |
| \((--)\) | \((--)\) | **PROVED** by Theorem 5.5 |
| \((--)\) | \((-+)\) | **PROVED** by Theorem 5.4 |
| \((-+)\) | \((+-)\) | **PROVED** by Theorem 5.3 |
| \((++)\) | \((--)\) | **PROVED** by Theorem 5.1 |
| \((++)\) | \((-+)\) | **PROVED** by Theorem 5.2 |

Thus the unique reversed tail and four further chambers are closed
uniformly.  The remaining row does not admit the proposed positive sign:
`FINAL_CHAMBER_COUNTERFAMILY.md` takes

\[
K=6,\qquad r=10,\qquad
h=224\,2^s,\qquad s\equiv2\pmod4,
\]

and obtains infinitely many legal points in \((--)\to(++)\) with

\[
\gamma _5=4\,302\,695-6q<0.
\]

The first is \(s=14,q=1\,468\,006\), where
\(\gamma _5=-4\,505\,341\).  This family has \(\gamma _6>0\) everywhere;
after one finite exceptional word its stable formula is

\[
\gamma _6=9\,256\,181\,220\,279+104q>0.
\]

The finite census through \(b=250\) is unchanged, but it is no longer the
evidence for the five proved rows: their unbounded quantifiers are supplied
by Lemmas 2.1, 4.1, and 4.2 and the exact \(q\le215\) bases.  The
one-promotion and one-wall exhaustiveness premises remain open as global
classification questions.  The rank-five bridge is refuted, while the
adaptive-seed theorem and Erdős #776 remain open.
