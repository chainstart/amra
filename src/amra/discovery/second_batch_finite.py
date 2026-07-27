from __future__ import annotations

import copy
import itertools
import hashlib
import json
import math
import random
import shutil
import subprocess
import sys
import time
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy
import sympy


EXECUTOR_VERSION = "amra.second_batch_finite.v3"
EXECUTOR_ID = "second_batch.finite.exact_search.v1"
STRATEGIES = ("screen-exact", "deep-diversified")
_CATALOGUE_SHARD_STRATEGIES = tuple(
    f"deep-catalogue-{shard}" for shard in range(3)
)
GAP_BINARY = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap"
)
GAP_ROOT = Path("/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap")
_KOU_21_26_DEEP_OFFSET = 1_000_000
_RAMSEY_DEEP_OFFSET = 2_000_000
_KOU_21_99_DEEP_OFFSET = 3_000_000
_OPG_48264_DEEP_OFFSET = 4_000_000
_RAMSEY_DEEP_CHUNK_FLIPS = 10_000


_SOURCE_ROWS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "unsolvedmath-comb-003",
        "COMB-003",
        "Ramsey Number R(5,5)",
        "combinatorics",
        "What is the exact value of $R(5,5)$, the smallest number $n$ such that any 2-coloring of the edges of $K_n$ contains a monochromatic $K_5$?",
    ),
    (
        "unsolvedmath-nt-010",
        "NT-010",
        "Brocard's Problem",
        "number_theory",
        "Find all integer solutions to $n! + 1 = m^2$.",
    ),
    (
        "unsolvedmath-nt-026",
        "NT-026",
        "The Odd Perfect Number Conjecture",
        "number_theory",
        "Do there exist any odd perfect numbers? (A perfect number equals the sum of its proper divisors.)",
    ),
    (
        "unsolvedmath-nt-027",
        "NT-027",
        "Firoozbakht's Conjecture",
        "number_theory",
        "Is the sequence $p_n^{1/n}$ strictly decreasing, where $p_n$ is the $n$-th prime?",
    ),
    (
        "unsolvedmath-nt-033",
        "NT-033",
        "Grimm's Conjecture",
        "number_theory",
        "Can each element of a set of consecutive composite numbers be assigned a distinct prime divisor?",
    ),
    (
        "unsolvedmath-nt-039",
        "NT-039",
        "Scholz Conjecture",
        "number_theory",
        "Is the shortest addition chain for $2^n - 1$ at most $n - 1$ plus the length of the shortest addition chain for $n$?",
    ),
    (
        "unsolvedmath-nt-043",
        "NT-043",
        "Quasiperfect Numbers",
        "number_theory",
        "Do quasiperfect numbers exist?",
    ),
    (
        "unsolvedmath-nt-044",
        "NT-044",
        "Almost Perfect Numbers Beyond Powers of 2",
        "number_theory",
        "Do any almost perfect numbers exist that are not powers of 2?",
    ),
    (
        "unsolvedmath-nt-046",
        "NT-046",
        "Amicable Numbers of Opposite Parity",
        "number_theory",
        "Do any pairs of amicable numbers exist where one is odd and one is even?",
    ),
    (
        "unsolvedmath-nt-050",
        "NT-050",
        "Odd Weird Numbers",
        "number_theory",
        "Do any odd weird numbers exist?",
    ),
    (
        "unsolvedmath-nt-053",
        "NT-053",
        "Is 10 a Solitary Number?",
        "number_theory",
        "Is 10 a solitary number (no other number shares its abundancy index)?",
    ),
    (
        "unsolvedmath-nt-078",
        "NT-078",
        "Beal's Conjecture",
        "number_theory",
        "For $A^x + B^y = C^z$ with $x, y, z > 2$, must $A$, $B$, and $C$ share a common prime factor?",
    ),
    (
        "unsolvedmath-nt-086",
        "NT-086",
        "Brocard's Conjecture (Prime Gaps)",
        "number_theory",
        "Are there always at least 4 primes between consecutive squares of primes $p_n^2$ and $p_{n+1}^2$?",
    ),
    (
        "unsolvedmath-guy-a12b",
        "GUY-A12b",
        "Selfridge-Wagstaff-Pomerance Prize Problem",
        "number_theory",
        "Does there exist a composite number $n \\equiv 3$ or $7 \\pmod{10}$ which divides both $2^n - 2$ and the Fibonacci number $u_{n+1}$?",
    ),
    (
        "unsolvedmath-guy-a19a",
        "GUY-A19a",
        "Erdős Conjecture on $n - 2^k$ Prime",
        "number_theory",
        "Are 4, 7, 15, 21, 45, 75, and 105 the only values of $n$ for which $n - 2^k$ is prime for all $k$ such that $2 \\le 2^k < n$?",
    ),
    (
        "unsolvedmath-guy-a7b",
        "GUY-A7b",
        "Shanks Chains of Length 7",
        "number_theory",
        "Are there any Shanks chains of length 7 with $p_{i+1} = 4p_i^2 - 17$?",
    ),
    (
        "unsolvedmath-opg-148",
        "OPG-148",
        "A nowhere-zero point in a linear mapping",
        "combinatorics",
        "Conjecture If ${\\mathbb F}$ is a finite field with at least 4 elements and $A$ is an invertible $n \\times n$ matrix with entries in ${\\mathbb F}$, then there are column vectors $x,y \\in {\\mathbb F}^n$ which have no coordinates equal to zero such that $Ax=y$.",
    ),
    (
        "unsolvedmath-opg-151",
        "OPG-151",
        "The permanent conjecture",
        "combinatorics",
        "Conjecture If $A$ is an invertible $n \\times n$ matrix, then there is an $n \\times n$ submatrix $B$ of $[A A]$ so that $perm(B)$ is nonzero.",
    ),
    (
        "unsolvedmath-opg-16570",
        "OPG-16570",
        "Magic square of squares",
        "number_theory",
        "Question Does there exist a $3\\times 3$ magic square composed of distinct perfect squares?",
    ),
    (
        "unsolvedmath-opg-37221",
        "OPG-37221",
        "Perfect cuboid",
        "number_theory",
        "Conjecture Does a perfect cuboid exist?",
    ),
    (
        "unsolvedmath-opg-46385",
        "OPG-46385",
        "Caccetta-Häggkvist Conjecture",
        "graph_theory",
        "Conjecture Every simple digraph of order $n$ with minimum outdegree at least $r$ has a cycle with length at most $\\lceil n/r\\rceil$",
    ),
    (
        "unsolvedmath-opg-369",
        "OPG-369",
        "Bases of many weights",
        "combinatorics",
        "Let $G$ be an (additive) abelian group, and for every $S \\subseteq G$ let ${\\mathit stab}(S) = \\{ g \\in G: g + S = S \\}$.\n\nConjecture Let $M$ be a matroid on $E$, let $w: E \\rightarrow G$ be a map, put $S = \\{ \\sum_{b \\in B} w(b): B \\mbox{ is a base} \\}$ and $H = {\\mathit stab}(S)$. Then $$|S| \\ge |H| \\left( 1 - rk(M) + \\sum_{Q \\in G/H} rk(w^{-1}(Q)) \\right).$$",
    ),
    (
        "unsolvedmath-opg-1793",
        "OPG-1793",
        "Non-edges vs. feedback edge sets in digraphs",
        "graph_theory",
        "For any simple digraph $G$, we let $\\gamma(G)$ be the number of unordered pairs of nonadjacent vertices (i.e. the number of non-edges), and $\\beta(G)$ be the size of the smallest feedback edge set.\n\nConjecture If $G$ is a simple digraph without directed cycles of length $\\le 3$, then $\\beta(G) \\le \\frac{1}{2} \\gamma(G)$.",
    ),
    (
        "unsolvedmath-comb-001-collision-1-3-2-3-conjecture-3976e813",
        "COMB-001",
        "1/3–2/3 Conjecture",
        "combinatorics",
        "Does every non-totally-ordered finite poset have two elements with probability between 1/3 and 2/3 in random linear extensions?",
    ),
    (
        "unsolvedmath-alg-007",
        "ALG-007",
        "Casas-Alvero Conjecture",
        "algebra",
        "If a univariate polynomial $f$ of degree $d$ over a field of characteristic 0 shares a common factor with each of its first $d-1$ derivatives, must $f$ be a power of a linear polynomial?",
    ),
    (
        "unsolvedmath-kou-21.26",
        "KOU-21.26",
        "Kourovka Notebook Problem 21.26",
        "group_theory",
        "Let $G$ be a non-trivial finite group and let $p_1,\\ldots,p_k$ be the distinct prime divisors of $|G|$. For each $i$, let $H_i$ be a Sylow $p_i$-subgroup of $G$. Is it true that there exists an element $x\\in G$ such that for all $i$ the subgroup $H_i\\cap H_i^x$ is inclusion-minimal in $\\{H_i\\cap H_i^g:g\\in G\\}$?",
    ),
    (
        "unsolvedmath-opg-600",
        "OPG-600",
        "Matchings extend to Hamiltonian cycles in hypercubes",
        "graph_theory",
        "Question Does every matching of hypercube extend to a Hamiltonian cycle?",
    ),
    (
        "unsolvedmath-opg-37670",
        "OPG-37670",
        "The Borodin-Kostochka Conjecture",
        "graph_theory",
        "Conjecture Every graph with maximum degree $\\Delta \\geq 9$ has chromatic number at most $\\max\\{\\Delta-1, \\omega\\}$.",
    ),
    (
        "unsolvedmath-opg-404",
        "OPG-404",
        "Concavity of van der Waerden numbers",
        "combinatorics",
        "For $k$ and $\\ell$ positive integers, the (mixed) van der Waerden number $w(k,\\ell)$ is the least positive integer $n$ such that every (red-blue)-coloring of $[1,n]$ admits either a $k$-term red arithmetic progression or an $\\ell$-term blue arithmetic progression.\n\nConjecture For all $k$ and $\\ell$ with $k \\geq \\ell$, $w(k,\\ell) \\geq w(k+1,\\ell-1)$.",
    ),
    (
        "unsolvedmath-opg-636",
        "OPG-636",
        "Even vs. odd latin squares",
        "combinatorics",
        "A latin square is even if the product of the signs of all of the row and column permutations is 1 and is odd otherwise.\n\nConjecture For every positive even integer $n$, the number of even latin squares of order $n$ and the number of odd latin squares of order $n$ are different.",
    ),
    (
        "unsolvedmath-kou-21.99",
        "KOU-21.99",
        "Kourovka Notebook Problem 21.99",
        "group_theory",
        "Conjecture: If $G$ is a transitive permutation group on a finite set $\\Omega$, then for any distinct $\\alpha,\\beta\\in\\Omega$ there is an element $g\\in G$ with $\\alpha^g=\\beta$ whose number of fixed points is different from 1.",
    ),
    (
        "unsolvedmath-opg-169",
        "OPG-169",
        "The Two Color Conjecture",
        "graph_theory",
        "Conjecture If $G$ is an orientation of a simple planar graph, then there is a partition of $V(G)$ into $\\{X_1,X_2\\}$ so that the graph induced by $X_i$ is acyclic for $i=1,2$.",
    ),
    (
        "unsolvedmath-opg-382",
        "OPG-382",
        "Aharoni-Berger conjecture",
        "combinatorics",
        "Conjecture If $M_1,\\ldots,M_k$ are matroids on $E$ and $\\sum_{i=1}^k rk_{M_i}(X_i) \\ge \\ell (k-1)$ for every partition $\\{X_1,\\ldots,X_k\\}$ of $E$, then there exists $X \\subseteq E$ with $|X| = \\ell$ which is independent in every $M_i$.",
    ),
    (
        "unsolvedmath-opg-48264",
        "OPG-48264",
        "Signing a graph to have small magnitude eigenvalues",
        "graph_theory",
        "Conjecture If $A$ is the adjacency matrix of a $d$-regular graph, then there is a symmetric signing of $A$ (i.e. replace some $+1$ entries by $-1$ ) so that the resulting matrix has all eigenvalues of magnitude at most $2 \\sqrt{d-1}$.",
    ),
)


_WITNESS_CONTRACTS: dict[str, tuple[str, str, str]] = {
    "unsolvedmath-comb-003": (
        "two-colourings of all 903 edges of K_43",
        "the colouring has no monochromatic set of five vertices",
        "a complete K_43 edge-colouring independently checked on all 962598 five-sets; K_42 witnesses are excluded",
    ),
    "unsolvedmath-nt-010": (
        "positive integers n, excluding the source-known solutions n=4,5,7",
        "n!+1 is an integer square",
        "an exact additional pair (n,m)",
    ),
    "unsolvedmath-nt-026": (
        "positive odd integers n",
        "the sum of proper divisors of n equals n",
        "an odd perfect number with its exact divisor sum",
    ),
    "unsolvedmath-nt-027": (
        "consecutive prime indices n and n+1",
        "p_n^(1/n) is not strictly greater than p_(n+1)^(1/(n+1))",
        "the exact integer inequality p_n^(n+1) <= p_(n+1)^n",
    ),
    "unsolvedmath-nt-033": (
        "maximal finite runs of consecutive composite integers",
        "no injective assignment of a prime divisor to every member exists",
        "the run, all prime-divisor sets, and a failed exact matching",
    ),
    "unsolvedmath-nt-039": (
        "positive integers n searched with exact shortest addition-chain lengths",
        "ell(2^n-1) > n-1+ell(n)",
        "n and the three exact integer chain lengths",
    ),
    "unsolvedmath-nt-043": (
        "positive integers n",
        "sigma(n)=2n+1",
        "a quasiperfect integer and exact divisor sum",
    ),
    "unsolvedmath-nt-044": (
        "positive integers n that are not powers of two",
        "the sum of proper divisors is n-1",
        "an almost-perfect non-power-of-two integer",
    ),
    "unsolvedmath-nt-046": (
        "unordered positive integer pairs of opposite parity",
        "each integer is the sum of the other's proper divisors",
        "an exact opposite-parity amicable pair",
    ),
    "unsolvedmath-nt-050": (
        "positive odd integers n",
        "n is abundant and no subset of proper divisors sums to n",
        "an odd weird number plus exact subset-sum exhaustion",
    ),
    "unsolvedmath-nt-053": (
        "positive integers n != 10",
        "sigma(n)/n = sigma(10)/10",
        "a second integer with the exact same reduced abundancy index",
    ),
    "unsolvedmath-nt-078": (
        "positive A,B,C and integer exponents x,y,z>2",
        "A^x+B^y=C^z and gcd(A,B,C)=1",
        "an exact finite-box Beal counterexample",
    ),
    "unsolvedmath-nt-086": (
        "consecutive primes p_n,p_(n+1)",
        "fewer than four primes lie strictly between their squares",
        "the endpoints and complete intervening-prime list",
    ),
    "unsolvedmath-guy-a12b": (
        "composite n congruent to 3 or 7 modulo 10",
        "n divides both 2^n-2 and Fibonacci u_(n+1)",
        "n and both exact modular residues",
    ),
    "unsolvedmath-guy-a19a": (
        "positive n outside the seven source-listed values",
        "n-2^k is prime for every power 2^k with 2<=2^k<n",
        "n and the complete checked prime list",
    ),
    "unsolvedmath-guy-a7b": (
        "prime starting values p_1",
        "seven successive values p_(i+1)=4p_i^2-17 are all prime",
        "the exact seven-prime chain",
    ),
    "unsolvedmath-opg-148": (
        "invertible matrices over prime fields F_p with p>=5",
        "no vector x with all coordinates nonzero has Ax coordinatewise nonzero",
        "p, A, determinant, and exhaustive nonzero-vector check",
    ),
    "unsolvedmath-opg-151": (
        "invertible matrices over prime fields",
        "every n-column submatrix of [A A] has zero permanent",
        "p, A, determinant, and all exact permanents",
    ),
    "unsolvedmath-opg-16570": (
        "three-by-three integer arrays generated in the standard magic-square parametrization",
        "all nine entries are distinct positive squares with equal row, column, and diagonal sums",
        "the nine roots, entries, and common sum",
    ),
    "unsolvedmath-opg-37221": (
        "positive integer edge triples",
        "all three face diagonals and the space diagonal are integers",
        "the edges and four exact squared-length certificates",
    ),
    "unsolvedmath-opg-46385": (
        "finite simple digraphs and their exact minimum outdegree r",
        "there is no directed cycle of length at most ceil(n/r)",
        "the arc set, r, and complete short-cycle exhaustion",
    ),
    "unsolvedmath-opg-369": (
        "graphic matroids of small labelled multigraph-free graphs with weights in composite cyclic groups Z_m",
        "S, its stabilizer H, all quotient-coset preimages, and their graphic ranks violate the displayed inequality",
        "the graph, weights, every spanning-forest base, S, H, cosets, preimage ranks, and both sides",
    ),
    "unsolvedmath-opg-1793": (
        "finite simple digraphs with no directed cycle of length at most three",
        "the minimum feedback-edge-set size beta exceeds half the nonedge count gamma",
        "the arc set, all cycles, beta, gamma, and exact deletion exhaustion",
    ),
    "unsolvedmath-comb-001-collision-1-3-2-3-conjecture-3976e813": (
        "finite labelled non-total posets",
        "no incomparable pair has ordering probability in [1/3,2/3]",
        "the order relation and complete list of linear extensions",
    ),
    "unsolvedmath-alg-007": (
        "monic integer polynomials, a characteristic-zero subfamily",
        "f shares a nonconstant gcd with every derivative but has more than one distinct root",
        "coefficients and exact polynomial gcds",
    ),
    "unsolvedmath-kou-21.26": (
        "six named permutation-group screen cases and a GAP SmallGroups deep catalogue of nonabelian groups of orders 62 through 255",
        "no group element simultaneously makes every chosen Sylow intersection inclusion-minimal",
        "the SmallGroup identifier, chosen Sylow subgroups, all conjugate-intersection orders, inclusion-minimality flags, and exact GAP replay",
    ),
    "unsolvedmath-opg-600": (
        "matchings in hypercubes Q_d; screen cases explicitly replicate d<=5, while deep Q_6 cases use all six directions and size at least 16 to exceed the encoded known frontiers",
        "the matching is not contained in any Hamiltonian cycle",
        "the matching plus two independently generated complete Z3 UNSAT encodings, their SHA-256 hashes, solver versions, and proof-output hashes",
    ),
    "unsolvedmath-opg-37670": (
        "simple labelled graphs on ten vertices, searched from dense graphs downward",
        "maximum degree Delta>=9 and chi(G)>max(Delta-1,omega(G))",
        "the edge set plus exact maximum degree, clique number, and chromatic number",
    ),
    "unsolvedmath-opg-404": (
        "finite integer pairs k>=ell>=2 with exactly computed mixed van der Waerden numbers",
        "w(k,ell) < w(k+1,ell-1)",
        "k, ell, both exact numbers, and exhaustive colouring certificates",
    ),
    "unsolvedmath-opg-636": (
        "Latin squares of a fixed positive even order n",
        "the exact even and odd counts are equal",
        "n, complete enumeration count, and parity totals",
    ),
    "unsolvedmath-kou-21.99": (
        "nonregular transitive coset actions from diversified symmetric, alternating, and dihedral groups with many nonconjugate subgroup types",
        "some ordered alpha!=beta has only mapping elements with exactly one fixed point",
        "the source group, subgroup, induced coset action, and exhaustive mapper fixed-point counts",
    ),
    "unsolvedmath-opg-169": (
        "orientations of simple planar graphs on at most four labelled vertices",
        "no vertex bipartition makes both induced digraphs acyclic",
        "the oriented edge set and exhaustive partition results",
    ),
    "unsolvedmath-opg-382": (
        "small explicitly encoded partition matroids on a common labelled ground set",
        "every ordered k-partition passes the rank premise but no ell-set is independent in every matroid",
        "all block/capacity data, every partition rank sum, and every ell-subset independence result",
    ),
    "unsolvedmath-opg-48264": (
        "bounded diverse cubic and quartic graph families, with switching equivalence fixing a spanning tree positive",
        "every symmetric edge signing has spectral radius above 2*sqrt(d-1)",
        "the graph, fixed spanning tree, every cycle-rank signing, and an integer vector v for each signing with v^T(4(d-1)I-A^2)v<0",
    ),
}

_WITNESS_SEARCH_IDS = {
    "unsolvedmath-comb-003",
    "unsolvedmath-nt-010",
    "unsolvedmath-nt-026",
    "unsolvedmath-nt-043",
    "unsolvedmath-nt-044",
    "unsolvedmath-nt-046",
    "unsolvedmath-nt-050",
    "unsolvedmath-guy-a12b",
    "unsolvedmath-guy-a7b",
    "unsolvedmath-opg-16570",
    "unsolvedmath-opg-37221",
}
_RESTRICTED_FAMILY_IDS = {
    "unsolvedmath-opg-148",
    "unsolvedmath-opg-151",
    "unsolvedmath-opg-369",
    "unsolvedmath-opg-382",
    "unsolvedmath-alg-007",
    "unsolvedmath-kou-21.26",
    "unsolvedmath-opg-37670",
    "unsolvedmath-kou-21.99",
    "unsolvedmath-opg-169",
    "unsolvedmath-opg-1793",
    "unsolvedmath-opg-46385",
    "unsolvedmath-opg-48264",
    "unsolvedmath-opg-636",
}
_DIVERSIFIED_IDS = {
    "unsolvedmath-comb-003",
    "unsolvedmath-nt-010",
    "unsolvedmath-nt-026",
    "unsolvedmath-nt-027",
    "unsolvedmath-nt-033",
    "unsolvedmath-nt-043",
    "unsolvedmath-nt-044",
    "unsolvedmath-nt-046",
    "unsolvedmath-nt-050",
    "unsolvedmath-nt-053",
    "unsolvedmath-nt-078",
    "unsolvedmath-nt-086",
    "unsolvedmath-guy-a12b",
    "unsolvedmath-guy-a19a",
    "unsolvedmath-opg-16570",
    "unsolvedmath-opg-37221",
    "unsolvedmath-opg-369",
    "unsolvedmath-opg-600",
    "unsolvedmath-opg-382",
    "unsolvedmath-kou-21.26",
    "unsolvedmath-kou-21.99",
}


def _spec(
    problem_id: str,
    source_id: str,
    title: str,
    domain: str,
    statement: str,
) -> dict[str, Any]:
    objects, premise, witness = _WITNESS_CONTRACTS[problem_id]
    if problem_id in _WITNESS_SEARCH_IDS:
        claim_scope = "witness_search"
        scope_limitation = (
            "The source is existential or asks for additional solutions. The "
            "executor can certify a new witness but bounded absence has no "
            "negative force."
        )
    elif problem_id in _RESTRICTED_FAMILY_IDS:
        claim_scope = "restricted_family"
        scope_limitation = (
            "The executor enumerates the explicitly named finite subfamily in "
            "model_contract.objects. A failure inside it is a valid source-level "
            "counterexample; no failure says nothing about objects outside it."
        )
    else:
        claim_scope = "full_claim"
        scope_limitation = (
            "The mathematical predicate matches the full source claim; only the "
            "finite search range is bounded."
        )
    catalogue_sharded = problem_id in {
        "unsolvedmath-kou-21.26",
        "unsolvedmath-kou-21.99",
        "unsolvedmath-opg-48264",
    }
    if catalogue_sharded:
        deep_search_role = "disjoint_canonical_catalogue_shards"
    elif problem_id in _DIVERSIFIED_IDS:
        deep_search_role = "seeded_stratified_frontier_search"
    else:
        deep_search_role = "monotone_exact_case_enumeration"
    catalogue_provenance = {
        "unsolvedmath-kou-21.26": {
            "catalogue": "all 6,308 nonabelian SmallGroups of orders 61..255",
            "shard_count": 3,
        },
        "unsolvedmath-kou-21.99": {
            "catalogue": "17 hash-distinct faithful nonregular coset actions",
            "shard_count": 3,
        },
        "unsolvedmath-opg-48264": {
            "catalogue": "all 41,301 nonisomorphic connected cubic graphs of order 18",
            "shard_count": 3,
        },
    }
    return {
        "problem_id": problem_id,
        "source_id": source_id,
        "title": title,
        "domain": domain,
        "executor_id": EXECUTOR_ID,
        "version": EXECUTOR_VERSION,
        "strategies": (
            ["screen-exact", *_CATALOGUE_SHARD_STRATEGIES]
            if catalogue_sharded
            else list(STRATEGIES)
        ),
        "screen_strategy": "screen-exact",
        "deep_strategies": (
            list(_CATALOGUE_SHARD_STRATEGIES)
            if catalogue_sharded
            else ["deep-diversified"]
        ),
        "screen_bounds": {"max_cases": 2_000},
        "supports_deep": True,
        "deep_bounds": {"max_cases": 1_000_000},
        "deep_launches": (
            1
            if catalogue_sharded
            else (3 if problem_id in _DIVERSIFIED_IDS else 1)
        ),
        "deep_search_role": deep_search_role,
        "frontier_provenance": {
            "case_generator_contract": objects,
            "resume_indexing": (
                "three disjoint strategy shards"
                if catalogue_sharded
                else (
                    "seed-selected stratum plus monotone local index"
                    if problem_id in _DIVERSIFIED_IDS
                    else "monotone exact case index"
                )
            ),
            **catalogue_provenance.get(problem_id, {}),
        },
        "claim_scope": claim_scope,
        "scope_limitation": scope_limitation,
        "model_contract": {
            "source_statement": statement,
            "source_quantifiers_preserved": (
                claim_scope != "restricted_family"
                and problem_id != "unsolvedmath-comb-003"
            ),
            "claim_scope": claim_scope,
            "scope_limitation": scope_limitation,
            "objects": objects,
            "premise": premise,
            "counterexample_or_witness": witness,
            "bounded_result_semantics": (
                "No witness means only that the explicitly enumerated finite cases "
                "were checked; it never proves the unbounded source statement."
            ),
            "candidate_policy": (
                "Source-listed or otherwise encoded known examples are excluded "
                "from candidate output."
            ),
        },
    }


SECOND_BATCH_FINITE_SPECS: tuple[dict[str, Any], ...] = tuple(
    _spec(*row) for row in _SOURCE_ROWS
)
_SPECS_BY_ID = {
    str(spec["problem_id"]): spec for spec in SECOND_BATCH_FINITE_SPECS
}


def _max_cases(budget: Mapping[str, Any]) -> int:
    value = budget.get("max_cases", 1)
    return max(0, int(value if value is not None else 1))


def _time_seconds(budget: Mapping[str, Any]) -> float:
    value = budget.get("time_seconds", 0)
    return max(0.0, float(value if value is not None else 0.0))


def _catalogue_strategy_shard(strategy_id: str) -> int | None:
    prefix = "deep-catalogue-"
    if not strategy_id.startswith(prefix):
        return None
    shard = int(strategy_id[len(prefix) :])
    if not 0 <= shard < 3:
        raise ValueError(f"invalid catalogue shard strategy {strategy_id!r}")
    return shard


def _seeded_index(
    problem_id: str, index: int, strategy_id: str, seed: int
) -> int:
    if strategy_id == "screen-exact":
        return index
    if problem_id == "unsolvedmath-opg-48264":
        shard = _catalogue_strategy_shard(strategy_id)
        effective_shard = (
            shard
            if shard is not None
            else random.Random(int(seed)).randrange(3)
        )
        return _OPG_48264_DEEP_OFFSET + effective_shard + index * 3
    if problem_id not in _DIVERSIFIED_IDS:
        return index
    stratum = random.Random(int(seed)).randrange(97)
    if problem_id == "unsolvedmath-kou-21.26":
        shard = _catalogue_strategy_shard(strategy_id)
        effective_shard = (
            shard
            if shard is not None
            else random.Random(int(seed)).randrange(3)
        )
        return _KOU_21_26_DEEP_OFFSET + effective_shard + index * 3
    if problem_id == "unsolvedmath-comb-003":
        return _RAMSEY_DEEP_OFFSET + stratum + index * 97
    if problem_id == "unsolvedmath-kou-21.99":
        shard = _catalogue_strategy_shard(strategy_id)
        effective_shard = (
            shard
            if shard is not None
            else random.Random(int(seed)).randrange(3)
        )
        return _KOU_21_99_DEEP_OFFSET + effective_shard + index * 3
    if problem_id in {"unsolvedmath-opg-369", "unsolvedmath-opg-600"}:
        return 1_000 + stratum + index * 97
    return stratum + index * 97


def _unpair(value: int) -> tuple[int, int]:
    diagonal = (math.isqrt(8 * value + 1) - 1) // 2
    start = diagonal * (diagonal + 1) // 2
    right = value - start
    return diagonal - right, right


def _untuple(value: int, length: int) -> tuple[int, ...]:
    values = []
    for _ in range(length - 1):
        left, value = _unpair(value)
        values.append(left)
    values.append(value)
    return tuple(values)


def _digits(value: int, base: int, length: int) -> tuple[int, ...]:
    result = []
    for _ in range(length):
        result.append(value % base)
        value //= base
    return tuple(result)


def _is_square(value: int) -> bool:
    return value >= 0 and math.isqrt(value) ** 2 == value


def _proper_divisor_sum(value: int) -> int:
    return int(sympy.divisor_sigma(value)) - value


def _fibonacci(index: int) -> int:
    return int(sympy.fibonacci(index))


def _perfect_power(value: int) -> tuple[int, int] | None:
    if value <= 1:
        return None
    for exponent in range(2, value.bit_length() + 1):
        base, exact = sympy.integer_nthroot(value, exponent)
        if exact and base > 1:
            return int(base), exponent
    return None


def _prime(index: int) -> int:
    return int(sympy.prime(max(1, index)))


def _run_gap_text(script: str, deadline: float | None = None) -> str:
    if not GAP_BINARY.exists() or not GAP_ROOT.exists():
        raise RuntimeError(f"isolated GAP is unavailable at {GAP_BINARY}")
    timeout = _remaining_timeout(deadline) if deadline is not None else 30.0
    try:
        completed = subprocess.run(
            [str(GAP_BINARY), "-l", str(GAP_ROOT), "-q"],
            input=script + "\nQUIT;\n",
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise _DeadlineExceeded from exc
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    if (
        completed.returncode != 0
        or stderr.strip()
        or "\nError," in "\n" + stdout
        or "brk>" in stdout
    ):
        raise RuntimeError(
            "isolated GAP failed: "
            + (stderr.strip() or stdout.strip() or f"exit {completed.returncode}")
        )
    return stdout


def _smallgroup_factor_family(order: int) -> str:
    factors = sympy.factorint(order)
    prime_count = len(factors)
    parity = "even" if order % 2 == 0 else "odd"
    if prime_count == 1:
        shape = "prime_power"
    elif prime_count == 2:
        shape = "two_prime"
    else:
        shape = "three_plus_prime"
    return f"{parity}_{shape}"


@lru_cache(maxsize=1)
def _kou_21_26_smallgroup_catalogue() -> tuple[tuple[int, int], ...]:
    output = _run_gap_text(
        """
for o in [61..255] do
 if SmallGroupsAvailable(o) then
  ids:=IdsOfAllSmallGroups(Size,o,IsAbelian,false);;
  for id in ids do Print("ID|",id[1],"|",id[2],"\\n"); od;
 fi;
od;
"""
    )
    by_order: dict[int, list[int]] = {}
    for raw in output.splitlines():
        if not raw.startswith("ID|"):
            continue
        _, order, index = raw.split("|")
        by_order.setdefault(int(order), []).append(int(index))
    if not by_order:
        raise RuntimeError("GAP returned no nonabelian SmallGroups catalogue entries")

    order_buckets: dict[str, list[int]] = {}
    for order in sorted(by_order):
        order_buckets.setdefault(_smallgroup_factor_family(order), []).append(order)
    ordered_orders: list[int] = []
    families = sorted(order_buckets)
    for position in range(max(map(len, order_buckets.values()))):
        for family in families:
            bucket = order_buckets[family]
            if position < len(bucket):
                ordered_orders.append(bucket[position])

    catalogue: list[tuple[int, int]] = []
    for depth in range(max(len(by_order[order]) for order in ordered_orders)):
        for order in ordered_orders:
            indices = by_order[order]
            if depth < len(indices):
                catalogue.append((order, indices[depth]))
    return tuple(catalogue)


@lru_cache(maxsize=1)
def _kou_21_26_catalogue_families() -> tuple[
    tuple[str, tuple[tuple[int, int, int], ...]], ...
]:
    buckets: dict[str, list[tuple[int, int, int]]] = {}
    for position, (order, group_index) in enumerate(
        _kou_21_26_smallgroup_catalogue()
    ):
        buckets.setdefault(_smallgroup_factor_family(order), []).append(
            (position, order, group_index)
        )
    return tuple(
        (family, tuple(buckets[family]))
        for family in sorted(buckets)
    )


@lru_cache(maxsize=1)
def _kou_21_26_catalogue_shards() -> tuple[
    tuple[tuple[str, int, int, int], ...], ...
]:
    family_buckets: list[list[list[tuple[str, int, int, int]]]] = [
        [[] for _family in _kou_21_26_catalogue_families()]
        for _shard in range(3)
    ]
    for family_index, (family, bucket) in enumerate(
        _kou_21_26_catalogue_families()
    ):
        for family_position, (
            catalogue_position,
            order,
            group_index,
        ) in enumerate(bucket):
            shard = (family_index + family_position) % 3
            family_buckets[shard][family_index].append(
                (family, catalogue_position, order, group_index)
            )

    shards: list[tuple[tuple[str, int, int, int], ...]] = []
    for buckets in family_buckets:
        ordered: list[tuple[str, int, int, int]] = []
        for row in itertools.zip_longest(*buckets):
            ordered.extend(entry for entry in row if entry is not None)
        shards.append(tuple(ordered))
    flattened = [
        (order, group_index)
        for shard in shards
        for _family, _position, order, group_index in shard
    ]
    if (
        len(flattened) != len(_kou_21_26_smallgroup_catalogue())
        or len(set(flattened)) != len(flattened)
        or set(flattened) != set(_kou_21_26_smallgroup_catalogue())
    ):
        raise RuntimeError("KOU-21.26 catalogue shards are not a partition")
    return tuple(shards)


def _kou_21_26_deep_case(index: int) -> dict[str, Any]:
    catalogue = _kou_21_26_smallgroup_catalogue()
    relative_index = int(index) - _KOU_21_26_DEEP_OFFSET
    shard = relative_index % 3
    shard_position = relative_index // 3
    shard_entries = _kou_21_26_catalogue_shards()[shard]
    if not 0 <= shard_position < len(shard_entries):
        raise _FiniteCatalogueExhausted
    family, position, order, group_index = shard_entries[shard_position]
    family_bucket = dict(_kou_21_26_catalogue_families())[family]
    family_position = next(
        offset
        for offset, (catalogue_position, _order, _group_index) in enumerate(
            family_bucket
        )
        if catalogue_position == position
    )
    return {
        "backend": "gap_smallgroups",
        "smallgroup_id": [order, group_index],
        "group_order": order,
        "catalogue_position": position,
        "catalogue_size": len(catalogue),
        "catalogue_family": family,
        "catalogue_family_position": family_position,
        "catalogue_family_size": len(family_bucket),
        "catalogue_shard": shard,
        "catalogue_shard_position": shard_position,
        "catalogue_shard_size": len(shard_entries),
        "catalogue_label": f"SmallGroup({order},{group_index})",
        "search_role": "nonabelian_smallgroups_orders_61_through_255",
    }


def _matching_extends_to_perfect(
    dimension: int,
    matching: Sequence[Sequence[int]],
) -> bool:
    used = {int(vertex) for edge in matching for vertex in edge}
    left = [
        vertex
        for vertex in range(1 << dimension)
        if vertex not in used and vertex.bit_count() % 2 == 0
    ]
    right = {
        vertex
        for vertex in range(1 << dimension)
        if vertex not in used and vertex.bit_count() % 2 == 1
    }
    if len(left) != len(right):
        return False
    matched_right: dict[int, int] = {}

    def augment(vertex: int, seen: set[int]) -> bool:
        for bit in range(dimension):
            other = vertex ^ (1 << bit)
            if other not in right or other in seen:
                continue
            seen.add(other)
            prior = matched_right.get(other)
            if prior is None or augment(prior, seen):
                matched_right[other] = vertex
                return True
        return False

    return all(augment(vertex, set()) for vertex in left)


def _hypercube_matching_case(index: int) -> dict[str, Any]:
    if index < 1_000:
        dimension = 2 + index % 4
        target_size = min(
            1 + index // 4,
            1 << (dimension - 1),
        )
    else:
        dimension = 6
        target_size = 16 + index % 15
    vertices = 1 << dimension
    edges = [
        (vertex, vertex ^ (1 << bit))
        for vertex in range(vertices)
        for bit in range(dimension)
        if vertex < (vertex ^ (1 << bit))
    ]
    generation_nonce = 0
    while True:
        rng = random.Random(0x600_000 + int(index) * 10_007 + generation_nonce)
        used: set[int] = set()
        matching: list[tuple[int, int]] = []
        if index >= 1_000:
            for bit in rng.sample(range(dimension), dimension):
                directional_edges = [
                    edge for edge in edges if (edge[0] ^ edge[1]) == 1 << bit
                ]
                rng.shuffle(directional_edges)
                edge = next(
                    (
                        candidate
                        for candidate in directional_edges
                        if not used.intersection(candidate)
                    ),
                    None,
                )
                if edge is None:
                    break
                matching.append(edge)
                used.update(edge)
            if len(matching) != dimension:
                generation_nonce += 1
                continue
        shuffled_edges = list(edges)
        rng.shuffle(shuffled_edges)
        for left, right in shuffled_edges:
            if left not in used and right not in used:
                matching.append((left, right))
                used.update((left, right))
                if len(matching) == target_size:
                    break
        if index < 1_000 or (
            len(matching) == target_size
            and not _matching_extends_to_perfect(dimension, matching)
        ):
            break
        generation_nonce += 1
        if generation_nonce > 10_000:
            raise RuntimeError("failed to generate an uncovered Q6 matching")
    return {
        "dimension": dimension,
        "matching_seed": int(index),
        "generation_nonce": generation_nonce,
        "target_size": target_size,
        "matching": [list(edge) for edge in sorted(matching)],
        "search_role": (
            "replication_d_le_5"
            if index < 1_000
            else "frontier_q6_uncovered_matching"
        ),
        "perfect_matching_extendable": _matching_extends_to_perfect(
            dimension, matching
        ),
    }


_KOU_21_99_ACTION_CANDIDATES: tuple[
    tuple[str, int, str, str], ...
] = (
    ("symmetric", 4, "three_cycle", "S4/C3"),
    ("symmetric", 4, "four_cycle", "S4/C4"),
    ("symmetric", 4, "klein_four", "S4/V4"),
    ("symmetric", 4, "two_point_stabilizer", "S4/S2"),
    ("symmetric", 4, "two_set_stabilizer", "S4/Stab(2-set)"),
    ("alternating", 4, "double_transposition", "A4/C2"),
    ("alternating", 4, "klein_four", "A4/V4"),
    ("alternating", 5, "double_transposition", "A5/C2"),
    ("alternating", 5, "three_cycle", "A5/C3"),
    ("alternating", 5, "five_cycle", "A5/C5"),
    ("alternating", 5, "klein_four", "A5/V4"),
    ("alternating", 5, "two_set_stabilizer", "A5/Stab(2-set)"),
    ("symmetric", 5, "point_stabilizer", "S5/S4"),
    ("symmetric", 5, "two_point_stabilizer", "S5/S3"),
    ("symmetric", 5, "two_set_stabilizer", "S5/Stab(2-set)"),
    ("symmetric", 5, "five_cycle", "S5/C5"),
    ("dihedral", 7, "reflection", "D14/C2"),
    ("dihedral", 7, "rotation", "D14/C7"),
    ("dihedral", 8, "reflection", "D16/C2"),
    ("dihedral", 8, "rotation_square", "D16/C4"),
    ("dihedral", 9, "reflection", "D18/C2"),
    ("dihedral", 9, "rotation_third", "D18/C3"),
    ("dihedral", 10, "reflection_rotation_square", "D20/D10"),
)


def _case(problem_id: str, index: int) -> dict[str, Any]:
    if problem_id == "unsolvedmath-comb-003":
        if index < _RAMSEY_DEEP_OFFSET:
            basin = "known_k42_extension"
        else:
            basin = (
                "known_k42_extension",
                "full_k43_restart",
                "perturbed_k42_extension",
            )[(index - _RAMSEY_DEEP_OFFSET) % 3]
        return {"order": 43, "attempt": index, "search_basin": basin}
    if problem_id == "unsolvedmath-nt-010":
        return {"n": index + 1}
    if problem_id in {"unsolvedmath-nt-026", "unsolvedmath-nt-050"}:
        return {"n": 2 * index + 1}
    if problem_id in {
        "unsolvedmath-nt-027",
        "unsolvedmath-nt-039",
        "unsolvedmath-nt-086",
    }:
        return {"n": index + 2}
    if problem_id == "unsolvedmath-guy-a7b":
        return {"n": index + 1}
    if problem_id == "unsolvedmath-nt-033":
        return {"start": index + 4}
    if problem_id in {
        "unsolvedmath-nt-043",
        "unsolvedmath-nt-044",
        "unsolvedmath-nt-053",
    }:
        return {"n": index + 1}
    if problem_id == "unsolvedmath-nt-046":
        left, right = _unpair(index)
        return {"a": left + 1, "b": right + 1}
    if problem_id == "unsolvedmath-nt-078":
        values = _untuple(index, 6)
        return {
            "A": values[0] + 1,
            "B": values[1] + 1,
            "C": values[2] + 1,
            "x": values[3] + 3,
            "y": values[4] + 3,
            "z": values[5] + 3,
        }
    if problem_id == "unsolvedmath-guy-a12b":
        block, residue = divmod(index, 2)
        return {"n": 10 * block + (3 if residue == 0 else 7)}
    if problem_id == "unsolvedmath-guy-a19a":
        return {"n": index + 3}
    if problem_id in {"unsolvedmath-opg-148", "unsolvedmath-opg-151"}:
        prime_index, matrix_code = _unpair(index)
        p = _prime(prime_index + (3 if problem_id.endswith("148") else 1))
        n = 1 + (matrix_code % 3)
        code = matrix_code // 3
        return {
            "p": p,
            "n": n,
            "matrix": [
                list(_digits(code, p, n * n)[row * n : (row + 1) * n])
                for row in range(n)
            ],
        }
    if problem_id == "unsolvedmath-opg-16570":
        a, b, c = _untuple(index, 3)
        return {"a": a + 1, "b": b + 1, "c": c + 1}
    if problem_id == "unsolvedmath-opg-37221":
        a, b, c = _untuple(index, 3)
        return {"edges": [a + 1, b + 1, c + 1]}
    if problem_id == "unsolvedmath-opg-369":
        moduli = (4, 6, 8, 9, 10, 12)
        modulus = moduli[index % len(moduli)]
        if index < 24:
            vertices = 2 + (index // len(moduli)) % 3
            code = index // (len(moduli) * 3)
            edge_count = math.comb(vertices, 2)
            graph_mask = code % (1 << edge_count)
            weight_code = code // (1 << edge_count)
            weights = list(_digits(weight_code, modulus, edge_count))
        else:
            vertices = 5 + (index // len(moduli)) % 3
            all_edges = tuple(itertools.combinations(range(vertices), 2))
            rng = random.Random(0x369_000 + int(index))
            chosen = {
                tuple(sorted((vertex, vertex + 1)))
                for vertex in range(vertices - 1)
            }
            chosen.update(
                edge for edge in all_edges if rng.random() < 0.45
            )
            graph_mask = sum(
                1 << edge_index
                for edge_index, edge in enumerate(all_edges)
                if edge in chosen
            )
            weights = [rng.randrange(modulus) for _ in all_edges]
        return {
            "modulus": modulus,
            "vertices": vertices,
            "graph_mask": graph_mask,
            "weights": weights,
        }
    if problem_id in {
        "unsolvedmath-opg-1793",
        "unsolvedmath-opg-46385",
    }:
        n = 2 + index % 4
        return {"vertices": n, "arc_mask": index // 4}
    if problem_id.startswith("unsolvedmath-comb-001"):
        n = 2 + index % 4
        return {"size": n, "relation_mask": index // 4}
    if problem_id == "unsolvedmath-alg-007":
        degree = 2 + index % 4
        coeff_code = index // 4
        coefficients = [digit - 2 for digit in _digits(coeff_code, 5, degree)]
        return {"coefficients": [1, *coefficients]}
    if problem_id == "unsolvedmath-kou-21.26":
        if index >= _KOU_21_26_DEEP_OFFSET:
            return _kou_21_26_deep_case(index)
        catalogue = (
            ("symmetric", 3, "S3"),
            ("alternating", 4, "A4"),
            ("dihedral", 6, "D12"),
            ("symmetric", 4, "S4"),
            ("alternating", 5, "A5"),
            ("dihedral", 10, "D20"),
        )
        family, parameter, label = catalogue[index % len(catalogue)]
        return {
            "family": family,
            "parameter": parameter,
            "catalogue_label": label,
        }
    if problem_id == "unsolvedmath-opg-600":
        return _hypercube_matching_case(index)
    if problem_id == "unsolvedmath-opg-382":
        if index == 0:
            return {
                "ground_size": 2,
                "k": 2,
                "ell": 1,
                "matroid_codes": [0, 0],
            }
        ground_size = 2 + (index - 1) % 4
        k = 4 + ((index - 1) // 4) % 2
        ell = 1 + ((index - 1) // 8) % ground_size
        code = (index - 1) // (8 * ground_size)
        return {
            "ground_size": ground_size,
            "k": k,
            "ell": ell,
            "matroid_codes": list(_digits(code, 8, k)),
        }
    if problem_id == "unsolvedmath-opg-37670":
        return {"vertices": 10, "missing_edge_mask": index}
    if problem_id == "unsolvedmath-opg-404":
        ell = 2 + index % 2
        return {"k": ell + index // 2, "ell": ell}
    if problem_id == "unsolvedmath-opg-636":
        return {"order": 2 * (index + 1)}
    if problem_id == "unsolvedmath-kou-21.99":
        if index >= _KOU_21_99_DEEP_OFFSET:
            return _kou_21_99_deep_case(index)
        catalogue = (
            ("symmetric", 3, "transposition", "S3/C2"),
            ("alternating", 4, "three_cycle", "A4/C3"),
            ("dihedral", 6, "reflection", "D12/C2"),
            ("symmetric", 4, "point_stabilizer", "S4/S3"),
            ("alternating", 5, "point_stabilizer", "A5/A4"),
            ("dihedral", 10, "reflection", "D20/C2"),
        )
        family, parameter, subgroup_kind, label = catalogue[
            index % len(catalogue)
        ]
        return {
            "family": family,
            "parameter": parameter,
            "subgroup_kind": subgroup_kind,
            "catalogue_label": label,
        }
    if problem_id == "unsolvedmath-opg-169":
        n = 2 + index % 3
        return {"vertices": n, "orientation_code": index // 3}
    if problem_id == "unsolvedmath-opg-48264":
        if index >= _OPG_48264_DEEP_OFFSET:
            position = index - _OPG_48264_DEEP_OFFSET
            catalogue = _opg_48264_deep_catalogue()
            if not 0 <= position < len(catalogue):
                raise _FiniteCatalogueExhausted
            shard = position % 3
            shard_position = position // 3
            shard_size = len(range(shard, len(catalogue), 3))
            return {
                "family": "nauty_cubic_18",
                "level": position,
                "catalogue_position": position,
                "catalogue_size": len(catalogue),
                "catalogue_shard": shard,
                "catalogue_shard_position": shard_position,
                "catalogue_shard_size": shard_size,
                "catalogue_label": f"nauty-cubic-18:{position}",
                "search_role": "nonisomorphic_cubic_order_18",
            }
        families = (
            "prism",
            "mobius_ladder",
            "petersen",
            "circulant4",
            "bipartite_quartic",
            "quartic_circulant",
        )
        return {
            "family": families[index % len(families)],
            "level": index // len(families),
        }
    raise KeyError(problem_id)


class _FiniteCatalogueExhausted(RuntimeError):
    pass


class _DeadlineExceeded(RuntimeError):
    pass


def _check_deadline(deadline: float | None) -> None:
    if deadline is not None and time.monotonic() >= deadline:
        raise _DeadlineExceeded


def _maximum_matching_exists(
    divisor_sets: Sequence[set[int]],
    deadline: float | None = None,
) -> bool:
    """Decide the divisor assignment with an augmenting-path matching."""

    matched_prime: dict[int, int] = {}

    def augment(number_index: int, seen: set[int]) -> bool:
        _check_deadline(deadline)
        for prime in sorted(divisor_sets[number_index]):
            if prime in seen:
                continue
            seen.add(prime)
            prior = matched_prime.get(prime)
            if prior is None or augment(prior, seen):
                matched_prime[prime] = number_index
                return True
        return False

    for number_index in sorted(
        range(len(divisor_sets)), key=lambda index: len(divisor_sets[index])
    ):
        if not augment(number_index, set()):
            return False
    return True


def _addition_chain_length(
    target: int, deadline: float | None = None
) -> int:
    if target <= 1:
        return 0
    frontier = {(1,)}
    for depth in range(1, target):
        next_frontier: set[tuple[int, ...]] = set()
        for chain in frontier:
            _check_deadline(deadline)
            additions = {
                chain[left] + chain[right]
                for left in range(len(chain))
                for right in range(left, len(chain))
                if chain[left] + chain[right] > chain[-1]
                and chain[left] + chain[right] <= target
            }
            for value in additions:
                if value == target:
                    return depth
                next_frontier.add((*chain, value))
        frontier = next_frontier
    raise RuntimeError(f"addition-chain search failed for {target}")


def _has_subset_sum(values: Sequence[int], target: int) -> bool:
    reachable = 1
    mask = (1 << (target + 1)) - 1
    for value in values:
        reachable |= reachable << value
        reachable &= mask
    return bool(reachable & (1 << target))


def _matrix_det_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    return int(sympy.Matrix(matrix).det()) % modulus


def _permanent_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    size = len(matrix)
    total = 0
    for permutation in itertools.permutations(range(size)):
        product = 1
        for row, column in enumerate(permutation):
            product = product * int(matrix[row][column]) % modulus
        total = (total + product) % modulus
    return total


def _directed_edges(vertices: int, mask: int) -> tuple[tuple[int, int], ...]:
    pairs = [
        (left, right)
        for left in range(vertices)
        for right in range(vertices)
        if left != right
    ]
    return tuple(pair for bit, pair in enumerate(pairs) if mask & (1 << bit))


def _is_acyclic(vertices: Iterable[int], edges: Iterable[tuple[int, int]]) -> bool:
    vertex_set = set(vertices)
    adjacency = {vertex: [] for vertex in vertex_set}
    indegree = {vertex: 0 for vertex in vertex_set}
    for left, right in edges:
        if left in vertex_set and right in vertex_set:
            adjacency[left].append(right)
            indegree[right] += 1
    ready = [vertex for vertex, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        vertex = ready.pop()
        visited += 1
        for neighbour in adjacency[vertex]:
            indegree[neighbour] -= 1
            if indegree[neighbour] == 0:
                ready.append(neighbour)
    return visited == len(vertex_set)


def _directed_cycles(
    vertices: int,
    edges: Iterable[tuple[int, int]],
    *,
    max_length: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    edge_set = set(edges)
    cycles: set[tuple[int, ...]] = set()
    upper = vertices if max_length is None else min(vertices, max_length)
    for length in range(2, upper + 1):
        for sequence in itertools.permutations(range(vertices), length):
            if sequence[0] != min(sequence):
                continue
            if all(
                (sequence[index], sequence[(index + 1) % length]) in edge_set
                for index in range(length)
            ):
                cycles.add(sequence)
    return tuple(sorted(cycles))


def _minimum_feedback_size(
    vertices: int, edges: Sequence[tuple[int, int]]
) -> int:
    for size in range(len(edges) + 1):
        for removed in itertools.combinations(range(len(edges)), size):
            removed_set = set(removed)
            remaining = [
                edge
                for index, edge in enumerate(edges)
                if index not in removed_set
            ]
            if _is_acyclic(range(vertices), remaining):
                return size
    return len(edges)


def _rank_gf2(columns: Sequence[int]) -> int:
    basis: dict[int, int] = {}
    for value in columns:
        vector = int(value)
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return len(basis)


def _flat_counts(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    if not matrix or not matrix[0]:
        return (1,)
    row_count = len(matrix)
    column_count = len(matrix[0])
    columns = [
        sum((int(matrix[row][column]) & 1) << row for row in range(row_count))
        for column in range(column_count)
    ]
    flats: list[tuple[int, int]] = []
    for mask in range(1 << column_count):
        selected = [
            columns[index]
            for index in range(column_count)
            if mask & (1 << index)
        ]
        rank = _rank_gf2(selected)
        closure = mask
        for index, column in enumerate(columns):
            if _rank_gf2([*selected, column]) == rank:
                closure |= 1 << index
        if closure == mask:
            flats.append((mask, rank))
    matroid_rank = _rank_gf2(columns)
    return tuple(
        sum(1 for _, rank in flats if rank == level)
        for level in range(matroid_rank + 1)
    )


def _is_unimodal(values: Sequence[int]) -> bool:
    falling = False
    for left, right in zip(values, values[1:]):
        if right < left:
            falling = True
        elif falling and right > left:
            return False
    return True


def _clique_number(
    vertices: int,
    edges: set[tuple[int, int]],
    deadline: float | None,
) -> int:
    for size in range(vertices, 0, -1):
        for subset in itertools.combinations(range(vertices), size):
            _check_deadline(deadline)
            if all(tuple(sorted(edge)) in edges for edge in itertools.combinations(subset, 2)):
                return size
    return 0


def _chromatic_number(
    vertices: int,
    edges: set[tuple[int, int]],
    lower_bound: int,
    deadline: float | None,
) -> int:
    adjacency = {
        vertex: {
            right if left == vertex else left
            for left, right in edges
            if vertex in (left, right)
        }
        for vertex in range(vertices)
    }
    order = sorted(range(vertices), key=lambda vertex: -len(adjacency[vertex]))

    def colorable(color_count: int) -> bool:
        colors = [-1] * vertices

        def assign(position: int) -> bool:
            _check_deadline(deadline)
            if position == vertices:
                return True
            vertex = order[position]
            forbidden = {colors[other] for other in adjacency[vertex]}
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if assign(position + 1):
                    colors[vertex] = -1
                    return True
                colors[vertex] = -1
            return False

        return assign(0)

    for color_count in range(max(1, lower_bound), vertices + 1):
        if colorable(color_count):
            return color_count
    return vertices


def _contains_progression(
    coloring: Sequence[int], length: int, color: int
) -> bool:
    if length <= 1:
        return any(value == color for value in coloring)
    size = len(coloring)
    return any(
        all(coloring[start + step * offset] == color for offset in range(length))
        for step in range(1, size)
        for start in range(size)
        if start + step * (length - 1) < size
    )


def _van_der_waerden(
    red_length: int,
    blue_length: int,
    deadline: float | None = None,
) -> int:
    z3 = shutil.which("z3")
    if z3 is None:
        raise RuntimeError("the exact mixed van der Waerden search requires z3")

    def progressions(size: int, length: int) -> Iterable[tuple[int, ...]]:
        if length <= 0:
            yield ()
            return
        if length == 1:
            yield from ((index,) for index in range(size))
            return
        for start in range(size):
            for step in range(1, size + 1):
                values = tuple(start + offset * step for offset in range(length))
                if values[-1] >= size:
                    break
                yield values

    for size in itertools.count(1):
        _check_deadline(deadline)
        variables = [f"x_{index}" for index in range(size)]
        lines = ["(set-logic QF_BOOL)"]
        lines.extend(f"(declare-fun {variable} () Bool)" for variable in variables)
        for sequence in progressions(size, red_length):
            if not sequence:
                lines.append("(assert false)")
            else:
                terms = " ".join(f"(not {variables[index]})" for index in sequence)
                lines.append(f"(assert (or {terms}))")
        for sequence in progressions(size, blue_length):
            if not sequence:
                lines.append("(assert false)")
            else:
                terms = " ".join(variables[index] for index in sequence)
                lines.append(f"(assert (or {terms}))")
        lines.append("(check-sat)")
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise _DeadlineExceeded
        try:
            completed = subprocess.run(
                [z3, "-in"],
                input="\n".join(lines) + "\n",
                text=True,
                capture_output=True,
                timeout=remaining,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise _DeadlineExceeded from exc
        answer = completed.stdout.strip().splitlines()
        if completed.returncode != 0 or not answer:
            detail = (completed.stderr or completed.stdout).strip()
            raise RuntimeError(f"z3 mixed van der Waerden check failed: {detail}")
        if answer[-1] == "unsat":
            return size
        if answer[-1] != "sat":
            raise RuntimeError(
                f"z3 returned an unexpected mixed van der Waerden result: {answer[-1]}"
            )


def _permutation_sign(permutation: Sequence[int]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def _latin_parity_counts(
    order: int, deadline: float | None = None
) -> tuple[int, int, int]:
    if order > 4:
        raise ValueError("exact Latin-square enumeration is capped at order 4")
    permutations = tuple(itertools.permutations(range(order)))
    even = odd = total = 0
    for rows in itertools.product(permutations, repeat=order):
        _check_deadline(deadline)
        if any(
            len({rows[row][column] for row in range(order)}) != order
            for column in range(order)
        ):
            continue
        sign = math.prod(_permutation_sign(row) for row in rows)
        sign *= math.prod(
            _permutation_sign(tuple(rows[row][column] for row in range(order)))
            for column in range(order)
        )
        total += 1
        if sign == 1:
            even += 1
        else:
            odd += 1
    return even, odd, total


def _cyclic_group(degree: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((point + shift) % degree for point in range(degree))
        for shift in range(degree)
    )


# Published K42 witness: https://cs.indstate.edu/ge/RAMSEY/g55.42
_RAMSEY_55_K42_ROWS = (
    "001110000000111011011011101101110000000110",
    "000111000000011101101111110110111000000011",
    "100011100000001110110111011011011100000001",
    "110001110000000111011011001101101110001000",
    "111000111000000011101101100110110111000000",
    "011100011100000001110110111111011011100000",
    "001110001110000000111011011111101101110000",
    "000111000111000000011101101100110110111000",
    "000011100011100000001110110110011011011100",
    "000001110001110000000111011011010101101110",
    "000000111000111000000011101101101110110111",
    "000000011100011100000001110110110011011011",
    "100000001110001110000000111011011001101101",
    "110000000111000111000000011101101101110110",
    "111000000011100011100000001110110111111011",
    "011100000001110001110000001111011011101101",
    "101110000000111000111000000011101101100110",
    "110111000000011100011100000001110110110011",
    "011011100000001110001110000000111011011111",
    "101101110000000111000111000000011101101111",
    "110110111000000011100011100000001110110110",
    "011011011100000001110001110000000111011011",
    "111101101110000000111000111000000011101101",
    "111110110111000000011100011100000001110110",
    "110011011011100000001110001110000000111011",
    "011001101101110000000111000111000000011101",
    "101101110110111100000011100011100000001110",
    "110111111011011100000001110001110000000111",
    "011011101101101110000000111000111000000011",
    "101101100110110111000000011100011100000001",
    "110110110011011011100000001110001110000000",
    "111011011101101101110000000111000111000000",
    "011101101010110110111000000011100011100000",
    "001110110110011011011100000001110001110000",
    "000111011011001101101110000000111000111000",
    "000011101101111110110111000000011100011100",
    "000001110110111111011011100000001110001110",
    "000000111011011001101101110000000111000111",
    "000100011101101100110110111000000011100011",
    "100000001110110110111011011100000001110001",
    "110000000111011011111101101110000000111000",
    "011000000011101101110110110111000000011100",
)


@lru_cache(maxsize=1)
def _ramsey_k43_search_arrays() -> tuple[
    tuple[tuple[int, int], ...],
    numpy.ndarray,
    numpy.ndarray,
    numpy.ndarray,
]:
    order = 43
    edges = tuple(itertools.combinations(range(43), 2))
    edge_lookup = numpy.zeros((order, order), dtype=numpy.uint16)
    for edge_index, (left, right) in enumerate(edges):
        edge_lookup[left, right] = edge_lookup[right, left] = edge_index
    five_set_count = math.comb(order, 5)
    five_sets = numpy.fromiter(
        itertools.chain.from_iterable(
            itertools.combinations(range(order), 5)
        ),
        dtype=numpy.uint8,
        count=five_set_count * 5,
    ).reshape(five_set_count, 5)
    pair_positions = tuple(itertools.combinations(range(5), 2))
    five_set_edges = numpy.empty(
        (five_set_count, len(pair_positions)),
        dtype=numpy.uint16,
    )
    for column, (left, right) in enumerate(pair_positions):
        five_set_edges[:, column] = edge_lookup[
            five_sets[:, left],
            five_sets[:, right],
        ]

    incidence_count = math.comb(order - 2, 3)
    incidence = numpy.empty(
        (len(edges), incidence_count),
        dtype=numpy.uint32,
    )
    triple_count = math.comb(order, 3)
    triples = numpy.fromiter(
        itertools.chain.from_iterable(
            itertools.combinations(range(order), 3)
        ),
        dtype=numpy.uint8,
        count=triple_count * 3,
    ).reshape(triple_count, 3)
    binomial = numpy.asarray(
        [
            [
                math.comb(value, width) if width <= value else 0
                for width in range(6)
            ]
            for value in range(order + 1)
        ],
        dtype=numpy.uint32,
    )
    for edge_index, (left, right) in enumerate(edges):
        remaining = triples[
            numpy.all(
                (triples != left) & (triples != right),
                axis=1,
            )
        ]
        vertices = numpy.empty((incidence_count, 5), dtype=numpy.uint8)
        vertices[:, :2] = (left, right)
        vertices[:, 2:] = remaining
        vertices.sort(axis=1)
        ranks = numpy.zeros(incidence_count, dtype=numpy.uint32)
        previous = numpy.full(incidence_count, -1, dtype=numpy.int16)
        for position in range(5):
            current = vertices[:, position].astype(numpy.int16)
            width = 5 - position
            ranks += (
                binomial[order - (previous + 1), width]
                - binomial[order - current, width]
            )
            previous = current
        incidence[edge_index] = ranks
    k42_mask = numpy.all(five_sets < 42, axis=1)
    return edges, five_set_edges, incidence, k42_mask


def _known_k42_edge_colors() -> dict[tuple[int, int], int]:
    return {
        (left, right): int(_RAMSEY_55_K42_ROWS[left][right])
        for left, right in itertools.combinations(range(42), 2)
    }


def _monochromatic_rows(
    colors: numpy.ndarray,
    five_set_edges: numpy.ndarray,
) -> numpy.ndarray:
    selected = colors[five_set_edges]
    return numpy.all(selected == selected[:, :1], axis=1)


def _full_k43_ramsey_search(
    attempt: int,
    max_flips: int,
    deadline: float | None,
    metrics: dict[str, Any] | None,
) -> dict[str, Any] | None:
    _check_deadline(deadline)
    edges, five_set_edges, incidence, _ = _ramsey_k43_search_arrays()
    _check_deadline(deadline)
    rng = random.Random(0x55_F00 + int(attempt))
    colors = numpy.fromiter(
        (rng.randrange(2) for _ in edges),
        dtype=numpy.uint8,
        count=len(edges),
    )
    conflicts = _monochromatic_rows(colors, five_set_edges)
    initial_conflicts = int(numpy.count_nonzero(conflicts))
    best_conflicts = initial_conflicts
    active_edges: set[int] = set()
    trajectory = hashlib.sha256(
        f"full:{attempt}:{colors.tobytes().hex()}:{initial_conflicts}".encode()
    )
    flips = 0
    for _ in range(max(0, int(max_flips))):
        _check_deadline(deadline)
        conflict_ids = numpy.flatnonzero(conflicts)
        if not len(conflict_ids):
            break
        conflict_id = int(conflict_ids[rng.randrange(len(conflict_ids))])
        variables = list(map(int, five_set_edges[conflict_id]))
        if rng.random() < 0.08:
            chosen_edge = rng.choice(variables)
        else:
            candidates = rng.sample(variables, min(4, len(variables)))
            scored = []
            for edge_index in candidates:
                affected = incidence[edge_index]
                before = int(numpy.count_nonzero(conflicts[affected]))
                colors[edge_index] ^= 1
                after_mask = _monochromatic_rows(
                    colors,
                    five_set_edges[affected],
                )
                colors[edge_index] ^= 1
                scored.append(
                    (
                        int(numpy.count_nonzero(after_mask)) - before,
                        rng.random(),
                        edge_index,
                    )
                )
            chosen_edge = min(scored)[2]
        colors[chosen_edge] ^= 1
        affected = incidence[chosen_edge]
        conflicts[affected] = _monochromatic_rows(
            colors,
            five_set_edges[affected],
        )
        active_edges.add(chosen_edge)
        flips += 1
        conflict_count = int(numpy.count_nonzero(conflicts))
        if conflict_count < best_conflicts:
            best_conflicts = conflict_count
            trajectory.update(f"{flips}:{best_conflicts};".encode())
    if metrics is not None:
        metrics.update(
            {
                "flips": flips,
                "best_conflicts": best_conflicts,
                "initial_conflicts": initial_conflicts,
                "trajectory_hash": trajectory.hexdigest(),
                "initialization": "full_random_K43",
                "search_basin": "full_k43_restart",
                "active_edge_count": len(active_edges),
                "edge_space_size": len(edges),
                "base_coloring_sha256": None,
            }
        )
    if numpy.any(conflicts):
        return None
    color_list = list(map(int, colors))
    return {
        "order": 43,
        "edges": [list(edge) for edge in edges],
        "colors": color_list,
        "monochromatic_k5_count": 0,
    }


def _perturbed_k42_edge_colors(
    attempt: int,
    deadline: float | None,
    metrics: dict[str, Any] | None,
) -> dict[tuple[int, int], int]:
    edges, five_set_edges, incidence, k42_mask = _ramsey_k43_search_arrays()
    edge_lookup = {edge: index for index, edge in enumerate(edges)}
    colors = numpy.zeros(len(edges), dtype=numpy.uint8)
    known = _known_k42_edge_colors()
    for edge, color in known.items():
        colors[edge_lookup[edge]] = color
    rng = random.Random(0x55_BA5E + int(attempt))
    target = 8 + abs(int(attempt)) % 17
    accepted = 0
    proposals = 0
    changed: set[int] = set()
    k42_edges = [
        edge_lookup[edge] for edge in itertools.combinations(range(42), 2)
    ]
    while accepted < target and proposals < target * 500:
        _check_deadline(deadline)
        proposals += 1
        edge_index = rng.choice(k42_edges)
        affected = incidence[edge_index]
        affected_k42 = affected[k42_mask[affected]]
        colors[edge_index] ^= 1
        creates_conflict = bool(
            numpy.any(
                _monochromatic_rows(
                    colors,
                    five_set_edges[affected_k42],
                )
            )
        )
        if creates_conflict:
            colors[edge_index] ^= 1
            continue
        accepted += 1
        if int(colors[edge_index]) == known[edges[edge_index]]:
            changed.discard(edge_index)
        else:
            changed.add(edge_index)
    if not changed:
        raise RuntimeError("failed to construct a distinct legal K42 base")
    result = {
        edge: int(colors[edge_lookup[edge]])
        for edge in itertools.combinations(range(42), 2)
    }
    base_hash = hashlib.sha256(
        bytes(result[edge] for edge in sorted(result))
    ).hexdigest()
    if metrics is not None:
        metrics.update(
            {
                "base_perturbation_accepts": accepted,
                "base_perturbation_proposals": proposals,
                "base_changed_edges": len(changed),
                "base_coloring_sha256": base_hash,
            }
        )
    return result


def _ramsey_55_conflicts(
    colors: Sequence[int],
    edge_index: Mapping[tuple[int, int], int],
    deadline: float | None,
) -> set[tuple[int, ...]]:
    conflicts: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(43), 5):
        _check_deadline(deadline)
        edge_colors = {
            colors[edge_index[(left, right)]]
            for left, right in itertools.combinations(vertices, 2)
        }
        if len(edge_colors) == 1:
            conflicts.add(vertices)
    return conflicts


def _search_ramsey_55(
    attempt: int,
    max_flips: int,
    deadline: float | None,
    metrics: dict[str, Any] | None = None,
    search_basin: str = "known_k42_extension",
) -> dict[str, Any] | None:
    if metrics is not None:
        metrics["max_flips_configured"] = max(0, int(max_flips))
    if search_basin == "full_k43_restart":
        return _full_k43_ramsey_search(
            attempt,
            max_flips,
            deadline,
            metrics,
        )
    if search_basin == "perturbed_k42_extension":
        base_colors = _perturbed_k42_edge_colors(
            attempt,
            deadline,
            metrics,
        )
        initialization = "legal_perturbed_K42_extension"
    elif search_basin == "known_k42_extension":
        base_colors = _known_k42_edge_colors()
        initialization = "known_K42_extension"
        if metrics is not None:
            metrics["base_coloring_sha256"] = hashlib.sha256(
                bytes(base_colors[edge] for edge in sorted(base_colors))
            ).hexdigest()
    else:
        raise ValueError(f"unsupported Ramsey search basin {search_basin!r}")
    edges = tuple(itertools.combinations(range(43), 2))
    rng = random.Random(0x55_000 + int(attempt))
    extension = [rng.randrange(2) for _ in range(42)]
    trajectory = hashlib.sha256(
        f"{attempt}:{''.join(map(str, extension))}:initializing".encode()
    )
    if metrics is not None:
        metrics.update(
            {
                "flips": 0,
                "best_conflicts": None,
                "initial_conflicts": None,
                "trajectory_hash": trajectory.hexdigest(),
                "initialization": initialization,
                "search_basin": search_basin,
                "active_edge_count": 0,
                "edge_space_size": len(edges),
            }
        )
    constraints: list[tuple[tuple[int, int, int, int], int]] = []
    incidence: list[list[int]] = [[] for _ in range(42)]
    for vertices in itertools.combinations(range(42), 4):
        _check_deadline(deadline)
        clique_colors = {
            int(base_colors[(left, right)])
            for left, right in itertools.combinations(vertices, 2)
        }
        if len(clique_colors) != 1:
            continue
        constraint_index = len(constraints)
        constraints.append((vertices, next(iter(clique_colors))))
        for vertex in vertices:
            incidence[vertex].append(constraint_index)
    conflict_list: list[int] = []
    conflict_position: dict[int, int] = {}

    def is_conflict(constraint_index: int) -> bool:
        vertices, color = constraints[constraint_index]
        return all(extension[vertex] == color for vertex in vertices)

    def add_conflict(constraint_index: int) -> None:
        if constraint_index not in conflict_position:
            conflict_position[constraint_index] = len(conflict_list)
            conflict_list.append(constraint_index)

    def remove_conflict(constraint_index: int) -> None:
        position = conflict_position.pop(constraint_index, None)
        if position is None:
            return
        last = conflict_list.pop()
        if position < len(conflict_list):
            conflict_list[position] = last
            conflict_position[last] = position

    for constraint_index in range(len(constraints)):
        if is_conflict(constraint_index):
            add_conflict(constraint_index)
    flips = 0
    best_conflicts = len(conflict_list)
    trajectory.update(f":{best_conflicts}".encode())
    if metrics is not None:
        metrics.update(
            {
                "flips": flips,
                "best_conflicts": best_conflicts,
                "initial_conflicts": len(conflict_list),
                "trajectory_hash": trajectory.hexdigest(),
                "initialization": initialization,
                "search_basin": search_basin,
            }
        )
    active_vertices: set[int] = set()
    for _ in range(max(0, int(max_flips))):
        _check_deadline(deadline)
        if not conflict_list:
            colors = [
                (
                    extension[left]
                    if right == 42
                    else int(base_colors[(left, right)])
                )
                for left, right in edges
            ]
            return {
                "order": 43,
                "edges": [list(edge) for edge in edges],
                "colors": colors,
                "monochromatic_k5_count": 0,
            }
        constraint_index = conflict_list[rng.randrange(len(conflict_list))]
        vertices, _ = constraints[constraint_index]
        if rng.random() < 0.04:
            chosen_vertex = rng.choice(vertices)
        else:
            scored = []
            for vertex in vertices:
                current = sum(
                    other in conflict_position for other in incidence[vertex]
                )
                extension[vertex] ^= 1
                after = sum(
                    is_conflict(other) for other in incidence[vertex]
                )
                extension[vertex] ^= 1
                scored.append((after - current, rng.random(), vertex))
            chosen_vertex = min(scored)[2]
        extension[chosen_vertex] ^= 1
        active_vertices.add(chosen_vertex)
        for affected in incidence[chosen_vertex]:
            if is_conflict(affected):
                add_conflict(affected)
            else:
                remove_conflict(affected)
        flips += 1
        if len(conflict_list) < best_conflicts:
            best_conflicts = len(conflict_list)
            trajectory.update(f"{flips}:{best_conflicts};".encode())
        if metrics is not None:
            metrics.update(
                {
                    "flips": flips,
                    "best_conflicts": best_conflicts,
                    "trajectory_hash": trajectory.hexdigest(),
                    "active_edge_count": len(active_vertices),
                }
            )
    if not conflict_list:
        colors = [
            (
                extension[left]
                if right == 42
                else int(base_colors[(left, right)])
            )
            for left, right in edges
        ]
        return {
            "order": 43,
            "edges": [list(edge) for edge in edges],
            "colors": colors,
            "monochromatic_k5_count": 0,
        }
    return None


def _graphic_rank(
    vertices: int,
    edges: Sequence[tuple[int, int]],
    selected: Iterable[int],
) -> int:
    parent = list(range(vertices))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    rank = 0
    for index in selected:
        left, right = edges[int(index)]
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
            rank += 1
    return rank


def _evaluate_many_weights(
    case: Mapping[str, Any],
    deadline: float | None,
) -> dict[str, Any] | None:
    modulus = int(case["modulus"])
    vertices = int(case["vertices"])
    all_edges = tuple(itertools.combinations(range(vertices), 2))
    graph_mask = int(case["graph_mask"])
    edges = tuple(
        edge for bit, edge in enumerate(all_edges) if graph_mask & (1 << bit)
    )
    raw_weights = tuple(map(int, case["weights"]))
    weights = tuple(
        raw_weights[all_edges.index(edge)] % modulus for edge in edges
    )
    rank = _graphic_rank(vertices, edges, range(len(edges)))
    bases = []
    for selected in itertools.combinations(range(len(edges)), rank):
        _check_deadline(deadline)
        if _graphic_rank(vertices, edges, selected) == rank:
            bases.append(selected)
    weight_set = {
        sum(weights[index] for index in base) % modulus for base in bases
    }
    stabilizer = {
        shift
        for shift in range(modulus)
        if {(value + shift) % modulus for value in weight_set} == weight_set
    }
    unseen = set(range(modulus))
    cosets: list[set[int]] = []
    while unseen:
        representative = min(unseen)
        coset = {(representative + value) % modulus for value in stabilizer}
        cosets.append(coset)
        unseen -= coset
    preimage_ranks = []
    for coset in cosets:
        _check_deadline(deadline)
        selected = [index for index, weight in enumerate(weights) if weight in coset]
        preimage_ranks.append(_graphic_rank(vertices, edges, selected))
    right_factor = 1 - rank + sum(preimage_ranks)
    right_side = len(stabilizer) * right_factor
    if len(weight_set) < right_side:
        return {
            "modulus": modulus,
            "vertices": vertices,
            "edges": [list(edge) for edge in edges],
            "weights": list(weights),
            "rank": rank,
            "bases": [list(base) for base in bases],
            "S": sorted(weight_set),
            "H": sorted(stabilizer),
            "cosets": [sorted(coset) for coset in cosets],
            "preimage_ranks": preimage_ranks,
            "left_side": len(weight_set),
            "right_side": right_side,
        }
    return None


def _hypercube_edges(dimension: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        (vertex, vertex ^ (1 << bit))
        for vertex in range(1 << dimension)
        for bit in range(dimension)
        if vertex < (vertex ^ (1 << bit))
    )


def _validated_hypercube_matching(
    dimension: int, raw_matching: Any
) -> tuple[tuple[int, int], ...] | None:
    if (
        not 1 <= dimension <= 6
        or not isinstance(raw_matching, Sequence)
        or isinstance(raw_matching, (str, bytes))
    ):
        return None
    vertex_count = 1 << dimension
    matching = []
    used: set[int] = set()
    for raw_edge in raw_matching:
        if (
            not isinstance(raw_edge, Sequence)
            or isinstance(raw_edge, (str, bytes))
            or len(raw_edge) != 2
        ):
            return None
        left, right = map(int, raw_edge)
        if left > right:
            left, right = right, left
        difference = left ^ right
        if (
            not 0 <= left < right < vertex_count
            or difference <= 0
            or difference & (difference - 1)
            or left in used
            or right in used
        ):
            return None
        used.update((left, right))
        matching.append((left, right))
    if len(set(matching)) != len(matching):
        return None
    return tuple(sorted(matching))


def _smt_exactly_one(names: Iterable[str]) -> str:
    terms = " ".join(f"(ite {name} 1 0)" for name in names)
    return f"(= (+ {terms}) 1)"


def _hamiltonian_successor_smt(
    dimension: int,
    matching: Sequence[tuple[int, int]],
    deadline: float | None,
) -> str:
    vertex_count = 1 << dimension
    edges = _hypercube_edges(dimension)
    arcs = tuple(
        (left, right) for edge in edges for left, right in (edge, edge[::-1])
    )
    lines = [
        "(set-option :produce-proofs true)",
        "(set-logic QF_LIA)",
    ]
    for left, right in arcs:
        lines.append(f"(declare-fun a_{left}_{right} () Bool)")
    for vertex in range(vertex_count):
        lines.append(f"(declare-fun p_{vertex} () Int)")
    lines.append("(assert (= p_0 0))")
    for vertex in range(1, vertex_count):
        lines.append(
            f"(assert (and (<= 1 p_{vertex}) "
            f"(<= p_{vertex} {vertex_count - 1})))"
        )
    lines.append(
        "(assert (distinct "
        + " ".join(f"p_{vertex}" for vertex in range(vertex_count))
        + "))"
    )
    for vertex in range(vertex_count):
        _check_deadline(deadline)
        outgoing = [
            f"a_{left}_{right}"
            for left, right in arcs
            if left == vertex
        ]
        incoming = [
            f"a_{left}_{right}"
            for left, right in arcs
            if right == vertex
        ]
        lines.append(f"(assert {_smt_exactly_one(outgoing)})")
        lines.append(f"(assert {_smt_exactly_one(incoming)})")
    for left, right in arcs:
        if right:
            lines.append(
                f"(assert (=> a_{left}_{right} "
                f"(= p_{right} (+ p_{left} 1))))"
            )
    for left, right in matching:
        lines.append(
            f"(assert (or a_{left}_{right} a_{right}_{left}))"
        )
    lines.extend(("(check-sat)", "(get-proof)"))
    return "\n".join(lines) + "\n"


def _hamiltonian_flow_smt(
    dimension: int,
    matching: Sequence[tuple[int, int]],
    deadline: float | None,
) -> str:
    vertex_count = 1 << dimension
    edges = _hypercube_edges(dimension)
    lines = [
        "(set-option :produce-proofs true)",
        "(set-logic QF_LIA)",
    ]
    for left, right in edges:
        lines.append(f"(declare-fun e_{left}_{right} () Bool)")
        lines.append(f"(declare-fun f_{left}_{right} () Int)")
        lines.append(f"(declare-fun f_{right}_{left} () Int)")
        for source, target in ((left, right), (right, left)):
            lines.append(
                f"(assert (and (<= 0 f_{source}_{target}) "
                f"(<= f_{source}_{target} "
                f"(ite e_{left}_{right} {vertex_count - 1} 0))))"
            )
    for vertex in range(vertex_count):
        _check_deadline(deadline)
        incident = [
            f"e_{min(vertex, other)}_{max(vertex, other)}"
            for other in (vertex ^ (1 << bit) for bit in range(dimension))
        ]
        lines.append(
            "(assert (= (+ "
            + " ".join(f"(ite {name} 1 0)" for name in incident)
            + ") 2))"
        )
        outgoing = [
            f"f_{vertex}_{vertex ^ (1 << bit)}"
            for bit in range(dimension)
        ]
        incoming = [
            f"f_{vertex ^ (1 << bit)}_{vertex}"
            for bit in range(dimension)
        ]
        balance = vertex_count - 1 if vertex == 0 else -1
        lines.append(
            "(assert (= (- (+ "
            + " ".join(outgoing)
            + ") (+ "
            + " ".join(incoming)
            + f")) {balance}))"
        )
    for left, right in matching:
        lines.append(f"(assert e_{left}_{right})")
    lines.extend(("(check-sat)", "(get-proof)"))
    return "\n".join(lines) + "\n"


def _remaining_timeout(deadline: float | None) -> float | None:
    if deadline is None:
        return None
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise _DeadlineExceeded
    return remaining


def _run_z3_proof(
    encoding: str,
    script: str,
    deadline: float | None,
) -> dict[str, Any]:
    executable = shutil.which("z3")
    if executable is None:
        return {
            "encoding": encoding,
            "status": "unavailable",
            "encoding_sha256": hashlib.sha256(script.encode()).hexdigest(),
            "proof_sha256": None,
            "solver": None,
        }
    try:
        version = subprocess.run(
            [executable, "-version"],
            capture_output=True,
            text=True,
            timeout=_remaining_timeout(deadline),
            check=False,
        ).stdout.strip()
        completed = subprocess.run(
            [executable, "-in", "-smt2"],
            input=script,
            capture_output=True,
            text=True,
            timeout=_remaining_timeout(deadline),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise _DeadlineExceeded from exc
    output = completed.stdout.strip()
    status = next(
        (
            line.strip()
            for line in output.splitlines()
            if line.strip() in {"sat", "unsat", "unknown"}
        ),
        "error",
    )
    proof_text = output.split(status, 1)[1] if status in output else ""
    return {
        "encoding": encoding,
        "status": status,
        "encoding_sha256": hashlib.sha256(script.encode()).hexdigest(),
        "proof_sha256": (
            hashlib.sha256(proof_text.encode()).hexdigest()
            if status == "unsat" and proof_text.strip()
            else None
        ),
        "solver": version,
    }


def _search_hypercube_matching(
    case: Mapping[str, Any],
    deadline: float | None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    dimension = int(case["dimension"])
    matching = _validated_hypercube_matching(
        dimension, case.get("matching")
    )
    if matching is None:
        return None
    directions = {
        (left ^ right).bit_length() - 1 for left, right in matching
    }
    perfect_matching_extendable = _matching_extends_to_perfect(
        dimension,
        matching,
    )
    matching_sha256 = hashlib.sha256(
        json.dumps(
            [list(edge) for edge in matching],
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    known_family_reasons = []
    if len(matching) == 1 << (dimension - 1):
        known_family_reasons.append("perfect_matching")
    if len(directions) <= 5:
        known_family_reasons.append("at_most_five_directions")
    if len(matching) <= 2 * dimension - 1:
        known_family_reasons.append("size_at_most_2d_minus_1")
    if perfect_matching_extendable:
        known_family_reasons.append("extendable_to_perfect_matching")
    frontier_exceeded = (
        dimension == 6
        and len(directions) == 6
        and len(matching) >= 16
        and not known_family_reasons
    )
    if metrics is not None:
        metrics.update(
            {
                "direction_count": len(directions),
                "matching_size": len(matching),
                "matching_sha256": matching_sha256,
                "frontier_exceeded": frontier_exceeded,
                "perfect_matching_extendable": perfect_matching_extendable,
                "known_family_reasons": known_family_reasons,
                "search_role": str(
                    case.get(
                        "search_role",
                        (
                            "frontier_q6_all_directions"
                            if frontier_exceeded
                            else "replication_d_le_5"
                        ),
                    )
                ),
            }
        )
    if (
        str(case.get("search_role", "")).startswith("frontier_q6")
        and not frontier_exceeded
    ):
        raise RuntimeError(
            "deep Q6 matching failed the strict uncovered-frontier guard: "
            + ", ".join(known_family_reasons or ["shape_guard"])
        )
    encoders = (
        ("directed_successor_order", _hamiltonian_successor_smt),
        ("undirected_degree_flow", _hamiltonian_flow_smt),
    )
    results = []
    for name, encoder in encoders:
        _check_deadline(deadline)
        script = encoder(dimension, matching, deadline)
        if metrics is not None:
            metrics["solver_active_encoding"] = name
        try:
            result = _run_z3_proof(name, script, deadline)
        except _DeadlineExceeded:
            if metrics is not None:
                metrics["solver_timeout_encoding"] = name
            raise
        results.append(result)
        if metrics is not None:
            metrics.setdefault("solver_results", []).append(
                {
                    "encoding": name,
                    "status": str(result["status"]),
                }
            )
        if result["status"] != "unsat":
            return None
    return {
        "dimension": dimension,
        "matching": [list(edge) for edge in matching],
        "solver_results": results,
        "trusted_result": (
            "two independent complete SMT encodings returned UNSAT"
        ),
    }


def _partition_matroid(ground_size: int, code: int) -> dict[str, Any]:
    code %= 8
    if code <= 3:
        return {
            "blocks": [list(range(ground_size))],
            "capacities": [min(code, ground_size)],
        }
    if code == 4:
        blocks = [
            [element for element in range(ground_size) if element % 2 == parity]
            for parity in (0, 1)
        ]
        return {"blocks": [block for block in blocks if block], "capacities": [1] * sum(bool(block) for block in blocks)}
    if code == 5:
        blocks = [
            list(range(start, min(start + 2, ground_size)))
            for start in range(0, ground_size, 2)
        ]
        return {"blocks": blocks, "capacities": [1] * len(blocks)}
    if code == 6:
        split = max(1, ground_size // 2)
        blocks = [list(range(split)), list(range(split, ground_size))]
        blocks = [block for block in blocks if block]
        return {"blocks": blocks, "capacities": [1] * len(blocks)}
    return {
        "blocks": [[element] for element in range(ground_size)],
        "capacities": [1] * ground_size,
    }


def _partition_matroid_rank(
    matroid: Mapping[str, Any], selected: Iterable[int]
) -> int:
    selected_set = set(selected)
    return sum(
        min(int(capacity), len(selected_set & set(block)))
        for block, capacity in zip(matroid["blocks"], matroid["capacities"])
    )


def _valid_partition_matroid(
    matroid: Any, ground_size: int
) -> bool:
    if not isinstance(matroid, Mapping):
        return False
    blocks = matroid.get("blocks")
    capacities = matroid.get("capacities")
    if (
        not isinstance(blocks, Sequence)
        or isinstance(blocks, (str, bytes))
        or not isinstance(capacities, Sequence)
        or isinstance(capacities, (str, bytes))
        or len(blocks) != len(capacities)
        or not blocks
    ):
        return False
    seen: set[int] = set()
    for block, capacity in zip(blocks, capacities):
        if (
            not isinstance(block, Sequence)
            or isinstance(block, (str, bytes))
            or not block
            or isinstance(capacity, bool)
            or not isinstance(capacity, int)
        ):
            return False
        elements = []
        for element in block:
            if (
                isinstance(element, bool)
                or not isinstance(element, int)
                or not 0 <= element < ground_size
            ):
                return False
            elements.append(element)
        if (
            len(set(elements)) != len(elements)
            or seen.intersection(elements)
            or not 0 <= capacity <= len(elements)
        ):
            return False
        seen.update(elements)
    return seen == set(range(ground_size))


def _evaluate_aharoni_berger(
    case: Mapping[str, Any],
    deadline: float | None,
) -> dict[str, Any] | None:
    ground_size = int(case["ground_size"])
    k = int(case["k"])
    ell = int(case["ell"])
    matroids = [
        _partition_matroid(ground_size, int(code))
        for code in case["matroid_codes"]
    ]
    partition_rank_sums = []
    premise = True
    for assignment in itertools.product(range(k), repeat=ground_size):
        _check_deadline(deadline)
        parts = [
            [element for element, owner in enumerate(assignment) if owner == index]
            for index in range(k)
        ]
        rank_sum = sum(
            _partition_matroid_rank(matroid, part)
            for matroid, part in zip(matroids, parts)
        )
        partition_rank_sums.append(
            {"assignment": list(assignment), "rank_sum": rank_sum}
        )
        if rank_sum < ell * (k - 1):
            premise = False
            break
    if not premise:
        return None
    common_independent = []
    for subset in itertools.combinations(range(ground_size), ell):
        _check_deadline(deadline)
        if all(
            _partition_matroid_rank(matroid, subset) == ell
            for matroid in matroids
        ):
            common_independent.append(subset)
    if not common_independent:
        return {
            "ground_size": ground_size,
            "k": k,
            "ell": ell,
            "matroids": matroids,
            "partition_rank_sums": partition_rank_sums,
            "common_independent_sets": [],
        }
    return None


def _compose_permutations(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def _permutation_group(
    family: str, parameter: int
) -> tuple[tuple[int, ...], ...]:
    if family == "cyclic":
        return _cyclic_group(parameter)
    if family == "symmetric":
        return tuple(itertools.permutations(range(parameter)))
    if family == "alternating":
        return tuple(
            permutation
            for permutation in itertools.permutations(range(parameter))
            if _permutation_sign(permutation) == 1
        )
    if family == "dihedral":
        rotations = _cyclic_group(parameter)
        reflections = tuple(
            tuple((shift - point) % parameter for point in range(parameter))
            for shift in range(parameter)
        )
        return tuple(dict.fromkeys((*rotations, *reflections)))
    raise ValueError(f"unsupported permutation group family {family!r}")


def _all_subgroups(
    group: Sequence[tuple[int, ...]], deadline: float | None
) -> tuple[frozenset[int], ...]:
    lookup = {element: index for index, element in enumerate(group)}
    identity = lookup[tuple(range(len(group[0])))]
    multiplication = [
        [
            lookup[_compose_permutations(group[left], group[right])]
            for right in range(len(group))
        ]
        for left in range(len(group))
    ]
    subgroups = []
    for mask in range(1 << len(group)):
        _check_deadline(deadline)
        if not mask & (1 << identity):
            continue
        members = [index for index in range(len(group)) if mask & (1 << index)]
        if all(
            mask & (1 << multiplication[left][right])
            for left in members
            for right in members
        ):
            subgroups.append(frozenset(members))
    return tuple(subgroups)


def _group_multiplication_table(
    group: Sequence[tuple[int, ...]],
) -> tuple[list[list[int]], int, list[int]]:
    lookup = {element: index for index, element in enumerate(group)}
    identity = lookup[tuple(range(len(group[0])))]
    multiplication = [
        [
            lookup[_compose_permutations(group[left], group[right])]
            for right in range(len(group))
        ]
        for left in range(len(group))
    ]
    inverses = [
        next(
            right
            for right in range(len(group))
            if multiplication[left][right] == identity
            and multiplication[right][left] == identity
        )
        for left in range(len(group))
    ]
    return multiplication, identity, inverses


def _generated_subgroup(
    multiplication: Sequence[Sequence[int]],
    identity: int,
    generators: Iterable[int],
    deadline: float | None,
) -> frozenset[int]:
    subgroup = {identity, *map(int, generators)}
    changed = True
    while changed:
        _check_deadline(deadline)
        changed = False
        current = tuple(subgroup)
        for left in current:
            for right in current:
                product = multiplication[left][right]
                if product not in subgroup:
                    subgroup.add(product)
                    changed = True
    return frozenset(subgroup)


def _is_power_of(value: int, prime: int) -> bool:
    while value > 1 and value % prime == 0:
        value //= prime
    return value == 1


def _sylow_subgroups(
    multiplication: Sequence[Sequence[int]],
    identity: int,
    prime: int,
    target_order: int,
    deadline: float | None,
) -> tuple[frozenset[int], ...]:
    trivial = frozenset({identity})
    known = {trivial}
    frontier = [trivial]
    group_order = len(multiplication)
    while frontier:
        subgroup = frontier.pop()
        for element in range(group_order):
            _check_deadline(deadline)
            if element in subgroup:
                continue
            generated = _generated_subgroup(
                multiplication,
                identity,
                (*subgroup, element),
                deadline,
            )
            if (
                len(generated) <= target_order
                and _is_power_of(len(generated), prime)
                and generated not in known
            ):
                known.add(generated)
                frontier.append(generated)
    return tuple(
        sorted(
            (subgroup for subgroup in known if len(subgroup) == target_order),
            key=lambda subgroup: tuple(sorted(subgroup)),
        )
    )


def _evaluate_sylow_intersections(
    case: Mapping[str, Any],
    deadline: float | None,
) -> dict[str, Any] | None:
    family = str(case["family"])
    parameter = int(case["parameter"])
    group = _permutation_group(family, parameter)
    multiplication, identity, inverses = _group_multiplication_table(group)
    factorization = {
        int(prime): int(exponent)
        for prime, exponent in sympy.factorint(len(group)).items()
    }
    chosen_sylows: dict[int, frozenset[int]] = {}
    for prime, exponent in sorted(factorization.items()):
        _check_deadline(deadline)
        sylows = _sylow_subgroups(
            multiplication,
            identity,
            prime,
            prime**exponent,
            deadline,
        )
        if not sylows:
            raise RuntimeError(
                f"failed to enumerate a Sylow {prime}-subgroup"
            )
        chosen_sylows[prime] = sylows[0]
    all_intersections: dict[int, list[frozenset[int]]] = {}
    minimal_flags: dict[int, list[bool]] = {}
    for prime, subgroup in chosen_sylows.items():
        intersections = []
        for element in range(len(group)):
            _check_deadline(deadline)
            conjugate = frozenset(
                multiplication[
                    multiplication[inverses[element]][member]
                ][element]
                for member in subgroup
            )
            intersections.append(subgroup & conjugate)
        all_intersections[prime] = intersections
        minimal_flags[prime] = [
            not any(other < intersection for other in intersections)
            for intersection in intersections
        ]
    if any(
        all(minimal_flags[prime][element] for prime in chosen_sylows)
        for element in range(len(group))
    ):
        return None
    return {
        "catalogue_label": str(case["catalogue_label"]),
        "family": family,
        "parameter": parameter,
        "group": [list(permutation) for permutation in group],
        "primes": sorted(chosen_sylows),
        "sylow_subgroups": {
            str(prime): sorted(subgroup)
            for prime, subgroup in chosen_sylows.items()
        },
        "intersections": {
            str(prime): [
                sorted(intersection) for intersection in intersections
            ]
            for prime, intersections in all_intersections.items()
        },
        "inclusion_minimal": {
            str(prime): flags
            for prime, flags in minimal_flags.items()
        },
    }


def _evaluate_gap_sylow_intersections(
    case: Mapping[str, Any],
    deadline: float | None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    raw_id = case.get("smallgroup_id")
    if (
        not isinstance(raw_id, Sequence)
        or isinstance(raw_id, (str, bytes))
        or len(raw_id) != 2
    ):
        raise RuntimeError("GAP SmallGroups case is missing a valid identifier")
    order, group_index = map(int, raw_id)
    script = f"""
RunSylowSearch:=function()
local G,els,primes,sylows,allIntersections,allMinimal,H,intersections,
      flags,I,J,good,position,i;
SizeScreen([1000000,1000000]);;
G:=SmallGroup({order},{group_index});;
els:=Elements(G);;
primes:=Set(FactorsInt(Size(G)));;
sylows:=List(primes,p->SylowSubgroup(G,p));;
allIntersections:=[];;
allMinimal:=[];;
for H in sylows do
 intersections:=List(els,g->Intersection(H,H^g));;
 flags:=List(intersections,I->
  not ForAny(intersections,J->Size(J)<Size(I) and IsSubgroup(I,J)));
 Add(allIntersections,intersections);
 Add(allMinimal,flags);
od;
good:=ForAny([1..Length(els)],position->
 ForAll([1..Length(primes)],i->allMinimal[i][position]));;
Print("GOOD|",good,"\\n");;
Print("SOLVABLE|",IsSolvableGroup(G),"\\n");;
Print("PRIMES|",JoinStringsWithSeparator(List(primes,String),","),"\\n");;
for i in [1..Length(primes)] do
 Print("DATA|",primes[i],"|",Size(sylows[i]),"|",
  JoinStringsWithSeparator(List(allIntersections[i],I->String(Size(I))),","),
  "|",JoinStringsWithSeparator(List(allMinimal[i],String),","),"\\n");
od;
end;;
RunSylowSearch();;
"""
    output = _run_gap_text(script, deadline)
    good: bool | None = None
    solvable: bool | None = None
    primes: list[int] = []
    sylow_orders: dict[str, int] = {}
    intersection_orders: dict[str, list[int]] = {}
    minimal_flags: dict[str, list[bool]] = {}
    for raw in output.splitlines():
        line = raw.strip()
        if line.startswith("GOOD|"):
            good = line.split("|", 1)[1] == "true"
        elif line.startswith("SOLVABLE|"):
            solvable = line.split("|", 1)[1] == "true"
        elif line.startswith("PRIMES|"):
            values = line.split("|", 1)[1]
            primes = [int(value) for value in values.split(",") if value]
        elif line.startswith("DATA|"):
            _, prime, sylow_order, sizes, flags = line.split("|", 4)
            sylow_orders[prime] = int(sylow_order)
            intersection_orders[prime] = [
                int(value) for value in sizes.split(",") if value
            ]
            minimal_flags[prime] = [
                value == "true" for value in flags.split(",") if value
            ]
    if (
        good is None
        or solvable is None
        or not primes
        or set(sylow_orders) != {str(prime) for prime in primes}
        or any(len(values) != order for values in intersection_orders.values())
        or any(len(values) != order for values in minimal_flags.values())
    ):
        raise RuntimeError("GAP Sylow-intersection protocol was incomplete")
    if metrics is not None:
        metrics.update(
            {
                "group_order": order,
                "smallgroup_id": [order, group_index],
                "catalogue_family": str(case["catalogue_family"]),
                "catalogue_position": int(case["catalogue_position"]),
                "catalogue_size": int(case["catalogue_size"]),
                "catalogue_family_position": int(
                    case["catalogue_family_position"]
                ),
                "catalogue_family_size": int(case["catalogue_family_size"]),
                "catalogue_shard": int(case["catalogue_shard"]),
                "catalogue_shard_position": int(
                    case["catalogue_shard_position"]
                ),
                "catalogue_shard_size": int(case["catalogue_shard_size"]),
                "group_search_role": str(case["search_role"]),
                "group_solvable": solvable,
                "prime_divisor_count": len(primes),
            }
        )
    if good:
        return None
    return {
        "backend": "gap_smallgroups",
        "smallgroup_id": [order, group_index],
        "group_order": order,
        "catalogue_label": str(case["catalogue_label"]),
        "catalogue_family": str(case["catalogue_family"]),
        "primes": primes,
        "sylow_orders": sylow_orders,
        "intersection_orders": intersection_orders,
        "inclusion_minimal": minimal_flags,
        "simultaneous_element_exists": False,
        "gap_replay": "exact_all_group_elements_and_conjugate_intersections",
    }


def _catalogue_subgroup(
    group: Sequence[tuple[int, ...]],
    kind: str,
) -> frozenset[int]:
    degree = len(group[0])
    if kind == "point_stabilizer":
        return frozenset(
            index
            for index, permutation in enumerate(group)
            if permutation[-1] == len(permutation) - 1
        )
    if kind == "two_point_stabilizer":
        return frozenset(
            index
            for index, permutation in enumerate(group)
            if permutation[-1] == degree - 1
            and permutation[-2] == degree - 2
        )
    if kind == "two_set_stabilizer":
        stabilized = {degree - 2, degree - 1}
        return frozenset(
            index
            for index, permutation in enumerate(group)
            if {permutation[degree - 2], permutation[degree - 1]}
            == stabilized
        )
    if kind == "transposition":
        generators = [(1, 0, *range(2, degree))]
    elif kind == "three_cycle":
        generators = [(1, 2, 0, *range(3, degree))]
    elif kind == "four_cycle":
        generators = [(1, 2, 3, 0, *range(4, degree))]
    elif kind == "five_cycle":
        generators = [(1, 2, 3, 4, 0, *range(5, degree))]
    elif kind == "double_transposition":
        generators = [(1, 0, 3, 2, *range(4, degree))]
    elif kind == "klein_four":
        generators = [
            (1, 0, 3, 2, *range(4, degree)),
            (2, 3, 0, 1, *range(4, degree)),
        ]
    elif kind == "reflection":
        generators = [tuple((-point) % degree for point in range(degree))]
    elif kind == "rotation":
        generators = [tuple((point + 1) % degree for point in range(degree))]
    elif kind == "rotation_square":
        generators = [tuple((point + 2) % degree for point in range(degree))]
    elif kind == "rotation_third":
        generators = [tuple((point + 3) % degree for point in range(degree))]
    elif kind == "reflection_rotation_square":
        generators = [
            tuple((-point) % degree for point in range(degree)),
            tuple((point + 2) % degree for point in range(degree)),
        ]
    else:
        raise ValueError(f"unsupported catalogue subgroup {kind!r}")
    multiplication, identity, _ = _group_multiplication_table(group)
    lookup = {element: index for index, element in enumerate(group)}
    if any(tuple(generator) not in lookup for generator in generators):
        raise RuntimeError(
            f"subgroup generator for {kind!r} is not in the source group"
        )
    return _generated_subgroup(
        multiplication,
        identity,
        (lookup[tuple(generator)] for generator in generators),
        None,
    )


def _coset_action(
    group: Sequence[tuple[int, ...]],
    subgroup: frozenset[int],
    deadline: float | None,
) -> tuple[tuple[tuple[int, ...], ...], tuple[frozenset[int], ...]]:
    multiplication, _, _ = _group_multiplication_table(group)
    unseen = set(range(len(group)))
    cosets = []
    while unseen:
        representative = min(unseen)
        coset = frozenset(
            multiplication[representative][member]
            for member in subgroup
        )
        cosets.append(coset)
        unseen -= coset
    owner = {
        element: coset_index
        for coset_index, coset in enumerate(cosets)
        for element in coset
    }
    representatives = [min(coset) for coset in cosets]
    action = []
    for element in range(len(group)):
        _check_deadline(deadline)
        permutation = tuple(
            owner[multiplication[element][representative]]
            for representative in representatives
        )
        action.append(permutation)
    return tuple(dict.fromkeys(action)), tuple(cosets)


@lru_cache(maxsize=1)
def _kou_21_99_deep_action_catalogue() -> tuple[
    tuple[str, int, str, str, str, int, int, int], ...
]:
    catalogue = []
    seen_hashes: set[str] = set()
    for family, parameter, subgroup_kind, label in (
        _KOU_21_99_ACTION_CANDIDATES
    ):
        source_group = _permutation_group(family, parameter)
        subgroup = _catalogue_subgroup(source_group, subgroup_kind)
        action, cosets = _coset_action(source_group, subgroup, None)
        action_payload = json.dumps(
            [list(permutation) for permutation in action],
            separators=(",", ":"),
        )
        action_hash = hashlib.sha256(action_payload.encode()).hexdigest()
        faithful = len(action) == len(source_group)
        nonregular = len(action) > len(cosets)
        if not faithful or not nonregular or action_hash in seen_hashes:
            continue
        seen_hashes.add(action_hash)
        catalogue.append(
            (
                family,
                parameter,
                subgroup_kind,
                label,
                action_hash,
                len(source_group),
                len(subgroup),
                len(cosets),
            )
        )
    if len(catalogue) < 12:
        raise RuntimeError(
            "KOU-21.99 faithful nonregular action catalogue is too small"
        )
    return tuple(catalogue)


@lru_cache(maxsize=1)
def _kou_21_99_action_shards() -> tuple[
    tuple[
        tuple[str, int, str, str, str, int, int, int],
        ...,
    ],
    ...,
]:
    catalogue = _kou_21_99_deep_action_catalogue()
    return tuple(
        tuple(
            entry
            for position, entry in enumerate(catalogue)
            if position % 3 == shard
        )
        for shard in range(3)
    )


def _kou_21_99_deep_case(index: int) -> dict[str, Any]:
    relative_index = int(index) - _KOU_21_99_DEEP_OFFSET
    shard = relative_index % 3
    shard_position = relative_index // 3
    shard_entries = _kou_21_99_action_shards()[shard]
    if not 0 <= shard_position < len(shard_entries):
        raise _FiniteCatalogueExhausted
    (
        family,
        parameter,
        subgroup_kind,
        label,
        action_hash,
        source_order,
        subgroup_order,
        degree,
    ) = shard_entries[shard_position]
    catalogue = _kou_21_99_deep_action_catalogue()
    catalogue_position = catalogue.index(shard_entries[shard_position])
    return {
        "family": family,
        "parameter": parameter,
        "subgroup_kind": subgroup_kind,
        "catalogue_label": label,
        "action_sha256": action_hash,
        "source_group_order": source_order,
        "subgroup_order": subgroup_order,
        "action_degree": degree,
        "catalogue_position": catalogue_position,
        "catalogue_size": len(catalogue),
        "catalogue_shard": shard,
        "catalogue_shard_position": shard_position,
        "catalogue_shard_size": len(shard_entries),
        "search_role": "faithful_nonregular_coset_action",
    }


@lru_cache(maxsize=1)
def _opg_48264_deep_catalogue() -> tuple[
    tuple[tuple[int, int], ...], ...
]:
    from amra.discovery.second_batch_graphs import (
        NAUTY_BIN,
        _decode_graph6,
        _nauty_env,
    )

    if not NAUTY_BIN.is_file():
        raise RuntimeError(f"nauty geng is unavailable at {NAUTY_BIN}")
    try:
        completed = subprocess.run(
            [
                str(NAUTY_BIN),
                "-q",
                "-c",
                "-d3",
                "-D3",
                "18",
            ],
            capture_output=True,
            text=True,
            env=_nauty_env(),
            timeout=60.0,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "timed out constructing the OPG-48264 deep catalogue"
        ) from exc
    catalogue = tuple(
        tuple(_decode_graph6(raw).edges)
        for raw in completed.stdout.splitlines()
        if raw.strip()
    )
    if len(catalogue) != 41_301 or len(set(catalogue)) != len(catalogue):
        raise RuntimeError(
            "nauty returned an incomplete or duplicate cubic graph catalogue"
        )
    return catalogue


def _group_edges(family: str, level: int) -> tuple[int, tuple[tuple[int, int], ...]]:
    if family == "nauty_cubic_18":
        catalogue = _opg_48264_deep_catalogue()
        if not 0 <= level < len(catalogue):
            raise ValueError(f"invalid nauty cubic catalogue index {level}")
        return 18, catalogue[level]
    if family == "prism":
        half = 3 + level % 6
        edges = {
            tuple(sorted((layer * half + vertex, layer * half + (vertex + 1) % half)))
            for layer in range(2)
            for vertex in range(half)
        }
        edges.update((vertex, half + vertex) for vertex in range(half))
        return 2 * half, tuple(sorted(edges))
    if family == "mobius_ladder":
        order = 8 + 2 * (level % 5)
        edges = {
            tuple(sorted((vertex, (vertex + 1) % order)))
            for vertex in range(order)
        }
        edges.update(
            tuple(sorted((vertex, vertex + order // 2)))
            for vertex in range(order // 2)
        )
        return order, tuple(sorted(edges))
    if family == "petersen":
        return 10, tuple(
            [(index, (index + 1) % 5) for index in range(5)]
            + [(5 + index, 5 + (index + 2) % 5) for index in range(5)]
            + [(index, 5 + index) for index in range(5)]
        )
    if family == "circulant4":
        order = 7 + level % 6
        edges = {
            tuple(sorted((vertex, (vertex + step) % order)))
            for vertex in range(order)
            for step in (1, 2)
        }
        return order, tuple(sorted(edges))
    if family == "bipartite_quartic":
        side = 8 if level >= 100 else 4 + level % 3
        return 2 * side, tuple(
            sorted(
                {
                    (left, side + (left + shift) % side)
                    for left in range(side)
                    for shift in range(4)
                }
            )
        )
    if family == "quartic_circulant":
        order = 9 + 2 * (level % 4)
        edges = {
            tuple(sorted((vertex, (vertex + step) % order)))
            for vertex in range(order)
            for step in (1, 3)
        }
        return order, tuple(sorted(edges))
    raise ValueError(f"unsupported graph family {family!r}")


def _spanning_tree_edge_indices(
    order: int, edges: Sequence[tuple[int, int]]
) -> tuple[int, ...]:
    parent = list(range(order))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    tree = []
    for edge_index, (left, right) in enumerate(edges):
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
            tree.append(edge_index)
    if len(tree) != order - 1:
        raise RuntimeError("signing search requires a connected graph")
    return tuple(tree)


def _signed_adjacency_matrix(
    order: int,
    edges: Sequence[tuple[int, int]],
    tree_edges: Sequence[int],
    signing_bits: int,
) -> list[list[int]]:
    tree = set(map(int, tree_edges))
    free = [index for index in range(len(edges)) if index not in tree]
    free_position = {edge_index: bit for bit, edge_index in enumerate(free)}
    matrix = [[0] * order for _ in range(order)]
    for edge_index, (left, right) in enumerate(edges):
        position = free_position.get(edge_index)
        sign = -1 if position is not None and signing_bits & (1 << position) else 1
        matrix[left][right] = matrix[right][left] = sign
    return matrix


def _signing_threshold_matrix(
    adjacency: Sequence[Sequence[int]],
    threshold_squared: int,
) -> list[list[int]]:
    order = len(adjacency)
    squared = [
        [
            sum(
                int(adjacency[row][middle]) * int(adjacency[middle][column])
                for middle in range(order)
            )
            for column in range(order)
        ]
        for row in range(order)
    ]
    return [
        [
            (threshold_squared if row == column else 0) - squared[row][column]
            for column in range(order)
        ]
        for row in range(order)
    ]


def _integer_quadratic_value(
    matrix: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> int:
    return sum(
        int(vector[row]) * int(matrix[row][column]) * int(vector[column])
        for row in range(len(vector))
        for column in range(len(vector))
    )


def _negative_quadratic_witness(
    matrix: Sequence[Sequence[int | Fraction]],
) -> tuple[int, ...] | None:
    """Return an exact integer negative direction, or None iff the matrix is PSD."""

    rational = [
        [Fraction(value) for value in row]
        for row in matrix
    ]

    def recurse(current: list[list[Fraction]]) -> list[Fraction] | None:
        size = len(current)
        if size == 0:
            return None
        for index in range(size):
            if current[index][index] < 0:
                vector = [Fraction(0)] * size
                vector[index] = Fraction(1)
                return vector
        positive = next(
            (
                index
                for index in range(size)
                if current[index][index] > 0
            ),
            None,
        )
        if positive is None:
            for left in range(size):
                for right in range(left + 1, size):
                    value = current[left][right]
                    if value:
                        vector = [Fraction(0)] * size
                        vector[left] = Fraction(1)
                        vector[right] = Fraction(-1 if value > 0 else 1)
                        return vector
            return None

        remaining = [index for index in range(size) if index != positive]
        pivot = current[positive][positive]
        column = [current[index][positive] for index in remaining]
        schur = [
            [
                current[left][right]
                - column[left_position] * column[right_position] / pivot
                for right_position, right in enumerate(remaining)
            ]
            for left_position, left in enumerate(remaining)
        ]
        tail = recurse(schur)
        if tail is None:
            return None
        vector = [Fraction(0)] * size
        for index, value in zip(remaining, tail):
            vector[index] = value
        vector[positive] = -sum(
            coefficient * value
            for coefficient, value in zip(column, tail)
        ) / pivot
        return vector

    rational_vector = recurse(rational)
    if rational_vector is None:
        return None
    denominator = math.lcm(
        *(value.denominator for value in rational_vector)
    )
    integer_vector = tuple(
        int(value * denominator) for value in rational_vector
    )
    if not any(integer_vector):
        raise RuntimeError("exact signing witness unexpectedly vanished")
    quadratic_value = sum(
        Fraction(integer_vector[row])
        * rational[row][column]
        * Fraction(integer_vector[column])
        for row in range(len(integer_vector))
        for column in range(len(integer_vector))
    )
    if quadratic_value >= 0:
        raise RuntimeError("exact signing witness failed its quadratic inequality")
    return integer_vector


def _evaluate_graph_signing(
    case: Mapping[str, Any],
    deadline: float | None,
    metrics: dict[str, Any] | None,
) -> dict[str, Any] | None:
    family = str(case["family"])
    order, edges = _group_edges(family, int(case.get("level", 0)))
    degrees = [
        sum(vertex in edge for edge in edges)
        for vertex in range(order)
    ]
    if not degrees or len(set(degrees)) != 1 or degrees[0] not in {3, 4}:
        raise RuntimeError(f"{family} did not generate a cubic/quartic graph")
    degree = degrees[0]
    tree_edges = _spanning_tree_edge_indices(order, edges)
    free_count = len(edges) - len(tree_edges)
    threshold_squared = 4 * (degree - 1)
    graph_sha256 = hashlib.sha256(
        json.dumps(
            [list(edge) for edge in edges],
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    signing_witnesses = []
    for signing_bits in range(1 << free_count):
        _check_deadline(deadline)
        adjacency = _signed_adjacency_matrix(
            order,
            edges,
            tree_edges,
            signing_bits,
        )
        threshold_matrix = _signing_threshold_matrix(
            adjacency,
            threshold_squared,
        )
        vector = _negative_quadratic_witness(threshold_matrix)
        if metrics is not None:
            metrics.update(
                {
                    "normalized_signings_checked": signing_bits + 1,
                    "cycle_rank": free_count,
                    "graph_order": order,
                    "graph_degree": degree,
                    "signing_graph_family": family,
                    "signing_graph_sha256": graph_sha256,
                    "signing_certificate_method": (
                        "exact_rational_schur_negative_direction"
                    ),
                    "signing_catalogue_position": case.get(
                        "catalogue_position"
                    ),
                    "signing_catalogue_size": case.get("catalogue_size"),
                    "signing_catalogue_shard": case.get("catalogue_shard"),
                    "signing_catalogue_shard_position": case.get(
                        "catalogue_shard_position"
                    ),
                    "signing_catalogue_shard_size": case.get(
                        "catalogue_shard_size"
                    ),
                    "signing_search_role": case.get("search_role"),
                }
            )
        if vector is None:
            return None
        quadratic_value = _integer_quadratic_value(
            threshold_matrix,
            vector,
        )
        signing_witnesses.append(
            {
                "signing_bits": signing_bits,
                "vector": list(vector),
                "quadratic_value": quadratic_value,
            }
        )
    return {
        "order": order,
        "family": family,
        "degree": degree,
        "edges": [list(edge) for edge in edges],
        "spanning_tree_edge_indices": list(tree_edges),
        "cycle_rank": free_count,
        "threshold_squared": threshold_squared,
        "signing_witnesses": signing_witnesses,
        "catalogue_position": case.get("catalogue_position"),
        "catalogue_size": case.get("catalogue_size"),
        "catalogue_shard": case.get("catalogue_shard"),
        "catalogue_shard_position": case.get("catalogue_shard_position"),
        "catalogue_shard_size": case.get("catalogue_shard_size"),
        "search_role": case.get("search_role"),
        "certificate_method": (
            "integer vectors with v^T(threshold_squared*I-A^2)v<0"
        ),
    }


def _evaluate(
    problem_id: str,
    case: Mapping[str, Any],
    *,
    deadline: float | None = None,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if problem_id == "unsolvedmath-comb-003":
        return _search_ramsey_55(
            int(case["attempt"]),
            int(case.get("max_flips", 25_000)),
            deadline,
            metrics,
            str(case.get("search_basin", "known_k42_extension")),
        )
    if problem_id == "unsolvedmath-nt-010":
        n = int(case["n"])
        value = math.factorial(n) + 1
        if n not in {4, 5, 7} and _is_square(value):
            return {"n": n, "m": math.isqrt(value), "factorial_plus_one": value}
        return None
    if problem_id == "unsolvedmath-nt-026":
        n = int(case["n"])
        divisor_sum = _proper_divisor_sum(n)
        return {"n": n, "proper_divisor_sum": divisor_sum} if divisor_sum == n else None
    if problem_id == "unsolvedmath-nt-027":
        n = int(case["n"])
        left, right = _prime(n), _prime(n + 1)
        lhs, rhs = left ** (n + 1), right**n
        if lhs <= rhs:
            return {"n": n, "p_n": left, "p_next": right, "lhs": lhs, "rhs": rhs}
        return None
    if problem_id == "unsolvedmath-nt-033":
        start = int(case["start"])
        _check_deadline(deadline)
        if sympy.isprime(start):
            return None
        run = []
        value = start
        while not sympy.isprime(value):
            _check_deadline(deadline)
            run.append(value)
            value += 1
        divisors = []
        for item in run:
            _check_deadline(deadline)
            divisors.append(set(map(int, sympy.factorint(item))))
        _check_deadline(deadline)
        if run and not _maximum_matching_exists(divisors, deadline):
            return {
                "run": run,
                "prime_divisors": [sorted(values) for values in divisors],
            }
        return None
    if problem_id == "unsolvedmath-nt-039":
        n = int(case["n"])
        lhs = _addition_chain_length(2**n - 1, deadline)
        short_length = _addition_chain_length(n, deadline)
        if lhs is None or short_length is None:
            return None
        rhs = n - 1 + short_length
        if lhs > rhs:
            return {"n": n, "left_chain_length": lhs, "right_bound": rhs}
        return None
    if problem_id == "unsolvedmath-nt-043":
        n = int(case["n"])
        sigma = int(sympy.divisor_sigma(n))
        return {"n": n, "sigma": sigma} if sigma == 2 * n + 1 else None
    if problem_id == "unsolvedmath-nt-044":
        n = int(case["n"])
        if n & (n - 1) and _proper_divisor_sum(n) == n - 1:
            return {"n": n, "proper_divisor_sum": n - 1}
        return None
    if problem_id == "unsolvedmath-nt-046":
        a, b = int(case["a"]), int(case["b"])
        if a < b and (a - b) % 2 and _proper_divisor_sum(a) == b and _proper_divisor_sum(b) == a:
            return {"a": a, "b": b, "sum_a": b, "sum_b": a}
        return None
    if problem_id == "unsolvedmath-nt-050":
        n = int(case["n"])
        divisors = [int(value) for value in sympy.divisors(n) if value < n]
        total = sum(divisors)
        if total > n and not _has_subset_sum(divisors, n):
            return {"n": n, "proper_divisors": divisors, "proper_divisor_sum": total}
        return None
    if problem_id == "unsolvedmath-nt-053":
        n = int(case["n"])
        if n != 10 and Fraction(int(sympy.divisor_sigma(n)), n) == Fraction(9, 5):
            return {"n": n, "sigma": int(sympy.divisor_sigma(n)), "ratio": "9/5"}
        return None
    if problem_id == "unsolvedmath-nt-078":
        a, b, c = (int(case[key]) for key in ("A", "B", "C"))
        x, y, z = (int(case[key]) for key in ("x", "y", "z"))
        if math.gcd(math.gcd(a, b), c) == 1 and a**x + b**y == c**z:
            return dict(case)
        return None
    if problem_id == "unsolvedmath-nt-086":
        n = int(case["n"])
        left, right = _prime(n), _prime(n + 1)
        primes = list(map(int, sympy.primerange(left * left + 1, right * right)))
        if len(primes) < 4:
            return {"n": n, "left": left, "right": right, "between": primes}
        return None
    if problem_id == "unsolvedmath-guy-a12b":
        n = int(case["n"])
        if n > 1 and not sympy.isprime(n) and n % 10 in {3, 7}:
            residue_two = (pow(2, n, n) - 2) % n
            residue_fib = _fibonacci(n + 1) % n
            if residue_two == residue_fib == 0:
                return {"n": n, "two_residue": 0, "fibonacci_residue": 0}
        return None
    if problem_id == "unsolvedmath-guy-a19a":
        n = int(case["n"])
        known = {4, 7, 15, 21, 45, 75, 105}
        values = [n - 2**power for power in range(1, n.bit_length()) if 2**power < n]
        if n not in known and values and all(sympy.isprime(value) for value in values):
            return {"n": n, "differences": values}
        return None
    if problem_id == "unsolvedmath-guy-a7b":
        first = _prime(int(case["n"]))
        chain = [first]
        for _ in range(6):
            next_value = 4 * chain[-1] ** 2 - 17
            if next_value <= 1 or not sympy.isprime(next_value):
                return None
            chain.append(next_value)
        if len(chain) == 7:
            return {"chain": chain}
        return None
    if problem_id == "unsolvedmath-opg-148":
        p, matrix = int(case["p"]), case["matrix"]
        n = len(matrix)
        if p < 5 or not sympy.isprime(p) or _matrix_det_mod(matrix, p) == 0:
            return None
        for vector in itertools.product(range(1, p), repeat=n):
            image = [
                sum(int(matrix[row][column]) * vector[column] for column in range(n)) % p
                for row in range(n)
            ]
            if all(image):
                return None
        return {"p": p, "matrix": matrix, "determinant_mod_p": _matrix_det_mod(matrix, p)}
    if problem_id == "unsolvedmath-opg-151":
        p, matrix = int(case["p"]), case["matrix"]
        n = len(matrix)
        if not sympy.isprime(p) or _matrix_det_mod(matrix, p) == 0:
            return None
        doubled = [list(row) + list(row) for row in matrix]
        permanents = []
        for columns in itertools.combinations(range(2 * n), n):
            submatrix = [[row[column] for column in columns] for row in doubled]
            permanents.append(_permanent_mod(submatrix, p))
        if permanents and not any(permanents):
            return {"p": p, "matrix": matrix, "permanents_mod_p": permanents}
        return None
    if problem_id == "unsolvedmath-opg-16570":
        a, b, c = (int(case[key]) for key in ("a", "b", "c"))
        grid = [
            [a + b, a - b - c, a + c],
            [a - b + c, a, a + b - c],
            [a - c, a + b + c, a - b],
        ]
        entries = [value for row in grid for value in row]
        if min(entries) > 0 and len(set(entries)) == 9 and all(_is_square(value) for value in entries):
            return {"parameters": [a, b, c], "grid": grid, "magic_sum": 3 * a}
        return None
    if problem_id == "unsolvedmath-opg-37221":
        a, b, c = map(int, case["edges"])
        squares = [a * a + b * b, a * a + c * c, b * b + c * c, a * a + b * b + c * c]
        if all(_is_square(value) for value in squares):
            return {"edges": [a, b, c], "diagonals": [math.isqrt(value) for value in squares]}
        return None
    if problem_id == "unsolvedmath-opg-369":
        return _evaluate_many_weights(case, deadline)
    if problem_id.startswith("unsolvedmath-comb-001"):
        n, mask = int(case["size"]), int(case["relation_mask"])
        pairs = list(itertools.combinations(range(n), 2))
        relation = {pair for bit, pair in enumerate(pairs) if mask & (1 << bit)}
        if any(
            (left, right) in relation
            and (right, upper) in relation
            and (left, upper) not in relation
            for left in range(n)
            for right in range(n)
            for upper in range(n)
        ):
            return None
        extensions = [
            permutation
            for permutation in itertools.permutations(range(n))
            if all(permutation.index(left) < permutation.index(right) for left, right in relation)
        ]
        if len(extensions) <= 1:
            return None
        good = False
        for left, right in pairs:
            if (left, right) in relation:
                continue
            probability = Fraction(
                sum(order.index(left) < order.index(right) for order in extensions),
                len(extensions),
            )
            if Fraction(1, 3) <= probability <= Fraction(2, 3):
                good = True
                break
        if not good:
            return {"size": n, "relation": sorted(relation), "linear_extensions": extensions}
        return None
    if problem_id == "unsolvedmath-alg-007":
        coefficients = tuple(map(int, case["coefficients"]))
        x = sympy.symbols("x")
        polynomial = sympy.Poly.from_list(coefficients, gens=x, domain=sympy.QQ)
        if polynomial.degree() < 2:
            return None
        gcds = [
            sympy.gcd(polynomial, polynomial.diff((x, order)))
            for order in range(1, polynomial.degree())
        ]
        premise = all(gcd.degree() >= 1 for gcd in gcds)
        squarefree = polynomial.sqf_part()
        if premise and squarefree.degree() > 1:
            return {
                "coefficients": list(coefficients),
                "gcds": [str(gcd.as_expr()) for gcd in gcds],
                "squarefree_degree": squarefree.degree(),
            }
        return None
    if problem_id == "unsolvedmath-kou-21.26":
        if case.get("backend") == "gap_smallgroups":
            return _evaluate_gap_sylow_intersections(case, deadline, metrics)
        if metrics is not None:
            group = _permutation_group(
                str(case["family"]), int(case["parameter"])
            )
            metrics.update(
                {
                    "group_order": len(group),
                    "smallgroup_id": None,
                    "catalogue_family": str(case["family"]),
                    "catalogue_position": None,
                    "catalogue_size": 6,
                    "group_solvable": None,
                    "prime_divisor_count": len(sympy.factorint(len(group))),
                }
            )
        return _evaluate_sylow_intersections(case, deadline)
    if problem_id == "unsolvedmath-opg-600":
        return _search_hypercube_matching(case, deadline, metrics)
    if problem_id == "unsolvedmath-opg-382":
        return _evaluate_aharoni_berger(case, deadline)
    if problem_id == "unsolvedmath-opg-37670":
        vertices = int(case["vertices"])
        pairs = tuple(itertools.combinations(range(vertices), 2))
        missing = int(case["missing_edge_mask"])
        edges = {
            edge for bit, edge in enumerate(pairs) if not missing & (1 << bit)
        }
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(vertices)
        ]
        delta = max(degrees, default=0)
        if delta < 9:
            return None
        omega = _clique_number(vertices, edges, deadline)
        chromatic = _chromatic_number(vertices, edges, omega, deadline)
        if chromatic > max(delta - 1, omega):
            return {
                "vertices": vertices,
                "edges": [list(edge) for edge in sorted(edges)],
                "maximum_degree": delta,
                "clique_number": omega,
                "chromatic_number": chromatic,
            }
        return None
    if problem_id == "unsolvedmath-opg-404":
        k, ell = int(case["k"]), int(case["ell"])
        left = _van_der_waerden(k, ell, deadline)
        right = _van_der_waerden(k + 1, ell - 1, deadline)
        if left is None or right is None:
            return None
        if left < right:
            return {"k": k, "ell": ell, "w_k_ell": left, "w_next": right}
        return None
    if problem_id == "unsolvedmath-opg-636":
        order = int(case["order"])
        if order > 4:
            return None
        counts = _latin_parity_counts(order, deadline)
        if counts is None:
            return None
        even, odd, total = counts
        if even == odd:
            return {"order": order, "even": even, "odd": odd, "total": total}
        return None
    if problem_id == "unsolvedmath-kou-21.99":
        family = str(case["family"])
        parameter = int(case["parameter"])
        source_group = _permutation_group(family, parameter)
        subgroup = _catalogue_subgroup(
            source_group, str(case["subgroup_kind"])
        )
        if not 1 < len(subgroup) < len(source_group):
            raise RuntimeError("coset action subgroup must be nontrivial and proper")
        group, cosets = _coset_action(source_group, subgroup, deadline)
        degree = len(cosets)
        action_payload = json.dumps(
            [list(permutation) for permutation in group],
            separators=(",", ":"),
        )
        action_hash = hashlib.sha256(action_payload.encode()).hexdigest()
        faithful = len(group) == len(source_group)
        nonregular = len(group) > degree
        if str(case.get("search_role", "")).startswith(
            "faithful_nonregular"
        ) and (
            not faithful
            or not nonregular
            or action_hash != str(case.get("action_sha256", ""))
        ):
            raise RuntimeError(
                "deep KOU-21.99 case failed its faithful nonregular action guard"
            )
        if metrics is not None:
            metrics.update(
                {
                    "action_family": family,
                    "action_label": str(case["catalogue_label"]),
                    "action_degree": degree,
                    "source_group_order": len(source_group),
                    "subgroup_order": len(subgroup),
                    "action_group_order": len(group),
                    "action_sha256": action_hash,
                    "action_faithful": faithful,
                    "action_nonregular": nonregular,
                    "action_catalogue_position": case.get(
                        "catalogue_position"
                    ),
                    "action_catalogue_size": case.get("catalogue_size"),
                    "action_catalogue_shard": case.get("catalogue_shard"),
                    "action_catalogue_shard_position": case.get(
                        "catalogue_shard_position"
                    ),
                    "action_catalogue_shard_size": case.get(
                        "catalogue_shard_size"
                    ),
                }
            )
        if {permutation[0] for permutation in group} != set(range(degree)):
            return None
        for alpha in range(degree):
            for beta in range(degree):
                _check_deadline(deadline)
                if alpha == beta:
                    continue
                fixed_counts = [
                    sum(permutation[point] == point for point in range(degree))
                    for permutation in group
                    if permutation[alpha] == beta
                ]
                if fixed_counts and all(count == 1 for count in fixed_counts):
                    return {
                        "degree": degree,
                        "family": family,
                        "parameter": parameter,
                        "catalogue_label": str(case["catalogue_label"]),
                        "action_sha256": action_hash,
                        "action_faithful": faithful,
                        "action_nonregular": nonregular,
                        "source_group": [
                            list(permutation) for permutation in source_group
                        ],
                        "subgroup": sorted(subgroup),
                        "cosets": [sorted(coset) for coset in cosets],
                        "group": [list(permutation) for permutation in group],
                        "alpha": alpha,
                        "beta": beta,
                        "fixed_counts": fixed_counts,
                    }
        return None
    if problem_id == "unsolvedmath-opg-169":
        vertices = int(case["vertices"])
        pairs = tuple(itertools.combinations(range(vertices), 2))
        choices = _digits(int(case["orientation_code"]), 3, len(pairs))
        edges = [
            pair if choice == 1 else (pair[1], pair[0])
            for pair, choice in zip(pairs, choices)
            if choice
        ]
        if not any(
            _is_acyclic(
                (vertex for vertex in range(vertices) if bool(mask & (1 << vertex)) == side),
                edges,
            )
            for mask in range(1 << vertices)
            for side in (False,)
            if _is_acyclic(
                (vertex for vertex in range(vertices) if bool(mask & (1 << vertex))),
                edges,
            )
        ):
            return {"vertices": vertices, "arcs": [list(edge) for edge in edges]}
        return None
    if problem_id in {
        "unsolvedmath-opg-1793",
        "unsolvedmath-opg-46385",
    }:
        vertices = int(case["vertices"])
        edges = _directed_edges(vertices, int(case["arc_mask"]))
        if problem_id == "unsolvedmath-opg-46385":
            outdegrees = [
                sum(left == vertex for left, _ in edges)
                for vertex in range(vertices)
            ]
            minimum = min(outdegrees, default=0)
            if minimum <= 0:
                return None
            limit = math.ceil(vertices / minimum)
            if not _directed_cycles(vertices, edges, max_length=limit):
                return {
                    "vertices": vertices,
                    "arcs": [list(edge) for edge in edges],
                    "minimum_outdegree": minimum,
                    "cycle_length_limit": limit,
                }
            return None
        if problem_id == "unsolvedmath-opg-1793":
            if _directed_cycles(vertices, edges, max_length=3):
                return None
            gamma = sum(
                (left, right) not in edges and (right, left) not in edges
                for left, right in itertools.combinations(range(vertices), 2)
            )
            beta = _minimum_feedback_size(vertices, edges)
            if 2 * beta > gamma:
                return {
                    "vertices": vertices,
                    "arcs": [list(edge) for edge in edges],
                    "beta": beta,
                    "gamma": gamma,
                }
            return None
    if problem_id == "unsolvedmath-opg-48264":
        return _evaluate_graph_signing(case, deadline, metrics)
    raise KeyError(problem_id)


def verify_second_batch_finite_candidate(
    problem_id: str, candidate: Mapping[str, Any]
) -> bool:
    """Replay a finite certificate from its atomic search case."""

    if problem_id not in _SPECS_BY_ID or not isinstance(candidate, Mapping):
        return False
    search_case = candidate.get("search_case")
    witness = candidate.get("witness")
    if not isinstance(search_case, Mapping) or not isinstance(witness, Mapping):
        return False
    if problem_id == "unsolvedmath-comb-003":
        if int(witness.get("order", 0)) != 43:
            return False
        edges = tuple(itertools.combinations(range(43), 2))
        encoded_edges = tuple(
            tuple(map(int, edge)) for edge in witness.get("edges", ())
        )
        colors = tuple(map(int, witness.get("colors", ())))
        if encoded_edges != edges or len(colors) != len(edges) or set(colors) - {0, 1}:
            return False
        return not _ramsey_55_conflicts(
            colors, {edge: index for index, edge in enumerate(edges)}, None
        )
    if problem_id == "unsolvedmath-opg-369":
        modulus = int(witness.get("modulus", 0))
        vertices = int(witness.get("vertices", 0))
        edges = tuple(
            tuple(map(int, edge)) for edge in witness.get("edges", ())
        )
        weights = tuple(map(int, witness.get("weights", ())))
        if (
            modulus < 4
            or sympy.isprime(modulus)
            or vertices < 1
            or len(edges) != len(weights)
            or len(set(edges)) != len(edges)
            or any(
                len(edge) != 2
                or not 0 <= edge[0] < edge[1] < vertices
                for edge in edges
            )
            or any(not 0 <= weight < modulus for weight in weights)
        ):
            return False
        rank = _graphic_rank(vertices, edges, range(len(edges)))
        bases = tuple(
            selected
            for selected in itertools.combinations(range(len(edges)), rank)
            if _graphic_rank(vertices, edges, selected) == rank
        )
        weight_set = {
            sum(weights[index] for index in base) % modulus for base in bases
        }
        stabilizer = {
            shift
            for shift in range(modulus)
            if {(value + shift) % modulus for value in weight_set}
            == weight_set
        }
        unseen = set(range(modulus))
        cosets = []
        while unseen:
            representative = min(unseen)
            coset = {(representative + value) % modulus for value in stabilizer}
            cosets.append(coset)
            unseen -= coset
        preimage_ranks = [
            _graphic_rank(
                vertices,
                edges,
                [
                    index
                    for index, weight in enumerate(weights)
                    if weight in coset
                ],
            )
            for coset in cosets
        ]
        right_side = len(stabilizer) * (
            1 - rank + sum(preimage_ranks)
        )
        return (
            len(weight_set) < right_side
            and int(witness.get("rank", -1)) == rank
            and witness.get("bases") == [list(base) for base in bases]
            and witness.get("S") == sorted(weight_set)
            and witness.get("H") == sorted(stabilizer)
            and witness.get("cosets")
            == [sorted(coset) for coset in cosets]
            and witness.get("preimage_ranks") == preimage_ranks
            and int(witness.get("left_side", -1)) == len(weight_set)
            and int(witness.get("right_side", -1)) == right_side
        )
    if problem_id == "unsolvedmath-opg-600":
        dimension = int(witness.get("dimension", 0))
        matching = _validated_hypercube_matching(
            dimension, witness.get("matching")
        )
        case_matching = _validated_hypercube_matching(
            int(search_case.get("dimension", 0)),
            search_case.get("matching"),
        )
        if (
            matching is None
            or case_matching != matching
            or int(search_case.get("dimension", 0)) != dimension
        ):
            return False
        try:
            replayed = _search_hypercube_matching(
                {"dimension": dimension, "matching": matching},
                time.monotonic() + 30.0,
            )
        except _DeadlineExceeded:
            return False
        return replayed is not None and dict(replayed) == dict(witness)
    if problem_id == "unsolvedmath-opg-382":
        ground_size = int(witness.get("ground_size", 0))
        k = int(witness.get("k", 0))
        ell = int(witness.get("ell", 0))
        matroids = witness.get("matroids")
        raw_codes = search_case.get("matroid_codes")
        if (
            ground_size < 1
            or ground_size > 5
            or k < 2
            or k > 5
            or not 1 <= ell <= ground_size
            or not isinstance(matroids, Sequence)
            or len(matroids) != k
            or int(search_case.get("ground_size", 0)) != ground_size
            or int(search_case.get("k", 0)) != k
            or int(search_case.get("ell", 0)) != ell
            or not isinstance(raw_codes, Sequence)
            or isinstance(raw_codes, (str, bytes))
            or len(raw_codes) != k
            or any(
                not _valid_partition_matroid(matroid, ground_size)
                for matroid in matroids
            )
        ):
            return False
        expected_matroids = [
            _partition_matroid(ground_size, int(code))
            for code in raw_codes
        ]
        if list(matroids) != expected_matroids:
            return False
        for assignment in itertools.product(range(k), repeat=ground_size):
            parts = [
                [
                    element
                    for element, owner in enumerate(assignment)
                    if owner == index
                ]
                for index in range(k)
            ]
            if sum(
                _partition_matroid_rank(matroid, part)
                for matroid, part in zip(matroids, parts)
            ) < ell * (k - 1):
                return False
        return not any(
            all(
                _partition_matroid_rank(matroid, subset) == ell
                for matroid in matroids
            )
            for subset in itertools.combinations(range(ground_size), ell)
        )
    if problem_id == "unsolvedmath-opg-48264":
        family = str(search_case.get("family", ""))
        level = int(search_case.get("level", -1))
        try:
            order, edges = _group_edges(family, level)
        except (TypeError, ValueError):
            return False
        encoded_edges = tuple(
            tuple(map(int, edge)) for edge in witness.get("edges", ())
        )
        tree_edges = _spanning_tree_edge_indices(order, edges)
        free_count = len(edges) - len(tree_edges)
        degrees = [
            sum(vertex in edge for edge in edges)
            for vertex in range(order)
        ]
        if not degrees or len(set(degrees)) != 1:
            return False
        degree = degrees[0]
        threshold_squared = 4 * (degree - 1)
        certificates = witness.get("signing_witnesses")
        if (
            int(witness.get("order", 0)) != order
            or str(witness.get("family", "")) != family
            or int(witness.get("degree", 0)) != degree
            or encoded_edges != edges
            or witness.get("spanning_tree_edge_indices") != list(tree_edges)
            or int(witness.get("cycle_rank", -1)) != free_count
            or int(witness.get("threshold_squared", -1)) != threshold_squared
            or witness.get("catalogue_position")
            != search_case.get("catalogue_position")
            or witness.get("catalogue_size")
            != search_case.get("catalogue_size")
            or witness.get("catalogue_shard")
            != search_case.get("catalogue_shard")
            or witness.get("catalogue_shard_position")
            != search_case.get("catalogue_shard_position")
            or witness.get("catalogue_shard_size")
            != search_case.get("catalogue_shard_size")
            or witness.get("search_role") != search_case.get("search_role")
            or not isinstance(certificates, Sequence)
            or isinstance(certificates, (str, bytes))
            or len(certificates) != 1 << free_count
        ):
            return False
        for expected_bits, certificate in enumerate(certificates):
            if not isinstance(certificate, Mapping):
                return False
            raw_vector = certificate.get("vector")
            if (
                int(certificate.get("signing_bits", -1)) != expected_bits
                or not isinstance(raw_vector, Sequence)
                or isinstance(raw_vector, (str, bytes))
                or len(raw_vector) != order
                or any(
                    isinstance(value, bool) or not isinstance(value, int)
                    for value in raw_vector
                )
                or not any(raw_vector)
            ):
                return False
            vector = tuple(map(int, raw_vector))
            adjacency = _signed_adjacency_matrix(
                order,
                edges,
                tree_edges,
                expected_bits,
            )
            threshold_matrix = _signing_threshold_matrix(
                adjacency,
                threshold_squared,
            )
            quadratic_value = _integer_quadratic_value(
                threshold_matrix,
                vector,
            )
            if (
                quadratic_value >= 0
                or int(certificate.get("quadratic_value", 0))
                != quadratic_value
            ):
                return False
        return True
    replayed = _evaluate(problem_id, dict(search_case))
    return replayed is not None and dict(replayed) == dict(witness)


def run_second_batch_finite_search(
    problem_id: str,
    *,
    strategy_id: str,
    budget: Mapping[str, Any],
    seed: int,
    checkpoint: Mapping[str, Any] | None = None,
    progress: Callable[..., None] | None = None,
) -> dict[str, Any]:
    if problem_id not in _SPECS_BY_ID:
        raise KeyError(problem_id)
    allowed_strategies = tuple(_SPECS_BY_ID[problem_id]["strategies"])
    if strategy_id not in allowed_strategies:
        raise ValueError(
            f"unsupported strategy {strategy_id!r}; "
            f"expected one of {allowed_strategies}"
        )
    stored = dict(checkpoint or {})
    if stored:
        if stored.get("strategy_id") != strategy_id:
            raise ValueError("checkpoint strategy_id does not match")
        if int(stored.get("seed", seed)) != int(seed):
            raise ValueError("checkpoint seed does not match")
    cursor = int(stored.get("next_case", 0))
    checked = 0
    candidate = None
    started = time.monotonic()
    max_cases = _max_cases(budget)
    time_limit = _time_seconds(budget)
    deadline = started + time_limit if time_limit else None
    timed_out = False
    catalogue_exhausted = False
    last_reported_cursor: int | None = None
    stored_coverage = stored.get("coverage")
    search_metrics: dict[str, Any] = (
        copy.deepcopy(dict(stored_coverage))
        if isinstance(stored_coverage, Mapping)
        else {}
    )

    def merge_case_metrics(case_metrics: Mapping[str, Any]) -> None:
        if "flips" in case_metrics:
            search_metrics["flips"] = int(
                search_metrics.get("flips", 0)
            ) + int(case_metrics["flips"])
            if case_metrics.get("best_conflicts") is not None:
                search_metrics["best_conflicts"] = min(
                    int(search_metrics.get("best_conflicts", 1 << 60)),
                    int(case_metrics["best_conflicts"]),
                )
            elif "best_conflicts" not in search_metrics:
                search_metrics["best_conflicts"] = None
            search_metrics.setdefault("trajectory_hashes", []).append(
                str(case_metrics["trajectory_hash"])
            )
            search_metrics["initialization"] = case_metrics.get(
                "initialization"
            )
            basin = str(case_metrics.get("search_basin") or "")
            if basin:
                search_metrics["search_basins_tested"] = sorted(
                    {
                        *map(
                            str,
                            search_metrics.get("search_basins_tested", []),
                        ),
                        basin,
                    }
                )
            base_hash = case_metrics.get("base_coloring_sha256")
            if base_hash:
                search_metrics["base_coloring_hashes"] = sorted(
                    {
                        *map(
                            str,
                            search_metrics.get("base_coloring_hashes", []),
                        ),
                        str(base_hash),
                    }
                )
            search_metrics["max_active_edge_count"] = max(
                int(search_metrics.get("max_active_edge_count", 0)),
                int(case_metrics.get("active_edge_count", 0)),
            )
            search_metrics["edge_space_size"] = int(
                case_metrics.get(
                    "edge_space_size",
                    search_metrics.get("edge_space_size", 0),
                )
            )
            for key in (
                "base_perturbation_accepts",
                "base_perturbation_proposals",
                "base_changed_edges",
            ):
                if key in case_metrics:
                    search_metrics[key] = int(
                        search_metrics.get(key, 0)
                    ) + int(case_metrics[key])
        if "group_order" in case_metrics:
            search_metrics["group_orders_tested"] = sorted(
                {
                    *map(int, search_metrics.get("group_orders_tested", [])),
                    int(case_metrics["group_order"]),
                }
            )
            group_id = case_metrics.get("smallgroup_id")
            if group_id is not None:
                encoded_id = list(map(int, group_id))
                existing_ids = [
                    list(map(int, value))
                    for value in search_metrics.get(
                        "smallgroup_ids_tested", []
                    )
                ]
                if encoded_id not in existing_ids:
                    existing_ids.append(encoded_id)
                search_metrics["smallgroup_ids_tested"] = existing_ids
            family = case_metrics.get("catalogue_family")
            if family:
                search_metrics["group_families_tested"] = sorted(
                    {
                        *map(
                            str,
                            search_metrics.get("group_families_tested", []),
                        ),
                        str(family),
                    }
                )
            if case_metrics.get("catalogue_position") is not None:
                search_metrics["group_catalogue_positions_tested"] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "group_catalogue_positions_tested", []
                            ),
                        ),
                        int(case_metrics["catalogue_position"]),
                    }
                )
                search_metrics["group_catalogue_shards_tested"] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "group_catalogue_shards_tested", []
                            ),
                        ),
                        int(case_metrics["catalogue_shard"]),
                    }
                )
        if "action_sha256" in case_metrics:
            search_metrics["action_hashes_tested"] = sorted(
                {
                    *map(
                        str,
                        search_metrics.get("action_hashes_tested", []),
                    ),
                    str(case_metrics["action_sha256"]),
                }
            )
            search_metrics["action_labels_tested"] = sorted(
                {
                    *map(
                        str,
                        search_metrics.get("action_labels_tested", []),
                    ),
                    str(case_metrics["action_label"]),
                }
            )
            search_metrics["action_degrees_tested"] = sorted(
                {
                    *map(
                        int,
                        search_metrics.get("action_degrees_tested", []),
                    ),
                    int(case_metrics["action_degree"]),
                }
            )
            for metric_key, coverage_key in (
                ("action_family", "action_families_tested"),
                ("source_group_order", "source_group_orders_tested"),
                ("subgroup_order", "subgroup_orders_tested"),
                ("action_group_order", "action_group_orders_tested"),
            ):
                value = case_metrics[metric_key]
                cast = str if metric_key == "action_family" else int
                search_metrics[coverage_key] = sorted(
                    {
                        *map(cast, search_metrics.get(coverage_key, [])),
                        cast(value),
                    }
                )
            position = case_metrics.get("action_catalogue_position")
            if position is not None:
                search_metrics["action_catalogue_positions_tested"] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "action_catalogue_positions_tested", []
                            ),
                        ),
                        int(position),
                    }
                )
                search_metrics["action_catalogue_shards_tested"] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "action_catalogue_shards_tested", []
                            ),
                        ),
                        int(case_metrics["action_catalogue_shard"]),
                    }
                )
        if "signing_graph_sha256" in case_metrics:
            search_metrics["signing_graph_hashes_tested"] = sorted(
                {
                    *map(
                        str,
                        search_metrics.get(
                            "signing_graph_hashes_tested", []
                        ),
                    ),
                    str(case_metrics["signing_graph_sha256"]),
                }
            )
            search_metrics["signing_graph_families_tested"] = sorted(
                {
                    *map(
                        str,
                        search_metrics.get(
                            "signing_graph_families_tested", []
                        ),
                    ),
                    str(case_metrics["signing_graph_family"]),
                }
            )
            search_metrics["normalized_signings_checked_total"] = int(
                search_metrics.get("normalized_signings_checked_total", 0)
            ) + int(case_metrics["normalized_signings_checked"])
            signing_position = case_metrics.get(
                "signing_catalogue_position"
            )
            if signing_position is not None:
                search_metrics[
                    "signing_catalogue_positions_tested"
                ] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "signing_catalogue_positions_tested", []
                            ),
                        ),
                        int(signing_position),
                    }
                )
                search_metrics["signing_catalogue_shards_tested"] = sorted(
                    {
                        *map(
                            int,
                            search_metrics.get(
                                "signing_catalogue_shards_tested", []
                            ),
                        ),
                        int(case_metrics["signing_catalogue_shard"]),
                    }
                )
        if "matching_sha256" in case_metrics:
            search_metrics["matching_hashes_tested"] = sorted(
                {
                    *map(
                        str,
                        search_metrics.get("matching_hashes_tested", []),
                    ),
                    str(case_metrics["matching_sha256"]),
                }
            )
            search_metrics["matching_sizes_tested"] = sorted(
                {
                    *map(
                        int,
                        search_metrics.get("matching_sizes_tested", []),
                    ),
                    int(case_metrics["matching_size"]),
                }
            )
        for solver_result in case_metrics.get("solver_results", []):
            key = (
                f"{solver_result['encoding']}:"
                f"{solver_result['status']}"
            )
            counts = dict(
                search_metrics.get("hypercube_solver_status_counts", {})
            )
            counts[key] = int(counts.get(key, 0)) + 1
            search_metrics["hypercube_solver_status_counts"] = counts
        for key in (
            "normalized_signings_checked",
            "cycle_rank",
            "graph_order",
            "graph_degree",
            "direction_count",
            "matching_size",
            "matching_sha256",
            "frontier_exceeded",
            "search_role",
            "perfect_matching_extendable",
            "known_family_reasons",
            "action_faithful",
            "action_nonregular",
            "action_catalogue_size",
            "action_catalogue_shard",
            "action_catalogue_shard_position",
            "action_catalogue_shard_size",
            "catalogue_size",
            "catalogue_family_position",
            "catalogue_family_size",
            "catalogue_shard_position",
            "catalogue_shard_size",
            "group_search_role",
            "group_solvable",
            "prime_divisor_count",
            "signing_certificate_method",
            "signing_catalogue_size",
            "signing_catalogue_shard",
            "signing_catalogue_shard_position",
            "signing_catalogue_shard_size",
            "signing_search_role",
            "max_flips_configured",
            "solver_active_encoding",
            "solver_timeout_encoding",
        ):
            if key in case_metrics:
                search_metrics[key] = case_metrics[key]

    def checkpoint_payload() -> dict[str, Any]:
        next_logical_index = _seeded_index(
            problem_id, cursor, strategy_id, int(seed)
        )
        return {
            "next_case": cursor,
            "strategy_id": strategy_id,
            "seed": int(seed),
            "stratum": (
                _catalogue_strategy_shard(strategy_id)
                if _catalogue_strategy_shard(strategy_id) is not None
                else next_logical_index % 97
                if strategy_id == "deep-diversified"
                and problem_id in _DIVERSIFIED_IDS
                else 0
            ),
            "atomic_boundary": "one complete finite case",
            "coverage": copy.deepcopy(search_metrics),
        }

    while checked < max_cases:
        if time_limit and time.monotonic() - started >= time_limit:
            timed_out = True
            break
        logical_index = _seeded_index(
            problem_id, cursor, strategy_id, int(seed)
        )
        try:
            search_case = _case(problem_id, logical_index)
        except _FiniteCatalogueExhausted:
            catalogue_exhausted = True
            break
        if problem_id == "unsolvedmath-comb-003":
            search_case["max_flips"] = int(
                budget.get(
                    "max_flips",
                    (
                        25_000
                        if strategy_id == "screen-exact"
                        else _RAMSEY_DEEP_CHUNK_FLIPS
                    ),
                )
            )
        case_metrics: dict[str, Any] = {}
        try:
            witness = _evaluate(
                problem_id,
                search_case,
                deadline=deadline,
                metrics=case_metrics,
            )
        except _DeadlineExceeded:
            if problem_id != "unsolvedmath-comb-003":
                merge_case_metrics(case_metrics)
            timed_out = True
            break
        merge_case_metrics(case_metrics)
        checked += 1
        cursor += 1
        if progress is not None and checked % 100 == 0:
            progress(checkpoint_payload(), checked)
            last_reported_cursor = cursor
        if witness is not None:
            candidate = {
                "problem_id": problem_id,
                "search_case": search_case,
                "witness": witness,
                "verification_method": (
                    "exact replay by verify_second_batch_finite_candidate"
                ),
            }
            if not verify_second_batch_finite_candidate(problem_id, candidate):
                raise RuntimeError("internally generated finite witness failed replay")
            break
    final_checkpoint = checkpoint_payload()
    if progress is not None and last_reported_cursor != cursor:
        progress(final_checkpoint, checked)
    elapsed = time.monotonic() - started
    stop_reason = (
        "candidate_found"
        if candidate is not None
        else "finite_catalogue_exhausted"
        if catalogue_exhausted
        else "time_budget_exhausted"
        if timed_out or (time_limit and elapsed >= time_limit)
        else "case_budget_exhausted"
    )
    return {
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "strategy_id": strategy_id,
        "outcome": "candidate" if candidate is not None else "inconclusive",
        "candidate": candidate,
        "checked_cases": checked,
        "stop_reason": stop_reason,
        "checkpoint": final_checkpoint,
        "model_contract": dict(_SPECS_BY_ID[problem_id]["model_contract"]),
        "tool_versions": {
            "executor": EXECUTOR_VERSION,
            "python": ".".join(map(str, __import__("sys").version_info[:3])),
            "sympy": sympy.__version__,
            "numpy": numpy.__version__,
            "gap_binary": (
                str(GAP_BINARY) if GAP_BINARY.exists() else None
            ),
            "z3_cli": shutil.which("z3"),
        },
        "metrics": {
            "elapsed_seconds": elapsed,
            "atomic_cases": checked,
            "timed_out_mid_case": timed_out,
            "finite_catalogue_exhausted": catalogue_exhausted,
            "claim_scope": _SPECS_BY_ID[problem_id]["claim_scope"],
            **search_metrics,
        },
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "SECOND_BATCH_FINITE_SPECS",
    "run_second_batch_finite_search",
    "verify_second_batch_finite_candidate",
]
