# Independent audit of the Erdős #809 canonical hardness normal form

Date: 2026-08-02

Status: REPAIR

Audited source:
MAXIMUM_WITNESS_CANONICAL_HARDNESS_NORMAL_FORM.md.

This is a hostile read-only reconstruction. Every displayed formula
in the opposite-star composition survives, but the final branch list
is not exhaustive as written: the inherited same-neighbourhood
alternative is mentioned and then dropped. There is also one
overstatement of equivalence between the good-edge closure condition
and the total public colour target.

## 1. Exact outer-low coordinate: pass

Put

\[
 r_B=\frac{1+\sqrt{1+8M_B}}2,\qquad
 k=\lfloor r_B\rfloor,\qquad q_*=k+2.
\]

Since \(M_B\) is an integer and
\(\binom{k+1}{2}\) is the first triangular number strictly larger
than \(M_B\),

\[
 M_B<\binom{q_*-1}{2}.
\]

Thus the inherited rich-outer compatibility theorem applies at
\(q_*\).

For one nonempty good colour class, let \(n_\gamma\) be its number of
good edges and \(h_\gamma\in\{0,1\}\) its number of high edges.
If \(h_\gamma=1\), then

\[
 (n_\gamma-1)_+=n_\gamma-h_\gamma;
\]

if \(h_\gamma=0\), then

\[
 (n_\gamma-1)_+=(n_\gamma-h_\gamma)-1.
\]

Summing gives exactly

\[
 D_A=|E_{\rm low}|-N_{\rm low}.
\]

An internal \(A\)-edge is low precisely when both endpoints have
\(B\)-degree below \(q_*\), while an \(A\)--\(B\) edge has a forced
outer endpoint in \(B\). Hence

\[
 |E_{\rm low}|
 =e(G[A_{<q_*}])+e(A,B_{<q_*}).
\]

No orientation multiplicity remains. The exact identity and the
canonical threshold pass.

## 2. Internal-low dense exit: pass

Write \(m=|A|\), \(g=m-\delta(G)-1\), \(h=|A_{<q}|\), and
\(H=G[A_{<q}]\). For every \(a\in A_{<q}\),

\[
\begin{aligned}
 d_H(a)
 &\ge \delta(G)-(q-1)-(m-h)\\
 &=h-g-q.
\end{aligned}
\]

Therefore

\[
 \delta(H)\ge h-g-q,\qquad
 e(H)\ge \frac{h(h-g-q)}2.
\]

If \(h\ge2g+2q+5\), then

\[
 2\delta(H)-h\ge5,
\]

so every two edges of \(H\) lie on a common \(C_7\). A rainbow
\(C_7\)-colouring makes all those edges differently coloured. Thus a
genuine hard counterexample must satisfy

\[
 h\le2g+2q+4
 \quad\text{or}\quad e(H)<\Phi(n,e).
\]

In the second alternative, the density lower bound gives

\[
 h(h-g-q)<2\Phi(n,e).
\]

All constants, strict inequalities, and directions agree with
(3a)--(3b).

## 3. First wording repair: good-edge closure is not the total target

Let \(c_A\) be the number of colours represented on at least one good
edge. The exact identities are

\[
 c_A=|E_{\rm good}(A)|-D_A
\]

and

\[
 |E_{\rm good}(A)|-\Phi(n,e)=M_B+S_m.
\]

Consequently

\[
 D_A\le M_B+S_m
 \quad\Longleftrightarrow\quad
 c_A\ge\Phi(n,e).
\]

This is exact equivalence for closure by colours occurring on good
edges. It is only sufficient for the public total-colour target,
because colours supported wholly in \(G[B]\) also count. Conversely,
every actual counterexample to the public target must violate the
good-edge inequality.

Therefore Section 1 should replace “the full maximum-witness target is
equivalent” by:

> the good-edge closure condition is exactly (3), and every hard
> counterexample must violate it.

Likewise, the premise in Section 2 must be an actual hard
maximum-witness counterexample, or an instance not already closed by a
direct compatible family. Merely violating the error-free form of
(3) does not by itself imply the dense-exit restrictions: such an
instance may already have enough colours supported wholly in \(B\).

This repair narrows the premise and does not invalidate any necessary
condition for a genuine counterexample.

## 4. Reserve Branch A: pass

The reserve alternatives are exhaustive because all quantities are
integral:

\[
 |\mathcal Q|\ge D_B
 \quad\text{or}\quad
 |\mathcal Q|\le D_B-1.
\]

In the first branch,
\(\mathcal Q\subseteq\overline E(G[B])\) gives \(D_B\le M_B\).
If the good-edge closure condition fails, then

\[
\begin{aligned}
 R_A-S_m
 &=D_A-D_B-S_m\\
 &\ge D_A-M_B-S_m>0.
\end{aligned}
\]

Together with the outer-low identity, this is exactly the explicit
canonical outer residue claimed in (4).

## 5. Reserve Branch B: one missing subbranch

The exact inherited chain is:

1. GLOBAL_RESERVE_UNION_REDUCTION.md, Theorem 2.1, gives
   \(E_0\ge1\) under \(|\mathcal Q|\le D_B-1\); it also gives
   \(D_B\ge2\).
2. The maximum-degree setup inherited from THIRD_ATTACK.md has
   \(\delta(G)\ge3\), so the hypothesis \(\delta(G)\ge2\) of the
   weighted trichotomy is satisfied.
3. GLOBAL_WEIGHTED_OBSTRUCTION_TRICHOTOMY.md, Theorem 1.1, applies to
   any inclusion-maximal repeated-zero matching \(F\), \(f=|F|\).
   After the matching size and mass caps, its selected coherent star
   has one of two types.

The exact same-neighbourhood output is

\[
 \boxed{
 E_0\le4f(\kappa-1)L(D_B-1,\kappa),
 }
\]

where

\[
 L(q,\kappa)=
 \left\lfloor
 \frac{2\kappa+1+
 \sqrt{(2\kappa+1)^2+8q}}2
 \right\rfloor.
\]

This is equation (7) of GLOBAL_WEIGHTED_OBSTRUCTION_TRICHOTOMY.md,
obtained from MATCHING_STAR_CONCENTRATION.md, Theorem 2.1, and
SAME_STAR_RESERVE_ENERGY.md, equation (13).

If the selected type is opposite-neighbourhood, one obtains the star
used in (6)--(15). The source normal form says “Retain the opposite
case” and then presents only that system. But the same-star inequality
is a necessary constraint, not an elimination: it can hold. Hence the
later claim that the displayed list is exhaustive drops a live
quantified alternative.

The repair is to state three hard subbranches:

1. **A:** \(|\mathcal Q|\ge D_B\), with the outer residue (4);
2. **B-same:** \(|\mathcal Q|\le D_B-1\), the inherited matching caps,
   and the displayed same-star cap above;
3. **B-opposite:** \(|\mathcal Q|\le D_B-1\), the inherited matching
   caps, and (7)--(15).

Equivalently, one may say that violation of the same-star cap forces
the opposite subbranch. Without one of these formulations,
“Retain the opposite case” is not an exhaustive composition.

The same-star cap is sufficient as a complete explicit necessary
constraint for that subbranch. It is not sufficient to contradict
the subbranch in all parameter ranges, exactly as the scope firewall
already acknowledges.

It can also be made free of the selected matching parameter. With

\[
 d_0=\binom{\delta(G)}2,\qquad
 \overline M=\binom n2-e(G),
\]

the inherited matching-size bound gives

\[
 f\le
 \left\lfloor
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}}
 \right\rfloor.
\]

Hence Branch B-same obeys the completely scalar necessary condition

\[
\boxed{
 E_0\le
 4(\kappa-1)L(D_B-1,\kappa)
 \left\lfloor
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}}
 \right\rfloor.
}
\]

This is the cleanest self-contained form to insert into the canonical
list.

## 6. Opposite-star three-budget splice: pass

For the selected opposite star, the common-host identities give

\[
 A_L=R_L-\ell r,\qquad
 0\le r\le\kappa,\qquad
 0\le A_L\le\ell(\kappa-r).
\]

The inherited exact reserve energy gives (8), and substituting
\(\lambda=|A|+1-\delta(G)=g+2\) gives (9).

The three-budget identity was independently reconstructed as

\[
 A_L+\ell(t-1)=2\mu+E_A+E_B.
\]

The \(\mu\) missing pairs internal to \(L\) and the \(E_B\) missing
pairs between \(L\) and \((U\cap B)\setminus L\) are disjoint actual
reserve edges. Therefore

\[
 2\mu+E_B
 \le |\mathcal Q|+
 \min\{|\mathcal Q|,\tbinom\ell2\}.
\]

The function

\[
 q\longmapsto
 \max\{0,K-q-\min(q,\tbinom\ell2)\}
\]

is nonincreasing. Thus reserve failure gives
\(E_A\ge\eta_B\) with exactly the \(\eta_B\) in (11).

Also

\[
 E_A=\ell|U\cap A|-\sum_{c\in L}d_A(c)
 \le\ell|U\cap A|-H,
\]

so

\[
 |U\cap A|\ge
 \left\lceil\frac{H+\eta_B}{\ell}\right\rceil=y_0.
\]

Independent colour supports and
\(\binom{\alpha(G[L])}{2}\le|\mathcal Q|\le D_B-1\) give

\[
 |N_A(b)|\ge
 \left\lceil\frac H{a_*}\right\rceil=x_0.
\]

The two sets form a genuine disjoint anticomplete rectangle. Hence
(12) passes.

## 7. Rectangle transference and quadratic cap: pass

For \(x,y,g\ge0\), define

\[
 F_g(x,y)=x(y-g)_++y(x-g)_+.
\]

Checking the four regions cut out by \(x=g\) and \(y=g\) shows that
\(F_g\) is nondecreasing in each coordinate. Therefore replacing the
actual rectangle side lengths by the lower bounds \(x_0,y_0\) has the
direction claimed in (13).

Dropping ceilings in (12) gives

\[
 H(H+\eta_B)\le a_*\ell M_A.
\]

Here \(a_*\ge1\): reserve failure forces \(D_B\ge2\), and
\(\ell\ge1\). The left side is increasing for \(H\ge0\), so

\[
 H\le
 \left\lfloor
 \frac{\sqrt{\eta_B^2+4a_*\ell M_A}-\eta_B}{2}
 \right\rfloor.
\]

Finally the inherited concentration
\(E_0/(4f)\le H-\ell\) gives (13a), with the same floor and sign.
No monotonicity or rounding reversal occurs.

## 8. Nonfatal publication-interface repairs

The inherited theorem calls cover their mathematical hypotheses, but
the normal-form note should make the following imports explicit:

- retain the maximum-witness assumptions
  \(\delta(G)\ge3\), \(L_4(2)\), and a rainbow-\(C_7\) colouring;
- say inclusion-maximal matching, rather than leaving “maximal”
  potentially ambiguous;
- cite GLOBAL_RESERVE_UNION_REDUCTION.md, Theorem 2.1, for
  \(E_0\ge1\), and its Corollary 2.2 for \(D_B\ge2\);
- before (14), define
  \(P=N(b)\), \(C=V(G)\setminus P\), and
  \(\Psi_e(p)=\binom p2+\binom{n-p}{2}-e(G)\);
- either display the inherited matching size/mass caps or point to
  their exact equation numbers.

These are self-containment repairs, not failures of the composition.

## 9. Verdict and smallest remaining gates

Verdict: REPAIR, not FAIL.

- The outer-low identity, canonical threshold, dense internal exit,
  Branch A algebra, common-host coordinates, three-budget
  \(a_*/\eta_B\) splice, monotone rectangle transfer, and quadratic
  root are correct.
- The normal form must explicitly retain the same-star alternative.
- “Equivalent to the full target” and the premise “a finite instance
  violates (3)” must be narrowed to the good-edge closure route or to
  a genuine hard counterexample.

After those repairs, the smallest unproved gates are visible without
an undefined residual:

1. in Branch A, control the cross-low term
   \(e(A,B_{<q_*})-N_{<q_*}\) after the internal-low dense exit;
2. in Branch B-same, turn the surviving explicit same-star cap into a
   contradiction or a charge to \(M_A,M_B,S_m\);
3. in Branch B-opposite, prove the finite system (7)--(15) infeasible
   or extract the final pairwise-\(C_7\)-compatible colour family.

The current normal form, repaired as above, is a sound necessary
obstruction system. It does not yet prove Erdős #809.

Finite arithmetic guards in the #809 directory also pass
(\(4/4\) pytest cases), but the verdict above rests on the
all-parameter reconstruction, not on finite testing.

## 10. Final reaudit after repair

Reaudited the shared source after the root integrated the findings
above. The repaired history is:

1. the standing \(L_4(2)\), \(\delta(G)\ge3\), rainbow-\(C_7\), and
   maximum-witness assumptions are now explicit;
2. (3) is correctly described as exact good-edge closure, sufficient
   but not necessary for the public total-colour target;
3. the premise is a genuine hard counterexample, so failure of (3)
   and the direct dense-exit restrictions have the required
   quantifiers;
4. Branch B now records an inclusion-maximal matching and displays its
   size and colour-mass bounds;
5. Branch B-same retains the exact live cap (5c), while Branch
   B-opposite alone receives (6)--(15);
6. global failure explicitly imports \(E_0\ge1\) and \(D_B\ge2\);
7. \(U,\rho_c,P,C,\Psi_e\) are locally defined;
8. the final list now says precisely: every hard counterexample
   violates (3), satisfies the disjunction (3a), satisfies (3b) only
   in its second arm, and then lies in exactly one of A, B-same, or
   B-opposite.

The formulas (5a)--(5c), their inherited hypotheses, the selected-star
quantifier, and every subsequent equation number were checked again.
No composition jump remains.

Final reaudit verdict: **INTERFACE PASS**.

This verdict certifies the repaired document as an exhaustive
necessary normal form for the maximum-witness branch. It does not
claim that any of its three remaining feasibility regions is empty.

## 11. Post-audit pressure-test improvements

Two further exact ledgers were proved after the PASS verdict. They are
not needed for validity of the repaired normal form, but sharpen its
remaining gates.

First,
ERDOS809_OUTER_LOW_MIXED_HIGH_IDENTITY.md proves

\[
 R_A=e(G[A_{<q_*}])
     +I_{\rm mix}(q_*)-N_{\rm int}(q_*),
\]

where \(I_{\rm mix}\) counts colours whose unique high good edge is
internal to \(A\) and which also contain a low \(A\)--\(B\) edge, while
\(N_{\rm int}\) counts wholly-low colours having only internal good
edges. Thus the cross-low term cancels exactly; Branch A's actual
positive gate is the anchored mixed-high count.

Second, ERDOS809_ZERO_STAR_DEFECT_MASS_LEDGER.md proves for every
selected zero-star

\[
 H\le D_B.
\]

For a repeated-zero selected star this gives

\[
 2\ell\le H\le D_B,\qquad
 E_0\le4f(D_B-\ell).
\]

Both statements have all-parameter proofs and independent finite
arithmetic guards. They further reduce, but do not eliminate, the
three repaired feasibility branches.
