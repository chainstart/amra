# Author adversarial audit: signed multiplier dispersion

## Verdict

**PASS, with the stated method-level scope.**  This is an author-side
adversarial reconstruction, not an independent-agent audit.  It checks
`evidence/signed_multiplier_dispersion_no_go.md` against the exact endpoint
normalization already established in the campaign.  It does not supply an
independent proof of the open high-conductor estimate.

## Reconstruction checks

1. **Endpoint coefficient and phase: PASS.**  On the unit group, the local
   allowed residues are
   \(-Q_0^{-1},\ldots,-d_pQ_0^{-1}\).  Their unnormalized local character
   sum contributes
   \(\chi_p(-Q_0)\sum_{j\le d_p}\overline{\chi_p(j)}\).  Multiplication over
   the remaining primes gives exactly the coefficient in (2), including
   \(\chi(-Q_0)\).  The product multiset contributes the complex square
   \(S_X^P(\chi)^2\), not an absolute square.

2. **Shifted physical/spectral identity: PASS.**  Replacing the product
   variable by \(gut\) multiplies each character term by \(\chi(g)\).
   Summing against real \(a_g\) gives (7), and \(\sum a_g=1\) leaves the
   principal contribution exactly \(\delta N\).  The identity remains real
   because it equals the real physical sum \(\sum_g a_g C_X(g)\).

3. **Endpoint transfer and budgets: PASS.**  If the one signed high part is
   \(o(\delta N)\), the inherited low-conductor estimate multiplied by
   \(L=\sum|a_g|\) is still negligible when
   \(\log L=o(k/\log k)\).  Also
   \(M_X=(1-o(1))X\), so the inherited \(\delta X^2\) normalization matches
   \(\delta N\).  Positivity of the real signed sum implies some nonnegative
   physical count is positive even when individual weights have both signs.
   The resulting candidate has
   \(n=Q_0gut\le Q_0GX^2\); the assumptions on \(G\) give exactly the stated
   subexponential or \(\exp(O(k/\log k))\) value budget.

4. **Truncated divisor transform and inverse cost: PASS.**  Regrouping
   \(n=gh\) proves (17).  Dirichlet convolution with the inverse of \(a\)
   proves (20) coefficient by coefficient.  Recovering one original interval
   factor therefore pays \(B_X=\sum_{d\le X}|b_d|\); recovering the square
   would pay the corresponding two-factor boundary ledger.  The existing
   equal-length low-conductor theorem does not by itself prove the mixed
   endpoint in (18).

5. **Sparse quadratic annihilator: PASS with limited scope.**  The values
   \(\chi(g_i)=1\) and \(\chi(-Q_0)=1\) impose at most \(s+1\) linear
   conditions on the quadratic-character cube.  A kernel of dimension
   \(d\ge m-s-1\) has at least \(d\) active coordinates, hence contains a
   vector of weight at least \(d/2\).  For \(s=o(m)\) its conductor exceeds
   the cutoff by an exponential margin.  This refutes uniform
   generator-only damping.  It does **not** lower-bound the actual endpoint
   sum because that character's interval coefficient can be zero or small.

6. **Full-support energy no-go: PASS with limited scope.**  Local
   nonprincipal-character orthogonality gives the kernel \(p-2\) on equal
   residues and \(-1\) otherwise.  For distinct representatives below
   \(G<P\), its off-diagonal magnitude is at most
   \(\prod_{p\mid g-h}p\le |g-h|\le G\).  Cauchy--Schwarz gives diagonal
   mass at least \(S^{-1}\prod_p(p-2)\), while the total off-diagonal mass is
   at most \(L^2G\).  Under the stated subexponential budgets the diagonal
   dominates.  This proves a whole-family multiplier-energy obstruction,
   but it is deliberately **not** promoted to a lower bound for
   \(\sum c_\chi A_a(\chi)S_X^P(\chi)^2\) or even for its coefficient-weighted
   square mass.

7. **Absorber phase and inversion: PASS.**  The factor
   \(\chi(-Q_0)A_a(\chi)\) is the Fourier transform of the translated
   multiplier.  Translation preserves all relevant norms and spectral
   zeros.  If a convolution inverse exists, its transform is reciprocal,
   giving \(\|b\|_1\ge |A_a(\chi)|^{-1}\).  This only kills the combination
   “uniform damping plus stable recovery”; a direct signed shifted-endpoint
   proof would not need to invert.

## Scope guard

The evidence proves exact identities and refutes an affordable universal
pointwise-damping/separated-energy/stable-inverse handoff.  It does not
refute a coefficient-aware signed estimate for the shifted physical count,
does not prove a high-conductor aggregate lower bound, and does not improve
the public Erdos-451 upper bound.  The sole multiplier escape remains the
explicit conditional sum (14); absent a theorem exploiting its interval
coefficients jointly, this mechanism should be frozen rather than counted
as a new survivor.
