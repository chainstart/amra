# Global hyperbola networks: the optimal abstract reuse bound

Date: 2026-07-30

## Purpose

The local \(C_4\), edge-character and single-pair BSG routes have now been
exhausted.  This note studies the remaining global interface: many shifted
squared-difference blocks, joined when they have a strong intersection.

There is one rigorous positive conclusion.  At the line-count threshold,
the total correlation forces one common parameter value to be reused by
\[
 L^{1/3-\eta-o(1)}
\]
blocks.  More generally, a weighted strong-edge network forces a
common-value clique of the exact size predicted by its total overlap mass.

This conclusion is optimal for abstract block systems.  An affine-line
tensor construction simultaneously saturates:

- total block incidence \(L^3\);
- union size \(L^{8/3+\eta}\);
- correlation mass \(L^{10/3-\eta}\);
- strong overlap \(L^{5/6-\eta}\);
- strong-graph degree \(L^{1/2}\); and
- maximum common-value multiplicity \(L^{1/3-\eta}\).

The construction is genuinely realizable by squared differences inside
each separate product fibre, because the radius pairs in one fibre form a
matching.  It need not be realizable simultaneously over all product
fibres: it assigns independent height data to different occurrences of the
same original radius class.  This identifies the exact missing geometric
input as **cross-fibre shared-endpoint compatibility**.

No exponent improvement is claimed.

## 1. Exact global network model

Work in the balanced regime
\[
 m\asymp L,\qquad F=Lm\asymp L^2.
\]
For each unordered radius pair \(e=(u,v)\), let
\[
 p(e)=u+v,\qquad C_e=T^2(q^u-q^v)^2,
\]
and truncate
\[
 S_e=C_e+\widetilde Y_e,\qquad
 \widetilde Y_e\subseteq(Z_u-Z_v)^2,\qquad |S_e|=k\asymp L. \tag{1}
\]
The block vertices split into \(\Theta(L)\) product fibres
\[
 {\cal B}_p=\{e:p(e)=p\},
\]
each having \(\Theta(L)\) vertices.  There are
\(B=\Theta(L^2)\) blocks and total incidence
\[
 I=\sum_e|S_e|=\Theta(L^3). \tag{2}
\]

For \(e,f\in{\cal B}_p\), put
\[
 w(e,f)=|S_e\cap S_f|.
\]
Every common value \(t\) and represented signed differences
\[
 x=a-b,\qquad y=c-d
\]
give
\[
 (x-y)(x+y)=\Delta_{ef},\qquad
 \Delta_{ef}=C_f-C_e. \tag{3}
\]
The constants have the vertex-potential identity
\[
 \Delta_{ef}+\Delta_{fg}=\Delta_{eg}. \tag{4}
\]
Equation (4) alone does not make pairwise witnesses consistent: the
intersection \(S_e\cap S_f\) and \(S_f\cap S_g\) may use disjoint values.

Let
\[
 h_p(t)=|\{e\in{\cal B}_p:t\in S_e\}|.
\]
Then
\[
 M=\sum_p|\{t:h_p(t)>0\}|, \tag{5}
\]
and the unordered total correlation is
\[
 W=\sum_{p,t}\binom{h_p(t)}2
   =\sum_p\sum_{\{e,f\}\subseteq{\cal B}_p}w(e,f). \tag{6}
\]
If
\[
 M\leq L^{8/3+\eta}, \tag{7}
\]
Cauchy--Schwarz gives, up to lower-order terms,
\[
 W\gtrsim I^2/M\gtrsim L^{10/3-\eta}. \tag{8}
\]

## 2. A provable global reuse lemma

### Theorem 1 (weighted overlap forces a common-value clique)

Let \({\cal G}\) be any graph whose vertices are blocks inside the product
fibres, and put
\[
 W_{\cal G}=\sum_{ef\in E({\cal G})}w(e,f).
\]
Then some parameter value belongs to at least
\[
 1+\frac{2W_{\cal G}}{I} \tag{9}
\]
blocks in one product fibre.

In particular, if a dyadic strong-edge scale satisfies
\[
 w(e,f)\geq r,\qquad
 r|E({\cal G})|
 \gtrsim L^{10/3-\eta-o(1)}, \tag{10}
\]
then one value is common to
\[
 L^{1/3-\eta-o(1)} \tag{11}
\]
blocks.

### Proof

For an incidence \(t\in S_e\), let
\[
 d_{\cal G}(e,t)
 =|\{f:ef\in E({\cal G}),\ t\in S_f\}|.
\]
Double-counting edge--common-value pairs gives
\[
 \sum_e\sum_{t\in S_e}d_{\cal G}(e,t)=2W_{\cal G}. \tag{12}
\]
There are \(I\) block--value incidences, so one pair \((e,t)\) has
\[
 d_{\cal G}(e,t)\geq2W_{\cal G}/I.
\]
The block \(e\) and all these neighbours lie in the same product fibre and
contain \(t\), proving (9).  Equations (2) and (10) give (11). \(\square\)

Theorem 1 is stronger than merely finding many strong edges: its blocks
share one actual parameter value, so all their hyperbolic relations use the
same \(t\).

## 3. Why this is still below the target propagation scale

The strong single-pair audit shows that a conclusion confined to four
height sets has local parameter capacity \(O(L^2)\), whereas the desired
global target is \(L^{8/3+\eta}\).  A propagation factor
\[
 L^{2/3+\eta} \tag{13}
\]
is needed.

The common-value family supplied by Theorem 1 has only
\[
 H=L^{1/3-\eta-o(1)}. \tag{14}
\]
Even if every one of these blocks contributed independently, it misses
(13) by
\[
 L^{1/3+2\eta+o(1)}. \tag{15}
\]

This is not a weakness of the averaging proof.  If (9) were to force
multiplicity \(L^{2/3+\eta}\), the required overlap would be
\[
 W_{\cal G}\gtrsim I L^{2/3+\eta}
 =L^{11/3+\eta}, \tag{16}
\]
while (8) supplies only \(L^{10/3-\eta}\).  The exact correlation-mass
shortfall is the factor in (15).

## 4. An affine-line tensor saturation model

Choose an integer \(d\geq3\), a prime power \(q\), and put
\[
 L=q^d,\qquad \eta=\frac13-\frac1d. \tag{17}
\]
If needed take \(q\) to be a square so the half-powers below are integral.
Define
\[
 h=q=L^{1/3-\eta},\quad
 g=q^{d/2-1}=L^{1/6+\eta},\quad
 r=q^{d/2+1}=L^{5/6-\eta}. \tag{18}
\]
Then
\[
 gr=L,\qquad gh=L^{1/2}. \tag{19}
\]

In each product fibre, identify its abstract \(L\) block vertices with
\(\mathbb F_q^d\).  Select \(g\) distinct line directions.  For every affine
line \(\ell\) in a selected direction, create a disjoint core \(X_\ell\) of
\(r\) symbols.  Give a block vertex \(v\) the set
\[
 S_v=\bigcup_{\ell\ni v}X_\ell. \tag{20}
\]
Each vertex lies on one line in every selected direction, so
\[
 |S_v|=gr=L. \tag{21}
\]
Two vertices overlap in \(r\) symbols exactly when their joining line has a
selected direction.  Every symbol lies in the \(h=q\) vertices of one line.

Repeat with disjoint symbol universes in \(L\) product fibres.  The exponent
ledger is
\[
\begin{array}{c|c}
\text{quantity}&\text{order}\\ \hline
\text{blocks}&L^2\\
\text{block size}&L\\
I&L^3\\
\text{strong degree}&L^{1/2+o(1)}\\
\text{strong edges}&L^{5/2+o(1)}\\
\text{edge overlap}&L^{5/6-\eta}\\
\max h_p(t)&L^{1/3-\eta}\\
M&L^{8/3+\eta}\\
W&L^{10/3-\eta}.
\end{array} \tag{22}
\]
Thus Cauchy--Schwarz, the strong network, Theorem 1 and the target union
size are all sharp together.

### Squared-difference realizability within one fibre

One product fibre is a matching on the original radius indices: distinct
block vertices use disjoint height-set pairs.  Choose numerical symbols
larger than every \(C_e\).  For each block independently, one endpoint
contains
\[
 \{\sqrt{s-C_e}:s\in S_e\},
\]
and the other contains zero; pad both sets as needed.  Hence the truncated
block contains the prescribed \(S_e\).  This realizes the affine-line tensor
inside one genuine product fibre.

The simultaneous \(L\)-fibre tensor is not asserted to be geometrically
realizable.  A radius class \(Z_u\) participates in one block in each of
\(\Theta(L)\) product fibres.  Construction (20) assigns an independent
height set to every occurrence, while the geometry requires all occurrences
to use the same \(Z_u\).  This is the compatibility omitted by the model.

## 5. Why standard incidence and sum-product theorems do not yet apply

The available relation has three degeneracies.

1. **Elekes--Szabó mismatch.**  The equation
   \(t-C_e-(a-b)^2=0\) has four variables, block-dependent sets, and the
   explicitly separable form \(t=C_e+\phi(a-b)\).  It is a group-like
   exceptional form, not a nondegenerate three-variable Cartesian surface.
2. **Point--line mismatch.**  Replacing \(y=(a-b)^2\) gives only
   \(t=C_e+y\), a family of parallel additive incidences.  A
   Szemerédi--Trotter or Stevens--de Zeeuw estimate sees no transverse line
   family and is saturated by the tensor model.
3. **Sum--product mismatch.**  Equation (3) uses two linear factors, but the
   factor sets can vary independently with every block edge.  No single set
   has been shown to carry both high additive and high multiplicative
   energy.  Inside one product fibre, matching makes this independence
   genuinely realizable.

These theorems cannot improve (11) without first using shared endpoint sets
across different product fibres.

## 6. A precise conditional route

The following statement would be sufficient but is **not proved**.

> **Conditional cross-fibre compatibility lemma.**  Under (1), (7) and
> (8), requiring all blocks incident to radius \(u\) to use the same
> \(m\)-point set \(Z_u\) forces either
> \(M\gg L^{8/3+\eta+\epsilon_0}\), or a family of at least
> \(L^{2/3+\eta-o(1)}\) radius-pair blocks whose common-value witnesses are
> generated by one shared additive or multiplicative coordinate system.

The first alternative is the desired gain.  The second supplies exactly the
propagation factor (13), after which an incidence or sum-product theorem
might become applicable.

The affine-line tensor proves that many strong hyperbola edges, large
common-value multiplicity and the potential identity (4) are insufficient
substitutes.  A proof must compare the multiple appearances of each
original \(Z_u\) across product fibres.

## 7. Verification

`verify_global_hyperbola_network_audit.py` constructs a finite affine-line
tensor over \(\mathbb F_2^4\), verifies every count in (22), tests the
weighted reuse inequality and checks the symbolic exponent identities.
