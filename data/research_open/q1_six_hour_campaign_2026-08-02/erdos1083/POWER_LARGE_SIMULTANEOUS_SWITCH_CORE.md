# Erdős #1083: the power-large simultaneous-switch core

Date: 2026-08-02

## 0. Result

Work in the literal exact block of
`HEAVY_FACTOR_HUB_RULED_CHART.md`.  Thus

\[
 P_V=P_{A_i}F_i,\qquad F_i=P_{\lambda_iX},\qquad
 |X|=S,\quad |A_i|=U<S^2,
\tag{0.1}
\]

and a centre row \(0\) is transverse to a common-tangent leaf family.
There is a subfamily \(J\), of size

\[
 K\ge \left\lceil
 \frac{|L|}{\lfloor\log _2U\rfloor}
 \right\rceil=t^{5/9-o(1)},
\tag{0.2}
\]

and one nonconstant irreducible factor \(G\) dividing every \(F_j\),
\(j\in J\), with \(g:=G(1)\ge2\) after normalization by a unit.

The entire family has the simultaneous normal form

\[
 \boxed{
 \begin{aligned}
 F_j&=G R_j, & P_{A_0}&=G B,\\
 B&=R_jQ_j, & P_{A_j}&=F_0Q_j
 \end{aligned}}
 \qquad(j\in J).
\tag{0.3}
\]

Its augmentations are

\[
 R_j(1)=S/g,\qquad B(1)=U/g,\qquad
 \boxed{Q_j(1)=C:=U/S<S.}
\tag{0.4}
\]

Both \(P_{A_0}=GR_jQ_j\) and every \(P_{A_j}=F_0Q_j\) are positive
\(0/1\) masks, although the three individual factors in (0.3) need
not be positive.

Moreover, if \(\Omega(B)\) is the number of nonconstant irreducible
factor occurrences of \(B\), counted with multiplicity, then

\[
 \boxed{\Omega(B)\ge\log _2\left\lceil K/2\right\rceil
       =(5/9-o(1))\log _2t.}
\tag{0.5}
\]

Thus the almost-full hub, not only the smaller full-skeleton family,
already carries a logarithmically large weighted subset-sum atlas.

Finally every row obeys an exact clean/contaminated dichotomy.  Put

\[
 W_0=\operatorname{span}_{\mathbb Q}(\operatorname{supp}F_0-
 \operatorname{supp}F_0),\qquad
 W(Q_j)=\operatorname{span}_{\mathbb Q}
 (\operatorname{supp}Q_j-\operatorname{supp}Q_j).
\tag{0.6}
\]

If \(W(Q_j)\cap W_0=\{0\}\), then \(Q_j\) is necessarily a \(C\)-term
\(0/1\) mask and

\[
 A_0=\lambda_jX\oplus\operatorname{supp}Q_j,
 \qquad
 A_j=\lambda_0X\oplus\operatorname{supp}Q_j.
\tag{0.7}
\]

Consequently every genuinely signed switch satisfies

\[
 \boxed{W(Q_j)\cap W_0\ne\{0\}.}
\tag{0.8}
\]

Define

\[
 J_{\rm clean}=\{j:W(Q_j)\cap W_0=\{0\}\},\qquad
 J_{\rm cont}=J\setminus J_{\rm clean}.
\tag{0.9}
\]

The dichotomy is first rowwise, and only then pigeonholed:

\[
 \boxed{
 \max\{|J_{\rm clean}|,|J_{\rm cont}|\}
 \ge \left\lceil\frac K2\right\rceil
 =t^{5/9-o(1)}.}
\tag{0.10}
\]

On the clean class both switches are direct.  On the contaminated
class the only automatic conclusion is
\(W(Q_j)\cap W_0\ne\{0\}\): a contaminated quotient may still be a
positive mask and need not be signed.

There is a separate mask/signed pigeonhole.  If an integral \(Q_j\)
has no negative coefficient, then positivity of the mask
\(F_0Q_j\) forces every nonzero coefficient of \(Q_j\) to equal one
and forbids support collisions.  Thus \(Q_j\) is already a mask and
both switches are direct.  Consequently at least
\(\lceil K/2\rceil\) rows have direct mask quotients, or at least that
many rows have genuinely signed quotients; the latter rows form a
subfamily of \(J_{\rm cont}\).  This second alternative must not be
identified with (0.10).

## 1. Derivation of the simultaneous normal form

Centre--leaf transversality and exact directness give

\[
 \gcd(F_0,F_j)=1,
 \qquad F_j\mid P_{A_0}.
\tag{1.1}
\]

The heavy-factor hub supplies one irreducible \(G\mid F_j\) for all
\(j\in J\).  Choose its sign so that \(g=G(1)\ge2\), and define

\[
 R_j=F_j/G,\qquad B=P_{A_0}/G.
\tag{1.2}
\]

Since \(F_j\mid P_{A_0}\), cancellation gives \(R_j\mid B\); write
\(B=R_jQ_j\).  Now

\[
 G B F_0=P_{A_0}F_0=P_{A_j}F_j=P_{A_j}G R_j.
\tag{1.3}
\]

Cancel \(G R_j\) in the Laurent domain to obtain
\(P_{A_j}=F_0Q_j\).  Evaluating at the augmentation proves (0.4).
In particular \(S\mid U\), so \(C\) is a positive integer.

This is simultaneous positivity, not merely divisibility: the left
side \(GR_jQ_j=P_{A_0}\), every switched complement
\(F_0Q_j=P_{A_j}\), and the total spectrum are all honest masks.

## 2. Divisor complexity on the almost-full family

If \(R_j\) and \(R_k\) are Laurent associates, then so are
\(F_j=GR_j\) and \(F_k=GR_k\).  Two \(0/1\) scalar-copy masks can be
associates only by translation, hence

\[
 \lambda_j(X-X)=\lambda_k(X-X).
\tag{2.1}
\]

Numerical width gives \(|\lambda_j|=|\lambda_k|\), so
\(\lambda_j/\lambda_k=\pm1\).  Since row scalars are distinct, every
associate class of residuals contains at most two rows.  Therefore
the \(R_j\)'s occupy at least \(\lceil K/2\rceil\) divisor-associate
classes of \(B\).

If

\[
 B\sim\prod_{\nu=1}^r H_\nu^{m_\nu},\qquad
 \Omega(B)=\sum_{\nu=1}^rm_\nu,
\tag{2.2}
\]

the number of divisor-associate classes is

\[
 \prod_{\nu=1}^r(m_\nu+1)
 \le 2^{\Omega(B)}.
\tag{2.3}
\]

This proves (0.5).  Constant integer primes do not occur: the mask
\(P_{A_0}=GB\) has content one, so \(G\) and \(B\) are primitive.

There is also a concrete width atlas.  Let

\[
 D=\max X-\min X,\qquad a=\operatorname{wd}(G),
\tag{2.4}
\]

and list the positive widths of the factor occurrences of \(B\) as
\(d_1,\ldots,d_R\).  For each row a divisor multiplicity vector gives

\[
 b_j:=\operatorname{wd}(R_j)=\sum_{\nu=1}^R
 \epsilon_{j,\nu}d_\nu,
 \qquad |\lambda_j|=(a+b_j)/D.
\tag{2.5}
\]

Choose \(\sigma\in\{-1,1\}\) so that

\[
 J_\sigma=\{j:\operatorname{sgn}(\lambda_j)=\sigma\},
 \qquad |J_\sigma|\ge\lceil K/2\rceil.
\]

On this same-sign class the \(b_j\)'s are distinct.  If \(h\ne0\) is
a fixed Newton direction of \(G\), then, for \(j\in J_\sigma\), the
common-tangent target parameters satisfy

\[
 \boxed{
 \lambda_j=\frac{\sigma(a+b_j)}D,\qquad
 z_j=\frac{\sigma(a+b_j)}{2\rho D},\qquad
 w_j=\frac{\sigma hD}{a+b_j}.}
\tag{2.6}
\]

For \(j,k\in J_\sigma\), and only after this same-sign restriction,
target--target squared distances on the common tangent are

\[
 \boxed{
 \|q_{j,\tau_0}-q_{k,\tau_0}\|^2
 =\frac{(b_j-b_k)^2}{4\rho^2D^2}.}
\tag{2.7}
\]

The sign restriction is essential.  Here is a literal exact-block
witness, including the centre's common tangent.  Take

\[
 X=\{-1/2,1/2\},\qquad
 \rho^2=\sqrt2,\qquad \beta=1+2\sqrt2,
 \qquad \lambda_0=\beta,\quad \lambda_+=1,\quad\lambda_-=-1.
\tag{2.8}
\]

The two leaf masks coincide, \(P_X=P_{-X}=:G\), whereas
\(F_0=P_{\beta X}\) is transverse to \(G\).  For a sufficiently large
common translation \(R\), put

\[
 \widetilde V=R+(\beta X\oplus X),\qquad
 A_0=R+X,\qquad A_+=A_-=R+\beta X.
\tag{2.9}
\]

These are three exact direct rows with \(S=U=2<S^2\).  Set

\[
 z_i=\frac{\lambda_i}{2\rho},\qquad
 T_i=A_i-\rho^2-z_i^2.
\tag{2.10}
\]

Then every row spectrum is literally \(\widetilde V\).  Moreover

\[
 \frac12-\frac{\beta^2}{4\rho^2}
 =-\frac\beta2-\frac1{4\rho^2},
\tag{2.11}
\]

so one tangent belongs to \(T_0\cap T_+\cap T_-\); large \(R\) makes
all tangents positive.  Both leaf residuals are units, hence
\(b_+=b_-=0\), but on the shared tangent

\[
 \|q_{+,\tau}-q_{-,\tau}\|^2
 =(z_+-z_-)^2=\frac1{\rho^2}>0.
\tag{2.12}
\]

Thus applying (2.7) across the two sign classes would incorrectly give
zero.  In general the numerator before fixing the sign is
\(
[\operatorname{sgn}(\lambda_j)(a+b_j)
 -\operatorname{sgn}(\lambda_k)(a+b_k)]^2
\), not \((b_j-b_k)^2\).

## 3. The clean-quotient lemma

Write \(Q_j=\sum_q c_q[q]\), with every \(c_q\ne0\).  Suppose
\(W(Q_j)\cap W_0=\{0\}\).  If

\[
 f+q=f'+q',\qquad f,f'\in\operatorname{supp}F_0,
 \quad q,q'\in\operatorname{supp}Q_j,
\tag{3.1}
\]

then \(f-f'=q'-q\in W_0\cap W(Q_j)\), so \(f=f'\) and \(q=q'\).
Thus the support-sum map is injective.  In the product

\[
 P_{A_j}=F_0Q_j
\tag{3.2}
\]

the coefficient at \(f+q\) is exactly \(c_q\).  Since \(P_{A_j}\) is
a \(0/1\) mask, every \(c_q=1\).  Hence \(Q_j\) is a mask, and
\(|\operatorname{supp}Q_j|=Q_j(1)=C\).  Equation (3.2) is direct;
\(P_{A_0}=F_jQ_j\) is direct as well because it too is a \(0/1\)
product of masks.  This proves (0.7)--(0.8).

The lemma uses the direction of the *quotient*.  Leaf--centre
transversality alone does not imply (0.6), because \(Q_j\) may mix
directions from both sides.  The signed two-row construction in
`SIMULTANEOUS_POSITIVE_COMPLEMENT_NO_GO.md` does exactly that.

## 4. Cyclotomic same-line candidates and the first budget barrier

The natural attempt to realize power-many contaminated switches is
the same-line construction.  Let \(S\) be prime, \(S\nmid M\), and put

\[
 F_m(y)=P_S(y^m)=1+y^m+\cdots+y^{(S-1)m}
 \qquad(m\mid M).
\tag{4.1}
\]

Then

\[
 F_m=\prod_{d\mid m}\Phi_{Sd}(y),
 \qquad F_m\mid F_M.
\tag{4.2}
\]

With an independent centre mask \(F_0=P_S(x)\), a common two-variable
regularizer \(Q=Q(x,y)\) gives

\[
 F_MQ\quad\hbox{and}\quad
 F_0R_m,\qquad R_m:=\frac{F_M}{F_m}Q
\tag{4.3}
\]

\(0/1\) masks for every selected \(m\), with

\[
 1\le Q(1)=R_m(1)=C<S.
\tag{4.4}
\]

The individual \(Q\) and \(R_m\) may be signed. First consider the
stronger positive-quotient subcase in which \(R_m\) itself is a mask.
There is then a sharp large-prime-power obstruction. Let
\(p\mid M\), put

\[
 a=v_p(m),\qquad e=v_p(M),
\]

and suppose \(a<e\).  Then \(p^{a+1}\mid M\) but
\(p^{a+1}\nmid m\), so the exact factorization (4.2) gives

\[
 \boxed{\Phi_{S p^{a+1}}(y)\mid F_M/F_m\mid R_m.}
\tag{4.5}
\]

Here \(p\ne S\), since \(S\nmid M\).  A nonzero polynomial with
nonnegative integer coefficients divisible by
\(\Phi_{S p^{a+1}}(y)\) has coefficient mass at least
\(\min\{S,p\}\).  Indeed, split it into fibres of the other variables;
each fibre remains divisible by this monic polynomial in \(y\).
Evaluating a nonzero fibre at a primitive root of exact order
\(S p^{a+1}\) gives a nonempty vanishing sum of roots of that order,
whose minimum length is its least prime divisor \(\min\{S,p\}\).
Since \(R_m\) is a \(C\)-term mask, therefore

\[
 \boxed{C\ge\min\{S,p\}.}
\tag{4.6}
\]

At the endpoint

\[
 C=t^{1/18+o(1)}\ll S=t^{7/9+o(1)},
\tag{4.7}
\]

both \(S\) and every prime \(p>C\) exceed \(C\).  Hence (4.6) forces

\[
 \boxed{v_p(m)=v_p(M)\qquad(p>C).}
\tag{4.8}
\]

Thus all divisor-coordinate variation in the positive-\(R_m\) submodel is
confined to prime-power coordinates based on primes at most \(C\),
not merely to the presence or absence of those primes.  The smallest
boundary missed by a support-only statement is

\[
 S=3,\qquad C=1,\qquad M=4,\qquad m=2.
\]

Here the large prime \(2>C\) divides both \(m\) and \(M\), but its
valuation drops.  Precisely

\[
 \frac{P_3(y^4)}{P_3(y^2)}=y^4-y^2+1=\Phi_{12}(y),
\]

whose nonnegative multiples have mass at least two, contradicting
\(C=1\).

The small-prime family is now closed even without assuming
\(R_m\ge0\). The quadratic simultaneous-positive theorem in
CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md proves that, for
every selected family \({\cal D}\),

\[
 \boxed{
 |{\cal D}|
 \le1+2\sum_{r=2}^{C}\varphi(r)
 \le C^2.}
\tag{4.9}
\]

Here is the mechanism. For \(m,n\in{\cal D}\), put
\(g=(m,n)\), \(a=m/g\), and \(b=n/g\). The reduced cyclotomic factors

\[
 H_{S,a}(y^g)=F_m/F_g,\qquad
 H_{S,b}(y^g)=F_n/F_g
\]

are coprime. The common-product identity forces
\(H_{S,a}(y^g)\mid R_n\) and \(H_{S,b}(y^g)\mid R_m\).
Although \(R_n\) may be signed, reducing the positive mask
\(P_S(x)R_n\) modulo \(x^S=1\) produces a nonnegative shadow of mass
exactly \(C\), preserving every factor independent of \(x\). A sharp
CRT--Fourier lemma says that a nonnegative multiple of
\(H_{S,a}\) has mass at least \(\min\{S,a\}\). Since \(C<S\),

\[
 a\le C,\qquad b\le C.
\tag{4.10}
\]

Fixing one \(m_0\), all reduced ratios \(m/m_0\) therefore lie among
the coprime pairs in \([C]^2\), proving (4.9). At the endpoint,

\[
 |{\cal D}|\le C^2=t^{1/9+o(1)}
 \ll t^{5/9-o(1)}.
\tag{4.11}
\]

This completely excludes a power-large same-line cyclotomic
simultaneous-positive family, including signed quotients. The theorem
extends to every centre mask which tiles a finite abelian quotient;
see FINITE_QUOTIENT_SHADOW_ESCAPE.md.

## 5. Exact open gate

Apply the rowwise partition (0.9) and then (0.10).  The endpoint problem
inside the literal block has now been reduced to one of two alternatives,
each on at least \(\lceil K/2\rceil=t^{5/9-o(1)}\) rows:

1. **clean branch:** power-many exact two-way tilings by an \(S\)-term
   scalar copy and a \(C=t^{1/18+o(1)}\)-term complement;
2. **contaminated branch:** power-many complementary divisors \(Q_j\)
   of one \(B\), all with augmentation \(C\), all made positive after
   multiplication by the same centre mask, and all returning a
   nonzero direction to \(W_0\).  These quotients may be masks or may
   be signed; contamination alone does not decide positivity.

The same-line cyclotomic model is no longer an open gate: (4.9)--(4.11)
exclude it by a polynomial margin, even when its quotients are signed.
The finite-quotient shadow theorem extends this exclusion to every
centre which tiles a finite abelian quotient.

Neither result closes the full contaminated branch.
FINITE_QUOTIENT_SHADOW_ESCAPE.md gives the smallest aperiodic local
escape:

\[
 (1+x+x^4)(1-x^4+x^5+x^7)
 =1+x+x^6+x^7+x^9+x^{11},
\]

where the signed quotient has augmentation \(2<3\), while
\(1+x+x^4\) has no root-of-unity zero and hence no finite-quotient
tiling shadow.

Moreover, MULTIDIRECTIONAL_TENSOR_SWITCH_BARRIER.md constructs
\(2^k-1\) signed contaminated switches satisfying the displayed
identities, augmentations, divisor conditions, and positivities in
(0.3)--(0.4), at the exact endpoint scales. It is not an exact-block
countermodel for two separate reasons: it takes \(F_0=G\), so the
centre--leaf transversality/coprimality interface fails, and its mixed
tensor source masks are not all scalar copies of one \(X\). Indeed every
homothety class in that model has at most \(k+1\) rows, and this
logarithmic bound is sharp.

There is also a partial firewall against repairing the tensor model by
making its centre transverse. The all-subset fibre theorem in
`PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md` says that if

\[
 A_J=F_0H\prod_{i\in J}(1-z_i+z_i^2)
\]

is a mask for every \(J\subseteq[k]\), the centre is transverse to the
switch span, and the projected regularizer \(\pi_W(H)\) is nonnegative,
then \(2^k\le C\). The nonnegativity of \(\pi_W(H)\) is an additional
hypothesis, not a consequence of the exact block. Hence this rules out
only a no-cancellation transverse tensor repair; a strongly signed
aperiodic quotient projection remains possible.

For a binary-box centre, even that projected-sign escape disappears.
TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md constructs a finite quotient
which both tiles the centre and annihilates the transverse leaf span, so
the positive mass-\(C\) shadow preserves all independent \(\Phi_6\)
switch factors even when the original quotient is signed. For tensor
patterns \(\epsilon,\eta\),

\[
 |\epsilon\setminus\eta|,\ |\eta\setminus\epsilon|
 \le\lfloor\log_2C\rfloor.
\]

At \(S=2^k\), \(C=S^{1/14}\), the whole pattern family is at most

\[
 \sum_{r\le k/7}\binom kr
 \le S^{H_2(1/7)}
 =t^{0.4601899388\ldots},
\]

below \(t^{5/9-o(1)}\). In particular the uniform scalar-copy endpoints
\(X\) and \(3X\) would force \(C\ge2^k=S\), contradicting \(C<S\).
This closes the signed transverse repair of the independent-\(\Phi_6\)
binary-box tensor model, but not an arbitrary source \(X\) or arbitrary
residual divisors.

The first open algebraic gate is therefore a *transverse scalar-copy*
simultaneous-switch theorem: use simultaneously
\(\gcd(F_0,GR_j)=1\), the fact that every \(GR_j\) is a homothetic copy
\(P_{\lambda_jX}\), and positivity of every \(F_0Q_j\), to rule out a
power-large aperiodic multidirectional family. Alternatively, geometry
must turn the contaminated directions into additional common-tangent
distances.

No claim here extracts the exact block from the original point set or
settles Erdős #1083.

## 6. Reproduction

```bash
python3 verify_power_large_simultaneous_switch_core.py
python3 -m unittest -v test_power_large_simultaneous_switch_core.py
```

The verifier checks the exact quotient ledger, divisor-count bound,
same-sign width atlas, literal mixed-sign boundary, clean-quotient
coefficient mechanism, both branch pigeonholes, exact endpoint triple,
and finite cyclotomic prime-valuation instances.  The all-parameter
statements are proved above.
