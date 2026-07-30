# Growing-depth Newton positivity from the exact heat operator

Date: 2026-07-30

Status: human proof with an explicit (deliberately non-optimized) uniform
remainder; symbolic and exact-count regression supplied.

### Variable dictionary

The several “depth” parameters are kept separate:

- \(k\) is the original coefficient index in \(C_k(n)\);
- \(q_0=\lfloor(k-2)/2\rfloor\) is the capacity boundary;
- \(r\) is the Newton depth, so the target is \(a_{k,q_0+r}\);
- \(N=q_0+4+r\) is the vertex count in the last Newton-inversion term;
- \(T=t_0+2r\) is that term's total component count;
- \(R=T-2\) is its total component excess;
- \(\rho=c_{\rm L}-1\) and \(\sigma=c_{\rm R}-1\) are the two
  individual component excesses, with \(\rho+\sigma=R\);
- \(J\) is an order in the \(1/n\) heat expansion.  The symbol \(d\)
  used in the diagonal-component note has this same role as \(J\), not
  the role of a component count or Newton depth.

## 1. Result

Use the notation of `FIXED_DEPTH_ASYMPTOTIC_THEOREM.md`.  Thus
\[
\mathcal C_t(n)=
\sum_{\substack{c,d\geq1\\c+d=t}}
\left(W_{1,c}(n)W_{1,d}(n)-W_{0,c}(n)W_{2,d}(n)\right)
\]
and
\[
a_{k,q_0+r}
=\frac{(k-2)!}{2}\sum_{j=0}^r(-1)^{r-j}
\binom{q_0+r}{r-j}
\mathcal C_{t_0+2j}(n_0+j).
\tag{1}
\]

The fixed-depth restriction can be removed up to the square-root scale.

### Theorem 1 (growing-depth positivity)

Let \(r=r(k)\) be any nonnegative integer sequence satisfying
\[
r=o(\sqrt{k}).
\]
Put
\[
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor,\qquad
N=q_0+4+r
\]
and
\[
T=
\begin{cases}
3+2r,&k\ \mathrm{odd},\\
4+2r,&k\ \mathrm{even}.
\end{cases}
\]
Then
\[
\boxed{
a_{k,q_0+r}
=\frac{2(k-2)!}{(T-3)!}N^{2N-8}
\left(1+o(1)\right)
}
\tag{2}
\]
Equivalently,
\[
\boxed{
\frac{a_{k,q_0+r}}
{\frac{2(k-2)!}{(T-3)!}N^{2N-8}}
\longrightarrow1.
}
\tag{3}
\]
In particular,
\[
\boxed{a_{k,q_0+r}>0}
\]
for all sufficiently large \(k\) along every such sequence.
Thus the little-\(o\) is uniform in the sequential sense: for every
choice of integers \(k_\nu\to\infty\) and
\(r_\nu/\sqrt{k_\nu}\to0\), the ratio in (3) tends to one.

The engine is the following uniform determinant estimate.

### Theorem 2 (uniform component-total asymptotic)

Let \(t=t(n)\geq3\), and put \(R=t-2\).  If
\[
R=o(\sqrt n),
\]
then
\[
\boxed{
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}\bigl(1+o(1)\bigr).
}
\tag{5}
\]
That is, (5) holds along every integer sequence
\(n_\nu\to\infty\), \(t_\nu\geq3\), with
\((t_\nu-2)/\sqrt{n_\nu}\to0\).
More explicitly, if
\[
n\geq4096(R+1)^2,
\tag{6}
\]
then
\[
\boxed{
\left|
\frac{\mathcal C_t(n)}{n^{2n-6}}
-\frac{4R}{R!\,n^2}
\right|
\leq
\frac{2^{50}(R+1)^3}{R!\,n^3}.
}
\tag{7}
\]
The numerical constant is intentionally wasteful.  Its value is useful only
because (7) is a checkable remainder bound rather than fixed-\(t\)
\(O_t(\cdot)\) notation.

## 2. Independent check of the heat representation

Put \(u=1/n\), \(D=d/dx\), and
\[
\phi_a(x)=(1+x/n)^{n-a}.
\]
For a formal Gaussian variable \(G\), define
\[
Y=z+i\sqrt z\,G.
\]
This notation means the polynomial moment functional determined by
\[
\mathbb E e^{sY}=\exp\left(zs-\frac z2s^2\right);
\tag{8}
\]
no probabilistic positivity is being assumed.

Because
\[
\exp\left(zwD-\frac z2w^2D^2\right)\phi_a(0)
=\mathbb E\phi_a(wY),
\tag{9}
\]
applying \(1+w\partial_w\) for \(a=1\) gives
\[
\boxed{
G_{0,n}(z)
:=\sum_{r\geq0}\frac{W_{0,r+1}(n)}{n^{n-2}}z^r
=\mathbb E\left[(1+Y)(1+Y/n)^{n-2}\right].
}
\tag{10}
\]
Indeed,
\[
\left.(1+w\partial_w)(1+wY/n)^{n-1}\right|_{w=1}
=(1+Y)(1+Y/n)^{n-2}.
\]
Likewise, applying \(3+w\partial_w\) for \(a=3\) gives
\[
\boxed{
G_{A,n}(z)
:=\sum_{r\geq0}\frac{A_{r+1}(n)}{n^{n-4}}z^r
=\mathbb E\left[(3+Y)(1+Y/n)^{n-4}\right].
}
\tag{11}
\]

Expanding (9) directly in \(z\) also recovers the finite formulas
\[
[z^r]H_1(z,w)
=\sum_{j=0}^r
\frac{(-1/2)^jw^{r+j}}{j!(r-j)!}
\prod_{\ell=1}^{r+j}(1-\ell/n),
\tag{12}
\]
and its \(a=3\) analogue with
\(\prod_{\ell=3}^{r+j+2}(1-\ell/n)\).
The two \(w\)-derivatives multiply the summands by \(r+j+1\) and
\(r+j+3\), respectively.  Thus (10)--(11) agree term by term with the
Liu--Chow and adjacent-pair contraction formulas; they are not merely
asymptotic ansätze.

## 3. Orbit identities and the exact determinant OGF

Let \(\vartheta=z\,d/dz\).  Define normalized OGFs
\[
B_i(z)=\sum_{r\geq0}
\frac{W_{i,r+1}(n)}{n^{n-2-i}}z^r
\quad(i=0,1,2),
\]
so \(B_0=G_{0,n}\).  Edge incidence gives
\[
B_1
=\frac2{1-u}\left(1-u(1+\vartheta)\right)B_0.
\tag{13}
\]
The adjacent/disjoint edge-pair orbit identity gives
\[
B_2=
\frac{
4(1-u(1+\vartheta))(1-u(2+\vartheta))B_0
-4u(1-u)(1-2u)G_{A,n}}
{(1-u)(1-2u)(1-3u)}.
\tag{14}
\]
Consequently
\[
\boxed{
\frac{\mathcal C_t(n)}{n^{2n-6}}
=[z^{t-2}]
\left(B_1(z)^2-B_0(z)B_2(z)\right).
}
\tag{15}
\]
Equations (10)--(15) are exact for every admissible \(n,t\).

## 4. A coefficientwise heat remainder

The point of the heat representation is that its coefficient saddle has
width \(\sqrt \rho\), not \(\rho\).  Here \(\rho\) is one component
excess; it is distinct from the Newton depth \(r\) in Theorem 1.

### Lemma 3 (explicit heat remainder)

Let
\[
g_\rho=\frac1{2^\rho \rho!}.
\]
For \(n\geq4096(\rho+1)^2\), the coefficients of (10)--(11) satisfy
\[
\begin{aligned}
\frac{[z^\rho]G_{0,n}}{g_\rho}
={}&1+\frac{5\rho}{n}
+\frac{\rho(35\rho-47)}{2n^2}+E_{0,\rho},\\
\frac{[z^\rho]G_{A,n}}{g_\rho}
={}&3+\frac{11\rho}{n}
+\frac{5\rho(13\rho-37)}{2n^2}+E_{A,\rho},
\end{aligned}
\tag{16}
\]
with
\[
|E_{0,\rho}|+|E_{A,\rho}|
\leq
\frac{2^{28}(\rho+1)^3}{n^3}.
\tag{17}
\]
After applying (13)--(14),
\[
\begin{aligned}
\frac{[z^\rho]B_1}{g_\rho}
={}&2+\frac{8\rho}{n}
+\frac{\rho(25\rho-49)}{n^2}+E_{1,\rho},\\
\frac{[z^\rho]B_2}{g_\rho}
={}&4+\frac{12\rho}{n}
+\frac{2\rho(17\rho-57)}{n^2}+E_{2,\rho},
\end{aligned}
\tag{18}
\]
where
\[
|E_{1,\rho}|+|E_{2,\rho}|
\leq
\frac{2^{34}(\rho+1)^3}{n^3}.
\tag{19}
\]

### Proof of Lemma 3

Write
\[
q(s)=s-\frac{s^2}{2}.
\]
Taking the coefficient of \(z^\rho\) in (8) gives the exact operator identity
\[
[z^\rho]\mathbb E f(Y)
=\frac1{\rho!}\left.f(D)q(s)^\rho\right|_{s=0}.
\tag{20}
\]
Set
\[
\mathcal R_{b,n}(D)
=e^{-D}(1+D/n)^{n-b}.
\]
Translation by \(e^D\) turns (20) into
\[
\frac{[z^\rho]\mathbb E[(a+Y)(1+Y/n)^{n-b}]}{g_\rho}
=
\left.(a+D)\mathcal R_{b,n}(D)
(1-(s-1)^2)^\rho\right|_{s=1}.
\tag{21}
\]
The two cases needed are \((a,b)=(1,2)\) and \((3,4)\).

Since \(D\) is nilpotent on the polynomial in (21), the following logarithm
is an exact finite formal identity:
\[
\log\mathcal R_{b,n}(D)
=\sum_{j\geq1}\frac{A_{b,j}(D)}{n^j},
\qquad
A_{b,j}(D)=(-1)^j
\left(\frac{bD^j}{j}+\frac{D^{j+1}}{j+1}\right).
\tag{22}
\]
Therefore no complex logarithm, branch choice, or uncontrolled Taylor
domain is present: after application to degree \(2\rho\), (22) and its
exponential are finite operator sums.  Condition
\(4096(\rho+1)^2\leq n\) is used only to sum their absolute majorant.
Keeping weights \(0,1,2\) in the exponential gives
\[
\mathcal R_{b,n}
=1+\frac{A_{b,1}}n
+\frac{A_{b,2}+A_{b,1}^2/2}{n^2}
+\mathcal E_{b,n}.
\tag{23}
\]
The derivatives at the center are explicit:
\[
\left.D^{2h}(1-(s-1)^2)^\rho\right|_{s=1}
=(-1)^h(2h)!\binom \rho h,\qquad
\left.D^{2h+1}(1-(s-1)^2)^\rho\right|_{s=1}=0.
\tag{24}
\]
Substitution of (22)--(24) into (23) gives exactly (16).

For completeness, here is a numerical-constant audit of the omitted
weights.  A monomial of total \(1/n\)-weight \(J\) in the exponential
of (22):

- has differential degree between \(J\) and \(2J\);
- is zero in (21) when \(J>2\rho+1\);
- has, after summing ordered compositions of \(J\), the majorant
  \[
  \left|
  (a+D)n^{-J}[v^J]\exp\!\left(\sum_{j\geq1}v^jA_{b,j}\right)
  (1-(s-1)^2)^\rho\big|_{s=1}
  \right|
  \leq
  \frac{2^{7J}(\rho+1)^J J^J}{n^J}.
  \tag{25}
  \]

To check (25), use
\[
(2h)!\binom \rho h\leq(4\rho h)^h,
\tag{26}
\]
The coefficient of weight \(J\) before applying \(a+D\) is exactly
\[
\sum_{m=1}^J\frac1{m!}
\sum_{\substack{j_1+\cdots+j_m=J\\j_i\geq1}}
A_{b,j_1}\cdots A_{b,j_m}.
\tag{26a}
\]
Thus all multinomial/order multiplicities are present: for fixed \(m\)
there are \(\binom{J-1}{m-1}\) ordered compositions.  Each \(A_{b,j}\)
has two monomials, each of coefficient at most \(4\) because \(b\leq4\).
Consequently the scalar multiplicity in (26a) is at most
\[
\sum_{m=1}^J
\binom{J-1}{m-1}\frac{8^m}{m!}
\leq8\cdot9^{J-1}.
\tag{26b}
\]
Every resulting differential monomial has degree between \(J\) and
\(2J\).  In (24), exactly one of the \(a\)-part and the extra \(D\)-part
has even parity; hence \(a+D\) contributes a factor at most \(3\) and
the surviving derivative is \(D^{2h}\) with \(h\leq J\).  Equations
(26), (26b), and
\[
3\cdot8\cdot9^{J-1}
\bigl(4(\rho+1)J\bigr)^J
\leq2^{7J}(\rho+1)^JJ^J
\]
give (25).  This count includes the outer \(1/m!\); dropping it in
(26b) only makes the displayed upper bound larger.

Under \(4096(\rho+1)^2\leq n\), summing (25) for \(J\geq3\) gives
\[
\sum_{J\geq3}
\frac{2^{7J}(\rho+1)^J J^J}{n^J}
\leq
\frac{2^{27}(\rho+1)^3}{n^3}.
\tag{27}
\]
Indeed, after the \(J=3\) factor is removed, use
\(J\leq2\rho+1\leq2(\rho+1)\).  Each summand divided by
\((\rho+1)^3/n^3\) is at most
\[
2^{21}J^3
\left(\frac{128(\rho+1)J}{n}\right)^{J-3}
\leq
2^{21}J^3\,16^{-(J-3)}.
\]
The last series is below \(2^{26}\).  Allowing both \((a,b)\) cases
gives (17).

Finally, (13)--(14) are coefficientwise rational identities.
For \(u\leq1/4\), their three denominators have product at least
\(3/32\); multiplication by \(1-u(\rho+1)\) and
\(1-u(\rho+2)\), followed by the same second-order expansion, enlarges
the bound in (17) by less than \(16\).  The relaxed constant in
(19) therefore covers all four tails.  This proves Lemma 3.

## 5. Proof of the uniform determinant estimate

Put
\[
\rho=c_{\rm L}-1,\qquad
\sigma=c_{\rm R}-1,\qquad
\rho+\sigma=R=t-2.
\]
Insert (16) and (18) into one ordered summand of (15).  The constant
term cancels.  The coefficient of \(1/n\) is
\[
-4(\rho-\sigma),
\tag{28}
\]
so its convolution sum cancels under
\((\rho,\sigma)\leftrightarrow(\sigma,\rho)\).  The symmetrized
\(1/n^2\) coefficient is
\[
2\left(3R-(\rho-\sigma)^2\right).
\tag{29}
\]
The weights satisfy
\[
\sum_{\rho+\sigma=R}g_\rho g_\sigma=\frac1{R!},
\qquad
\sum_{\rho+\sigma=R}g_\rho g_\sigma(\rho-\sigma)^2
=\frac R{R!}.
\tag{30}
\]
Thus the summed \(1/n^2\) coefficient is
\[
\frac{4R}{R!}.
\tag{31}
\]

The explicit tails in Lemma 3 and the elementary bound
\[
\sum_{\rho+\sigma=R}
g_\rho g_\sigma(\rho+1)^i(\sigma+1)^j
\leq\frac{(R+1)^{i+j}}{R!}
\tag{32}
\]
show that everything of weight at least three has absolute value at
most
\[
\frac{2^{50}(R+1)^3}{R!\,n^3}.
\tag{33}
\]
Here (33) includes products of two remainders and the rational-orbit
tails.  A constants audit is as follows.  Under (6), each second-order
truncation in (16), (18) has absolute value at most \(8\).  Products of
their displayed \(1/n\) and \(1/n^2\) terms above weight two contribute
at most
\[
\frac{2^{20}(R+1)^3}{n^3}
\]
per ordered pair.  A single remainder contributes at most
\(8\cdot2^{34}(R+1)^3/n^3\).  Retaining the constants, a product of two
remainders is at most
\[
2^{68}\frac{(R+1)^6}{n^6}
\leq
2^{32}\frac{(R+1)^3}{n^3},
\]
because (6) gives
\((R+1)^3/n^3\leq2^{-36}(R+1)^{-3}\).
There are fewer than \(16\) resulting product types.  Convolution and
(32) therefore give a constant below \(2^{42}\); the stated \(2^{50}\)
leaves eight additional binary orders of slack.  Combining
(31)--(33) proves (7), hence (5).

The symbolic expansion supplies a useful check:
\[
\begin{aligned}
e^{-z}\left(B_1^2-B_0B_2\right)
={}&\frac{4z}{n^2}
+\frac{16z^2}{n^3}\\
&+\frac{40z^3-96z^2}{n^4}
+\frac{80z^4-610z^3}{n^5}
+O(n^{-6}).
\end{aligned}
\tag{34}
\]
The first two terms reproduce
\[
\frac4{(t-3)!}n^{2n-8}
+\frac{16}{(t-4)!}n^{2n-9}.
\]
Equation (34) is a regression check; the proof of the uniform remainder
is (20)--(33).

As an independent diagonal check, `diagonal_component_2026-07-30/`
defines
\[
\Delta_R(u)=R!\,\mathcal C_{R+2}(n)/n^{2n-6}
=\sum_dP_d(R)u^d
\]
and proves
\[
\deg P_d=d-1,\qquad
[R^{d-1}]P_d(R)=\frac23d(d^2-1).
\]
Applying \(R![z^R]e^z\) to each coefficient in (34) reproduces its
\(P_2,\ldots,P_6\) exactly.  This all-orders degree theorem is fully
compatible with (7), but by itself is coefficientwise and does not
bound the sum over \(d\) when \(R\) grows.  Lemma 3 supplies that missing
analytic control in the range \(R=o(\sqrt n)\).

## 6. Newton inversion does not destroy the range

Return to (1).  Its last term has vertex count \(N\), total component
count \(T\), and \(R=T-2\).  The term \(j=r-\ell\) has parameters
\[
N_\ell=N-\ell,\qquad R_\ell=R-2\ell.
\]
The truncation at \(j=0\) is exact, not an asymptotic convenience.
Capacity gives \(C_k(4+i)=0\) for \(i<q_0\); in the one even-parity
borderline case the additional identity
\[
W_{1,1}^2-W_{0,1}W_{2,1}=0
\]
supplies the same vanishing.  Hence (1) contains every nonzero support
term in the Newton inversion.
Let
\[
M(R,N)=\frac{4R}{R!}N^{2N-8}.
\]
For all admissible \(\ell\),
\[
\frac{M(R_\ell,N_\ell)}{M(R,N)}
\leq\left(\frac{R^2}{N^2}\right)^\ell.
\tag{35}
\]
This follows directly from
\[
\frac{R!}{(R-2\ell)!}\leq R^{2\ell}
\]
and
\[
(N-\ell)^{2(N-\ell)-8}
\leq N^{2N-8-2\ell}.
\]
Moreover \(q_0+r=N-4\), so
\[
\binom{q_0+r}{\ell}\leq\frac{N^\ell}{\ell!}.
\tag{36}
\]
Therefore all terms before the last one, in absolute value relative to
the last main term, are bounded by
\[
2\sum_{\ell\geq1}
\frac1{\ell!}\left(\frac{R^2}{N}\right)^\ell
=2\left(e^{R^2/N}-1\right)
\tag{37}
\]
once the determinant error in (7) is below its main term.

For an entirely explicit sufficient condition, assume
\[
N\geq8192(R+1)^2.
\tag{38}
\]
Then (7) applies to every \((R_\ell,N_\ell)\).  To ensure that its
error is at most the corresponding main term, impose the stronger
(still explicit) condition
\[
N\geq2^{52}(R+1)^2.
\tag{38a}
\]
Under (38a), equations (1), (7), and (35)--(37) give
\[
\left|
\frac{a_{k,q_0+r}}
{\frac{(k-2)!}{2}M(R,N)}-1
\right|
\leq
\frac{2^{51}(R+1)^2}{N}
+2\left(e^{R^2/N}-1\right).
\tag{39}
\]
The constant in (39), like that in (7), is not optimized.

### Corollary 4 (explicit finite sufficient window)

With the notation of Theorem 1, if
\[
\boxed{N\geq2^{54}(R+1)^2,}
\tag{40}
\]
then
\[
\boxed{a_{k,q_0+r}>0.}
\tag{41}
\]
Indeed, (40) implies (38a), while the right-hand side of (39) is at
most
\[
\frac18+2\left(e^{2^{-54}}-1\right)<1.
\]
Thus the normalized Newton coefficient differs from the positive main
term by less than one in relative value.  This finite window is
deliberately extremely conservative, but it is directly citable and
requires no asymptotic quantifier.

If \(r=o(\sqrt k)\), then \(R=O(r+1)\), \(N\asymp k\), condition
(38a) eventually holds, and the right-hand side of (39) tends to zero.
Since
\[
\frac{(k-2)!}{2}M(R,N)
=\frac{2(k-2)!}{(T-3)!}N^{2N-8},
\]
Theorem 1 follows.

This final summation is essential.  The positivity of every individual
\(\mathcal C_t(n)\) in a growing window would not by itself imply the
positivity of the alternating Newton sum (1).  Inequalities
(35)--(37) prove that the last positive term dominates the absolute
sum of all earlier terms when \(R^2/N\to0\).

## 7. Verification

Run

```bash
python3 verify_growing_depth_heat.py --order 6
python3 verify_growing_depth_heat.py --order 4 --stress-maximum-k 60
pytest -q test_verify_growing_depth_heat.py
```

The verifier:

1. derives (10)--(11) from the tilted Gaussian moments;
2. constructs (13)--(15);
3. checks
   \[
   0,\ 0,\ 4z,\ 16z^2,\ 40z^3-96z^2,\ldots
   \]
   for determinant weights \(0,1,2,3,4,\ldots\);
4. compares the heat coefficients with exact finite Liu--Chow and
   adjacent-pair sums;
5. checks an exact determinant coefficient for \(n=24,t=5\).

The optional exact-integer stress grid checks 317 Newton coefficients
for \(8\leq k\leq60\) and depths
\(0\leq r\leq\min(6,\lfloor\sqrt k\rfloor)\).  All are positive; the
smallest ratio to the final endpoint main term occurs at \((k,r)=(10,3)\)
and is approximately \(0.493\).  This is a stress test, not a premise
of the proof.

These computations verify algebra and normalization.  The analytic
uniformity is supplied by the majorant proof, not inferred from finite
tests.

## 8. Scope and remaining barrier

This attack proves positivity for every depth sequence
\[
r=o(\sqrt k),
\]
which is genuinely stronger than “every fixed \(r\).”  It does not cover
\(r\asymp\sqrt k\) with an arbitrary fixed constant, because the deliberately
coarse remainder in (7) is only \(O(R^2/n)\) relative to the main term.
It also does not approach \(r\asymp k\).

The symbolic kernel (34) suggests that the true expansion parameter may be
\(R/n\), since the exact \(n^{-4}\) term is only \(O(R^2/n^2)\) relative
to the main term.  Reaching \(R=o(n)\) would require preserving additional
cancellations inside the heat remainder rather than taking absolute values
component by component.  The next precise target is therefore a direct
coefficientwise majorant for the determinant kernel itself, not more
fixed-order component expansions.

## 9. Red-team audit

The thinnest analytic step is (25), because a careless absolute-value
bound on the original alternating Liu--Chow sum grows exponentially in
\(\rho\).  The centered identity (24) is what prevents that loss.
The proof above exposes every factor used in the majorant:
operator-weight compositions, the two monomials in \(A_{b,j}\), the
outer factorial, the centered derivative, and the finite
\(J\leq2\rho+1\) cutoff.  No unbounded analytic tail remains.

The next possible failure point is confusing determinant positivity
with Newton positivity.  Section 6 explicitly bounds the entire
alternating prefix by \(2(e^{R^2/N}-1)\); therefore the conclusion is
indeed
\[
a_{k,q_0+r}>0\qquad\text{for every }r=o(\sqrt k),
\]
not merely \(\mathcal C_t(n)>0\) for \(t=o(\sqrt n)\).

What is *not* proved is a uniform fixed-constant window
\(r\leq c\sqrt k\).  The present error tends to zero only when
\(r^2/k\to0\), and the explicit constants are far too large for useful
finite thresholds.  Extending the claim to \(r=O(\sqrt k)\) or
\(r=o(k)\) requires determinant-level cancellation beyond the
componentwise absolute majorant.
