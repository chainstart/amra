# Independent audit of the conversion-round2 decisive lemma

Verdict: **pass, with all conditional boundaries retained**.

## M809C-05

For odd `n`,

\[
 \left\lfloor{n^2\over4}\right\rfloor={n^2-1\over4},\qquad
 e={n^2+3\over4},\qquad e-{n^2\over4}={3\over4}.
\]

Substitution into

\[
 \Phi(n,e)={e\over2}+{n\over2}\sqrt{e-{n^2\over4}}
\]

gives `Phi=e/2+n sqrt(3)/4`.  Hence

\[
 S_m=e-\binom{|B|}{2}-\Phi(n,e)
\]

has nonzero `sqrt(3)` coefficient `-n/4` for every integral `|B|` and
is irrational.  Since the cardinality of a finite unweighted set is an
integer, the universal M809C-05 statement is refuted exactly as written.
Weighted atoms or an integer rounded ledger are outside this refutation.

## M809C-08

Under the inherited rich-outer hypothesis, every mixed colour has one unique
high internal anchor; selecting it is injective by colour, and all selected
high edges belong to one pairwise-`C7`-compatible family.  As `I_mix` is an
integer, `I_mix>=ceil(Phi)` therefore gives at least `Phi` compatible edges of
distinct colours.  The direct subcase is valid.

The remaining inference does not follow from scalar bookkeeping.  At `n=14`,
`e=50`, `|B|=3`, one has `Phi=32` and `S_m=15`; the profile

```text
e(G[A_<q*])=8, I_mix=8, N_int=0, R_A=16
```

satisfies `R_A>S_m`, although both displayed positive channels are below
`Phi`.  This is only a logical counterprofile, not a graph-realizable
counterexample.  A graph-specific cross-channel theorem or a direct proof of
`R_A<=S_m` remains possible and necessary.

## M809C-11

For an explicitly constructed finite demand--carrier bipartite graph, let
`nu` be maximum matching size and

\[
 \delta=\max_{T\subseteq D}(|T|-|N(T)|).
\]

Every matching leaves at least `delta` demands unpaid.  Conversely, adjoining
`delta` universal dummy carriers makes every Hall inequality valid; Hall's
theorem gives a matching covering all demands, and deleting the dummies leaves
at most `delta` unpaid.  Thus

\[
 |D|-\nu=\delta.
\]

The checker exhaustively verified this equality on all 74,963 bipartite
graphs with at most four vertices on each side.  The three-demand/two-carrier
instance has rank two and deficiency one; one genuinely adjacent owned slack
carrier raises the rank to three.  Merely listing owners without legal arcs
does nothing.

Therefore Hall is an exact allocation theorem only after typed carriers and
legal arcs exist.  It creates neither and supplies no graph-specific expansion.

The standalone checker imports no author evidence and ran under 512 MiB and a
120-second timeout in 1.4 seconds, without Lean.  Its SHA-256 is
`e6e4004252d332989819f453ccdcdb5774b671ca42614583e6d5d93abec13ed6`.
Neither the public problem nor its `1/8` main term changes.
