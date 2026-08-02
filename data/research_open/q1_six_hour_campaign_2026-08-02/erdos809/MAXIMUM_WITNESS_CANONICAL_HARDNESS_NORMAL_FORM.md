# Erdős #809 — canonical hardness normal form for the maximum witness

Date: 2026-08-02

Status: `PROVED_COMPOSITION__INDEPENDENTLY_CROSS_AUDITED_AFTER_REPAIR__PAIRWISE_SQRT_SHARPENING_INDEPENDENTLY_BLIND_AUDITED_AFTER_LOCAL_REPAIR`

## 1. Exact outer-`A` coordinate

Throughout, \(G\) is a finite simple \(L_4(2)\) graph with
\(\delta(G)\ge3\), every \(C_7\) in the given edge-colouring is rainbow,
and \(v\) is a maximum-degree vertex.  Use the partition
`A=N[v]`, `B=V(G)\setminus A`, and write

\[
 q_*=2+\left\lfloor\frac{1+\sqrt{1+8M_B}}2\right\rfloor.
\tag{1}
\]

Let `E_low` be the good edges with no admissible outer endpoint of
`B`-degree at least `q_*`, and let `N_low` be the number of nonempty
good colour classes wholly contained in `E_low`.  The exact low-degree
localization theorem gives

\[
 \boxed{D_A=|E_{\rm low}|-N_{\rm low}.}
\tag{2}
\]

Consequently the good-edge closure condition is equivalent to the one
canonical inequality

\[
 \boxed{
 |E_{\rm low}|-N_{\rm low}\le M_B+S_m.
 }
\tag{3}
\]

No orientation choice remains in (2).  This equivalence concerns the
number of colours represented on good edges.  It is sufficient, but not
necessary, for the public total-colour target because colours supported
wholly in \(G[B]\) also count.  In particular, every genuine counterexample
to the public target must violate (3).

There is a second exact coordinate in which the cross-low term disappears.
Let \(I_{\rm mix}(q_*)\) count colours whose unique high good edge is
internal to \(A\) and which also contain an \(A\)--\(B\) good edge.  Let
\(N_{\rm int}(q_*)\) count nonempty good colour classes with neither a
high good edge nor an \(A\)--\(B\) edge.  Then

\[
 \boxed{
 R_A=e(G[A_{<q_*}])+I_{\rm mix}(q_*)-N_{\rm int}(q_*).
 }
\tag{2a}
\]

Thus the only positive cross-origin term surviving in \(R_A\) is anchored
to a distinct high internal edge.

If \(h_A=|A_{<q_*}|\) and \(g=|A|-\delta(G)-1\), the internal-low
dense-exit theorem adds the hard-instance restriction

\[
 \boxed{
 h_A\le2g+2q_*+4
 \quad\text{or}\quad
 e(G[A_{<q_*}])<\Phi(n,e).
 }
\tag{3a}
\]

In the second alternative,

\[
 h_A(h_A-g-q_*)<2\Phi(n,e).
\tag{3b}
\]

## 2. Exact reserve branches

Let `mathcal Q` be the inherited global reserve union.  Consider a genuine
hard maximum-witness counterexample, so in particular (3) fails and no
direct compatible-edge exit has already supplied the public colour
target.  Exactly one of the following reserve branches holds.

### Branch A: the `B` defect is paid

If

\[
 |\mathcal Q|\ge D_B,
\]

then `D_B<=M_B`, and the entire failure is forced into the canonical
low-degree outer residue:

\[
 \boxed{
 R_A-S_m
 =D_A-D_B-S_m
 \ge D_A-M_B-S_m>0.
 }
\tag{4}
\]

Thus this branch no longer has an unspecified outer-`A` object: it is
the explicit quantity in (2), minus `D_B+S_m`.  Equivalently, every hard
counterexample in Branch A must satisfy the sharper anchored gate

\[
 \boxed{
 e(G[A_{<q_*}])+I_{\rm mix}(q_*)-N_{\rm int}(q_*)>S_m.
 }
\tag{4a}
\]

### Branch B: global reserve obstruction

If

\[
 |\mathcal Q|\le D_B-1,
\tag{5}
\]

put

\[
 d_0=\binom{\delta(G)}2,\qquad
 \overline M=\binom n2-e(G),\qquad
 \kappa=n-2\delta(G).
\tag{5a}
\]

The inherited global weighted obstruction theorem supplies an
inclusion-maximal repeated-zero matching \(F\), with
\(f=|F|\) and \(H_F=\sum_{e\in F}h_e\), satisfying

\[
\boxed{
 f\le
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}},
 \qquad
 H_F\le
 \min\left\{
 \frac{|A|}{2}\sqrt{D_B-1},
 \frac{\overline M}{d_0}\sqrt{M_A(D_B-1)}
 \right\}.}
\tag{5b}
\]

For the coherent star selected from \(F\), let \(\ell\) be its number
of leaves, let \(h_c\ge2\) be the repeated-pair multiplicity of leaf
\(c\), and put \(H=\sum_c h_c\), \(W=H-\ell\).  The exact colour-defect
mass ledger gives the universal constraints

\[
 \boxed{
 2\ell\le H\le D_B,
 \qquad
 E_0\le4f(D_B-\ell).
 }
\tag{5b'}
\]

It then has two exhaustive structural subbranches.

#### Branch B-same: same-neighbourhood concentration

If the selected coherent star is of same-neighbourhood type, the complete
explicit necessary constraint is

\[
\boxed{
 E_0\le4f(\kappa-1)L(D_B-1,\kappa),
 \qquad
 L(q,\kappa)=
 \left\lfloor
 \frac{2\kappa+1+\sqrt{(2\kappa+1)^2+8q}}2
 \right\rfloor.}
\tag{5c}
\]

This cap is a live subbranch, not an automatic contradiction.

#### Branch B-opposite: opposite-neighbourhood concentration

Otherwise the inherited theorem supplies one opposite star, retaining
the quantities \(\ell,h_c,H,W\) from (5b'), and

\[
 U=\bigcup_{c\in L}N(c),\qquad
 \rho_c=n-d(b)-d(c),
\]

\[
 R_L=\sum_c\rho_c,
 \quad g=|A|-\delta(G)-1,
 \quad t=|L\setminus U|.
\tag{6}
\]

The new common-host reductions put this opposite residue into the
following explicit feasibility system.  There are integers

\[
 t+2\le r\le\kappa=n-2\delta(G),
 \qquad
 A_L=R_L-\ell r,
 \qquad
 0\le A_L\le\ell(\kappa-r),
\tag{7}
\]

such that

\[
 \boxed{
 2|\mathcal Q|
 \ge
 2\sum_{c\in L}(h_c+\rho_c-\lambda)
 -\sum_{c\in L}\min\{\ell-1,\rho_c-2\},
 \qquad
 \lambda=|A|+1-\delta(G).
 }
\tag{8}
\]

In particular,

\[
 \boxed{
 2|\mathcal Q|\ge2W+R_L-2g\ell,
 }
\tag{9}
\]

and the sharper defect-slack form

\[
 Z=D_B-H,\qquad
 \Xi=\sum_{c\in L}(\rho_c-\ell-1)_+,
\]

\[
 \boxed{
 R_L+\Xi
 \le2(g+1)\ell+2Z-2.
 }
\tag{9a}
\]

Consequently,

\[
 \boxed{
 \ell t+A_L+\Xi
 \le2g\ell+2Z-2.
 }
\tag{9b}
\]

Since every \(\rho_c\ge3\), this also forces

\[
 \boxed{(2g-1)\ell+2Z\ge2.}
\tag{9c}
\]

The exact edge count gives the further individual-residual and
degree-spread barriers

\[
 \boxed{
 \rho_c\ge
 \left\lceil
 \frac{\delta(G)^2+\delta(G)\kappa+n-3-\overline M}
      {\delta(G)-1}
 \right\rceil
 \quad(c\in L),
 }
\tag{9d}
\]

\[
 \boxed{
 r-t\ge
 \left\lceil
 \frac{\delta(G)^2+\delta(G)\kappa+\delta(G)-1+\ell-\overline M}
      {\delta(G)-1}
 \right\rceil.
 }
\tag{9e}
\]

Put \(p=d(b)\) and \(d=r-t\).  The maximum-degree cap gives the
additional disjoint missing-pair budget

\[
 \boxed{
 \begin{aligned}
 \overline M\ge{}&
 p(n-p-d)+n-p-1+(d-1)\ell\\
 &+\left(
 (d-1)(n-\ell-2-\Delta)_+
 -\binom{d-1}{2}
 \right)_+.
 \end{aligned}}
\tag{9f}
\]

\[
 \boxed{
 \begin{array}{c|c|c|c}
 &\kappa&\delta&n\\ \hline
 n\ {\rm even}&\le2g-2&\le g^2-2g-2&\le2g^2-2g-6\\
 n\ {\rm odd}&\le2g-1&\le g^2-2g-1&\le2g^2-2g-3
 \end{array}
 }
\tag{9g}
\]

Equivalently,

\[
 \boxed{
 g\ge
 \begin{cases}
 \left\lceil(1+\sqrt{2n+13})/2\right\rceil,&n\ {\rm even},\\
 \left\lceil(1+\sqrt{2n+7})/2\right\rceil,&n\ {\rm odd}.
 \end{cases}}
\tag{9h}
\]

Thus every surviving B-opposite obstruction has square-root degree
spread.  The parity constants are attained by explicit graphs satisfying
the local degree/opposite-shore hypotheses and, for \(g\ge5\),
\(L_4(2)\).  They even admit rainbow recolourings with one zero-shore
pair of multiplicity \(g\), but its missing-star reserve pays all
\(D_B=g\).  Thus they realize local repeated-colour provenance but not
the reserve-failure provenance of a genuine hard counterexample.  The
complete calculation is recorded in
`MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md`.

\[
 \boxed{
 |\mathcal Q|\ge
 \binom\ell2-
 \binom{\min\{\ell,A_L\}}2,
 }
\tag{10}
\]

and, with

\[
 a_B=\left\lfloor
 \frac{1+\sqrt{1+8(D_B-1)}}2
 \right\rfloor,
 \qquad
 a_*=\min\{\ell,a_B\},
 \qquad
 x_0=\left\lceil\frac H{a_*}\right\rceil,
 \qquad
 \eta_B=\max\left\{
 0,\,
 A_L+\ell(t-1)-(D_B-1)
 -\min\left\{D_B-1,\binom\ell2\right\}
 \right\},
 \qquad
 y_0=\left\lceil\frac{H+\eta_B}\ell\right\rceil,
\tag{11}
\]

\[
 \boxed{M_A\ge x_0y_0,}
\tag{12}
\]

\[
\boxed{
 M_B\ge
 x_0(y_0-g)_+ +y_0(x_0-g)_+-M_A+L_m.
 }
\tag{13}
\]

In particular, the selected opposite star obeys the
synchronization-free weighted cap

\[
 \boxed{
 E_0\le
 4f\left(
 \left\lfloor
 \frac{\sqrt{\eta_B^2+4a_*\ell M_A}-\eta_B}{2}
 \right\rfloor-\ell
 \right).
 }
\tag{13a}
\]

For the common complementary host, put

\[
 P=N(b),\qquad C=V(G)\setminus P,
 \qquad
 \Psi_e(p)=\binom p2+\binom{n-p}{2}-e(G).
\tag{13b}
\]

It also obeys the exact energy and synchronization statements

\[
 M(P)+M(C)\le\Psi_e(|P|)+|P|r,
\tag{14}
\]

\[
 |N(c)\mathbin\triangle N(d)|\le2(\kappa-r)
 \quad(c,d\in L).
\tag{15}
\]

Every genuine hard counterexample violates (3), satisfies the disjunction
(3a), and satisfies (3b) whenever the second arm of (3a) holds.  It also
satisfies exactly one of:

- Branch A: (4)--(4a);
- Branch B-same: (5), (5a)--(5c), and (5b');
- Branch B-opposite: (5), (5a)--(5b), (5b'), and (6)--(15),
  including the sharpened obstructions (9a)--(9c).

This is one finite exhaustive list of scalar/structural obstructions.
The previous free residual sum `R_L` and separate undefined `R_A` no
longer occur without coordinates.

At the perfect-synchronization endpoint `A_L=0`, the system has the
additional closed weighted cap

\[
 E_0\le4f(M_A+D_B-1-\ell),
\tag{16}
\]

so the unresolved opposite branch may be restricted to positive
synchronization defect whenever (16) is violated.

More generally, if `0<=A_L<ell`, Corollary 3.4 of the common-coordinate
note gives a closed rational cap on `H` and hence on `E_0`.  Therefore a
global obstruction violating that cap must cross the exact integer
gate

\[
 \boxed{A_L\ge\ell.}
\tag{17}
\]

## 3. Proof of the composition

Equation (2) is Corollary 2.2 of
`OUTER_A_LOW_DEGREE_RESIDUE_THEOREM.md`.  Colourwise cancellation in
`../erdos1083/ERDOS809_OUTER_LOW_MIXED_HIGH_IDENTITY.md` gives (2a), and (4a)
is (4) combined with (2a).  Equations (3a)--(3b) follow from
`OUTER_A_INTERNAL_LOW_DENSE_EXIT.md`.  Equations (3)--(4) are rearrangements of
the exact good-edge budget and `D_A=R_A+D_B`.  The reserve alternatives
are exhaustive, and the implication `|mathcal Q|>=D_B => D_B<=M_B`
is the inherited global reserve theorem.

Under (5), `GLOBAL_RESERVE_UNION_REDUCTION.md`, Theorem 2.1 and
Corollary 2.2, give \(E_0\ge1\) and \(D_B\ge2\).  The inherited global
weighted trichotomy therefore applies; its matching bounds are (5b) and
its same-neighbourhood output is (5c).  The colourwise zero-star mass
ledger in `../erdos1083/ERDOS809_ZERO_STAR_DEFECT_MASS_LEDGER.md`
gives \(H\le D_B\); repeated-pair multiplicity gives
\(H\ge2\ell\), and \(E_0/(4f)\le H-\ell\) gives (5b').  In the
opposite case, (7), (14),
and (15) are the common-host theorem; (8)--(9) are the
inherited exact and coarse reserve--residual energy inequalities.
Applying
\(\min\{\ell-1,\rho_c-2\}=\rho_c-2-(\rho_c-\ell-1)_+\)
inside (8), followed by \(|\mathcal Q|\le D_B-1\) and \(H=D_B-Z\),
gives (9a).  In the maximum-witness branch, both \(b\) and the maximum
witness \(v\), as well as \(L\setminus U\), lie in \(R\).  This gives
\(r\ge t+2\) in (7) and then (9b); see
`OPPOSITE_STAR_DEFECT_SLACK_ENERGY.md`.  Likewise
\(\rho_c\ge3\), so \(R_L\ge3\ell\) in (9a) gives (9c).
Counting the disjoint missing-pair families \(N(b)\times N(c)\) and
the pairs incident with \(b,c\) gives (9d).  Counting
\(N(b)\times(U\cup T)\), all missing pairs incident with \(b\), and
the \(\ell\) missing pairs from \(v\) to \(L\) gives (9e).
The vertices in
\(R\setminus(\{b\}\cup T)\) are also anticomplete to \(L\); after
those pairs are counted, their maximum-degree deficits give (9f), with
internal pairs charged at most twice.  Maximal degree and the exact value
\(e(G)=\lfloor n^2/4\rfloor+1\) first bound \(\kappa\).  Concavity in
\(p=d(b)\), followed by exact parity subtraction in (9f), gives
(9g)--(9h).  See
`MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md`.  Equation (10) is the new
synchronization--reserve bridge.  Leaf-colour supports are independent
in `G[L]`, while every independent leaf pair is an actual reserve
edge.  Thus `alpha(G[L])<=a_B`, and colour-support compression gives
`d_A(b)>=x_0`.  Exact three-budget conservation shows that the part of
the synchronization defect not paid by the actual \(B\)-reserve
creates at least \(\eta_B\) missing leaf incidences in \(U\cap A\).
Consequently the whole union host \(U\cap A\), which is anticomplete
to \(N_A(b)\), has size at least \(y_0\).  This proves (12).  The
rectangle-to-budget theorem gives

\[
 M_B\ge x(y-g)_+ +y(x-g)_+-M_A+L_m.
\]

Its first two terms are nondecreasing in `x,y`, so substitution of
`x_0,y_0` proves (13).  Finally,
\(M_A\ge H(H+\eta_B)/(a_*\ell)\), and the inherited concentration
inequality \(E_0/(4f)\le H-\ell\) proves (13a).  This proves the repaired
three-branch normal form.  QED.

## 4. Scope firewall

The normal form is not a proof that its hard feasibility region is
empty.  It records necessary conditions for a genuine hard counterexample;
failure of the good-edge closure condition alone is not asserted to be
equivalent to failure of the public total-colour target.  The union
rectangle and three-budget conservation remove the former large-\(A_L\)
loss in B-opposite, but
linear degree spread `g`, quadratic outside-rectangle energy in `M_A`,
and high-rank low-degree colour structure can still survive.  The
same-star alternative is bounded but not eliminated in every parameter
range, and other BCM witness branches remain.  Maximum-degree Case 1
and Erdős #809 are open.
