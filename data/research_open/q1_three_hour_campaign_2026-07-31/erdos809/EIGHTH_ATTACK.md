# Erdős #809 — eighth attack: absorption failure versus residual moment

Date: 2026-07-31

Status:
ABSORPTION_TO_RESIDUAL_IMPLICATION_REFUTED_BY_FULL_CONTRACT_GRAPH__WEIGHTED_DEGREE_SUPPORT_CRITERION_PROVED

## 1. Outcome

The proposed implication
\[
\text{failure of the seventh-stage absorption certificate}
\quad\Longrightarrow\quad
\mathcal R_{\mathrm{opp}}
=o\!\left(nE_0^{\mathrm{opp}}\right)                         \tag{1}
\]
is false, even under the full fixed-\(s\) maximum-witness contract.

There is an infinite three-clique-chain family satisfying:

- \(e(G)=(1/4+s^2+o(1))n^2\) and \(e(G)>n^2/4\);
- \(\delta(G)=(1/2-s-o(1))n\);
- the exact BCM maximum-degree threshold;
- \(L_4(2)\);
- a coloring in which every \(C_7\) is rainbow;
- \(\zeta=0\) in the normalized maximum-degree notation;

but for which
\[
\frac{\mathcal R_{\mathrm{opp}}}
     {nE_0^{\mathrm{opp}}}
\longrightarrow 2s>0.                                      \tag{2}
\]
Both the high/low certificate and the more direct sufficient condition
\(R_A+E_0\le S_m\) fail on this family.

This does not refute the exact defect budget or Erdős #809. In fact,
\[
D_A=D_B=M_B,
\]
so the exact budget closes before any zero-shore excess estimate is
needed. The example proves that failure of a sufficient absorption
test is not evidence that a structural exit must occur.

A positive conditional result survives. If the weighted endpoints of
opposite zero pairs are concentrated at degree
\(n/2-o(n)\), then the residual moment is little-\(o\). A precise
low-degree-support inequality is proved in Section 3. Combined with the
seventh-stage theorem, it yields an aligned core. The newly isolated
gap is therefore to control weighted endpoint degree support in a
sequence that is genuinely hard for the exact \(M_B+S_m\) budget.

## 2. Three logically different notions of absorption

For an integer \(H\ge2\), put
\[
F_H=(H-1)M_B+\frac{2Q_A}{H}.                                \tag{3}
\]
The previous attacks proved
\[
E_0\le F_H,
\qquad
D_B\le M_B+E_0.                                             \tag{4}
\]
It is essential to distinguish the following statements.

1. **High/low certificate**
   \[
   R_A+F_H\le S_m
   \quad\text{for some }H.                                  \tag{5}
   \]
2. **Zero-shore sufficient test**
   \[
   R_A+E_0\le S_m.                                          \tag{6}
   \]
3. **Exact defect budget**
   \[
   D_A\le M_B+S_m.                                          \tag{7}
   \]

Equations (4) give only
\[
(5)\Longrightarrow(6)\Longrightarrow(7).                  \tag{8}
\]
Neither reverse implication follows. In particular, failure of (5)
does not imply failure of (6), and failure of (6) does not imply failure
of (7).

The graph family below has
\[
(7)\ \text{true},
\qquad
(6)\ \text{false},
\qquad
(5)\ \text{false for every }H.                             \tag{9}
\]
Thus any attempt to derive (1) from failure of (5), or even from failure
of (6), reverses a one-way upper-bound argument.

At the level of pure parameters, the obstruction is already visible:
\(R_A,M_B,Q_A,S_m\) contain no weighted endpoint-degree statistic.
That observation alone is not a graph counterexample. Sections 4--7
give a graph realization satisfying all known global hypotheses.

## 3. A conditional lemma that does imply small residual moment

Let \(\mathcal Z_{\mathrm{opp}}\) be the opposite-type zero-shore pairs
and set
\[
w_{bc}=(h_{bc}-1)_+,
\qquad
E_0^{\mathrm{opp}}
=\sum_{bc\in\mathcal Z_{\mathrm{opp}}}w_{bc}.                \tag{10}
\]
For each vertex \(v\), define its weighted opposite incidence
\[
\omega(v)
=
\sum_{\substack{bc\in\mathcal Z_{\mathrm{opp}}\\v\in\{b,c\}}}
w_{bc}.                                                      \tag{11}
\]
Then
\[
\sum_v\omega(v)=2E_0^{\mathrm{opp}}.                        \tag{12}
\]

### Lemma 3.1 (exact weighted degree-deficit identity)

\[
\boxed{
\mathcal R_{\mathrm{opp}}
=
nE_0^{\mathrm{opp}}-\sum_v\omega(v)d(v)
=
\sum_v\omega(v)\left(\frac n2-d(v)\right).
}                                                            \tag{13}
\]

#### Proof

Expand the definition
\[
\mathcal R_{\mathrm{opp}}
=
\sum_{bc}w_{bc}\bigl(n-d(b)-d(c)\bigr)
\]
and collect the two endpoint contributions. Equation (12) gives the
second form. \(\square\)

Thus the desired residual estimate is exactly weighted endpoint-degree
saturation:
\[
\mathcal R_{\mathrm{opp}}
=o\!\left(nE_0^{\mathrm{opp}}\right)
\quad\Longleftrightarrow\quad
\sum_v\omega(v)d(v)
=
\left(1-o(1)\right)nE_0^{\mathrm{opp}}.                     \tag{14}
\]

The following one-sided criterion is easier to apply.

### Lemma 3.2 (low-degree-support bound)

Fix \(\varepsilon>0\), and put
\[
L_\varepsilon
=
\left\{
v:d(v)<\left(\frac12-\varepsilon\right)n
\right\},
\qquad
\Omega_\varepsilon
=
\sum_{v\in L_\varepsilon}\omega(v).                         \tag{15}
\]
With \(\kappa=n-2\delta\),
\[
\boxed{
\mathcal R_{\mathrm{opp}}
\le
2\varepsilon nE_0^{\mathrm{opp}}
+\kappa\Omega_\varepsilon.
}                                                            \tag{16}
\]

#### Proof

Split the weighted opposite pairs into those touching
\(L_\varepsilon\) and those avoiding it.

If \(bc\) avoids \(L_\varepsilon\), then
\[
\rho(b,c)
=n-d(b)-d(c)
\le2\varepsilon n.
\]
The total contribution of these pairs is at most
\(2\varepsilon nE_0^{\mathrm{opp}}\).

Every opposite pair satisfies
\[
\rho(b,c)\le n-2\delta=\kappa.
\]
The total weight of pairs touching \(L_\varepsilon\) is at most
\(\Omega_\varepsilon\), because each such pair contributes its weight
to at least one endpoint incidence in (15). This proves (16).
\(\square\)

### Corollary 3.3 (degree-supported aligned core)

Suppose \(\varepsilon_n=o(1)\),
\[
\Omega_{\varepsilon_n}
=o\!\left(E_0^{\mathrm{opp}}\right),                         \tag{17}
\]
and \(E_0^{\mathrm{opp}}>0\). Then
\[
\mathcal R_{\mathrm{opp}}
=o\!\left(nE_0^{\mathrm{opp}}\right).                        \tag{18}
\]
If additionally \(\zeta=o(1)\), Corollary 6.1 of
SEVENTH_ATTACK.md gives an aligned
\((1/2+s-o(1))n\)-vertex core with \(o(n^2)\) missing edges.

The counterfamily below violates (17) maximally: all weighted opposite
endpoints have degree \((1/2-s+o(1))n\).

## 4. Full graph realization

Take disjoint sets
\[
U,X,W,Y,H,
\qquad
|U|=|X|=|W|=|Y|=k,
\qquad
|H|=r.
\]
Make each of
\[
C_1=U\cup X,
\qquad
C_2=W\cup Y,
\qquad
H
\]
a clique. Add all \(H\)--\(X\) and \(H\)--\(Y\) edges, and no other
edges.

Thus
\[
n=4k+r
\]
and
\[
\begin{aligned}
e(G)
&=
2\binom{2k}{2}+\binom r2+2kr\\
&=
\frac{n^2}{4}+\frac{r^2}{4}-\frac n2.                      \tag{19}
\end{aligned}
\]
Set
\[
s=\frac{r}{2n}.
\]
Along any fixed-ratio sequence with \(k,r\to\infty\),
\[
e(G)
=
\left(\frac14+s^2\right)n^2-\frac n2
=
\left(\frac14+s^2+o(1)\right)n^2.                           \tag{20}
\]
For fixed \(s>0\), (20) exceeds \(n^2/4\) for all sufficiently large
\(n\).

The degrees on \(U,W\) and on \(X,Y,H\), respectively, are
\[
2k-1,
\qquad
2k+r-1.
\]
Consequently
\[
\delta
=
\left(\frac12-s\right)n-1,
\qquad
\Delta
=
\left(\frac12+s\right)n-1.                                 \tag{21}
\]

Fix \(v\in H\). Its closed neighbourhood is
\[
A=N[v]=H\cup X\cup Y,
\qquad
B=U\cup W,                                                  \tag{22}
\]
and
\[
|A|=2k+r=\Delta+1.
\]
Moreover,
\[
e-\frac{n^2}{4}+\frac n2=\frac{r^2}{4},
\]
so the BCM threshold is exactly
\[
\frac n2+
\sqrt{e-\frac{n^2}{4}+\frac n2}
=
\frac n2+\frac r2
=
2k+r
=
|A|.                                                        \tag{23}
\]
Thus (22) is an exact maximum-degree BCM witness, not merely an
asymptotically admissible set.

## 5. The robust exact-four-path property

For sufficiently large \(k,r\), the graph has \(L_4(2)\). Let at most
two vertices be deleted, with the two path endpoints retained.

- Two endpoints in the same one of \(C_1,C_2,H\) are joined by an
  exact four-edge path using three fresh vertices in that clique.
- For \(a\in C_1\) and \(h\in H\), choose fresh
  \(a_1,a_2\in C_1\) and \(x\in X\); then
  \[
  a-a_1-a_2-x-h
  \]
  is an exact four-edge path. The \(C_2\)--\(H\) case is symmetric.
- For \(a\in C_1\) and \(b\in C_2\), choose fresh
  \(x\in X\), \(h\in H\), and \(y\in Y\); then
  \[
  a-x-h-y-b
  \]
  is an exact four-edge path.

All choices can avoid two deleted vertices once the five groups are
large. The finite verifier independently checks the equivalent
path-hypergraph transversal condition on all endpoint pairs.

## 6. Rainbow-\(C_7\) coloring

Match \(U\) bijectively with \(W\). For every
\(u_i\in U\), its matched \(w_i\in W\), and every
\(1\le j\le k\), give
\[
u_i x_j
\qquad\text{and}\qquad
w_i y_j                                                     \tag{24}
\]
one common new color. Give every remaining edge a fresh color.

Each pair in (24) is an induced matching. No \(C_7\) contains both
edges. Indeed, \(H\) separates \(C_1\) from \(C_2\). A cycle using both
specified edges needs two passages between \(C_1\) and \(C_2\), each of
length at least two. Its \(C_1\)-arc containing \(u_ix_j\) has length at
least two because \(u_i\) has no neighbour in \(H\); the corresponding
\(C_2\)-arc has length at least two for the same reason at \(w_i\).
The cycle therefore has length at least
\[
2+2+2+2=8.
\]
Hence every \(C_7\) is rainbow.

## 7. Exact obstruction calculations

For every matched pair \(u_iw_i\),
\[
N(u_i)\cap N(w_i)=\varnothing,
\qquad
E\bigl(N(u_i),N(w_i)\bigr)=\varnothing.
\]
It is an opposite zero-shore pair with
\[
h_{u_iw_i}=k
\]
and
\[
\rho(u_i,w_i)
=
n-2(2k-1)
=
r+2.                                                        \tag{25}
\]
There are \(k\) such weighted pairs. Therefore
\[
E_0^{\mathrm{opp}}
=E_0
=
k(k-1),                                                     \tag{26}
\]
and
\[
\mathcal R_{\mathrm{opp}}
=
(r+2)k(k-1).                                                \tag{27}
\]
It follows that
\[
\frac{\mathcal R_{\mathrm{opp}}}
     {nE_0^{\mathrm{opp}}}
=
\frac{r+2}{n}
\longrightarrow
\frac rn
=2s.                                                        \tag{28}
\]
This proves the failure of (1).

For the witness (22), the only missing edges in \(A\) are \(X\times Y\),
and the only missing edges in \(B\) are \(U\times W\). Thus
\[
M_A=M_B=k^2.                                                \tag{29}
\]
Every \(x\in X\) and \(y\in Y\) has \(B\)-degree \(k\), so
\[
Q_A
=
\sum_{xy\in X\times Y}d_B(x)d_B(y)
=
k^4.                                                        \tag{30}
\]
The \(k^2\) repeated color classes in (24) each contribute one defect.
Both outer endpoints lie in \(B\), giving
\[
D_A=D_B=k^2,
\qquad
R_A=0.                                                      \tag{31}
\]

At the exact BCM size scale,
\[
S_m
=
e-\binom{|B|}{2}-\Phi(n,e)
=
\left(\frac{1-4s^2}{8s}+o(1)\right)n
=o(n^2).                                                    \tag{32}
\]
Equations (26) and (32) show
\[
R_A+E_0>S_m
\]
for all sufficiently large members of the family. Thus the direct
zero-shore sufficient test (6) fails.

For the high/low certificate,
\[
F_H
=(H-1)k^2+\frac{2k^4}{H}.
\]
Minimizing over positive real \(H\) gives
\[
F_H\ge2\sqrt2\,k^3-k^2=\Theta(n^3),                         \tag{33}
\]
so (5) fails by an even larger margin.

Nevertheless, (29) and (31) give
\[
D_A=M_B\le M_B+S_m.                                        \tag{34}
\]
The exact budget closes. The total number of colors is
\[
e-k^2
=
\left(
T(s)+\frac{(1/2-s)^2}{4}+o(1)
\right)n^2,
\]
strictly above the BCM target. Therefore the construction is not a
counterexample to Erdős #809.

The mechanism is now explicit: \(Q_A\) is of order \(n^4\), making the
high/low upper bound useless, while the unused global supply of missing
\(B\)-pairs makes \(M_B\) large enough to pay the true defect directly.
The zero-shore excess \(E_0\) is a local-congestion overcharge in this
family.

## 8. Correctly localized remaining question

The eighth-stage countermodel eliminates the route
\[
\text{failure of a sufficient upper-bound certificate}
\Longrightarrow
\text{small residual moment}.
\]
A viable next statement must first impose genuine hardness for the
exact budget, for example a positive gap in
\[
D_A-(M_B+S_m),
\]
or an equivalent Hall-type deficiency for charging actual defect tokens
to missing \(B\)-pairs. It must then control the weighted low-degree
incidence \(\Omega_\varepsilon\) from Lemma 3.2, or supply a different
compatible-family exit.

It remains open whether a genuinely hard maximum-witness sequence
forces one of:

1. \(\Omega_{\varepsilon_n}=o(E_0^{\mathrm{opp}})\) for some
   \(\varepsilon_n=o(1)\), hence an aligned opposite core;
2. a synchronized same-neighbourhood core;
3. a direct \(C_7\)-compatible family large enough to close the color
   bound.

The present family does not test that stronger statement because its
exact defect is already paid by \(M_B\).

## 9. Finite verification

The verifier verify_809_eighth_attack.py uses
\[
(k,r)=(6,16),
\qquad
n=40.
\]
It checks:

1. \(e=444>400=n^2/4\), \(\delta=11\), and \(\Delta=27\);
2. \(|A|=28\), exactly equal to the BCM threshold;
3. all 780 endpoint pairs for \(L_4(2)\), equivalent to 578,760
   endpoint/deletion checks;
4. all 36 repeated color pairs are induced and lie on no common
   \(C_7\);
5. \(D_A=D_B=M_B=36\), \(R_A=0\), \(Q_A=1296\), and
   \(S_m=23.335\ldots\);
6. \(E_0^{\mathrm{opp}}=30\),
   \(\mathcal R_{\mathrm{opp}}=540\), and
   \(\mathcal R_{\mathrm{opp}}/(nE_0^{\mathrm{opp}})=0.45\);
7. the best finite high/low bound is \(576>S_m\), while the exact
   budget closes;
8. the exact weighted endpoint identity (13) and the finite
   low-degree-support inequality (16).

The command

    python3 -m unittest -v test_809_eighth_attack.py

returns

    Ran 4 tests
    OK

## 10. Claim boundary

- Implication (1) from high/low certificate failure: **false**.
- The same implication from failure of \(R_A+E_0\le S_m\): **false**.
- Exact weighted degree-deficit identity (13): **proved**.
- Low-degree-support bound (16): **proved**.
- Conditional aligned core under (17) and \(\zeta=o(1)\): **proved**.
- Three-clique-chain full-contract graph and coloring: **proved**.
- Exact defect budget on that graph: **holds; not a counterexample**.
- Small residual moment from genuine exact-budget hardness: **open**.
- Maximum-degree Case 1 and Erdős #809: **open / not claimed**.
