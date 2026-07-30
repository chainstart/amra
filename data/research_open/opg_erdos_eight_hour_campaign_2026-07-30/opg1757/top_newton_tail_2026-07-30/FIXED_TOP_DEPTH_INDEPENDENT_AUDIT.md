# Independent red-team audit of the fixed top-depth asymptotic theorem

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS, INCLUDING THE REFINED }b_{k,d}=O_d(k^d)\text{ BOUND}}
\]

The two defects reported in the first audit have been repaired in the
main text: equation (1) now contains the missing plus sign, and the
mixed falling-moment identity is stated explicitly.  The refined
bidegree lemma and its two determinant cancellations also pass.

No counterexample was found to
\[
p_{k,d}=\frac{2^d}{d!}k^{2d}+O_d(k^{2d-1}).
\]
The strengthened conclusion
\[
\boxed{b_{k,d}=O_d(k^d)}
\]
is also justified.  The marked-cycle bidegree, exceptional depths,
elementary-symmetric asymptotic, triangular signs, and leading
constant all survive independent reconstruction.

## 1. Independent combinatorial model

The audit does not import either existing top-tail verifier or its
recorded \(R_{\ell,h}\) polynomials.

For a prescribed matching of size \(h\), contract each prescribed edge
to a vertex of weight two; every other vertex has weight one.  Between
contracted vertices \(i,j\), the original complete graph supplies
\(w_iw_j\) possible edges.  For a block \(B\) of contracted vertices,
the weighted Cayley identity gives
\[
\sum_{\text{trees on }B}\prod_{\{i,j\}\in T}w_iw_j
=
\begin{cases}
1,&|B|=1,\\[1mm]
\left(\prod_{i\in B}w_i\right)
\left(\sum_{i\in B}w_i\right)^{|B|-2},&|B|\ge2.
\end{cases}                                         \tag{B}
\]
Summing products of (B) over set partitions reconstructs
\(U_{h,j}(s)\) exactly.  This supplies a direct combinatorial
implementation independent of the Lagrange-profile code.

For losses \(0\le\ell\le4\), all \(h=0,1,2\), and enough values of
\(j\) to include redundant checks, interpolation from (B) gives
\[
\deg_j R_{\ell,h}\le\ell.
\]
The audit also independently expands the source finite products
through loss six; their symbols agree with the weighted-contraction
counts wherever both apply.

## 2. Marked-cycle inclusion--exclusion

### Endpoint-only contacts do not violate \(v\le e-u\)

Let \(H\) be the union of any selected collection of bad cycles.
Let \(e\) count its nonprescribed edges, \(v\) its nonfixed vertices,
\(f\) its fixed endpoints, \(p\) its prescribed matching edges, and
\(u\) the number of marked pairs having at least one endpoint in
\(H\).

Every connected component of a union of selected cycles has at least
as many edges as vertices.  Hence
\[
e+p\ge v+f.
\]
For each touched pair:

- one endpoint and no prescribed edge contributes \(f_i-p_i=1\);
- two endpoints and no prescribed edge contribute \(2\); and
- two endpoints together with the prescribed edge contribute \(1\).

Thus \(f-p\ge u\), and
\[
\boxed{v\le e-(f-p)\le e-u.}
\]
This proof is unaffected by:

- cycles containing one or two prescribed edges;
- several cycles sharing paths or vertices;
- nonprescribed edges joining two fixed endpoints; or
- disconnected unions of cycles.

In particular, a cycle may touch a marked endpoint without using its
prescribed edge; this is the first bullet and still spends one unit of
\(e-v\).  The audit generated 4,000 deterministic random unions of
overlapping cycles with \(h=0,1,2\), plus targeted equality examples
of all three types above.  None violated \(v\le e-u\).

### Degree accounting

Embedding the \(v\) free core vertices contributes degree \(v\) in
\(s\).  Fixing its \(e\) nonprescribed edges consumes \(e\) of the
chosen edge slots and contributes degree at most \(e\) in \(j\).
Selecting the \(u\) touched pairs contributes degree at most \(u\) in
\(h\).  Relative to \(s^{2j}\), the core loss is
\[
\delta=2e-v\ge e+u.
\]
The remaining edge selection at loss \(\ell-\delta\) has
\((j,h)\)-total degree at most \(\ell-\delta\).  Thus the total is at
most
\[
e+u+\ell-\delta\le\ell.
\]
Moreover \(e+u\le\delta\le\ell\).  There are
only finitely many cycle-union multitypes for each such \(e\);
inclusion--exclusion multiplicities depend on the finite core and add
no \(j\)- or \(h\)-degree.

The embedding factor is of the form
\((s-\alpha h-\beta)_{\underline v}\).  Choosing a factor involving
\(h\) spends at least one additional power of \(s\) for each added
\(h\)-degree.  The unrestricted edge-binomial part has the same
property: choosing \(-h\) instead of the quadratic \(s^2\) term spends
two powers of \(s\) while adding one degree in \(j\) and one in \(h\).

Therefore
\[
\deg_j[h^r]R_{\ell,h}(j)\le\ell-r.
\]
Independent weighted-contraction calculations verify this bidegree
for losses \(0,\ldots,3\), including redundant \(j\)- and \(h\)-values.

## 3. Refined determinant cancellation and \(b_{k,d}\)

If the total profile loss is \(L=d+4\), every product in (10) has
joint degree at most \(L\) in the two variables \(J,k-J\).
The bidegree result permits the decomposition
\[
R_{\ell,h}(j)
=A_\ell(j)+C_\ell(j)+hB_\ell(j)
+O_{\deg_j}(\ell-2),
\]
where \(A_\ell\) is the \(h\)-independent homogeneous degree-\(\ell\)
part.  At \(j\)-degree \(\ell-1\), the \(h^0\) part is \(C_\ell\)
and the \(h^1\) part is \(hB_\ell\).  Every \(h^r\), \(r\ge2\), has
\(j\)-degree at most \(\ell-2\).  Thus this decomposition contains
every term capable of contributing at total degrees \(L\) or \(L-1\);
no omitted term can reach those degrees.

In
\[
R_{\ell,1}(J)R_{L-\ell,1}(k-J)
-R_{\ell,0}(J)R_{L-\ell,2}(k-J),
\]
the degree-\(L\) term \(A_\ell A_{L-\ell}\) cancels pointwise.  At
degree \(L-1\), both independent \(C\)-terms cancel pointwise, leaving
\[
\sum_{\ell=0}^L\left[
B_\ell(J)A_{L-\ell}(k-J)
-A_\ell(J)B_{L-\ell}(k-J)
\right].                                             \tag{C}
\]
Under \(J\mapsto k-J\) and
\(\ell\mapsto L-\ell\), expression (C) changes sign.  The
\({\rm Bin}(k,\tfrac12)\) law is invariant under that map, so its
expectation is exactly zero.  For even \(L\), the middle
\(\ell=L/2\) term is itself antisymmetric; it is not an exception.

The remaining integrand has total degree at most \(L-2\).  Expanding
it in mixed falling factorials and using the now-displayed identity
\[
\mathbb E[(J)_{\underline a}(k-J)_{\underline b}]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}}
\]
shows that its expectation has \(k\)-degree at most \(L-2\).  Division
by \(2k(k-1)\) yields
\[
\boxed{b_{k,d}=O_d(k^{L-4})=O_d(k^d).}
\]

The independent verifier checks the mixed identity for 765 parameter
combinations.  It also rebuilds the exact profile kernels without
stored symbols for \(L=4,5,6\), verifies pointwise cancellation at
degree \(L\), verifies antisymmetry at degree \(L-1\), and confirms
that the expectation has degree at most \(L-2\).

## 4. Exceptional depths \(d=1,2\)

Using independently reconstructed finite profiles through total losses
five and six, followed by an independent binomial expectation, gives
symbolically
\[
\boxed{b_{k,1}=k-2,}
\qquad
\boxed{b_{k,2}=(k-2)(k-21).}
\]
These are exact polynomial identities, not fits in \(k\).

They imply
\[
b_{k,1}=O(k)=O(k^{2\cdot1-1}),
\]
and
\[
b_{k,2}=O(k^2)=O(k^{2\cdot2-1}).
\]
For \(d\ge3\), \(d+2\le2d-1\); \(d=0\) is separately
\(b_{k,0}=1\).  Hence all exceptional cases used in (14) are covered.

As a second check, the weighted-contraction model reconstructs the
complete \(c_k(s)\) polynomials for \(2\le k\le6\) and reproduces both
exceptional formulas exactly.

## 5. Elementary symmetric leading term

For \(q=2k+O(1)\), let
\[
P_\nu(q)=\sum_{x=4}^{q+3}x^\nu.
\]
Then
\[
\deg_kP_\nu=\nu+1.
\]
Newton's identities express \(E_r\) as a sum indexed by partitions
\(r=\sum\nu m_\nu\).  The corresponding \(k\)-degree is
\[
\sum_\nu(\nu+1)m_\nu
=r+\sum_\nu m_\nu.
\]
It equals \(2r\) only for \(m_1=r\).  Every term containing a power
sum \(P_\nu\) with \(\nu\ge2\) has degree at most \(2r-1\).  Since
\[
P_1(q)=2k^2+O(k),
\]
the unique leading contribution is
\[
\frac{P_1(q)^r}{r!}
=\frac{2^r}{r!}k^{2r}+O_r(k^{2r-1}).
\]
Thus (15) has the stated positive sign and coefficient.

Independent exact symmetric-polynomial interpolation verifies this
coefficient through \(r=12\) and five different offsets in
\(q=2k+O(1)\).

## 6. Triangular recurrence and sign

Because
\[
(s-4)_{\underline q}
=\prod_{\nu=4}^{q+3}(s-\nu)
=\sum_r(-1)^rE_r(q)s^{q-r},
\]
the sign in (17), and hence in (18), is
\((-1)^{d-i}\).  Solving the triangular system gives
\[
p_{k,d}
=b_{k,d}
-\sum_{i=0}^{d-1}
p_{k,i}(-1)^{d-i}E_{d-i}(m-i).
\]
The \(b_{k,d}\) term is absorbed into
\(O_d(k^{2d-1})\).  At leading order,
\[
-2^d\sum_{i=0}^{d-1}
\frac{(-1)^{d-i}}{i!(d-i)!}.
\]
Since the full alternating binomial sum is zero, the truncated sum is
\(-1/d!\).  The two minus signs therefore give
\[
\boxed{[k^{2d}]p_{k,d}=\frac{2^d}{d!}>0.}
\]

The independent verifier:

- checks the triangular identity directly against base-four finite
  differences for exact \(c_k(s)\);
- reconstructs the recurrence without stored top-tail formulas; and
- verifies \(2^d/d!\) through \(d=12\).

No sign reversal or off-by-one root was found.

## 7. Secondary review of growing-top-window Lemma 2

`GROWING_TOP_WINDOW_THEOREM.md` uses the refined cancellation with
coefficient norms retained as the loss \(j\) grows.  No contradiction
was found.

- The arithmetic-progression elementary symmetric coefficients in
  (8) can be bounded through Newton identities and Faulhaber power
  sums by \(\exp(O(\ell\log\ell))\).
- Identity (9) is exact: it follows by differentiating
  \((2+x)^r\) \(v\) times and setting \(x=-1\).
- Power/falling-factorial conversions of order at most \(2\ell\),
  together with \(O(\ell^2)\) truncated convolutions, fit inside the
  deliberately larger
  \(\exp(O(\ell^2\log\ell))\) envelope.
- The degree-\(L\) and degree-\((L-1)\) cancellations are exactly the
  two cancellations audited above.  Removing them cannot increase the
  coefficient norm.
- For \(k\ge2(j+5)\), division by \(2k(k-1)\) converts the remaining
  \(k^{j+2}\) numerator bound to \(k^j\).

Thus Lemma 2 is sufficient for its stated coarse exponential constant.
For publication clarity, equation (12) could be replaced by, or
supplemented with, the mixed moment (14) from the fixed-depth note;
expanding \(k-J\) first makes the displayed marginal identity
sufficient, but obscures the norm bookkeeping.  This is a presentation
recommendation, not a logical failure.

## 8. Final assessment

The repaired and strengthened main theorem passes independent audit:

- endpoint-only marked-pair contacts satisfy \(v\le e-u\);
- the bidegree lemma yields the stated \(A+C+hB\) decomposition;
- every possible degree-\(L\) term cancels pointwise;
- the complete degree-\((L-1)\) term is antisymmetric in expectation;
- \(b_{k,d}=O_d(k^d)\) follows; and
- the original fixed-top asymptotic and eventual positivity remain
  valid.

No further repair is required by this audit.

## 9. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/top_newton_tail_2026-07-30
pytest -q test_independent_verify_fixed_top_depth.py
python3 independent_verify_fixed_top_depth.py
```
