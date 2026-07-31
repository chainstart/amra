# Independent audit: OPG-1757 pooled top face

Date: 2026-07-31

## Verdict

No fatal mathematical gap was found.  The theorem is valid in its stated
scope:

- the highest \(\beta\)-coefficient at every pooled depth;
- the exact global pooled-depth cutoff;
- complete coefficientwise positivity of \(B_{2s-5}\) and \(B_{2s-6}\).

The audit does not endorse positivity of every \(B_n\), the full
complete-split Rayleigh statement, or arbitrary-host OPG-1757.

## Independent checks

1. The normalization
   \[
   P_s^{(2)}(\beta,k)
   =(1+s\beta)^{2s-2k-4}D_k
   \]
   was checked, including the exact-divisibility regime with negative
   exponent.  An independent brute-force forest enumeration covered
   \(s=4,\ k=2,\ldots,5\).
2. The direct high-degree endpoint of \(D_k\), its transfer to \(P_s^{(2)}\),
   and the Stirling inversion were recomputed.
3. The support implication
   \[
   \min\deg_\beta B_n\ge2n,\qquad
   \max\deg_\beta B_n\le4s-10
   \]
   was checked and correctly yields \(B_n=0\) for \(n>2s-5\).
4. At \(n=2s-6\), degrees \(2n\) and \(2n+1\) force zero active-page
   overlap.  The audit confirmed the factor
   \(n!/(j!q!)\), its cancellation against ordered-chain factorials, the
   remaining \(\lambda^2\), and the one-ternary-edge contraction weight.
5. All seven unit tests and the full verifier pass.
6. Beyond the main verifier range, the binary/ternary endpoint formulas
   were checked at \(s=13,14,15,16\) and agreed exactly.

## Editorial recommendation

The theorem note now includes the short proof \(B_0=B_1=0\), addressing one
audit comment.  Before journal submission, expand the algebra taking the
normalized component table to the two closed forms for \(C\) and \(Q\), or
export a standalone symbolic certificate for that simplification.  This is
an auditability improvement, not a detected correctness failure.
