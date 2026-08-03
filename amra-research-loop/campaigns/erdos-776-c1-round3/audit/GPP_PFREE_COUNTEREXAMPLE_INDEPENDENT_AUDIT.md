# Independent audit: actual G++ p-free counterexample

## Verdict

**Pass, with a strict scope firewall.**  The state `(j,k,r)=(21,4,26466)` is
an actual dyadic `++ -> ++` state with `gamma4<0`.  It violates the proposed
universal p-free coverage inequality by the exact margin

\[
 U_3(e)-U_2(\alpha)-1=-136419183,
\]

and also violates M303's nested threshold.  Nevertheless the exact
base-retaining rank-five surplus is

\[
 \gamma_5=859354068710>0.
\]

Thus this point refutes the assertion that every actual G++ state is covered
by that p-free sufficient gate and refutes M303.  It does not refute the
conditional implication when the p-free antecedent actually holds, and it
does not refute exact rank-five recovery.

The audit imports neither the author verifier nor its generated JSON.  A new
greedy canonical Macaulay engine reconstructs all quantities from integers.

## 1. Actual dyadic state

Put

\[
 h=112\,2^{j-1},\qquad
 q=\frac{2h-\binom{k-1}{2}-2+r}{k-1},\qquad
 u=r+k-1,\qquad b=q+k.
\]

At `(j,k,r)=(21,4,26466)`, the numerator is divisible by three and gives

\[
 (h,q,u,b)=(117440512,78302495,26469,78302499).
\]

With `n=C(q,2)+r`, direct integer cancellation gives

\[
 \binom{b-1}{2}+2-n=234881024=2h.
\]

The legal inequalities `0<=r<q`, `0<=u<q+1`, and `5<=b<h` all hold.  This
is therefore an actual dyadic point, not a relaxed real or residue-incompatible
state.

## 2. Independent canonical engine and chamber signs

For a nonnegative integer `N`, the audit greedily constructs its unique
rank-`s` word

\[
 N=\sum_{i=1}^s\binom{t_i}{i},\qquad t_s>\cdots>t_1,
\]

and defines `U_s(N)=sum_i C(t_i,i+1)`.  Binary search is used only to locate
each exact integer top index.

The two initial words are

\[
\begin{aligned}
n&=\binom{78302495}{2}+\binom{26466}{1},\\
n+b-1&=\binom{78302496}{2}+\binom{26469}{1}.
\end{aligned}
\]

After one literal orbit step, the complete words are

\[
\begin{aligned}
x_3={}&\binom{78302495}{3}+\binom{8606}{2}+\binom{510}{1},\\
y_3={}&\binom{78302496}{3}+\binom{8615}{2}+\binom{2420}{1}.
\end{aligned}
\]

Hence

\[
 \alpha=37027825>0,\qquad \beta=37107225>0,
\]

and both are strictly below their advertised next binomial caps.  This is the
first `++` sign pair.

Writing `tau=C(b,2)+1-n`, the independently raised tails are

\[
\begin{aligned}
p&=U_2(\alpha)-\tau+1=105881285695,\\
v&=U_2(\beta)-\tau=106217638624.
\end{aligned}
\]

They are positive and their words are

\[
\begin{aligned}
p={}&\binom{8597}{3}+\binom{6294}{2}+\binom{934}{1},\\
v={}&\binom{8606}{3}+\binom{6826}{2}+\binom{5479}{1}.
\end{aligned}
\]

The full next states are `x_4=C(q,4)+p` and `y_4=C(q+1,4)+v`, with both
tails strictly below their caps.  This proves the second `++`, hence the
literal transition is `++ -> ++`.

## 3. Negative gamma4 and failure of the p-free gate

The full orbit and normalized chart independently agree on

\[
 \gamma_3=-313130586,
 \qquad
 \gamma_4=-13858416<0.
\]

The increment is

\[
 e=v-p=336352929
   =\binom{1264}{3}+\binom{1068}{2}+\binom{287}{1}.
\]

Exact raising gives

\[
 U_3(e)-U_2(\alpha)-1=-136419183<0.
\]

Accordingly this actual target point does not pass the proposed p-free
sufficient gate.  This does not invalidate Macaulay superadditivity or the
logical sufficient implication conditional on a nonnegative p-free margin;
it invalidates using that condition as universal coverage of the G++ chamber.

For M303, `C(8606,2)<=alpha<C(8607,2)`.  The least `t` satisfying

\[
 \binom t4\ge\binom{8607}{3}
\]

is `t=1266`.  M303 would require

\[
 e\ge\binom{1266}{3}=337380560,
\]

but instead

\[
 e-\binom{1266}{3}=-1027631.
\]

This is a direct counterexample to M303's universal threshold claim.

## 4. Full unnormalized orbit cross-check

The second computation chain never removes leading binomial terms before
raising.  Starting with

\[
 L_2=n,\quad R_2=n+b-1,
\]

it forms

\[
 L_3=U_2(L_2)-\tau+1,\quad R_3=U_2(R_2)-\tau,
\]

and then

\[
 L_4=U_3(L_3)-\tau+1,\quad R_4=U_3(R_3)-\tau.
\]

The literal rank-five surplus

\[
 U_4(R_4)-U_4(L_4)-U_3(L_3)-1
\]

is exactly `859354068710`.  Independently, the normalized tail expression

\[
 U_3(v)-U_3(p)-U_2(\alpha)-1
\]

returns the same integer.  The difference between this value and the p-free
margin is the positive base-dependent cross-term gain

\[
 859490487893.
\]

Discarding the base word of `p` therefore loses precisely the information
that makes this actual state recover at rank five.

## 5. Scope

The audited evidence strictly supports:

- refutation of universal G++ coverage by `U_3(e)>=U_2(alpha)+1`;
- refutation of `M303-nested-binomial-envelope`.

It does not support:

- refutation of the p-free conditional implication on states satisfying its
  antecedent;
- refutation of exact base-retaining rank-five recovery—the witness has
  `gamma5>0`;
- any conclusion about all actual G++ states, the rank-42 interface, or the
  public Erdős #776 problem.

No Lean was used.  Reproduction:

- `audit/verify_gpp_pfree_counterexample_independent.py`, SHA-256
  `2eef2f7886ce43925614fc0fe7daf527e7ee2529e8a3fcec181f9993fbd567e6`
- `audit/GPP_PFREE_COUNTEREXAMPLE_INDEPENDENT_AUDIT.json`, SHA-256
  `0ae7bbbdc8fcd02a055c858371a3e8aa6d001928f52aeb99aaf7efd2d25858a4`

```sh
ulimit -v 2097152
timeout 120s python3 audit/verify_gpp_pfree_counterexample_independent.py
```
