# Independent audit: weighted reverse-circle dyadic refinement

Date: 2026-07-30

Audited files:

- `WEIGHTED_REVERSE_CIRCLE_DYADIC_REFINEMENT.md`
- `verify_weighted_reverse_circle_dyadic_refinement.py`

## 0. Verdict

\[
\boxed{\mathrm{PASS}}
\]

The dyadic weighted-incidence inequality and the strengthened
multiplicity exponent
\[
\mu\ge t^{(5-15\kappa)/2-o(1)}
\qquad(1/5\le\kappa<1/3)
\]
are correct.  The improvement is structural and does not extend the
current hub-exclusion endpoint beyond \(\kappa<1/5\).

## 1. Independent weighted summation

Let the merged positive-radius circles have integer weights \(w_C\),
total weight \(\mathsf T=\sum_Cw_C\), and maximum weight \(\mu\).
For
\[
\mathcal C_j=\{C:2^j\le w_C<2^{j+1}\},
\qquad n_j=|\mathcal C_j|,
\]
one has \(n_j\le\mathsf T/2^j\).  Multiplying the ordinary
point--circle incidence theorem for \(\mathcal C_j\) by \(2^{j+1}\)
gives, up to absolute constants,
\[
\begin{aligned}
W_j\ll{}&
Q^{2/3}\mathsf T^{2/3}2^{j/3}\\
&+Q^{6/11}\mathsf T^{9/11}2^{2j/11}t^{o(1)}
+Q2^j+\mathsf T.
\end{aligned}
\]
The first three sums are geometric and are dominated by their final
layer.  The last is repeated \(O(\log\mathsf T)=t^{o(1)}\) times.
Thus
\[
W\ll
Q^{2/3}\mathsf T^{2/3}\mu^{1/3}
+Q^{6/11}\mathsf T^{9/11}\mu^{2/11}t^{o(1)}
+Q\mu+\mathsf Tt^{o(1)}.
\tag{A1}
\]
No assumption that every circle has weight \(\mu\) is used.  This is
the point missed by the earlier coarse estimate
\(\mu I(P,\mathcal C)\).

## 2. Independent exponent calculation

Put
\[
Q=t^{3+o(1)},\quad
\mathsf T\le MQL=t^{6-2\kappa+o(1)},\quad
\mu=t^{m+o(1)}.
\]
The four exponents on the right of (A1) are
\[
6-\frac{4\kappa}{3}+\frac m3,\quad
\frac{72-18\kappa+2m}{11},\quad
3+m,\quad
6-2\kappa.
\]
Against \(W\ge t^{7-3\kappa-o(1)}\), the first three require
\[
m\ge3-5\kappa,\qquad
m\ge\frac{5-15\kappa}{2},\qquad
m\ge4-3\kappa.
\]
For every \(\kappa>0\), the middle threshold is the smallest.  The
fourth term misses by \(1-\kappa\).  Hence
\[
m\ge\frac{5-15\kappa}{2}-o(1).
\tag{A2}
\]
At \(\kappa=1/5\), (A2) requires \(m\ge1\); for smaller
\(\kappa\), it contradicts the independent injective cap
\(\mu\le M=t^{1+o(1)}\).  At \(\kappa=1/4\), it gives
\(m\ge5/8\), and it becomes trivial at \(\kappa=1/3\).

## 3. Degenerate-circle and scope audit

Empty equations have zero incidence.  Zero-radius triples contribute
at most \(MQL=t^{6-2\kappa+o(1)}\), which is
\(o(t^{7-3\kappa-o(1)})\) for fixed \(\kappa<1\).  The perpendicular
target plane was removed upstream.  Therefore (A1)--(A2) apply to the
positive-radius mass required by the hub.

The refinement does not say that the new multiplicity lower bound is
attained, nor does it make one repeated circle expand.  The saved
circle--axis saturation examples remain compatible with high
multiplicity.

## 4. Reproduction

```bash
python3 verify_weighted_reverse_circle_dyadic_refinement.py
pytest -q test_verify_weighted_reverse_circle_dyadic_refinement.py
```

The independent hand calculation above agrees with all exact rational
thresholds checked by the verifier, including the endpoints
\(\kappa=1/5,1/3\) and the interior value \(\kappa=1/4\).
