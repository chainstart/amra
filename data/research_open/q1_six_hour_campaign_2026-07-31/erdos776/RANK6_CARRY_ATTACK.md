# The rank-six carry gate

## 1. Frozen target

Let

\[
L=224\,2^{j-1}\quad(j\ge2),\qquad 1\le b\le L,
\]

and put

\[
c=b+L/2-2,\qquad T=L+b-3.
\]

For \(p=3,4,5\), let

\[
x_3(b)=\binom c3+\binom{b-1}{2}+2-L,
\qquad x_{p+1}(b)=U_p(x_p(b))-T.
\tag{1.1}
\]

The adjacent orbit is exactly \(y_p(b)=x_p(b+1)\), with the adjacent tax
\(T+1\).  The remaining target from the preceding campaign is

\[
\boxed{\gamma _5=x_6(b+1)-S_5(x_5(b))\ge0.}
\tag{1.2}
\]

Here \(U_p\) is the upper Macaulay shift and \(S_p(n)=n+U_p(n)\).

## 2. Exact adjoint reformulation

Define

\[
\delta_p=U_p(y_p)-S_p(x_p)=\gamma_p+T+1.
\]

The inherited signed-lift calculation gives

\[
y_5=x_4+x_5+\delta_4-1,
\qquad \delta_4\ge0,
\tag{2.1}
\]

and \(x_5=U_4(x_4)-T\).  If

\[
A=S_5(x_5),\qquad
R=y_5-\operatorname{KK}_6(A),
\tag{2.2}
\]

then Macaulay adjunction gives the following exact version of the target.

### Lemma 2.1 (reserve-versus-carry equivalence)

The rank-six gate (1.2) is equivalent to

\[
\boxed{
\operatorname{KK}_6(A+T+1)-\operatorname{KK}_6(A)\le R.
}
\tag{2.3}
\]

Moreover

\[
R=x_4-1-\operatorname{KK}_5(x_5)+\delta_4.
\tag{2.4}
\]

#### Proof

By adjunction,

\[
U_5(y_5)\ge A+T+1
\quad\Longleftrightarrow\quad
\operatorname{KK}_6(A+T+1)\le y_5.
\]

The left inequality is (1.2), since
\(x_6(b+1)=U_5(y_5)-(T+1)\).  Finally, the shifted canonical word for
\(A=S_5(x_5)\) has lower shadow

\[
\operatorname{KK}_6(A)=x_5+\operatorname{KK}_5(x_5).
\]

Subtract this identity from (2.1).  This proves (2.3)--(2.4). \(\square\)

This is useful because it isolates the last obstruction as one concrete
suffix carry: the left side only sees what happens when \(T+1\) is added
to the shifted canonical word of \(x_5\), while the right side is the
unused lower-shadow capacity plus the previous signed-lift surplus.

## 3. The rank-six gate is false

The dangerous chamber is not an endpoint.  Put

\[
h=L/2,\qquad b=h+5.
\tag{3.1}
\]

Then \(c=2h+3\) and \(T=3h+2\).  For every dyadic value
\(h=112\,2^{j-1}\) with \(j\ge4\), direct Pascal normalization gives

\[
\begin{aligned}
x_3={}&\binom{2h+3}{3}+\binom{h+2}{2}+\binom71,\\
y_3={}&\binom{2h+4}{3}+\binom{h+3}{2}+\binom91,\\[2mm]
x_4={}&\binom{2h+3}{4}+\binom{h+1}{3}
       +\binom{h-2}{2}+\binom{16}1,\\
y_4={}&\binom{2h+4}{4}+\binom{h+2}{3}
       +\binom{h-1}{2}+\binom{33}1,\\[2mm]
x_5={}&\binom{2h+3}{5}+\binom{h+1}{4}
       +\binom{h-3}{3}+\binom{h-6}{2}+\binom{103}1,\\
y_5={}&\binom{2h+4}{5}+\binom{h+2}{4}
       +\binom{h-2}{3}+\binom{h-5}{2}+\binom{513}1.
\end{aligned}
\tag{3.2}
\]

All displayed words are canonical.  Applying \(U_5\), the first four
terms of \(U_5(y_5)\) cancel exactly with the first four terms of
\(S_5(x_5)\).  Consequently

\[
\boxed{
\gamma _5
=\binom{513}{2}-\binom{104}{2}-(3h+3)
=125969-3h.
}
\tag{3.3}
\]

### Theorem 3.1 (infinite counterfamily to the fixed rank-six gate)

For every \(j\ge10\), take

\[
L=224\,2^{j-1},\qquad b=L/2+5.
\]

Then \(\gamma _5<0\).  Hence (1.2), (2.3), and the proposed all-strip
rank-six carry lemma are false on an infinite family.

The first member has

\[
(j,L,b,h,M,T)=(10,114688,57349,57344,171813,172034)
\]

and

\[
\boxed{\gamma _5=-46063,qquad
\delta _5=125972<T+1=172035.}
\tag{3.4}
\]

An exhaustive exact search of all preceding strips \(2\le j\le9\), and
of the tenth strip through this point, finds no earlier failure.  In the
entire tenth strip, \(b=57349\) is the unique negative point.  This finite
minimality statement is guarded separately from the symbolic infinite
family: it is not used to prove (3.3).

At the first point the adjoint quantities from Lemma 2.1 are

\[
\begin{array}{rcl}
A=S_5(x_5)&=&3160895729059072539108322510,\\
\operatorname{KK}_6(A)&=&165366563303330760992883,\\
\operatorname{KK}_6(A+T+1)&=&165366563303330760993376,\\
R&=&409.
\end{array}
\]

Thus the lower-shadow carry is \(493\), exceeding its reserve by exactly
\(84\).  This independently witnesses the failure of (2.3).

## 4. No fixed post-carry rank can repair the argument

The phenomenon in (3.3) persists at every fixed rank.  Define two integer
sequences

\[
A_3=7,\qquad B_3=9,
\tag{4.1}
\]

and, for \(p\ge3\),

\[
\begin{aligned}
A_{p+1}&=\binom{A_p}{2}-(12p-31),\\
B_{p+1}&=\binom{B_p}{2}-(12p-33).
\end{aligned}
\tag{4.2}
\]

The first values are

\[
\begin{array}{c|rrrrrr}
p&3&4&5&6&7&8\\ \hline
A_p&7&16&103&5224&13642435&93058009543342\\
B_p&9&33&513&131301&8619910611&37151429466505241304.
\end{array}
\tag{4.3}
\]

For completeness, the inherited local-to-global cancellation is not
restricted to the three ranks for which it was first stated.  Fix any
\(P\).  Once \(h\) is large enough for the words below to be canonical,
they are nonnegative and remain strictly below the separated global high
block.  Therefore subtraction is absorbed entirely in the displayed low
tail, and the Pascal cancellation in the proof of the inherited Theorem
6.3 iterates through rank \(P\).  Thus

\[
\boxed{\Gamma_{j+p-2}=\gamma_p\qquad(3\le p\le P)}
\tag{4.3a}
\]

on this family for all sufficiently large \(h\).  Hence the following
no-go theorem concerns the actual global diagonal surplus, not merely a
detached model recurrence.

### Theorem 4.1 (fixed-rank obstruction theorem)

Fix \(p\ge3\).  For all sufficiently large \(h\), along the family
\(b=h+5\) the canonical low tails are

\[
\begin{aligned}
x_p={}&\binom{2h+3}{p}
 +\sum_{k=3}^{p-1}\binom{h+4k-4p+5}{k}
 +\binom{h+14-4p}{2}+\binom{A_p}{1},\\
y_p={}&\binom{2h+4}{p}
 +\sum_{k=3}^{p-1}\binom{h+4k-4p+6}{k}
 +\binom{h+15-4p}{2}+\binom{B_p}{1}.
\end{aligned}
\tag{4.4}
\]

Consequently

\[
\boxed{
\gamma _p
=\binom{B_p}{2}-\binom{A_p+1}{2}-3h-3.
}
\tag{4.5}
\]

In particular, for every fixed \(P\) there are arbitrarily large dyadic
strips on which

\[
\gamma _3,\gamma _4,\ldots,\gamma _P<0.
\tag{4.6}
\]

#### Proof

The case \(p=3\) is the first line of (3.2).  Assume (4.4) at rank
\(p\).  Upper shift sends the rank-two term in the \(x\)-word to
\(\binom{h+14-4p}{3}\).  Pascal expansion at the desired next rank
leaves \(\binom{h+13-4p}{2}\).  Since

\[
\binom{h+13-4p}{2}-\binom{h+10-4p}{2}
=3h+33-12p,
\]

subtracting the tax \(3h+2\) leaves precisely
\(\binom{A_p}{2}-(12p-31)=A_{p+1}\).  The same calculation for \(y\)
uses

\[
\binom{h+14-4p}{2}-\binom{h+11-4p}{2}
=3h+36-12p
\]

and tax \(3h+3\), giving \(B_{p+1}\).  For fixed \(p\), taking \(h\)
larger than all the finitely many constants makes every word canonical,
so the induction is legitimate.

In \(U_p(y_p)-S_p(x_p)\), every \(h\)-dependent term in (4.4) cancels
with its paired term.  The two constant rank-one tails and the adjacent
tax give (4.5).  Finally, for fixed \(P\), choose a dyadic \(h\) larger
than the finitely many canonicality thresholds and all constants on the
right of (4.5) for \(3\le p\le P\).  This gives (4.6). \(\square\)

Theorem 4.1 is stronger than the single counterexample: merely replacing
rank six by any other **fixed** post-carry rank cannot establish a uniform
diagonal seed.

### Theorem 4.2 (necessary adaptive-rank scale)

Let \(\rho(h)\) be the first \(p\ge3\), if one exists, for which
\(\gamma_p\ge0\) along \(b=h+5\).  Then

\[
\boxed{\rho(h)\ge \log_2\log h-O(1).}
\tag{4.7}
\]

Equivalently, since \(h=112\,2^{j-1}\),

\[
\boxed{\rho(h)\ge \log_2 j-O(1).}
\tag{4.8}
\]

#### Proof

For \(p\ge4\), the recurrence for \(B_p\) gives the elementary bounds

\[
3^{2^{p-3}+1}\le B_p\le33^{2^{p-4}}.
\tag{4.9}
\]

Indeed \(B_{p+1}\ge B_p^2/3\) and \(B_{p+1}\le B_p^2\), starting
from \(B_4=33\).  Also \(A_p\le B_p/2\) for \(p\ge4\), by induction
from \(A_4=16,B_4=33\).  Put

\[
P(h)=\left\lfloor
4+\log_2\!\left(\frac{\log h}{2\log33}\right)
\right\rfloor.
\tag{4.10}
\]

For every \(4\le p\le P(h)\), (4.9) gives \(B_p\le\sqrt h\).
For sufficiently large \(h\), this also makes (4.4) canonical
simultaneously at all those ranks.  Formula (4.5) and the crude upper
bound

\[
\binom{B_p}{2}-\binom{A_p+1}{2}-3\le B_p^2/2
\]

then give \(\gamma_p<h/2-3h<0\).  The ranks below four are already
negative once \(h\) is large.  Hence \(\rho(h)>P(h)\), which is
(4.7); (4.8) follows from the dyadic definition of \(h\). \(\square\)

This lower bound identifies the correct qualitative replacement for a
fixed rank: any successful diagonal-seed theorem must allow at least a
**doubly logarithmic** post-carry delay.  Define

\[
p_{\rm cand}(h)=\min\left\{p\ge3:
\binom{B_p}{2}-\binom{A_p+1}{2}-3\ge3h\right\}.
\tag{4.11}
\]

### Theorem 4.3 (sharp adaptive scale on the counterfamily)

For all sufficiently large dyadic \(h\),

\[
\boxed{\rho(h)=p_{\rm cand}(h)
=\log_2\log h+O(1)=\log_2j+O(1).}
\tag{4.12}
\]

#### Proof

We need one additional elementary separation estimate.  For \(p\ge5\),

\[
\boxed{A_p^4\le B_p^3.}
\tag{4.13}
\]

It holds directly at \(p=5\).  Thereafter
\(A_{p+1}\le A_p^2/2\) and
\(B_{p+1}\ge(2/5)B_p^2\); the latter inequality follows immediately
from \(B_p\ge513\) and (4.2).  Since
\(1/16<8/125\), (4.13) propagates.

Let \(p=p_{\rm cand}(h)\).  The bounds used in Theorem 4.2 imply both
existence and

\[
p=\log_2\log h+O(1).
\tag{4.14}
\]

At the preceding rank, minimality and the lower estimate

\[
\binom{B_{p-1}}2-\binom{A_{p-1}+1}2-3
\ge B_{p-1}^2/4
\]

give \(B_{p-1}<\sqrt{12h}\).  Consequently

\[
B_p\le B_{p-1}^2/2\le6h,
\qquad
A_p\le B_p^{3/4}\le(6h)^{3/4}.
\tag{4.15}
\]

The sequence \(B_q\) is increasing.  Thus
\(B_q\le B_{p-1}<\sqrt{12h}\) for every \(q<p\); for sufficiently large
\(h\), every \(y_q\) suffix below rank \(p\) is consequently below its
canonical cap.  The corresponding \(x_q\) words are canonical as well,
and (4.15) also makes the \(x_p\)-word canonical.  Hence all ranks below
\(p\) have
\(\gamma_q=K_q-3h<0\), where
\(K_q=\binom{B_q}2-\binom{A_q+1}2-3\).

It remains to handle the only subtlety: \(B_p\) may exceed its rank-one
canonical cap.  Set

\[
d=h+15-4p,
\]

the upper index of the rank-two term in the formal \(y_p\)-word.  If
\(B_p<d\), that word is canonical and (4.5) gives
\(\gamma_p=K_p-3h\ge0\).

If \(B_p\ge d\), the actual value of \(y_p\) is at least the canonical
number obtained by replacing its suffix

\[
\binom d2+\binom{B_p}1
\quad\text{by}\quad
\binom{d+1}2.
\]

This replacement is canonical because the preceding rank-three upper
index is \(d+3\).  Monotonicity of \(U_p\), followed by cancellation of
the paired high terms, yields

\[
\gamma_p
\ge \binom d2-\binom{A_p+1}2-(3h+3).
\tag{4.16}
\]

By (4.14)--(4.15), \(d=h-O(\log\log h)\) while
\(A_p^2=O(h^{3/2})\).  The right side of (4.16) is therefore positive
for all sufficiently large \(h\).  Thus rank \(p\) succeeds and every
earlier rank fails, proving \(\rho(h)=p_{\rm cand}(h)\).  Combining
(4.9) with the quadratic bounds for \(K_p\) gives the asymptotic formula
in (4.12). \(\square\)

Theorem 4.3 completely resolves the adaptive delay on the explicit
counterfamily.  What remains open is an upper bound of the same order
**uniformly over all** \(1\le b\le L\).

### Proposition 4.4 (the critical central chamber)

The offset five is not accidental.  Fix any integer \(k\ge5\) and put
\(b=h+k\).  Define

\[
A_3(k)=2k-3,\qquad B_3(k)=2k-1,
\tag{4.17}
\]

and

\[
\begin{aligned}
A_{p+1}(k)&=\binom{A_p(k)}2+2k+21-12p,\\
B_{p+1}(k)&=\binom{B_p(k)}2+2k+23-12p.
\end{aligned}
\tag{4.18}
\]

For every fixed \(k,p\), and all sufficiently large \(h\), the paired
canonical words are

\[
\begin{aligned}
x_p={}&\binom{2h+k-2}{p}
 +\sum_{r=3}^{p-1}\binom{h+4r-4p+k}{r}
 +\binom{h+k+9-4p}{2}+\binom{A_p(k)}1,\\
y_p={}&\binom{2h+k-1}{p}
 +\sum_{r=3}^{p-1}\binom{h+4r-4p+k+1}{r}
 +\binom{h+k+10-4p}{2}+\binom{B_p(k)}1.
\end{aligned}
\tag{4.19}
\]

Hence

\[
\boxed{
\gamma_p(k)=
\binom{B_p(k)}2-\binom{A_p(k)+1}2-(3h+k-2).
}
\tag{4.20}
\]

The proof is the same two-Pascal/three-step borrow used in Theorem 4.1;
keeping \(k\) symbolic gives (4.18).  For each fixed \(p\), the constant
part

\[
K_p(k)=\binom{B_p(k)}2-\binom{A_p(k)+1}2-(k-2)
\]

is strictly increasing for integers \(k\ge5\).  Here is the short exact
check.  Write

\[
a=A_p(k+1)-A_p(k),\qquad
d=B_p(k+1)-B_p(k).
\]

Initially \(a=d=2\) and \(B_p-A_p=2\).  The recurrences give

\[
\begin{aligned}
a'&=a(2A_p+a-1)/2+2,\\
d'&=d(2B_p+d-1)/2+2.
\end{aligned}
\]

Thus \(d\ge a\ge2\) and \(B_p-A_p\ge2\) propagate.  Direct subtraction
then yields

\[
\begin{aligned}
K_p(k+1)-K_p(k)
&=\frac{d(2B_p+d-1)-a(2A_p+a+1)}2-1\\
&\ge a(B_p-A_p-1)-1\ge1.
\end{aligned}
\tag{4.21}
\]

Thus \(k=5\) is the slowest fixed-offset chamber among all \(k\ge5\).
Offsets \(k\le4\) cross a different borrow wall (the formal \(A_p(k)\)
becomes negative), so this proposition does not silently claim the
uniform all-\(b\) theorem.  It does explain why the first obstruction is
the isolated point \(b=h+5\), rather than a strip endpoint or a generic
bulk point.

The four exceptional offsets can in fact be disposed of exactly.  This
also shows that the wall at five is a genuine change of regime, rather
than an artefact of the recurrence notation.

### Proposition 4.5 (the four offsets before the wall)

For every dyadic \(h=112\,2^{j-1}\), \(j\ge2\), the first nonnegative
local surplus on \(b=h+k\), \(1\le k\le4\), is as follows:

\[
\begin{array}{c|c|c}
k&\text{first rank}&\text{surplus there}\\ \hline
1&4&\binom{h-7}{2}+3h-122\\
2&4&2h-70\\
3&4&3h-43\\
4&5&13h+5003.
\end{array}
\tag{4.22}
\]

In particular every entry in the last column is positive throughout the
allowed dyadic range, whereas all preceding surpluses are negative.

#### Proof

The needed words after crossing the borrow wall are short enough to
write explicitly.  For \(k=1\),

\[
\begin{aligned}
x_3&=\binom{2h-1}{3}+\binom{h-3}{2}+\binom{h-4}{1},&
y_3&=\binom{2h}{3}+\binom{h-1}{2}+\binom11,\\
x_4&=\binom{2h-1}{4}+\binom{h-3}{3}+\binom{h-8}{2}
      +\binom{h-24}{1},&
y_4&=\binom{2h}{4}+\binom{h-2}{3}+\binom{h-6}{2}
      +\binom{h-17}{1}.
\end{aligned}
\tag{4.23}
\]

Pascal cancellation gives

\[
\gamma_3=-2h-2,
\qquad
\gamma_4=\binom{h-7}{2}+3h-122.
\tag{4.24}
\]

For \(k=2\), the rank-four pair is

\[
\begin{aligned}
x_4&=\binom{2h}{4}+\binom{h-2}{3}+\binom{h-6}{2}
      +\binom{h-17}{1},\\
y_4&=\binom{2h+1}{4}+\binom{h-1}{3}+\binom{h-5}{2}
      +\binom{h-11}{1},
\end{aligned}
\tag{4.25}
\]

and therefore

\[
\gamma_3=2-3h,
\qquad
\gamma_4=
\binom{h-11}{2}-\binom{h-16}{2}-3h=2h-70.
\tag{4.26}
\]

For \(k=3\),

\[
\begin{aligned}
x_4&=\binom{2h+1}{4}+\binom{h-1}{3}+\binom{h-5}{2}
      +\binom{h-11}{1},\\
y_4&=\binom{2h+2}{4}+\binom h3+\binom{h-3}{2}+\binom31,
\end{aligned}
\tag{4.27}
\]

so

\[
\gamma_3=3-3h,
\qquad
\gamma_4=
\binom{h-4}{2}+\binom32-\binom{h-10}{2}-(3h+1)
=3h-43.
\tag{4.28}
\]

Finally, for \(k=4\), the formal recurrence is still canonical at rank
four and yields \(\gamma_3=4-3h\), \(\gamma_4=112-3h\).  Its next
rank-one constant is negative, and the normalized rank-five pair is

\[
\begin{aligned}
x_5&=\binom{2h+2}{5}+\binom h4+\binom{h-4}{3}
      +\binom{h-8}{2}+\binom{h-24}{1},\\
y_5&=\binom{2h+3}{5}+\binom{h+1}{4}+\binom{h-3}{3}
      +\binom{h-6}{2}+\binom{103}{1}.
\end{aligned}
\tag{4.29}
\]

Thus

\[
\gamma_5=
\binom{h-7}{2}+\binom{103}{2}-\binom{h-23}{2}-(3h+2)
=13h+5003.
\tag{4.30}
\]

Every displayed word is canonical for \(h\ge224\).  Equations
(4.24), (4.26), (4.28), and (4.30) prove the table and the asserted
minimality. \(\square\)

The fixed-offset calculation by itself cannot be extrapolated to
\(k=k(h)\): the rank-one constant can hit its canonical cap.  The next
lemma gives an exact atlas for that event and reduces the surviving
moving chamber to rank two.

For a nonnegative integer \(n\), write \(U_2(n)\) for its rank-two upper
Macaulay shift and put \(S_2(n)=n+U_2(n)\).  Define

\[
\Phi_\tau(n,m)=U_2(n+m)-S_2(n)-\tau .
\tag{4.31}
\]

### Lemma 4.6 (rank-two endpoint principle)

Write

\[
n=\binom q2+r,\qquad n+m=\binom{q+s}{2}+u,
\quad 0\le r<q,\quad 0\le u<q+s.
\tag{4.32}
\]

Then

\[
\boxed{\;
\Phi_\tau(n,m)=
\binom{q+s}{3}-\binom{q+1}{3}
+\binom u2-\binom{r+1}{2}-\tau .
\;}
\tag{4.33}
\]

For fixed \(q,m,s,\tau\), put

\[
c=m-sq-\binom s2.
\tag{4.34}
\]

The admissible remainders form the integer interval

\[
I=[0,q-1]\cap[-c,q+s-1-c],
\qquad u=r+c,
\tag{4.35}
\]

and (4.33) is affine in \(r\):

\[
\boxed{\;
\Phi_\tau=
\binom{q+s}{3}-\binom{q+1}{3}
+\frac{(c-1)(2r+c)}2-\tau .
\;}
\tag{4.36}
\]

Consequently its minimum on each carry-count chamber \(s\) occurs at
the left endpoint of \(I\) if \(c\ge1\), and at the right endpoint if
\(c\le1\).

#### Proof

The rank-two canonical word in (4.32) gives

\[
U_2(n)=\binom q3+\binom r2,\qquad
S_2(n)=\binom{q+1}{3}+\binom{r+1}{2}.
\]

This proves (4.33).  Subtracting the two equations in (4.32) gives
\(u=r+c\), and the canonical bounds give (4.35).  Finally,

\[
\binom{r+c}{2}-\binom{r+1}{2}
=\frac{(c-1)(2r+c)}2,
\]

which proves (4.36) and the endpoint assertion. \(\square\)

This is an exact endpoint reduction, not a numerical approximation:
once \(q\) and the number \(s\) of triangular walls crossed are fixed,
there is no interior minimum left to inspect.

### Proposition 4.7 (moving-offset cap atlas)

Let \(k\ge5\), and suppose the paired formula (4.19) has propagated
through rank \(p-1\).  Set

\[
A=A_p(k),\quad B=B_p(k),\quad D=B-A,\quad
d=h+k+9-4p,\quad \tau=3h+k-2.
\tag{4.37}
\]

The formal low blocks at rank \(p\) are

\[
\binom{d+3}{3}+\binom d2+A,\qquad
\binom{d+4}{3}+\binom{d+1}{2}+B.
\tag{4.38}
\]

There are three exact cap chambers.

1. If

   \[
   N_x=\binom d2+A<\binom{d+3}{2},\qquad
   N_y=\binom{d+1}{2}+B<\binom{d+4}{2},
   \tag{4.39}
   \]

   neither rank-three top advances, and

   \[
   \boxed{\gamma_p=\Phi_\tau(N_x,d+D).}
   \tag{4.40}
   \]

   This includes rank-one overflow: the still smaller subchamber
   \(A<d,\ B<d+1\) is exactly the formal chamber (4.20).

2. If the second inequality in (4.39) fails but the first does not, put
   \(R_y=B-(3d+6)\).  Provided \(R_y<\binom{d+5}{2}\), only the
   \(y\)-word crosses the rank-three wall, and

   \[
   \boxed{\gamma_p=
   \binom{d+4}{3}+U_2(R_y)-S_2(N_x)-\tau.}
   \tag{4.41}
   \]

3. If both words cross that wall, put

   \[
   R_x=A-(3d+3),\qquad R_y=B-(3d+6).
   \tag{4.42}
   \]

   If \(0\le R_x<\binom{d+4}{2}\) and
   \(0\le R_y<\binom{d+5}{2}\), the new rank-three tops are again
   adjacent, all higher terms cancel, and

   \[
   \boxed{\gamma_p=\Phi_\tau(R_x,D-3).}
   \tag{4.43}
   \]

#### Proof

In chamber 1, the rank-three terms in (4.38) remain canonical and the
rank-two tails have values \(N_x,N_y\).  Their difference is
\[
N_y-N_x=d+B-A=d+D.
\]
The adjacent rank-three terms cancel in \(U_p(y_p)-S_p(x_p)\), leaving
(4.40).

The identity
\[
\binom{d+3}{2}-\binom d2=3d+3
\]
shows that crossing the \(x\)-wall replaces its low block by
\(\binom{d+4}{3}+R_x\); the analogous \(y\)-threshold is \(3d+6\).
If only \(y\) crosses, the two rank-three upper indices differ by two,
and the uncancelled Pascal term is \(\binom{d+4}{3}\), giving (4.41).
If both cross, their new upper indices are adjacent and
\[
R_y-R_x=B-A-3=D-3,
\]
which gives (4.43). \(\square\)

Combining Proposition 4.7 with Lemma 4.6 turns every synchronized
cap-overflow chamber into endpoint inequalities in the four integers
\((q,s,r,\tau)\).  It also explains why a carry can abruptly reset a
previously very positive surplus: after a synchronized wall crossing,
the large paired terms cancel again and only \(\Phi_\tau\) remains.

### Corollary 4.8 (complete rank-four central atlas)

At rank four,

\[
\begin{aligned}
A_4&=2k^2-5k-9,&B_4&=2k^2-k-12,&D_4&=4k-3,\\
K_4&=8k^3-20k^2-31k+44.
\end{aligned}
\tag{4.44}
\]

For \(5\le k\le h-2\), the rank-three starting words are canonical and
at most one rank-three wall is crossed.  Put

\[
f(k)=2k^2-8k+9,\qquad g(k)=2k^2-4k+3=f(k+1).
\tag{4.45}
\]

Then the rank-three cap chambers are exactly

\[
\begin{array}{c|c}
g(k)<3h&\text{neither word crosses},\\
f(k)<3h<g(k)&\text{only \(y\) crosses},\\
3h<f(k)&\text{both words cross}.
\end{array}
\tag{4.46}
\]

The earlier rank-one cap is also explicit:

\[
\begin{aligned}
A_4<d&\iff 2k^2-6k-2<h,\\
B_4<d+1&\iff 2k^2-2k-6<h,
\end{aligned}
\qquad
2k^2-2k-6=
\left(2(k+1)^2-6(k+1)-2\right).
\tag{4.46a}
\]

Crossing this first wall merely changes the rank-two coordinates in
(4.40); it does not create another high-rank case.

Equalities cannot occur because \(f,g\) are odd while \(3h\) is even.
Since \(f\) is strictly increasing and \(g(k)=f(k+1)\), the middle
chamber contains exactly one integer \(k\).

In that one-sided chamber, let
\(\varepsilon=3h-f(k)\).  Then

\[
1\le\varepsilon\le4k-7,\qquad
\gamma_4=
\binom Q2-\binom{Q-\varepsilon}{2}
+U_2(4k-6-\varepsilon)-(3h+k-2),
\quad Q=h+k-4.
\tag{4.47}
\]

Moreover \(\varepsilon\ne1,3\): after division by two, those two cases
would respectively require

\[
(k-2)^2+1=168\,2^{j-1},\qquad
(k-2)^2+2=168\,2^{j-1},
\]

both impossible modulo \(8\).  Thus \(\varepsilon\ge5\), and already
the first binomial difference in (4.47) proves

\[
\boxed{\gamma_4>0}
\tag{4.48}
\]

throughout the one-sided chamber.

In the synchronized chamber, Proposition 4.7 becomes the particularly
small exact target

\[
\boxed{\gamma_4=
\Phi_{3h+k-2}\bigl(f(k)-3h,\,4k-6\bigr).}
\tag{4.49}
\]

Finally, the two excluded right endpoints normalize separately:

\[
\begin{array}{c|c}
k=h-1&\gamma_4=2h^2-11h-27>0,\\
k=h&\gamma_4=-2h-9,\quad
\gamma_5=\binom{2h-14}{2}+4h-144>0.
\end{array}
\tag{4.50}
\]

#### Proof

For \(5\le k\le h-2\), both rank-three starting words in (4.19) are
canonical.  Substituting \(p=4\) into (4.18) gives (4.44), while the
rank-one cap conditions give (4.46a).  The rank-three crossing
thresholds in Proposition 4.7 are

\[
A_4-(3d+3)=f(k)-3h,\qquad
B_4-(3d+6)=g(k)-3h,
\]

which proves (4.46).  No second rank-three wall can be crossed.  Indeed,
on writing \(t=h-k\ge2\), the remaining capacities after the first
crossing are

\[
\begin{aligned}
\binom{d+4}{2}-(f(k)-3h)
  &=\frac{(t+2)(4h-3t-3)}2>0,\\
\binom{d+5}{2}-(g(k)-3h)
  &=\frac{(t+1)(4h-3t)}2>0.
\end{aligned}
\tag{4.51}
\]

In the one-sided chamber, normalizing
\(\binom{Q}{2}-\varepsilon\) and applying (4.41) gives (4.47).
Here \(f(k)<3h\) forces \(k<h/3\) for \(h\ge224\), so
\(\varepsilon\le4k-7<Q\) and the displayed normalization is legal.
The modulo-eight argument following that formula gives
\(\varepsilon\ge5\), and hence

\[
\binom Q2-\binom{Q-\varepsilon}{2}-(3h+k-2)
\ge 2h+4k-33>0.
\]

This proves (4.48).  If both words cross, (4.42) reads
\((R_x,R_y)=(f(k)-3h,g(k)-3h)\), so (4.43) is exactly (4.49).
Direct Pascal normalization at \(k=h-1,h\) gives (4.50). \(\square\)

Thus the moving central-offset problem is now localized to two
explicit pieces: the pre-cap formula \(K_p(k)-3h\) at adaptive rank,
and synchronized endpoint tests of the form (4.36).  In particular,
the only unresolved rank-four central chamber is (4.49); no asymmetric
cap chamber remains.

There is a further useful compression of (4.49).  It removes \(h\)
entirely and exposes the exact two-dimensional integer chart on which a
rank-five bridge must be proved.

### Corollary 4.9 (dimensionless synchronized chart)

In the synchronized rank-four chamber put

\[
n=f(k)-3h,\qquad m=4k-6.
\tag{4.52}
\]

Then

\[
h=\frac{2k^2-8k+9-n}{3},\qquad
\tau=3h+k-2=2k^2-7k+7-n,
\tag{4.53}
\]

and (4.49) simplifies to

\[
\boxed{\gamma_4=
U_2(n+4k-6)-U_2(n)-(2k^2-7k+7).}
\tag{4.54}
\]

Thus even the explicit \(n\) in \(S_2(n)\) cancels.  The admissible
lattice is

\[
\begin{gathered}
k\ge5,\qquad n\ge0,\qquad
n\equiv 2k^2-8k+9\pmod3,\\
h=\frac{2k^2-8k+9-n}{3}\ge224,\qquad k\le h-2.
\end{gathered}
\tag{4.55}
\]

The last inequality is equivalently
\(n\le2k^2-11k+3\).  Original strip points additionally require
\(h/112\) to be a power of two; retaining all integral \(h\) gives a
stronger lattice on which to seek the bridge.

The next surplus is also an exact two-variable expression.  Put

\[
\begin{aligned}
e&=h+k-3=\frac{2k^2-5k-n}{3},\\
T&=\tau-1=2k^2-7k+6-n,\\
z&=U_2(n),\qquad w=U_2(n+4k-6),\\
X&=\binom e4+z-T,\qquad
Y=\binom{e+1}{4}+w-\tau.
\end{aligned}
\tag{4.56}
\]

Then

\[
\boxed{\gamma_5=U_4(Y)-S_4(X)-\tau.}
\tag{4.57}
\]

#### Proof

Equations (4.53) and (4.54) follow by substituting
\(3h=f(k)-n\) into (4.49).  In the synchronized chamber the normalized
rank-four pair is

\[
x_4=\binom{2h+k-2}{4}+\binom e3+n,\qquad
y_4=\binom{2h+k-1}{4}+\binom{e+1}{3}+n+m.
\]

One upper shift and the two adjacent taxes give
\[
x_5=\binom{2h+k-2}{5}+X,\qquad
y_5=\binom{2h+k-1}{5}+Y.
\]
The leading terms cancel in \(U_5(y_5)-S_5(x_5)\), leaving (4.57).
\(\square\)

Formulae (4.54) and (4.57) are the current sharp bridge target:

\[
\boxed{\gamma_4<0\quad\Longrightarrow\quad\gamma_5\ge0.}
\tag{4.58}
\]

No counterexample to (4.58) occurs in the recorded exact lattice
searches.  At this stage of the reduction, (4.58) is not yet claimed as
a theorem; it is proved below in Theorems 4.11, 4.12, and 4.14.  Unlike a
strip scan, the chart (4.55)--(4.57) is suitable for a proof: apply Lemma 4.6
to \(n\), then split only when \(z-T\) and \(w-\tau\) cross their
rank-three caps.

The negative part of this chart already occupies a strict
dimensionless subcone.

### Lemma 4.10 (one-third chunk localization)

Suppose

\[
n=\binom q2+r,\qquad 0\le r<q,
\]

is a point of (4.55).  If \(\gamma_4<0\), then

\[
\boxed{\quad q<\left\lceil\frac{4k-6}{3}\right\rceil.\quad}
\tag{4.59}
\]

#### Proof

We use the elementary rank-two increment bound

\[
U_2(N+a)-U_2(N)\ge\binom a2
\tag{4.60}
\]

whenever the leading upper index of \(N\) is at least \(a\).  This is
the \(p=2\) large-leading Macaulay increment lemma; it follows by adding
a new vertex joined to an \(a\)-set in the clique interpretation.

Put \(m=4k-6\).  If \(q\ge\lceil m/3\rceil\), split \(m\) into three
integers \(a_1,a_2,a_3\) differing by at most one.  Each \(a_i\le q\),
and the leading index cannot decrease as the chunks are added.  Three
applications of (4.60) give

\[
U_2(n+m)-U_2(n)\ge\sum_{i=1}^3\binom{a_i}{2}.
\tag{4.61}
\]

Writing \(k=3t+\ell\), the excess of the right side over
\(2k^2-7k+7\) is

\[
\begin{array}{c|c}
\ell&\displaystyle
\sum_i\binom{a_i}{2}-(2k^2-7k+7)\\ \hline
0&6t^2-9t+2\\
1&t(6t-5)\\
2&(2t-1)(3t+1).
\end{array}
\tag{4.62}
\]

It is positive for every \(k\ge5\).  Equation (4.54) would therefore
give \(\gamma_4>0\), a contradiction. \(\square\)

Hence a proof of (4.58) may assume both (4.59) and the exact affine
endpoint reduction (4.36).  In particular \(n<\binom{q+1}{2}\) is
bounded by a fixed \(q/k<4/3\) cone, rather than the much larger
formal cap \(n=O(k^2)\).

The first of the two rank-five cap states can now be closed completely.

### Theorem 4.11 (the synchronized double-borrow bridge)

Let \((k,n)\) lie in (4.55), and suppose \(\gamma_4<0\).  Use the
notation

\[
\begin{aligned}
H&=2k^2-7k+7,&
\Delta&=U_2(n+4k-6)-U_2(n),\\
S&=S_2(n),&
E&=h+k-5.
\end{aligned}
\tag{4.63}
\]

If both rank-five low blocks borrow, equivalently

\[
S-H+1<0,\qquad S+\gamma_4<0,
\tag{4.64}
\]

then

\[
\boxed{\gamma_5>0.}
\tag{4.65}
\]

#### Proof

Put

\[
a=H-1-S,\qquad b=-S-\gamma_4.
\tag{4.66}
\]

The hypotheses say \(a,b>0\), and (4.54) gives

\[
a-b=\Delta-1>0.
\tag{4.67}
\]

The algebraic low remainders in (4.56) are \(-a,-b\).  Two Pascal
borrows therefore normalize them as

\[
\begin{aligned}
X&=\binom{E+1}{4}+\binom E3+P,
&P&=\binom E2-a,\\
Y&=\binom{E+2}{4}+\binom{E+1}{3}+Q,
&Q&=\binom{E+1}{2}-b.
\end{aligned}
\tag{4.68}
\]

These are legal rank-two tails.  Indeed the synchronized chamber forces
\(k\ge21\), while

\[
a<3h+k-3=3E-2k+12<3E-6
<\binom E2.
\tag{4.69}
\]

Also \(0<b<a\).  The two high pairs in (4.68) cancel, leaving the exact
rank-two bridge

\[
\boxed{\gamma_5=U_2(Q)-S_2(P)-\tau,\qquad
\tau=H-n.}
\tag{4.70}
\]

We now apply the endpoint principle without hiding a chamber.  For
\(1\le i\le3\), set

\[
D_i=iE-\binom{i+1}{2},\qquad D_0=0,
\]

and choose the unique \(i\) with \(D_{i-1}<a\le D_i\).  Similarly put

\[
D'_j=j(E+1)-\binom{j+1}{2}
\]

and choose \(j\) from \(D'_{j-1}<b\le D'_j\).  Equation (4.69) gives
\(i\le3\), and \(b<a\), \(D'_i>D_i\) give \(j\le i\).  Write

\[
\begin{aligned}
P&=\binom{E-i}{2}+r,&r&=D_i-a,\\
Q&=\binom{E+1-j}{2}+v,&v&=D'_j-b.
\end{aligned}
\tag{4.71}
\]

Then

\[
v=r+c,\qquad c=\Delta-1+D'_j-D_i,
\tag{4.72}
\]

and

\[
\gamma_5=
\binom{E+1-j}{3}-\binom{E-i+1}{3}
+\binom{r+c}{2}-\binom{r+1}{2}-\tau .
\tag{4.73}
\]

There are only the six pairs \(1\le j\le i\le3\), and (4.73) is affine
in \(r\).  We record all endpoints.

If \(i=j\), then \(c=\Delta+i-1>1\), so the left endpoint gives

\[
\gamma_5\ge\binom{\Delta}{2}-\tau.
\tag{4.74}
\]

If \(i=j+1\) and \(c\ge1\), the left endpoint gives

\[
\gamma_5\ge\binom{E-j}{2}-\tau.
\tag{4.75}
\]

If \(i=j+1\) and \(c\le0\), the right endpoint gives

\[
\gamma_5\ge
\binom{\Delta+j-2}{2}+E-j-1-\tau.
\tag{4.76}
\]

Finally \(i=3,j=1\).  For \(c\ge1\), the left endpoint is at least

\[
\binom{E-1}{2}+\binom{E-2}{2}-\tau.
\tag{4.77}
\]

For \(c\le0\), the right endpoint is

\[
\frac{\Delta^2-2\Delta E+\Delta+2E^2-2E-4}{2}-\tau
\ge\frac{E^2-2E-4}{2}-\tau.
\tag{4.78}
\]

Every displayed lower bound is positive.  To see this with explicit
constants, superadditivity gives

\[
\Delta\ge U_2(4k-6)\ge2k+3.
\tag{4.79}
\]

The last inequality starts with \(U_2(14)=16\); increasing \(k\) by one
adds four units below a leading index at least five, so the
large-leading increment bound adds at least \(\binom42=6\), while
\(2k+3\) adds only two.  Moreover

\[
\tau\le H=2k^2-7k+7,\qquad
\tau=3E-2k+13\le3E+3,\qquad E\ge224.
\tag{4.80}
\]

Equations (4.74) and (4.76) follow from
\(\binom{\Delta-1}{2}>H\); (4.75), (4.77), and (4.78) follow from
\(\binom{E-2}{2}>3E+3\) and
\((E^2-2E-4)/2>3E+3\).  This proves (4.65). \(\square\)

Thus any still-open point of (4.58) must be in one of exactly two
states:

\[
\begin{array}{ll}
\text{asymmetric transition:}&S-H+1<0\le S+\gamma_4,\\
\text{no borrow:}&0\le S-H+1<S+\gamma_4.
\end{array}
\tag{4.81}
\]

The double-borrow cap chamber is no longer part of the open bridge.

### Theorem 4.12 (the asymmetric borrow/no-borrow bridge)

Under the hypotheses of Theorem 4.11, suppose instead that

\[
S-H+1<0\le S+\gamma_4.
\tag{4.82}
\]

Then

\[
\boxed{\gamma_5>0.}
\tag{4.83}
\]

#### Proof

Put

\[
a=H-1-S>0,\qquad \ell=S+\gamma_4\ge0.
\tag{4.84}
\]

The \(x\)-block borrows as in (4.68), while the \(y\)-block does not:

\[
X=\binom{E+1}{4}+\binom E3+P,\quad
P=\binom E2-a,\qquad
Y=\binom{E+3}{4}+\ell.
\]

After cancellation,

\[
\boxed{\gamma_5=
\binom{E+1}{3}+U_3(\ell)-S_2(P)-\tau.}
\tag{4.85}
\]

Choose \(i\in\{1,2,3\}\) from
\(D_{i-1}<a\le D_i\), as in Theorem 4.11, and write

\[
P=\binom{E-i}{2}+r,\qquad 0\le r<E-i.
\]

If \(i\ge2\), then (4.85), even after discarding \(U_3(\ell)\), is at
least

\[
\binom E2+E-2-\tau>0
\tag{4.86}
\]

because \(E\ge224\) and \(\tau\le3E+3\).

It remains to take \(i=1\), so \(1\le a\le E-1\).  In this case (4.85)
is the exact formula

\[
\gamma_5=
\binom E2-\binom{E-a}{2}+U_3(\ell)-\tau.
\tag{4.87}
\]

If \(a\ge4\), its first difference alone is at least \(4E-10\), hence
\(\gamma_5\ge E-13>0\).

Suppose \(a\le3\).  By (4.67),

\[
\ell=\Delta-1-a
\ge U_2(4k-6)-4.
\tag{4.88}
\]

For every \(k\ge53\),

\[
\boxed{
U_3\!\left(U_2(4k-6)-4\right)>2k^2-7k+7=H.
}
\tag{4.89}
\]

Here is an exact proof of the numerical threshold.  Let \(p\) be
defined by

\[
\binom p2\le4k-6<\binom{p+1}{2}.
\]

For \(k\ge53\), \(p\ge20\).  Direct canonical arithmetic for the ten
finite leading rows gives

\[
\begin{array}{c|rrrrrrrrrr}
p&20&21&22&23&24&25&26&27&28&29\\ \hline
\min\bigl(U_3(U_2(4k-6)-4)-H\bigr)
&101&65&189&324&507&725&1001&1305&1678&2105.
\end{array}
\tag{4.90}
\]

For \(p\ge30\), monotonicity and the canonical word

\[
\binom p3-4
=\binom{p-1}{3}+\binom{p-2}{2}+\binom{p-6}{1}
\]

give

\[
U_3(U_2(4k-6)-4)
\ge\binom{p-1}{4}+\binom{p-2}{3}+\binom{p-6}{2}.
\]

Since \(k\le[p(p+1)+10]/8\), the excess over \(H\) is bounded below by

\[
\frac{p^4-30p^3+65p^2-384p+1596}{96}>0.
\tag{4.91}
\]

The polynomial is positive at \(p=30\), and its derivative is positive
thereafter.  This proves (4.89).  Equations (4.87)--(4.89) now give
\(\gamma_5>0\).

Only \(21\le k\le52\) remains.  The synchronized condition gives
\(h\le f(52)/3<1792\), so the only allowed dyadic values are
\(h=224,448,896\).  Exact Pascal normalization leaves precisely the
three asymmetric points

\[
\begin{array}{c|r|r|r|r}
h&k&n&a&\gamma_5\\ \hline
224&22&129&95&19749\\
448&29&115&870&217989\\
896&40&201&1530&808309.
\end{array}
\tag{4.92}
\]

They are positive, completing the proof. \(\square\)

After Theorems 4.11 and 4.12, the only open part of (4.58) is the
synchronized no-borrow state

\[
\boxed{0\le S_2(n)-H+1<S_2(n)+\gamma_4.}
\tag{4.93}
\]

This last state also closes.  The useful point is that its apparently
rank-four expression is exactly a rank-three increment, and that increment
has two complementary lower bounds.

### Lemma 4.13 (rank-three promotion profile)

For integers \(a\ge2\) and \(D\ge0\), define

\[
 {\cal P}_a(D)=U_3\!\left(\binom a3+D\right)-\binom a4.
\tag{4.94}
\]

If the leading index in the rank-three canonical word of \(x\) is at
least \(a\), then

\[
 U_3(x+D)-U_3(x)\ge {\cal P}_a(D).
\tag{4.95}
\]

#### Proof

Write

\[
D=\binom{a+t}{3}-\binom a3+R,
\qquad 0\le R<\binom{a+t}{2}.
\]

Add successively the \(t\) chunks

\[
\binom a2,\binom{a+1}{2},\ldots,\binom{a+t-1}{2},
\]

and then \(R\).  Before the \(i\)-th addition the leading rank-three
index is at least \(a+i\).  The large-leading incremental-shift lemma
therefore gives respective gains

\[
\binom a3,\binom{a+1}{3},\ldots,
\binom{a+t-1}{3},U_2(R).
\]

Their sum is exactly \({\cal P}_a(D)\).  This proves (4.95).
\(\square\)

### Theorem 4.14 (the synchronized no-borrow bridge)

Let \((k,n)\) satisfy (4.55), suppose \(\gamma_4<0\), and suppose (4.93)
holds.  Then

\[
\boxed{\gamma_5>0.}
\tag{4.96}
\]

#### Proof

Put

\[
K=2k-3,\qquad z=U_2(n),\qquad
\Delta=U_2(n+2K)-z.
\]

Then

\[
H=\binom K2+1,\qquad
x=S_2(n)-\binom K2\ge0,\qquad d=\Delta-1>0.
\tag{4.97}
\]

The two non-borrowing low blocks in (4.56) are exactly \(x\) and
\(x+d\).  Since \(x+\tau=z+1\), cancellation of their adjacent high
terms gives

\[
\boxed{\gamma_5=U_3(x+d)-U_3(x)-z-1.}
\tag{4.98}
\]

Take triangular coordinates

\[
n=\binom q2+r,\quad 0\le r<q,\qquad
n+2K=\binom{q+s}{2}+u,\quad0\le u<q+s.
\tag{4.99}
\]

They give the exact endpoint expression

\[
z=\binom q3+\binom r2,\qquad
\Delta=\binom{q+s}{3}-\binom q3
       +\binom u2-\binom r2.
\tag{4.100}
\]

Lemma 4.10 says \(q<\lceil2K/3\rceil\).  Write

\[
2K=Jq+v,\qquad0\le v<q.
\]

Splitting the addition of \(2K\) into \(J\) chunks of size \(q\) and
one chunk of size \(v\), the rank-two large-leading increment lemma gives

\[
d\ge D_{K,q}:=J\binom q2+\binom v2-1,\qquad J\ge3.
\tag{4.101}
\]

Also

\[
z<\binom{q+1}{3}.
\tag{4.102}
\]

Let \(A\) be the leading index of the rank-three canonical word of \(x\)
(take \(A=2\) if \(x=0\)), and put \(a=\lfloor q/2\rfloor\).  We split
at \(A=a\).

If \(A\ge a\), (4.101) implies

\[
d\ge3\binom q2-1.
\]

For \(q\ge52\), nine complete promotion rows fit.  Indeed, writing
\(q=2t\) or \(q=2t+1\), the unused capacities are respectively

\[
\begin{aligned}
3\binom q2-1-
 \left(\binom{a+9}{3}-\binom a3\right)
&=\frac{3t^2-69t-170}{2},\\
&=\frac{3t^2-57t-170}{2},
\end{aligned}
\tag{4.103}
\]

which are positive for \(t\ge26\).  Lemma 4.13 and nine promotions now
give an excess over (4.102) of, respectively,

\[
\begin{aligned}
\binom{a+9}{4}-\binom a4-\binom{q+1}{3}
&=\frac{t^3+81t^2+416t+756}{6},\\
&=\frac{t^3+69t^2+410t+756}{6}.
\end{aligned}
\tag{4.104}
\]

Both are strictly positive.  The remaining feasible values
\(16\le q\le51\) are a finite endpoint set; exact canonical arithmetic
gives

\[
\min_{16\le q\le51}
\left\{{\cal P}_{\lfloor q/2\rfloor}
 \left(3\binom q2-1\right)-\binom{q+1}{3}\right\}=386.
\tag{4.105}
\]

Suppose instead that \(A<a\).  Then \(x<\binom a3\), while
\(S_2(n)\ge\binom{q+1}{3}\).  Hence

\[
\binom K2>
R_q:=\binom{q+1}{3}-\binom a3.
\tag{4.106}
\]

Superadditivity and (4.101) yield

\[
U_3(x+d)-U_3(x)\ge U_3(d)\ge U_3(D_{K,q}).
\tag{4.107}
\]

For \(q\ge92\), this last quantity is larger than (4.102) by a direct
root estimate.  Set

\[
p=\left\lfloor\frac{31}{20}q^{3/4}\right\rfloor.
\]

Since \(a\le q/2\), (4.106) gives

\[
K>\sqrt{2R_q}>\frac{27}{50}q^{3/2}.
\]

Using \(J>2K/q-1\) in (4.101), and \(q^{1/4}>3\), gives

\[
D_{K,q}>
(q-1)\left(\frac{27}{50}q^{3/2}-\frac q2\right)-1
>q^{9/4}>\binom p3.
\tag{4.108}
\]

For the middle inequality, after division by \(q^{9/4}\) the displayed
lower bound is greater than

\[
\frac{91}{92}\frac{109}{75}-\frac1{8464}>1
\qquad(q\ge92).
\]

The last inequality in (4.108) uses
\((31/20)^3/6<1\).  Moreover

\[
\left(\frac{31}{20}-\sqrt2\right)q^{3/4}>4
\qquad(q\ge92),
\]

so \(p-3>\sqrt2\,q^{3/4}\).  Consequently

\[
U_3(D_{K,q})\ge\binom p4
>\frac{(p-3)^4}{24}
>\frac{q^3}{6}
>\binom{q+1}{3}.
\tag{4.109}
\]

It remains only \(q\le91\).  Feasibility of \(x\ge0\) forces

\[
\binom K2\le\binom{q+1}{3}+\binom q2,
\tag{4.110}
\]

and \(K\ge39\) forces \(q\ge16\).  Conditions (4.59), (4.106), and
(4.110) leave exactly \(738\) odd pairs \((K,q)\).  Applying the exact
quantity \(D_{K,q}\) at those finite endpoints gives

\[
\min\left\{U_3(D_{K,q})-\binom{q+1}{3}\right\}
=1150,
\tag{4.111}
\]

attained at \((K,q)=(39,16)\).  Equations (4.98), (4.102), and the two
cases prove \(\gamma_5>0\).  \(\square\)

Combining Theorems 4.11, 4.12, and 4.14 proves the full synchronized
rank-four/rank-five bridge (4.58).  This closes every borrow state in the
synchronized cap chamber; no empirical strip scan is used for its infinite
tail.  It does **not** close the separate pre-cap adaptive-rank problem.

## 5. Scope and impact

This result refutes an intermediate sufficient lemma, **not Erdős
#776**.  It invalidates the claimed implication from one universal
rank-six tail inequality to the rank-42 capacity theorem.  The exact
rank-42 and rank-248 reductions remain valid, but their present proof
route now needs either

1. an adaptive post-carry rank depending on the strip, or
2. a capacity argument that does not pass through adjacent diagonal
   surplus.

The falsifier is especially informative because (4.6) rules out every
fixed-rank patch of the same form.
