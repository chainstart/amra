# The critical square-root bottom Newton window

Date: 2026-07-30

## 1. Outcome

The explicit heat remainder and the complete alternating-prefix estimate
in `GROWING_DEPTH_ATTACK.md` already contain a genuine fixed-constant
square-root window.  Translating their constants gives:

### Theorem 1 (explicit fixed square-root window)

Let
\[
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]
If
\[
\boxed{
k\ge 9\cdot2^{58},
\qquad
0\le r\le
\left\lfloor\frac{\sqrt{k}}{2^{28}}\right\rfloor,
}
\tag{1}
\]
then
\[
\boxed{a_{k,q_0+r}>0.}
\tag{2}
\]

Thus the previously stated range \(r=o(\sqrt{k})\) rigorously extends to
\[
\boxed{r\le c\sqrt{k}\quad\text{with}\quad c=2^{-28}.}
\tag{3}
\]
The constant is deliberately tiny because it inherits the
componentwise heat-majorant constant \(2^{50}\).  No numerical
extrapolation is used.

This note also resums every earlier Newton main term at the critical
scale.  If the determinants are replaced by their heat-leading terms,
the exact scaling function is
\[
\boxed{
\exp\left(-e^{-2}\frac{R^2}{N}\right).
}
\tag{4}
\]
For \(r/\sqrt{k}\to\tau\), this becomes
\[
\boxed{\exp(-8e^{-2}\tau^2).}
\tag{5}
\]
Equation (5) is proved for the fully alternating main-term model.  The
current determinant remainder is sufficient for Theorem 1 but does not
vanish when \(R^2/N\to\lambda>0\), so (5) is not claimed as the scaling
limit of the exact Newton coefficient.

## 2. Parameters and the inherited uniform estimate

For the last Newton-inversion term, put
\[
N=q_0+4+r,
\]
\[
R=
\begin{cases}
1+2r,&k\text{ odd},\\
2+2r,&k\text{ even}.
\end{cases}
\tag{6}
\]
The exact last determinant main term is
\[
M(R,N)=\frac{4R}{R!}N^{2N-8}.
\tag{7}
\]

The heat proof gives, whenever
\[
N\ge2^{52}(R+1)^2,
\tag{8}
\]
the complete Newton-inversion estimate
\[
\boxed{
\left|
\frac{a_{k,q_0+r}}
{\frac{(k-2)!}{2}M(R,N)}
-1
\right|
\le
\frac{2^{51}(R+1)^2}{N}
+2\left(e^{R^2/N}-1\right).
}
\tag{9}
\]

Both terms in (9) are essential:

- the first controls the uniform determinant heat remainder, including
  the last term;
- the second is the absolute sum of every alternating earlier Newton
  term, after its determinant error is included.

Thus (9) does not infer Newton positivity from determinant positivity.
It explicitly controls the entire alternating inversion.

## 3. Proof of Theorem 1

For both parities,
\[
N\ge\frac{k}{2},
\qquad
R+1\le2r+3.
\tag{10}
\]
Under (1),
\[
2r\le2^{-27}\sqrt{k}.
\]
The lower bound on \(k\) gives
\[
\sqrt{k}\ge3\cdot2^{29},
\qquad
3\le2^{-29}\sqrt{k}.
\]
Therefore
\[
R+1
\le
\left(2^{-27}+2^{-29}\right)\sqrt{k}
=5\cdot2^{-29}\sqrt{k}.
\tag{11}
\]
Consequently,
\[
2^{52}(R+1)^2
\le
2^{52}\cdot25\cdot2^{-58}k
=\frac{25}{64}k
<\frac{k}{2}
\le N.
\tag{12}
\]
This proves the heat-range condition (8), including the uniform
remainder requirements for every earlier determinant in the Newton
sum.

Set
\[
x=\frac{(R+1)^2}{N}.
\]
Equation (12) gives
\[
0\le x\le2^{-52},
\qquad
\frac{R^2}{N}\le x.
\tag{13}
\]
Using
\[
e^y-1\le\frac{y}{1-y}
\qquad(0\le y<1)
\tag{14}
\]
in (9), the total relative error is at most
\[
\frac12+\frac{2x}{1-x}
\le
\frac12+
\frac{2^{-51}}{1-2^{-52}}
<1.
\tag{15}
\]
The reference quantity
\[
\frac{(k-2)!}{2}M(R,N)
\]
is positive.  Equation (15) therefore proves (2). \(\square\)

## 4. Where every alternating earlier term goes

The term \(j=r-\ell\) in Newton inversion has
\[
N_\ell=N-\ell,\qquad R_\ell=R-2\ell.
\]
Its main-term ratio satisfies
\[
\frac{M(R_\ell,N_\ell)}{M(R,N)}
\le
\left(\frac{R^2}{N^2}\right)^\ell,
\tag{16}
\]
on the actual Newton support.  Indeed there
\[
N_\ell=N-\ell\ge q_0+4\ge4,
\]
which is the needed scope for comparing the nonnegative powers
\((N-\ell)^{2(N-\ell)-8}\) and
\(N^{2N-8-2\ell}\).  Inequality (16) is not asserted for arbitrary
small triples outside this support.
and
\[
\binom{N-4}{\ell}\le\frac{N^\ell}{\ell!}.
\tag{17}
\]
Condition (8) makes the heat error of every admissible earlier
determinant smaller than its main term.  Hence its exact magnitude is
at most twice its main term.  Summing without using cancellation gives
\[
\sum_{\ell\ge1}
\left|
\binom{N-4}{\ell}
\frac{\mathcal C_{R_\ell+2}(N_\ell)}
     {M(R,N)}
\right|
\le
2\sum_{\ell\ge1}
\frac{(R^2/N)^\ell}{\ell!}
=2(e^{R^2/N}-1).
\tag{18}
\]
This is the second term in (9).  The support cutoff in the exact Newton
formula is retained; extending the nonnegative majorant to
\(\ell=\infty\) only enlarges it.

## 5. Critical resummation of the main terms

Define the fully alternating main-term ratio
\[
\mathscr S_{N,R}
=
\sum_{\ell=0}^{\lfloor(R-1)/2\rfloor}
(-1)^\ell
\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}.
\tag{19}
\]

### Theorem 2 (main-term critical scaling)

Suppose
\[
N\to\infty,\qquad R\to\infty,\qquad
\frac{R^2}{N}\to\lambda\in[0,\infty).
\tag{20}
\]
Then
\[
\boxed{
\mathscr S_{N,R}
\longrightarrow
\exp(-e^{-2}\lambda).
}
\tag{21}
\]

### Proof

For every fixed \(\ell\),
\[
\begin{aligned}
&\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}\\
&=
\binom{N-4}{\ell}
\frac{R-2\ell}{R}
\frac{R!}{(R-2\ell)!}
N^{-2\ell}
\left(1-\frac{\ell}{N}\right)^{2N-2\ell-8}.
\end{aligned}
\tag{22}
\]
The five factors respectively have the fixed-\(\ell\) limits
\[
\frac{N^\ell}{\ell!},\qquad
1,\qquad
R^{2\ell},\qquad
N^{-2\ell},\qquad
e^{-2\ell}.
\]
Thus (22) tends to
\[
\frac{(\lambda e^{-2})^\ell}{\ell!}.
\tag{23}
\]

Moreover, (16)--(17) give the uniform domination
\[
0\le
\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}
\le
\frac{(R^2/N)^\ell}{\ell!}.
\tag{24}
\]
For the support in (19), condition (20) gives
\(\ell\le R/2=O(\sqrt N)\), hence \(N-\ell\ge4\) uniformly for all
sufficiently large \(N\); thus the stated scope of (16) covers every
summand in (24).
For large \(N\), the right side is bounded by
\[
\frac{(\lambda+1)^\ell}{\ell!}.
\]
Extend the summand by zero past its support.  Dominated convergence on
\(\ell\in\mathbb Z_{\ge0}\) now gives
\[
\lim\mathscr S_{N,R}
=\sum_{\ell\ge0}
\frac{(-\lambda e^{-2})^\ell}{\ell!}
=e^{-\lambda e^{-2}}.
\]
\(\square\)

If \(r/\sqrt{k}\to\tau>0\), then
\[
N\sim\frac{k}{2},
\qquad
R\sim2r,
\qquad
\frac{R^2}{N}\to8\tau^2,
\]
which yields (5).

## 6. Exact obstruction to the full critical scaling limit

The determinant estimate currently available is
\[
\left|
\frac{\mathcal C_{R+2}(N)}{N^{2N-6}}
-\frac{4R}{R!\,N^2}
\right|
\le
\frac{2^{50}(R+1)^3}{R!\,N^3}.
\tag{25}
\]
Relative to its main term, this is
\[
\boxed{
\varepsilon_{\rm det}(R,N)
\le
2^{48}\frac{(R+1)^3}{RN}.
}
\tag{26}
\]
If \(R\to\infty\) and \(R^2/N\to\lambda>0\), the right side tends to
\[
2^{48}\lambda,
\tag{27}
\]
not to zero.  Therefore (25) cannot justify replacing all exact
determinants by their main terms in (19).  This is the precise analytic
barrier to promoting (21) to the exact scaling law.

The symbolic determinant kernel strongly suggests that (26) is
componentwise-majorant loss rather than true behavior.  Its first terms
are
\[
\frac{4R}{R!\,N^2}
+\frac{16R(R-1)}{R!\,N^3}
+O\left(\frac{R^3}{R!\,N^4}\right),
\tag{28}
\]
whose correction relative to the main term is
\[
O(R/N)=o(1)
\]
through the square-root window.  A proof of the exact scaling function
requires a determinant-level all-orders majorant preserving these
cancellations.

## 7. What has and has not been proved

### Proved

- a fixed, explicit square-root positivity window with
  \(c=2^{-28}\);
- uniform control of the heat remainder throughout that window;
- absolute control of every alternating earlier Newton term;
- the exact critical scaling function of the alternating main-term
  model.

### Not proved

- the scaling limit (5) for the exact Newton coefficient;
- positivity for arbitrary fixed \(c>2^{-28}\);
- a determinant-level remainder \(o(1)\) for every bounded
  \(R^2/N\).

The next sharp target is
\[
\frac{\mathcal C_{R+2}(N)}
     {\frac{4R}{R!}N^{2N-8}}
=1+o(1)
\qquad
\text{uniformly for }R^2/N\le L
\tag{29}
\]
for each fixed \(L\).  Combined with Theorem 2, (29) would rigorously
give the exact critical function (5).

## 8. Verification

`verify_critical_sqrt_bottom_window.py`:

1. checks the integer inequalities translating (1) into (8);
2. evaluates the complete error majorant (15);
3. computes the exact finite alternating main-term sum (19);
4. compares it with \(e^{-e^{-2}R^2/N}\); and
5. records the nonvanishing critical limit of the present determinant
   remainder.

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757
pytest -q test_verify_critical_sqrt_bottom_window.py
python3 verify_critical_sqrt_bottom_window.py
```

The numerical scaling samples are regression evidence only.  The fixed
window follows from the exact integer inequalities and (9); Theorem 2
follows from dominated convergence.
