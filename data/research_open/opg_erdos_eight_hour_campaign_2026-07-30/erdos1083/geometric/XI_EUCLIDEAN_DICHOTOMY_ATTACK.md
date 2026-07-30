# Xi–parameter energy attack for genuine cross-fibre distances

Date: 2026-07-30

## 1. Outcome

The sparse same-radius statistic
\[
\Xi(E,A):=\frac{I^2}{2I+\lambda(A)J^2}
\]
can be joined rigorously to the all-pairs affine-line parameter count
\[
M=\left|\{(A_{ij},B_{ij})\}\right|,
\qquad
A_{ij}=(\rho_i-\rho_j)^2+(z_i-z_j)^2,\quad
B_{ij}=2\rho_i\rho_j.
\]
The resulting theorem gives a useful inverse statement, with complete
exponent optimization.  It also proves that the proposed
radius-concentration / parameter-energy / Xi trichotomy is not closed as
stated: a fourth, independent **angular-column starvation** branch is
necessary.

On the critical anisotropic grid:

* with the full \(J=N^{2/5}\) synchronized angular pattern, Xi is
  \(N^{4/5-o(1)}\), so the grid is decisively eliminated;
* with only the \(J=N^{1/5}\) inherited/source angular columns, Xi is
  exactly \(N^{3/5-o(1)}\), while the parameter-line route gives only
  \(N^{1/2+o(1)}\).

Thus the sparse critical grid is an equality obstruction to this proof
interface.  The equality occurs in the **incidence-mass/column-starvation
branch**, not in the height-overlap branch: its \(\lambda(A)\) is small.
This is an interface counterexample, not a counterexample to the Erdős
distance statement itself.

## 2. A coherent Euclidean certificate

Consider \(F\) distinct coaxial circles
\[
C_i=(\rho_i,z_i),\qquad 1\le i\le F.
\]
Assume first that a set of \(J\) angular columns, including the reference
column \(0\), is present on every circle.  Put
\[
X=\{1-\cos\beta:\beta\in B\}.
\]
The cosine symmetry gives \(|X|\ge J/2\), which changes only absolute
constants below.
For every unordered circle pair \(i\le j\), the genuine squared-distance
formula is
\[
\boxed{
d^2=A_{ij}+B_{ij}x,\qquad x\in X,
}
\tag{1}
\]
where
\[
A_{ij}=(\rho_i-\rho_j)^2+(z_i-z_j)^2,\qquad
B_{ij}=2\rho_i\rho_j.
\tag{2}
\]
Repeated circle pairs can give the same parameter pair.  Let
\[
\mu(a,b)=|\{i\le j:(A_{ij},B_{ij})=(a,b)\}|,
\]
\[
P=\sum_{a,b}\mu(a,b)=\binom{F+1}{2},\qquad
\mathcal E_{\rm par}=\sum_{a,b}\mu(a,b)^2,\qquad
M=|\operatorname{supp}\mu|.
\tag{3}
\]
The same discussion applies to a selected coherent family of \(P\)
circle pairs, provided every selected pair supports the same \(J\)
chord inputs.

Independently, fix an anchor on one radius class and let
\[
E\subseteq\{1,\ldots,m\}\times B,\qquad |E|=I,
\]
be its height–angle incidences.  With
\[
a_r=(z_r-z_0)^2,\qquad
A=\{a_1,\ldots,a_m\},\qquad
\lambda(A)=\max_{t\ne0}|A\cap(A+t)|,
\tag{4}
\]
the sparse theorem gives
\[
D+1\ge \Xi(E,A)
:=\frac{I^2}{2I+\lambda(A)J^2}.
\tag{5}
\]
In the fully coherent rectangle on that radius class, \(I=mJ\).

## 3. The joined theorem

### Theorem 1 (Xi–parameter union bound)

For every coherent certificate above,
\[
\boxed{
D+1\gg
\max\left\{
\frac{I^2}{2I+\lambda(A)J^2},
\ \min\{M,\sqrt{JM}\}
\right\}.
}
\tag{6}
\]
Moreover,
\[
M\ge \frac{P^2}{\mathcal E_{\rm par}},
\tag{7}
\]
and hence
\[
\boxed{
D+1\gg
\max\left\{
\Xi(E,A),
\ \min\left\{
\frac{P^2}{\mathcal E_{\rm par}},
\frac{\sqrt J\,P}{\sqrt{\mathcal E_{\rm par}}}
\right\}
\right\}.
}
\tag{8}
\]

### Proof

Equation (5) is `SPARSE_ANGLE_INCIDENCE_EXPANSION.md`, applied to
distances from the fixed anchor.  For the second term, retain one graph
line
\[
y=a+bx
\]
for every distinct pair \((a,b)\) in (2), and the \(J\) points on that
line supplied by (1).  The standard Szemerédi--Trotter incidence bound
gives
\[
D+1\gg\min\{M,\sqrt{JM}\}.
\]
Both sets consist of genuine squared distances of the original
configuration, so their maximum is a valid lower bound.  Finally,
Cauchy--Schwarz in (3) gives
\[
P^2=\left(\sum_{a,b}\mu(a,b)\right)^2
\le M\sum_{a,b}\mu(a,b)^2
=M\mathcal E_{\rm par}.
\]
This proves (7) and (8). \(\square\)

The theorem does not assume that the two lower-bound sets are disjoint.
It therefore loses no validity through an unjustified addition of
same-radius and cross-radius distances.

## 4. Exact target inverse theorem

Let \(T\ge1\) be a desired distance threshold and define
\[
H(T,J):=\max\left\{T,\frac{T^2}{J}\right\}.
\tag{9}
\]
If
\[
M\gg H(T,J),
\]
then both \(M\gg T\) and \(\sqrt{JM}\gg T\), so the parameter term in
(6) reaches \(T\).  By (7), the sufficient low-energy condition is
\[
\boxed{
\mathcal E_{\rm par}\ll\frac{P^2}{H(T,J)}.
}
\tag{10}
\]

For Xi, if \(\Xi<T\), then exactly
\[
\lambda(A)>
\frac{I^2/T-2I}{J^2}.
\tag{11}
\]
In particular, if \(I\ge4T\), then
\[
\boxed{
\lambda(A)>\frac{I^2}{2TJ^2}.
}
\tag{12}
\]

### Corollary 2 (the honest four-way alternative)

Up to the absolute constants in Szemerédi--Trotter, at least one of the
following holds:

1. **Xi expansion:** \(\Xi(E,A)\gg T\);
2. **low parameter energy:**
   \(\mathcal E_{\rm par}\ll P^2/H(T,J)\), and the parameter lines give
   \(D\gg T\);
3. **angular-column/incidence starvation:** \(I<4T\);
4. **double high energy:** simultaneously
   \[
   \mathcal E_{\rm par}\gg\frac{P^2}{H(T,J)}
   \quad\text{and}\quad
   \lambda(A)\gg\frac{I^2}{TJ^2}.
   \tag{13}
   \]

Indeed, if neither successful branch 1 nor 2 holds and \(I\ge4T\),
(10)--(12) force branch 4.  Otherwise branch 3 holds.

This exposes the logical defect in the desired three-way formulation.
Small Xi does not imply high height energy unless \(I\) is already
larger than the target.  It can instead be caused solely by too few
reused angular incidences.

## 5. Complete exponent optimization

Write, suppressing \(N^{o(1)}\) factors,
\[
I=N^i,\quad J=N^j,\quad\lambda=N^\ell,\quad
P=N^p,\quad\mathcal E_{\rm par}=N^e.
\tag{14}
\]
Then the two exponents in (8) are
\[
\boxed{
x_\Xi
=2i-\max\{i,\ell+2j\}
=\min\{i,\,2i-\ell-2j\},
}
\tag{15}
\]
\[
\boxed{
m_{\rm par}=2p-e,\qquad
x_{\rm par}
=\min\left\{m_{\rm par},
\frac{j+m_{\rm par}}2\right\}.
}
\tag{16}
\]
Consequently the joined certificate proves
\[
D\ge N^{\,\max\{x_\Xi,x_{\rm par}\}-o(1)}.
\tag{17}
\]

For a target
\[
d=\frac35+\varepsilon,
\]
Xi succeeds precisely at exponent level when
\[
i>d,\qquad 2i-\ell-2j>d.
\tag{18}
\]
The parameter route succeeds when
\[
2p-e>d,\qquad j+2p-e>2d,
\tag{19}
\]
or equivalently
\[
\boxed{
e<
\min\{2p-d,\ 2p+j-2d\}.
}
\tag{20}
\]

For a complete \(m\times J\) same-radius rectangle, writing
\(m=N^\mu\), one has \(i=\mu+j\) and therefore
\[
\boxed{
x_\Xi=\min\{\mu+j,\ 2\mu-\ell\}.
}
\tag{21}
\]
This formula separates the two Xi bottlenecks:

* \(\mu+j\) is the total-incidence or angular-column cap;
* \(2\mu-\ell\) is the height-overlap cap.

No estimate on \(\lambda\) can overcome the first cap.

## 6. Critical anisotropic grid: exact equality diagnosis

Use the construction of
`CRITICAL_ANISOTROPIC_GRID_BARRIER.md`:
\[
L=t,\qquad m=t^2,\qquad F=Lm=t^3,\qquad N=t^5,
\tag{22}
\]
with radii \(\rho_u=mq^u\) and common heights
\(\{0,\ldots,m-1\}\).  It has
\[
M=m\binom{L+1}{2}=\Theta(t^4)=N^{4/5+o(1)},
\tag{23}
\]
\[
\mathcal E_{\rm par}=\Theta(t^8)=N^{8/5+o(1)},\qquad
P=\Theta(F^2)=N^{6/5+o(1)}.
\tag{24}
\]
For the anchored square-height set
\[
A=\{0^2,1^2,\ldots,(m-1)^2\},
\]
the equation \(b^2-a^2=h\) factors as
\((b-a)(b+a)=h\), so
\[
\lambda(A)\le \max_{h\le m^2}\tau(h)=m^{o(1)}.
\tag{25}
\]
Thus \(\ell=0\) at exponent resolution.

### 6.1 Only the inherited \(J=t=N^{1/5}\) columns

Here
\[
j=\frac15,\qquad
\mu=\frac25,\qquad
i=\mu+j=\frac35.
\]
Equations (15)--(16) give
\[
x_\Xi
=\min\left\{\frac35,\frac45\right\}
=\frac35,
\tag{26}
\]
\[
m_{\rm par}=\frac45,\qquad
x_{\rm par}
=\min\left\{\frac45,\frac{1/5+4/5}{2}\right\}
=\frac12.
\tag{27}
\]
Hence
\[
\max\{x_\Xi,x_{\rm par}\}=\frac35.
\tag{28}
\]
For every fixed \(\varepsilon>0\), this certificate cannot prove
\(N^{3/5+\varepsilon}\).

The parameter-energy target from (20) is
\[
e<\frac75-2\varepsilon,
\tag{29}
\]
whereas the grid has \(e=8/5\).  Xi fails for the simpler reason
\[
I=mJ=t^3=N^{3/5}.
\tag{30}
\]
This is branch 3 of Corollary 2 at equality.  It is **not** caused by
large \(\lambda\), since (25) is subpolynomial.

The equality can be realized at the actual one-radius distance-union
level.  Choose \(J\) angles so that
\[
2\rho^2(1-\cos\beta_k)=k,\qquad 0\le k<J;
\tag{31}
\]
these exist and are distinct when \(J-1\le4\rho^2\).  The anchored
squared distances are then
\[
\{d^2+k:0\le d<m,\ 0\le k<J\}.
\tag{32}
\]
For \(J\le m\), this set has size \(\Theta(mJ)\): the upper bound is
trivial, while the intervals
\([d^2,d^2+J-1]\) are disjoint once \(2d-1\ge J\).  At
\(m=t^2,J=t\), (32) therefore has \(\Theta(t^3)\) values.  Thus no
stronger conclusion can be extracted from \(m,J,\lambda\) alone.

This construction only saturates the selected same-radius/interface
data.  Other cross-radius distances may be numerous, so it is not an
\(f_3(N)\) counterexample.

### 6.2 The full \(J=t^2=N^{2/5}\) angular pattern

Now
\[
j=\frac25,\qquad i=\frac45.
\]
The exponents become
\[
x_\Xi=\frac45,\qquad x_{\rm par}=\frac35.
\tag{33}
\]
Therefore the full critical grid is killed by Xi:
\[
D\ge N^{4/5-o(1)}
\]
inside the repeated-radius slice.  The all-pairs parameter route still
lands exactly at \(N^{3/5}\), since
\[
\sqrt{JM}=\sqrt{t^2t^4}=t^3.
\]
The energy threshold is
\[
e<\frac85-2\varepsilon;
\tag{34}
\]
the grid has equality at \(\varepsilon=0\), but Xi supplies the gain.

## 7. What remains to prove

The attack converts the vague critical obstruction into one quantitative
task.  At the critical radius multiplicity \(m=N^{2/5+o(1)}\), one must
show that some repeated-radius class reuses
\[
J>N^{1/5+\delta}
\tag{35}
\]
angular columns, or more generally has
\[
I>N^{3/5+\delta},
\tag{36}
\]
while keeping the second Xi cap in (15) above the target.  With
\(\lambda=N^{o(1)}\), any fixed \(\delta>0\) in (35) gives the distance
gain \(N^{3/5+\delta-o(1)}\) until the height cap \(N^{4/5-o(1)}\) is
reached.

Alternatively, the cross-fibre route must improve the critical
parameter energy from
\[
\mathcal E_{\rm par}=N^{8/5+o(1)}
\]
to the threshold in (20).  For only \(J=N^{1/5}\) coherent columns this
would require
\[
\mathcal E_{\rm par}
<N^{7/5-2\varepsilon-o(1)},
\]
a full \(N^{1/5+2\varepsilon}\) saving over the grid.  This is much
stronger than merely beating the old \(F^{8/3}\) barrier.

The most realistic next lemma is therefore not a new marginal estimate.
It is a joint correlation-to-incidence statement proving either:

1. angular reuse beyond \(N^{1/5}\) inside one repeated-radius class; or
2. exclusion of the simultaneous column-starved/high-parameter-energy
   geometry by a genuine cross-angle union theorem.

## 8. Claim status

* Theorem 1, Corollary 2, and the exponent optimization are proved.
* The verifier checks the exact finite grid formulas, exponent ledger,
  Xi inverse inequality, and the interval-union equality construction.
* The requested three-way theorem is disproved as an interface theorem;
  the corrected result has four branches.
* No unconditional improvement of \(f_3(N)\) is claimed.
