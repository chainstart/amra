# Affine echo families reduce exactly to sets of multiples

This is an author-verified all-parameter theorem.  It uses the classical
Davenport--Erdős theorem that the set of multiples of an arbitrary set of
positive integers has logarithmic density, equal to the increasing limit of
the densities of its finite subunions.  It is not an independent audit and no
novelty claim is made.

## The theorem

Fix integers `c >= 1` and `b` with `gcd(b,c)=1` and `c+b>0`, and an arbitrary
set `R` of positive integers for which `cr+b > r`.  Define

    D_(c,b)(R) = union over r in R of {r + h(cr+b) : h >= 0}.

Then `D_(c,b)(R)` has logarithmic density.

More precisely, put

    A = {cr+b : r in R}

and let `M_A` be the set of positive multiples of members of `A`.  If the
logarithmic density of `M_A` is `beta`, then the logarithmic density of
`D_(c,b)(R)` is also `beta`.

## Algebraic equivalence

For positive integers `k,r`,

    k = r + h(cr+b) for some h >= 0

is equivalent to

    ck+b = (1+ch)(cr+b).

Conversely, if `cr+b` divides `ck+b`, then the quotient is congruent to `1`
modulo `c`, because numerator and denominator are both `b (mod c)` and `b`
is invertible modulo `c`.  The
positive quotient is therefore `1+ch` for some `h >= 0`.  Hence

    k in D_(c,b)(R)  iff  ck+b is in M_A.

## Logarithmic equidistribution in the required progression

Let

    E = M_A intersect {b (mod c)}.

For a finite subset `F` of `A`, write `M_F` and `E_F` for the corresponding
sets.  Every member of `A` is coprime to `c`.  Inclusion--exclusion therefore
shows

    density(E_F) = density(M_F) / c:

every intersection term is the set of multiples of an lcm `L` coprime to
`c`, and its further intersection with `b (mod c)` has density `1/(cL)`.

Let `beta_F=density(M_F)`.  Davenport--Erdős gives
`beta_F -> beta=delta_log(M_A)` along an exhausting sequence of finite
subsets.  Since `M_F` is contained in `M_A`, the difference
`M_A minus M_F` has logarithmic density `beta-beta_F`.  The inclusions

    E_F subset E subset E_F union (M_A minus M_F)

give

    beta_F/c <= lower_delta_log(E)

and

    upper_delta_log(E) <= beta_F/c + beta-beta_F.

Letting `F` exhaust `A` squeezes both sides to `beta/c`.  Thus `E` has
logarithmic density `beta/c`.

Finally, under the bijection `k -> ck+b`,

    1/k = c/(ck+b) + O(1/k^2).

The total error is bounded, while `log(cX)=log X+O(1)`.  Therefore
`delta_log(D_(c,b)(R))=c delta_log(E)=beta`, as claimed.

## Periodic approximation and finite unions

The proof gives more than existence.  If `F` is finite, the corresponding
`D_(c,b)(F)` is periodic, and the same transformation gives

    upper_delta_log(D_(c,b)(R) minus D_(c,b)(F))
      <= c (beta-beta_F).

The right side tends to zero as `F` exhausts `R`.  Thus every affine echo
family is approximable from inside by finite periodic unions with arbitrarily
small upper-logarithmic remainder.

This approximation property is stable under finite unions.  For finitely many
pairs `(c_l,b_l)`, choose a finite periodic approximation to each family with
total remainder below `epsilon`; the union of the approximants is periodic,
and the union of all remainders has upper logarithmic density below
`epsilon`.  Letting the approximants increase proves:

> Every finite union of coprime affine echo families has logarithmic density.

Therefore a counterexample based on this representation must use infinitely
many genuinely different affine charts with a non-summable tail, or a truly
non-affine relation between first target and echo period.  Merely alternating
among finitely many slopes and intercepts cannot work.

## Consequence for the binary-reservoir attack

In the binary construction take `c=Q/2` and `b=-1`.  The exact echo
calculation gives

    d_r = Qr/2-1 = cr-1,
    deleted rare indices = union over selected r of {r+h d_r:h>=0}.

The theorem applies to every selected index set `R`, including arbitrary
scale-spanning and alternating-block schedules.  If `beta` is the associated
multiples-set logarithmic density, the final survivor has logarithmic density

    1/2 + (1-beta)/Q.

Thus the strongest explicit positive-background amplifier from this campaign
cannot be concatenated into a counterexample, even with infinitely many
blocks.  This closes that algebraic family, not the public problem: general
conditional cells need not have echo modulus affine in their first active
index, and no decomposition of all positive-density systems into finitely or
summably many affine families is known.

## Source dependency

- H. Davenport and P. Erdős, *On Sequences of Positive Integers*, Theorem 1:
  https://users.renyi.hu/~p_erdos/1936-04.pdf
