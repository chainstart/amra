# Anchor-coherence extraction audit

Date: 2026-07-30

## Purpose

`ITERATED_PARTNER_REUSE_NETWORK.md` proves a strong global bound when all
hub witnesses use one common height anchor.  This note asks whether such a
subnetwork can be extracted from the low--low overlap mass
\[
 {\cal D}_{\rm low,low}
 \gtrsim L^{10/3-\eta-o(1)}. \tag{1}
\]

The answer from the currently retained marginals is negative.  Every direct
pigeonhole, dyadic, dependent-random-choice or BSG cleaning loses a fixed
power more than is available.  A finite Latin-square tensor makes this
failure exact: it has the required union, overlap and joint-moment scales,
but distributes the services uniformly over hub-anchor pairs, with
multiplicity one per pair and no common numerical anchor between hubs.

This is a strict barrier to extraction from the known marginal data.  It is
not a full Euclidean counterexample: it does not impose the same partner
height set in every product fibre.  The first additional identity capable
of detecting that omission is a representation-level Gram rectangle,
\[
\begin{aligned}
 &Q(P,N)+Q(P',N')-Q(P,N')-Q(P',N)\\
 &\hspace{2cm}=2(P-P')\mathbin{\cdot}(N'-N). \tag{2}
\end{aligned}
\]
Thus the next input must count point-representation rectangles, or an
equivalent anchor-conditioned triangle moment.  Value-level overlap and
triangle marginals do not suffice.

No unconditional exponent improvement is claimed.

## 1. How much coherent mass is needed?

Write
\[
 S=L^{10/3-\eta-o(1)}
\]
for the low--low service mass.  The anchor-coherent theorem bounds a
coherent subnetwork by
\[
 O(L^2U+L^3)=O(L^3), \tag{3}
\]
because \(U\leq L\).  Consequently an extraction must retain at least
\[
 \theta S\gg L^3,\qquad
 \theta\gg L^{-1/3+\eta+o(1)}. \tag{4}
\]
This is the exact retention threshold.

The hub concentration audit permits
\[
 L^{2/3-\eta/2-o(1)}
 \lesssim U
 \lesssim L^{5/6+2\eta+o(1)}. \tag{5}
\]
There are \(Um\asymp UL\) hub-coordinate vertices and \(U^2m^2\) ordered
hub-coordinate pairs.  Pigeonholing (1) gives only
\[
\begin{aligned}
 \max_{(u,a)}\deg(u,a)
 &\gtrsim \frac{S}{Um},\\
 \max_{(u,a),(x,c)}\operatorname{mult}((u,a),(x,c))
 &\gtrsim \frac{S}{U^2m^2}. \tag{6}
\end{aligned}
\]
At the lower endpoint \(U=L^{2/3-\eta/2}\), these are respectively
\[
 L^{5/3-\eta/2}
 \quad\hbox{and}\quad
 1. \tag{7}
\]
The first is far below \(L^3\); the second has no power at all.

More fundamentally, fixing one coordinate \((u,a)\) also fixes its hub
index \(u\).  It does not produce the common numerical height \(A\) across
many hub indices required by the additive state.  Different real height
sets \(Z_u\) may be disjoint, so services with \(a=c=A\) may be absent.

## 2. Random anchor selection and buckets

Choose \(r\) of the \(m\) anchors at every hub.  Independent uniform
selection retains a service with probability
\[
 \left(\frac rm\right)^2. \tag{8}
\]
Even if the resulting subnet were coherent, (4) would require
\[
 r\gtrsim L^{5/6+\eta/2-o(1)}. \tag{9}
\]
Thus one must retain almost the whole height set, not a bounded-rank core.

Equivalently, partition every hub set into \(K\) balanced buckets.  The
largest ordered bucket pair is guaranteed only \(S/K^2\) services.  To
cross (3), one needs
\[
 K\lesssim L^{1/6-\eta/2+o(1)},\qquad
 \frac mK\gtrsim L^{5/6+\eta/2-o(1)}. \tag{10}
\]
A bucket at this scale still has polynomially many unrelated anchors.

Nearness does not repair this loss.  For a bucket centre \(A\),
\[
 (a-z)^2
 =(A-z)^2+2(a-A)(A-z)+(a-A)^2. \tag{11}
\]
The middle term remains an exact bilinear interaction.  There is no
separation scale for the selected distance values, and their cardinality
\(M\) gives no lower bound on numerical gaps.  Hence an approximate
collision cannot be rounded to an exact collision.  Absolute dyadic
magnitudes are also noncanonical because a vertical translation preserves
all differences.

The matrix \(((a-z)^2)_{a,z}\) has algebraic rank at most three, but rank
alone does not control equality fibres after independently varying radial
potentials.  The previous theorem used one fixed translate of a \(B_4\)
difference set, not merely low matrix rank.

## 3. Why DRC and BSG do not improve the ledger

Form the bipartite multigraph on hub-coordinate vertices, putting one edge
for every selected service.  DRC can find coordinate subsets with large
common graph neighbourhoods.  It cannot turn different numerical anchors
into one anchor \(A\), and at density
\[
 \delta=\frac{S}{U^2m^2} \tag{12}
\]
its \(t\)-fold common-neighbour guarantee pays \(\delta^t\).  At the lower
endpoint in (5), \(\delta\asymp1\), yet the Latin model below still has no
common numerical anchor.  At the upper endpoint,
\[
 \delta=L^{-1/3-5\eta+o(1)}, \tag{13}
\]
so even graph-density retention loses another fixed power.

A BSG cleaning needs large additive energy of one fixed numerical anchor
set.  Projecting
\[
 (a-c-z+d)(a+c-z-d)=\Delta \tag{14}
\]
onto \(a,c\) supplies no such energy: the partner variables \(z,d\) can
absorb the hyperbola parameter.  The one-pair saturation from
`HUB_CROSS_FIBRE_ENERGY.md` already realizes this freedom.  Thus BSG has no
valid energy premise before a representation-level cross-fibre constraint
is used.

## 4. A strict anchor-diffuse marginal barrier

Take \(L\) prime, omit one harmless product fibre, and work over label
indices \(\mathbb F_L\).  Put
\[
 U=L^{2/3-\eta/2},\qquad h=L^{1/3-\eta}, \tag{15}
\]
ignoring integer rounding.

In every product fibre create \(L\) blocks of \(L\) selected symbols.

1. Mark \(U\) blocks as hub blocks and give all of them the same \(L\)
   fibre symbols.
2. Partition the other blocks into groups of \(h\), and give each group its
   own \(L\) common symbols.

The total selected incidence, union and ordered overlap scales are
\[
\begin{aligned}
 I&=\Theta(L^3),\\
 M&=\Theta(L^2+L^3/h)
   =\Theta(L^{8/3+\eta}),\\
 {\cal D}_{\rm hub}
   &=\Theta(U^2L^2)
   =\Theta(L^{10/3-\eta}),\\
 {\cal D}_{\rm other}
   &=\Theta(L^3h)
   =\Theta(L^{10/3-\eta}). \tag{16}
\end{aligned}
\]
Assign triangle degree \(\tau=1\) to every block--value incidence.  Then
\[
 \sum\tau=\Theta(L^3),\qquad
 {\cal J}=\sum d\tau=\Theta(L^{10/3-\eta}), \tag{17}
\]
matching every proved marginal lower bound and respecting
\(d\leq L,\ \tau\leq L^2\).

### Latin anchor assignment

Choose distinct slopes \(s_u\in\mathbb F_L\).  In a nonzero fibre
\(p\in\mathbb F_L^\times\), assign the incidence with symbol
\(k\in\mathbb F_L\) at hub \(u\) the anchor label
\[
 \alpha(u,p,k)=k+s_up. \tag{18}
\]
Every block uses every one of its \(L\) anchors exactly once.

For \(u\ne x\), the map
\[
 (p,k)\longmapsto
 (\alpha(u,p,k),\alpha(x,p,k)) \tag{19}
\]
is a bijection from
\(\mathbb F_L^\times\times\mathbb F_L\) onto the ordered pairs
\((\alpha,\beta)\) with \(\alpha\ne\beta\).  Indeed
\[
 p=\frac{\beta-\alpha}{s_x-s_u},
 \qquad k=\alpha-s_up. \tag{20}
\]
Consequently:

- every ordered anchor-label pair occurs once for a fixed hub pair;
- every hub-anchor vertex has the same service degree;
- dyadic cleaning has only one scale;
- every fixed hub-pair anchor graph is complete bipartite minus a matching,
  so DRC sees maximal graph expansion; and
- nevertheless no anchor pair has multiplicity greater than one.

Finally assign anchor labels at different hubs to disjoint sets of real
numbers.  Then no numerical height \(A\) is shared by two hubs, while every
degree, overlap and joint-moment marginal above is unchanged.

This tensor is realizable by squared differences separately inside each
product fibre, since those blocks form a matching and partner coordinates
can be chosen independently.  It is not globally realizable as constructed:
one nonhub height set would receive independently prescribed partner
coordinates from many fibres.  That omitted consistency is invisible to
the marginals used by pigeonhole, DRC and BSG.

## 5. Exact loss comparison

The barrier makes all evident extraction losses sharp.

| Extraction | Retained mass | Needed mass |
|---|---:|---:|
| one hub-coordinate | \(S/(UL)\) | \(L^3\) |
| one ordered coordinate pair | \(S/(U^2L^2)=1\) at minimal \(U\) | \(L^3\) |
| one random anchor per hub | \(S/L^2=L^{4/3-\eta}\) | \(L^3\) |
| one of \(K^2\) bucket pairs | \(S/K^2\) | \(L^3\) |
| one common numerical \(A\) | \(0\) in the barrier | \(L^3\) |

Even if every hub shared the same \(m\) numerical anchors and every service
had equal labels at its two hubs, pigeonholing one \(A\) would retain only
\(S/m=L^{7/3-\eta}\), still short by \(L^{2/3+\eta}\).

Therefore no bounded sequence of dyadic pigeonholes and standard DRC/BSG
cleanings can reach (4) from the known marginals.

## 6. The first missing representation identity

Let
\[
 P=(\rho_u,a),\quad P'=(\rho_x,c),\quad
 N=(\rho_v,z),\quad N'=(\rho_y,d),
\]
and \(Q(P,N)=\|P-N\|^2\).  Direct expansion gives
\[
 Q(P,N)+Q(P',N')-Q(P,N')-Q(P',N)
 =2(P-P')\cdot(N'-N). \tag{21}
\]
Its vertical contribution is
\[
 2(a-c)(d-z). \tag{22}
\]
Unlike a value-level collision, (21) simultaneously reuses the same two
hub coordinates and the same two partner coordinates on all four cross
edges.  The Latin tensor assigns those representations independently and
therefore has no reason to satisfy (21).

The required next statistic is a representation-refined rectangle moment:
count pairs of overlap services for which the two cross block values in
(21) are also selected using the same point coordinates.  An equivalent
form is an anchor-conditioned triangle degree
\[
 \tau_{\rm pt}(e,a;i,j)
\]
that retains actual endpoint indices \((i,j)\), rather than only the
squared value \(a\).  A useful theorem must show that overlap-weighted
\(\tau_{\rm pt}\), or the corresponding rectangle count, gains
\[
 L^{1/3+2\eta-o(1)}. \tag{23}
\]

The current \({\cal J}=\sum d\tau\) is value-level.  Its compatible triangle
may use a different representation of the same squared value, so it does
not force (21).  This is why it cannot rule out the anchor-diffuse tensor.

## 7. Status

Anchor coherence cannot be extracted with sufficient mass from the present
union, overlap, hub-degree and value-level triangle marginals.  The barrier
is exact at every relevant exponent and remains maximally dense for DRC.
Near-anchor buckets do not preserve exact collision equations, and
low-rank matrix language alone loses the \(B_4\) translate structure.

The next attack must use representation-level endpoint reuse, specifically
the Gram rectangle (21) or an equivalent point-conditioned joint moment.
Until such a statistic is proved large, the common-anchor \(c=4/5\)
subtheorem does not reconnect to the unrestricted problem.

No improvement of the \(3/5\) distance exponent is obtained.

## 8. Verification

`verify_anchor_coherence_extraction.py` checks the exponent-loss ledger, the
finite block marginal barrier, the Latin bijection and uniform anchor
degrees, and the Gram rectangle identity.
