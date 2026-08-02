# Erdős #1083: dependency map for the signed-switch results

Date: 2026-08-02

Status: **BOUNDARY MAP — INDEPENDENT CROSS-AUDIT PASSED AFTER WORDING REPAIR**

## 0. Purpose

The three positive results proved in the current attack use different
extra hypotheses.  None subsumes the other two, and their conclusions
must not be combined outside the intersections displayed below.

The common starting datum is only

\[
 F_0R\text{ is a \(0/1\) mask},\qquad
 F_0(1)=S,\qquad 1\le R(1)=C<S,
\tag{0.1}
\]

with \(R\) allowed to be signed.

## 1. Proof-dependency graph

~~~text
                         common positive multiple (0.1)
                                      |
                 +--------------------+--------------------+
                 |                                         |
       centre has an exact                         full independent
       finite-quotient tile                       Phi_6 switch cube
                 |                                         |
                 v                                         v
     nonnegative shadow K of mass C             every nonempty switch
     preserving external divisors                fibre has mass >= 2^k
                 |                                         |
     +-----------+-----------+                  transverse F_0 and the
     |                       |                  ADDITIONAL hypothesis
 one-dimensional       arbitrary external                pi_W(H) >= 0
 cyclotomic ratios       divisor family                    |
     |                       |                              v
 sharp mass lemma        no count by itself               C >= 2^k
     |
 pairwise reduced ratios <= C
     |
 family size <= C^2

Failure boundary on the left: an aperiodic centre need not have a
finite-quotient shadow.

Failure boundary on the right: a strongly signed pi_W(H) is not
controlled by the fibre theorem.
~~~

There is now one proved intersection of the two branches:

~~~text
 binary-box centre + transverse independent Phi_6 leaf span
          |                         |
 tailored separating       Newton-zonotope mass
 finite shadow             for d retained factors
          +-------------+-----------+
                        v
       one-sided Hamming differences <= log_2 C
                        |
                        v
       endpoint family <= S^{H_2(1/7)}
                         = t^{0.4601899388...}
~~~

Unlike the fibre-only corollary, this derived binary-box theorem allows
the original quotient projection to remain signed.

## 2. Exact hypothesis ledger

| Result | Extra hypotheses beyond (0.1) | Conclusion | Hypotheses it does **not** remove |
|---|---|---|---|
| Cyclotomic quadratic bound | \(S\) prime; leaf factors are the reduced one-dimensional ratios \(H_{S,a}(y^g)=P_S(y^{ag})/P_S(y^g)\); the centre supplies a mass-\(C\) positive shadow preserving those factors | \(a,b\le C\) pairwise and \(|\mathcal D|\le1+2\sum_{r=2}^C\varphi(r)\le C^2\) | Does not show that arbitrary residual divisors are cyclotomic or one-dimensional |
| Finite-quotient shadow | \(\Gamma=\Gamma_0\oplus\Gamma_1\); the centre mask exactly tiles a finite quotient of \(\Gamma_0\); the factor to preserve lies in \(\mathbb Z[\Gamma_1]\) | A nonnegative external shadow \(K\), \(K(1)=C\), preserving every external divisor | Gives no family-size bound without a separate mass theorem; does not cover aperiodic centres |
| Transverse \(\Phi_6\)-fibre bound | \(k\) independent factors \(T_i=1-z_i+z_i^2\); **all** \(2^k\) subset states are masks; \(F_0\) is transverse to their span; **additionally** \(\pi_W(H)\ge0\) | Every switch fibre has mass at least \(2^k\), equality only for the binary box; globally \(C\ge2^k\) | Does not control signed \(\pi_W(H)\), arbitrary divisor subfamilies, or the common-\(X\) scalar-copy condition |
| Derived signed binary-box switch bound | The centre is a \(k\)-dimensional binary box; the leaf patterns use independent \(\Phi_6\) switches; centre and leaf spans are transverse | A tailored finite shadow handles signed quotients; pairwise one-sided Hamming distance is at most \(\log_2C\), and the endpoint family is at most \(S^{H_2(1/7)}\) | Does not reduce arbitrary \(X\) or arbitrary residual divisors to a binary \(\Phi_6\) model |

The word “additionally” in the transverse \(\Phi_6\)-fibre row is essential:
\(\pi_W(H)\ge0\) is not a consequence of exact-block positivity.

## 3. Non-overlap and sharp boundaries

### 3.1 Cyclotomic versus finite quotient

The finite-quotient theorem is a positivity-transfer engine, not a
counting theorem.  It becomes the \(C^2\) theorem only after the
one-dimensional cyclotomic factors and their sharp
\(\min\{S,a\}\)-mass bound are supplied.  Conversely, the cyclotomic
pairwise argument needs some positive shadow; for the interval centre
this is the prime cyclic shadow, and for a general finite tile it is the
finite-quotient theorem.

The identity

\[
 (1+x+x^4)(1-x^4+x^5+x^7)
 =1+x+x^6+x^7+x^9+x^{11}
\tag{3.1}
\]

shows that the shadow hypothesis cannot simply be deleted.  Its centre
has no torsion zero and no finite-quotient tiling, while the signed
quotient has augmentation \(2<3\).  This is one row, not a simultaneous
counterexample.

### 3.2 Finite quotient versus transverse fibres

The fibre theorem does not require the centre to tile any finite
quotient and does not use torsion characters.  It instead spends the
positivity of all \(2^k\) switch states.  The global inequality
\(C\ge2^k\) uses \(\pi_W(H)\ge0\); without that additional condition,
the \(S\) distinct projected centre terms can in principle cancel down
to few quotient fibres.

The finite-quotient theorem can sometimes rule out precisely such
cancellation, but only when the centre has the required exact finite
tiling and the switch factors are external to it.  The aperiodic escape
shows why this implication is unavailable in general.

The binary-box theorem is the sharp positive instance of this
interaction. A rational dual construction produces a quotient which
tiles the binary centre while killing the transverse leaf span, so the
external \(\Phi_6\) factors survive in the shadow. It therefore removes
the sign hypothesis \(\pi_W(H)\ge0\) for this model, but not for an
arbitrary aperiodic centre.

### 3.3 Fibre rigidity versus scalar-copy rigidity

The fibre theorem concerns the complement states
\(F_0H\prod_{i\in J}T_i\).  It does not make the corresponding source
masks scalar copies.  Independently, the mixed \(1/3\)-step tensor boxes
have homothety classes of size at most \(k+1\), sharply.  Therefore a
repair of the tensor barrier must pass two distinct tests:

1. centre--leaf transversality with strongly signed quotient projection;
2. a power-large common-\(X\) scalar-copy source family.

Neither test currently follows from the other.

For the binary-box \(\Phi_6\) model the two tests can now be imposed
together. In particular the genuine scalar-copy endpoints \(X\) and
\(3X\) force \(C\ge S\) and are excluded from the strict block. This is
a model-specific closure, not a structural reduction of general \(X\).

## 4. Exact remaining gate

After these results, the unresolved algebraic target can be stated
without conflating hypotheses:

> Bound a power-large complementary-divisor family for an aperiodic
> centre when every source is a scalar copy of one fixed \(X\), every
> centre--leaf pair is transverse, every switched complement is a mask,
> and the quotient projections may remain genuinely signed.

This is still a conditional exact-block target.  Stability from the
original near-extremal point configuration to the literal block is a
separate outer problem, and Erdős #1083 remains open.
