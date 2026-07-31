# Independent root audit — Erdős #809

Date: 2026-07-30

## Verdict

**PASS, with one mandatory scope qualification.**

I found no logical break in the new near-Dirac theorem
\[
e(G)>\lfloor n^2/4\rfloor,\qquad
\delta(G)\ge n/2-o(n)
\quad\Longrightarrow\quad
\chi_{\mathrm{rainbow}\ C_7}(G)\ge n^2/8-o(n^2).
\]
The exact-four-path obstruction lemma, the two structural closures, and
the colour count fit together with the stated quantifiers.

This is **not** a proof of Erdős #809.  Moreover, “the BCM-style
\(k=3\) Case-2 induction step is closed” is correct only as a conditional
statement inside BCM's all-\(e\) strong induction.  It does not eliminate,
invoke a replacement for, or secretly prove the linearly low-minimum-degree
Case 1.

## Itemized audit

| item | verdict | audit finding |
|---|---|---|
| Exact-length-four quantifiers | **PASS** | `FOUR_PATH_OBSTRUCTION_STABILITY.md` assumes the existence of one obstructed ordered endpoint pair after at most one chosen deletion set.  It does not assert a common partition for all pairs or deletion sets.  “Length four” is consistently exactly four edges and all paths are simple. |
| Adding the endpoint edge | **PASS** | A simple \(u\)-to-\(v\) four-edge path cannot use a newly added \(uv\) without repeating an endpoint.  Thus the reduction to \(uv\in E(H)\) preserves the obstruction. |
| Edit-distance bound | **PASS** | With \(t=N-2d\) and \(\Theta=t+4\), the proof gives \(|A|\le2\), \(|Z|\le t+2\), neighbourhood-type errors at most \(2\Theta\) and \(\Theta\), and minority type classes of size at most \(4\Theta\) and \(2\Theta\).  Hence only \(O(|t|+1)\) exceptional vertices remain and summing their incident edges plus regular-vertex errors gives \(O((|t|+1)N)\). |
| Exhaustiveness of two-clique / bipartite alternatives | **PASS** | The essential symmetry estimates are \(|X_U||X_W|\le2\Theta|X|\) and \(|Y_U||Y_W|\le\Theta|Y|\).  They force one dominant type on each side.  The two dominant types cannot have the same orientation: the required contradiction follows from \(N\ge100(t+10)\), which is stronger than the explicit inequality \(N>15t+64\).  The only remaining orientations are complementary, yielding exactly the clique-union and complete-bipartite models. |
| Robust-path \(C_7\) splices | **PASS** | In Lemma 2.1 the deleted endpoints prevent collision with the exact four-edge path.  In Lemma 2.3, edge distance two makes \(x,a,z,y,w\) distinct and excludes \(yw\); a simple three-edge \(y\)-to-\(w\) path in \(G-\{x,a,z\}\) then supplies the other two internal vertices, so the resulting cycle has seven distinct vertices. |
| Dense two-clique closure | **PASS** | In the empty-common-neighbourhood branch, \(P,Q\) are disjoint and anticomplete, \(|P|,|Q|=n/2-o(n)\), and \(\delta(G[P]),\delta(G[Q])=|P|-o(n)\).  The two displayed dense-graph templates contain any specified edge pair in a simple \(C_7\), and \(e(G[P])\ge n^2/8-o(n^2)\). |
| Near-bipartite maximum-cut closure | **PASS** | Maximum-cut local optimality gives every vertex linear crossing degree.  Cleaning leaves all selector pools of size at least \(\tau n\), while each prescribed row or column loses only \(O(\rho n)\), with \(\rho=o(\tau)\).  The ten equal-row/equal-column/disjoint templates are exhaustive and use seven distinct vertices after avoiding a bounded used set.  The rectangle count has normalized minimum \(1/2\). |
| Compatible edges to colour lower bound | **PASS** | Pairwise \(C_7\)-compatible family edges must have pairwise different colours in a colouring in which every \(C_7\) is rainbow.  Both structural closures construct \(n^2/8-o(n^2)\) such edges; the robust-path branch separately handles two-edge colour classes by \(e(G)/2\). |
| \(\varepsilon\)-\(\eta\) order | **PASS** | The diagonal argument correctly converts the sequential theorem into: for each \(\xi\), first choose \(\eta(\xi)\) and \(n_0(\xi)\).  In the induction interface the order is then \(\varepsilon\to\xi=\varepsilon/4\to\eta_0\to\kappa\to n_0\), with \(2\kappa<\eta_0\) and \((\kappa+\kappa^2)/2<\varepsilon/4\).  No uniform quantitative rate for \(\eta(\xi)\) is used. |
| BCM-style Case 2 | **PASS WITH SCOPE QUALIFICATION** | Equations (24)--(27) correctly show that, after the vertex-deletion alternative fails and under the Case-2 density cutoff, the near-Dirac theorem beats the induction potential.  This closes that branch conditional on BCM's strong induction hypothesis.  It does not prove the induction hypothesis in the Case-1 range and therefore does not prove #809. |
| Case-1 reduction | **PASS AS A REDUCTION** | Given the stated BCM outputs \(L_4(2)\) and a set \(A\) of pairwise distance at most three, same-colour good edges have edge distance two or three.  These yield respectively the no-three-step certificate or disjoint outer neighbourhoods.  No colour lower bound inside either fixed-\(s\) profile is claimed. |

## Verification rerun

The current test suite was rerun from its own directory:

```text
python3 -m unittest -v test_809_near_dirac.py
Ran 5 tests — OK
```

The full verifier also passed:

```text
labelled graphs through order 6:             33,864
exact-four-path obstruction profiles:       212,888
actual distance-two / three-path splices:       728
core/hub family pairs covered:              496 / 496
rational rectangle profiles:                80,601
normalized rectangle minimum:               1/2
```

The inherited R004 split-union verifier was rerun separately and passed
its dense, sparse-hub, template-distinctness, and rectangle-count guards.
These are finite guards for formulas and templates, not substitutes for
the asymptotic proofs.

One invocation detail should be recorded: running the unit-test file from
the repository root fails because it imports its sibling verifier as a
top-level module.  Running it from the `erdos809` directory succeeds.  This
is a packaging issue, not a mathematical failure.

## Minimum remaining gaps

### To solve Erdős #809

The minimum mathematical gap is exactly the parameterized Case-1 bound.
For fixed
\[
s=\sqrt{e/n^2-1/4}>0,
\]
one must prove, in each of the two obstruction profiles isolated in
`CASE1_OBSTRUCTION_REDUCTION.md`, at least
\[
\left(\frac18+\frac{s}{2}+\frac{s^2}{2}-o(1)\right)n^2
\]
colours.  The present near-Dirac theorem only handles \(s=o(1)\).

### To make the present result paper-ready

Even without solving #809, the exact-four-path stability theorem could
support a standalone paper only after:

1. a full novelty audit against prescribed-length-path and dense-graph
   stability literature;
2. replacement of the inherited BCM algebra and R004 split theorem by
   explicitly stated, locally checkable lemmas or precise citations;
3. an external graph-theory proof audit;
4. preferably, a broader quantitative theorem than the single near-Dirac
   \(C_7\) application.

The closest preprint already announces an unspecified \(k=3\) Case-2
stability argument, so priority and theorem separation are material.

## Paper-level grade

- **As a solution of #809:** fail; the original problem remains open.
- **As a Q1-ready result today:** not yet.
- **As a mathematical milestone:** strong unbounded partial theorem and a
  credible paper seed.
- **Conservative present grade:** Q2-candidate / Q1-seed, subject to novelty
  clearance and external audit.
- **Clear Q1 route:** close the fixed-\(s\) Case-1 theorem, or generalize the
  exact-length-four obstruction dichotomy into an independently significant
  prescribed-path stability result.

## Claim-language correction

The report's current boundary statements are mostly accurate.  The safest
wording for the Case-2 contribution is:

> The near-Dirac theorem supplies the missing \(k=3\) estimate in the
> low-density Case-2 branch of the BCM strong-induction framework,
> conditional on the framework's induction hypothesis; the complementary
> Case 1 and Erdős #809 remain open.

Any wording suggesting that Case 2 is solved independently of the
all-parameter induction, or that it bypasses Case 1, should be rejected.
