# Independent audit: the `k=4`, `r=9` rank-six counterfamily

Verdict: **pass as an infinite actual counterfamily to M305 and fixed
two-row recovery; no implication for adaptive recovery or Erdős #776**.

The audit used a new greedy Macaulay engine and did not import the author's
verifier.

## 1. Actual dyadic family

For odd `j`, define

\[
h=112\,2^{j-1},\qquad q={2h+4\over3},\qquad
(k,r,u,b)=(4,9,12,q+4).
\]

Since `j-1` is even, `2^(j-1)=1 (mod 3)`, hence `h=1 (mod 3)` and
`q` is integral.  With

\[
n=\binom q2+9,\qquad H=\binom b2+1,\qquad \tau=H-n,
\]

direct cancellation gives

\[
\binom{b-1}{2}+2-\left(\binom q2+9\right)
=3q-4=2h.
\]

Thus every odd `j` is an actual dyadic state, not a relaxed phase point.
The subsequence satisfies `q_(j+2)=4q_j-4` and is strictly increasing.

## 2. Blind orbit reconstruction

Let `U_s` be obtained by greedily expanding an integer in its canonical
rank-`s` Macaulay word and raising every lower binomial index by one.  Starting
from `n` and `n+b-1`, the independent engine constructs

\[
x_3=n+U_2(n)-H+1,
\qquad
y_3=x_3+U_2(n+b-1)-U_2(n)-1.
\]

Removing their leading terms gives

\[
x_3=\binom{q-1}{3}+\alpha,qquad
y_3=\binom q3+\beta.
\]

The next normalized tails are reconstructed recursively as

\[
\begin{aligned}
p&=U_2(\alpha)-\tau+1,&v&=U_2(\beta)-\tau,\\
P&=U_3(p)-\tau+1,&V&=U_3(v)-\tau.
\end{aligned}
\]

The greedy engine independently returns exactly

\[
\begin{aligned}
\alpha&=\binom{q-5}{2}+\binom{25}{1},&
\beta&=\binom{q-4}{2}+\binom{58}{1},\\
p&=\binom{q-6}{3}+\binom{q-10}{2}+\binom{269}{1},&
v&=\binom{q-5}{3}+\binom{q-9}{2}+\binom{1625}{1},\\
P&=\binom{q-6}{4}+\binom{q-11}{3}+\binom{q-15}{2}
  +\binom{35995}{1},&
V&=\binom{q-5}{4}+\binom{q-10}{3}+\binom{q-14}{2}
  +\binom{1319452}{1}.
\end{aligned}
\]

The most restrictive strict top-index inequality is
`q-14>1319452`, or `q>1319466`.  Therefore all six displayed words
are canonical for every odd `j>=17`; canonical stability is not what delays
the first double-negative witness to `j=33`.

## 3. Pascal cancellations

The full states, rather than only the normalized formulas, give

\[
\gamma_3=U_2(n+b-1)-U_2(n)-H=23-4q.
\]

Using the reconstructed rank-three states,

\[
\gamma_4=U_3(y_3)-U_3(x_3)-U_2(n)-1=1330-4q.
\]

At the next two ranks, leading Pascal terms cancel and the independent full
orbit agrees with

\[
\gamma_5=V-P-U_2(\alpha)=1283187-4q,
\]

and, after setting
`A=U_4(P)-tau+1`, `B=U_4(V)-tau`,

\[
\gamma_6=B-A-U_3(p)=869828292418-4q.
\]

These identities were replayed from complete canonical expansions at
`j=17,29,31,33,35,37,55`; they were not inferred from the author's displayed
linear formulas.

## 4. First witness and infinite sign stability

The sign thresholds are exact:

\[
\gamma_5<0\iff q\ge320797,
\qquad
\gamma_6<0\iff q\ge217457073105.
\]

At `j=31`,

\[
q=80172722860,quad
(\gamma_5,\gamma_6)=(-320689608253,549137400978),
\]

so rank six still recovers.  At `j=33`,

\[
q=320690891436,quad
(\gamma_5,\gamma_6)=(-1282762282557,-412935273326).
\]

This is the first odd member in the stable displayed family with both signs
negative.  Since `q_(j+2)=4q_j-4`, every odd `j>=33` remains above both
thresholds, proving an infinite actual double-negative family.

The independent full rank-seven orbit at `j=33` gives

\[
\gamma_7=129084548046247672655610>0.
\]

No all-`j` rank-seven positivity claim is needed for the refutation.

## 5. Scope firewall

The family satisfies the antecedent of `M305-rank6-deficit-domination` but
has `gamma6<0`; it therefore refutes M305 and the proposed fixed two-row
rank-five/rank-six recovery.  It does not refute a strategy that chooses a
later rank adaptively—the first witness already recovers at rank seven.  It
also does not establish or refute the global rank-42 interface or the public
antichain problem.

The independent checker ran under 2 GiB virtual memory and a 120-second
timeout.  No Lean process was used.
