# Erdős #809 — sixth attack: aggregate zero-shore bypass

Date: 2026-07-31

Status:
`SUMMABLE_OVERLAP_LEMMA_AND_LOCAL_ALIGNMENT_PROVED__E0_LITTLE_O_REFUTED_BY_FULL_CONTRACT_ALIGNED_MODEL__GLOBAL_DICHOTOMY_OPEN`

## 1. Outcome

Let (Z) be the graph of zero-shore missing pairs in (B), and give
(e=bb'\in E(Z)) weight

\[
h_e=\lambda(b,b').
\]

The fifth attack proved that (e) forces an (h_e\)-by-(h_e)
missing rectangle inside (A).  This attack determines exactly how far
that fact can be summed.

1. For a fixed missing (A)-pair (aa'), its rectangle overlap has an
   explicit upper bound in terms of the two coordinate degrees and the
   sizes of the colours incident with them.  Summing gives
   \[
   \sum_{e\in E(Z)}h_e^2
   \le
   2\sum_{aa'\in\overline E(A)}d_B(a)d_B(a').                \tag{1}
   \]
2. For every threshold (H\ge2), the zero-shore excess
   \[
   E_0=\sum_{e\in E(Z)}(h_e-1)_+
   \]
   satisfies the weighted high/low bound
   \[
   E_0
   \le
   (H-1)M_B+
   \frac2H\sum_{aa'\in\overline E(A)}d_B(a)d_B(a').          \tag{2}
   \]
3. A zero-shore star has an exact two-type neighbourhood clustering.
   With \(\kappa=n-2\delta\), every zero-shore neighbour (c) of a
   fixed (b) has (N(c)) either within (2\kappa) of (N(b)), or
   within \(\kappa\) of its complement.  An edge of weight
   (h_e>\kappa) must be of the second, opposite-neighbourhood type.
4. There is **no** uniform (O(1)), or even (o(n)), overlap bound.
   More decisively, the desired statement (E_0=o(n^2)) is false under
   the full fixed-(s) Case-1 contract.  A three-hub two-clique family
   has
   \[
   E_0=\Theta(n^2)
   \]
   and one fixed missing (A)-pair lies in \(\Theta(n)\) zero-shore
   rectangles.

The countermodel is not a counterexample to the canonical route or to
#809: it contains an aligned complete core of
((1/2+s+o(1))n) vertices, and its repeated-edge defect is absorbed by
the exact edge-energy slack.  It proves that the aggregate bypass must
be a stability dichotomy:

> either rectangle overlap is chargeable, or its concentration yields
> an aligned two-clique/complete-split core.

That dichotomy remains open.  Erdős #809 remains open.

## 2. Rectangle incidence and fixed-pair overlap

Orient every zero-shore pair (e=bb') arbitrarily.  Let

\[
X_e=\{x_\gamma:\gamma\in\Gamma(b,b')\},\qquad
Y_e=\{y_\gamma:\gamma\in\Gamma(b,b')\}.
\]

Then

\[
|X_e|=|Y_e|=h_e,
\qquad X_e\times Y_e\subseteq\overline E(A).                 \tag{3}
\]

For an ordered missing pair ((a,a')) in (A), define

\[
\mu(a,a')
=
|\{e:(a,a')\in X_e\times Y_e\}|.                            \tag{4}
\]

Let

\[
q(a)=d_B(a).
\]
For a colour \(\gamma\), let (t_\gamma) be the number of its
(A)-to-(B) good edges, and put

\[
L(a)=
\sum_{ab\in E(A,B)}(t_{\chi(ab)}-1).                         \tag{5}
\]

### Lemma 2.1 (fixed missing-pair overlap)

For every ordered missing (A)-pair,

\[
\boxed{
\mu(a,a')
\le
\min\{q(a)q(a'),L(a),L(a')\}.
}                                                            \tag{6}
\]

#### Proof

An occurrence of ((a,a')) determines an oriented zero pair
((b,b')) with

\[
ab,a'b'\in E(A,B).
\]
Coordinate-edge uniqueness gives at most (q(a)q(a')) choices.

Fix the first coordinate edge (ab), of colour \(\gamma\).  For this
rectangle occurrence, (b') must be another outer endpoint of colour
\(\gamma\), giving at most (t_\gamma-1) choices.  Summing over the
edges (ab) gives (L(a)).  The argument at (a') is symmetric.
\(\square\)

The colour-size capacities themselves have the exact sum

\[
\sum_{a\in A}L(a)
=
\sum_\gamma t_\gamma(t_\gamma-1)
=
2\sum_{\{b,b'\}\subset B}\lambda(b,b').                    \tag{7}
\]

This is useful bookkeeping, but it is self-referential: large repeated
colour classes can make the (L(a)) large.

## 3. Summable overlap and high/low decomposition

Double-count the ordered pairs in all rectangles.  Equation (3) gives

\[
\sum_{(a,a')\in\overrightarrow{\overline E}(A)}\mu(a,a')
=
\sum_{e\in E(Z)}h_e^2.                                      \tag{8}
\]

Applying the degree part of (6) yields (1), where the factor two comes
from the two orientations of every missing (A)-edge.  Write

\[
Q_A
=
\sum_{aa'\in\overline E(A)}d_B(a)d_B(a').                   \tag{9}
\]

Then

\[
\sum_e h_e^2\le2Q_A.                                       \tag{10}
\]

### Theorem 3.1 (weighted high/low bound)

For every integer (H\ge2),

\[
E_0\le(H-1)M_B+\frac{2Q_A}{H}.                              \tag{11}
\]

#### Proof

On pairs with (h_e\le H), each excess is at most (H-1), and there
are at most (M_B) pairs.  On pairs with (h_e>H),

\[
h_e-1\le h_e\le\frac{h_e^2}{H}.
\]

Sum and apply (10). \(\square\)

A second immediate bound is

\[
E_0
\le
\sqrt{2M_BQ_A}.                                              \tag{12}
\]

These are the strongest direct estimates supplied by rectangle
incidence alone.  They do not imply (o(n^2)) in the fixed-(s)
regime: both (M_B) and (Q_A) may be macroscopically large.

## 4. Exact local alignment of a zero-shore star

The R003 decomposition gives more structure than the rectangle count.
Put

\[
\kappa=n-2\delta(G).
\]

The existence of a zero-shore pair already forces \(\kappa\ge0\).
Fix (bin B), put (P=N(b)) and (C=V(G)\setminus P), and let (c)
be a zero-shore neighbour of (b).  Write (Q=N(c)).

### Lemma 4.1 (two-type star alignment)

Exactly one of the following types occurs.

1. **Same-neighbourhood type:** (P\cap Q\ne\varnothing), and
   \[
   |P\mathbin\triangle Q|\le2\kappa.                        \tag{13}
   \]
2. **Opposite-neighbourhood type:** (P\cap Q=\varnothing), and
   \[
   Q\subseteq C,
   \qquad |C\setminus Q|\le\kappa.                          \tag{14}
   \]

If the zero edge (bc) has weight (h), then the first type also
satisfies

\[
h\le\kappa.                                                  \tag{15}
\]

#### Proof

In the nonempty-intersection branch, the R003 block

\[
W=(P\cup Q)\setminus(P\cap Q)=P\mathbin\triangle Q
\]

has size at most (2n-4\delta=2\kappa), giving (13).

In the empty-intersection branch, (Q\subseteq C), and

\[
|C\setminus Q|
=n-|P|-|Q|
\le n-2\delta
=\kappa,
\]

giving (14).  Finally, the two (h)-element coordinate sets of the
edge lie disjointly in (P\setminus Q) and (Q\setminus P).  Hence

\[
2h\le|P\mathbin\triangle Q|\le2\kappa
\]

in the first branch. \(\square\)

Consequently:

- any edge with (h>\kappa) is opposite-neighbourhood type;
- two same-type leaves of a zero-shore star have neighbourhood
  symmetric difference at most (4\kappa);
- two opposite-type leaves have neighbourhood symmetric difference at
  most (2\kappa).

For \(\kappa=o(n)\), this is the old near-Dirac stability mechanism.
For fixed (s), \(\kappa=(2s+o(1))n), so the error remains linear.
The missing global step is to show that quadratic **weighted** mass in
one of these local types synchronizes the choices of (P) across many
centres.

## 5. Full-contract obstruction to low overlap

The following family shows that neither uniform overlap nor
(E_0=o(n^2)) can be the correct target.

### 5.1 Graph

Take disjoint sets

\[
U,X,W,Y,H,
\qquad |H|=3,
\]

such that

\[
C_1=U\cup X,qquad C_2=W\cup Y
\]

are cliques.  There are no (C_1)--(C_2) edges.  Every hub in (H)
is adjacent to every vertex of (X\cup Y), and there are no other
hub edges.

For exact integer parameters, choose

\[
|C_1|=p,quad |C_2|=q,quad |Y|=t,
\]

\[
|U|=t-3,quad |X|=p+3-t,quad |W|=q-t.                      \tag{16}
\]

Then

\[
n=p+q+3,qquad
e=\binom p2+\binom q2+3(p+3).                               \tag{17}
\]

The degrees on (U,X,W,Y,H) are respectively

\[
p-1,quad p+2,quad q-1,quad q+2,quad p+3.                \tag{18}
\]

Thus every hub is a maximum-degree vertex.  For (v\in H),

\[
A=N[v]=X\cup Y\cup\{v\},qquad |A|=p+4.                    \tag{19}
\]

The exact BCM size inequality holds whenever (p-q\ge2), because

\[
\left(|A|-\frac n2\right)^2
-
\left(e-\frac{n^2}{4}+\frac n2\right)
=p-q-2\ge0.                                                  \tag{20}
\]

For all sufficiently large groups the graph has (L_4(2)).  After two
deletions, a surviving hub joins (X) to (Y).  Pairs in one clique
have exact four-edge paths inside that clique; cross pairs use one of

\[
U-X-H-Y-W,quad
U-C_1-X-H-Y,quad
X-H-Y-C_2-W,quad
X-X-H-Y-Y,
\]

with filler vertices chosen in the cliques.  A hub-to-clique pair is
handled by (H-X-C_1-C_1-C_1), and two hubs by
(H-X-C_1-X-H).  The finite verifier checks all endpoint/deletion
choices on the 34-vertex instance.

### 5.2 Colouring

Assume asymptotically

\[
\frac pn\to a=\frac12+s,qquad
\frac qn\to b=\frac12-s,qquad
\frac tn\to\theta,
\]

where

\[
\frac b2<\theta<\frac a2.
\]

Then (W) can be injected into (U), and (Y) into (X).  For every
(w\in W), pair all edges (wy), (y\in Y), with the edges

\[
u(w)\psi(y),qquad y\in Y,
\]

using one new colour per pair.  Give every other edge a fresh colour.

Each repeated colour consists of one (U)--(X) edge in (C_1) and
one (W)--(Y) edge in (C_2).  Such edges cannot lie on a common
(C_7): a cycle must cross between the two cliques twice, each crossing
uses a two-edge (X-H-Y) segment, and a segment inside either clique
containing the specified (U)--(X) or (W)--(Y) edge has length at
least two.  The cycle therefore has length at least eight.  Hence every
(C_7) is rainbow.

For every matched pair (u(w)w),

\[
h_{u(w)w}=|Y|=t,
\]

and it is zero-shore because there are no (C_1)--(C_2) edges.
All its rectangles contain the same block

\[
\psi(Y)\times Y.
\]

Therefore

\[
E_0
=|W|(t-1)
=\bigl(\theta(b-\theta)+o(1)\bigr)n^2,                      \tag{21}
\]

while every fixed pair in \(\psi(Y)\times Y\) has overlap

\[
\mu(a,a')=|W|=\Theta(n).                                    \tag{22}
\]

This refutes both (E_0=o(n^2)) and uniform sublinear overlap under the
full structural and colouring contract.

### 5.3 Why it is not a route counterexample

The aligned core (C_1) is a clique of size

\[
|C_1|=(1/2+s+o(1))n.
\]

It already contains the required number of pairwise
(C_7)-compatible edges.  Moreover, for the mixed maximum witness (19),

\[
M_A
=|X||Y|
=\bigl(\theta(a-\theta)+o(1)\bigr)n^2,
\]

\[
M_B
=|U||W|+O(n)
=\bigl(\theta(b-\theta)+o(1)\bigr)n^2,
\]

and

\[
S_m
=e(A,B)-M_A+o(n^2)
=\bigl(\theta(b-\theta)+o(1)\bigr)n^2.                      \tag{23}
\]

The repeated-good-edge defect is

\[
D_A=|W||Y|
=\bigl(\theta(b-\theta)+o(1)\bigr)n^2.                     \tag{24}
\]

Thus the exact budget has ample room.  The large (E_0) is a failure
of the pairwise charge, not a failure of the colour bound.

## 6. Strongest remaining aggregate statement

The sixth attack rules out the proposed endpoint

\[
E_0=o(n^2).
\]

The quantifier-safe replacement is:

> **Aggregate alignment dichotomy.**  If the zero-shore rectangles
> cannot be absorbed into (M_B+S_m), then the same- or
> opposite-neighbourhood clusters of Lemma 4.1 synchronize into an
> aligned complete-split or two-clique core containing
> (T(s)n^2-o(n^2)) pairwise (C_7)-compatible edges.

The three-hub family shows why the structural conclusion is necessary
and numerically sharp.  Equations (6), (11), and Lemma 4.1 are the
proved inputs.  Synchronization across different star centres is still
missing.

## 7. Verification

`verify_809_sixth_attack.py` checks:

1. the rectangle-area identity and a finite high/low split;
2. on the 34-vertex instance
   \[
   (p,q,t)=(18,13,8),
   \]
   density above (n^2/4), minimum and maximum degrees, the exact BCM
   witness threshold, zero shores, induced repeated colours, absence of
   a ((2,3))-linkage for every repeated pair, (E_0=35), fixed-pair
   overlap (5), and an 18-vertex clique core;
3. all 296,769 endpoint/deletion checks for (L_4(2)).

The command

```text
python3 -m unittest -v test_809_sixth_attack.py
```

returns

```text
Ran 3 tests
OK
```

## 8. Claim boundary

- Fixed missing-(A)-pair overlap bound (6): **proved**.
- Summable square bound (1): **proved**.
- Weighted high/low bound (2): **proved**.
- Two-type zero-star alignment lemma: **proved**.
- Uniform (O(1)) or (o(n)) rectangle overlap: **false**.
- (E_0=o(n^2)) under the full Case-1 contract: **false**.
- Three-hub full-contract family has an aligned clique core and satisfies
  the defect budget: **proved**.
- Aggregate alignment dichotomy: **open**.
- Maximum-degree Case 1 and Erdős #809: **open / not claimed**.
