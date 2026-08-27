# Author adversarial audit: M10 high-support round 3

Date: 2026-08-27

Scope: self-audit of
`work/m10_round1/high_support_joint_correlation_round3.md`.  This is not an
independent-agent cross-audit.

Verdict: **PASS after mandatory linkage corrections; open closure remains.**

## Checks reconstructed

1. **Exact carry.**  Expanding `product_i U_i(c_ix)` imposes only
   `A(z)=x (mod P)`, hence it equals `sum_ell W(x+ell P)`.  It is not
   `W(x)`.  The exact fibre additionally imposes the displayed integer
   equation on `sum_i t_i`.
2. **One-sided bridge.**  `S=sum_r Omega(r)V(r)` contains every diagonal
   pair `Phi(A)W(A)` and extra nonnegative cross-carry pairs.  Removing the
   zero-vector cross contribution `Omega(0)=1` leaves `E-1<=S-1`; thus
   `S<2` is sufficient, but equality was not claimed.
3. **Fourier normalization.**  With normalized finite DFT,
   `Omega_hat(j)=h^(-1)(1-|j|_P/h)_+`; Parseval supplies the factor `P`, so
   the prefactor in the small-lift sum is exactly `P/h`.
4. **Phase scope.**  The cofactor identity makes the local residues of
   `H(a)` equal to `a_i`, but `H(a)/P=sum_i a_ic_i/p_i (mod 1)`.  The note
   therefore retains, rather than discards, the joint inverse-derivative
   phase.
5. **Dual scales.**  The coefficient-side support is `|H|<h`; the
   real-space Fejer kernel is concentrated on scale `P/h`.  The dyadic
   tail calculation is included before using the old `T=P/h`
   subset-period estimate against the sufficient majorant.
6. **Growing smoothing order.**  For general even `L`, the zero-frequency
   mass is written as `Q_L(0)>=cP/h`, not incorrectly as `P/h`; only the
   `L=2` identity is exact triangular Fejer.
7. **Exact moments.**  Equal numerators force every coordinate difference
   to be a multiple of its own prime and then impose `s-1` global zero-sum
   carry equations.  The diagonal lower family uses nonzero representatives
   below `p_i/(4b)`, so it genuinely lies in full reduced support.
8. **Claim boundary.**  Large available upper ledgers are described only
   as method no-goes.  No finite computation, maximum-gap theorem, public
   #451 bound, or equivalence between the majorant and exact fibre is
   claimed.

Mandatory correction history: the initial draft incorrectly treated
independent local carries as the exact fibre and incorrectly suggested that
the cofactor cancellation erased the global inverse-derivative phase.
Both statements were removed before this audit.
