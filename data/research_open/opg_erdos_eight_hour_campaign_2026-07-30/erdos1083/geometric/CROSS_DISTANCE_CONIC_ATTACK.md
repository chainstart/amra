# Erdős #1083: cross-distance conic attack on the joint mass

Date: 2026-07-30

Status: exact geometric identity, rigorous incidence ledger, and a capacity
barrier.  No unconditional improvement of \(f_3(n)\) is claimed.

## 1. Interface and target

At the plane-reflection/common-axis node of the inherited proof, let
\(\mathcal A\) be the active angles.  The critical parameters are
\[
|\mathcal A|=M\geq n^{1/5-o(1)},\qquad
q_\alpha\geq Q=n^{3/5-o(1)},\qquad
r_\alpha\geq R_0=n^{1-o(1)}
\tag{1}
\]
and the global number of nonzero distances is
\[
D=n^{3/5+o(1)}.
\tag{2}
\]
If the inherited lower bound supplies more active angles, select an
arbitrary subfamily of size \(M=n^{1/5-o(1)}\); all ledgers below refer
to that subfamily.
Here \(q_\alpha\) counts source points in the axial plane of angle
\(\alpha\), while \(r_\alpha\) counts points whose rotation by \(2\alpha\)
also belongs to the configuration.

After removing the \(o(Q),o(R_0)\) contribution from the common axis, the
forced joint mass is
\[
\mathcal J
:=\sum_{\alpha\in\mathcal A}q_\alpha^\circ r_\alpha^\circ
\geq n^{9/5-o(1)}.
\tag{3}
\]
The proposed direct estimate is
\[
\boxed{\mathcal J\leq nD\,n^{o(1)}.}
\tag{target J}
\]
At (2), its right side is \(n^{8/5+o(1)}\), so target J would close this
node with a full \(n^{1/5-o(1)}\) gap.

`CIRCLE_INTERFACE_NO_GO.md` proves that the separate angular capacities
cannot establish target J.  This note spends exactly the omitted
cross-fibre distances.

## 2. Two cross-fibre distances

Take the common axis to be the \(z\)-axis.  A circular fibre is
\[
\mathcal C(\rho,z)
=\{(\rho\cos\theta,\rho\sin\theta,z):\theta\in\mathbb R/2\pi\mathbb Z\}.
\]
Let the source point lie on \(\mathcal C(\rho,z)\) at angle \(\alpha\),
and let a rotation-success pair on \(\mathcal C(\sigma,w)\) have angles
\[
\gamma,\qquad\gamma+2\alpha.
\]
Put
\[
C=(z-w)^2+\rho^2+\sigma^2,\qquad p=2\rho\sigma.
\tag{4}
\]
The two squared cross-fibre distances are
\[
\boxed{
d_-=C-p\cos(\gamma-\alpha),\qquad
d_+=C-p\cos(\gamma+\alpha).
}
\tag{5}
\]
If the source point is the antipodal intersection at \(\alpha+\pi\),
the two cosine terms change sign.  Every squared identity below is
unchanged.

Adding and subtracting (5) gives
\[
2C-d_+-d_-=2p\cos\gamma\cos\alpha,
\tag{6}
\]
\[
d_+-d_-=2p\sin\gamma\sin\alpha.
\tag{7}
\]
Therefore
\[
\boxed{
(2C-d_+-d_-)^2\sin^2\alpha
+(d_+-d_-)^2\cos^2\alpha
=p^2\sin^2(2\alpha).
}
\tag{8}
\]
Thus the proposed conic identity has the stated constants and signs.

The physical parameters obey
\[
C-p=(z-w)^2+(\rho-\sigma)^2\geq0.
\tag{9}
\]

## 3. Quotienting the distance pair

Assume
\[
\sin\alpha\cos\alpha\ne0.
\tag{10}
\]
There are only \(O(1)\) excluded angles modulo \(\pi\), harmless compared
with \(M=n^{1/5-o(1)}\).

Set
\[
u=d_++d_-,\qquad s=(d_+-d_-)^2.
\tag{11}
\]
Equation (8) becomes
\[
\boxed{
s=4p^2\sin^2\alpha
-\tan^2\alpha\,(2C-u)^2.
}
\tag{12}
\]
For fixed \(\alpha\), subtract the common quadratic term by defining
\[
y=s+\tan^2\alpha\,u^2.
\]
Then (12) is the line
\[
\boxed{
y=4C\tan^2\alpha\,u
+4p^2\sin^2\alpha-4C^2\tan^2\alpha.
}
\tag{13}
\]
Because \(p>0\), the map \((C,p)\mapsto\) line (13) is injective.
Consequently the fixed-angle conics form a genuine two-degree-of-freedom
pseudoline family; ordinary Szemerédi--Trotter applies after the exact
change of coordinates.

Let \(\Delta\) be the set of squared distances, adjoining \(0\) if needed.
The incidence point set
\[
\mathcal P_\alpha
=\{(x+y,(x-y)^2+\tan^2\alpha(x+y)^2):x,y\in\Delta\}
\tag{14}
\]
has
\[
|\mathcal P_\alpha|\leq(D+1)^2=O(D^2).
\tag{15}
\]

For fixed \(\alpha,C,p\), the ordered pair \((d_-,d_+)\) determines
\[
\cos\gamma=\frac{2C-d_+-d_-}{2p\cos\alpha},\qquad
\sin\gamma=\frac{d_+-d_-}{2p\sin\alpha}.
\tag{16}
\]
After the quotient \(s=(d_+-d_-)^2\), at most two values of \(\gamma\)
remain.  A source circle has at most two source points in the axial plane.
Hence one line--point incidence represents at most four source/success
flags for a fixed ordered circle pair.

This bounded collision is independently enumerated in the verifier.

## 4. Cross-fibre mass remains critical

Write
\[
a_{\alpha,i}\in\{0,1,2\}
\]
for the number of source points on fibre \(i\), and
\[
b_{\alpha,j}
=|A_j\cap(A_j-2\alpha)|
\]
for the number of rotation-success starting points on fibre \(j\).
Then
\[
q_\alpha^\circ=\sum_i a_{\alpha,i},\qquad
r_\alpha^\circ=\sum_j b_{\alpha,j}.
\]

Every circular fibre contains \(O(D)\) points.  Indeed, from any one
of its \(m\) points, a fixed chord length reaches at most two other
points, so that point alone sees at least \((m-1)/2\) distinct nonzero
distances.
The same-fibre part of \(q_\alpha^\circ r_\alpha^\circ\) is therefore
\[
\sum_i a_{\alpha,i}b_{\alpha,i}=O(q_\alpha^\circ D).
\tag{17}
\]
At the critical parameters, this is \(n^{6/5+o(1)}\), whereas
\[
q_\alpha^\circ r_\alpha^\circ=n^{8/5-o(1)}.
\]
Thus discarding same-fibre flags preserves \(1-o(1)\) of (3).

## 5. Weighted two-degree-of-freedom incidence bound

For one fixed \(\alpha\), dyadically select success fibres satisfying
\[
\lambda\leq b_{\alpha,j}<2\lambda.
\tag{18}
\]
One class carries at least \(r_\alpha^\circ/O(\log D)\) success mass.
Let:

- \(S_\alpha\) be the number of source fibres;
- \(B_\alpha\) be the number of success fibres in this class;
- \(H_\alpha=S_\alpha B_\alpha\) be the number of ordered circle-pair
  line instances;
- \(J_\alpha\asymp H_\alpha\lambda\) be their joint flags;
- \(\mu_\alpha\) be the maximum number of those ordered circle pairs
  with one common parameter \((C,p)\).

The logarithmic loss is absorbed into \(n^{o(1)}\).

### Lemma 1 (weighted line incidence)

Let \(P\) points and a multiset of \(H\) lines be given, with maximum
line multiplicity \(\mu\).  Then
\[
I_{\rm wt}
\ll
P^{2/3}H^{2/3}\mu^{1/3}+\mu P+H
\tag{19}
\]
up to one logarithmic factor.

To prove (19), group distinct lines by weights
\(2^j\leq w<2^{j+1}\).  If the total weight in one group is \(H_j\),
the number of distinct lines is at most \(H_j/2^j\).  Szemerédi--Trotter
gives
\[
I_j\ll
P^{2/3}H_j^{2/3}2^{j/3}+2^jP+H_j.
\]
Sum the groups, use \(2^j\leq\mu\), Hölder on
\(\sum H_j^{2/3}\), and the geometric sum
\(\sum2^j\leq2\mu\).  This proves (19).

By the four-to-one collision bound following (16),
\[
J_\alpha
\ll
D^{4/3}H_\alpha^{2/3}\mu_\alpha^{1/3}
+\mu_\alpha D^2+H_\alpha.
\tag{20}
\]
If \(\lambda\) is larger than an absolute constant, then
\(H_\alpha\asymp J_\alpha/\lambda\), so the last term can be absorbed.
Solving the remaining inequality gives
\[
\boxed{
J_\alpha
\ll n^{o(1)}\mu_\alpha
\left(\frac{D^4}{\lambda^2}+D^2\right).
}
\tag{21}
\]

Equation (21) is the strongest conclusion supplied by the fixed-angle
two-degree-of-freedom incidence route.

## 6. The complete exponent ledger

Assume, on joint-mass-carrying dyadic classes,
\[
\mu_\alpha\leq n^{u+o(1)},\qquad
\lambda_\alpha\geq n^{\ell-o(1)}.
\tag{22}
\]
At the critical scale
\[
D=n^{3/5+o(1)},\qquad M=n^{1/5+o(1)},
\]
summing (21) gives the two exponents
\[
\boxed{
U_{\rm 2d}
=\max\left\{
\frac{13}{5}+u-2\ell,\,
\frac75+u
\right\}.
}
\tag{23}
\]
Compare this with:
\[
\mathcal J_{\rm forced}=n^{9/5-o(1)},\qquad
nD=n^{8/5+o(1)}.
\tag{24}
\]

### 6.1 Fixed-power contradiction at the inherited node

The two-degree route has a fixed-power gap against (3) precisely when
\[
\boxed{
u<\frac25,\qquad
\ell>\frac25+\frac u2.
}
\tag{25}
\]
The saving in the joint-mass exponent is
\[
\eta_{\rm 2d}
=\min\left\{
\frac25-u,\,
2\ell-\frac45-u
\right\}>0.
\tag{26}
\]
This would contradict the critical node by \(n^{\eta_{\rm 2d}-o(1)}\).
Turning that node contradiction into a numerical improvement for \(f_3\)
still requires the inherited argument to be uniform under the perturbed
distance exponent; no such unconditional claim is made here.

### 6.2 Sufficient hypotheses for target J itself

From (21), the exact sufficient inequalities are
\[
M\mu D^2\leq nD\,n^{o(1)},\qquad
\frac{M\mu D^4}{\lambda^2}\leq nD\,n^{o(1)}.
\tag{27}
\]
Equivalently,
\[
\boxed{
\mu\leq\frac{n}{MD}\,n^{o(1)},\qquad
\lambda^2\geq\frac{M\mu D^3}{n}\,n^{-o(1)}.
}
\tag{28}
\]
At the critical exponents, this is
\[
\boxed{
u\leq\frac15,\qquad
\ell\geq\frac12+\frac u2.
}
\tag{29}
\]
Even with collision-free circle-pair parameters (\(\mu=1\)), the method
needs roughly \(n^{1/2}\) successes on every mass-carrying success fibre.

## 7. A global three-degree comparison

If \(\alpha\) is allowed to vary, (12) is a quadratic graph
\[
s=-a u^2+b u+c.
\]
Apart from the \(O(1)\) symmetry \(\tan^2\alpha=\tan^2(\pi-\alpha)\),
these curves have three degrees of freedom.  The standard three-degree
curve-incidence estimate gives the weighted comparison
\[
I_{\rm wt}
\ll
P^{3/5}H^{4/5}\mu^{1/5}+\mu P+H
\tag{30}
\]
up to subpolynomial losses.  Consequently
\[
\mathcal J
\ll n^{o(1)}\mu
\left(\frac{D^6}{\lambda^4}+D^2\right).
\tag{31}
\]
Its critical upper exponent is
\[
\boxed{
U_{\rm 3d}
=\max\left\{
\frac{18}{5}+u-4\ell,\,
\frac65+u
\right\}.
}
\tag{32}
\]
It contradicts the forced \(9/5\) exponent if
\[
u<\frac35,\qquad
\ell>\frac9{20}+\frac u4,
\tag{33}
\]
and proves target J under
\[
u\leq\frac25,\qquad
\ell\geq\frac12+\frac u4.
\tag{34}
\]

The two-degree estimate is better for small parameter multiplicity when
only a contradiction is sought: at \(u=0\), it needs
\(\ell>2/5\), versus \(\ell>9/20\) in (33).  Both formulations need
\(\ell\geq1/2\) to reach target J itself when \(\mu=1\).

Equation (30) is included only as a comparison.  The fixed-angle line
reduction (13) is elementary and is the primary audited route.

## 8. Strict incidence-capacity barrier

The hypotheses inherited from `PROGRESS.md` do not provide any positive
power lower bound for \(\lambda\).  It is consistent with all marginal
capacities that
\[
r_\alpha^\circ
\]
is spread over \(r_\alpha^\circ\) fibres, one success per fibre.  Then
\(\lambda=1\),
\[
H_\alpha\asymp J_\alpha,
\]
and the \(+H_\alpha\) term in (20) equals the quantity to be bounded.
No incidence theorem of this form yields any saving.

The large source count \(q_\alpha\) does not repair this: it creates many
different source--success circle-pair curves, rather than many incidences
on one fixed curve.  When \(b_{\alpha,j}=1\), each of those curves may
still carry only one distance-pair point.

This is not merely an artifact of using a general line theorem.  Fix
\(0<\alpha<\pi/2\), a distance \(d>0\), and the incidence point
\[
(d_-,d_+)=(d,d).
\]
For every
\[
\frac{d}{1+\cos\alpha}
<C<
\frac{d}{1-\cos\alpha},
\]
put
\[
p=\frac{|C-d|}{\cos\alpha}.
\tag{35}
\]
Then \(0<p<C\), and (8) holds at \((d,d)\).  These are physical
circle-pair parameters: take
\[
\rho=\sigma=\sqrt{p/2},\qquad
|z-w|=\sqrt{C-p}.
\tag{36}
\]
Thus arbitrarily many distinct physical \((C,p)\) curves can pass through
one distance-pair point, each contributing one incidence.  This realizes
the unavoidable \(+H\) capacity even when
\[
\mu=1.
\]
For \(C>d\), take \(\gamma=0\); for \(C<d\), take \(\gamma=\pi\).
Equations (5) then realize the two equal squared distances \(d_-=d_+=d\).
It is an incidence-interface construction, not one global \(n\)-point
counterexample with few distances.

Parameter multiplicity is independently uncontrolled as well.  Repeated
radii and repeated height gaps can give many ordered circle pairs with the
same \((C,p)\).  The global distance count \(D\) alone supplies no bound
matching (28).

Hence two independent inputs are missing:

1. **curve richness:** success mass must concentrate on fibres with
   \(b_{\alpha,j}\geq\lambda\);
2. **parameter control:** mass-carrying ordered circle pairs must have
   bounded \((C,p)\)-multiplicity \(\mu\).

The least sufficient tradeoff delivered by this method is (28).  A weaker
tradeoff sufficient only to contradict the critical joint mass is (25).
These hypotheses need hold only after joint-mass weighting on classes that
retain \(n^{9/5-o(1)}\) total mass; imposing them on every active angle is
stronger than necessary.

## 9. What the conic identity does and does not achieve

The identity (8) is useful:

- it injects genuinely cross-fibre distances into target J;
- it reduces each fixed angle to an exact line-incidence problem;
- it identifies the only geometric parameter collision, \((C,p)\);
- it converts any future fibre-richness and parameter-multiplicity theorem
  into an explicit exponent gain through (23).

It does not, by itself, improve \(f_3(n)\).  The source and success
marginals allow \(\lambda=1\), and then the incidence capacity is exactly
the forced joint mass.  Claiming (21) without its richness hypothesis, or
dropping the \(+H\) term, would incorrectly turn a conditional incidence
bound into an unconditional distance theorem.

The minimum next lemma is therefore not another generic incidence estimate.
It is a joint inverse statement showing that under \(D=n^{3/5+o(1)}\),
most of the mass in (3) lies on classes satisfying either (25) or,
for the full target J, (28).

## 10. Verification

Run

```bash
python3 verify_cross_distance_conic.py --trials 2000
pytest -q test_verify_cross_distance_conic.py
```

The verifier:

1. checks (5), (8), and (12) on random radii, heights, angles, and both
   source antipodes;
2. enumerates a \(17\)-angle model and confirms ordered
   \((d_-,d_+)\)-multiplicity one and quotient multiplicity at most two;
3. constructs arbitrarily many distinct physical curves through
   \((d,d)\), verifying the strict \(+H\) barrier;
4. counts exact \((C,p)\)-collisions in a small rational circle family;
5. checks the critical exponent ledger.

The computations audit identities and collision constants.  They are not
used as evidence for an unconditional bound on \(f_3(n)\).
