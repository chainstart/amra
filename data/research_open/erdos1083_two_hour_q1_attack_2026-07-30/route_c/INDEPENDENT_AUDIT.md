# Independent red-team audit: prime-power cyclotomic fibre escape

Date: 2026-07-30

Audited target:
`PRIME_POWER_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md`

## 0. Verdict

\[
\boxed{\texttt{PASS; BOTH AUDIT CORRECTIONS ARE INCORPORATED}}
\]

No counterexample was found to Theorem 3, its Kneser lower bound, the
aperiodic corollary, the complete-fibre corollary, or the stated
prime-power base-field extension.  The selected squared-distance labels
are genuinely injective across angular classes, heights, and radii.

The current revision has incorporated both points raised in the first
audit:

1.  The equal-fibre constant is now stated in its sharp
    prime-dependent form
    \[
    \frac{p-1}{2p}|P|
    \]
    for \(m=p^a\), with uniform consequence \(3|P|/7\) for \(p\ge7\).
    The order-\(p\) subgroup example makes the constant exact.
2.  The base-field proof now correctly says that the \(p\) terms
    arising from one coefficient of \(h\) occupy one residue class
    modulo \(p^{a-1}\), while different coefficients occupy different
    residue classes.  This is the required disjoint-support argument.

There is also a possible extension, not a defect: five-term rigidity
fails at \(p=5\), but the sign pattern of a distance-label collision
appears to rule out the five-gon relation.  Thus \(p\ge7\) is sufficient
but probably not optimal for the prime-power injection.

A separate, broader rational-coefficient extension is available from
Mann's short root-of-unity relation theorem: five-term rigidity holds
for every \(m>1\) with \(\gcd(m,30)=1\).  That extension is not yet part
of the audited target and should not be conflated with Corollary 7 over
an arbitrary base field \(K\).

## 1. Relation-space dimension and minimum support

Put \(q=p^{a-1}\).  The evaluation map
\[
\mathbb Q^m\longrightarrow\mathbb Q(\zeta),\qquad
(c_j)\longmapsto\sum_jc_j\zeta^j
\]
is surjective and has nullity
\[
m-\varphi(m)=p^a-(p-1)p^{a-1}=q.
\]
For \(0\le u<q\), the \(p\)-gon relation supported on
\[
\{u,u+q,\ldots,u+(p-1)q\}
\]
vanishes.  These \(q\) supports are pairwise disjoint, so the relations
are independent and hence form a basis of the kernel.

It follows more strongly than a mere dimension count that every kernel
vector is constant on each such \(p\)-element coset.  A nonzero vector
therefore has at least \(p\) nonzero coordinates.  This proves the
minimum-support assertion and the five-term rigidity for \(p\ge7\).
No hidden assumption on the signs or integrality of the rational
coefficients is used here.

The supplied quotient-ring verifier implements the correct reduction.
For a degree-\(<p^a\) coefficient vector, the coefficient at
\((p-1)q+i\) is subtracted from every basis exponent congruent to \(i\)
modulo \(q\), exactly as prescribed by
\[
X^{(p-1)q+i}
\equiv-\sum_{k=0}^{p-2}X^{kq+i}\pmod{\Phi_{p^a}(X)}.
\]

## 2. Five-exponent label injection

Suppose two selected labels agree.  After bringing the right side to the
left, their coefficient vector is supported on
\[
\{0,d,-d,e,-e\}.
\]
For \(p\ge7\), the minimum-support result forces the collected vector to
be identically zero.

The canonical representatives satisfy
\[
1\le d,e\le(m-1)/2.
\]
Consequently, if \(d\ne e\), the sign pairs
\(\{d,-d\}\) and \(\{e,-e\}\) are disjoint.  The coefficient at
\(\zeta^d\) is then \(-r^2\), which cannot vanish.  Hence \(d=e\).
The coefficient at \(\zeta^d\) next gives \(r^2=s^2\); positive radii
give \(r=s\).  The constant coefficient gives equality of the two
anchored height squares.  Both height offsets are nonnegative because
the anchors are minima, so the heights themselves are equal.

This also covers the anchor fibre \(z=z_r^-\): a selected class has
\(d\ne0\), hence the realized chord has positive squared distance.
Thus no selected zero distance has accidentally been counted.

I found no collision in an independent exact-rational grid audit:

| angular order | exact labels checked | collisions |
|---:|---:|---:|
| \(5\) | 60 | 0 |
| \(25\) | 360 | 0 |
| \(7\) | 90 | 0 |
| \(49\) | 720 | 0 |

The \(p=5\) rows are outside the stated theorem and are reported only to
show that failure of the coarse support lemma is not itself a
distance-label counterexample.  Indeed, if a five-supported collision
at \(p=5\) were a nonzero relation, all five coefficients on one
\(5\)-gon coset would be equal.  The two chord pairs have coefficients
\(-r^2\) and \(+s^2\), which is impossible for positive radii.

## 3. Kneser constant and sign classes

For
\[
D=A-B,\qquad H=\operatorname{Stab}(D),
\]
Kneser's theorem gives exactly
\[
|D|\ge |A+H|+|B+H|-|H|=L.
\]
Discarding zero loses at most one element.  Since \(m\) is odd, every
nonzero unoriented class has exactly two elements, and therefore
\[
q(D)\ge\left\lceil\frac{|D|-1}{2}\right\rceil
\ge\left\lceil\frac{L-1}{2}\right\rceil.
\]
The use of \(|D|-1\) is safe even when \(0\notin D\); it is simply one
unit weaker in that case.

I exhaustively checked all \(127^2=16129\) ordered pairs of nonempty
subsets \(A,B\subseteq\mathbb Z/7\mathbb Z\).  Every pair satisfies both
the Kneser bound and the displayed sign-class bound.  No small
counterexample or parity exception was found.

## 4. Equal fibres: audit strengthening incorporated

The current proof uses the fact that every nontrivial subgroup of
\(\mathbb Z/p^a\mathbb Z\) has order at least \(p\), as suggested in the
first audit.

Let \(h=|H|\).  If \(h=1\), Kneser gives
\[
q\ge S-1,\qquad \frac qS\ge\frac12
\quad(S\ge2).
\]
If \(h>1\), then \(h\ge p\).  Put \(k=\lceil S/h\rceil\).  Both
\(A+H\) and \(B+H\) contain at least \(k\) \(H\)-cosets, so
\[
L\ge(2k-1)h
\]
and, since \(h\) is odd,
\[
\frac qS
\ge
\frac{(2k-1)h-1}{2S}
\ge
\frac{(2k-1)h-1}{2kh}.
\]
For \(k=1\), the right side is \((h-1)/(2h)\ge(p-1)/(2p)\).
For \(k\ge2\), it is larger.  Hence
\[
\boxed{
|\Delta^2(P)|
\ge\frac{p-1}{2p}|P|
\ge\frac37|P|.
}
\]

This is sharp: take one fibre with
\(A=B=H\), where \(H\) is a subgroup of order \(p\).  Then
\[
D=H,\qquad q=\frac{p-1}{2},\qquad |P|=p.
\]
For \(p=7\), equality is \(3/7\).  The exhaustive
\(\mathbb Z/7\mathbb Z\) calculation found the following actual minima:

| \(S\) | minimum \(q/S\) |
|---:|---:|
| 2 | \(1/2\) |
| 3 | \(2/3\) |
| 4 | \(3/4\) |
| 5 | \(3/5\) |
| 6 | \(1/2\) |
| 7 | \(3/7\) |

Thus the manuscript's revised constant and subgroup sharpness statement
are both correct.

## 5. Aperiodic and complete fibres

When \(H=\{0\}\), one has \(L=2S-1\), hence
\[
q\ge S-1.
\]
Summing gives the claimed \((1-1/S)|P|\) lower bound.  The observation
\(2S-1\le m\) follows because Kneser's lower bound must fit in \(G\).

For complete fibres, \(D=G\), and because \(m\) is odd there are exactly
\((m-1)/2\) nonzero sign classes.  The resulting
\((m-1)/(2m)\) factor follows exactly.  These two endpoint regimes are
consistent with the stabilizer-sensitive main bound.

## 6. Base-field extension

Assume \(\Phi_{p^a}\) is irreducible over \(K\).  It is then the minimal
polynomial of \(\zeta\) over \(K\).  Any degree-\(<m\) relation
\(f(\zeta)=0\) has
\[
f=h\Phi_{p^a},\qquad \deg h<q.
\]
Writing \(h=\sum_{i=0}^{q-1}h_iX^i\), one obtains
\[
h\Phi_{p^a}
=\sum_{i=0}^{q-1}\sum_{k=0}^{p-1}h_iX^{i+kq}.
\]
For distinct \(i\), these supports lie in distinct residue classes
modulo \(q\); within one residue class all \(p\) coefficients equal
\(h_i\).  Thus every nonzero product has support at least \(p\).

This proves the extension exactly as intended.  The current revision
uses the correct residue-class wording.

The final inference from equal anchored squares to equal heights remains
valid over \(K\subset\mathbb R\), since it uses the real order and the
nonnegative anchored offsets, not an algebraic square-root choice in
\(K\).

## 7. Sharpness and scope

The subgroup example is an exact witness for the Kneser stabilizer loss,
and the order-eight identity in the manuscript is a correct warning that
arbitrary composite orders can have cross-radius collisions.

The theorem remains a terminal structured-family exclusion.  It does
not extract such a fibre from an arbitrary critical configuration and
therefore does not, by itself, improve the \(N^{3/5}\) exponent.

The \(p=5\) red-team check shows that the sentence “five-term rigidity is
false” is correct, but it should not be read as a sharpness example for
the geometric theorem.  A genuine \(p=5\) collision would need to
respect the opposite signs on the two chord pairs, and the basic
five-gon relation does not.

## 8. Reproduction record

The supplied verifier and tests were run without bytecode or pytest
cache writes:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify_prime_power_cyclotomic_escape.py
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider \
  test_verify_prime_power_cyclotomic_escape.py
```

Result:

```text
7 passed in 0.05s
```

The independent exhaustive calculation additionally checked all
nonempty subset pairs in \(\mathbb Z/7\mathbb Z\), the exact equal-size
minima above, and exact quotient-field label grids at orders
\(5,25,7,49\).  These computations support the finite algebra and
sharpness analysis; the unbounded conclusions rest on the proofs
audited in Sections 1--6.
