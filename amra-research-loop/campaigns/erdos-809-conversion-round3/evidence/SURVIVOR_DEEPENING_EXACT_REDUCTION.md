# Round-three survivor deepening: exact rounding and creation boundary

## Exact rounding reduction

The outer residue `R_A` is an integer.  Therefore, for every real `S_m`,

\[
 R_A\le S_m\iff R_A\le\lfloor S_m\rfloor,
 \qquad
 R_A>S_m\iff R_A\ge\lfloor S_m\rfloor+1.
\]

For odd `n` at the public edge count, `S_m` is irrational, so equality with
an integer cannot occur.  The fractional remainder
`omega=S_m-floor(S_m)` cannot pay one integral demand and does not need to be
represented as a carrier.  Thus M809R3-01 deepens to one precise target:
construct `floor(S_m)` owned unit carriers, or prove the integer scalar gate
`R_A<=floor(S_m)` directly.  A weighted remainder provides no extra integral
capacity.

## Actual exchange exit

Let `X_G` be the graph-realizable low-edge/high-anchor exchange graph.  Its
arcs must preserve distinct colours and carry actual `C7` completion
certificates.  If

\[
 \nu(X_G)\ge\lceil\Phi(n,e)\rceil,
\]

the matched outputs give the direct colour exit.  This is the exact M809R3-05
target.  The round-two scalar counterprofile does not refute it because it
constructs no graph `G` and no exchange graph.  Conversely the scalar
inequality `R_A>S_m` supplies no lower bound on `nu(X_G)`; graph geometry is
indispensable.

## Carrier-creation boundary

For an explicit typed demand--carrier graph `C_G`, put

\[
 \delta(C_G)=\max_{T\subseteq D}(|T|-|N(T)|)=|D|-\nu(C_G).
\]

Exactly `delta` *universal* new carriers are necessary and sufficient to make
every demand payable.  Actual created carriers are not universal, so merely
creating `delta` objects is insufficient.  Their legal neighbourhoods must
satisfy every augmented Hall cut

\[
 |N_{C_G}(T)\cup N_Z(T)|\ge |T|.
\]

Equivalently, an alternating-path proof must end at genuinely unused actual
carriers often enough to raise matching rank to `|D|`.  Hall allocates these
outputs after creation; it does not prove reachability.  Nonreuse across
overlapping circuits remains part of M809R3-08, not a bookkeeping corollary.

## Conditional decisive interface

For every hard maximum-witness graph with
`R_A>=floor(S_m)+1`, it would suffice to prove one of:

1. the actual exchange rank is at least `ceil(Phi)`, giving the direct colour
   exit; or
2. a graph-derived alternating creation system supplies previously unused
   actual carriers whose legal neighbourhoods eliminate every Hall deficit,
   while one global owner map prevents reuse across circuits.

This is a typed conditional reduction, not the missing theorem.  Neither
alternative is proved for every hard graph, and composition with every public
branch is still absent.  Hence the `1/8` main term is unchanged.

The exact checker verified 122 odd-order rounding rows and all 74,963
bipartite graphs with at most four vertices per shore under a 5 GiB,
120-second limit in 1.6 seconds.  No Lean was used.
