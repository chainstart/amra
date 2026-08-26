# Independent reconstruction (blind first stage)

Completed at 2026-08-26T14:45:17+08:00, before opening any author evidence for this campaign.  In particular, during this first stage I did **not** read `evidence/parametric_frontier_proof.md`, `evidence/frontier_falsification.md`, `evidence/theorem41_uniformity_audit.md`, `evidence/frontier_algebra_replay.json`, or `audit/adversarial_self_audit.md`.  The mathematical inputs used were only the frozen `closure_contract.json`, van Doorn--Tang arXiv:2606.19863v1 (Theorem 4.1 and Sections 2--6 as needed to check the range partition), and the upstream Lean source described below.  Repository phase metadata and the AMRA/OpenMath rules were read only to establish that this is the `independent_audit` phase and to follow the required resource policy.

## Verdict reconstructed without the author proof

For every **fixed** \(\theta\in(2/5,3/5)\) satisfying the frozen prime input \(\mathrm{PI}(\theta)\), the supremum delivered by the stated Theorem-4.1 certificate class is
\[
c_*(\theta)=\frac{1-\theta}{3}.
\]
More precisely:

* every fixed \(0<c<(1-\theta)/3\) is proved, with the threshold in \(k\) allowed to depend on \(c,\theta\), and on the prime-input constant;
* every fixed \(c>(1-\theta)/3\) is impossible for the delimited nonnegative Theorem-4.1 comparison certificates, even after finite or polylogarithmic segmentation into comparable blocks;
* the endpoint \(c=(1-\theta)/3\) is **not** an \(o(k^\theta/\log k)\) certificate.  It is not, however, an unconditional exact-constant no-go.  With the explicit upstream Lean constant \(c_6\), the best first-two-term coefficient tends to
  \[
  c_6 d_\infty,\qquad
  d_\infty=2^{1/3}+2^{-2/3}.
  \]
  Thus the endpoint is certifiable by this inequality if an available prime-count lower constant is strictly larger than \(c_6d_\infty\), and it is not certifiable from this comparison when that lower constant is smaller.  The frozen qualitative hypothesis only asserts the existence of some positive constant and gives no such size comparison.  Consequently the correct universal result under the frozen input is the open inequality \(c<c_*\), while \(c_*\) is still the supremum.

This endpoint distinction is essential: a blanket no-go for all \(c\ge c_*\) would overstate what the nonnegative-bound argument proves.  The robust constant-free no-go range is \(c>c_*\); at equality one has a sharp constant competition.

## Source inequality and uniformity in the derivative order

Write \(L=\log k\), \(M=\log L\), and let \(K\) be the bad-point count in a prime block.  The paper's Theorem 4.1 gives, for every integer
\(2\le r\le \tfrac12 k^{1-\theta}\) and every \(\lambda\ge1\),
\[
K\ll k^\theta(A+B+T)+r\lambda,
\]
where
\[
\begin{aligned}
A&=\left(\frac{nr!\lambda^r}{k^{r+1}}\right)^{1/(2r-1)},\\
B&=\left(\frac{k^{r+\theta}}{nr!\lambda^r}\right)^{1/(r-1)},\\
T&=\left(\frac{(r+1)\lambda}{k}\right)^{1/(2r)}.
\end{aligned}
\]

The needed hidden constant really can be chosen independently of \(r\).  At upstream repository commit `92a033fa99f0a53a3c16257c47e3d9e04dfc3f55`, `ErdosProblem451.lean` states `konyagin_thm` with one fixed numerical definition `c₆` and error `2*r*lam`; `konyagin_application` then gives the displayed specialization for arbitrary `r`, arbitrary `lam`, and arbitrary `theta` satisfying `0 < theta < 1`.  The definitions are `K_const := max 4 c₉`, `B_const := 16*K_const`, `C₀_const := 4*B_const`, and `c₆ := 4*C₀_const`, none depending on \(r\).  Static source inspection found no `sorry` or `admit`; the only declared axiom in the file is the fixed-\(21/40\) Baker--Harman--Pintz input used later by `main_theorem`, not by `konyagin_thm` or its specialization.

Upstream source URL: <https://github.com/Woett/ChatGPT-s-note-on-Erdos451/blob/92a033fa99f0a53a3c16257c47e3d9e04dfc3f55/ErdosProblem451.lean>.  The Git blob is `ca59562120ba9698856dbaec6af6fb57ae3bd63f` (330548 bytes), and the raw-file SHA-256 independently obtained under the OpenMath memory guard is `44e478bed8d756f271aaffd45af5fa4797fbee857aa780f7412275a521b84004`.

This is a dependency/source audit, not a claim that I locally replayed the whole 330 kB file in the Lean kernel: the upstream file requests Lean 4.28.0, while the available AMRA project is pinned to 4.26.0 (and the global executable is 4.33.1).  The parametric-frontier argument below is therefore an independently reconstructed natural proof using the exact uniform theorem statement, not a new formalization.

## The \(\lambda\)-optimization and the invariant

Put \(a=2r-1\), \(b=r-1\), and \(t=nr!\lambda^r\).  Direct elimination of \(t\) gives the exact invariant
\[
A^aB^b=k^{\theta-1}. \tag{1}
\]
It follows immediately that
\[
\max(A,B)\ge k^{(\theta-1)/(3r-2)}. \tag{2}
\]
Arbitrary choice of \(\lambda\) cannot change this obstruction.  The exact unconstrained minimum of \(A+B\), subject to (1), occurs when
\(B=(b/a)A\) and equals
\[
d_r k^{(\theta-1)/(3r-2)},\qquad
d_r=\left(\frac ab\right)^{b/(a+b)}+
    \left(\frac ba\right)^{a/(a+b)}. \tag{3}
\]
Here \(d_r\to d_\infty=2^{1/3}+2^{-2/3}\).

For the simpler equalized choice used in Section 6, set
\[
e_r=(1-\theta)\frac{2r-1}{3r-2},\qquad
\lambda_0^r=\frac{k^{r+1-e_r}}{nr!}. \tag{4}
\]
Then
\[
A=B=k^{(\theta-1)/(3r-2)}. \tag{5}
\]
The exact minimizer in (3) is obtained from (4) by multiplying
\(t\) by \((a/b)^{ab/(a+b)}\), equivalently multiplying \(\lambda_0\) by the positive \(r\)-th root of that factor.  This changes no power or logarithmic estimate.

## Minimal \(r\) and the positive theorem

In the large range define the paper's integer
\[
r_p=\min\{r\ge1:nr!\le k^{r+\theta}\}. \tag{6}
\]
For \(n>\tfrac12k^{2+\theta}\), one has \(r_p\ge3\).  For every fixed \(\rho>c\), and all sufficiently large \(k\),
\[
r_p\le \left\lceil\rho\frac{L}{M}\right\rceil. \tag{7}
\]
Indeed, \(\log n\le cL^2/M\), whereas for the integer on the right the leading term of \(rL\) is \(\rho L^2/M\), which dominates both \(\log n\) and \(\log(r!)=O(L)\).  At the worst endpoint \(n=\lfloor\exp(cL^2/M)\rfloor\), Stirling also gives
\[
r_p=c\frac{L}{M}+O(1), \tag{8}
\]
so the factor `2c` in the source paper's convenient reference order is not the optimized asymptotic order.

Minimality in (6) gives
\[
n(r_p-1)!>k^{r_p-1+\theta}. \tag{9}
\]
The definition (6) also makes (4) admissible, because
\[
r+1-e_r-(r+\theta)
=(1-\theta)\frac{r-1}{3r-2}>0,
\]
so \(\lambda_0\ge1\).  The bound (7) also implies
\(r\le\tfrac12k^{1-\theta}\) for large \(k\), uniformly for all \(n\) in the large range.

Now fix \(c<(1-\theta)/3\), and choose once and for all
\[
c<\rho<\frac{1-\theta}{3}.
\]
Equations (5) and (7) give
\[
A+B\le 2L^{-(1-\theta)/(3\rho)+o(1)}=o(L^{-1}). \tag{10}
\]

The remaining two terms do not alter the frontier.  From (4) and (9),
\[
\lambda^r<\frac{k^{2-\theta-e_r}}{r}
\le k^{2-\theta-e_r}. \tag{11}
\]
Consequently, uniformly for \(3\le r\le \rho L/M+O(1)\),
\[
\log T
\le-\frac{L}{2r}+O\!\left(\frac{L}{r^2}+\frac{\log r}{r}\right)
\le-\left(\frac1{2\rho}+o(1)\right)M.
\]
Since \(\rho<(1-\theta)/3<1/5\), this is \(o(L^{-1})\).

For the additive term, the real function
\[
g(r)=\frac{2-\theta-e_r}{r}
=\frac{4r-r\theta+\theta-3}{r(3r-2)}
\]
is decreasing for \(r\ge3\) throughout the frozen \(\theta\)-range.  Hence
\[
\lambda\le k^{g(3)}=k^{(9-2\theta)/21},
\quad
r\lambda\le O(L/M)k^{(9-2\theta)/21}
=o(k^\theta/L), \tag{12}
\]
because \((9-2\theta)/21<\theta\) is equivalent to \(\theta>9/23\), and the frozen assumption \(\theta>2/5\) is stronger.  Thus Theorem 4.1 gives
\(K=o(k^\theta/L)\) in the complete large range.

The symbolic derivative check for \(g\), and the exact factor in (3), were independently recomputed with
`/home/biostar/work/projects/openmath/bin/openmath-memory-guard -- python3 -c ...`; the guard reported unit `openmath-task-20260826-143954-112179.scope`.

## All \(n\)-ranges and the output prime interval

The source ranges meet without a gap:

1. **Small:** \(2k<n\le\tfrac12k^{2-\theta}\).  Choose \(m\) with \(mk<n\le(m+1)k\), so \(2\le m\le\tfrac12k^{1-\theta}\).  If \(n<mk+mk^\theta\), a prime in
   \[
   \left(k+\frac{m}{m-1}k^\theta,
   k+\frac{2m-1}{m-1}k^\theta\right)
   \]
   makes \((m-1)p\in(n-k,n)\).  If \(n\ge mk+mk^\theta\), a prime in \((k,k+k^\theta)\) makes \(mp\in(n-k,n)\).  Since \((2m-1)/(m-1)\le3\), in both cases \(p\in(k,k+3k^\theta)\).

   The shifted interval in the first subcase has length exactly \(k^\theta\).  The frozen forward prime input at base \(x=k+O(k^\theta)\) initially gives a slightly longer interval of length \(x^\theta=k^\theta+O(k^{2\theta-1})\).  The excess contains only \(O(k^{2\theta-1})=o(k^\theta/L)\) integers, so deleting it retains a prime (indeed \(\gg k^\theta/L\) primes).  This supplies the translation that Section 2 uses and preserves the strict upper endpoint \(k+3k^\theta\).

2. **Medium:** \(\tfrac12k^{2-\theta}<n\le k^2/L^2\).  The elementary count in Section 3 is
   \[
   K<3+\frac{12k^{1+\theta}}n+\frac n{k^{2-\theta}}+4k^{2\theta-1}
   \le 3+28k^{2\theta-1}+\frac{k^\theta}{L^2}
   =o(k^\theta/L).
   \]

3. **Medium-large:** \(k^2/L^2<n\le\tfrac12k^{2+\theta}\).  Take \(r=2\) and
   \(\lambda=\sqrt{k^{2+\theta}/(2n)}\,L\).  Then \(\lambda\ge L\ge1\), and the four normalized contributions are
   \[
   k^{(\theta-1)/3}L^{2/3},\quad L^{-2},\quad
   O(k^{(\theta-2)/8}L^{1/2}),\quad
   O(k^{\theta/2}L^2)/k^\theta,
   \]
   each \(o(L^{-1})\) after interpreting the last term as the additive contribution divided by \(k^\theta\).

4. **Large:** \(\tfrac12k^{2+\theta}<n\le\exp(cL^2/M)\), handled by (6)--(12).

In ranges 2--4 the far-prime argument returns a prime already in \((k,k+k^\theta)\); range 1 returns one in \((k,k+3k^\theta)\).  A prime \(p\) with the required distance property has \(n\bmod p\in[k^\theta,p-k^\theta]\subset[1,k]\), hence divides one factor of \((n-k)\cdots(n-1)\).  All inequalities are for integer \(n\), and the shared endpoints above are assigned to one adjacent range, so no integer \(n\) is omitted.

The quantifier is pointwise in \(\theta\): for every fixed \(\theta\in(2/5,3/5)\) and fixed \(c<c_*(\theta)\), there is a sufficiently-large-\(k\) threshold.  Nothing here asserts uniformity as \(\theta\) approaches either endpoint, and the frozen task expressly excludes \(\theta=2/5,3/5\) and all exterior values.

## No-go above the frontier

Take the worst allowed integer
\[
n_k=\left\lfloor\exp(cL^2/M)\right\rfloor.
\]
It lies in the large range for all sufficiently large \(k\).  For any admissible \(r\) and \(\lambda\ge1\), if \(A\le L^{-1}\), then \(\lambda\ge1\), \(r!\ge1\), and the definition of \(A\) imply
\[
r\ge
\frac{\log n_k-L-M}{L-2M}
=c\frac{L}{M}+O(1). \tag{13}
\]
If \(A>L^{-1}\), the desired \(o(L^{-1})\) estimate has already failed.  Otherwise (1), (2), and (13) give
\[
\max(A,B)
\ge L^{-(1-\theta)/(3c)+o(1)}. \tag{14}
\]
For \(c>(1-\theta)/3\), the right side is \(\gg L^{-1}\), and in fact the ratio of the nonnegative Theorem-4.1 right side to \(k^\theta/L\) diverges.  Neither the third term nor the additive term can cancel it.

At equality, the sharper form of (13) and (3) give
\[
\inf_{r,\lambda}\,L(A+B)\longrightarrow d_\infty.
\]
This proves the endpoint constant statement in the verdict, but not a blanket endpoint impossibility independent of the prime-count constant.

Finite or polylogarithmic segmentation does not change this obstruction.  In the underlying `konyagin_thm`, a block of length \(N_j\) has outer factor \(N_j\), while the inner first-two-term invariant is still (1), up to \(1+o(1)\) for bases \(k+O(k^\theta)\).  Summing nonnegative blockwise upper bounds over comparable blocks replaces \(k^\theta\) by \(\sum_jN_j\asymp k^\theta\); it cannot reduce (14).  This remains true even if one grants an ideal prime distribution among subblocks, which is stronger than the frozen prime input.  Repeating or overlapping blocks only increases the summed nonnegative certificate.

The no-go is solely about this upper-bound/comparison certificate class.  It is not a lower bound for the true bad-point count and is not an impossibility theorem for Erdős #451 or for a different analytic mechanism.

## Unconditional specialization

The source paper packages Baker--Harman--Pintz as the required prime input at
\(\theta=21/40\).  Therefore
\[
c_*\!\left(\frac{21}{40}\right)
=\frac{1-21/40}{3}=\frac{19}{120}.
\]
For every fixed \(0<c<19/120\), all sufficiently large \(k\), and every integer
\(2k<n\le\exp(cL^2/M)\), the product has a prime divisor
\(p\in(k,k+3k^{21/40})\).  Since \(21/40<1\), eventually
\(3k^{21/40}<k\), and hence the same prime lies in \((k,2k)\).

## First-stage audit result

Blind reconstruction result: **PASS**, with the endpoint qualification above.  The candidate supremum, its positive open range, the strict supercritical no-go, all four \(n\)-ranges, the fixed-\(\theta\) quantifier, output interval, arbitrary-\(\lambda\) optimization, third term, additive term, minimal \(r\), segmentation robustness, and \(r\)-uniform Theorem-4.1 constant have all been independently reconstructed.  The remaining formal-evidence limitation is that the full upstream Lean file was source-audited but not locally kernel-replayed under its exact Lean 4.28.0 environment.

## Second stage: comparison with author evidence

Only after completing and saving every section above, I opened the author files
`evidence/parametric_frontier_proof.md`, `evidence/frontier_falsification.md`,
`evidence/theorem41_uniformity_audit.md`, `evidence/frontier_algebra_replay.json`,
and `audit/adversarial_self_audit.md`.

### Item-by-item comparison

| Audit item | Blind reconstruction | Author evidence | Comparison |
|---|---|---|---|
| Frontier | \((1-\theta)/3\) | \((1-\theta)/3\) | Match |
| Minimal order | \(r=cL/M+O(1)\) at the worst \(n\), and \(r\le(c+\varepsilon+o(1))L/M\) uniformly | Same upper bound; identifies the inherited factor-two loss | Match |
| Arbitrary \(\lambda\) | Exact invariant (1), exact weighted optimizer (3) | Same invariant; notes weighted optimizer has the same exponent | Match |
| Third term | \(L^{-1/(2c)+o(1)}\) at the active scale; inactive before \(c=1/2\) | Same, with a slightly coarser but valid uniform split | Match |
| Additive term | Worst at \(r=3\), exponent \((9-2\theta)/21<\theta\) for \(\theta>9/23\) | Same derivative and range check | Match |
| Lower \(n\)-ranges | Independently replayed Sections 2, 3, and 5, including the shifted small-range prime interval | Imported unchanged by the author proof | Match; blind audit supplies the omitted dependency replay |
| \(\theta\) and \(n\) quantifiers | Fixed \(\theta\in(2/5,3/5)\), fixed strict \(c<c_*\), every integer \(n\) in the full range | Same | Match |
| Prime output | First \((k,k+3k^\theta)\), then \((k,2k)\) for large \(k\) | Same | Match |
| Uniform Theorem 4.1 constant | Fixed upstream `c₆`, independent of \(r\), with error `2*r*lam` | Same raw SHA-256 and source locations | Match |
| Supercritical no-go | All \(c>c_*\) fail even under arbitrary \(\lambda\) and nonnegative comparable block sums | Same | Match |
| Equality endpoint | No little-o certificate at \(c=c_*\); exact comparison is a constant competition | Theorem B is explicitly restricted to *little-o certificates* and excludes equality in that class | Match on the claimed class |
| \(\theta=21/40\) | Every fixed \(c<19/120\), conditional only on the source's BHP input, then \(p<2k\) | Same | Match |

There is no mathematical mismatch in the theorem actually claimed by the
author artifacts.  Two qualifications should remain visible:

1. The equality endpoint is a no-go only for the author's explicitly defined
   **little-o** certificate.  It is not an exact-constant impossibility: with
   the explicit formal constant, an endpoint comparison could succeed if the
   available prime lower constant exceeded
   \(c_6(2^{1/3}+2^{-2/3})\).  The author theorem does not claim otherwise, but
   its shorter self-audit does not spell out this constant-level possibility.
2. The upstream Lean source and hash verify that no \(r\)-dependent constant is
   hidden in the formal statement, but neither the author nor this reviewer
   locally kernel-replayed the full file in its requested Lean 4.28.0
   environment.  This limits the *machine-reproduced* evidence classification;
   it does not leave a mathematical dependency gap in the independently
   reconstructed natural proof.

The author's guarded finite replay was independently rerun with
`/home/biostar/work/projects/openmath/bin/openmath-memory-guard -- python3
amra-research-loop/campaigns/erdos-451-parametric-frontier-20260826/work/verify_frontier.py`.
It passed under unit `openmath-task-20260826-144906-115238.scope`.  A separate
guarded hash replay under unit `openmath-task-20260826-144856-115122.scope`
matched every hash recorded in `frontier_algebra_replay.json`.  These checks
remain finite/exact-algebra support; the universal result rests on the natural
proof above.

### Final gate classifications

* `independent_reconstruction`: **passed**.
* `statement_match`: **passed**, including all parameter ranges, strict
  endpoint semantics, compound attaining/no-go claims, and the output interval.
* `dependency_check`: **passed** for the conditional theorem and its stated BHP
  specialization.  `PI(theta)` remains an explicit hypothesis rather than a
  secretly discharged input; Theorem 4.1 is uniform in growing \(r\).
* `novelty_check`: **priority_uncertain**.  No primary-literature priority
  search was performed, so this audit makes no novelty or publication-priority
  claim.

Overall independent-audit result: **PASS**.  This result satisfies the current
audit gate but does not itself authorize promotion, publication, or a priority
claim.

The repository's full phase validator was then run under OpenMath guard unit
`openmath-task-20260826-145046-115998.scope`.  It reported no reconstruction,
statement, dependency, or novelty error, but returned `valid: false` because
`decision.json` is intentionally still `undecided`: it requested a promotion
outcome, a frozen success condition, a reason, and evidence.  Those four
decision errors are outside this independent-auditor task.  In accordance with
the instruction not to promote early, neither `decision.json` nor the campaign
phase was changed.
