# Erdős #809 — first attack on the Case-1 linkage defect

Date: 2026-07-31

Status:
`RAW_LD_REFUTED__A_ORIENTATION_REPAIRED__BUDGET_TARGET_REQUIRES_WITNESS_QUANTIFIER`

Postscript after the second attack: `SECOND_ATTACK.md` proves that the
budgeted-defect inequality is also false when quantified over **every**
admissible \(A\).  In this file, “the correct closure target” means the
exact algebraic target for a fixed selected witness; a global theorem
must use an existential/canonical BCM witness quantifier.

## 1. Main outcome

The proposed raw linkage-defect estimate
\[
\sum_\gamma (|M_\gamma|-1)_+=o(n^2)                           \tag{LD}
\]
is **false under the frozen Case-1 contract as currently stated**.

There is an asymptotic counterexample family satisfying

- \(e(G)=(1/4+s^2+o(1))n^2\);
- \(\delta(G)\ge(1/2-s-o(1))n\);
- the full robust exact-four-path property \(L_4(2)\);
- a permitted set \(A\) of size at least
  \((1/2+s-o(1))n\) and diameter at most three;
- a colouring in which every \(C_7\) is rainbow;

but for which
\[
\sum_\gamma (|M_\gamma|-1)_+
=\left(\frac{(1/2-s)^2}{2}+o(1)\right)n^2.                    \tag{1}
\]

This does **not** refute Erdős #809.  The same colouring uses
\[
\left(\frac12\left(\frac12+s\right)^2+o(1)\right)n^2
=\left(\frac18+\frac s2+\frac{s^2}{2}+o(1)\right)n^2
\]
colours, exactly the BCM target.  It refutes only the claim that every
repeated good edge must be a lower-order error.

For a fixed selected witness, the exact good-edge closure target is the
**budgeted defect**
\[
\boxed{
\sum_\gamma (|M_\gamma|-1)_+
\le |E_{\rm good}|-T(s)n^2+o(n^2),
}
\qquad
T(s)=\frac18+\frac s2+\frac{s^2}{2}.                          \tag{BD}
\]
Unlike (LD), (BD) credits the surplus when the selected \(A\) makes
\(|E_{\rm good}|\) substantially larger than its guaranteed lower bound.

There is also a separate endpoint-orientation repair.  One must first
choose globally closest endpoints and only then record where the selected
\(A\)-endpoints lie.  Forcing the inner endpoints to lie in \(A\) can
produce a shortest \(A\)-path contaminated by one of the specified outer
endpoints; in that case even a constant outer-codegree conclusion is
false.

## 2. Complete repair of the endpoint taxonomy

Let \(xy,zw\) be two same-colour good edges.  Choose and fix
\[
x\in A\cap\{x,y\},\qquad z\in A\cap\{z,w\};
\]
thus \(y,w\) denote the complementary endpoints.

The \(L_4(2)\) argument makes the two edges an induced matching and
excludes edge distance zero or one.  The two selected \(A\)-endpoints have
distance at most three, so
\[
d(x,z)\in\{2,3\}
\]
and the global edge distance is two or three.

### Lemma 2.1 (complete \(A\)-oriented three-certificate taxonomy)

Exactly one of the following usable situations holds.

1. **A2:** \(d(x,z)=2\).  If \(x-a-z\) is a shortest path, then
   \[
   \tau_3(y,w)\le3,
   \]
   witnessed by \(\{x,a,z\}\).
2. **A3-clean:** \(d(x,z)=3\), and there is a shortest path
   \[
   x-a-b-z
   \]
   with \(\{a,b\}\cap\{y,w\}=\varnothing\).  Then
   \[
   N(y)\cap N(w)\subseteq\{a,b\},
   \]
   so the outer codegree is at most two.
3. **A3-contaminated:** \(d(x,z)=3\), and every three-edge
   \(x\)-to-\(z\) path meets \(\{y,w\}\).  Then the two specified outer
   endpoints themselves form a path cover:
   \[
   \tau_3(x,z)\le2.                                           \tag{2}
   \]

Here \(\tau_3(r,t)\) is the minimum number of internal vertices meeting
every simple three-edge \(r\)-to-\(t\) path.

#### Proof

In A2, the internal vertex \(a\) cannot be \(y\) or \(w\): otherwise one
of the forbidden cross edges \(yz,xw\) would exist.  Any three-edge
\(y\)-to-\(w\) path avoiding \(\{x,a,z\}\) would splice with
\[
y-x-a-z-w
\]
to form a \(C_7\).

In A3-clean, take
\[
c\in N(y)\cap N(w)\setminus\{a,b\}.
\]
The vertex \(c\) cannot be \(x\) or \(z\), again because the two specified
edges form an induced matching.  Hence \(x-a-b-z\) and \(y-c-w\) are
vertex-disjoint paths of lengths three and two and form a forbidden
\(C_7\) with the specified edges.

Finally, if no clean three-path exists, the definition says exactly that
\(\{y,w\}\) meets every three-edge \(x\)-to-\(z\) path, proving (2).
\(\square\)

This is the safe taxonomy when the charging scheme insists on retaining
the selected \(A\)-endpoints.

### Equivalent closest-endpoint four-profile taxonomy

Choose a globally closest pair
\[
u\in\{x,y\},\qquad v\in\{z,w\},
\]
and write \(u',v'\) for the complementary endpoints of their respective
edges.  There are exactly four profiles, after identifying the two
symmetric mixed cases.

| profile | global distance | position of closest endpoints | certificate |
|---|---:|---|---|
| D2-AA | 2 | \(u=x,\ v=z\) | \(\tau_3(y,w)\le3\) |
| D2-AO | 2 | exactly one of \(u,v\) is the selected \(A\)-endpoint | \(\tau_3(u',v')\le3\) |
| D2-OO | 2 | \(u=y,\ v=w\) | \(\tau_3(x,z)\le3\) |
| D3 | 3 | all endpoint pairs have distance at least 3; \(x,z\) are a closest pair | \(N(y)\cap N(w)=\varnothing\) |

### Lemma 2.2 (four-profile certificate taxonomy)

The four rows above are exhaustive and their certificates are valid.

#### Proof

If \(d(u,v)=2\), choose a shortest path \(u-a-v\).  Any simple
three-edge \(u'\)-to-\(v'\) path avoiding \(\{u,a,v\}\), together with
\[
u'-u-a-v-v',
\]
would form a simple \(C_7\) containing both same-colour edges.  Hence
\[
\tau_3(u',v')\le3.                                            \tag{3}
\]
Whether \(u,v\) are the two selected \(A\)-endpoints, exactly one of
them, or neither gives D2-AA, D2-AO, and D2-OO.

If the global edge distance is three, the chosen \(A\)-endpoints
\(x,z\) have distance at most three and hence exactly three.  Moreover
the complementary endpoints \(y,w\) also have distance at least three.
They therefore have no common neighbour:
\[
N(y)\cap N(w)=\varnothing.                                   \tag{4}
\]
This is D3.  The cases are exhaustive. \(\square\)

The sentence in `CASE1_SECOND_ATTACK.md` that simultaneously takes
\(x,z\in A\) and makes them the globally closest endpoints is justified
only in D2-AA and D3.  D2-AO and D2-OO are missing from the proposed
\(A\)-based charging plan.

### Two finite orientation guards

First take vertices \(x,y,z,w,a,b\), specified edges \(xy,zw\), and add
\[
xa,\ ab,\ bz,\ ya,\ yb,\ wa,\ wb.
\]
Put \(A=\{x,z\}\).  Then
\[
d(x,z)=3,\qquad d(y,w)=2,\qquad
N(y)\cap N(w)=\{a,b\}.
\]
The specified edges are induced and cannot lie on a \(C_7\), since the
graph has only six vertices.  Thus the selected \(A\)-endpoints need not
be globally closest.

There is a stronger contamination obstruction.  For any \(r\), take
vertices
\[
x,y,z,w,a,c_1,\ldots,c_r
\]
and edges
\[
xy,\ zw,\ ya,\ az,\quad yc_i,\ wc_i\quad(1\le i\le r).
\]
Again put \(A=\{x,z\}\).  The path \(x-y-a-z\) shows
\(d(x,z)=3\), but it is contaminated by the specified outer endpoint
\(y\), while
\[
|N(y)\cap N(w)|=r.
\]
The vertex \(x\) has degree one, so no cycle contains \(xy\); the two
specified edges may receive the same colour in a rainbow-\(C_7\)
colouring.  Hence an \(A\)-oriented distance-three path gives no constant
codegree bound unless one separately proves that an internal
\(x\)-to-\(z\) geodesic avoids \(\{y,w\}\).

In this family every length-three \(x\)-to-\(z\) path uses \(y\), so it
falls in A3-contaminated and its correct certificate is
\(\tau_3(x,z)\le1\), not a codegree bound.

## 3. Counterexample family to raw (LD)

Fix \(0<s<1/2\).  Take integer sequences
\[
p+q=n,\qquad
\frac pn\longrightarrow\frac12+s,\qquad
\frac qn\longrightarrow\frac12-s,
\]
with \(p\ge q\) and \(q\to\infty\).

Let \(P,Q\) be disjoint sets of sizes \(p,q\).  Start with
\[
K_P\cup K_Q
\]
and add four independent bridge edges
\[
p_iq_i,\qquad 1\le i\le4,
\]
where the eight bridge endpoints are distinct.  Call the resulting graph
\(G_{p,q}\).

### 3.1 Density and minimum degree

We have
\[
\begin{aligned}
e(G_{p,q})
&=\binom p2+\binom q2+4\\
&=\left(\frac14+s^2+o(1)\right)n^2,
\end{aligned}
\]
and
\[
\delta(G_{p,q})=q-1
=\left(\frac12-s-o(1)\right)n.
\]
For fixed \(s>0\), \(e(G_{p,q})>\lfloor n^2/4\rfloor\) for all sufficiently
large \(n\).

### 3.2 Diameter-three witness

The graph has diameter at most three.  Vertices in the same clique are
adjacent.  Given \(u\in P,v\in Q\), choose a bridge \(p_iq_i\) whose two
endpoints avoid \(u,v\); then
\[
u-p_i-q_i-v
\]
has length three.  Hence the frozen contract permits
\[
A=V(G_{p,q}).
\]
Every edge is then good.

### 3.3 Robust exact-four paths

The graph \(G_{p,q}\) satisfies \(L_4(2)\) once \(p,q\) are sufficiently
large.

Delete any set \(T\) of at most two vertices.  At least two of the four
independent bridges survive.

- Two endpoints in the same clique have a four-edge simple path entirely
  inside that clique.
- For endpoints \(u\in P,v\in Q\), if a surviving bridge \(p_iq_i\)
  avoids both endpoints, choose a spare \(a\in P\) and use
  \[
  u-a-p_i-q_i-v.
  \]
- If a surviving bridge is incident with exactly one endpoint, traverse
  that bridge and use three clique edges on the other side.
- If \(u=p_i,v=q_i\) are the endpoints of one surviving bridge, use a
  second surviving bridge \(p_jq_j\) and a spare \(b\in Q\):
  \[
  u-p_j-q_j-b-v.
  \]

All spare vertices can avoid \(T\) and the bounded displayed set because
\(p,q\to\infty\).  This covers every endpoint configuration.

The use of four bridges is deliberate.  With only three bridges, deleting
two bridge endpoints can leave a surviving bridge whose own endpoints
need not admit an exact four-edge path.

## 4. A rainbow-\(C_7\) colouring with quadratic defect

Put
\[
P^\circ=P\setminus\{p_1,p_2,p_3,p_4\},\qquad
Q^\circ=Q\setminus\{q_1,q_2,q_3,q_4\}.
\]
Since \(p\ge q\), inject the edges of \(K_{Q^\circ}\) into the edges of
\(K_{P^\circ}\).  Give each edge of \(K_{Q^\circ}\) the same colour as
its assigned image, and give every remaining edge a fresh colour.

No assigned pair lies on a common \(C_7\).  Indeed, a cycle meeting both
cliques uses an even positive number of bridge edges.

- Four bridge crossings already require four nonempty internal segments,
  since the bridge edges form a matching, so such a cycle has length at
  least eight.
- With two bridge crossings, the cycle consists of the two bridges and
  one path inside each clique between bridge endpoints.  A path containing
  an edge of \(K_{P^\circ}\) has length at least three, and the same holds
  in \(Q\).  The cycle again has length at least
  \[
  2+3+3=8.
  \]

Thus every \(C_7\) is rainbow.  Since \(A=V(G_{p,q})\), every paired edge
is good and
\[
\begin{aligned}
\sum_\gamma(|M_\gamma|-1)_+
&=\binom{q-4}{2}\\
&=\left(\frac{(1/2-s)^2}{2}+o(1)\right)n^2.
\end{aligned}                                                 \tag{4}
\]
This proves that raw (LD) is false.

The number of colours is
\[
\begin{aligned}
e(G_{p,q})-\binom{q-4}{2}
&=\binom p2+4q-6\\
&=\left(\frac12\left(\frac12+s\right)^2+o(1)\right)n^2\\
&=(T(s)+o(1))n^2.
\end{aligned}                                                 \tag{5}
\]
Therefore the family saturates, rather than violates, the conjectured
lower bound.

## 5. The exact corrected closure target

Let
\[
D_A=\sum_\gamma(|M_\gamma|-1)_+.
\]
The exact number of colours appearing on good edges is
\[
c_A=|E_{\rm good}|-D_A.                                      \tag{6}
\]
Consequently the good-edge route reaches the BCM target exactly when
\[
D_A\le |E_{\rm good}|-T(s)n^2+o(n^2).                         \tag{7}
\]
This is (BD).

Equation (7), rather than \(D_A=o(n^2)\), is the minimum algebraically
correct linkage-defect target.  On the bridge family,
\[
|E_{\rm good}|-T(s)n^2
=\left(\frac{(1/2-s)^2}{2}+o(1)\right)n^2,
\]
and (4) consumes precisely that quadratic allowance.

There are two possible ways to continue.

1. **Budgeted charging.**  Charge repeated good edges only after reserving
   the surplus \(|E_{\rm good}|-T(s)n^2\).  Zero-codegree pairs across a
   two-clique cut are allowed to consume the smaller-clique budget.
2. **Canonical witness selection.**  Strengthen the BCM use of Lemma 3.1
   by selecting a diameter-three witness \(A\) concentrated on the
   appropriate high-degree/large-clique core, and prove raw (LD) only for
   that selected witness.

The second option needs an actual selection lemma.  Merely requiring
\(|A|=(1/2+s+o(1))n\) is insufficient: in the bridge family a set of that
size can still take linear portions from both cliques, producing
quadratically many repeated good pairs.  The quantifier must be
existential/canonical, not “for every diameter-three \(A\) of the right
size.”

## 6. Consequence for bounded-congestion charging

No charging argument can prove raw (LD) from the frozen contract alone.
In the counterexample, there are quadratically many legitimate
zero-codegree certificates across the two-clique cut.  A bounded-
congestion charge to those pairs or to missing cross adjacencies gives an
\(O(n^2)\) bound, which is sharp, not \(o(n^2)\).

The charging theorem must therefore distinguish:

- **paid defects**, supported by the structural surplus above \(T(s)n^2\);
- **unpaid defects**, which must total \(o(n^2)\).

The remaining high-value lemma in this route must be quantifier-safe:

> Under the genuine BCM Case-1 hypotheses, select a witness from the
> actual branches of BCM Lemma 3.1 and prove the budgeted defect
> inequality (7) for that witness, preferably by a stability dichotomy
> in which the only quadratic defect is reuse across an asymptotic
> two-clique decomposition.

That existential/canonical statement is still open.  The universal
version is false by `SECOND_ATTACK.md`.

## 7. Claim boundary

- Four-profile closest-endpoint/\(A\)-position taxonomy:
  **proved, general graph lemma under the stated structural assumptions**.
- Simultaneous “\(A\)-oriented and globally closest” choice:
  **false in general**.
- Any constant outer-codegree bound from an arbitrary \(A\)-oriented
  distance-three geodesic: **false because of contaminated geodesics**.
- Zero outer codegree in the global-distance-three profile:
  **proved**.
- Raw linkage defect (LD) under the frozen contract:
  **false; explicit asymptotic counterexample family**.
- Budgeted defect (BD) as the exact good-edge closure target:
  **proved algebraic equivalence**.
- Budgeted defect inequality for every admissible \(A\):
  **false by `SECOND_ATTACK.md`**.
- Existence of a BCM branch-generated \(A\) satisfying budgeted defect:
  **open**.
- Erdős #809:
  **open**.
