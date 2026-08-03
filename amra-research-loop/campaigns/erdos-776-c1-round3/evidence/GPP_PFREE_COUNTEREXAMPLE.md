# The p-free G++ sufficient gate is false

The actual state

\[
(j,h,q,k,r,u,b)=
(21,117440512,78302495,4,26466,26469,78302499)
\]

satisfies the literal dyadic identity and lies in the `(++ )->(++ )`
target chamber.  Its normalized data are

\[
\begin{aligned}
\alpha&=37027825,&\beta&=37107225,\\
p&=105881285695,&v&=106217638624,\\
e&=v-p=336352929,&\gamma_4&=-13858416.
\end{aligned}
\]

The base-free superadditivity lower gate fails:

\[
U_3(e)-U_2(\alpha)-1=-136419183<0.
\]

In particular, the nested-binomial lower threshold proposed in M303 is
also false here.  However, retaining the base `p` gives

\[
U_3(v)-U_3(p)-U_2(\alpha)-1
=859354068710>0.
\]

An independent evaluation from the full unnormalized orbit gives the same
rank-five surplus.  Thus this is a counterexample to the p-free route, not
to exact rank-five recovery.  Any surviving proof must exploit the base
word of `p` and the carries crossed by `[p,v]`.
