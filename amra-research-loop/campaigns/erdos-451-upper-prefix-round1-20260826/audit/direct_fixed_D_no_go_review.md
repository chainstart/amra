# Adversarial review of the direct fixed-`D` no-go argument

## Verdict

**PASS.  Required corrections: none.**

This is an adversarial cross-reconstruction inside the same model family and
shared workspace, not an independent human proof or an independent-model
certification.  No new mechanism is introduced.

## Checked interfaces

- **Rank-three row identity:** expanding
  `G_p=p*1_[0,b)-b` reproduces every coefficient in (1); the two constant
  cells cancel because `|A|=b_1`.  Two incomplete `p_1`-rows cost less than
  `4k^4`.
- **Affine slice:** for `j=a+t p_2`, the first phase is fixed and the second
  advances by the invertible step `p_2 Delta_3 mod p_3`.  Formula (5) is the
  exact centered combination; no rank-two common-start factor is silently
  substituted.
- **Bounded cluster to fixed pattern:** Maynard's fixed-rank bounded-cluster
  theorem supplies infinitely many bounded-diameter `r`-tuples.  There are
  finitely many integer offset patterns in that diameter, so an infinite
  subsequence has fixed `0=d_1<...<d_r` and base `x` tending to infinity.
- **Barycentric sign and global frequency:** with
  `F(X)=product_i(X-d_i)` and
  `L=product_{i<j}(d_j-d_i)`, the integers
  `h_i=L/F'(d_i)` satisfy
  `sum_i h_i/(x+d_i)=(-1)^(r+1)L/Q`.  Multiplying by `Q` shows that the local
  CRT frequency induced by the signed global frequency
  `ell=(-1)^(r+1)L` is exactly `h_i mod p_i`.
- **Local Fourier normalization:** for nonzero `h_i`, the constant `-b_i`
  has zero Fourier sum and the `p_i` multiplier cancels the normalized
  `1/p_i`.  Hence the local coefficient is exactly the interval exponential
  sum in (10), of magnitude asymptotic to
  `p_i*|sin(pi h_i rho)|/(pi|h_i|)`.  Irrational `rho` makes every limiting
  constant nonzero.
- **Abel factor:** the unnormalized Fourier sum is `Q*ahat(ell)`, while Abel
  bounds it by at most
  `Q*|1-exp(-2 pi i ell/Q)|*max|S_T|`.  These two `Q` factors cancel, and the
  remaining inverse sine contributes a new `Q/(2 pi|ell|)`.  Thus
  `|ahat(ell)|=Omega_r(Q)` correctly yields a prefix of size
  `Omega_r(Q^2)=Omega_r(k^(2r))`; there is neither a missing nor an extra
  factor of `Q`.
- **Moving the start to `s=k`:** a prefix ending before `k` has magnitude at
  most `k*k^r=k^(r+1)`, so it cannot realize the
  `Omega_r(k^(2r))` lower bound for fixed `r>=2` and large `k`.  The selected
  endpoint therefore exceeds `k`; subtracting the first `k` terms loses at
  most `k^(r+1)` and preserves half the lower bound eventually.
- **Fixed-`D` quantifiers:** after absolute `C,D` are proposed, choose a
  fixed integer `r>D`, then let `k` tend to infinity along the fixed-pattern
  cluster subsequence.  The ratio
  `Omega_r(k^(2r))/(C^r k^(r+D))` diverges.  This disproves every uniform
  fixed-`D` all-support/all-interval estimate, while making no growing-rank
  cluster claim.  The later `r log k` ledger is correctly conditional on a
  rank-by-rank termwise recursion with `D_r>=r`; scale-dependent or
  cross-support cancellation remains outside the no-go theorem.

The review therefore finds the stated theorem and its limited campaign
consequence internally consistent.
