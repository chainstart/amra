# Independent audit of the ordinary subleading-symbol theorem

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS AFTER THE ALL-ORDERS SADDLE CERTIFICATE}}
\]

No counterexample was found to the claimed functions
\(P_h,Q_h,S_h\), to \(H_2,H_3\), or to
\[
[k^{d-1}]b_{k,d}
=-\frac{22d^3+147d^2+161d-258}{36}.
\]

The first audited version had a proof-completeness gap in Lemma 2.  It
said that one normalized the exact Lagrange profiles, retained four
orders, and “collecting” gave the nine rational functions, but did not
display:

- the general coefficient extracted at arbitrary loss \(\ell\);
- a recurrence satisfied by the source coefficients;
- the recurrence claimed to follow after multiplication by
  \(w^{5/2},w^{11/2},w^{17/2}\); or
- the finite initial conditions that would identify the source
  sequence with the claimed rational series.

That gap is now repaired by an exact Cauchy-integral representation
and a parameterized saddle/Gamma recurrence in the symbolic variable
\(x\).  It proves the four diagonal functions through \(s^{-3}\)
without truncating the loss variable.  The companion symbolic
certificate verifies twelve rational-function identities and performs
no finite-loss interpolation.

The binomial central expansion and completion of the theorem are also
correct.  In particular, \(1/8\) is the right
coefficient, the order-\(k^{-1}\) determinant term has exactly zero
expectation, and the fourth binomial central moment first contributes
one order later than \(H_3\).

## 1. Independent source-profile reconstruction

The independent verifier imports no existing OPG verifier or stored
profile symbol.  It starts from
\[
\widehat F_{\alpha,r}(z)
=\prod_{a=0}^{r-1}(1-(\alpha+a)z)
\]
and
\[
\widehat E_{\beta,r}(z)
=\sum_{q=0}^r
\binom rq2^{r-q}(-1)^q
\prod_{a=0}^{q-1}(1-(\beta+r+a)z).
\]
These are the normalized outer falling product and finite Lagrange
sum with \(z=s^{-1}\).

It forms
\[
\widehat D_{\beta,r}
=\widehat E_{\beta,r}
-2rz\widehat E_{\beta+1,r-1},
\]
and then
\[
\widehat U_{0,r}
=\widehat F_{0,r}\widehat D_{0,r},
\]
\[
\widehat U_{1,r}
=\widehat F_{2,r}\widehat D_{2,r},
\]
\[
\widehat U_{2,r}
=\widehat F_{4,r}\widehat D_{4,r}
+8rz^2\widehat F_{4,r-1}\widehat E_{4,r-1}.
\]
Thus every tested \(R_{\ell,h}(r)\) is recovered directly from the
source Lagrange definitions.

For each loss, the verifier interpolates the degree-\(\ell\)
polynomial in \(r\), uses \(\ell+1\) values, and checks one spare
value.  It then extracts the coefficients of
\[
r^\ell,\quad r^{\ell-1},\quad
r^{\ell-2},\quad r^{\ell-3}.
\]

Through loss 16, all 186 available coefficients agree with the
series expansions of (5)--(8).  This is strong evidence for the
formulas but remains a finite check.

## 2. Audit history: why the first Lemma 2 was incomplete

For a claimed function of the form
\[
F(z)=\frac{N(z)}{c(1-2z)^\alpha},
\]
its coefficients have the explicit all-orders form
\[
[z^n]F(z)
=\frac1c
\sum_{q=0}^{\deg N}
N_q\,
2^{n-q}
\frac{(\alpha)_{n-q}}{(n-q)!},
\tag{A}
\]
where terms with \(n<q\) are zero.

Equivalently, \(F\) satisfies the polynomial differential equation
\[
(1-2z)N(z)F'(z)
-\left((1-2z)N'(z)+2\alpha N(z)\right)F(z)=0.
\tag{B}
\]
Equation (B) gives a finite-width recurrence for the coefficients,
and finitely many initial values determine the series.

The first proof supplied neither (A) for the Lagrange-extracted source
coefficients nor a proof that those coefficients satisfied the
recurrence from (B).  Multiplying a *claimed* function by
\((1-2z)^\alpha\) and obtaining a finite numerator proves a recurrence
for that claimed function only.  It does not prove that the
independently defined profile coefficients obey it.

The statement

```text
Collecting ... and then summing in ell gives (5)--(8).
```

is therefore the entire substantive resummation, not a derivation of
it.  The following sentence about coefficient recurrences does not
write or verify those recurrences.

Because Theorem 1 is an all-\(d\) statement, a check through
\(\ell=16\), or any other fixed loss, could not fill this gap.  This
is why the initial audit returned FAIL.

## 3. Implemented all-orders patch for Lemma 2

The revision uses a stronger parameterization than a list of nine
loss recurrences.  Put \(j=xs\) and
\[
\Phi_h(s,x)=\frac{2^jj!}{s^{2j}}U_{h,j}(s).
\]
Then the polynomial expansion of \(R_{\ell,h}(j)\) gives exactly
\[
\Phi_h(s,x)
=A(x)+s^{-1}P_h(x)+s^{-2}Q_h(x)+s^{-3}S_h(x)
+O_{\rm formal}(s^{-4}).
\tag{C}
\]
An identity in the symbolic variable \(x\) therefore proves every
loss coefficient simultaneously.

The revised theorem derives exact Cauchy integrals for the three main
profiles and the exceptional \(h=2\) profile, all with phase
\[
\phi_x(y)
=y+(1-x)\log(1-y/2)-x\log y
\]
and small saddle \(y_0=2x\).  It then specifies:

- every phase derivative
  \[
  \phi_x^{(r)}(2x)
  =\frac{(r-1)!}{2^r}
  \left(-(1-x)^{1-r}+(-1)^rx^{1-r}\right);
  \]
- the Gaussian moment functional;
- a recurrence for the exponential saddle polynomials through
  inverse-\(s\) rank three;
- the Bernoulli-polynomial Gamma correction and its exponential
  recurrence;
- exact derivative formulas for the main and exceptional amplitudes;
  and
- the three signed Gamma-argument lists.

These finite recurrences produce
\[
\Phi_a^{\rm main}
=\sqrt{1-2x}\sum_{r=0}^3
C_r(g_a,{\cal A}_a)s^{-r}+O(s^{-4})
\]
for \(a=0,2,4\), and
\[
\Phi^{\rm ex}
=\frac{8x}{s\sqrt{1-2x}}
\sum_{r=0}^2C_r(g_*,{\cal A}_*)s^{-r}
+O(s^{-4}).
\]
Combining the \(a=4\) main term with the exceptional term gives
\(h=2\).

The new
`verify_ordinary_subleading_saddle_certificate.py` implements these
recurrences with symbolic \(x\) and proves:

\[
\begin{array}{c|c}
\text{profile}&\text{identities}\\ \hline
h=0&A,P_0,Q_0,S_0\\
h=1&A,P_1,Q_1,S_1\\
h=2&A,P_2,Q_2,S_2.
\end{array}
\]

These are twelve rational-function identities, not a test of twelve
losses.  Analytic equality for \(0<x<1/2\) implies equality of every
Taylor coefficient at \(x=0\), completing the all-orders
resummation.

## 4. The order-\(k^{-1}\) determinant term

Let
\[
B(z):=P_1(z)-P_0(z).
\]
The displayed functions satisfy the exact identity
\[
P_2(z)-P_1(z)=P_1(z)-P_0(z)=B(z),
\]
or equivalently
\[
P_0+P_2=2P_1.
\]

The order-\(k^{-1}\) determinant kernel omitted from the manuscript's
notation is therefore
\[
G_1(x,t)
=t\left(
B(tx)A(t(1-x))
-A(tx)B(t(1-x))
\right).
\]
It obeys
\[
\boxed{
G_1(1-x,t)=-G_1(x,t).
}
\]

The binomial law is exactly invariant under \(J\mapsto k-J\), not
merely asymptotically symmetric.  Hence
\[
\mathbb E\,G_1(J/k,t)=0
\]
coefficientwise for every \(k\).  There is no residual
order-\(k^{-1}\) contribution from a Taylor correction, lattice
effect, or odd central moment.

The independent verifier constructs \(G_1\) from the displayed
\(P_h\) and checks this functional identity symbolically.

## 5. Central binomial expansion and the coefficient \(1/8\)

Put
\[
\delta=\frac Jk-\frac12.
\]
The exact central moments needed here are
\[
\mathbb E\delta^2=\frac1{4k},
\qquad
\mathbb E\delta^3=0,
\]
\[
\mathbb E\delta^4
=\frac3{16k^2}-\frac1{8k^3}.
\tag{D}
\]

For every fixed coefficient of the loss marker \(t\), \(G_2\) and
\(G_3\) are polynomials in \(x\), so Taylor expansion is
coefficientwise finite.  Consequently
\[
\begin{aligned}
\mathbb E\,G_2(\tfrac12+\delta,t)
={}&G_2(\tfrac12,t)
+\frac12G_2''(\tfrac12,t)\mathbb E\delta^2\\
&+\frac1{24}G_2^{(4)}(\tfrac12,t)\mathbb E\delta^4
+\cdots\\
={}&G_2(\tfrac12,t)
+\frac1{8k}G_2''(\tfrac12,t)
+O_L(k^{-2}).
\end{aligned}
\tag{E}
\]

Since \(G_2\) itself multiplies \(k^{-2}\), equation (E) contributes
\[
k^{-2}G_2(\tfrac12,t)
+k^{-3}\frac18G_2''(\tfrac12,t)
+O_L(k^{-4}).
\]
This proves the coefficient \(1/8\).

Likewise,
\[
k^{-3}\mathbb E\,G_3(\tfrac12+\delta,t)
=k^{-3}G_3(\tfrac12,t)+O_L(k^{-4}).
\]

The fourth moment in (D) is \(O(k^{-2})\), so its multiplication by
the leading \(k^{-2}G_2\) term starts at \(k^{-4}\).  It cannot enter
\(H_3\).  No binomial fourth-order term is missing.

The independent verifier checks (D) exactly for \(1\le k\le64\),
giving 192 rational moment identities.

## 6. Verification of \(G_2,G_3,H_2,H_3\)

Direct multiplication of
\[
\mathcal F_1(x)\mathcal F_1(1-x)
-\mathcal F_0(x)\mathcal F_2(1-x)
\]
gives at order \(k^{-2}\):

\[
\begin{aligned}
G_2=t^2\{&
(Q_1(u)-Q_0(u))A(v)
+A(u)(Q_1(v)-Q_2(v))\\
&+P_1(u)P_1(v)-P_0(u)P_2(v)\},
\end{aligned}
\]
and at order \(k^{-3}\):
\[
\begin{aligned}
G_3=t^3\{&
(S_1(u)-S_0(u))A(v)
+A(u)(S_1(v)-S_2(v))\\
&+P_1(u)Q_1(v)+Q_1(u)P_1(v)\\
&-P_0(u)Q_2(v)-Q_0(u)P_2(v)\}.
\end{aligned}
\]
No \(P^3\) term occurs because the determinant is a product of two
profiles, not an exponential of a profile.

Substituting the claimed functions and simplifying independently
gives
\[
\boxed{
H_2(t)=G_2(\tfrac12,t)=\frac{2t^4}{1-t},
}
\]
\[
\boxed{
H_3(t)
=G_3(\tfrac12,t)
+\frac18G_2''(\tfrac12,t)
=-\frac{
t^4(43t^4-129t^3+108t^2-6t+6)
}{3(1-t)^4}.
}
\]

Thus (17)--(18) pass, conditional on the all-orders profile functions.

## 7. Coefficient extraction from \(H_3\)

For \(L\ge5\),
\[
[t^L]H_2=2.
\]
Expanding the rational function \(H_3\) gives
\[
\boxed{
[t^L]H_3
=-\frac{
22L^3-117L^2+41L+78
}{18}.
}
\]
The independent verifier checks this identity for \(5\le L\le16\).

With \(L=d+4\),
\[
N_L(k)
=2k^{L-2}
+[t^L]H_3\,k^{L-3}
+O_L(k^{L-4}).
\]
Since
\[
\frac1{2k(k-1)}
=\frac1{2k^2}
\left(1+\frac1k+O(k^{-2})\right),
\]
the coefficient of \(k^{d-1}=k^{L-5}\) is
\[
\begin{aligned}
[k^{d-1}]b_{k,d}
&=1+\frac12[t^{d+4}]H_3\\
&=
\boxed{
-\frac{22d^3+147d^2+161d-258}{36}.
}
\end{aligned}
\]
The leading \(1\) here is the \(1/k\) correction from
\((1-1/k)^{-1}\); it is not missing from the manuscript.

Independent exact determinant computations recover \(b_{k,d}\),
interpolate its degree-\(d\) polynomial, and confirm this coefficient
for \(1\le d\le12\), with two unused \(k\)-values at every depth.

Finally, the standard identities
\[
\sum_{d\ge1}dz^d=\frac z{(1-z)^2},
\quad
\sum_{d\ge1}d^2z^d=\frac{z(1+z)}{(1-z)^3},
\]
\[
\sum_{d\ge1}d^3z^d
=\frac{z(1+4z+z^2)}{(1-z)^4}
\]
simplify the coefficient generating function to
\[
-\frac{
z(43z^3-123z^2+90z+12)
}{6(1-z)^4}.
\]
Thus (2) also passes.

## 8. Independent verification record

The new verifier is
`independent_verify_ordinary_subleading_symbol.py`; it imports no
existing OPG verifier.  At its default scope it performs:

\[
\begin{array}{c|r}
\text{check}&\text{count}\\ \hline
\text{profile rank coefficients through loss 16}&186\\
\text{exact central moments}&192\\
H_3\text{ coefficient checks}&12\\
\text{ordinary subleading polynomials}&12.
\end{array}
\]

It also verifies:

- exact antisymmetry of \(G_1\);
- the symbolic simplifications of \(H_2,H_3\);
- two spare interpolation values at every ordinary depth; and
- the final rational generating function.

The separate all-orders certificate reports:

```text
finite_loss_interpolation:             false
symbolic_identity_checks:              12
maximum_inverse_s_rank:                3
status: all_orders_symbolic_certificate_passed
```

The finite verifier remains useful regression evidence, while the
symbolic saddle certificate supplies the previously missing
all-orders proof.

## 9. Final assessment

The central-binomial and determinant parts of the manuscript are
correct.  I found no missing antisymmetric, variance, or fourth-moment
contribution, and the final cubic coefficient is algebraically
consistent with every exact polynomial tested.

The revised Lemma 2 now contains an explicit parameterized extraction
from the exact Lagrange profiles, and the companion certificate checks
the resulting identities symbolically in \(x\), rather than at
finitely many losses.

The original proof-completeness objection is therefore resolved.
The current ordinary subleading-symbol theorem passes this strict
independent audit.
