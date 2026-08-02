# Independent audit of opposite-star defect-slack energy

Date: 2026-08-02

Auditor: OPG-1757 lane

Status: PASS

The audit independently checked the four interfaces in
`OPPOSITE_STAR_DEFECT_SLACK_ENERGY.md`:

1. \(\min\{\ell-1,\rho-2\}=\rho-2-(\rho-\ell-1)_+\) is the
   all-real identity \(\min\{a,x\}=x-(x-a)_+\).
2. The inherited definitions give
   \(\lambda=|A|+1-\delta(G)=g+2\).
3. Substitution into the exact reserve energy gives
   \(2H+R_L+\Xi-2(g+1)\ell\), with the displayed coefficient and sign.
4. Reserve failure is \(2|\mathcal Q|\le2D_B-2\); combining in that
   direction and writing \(H=D_B-Z\) gives
   \(R_L+\Xi\le2(g+1)\ell+2Z-2\).

The set-theoretic strengthening was also reconstructed from the original
zero-shore definitions.  Each \(bc\) is a missing pair, so
\(L\subseteq C\), \(b\in C\), and \(b\notin N(c)\) for every leaf.
Consequently

\[
 \{b\}\mathbin{\dot\cup}(L\setminus U)\subseteq C\setminus U=R,
\]

which proves \(r\ge t+1\) and the derived inequality (3a).

The verifier's domain \(\ell\ge1,\rho_c\ge2\) agrees with the actual
opposite-star domain: \(C\setminus N(c)\) contains both \(b\) and \(c\).
It checked 336,000 scalar profiles, of which 201,212 met both reserve
antecedents and 171,912 used a strict \(\Xi>0\) improvement; all 5
focused tests passed.

Verdict: PASS.  These are necessary constraints only; they do not empty
the B-opposite feasibility region or solve Erdős #809.
