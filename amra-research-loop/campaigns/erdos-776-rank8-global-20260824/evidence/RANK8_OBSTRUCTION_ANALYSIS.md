# Rank-8 obstruction analysis for Erdős #776

## Frozen interfaces

The public closure target is the exact threshold `n_0(r)`, including both
existence for every larger order and a sharp lower obstruction.  The present
colex route has the shortened defect orbit

\[
 D_{V-12}=0,\qquad D_{q-1}=V+\operatorname{KK}_q(D_q),       \tag{1}
\]

and the inherited exact implication

\[
 D_8<{V-11\choose8}\quad\Longrightarrow\quad
 D_2\le {V-9\choose2}.                                  \tag{2}
\]

On the proved two-term rank-eight chart,

\[
 D_8={V-12\choose8}+{V-13\choose7}+W_6,                 \tag{3}
\]

so the only open entry in this route is

\[
 W_6<{V-13\choose6}.                                    \tag{4}
\]

Equations (1)--(4) do not determine `n_0(r)`.  Even an all-`V` proof must be
composed with the inherited antichain construction and parameter map.  That
would improve the upper term, of the recorded `2r+5` type; exact threshold
closure would still require a matching lower boundary and small-`r` audit.

## Where inherited approaches lose the needed information

### Two-binomial domination is a gate, not an invariant

Put

\[
 P_q={V-12\choose q}+{V-13\choose {q-1}}.
\]

At `V=288`, exact canonical arithmetic gives

\[
 D_{18}-P_{18}=-2,924,809,
 \qquad D_{16}-P_{16}=67.                               \tag{5}
\]

Thus the successful rank-18 zero-slack condition is not preserved literally
at every lower rank.  The proved fixed-depth residual theorem survives; a
proof that treats `P_q` itself as a barrier does not.

### Independent-tax subadditivity destroys the overlap credit

The first `+V` tax at `V=40`, shadowed independently from rank 27 to rank 8,
contributes exactly

\[
 {28\choose8}+{27\choose7}=3,996,135,                  \tag{6}
\]

the two-term baseline in (3).  The very next independently shadowed tax
contributes `2,877,875`, while the entire residual capacity in (4) is only

\[
 {27\choose6}=296,010.                                 \tag{7}
\]

Hence a union bound or termwise subadditive decomposition overspends the
rank-six reservoir after only two taxes.  Recompression is not a technical
detail: common-prefix overlap is the source of essentially the whole gain.

### Blind adjacent coupling loses a full rank

Compare the `V` and `V+1` orbits at their first common rank.  A blind
subadditive coupling starts the difference at `V+1` and shadows it separately.
Even if every later `+1` tax is discarded, at rank eight it gives

\[
 {V-11\choose8}+{V-12\choose7}.                        \tag{8}
\]

The increment permitted by the target cap is only

\[
 {V-11\choose7}.                                       \tag{9}
\]

At `V=40`, (8) is `5,476,185`, whereas (9) is `1,560,780`.
Any viable adjacent proof must cancel the common canonical prefix before
shadowing the suffix difference.

### The raw residual is not monotone

Exact values give

\[
 W_6(41)-W_6(40)=-8,905,
 \qquad W_6(51)-W_6(50)=2.                             \tag{10}
\]

Thus neither direction of scalar monotonicity can be an induction invariant.
The open candidates are the margin, the normalized ratio, or a canonical
suffix-height potential.

### Finite carry charts do not close the universal parameter

The independent verifier scans `40<=V<=500`, and checks (4) throughout.
It finds no failure of the three current survivor candidates: positive cap
increment, nonincreasing normalized ratio, and logarithmic rank-six top.
This is falsifier evidence only.  New carry walls may occur for unbounded
`V`, so no finite chart or larger cutoff is promoted.

## Required new information

The rank-eight route now needs one of the following, with full integer
quantifiers:

1. an overlap-aware adjacent shadow theorem controlling the **suffix** jump
   after the two common harmonic terms cancel;
2. a carry-height theorem proving that the top index of the six-canonical word
   of `W_6` grows only logarithmically;
3. an independent global construction that bypasses (1), together with its
   exact `r,n` parameter map.

For the public threshold, one additionally needs a lower-bound mechanism
that meets the construction.  The residual full-rank antichain at
`n=2r+5` remains a logically separate boundary problem and is not resolved by
rank-eight entry.
