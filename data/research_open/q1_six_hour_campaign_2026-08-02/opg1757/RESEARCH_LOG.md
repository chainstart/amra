# OPG-1757 chronological research log

All times are HKT (UTC+8), 2026-08-02.

## 10:30--10:40: mandatory source freeze

- Read in full the previous lane's `README.md`, `CLAIM_LEDGER.md`,
  `UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md`,
  `POLYNOMIAL_GROWING_DEFICIT_WINDOW.md`,
  `POLYNOMIAL_WINDOW_RED_TEAM.md`, `BASE4_NEWTON_GLOBAL_ATTACK.md`,
  `SECOND_ACTIVE_NEWTON_RECURRENCE_ATTACK.md`, both unit-test modules,
  all four verifier programs, the quantifier self-audit, and the blind
  audit map.
- Read the inherited all-order `LAURENT_DEGREE_LEMMA.md` in full and
  checked that its normalization is the same `Q_{h,e,c}` used by the
  polynomial candidate.
- Replayed 9 unit tests, the extended polynomial certificate, the
  base-four census, and the second-active probe.  All passed; exact
  counts are frozen in `BASELINE_FREEZE.md`.
- Began an independent six-gate reconstruction.  The first point still
  requiring a written independent derivation is the absolute profile EGF
  and its comparison to the leading symbol; no failure has yet been
  found.

## 10:40--10:50: polynomial gate closed and exponent sharpened

- Independently derived the five-coordinate absolute profile EGF
  `exp(y(1+2z+2z^2))`, including the determinant factor two and outer
  factor four.  This gives exactly `8/(q+1)!`, including both beta
  boundaries.
- Reconstructed the same normalized all-order endpoint filtration and
  the apparent-to-actual loss shift `K=k+2`.  The former `1/67` theorem
  is now `PROVED`; all six blind-audit gates are closed in
  `POLYNOMIAL_WINDOW_INDEPENDENT_AUDIT.md`.
- Tightened triangular interpolation from
  `[128(k+1)]^(16k) q^(2k)` to
  `[64(k+1)]^(6k) q^(2k)`.  After four-factor convolution, exact profile
  comparison, and a correlated `k<=2q` estimate, obtained
  `|c_k|/L <= ((2^23 q)^8)^k`.
- Proved the uniform threshold `s>=2(2^23 q)^8` and simultaneous window
  `q<=s^(1/8)/2^24`; the stable range `s>=6q+4` is automatic, so the
  use at `q=q(s)` has no hidden fixed-parameter constant.
- New independent certificate: 5 tests pass; 120 exact profile
  identities, 6,640 endpoint/convolution checks, 144,580 falling
  coefficients, and 22,650 geometric-loss checks pass.  These checks
  support transcription only; the universal proof is written out.
- Next attack: independently audit the pending odd second-active Newton
  recurrence and then push its even counterpart/full Newton convolution.

## 10:50--11:03: odd second-active row promoted

- Independently derived the normalized row identity
  `sum C_(q,r)(s) z^r = s^(2s-2) B_p(s,z/s)/(p! z^(2p))`.
  This fixes the B4/B2 comparison and all changing powers.
- Reconstructed the B4 transport after homogenization.  The lower range
  is dominated by a fixed degree-seven positive kernel with 57 positive
  numerator monomials; the four top degrees were independently extracted
  from reverse coefficients of the three exponential terms in `L_s`.
- Found and handled the only small-boundary subtlety: at `s=5` the
  formal common `(1+z)` exponent is negative, so `H_5` must be computed
  directly from the exact `q=1` natural-support layer.  It equals
  `52+64z+28z^2`; no invalid negative-power cancellation is used.
- The independent symbolic certificate passes 3 tests, confirms all four
  top identities, 57 kernel monomials, 20 shifted top-polynomial
  monomials, ten exceptional boundary values, and 94 base/finite
  recurrence coefficients.
- Promoted odd second-active positivity to `PROVED`.  The first unproved
  Newton step is now the even B5/B3 transport kernel.

## 11:03--11:08: complete q=7 Newton layer

- Extended the frozen endpoint table from rank eight to rank nine.  The
  27 new endpoints use exact Abel-degree interpolation plus one unused
  check point each; the complete table has 135 formulas.
- Constructed all fifteen normalized `q=7` layers and checked their
  degree and leading symbol before taking forward differences at four.
- Exact census: 180 active coefficients positive, 45 boundary-forced
  coefficients zero, no negative coefficient.  The smallest active
  value is 512 at `(r,j)=(14,3)`.
- Status is deliberately `FINITE / PROVED AT q=7`; this does not close
  the all-deficit Newton conjecture.

## 11:08--11:46: even second-active comparison kernel

- Rewrote the stable even B5/B3 row as an exact two-term coefficient
  comparison.  For every bulk degree `d<=2s-12`, positivity reduces to
  the coefficient of one comparison kernel `K_s`; the discarded term is
  the product of a proved nonnegative B3 coefficient and
  `s^N-(s-1)^N`.
- Proved `K_(s,d)>0` for the 31 uniform columns `d=0,...,30`.  At the
  natural start of each column, the exact coefficient is a polynomial in
  the remaining shift with all 682 monomial coefficients positive.
  This is an all-`s` statement for those columns, not a finite scan.
- Reverse-extracted the six highest coefficients of the row into four
  exponential-polynomial pieces with bases 25, 16, 9, and 4.  A
  25-versus-16 ratio-monotonicity certificate (72 shifted monomials) plus
  four exact boundary values proves all six columns for every `s>=7`.
- The two bands meet through `s=21`; together with the direct `s=6`
  boundary this proves every even second-active row for even deficits
  `2<=q<=32`.  The universal even theorem is still open.
- Derived an exact obstruction to the most natural fixed-depth `u_2`
  layer proof.  After merging any fixed `R>=6` layers, the coefficient
  at beta degree `R+3` has negative leading term
  `-3*2^R*(R+5)*s^(R+2)/(R-1)!`.  This refutes the proof route, not the
  positive recurrence itself.
- New verifier and three unit tests pass.  The separate finite workbench
  through `s=35` checks 1,073 comparison-kernel, 1,064 kernel-recurrence,
  1,064 first-transport, and 1,053 second-transport coefficients, with no
  failure; these scans remain explicitly `FINITE`.

## 11:46--11:56: universal even row closed

- Split the comparison numerator as `M_s=Y_s+P_s`, where `P_s` is an
  immediate positive multiple of the proved B3 bracket and
  `Y_s=A_s-3B_s-boundary`.  This removes the low-degree negative part
  which obstructed the direct comparison-kernel recurrence.
- Derived an exact four-exponential recurrence for `Y_s`.  Expanding
  around `u_2` and merging the first four layers gives a fixed initial
  kernel with 112 positive shifted monomials.  The fourth layer has 59
  positive monomials, while `81*E5+8*E4` has 52 and controls every later
  layer by monotonicity; `E5` itself has 36 positive monomials.
- Proved the two boundary coefficients at beta degrees 14 and 15 by 31
  positive shifted monomials.  Three positive `Y_8` values then start a
  coefficientwise induction for every degree at least 16.  `Y_7` has one
  positive top value.
- Combined this high tail with the already proved eight low comparison
  columns and six reverse row coefficients.  The comparison kernel is
  now positive on its complete support, so every even second-active row
  is strictly positive.
- Combined with the independently audited odd theorem: for every
  `q>=1`, every coefficient in Newton order `floor(q/2)+1` is strictly
  positive.  This is a universal theorem; later active orders and the
  original arbitrary-host statement remain open.
- `verify_even_second_active_universal.py` passes, and the combined five
  even-row unit tests pass.

## 11:56--12:00: independent even-row audit

- A separate agent reconstructed the moving-support induction, including
  the two new top degrees introduced when `s` increases, instead of merely
  replaying the author's coefficient census.
- Its focused audit suite passes all eight gates.  The even theorem and
  hence the parity-free second-active theorem are now marked
  `PROVED / AUDIT PASSED`; the full Newton conjecture is unchanged.

## 12:00--12:30: third-active exact reduction

- Collapsed the third forward difference to its only three surviving
  boundary values.  Odd deficits are therefore exactly a `B6/B4/B2`
  comparison and even deficits a `B7/B5/B3` comparison.
- Removed the maximal common `(1+z)` factor and derived stable closed
  formulas for both parity branches.  The reduced degree is at most `2s-6` in
  each branch; the stable ranges begin at `s=8` (odd) and `s=9` (even).
- Proved maximality symbolically: explicit factorizations of
  `K6(s,-1/s)` and `K7(s,-1/s)` make both reduced values at `z=-1`
  strictly positive on their complete stable ranges.
- Isolated the first open sign gate as the two natural transports
  `H_o(s+1)-(s+6z)^2 H_o(s)` and
  `H_e(s+1)-(s+7z)^2 H_e(s)`.  If these are coefficientwise positive,
  finite bases complete the universal third-active theorem.
- The exact workbench verifies both reductions through `m=100` and
  finds no counterexample among 40,803 original row coefficients or
  21,547 transport coefficients.  This is explicitly retained as
  finite falsification evidence; transport positivity remains open.
- Six focused third-row tests and the five existing even-row tests
  pass.  The original OPG firewall is unchanged.

## 12:35--13:15: cross-lane red-team audit of Erdős #776

- Rebuilt the negative initial no-borrow variables and both Pascal
  cancellations independently.  No formula counterexample was found.
- Supplied the omitted cap-legality guard for equations (2.7)--(2.9):
  the two initial gaps are `(h-1)(2b+h)/2` and
  `(h-1)(2b+h+2)/2`, and the standard upper-shift cap inequality then
  propagates legality through `X1,Y1`.
- Audited the sequential proof of Lemma 2.1.  Its scales are uniform:
  under a hypothetical `X1<=0`, they are
  `x0=O(b^(3/2))`, `n=Theta(b^(4/3))`,
  `Delta=Theta(b^(5/3))`, and `U3(y0)=Theta(b^(20/9))`,
  contradicting a rank-four negative surplus.
- A separate combinadic engine reconstructed 246,955 full local orbits
  through `b=150`; a dimensionless exact scan covered 10,209,264
  relaxed points through `b=500`.  It found no illegal next low block
  and no nonpositive rank-five value on the 1,320 open-gate antecedents.
  The minimum was `gamma5=4222` at `(b,h,n)=(47,238,561)`.
- Initial verdict `REPAIR` was upgraded to `PASS AFTER REPAIR` after the
  author note incorporated the legality guard and corrected the stale
  equation number.  The pass covers only the reduction, legality, and
  Lemma 2.1; implication (2.13) and the observed one-promotion reduction
  remain open.
- Proved a red-team route obstruction: for every fixed `K>=4`, a
  parity-adjusted root choice `r=sqrt(2Kq)+O(1)` gives infinitely many
  relaxed one-promotion points with `gamma3<0`, `x0>0`, and
  `gamma4<0`.  Hence the open gate cannot be closed by reducing to a
  finite list of `K` values.
- Independent hostile reconstruction passed the entire exact third-active
  reduction.  A separate old-enumerator verifier reproduces the six bases,
  440 row coefficients, and 637 strict transport coefficients through its
  independent finite range; the two unbounded transport signs remain open.

## 13:20--13:32: third-active transport boundary bands

- Reverse-extracted the two strict transport candidates at a fixed offset
  from their moving top degree.  Each coefficient is exactly a finite sum
  `sum_a a^(2n) P_(t,a)(n)` with fixed rational polynomials.
- Proved the complete natural escape bands: the highest eight coefficients
  of the odd transport are positive for every `s>=8`, and the highest ten
  coefficients of the even transport are positive for every `s>=9`.
- The dominant-page term cancels identically in the highest coefficient;
  the proof correctly drops from base 6 to 5 in the odd branch and from
  base 7 to 6 in the even branch.
- For the other columns, a fixed dominant-exponential ratio is monotone
  after the explicit shifts `(0,2,1,1,0,0,0,1)` and
  `(0,4,3,2,1,1,1,2,2,3)`.  Exact certificates check 330 shifted
  monomials, 24 earlier values, and 72 direct reverse-index comparisons.
- This is an all-parameter boundary theorem, not an extrapolation from the
  `m<=100` scan.  The bulk coefficients of both transports remain open.

## 13:32--13:58: third-active transport low columns

- Kept the exact scale difference in the top `B6/B7` transport and used
  `(s+1)^N-s^N>=N*s^(N-1)`.  This Bernoulli gain is essential: deleting
  it makes the odd coarse kernel's constant coefficient negative from
  `s=16` onward.
- Dropped the favorable transported-middle and next-bottom terms, and
  overpaid the remaining negative bottom transport by replacing each
  nonnegative power of `s-2` by the corresponding power of `s`.
- The resulting sufficient kernels prove the first 31 coefficients of
  both transports for every stable parameter in the natural bulk range.
  Their shifted fixed-column certificates contain 775 odd and 837 even
  strictly positive monomials.
- Independently certified the needed `B6/B7` discrete page remainders on
  the same columns (713 and 775 nonnegative shifted monomials), so lowering
  their scale from `(s+1)^N` to `s^N` has no hidden sign assumption.
- Combined with the reverse bands, the complete transports are now proved
  through odd `s=21` and even `s=22`.  The conclusion retained for
  unbounded parameters is only the two low bands plus the two top bands;
  the growing middle interval remains open.

## 13:58--14:15: fixed-layer recurrence obstruction

- Rewrote the odd sufficient kernel recurrence, after clearing its
  positive denominator, as five fixed-degree kernels on bases
  `u_6,...,u_2`; direct reconstruction passed.
- Expanding around `u_2`, found an exact obstruction to every fixed merge
  depth.  The beta-linear coefficient of layer `r` is
  `-32(3^r-3*2^r+3)s+408*4^r-1392*3^r+1728*2^r-912`.
- For every fixed `r>=3` its leading coefficient in `s` is negative.
  The first small witness is `[beta]R_(17,4)=-1152`; the `r=3` layer is
  already `-96(2s-15)`.
- This refutes only termwise positivity after a fixed number of merged
  layers.  The actual sufficient-kernel recurrence and transport remain
  open and may require a growing-depth or `d/s` argument.

## 14:15--14:35: normalized interior symbols

- Reorganized both sufficient kernels and both required `B6/B7` page
  remainders into common-exponent sums over bases `u_2,...,u_p`.
- For `theta=d/s` in a compact subinterval of `(0,2)`, proved a uniform
  coefficient-symbol lemma.  Every lower base is suppressed by a factor
  at most `poly(s)*((p-1)/p)^(epsilon*s)`.
- The odd sufficient/page symbols factor as respectively
  `1119744*x^16*(1+6x)^2` and
  `4478976*x^16*(1+6x)^2`.  The even constants are `161414428` and
  `807072140`, with common factor `x^20*(1+7x)^2`.
- Under `x=theta/(p*(2-theta))`, none of the four symbols has an interior
  zero.  This proves both transports throughout every macroscopic window
  `epsilon*s<=d<=(2-epsilon)*s` for all sufficiently large `s`.
- The unresolved growing middle is now localized to two mesoscopic
  boundary layers: `d` or `2s-d` tends to infinity but remains `o(s)`.

## 14:35--14:50: logarithmic low-boundary localization

- Strengthened the dominant-symbol calculation to an exact coefficientwise
  statement: the dominant kernels for both sufficient inequalities and both
  page differences are nonnegative after the stable shifts.  Their four
  certificates contain 126, 176, 80, and 120 positive monomials.
- Retained one explicit positive dominant summand in each half of the
  binomial support.  Every lower-base monomial is bounded relative to it by
  `C*s^(M+q)*((p-1)/p)^d`; the worst budgets are `M+q=30` for `p=6` and
  `M+q=36` for `p=7`.
- Since `241*log(6/5)>30` and `241*log(7/6)>36`, all four required kernels
  are strictly positive whenever `d>=241*log(s)` and `s` is sufficiently
  large.  The old top-band theorem closes the degrees above the bulk cutoff.
- Consequently the high mesoscopic layer is no longer open.  Combining with
  the 31 fixed low columns localizes the entire remaining transport gap to
  `31<=d<241*log(s)`.  The threshold in `s` remains existential, and neither
  complete transport is promoted.

## 15:35--15:42: blind audit

- Root reconstructed the four common-base indices, retained endpoint
  legality, exact 30/36 polynomial budgets, rational logarithmic margins,
  and both bulk/top splices without importing the author workbench into the
  new scalar verifier.  The fixed-layer witness was also recovered.
- Verdict: `PASS AFTER REPAIR`.  The only mathematical-language repair was
  to state explicitly that `31<=d<241*log(s)` is the eventual frontier for
  `s>=S`, not a classification of all parameters below the ineffective
  threshold.  OPG-1757 and both complete transports remain open.
