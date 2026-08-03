# An actual c=1 family negative at ranks five and six

For every odd `j`, set

\[
h=112\,2^{j-1},\qquad q=(2h+4)/3,
\qquad (k,r,u,b)=(4,9,12,q+4).
\]

Because `h=1 (mod 3)` for odd `j`, `q` is integral.  Direct substitution
gives

\[
\binom{b-1}{2}+2-\left(\binom q2+9\right)=2h,
\]

so these are actual dyadic states, not relaxed points.  Their first two
normalized tails are, for all sufficiently large `q`,

\[
\begin{aligned}
\alpha&=\binom{q-5}{2}+\binom{25}{1},&
\beta&=\binom{q-4}{2}+\binom{58}{1},\\
p&=\binom{q-6}{3}+\binom{q-10}{2}+\binom{269}{1},&
v&=\binom{q-5}{3}+\binom{q-9}{2}+\binom{1625}{1},\\
P&=\binom{q-6}{4}+\binom{q-11}{3}+\binom{q-15}{2}+\binom{35995}{1},&
V&=\binom{q-5}{4}+\binom{q-10}{3}+\binom{q-14}{2}+\binom{1319452}{1}.
\end{aligned}
\]

The words are canonical once all strict index inequalities hold; the
strongest is `q-14>1319452`, i.e. `q>1319466`.  This already holds on the
odd strip `j=17`.
Pascal cancellation then gives the literal formulas

\[
\gamma _3=23-4q,\quad
\gamma _4=1330-4q,\quad
\gamma _5=1283187-4q,\quad
\gamma _6=869828292418-4q.
\]

At the first checked failing strip `j=33`,

\[
q=320690891436,qquad
(\gamma _5,\gamma _6)=(-1282762282557,-412935273326).
\]

A direct full-orbit computation, independent of the normalized
cancellation, gives the same values and gives

\[
\gamma _7=129084548046247672655610>0.
\]

Thus the proposed universal two-row recovery is false on infinitely many
actual `c=1` states.  The first displayed witness still recovers at rank
seven, so this does not refute adaptive recovery or Erdős #776.

Guard:

```text
AMRA_MEMORY_KIB=1048576 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
amra-research-loop/scripts/run_bounded.sh python3 \
amra-research-loop/campaigns/erdos-776-c1-round3/evidence/verify_k4_r9_rank6_counterfamily.py
```
