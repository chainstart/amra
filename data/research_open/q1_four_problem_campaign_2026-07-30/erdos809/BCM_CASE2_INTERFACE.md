# Closing the BCM-style \(k=3\) Case-2 induction step

## 1. Uniform form of the near-Dirac theorem

Theorem A in `NEAR_DIRAC_C7_THEOREM.md` is equivalent to the following
uniform statement.

**Corollary 1.**  For every \(\xi>0\), there are
\(\eta=\eta(\xi)>0\) and \(n_0=n_0(\xi)\) such that every \(n\ge n_0\)
vertex graph \(G\) satisfying
\[
e(G)>\lfloor n^2/4\rfloor,\qquad
\delta(G)\ge(1/2-\eta)n
\]
uses at least
\[
(1/8-\xi)n^2
\]
colours in every edge-colouring for which all \(C_7\)'s are rainbow.

To see the equivalence, suppose the uniform statement failed for one
\(\xi\).  Choose successively counterexamples with
\(\eta=1/j\) and orders tending to infinity.  They form a sequence with
\(\delta=n/2-o(n)\), contradicting Theorem A.

## 2. The induction potential

Fix a desired final error \(\varepsilon>0\).  As in BCM26, consider
\[
g(n,e)
=\frac e2+\frac n2\sqrt{e-\frac{n^2}{4}}
-\varepsilon n^2-C_\varepsilon,                               \tag{21}
\]
where the constant only handles the finite base range.

Apply Corollary 1 with
\[
\xi=\varepsilon/4,
\]
and let \(\eta_0\) be the resulting minimum-degree tolerance.  Choose a
fixed \(\kappa>0\) so small that
\[
2\kappa<\eta_0,\qquad
\frac{\kappa+\kappa^2}{2}<\frac{\varepsilon}{4}.               \tag{22}
\]

Use the density split
\[
e<\left(\frac14+\kappa^2\right)n^2                            \tag{23}
\]
for Case 2.  The use of \(\kappa\), rather than BCM26's convenient
\(\varepsilon^3\), is only a hierarchy choice.

## 3. Minimum degree after the deletion alternative fails

The exact algebra in BCM26 does not use \(k\) at this stage.  If deleting
a minimum-degree vertex and invoking the induction hypothesis does not
already prove \(f(n,e,C_7)\ge g(n,e)\), then
\[
\delta>
\frac n2-\sqrt{e-\frac{n^2}{4}}-\frac12.                      \tag{24}
\]
Under (23),
\[
\delta>(1/2-\kappa)n-\frac12
\ge(1/2-2\kappa)n
\ge(1/2-\eta_0)n                                               \tag{25}
\]
for all sufficiently large \(n\).

Corollary 1 therefore gives
\[
f(n,e,C_7)\ge(1/8-\varepsilon/4)n^2.                           \tag{26}
\]

## 4. Comparison with the required potential

Condition (23) gives
\[
\frac e2
<\left(\frac18+\frac{\kappa^2}{2}\right)n^2,
\]
and
\[
\frac n2\sqrt{e-\frac{n^2}{4}}
<\frac{\kappa}{2}n^2.
\]
Equations (21)--(22) imply
\[
g(n,e)
<\left(\frac18-\frac{3\varepsilon}{4}\right)n^2-C_\varepsilon.
                                                                    \tag{27}
\]
The lower bound (26) is strictly larger.  Thus the \(k=3\) Case-2
induction step closes.

## 5. Exact conclusion and boundary

The package now supplies a complete self-contained substitute for the
unwritten \(k=3\) stability argument mentioned by BCM26 in their second
case.  It does not touch the complementary range
\[
e\ge\left(\frac14+\kappa^2\right)n^2,
\]
where the induction only forces
\[
\delta\gtrsim
\frac n2-\sqrt{e-\frac{n^2}{4}}.
\]
That linearly low-minimum-degree Case 1 is the sole remaining proof
bottleneck in this route.

The cutoff \(\kappa\) depends on \(\varepsilon\).  Any future Case-1 proof
must carry this hierarchy, but no quantitative rate for
\(\eta(\xi)\) is needed.
