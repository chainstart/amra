# Independent units versus additive containers

## 1. The naive statement is false

Multiplicatively independent unit directions do not, by themselves, force
independent additive directions.

Let

\[
f(x)=\prod_{k=1}^{5}(x+k)-1
=x^5+15x^4+85x^3+225x^2+274x+119,
\]

and let \(f(\theta)=0\).  Reduction modulo \(2\) is irreducible, so \(f\)
is irreducible over \(\mathbb Q\).  Exact Sturm isolation gives five real
roots.  For

\[
\varepsilon_k=\theta+k,\qquad1\le k\le5,
\]

\[
N(\varepsilon_k)=1,\qquad
\prod_{k=1}^5\varepsilon_k=1.
\]

The first four units are multiplicatively independent.  This is certified
without a floating-point zero test.  Rational root intervals of width below
\(10^{-30}\) are converted by dividing degenerate integer intervals
entirely inside a 60-decimal-digit interval context.  Every
\(\theta_i+k\) interval is explicitly checked not to cross zero before
taking its absolute value and logarithm.  The resulting \(4\times4\) log
minor is contained in the deliberately rounded-out decimal interval

\[
[6.31087583266352,\ 6.31087583266354],
\]

which excludes zero.

Nevertheless all five units lie in

\[
\operatorname{span}_{\mathbb Q}\{1,\theta\},
\]

and even in the affine progression
\(\theta+\{1,2,3,4,5\}\).  Thus the raw claim

> independent logarithmic unit directions force comparable additive rank

is false.

## 2. Why the hyperbola may still expand

The translation problem does not use \(t\) alone.  It uses

\[
t+R/t,\qquad t-R/t,\qquad R=-3069.
\]

In the consecutive-unit family,

\[
(\theta+k)^{-1}
=\prod_{j\ne k}(\theta+j).
\]

The inverse has degree \(d-1\), despite \(\theta+k\) being affine-linear.
Put \(M=3069\) and

\[
P_d(x)=\prod_{j=1}^d(x+j),\qquad
q_k(x)=\frac{P_d(x)}{x+k}.
\]

For the actual SAT translations \(u(t),c(t)\), put
\(U_k=2u(\theta+k)\) and \(C_k=2c(\theta+k)\).  Thus, before reduction
modulo \(f_d=P_d-1\),

\[
U_k=x+k-Mq_k+3,\qquad C_k=x+k+Mq_k.                       \tag{1}
\]

The inverse expansion has an exact full-minor identity.  Order coefficient
columns as \(1,x,\ldots,x^{d-1}\), and select the \(d\) rows

\[
U_1,C_1,U_2,C_2,U_3,\ldots,U_{d-2}.                       \tag{2}
\]

Then

\[
\boxed{
\det\!\operatorname{Coeff}
(U_1,C_1,U_2,C_2,U_3,\ldots,U_{d-2})
=(-1)^d\,4M^{d-2}\prod_{m=1}^{d-3}m!
}.                                                        \tag{3}
\]

In particular, the doubled inverse-symmetrized polynomials have full
coefficient rank in every degree \(d\ge4\).  This polynomial identity
does not depend on irreducibility or real-root assertions.  Its
interpretation as additive rank of actual elements of
\(\mathbb Q(\theta)\), however, requires \(f_d\) to be the degree-\(d\)
minimal polynomial of the selected real root.

### Proof of (3)

The polynomials \(q_k\) are scaled Lagrange polynomials at
\(-1,\ldots,-d\):

\[
q_k(-j)=0\ (j\ne k),\qquad
q_k(-k)=(-1)^{k-1}(k-1)!(d-k)!.                          \tag{4}
\]

The Vandermonde determinant of the nodes has absolute value
\(\prod_{m=1}^{d-1}m!\).  Consequently

\[
\left|\det(q_1,\ldots,q_d)\right|
=\prod_{m=1}^{d-1}m!.                                    \tag{5}
\]

In (2), replace \(U_i\) by \(U_i+C_i\) for \(i=1,2\), and then subtract
the first new row from the second.  The two affine rows become
\(2x+5\) and \(2\).  They span every affine remainder in the other rows,
so row additions reduce those rows to

\[
Mq_1,\ Mq_2,\ -Mq_3,\ldots,-Mq_{d-2}.
\]

It remains to replace \(q_{d-1},q_d\) in (5) by \(2\) and \(2x+5\).
The coordinate of a polynomial \(h\) on \(q_k\) is
\(h(-k)/q_k(-k)\).  The final \(2\times2\) replacement determinant has
absolute value

\[
\frac4{|q_{d-1}(-(d-1))q_d(-d)|}
=\frac4{(d-2)!(d-1)!}.
\]

Combining this with (5), the \(M^{d-2}\) factor, and the row signs proves
(3).  Notice that the \(+3\) disappears: the identity holds with any
common offset.

### Exact side lengths

Write

\[
q_1(x)=\prod_{j=2}^d(x+j)=\sum_{j=0}^{d-1}b_jx^j.
\]

All \(b_j\) are positive, and coefficientwise \(q_1\) is maximal among
the \(q_k\).  For the first \(d-1\) units, the exact doubled symmetric
power-basis side lengths used by the verifier are

\[
L_0=2(Mb_0+1)+1,\quad
L_1=2(Mb_1+1)+1,\quad
L_j=2Mb_j+1\quad(2\le j<d).                              \tag{6}
\]

Thus the audited two-coset size budget is

\[
B_d=2\prod_{j=0}^{d-1}L_j.                               \tag{7}
\]

This is the exact cardinality when the two translates are disjoint
(in particular when \(Y\notin\mathbb Q(\theta)\)); in general their union
has cardinality between \(B_d/2\) and \(B_d\).  This possible factor two
does not affect any exponent comparison below.

Equations (3) and (6), rather than numerical rank calculations, explain
all earlier observations.  Exact computer algebra additionally verifies
that every \(f_d=P_d-1\) is irreducible and has \(d\) real roots for
\(5\le d\le30\).  This is a finite verification, not a proof for every
degree.

The determinant recurrence is especially simple:

\[
D_{d+1}=3069(d-2)!\,D_d,\qquad
D_5=231249420072.                                        \tag{8}
\]

The exact digit counts are:

| \(d\) | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| digits of \(D_d\) | 12 | 16 | 21 | 27 | 33 | 40 | 48 | 57 |
| digits of \(B_d\) | 27 | 36 | 46 | 57 | 71 | 85 | 102 | 120 |

Since

\[
\prod_{m=1}^{d-3}m!=G(d-1),
\]

the Barnes-\(G\) asymptotic gives

\[
\log D_d
=\frac{(d-2)^2}{2}\log(d-2)-\frac34(d-2)^2+O(d\log d).
                                                                    \tag{9}
\]

The determinant-volume lemma below gives the same
\(\Omega(d^2\log d)\) lower order for any proper integral box containing
the selected doubled shifts.  Equivalently it applies to the actual
shifts in the half-power coordinate lattice
\(\langle1/2,x/2,\ldots,x^{d-1}/2\rangle_{\mathbb Z}\); normalizing back
to the ordinary power lattice changes determinants by only \(2^{-d}\).
Meanwhile \(b_j\le q_1(1)=(d+1)!/2\) gives
\(\log B_d=O(d^2\log d)\).  Hence

\[
\log B_d=\Theta(d^2\log d).                              \tag{10}
\]

## 3. Compatibility and small-doubling audit

This identity is strong negative evidence for additive compression, but
it is not a construction at the target exponent.

Assume now that \(f_d\) is irreducible of degree \(d\) and choose a real
root \(\theta\).  Take

\[
T_d=\{\theta+1,\ldots,\theta+d-1\}.
\]

One half of the coordinate box behind (6), together with its translate
by \(-Y\), satisfies the exact hyperbola compatibility equations for
the actual shifts \(u=U/2,c=C/2\).  Doubling each coordinate
ensures that each selected shift has overlap density at least \(2^{-d}\).
The additive doubling constant of the two-coset construction is
\(O(2^d)\).  By (10), both quantities are only
\(B_d^{o(1)}\) losses, so small doubling and exact compatibility are not
the failure.

The fatal count, along any unbounded sequence of degrees for which the
preceding number-field hypotheses hold, is

\[
|T_d|=d-1=B_d^{o(1)},
\]

whereas the campaign requires \(|T_d|\ge B_d^{2/5-o(1)}\).  Even granting
perfect overlap to every parameter cannot repair this polynomial gap.
Even the optimistic upper bound \(2^{d-1}\) for squarefree products of the
displayed units is only \(B_d^{o(1)}\), and (3) does not show that their
inverse-symmetrized images remain inside (6).

The determinant and box-size formulas are unconditional polynomial
identities, but irreducibility and total reality are currently verified
only for \(5\le d\le30\).  Thus the following number-field interpretation
is proved in that finite range and conditional on the stated hypotheses
along an unbounded degree sequence.  In that precise sense the family:

- exactly satisfies the local hyperbola equations;
- admits an \(n^{o(1)}\)-doubling rectangular realization;
- rigorously forces \(\exp(\Theta(d^2\log d))\) container volume;
- supplies only \(n^{o(1)}\) certified parameters.

It supports the obstruction side of the inverse-symmetrized conjecture,
not the desired counterexample side.

## 4. A proved determinant-to-volume lemma

Let

\[
P=\left\{\sum_{j=1}^s m_jg_j:0\le m_j<M_j\right\}
\]

be a proper integral or fractional-ideal coordinate box.  If shift vectors
\(h_1,\ldots,h_s\in P-P\) have coordinate matrix \(H\), then every
\(s\times s\) minor \(\Delta\) satisfies

\[
|\Delta|\le s!\prod_{j=1}^s(M_j-1)
<s!|P|.                                                   \tag{1}
\]

Therefore

\[
|P|\ge\frac{|\Delta|}{s!}.                                \tag{2}
\]

This elementary lemma converts inverse-symmetrized determinant growth into
an additive-container cost.

## 5. The exact threshold condition

Let \(T\) be the relevant unit-word parameter set.  If a linear-size
selection of inverse-symmetrized shifts has a minor satisfying

\[
\frac{|\Delta|}{s!}\ge |T|^{5/2+\eta}                    \tag{3}
\]

for some fixed \(\eta>0\), then (2) gives

\[
|T|\le |P|^{1/(5/2+\eta)}
=|P|^{2/5-\delta(\eta)}.                                 \tag{4}
\]

Thus (3) rules out the required \(n^{2/5}\) parameter count inside the
proper integral-box ansatz.  The exponent \(5/2\) is the exact boundary
dual to \(2/5\).

Equation (3) is an additional condition, not a proved universal theorem.

## 6. Weakest credible conjecture

**Inverse-symmetrized determinant conjecture.**  In a bounded-index
integral/fractional-ideal coordinate lattice, a controlled-height,
growing-rank family of multiplicatively independent non-torsion units has
a linear-size collection among

\[
t+R/t,\qquad t-R/t
\]

whose coordinate minor satisfies (3), unless the units lie in a
quantitatively describable exceptional subfield or norm-torus structure.

Status: **CONJECTURE**.

The qualifications are necessary:

- without inversion, the consecutive-unit family is a counterexample;
- without an integral or bounded-index lattice, rescaling the GAP
  generators can make coordinate determinants meaningless;
- without height control, field-dependent scaling defeats uniformity;
- subfields and norm tori may create genuine low-dimensional exceptions.

## 7. Proof skeleton and falsification plan

A proof would need:

1. a lower bound for a suitable exterior product of logarithmic unit
   vectors, after removing subfield/norm-torus degeneracies;
2. a comparison from logarithmic exterior products to coefficient
   determinants of \(t\pm R/t\);
3. the determinant-volume lemma (1);
4. the threshold comparison (3)--(4).

A falsification search should look for growing-degree fields with many
independent units for which both \(t+R/t\) and \(t-R/t\) have low-rank,
small-determinant coefficient vectors.  Merely finding units in an affine
progression is insufficient: the family above shows that inversion can
restore full rank.

## 8. Reproducibility

```bash
python3 verify_symmetrized_unit_container.py
pytest -q test_verify_symmetrized_unit_container.py
```
