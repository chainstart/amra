# Independent audit of the general-\(k\) low coefficients

Date: 2026-07-30

## Verdict

The cycle classification, binomial deconvolution, sparse seven-edge
interpolation, Newton-support argument, and first-coefficient extraction in
`GENERAL_K_LOW_COEFFICIENTS.md` pass an
independent audit.  In the polynomial stable range the calculation proves

\[
\begin{aligned}
[\beta^0]K_k&=1,\\
[\beta^1]K_k&=2(k-2)(k+3),\\
[\beta^2]K_k
&=(k-2)\bigl((k+3)s+2k^3+7k^2-9k-60\bigr).
\end{aligned}
\]

The subsequent seven-edge computation proves

\[
[\beta^3]K_k
=\frac{2(k-2)}3\left[
(3k^3+11k^2-11k-105)s
+(k-3)(2k^4+13k^3+18k^2-96k-300)
\right].
\]

It also proves, as an identity in \(\mathbb Q[s][\beta]\),

\[
[\beta^d]F_k=0\quad(d<2k-4)
\]

and proves that the coefficient at \(2k-4\) is not the zero polynomial.  This
audit does **not** promote that coefficient to a pointwise-positive polynomial
for every \(k,s\), and it does not prove all of \(F_k\) or \(K_k\)
coefficientwise nonnegative.

## Audit of the six-edge classification

For profile \(h\), write the core-block weights as \(w_i\in\{1,2\}\).  A
four-edge cyclic subset of the weighted complete bipartite graph is exactly a
\(K_{2,2}\), so its total weight is

\[
\binom{k}{2}\sum_{i<j}w_i^2w_j^2.
\]

A five-edge cyclic subset contains a unique four-cycle.  Once that cycle uses
core weights \(w_i,w_j\), the total weight of an outside edge is
\(ks-2(w_i+w_j)\).  This gives the stated \(R_h\).

At six edges, begin by marking a four-cycle and choosing two outside edges.
There are only three corrections:

- a \(K_{2,3}\) contains three marked four-cycles and is therefore overcounted
  by two;
- a \(K_{3,2}\) has the same overcount;
- a chordless \(C_6\) contains no four-cycle and must be added once.

For three selected core blocks and three selected pages there are exactly six
undirected alternating six-cycles.  The outside-edge elementary symmetric sum
for a fixed core pair is

\[
e_{2,h}-2ks(w_i+w_j)
  +3w_i^2+4w_iw_j+3w_j^2.
\]

These observations independently reproduce equation (8), including both the
\(-2\binom{k}{2}w_h\) theta correction and
\(+6\binom{k}{3}w_h\) chordless-cycle correction.

## Audit of the determinant and deconvolution

Let \(E_h\) be the unrestricted edge-slot polynomial and let
\(C_h,R_h,S_h\) be the rejected cyclic weights in degrees \(4,5,6\).
Because \(E_1^2=E_0E_2\), expanding

\[
(E_1-\mathrm{bad}_1)^2
 -(E_0-\mathrm{bad}_0)(E_2-\mathrm{bad}_2)
\]

through degree six gives exactly

\[
\begin{aligned}
d_4&=\delta C,\\
d_5&=\delta R+ks\,\delta C,\\
d_6&=\delta S+ks\,\delta R
 C_0e_{2,2}+C_2e_{2,0}-2C_1e_{2,1}.
\end{aligned}
\]

No product of two bad terms can occur before degree eight.  Dividing
triangularly by \((1+k\beta)^{2s-2k-2}\), rather than identifying the
\(d_i\) directly with coefficients of \(K_k\), yields the three displayed
formulas above.

The standalone verifier
`audit_general_k_low_coefficients_independent.py` performs this derivation
without importing any saved \(K_3,\ldots,K_7\) formula.  It then directly
enumerates all bipartite edge subsets through degree seven.  The reconstructed
rows are

\[
\begin{array}{c|c|c}
k&s&([\beta^0]K_k,[\beta^1]K_k,[\beta^2]K_k,[\beta^3]K_k)\\ \hline
2&5&(1,0,0,0)\\
3&6&(1,12,66,168)\\
4&7&(1,28,386,3308).
\end{array}
\]

For the general seven-edge identity, a pair of forest edge sets with seven
total edges uses at most seven page labels and at most seven anonymous core
labels.  Its count therefore has binomial-basis degree at most seven in each
population variable.  The three triangular deconvolution terms can raise the
\(k\)-degree only to eight and do not raise the \(s\)-degree past seven.
Consequently the exact \(9\times8\) grid used in the primary verifier uniquely
determines the bivariate polynomial.  This is a finite-difference proof with
an a priori degree bound, not an unbounded pattern extrapolation.  The direct
rows above give a separate edge-subset check at three points outside that
sparse implementation.

## Audit of the first support of \(F_k\)

Here the relevant nilpotent steps are the active-page transfers in the
original core-partition view.  If the two histories use \(j,q\) active pages
and overlap in \(\ell\) page labels, their pooled Newton order is
\(r=j+q-\ell\).  Every nilpotent step selects at least two current components,
so it contributes at least two spokes.  Object by object,

\[
d\ge 2(j+q)=2(r+\ell)\ge2r.
\]

Thus the vanishing before degree \(2r\) is a support statement, not a signed
cancellation.  At equality, \(\ell=0\) and every active page selects exactly
two components.  Reading such a history as an ordered list of edges produces
a forest on the initial core blocks; conversely every ordering of the edges
of such a forest is legal.  Therefore

\[
\sum N^j_{\min}=j![x^j]\Phi_h(x).
\]

The \(\ell=0\) coefficient in
\(\binom tj\binom tq\) is \(k!/(j!q!)\) when \(j+q=k\).
Convolving and cancelling the factorials gives

\[
[\beta^{2k}]B_k
=k![x^k](\Phi_1^2-\Phi_0\Phi_2),
\]

which confirms equations (16)--(17).

For the top \(s\)-degree, the two page labels responsible for the local
second-profile defect can be chosen in \(2k(k-1)\) oriented ways.  Every
remaining page must use two fresh anonymous unit blocks to retain the maximum
\(2k-4\) anonymous labels.  Assigning each page to one of the two histories
contributes \(2^{k-2}\), while turning the fresh labels into unordered pairs
contributes \(2^{-(k-2)}\).  Hence

\[
[\beta^{2k}]B_k
=2k(k-1)(s-4)_{2k-4}+O(s^{2k-5}),
\]

so the normalized first coefficient of \(F_k\) is monic of degree \(2k-4\)
and cannot vanish identically.

## Complete-graph interpretation and remaining theorem

There is a useful exact reformulation.  Let \(Z_{K_s}(x)\) be the ordinary
forest polynomial of \(K_s\), and let \(e,f\) be disjoint edges.  Contracting
the forced edges gives

\[
Z_e=x\Phi_1,\qquad Z_{ef}=x^2\Phi_2,\qquad Z=\Phi_0.
\]

By symmetry \(Z_e=Z_f\), and therefore

\[
\boxed{
Z_eZ_f-ZZ_{ef}
=x^2(\Phi_1^2-\Phi_0\Phi_2).
}
\]

Consequently, pointwise positivity of the first coefficient of every \(F_k\)
is precisely the corresponding coefficientwise Rayleigh assertion for two
disjoint edges of the uniformly weighted complete graph.  This is a sharper
target than merely computing \(B_8\), but it is still a theorem to be proved;
the general independent-set-Rayleigh conjecture cannot be assumed here.

The independent component recurrence (weighted Cayley on the component
containing a distinguished vertex) checked this extraction for
\(2\le k\le10\) at \(s=k,k+1\).  All values were nonnegative, with the sole
zero \(k=s=4\); this is finite evidence only.

## Reproduction

Run

```bash
cd data/research_open/q1_eight_hour_campaign_2026-07-29/opg1757
python3 audit_general_k_low_coefficients_independent.py
```

The expected terminal line is `STATUS|PASS`.
