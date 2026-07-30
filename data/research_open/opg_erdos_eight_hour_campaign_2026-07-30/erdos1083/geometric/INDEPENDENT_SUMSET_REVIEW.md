# Independent review of the square–chord sumset attack

Date: 2026-07-30

Reviewed files:

- `SUMSET_EXPANSION_ATTACK.md`;
- `verify_sumset_expansion.py`;
- `test_verify_sumset_expansion.py`.

No reviewed file was modified.

## 1. Verdict

The square-translate energy theorem is correct, including its constant
\[
|A_m+\{x_k\}|
\ge
\frac{m^2S^2}{2mS+\tau_*(m)S^2}.                    \tag{1}
\]
The chord-multiplicity argument correctly supplies its hypothesis whenever
the \(S\) angular points are distinct.

At \(m=S=t^2\), the theorem gives a valid
\(t^{4-o(1)}=N^{4/5-o(1)}\) lower bound for the explicit common-radius
slice of the anisotropic construction with \(N=t^5\).  Since \(D\) denotes
nonzero distances, the exact implication is
\[
D\ge |A_m+X_S|-1,                                  \tag{2}
\]
not literally \(D\ge |A_m+X_S|\).  The subtraction of one has no effect on
the displayed exponent.

The result is not an unconditional improvement for \(f_3(N)\).  The old
proof tree does not force the simultaneous common-radius, arithmetic-height,
and common-angular rectangle used by the slice.

## 2. Chord-layer multiplicity

Let \(z_k=e^{ik\theta}\).  If
\[
\cos(k\theta)=\cos(l\theta),
\]
then \(z_k+z_k^{-1}=z_l+z_l^{-1}\), so
\[
(z_k-z_l)(z_k-z_l^{-1})=0.
\]
Thus \(z_l=z_k\) or \(z_l=z_k^{-1}\).  If the indexed angular points
\(z_0,\ldots,z_{S-1}\) are pairwise distinct, a fixed chord value has at
most the two preimages \(z,z^{-1}\).  At \(z=\pm1\), these coincide and the
multiplicity is one.

Therefore the hypothesis “every \(x\)-value occurs at most twice” is valid.
The verifier assumes this condition and asserts it on each supplied finite
case; it does not itself prove that arbitrary input vectors arise from
distinct angular points.  That implication is the human argument above.

## 3. Energy and the zero-difference layer

For
\[
r(y)=\#\{(d,k):0\le d<m,\ 0\le k<S,\ d^2+x_k=y\},
\]
one has \(\sum_y r(y)=mS\), even when indexed \(x_k\)'s repeat.  The support
of \(r\) is the ordinary set \(A_m+\{x_k\}\), so Cauchy gives
\[
(mS)^2\le |A_m+\{x_k\}|\sum_y r(y)^2.               \tag{3}
\]

The energy split and constants are correct:

1. \(k=l\): \(d^2=e^2\), hence \(d=e\), giving exactly \(mS\).
2. \(k\ne l,\ x_k=x_l\): again \(d=e\).  A multiplicity-two value
   contributes two ordered index pairs.  Summed over all values, there are
   at most \(S\) such ordered pairs, hence at most another \(mS\).
3. \(x_k\ne x_l\): any collision forces
   \[
   n=x_l-x_k=d^2-e^2\in\mathbb Z\setminus\{0\},
   \qquad |n|\le(m-1)^2.                             \tag{4}
   \]

Thus the \(n=0\) case is fully contained in the first two contributions and
must not be passed to the divisor function.

For \(n>0\),
\[
n=(d-e)(d+e)
\]
has \(d-e>0\).  A positive divisor \(d-e\) determines \(d+e\), and hence
determines \(d,e\); parity and range restrictions only remove candidates.
For \(n<0\), interchange \(d,e\).  Consequently a fixed ordered layer pair
has at most \(\tau(|n|)\), not \(2\tau(|n|)\), solutions.

This proves
\[
\sum_y r(y)^2
\le 2mS+\tau_*(m)S^2.                               \tag{5}
\]
The use of \(S^2\), rather than the slightly smaller number of unequal
ordered layer pairs, is harmless.  Combining (3) and (5) gives (1) with the
stated denominator.

An independent brute-force check verified
\[
\#\{(d,e)\in[0,m-1]^2:d^2-e^2=n\}\le\tau(|n|)
\]
for every nonzero represented \(n\) and every \(1\le m\le29\).

## 4. Critical scaling

At \(m=S\),
\[
\frac{m^2S^2}{2mS+\tau_*(m)S^2}
=\frac{m^2}{\tau_*(m)+2}.                            \tag{6}
\]
Since
\[
\tau_*(m)
\le\max_{n\le m^2}\tau(n)=m^{o(1)},
\]
(6) is \(m^{2-o(1)}\).  For \(m=S=t^2\), it is
\(t^{4-o(1)}\).

The explicit anisotropic grid has
\[
L=t,\qquad m=S=t^2,\qquad
F=Lm=t^3,\qquad N=FS=t^5.
\]
Its smallest-radius class contains \(mS=t^4\) points and realizes the
square–chord set in (6).  Therefore (2) yields
\[
D\ge t^{4-o(1)}-1=N^{4/5-o(1)}.                     \tag{7}
\]
This conversion is correct only for that full construction and its
displayed slice; the slice itself has \(t^4\), not \(t^5\), points.

## 5. Refined inverse count

The refined count \(R\) is explicitly an **ordered** count of \((k,l)\).
The energy estimate
\[
\sum_y r(y)^2\le2mS+\tau_*(m)R
\]
and the rearrangements
\[
R\ge\frac{mS}{\tau_*(m)}
\left(\frac{\sqrt S}{K}-2\right)
\]
and, when \(\sqrt S\ge4K\),
\[
R\ge\frac{mS^{3/2}}{2K\tau_*(m)}
\]
are correct.

Every unordered layer pair contributes its two orientations, whose
polynomials differ only by an overall sign.  Thus the lower bound certifies
at least \(R/2\) unordered Chebyshev relations, not \(R\) independent
relations.  Distinct relations all vanish at the same \(c=\cos\theta\), but
their number by itself does not lower the degree below \(S-1\); a gcd or
resultant argument would be needed for a stronger structural conclusion.

## 6. Algebraic degree and height

For every nontrivial collision,
\[
P_{k,l,n}(z)=2m^2(T_k(z)-T_l(z))-n
\]
is a nonzero integer polynomial of degree at most \(S-1\).  Hence one
collision already proves
\[
[\mathbb Q(c):\mathbb Q]\le S-1.
\]
The minimal polynomial of \(c\) divides every relation polynomial over
\(\mathbb Q[z]\).  This divisibility is correct, but should not be read as
independence of the \(R\) ordered relations.

The recurrence for \(T_j\) gives a coefficient \(\ell^1\)-norm bounded by
\(3^j\), so the deliberately loose estimate
\[
\|P_{k,l,n}\|_1\le5m^2\,3^S
\]
is valid.  The Mahler-measure inequality then gives the absolute logarithmic
Weil height
\[
h(c)=O(S+\log m).
\]
A standard factor-height inequality gives the same asymptotic bound for the
logarithm of the naive height of the primitive minimal polynomial.  The note
would be clearer if it named which height convention is intended, but the
asymptotic claim is sound under either standard convention.

## 7. Other angle classes

- If \(c\) is transcendental, an intersection of two distinct layers would
  give a nonzero rational polynomial relation in \(c\); hence all \(mS\)
  indexed sums are distinct.
- If \(c\) is algebraic of degree at least \(S\), the same conclusion follows
  from the degree-\((S-1)\) bound.
- If \(e^{i\theta}\) is a root of unity and the first \(S\) angular points
  are distinct, chord multiplicity is still at most two.
- For a nonzero algebraic \(\theta\), algebraicity of \(\cos\theta\) would
  make \(e^{i\theta}\) algebraic through a quadratic equation, contradicting
  Lindemann–Weierstrass.  The stated transcendence conclusion is correct.

## 8. Verifier scope

The verifier correctly:

- computes exact representation energies;
- checks both energy upper bounds;
- uses the exact maximal divisor count through \((m-1)^2\);
- counts the refined relation pairs as ordered pairs;
- tests rational, algebraic quotient-field, cyclotomic and integral-resonant
  examples.

The three modulus polynomials used for the algebraic cases are irreducible
over \(\mathbb Q\), so equality of reduced coordinate vectors is legitimate
in those cases.

The verifier is finite evidence.  It does not machine-prove:

- the angular multiplicity implication for arbitrary \(\theta\);
- the divisor-factorization theorem for arbitrary \(m\);
- the algebraic height statement;
- the inherited proof-tree extraction.

Reproduction succeeded:

```text
2 passed in 0.59s
certificate sha256 =
e48128e422c757efed9475ed1124b7b4f4cd0542fb2cec36a994ecc9562e502a
```

## 9. Publication and claim boundary

The elementary theorem is a valid structured-slice improvement and rules
out the explicit critical anisotropic grid as a low-distance extremizer.
It does not establish
\[
f_3(N)\ge N^{4/5-o(1)}
\]
or any unconditional exponent beyond the inherited \(3/5-o(1)\).

The only corrections needed at claim level are:

1. retain the \(-1\) when translating a squared-distance set containing zero
   to the number of nonzero distances;
2. distinguish ordered relation count \(R\), unordered relations \(R/2\),
   and algebraically independent information;
3. specify the intended height convention.

None changes the main conditional energy theorem or its exponent.
