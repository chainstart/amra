# Eight-hour mathematics campaign: final report

Campaign window: 2026-07-29--30, Asia/Hong_Kong

## Bottom line

The session did not produce a result that can yet be certified as a Chinese
Academy of Sciences Zone-1 paper.  It did produce:

1. a substantially strengthened KOU-21.137 specialist-manuscript candidate;
2. a complete closure-aware exclusion of every dimension-eleven profile in
   the \(J^9=0\) algebra-group search;
3. an exact finite injection and a sharply localized general-injection
   contract for OPG-1757;
4. no-go theorems under fixed-field, bounded-complexity, or explicit-
   normalization assumptions, together with exhaustive finite tests for
   Erdős #1083.

The honest publication ranking is KOU first, OPG second, Erdős third.

## 1. KOU-21.137 and Wilson power subgroups

### Main theorem package

For an arbitrary group \(A\) and prime \(p\), the raw \(p\)-th powers in
\(A\wr C_p\) form a subgroup exactly in the two cases described by the
prime-wreath criterion.  In the proper case

\[
P_p(A)=A',\qquad x^A=xA'\quad(x\notin A'),
\]

and the power subgroup is the \(p\)-fold fibre product over \(A/A'\).
For finite seeds this yields an at-most-five-branch classification; for
finite nonabelian 2-group seeds the condition is precisely
semi-extraspeciality.

For the original square problem:

- there is no qualifying group below order 128;
- exactly ten order-128 groups qualify,
  `SmallGroup(128,928..937)`;
- they are ten central lifts of one explicit order-64 quotient, split into
  six \(C_2\times D_8\) and four \(C_2\times Q_8\) square-subgroup types.

The individual \(D_8\wr C_2\) example is prior public work and is not claimed
as an AMRA discovery.

### Odd-prime and algebra search boundary

- All 1,396,077 groups of order \(3^8\) were covered by the official
  SmallGroups catalogue scan.  Sixty-three nonpowerful hard candidates were
  rerun independently; none had a closed raw-cube set.  Hence a finite
  \(p=3\) Wilson counterexample has order at least \(3^9\).
- All 92 dimension-ten algebra profiles in the stronger \(J^9=0\)
  algebra-group scope were excluded by human lemmas.  An independent
  Cartesian-product ledger also leaves zero survivors.
- An explicit dimension-eleven algebra has noncommuting cubes, proving the
  pure commutativity lower bound sharp.  Its 171 raw cubes are not closed:
  the leading image has seven points and unequal fibre sizes
  \(9,27,\ldots,27\).
- Of 246 dimension-eleven profiles, the structural filters leave only
  \((2,2,2,2,2,1)\) and \((2,2,2,2,1,1,1)\).  A new normal-word lemma,
  independently checked by all 130 planes in
  \(\operatorname{Gr}(2,4)(\mathbb F_3)\), proves
  \(d_1=d_2=2\Rightarrow d_3\le2\) and removes the formerly surviving
  \((2,2,3,1,1,1,1)\) profile.  Raw-cube closure excludes the length-six
  profile by a fibre-coset argument.  The final profile
  \[
  (2,2,2,2,1,1,1).
  \]
  splits into \(\dim Q=1\) and
  \(\dim Q=2,\ K=1+J^6,\ |H|=81\).  The pure sevenfold tail makes
  \([A_3,A_4]=0\), so the first branch is abelian.  In the second branch,
  closure makes \(P:A_2\to J^6,\ w\mapsto w^3\) a bijection.  Exact
  quadratic-relation reduction leaves 12 bijective relation planes; three
  violate the required fourth-layer dimension and the other nine force
  graded commutativity.  Human factorization of the remaining quadratic
  form then produces a nonzero short-chain element \(w\in A_2\) with
  \(w^3=0\), contradicting that bijection.  Thus no dimension-eleven
  profile survives.

The next-dimensional frontier has also been enumerated without promoting
necessary conditions to existence.  For \(\dim J=12\), the same proved
filters reduce 582 positive filtration profiles to exactly eight branch
inputs.  A generalized length-six fibre lemma then excludes
\((2,2,2,2,2,2)\) without any hypothesis on \(\dim A_6\).  Associativity
of the filtered cross-relations, after the exact finite quadratic
normal-form reduction, excludes \((2,2,2,2,2,1,1)\), and the
exact quadratic lemma excludes \((2,2,2,3,1,1,1)\) by forcing
\(d_4\le2\).  The other five now satisfy explicit closure contracts.  For
\((2,3,2,2,1,1,1)\), a fail-closed graded audit reduces the search to 48
cases; all 48 strict homogeneous quotients have commuting cubes, so only
terminal filtered deformations remain relevant.  This is a reproducible map
for the next proof round, not an exclusion of dimension 12 and not evidence
that any remaining profile is realizable.

The new length-six proof is solver-free.  Closure makes the leading cubic map
bijective and forces the equal-leading fibres to be \(J^6\)-cosets.  For
\(z\in J^3\),
\[
D=(v+z)^3-v^3=v^2z+vzv+zv^2\in J^6.
\]
Since \(J^7=0\), \(vD=Dv=0\), and subtraction gives
\(v^3z=zv^3\).  Taking \(z=x^3\) makes all cubes commute, a contradiction.

### Publication gate

This is the only line currently close to a standalone manuscript.  Before a
strong novelty claim, authorized full-text audits of Mann (2005), Theorem 16,
and Bennett's 2012 thesis are mandatory, followed by MathSciNet/zbMATH
citation chaining and a finite-\(p\)-group specialist review.

## 2. OPG-1757

### Closed results

- exact fixed-page forest transfers through seven pages;
- uniform positivity of the complete \(B_4,\ldots,B_7\) coefficient
  families;
- arbitrary-\(k\) degree/end coefficients and the first five
  \(\beta\)-layers;
- a rooted-tree/Lagrange single-convolution formula for the first critical
  coefficient;
- a general base-4 Newton support theorem and nonnegativity through \(k=30\);
- a necessary-and-sufficient universal outside-stability criterion for
  edge-disjoint local/external forest replacements: the target
  boundary-connectivity partition must refine the source partition;
- an outside-stable saturated-\(K_4\) local repair;
- a complete finite injection for \(q=1,k=5\):
  2,140 negative forest pairs map into 2,240 positive pairs.

An earlier direct certificate uses 594 direct moves and 1,546 balanced
exchanges and compresses to 22 endpoint-symmetry rule orbits.  The stronger
structural certificate uses three transition classes
(`core-cross`, `E-active`, and `F-active`) and 350 reversible shortest
alternating chains.  Their lengths range from 2 to 8.  The final image
decomposes as \(1590+295+203+52=2140\), leaving exactly 100 positive
objects unused.

### Exact remaining obstruction

The formerly isolated 150 five-vertex objects are no longer an obstruction:
the bridge moves and the three transition classes absorb all of them.
However, a strictly decreasing source-only potential cannot certify the
current Round-21 deterministic, step-by-step conflict routing even in
\(q=1,k=5\): that routing has a certified source two-cycle.  A phase/BFS-
aware potential is one viable replacement, but the certificate does not
exclude a different acyclic routing, a whole-chain potential, or a direct
Hall argument.

The \(q=2,\ k\le7\) audit also shows that the three transitions do not
generalize unchanged.  Within the present nested rule family, an
active--active fourth transition first becomes necessary at \(k=3\), where
it closes an \(8>6\) Hall deficit using two length-three augmenting chains.
It closes the full layer through \(k=5\) but leaves deficits 4 and 32 at
\(k=6,7\); the particular active-handoff orbit tested closes \(k=6\) but
gives no gain at \(k=7\).  A complementary single
`core-cross`--to--`active-active` signature \(02\to45\) closes \(k=7\);
zero new signatures fail, so one is exactly minimal relative to the
four-rule graph at that finite layer.  The two finite signatures together
close the current \(q=2,k\le7\) ledger.

This still is not a uniform or outside-stable explicit injection.  The
\(02\to45\) target has up to four candidate preimages, and a displayed
\(q=3\) extension preserves the source forest but creates a target cycle.
The new characterization shows this failure is structural: any
context-free rule that merges boundary components has such an external
path witness, while a context-free rule and inverse must preserve the
boundary partition exactly.  Thus neither finite completion can be promoted
to an all-\(q,k\) repair without external-partition tags, a component-refining
rule, or a global Hall argument.

The certified finite construction proves the whole \(q=1,k=5\) coefficient
layer, but it is not yet an equivariant, outside-stable injection for
arbitrary numbers of active vertices.  A general proof now needs either a
finite complete rule grammar with a valid termination/recovery invariant, or
a direct uniform Hall argument, plus image separation.  General coefficient
positivity, and hence the full OPG theorem, remains open.

## 3. Erdős #1083

No improvement to the recognized \(n^{3/5-o(1)}\) three-dimensional
distinct-distance exponent was obtained.

The search nevertheless reached a sharp decision boundary:

- Laurent boxes, divisor multistars, repetitions, tensors and unions give at
  most
  \[
  \exp\!\left((\log2+o(1))\frac{\log n}{\log\log n}\right)=n^{o(1)}
  \]
  gain;
- fixed number fields contribute only ideal divisors times a fixed-rank unit
  lattice;
- fixed-rank rational, polynomial, GAP and multiplicative-group
  parametrizations remain \(n^{o(1)}\);
- 104 sparse fields of degrees 3--8 and 158 dense cubic/quartic fields were
  tested exactly, with no candidate near the \(n^{2/5}\) required gain;
- 122 quartic fields, 244 boundedly independent unit pairs and 118,584
  two-unit word subsets were tested, including 25 elementary
  nonrectangular shears on the finalists.  The best target ratio was only
  \(1.45903\times10^{-4}\), and the shear improved its rectangular container
  by about \(0.48\%\).

For a fixed number field \(K\) and unit rank \(r\), bounded-height words
number only \(O_K((\log n)^r)\).  In a varying family the exact packing
bound has the form
\[
|T_n|\le
\left(1+\frac{2C_n\log n}{\lambda_n}\right)^{r_n},
\]
where \(C_n\) controls the container radius and \(\lambda_n\) is the
shortest logarithmic-unit vector.  Only under
\(\log C_n+\log(1/\lambda_n)=o(\log\log n)\) does reaching
\(n^{2/5-o(1)}\) force

\[
r_n\ge(2/5-o(1))\frac{\log n}{\log\log n}.
\]

Without uniform height and regulator control there is no unconditional
numerical rank threshold; the present full power-basis estimates safely give
only a conditional \(1/5\)-scale bound.  The remaining algebraic route is
therefore the varying-field, growing-degree, noncommensurable regime, with
growing rank required only under the displayed uniformity hypothesis.
Fixed quartic tuning cannot cross the exponent gap.

One exact obstruction identity was obtained for
\(f_d(x)=\prod_{k=1}^d(x+k)-1\).  For the selected inverse-symmetrized rows,
\[
|\Delta_d|
=4\cdot3069^{d-2}\prod_{m=1}^{d-3}m!.
\]
It forces a proper coefficient box of size
\(\exp(\Theta(d^2\log d))\), while the family supplies only \(d-1=n^{o(1)}\)
parameters.  This is an exact obstruction for that family, not a universal
inverse theorem or an exponent improvement.  The polynomial identity holds
for every \(d\ge4\); its interpretation as a degree-\(d\) number-field
family requires irreducibility and a suitable real root.  Those hypotheses
have been verified only for \(5\le d\le30\), so an asymptotic number-field
family remains conditional.

## Reproducibility and trust

Every claimed finite result has a deterministic script, regression test and
scope statement.  Human theorems are separated from bounded evidence.
Timeouts are recorded as incomplete.  No branch, commit or push was made
during this campaign.

Final regressions reproduced:

- the final unified campaign run passed all 230 collected tests and 12
  subtests in 373.26 seconds: 42 KOU, 38 OPG and 150 Erdős tests;
- the KOU run includes the
  \(36\to144\to48\) graded frontier with SHA-256
  `80fd2b21a7b59d1b542b759b5f20a062f451cca9c6dcdf96191e4eef386183ef`;
- the OPG Round-22 audit SHA-256 is
  `28d47f0e106a73b33001be108c3a5b7180b9ec0dc093cd2b8484fef786d67c2e`;
  the new outside-stability theorem was separately falsification-tested on
  all 1,444 ordered pairs of four-boundary local forests and 50,050
  enumerated external-context checks;
- all 21 JSON certificates parse, bytecode compilation of the full campaign
  tree succeeds, and the whitespace/diff checks are clean.

The main navigation files are:

- [`CLAIM_LEDGER.md`](CLAIM_LEDGER.md);
- [`PUBLICATION_READINESS.md`](PUBLICATION_READINESS.md);
- [`kou21137/README.md`](kou21137/README.md);
- [`opg1757/REPORT.md`](opg1757/REPORT.md);
- [`erdos1083/PROGRESS.md`](erdos1083/PROGRESS.md).

## Recommended next action

1. Freeze a short KOU manuscript around the prime-wreath criterion, finite
   seed classification and order-128 theorem, with the \(J^9=0\)
   dimension-12 lower bound as a separately scoped theorem or companion
   section; complete the two blocked source audits before claiming novelty.
2. Replace the two complementary \(k=6,7\) finite signatures by a
   component-refining or external-partition-aware block rule, or prove a
   uniform Hall theorem; then supply recoverable tags, termination, and
   pairwise image separation.
3. Continue Erdős #1083 only in a varying-field/noncommensurable regime with
   explicit height, regulator, and popular-difference control; do not infer a
   rank threshold unless those constants are uniform.
