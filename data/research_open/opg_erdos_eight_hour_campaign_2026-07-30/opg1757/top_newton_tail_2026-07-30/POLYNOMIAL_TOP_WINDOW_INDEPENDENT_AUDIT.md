# Independent audit of the polynomial top-window theorem

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

The pair lower bound, star-graph upper bound, profile estimate,
conversion to \(A^j j^{Aj}\), and choice of an absolute \(\eta\) are
valid.

The first audited version had one strict error in its proof of
Lemma 2.  Its then-printed equations (7)--(8) gave the combined
exponential cost
\[
\frac{4d^2+8d}{n}.
\]
That version claimed this was at most \(6d^2/n\) for \(d\ge2\).
That assertion fails at
\[
\boxed{
d=2:\ 32>24,\qquad
d=3:\ 60>54.
}
\]
These are counterexamples to the displayed constant ledger, not to
the stated \(4\)-Stirling ratio.

The revised manuscript now implements the required repair: it handles
\(j=0\) by the exact ratio \(1\), and for \(j\ge1\) retains the
\(j\)-dependence in the numerator estimate.  Its exponential cost is
\[
\frac{2(d-j)(4-j)_+}{n}
\]
rather than \(8d/n\).  This yields
\[
4d^2+2(d-j)(4-j)_+\le6d^2
\]
for every \(d\ge1\) and \(1\le j\le d\).  The revision explicitly
checks \(d=2,j=1\) and covers \(d\ge3\) by
\(2(d-j)(4-j)_+\le6d\le2d^2\).

Every step in the current revision is rigorous, so the
polynomial-width conclusion passes.

## 1. Pair lower bound

The coefficient
\[
T_{n,d}={n\brace n-d}_4
\]
counts partitions of \(n+4\) elements into \(n-d+4\) blocks, with the
four distinguished elements in different blocks.

Select \(2d\) of the \(n\) ordinary elements, partition them into
\(d\) unordered pairs, and leave all remaining elements singleton.
Every such partition is admissible and distinct.  Their number is
\[
\frac{(n)_{\underline{2d}}}{2^dd!}.
\]
Therefore
\[
\boxed{
T_{n,d}\ge
\frac{(n)_{\underline{2d}}}{2^dd!}.
}
\]
No distinguished element or symmetry factor is missing.

## 2. Star-graph upper bound

Take an admissible partition of \(N=n-j+4\) elements with block
deficit \(r=d-j\).  In every nonsingleton block, join its least
element to all other elements of that block.  A block of size \(q\)
contributes \(q-1\) edges, so the total edge count is exactly \(r\).

The resulting graph is a disjoint union of stars.  Its connected
components recover the original blocks, making the construction
injective.  Forgetting both the star-forest restriction and the
distinguished-element restriction gives
\[
T_{n-j,d-j}
\le
\binom{\binom{n-j+4}{2}}{d-j}.
\]
Using
\[
\binom Mr\le\frac{M^r}{r!},
\qquad
\binom{N}{2}\le\frac{N^2}{2},
\]
gives
\[
\boxed{
T_{n-j,d-j}
\le
\frac{(n-j+4)^{2(d-j)}}
{2^{d-j}(d-j)!}.
}
\]

Dividing this by the pair lower bound yields exactly
\[
\frac{T_{n-j,d-j}}{T_{n,d}}
\le
2^j(d)_{\underline j}
\frac{(n-j+4)^{2(d-j)}}
{(n)_{\underline{2d}}}.
\tag{A}
\]

## 3. Denominator estimate

Under \(d\le n/4\), every \(0\le r\le2d-1\) satisfies \(r/n\le1/2\).
Thus
\[
\log(1-r/n)\ge-2r/n,
\]
and
\[
\begin{aligned}
(n)_{\underline{2d}}
&=n^{2d}\prod_{r=0}^{2d-1}(1-r/n)\\
&\ge
n^{2d}
\exp\!\left(
-\frac2n\sum_{r=0}^{2d-1}r
\right)\\
&=
n^{2d}
\exp\!\left(
-\frac{2d(2d-1)}n
\right)\\
&\ge
n^{2d}\exp(-4d^2/n).
\end{aligned}
\tag{B}
\]
The constant \(4\) is correct.

## 4. Audit history and verification of the repaired numerator estimate

The first version replaced the numerator by the \(j\)-independent bound
\[
(n-j+4)^{2(d-j)}
\le
n^{2(d-j)}e^{8d/n}.
\]
Although this inequality is valid, combining it with (B) gives
\[
e^{(4d^2+8d)/n}.
\]
The inference
\[
4d^2+8d\le6d^2\qquad(d\ge2)
\]
is false precisely for \(d=2,3\).  Declaring only \(d=0,1\)
“immediate” does not cover these two cases.

The current revision uses the stronger uniform estimate.  If \(j=0\),
the ratio in Lemma 2 is exactly one, while its claimed upper bound is
\(e^{6d^2/n}\ge1\).

Now assume \(1\le j\le d\).  If \(j\le4\), then
\[
\begin{aligned}
(n-j+4)^{2(d-j)}
&=
n^{2(d-j)}
\left(1+\frac{4-j}{n}\right)^{2(d-j)}\\
&\le
n^{2(d-j)}
\exp\!\left(
\frac{2(d-j)(4-j)}n
\right).
\end{aligned}
\]
If \(j\ge4\), then \(n-j+4\le n\), so the same statement holds with
zero exponential cost.  Together,
\[
(n-j+4)^{2(d-j)}
\le
n^{2(d-j)}
\exp\!\left(
\frac{2(d-j)(4-j)_+}{n}
\right).
\tag{C}
\]

For \(j\ge1\),
\[
(d-j)(4-j)_+
\le3(d-1).
\]
Hence
\[
\begin{aligned}
4d^2+2(d-j)(4-j)_+
&\le4d^2+6(d-1)\\
&\le6d^2,
\end{aligned}
\]
because
\[
6d^2-\bigl(4d^2+6d-6\bigr)
=2(d^2-3d+3)>0.
\]

Substituting (B)--(C) into (A) and using
\((d)_{\underline j}\le d^j\) proves
\[
\boxed{
\frac{T_{n-j,d-j}}{T_{n,d}}
\le
\exp(6d^2/n)
\left(\frac{2d}{n^2}\right)^j.
}
\]
Thus the revised proof of Lemma 2, including the constant \(6\), is
correct.

## 5. From the near-logarithmic profile bound to
\(A^j j^{Aj}\)

The previously audited estimate supplies a fixed absolute \(C_0\)
such that
\[
|b_{k,j}|
\le
\exp(C_0(j+5)\log(j+5))k^j
\]
whenever \(k\ge2(j+5)\).

For \(j\ge6\),
\[
(j+5)\log(j+5)\le3j\log j.
\]
Choose \(A\ge\max\{1,3C_0\}\).  Then
\[
\exp(C_0(j+5)\log(j+5))
\le j^{Aj}
\le A^jj^{Aj}.
\]

There are only five remaining indices.  Enlarge the same fixed \(A\)
so that
\[
\log A
\ge
\max_{1\le j\le5}
\frac{C_0(j+5)\log(j+5)}j.
\]
Then \(A^j\) alone covers the near-logarithmic bound for each of
these indices.  Therefore one absolute \(A\), independent of
\(j,k,d\), satisfies
\[
\boxed{
|b_{k,j}|\le A^jj^{Aj}k^j
\qquad(j\ge1).
}
\]
The \(j=1\) case, where \(j^{Aj}=1\), is explicitly covered by the
\(A^j\) factor.

## 6. Relative-error reduction

Using the repaired ratio with \(n=m=2k-4\),
\[
\begin{aligned}
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
&\le
e^{6d^2/m}
\sum_{j=1}^d
A^jj^{Aj}k^j
\left(\frac{2d}{m^2}\right)^j.
\end{aligned}
\]
For \(k\ge4\), \(m\ge k\).  Since \(j\le d\),
\[
A^jj^{Aj}k^j
\left(\frac{2d}{m^2}\right)^j
\le
\left(
\frac{2A\,d^{A+1}}k
\right)^j.
\]
No extra power of \(d\), \(j\), \(k\), or \(A\) is missing.

## 7. Choosing an absolute \(\eta\)

The quantifier order is:

1. the profile proof fixes an absolute \(C_0\);
2. Section 5 fixes an absolute \(A=A(C_0)\);
3. choose an absolute number
   \[
   \boxed{
   \eta=\frac1{2(A+1)}.
   }
   \]

Since \(A\ge1\),
\[
0<\eta<\min\left\{\frac12,\frac1{A+1}\right\}.
\]
This is a concrete admissible choice, even though \(C_0\) and \(A\)
were intentionally not optimized.

Uniformly over all integers \(0\le d\le k^\eta\),
\[
\frac{d^2}{m}
\le k^{2\eta-1}
=o(1),
\]
and
\[
\theta_k(d):=
\frac{2A\,d^{A+1}}k
\le
2A k^{\eta(A+1)-1}
=2A k^{-1/2}
=o(1).
\]

The hypotheses used earlier also hold uniformly:

- \(d\le m/4\), because \(\eta<1\);
- \(k\ge2(j+5)\) for every \(j\le d\), again because
  \(d=o(k)\);
- \(m\ge k\) for \(k\ge4\).

For sufficiently large \(k\),
\[
\sup_{0\le d\le k^\eta}\theta_k(d)<\frac12.
\]
Therefore
\[
\begin{aligned}
\sup_{0\le d\le k^\eta}
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
&\le
e^{6k^{2\eta-1}}
\frac{2Ak^{-1/2}}{1-2Ak^{-1/2}}\\
&=o(1).
\end{aligned}
\tag{D}
\]
Here juxtaposition denotes multiplication:
\[
(1+o(1))
\frac{\theta_k}{1-\theta_k}=o(1).
\]

Thus the uniform \(o(1)\) and eventual positivity follow after the
Lemma 2 repair.

## 8. Independent verifier

The new verifier
`independent_verify_polynomial_top_window.py` implements the
\(4\)-Stirling recurrence locally and imports no existing OPG
verifier.  At \(n\le160\), it records:

\[
\begin{array}{c|r}
\text{check}&\text{count}\\ \hline
\text{pair lower bounds}&3,160\\
\text{star-graph upper bounds}&46,620\\
\text{exact intermediate quotients}&46,620\\
\text{final constant-6 ratios}&46,620\\
\text{corrected exponent inequalities}&32,896.
\end{array}
\]

It finds exactly the two failures in the printed coarse exponent
step:
\[
(d,\text{printed coefficient},\text{target})
=(2,32,24),(3,60,54).
\]
It also checks the repaired
\[
4d^2+2(d-j)(4-j)_+\le6d^2
\]
through \(d=256\), and checks the positive exponent margins for
\(\eta=1/(2(A+1))\) at \(1\le A\le32\).

The finite checks support the exact derivation but do not replace it.

## 9. Implemented manuscript repair

The revised numerator and constant-combination paragraph now states:

```text
The case j=0 is immediate because the ratio is one.  For j>=1,

(n-j+4)^(2(d-j))
 <= n^(2(d-j))
    exp(2(d-j)(4-j)_+/n).

Since (d-j)(4-j)_+ <= 3(d-1),

4d^2 + 2(d-j)(4-j)_+ <= 4d^2+6(d-1) <= 6d^2.
```

No theorem statement, downstream exponent, or choice of \(\eta\)
changed.  This is mathematically equivalent to the repair prescribed
by the first audit.  The manuscript's separate check
\[
d=2,\ j=1:\qquad 4d^2+2(d-j)(4-j)_+=22\le24
\]
handles the only \(d=2\) case with a nonzero added term.  For
\(d\ge3\), its estimate
\[
2(d-j)(4-j)_+\le6d\le2d^2
\]
closes the constant-\(6\) bound.  The \(j=0\) and \(d=0,1\) cases are
correctly separated.  Explicitly, the only nontrivial \(d=1\) case is
\[
\frac{T_{n-1,0}}{T_{n,1}}
=\frac{2}{n(n+7)}
\le\frac{2}{n^2}
\le e^{6/n}\frac{2}{n^2}.
\]

## 10. Final assessment

The current manuscript passes the strict audit.  Its revised
derivation of the constant \(6\) covers the two cases missed by the
first version, and the independent verifier confirms the resulting
ratio throughout its finite test range.

The profile-to-\(A\) conversion and the uniform absolute-\(\eta\)
quantifiers continue to pass without changes.
