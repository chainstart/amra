# Erdős #809 — degree-spread barrier for a maximum-witness opposite star

Date: 2026-08-02

Status: PROVED__INDEPENDENTLY_BLIND_AUDITED_AFTER_LOCAL_REPAIR

## 0. Outcome

Let \(v\) be a maximum-degree vertex in an \(n\)-vertex graph with
\(e(G)=\lfloor n^2/4\rfloor+1\) and \(\delta(G)\ge3\).  Put
\(g=\Delta(G)-\delta(G)\).  If two vertices \(b,c\notin N[v]\) satisfy

\[
 bc\notin E(G),\qquad
 N(b)\cap N(c)=\varnothing,\qquad
 E(N(b),N(c))=\varnothing,
\]

then

\[
 n\le
 \begin{cases}
 2g^2-2g-6,&n\ \mathrm{even},\\
 2g^2-2g-3,&n\ \mathrm{odd}.
 \end{cases}
\]

Thus a single opposite-neighbourhood pair forces
\(g=\Omega(\sqrt n)\).  Both constants are attained by explicit graph
families; for every \(g\ge5\) those families also satisfy \(L_4(2)\)
and admit a rainbow-\(C_7\) colouring.  They can realize local
repeated-colour zero-shore provenance, but their entire colour defect is
paid by the forced reserve, so they do not realize the hard
reserve-failure branch.

## 1. Setup

Let \(G\) have

\[
 e(G)=\left\lfloor\frac{n^2}{4}\right\rfloor+1,
\]

let \(v\) be a maximum-degree witness, and put

\[
 \Delta=d(v),\qquad
 \delta=\delta(G),\qquad
 g=\Delta-\delta,\qquad
 \kappa=n-2\delta,
\]

\[
 A=N[v],\qquad B=V(G)\setminus A.
\]

Suppose \(b,c\in B\) form an opposite-neighbourhood zero-shore pair.
Thus, with \(P=N(b)\) and \(Q=N(c)\),

\[
 bc\notin E(G),\qquad P\cap Q=\varnothing,\qquad E(P,Q)=\varnothing.
\]

Write

\[
 \rho_c=n-d(b)-d(c).
\]

## 2. Two maximum-witness basepoints

For a coherent opposite star with leaf set \(L\), retain

\[
 U=\bigcup_{c\in L}N(c),\qquad
 C=V(G)\setminus N(b),\qquad
 R=C\setminus U,\quad r=|R|,
\]

and \(T=L\setminus U,\ t=|T|\).  Since every star vertex lies in \(B\),
the maximum witness \(v\) is adjacent to neither \(b\) nor any leaf.
The centre is also adjacent to no leaf.  Therefore

\[
\boxed{
 \{b,v\}\mathbin{\dot\cup}T\subseteq R,
 \qquad r\ge t+2.
}
\tag{1}
\]

For each leaf, the three distinct vertices \(b,c,v\) all lie outside
\(N(b)\cup N(c)\).  Hence

\[
\boxed{3\le\rho_c\le\kappa.}
\tag{2}
\]

This is one unit stronger at both places than the colouring-free
common-host bound.

## 3. An edge-budget lower bound on every residual

Let

\[
 \overline M=\binom n2-e(G).
\]

Three disjoint families of missing pairs are forced:

- all \(d(b)d(c)\) pairs in \(P\times Q\);
- all pairs incident with \(b\) outside \(P\);
- all pairs incident with \(c\) outside \(Q\), with \(bc\) counted only
  once.

Consequently

\[
 \overline M
 \ge d(b)d(c)+n+\rho_c-3.
\tag{3}
\]

Since \(d(b),d(c)\ge\delta\) and
\(d(b)+d(c)=n-\rho_c=2\delta+\kappa-\rho_c\),

\[
 d(b)d(c)
 \ge\delta^2+\delta(\kappa-\rho_c).
\]

Thus every opposite leaf satisfies

\[
\boxed{
 \rho_c\ge
 \rho_{\rm edge}:=
 \left\lceil
 \frac{\delta^2+\delta\kappa+n-3-\overline M}
      {\delta-1}
 \right\rceil.
}
\tag{4}
\]

The denominator is positive under the standing \(\delta\ge3\)
hypothesis.

There is also an aggregate lower bound on the common residual after
removing its isolated leaves.  The sets \(U\) and \(T\) are disjoint and
\(P=N(b)\) is anticomplete to both.  In addition, all pairs from \(b\)
to \(V\setminus(P\cup\{b\})\), and all \(\ell\) pairs from \(v\) to
the leaves, are missing.  These three families are disjoint.  Minimizing
over \(p=|P|\), subject to \(p\ge\delta\) and
\(|U|+t=n-p-(r-t)\ge\delta\), gives

\[
\begin{aligned}
\overline M
&\ge p\bigl(n-p-(r-t)\bigr)+n-p-1+\ell\\
&\ge
\delta\bigl(n-(r-t)-\delta\bigr)
 +(r-t)+\delta-1+\ell.
\end{aligned}
\]

Indeed the first line is concave in \(p\), so its minimum on
\([\delta,n-(r-t)-\delta]\) is at an endpoint; the second endpoint is
the smaller one because \(r-t\le\kappa\).  Rearrangement gives

\[
\boxed{
 r-t\ge
 d_{\rm edge}:=
 \left\lceil
 \frac{\delta^2+\delta\kappa+\delta-1+\ell-\overline M}
      {\delta-1}
 \right\rceil.
}
\tag{4a}
\]

There is one more exact gain from the degree cap.  Put
\(d=r-t\) and

\[
 W_R=R\setminus(\{b\}\cup T),\qquad |W_R|=d-1.
\]

Every vertex of \(W_R\) is nonadjacent to \(b\) and to all \(\ell\)
leaves.  Its remaining potential-neighbour set has size exactly
\(n-\ell-2\), so it misses at least
\((n-\ell-2-\Delta)_+\) pairs inside that set.  Summing over \(W_R\)
and allowing every missing pair internal to \(W_R\) to be counted twice
gives the disjoint additional budget

\[
\boxed{
\begin{aligned}
\overline M\ge{}&
p(n-p-d)+n-p-1+(d-1)\ell\\
&+
\left(
(d-1)(n-\ell-2-\Delta)_+
-\binom{d-1}{2}
\right)_+,
\qquad p=d(b).
\end{aligned}}
\tag{4b}
\]

The first three terms count respectively
\(P\times(U\cup T)\), all missing pairs incident with \(b\), and
\(W_R\times L\).  The last term counts only missing pairs from
\(W_R\) to \(P\cup(U\setminus L)\cup W_R\), so the four families are
disjoint.

## 4. Degree spread must be at least four

The average degree and maximality of \(v\) give

\[
 \Delta\ge
 \left\lceil\frac{2e(G)}n\right\rceil.
\]

Writing \(n=2m\) or \(2m+1\), direct evaluation gives

\[
\boxed{
 \kappa\le
 \begin{cases}
 2g-2,&n=2m,\\
 2g-1,&n=2m+1.
 \end{cases}}
\tag{5}
\]

If \(g\le2\), the only largest possibilities are
\(\kappa=2\) in even order and \(\kappa=3\) in odd order.  In both
cases (4) gives \(\rho_{\rm edge}\ge4\), contradicting
\(\rho_c\le\kappa\).  This proves \(g\ge3\); combining it with the
\(g=3\) exclusion in the next section gives

\[
\boxed{g\ge4}
\tag{6}
\]

for every maximum-witness B-opposite obstruction.  The first
arithmetically possible layer \(g=3\) is eliminated by (4a)--(4b).

## 5. Elimination of the apparent endpoint \(g=3\)

The same arithmetic first makes this layer finite, after which the
degree-cap budget empties it.

### Even order

If \(n=2m\) and \(g=3\), then necessarily

\[
 \kappa=4,\qquad m\ge6,\qquad \rho_c=4\quad(c\in L).
\tag{7}
\]

Hence

\[
 A_L=(4-r)\ell,\qquad 2\le r\le4,\qquad
 t\le r-2,\qquad r-t\ge3.
\tag{8}
\]

Let \(\mu=M(G[L])\), and let \(E_A,E_B\) be the external incidence
deficits of the three-budget identity.  That identity becomes

\[
\boxed{
 (3-r+t)\ell=2\mu+E_A+E_B.
}
\tag{9}
\]

Put \(d=r-t\).  Since the right-hand side of (9) is nonnegative,
\(d\le3\).  On the other hand, (4a) reads

\[
 d\ge
 \left\lceil2+\frac{\ell}{m-3}\right\rceil\ge3.
\]

Thus

\[
 d=3,\qquad \ell\le m-3.
\tag{9a}
\]

Here \(p=d(b)=m-2\).  Substitute \(n=2m\), \(\Delta=m+1\),
\(d=3\), and (9a) into (4b).  If \(\ell\le m-4\), its right-hand
side is

\[
 (m-2)(m-1)+(m+1)+2\ell
 +2(m-\ell-3)-1=m^2-4.
\]

If \(\ell=m-3\), the final positive-part term vanishes and the right-hand
side is \(m^2-3\).  Both values are strictly larger than

\[
 \overline M=m^2-m-1
\]

for \(m\ge6\), a contradiction.  Hence there is no even-order
\(g=3\) B-opposite obstruction.

### Odd order

If \(n=2m+1\) and \(g=3\), then

\[
 \kappa=5,\qquad
 \rho_c\in\{4,5\}.
\tag{10}
\]

Put \(u=|\{c:\rho_c=5\}|\).  Then the complete scalar conservation
law is

\[
\boxed{
 A_L=(4-r)\ell+u,\qquad
 2\le r\le5,\qquad
 t\le r-2,\qquad
 r-t\ge3\ \hbox{if }\ell\ge3,
}
\tag{11}
\]

\[
\boxed{
 (3-r+t)\ell+u=2\mu+E_A+E_B.
}
\tag{12}
\]

In this parity \(\delta=m-2\), \(\Delta=m+1\), and
\(|B|=m-1\), so \(\ell\le m-1\).  The centre degree is either
\(p=d(b)=m-2\) or \(m-1\).  If \(p=m-1\), every residual is four,
so \(u=0\), and (12) gives \(d=r-t\le3\).  If \(p=m-2\), then
\(u\le\ell\), and (12) gives \(d\le4\).

Suppose first that \(\ell\le m-3\).  Replacing the last positive part
in (4b) by its (possibly negative) argument and simplifying gives the
valid weaker lower bounds

\[
 \overline M\ge
 \begin{cases}
 m^2+m+1-d-\binom{d-1}{2}\ge m^2+m-3,
     &p=m-1,\ d\le3,\\[2mm]
 m^2+m-2-\binom{d-1}{2}\ge m^2+m-5,
     &p=m-2,\ d\le4.
 \end{cases}
\tag{12a}
\]

If instead \(\ell\ge m-2\), discard the nonnegative final term of
(4b) and use \(\ell\ge m-2\).  This gives

\[
 \overline M\ge
 \begin{cases}
 m^2+m+1-d\ge m^2+m-2,&p=m-1,\ d\le3,\\
 m^2+m-2,&p=m-2,\ d\le4.
 \end{cases}
\tag{12b}
\]

Every bound in (12a)--(12b) is strictly larger than
\(\overline M=m^2-1\) for \(m\ge5\).  This contradiction eliminates
the odd-order \(g=3\) layer as well.

## 6. All-parameter square-root barrier

The same degree-cap budget gives substantially more than the constant
barrier, and only one opposite pair is needed.  Fix any leaf \(c\) and
specialize the common-host notation to \(L=\{c\}\).  Then

\[
 \ell=t=1,\qquad r=\rho_c,\qquad d=r-t=\rho_c-1.
\tag{15}
\]

Equivalently,
\[
 W_R=V(G)\setminus\bigl(N(b)\cup N(c)\cup\{b,c\}\bigr),
 \qquad |W_R|=d-1.
\]
Thus the four families behind (4b) are, in this specialization,
\(N(b)\times(N(c)\cup\{c\})\), all missing pairs incident with \(b\),
\(W_R\times\{c\}\), and the remaining maximum-degree deficits of
\(W_R\).  No multi-leaf hypothesis is being retained.

Put \(p=d(b)\).  Since
\(d(c)=n-p-\rho_c=n-p-d-1\ge\delta\), while \(p\ge\delta\),

\[
 \delta\le p\le n-\delta-d-1,
 \qquad 2\le d\le\kappa-1.
\tag{16}
\]

The last inequality also uses \(\rho_c\ge3\), proved in (2).
Specializing (4b) to \(\ell=1\), and using

\[
 (d-1)+
 \left((d-1)(n-3-\Delta)_+
       -\binom{d-1}{2}\right)_+
 \ge
 (d-1)(n-2-\Delta)-\binom{d-1}{2},
\]

\[
 p(n-p-d)+n-p-1=p(n-d-1-p)+n-1
\]

is concave in \(p\), and its two endpoints in (16) have the same
value.  Therefore

\[
 \overline M\ge \mathcal L_0:=
 \delta(n-d-1-\delta)+n-1
 +(d-1)(n-2-\Delta)-\binom{d-1}{2}.
\tag{17}
\]

Let \(h=\kappa-d-1\ge0\).  If \(n\) is even, put
\(a=2g-\kappa\ge2\), using (5).  Direct subtraction of
\(\overline M=n^2/4-n/2-1\) from (17) gives the exact identity

\[
 \mathcal L_0-\overline M
 =\delta-g^2+2g+2
 +\frac{a^2-4+2h(2g-h-1)}4.
\tag{18}
\]

Here \(h\le\kappa-3\le2g-5\), so the final fraction is nonnegative.
The necessary inequality \(\mathcal L_0\le\overline M\) yields

\[
 \delta\le g^2-2g-2,
 \qquad
 \boxed{n\le2g^2-2g-6}\quad(n\ \mathrm{even}).
\tag{19}
\]

If \(n\) is odd, set \(a=2g-\kappa\ge1\).  The corresponding exact
identity is

\[
 \mathcal L_0-\overline M
 =\delta-g^2+2g+1
 +\frac{a^2-1+2h(2g-h-1)}4.
\tag{20}
\]

Again the fraction is nonnegative, now because
\(h\le\kappa-3\le2g-4\).  Hence

\[
 \delta\le g^2-2g-1,
 \qquad
 \boxed{n\le2g^2-2g-3}\quad(n\ \mathrm{odd}).
\tag{21}
\]

Equivalently, every maximum-witness B-opposite obstruction satisfies

\[
\boxed{
 g\ge
 \begin{cases}
 \left\lceil(1+\sqrt{2n+13})/2\right\rceil,&n\ \mathrm{even},\\[1mm]
 \left\lceil(1+\sqrt{2n+7})/2\right\rceil,&n\ \mathrm{odd}.
 \end{cases}}
\tag{22}
\]

If the pair is additionally a genuine one-leaf repeated-colour
zero-shore obstruction, put \(Z=D_B-h_c\).  The independently audited
defect-slack inequality specializes to

\[
 \rho_c+(\rho_c-2)\le2g+2Z,
\]

and therefore

\[
\boxed{Z\ge\rho_c-1-g=d-g.}
\tag{22b}
\]

Thus equality in the graph-geometric even and odd bounds would cost,
respectively, at least \(g-3\) and \(g-2\) units of unpaid colour defect.
The recoloured sharpness graphs below have no unpaid defect at all: their
reserve test succeeds, so (22b), which assumes reserve failure, does not
apply to them.

The bound is sharp at the level of the uncoloured graph structure used
in this theorem.  For every \(g\ge4\), equality in (19) has parameters

\[
 \delta=g^2-2g-2,\quad \kappa=2g-2,\quad
 p=\delta,\quad \ell=1,\quad d=\kappa-1,\quad\rho=\kappa,
\]

and equality in (21) by the same pattern with
\(\delta=g^2-2g-1\) and \(\kappa=2g-1\).

Here is one graph realizing either profile.  Take disjoint sets
\(P,U,W\), two further vertices \(b,c\), and put

\[
 |P|=|U|=\delta,\qquad
 |W|=\kappa-2,\qquad \Delta=\delta+g.
\]

Make \(P\) and \(U\) cliques, join \(b\) exactly to \(P\), join \(c\)
exactly to \(U\), and leave \(W\) independent.  Finally put a balanced
bipartite graph between \(W\) and \(P\cup U\), with every \(W\)-degree
equal to \(\Delta\) and every right degree at most \(g\).  Such a graph
is explicit: order \(P\cup U\) cyclically and give the \(i\)-th vertex
of \(W\) the \(\Delta\) consecutive positions starting at
\(i\Delta\).  The right degrees differ by at most one.  The inequalities

\[
 \Delta<2\delta,\qquad |W|\Delta\le2\delta g
\]

hold for both displayed parameter families when \(g\ge4\), so the
construction is legal.  Explicitly, \(2\delta-\Delta\) equals
\(g^2-3g-2\) in even order and \(g^2-3g-1\) in odd order, while
\(2\delta g-|W|\Delta\) equals respectively
\(2(g^2-2g-4)\) and \(g^2-3g-3\); all four quantities are nonnegative
for \(g\ge4\) (and the first two are positive).

The cyclic balancing also gives every vertex of \(P\cup U\) at least
\(g-1\) neighbours in \(W\): indeed
\(|W|\Delta-2\delta(g-1)\) equals \(4\) in even order and
\(g^2-g+1\) in odd order, while the balanced right degrees differ by
at most one.  Every interval of length
\(\Delta=\delta+g\) in the cyclic ordering of two consecutive
\(\delta\)-blocks contains at least \(g\) points of each block.
Consequently, every \(w\in W\) has at least \(g\) neighbours in each
of \(P,U\).

There are

\[
 \delta^2+\delta+|W|\Delta
 =
 \begin{cases}
  (\delta+g-1)^2+1,&n\ \mathrm{even},\\
  (\delta+g-1)(\delta+g)+1,&n\ \mathrm{odd}
 \end{cases}
\]

edges.  Thus \(e(G)=\lfloor n^2/4\rfloor+1\),
\(\delta(G)=\delta\), and \(\Delta(G)=\Delta\).  Moreover
\(N(b)=P\), \(N(c)=U\), and \(P\) is anticomplete to \(U\).
Any \(v\in W\) is a maximum-degree witness with \(b,c\notin N[v]\),
while the one-leaf common residual has \(r=\rho=\kappa\) and
\(d=\kappa-1\).  This proves graph-level sharpness of (19) and (21).

The colouring firewall can be made exact.  Every \(v\in W\) has at least
\(g\) neighbours in each of \(P,U\).  Choose distinct
\(x_1,\ldots,x_g\in N(v)\cap P\) and
\(y_1,\ldots,y_g\in N(v)\cap U\), give \(bx_i,cy_i\) one common colour
\(\gamma_i\), and colour every other edge injectively.  Each two-edge
colour class is induced.  It cannot lie on a \(C_7\).  Indeed, deleting
\(bx_i,cy_i\) would leave two paths of total length five, with endpoint
pairing either

\[
 (b,c),(x_i,y_i)
 \quad\hbox{or}\quad
 (b,y_i),(x_i,c).
\]

All four endpoint pairs are nonadjacent.  In the second pairing neither
pair even has a two-edge path: \(N(b)=P\) has no edge to
\(y_i\in U\), and \(N(c)=U\) has no edge to \(x_i\in P\).  Its two
paths would therefore have total length at least six.  In the first
pairing \(b,c\) have no two-edge path because \(P\cap U=\varnothing\),
so their path would have to be the length-three member.  Such a path
would have type \(b-P-U-c\), impossible because \(P\) is anticomplete
to \(U\).  Hence the new colouring is still rainbow on every \(C_7\),
and the active pair \(bc\) has multiplicity \(h_c=g\).

This does **not** produce the hard B-opposite branch.  Relative to
\(A=N[v]\), the recolouring has \(D_B=g\).  If
\(B=V(G)\setminus A\), the missing-star part alone of the zero-shore
reserve has size

\[
 \overline d_B(b)+\overline d_B(c)-1
 =\delta+2\kappa-g-5
 =\begin{cases}
   g^2+g-11,&n\text{ even},\\
   g^2+g-8,&n\text{ odd},
  \end{cases}
 \ge g=D_B.
\tag{22c}
\]

Thus the global reserve-union test closes immediately.  The examples
realize local repeated-colour zero-shore provenance, but rigorously fail
the reserve-failure condition required of a hard obstruction.  This also
explains why the positive slack demanded by (22b) is absent here.

In fact, for \(g\ge5\) this graph satisfies \(L_4(2)\).  After deleting
at most two non-endpoints, use the following type templates, together
with their images under \(b,P\leftrightarrow c,U\):

\[
\begin{array}{c|c}
\text{endpoint types}&\text{exact four-edge path types}\\ \hline
b,c&b-P-W-U-c\\
b,P&b-P-P-P-P\\
b,U&b-P-P-W-U\\
b,W&b-P-P-P-W\\
P,P&P-P-P-P-P\\
P,U&P-P-W-U-U\\
P,W&P-P-P-P-W\\
W,W&W-P-P-P-W .
\end{array}
\tag{22a}
\]

The two endpoint-side degree bounds above leave at least two choices
after the deletions, and \(\delta\ge13\) leaves all clique filler
vertices distinct.  Thus every template can be instantiated without a
deleted or repeated vertex.  Giving every edge a distinct colour makes
every \(C_7\) rainbow.  Hence the constants remain sharp even under the
local \(L_4(2)\) and rainbow conditions.  The recolouring above shows
that local repeated-colour provenance is possible, but (22c) proves that
it belongs to the reserve-paid branch rather than a genuine hard
counterexample to Erdős #809.

## 7. Proof of the endpoint statements

For \(n=2m\),

\[
 \overline M=m^2-m-1,\qquad
 \left\lceil\frac{2e(G)}n\right\rceil=m+1.
\]

For \(n=2m+1\),

\[
 \overline M=m^2-1,\qquad
 \left\lceil\frac{2e(G)}n\right\rceil=m+1.
\]

Substituting \(\delta=m-k\), with
\(\kappa=2k\) or \(2k+1\), into (4) gives respectively

\[
 \rho_{\rm edge}
 =
 \left\lceil
 \frac{3m-k^2-2}{m-k-1}
 \right\rceil
\quad(n=2m),
\tag{23}
\]

\[
 \rho_{\rm edge}
 =
 \left\lceil
 \frac{3m-k^2-k-1}{m-k-1}
 \right\rceil
\quad(n=2m+1).
\tag{24}
\]

Equations (5)--(7) and (10) follow immediately.  Equations (8),
(11), and the bounds on \(t\) follow from
\(R_L=\ell r+A_L=\sum_c\rho_c\) and (1).  Substitution into the exact
three-budget conservation identity proves (9) and (12).  The
contradictions following (9) and (12) are direct substitutions into
the independently counted missing-pair budget (4b).  QED.

## 8. Boundary

This theorem forces square-root degree spread in the maximum-witness
B-opposite branch, with parity-sharp constants already realized by
graphs satisfying \(L_4(2)\) and a rainbow colouring.  It does not
eliminate the surviving \(g=\Omega(\sqrt n)\) regime, B-same, Branch A,
or the other BCM witness branches.  Erdős #809 remains open.

## 9. Reproduction

\[
\texttt{python3 verify\_maximum\_witness\_degree\_spread.py}
\]

The verifier checks the parity formulas, residual roots, the complete
\(g\le3\) exclusion, the all-parameter square-root comparison and its
sharp graph endpoints, and all scalar conservation identities.  Full
finite graph guards are also run by
`test\_opposite\_star\_common\_host.py`.
