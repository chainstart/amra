# Erdős #1083 two-hour proof attack: final report

Date: 2026-07-30

## 1. Executive verdict

The requested Q1-level global breakthrough was **not reached**:
no fixed \(\delta>0\) is proved in
\[
f_3(N)\gg N^{3/5+\delta},
\]
and Erdős #1083 remains open.

The campaign nevertheless produced one genuine unconditional
structural advance.  At the critical normalization \(N=t^5\), it
improves the rich plane-pair matching exponent from the previously
proved \(1/5\), first to \(9/41\), and finally to
\[
\boxed{2/9}.
\]
The improvement from \(9/41\) is small but strict:
\[
\frac29-\frac9{41}=\frac1{369}.
\]
The final theorem was reconstructed independently twice and supported
by exact exponent certificates.

This is the strongest publishable candidate produced in the attack.
It is not yet safe to label it a Q1 paper because it changes a
critical inverse-structure exponent without changing the global
distinct-distance exponent.

## 2. Main theorem proved

Assume the inherited critical cross-plane codegree branch and its
audited matching-or-hub theorem.  Fix a signed centre coordinate
\(A\).  The reverse circles in the source plane have equations
\[
(u-A)^2+(z-w)^2=\rho^2.
\]
Define
\[
\Phi_A(u,z)
=
\left(z,(u-A)^2+z^2\right).
\]
The map has fibres of size at most two, and the circle above becomes
the line
\[
Y=2wZ+(\rho^2-w^2).
\]
Different normalized positive-radius circles give different lines.
Therefore
\[
I(P_\alpha,\mathcal C_A)
\ll
Q^{2/3}N_A^{2/3}+Q+N_A.
\]
If \(R\) signed values of \(A\) occur and
\(N=\sum_A N_A\), summing and using Hölder gives
\[
\boxed{
I(P_\alpha,\mathcal C)
\ll
Q^{2/3}R^{1/3}N^{2/3}+RQ+N.
}
\]

The proof then performs a secondary dyadic decomposition.  With
\[
s=t^{a+o(1)},\quad
u=t^{m+o(1)},\quad
N=t^{b+o(1)},\quad
K=t^{c+o(1)},\quad
R=t^{r+o(1)},
\]
and \(t^{h+o(1)}\) circles on every retained signed parameter-line
fibre, it obtains
\[
\begin{aligned}
b&=c+h,\\
11a+2b&\le18+o(1),\\
a+b+m&\ge7-3\kappa-o(1),\\
b+m&\le6-2\kappa+o(1),\\
c&\le6-4\kappa-3m+o(1),\\
r+h+m&\le4+o(1).
\end{aligned}
\]
The last inequality is genuinely geometric: one signed
\((A,\rho^2)\)-fibre uses \(t^{h+m-o(1)}\) distinct target points in
the plane \(x=A\), and planes belonging to different signed \(A\)'s
are disjoint.

All three terms of the summed incidence estimate are audited
separately.  The \(+N\) branch contradicts \(a>0\); the \(+RQ\)
branch contradicts the full point--circle ledger; the main term
forces
\[
m\le\frac{1+3\kappa}{2}+o(1).
\]
The inherited point--circle term simultaneously forces
\[
m\ge\frac{5-15\kappa}{2}-o(1).
\]
They are incompatible for every fixed \(\kappa<2/9\).  Hence the hub
branch is impossible in that range.

Applying the matching-or-hub extraction at
\(\kappa=2/9-\varepsilon\) proves:

> For every fixed \(\varepsilon>0\), at least \(t^{1-o(1)}\)
> distance labels support a matching of
> \(t^{2/9-\varepsilon-o(1)}\) pairwise disjoint rich axial-plane
> pairs, with \(t^{3-o(1)}\) representations in every matched cell.

In \(N=t^5\) notation, the three scales are respectively
\[
N^{1/5-o(1)},\qquad
N^{2/45-\varepsilon/5-o(1)},\qquad
N^{3/5-o(1)}.
\]

## 3. Why the proof stops exactly at \(2/9\)

At \(\kappa=2/9\), every scalar inequality used by the proof is
simultaneously feasible at
\[
\begin{array}{c|cccccccccc}
 &\ell&p&a&b&m&c&h&r&j&x\\ \hline
\text{exponent}
 &14/9&23/9&7/9&85/18&5/6&
 47/18&19/9&19/18&14/9&53/18 .
\end{array}
\]
This is an exact exponent ledger, not a Euclidean construction.
It proves that another linear combination of the same capacity
inequalities cannot exclude the endpoint.

At this ledger, one fixed signed parameter fibre has
\[
(S,U,H,R,D)
=
t^{(7/9,\,5/6,\,19/9,\,1,\,3)+o(1)},
\]
where \(S\) is source richness, \(U\) is target multiplicity, \(H\)
is the number of centre heights, \(R\) is the global tangent-square
support, and \(D\) is the distance budget.  Cauchy--Schwarz requires
cross-distance collision exponent \(40/9\), whereas all same-height
collisions have exponent at most \(35/9\).  Thus any actual endpoint
configuration must supply a cross-height parabolic-affine energy
surplus of
\[
\boxed{5/9}
\]
in the \(t\)-exponent.

There is a further numerical floor.  The coarse benchmark
\(S^2UH\) has exponent \(9/2\), only \(1/18\) above the required
\(40/9\).  Therefore a bound
\[
\mathcal E_{\rm cross}
\ll t^{-\delta}S^2UH
\]
excludes the exact endpoint only when \(\delta>1/18\), not for an
arbitrary positive \(\delta\).

An exact row-minimality theorem gives
\[
H\le R(R-1)
\]
when every row sumset has the smallest possible size.  At the live
endpoint this misses by \(t^{1/9-o(1)}\).  Hence literal row-by-row
arithmetic-progression saturation is impossible, but a quantitative
stability theorem in the highly unbalanced regime is still missing.

## 4. Other routes completed

### Matching branch barrier

The four-plane equal-distance equation is real-linearly equivalent
to
\[
A\cdot B=0
\]
and has signature \((3,3)\).  Explicit Euclidean families show both
that disjoint plane pairs can share one cosine coefficient and that
even numerically distinct coefficients can retain a common rich
chord structure.  Therefore the matching theorem alone does not
automatically produce extra distances.

### Six-coprime cyclotomic fibre theorem

For every \(m>1\) with \(\gcd(m,6)=1\), signed five-term cyclotomic
rigidity and Kneser's theorem yield selected-label injection across
the specified coaxial fibres and the sharp equal-fibre bound
\[
|\Delta^2(P)|
\ge
\frac{\ell-1}{2\ell}|P|,
\]
where \(\ell\ge5\) is the least prime factor of \(m\).
Divisibility by \(2\) or \(3\) gives explicit failures of universal
injection, so the arithmetic threshold is exact for this mechanism.
The theorem is clean, but no extraction theorem forces this
structured family in an arbitrary critical configuration.

### Cross-height localization

The exact formula
\[
\rho^2+\tau+z^2+2\rho zx
\]
was tested both positively and negatively.  A genuine Euclidean
cancellation model shows that the formula and fibre cardinalities
alone cannot give a power saving.  The useful additional resource is
reuse of one small global tangent-square set over many centre
heights.  Same-height energy is too small; the unresolved object is
the resulting cross-height parabolic-affine energy.

## 5. Audit and reproducibility

The strongest theorem has two independent proof reconstructions:

1. `route_b/COLLINEAR_CENTER_LINEARIZATION_INDEPENDENT_AUDIT.md`;
2. `route_d/TWO_NINTHS_INDEPENDENT_AUDIT.md`.

Both return **PASS** and both reject any claim at the exact endpoint.
The second audit identifies a critical dependency: elimination of
the \(+RQ\) branch requires retaining the full inequality
\(11a+2b\le18\).  The main proof does retain and use it.

The package also contains exact rational, symbolic, finite-geometric,
and cyclotomic quotient-ring verifiers.  They certify arithmetic,
search for finite counterexamples, and guard the exponent ledgers;
the written proofs remain the basis of the all-parameter results.

## 6. Literature and publication assessment

The current Erdős Problems record still lists \(N^{3/5}\) as the
recognized arbitrary-set lower bound in \(\mathbb R^3\).  Targeted
2025--2026 searches found later results for restricted curves and
surfaces, but no general replacement for this exponent.

The parabolic circle-to-line map is elementary and should not itself
be sold as new.  The potentially new contribution is the integration
of that map with the weighted hub ledger, rich parameter-line
decomposition, and target service capacity to obtain the rational
threshold \(2/9\).

The defensible publication ranking is:

1. **Route B \(2/9\):** substantial structural theorem and best paper
   nucleus, but not yet safely Q1 without a global consequence or a
   broader stand-alone stability theorem.
2. **Route C six-coprime theorem:** possible specialized short note
   or supporting section, not currently Q1-scale.
3. **Routes A/D:** useful sharp barriers and next-problem
   localization, best included as supporting results.

An independent paper-readiness red team also found a nonmathematical
but submission-critical gap: the two-hour folder does not contain the
upstream proofs of the critical codegree, cell cap, and
matching-or-hub theorem.  The \(2/9\) calculation is credible
conditional on those audited repository results, but a paper must
either import the full chain or state the codegree as a transparent
hypothesis.  The red team supplies a clean theorem formulation in
`route_f/PAPER_READINESS_RED_TEAM.md`.

The campaign subsequently implemented the second option in
`route_h/SELF_CONTAINED_CONDITIONAL_THEOREM.md`.  That note defines the
axial geometry and cell weights, states the cell cap and critical
pair-codegree as explicit hypotheses, and gives one continuous proof
of the finite matching-or-hub lemma, tangent-label reduction,
fixed-\(A\) lift, and strict \(2/9\) conclusion.  It is a
self-contained conditional theorem; it does not close the reduction
from a general #1083 configuration and therefore does not remove the
Q1 significance gap.

Before making a public novelty claim, the work still needs an
exhaustive MathSciNet/Zentralblatt/formula-level priority audit and a
self-contained manuscript that imports all inherited hypotheses.

## 7. Next theorem to attack

The best next target is not another scalar incidence bound.  It is a
stability/incompatibility statement saying that a common global set
\(T_\ast\), \(|T_\ast|\le t^{1+o(1)}\), cannot support
\(t^{19/9-o(1)}\) height rows of size \(t^{5/6-o(1)}\) whose affine
parabolic images against a source set of size \(t^{7/9-o(1)}\)
compress into \(t^{3+o(1)}\) values while the fixed-column
Szemerédi--Trotter and label-service ledgers are simultaneously near
extremal.

A successful theorem needs to exploit at least two heights and the
common label/target-plane service.  Generic one-step sum-product,
single-height energy, or plane-pair matching cardinality has already
been proved insufficient.

The threshold payoff is now explicit.  A factor \(t^{-\delta}\)
saving in the fixed-\(A\) incidence main term moves the structural
threshold to \(2/9+\delta/6\).  The same saving in the rich-line count
or target-capacity inequality moves it to \(2/9+\delta/18\).  A
cross-energy estimate must first be made uniform over nearby dyadic
ledgers before either conversion can be invoked.

Route E packages the latter target as the single joint inequality
\[
RNu^4\le t^{-\delta+o(1)}MQ(ML)^2.
\]
Its full branch audit proves that this hypothesis gives matchings of
size \(t^{2/9+\delta/18-\varepsilon-o(1)}\).  It also constructs an
exact target-service saturation model, so the missing saving must
couple source incidences to target service rather than improve either
capacity in isolation.
