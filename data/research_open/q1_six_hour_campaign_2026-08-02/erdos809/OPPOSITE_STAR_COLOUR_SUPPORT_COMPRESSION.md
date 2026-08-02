# Erdős #809 — leaf independence compresses centre colour support

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

For an opposite active zero-star with centre `b`, leaf set `L`, and
pair multiplicities `h_c`, let

\[
 \Gamma_c=\{\gamma:b,c\in Y_\gamma\},
 \qquad
 H_L=\sum_{c\in L}|\Gamma_c|.
\tag{1}
\]

Put

\[
 \alpha_L=\alpha(G[L]).
\tag{2}
\]

## 2. Colour-support compression

### Theorem 2.1

The number of distinct colours occurring among the sets `Gamma_c` is
at least

\[
 \boxed{
 \left|\bigcup_{c\in L}\Gamma_c\right|
 \ge\left\lceil\frac{H_L}{\alpha_L}\right\rceil.
 }
\tag{4}
\]

Consequently

\[
 \boxed{
 d_A(b)\ge\left\lceil\frac{H_L}{\alpha_L}\right\rceil,
 }
\tag{5}
\]

and the union-host missing rectangle gives

\[
 \boxed{
 M_A\ge
 \left\lceil\frac{H_L}{\alpha_L}\right\rceil
 \left\lceil\frac{H_L}{\ell}\right\rceil.
 }
\tag{6}
\]

#### Proof

For one colour `gamma`, the set

\[
 L_\gamma=\{c\in L:\gamma\in\Gamma_c\}
\]

lies inside the outer endpoint set `Y_gamma`.  Every pair in
`binom(Y_gamma,2)` is an active base pair and therefore a missing
`B`-edge.  Hence `L_gamma` is independent in `G[L]` and has at most
`alpha_L` members.  The `H_L` leaf--colour incidences are thus covered
by colour supports of size at most `alpha_L`, proving (4).

Distinct colours at `b` use distinct incident good `A`--`b` edges,
which proves (5).  The whole union host \(A\cap U\) is anticomplete to
\(N_A(b)\), and it contains \(N_A(c)\) for every leaf.  Its size is
therefore at least
\(\max_c h_c\ge\lceil H_L/\ell\rceil\), proving (6).  QED.

## 3. Eliminate the independence number under reserve failure

Every pair of a maximum independent set in `G[L]` is a missing
`B`-edge incident with active zero-shore leaves.  Therefore

\[
 \binom{\alpha_L}{2}\le|\mathcal Q|.
\tag{7}
\]

Under global reserve failure, define

\[
 a_B=\left\lfloor
 \frac{1+\sqrt{1+8(D_B-1)}}2
 \right\rfloor.
\tag{8}
\]

Put \(a_*=\min\{\ell,a_B\}\).  Then `alpha_L<=a_*`, and
(5)--(6) strengthen to

\[
 \boxed{
 d_A(b)\ge\left\lceil\frac{H_L}{a_*}\right\rceil,
 \qquad
 M_A\ge
 \left\lceil\frac{H_L}{a_*}\right\rceil
 \left\lceil\frac{H_L}{\ell}\right\rceil.
 }
\tag{9}
\]

The rectangle-to-budget transference also yields

\[
 \boxed{
 M_B\ge
 x_0(y_U-g)_+ +y_U(x_0-g)_+-M_A+L_m,
 \quad
 x_0=\left\lceil\frac{H_L}{a_*}\right\rceil,\quad
 y_U=\left\lceil\frac{H_L}{\ell}\right\rceil.
 }
\tag{10}
\]

For the critical clique endpoint, `alpha_L=1`, and (6) is exactly the
strong rectangle theorem `M_A>=H_L ceil(H_L/ell)`.  Thus this result
interpolates between arbitrary leaf support and that rigid endpoint,
without any loss from the synchronization defect.

## 4. Scope firewall

When `D_B` is quadratic, `a_B` may be linear and (9) may reduce to the
average-colour scale.  The theorem gives a sharper exact coordinate,
not a universal contradiction.  Erdős #809 remains open.
