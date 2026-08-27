# Representation search

The search used five non-equivalent families: exponent geometry, exact
prime-incidence kernels, valuation cylinders, probabilistic deletion laws,
and scope comparators.  The first two describe the arithmetic construction;
the third supplies the only positive-density indistinguishability class; the
last two delimit what a single path can and cannot refute.

The central candidate uses `m=floor(K/16)`, a path of `2m+1` vertices, edge
primes above `b^m`, and base-`b` padding.  It retains three quantities instead
of the earlier single `o(K)` estimate: rough-part height, one-digit rounding
loss, and balancing decrement.  The candidate comparison `s=floor(K/2)` is
deliberately tested with Bertrand alone; without a sharper prime theorem its
rough parts can consume the available exponent budget.

The cylinder representation is frozen independently of the constructed
edge.  It is not an alias for every local rule.  In particular, exact labels,
adaptive largest-prime residues, and global owner selection lie in the scope
comparator family and require a transversal packing argument that the present
construction does not supply.
