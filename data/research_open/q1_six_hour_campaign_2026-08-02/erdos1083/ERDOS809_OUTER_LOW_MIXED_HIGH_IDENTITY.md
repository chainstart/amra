# Erdős #809 red-team addendum: exact elimination of the cross-low term

Date: 2026-08-02

Status: PROVED__INDEPENDENTLY_AUDITED

## 0. Result

Retain the maximum-witness setup and an integer \(q\ge2\) satisfying

\[
 M_B<\binom{q-1}{2}.
\]

Thus all high good edges form one pairwise-\(C_7\)-compatible family
and every colour contains at most one high good edge.

Let

\[
 H_q=G[A_{<q}].
\]

Define \(I_{\rm mix}(q)\) to be the number of colours whose unique
high good edge is internal to \(A\) and which also contain at least
one \(A\)--\(B\) good edge. Define \(N_{\rm int}(q)\) to be the number
of nonempty good colour classes which contain no high good edge and
no \(A\)--\(B\) edge. Then

\[
\boxed{
 R_A=e(H_q)+I_{\rm mix}(q)-N_{\rm int}(q).
}
\tag{1}
\]

In particular,

\[
\boxed{R_A\le e(H_q)+I_{\rm mix}(q).}
\tag{2}
\]

At the canonical threshold \(q=q_*(M_B)\), this is an unconditional
exact normal form. It eliminates the apparently free cross-low term

\[
 e(A,B_{<q})-N_{<q}
\]

from the outer residue. The actual positive obstruction is only a
mixed high-internal colour count. Purely low cross colours pay for
themselves exactly through \(D_B\) and the one-colour credit.

This does not close Branch A. It replaces its smallest unknown by the
more structured quantity \(I_{\rm mix}(q_*)\).

## 1. Colourwise proof

For a nonempty good colour \(\gamma\), write

\[
 t_\gamma=
 |\{\text{\(A\)--\(B\) edges of colour \(\gamma\)}\}|,
 \qquad
 a_\gamma=
 |\{\text{internal-\(A\) edges of colour \(\gamma\)}\}|.
\]

Split its low edges into

\[
 \ell_\gamma^B=
 |\{\text{low \(A\)--\(B\) edges}\}|,
 \qquad
 \ell_\gamma^A=
 |\{\text{low internal-\(A\) edges}\}|.
\]

Let \(j_\gamma\) indicate that the unique high edge, if present, is an
\(A\)--\(B\) edge, and let \(i_\gamma\) indicate that it is internal
to \(A\). Rich-outer compatibility gives

\[
 i_\gamma,j_\gamma\in\{0,1\},
 \qquad i_\gamma+j_\gamma\le1,
\tag{3}
\]

and

\[
 t_\gamma=\ell_\gamma^B+j_\gamma.
\tag{4}
\]

Let \(n_\gamma\) be the indicator that the class is wholly low. The
exact low-edge localization and the definition of \(D_B\) give the
colourwise contribution to \(R_A=D_A-D_B\):

\[
 r_\gamma
 =\ell_\gamma^A+\ell_\gamma^B-n_\gamma
  -(t_\gamma-1)_+.
\tag{5}
\]

If \(t_\gamma\ge1\), then (4) gives

\[
 \ell_\gamma^B-(t_\gamma-1)=1-j_\gamma.
\tag{6}
\]

There are now only four cases.

1. The unique high edge is cross: \(j_\gamma=1\). Then
   \(r_\gamma=\ell_\gamma^A\).
2. The unique high edge is internal and \(t_\gamma=0\). Then
   \(r_\gamma=\ell_\gamma^A\).
3. The unique high edge is internal and \(t_\gamma\ge1\). Then
   \(r_\gamma=\ell_\gamma^A+1\); this is exactly one
   \(I_{\rm mix}\) contribution.
4. There is no high edge. If \(t_\gamma\ge1\), the \(+1\) in (6)
   cancels the wholly-low credit \(n_\gamma=1\), giving
   \(r_\gamma=\ell_\gamma^A\). If \(t_\gamma=0\), then
   \(r_\gamma=\ell_\gamma^A-1\), exactly one negative
   \(N_{\rm int}\) contribution.

Summing (5) over colours proves

\[
 R_A=\sum_\gamma\ell_\gamma^A+
 I_{\rm mix}(q)-N_{\rm int}(q).
\]

As an independent check, the original defect definitions give the
same colourwise residue without using high/low language:

\[
 r_\gamma=
 \begin{cases}
 a_\gamma,&t_\gamma\ge1,\\
 (a_\gamma-1)_+,&t_\gamma=0.
 \end{cases}
\tag{7}
\]

Each of the four cases above reduces to this formula.

An internal \(A\)-edge is low precisely when both endpoints lie in
\(A_{<q}\). Therefore

\[
 \sum_\gamma\ell_\gamma^A=e(G[A_{<q}])=e(H_q),
\]

which proves (1).

## 2. Structural consequences

Choosing the unique high internal edge in every mixed colour injects
the \(I_{\rm mix}(q)\) colours into

\[
 E(G[A])\setminus E(H_q).
\]

Moreover these selected edges are pairwise \(C_7\)-compatible. Hence

\[
 I_{\rm mix}(q)
 \le e(G[A])-e(H_q),
\tag{8}
\]

and any hard counterexample must have

\[
 I_{\rm mix}(q)<\Phi(n,e).
\tag{9}
\]

The first inequality alone only recovers \(R_A\le e(G[A])\). The
useful gain is qualitative: every uncancelled cross-low unit is
anchored to a distinct high internal edge and to a mixed same-colour
pair. A future closure theorem can attack these anchored pairs rather
than the entire cross-low edge set.

## 3. Correct boundary

Equation (1) is an identity inside the maximum-witness good-edge
accounting. It does not say that \(I_{\rm mix}\) is small enough to be
absorbed by \(S_m\), nor that the negative credit \(N_{\rm int}\) is
large. It also does not close B-same or B-opposite.

At \(q=q_*\), the repaired canonical normal form therefore has the
sharper Branch-A gate

\[
 e(G[A_{<q_*}])+I_{\rm mix}(q_*)-N_{\rm int}(q_*)>S_m,
\]

instead of an unstructured cross-low residue.

## 4. Reproduction

\[
\texttt{python3 verify\_erdos809\_outer\_low\_mixed\_high\_identity.py}
\]

The verifier exhausts all colour profiles up to the stated finite
range. The all-parameter identity is the proof above.
