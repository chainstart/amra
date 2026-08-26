# Author audit: discrete spectral norm ledger

Date: 2026-08-27

Audited artifact:
`evidence/m10_discrete_spectral_norm_ledger_round3.md`.

Verdict: **PASS, with open statements kept conditional.**  This is an
author-side adversarial reconstruction, not an independent-agent audit.

## Checked identities

1. Unnormalized finite Parseval gives `p/r` and `p/s` for the two local
   uniform interval transforms.  Cauchy--Schwarz proves the local `L1`
   bound; physical-space Young plus Parseval proves the local `L2` bound.
   The exact trapezoid square sum has plateau length `s-r+1`, as stated.

2. The centered Dirichlet estimate gives the `4^(-j)` Fejer decay on
   doubling shells.  Global Cauchy--Schwarz therefore leaves precisely the
   square-root conductor term in (8)--(10).  The higher-Holder formula
   (10a)--(10b) follows from `Gamma<=1` and has no hidden improvement over
   `q=2` in the 451 parameter range.

3. The arc lemma removes the principal atom and is only required for
   `gamma=1` and for the specific `gamma=p_0` after width-one elimination.
   The all-unit formulation is genuinely false: the all-one local word is
   a unit frequency of weight at least `(4/pi^2)^m`, and its inverse unit
   sends that atom to residue one.

4. AM--GM gives `|T_i|<=G_i` with equality at zero.  The transform of each
   squared interval kernel is the centered cyclic triangle in (16); it is
   nonnegative and supported on `|ell|_(p_i)<s_i`.  CRT factors the global
   transform, and the integer Fejer expansion is valid for integral
   `1<=h<P`.  Subtracting the common zero word gives (19), hence the strict
   sufficient condition (20).  After width-one elimination, the argument
   correctly replaces `phi_i(ell)` by `phi_i(p_0 ell)`.

5. The full-period mean in (21) is exact because the product majorant has
   value one at the global zero frequency.  The larger-sieve denominator
   uses `2s_i-1>=d_i`, so its displayed upper bound and negative target
   asymptotic have the correct direction.

6. The principal dual term gives the exact necessary threshold
   `L_G/h<2`.  The formulas for `kappa(d)` are correct in both parity cases,
   and distinct offsets give the stated polynomial correction to `2^m`.
   Hence every fixed base below two is rigorously excluded for this
   positive majorant.

7. The additive discrepancy (21e) is sufficient by (21f), and (21g) is
   exactly the nonzero `G`-spectral mass.  It follows from an arc theorem
   for `G`, not from the earlier arc theorem for the smaller weight
   `Gamma`.  Subset period conditioning pays the omitted factor
   `L_(J^c)`; the stated obstruction has the correct direction.

8. Removing `|ell|<=floor(K^m)` costs at most `2K^m+1`; hence the stated
   moving-tail reduction is exact.  The parity check in (21f1) passes.
   However `E_gamma<m/2` and `L_G>3^m`, so pointwise energy damping plus
   trivial tail cardinality cannot reach the main scale.  The note keeps
   weighted joint-energy distribution open rather than promoting this
   reparameterization.

9. For `gamma=1` and `|ell|<k/2`, there is no local wraparound and
   `d_i+1<=k`; the geometric-series proof of (21k)--(21l) is valid and
   costs only `O(k/m)=O(log k)`.  The quotient inequalities also make the
   annulus `k/2<=|ell|<k` identically zero.  This proof does not extend to
   `gamma=p_0`.  In that dilation the isolated `ell=+-1` annihilation is
   correct for any remaining `d_i>=3`, but no interval theorem is inferred.

10. Integer support is exactly `2|N-qp|<=p-k`; solving its two inequalities
    gives (21n), and subtracting adjacent endpoints gives the gap
    `2k/(2q+1)`.  If an active quotient interval meets `p<2k`, then
    `q>=(2N-k)/(4k)`; hence `N>2k^2` forces `q>=k` and makes every such gap
    strictly shorter than one.  The large-`q` scale and the loss incurred
    by separate fixed-`q` prime counts are correctly classified as a
    reparameterization obstruction, not as a proved tail estimate.

## Scope guards

- A large right side produced by a separated norm inequality is a no-go
  for that ledger, not a lower bound on the actual coupled spectral error.
- The fixed-exponential arc estimate (12) is conditional.
- The positive compact-dual estimate (20) is also conditional and needs a
  factor-two density bound; a `K^m` relative loss is not sufficient.
- Guarded finite data rigorously falsify the displayed `C_0=2,B=0` finite
  specialization.  They neither refute polynomial enlargement nor prove
  the `C_0=5/2,B=0` asymptotic; the latter is finite evidence only.
- M05's one-block anchored successor theorem does not imply either open
  estimate.  No maximum-gap theorem and no new Erdos 451 upper bound is
  claimed.
