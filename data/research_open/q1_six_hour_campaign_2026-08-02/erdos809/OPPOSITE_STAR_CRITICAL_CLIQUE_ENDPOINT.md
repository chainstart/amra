# Erdős #809 — the critical clique endpoint has disjoint colour support

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Rigid endpoint

Let an opposite active zero-star have `ell` leaves and synchronization
defect `A_L=ell`.  Assume its leaf graph is nonempty.  The exact
leaf-deficit rigidity theorem gives

\[
 G[L]=K_\ell,
 \qquad
 N(c)=U\setminus\{c\}\quad(c\in L).
\tag{1}
\]

For each leaf `c`, let `Gamma_c` be the set of colours in which `b,c`
are both outer endpoints.  Thus

\[
 h_c=|\Gamma_c|,
 \qquad
 H_L=\sum_{c\in L}h_c.
\tag{2}
\]

## 2. Disjoint colour support

### Theorem 2.1 (critical clique coordinate rectangle)

The sets `Gamma_c`, `c in L`, are pairwise disjoint.  If

\[
 X=N_A(b),\qquad Y=A\cap U,
\]

then `X,Y` are disjoint and anticomplete and

\[
 |X|\ge H_L,
 \qquad
 |Y|\ge\max_c h_c\ge
 \left\lceil\frac{H_L}{\ell}\right\rceil.
\tag{3}
\]

Consequently,

\[
 \boxed{
 M_A\ge
 H_L\left\lceil\frac{H_L}{\ell}\right\rceil.
 }
\tag{4}
\]

#### Proof

Every two outer endpoints belonging to one good colour form an active
base pair and hence a missing pair in `B`.  If one colour belonged to
both `Gamma_c` and `Gamma_d`, then the adjacent clique leaves `c,d`
would be a missing pair, a contradiction.  Thus the colour sets are
disjoint.

Distinct colours incident with the outer endpoint `b` use distinct
good `A`--`b` edges, so disjointness gives `d_A(b)=|X|>=H_L`.
Equation (1) gives one common leaf `A`-neighbourhood

\[
 N_A(c)=A\cap U=Y.
\]

The `h_c` colour coordinates at `c` are distinct elements of `Y`, so
`|Y|>=max h_c>=ceil(H_L/ell)`.  Finally, the opposite zero-shore
condition makes `N(b)` anticomplete to `U`; hence `X` is anticomplete
to `Y`, and its rectangle consists of missing edges inside `A`.  This
proves (4).  QED.

## 3. Consequences

The rectangle-to-budget theorem also gives, with

\[
 y_0=\left\lceil\frac{H_L}{\ell}\right\rceil,
 \qquad g=|A|-\delta(G)-1,
\]

the direct lower bound

\[
 \boxed{
 M_B\ge
 H_L(y_0-g)_+ +y_0(H_L-g)_+-M_A+L_m.
 }
\tag{5}
\]

Moreover, (4) implies

\[
 H_L\le\left\lfloor\sqrt{\ell M_A}\right\rfloor.
\tag{6}
\]

If this is the opposite star selected by a maximal repeated-zero
matching of size `f`, then `E_0/(4f)<=W=H_L-ell`, and therefore

\[
 \boxed{
 E_0\le
 4f\left(\left\lfloor\sqrt{\ell M_A}\right\rfloor-\ell\right).
 }
\tag{7}
\]

A negative right side means that the critical clique endpoint is
impossible.  Thus both sides of the first synchronization transition
have explicit weighted caps: `A_L<ell` is controlled by the
reserve/coordinate cap, and the nonempty `A_L=ell` endpoint is
controlled by (7).

## 4. Scope firewall

The empty-leaf-graph possibility at `A_L=ell` is not covered by the
disjoint-support improvement (although the earlier reserve bounds still
apply).  Defects `A_L>ell` admit nonrigid intermediate supports.  The
theorem is a closed endpoint estimate, not a proof of Erdős #809.
