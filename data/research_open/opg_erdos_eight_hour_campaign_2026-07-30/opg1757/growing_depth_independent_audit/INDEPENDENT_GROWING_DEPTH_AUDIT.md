# Independent red-team audit of `GROWING_DEPTH_ATTACK.md`

Date: 2026-07-30

## Verdict

\[
\boxed{\text{FAIL AS ORIGINALLY WRITTEN; PASS AFTER ONE LOCAL REPAIR}}
\]

No counterexample was found to Theorems 1--2, the explicit
\(2^{54}\) corollary, or the seventh-layer formulas.  The normalization,
majorant, determinant estimate, Newton comparison, and parity/support
logic all survive independent reconstruction.

One genuine justification gap was found in the original constants
audit following (33).  The sentence asserting that a product of two
remainders is smaller merely because
\((R+1)^3/n^3<1\) did not retain the product constant \(2^{68}\).
That inference is insufficient as written.  The repair is short and
uses the already assumed condition (6):
\[
\begin{aligned}
2^{68}\frac{(R+1)^6}{n^6}
&=
\left(2^{68}\frac{(R+1)^3}{n^3}\right)
\frac{(R+1)^3}{n^3}\\
&\le
2^{32}\frac{(R+1)^3}{n^3},
\end{aligned}
\]
because
\[
n\ge2^{12}(R+1)^2
\quad\Longrightarrow\quad
\frac{(R+1)^3}{n^3}
\le\frac{2^{-36}}{(R+1)^3}.
\]
Thus the claimed \(2^{42}\), and hence \(2^{50}\), aggregate constant
still has ample slack.  This correction has been inserted into
`GROWING_DEPTH_ATTACK.md`.  The final mathematical result therefore
passes after repair.

## 1. Independence and reconstruction

The audit script imports no existing OPG verifier.  It independently
implements:

- the two finite Liu--Chow product sums;
- the adjacent-pair finite product;
- the one- and two-edge orbit identities;
- the formal heat coefficient
  \[
  \frac1{\rho!}f(D)\left(s-\frac{s^2}{2}\right)^\rho\bigg|_{s=0};
  \]
- determinant convolution with weights
  \(g_\rho g_\sigma\);
- exact Newton inversion; and
- the raw symbolic \(W_0,A,W_1,W_2\) sums used to recompute
  \(C_{15},C_{16}\).

For \(12\le n\le30\) and \(0\le\rho\le6\), the direct heat-operator
coefficient agrees exactly, as a rational number, with the independent
finite product for both \((a,b)=(1,2)\) and \((3,4)\).  This checks the
factor \(g_\rho=1/(2^\rho\rho!)\), the translation by \(e^{-D}\), and
the two \(w\)-derivative multipliers without reusing (16).

## 2. Lemma 3: equations (20)--(27)

### Equations (20)--(24)

Expanding
\[
\mathbb E e^{sY}=e^{z(s-s^2/2)}
\]
gives (20) coefficientwise.  Translating
\[
2^\rho q(s)^\rho
=\left(1-(s-1)^2\right)^\rho
\]
and moving evaluation from \(0\) to \(1\) gives exactly the
\(e^{-D}\) in (21); no power of two is missing.

Independently expanding
\[
-D+(n-b)\log(1+D/n)
\]
gives
\[
\sum_{j\ge1}\frac{(-1)^j}{n^j}
\left(\frac{bD^j}{j}+\frac{D^{j+1}}{j+1}\right),
\]
so all signs in (22), including the corrected alternating heat signs,
are correct.  Direct differentiation at the center reproduces (24).
Substitution yields every coefficient displayed in (16) and (18) for
\(0\le\rho\le18\).

### Equations (25)--(27)

The composition count in (26a) is complete:
\(\binom{J-1}{m-1}\) counts ordered positive compositions, each
\(A_{b,j}\) contributes at most two differential monomials, and its
scalar coefficients are bounded by four.  Therefore (26b) is a valid
overestimate.

For a surviving even derivative \(D^{2h}\), the elementary sharper
bound
\[
(2h)!\binom{\rho}{h}
\le(2h)^h\rho^h
\le(4\rho h)^h
\]
confirms (26).  The parity argument after \(a+D\) is also sound:
exactly one of the two resulting derivative orders is even, and the
surviving \(h\) is at most \(J\).  These observations reproduce (25).

For every nonzero term, \(J\le2\rho+1\).  Under
\(n\ge4096(\rho+1)^2\),
\[
\frac{128(\rho+1)J}{n}\le\frac1{16}.
\]
The remaining numerical series is
\[
\sum_{J\ge3}\frac{J^3}{16^{J-3}}
=31.546785\ldots<32,
\]
which verifies the \(2^{27}\) one-component tail and the \(2^{28}\)
two-component bound.

Independent exact tests through \(\rho=28\) found:

- largest observed ratio to the bound in (17):
  \(3.564\times10^{-7}\);
- largest observed ratio of the series in (27) to its bound:
  \(0.468840\).

These finite values are stress tests only; the general proof is the
composition and geometric-series argument above.

## 3. Orbit tails and determinant estimate (32)--(33)

The orbit formulas reconstructed directly from incidence counting
agree with (13)--(14).  On the Lemma 3 range,
\(\rho/n\) is small and
\[
(1-u)(1-2u)(1-3u)\ge\frac3{32}.
\]
Independent exact expansion of \(B_1,B_2\) through second order gives
the coefficients in (18).  Exact evaluations at
\(n=4096(\rho+1)^2\), \(0\le\rho\le28\), satisfy (19).

Equation (32) follows without approximation from
\[
\rho+1,\sigma+1\le R+1,\qquad
\sum_{\rho+\sigma=R}g_\rho g_\sigma=\frac1{R!}.
\]
The constant and \(1/n\) determinant terms cancel, while the
symmetrized \(1/n^2\) coefficient and the binomial second moment give
\(4R/R!\), confirming (28)--(31).

The only defect found was the double-remainder explanation stated in
the verdict.  After its correction, single remainders cost at most
\(2^{39}\) in aggregate, double remainders at most \(2^{33}\), and
the displayed cross-terms are below \(2^{20}\) per ordered type.
Thus \(2^{42}<2^{50}\) is valid.

Random and deterministic exact rational tests used
\[
1\le R\le24,\qquad
n\ge4096(R+1)^2.
\]
The largest observed ratio of the determinant error to the right side
of (7) was
\[
1.3643\times10^{-15}.
\]
Again, the infinite-range result rests on the repaired analytic bound,
not this scan.

## 4. Support, parity, and Newton ratios (35)--(39)

The support boundary was rebuilt from
\[
t=2n-2-k.
\]
At \(n_0=q_0+4\), the first possible total is
\[
t_0=3\quad(k\text{ odd}),\qquad
t_0=4\quad(k\text{ even}).
\]
One step below gives \(t=1\) in the odd case and \(t=2\) in the even
case.  Totals below two are empty, while the sole \(t=2\) determinant
is
\[
W_{1,1}^2-W_{0,1}W_{2,1}=0.
\]
Thus truncating Newton inversion at \(j=0\) is exact.

For the last term,
\[
R=
\begin{cases}
1+2r,&k\text{ odd},\\
2+2r,&k\text{ even}.
\end{cases}
\]
Hence every earlier \(R_\ell=R-2\ell\) remains respectively a positive
odd or positive even integer; Theorem 2 is never applied at \(R=0\)
or a negative value.

Direct division gives
\[
\frac{M(R_\ell,N_\ell)}{M(R,N)}
=\frac{R_\ell}{R}\frac{R!}{R_\ell!}
\cdot\frac{(N-\ell)^{2(N-\ell)-8}}{N^{2N-8}},
\]
from which (35) follows term by term.  Equation (36) is the usual
falling-factorial bound.  Once each determinant relative error is
below one, every earlier exact determinant has magnitude at most twice
its main term, yielding precisely (37).

Under (38a), the raw relative error supplied by (7) is
\[
\frac{2^{48}(R_\ell+1)^3}{R_\ell N_\ell}<1
\]
for every admissible parity and \(\ell\).  Independent exact
inequality checks covered both parities through Newton depth 80.
Separating the last-term error from the earlier absolute prefix gives
(39); no alternating term was omitted.

For (40),
\[
\frac{2^{51}(R+1)^2}{N}\le\frac18,\qquad
\frac{R^2}{N}\le2^{-54}.
\]
Using the elementary bound
\[
e^x-1\le\frac{x}{1-x}\qquad(0\le x<1)
\]
confirms
\[
\frac18+2(e^{2^{-54}}-1)<1.
\]
Thus the explicit \(2^{54}\) corollary is correct.

An independent exact Newton grid checked 205 coefficients for
\(8\le k\le44\) and
\(0\le r\le\min(7,\lfloor\sqrt k\rfloor)\); all were positive.

## 5. Independent seventh-layer re-audit

The raw Liu--Chow sums were symbolically rebuilt without importing the
sixth- or seventh-layer verifier.  They give
\[
\mathcal C_{15}(n)
=\frac{(n-4)_{\underline6}P_{15}(n)n^{2n-32}}
{119750400},
\]
\[
\mathcal C_{16}(n)
=\frac{(n-4)_{\underline6}P_{16}(n)n^{2n-34}}
{1556755200}.
\]
Both identities simplify exactly to zero after subtraction, confirming
the two denominators.

The same independent determinant implementation recomputed all 24
finite values used to close the seventh-layer residual ranges:

- odd \(k=7,9,\ldots,25\);
- even \(k=6,8,\ldots,32\).

Every integer agrees exactly with
`SEVENTH_ACTIVE_NEWTON_THEOREM.md`.  In particular, the corrected
\(\mathcal C_5\) normalization and denominator \(60\) in its
seven-point Newton term survive this audit.

## 6. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/growing_depth_independent_audit
pytest -q test_independent_verify_growing_depth.py
python3 independent_verify_growing_depth.py
```
