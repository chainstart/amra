# Joint radius--height expansion as an affine-copy problem

Date: 2026-07-29

## Scope

This note tests whether the synchronized coaxial-circle model can be pushed
past the separate radius and height estimates in
`COAXIAL_SYNCHRONIZATION_DICHOTOMY.md`.  It gives exact reductions to unions
of affine copies, proves the general lower bound available from the ordinary
Szemerédi--Trotter theorem, and isolates the additional structural lemma
needed for an exponent improvement.

It does **not** improve the \(3/5\) exponent in Erdős problem 1083.

## 1. Exact anchored affine-copy reduction

Keep the synchronized-circle setup, with \(S\geq2\), and put
\[
 X_\theta=\{2(1-\cos(k\theta)):0\leq k<S\}.
\]
Relabel the circles as \(C_0,\ldots,C_{F-1}\), choosing \(C_0\) so that its
height \(z_0\) is minimal.  Write its radius as \(\rho_0>0\).  For every
circle \(C_i\), set
\[
 a_i=(\rho_i-\rho_0)^2+(z_i-z_0)^2,\qquad
 b_i=\rho_i\rho_0.
\]

### Proposition 1

If \(\Delta^2(P)\) is the set of squared distances of the synchronized point
configuration, then
\[
 \bigcup_{i=0}^{F-1}(a_i+b_iX_\theta)
 \ \subseteq\ \Delta^2(P)\cup\{0\}. \tag{1}
\]
Moreover \(b_i>0\), \(a_i\geq0\), and all parameter pairs
\((a_i,b_i)\) are distinct.

### Proof

For each \(i\) and \(0\leq k<S\), take the point of angle \(k\theta\) on
\(C_i\) and the point of angle zero on \(C_0\).  Their squared distance is
\[
\begin{aligned}
 &\rho_i^2+\rho_0^2-2\rho_i\rho_0\cos(k\theta)
 +(z_i-z_0)^2\\
 &\quad=(\rho_i-\rho_0)^2+(z_i-z_0)^2
       +2\rho_i\rho_0(1-\cos(k\theta))\\
 &\quad=a_i+b_iX_{\theta,k}.
\end{aligned}
\]
This proves (1).  If \(b_i=b_j\), then \(\rho_i=\rho_j\).  Equality
\(a_i=a_j\) then gives \((z_i-z_0)^2=(z_j-z_0)^2\).  Both differences are
nonnegative by the choice of \(z_0\), so \(z_i=z_j\).  The two coaxial
circles would be identical.  Thus distinct circles give distinct parameter
pairs. \(\square\)

Only the reference term \(i=0,k=0\) can be zero.  Hence, for the union \(V\)
in (1), the original nonzero distance count satisfies
\[
 D\geq |V|-1. \tag{2}
\]

## 2. All circle pairs and the exact line-count target

The anchored reduction uses only \(F\) parameter lines.  Retaining all circle
pairs gives a potentially stronger and still exact formulation.  For an
unordered pair \(\{i,j\}\), including \(i=j\), put
\[
 A_{ij}=(\rho_i-\rho_j)^2+(z_i-z_j)^2,\qquad
 B_{ij}=2\rho_i\rho_j.
\]
Let
\[
 {\cal L}=\{(A_{ij},B_{ij}):0\leq i\leq j<F\},\qquad
 M=|{\cal L}|.
\]
For every distinct parameter pair in \({\cal L}\), the squared-distance set
contains the \(S\)-term affine copy
\[
 A_{ij}+B_{ij}\{1-\cos(k\theta):0\leq k<S\}. \tag{3}
\]
Thus \(M\), not the raw \(\binom{F+1}{2}\) circle-pair count, is the correct
quantity: different circle pairs can define exactly the same affine line.

The ordinary Szemerédi--Trotter theorem applied to the \(M\) distinct graph
lines in (3) gives
\[
 D+1\geq c\min\{M,\sqrt{SM}\}. \tag{4}
\]
At
\[
 S=N^{2/5},\qquad F=N^{3/5},
\]
(4) improves \(N^{3/5}\) only if
\[
 M>N^{4/5+\varepsilon}=F^{4/3+(5/3)\varepsilon}. \tag{5}
\]
In particular, the attractive structural target
\[
 M\geq F^{3/2-o(1)} \tag{6}
\]
would give
\[
 D\geq N^{13/20-o(1)},
\]
a \(1/20\) exponent gain.

There is a simple unconditional floor \(M\geq F\).  In a radius class
containing \(n_\rho\) circles, fix its smallest height.  The \(n_\rho\)
squared height differences from that circle are distinct, and all have
slope parameter \(2\rho^2\).  Distinct radii give distinct slopes, so summing
over the radius classes gives \(\sum_\rho n_\rho=F\) distinct lines.

No proof of (5), let alone (6), is currently available in the balanced regime
\(L\asymp m\asymp F^{1/2}\).  A crude multiplicity calculation explains the
gap.  If
\[
 \mu(A,B)=|\{\{i,j\}:(A_{ij},B_{ij})=(A,B)\}|,
\]
then a fixed product \(B=2\rho_i\rho_j\) pairs the \(L\) radii in a matching,
and for each radius pair a fixed squared height difference has at most
\(2m\) realizations.  Hence only
\[
 \mu(A,B)\leq 2Lm
\]
follows immediately, which is \(O(F)\) in the balanced case and yields no
more than \(M\gg F\).

Equivalently, with parameter energy
\[
 {\cal E}=\sum_{A,B}\mu(A,B)^2,
\]
Cauchy--Schwarz gives \(M\gg F^4/{\cal E}\).  Breaking the threshold (5)
requires
\[
 {\cal E}<F^{8/3-\delta}
\]
for some fixed \(\delta>0\), while (6) would follow from
\({\cal E}\leq F^{5/2+o(1)}\).  Proving such an energy estimate, or showing
that high energy forces an independent semiconvex distance expansion, is an
exact all-pairs version of the missing lemma.

There is a useful rigorous separation of the generic-radius regime.  For
each product \(p\), let
\[
 t_p=|\{\{\rho,\sigma\}:\rho\sigma=p\}|,
 \qquad
 E_\times(R)=\sum_p t_p^2,
\]
where the radius pairs are unordered and may repeat a radius.

### Proposition 2 (multiplicative-energy reduction)

With maximum radius multiplicity \(m\),
\[
 {\cal E}\leq 2m^3E_\times(R)
 \quad\hbox{and consequently}\quad
 M\gg \frac{F^4}{m^3E_\times(R)}. \tag{7}
\]

### Proof

Fix two unordered radius pairs \(\{\rho,\sigma\}\) and
\(\{\rho',\sigma'\}\) with the same product.  Equality of the corresponding
intercepts is
\[
 (z-w)^2-(z'-w')^2
 =(\rho'-\sigma')^2-(\rho-\sigma)^2. \tag{8}
\]
After choosing \(z,w,z'\), equation (8) has at most two real choices for
\(w'\).  Each height set has at most \(m\) elements, so these two radius
pairs contribute at most \(2m^3\) ordered solutions.  Summing over the
\(E_\times(R)\) pairs of radius pairs proves the energy bound.  Cauchy--Schwarz
then proves the line-count bound. \(\square\)

In the balanced regime \(L\asymp m\asymp F^{1/2}\), Proposition 2 crosses the
required threshold whenever
\[
 E_\times(R)\leq L^{7/3-\delta}. \tag{9}
\]
Indeed it then gives \(M\gg F^{4/3+\delta/2}\).  In particular, a
multiplicatively Sidon radius set has \(E_\times(R)=O(L^2)\) and gives
\(M\gg F^{3/2}\).  The unresolved case has large multiplicative energy
\(E_\times(R)>L^{7/3-o(1)}\); inverse principles suggest multiplicative
structure in the radii, but turning that structure into extra intercept or
distance expansion is still missing.

This is a genuine structure split: the all-pairs route is already sufficient
for low multiplicative-energy radii, and only the high-energy radius branch
needs a new lemma.  It is not yet an unconditional dichotomy because the
second branch has not been closed.

High multiplicative energy is not by itself a counterexample to (6).  Take
\[
 \rho_u=m2^u,\qquad 0\leq u<L,
\]
and again use heights \(\{0,\ldots,m-1\}\) on every radius.  Products now
depend only on \(u+v\), so \(E_\times(R)\asymp L^3\), its largest natural
scale.  For a fixed product, however, the radial offsets
\((\rho_u-\rho_v)^2\) are distinct as the index gap \(|u-v|\) varies.
They are integer multiples of \(m^2\), whereas all squared height
differences lie in \([0,(m-1)^2]\).  The translated height-difference blocks
are therefore disjoint, and once again
\[
 M=m\binom{L+1}{2}.
\]
Thus the high-energy branch must use the tradeoff between repeated radius
products and diversity of the associated radial offsets; radius-product
energy alone is too coarse to settle it.

For a rigorous benchmark, take multiplicatively Sidon radii
\(\rho_u=2^{3^u}\) and give every radius the common height set
\(\{0,\ldots,m-1\}\).  The products \(\rho_u\rho_v\), \(u\leq v\), are all
distinct, while each radius pair has exactly \(m\) squared height
differences.  Hence
\[
 M=m\binom{L+1}{2}.
\]
When \(L=m\), this is of order \(L^3=F^{3/2}\), so (6) has the right scale
for this balanced model.  It is supporting evidence only, not a universal
lower bound.

## 3. The ordinary anchored incidence bound

For completeness, the anchored version has the following general bound.

### Proposition 3

Let \(X\subset\mathbb R\) have \(S\geq2\) elements, and let
\(\ell_i(x)=a_i+b_i x\), \(1\leq i\leq F\), be distinct affine functions.
If \(V=\bigcup_i\ell_i(X)\), then
\[
 |V|\geq c\min\{F,\sqrt{FS}\}. \tag{10}
\]

### Proof

Every graph line \(\ell_i\) contains \(S\) points of \(X\times V\).
The \(F\) distinct lines therefore have \(FS\) incidences with the
\(S|V|\) Cartesian-product points.  Szemerédi--Trotter gives
\[
 FS\leq C\left((S|V|)^{2/3}F^{2/3}+S|V|+F\right).
\]
The first two terms give respectively
\(|V|\geq c\sqrt{FS}\) and \(|V|\geq cF\); bounded \(S\) is absorbed into
the constant. \(\square\)

At the critical scale, (10) is only \(N^{1/2}\), weaker than both the inherited
bound and the separate semiconvex estimate \(SF^{1/4}=N^{11/20}\).

## 4. A strict two-angular-slice barrier

The two evaluations of an affine function determine it, but that injectivity
alone cannot give more than a square-root bound.

### Proposition 4

Fix \(0=x_0<x_1\).  For every integer \(q\geq2\), there are
\(F=\binom q2\) distinct positive-slope affine functions whose values on
\(\{x_0,x_1\}\) all lie in one \(q\)-element set.  Their parameters can also
be chosen in the anchored geometric form
\[
 a_i=(\rho_i-1)^2+z_i^2,\qquad b_i=\rho_i,
 \qquad \rho_i>0,\ z_i\geq0. \tag{11}
\]

### Proof

For every \(1\leq u<v\leq q\), set \(b_{u,v}=(v-u)/x_1\).  Choose
\(C\geq\max_{u<v}(b_{u,v}-1)^2\) and put \(a_{u,v}=C+u\).  The endpoint
values are \(C+u,C+v\), so their union is exactly
\(\{C+1,\ldots,C+q\}\).  Ordered endpoint values uniquely determine the
function.  Taking \(\rho_{u,v}=b_{u,v}\) and
\[
 z_{u,v}=\sqrt{a_{u,v}-(b_{u,v}-1)^2}
\]
proves (11). \(\square\)

Thus two angular slices are compatible with \(|V|=\Theta(\sqrt F)\), even
under the exact anchored radius--height parametrization.  This does not
control the remaining chord values or distances between non-reference
circles.

## 5. Minimum missing lemmas

For the anchored union, a sufficient strong statement would be
\[
 \left|\bigcup_i(a_i+b_iX_\theta)\right|
 \geq S F^{1/2-o(1)}, \tag{AC}_{1/2}
\]
which gives \(N^{7/10-o(1)}\).  More minimally, a bound
\[
 |V|\geq S F^{\beta-o(1)}
\]
has critical exponent \(2/5+3\beta/5\), so any fixed \(\beta>1/3\) would
improve \(3/5\).  The current balanced semiconvex estimate has only
\(\beta=1/4\).

For the all-pairs route, it is enough to prove (5), either directly or through
the parameter-energy alternative above.  This target is weaker than proving
the full anchored affine-copy bound, and is the most concrete next attack.

Any proposed lemma must survive:

1. fixed-radius and fixed-height semiconvex extremizers;
2. the exact two-slice collapse in Proposition 4;
3. balanced multiplicities \(L\asymp m\asymp F^{1/2}\);
4. collisions of parameter lines from different radius pairs;
5. synchronization-extraction losses in the inherited proof tree.

The exact verifier for Proposition 4, the Sidon benchmark, and the exponent
arithmetic is
`verify_affine_copy_barrier.py`.
