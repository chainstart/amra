# Independent audit of the cosine--radial repeated-circle barrier

Date: 2026-07-30

Audited file:

- `COSINE_RADIAL_REPEATED_CIRCLE_BARRIER.md`

## 0. Verdict

\[
\boxed{\text{PASS WITH ONE HARMLESS SUBSYSTEM QUALIFICATION}}
\]

The normal form, multiplicity consequences, collinear-distance bound,
and the complete saturation-model distance ledger are correct.
The construction genuinely shows that an arbitrarily large complete
source-circle/target-axis block can determine only linearly many
distances.

The rational-chord and cyclotomic scope conclusions are also correct:
one repeated circle gives only two target rays on each ordinary radius,
and no prime cyclic angular orbit is forced.

There is one wording qualification.  In Section 3.1, the exact identity
\[
 |\mathcal J|=2m
\]
refers to the target subsystem \(T_m\).  The full configuration
\(S_n\cup T_m\) also occupies the source ray \(\alpha\), so its total
number of occupied rays is \(2m+1\).  If the source and target radial
supports are made disjoint as suggested in the manuscript, that extra
ray contributes no radial overlap.  Replacing \(2m\) by \(2m+1\) only
makes the rational-chord lower bound smaller and does not affect the
claimed \(O(1)\) terminal output.

## 1. Audit of the normal form

For a source point \(p=(u,0,z)\) and a target point in axial plane
\(\Pi_{\beta_i}\),
\[
 q_i=(v_i\cos\theta_i,v_i\sin\theta_i,w_i),
 \qquad \theta_i=\beta_i-\alpha,
\]
the reverse circle in the source plane is
\[
 u^2+z^2-2(v_i\cos\theta_i)u-2w_i z
 +v_i^2+w_i^2-d_i=0.
\tag{A1}
\]
Equality of normalized equations is therefore exactly
\[
 v_i\cos\theta_i=A,\qquad
 w_i=w_0,\qquad
 v_i^2-d_i=C.
\tag{A2}
\]
Putting \(y_i=v_i\sin\theta_i\) gives
\[
 q_i=(A,y_i,w_0),\qquad
 v_i^2=A^2+y_i^2,\qquad
 d_i=A^2+y_i^2-C.
\tag{A3}
\]
Completing squares in (A1) gives
\[
 (u-A)^2+(z-w_0)^2=A^2-C.
\tag{A4}
\]
Thus the displayed normal form and, in particular, the claimed
radius-square \(r^2=A^2-C\) are correct.  Since the extracted circle
has an incidence, \(A^2-C\geq0\).  In the nondegenerate saturation
model it is strictly positive.

Because every target is off the common axis, \(v_i\ne0\).  The retained
planes satisfy \(\cos\theta_i\ne0\), hence \(A\ne0\).  For one fixed
\(\beta\), injectivity of \((q,d)\mapsto\Gamma_{\beta,q,d}\) implies
that distinct triples producing the same circle cannot share
\(\beta\).  Therefore all \(\beta_i\)'s are distinct.

Finally,
\[
 \tan\theta_i=\frac{y_i}{A}.
\]
Axial planes are indexed modulo \(\pi\), on which tangent is
injective.  Hence the \(y_i\)'s are pairwise distinct.  All assertions
in the normal-form lemma follow without an unstated orientation
choice; the signed radial coordinate absorbs the opposite ray.

## 2. Audit of the multiplicity consequences

The maps
\[
 y_i^2\longmapsto |v_i|
 =\sqrt{A^2+y_i^2},
\qquad
 y_i^2\longmapsto d_i=A^2-C+y_i^2
\tag{A5}
\]
are injective.  Since one square has at most the two real preimages
\(y,-y\),
\[
 |\{|v_i|\}|=|\{d_i\}|=|\{y_i^2\}|
 \geq\left\lceil\frac{\mu}{2}\right\rceil.
\tag{A6}
\]
Consequently
\[
 \mu\leq2|\mathcal D_0|.
\tag{A7}
\]
There are \(\mu\) distinct target planes, all different from the
source plane, so
\[
 \mu\leq|\mathcal A|-1.
\tag{A8}
\]

The target points all lie on the line
\[
 \{(A,y,w_0):y\in\mathbb R\}.
\]
Order their pairwise distinct transverse coordinates
\(y_1<\cdots<y_\mu\).  The \(\mu-1\) squared distances
\[
 |q_j-q_1|^2=(y_j-y_1)^2,\qquad 2\leq j\leq\mu,
\tag{A9}
\]
are strictly increasing.  Thus the target set determines at least
\(\mu-1\) nonzero distinct squared distances.  This proves the
collinear-distance claim with no genericity assumption.

If \(p=(u,0,z)\) is incident to the common circle, then (A3)--(A4)
give
\[
 |p-q_i|^2
 =(u-A)^2+(z-w_0)^2+y_i^2
 =A^2-C+y_i^2=d_i.
\tag{A10}
\]
Therefore all \(s\mu\) edges of the asserted complete bipartite block
really use only the labels \(\{d_i\}\).

## 3. Audit of the saturation model

The source set is a regular \(n\)-gon on the circle of radius \(r\)
with centre \((a,0,0)\) in the source plane.  The assumption \(a>r\)
makes every source point off the common \(z\)-axis.  The target set is
the symmetric odd arithmetic progression
\[
 (a,hj,0),\qquad
 j\in\{\pm1,\pm3,\ldots,\pm(2m-1)\}.
\]
Its \(2m\) slopes \(hj/a\), and hence its \(2m\) axial planes, are
distinct.

For every source point \(p\in S_n\) and target \(q_j\in T_m\),
\[
 |p-q_j|^2=r^2+h^2j^2.
\tag{A11}
\]
Thus the \(2m\) target triples yield one common source circle, while
the cross-distance labels depend only on \(j^2\).  There are exactly
\(m\) such values.  This attains
\[
 \mu=2m,\qquad
 |\{|v_j|\}|=|\{d_j\}|=m=\mu/2.
\tag{A12}
\]

The full nonzero squared-distance ledger is:

\[
\begin{array}{c|c|c}
\text{pair type}&\text{values}&\text{number}\\ \hline
S_n-S_n&
2r^2\bigl(1-\cos(2\pi\ell/n)\bigr),
1\leq\ell\leq\lfloor n/2\rfloor&
\lfloor n/2\rfloor\\
T_m-T_m&
4h^2s^2,\quad1\leq s\leq2m-1&
2m-1\\
S_n-T_m&
r^2+h^2(2j-1)^2,\quad1\leq j\leq m&
m.
\end{array}
\tag{A13}
\]

Within each row the listed values are distinct.  Values from different
rows may coincide, which can only reduce the union.  Hence
\[
 |\Delta^2(S_n\cup T_m)|
 \leq\lfloor n/2\rfloor+(2m-1)+m
 =\lfloor n/2\rfloor+3m-1.
\tag{A14}
\]
This checks all source--source, target--target, and cross distances.
The target arithmetic progression has exactly \(2m-1=\mu-1\)
distance values, so the collinear lower bound is simultaneously sharp.

## 4. Scope of the arithmetic terminals

### Rational-chord theorem

On the target subsystem, every ordinary radius
\[
 \sqrt{a^2+h^2j^2}
\]
supports exactly the two rays indexed by \(j\) and \(-j\), with one
height on each ray.  Therefore its ordered overlap contribution is
two, and
\[
 \Omega_{\rm cyl}=2m.
\]
There are \(2m\) target rays.  With rational \(a,h\), the only
same-radius horizontal chord is \(2h|j|\), so a common scale makes the
chords integral and the anchored chord multiplicity is \(K=1\).
The weighted rational-chord theorem consequently gives only
\[
 \frac{2m}{(2m)L_U T_2}=t^{o(1)}
\]
at best.

For the full configuration there is one additional source ray.
Choosing \(h\) as in the manuscript makes the target radii disjoint
from all source radii, so this ray adds neither overlap nor a useful
edge.  The denominator becomes \(2m+1\), leaving the conclusion
unchanged.

### Partial cyclotomic theorem

The relation \(v_i\cos(\beta_i-\alpha)=A\) permits arbitrary distinct
real transverse coordinates \(y_i=A\tan(\beta_i-\alpha)\).  It does
not imply a prime cyclic orbit or any cyclotomic field condition, so
the partial-fibre theorem is not automatically applicable.

Even after imposing such extra conditions, one target radius has two
angles and one occupied height.  Its angle difference set has at most
one nonzero sign class, so the partial-fibre lower bound contributes
at most one label per radius, hence \(O(\mu)\) in total.  The
saturation model already has \(\mu/2\) cross labels and \(O(\mu)\)
total target distances.  Thus no polynomial amplification follows
from the existing cyclotomic terminal.

## 5. Final assessment

All substantive claims in the barrier pass.  The construction is a
valid Euclidean sharp family for everything inferable from a single
repeated reverse circle:

- \(\mu\) distinct target planes;
- only \(\lceil\mu/2\rceil\) radii and labels;
- only \(\mu-1\) target distances;
- \(n\mu\) cross incidences but \(O(n+\mu)\) total distances.

The manuscript correctly limits its no-go to the repeated-circle
chart and the currently available rational/cyclotomic terminals.  It
does not claim that additional information from many incompatible
repeated circles, rotation energy, or the full Euclidean point set
could never produce expansion.
