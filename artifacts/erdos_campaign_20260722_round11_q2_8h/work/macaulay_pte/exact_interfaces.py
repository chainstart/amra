#!/usr/bin/env python3
"""Exact finite audits for the Round 11 #776/#256 interfaces.

The all-parameter arguments are written in REPORT.md.  This program only
checks the integer identities, the Galois/plateau interfaces, selected
rank-coupled traces, and small hostile controls for the prime-split
cyclotomic theorem.  No finite range is used as an all-parameter proof.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, combinations_with_replacement
from math import comb


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(high, lower) <= remaining:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower) <= remaining:
                low = middle
            else:
                high = middle
        upper = low
        if cap is not None:
            upper = min(upper, cap - 1)
            while upper >= lower and comb(upper, lower) > remaining:
                upper -= 1
        if upper < lower:
            continue
        result.append((upper, lower))
        remaining -= comb(upper, lower)
        cap = upper
    if remaining:
        raise AssertionError((number, rank, result, remaining))
    return result


def upper_raise(number: int, rank: int) -> int:
    return sum(comb(upper, lower + 1)
               for upper, lower in canonical(number, rank))


def lower_shadow(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1)
               for upper, lower in canonical(number, rank))


def suspension(number: int, rank: int) -> int:
    """Diagonal Macaulay suspension: increment both binomial indices."""
    return sum(comb(upper + 1, lower + 1)
               for upper, lower in canonical(number, rank))


def canonical_value(expansion: list[tuple[int, int]]) -> int:
    return sum(comb(upper, lower) for upper, lower in expansion)


def _lazy_add(
    expansion: list[tuple[int, int]],
    shift: int,
    rank: int,
    increment: int,
) -> None:
    """Add to a lazily rank-shifted canonical expansion, in place.

    An entry ``(a, j)`` denotes C(a, j+shift).  For a canonical term
    C(a,i), the existing leading term survives addition by ``increment``
    exactly while ``tail+increment < C(a,i-1)``.  Thus only the carry
    suffix has to be expanded again.  This is an exact acceleration, not a
    heuristic or a replacement recurrence.
    """
    tail = 0
    for index in range(len(expansion) - 1, -1, -1):
        upper, stored_lower = expansion[index]
        lower = stored_lower + shift
        term = comb(upper, lower)
        tail += term
        below = tail - term
        if lower > 1 and below + increment < comb(upper, lower - 1):
            suffix = canonical(below + increment, lower - 1)
            del expansion[index + 1:]
            expansion.extend((a, i - shift) for a, i in suffix)
            return
    suffix = canonical(tail + increment, rank)
    expansion.clear()
    expansion.extend((a, i - shift) for a, i in suffix)


def lazy_defect(m: int) -> tuple[int, list[tuple[int, int]]]:
    """Evaluate d^[M]_3 by the exact lazy-carry form of (10a)."""
    if m < 5:
        raise ValueError(m)
    expansion: list[tuple[int, int]] = []
    shift = 0
    for q in range(m - 2, 3, -1):
        # Apply KK_q: every lower index drops by one.  Rank-one terms
        # become C(a,0)=1 and are folded into the additive constant.
        shift -= 1
        rank_zero_terms = 0
        while expansion and expansion[-1][1] + shift <= 0:
            _, stored_lower = expansion.pop()
            assert stored_lower + shift == 0
            rank_zero_terms += 1
        _lazy_add(expansion, shift, q - 1, m - 3 + rank_zero_terms)
    actual = [(upper, stored_lower + shift)
              for upper, stored_lower in expansion]
    return canonical_value(actual), actual


def macaulay_self_test(box: int) -> dict[str, object]:
    identity_checks = 0
    plateau_checks = 0
    galois_checks = 0
    for rank in range(1, 9):
        for x in range(box + 1):
            # Pascal and canonical uniqueness give S_p(x)=x+U_p(x).
            assert suspension(x, rank) == x + upper_raise(x, rank)
            # Incrementing both indices commutes with upper raising.
            assert upper_raise(suspension(x, rank), rank + 1) == suspension(
                upper_raise(x, rank), rank + 1
            )
            # The general plateau escape lemma has cost at most rank+1.
            assert upper_raise(x + rank + 1, rank) >= upper_raise(x, rank) + 1
            identity_checks += 2
            plateau_checks += 1
            for y in range(min(box, 40) + 1):
                assert ((upper_raise(x, rank) >= y)
                        == (x >= lower_shadow(y, rank + 1)))
                galois_checks += 1
    # The size hypothesis in the propagation lemma cannot simply be dropped:
    # at p=4, r=2, x=22 one has z=U_4(x)-r=6 but U_5(z+r)=U_5(z)=1.
    plateau_counterexample = {
        "rank": 4,
        "increment": 2,
        "x": 22,
        "z": upper_raise(22, 4) - 2,
        "upper_z": upper_raise(upper_raise(22, 4) - 2, 5),
        "upper_z_plus_increment": upper_raise(upper_raise(22, 4), 5),
    }
    assert plateau_counterexample == {
        "rank": 4,
        "increment": 2,
        "x": 22,
        "z": 6,
        "upper_z": 1,
        "upper_z_plus_increment": 1,
    }
    return {
        "suspension_identity_and_commutation_checks": identity_checks,
        "plateau_escape_checks": plateau_checks,
        "galois_checks": galois_checks,
        "small_increment_plateau_counterexample": plateau_counterexample,
    }


def c_sequence(r: int) -> dict[int, int]:
    n = r + 5
    value = comb(n - 1, 3) + comb(n - 2, 2)
    result = {3: value}
    for rank in range(3, n - 2):
        value = upper_raise(value, rank) - r
        if value < 0:
            raise AssertionError(("negative_candidate", r, rank + 1, value))
        result[rank + 1] = value
    return result


def rank_coupled_row(r: int) -> dict[str, int | bool]:
    left = c_sequence(r)
    right = c_sequence(r + 1)
    safe_last = r - 2
    comparisons: list[tuple[int, int]] = []
    propagation_checks = 0
    for rank in range(3, safe_last + 1):
        gap = right[rank + 1] - suspension(left[rank], rank)
        comparisons.append((rank, gap))
        if gap >= 0 and rank < safe_last:
            # Here r >= rank+2, so the all-parameter plateau lemma proves
            # propagation.  We also audit the exact integers on this row.
            assert right[rank + 2] >= suspension(left[rank + 1], rank + 1)
            propagation_checks += 1
    suffix_start = safe_last + 1
    for rank, gap in reversed(comparisons):
        if gap >= 0:
            suffix_start = rank
        else:
            break
    return {
        "r": r,
        "candidate_endpoint": left[r + 3],
        "safe_propagation_last_rank": safe_last,
        "observed_domination_suffix_start": suffix_start,
        "suffix_seed_gap": dict(comparisons).get(suffix_start, 0),
        "preceding_gap": dict(comparisons).get(suffix_start - 1, 0),
        "propagation_checks": propagation_checks,
        "finite_scope_only": True,
    }


def reverse_top_no_go(max_r: int = 300) -> dict[str, object]:
    for r in range(2, max_r + 1):
        left = lower_shadow(r, r + 3)
        right = lower_shadow(r + 1, r + 4)
        assert left == r * (r + 7) // 2
        assert right == (r * r + 9 * r + 8) // 2
        assert right - suspension(left, r + 2) == 4
    return {
        "verified_range": [2, max_r],
        "exact_symbolic_formula_in_report":
            "b_(r+1,r+3)-S_(r+2)(b_(r,r+2))=4",
        "finite_checks": max_r - 1,
    }


def defect_tail_reduction(max_m: int = 300) -> dict[str, object]:
    """Audit the exact q=3-to-end reduction and its constant 28.

    This checks the endpoint equivalence, finite instances of the single
    sufficient target d_3 <= binom(M-1,3)+28, and finite instances of the
    separately proved all-M diagonal defect domination.  The finite range is
    not a proof of the scalar target for all M.
    """
    maximum_slack_defect = -1
    maximum_slack_defect_at = 0
    branch_checks = 0
    endpoint_equivalence_checks = 0
    aligned_defect_checks = 0
    previous_defects = {6: 0}
    for q in range(6, 3, -1):
        previous_defects[q - 1] = 5 + lower_shadow(previous_defects[q], q)
    for m in range(9, max_m + 1):
        r = m - 3
        defects = {m - 2: 0}
        for q in range(m - 2, 3, -1):
            assert defects[q] <= comb(m, q)
            branch_checks += 1
            defects[q - 1] = r + lower_shadow(defects[q], q)
        assert defects[3] <= comb(m, 3)
        branch_checks += 1
        for q in range(4, m - 3):
            assert defects[q] <= suspension(previous_defects[q - 1], q - 1)
            aligned_defect_checks += 1

        slack = comb(m, 3) - defects[3]
        raised_slack = upper_raise(slack, m - 3)
        penultimate = comb(m, 2) + raised_slack + 3
        endpoint = upper_raise(penultimate, m - 1) - r
        quadratic_threshold = comb(m - 1, 2) - 28
        scalar_target = comb(m - 1, 3) + 28

        assert lower_shadow(m - 9, m - 2) == quadratic_threshold
        assert ((endpoint >= 0) == (slack >= quadratic_threshold))
        assert ((slack >= quadratic_threshold)
                == (defects[3] <= scalar_target))
        assert defects[3] <= scalar_target
        lazy_value, lazy_expansion = lazy_defect(m)
        assert lazy_value == defects[3]
        assert lazy_expansion == canonical(defects[3], 3)
        endpoint_equivalence_checks += 1
        slack_defect = comb(m - 1, 2) - slack
        if slack_defect > maximum_slack_defect:
            maximum_slack_defect = slack_defect
            maximum_slack_defect_at = m
        previous_defects = defects
    return {
        "verified_m_range": [9, max_m],
        "branch_no_borrow_checks": branch_checks,
        "endpoint_equivalence_checks": endpoint_equivalence_checks,
        "all_M_diagonal_defect_domination_checks": aligned_defect_checks,
        "quadratic_threshold": "binom(M-1,2)-28",
        "single_sufficient_target": "d_3<=binom(M-1,3)+28",
        "maximum_observed_d3_excess_over_binom_Mminus1_3":
            maximum_slack_defect,
        "maximum_first_attained_at_m": maximum_slack_defect_at,
        "lazy_carry_equivalence_checks": max_m - 8,
        "finite_scope_only": True,
    }


def coefficients(exponents: tuple[int, ...]) -> list[int]:
    values = [1]
    for exponent in exponents:
        updated = values + [0] * exponent
        for index, value in enumerate(values):
            updated[index + exponent] -= value
        values = updated
    return values


def energy(exponents: tuple[int, ...]) -> int:
    return sum(value * value for value in coefficients(exponents))


def cyclic_binomial_product(residues: list[int], modulus: int) -> list[int]:
    values = [0] * modulus
    values[0] = 1
    for residue in residues:
        updated = values.copy()
        for index, value in enumerate(values):
            updated[(index + residue) % modulus] -= value
        values = updated
    return values


def primes_through(limit: int) -> list[int]:
    result = []
    for candidate in range(2, limit + 1):
        if all(candidate % divisor for divisor in range(2, int(candidate**0.5) + 1)):
            result.append(candidate)
    return result


def valuation(number: int, prime: int) -> int:
    result = 0
    while number % prime == 0:
        number //= prime
        result += 1
    return result


def half_split_scan(max_exponent: int) -> dict[str, object]:
    tested = 0
    forbidden_low_energy = 0
    allowed_two_support_controls = 0
    controls: list[dict[str, object]] = []
    for n in (4, 6):
        m = n // 2
        for values in combinations(range(1, max_exponent + 1), n):
            e = energy(values)
            for prime in primes_through(max_exponent):
                if sum(value % prime == 0 for value in values) != m:
                    continue
                tested += 1
                outside = [value % prime for value in values if value % prime]
                group_ring = cyclic_binomial_product(outside, prime)
                support = [index for index, value in enumerate(group_ring) if value]
                if (m - 1) % (prime - 1):
                    if e < 3 * n:
                        forbidden_low_energy += 1
                elif e < 3 * n and len(support) == 2:
                    nonzero_values = [group_ring[index] for index in support]
                    assert nonzero_values[0] == -nonzero_values[1]
                    alpha = abs(nonzero_values[0])
                    assert alpha ** (prime - 1) == prime ** (m - 1)
                    allowed_two_support_controls += 1
                    if len(controls) < 8:
                        controls.append({
                            "exponents": values,
                            "energy": e,
                            "prime": prime,
                            "cyclic_product": group_ring,
                            "alpha": alpha,
                        })
    assert forbidden_low_energy == 0
    return {
        "max_exponent": max_exponent,
        "half_splits_tested": tested,
        "forbidden_low_energy_counterexamples": forbidden_low_energy,
        "allowed_two_support_controls": allowed_two_support_controls,
        "selected_controls": controls,
    }


def general_prime_split_scan(max_exponent: int) -> dict[str, object]:
    """Hostile finite audit of the all-parameter prime split theorem.

    Repetitions are included because Erdős #256 allows exponent multisets.
    The scan is diagnostic only; the cyclotomic-norm proof carries the
    universal quantifiers.
    """
    splits_tested = 0
    incompatible_splits = 0
    forbidden_low_energy = 0
    low_energy_norm_controls = 0
    tight_controls: list[dict[str, object]] = []
    primes = primes_through(max_exponent)
    for n in range(3, 8):
        for values in combinations_with_replacement(
                range(1, max_exponent + 1), n):
            e = energy(values)
            for prime in primes:
                m = sum(value % prime == 0 for value in values)
                if not 0 < m < n:
                    continue
                splits_tested += 1
                s = n - m
                incompatible = (s - 1) % (prime - 1) != 0
                if incompatible:
                    incompatible_splits += 1
                    if e < 6 * m:
                        forbidden_low_energy += 1
                if e < 6 * m:
                    residues = [value % prime for value in values
                                if value % prime]
                    group_ring = cyclic_binomial_product(residues, prime)
                    support = [index for index, value
                               in enumerate(group_ring) if value]
                    assert len(support) == 2
                    assert group_ring[support[0]] == -group_ring[support[1]]
                    alpha = abs(group_ring[support[0]])
                    assert alpha ** (prime - 1) == prime ** (s - 1)
                    assert not incompatible
                    low_energy_norm_controls += 1
                if incompatible and e == 6 * m and len(tight_controls) < 10:
                    tight_controls.append({
                        "exponents": values,
                        "energy": e,
                        "prime": prime,
                        "divisible_count_m": m,
                        "outside_count_s": s,
                    })
    assert forbidden_low_energy == 0
    return {
        "n_range": [3, 7],
        "max_exponent": max_exponent,
        "exponent_multisets_including_repetitions": True,
        "nontrivial_prime_splits_tested": splits_tested,
        "arithmetically_incompatible_splits_tested": incompatible_splits,
        "forbidden_low_energy_counterexamples": forbidden_low_energy,
        "compatible_low_energy_norm_controls": low_energy_norm_controls,
        "selected_tight_controls": tight_controls,
    }


def prime_power_half_split_scan(max_exponent: int) -> dict[str, object]:
    powers: list[tuple[int, int, int]] = []
    for prime in primes_through(max_exponent):
        modulus = prime * prime
        exponent = 2
        while modulus <= max_exponent:
            powers.append((modulus, prime, exponent))
            modulus *= prime
            exponent += 1
    half_splits = 0
    low_energy_controls = 0
    for n in (4, 6):
        m = n // 2
        for values in combinations(range(1, max_exponent + 1), n):
            e = energy(values)
            for modulus, prime, exponent in powers:
                if sum(value % modulus == 0 for value in values) != m:
                    continue
                half_splits += 1
                if e >= 3 * n:
                    continue
                residues = [value % modulus for value in values
                            if value % modulus]
                group_ring = cyclic_binomial_product(residues, modulus)
                support = [index for index, value in enumerate(group_ring) if value]
                assert len(support) == 2
                assert group_ring[support[0]] == -group_ring[support[1]]
                alpha = abs(group_ring[support[0]])
                difference = (support[1] - support[0]) % modulus
                lhs = sum(prime ** valuation(value, prime)
                          for value in residues)
                rhs = prime ** valuation(difference, prime)
                phi = prime ** (exponent - 1) * (prime - 1)
                alpha_valuation = valuation(alpha, prime)
                assert alpha == prime ** alpha_valuation
                assert lhs - rhs == phi * alpha_valuation
                low_energy_controls += 1
    return {
        "prime_powers": [modulus for modulus, _, _ in powers],
        "half_splits_tested": half_splits,
        "low_energy_norm_identity_controls": low_energy_controls,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--box", type=int, default=250)
    parser.add_argument("--max-exponent", type=int, default=14)
    parser.add_argument(
        "--large-defect-m", type=int, default=0,
        help="optional exact lazy-carry defect spot check (75000 takes minutes)",
    )
    args = parser.parse_args()
    if args.box < 40 or args.max_exponent < 8:
        raise SystemExit("use --box>=40 and --max-exponent>=8")
    payload = {
        "status": "PASS",
        "scope": "finite audits only; all-parameter proofs are in REPORT.md",
        "macaulay": macaulay_self_test(args.box),
        "rank_coupled_selected_rows": [
            rank_coupled_row(r) for r in (20, 30, 50, 100, 200, 300)
        ],
        "reverse_top_no_go": reverse_top_no_go(),
        "defect_tail_reduction": defect_tail_reduction(),
        "general_prime_split": general_prime_split_scan(args.max_exponent),
        "prime_half_split": half_split_scan(args.max_exponent),
        "prime_power_half_split": prime_power_half_split_scan(args.max_exponent),
    }
    if args.large_defect_m:
        value, expansion = lazy_defect(args.large_defect_m)
        payload["large_defect_spot"] = {
            "M": args.large_defect_m,
            "d_3": value,
            "binom_M_minus_1_3": comb(args.large_defect_m - 1, 3),
            "excess": value - comb(args.large_defect_m - 1, 3),
            "canonical_expansion": expansion,
        }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
