# Red-team dossier: polynomial OPG deficit window

Date: 2026-08-01

Verdict at 00:26 HKT: **no internal counterexample found; independent
proof audit still required**.

Target under audit:

\[
s\ge2(4096q)^{67}
\quad\Longrightarrow\quad
C_{q,r}(s)>0\quad(0\le r\le2q).
\]

## 1. Dependency isolation

The candidate proof imports exactly two prior theorems.

1. For every marked endpoint,
   \(Q_{h,e,c}\in\mathbb Q[s]\), with leading coefficient
   \(A_{e,c}=1/(2^{e+c-1}(c-1)!e!)\).  The new height proof supplies
   \[
   \lVert Q_{h,e,c}\rVert_1
   \le15(m+1)2^m(2m+4)^{2m},\quad m=e+c-1.
   \]
2. In the relative Laurent expansion, \(q_{h,k}(e,c-1)\) is a
   bivariate polynomial of total degree at most \(2k\), simultaneously
   for every \(k\ge1\) and \(h=0,1,2\).

The second item is the all-order filtered-ring theorem already audited
in the preceding campaign.  It includes functional shifts \(2,3,4\)
for \(h=0,1,2\).  No assertion about pooled inversion is imported from
it.

Everything after these two inputs is reproved in
POLYNOMIAL_GROWING_DEFICIT_WINDOW.md.

## 2. Main failure modes tested

### A. Interpolation controls the wrong quantity

Potential failure: a degree bound plus node values might bound
polynomial coefficients but not the needed values at a large profile.

Disposition: the proof explicitly uses the bivariate Newton identity.
Mixed differences are bounded by \(2^{i+j}M_k\); evaluating the Newton
basis at the actual nonnegative integers \(e,\rho\le q+1\) gives the
point-value bound (7).  No coefficient-norm substitution is made.

### B. The triangular grid is insufficient

Potential failure: \(\Delta_e^i\Delta_\rho^j p(0,0)\) might use a node
outside \(e+\rho\le2k\).

Disposition: only \(i+j\le2k\) survives for a total-degree-\(2k\)
polynomial, and every node in that mixed difference has
\(a+b\le i+j\le2k\).  The triangle is exactly sufficient.

### C. A marking or falling shift escapes the bound

Potential failure: the pooled determinant might introduce a fourth
endpoint marking or an unbounded shift.

Disposition: the exact master products are \((1,1)\) and \((0,2)\).
The four shifts are
\[
1+c+e,\quad1+d+f,\quad c+e,\quad2+d+f,
\]
all at most \(q+4\), and \(\ell\le q\).  Every one is included in
the falling-factor check.

### D. Absolute profile summation costs \(C^q\)

Potential failure: replacing the determinant by absolute values could
destroy the small positive leading symbol.

Disposition: the absolute baseline profile sum is evaluated exactly,
not bounded by tuple count:
\[
S_{q,r}=\frac8{(q+1)!}[z^r](1+2z+2z^2)^{q+1}.
\]
For \(a_{q,r}=[z^r](1+2z+2z^2)^q\), the word-increment map gives
\[
a_{q,r-1}\le q a_{q,r},\qquad
a_{q,r-2}\le q^2a_{q,r}.
\]
Thus \(S_{q,r}/L_{q,r}\le10q\), uniformly at both \(r=0\) and
\(r=2q\).  No exponential profile factor remains.

### E. The loss index is off by two

Potential failure: using actual Laurent loss \(k\) where the master has
apparent degree \(2q+2\).

Disposition: every profile has exact apparent degree
\[
2m_1+2m_2+2\ell=2q+2.
\]
The first two degrees cancel; \(s^{2q-k}\) is therefore apparent loss
\(K=k+2\).  The candidate proof uses \(U_{k+2}\) throughout.

### F. The final geometric constant is insufficient

Potential failure: an additive \(k+2\) in the exponent is lost.

Disposition: for \(k\ge1\),
\[
k+2\le3k,\qquad k+3\le4k\le8q.
\]
The factors in the exact bound cost respectively \(60k\), \(6k\), and
\(k\) powers of the common base, totaling \(67k\).
At \(s=2X_q\), the finite tail is
\(\sum_{k=1}^{2q}2^{-k}=1-2^{-2q}<1\), so equality in the threshold
still gives strict positivity.

### G. “Fixed \(q\)” cannot be diagonalized

Potential failure: an inherited asymptotic statement might have a hidden
\(q\)-dependent threshold.

Disposition: the endpoint formulas and master formula are exact
polynomial identities, not \(O_q(\cdot)\) expansions.  Their common
combinatorial safe range is explicitly \(s\ge6q+4\), which is absorbed
by \(s\ge2(4096q)^{67}\).  Every new constant is displayed uniformly in
\(q\), so applying the theorem to \(q=q(s)\) introduces no quantifier
exchange.

## 3. Executable falsification results

Ordinary certificate:

    OPG POLYNOMIAL WINDOW BOUNDS CERTIFICATE: PASS
    exact_profile_coefficients: 99
    newton_reconstructions: 1001
    constant_chain_values: 7440
    falling_coefficients: 881548
    window_exponent: 67

Extended endpoint certificate adds:

    exact_q6_endpoint_losses: 1008
    exact_q6_layer_losses: 156

The exact profile test enumerates every profile for \(q\le9\) and every
\(0\le r\le2q\) in both master \((e,f,c,d,\ell)\) coordinates and an
independent five-tuple \((\rho,e,\sigma,f,\ell)\) loop, comparing both
rational sums with \([z^r]A^{q+1}/(q+1)!\).  The falling test includes
881,548 individual
shift/loss coefficients through \(q=12\).  The exact endpoint test uses
all 108 frozen \(q=6\) endpoint polynomials and all their Laurent losses.

Unit tests: **9/9 pass** across the height and polynomial-window
certificates.  The relevant script digests are:

- uniform-height certificate:
  5ba459bbd3bfc6ea3d1bdec9f5de783f25baaeb9733d4d7c6ca2a371d5c1faff;
- polynomial-window certificate:
  9aa6c5bbed178e1c39a55637c3fde003ed3d1e861d4aa40d5062cbc1028623db.

The inherited all-order filtration interface was also rerun through its
strongest available executable audit: 216 exact endpoint Laurent
coefficients, all three marking shifts, and the degree-four pooled
kernel passed.

## 4. Remaining audit obligation

There is no known unclosed algebraic step in Sections 2--5 of the
candidate theorem.  Nevertheless, because the conclusion upgrades a
logarithmic window to a power window, its status remains PENDING until an
independent reader has:

1. rechecked that the inherited all-\(k\) degree theorem has exactly the
   normalized \(Q_{h,e,c}\) used here;
2. independently reconstructed the absolute profile EGF (17);
3. independently followed the index shift \(K=k+2\) and constant chain.
