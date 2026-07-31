# Second independent red-team audit: tangent--label rich-line hub theorem

Date: 2026-07-30

Audited target:
`TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`

Audited snapshot SHA-256:

```text
b4ab41017df14e4b7f3adac67d39c9bb4b83cb90e4e708c79cc3f5a8dfee17b5
```

## 0. Verdict

\[
\boxed{
\begin{array}{c}
\texttt{REPAIRED }3/14\texttt{ CHAIN: PASS}\\
\texttt{PLANAR TARGET-FIBRE REFINEMENT TO }9/41\texttt{: PASS}
\end{array}}
\]

The first audit correctly found that the Szemerédi--Trotter rich-line
bound cannot be used for the \(u=1,2\) layers.  The revised manuscript
repairs this point:

1. Theorems 2 and 3 are now stated only for \(u\ge4\);
2. the mass-carrying layer is first passed through the weighted
   point--circle inequality;
3. this forces
   \[
   m\ge\frac{5-15\kappa}{2}-o(1);
   \]
4. throughout both claimed strict ranges, \(m\) is bounded away from
   zero, hence \(u=t^{m+o(1)}\ge4\) for all sufficiently large \(t\);
5. only then is the rich-line theorem invoked.

I independently reconstructed:

- \(\mu(C)\le2r(\ell_C)\);
- the \(4Q\) source-fibre cap;
- retention of the positive-radius hub mass \(W\);
- the dyadic layer extraction;
- the point--circle lower bound on \(m\);
- the tangent-line upper bound on \(m\);
- the \(3/14\) crossing;
- the new planar target-fibre cap;
- inequalities (43)--(48) and the \(9/41\) crossing; and
- both endpoint exponent ledgers.

No exponent or quantifier defect was found in the revised strict-range
claims.  The conclusions remain structural matching results; neither
one improves the \(3/5\) distinct-distance exponent.

## 1. Repetition-to-rich-line bound

For a merged positive-radius circle \(C\), every producing triple
\((\beta,q,d)\) gives

\[
\left(\tan^2(\alpha-\beta),d\right)
\in
\ell_C\cap(\mathcal T_\alpha\times\mathcal D_0).
\]

For one fixed target plane \(\beta\), injectivity of

\[
(q,d)\longmapsto\Gamma_{\beta,q,d}
\]

allows at most one producing triple.  Axial planes are indexed modulo
\(\pi\), and a fixed value of \(\tan^2(\alpha-\beta)\) has at most two
preimages on that quotient.  Consequently every parameter point has
at most two triple preimages and

\[
\boxed{\mu(C)\le2r(\ell_C).}
\]

The factor two cannot in general be removed: the reflected angular
values have equal tangent squares.  The horizontal-line case \(A=0\)
does not invalidate this counting statement.

## 2. The \(4Q\) source-fibre cap

Fix one parameter line

\[
\ell:y=b+ax,\qquad a\ge0,\quad b>0.
\]

It fixes

\[
A(C)^2=a,\qquad \rho(C)^2=b.
\]

For a source point \(p=(u,z)\), a circle in this line fibre has centre
\((A,w)\) and contains \(p\) only if

\[
(z-w)^2=b-(u-A)^2.
\]

There are at most two signs of \(A\), and for each sign at most two
values of \(w\).  Thus each source point is incident to at most four
merged circles in the complete fibre.  Summing over
\(|P_\alpha|\le Q\) proves

\[
\boxed{\sum_{\ell_C=\ell}s(C)\le4Q.}
\]

This is an incidence cap, not merely a circle-count cap, so a circle
rich in source points is charged correctly.  When \(A=0\), the two
signs coincide and the true bound is at most \(2Q\); \(4Q\) remains
valid.

## 3. Retention of the hub mass

Before the positive-radius deletion, summing the hub condition over
the selected labels gives representation mass at least

\[
LH=t^{7-3\kappa-o(1)}.
\]

There are at most

\[
\mathsf T\le MQL=t^{6-2\kappa+o(1)}
\]

triples \((\beta,q,d)\).  Empty or negative-radius equations contribute
no real source incidences, and every zero-radius equation contributes
at most one.  For every fixed \(\kappa<1\),

\[
(7-3\kappa)-(6-2\kappa)=1-\kappa>0.
\]

Therefore deleting all zero-radius triples loses \(o(LH)\).
Merging equal positive-radius circles preserves the remaining mass
exactly, because a circle of source richness \(s(C)\) repeated
\(\mu(C)\) times contributes \(s(C)\mu(C)\).  Hence

\[
\boxed{
W=\sum_Cs(C)\mu(C)
\ge t^{7-3\kappa-o(1)}.
}
\]

The perpendicular target plane had already been removed in the
inherited hub theorem, so it is not silently charged to \(W\).

## 4. Dyadic extraction and the repaired \(u\ge4\) gate

Every retained circle has

\[
1\le s(C)\le Q,\qquad1\le\mu(C)\le M.
\]

There are \(O(\log Q\log M)=t^{o(1)}\) dyadic layers.  Thus one layer
\(\mathcal C_{s,u}\) has

\[
W_{s,u}\ge t^{7-3\kappa-o(1)}.
\]

For this layer write

\[
u=t^{m+o(1)},\qquad0\le m\le1.
\]

The manuscript now applies the point--circle bound before the
tangent--label bound.  For every \(\kappa<9/41\), and therefore also
for every \(\kappa<3/14\), the resulting lower bound gives

\[
m\ge\frac{5-15\kappa}{2}-o(1)
\ge\frac{35}{41}-o(1)>0.
\]

Hence \(u\to\infty\) polynomially and the selected layer lies in the
valid \(u\ge4\) domain.  No rich-line estimate for the bounded-\(u\)
layers is needed or claimed.

## 5. Independent reconstruction of the \(3/14\) chain

Let \(N=|\mathcal C_{s,u}|\).  Since \(Nu\le\mathsf T\), multiplying
the planar point--circle incidence theorem by the upper dyadic weight
gives four exponent candidates:

\[
6-\frac{4\kappa}{3}+\frac m3,\qquad
\frac{72}{11}-\frac{18\kappa}{11}+\frac{2m}{11},
\qquad
3+m,\qquad
6-2\kappa.
\]

The required layer exponent is \(7-3\kappa\).  The corresponding
thresholds from the first three terms are

\[
m\ge3-5\kappa,\qquad
m\ge\frac{5-15\kappa}{2},\qquad
m\ge4-3\kappa,
\]

while the fourth term misses by \(1-\kappa\).  For
\(0<\kappa<1/3\), the middle threshold is the weakest and therefore
necessary:

\[
\boxed{
m\ge\frac{5-15\kappa}{2}-o(1).
}
\]

Once \(u\ge4\), \(\mu(C)\le2r(\ell_C)\) makes every represented
parameter line at least \(u/2\)-rich.  Szemerédi--Trotter and the
\(4Q\) cap give

\[
W_{s,u}
\ll
Q\left\{
\frac{(ML)^2}{u^2}+ML
\right\}.
\]

The two exponents are

\[
9-4\kappa-2m,\qquad6-2\kappa.
\]

The second again misses by \(1-\kappa\).  The first must carry the
layer and therefore

\[
\boxed{m\le1-\frac\kappa2+o(1).}
\]

The two inequalities are incompatible exactly when

\[
\frac{5-15\kappa}{2}
>
1-\frac\kappa2,
\]

which is

\[
\boxed{\kappa<\frac3{14}.}
\]

At \(\kappa=3/14\) the two bounds meet at \(m=25/28\); the source-fibre
argument alone does not exclude the endpoint.

### The \(3/14\) endpoint ledger

The earlier ledger

\[
a=\frac{11}{14},\quad
b=\frac{131}{28},\quad
m=\frac{25}{28},\quad
p=\frac{18}{7},\quad
c=\frac{69}{28}
\]

is consistent:

\[
\begin{aligned}
a+b+m&=7-3\kappa=\frac{89}{14},\\
b+m&=6-2\kappa=\frac{39}{7},\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=2p-3m=a+b-3,\\
m&=\frac{5-15\kappa}{2}=1-\frac\kappa2.
\end{aligned}
\]

The second rich-line term has exponent \(p-m<c\).  Thus the original
\(3/14\) method boundary is algebraically correct.

## 6. Planar target-fibre cap

Fix a parameter line \(\ell:y=b+ax\), one sign
\(A\in\{\sqrt a,-\sqrt a\}\), and all merged circles over this line
with that sign.  They have common radius \(\sqrt b\), centres

\[
(A,w_C),
\]

and distinct circles have distinct \(w_C\).

After rotating the source plane to the \(xz\)-plane, every producing
target triple has the actual Cartesian point

\[
\boxed{
q=(A,A\tan(\beta-\alpha),w_C).
}
\]

Thus all target points lie in the ordinary plane \(x=A\).

The inherited target sets are off-axis and the perpendicular target
plane has been removed.  Hence \(v\ne0\),
\(\cos(\alpha-\beta)\ne0\), and

\[
A=v\cos(\alpha-\beta)\ne0.
\]

For one circle, fixed-plane injectivity gives distinct target planes;
because tangent is injective modulo \(\pi\) and \(A\ne0\), their
transverse coordinates are distinct.  Across different circles,
the heights \(w_C\) are distinct.  Therefore the points are mutually
distinct and

\[
|X_{\ell,A}|=\sum_C\mu(C).
\]

The planar distinct-distance theorem gives

\[
D
\ge|\Delta^2(X_{\ell,A})|
\gg\frac{|X_{\ell,A}|}{\log(2|X_{\ell,A}|)}.
\]

The standard inversion of this inequality yields

\[
\boxed{
\sum_C\mu(C)
\ll D\log(2D).
}
\]

The proof is valid because \(X_{\ell,A}\) is an actual subset of the
original configuration, not a multiset of parameter triples.

### Minor presentation dependence

The nonzero-\(A\) step uses the inherited fact that every target point
in \(P_\beta\) is off the common axis.  The main proof cites this fact,
but adding it explicitly to the setup bullet list would make Lemma 2
self-contained.  This is a presentation improvement, not a logical
gap in the inherited setting.

## 7. Refined dyadic capacity

For one parameter line, the source cap gives fibre mass
\(O(Qu)\).  Splitting into the at most two signs of \(A\), the planar
target cap and \(s(C)<2s\) give fibre mass

\[
O(Ds\log(2D)).
\]

The \(u/2\)-rich line count is

\[
O\left(
\frac{(ML)^2}{u^3}+\frac{ML}{u}
\right).
\]

Multiplying by the better fibre cap proves, for \(u\ge4\),

\[
\boxed{
W_{s,u}
\ll
\left\{
\frac{(ML)^2}{u^3}+\frac{ML}{u}
\right\}
\min\{Qu,Ds\log(2D)\}.
}
\]

No interaction between the two sign classes is omitted; splitting
them changes only an absolute factor.

## 8. Independent reconstruction of the \(9/41\) LP

Write

\[
s=t^{a+o(1)},\qquad
N=t^{b+o(1)},\qquad
u=t^{m+o(1)}.
\]

For \(\kappa<9/41\), the
\(Q^{2/3}N^{2/3}\), \(+Q\), and \(+N\) point--circle terms cannot carry
the selected layer.  The first would require
\(m\ge3-5\kappa>1\), the second \(m\ge4-3\kappa>1\), and the last is
bounded by \(\mathsf T=t^{6-2\kappa+o(1)}\), which misses the hub mass
by \(1-\kappa\).

Hence the \(6/11,9/11\) term must carry.  Cancelling its dyadic factor
\(u\) gives

\[
11a+2b\le18+o(1).
\]

The layer mass gives

\[
b\ge7-3\kappa-a-m-o(1).
\]

Eliminating \(b\) yields

\[
\boxed{
a\le\frac{4+6\kappa+2m}{9}+o(1).
}
\]

Using the \(Ds\) branch of the refined tangent-line bound gives the
two exponent candidates

\[
9+a-4\kappa-3m,\qquad
6+a-2\kappa-m.
\]

Their difference is

\[
3-2\kappa-2m>0
\]

for \(m\le1\) and \(\kappa<9/41\).  Thus the first must reach
\(7-3\kappa\), which forces

\[
\boxed{a\ge3m-2+\kappa-o(1).}
\]

Combining the two bounds on \(a\) gives

\[
\boxed{
m\le\frac{22-3\kappa}{25}+o(1).
}
\]

Together with the point--circle lower bound, a surviving hub would
require

\[
\frac{5-15\kappa}{2}
\le
\frac{22-3\kappa}{25}+o(1).
\]

The exact difference is

\[
\frac{81-369\kappa}{50},
\]

so the crossing is

\[
\boxed{\kappa=\frac9{41}.}
\]

Every fixed \(\kappa<9/41\) leaves a fixed positive exponent gap.
The endpoint itself is not excluded.

## 9. The \(9/41\) endpoint ledger

At \(\kappa=9/41\), the manuscript uses

\[
a=\frac{32}{41},\quad
b=\frac{193}{41},\quad
m=\frac{35}{41},\quad
p=c=\frac{105}{41}.
\]

Direct calculation gives

\[
\begin{aligned}
a+b+m&=\frac{260}{41}=7-3\kappa,\\
b+m&=\frac{228}{41}=6-2\kappa,\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=2p-3m=p,\\
c+3+a&=\frac{260}{41},\\
m&=\frac{5-15\kappa}{2}
=\frac{22-3\kappa}{25}.
\end{aligned}
\]

There are \(t^{b-c}=t^{88/41}\) circles per typical parameter line.
Their target-point mass has exponent

\[
(b-c)+m=\frac{123}{41}=3,
\]

which saturates the planar target-fibre cap.  Their source incidence
mass has exponent

\[
(b-c)+a=\frac{120}{41}<3,
\]

leaving \(3/41\) slack in the \(4Q\) source cap.  The second rich-line
term has exponent

\[
p-m=\frac{70}{41}<c.
\]

Thus every equality and every claimed slack direction in the endpoint
ledger is correct.

## 10. Scope and residual risks

### Certified

- the repaired strict \(3/14\) exclusion;
- the planar target-fibre lemma;
- the refined strict \(9/41\) exclusion;
- the matching exponent \(9/41-\varepsilon\), with the usual convention
  that when the displayed exponent is nonpositive the statement is
  trivial;
- the exact claim boundary that no improved global distance exponent
  has yet been proved.

### Not certified by this argument

- either endpoint \(\kappa=3/14\) by the source cap alone or
  \(\kappa=9/41\) by the refined argument;
- Euclidean realizability of the \(9/41\) equality ledger;
- an inverse theorem for simultaneous near-extremizers;
- a Q1-level publication claim from this structural theorem alone.

### Minor formalization notes

- The inversion
  \(D\gg n/\log(2n)\Rightarrow n\ll D\log(2D)\) is standard but could
  be written as a one-line auxiliary inequality.
- The exponent variables \(a,b,m\) may be formalized by passing to a
  convergent subsequence of logarithmic exponents.  The current
  \(t^{a+o(1)}\) notation is standard and does not change the strict
  conclusions.

## 11. Reproduction

The revised verifier and tests were run without bytecode or pytest
cache writes:

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_b
PYTHONDONTWRITEBYTECODE=1 python3 verify_tangent_label_rich_line_hub.py
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider \
  test_verify_tangent_label_rich_line_hub.py
```

Result:

```text
5 passed in 0.34s
```

The code verifies the radius identity, both threshold crossings, the
\(9/41\) endpoint ledger, a finite \(4Q\) source-fibre example, and a
finite coplanar target-fibre example.  The incidence theorems, hub-mass
retention, and distinctness of the full target subset were audited
mathematically above rather than delegated to the finite tests.
