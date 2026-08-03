# Random-cluster boundary lemma for OPG-1757

Status: **PROVED AS AN EXACT REPRESENTATION BRIDGE; NOT A GLOBAL INTERFACE**.

Let `G=(V,E)` be fixed and put

\[
 P_q(\mathbf x)=q^{-|V|}\sum_{A\subseteq E}q^{k(A)}
       \prod_{a\in A}(q x_a)
   =\sum_{A\subseteq E}q^{|A|-|V|+k(A)}\mathbf x^A.
\]

The exponent `|A|-|V|+k(A)` is the cyclomatic number of `A`, hence is a
nonnegative integer and vanishes exactly when `A` is a forest.  Therefore
`P_q` is a polynomial in `q` with

\[
 P_0(\mathbf x)=F_G(\mathbf x),
\]

the multivariate forest polynomial.  Coefficientwise convergence also holds
after either marked-edge derivative.  Thus, for distinct `e,f`,

\[
 \lim_{q\downarrow0}
 \big((P_q)_e(P_q)_f-P_q(P_q)_{ef}\big)
 = (F_G)_e(F_G)_f-F_G(F_G)_{ef}.
\]

Consequently, nonnegativity of the scaled random-cluster Rayleigh difference
along any sequence `q_j -> 0+`, for every fixed positive activity vector,
implies the weighted forest Rayleigh inequality on that host.

This closes only the `q -> 0` passage.  It does **not** prove the required
finite-`q` negative-dependence premise, and therefore does not close the
campaign's arbitrary-host interface.  The finite-`q` premise retains the
same marked-edge correlation difficulty and must be independently justified.

## Bounded evidence

- `opg_triangle_random_cluster_probe.lean` proves exactly that the scaled
  triangle Rayleigh difference is `z*(1-q)*(1+z)`, hence nonnegative for
  `0 <= q <= 1` and `z >= 0`.
- `random_cluster_boundary_probe.py` uses exact symbolic arithmetic to check
  the unweighted complete graphs `K3`, `K4`, and `K5`.  Every marked-pair
  orbit factors as `(1-q)` times a polynomial with strictly positive integer
  coefficients.

Both are finite-host evidence only.
