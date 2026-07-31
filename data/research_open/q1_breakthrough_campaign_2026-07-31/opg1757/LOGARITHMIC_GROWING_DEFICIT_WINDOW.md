# OPG-1757: a logarithmically growing positive deficit window

Date: 2026-07-31

Status: `PROVISIONAL__CONDITIONAL_ON_UNIFORM_HEIGHT_LEMMA`

## 1. Result

Conditional on the uniform height lemma (3), there are absolute constants
\(c_0>0\) and \(s_0\) such that, for every
integer \(s\ge s_0\) and every integer
\[
0\le q\le c_0\frac{\log s}{\log\log s},
\tag{1}
\]
every coefficient in the natural support of the complete-split pooled
disjoint-core layer satisfies
\[
\boxed{
 [\beta^{2n+r}]B_{2s-5-q}(s,\beta)>0
 \qquad(0\le r\le2q).
}
\tag{2}
\]
Thus proving (3) with a fully explicit, class-by-class accounting would
make the fixed-deficit theorem uniform in a window whose width tends to
infinity.  No fixed \(q=7,8,\ldots\) interpolation enters this reduction.

## 2. Uniform height lemma

For a rational polynomial \(P(s)=\sum_jp_js^j\), put
\[
\|P\|_1=\sum_j|p_j|.
\]
The missing publication-grade lemma is the assertion that there is an
absolute constant \(K\ge2\) such that, simultaneously for all
\(q\ge1\) and \(0\le r\le2q\),
\[
\boxed{
\|C_{q,r}\|_1\le(Kq)^{Kq}.
}
\tag{3}
\]

Here is the current size ledger.  It identifies the correct scale but does
not yet enumerate every endpoint/profile class with explicit uniform
constants.  In the zero-, one-, and two-marked
coefficient formulas of `ENDPOINT_POLYNOMIALITY_THEOREM.md`, every
endpoint used at deficit \(q\) has
\[
e+c\le q+2.
\tag{4}
\]
For fixed \([u^e]\):

- the exponential in \(\Phi-t\) is indexed by a partition of at most
  \(e\), hence by at most \(2^{O(q)}\) records;
- distributing excess among at most \(c\) copies of \(V\), and choosing
  the linear or quadratic zero-excess term in each copy, produces at most
  \(2^{O(q)}\) records;
- the boundary or marked-path factor contributes at most \(e+1\) choices;
- every resulting \(t\)-degree is \(O(q)\), uniformly in the endpoint
  profile.

All scalar EGF coefficients have absolute value at most
\(\exp(O(q\log q))\); their factorial denominators only decrease this
bound.  Coefficient
extraction replaces a monomial \(t^d\) by a shifted falling factorial
\((s-a)_d\), where \(a\in\{1,2,4\}\) and \(d=O(q)\).  Its coefficient
norm obeys
\[
\|(s-a)_d\|_1
\le\prod_{j=0}^{d-1}(1+a+j)
\le(Kq)^{Kq}.
\tag{5}
\]
The termwise nonnegative \(s\)-valuation proved in the polynomiality
theorem adds only a monomial factor.  Hence every endpoint polynomial
needed at deficit \(q\) has norm at most \((Kq)^{Kq}\), after enlarging
the absolute \(K\).

The fixed-deficit master formula contains only:

- \(O(q)\) overlap choices;
- polynomially many excess/component splittings;
- binomial factors at most \(2^{q+1}\);
- two falling factorials of degree at most \(q+1\); and
- a product of two endpoint polynomials.

Using
\[
\|PQ\|_1\le\|P\|_1\|Q\|_1,
\qquad
\|P+Q\|_1\le\|P\|_1+\|Q\|_1,
\]
and enlarging \(K\) once more is expected to prove (3).  To promote this
to a theorem, the suppressed \(O(q)\) degrees, record multiplicities, and
scalar coefficient bounds must be replaced by an explicit uniform table
for every marked-endpoint class.  Until that audit is supplied, (3) and
the growing window remain conditional.

## 3. Dominance of the positive leading symbol

The endpoint polynomiality theorem and the leading-symbol theorem give
\[
C_{q,r}(s)=L_{q,r}s^{2q}+\text{lower powers},
\]
where
\[
L_{q,r}=\frac4{q!}[z^r](1+2z+2z^2)^q
\ge\frac4{q!}\ge4q^{-q}.
\tag{6}
\]
For \(s\ge2\), equations (3) and (6) imply
\[
\left|C_{q,r}(s)-L_{q,r}s^{2q}\right|
\le2(Kq)^{Kq}s^{2q-1}.
\tag{7}
\]
Consequently there is an absolute \(K_1\) such that all offsets are
strictly positive whenever
\[
s\ge(K_1q)^{K_1q}.
\tag{8}
\]
The inherited stable-range condition \(s\ge6q+4\) is absorbed by (8)
after changing \(K_1\).

Finally, conditional on (3), choose \(c_0>0\) sufficiently small in terms
of \(K_1\).  If
\(q\le c_0\log s/\log\log s\), then
\[
K_1q\log(K_1q)<\log s
\]
for all sufficiently large \(s\), so (8) holds.  This proves the
conditional implication (3) \(\Longrightarrow\) (1)--(2).

## 4. Scope firewall

Once (3) is completed, the constant \(c_0\) will be absolute and
effectively extractable; it has not been optimized.  The proposed result
does not reach polynomial, linear, or full deficit width.  It also does
not prove the complete-split Rayleigh statement outside the disjoint-core
\(\alpha^2\) pooled layer, or arbitrary-host OPG-1757.
