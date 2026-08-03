# Exact next-host census after W4

The independently audited rim and spoke certificates settle both edge orbits
of `W4`.  To avoid choosing the next symbolic host by familiarity, the
bounded checker enumerates the complete NetworkX atlas of unlabeled simple
graphs, keeps `4<=|V|<=6`, `7<=|E|<=9`, and tests vertex connectivity at
least three.  Edge orbits are then computed from every exact automorphism.

There are four hosts in this range.  The unique eight-edge host is `W4`,
which is also `K5` minus a two-edge matching.  Beyond it, exactly three
nine-edge hosts remain:

- `K5-e`, with edge-orbit sizes 3 and 6;
- `K3,3`, with one nine-edge orbit;
- the triangular prism, with edge-orbit sizes 3 and 6.

Thus `K5` is not the immediate next target.  `K3,3` is the cheapest exact
next symbolic attack because a single marked-edge orbit suffices; `K5-e`
and the prism each require two certificates or one proved good orbit.

This is a complete finite routing statement only for the displayed vertex
and edge range.  It neither proves domination on any of the three hosts nor
changes G201 or OPG-1757.

Reproduction uses at most 1 GiB and 60 seconds:

```sh
AMRA_MEMORY_KIB=1048576 AMRA_TIMEOUT_SECONDS=60 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  evidence/next_3connected_host_census.py
```
