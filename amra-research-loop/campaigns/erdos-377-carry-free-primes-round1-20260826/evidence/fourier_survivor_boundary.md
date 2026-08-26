# Boundary of the mixed-modulus Fourier survivor

For an odd modulus `q`, let `H_q={0,...,(q-1)/2}`.  Its unnormalised Fourier
coefficient at frequency `r` is a geometric sum, hence

    |hat(1_Hq)(r)|
      = |sin(pi r |H_q|/q) / sin(pi r/q)|.

Consequently the normalised Fourier `l1` norm is of order `log q`.  For coprime
prime-power moduli the CRT indicator is a tensor product, so these `l1` norms
multiply.  A pointwise estimate obtained by expanding every lower-half
indicator and taking absolute values therefore becomes worse, not better, as
more prime bases are included.

This does not refute M377-07 outright: a new inequality could exploit
cancellation between frequencies or a large-sieve average tied to the global
cutoff.  It sharply limits the survivor, however.  It must be pointwise in the
fixed integer `n`, must retain phase cancellation, and cannot tensorise by
Fourier `l1` norm or by full-period CRT independence.  No such inequality was
proved in this round.
