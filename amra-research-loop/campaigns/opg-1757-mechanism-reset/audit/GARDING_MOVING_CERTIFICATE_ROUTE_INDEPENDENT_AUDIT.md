# Independent audit: Gårding moving-certificate route

Date: 2026-08-02
Auditor: `/root/erdos809_lane` (author-swapped; no authorship of the route note)
Verdict: **REPAIR THE INDUCTION CLAIM; REPRESENTATION AND LITERATURE BRIDGE PASS**

## 1. Audited artifact and sources

- `evidence/GARDING_MOVING_CERTIFICATE_ROUTE.md`
  SHA-256 `9e528bc23eabe2fe48aa23a465ceeec60170d9deafc3fcb741408220dae073d5`
- Fang--Ma, *Gårding Polynomials*, arXiv:2604.27755v2.  The v2 TeX source,
  rather than only the abstract, was checked for the definitions, deletion--
  contraction formula, proposition following the definition of `xi_e`, closure
  results, Problem 14.17, and Appendix B.
- Erickson, *Sums of squares and negative correlation for spanning forests of
  series parallel graphs*, arXiv:1008.3660.  The claimed theorem boundary was
  checked against the paper abstract.

No Lean process or other heavy computation was started for this audit.

## 2. `C_M` and forest inversion: pass

Fang--Ma's cospanning-set generating function is

\[
 C_M(\mathbf w)=\sum_{X\subseteq E:\ E\setminus X\text{ independent}}\mathbf w^X.
\]

If

\[
 F_M(\mathbf x)=\sum_{I\text{ independent}}\mathbf x^I,
\]

then, as a Laurent identity,

\[
 C_M(\mathbf w)=\mathbf w^E F_M(\mathbf w^{-1}).
\]

For a cycle matroid, `F_M` is the all-spanning-subgraph, unrooted forest
polynomial (isolated vertices are allowed).  Inversion transforms each marked
Rayleigh difference by a positive monomial factor on strictly positive
activities; the boundary follows by continuity.  Fang--Ma also state the
result directly: graphic `C_M` is Rayleigh exactly when the unrooted
spanning-forest generating function is Rayleigh.  The route's bridge is
therefore correct.

The second implication is also correctly scoped: a multi-affine Gårding
polynomial with nonnegative coefficients is Rayleigh.  Thus graphic
`C`-Gårding is a sufficient, strictly stronger target.  Fang--Ma's Problem
14.17 asks exactly whether graphic matroids are `C`-Gårding.  The paper also
exhibits `S_{M(K_5)}` as non-Gårding; that is an `S` statement and does not
settle the proposed `C` route.

## 3. Proposition 13.9 and `triangleleft`: pass with an important precision

The v2 source gives, for an ordinary non-loop/non-coloop element,

\[
 C_M=(w_e+1)C_{M\setminus e}-\xi_e(M),\qquad
 \xi_e(M)=C_{M\setminus e}-C_{M/e}.
\]

It proves that `xi_e` has nonnegative coefficients and that the following are
equivalent:

1. `M` is `C`-Gårding;
2. there is an `e` for which `M\e` is `C`-Gårding and
   `xi_e(M) triangleleft C_{M\e}`.

The proof says explicitly that it suffices to treat matroids without loops.
The exceptional deletion--contraction formulae are

\[
 C_M=w_eC_{M\setminus e}\quad(e\text{ a loop}),\qquad
 C_M=(w_e+1)C_{M\setminus e}\quad(e\text{ a coloop}).
\]

Consequently, the route's displayed equivalence is faithful in its intended
loopless setting, but a complete induction must retain the loop/coloop
reductions.

The exact meaning of domination is sharper than the route's informal phrase:

\[
 f\triangleleft g\quad\Longleftrightarrow\quad
 f|_{\mathcal C_g}>0,
\]

where `C_g` is the distinguished Gårding positivity component; by convention
`0 triangleleft g`.  For two nonzero Gårding polynomials this is equivalent to
`C_g` being contained in `C_f`.  It is strict positivity on the **entire
distinguished component**, not coefficientwise positivity and not positivity
only on the positive orthant.  In particular, a negative-ray kill point is
valid only after component membership has been established; the inequality
`C_{M\e}>0` alone need not establish that membership.

## 4. Literature boundary: mostly pass; K4 wording needs qualification

- Erickson proves an SOS representation for the Rayleigh difference of the
  spanning-forest polynomial of a series-parallel graph.  This is a Rayleigh
  theorem, not a `C`-Gårding theorem.
- Fang--Ma prove the stronger `S/C`-Gårding result for cycle matroids of
  series-parallel networks, and preservation under series/parallel
  connections and 2-sums.  They also give the direct-sum product formula and
  prove every matroid on at most six elements is `S`-Gårding; the corresponding
  `C` statement follows by duality.
- Hence cactus, block/one-sum, and series-parallel probes are legitimately
  known-class checks rather than frontier cases, provided direct sums and
  the appropriate series/parallel construction are named in the reduction.

Appendix B does contain exactly the displayed identity

\[
 (xy+z-2)(yz+x-2)(xz+y-2)
 -(xyz-1)(x+y+z-3)^2
 =(x-1)^2(y-1)^2(z-1)^2.
\]

However, it is used there to prove a domination decomposition for
`S_{M(K_4)}`, not directly the recursive
`xi_e triangleleft C_{M(K_4)\e}` certificate.  `K4` is covered for `C` by the
six-element theorem/duality (and its cycle matroid is self-dual), so the
route's qualitative analogy is sound, but it must not be cited as an explicit
instance of Proposition 13.9's moving-edge certificate without an additional
derivation.

## 5. Does the proposed "exact next lemma" close the proof?

**Not with only the sentence currently given.**  The proposed lemma supplies
an edge only for loopless 3-connected graphic matroids.  Proposition 13.9
requires `M\e` to be `C`-Gårding, and deletion of an edge from a 3-connected
matroid commonly destroys 3-connectivity.  Therefore recursion restricted to
the stated class does not close.

The lemma *does* become sufficient under the following explicit
minimal-counterexample/strong-induction wrapper:

1. Assume `M` is a graphic non-`C`-Gårding matroid with the least number of
   elements.
2. Remove loops and coloops using their exceptional product formulae; reduce
   disconnected/1-separated cases using direct sums.
3. Use Fang--Ma's series/parallel and 2-sum closure, together with standard
   matroid decomposition, to rule out a proper 2-separation.  The pieces must
   be proper smaller graphic matroids, so minimality applies to both.
4. The remaining minimal counterexample is loopless, simple/cosimple, and
   3-connected.  The at-most-six-element theorem disposes of `|E|<=6`.
5. Apply the moving-edge lemma.  Its deletion `M\e` is a smaller graphic
   matroid whether or not it remains 3-connected, hence is `C`-Gårding by
   minimality.  Proposition 13.9 then contradicts the choice of `M`.

This wrapper is not cosmetic: it is what supplies the deletion hypothesis
when the chosen edge exits the 3-connected class.  The route should therefore
replace “Together with minor induction” by a stated reduction proposition or
by the above least-counterexample argument.  Minor-closedness alone is the
wrong direction for reconstructing `M` from its minors; the direct/2-sum and
series/parallel closure theorems are essential.

The moving-edge lemma is not logically overstrong relative to that wrapper:
it is exactly sufficient on the irreducible 3-connected class.  It is,
however, stronger than the OPG/Rayleigh conclusion and could fail even if OPG
is true, as the route correctly notes.  The deletion base was omitted from
the prose rather than from the mathematical strategy; it is supplied by
strong induction only after the wrapper is made explicit.

## 6. First-host claim

`K5` is a natural first **highly symmetric** host and has only one edge orbit,
but it is not the smallest new 3-connected graphic host beyond the
six-element theorem.  A simple 3-connected graph on five vertices has at
least eight edges, and the four-wheel `W4` attains eight; it is already
non-series-parallel and outside the six-element base.  Thus a resource-aware
search should test `W4` and other 8--9-edge 3-connected hosts before, or in
parallel with, `K5`.  This does not invalidate `K5` as the first symmetric
probe, only any reading of it as the size-minimal frontier.

## 7. Audit disposition

- `C_M`/forest inversion and Rayleigh bridge: **PASS**.
- Proposition 13.9 and nonnegative `xi_e`: **PASS**, with loop/coloop cases
  retained in a full proof.
- Meaning of `triangleleft`: **PASS**, subject to proving distinguished-
  component membership in every kill test.
- Series-parallel and at-most-six literature boundary: **PASS**.
- K4 Appendix B comparison: **QUALIFY**; it is an `S`-domination proof, not
  directly the proposed `C/xi_e` recursion certificate.
- “Exact next lemma + minor induction proves all graphic cases”: **REPAIR**;
  add the minimal-counterexample decomposition wrapper above.
- OPG-1757 promotion: **REJECTED/UNCHANGED**.  No domination lemma or OPG
  statement is proved by the route note.

The repaired route remains a legitimate high-value search program.  Its
first decisive theoretical task is not merely finding an edge certificate;
it is stating and then respecting the irreducible-minimal-counterexample
interface through which that certificate would imply the global theorem.
