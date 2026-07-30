# Weighted labelled-C4 energy dichotomy

Date: 2026-07-30

## Purpose and outcome

`LABELLED_C4_ALGEBRA.md` proves that, after four radius pairs are frozen,
three adjusted squared-difference labels admit at most four fourth labels.
That distinct-label statement loses the multiplicity of actual point
rectangles.  This note installs the missing weight.

The correct weight is not the product of the four marginal cell
multiplicities.  It is the number of actual rectangles in one **signed
translation fibre**.  If \(q_\sigma\) is that number, then
\[
 Q=\sum_\sigma q_\sigma,\qquad
 J=\sum_\sigma q_\sigma^2
\]
are respectively the actual labelled-\(C_4\) count and its fibre collision
moment.  The main exact inequality is
\[
 \frac{Q^2}{P}
 \leq J
 \leq Q+m^2\max_i E_+(Z_i),                 \tag{1}
\]
where \(P=|\{\sigma:q_\sigma>0\}|\), every \(|Z_i|\leq m\), and
\(E_+(Z_i)\) is additive energy.

Thus a small occupied signed-label palette forces either a large common
translation fibre, which is direct endpoint reuse, or a height set of
near-maximal additive energy, where BSG/Freiman becomes applicable.
This is the strongest unconditional weighted dichotomy obtained in this
round.

It does not yield an exponent improvement at \(\eta=1/30\).  At that
endpoint the cross graph is exactly at its \(C_4\)-free KST scale.  An
explicit affine-plane/Latin construction has the exact campaign vertex and
edge proportions, is \(C_4\)-free, uses shared real arithmetic-progression
height sets, and uses only \(O(Um)\) genuine squared-distance cells.  It
therefore passes the quartic, representation and shared-\(Z\) interfaces.
The remaining theorem must use the paired origin of Gram-service cross
edges, or convert the additive/translation branch into global distance
expansion.

No unconditional distance-exponent improvement is claimed.

## 1. Actual signed fibres

Fix four radius classes.  Let \(Z_0,Z_2\) be the two hub height sets and
\(Z_1,Z_3\) the partner height sets, all of size at most \(m\).  Allow
arbitrary selected edge sets
\[
 {\cal E}_{01},\ {\cal E}_{21},\
 {\cal E}_{23},\ {\cal E}_{03}.
\]
An actual coordinate rectangle is a tuple
\[
 (a,c,z,d)\in Z_0\times Z_2\times Z_1\times Z_3
\]
whose four edges are selected.  Its signed shifts are
\[
\sigma=(s_{01},s_{21},s_{23},s_{03})
      =(a-z,c-z,c-d,a-d),                    \tag{2}
\]
and satisfy
\[
 s_{01}-s_{21}+s_{23}-s_{03}=0.             \tag{3}
\]

For a fixed compatible \(\sigma\), all four heights are determined by the
single translation coordinate \(a\):
\[
\begin{aligned}
 z&=a-s_{01},\\
 c&=a-s_{01}+s_{21},\\
 d&=a-s_{01}+s_{21}-s_{23}.                 \tag{4}
\end{aligned}
\]
Consequently its rectangle multiplicity \(q_\sigma\) is a selected subset
of the fourfold shifted intersection
\[
 Z_0\cap(Z_1+s_{01})
 \cap(Z_2+s_{01}-s_{21})
 \cap(Z_3+s_{01}-s_{21}+s_{23}),             \tag{5}
\]
and
\[
 q_\sigma\leq m.                             \tag{6}
\]
For unsigned squared labels there are only constantly many sign branches.
Using signed fibres removes that harmless constant and makes (4) exact.

Let
\[
 Q=\sum_\sigma q_\sigma,\quad
 J=\sum_\sigma q_\sigma^2,\quad
 P=|\{\sigma:q_\sigma>0\}|.                  \tag{7}
\]
Then Cauchy and (6) give
\[
 \frac{Q^2}{P}\leq J\leq mQ.                 \tag{8}
\]

## 2. Fibre collisions inject into common differences

For \(h\in\mathbb R\), write
\[
 r_i(h)=|\{(x,x')\in Z_i^2:x-x'=h\}|.
\]
Define the fourfold common nonzero-difference energy
\[
 {\cal D}_4(Z_0,Z_1,Z_2,Z_3)
 =\sum_{h\ne0}\prod_{i=0}^3r_i(h).           \tag{9}
\]

### Theorem 1 (weighted labelled-cycle inequality)

For arbitrary selected edge sets as above,
\[
 J-Q\leq {\cal D}_4(Z_0,Z_1,Z_2,Z_3)
 \leq
 m^2\prod_{i=0}^3 E_+(Z_i)^{1/4}
 \leq m^2\max_iE_+(Z_i).                    \tag{10}
\]
In particular,
\[
 \boxed{\quad
 \max_iE_+(Z_i)
 \geq
 \frac{Q^2/P-Q}{m^2}
 \quad}                                      \tag{11}
\]
whenever the numerator is positive.

### Proof

The quantity
\[
 J-Q=\sum_\sigma q_\sigma(q_\sigma-1)
\]
counts ordered pairs of distinct rectangles in the same signed fibre.
By (4), two such rectangles differ by one nonzero translation \(h\) in
all four height classes.  Sending the pair to its four ordered endpoint
pairs gives an injection into the tuples counted by
\(\prod_i r_i(h)\).  This proves the first inequality in (10).  It is an
equality for complete four-block graphs.

Hölder gives
\[
 {\cal D}_4
 \leq\prod_i\left(\sum_h r_i(h)^4\right)^{1/4}.
\]
Since \(r_i(h)\leq m\),
\[
 \sum_h r_i(h)^4
 \leq m^2\sum_h r_i(h)^2
 =m^2E_+(Z_i).
\]
Multiplication proves the second inequality in (10); the third is
immediate.  Combining (10) with the Cauchy lower bound in (8) proves
(11). \(\square\)

### Corollary 2 (usable dichotomy)

For any threshold \(R\geq1\), one of the following holds:

1. some signed label fibre has \(q_\sigma\geq R\), so the four height sets
   contain a common translated selected subset of size \(R\);
2. the occupied signed-label palette satisfies \(P>Q/R\).

Moreover, if
\[
 \frac{Q^2}{P}-Q\geq\frac{m^5}{K},           \tag{12}
\]
then some height set satisfies
\[
 E_+(Z_i)\geq\frac{m^3}{K}.                 \tag{13}
\]
This is the standard near-maximal-energy regime in which BSG gives a large
subset with small doubling and Freiman theory places that subset in a
bounded-rank progression, with losses polynomial in \(K\).

The conclusion of the first branch is endpoint reuse, not automatically
additive structure.  The counterexample in Section 4 shows this distinction
is necessary.

## 3. Why products of marginal multiplicities are invalid

Let
\[
 \nu_{ij}(s)
 =|\{(x,y)\in{\cal E}_{ij}:x-y=s\}|.
\]
Forgetting endpoint incidence produces the marginal cocycle energy
\[
 {\cal W}
 =
 \sum_{s_{01}-s_{21}+s_{23}-s_{03}=0}
 \nu_{01}(s_{01})\nu_{21}(s_{21})
 \nu_{23}(s_{23})\nu_{03}(s_{03}).           \tag{14}
\]
Every actual rectangle contributes to \({\cal W}\), but the converse is
false: the four independently chosen edges need not share endpoints.

Analytically,
\[
 {\cal W}
 =
 \langle\nu_{01}*\nu_{23},
         \nu_{21}*\nu_{03}\rangle,
\]
so Cauchy forces a large additive convolution energy when \({\cal W}\) is
large.  This is an energy of independent edge representations, not the
point-conditioned rectangle moment needed by the proof.

The translation construction below has \(r\) actual rectangles but
\({\cal W}=r^4\).  Therefore no argument may replace \(Q\) or \(J\) by a
product of the four cell representation counts without proving an endpoint
gluing lemma.  The signed fibre \(q_\sigma\) is precisely that gluing
statistic.

## 4. Translation-fan pressure test

Let \(X\) be any \(r\)-element real set and choose four constants
\(\alpha_i\).  Put
\[
 Z_i=X+\alpha_i.
\]
For each \(x\in X\), retain only the four edges of the rectangle formed by
\[
 x+\alpha_0,\quad x+\alpha_2,\quad
 x+\alpha_1,\quad x+\alpha_3.
\]
The graph is a disjoint union of \(r\) coordinate rectangles.  All
rectangles have the same signed shift vector, so
\[
 Q=r,\qquad P=1,\qquad J=r^2,\qquad
 {\cal W}=r^4.                               \tag{15}
\]

Choose \(X=\{1,2,4,\ldots,2^{r-1}\}\).  Its nonzero ordered differences are
all distinct, and
\[
 E_+(X)=2r^2-r,                              \tag{16}
\]
the minimum-order additive energy.  Thus even a maximal fibre
\(q_\sigma=r\) does not imply \(E_+(Z_i)\gg r^{3-o(1)}\).  What it does
give is the exact common translated subset (5), which must be routed into
an endpoint-reuse or common-anchor theorem.

This example also shows why (10) is sharp at low energy:
\[
 J-Q=r(r-1)={\cal D}_4.
\]

## 5. Complete-AP pressure test

Now take
\[
 Z_0=Z_1=Z_2=Z_3=\{0,1,\ldots,m-1\}
\]
and retain all four complete bipartite blocks.  Then
\[
 Q=m^4,\qquad
 E_+(Z_i)=\frac{2m^3+m}{3}.                 \tag{17}
\]
For a signed fibre, (5) is an interval intersection.  All its translations
are retained, so the first inequality in (10) is an equality:
\[
 J-Q
 ={\cal D}_4
 =2\sum_{k=1}^{m-1}(m-k)^4
 =\left(\frac25+o(1)\right)m^5.              \tag{18}
\]
There are \(P=\Theta(m^3)\) occupied signed fibres and the largest fibre
has size \(m\).

This is the high-energy branch of Theorem 1.  It simultaneously saturates
the shared height capacity, the \(m^4\) point-rectangle count, the
\(\Theta(m^3)\) signed-label palette and the \(m^5\) fibre collision
moment.  Hence the powers in (10)--(13) cannot be improved in general.

The verifier at \(m=7\) obtains
\[
 Q=2401,\quad P=1105,\quad J=6951,\quad
 J-Q={\cal D}_4=4550,\quad E_+(Z)=231.
\]

## 6. Exact near-KST stability

Let a bipartite graph have hub side \(H\), partner side \(N\), sizes
\[
 |H|=h,\qquad |N|=n,
\]
and \(E\) edges.  For \(y\in N\), write \(d_y\) for its degree.  In a
\(C_4\)-free graph every hub pair has codegree at most one.  Let
\(\Delta\) be the number of hub pairs with no common partner, and put
\[
 {\cal V}=\sum_{y\in N}\left(d_y-\frac En\right)^2.
\]

### Lemma 3 (exact C4-free stability identity)

Every \(C_4\)-free bipartite graph satisfies
\[
 \boxed{\quad
 {\cal V}+2\Delta
 =
 h(h-1)-\frac{E^2}{n}+E.
 \quad}                                      \tag{19}
\]

### Proof

Because codegrees are zero or one,
\[
 \binom h2-\Delta=\sum_y\binom{d_y}{2}.
\]
Also
\[
 \sum_y d_y^2=\frac{E^2}{n}+{\cal V}.
\]
Substitution and multiplication by two give (19). \(\square\)

Thus a \(C_4\)-free graph close to \(E=h\sqrt n\) must be close to a
pairwise-balanced block design: partner degrees have small variance and
almost every hub pair lies in exactly one partner neighbourhood.  This is
the minimal precise near-KST conclusion available without further
geometry.  It does not itself contradict the campaign, as the next
construction shows.

## 7. Latin/transversal design obstruction with real cells

Let \(q\) be prime and \(1\leq U\leq q\).  Define
\[
\begin{aligned}
 H&=\{(s,x):s\in\{0,\ldots,U-1\},\ x\in\mathbb F_q\},\\
 N&=\{(p,b):p,b\in\mathbb F_q\},
\end{aligned}
\]
and join \((s,x)\) to \((p,b)\) when
\[
 x=ps+b\pmod q.                             \tag{20}
\]
Every partner has degree \(U\).  Two hubs in distinct \(s\)-groups have
one common partner, while two in the same group have none.  Therefore
\[
\begin{aligned}
 h&=Uq, & n&=q^2, & E&=Uq^2=h\sqrt n,\\
 C_4(G)&=0, &
 \Delta&=U\binom q2, & {\cal V}&=0.          \tag{21}
\end{aligned}
\]
Equation (19) holds with equality term by term.  This is a transversal
design, equivalently \(U\) parallel classes of the affine-plane/Latin
construction.

It also admits the exact real cell interface.  Give every hub and partner
radius class the real height set
\[
 Z=\{0,1,\ldots,q-1\}.
\]
Place the partner radius indices after the hub indices and choose geometric
radii \(R_j=B^j\), with \(B\) sufficiently large.  An edge in block
\((s,p)\) has the full cell label
\[
 \left(
 s+p_{\rm index},
 (R_s-R_{p_{\rm index}})^2+(x-b)^2
 \right).                                   \tag{22}
\]
For fixed \(s,p\), let \(r\) be the ordinary representative of \(ps\bmod
q\).  Equation (20) gives
\[
 x-b\in\{r,r-q\}.                            \tag{23}
\]
Thus every radius block uses at most two genuine squared-distance cells,
and the whole graph uses at most
\[
 2Uq                                           \tag{24}
\]
cells.  A sufficiently large \(B\) separates radial offsets belonging to
different blocks with the same product index.  Each cell has at most \(q\)
representations.  All shared height sets have the maximal-order AP energy
\[
 E_+(Z)=\frac{2q^3+q}{3}.                   \tag{25}
\]

This construction is not asserted to arise from the full paired
Gram-service selection.  It is an exact counterexample to every proposed
lemma using only:

1. the two coordinate-side capacities;
2. edge density at the KST scale;
3. real shared height sets of capacity \(m\);
4. genuine geometric radius/product and squared-distance cell labels;
5. a small cell universe and the quartic rule on existing \(C_4\)'s.

The quartic condition is vacuous because there are no \(C_4\)'s.  The
construction returns the high-additive-energy branch, showing exactly what
an anti-Latin theorem would have to exploit.

## 8. The \(\eta=1/30\) ledger

At the campaign endpoint,
\[
\begin{aligned}
 m&=L, & U&=L^{9/10},\\
 h=Um&=L^{19/10}, & n=Lm&=L^2,\\
 E_{\rm forced}&=L^{29/10-o(1)},&
 h\sqrt n&=L^{29/10}.
\end{aligned}                               \tag{26}
\]
There is zero power surplus over KST.  Hence no positive power lower bound
for \(Q\) follows.  The Latin model realizes every exponent in (26), has
no coordinate \(C_4\), and uses only
\[
 O(Um)=L^{19/10}
\]
cells, below the allowed
\[
 M\leq L^{27/10+o(1)}.                       \tag{27}
\]

For an deliberately optimistic comparison only, suppose an additional
constant-factor supersaturation supplied the natural
\[
 Q=L^{2(19/10)+o(1)}=L^{19/5+o(1)}.          \tag{28}
\]
and suppose this count could be placed in one frozen radius quartet, or
that Theorem 1 could be summed over quartets without loss.  Neither is
currently proved.  There are up to \(U^2L^2=L^{19/5}\) radius quartets, so
naive freezing can consume the entire count.  The following palette ledger
is therefore a best-case lower bound on the actual gap.

The rich-cell endpoint-reuse target from the preceding round is
\[
 R=L^{1/5-o(1)}.
\]
Corollary 2 would force such a fibre only if the occupied signed palette
obeyed
\[
 P\leq Q/R=L^{18/5+o(1)}.                   \tag{29}
\]
The current bounds are
\[
 P\leq 8M^3=L^{81/10+o(1)}
\]
globally, or merely \(P\leq O(m^6)=L^6\) after four blocks are frozen.
Their gaps above (29) are respectively
\[
 L^{9/2+o(1)}
 \quad\hbox{and}\quad
 L^{12/5+o(1)}.                              \tag{30}
\]

To force near-maximal additive energy from (11), one needs
\[
 Q^2/P\gtrsim m^5.
\]
Under the hypothetical (28), this requires
\[
 P\leq L^{13/5+o(1)},                        \tag{31}
\]
even stronger than (29).  Thus the weighted inequality is sharp but the
available palette control misses its useful range by several powers.

If the edge count had a power surplus \(L^\sigma\) over KST, standard
codegree convexity would give
\[
 Q\gtrsim L^{19/5+4\sigma-o(1)}.
\]
At \(\eta=1/30\), however, \(\sigma=0\); this formula cannot be invoked.

## 9. Strongest correct conditional theorem and minimum gap

The unconditional theorem produced in this round is (1), together with
the exact endpoint-reuse/additive-energy alternatives (12)--(13).  It is
sharp on both the AP and arbitrary-translation models.

The \(C_4\)-free branch has the exact stability identity (19).  Therefore
the smallest useful next geometric statement is an **anti-transversal
inverse theorem**:

> For cross edges that retain their pairing by original Gram services, an
> approximate pairwise-balanced neighbourhood design at the scale (26)
> either expands the global cell universe beyond \(L^{27/10+o(1)}\), or
> produces a common-translation/additive-height component which reconnects
> to the anchor-coherent endpoint-reuse theorem.

Both conclusions are necessary.  The Latin model rules out the first
conclusion from the coordinate graph alone, while the AP and translation
models show that the structured second conclusion cannot simply be called
negligible.

Quantitatively, even granting \(Q=L^{19/5}\), the missing coloured-palette
gain for endpoint reuse is \(L^{12/5}\) after freezing four blocks
(\(L^{9/2}\) from the global \(M^3\) bound).  Before that palette gap is
relevant, one must first defeat the zero-surplus Latin branch at KST.  This
best-case ledger also suppresses the possible \(U^2L^2=L^{19/5}\)
radius-quartet freezing loss.  These are the minimum remaining
obstructions; the labelled quartic by itself has been fully exploited.
