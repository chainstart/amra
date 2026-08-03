# K4 disjoint-pair complete-channel certificate

Exact symbolic forest enumeration for marked edges `01,23` and remaining
activities

```text
a=x_02, b=x_03, c=x_12, d=x_13
```

gives

\[
\Delta=a^2d^2+a^2d-2abcd+ad^2+ad+b^2c^2+b^2c+bc^2+bc.
\]

Although the coefficient of `abcd` is `-2`, the complete expression is

\[
\Delta=(ad-bc)^2+ad(a+d+1)+bc(b+c+1)\ge0.
\]

The identity and its nonnegative-activity consequence are checked in
`opg_k4_complete_channel_probe.lean` using `ring` and `positivity` under the
campaign's bounded Lean runner.

This kills coefficientwise and fiber-preserving transport mechanisms while
supporting a moving complete-Gram/SOS representation: the two perfect
matching monomials must share one quadratic channel.  It proves only one
finite host/orbit and does not change OPG-1757.

The shape is consistent with the positive-semidefinite
`alpha-beta-gamma` ansatz proposed in Nguyen--Pylyavskyy,
https://arxiv.org/abs/2507.09520, especially their K4 example.  Novelty is
not claimed.
