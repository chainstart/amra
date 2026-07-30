# Independent red-team audit of the critical square-root bottom window

Date: 2026-07-30

Audited target: `CRITICAL_SQRT_BOTTOM_WINDOW_THEOREM.md`

## 0. Verdict and novelty classification

\[
\boxed{\textsf{PASS WITH SCOPE CLARIFICATION}.}
\]

The explicit positivity statement
\[
k\ge9\cdot2^{58},\qquad
0\le r\le\left\lfloor2^{-28}\sqrt{k}\right\rfloor
\quad\Longrightarrow\quad
a_{k,q_0+r}>0
\tag{A1}
\]
is correct.

Its mathematical status needs the following precise description.

1. The heat remainder, determinant estimate, full alternating-prefix
   bound, and equation (39) were already proved in
   `GROWING_DEPTH_ATTACK.md`.
2. Statement (A1) is a new **explicit reparameterization and
   fixed-constant specialization of equation (39)**.  It is not a new
   heat-kernel or Newton-inversion estimate.
3. It is **not literally a substitution into Corollary 4**.  The
   advertised boundary generally satisfies the \(2^{52}\) condition
   used by equation (39), but at the first endpoint it fails the
   \(2^{54}\) sufficient condition stated in Corollary 4.
4. The critical exponential
   \(\exp(-e^{-2}R^2/N)\) is a genuinely new explicit resummation of
   the already available leading-term model.  It is not a scaling
   theorem for the exact Newton coefficient.

Thus the document contains a useful new corollary in the original
\((k,r)\) parameters and a new model calculation, but no new
determinant-level analytic estimate.

## 1. Exact constant translation

For both parities,
\[
N=q_0+4+r\ge\frac{k}{2},\qquad R+1\le2r+3.
\tag{A2}
\]
Under (A1),
\[
2r\le2^{-27}\sqrt{k}.
\]
The threshold \(k\ge9\cdot2^{58}\) gives
\[
3\le2^{-29}\sqrt{k},
\]
and hence
\[
R+1\le5\cdot2^{-29}\sqrt{k}.
\tag{A3}
\]
Therefore
\[
2^{52}(R+1)^2
\le\frac{25}{64}k
<\frac{k}{2}
\le N.
\tag{A4}
\]
With \(x=(R+1)^2/N\), equation (39) is bounded by
\[
2^{51}x+2(e^{R^2/N}-1)
\le\frac12+\frac{2x}{1-x}<1,
\tag{A5}
\]
because \(R^2/N\le x\le2^{-52}\).  The positive endpoint
main term therefore dominates the full exact alternating sum.

### Why this is not merely Corollary 4

Corollary 4 assumes
\[
N\ge2^{54}(R+1)^2.
\tag{A6}
\]
At the first endpoint
\[
k=9\cdot2^{58},\qquad r=6,\qquad R=14,
\]
one has
\[
N=\frac{k}{2}+9
<2^{54}\cdot15^2.
\tag{A7}
\]
Thus (A6) fails, although (A4) and the sharper error budget (A5)
hold.  Theorem 1 is a direct specialization of equation (39) with a
new constant calculation, not a literal restatement of Corollary 4.

Corollary 4 already makes the existence of some fixed square-root
constant implicit.  The new content of (A1) is the explicit
\(c=2^{-28}\), its finite threshold, and the sharper use of the two
separate errors in (39).

## 2. Does equation (39) cover every earlier term?

Yes.  For the actual Newton term indexed by \(0\le\ell\le r\),
\[
N_\ell=N-\ell,\qquad R_\ell=R-2\ell.
\tag{A8}
\]
Since
\[
N=q_0+4+r,
\]
one has the exact support bounds
\[
N_\ell\ge q_0+4\ge4,\qquad R_\ell\ge1.
\tag{A9}
\]
Also \(r\le R/2\).  Under
\[
N\ge2^{52}(R+1)^2,
\]
we have \(R<N\), and therefore
\[
N_\ell\ge N-r\ge N-\frac R2\ge\frac N2.
\tag{A10}
\]
It follows that
\[
N_\ell
\ge2^{51}(R+1)^2
\ge4096(R_\ell+1)^2.
\tag{A11}
\]
Thus the determinant estimate applies to every earlier term, not just
the last one.

The relative determinant error at \((R_\ell,N_\ell)\) is
\[
\varepsilon_\ell
\le
2^{48}\frac{(R_\ell+1)^3}{R_\ell N_\ell}.
\tag{A12}
\]
Because \(R_\ell\ge1\),
\[
\frac{(R_\ell+1)^3}{R_\ell}
\le2(R_\ell+1)^2
\le2(R+1)^2.
\]
Using (A10),
\[
\varepsilon_\ell
\le2^{50}\frac{(R+1)^2}{N}
\le\frac14<1.
\tag{A13}
\]
Consequently every exact earlier determinant has magnitude at most
twice its positive main term.  Combining this with
\[
\binom{N-4}{\ell}\le\frac{N^\ell}{\ell!}
\]
and the main-ratio estimate gives the complete finite-prefix bound
\[
2\sum_{\ell\ge1}
\frac{(R^2/N)^\ell}{\ell!}
=2(e^{R^2/N}-1).
\tag{A14}
\]
Extending past the exact support only adds nonnegative majorant terms.
Therefore the interpretation of the second term in equation (39) is
correct.

## 3. The small-\(N\) scope of equation (35)

The proof of
\[
\frac{M(R-2\ell,N-\ell)}{M(R,N)}
\le\left(\frac{R^2}{N^2}\right)^\ell
\tag{A15}
\]
uses
\[
(N-\ell)^{2(N-\ell)-8}
\le N^{2N-8-2\ell}.
\tag{A16}
\]
This comparison requires
\[
2(N-\ell)-8\ge0,
\quad\text{equivalently}\quad N-\ell\ge4.
\tag{A17}
\]
It is not a valid unrestricted inequality for arbitrary small
\((N,R,\ell)\).  For example,
\[
(N,R,\ell)=(3,3,1)
\]
has exponent \(-4\), and exact calculation gives
\[
\frac{M(1,2)}{M(3,3)}=\frac98
>1
=\left(\frac{3^2}{3^2}\right).
\tag{A18}
\]

This does not damage either result under audit:

- on the actual Newton support, (A9) proves (A17) for every term;
- in the critical main-model theorem,
  \(R^2/N\to\lambda<\infty\) implies \(R=O(\sqrt N)\), so for every
  sufficiently large \(N\) and every supported
  \(\ell\le(R-1)/2\),
  \[
  N-\ell\ge N-O(\sqrt N)\ge4.
  \]

Equation (35) should therefore be read as an actual-support or
eventually-asymptotic inequality, not as a statement for all positive
integers \(N,R\).  The theorem uses it only within those valid scopes.

## 4. Dominated convergence for the main model

Let the nonnegative magnitude of the \(\ell\)-th model summand be
\[
u_{N,R}(\ell)
=
\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}
\]
on its support, and zero otherwise.

For every fixed \(\ell\), under
\[
N\to\infty,\qquad R\to\infty,\qquad
\frac{R^2}{N}\to\lambda,
\]
direct factorization gives
\[
u_{N,R}(\ell)
\longrightarrow
\frac{(\lambda e^{-2})^\ell}{\ell!}.
\tag{A19}
\]
The five elementary factors are:
\[
\binom{N-4}{\ell}\sim\frac{N^\ell}{\ell!},
\quad
\frac{R-2\ell}{R}\to1,
\quad
\frac{R!}{(R-2\ell)!}\sim R^{2\ell},
\]
\[
N^{-2\ell},
\quad
\left(1-\frac{\ell}{N}\right)^{2N-2\ell-8}
\to e^{-2\ell}.
\]

For all sufficiently large \(N\), Section 3 makes equation (35)
uniformly valid over the full support.  Hence
\[
0\le u_{N,R}(\ell)
\le\frac{(R^2/N)^\ell}{\ell!}
\le\frac{(\lambda+1)^\ell}{\ell!}.
\tag{A20}
\]
The final sequence is summable on
\(\mathbb Z_{\ge0}\).  Extending the triangular array by zero beyond
its support therefore permits dominated convergence with counting
measure:
\[
\begin{aligned}
\lim_{N\to\infty}
\sum_{\ell\ge0}(-1)^\ell u_{N,R}(\ell)
&=
\sum_{\ell\ge0}
\frac{(-\lambda e^{-2})^\ell}{\ell!}\\
&=\exp(-\lambda e^{-2}).
\end{aligned}
\tag{A21}
\]
The domination is genuine and uniform; it does not rely on numerical
cancellation.

The theorem assumes \(R\to\infty\).  If \(R\) instead remains bounded
while \(R^2/N\to0\), the model sum still tends to \(1\), but that is a
separate finite-support observation rather than an application of its
stated dominated-convergence theorem.

## 5. Exact-model distinction

The determinant relative remainder is only bounded by
\[
2^{48}\frac{(R+1)^3}{RN}.
\tag{A22}
\]
When \(R\to\infty\) and \(R^2/N\to\lambda>0\), this upper bound tends
to \(2^{48}\lambda\), not zero.  Thus the main-model limit (A21)
cannot presently be transferred to the exact Newton coefficient.

This is not a merely technical wording issue: a new determinant-level
majorant preserving cancellation is required.  The document states
this limitation correctly.

## 6. Independent verifier

`independent_verify_critical_sqrt_bottom_window.py` imports no existing
AMRA verifier.  It independently performs:

1. exact parity and endpoint parameter reconstruction;
2. the \(2^{52}\) equation-(39) boundary check;
3. the failed \(2^{54}\) Corollary-4 check at the first endpoint;
4. every earlier-term heat-range and relative-error check;
5. 3,555 exact instances of equation (35) on actual Newton support;
6. the explicit negative-exponent counterexample (A18);
7. independent main-model evaluation; and
8. termwise verification of the factorial dominating envelope for
   four critical sequences.

Run:
```bash
python3 independent_verify_critical_sqrt_bottom_window.py \
  > critical_sqrt_bottom_window_independent_certificate.json
pytest -q test_independent_verify_critical_sqrt_bottom_window.py
```

The numerical model samples are regressions.  The theorem-level
dominated-convergence justification is equations (A19)--(A21), and the
exact positivity proof is equations (A2)--(A14).
