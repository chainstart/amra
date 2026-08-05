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

## 5. Reproduction and consequence

Run from the campaign directory:

```sh
python3 evidence/verify_pnl_double_corner_blowup.py \
  | diff -u evidence/pnl_double_corner_blowup.json -
```

The standard-library verifier reconstructs the 128 deletion forests and 58
marked-connection forests, checks every displayed identity over exact
rationals, and fixes the decisive polynomial hashes.

These results eliminate the bounded double corner, both pure route-scale
endpoints, and the first observed mixed infinity direction as possible
negative principals.  Route degrees 8 through 11, higher mixed Newton
orders, and the compact interiors remain coupled.  Coverage stays at 63 of
81 negative-page chambers; `q3:PNL`, its symmetry image, the generic
`Delta_b` sign, and OPG-1757 remain open.
