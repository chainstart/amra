# OPG-1757: all-depth top face and two deepest pooled layers

Date: 2026-07-31

## 1. Result

Let
\[
P_s^{(2)}(\beta,t)
=\sum_{n\geq 0}\binom{t}{n}B_n(s,\beta)
\]
be the normalized disjoint-core \(\alpha^2\) Rayleigh layer for the
complete-split family, with \(s\geq4\).  Then, for every \(n\geq0\),
\[
\boxed{
[\beta^{4s-10}]B_n(s,\beta)
=4s^{2s-8}n!
\left(
\left\{\!\!\begin{matrix}2s-5\\n\end{matrix}\!\!\right\}
-
\left\{\!\!\begin{matrix}2s-6\\n\end{matrix}\!\!\right\}
\right),
}
\tag{1}
\]
where the braces are Stirling numbers of the second kind.

Consequently:

1. the coefficient in (1) is strictly positive for every
   \(2\leq n\leq2s-5\);
2. \(B_n(s,\beta)=0\) for every \(n>2s-5\);
3. the deepest nonzero pooled layer is completely determined:
   \[
   \boxed{
   B_{2s-5}(s,\beta)
   =4s^{2s-8}(2s-5)!\,\beta^{4s-10}>_{\rm coeff}0;
   }
   \tag{2}
   \]
4. the exact nonzero depth range is \(2\leq n\leq2s-5\).

Thus (1) is an unbounded theorem across **all pooled depths at once**, and
(2) closes a new pooled layer whose depth grows linearly with \(s\).
Moreover, the next layer is also completely positive:
\[
\boxed{
\begin{aligned}
B_{2s-6}(s,\beta)
={}&4(2s-6)!\,s^{2s-10}\beta^{4s-12}\\
&\times\left[
s^2+4s-24
+2s(s^2-s-8)\beta
+s^2(s-2)(2s-7)\beta^2
\right].
\end{aligned}
}
\tag{3}
\]
For \(s=4\), the combined expression in (3) is interpreted after
cancellation of \(s^{2s-10}=s^{-2}\); its three coefficients are
\(4,16,16\).  Every displayed coefficient is strictly positive for
\(s\geq4\).

Equations (2)--(3) therefore close the two deepest pooled layers.  They do
not prove that every coefficient of every \(B_n\) is nonnegative.

## 2. Fixed-page normalization

Write \(\lambda=1+s\beta\), and let
\[
D_k(s,\beta)=(H_1^{(k)})^2-H_0^{(k)}H_2^{(k)}
\]
be the fixed-\(k\)-page determinant for the three contracted core profiles
\[
(1^s),\qquad(2,1^{s-2}),\qquad(2,2,1^{s-4}).
\]
The inherited nilpotent-page normalization gives the exact polynomial
identity
\[
\boxed{
P_s^{(2)}(\beta,k)=\lambda^{\,2s-2k-4}D_k(s,\beta)
}
\tag{4}
\]
for every integer \(k\geq0\).  When the exponent is negative, (4) means the
exact divisibility supplied by the page-transfer construction; it is not a
formal Laurent-series truncation.

The previous highest-coefficient calculation for the auxiliary kernel
\(K_k\) was stated first in the stable range \(s\geq k+3\).  That statement
cannot simply be extrapolated to the all-depth regime \(k>s\).  The next
lemma instead works directly with the original forest polynomials and is
valid for every \(s\geq4,\ k\geq2\).

## 3. A parameter-uniform high-degree lemma

For profile \(h\in\{0,1,2\}\), let \(W_{h,c}\) be the weight, without its
\(\beta\)-power, of spanning forests having exactly \(c\) connected
components.  If a temporarily labelled component contains \(a\) doubled
core blocks, \(b\) singleton core blocks, and \(j\) page vertices, put
\[
T(a,b,j)=
\begin{cases}
1,&a+b=1,\ j=0,\\
1,&a+b=0,\ j=1,\\
j^{a+b-1}(2a+b)^{j-1}2^a,&a+b\geq1,\ j\geq1,\\
0,&\text{otherwise}.
\end{cases}
\]
The weighted complete-bipartite Matrix--Tree formula and component-set
partitioning give the positive finite sum
\[
W_{h,c}
=\frac1{c!}
\sum_{\substack{\sum_i a_i=h\\
                 \sum_i b_i=s-2h\\
                 \sum_i j_i=k}}
\binom{h}{a_1,\ldots,a_c}
\binom{s-2h}{b_1,\ldots,b_c}
\binom{k}{j_1,\ldots,j_c}
\prod_{i=1}^cT(a_i,b_i,j_i).
\tag{5}
\]
This formula has no stability-range restriction.

Set
\[
L_h=W_{h,1},\qquad
a_h=\frac{W_{h,2}}{W_{h,1}},\qquad
b_h=\frac{W_{h,3}}{W_{h,1}}.
\]
Direct evaluation of (5) for \(c=1,2,3\) gives
\[
L_h=2^h k^{s-h-1}s^{k-1},
\tag{6}
\]
\[
a_h=
\frac{s^2-(k-1)s+(k-1)(k+2)}{sk}
-\frac{h(3s-2k+2)}{2sk},
\tag{7}
\]
and
\[
2b_1-b_0-b_2
=-\frac{
4k^2-12ks-12k+9s^2+12s+8
}{4k^2s^2}.
\tag{8}
\]
In particular, \(a_h\) is affine in \(h\), while
\[
a_1^2-a_0a_2
=\frac{(-2k+3s+2)^2}{4k^2s^2}.
\tag{9}
\]

The largest possible degree in either product defining \(D_k\) is
\(2s+2k-4\).  Equations (5)--(8) show successively that its top two
coefficients cancel:
\[
L_1^2-L_0L_2=0,\qquad
L_1^2(2a_1-a_0-a_2)=0.
\]
At the next degree,
\[
\begin{aligned}
[\beta^{2s+2k-6}]D_k
&=L_1^2
\left(a_1^2-a_0a_2+2b_1-b_0-b_2\right)\\
&=L_1^2\frac{k-1}{k^2s^2}\\
&=\boxed{
4(k-1)k^{2s-6}s^{2k-4}
}>0.
\end{aligned}
\tag{10}
\]
Hence, for every \(s\geq4,\ k\geq2\),
\[
\deg_\beta D_k=2s+2k-6.
\tag{11}
\]

Applying (4), including its exact-divisibility interpretation when needed,
gives the all-parameter fixed-value identity
\[
\boxed{
[\beta^{4s-10}]P_s^{(2)}(\beta,k)
=4s^{2s-8}(k-1)k^{2s-6}.
}
\tag{12}
\]
In particular, \(\deg_\beta P_s^{(2)}(\beta,k)=4s-10\) for every
\(k\geq2\).

## 4. Pooled inversion is a Stirling transform

Newton inversion of
\[
P_s^{(2)}(\beta,t)=\sum_n\binom tnB_n(s,\beta)
\]
gives
\[
B_n(s,\beta)
=\sum_{k=0}^n(-1)^{n-k}\binom nkP_s^{(2)}(\beta,k).
\tag{13}
\]
Put \(m=2s-6\).  Substituting (12) into (13) and extracting the top
\(\beta\)-coefficient,
\[
\begin{aligned}
[\beta^{4s-10}]B_n
&=4s^{2s-8}
\sum_{k=0}^n(-1)^{n-k}\binom nk(k^{m+1}-k^m)\\
&=4s^{2s-8}n!
\left(
\left\{\!\!\begin{matrix}m+1\\n\end{matrix}\!\!\right\}
-
\left\{\!\!\begin{matrix}m\\n\end{matrix}\!\!\right\}
\right),
\end{aligned}
\]
which proves (1).

The Stirling recurrence yields the manifestly positive form
\[
\left\{\!\!\begin{matrix}m+1\\n\end{matrix}\!\!\right\}
-
\left\{\!\!\begin{matrix}m\\n\end{matrix}\!\!\right\}
=(n-1)
\left\{\!\!\begin{matrix}m\\n\end{matrix}\!\!\right\}
+
\left\{\!\!\begin{matrix}m\\n-1\end{matrix}\!\!\right\}.
\tag{14}
\]
For \(2\leq n\leq m+1=2s-5\), the right side is strictly positive.
For \(n>m+1\), it is zero.

## 5. Why the last depth is the entire polynomial

The pooled page-transfer construction supplies a second, independent
support bound.  If the two nilpotent chains use \(j\) and \(q\) active
pages and have overlap \(\ell\), their pooled depth is
\[
n=j+q-\ell.
\]
Every active page performs a genuine merge and therefore contributes at
least two spokes.  Thus every object contributing to \(B_n\) has
\[
\deg_\beta\geq2(j+q)=2(n+\ell)\geq2n.
\tag{15}
\]
On the other hand, (4) and (11)--(12) imply
\[
\deg_\beta B_n\leq4s-10.
\tag{16}
\]

For zero or one page there is no two-page cycle defect, so
\(D_0=D_1=0\).  Equation (4) gives
\[
B_0=P_s^{(2)}(\beta,0)=0,\qquad
B_1=P_s^{(2)}(\beta,1)-P_s^{(2)}(\beta,0)=0.
\tag{17}
\]

If \(n>2s-5\), (15) and (16) are incompatible, so \(B_n=0\).  At
\(n=2s-5\), both bounds equal \(4s-10\), so the layer is a monomial.
Equation (1) and
\[
\left\{\!\!\begin{matrix}2s-5\\2s-5\end{matrix}\!\!\right\}=1,\qquad
\left\{\!\!\begin{matrix}2s-6\\2s-5\end{matrix}\!\!\right\}=0
\]
then prove (2).

## 6. The complete second-deepest layer

It remains to prove (3), because the all-depth top face supplies only its
highest coefficient.  Let \(A_{h,j}\) denote the \(j\)-th nilpotent page
chain from profile \(h\).  Introduce the weighted complete-graph forest
polynomial
\[
\Phi_{\mathbf w}(x)
=\sum_{F\ {\rm forest}}x^{|F|}
\prod_{\{i,j\}\in F}w_iw_j.
\]
Also introduce the one-ternary-edge hyperforest polynomial
\[
\Psi_{\mathbf w}(x)
=x\sum_{\substack{T\subseteq[b]\\|T|=3}}
\left(\prod_{i\in T}w_i\right)
\Phi_{\mathbf w/T}(x),
\tag{18}
\]
where \(\mathbf w/T\) contracts the three weights in \(T\) to their sum.
Write \(\Phi_h,\Psi_h\) for the three profiles.

A degree-\(2j\) chain record consists entirely of binary merges.  Forgetting
their order gives a weighted ordinary forest, and every ordering of its
\(j\) edges is valid.  A degree-\((2j+1)\) record has exactly one ternary
merge; contracting it gives exactly the hyperforest in (18), and again all
\(j!\) orders are valid.  Hence
\[
\boxed{
[\beta^{2j}]A_{h,j}=j![x^j]\Phi_h,\qquad
[\beta^{2j+1}]A_{h,j}=j![x^j]\Psi_h.
}
\tag{19}
\]

Put \(n=2s-6\).  At pooled depth \(n\), a contribution of degree \(2n\) or
\(2n+1\) cannot have an overlap between the two active-page sets.  The
positive binomial linearization multiplier then cancels the two chain
factorials to a common \(n!\).  Moreover,
\[
2s-4-j-q=2
\]
whenever \(j+q=n\), so the linear coefficient of the remaining
\(\lambda^2\) is \(2s\).  Define
\[
C(x)=\Phi_1^2-\Phi_0\Phi_2,
\qquad
Q(x)=2\Phi_1\Psi_1-\Phi_0\Psi_2-\Psi_0\Phi_2.
\]
Equation (19) gives the exact identities
\[
\frac{[\beta^{2n}]B_n}{n!}=[x^n]C(x),
\tag{20}
\]
\[
\frac{[\beta^{2n+1}]B_n}{n!}
=[x^n]\bigl(2sC(x)+Q(x)\bigr).
\tag{21}
\]

For completeness, these two near-spanning coefficients can be evaluated
without Bell states.  If \(\mathbf w=(w_1,\ldots,w_b)\), let
\[
\mathcal F_c(\mathbf w)
=\frac1{c!}
\sum_{\substack{I_1\sqcup\cdots\sqcup I_c=[b]\\I_r\ne\varnothing}}
\prod_{r=1}^c
\left[
\left(\sum_{i\in I_r}w_i\right)^{|I_r|-2}
\prod_{i\in I_r}w_i
\right],
\tag{22}
\]
where a singleton bracket is \(1\).  Weighted Cayley gives
\[
[x^{b-c}]\Phi_{\mathbf w}=\mathcal F_c(\mathbf w).
\]
Similarly, from (18),
\[
[x^{b-c-1}]\Psi_{\mathbf w}
=\sum_{|T|=3}
\left(\prod_{i\in T}w_i\right)
\mathcal F_c(\mathbf w/T).
\tag{23}
\]
To expose the algebra in (25)--(26), put
\[
\mathbf w_h=(\underbrace{2,\ldots,2}_{h},
\underbrace{1,\ldots,1}_{s-2h})
\]
and write
\[
F_{h,c}=\mathcal F_c(\mathbf w_h),\qquad
G_{h,c}=\sum_{|T|=3}
\left(\prod_{i\in T}(\mathbf w_h)_i\right)
\mathcal F_c(\mathbf w_h/T).
\]
The five normalized component sums needed here are:
\[
\begin{array}{c|c|c|c|c|c}
h&
\dfrac{F_{h,1}}{2^hs^{s-h-2}}&
\dfrac{F_{h,2}}{2^hs^{s-h-4}}&
\dfrac{F_{h,3}}{2^hs^{s-h-6}}&
\dfrac{G_{h,1}}{2^hs^{s-h-3}}&
\dfrac{G_{h,2}}{2^hs^{s-h-5}}
\\ \hline
0&
1&
\dfrac{(s-1)(s+6)}2&
\dfrac{(s-2)(s-1)(s^2+13s+60)}8&
\dfrac{(s-2)(s-1)}2&
\dfrac{(s-3)(s-2)(s-1)(3s+20)}{12}
\\[2mm]
1&
1&
\dfrac{(s-2)(s+6)}2&
\dfrac{(s-3)(s-2)(s^2+13s+60)}8&
\dfrac{(s-3)(s-2)}2&
\dfrac{(s-4)(s-3)(s-2)(3s+20)}{12}
\\[2mm]
2&
1&
\dfrac{s^2+3s-20}2&
\dfrac{(s-4)(s^3+10s^2+17s-210)}8&
\dfrac{(s-4)(s-3)}2&
\dfrac{(s-5)(s-4)(3s^2+11s-66)}{12}.
\end{array}
\tag{24}
\]
Each entry follows directly from (22) by choosing the distribution of the
zero, one, or two doubled blocks among the components and applying Abel's
binomial identity.  Thus this table is an exact symbolic evaluation, not
interpolation from fixed \(s\).

Substitution of
\[
(1^s),\qquad(2,1^{s-2}),\qquad(2,2,1^{s-4})
\]
into (22) for \(c\leq3\), and into (23) for \(c\leq2\), gives
\[
\boxed{
[x^{2s-6}]C(x)
=4(s^2+4s-24)s^{2s-10},
}
\tag{25}
\]
\[
\boxed{
[x^{2s-6}]Q(x)
=-8(5s-16)s^{2s-9}.
}
\tag{26}
\]
Equations (22)--(23) are finite positive component-partition sums; (25)--(26)
follow by grouping components according to how many doubled blocks they
contain and applying the binomial theorem.  The verifier evaluates these
sums independently before comparing them with the closed forms.
The complete intermediate substitution, including every product term, is
now recorded in `SECOND_ATTACK.md`, equations (17)--(19), and checked
symbolically by `verify_second_deficit.py`.

Equations (20), (21), (25), and (26) now give
\[
\begin{aligned}
[\beta^{4s-12}]B_{2s-6}
&=4(2s-6)!(s^2+4s-24)s^{2s-10},\\
[\beta^{4s-11}]B_{2s-6}
&=8(2s-6)!(s^2-s-8)s^{2s-9}.
\end{aligned}
\tag{27}
\]
Finally, (1) at \(n=2s-6\) uses
\[
\left\{\!\!\begin{matrix}2s-5\\2s-6\end{matrix}\!\!\right\}
-
\left\{\!\!\begin{matrix}2s-6\\2s-6\end{matrix}\!\!\right\}
=(s-2)(2s-7)
\]
and gives
\[
[\beta^{4s-10}]B_{2s-6}
=4(2s-6)!(s-2)(2s-7)s^{2s-8}.
\tag{28}
\]
The support bounds (15)--(16) allow no other degree.  Combining
(27)--(28) proves (3).

## 7. Scope and remaining gap

What is now proved:

- an exact top-\(\beta\) coefficient for every pooled depth \(n\);
- strict top-face positivity throughout the full unbounded depth range;
- the exact global depth cutoff \(n=2s-5\);
- complete coefficientwise positivity of the two deepest layers.

What remains open:

- coefficientwise positivity of the interior coefficients
  \(2n\leq d<4s-10\) for arbitrary \(s,n\);
- an all-depth positive formula or injection for every \(B_n\);
- the complete \(\alpha^2\) layer of the complete-split family;
- arbitrary-host OPG-1757.

The most economical next target is now \(B_{2s-7}\).  Its support is only
\[
4s-14\leq d\leq4s-10,
\]
so it has at most five coefficients.  The same merge-excess expansion says
that these five coefficients require ordinary forests together with at most
two units of excess: two ternary merges, one quaternary merge, or one
active-page overlap.  This is a sharply bounded second-round problem and a
natural test of whether the method extends to every fixed distance from the
top-depth boundary.
