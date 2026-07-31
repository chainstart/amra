# Independent audit — reserve-Hall attack on Erdős #809

Date: 2026-07-31

Audit mode: read-only reconstruction by the #1083 research agent; the
root agent applied two wording corrections after the audit.

## Verdict

| Item | Verdict |
|---|---|
| Zero-shore reserve validity | **PASS** |
| Nonempty-shore base-pair uniqueness | **PASS** |
| Hall injection and compressed deficiency | **PASS** |
| Outer-\(A\) quantifier firewall | **PASS** |
| Balanced three-clique-chain calculation | **PASS** |
| Unbalanced three-hub calculation | **PASS** |
| Universal reserve-expansion conjecture | **OPEN / NOT AUDITED AS A THEOREM** |

## Reconstruction

For a zero-shore pair \(bc\), any distinct
\(p\in N_B(b),q\in N_B(c)\) with \(pq\in E(G)\) would give the simple
shore path \(b-p-q-c\).  Hence the neighbourhood rectangle and the
explicitly missing incident stars in \(\mathcal K(bc)\) consist only of
missing \(B\)-edges.  Exhaustion on every graph of order at most six
checked 78,008 zero-shore instances without a failure.

After a root is fixed, one colour cannot create the same token base pair
twice.  If a nonempty-shore pair were shared by two colours, the
coefficient-one fixed-pair theorem from `FOURTH_ATTACK.md` would be
violated.  Therefore the direct charges \(C_+\) are pairwise distinct.
Deleting them from the Hall right side and saturating all zero-shore
tokens gives a genuine injection of all \(D_B\) tokens into the \(M_B\)
missing edges.  Hall failure gives the stated deficient subfamily.

No outer-\(A\) term is silently discarded.  The theorem controls
\(D_B\), and closes \(D_A\) only when all repeated colours are
outer-\(B\) supported or the separate inequality \(R_A\le S_m\) is
available.

For the balanced chain, every reserve is the complete missing block
\(U\times W\), so \(k^2\) tokens match its \(k^2\) edges.  In the
three-hub family, a token set meeting \(g\) groups has at most
\((u+3)g\) tokens and a candidate union of at least \(uw+4g\) edges;
the Hall margin is

\[
u(w-g)+g\ge0.
\]

## Corrections made after audit

1. Roots are selected only for colours with \(t_\gamma\ge1\); a colour
   with no outer-\(B\) edge has no \(D_B\) token.
2. The rectangle count in Lemma 3.2 is now written as
   \(ab-r(r+1)/2\ge\binom{\min(a,b)}2\), rather than implying equality
   whenever only one neighbourhood contains the other.

Neither correction changes a theorem statement or inequality.
