# Independent audit of the mixed-high outer-residue identity

Date: 2026-08-02

Status: PASS

Audited source:
../erdos1083/ERDOS809_OUTER_LOW_MIXED_HIGH_IDENTITY.md.

For one nonempty good colour, let \(t\) and \(a\) be its numbers of
cross and internal-\(A\) good edges. Its exact contribution to
\(R_A=D_A-D_B\) is

\[
 r_\gamma=t+a-1-(t-1)_+
 =\begin{cases}
 a,&t\ge1,\\
 a-1,&t=0.
 \end{cases}
\tag{1}
\]

Under \(M_B<\binom{q-1}{2}\), all high good edges are pairwise
\(C_7\)-compatible, so a colour contains at most one. Splitting that
possible edge into cross-high, internal-high, or absent gives:

- cross-high: all \(a\) internal edges are low, so (1) contributes
  \(\ell_\gamma^A\);
- internal-high and \(t=0\): \(\ell_\gamma^A=a-1\);
- internal-high and \(t\ge1\): \(\ell_\gamma^A=a-1\), plus exactly one
  mixed-colour correction;
- no high edge and \(t\ge1\): \(\ell_\gamma^A=a\);
- no high edge and \(t=0\): \(\ell_\gamma^A=a\), minus exactly one
  internal-only wholly-low colour credit.

Thus, colour by colour,

\[
 r_\gamma=\ell_\gamma^A+
 {\bf1}_{\rm mixed}-
 {\bf1}_{\rm internal\ only\ low}.
\]

Summing and observing that the low internal edges are exactly
\(E(G[A_{<q}])\) independently reproduces

\[
\boxed{
 R_A=e(G[A_{<q}])+I_{\rm mix}(q)-N_{\rm int}(q).
}
\]

Choosing the unique internal-high edge of each mixed colour is injective
and lands in one pairwise-\(C_7\)-compatible high-edge family. Hence the
source note's structural interpretation is also correct.

The separate verifier exhausts 4,960 colour profiles and 500 aggregate
prefixes; 4/4 focused tests pass. These checks guard the case split,
while the proof above is all-parameter.

Verdict: PASS. The identity eliminates the former free cross-low term,
but it does not bound \(I_{\rm mix}\), empty the Branch-A feasibility
region, or solve Erdős #809.
