# Erdős Problem #598 — independent evidence audit

## Verdict

`verified_closed`

Closure mode: **relative independence**, with the consistency strength of the
negative side not known exactly.

More precisely:

1. If \(0^\sharp\) does not exist—in particular in \(V=L\)—the answer is
   yes for every infinite \(m\).
2. Assuming an \(I1\) rank-into-rank hypothesis, Garti–Hayut's published
   forcing results yield a model in which the answer is no for some \(m\).

Thus the universal assertion is independent of ZFC relative to the consistency
of \(I1\).  The known lower bound for a counterexample is the existence of
\(0^\sharp\); the exact consistency strength between \(0^\sharp\) and \(I1\)
remains open.

## Formal statement

Put \(\kappa=(2^{\aleph_0})^+\), and write

\[
\operatorname{Col}_\omega(m,\kappa)
\quad\Longleftrightarrow\quad
\exists c:[m]^\omega\to\kappa\
\forall X\in[m]^\kappa\
c``[X]^\omega=\kappa.
\]

In partition notation this is
\(m\nrightarrow[\kappa]^\omega_\kappa\).  Problem #598 asks whether
\(\operatorname{Col}_\omega(m,\kappa)\) holds for every \(m\) (the case
\(m<\kappa\) is vacuous).

## Negative model: Garti–Hayut and the bounded-to-full transfer

### Fixed primary results

The following are the exact published/preprint statements used.

- Garti–Hayut, *Magidor cardinals*, Claim 1.3(d), proves
  \(2^{\aleph_0}<\alpha_M(\lambda)\) for every Magidor cardinal
  \(\lambda\).  Corollary 1.6 restates the resulting continuum
  consequence.  Theorem 1.4 proves that Magidor cardinals are Jónsson.
- Garti–Hayut, *The first omitting cardinal for Magidority*, Claim
  1.10(a), proves, from suitable large cardinals, that for every successor
  ordinal \(\beta\) it is consistent that a Magidor \(\lambda\) has
  \(\alpha_M(\lambda)=\aleph_{\beta+1}\).  Its proof explicitly starts
  from an \(I1(\rho,\lambda)\) instance.  Taking \(\beta=1\) gives
  \(\alpha_M(\lambda)=\aleph_2\).

In that forcing extension, Claim 1.3(d) gives
\(\mathfrak c<\aleph_2\).  Cantor's theorem gives
\(\mathfrak c\ge\aleph_1\), so

\[
\mathfrak c=\aleph_1,\qquad
\kappa=\mathfrak c^+=\aleph_2=\alpha_M(\lambda).
\]

The April 2026 secondary note cites “Claim 1.3(c)” for this inequality.
That letter is wrong: part (c) is \(\alpha_J\le\alpha_M\); the required
continuum inequality is Claim 1.3(d).  The primary theorem nevertheless
supplies exactly the needed fact.

### Bounded obstruction, checked

By the definition of \(\alpha_M(\lambda)\),

\[
\lambda\rightarrow[\lambda]^{\omega\text{-bd}}_\kappa.
\]

Let \(c:[\lambda]^\omega\to\kappa\) be arbitrary.  Restrict \(c\) to the
bounded countable subsets.  The displayed relation supplies
\(A\in[\lambda]^\lambda\) and \(\xi<\kappa\) such that \(\xi\) is absent
on every bounded countable subset of \(A\).

A Magidor cardinal has cofinality \(\omega\).  More generally, if
\(\operatorname{cf}(\lambda)<\kappa\), \(\kappa\) is regular, and
\(|A|=\lambda\), then some bounded initial segment of \(A\) has size at
least \(\kappa\): otherwise a union of
\(\operatorname{cf}(\lambda)<\kappa\) many sets of size \(<\kappa\)
would have size \(<\kappa\), contradicting \(|A|=\lambda\).
Choose \(X\) of size \(\kappa\) in that bounded segment.  Every
countable subset of \(X\) is bounded in \(\lambda\), so all of them omit
\(\xi\).  Hence

\[
\lambda\rightarrow[\kappa]^\omega_\kappa,
\]

which is exactly \(\neg\operatorname{Col}_\omega(\lambda,\kappa)\).
This verifies the passage from Garti–Hayut's
\(\omega\)-bounded relation to the problem's unrestricted countable
subsets; simply dropping “bd” without this bounded-\(\kappa\)-set
argument would not be valid.

One bad \(m=\lambda\) refutes the problem's universal assertion.

## Positive model: the \(V=L\)/\(0^\sharp\) direction

The recent MathOverflow proof can be made into the following exact
contrapositive:

\[
\exists\lambda\ge\kappa>\aleph_0\
\bigl(\lambda\rightarrow[\kappa]^\omega_\kappa\bigr)
\quad\Longrightarrow\quad
0^\sharp\text{ exists}.
\]

The steps were independently checked.

### Countable exponent to finite exponent

For an arbitrary \(g:[\lambda]^{<\omega}\to\kappa\), define a colouring
of countable sets by using sets of order type \(\omega+n\): on such a
set take \(g\) of its last \(n\) elements, and give all other order
types a default value.  If a \(\kappa\)-set \(X\) omits a colour for
this countable colouring, remove its first \(\omega\) elements.
Every finite subset of the remaining \(\kappa\)-set can be extended
downwards to a countable subset of order type \(\omega+n\).  Hence the
same colour is omitted by \(g\).  Therefore

\[
\lambda\rightarrow[\kappa]^\omega_\kappa
\Longrightarrow
\lambda\rightarrow[\kappa]^{<\omega}_\kappa.
\]

Uncountability of \(\kappa\) is used when the first countably many
elements are removed.

### Elementary submodel and condensation

The standard model-theoretic form of the finite relation says that for
every countable-language structure \(M\) of size \(\lambda\), with a
unary predicate \(P\) of size \(\kappa\), there is
\(N\prec M\) of size \(\kappa\) with \(N\cap P\ne P\).  This direction
can also be seen directly: Skolemize the structure, identify \(P\) with
the colours, and use finite dummy points to encode all the countably
many Skolem operations into one finite-set colouring.  A set omitting
one colour generates a Skolem hull still omitting the corresponding
element of \(P\).

Apply this to \(M=(L_\lambda,\in,\kappa,\ldots)\) and \(P=\kappa\).
By condensation, the transitive collapse of \(N\) is \(L_\alpha\) for
some \(\alpha\) with \(|\alpha|=\kappa\).  The inverse collapse is an
elementary embedding

\[
j:L_\alpha\longrightarrow L_\lambda.
\]

Since \(N\cap\kappa\ne\kappa\), \(j\) has a critical point
\(\gamma<\kappa=|\alpha|\).

Jech, *Set Theory*, Theorem 18.27 states exactly: if
\(j:L_\alpha\to L_\beta\) is elementary with critical point \(\gamma\)
and \(\gamma<|\alpha|\), then \(0^\sharp\) exists.  It applies with no
missing size hypothesis.  Consequently, if \(0^\sharp\) does not exist,
then \(m\nrightarrow[\kappa]^\omega_\kappa\) for every
\(m\ge\kappa\).  In particular \(V=L\) satisfies the affirmative answer
to #598 for all \(m\).

## What is and is not formalized

The public `Erdos598.lean` file formalizes combinatorial portions of the
secondary note, but its forcing-extension theorem is literally

```lean
theorem threshold_model_description : True := trivial
```

and is described in the file as documentation.  It is not a Lean proof
of the relative-consistency result and was not used as closure evidence.

## Evidence assessment

- The load-bearing forcing and Magidor facts are in published
  Garti–Hayut papers.
- The bounded-to-full relation is a short ZFC argument and is valid with
  all cardinal/cofinality hypotheses present.
- The \(0^\sharp\) endpoint is the exact fixed statement of Jech
  Theorem 18.27; its hypotheses match the collapse embedding.
- The secondary note contains a citation-letter typo and the Lean
  artifact does not formalize forcing, but neither defect breaks the
  mathematical proof.
- What remains open is the exact consistency strength of the negative
  relation, not the relative-independence conclusion above.

## Timing

- Start: `2026-07-23T19:39:06+08:00`
- End: `2026-07-23T19:47:16+08:00`
- Active agent time: `490 s = 0.136111 agent-hours`
- Budget ceiling: `1 agent-hour`

