# Uniform recovery from the first negative-side cap

This note closes the cap gate left open in `NEGATIVE_PRECAP_ATLAS.md` for
the double-borrow chamber \(b\ge5\).  All claims are about the local paired
orbit defined there.  The transfer to the global orbit is recorded in
Section 4.

Write

\[
s=b+12-6p,\qquad d=h+b+4-3p,\qquad
\tau=2h+b-2=2d+2-s.
\tag{1.1}
\]

At a first noncanonical row \(p\ge4\), put

\[
a=A_{p-1}(b),\qquad t=B_{p-1}(b),\qquad q=t-a,
\qquad A=\binom a2+s,
\qquad B=\binom t2+s+1,
\qquad D=B-A.
\tag{1.2}
\]

Previous-row canonicality gives \(a\le d+2\) and \(t\le d+3\).
Proposition 3.1 of the atlas proves that neither low block can cross more
than one rank-three wall.

## 1. Two uniform growth lemmas

### Lemma 1.1 (the adjacent constant gap)

For every formal pre-cap row \(r\ge3\),

\[
q_r:=B_r(b)-A_r(b)>0,\qquad q_r^2\ge2A_r(b).
\tag{1.3}
\]

Consequently, at the next row,

\[
D=q_ra+\binom{q_r}{2}+1\ge q_ra
   \ge \sqrt{2a}\,a.
\tag{1.4}
\]

#### Proof

At rank three,

\[
q_3=b+1,\qquad q_3^2-2A_3=b+13>0.
\]

Also \(A_r(b)\ge b\).  For \(r=3\) this is immediate; at \(r=4\) the
minimum is \(A_4(5)=29\), and the elementary induction
\(A_r(b)\ge6r+5\) for \(r\ge4\) keeps
\(\binom{A_r}{2}\ge6r-6\).  Thus the recurrence preserves
\(A_{r+1}\ge b\).

If \(a=A_r\) and \(q=q_r\), then

\[
q_{r+1}=qa+\binom q2+1\ge qa,
\qquad
A_{r+1}\le\binom a2+b\le\binom a2+a\le a^2.
\]

Hence \(q^2\ge2a\) implies

\[
q_{r+1}^2\ge q^2a^2\ge2a^3\ge2A_{r+1}.
\]

This proves the induction and (1.4). \(\square\)

### Lemma 1.2 (rank-two growth)

For the Macaulay raising operator \(U_2\),

\[
U_2(N)=\frac{\sqrt2}{3}N^{3/2}+O(N)
\tag{1.5}
\]

with an absolute uniform error.  In particular, if \(a\to\infty\),

\[
n=O(a^2),\qquad m=\Omega(a^{3/2}),\qquad R=O(a^2),
\]

then

\[
U_2(n+m)-U_2(n)-n-R>0
\tag{1.6}
\]

for all sufficiently large \(a\).

#### Proof

If \(N=\binom z2+r\), \(0\le r<z\), then

\[
U_2(N)=\binom z3+\binom r2,
\qquad z=\sqrt{2N}+O(1),
\]

which gives (1.5).  For (1.6), split into \(m\le n\) and \(m>n\).
In the first case \(m=\Omega(a^{3/2})\) also forces
\(n=\Omega(a^{3/2})\).  The main-term increment in (1.5) is
\(\Omega(m\sqrt n)=\Omega(a^{9/4})\), while the total error is
\(O(n+m)\); moreover \(m/\sqrt n=\Omega(\sqrt a)\), so that increment
dominates both the error and \(R=O(a^2)\).  In the second case the
main-term increment is \(\Omega(m^{3/2})\), while the error is
\(O(n+m)\).  Both main terms dominate \(n+R=O(a^2)\). \(\square\)

## 2. Every later first cap is immediately positive

The initial double-borrow inequality is

\[
\binom{b-1}{2}-(2h-b-1)<0,
\quad\text{equivalently}\quad b^2-b+4<4h.
\tag{2.1}
\]

Thus \(b=O(\sqrt h)\).  Uniformly for \(p\le p_5(h)\), where
\(p_5(h)=O(\log\log h)\),

\[
d\sim h,\qquad s=o(d),\qquad \tau=2d+o(d).
\tag{2.2}
\]

### Proposition 2.1 (first-cap sign for \(p\ge4\))

For all sufficiently large \(h\), if the first noncanonical row occurs at
\(4\le p\le p_5(h)\), then

\[
\gamma_p>0.
\tag{2.3}
\]

The threshold is uniform in every moving integer \(b\ge5\) satisfying
(2.1).

#### Proof

Proposition 3.1 of the atlas makes the following cases exhaustive.

**No rank-three wall.**  If \(A<d\), first noncanonicality forces
\(B\ge d+1\).  Put \(w=d-A\).  Direct normalization of (3.2) in the
atlas gives

\[
\gamma_p=
 \frac{w(2d-w+1)}2+\binom{D-w-1}{2}-\tau.
\tag{2.4}
\]

Here \(1\le w\le D-1\).  For \(w\ge3\), the first term is at least
\(3d-3>\tau\).  For \(w=1,2\),
\(\binom a2=d+o(d)\), so \(a=\Theta(\sqrt d)\).  Lemma 1.1 gives
\(D=\Omega(d^{3/4})\), and the triangular term in (2.4) is
\(\Omega(d^{3/2})\), which dominates \(\tau\).

If \(A\ge d\), put \(v=A-d\).  The same literal normalization gives

\[
\gamma_p=
 \binom{v+D-1}{2}-\binom{v+1}{2}-\tau.
\tag{2.5}
\]

The binomial difference is increasing in \(v\), hence is at least
\(\binom{D-1}{2}\).  Now \(A\ge d\) gives
\(\binom a2\ge d-o(d)\); (1.4) again makes this lower bound
\(\Omega(d^{3/2})\).

**Only the \(y\)-block crosses its rank-three wall.**  Put
\(R=B-(2d+3)\ge0\).  If \(A<d\), (3.3) becomes

\[
\gamma_p=(d+1)^2+U_2(R)-\binom{A+1}{2}-\tau>0,
\tag{2.6}
\]

because \(A\le d-1\), so the displayed polynomial difference is
\(\Theta(d^2)\).

If \(A\ge d\), put \(w=2d-A\ge0\).  Then

\[
R=D-w-3,\qquad
\gamma_p=
 \binom{d+2}{2}-\binom{d-w+1}{2}+U_2(R)-\tau.
\tag{2.7}
\]

For \(w\ge2\), the first binomial difference is at least \(3d>\tau\).
For \(w=0,1\), \(\binom a2=2d+o(d)\), while
\(R\sim D=\Omega(d^{3/4})\).  Equation (1.5) gives
\(U_2(R)=\Omega(d^{9/8})\), again larger than \(\tau\).

**Both blocks cross.**  Put

\[
n=A-(2d+1),\qquad m=D-2.
\]

Equation (3.4) is

\[
\gamma_p=U_2(n+m)-U_2(n)-n-\tau.
\tag{2.8}
\]

Since \(A\ge2d+1\) and \(s=o(d)\), one has \(a\to\infty\) uniformly
with \(h\), as well as \(d=O(a^2)\), \(n=O(a^2)\), and
\(\tau=O(a^2)\).  Lemma 1.1 gives
\(m=\Omega(a^{3/2})\).
Lemma 1.2 applied to (2.8) proves positivity. \(\square\)

## 3. Exact recovery from the initial cap

At \(p=3\), set

\[
d=h+b-5,\qquad A=\binom{b+1}{2}-6,\qquad
B=A+b+1,\qquad \tau=2h+b-2.
\tag{3.1}
\]

Under (2.1), \(A<2d+1\) and \(B<2d+3\), so an initial cap never
crosses a rank-three wall.  If only \(y\) reaches its stable rank-two cap,
put \(w=d-A\).  Formula (2.4), now with \(D=b+1\), is strictly increasing
in \(w\).  It is positive for \(w\ge2\); the only possibly negative case
is \(w=1\).  If \(A\ge d\), put

\[
v=A-d=\binom b2-h-1.
\tag{3.2}
\]

Then direct simplification gives

\[
\gamma_3=\frac{(b+1)(2v-b)+8}{2}.
\tag{3.3}
\]

Thus \(\gamma_3<0\) implies

\[
0\le v\le\left\lfloor\frac{b-1}{2}\right\rfloor.
\tag{3.4}
\]

### Proposition 3.1 (one-step initial recovery)

Assume \(h\ge224\), (2.1), and that the first cap occurs at \(p=3\).
Then

\[
\gamma_3<0\quad\Longrightarrow\quad\gamma_4>0.
\tag{3.5}
\]

#### Proof

First suppose only \(y\) caps and \(\gamma_3<0\).  The preceding discussion
forces \(w=1\), hence \(h=\binom b2\) and \(b\ge22\).  Exact Pascal
normalization at the next row yields

\[
\boxed{
\gamma_4=
 \binom{d-2}{2}+\binom{d-b-3}{2}
 -\binom{b-11}{2}-\tau>0.}
\tag{3.6}
\]

For positivity it suffices to drop the second positive term.  Substitution
of \(d=\binom{b+1}{2}-5\) leaves

\[
\binom{d-2}{2}-\binom{b-11}{2}-\tau
=\frac{b^4+2b^3-41b^2+62b-288}{8}>0
\]

for \(b\ge22\).

Now suppose both stable rank-two tails cap.  Define

\[
r_x=b+\binom v2-10,\qquad
Q=\tau-\binom{b+v}{2}.
\tag{3.7}
\]

The \(x_4\) low tail is exactly

\[
\binom{d-2}{2}+r_x.
\tag{3.8}
\]

If \(Q\ge0\) and \(v=0\), exact raising gives

\[
\boxed{
\gamma_4=\binom{d-3}{2}-\binom{b-9}{2}-\tau>0.}
\tag{3.9}
\]

The lower bound is

\[
\frac{b^4+2b^3-49b^2+38b+32}{8}>0
\qquad(b\ge22).
\]

If \(Q\ge0\) and \(v\ge1\), put

\[
r_y=bv+\binom{v+1}{2}-2.
\]

Then

\[
\boxed{
\gamma_4=\binom{d-1}{2}
 +\binom{r_y}{2}-\binom{r_x+1}{2}-\tau>0.}
\tag{3.10}
\]

Indeed \(r_y-r_x=(b+1)(v-1)+8>0\), while
\(\binom{d-1}{2}>\tau\).

Finally, if \(Q<0\), the \(y_4\) tail has positive rank-two remainder
\(-Q\), and

\[
\boxed{
\gamma_4=\binom d2+\binom{d-1}{2}
 -\binom{r_x+1}{2}+U_2(-Q)-\tau>0.}
\tag{3.11}
\]

From (3.4), \(r_x+1\le d/2\).  Hence, even after dropping \(U_2(-Q)\),
the right side is at least

\[
(d-1)^2-\frac{d^2}{8}-2d>0.
\]

Equations (3.6) and (3.9)--(3.11) are identities, not estimates; they are
also checked independently by `verify_negative_cap_recovery.py`.
This proves (3.5). \(\square\)

## 4. Uniform adaptive consequence

### Theorem 4.1 (double-borrow negative-side seed)

For all sufficiently large dyadic \(h\), uniformly for every moving
integer \(b\ge5\) satisfying (2.1), the paired orbit has a nonnegative
diagonal surplus by rank

\[
p_5(h)=\log_2\log h+O(1).
\tag{4.1}
\]

#### Proof

If the stable words remain canonical through \(p_5(h)\), Corollary 2.2 of
the atlas supplies the seed.  Otherwise take the first noncanonical row.
Proposition 2.1 supplies the seed there when \(p\ge4\).  At \(p=3\), either
the surplus is already nonnegative or Proposition 3.1 supplies it at the
next row.

The local-to-global transfer is uniform.  Under (2.1) and
\(p\le p_5(h)+1\), every local upper index is
\(h+O(\sqrt h+\log\log h)\), whereas the inherited high block begins at
\(3h/2+3\).  Thus no carry reaches that block, and the local surplus equals
the corresponding global diagonal surplus. \(\square\)

This theorem closes both the pre-cap and cap branches of the moving
double-borrow chamber.  It does not claim that the remaining negative
offset chambers, where one or both initial signed tails are nonnegative,
have been covered.
