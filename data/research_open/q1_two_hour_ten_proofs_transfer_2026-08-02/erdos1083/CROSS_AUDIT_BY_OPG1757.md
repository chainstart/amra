# Independent cross-audit of the Erdős #1083 freeze

Auditor: OPG-1757 lane  
Window: 2026-08-02 21:25--21:50 HKT  
Verdict: **PASS_AFTER_REPAIR**  
Public-problem status: **Erdős #1083 remains OPEN**.

## 1. Independence and scope

I checked the frozen hashes in `AUTHOR_FREEZE_2120.md`; all five match the
files actually audited.  I did not import, call, copy, or derive expected
values from either author verifier.  The independent executable check is
`cross_audit_by_opg1757_independent.py`; it builds convolutions,
autocorrelations, factorial energies, finite Fourier transforms, and the two
explicit signed examples directly from the displayed definitions.

The algebraic stage results survive reconstruction, subject to the two local
repairs in Section 2.  Neither repair touches the exact-block application,
where `S>=2` is already stated.  Nothing audited here proves the missing
power-large reciprocal-frame bound, the Euclidean outer extraction, or Erdős
#1083.

## 2. Required repairs

### R1. Add `S>=1` to the global hypotheses (0.1)

As displayed, (0.1)--(0.2) allow `S=0`.  Take the torsion-free trivial group,

```text
A_0=A_j=empty,  q=2[0],  C=2,  M=N_j=empty.
```

Then both products in (0.2) are the empty mask and
`|M|=|N_j|=SC=0`, so every displayed hypothesis holds.  But the trivial
group has no two-term mask, and therefore the edit conclusion (0.6) is
impossible.  The sentence in Lemma 1.2 saying that the trivial-group case
“necessarily `S=C=1`” is false at this boundary.  The same boundary also
invalidates (1.3), because `q=2[0]` is nonnegative and not a mask, and it
invalidates the headline Fourier-invertibility claim because the zero mask is
not invertible.

Concrete repair: add

```text
1 <= S=|A_0|=|A_j|
```

to (0.1), or state the entire package only for `S>=2`.  With `S>=1`, a
trivial torsion-free group forces `S=1`; the mask product then forces
`C=1,q=1`, exactly as the intended trivial-case argument says.  A nontrivial
torsion-free abelian group is infinite, so the fresh points used in Lemma 1.2
exist.  The exact-block application already has `S>=2`, hence it is
unaffected.

### R2. Retain “signed” in the minimum-debt normal form

The sentence preceding (2.16), read literally, says that `delta(q)=1` alone
forces `q=P_R-[v]`.  The unsigned integral function `q=2[0]` has augmentation
two and `delta(q)=1`, but has no negative coefficient.  What the proof and
application establish is

```text
if q is signed and delta(q)=1, then q=P_R-[v], v not in R, |R|=C+1.
```

This signed hypothesis is present in the surrounding Theorem 2.2 context,
so the repair is expository and does not change the common cancellation
alphabet conclusion.

## 3. Independent reconstruction

### Factorial energy and edit stability

For an integer coefficient `n`, `n(n-1)/2` is a nonnegative integer: it is
`binom(n,2)` for `n>0` and `binom(|n|+1,2)` for `n<0`.  Summing gives

```text
delta(q) >= E_+(q)+N_-(q) >= 0,
```

with equality zero exactly for a zero-one mask of augmentation `C`.
Writing positive mass as `C+N_-` and the number of positive support points
as `r=C+N_--E_+` reproduces the two edit cases.  Keeping `C` positive points
costs `2N_-`; keeping all `r<C` and adding fresh points costs `2E_+`.
Thus the distance is at most `2 delta(q)` on an infinite group.

The independent script exhausted 270 signed/unsigned coefficient functions
on four fixed sites with positive augmentation.  It checked integrality,
nonnegativity, the zero case, and an explicitly constructed edit mask in
every case.

### Autocorrelation sign, order, and stability

Direct expansion gives

```text
||P_A q||_2^2
= S ||q||_2^2 + sum_(a,b in A, a!=b) Corr_q(b-a).
```

The sum is over **ordered** pairs.  Since
`||q||_2^2-C=2 delta(q)`, a mask output of mass `SC` gives exactly
`-2S delta(q)`, with the negative sign claimed in (2.2).  For the witness

```text
A={0,1,2},  q=1-x+x^2,  delta(q)=1,
```

the ordered sum is `-6`; an erroneous unordered sum is only `-3`.  Replacing
the mask norm by
`||H||_2^2=SC+2 delta(H)` yields (2.18) and subtraction yields (2.19).
The script checked 3,780 exact ledger instances, including 140 mask-product
instances.

### Popular difference

Writing `q=q^+-q^-`, coefficientwise nonnegativity gives `U=P_Aq^+ >=
V=P_Aq^-`.  Integrality implies

```text
<U,V> >= ||V||_2^2 >= S N_-.
```

Expanding the same scalar product has total positive/negative weight
`(C+N_-)N_-` and uses the ordered multiplicity of `r-v`, never the zero
difference because the supports are disjoint.  The weighted average therefore
gives (2.7), and bounding by `mu(A)` gives (2.8).  An independent exhaustive
search checked every eligible case in a 227-instance finite family, allowing
colliding nonnegative outputs.  The Sidon specialization and the
`7/9-1/18=13/18` endpoint exponent follow.

### Prime shadow, collisions, and Fourier normalization

For a finite collection of supports in `Z^r`, only finitely many primes can
annihilate a fixed nonzero difference vector.  A sufficiently large prime is
therefore simultaneously support-injective.  This condition is genuinely
needed for norm preservation: reducing `[0]+[7]` modulo seven changes its
squared norm from two to four.  Product equality itself survives because
reduction is a group-ring homomorphism; injectivity on `M,N_j` keeps their
images masks, and injectivity on `q_j` keeps its squared norm.

For a nontrivial character of `(Z/pZ)^r`, a vanishing `S`-term character sum
would give a nonnegative integer polynomial of degree below `p` divisible by
`Phi_p`; its mass would be a positive multiple of `p`.  Thus `0<S<p` gives
invertibility.  The strict guard is necessary: the full three-term mask on
`Z/3Z` vanishes at a nontrivial character.

With the unnormalized transform, Parseval is

```text
||f||_2^2 = (1/|H|) sum_chi |f_hat(chi)|^2.
```

Dividing `M_hat=A_j_hat q_j_hat` and applying this normalization gives (3.2).
Using the second mask product gives (3.5); subtracting it from `S` times
(3.2) gives (3.3), and summing gives (3.4).  No pointwise sign is used.  On
the exact witness above modulo seven, the independently evaluated right-hand
sides were respectively `2`, `6`, and `4` for a duplicated two-row aggregate,
exactly `2 delta`, `2S delta`, and `2 sum delta`.  All 156 nonempty proper
rank-one masks for `p=5,7` were also checked for nonvanishing transforms.

### Full-transverse minimum-debt firewall

For each `4<=S<=12`, direct bivariate convolution verified that

```text
Q_S=x+y-xy+xy^S+x^S y
```

has augmentation three, squared norm five, and `delta(Q_S)=1`, while both
`P_S(x)Q_S` and `P_S(y)Q_S` are zero-one masks with exactly `3S` terms.
Thus the claimed rowwise-transversality no-go is real: even the strongest
single-row geometry cannot force a debt larger than one.  The manuscript
correctly does not promote this to a power-large common-mask construction.

### Aperiodic signed quotient

Independent univariate multiplication recovered exactly the ten exponents in
(0.6), and independent multiplication of the three factors in (4.2)
recovered `Q`.  Their augmentations are `(2,1,1)` and
`Q(1)=2, ||Q||_2^2=6, delta(Q)=2`.  Separately, exact arithmetic modulo three
recovered both Rabin remainders and the zero `3^6` remainder, confirming
irreducibility.  The three rational sign intervals for
`y^3+y^2-3y-1` confirm both unit-circle and off-circle roots, so the
irreducible polynomial cannot have a torsion zero.  The derivative bound 15,
nearest-root arc length, and continued-fraction subsequence give the stated
`15 pi/n` and infinite-subsequence `30 pi/n^2` bounds.  Finally,
`M=PQ` makes the ratio identically `|Q|^2`; Parseval gives average six on a
support-injective shadow.  This is a one-row obstruction only, as the firewall
states.

## 4. Independent executable result

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 cross_audit_by_opg1757_independent.py
```

Result:

```text
ERDOS1083 INDEPENDENT CROSS-AUDIT: PASS_AFTER_REPAIR
factorial_edit_cases: 270
collision_ledger_cases: 3780
mask_product_cases: 140
ordered_debt_witness: -6
unordered_half_witness: -3
popular_difference_cases: 227
invertible_masks: 156
Fourier right-hand sides: rowwise 2.0; second 6.0; aggregate 4.0
full_transverse_delta_one_parameters: 9
aperiodic quotient: 10 product terms; delta 2; irreducible mod 3
fixed-M addendum: 4 augmentation-five divisors; exactly 1 mask divisor
small gcd corroboration: 127 primitive pairs through 20; 0 nonconstant gcds
S=0 hostile counterexample: FOUND
unsigned delta=1 wording counterexample: FOUND
imports_author_verifier: False
public_problem_proved: False
```

## 5. Audit addendum: `SECOND_SCALAR_SCRATCH_HANDOFF.md`

This subsection is explicitly an addendum, not part of the author-frozen
theorem verdict.

The exact fixed-`M` portion passes independent reconstruction.  Factoring the
displayed `M=PQ` gives four distinct irreducible monic factors with
augmentations `(5,2,1,1)`.  Because the factorization is square-free, every
normalized divisor is a subset product.  Augmentation five forces inclusion
of `P`, exclusion of the augmentation-two factor, and an arbitrary choice of
the two augmentation-one factors.  There are therefore exactly four such
divisors.  Direct expansion shows exactly one is a zero-one mask, namely
`P`.  Reciprocity also gives `x^6P(x^-1)=P`, so reversing the scalar sign
does not create a new fixed-`M` divisor.

The augmentation contradiction is valid in precisely its conditional scope.
If two primitive scalar substitutions are coprime and both divide an integral
common mask of augmentation `5C`, their monic product divides it; Gauss's
lemma leaves an integral quotient.  Evaluation at one gives
`5C=25R(1)`, impossible for `1<=C<5`.  This argument does not prove the
substitutions coprime outside the tested range.

As an independent finite guard, the audit script checked all 127 primitive
unordered pairs `1<=r<s<=20` and found no nonconstant gcd.  This deliberately
does not duplicate the author's larger searches.  The manuscript correctly
labels its bounds `r,s<=100`, `<=24`, and `<=200` as finite and explicitly
leaves larger rational ratios, irrational directions, different quotients,
and different common masks open.  No unbounded second-scalar conclusion may
be entered in a claim ledger.

## 6. Repair validation

At 21:34 HKT the author applied both requested changes.  I independently
reopened the repaired manuscript and confirmed that (0.1) now begins
`1<=S=|A_0|=|A_j|` and that the paragraph before (2.16) now says “in the
signed minimum-debt case” and explicitly assumes `q` signed.  The repaired
main manuscript has SHA-256

```text
dc2bff5f9cbd92274463104ca0b84b60eaeb07bfb13f644f86c6c0e1d6db4dd0  SIGNED_RESIDUAL_FACTORIAL_ENERGY.md
```

The independent audit script was rerun after the repair and again completed
successfully.  The hostile counterexamples remain in that script as regression
guards against accidentally removing either hypothesis.

## 7. Verdict and firewall

**PASS_AFTER_REPAIR.**  The live manuscript now has `S>=1` in (0.1) and
“signed” in the minimum-debt normal-form sentence.  After those local repairs, the factorial
energy, edit stability, ordered autocorrelation, popular-difference,
prime-shadow/Fourier, stable collision, full-transverse minimum-debt, and
aperiodic signed-escape claims pass independent reconstruction in their stated
application range.

The audit does not supply the missing `o(K)` reciprocal-frame upper bound,
cross-row synchronization, outer Euclidean extraction, a distance-exponent
improvement, or a counterexample to Erdős #1083.  The public problem remains
**OPEN**.

## 8. Final scratch addendum: global second-scalar theorem

Target: `SECOND_SCALAR_FINAL_SCRATCH.md`  
Decision: **PROMOTE** as a fixed-source stage theorem.  
Public status: **Erdős #1083 remains OPEN**.

The unbounded gcd proof survives an independent hostile reconstruction.

1. For `f(y)=y^3+y^2-3y-1`, the rational-root test gives irreducibility and
   the discriminant is `148=4*37`, a nonsquare.  Its three displayed sign
   intervals give three real roots.  Hence its splitting field `K` is a
   totally real `S_3` extension and its unique quadratic subfield is
   `Q(sqrt(37))`.
2. With `d_i=y_i^2-4`, the resultant/product calculation is
   `prod_i d_i=(-f(2))(-f(-2))=5`.  This is not a square in `K`, since that
   would put `Q(sqrt(5))` inside an `S_3` field whose only quadratic subfield
   is `Q(sqrt(37))`.  Transitivity lets any single `y_i`, or the complementary
   `y_k` in a two-factor product `5/d_k`, be sent to an inside root.  The
   resulting negative real conjugate cannot be a square in the totally real
   field.  These arguments exclude all seven nonempty subset products, so
   the three square classes really are independent.
3. Kummer independence gives
   `Gal(K(sqrt(d_1),sqrt(d_2),sqrt(d_3))/K)=C_2^3`.  The `S_3` action lifts by
   permuting the indexed square roots.  Thus each coordinate sign flip is an
   actual automorphism: it inverts exactly one reciprocal root pair and fixes
   the other two pairs pointwise.  This is the precise property needed later,
   not merely a root-count heuristic.
4. If a common root `alpha` existed, then roots `z=alpha^r` and
   `w=alpha^s` of `P` would obey `z^s=w^r`.  For different reciprocal pairs,
   the sign-flip of `z` alone gives `z^(-s)=w^r`, hence `z^(2s)=1`.  In one
   pair, either `z=w`, giving `z^(s-r)=1`, or `z=w^(-1)`, giving
   `z^(r+s)=1`.  Transitivity plus the off-circle pair shows that no root of
   irreducible `P` is torsion, so all cases contradict `r!=s`.
5. For rationally dependent nonzero real scalars, the group they generate is
   a rank-one lattice.  Removing its common positive unit and using
   reciprocity for negative exponents reduces the two masks to associates of
   `P(x^r),P(x^s)` with coprime positive integers `r,s`; unequal absolute
   values give `r!=s`.  For a rationally independent pair the group ring is
   `Z[u^+-1,v^+-1]`; irreducibility survives the pure transcendental
   extension, so `P(u)` and `P(v)` are nonassociate and coprime.
6. In the Laurent UFD, two coprime monic masks dividing an integral `H` have
   product dividing `H`.  Augmentation then gives
   `5C=25R(1)`, impossible for `1<=C<5`.  This proves only the fixed
   five-point-source no-second-row theorem and does not control other sources
   or a power-large family.

One display-only repair is requested: the display containing equation (5),
`z^s=w^r`, is missing its closing `\]`.  This does not affect the theorem or
the **PROMOTE** decision, but should be fixed before publication.
