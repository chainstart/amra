# Independent red-team audit of partial cyclotomic fibre escape

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS for prime }p}
\]

`PARTIAL_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md` is correct as stated.
The direction of the difference set, quotient by \(d\sim-d\), integer
rounding after Cauchy--Davenport, injection across radii and heights,
and the constant in the equal-fibre corollary have all been
independently reconstructed.

The unchanged theorem is false for a general cyclic angular group.
The smallest composite counterexample of order at least seven is the
order-eight subgroup fibre
\[
\{0,2,4,6\}\subset\mathbb Z/8\mathbb Z:
\]
it is a square, so it has two nonzero chord distances, whereas the
prime-form corollary would demand \(S-1=3\).

## 1. Difference direction and the sign quotient

At radius \(r\), let
\[
A^-=\mathcal A_{r,z_r^-},
\qquad
A=\mathcal A_{r,z}.
\]
For endpoints with anchor angle \(i\in A^-\) and target angle
\(j\in A\), their directed angular difference is
\[
j-i\in A-A^-.
\]
Thus the direction in
\[
\mathcal D_{r,z}=\mathcal A_{r,z}-\mathcal A_{r,z_r^-}
\]
is correct.

The horizontal squared chord is
\[
r^2\left(2-\zeta^{j-i}-\zeta^{-(j-i)}\right),
\]
which is unchanged under \(j-i\mapsto i-j\).  Hence nonzero differences
must be quotiented by
\[
d\sim-d.
\]
For odd \(p\), every nonzero class has exactly two elements and a
unique representative in
\[
\{1,\ldots,(p-1)/2\}.
\]
The theorem only uses the weaker fact that such a class contains at
most two elements.

If a class meets \(\mathcal D_{r,z}\), its representative \(d\) or
\(-d\) equals \(j-i\) for an actual endpoint pair.  Thus every selected
class gives a genuine distance; no orientation has been reversed or
invented.

## 2. Cauchy--Davenport and integer rounding

Cauchy--Davenport applied to \(A+(-A^-)\) gives exactly
\[
|\mathcal D_{r,z}|
\ge
M:=\min(p,|A|+|A^-|-1).
\tag{1}
\]
There are two cases:

* if \(0\in\mathcal D_{r,z}\), deleting it leaves
  \(|\mathcal D_{r,z}|-1\) elements;
* if \(0\notin\mathcal D_{r,z}\), all
  \(|\mathcal D_{r,z}|\) elements remain.

Since every sign class contains at most two nonzero elements, both
cases imply
\[
q_{r,z}
\ge
\left\lceil\frac{|\mathcal D_{r,z}|-1}{2}\right\rceil
\ge
\boxed{
\left\lceil\frac{M-1}{2}\right\rceil.
}
\tag{2}
\]
The second inequality uses monotonicity of the ceiling function.  No
floor/ceiling unit is lost.

The independent verifier exhausts all
\[
(2^7-1)^2=16129
\]
ordered pairs of nonempty subsets of \(\mathbb F_7\), checking both
(1) and (2).

## 3. Injection across radius and height

For one selected unoriented class, write
\[
\lambda(r,z,d)
=r^2a_d+(z-z_r^-)^2.
\]
If two selected labels coincide, the resulting rational relation is
supported on
\[
\{0,d,p-d,e,p-e\}.
\]
For \(p\ge7\) this is a proper subset of all \(p\) cyclotomic
characters.  The unique rational all-ones relation therefore forces
all coefficients to vanish.

The representatives \(d,e\in[1,(p-1)/2]\) give disjoint exponent pairs
unless \(d=e\).  It follows successively that
\[
d=e,\qquad r^2=s^2,\qquad r=s.
\]
After \(r=s\), both heights belong to the same radius-dependent set,
so their anchors agree.  The constant term gives
\[
(z-z_r^-)^2=(w-z_r^-)^2.
\]
Both differences are nonnegative by minimality of the anchor, hence
\[
z=w.
\]
This checks the cross-radius and cross-height quantifiers.  The
angular sets themselves need not agree at any two heights.

## 4. Equal fibre size

If all fibres have size \(S\), then
\[
a_r=s_{r,z}=S.
\]
Under
\[
2\le S\le\frac{p+1}{2},
\]
one has the exact integer inequality
\[
2S-1\le p.
\]
Consequently (2) becomes
\[
\left\lceil\frac{(2S-1)-1}{2}\right\rceil
=S-1.
\]
Summing over the height layers gives
\[
|\Delta^2(P)|
\ge
(S-1)\sum_r|\mathcal Z_r|.
\]
Since
\[
|P|=S\sum_r|\mathcal Z_r|,
\]
the constant is exactly
\[
\boxed{1-\frac1S.}
\]
The endpoint \(S=(p+1)/2\) is valid: it gives
\(2S-1=p\), not \(p+1\).

## 5. Small-counterexample search

The independent search found no prime counterexample:

* every ordered nonempty subset pair in \(\mathbb F_7\) satisfies the
  claimed sign-class lower bound;
* varying examples over \(\mathbb F_{11}\) have unequal angular
  supports, unequal height counts, rational nonintegral squared radii,
  and non-arithmetic anchored height squares;
* canonical coefficient vectors in the real cyclotomic basis verify
  global injection without importing the author's quotient
  implementation.

The search does find the expected composite obstruction immediately.

### Order eight: failure of the linear constant

Take one radius, one height, and angular support
\[
A=\{0,2,4,6\}\subset\mathbb Z/8\mathbb Z.
\]
This is a square.  Its nonzero difference classes are represented by
\[
2,\ 4,
\]
so it has exactly two squared chord distances.  Here \(S=4\) and
\[
S\le\frac{8+1}{2},
\]
but the unchanged prime conclusion would give at least \(S-1=3\)
distances.  Thus the equal-size corollary is false for general cyclic
order.

For odd composite order, the first analogous example is
\[
\{0,3,6\}\subset\mathbb Z/9\mathbb Z,
\]
a regular triangle with one distance instead of the predicted two.

### Order eight: failure of algebraic injection

There is also a cross-radius collision.  At order eight,
\[
a_2=2,\qquad a_4=4.
\]
The two distinct choices
\[
(r^2,d)=(1,2),
\qquad
(s^2,e)=\left(\frac12,4\right)
\]
both give squared label \(2\).  Hence the prime cyclotomic
independence step also fails, separately from Cauchy--Davenport.

## 6. What survives for composite order

For \(G=\mathbb Z/n\mathbb Z\), Kneser's theorem gives, with
\[
H=\operatorname{Stab}(A-A^-),
\]
\[
|A-A^-|
\ge
|A+H|+|A^-+H|-|H|.
\tag{3}
\]
The sign quotient still gives
\[
q\ge
\left\lceil\frac{|A-A^-|-1}{2}\right\rceil.
\tag{4}
\]
Thus a stabilizer-dependent combinatorial bound survives.

However, (3)--(4) do not repair the algebraic injection across radii
and heights; the order-eight collision above is an explicit failure.
An extension to composite order would need both:

1. an aperiodicity/stabilizer term replacing Cauchy--Davenport; and
2. a separate linear-independence hypothesis for the relevant real
   cyclotomic chord characters.

Because neither follows from the cyclic order alone, no general
composite-order theorem is asserted.

## 7. Claim status

### Base-field extension audit

Theorem 4 is valid under its stated, deliberately sufficient
hypothesis.  If \(K\subset\mathbb R\), \(r^2\) and the anchored height
squares lie in \(K\), and \(\Phi_p\) is irreducible over \(K\), an
equality of selected labels produces a polynomial
\[
f\in K[X],\qquad \deg f\le p-1,\qquad f(\zeta_p)=0.
\]
Minimal-polynomial divisibility gives \(f=0\) or
\(f=c\Phi_p\).  The second alternative is impossible for \(c\ne0\):
\(f\) is supported on at most five exponents, while \(\Phi_p\) has
all \(p\ge7\) coefficients nonzero.  Coefficient comparison therefore
recovers, in order,
\[
d=e,\quad r^2=s^2,\quad r=s,\quad z=w.
\]
The order and sign steps use that the geometric radii and heights are
real; no ordering of arbitrary elements of \(K\) is being assumed.

For a fixed number field, the “all but finitely many primes” statement
also passes audit.  Irreducibility is equivalent to
\[
K\cap\mathbb Q(\zeta_p)=\mathbb Q
\]
because the cyclotomic extension is Galois.  With
\(K_{\rm ab}=K\cap\mathbb Q^{\rm ab}\), Kronecker--Weber places
\(K_{\rm ab}\) in one \(\mathbb Q(\zeta_m)\).  For \(p\nmid m\), a
nontrivial intersection with the prime-conductor field would have
conductor both divisible by \(p\) and supported on primes dividing
\(m\), which is impossible.  Only primes dividing \(m\) remain as
possible exceptions.

This hypothesis is stronger than logically necessary for these real
chord labels: linear disjointness from the maximal real cyclotomic
subfield would suffice.  That sharpening is not needed for, and is
not claimed by, Theorem 4.

### Proved

* the prime theorem and all stated corollaries;
* Theorem 4 over a real coefficient field with irreducible
  \(\Phi_p\), including the fixed-number-field finite-exception
  statement;
* the exact ceiling in the Cauchy--Davenport bound;
* cross-radius and cross-height injection;
* the equal-size constant through \(S=(p+1)/2\);
* failure of the unchanged statement for composite cyclic order.

### Not proved

* extraction of these fibres from a general critical configuration;
* a useful uniform composite-order replacement;
* an unconditional improvement for Erdős #1083.

## 8. Verification

Run:

```bash
pytest -q test_independent_verify_partial_cyclotomic_fibre_escape.py
python3 independent_verify_partial_cyclotomic_fibre_escape.py
```

The independent implementation imports nothing from
`verify_partial_cyclotomic_fibre_escape.py`.
