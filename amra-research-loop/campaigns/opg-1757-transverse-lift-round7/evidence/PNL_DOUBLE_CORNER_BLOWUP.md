# Double-corner and route-scale blow-ups in the `q3:PNL` chamber

## 1. Scope

This note studies the `q3:PNL` nested-odds chart after removing the exact
factor

```text
c^2*q0^4*q4*(1-s4).
```

It resolves the all-bounded double corner, proves both endpoint faces of the
induced activity blow-ups nonnegative, and proves the first mixed Newton face
at route-scale infinity nonnegative.  The coupled intermediate route orders
and higher mixed orders are not controlled here, so this is a reduction and
not a chamber certificate.

Use local coordinates

```text
x=1-s0,  h=1-s3,  z=1-s4,  t=1-tau.
```

The resulting quotient has 2,920 terms.  Every monomial has total
`(x,h)`-degree at least two.

## 2. Exact double-corner principal

Let

```text
B=c*q0*q4+c*q0+c*q4+q0*q4.
```

The entire total-degree-two face in `(x,h)` is the 522-term identity

```text
c^2*q4*(q0+1)*(q4+1-z)^2*B
  * (B*(x-h*(1-t))^2+q0^2*(c+q4)*h^2*(1-t)^2).       (2.1)
```

Thus the corner has exact vanishing order two and a nonnegative moving-square
principal.  The dependence on `z` and `t` in (2.1) is essential; the verifier
checks the full identity rather than an endpoint specialization.

Blow up the ideal `(x,h)^2` in its two standard charts:

```text
h=x*y, divide by x^2;       x=h*y, divide by h^2.     (2.2)
```

Both transformed polynomials have 2,920 terms, and their homogeneous route
degree ranges from 7 through 12.

## 3. Route-scale endpoint faces

The degree-seven face in each chart is an exact square times manifestly
nonnegative factors.  At degree twelve, the `x`-dominant chart reduces to

```text
q0*(c+q4)*y*Px(t)+c*q4*Gx^2,                         (3.1)
```

where the three quadratic Bernstein rows of `Px` are

```text
b0=y*(1-x)^2,
b1=x*(1-x*y)*(1+x*y-2*y)/2,
b2=x*(1-x*y)^2.
```

If `b1>=0`, (3.1) is immediate.  If `b1<0`, then `y*(2-x)>1`, while

```text
b0*b2-b1^2
 = x*(1-x*y)^3*(y*(2-x)^2-x)/4 >= 0.                (3.2)
```

The `h`-dominant degree-twelve face similarly reduces to

```text
q0*(c+q4)*Fh(t)+c*q4*Gh^2.                           (3.3)
```

Its quadratic Bernstein determinant is

```text
h*y^2*(1-h)^3*J/4,
J=4*(1-h*y)-h*y^2*(1-h) >= 3*(1-h).                 (3.4)
```

Equations (3.1)--(3.4) prove both infinite-route endpoint faces
nonnegative; the degree-seven squares prove the zero-route endpoints.

## 4. First mixed infinity face

In the `c`-maximal projective chart, compactify the common route scale and
write

```text
a=1-scale,  b=q4/c,  r=q0/c,  v=1-y,  e=1-z.
```

The compact polynomial has 7,874 terms.  At `(a,v,b,e)=(0,0,0,0)`, the
equal-weight Newton principal has 46 terms and factors as

```text
b*r^4*(1-x)^2*(a+b*(1-x))*H,                         (4.1)

H=a^2*t^2*x^2
  +a*b*x*(1-x^2)*t*(2*t-1)
  +b^2*(1-x)^2*C,

C=(1+2*x)*t^2-(x+2)*t+1.                            (4.2)
```

The discriminant of `C` is `x*(x-4)<=0`.  For `t>=1/2`, every summand of
`H` is nonnegative.  For `0<=t<=1/2`, the determinant of the binary
quadratic in `(a,b)` is

```text
t^2*x^2*(1-x)^2*J,
J=3-x^2-2*x-4*t+4*t*x+4*t*x^2-4*t^2*x^2.            (4.3)
```

After `t=s/2`, the bidegree-`(2,2)` Bernstein controls of `J` are

```text
[[3, 2,   1],
 [2, 3/2, 1],
 [0, 1,   1]].                                      (4.4)
```

They are all nonnegative, proving (4.1) nonnegative on the closed chart.

## 5. The `q0`-maximal mixed corner

In the `q0`-maximal chart let `u` be the compact route scale,
`A=c/q0`, `B=q4/q0`, and reverse `y,z` as above.  The observed zero
stratum is

```text
x=B=1-y=1-z=0.
```

Its equal-weight principal has 46 terms and is

```text
A^4*(1-u)*Q(t),
Q(t)=q0+q1*t+q2*t^2,                                (5.1)
q0=B*u*L^2,
q1=-u*L*M,
q2=B*(L+u^2*x-u*x)^2,
L=-B*u+e*u-e,
```

with the 8-term polynomial `M` reconstructed by the verifier.  Put
`a=1-u` and `p=B*u+a*e`.  The middle quadratic Bernstein row is exactly

```text
b1=a*x*u*p*(a*e-B*u)/2.                             (5.2)
```

The endpoint `Q(1)` is nonnegative: after homogenizing in `(x,B,e)`, its
three maximum charts have respectively 25, 27, and 33 nonzero Bernstein
controls, all positive.

Only `a*e<B*u` requires a determinant check.  Write
`a*e=B*u*y`, `0<=y<=1`, and split into `x=B*q` and `B=x*q`.  After positive
monomial factors are removed, the two determinants are proportional to

```text
J_B = a^2*q^2*(1-y)^2
    + a*q^2*(4-(1-y)^2)
    + 4*a*q*(1-y^2)
    + 4*(q+1)*(y+1)^2,

J_x = a^2*(1-y)^2
    + a*(4-(1-y)^2)
    + 4*a*q*(1-y^2)
    + 4*q*(q+1)*(y+1)^2.                            (5.3)
```

Every summand in (5.3) is nonnegative on the unit cube.  Thus (5.1) is
nonnegative.

## 6. The `q4`-maximal infinity corner

In the `q4`-maximal chart put `a=1-scale`, `A=c/q4`, and `B=q0/q4`.
The equal-weight `(a,A)` principal has 86 terms and factors as

```text
B^4*y*(1-x)^2*(a+A*(1-x*y))*H,                      (6.1)

H=A^2*Px(t)-A*a*t*x*K+a^2*t^2*x^2*y,
K=2*t*x^2*y^2-2*t*y-x^2*y^2+2*y-1.                 (6.2)
```

Here `Px` is the same nonnegative quadratic proved in Section 3.  If the
cross coefficient `-t*x*K` is nonnegative, (6.2) is immediate.  Otherwise
`K>0`, and the binary-quadratic determinant is

```text
t^2*x^2*(1-x*y)^2*J,

J=-4*t^2*x^2*y^2+4*t*x^2*y^2+4*t*x*y-4*t*y
  -x^2*y^2-2*x*y+4*y-1.                            (6.3)
```

The tridegree-`(2,2,2)` Bernstein controls of `J-K` are all nonnegative.
Hence `J=(J-K)+K>0` in the only region where the determinant is needed,
which proves (6.1) nonnegative.

## 7. The common `h`-dominant root

The three `h`-dominant projective charts have the same accumulation after
reversing the route scale, both projective ratios, `h`, `z`, and `t`.  Put

```text
a=1-scale,  H=1-h,  s=1-t,  y=x/h.
```

Although their compact polynomials have respectively 22,786, 21,692, and
20,982 terms, their common total-degree-three face has only 34 terms and is
the exact moving square

```text
3*(H+3*a)*(1-y)^2*(y*(H+3*a+s)-s)^2.                (7.1)
```

Thus the repeated subdivision tail near `y≈1` is again a root curve, not a
negative principal.  Set

```text
w=y*(H+3*a+s)-s,        -s<=w<=H+3*a.               (7.2)
```

Splitting this exact interval gives two compact root charts.  For `w>=0`,
write `w=(H+3*a)z`; after clearing the fourth power of the denominator, the
degree-seven principal is

```text
3*(H+3*a)^5*z^2*(1-z)^2*(H+3*a+s)^2.               (7.3)
```

For `w<=0`, write `w=-s*z`; the corresponding principal is

```text
3*(H+3*a)*(H+3*a+s*z)^2*s^2*z^2*(H+3*a+s)^2.       (7.4)
```

Both are manifestly nonnegative for `0<=z<=1`.  The cleared root-chart
polynomials have 86,464 and 59,892 terms; their remaining radial degrees
start at eight and extend through twenty-seven.

For the negative-root polynomial, projectivize the six nonnegative
deviations and remove their common radial order seven.  Two of the six
maximum-direction charts close without subdivision:

| maximal direction | nonzero Bernstein controls | smallest control |
|---|---:|---:|
| `H=1-h` | 427,058 | `1/51710400` |
| `s=1-t` | 540,935 | `1/25116480` |

Every listed control is strictly positive and is reconstructed with exact
rational arithmetic.  These are full radial subcharts, not merely their
degree-seven principals.  The other four negative-root directions and all
higher orders in the positive-root branch remain open.  Inside the open
`a`-maximal direction, `PNL_A_ROOT_SECOND_NEWTON.md` resolves the observed
rational accumulation at `s/a=2/3` and closes eight of the fourteen charts in
its two-sided second Newton fan: `zeta`, `r`, and `Hbar` below `2/3`, and those
three plus `B` and `d` above `2/3`.  Their 22,149,098 stored nonzero controls
are all strictly positive.  Six second-fan charts remain open, so the first
`a`-maximal chart as a whole is not claimed.
Within the still-open upper `A` direction,
`PNL_A_BOUNDARY_THIRD_NEWTON.md` extracts another exact transverse square and
closes the full no-root half-region plus three nested third-Newton charts with
4,205,922 strictly positive nonzero controls.  In the remaining below-root
`v` chart, its next 122-term Newton face also has an exact manifestly
nonnegative factorization, and the `b=1` and `y=1` endpoints of the resulting
`q`-maximal fourth chart have full low-dimensional Bernstein certificates.
The remaining higher orders stay open.

## 8. Reproduction and consequence

Run from the campaign directory:

```sh
python3 evidence/verify_pnl_double_corner_blowup.py \
  | diff -u evidence/pnl_double_corner_blowup.json -

python3 evidence/verify_pnl_a_root_second_newton.py \
  | diff -u evidence/pnl_a_root_second_newton.json -

python3 evidence/verify_pnl_a_boundary_third_newton.py \
  | diff -u evidence/pnl_a_boundary_third_newton.json -
```

The standard-library verifier reconstructs the 128 deletion forests and 58
marked-connection forests, checks every displayed identity over exact
rationals, and fixes the decisive polynomial hashes.

These results eliminate the bounded double corner, both pure route-scale
endpoints, the first observed mixed Newton direction in every `x`-dominant
route chart, and the common moving-root principal in all three `h`-dominant
charts.  They additionally close two full first-level negative-root radial
subcharts and two nested second-Newton subcharts in the `a` direction.  Route
degrees 8 through 11, the other mixed/root directions, and the compact
interiors remain coupled.  Coverage stays at 63 of 81 negative-page chambers;
`q3:PNL`, its symmetry image, the generic `Delta_b` sign, and OPG-1757 remain
open.
