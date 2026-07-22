# Erdős #143: rational-fibre bracket identity and direct numerator-GCD incidence

Date: 2026-07-22 (Asia/Hong_Kong)

Status: strict route conversion, not a proof of the weighted conjecture.  The
round-7 large-prime support cutoff is replaced by a direct cross-shell count
inside each rational equivalence class.  The calculation identifies exactly
which denominator sum a successful Carleson/GCD-graph estimate must control.

## 1. Old-route autopsy

The round-7 extremal-prime lemma is correct:

\[
 \sum_{\substack{p\mid st\\p>z}}{1\over p}>1
 \quad\Longrightarrow\quad
 \log(st)\ge z^{e-o(1)}.
\]

Moreover, exponent \(e\) is optimal from the trigger data alone.  Thus this
part is **correct but local**, and further improvement using only distinct
large prime divisors is a **proved method barrier**.

The later observation that a charge \(1/p\) cancels after writing \(t=pd\)
does not refute that lemma.  It refutes only the proposed naive Tonelli
summation of its pointwise majorant.  The remaining gap is genuinely an
incidence problem: one needs to count how often large rational height can
coexist with the primitive numerator/denominator constraints.  Separately,
Koukoulopoulos--Lamzouri--Lichtman's finite-event argument proves the
\(o(\log X)\) harmonic conclusion, not the convergence of
\(\sum_{\alpha\in A}1/(\alpha\log\alpha)\).

## 2. Exact bracket identity in one rational fibre

Fix one equivalence class for the relation
\(\alpha\sim\beta\iff\alpha/\beta\in\mathbb Q\).  Write its elements as

\[
 \alpha=\gamma{a\over q},\qquad
 \beta =\gamma{b\over r},                              \tag{1}
\]

where \(\gamma>0\), \(a,b,q,r\in\mathbb N\), and

\[
 (a,q)=(b,r)=1.                                       \tag{2}
\]

Assume \(\alpha>\beta\).  If

\[
 {\alpha\over\beta}={ar\over bq}={s\over t}
\]

is reduced, then

\[
 \boxed{
 [\alpha,\beta]
 ={\operatorname{lcm}(q,r)
   \over \gamma\gcd(a,b)}.
 }                                                     \tag{3}
\]

Here the left side is the KLL bracket
\(H(\alpha/\beta)/\max\{\alpha,\beta\}=t/\beta=s/\alpha\).

### Proof

Conditions (2) imply the elementary but useful identity

\[
 \boxed{\gcd(ar,bq)=\gcd(a,b)\gcd(q,r).}              \tag{4}
\]

This can be checked prime by prime.  If a prime divides both \(a,b\), then
it divides neither \(q,r\); if it divides both \(q,r\), it divides neither
\(a,b\).  In either mixed case, coprimality in (2) prevents it from dividing
both \(ar\) and \(bq\).  The valuations on the two sides of (4) therefore
agree.

Put \(g=\gcd(ar,bq)\).  Then \(t=bq/g\), and hence

\[
 [\alpha,\beta]={t\over\beta}
 ={bq/g\over\gamma b/r}
 ={qr\over\gamma g}.
\]

Substitution of (4) gives (3).

Formula (3) is invariant under changing the rational representative of the
fibre.  It says that a small KLL bracket is exactly a large *numerator GCD
relative to the denominator lcm*, not merely the presence of some large
prime in the rational height.

## 3. Conversion of the round-7 support theorem

For every fixed \(\eta>0\), the round-7 support lemma says that a surviving
\(E_3\) pair obeys

\[
 [\alpha,\beta]
 \ll_\eta\{\log(\alpha\beta)\}^{1/e+\eta}.             \tag{5}
\]

Combining (3) and (5) gives the direct primitive-incidence condition

\[
 \boxed{
 \gcd(a,b)
 \gg_{\eta}
 {\operatorname{lcm}(q,r)
  \over
  \gamma\{\log(\alpha\beta)\}^{1/e+\eta}}.
 }                                                     \tag{6}
\]

This is stronger information than the statement that \(st\) has a large
prime prefix: it locates the necessary concentration in a common divisor of
the two primitive numerators and explicitly exposes the lcm of the two
denominators.

## 4. A direct dyadic incidence bound

Let \(A,B\ge1\), \(D\ge1\).  The number of integer pairs

\[
 a\in(A,2A],\qquad b\in(B,2B],\qquad \gcd(a,b)\ge D
\]

satisfies

\[
 \boxed{
 \#\{(a,b):\gcd(a,b)\ge D\}
 \ll {AB\over D}+(A+B)\log(2\min(A,B))+\min(A,B).
 }                                                     \tag{7}
\]

Indeed,

\[
 1_{\gcd(a,b)\ge D}
 \le\sum_{\substack{d\mid a,\ d\mid b\\d\ge D}}1,
\]

and summing
\((A/d+1)(B/d+1)\) over
\(D\le d\le2\min(A,B)\) proves (7).  The coprimality conditions in (2)
can only reduce this count.

For elements in dyadic shells

\[
 \alpha\asymp X,\qquad \beta\asymp Y,
\]

the numerator lengths are

\[
 A\asymp {qX\over\gamma},\qquad
 B\asymp {rY\over\gamma}.
\]

If \([\alpha,\beta]\le T\), equation (3) imposes

\[
 D={\operatorname{lcm}(q,r)\over\gamma T}.
\]

When this displayed \(D\) is below one, replace it by one in (7); the
resulting trivial bound is still at most the expression obtained by using
the displayed \(D\).

The main term of (7) then becomes

\[
 {AB\over D}
 \asymp {\gcd(q,r)\,TXY\over\gamma}.                 \tag{8}
\]

Equivalently, relative to all numerator pairs in these two fibres, the
main-term density is

\[
 \ll {\gamma T\over\operatorname{lcm}(q,r)}.          \tag{9}
\]

Equations (7)--(9) are the promised cross-shell/primitive-incidence
replacement for the old prime-by-prime charging step.

## 5. Why the direct count still does not close

After multiplying a pair in the two shells by the natural vertex weights

\[
 \kappa(\alpha)\kappa(\beta)
 \asymp {1\over XY\log X\log Y},
\]

the main term (8) has scale

\[
 {\gcd(q,r)\,T\over
  \gamma\log X\log Y}.                                \tag{10}
\]

The round-7 support theorem makes \(T\) polylogarithmic, but (10) still has
to be summed over all occupied denominator pairs \((q,r)\).  There is no
free decay in \(q,r\): the lcm gain in (9) is exactly changed into the
\(\gcd(q,r)\) factor after counting the available numerators.  The boundary
terms in (7) are also non-negligible for very thin numerator fibres.

Thus the next required theorem is not another support cutoff.  It is a
weighted incidence inequality which uses both facts simultaneously:

1. for each fixed denominator, the occupied numerator set is primitive;
2. across denominators, the large-\(\gcd(a,b)\) events in (6) cannot occur at
   the unrestricted divisor-counting rate.

A suitable target is a Carleson/GCD-graph bound for the bilinear divisor
energies

\[
 \sum_d
 \left(\sum_{q}\sum_{\substack{a:\ d\mid a}}
       w_{q,a}\right)
 \left(\sum_r\sum_{\substack{b:\ d\mid b}}
       w_{r,b}\right),                                \tag{11}
\]

with the threshold \(d\gtrsim\operatorname{lcm}(q,r)/(\gamma T)\) retained
inside the two denominator sums.  Dropping that coupling recreates (10)
and loses.

## 6. Strict conclusion

The new direction succeeds in converting the surviving \(E_3\) geometry
to an exact primitive numerator-GCD incidence problem and proves the
elementary dyadic count (7).  It does not establish the required coupled
Carleson inequality (11), and it does not supply the separate bridge from
finite-event density estimates to convergence of
\(\sum1/(\alpha\log\alpha)\).  Erdős #143 therefore remains open.

The identity (3) is consistent with the numerator/denominator GCD product
used implicitly in KLL's GCD graphs; no literature-priority claim is made.
