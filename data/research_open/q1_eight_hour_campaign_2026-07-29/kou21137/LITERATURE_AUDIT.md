# KOU-21.137 literature and priority audit

Search date: 2026-07-29--30

## Method and limitation

The search used exact-title/DOI lookup, arXiv full text, publisher pages, and
targeted phrase combinations around:

- `"KOU-21.137"` and `"Kourovka 21.137"`;
- `"set of squares" subgroup wreath product`;
- `"power-closed" Camina group`;
- `"weakly power closed" wreath product`;
- `semi-extraspecial squares wreath product`;
- `extraspecial "set of squares"`;
- `powers in wreath products finite groups`.

OpenAlex-style broad discovery was also attempted, but its results for the
exact problem were largely irrelevant; exact web and source-text searches were
more informative.  This is a serious preliminary audit, not a substitute for
MathSciNet and zbMATH searches by a group theorist with institutional access.
Accordingly, the conclusions below use “not identified” rather than “does not
exist.”

An authorized-full-text preflight on 2026-07-30 found no configured local
library-resource entry and no reusable authenticated Chrome control session.
The Bennett repository labels its download `Campus Only`, and the Mann
publisher page did not expose authorized full text in the current session.
No access control was bypassed.  These sources therefore remain genuine
pre-submission blockers rather than failed keyword searches.

## Priority-critical sources

### 1. The explicit \(D_8\wr C_2\) counterexample is already public

Elias Judin's public gist,
[“Kourovka Notebook Problem 21.137 Lean proof”](https://gist.github.com/eliasjudin/3e74b54004d82cb86651a14ecf082463),
was created on 2026-04-14.  It explicitly states that the answer is no and
constructs
\[
  D_8\wr C_2
\]
of order 128 and exponent 8, with a nonabelian subgroup of square values.

Priority consequence: AMRA must not claim discovery of this individual
counterexample.  A manuscript must cite it as prior public work, even if a
referee later decides that a gist is not a formal publication.

A final date-sensitive check inspected van Doorn, Judin, Monticone, and
Morrison,
[“On Some Problems from the Kourovka Notebook”](https://arxiv.org/abs/2607.17477)
(submitted 2026-07-20).  That agent-discovery paper treats Problems 3.46,
18.50, 19.25, 20.125, 21.8, 21.24, 21.147, and 21.150; it does not include
Problem 21.137.  It therefore does not supersede the separate April gist or
the candidate general theorems here.  This is only a current-paper check,
not a replacement for the blocked historical-source audits.

### 2. General powers in wreath products have already been characterized

R. Kundu and S. Mondal,
[“Powers in wreath products of finite groups”](https://arxiv.org/abs/2010.04954),
*Journal of Group Theory* **25** (2022), 941–964,
[doi:10.1515/jgth-2021-0057](https://www.degruyterbrill.com/document/doi/10.1515/jgth-2021-0057/html),
characterize prime-power elements in \(G\wr S_n\) using conjugacy-class cycle
data (Proposition 4.3 in the published numbering).

Priority consequence: the elementary formula
\[
  \operatorname{Sq}(A\wr C_2)
  =(\operatorname{Sq}(A)\times\operatorname{Sq}(A))
   \cup\{(x,y):x\sim_A y\}
\]
should be presented as a direct specialization/computation compatible with
their general theory, not as the first computation of powers in a wreath
product.

The same caution applies to the later odd-prime formula
\[
  P_p(A\wr C_p)
    =P_p(A)^p\cup\bigcup_{C\in\mathcal C(A)}C^p.
\]
Its direct prefix-product proof is useful, but the formula itself is a
specialization of the established wreath cycle-data framework.  The
potentially publishable contribution is instead the conjugacy-class moment
obstruction showing that, when
\(P_p(A)\leq Z(A)\cap A'\) is a proper subgroup of \(A'\), neither the
value set nor its diagonal-\(P_p(A)\) quotient can be closed.  No priority
claim is made for this obstruction until a citation-chain search from
Kundu--Mondal and the power-value-subgroup literature is completed.

The candidate new step is instead the subgroup-closure theorem:
the displayed union is a subgroup exactly when the seed's square-value set
\(P\) is a subgroup and every nontrivial \(P\)-coset is a conjugacy class.
No statement of that exact closure criterion was identified in the searched
sources.

A narrow citation-chain check around Kundu--Mondal also inspected the full
official arXiv source of S. Panja and A. Singh,
[“Powers in finite groups”](https://arxiv.org/abs/2411.07017).  All five
source files (550 lines in total) were searched for `wreath`, `Camina`,
`semi-extraspecial`, `subgroup`, `closed`, `closure`, and power-value/word-map
variants.  The sole occurrence of `wreath` is one sentence in the finite
groups section: it points to Kundu--Mondal for results of a similar flavor
after discussing enumeration of roots in symmetric groups.  The remainder
of that section concerns conjugacy-class tests, generating functions, and
root proportions in classical groups.  There is no Camina condition,
semi-extraspecial group, power-value subgroup-closure criterion, or
classification of wreath seeds.  The incidental occurrences of `subgroup`
refer to unrelated standard notions.

Thus this survey does not cover the present closure theorem.  It does,
however, confirm that Kundu--Mondal is the obvious prior source that a
referee will expect to see.  Semantic Scholar displayed three citations for
the Kundu--Mondal DOI whereas OpenAlex displayed none, so the citation chain
is demonstrably incomplete.  The correct conclusion is only that no
covering result was found in this narrow chain, not that none exists.

### 3. General square-value subgroups have prior structural theory

M. W. Liebeck and A. Shalev,
[“Powers in finite groups and a criterion for solubility”](https://doi.org/10.1090/S0002-9939-2013-11790-9),
*Proceedings of the American Mathematical Society* **141** (2013),
4179–4189, study
\[
  G^{[k]}=\{g^k:g\in G\}
\]
for general finite groups.  Their author-hosted full text was inspected.
Theorem 3 proves that when \(G^{[2]}\) is a subgroup, the nonabelian
composition factors of \(G\) belong to a short specified list.

This result must be cited as general prior theory.  It does not subsume the
present 2-group problem: a finite 2-group has no nonabelian composition
factor, whereas KOU-21.137 asks whether the square-value subgroup inside such
a group can itself be nonabelian.  It also does not give the wreath
if-and-only-if criterion or the minimum-order classification.

### 4. Bennett's thesis is directly on the set-of-powers question

C. A. Bennett,
[“The Set of Powers in a Group”](https://bearworks.missouristate.edu/theses/1643/),
MSc thesis, Missouri State University, 2012, BearWorks item 1643.
The repository abstract explicitly says that the thesis studies when the set
of \(n\)-th powers is a subgroup and gives sufficient conditions involving
nilpotency.  The PDF endpoint redirected this session to a subscription
login, so the theorem statements and examples could not be inspected
lawfully.

Because its stated subject directly contains the present closure question,
the authorized full thesis is a second **pre-submission blocker**.  No
non-overlap claim should be made from the abstract alone.

### 5. Kappe and Mendoza give earlier minimal nonclosure data

L.-C. Kappe,
[“Variations on a Theme of Desmond MacHale”](https://www.irishmathsoc.org/bull56/GiG5608.pdf),
*Irish Mathematical Society Bulletin* **56** (2005), 87--94, was inspected
in open full text after the browser PDF endpoint timed out and the same URL
was fetched directly.

On pp. 90--91 Kappe defines
\[
  G(n)=\{x^n:x\in G\},\qquad G_n=\langle G(n)\rangle,
\]
introduces the minimal nonclosure order \(\mu(n)\), reports Mendoza's 2004
thesis results for \(\mu(n)\), and gives GAP counts for 2-groups of orders
\(16,32,64,128,256\) whose \(n\)-th powers are not closed for
\(n=2,4,8,16\).  For \(n=2\), the displayed nonclosure counts are
\(2,16,127,1391,27290\).

This is direct prior background for computational power-value closure and
must be cited.  It does not state the present wreath criterion, classify
closed-but-nonabelian square subgroups, or connect closure to Camina and
semi-extraspecial groups.  It therefore narrows the novelty claim without
covering the structural results.

The later full treatment is L.-C. Kappe and G. Mendoza,
“Groups of minimal order which are not \(n\)-power closed,”
*Contemporary Mathematics* **511** (2010), 93--107,
[doi:10.1090/conm/511/10044](https://doi.org/10.1090/conm/511/10044).
Its stated scope is the minimum order at which
\(G(n)=\{g^n:g\in G\}\) fails to equal the subgroup it generates (for the
covered values of \(n\)).  The available author slides and later
paper-level citations explicitly identify this as a classification of
minimal **nonclosure** counterexamples.  That problem is complementary to,
but logically different from, KOU-21.137: here the value set is assumed
closed and the question is whether the resulting subgroup must be powerful
or abelian.  A final manuscript should cite the 2010 paper for terminology
and the computational/minimal-order history, without presenting it as a
source for the new closed-but-nonpowerful classification.

### 6. Kappe--Ying (1992) already contain a cyclic-wreath power-closed example

L.-C. Kappe and J. H. Ying,
[“On exact power margin groups”](https://www.numdam.org/item/RSMUP_1992__87__245_0/),
*Rendiconti del Seminario Matematico della Università di Padova* **87**
(1992), 245--265, MR 1183910, was inspected in open full text.

Their Definition 2.1 calls a group \(n\)-power closed when its raw set of
\(n\)-th powers equals the subgroup generated by those powers, and
Definition 2.3 calls it power closed when this holds for every \(n\).
Thus this is directly the value-set closure terminology relevant here, not
merely the stronger modern section-wise convention.  The paper develops its
relation to exponent closure, semi-\(n\)-abelian groups, and exact power
margins.

Most importantly, Example 6.4 explicitly says that its group \(K\) is
isomorphic to
\[
  C_p\wr C_p
\]
and proves (for the odd-prime construction in that part of the paper) that
\(K\) is power closed but not exponent closed.  In the notation of the
present theorem this is the abelian seed \(A=C_p\), for which the raw
\(p\)-th powers are the diagonal \(C_p\).  Therefore neither this individual
positive wreath family nor the observation that its power values close can
be claimed as new.

The paper does not state an arbitrary-seed formula or an if-and-only-if
criterion for \(P_p(A\wr C_p)\), and its sole wreath occurrence is the
cyclic-by-cyclic example.  It does not discuss Camina or semi-extraspecial
seeds, closed nonabelian square-value subgroups, KOU-21.137, or the ten
order-128 lifts.  The candidate novelty is consequently the general closure
criterion and classification, not the first power-closed wreath product.

The OpenAlex citation record for Kappe--Ying listed two citing papers, both
of which were followed through in full text.

- Kappe, Mazur, Mendoza and Ward,
  [“On minimal non-\(p\)-closed groups and related properties”](https://people.wou.edu/~wardm/KMMW%20final%20version%20for%20Web.pdf),
  *Publicationes Mathematicae Debrecen* **78** (2011), 219--233,
  doi:10.5486/PMD.2011.4779, distinguishes \(n\)-power closure from
  \(n\)-exponent closure and points to the minimum-nonclosure literature.
  Its \(C_p\wr C_p\) discussion concerns the different property that
  elements of order dividing \(p\) fail to form a subgroup.
- Sankari and Abobala,
  [“On a New Criterion for the Solvability of Non-Simple Finite Groups and
  \(m\)-Abelian Solvability”](https://doi.org/10.1155/2021/5583128),
  *Journal of Mathematics* (2021), Article 5583128, uses the same raw
  \(m\)-power closure property under the name “exponent type \(m\)” to give
  solvability criteria.  It cites the authors' short 2020 paper
  “A Contribution to \(m\)-Power Closed Groups.”  Full-text searches of
  both papers found no wreath, Camina, semi-extraspecial, or arbitrary-seed
  closure theorem.

This citation-chain check is narrow: OpenAlex reports only two citations
and does not index every mathematical reference.  It materially improves
the audit but does not replace MathSciNet/zbMATH forward citation searches.

### 7. Chuah (2021) is direct square-subgroup background, not a wreath result

H. Chuah,
[“On Groups whose Squares are Subgroups”](https://www.maths.tcd.ie/pub/ims/bull88/wef/Classroom/Chuah/Chuah-wef.pdf),
*Irish Mathematical Society Bulletin* **88** (Winter 2021), 69--77,
[doi:10.33232/BIMS.0088.69.77](https://doi.org/10.33232/BIMS.0088.69.77),
was inspected in full.

The paper studies exactly the single-group property that
\[
  G^{[2]}=\{g^2:g\in G\}
\]
is a subgroup.  Among its results, it proves that this property implies
\(G'\subseteq G^{[2]}\), classifies the orders \(n\) for which every group of
order \(n\) has the property, identifies order 12 as the smallest
nonclosure order and order 16 as the smallest 2-group nonclosure order, and
classifies the dicyclic examples.  Its references also point directly to
Sun (1980), Haugh--MacHale (1997), and the earlier terminology around sets of
squares.

This is mandatory background for any manuscript about KOU-21.137.  A
full-text search and theorem-by-theorem inspection found no wreath product,
Camina group, semi-extraspecial group, cyclic-prime wreath closure criterion,
minimum closed-but-nonabelian square subgroup, or classification of the ten
order-128 lifts.  The paper's minimal-order statements concern groups whose
square sets are **not** closed, whereas KOU-21.137 assumes closure and asks
whether that subgroup can be nonabelian.  It therefore narrows the novelty
language but does not cover the present main theorems.

## Power-structure context

### Terminology firewall

The literature does not use `power-closed` uniformly.  To prevent a
terminological shortcut from becoming a false novelty claim, this project
separates the following three quantified properties.  For a finite
\(p\)-group \(G\), write
\[
  V_{p^k}(G)=\{g^{p^k}:g\in G\}.
\]

1. **Single-group square closure**:
   \(V_2(G)\) is a subgroup.  This is the property used in the 2-primary part
   of KOU-21.137 and in the present wreath theorem.
2. **Weak power closure in one group**, in the terminology used by Flake and
   Thevis: \(V_{p^k}(G)\) is a subgroup for every \(k\geq1\).
3. **Section-wise power closure**: every section \(H/N\), with
   \(N\trianglelefteq H\leq G\), has the preceding weak power-closure
   property.

Thus
\[
  \text{section-wise power closure}
  \Longrightarrow
  \text{weak power closure in }G
  \Longrightarrow
  \text{single-group square closure when }p=2.
\]
Neither converse is used or assumed here.  In particular, for an
exponent-eight 2-group the KOU hypothesis only gives closure of the square
values; weak power closure would additionally require closure of the fourth
powers.  Weak power closure passes to quotients, so section-wise closure is
equivalently weak power closure in every subgroup.  Older papers sometimes
attach `power-closed` to different points in this hierarchy, or formulate the
condition first for \(p\)-th powers and then for its iterates.  A manuscript
must therefore state the quantifiers rather than rely on the label.

1. A. Mann,
   [“The power structure of \(p\)-groups. I”](https://www.sciencedirect.com/science/article/pii/0021869376900302),
   *Journal of Algebra* **42** (1976), 121–135,
   doi:10.1016/0021-8693(76)90030-2.

2. L. E. Wilson,
   “Dimension subgroups and \(p\)-th powers in \(p\)-groups,”
   *Israel Journal of Mathematics* **138** (2003), 1–17,
   doi:10.1007/BF02783415.  Wilson describes groups in which every product of
   \(p^k\)-th powers is again a \(p^k\)-th power as power-closed and proves
   nilpotency-class criteria.

3. L. E. Wilson,
   [“On the power structure of powerful \(p\)-groups”](https://www.degruyterbrill.com/document/doi/10.1515/jgth.5.2.129/html),
   *Journal of Group Theory* **5** (2002), 129–144,
   doi:10.1515/jgth.5.2.129.

4. J. Flake and A. Thevis,
   [“Strata of \(p\)-origamis”](https://onlinelibrary.wiley.com/doi/abs/10.1002/mana.202100290),
   *Mathematische Nachrichten* **296** (2023), 1087–1116,
   doi:10.1002/mana.202100290.  Section 3.2.4 calls a \(p\)-group weakly
   power closed when products of \(p^k\)-th powers are again \(p^k\)-th
   powers for all \(k\), and distinguishes this from the stronger
   section-closed notion.

These sources establish that closure of power values is a mature subject.
They increase the burden to articulate exactly what is new: a wreath-specific
closure criterion, its Camina interpretation, infinite exponent-eight
counterexamples, and the minimum-order classification.

### Mann (2005), Theorem 16: unresolved priority blocker

A secondary web entry claims that Theorem 16 of

A. Mann,
[“The number of generators of finite \(p\)-groups”](https://doi.org/10.1515/jgth.2005.8.3.317),
*Journal of Group Theory* **8** (2005), 317–337,

describes power-closed 2-groups of exponent at least eight.  The entry defines
`power closed` section-wise, but it is a citation-light tertiary source and
cannot establish the theorem's actual hypotheses, terminology, conclusion,
or relationship to the present groups.

The access audit on 2026-07-29 found:

- the publisher landing page and bibliographic metadata, but the publisher
  explicitly reported that the current session had no access to the article;
- no open-access copy or repository location in OpenAlex;
- a Crossref PDF link that returned to the publisher's access/CAPTCHA flow;
- metadata and later discussion of monotone 2-groups, but no reliable
  quotation of Mann's Theorem 16.

No access control was bypassed.  Therefore this audit does **not** assert what
Theorem 16 proves.  The paper's title and its later citations also make it
unsafe to infer its scope from the tertiary summary.

Even if Mann's theorem classifies the strongest, section-wise class, that
would not by logic alone classify groups satisfying only single-group square
closure.  Moreover, Mann may use a different quantifier convention or prove
auxiliary results about the weaker class or the same structural ingredients.
Obtaining an authorized full text and auditing the definition preceding
Theorem 16, the theorem itself, its proof, corollaries, and cited antecedents
is therefore a **pre-submission blocker**.  Until that is done, “not
identified” in the novelty table below must not be upgraded to “new.”

The completed order-\(128\) computation does, however, locate the ten groups
precisely in the terminology hierarchy.  In every one,
\[
 |V_2(G)|=|\langle V_2(G)\rangle|=16,\qquad
 |V_4(G)|=|\langle V_4(G)\rangle|=2,
\]
and the higher power-value sets are trivial.  Thus all ten are weakly power
closed in the single-group sense.  Each has maximal subgroups among
\[
  \operatorname{SmallGroup}(64,i),\qquad i=32,33,36,37,
\]
whose 12 square values generate a group of order 16 but are not closed.
Therefore none of the ten is section-wise power closed.  This proves that a
classification restricted to the strongest, section-wise class would not
classify these examples.  It does **not** remove the Mann blocker: the
inaccessible paper may contain additional results about the weaker class or
about the same structural ingredients.

## Camina and semi-extraspecial context

1. M. L. Lewis,
   [“Semi-extraspecial Groups”](https://arxiv.org/abs/1709.03857),
   surveys semi-extraspecial \(p\)-groups and their connections with Camina
   groups and VZ-groups.

2. M. L. Lewis,
   [“Semi-extraspecial groups with an abelian subgroup of maximal possible order”](https://arxiv.org/abs/1710.10299).

3. M. L. Lewis and J. Maglione,
   [“Enumerating isoclinism classes of semi-extraspecial groups”](https://arxiv.org/abs/1806.10511).

4. I. D. Macdonald,
   “More on \(p\)-groups of Frobenius type,”
   *Israel Journal of Mathematics* **56** (1986), 335–344,
   [doi:10.1007/BF02782940](https://doi.org/10.1007/BF02782940).
   Later sources consistently identify Theorem 3.1 as proving that every
   Camina 2-group has nilpotency class two.

5. L. Verardi,
   “Gruppi semiextraspeciali di esponente \(p\),”
   *Annali di Matematica Pura ed Applicata* **148** (1987), 131–171,
   [doi:10.1007/BF01774287](https://doi.org/10.1007/BF01774287).
   Later sources attribute to this paper the equivalence between
   class-two Camina \(p\)-groups and semi-extraspecial \(p\)-groups.

6. S. Brenner, R. D. Camina, and M. Lewis,
   [“Semi-extraspecial \(p\)-groups with automorphisms of large order”](https://doi.org/10.5802/crmath.762),
   *Comptes Rendus Mathématique* **363** (2025), 933–940,
   also [arXiv:2502.01598](https://arxiv.org/abs/2502.01598).
   Its open full text explicitly states both the Macdonald class-two theorem
   and the Verardi equivalence, with theorem-level attribution.  It also
   records the known Beisiegel dimension bound: if
   \(|G:Z(G)|=p^{2a}\) and \(|Z(G)|=p^b\), then \(b\leq a\).

7. M. L. Lewis and A. Mohammadian,
   [“Triangle-Free Cyclic Conjugacy Class Graph of a Finite Group”](https://doi.org/10.1007/s00009-025-02904-4),
   *Mediterranean Journal of Mathematics* **22** (2025), article 143.
   The open full text observes that semi-extraspecial 2-groups have exponent
   at most four and are real.  That observation does not by itself say that
   every element of the center is a square.

8. L. Kölsch and A. Polujan,
   [“Value Distributions of Perfect Nonlinear Functions”](https://arxiv.org/abs/2302.03121),
   *Combinatorica* **44** (2024), 1211–1232,
   [doi:10.1007/s00493-023-00067-y](https://doi.org/10.1007/s00493-023-00067-y).
   Their Theorem 2.4 gives general sharp lower and upper bounds on fibers of
   perfect nonlinear maps, and Corollary 2.7 proves surjectivity when
   \(|H|\leq\sqrt{|G|}\).  For
   \(|G|=2^{2n}\), \(|H|=2^m\), their lower bound is exactly
   \[
     2^{2n-m}-2^n+2^{n-m}
     =2^{n-m}(2^n-2^m+1).
   \]

9. K. Nyberg,
   “Perfect nonlinear S-boxes,” in *Advances in Cryptology—EUROCRYPT '91*,
   LNCS **547**, 378–386,
   [doi:10.1007/3-540-46416-6_32](https://doi.org/10.1007/3-540-46416-6_32).
   Nyberg's classical parameter theorem gives the vectorial bent restriction
   that the input dimension is at least twice the output dimension.

10. M. L. Lewis,
    [“Classifying Camina groups: a theorem of Dark and Scoppola”](https://arxiv.org/abs/0807.0167),
    *Rocky Mountain Journal of Mathematics* **44** (2014), 591--597,
    [doi:10.1216/RMJ-2014-44-2-591](https://doi.org/10.1216/RMJ-2014-44-2-591),
    records the three branches: Camina \(p\)-groups, Frobenius groups with
    cyclic complement, and Frobenius groups with quaternion complement.
    The paper has a published 2015 erratum, so its proof should not be cited
    without the correction below.

11. I. M. Isaacs and M. L. Lewis,
    [“Camina \(p\)-groups that are generalized Frobenius complements”](https://arxiv.org/abs/1411.3278),
    *Archiv der Mathematik* **104** (2015), 401--407,
    [doi:10.1007/s00013-015-0755-4](https://doi.org/10.1007/s00013-015-0755-4).
    This paper explicitly corrects the erroneous general-case argument and
    proves that the relevant complement is \(Q_8\).

12. R. Dark and C. M. Scoppola,
    “On Camina Groups of Prime Power Order,” *Journal of Algebra* **181**
    (1996), 787--802,
    [doi:10.1006/jabr.1996.0146](https://doi.org/10.1006/jabr.1996.0146).

13. J. D. Dixon and B. Mortimer, *Permutation Groups*, GTM 163, Springer,
    1996, Theorem 3.4A, is a standard reference for the abelianity of a
    Frobenius kernel when the complement has even order.  The present proof
    also includes the short fixed-point-free-involution argument directly.

14. M. L. Lewis,
    [“Centralizers of Camina \(p\)-groups of nilpotence class 3”](https://arxiv.org/abs/1510.06293),
    *Journal of Group Theory* **21** (2018), 319--335,
    [doi:10.1515/jgth-2017-0034](https://doi.org/10.1515/jgth-2017-0034),
    records explicitly that \(G/G_3\) has exponent \(p\) when \(G\) is a
    Camina \(p\)-group of class three.  Consequently all \(p\)-th powers lie
    in \(G_3<G'\).  This prior fact is the key exclusion of the class-three
    branch in the finite all-prime seed classification; it is not a new
    lemma of the present project.  Lewis in turn attributes the exponent
    fact to “Some finite groups with large conjugacy classes” (1990), so that
    upstream source remains part of the pre-submission audit.

The wreath criterion naturally says, in the nondegenerate case,
\[
  P=\operatorname{Sq}(A)=A',\qquad x^A=xA'\quad(x\notin A'),
\]
so the relevant seeds are Camina groups with the additional constraint that
their derived subgroup is exactly their square-value set.  Central such seeds
are special 2-groups.  This places the result inside an established
classification literature and provides the correct vocabulary.

The new proof pass connects this vocabulary to established bent-function
theory for finite 2-group seeds:

- the square map \(q:A/Z(A)\to Z(A)\) of a semi-extraspecial 2-group is
  perfect nonlinear/vectorial Boolean bent, since each nonzero derivative is
  an affine translate of the surjective map \(b(v,-)\);
- Nyberg and Kölsch--Polujan then supply the dimension bound, square
  surjectivity, and the exact all-fiber lower bound; the draft's
  Pfaffian/Fourier argument is a self-contained specialization, not a
  priority claim;
- conversely, the wreath criterion makes any nonabelian 2-group seed a
  Camina 2-group, after which Macdonald and Verardi identify it as
  semi-extraspecial.

Thus the finite nonabelian 2-group seeds for square closure in
\(A\wr C_2\) are exactly the semi-extraspecial 2-groups.  The Macdonald
class-two theorem, Verardi equivalence, Camina property, and center-dimension
bound are all prior work and must be credited as such.

The group-theory sources searched did not explicitly formulate the square
map as perfect nonlinear.  However, once that identification is made,
surjectivity and the fiber estimate are immediate prior results from the
bent-function literature.  Therefore neither statement may be presented as
new.  The only candidate novelty in this step is the cross-field
identification and its use with the exact wreath criterion.

The original Macdonald (1986) and Verardi (1987) full texts were not inspected
line-by-line in this session.  The exact statements are supported by the
open 2025 Brenner--Camina--Lewis article and several later sources, but
authorized copies of both originals remain desirable before submission.

The searched Camina/semi-extraspecial sources did not identify the exact
combination of:

- identifying the semi-extraspecial square map as perfect nonlinear and
  importing its known value-distribution theory into the wreath problem;
- classifying all finite nonabelian 2-group seeds in \(A\wr C_2\) as exactly
  the semi-extraspecial groups;
- using such a seed in \(A\wr C_2\);
- proving an if-and-only-if criterion for square-value closure;
- obtaining \(P_2(W)=W'\), and also \(P_2(W)=\Phi(W)\) for finite
  2-group seeds;
- applying this to KOU-21.137.

That negative search result is provisional.

## Final algebra-group terminology check

A final targeted search used the combinations `algebra group cube set
subgroup`, `power values algebra groups`, `nilpotent associative
F_3 power map`, and `cyclic wreath pth powers subgroup closure`.
It located adjacent work on
[power maps in finite groups](https://arxiv.org/abs/1707.06696),
[surjectivity of power maps in solvable groups](https://arxiv.org/abs/1608.02701),
and
[nilpotent associative algebras and coclass](https://www.sciencedirect.com/science/article/pii/S002186931500160X),
but none of the inspected statements concerns closure and noncommutativity
of the raw cube-value set in \(1+J\), or the dimension-eleven/twelve
filtration boundary proved here.  This is a negative keyword-and-abstract
check, not a priority clearance: terminology in algebra-group, radical-ring,
regular-\(p\)-group, or verbal-width literature may conceal an equivalent
result.  The dimension bound therefore remains a candidate-new theorem
pending MathSciNet/zbMATH citation chaining and specialist review.

## Provisional novelty map

| Component | Priority status |
|---|---|
| \(D_8\wr C_2\) is a KOU-21.137 counterexample | Prior public Lean gist, 2026-04-14 |
| General characterization of powers in \(G\wr S_n\) | Kundu–Mondal, 2022 |
| Direct formula for squares in \(A\wr C_2\) | Elementary specialization; do not claim strongly |
| General restrictions from \(G^{[2]}\leq G\) | Liebeck–Shalev, 2013; composition-factor result |
| General conditions for a power-value set to be a subgroup | Bennett thesis, 2012; full-text audit blocked |
| Minimal orders and SmallGroups counts for nonclosed power-value sets | Kappe 2005 / Mendoza 2004; direct prior computational background |
| \(C_p\wr C_p\) is power closed for the odd-prime example | Kappe--Ying 1992, Example 6.4; direct prior wreath example |
| Single-group square-subgroup background and order criteria | Chuah 2021, building on Sun 1980 and Haugh--MacHale 1997; direct prior theory |
| Exact criterion for the square-value set to be a subgroup | Not identified in this search; candidate new theorem |
| Under the criterion, \(P=A'\), square subgroup \(=W'\), and for 2-group seeds also \(=\Phi(W)\) | Not identified; candidate new structural refinement |
| Camina 2-groups have class two | Macdonald, 1986, Theorem 3.1; prior theorem |
| Class-two Camina \(p\)-groups are semi-extraspecial | Verardi, 1987; prior equivalence |
| Semi-extraspecial center bound \(b\leq a\) | Beisiegel, 1977; prior theorem |
| Perfect nonlinear/vectorial bent parameter bound \(m\leq n\) | Nyberg, 1991; prior theorem; also consistent with Beisiegel's group bound |
| Perfect nonlinear fiber lower bound and surjectivity for \(|H|\leq\sqrt{|G|}\) | Kölsch--Polujan, Theorem 2.4 and Corollary 2.7; prior results |
| Semi-extraspecial square map is perfect nonlinear | Direct observation from the Camina commutator condition; exact group-theory formulation not identified, but no independent value-distribution novelty |
| Finite nonabelian 2-group seeds \(A\) with \(P_2(A\wr C_2)\) closed are exactly the semi-extraspecial groups | Exact application/combination not identified; candidate new classification built on Nyberg, Kölsch--Polujan, Macdonald, and Verardi |
| Three-branch classification of finite nonabelian Camina groups | Dark--Scoppola; Lewis 2014 with erratum; corrected general argument in Isaacs--Lewis 2015 |
| Five-class classification of all finite wreath seeds | Exact synthesis with the square-wreath criterion not identified; candidate application of prior Camina/Frobenius structure |
| At-most-five-class classification of all finite seeds for every prime \(p\) | Exact synthesis not identified; candidate application of the unrestricted wreath criterion, Dark--Scoppola classification, and Lewis's prior class-three exponent theorem |
| Odd-prime formula \(P_p(A\wr C_p)=P_p(A)^p\cup\bigcup_C C^p\) | Direct specialization of established wreath cycle-data theory; no strong priority claim |
| Panja--Singh survey coverage of Kundu--Mondal | Full arXiv source has one sentence pointing to the wreath paper and no subgroup-closure/Camina result; useful negative check, not an exhaustive priority clearance |
| Unrestricted closure criterion for \(P_p(A\wr C_p)\) at every prime \(p\) | Not identified in the present search; candidate main theorem, but requires citation-chain audit from Kundu--Mondal and power-value-subgroup work |
| Structural position \(H\le W'\), \([W':H]=|A/A'|^{p-2}\), and \(\Phi(W)=W'\) for finite \(p\)-group seeds | Direct consequence of the new closure criterion plus the standard wreath abelianization/Frattini formula; exact packaged statement not identified, but should be presented as a structural corollary rather than an independent priority claim |
| Odd-\(p\) nilpotency barrier: exponent \(p^2\), class \(\le p\) implies all raw \(p\)-th powers commute | Direct Hall-collection consequence; exact KOU formulation not identified.  Must cite Hall/Struik and compare with regular \(p\)-group and Moravec power-map theory; candidate search-filter corollary, not a standalone priority claim |
| Metabelian refinement: exponent \(p^2\), class \(<2p\) implies all raw \(p\)-th powers commute | Proved here by the standard group-ring module and cyclotomic-norm mechanism.  The exact sentence was not found, but Bachmuth--Mochizuki (1968) and subsequent metabelian Burnside-group work study precisely these cyclotomic ideals.  Treat as a likely corollary of prior machinery, not a standalone novelty claim, until that citation chain is checked line-by-line |
| Universal class-\((2p-1)\) refinement | Unproved.  Full order-\(2187\) evidence at \(p=3\) and the metabelian theorem do not establish it |
| Khukhro class-\((2p-1)\) exponent-\(p^2\) construction | Prior Hughes-subgroup boundary result (conditional relation ideal, verified for \(p=5,7,11\)); it does not state that \(G^p\) is nonabelian and is not a counterexample to the universal power-commutator candidate without an additional calculation |
| Havas--Vaughan-Lee explicit \(p=5\), class-nine anti-Hughes family | Published Magma output gives \(\exp(G')=5\), \(H_5(G)=\langle c\rangle G'\), and central \(c^5\).  A short Hall argument then puts all fifth powers in the abelian subgroup \(\langle c^5\rangle\gamma_6(G)\); this family is not a power-commutator counterexample |
| Central-power exact closure criterion, moment obstruction, and diagonal-quotient invariance | Not identified in the present search; candidate result requiring dedicated citation-chain audit |
| Every exponent-lowering quotient of the positive exponent-\(p^2\) wreath family has abelian power subgroup | Not identified in the present search; candidate result requiring dedicated citation-chain audit |
| Every quotient of an exponent-\(p\) semi-extraspecial wreath seed whose power values close has abelian power subgroup | Not identified in the present search; candidate all-quotients obstruction.  Requires a dedicated priority search around Camina groups, verbal subsets in quotients, and modular wreath-product arguments before any novelty claim |
| Exponent-nine algebra groups \(1+J\) over \(\mathbb F_3\): if \(\dim J\le11\) and the raw cube set is a subgroup, then it is abelian | Not identified in the present search; candidate new closure-aware lower bound.  The proof combines a 246-profile reduction, pure-tail lemmas, and a 130-plane quadratic audit.  It needs a dedicated algebra-group/power-map priority search and specialist review before a novelty claim |
| Extraspecial and \(\operatorname{UT}_3(\mathbb F_{2^m})\) families | Consequences of the semi-extraspecial theorem; no separate priority claim |
| Minimum order 128; ten types as a \(6+4\) family of central lifts of one explicit quotient | Not identified; candidate new certified classification |

## Required pre-submission follow-up

1. Obtain Mann (2005) and Bennett (2012) through an authorized institutional
   subscription, interlibrary loan, or author-provided copy.  Audit Mann's
   Theorem 16 line-by-line against the three property levels, and audit every
   subgroup-closure theorem and example in Bennett's thesis.
2. Cite and distinguish Liebeck–Shalev (2013), whose composition-factor
   theorem is prior general theory but is orthogonal to the internal
   nonabelian square subgroup of a 2-group.
3. Cite Kappe--Ying (1992), Example 6.4, as the direct cyclic-wreath
   predecessor, and Chuah (2021) as direct square-subgroup background.
   Obtain Sun (1980) and inspect its original theorem hypotheses rather than
   relying only on Chuah's restatement.
4. Search MathSciNet and zbMATH for all papers citing Mann (1976), Mann
   (2005), Bennett (2012), Wilson (2003), Liebeck–Shalev (2013), and
   Kappe--Ying (1992) and Kundu–Mondal (2022), using citation chaining
   rather than keywords alone.
5. Search terminology variants: `power closed`, `power-closed`,
   `weakly power closed`, `\(\mathcal P_2\)-group`, `Camina pair`,
   `semi-extraspecial`, `special 2-group`, `word-value subgroup`, and
   `verbal width one`.
6. Ask a specialist in finite \(p\)-groups to check whether Theorem 2 is an
   immediate known consequence under a different vocabulary.
7. Cite the Judin artifact transparently and date the AMRA computations.
8. Do not market the package as a Q1 result until novelty and proof audits are
   complete.
9. Obtain authorized copies of Macdonald (1986) and Verardi (1987), and
   inspect the cited theorem, all adjacent corollaries, and their references
   for any statement about squares or quadratic maps.  The open 2025
   secondary verification is strong but does not replace an original-source
   priority audit.
10. Citation-chain the vectorial bent/perfect-nonlinear literature around
   Nyberg and Kölsch--Polujan for prior appearances of square maps of special
   2-groups.  Do not claim the fiber bound or surjectivity as new.
11. Obtain Mendoza's 2004 thesis cited by Kappe and inspect its complete
    examples and algorithms.  Citation-chain Lewis 2014, its erratum, and
    Isaacs--Lewis 2015 before claiming priority for the five-class finite-seed
    synthesis.
12. Resolve the Semantic Scholar/OpenAlex citation-count discrepancy for
    Kundu--Mondal through MathSciNet, zbMATH, Crossref, and publisher
    references.  Inspect every true citer, including Panja--Singh, before
    claiming priority for the unrestricted all-prime closure theorem.
13. Inspect Bachmuth--Mochizuki, *The class of the free metabelian group
    with exponent \(p^2\)* (1968), Bachmuth--Heilbronn--Mochizuki,
    *Burnside metabelian groups* (1968), and the later Dark--Newell/Newman
    papers for the exact cyclotomic-ideal consequence used in
    `METABELIAN_2P_NILPOTENCY_BARRIER.md`.
14. Compute \([G^p,G^p]\) in Khukhro's class-\((2p-1)\) presentation before
    using the Hughes boundary as evidence either for or against the
    unrestricted sharp-\(2p\) candidate.
