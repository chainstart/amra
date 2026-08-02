# Erdős #809 — common-coordinate rectangle transfers to the `B` budget

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Exact graph lemma

Let

\[
 A=N[v],\quad B=V(G)\setminus A,\quad
 m=|A|,\quad r_B=|B|,
\]

where `v` has maximum degree.  Put

\[
 g=m-\delta(G)-1=\Delta(G)-\delta(G)\ge0
\tag{1}
\]

and

\[
 L_m=\binom m2+\binom{r_B}2-e(G).
\tag{2}
\]

Suppose `X,Y subset A` are disjoint and anticomplete, with
`x=|X|`, `y=|Y|`.  Let `M_A,M_B` be the missing-edge counts inside
the two blocks.

### Theorem 1.1 (rectangle-to-budget transference)

One always has

\[
 \boxed{
 e(A,B)\ge x(y-g)_+ +y(x-g)_+,
 }
\tag{3}
\]

and consequently

\[
 \boxed{
 M_B\ge
 x(y-g)_+ +y(x-g)_+-M_A+L_m.
 }
\tag{4}
\]

If `E_A=M_A-xy` is the missing-`A` energy outside the forced
rectangle and `x,y>=g`, this becomes

\[
 \boxed{
 M_B\ge xy-g(x+y)-E_A+L_m.
 }
\tag{5}
\]

#### Proof

A vertex of `X` has at most `m-1-y` neighbours in `A`, so its degree
into `B` is at least

\[
 \delta(G)-(m-1-y)=y-g,
\]

clipped at zero.  Summing over `X`, and symmetrically over `Y`, proves
(3); the two edge sums are disjoint because their `A` endpoints lie in
disjoint sets.

The exact maximum-witness edge ledger is

\[
 e(A,B)=M_A+M_B-L_m.
\]

Substitution proves (4).  Since the `xy` pairs of `X cross Y` are
missing, `E_A=M_A-xy>=0`; expanding (4) when `x,y>=g` proves (5).
QED.

## 2. Opposite-star specialization

For the opposite star, take

\[
 X=N_A(b),\qquad
 Y=K_A=A\cap\bigcap_{c\in L}N(c).
\tag{6}
\]

The common-coordinate theorem proves that these sets are disjoint and
anticomplete and gives

\[
 y\ge
 \max\left\{0,
 \left\lceil
 \frac{\sum_{c\in L}d_A(c)+A_L}{\ell}
 \right\rceil-A_L
 \right\}.
\tag{7}
\]

Thus (4) is an exact route from opposite-star synchronization to the
actual missing-`B` budget.  In particular, if

\[
 g=o(n),\quad E_A=o(n^2),\quad L_m\ge0,
 \quad x,y=\Omega(n),
\]

then

\[
 M_B\ge xy-o(n^2).
\tag{8}
\]

This identifies the three losses that a hard synchronized star must
retain: degree spread `g`, missing energy outside its canonical
rectangle `E_A`, or failure of both coordinate sides to be linear.

## 3. Scope firewall

Equation (4) is exact, but it does not yet upper-bound the full colour
defect `D_B` by its right side.  At fixed positive density parameter,
`g` may be linear, and `E_A` may be quadratic.  The outer-`A` residue
is also untouched.  Maximum-degree Case 1 and Erdős #809 remain open.
