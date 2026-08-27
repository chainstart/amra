# Obstruction analysis: prime abundance removes the epsilon loss

## The inherited loss

Q.1 obtains `2s` labels by repeatedly applying Bertrand's postulate.  Its
bound permits the last prime to be `2^(2s)` times the first, so keeping the
rough products below `N` forces `s=O(epsilon K)` when the first prime is near
`N^(1/2-epsilon)`.

This is not the actual supply near a large scale.  The prime number theorem
gives

`pi(2X)-pi(X) ~ X/log X`.

For `X=b^(floor(K/2)-A)` with fixed `b,A`, this count grows exponentially in
`K` and eventually exceeds `K/2`.  Hence all edge labels for a path with
`s=floor(K/4)` can be selected inside the single interval `(X,2X)`.

## Exact candidate budget

Every path rough part is then less than `(2X)^2=4X^2`.  Since `4<=b^2`,

`q_i < b^(K-2A+2)`.

Rounding upward to the next power of `b` leaves at least `2A-2` padding
exponent units.  The one-vertex shore imbalance still has discrepancy below
`K+s`; distributing it over `s+1` vertices costs at most five units each.
Thus `A>=4` leaves nonnegative exponents and a fixed tail `(N/b^6,N]`.

The same unique edge-prime equations prove support minimality.  All
controlled zero-transcript primes smaller than `X` are avoided.

## Matching host boundary

The interval cannot be shifted wholly above `sqrt(N)`: an internal vertex is
the product of two distinct incident labels, and two labels greater than
`sqrt(N)` already have product greater than `N` before padding.  The proposed
cutoff is therefore within a fixed factor of the exact limit of this path
host.

## Query consequence

The deterministic and shared-seed randomized arguments of Q.2--Q.4 use only
the existence of a relation contained in the retained zero transcript.  If
the geometric budget passes, they lift verbatim with controlled primes below
`X`, threshold `t<N/b^6`, and the same exact bound

`Pr(transversal)<=E|D|/(L-t)`.
