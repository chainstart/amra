# Independent audit of growing-promotion uniformity

Auditor: Erdős #1083 lane (not an author of the #776 derivation)
Date: 2026-08-02
Verdict on the displayed relaxed-comparator lemma: **PASS**
Campaign-promotion verdict: **BLOCKED — the actual seed/rank-capacity bridge is absent**

## Reconstruction boundary

I reconstructed the argument from the exact coordinates

\[
n={q\choose2}+r,\qquad n+b-1={q+c\choose2}+u,
\]

the canonical-shadow definition of \(U_j\), and the previously audited fixed-\(c\)
results. I did not import either author probe. The independent executable implements
the greedy Macaulay expansion directly.

This audit certifies only the relaxed no-borrow statement in
`decisive_lemma.json`. It does not certify an antichain construction for the public
problem.

## 1. Exact coordinate reconstruction

Subtracting the triangular coordinates gives

\[
b=cq+{c\choose2}+u-r+1.
\]

With

\[
z={q\choose3}+{r\choose2},\quad
w={q+c\choose3}+{u\choose2},\quad H={b\choose2}+1,
\]

the definitions give

\[
x=n+z-H+1,\qquad y=n+w-H,
\]

and hence, without an asymptotic step,

\[
y-x=w-z-1=:\Delta,\qquad x+(H-n)=z+1.
\]

Therefore the claimed cancellation

\[
\gamma_4=U_3(y)-U_3(x)-z-1
\]

is exact. The independent guard checked both equalities on 585,588 admissible
negative-\(\gamma_3\) rows.

## 2. The uniform \(U_3\) asymptotic and subtraction error

Write uniquely

\[
N={a\choose3}+R,\qquad 0\le R<{a\choose2}.
\]

Then

\[
U_3(N)={a\choose4}+U_2(R).
\]

The remainder interval is exactly the gap between consecutive rank-three
leading blocks, so \(a=(6N)^{1/3}+O(1)\). Monotonicity gives
\(0\le U_2(R)\le {a\choose3}=O(N)\). Expanding the leading binomial therefore
gives, with one absolute implied constant,

\[
U_3(N)=\frac{6^{4/3}}{24}N^{4/3}+O(N).
\]

When this formula is applied separately at \(x+\Delta\) and \(x\), the error
is the sum of two absolute errors, not their difference. In the small
\(c/\sqrt q\) branch both arguments are \(O(q^3)\), so the subtraction error
is indeed \(O(q^3)\). The main difference is

\[
\frac{6^{4/3}}{24}\big((x+\Delta)^{4/3}-x^{4/3}\big)
=\frac q3\Delta(1+o(1))
=\frac{cq^3}{6}(1+o(1)).
\]

Because this branch assumes \(c\to\infty\), the ratio of the absolute error
to the main term is \(O(1/c)=o(1)\). Thus the author did not illegally
cancel two \(O(N)\) terms.

## 3. Promotion-scale and displacement estimates

No-borrow admissibility gives

\[
{b\choose2}+1\le n+z+1=O(q^3).
\]

The remainder ranges give

\[
b\ge(c-1)q,
\]

so \(c=O(\sqrt q)\). This implication remains valid even before assuming
\(c=o(q)\); it then supplies \(c/q\to0\).

Expanding \(\Delta\), the terms omitted from \(cq^2/2\) have sizes
\(O(c^2q+c^3+q^2)\). Relative to \(cq^2\), these are
\(O(c/q+c^2/q^2+1/c)=o(1)\) along every \(c\to\infty\) admissible sequence.
Consequently

\[
\Delta=\frac{cq^2}{2}(1+o(1))>0.
\]

The independent exact samples reproduce convergence of
\(2\Delta/(cq^2)\) to one in both slow-growing and positive
\(\sqrt q\)-scale regimes.

## 4. The two subsequence branches

The bound \(c=O(\sqrt q)\) makes \(c/\sqrt q\) bounded. Every bad sequence
therefore has a subsequence on which this ratio converges.

If its limit is positive, superadditivity gives

\[
\gamma_4\ge U_3(\Delta)-z-1.
\]

Here

\[
\frac{U_3(\Delta)}{q^3}\asymp
\frac{c^{4/3}}{q^{1/3}}\to\infty,
\qquad \frac z{q^3}\to\frac16,
\]

so positivity follows.

If the limit is zero, \(b=cq(1+o(1))\) and
\({b\choose2}=o(q^3)\), whence

\[
x=\frac{q^3}{6}(1+o(1)),\qquad \Delta/x\to0.
\]

The subtraction calculation in Section 2 then yields

\[
U_3(x+\Delta)-U_3(x)
=\frac{cq^3}{6}(1+o(1))+O(q^3).
\]

After subtracting \(z+1=q^3/6+O(q^2)\), positivity again follows because
\(c\to\infty\). These alternatives cover every convergent-ratio
subsequence, so an infinite nonpositive growing-\(c\) sequence cannot
exist.

## 5. Uniform-\(Q\) quantifiers

The negation of one uniform threshold produces bad admissible states with
\(q_i\ge i\). If \((c_i)\) is bounded, an integer constant subsequence
contradicts the already audited theorem

\[
\forall c\ge2\;\exists Q_c\;\forall q\ge Q_c.
\]

If \((c_i)\) is unbounded, a subsequence satisfies \(c_i\to\infty\) and
contradicts the growing-\(c\) lemma. This proves

\[
\exists Q\;\forall q\ge Q\;\forall c\ge2
\]

for admissible relaxed no-borrow states. Non-effectivity of \(Q\) does not
invalidate the existential claim.

## 6. Evidence and decision

The independent bounded guard ran under 1 GiB and 300 seconds and found no
nonpositive \(\gamma_4\) among 585,588 retained rows. This is only a finite
consistency check; the unbounded result rests on the reconstruction above.

The decisive lemma passes exactly as a relaxed-comparator theorem. It does
not meet the campaign's frozen `global_interface_closed` success condition:
no borrow-aware Hall/capacity theorem transfers this positivity to an actual
seed occupying the required Boolean-lattice ranks. Promotion must therefore
remain blocked even though independent reconstruction of the lemma passes.

Novelty relative to external literature was not checked; priority remains
uncertain.
