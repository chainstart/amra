# Resonant multistar convergence audit

## 1. Scope and final outcome

This note asks whether the logarithmic construction from Round 28 can be
upgraded to the required \(n^{2/5}\) average compatibility degree by any
of the natural operations on the same ansatz:

- choosing the box side \(L=L(k)\);
- repeating generators or imposing low-rank integer relations;
- taking additive tensors/products of boxes;
- taking unions of boxes.

The independent-frequency construction is at most logarithmic.  Low-rank
relations do improve it: a rank-three divisor construction attains

\[
\exp\!\left(\Omega\!\left(\frac{\log n}{\log\log n}\right)\right).
\]

This is the correct scale for the lattice-aligned Laurent multistar
ansatz.  The classical maximal order of the divisor function gives the
matching upper bound

\[
\overline d(A)
\le
\exp\!\left((\log 2+o(1))
            \frac{\log n}{\log\log n}\right)
=n^{o(1)}.                                                 \tag{1}
\]

Thus the ansatz still misses \(n^{2/5}\) by a factor

\[
n^{2/5-o(1)}.                                              \tag{2}
\]

The theorem is deliberately scoped.  It covers proper lattice boxes in
Laurent-monomial parameters, their properized repetitions, additive
tensors in algebraically independent frequencies, and unions whose cross
interactions are generic or remain in the same lattice.  It does not claim
a bound for an arbitrary real translation set.

## 2. Variable side length

For the independent-frequency box of Round 28,

\[
n=2L^{2k},\qquad
\overline d(A)=1+k(1-1/L)^2.
\]

Eliminating \(k\) gives

\[
\overline d(A)
=1+
\frac{(1-1/L)^2}{2\log L}\log(n/2).                       \tag{3}
\]

For integer \(L\ge2\), the coefficient in (3) is maximized at \(L=4\).
Allowing \(L=L(k)\) cannot change the order: since \(L\ge2\),
\(k\le\log_2(n/2)/2\), so the gain is always \(O(\log n)\).

## 3. Repetitions do not create new resonances

Repeating a generator does not raise the number of distinct hyperbola
points.  In a set rather than a multiset, \(r\) repeated copies of one
coordinate simply replace a side of length \(L\) by a side of effective
length \(1+r(L-1)\).  After properization:

- the number of distinct resonant parameter orbits is unchanged;
- representation ratios may approach \(1\), but never exceed \(1\);
- the operation is already covered by variable side lengths.

Thus repetitions can improve constants only.

## 4. Why low rank leads to divisors

Continue with the actual SAT hyperbola

\[
(a-3/2-c)(a-3/2+c)=R,\qquad R=-3069.                      \tag{4}
\]

Fix one Laurent frequency \(T\).  A parameter \(t=\lambda T\) gives

\[
\begin{aligned}
u(\lambda)&=\tfrac12(\lambda T+R\lambda^{-1}T^{-1})+\tfrac32,\\
c(\lambda)&=\tfrac12(\lambda T-R\lambda^{-1}T^{-1}).
\end{aligned}                                             \tag{5}
\]

Normalize a rank-three translation lattice with basis

\[
g_1=T/2,\qquad g_2=RT^{-1}/(2N),\qquad g_3=1/2.
\]

For (5) to be a lattice difference, its first two integer coordinates
\(x,y\) satisfy

\[
x y=N.                                                     \tag{6}
\]

Hence the number of distinct same-frequency resonant parameters is at most
the signed divisor count \(2\tau(|N|)\).  If the containing proper box has
first two side lengths \(M_1,M_2\), every supported shift satisfies
\(|x|<M_1\), \(|y|<M_2\), and therefore

\[
|N|<M_1M_2\le |P|\le n.                                  \tag{7}
\]

Equations (6)--(7), followed by the maximal-order divisor bound,
give (1) for one frequency.

This also explains why low-rank rational relations beat the independent
box's logarithm but cannot yield a fixed power.  They compress many curve
points into the factor pairs of one integer; divisor multiplicity is
subpolynomial.

## 5. A matching divisor multistar construction

The upper scale is real, not an artefact of the proof.  Let \(N\) have many
divisors.  Partition its positive divisors into dyadic intervals.  Some
interval \([Z,2Z)\) contains a set \(\mathcal D\) with

\[
|\mathcal D|
\ge \frac{\tau(N)}{1+\log_2N}.                             \tag{8}
\]

Use the rank-three basis above and the box side lengths

\[
M_1=2\max_{x\in\mathcal D}x+1,\quad
M_2=2\max_{x\in\mathcal D}N/x+1,\quad
M_3=7.
\]

For every \(x\in\mathcal D\), put \(y=N/x\).  The two points

\[
(u_x,c_x-Y),\qquad (u_x,-c_x-Y)
\]

are compatible.  Each of their two relevant overlap counts is a fixed
positive proportion of the box size.  With
\(A=P\cup(P-Y)\), the exact overlap calculation gives

\[
\overline d(A)\ge1+\frac{|\mathcal D|}{28}.                \tag{9}
\]

Because the divisors lie in one dyadic interval,

\[
n=2|P|\le210N.                                             \tag{10}
\]

Take a sequence with

\[
\tau(N)=
\exp\!\left((\log2-o(1))
            \frac{\log N}{\log\log N}\right).
\]

Then (8)--(10) attain the scale in (1), up to the harmless
\(\log N\) divisor-bin loss.  Primorials already give the same
\(\exp(\Theta(\log n/\log\log n))\) order and are used in the executable
certificate.

## 6. Tensor/product audit

Let the component boxes use algebraically independent Laurent variables
\(T_1,\ldots,T_q\).  The units of the multivariate Laurent ring are scalar
monomials.  In (4), both factors must be units.  A difference formed as a
sum of independent component differences can therefore be compatible only
when all but one frequency cancel.  Compatibility gains add:

\[
\overline d(A)-1
\le
2\sum_{i=1}^q\tau(|N_i|)+O(q).                            \tag{11}
\]

They do not multiply.  Properness and nontrivial side lengths give
\(q\le O(\log n)\), while every \(|N_i|\le n\).  The extra logarithmic
factor in (11) is absorbed into the \(o(1)\) of (1).

This includes ordinary Minkowski sums and additive tensor encodings.
Introducing a mixed monomial as a new generator merely adds a new
frequency coordinate and is charged in the same way.

## 7. Union audit

For generically separated boxes \(A_i\), cross-box differences contain
independent offsets and do not solve (4), apart from the universal
baseline.  If \(n_i=|A_i|\), their nonbaseline masses satisfy

\[
\frac{\sum_i n_i^2(\overline d(A_i)-1)}
     {(\sum_i n_i)^2}
\le \max_i(\overline d(A_i)-1).                           \tag{12}
\]

Thus a generic union dilutes rather than multiplies the best component
gain.  If the offsets are chosen so cross-box resonances stay in the same
Laurent lattice, properizing the union returns to the divisor bound in
Sections 4--5.  A union with new structured cross interactions outside
that lattice is a genuinely different ansatz and is not covered by this
no-go theorem.

## 8. Reviewable no-go theorem

**Laurent lattice multistar no-go theorem.**  Fix a nondegenerate SAT base
service.  Let \(A\) be obtained from finitely many proper lattice boxes
whose scalable translation-hyperbola factors are Laurent monomials,
allowing:

1. arbitrary integer side lengths, depending on the rank;
2. repeated generators after properization;
3. additive products over algebraically independent frequencies;
4. generic unions, or unions whose cross resonances remain lattice-aligned.

Then

\[
\frac{H_{X,Y}(A)}{|A|^2}
\le
\exp\!\left((\log2+o(1))
            \frac{\log |A|}{\log\log |A|}\right)
=|A|^{o(1)}.                                               \tag{13}
\]

There are rank-three examples attaining
\(\exp(\Omega(\log |A|/\log\log |A|))\).  Consequently no construction
in this ansatz can supply the required \(|A|^{2/5}\) average degree.

The minimal dependencies are:

1. the exact two-layer hyperbola reduction from Round 28;
2. the description of units in a Laurent polynomial ring;
3. elementary proper-box overlap counts and quadratic-mass convexity;
4. the classical maximal-order estimate for \(\tau(N)\).

No incidence theorem, Balog--Szemerédi--Gowers theorem, or sum-product
estimate is used.

## 9. Publication assessment

The following are reusable structural results:

- exact translation-hyperbola energy and its additive-energy capacity;
- the actual-SAT two-layer reduction;
- the distinction between high maximum degree and high average degree;
- the logarithmic proper-box family;
- the sharper divisor multistar family and lattice-ansatz no-go theorem.

Together they form a coherent obstruction section or technical note.
They do not by themselves resolve the original geometric problem and do
not provide the polynomial exponent required for a strong standalone
claim.  A journal submission would need either:

- an application of these lemmas that closes a recognized open case; or
- a theorem extending (13) from Laurent lattice boxes to arbitrary
  high-energy translation sets.

The remaining mathematical escape route is now precise: construct
polynomially many popular hyperbola differences that are not controlled
by one integer factor equation, independent-frequency rank, or
quadratic-mass-separated unions.

## Reproducibility

```bash
python3 verify_resonant_ansatz_no_go.py
pytest -q test_verify_resonant_ansatz_no_go.py
```

The script selects the densest divisor bin, computes every overlap and
compatibility contribution exactly, checks the linear size bound, audits
the variable-side optimum, and records the final exponent ledger.
