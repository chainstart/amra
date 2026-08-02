# Erdős #809 — the Ramsey label invariant needs a reserve coordinate

Date: 2026-08-02

Status:
`PROVED_TRANSFER_OBSTRUCTION_AND_EXPLICIT_RESERVE_PAYMENT__PUBLIC_PROBLEM_OPEN`

## 1. The mechanism being tested

The multicolour-triangle result in `openai/ten-proofs` does not propagate
triangle-freeness alone.  At recursive stage \(j\), it maintains the
strictly stronger invariant

\[
  \chi(\Gamma_j(\gamma))\le j+1
\]

for every colour graph.  A palette records which colours are absent and a
proper label of each active colour graph; a saturated coordinate-cover map
then forces two cross edges of the same colour to land in one old label
class.  The relevant formal interfaces are `Colorable`,
`paletteBlockLabel_valid`, and the two same-label lemmas in
`MulticolorTriangleRamsey.lean` at snapshot
`94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`.

This note tests the literal transplant to the \(L_4(2)\) normal form and
then to the sharp equality cores of the maximum-witness B-opposite
reduction for Erdős #809.  The result is negative but exact: the strongest
possible constant version of the colour-label bound, namely two labels and
maximum colour degree one, already follows automatically for *every*
rainbow-\(C_7\) colouring in the normal form.  Sharp noninjective cores
show that this automatic invariant does not settle the defect.  The
missing coordinate is genuine reserve incidence.

## 2. The sharp endpoint family

Fix \(g\ge4\).  For the even and odd rows respectively put

\[
\begin{array}{c|ccc}
 &\delta&\kappa&n\\ \hline
 \mathrm{even}&g^2-2g-2&2g-2&2g^2-2g-6\\
 \mathrm{odd}&g^2-2g-1&2g-1&2g^2-2g-3.
\end{array}
\]

Let \(P,U\) be disjoint sets of size \(\delta\), add vertices \(b,c\),
and let \(W\) have size \(\kappa-2\).  Make

- \(P\cup\{b\}\) and \(U\cup\{c\}\) cliques;
- \(P\) anticomplete to \(U\);
- \(b\) anticomplete to \(U\cup W\cup\{c\}\) and \(c\) anticomplete to
  \(P\cup W\cup\{b\}\);
- each \(w_i\in W\) adjacent to a consecutive cyclic interval of
  \(\Delta=\delta+g\) vertices in the cyclic order \(P,U\).

The already blind-audited endpoint theorem proves that these graphs have

\[
 e(G)=\lfloor n^2/4\rfloor+1,\qquad
 \delta(G)=\delta,\qquad \Delta(G)=\delta+g,
\]

and, for \(g\ge5\), satisfy \(L_4(2)\).  Every \(w\in W\) is a maximum
witness and has at least \(g\) neighbours in each of \(P,U\).

Fix one such witness \(v\), put \(A=N[v]\), and choose distinct

\[
 x_1,\ldots,x_g\in A\cap P,\qquad
 y_1,\ldots,y_g\in A\cap U.
\]

Give the two edges \(bx_i,cy_i\) the common fresh colour \(\gamma_i\),
and give every remaining edge its own fresh colour.

## 3. Exact label-complexity obstruction

### Theorem 3.1 (automatic two-label theorem)

Let \(G\) satisfy \(L_4(2)\) and \(\delta(G)\ge3\), and suppose every
\(C_7\) in an edge-colouring of \(G\) is rainbow.  Then every colour graph
is an **induced matching** (distinct edges of one colour have neither a
common endpoint nor a cross edge).  In particular, for every colour
\(\gamma\),

\[
 \Delta(\Gamma(\gamma))\le1,\qquad
 \operatorname{degen}(\Gamma(\gamma))\le1,\qquad
 \chi(\Gamma(\gamma))\le2.
\]

#### Proof

Take two distinct edges of one colour.  If they share a vertex, choose at
the other endpoint an extra neighbour (possible because
\(\delta(G)\ge3\)); an exact four-edge path avoiding the shared vertex and
one other endpoint completes the two equal-colour edges to a \(C_7\).
If the two edges are disjoint but some endpoint of one is adjacent to an
endpoint of the other, use \(L_4(2)\) after deleting those two adjacent
endpoints to join the two remaining endpoints by an exact four-edge path.
Again the three displayed edges and the path form a \(C_7\).  Both cases
contradict rainbow-\(C_7\), so two equal-colour edges are vertex-disjoint
and have no cross adjacency.  In particular the colour graph is an
induced matching.  Orient each matching edge arbitrarily and label its two
endpoints zero and one; isolated vertices receive either label.  This is
a proper two-labeling.  \(\square\)

### Lemma 3.1a (the label state has a full edge-flip gauge)

Let one colour graph contain \(t\) nonempty matching edges, oriented from
their inner endpoints to their outer endpoints.  On the incident vertices
it has exactly \(2^t\) proper labelings by \(\{0,1\}\): each edge may be
flipped independently.  Moreover, the resulting word of labels on the
\(t\) outer endpoints ranges over all of \(\{0,1\}^t\).

Indeed, choosing the outer label on each edge arbitrarily forces, and is
forced by, the opposite label on its inner endpoint.  Thus existential
two-labelability forgets a complete \(t\)-bit gauge coordinate.  A root,
orientation, or deficient subfamily chosen after these flips cannot be an
invariant of the colour class.  Any useful palette transfer must therefore
fix the gauge by a rule shared across colours or blocks before the Hall
family is exposed.

Thus the literal Lean colourability state used by the triangle-Ramsey
recursion is not merely weak on #809's sharp examples: with two labels, it
is already a free consequence of the standing normal-form hypotheses.

### Theorem 3.2 (two-label sharp-core stress theorem)

For every \(g\ge4\) and each parity row, the colouring above has the
following properties.

1. Every \(C_7\) is rainbow.
2. Exactly \(g\) colours are repeated, and every repeated colour graph is
   \(2K_2\).  Every other nonempty colour graph is \(K_2\).
3. Every colour graph has maximum degree at most one, degeneracy at most
   one, arboricity at most one, and chromatic number at most two.
4. There is an explicit proper two-labeling for every repeated colour:
   label \(b,c\) by zero and \(x_i,y_i\) by one.
5. Relative to \(A=N[v]\), the good-edge defect is exactly
   
   \[
      D_B=\sum_\gamma (t_\gamma-1)_+=g.
   \]

#### Proof

Items 2--4 are immediate from the definition: the two edges in a repeated
class have four distinct endpoints, and both join its zero label class to
its one label class.  Singleton classes satisfy the same numerical bounds.
Here \(b,c\notin A\) while \(x_i,y_i\in A\), so both members of every
doubled class are good cross edges and \(t_{\gamma_i}=2\).  The \(g\)
doubled classes save exactly one colour each, proving item 5.

It remains to check item 1.  Removing the two \(\gamma_i\)-edges from a
hypothetical seven-cycle leaves two internally disjoint paths whose total
length is five.  Up to reversal, their endpoint pairing is either

\[
  (b,c),(x_i,y_i)
  \quad\hbox{or}\quad
  (b,y_i),(x_i,c).
\]

For the first pairing, \(d(b,c)\ge4\): a three-edge path would have type
\(b-P-U-c\), contrary to \(P\perp U\).  Also
\(d(x_i,y_i)\ge2\).  For the crossed pairing, each distance is at least
three: \(N(b)=P\) has no common neighbour with \(y_i\in U\), and the
symmetric assertion holds for \(x_i,c\).  Thus either pairing requires at
least six remaining edges, not five.  No \(C_7\) contains both edges of a
repeated class.  Since these are the only repeated colours, every
\(C_7\) is rainbow.  \(\square\)

For \(g\ge5\), the previously audited endpoint construction also has
\(L_4(2)\), so these rows are genuine noninjective stress examples inside
the hypotheses of Theorem 3.1.  The \(g=4\) rows are retained only as
graph-and-colouring certificate boundary cases; no \(L_4(2)\) claim is
made for them here.

### Corollary 3.3 (literal Ramsey invariant is non-separating)

No argument whose only colour-class input is a uniform proper-label bound
\(\chi(\Gamma(\gamma))\le h\), even with \(h=2\), adds any restriction to
the \(L_4(2)\) normal form.  In particular it cannot by itself eliminate
the parity-sharp B-opposite equality cores or force their colouring to be
injective.

This is a statement about the proposed transfer interface, not an
impossibility theorem for all uses of palettes.  The ten-proofs recursion
also controls how labels agree across blocks; an #809 analogue must retain
such incidence data rather than only the chromatic number.

## 4. The missing reserve coordinate

Let \(B=V(G)\setminus A\).  The union of missing \(B\)-pairs incident to
the two zero-shore vertices is

\[
 \mathcal Q_{b,c}
 =\{bz:z\in B\setminus\{b\},\ bz\notin E\}
  \cup
  \{cz:z\in B\setminus\{c\},\ cz\notin E\}.
\]

The common missing pair \(bc\) is counted once.  Direct substitution gives

\[
 |\mathcal Q_{b,c}|
 =\delta+2\kappa-g-5
 =\begin{cases}
   g^2+g-11,&n\text{ even},\\
   g^2+g-8,&n\text{ odd}.
  \end{cases}
\]

This is at least \(g=D_B\).  Therefore enumerating
\(\mathcal Q_{b,c}\) and assigning its first \(g\) distinct pairs to
\(\gamma_1,\ldots,\gamma_g\) gives a literal injection

\[
 \{\gamma_1,\ldots,\gamma_g\}\hookrightarrow\mathcal Q_{b,c}.
\]

The equality cores are thus not hard reserve-failure configurations.  In
ten-proofs language, the proper labels are only the recursive state; the
reserve injection is the conserved resource which pays every attempted
reuse.

### Exact next interface

The useful transferred target is not
\(\chi(\Gamma(\gamma))=O(1)\).  It is a *label--reserve Hall system*:
for each repeated colour \(\gamma\), define from its oriented proper labels
a set \(\mathcal Q_\gamma\) of legal missing-pair tokens, and prove

\[
 \left|\bigcup_{\gamma\in S}\mathcal Q_\gamma\right|\ge |S|
 \qquad\text{for every set }S\text{ of hard repeated colours}. \tag{LRH}
\]

Then Hall's theorem pays every repeated colour by a distinct actual
reserve token.  The present construction satisfies (LRH) in the maximally
overlapping form \(\mathcal Q_\gamma=\mathcal Q_{b,c}\).  The unresolved
work is to derive the legal token sets canonically for different zero
shores and to absorb the residual Branch A and B-same mass.  Cardinality
of one global reserve union alone does not supply those incidences.

This Hall formulation is not being claimed as new here: it is exactly the
success alternative in the earlier reserve--Hall theorem for #809, with
\(\mathcal K(e)\) as the legal-token set of a zero-shore base pair.  The
ten-proofs transfer sharpens the next move.  The failed Hall alternative
should be encoded by fixed endpoint-label words *before* a deficient
subfamily is selected, after the model of the saturated coordinate-cover
matrix.  One then seeks either reserve expansion or a bounded exceptional
word set which collapses to the already isolated coherent-star branches.
Choosing labels after seeing the deficient family would be tautological,
just as choosing a saturated-matrix row after seeing the word pair is
tautological in the Ramsey proof.

## 5. Executable certificate and firewall

`verify_palette_reserve_transfer.py` independently rebuilds both parity
families, checks the exact edge and degree ledgers, constructs all doubled
colour classes and their proper two-labelings, verifies the two distance
pairings excluding a repeated-colour \(C_7\), enumerates the actual
missing-star reserve, and constructs the injection.  It also enumerates the
full \(2^t\) edge-flip gauge for \(0\le t\le10\).  The regression test checks
34 parameter rows through \(g=20\).

This theorem does **not** prove or refute Erdős #809.  It proves that one
prominent ten-proofs invariant is insufficient when stripped of its
cross-block agreement/resource coordinate, and it specifies the literal
coupled invariant which a successful transfer must establish.
