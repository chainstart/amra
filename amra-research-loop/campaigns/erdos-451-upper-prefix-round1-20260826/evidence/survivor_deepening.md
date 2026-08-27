# Survivor deepening: prefix code and the exact gap lemma

## 1. Correct target: a successor after `2k`, not the least positive point

Let

\[
P_k=\prod_{k<p<2k}p,
\qquad
\mathcal A_k=\{a\bmod P_k:a\bmod p\in
\{0,k+1,\ldots,p-1\}\text{ for every }p\}.
\]

If `p_0` is the least prime in `(k,2k)`, then `p_0` itself lies in
`A_k`: its `p_0` coordinate is zero, and for every larger interval prime `q`
one has `p_0 mod q=p_0>k`.  Thus a theorem about the *least positive* point of
`A_k` merely rediscovers a point at most `2k` and says nothing about `n_k`.

The required object is exactly

\[
n_k=\min(\mathcal A_k\cap(2k,\infty)).                 \tag{1}
\]

This correction is now explicit in representations R01, R03, R09 and
mechanisms M01, M05, M10.

## 2. An unconditional fixed-prefix code lemma

For `H>2k`, map every integer `n in (2k,H]` to its CRT residue codeword

\[
\Phi(n)=(n\bmod p)_{k<p<2k}.
\]

> **Prefix agreement lemma.**  Let `k>=2`, and let `n!=n'` lie in
> `(2k,H]`.  The number of interval primes at which `Phi(n)` and `Phi(n')`
> agree is at most
> \[
> R(H,k)=\left\lfloor\frac{\log(H-2k)}{\log k}\right\rfloor
> \]
> when `H-2k>=1`; the universally safe bound
> `floor(log(H-1)/log k)` holds without using the lower endpoint.

**Proof.**  If the two residues agree at every prime in a set `S`, then the
squarefree product `prod_{p in S}p` divides the nonzero integer `|n-n'|`.
Every such prime is larger than `k`, while `|n-n'|<=H-2k-1` (and certainly
`<=H-1`).  Hence

\[
k^{|S|}<\prod_{p\in S}p\le |n-n'|<H-2k,
\]

which gives the claim after taking logarithms.  `square`

Consequently the fixed prefix is a high-distance CRT code: at
`H=exp(epsilon k)`, distinct codewords agree in at most
`(epsilon+o(1))k/log k` of the `m_k=(1+o(1))k/log k` coordinates.  This is
genuine position-sensitive information; it is not a translation average.

It does **not** yet prove (1).  The forbidden/allowed test records interval
membership, not exact equality.  Two codewords may occupy the same local
interval with different residues at every coordinate, so the agreement lemma
alone supplies no allowed word.

## 3. The conditional decisive lemma

For pairwise coprime moduli `q_1,...,q_m`, cyclic intervals `I_i` of lengths
`d_i`, and `Q=prod q_i`, let

\[
A=\{a\bmod Q:a\bmod q_i\in I_i\ \forall i\},
\qquad |A|=\prod_i d_i,
\]

and let `G(A)` be the largest cyclic gap between consecutive elements of
`A` in `Z/QZ`.

> **CRT interval-box gap lemma (open).**  There are absolute constants
> `B,C>0` such that
> \[
> G(A)\le q_{\max}^{B} C^m\frac{Q}{|A|}.               \tag{2}
> \]

This is a genuine general statement about all CRT products of cyclic
intervals, not a renaming of (1).  Local translations do not affect it:
arbitrary translations of the `I_i` combine by CRT into one global translate
of `A`, and `G(A)` is translation invariant.  The polynomial
`q_max^B` cannot simply be deleted: already for one modulus, an interval of
length near `q/2` can have gap of order `q`, while `Q/|A|` is order one.

For the 451 box, (2) immediately gives

\[
n_k\le 2k+G(\mathcal A_k)
\le 2k+(2k)^B C^{m_k}
     \prod_{k<p<2k}\frac p{p-k}.                       \tag{3}
\]

The prime number theorem, with a standard endpoint truncation (or a
Brun--Titchmarsh bound for the narrow endpoint), gives

\[
m_k=(1+o(1))\frac{k}{\log k},
\qquad
\sum_{k<p<2k}\log\frac p{p-k}
=(\log4+o(1))\frac{k}{\log k}.                         \tag{4}
\]

Indeed the limiting integral in the second formula is

\[
\int_1^2\log\frac{t}{t-1}\,dt=2\log2=\log4.
\]

Combining (3)--(4) would prove the stronger conclusion

\[
n_k\le
\exp\!\left((\log4+\log C+o(1))\frac{k}{\log k}\right)
=\exp(O(k/\log k))=\exp(o(k)).                          \tag{5}
\]

Thus (2) is an exact, sufficient closure lemma.

## 4. What has and has not survived

Small exhaustive gap tests did not falsify the scale in (2): for moduli
`(3,5)`, `(3,5,7)`, `(5,7,11)`, `(3,5,7,11)`, exhaustive width searches gave
maximum observed ratios

\[
G(A)/(Q/|A|)=2.000,\ 3.086,\ 4.239,\ 4.909,
\]

respectively.  These are finite tests only.

The available standard mechanisms do not prove (2):

- full-period density gives `|A|` but no gap bound;
- translated-window moments have the wrong pointwise quantifier;
- symmetric Minkowski produces mixed coordinate signs;
- a difference-set or additive-energy bound is translation invariant but
  does not orient the difference into the one-sided box;
- Fourier support size does not control near-zero full-support characters.

A cardinality-only chain decomposition is also quantitatively too weak.  The
offset box `prod_i {0,...,d_i-1}` is graded by `sum_i s_i`.  There are at most

\[
1+\sum_i(d_i-1)
\]

ranks, and every rank is an antichain.  Hence some antichain has size at least

\[
\frac{\prod_i d_i}{1+\sum_i(d_i-1)}.                    \tag{6}
\]

For the 451 widths, the numerator is `exp((1-o(1))k)` and the denominator is
polynomial in `k`.  Thus the abstract product order admits antichains much
larger than `exp(epsilon k)` for any fixed `epsilon<1`.  Dilworth or monotone
collision based only on the number of prefix points cannot force a
coordinatewise-oriented pair at the target scale.  This does not rule out
using the special arithmetic order of the actual CRT representatives.

M05, M08 and M10 therefore converge on a precise missing interface—an
orthant/common-interval gap inequality—but currently provide no proof of it.
The prefix agreement lemma is proved, while the decisive gap lemma (2) remains
conditional.  No original exponent or upper bound has changed.
