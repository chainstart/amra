# Independent audit of the opposite-star three-budget theorem

Date: 2026-08-02

Status: `INTERFACE_PASS`

Audited source: `OPPOSITE_STAR_THREE_BUDGET_CONSERVATION.md`

This is an independent hostile reconstruction of the interfaces used in
the theorem. It does not promote the still-open global feasibility claim.

## 1. Conservation identity

The disjoint decomposition

\[
 U=(L\cap U)\mathbin{\dot\cup}(A\cap U)
   \mathbin{\dot\cup}((U\cap B)\setminus L)
\]

gives

\[
 A_L=\ell s-2e(G[L])+E_A+E_B.
\]

Writing \(s=\ell-t\) and
\(2e(G[L])=\ell(\ell-1)-2\mu\) independently reproduces

\[
 A_L+\ell(t-1)=2\mu+E_A+E_B.
\]

In particular, the isolated-leaf correction has the displayed sign.

## 2. Injection into the actual reserve

The \(\mu\) objects are unordered missing pairs internal to \(L\).
The \(E_B\) objects are pairs \((c,z)\) with
\(c\in L\) and \(z\in (U\cap B)\setminus L\). These two families
are disjoint, neither has internal multiplicity, and every member is a
missing \(B\)-edge incident with an active zero-shore leaf. Therefore

\[
 |\mathcal Q|\ge \mu+E_B.
\]

Together with \(\mu\le\binom\ell2\), this yields the sharper scalar
elimination

\[
 2\mu+E_B\le |\mathcal Q|+
 \min\{|\mathcal Q|,\binom\ell2\}.
\]

## 3. Monotone reserve elimination

For

\[
 K=A_L+\ell(t-1),\qquad
 f(q)=\max\{0,K-q-\min(q,\tbinom\ell2)\},
\]

the function \(f\) is nonincreasing. Thus
\(|\mathcal Q|\le D_B-1\) implies \(\eta\ge\eta_B\) in the source
note. No reversal of the reserve inequality occurs.

## 4. Real rectangle and quadratic direction

The exact identity

\[
 E_A=\ell|Y|-\sum_{c\in L}d_A(c)
\]

and \(\sum_c d_A(c)\ge H\) give

\[
 |Y|\ge\left\lceil\frac{H+\eta_B}{\ell}\right\rceil.
\]

Independently, centre-colour supports are independent subsets of
\(G[L]\), so

\[
 |N_A(b)|\ge\left\lceil\frac H{a_*}\right\rceil.
\]

The opposite zero-shore condition makes \(N_A(b)\) and \(Y\) a genuine
anticomplete rectangle. Dropping ceilings gives

\[
 H(H+\eta_B)\le a_*\ell M_A.
\]

The left side is increasing for \(H\ge0\); solving the positive
quadratic and then taking the floor gives exactly the source note's
upper bound. The direction of every rounding step is correct.

## 5. Verdict

`INTERFACE_PASS`: the set decomposition, reserve injection, optimal
one-variable elimination, anticomplete rectangle, and quadratic-root
rounding all survive hostile reconstruction. The theorem strengthens
the opposite-star branch but does not prove that the entire #809 hard
normal form is infeasible.
