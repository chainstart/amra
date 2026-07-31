# Erdős #809 — third attack: the BCM maximum-degree witness

Date: 2026-07-31

Status:
`CENTER_PROFILE_COLLAPSED__EXCESS_DEGREE_ENERGY_REGIME_CLOSED__CANONICAL_CHARGE_OPEN`

## 1. Main outcome

This attack treats only the first, maximum-degree branch of BCM
Lemma 3.1.  Let \(v\) be a maximum-degree vertex and
\[
A=N[v].
\]
Three rigorous advances result.

1. **All four old endpoint profiles collapse to one centered
   certificate.**  If two good edges have the same colour, neither is
   incident with \(v\).  Orient one endpoint of each into \(A\), say
   \(xy,zw\) with \(x,z\in A\).  Then
   \[
   x-v-z
   \]
   is a clean shortest path, and every three-edge \(y\)-to-\(w\) path
   meets \(\{x,v,z\}\).  There is no distance-three or contaminated
   profile in this branch.
2. **The good-edge surplus has an exact complement-energy form.**  If
   \(B=V\setminus A\), then
   \[
   |E_{\rm good}(A)|-\Phi(n,e)
   =\overline e(B)+S_m,                                      \tag{1}
   \]
   where \(\overline e(B)\) is the number of missing edges in \(G[B]\),
   \(m=|A|\), and \(S_m\ge0\) is an explicit size slack.  Thus the precise
   remaining charge is
   \[
   D_A\le\overline e(B)+S_m+o(n^2).                           \tag{2}
   \]
3. **A positive-width maximum-degree regime closes.**  Let \(k\) be the
   least integer with
   \[
   \binom k2\ge\Phi(n,e).
   \]
   If \(m=k+g\), \(g\ge1\), and the number \(M_A\) of missing edges in
   \(G[A]\) satisfies
   \[
   M_A\le\frac{g(k-7)}{16},                                  \tag{3}
   \]
   then \(G[A]\) contains at least \(\Phi(n,e)\) pairwise
   \(C_7\)-compatible edges.  Hence the target colour bound, and (2) for
   this witness, both hold.
4. **A rich-outer regime closes directly against \(M_B\).**  If
   \(M_B<\binom{q-1}{2}\), every good edge admitting an orientation whose
   outer endpoint has at least \(q\) neighbours in \(B\) belongs to one
   pairwise \(C_7\)-compatible family.

Condition (3) permits \(M_A=\Theta(n^2)\) when the maximum degree exceeds
the extremal threshold by a fixed linear amount.  It strictly extends
the \(o(n^2)\)-missing-edge core closure in `SECOND_ATTACK.md`.

A rotated two-clique family shows that an arbitrary maximum-degree
witness \(N[v]\) need not align with the actual dense larger core, even
under the density, minimum-degree, and \(L_4(2)\) asymptotic contract.
Thus witness alignment alone cannot close the branch.  The centered
defect charge (2) remains open, and Erdős #809 is not proved.

## 2. Frozen maximum-degree setup

Let \(G\) be an \(n\)-vertex graph satisfying \(L_4(2)\), and assume
\(\delta(G)\ge3\).  Let every \(C_7\) in an edge-colouring of \(G\) be
rainbow.  Choose a maximum-degree vertex \(v\), and put
\[
\Delta=d(v),\qquad A=N[v],\qquad m=|A|=\Delta+1,
\]
\[
B=V\setminus A,\qquad r=|B|=n-m.
\]
An edge is good if it has an endpoint in \(A\).

In the BCM maximum-degree branch,
\[
m\ge C_1
=\frac n2+\sqrt{e-\frac{n^2}{4}+\frac n2}.                   \tag{4}
\]
As before,
\[
\Phi(n,e)
=\frac e2+\frac n2\sqrt{e-\frac{n^2}{4}}.                    \tag{5}
\]

## 3. Center-collapse lemma

### Lemma 3.1 (single centered profile)

Let \(xy,zw\) be two same-colour good edges.  Choose
\[
x\in A\cap\{x,y\},\qquad z\in A\cap\{z,w\},
\]
and use \(y,w\) for the complementary endpoints.  Then:

1. neither specified edge is incident with \(v\);
2. the two edges form an induced matching;
3. \(x-v-z\) is a clean shortest \(x\)-to-\(z\) path of length two;
4. every simple three-edge \(y\)-to-\(w\) path meets
   \[
   \{x,v,z\}.                                                 \tag{6}
   \]

Equivalently,
\[
\tau_3(y,w)\le3
\]
with a cover whose middle vertex is the same fixed \(v\) for every
repeated pair.

#### Proof

The \(L_4(2)\) splice from `NEAR_DIRAC_C7_THEOREM.md` shows that two
edges at edge distance zero or one lie on a common \(C_7\).  Same-colour
edges must therefore have edge distance at least two.  In particular,
they form an induced matching.

If one specified edge were incident with \(v\), the other good edge
would have an endpoint in \(A=N[v]\), putting the two edges at edge
distance at most one.  Thus neither contains \(v\).

Now \(x,z\in N(v)\), so \(x-v-z\) is a two-edge path.  Edge distance at
least two makes \(x,z\) nonadjacent and ensures that \(v\) is distinct
from all four specified endpoints.  Hence this path is clean and
shortest.

Finally, a three-edge \(y\)-to-\(w\) path avoiding \(\{x,v,z\}\), joined
to
\[
y-x-v-z-w,
\]
would be a simple \(C_7\) containing both same-colour edges.  This is
forbidden, proving (6). \(\square\)

### Consequence

The D2-AA / D2-AO / D2-OO / D3 closest-endpoint classification remains
valid as a global taxonomy, but none of it is needed for the
maximum-degree witness.  Retaining the selected \(A\)-endpoints always
gives the clean centered A2 certificate.  In particular:

- the distance-three zero-codegree branch disappears;
- contaminated \(A\)-geodesics disappear;
- every attempted charge may keep the same central vertex \(v\).

This is the strongest simplification of the local obstruction found in
the campaign.

### Lemma 3.2 (outside missing-edge rectangle)

In the setting of Lemma 3.1, put
\[
P_y=N_B(y)\setminus\{w\},\qquad
P_w=N_B(w)\setminus\{y\}.
\]
Then there is no edge of \(G[B]\) with one endpoint in \(P_y\) and the
other in \(P_w\).

Indeed, if distinct \(p\in P_y,q\in P_w\) satisfied \(pq\in E(G)\), then
\[
y-p-q-w
\]
would be a three-edge path avoiding \(\{x,v,z\}\), contrary to (6).

If
\[
d_B(y),d_B(w)\ge q,
\]
then
\[
|P_y|,|P_w|\ge q-1.
\]
The number of distinct unordered pairs with one endpoint in each of two
sets of size at least \(q-1\) is minimized when the sets coincide.
Consequently Lemma 3.2 forces
\[
M_B\ge\binom{q-1}{2}.                                       \tag{6a}
\]

This is the first direct conversion of the centered certificate into
the exact outside-missing-edge budget.

### Lemma 3.3 (colour-class \(B\)-endpoint accounting)

Fix, for every good edge in a colour class \(\gamma\), one orientation
whose inner endpoint lies in \(A\).  Let \(Y_\gamma\subseteq B\) be the
set of resulting outer endpoints in \(B\), and put
\[
t_\gamma=|Y_\gamma|.
\]
Then \(Y_\gamma\) is an independent set in \(G[B]\).  Consequently,
\[
\binom{t_\gamma}{2}
\le M_B.                                                     \tag{6b}
\]
Moreover, after rooting the \(B\)-outer edges of this colour class at
one outer endpoint \(b_\gamma\), its other \(t_\gamma-1\) edges inject
into the distinct missing pairs
\[
\{b_\gamma,b\},
\qquad b\in Y_\gamma\setminus\{b_\gamma\}.                   \tag{6c}
\]

Indeed, the same-colour edges form an induced matching, so any two
distinct outer endpoints in \(B\) are nonadjacent.  This proves both
claims.

The exact global accounting is
\[
\sum_\gamma\binom{t_\gamma}{2}
=\sum_{\{b,b'\}\in\overline E(G[B])}\lambda(b,b'),            \tag{6d}
\]
where \(\lambda(b,b')\) is the number of colours whose chosen
\(B\)-outer endpoint set contains both \(b,b'\).  Hence, if one could
prove
\[
\max_{\{b,b'\}}\lambda(b,b')\le\Lambda,
\]
then the \(B\)-outer portion of the defect would be at most
\[
\sum_\gamma(t_\gamma-1)_+
\le\Lambda M_B.                                              \tag{6e}
\]

The missing requirement for (13) is essentially
\(\Lambda=1+o(1)\), together with control of edges whose outer endpoints
remain in \(A\).  Neither follows from a single colour class.

## 4. Exact complement-energy ledger

Write
\[
M_A=\binom m2-e(G[A]),\qquad
M_B=\binom r2-e(G[B]),
\]
and
\[
X=e(A,B).
\]

### Lemma 4.1 (maximum-degree domination)

\[
X\le2M_A.                                                     \tag{7}
\]

#### Proof

For \(u\in A\), let
\[
\overline d_A(u)=m-1-d_{G[A]}(u)
\]
be its missing degree inside \(A\).  Since \(v\) has maximum degree,
\[
d_G(u)\le\Delta=m-1.
\]
Therefore
\[
d_B(u)
=d_G(u)-d_{G[A]}(u)
\le(m-1)-d_{G[A]}(u)
=\overline d_A(u).
\]
Summing over \(u\in A\) gives
\[
X=\sum_{u\in A}d_B(u)
\le\sum_{u\in A}\overline d_A(u)
=2M_A.
\]
\(\square\)

### Lemma 4.2 (edge-energy identity)

Put
\[
U_m=\binom m2+\binom r2,\qquad L_m=U_m-e.
\]
Then \(L_m\ge0\), and
\[
X=M_A+M_B-L_m.                                               \tag{8}
\]

#### Proof

The identity follows by writing
\[
e
=\binom m2-M_A+\binom r2-M_B+X.
\]
The BCM threshold \(C_1\) is the larger solution of
\[
\binom x2+\binom{n-x}{2}=e.
\]
The left side is increasing for \(x\ge n/2\).  Since \(m\ge C_1\),
\(U_m\ge e\), so \(L_m\ge0\). \(\square\)

Equations (7)--(8) give the necessary energy constraints
\[
M_A+M_B\ge L_m,\qquad M_B\le M_A+L_m.                         \tag{9}
\]
They do not by themselves control the colour defect.

### Lemma 4.3 (exact good-edge surplus)

Define
\[
S_m=e-\binom r2-\Phi(n,e).                                   \tag{10}
\]
Then
\[
S_m\ge0
\]
and
\[
|E_{\rm good}(A)|-\Phi(n,e)=M_B+S_m.                         \tag{11}
\]

#### Proof

Since the only bad edges are those in \(G[B]\),
\[
\begin{aligned}
|E_{\rm good}(A)|
&=e-e(G[B])\\
&=e-\binom r2+M_B,
\end{aligned}
\]
which gives (11).

For nonnegativity, put
\[
t=\sqrt{e-\frac{n^2}{4}},\qquad r_0=\frac n2-t.
\]
The exact identity
\[
\Phi(n,e)=e-\frac{r_0^2}{2}                                  \tag{12}
\]
holds.  Equation (4) gives
\[
r\le\frac n2-\sqrt{t^2+\frac n2}<r_0.
\]
Hence
\[
\binom r2\le\frac{r^2}{2}<\frac{r_0^2}{2}=e-\Phi(n,e),
\]
and \(S_m\ge0\). \(\square\)

Combining (11) with
\[
c_A=|E_{\rm good}(A)|-D_A
\]
shows that the maximum-degree branch has one exact global target:
\[
\boxed{
D_A\le M_B+S_m+o(n^2).
}                                                             \tag{13}
\]

When
\[
e=\left(\frac14+s^2+o(1)\right)n^2,\qquad
m=\left(\frac12+s+\theta+o(1)\right)n,
\]
one has
\[
\frac{S_m}{n^2}
=\theta\left(\frac12-s\right)-\frac{\theta^2}{2}+o(1).        \tag{14}
\]
At the minimal-size scale \(\theta=0\), (13) becomes
\[
D_A\le M_B+o(n^2).                                           \tag{15}
\]
Thus missing edges in the **outside** block, not missing edges in
\(A\), are the exact asymptotic budget.

## 5. Excess-degree / missing-energy closure

The preceding identity isolates the charge target.  A separate
compatible-core argument closes a nontrivial parameter region before
that charge is needed.

Define
\[
k=k(n,e)
=\min\left\{j\in\mathbb N:\binom j2\ge\Phi(n,e)\right\}.       \tag{16}
\]
Equation (4) implies \(k\le m\): indeed,
\[
\binom m2
\ge e-\binom r2
\ge\Phi(n,e)
\]
by the proof of Lemma 4.3.

### Theorem 5.1 (exact excess-degree cleaning theorem)

Assume \(k\ge8\), write
\[
m=k+g,\qquad g\ge1,
\]
and suppose
\[
M_A\le\frac{g(k-7)}{16}.                                     \tag{17}
\]
Then \(G[A]\) contains a family of at least \(\Phi(n,e)\) edges such that
every two lie on a common \(C_7\).  Consequently every rainbow-\(C_7\)
colouring of \(G\) uses at least \(\Phi(n,e)\) colours, and the budgeted
defect inequality holds for this \(A\) without an asymptotic error.

#### Proof

For \(u\in A\), retain the missing degree
\[
\overline d_A(u)=m-1-d_{G[A]}(u).
\]
Delete the set
\[
R=\left\{
u\in A:
\overline d_A(u)>\frac{k-7}{4}
\right\}.
\]
The missing-degree sum equals \(2M_A\).  Therefore, using (17),
\[
|R|\frac{k-7}{4}<2M_A
\le\frac{g(k-7)}8,
\]
so
\[
|R|<\frac g2.                                                \tag{18}
\]

Put \(H=G[A\setminus R]\) and \(h=|V(H)|\).  Then
\[
h>k+\frac g2.                                                \tag{19}
\]
Every retained vertex has at most \((k-7)/4\) nonneighbours inside
\(H\), so
\[
\begin{aligned}
2\delta(H)-h
&\ge h-2-\frac{k-7}{2}\\
&>\frac{k+g+3}{2}\\
&\ge5.                                                       \tag{20}
\end{aligned}
\]
By Lemma 5.2 of `SECOND_ATTACK.md`, every two edges of \(H\) lie on a
common \(C_7\).

It remains to count the edges.  From (19),
\[
\begin{aligned}
\binom h2-\binom k2
&=(h-k)\frac{h+k-1}{2}\\
&>\frac g2\cdot\frac{2k-1}{2}\\
&>\frac{g(k-7)}{16}\\
&\ge M_A.
\end{aligned}
\]
Hence
\[
e(H)
\ge\binom h2-M_A
\ge\binom k2
\ge\Phi(n,e).
\]
All these edges must have distinct colours. \(\square\)

### Corollary 5.2 (positive-width asymptotic regime)

Fix \(s\in(0,1/2)\) and \(\theta>0\).  Suppose
\[
e=\left(\frac14+s^2+o(1)\right)n^2
\]
and the maximum-degree branch supplies
\[
\frac{|A|}{n}
\ge\frac12+s+\theta+o(1).
\]
Since
\[
\frac{k}{n}\longrightarrow\frac12+s,
\]
Theorem 5.1 applies whenever
\[
\limsup_{n\to\infty}\frac{M_A}{n^2}
<
\frac{\theta(1/2+s)}{16}.                                    \tag{21}
\]
This permits a fixed positive density of missing edges in \(A\).  It is
strictly stronger than requiring \(M_A=o(n^2)\).

### Theorem 5.3 (rich-outer compatibility clique)

For an integer \(q\ge2\), let \(\mathcal F_q\) be the set of good edges
which admit an orientation
\[
xy,\qquad x\in A,\qquad d_B(y)\ge q.                          \tag{21a}
\]
If
\[
M_B<\binom{q-1}{2},                                          \tag{21b}
\]
then every two edges of \(\mathcal F_q\) lie on a common \(C_7\).
Therefore, if additionally
\[
|\mathcal F_q|\ge\Phi(n,e),                                  \tag{21c}
\]
the maximum-degree branch closes.

#### Proof

Take two edges of \(\mathcal F_q\) and choose orientations as in (21a).
If their edge distance is zero or one, \(L_4(2)\) puts them on a common
\(C_7\).  Otherwise they form an induced matching and Lemma 3.1 applies.
If they did not lie on a common \(C_7\), Lemma 3.2 and (6a) would give
\[
M_B\ge\binom{q-1}{2},
\]
contrary to (21b).  Hence \(\mathcal F_q\) is a clique in the
\(C_7\)-compatibility graph. \(\square\)

In particular, if \(M_B=o(n^2)\), then for every fixed \(\rho>0\), all
good edges admitting an orientation whose outer endpoint has at least
\(\rho n\) neighbours in \(B\) form a pairwise compatible family for
all sufficiently large \(n\).  The remaining hard edges necessarily
have low-\(B\)-degree outer endpoints.

### Exact failure certificate

If the maximum-degree branch is not already closed by Theorem 5.1, then
one has the explicit alternative
\[
M_A>\frac{(m-k)(k-7)}{16}                                    \tag{22}
\]
whenever \(m>k\), or \(m=k\).  Thus a linearly stronger maximum degree
can remain hard only if a quantitatively large missing-edge energy is
present inside its closed neighbourhood.

## 6. Red team: a maximum witness need not align with the dense core

The following asymptotic family refutes the candidate assertion

> every maximum-degree BCM witness \(N[v]\) is aligned with the dense
> larger clique core.

It does not refute Theorem 5.1, (13), or #809.

Fix \(s\in(0,1/2)\) along an integral subsequence and put
\[
u=2sn,\qquad r=\left(\frac12-s\right)n,\qquad
m=u+r=\left(\frac12+s\right)n.
\]
Take disjoint sets
\[
U,\ Z,\ W
\]
of sizes \(u,r,r\), respectively, and choose \(v\in W\).

1. Make \(P=U\cup Z\) a clique of order \(m\), and make \(W\) a clique.
2. Add all \(v\)--\(U\) edges.
3. Add four independent \(Z\)--\(W\) bridges avoiding \(v\).
4. Delete a matching in \(P\) covering every vertex of \(U\) and the
   four \(Z\)-bridge endpoints.

The deleted matching compensates every added edge at its \(P\)-endpoint.
Consequently
\[
\Delta(G)=m-1,
\qquad
A=N[v]=U\cup W.                                               \tag{23}
\]
The true dense larger core is
\[
P=U\cup Z,
\]
but
\[
|A\cap P|=|U|=2sn,
\qquad
|P\setminus A|=|Z|
=\left(\frac12-s\right)n.                                    \tag{24}
\]
Thus \(A\) is not aligned with \(P\).

The graph has
\[
e(G)
=\binom m2+\binom r2+O(n)
=\left(\frac14+s^2+o(1)\right)n^2,
\]
\[
\delta(G)=r-O(1)
=\left(\frac12-s-o(1)\right)n.
\]
It also satisfies \(L_4(2)\) for all sufficiently large \(n\).  Start
from two cliques joined by four independent bridges, which has \(L_4(2)\).
The only deleted edges form a matching inside the larger clique.  Every
exact-four path template can choose its bounded number of spare
within-clique vertices to avoid both the deletion set and the unique
nonneighbour of each used vertex.

### A saturating colouring with zero canonical defect

Give every \(P\)-edge, bridge, and \(v\)--\(U\) edge a fresh colour.
Inject the edges of
\[
W\setminus\bigl(\{v\}\cup
\{\text{four bridge endpoints}\}\bigr)
\]
into the edges of \(Z\) avoiding its four bridge endpoints, and reuse
the image colours.  Give the remaining \(W\)-edges fresh colours.

No paired \(W\)-edge and \(Z\)-edge lie on a common \(C_7\).

- With two bridge crossings, a within-clique segment containing either
  generic paired edge has length at least three, giving length at least
  eight.
- With one bridge and one \(v\)--\(U\) crossing, the \(W\)-segment from
  \(v\) to the bridge endpoint containing a generic \(W\)-edge has
  length at least three.  The \(P\)-segment from a \(U\)-entry to the
  \(Z\)-bridge endpoint containing a generic \(Z\)-edge also has length
  at least three.  Again the total is at least eight.
- Four or more crossings cannot shorten a cycle containing both generic
  paired edges to seven.

Thus every \(C_7\) is rainbow, and the number of colours is
\[
\binom m2+O(n)
=\left(\Phi(n,e)+o(n^2)\right).
\]
For the rotated witness \(A=U\cup W\), every reused \(W\)-edge is good
but its paired \(Z\)-edge is bad.  Therefore
\[
D_A=0.                                                       \tag{25}
\]

This red team establishes two boundaries.

1. The phrase “canonical maximum-degree witness” still needs a
   tie-breaking or existential quantifier: different maximum-degree
   vertices can yield differently oriented closed neighbourhoods.
2. Nonalignment is not itself an obstruction.  The colouring may place
   every reused mate outside the good-edge set, exactly as (13) requires.

## 7. Precise first open gap

After this attack, the unresolved maximum-degree branch has the following
fully reduced form.

- Every repeated good-edge pair has the same centered cover certificate
  (6).
- Its total unpaid defect must be bounded by the exact budget
  \[
  M_B+S_m.
  \]
- The branch is already closed if the maximum-degree excess and
  \(A\)-missing energy satisfy (17).
- The branch is also closed if the rich-outer family satisfies
  (21b)--(21c).
- A maximum witness cannot be assumed to align with the actual dense
  core.

The first missing theorem is therefore:

> **Centered canonical charge.**  Root every non-singleton good colour
> class.  For each nonroot edge use (6), with the common center \(v\), to
> charge it either to a distinct missing edge of \(G[B]\) or to the size
> slack \(S_m\), with total congestion \(1+o(1)\).

Equivalently, prove (13).  A proof must exploit the simultaneous family
of covers
\[
\{x_i,v,x_j\}
\]
inside each colour class; a one-pair no-three-step decomposition cannot
distinguish the rotated family from a genuine obstruction.

By Theorem 5.3, the genuinely uncovered residue may be restricted
further to good edges whose possible outer endpoints have low degree
into \(B\), unless \(M_B\) is already quadratically large enough to
provide substantial budget.

There is a sharp local congestion warning.  For any \(h\), take vertices
\[
v,b,b',x_1,z_1,\ldots,x_h,z_h
\]
and edges
\[
vx_i,\ vz_i,\ bx_i,\ b'z_i
\qquad(1\le i\le h).
\]
Put
\[
A=N[v]=\{v,x_1,z_1,\ldots,x_h,z_h\},\qquad B=\{b,b'\},
\]
and give \(bx_i,b'z_i\) the common colour \(\gamma_i\), using different
colours for different \(i\).  The graph is bipartite and hence contains
no \(C_7\), while
\[
\lambda(b,b')=h.                                             \tag{26}
\]
This sparse graph does not satisfy \(L_4(2)\) or the Case-1 density
conditions.  Its role is precise: the centered certificate, the
induced-matching condition, and the per-colour accounting (6b)--(6d)
alone allow unbounded congestion.  Any proof of (13) must use the global
density/\(L_4(2)\) contract to rule out this incidence pattern.

No bounded-congestion charge of this strength is proved here.

## 8. Verification

`verify_809_third_attack.py` supplies four independent finite guards.

1. For 200 random order-18 graphs, it selects a maximum-degree center
   and checks (7)--(8); 194 instances have nonzero crossing energy.
2. It checks the cleaning theorem on a concentrated missing-star profile
   and a dispersed missing-matching profile.
3. For the finite rotated instance
   \[
   (n,m,r,u)=(20,13,7,6),
   \]
   it verifies:
   \[
   \Delta=12,\quad \delta=6,\quad e=104>20^2/4,
   \]
   \[
   |N[v]|=13,\quad |N[v]\cap P|=6,
   \]
   all 32,680 exact-four endpoint/deletion checks for \(L_4(2)\), the
   non-compatibility of the paired generic edges, and \(D_A=0\).
4. With \(M_B=2<\binom32\) on the same instance, it checks all 64
   rich-outer edges in \(\mathcal F_4\); its 2,016 pairs are already at
   edge distance zero or one.  A separate sharp local profile verifies
   the centered missing-rectangle splice for a genuine distance-two
   pair.

The command

```text
python3 -m unittest -v test_809_third_attack.py
```

returns

```text
Ran 4 tests
OK
```

These computations are finite guards.  Lemmas 3.1 and 4.1--4.3 and
Theorem 5.1 are proved symbolically above.

## 9. Claim boundary

- Center-collapse lemma for \(A=N[v]\): **proved**.
- Maximum-degree domination \(e(A,B)\le2M_A\): **proved**.
- Exact edge-energy and good-surplus identities: **proved**.
- Excess-degree / missing-energy closure (17): **proved, unbounded
  conditional theorem**.
- Positive-width asymptotic regime (21): **proved**.
- Rich-outer compatibility theorem (21a)--(21c): **proved**.
- Every maximum-degree witness aligns with a dense larger core:
  **false by the rotated family**.
- Rotated family satisfies the frozen asymptotic graph contract and has a
  saturating rainbow-\(C_7\) colouring with \(D_A=0\): **proved**.
- Centered canonical charge (13): **open**.
- Maximum-degree BCM branch in full generality: **open**.
- Erdős #809: **open / not claimed**.
