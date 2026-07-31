# OPG-1757 breakthrough attack: final report

Date: 2026-07-31

## Strongest result

For every fixed deficit \(q\ge0\) and every beta offset
\(0\le r\le2q\), the cleared fixed-deficit numerator has exact degree
\[
\deg R_{q,r}=2q+r
\]
and exact positive leading coefficient
\[
[s^{2q+r}]R_{q,r}
=\frac4{q!}[z^r](1+2z+2z^2)^q>0.
\]
Consequently, for each fixed \(q\), the entire growing-depth layer
\[
B_{2s-5-q}(s,\beta)
\]
is strictly positive throughout its natural support for all sufficiently
large \(s\); coefficients below \(\beta^{2n}\) are structurally zero.
This is an arbitrary-fixed-\(q\) theorem, not another computed
\(q=7\) or \(q=8\) layer.

The proof has three new structural steps:

1. a marked exceptional-block subleading expansion valid for arbitrary
   weight, excess, and component count;
2. an exact second-difference/curvature formula across the
   \(h=0,1,2\) prescribed-edge endpoints;
3. a four-profile EGF collapse to the positive atom
   \((1+2z+2z^2)^q\).

The complete proof is in
`ALL_FIXED_DEFICIT_EVENTUAL_POSITIVITY_THEOREM.md`.

The coefficient-height reduction in
`LOGARITHMIC_GROWING_DEFICIT_WINDOW.md` gives a plausible conditional
upgrade: if its uniform height lemma is completed, then for some absolute
\(c_0>0\), every deficit
\[
q\le c_0\frac{\log s}{\log\log s}
\]
is simultaneously supportwise positive for all sufficiently large
\(s\).  Independent red-team review found the fixed-\(q\) theorem
proof-grade, but judged the present big-O size ledger insufficient to
claim this growing window unconditionally.

In addition, `ENDPOINT_POLYNOMIALITY_THEOREM.md` proves that every
normalized endpoint \(Q_{h,e,c}\) is a polynomial and hence that every
fixed-deficit denominator cancels:
\[
C_{q,r}\in\mathbb Q[s],\qquad s^r\mid R_{q,r},\qquad
\deg C_{q,r}=2q.
\]
The key observation is that the apparent two-marked path pole cancels
exactly against the Lagrange-inversion Jacobian; the remaining monomials
all have nonnegative \(s\)-valuation.

## Additional structural result

`TWO_MARKED_HYPERFOREST_EGF_LEMMA.md` gives a closed all-excess EGF for
the formerly incidence-enumerated \(h=2\) endpoint.  Its same-component
kernel is
\[
ab e^{(a+b)\Phi(T,u)}\frac{e^{uT}}{1-Te^{uT}}.
\]
This replaces every partition-of-excess list by a unique-path formula;
the accompanying polynomiality theorem controls its path pole exactly.

## Universal second symbol

`SECOND_SYMBOL_THEOREM.md` proves that the complete second Laurent symbol
is an \(A(z)^{q-2}\)-background times one explicit quartic local-defect
symbol, for every \(q\) and every offset.  The degree-four symmetrized
determinant collapse, five Poisson/Touchard moments, and all finite
certificates pass.  `LAURENT_DEGREE_LEMMA.md` supplies the formerly missing
filtered-ring proof that every relative order-\(k\) endpoint coefficient
has total profile degree at most \(2k\); the triangular endpoint
certificate and the second symbol are therefore all-parameter.

## Verification

The main ordinary certificate passes with digest
`cca70600865309db23389e5f584cf91d47a35a82e8348227afe199cdc36afbe0`.
The extended \(q=6\) regression passes with digest
`56fc206f63f3227d19dbcc358281d505241e914e9e03f75cda62298c6d5fd6e5`.
The two-marked EGF agrees with twelve independent primitive endpoints,
including the \(N=0\) boundary.  The
second-symbol theorem's extended certificate checks 216 endpoint Laurent
coefficients, exact cancellation of the apparent \(q=1\) denominator,
both extreme offsets through \(q=30\), and the exact degree-four Touchard
collapse.  The original
48-coefficient \(q\le6\) check remains as an independent discovery-path
regression.  The two unit tests pass.

## Remaining publication-critical gate

This attack proves the previously missing all-fixed-deficit asymptotic
theorem and reduces a logarithmically growing uniform window to one
explicit coefficient-height lemma.  It still does not
give polynomial/linear deficit width, the whole complete-split pooled
Rayleigh difference, or arbitrary-host OPG-1757.
The strongest next attack is a positive basis or a uniform root bound for
the resulting degree-\(2q\) polynomials, not another isolated fixed-\(q\)
computation.
