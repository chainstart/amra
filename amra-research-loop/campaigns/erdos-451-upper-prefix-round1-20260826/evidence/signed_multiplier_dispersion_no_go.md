# Signed multiplier dispersion: exact endpoint identities and an affordable uniform-damping no-go

## Status and scope

This note tests one concrete continuation of the full-modulus
high-conductor endpoint isolated in
violation_generating_polynomial_dual_no_go.md: multiply the product variable
by an affordable signed family of units and try to damp every unresolved
character while retaining the canonical \(Q_0\) phase.

The exact shifted-endpoint and divisor-multiplier identities are useful.
They give a precise sufficient closure lemma with principal normalization,
\(\ell^1\) cost, and candidate-value budget.  The universal version of the
amplifier is nevertheless refuted.  An affordable multiplier cannot give
exponential pointwise damping on all high conductors: a sparse multiplier
has a high-support quadratic annihilator even after the \(Q_0\) phase is
included, and every subexponential-support multiplier retains
subexponential-size Fourier mass on exact full-support characters by an
exact Parseval/diagonal argument.  Stable inversion pays back any uniform
damping.

These are method no-go theorems.  They do not lower-bound the actual
coefficient-weighted signed endpoint sum, because the interval coefficient
of an individual undamped character may vanish or be small and different
characters may cancel.  No Erdos-451 upper bound is proved.  The campaign
remains in survivor_deepening and closes remains empty.

## 1. Endpoint notation

Retain

\[
 A=\lfloor k/\log^2k\rfloor,\qquad
 Q_0={k+A\choose A},\qquad
 {\cal P}=\{p:k+A<p<2k\},\qquad
 P=\prod_{p\in{\cal P}}p,
\]

and let \(m=|{\cal P}|\).  Put \(d_p=p-k-1\),
\(\delta_p=d_p/(p-1)\), and

\[
 \delta=\prod_{p\in{\cal P}}\delta_p.
\]

Fix

\[
 X=\left\lfloor\exp(\gamma k/\log k)\right\rfloor,
 \qquad Y=X^{4/3-\eta},\qquad
 \gamma>0,\quad0<\eta<4/3.                        \tag{1}
\]

Write

\[
 S_X^P(\chi)=\sum_{\substack{n\leq X\\(n,P)=1}}\chi(n),
 \qquad
 N=M_X^2,\qquad
 M_X=\#\{n\leq X:(n,P)=1\}.
\]

The exact endpoint coefficient is

\[
 c_\chi={1\over\varphi(P)}\chi(-Q_0)
 \prod_{p\in{\cal P}}
 \left(\sum_{j=1}^{d_p}\overline{\chi_p(j)}\right),             \tag{2}
\]

where the inner sum is \(d_p\) at a principal local component.  If
\({\bf F}\) is the indicator of the simultaneous allowed unit residues,
then

\[
 {\bf F}(y)=\sum_{\chi\bmod P}c_\chi\chi(y),\qquad
 \sum_{\substack{u,t\leq X\\(ut,P)=1}}{\bf F}(ut)
 =\sum_{\chi\bmod P}c_\chi S_X^P(\chi)^2.          \tag{3}
\]

The square in (3) is a complex square, not an absolute square.  The
principal term is \(\delta N\), the aggregate with
\(1<f_\chi\leq Y\) is already \(o(\delta N)\), and the unresolved part is
the single signed sum over \(f_\chi>Y\).

## 2. Exact shifted-multiplier identity

Let \(a=(a_g)\) be finitely supported real weights on positive integers
\(g\) satisfying \((g,P)=1\).  Put

\[
 G=\max\{g:a_g\neq0\},\qquad
 \sigma=\sum_ga_g,\qquad
 L=\sum_g|a_g|,\qquad
 {\cal A}_a(\chi)=\sum_ga_g\chi(g).                \tag{4}
\]

For one multiplier define the physical shifted endpoint count

\[
 C_X(g)=
 \sum_{\substack{u,t\leq X\\(ut,P)=1}}{\bf F}(gut).              \tag{5}
\]

Fourier inversion gives the exact identity

\[
 C_X(g)=\sum_{\chi\bmod P}
 c_\chi\chi(g)S_X^P(\chi)^2.                       \tag{6}
\]

Therefore the signed amplified count

\[
 Z_a=\sum_ga_gC_X(g)
\]

has the exact spectral form

\[
\boxed{\quad
 Z_a=\sum_{\chi\bmod P}
 c_\chi{\cal A}_a(\chi)S_X^P(\chi)^2.
 \quad}                                            \tag{7}
\]

No support, conductor, phase, or sign has been separated in (7).  In
particular,

\[
 \chi(-Q_0){\cal A}_a(\chi)
 =\sum_ga_g\chi(-Q_0g),                            \tag{8}
\]

so the absorber phase remains coupled to the multiplier.

If \(\sigma=1\), the principal contribution to (7) is exactly
\(\delta N\).  Let

\[
\begin{aligned}
 {\cal L}_a&=\sum_{\substack{\chi\neq{\bf1}\\f_\chi\leq Y}}
 c_\chi{\cal A}_a(\chi)S_X^P(\chi)^2,\\
 {\cal H}_a&=\sum_{\substack{\chi\bmod P\\f_\chi>Y}}
 c_\chi{\cal A}_a(\chi)S_X^P(\chi)^2 .
\end{aligned}                                      \tag{9}
\]

Then

\[
 Z_a=\delta N+{\cal L}_a+{\cal H}_a.               \tag{10}
\]

The already proved low-conductor theorem and
\(|{\cal A}_a(\chi)|\leq L\) give

\[
 |{\cal L}_a|
 \leq L\sum_{\substack{\chi\neq{\bf1}\\f_\chi\leq Y}}
 |c_\chi|\,|S_X^P(\chi)|^2.                        \tag{11}
\]

The proof of that theorem has relative saving
\(\exp(-(3\eta/2)\log X+o(\log X))\).  Hence the sufficient affordable
condition

\[
 \log L=o(\log X)=o(k)                             \tag{12}
\]

makes \({\cal L}_a=o(\delta N)\).
Here \(M_X=(1-o(1))X\): indeed, removing the primes in
\({\cal P}\) costs at most \(X\sum_{p\in{cal P}}1/p+O(m)\), and
\(\sum_{k<p<2k}1/p=o(1)\).  Thus the old theorem's normalization
\(o(\delta X^2)\) is equivalent to the one used here.

## 3. Exact conditional closure lemma

The preceding identity gives a genuine shifted-endpoint closure statement,
not a restatement of the unweighted endpoint estimate.

> **Conditional signed shifted-endpoint lemma.**  Suppose there are real
> unit-supported weights \(a_g=a_g(k)\) such that
> \[
> \sum_ga_g=1,\qquad
> \log L=o(k/\log k),\qquad
> \log G=o(k),                                     \tag{13}
> \]
> and, as one signed sum,
> \[
> |{\cal H}_a|=o(\delta N).                        \tag{14}
> \]
> Then for all sufficiently large \(k\) there is a valid 451 integer
> \[
> 2k<n\leq Q_0GX^2=\exp(o(k)).                     \tag{15}
> \]
> If instead \(\log G=O(k/\log k)\), the right side in (15) is
> \(\exp(O(k/\log k))\).

**Derivation.**  Condition (12) follows from (13), so (10), (11), and
(14) give \(Z_a=\delta N+o(\delta N)>0\).  If every physical count
\(C_X(g)\) with \(a_g\neq0\) vanished, then \(Z_a\) would vanish.  Hence
some such \(g\) has an allowed pair \(u,t\), and
\(n=Q_0gut\) is a valid candidate.  It is at most \(Q_0GX^2\); the
absorbed primes divide \(Q_0\), all remaining primes are handled by
\({\bf F}(gut)=1\), and \(Q_0>2k\) eventually.  Finally
\(\log Q_0=o(k/\log k)\), proving (15). \(\square\)

The lemma is conditional because (14) is open.  Its role is to fix the
normalization and all costs that a multiplier construction must meet.
Negative weights are allowed: positivity of \(Z_a\), rather than
positivity of every weight, still implies that at least one physical
shifted count is nonzero.

## 4. Prefix-preserving divisor multiplier

The suggested truncated transform also has an exact physical meaning.
Extend \(a_g\) by zero outside its finite support and define

\[
 T_{a,X}(\chi)=\sum_{g\leq X}a_g\chi(g)S_{X/g}^P(\chi),\qquad
 w_a(n)=\sum_{g\mid n}a_g.                         \tag{16}
\]

Regrouping \(n=gh\) gives

\[
\boxed{\quad
 T_{a,X}(\chi)=
 \sum_{\substack{n\leq X\\(n,P)=1}}w_a(n)\chi(n).
 \quad}                                            \tag{17}
\]

Consequently

\[
 \sum_{\chi\bmod P}c_\chi
 T_{a,X}(\chi)S_X^P(\chi)
 =
 \sum_{\substack{u,t\leq X\\(ut,P)=1}}
 w_a(u){\bf F}(ut).                               \tag{18}
\]

This version pays no \(G\) in the candidate value.  Its principal
normalization is

\[
 \delta M_XW_{a,X},\qquad
 W_{a,X}=\sum_{\substack{u\leq X\\(u,P)=1}}w_a(u)
 =\sum_{g\leq X}a_gM_{X/g}.                       \tag{19}
\]

Thus a useful truncated closure theorem must prove \(W_{a,X}>0\), keep the
mixed high-conductor sum in (18) below
\(\delta M_XW_{a,X}\), and provide a low-conductor theorem uniform in all
lengths \(X/g\).  The existing low-conductor result for
\(S_X^P(\chi)^2\) does not automatically supply that mixed-length
uniformity.

There is an exact inverse-filter audit.  If \(a_1\neq0\), let \(b\) be the
Dirichlet-convolution inverse of \(a\).  Then for every character
\(\chi\bmod P\),

\[
\boxed{\quad
 S_X^P(\chi)=
 \sum_{d\leq X}b_d\chi(d)T_{a,X/d}(\chi).
 \quad}                                            \tag{20}
\]

Indeed, after expansion the coefficient of
\(\chi(h)S_{X/h}^P(\chi)\) is
\(\sum_{dg=h}b_da_g=(b*a)(h)\), which is one at \(h=1\) and zero
otherwise.  Any recovery of the original endpoint through (20) must pay
the boundary/inverse norm

\[
 B_X=\sum_{d\leq X}|b_d|                           \tag{21}
\]

once for each recovered interval factor.  A claim that smoothing is free
without bounding \(B_X\) is incomplete.

## 5. Sparse quadratic annihilator, including \(Q_0\)

First suppose the multiplier has \(s\) distinct support values
\(g_1,\ldots,g_s\).  For each subset
\(\varepsilon\in{\mathbb F}_2^m\), define the quadratic character

\[
 \chi_\varepsilon(n)=
 \prod_{\substack{p\in{\cal P}\\\varepsilon_p=1}}
 \left({n\over p}\right).                         \tag{22}
\]

Impose the \(s+1\) linear conditions

\[
 \chi_\varepsilon(g_i)=1\quad(1\leq i\leq s),
 \qquad \chi_\varepsilon(-Q_0)=1.                 \tag{23}
\]

Their kernel has dimension at least \(m-s-1\).  If that dimension is
\(d>0\), its active coordinate set has at least \(d\) elements.  A uniform
kernel vector has average Hamming weight half the active-coordinate count,
so some vector in the kernel has weight at least \(d/2\).  Its conductor
satisfies

\[
 f_{\chi_\varepsilon}\geq k^{d/2}.                \tag{24}
\]

In particular, if \(s=o(m)\), then

\[
 \log f_{\chi_\varepsilon}\geq(1/2-o(1))k
 \gg\log Y.                                       \tag{25}
\]

For this high-conductor character,

\[
 {\cal A}_a(\chi_\varepsilon)=\sum_ga_g=1,\qquad
 \chi_\varepsilon(-Q_0)=1.                        \tag{26}
\]

Thus neither the multiplier nor the absorber phase gives any damping on
that character.

This is a strict no-go for a sparse generator-only claim of uniform
damping on every high conductor.  It is not a lower bound for
\({\cal H}_a\): the corresponding interval coefficient in (2) may be
zero or small, and one undamped character does not control the signed
aggregate.

## 6. Exact full-support multiplier energy

The sparse restriction is not needed for an energy obstruction.  Aggregate
equal residue classes and suppose the multiplier is represented by
distinct positive units \(g\leq G\).  Orthogonality over characters that
are nonprincipal at every remaining prime gives

\[
 \sum_{\operatorname{supp}\chi={\cal P}}
 |{\cal A}_a(\chi)|^2
 =
 \sum_{g,h}a_g\overline{a_h}
 \prod_{p\in{\cal P}}
 \begin{cases}
 p-2,&g\equiv h\pmod p,\\
 -1,&g\not\equiv h\pmod p.
 \end{cases}                                      \tag{27}
\]

Assume

\[
 \sum_ga_g=1,\qquad
 S=|\operatorname{supp}a|=\exp(o(k)),\qquad
 L=\exp(o(k)),\qquad G=\exp(o(k)).                 \tag{28}
\]

For large \(k\), \(G<P\).  The diagonal of (27) is at least

\[
 {1\over S}\prod_{p\in{\cal P}}(p-2)
 =\exp((1+o(1))k),                                \tag{29}
\]

because Cauchy--Schwarz gives
\(\sum_g|a_g|^2\geq1/S\).  If \(g\neq h\), the magnitude of the local
product in (27) is at most

\[
 \prod_{\substack{p\in{\cal P}\\p\mid g-h}}p
 \leq|g-h|\leq G.                                 \tag{30}
\]

All off-diagonal terms together therefore have magnitude at most
\(L^2G=\exp(o(k))\), which is negligible compared with (29).  Hence

\[
\boxed{\quad
 \sum_{\operatorname{supp}\chi={\cal P}}
 |{\cal A}_a(\chi)|^2
 \geq(1-o(1)){1\over S}
       \prod_{p\in{\cal P}}(p-2).
 \quad}                                            \tag{31}
\]

There are exactly \(\prod_p(p-2)\) full-support characters.  It follows
that the mean-square multiplier size on this whole slice is at least
\((1-o(1))/S\), and in particular at least one character satisfies

\[
 |{\cal A}_a(\chi)|\geq(1-o(1))S^{-1/2}
 =\exp(-o(k)).                                     \tag{32}
\]

Every such character has conductor \(P>Y\).  Therefore no multiplier
satisfying (28) can provide \(\exp(-c k)\) pointwise damping on every
unresolved character for any fixed \(c>0\).

Equation (31) concerns multiplier energy, not the weighted energy
\(\sum|c_\chi{\cal A}_a(\chi)|^2\), and still less the signed sum
\({\cal H}_a\).  It rigorously kills the proposed universal damping
handoff, but not coefficient-aware \(Q_0\)-phase cancellation.

## 7. General Parseval and the Burgess barrier

For completeness, on the full unit group
\(\Gamma=({\mathbb Z}/P{\mathbb Z})^\times\), Parseval gives

\[
 \sum_{\chi\in\widehat\Gamma}|{\cal A}_a(\chi)|^2
 =\varphi(P)\sum_{x\in\Gamma}|a(x)|^2.             \tag{33}
\]

The number of characters with \(f_\chi\leq Y\) is \(\exp(o(k))\): their
support rank is at most \(\log Y/\log k=O(k/\log^2k)\), the number of such
supports is \(\exp(o(k/\log k))\), and each support contributes at most
\(Y\) characters.  Under (28), the low-conductor contribution to (33) is
at most \(\exp(o(k))\), whereas the total is at least
\(\varphi(P)/S=\exp((1+o(1))k)\).  Thus almost all multiplier \(L^2\)
energy remains in the high-conductor region.

For the unit-supported positive interval multiplier

\[
 a_g={\bf1}_{g\leq G,(g,P)=1}/M_G,
 \qquad M_G=\#\{g\leq G:(g,P)=1\},
\]

the spectral factor is the normalized unit-sieved short character sum

\[
 {\cal A}_a(\chi)={1\over M_G}\sum_{g\leq G}\chi(g). \tag{34}
\]

Here the usual extension of a Dirichlet character by zero on nonunits makes
the numerator the classical short character sum, and in the long ranges
relevant below \(M_G=(1-o(1))G\).  The classical Burgess range becomes
nontrivial only when
\(G\geq f_\chi^{1/4+\epsilon}\), up to the standard refinement of the
least-nonresidue exponent.  At the full conductor
\(f_\chi=P=\exp((1+o(1))k)\), this requires
\(\log G\geq(1/4+o(1))k\), which is incompatible with the
\(\log G=o(k)\) endpoint budget in (13).  This analytic barrier is
consistent with, but weaker than, the exact energy obstruction (31).

## 8. Why \(Q_0\) does not repair universal damping

Equation (8) shows that multiplication by the absorber phase simply
translates the multiplier measure from \(g\) to \(-Q_0g\) on the unit
group.  Translation preserves support cardinality, \(\ell^1\) and
\(\ell^2\) norms, Parseval energy, and invertibility.  The sparse
annihilator theorem already included \(-Q_0\) as an additional linear
constraint, at the cost of only one dimension.

For a group-convolution filter \(a\), suppose a recovery filter \(b\)
satisfies

\[
 a*b=\delta_1.
\]

Its Fourier transform obeys

\[
 {\cal A}_a(\chi){\cal A}_b(\chi)=1.               \tag{35}
\]

Consequently

\[
 \|b\|_1\geq|{\cal A}_b(\chi)|
 ={1\over|{\cal A}_a(\chi)|}.                     \tag{36}
\]

Any exponential uniform damping that could repair the old
\(\exp((1/2+o(1))k)\) separated full-support ledger forces an exponential
inverse-filter cost, violating the affordable \(\ell^1\) budget.  If the
amplifier has a spectral zero, exact recovery is impossible.

Again, (36) does not address a direct shifted-endpoint proof using (10),
because that proof need not invert the filter.  It does show that smoothing
cannot both erase the high spectrum and recover the original endpoint at
subexponential cost.

## 9. Decision for this mechanism

The following concrete mechanism is refuted:

> Choose an affordable signed multiplier of subexponential value, support,
> and \(\ell^1\) cost; obtain exponential pointwise damping on every
> \(f_\chi>Y\); then close the endpoint by triangle, separated energy, or a
> stable inverse filter.

Sparse support has an exact high-conductor annihilator with trivial
\(Q_0\) phase.  Arbitrary subexponential support has exact full-support
energy at least the scale (31).  Stable inversion repays any uniform
damping.  These statements remain true before any coefficient vector is
separated.

The only multiplier escape is a direct proof of the single
coefficient-aware signed correlation (14), or its prefix-preserving mixed
form (18), using cancellation between
\(c_\chi\), \({\cal A}_a(\chi)\), and \(S_X^P(\chi)^2\).  The \(Q_0\)
translation alone supplies no estimate of that correlation.  Because this
escape is not demonstrably simpler than the original high-conductor endpoint
sum, the multiplier/dispersion mechanism should be frozen rather than
retained as a new survivor.  Further allocation is better directed to the
remaining orthant/anchored-CRT gap mechanisms, unless a genuinely
coefficient-weighted shifted-endpoint theorem is supplied.

## 10. Evidence classification

Unconditional exact results:

1. the shifted physical/spectral identities (5)-(10);
2. the prefix-preserving divisor identity (16)-(20);
3. the sparse \(Q_0\)-aware quadratic annihilator (22)-(26);
4. the exact full-support energy lower bound (27)-(32);
5. the group Parseval and inverse-filter bounds (33), (35), and (36).

Conditional:

1. the endpoint implication (13)-(15);
2. any coefficient-aware estimate (14) or mixed-length estimate (18).

Background analytic limitation:

1. the Burgess threshold comparison following (34).

No finite experiment was used, so there is no guarded computation record.
The public problem, main exponent, and main term are unchanged.
