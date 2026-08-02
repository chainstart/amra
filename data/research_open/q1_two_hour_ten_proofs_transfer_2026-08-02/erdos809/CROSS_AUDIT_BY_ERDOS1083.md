# Independent cross-audit by the Erdős #1083 lane

Date: 2026-08-02

Formal verdict: **PASS_AFTER_REPAIR**

Mathematical verdict: **PASS**.  The only repair is the missing backslash in
one `\qquad` at line 70 of the palette manuscript.  It changes no statement,
hypothesis, formula, or proof.

Public-problem verdict: **Erdős #809 remains OPEN / NOT CLAIMED**.

## 1. Independence and audited snapshot

The audit reconstructed the claims from the two theorem statements and did
not import or call either author verifier.  The author-freeze hashes were

```text
4eb83fbe8d3ecaa030215a157d530f09e8f26c2ff7c203c56ca3a0f4bfb153da  MAXIMUM_WITNESS_NEAR_SHARP_STABILITY.md
207896890131d1de0059031dbd147e6370be0cc8cda1204b9bd0b22d6b7d42f3  TEN_PROOFS_PALETTE_RESERVE_TRANSFER.md
2787b2fa673f688492d988abcdaf1ee15c29cd943d85333e4e9c3441815239b9  CLAIM_LEDGER.md
```

Only the palette manuscript changed during audit, from `,qquad` to
`,\qquad`.  The independent executable is
`verify_cross_audit_by_erdos1083.py`.

## 2. Verdict matrix

| Item | Verdict | Independent reconstruction |
|---|---|---|
| Induced-matching theorem | **PASS** | Both edge-distance-zero/one splices make a simple seven-cycle |
| Full \(2^t\) label gauge | **PASS** | Each matching edge can be flipped independently; its outer bit is arbitrary |
| Sharp graph and recolouring | **PASS** | 18 graphs and 144 repeated classes rebuilt without author code |
| Repeated-colour \(C_7\) pairing | **PASS** | The two pairings cost at least \(4+2\) and \(3+3\) remaining edges |
| Exact defect and reserve | **PASS** | \(D_B=g\); 1,245 actual reserve pairs enumerated and the closed formula recovered |
| Even and odd factorizations | **PASS** | 13,313,069 scalar profiles; exact integer identities in both parities |
| Minimum-degree to vertex-deficit conversion | **PASS** | Exact identity, including the \(a-2\) and \(a-1\) terms |
| Parity/ranges of \(a,h,u\) | **PASS** | \(a\equiv n\pmod2\), \(0\le h\le2g-a-3\), \(0\le u\le h\) |
| Near-band constants | **PASS** | First parameter-shift costs \(8,6\); first residual-gap cost \(2g-2\) |
| \(g=4\) firewall | **PASS** | Both rows are used only as graph/colour boundary rows; \(L_4(2)\) is asserted only for \(g\ge5\) |
| Quantifier/public-problem firewall | **PASS** | Branch A, B-same, general B-opposite LRH, and other BCM branches remain open |
| Palette line 70 | **REPAIRED** | Missing TeX backslash only; no mathematical content changed |

## 3. Induced matching and the label gauge

Suppose equal-colour edges share a vertex, say \(xy,xz\).  Since
\(\delta(G)\ge3\), choose

\[
 u\in N(y)\setminus\{x,z\}.
\]

The \(L_4(2)\) property supplies an exact four-edge \(u\)-to-\(z\) path
after deleting \(x,y\).  Adding \(xy,yu,zx\) gives a simple \(C_7\)
containing the two equal-colour edges.  If disjoint equal-colour edges
\(xy,zw\) have a cross edge \(xz\), an exact four-edge \(y\)-to-\(w\)
path after deleting \(x,z\), together with \(xy,xz,zw\), gives the same
contradiction.  Thus each colour class is an induced matching.

On the incident vertices of a \(t\)-edge matching, a proper two-labeling
chooses one endpoint bit independently on each edge and forces the other bit.
There are exactly \(2^t\) choices, and any prescribed word on designated
outer endpoints occurs.  Isolated vertices were correctly excluded from the
exact \(2^t\) count in the statement.

## 4. Sharp recolouring and actual reserve

Deleting the two edges \(bx_i,cy_i\) of one repeated class from a hypothetical
seven-cycle leaves two paths of total length five.  Their endpoint pairing is
one of

\[
 (b,c),(x_i,y_i),\qquad (b,y_i),(x_i,c).
\]

The first pairing needs at least \(4+2=6\) edges: a path of length at most
three from \(b\) to \(c\) would require either a common neighbour in
\(P\cap U\) or an edge from \(P\) to \(U\).  The crossed pairing needs at
least \(3+3=6\), because \(N(b)=P\) has no common neighbour with
\(y_i\in U\), and symmetrically for \(x_i,c\).  Therefore no \(C_7\)
contains both members of a repeated class.  All other colours are fresh, so
the recolouring is rainbow on every \(C_7\).

Relative to \(A=N[v]\), both edges of each of the \(g\) doubled classes are
good cross edges.  Each saves exactly one colour, so \(D_B=g\).

For the reserve calculation, write

\[
 r_P=|N(v)\cap P|,\qquad r_U=|N(v)\cap U|,
 \qquad r_P+r_U=\Delta.
\]

Since \(|B|=n-\Delta-1\), the missing degrees of \(b,c\) inside \(B\)
are

\[
 |B|-1-(\delta-r_P),\qquad |B|-1-(\delta-r_U).
\]

Their missing stars meet exactly in the missing pair \(bc\).  Hence their
union has size

\[
 2(|B|-1)-2\delta+\Delta-1
 =\delta+2\kappa-g-5.
\]

This equals \(g^2+g-11\) in even order and \(g^2+g-8\) in odd order,
and is at least \(g\) for every \(g\ge4\).  Thus the stated injection of
the \(g\) doubled colours into actual missing pairs is literal.

The audit rebuilt both parity graphs for \(4\le g\le12\), checking edge
count, all degrees, the bridge-side neighbour lower bounds, the 144 repeated
classes, and the actual reserve sets.  The two \(g=4\) rows were deliberately
counted only as graph/colour boundary rows.  The manuscript invokes the
previously audited \(L_4(2)\) property only for \(g\ge5\); no hidden
\(g=4\) use was found.

## 5. Exact stability reconstruction

Put \(p=\delta+u\), \(d=\kappa-h-1\).  Then

\[
 n-d-1=2\delta+h,
 \]

and the relaxed missing-pair lower bound before minimizing the centre is

\[
 \mathcal L(p)=p(n-d-1-p)+n-1
 +(d-1)(n-2-\Delta)-\binom{d-1}{2}.
\]

The two allowed endpoints are \(\delta,\delta+h\), where the quadratic has
the same value, and direct subtraction gives

\[
 \boxed{\mathcal L(\delta+u)-\mathcal L(\delta)=u(h-u).}
\]

Thus the sign of the centre term is positive.  The independent hostile check
also used \(h=2,u=1\), where the excess is exactly one; reversing the sign
fails already at this first interior point.

For even order, with \(\delta^*=g^2-2g-2\), exact expansion gives

\[
 \mathcal L(p)-\overline M
 =\delta-\delta^*
 +\frac{a^2-4+2h(2g-h-1)}4+u(h-u).
\]

For odd order, with \(\delta^*=g^2-2g-1\), it gives

\[
 \mathcal L(p)-\overline M
 =\delta-\delta^*
 +\frac{a^2-1+2h(2g-h-1)}4+u(h-u).
\]

Because \(n=2\delta+\kappa\) and \(\kappa=2g-a\), the vertex deficit is
exactly

\[
 T=2(\delta^*-\delta)+(a-2)
 \quad\text{or}\quad
 T=2(\delta^*-\delta)+(a-1).
\]

Writing \(\mathcal E\) for the right side of (E) or (O), the audit obtains
the single exact identity

\[
 \boxed{T-\mathcal E=-2\bigl(\mathcal L(p)-\overline M\bigr).}
\]

The necessary graph inequality \(\mathcal L(p)\le\overline M\) is therefore
equivalent to \(T\ge\mathcal E\), confirming both factorizations and the
direction of every inequality.

Parity is also forced rather than assumed: \(\kappa\equiv n\pmod2\), so
\(a=2g-\kappa\) is even in even order and odd in odd order.  From
\(2\le d\le\kappa-1\) and \(p\in[\delta,\delta+h]\),

\[
 0\le h\le\kappa-3=2g-a-3,
 \qquad 0\le u\le h.
\]

The first nonbaseline \(a\) is \(4\) in even order and costs \(8\), or
\(3\) in odd order and costs \(6\).  For \(h\ge1\), concavity of
\(h(2g-h-1)\) on its admissible interval puts its minimum at an endpoint.
At \(h=1\) it is \(2g-2\); at the other endpoint its excess is

\[
 (a+1)(2g-a-4)\ge0.
\]

This verifies the strict near-band thresholds.  The strict inequality is
essential: at costs \(8\), \(6\), or \(2g-2\), a first shifted profile is
not excluded.  Finally, with \(m=\min\{u,h-u\}\),

\[
 2u(h-u)=2m(h-m)\ge mh,
\]

which confirms the arbitrary-deficit centre localization.  Substituting the
near-band values \(d=2g-3\) and \(2g-2\) into the inherited one-leaf bound
\(Z\ge d-g\) gives exactly \(g-3\) and \(g-2\).

## 6. Executable result and scope

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_cross_audit_by_erdos1083.py
```

The script reports `pass: true` after 13,313,069 independent scalar profiles,
26,165,382 feasible profile instances over three choices of \(\delta\), 18
rebuilt sharp graphs, 144 repeated classes, and 1,245 actual reserve pairs.
Finite checks guard identities and boundary examples; the displayed algebra
and splice arguments prove the unbounded statements.

The palette obstruction and the conditional B-opposite stability theorem do
not prove label--reserve Hall expansion, do not handle Branch A or B-same, and
do not close the other BCM branches.  They neither prove nor refute Erdős
#809.
