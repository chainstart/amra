# OPG-1757: decidability of every fixed long-band positivity problem

Date: 2026-07-30

## 0. Corollary

For each fixed \(q\ge0\), the statement
\[
\boxed{
\gamma_{d,q}>0
\quad\text{for every integer }d\ge2q+1
}
\tag{1}
\]
is decidable by a finite exact rational computation.

This is a decidability theorem, not a proof that the answer to (1) is
`TRUE` for every \(q\).  It supplies a terminating certificate
procedure for each specified band.  The first eight inputs
\(q=0,\ldots,7\) return `TRUE`, agreeing with the separately proved
band theorems.

## 1. Exact production of the band polynomial

Fix \(q\).  The all-fixed-rank ordinary-symbol algorithm computes
\[
\beta_{d,r}\in\mathbb Q[d]
\qquad(0\le r\le q+1)
\tag{2}
\]
in finitely many exact symbolic operations.  Concretely, its rational
generating functions give exact depth values, while
\[
\deg_d\beta_{d,r}=3r
\tag{3}
\]
makes finite exact coefficient recovery unique.

The signed-Stirling and ordinary-to-falling triangle then computes
\[
\mathfrak h_0(d),\ldots,\mathfrak h_{q+1}(d),
\]
and the long-recurrence triangle computes
\[
\mathfrak g_0(d),\ldots,\mathfrak g_q(d),
\qquad
\mathfrak g_q(d)=\gamma_{d,q}
\quad(d\ge2q+1).
\tag{4}
\]
All operations take place in \(\mathbb Q[d]\).

The all-rank leading-layer theorem supplies the essential termination
input:
\[
\boxed{
\deg\mathfrak g_q=3q+2,
\qquad
[d^{3q+2}]\mathfrak g_q(d)>0.
}
\tag{5}
\]
Thus the computed polynomial is nonzero and eventually positive.

## 2. A finite exact decision interval

Put
\[
m=2q+1,\qquad
p_q(u)=\mathfrak g_q(u+m).
\tag{6}
\]
Clear its positive rational denominator and write
\[
P_q(u)=a_nu^n+a_{n-1}u^{n-1}+\cdots+a_0
\in\mathbb Z[u],
\qquad
a_n>0,
\tag{7}
\]
where \(n=3q+2\).

Define the exact rational Cauchy bound
\[
\boxed{
B_q=1+\max_{0\le i<n}\left|\frac{a_i}{a_n}\right|.
}
\tag{8}
\]
Every complex root \(z\) of \(P_q\) satisfies
\[
|z|\le B_q.
\tag{9}
\]
Therefore \(P_q\) has no real root on \((B_q,\infty)\).  Since its
leading coefficient is positive,
\[
\lim_{u\to+\infty}P_q(u)=+\infty,
\]
so continuity and (9) imply
\[
P_q(u)>0\qquad(u>B_q).
\tag{10}
\]

It follows that the algorithm only has to evaluate the finite list
\[
\boxed{
P_q(0),P_q(1),\ldots,P_q(\lceil B_q\rceil).
}
\tag{11}
\]
If every value in (11) is positive, then (10) proves (1).  If one is
zero or negative, its index supplies an exact counterexample
\[
d=m+u
\]
to (1).  Hence the procedure always terminates with the correct
answer.

If \(\lceil B_q\rceil<0\), the interval is empty and (10) already
decides the problem.  With the standard bound (8), however,
\(B_q\ge1\), so this edge case does not arise.

## 3. Why eventual positivity alone was not yet decidability

The leading-layer theorem proves that every fixed band is eventually
positive, but does not itself print an effective threshold.  Equation
(8) turns the exact computed polynomial into such a threshold using
only rational arithmetic.  No numerical root isolation, floating
point approximation, or conjectural root bound is needed.

The resulting bounds may be very large and are not intended as an
efficient verification strategy.  Decidability only requires
finiteness.  Sturm sequences, positive shifts, or sharper positive-root
bounds can shorten the certificate without changing the conclusion.

## 4. Exact replay for \(q=0,\ldots,7\)

`verify_all_fixed_band_positivity_decidability.py` rebuilds the first
eight band polynomials from the independent rank-eight triangle and
computes (8) exactly.  The resulting endpoints are:

\[
\begin{array}{c|c|c}
q&\deg P_q&\lceil B_q\rceil\\ \hline
0&2&11\\
1&5&1404\\
2&8&559962\\
3&11&479961763\\
4&14&811996809260\\
5&17&2151028705603519\\
6&20&8462531428815041792\\
7&23&47334631004004373589462.
\end{array}
\tag{12}
\]

For these eight bands, every coefficient of \(P_q(u)\) is already
strictly positive.  This is a stronger exact certificate that
simultaneously verifies every value in the potentially enormous
finite intervals (11), without enumerating them.  The verifier still
records the Cauchy bounds and interval sizes to replay the general
decision construction.

The accompanying tests also exercise the literal finite enumeration
branch on small mixed-sign polynomials, including one `TRUE` instance
and one instance with explicit nonpositive integer witnesses.

## 5. Claim boundary

### Proved

* for every specified fixed \(q\), a finite exact algorithm decides
  full admissible-depth positivity of \(\gamma_{d,q}\);
* a `FALSE` result produces an exact admissible integer witness;
* \(q=0,\ldots,7\) replay as `TRUE`.

### Not proved

* that the procedure returns `TRUE` for every \(q\);
* a uniform practical bound on the size or running time of the finite
  check;
* all-band positivity, interlacing, real-rootedness, or OPG-1757.

In particular, applying the procedure separately to arbitrarily many
fixed bands cannot be promoted to an all-\(q\) positivity proof without
new uniform mathematics.

## 6. Reproduction

```bash
python3 verify_all_fixed_band_positivity_decidability.py
pytest -q test_verify_all_fixed_band_positivity_decidability.py
```
