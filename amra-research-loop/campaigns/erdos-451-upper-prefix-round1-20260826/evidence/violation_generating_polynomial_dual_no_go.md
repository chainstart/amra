# Violation generating polynomial: exact phase expansion and a proper-degree dual no-go

This note attacks only the coupled endpoint interface left open by
signed_missing_prime_typeii_audit.md.  It does not estimate the accessible
Mobius ledger and the full Bonferroni remainder separately.  Instead it
puts both into one generating polynomial, preserves the canonical absorber
phase in an exact character expansion, and asks whether proper-degree data
can certify the endpoint.

The answer to the universal version is negative.  In fact every pointwise
one-sided multilinear certificate of degree less than the number of
remaining primes has nonpositive expectation under the principal product
law.  Two explicit nonnegative rational product-law perturbations have all
the same proper marginals and endpoints separated by twice the survivor
density.  A compact contour reconstruction has exponential condition
number for the same reason.  These are method no-go results, not
counterexamples to the actual 451 product multiset.

The unique surviving formulation is consequently an exact full-modulus,
high-conductor, signed character sum retaining the \(Q_0\) phase.  A
precise conditional lemma below shows that an \(o(\delta N)\) bound for
that one sum would prove an \(\exp(O(k/\log k))\) upper bound.  This lemma
is open.  The campaign remains in survivor_deepening with closes equal to
the empty list.

## 1. Exact generating identity

Let

\[
 A=\lfloor k/\log^2 k\rfloor,\qquad
 Q_0={k+A\choose A},\qquad
 {\cal P}=\{p:k+A<p<2k\},\qquad
 P=\prod_{p\in{\cal P}}p ,
\]

and write \(m=|{\cal P}|\).  For \(p=k+b\), put

\[
 d_p=b-1,\qquad
 \delta_p={d_p\over p-1},\qquad
 q_p={k\over p-1}=1-\delta_p.                    \tag{1}
\]

Let \({\cal W}_X\) be the multiset of products \(x=ut\) with
\(1\leq u,t\leq X\) and \((ut,P)=1\).  Its occurrence count is

\[
 M_X=\#\{n\leq X:(n,P)=1\},\qquad N=M_X^2.       \tag{2}
\]

As in the preceding Type-II note, define

\[
 I_p(x)={\bf 1}_{p\mid D(Q_0x)},\qquad
 J_p(x)=1-I_p(x),\qquad
 V(x)=\sum_{p\in{\cal P}}J_p(x).                 \tag{3}
\]

Thus \(V(x)=0\) exactly when \(n=Q_0x\) obeys every remaining
451 congruence; primes in \((k,k+A]\) have already been absorbed by
\(Q_0\).  Define

\[
 F_X(z)=\sum_{x\in{\cal W}_X}z^{V(x)}.           \tag{4}
\]

For \(T\subseteq{\cal P}\), let \(P_T=\prod_{p\in T}p\) and let
\(N_{P_T}(X)\) be the count on which every \(I_p\), \(p\in T\), is one.
Pointwise expansion of

\[
 z^{V(x)}=\prod_{p\in{\cal P}}\bigl(z+(1-z)I_p(x)\bigr)
\]

gives the literal identity

\[
 F_X(z)=\sum_{T\subseteq{\cal P}}
 z^{m-|T|}(1-z)^{|T|}N_{P_T}(X).                 \tag{5}
\]

Writing

\[
 N_{P_T}(X)=\delta_TN+{\cal E}_{P_T}(X),\qquad
 \delta_T=\prod_{p\in T}\delta_p,
\]

the principal and error parts combine as

\[
\boxed{\;
 F_X(z)=N\prod_{p\in{\cal P}}(\delta_p+q_pz)
 +\sum_{T\subseteq{\cal P}}
 z^{m-|T|}(1-z)^{|T|}{\cal E}_{P_T}(X).\;}       \tag{6}
\]

At the endpoint only the full divisor survives:

\[
 F_X(0)=N_P(X)=\delta N+{\cal E}_P(X),\qquad
 \delta=\prod_{p\in{\cal P}}\delta_p.            \tag{7}
\]

Thus (6) is exactly the requested joint ledger.  It does not upper-bound
the low-rank Mobius terms and the violation remainder separately; their
cancellation is already recombined into one polynomial.

Differentiation at the opposite endpoint has a useful triangular meaning:

\[
 {F_X^{(j)}(1)\over j!}
 =\sum_{\substack{T\subseteq{\cal P}\\|T|=j}}
 \#\{x\in{\cal W}_X:J_p(x)=1\text{ for all }p\in T\}.          \tag{8}
\]

Hence the jet of order \(R\) at \(z=1\) is precisely failure-intersection
information through support rank \(R\).

## 2. Exact \(Q_0\)-phase character expansion

For a multiplicative character \(\psi\bmod p\), define

\[
 \rho_{p,\psi}={\psi(-Q_0)\over d_p}
       \sum_{j=1}^{d_p}\overline{\psi(j)}
 \quad(\psi\neq{\bf 1}).                          \tag{9}
\]

The allowed unit residues are
\(-Q_0^{-1},\ldots,-d_pQ_0^{-1}\).  Multiplicative Fourier inversion
therefore gives the local coefficient

\[
 c_{p,{\bf 1}}(z)=\delta_p+q_pz,\qquad
 c_{p,\psi}(z)=(1-z)\delta_p\rho_{p,\psi}
 \quad(\psi\neq{\bf 1}).                          \tag{10}
\]

For a character \(\chi\bmod P\), let \(S(\chi)\) be the set of primes at
which its local component is nonprincipal, and put

\[
 c_\chi(z)=(1-z)^{|S(\chi)|}\delta_{S(\chi)}
 \prod_{p\in S(\chi)}\rho_{p,\chi_p}
 \prod_{p\notin S(\chi)}(\delta_p+q_pz).          \tag{11}
\]

With

\[
 S_X^P(\chi)=\sum_{\substack{n\leq X\\(n,P)=1}}\chi(n),
\]

the exact phase-preserving expansion is

\[
\boxed{\quad
 F_X(z)=\sum_{\chi\bmod P}c_\chi(z)
              \bigl(S_X^P(\chi)\bigr)^2.\quad}    \tag{12}
\]

The square in (12) is a signed complex square, not an absolute square.
In particular the product of the local phases in (9) is
\(\chi(-Q_0)\), and it has not been removed by a norm.

Formula (11) also explains (8) spectrally: the derivative
\(F_X^{(j)}(1)\) receives contributions only from character supports of
rank at most \(j\).  At \(z=0\), all support ranks are present and (12)
becomes

\[
 F_X(0)={1\over\varphi(P)}
 \sum_{\chi\bmod P}\chi(-Q_0)
 \prod_{p\in{\cal P}}\left(\sum_{j=1}^{d_p}
          \overline{\chi_p(j)}\right)
 \bigl(S_X^P(\chi)\bigr)^2.                       \tag{13}
\]

For a principal local component the corresponding inner sum in (13) is
\(d_p\).  Thus (13) includes all primitive conductors and all supports
with the correct outside density factors.

## 3. A universal proper-degree one-sided dual no-go

The local principal failure probabilities satisfy

\[
 q_p-\delta_p={2k+1-p\over p-1}>0,               \tag{14}
\]

so \(q_p/\delta_p\geq1\) for every remaining prime.  The following theorem
uses exactly this inequality.

> **Proper-degree cube dual theorem.**  Let
> \(\mu(S)=\prod_{i\in S}q_i\prod_{i\notin S}\delta_i\) be an
> independent law on subsets of \([m]\), where
> \(q_i+\delta_i=1\) and \(q_i\geq\delta_i>0\).
> Let \(Q(J_1,\ldots,J_m)\) be a real multilinear polynomial of total degree
> less than \(m\).  If
> \[
> Q(0)=1,\qquad Q({\bf 1}_S)\leq0
>       \quad\text{for every nonempty }S,          \tag{15}
> \]
> then
> \[
> {\mathbb E}_\mu Q\leq0.                          \tag{16}
> \]

**Proof.**  The missing top multilinear coefficient is the identity

\[
 0=\sum_{S\subseteq[m]}(-1)^{m-|S|}Q({\bf 1}_S),
\]

and hence

\[
 Q(0)=\sum_{\varnothing\neq S\subseteq[m]}
              (-1)^{|S|+1}Q({\bf 1}_S).           \tag{17}
\]

Let \(\mu_0=\mu(\varnothing)=\prod_i\delta_i\).  Substitution of (17)
into the expectation gives

\[
 {\mathbb E}_\mu Q
 =\sum_{\varnothing\neq S\subseteq[m]}
 \left(\mu(S)+(-1)^{|S|+1}\mu_0\right)
 Q({\bf 1}_S).                                    \tag{18}
\]

For odd \(|S|\) the bracket is positive.  For even \(|S|\),

\[
 {\mu(S)\over\mu_0}=\prod_{i\in S}{q_i\over\delta_i}\geq1,
\]

so the bracket is again nonnegative.  Every value multiplying it in
(18) is nonpositive by (15), proving (16). \(\square\)

This strictly strengthens the odd-Bonferroni obstruction.  It kills every
universal pointwise one-sided certificate that uses a proper-degree
multilinear polynomial in the individual failure coordinates, including
nonsymmetric certificates.  The scalar case \(Q=P(V)\) follows
immediately, so Krawtchouk, discrete-Chebyshev, or arbitrary low-degree
polynomials of the violation count do not evade the obstruction.

The theorem does not say that all signed proper-degree averages are
useless.  It says that they cannot by themselves form a pointwise
nonpositive separator of every nonzero violation pattern under the actual
principal probabilities.  Arithmetic phase deviations, a full-degree
term, or a non-pointwise argument remain possible.

## 4. Exact indistinguishability of all proper marginals

There is also a sharp primal witness.  Let

\[
 \mu_{\pm}(S)=\mu(S)\pm\delta(-1)^{|S|},\qquad
 \delta=\mu(\varnothing)=\prod_i\delta_i.          \tag{19}
\]

Both are nonnegative probability laws.  Indeed every atom of \(\mu\) is
at least \(\delta\), and the signed perturbation has total mass
\(\delta(1-1)^m=0\).  If any proper subset of coordinates is fixed, summing
over one omitted coordinate cancels the perturbation.  Thus
\(\mu_+\) and \(\mu_-\) have identical marginals on every proper coordinate
set, but

\[
 \mu_+(\varnothing)=2\delta,\qquad
 \mu_-(\varnothing)=0.                            \tag{20}
\]

All probabilities are rational in the 451 application.  Clearing
denominators realizes (19) as two exact finite multisets, so this is not
an asymptotic or positivity fiction.

Their violation generating polynomials are

\[
 f_\pm(z)=\prod_{p\in{\cal P}}(\delta_p+q_pz)
                 \pm\delta(1-z)^m.                \tag{21}
\]

Consequently every derivative of order less than \(m\) agrees at \(z=1\),
while the endpoint values differ by \(2\delta\).  No universal theorem
depending only on proper marginals, or equivalently on the proper jet of
the scalar generating polynomial, can recover \(F_X(0)\) with
\(o(\delta N)\) accuracy.

This witness is not asserted to be a distribution of the actual products
\(Q_0ut\).  Its precise scope is to refute a distribution-free handoff from
the low-rank Type-II ledger to the endpoint.

## 5. Compact-contour condition number

For polynomials \(H\) of degree at most \(m\), put

\[
 \|H\|_r=\sup_{|1-z|\leq r}|H(z)|,\qquad 0<r<1.
\]

Any linear functional on this polynomial space which agrees with endpoint
evaluation \(H\mapsto H(0)\) has operator norm at least

\[
 r^{-m}.                                         \tag{22}
\]

This follows by testing \(H(z)=(1-z)^m\): its endpoint value is one and
its \(r\)-disc norm is \(r^m\).  Hence a contour or analytic-continuation
argument with endpoint norm \(\exp(o(m))\) must take

\[
 -\log r=o(1),\qquad r=1-o(1).                    \tag{23}
\]

At such a radius the full-support damping is only \(\exp(-o(m))\).
Therefore a generic compact contour cannot turn proper-rank control near
\(z=1\) into the required endpoint estimate with subexponential
conditioning.  This lower bound concerns universal linear continuation;
it does not rule out a contour identity whose integrand has additional
arithmetic \(Q_0\)-phase cancellation.

## 6. The narrower surviving endpoint lemma

Fix constants \(\gamma>0\) and \(0<\eta<4/3\), and set

\[
 X=\left\lfloor\exp(\gamma k/\log k)\right\rfloor,\qquad
 Y=X^{\,4/3-\eta}.                                \tag{24}
\]

For a character \(\chi\bmod P\), let \(f_\chi\) denote the conductor of
its inducing primitive character.  Define the single signed high-conductor
endpoint sum

\[
 {\cal H}_X={1\over\varphi(P)}
 \sum_{\substack{\chi\bmod P\\f_\chi>Y}}
 \chi(-Q_0)
 \prod_{p\in{\cal P}}\left(\sum_{j=1}^{d_p}
        \overline{\chi_p(j)}\right)
 \bigl(S_X^P(\chi)\bigr)^2.                       \tag{25}
\]

> **Conditional full-modulus endpoint lemma.**  If, for the quantities
> in (24),
> \[
> |{\cal H}_X|=o(\delta N),                        \tag{26}
> \]
> as one signed sum, then for all sufficiently large \(k\) there is a
> valid 451 integer
> \[
> 2k<n\leq\exp((2\gamma+o(1))k/\log k).            \tag{27}
> \]

**Derivation.**  The low-conductor theorem already proved in
weighted_multiplicative_character_deepening.md controls, in aggregate,
all nonprincipal terms with \(1<f_\chi\leq Y\) by
\(o(\delta X^2)\).  Also

\[
 X\left(1-\sum_{p\in{\cal P}}{1\over p}\right)-m
 \leq M_X\leq X,
 \qquad M_X=(1-o(1))X,                            \tag{28}
\]

so \(N\sim X^2\).  In (13), the principal character contributes
\(\delta N\).  Equation (26), together with the low-conductor theorem,
therefore gives

\[
 F_X(0)=\delta N+o(\delta N)>0.
\]

Thus some unit product \(ut\leq X^2\) makes \(n=Q_0ut\) satisfy all
remaining congruences.  The absorbed primes already divide \(Q_0\), and

\[
 \log Q_0\leq A\log\!\left({e(k+A)\over A}\right)=o(k/\log k).
\]

For sufficiently large \(k\), one has \(Q_0>2k\), so every such product
also satisfies the strict lower bound in (27). \(\square\)

The open range in (25) begins at conductor rank

\[
 {\log Y\over\log(2k)}
 =\left({4\over3}-\eta+o(1)\right)
   {\gamma k\over\log^2 k}                        \tag{29}
\]

and extends through the full rank \(m=(1+o(1))k/\log k\).  This is much
narrower than saying that a coupled estimate is needed: the modulus,
cutoff, normalization, absorber phase, local endpoint coefficient, signed
complex square, and target norm are all fixed in (25)-(26).

Condition (26) is not proved here.  It must not be replaced by a triangle
inequality, a separated coefficient/kernel norm, a low-degree one-sided
polynomial certificate, or compact-contour continuation.  Those moves
discard exactly the top interaction isolated above.

## 7. Result and boundary

The unconditional results of this note are:

1. the exact joint generating identity (5)-(7);
2. the exact \(Q_0\)-phase character expansion (9)-(13);
3. the proper-degree multilinear one-sided dual theorem (15)-(18);
4. the two exact proper-marginal comparators (19)-(21); and
5. the contour condition-number lower bound (22).

They rigorously kill the universal low-degree/Krawtchouk/proper-marginal
handoff and generic compact-contour recovery.  They do not lower-bound the
actual signed endpoint error, do not construct an actual product-multiset
counterexample, and do not prove a new Erdos-451 upper bound.

The sole survivor is the arithmetic high-conductor endpoint estimate
(26), equivalently the full-degree \(Q_0\)-phased interaction of the actual
product multiset.  It is recorded as a conditional decisive lemma with
closes equal to the empty list.
