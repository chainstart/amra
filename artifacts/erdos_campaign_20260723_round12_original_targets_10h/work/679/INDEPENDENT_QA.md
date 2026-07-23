# Erdős #679 round-12 adversarial QA

Date: 2026-07-23

Verdict: **PASS AS A STRICT MOVING-CUTOFF REDUCTION; ORIGINAL FIRST
QUESTION OPEN; CLOSURES = 0.**

This audit targets the new point that is easiest to overstate: the local hit
value \(\rho\) tends to zero, while the conductor coefficient tends to one.
Every error must therefore be smaller than the deliberately retained margin
\(\Delta HL=HL/L_3\).

## 1. Original quantifiers and integer threshold

The target used is

\[
 \forall\varepsilon>0\ \exists K_\varepsilon\ \forall N_0\ \exists n>N_0\
 \ \forall k\in[K_\varepsilon,n):\quad
 \omega(n-k)<(1+\varepsilon){\log k\over\log\log k}.
\]

With
\(r_\varepsilon(k)=\lceil(1+\varepsilon)\log k/\log\log k\rceil-1\),
the strict inequality is exactly equivalent to
\(\omega(n-k)\le r_\varepsilon(k)\).  There is no equality or floor error.
For a candidate and large \(X\), the block \(H\le k<2H\) lies beyond its
fixed \(K_\varepsilon\) and below \(n\asymp X\).  Thus \(T(n)\le R\)
holds with the exact \(R\) used to define \(\rho=R/(HL)\).

This is only a necessary condition on every candidate.  It neither changes
the order of the target quantifiers nor proves the negation.

## 2. Size of the moving parameter

For fixed \(d\ge1\),

\[
 \log H=dL_2+o(1),\quad
 \log\log H=L_3+\log d+o(1),\quad
 \log\log z=L_2-L_3.
\]

Hence

\[
 L=L_2-2L_3-\log d+o(1),\qquad
 \rho={(1+\varepsilon)d+o(1)\over L_3}.
\]

So \(0<\rho<1\), \(b=1-\rho\), and
\(\sigma=I(\rho)-1/L_3>0\) eventually.  Expanding \(I\) only after the
exact proof gives

\[
 \sigma=1-{(1+\varepsilon)d\over L_3}
 \left(1+\log{L_3\over(1+\varepsilon)d}\right)
 -{1+o(1)\over L_3}.
\]

The asymptotic replacement error in \(\rho\) is
\(O_{d,\varepsilon}(L_3^{-2})+O(L_3/L_2)\); after multiplication by
\(1+\log(1/\rho)=O(L_4)\), it is \(o(1/L_3)\).  It cannot consume the
chosen margin.

## 3. Lower prime endpoint is uniform as \(\rho\to0\)

For \(H<p<2H\), neither \(H/p=o(1)\) nor a uniform local Taylor expansion
is asserted.  Both moment factors are at least
\(1-H/p\ge(2H)^{-1}\).  There are \(O(H/\log H)\) primes in this segment,
so replacing its logarithm by the corresponding linear sum costs at most
\(O(H)\), uniformly in \(\rho\).

For \(p\ge2H\), the quadratic Taylor remainder totals
\(O(H^2\sum_{n\ge2H}n^{-2})=O(H)\).  Therefore

\[
 \log\mu=-(1-\rho)HL+O(H),\qquad
 \log M_2=-(1-\rho^2)HL+O(H)
\]

with constants independent of the moving \(\rho\).

## 4. Exact energy normalisation

For \(x=H/p\), the local centred variance is
\(b^2x(1-x)\), and the local second moment is
\(1-(1-\rho^2)x\).  Thus the normalised energy inclusion parameter is

\[
 \theta_p={b^2x(1-x)\over1-(1-\rho^2)x}.
\]

For \(p\ge2H\), the exact difference is

\[
 b^2x-\theta_p
 ={b^2\rho^2x^2\over1-(1-\rho^2)x},
\]

not an uncontrolled relative \(o(1)\).  Summing it costs \(O(\rho^2H)\);
the lower endpoint costs \(O(H/\log H)\).  Hence
\(\Lambda=\sum\theta_p=b^2HL+O(H)\), uniformly.

ANOVA orthogonality and Parseval make the subset coordinates genuinely
independent after energy normalisation.  This is not a heuristic
probabilistic model.

## 5. Poisson-binomial and conductor errors fit inside the margin

The conductor cutoff implies

\[
 |T|\le r_0={\sigma HL\over\log H}=O_d(H),
\]

whereas \(\Lambda\asymp HL\).  Exponential Markov with
\(y=r_0/\Lambda\) gives

\[
 \log\mathbb P(|T|\le r_0)
 \le-\Lambda+r_0+r_0\log(\Lambda/r_0)
 =-b^2HL+O_d(HL_3).
\]

The complete second-moment error adds only \(O(H)\).  The resulting low
energy exponent is therefore \(-2bHL+O_d(HL_3)\).  Since

\[
 {HL_3\over HL/L_3}={L_3^2\over L}=o(1),
\]

this error is uniformly \(o(\Delta HL)\).

## 6. Physical interval and Farey factors fit inside the margin

All non-empty ANOVA frequencies are primitive.  Different subsets have
different squarefree conductors, so reduced fractions do not collide.
The additive large sieve contributes \(N-1+\mathcal C_X^2\), and physical
Cauchy contributes \(N^{1/2}\).  At \(d=1\), the worst allowed case,

\[
 {\log N\over\Delta HL}
 \asymp {L_3\over L_2}=o(1).
\]

Thus the logarithm of the low-conductor signed interval sum is at most

\[
 -\{\rho\log(1/\rho)+\Delta-o(\Delta)\}HL.
\]

No complete-period averaging over the interval start occurs in this step.

## 7. Candidate comparison uses an exact entropy identity

The candidate contribution is at least

\[
 \rho^R=\exp\{-\rho\log(1/\rho)HL\}
\]

because \(R=\rho HL\) exactly.  The low term has the additional strict
\(\Delta HL\) saving.  The zero term is smaller because

\[
 (1-\rho)-\rho\log(1/\rho)
 =1-\rho+\rho\log\rho=I(\rho)>0.
\]

It follows only that the complementary high-conductor **signed** sum is
positive and at least \((1-o(1))\rho^R\).  Positivity is not an upper bound,
absolute coefficient estimate, or contradiction.

## 8. Remaining gap and source boundary

The uncontrolled tail begins at the explicit threshold

\[
 c(T)>
 \exp\left(\left[I(\rho)-{1\over L_3}\right]HL\right),
 \qquad
 \rho={R\over HL}\sim{(1+\varepsilon)d\over L_3}.
\]

No checked theorem of Lau, Tao--Teräväinen, Bettin--Chandee, Wright, or
van Doorn--Tang bounds that signed tail at the self-consistent start.
Lau's Section 7 alternative remains conditional on Conjecture 8.

The official first question therefore remains open.  The already-disproved
additive-constant second question is not counted.  No finite computation is
used as asymptotic evidence.

## 9. Adversarial QA of the far-shift theorem

The Hardy--Ramanujan input used in
`hardy_ramanujan_far_shift_reduction.md` is uniform in **all** integers
\(j\ge1\); no fixed-\(j\) asymptotic is extrapolated.  For a fixed
\(k\), writing \(m=n-k\) maps every relevant \(n\in[X,2X]\), \(k<n\),
into \(1\le m\le2X\).  Thus the global level-set bound at \(2X\) is a
valid (deliberately wasteful) upper bound even when \(k>X\).

For any fixed

\[
 K_X=\exp\{(\log_2X)^{D_\varepsilon}\},\qquad
 D_\varepsilon>{1+\varepsilon\over\varepsilon},
\]

one has \(K_X=X^{o(1)}<X\) eventually.  Uniformly for
\(K_X\le k<2X\), \(v=\log_2k\ge D_\varepsilon L_3\), and direct
substitution gives

\[
 (r_k-1)\log((r_k-1)/(eB_X))
 \ge(1+\eta_D/2)\log k,
 \qquad
 \eta_D=(1+\varepsilon)(1-1/D_\varepsilon)-1>0.
\]

The factorial tail is geometric because \(r_k\ge2B_X\).  Summing the
resulting \(k^{-1-\varepsilon/4}\) estimate over every integer
\(K_X\le k<2X\) covers the complete condition \(K_X\le k<n\) for every
\(n\in[X,2X]\); it is not a dyadic sampling of \(k\).

The theorem only says that the set of far-bad \(n\)'s has density
\(O_{\varepsilon,D}(K_X^{-\eta_D/2}/\log X)\).  Its cardinality can
still be \(X^{1-o(1)}\).  A near-good integer supplied by a nonuniform
sieve may lie inside it.  Also \(K_X\) grows with \(X\), so it is not the
fixed \(K_\varepsilon\) in the original quantifier.  The theorem confines
the task to a growing near range for almost every dyadic integer; it does
not prove the required intersection or an original candidate.

The bounded-density splice was also checked.  If \(M_X\) is the maximal
density ratio of a near-shift measure to uniform measure, the far-bad
probability is at most
\(M_XK_X^{-\varepsilon/4}/\log X\).  A primorial progression with
cutoff \(w=(\log X)^c\) has \(\log M_X\gg(\log X)^c\), much larger than
\(\log K_X=(\log_2X)^{D_\varepsilon}\).  Moreover inheriting small primes
all the way through \(K_X\gg\log X\) would make the primorial modulus
larger than \(X\).  This only invalidates a black-box density splice; it
does not exclude a Hardy--Ramanujan estimate proved directly under the
weighted measure.

The exponent audit is sharp for this architecture: at the lower endpoint,
the pointwise large-deviation exponent divided by \(\log k\) tends to
\((1+\varepsilon)(D-1)/D\).  It exceeds the unit exponent needed to sum
over all \(k\) exactly when \(D>(1+\varepsilon)/\varepsilon\).  Taking
\(D=2(1+\varepsilon)/\varepsilon\) gives \(\eta_D=\varepsilon/2\) and
recovers the displayed \(K_X^{-\varepsilon/4}\) saving with a factor-eight
smaller \(D\) than the initial safe choice.

The critical-power refinement was checked separately.  With
\(A=1+\varepsilon\), \(D_0=A/\varepsilon\), and

\[
 \log K_X^*=C_*B^{D_0}L^{D_0},
 \qquad C_*>(e/\varepsilon)^{D_0},
\]

write \(c_*=\log C_*-D_0\log(e/\varepsilon)>0\).  At the lower endpoint,
\(v=\log_2K_X^*=D_0L+D_0\log L+\log C_*+o(1)\), and direct cancellation
gives

\[
 v-D_0\{L+\log v-\log A+1\}=c_*+o(1).
\]

Since \(A(1-1/D_0)=1\), the factorial-tail exponent exceeds one by
\((Ac_*/D_0^2+o(1))/L\).  It is increasing with \(v\), so the estimate is
uniform for every larger \(k\).  Taking the smaller safe excess
\(\xi_X=Ac_*/(5D_0^2L)\), summation gives
\(X(\log X)^{-1}\xi_X^{-1}(K_X^*)^{-\xi_X}\).  Here
\(\xi_X\log K_X^*\to\infty\), while \(K_X^*=X^{o(1)}\).

The boundary was then audited one order further.  Set
\(M=\log L\), \(c_0=1-\log\varepsilon\), and
\(C_0=(e/\varepsilon)^{D_0}\).  At \(C_*=C_0\), exact substitution gives

\[
 v-D_0\{L+\log v-\log A+1\}
 =-D_0\log(1+(M+c_0)/L)+o(M/L)<0.
\]

Thus the equality coefficient is not admissible for this union-bound
argument.  With the moving coefficient
\(C_X=C_0\exp(3D_0M/L)\), the same difference instead equals

\[
 {D_0(2M-c_0)\over L}+O_\varepsilon(D_0M^2/L^2)
 \ge {D_0M\over L}.
\]

This gives the safe excess
\(\xi_X^\dagger=AM/(5D_0L^2)\) and the bound recorded as (17) in the
far-shift note.  Both signs follow from the unexpanded logarithm, so no
fixed-\(\varepsilon\) constant is swallowed by the asymptotic.  The
coefficient ratio tends to one, but the cutoff still depends on \(X\) and
the conclusion is still only almost-all.

The order of quantifiers is fixed \(\varepsilon\), hence fixed
\(D_0=1+1/\varepsilon\) and \(C_0\), followed by \(X\to\infty\).
Only \(C_X=C_0\exp(3D_0M/L)\) and
\(K_X^\dagger=\exp(C_XB^{D_0}L^{D_0})+O(1)\) vary.  Moreover
\[
 \xi_X^\dagger\log K_X^\dagger
 ={AC_X\over5D_0}B^{D_0}M L^{D_0-2}\to\infty,
\]
and \(K_X^\dagger=X^{o(1)}\).  Integer, endpoint, and \(O(1)\)
Hardy--Ramanujan errors are \(o(M/L^2)\) on the normalised-exponent scale,
strictly below \(\xi_X^\dagger\asymp M/L^2\).  The negative equality sign
is explicitly classified as a limitation of this HR union-bound
architecture, not as a transition for the original #679 question.

## 10. Adversarial QA of simultaneous energy/support saturation

For any fixed \(\sigma\) in a compact subinterval of \((0,\infty)\), the
top-prime family in `dense_top_band_barrier.md` has

\[
 r=\lfloor\sigma HL/\log z\rfloor,
 \qquad {\cal B}=\{z/2<p\le z\}.
\]

Here \(H=o(z)\), \(r=o(M)\), and the PNT applies at the moving endpoint.
The moving cutoff \(\sigma=I(\rho)-1/L_3\to1\) lies in such a compact
interval, so the calculation applies uniformly to the actual cutoff.
Flooring \(r\) and replacing \(z\) by \(z/2\) cost
\(O(\log z+r)=O_d(H)=o(HL)\) in logarithmic conductor.

Stirling gives \(\log{M\choose r}=\sigma HL-o(HL)\); the discarded term
is at most

\[
 r(\log\log z+\log r+O(1))
 \ll_d HL L_2^2/L_1=o(HL).
\]

Every primitive local Fourier coefficient is nonzero because
\(p>H\) and \(p\nmid H\), so the geometric sum of \(H\) consecutive
residues cannot vanish at a nonzero frequency.  Reduced fractions from
different squarefree conductors do not collide.  Therefore the primitive
support count really is \(\exp\{(2\sigma-o(1))HL\}\), not merely an upper
bound.  Pigeonhole and Farey separation then sandwich the actual minimum
spacing at \(\exp\{-(2\sigma+o(1))HL\}\).

The maximum squared coefficient in the same family is at most
\(\mu^2(O(H^2/z^2))^r
=\exp\{-2bHL-2\sigma HL+o(HL)\}\).  Comparing this with the total band
energy proves that the inverse-participation number is
\(\exp\{(2\sigma+o(1))HL\}\).  Hence the energy is not concentrated on an
exponentially sparse subset; this check uses the exact coefficient bound,
not the raw support count alone.

For energy, the probability of the selected family under the exact
normalised Bernoulli law is

\[
 {\mu^2\over M_2}
 e_r(\theta_p/(1-\theta_p):p\in{\cal B}).
\]

Using \(\theta_p/(1-\theta_p)\gg H/z\) loses only
\(O(rL_3)=o(HL)\) beyond the exact empty-set exponent \(-b^2HL+O(H)\).
After multiplying by \(M_2\), the same narrow band has energy
\(\exp\{-2bHL-o(HL)\}\).

This simultaneous saturation rules out a fixed exponential gain based
only on total band energy, raw/effective support count, or minimum spacing.  It does
**not** show that the large-sieve operator norm is attained by the actual
coefficient vector.  Coefficient-sensitive phase cancellation remains a
logically open route; no universal impossibility claim is made.

## 11. Adversarial QA of the low-cutoff block obstruction

Goudout's arXiv:1607.08666 TeX was checked directly, not through a search
snippet or secondary summary.  The strengthened obstruction uses its
Theorem 2, which is uniform for \(5\le j\le\log_2X\) under

\[
 F_j(X)(\log_3X)^{2+\eta}\le\delta_j(X)h\le X,
\]

and gives a positive lower bound
\(\gg\delta_j(X)h/F_j(X)\) for almost every real starting point
\(x\asymp X\).  Put

\[
 A=1+\varepsilon,\quad B=\log_2X,\quad
 L=\log_3X,\quad M=\log_4X,
\]

and, for fixed \(0\le\theta<A\), take

\[
 H=\left\lfloor e^{B-\theta BM/L}\right\rfloor,
 \qquad
 j=\left\lceil A{\log(2H)\over\log_2(2H)}\right\rceil.
\]

Then \(j=(A+o(1))B/L\), so \(5\le j\le B\), and
\(F_j(X)=(A^{-2}(1-e^{-A})^{-1}+o(1))L^2\).  For
\(q=j-1\), the exact density is
\(\delta_j=\lambda(q/B)B^q/(e^Bq!)\).  The Euler product defining
\(\lambda\) has a summable logarithmic derivative at zero, so
\(\lambda(q/B)\to1\).  Stirling, including floor/ceiling errors, gives

\[
 \log(\delta_jH)=(A-\theta+o(1)){BM\over L}\to+\infty.
\]

This dominates \(\log(F_jL^{2+\eta})=O(M)\), and the upper condition
\(\delta_jH\le X\) is automatic.  Thus every hypothesis of Theorem 2 is
met.  With integer \(H\), the
count in \((x,x+H]\) is constant as \(x\) runs between two consecutive
integers.  Therefore a measure-\(o(X)\) exceptional set of real starts
contains only \(o(X)\) exceptional integer starts.  Translating the start
to \(n-2H\) discards only \(O(H)=o(X)\) boundary endpoints.

For every remaining endpoint, the supplied \(m\in(n-2H,n-H]\) gives
\(k=n-m\in[H,2H)\).  Monotonicity of
\(\log t/\log_2t\), together with the ceiling defining \(j\), makes
\(\omega(n-k)=j\) a genuine violation of the strict #679 inequality.
Hence the bad endpoints have cardinality \((1-o(1))X\), not merely
positive density.

This does not contradict the high far-cutoff theorem: the two cutoffs are
vastly different.  Nor does an almost-everywhere statement rule out a
sparse infinite exceptional sequence, so it is not a disproof of #679.
It does rule out lowering an **almost-all far-good** cutoff to this scale.
Theorem 1 independently gives the same conclusion at the much larger
initially proposed scale \(H=e^{C\log_2X\log_3X}\).  No statement is
extrapolated to \(H=(\log X)^C\) for a fixed \(C<1\).

The sharper cutoff was checked through third order.  Put
\(T=M+1-\log A\) and

\[
 s_0={AT\over L}-{A^2T(T-1)\over L^2}.
\]

Direct symbolic expansion, independently reproduced by
`verify_goudout_cutoff_series.py`, gives
\[
 \kappa\{\log(1/\kappa)+1\}
 ={AT\over L}-{A^2T(T-1)\over L^2}+{C_3(A,T)\over L^3}
  +O_A(T^4/L^4),
 \quad
 C_3(A,T)={A^2T\over2}(2AT^2-5AT+2A+2T-2).
\]
Since \(C_3(A,T)=(A^3+o_A(1))T^3>0\), the former second-order
\(\gamma=0\) boundary is admissible:
\(\log(\delta_{r_0}H_0)=(A^3+o_A(1))BT^3/L^3\to\infty\).
Floor, ceiling, \(\lambda\), and Stirling errors are all little-oh of this
quantity.  One order closer, taking
\(s_\gamma=s_0+(C_3-\gamma)/L^3\) gives
\(\log(\delta_{r_\gamma}H_\gamma)
=(\gamma+o(1))B/L^3\).  At the new third-order zero-margin truncation,
one more expansion gives

\[
 C_4(A,T)=(-A^4+o_A(1))T^4<0,
 \qquad
 \log(\delta_rH)=(C_4+o(T^4))B/L^4\to-\infty.
\]

Thus Goudout's exact-level density condition actually fails at that
truncation; this fourth-order sign is also checked in the symbolic output.

The applicability conditions were checked uniformly with the correct
order of limits: first fix \(\varepsilon>0\), the third-order margin
\(\gamma>0\), and Goudout's auxiliary \(\eta>0\), then let \(X\to\infty\).
Indeed,

\[
 s_0={AT\over L}\{1-A(T-1)/L\}\in(0,1),
 \qquad s_\gamma=s_0+O_A(T^3/L^3)\in(0,1)
\]

eventually.  Thus \(H_\gamma\to\infty\) and
\(H_\gamma=\exp((1-o(1))B)=X^{o(1)}\).  Also
\(r_\gamma/B=(A+o(1))/L\), so \(5\le r_\gamma\le B\), exactly the
range of Theorem 2.  Its upper condition holds because
\(\log(\delta_rH)=O(BT^3/L^3)=o(\log X)\).  Its lower condition holds
with room to spare since

\[
 F_r=(A^{-2}(1-e^{-A})^{-1}+o(1))L^2,
 \quad
 \log\{F_rL^{2+\eta}\}=O_\eta(M),
\]

whereas even the closer third-order-margin construction has
\(\log(\delta_rH)\sim\gamma B/L^3\gg M\).

Flooring \(H\), replacing \(H\) by \(2H\) in the threshold, and ceiling
of \(r\) change the density logarithm by at most \(O_A(L+M)\).  The
Euler factor has \(\log\lambda((r-1)/B)=O_A(1/L)\), and Stirling's
remainder is \(O(L)\).  All are
\(o(B/L^3)\).  The analytic series remainder is
\(O_A(BT^4/L^4)=o(B/L^3)\).  Therefore none can consume fixed
third-order \(\gamma\), and they are also negligible relative to the
positive \(A^3BT^3/L^3\) term at the old second-order zero-margin point.

This exact-level optimisation is deliberately not advertised as a stronger
#679 obstruction.  At all of these \(H=(\log X)^{1-o(1)}\) scales the
target threshold is \(o(B)\), whereas the normal order of
\(\omega(n-H)\) is \((1+o(1))B\).  One deterministic moving shift already
makes \((1-o(1))X\) endpoints violate #679.  Goudout's fine threshold
instead audits when an interval contains the much rarer exact level
\(\omega=r\).  Its substantive extension for #679 begins at
\(H=e^{CBL}\) with \(AC>1\), where a fixed shift is normally below the
target but a whole block still finds a rare high-\(\omega\) value.

Finally, the fixed-\((\varepsilon,K)\) candidate-density corollary uses
the adjacent shifts \(k_X=\lfloor\log X\rfloor\) and \(k_X+1\).  After
increasing the common integer threshold by at most one, a candidate forces
both \(\omega(m),\omega(m+1)\le(A+o(1))B/L\).  The exact-level densities
increase geometrically up to this endpoint, and

\[
 \sum_{j\le(A+o(1))B/L}\delta_j(X)
 \le\exp\{-B+(A+o(1))B(M+1-\log A)/L\}.
\]

Goudout's published two-shift corollary at fixed difference \(b=1\)
bounds each joint exact level by \(O(\delta_{j_1}\delta_{j_2}X)\).
Summing gives

\[
 \#\mathcal G_{\varepsilon,K}(X)
 \ll {X\over(\log X)^{2-o(1)}}.
\]

The \(O(\log X)\) endpoint translation loss is negligible.  Only the
stated two-shift theorem is used, not the paper's remark that more fixed
translates should be accessible.  This quantitative density zero still
does not imply finiteness or exclude a sparse infinite sequence.

The separate primorial check is also exact.  If \(Q=p_1\cdots p_j\), then
\(Q=H^{1+\varepsilon-o(1)}>2H\).  The length-\(H\) translation intervals
attached to distinct multiples of \(Q\) are disjoint, so the pair-to-endpoint
map is injective and supplies \(XH^{-\varepsilon+o(1)}\) actual bad
endpoints.  This is an operator-level obstruction only; the stronger
almost-all conclusion comes from Goudout.

## 12. Adversarial QA of the Lau mass comparison

Lau v2's equation `eqn:probabilitydenominator` was checked in the official
TeX.  Since \(\log W=(0.6+o(1))\log x\), while the logarithms of
\(\prod_{k\le K}\log R_k\), \((W/\varphi(W))^K\), and \(c_0^K\) are all
\(o(\log x)\), it gives \(Z=\sum_n\nu(n)=x^{0.4+o(1)}\).

The first-hand source defines \(\eta:\mathbb R\to[0,1]\), supported on
\([-1,1]\), and then defines
\(\widetilde\eta(u)=e^{-u}\eta(u)\).  For \(d\ge1\), its argument is
nonnegative, so \(|\widetilde\eta|\le1\) and its support forces
\(d\le R_k\).  Consequently each divisor sum has absolute value at most
\(\min\{R_k,\tau(n+k)\}\).  Here \(k\le K=(\log x)^{1/1000}=o(x)\)
and \(n\in[x,2x]\), hence \(n+k\le3x\) eventually.  The standard uniform
divisor bound \(\tau(m)\le x^{C/\log_2x}\) for \(m\le3x\) then gives

\[
 {\log\max_n\nu(n)\over\log x}
 \le2\sum_{k\le K}\min\left\{{1\over100k^{50}},
                              {C\over\log_2x}\right\}
 =O((\log_2x)^{-49/50}).
\]

Here the split point is
\((\log_2x/(100C))^{1/50}\): the initial and tail sums are both
\(O((\log_2x)^{-49/50})\).  Therefore
\(\max\nu=x^{o(1)}\), and a fixed positive amount of Lau weight guarantees
an unweighted count \(x^{0.4-o(1)}\).  This strengthens the crude
\(x^{0.3799\ldots-o(1)}\) extraction, but the far exceptional upper bound
remains \(x^{1-o(1)}\), so no intersection follows.  Equivalently, the
maximum density ratio is still only bounded by \(x^{0.6+o(1)}\).

A full-text search of the v2 TeX found no \(\sum\nu^2\) estimate, sharper
stated max-weight bound, or direct support-cardinality lemma that changes
this comparison.  Goudout's \(o(x)\) exceptional set can likewise contain
all \(x^{0.4+o(1)}\) points on the basic progression \(W\mid n\).  Finally,
Lau's proved near conclusion is \(C\log k\), not the exact #679 threshold,
independently of the mass issue.

The apparent repair “first prove the far estimate inside \(W\mid n\)” was
also checked against the cited sources.  It requires a Hardy--Ramanujan
large-deviation estimate for the growing-coefficient forms \(Wa-k\), where
\(W=x^{0.6+o(1)}\).  Spiro's arithmetic-progression theorem states
uniformity only for moduli at most a fixed power of \(\log x\).  Fan's
Theorem 1.1 applies to prime factors of the running integer in a sifted set
with a fixed bound on forbidden residue classes; it does not directly
cover \(\omega(Wa-k)\) with growing \(W,k\).  No such uniform theorem is
silently assumed.

## 13. Revalidation of the inherited many-fixed-shift bound

Tenenbaum's published Theorem 1 (arXiv:1710.04877; *J. Number Theory*
188 (2018)) was checked directly.  It proves, rather than merely remarks
on, the joint local upper bound for every fixed number of irreducible,
pairwise coprime polynomial arguments without a fixed prime divisor.

Taking genuinely consecutive shifts for \(r\ge2\) would violate the last
hypothesis: their product is divisible by every prime \(p\le r\) at every
integer.  The revalidation instead takes
\(P_r=\prod_{p\le r}p\) and \(Q_j(m)=m-jP_r\).  For \(p\le r\), all
roots coalesce at zero and do not cover residue \(1\); for \(p>r\), at
most \(r<p\) residues are roots.  Thus there is no fixed prime divisor.
The polynomials and their discriminant/coefficient factor are fixed once
\(r\) is fixed.

All target shifts are \(\lfloor\log X\rfloor+jP_r\), hence are admissible
and have threshold \((1+\varepsilon+o(1))B/L\).  This lies in Tenenbaum's
proved range \(1\le k_j\le R B\).  Summing exact levels yields

\[
 \# {\cal G}_{\varepsilon,K}(X)
 \ll_{\varepsilon,K,r}{X\over(\log X)^{r-o(1)}}.
\]

Choosing fixed \(r>C\) gives
\(\# {\cal G}_{\varepsilon,K}(X)\ll_{\varepsilon,K,C}
X/(\log X)^C\) for every fixed \(C\).  This result was already present in
earlier campaign records and is classified here as **inherited/revalidated,
not round-12-new**.  The separately reported \(r=2\) estimate uses
Goudout's formally proved fixed-\(b=1\) corollary verbatim, not his
more-shifts remark.  Neither estimate implies finiteness.

## 14. Final QA verdict at this stage

The principal new unconditional outputs are:

1. the entropy-optimised cutoff approaching coefficient one;
2. the far-shift exceptional-set estimate, including the
   tending-to-critical constant refinement;
3. the simultaneous energy/support/spacing barrier at the cutoff;
4. the rigorous almost-all-bad obstruction at the proposed lower cutoff;
5. the pointwise Lau-weight improvement \(\max\nu=x^{o(1)}\), together
   with the still-quantitative failure of a black-box far-good splice.

All are strict partial results or method diagnostics.  None supplies the
missing signed high-conductor upper bound, none proves Lau's Conjecture 8,
and none produces or excludes infinitely many original candidates.
Verdict remains **OPEN, closures = 0**.
