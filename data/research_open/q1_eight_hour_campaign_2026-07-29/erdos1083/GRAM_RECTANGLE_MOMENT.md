# Gram rectangle moment

Date: 2026-07-30

## Purpose

`ANCHOR_COHERENCE_EXTRACTION_AUDIT.md` shows that value-level overlap and
triangle marginals cannot force a common hub anchor.  The first identity
that retains actual point coordinates is the Gram rectangle.  This note
builds the corresponding cross-service moment.

There is one unconditional gain.  If \({\cal S}\) is a chosen set of
point-represented services with
\[
 |{\cal S}|=S\gtrsim L^{10/3-\eta-o(1)}
\]
and the global parameter-line union has size
\[
 M\leq L^{8/3+\eta},
\]
then the two cross edges of the services have collision energy
\[
 {\cal R}_{\rm cell}
\gtrsim \frac{S^2}{M}
\gtrsim L^{4-3\eta-o(1)}. \tag{1}
\]
Its average degree per service is
\[
 L^{2/3-2\eta-o(1)}, \tag{2}
\]
which exceeds the required \(L^{1/3+2\eta}\) whenever
\(\eta<1/12\).

The collision in (1) remembers a product fibre and a distance value, but
not the actual point pair representing that value.  Let \(V\) be the
largest number of actual point-pair representations of a cross cell visited
by the services.  The genuine point-conditioned rectangle moment satisfies
\[
 {\cal R}_{\rm pt}
\gtrsim \frac{S^2}{MV}. \tag{3}
\]
Consequently the desired
\[
 {\cal R}_{\rm pt}\gtrsim L^{11/3+\eta-o(1)} \tag{4}
\]
holds under the explicit real-Euclidean nondegeneracy hypothesis
\[
 V\leq L^{1/3-4\eta+o(1)}. \tag{5}
\]

This is a rigorous conditional subcase, not an unconditional exponent
improvement.  An exact real vertical-translation fan shows why (5) cannot
be deleted: arbitrarily many services can share both cross distance cells
while using distinct actual cross point pairs.  Every Gram identity holds,
but cell energy is quadratic and point-conditioned energy only linear.

## 1. Point-pair states and services

Represent one axial point by
\[
 P=(\rho_u,a),\qquad N=(\rho_v,z)
\]
and put
\[
 Q(P,N)=\|P-N\|^2
 =(\rho_u-\rho_v)^2+(a-z)^2. \tag{6}
\]
A point-represented service is a quadruple
\[
 \sigma=(P,N;P',N')
\]
where
\[
\begin{aligned}
 P&=(\rho_u,a),&N&=(\rho_v,z),\\
 P'&=(\rho_x,c),&N'&=(\rho_y,d),
\end{aligned}
\]
such that
\[
 u+v=x+y,\qquad Q(P,N)=Q(P',N')=:t_\sigma. \tag{7}
\]
Every selected block-value overlap admits such a service after choosing one
point-pair representation in each of its two blocks.  Thus the ordered
overlap mass supplies \(S\) services, up to harmless orientation constants.

The four points obey
\[
\begin{aligned}
 &Q(P,N)+Q(P',N')-Q(P,N')-Q(P',N)\\
 &\qquad=2(P-P')\cdot(N'-N). \tag{8}
\end{aligned}
\]
Equivalently,
\[
 2t_\sigma-Q(P,N')-Q(P',N)
 =2(P-P')\cdot(N'-N). \tag{9}
\]
The two terms
\[
 Q(P,N'),\qquad Q(P',N) \tag{10}
\]
are the cross values of the service.

## 2. Cross cells live in the same global union

For a radius pair \(ij\), define its cell by
\[
 (i+j,Q((\rho_i,s),(\rho_j,t))). \tag{11}
\]
The first coordinate is the geometric-product fibre and the second is the
shifted squared-difference value.  Hence every cross value in (10) belongs
to the same global cell universe counted by \(M\).

The two cross cells of \(\sigma\) are
\[
\begin{aligned}
 \xi_-(\sigma)&=(u+y,Q(P,N')),\\
 \xi_+(\sigma)&=(x+v,Q(P',N)). \tag{12}
\end{aligned}
\]
Notice that \(u+y\) and \(x+v\) are generally different.  The cross edges
do not themselves form another same-product service; their role is to
propagate the original service into two other product fibres.

For a cell \(\xi\), let
\[
 r(\xi)=|\{(\sigma,\epsilon):
   \sigma\in{\cal S},\ \epsilon\in\{-,+\},
   \ \xi_\epsilon(\sigma)=\xi\}|. \tag{13}
\]
Then
\[
 \sum_\xi r(\xi)=2S,\qquad
 |\{\xi:r(\xi)>0\}|\leq M. \tag{14}
\]

## 3. Unconditional cell energy

Define
\[
 {\cal R}_{\rm cell}=\sum_\xi r(\xi)^2. \tag{15}
\]
Cauchy--Schwarz and (14) give
\[
 {\cal R}_{\rm cell}
\geq\frac{(2S)^2}{M}. \tag{16}
\]
Removing the \(2S\) diagonal terms changes no exponent because
\[
 S/M=L^{2/3-2\eta-o(1)}\to\infty
\]
in the relevant range.

Substituting the known exponents gives
\[
 \frac{S^2}{M}
\gtrsim
 L^{2(10/3-\eta)-(8/3+\eta)}
=L^{4-3\eta}. \tag{17}
\]
The target point-conditioned moment is
\[
 L^{11/3+\eta}. \tag{18}
\]
Thus the cell energy has a surplus
\[
 L^{1/3-4\eta}, \tag{19}
\]
positive exactly when \(\eta<1/12\).  For the campaign benchmark
\(\eta=1/30\), the exponents are
\[
 {\cal R}_{\rm cell}:L^{39/10},\qquad
 {\cal R}_{\rm target}:L^{37/10},
\]
leaving \(L^{1/5}\).

Equation (16) is a new unconditional cross-fibre energy statement.  It does
not yet retain a common point representation.

## 4. Point-conditioned rectangle energy

For a cell \(\xi=(p,s)\), let \(\Pi_\xi\) be the set of actual ordered point
pairs \(\pi=(A,B)\) occurring on radius pairs of product exponent \(p\)
with
\[
 Q(A,B)=s.
\]
Restrict to point pairs that occur as a cross edge of a service, and put
\[
 \nu(\xi)=|\Pi_\xi|,\qquad
 V=\max_{\xi:r(\xi)>0}\nu(\xi). \tag{20}
\]

Let \(r(\xi,\pi)\) count service-cross occurrences using the actual pair
\(\pi\).  Define
\[
 {\cal R}_{\rm pt}
=\sum_\xi\sum_{\pi\in\Pi_\xi}r(\xi,\pi)^2. \tag{21}
\]
Two off-diagonal occurrences counted by one term of (21) share the same
cross point pair.  Each occurrence, together with its two diagonal points,
is a Gram rectangle of the form (8).  Thus (21) is genuinely
point-conditioned.

The centred count of distinct pairs is
\(\sum_{\xi,\pi}r(\xi,\pi)(r(\xi,\pi)-1)
={\cal R}_{\rm pt}-2S\).  Whenever (4) holds this subtraction is
lower-order, since \(11/3+\eta>10/3-\eta\).

For every \(\xi\), Cauchy gives
\[
 \sum_{\pi\in\Pi_\xi}r(\xi,\pi)^2
\geq\frac{r(\xi)^2}{\nu(\xi)}.
\]
Summing and using (16),
\[
 {\cal R}_{\rm pt}
\geq\frac{{\cal R}_{\rm cell}}V
\geq\frac{4S^2}{MV}. \tag{22}
\]
This proves (3).

### Theorem 1 (cross-Sidon conditional rectangle moment)

If the visited cross cells satisfy (5), then (4) holds.  Equivalently, the
point-conditioned average rectangle degree is at least
\[
 \frac{{\cal R}_{\rm pt}}S
\gtrsim L^{1/3+2\eta-o(1)}. \tag{23}
\]

### Proof

Insert
\[
 S=L^{10/3-\eta-o(1)},\quad
 M\leq L^{8/3+\eta},\quad
 V\leq L^{1/3-4\eta+o(1)}
\]
into (22):
\[
\begin{aligned}
 {\cal R}_{\rm pt}
 &\gtrsim
 L^{2(10/3-\eta)-(8/3+\eta)-(1/3-4\eta)-o(1)}\\
 &=L^{11/3+\eta-o(1)}.
\end{aligned}
\]
Division by \(S\) gives (23). \(\square\)

Hypothesis (5) is intrinsic and checkable on a real point set.  A sufficient
version is:

1. every cross shifted value has \(O(1)\) point-pair representations inside
   each radius block; and
2. every cross cell visited by the services belongs to at most
   \(L^{1/3-4\eta+o(1)}\) radius blocks.

This is a cross-Sidon/no-superrich-cell subcase.  The theorem proves the
full required moment under that nondegeneracy assumption.

## 5. The unconditional representation cap is too weak

One fixed squared distance has at most \(2m\) ordered representations in
one block: after choosing the first height, the second is determined up to
two signs.  One product fibre contains \(O(L)\) blocks.  Therefore
\[
 V\leq2Lm=O(L^2). \tag{24}
\]
Using only (24), equation (22) gives
\[
 {\cal R}_{\rm pt}\gtrsim L^{2-3\eta-o(1)}, \tag{25}
\]
far below (18).  The exact remaining loss is representation multiplicity,
not the number of value cells.

## 6. A real vertical-translation fan

The loss in (24) is not an artefact.  Fix four distinct geometric radius
indices
\[
 u+v=x+y.
\]
Choose constants \(D,R,S_0\) satisfying
\[
 C_{uv}+R^2=C_{xy}+S_0^2. \tag{26}
\]
For any distinct translations \(A_j\), put
\[
\begin{aligned}
 P_j&=(\rho_u,A_j),&
 N_j&=(\rho_v,A_j+R),\\
 P'_j&=(\rho_x,A_j+D+S_0),&
 N'_j&=(\rho_y,A_j+D). \tag{27}
\end{aligned}
\]
Then every \(j\) is an exact service:
\[
 Q(P_j,N_j)=C_{uv}+R^2
 =C_{xy}+S_0^2=Q(P'_j,N'_j). \tag{28}
\]
Both cross values are also independent of \(j\):
\[
\begin{aligned}
 Q(P_j,N'_j)&=C_{uy}+D^2,\\
 Q(P'_j,N_j)&=C_{xv}+(D+S_0-R)^2. \tag{29}
\end{aligned}
\]
Thus \(r\) translated services produce two cross cells of multiplicity
\(r\).  Their cell energy is \(2r^2\).

However, all \(2r\) actual cross point pairs are distinct and each has one
completion.  Hence their point-conditioned energy is only \(2r\).  Every
identity (8) holds exactly.  The four shared height sets use only \(r\)
coordinates each, so the construction is a genuine real squared-distance
configuration up to \(r\leq m\).

Condition (26) always has rational solutions.  With
\(\Delta=C_{xy}-C_{uv}\) and nonzero rational \(s\), take
\[
 R=\frac{s+\Delta/s}{2},\qquad
 S_0=\frac{\Delta/s-s}{2};
\]
then \(R^2-S_0^2=\Delta\).

The fan proves that the Gram identity and cell energy alone do not imply a
point-conditioned moment.  A proof beyond Theorem 1 must either control
vertical-translation orbits or show that many such orbits themselves force
distance/parameter-line expansion elsewhere.

## 7. Exact dichotomy left by this round

The argument gives a rigorous alternative:

1. **cross-Sidon branch:** \(V\leq L^{1/3-4\eta+o(1)}\), and the required
   point-conditioned moment (4) holds;
2. **representation-rich branch:** some visited product-fibre distance cell
   contains more than \(L^{1/3-4\eta-o(1)}\) distinct actual point pairs.

The second branch is a concrete geometric structure, not an abstract
anchor label.  The translation fan shows it can occur locally.  What is not
proved is that enough representation-rich cells cannot coexist with the
small global union and all shared height-set constraints.

Theorem 1 may be useful as a publishable nondegenerate subcase, but no claim
of publication readiness is made.  No unconditional improvement of the
\(3/5\) distance exponent follows.

## 8. Verification

`verify_gram_rectangle_moment.py` checks the exponent ledger, Cauchy moment
inequalities, the universal representation cap, and an exact rational
vertical-translation fan with geometric radii.
