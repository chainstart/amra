# OPG-1757 first attack: pooled all-depth boundary closure

Date: 2026-07-31

> **Second-attack update.**  The proposed target \(B_{2s-7}\) has now been
> completely closed.  See `SECOND_ATTACK.md`.  The first open growing-depth
> layer is \(B_{2s-8}\).

## Outcome

The first attack produced an unbounded pooled-kernel theorem instead of
extending another fixed-\(\beta\)-rank window.

For
\[
P_s^{(2)}(\beta,t)=\sum_{n\ge0}\binom tnB_n(s,\beta),
\]
the complete top \(\beta\)-face is now explicit at every depth:
\[
\boxed{
[\beta^{4s-10}]B_n
=4s^{2s-8}n!
\left(
{2s-5\brace n}-{2s-6\brace n}
\right).
}
\]
This proves strict positivity simultaneously for every
\(2\le n\le2s-5\), proves \(B_n=0\) beyond \(2s-5\), and closes the two
deepest pooled layers:
\[
\boxed{
B_{2s-5}
=4s^{2s-8}(2s-5)!\beta^{4s-10},
}
\]
\[
\boxed{
\begin{aligned}
B_{2s-6}
={}&4(2s-6)!\,s^{2s-10}\beta^{4s-12}\\
&\times\left[
s^2+4s-24
+2s(s^2-s-8)\beta
+s^2(s-2)(2s-7)\beta^2
\right].
\end{aligned}
}
\]
Both are coefficientwise strictly positive for every \(s\ge4\).

The detailed proof is in `ALL_DEPTH_TOP_FACE_THEOREM.md`.  This is the
strongest unbounded closure obtained in this attack.

## Materials audited

The attack read the complete previous OPG package in
`q1_four_problem_campaign_2026-07-30/opg1757/`, the main 2026-07-29 OPG
report, and the supporting fixed-page, pooled-Newton, leading-\(F_k\),
component-partition, growing-depth, and TP2-barrier notes and verifiers.

The important inherited facts were:

- fixed-page kernel positivity through \(\beta^8\);
- exact pooled formulas for \(B_2,\ldots,B_7\);
- the all-\(k\) minimal-degree bound
  \(\min\deg_\beta B_k\ge2k\);
- the exact negative fixed-layer TP2 minor;
- the general fixed-page endpoint calculation, but initially only in its
  stable \(s\ge k+3\) formulation.

The last item was not extrapolated into the \(k>s\) region.  The new proof
recomputes the required endpoint directly in the original forest
polynomials.

## Mechanism

### 1. Direct high-degree forest endpoint

Let \(D_k=(H_1^{(k)})^2-H_0^{(k)}H_2^{(k)}\).  A direct positive
component-set-partition evaluation of forests with one, two, and three
components gives, for every \(s\ge4,k\ge2\),
\[
[\beta^{2s+2k-6}]D_k
=4(k-1)k^{2s-6}s^{2k-4}.
\]
After the exact nilpotent normalization
\[
P_s^{(2)}(\beta,k)=(1+s\beta)^{2s-2k-4}D_k,
\]
this becomes
\[
[\beta^{4s-10}]P_s^{(2)}(\beta,k)
=4s^{2s-8}(k-1)k^{2s-6}.
\]
The right side is an ordinary polynomial in \(k\), even where the
normalizing exponent is negative.

### 2. Stirling inversion

Newton inversion sends \(k^m\) to
\(n!{m\brace n}\).  Since
\((k-1)k^{2s-6}=k^{2s-5}-k^{2s-6}\), the all-depth formula follows in one
step.  The Stirling recurrence rewrites its sign as
\[
(n-1){2s-6\brace n}+{2s-6\brace n-1}>0.
\]

### 3. Binary and ternary hyperforest closure

At the next depth \(n=2s-6\), only three \(\beta\)-degrees are possible.
Minimal spoke records consist of binary merges and become ordered weighted
complete-graph forests.  Records with one extra spoke contain exactly one
ternary merge; contracting that merge gives a weighted hyperforest with one
ternary edge.  The ordered-page factorials cancel the pooled binomial
linearization exactly.

Weighted Cayley formulas for one, two, and three ordinary components and
for one and two components after ternary contraction give the bottom two
coefficients.  The all-depth Stirling formula gives the third.  This proves
the displayed complete formula for \(B_{2s-6}\).

## What failed and what was avoided

- Statewise and fixed-layer TP2 remain false; the exact negative
  \((0,1)\) minor was preserved as a firewall.
- No claim was inferred from the finite \(s\le12\) positive triangle.
- The stable-range auxiliary \(K_k\) top coefficient was not used outside
  its stated range.
- Fixed-rank computation was used only as an independent regression audit,
  not as the discovery target or proof.

## Executable audit

Run:

```bash
python3 -m unittest -v test_verify_pooled_top_face.py
python3 verify_pooled_top_face.py \
  --minimum-s 4 --maximum-s 12 --maximum-pages 9
```

Current result:

- 7 unit tests pass;
- 72 direct bipartite component endpoint pairs pass, including many
  \(k>s-3\) points;
- binary/ternary hyperforest endpoint formulas pass for
  \(s=4,\ldots,12\);
- all 1140 nonzero primitive pooled coefficients for \(s=4,\ldots,12\)
  were regenerated;
- the top face and both deepest-layer formulas agree exactly;
- certificate digest:
  `a81eaebd995ab87e5911718c7f68a4cc2129329be1cf014f8b2e88d9bed2ad8f`.

The 1140-row interior sign check remains explicitly finite-only.

An independent red-team also brute-force checked the negative-exponent
normalization at \(s=4,k=2,\ldots,5\), extended the binary/ternary endpoint
audit through \(s=16\), and found no fatal gap.  Its verdict is recorded in
`INDEPENDENT_AUDIT.md`.

## First remaining gap

The first unresolved growing-depth layer is
\[
B_{2s-7}.
\]
It has only five possible coefficients:
\[
4s-14\le\deg_\beta B_{2s-7}\le4s-10.
\]
The top one is already positive by the Stirling theorem.  The lower four
require exactly the following bounded excess mechanisms:

- ordinary binary forests;
- one ternary merge;
- two ternary merges;
- one quaternary merge;
- one overlap between the active-page sets.

This is more precise than the former “prove every \(B_n\)” gap.

## Recommended second attack

1. Define the excess-two forest species
   \(\Psi^{(3,3)},\Psi^{(4)}\), and the one-overlap two-colour species.
2. Prove ordered-chain identities analogous to
   \([\beta^{2j+1}]A_{h,j}=j![x^j]\Psi_h\).
3. Evaluate only the near-spanning component layers needed for the five
   coefficients of \(B_{2s-7}\).
4. Factor the results after the \(s\mapsto s-4\) shift and audit them
   independently against the primitive transfer.
5. If successful, formulate a fixed-depth-deficit theorem: for every fixed
   \(q\), \(B_{2s-5-q}\) is coefficientwise positive for all \(s\) beyond
   an explicit boundary, with finitely many small \(s\) handled exactly.

Step 5 is the most plausible route from this milestone to a result with
standalone high-impact potential.  It would convert two isolated deepest
layers into an infinite tail theorem.

## Publication and scope assessment

The new result is mathematically substantive: it is the first theorem here
that controls every pooled depth simultaneously, and it closes two layers
whose indices grow with \(s\).  It is suitable as a strong structural
section of an OPG paper.

It is not yet a Q1-level resolution by itself.  The complete
\(\alpha^2\) layer remains open, and the result concerns the
complete-split model rather than arbitrary-host OPG-1757.  A credible
Q1-level central theorem would be one of:

- all \(B_n\ge_{\rm coeff}0\);
- the fixed-depth-deficit theorem proposed above;
- a broader complete-split Rayleigh theorem containing this layer;
- an extension of the pooled mechanism beyond the model family.

## Current literature boundary

The July 31 boundary check found no collision with the closest identified
2026 preprints:

- Tang--Zhang, [arXiv:2603.10738](https://arxiv.org/abs/2603.10738), treats
  uniform spanning subgraphs of \(K_n\), including fixed-component forests
  for sufficiently large \(n\), not the present complete-split
  coefficientwise pooled theorem.
- Fang--Ma, [arXiv:2604.27755v2](https://arxiv.org/abs/2604.27755), gives
  Gårding/Rayleigh results for stated matroid classes but does not place
  this complete-split graphic family in those classes.
- The newer Fang--Ma ideal-Gårding preprint,
  [arXiv:2607.16832v1](https://arxiv.org/abs/2607.16832), is structural;
  its current text contains no forest or graphic-family application that
  subsumes this result.

This comparison is a scope firewall, not a completed worldwide priority
opinion.  Official arXiv records were cross-checked with an OpenAlex search
over the combined complete-split/Rayleigh/forest/negative-correlation
keywords; it found the same nearby works and no additional direct theorem,
but database non-retrieval is not evidence of nonexistence.
