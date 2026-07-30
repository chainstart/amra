# Next breakthrough target

## The only remaining resonant-translation candidate

Find a sequence of real translation sets \(A_n\), \(|A_n|=n\), and
parameter sets \(T_n\) for the actual SAT service

\[
X=-\frac32,\qquad Y=\frac{\sqrt{12285}}2,\qquad R=-3069,
\]

such that, with

\[
u(t)=\frac12(t+R/t)-X,\qquad c(t)=\frac12(t-R/t),
\]

one has

\[
\boxed{
\sum_{t\in T_n}r_{A_n}(u(t))
\bigl[r_{A_n}(c(t)-Y)+r_{A_n}(-c(t)-Y)\bigr]
\ge n^{12/5}.
}
\]

At overlap density \(\rho\), this requires

\[
|T_n|\ge \frac{n^{2/5}}{2\rho^2}.
\]

The construction must simultaneously avoid every known collapse:

- no bounded-degree number field with fixed fractional-ideal lattice;
- no common integer or ideal equation \(xy=N\) of norm \(n^{O(1)}\);
- no properization into \(O(\log n)\) independent Laurent frequencies;
- no generic union, whose gains are only \(n_i^2\)-weighted;
- no independent tensor, whose gains only add.

## Why this is the correct boundary

All audited alternatives are now subpolynomial:

- fixed fields: ideal divisors times a fixed-rank unit lattice;
- polynomial maps: constant, unless rational/Laurent;
- rational or commensurable multiplicative sets:
  \(\exp(\Theta(\log n/\log\log n))\);
- generic rank-two GAPs: only \((u,v)=(0,0),(3,0)\);
- the actual quadratic GAP \(\{i+jY\}\): average degree tends to \(4\).

Thus a breakthrough requires a growing-degree/growing-multiplicative-rank
set whose hyperbola image has unexpectedly low additive dimension.

## Next finite experiment

For degrees \(3\le d\le8\):

1. enumerate small irreducible defining polynomials and several short
   algebraic units;
2. enumerate bounded multiplicative words \(t\);
3. compute \(u(t)\) and \(c(t)\pm Y\) exactly in the compositum;
4. solve for the smallest proper GAP or union of GAPs containing these
   shifts;
5. score

   \[
   \mathcal S(A,T)=n^{-2}
   \sum_{t\in T}r_A(u(t))
   [r_A(c(t)-Y)+r_A(-c(t)-Y)];
   \]

6. reject any candidate admitting a common divisor normalization.

The first meaningful milestone is growth faster than every tested divisor
model, not merely a large maximum-degree star.  The publication threshold
is a certified family with \(\mathcal S(A,T)\ge n^\varepsilon\) for some
fixed \(\varepsilon>0\); the geometric campaign needs
\(\varepsilon\ge2/5\).

## Round 31 update

The single-unit experiment is complete.  Exact quotient-ring arithmetic
covered 104 sparse real unit fields of degrees 3–8 and every exponent
subset of \([-4,4]\).  A second search exhausted all 36 cubics and 122
quartics with interior coefficients bounded by 2, again over all 511
subsets.

The best multi-parameter ratio of certified nonbaseline gain to the
\(n^{2/5}\) target was \(6.19\times10^{-4}\), for

\[
f=x^4+x^2-1,\qquad e\in\{-4,-2,0,2,4\}.
\]

A fixed cyclic unit is now ruled out asymptotically: archimedean expansion
implies that only \(O_\theta(\log n)\) powers fit in a power-basis box of
size \(n\).

The next executable target is narrower:

1. select quartic fields with unit rank at least two;
2. enumerate two-unit words \(\varepsilon_1^a\varepsilon_2^b\);
3. compute a minimal nonrectangular GAP/union container for their images;
4. compare the weighted gain with the rectangular and divisor models.

Extending the exponent radius of one fixed unit cannot change the
asymptotic class.

## Round 32 update

The two-unit quartic sanity check is also negative.  Across 122 fields,
244 exact norm-\(\pm1\) unit pairs, and 118,584 rank-two word subsets, the
best elementary-shear target ratio was only

\[
1.459\times10^{-4}.
\]

The nonrectangular shear improved its rectangular score by about \(0.48\%\).
For each fixed field \(K\), rank \(r\) gives the asymptotic bound
\(O_K((\log n)^r)\).  Under the varying-field uniformity conditions below,
reaching the \(n^{2/5}\) target requires

\[
r\ge(2/5-o(1))\frac{\log n}{\log\log n}.
\]

For varying fields this coefficient is conditional: it requires uniform
height control and
\(\lambda_n=(\log n)^{-o(1)}\) for the shortest logarithmic unit.  A full
power-basis model with only the standard degree-dependent unit-height bound
gives the weaker safe coefficient \(1/5\).  Without height/container
uniformity, fixed-field counting gives no numerical coefficient.

The next target is no longer another fixed quartic experiment.  It is a
varying-field family—with growing rank only when the stated uniformity
conditions apply—together with an additive compression theorem or
construction showing that polynomially many unit-word hyperbola images fit
one size-\(n\) popular-difference container.

The immediate theoretical target is a uniform
height-versus-additive-container inequality, not another finite unit-word
enumeration.

The raw unit version is false.  For a root of
\(\prod_{k=1}^5(x+k)-1\), four independent units
\(\theta+1,\ldots,\theta+4\) lie in additive rank two.  Inversion restores
full rank in exact tests, so the revised target is the explicitly marked
inverse-symmetrized determinant conjecture in
`SYMMETRIZED_UNIT_CONTAINER_AUDIT.md`.

## Round 35 update

For the consecutive-unit family the finite rank observation has been
replaced by an exact identity.  With \(M=3069\), the coefficient minor on

\[
u_1,c_1,u_2,c_2,u_3,\ldots,u_{d-2}
\]

is

\[
(-1)^d4M^{d-2}\prod_{m=1}^{d-3}m!.
\]

This follows from the scaled Lagrange basis
\(q_k=\prod_{j\ne k}(x+j)\), not from numerical rank detection.  It forces
every proper integral container for these shifts to have
\(\exp(\Omega(d^2\log d))\) volume.  The explicit rectangular container
has matching \(\exp(O(d^2\log d))\) volume and \(n^{o(1)}\) doubling.

The family nevertheless fails the construction target for a decisive
reason: it has only \(d-1=n^{o(1)}\) certified parameters, versus the
required \(n^{2/5-o(1)}\).  Hence the next useful direction is not further
testing of \(\theta+k\).  It is either:

1. prove a comparable determinant lower bound for a polynomial-size
   unit-word set, thereby establishing the obstruction conjecture; or
2. find a structured word family in which most large minors collapse
   while all hyperbola images retain popular overlap in one common
   container.

Any candidate must be scored by parameter count and overlap multiplicity,
not merely by unit rank.
