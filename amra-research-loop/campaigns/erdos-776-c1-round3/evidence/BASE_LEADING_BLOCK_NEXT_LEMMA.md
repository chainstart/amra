# A base-retaining replacement for the false G++ gate

For an actual `(++ )->(++ )` state with `gamma4<0`, write

\[
c=\operatorname{top}_3(p),\qquad
d=\operatorname{top}_3(v),
\]

where `top_3(N)` is the leading index in the canonical rank-three word of
`N`.  Then

\[
U_3(v)\ge\binom d4,
\qquad
U_3(p)\le\binom{c+1}{4}-1.
\]

Consequently the exact rank-five surplus satisfies

\[
\begin{aligned}
\gamma _5
 &=U_3(v)-U_3(p)-U_2(\alpha)-1\\
 &\ge
 \binom d4-\binom{c+1}{4}-U_2(\alpha).
\end{aligned}
\]

Thus the following is an exact sufficient next lemma:

\[
\boxed{
\binom{\operatorname{top}_3(v)}4
-\binom{\operatorname{top}_3(p)+1}4
\ge U_2(\alpha).}
\]

If `a=top_2(alpha)`, the stronger but purely top-index condition

\[
\binom d4-\binom{c+1}4\ge\binom{a+1}3
\]

also suffices, because `U_2(alpha) < binom(a+1,3)`.  In fact its margin
`L` gives the strict bound `gamma5 >= L+1`.

Unlike the refuted p-free gate, this retains the base location of the
interval `[p,v]` and counts complete cubic caps crossed by it.

`probe_adaptive_gamma4_wall.py` conditions on the rare negative-`gamma4`
region.  For each tested `(j,k)` fibre it locates a sign-change wall by
exponential and binary search, then checks exact windows at both the first
target point and the located wall.  Its frozen finite domain is

- `j=6,...,60,70,80,90,100`;
- `4<=k<=300`;
- 823,476 accepted actual `(++ )->(++ )` rows on 7,812 fibres.

No leading-block counterexample occurs.  The minimum exact margin is
84,520 at `(j,k,r)=(6,4,145)`.  The same run independently rediscovers the
p-free counterexample at `(21,4,26466)`, where the leading-block margin is
742,028,295,195 even though the p-free margin is negative.

The stronger top-index condition also has no counterexample in this run;
its minimum margin is 83,805 at the same smallest state.  A separate
carry-aware implementation checks 58,026 compatible points in 50 fibres,
including 18,081 target points and 2,620 explicitly added carry neighbours,
and obtains the same minimum.  Every target in that independent domain is
in the hard multi-cap cell `c<a` and `c+2<=d<=a+1`; hence the remaining
analytic task is genuinely a sum-of-caps estimate rather than a trivial
single-cap separation.

This is finite falsification evidence, not an all-parameter proof.  Carries
can make the sign pattern nonmonotone, so binary wall location is used only
to centre exact windows and is not claimed to exhaust a fibre.  The open
task is to prove the boxed cap-crossing inequality uniformly from the
actual dyadic relations, or find a counterexample in an untested carry
cell.  In top-index form, the exact unresolved estimate is
`sum_{x=c+1}^{d-1} binom(x,3) >= binom(a+1,3)`.
