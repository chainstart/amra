# Hub concentration dichotomy for the joint moment

Date: 2026-07-30

## Purpose

`JOINT_OVERLAP_TRIANGLE_MOMENT.md` proves
\[
 {\cal J}\gtrsim L^{10/3-\eta-o(1)}
\]
but the useful benchmark is
\[
 {\cal J}_{\rm target}\gtrsim L^{11/3+\eta-o(1)}.
\]
This note attacks the only remaining obstruction: overlap mass concentrated
on block incidences whose endpoint triangle links survive random truncation
with only constant expectation.

There is a rigorous hub dichotomy.  At the target link threshold
\[
 G=L^{1/3+2\eta},
\]
every block with link weight below \(G\) is incident to a radius vertex
having linearly many large squared-difference blocks.  If most overlap mass
lies between such low-link blocks, their matching structure forces many hub
vertices, and the full block mass gives
\[
 M\gtrsim L^{5/2-3\eta/2-o(1)}.
\]
Otherwise the overlap-weighted triangle link reaches the target scale.

The line-count alternative is short of \(L^{8/3+\eta}\) by
\[
 L^{1/6+5\eta/2}.
\]
Thus the proposed full dichotomy is not proved.  The audit identifies the
precise residual: one needs an improvement over the extremal capacity
\(U^2L^2\) for correlations among blocks covered by \(U\) high-complexity
endpoints, or a proof that saturating that capacity already expands \(M\).

No complete point-set counterexample satisfying small \(M\) was found, and
no exponent breakthrough is claimed.

## 1. Exact size-sensitive triangle link

Write
\[
 s_{uv}=|Y_{uv}|,\qquad Y_{uv}=(Z_u-Z_v)^2,
\]
and choose \(k=\Theta(m)=\Theta(L)\) values from every block.
Conditioned on retaining one value \(a\in Y_{uv}\), the shared-endpoint
argument gives the expected triangle-link lower bound
\[
 R_{uv}
 =c\,mk^2
 \sum_{w\notin\{u,v\}}\frac1{s_{uw}s_{vw}}. \tag{1}
\]
Indeed, for each \(w\), one representation of \(a\) and the \(m\) choices
in \(Z_w\) give at least \(m/2\) distinct compatible pairs.  Uniform
truncation keeps one such pair with probability
\[
 \frac{k}{s_{uw}}\frac{k}{s_{vw}}.
\]

Let \(q_{uv}\) denote the expected ordered overlap mass supported on selected
incidences of block \(uv\).  The random-truncation proof gives
\[
 \mathbb E{\cal J}
\gtrsim\sum_{u<v}q_{uv}R_{uv}. \tag{2}
\]
Thus if a fixed proportion of
\[
 {\cal D}=\sum q_{uv}\gtrsim L^{10/3-\eta-o(1)}
\]
lies on blocks with \(R_{uv}\geq G\), then
\[
 \mathbb E{\cal J}\gtrsim G{\cal D}
\gtrsim L^{11/3+\eta-o(1)}, \tag{3}
\]
which is exactly the desired joint-moment benchmark.

The remaining case is concentration on blocks with \(R_{uv}<G\).

## 2. Low link implies a high-complexity endpoint

Put
\[
 G=L^{1/3+2\eta},\qquad
 S=L^{11/6-\eta-o(1)}. \tag{4}
\]
Call a radius-pair block \(uw\) \(S\)-large when \(s_{uw}\geq S\).
Call a radius vertex \(u\) a hub when it is incident to at least \(cL\)
\(S\)-large blocks, for a sufficiently small fixed \(c>0\).  Let \(U\) be
the hub set.

### Lemma 1 (low-link vertex cover)

After adjusting absolute constants in the definitions, every block
\(uv\) with
\[
 R_{uv}<cG \tag{5}
\]
has at least one endpoint in \(U\).

### Proof

If neither endpoint is a hub, then for at least a fixed positive proportion
of the \(L\) vertices \(w\), both \(s_{uw}<S\) and \(s_{vw}<S\).  Their
contribution to (1) is
\[
 R_{uv}
\gtrsim mk^2\frac{L}{S^2}
\asymp \frac{L^4}{S^2}
=L^{1/3+2\eta+o(1)}=G L^{o(1)}.
\]
Choosing constants and the \(o(1)\) slack contradicts (5). \(\square\)

This is a genuine structural use of the shared endpoint \(w\): a low
triangle link cannot be assigned independently to every block.

## 3. Size and matching bounds for the hub

Under the counterassumption
\[
 M\leq L^{8/3+\eta},
\]
the full incidence mass satisfies
\[
 I_{\rm full}=\sum_{u<v}s_{uv}\leq LM
\leq L^{11/3+\eta}. \tag{6}
\]
Every hub is incident to \(\Omega(L)\) blocks of size at least \(S\), so
\[
 |U|LS\lesssim I_{\rm full}. \tag{7}
\]
In particular,
\[
 |U|\lesssim L^{5/6+2\eta+o(1)}. \tag{8}
\]

The blocks in one product fibre form a matching on the radius vertices.
Since every low-link block is incident to \(U\), there are at most
\[
 |U| \tag{9}
\]
low-link blocks in one product fibre, and at most \(O(|U|L)\) in all
fibres.

Every truncated block has \(k=\Theta(L)\) incidences.  Hence the total
ordered correlation carried by pairs of low-link blocks is at most
\[
 O(|U|L)\cdot k\cdot O(|U|)
=O(|U|^2L^2). \tag{10}
\]

### Lemma 2 (concentrated overlap forces many hubs)

If
\[
 {\cal D}_{\rm low,low}
\gtrsim L^{10/3-\eta-o(1)}, \tag{11}
\]
then
\[
 |U|\gtrsim L^{2/3-\eta/2-o(1)}. \tag{12}
\]

### Proof

Combine (10) and (11), then take square roots. \(\square\)

Finally, the \(\Omega(|U|L)\) \(S\)-large incidences at hub endpoints,
together with \(M\geq I_{\rm full}/L\), give
\[
 M\gtrsim |U|S. \tag{13}
\]
Using (4) and (12),
\[
 M\gtrsim
 L^{2/3-\eta/2}
 L^{11/6-\eta-o(1)}
=L^{5/2-3\eta/2-o(1)}. \tag{14}
\]

## 4. The proved partial dichotomy

Combining Sections 1--3 gives the following rigorous conclusion.

### Theorem 3 (hub concentration partial dichotomy)

At the target line-count counterassumption, at least one of the following
holds:

1. a positive proportion of overlap mass has a high-link orientation,
   and a random truncation has
   \[
   {\cal J}\gtrsim L^{11/3+\eta-o(1)}; \tag{15}
   \]
2. a positive proportion of overlap mass lies between two low-link blocks,
   there is a hub set satisfying (12), and
   \[
   M\gtrsim L^{5/2-3\eta/2-o(1)}. \tag{16}
   \]

### Justification

An unordered overlap between one low-link and one high-link block contributes
an ordered incidence on the high-link side to (2).  Therefore, unless a
positive fraction of the mass is between two low-link blocks, a positive
fraction has a high-link orientation and (3) applies.  In the complementary
case Lemma 2 and (14) apply.

Theorem 3 does **not** improve the Erdős exponent.  Its second alternative
is weaker than the desired line bound.

## 5. Exact residual exponent

The desired alternative is
\[
 M\gtrsim L^{8/3+\eta-o(1)}. \tag{17}
\]
The difference between (17) and (16) is
\[
\left(\frac83+\eta\right)
 -\left(\frac52-\frac32\eta\right)
=\frac16+\frac52\eta. \tag{18}
\]

The loss comes from the sharp abstract capacity (10).  To reach (17) using
the same size threshold \(S\), one would need
\[
 |U|\gtrsim L^{5/6+2\eta-o(1)}, \tag{19}
\]
whereas correlation capacity gives only (12).  The gap in hub size is
again (18).

## 6. Why the evident refinements stop

### Endpoint energy layering

Large \(s_{uv}\) means low additive collision in the signed difference map,
but it does not by itself lower the set-level shifted overlap with a
disjoint same-product block.  Those two blocks use four disjoint radius
classes, so a single hyperbola correlation can be prescribed independently.
An energy improvement must compare many appearances of each hub endpoint
across different fibres.

### Four-vertex compatibility

A same-product overlap pair consists of disjoint radius pairs
\(uv,xy\).  The low-link cover says each pair is incident to a hub, but it
does not force the same hub or a shared height point.  The four endpoint
sets therefore do not yet create a point-level \(K_4\) compatibility test.
The extremal count of low block pairs per fibre is \(\Theta(|U|^2)\), exactly
the capacity used in (10).

### Hölder and Cauchy

Hölder applied to the reciprocal vectors
\[
 (1/s_{uw})_w
\]
can enlarge the unweighted average of \(R_{uv}\).  The hub cover shows why
this does not control the overlap-weighted average: all overlap can still be
placed on the \(|U|L\) covered blocks, up to (10).

## 7. Model obstruction and missing global consistency

The block-size landscape from the previous audit is realizable: generic
height sets on a hub and a common arithmetic progression outside give large
blocks incident to the hub and small outside blocks.  It realizes the
endpoint-size and reciprocal-link part of the obstruction.

We did not construct a complete point set that also has:

1. the geometric radial offsets \(C_{uv}\);
2. overlap mass \(L^{10/3-\eta}\) concentrated near the capacity (10);
3. global line count \(M\leq L^{8/3+\eta}\).

Building such a model requires the shifted hyperbola correlations of
\(\Theta(|U|^2)\) low block pairs in each collection of product fibres to be
realized by the same \(m\)-point hub height sets.  The triangle and joint
moment identities obstruct assigning those correlations independently.

Thus the full proposed dichotomy remains **conditional and unproved**:

> Saturating (10) with genuine shifted squared-difference blocks either
> forces an additional \(L^{1/6+5\eta/2-o(1)}\) line expansion, or raises
> the overlap-weighted triangle link to (3).

This is now the exact global consistency statement.  It is stronger than a
local \(C_4\), single-pair BSG, or marginal endpoint-reuse lemma.

## 8. Verification

`verify_hub_concentration_dichotomy.py` checks all exponent identities, the
finite low-link vertex-cover implication, the product-fibre matching
capacity, and the residual exponent.
