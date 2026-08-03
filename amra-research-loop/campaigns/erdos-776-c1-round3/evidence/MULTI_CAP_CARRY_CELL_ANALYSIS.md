# Multi-cap carry-cell analysis

## Outcome

The multi-cap inequality has not been proved or refuted on the actual dyadic
domain.  It admits an exact carry-cell formulation, however, and the role of
legality is now sharp enough to guide the next proof attempt:

- after relaxing legality to `s=k-1=1`, there is an infinite counterfamily;
- actual legality forces `s>=3`;
- no dyadic `q,h` information is needed to state the remaining candidate
  theorem, only `s>=2` and the exact complement/sign relations.

Thus a proof that ignores `s` cannot work.  The smallest plausible stronger
lemma is a relaxed `s>=2` carry theorem; it strictly contains the actual
domain and its threshold is sharp because `s=1` fails infinitely often.

## 1. Exact coordinates for every carry cell

Write `s=k-1`, `u=r+s`, and the two rank-two canonical words as

\[
 \alpha=\binom a2+e,\quad 0\le e<a,
 \qquad
 \beta=\binom A2+E,\quad 0\le E<A.
\]

The complement identities give

\[
 \tau=\binom r2-\alpha+1,qquad
 \beta-\alpha=\Delta_s(r):=sr+\binom s2-1.
\]

Consequently the upstream rank-two carry is completely described by

\[
 \binom A2\le \binom a2+e+\Delta_s(r)<\binom{A+1}2,
 \qquad
 E=\binom a2+e+\Delta_s(r)-\binom A2.
\]

The next two inputs are

\[
 p=\binom{a+1}3+\binom{e+1}2-\binom r2,
 \qquad
 v=\binom{A+1}3+\binom{E+1}2-\binom u2.
\]

Define their deficits from the next rank-three caps by

\[
 \rho=\binom{c+1}3-p,qquad
 \sigma=\binom{d+1}3-v.
\]

Then the statements that `c=top_3(p)` and `d=top_3(v)` are exactly

\[
 1\le\rho\le\binom c2,qquad
 1\le\sigma\le\binom d2.
\]

Equivalently, if

\[
 \delta=\binom r2-\binom{e+1}2,qquad
 \varepsilon=\binom u2-\binom{E+1}2,
\]

then

\[
 \rho=\delta-\left(\binom{a+1}3-\binom{c+1}3\right),
\]

\[
 \sigma=\varepsilon-\left(\binom{A+1}3-\binom{d+1}3\right).
\]

These inequalities partition the problem into disjoint, exact carry cells;
there is no approximation or monotonic-wall assumption in this partition.

Finally,

\[
 v-p=\sum_{x=c+1}^{d}\binom x2+\rho-\sigma,
\]

so the failed rank-four condition is exactly

\[
 \boxed{\sum_{x=c+1}^{d}\binom x2+\rho-\sigma<\binom r2.}
\]

This exposes why `gamma4<0` alone does not prove the desired result: it is an
upper bound on the interval length, while the multi-cap claim needs a lower
bound on the number and location of crossed caps.

## 2. Necessary and sufficient top-cell threshold

For fixed `a,c`, define

\[
 D(a,c)=\min\left\{D\ge c+2:
   \binom D4-\binom{c+1}4\ge\binom{a+1}3\right\}.
\]

Since the left side is strictly increasing in `D`, the proposed multi-cap
inequality is equivalent to each of

\[
 d\ge D(a,c),
\]

\[
 v\ge\binom{D(a,c)}3,
\]

and the following upstream rank-two carry bound:

\[
 \boxed{\binom A3+\binom E2-\tau
        \ge\binom{D(a,c)}3.}
\]

This boxed inequality is the smallest remaining lemma: it contains no
rank-three lower digits and no `d`.  Proving it from the preceding carry
cell constraints closes the candidate; lowering its right side by one
admits the entire failing boundary cell `d=D(a,c)-1`.

A convenient sufficient, but not necessary, subcell condition is

\[
 (d-c-1)\binom{c+1}3\ge\binom{a+1}3,
\]

because every term of
`sum_{x=c+1}^{d-1} C(x,3)` is at least `C(c+1,3)`.  This is stronger than
the exact `D(a,c)` threshold and should only be used as a killable first
branch, not substituted for the target theorem.

## 3. Where dyadic legality enters

The dyadic lattice can be reconstructed from `(r,s,a,e)` by

\[
 q=\frac{\binom{r+1}2-\binom a2-e-\binom{s+1}2}{s+1},
\]

\[
 2h=sq+\binom s2+2-r,qquad h=112\,2^{j-1}.
\]

The remaining legal inequalities are `q>=2`, `r<q`, `r+s<q+1`, and
`q+s+1<h`.

Most importantly, `q+s+1<h` excludes `s=1,2` directly:

- for `s=1`, `q=2h-2+r`, hence `q+2>=2h>h`;
- for `s=2`, `q=h+(r-3)/2`, hence `q+3=h+(r+3)/2>h`.

Therefore every actual state has

\[
 \boxed{s\ge3.}
\]

The power-of-two condition may ultimately be unnecessary.  A stronger and
cleaner surviving conjecture is:

> **Relaxed carry theorem.**  Let `s>=2`.  Assume the exact complement
> identities, `p,v>0`, `beta<=C(r,2)` (equivalently `gamma3<0`), and
> `v-p<C(r,2)` (equivalently `gamma4<0`).  Then
> `d>=D(a,c)`.

This would prove the actual result because legality gives `s>=3`.  It cannot
be extended to `s=1`.

## 4. Infinite boundary counterfamily at `s=1`

For every integer `a>=6`, set

\[
 s=1,qquad r=a+2,qquad e=a-1,qquad
 \alpha=\binom{a+1}2-1.
\]

Then

\[
 \tau=a+3,qquad
 \beta=\binom{a+1}2+a=\binom r2-1,
\]

so `gamma3=-2`.  The rank-two words are `(a,a-1)` and `(a+1,a)`, and

\[
 p=\binom a3+\binom{a-1}2-a-2,
\]

\[
 v=\binom{a+1}3+\binom a2-a-3.
\]

For `a>=6`, these have top indices

\[
 c=a,qquad d=a+1,
\]

while

\[
 \gamma_4=v-p-\binom r2=-a-3<0.
\]

Nevertheless

\[
 \binom d4-\binom{c+1}4-\binom{a+1}3
 =-\binom{a+1}3<0.
\]

Thus complement identities, both double-positive stages, `gamma3<0`, and
`gamma4<0` do not suffice by themselves.  The family sits exactly in the
one-cap cell `d=c+1`, and legality removes it by forcing `s>=3`.

## 5. Finite check of the relaxed boundary model

[`check_multi_cap_boundary_cells.py`](check_multi_cap_boundary_cells.py)
enumerates the relaxed carry coordinates, not the actual dyadic fibres.  On
`4<=r<=180` and `1<=s<=8` it found:

- `s=1`: 876,058 admissible relaxed states, 750,926 failures;
- `s=2`: 158,658 admissible states, no failure;
- `s=3`: 17,085 admissible states, no failure;
- `s=4,...,8`: no admissible state occurs below this small `r` cutoff.

The run took 11.3 seconds under the 2 GiB/180 second limit.  The result is
stored in
[`multi_cap_boundary_cells.json`](multi_cap_boundary_cells.json).

This finite absence for `s=2,3` is evidence for the relaxed carry theorem,
not a proof.  Its role is to isolate the sharp analytic threshold suggested
by the infinite `s=1` counterfamily; it does not advance the campaign to a
global conclusion.

