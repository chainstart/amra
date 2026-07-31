# Erdős #809 — seventh attack: quantified zero-star stability

Date: 2026-07-31

Status:
EXACT_OPPOSITE_CORE_ENERGY_AND_WEIGHTED_RESIDUAL_DICHOTOMY_PROVED__RESIDUAL_MOMENT_CONTROL_OPEN

## 1. Outcome

The sixth attack shows that neither uniformly low rectangle overlap nor
\(E_0=o(n^2)\) is true in general. This attack replaces those false
targets with two quantitative exits.

1. **Absorption exit.** For any integer \(H\ge 2\), the maximum-witness
   branch closes whenever
   \[
   R_A+(H-1)M_B+\frac{2Q_A}{H}\le S_m,                       \tag{1}
   \]
   where
   \[
   Q_A=\sum_{aa'\in\overline E(A)}d_B(a)d_B(a').
   \]
2. **Aligned-core exit.** An opposite-type zero-shore pair \(bc\) with
   small
   \[
   \rho(b,c)=n-d(b)-d(c)                                    \tag{2}
   \]
   yields a two-block partition with an explicit missing-edge bound.
   If the maximum-degree excess is \(o(n)\) and
   \(\rho(b,c)=o(n)\), one block has size
   \((1/2+s-o(1))n\) and misses only \(o(n^2)\) clique edges.

For a weighted opposite zero-star, the correct parameter is not its
total weight alone but its weighted residual average
\[
\bar\rho_b
=
\frac{\sum_c(h_{bc}-1)_+\rho(b,c)}
     {\sum_c(h_{bc}-1)_+}.                                  \tag{3}
\]
Some positively weighted leaf satisfies
\(\rho(b,c)\le\bar\rho_b\), giving a fully explicit core bound. In the
three-hub two-clique family, the weighted matched pair has
\(\rho(b,c)=O(1)\), so the pair certificate detects its aligned clique
core and is near-sharp there.

What is not proved is that failure of the absorption exit forces
\(\bar\rho_b=o(n)\) for some opposite star. At fixed \(s\), the older
bound
\[
\bar\rho_b\le n-2\delta=(2s+o(1))n
\]
still leaves a quadratic error. Same-neighbourhood mass also requires a
global complete-split synchronization theorem. Erdős #809 remains open.

## 2. Quantitative absorption exit

Recall from FOURTH_ATTACK.md that
\[
D_B\le M_B+E_0,
\qquad
D_A=R_A+D_B.                                                \tag{4}
\]
The sixth-stage high/low theorem gives, for every integer \(H\ge2\),
\[
E_0\le(H-1)M_B+\frac{2Q_A}{H}.                              \tag{5}
\]

### Proposition 2.1

If (1) holds for some integer \(H\ge2\), then
\[
D_A\le M_B+S_m,
\]
and the maximum-degree branch closes.

#### Proof

Combining (4) and (5) gives
\[
\begin{aligned}
D_A
&\le M_B+R_A+(H-1)M_B+\frac{2Q_A}{H}\\
&\le M_B+S_m.
\end{aligned}
\]
\(\square\)

This is a checkable sufficient condition. It is not asserted to hold
automatically.

## 3. Exact opposite-pair core energy

Fix an opposite-type zero-shore pair \(bc\). Put
\[
P=N(b),\qquad Q=N(c),\qquad p=|P|=d(b),\qquad q=|Q|=d(c).
\]
Opposite type means
\[
P\cap Q=\varnothing,
\qquad
E(P,Q)=\varnothing.                                        \tag{6}
\]
Let
\[
C=V(G)\setminus P,\qquad
L=C\setminus Q,\qquad
\rho=|L|=n-p-q.                                             \tag{7}
\]
Every edge of the cut \((P,C)\) has its endpoint in \(C\) inside \(L\),
so
\[
e(P,C)\le p\rho.                                            \tag{8}
\]
For every vertex set \(J\), write
\[
M(J)=\binom{|J|}{2}-e(G[J]).
\]
Define
\[
\Psi_e(p)
=
\binom p2+\binom{n-p}{2}-e(G).                              \tag{9}
\]

### Theorem 3.1 (exact opposite-core energy)

\[
\boxed{
M(P)+M(C)
=
\Psi_e(p)+e(P,C)
\le
\Psi_e(p)+p\rho.
}                                                            \tag{10}
\]

#### Proof

The edge partition gives
\[
e(G)
=
\binom p2-M(P)
+
\binom{n-p}{2}-M(C)
+e(P,C).
\]
Rearranging proves the identity, and (8) proves the inequality.
\(\square\)

Thus both sides of the partition are simultaneously close to cliques
whenever the right-hand side of (10) is small.

## 4. Normalized aligned-core theorem

Assume the fixed-\(s\) normalization
\[
e(G)=\left(\frac14+s^2+o(1)\right)n^2,
\qquad
\delta(G)\ge\left(\frac12-s-o(1)\right)n.                   \tag{11}
\]
Measure maximum-degree overshoot by
\[
\zeta
=
\max\left\{
0,\frac{\Delta(G)}n-\left(\frac12+s\right)
\right\}.                                                   \tag{12}
\]
Write
\[
\alpha=\frac pn,
\qquad
r=\frac\rho n.
\]
Expanding (9) using (11) gives
\[
\frac{\Psi_e(p)}{n^2}
=
\left(\alpha-\frac12\right)^2-s^2+o(1).                    \tag{13}
\]
Because \(\delta\le p\le\Delta\), equations (11) and (12) imply
\[
\left|\alpha-\frac12\right|\le s+\zeta+o(1),
\]
and hence
\[
\frac{\Psi_e(p)}{n^2}
\le
2s\zeta+\zeta^2+o(1).                                      \tag{14}
\]

### Corollary 4.1 (parameterized aligned core)

Let \(R\) be the larger of \(P\) and \(C\). Then
\[
\frac{|R|}{n}
\ge
\frac12+
\sqrt{\left(s^2-\alpha r-o(1)\right)_+},                   \tag{15}
\]
and
\[
\boxed{
M(R)
\le
\left(2s\zeta+\zeta^2+\alpha r+o(1)\right)n^2.
}                                                            \tag{16}
\]

#### Proof

Since \(M(R)\le M(P)+M(C)\), equations (10) and (14) give
(16). Also, \(M(P)+M(C)\ge0\), so (10) implies
\[
0\le\Psi_e(p)+p\rho.
\]
After division by \(n^2\), equation (13) yields
\[
\left|\alpha-\frac12\right|
\ge
\sqrt{\left(s^2-\alpha r-o(1)\right)_+}.
\]
Finally,
\[
\frac{|R|}{n}
=
\frac12+\left|\alpha-\frac12\right|,
\]
which proves (15). \(\square\)

In particular,
\[
\zeta=o(1),
\qquad
\rho=o(n)                                                   \tag{17}
\]
imply
\[
|R|\ge(1/2+s-o(1))n,
\qquad
M(R)=o(n^2).                                                \tag{18}
\]
The dense-core theorem in SECOND_ATTACK.md then supplies the required
pairwise \(C_7\)-compatible family.

Equation (16) is the correct parameterized replacement when an
\(o(n^2)\) conclusion is unavailable. The coarse R003 estimate
\[
\rho\le\kappa=n-2\delta
\]
gives only
\[
M(R)
\le
\left(
2s\zeta+\zeta^2
+\alpha\frac{\kappa}{n}
+o(1)
\right)n^2,                                                 \tag{19}
\]
which remains quadratic for fixed \(s>0\).

## 5. Weighted opposite-star theorem

Fix \(b\), and let \(\mathcal O_b\) be its opposite-type zero-shore
neighbours. Put
\[
w_{bc}=(h_{bc}-1)_+,
\qquad
\Omega_b=\sum_{c\in\mathcal O_b}w_{bc}.                     \tag{20}
\]
When \(\Omega_b>0\), define the residual moment and average
\[
\mathcal R_b
=
\sum_{c\in\mathcal O_b}w_{bc}\rho(b,c),
\qquad
\bar\rho_b=\frac{\mathcal R_b}{\Omega_b}.                   \tag{21}
\]

### Theorem 5.1 (weighted-star core certificate)

There is a \(c\in\mathcal O_b\) with \(w_{bc}>0\) such that
\[
\rho(b,c)\le\bar\rho_b.                                     \tag{22}
\]
Consequently, with \(\alpha=d(b)/n\), some block \(R_b\) obeys
\[
\frac{|R_b|}{n}
\ge
\frac12+
\sqrt{
\left(
s^2-\alpha\frac{\bar\rho_b}{n}-o(1)
\right)_+},                                                 \tag{23}
\]
and
\[
M(R_b)
\le
\left(
2s\zeta+\zeta^2
+\alpha\frac{\bar\rho_b}{n}
+o(1)
\right)n^2.                                                 \tag{24}
\]

#### Proof

Equation (22) follows by weighted averaging. Apply Corollary 4.1 to the
selected leaf. \(\square\)

Since every opposite pair satisfies \(\rho\le\kappa\), one always has
\[
\bar\rho_b\le\kappa.                                        \tag{25}
\]
At fixed \(s\), this recovers only (19). The gain required for an
asymptotically complete aligned core is precisely
\[
\bar\rho_b=o(n).                                            \tag{26}
\]

## 6. Global residual-moment interface

Let
\[
E_0^{\mathrm{opp}}
=
\sum_{bc\ \mathrm{opposite}}w_{bc},
\qquad
\mathcal R_{\mathrm{opp}}
=
\sum_{bc\ \mathrm{opposite}}w_{bc}\rho(b,c).                \tag{27}
\]
If \(E_0^{\mathrm{opp}}>0\), weighted averaging selects an opposite
pair satisfying
\[
\rho(b,c)
\le
\frac{\mathcal R_{\mathrm{opp}}}{E_0^{\mathrm{opp}}}.        \tag{28}
\]

### Corollary 6.1 (conditional global stability)

If
\[
\zeta=o(1),
\qquad
\mathcal R_{\mathrm{opp}}
=o\left(nE_0^{\mathrm{opp}}\right),                          \tag{29}
\]
then an aligned core satisfying (18) exists.

The residual moment also has the exact degree form
\[
\mathcal R_{\mathrm{opp}}
=
nE_0^{\mathrm{opp}}
-
\sum_{bc\ \mathrm{opposite}}
w_{bc}\bigl(d(b)+d(c)\bigr).                                \tag{30}
\]
Thus (29) says that the excess weight is concentrated on zero pairs
whose degree sums are \(n-o(n)\).

Neither \(E_0\), \(Q_A\), nor the coarse bound
\(\rho\le\kappa\) currently proves (29). This weighted degree-sum
control is the exact new gap in the opposite branch.

## 7. What remains in the same-neighbourhood branch

For a same-type zero edge, SIXTH_ATTACK.md gives
\[
h_{bc}\le\kappa,
\qquad
|N(b)\mathbin\triangle N(c)|\le2\kappa.                     \tag{31}
\]
R003 also gives an independent common-neighbour block
\[
|N(b)\cap N(c)|\ge3\delta-n
\]
that is anticomplete to the symmetric difference. When
\(\kappa=o(n)\), this is the near-complete-split closure already proved.
For fixed \(s\), both error bounds are linear. A quadratic amount of
same-type weight must be synchronized across different centres before
one obtains a single global complete-split core. No such
synchronization is claimed here.

## 8. Audit against the three-hub family

In the sixth-stage three-hub family, choose a matched
\(u\in U\) and \(w\in W\). Then
\[
P=N(u),
\qquad
Q=N(w),
\qquad
P\cap Q=\varnothing,
\]
and
\[
\rho(u,w)=O(1).
\]
The direct opposite-pair certificate therefore applies. In the
verified finite coloring, the corresponding positive-weight star is
supported on this matched leaf, so its weighted residual average is
also \(O(1)\). Moreover, \(\zeta=o(1)\) along the family. Corollary 4.1
recovers a block of size \((1/2+s-o(1))n\) with \(o(n^2)\) missing
edges; this is \(C_1\), up to \(O(1)\) vertices. The model is therefore
an equality/near-equality witness for the new stability parameter, not
a counterexample to it.

## 9. Exact seventh-stage alternative

The proved exits are now:

1. condition (1) holds and the defect is absorbed;
2. an opposite edge has small \(\rho\), and (15)--(16) produce a
   parameterized core.

If neither exit applies, the proved information only says that every
substantial opposite weighted star has a linear residual average, or
the maximum-degree overshoot \(\zeta\) is non-negligible, or substantial
excess lies in the unsynchronized same-type branch. This is a precise
description of the remaining state space, not a closure. In particular,
no finite or local statement here is extrapolated to the fixed-\(s\)
theorem.

## 10. Verification

The verifier verify_809_seventh_attack.py checks the following on the
34-vertex three-hub model:

1. the exact identity (10), including
   \[
   M(P)+M(C)=\Psi_e(p)+e(P,C);
   \]
2. the cut bound \(e(P,C)\le p\rho\);
3. the opposite-star complement error, weighted residual moment, and
   weighted-average selection;
4. a finite numerical instance of the absorption condition (1).

The command

    python3 -m unittest -v test_809_seventh_attack.py

returns

    Ran 3 tests
    OK

## 11. Claim boundary

- Quantitative absorption condition (1): **proved sufficient**.
- Exact opposite-core energy identity (10): **proved**.
- Parameterized core bounds (15)--(16): **proved**.
- Weighted-star certificate (23)--(24): **proved**.
- Conditional global stability under (29): **proved**.
- Failure of absorption automatically implies (29): **open**.
- Fixed-\(s\) synchronization of same-type stars: **open**.
- Full aggregate stability dichotomy: **open**.
- Maximum-degree Case 1 and Erdős #809: **open / not claimed**.
