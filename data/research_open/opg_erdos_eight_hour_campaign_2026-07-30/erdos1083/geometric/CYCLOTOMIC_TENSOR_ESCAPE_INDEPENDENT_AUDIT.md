# Independent red-team audit of cyclotomic tensor escape

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

Theorem 1 of `CYCLOTOMIC_TENSOR_ESCAPE_THEOREM.md` is correct as
stated.  The proof has been independently reconstructed at both the
full cyclotomic and maximal-real-subfield levels.  In particular:

1. the relation space among \(1,\zeta,\ldots,\zeta^{p-1}\) over
   \(\mathbb Q\) is exactly the span of
   \(1+X+\cdots+X^{p-1}\);
2. the relation used in the proof has support at most five, hence
   strictly less than \(p\) for \(p\ge7\);
3. the exponent pairs belonging to distinct
   \(d,e\in[1,(p-1)/2]\) are disjoint;
4. after \(r=s\), both heights belong to the same
   radius-dependent set \(\mathcal Z_r\); the deductions
   \(r^2=s^2\Rightarrow r=s\) and
   \((u-z_r^-)^2=(v-z_r^-)^2\Rightarrow u=v\) use exactly positivity
   of the radii and minimality of the common anchor \(z_r^-\); and
5. every indexed value is a genuine nonzero squared distance, so
   injectivity supplies exactly
   \((p-1)\sum_r|\mathcal Z_r|/2\) distinct labels.

No unconditional conclusion beyond the stacked polygon-fibre family is
created by the theorem.

The field-extension sentence in Section 3 can be strengthened.  The
clean field-theoretic condition is not irreducibility of the full
\(\Phi_p\) over \(F\), but linear disjointness from the maximal real
cyclotomic field:
\[
\boxed{
F\cap\mathbb Q(\zeta_p+\zeta_p^{-1})=\mathbb Q.
}
\tag{1}
\]
Under (1), the same theorem holds when every squared radius and every
radius-dependent anchored squared height difference belongs to \(F\).
This extension and its sharp failure mode are proved below.

## 1. Audit of the unique-relation step

Let
\[
\zeta=e^{2\pi i/p}.
\]
Suppose
\[
\sum_{j=0}^{p-1}q_j\zeta^j=0,
\qquad q_j\in\mathbb Q.
\tag{2}
\]
Then the polynomial
\[
Q(X)=\sum_{j=0}^{p-1}q_jX^j
\]
has degree at most \(p-1\) and vanishes at \(\zeta\).  Since the
minimal polynomial is
\[
\Phi_p(X)=1+X+\cdots+X^{p-1}
\]
of degree \(p-1\), either \(Q=0\), or
\[
Q=c\Phi_p
\]
for some \(c\in\mathbb Q\).  Thus every coefficient \(q_j\) is the
same.  This proves that the only rational relation is the all-ones
relation.

The equality of two selected squared distances gives
\[
\begin{aligned}
0={}&
\left(
2r^2-2s^2
+(u-z_r^-)^2-(v-z_s^-)^2
\right)\\
&-r^2(\zeta^d+\zeta^{p-d})
+s^2(\zeta^e+\zeta^{p-e}).
\end{aligned}
\tag{3}
\]
All coefficients are rational under the theorem's hypotheses.  Its
support lies in
\[
\{0,d,p-d,e,p-e\},
\tag{4}
\]
which has cardinality at most five.  Since \(p\ge7\), a nonzero
multiple of the all-ones relation cannot have this support.  Therefore
every coefficient in (3) is zero.

This argument is unaffected when some displayed exponents coincide:
coincidence only decreases the support.

The audit found one harmless editorial defect: immediately after
equation (10), “Relation (8) is supported” needed to read
“Relation (9) is supported.”  The author has now corrected this
cross-reference.  No mathematical step was affected.

## 2. Audit of the \(d/e\) exponent pairs

For
\[
1\le d,e\le\frac{p-1}{2},
\]
the equality of unordered pairs
\[
\{d,p-d\}=\{e,p-e\}
\tag{5}
\]
forces \(d=e\).  Indeed, \(d=p-e\) is impossible because
\[
d\le\frac{p-1}{2}<\frac{p+1}{2}\le p-e.
\]
Consequently, if \(d\ne e\), the coefficient of \(\zeta^d\) in (3)
is exactly \(-r^2\), which is nonzero.  This contradicts the conclusion
of Section 1, so
\[
d=e.
\tag{6}
\]

With \(d=e\), the coefficient of \(\zeta^d\) is
\[
-r^2+s^2.
\]
It vanishes only when \(r^2=s^2\).  Both radii are assumed positive,
not merely nonzero, so
\[
r=s.
\tag{7}
\]
This equality also makes the two radius-dependent anchors equal:
\(z_r^-=z_s^-\).  The remaining constant coefficient gives
\[
(u-z_r^-)^2=(v-z_r^-)^2.
\]
Because \(u,v\in\mathcal Z_r\) and
\(z_r^-=\min\mathcal Z_r\), both differences are nonnegative.
Equality of their squares therefore gives equality of the differences
and hence
\[
u=v.
\tag{8}
\]
All three coordinates of the indexing triple are therefore equal.

The assumptions used at this last stage are precise:

* positivity of radii rules out \(r=-s\);
* tying \(\mathcal Z_r\) to its radius makes the anchors identical
  after \(r=s\);
* minimality of \(z_r^-\) rules out the negative-square-root branch.

No ordering of the other heights, common height count, common
progression, or common anchor across different radii is used.

## 3. Audit of the distance count

For every
\[
(r,d,u)\in
\mathcal R\times
\{1,\ldots,(p-1)/2\}\times\mathcal Z_r,
\]
choose the two points
\[
\left(r,0,z_r^-\right)
\quad\text{and}\quad
\left(
r\cos\frac{2\pi d}{p},
r\sin\frac{2\pi d}{p},
u
\right)
\]
after the harmless common horizontal rotation implicit in (1).
Both belong to the stacked fibre set, and their squared distance is
\[
r^2a_d+(u-z_r^-)^2.
\tag{9}
\]
It is positive because
\[
a_d=4\sin^2(\pi d/p)>0.
\]

The injectivity proved above therefore embeds a set of cardinality
\[
\frac{p-1}{2}\sum_{r\in\mathcal R}|\mathcal Z_r|
\tag{10}
\]
into the nonzero squared-distance set.  Since
\[
N=p\sum_{r\in\mathcal R}|\mathcal Z_r|,
\]
equation (10) is exactly
\[
\frac{p-1}{2p}N.
\]
No uncounted orientation multiplicity, zero-distance label, or
square-root ambiguity enters this lower bound.

## 4. Independent finite verification method

The independent verifier does not use the author's quotient by the
all-ones relation among the \(p\) powers of \(\zeta\).  Instead it
works in the maximal real field
\[
K_p^+=\mathbb Q(\zeta+\zeta^{-1})
\]
with
\[
b_d=\zeta^d+\zeta^{-d},
\qquad
1\le d\le m=\frac{p-1}{2}.
\]
The \(m+1\) elements
\[
1,b_1,\ldots,b_m
\]
have the unique relation
\[
1+b_1+\cdots+b_m=0.
\tag{11}
\]
Thus
\[
1,b_1,\ldots,b_{m-1}
\]
are a rational basis.  A selected label is represented canonically by
\[
w+r^2(2-b_d),
\qquad
w=(u-z_r^-)^2\in\mathbb Q_{\ge0}.
\tag{12}
\]
For \(d<m\), its coefficient vector in this basis has constant
\(w+2r^2\), coefficient \(-r^2\) in slot \(d\), and zero
elsewhere.  For \(d=m\), equation (11) gives constant
\(w+3r^2\) and coefficient \(r^2\) in every nonconstant
slot.

Exact rational tuples built from these vectors verify injectivity
without sharing the author's representation or implementation.  The
test data use unequal cardinalities, negative and irrational anchors,
and non-arithmetic gaps at different radii.

## 5. Base-field extension

Let \(F\subset\mathbb C\) be a number field in a chosen embedding, and
put
\[
K_p^+=\mathbb Q(\zeta_p+\zeta_p^{-1}),
\qquad
m=[K_p^+:\mathbb Q]=\frac{p-1}{2}.
\tag{13}
\]

### Theorem 2 (exact base-field extension)

The weakest coefficient-independent hypothesis needed by this proof is
\[
\boxed{
1,b_d,b_e\ \text{are linearly independent over }F
\quad\text{for every }d\ne e.
}
\tag{14a}
\]
For \(p\ge7\), this also implies independence of every pair
\(1,b_d\).  Condition (14) below is a clean field-theoretic sufficient
condition for (14a).

Assume
\[
F\cap K_p^+=\mathbb Q,
\tag{14}
\]
and replace the rationality hypotheses in Theorem 1 by
\[
r^2\in F\cap\mathbb R_{>0}\quad(r\in\mathcal R),
\qquad
(z-z_r^-)^2\in F\cap\mathbb R_{\ge0}
\quad(z\in\mathcal Z_r).
\tag{15}
\]
Then
\[
\boxed{
|\Delta^2(P)|
\ge\frac{p-1}{2}\sum_r|\mathcal Z_r|.
}
\tag{16}
\]

#### Proof

The extension \(K_p^+/\mathbb Q\) is Galois.  Hence (14) is equivalent
to linear disjointness of \(F\) and \(K_p^+\) over \(\mathbb Q\).
The rational basis
\[
1,b_1,\ldots,b_{m-1}
\]
therefore remains linearly independent over \(F\).  Equivalently,
(11) remains the unique \(F\)-linear relation among
\(1,b_1,\ldots,b_m\).

Equality of two labels gives the \(F\)-linear relation
\[
\left(
2r^2-2s^2
+(u-z_r^-)^2-(v-z_s^-)^2
\right)
-r^2b_d+s^2b_e=0.
\tag{17}
\]
It is supported on at most three of the \(m+1\) characters.  Since
\(p\ge7\), one has \(m+1\ge4\), so it cannot be a nonzero multiple of
the full-support relation (11).  Repeating (6)--(8) proves injectivity
and hence (16).
\(\square\)

This is strictly sharper than requiring \(\Phi_p\) to remain
irreducible over \(F\).  For example, when \(p\equiv3\pmod4\), the
imaginary quadratic subfield of \(\mathbb Q(\zeta_p)\) meets
\(K_p^+\) only in \(\mathbb Q\).  Taking it as \(F\) makes
\(\Phi_p\) reducible over \(F\), while Theorem 2 still applies to
rational squared radii and rational anchored height squares.  Only the
real chord field is relevant.

## 6. Conditions in terms of \([F:\mathbb Q]\) and \(p\)

Let
\[
n=[F:\mathbb Q].
\]
The intersection degree
\[
q=[F\cap K_p^+:\mathbb Q]
\tag{18}
\]
divides both \(n\) and \(m=(p-1)/2\).  Consequently,
\[
\boxed{
\gcd\left(n,\frac{p-1}{2}\right)=1
\quad\Longrightarrow\quad
F\cap K_p^+=\mathbb Q.
}
\tag{19}
\]
This is a degree-only sufficient condition.

There is also a stronger fixed-field statement.  The prime \(p\) is
totally ramified in \(K_p^+\), and it remains ramified in every
nontrivial intermediate field.  Therefore
\[
\boxed{
p\nmid\operatorname{Disc}(F)
\quad\Longrightarrow\quad
F\cap K_p^+=\mathbb Q.
}
\tag{20}
\]
For any fixed \(F\), Theorem 2 thus applies to every prime \(p\ge7\)
outside the finite set of rational primes ramified in \(F\), regardless
of the common divisors of \(n\) and \((p-1)/2\).

There is no necessary-and-sufficient condition involving only the two
integers \(n\) and \(p\).  Fields of the same degree may either meet or
avoid \(K_p^+\).  The intersection statement (14) is exactly the
condition preserving the unique full family relation (11), and is a
uniform sufficient condition for injectivity.  It is not asserted to be
necessary: the three-character condition (14a) may survive some
nontrivial intersections.

The quantitative loss when (14) fails is visible in the relation
space.  With \(q\) as in (18),
\[
[FK_p^+:F]=\frac{m}{q}.
\]
Since the \(m+1\) characters span the compositum over \(F\), their
\(F\)-linear relation space has dimension
\[
\boxed{
m+1-\frac{m}{q}.
}
\tag{21}
\]
It is one-dimensional exactly when \(q=1\).  Degree information alone
does not control whether the additional relations are sparse enough to
collide the three terms in (17).

## 7. Sharp failure boundary

The disjointness condition cannot simply be deleted.  Take
\[
F=K_p^+
\]
and choose distinct \(d,e\in[1,m]\).  Since every \(a_j\) is positive,
put
\[
r^2=a_e,\qquad s^2=a_d.
\tag{22}
\]
Both squared radii lie in \(F\).  They are distinct because
\(a_j=4\sin^2(\pi j/p)\) is strictly increasing for
\(1\le j\le m\), so \(r\ne s\).  Nevertheless,
\[
\boxed{
r^2a_d=a_ea_d=a_da_e=s^2a_e.
}
\tag{23}
\]
Thus the two distinct triples
\[
(r,d,z_r^-)\ne(s,e,z_s^-)
\]
give the same selected squared distance.

More generally, take
\[
\mathcal R=\{\sqrt{a_j}:1\le j\le m\},
\qquad
\mathcal Z_{\sqrt{a_j}}=\{0\}.
\]
The \(m^2\) selected labels
\[
a_ja_d
\]
are symmetric in \(j,d\), so there are at most
\[
\frac{m(m+1)}2
\tag{24}
\]
of them.  The injective subsystem used in Theorem 1 loses an asymptotic
factor two.

This is a counterexample to base-field injectivity, not a counterexample
to the total-distance lower bound: cross-radius point pairs may create
additional labels.  It marks the exact boundary of the present proof
mechanism without overstating a Euclidean counterexample.

## 8. Claim status

### Proved

* Theorem 1 in the audited note, with every quantifier checked;
* the sharper base-field Theorem 2 under (14);
* sufficient conditions (19)--(20);
* the exact relation-space dimension (21);
* the collision family (22)--(24) when the field contains the real
  cyclotomic coefficient field.

### Not proved

* the same injectivity for every field with nontrivial intersection;
* failure of the total-distance lower bound when (14) fails;
* extraction of the stacked polygon fibres from a general critical
  configuration;
* an unconditional improvement for Erdős #1083.

## 9. Verification

Run:

```bash
pytest -q test_independent_verify_cyclotomic_tensor_escape.py
python3 independent_verify_cyclotomic_tensor_escape.py
```

The independent implementation imports nothing from
`verify_cyclotomic_tensor_escape.py`.
