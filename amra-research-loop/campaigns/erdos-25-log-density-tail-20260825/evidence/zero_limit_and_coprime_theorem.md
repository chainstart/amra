# Two rigorous reductions for Erdős #25

Let \(A_K\) be the set left after the first \(K\) delayed residue classes are
removed.  It differs by a finite set from a periodic set, hence has a natural
and logarithmic density \(\delta_K\).  The sequence \(\delta_K\) decreases to
some \(\delta\ge0\).

## Zero-limit lemma

If \(\delta=0\), then the infinite complement \(A\) has logarithmic density
zero.

Indeed \(A\subseteq A_K\) for every \(K\), so its upper logarithmic density is
at most \(\delta_K\).  Letting \(K\to\infty\) gives upper density zero, while
the lower density is nonnegative.  Thus only the case \(\delta>0\) can contain
the original difficulty.

## Pairwise-coprime theorem

If the moduli \(n_i\) are pairwise coprime, then the logarithmic density in the
public question exists.

For finite \(K\), the Chinese remainder theorem gives

\[
 \delta_K=\prod_{i=1}^{K}\left(1-\frac1{n_i}\right),
\]

independently of the chosen residues; delayed onsets change only finitely many
points at a fixed stage.

If \(\sum_i1/n_i=\infty\), this product tends to zero, and the zero-limit lemma
applies.

If \(\sum_i1/n_i<\infty\), the standard tail union estimate is uniform in the
logarithmic average.  For a delayed residue class \(C_i\) and \(x\ge n_i\),

\[
 \sum_{m\le x,\,m\in C_i}\frac1m
 \le \frac{1+\log x}{n_i}.
\]

Consequently the normalised harmonic mass of
\(A_K\setminus A\) has limsup at most \(\sum_{i>K}1/n_i\).  This tends to zero,
while the logarithmic densities of \(A_K\) tend to the positive infinite
product.  Hence \(A\) has that logarithmic density.

The theorem is a restricted cohort, not a solution of #25.  In the general
positive-limit case the new residue classes are highly dependent, and neither
CRT independence nor reciprocal summability is available.
