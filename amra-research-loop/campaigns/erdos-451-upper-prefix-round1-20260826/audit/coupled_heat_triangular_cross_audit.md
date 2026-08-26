# Same-model cross-audit: coupled conductor heat and triangular divisors

## Verdict: PASS

This is a fresh reconstruction by a separate Codex agent in the same
model/tool ecosystem.  It is not a human review or externally independent
audit.  I did not modify the author note, JSON evidence, or replay script.
Every requested identity and asymptotic ledger survives; no mandatory
mathematical correction was found.

## Conductor heat: (4), (7)--(15)

For squarefree `P`, the exact Fourier coefficient and the character kernel
factor coordinatewise.  A principal local coordinate contributes
`delta_p`, while the sum of all nonprincipal local terms is exactly
`z_p(x)`.  Since the primitive support conductor contributes one factor
`p^(-sigma)` precisely on each nonprincipal coordinate, expansion of the
physical-space product reconstructs (4), including the `chi(-Q0)` phases.
For the product multiset,
`K_chi(W)=S_X^P(chi)^2=sum_{x in W}chi(x)`, so no normalization factor is
missing.

At an allowed coordinate the local factor in (4) is

```text
a_p=delta_p+p^(-sigma)(1-delta_p),
```

and at a violation it is
`delta_p(1-p^(-sigma))=a_p r_p`.  Multiplying proves the positive
near-survivor identity (7).  Because `a_p>=delta_p`,

```text
0<=r_p<=1-p^(-sigma)<=sigma log(p)<=sigma log(2k),
```

which verifies (8).  If there is no survivor, every violation set is
nonempty; all `r_p<=1` and `A(sigma)<=1`, so summing gives (9).

Consequently principal-scale positivity can contradict the no-survivor case
only under (11).  With `log P=(1+o(1))k` and
`delta=exp(-Theta(k/log k))`, (11) implies uniformly for every `f|P`

```text
1-f^(-sigma)<=sigma log f
  =O(delta k/log k)=o(1),
```

which is (13).  Conversely, fixed damping at
`Y=exp(Theta(k/log k))` needs `sigma=Omega(log k/k)`; then (9) is on the
`N log(k)^2/k` scale, exponentially above `delta N`.  The endpoint
resolution no-go is therefore correctly scoped to positivity-only heat
continuation, not to a signed Tauberian theorem controlling near-survivors.

Direct differentiation also confirms (14).  An all-allowed occurrence has
derivative `-sum_p(1-delta_p)log p`; an occurrence whose only violation is
`p` has derivative `delta_p log p`; at least two violations give a zero of
order at least two.  More generally, each violated factor has leading term
`sigma delta_p log p`, while every allowed factor is `1+O_k(sigma)`, proving
the positive leading coefficient and order in (15).  Thus the derivative
ledger is genuinely triangular in the exact violation number.

## Triangular divisor interface: (17), (20)--(25)

For `p=k+b`, membership means
`Q0*x congruent -j (mod p)` for a unique `1<=j<=d_p=b-1`.  In the product
`D(y)`, the same prime appears in the `j`-th gcd exactly when
`p>k+j`; this is equivalent to `j<=b-1`.  Since `p>k`, it cannot divide two
different shifts among `y+1,...,y+k-1`, so `D(y)` is squarefree.  Since
`d_p<p`, the denominator `d_p!` is a unit modulo `p`; hence the binomial
condition is equivalent to one of its numerator shifts being divisible by
`p`.  This reconstructs all three statements in (17), as well as the stated
base-`p` carry interpretation.

For a support `S`, `E_S=P_S/gcd(P_S,D(y))` is exactly the product of the
violated support primes.  Locally,

```text
allowed:  z_p=k/(p-1),
violated: z_p=-(b-1)/(p-1)
          =(k/(p-1)) (-(b-1)/k).
```

Factoring `kappa_S` proves (20), with the parity and varying offset weights
preserved.  At full support `delta=kappa rho`, so (21) is exactly sufficient
for `C_P(W)=o(delta N)`; the note correctly warns that it addresses only the
full-support slice rather than the entire high-conductor aggregate.

Each prime in `D(y)` divides its unique selected shift, proving (22).  The
binomial absorber has `log Q0=O(k/log k)` at
`A=floor(k/log(k)^2)`, while `X^2=exp(O(k/log k))`, giving (23).  Therefore

```text
log D(y)<=k log(y+k)=O(k^2/log k),
omega(D(y))=O(k^2/log(k)^2),
```

as in (24).  PNT gives (25): `log P=Theta(k)` and
`|mathcal P|=Theta(k/log k)`.  The crude size capacity thus exceeds the
entire remaining-prime set and cannot force a missing prime or signed
cancellation.  This is correctly a no-go for size-only use of (22), not for
a shifted-divisor theorem retaining the signs in (20).

## Guarded finite replay and hashes

The JSON boundary is accurate: it labels the computation only as a finite
regression of (7), (17), and (20), with no asymptotic inference.  Its
`source_sha256`

```text
3d1b707a35cb63877d1a0f759265ed3c47f62f822234e478959a4dc645633a7d
```

matches the current
`work/coupled_heat_triangular_audit.py` byte-for-byte.  The recorded command
uses the required OpenMath memory guard, unit
`openmath-task-20260826-193424-224509.scope`, exit status `0`, peak RSS
`12,160 KiB`, zero swap, and `0.28s` wall time.

I independently replayed the unchanged script through the same guard:

```text
unit=openmath-task-20260826-194120-227031.scope
exit status=0
peak RSS=12,000 KiB
swap=0
wall time=0.26s
```

It reproduced all four cases, all 3,913 tested unit pairs, every listed
prime set and count, and `all_identities_exact=true`.  The small RSS/time
variation is ordinary run-to-run measurement noise.  The script uses exact
`Fraction` arithmetic for the centered and heat identities and integer
arithmetic for the triangular identity.

## Scope conclusion

The conductor heat identity and triangular shifted-divisor identity are
genuine coupled representations, but neither supplies the still-missing
near-survivor distribution or signed weighted-divisor cancellation.  The
author's `closes=[]`, unchanged public exponent, and surviving two-route
interface are stated at the correct strength.
