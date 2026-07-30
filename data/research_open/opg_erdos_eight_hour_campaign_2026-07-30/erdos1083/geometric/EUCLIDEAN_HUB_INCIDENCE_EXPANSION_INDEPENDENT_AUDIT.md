# Independent red-team audit: Euclidean hub incidence expansion

Date: 2026-07-30

Audited file:
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

The reverse-circle parametrization is injective on every retained
nonperpendicular plane, the degenerate-circle handling is harmless,
the retained directed codegree and cell cap pass consistently to the
unordered graph used by the matching-or-hub theorem, and the planar
point--circle incidence bound is applied within its valid scope.
All four exponent substitutions are correct.  They exclude the hub
branch for every fixed \(\kappa<1/5\) and give the stated
\(t^{1/5-\varepsilon-o(1)}\) rich matching.

## 1. Reverse-circle coordinate audit

Fix the source plane \(\Pi_\alpha\), a target plane \(\Pi_\beta\),
and put \(c=\cos(\alpha-\beta)\).  For
\[
p=(u,z),\qquad q=(v,w),
\]
the distance equation is
\[
u^2+z^2-2cv\,u-2wz+v^2+w^2-d=0.
\tag{A}
\]
The normalized coefficient triple after \(u^2+z^2\) is
\[
(-2cv,-2w,v^2+w^2-d).
\tag{B}
\]
If \(c\ne0\), equality of two triples first gives \(v=v'\) and
\(w=w'\), and then \(d=d'\).  Thus
\[
(q,d)\longmapsto\Gamma_{\beta,q,d}
\]
is injective for each fixed retained \(\beta\).  No injectivity
between different target planes is needed, because the incidence
theorem is applied separately for each \(\beta\).

Completing squares in (A) gives centre and squared radius
\[
(cv,w),\qquad r^2=d-(1-c^2)v^2.
\tag{C}
\]
When \(r^2<0\), the equation has no real source point.  When
\(r^2=0\), its real locus is the single centre and hence contributes
at most one incidence.  There are at most \(QL\) parameter pairs
\((q,d)\) for a fixed \(\beta\), so every zero-radius contribution is
absorbed by the \(+QL\) term.  Discarding the imaginary members and
separately charging the zero members leaves a set of distinct
positive-radius real circles.

At \(c=0\), opposite radial coordinates \(v,-v\) with the same
\((w,d)\) give the same normalized equation.  More collisions can
occur through equality of \(v^2-d\).  This verifies that deletion of
the perpendicular target plane is necessary for the asserted
parameter injectivity.

## 2. Compatibility with the inherited codegree and cell cap

`ANGULAR_STARVATION_BRANCH_ATTACK.md` defines its incidence tensor on
ordered plane pairs after deleting equal and perpendicular pairs.
There are \(M^2\) ordered pairs in total.  Only \(M\) are equal, and
each plane modulo \(\pi\) has at most one perpendicular partner, so
only \(O(M)\) directed pairs are deleted.  Its audited calculation
therefore gives, on precisely this retained graph,
\[
\mathfrak E_{\rm all}\ge t^{13-o(1)},\qquad
\mathfrak E_{\rm diag}\le t^{12+o(1)}.
\tag{D}
\]

For a retained unordered pair \(e=\{\alpha,\beta\}\), define
\[
W_{e,d}=R_{\alpha,\beta}(d).
\tag{E}
\]
This is orientation-independent because reversing an ordered point
pair is a bijection:
\[
R_{\alpha,\beta}(d)=R_{\beta,\alpha}(d).
\]
If \(E_{\rm all}^{\rm un}\) and \(E_{\rm diag}^{\rm un}\) denote the
corresponding unordered energies, exact double counting gives
\[
E_{\rm all}^{\rm dir}=4E_{\rm all}^{\rm un},\qquad
E_{\rm diag}^{\rm dir}=2E_{\rm diag}^{\rm un}.
\tag{F}
\]
Consequently (D) implies
\[
\mathfrak C_{\rm plane}^{\rm un}
=E_{\rm all}^{\rm un}-E_{\rm diag}^{\rm un}
\ge t^{13-o(1)}.
\tag{G}
\]
Thus passage from ordered to unordered plane pairs loses only
absolute factors and a lower-order diagonal term.

The same retained nonperpendicular cell satisfies the previously
proved two-degrees-of-freedom bound
\[
W_{e,d}=R_{\alpha,\beta}(d)
\ll Q^{4/3}+Q=t^{4+o(1)}.
\tag{H}
\]
This is exactly the cell cap assumed by
`HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md`.  Deletion cannot increase
any cell, and the codegree lower bound (G) was proved after deletion.
Hence neither hypothesis is silently inherited from an exceptional
perpendicular cell.

In the hub alternative, the rich weighted degree is a subsum of
\[
\sum_{\substack{\beta\ne\alpha\\c_{\alpha,\beta}\ne0}}
R_{\alpha,\beta}(d).
\]
Therefore the hub mass assumption used in the incidence theorem is
the correct consequence of the matching-or-hub alternative; no
ordered/unordered factor affects an exponent.

## 3. Applicability of the planar incidence theorem

The cited Sharir--Sheffer--Zahl paper records in its equation (1) the
classical planar arbitrary-circle estimate
\[
I(m,n)=O\!\left(
m^{2/3}n^{2/3}
+m^{6/11}n^{9/11}\log^{2/11}(m^3/n)
+m+n
\right),
\tag{I}
\]
attributing its precise logarithmic form to the earlier planar
literature.  Its hypotheses here are met:

- \(P_\alpha\) is a finite set of at most \(Q\) real planar points;
- after the preceding treatment, \(\mathcal C_\beta\) is a finite set
  of at most \(QL\) distinct positive-radius real circles; and
- the theorem imposes no equal-radius, generic-position, or
  two-degrees-of-freedom assumption beyond being a set of circles.

In the present range
\[
\frac{m^3}{n}=\frac{Q^3}{QL}
=t^{4+2\kappa+o(1)}>1,
\]
so replacing the logarithm by
\(\log(2+m^3/n)\) is harmless and it contributes only \(t^{o(1)}\).
The citation is therefore substantively correct, although SSZ is a
secondary source for this planar theorem rather than its original
proof.

Post-audit source note: Janzer--Janzer--Methuku--Tardos,
*Tight bounds for intersection-reverse sequences, edge-ordered
graphs, and applications* (JLMS 2025), removes the logarithm from the
underlying pseudo-circle cutting bound.  This only strengthens (I);
the \(6/11,9/11\) powers and every audited exponent comparison remain
unchanged.

For each fixed \(\beta\), use \(m=Q\) and \(n=QL\), then sum over at
most \(M\) target planes.  This gives exactly
\[
LH\ll M\left\{
Q^{2/3}(QL)^{2/3}
+Q^{6/11}(QL)^{9/11}t^{o(1)}
+Q+QL
\right\}.
\tag{J}
\]

## 4. Cross-plane repeated-circle refinement

The second part of the theorem correctly changes the order of
operations.  Start with all triples \((\beta,q,d)\), then:

1. discard every empty or imaginary reverse circle;
2. charge every incidence-active zero-radius triple directly; and
3. merge equal positive-radius active circles.

The first step makes the structural multiplicity incidence-active:
an empty normalized equation cannot inflate \(\mu\).  The second step
costs at most \(MQL\), since a zero-radius triple has at most one
incidence.  After the third step, write \(w_C\le\mu\) for the merged
circle weights and
\[
\mathsf T=\sum_Cw_C\le MQL.
\]
In the dyadic layer \(u\le w_C<2u\), the number of distinct circles
is at most \(\mathsf T/u\).  Multiplying the planar point--circle
bound for that layer by \(2u\) gives
\[
\begin{aligned}
O\bigl(&
Q^{2/3}\mathsf T^{2/3}u^{1/3}
+Q^{6/11}\mathsf T^{9/11}u^{2/11}t^{o(1)}\\
&+Qu+\mathsf T
\bigr).
\end{aligned}
\]
Summing the geometric dyadic powers through \(u\le\mu\), and
absorbing the logarithmic repetition of the last term, gives the
revised bound (22):
\[
Q^{2/3}\mathsf T^{2/3}\mu^{1/3}
+Q^{6/11}\mathsf T^{9/11}\mu^{2/11}t^{o(1)}
+Q\mu+\mathsf Tt^{o(1)}.
\]

This incidence-active restriction is essential to the structural
interpretation: without it, the maximum repeated normalized equation
could consist entirely of empty circles.  The theorem's revised
definition explicitly performs the deletion before defining \(\mu\),
so this risk is closed.

Write \(\mu=t^{m+o(1)}\).  The exact exponent ledger for the weighted
dyadic union is
\[
\begin{array}{c|c}
\text{term}&t\text{-exponent}\\ \hline
Q^{2/3}\mathsf T^{2/3}\mu^{1/3}
&6-4\kappa/3+m/3\\
Q^{6/11}\mathsf T^{9/11}\mu^{2/11}
&72/11-18\kappa/11+2m/11\\
Q\mu&3+m\\
\mathsf T&6-2\kappa.
\end{array}
\tag{M}
\]
Comparing the first three terms with
\(LH=t^{7-3\kappa-o(1)}\) respectively requires
\[
m\ge3-5\kappa,\qquad
m\ge\frac{5-15\kappa}{2},\qquad
m\ge4-3\kappa.
\tag{N}
\]
The middle threshold is strictly smallest for \(\kappa>0\), while
the last term misses the hub exponent by \(1-\kappa\).  Hence
\[
\mu\ge t^{(5-15\kappa)/2-o(1)}.
\]
The exponent is positive exactly for \(\kappa<1/3\), as claimed.

Equality of two normalized equations across target planes is
equivalent to
\[
c_{\alpha,\beta}v=c_{\alpha,\beta'}v'=A,\qquad
w=w'=w_0,\qquad
v^2-d=v'^2-d'=C.
\tag{O}
\]
Within one fixed nonperpendicular \(\beta\), Lemma 1 permits at most
one triple in a repeated-circle class.  Hence a class of multiplicity
\(\mu\) uses \(\mu\) distinct target planes and yields exactly the
claimed common-height cosine--radial chart.  Because the common
circle is incidence-active, the class also has an actual witness in
\(P_\alpha\), not just matching formal coefficients.

## 5. Independent exponent audit

Write an exponent as \(a+b\kappa\).  The substitutions
\[
M=t,\qquad Q=t^3,\qquad L=t^{2-2\kappa}
\]
give the following exact ledger:
\[
\begin{array}{c|c}
\text{quantity}&t\text{-exponent}\\ \hline
LH&7-3\kappa\\
M Q^{2/3}(QL)^{2/3}&19/3-4\kappa/3\\
M Q^{6/11}(QL)^{9/11}&74/11-18\kappa/11\\
MQ&4\\
MQL&6-2\kappa.
\end{array}
\tag{K}
\]
On \(0<\kappa<1\), the \(6/11,9/11\) term is the largest upper
term.  Its differences from the \(2/3\), point, and circle terms are
\[
\frac{13-10\kappa}{33},\qquad
\frac{30-18\kappa}{11},\qquad
\frac{8+4\kappa}{11},
\]
all strictly positive.

The lower exponent minus the four upper exponents is respectively
\[
\frac{2-5\kappa}{3},\qquad
\frac{3-15\kappa}{11},\qquad
3-3\kappa,\qquad
1-\kappa.
\tag{L}
\]
The second is the smallest throughout \(0<\kappa<1\), and it is
positive exactly when \(\kappa<1/5\).  For each fixed such
\(\kappa\), its positive constant gap absorbs all \(t^{o(1)}\)
losses.  Equality \(\kappa=1/5\) is correctly not claimed.

Finally, for fixed \(0<\varepsilon<1/5\), choose
\[
\kappa=\frac15-\varepsilon.
\]
The hub branch is impossible, so the parameterized dichotomy forces
at least \(t^{1-o(1)}\) labels with a matching of size
\[
t^{\kappa-o(1)}
=t^{1/5-\varepsilon-o(1)}.
\]
Every matching edge retains the rich-cell lower bound
\(t^{3-o(1)}\).  For \(\varepsilon\ge1/5\), the statement follows
from any fixed \(0<\kappa<1/5\) and is weaker.  Thus the advertised
“every fixed \(\varepsilon>0\)” formulation is valid.

## 6. Exact certificate

`independent_verify_euclidean_hub_incidence.py` independently checks:

- finite injectivity samples for four nonzero rational cosines and a
  perpendicular collision;
- the completed-square radius identity and real/zero/imaginary
  classification;
- exact directed/unordered energy conversion;
- all four affine incidence exponents and all four lower--upper
  gaps;
- dominance of the \(6/11,9/11\) term and the \(1/5\) endpoint; and
- the \(\kappa=1/5-\varepsilon\) matching substitution;
- the once-merged weighted-union exponents and \(1/3\) threshold; and
- an exact cross-plane repeated-circle example.

It is an exact algebra certificate, not a replacement for the
external planar incidence theorem.

Reproduction:

```bash
python3 independent_verify_euclidean_hub_incidence.py
pytest -q test_independent_verify_euclidean_hub_incidence.py
```
