# A critical anisotropic-grid barrier for the coaxial affine-line route

Date: 2026-07-30

## Result and exact scope

This note red-teams the proposed unconditional line-count input
\[
M\ge F^{4/3+\varepsilon}
\]
in the synchronized coaxial-fibre branch of Erdős problem 1083.  It gives
an explicit integer Euclidean configuration with
\[
M=\Theta(F^{4/3})
\]
and parameter energy \(\Theta(F^{8/3})\).  Thus neither a pointwise
multiplicity argument nor a universal improvement of the parameter-line
count can cross the inherited exponent.

This is an obstruction to that proof interface, not an \(N\)-point
counterexample with only \(N^{3/5}\) distances.  A theorem exploiting the
union of the affine copies, rather than only their number, may still
expand this configuration.

## 1. The construction

Fix integers \(L,m\ge1\) and \(q\ge2\).  Use the \(L\) radii
\[
\rho_u=mq^u,\qquad 0\le u<L,
\]
and put the same height set
\[
Z_u=\{0,1,\ldots,m-1\}
\]
on every radius.  This gives \(F=Lm\) coaxial circles.

For an unordered radius pair \(u\le v\), its product parameter and radial
offset are
\[
B_{uv}=2m^2q^{u+v},\qquad
C_{uv}=m^2(q^u-q^v)^2.
\]
The corresponding intercept set is
\[
C_{uv}+\{0^2,1^2,\ldots,(m-1)^2\}.                 \tag{1}
\]

## 2. Exact line count

### Theorem 1

For the construction above,
\[
\boxed{M=m\binom{L+1}{2}.}                         \tag{2}
\]

### Proof

Pairs with different \(u+v\) have different \(B\).  For fixed \(u+v\),
the radial offsets \(C_{uv}\) are distinct integers divisible by \(m^2\).
Indeed the product \(q^{u+v}\) together with
\((q^u-q^v)^2\) determines
\[
(q^u+q^v)^2=(q^u-q^v)^2+4q^{u+v},
\]
and hence the unordered pair \(\{q^u,q^v\}\).

Consequently two distinct offsets with the same \(B\) differ by at least
\(m^2\).  Every squared height difference in (1) lies in
\([0,(m-1)^2]\), so these blocks are disjoint.  Each radius pair therefore
contributes exactly \(m\) lines, and there are \(\binom{L+1}{2}\) unordered
radius pairs. \(\square\)

When \(L,m\ge2\), the maximum multiplicity of one parameter line is only
\[
\max\{m,2(m-1)\}=2(m-1)\quad(m\ge2).                \tag{3}
\]
Thus the obstruction is not caused by one giant line class.

## 3. Exact parameter energy

Let \(\mu(A,B)\) count unordered circle pairs producing \((A,B)\), including
self-pairs, and put
\[
\mathcal E=\sum_{A,B}\mu(A,B)^2.
\]
Write
\[
\Sigma_2(m)=\sum_{r=1}^{m-1}r^2
            =\frac{(m-1)m(2m-1)}6.
\]

### Theorem 2

\[
\boxed{
\mathcal E
=L\bigl(m^2+\Sigma_2(m)\bigr)
 +
 \binom L2\bigl(m^2+4\Sigma_2(m)\bigr).
}                                                       \tag{4}
\]

### Proof

For a same-radius pair, height difference \(0\) has multiplicity \(m\),
and positive difference \(d\) has multiplicity \(m-d\).  Its energy is
\(m^2+\Sigma_2(m)\).

For two distinct radii, difference \(0\) again has multiplicity \(m\),
while positive difference \(d\) has multiplicity \(2(m-d)\), according
to its sign.  Its energy is \(m^2+4\Sigma_2(m)\).  The blocks proved
disjoint in Theorem 1, so their energies add. \(\square\)

## 4. The exact critical specialization

Set
\[
L=t,\qquad m=S=t^2.
\]
Put the same synchronized angular pattern of length \(S\) on every circle.
Then
\[
F=Lm=t^3,\qquad N=FS=t^5,
\]
while Theorems 1 and 2 give
\[
M=t^2\binom{t+1}{2}=\Theta(t^4)=\Theta(F^{4/3}),
\]
\[
\mathcal E=\Theta(t^8)=\Theta(F^{8/3}).            \tag{5}
\]

All three previously available mechanisms now land exactly at the inherited
scale:
\[
\sqrt{SM}=\Theta(t^3)=\Theta(N^{3/5}),             \tag{6}
\]
\[
S\sqrt m=t^3=N^{3/5},                              \tag{7}
\]
\[
\frac F{\log F}=N^{3/5-o(1)}.                      \tag{8}
\]

Therefore:

> No universal theorem of the form
> \(M\ge F^{4/3+\varepsilon}\), with fixed \(\varepsilon>0\), can hold
> even for integer geometric-progression radii and identical interval
> height sets.

Likewise, the desired energy estimate
\(\mathcal E\le F^{8/3-\varepsilon}\) is false at the exact threshold.

## 5. Strongest surviving off-critical theorem

The same family gives a sharp positive dichotomy away from its critical
anisotropy.  Parameterize
\[
m=F^{\alpha+o(1)},\qquad L=F^{1-\alpha+o(1)}.
\]
Equation (2) gives
\[
M=F^{2-\alpha+o(1)}.
\]
At the inherited synchronized scale
\(S=N^{2/5+o(1)}\), \(F=N^{3/5+o(1)}\), the all-pairs incidence route gives
\[
D\gg\sqrt{SM}
 =N^{\,4/5-(3/10)\alpha-o(1)},                    \tag{9}
\]
while the equal-radius route gives
\[
D\gg S\sqrt m
 =N^{\,2/5+(3/10)\alpha-o(1)}.                    \tag{10}
\]
Combining them,
\[
\boxed{
D\gg
N^{\,3/5+(3/10)|\alpha-2/3|-o(1)}.
}                                                       \tag{11}
\]

Hence if
\[
|\alpha-2/3|\ge\delta
\]
for a fixed \(\delta>0\), this structured branch yields the genuine gain
\[
D\gg N^{3/5+3\delta/10-o(1)}.                    \tag{12}
\]
The exponent calculation is exact, and the critical value
\(\alpha=2/3\) is the unique point where the two mechanisms meet without
a fixed saving.

## 6. Consequence for the main proof tree

The affine-line-count interface alone cannot give an unconditional
improvement of \(f_3(N)\): the actual synchronized branch may lie at
\[
L=N^{1/5+o(1)},\qquad
m=S=N^{2/5+o(1)}.
\]
At this node a successful proof must use information discarded by \(M\)
and \(\mathcal E\), for example:

1. expansion of the full union
   \(\bigcup(A_{ij}+B_{ij}X_\theta)\);
2. a theorem showing that the inherited joint-correlation hypotheses
   forbid this critical anisotropy;
3. additional cross-angle distances in the explicit grid; or
4. a common-pattern extraction with strength beyond mere synchronized
   interval heights.

Equation (11) is the strongest fixed-gain statement obtainable from the
two existing mechanisms on this extremal family.  It reconnects to the
original distance exponent, but it deliberately does not claim that the
inherited proof always avoids the critical window.

## 7. A positive nonresonant-angle theorem

The critical grid defeats a universal lower bound for \(M\), but an
arithmetic property of the angular progression can still force a fixed
gain.

### Theorem 3 (2-adic angular escape)

Use the \(m\) coaxial circles of common radius \(m\), with heights
\(\{0,\ldots,m-1\}\), and put the same angular progression
\[
\{0,\theta,\ldots,(S-1)\theta\}
\]
on them.  If \(\cos\theta=3/4\), then the number of nonzero distances is
at least
\[
\boxed{
m\max\{0,S-1-2v_2(m)\}.
}                                                       \tag{13}
\]

### Proof

Let \(T_k\) be the \(k\)-th Chebyshev polynomial.  We claim that, for every
\(k\ge1\),
\[
T_k(3/4)=\frac{a_k}{2^{k+1}},\qquad a_k\ \text{odd}.      \tag{14}
\]
The cases \(k=1,2\) are \(3/4\) and \(1/8\).  If (14) holds in two
consecutive degrees, the recurrence
\[
T_{k+1}(3/4)=\frac32T_k(3/4)-T_{k-1}(3/4)
\]
has numerator \(3a_k-4a_{k-1}\), which is odd, over \(2^{k+2}\).
This proves (14).

Consequently
\[
1-\cos(k\theta)
=1-T_k(3/4)
=\frac{b_k}{2^{k+1}},\qquad b_k\ \text{odd}.              \tag{15}
\]
On their common radius \(m\), squared distances with height difference
\(d\in\{0,\ldots,m-1\}\) and angular difference \(k\) are
\[
d^2+2m^2(1-\cos(k\theta)).                               \tag{16}
\]
For \(k>2v_2(m)\), every number in (16) has reduced denominator exactly
\[
2^{k-2v_2(m)}.
\]
Adding the integer \(d^2\) cannot change that denominator.  Thus the
sets belonging to different such \(k\)'s are disjoint.  For fixed \(k\),
the \(m\) values \(d^2\) are distinct.  There are
\(\max\{0,S-1-2v_2(m)\}\) usable values of \(k\), proving (13).
\(\square\)

At the critical specialization \(m=S=t^2\), (13) gives
\[
D\ge t^2\bigl(t^2-O(\log t)\bigr)
   =N^{4/5-o(1)}.                                        \tag{17}
\]
This is a fixed \(1/5\) gain over the inherited exponent inside this
explicit angular subcase.  It does not solve the common-axis branch,
because the inherited extraction does not supply \(\cos\theta=3/4\) or
an analogous denominator-growth hypothesis.  It identifies a precise
surviving target: prove expansion for nonresonant angular progressions,
then classify the complementary bounded-denominator/resonant angles.

### Theorem 4 (odd-prime rational-angle escape)

Use the same \(m\) circles of common radius \(m\).  Suppose
\(\cos\theta=a/b\) in lowest terms, \(|a|<b\), and an odd prime \(p\)
divides \(b\).  Write \(e=v_p(b)\).  Then
\[
\boxed{
D\ge
m\max\left\{0,S-1-\left\lfloor\frac{2v_p(m)}e\right\rfloor\right\}.
}                                                       \tag{18}
\]

Indeed, for \(k\ge1\), the leading-term expansion of the Chebyshev
polynomial is
\[
T_k(x)=2^{k-1}x^k+
\sum_{j\ge1}c_{k,j}x^{k-2j},
\qquad c_{k,j}\in\mathbb Z.                            \tag{19}
\]
After substituting \(a/b\) and taking denominator \(b^k\), every term
except the leading one has a factor \(b^{2j}\).  Modulo the odd prime
\(p\), the numerator is therefore
\(2^{k-1}a^k\ne0\).  It follows that
\[
v_p(1-T_k(a/b))=-ek.                                   \tag{20}
\]
For the distances in (16), multiplication by \(2m^2\) changes this
valuation to \(2v_p(m)-ek\).  Whenever this is negative, adding the
integer \(d^2\) preserves it.  Different \(k\)'s therefore give
disjoint \(m\)-element distance sets.  Counting the eligible \(k\)'s
proves (18).

In particular, at \(m=S=t^2\), every fixed rational cosine covered by
Theorem 3 or 4 gives
\[
D\ge N^{4/5-o(1)}.
\]
Thus the explicit critical line-count extremizer survives only if its
angular structure is substantially more resonant than these rational
families.  This is still a subcase theorem: the inherited branch does
not force a rational cosine.

## 8. Exact full-union pressure test

The line-count extremizer need not extremize the full affine union.  As a
falsification experiment, the verifier takes rational values
\[
\cos\theta=\frac{h-1}{h},\qquad2\le h\le20,
\]
computes all \(S=t^2\) values \(1-T_k(\cos\theta)\) by the exact Chebyshev
recurrence, rejects repeated angular values, and counts
\[
\bigcup_{A,B}\{A+B(1-\cos(k\theta)):0\le k<S\}
\]
with rational arithmetic.  The smallest counts found are

The displayed full-union count includes the value \(0\); the number of
nonzero distances is therefore exactly one smaller in each row.

| \(t\) | \(N=t^5\) | \(M\) | smallest full union | \(\cos\theta\) |
|---:|---:|---:|---:|---:|
| 2 | 32 | 12 | 32 | \(1/2\) |
| 3 | 243 | 54 | 441 | \(3/4\) |
| 4 | 1024 | 160 | 2281 | \(3/4\) |
| 5 | 3125 | 375 | 8900 | \(3/4\) |

These finite data prove nothing asymptotic, but they show that the explicit
barrier is specific to the statistic \(M\): its full affine union already
greatly exceeds the critical \(t^3=N^{3/5}\) scale in every tested
nonperiodic angular progression.  A plausible surviving route is therefore
a special expansion theorem for this affine union at the critical
anisotropy, not another lower bound for \(M\).

## Reproduction

```bash
python3 verify_critical_anisotropic_grid.py
pytest -q test_critical_anisotropic_grid.py
```
