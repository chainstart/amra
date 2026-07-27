from __future__ import annotations

from array import array
import copy
import itertools
import math
import random
import re
import signal
import shutil
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Mapping

import sympy
from sympy import (
    Poly,
    bernoulli,
    factorint,
    isprime,
    jacobi_symbol,
    nextprime,
    symbols,
    totient,
)
from sympy.ntheory.primetest import is_strong_lucas_prp, mr


EXECUTOR_VERSION = "amra.second_batch_arithmetic.v2"
GAP_BINARY = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap"
)
GAP_ROOT = Path("/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap")
NUMBER_THEORY_BIN = Path("/home/biostar/.cache/amra/tools/number-theory/usr/bin")
_RUNTIME_STATE = threading.local()
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND = 1 << 64
_RESUMABLE_PROBLEMS = frozenset(
    {
        "unsolvedmath-kou-21.87",
        "unsolvedmath-kou-21.88",
        "unsolvedmath-kou-21.89",
        "unsolvedmath-kou-21.115",
        "unsolvedmath-opg-156",
        "unsolvedmath-opg-37396",
        "unsolvedmath-opg-37404",
        "unsolvedmath-opg-416",
        "unsolvedmath-opg-491",
        "unsolvedmath-opg-511",
        "unsolvedmath-opg-563",
        "unsolvedmath-opg-791",
        "unsolvedmath-opg-822",
        "unsolvedmath-nt-035",
        "unsolvedmath-nt-059",
        "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45",
        "unsolvedmath-geo-025",
        "unsolvedmath-hl-b",
        "unsolvedmath-opg-508",
        "unsolvedmath-nt-058",
    }
)

_CLAIM_SCOPE_OVERRIDES: dict[str, tuple[str, str]] = {
    "unsolvedmath-kou-21.130": (
        "restricted_family",
        "The search covers odd cyclic groups only, not all finite odd abelian groups.",
    ),
    "unsolvedmath-kou-21.137": (
        "explicit_subclaim",
        "The search tests only the stated abelian conclusions at exponent p^2 or 8.",
    ),
    "unsolvedmath-kou-21.35": (
        "restricted_family",
        "The word is fixed to the basic commutator rather than every multilinear commutator word.",
    ),
    "unsolvedmath-kou-21.113": (
        "explicit_subclaim",
        "The search addresses part (a), not the projective-module question in part (b).",
    ),
    "unsolvedmath-kou-21.115": (
        "restricted_family",
        "The search covers coset unions in finite cyclic groups only.",
    ),
    "unsolvedmath-opg-791": (
        "restricted_family",
        "The search covers monic quartics with four distinct integer roots only.",
    ),
    "unsolvedmath-opg-416": (
        "restricted_family",
        "The exact interval model covers distinct integer speed tuples only.",
    ),
    "unsolvedmath-kou-21.87": (
        "restricted_family",
        "The exact finite-group predicate is restricted to groups in GAP SmallGroups.",
    ),
    "unsolvedmath-kou-21.88": (
        "witness_search",
        "A witness settles existence, while nonfinding in GAP SmallGroups cannot prove nonexistence.",
    ),
    "unsolvedmath-kou-21.89": (
        "full_claim",
        "The full partition-divisibility predicate is checked, but nonfinding covers only n through the recorded bound.",
    ),
    "unsolvedmath-opg-511": (
        "witness_search",
        "Only Part (1), the Baillie-PSW counterexample search, is covered; Part (2) is excluded.",
    ),
    "unsolvedmath-opg-60034": (
        "explicit_subclaim",
        "A multiplicity above eight refutes only the proposed bound eight, not finiteness of a larger bound.",
    ),
    "unsolvedmath-opg-508": (
        "witness_search",
        "A witness settles the existence branch, while nonfinding cannot prove nonexistence.",
    ),
    "unsolvedmath-guy-a12a": (
        "witness_search",
        "A positive square-pseudoprime witness answers the existence question; nonfinding cannot establish nonexistence beyond the recorded bound.",
    ),
    "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45": (
        "restricted_family",
        "A counterexample over a prime field refutes the full matroid conjecture; nonfinding covers only the recorded representable instances.",
    ),
    "unsolvedmath-nt-058": (
        "restricted_family",
        "The search requires positive, internally distinct, disjoint bases on the two sides.",
    ),
    "unsolvedmath-geo-025": (
        "restricted_family",
        "A witness in either executable family refutes the full conjecture; nonfinding covers only the named d<=4 cube/cross-polytope screen and the recorded deep sign-vector conv(+-v_i), v_i in {+-1}^d, strata.",
    ),
}


class _SearchTimeLimit(TimeoutError):
    pass


def _remaining_runtime_seconds() -> float | None:
    deadline = getattr(_RUNTIME_STATE, "deadline", None)
    if deadline is None:
        return None
    return float(deadline) - time.monotonic()


@contextmanager
def _atomic_progress_commit():
    is_main_thread = threading.current_thread() is threading.main_thread()
    can_mask_signal = is_main_thread and hasattr(signal, "pthread_sigmask")
    previous_mask = None
    previous_trace = None
    if can_mask_signal:
        previous_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK,
            {signal.SIGALRM},
        )
    else:
        previous_trace = sys.gettrace()
        if previous_trace is not None:
            sys.settrace(None)
    try:
        yield
    finally:
        if previous_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        elif previous_trace is not None:
            sys.settrace(previous_trace)


@contextmanager
def _bounded_runtime(seconds: float | None):
    if seconds is None:
        yield
        return
    seconds = float(seconds)
    if seconds <= 0:
        raise ValueError("time_seconds must be positive")

    previous_deadline = getattr(_RUNTIME_STATE, "deadline", None)
    deadline = time.monotonic() + seconds
    if previous_deadline is not None:
        deadline = min(deadline, float(previous_deadline))
    _RUNTIME_STATE.deadline = deadline

    is_main_thread = threading.current_thread() is threading.main_thread()
    can_signal = is_main_thread and hasattr(signal, "setitimer")
    previous_trace = None
    previous_handler: Any = None
    previous_timer: tuple[float, float] | None = None
    started = time.monotonic()

    def raise_timeout(signum: int, frame: Any) -> None:
        del signum, frame
        raise _SearchTimeLimit("search time budget exhausted")

    if can_signal:
        previous_handler = signal.getsignal(signal.SIGALRM)
        previous_timer = signal.getitimer(signal.ITIMER_REAL)
        signal.signal(signal.SIGALRM, raise_timeout)
        remaining = max(0.001, deadline - time.monotonic())
        if previous_timer[0] > 0:
            remaining = min(remaining, previous_timer[0])
        signal.setitimer(signal.ITIMER_REAL, remaining)
    else:
        previous_trace = sys.gettrace()
        ticks = 0

        def deadline_trace(frame: Any, event: str, arg: Any):
            del frame, arg
            nonlocal ticks
            if event == "line":
                ticks += 1
                if ticks % 256 == 0 and time.monotonic() >= deadline:
                    raise _SearchTimeLimit("search time budget exhausted")
            return deadline_trace

        sys.settrace(deadline_trace)

    try:
        yield
    finally:
        if can_signal:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)
            if previous_timer is not None and previous_timer[0] > 0:
                elapsed = time.monotonic() - started
                signal.setitimer(
                    signal.ITIMER_REAL,
                    max(0.001, previous_timer[0] - elapsed),
                    previous_timer[1],
                )
        else:
            sys.settrace(previous_trace)
        _RUNTIME_STATE.deadline = previous_deadline


def _spec(
    problem_id: str,
    source_id: str,
    title: str,
    *,
    domain: str,
    model_contract: str,
    strategies: tuple[str, ...],
    screen_bounds: dict[str, int],
    deep_bounds: dict[str, int],
    source_statement: str | None = None,
    deep_search_role: str | None = None,
    frontier_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    slug = source_id.lower().replace(".", "_").replace("-", "_")
    claim_scope, scope_limitation = _CLAIM_SCOPE_OVERRIDES.get(
        problem_id,
        (
            "full_claim",
            "The model encodes the full claim, but nonfinding covers only the recorded finite bounds.",
        ),
    )
    contract: str | dict[str, str] = model_contract
    if source_statement is not None:
        contract = {
            "source_statement": source_statement,
            "counterexample_condition": model_contract,
            "claim_scope": claim_scope,
            "scope_limitation": scope_limitation,
        }
    search_role = (
        deep_search_role
        or (
            "stratified_multistart"
            if "multistart" in strategies
            else "same_enumerator_extended_bound"
        )
    )
    provenance = dict(frontier_provenance or {})
    if not provenance:
        provenance = {
            "coverage_basis": "executor_declared_extended_bounds",
            "screen_bounds": dict(screen_bounds),
            "deep_bounds": dict(deep_bounds),
            "search_stream": search_role,
        }
    spec = {
        "problem_id": problem_id,
        "source_id": source_id,
        "title": title,
        "domain": domain,
        "model_contract": contract,
        "executor_id": f"second_batch.arithmetic.{slug}.v1",
        "version": EXECUTOR_VERSION,
        "strategies": list(strategies),
        "screen_bounds": dict(screen_bounds),
        "supports_deep": len(strategies) > 1,
        "deep_launches": 3 if "multistart" in strategies else 1,
        "deep_bounds": dict(deep_bounds),
        "deep_search_role": search_role,
        "frontier_provenance": provenance,
        "claim_scope": claim_scope,
        "scope_limitation": scope_limitation,
    }
    if source_statement is not None:
        spec["source_statement"] = source_statement
    return spec


SECOND_BATCH_ARITHMETIC_SPECS: tuple[dict[str, Any], ...] = (
    _spec(
        "unsolvedmath-kou-21.87",
        "KOU-21.87",
        "Coprime indices of d-generator subgroups",
        domain="group_theory",
        model_contract=(
            "For a finite GAP SmallGroup G and d>=1, compute exactly the minimum "
            "generator number d(G) and the gcd of [G:H] over every subgroup H "
            "generated by at most d elements. A witness has gcd 1 and d(G)>d+1. "
            "The screen replicates the known solvable region; the deep strategy "
            "checks nonsolvable SmallGroups first, beginning with A5."
        ),
        strategies=("exact-small", "smallgroups-targeted"),
        screen_bounds={"max_order": 16, "max_d": 3, "max_cases": 200},
        deep_bounds={"max_order": 512, "max_d": 8, "max_cases": 100_000},
        deep_search_role="targeted_catalog_post_solvable_frontier",
        frontier_provenance={
            "known_region": "solvable finite groups",
            "deep_region": "nonsolvable GAP SmallGroups beginning with A5",
        },
        source_statement=(
            "Assume that a finite group G has a family of d-generator subgroups "
            "whose indices have no common divisor. Is it true that G can be "
            "generated by d+1 elements?"
        ),
    ),
    _spec(
        "unsolvedmath-kou-21.88",
        "KOU-21.88",
        "Odd nonabelian group with commuting probability 1/17",
        domain="group_theory",
        model_contract=(
            "A witness is an odd-order nonabelian GAP SmallGroup G whose exact "
            "conjugacy-class count k(G) satisfies 17*k(G)=|G|. Catalog enumeration "
            "first applies the necessary odd-order and 17-divisibility filters, and "
            "the deep order schedule prioritizes semidirect-factor structure."
        ),
        strategies=("exact-small", "odd-smallgroups"),
        screen_bounds={"max_order": 63, "max_cases": 1_000},
        deep_bounds={"max_order": 2_000, "max_cases": 500_000},
        deep_search_role="targeted_odd_order_catalog",
        source_statement=(
            "Is there a finite non-abelian group G of odd order, with k(G) "
            "conjugacy classes, such that k(G)/|G|=1/17?"
        ),
    ),
    _spec(
        "unsolvedmath-kou-21.2",
        "KOU-21.2",
        "Kourovka Notebook Problem 21.2",
        domain="group_theory",
        model_contract=(
            "A witness is a non-simple finite group G, a simple group S of the same "
            "order, and a bijection f with ord(x) dividing ord(f(x)) for every x."
        ),
        strategies=("exact-small", "deep-exact"),
        screen_bounds={"max_order": 16, "max_cases": 200},
        deep_bounds={"max_order": 512, "max_cases": 50_000},
    ),
    _spec(
        "unsolvedmath-kou-21.25",
        "KOU-21.25",
        "Kourovka Notebook Problem 21.25",
        domain="group_theory",
        model_contract=(
            "A witness is a finite simple SmallGroup G and primes p,q dividing |G| "
            "such that no pair of Sylow p- and q-subgroups generates G."
        ),
        strategies=("exact-small", "simple-groups"),
        screen_bounds={"max_order": 64, "max_cases": 100},
        deep_bounds={"max_order": 2_000, "max_cases": 20_000},
    ),
    _spec(
        "unsolvedmath-kou-21.59",
        "KOU-21.59",
        "Kourovka Notebook Problem 21.59",
        domain="group_theory",
        model_contract=(
            "A witness is a non-isomorphic pair G,H with the same multiset of complex "
            "irreducible character degrees, where G is almost simple or quasisimple."
        ),
        strategies=("exact-small", "character-table-join"),
        screen_bounds={"max_order": 64, "max_cases": 500},
        deep_bounds={"max_order": 2_000, "max_cases": 200_000},
    ),
    _spec(
        "unsolvedmath-kou-21.130",
        "KOU-21.130",
        "Kourovka Notebook Problem 21.130",
        domain="group_theory",
        model_contract=(
            "A witness is an odd cyclic group and a subset of size greater than two "
            "for which exhaustive cyclic orderings never have distinct adjacent sums. "
            "The negative search scope is explicitly the cyclic subgroup family."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={"max_order": 9, "max_subset": 6, "max_cases": 2_000},
        deep_bounds={"max_order": 127, "max_subset": 16, "max_cases": 2_000_000},
    ),
    _spec(
        "unsolvedmath-kou-21.137",
        "KOU-21.137",
        "Kourovka Notebook Problem 21.137",
        domain="group_theory",
        model_contract=(
            "The executable target is the explicit subclaim: for odd p and exponent "
            "p^2, or p=2 and exponent 8, if p-th powers form a subgroup then it is "
            "abelian. A witness is a SmallGroup violating that implication."
        ),
        strategies=("exact-small", "p-groups"),
        screen_bounds={"max_order": 32, "max_cases": 200},
        deep_bounds={"max_order": 4_096, "max_cases": 500_000},
    ),
    _spec(
        "unsolvedmath-kou-21.35",
        "KOU-21.35",
        "Kourovka Notebook Problem 21.35",
        domain="group_theory",
        model_contract=(
            "The targeted word is the basic commutator [x,y]. A witness is a finite "
            "SmallGroup and prime p satisfying the stated order premise for all "
            "commutator values while its derived subgroup is not p-nilpotent."
        ),
        strategies=("exact-small", "commutator-targeted"),
        screen_bounds={"max_order": 16, "max_cases": 100},
        deep_bounds={"max_order": 512, "max_cases": 100_000},
    ),
    _spec(
        "unsolvedmath-kou-21.113",
        "KOU-21.113",
        "Kourovka Notebook Problem 21.113",
        domain="group_theory",
        model_contract=(
            "The executable target is part (a). A witness is a finite SmallGroup G "
            "and p dividing |G| for which the explicitly defined class function "
            "Psi_(p,G) has a negative or non-integral irreducible multiplicity."
        ),
        strategies=("exact-small", "character-targeted"),
        screen_bounds={"max_order": 16, "max_cases": 100},
        deep_bounds={"max_order": 512, "max_cases": 100_000},
    ),
    _spec(
        "unsolvedmath-kou-21.115",
        "KOU-21.115",
        "Kourovka Notebook Problem 21.115",
        domain="group_theory",
        model_contract=(
            "The exact targeted family is finite cyclic groups. A witness is a list "
            "of distinct cosets whose union is proper but whose complement has size "
            "strictly below |G|/2^n."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={"max_order": 12, "max_cosets": 3, "max_cases": 2_000},
        deep_bounds={"max_order": 512, "max_cosets": 10, "max_cases": 10_000_000},
    ),
    _spec(
        "unsolvedmath-kou-21.134",
        "KOU-21.134",
        "Kourovka Notebook Problem 21.134",
        domain="group_theory",
        model_contract=(
            "A witness is a pair of non-isomorphic finite SmallGroups with identical "
            "power-equation type, where the reference group has trivial solvable "
            "radical or is almost simple and the comparison violates the conclusion."
        ),
        strategies=("exact-small", "type-hash-join"),
        screen_bounds={"max_order": 16, "max_cases": 200},
        deep_bounds={"max_order": 2_000, "max_cases": 500_000},
    ),
    _spec(
        "unsolvedmath-kou-21.135",
        "KOU-21.135",
        "Kourovka Notebook Problem 21.135",
        domain="group_theory",
        model_contract=(
            "A witness is a pair of finite SmallGroups with the same multiset of "
            "irreducible character degrees, where the first has trivial solvable "
            "radical and the second does not."
        ),
        strategies=("exact-small", "character-table-join"),
        screen_bounds={"max_order": 16, "max_cases": 200},
        deep_bounds={"max_order": 2_000, "max_cases": 500_000},
    ),
    _spec(
        "unsolvedmath-opg-37396",
        "OPG-37396",
        "3 is a primitive root modulo primes of the form 16 q^4 + 1",
        domain="number_theory",
        model_contract=(
            "A witness is primes q>3 and p=16q^4+1 with multiplicative order of 3 "
            "strictly smaller than p-1."
        ),
        strategies=("exact-small", "segmented-primes"),
        screen_bounds={"max_q": 1_000, "max_cases": 500},
        deep_bounds={
            "max_q": 100_000_000,
            "prime_block_size": 64,
            "segment_size": 65_536,
            "max_cases": 10_000_000,
        },
        deep_search_role="segmented_prime_q_stream",
    ),
    _spec(
        "unsolvedmath-opg-37413",
        "OPG-37413",
        "Alexa's Conjecture on Primality",
        domain="number_theory",
        model_contract=(
            "A witness is p>=8 for which primality disagrees with the stated exact "
            "modular-residue sum test."
        ),
        strategies=("exact-small", "composite-targeted"),
        screen_bounds={"max_n": 500, "max_cases": 500},
        deep_bounds={"max_n": 100_000_000, "max_cases": 100_000_000},
    ),
    _spec(
        "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45",
        "OPG-ROTAS-BASIS",
        "Rota's Basis Conjecture",
        domain="combinatorics",
        model_contract=(
            "Let M be a rank-n matroid and let B_1,...,B_n be pairwise-disjoint "
            "labelled copies of bases of M. A counterexample is such finite data "
            "for which no partition into n disjoint transversal bases exists. "
            "The executable family uses vector matroids over prime fields; row "
            "labels keep equal vectors in different input bases disjoint."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={
            "max_rank": 3,
            "max_field_prime": 2,
            "solver_node_limit": 1_000_000,
            "max_cases": 1_000,
        },
        deep_bounds={
            "minimum_rank": 5,
            "max_rank": 7,
            "max_field_prime": 5,
            "solver_node_limit": 5_000_000,
            "max_cases": 1_000_000,
        },
        deep_search_role=(
            "independent_stratified_prime_field_vector_matroid_instances"
        ),
        frontier_provenance={
            "authoritative_problem_url": (
                "https://www.openproblemgarden.org/op/rotas_basis_conjecture"
            ),
            "current_progress": "arXiv:2508.05601",
            "status": "open_in_full_generality",
            "normalization": (
                "rank-n matroid with n pairwise-disjoint labelled base copies"
            ),
        },
        source_statement=(
            "Let M be a matroid of rank n and let B_1,...,B_n be pairwise-"
            "disjoint labelled bases of M. Can their elements always be "
            "rearranged into n disjoint transversal bases?"
        ),
    ),
    _spec(
        "unsolvedmath-kou-21.89",
        "KOU-21.89",
        "Partition number p(n) dividing n!",
        domain="number_theory",
        model_contract=(
            "For every n>39 through the bound, compute p(n) by the exact generalized-"
            "pentagonal recurrence. A witness has n! mod p(n)=0, computed without "
            "constructing n!."
        ),
        strategies=("exact-small", "partition-recurrence"),
        screen_bounds={"max_n": 500, "max_cases": 461},
        deep_bounds={"max_n": 1_000_000, "max_cases": 999_961},
        source_statement=(
            "For n>39, is it true that the number of conjugacy classes in the "
            "symmetric group S_n of degree n is never a divisor of the order of "
            "S_n? In other words, is it true that, for n>39, the number p(n) of "
            "integer partitions of n is never a divisor of n!?"
        ),
    ),
    _spec(
        "unsolvedmath-opg-55810",
        "OPG-55810",
        "Are all Fermat Numbers square-free?",
        domain="number_theory",
        model_contract=(
            "A witness is n and an integer r>1 for which r^2 divides "
            "2^(2^n)+1, checked by exact modular exponentiation."
        ),
        strategies=("exact-small", "square-factor-sieve"),
        screen_bounds={"max_index": 6, "max_factor": 1_000, "max_cases": 10_000},
        deep_bounds={"max_index": 48, "max_factor": 10_000_000, "max_cases": 100_000_000},
    ),
    _spec(
        "unsolvedmath-opg-59976",
        "OPG-59976",
        "Are all Mersenne Numbers with prime exponent square-free?",
        domain="number_theory",
        model_contract=(
            "A witness is primes p,r with r^2 dividing 2^p-1, checked by exact "
            "modular exponentiation."
        ),
        strategies=("exact-small", "square-factor-sieve"),
        screen_bounds={"max_exponent": 100, "max_factor": 1_000, "max_cases": 10_000},
        deep_bounds={"max_exponent": 10_000_000, "max_factor": 10_000_000, "max_cases": 100_000_000},
    ),
    _spec(
        "unsolvedmath-opg-822",
        "OPG-822",
        "Wall-Sun-Sun primes and Fibonacci divisibility",
        domain="number_theory",
        model_contract=(
            "A witness is a prime p>5 for which p^2 divides "
            "F_(p-(p/5)), verified by fast doubling modulo p^2."
        ),
        strategies=("exact-small", "post-frontier-prime-stream"),
        screen_bounds={"max_prime": 1_000, "max_cases": 500},
        deep_bounds={
            "start_prime": 200_000_000_000_000_003,
            "max_prime": 100_000_000_000_000_000_000,
            "known_computational_lower_bound": 146_000_000_000_000_000,
            "checkpoint_block_size": 128,
            "max_cases": 100_000_000,
        },
        deep_search_role="post_frontier_prime_stream",
        frontier_provenance={
            "known_lower_bound": 146_000_000_000_000_000,
            "deep_starts_above": 200_000_000_000_000_000,
            "status": "post_known_computational_range",
        },
    ),
    _spec(
        "unsolvedmath-nt-035",
        "NT-035",
        "Lehmer's Totient Problem",
        domain="number_theory",
        model_contract=(
            "A witness is a composite squarefree n with phi(n) dividing n-1. "
            "Deep search enumerates factor subsets that satisfy Korselt's "
            "condition before applying the exact Lehmer divisibility test."
        ),
        strategies=("exact-small", "structural-post-frontier"),
        screen_bounds={"max_n": 1_000, "max_cases": 1_000},
        deep_bounds={
            "minimum_n": 1_000_000_000_000_000_000_000_000_000_001,
            "minimum_prime_factors": 15,
            "subset_block_size": 256,
            "max_cases": 10_000_000,
        },
        deep_search_role="post_frontier_korselt_subset_stream",
        frontier_provenance={
            "minimum_n_exclusive": 10**30,
            "minimum_distinct_prime_factors": 15,
            "source": "EMS 2024, DOI 10.4171/EM/492",
            "status": "necessary_conditions_enforced",
        },
    ),
    _spec(
        "unsolvedmath-nt-059",
        "NT-059",
        "Lemoine's Conjecture",
        domain="number_theory",
        model_contract=(
            "A witness is an odd n>5 for which exhaustive odd primes p leave no "
            "even semiprime n-p."
        ),
        strategies=("exact-small", "segmented-primes"),
        screen_bounds={"max_n": 1_000, "max_cases": 500},
        deep_bounds={
            "max_n": 100_000_000,
            "n_block_size": 64,
            "max_cases": 50_000_000,
        },
    ),
    _spec(
        "unsolvedmath-geo-025",
        "GEO-025",
        "Kalai's 3^d Conjecture",
        domain="geometry",
        model_contract=(
            "A counterexample is a full-dimensional centrally symmetric "
            "d-polytope with fewer than 3^d nonempty faces. Face counting "
            "includes the polytope itself and excludes the empty face, so the "
            "d-cube has exactly 3^d faces. The exact-small screen replays cubes "
            "and cross-polytopes through d=4. The deep executable family consists "
            "of centrally symmetric subpolytopes of the d-cube, represented as "
            "conv(+-v_i) for sign vectors v_i in {+-1}^d."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={
            "max_dimension": 4,
            "max_antipodal_pairs": 7,
            "max_cases": 100,
        },
        deep_bounds={
            "minimum_dimension": 5,
            "max_dimension": 7,
            "max_antipodal_pairs": 12,
            "max_facet_subsets": 2_000_000,
            "max_cases": 1_000_000,
        },
        deep_search_role=(
            "exact_non_simple_non_simplicial_sign_vector_cube_subpolytope_strata"
        ),
        frontier_provenance={
            "known_dimensions": "d <= 4",
            "open_dimensions": "d >= 5",
            "convention": (
                "all nonempty faces including P, excluding the empty face"
            ),
            "sources": [
                "arXiv:2308.02909",
                "arXiv:0708.3661",
            ],
            "status": "open_beyond_dimension_four",
        },
        source_statement=(
            "Does every centrally symmetric d-dimensional polytope have at "
            "least 3^d nonempty faces, counting the polytope itself and "
            "excluding the empty face?"
        ),
    ),
    _spec(
        "unsolvedmath-opg-37404",
        "OPG-37404",
        "Sum of prime and semiprime conjecture",
        domain="number_theory",
        model_contract=(
            "A witness is an even n>10 for which exhaustive odd primes p leave no "
            "odd semiprime n-p."
        ),
        strategies=("exact-small", "segmented-primes"),
        screen_bounds={"max_n": 1_000, "max_cases": 500},
        deep_bounds={
            "max_n": 100_000_000,
            "n_block_size": 64,
            "max_cases": 50_000_000,
        },
    ),
    _spec(
        "unsolvedmath-opg-791",
        "OPG-791",
        "Quartic rationally derived polynomials",
        domain="number_theory",
        model_contract=(
            "The targeted exact family is monic quartics with four distinct integer "
            "roots. A witness has rational roots for every positive-degree derivative."
        ),
        strategies=("exact-small", "integer-root-targeted"),
        screen_bounds={"root_height": 4, "max_cases": 1_000},
        deep_bounds={"root_height": 10_000, "max_cases": 100_000_000},
        deep_search_role="affine_normalized_root_shape_strata",
    ),
    _spec(
        "unsolvedmath-opg-563",
        "OPG-563",
        "Davenport's constant",
        domain="number_theory",
        model_contract=(
            "A direct refutation is a sequence of length d(n-1)+1 in Z_n^d with no "
            "nonempty zero-sum subsequence. Exact-small exhausts canonical sequences "
            "until its recorded case cap."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={"max_n": 2, "max_dimension": 2, "max_cases": 1_000},
        deep_bounds={
            "max_n": 15,
            "max_dimension": 8,
            "memory_mb": 1_024,
            "max_cases": 10_000_000,
        },
        deep_search_role="critical_zero_sum_free_prefix_mutation",
    ),
    _spec(
        "unsolvedmath-hl-b",
        "HL-B",
        "Hardy-Littlewood Conjecture B (Second Conjecture)",
        domain="number_theory",
        model_contract=(
            "A witness is integers x,y>=2 with pi(x+y)>pi(x)+pi(y), with all three "
            "prime counts recomputed from an exact sieve."
        ),
        strategies=("exact-small", "gap-targeted"),
        screen_bounds={"max_xy": 500, "max_cases": 250_000},
        deep_bounds={
            "max_xy": 100_000_000,
            "minimum_x_to_y_ratio": 128,
            "max_cases": 100_000_000,
        },
        deep_search_role="prime_dense_y_much_smaller_than_x_windows",
    ),
    _spec(
        "unsolvedmath-opg-416",
        "OPG-416",
        "Lonely runner conjecture",
        domain="number_theory",
        model_contract=(
            "The exact targeted family uses distinct integer speeds. A witness is a "
            "speed tuple and runner for which rational interval decomposition proves "
            "that no time has all circular distances at least 1/k."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={"max_runners": 4, "max_speed": 6, "max_cases": 1_000},
        deep_bounds={
            "minimum_runners": 14,
            "max_runners": 16,
            "max_speed": 1_000,
            "max_cases": 10_000_000,
        },
        deep_search_role="post_total_runner_13_canonical_speed_tuples",
        frontier_provenance={
            "proved_through_total_runners": 13,
            "deep_total_runner_counts": [14, 15, 16],
            "source": "arXiv:2604.23906",
            "status": "strictly_post_frontier",
        },
    ),
    _spec(
        "unsolvedmath-opg-156",
        "OPG-156",
        "Few subsequence sums in Z_n x Z_n",
        domain="number_theory",
        model_contract=(
            "A witness is a zero-free sequence in Z_n^2 of the stated length whose "
            "exact set of subsequence sums is smaller than that of the proposed "
            "canonical sequence."
        ),
        strategies=("exact-small", "multistart"),
        screen_bounds={"max_n": 3, "max_cases": 2_000},
        deep_bounds={"max_n": 16, "max_cases": 10_000_000},
    ),
    _spec(
        "unsolvedmath-opg-60034",
        "OPG-60034",
        "Singmaster's conjecture",
        domain="number_theory",
        model_contract=(
            "The executable target is the widely discussed candidate upper bound 8, "
            "not the finiteness conjecture itself. A witness is a Pascal-triangle "
            "value other than 1 occurring at least nine times within the complete "
            "rows through the recorded bound."
        ),
        strategies=("exact-small", "multiplicity-targeted"),
        screen_bounds={"max_row": 100, "max_cases": 10_000},
        deep_bounds={"max_row": 1_000_000, "max_cases": 100_000_000},
    ),
    _spec(
        "unsolvedmath-guy-a12a",
        "GUY-A12a",
        "Square Pseudoprimes",
        domain="number_theory",
        model_contract=(
            "A witness is a square base-2 Fermat pseudoprime not divisible by either "
            "of the two square factors named in the question."
        ),
        strategies=("exact-small", "square-targeted"),
        screen_bounds={"max_root": 1_000, "max_cases": 1_000},
        deep_bounds={"max_root": 100_000_000, "max_cases": 100_000_000},
    ),
    _spec(
        "unsolvedmath-opg-508",
        "OPG-508",
        "A sextic counterexample to Euler's sum of powers conjecture",
        domain="number_theory",
        model_contract=(
            "A witness is six positive integers satisfying the displayed exact "
            "five-versus-one sixth-power identity. Failure to find one is reported "
            "only as a bounded witness search, never as nonexistence."
        ),
        strategies=("exact-small", "meet-in-the-middle"),
        screen_bounds={"max_base": 8, "max_cases": 10_000},
        deep_bounds={"max_base": 100_000, "max_cases": 100_000_000},
        deep_search_role="random_partial_tuple_exact_root_completion",
    ),
    _spec(
        "unsolvedmath-opg-511",
        "OPG-511",
        "Counterexamples to the Baillie-PSW primality test",
        domain="number_theory",
        model_contract=(
            "Only Part (1) is searched. A witness is an odd composite n that passes "
            "both strong Miller-Rabin to base 2 and the Method A/Selfridge strong "
            "Lucas probable-prime test, accompanied by a replayable nontrivial "
            "factor. The bounded screen is replication below the published exhaustive "
            "lower bound 2^64; discovery uses two structurally different families "
            "whose every tested integer is strictly greater than 2^64."
        ),
        strategies=("exact-small", "chernick-korselt", "remote-factor-layers"),
        screen_bounds={
            "start_n": 3,
            "max_n": 100_000,
            "segment_size": 4_096,
            "max_cases": 50_000,
        },
        deep_bounds={
            "discovery_min_n": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND + 1,
            "max_n": 10**27,
            "structure_block_size": 256,
            "remote_block_size": 32,
            "remote_layers": 24,
            "max_cases": 100_000_000,
        },
        deep_search_role="post_frontier_structural_families",
        frontier_provenance={
            "screen_role": "published_range_replication_below_2^64",
            "deep_region": "all tested integers are greater than 2^64",
            "part_number": 1,
            "excluded_other_part": (
                "Part (2), the Fibonacci divisibility subproblem"
            ),
            "nonoverlap": (
                "GUY-A12B executes Part (2); this executor only searches "
                "Baillie-PSW Part (1)"
            ),
        },
        source_statement=(
            "Problem (1) Find a counterexample to Baillie-PSW primality test or "
            "prove that there is no one. Problem (2) Find a composite n congruent "
            "to 3 or 7 modulo 10 which divides both 2^(n-1)-1 and F_(n+1), or "
            "prove that there is no such n."
        ),
    ),
    _spec(
        "unsolvedmath-opg-491",
        "OPG-491",
        "Odd incongruent covering systems",
        domain="number_theory",
        model_contract=(
            "A witness is a finite set of pairwise distinct odd moduli greater than "
            "one and residues whose congruence classes cover a complete lcm period."
        ),
        strategies=("exact-small", "cover-targeted"),
        screen_bounds={"max_modulus": 9, "max_moduli": 3, "max_cases": 20_000},
        deep_bounds={
            "max_modulus": 999,
            "max_moduli": 20,
            "max_period": 2_000_000,
            "max_cases": 100_000_000,
        },
        deep_search_role="smooth_period_large_modulus_multistart",
    ),
    _spec(
        "unsolvedmath-nt-058",
        "NT-058",
        "Lander-Parkin-Selfridge Conjecture",
        domain="number_theory",
        model_contract=(
            "The targeted exact family requires all positive bases on opposite sides "
            "to be disjoint. A witness has equal sums of k-th powers with m+n<k."
        ),
        strategies=("exact-small", "meet-in-the-middle"),
        screen_bounds={"max_power": 5, "max_base": 8, "max_cases": 20_000},
        deep_bounds={"max_power": 16, "max_base": 1_000_000, "max_cases": 100_000_000},
        deep_search_role="random_terms_exact_power_root_completion",
    ),
)


_SPECS_BY_ID = {str(spec["problem_id"]): spec for spec in SECOND_BATCH_ARITHMETIC_SPECS}


def _budget_dict(budget: Any) -> dict[str, Any]:
    if budget is None:
        return {}
    if isinstance(budget, Mapping):
        return dict(budget)
    if hasattr(budget, "to_dict"):
        return dict(budget.to_dict())
    try:
        return dict(vars(budget))
    except TypeError as exc:
        raise TypeError("budget must be a mapping or expose to_dict()") from exc


def _case_rng(seed: int, case_index: int, salt: int) -> random.Random:
    mixed = (
        (int(seed) & ((1 << 64) - 1))
        ^ ((int(case_index) + 1) * 0x9E3779B97F4A7C15)
        ^ (int(salt) * 0xD1B54A32D192ED03)
    ) & ((1 << 128) - 1)
    return random.Random(mixed)


def _positive_int(
    budget: Mapping[str, Any],
    key: str,
    default: int,
    *,
    minimum: int = 1,
) -> int:
    try:
        value = int(budget.get(key, default))
    except (TypeError, ValueError):
        value = default
    return max(minimum, value)


class _SearchProgressState:
    """Durable block cursor shared by the four long-running arithmetic searches."""

    def __init__(
        self,
        *,
        problem_id: str,
        strategy_id: str,
        checkpoint: Mapping[str, Any] | None,
        progress: Callable[[Mapping[str, Any], int], Any] | None,
        resumable: bool,
    ) -> None:
        raw = dict(checkpoint or {})
        nested = raw.get("cursor")
        if isinstance(nested, Mapping):
            raw = dict(nested)
        compatible = (
            resumable
            and raw.get("problem_id") == problem_id
            and raw.get("effective_strategy_id", raw.get("strategy_id"))
            == strategy_id
        )
        if not compatible:
            raw = {}
        self.problem_id = problem_id
        self.strategy_id = strategy_id
        self.progress = progress
        self.resumable = resumable
        self.checkpoint_received = checkpoint is not None
        self.restored = bool(raw)
        self.checked = int(raw.get("checked_cases", 0)) if raw else 0
        self.metrics: dict[str, Any] = copy.deepcopy(
            dict(raw.get("metrics") or {})
        )
        self.cursor: dict[str, Any] = copy.deepcopy(raw) or {
            "problem_id": problem_id,
            "effective_strategy_id": strategy_id,
            "phase": "starting",
            "checked_cases": self.checked,
            "metrics": {},
        }

    def commit(
        self,
        *,
        checked_increment: int = 0,
        cursor: Mapping[str, Any] | None = None,
        metrics: Mapping[str, Any] | None = None,
    ) -> None:
        increment = int(checked_increment)
        if increment < 0:
            raise ValueError("checked_increment must not be negative")
        next_checked = self.checked + increment
        next_metrics = (
            self.metrics
            if metrics is None
            else copy.deepcopy(dict(metrics))
        )
        next_cursor = {
            "problem_id": self.problem_id,
            "effective_strategy_id": self.strategy_id,
            "phase": "searching",
            "checked_cases": next_checked,
            **copy.deepcopy(dict(cursor or {})),
            "metrics": copy.deepcopy(next_metrics),
        }
        with _atomic_progress_commit():
            self.checked = next_checked
            self.metrics = next_metrics
            self.cursor = next_cursor
        if self.progress is not None:
            self.progress(copy.deepcopy(next_cursor), next_checked)

    def final_cursor(
        self,
        *,
        phase: str,
        exhausted: bool,
        search_completed: bool,
    ) -> dict[str, Any]:
        return {
            **copy.deepcopy(self.cursor),
            "problem_id": self.problem_id,
            "effective_strategy_id": self.strategy_id,
            "phase": phase,
            "checked_cases": self.checked,
            "checked_cases_exact": True,
            "search_completed": bool(search_completed),
            "bounded_scope_exhausted": bool(exhausted),
            "metrics": copy.deepcopy(self.metrics),
            "resume": {
                "mode": "block_cursor" if self.resumable else "atomic_bound_restart",
                "checkpoint_received": self.checkpoint_received,
                "intra_bound_cursor_restored": self.restored,
                "note": (
                    "The next block cursor is durable; at most the active unfinished "
                    "block is replayed."
                    if self.resumable
                    else "This bounded generator does not expose an intra-bound cursor."
                ),
            },
        }


def _coverage_metrics(
    state: _SearchProgressState,
    *,
    family: str,
    values: list[int],
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    metrics = dict(state.metrics)
    if extra:
        metrics.update(dict(extra))
    family_counts = {
        str(key): int(value)
        for key, value in dict(metrics.get("family_sample_counts") or {}).items()
    }
    family_counts[family] = family_counts.get(family, 0) + len(values)
    metrics["family_sample_counts"] = family_counts
    if values:
        observed_min = min(values)
        observed_max = max(values)
        previous_min = metrics.get("min_tested_n")
        previous_max = metrics.get("max_tested_n")
        metrics["min_tested_n"] = (
            observed_min if previous_min is None else min(int(previous_min), observed_min)
        )
        metrics["max_tested_n"] = (
            observed_max if previous_max is None else max(int(previous_max), observed_max)
        )
    return metrics


@lru_cache(maxsize=1)
def _gap_version() -> str | None:
    if not GAP_BINARY.exists() or not GAP_ROOT.exists():
        return None
    completed = subprocess.run(
        [str(GAP_BINARY), "-l", str(GAP_ROOT), "-q"],
        input='Print(GAPInfo.Version, "\\n");; QUIT;\n',
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if completed.returncode:
        return None
    return completed.stdout.strip().splitlines()[0] if completed.stdout.strip() else None


def _tool_versions() -> dict[str, Any]:
    return {
        "python_sympy": sympy.__version__,
        "gap": _gap_version(),
        "smallgrp": "bundled with isolated GAP 4.12.1" if _gap_version() else None,
        "pari_gp": "2.15.4" if (NUMBER_THEORY_BIN / "gp").exists() else None,
        "primesieve": "12" if (NUMBER_THEORY_BIN / "primesieve").exists() else None,
        "primecount": "7.10" if (NUMBER_THEORY_BIN / "primecount").exists() else None,
        "z3_cli": shutil.which("z3"),
    }


def _run_gap(script: str, *, timeout: int = 120) -> str:
    if _gap_version() is None:
        raise RuntimeError(f"isolated GAP is unavailable at {GAP_BINARY}")
    effective_timeout = float(max(1, timeout))
    remaining = _remaining_runtime_seconds()
    if remaining is not None:
        if remaining <= 0:
            raise _SearchTimeLimit("search time budget exhausted before GAP launch")
        effective_timeout = min(effective_timeout, max(0.001, remaining))
    try:
        completed = subprocess.run(
            [str(GAP_BINARY), "-l", str(GAP_ROOT), "-q"],
            input=script + "\nQUIT;\n",
            text=True,
            capture_output=True,
            timeout=effective_timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise _SearchTimeLimit("GAP subprocess exceeded search time budget") from exc
    stdout = _ANSI_ESCAPE.sub("", completed.stdout or "")
    stderr = _ANSI_ESCAPE.sub("", completed.stderr or "")
    gap_failed = (
        completed.returncode != 0
        or bool(stderr.strip())
        or re.search(r"(?m)^Error,", stdout) is not None
        or "you can 'quit;' to quit to outer loop" in stdout
        or re.search(r"(?m)^brk>", stdout) is not None
    )
    if gap_failed:
        detail = (stderr or stdout).strip()
        raise RuntimeError(f"GAP exited {completed.returncode}: {detail}")
    return stdout


def _parse_gap_result(output: str) -> tuple[dict[str, Any] | None, int]:
    candidate: dict[str, Any] | None = None
    checked: int | None = None
    for raw in output.splitlines():
        line = raw.strip()
        if line.startswith("CAND|"):
            fields = line.split("|")
            candidate = {"fields": [int(value) for value in fields[1:]]}
        elif line.startswith("DONE|"):
            checked = int(line.split("|", 1)[1])
    if checked is None:
        raise RuntimeError("GAP search protocol ended without a DONE marker")
    return candidate, checked


def _semidirect_factor_score(order: int) -> tuple[int, int, int]:
    factors = factorint(order)
    primes = sorted(int(prime) for prime in factors)
    interactions = 0
    for source in primes:
        for target in primes:
            if source == target:
                continue
            exponent = int(factors[target])
            if any(pow(target, power, source) == 1 for power in range(1, exponent + 2)):
                interactions += 1
    return (-interactions, -len(primes), order)


@lru_cache(maxsize=32)
def _targeted_gap_coordinates(
    problem_id: str,
    max_order: int,
    strategy_id: str,
) -> tuple[tuple[tuple[int, int], ...], tuple[int, ...], dict[str, Any]]:
    if problem_id == "unsolvedmath-kou-21.87":
        if strategy_id == "smallgroups-targeted":
            script = f"""
orders:=Filtered([1..{max_order}],o->SmallGroupsAvailable(o));;
ids:=IdsOfAllSmallGroups(Size,orders,IsSolvableGroup,false);;
for id in ids do Print("ID|",id[1],"|",id[2],"\\n"); od;
Print("META|nonsolvable_only\\n");
"""
            coverage_kind = "nonsolvable_smallgroups_discovery"
        else:
            replication_max_order = min(max_order, 32)
            script = f"""
for o in [1..{replication_max_order}] do
 if SmallGroupsAvailable(o) then
  for idx in [1..NumberSmallGroups(o)] do
   Print("ID|",o,"|",idx,"\\n");
  od;
 fi;
od;
Print("META|solvable_replication\\n");
"""
            coverage_kind = "known_solvable_screen_replication"
    elif problem_id == "unsolvedmath-kou-21.88":
        script = f"""
for o in [1..{max_order}] do
 if o mod 2=1 and o mod 17=0 then
  if SmallGroupsAvailable(o) then
   for idx in [1..NumberSmallGroups(o)] do
    Print("ID|",o,"|",idx,"\\n");
   od;
  else
   Print("UNAVAILABLE|",o,"\\n");
  fi;
 fi;
od;
Print("META|odd_and_17_divisible_prefilter\\n");
"""
        coverage_kind = "odd_17_divisible_smallgroups"
    else:
        raise KeyError(problem_id)

    coordinates: list[tuple[int, int]] = []
    unavailable: list[int] = []
    for raw in _run_gap(script, timeout=60).splitlines():
        line = raw.strip()
        if line.startswith("ID|"):
            _, order, index = line.split("|")
            coordinates.append((int(order), int(index)))
        elif line.startswith("UNAVAILABLE|"):
            unavailable.append(int(line.split("|", 1)[1]))
    if problem_id == "unsolvedmath-kou-21.88" and strategy_id == "odd-smallgroups":
        coordinates.sort(key=lambda value: (_semidirect_factor_score(value[0]), value[1]))
    else:
        coordinates.sort()
    metadata = {
        "coverage_kind": coverage_kind,
        "eligible_catalog_groups": len(coordinates),
    }
    if problem_id == "unsolvedmath-kou-21.87":
        metadata["solvable_groups_constructed"] = (
            0 if strategy_id == "smallgroups-targeted" else len(coordinates)
        )
        metadata["first_target_group_id"] = (
            list(coordinates[0]) if coordinates else None
        )
    return tuple(coordinates), tuple(unavailable), metadata


def _gap_targeted_chunk(
    problem_id: str,
    coordinates: tuple[tuple[int, int], ...],
    *,
    max_d: int,
) -> tuple[dict[str, Any] | None, int, int]:
    coordinate_literal = "[" + ",".join(
        f"[{order},{index}]" for order, index in coordinates
    ) + "]"
    if problem_id == "unsolvedmath-kou-21.87":
        predicate = """
els:=Elements(G);
if o=1 then
 minGen:=0;
else
 minGen:=fail;
 upper:=Length(GeneratorsOfGroup(G));
 for r in [1..upper] do
  for tuple in Combinations(els,r) do
   if Size(Subgroup(G,tuple))=o then minGen:=r; break; fi;
  od;
  if minGen<>fail then break; fi;
 od;
fi;
if minGen=fail then Error("exact minimum generator search failed"); fi;
if minGen>2 then
 for d in [1..Minimum(maxD,minGen-2)] do
  indexGcd:=o;
  for r in [1..d] do
   for tuple in Combinations(els,r) do
    H:=Subgroup(G,tuple);
    indexGcd:=Gcd(indexGcd,Index(G,H));
    if indexGcd=1 then break; fi;
   od;
   if indexGcd=1 then break; fi;
  od;
  if indexGcd=1 and minGen>d+1 then
   Print("CAND|",o,"|",idx,"|",d,"|",minGen,"|",indexGcd,"\\n");
   found:=true; break;
  fi;
 od;
fi;
"""
    elif problem_id == "unsolvedmath-kou-21.88":
        predicate = """
classCount:=Length(ConjugacyClasses(G));
if not IsAbelian(G) then
 nonabelian:=nonabelian+1;
 if 17*classCount=o then
  Print("CAND|",o,"|",idx,"|",classCount,"\\n");
  found:=true;
 fi;
fi;
"""
    else:
        raise KeyError(problem_id)
    script = f"""
RunTargetedChunk:=function()
local coordinates,maxD,checked,found,id,o,idx,G,els,minGen,upper,r,tuple,d,
      indexGcd,H,classCount,nonabelian;
coordinates:={coordinate_literal};
maxD:={max_d};
checked:=0; found:=false; nonabelian:=0;
for id in coordinates do
 o:=id[1]; idx:=id[2];
 G:=SmallGroup(o,idx);
 checked:=checked+1;
 {predicate}
 if found then break; fi;
od;
Print("NONABELIAN|",nonabelian,"\\n");
Print("DONE|",checked,"\\n");
end;;
RunTargetedChunk();;
"""
    output = _run_gap(script, timeout=120)
    candidate, checked = _parse_gap_result(output)
    nonabelian = 0
    for line in output.splitlines():
        if line.startswith("NONABELIAN|"):
            nonabelian = int(line.split("|", 1)[1])
    if candidate:
        fields = candidate.pop("fields")
        if problem_id == "unsolvedmath-kou-21.87":
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                d=fields[2],
                minimal_generator_number=fields[3],
                index_gcd=fields[4],
            )
        else:
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                conjugacy_class_count=fields[2],
            )
        candidate["group_id"] = [
            candidate["group_order"],
            candidate["group_index"],
        ]
        candidate["group_catalog"] = "GAP SmallGroups"
    return candidate, checked, nonabelian


def _gap_targeted_scan(
    problem_id: str,
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_order = _positive_int(budget, "max_order", 16)
    max_cases = _positive_int(budget, "max_cases", 1_000)
    max_d = _positive_int(budget, "max_d", 3)
    coordinates, unavailable, catalog_metadata = _targeted_gap_coordinates(
        problem_id,
        max_order,
        strategy_id,
    )
    position = int(state.cursor.get("next_group_position", 0))
    position = max(0, min(position, len(coordinates)))
    chunk_size = _positive_int(budget, "group_chunk_size", 4)
    chunk_size = min(chunk_size, 8)
    metrics = {
        **state.metrics,
        **catalog_metadata,
        "unavailable_orders": list(unavailable),
        "search_order": (
            "nonsolvable_groups_order_then_catalog_index"
            if problem_id == "unsolvedmath-kou-21.87"
            and strategy_id == "smallgroups-targeted"
            else "semidirect_factor_priority_then_catalog_index"
            if problem_id == "unsolvedmath-kou-21.88"
            and strategy_id == "odd-smallgroups"
            else "order_then_catalog_index"
        ),
        "chunks_completed": int(state.metrics.get("chunks_completed", 0)),
        "nonabelian_groups_checked": int(
            state.metrics.get("nonabelian_groups_checked", 0)
        ),
    }
    state.metrics = metrics

    while position < len(coordinates) and state.checked < max_cases:
        remaining = max_cases - state.checked
        chunk = coordinates[position : position + min(chunk_size, remaining)]
        candidate, checked, nonabelian = _gap_targeted_chunk(
            problem_id,
            chunk,
            max_d=max_d,
        )
        if candidate is not None:
            return candidate, state.checked + checked, True
        if checked != len(chunk):
            raise RuntimeError(
                "targeted GAP chunk completed without accounting for every group"
            )
        position += checked
        next_pair = coordinates[position] if position < len(coordinates) else None
        metrics = {
            **metrics,
            "chunks_completed": int(metrics["chunks_completed"]) + 1,
            "nonabelian_groups_checked": int(
                metrics["nonabelian_groups_checked"]
            )
            + nonabelian,
            "last_group_id": list(chunk[-1]),
            "a5_reached": bool(
                metrics.get("a5_reached")
                or (problem_id == "unsolvedmath-kou-21.87" and (60, 5) in chunk)
            ),
        }
        state.commit(
            checked_increment=checked,
            cursor={
                "cursor_kind": "gap_smallgroup",
                "next_group_position": position,
                "next_order": None if next_pair is None else next_pair[0],
                "next_group_index": None if next_pair is None else next_pair[1],
            },
            metrics=metrics,
        )
    exhausted = position >= len(coordinates)
    return None, state.checked, exhausted


def _gap_group_scan(
    problem_id: str,
    budget: Mapping[str, Any],
    *,
    strategy_id: str = "exact-small",
    state: _SearchProgressState | None = None,
) -> tuple[dict[str, Any] | None, int, bool]:
    if problem_id in {"unsolvedmath-kou-21.87", "unsolvedmath-kou-21.88"}:
        if state is None:
            state = _SearchProgressState(
                problem_id=problem_id,
                strategy_id=strategy_id,
                checkpoint=None,
                progress=None,
                resumable=True,
            )
        return _gap_targeted_scan(
            problem_id,
            budget,
            strategy_id=strategy_id,
            state=state,
        )
    max_order = _positive_int(budget, "max_order", 16)
    max_cases = _positive_int(budget, "max_cases", 1_000)
    max_d = _positive_int(budget, "max_d", 3)
    if problem_id == "unsolvedmath-kou-21.87":
        body = """
            els := Elements(G);
            if o = 1 then
              minGen := 0;
            else
              minGen := fail;
              upper := Length(GeneratorsOfGroup(G));
              for r in [1..upper] do
                for tuple in Combinations(els,r) do
                  if Size(Subgroup(G,tuple)) = o then
                    minGen := r; break;
                  fi;
                od;
                if minGen <> fail then break; fi;
              od;
              if minGen = fail then
                Error("exact minimum generator search failed");
              fi;
            fi;
            if minGen > 2 then
              for d in [1..Minimum(maxD,minGen-2)] do
                indexGcd := o;
                for r in [1..d] do
                  for tuple in Combinations(els,r) do
                    H := Subgroup(G,tuple);
                    indexGcd := Gcd(indexGcd,Index(G,H));
                    if indexGcd = 1 then break; fi;
                  od;
                  if indexGcd = 1 then break; fi;
                od;
                if indexGcd = 1 and minGen > d+1 then
                  Print("CAND|",o,"|",idx,"|",d,"|",minGen,"|",
                        indexGcd,"\\n");
                  found := true; break;
                fi;
              od;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.88":
        body = """
            if o mod 2 = 1 and not IsAbelian(G) then
              classCount := Length(ConjugacyClasses(G));
              if 17*classCount = o then
                Print("CAND|",o,"|",idx,"|",classCount,"\\n");
                found := true;
              fi;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.25":
        body = """
            if IsSimpleGroup(G) then
              ps := Filtered(Set(FactorsInt(o)),IsPrimeInt);
              for p in ps do
                P := SylowSubgroup(G,p);
                for q in ps do
                  checked := checked + 1;
                  Q := SylowSubgroup(G,q);
                  ok := false;
                  for g in Elements(G) do
                    K := Q^g;
                    if Size(Group(Concatenation(GeneratorsOfGroup(P),
                                                GeneratorsOfGroup(K)))) = o then
                      ok := true; break;
                    fi;
                  od;
                  if not ok then
                    Print("CAND|",o,"|",idx,"|",p,"|",q,"\\n");
                    found := true; break;
                  fi;
                  if checked >= maxCases then stop := true; break; fi;
                od;
                if found or stop then break; fi;
              od;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.59":
        body = """
            if IsAlmostSimpleGroup(G) or IsQuasisimpleGroup(G) then
              degs := SortedList(List(Irr(G), chi -> chi[1]));
              for j in [1..NumberSmallGroups(o)] do
                if j <> idx then
                  checked := checked + 1;
                  H := SmallGroup(o,j);
                  if degs = SortedList(List(Irr(H), chi -> chi[1])) then
                    Print("CAND|",o,"|",idx,"|",j,"\\n");
                    found := true; break;
                  fi;
                  if checked >= maxCases then stop := true; break; fi;
                fi;
              od;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.137":
        body = """
            fac := Filtered(Set(FactorsInt(o)),IsPrimeInt);
            if Length(fac) = 1 then
              p := fac[1];
              if (p = 2 and Exponent(G) = 8) or
                 (p <> 2 and Exponent(G) = p^2) then
                vals := Set(List(Elements(G), x -> x^p));
                H := Group(vals);
                if Size(H) = Length(vals) and not IsAbelian(H) then
                  Print("CAND|",o,"|",idx,"|",p,"\\n");
                  found := true;
                fi;
              fi;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.35":
        body = """
            vals := Set(List(Cartesian(Elements(G),Elements(G)),
                             pair -> Comm(pair[1],pair[2])));
            for p in Filtered(Set(FactorsInt(o)),IsPrimeInt) do
              premise := true;
              for x in vals do
                if Order(x) mod p <> 0 then
                  for y in vals do
                    if Order(y) mod p = 0 and Order(x*y) mod p <> 0 then
                      premise := false; break;
                    fi;
                  od;
                fi;
                if not premise then break; fi;
              od;
              if premise and not IsPNilpotent(DerivedSubgroup(G),p) then
                Print("CAND|",o,"|",idx,"|",p,"\\n"); found := true; break;
              fi;
            od;
        """
    elif problem_id == "unsolvedmath-kou-21.113":
        body = """
            classes := ConjugacyClasses(G);
            reps := List(classes,Representative);
            for p in Filtered(Set(FactorsInt(o)),IsPrimeInt) do
              psi := [];
              for x in reps do
                if Order(x) mod p = 0 then
                  Add(psi,0);
                else
                  cent := Centralizer(G,x);
                  Add(psi,Length(Filtered(Elements(cent),z ->
                    Order(z)=1 or
                    ForAll(Set(FactorsInt(Order(z))),q -> q=p))));
                fi;
              od;
              mults := List(Irr(G),chi ->
                Sum([1..Length(classes)],i ->
                  Size(classes[i])*psi[i]*ComplexConjugate(chi[i]))/o);
              if ForAny(mults,m -> not IsInt(m) or m < 0) then
                Print("CAND|",o,"|",idx,"|",p,"\\n"); found := true; break;
              fi;
            od;
        """
    elif problem_id == "unsolvedmath-kou-21.134":
        body = """
            if Size(SolvableRadical(G))=1 or IsAlmostSimpleGroup(G) then
              for j in [1..NumberSmallGroups(o)] do
                if j<>idx then
                  checked:=checked+1; H:=SmallGroup(o,j);
                  e:=Lcm(Exponent(G),Exponent(H));
                  divs:=DivisorsInt(e);
                  same:=ForAll(divs,n ->
                    Length(Filtered(Elements(G),x->x^n=One(G))) =
                    Length(Filtered(Elements(H),x->x^n=One(H))));
                  if same and
                    ((Size(SolvableRadical(G))=1 and Size(SolvableRadical(H))<>1)
                     or (IsAlmostSimpleGroup(G) and IdGroup(G)<>IdGroup(H))) then
                    Print("CAND|",o,"|",idx,"|",j,"\\n");
                    found:=true; break;
                  fi;
                  if checked>=maxCases then stop:=true; break; fi;
                fi;
              od;
            fi;
        """
    elif problem_id == "unsolvedmath-kou-21.135":
        body = """
            if Size(SolvableRadical(G))=1 then
              degs:=SortedList(List(Irr(G),chi->chi[1]));
              for j in [1..NumberSmallGroups(o)] do
                if j<>idx then
                  checked:=checked+1; H:=SmallGroup(o,j);
                  if Size(SolvableRadical(H))<>1 and
                     degs=SortedList(List(Irr(H),chi->chi[1])) then
                    Print("CAND|",o,"|",idx,"|",j,"\\n");
                    found:=true; break;
                  fi;
                  if checked>=maxCases then stop:=true; break; fi;
                fi;
              od;
            fi;
        """
    else:
        raise KeyError(problem_id)

    script = f"""
RunSearch := function()
local maxOrder,maxCases,maxD,checked,found,stop,o,idx,G,n,sols,ps,p,cp,q,cq,
      ok,H,K,P,Q,g,fac,vals,premise,x,y,classes,reps,psi,cent,z,mults,chi,j,
      degs,e,divs,same,els,upper,minGen,r,tuple,d,indexGcd,classCount;
maxOrder := {max_order};
maxCases := {max_cases};
maxD := {max_d};
checked := 0; found := false; stop := false;
for o in [1..maxOrder] do
  if SmallGroupsAvailable(o) then
    for idx in [1..NumberSmallGroups(o)] do
      checked := checked + 1;
      G := SmallGroup(o,idx);
      {body}
      if found or stop or checked >= maxCases then stop := true; break; fi;
    od;
  fi;
  if found or stop then break; fi;
od;
Print("DONE|",checked,"\\n");
end;;
RunSearch();;
"""
    candidate, checked = _parse_gap_result(_run_gap(script))
    if candidate:
        fields = candidate.pop("fields")
        if problem_id == "unsolvedmath-kou-21.87":
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                d=fields[2],
                minimal_generator_number=fields[3],
                index_gcd=fields[4],
            )
        elif problem_id == "unsolvedmath-kou-21.88":
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                conjugacy_class_count=fields[2],
            )
        elif problem_id == "unsolvedmath-kou-21.25":
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                prime_p=fields[2],
                prime_q=fields[3],
            )
        elif problem_id == "unsolvedmath-kou-21.59":
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                comparison_group_index=fields[2],
            )
        elif problem_id in {"unsolvedmath-kou-21.134", "unsolvedmath-kou-21.135"}:
            candidate.update(
                group_order=fields[0],
                group_index=fields[1],
                comparison_group_index=fields[2],
            )
        else:
            candidate.update(group_order=fields[0], group_index=fields[1], prime=fields[2])
        candidate["group_id"] = [candidate["group_order"], candidate["group_index"]]
        candidate["group_catalog"] = "GAP SmallGroups"
    exhausted = candidate is None and checked < max_cases
    return candidate, checked, exhausted


def _gap_verify_candidate(problem_id: str, candidate: Mapping[str, Any]) -> bool:
    o = int(candidate["group_order"])
    idx = int(candidate["group_index"])
    if problem_id in {"unsolvedmath-kou-21.87", "unsolvedmath-kou-21.88"}:
        if list(candidate.get("group_id", ())) != [o, idx]:
            return False
        if candidate.get("group_catalog") != "GAP SmallGroups":
            return False
    if problem_id == "unsolvedmath-kou-21.87":
        d = int(candidate["d"])
        reported_minimum = int(candidate["minimal_generator_number"])
        reported_gcd = int(candidate["index_gcd"])
        predicate = f"""
MinimumGeneratorNumber:=function(group)
 local elements,upper,r,tuple;
 if Size(group)=1 then return 0; fi;
 elements:=Elements(group);
 upper:=Length(GeneratorsOfGroup(group));
 for r in [1..upper] do
  for tuple in Combinations(elements,r) do
   if Size(Subgroup(group,tuple))=Size(group) then return r; fi;
  od;
 od;
 return fail;
end;;
IndexGcdForD:=function(group,dValue)
 local result,elements,r,tuple,H;
 result:=Size(group);
 elements:=Elements(group);
 for r in [1..dValue] do
  for tuple in Combinations(elements,r) do
   H:=Subgroup(group,tuple);
   result:=Gcd(result,Index(group,H));
   if result=1 then return result; fi;
  od;
 od;
 return result;
end;;
d:={d};;
minGen:=MinimumGeneratorNumber(G);;
indexGcd:=IndexGcdForD(G,d);;
ok:=minGen<>fail and d>=1 and minGen>d+1 and indexGcd=1
 and minGen={reported_minimum} and indexGcd={reported_gcd};;
"""
    elif problem_id == "unsolvedmath-kou-21.88":
        reported_classes = int(candidate["conjugacy_class_count"])
        predicate = f"""
classCount:=Length(ConjugacyClasses(G));;
ok:={o} mod 2=1 and not IsAbelian(G) and 17*classCount={o}
 and classCount={reported_classes};;
"""
    elif problem_id == "unsolvedmath-kou-21.25":
        p = int(candidate["prime_p"])
        q = int(candidate["prime_q"])
        predicate = f"""
ok:=IsSimpleGroup(G);;
if ok then
 cp:=AsList(ConjugacyClassSubgroups(G,SylowSubgroup(G,{p})));;
 cq:=AsList(ConjugacyClassSubgroups(G,SylowSubgroup(G,{q})));;
 for H in cp do for K in cq do
  if Size(Group(Concatenation(GeneratorsOfGroup(H),GeneratorsOfGroup(K))))={o}
  then ok:=false; break; fi;
 od; if not ok then break; fi; od;
fi;
"""
    elif problem_id == "unsolvedmath-kou-21.59":
        j = int(candidate["comparison_group_index"])
        predicate = f"""
H:=SmallGroup({o},{j});;
ok:=(IsAlmostSimpleGroup(G) or IsQuasisimpleGroup(G))
 and IdGroup(G)<>IdGroup(H)
 and SortedList(List(Irr(G),chi->chi[1]))
     =SortedList(List(Irr(H),chi->chi[1]));;
"""
    elif problem_id == "unsolvedmath-kou-21.137":
        p = int(candidate["prime"])
        predicate = f"""
p:={p};; vals:=Set(List(Elements(G),x->x^p));; H:=Group(vals);;
ok:=((p=2 and Exponent(G)=8) or (p<>2 and Exponent(G)=p^2))
 and Size(H)=Length(vals) and not IsAbelian(H);;
"""
    elif problem_id == "unsolvedmath-kou-21.35":
        p = int(candidate["prime"])
        predicate = f"""
p:={p};; vals:=Set(List(Cartesian(Elements(G),Elements(G)),
 pair->Comm(pair[1],pair[2])));; premise:=true;;
for x in vals do if Order(x) mod p<>0 then for y in vals do
 if Order(y) mod p=0 and Order(x*y) mod p<>0 then premise:=false; break; fi;
od; fi; if not premise then break; fi; od;
ok:=premise and not IsPNilpotent(DerivedSubgroup(G),p);;
"""
    elif problem_id == "unsolvedmath-kou-21.113":
        p = int(candidate["prime"])
        predicate = f"""
p:={p};; classes:=ConjugacyClasses(G);; reps:=List(classes,Representative);;
PVal:=function(x)
 if Order(x) mod p=0 then return 0; fi;
 return Length(Filtered(Elements(Centralizer(G,x)),z->
  Order(z)=1 or ForAll(Set(FactorsInt(Order(z))),q->q=p)));
end;;
psi:=List(reps,PVal);;
mults:=List(Irr(G),chi->Sum([1..Length(classes)],i->
 Size(classes[i])*psi[i]*ComplexConjugate(chi[i]))/{o});;
ok:=ForAny(mults,m->not IsInt(m) or m<0);;
"""
    elif problem_id == "unsolvedmath-kou-21.134":
        j = int(candidate["comparison_group_index"])
        predicate = f"""
H:=SmallGroup({o},{j});; e:=Lcm(Exponent(G),Exponent(H));;
same:=ForAll(DivisorsInt(e),n->
 Length(Filtered(Elements(G),x->x^n=One(G)))=
 Length(Filtered(Elements(H),x->x^n=One(H))));;
ok:=same and ((Size(SolvableRadical(G))=1 and Size(SolvableRadical(H))<>1)
 or (IsAlmostSimpleGroup(G) and IdGroup(G)<>IdGroup(H)));;
"""
    elif problem_id == "unsolvedmath-kou-21.135":
        j = int(candidate["comparison_group_index"])
        predicate = f"""
H:=SmallGroup({o},{j});;
ok:=Size(SolvableRadical(G))=1 and Size(SolvableRadical(H))<>1
 and SortedList(List(Irr(G),chi->chi[1]))
 =SortedList(List(Irr(H),chi->chi[1]));;
"""
    else:
        return False
    output = _run_gap(
        f"""
VerifyCandidate := function()
local G,n,sols,ok,cp,cq,H,K,p,vals,premise,x,y,classes,reps,PVal,
      psi,mults,j,e,same,degs,MinimumGeneratorNumber,IndexGcdForD,d,minGen,
      indexGcd,classCount;
G:=SmallGroup({o},{idx});
{predicate}
Print("VERIFY|",ok,"\\n");
end;;
VerifyCandidate();;
"""
    )
    return "VERIFY|true" in output


@lru_cache(maxsize=32)
def _gap_order_profiles(max_order: int, max_cases: int) -> tuple[tuple[Any, ...], ...]:
    script = f"""
checked:=0;; stop:=false;;
for o in [1..{max_order}] do
 if SmallGroupsAvailable(o) then
  for idx in [1..NumberSmallGroups(o)] do
   G:=SmallGroup(o,idx);; checked:=checked+1;;
   Print("PROFILE|",o,"|",idx,"|",IsSimpleGroup(G),"|");
   Print(JoinStringsWithSeparator(List(Elements(G),x->String(Order(x))),","));
   Print("\\n");
   if checked>={max_cases} then stop:=true; break; fi;
  od;
 fi;
 if stop then break; fi;
od;
Print("DONE|",checked,"\\n");
"""
    rows: list[tuple[Any, ...]] = []
    for line in _run_gap(script).splitlines():
        if not line.startswith("PROFILE|"):
            continue
        _, order, index, simple, orders = line.split("|", 4)
        rows.append(
            (
                int(order),
                int(index),
                simple == "true",
                tuple(int(value) for value in orders.split(",") if value),
            )
        )
    return tuple(rows)


def _divisibility_matching(
    left_orders: tuple[int, ...],
    right_orders: tuple[int, ...],
) -> list[int] | None:
    adjacency = [
        [right for right, value in enumerate(right_orders) if value % target == 0]
        for target in left_orders
    ]
    matched_left = [-1] * len(right_orders)

    def augment(left: int, seen: set[int]) -> bool:
        for right in adjacency[left]:
            if right in seen:
                continue
            seen.add(right)
            if matched_left[right] < 0 or augment(matched_left[right], seen):
                matched_left[right] = left
                return True
        return False

    if not all(augment(left, set()) for left in range(len(left_orders))):
        return None
    assignment = [-1] * len(left_orders)
    for right, left in enumerate(matched_left):
        if left >= 0:
            assignment[left] = right
    return assignment


def _search_kou_21_2(
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_order = _positive_int(budget, "max_order", 16)
    max_cases = _positive_int(budget, "max_cases", 200)
    profiles = _gap_order_profiles(max_order, max_cases)
    checked = 0
    by_order: dict[int, list[tuple[Any, ...]]] = {}
    for profile in profiles:
        by_order.setdefault(int(profile[0]), []).append(profile)
    for order in sorted(by_order):
        simple = [profile for profile in by_order[order] if profile[2]]
        nonsimple = [profile for profile in by_order[order] if not profile[2]]
        for s_profile in simple:
            for g_profile in nonsimple:
                checked += 1
                matching = _divisibility_matching(g_profile[3], s_profile[3])
                if matching is not None:
                    return (
                        {
                            "group_order": order,
                            "group_index": g_profile[1],
                            "simple_group_index": s_profile[1],
                            "bijection_image_positions": matching,
                            "group_catalog": "GAP SmallGroups",
                        },
                        checked,
                        True,
                    )
    return None, checked, len(profiles) < max_cases


def _verify_kou_21_2(candidate: Mapping[str, Any]) -> bool:
    order = int(candidate["group_order"])
    max_index = max(int(candidate["group_index"]), int(candidate["simple_group_index"]))
    profiles = _gap_order_profiles(order, 1_000_000)
    lookup = {(row[0], row[1]): row for row in profiles}
    g = lookup.get((order, int(candidate["group_index"])))
    s = lookup.get((order, int(candidate["simple_group_index"])))
    if g is None or s is None or g[2] or not s[2]:
        return False
    return _divisibility_matching(g[3], s[3]) is not None


def _has_distinct_adjacent_sum_cycle(modulus: int, subset: tuple[int, ...]) -> bool:
    first = subset[0]
    for tail in itertools.permutations(subset[1:]):
        ordering = (first,) + tail
        sums = {
            (ordering[index] + ordering[(index + 1) % len(ordering)]) % modulus
            for index in range(len(ordering))
        }
        if len(sums) == len(ordering):
            return True
    return False


def _search_kou_21_130(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_order = _positive_int(budget, "max_order", 9, minimum=3)
    max_subset = _positive_int(budget, "max_subset", 6, minimum=3)
    max_cases = _positive_int(budget, "max_cases", 2_000)
    rng = random.Random(seed)
    checked = 0
    for modulus in range(3, max_order + 1, 2):
        subsets = [
            subset
            for size in range(3, min(max_subset, modulus) + 1)
            for subset in itertools.combinations(range(modulus), size)
        ]
        if strategy_id == "multistart":
            rng.shuffle(subsets)
        for subset in subsets:
            checked += 1
            if not _has_distinct_adjacent_sum_cycle(modulus, subset):
                return (
                    {"cyclic_modulus": modulus, "subset": list(subset)},
                    checked,
                    True,
                )
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _integer_cuberoot(value: int) -> int:
    low, high = 0, max(1, value)
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**3 <= value:
            low = middle
        else:
            high = middle
    return high if high**3 <= value else low


def _prime_sieve(limit: int) -> tuple[bytearray, array]:
    limit = max(1, int(limit))
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            count = ((limit - start) // prime) + 1
            sieve[start : limit + 1 : prime] = b"\x00" * count
    primes = array(
        "I",
        (index for index, value in enumerate(sieve) if value),
    )
    return sieve, primes


def _segmented_primes(
    start: int,
    stop: int,
    *,
    segment_size: int = 65_536,
):
    if stop < max(2, start):
        return
    _, base_primes = _prime_sieve(math.isqrt(stop))
    low = max(2, int(start))
    size = max(1_024, int(segment_size))
    while low <= stop:
        high = min(stop, low + size - 1)
        flags = bytearray(b"\x01") * (high - low + 1)
        for prime in base_primes:
            first = max(
                int(prime) * int(prime),
                ((low + int(prime) - 1) // int(prime)) * int(prime),
            )
            if first > high:
                continue
            flags[first - low : high - low + 1 : int(prime)] = (
                b"\x00"
                * (((high - first) // int(prime)) + 1)
            )
        for offset, flag in enumerate(flags):
            if flag:
                yield low + offset
        low = high + 1


def _factor_certificate(value: int) -> dict[str, int]:
    return {str(prime): int(exponent) for prime, exponent in factorint(value).items()}


def _is_primitive_root_3(prime: int) -> bool:
    return all(
        pow(3, (prime - 1) // divisor, prime) != 1
        for divisor in factorint(prime - 1)
    )


def _search_primitive_root(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_q = _positive_int(budget, "max_q", 1_000, minimum=5)
    max_cases = _positive_int(budget, "max_cases", 500)
    if strategy_id != "exact-small":
        segment_size = _positive_int(
            budget,
            "segment_size",
            65_536,
            minimum=1_024,
        )
        block_size = _positive_int(
            budget,
            "prime_block_size",
            64,
        )
        next_q = max(5, int(state.cursor.get("next_q", 5)))
        metrics = {
            **state.metrics,
            "coverage_kind": "segmented_prime_q_stream",
            "segments_completed": int(
                state.metrics.get("segments_completed", 0)
            ),
            "min_tested_q": state.metrics.get("min_tested_q"),
            "max_tested_q": state.metrics.get("max_tested_q"),
        }
        while next_q <= max_q and state.checked < max_cases:
            segment_high = min(max_q, next_q + segment_size - 1)
            tested: list[int] = []
            resume_q = segment_high + 1
            for q in _segmented_primes(
                next_q,
                segment_high,
                segment_size=segment_size,
            ):
                if state.checked + len(tested) >= max_cases:
                    resume_q = q
                    break
                tested.append(q)
                p = 16 * q**4 + 1
                if isprime(p) and not _is_primitive_root_3(p):
                    return (
                        {
                            "q": q,
                            "p": p,
                            "order_of_3": int(sympy.n_order(3, p)),
                            "p_minus_1_factorization": _factor_certificate(
                                p - 1
                            ),
                        },
                        state.checked + len(tested),
                        True,
                    )
                if len(tested) >= block_size:
                    resume_q = q + 1
                    break
            if not tested:
                next_q = resume_q
                if next_q > segment_high:
                    metrics["segments_completed"] = (
                        int(metrics["segments_completed"]) + 1
                    )
                state.commit(
                    cursor={
                        "cursor_kind": "primitive_root_prime_segment",
                        "next_q": next_q,
                    },
                    metrics=metrics,
                )
                continue
            metrics = {
                **metrics,
                "segments_completed": (
                    int(metrics["segments_completed"])
                    + int(resume_q > segment_high)
                ),
                "min_tested_q": (
                    tested[0]
                    if metrics.get("min_tested_q") is None
                    else min(int(metrics["min_tested_q"]), tested[0])
                ),
                "max_tested_q": (
                    tested[-1]
                    if metrics.get("max_tested_q") is None
                    else max(int(metrics["max_tested_q"]), tested[-1])
                ),
            }
            state.commit(
                checked_increment=len(tested),
                cursor={
                    "cursor_kind": "primitive_root_prime_segment",
                    "next_q": resume_q,
                },
                metrics=metrics,
            )
            next_q = resume_q
        return None, state.checked, next_q > max_q

    checked = 0
    for q in range(5, max_q + 1):
        if not isprime(q):
            continue
        checked += 1
        p = 16 * q**4 + 1
        if isprime(p) and not _is_primitive_root_3(p):
            order = sympy.n_order(3, p)
            return (
                {
                    "q": q,
                    "p": p,
                    "order_of_3": int(order),
                    "p_minus_1_factorization": _factor_certificate(p - 1),
                },
                checked,
                True,
            )
        if checked >= max_cases:
            return None, checked, False
    return None, checked, True


def _alexa_test(value: int) -> bool:
    count = _integer_cuberoot(value) // 2
    residue_sum = sum(pow(2 * index + 1, value - 1, value) for index in range(1, count + 1))
    return residue_sum == count


def _search_predicate_mismatch(
    budget: Mapping[str, Any],
    *,
    minimum: int,
    predicate: Callable[[int], bool],
    certificate: Callable[[int], dict[str, Any]],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_n = _positive_int(budget, "max_n", 500, minimum=minimum)
    max_cases = _positive_int(budget, "max_cases", max_n)
    checked = 0
    for value in range(minimum, max_n + 1):
        checked += 1
        if bool(isprime(value)) != bool(predicate(value)):
            payload = certificate(value)
            payload.update(n=value, is_prime=bool(isprime(value)))
            if not isprime(value):
                payload["factorization"] = _factor_certificate(value)
            return payload, checked, True
        if checked >= max_cases:
            return None, checked, False
    return None, checked, True


def _giuga_test(value: int) -> bool:
    return sum(pow(index, value - 1, value) for index in range(1, value)) % value == value - 1


def _partition_number(partitions: list[int], value: int) -> int:
    total = 0
    index = 1
    while True:
        lower = index * (3 * index - 1) // 2
        if lower > value:
            return total
        sign = 1 if index % 2 else -1
        total += sign * partitions[value - lower]
        upper = index * (3 * index + 1) // 2
        if upper <= value:
            total += sign * partitions[value - upper]
        index += 1


def _factorial_mod(n: int, modulus: int) -> int:
    residue = 1 % modulus
    for factor in range(2, n + 1):
        residue = (residue * factor) % modulus
        if residue == 0:
            break
    return residue


def _partition_divides_factorial_by_valuations(n: int, partition: int) -> bool:
    """Replay a positive divisibility claim without the modular-product routine."""

    factors = factorint(partition)
    if math.prod(int(prime) ** int(exponent) for prime, exponent in factors.items()) != partition:
        return False
    for prime, required in factors.items():
        available = 0
        quotient = n
        while quotient:
            quotient //= int(prime)
            available += quotient
        if available < int(required):
            return False
    return True


def _search_partition_divisor(
    budget: Mapping[str, Any],
    *,
    state: _SearchProgressState | None = None,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_n = _positive_int(budget, "max_n", 500)
    max_cases = _positive_int(budget, "max_cases", max(1, max_n - 39))
    if max_n <= 39:
        return None, 0, True
    if state is None:
        state = _SearchProgressState(
            problem_id="unsolvedmath-kou-21.89",
            strategy_id="exact-small",
            checkpoint=None,
            progress=None,
            resumable=True,
        )

    next_n = max(40, int(state.cursor.get("next_n", 40)))
    if next_n > max_n:
        return None, state.checked, True
    if state.checked >= max_cases:
        return None, state.checked, False
    replay_started = time.monotonic()
    partitions = [1]
    for value in range(1, next_n):
        partitions.append(_partition_number(partitions, value))
    replay_seconds = time.monotonic() - replay_started
    metrics = {
        **state.metrics,
        "partition_method": "generalized_pentagonal_recurrence",
        "divisibility_method": "iterated_modular_product",
        "replayed_partition_terms": int(
            state.metrics.get("replayed_partition_terms", 0)
        )
        + max(0, next_n - 1),
        "replay_seconds": round(
            float(state.metrics.get("replay_seconds", 0.0)) + replay_seconds,
            6,
        ),
        "blocks_completed": int(state.metrics.get("blocks_completed", 0)),
    }
    state.commit(
        cursor={
            "cursor_kind": "partition_n_block",
            "next_n": next_n,
        },
        metrics=metrics,
    )

    block_size = min(_positive_int(budget, "n_block_size", 16), 64)
    while next_n <= max_n and state.checked < max_cases:
        remaining = max_cases - state.checked
        block_end = min(max_n, next_n + min(block_size, remaining) - 1)
        tested: list[int] = []
        for n in range(next_n, block_end + 1):
            partitions.append(_partition_number(partitions, n))
            partition = partitions[n]
            residue = _factorial_mod(n, partition)
            tested.append(n)
            if residue == 0:
                return (
                    {
                        "n": n,
                        "partition_number": partition,
                        "factorial_mod_partition": residue,
                        "partition_method": "generalized_pentagonal_recurrence",
                        "divisibility_method": "iterated_modular_product",
                        "internal_replay_method": "prime_valuations_in_factorial",
                    },
                    state.checked + len(tested),
                    True,
                )
        next_n = block_end + 1
        metrics = {
            **metrics,
            "blocks_completed": int(metrics["blocks_completed"]) + 1,
            "min_tested_n": min(
                int(metrics.get("min_tested_n", tested[0])),
                tested[0],
            ),
            "max_tested_n": max(
                int(metrics.get("max_tested_n", tested[-1])),
                tested[-1],
            ),
        }
        state.commit(
            checked_increment=len(tested),
            cursor={
                "cursor_kind": "partition_n_block",
                "next_n": next_n,
            },
            metrics=metrics,
        )
    return None, state.checked, next_n > max_n


def _search_fermat_square_factor(
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_index = _positive_int(budget, "max_index", 6, minimum=0)
    max_factor = _positive_int(budget, "max_factor", 1_000, minimum=3)
    max_cases = _positive_int(budget, "max_cases", 10_000)
    _, primes = _prime_sieve(max_factor)
    checked = 0
    for index in range(max_index + 1):
        exponent = 1 << index
        for divisor in primes:
            if divisor == 2:
                continue
            checked += 1
            if (pow(2, exponent, divisor * divisor) + 1) % (divisor * divisor) == 0:
                return {"index": index, "square_divisor": divisor}, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _search_mersenne_square_factor(
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_exponent = _positive_int(budget, "max_exponent", 100, minimum=2)
    max_factor = _positive_int(budget, "max_factor", 1_000, minimum=3)
    max_cases = _positive_int(budget, "max_cases", 10_000)
    _, exponents = _prime_sieve(max_exponent)
    _, divisors = _prime_sieve(max_factor)
    checked = 0
    for exponent in exponents:
        for divisor in divisors:
            if divisor == 2 or (divisor - 1) % (2 * exponent):
                continue
            checked += 1
            if pow(2, exponent, divisor * divisor) == 1:
                return {"prime_exponent": exponent, "square_divisor": divisor}, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _fib_pair_mod(index: int, modulus: int) -> tuple[int, int]:
    if index == 0:
        return 0, 1
    left, right = _fib_pair_mod(index // 2, modulus)
    c = left * ((2 * right - left) % modulus) % modulus
    d = (left * left + right * right) % modulus
    return (d, (c + d) % modulus) if index % 2 else (c, d)


def _search_wall_sun_sun(
    budget: Mapping[str, Any],
    *,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_prime = _positive_int(budget, "max_prime", 1_000, minimum=7)
    start_prime = _positive_int(budget, "start_prime", 7, minimum=7)
    max_cases = _positive_int(budget, "max_cases", 500)
    block_size = min(
        _positive_int(budget, "checkpoint_block_size", 128),
        4_096,
    )
    next_candidate = max(
        start_prime,
        int(state.cursor.get("next_prime_candidate", start_prime)),
    )
    if next_candidate <= 7:
        prime = 7
    else:
        prime = int(nextprime(next_candidate - 1))
    metrics = {
        **state.metrics,
        "coverage_kind": (
            "post_frontier_streamed_primes"
            if budget.get("known_computational_lower_bound") is not None
            else "published_range_replication"
        ),
        "known_computational_lower_bound": budget.get(
            "known_computational_lower_bound"
        ),
        "blocks_completed": int(state.metrics.get("blocks_completed", 0)),
        "min_tested_prime": state.metrics.get("min_tested_prime"),
        "max_tested_prime": state.metrics.get("max_tested_prime"),
    }
    while state.checked < max_cases and prime <= max_prime:
        tested: list[int] = []
        while (
            len(tested) < min(block_size, max_cases - state.checked)
            and prime <= max_prime
        ):
            tested.append(prime)
            next_value = int(nextprime(prime))
            legendre = int(sympy.legendre_symbol(prime, 5))
            index = prime - legendre
            residue = _fib_pair_mod(index, prime * prime)[0]
            if residue == 0:
                return (
                    {
                        "prime": prime,
                        "fibonacci_index": index,
                        "residue_mod_p2": residue,
                    },
                    state.checked + len(tested),
                    True,
                )
            prime = next_value
        if not tested:
            break
        metrics = {
            **metrics,
            "blocks_completed": int(metrics["blocks_completed"]) + 1,
            "min_tested_prime": (
                tested[0]
                if metrics.get("min_tested_prime") is None
                else min(int(metrics["min_tested_prime"]), tested[0])
            ),
            "max_tested_prime": (
                tested[-1]
                if metrics.get("max_tested_prime") is None
                else max(int(metrics["max_tested_prime"]), tested[-1])
            ),
        }
        state.commit(
            checked_increment=len(tested),
            cursor={
                "cursor_kind": "wall_sun_sun_prime_stream",
                "next_prime_candidate": prime,
            },
            metrics=metrics,
        )
    return None, state.checked, prime > max_prime


def _unrank_combination_lex(
    population_size: int,
    selection_size: int,
    rank: int,
) -> tuple[int, ...]:
    total = math.comb(population_size, selection_size)
    if rank < 0 or rank >= total:
        raise IndexError("combination rank is outside the finite family")
    result: list[int] = []
    lower = 0
    remaining_rank = int(rank)
    for position in range(selection_size):
        remaining = selection_size - position - 1
        for value in range(
            lower,
            population_size - remaining,
        ):
            block = math.comb(
                population_size - value - 1,
                remaining,
            )
            if remaining_rank < block:
                result.append(value)
                lower = value + 1
                break
            remaining_rank -= block
    return tuple(result)


@lru_cache(maxsize=1)
def _lehmer_korselt_families() -> tuple[dict[str, Any], ...]:
    exponent_shapes = (
        (6, 4, 2),
        (7, 4, 2),
        (6, 5, 2),
        (6, 4, 3),
        (8, 3, 2),
        (7, 3, 3),
    )
    families = []
    for powers in exponent_shapes:
        modulus = 2 ** powers[0] * 3 ** powers[1] * 11 ** powers[2]
        pool = tuple(
            sorted(
                divisor + 1
                for divisor in map(int, sympy.divisors(modulus))
                if isprime(divisor + 1)
                and math.gcd(divisor + 1, modulus) == 1
            )
        )
        core = pool[:10]
        choices = pool[10:]
        if len(choices) < 6:
            raise RuntimeError("Korselt family has too few variable primes")
        families.append(
            {
                "modulus": modulus,
                "exponent_shape": list(powers),
                "pool": pool,
                "core": core,
                "choices": choices,
                "variable_factor_count": 6,
                "combination_count": math.comb(len(choices), 6),
            }
        )
    return tuple(families)


def _search_lehmer(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    if strategy_id != "exact-small":
        minimum_n = _positive_int(
            budget,
            "minimum_n",
            1_000_000_000_000_000_000_000_000_000_001,
        )
        minimum_factors = _positive_int(
            budget,
            "minimum_prime_factors",
            15,
            minimum=15,
        )
        max_cases = _positive_int(budget, "max_cases", 10_000_000)
        block_size = _positive_int(
            budget,
            "subset_block_size",
            256,
        )
        families = _lehmer_korselt_families()
        pending = 0
        checked = state.checked
        subsets_enumerated = int(
            state.metrics.get("subsets_enumerated", checked)
        )
        korselt_candidates = int(
            state.metrics.get("korselt_candidates", 0)
        )
        post_frontier = int(
            state.metrics.get("post_frontier_candidates", 0)
        )
        quotient_feasible = int(
            state.metrics.get("quotient_feasible_candidates", 0)
        )
        lehmer_tested = int(state.metrics.get("lehmer_tested", 0))
        family_moduli = {
            int(value)
            for value in state.metrics.get("family_moduli", [])
        }
        min_tested = state.metrics.get("min_tested_n")
        max_tested = state.metrics.get("max_tested_n")
        while checked < max_cases:
            case_index = checked
            family_index = (
                case_index + abs(int(seed))
            ) % len(families)
            combination_rank = case_index // len(families)
            family = families[family_index]
            if combination_rank >= int(family["combination_count"]):
                return None, state.checked, True
            indices = _unrank_combination_lex(
                len(family["choices"]),
                int(family["variable_factor_count"]),
                combination_rank,
            )
            ordered = tuple(
                sorted(
                    (
                        *family["core"],
                        *(
                            family["choices"][index]
                            for index in indices
                        ),
                    )
                )
            )
            value = math.prod(ordered)
            phi = math.prod(prime - 1 for prime in ordered)
            checked += 1
            pending += 1
            subsets_enumerated += 1
            family_moduli.add(int(family["modulus"]))
            is_korselt = all(
                (value - 1) % (prime - 1) == 0
                for prime in ordered
            )
            if is_korselt:
                korselt_candidates += 1
            beyond_frontier = (
                is_korselt
                and value >= minimum_n
                and len(ordered) >= minimum_factors
            )
            if beyond_frontier:
                post_frontier += 1
                min_tested = (
                    value
                    if min_tested is None
                    else min(int(min_tested), value)
                )
                max_tested = (
                    value
                    if max_tested is None
                    else max(int(max_tested), value)
                )
            feasible = beyond_frontier and value > 2 * phi
            if feasible:
                quotient_feasible += 1
                lehmer_tested += 1
            if feasible and (value - 1) % phi == 0:
                return {
                    "n": value,
                    "phi": phi,
                    "factorization": {str(prime): 1 for prime in ordered},
                }, checked, False
            metrics = {
                "coverage_kind": (
                    "post_frontier_korselt_compatible_subsets"
                ),
                "minimum_n": minimum_n,
                "minimum_prime_factors": minimum_factors,
                "factor_counts": [len(ordered)],
                "family_moduli": sorted(family_moduli),
                "subsets_enumerated": subsets_enumerated,
                "korselt_candidates": korselt_candidates,
                "post_frontier_candidates": post_frontier,
                "quotient_feasible_candidates": quotient_feasible,
                "lehmer_tested": lehmer_tested,
                "min_tested_n": min_tested,
                "max_tested_n": max_tested,
                "all_tested_structures_squarefree": True,
                "korselt_filter_exact": True,
            }
            if pending >= block_size:
                state.commit(
                    checked_increment=pending,
                    cursor={
                        "cursor_kind": "lehmer_korselt_subset",
                        "next_case": checked,
                    },
                    metrics=metrics,
                )
                pending = 0
        if pending:
            state.commit(
                checked_increment=pending,
                cursor={
                    "cursor_kind": "lehmer_korselt_subset",
                    "next_case": checked,
                },
                metrics=metrics,
            )
        return None, state.checked, False

    max_n = _positive_int(budget, "max_n", 1_000, minimum=2)
    max_cases = _positive_int(budget, "max_cases", max_n)
    checked = 0
    for value in range(4, max_n + 1):
        if isprime(value):
            continue
        checked += 1
        phi = int(totient(value))
        if (value - 1) % phi == 0:
            return {
                "n": value,
                "phi": phi,
                "factorization": _factor_certificate(value),
            }, checked, True
        if checked >= max_cases:
            return None, checked, False
    return None, checked, True


def _prime_field_rank(
    vectors: tuple[tuple[int, ...], ...],
    field_prime: int,
) -> int:
    if not vectors:
        return 0
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise ValueError("prime-field vectors must have equal dimension")
    matrix = [
        [int(value) % field_prime for value in vector]
        for vector in vectors
    ]
    row = 0
    for column in range(width):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(matrix))
                if matrix[candidate][column] % field_prime
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], -1, field_prime)
        matrix[row] = [
            (value * inverse) % field_prime for value in matrix[row]
        ]
        for other in range(len(matrix)):
            if other == row:
                continue
            factor = matrix[other][column] % field_prime
            if factor:
                matrix[other] = [
                    (left - factor * right) % field_prime
                    for left, right in zip(matrix[other], matrix[row])
                ]
        row += 1
        if row == len(matrix):
            break
    return row


@lru_cache(maxsize=8)
def _prime_field_bases(
    rank: int,
    field_prime: int,
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    vectors = tuple(
        vector
        for vector in itertools.product(range(field_prime), repeat=rank)
        if any(vector)
    )
    return tuple(
        tuple(sorted(base))
        for base in itertools.combinations(vectors, rank)
        if _prime_field_rank(tuple(base), field_prime) == rank
    )


def _rota_row_permutations(
    allowed_by_column: tuple[tuple[int, ...], ...],
):
    rank = len(allowed_by_column)
    assignment = [-1] * rank
    unused_columns = set(range(rank))

    def generate():
        if not unused_columns:
            yield tuple(assignment)
            return
        column = min(
            unused_columns,
            key=lambda value: sum(
                vector_index not in assignment
                for vector_index in allowed_by_column[value]
            ),
        )
        unused_columns.remove(column)
        for vector_index in allowed_by_column[column]:
            if vector_index in assignment:
                continue
            assignment[column] = vector_index
            yield from generate()
            assignment[column] = -1
        unused_columns.add(column)

    yield from generate()


def _rota_transversal_decomposition(
    bases: tuple[tuple[tuple[int, ...], ...], ...],
    field_prime: int,
    *,
    node_limit: int | None,
) -> tuple[bool | None, int, tuple[tuple[int, ...], ...] | None]:
    rank = len(bases)
    if (
        rank < 1
        or any(len(base) != rank for base in bases)
        or any(
            _prime_field_rank(base, field_prime) != rank
            for base in bases
        )
    ):
        return False, 0, None
    columns: list[list[tuple[int, ...]]] = [
        [bases[0][column]] for column in range(rank)
    ]
    arrangements: list[tuple[int, ...]] = [tuple(range(rank))]
    nodes = 0
    aborted = False

    def assign_row(row_index: int) -> bool:
        nonlocal nodes, aborted
        if row_index == rank:
            return True
        base = bases[row_index]
        feasible = {
            column: tuple(
                vector_index
                for vector_index, vector in enumerate(base)
                if _prime_field_rank(
                    tuple((*columns[column], vector)),
                    field_prime,
                )
                == len(columns[column]) + 1
            )
            for column in range(rank)
        }
        if any(not choices for choices in feasible.values()):
            return False
        for assignment in _rota_row_permutations(
            tuple(feasible[column] for column in range(rank))
        ):
            nodes += 1
            if node_limit is not None and nodes > node_limit:
                aborted = True
                return False
            for column, vector_index in enumerate(assignment):
                columns[column].append(base[vector_index])
            arrangements.append(assignment)
            solved = assign_row(row_index + 1)
            if solved:
                return True
            arrangements.pop()
            for column in range(rank):
                columns[column].pop()
            if aborted:
                return False
        return False

    solved = assign_row(1)
    if solved:
        result = tuple(arrangements)
        if any(
            sorted(permutation) != list(range(rank))
            for permutation in result
        ):
            raise RuntimeError(
                "Rota solver returned a non-permutation row"
            )
        return True, nodes, result
    if aborted:
        return None, nodes, None
    return False, nodes, None


def _random_prime_field_base(
    *,
    rank: int,
    field_prime: int,
    rng: random.Random,
    template: int,
    row_index: int,
) -> tuple[tuple[int, ...], ...]:
    standard = [
        tuple(1 if coordinate == index else 0 for coordinate in range(rank))
        for index in range(rank)
    ]
    if template in {1, 2}:
        matrix = [list(vector) for vector in standard]
        steps = rank + row_index + template
        for step in range(steps):
            source = (step + row_index) % rank
            target = (
                source
                + 1
                + rng.randrange(max(1, rank - 1))
            ) % rank
            coefficient = 1 + rng.randrange(field_prime - 1)
            matrix[target] = [
                (left + coefficient * right) % field_prime
                for left, right in zip(matrix[target], matrix[source])
            ]
        rng.shuffle(matrix)
        return tuple(sorted(tuple(vector) for vector in matrix))

    base: list[tuple[int, ...]] = []
    attempts = 0
    while len(base) < rank:
        attempts += 1
        if attempts > 100_000:
            raise RuntimeError("failed to generate a prime-field basis")
        if template == 3:
            support = rng.sample(
                range(rank),
                rng.randint(1, min(3, rank)),
            )
            candidate_list = [0] * rank
            for coordinate in support:
                candidate_list[coordinate] = (
                    1 + rng.randrange(field_prime - 1)
                )
            candidate = tuple(candidate_list)
        else:
            candidate = tuple(
                rng.randrange(field_prime) for _ in range(rank)
            )
        if (
            any(candidate)
            and candidate not in base
            and _prime_field_rank(
                tuple((*base, candidate)),
                field_prime,
            )
            == len(base) + 1
        ):
            base.append(candidate)
    return tuple(sorted(base))


def _search_rota_basis(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_cases = _positive_int(budget, "max_cases", 1_000)
    node_limit = _positive_int(
        budget,
        "solver_node_limit",
        1_000_000,
    )
    checked = state.checked
    exact_cases = int(state.metrics.get("exact_solver_cases", 0))
    cutoff_cases = int(state.metrics.get("solver_cutoff_cases", 0))
    nodes_total = int(state.metrics.get("solver_nodes", 0))
    decomposition_cases = int(
        state.metrics.get("decomposition_cases", 0)
    )
    covered = {
        tuple(map(int, values))
        for values in state.metrics.get("rank_field_strata", [])
    }
    templates = {
        int(value)
        for value in state.metrics.get("generator_templates", [])
    }

    if strategy_id == "exact-small":
        rank = min(
            3,
            _positive_int(budget, "max_rank", 3),
        )
        field_prime = 2
        options = _prime_field_bases(rank, field_prime)
        standard = tuple(
            tuple(
                1 if coordinate == index else 0
                for coordinate in range(rank)
            )
            for index in range(rank)
        )
        total_instances = len(options) ** (rank - 1)
        limit = min(max_cases, total_instances)
        while checked < limit:
            value = checked
            selected = []
            for _ in range(rank - 1):
                selected.append(options[value % len(options)])
                value //= len(options)
            bases = (standard, *selected)
            solved, nodes, arrangement = _rota_transversal_decomposition(
                bases,
                field_prime,
                node_limit=node_limit,
            )
            checked += 1
            nodes_total += nodes
            if solved is None:
                cutoff_cases += 1
            else:
                exact_cases += 1
            if solved:
                decomposition_cases += 1
            if solved is False:
                return {
                    "rank": rank,
                    "field_prime": field_prime,
                    "labelled_bases": [
                        [list(vector) for vector in base]
                        for base in bases
                    ],
                    "solver_nodes": nodes,
                    "exhaustive_no_transversal_decomposition": True,
                }, checked, True
            metrics = {
                "coverage_kind": (
                    "exhaustive_binary_rank_three_base_tuples"
                ),
                "rank_field_strata": [[rank, field_prime]],
                "generator_templates": [0],
                "exact_solver_cases": exact_cases,
                "solver_cutoff_cases": cutoff_cases,
                "solver_nodes": nodes_total,
                "decomposition_cases": decomposition_cases,
                "label_semantics": (
                    "row-index and within-row index are disjoint element labels"
                ),
                "total_instances": total_instances,
            }
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "rota_exact_base_tuple",
                    "next_case": checked,
                },
                metrics=metrics,
            )
        return None, state.checked, checked >= total_instances

    minimum_rank = _positive_int(
        budget,
        "minimum_rank",
        5,
        minimum=4,
    )
    maximum_rank = _positive_int(
        budget,
        "max_rank",
        7,
        minimum=minimum_rank,
    )
    maximum_field = _positive_int(
        budget,
        "max_field_prime",
        5,
        minimum=2,
    )
    fields = [
        value
        for value in range(2, maximum_field + 1)
        if isprime(value)
    ]
    strata = tuple(
        (rank, field_prime, template)
        for rank in range(minimum_rank, maximum_rank + 1)
        for field_prime in fields
        for template in range(4)
    )
    if not strata:
        return None, state.checked, True
    while checked < max_cases:
        case_index = checked
        rank, field_prime, template = strata[
            case_index % len(strata)
        ]
        sample_index = case_index // len(strata)
        rng = _case_rng(
            seed,
            sample_index,
            40_000 + rank * 100 + field_prime * 10 + template,
        )
        standard = tuple(
            tuple(
                1 if coordinate == index else 0
                for coordinate in range(rank)
            )
            for index in range(rank)
        )
        bases = (
            standard,
            *(
                _random_prime_field_base(
                    rank=rank,
                    field_prime=field_prime,
                    rng=rng,
                    template=template,
                    row_index=row_index,
                )
                for row_index in range(1, rank)
            ),
        )
        solved, nodes, arrangement = _rota_transversal_decomposition(
            bases,
            field_prime,
            node_limit=node_limit,
        )
        checked += 1
        nodes_total += nodes
        covered.add((rank, field_prime))
        templates.add(template)
        if solved is None:
            cutoff_cases += 1
        else:
            exact_cases += 1
        if solved:
            decomposition_cases += 1
        if solved is False:
            return {
                "rank": rank,
                "field_prime": field_prime,
                "labelled_bases": [
                    [list(vector) for vector in base]
                    for base in bases
                ],
                "solver_nodes": nodes,
                "exhaustive_no_transversal_decomposition": True,
            }, checked, False
        metrics = {
            "coverage_kind": (
                "independent_stratified_prime_field_vector_matroids"
            ),
            "rank_field_strata": [
                list(values) for values in sorted(covered)
            ],
            "generator_templates": sorted(templates),
            "exact_solver_cases": exact_cases,
            "solver_cutoff_cases": cutoff_cases,
            "solver_nodes": nodes_total,
            "decomposition_cases": decomposition_cases,
            "independent_restarts": True,
            "search_completeness": (
                "exact_decision_per_instance_unless_node_limit_recorded"
            ),
            "label_semantics": (
                "row-index and within-row index are disjoint element labels"
            ),
        }
        state.commit(
            checked_increment=1,
            cursor={
                "cursor_kind": "rota_stratified_instance",
                "next_case": checked,
            },
            metrics=metrics,
        )
    return None, state.checked, False


def _integer_matrix_rank(
    vectors: tuple[tuple[int, ...], ...],
) -> int:
    if not vectors:
        return 0
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise ValueError("integer vectors must have equal dimension")
    matrix = [
        [Fraction(value) for value in vector]
        for vector in vectors
    ]
    row = 0
    for column in range(width):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(matrix))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        pivot_value = matrix[row][column]
        matrix[row] = [
            value / pivot_value for value in matrix[row]
        ]
        for other in range(row + 1, len(matrix)):
            factor = matrix[other][column]
            if factor:
                matrix[other] = [
                    left - factor * right
                    for left, right in zip(matrix[other], matrix[row])
                ]
        row += 1
        if row == len(matrix):
            break
    return row


def _integer_determinant(
    matrix: tuple[tuple[int, ...], ...],
) -> int:
    size = len(matrix)
    if size == 0:
        return 1
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a square matrix")
    values = [list(map(int, row)) for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if values[row][pivot_index]
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            values[pivot_index], values[pivot_row] = (
                values[pivot_row],
                values[pivot_index],
            )
            sign = -sign
        pivot = values[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    values[row][column] * pivot
                    - values[row][pivot_index]
                    * values[pivot_index][column]
                )
                values[row][column] = numerator // previous
            values[row][pivot_index] = 0
        previous = pivot
    return sign * values[-1][-1]


def _exact_polytope_facets(
    vertices: tuple[tuple[int, ...], ...],
    dimension: int,
    *,
    subset_limit: int | None = None,
) -> tuple[tuple[frozenset[int], ...] | None, int]:
    subset_count = math.comb(len(vertices), dimension)
    if subset_limit is not None and subset_count > subset_limit:
        return None, 0
    facets: set[frozenset[int]] = set()
    considered = 0
    for indices in itertools.combinations(range(len(vertices)), dimension):
        considered += 1
        origin = vertices[indices[0]]
        differences = tuple(
            tuple(
                vertices[index][coordinate] - origin[coordinate]
                for coordinate in range(dimension)
            )
            for index in indices[1:]
        )
        normal = tuple(
            (-1 if coordinate % 2 else 1)
            * _integer_determinant(
                tuple(
                    tuple(
                        row[column]
                        for column in range(dimension)
                        if column != coordinate
                    )
                    for row in differences
                )
            )
            for coordinate in range(dimension)
        )
        if not any(normal):
            continue
        offset = sum(
            left * right for left, right in zip(normal, origin)
        )
        evaluations = tuple(
            sum(left * right for left, right in zip(normal, vertex))
            - offset
            for vertex in vertices
        )
        if min(evaluations) < 0 < max(evaluations):
            continue
        facet = frozenset(
            index
            for index, evaluation in enumerate(evaluations)
            if evaluation == 0
        )
        if len(facet) >= dimension and len(facet) < len(vertices):
            facets.add(facet)
    return (
        tuple(
            sorted(
                facets,
                key=lambda face: (len(face), tuple(face)),
            )
        ),
        considered,
    )


def _facet_intersection_lattice(
    vertex_count: int,
    facets: tuple[frozenset[int], ...],
) -> frozenset[frozenset[int]]:
    faces: set[frozenset[int]] = {
        frozenset(range(vertex_count))
    }
    for facet in facets:
        faces.update(
            intersection
            for face in tuple(faces)
            if (intersection := face & facet)
        )
    return frozenset(faces)


def _pairwise_incidence_lattice(
    vertex_count: int,
    facets: tuple[frozenset[int], ...],
) -> frozenset[frozenset[int]]:
    faces: set[frozenset[int]] = {
        frozenset(range(vertex_count)),
        *facets,
    }
    frontier = list(facets)
    while frontier:
        face = frontier.pop()
        for other in tuple(faces):
            intersection = face & other
            if intersection and intersection not in faces:
                faces.add(intersection)
                frontier.append(intersection)
    return frozenset(faces)


def _polytope_face_vector(
    vertices: tuple[tuple[int, ...], ...],
    dimension: int,
    faces: frozenset[frozenset[int]],
) -> tuple[int, ...]:
    counts = [0] * (dimension + 1)
    for face in faces:
        anchor = vertices[next(iter(face))]
        differences = tuple(
            tuple(
                vertices[index][coordinate] - anchor[coordinate]
                for coordinate in range(dimension)
            )
            for index in face
        )
        face_dimension = _integer_matrix_rank(differences)
        if not 0 <= face_dimension <= dimension:
            raise RuntimeError("invalid exact polytope face dimension")
        counts[face_dimension] += 1
    return tuple(counts)


def _exact_cs_polytope_data(
    vertices: tuple[tuple[int, ...], ...],
    dimension: int,
    *,
    subset_limit: int | None,
    cross_check: bool,
) -> dict[str, Any] | None:
    if (
        dimension < 1
        or len(vertices) < 2 * dimension
        or len(set(vertices)) != len(vertices)
        or any(len(vertex) != dimension for vertex in vertices)
        or any(not any(vertex) for vertex in vertices)
        or _integer_matrix_rank(vertices) != dimension
    ):
        return None
    vertex_set = set(vertices)
    if any(
        tuple(-coordinate for coordinate in vertex) not in vertex_set
        for vertex in vertices
    ):
        return None
    facets, subsets_considered = _exact_polytope_facets(
        vertices,
        dimension,
        subset_limit=subset_limit,
    )
    if facets is None or not facets:
        return None
    faces = _facet_intersection_lattice(len(vertices), facets)
    if any(
        frozenset({index}) not in faces
        for index in range(len(vertices))
    ):
        return None
    if cross_check:
        incidence_faces = _pairwise_incidence_lattice(
            len(vertices),
            facets,
        )
        if incidence_faces != faces:
            raise RuntimeError(
                "polytope face-lattice closure implementations disagree"
            )
    face_vector = _polytope_face_vector(
        vertices,
        dimension,
        faces,
    )
    if (
        sum(face_vector) != len(faces)
        or face_vector[-1] != 1
        or face_vector[0] != len(vertices)
    ):
        raise RuntimeError("polytope face-vector audit failed")
    facet_incidence = [
        sum(index in facet for facet in facets)
        for index in range(len(vertices))
    ]
    return {
        "facets": facets,
        "faces": faces,
        "face_vector": face_vector,
        "nonempty_face_count": len(faces),
        "facet_subsets_considered": subsets_considered,
        "simplicial": all(
            len(facet) == dimension for facet in facets
        ),
        "simple": all(
            incidence == dimension for incidence in facet_incidence
        ),
    }


def _cross_polytope_vertices(
    dimension: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vector
        for coordinate in range(dimension)
        for vector in (
            tuple(
                1 if index == coordinate else 0
                for index in range(dimension)
            ),
            tuple(
                -1 if index == coordinate else 0
                for index in range(dimension)
            ),
        )
    )


def _cube_vertices(
    dimension: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.product((-1, 1), repeat=dimension))


def _stratified_cs_vertices(
    *,
    dimension: int,
    antipodal_pairs: int,
    template: int,
    seed: int,
    sample_index: int,
) -> tuple[tuple[int, ...], ...]:
    representatives = list(
        itertools.product((1,), *([(-1, 1)] * (dimension - 1)))
    )
    rng = _case_rng(
        seed,
        sample_index,
        50_000 + dimension * 100 + antipodal_pairs * 10 + template,
    )
    for attempt in range(128):
        if template == 0:
            ordered = list(representatives)
            rng.shuffle(ordered)
        elif template == 1:
            offset = (sample_index + attempt) % len(representatives)
            ordered = sorted(
                representatives,
                key=lambda vector: (
                    abs(sum(vector)),
                    sum(value < 0 for value in vector),
                    vector,
                ),
            )
            ordered = ordered[offset:] + ordered[:offset]
        elif template == 2:
            step = 1 + 2 * (
                (sample_index + attempt)
                % max(1, len(representatives) // 2)
            )
            while math.gcd(step, len(representatives)) != 1:
                step += 2
            start = rng.randrange(len(representatives))
            ordered = [
                representatives[
                    (start + step * index) % len(representatives)
                ]
                for index in range(len(representatives))
            ]
        else:
            random_weights = {
                vector: rng.random() for vector in representatives
            }
            ordered = sorted(
                representatives,
                key=lambda vector: (
                    sum(
                        vector[index]
                        != vector[(index + 1) % dimension]
                        for index in range(dimension)
                    ),
                    random_weights[vector],
                ),
            )
        selected = tuple(ordered[:antipodal_pairs])
        if _integer_matrix_rank(selected) == dimension:
            vertices = set(selected) | {
                tuple(-coordinate for coordinate in vector)
                for vector in selected
            }
            return tuple(sorted(vertices))
    raise RuntimeError("failed to generate a full-dimensional cs polytope")


def _search_kalai_three_power_d(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_cases = _positive_int(budget, "max_cases", 100)
    checked = state.checked
    exact_polytopes = int(state.metrics.get("exact_polytopes", 0))
    cap_skips = int(state.metrics.get("facet_cap_skips", 0))
    targeted = int(
        state.metrics.get("non_simple_non_simplicial", 0)
    )
    covered = {
        tuple(map(int, values))
        for values in state.metrics.get("dimension_pair_strata", [])
    }
    minimum_surplus = state.metrics.get("minimum_face_surplus")

    if strategy_id == "exact-small":
        maximum_dimension = _positive_int(
            budget,
            "max_dimension",
            4,
        )
        instances = tuple(
            (dimension, family, vertices)
            for dimension in range(1, maximum_dimension + 1)
            for family, vertices in (
                (
                    "cross_polytope",
                    _cross_polytope_vertices(dimension),
                ),
                ("cube", _cube_vertices(dimension)),
            )
        )
        limit = min(max_cases, len(instances))
        while checked < limit:
            dimension, family, vertices = instances[checked]
            data = _exact_cs_polytope_data(
                vertices,
                dimension,
                subset_limit=None,
                cross_check=True,
            )
            if data is None:
                raise RuntimeError(
                    "small cs polytope exact replay failed"
                )
            exact_polytopes += 1
            surplus = int(data["nonempty_face_count"]) - 3**dimension
            minimum_surplus = (
                surplus
                if minimum_surplus is None
                else min(int(minimum_surplus), surplus)
            )
            checked += 1
            if surplus < 0:
                return {
                    "dimension": dimension,
                    "vertices": [list(vertex) for vertex in vertices],
                    "face_vector": list(data["face_vector"]),
                    "nonempty_face_count": data[
                        "nonempty_face_count"
                    ],
                    "face_convention": (
                        "includes_polytope_excludes_empty_face"
                    ),
                }, checked, True
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "kalai_small_named_polytope",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": (
                        "exact_named_cs_polytope_replication"
                    ),
                    "families": sorted(
                        {
                            *state.metrics.get("families", []),
                            family,
                        }
                    ),
                    "dimensions": list(
                        range(1, maximum_dimension + 1)
                    ),
                    "exact_polytopes": exact_polytopes,
                    "facet_cap_skips": 0,
                    "non_simple_non_simplicial": 0,
                    "minimum_face_surplus": minimum_surplus,
                    "face_convention": (
                        "sum_f_0_through_f_d_includes_P_excludes_empty"
                    ),
                    "double_lattice_cross_check": True,
                },
            )
        return None, state.checked, checked >= len(instances)

    minimum_dimension = _positive_int(
        budget,
        "minimum_dimension",
        5,
        minimum=5,
    )
    maximum_dimension = _positive_int(
        budget,
        "max_dimension",
        7,
        minimum=minimum_dimension,
    )
    maximum_pairs = _positive_int(
        budget,
        "max_antipodal_pairs",
        12,
        minimum=minimum_dimension + 1,
    )
    facet_cap = _positive_int(
        budget,
        "max_facet_subsets",
        2_000_000,
    )
    strata = tuple(
        (dimension, pairs, template)
        for dimension in range(
            minimum_dimension,
            maximum_dimension + 1,
        )
        for pairs in range(
            dimension + 1,
            min(maximum_pairs, 2 ** (dimension - 1)) + 1,
        )
        for template in range(4)
    )
    if not strata:
        return None, state.checked, True
    while checked < max_cases:
        case_index = checked
        dimension, pairs, template = strata[
            case_index % len(strata)
        ]
        sample_index = case_index // len(strata)
        vertices = _stratified_cs_vertices(
            dimension=dimension,
            antipodal_pairs=pairs,
            template=template,
            seed=seed,
            sample_index=sample_index,
        )
        data = _exact_cs_polytope_data(
            vertices,
            dimension,
            subset_limit=facet_cap,
            cross_check=False,
        )
        checked += 1
        covered.add((dimension, pairs))
        if data is None:
            cap_skips += 1
        else:
            exact_polytopes += 1
            if not data["simplicial"] and not data["simple"]:
                targeted += 1
            surplus = int(data["nonempty_face_count"]) - 3**dimension
            minimum_surplus = (
                surplus
                if minimum_surplus is None
                else min(int(minimum_surplus), surplus)
            )
            if surplus < 0:
                return {
                    "dimension": dimension,
                    "vertices": [list(vertex) for vertex in vertices],
                    "face_vector": list(data["face_vector"]),
                    "nonempty_face_count": data[
                        "nonempty_face_count"
                    ],
                    "facet_count": len(data["facets"]),
                    "face_convention": (
                        "includes_polytope_excludes_empty_face"
                    ),
                }, checked, False
        state.commit(
            checked_increment=1,
            cursor={
                "cursor_kind": "kalai_cs_polytope_stratum",
                "next_case": checked,
            },
            metrics={
                "coverage_kind": (
                    "exact_sign_vector_cube_subpolytope_independent_strata"
                ),
                "vertex_family": "antipodally_closed_subsets_of_{-1,+1}^d",
                "dimension_pair_strata": [
                    list(values) for values in sorted(covered)
                ],
                "templates": [0, 1, 2, 3],
                "exact_polytopes": exact_polytopes,
                "facet_cap_skips": cap_skips,
                "non_simple_non_simplicial": targeted,
                "minimum_face_surplus": minimum_surplus,
                "known_dimension_frontier": 4,
                "minimum_search_dimension": minimum_dimension,
                "independent_restarts": True,
                "exact_facets_and_face_lattice": True,
                "face_convention": (
                    "sum_f_0_through_f_d_includes_P_excludes_empty"
                ),
            },
        )
    return None, state.checked, False


def _is_semiprime(value: int, *, odd: bool) -> bool:
    if value < 4 or (odd and value % 2 == 0):
        return False
    factors = factorint(value)
    return sum(int(exponent) for exponent in factors.values()) == 2 and (
        not odd or all(int(prime) % 2 for prime in factors)
    )


def _odd_semiprime_flags(
    limit: int,
    primes: array,
) -> bytearray:
    flags = bytearray(limit + 1)
    odd_primes = primes[1:] if primes and primes[0] == 2 else primes
    for left_index, left in enumerate(odd_primes):
        if left * left > limit:
            break
        for right in odd_primes[left_index:]:
            product = left * right
            if product > limit:
                break
            flags[product] = 1
    return flags


def _search_prime_semiprime(
    budget: Mapping[str, Any],
    *,
    lemoine: bool,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_n = _positive_int(budget, "max_n", 1_000, minimum=11)
    max_cases = _positive_int(budget, "max_cases", max_n)
    flags, primes = _prime_sieve(max_n)
    semiprime_flags = (
        None if lemoine else _odd_semiprime_flags(max_n, primes)
    )
    block_size = _positive_int(budget, "n_block_size", 64)
    first_n = 7 if lemoine else 12
    next_n = max(first_n, int(state.cursor.get("next_n", first_n)))
    if next_n % 2 != first_n % 2:
        next_n += 1
    metrics = {
        **state.metrics,
        "coverage_kind": "segmented_n_blocks_with_global_prime_flags",
        "representation_type": (
            "odd_prime_plus_twice_prime"
            if lemoine
            else "odd_prime_plus_odd_semiprime"
        ),
        "precomputation_limit": max_n,
        "prime_flag_bytes": len(flags),
        "semiprime_flag_bytes": (
            0 if semiprime_flags is None else len(semiprime_flags)
        ),
        "prime_storage_bytes": len(primes) * primes.itemsize,
        "blocks_completed": int(
            state.metrics.get("blocks_completed", 0)
        ),
    }
    while next_n <= max_n and state.checked < max_cases:
        remaining_cases = max_cases - state.checked
        count = min(block_size, remaining_cases)
        block_values = [
            next_n + 2 * offset
            for offset in range(count)
            if next_n + 2 * offset <= max_n
        ]
        tested: list[int] = []
        for value in block_values:
            represented = False
            for prime in primes:
                prime = int(prime)
                if prime >= value:
                    break
                if prime == 2:
                    continue
                remainder = value - prime
                if lemoine:
                    represented = (
                        remainder % 2 == 0
                        and bool(flags[remainder // 2])
                    )
                else:
                    represented = bool(semiprime_flags[remainder])
                if represented:
                    break
            tested.append(value)
            if not represented:
                return {
                    "n": value,
                    "representation_type": metrics[
                        "representation_type"
                    ],
                }, state.checked + len(tested), True
        if not tested:
            break
        next_n = tested[-1] + 2
        metrics = {
            **metrics,
            "blocks_completed": int(metrics["blocks_completed"]) + 1,
            "min_tested_n": min(
                int(metrics.get("min_tested_n", tested[0])),
                tested[0],
            ),
            "max_tested_n": max(
                int(metrics.get("max_tested_n", tested[-1])),
                tested[-1],
            ),
        }
        state.commit(
            checked_increment=len(tested),
            cursor={
                "cursor_kind": "prime_semiprime_n_block",
                "next_n": next_n,
            },
            metrics=metrics,
        )
    return None, state.checked, next_n > max_n


def _agoh_test(value: int) -> bool:
    rational = sympy.Rational(value) * bernoulli(value - 1)
    numerator = int(rational.p)
    denominator = int(rational.q)
    if math.gcd(denominator, value) != 1:
        return False
    residue = numerator * pow(denominator, -1, value) % value
    return residue == value - 1


def _search_quartic(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    height = _positive_int(budget, "root_height", 4)
    max_cases = _positive_int(budget, "max_cases", 1_000)
    variable = symbols("x")

    def evaluate_roots(
        roots: tuple[int, int, int, int],
    ) -> dict[str, Any] | None:
        expression = sympy.prod(variable - root for root in roots)
        polynomial = Poly(sympy.expand(expression), variable, domain=sympy.QQ)
        derivative_roots: list[list[str]] = []
        current = polynomial
        while current.degree() > 1:
            current = current.diff()
            roots_with_multiplicity = current.all_roots()
            if not all(bool(root.is_Rational) for root in roots_with_multiplicity):
                return None
            derivative_roots.append([str(root) for root in roots_with_multiplicity])
        return {
            "coefficients": [int(value) for value in polynomial.all_coeffs()],
            "roots": list(roots),
            "derivative_roots": derivative_roots,
        }

    if strategy_id == "exact-small":
        checked = 0
        for positive_roots in itertools.combinations(
            range(1, height + 1),
            3,
        ):
            if math.gcd(*positive_roots) != 1:
                continue
            roots = (0, *positive_roots)
            checked += 1
            candidate = evaluate_roots(roots)
            if candidate is not None:
                return candidate, checked, True
            if checked >= max_cases:
                return None, checked, False
        return None, checked, True

    height_strata = []
    lower = 0
    upper = 4
    while lower < height:
        upper = min(height, max(lower + 1, upper))
        height_strata.append((lower + 1, upper))
        lower = upper
        upper *= 2
    positions = [
        int(value)
        for value in state.cursor.get(
            "stratum_positions",
            [0] * len(height_strata),
        )
    ]
    if len(positions) != len(height_strata):
        positions = [0] * len(height_strata)
    next_stratum = int(state.cursor.get("next_stratum", 0))
    checked = state.checked
    covered = {
        tuple(map(int, pair))
        for pair in state.metrics.get("root_height_strata", [])
    }
    raw_shapes = int(state.metrics.get("raw_shapes_enumerated", 0))
    while checked < max_cases:
        selected = next_stratum % len(height_strata)
        next_stratum = (selected + 1) % len(height_strata)
        low, high = height_strata[selected]
        position = positions[selected]
        width = high - low + 1
        maximum_root = low + position % width
        pair_rank = position // width
        positions[selected] += 1
        raw_shapes += 1
        if maximum_root < 3 or pair_rank >= math.comb(
            maximum_root - 1,
            2,
        ):
            if all(
                positions[index]
                >= (right - left + 1)
                * max(1, math.comb(right - 1, 2))
                for index, (left, right) in enumerate(height_strata)
            ):
                return None, state.checked, True
            continue
        left_index, middle_index = _unrank_combination_lex(
            maximum_root - 1,
            2,
            pair_rank,
        )
        roots = (
            0,
            left_index + 1,
            middle_index + 1,
            maximum_root,
        )
        if math.gcd(*roots[1:]) != 1:
            continue
        candidate = evaluate_roots(roots)
        checked += 1
        covered.add((low, high))
        metrics = {
            "coverage_kind": "affine_normalized_root_shape_strata",
            "root_height_strata": [
                list(pair) for pair in sorted(covered)
            ],
            "raw_shapes_enumerated": raw_shapes,
            "canonical_shapes_checked": checked,
            "affine_normalization": "subtract_min_then_divide_gcd",
            "duplicate_canonical_shapes": 0,
        }
        state.commit(
            checked_increment=1,
            cursor={
                "cursor_kind": "quartic_root_shape_strata",
                "stratum_positions": positions,
                "next_stratum": next_stratum,
            },
            metrics=metrics,
        )
        if candidate is not None:
            return candidate, state.checked, False
    return None, state.checked, False


def _add_vectors(left: tuple[int, ...], right: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple((a + b) % modulus for a, b in zip(left, right))


def _zero_sum_free(sequence: tuple[tuple[int, ...], ...], modulus: int) -> bool:
    zero = (0,) * len(sequence[0])
    reachable: set[tuple[int, ...]] = set()
    for value in sequence:
        new_values = {value}
        new_values.update(_add_vectors(existing, value, modulus) for existing in reachable)
        if zero in new_values:
            return False
        reachable.update(new_values)
    return True


def _search_davenport(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_n = _positive_int(budget, "max_n", 2, minimum=2)
    max_dimension = _positive_int(budget, "max_dimension", 2)
    max_cases = _positive_int(budget, "max_cases", 1_000)
    if strategy_id == "multistart":
        memory_mb = _positive_int(budget, "memory_mb", 1_024)
        max_state_space = min(1_000_000, max(4_096, memory_mb * 512))
        target_moduli = (6, 10, 12, 14, 15)
        strata = [
            (modulus, dimension)
            for modulus in target_moduli
            if modulus <= max_n
            for dimension in range(3, max_dimension + 1)
            if modulus**dimension <= max_state_space
        ]
        if not strata:
            return None, state.checked, True
        covered = {
            tuple(int(value) for value in pair)
            for pair in state.metrics.get("parameter_strata", [])
        }
        checked = state.checked
        accepted_mutations = int(
            state.metrics.get("accepted_prefix_mutations", 0)
        )
        attempted_mutations = int(
            state.metrics.get("attempted_prefix_mutations", 0)
        )
        prefix_hashes = {
            str(value)
            for value in state.metrics.get("prefix_hashes", [])
        }
        while checked < max_cases:
            case_index = checked
            modulus, dimension = strata[
                (case_index + abs(int(seed))) % len(strata)
            ]
            rng = _case_rng(seed, case_index, 563)
            length = dimension * (modulus - 1) + 1
            basis = [
                tuple(
                    1 if coordinate == basis_index else 0
                    for coordinate in range(dimension)
                )
                for basis_index in range(dimension)
            ]
            prefix = [
                vector
                for vector in basis
                for _ in range(modulus - 1)
            ]
            mutation_budget = 1 + case_index % 4
            for _ in range(mutation_budget):
                attempted_mutations += 1
                position = rng.randrange(len(prefix))
                replacement = tuple(
                    rng.randrange(modulus)
                    for _ in range(dimension)
                )
                if not any(replacement):
                    continue
                trial = list(prefix)
                trial[position] = replacement
                if _zero_sum_free(tuple(trial), modulus):
                    prefix = trial
                    accepted_mutations += 1
            local_position = case_index // len(strata)
            append_code = 1 + local_position % (
                modulus**dimension - 1
            )
            coordinates = []
            residual = append_code
            for _ in range(dimension):
                coordinates.append(residual % modulus)
                residual //= modulus
            appended = tuple(coordinates)
            sequence = tuple((*prefix, appended))
            covered.add((modulus, dimension))
            prefix_hash = str(
                sum(
                    (position + 1)
                    * sum(
                        (coordinate + 1) * value
                        for coordinate, value in enumerate(vector)
                    )
                    for position, vector in enumerate(prefix)
                )
            )
            prefix_hashes.add(prefix_hash)
            if _zero_sum_free(sequence, modulus):
                return {
                    "modulus": modulus,
                    "dimension": dimension,
                    "sequence": [list(value) for value in sequence],
                }, checked + 1, False
            checked += 1
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "davenport_critical_prefix_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": (
                        "critical_zero_sum_free_prefix_mutation"
                    ),
                    "parameter_strata": [
                        list(pair) for pair in sorted(covered)
                    ],
                    "eligible_strata": len(strata),
                    "max_state_space": max_state_space,
                    "target_moduli": list(target_moduli),
                    "minimum_dimension": 3,
                    "attempted_prefix_mutations": attempted_mutations,
                    "accepted_prefix_mutations": accepted_mutations,
                    "prefix_hashes": sorted(prefix_hashes)[-128:],
                    "iid_sequence_generation": False,
                },
            )
        return None, state.checked, False

    checked = 0
    for modulus in range(2, max_n + 1):
        for dimension in range(1, max_dimension + 1):
            elements = list(itertools.product(range(modulus), repeat=dimension))
            length = dimension * (modulus - 1) + 1
            for indices in itertools.combinations_with_replacement(range(len(elements)), length):
                sequence = tuple(elements[index] for index in indices)
                checked += 1
                if _zero_sum_free(sequence, modulus):
                    return {
                        "modulus": modulus,
                        "dimension": dimension,
                        "sequence": [list(value) for value in sequence],
                    }, checked, True
                if checked >= max_cases:
                    return None, checked, False
    return None, checked, True


def _search_hardy_littlewood_b(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    maximum = _positive_int(budget, "max_xy", 500, minimum=2)
    max_cases = _positive_int(budget, "max_cases", maximum * maximum)
    if strategy_id == "gap-targeted":
        ratio = _positive_int(
            budget,
            "minimum_x_to_y_ratio",
            128,
            minimum=4,
        )
        maximum_y = max(2, maximum // (ratio + 1))
        y_values = {2, 3}
        value = 5
        while value <= maximum_y:
            y_values.add(value)
            value = max(value + 1, (value * 8 + 4) // 5)
        y_strata = sorted(
            value for value in y_values if 2 <= value <= maximum_y
        )
        if not y_strata:
            return None, state.checked, True
        positions = [
            int(value)
            for value in state.cursor.get(
                "stratum_positions",
                [0] * len(y_strata),
            )
        ]
        if len(positions) != len(y_strata):
            positions = [0] * len(y_strata)
        next_stratum = int(state.cursor.get("next_stratum", 0))
        checked = state.checked
        min_sum = state.metrics.get("min_x_plus_y")
        max_sum = state.metrics.get("max_x_plus_y")
        minimum_ratio_seen = state.metrics.get("minimum_x_to_y_seen")
        maximum_window_count = int(
            state.metrics.get("maximum_window_prime_count", 0)
        )
        maximum_excess = int(
            state.metrics.get("maximum_prime_count_excess", -10**9)
        )
        while checked < max_cases:
            selected = (
                next_stratum + abs(int(seed))
            ) % len(y_strata)
            next_stratum = (
                selected + 1 - abs(int(seed))
            ) % len(y_strata)
            right = y_strata[selected]
            position = positions[selected]
            left = maximum - right - position
            positions[selected] += 1
            if left < ratio * right:
                if all(
                    maximum - y - positions[index] < ratio * y
                    for index, y in enumerate(y_strata)
                ):
                    return None, state.checked, True
                continue
            pi_left = int(sympy.primepi(left))
            pi_right = int(sympy.primepi(right))
            pi_sum = int(sympy.primepi(left + right))
            window_count = pi_sum - pi_left
            excess = window_count - pi_right
            checked += 1
            total = left + right
            min_sum = total if min_sum is None else min(int(min_sum), total)
            max_sum = total if max_sum is None else max(int(max_sum), total)
            observed_ratio = left // right
            minimum_ratio_seen = (
                observed_ratio
                if minimum_ratio_seen is None
                else min(int(minimum_ratio_seen), observed_ratio)
            )
            maximum_window_count = max(
                maximum_window_count,
                window_count,
            )
            maximum_excess = max(maximum_excess, excess)
            if excess > 0:
                return {
                    "x": left,
                    "y": right,
                    "pi_x": pi_left,
                    "pi_y": pi_right,
                    "pi_x_plus_y": pi_sum,
                    "prime_count_in_x_window": window_count,
                }, checked, False
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "hardy_littlewood_sliding_window",
                    "stratum_positions": positions,
                    "next_stratum": next_stratum,
                },
                metrics={
                    "coverage_kind": (
                        "prime_dense_y_much_smaller_than_x_windows"
                    ),
                    "y_strata": y_strata,
                    "minimum_x_to_y_ratio": ratio,
                    "minimum_x_to_y_seen": minimum_ratio_seen,
                    "min_x_plus_y": min_sum,
                    "max_x_plus_y": max_sum,
                    "maximum_window_prime_count": maximum_window_count,
                    "maximum_prime_count_excess": maximum_excess,
                    "unique_pair_generation": True,
                    "duplicate_pairs": 0,
                    "prime_count_method": "exact_sympy_primepi",
                },
            )
        return None, state.checked, False

    flags, _ = _prime_sieve(2 * maximum)
    counts = [0] * len(flags)
    for value in range(1, len(flags)):
        counts[value] = counts[value - 1] + int(flags[value])
    checked = 0
    pairs = itertools.product(range(2, maximum + 1), repeat=2)
    for left, right in pairs:
        checked += 1
        if counts[left + right] > counts[left] + counts[right]:
            return {
                "x": left,
                "y": right,
                "pi_x": counts[left],
                "pi_y": counts[right],
                "pi_x_plus_y": counts[left + right],
            }, checked, True
        if checked >= max_cases:
            return None, checked, False
    return None, checked, True


def _circular_distance(value: Fraction) -> Fraction:
    fractional = value - math.floor(value)
    return min(fractional, 1 - fractional)


def _runner_has_lonely_time(speeds: tuple[int, ...], runner: int) -> bool:
    count = len(speeds)
    relative = [
        abs(speed - speeds[runner])
        for index, speed in enumerate(speeds)
        if index != runner
    ]
    threshold = Fraction(1, count)
    feasible = [(Fraction(0), Fraction(1))]
    for magnitude in relative:
        allowed = [
            (
                Fraction(integer, magnitude)
                + threshold / magnitude,
                Fraction(integer + 1, magnitude)
                - threshold / magnitude,
            )
            for integer in range(magnitude)
        ]
        intersections = []
        left_index = right_index = 0
        while left_index < len(feasible) and right_index < len(allowed):
            lower = max(
                feasible[left_index][0],
                allowed[right_index][0],
            )
            upper = min(
                feasible[left_index][1],
                allowed[right_index][1],
            )
            if lower <= upper:
                intersections.append((lower, upper))
            if feasible[left_index][1] < allowed[right_index][1]:
                left_index += 1
            else:
                right_index += 1
        feasible = intersections
        if not feasible:
            return False
    return True


def _search_lonely_runner(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_runners = _positive_int(budget, "max_runners", 4, minimum=2)
    max_speed = _positive_int(budget, "max_speed", 6, minimum=1)
    max_cases = _positive_int(budget, "max_cases", 1_000)
    max_runners = min(max_runners, max_speed + 1)
    if strategy_id == "multistart":
        minimum_runners = _positive_int(
            budget,
            "minimum_runners",
            14,
            minimum=14,
        )
        runner_counts = list(
            range(minimum_runners, max_runners + 1)
        )
        if not runner_counts:
            return None, state.checked, True
        tuple_ranks = {
            int(key): int(value)
            for key, value in dict(
                state.cursor.get("tuple_ranks") or {}
            ).items()
        }
        covered_counts = {
            int(value) for value in state.metrics.get("runner_counts", [])
        }
        max_speed_seen = int(state.metrics.get("max_speed_seen", 0))
        predicates_checked = int(
            state.metrics.get("runner_predicates_checked", 0)
        )
        raw_tuples = int(
            state.metrics.get("raw_speed_tuples_enumerated", 0)
        )
        checked = state.checked
        while checked < max_cases:
            count = runner_counts[
                (checked + abs(int(seed))) % len(runner_counts)
            ]
            rank = tuple_ranks.get(count, 0)
            total = math.comb(max_speed, count - 1)
            if rank >= total:
                if all(
                    tuple_ranks.get(value, 0)
                    >= math.comb(max_speed, value - 1)
                    for value in runner_counts
                ):
                    return None, state.checked, True
                tuple_ranks[count] = rank
                continue
            tuple_ranks[count] = rank + 1
            indices = _unrank_combination_lex(
                max_speed,
                count - 1,
                rank,
            )
            raw_tuples += 1
            speeds = (0, *(index + 1 for index in indices))
            normalization_gcd = math.gcd(*speeds[1:])
            if normalization_gcd != 1:
                continue
            covered_counts.add(count)
            max_speed_seen = max(max_speed_seen, speeds[-1])
            failed_runner = None
            for runner in range(count):
                predicates_checked += 1
                if not _runner_has_lonely_time(speeds, runner):
                    failed_runner = runner
                    break
            checked += 1
            if failed_runner is not None:
                return {
                    "speeds": list(speeds),
                    "runner_index": failed_runner,
                }, checked, False
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "lonely_runner_canonical_tuple",
                    "tuple_ranks": {
                        str(key): value
                        for key, value in tuple_ranks.items()
                    },
                },
                metrics={
                    "coverage_kind": (
                        "post_total_runner_13_canonical_speed_tuples"
                    ),
                    "runner_counts": sorted(covered_counts),
                    "max_speed_seen": max_speed_seen,
                    "raw_speed_tuples_enumerated": raw_tuples,
                    "canonical_tuples_checked": checked,
                    "runner_predicates_checked": predicates_checked,
                    "normalization": "subtract_min_then_divide_gcd",
                    "duplicate_canonical_tuples": 0,
                    "proved_frontier_total_runners": 13,
                },
            )
        return None, state.checked, False

    checked = 0
    for count in range(2, max_runners + 1):
        for speeds in itertools.combinations(range(max_speed + 1), count):
            normalized = tuple(speed - speeds[0] for speed in speeds)
            divisor = math.gcd(*normalized[1:])
            if divisor != 1:
                continue
            failed_runner = None
            for runner in range(count):
                if not _runner_has_lonely_time(speeds, runner):
                    failed_runner = runner
                    break
            checked += 1
            if failed_runner is not None:
                return {
                    "speeds": list(normalized),
                    "runner_index": failed_runner,
                }, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _cyclic_cosets(modulus: int) -> list[tuple[int, ...]]:
    cosets: set[tuple[int, ...]] = set()
    for subgroup_size in sympy.divisors(modulus):
        step = modulus // int(subgroup_size)
        subgroup = {(index * step) % modulus for index in range(int(subgroup_size))}
        for representative in range(step):
            cosets.add(tuple(sorted((representative + value) % modulus for value in subgroup)))
    return sorted(cosets)


def _search_kou_21_115(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_order = _positive_int(budget, "max_order", 12, minimum=2)
    max_cosets = _positive_int(budget, "max_cosets", 3)
    max_cases = _positive_int(budget, "max_cases", 2_000)
    if strategy_id == "multistart":
        moduli = list(range(2, max_order + 1))
        covered_moduli = {
            int(value) for value in state.metrics.get("moduli", [])
        }
        covered_sizes = {
            int(value) for value in state.metrics.get("family_sizes", [])
        }
        pending = 0
        checked = state.checked
        while checked < max_cases:
            case_index = checked
            modulus = moduli[
                (case_index + abs(int(seed))) % len(moduli)
            ]
            cosets = _cyclic_cosets(modulus)
            largest = min(max_cosets, len(cosets))
            family_size = 1 + (
                case_index // len(moduli) + abs(int(seed))
            ) % largest
            rng = _case_rng(seed, case_index, 2115)
            family = tuple(rng.sample(cosets, family_size))
            checked += 1
            pending += 1
            covered_moduli.add(modulus)
            covered_sizes.add(family_size)
            union = set().union(*(set(coset) for coset in family))
            complement = modulus - len(union)
            if complement and complement * (2**len(family)) < modulus:
                return {
                    "cyclic_modulus": modulus,
                    "cosets": [list(coset) for coset in family],
                    "complement_size": complement,
                }, checked, False
            if pending >= 64:
                state.commit(
                    checked_increment=pending,
                    cursor={
                        "cursor_kind": "cyclic_coset_stratified_case",
                        "next_case": checked,
                    },
                    metrics={
                        "coverage_kind": "stratified_random_coset_families",
                        "moduli": sorted(covered_moduli),
                        "family_sizes": sorted(covered_sizes),
                    },
                )
                pending = 0
        if pending:
            state.commit(
                checked_increment=pending,
                cursor={
                    "cursor_kind": "cyclic_coset_stratified_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": "stratified_random_coset_families",
                    "moduli": sorted(covered_moduli),
                    "family_sizes": sorted(covered_sizes),
                },
            )
        return None, state.checked, False

    checked = 0
    for modulus in range(2, max_order + 1):
        cosets = _cyclic_cosets(modulus)
        families = (
            family
            for size in range(1, min(max_cosets, len(cosets)) + 1)
            for family in itertools.combinations(cosets, size)
        )
        for family in families:
            checked += 1
            union = set().union(*(set(coset) for coset in family))
            complement = modulus - len(union)
            if complement and complement * (2 ** len(family)) < modulus:
                return {
                    "cyclic_modulus": modulus,
                    "cosets": [list(coset) for coset in family],
                    "complement_size": complement,
                }, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _passes_bpsw_part_one(value: int) -> bool:
    return (
        value > 2
        and value % 2 == 1
        and bool(mr(value, [2]))
        and bool(is_strong_lucas_prp(value))
    )


def _native_strong_miller_rabin_base_2(value: int) -> bool:
    if value == 2:
        return True
    if value < 3 or value % 2 == 0:
        return False
    odd_part = value - 1
    power_of_two = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        power_of_two += 1
    residue = pow(2, odd_part, value)
    if residue in {1, value - 1}:
        return True
    for _ in range(power_of_two - 1):
        residue = residue * residue % value
        if residue == value - 1:
            return True
    return False


def _selfridge_parameters(value: int) -> tuple[int, int, int] | None:
    absolute = 5
    sign = 1
    while True:
        discriminant = sign * absolute
        common = math.gcd(abs(discriminant), value)
        if 1 < common < value:
            return None
        symbol = int(jacobi_symbol(discriminant, value))
        if symbol == -1:
            return discriminant, 1, (1 - discriminant) // 4
        absolute += 2
        sign = -sign


def _lucas_sequence_mod(
    modulus: int,
    p_value: int,
    q_value: int,
    index: int,
) -> tuple[int, int, int]:
    if index == 0:
        return 0, 2 % modulus, 1 % modulus
    discriminant = p_value * p_value - 4 * q_value
    inverse_two = (modulus + 1) // 2
    u_value = 0
    v_value = 2
    q_power = 1
    for bit in bin(index)[2:]:
        u_value = u_value * v_value % modulus
        v_value = (v_value * v_value - 2 * q_power) % modulus
        q_power = q_power * q_power % modulus
        if bit == "1":
            old_u, old_v = u_value, v_value
            u_value = (p_value * old_u + old_v) * inverse_two % modulus
            v_value = (
                discriminant * old_u + p_value * old_v
            ) * inverse_two % modulus
            q_power = q_power * q_value % modulus
    return u_value, v_value, q_power


def _native_selfridge_strong_lucas_prp(value: int) -> bool:
    if value < 3 or value % 2 == 0 or math.isqrt(value) ** 2 == value:
        return False
    parameters = _selfridge_parameters(value)
    if parameters is None:
        return False
    _, p_value, q_value = parameters
    odd_part = value + 1
    power_of_two = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        power_of_two += 1
    u_value, v_value, q_power = _lucas_sequence_mod(
        value,
        p_value,
        q_value,
        odd_part,
    )
    if u_value == 0 or v_value == 0:
        return True
    for _ in range(1, power_of_two):
        v_value = (v_value * v_value - 2 * q_power) % value
        q_power = q_power * q_power % value
        if v_value == 0:
            return True
    return False


def _internally_verify_bpsw_candidate(candidate: Mapping[str, Any]) -> bool:
    value = int(candidate["n"])
    factor = int(candidate["nontrivial_factor"])
    cofactor = int(candidate["cofactor"])
    certificate = candidate.get("factor_certificate")
    if not isinstance(certificate, Mapping):
        return False
    return (
        value > 2
        and value % 2 == 1
        and 1 < factor < value
        and 1 < cofactor < value
        and factor * cofactor == value
        and int(certificate.get("factor", 0)) == factor
        and int(certificate.get("cofactor", 0)) == cofactor
        and int(certificate.get("product", 0)) == value
        and _native_strong_miller_rabin_base_2(value)
        and _native_selfridge_strong_lucas_prp(value)
    )


def _segmented_odd_composites(
    start: int,
    stop: int,
    segment_size: int,
):
    if stop < max(3, start):
        return
    _, base_primes = _prime_sieve(math.isqrt(stop))
    lower_bound = max(3, start)
    for low in range(lower_bound, stop + 1, segment_size):
        high = min(stop, low + segment_size - 1)
        first_factors = [0] * (high - low + 1)
        for prime in base_primes:
            first = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if first > high:
                continue
            for multiple in range(first, high + 1, prime):
                offset = multiple - low
                if first_factors[offset] == 0:
                    first_factors[offset] = prime
        for offset, factor in enumerate(first_factors):
            value = low + offset
            if value % 2 == 1 and factor:
                yield value, factor


def _bpsw_candidate_payload(
    value: int,
    factor: int,
    *,
    family: str,
    family_parameters: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "n": int(value),
        "nontrivial_factor": int(factor),
        "cofactor": int(value // factor),
        "factor_certificate": {
            "factor": int(factor),
            "cofactor": int(value // factor),
            "product": int(value),
        },
        "miller_rabin_base_2": True,
        "strong_lucas_prp": True,
        "lucas_parameter_method": "Selfridge_Method_A",
        "search_family": family,
        "family_parameters": dict(family_parameters),
    }


def _search_bpsw_replication(
    budget: Mapping[str, Any],
    *,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    start_n = _positive_int(budget, "start_n", 3, minimum=3)
    max_n = min(
        _positive_int(budget, "max_n", 100_000, minimum=3),
        _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
    )
    segment_size = min(_positive_int(budget, "segment_size", 4_096), 16_384)
    max_cases = _positive_int(budget, "max_cases", 50_000)
    next_n = max(start_n, int(state.cursor.get("next_n", start_n)))
    metrics = {
        **state.metrics,
        "coverage_kind": "published_range_replication",
        "known_exhaustive_lower_bound": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
        "lucas_variant": "Method_A_Selfridge_strong",
        "segments_completed": int(state.metrics.get("segments_completed", 0)),
    }
    while next_n <= max_n and state.checked < max_cases:
        high = min(max_n, next_n + segment_size - 1)
        values: list[int] = []
        for value, factor in _segmented_odd_composites(next_n, high, segment_size):
            if state.checked + len(values) >= max_cases:
                break
            values.append(value)
            if _passes_bpsw_part_one(value):
                return (
                    _bpsw_candidate_payload(
                        value,
                        factor,
                        family="sequential_composite_replication",
                        family_parameters={"segment": [next_n, high]},
                    ),
                    state.checked + len(values),
                    True,
                )
        if values and state.checked + len(values) >= max_cases:
            resume_n = values[-1] + 2
        else:
            resume_n = high + 1
        metrics = _coverage_metrics(
            state,
            family="sequential_composite_replication",
            values=values,
            extra={
                **metrics,
                "segments_completed": int(metrics["segments_completed"]) + 1,
                "last_interval": [next_n, high],
            },
        )
        state.commit(
            checked_increment=len(values),
            cursor={
                "cursor_kind": "bpsw_replication_segment",
                "next_n": resume_n,
            },
            metrics=metrics,
        )
        next_n = resume_n
    return None, state.checked, next_n > max_n


def _chernick_value(parameter: int) -> tuple[int, int, int, int]:
    first = 6 * parameter + 1
    second = 12 * parameter + 1
    third = 18 * parameter + 1
    return first * second * third, first, second, third


def _first_chernick_parameter_above(lower_bound: int) -> int:
    low, high = 1, 2
    while _chernick_value(high)[0] <= lower_bound:
        low, high = high, high * 2
    while low + 1 < high:
        middle = (low + high) // 2
        if _chernick_value(middle)[0] <= lower_bound:
            low = middle
        else:
            high = middle
    return high


def _search_bpsw_chernick(
    budget: Mapping[str, Any],
    *,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    discovery_min = max(
        _positive_int(
            budget,
            "discovery_min_n",
            _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND + 1,
        ),
        _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND + 1,
    )
    max_n = _positive_int(budget, "max_n", 10**27, minimum=discovery_min)
    max_cases = _positive_int(budget, "max_cases", 100_000_000)
    first_parameter = _first_chernick_parameter_above(discovery_min - 1)
    parameter = max(
        first_parameter,
        int(state.cursor.get("next_structure_parameter", first_parameter)),
    )
    block_size = min(_positive_int(budget, "structure_block_size", 256), 2_048)
    metrics = {
        **state.metrics,
        "coverage_kind": "post_2^64_discovery",
        "known_exhaustive_lower_bound": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
        "discovery_min_n_exclusive": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
        "lucas_variant": "Method_A_Selfridge_strong",
        "structure": "(6m+1)(12m+1)(18m+1)",
        "korselt_certified_samples": int(
            state.metrics.get("korselt_certified_samples", 0)
        ),
        "structure_parameters_scanned": int(
            state.metrics.get("structure_parameters_scanned", 0)
        ),
        "min_structure_parameter": state.metrics.get("min_structure_parameter"),
        "max_structure_parameter": state.metrics.get("max_structure_parameter"),
        "blocks_completed": int(state.metrics.get("blocks_completed", 0)),
    }
    while state.checked < max_cases:
        first_value = _chernick_value(parameter)[0]
        if first_value > max_n:
            return None, state.checked, True
        remaining = max_cases - state.checked
        stop_parameter = parameter + min(block_size, remaining) - 1
        values: list[int] = []
        certified = 0
        actual_stop = parameter - 1
        for current in range(parameter, stop_parameter + 1):
            value, first, second, third = _chernick_value(current)
            if value > max_n:
                break
            actual_stop = current
            values.append(value)
            is_korselt = bool(
                isprime(first) and isprime(second) and isprime(third)
            )
            certified += int(is_korselt)
            if _passes_bpsw_part_one(value):
                return (
                    _bpsw_candidate_payload(
                        value,
                        first,
                        family="chernick_korselt_form",
                        family_parameters={
                            "m": current,
                            "linear_factors": [first, second, third],
                            "korselt_certified": is_korselt,
                        },
                    ),
                    state.checked + len(values),
                    True,
                )
        if not values:
            return None, state.checked, True
        parameter = actual_stop + 1
        metrics = _coverage_metrics(
            state,
            family="chernick_korselt_form",
            values=values,
            extra={
                **metrics,
                "korselt_certified_samples": int(
                    metrics["korselt_certified_samples"]
                )
                + certified,
                "structure_parameters_scanned": int(
                    metrics["structure_parameters_scanned"]
                )
                + len(values),
                "blocks_completed": int(metrics["blocks_completed"]) + 1,
                "last_parameter_interval": [
                    actual_stop - len(values) + 1,
                    actual_stop,
                ],
                "min_structure_parameter": (
                    actual_stop - len(values) + 1
                    if metrics.get("min_structure_parameter") is None
                    else min(
                        int(metrics["min_structure_parameter"]),
                        actual_stop - len(values) + 1,
                    )
                ),
                "max_structure_parameter": (
                    actual_stop
                    if metrics.get("max_structure_parameter") is None
                    else max(int(metrics["max_structure_parameter"]), actual_stop)
                ),
            },
        )
        state.commit(
            checked_increment=len(values),
            cursor={
                "cursor_kind": "bpsw_structure_parameter",
                "next_structure_parameter": parameter,
            },
            metrics=metrics,
        )
    return None, state.checked, False


def _remote_bpsw_layers(minimum: int, maximum: int, count: int) -> tuple[int, ...]:
    if maximum < minimum:
        return ()
    layers: list[int] = []
    center = minimum
    while center <= maximum and len(layers) < count:
        layers.append(center)
        center *= 2
    if layers and layers[-1] < maximum and len(layers) < count:
        layers.append(maximum)
    return tuple(layers)


def _remote_semiprime_streams(
    layers: tuple[int, ...],
) -> tuple[dict[str, Any], ...]:
    streams: list[dict[str, Any]] = []
    used_first_factors: set[int] = set()
    for layer_index, center in enumerate(layers):
        root = math.isqrt(center)
        for scale in (1, 4, 16, 64):
            first = int(sympy.prevprime(max(4, root // scale + 1)))
            while first in used_first_factors:
                first = int(sympy.prevprime(first))
            used_first_factors.add(first)
            second = int(
                nextprime(max(first + 1, (center + first - 1) // first))
            )
            streams.append(
                {
                    "layer_index": layer_index,
                    "layer_center": center,
                    "scale": scale,
                    "family": (
                        "remote_semiprime_balanced"
                        if scale == 1
                        else f"remote_semiprime_skew_{scale}"
                    ),
                    "first": first,
                    "initial_second": second,
                }
            )
    return tuple(streams)


def _search_bpsw_remote_layers(
    budget: Mapping[str, Any],
    *,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    discovery_min = max(
        _positive_int(
            budget,
            "discovery_min_n",
            _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND + 1,
        ),
        _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND + 1,
    )
    max_n = _positive_int(budget, "max_n", 10**27, minimum=discovery_min)
    max_cases = _positive_int(budget, "max_cases", 100_000_000)
    requested_layers = _positive_int(budget, "remote_layers", 24)
    layers = _remote_bpsw_layers(discovery_min, max_n, requested_layers)
    streams = _remote_semiprime_streams(layers)
    sample_index = max(0, int(state.cursor.get("next_sample_index", 0)))
    block_size = min(_positive_int(budget, "remote_block_size", 32), 256)
    restored_seconds = state.cursor.get("stream_next_seconds")
    restored_positions = state.cursor.get("stream_positions")
    if (
        isinstance(restored_seconds, list)
        and len(restored_seconds) == len(streams)
    ):
        stream_next_seconds = [int(value) for value in restored_seconds]
    else:
        stream_next_seconds = [
            int(stream["initial_second"]) for stream in streams
        ]
    if (
        isinstance(restored_positions, list)
        and len(restored_positions) == len(streams)
    ):
        stream_positions = [int(value) for value in restored_positions]
    else:
        stream_positions = [0] * len(streams)
    metrics = {
        **state.metrics,
        "coverage_kind": "post_2^64_discovery",
        "known_exhaustive_lower_bound": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
        "discovery_min_n_exclusive": _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
        "lucas_variant": "Method_A_Selfridge_strong",
        "layer_centers": list(layers),
        "layer_count": len(layers),
        "stream_count": len(streams),
        "unique_candidate_generation": True,
        "duplicate_candidates_generated": 0,
        "layer_sample_counts": {
            str(key): int(value)
            for key, value in dict(
                state.metrics.get("layer_sample_counts") or {}
            ).items()
        },
        "blocks_completed": int(state.metrics.get("blocks_completed", 0)),
    }
    if not streams:
        return None, state.checked, True
    while state.checked < max_cases:
        remaining = max_cases - state.checked
        count = min(block_size, remaining)
        values: list[int] = []
        families: list[str] = []
        samples: list[tuple[int, int, int, str, int, int, int]] = []
        inactive_visits = 0
        while len(samples) < count:
            stream_index = sample_index % len(streams)
            sample_index += 1
            stream = streams[stream_index]
            first = int(stream["first"])
            second = stream_next_seconds[stream_index]
            value = first * second
            if value > max_n:
                inactive_visits += 1
                if inactive_visits >= len(streams):
                    break
                continue
            inactive_visits = 0
            position = stream_positions[stream_index]
            stream_positions[stream_index] = position + 1
            stream_next_seconds[stream_index] = int(nextprime(second))
            family = str(stream["family"])
            values.append(value)
            families.append(family)
            samples.append(
                (
                    value,
                    first,
                    second,
                    family,
                    int(stream["layer_index"]),
                    position,
                    stream_index,
                )
            )
            if _passes_bpsw_part_one(value):
                return (
                    _bpsw_candidate_payload(
                        value,
                        first,
                        family=family,
                        family_parameters={
                            "prime_factors": [first, second],
                            "layer_index": int(stream["layer_index"]),
                            "layer_center": int(stream["layer_center"]),
                            "scale": int(stream["scale"]),
                            "stream_index": stream_index,
                            "position": position,
                        },
                    ),
                    state.checked + len(values),
                    True,
                )
        if not samples:
            return None, state.checked, True
        family_counts = {
            str(key): int(value)
            for key, value in dict(metrics.get("family_sample_counts") or {}).items()
        }
        for family in families:
            family_counts[family] = family_counts.get(family, 0) + 1
        layer_sample_counts = {
            str(key): int(value)
            for key, value in dict(metrics.get("layer_sample_counts") or {}).items()
        }
        for sample in samples:
            layer_key = str(sample[4])
            layer_sample_counts[layer_key] = layer_sample_counts.get(layer_key, 0) + 1
        previous_min = metrics.get("min_tested_n")
        previous_max = metrics.get("max_tested_n")
        metrics = {
            **metrics,
            "family_sample_counts": family_counts,
            "layer_sample_counts": layer_sample_counts,
            "min_tested_n": min(
                min(values),
                min(values) if previous_min is None else int(previous_min),
            ),
            "max_tested_n": max(
                max(values),
                max(values) if previous_max is None else int(previous_max),
            ),
            "blocks_completed": int(metrics["blocks_completed"]) + 1,
            "last_sample_index": sample_index - 1,
            "last_layer_indices": sorted({sample[4] for sample in samples}),
            "last_stream_indices": sorted({sample[6] for sample in samples}),
        }
        state.commit(
            checked_increment=len(values),
            cursor={
                "cursor_kind": "bpsw_remote_layer_sample",
                "next_sample_index": sample_index,
                "stream_next_seconds": list(stream_next_seconds),
                "stream_positions": list(stream_positions),
            },
            metrics=metrics,
        )
    return None, state.checked, False


def _search_bpsw_counterexample(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    state: _SearchProgressState | None = None,
) -> tuple[dict[str, Any] | None, int, bool]:
    if state is None:
        state = _SearchProgressState(
            problem_id="unsolvedmath-opg-511",
            strategy_id=strategy_id,
            checkpoint=None,
            progress=None,
            resumable=True,
        )
    if strategy_id == "exact-small":
        return _search_bpsw_replication(budget, state=state)
    if strategy_id == "chernick-korselt":
        return _search_bpsw_chernick(budget, state=state)
    if strategy_id == "remote-factor-layers":
        return _search_bpsw_remote_layers(budget, state=state)
    raise ValueError(f"unsupported BPSW strategy: {strategy_id}")


def _subsequence_sums(
    sequence: tuple[tuple[int, int], ...],
    modulus: int,
) -> set[tuple[int, int]]:
    reachable = {(0, 0)}
    for value in sequence:
        reachable.update(
            ((left + value[0]) % modulus, (right + value[1]) % modulus)
            for left, right in tuple(reachable)
        )
    return reachable


def _search_few_subsequence_sums(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_n = _positive_int(budget, "max_n", 3, minimum=2)
    max_cases = _positive_int(budget, "max_cases", 2_000)
    if strategy_id == "multistart":
        strata = [
            (modulus, t)
            for modulus in range(2, max_n + 1)
            for t in range(modulus)
        ]
        covered = {
            tuple(int(value) for value in pair)
            for pair in state.metrics.get("parameter_strata", [])
        }
        pending = 0
        checked = state.checked
        while checked < max_cases:
            case_index = checked
            modulus, t = strata[
                (case_index + abs(int(seed))) % len(strata)
            ]
            rng = _case_rng(seed, case_index, 156)
            length = modulus - 1 + t
            sequence = tuple(
                (rng.randrange(modulus), rng.randrange(modulus))
                for _ in range(length)
            )
            proposed = ((1, 0),) * (modulus - 1) + ((0, 1),) * t
            proposed_count = len(_subsequence_sums(proposed, modulus))
            sums = _subsequence_sums(sequence, modulus)
            checked += 1
            pending += 1
            covered.add((modulus, t))
            if _zero_sum_free(sequence, modulus) and len(sums) < proposed_count:
                return {
                    "modulus": modulus,
                    "t": t,
                    "sequence": [list(value) for value in sequence],
                    "subsequence_sum_count": len(sums),
                    "proposed_count": proposed_count,
                }, checked, False
            if pending >= 32:
                state.commit(
                    checked_increment=pending,
                    cursor={
                        "cursor_kind": "few_subsequence_stratified_case",
                        "next_case": checked,
                    },
                    metrics={
                        "coverage_kind": "stratified_random_sequences",
                        "parameter_strata": [
                            list(pair) for pair in sorted(covered)
                        ],
                        "eligible_strata": len(strata),
                    },
                )
                pending = 0
        if pending:
            state.commit(
                checked_increment=pending,
                cursor={
                    "cursor_kind": "few_subsequence_stratified_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": "stratified_random_sequences",
                    "parameter_strata": [
                        list(pair) for pair in sorted(covered)
                    ],
                    "eligible_strata": len(strata),
                },
            )
        return None, state.checked, False

    checked = 0
    for modulus in range(2, max_n + 1):
        elements = list(itertools.product(range(modulus), repeat=2))
        for t in range(modulus):
            length = modulus - 1 + t
            proposed = ((1, 0),) * (modulus - 1) + ((0, 1),) * t
            proposed_count = len(_subsequence_sums(proposed, modulus))
            candidates = (
                tuple(elements[index] for index in indices)
                for indices in itertools.combinations_with_replacement(
                    range(len(elements)), length
                )
            )
            for sequence in candidates:
                checked += 1
                sums = _subsequence_sums(sequence, modulus)
                generic = tuple(tuple(value) for value in sequence)
                if _zero_sum_free(generic, modulus) and len(sums) < proposed_count:
                    return {
                        "modulus": modulus,
                        "t": t,
                        "sequence": [list(value) for value in sequence],
                        "subsequence_sum_count": len(sums),
                        "proposed_count": proposed_count,
                    }, checked, strategy_id == "exact-small"
                if checked >= max_cases:
                    return None, checked, False
    return None, checked, True


def _search_pascal_multiplicity(
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_row = _positive_int(budget, "max_row", 100, minimum=1)
    max_cases = _positive_int(budget, "max_cases", 10_000)
    positions: dict[int, list[list[int]]] = {}
    checked = 0
    for row in range(max_row + 1):
        for column in range(row + 1):
            checked += 1
            value = math.comb(row, column)
            if value != 1:
                positions.setdefault(value, []).append([row, column])
                if len(positions[value]) >= 9:
                    return {
                        "value": value,
                        "multiplicity": len(positions[value]),
                        "positions": positions[value],
                        "targeted_bound": 8,
                    }, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _search_square_pseudoprime(
    budget: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, int, bool]:
    max_root = _positive_int(budget, "max_root", 1_000, minimum=2)
    max_cases = _positive_int(budget, "max_cases", max_root)
    excluded = (1_194_649, 12_327_121)
    checked = 0
    for root in range(3, max_root + 1, 2):
        checked += 1
        value = root * root
        if all(value % divisor for divisor in excluded) and pow(2, value - 1, value) == 1:
            return {
                "root": root,
                "square_pseudoprime": value,
                "factorization": _factor_certificate(value),
            }, checked, True
        if checked >= max_cases:
            return None, checked, False
    return None, checked, True


def _search_sextic_identity(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_base = _positive_int(budget, "max_base", 8)
    max_cases = _positive_int(budget, "max_cases", 10_000)
    if strategy_id != "exact-small":
        pending = 0
        checked = state.checked
        min_target = state.metrics.get("min_target_base")
        max_target = state.metrics.get("max_target_base")
        while checked < max_cases:
            case_index = checked
            rng = _case_rng(seed, case_index, 508)
            target = rng.randint(2, max_base)
            partial = tuple(rng.randint(1, target) for _ in range(4))
            remainder = target**6 - sum(value**6 for value in partial)
            checked += 1
            pending += 1
            min_target = (
                target if min_target is None else min(int(min_target), target)
            )
            max_target = (
                target if max_target is None else max(int(max_target), target)
            )
            if remainder > 0:
                final, exact = sympy.integer_nthroot(remainder, 6)
                if exact and 0 < int(final) <= max_base:
                    return {
                        "left_bases": sorted([*partial, int(final)]),
                        "right_base": target,
                    }, checked, False
            if pending >= 64:
                state.commit(
                    checked_increment=pending,
                    cursor={
                        "cursor_kind": "sextic_power_completion_case",
                        "next_case": checked,
                    },
                    metrics={
                        "coverage_kind": "random_four_plus_exact_sixth_root",
                        "min_target_base": min_target,
                        "max_target_base": max_target,
                    },
                )
                pending = 0
        if pending:
            state.commit(
                checked_increment=pending,
                cursor={
                    "cursor_kind": "sextic_power_completion_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": "random_four_plus_exact_sixth_root",
                    "min_target_base": min_target,
                    "max_target_base": max_target,
                },
            )
        return None, state.checked, False

    bases = range(1, max_base + 1)
    two_sums: dict[int, tuple[int, int]] = {}
    for pair in itertools.combinations_with_replacement(bases, 2):
        two_sums.setdefault(pair[0] ** 6 + pair[1] ** 6, pair)
    checked = 0
    for target in bases:
        target_power = target**6
        for triple in itertools.combinations_with_replacement(bases, 3):
            checked += 1
            remainder = target_power - sum(value**6 for value in triple)
            pair = two_sums.get(remainder)
            if pair is not None:
                left = tuple(sorted(pair + triple))
                return {"left_bases": list(left), "right_base": target}, checked, True
            if checked >= max_cases:
                return None, checked, False
    return None, checked, True


def _search_odd_covering(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_modulus = _positive_int(budget, "max_modulus", 9, minimum=3)
    max_moduli = _positive_int(budget, "max_moduli", 3, minimum=1)
    max_cases = _positive_int(budget, "max_cases", 20_000)
    moduli_pool = list(range(3, max_modulus + 1, 2))
    if strategy_id != "exact-small":
        max_period = _positive_int(
            budget,
            "max_period",
            2_000_000,
        )
        smooth_periods = sorted(
            {
                3**a * 5**b * 7**c
                for a in range(2, 7)
                for b in range(1, 5)
                for c in range(0, 3)
                if 3**a * 5**b * 7**c <= max_period
            }
        )
        families = []
        for period in smooth_periods:
            pool = [
                int(value)
                for value in sympy.divisors(period)
                if 1 < int(value) <= max_modulus
                and int(value) % 2 == 1
            ]
            if len(pool) >= min(8, max_moduli):
                families.append((period, tuple(sorted(pool))))
        if not families:
            return None, state.checked, True
        checked = state.checked
        structure_hashes = {
            str(value)
            for value in state.metrics.get("modulus_set_hashes", [])
        }
        duplicate_structures = int(
            state.metrics.get("duplicate_modulus_sets", 0)
        )
        periods = {
            int(value)
            for value in state.metrics.get("period_strata", [])
        }
        best_uncovered = state.metrics.get("best_uncovered_residues")
        while checked < max_cases:
            case_index = checked
            period, pool = families[
                (case_index + abs(int(seed))) % len(families)
            ]
            count = min(
                max_moduli,
                max(8, 8 + case_index % max(1, max_moduli - 7)),
                len(pool),
            )
            local_position = case_index // len(families)
            stride = 1 + 2 * (local_position % max(1, len(pool) // 2))
            while math.gcd(stride, len(pool)) != 1:
                stride += 2
            start = (
                local_position * 17 + abs(int(seed))
            ) % len(pool)
            indices = []
            position = start
            while len(indices) < count:
                if position not in indices:
                    indices.append(position)
                position = (position + stride) % len(pool)
            moduli = tuple(sorted(pool[index] for index in indices))
            structure_hash = ",".join(map(str, moduli))
            if structure_hash in structure_hashes:
                duplicate_structures += 1
            structure_hashes.add(structure_hash)
            periods.add(period)
            rng = _case_rng(seed, case_index, 491)
            residues = [
                rng.randrange(modulus) for modulus in moduli
            ]
            class_bits: list[list[int]] = []
            for modulus in moduli:
                residue_bits = []
                for residue in range(modulus):
                    bits = 0
                    for value in range(residue, period, modulus):
                        bits |= 1 << value
                    residue_bits.append(bits)
                class_bits.append(residue_bits)
            universe = (1 << period) - 1
            for _ in range(4):
                changed = False
                for index, modulus in enumerate(moduli):
                    other_cover = 0
                    for other_index, other_residue in enumerate(residues):
                        if other_index != index:
                            other_cover |= class_bits[other_index][other_residue]
                    best_residue = max(
                        range(modulus),
                        key=lambda residue: (
                            other_cover
                            | class_bits[index][residue]
                        ).bit_count(),
                    )
                    changed |= best_residue != residues[index]
                    residues[index] = best_residue
                if not changed:
                    break
            covered = 0
            for index, residue in enumerate(residues):
                covered |= class_bits[index][residue]
            uncovered = period - covered.bit_count()
            checked += 1
            best_uncovered = (
                uncovered
                if best_uncovered is None
                else min(int(best_uncovered), uncovered)
            )
            if uncovered == 0:
                return {
                    "moduli": list(moduli),
                    "residues": residues,
                    "period": period,
                }, checked, False
            state.commit(
                checked_increment=1,
                cursor={
                    "cursor_kind": "odd_covering_smooth_period_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": (
                        "smooth_period_large_modulus_multistart"
                    ),
                    "period_strata": sorted(periods),
                    "modulus_counts": sorted(
                        {
                            *map(
                                int,
                                state.metrics.get("modulus_counts", []),
                            ),
                            count,
                        }
                    ),
                    "modulus_set_hashes": sorted(structure_hashes)[-256:],
                    "duplicate_modulus_sets": duplicate_structures,
                    "best_uncovered_residues": best_uncovered,
                    "candidate_check": "exact_complete_lcm_period_bitset",
                    "search_completeness": (
                        "multistart_coordinate_descent_not_exhaustive"
                    ),
                },
            )
        return None, state.checked, False

    checked = 0
    for count in range(1, min(max_moduli, len(moduli_pool)) + 1):
        for moduli in itertools.combinations(moduli_pool, count):
            period = math.lcm(*moduli)
            for residues in itertools.product(*(range(modulus) for modulus in moduli)):
                checked += 1
                if all(
                    any(value % modulus == residue for modulus, residue in zip(moduli, residues))
                    for value in range(period)
                ):
                    return {
                        "moduli": list(moduli),
                        "residues": list(residues),
                        "period": period,
                    }, checked, True
                if checked >= max_cases:
                    return None, checked, False
    return None, checked, True


def _search_equal_power_sums(
    budget: Mapping[str, Any],
    *,
    strategy_id: str,
    seed: int,
    state: _SearchProgressState,
) -> tuple[dict[str, Any] | None, int, bool]:
    max_power = _positive_int(budget, "max_power", 5, minimum=3)
    max_base = _positive_int(budget, "max_base", 8)
    max_cases = _positive_int(budget, "max_cases", 20_000)
    if strategy_id != "exact-small":
        configurations = [
            (power, left_terms, right_terms)
            for power in range(3, max_power + 1)
            for left_terms in range(1, power - 1)
            for right_terms in range(1, power - left_terms)
            if left_terms + right_terms <= max_base
        ]
        if not configurations:
            return None, state.checked, True
        covered_powers = {
            int(value) for value in state.metrics.get("powers", [])
        }
        covered_shapes = {
            tuple(int(value) for value in shape)
            for shape in state.metrics.get("term_shapes", [])
        }
        pending = 0
        checked = state.checked
        while checked < max_cases:
            case_index = checked
            power, left_terms, right_terms = configurations[
                (case_index + abs(int(seed))) % len(configurations)
            ]
            rng = _case_rng(seed, case_index, 58)
            chosen = rng.sample(
                range(1, max_base + 1),
                left_terms + max(0, right_terms - 1),
            )
            left = tuple(sorted(chosen[:left_terms]))
            right_partial = tuple(sorted(chosen[left_terms:]))
            remainder = (
                sum(value**power for value in left)
                - sum(value**power for value in right_partial)
            )
            checked += 1
            pending += 1
            covered_powers.add(power)
            covered_shapes.add((left_terms, right_terms))
            if remainder > 0:
                final, exact = sympy.integer_nthroot(remainder, power)
                final = int(final)
                if (
                    exact
                    and 0 < final <= max_base
                    and final not in set(left)
                    and final not in set(right_partial)
                ):
                    right = tuple(sorted((*right_partial, final)))
                    return {
                        "power": power,
                        "left_bases": list(left),
                        "right_bases": list(right),
                    }, checked, False
            if pending >= 32:
                state.commit(
                    checked_increment=pending,
                    cursor={
                        "cursor_kind": "equal_power_completion_case",
                        "next_case": checked,
                    },
                    metrics={
                        "coverage_kind": "random_terms_plus_exact_power_root",
                        "powers": sorted(covered_powers),
                        "term_shapes": [
                            list(shape) for shape in sorted(covered_shapes)
                        ],
                    },
                )
                pending = 0
        if pending:
            state.commit(
                checked_increment=pending,
                cursor={
                    "cursor_kind": "equal_power_completion_case",
                    "next_case": checked,
                },
                metrics={
                    "coverage_kind": "random_terms_plus_exact_power_root",
                    "powers": sorted(covered_powers),
                    "term_shapes": [
                        list(shape) for shape in sorted(covered_shapes)
                    ],
                },
            )
        return None, state.checked, False

    checked = 0
    bases = range(1, max_base + 1)
    for power in range(3, max_power + 1):
        sums_by_terms: dict[int, dict[int, tuple[int, ...]]] = {}
        for terms in range(1, power - 1):
            table: dict[int, tuple[int, ...]] = {}
            for values in itertools.combinations(bases, terms):
                table.setdefault(sum(value**power for value in values), values)
            sums_by_terms[terms] = table
        for left_terms in range(1, power - 1):
            for right_terms in range(1, power - left_terms):
                right = sums_by_terms[right_terms]
                for total, left_values in sums_by_terms[left_terms].items():
                    checked += 1
                    right_values = right.get(total)
                    if right_values is not None and set(left_values).isdisjoint(right_values):
                        return {
                            "power": power,
                            "left_bases": list(left_values),
                            "right_bases": list(right_values),
                        }, checked, True
                    if checked >= max_cases:
                        return None, checked, False
    return None, checked, True


def _verify_candidate(problem_id: str, candidate: Mapping[str, Any]) -> bool:
    if problem_id in {
        "unsolvedmath-kou-21.87",
        "unsolvedmath-kou-21.88",
        "unsolvedmath-kou-21.25",
        "unsolvedmath-kou-21.59",
        "unsolvedmath-kou-21.137",
        "unsolvedmath-kou-21.35",
        "unsolvedmath-kou-21.113",
        "unsolvedmath-kou-21.134",
        "unsolvedmath-kou-21.135",
    }:
        return _gap_verify_candidate(problem_id, candidate)
    if problem_id == "unsolvedmath-kou-21.2":
        return _verify_kou_21_2(candidate)
    if problem_id == "unsolvedmath-kou-21.130":
        subset = tuple(int(value) for value in candidate["subset"])
        return not _has_distinct_adjacent_sum_cycle(int(candidate["cyclic_modulus"]), subset)
    if problem_id == "unsolvedmath-kou-21.115":
        modulus = int(candidate["cyclic_modulus"])
        cosets = [tuple(int(value) for value in coset) for coset in candidate["cosets"]]
        if modulus < 2 or not cosets or len(set(cosets)) != len(cosets):
            return False
        for coset in cosets:
            if not coset or len(set(coset)) != len(coset):
                return False
            if any(value < 0 or value >= modulus for value in coset):
                return False
            representative = coset[0]
            subgroup = {(value - representative) % modulus for value in coset}
            if 0 not in subgroup or any(
                (left + right) % modulus not in subgroup
                for left in subgroup
                for right in subgroup
            ):
                return False
            if set(coset) != {
                (representative + value) % modulus for value in subgroup
            }:
                return False
        union = set().union(*(set(coset) for coset in cosets))
        complement = modulus - len(union)
        return 0 < complement and complement * (2 ** len(cosets)) < modulus
    if problem_id == "unsolvedmath-opg-37396":
        q, p = int(candidate["q"]), int(candidate["p"])
        return isprime(q) and q > 3 and p == 16 * q**4 + 1 and isprime(p) and not _is_primitive_root_3(p)
    if (
        problem_id
        == "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45"
    ):
        field_prime = int(candidate.get("field_prime", 0))
        rank = int(candidate.get("rank", 0))
        raw_bases = candidate.get("labelled_bases", ())
        if not isprime(field_prime) or rank < 1 or len(raw_bases) != rank:
            return False
        bases = tuple(
            tuple(
                tuple(map(int, vector))
                for vector in base
            )
            for base in raw_bases
        )
        if (
            any(len(base) != rank for base in bases)
            or any(
                len(vector) != rank
                for base in bases
                for vector in base
            )
            or any(
                _prime_field_rank(base, field_prime) != rank
                for base in bases
            )
        ):
            return False
        solved, _, arrangement = _rota_transversal_decomposition(
            bases,
            field_prime,
            node_limit=None,
        )
        return solved is False and arrangement is None
    if problem_id == "unsolvedmath-opg-37413":
        value = int(candidate["n"])
        return bool(isprime(value)) != _alexa_test(value)
    if problem_id == "unsolvedmath-opg-37411":
        value = int(candidate["n"])
        return bool(isprime(value)) != _giuga_test(value)
    if problem_id == "unsolvedmath-kou-21.89":
        n = int(candidate["n"])
        if n <= 39:
            return False
        partitions = [1]
        for value in range(1, n + 1):
            partitions.append(_partition_number(partitions, value))
        partition = partitions[n]
        return (
            int(candidate["partition_number"]) == partition
            and int(candidate["factorial_mod_partition"]) == 0
            and _partition_divides_factorial_by_valuations(n, partition)
        )
    if problem_id == "unsolvedmath-opg-55810":
        n, divisor = int(candidate["index"]), int(candidate["square_divisor"])
        return divisor > 1 and (pow(2, 1 << n, divisor * divisor) + 1) % (divisor * divisor) == 0
    if problem_id == "unsolvedmath-opg-59976":
        p, divisor = int(candidate["prime_exponent"]), int(candidate["square_divisor"])
        return isprime(p) and divisor > 1 and pow(2, p, divisor * divisor) == 1
    if problem_id == "unsolvedmath-opg-822":
        p = int(candidate["prime"])
        index = p - int(sympy.legendre_symbol(p, 5))
        return isprime(p) and p > 5 and _fib_pair_mod(index, p * p)[0] == 0
    if problem_id == "unsolvedmath-nt-035":
        value = int(candidate["n"])
        factorization = {
            int(prime): int(exponent)
            for prime, exponent in dict(
                candidate.get("factorization") or {}
            ).items()
        }
        if (
            len(factorization) < 2
            or any(
                exponent != 1 or not isprime(prime)
                for prime, exponent in factorization.items()
            )
            or math.prod(factorization) != value
        ):
            return False
        phi = math.prod(prime - 1 for prime in factorization)
        return (
            int(candidate.get("phi", phi)) == phi
            and (value - 1) % phi == 0
        )
    if problem_id == "unsolvedmath-geo-025":
        dimension = int(candidate.get("dimension", 0))
        vertices = tuple(
            tuple(map(int, vertex))
            for vertex in candidate.get("vertices", ())
        )
        data = _exact_cs_polytope_data(
            vertices,
            dimension,
            subset_limit=None,
            cross_check=True,
        )
        if data is None:
            return False
        face_vector = tuple(map(int, candidate.get("face_vector", ())))
        face_count = int(candidate.get("nonempty_face_count", -1))
        return (
            face_vector == data["face_vector"]
            and face_count == data["nonempty_face_count"]
            and sum(face_vector) == face_count
            and face_count < 3**dimension
            and candidate.get("face_convention")
            == "includes_polytope_excludes_empty_face"
        )
    if problem_id in {"unsolvedmath-nt-059", "unsolvedmath-opg-37404"}:
        value = int(candidate["n"])
        lemoine = problem_id == "unsolvedmath-nt-059"
        flags, primes = _prime_sieve(value)
        for prime in primes:
            if prime == 2 or prime >= value:
                continue
            remainder = value - prime
            if lemoine and remainder % 2 == 0 and flags[remainder // 2]:
                return False
            if not lemoine and _is_semiprime(remainder, odd=True):
                return False
        return True
    if problem_id == "unsolvedmath-nt-087":
        value = int(candidate["n"])
        return bool(isprime(value)) != _agoh_test(value)
    if problem_id == "unsolvedmath-opg-791":
        variable = symbols("x")
        polynomial = Poly.from_list(list(candidate["coefficients"]), gens=variable, domain=sympy.QQ)
        roots = polynomial.all_roots()
        if len(set(roots)) != 4 or not all(bool(root.is_Rational) for root in roots):
            return False
        current = polynomial
        while current.degree() > 1:
            current = current.diff()
            if not all(bool(root.is_Rational) for root in current.all_roots()):
                return False
        return True
    if problem_id == "unsolvedmath-opg-563":
        modulus = int(candidate["modulus"])
        sequence = tuple(tuple(int(x) for x in value) for value in candidate["sequence"])
        dimension = int(candidate["dimension"])
        return len(sequence) == dimension * (modulus - 1) + 1 and _zero_sum_free(sequence, modulus)
    if problem_id == "unsolvedmath-hl-b":
        x, y = int(candidate["x"]), int(candidate["y"])
        return int(sympy.primepi(x + y)) > (
            int(sympy.primepi(x)) + int(sympy.primepi(y))
        )
    if problem_id == "unsolvedmath-opg-416":
        speeds = tuple(int(value) for value in candidate["speeds"])
        runner = int(candidate["runner_index"])
        return len(set(speeds)) == len(speeds) and not _runner_has_lonely_time(speeds, runner)
    if problem_id == "unsolvedmath-opg-511":
        return _internally_verify_bpsw_candidate(candidate)
    if problem_id == "unsolvedmath-opg-156":
        modulus = int(candidate["modulus"])
        t = int(candidate["t"])
        sequence = tuple(
            tuple(int(coordinate) for coordinate in value)
            for value in candidate["sequence"]
        )
        if (
            modulus < 2
            or not 0 <= t < modulus
            or len(sequence) != modulus - 1 + t
            or any(
                len(value) != 2
                or any(coordinate < 0 or coordinate >= modulus for coordinate in value)
                for value in sequence
            )
        ):
            return False
        proposed = ((1, 0),) * (modulus - 1) + ((0, 1),) * t
        actual_count = len(_subsequence_sums(sequence, modulus))
        proposed_count = len(_subsequence_sums(proposed, modulus))
        return (
            _zero_sum_free(sequence, modulus)
            and actual_count < proposed_count
            and int(candidate["subsequence_sum_count"]) == actual_count
            and int(candidate["proposed_count"]) == proposed_count
        )
    if problem_id == "unsolvedmath-opg-60034":
        value = int(candidate["value"])
        positions = [
            (int(position[0]), int(position[1]))
            for position in candidate["positions"]
        ]
        return (
            value != 1
            and len(set(positions)) >= 9
            and all(0 <= column <= row for row, column in positions)
            and all(math.comb(row, column) == value for row, column in positions)
        )
    if problem_id == "unsolvedmath-guy-a12a":
        root = int(candidate["root"])
        value = int(candidate["square_pseudoprime"])
        excluded = (1_194_649, 12_327_121)
        return (
            root > 1
            and root % 2 == 1
            and value == root * root
            and not isprime(value)
            and pow(2, value - 1, value) == 1
            and all(value % divisor for divisor in excluded)
        )
    if problem_id == "unsolvedmath-opg-508":
        left = tuple(int(value) for value in candidate["left_bases"])
        right = int(candidate["right_base"])
        return (
            len(left) == 5
            and right > 0
            and all(value > 0 for value in left)
            and sum(value**6 for value in left) == right**6
        )
    if problem_id == "unsolvedmath-opg-491":
        moduli = tuple(int(value) for value in candidate["moduli"])
        residues = tuple(int(value) for value in candidate["residues"])
        if (
            not moduli
            or len(moduli) != len(residues)
            or len(set(moduli)) != len(moduli)
            or any(modulus <= 1 or modulus % 2 == 0 for modulus in moduli)
            or any(
                residue < 0 or residue >= modulus
                for modulus, residue in zip(moduli, residues)
            )
        ):
            return False
        period = math.lcm(*moduli)
        return all(
            any(
                value % modulus == residue
                for modulus, residue in zip(moduli, residues)
            )
            for value in range(period)
        )
    if problem_id == "unsolvedmath-nt-058":
        power = int(candidate["power"])
        left = tuple(int(value) for value in candidate["left_bases"])
        right = tuple(int(value) for value in candidate["right_bases"])
        return (
            power >= 3
            and left
            and right
            and len(left) + len(right) < power
            and all(value > 0 for value in left + right)
            and len(set(left)) == len(left)
            and len(set(right)) == len(right)
            and set(left).isdisjoint(right)
            and sum(value**power for value in left)
            == sum(value**power for value in right)
        )
    return False


SearchResult = tuple[dict[str, Any] | None, int, bool]


def _execute(
    problem_id: str,
    *,
    strategy_id: str,
    budget: Mapping[str, Any],
    seed: int,
    state: _SearchProgressState | None = None,
) -> SearchResult:
    if problem_id in {
        "unsolvedmath-kou-21.87",
        "unsolvedmath-kou-21.88",
        "unsolvedmath-kou-21.25",
        "unsolvedmath-kou-21.59",
        "unsolvedmath-kou-21.137",
        "unsolvedmath-kou-21.35",
        "unsolvedmath-kou-21.113",
        "unsolvedmath-kou-21.134",
        "unsolvedmath-kou-21.135",
    }:
        return _gap_group_scan(
            problem_id,
            budget,
            strategy_id=strategy_id,
            state=state,
        )
    if problem_id == "unsolvedmath-kou-21.2":
        return _search_kou_21_2(budget)
    if problem_id == "unsolvedmath-kou-21.130":
        return _search_kou_21_130(budget, strategy_id=strategy_id, seed=seed)
    if problem_id == "unsolvedmath-kou-21.115":
        return _search_kou_21_115(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-37396":
        return _search_primitive_root(
            budget,
            strategy_id=strategy_id,
            state=state,
        )
    if (
        problem_id
        == "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45"
    ):
        return _search_rota_basis(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-37413":
        return _search_predicate_mismatch(
            budget,
            minimum=8,
            predicate=_alexa_test,
            certificate=lambda value: {
                "test_value": _alexa_test(value),
                "term_count": _integer_cuberoot(value) // 2,
            },
        )
    if problem_id == "unsolvedmath-opg-37411":
        return _search_predicate_mismatch(
            budget,
            minimum=2,
            predicate=_giuga_test,
            certificate=lambda value: {"power_sum_mod_n": sum(pow(i, value - 1, value) for i in range(1, value)) % value},
        )
    if problem_id == "unsolvedmath-kou-21.89":
        return _search_partition_divisor(budget, state=state)
    if problem_id == "unsolvedmath-opg-55810":
        return _search_fermat_square_factor(budget)
    if problem_id == "unsolvedmath-opg-59976":
        return _search_mersenne_square_factor(budget)
    if problem_id == "unsolvedmath-opg-822":
        return _search_wall_sun_sun(budget, state=state)
    if problem_id == "unsolvedmath-nt-035":
        return _search_lehmer(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-geo-025":
        return _search_kalai_three_power_d(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-nt-059":
        return _search_prime_semiprime(
            budget,
            lemoine=True,
            state=state,
        )
    if problem_id == "unsolvedmath-nt-087":
        return _search_predicate_mismatch(
            budget,
            minimum=2,
            predicate=_agoh_test,
            certificate=lambda value: {"n_times_bernoulli": str(sympy.Rational(value) * bernoulli(value - 1))},
        )
    if problem_id == "unsolvedmath-opg-37404":
        return _search_prime_semiprime(
            budget,
            lemoine=False,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-791":
        return _search_quartic(
            budget,
            strategy_id=strategy_id,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-563":
        return _search_davenport(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-hl-b":
        return _search_hardy_littlewood_b(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-416":
        return _search_lonely_runner(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-511":
        return _search_bpsw_counterexample(
            budget,
            strategy_id=strategy_id,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-156":
        return _search_few_subsequence_sums(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-60034":
        return _search_pascal_multiplicity(budget)
    if problem_id == "unsolvedmath-guy-a12a":
        return _search_square_pseudoprime(budget)
    if problem_id == "unsolvedmath-opg-508":
        return _search_sextic_identity(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-opg-491":
        return _search_odd_covering(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    if problem_id == "unsolvedmath-nt-058":
        return _search_equal_power_sums(
            budget,
            strategy_id=strategy_id,
            seed=seed,
            state=state,
        )
    raise KeyError(problem_id)


def run_second_batch_arithmetic_search(
    problem_id: str,
    *,
    strategy_id: str,
    budget: Any,
    seed: int,
    checkpoint: Mapping[str, Any] | None = None,
    progress: Callable[[Mapping[str, Any], int], Any] | None = None,
) -> dict[str, Any]:
    """Run one bounded, deterministic second-batch counterexample search."""

    try:
        spec = _SPECS_BY_ID[problem_id]
    except KeyError as exc:
        raise KeyError(f"second-batch arithmetic problem is not registered: {problem_id}") from exc
    requested_strategy_id = strategy_id
    if strategy_id == "screen-exact":
        effective_strategy_id = "exact-small"
    elif strategy_id == "deep-diversified":
        alternatives = [
            value for value in spec["strategies"] if value != "exact-small"
        ]
        effective_strategy_id = (
            alternatives[abs(int(seed)) % len(alternatives)]
            if alternatives
            else "exact-small"
        )
    else:
        effective_strategy_id = strategy_id
    if effective_strategy_id not in spec["strategies"]:
        raise ValueError(
            f"strategy '{strategy_id}' is not registered for {problem_id}; "
            f"choose one of {spec['strategies']}, screen-exact, or deep-diversified"
        )
    effective_seed = int(seed) if effective_strategy_id == "multistart" else 0
    normalized_budget = {**spec["screen_bounds"], **_budget_dict(budget)}
    state = _SearchProgressState(
        problem_id=problem_id,
        strategy_id=effective_strategy_id,
        checkpoint=checkpoint,
        progress=progress,
        resumable=problem_id in _RESUMABLE_PROBLEMS,
    )
    candidate: dict[str, Any] | None = None
    checked = state.checked
    exhausted = False
    verified = False
    timed_out = False
    engine_error: str | None = None
    search_completed = False
    raw_time_limit = normalized_budget.get("time_seconds")
    time_limit = None if raw_time_limit is None else float(raw_time_limit)
    try:
        with _bounded_runtime(time_limit):
            candidate, checked, exhausted = _execute(
                problem_id,
                strategy_id=effective_strategy_id,
                budget=normalized_budget,
                seed=effective_seed,
                state=state,
            )
            state.checked = checked
            search_completed = True
            verified = candidate is not None and _verify_candidate(
                problem_id,
                candidate,
            )
    except _SearchTimeLimit:
        timed_out = True
        checked = state.checked
    except RuntimeError as exc:
        engine_error = str(exc)
        checked = state.checked

    if timed_out:
        outcome = "inconclusive"
        stop_reason = "time_budget_exhausted"
        candidate = None
        exhausted = False
    elif engine_error is not None:
        outcome = "inconclusive"
        stop_reason = "search_engine_error"
        candidate = None
        exhausted = False
    elif candidate is not None and not verified:
        outcome = "inconclusive"
        stop_reason = "candidate_failed_internal_verification"
        candidate = None
    elif candidate is not None:
        candidate = {
            **candidate,
            "internal_verification": {
                "status": "passed",
                "verifier": f"{spec['executor_id']}.same_module_replay",
                "independence": "internal_only_external_campaign_verification_required",
            },
        }
        outcome = "candidate_counterexample"
        stop_reason = "candidate_passed_internal_verification"
    elif exhausted:
        outcome = "no_counterexample_within_bound"
        stop_reason = "bounded_scope_exhausted"
    else:
        outcome = "inconclusive"
        stop_reason = "case_budget_exhausted"
    phase = (
        "time_budget_exhausted"
        if timed_out
        else "search_engine_error"
        if engine_error is not None
        else "complete"
    )
    state.checked = checked
    next_checkpoint = {
        **state.final_cursor(
            phase=phase,
            exhausted=exhausted,
            search_completed=search_completed,
        ),
        "strategy_id": requested_strategy_id,
        "launch_seed": effective_seed,
        "completed_budget": normalized_budget,
    }
    payload = {
        "outcome": outcome,
        "candidate": candidate,
        "checked_cases": checked,
        "stop_reason": stop_reason,
        "checkpoint": next_checkpoint,
        "model_contract": spec["model_contract"],
        "tool_versions": _tool_versions(),
        "executor_id": spec["executor_id"],
        "version": spec["version"],
        "strategy_id": requested_strategy_id,
        "effective_strategy_id": effective_strategy_id,
        "budget": normalized_budget,
        "metrics": dict(state.metrics),
    }
    if engine_error is not None:
        payload["engine_error"] = engine_error
    if progress is not None:
        progress(dict(next_checkpoint), checked)
    return payload


__all__ = [
    "SECOND_BATCH_ARITHMETIC_SPECS",
    "run_second_batch_arithmetic_search",
]
