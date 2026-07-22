# Erdős #25: harmonic-weighted compatible cliques

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous sufficient condition for the logarithmic density in the
official problem; not a full solution.

## 1. Arithmetic boundary weight

Use the globally reduced compatibility graph at cutoff `X` from
`LOG_AVERAGED_CLIQUE_ENTROPY.md`.  For every nonempty compatible clique `Q`,
let

\[
 L_Q=\mathop{\rm lcm}_{i\in Q}n_i,
 \qquad M_Q=\max_{i\in Q}n_i,
\]

and let `r_Q in {1,...,L_Q}` be the least positive representative of the
joint CRT class (the zero residue is represented by `L_Q`).  Define

\[
 {cal B}(X)=1+\sum_{\substack{Q\text{ compatible}\\Q\ne\varnothing}}
 \left\{\frac2{r_Q}+\frac{2+\log(2L_Q)}{L_Q}\right\}.       \tag{1}
\]

The sum is over actual cliques, not all subsets.

## 2. Theorem

If

\[
 \boxed{{\cal B}(X)=o(\log X),}                            \tag{2}
\]

then the activated survivor `A` has logarithmic density

\[
 \delta=\lim_{X\to\infty}\delta_X,                         \tag{3}
\]

where `delta_X` is the periodic density after forbidding all complete classes
whose moduli are at most `X`.

Condition (2) is arithmetic rather than purely combinatorial.  It may hold
even when the unweighted clique count is much larger than `X`, provided that
the joint CRT representatives and least common multiples make most boundary
terms cheap.

## 3. A progression lemma

Let `1<=r<=L`, `1<=M<=L`, and

\[
 S_{L,r,M}(X)=
 \sum_{\substack{m\le X,\ m\equiv r\pmod L\\m\ge M}}\frac1m.
\]

Then, uniformly in all parameters,

\[
 \left|S_{L,r,M}(X)-\frac{\log X}{L}\right|
 \le \frac2r+\frac{2+\log(2L)}L.                         \tag{4}
\]

To prove this, first omit the condition `m>=M`.  If the progression is
nonempty below `X`, write its terms as `r+kL`.  For `k>=1`,

\[
 \frac1{(k+1)L}\le\frac1{r+kL}\le\frac1{kL}.
\]

The integral bounds for harmonic numbers, together with
`X/L` lying between the last index and that index plus two, give

\[
 \left|\sum_{\substack{m\le X\\m\equiv r\pmod L}}\frac1m
       -\frac{\log X}{L}\right|
 \le \frac1r+\frac{2+\log(2L)}L.                         \tag{5}
\]

The same inequality is immediate when the progression has no term or only
its first term below `X`.  Finally, because `M<=L`, activation deletes at
most the single representative `r` from the complete progression.  Its
weight is at most `1/r`, proving (4).

The representative convention matters: replacing `r_Q` by `M_Q` would be
false when a very small complete-class representative is removed at
activation.

## 4. Proof of the theorem

Let

\[
 H_A(X)=\sum_{\substack{m\le X\\m\in A}}\frac1m.
\]

Finite inclusion--exclusion over the activated slices gives one term
`S_(L_Q,r_Q,M_Q)(X)` for every compatible clique, with the usual alternating
sign.  Inclusion--exclusion over the corresponding complete periodic classes
gives

\[
 \delta_X=
 \sum_{Q\text{ compatible}}(-1)^{|Q|}\frac1{L_Q},          \tag{6}
\]

where the empty clique contributes 1.  The elementary estimate
`|sum_(m<=X)1/m-log X|<=1` handles that empty term.  Applying (4) to every
nonempty term and using the triangle inequality yields

\[
 \boxed{|H_A(X)-\delta_X\log X|\le {\cal B}(X).}            \tag{7}
\]

The finite densities decrease to `delta`.  Divide (7) by `log X`, use (2),
and then use `delta_X->delta`; this proves (3).

## 5. Relation to the other round-11 criteria

- The unweighted pointwise theorem pays `O(1)` per clique in ordinary
  counting and therefore asks for `kappa(X)=o(X)`.
- The logarithmically averaged theorem allows bad cutoff scales but keeps the
  same unweighted endpoint payment.
- The present theorem instead keeps a single cutoff and pays each clique by
  its actual CRT arithmetic.  Neither criterion contains the other in full,
  so they can be combined by taking the better error bound at each scale.

## 6. Evidence and publication boundary

The proof is exact finite inclusion--exclusion plus the progression lemma;
no probabilistic independence or finite computation is used.  The condition
is not known to hold for every residue system, and cancellation between the
alternating clique terms was discarded in (7).  Thus Erdős #25 remains open.
Together with the width, degeneracy, log-average, and hybrid-core criteria,
this is a coherent potential short-note package, subject to a full novelty
search and external review; it does not by itself meet the campaign's SCI-Q2
stopping threshold.

The companion `MOBIUS_COMPRESSED_CLIQUES.md` strengthens this estimate by
first combining all cliques that induce the same activated CRT progression.
Its boundary is never larger and is exponentially smaller on an explicit
squarefree-block family of nonredundant congruence systems.
