# #679: revalidation of the inherited arbitrary-fixed-shift sparsity bound

Date: 2026-07-23

Status: **inherited result, revalidated in round 12; not a new result of this
round.**  Earlier campaign reports already recorded the consequence
\(N_{\varepsilon,K}(X)\ll_A X/(\log X)^A\) for every fixed \(A\).
This note checks the formal published source and repairs an easy fixed-divisor
pitfall in choosing the shifts.

## 1. Candidate set

Fix \(\varepsilon>0\) and \(K\), and let

\[
 {\cal G}_{\varepsilon,K}(X)=
 \left\{n\in[X,2X]:
 \omega(n-k)<(1+\varepsilon){\log k\over\log_2k}
 \quad(K\le k<n)\right\}.
\]

Put \(A=1+\varepsilon\), \(B=\log_2X\), and \(L=\log_3X\).

## 2. A shift family with no fixed prime divisor

Fix an integer \(r\ge2\), and put

\[
 P_r=\prod_{p\le r}p,\qquad k_0=\lfloor\log X\rfloor,\qquad
 k_j=k_0+jP_r\quad(0\le j<r).
\]

For large \(X\), all \(k_j\) lie in \([K,n)\) for every
\(n\in[X,2X]\).  On writing \(m=n-k_0\), the relevant fixed polynomials
are

\[
 Q_j(m)=m-jP_r\qquad(0\le j<r).
\]

They are distinct irreducible linear polynomials and are pairwise coprime.
Their product has no fixed prime divisor.  Indeed, if \(p\le r\), then
\(P_r\equiv0\pmod p\), so all \(Q_j(m)\equiv m\pmod p\), and \(m=1\)
is not a root.  If \(p>r\), their product has at most \(r<p\) residue
roots modulo \(p\).  This choice is essential: \(r\) genuinely consecutive
linear factors would have a fixed divisor for every prime \(p\le r\).

## 3. Direct use of Tenenbaum's proved theorem

Tenenbaum, *J. Number Theory* 188 (2018), Theorem 1
(arXiv:1710.04877), proves for every fixed number of such polynomials,
uniformly for \(1\le h_j\le R\log_2X\),

\[
 \#\{m\asymp X:\omega(Q_j(m))=h_j\ (0\le j<r)\}
 \ll_r {X\over(\log X)^r}
 \prod_{j<r}{(B+O_r(1))^{h_j-1}\over(h_j-1)!}.       \tag{1}
\]

The coefficient/discriminant factor in the theorem is fixed here because
the \(Q_j\)'s are fixed once \(r\) is fixed.  Its interval hypothesis is
met with any fixed \(\alpha<1\).  Applying it on
\((X-k_0,2(X-k_0)]\) leaves only \(O(k_0)=O(\log X)\) boundary points
from the original dyadic interval.

A candidate forces every one of the \(r\) values to obey

\[
 \omega(Q_j(m))\le
 q_X:={ (A+o(1))B\over L}.
\]

Eventually \(1\le q_X\le R B\), so (1) is in its stated uniform range.
Since \(q_X<B+O_r(1)\), the summands increase up to this endpoint and

\[
 \begin{split}
 T_X&:=\sum_{1\le h\le q_X}
       {(B+O_r(1))^{h-1}\over(h-1)!},\\
 \log T_X
 &\le { (A+o(1))B\over L}
       \{\,\log L+1-\log A\,\}
 =o(B).                                                \tag{2}
 \end{split}
\]

Summing (1) over the \(r\) exact levels therefore yields

\[
 \boxed{\#
 {\cal G}_{\varepsilon,K}(X)
 \ll_{\varepsilon,K,r}{X\over(\log X)^{r-o(1)}}.}       \tag{3}
\]

Equivalently, for every fixed \(C>0\),

\[
 \boxed{\#
 {\cal G}_{\varepsilon,K}(X)
 \ll_{\varepsilon,K,C}{X\over(\log X)^C}.}              \tag{4}
\]

Choose a fixed integer \(r>C\) in (3); the little-oh then absorbs
\(r-C\).

## 4. Claim boundary

Equation (3) formally contains the two-shift density bound as a weak
special case.  Independently, the \(r=2\), adjacent-shift estimate
\(X/(\log X)^{2-o(1)}\) follows directly from Goudout's **proved**
fixed-\(b=1\) corollary; no use of Goudout's remark about more shifts is
needed for that statement.

Even the all-fixed-\(C\) bound (4) does not prove that the candidate set is
finite: the implied constants are nonuniform in \(C\), and every fixed
upper bound is still much larger than one on a dyadic interval.  It neither
proves nor disproves the existence of infinitely many candidates.  The
original first question remains open.
