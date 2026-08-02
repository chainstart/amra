# Erdős #809 — common-coordinate missing-energy theorem

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

Use the maximum-degree partition

\[
 A=N[v],\qquad B=V(G)\setminus A,
\]

and an opposite-type active zero-star with centre `b in B` and leaf set
`L subset B`, `|L|=ell`.  As in the common-host theorem, put

\[
 P=N(b),\quad Q_c=N(c),\quad
 U=\bigcup_{c\in L}Q_c,
\]

and define

\[
 a_c=|U\setminus Q_c|,\qquad A_L=\sum_{c\in L}a_c.
\tag{1}
\]

Write `d_A(x)=|N(x) intersect A|`, and let `M_A` be the number of
missing edges inside `A`.

## 2. Exact common-coordinate theorem

### Theorem 2.1

The common leaf-coordinate set

\[
 K_A=A\cap\bigcap_{c\in L}N(c)
\tag{2}
\]

satisfies

\[
 \boxed{
 |K_A|
 \ge
 \max\left\{0,\max_{c\in L}(d_A(c)+a_c)-A_L\right\}
 }
\tag{3}
\]

and hence

\[
 \boxed{
 |K_A|
 \ge
 \max\left\{0,
 \left\lceil
 \frac{\sum_{c\in L}d_A(c)+A_L}{\ell}
 \right\rceil-A_L
 \right\}.
 }
\tag{4}
\]

Moreover, `N_A(b)` and `K_A` are disjoint and anticomplete, so

\[
 \boxed{M_A\ge d_A(b)|K_A|.}
\tag{5}
\]

#### Proof

Fix `c in L`.  Every vertex of `N_A(c)` lies in `Q_c subset U`.  A
member of `N_A(c)` that is absent from the common intersection in (2)
belongs to `U\setminus Q_d` for at least one other leaf `d`.  Therefore

\[
 |K_A|
 \ge d_A(c)-\sum_{d\ne c}a_d
 =d_A(c)+a_c-A_L.
\]

Taking the maximum over `c`, clipping at zero, and then averaging the
integers `d_A(c)+a_c` proves (3)--(4).

The opposite zero-shore condition says that `P=N(b)` is disjoint and
anticomplete to every `Q_c`, hence to `U`.  Thus
`N_A(b)=A intersect P` and `K_A subset A intersect U` form a missing
rectangle inside `A`.  Its `d_A(b)|K_A|` pairs are all distinct, proving
(5).  QED.

## 3. Colour-mass corollary

Let `h_c` be the active-pair colour multiplicity of `bc`, and put

\[
 H_L=\sum_{c\in L}h_c.
\]

Each common colour supplies a distinct `A`-neighbour of `c`, so
`d_A(c)>=h_c`.  At the centre, one `A`-edge can represent only one
colour, while any one colour contains at most all `ell` leaves.  Hence

\[
 d_A(b)\ge\left\lceil\frac{H_L}{\ell}\right\rceil.
\]

Equations (4)--(5) give the exact integer certificate

\[
 \boxed{
 M_A\ge
 \left\lceil\frac{H_L}{\ell}\right\rceil
 \max\left\{0,
 \left\lceil\frac{H_L+A_L}{\ell}\right\rceil-A_L
 \right\}.
 }
\tag{6}
\]

Together with the synchronization--reserve theorem,

\[
 |\mathcal Q|
 \ge\binom\ell2-
 \binom{\min\{\ell,A_L\}}2,
\tag{7}
\]

this is a simultaneous two-budget obstruction.  Small synchronization
defect forces both an actual `B`-reserve expenditure and an `A`-side
missing rectangle.

### Corollary 3.1 (perfect synchronization pays total colour mass)

If `A_L=0`, then all leaf neighbourhoods equal `U`, and

\[
 |\mathcal Q|\ge\binom\ell2,
 \qquad
 M_A\ge\left\lceil\frac{H_L}{\ell}\right\rceil^2.
\]

Consequently

\[
 \boxed{|\mathcal Q|+M_A\ge H_L.}
\tag{8}
\]

Indeed, put `x=ceil(H_L/ell)`, so `H_L<=ell x`.  For `ell>=2`,

\[
 \binom\ell2+x^2-\ell x\ge0
\]

because its discriminant as a quadratic in `x` is
`2ell-ell^2<=0`; for `ell=1`, the assertion is `x^2>=x`.
Thus a perfectly synchronized high-multiplicity star cannot avoid
paying its full colour mass into the two genuine missing-edge budgets.

### Corollary 3.2 (defect-stable two-budget inequality)

For arbitrary synchronization defect `A_L`, put

\[
 x=\left\lceil\frac{H_L}{\ell}\right\rceil.
\]

Then

\[
 \boxed{
 |\mathcal Q|+M_A
 \ge
 H_L-A_Lx-\binom{A_L}{2}.
 }
\tag{9}
\]

If `A_L<=ell`, equations (6)--(7) give

\[
 |\mathcal Q|+M_A
 \ge
 \binom\ell2-\binom{A_L}2+x(x-A_L).
\]

The elementary inequality `binom(ell,2)+x^2>=ell*x>=H_L`
proves (9).  If `A_L>ell`, its right side is already nonpositive
because `A_L*x>=ell*x>=H_L`, so (9) remains true.  Thus the perfect
endpoint has an explicit stable extension; the loss is polynomial in
the total synchronization deficit, not in the common residual `r`.

### Corollary 3.3 (global perfect-star weighted cap)

Suppose this opposite star is the one selected from a maximal
repeated-zero matching of size `f` by the inherited global weighted
trichotomy, and suppose global reserve failure holds.  If `A_L=0`, then

\[
 \boxed{
 E_0\le4f\bigl(M_A+D_B-1-\ell\bigr).
 }
\tag{10}
\]

Indeed, the concentration theorem gives
`W=H_L-ell>=E_0/(4f)`, while Corollary 3.1 and reserve failure give

\[
 H_L\le M_A+|\mathcal Q|\le M_A+D_B-1.
\]

Combining the two inequalities proves (10).  A negative right side
means that the perfect-synchronization branch is impossible.  This is
an explicit opposite-star endpoint cap; it does not control positive
`A_L` without the loss in Corollary 3.2.

### Corollary 3.4 (closed cap below one deficit per leaf)

In the same global-obstruction setting, put

\[
 a=A_L,\qquad B_0=M_A+D_B-1.
\]

If `0<=a<ell`, then

\[
 \boxed{
 H_L\le
 \left\lfloor
 \frac{\ell\left(B_0+\binom a2\right)+a(\ell-1)}
      {\ell-a}
 \right\rfloor.
 }
\tag{11}
\]

Consequently the star selected by the inherited matching concentration
obeys

\[
 \boxed{
 E_0\le4f\left(
 \left\lfloor
 \frac{\ell\left(B_0+\binom a2\right)+a(\ell-1)}
      {\ell-a}
 \right\rfloor-ell
 \right).
 }
\tag{12}
\]

To prove (11), combine Corollary 3.2 with
`|mathcal Q|<=D_B-1` to obtain

\[
 H_L\le B_0+a\left\lceil\frac{H_L}{\ell}\right\rceil
              +\binom a2.
\]

Now use

\[
 \left\lceil\frac{H_L}{\ell}\right\rceil
 \le\frac{H_L+\ell-1}{\ell}
\]

and rearrange; the denominator is positive because `a<ell`.
Equation (12) follows from `E_0/(4f)<=W=H_L-ell`.

Thus every opposite-star obstruction below one total synchronization
deficit per leaf has a closed weighted cap.  Any obstruction violating
(12) must satisfy the sharp integer threshold `A_L>=ell`.

## 4. Sharpness and scope firewall

### 4.1 Full-contract equality model

The three-clique-chain construction from the inherited eighth attack
shows that (6) can be exactly sharp under the full BCM contract.  In
that construction take a matched pair `b in U_0`, `c in W_0`, with
`|U_0|=|W_0|=|X|=|Y|=k` and maximum-degree witness

\[
 A=H\cup X\cup Y.
\]

For the one-leaf opposite star,

\[
 d_A(b)=d_A(c)=h_c=k,\qquad A_L=0,\qquad K_A=Y,
\]

while the only missing pairs in `A` form `X cross Y`.  Hence

\[
 M_A=k^2=d_A(b)|K_A|,
\]

and the right side of (6) is also `k^2`.  The model has `L_4(2)`, an
exact maximum-degree BCM witness, and a rainbow-`C_7` colouring, while
its true defect is paid by `M_B`.  Thus no uniform improvement of (6)
is possible without using additional global information.

### 4.2 Remaining boundary

The certificate is parametric: it does not yet force `A_L` to be small,
or `ell,H_L` to be large enough relative to `M_A,D_B`.  It therefore
does not close the intermediate opposite-star regime or the separate
outer-`A` residue.  Erdős #809 remains open.
