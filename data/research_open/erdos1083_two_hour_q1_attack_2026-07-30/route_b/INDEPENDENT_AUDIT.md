# Independent red-team audit: tangent--label rich-line hub theorem

Date: 2026-07-30

Audited target:
`TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`

## 0. Verdict

\[
\boxed{
\texttt{PASS AFTER THE }u\ge4\texttt{ REPAIR;}
\quad
\texttt{THE REFINED }9/41\texttt{ CONSEQUENCE ALSO PASSES.}
}
\]

The tangent--label identity, the repetition-to-line multiplicity bound,
the \(4Q\) parameter-line fibre cap, the inherited positive-radius hub
mass, both multiplicity thresholds, and their crossing at \(3/14\) all
pass independent audit.  The later planar target-fibre cap, its refined
dyadic capacity theorem, the \(9/41\) exponent algebra, and the new
endpoint ledger pass as well.

An earlier version had one material logical defect.  The rich-line
consequence of Szemerédi--Trotter is valid for lines incident to at least
two points, not for arbitrary one-rich lines.  From
\[
\mu(C)\le2r(\ell_C)
\]
and \(u\le\mu(C)\), one obtains only
\[
r(\ell_C)\ge u/2.
\]
The current theorem has repaired this point: Theorems 2 and 3 are
explicitly restricted to \(u\ge4\), and the point--circle inequality is
applied first.  In the full refined range \(\kappa<9/41\), it forces
\[
u=t^{m+o(1)},\qquad
m\ge\frac{5-15\kappa}{2}-o(1)>\frac{35}{41}-o(1).
\]
Hence the mass-carrying layer has \(u\to\infty\), and in particular
\(u\ge4\) for sufficiently large \(t\).  Thus neither the \(3/14\) nor
the \(9/41\) conclusion uses an uncontrolled bounded-multiplicity layer.

The current setup also states directly that all retained source and
target points are off the common axis, so \(v\ne0\) and hence
\(A=\cos(\alpha-\beta)v\ne0\).  This agrees with the inherited
angular-starvation setup, where every \(P_\beta\) is the off-axis point
set.  The condition is essential to Lemma 2: without \(A\ne0\), target
points from different axial planes could collapse on the common axis.

## 1. Tangent--label identity

With
\[
c=\cos(\alpha-\beta),\qquad A=cv,
\]
the reverse circle has squared radius
\[
\rho^2=d-(1-c^2)v^2.
\]
For a retained nonperpendicular plane \(c\ne0\), substitution
\(v=A/c\) gives
\[
\rho^2
=d-A^2\frac{1-c^2}{c^2},
\]
and therefore
\[
\boxed{d=\rho^2+A^2\tan^2(\alpha-\beta).}
\]
The height coordinate \(w\) correctly drops out.  No sign of \(A\) is
lost in this identity because the parameter line records \(A^2\).
The line intercept is positive after the zero-radius removal.

The supplied symbolic verifier independently reduces the identity to
zero, and a separate hand expansion gives the same formula.

## 2. Audit of \(\mu(C)\le2r(\ell_C)\)

Fix one merged circle \(C\).  Fixed-plane injectivity of
\[
(q,d)\longmapsto\Gamma_{\beta,q,d}
\]
shows that a target plane \(\beta\) contributes at most one triple to
\(C\).

Each contributing triple maps to
\[
\left(
\tan^2(\alpha-\beta),d
\right)
\in
\ell_C\cap(\mathcal T_\alpha\times\mathcal D_0).
\]
Axial planes are indexed modulo \(\pi\).  On such an interval, a fixed
value of \(\tan^2(\alpha-\beta)\) has at most two plane preimages.
Therefore at most two triples map to any one parameter point, proving
\[
\mu(C)\le2r(\ell_C).
\]

The horizontal-line case \(A=0\) is harmless.  The line then has
constant ordinate \(d=\rho^2\), but different tangent-square
coordinates remain different points, and the at-most-two angular
preimage count is unchanged.

No stronger inequality such as \(\mu(C)\le r(\ell_C)\) is justified:
the two reflected target-plane angles can share the same tangent square.

## 3. Audit of the \(4Q\) fibre cap

Fix a parameter line
\[
\ell:y=b+ax,\qquad a\ge0,\quad b>0.
\]
Every circle over this line has
\[
A=\pm\sqrt a,\qquad \rho=\sqrt b,
\]
and centre \((A,w)\).  For one source point \(p=(u,z)\), incidence is
equivalent to
\[
(z-w)^2=b-(u-A)^2.
\]
For each of the at most two values of \(A\), this equation has at most
two real solutions for \(w\).  Hence a source point lies on at most four
circles in the complete line fibre.  Summing over
\(|P_\alpha|\le Q\) gives
\[
\sum_{\ell_C=\ell}s(C)\le4Q.
\]

This counts incidences rather than merely circles, so coincident
incidences cannot evade the bound.  Equal circles were merged before
the sum.  At \(A=0\), the two sign choices coincide and the true cap is
at most \(2Q\); \(4Q\) remains valid.

The supplied random integer-coordinate certificate found maximum local
multiplicity four and total incidence below \(4Q\).  The finite
certificate is not needed for the proof above.

## 4. Rich-line Szemerédi--Trotter step

Let
\[
n=|\mathcal T_\alpha\times\mathcal D_0|\le ML.
\]
The standard rich-line consequence of Szemerédi--Trotter is
\[
\#\{\ell:|\ell\cap\mathcal P|\ge k\}
\ll \frac{n^2}{k^3}+\frac nk
\qquad(k\ge2).
\]
For a layer with \(u\ge4\), Section 2 gives
\[
r(\ell)\ge u/2\ge2,
\]
and therefore
\[
|\Lambda_{s,u}|
\ll\frac{(ML)^2}{u^3}+\frac{ML}{u}.
\]
Combining this with the \(4Q\) fibre cap and
\(\mu(C)<2u\) correctly gives
\[
W_{s,u}
\ll
Q\left\{
\frac{(ML)^2}{u^2}+ML
\right\}.
\]

For \(u=1,2\), however, \(r(\ell)\ge u/2\) only forces a line to contain
one parameter point.  No bound of order \(n^2\) exists for the number
of one-rich lines in general.  The current manuscript correctly makes
no rich-line assertion for those layers.

The supplied verifier does not test this logical gate; it checks the
radius identity, exponent algebra, a finite \(4Q\) example, and the
fixed-\(A\) planar target encoding.

### Repair incorporated in the current text

State the dyadic theorem for \(u\ge4\).  In the hub proof:

1. choose the mass-carrying \((s,u)\)-layer;
2. apply the weighted point--circle bound;
3. infer \(u=t^{m+o(1)}\) with
   \(m\ge(5-15\kappa)/2-o(1)\);
4. for \(\kappa<3/14\), conclude \(u\ge4\) for large \(t\);
5. only then apply the tangent--label rich-line bound.

The current proof follows this order.  The same observation applies in
the larger range \(\kappa<9/41\), because the forced lower exponent for
\(u\) is then still \(35/41-o(1)>0\).

## 5. Does \(W\) retain the hub mass?

Yes, subject to the inherited removals explicitly cited by the
manuscript.

For each retained triple \((\beta,q,d)\), the corresponding circle
contributes exactly
\[
|P_\alpha\cap\Gamma_{\beta,q,d}|
\]
representations of \(d\).  Merging equal positive-radius circles and
assigning multiplicity \(\mu(C)\) therefore preserves this mass exactly:
\[
\sum_{\beta,q,d}
|P_\alpha\cap\Gamma_{\beta,q,d}|
=\sum_Cs(C)\mu(C)=W.
\]

Negative-radius equations have no real source incidence.  A zero-radius
triple has at most one source incidence, and there are at most
\[
MQL=t^{6-2\kappa+o(1)}
\]
triples.  The hub mass is
\[
LH=t^{7-3\kappa-o(1)}.
\]
For every fixed \(\kappa<1\), the exponent gap is \(1-\kappa>0\).
Thus deleting all zero-radius triples loses \(o(LH)\), and the retained
positive-radius mass still satisfies
\[
W\ge t^{7-3\kappa-o(1)}.
\]

The perpendicular target plane had already been removed before the
matching-or-hub extraction in the inherited theorem.  Consequently no
mass from that exceptional pair is silently used here.

## 6. Weighted point--circle lower threshold

Let \(N=|\mathcal C_{s,u}|\).  Since every circle in the layer has
weight at least \(u\),
\[
Nu\le\mathsf T\le MQL.
\]
Multiplying the planar point--circle incidence bound by \(2u\) gives
\[
\begin{aligned}
W_{s,u}\ll{}&
Q^{2/3}\mathsf T^{2/3}u^{1/3}\\
&+Q^{6/11}\mathsf T^{9/11}u^{2/11}t^{o(1)}
+Qu+\mathsf Tt^{o(1)}.
\end{aligned}
\]
At
\[
Q=t^{3+o(1)},\qquad
\mathsf T\le t^{6-2\kappa+o(1)},\qquad
u=t^{m+o(1)},
\]
the four exponents are exactly
\[
6-\frac{4\kappa}{3}+\frac m3,\quad
\frac{72}{11}-\frac{18\kappa}{11}+\frac{2m}{11},\quad
3+m,\quad
6-2\kappa.
\]
Comparison with \(7-3\kappa\) gives the candidate thresholds
\[
m\ge3-5\kappa,\qquad
m\ge\frac{5-15\kappa}{2},\qquad
m\ge4-3\kappa,
\]
while the last term misses by \(1-\kappa\).  For \(\kappa>0\), the
middle threshold is the smallest.  Thus, for \(\kappa<1/3\),
\[
\boxed{
m\ge\frac{5-15\kappa}{2}-o(1).
}
\]
This part of the argument is correct and does not use the defective
bounded-\(u\) rich-line claim.

## 7. Tangent--label upper threshold and \(3/14\)

Once \(u\ge4\), the repaired tangent--label bound has exponents
\[
9-4\kappa-2m,\qquad6-2\kappa.
\]
The second misses the hub exponent by \(1-\kappa\); hence the first must
reach it:
\[
7-3\kappa
\le9-4\kappa-2m+o(1).
\]
Therefore
\[
\boxed{m\le1-\frac\kappa2+o(1).}
\]

The lower and upper bounds are incompatible precisely when
\[
\frac{5-15\kappa}{2}>1-\frac\kappa2,
\]
that is,
\[
\boxed{\kappa<\frac3{14}.}
\]
The difference is
\[
\frac32-7\kappa,
\]
so every fixed strict inequality absorbs the \(t^{o(1)}\) losses.
No endpoint exclusion at \(\kappa=3/14\) follows.

For \(\kappa<3/14\), the lower threshold is at least
\[
\frac{5-15(3/14)}2=\frac{25}{28},
\]
up to a fixed positive margin in the strict range.  This verifies that
the repaired proof always reaches the \(u\ge4\) domain before using
Szemerédi--Trotter rich lines.

## 8. Endpoint ledger

At \(\kappa=3/14\), the displayed values
\[
a=\frac{11}{14},\quad
b=\frac{131}{28},\quad
m=\frac{25}{28},\quad
p=\frac{18}{7},\quad
c=\frac{69}{28}
\]
satisfy all printed equalities:
\[
\begin{aligned}
a+b+m&=\frac{89}{14}=7-3\kappa,\\
b+m&=\frac{39}{7}=6-2\kappa,\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=a+b-3=2p-3m,\\
m&=\frac{5-15\kappa}{2}=1-\frac\kappa2.
\end{aligned}
\]
The second rich-line term has exponent \(p-m<c\), and the two weighted
tangent-line terms have exponents
\[
3+2p-2m=\frac{89}{14},\qquad
3+p<\frac{89}{14}.
\]
Thus the abstract equality ledger is internally consistent.  It is
correctly labeled as an exponent ledger rather than a Euclidean
realization.

## 9. Matching corollary and scope

For fixed \(0<\varepsilon<3/14\), set
\[
\kappa=3/14-\varepsilon.
\]
The repaired hub exclusion forces the matching alternative with the
claimed exponent.  For \(\varepsilon\ge3/14\), the displayed lower
power is nonpositive and follows trivially from any fixed positive
\(\kappa<3/14\); stating this boundary convention would improve the
presentation.

The theorem improves the structural matching exponent only.  It does
not prove a distinct-distance exponent above \(3/5\), and the manuscript
correctly preserves that boundary.

## 10. Reproduction record

The supplied verifier and regression tests were rerun without bytecode
or pytest cache writes:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify_tangent_label_rich_line_hub.py
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider \
  test_verify_tangent_label_rich_line_hub.py
```

Result:

```text
4 passed in 0.41s
```

The exact certificate confirms:

- the radius identity;
- the two threshold formulas and their \(3/14\) crossing;
- every endpoint-ledger equality; and
- a finite example of the \(4Q\) fibre cap.

It does not certify the analytic incidence theorems, the rich-line
domain condition, or the inherited hub-mass retention.  Those points
were audited separately above and below.

## 11. Planar target-fibre cap

Fix a parameter line
\[
\ell:y=b+ax
\]
and one sign \(A=\pm\sqrt a\).  Every circle in this fibre has the
same radial centre \(A\), the same positive radius \(\sqrt b\), and a
centre \((A,w_C)\).  Distinct merged circles have distinct \(w_C\)'s.

For a producing triple \((\beta,q,d)\), rotation of the source plane to
the \(xz\)-plane gives
\[
q=(A,A\tan(\beta-\alpha),w_C).
\]
The inherited off-axis condition gives \(A\ne0\).  Axial planes are
indexed modulo \(\pi\), on which tangent is injective.  Hence the
\(\mu(C)\) target planes contributing to a fixed circle give
\(\mu(C)\) distinct target points.  Different circles have different
height \(w_C\), so their target points are distinct as well.  All lie
in the ordinary plane \(x=A\).  Thus the original configuration
contains exactly
\[
n_{\ell,A}=\sum_{\substack{C:\ell_C=\ell\\A(C)=A}}\mu(C)
\]
distinct points in one plane.

The planar distinct-distance lower bound
\[
|\Delta(X)|\gg |X|/\log(2|X|)
\]
and the global budget \(D\) imply
\[
\boxed{n_{\ell,A}\ll D\log(2D).}
\]
This proves Lemma 2.  Splitting a line fibre into the at most two signs
of \(A\), and using \(s(C)<2s\), gives the second fibre capacity
\[
\sum_{\ell_C=\ell}s(C)\mu(C)\ll Ds\log(2D).
\]
Taking the minimum with the already audited \(Qu\) capacity and
multiplying by the valid \(u\ge4\) rich-line count proves Theorem 3.

The off-axis condition is indispensable.  If \(A=0\), the displayed
target coordinate is \((0,0,w_C)\) for every \(\beta\), so multiplicity
would not in general produce distinct planar points.  The proof chain
does exclude this case: `ANGULAR_STARVATION_BRANCH_ATTACK.md` defines
every \(P_\beta\) to be its off-axis source set, and the perpendicular
plane has separately been deleted.  The current Route B setup now cites
this inherited deletion explicitly.

## 12. Independent audit of the \(9/41\) algebra

Write
\[
s=t^{a+o(1)},\qquad
N=t^{b+o(1)},\qquad
u=t^{m+o(1)}.
\]
The \(6/11,9/11\) point--circle term is the only term capable of carrying
the selected layer for \(\kappa<9/41\).  Comparing
\[
Nsu
\quad\hbox{with}\quad
uQ^{6/11}N^{9/11}
\]
gives
\[
11a+2b\le18+o(1).
\]
The mass lower bound gives
\[
b\ge7-3\kappa-a-m-o(1),
\]
and therefore
\[
\boxed{a\le\frac{4+6\kappa+2m}{9}+o(1).}
\]

The \(Ds\) branch of Theorem 3 has exponents
\[
9+a-4\kappa-3m,\qquad
6+a-2\kappa-m.
\]
Their difference is \(3-2\kappa-2m>0\) for
\(m\le1\) and \(\kappa<9/41\).  Consequently the first term must carry,
which yields
\[
\boxed{a\ge3m-2+\kappa-o(1).}
\]
Combining the two bounds on \(a\) gives
\[
\boxed{m\le\frac{22-3\kappa}{25}+o(1).}
\]
The independent point--circle lower threshold remains
\[
\boxed{m\ge\frac{5-15\kappa}{2}-o(1).}
\]
Solving equality of these two affine functions gives
\[
25(5-15\kappa)=2(22-3\kappa),
\qquad
\boxed{\kappa=\frac9{41}}.
\]
Therefore every fixed \(\kappa<9/41\) is excluded by a fixed power gap,
while the endpoint itself is not excluded.

## 13. Refined endpoint ledger

At \(\kappa=9/41\), the current values
\[
a=\frac{32}{41},\quad
b=\frac{193}{41},\quad
m=\frac{35}{41},\quad
p=c=\frac{105}{41}
\]
satisfy
\[
\begin{aligned}
a+b+m&=\frac{260}{41}=7-3\kappa,\\
b+m&=\frac{228}{41}=6-2\kappa,\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=2p-3m=p,\\
c+3+a&=\frac{260}{41}.
\end{aligned}
\]
Moreover
\[
(b-c)+m=3,\qquad (b-c)+a=\frac{120}{41}<3.
\]
Thus the planar target cap is exactly active and the source \(4Q\) cap
has slack.  The ledger is internally consistent and is properly
labelled as an abstract exponent saturation, not a realized Euclidean
configuration.

## 14. Updated scope verdict

The repaired Route B theorem proves an unconditional improvement of the
structural matching exponent from \(1/5\) to \(9/41-\varepsilon\).  It
does **not** prove an improvement of the \(3/5\) distinct-distance
exponent and is not, by itself, a resolution of Erdős #1083.  The main
document states both boundaries correctly.
