# Canonical one-step reset no-go

## Statement

At any rank `n>=4`, allow the lower-tail digits `A_n,B_n` to depend
arbitrarily on the actual strip parameter `q`.  Suppose the reset retains
the round-four bottom recurrence

```text
B_(n+1) = C(B_n,2) - (20n-52)
```

and the same leading `H/q` staircase, and suppose the next word is canonical,
so in particular

```text
B_(n+1) < q-(5(n+1)-16) = q-(5n-11).
```

Then its current surplus

```text
gamma_n = C(B_n,2)-C(A_n+1,2)+2-4q
```

is strictly negative whenever `q>=5n-13`.

## Proof

Nonnegativity of the binomial term and the bottom recurrence give

```text
gamma_n
 <= C(B_n,2)+2-4q
  = B_(n+1)+(20n-52)+2-4q
  < q-(5n-11)+20n-50-4q
  = -3q+15n-39.
```

For `q>=5n-13`, the last expression is at most zero, and the preceding
canonical inequality is strict.  Hence `gamma_n<0`.

## Route consequence and boundary

This eliminates not only fixed finite reset menus but also arbitrary
`q`-dependent or growing-menu choices **while the same leading staircase,
bottom recurrence, and one-step canonical continuation are retained**.
A successful pre-rank-42 seed must therefore alter a leading block or the
bottom recurrence, or recover only at a terminal word for which no canonical
continuation is claimed.  The latter does not by itself supply the required
persistent suffix interface.

This remains a route obstruction, not a proof of the public Erdos-776 bound.
