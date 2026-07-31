# Erdős #1083 route A: four-plane matching coefficient audit

Date: 2026-07-30

## 0. Outcome

This note attacks the matching branch supplied by
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`.  At the critical
normalization it gives, for every fixed \(\varepsilon>0\),

\[
 L=t^{1-o(1)}
 \tag{1}
\]

distance labels, each of which has a matching of

\[
 K=t^{1/5-\varepsilon-o(1)}
 \tag{2}
\]

pairwise vertex-disjoint axial-plane pairs, with cell weight

\[
 W_{e,d}\ge Q=t^{3-o(1)}.
 \tag{3}
\]

Four exact conclusions are obtained.

1. **FALSE:** vertex-disjoint plane pairs do not have to carry
   distinct Euclidean coefficients
   \(\lvert\cos(\alpha-\beta)\rvert\).  A matching of arbitrary size
   can have one common coefficient.
2. **PROVED:** after reducing the two independent height translations,
   every individual four-plane equal-distance quadratic has rank six,
   signature \((3,3)\), and the same split real-linear normal form,
   independently of its two cosine coefficients.  It contains
   three-dimensional linear rulings (five-dimensional after restoring
   the two null height translations).
3. **PROVED SHARP LOCAL BARRIER:** there is a literal Euclidean family
   with \(K\) disjoint plane pairs and \(L\le Q/2+1\) common labels,
   every selected cell having at least \(Q\) representations, while all
   \(K\) plane-pair coefficients are identical.  Its selected
   \(2KQ\)-point subsystem has exactly \(2KQ-1\) nonzero squared
   distances.
4. **PROVED COEFFICIENT-DIVERSE BARRIER:** there is also a rational
   Euclidean ruled family in which the \(K\) matched coefficients are
   all distinct, the matched horizontal chord is nevertheless constant,
   all the same rich labels occur, and the whole subsystem still has
   only \(KQ\,t^{o(1)}\) distances.

Thus the phrase “coefficient-separated matching” must mean
**plane-coordinate separated** (no shared plane endpoints), not
**numerically coefficient distinct**.  The matching statement alone
does not supply the coefficient diversity required by the proposed
four-plane attack.

The result is a rigorous barrier and a refinement of the next target.
It is not an improvement of the \(3/5\) exponent.

## 1. The four-plane quadratic has a coefficient-free split normal form

For a nonparallel pair of axial planes write

\[
 F_c(x,y,h)=x^2+y^2-2cxy+h^2,\qquad -1<c<1,
 \tag{4}
\]

where \(c=\cos(\alpha-\beta)\) and \(h=z-w\).  The original two height
coordinates have one irrelevant common-translation coordinate; only
\(h\) occurs in the distance.

### Theorem 1 (split normal form)

For any \(c,c'\in(-1,1)\), the four-plane equal-distance equation

\[
 F_c(x,y,h)=F_{c'}(u,v,k)
 \tag{5}
\]

is real-linearly equivalent to

\[
 X_1^2+X_2^2+X_3^2
 =
 Y_1^2+Y_2^2+Y_3^2.
 \tag{6}
\]

Equivalently, after the further invertible change

\[
 A=X-Y,\qquad B=X+Y,
 \tag{7}
\]

it is

\[
 \boxed{A\mathbin{\cdot}B=0.}
 \tag{8}
\]

Consequently the reduced quadratic has rank six and signature
\((3,3)\).  It contains a three-dimensional linear space

\[
 \{(X,Y):Y=OX\}
 \tag{9}
\]

for every \(O\in O(3)\).  Restoring the unused coordinates \(z+w\)
and \(s+t\) gives rank six, nullity two, and five-dimensional linear
rulings in the original eight variables.

### Proof

The exact identity

\[
 x^2+y^2-2cxy
 =
 \frac{1-c}{2}(x+y)^2
 +
 \frac{1+c}{2}(x-y)^2
 \tag{10}
\]

has two positive coefficients for \(-1<c<1\).  Put

\[
 X_1=\sqrt{\frac{1-c}{2}}(x+y),\qquad
 X_2=\sqrt{\frac{1+c}{2}}(x-y),\qquad
 X_3=h
 \tag{11}
\]

and define \(Y\) similarly using \(c'\) and \((u,v,k)\).  Both changes
are invertible, and (5) becomes (6).  Finally,

\[
 \|X\|^2-\|Y\|^2=(X-Y)\mathbin{\cdot}(X+Y),
 \]

which proves (8).  Equation (9) lies in (6) because orthogonal maps
preserve the norm. \(\square\)

### What Theorem 1 does and does not say

It rules out a saving based only on treating one four-plane equation
as a coefficient-generic real quadric: all such quadrics have the same
split ruled type.  It does **not** rule out an argument that preserves
the endpoint Cartesian products.  The whitening map (11) mixes the two
radial endpoint variables, and hence does not preserve arbitrary sets
\(P_\alpha\times P_\beta\).  Arithmetic or simultaneous compatibility
across several plane pairs can still carry information.

The necessary new input is therefore not merely
\(c\ne c'\).  It must exploit simultaneous product-set compatibility
of several distance equations sharing actual endpoint sets.

## 2. A matching does not separate cosine coefficients

An axial plane is naturally indexed by an angle modulo \(\pi\).  The
coordinate-independent coefficient invariant of a plane pair is

\[
 \chi(\alpha,\beta)
 =
 \lvert\cos(\alpha-\beta)\rvert.
 \tag{12}
\]

Changing the sign convention for one signed radial coordinate changes
the sign of \(c\), but not \(\chi\).

### Proposition 2 (coefficient multiplicity dichotomy)

Let \(\mathcal M\) be a matching of \(K\) axial-plane pairs and let
\(C\) be the number of different values of \(\chi\) on
\(\mathcal M\).  Then, for every \(1\le R\le K\), either

\[
 C\ge R,
 \tag{13}
\]

or some one angular coefficient occurs on more than \(K/R\) edges.
After orienting each of these disjoint edges separately, the latter
family has the exact form

\[
 \beta_i=\alpha_i+\theta\pmod\pi
 \tag{14}
\]

for one fixed acute separation \(\theta\).

This is just pigeonholing, but it is the strongest conclusion available
from a matching without an additional hypothesis.  In particular,
\(C=1\) is possible for every \(K\).

## 3. Exact Euclidean common-coefficient matching barrier

The next construction simultaneously verifies the cell richness, the
common labels, the four-plane equality count, and the failure of
coefficient diversity.

### Theorem 3 (vertical polygonal matching barrier)

Let \(K,Q\ge1\), put

\[
 \phi=2\arctan\frac{1}{16K},
 \tag{15}
\]

and, for \(0\le i<2K\), let \(\Pi_i\) be the axial plane of angle
\(i\phi\).  In \(\Pi_i\) take the vertical column

\[
 P_i
 =
 \{(\cos(i\phi),\sin(i\phi),z):0\le z<Q,\ z\in\mathbb Z\}.
 \tag{16}
\]

Put \(P=\bigcup_iP_i\), and define

\[
 a_h=2-2\cos(h\phi)\qquad(0\le h<2K).
 \tag{17}
\]

Then:

1. the \(2K\) planes are distinct;
2. the nonzero squared-distance set has the exact cardinality
   \[
   \boxed{|\Delta^2(P)\setminus\{0\}|=2KQ-1;}
   \tag{18}
   \]
3. the adjacent pairs
   \[
   \mathcal M=\{\{\Pi_{2r},\Pi_{2r+1}\}:0\le r<K\}
   \tag{19}
   \]
   form a matching and all have the same coefficient
   \[
   \cos\phi;
   \tag{20}
   \]
4. for every
   \[
   0\le s\le\lfloor Q/2\rfloor,
   \qquad d_s=a_1+s^2,
   \tag{21}
   \]
   every cell \((e,d_s)\), \(e\in\mathcal M\), has exact oriented
   representation weight
   \[
   r_Q(s)
   =
   \begin{cases}
   Q,&s=0,\\
   2(Q-s),&s>0,
   \end{cases}
   \tag{22}
   \]
   and hence \(r_Q(s)\ge Q\);
5. on the selected oriented matching rows, the exact cross-row
   contribution of \(d_s\) is
   \[
   \boxed{K(K-1)r_Q(s)^2.}
   \tag{23}
   \]

### Proof

Since \(\arctan u<u\) for \(u>0\),

\[
 (2K-1)\phi<2K\phi
 <4K\frac1{16K}
 =\frac14<\frac\pi3.
 \tag{24}
\]

Thus all plane angles are distinct and lie in an interval shorter than
\(\pi/3\).  The squared distance between points in columns \(i,j\) is

\[
 a_{\lvert i-j\rvert}+(z-w)^2.
 \tag{25}
\]

Every pair

\[
 (h,s)\in\{0,\ldots,2K-1\}\times\{0,\ldots,Q-1\}
 \tag{26}
\]

is realized.  Moreover \(a_h\) is strictly increasing and

\[
 0\le a_h<1.
 \tag{27}
\]

If

\[
 a_h+s^2=a_{h'}+s'^2,
 \]

then the integer \(s^2-s'^2\) lies strictly between \(-1\) and \(1\).
It is zero, so \(s=s'\), and strict monotonicity gives \(h=h'\).
There are therefore exactly \(2KQ\) squared labels including zero,
which proves (18).

Every edge in (19) has angular gap \(\phi\), proving (20).  On such an
edge, (25) equals \(d_s\) exactly when \(\lvert z-w\rvert=s\).
There are \(Q\) solutions for \(s=0\), and \(2(Q-s)\) for \(s>0\).
This proves (22).  Finally, the codegree sum over ordered distinct
selected rows has \(K(K-1)\) terms, each of weight \(r_Q(s)^2\), which
proves (23). \(\square\)

### Exact arithmetic realization

Although (16) is written trigonometrically, the construction has
rational horizontal coordinates.  If

\[
 u=\frac1{16K},\qquad
 c=\frac{1-u^2}{1+u^2},\qquad
 s=\frac{2u}{1+u^2},
 \tag{28}
\]

then rotation by \(\phi=2\arctan u\) has the rational matrix

\[
 \begin{pmatrix}c&-s\\s&c\end{pmatrix}.
 \tag{29}
\]

Starting from \((1,0)\), every horizontal coordinate in (16) is
rational.  The verifier uses exact `fractions.Fraction` arithmetic.

### Theorem 4 (coefficient-diverse ruled matching barrier)

There is a second, stronger obstruction to using numerical coefficient
diversity alone.  For \(1\le r\le K\), put

\[
 A_r=(3r,1),\qquad B_r=(3r+1,1)
 \tag{30}
\]

in the horizontal plane, and take the \(2K\) vertical columns

\[
 \{(A_r,z):0\le z<Q\},\qquad
 \{(B_r,z):0\le z<Q\}.
 \tag{31}
\]

Each horizontal point defines its own axial plane through the vertical
axis.  Pair the \(A_r\)-plane with the \(B_r\)-plane.

Then:

1. all \(2K\) axial planes are distinct;
2. every matched horizontal chord has squared length one;
3. the \(K\) coefficient invariants
   \[
   \chi_r
   =
   \frac{A_r\mathbin{\cdot}B_r}
   {\|A_r\|\|B_r\|}
   \tag{32}
   \]
   are all distinct;
4. every label
   \[
   d_s=1+s^2,\qquad 0\le s\le\lfloor Q/2\rfloor,
   \tag{33}
   \]
   has the same exact cell weight \(r_Q(s)\) from (22) on all \(K\)
   matching edges;
5. if \(P^\sharp_{K,Q}\) denotes the union of the \(2K\) columns, then
   \[
   \frac{KQ}{T_2}
   \le
   |\Delta^2(P^\sharp_{K,Q})|
   \le
   3KQ,
   \tag{34}
   \]
   where
   \[
   T_2=\max_{1\le n\le (3K)^2+Q^2}4\tau(n).
   \tag{35}
   \]

In particular, if \(K,Q\) have polynomial size in \(t\), then

\[
\boxed{
|\Delta^2(P^\sharp_{K,Q})|
=KQ\,t^{o(1)}.
}
\tag{36}
\]

### Proof

The horizontal rays have slopes

\[
\frac1{3r},\qquad\frac1{3r+1};
\]

all are distinct because their denominators are distinct modulo three.
The matched chord is \(B_r-A_r=(1,0)\).

Let \(\delta_r\) be the acute angle between \(A_r\) and \(B_r\).  The
tangent subtraction formula gives

\[
\tan\delta_r
=
\frac{1}{3r(3r+1)+1}.
\tag{37}
\]

Hence \(\delta_r\) is strictly decreasing, so \(\chi_r=\cos\delta_r\)
is strictly increasing.  This proves coefficient diversity.  Equation
(33) and the cell weights follow from the unit horizontal chord exactly
as in Theorem 3.

Every horizontal difference is an integer of magnitude less than
\(3K\), and every vertical difference has magnitude less than \(Q\).
There are fewer than \(3KQ\) possible pairs of their absolute values,
which proves the upper bound in (34).

For the lower bound, retain horizontal differences

\[
x=3j,\qquad 0\le j<K,
\]

between \(A_1\) and the \(K\) columns \(A_{j+1}\), and every vertical
difference \(0\le s<Q\).  This gives \(KQ\) integer input pairs
\((x,s)\) and squared labels

\[
x^2+s^2.
\]

One label has at most
\(r_2(n)\le4\tau(n)\le T_2\) signed representations when \(n>0\);
the zero label has one input representation and is also bounded by
\(T_2\).  This proves the lower bound. \(\square\)

Theorem 4 pinpoints the real issue: separated angular coefficients can
be exactly compensated by separated radial coordinates.  A useful
coefficient theorem must control the coupled quantities

\[
x^2+y^2-2cxy,
\]

not \(c\) by itself.

## 4. Critical exponent interpretation

Take

\[
 Q=t^3,\qquad
 K=t^{\kappa-o(1)},\qquad
 L=t,
 \tag{38}
\]

where \(0<\kappa<1\).  Since \(L\ll Q\), Theorem 3 supplies exactly the
local data

\[
 L\text{ labels}\times K\text{ disjoint rich plane pairs}
\times Q\text{ representations per cell},
 \tag{39}
\]

with no numerical coefficient separation.  Its matched subsystem has

\[
 |\Delta^2|=t^{3+\kappa-o(1)}.
 \tag{40}
\]

At the currently proved value
\(\kappa=1/5-\varepsilon\), this is
\(t^{16/5-\varepsilon-o(1)}\).

This makes the model a sharp benchmark for any argument that uses only
the selected matching planes and cells: the largest possible universal
conclusion cannot exceed a factor \(K\) over \(Q\).

It is **not** a counterexample to the full critical node.  The inherited
node has \(M=t\) active planes, whereas the selected subsystem above has
only \(2K\) planes when \(K=o(t)\).  Extending (16) to all \(M=t\)
vertical columns gives exactly \(MQ=t^4\) squared-distance labels, which
is already a strong expansion branch.

### Energy-retention audit

There is a second exponent obstruction.  Let
\(\mathfrak C_{\rm selected}\) be only the cross-row codegree formed
inside the \(K\) selected matching cells for the \(L\) guaranteed
labels.  The cell lower bound \(W_{e,d}\ge Q=t^{3-o(1)}\) certifies only

\[
\mathfrak C_{\rm selected}
\ge
LK(K-1)Q^2
=t^{7+2\kappa-o(1)}.
\]

At the other extreme, the incidence cell cap
\(W_{e,d}\le t^{4+o(1)}\) gives

\[
\mathfrak C_{\rm selected}
\le
LK^2t^{8+o(1)}
=t^{9+2\kappa+o(1)}.
\]

For \(\kappa=1/5-\varepsilon\), even this upper limit is

\[
t^{47/5-2\varepsilon+o(1)},
\]

whereas the inherited full cross-plane codegree is
\(t^{13-o(1)}\).  Thus the selected matching rows can carry at most a

\[
t^{-18/5-2\varepsilon+o(1)}
\]

fraction of the full forced energy.

This does not invalidate the matching theorem; it clarifies its role.
It is a structural witness, not an energy-preserving regularization.
An argument confined to four-plane products among the selected matching
cells cannot simply reuse the \(t^{13}\) lower bound.  It must either
propagate the matching structure to unselected cells, or strengthen the
extraction so that substantially more labels or representation mass are
retained.

## 5. Refined target forced by the audit

The following implication is false:

\[
\text{large plane matching}
\Longrightarrow
\text{many distinct cosine coefficients}.
\tag{41}
\]

The four-plane route must instead prove a three-way statement.

1. **Product-sensitive coefficient diversity:** many matched equations
   have coefficients that remain separated under coordinate changes
   preserving the actual endpoint Cartesian products, and this gives an
   incidence saving.
2. **Fixed-angle translation chart:** a large submatching has one
   coefficient, hence the angular translation structure (14); use the
   repeated geometry together with endpoint/radius/height information.
3. **Direct expansion:** the recovered ruled family behaves like
   Theorem 3 and already supplies \(QK^\eta\) or more distances.

Numerical inequality of two cosine coefficients is insufficient by
Theorems 1 and 4, while coefficient diversity is not inherited by
Proposition 2 and Theorem 3.  A successful result must retain coupled
coefficient--radius information and endpoint product structure across
several labels or several incident plane pairs.

## 6. What the whole \(L\times K\) family does force

Although one colour class is only a matching, the union of all colour
classes has \(LK\) edge occurrences.  The following elementary
regularization identifies the first place where simultaneous
coefficient compatibility could enter.

### Proposition 5 (repeated pair or short properly coloured cycle)

Let \(G_d\) be a matching of size at least \(K\) on the same set of
\(M\) plane vertices, for each of \(L\) distinct labels \(d\).
Let

\[
\mu=\max_e|\{d:e\in G_d\}|
\tag{42}
\]

be the largest label multiplicity of one unordered plane pair.  For
any threshold \(R\ge1\), either

\[
\boxed{\mu\ge R,}
\tag{43}
\]

or the simple union graph has at least

\[
\boxed{\frac{LK}{R}}
\tag{44}
\]

different edges.

In the critical exponent notation

\[
M=t^{1+o(1)},\quad L=t^{1-o(1)},\quad
K=t^{\kappa-o(1)},
\tag{45}
\]

fix \(0<\rho<\kappa\) and take \(R=t^\rho\).  Then either one plane
pair supports \(t^{\rho-o(1)}\) selected labels, or the union contains
a properly edge-coloured cycle of bounded length.  More precisely, for
every fixed integer \(r\) with

\[
r(\kappa-\rho)>1,
\tag{46}
\]

it contains, for all sufficiently large \(t\), a cycle of length at
most \(2r+1\).  Adjacent edges on this cycle have different labels.

### Proof

There are at least \(LK\) labelled edge occurrences.  If every
underlying edge occurs fewer than \(R\) times, their number is greater
than \(LK/R\), proving (44).

Under (45), the latter simple graph has

\[
t^{1+\kappa-\rho-o(1)}
\]

edges on \(t^{1+o(1)}\) vertices.  Repeatedly delete vertices of degree
less than the edge-to-vertex ratio.  A nonempty subgraph remains with
minimum degree

\[
\delta=t^{\kappa-\rho-o(1)}.
\]

If its girth exceeded \(2r+1\), a breadth-first tree of depth \(r\)
would contain at least

\[
1+\delta\sum_{j=0}^{r-1}(\delta-1)^j
\ge(\delta-1)^r
\]

different vertices.  By (46) this exceeds \(M\) for large \(t\), a
contradiction.  Finally, two adjacent edges cannot carry the same
selected label because every \(G_d\) is a matching. \(\square\)

At \(\kappa=1/5-\varepsilon\), choosing (for example)
\(\rho=\kappa/2\) gives either a polynomial repeated-pair family or a
cycle of an absolute length depending only on \(\varepsilon\).

This is a genuine simultaneous structure, but it does not close the
problem.  In the repeated-pair branch, \(R\) labels of weight \(Q\)
give only \(RQ\) point--circle incidences among \(Q\) points and
\(QR\) source-label circles.  This is exactly the linear \(+n\) term
of the planar incidence bound.  Theorem 3 realizes this behaviour
literally.  In the cycle branch, weight \(Q\) in each cell does not
ensure that the endpoint subsets used by the two incident cells
overlap.  A new Euclidean endpoint-overlap lemma is still required
before the coefficient holonomy around the cycle can be used.

## 7. Claim boundary

### PROVED

- the split normal form and exact rank/signature/ruling statement;
- the coefficient multiplicity/fixed-angle translation dichotomy;
- the rational-coordinate Euclidean construction;
- its exact distance count, rich-cell weights, and selected codegree;
- the rational coefficient-diverse ruled construction and its
  two-square upper/lower distance bounds;
- the exponent-level \(KQ\) local benchmark.

### FALSE

- “pairwise disjoint plane pairs have distinct cosine coefficients”;
- “coefficient inequality makes one four-plane quadric non-ruled”;
- any claim that the present result improves \(f_3(N)\).

### CONDITIONAL / OPEN

- extracting endpoint product compatibility from the \(L\times K\)
  matching data;
- proving expansion in the fixed-angle translation branch without
  already assuming vertical/common-radius columns;
- lifting the short plane cycle in Proposition 5 to a positive-density
  cycle of actual endpoint incidences;
- a fixed improvement over the \(3/5\) exponent.

## 8. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_a
pytest -q test_verify_four_plane_matching_barrier.py
python3 verify_four_plane_matching_barrier.py
```
