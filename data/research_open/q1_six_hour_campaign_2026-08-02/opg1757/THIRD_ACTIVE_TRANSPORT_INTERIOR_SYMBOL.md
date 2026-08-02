# OPG-1757: macroscopic interior positivity of the third-active transports

Date: 2026-08-02

Status: **PROVED COMPACT-INTERIOR ASYMPTOTIC THEOREM; BOUNDARY LAYERS OPEN**.

## 1. Theorem

Let

\[
 R_s^{\rm o}=H_{s+1}^{\rm o}-(s+6z)^2H_s^{\rm o},
 \qquad
 R_s^{\rm e}=H_{s+1}^{\rm e}-(s+7z)^2H_s^{\rm e}.
\tag{1}
\]

For every fixed `0<epsilon<1`, there is `s_0(epsilon)` such that, for
every integer `s>=s_0(epsilon)` and every integer `d` satisfying

\[
 \varepsilon s\le d\le(2-\varepsilon)s,
\tag{2}
\]

one has

\[
 \boxed{[z^d]R_s^{\rm o}>0,\qquad [z^d]R_s^{\rm e}>0.}
\tag{3}
\]

The threshold is not made explicit here.  The theorem is uniform on
every compact subinterval of `0<d/s<2`; it is not a finite scan.

## 2. Exact exponential decompositions

Use `u_a=1+a beta`.  Let `L_s^o(beta)` and `L_s^e(beta)` be the
sufficient transport kernels of `THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md`,
and clear their positive denominators:

\[
 W_s^{\rm o}=12s\beta^8L_s^{\rm o},
 \qquad
 W_s^{\rm e}=60s\beta^{10}L_s^{\rm e}.
\tag{4}
\]

Exact differentiation and collection of the frozen fixed-page formulas
give

\[
 W_s^{\rm o}=\sum_{a=2}^6u_a^{2s-15}C_{a,s}^{\rm o}(\beta),
\tag{5}
\]

\[
 W_s^{\rm e}=\sum_{a=2}^7u_a^{2s-17}C_{a,s}^{\rm e}(\beta).
\tag{6}
\]

Every `C_(a,s)` has fixed beta degree and coefficients polynomial in
`s`.

The top-page discrete remainders needed to justify the Bernoulli scale
step are

\[
 D_{p,s}=P_{p,s+1}-u_p^2P_{p,s},
 \qquad p\in\{6,7\}.
\tag{7}
\]

After restoring the removed beta power,

\[
 \beta^{2p-4}D_{p,s}
 =F_{p,s+1}-u_p^2F_{p,s}
 =\sum_{a=2}^pu_a^{2s-2p-2}G_{p,a,s}(\beta),
\tag{8}
\]

again with fixed-degree polynomial kernels.  In the dominant base,

\[
 G_{p,p,s}=u_p^2\{K_p(s+1)-K_p(s)\}.
\tag{9}
\]

## 3. Uniform coefficient-symbol lemma

Let `L=2s+O(1)`, `k/s=theta+O(1/s)`, and fix `i`.  Uniformly for
`epsilon<=theta<=2-epsilon`,

\[
 \frac{[\beta^{k-i}]u_p^L}{[\beta^k]u_p^L}
 =p^{-i}\frac{(k)_i}{(L-k+1)_i}
 \longrightarrow
 \left(\frac{\theta}{p(2-\theta)}\right)^i.
\tag{10}
\]

Thus, if the largest `s`-degree among the coefficients of a fixed
kernel `C_s(beta)` is `kappa`, then

\[
 \frac{[\beta^k]u_p^LC_s(\beta)}
 {p^k\binom Lk s^\kappa}
 \longrightarrow
 \Phi\left(\frac{\theta}{p(2-\theta)}\right),
\tag{11}
\]

where `Phi` is formed from the leading `s`-coefficients of `C_s`.
Because only finitely many shifts `i` occur, the convergence is uniform
on the compact interval in (10).

Every lower base `a<p` is exponentially negligible there.  Its ratio
to the `p`-base is bounded by

\[
 O(s^M)\left(\frac ap\right)^k
 \le O(s^M)\left(\frac{p-1}{p}\right)^{\varepsilon s},
\tag{12}
\]

for some fixed `M`; this tends uniformly to zero.  Polynomial degree
advantages of lower-base kernels therefore cannot change the dominant
sign.

## 4. The four main symbols and their zeros

Exact extraction gives:

| object | dominant base `p` | `kappa` | `Phi(x)` |
|---|---:|---:|---|
| odd sufficient kernel | 6 | 9 | `1119744*x^16*(1+6*x)^2` |
| odd page remainder | 6 | 7 | `4478976*x^16*(1+6*x)^2` |
| even sufficient kernel | 7 | 11 | `161414428*x^20*(1+7*x)^2` |
| even page remainder | 7 | 9 | `807072140*x^20*(1+7*x)^2` |

With

\[
 x=\frac{\theta}{p(2-\theta)},
\tag{13}
\]

these become positive constants times

\[
 \frac{4\theta^{16}}{6^{16}(2-\theta)^{18}}
 \quad\hbox{or}\quad
 \frac{4\theta^{20}}{7^{20}(2-\theta)^{22}}.
\tag{14}
\]

Hence there is no zero in `0<theta<2`.  The only finite boundary zero
is `theta=0`, of multiplicity 16 in the odd branch and 20 in the even
branch.  In the `x` coordinate there is also a negative double root
`x=-1/p`, outside the relevant positive interval.  The apparent pole at
`theta=2` records degeneration of the chosen binomial normalization,
not a sign change.

Equations (10)--(14) prove that both page remainders (7) and both
sufficient kernels (4) are strictly positive on (2) once `s` is large
enough.  The page-remainder sign makes the Bernoulli scaling step legal;
the sufficient-kernel inequalities from the low-column note then give
(3).

## 5. Boundary left by this theorem

Taken alone, this theorem localizes the growing-middle obstruction to
mesoscopic
boundary layers:

\[
 d\to\infty,\quad d=o(s),
 \qquad\hbox{or}\qquad
 2s-d\to\infty,\quad 2s-d=o(s).
\tag{15}
\]

The subsequent quantitative argument in
`THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md` removes the second layer and
shrinks the first one to `31<=d<241*log(s)`.  Thus (15) records precisely
the boundary not covered by the compact-interior symbol alone; it is no
longer the current global frontier.

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 third_active_transport_recurrence_attack.py
```

The verifier reconstructs (5)--(8) at exact integer parameters and
checks all four factorizations in the table.  The complete transports,
the universal third-active row, and the original OPG-1757 proposition
remain open.
