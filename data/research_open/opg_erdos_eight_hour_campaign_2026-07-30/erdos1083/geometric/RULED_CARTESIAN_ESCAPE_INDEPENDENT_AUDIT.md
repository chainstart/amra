# Independent audit of the ruled Cartesian escape theorem

Date: 2026-07-30

Audited file: `RULED_CARTESIAN_ESCAPE_THEOREM.md`

## 1. Verdict

\[
\boxed{\textbf{MAIN INTEGER THEOREM: PASS}}
\]

\[
\boxed{\textbf{REVISED DOCUMENT: PASS WITH SCOPE QUALIFICATION}}
\]

The integer theorem, including its power exponents, is correct.  There is
no zero-value defect.  The denominator \(4\max\tau^2\) is valid, although
the constant \(4\) is not optimal and can be replaced by \(2\).

The earlier failure in Section 2 has been repaired.  The revised text uses
uniform Euclidean scaling by \(D^2\), observes that squared distances scale
by \(D^4\), and requires both the common denominator and the numerators to
have polynomial height.  The direct anchored product argument remains
integral after this scaling, as checked in Section 9 below.

The proof-tree scope statement is appropriately cautious: the theorem
eliminates the exact full integer Cartesian model, but not the complete
ruled branch without an additional stability/extraction theorem.

## 2. Independent reconstruction of the integer proof

Assume
\[
J\subseteq[-T,T]\cap\mathbb Z,\quad
A\subseteq[1,T]\cap\mathbb Z,\quad
Z\subseteq[-T,T]\cap\mathbb Z,
\]
with all three sets nonempty and \(|J|\ge2\).  Nonemptiness of \(A\)
implies \(T\ge1\).

Choose
\[
j_0=\min J,\qquad z_0\in Z,
\]
and put
\[
L=\{j-j_0:j\in J\setminus\{j_0\}\},\qquad
U=Z-z_0.
\]
Because \(j_0\) is the minimum,
\[
\boxed{L\subseteq[1,2T]\cap\mathbb Z.}
\tag{1}
\]
In particular, no element of \(L\) is zero or negative.

For \(a\in A,\ell\in L,u\in U\), compare
\[
(a,(j_0+\ell)a,z_0+u)
\quad\text{and}\quad
(a,j_0a,z_0).
\]
Their squared distance is exactly
\[
(a\ell)^2+u^2.
\tag{2}
\]

### Audit conclusion

This anchoring is valid for every triple \((a,\ell,u)\).  Both points
belong to the original Cartesian product, and (2) supplies a subset of
the full squared-distance set.

## 3. Product-fibre audit

Let
\[
X=A\cdot L.
\]
For \(x\in X\), every representation
\[
x=a\ell,\qquad a\in A,\quad\ell\in L
\]
uses positive integers.  Once the positive divisor \(a\mid x\) is chosen,
\(\ell=x/a\) is fixed.  Therefore
\[
\boxed{
|\{(a,\ell)\in A\times L:a\ell=x\}|
\le\tau(x).
}
\tag{3}
\]
Moreover
\[
1\le x\le2T^2.
\tag{4}
\]
Summing the fibres of the product map gives
\[
\boxed{
|X|\ge
\frac{|A||L|}
{\max_{1\le n\le2T^2}\tau(n)}.
}
\tag{5}
\]

### Verdict

**PASS.**  The positivity of \(A\) and the choice \(j_0=\min J\) are both
essential.  Without either condition, a zero product could occur and
\(\tau(0)\) would be undefined.  Under the stated hypotheses it cannot.

## 4. Sum-of-two-squares fibre audit

Map
\[
X\times U\longrightarrow\mathbb Z_{>0},\qquad
(x,u)\longmapsto x^2+u^2.
\tag{6}
\]
Since \(x\ge1\), every label in (6) is positive even when \(u=0\).

For a positive integer \(n\), the standard ordered signed
representation count is
\[
r_2(n)
=4\sum_{d\mid n}\chi_4(d),
\]
so
\[
\boxed{r_2(n)\le4\tau(n).}
\tag{7}
\]
Every fibre of (6) is a subset of the ordered signed integer
representations counted by \(r_2(n)\).  Hence the bound used in the
audited proof is valid.

There is a small strengthening.  Because \(X\subset\mathbb Z_{>0}\), the
first coordinate is never zero and only the positive half of the
\(x\)-sign pairs can occur.  Thus
\[
|\{(x,u)\in X\times U:x^2+u^2=n\}|
\le\frac{r_2(n)}2
\le2\tau(n).
\tag{8}
\]

### Verdict

**PASS for the claimed \(4\tau(n)\) bound.**  If “exact constant 4” means
“optimal constant”, it is **FAIL**: constant \(2\) is already valid in
this restricted positive-\(x\) problem.  The theorem only needs validity,
not optimality.

## 5. Coordinate-range audit

Equations (1) and the original bounds give
\[
|x|=|a\ell|\le2T^2,\qquad |u|\le2T.
\]
Therefore
\[
x^2+u^2
\le4T^4+4T^2
\le8T^4,
\tag{9}
\]
where the final inequality uses \(T\ge1\).

### Verdict

**PASS.**  The value \(8T^4\) is a safe uniform upper bound.  The sharper
expression is \(4T^4+4T^2\).

## 6. Combination and constant audit

The domain of (6) has size \(|X||U|=|X||Z|\).  Using the audited proof's
weaker but valid fibre bound (7),
\[
|\Delta^2(P)|
\ge
\frac{|X||Z|}
{4\max_{1\le n\le8T^4}\tau(n)}.
\]
Insert (5), use \(2T^2\le8T^4\), and obtain
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{(|J|-1)|A||Z|}
{4\left(\max_{1\le n\le8T^4}\tau(n)\right)^2}.
}
\tag{10}
\]
This is exactly the stated Theorem 1 bound.

Using (8) would improve the denominator in (10) from \(4\) to \(2\).

### Verdict

**PASS.**  The displayed constant \(4\) follows correctly from the two
fibre bounds and the common maximum.  It is safe, not sharp.

## 7. Polynomial-height divisor bound

Let
\[
K=|P(J,A,Z)|=|J||A||Z|.
\tag{11}
\]
The equality holds because \(a>0\): from a point
\((a,ja,z)\), the first and third coordinates recover \(a,z\), while
the ratio of the second to first coordinate recovers \(j\).

Assume
\[
T\le K^C
\]
for one fixed \(C\).  Then
\[
8T^4\le8K^{4C}.
\]
The uniform divisor estimate
\[
\max_{n\le Y}\tau(n)
=\exp\left(O\left(\frac{\log Y}{\log\log Y}\right)\right)
=Y^{o(1)}
\]
gives
\[
\max_{n\le8T^4}\tau(n)^2=K^{o(1)}.
\]
Equation (10) therefore implies
\[
|\Delta(P)|=|\Delta^2(P)|
\ge (|J|-1)|A||Z|K^{-o(1)}.
\tag{12}
\]
Positive distances and positive squared distances are in bijection, so
the equality of the two label counts is valid.

### Verdict

**PASS for asymptotic families with fixed \(C\).**  “Polynomial height”
must mean a uniform fixed polynomial exponent.  Allowing \(C\) to grow
with \(K\) would not justify a \(K^{o(1)}\) loss.

## 8. Critical exponent audit

At
\[
|J|=N^{1/5-o(1)},\qquad
|A||Z|=N^{3/5-o(1)},
\]
one has
\[
(|J|-1)|A||Z|
=N^{4/5-o(1)}.
\]
The subtraction of one is harmless because \(|J|\) grows as a positive
power.  Also
\[
K=|J||A||Z|=N^{4/5-o(1)},
\]
so \(K^{o(1)}=N^{o(1)}\).  Hence
\[
|\Delta(P)|\ge N^{4/5-o(1)}.
\tag{13}
\]

### Verdict

**PASS**, conditional on the explicitly stated polynomial coordinate
range.

## 9. Revised rational-scaling audit

Write the rational parameters with a common positive denominator:
\[
j=\frac{m_j}{D},\qquad
a=\frac{m_a}{D},\qquad
z=\frac{m_z}{D}.
\tag{14}
\]
The revised Section 2 uniformly scales the actual Euclidean coordinates by
\(D^2\):
\[
D^2(a,ja,z)
=(D m_a,m_jm_a,Dm_z)\in\mathbb Z^3.
\tag{15}
\]
This is correct.

More importantly, the product-fibre proof—not merely coordinate
integrality—survives.  For two anchored points with the same \(a\),
the scaled horizontal and vertical differences are
\[
D^2a(j-j_0)=m_a(m_j-m_{j_0}),
\qquad
D^2(z-z_0)=D(m_z-m_{z_0}).
\tag{16}
\]
Both are integers.  The first remains a product of one numerator from the
radial set and one difference of slope numerators, so its fibre is still
bounded by a divisor function.  If \(D\) and every numerator in (14) are
bounded by a fixed power of \(K=|P|\), the integers in (16), and hence
their sums of squares, are also polynomially bounded.  The uniform divisor
loss remains \(K^{o(1)}\).

Uniform coordinate scaling by \(D^2\) multiplies every squared distance by
\(D^4\).  Because this factor is common and nonzero, it preserves the
number of distinct distance labels.

The finite counterexample
\[
j=a=z=\frac12,\qquad D=2
\]
still usefully confirms why \(D\)-scaling would have failed:
\[
D(a,ja,z)=\left(1,\frac12,1\right),
\]
whereas the revised \(D^2\)-scaling gives
\[
D^2(a,ja,z)=(2,1,2).
\]

### Verdict

**PASS after revision.**  The revised quantifiers explicitly require a
single common denominator \(D\) and polynomial bounds on \(D\) and the
numerators.  Independent denominators with a superpolynomial least common
multiple remain correctly excluded.

## 10. Does it eliminate the full ruled branch?

### Exact model from the transfer attack

For
\[
p_{j,a,z}=(a,ja,z),\qquad
j\in\mathcal J_t,\quad1\le a\le t,\quad0\le z<t^2,
\]
take the theorem's height parameter \(T=t^2\).  Then
\[
J\subseteq[-T,T],\quad A\subseteq[1,T],\quad
Z\subseteq[-T,T],
\]
and \(T\) is polynomial in the subgrid size.  The theorem gives
\[
|\Delta(P)|\ge|\mathcal J_t|\,t\,t^2\,t^{-o(1)}
=t^{4-o(1)}.
\]

Thus it **does rigorously eliminate the exact complete integer product
model** used in `CROSS_PLANE_TO_RADIUS_TRANSFER_ATTACK.md`.

### General ruled near-extremizers

It does **not** eliminate all configurations that may arise from a
near-equality inverse theorem.  The theorem additionally requires:

1. one full common product \(J\times A\times Z\);
2. the same radial set \(A\) for every active slope;
3. the same height set \(Z\) for every \((j,a)\);
4. integer coordinates, or a correctly formulated common denominator of
   polynomial size;
5. a retained Cartesian subgrid with the necessary fixed-power sizes.

High cross-plane energy alone currently supplies none of these five
properties.  Sparse products, slope-dependent \(A_j\), fibre-dependent
\(Z_{j,a}\), irrational rulings, or superpolynomial denominator growth
remain outside the theorem.

### Scope verdict

\[
\boxed{
\begin{array}{ll}
\text{exact full ruled Cartesian model:} & \textbf{PASS / excluded},\\
\text{complete ruled branch:} & \textbf{NOT EXCLUDED}.
\end{array}
}
\]

The additional missing hypothesis is precisely a stability extraction:
near saturation of the cross-plane transfer must yield a polynomial-height
Cartesian subgrid retaining fixed powers of \(|J|,|A|,|Z|\), or else give
a fixed incidence saving directly.

## 11. Final disposition

The two required rational-scaling corrections have been made:

1. coordinate scaling is now \(D^2\), with squared-distance scaling
   \(D^4\);
2. the common denominator and numerators are required to have polynomial
   height.

No further correctness change is required.  Two qualifications remain:

1. the stated constant \(4\) is valid but can optionally be strengthened
   to \(2\);
2. the existing warning about the missing stability extraction must remain,
   because the theorem still excludes only a complete polynomial-height
   Cartesian subgrid, not every ruled near-extremizer.
