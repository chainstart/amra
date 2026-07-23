#!/usr/bin/env python3
"""Exact regression checks for the Round 12 #776/#256 interfaces.

Finite ranges in this file are only implementation audits.  The all-parameter
arguments (including the log-sine/Dirichlet-character step) are in REPORT.md.
"""

from __future__ import annotations

import argparse
import json
import time
from itertools import combinations_with_replacement
from math import comb


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    out: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if not remaining:
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
        out.append((upper, lower))
        remaining -= comb(upper, lower)
        cap = upper
    if remaining:
        raise AssertionError((number, rank, out, remaining))
    return out


def upper_raise(number: int, rank: int) -> int:
    return sum(comb(a, i + 1) for a, i in canonical(number, rank))


def lower_shadow(number: int, rank: int) -> int:
    return sum(comb(a, i - 1) for a, i in canonical(number, rank))


def canonical_runs(number: int, rank: int) -> list[tuple[int, int, int]]:
    """Run-length compressed canonical expansion.

    A tuple (high, low, offset) denotes all terms
    C(i+offset,i), high >= i >= low.  Greedy canonical terms keep the same
    offset for a maximal consecutive run; hockey-stick identities let us
    skip the run exactly.
    """
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remaining = number
    lower = rank
    offset_cap: int | None = None
    runs: list[tuple[int, int, int]] = []
    while remaining:
        if lower < 1:
            raise AssertionError((number, rank, remaining, runs))
        if offset_cap is None:
            high_offset = 1
            while comb(lower + high_offset, high_offset) <= remaining:
                high_offset *= 2
        else:
            high_offset = offset_cap + 1
        lo, hi = -1, high_offset
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(lower + middle, middle) <= remaining:
                lo = middle
            else:
                hi = middle
        offset = lo
        if offset < 0:
            raise AssertionError((number, rank, remaining, lower, offset_cap))

        # Sum from i=low through lower of C(i+offset,offset).
        left, right = 1, lower
        while left < right:
            length = (left + right + 1) // 2
            low_rank = lower - length + 1
            run_value = (
                comb(lower + offset + 1, offset + 1)
                - comb(low_rank + offset, offset + 1)
            )
            if run_value <= remaining:
                left = length
            else:
                right = length - 1
        length = left
        low_rank = lower - length + 1
        run_value = (
            comb(lower + offset + 1, offset + 1)
            - comb(low_rank + offset, offset + 1)
        )
        runs.append((lower, low_rank, offset))
        remaining -= run_value
        lower -= length
        offset_cap = offset
    return runs


def run_value(runs: list[tuple[int, int, int]]) -> int:
    return sum(
        comb(high + offset + 1, offset + 1)
        - comb(low + offset, offset + 1)
        for high, low, offset in runs
    )


def run_lower_shadow(runs: list[tuple[int, int, int]]) -> int:
    return sum(
        comb(high + offset + 1, offset + 2)
        - comb(low + offset, offset + 2)
        for high, low, offset in runs
    )


def compressed_original_d3(m: int) -> tuple[int, list[tuple[int, int, int]]]:
    value = m - 6
    runs = canonical_runs(value, m - 3)
    for rank in range(m - 3, 3, -1):
        value = m - 3 + run_lower_shadow(runs)
        runs = canonical_runs(value, rank - 1)
        assert run_value(runs) == value
    return value, runs


def _lazy_add(
    expansion: list[tuple[int, int]],
    shift: int,
    rank: int,
    increment: int,
) -> None:
    """Exact suffix-carry addition for a lazily rank-shifted expansion."""
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


def lazy_original_d3(m: int) -> tuple[int, list[tuple[int, int]]]:
    """Large-M exact evaluator using the Round 11 lazy-carry representation."""
    expansion = [(i, i) for i in range(m - 3, 3, -1)]
    shift = 0
    for rank in range(m - 3, 3, -1):
        shift -= 1
        rank_zero_terms = 0
        while expansion and expansion[-1][1] + shift <= 0:
            _, stored_lower = expansion.pop()
            assert stored_lower + shift == 0
            rank_zero_terms += 1
        _lazy_add(
            expansion, shift, rank - 1,
            m - 3 + rank_zero_terms,
        )
    actual = [(upper, stored_lower + shift)
              for upper, stored_lower in expansion]
    value = sum(comb(upper, lower) for upper, lower in actual)
    return value, actual


def ordinary_defects(m: int) -> dict[int, int]:
    defects = {m - 2: 0}
    for q in range(m - 2, 3, -1):
        defects[q - 1] = m - 3 + lower_shadow(defects[q], q)
    return defects


def original_start_defects(m: int) -> dict[int, int]:
    """Defect state after retaining the three units in the original start.

    The stronger Round 11 candidate starts with delta_3=0.  The actual
    a_3=binom(N,3)-r is three larger.  Its first upper raise contributes
    U_1(3)=3, hence the complementary state begins at d_(M-3)=M-6.
    """
    defects = {m - 3: m - 6}
    for q in range(m - 3, 3, -1):
        defects[q - 1] = m - 3 + lower_shadow(defects[q], q)
    return defects


def actual_forward_endpoint(m: int) -> int:
    n = m + 2
    r = m - 3
    value = comb(n, 3) - r
    for rank in range(3, m):
        value = upper_raise(value, rank) - r
    return value


def macaulay_audit(max_m: int) -> dict[str, object]:
    endpoint_checks = 0
    early_formula_checks = 0
    precarry_normal_form_checks = 0
    largest_precarry_rank_checked = 0
    max_observed_excess = -10**9
    max_observed_at = 0
    for m in range(9, max_m + 1):
        actual = original_start_defects(m)
        compressed_value, compressed_runs = compressed_original_d3(m)
        assert compressed_value == actual[3]
        assert run_value(compressed_runs) == actual[3]
        lazy_value, lazy_expansion = lazy_original_d3(m)
        assert lazy_value == actual[3]
        assert lazy_expansion == canonical(actual[3], 3)
        slack = comb(m - 2, 2) + 4
        v = m - 3
        precarry_scalar = 5
        precarry_active = True
        for rank in range(2, m - 5):
            slack = upper_raise(slack, rank) - (m - 3)
            assert slack >= 0
            new_rank = rank + 1
            if precarry_active:
                if new_rank > 3:
                    old_rank = new_rank - 1
                    precarry_scalar = (
                        comb(precarry_scalar, 2) - 2 * old_rank + 3
                    )
                threshold = v - 2 * new_rank + 5
                if 0 < precarry_scalar < threshold:
                    expected_expansion = [(v, new_rank)]
                    expected_expansion.extend(
                        (v - 2 * new_rank + 2 * lower, lower)
                        for lower in range(new_rank - 1, 2, -1)
                    )
                    expected_expansion.extend([
                        (v - 2 * new_rank + 5, 2),
                        (precarry_scalar, 1),
                    ])
                    assert canonical(slack, new_rank) == expected_expansion
                    precarry_normal_form_checks += 1
                    largest_precarry_rank_checked = max(
                        largest_precarry_rank_checked, new_rank
                    )
                else:
                    precarry_active = False
        # The loop ends at slack rank M-5, dual to the original defect rank 4.
        assert slack == comb(m - 1, 4) - actual[4]
        if m >= 32:
            quadratic_target = comb(m - 3, 2) - comb(28, 2)
            assert (
                actual[3] <= comb(m - 1, 3) + 28
            ) == (slack >= quadratic_target)
        endpoint = actual_forward_endpoint(m)
        target = comb(m - 1, 3) + 28
        assert (endpoint >= 0) == (actual[3] <= target)
        endpoint_checks += 1
        excess = actual[3] - comb(m - 1, 3)
        if excess > max_observed_excess:
            max_observed_excess = excess
            max_observed_at = m

        if m >= 14:
            strong = ordinary_defects(m)
            assert strong[m - 4] == comb(m - 1, 2) - 1
            assert actual[m - 4] == comb(m - 1, 2) - 7
            assert strong[m - 4] - actual[m - 4] == 6
            assert strong[m - 5] == (
                comb(m - 2, 3) + comb(m - 4, 2) + 2 * m - 9
            )
            assert actual[m - 5] == (
                comb(m - 2, 3) + comb(m - 4, 2) + m - 13
            )
            assert strong[m - 5] - actual[m - 5] == m + 4
            assert strong[m - 6] == (
                comb(m - 2, 4)
                + comb(m - 4, 3)
                + comb(m - 6, 2)
                + comb(m - 7, 2)
                + 5 * m
                - 45
            )
            assert actual[m - 6] == (
                comb(m - 2, 4)
                + comb(m - 4, 3)
                + comb(m - 6, 2)
                + m
                - 24
            )
            assert strong[m - 6] - actual[m - 6] == (
                comb(m - 7, 2) + 4 * m - 21
            )
            early_formula_checks += 1
    return {
        "verified_m_range": [9, max_m],
        "actual_endpoint_equivalence_checks": endpoint_checks,
        "compressed_engine_equivalence_checks": endpoint_checks,
        "lazy_carry_engine_equivalence_checks": endpoint_checks,
        "quadratic_forward_slack_equivalence_checks": endpoint_checks,
        "growing_slack_formula_checks": early_formula_checks,
        "precarry_normal_form_checks": precarry_normal_form_checks,
        "largest_precarry_rank_checked": largest_precarry_rank_checked,
        "strong_minus_actual_defect_at_rank_Mminus4": "6",
        "strong_minus_actual_defect_at_rank_Mminus5": "M+4",
        "strong_minus_actual_defect_at_rank_Mminus6":
            "binom(M-7,2)+4M-21",
        "round11_displayed_seed_correction":
            "d^[M]_(M-4)=binom(M-1,2)-1, not binom(M-1,2)",
        "maximum_finite_actual_d3_excess": max_observed_excess,
        "maximum_first_attained_at_m": max_observed_at,
        "finite_scope_only": True,
    }


def first_carry_interval_audit() -> dict[str, object]:
    """Audit the exact first-carry normal form on representative V values."""
    x8 = 19_961_710
    samples = [6329, 74997, 149997, 1_000_000, 19_961_721]
    for v in samples:
        slack = comb(v + 1, 2) + 4
        for rank in range(2, 8):
            slack = upper_raise(slack, rank) - v
        y = x8 - (v - 11)
        assert 0 <= y < comb(v - 9, 2)
        expected = [(v, 8)]
        expected.extend(
            (v - 16 + 2 * lower, lower)
            for lower in range(7, 3, -1)
        )
        expected.append((v - 9, 3))
        expected.extend(canonical(y, 2))
        assert canonical(slack, 8) == expected
    return {
        "V_interval": [6329, 19_961_721],
        "representative_V_values": samples,
        "exact_first_carry_checks": len(samples),
        "counterexamples": 0,
        "finite_checks_support_an_algebraic_interval_identity": True,
    }


def general_first_carry_partition_audit(max_first_rank: int = 9) -> dict[str, object]:
    """Audit the all-V first-carry interval formula through selected ranks."""
    scalar = {3: 5}
    previous_right = 6
    checked = 0
    intervals: dict[str, list[int]] = {}
    for first_rank in range(4, max_first_rank + 1):
        old_rank = first_rank - 1
        scalar[first_rank] = (
            comb(scalar[old_rank], 2) - 2 * old_rank + 3
        )
        left = scalar[old_rank] + 2 * first_rank - 6
        right = scalar[first_rank] + 2 * first_rank - 5
        assert left == previous_right + 1
        intervals[str(first_rank)] = [left, right]
        for v in sorted({left, (left + right) // 2, right}):
            slack = comb(v + 1, 2) + 4
            for rank in range(2, first_rank):
                slack = upper_raise(slack, rank) - v
            y = scalar[first_rank] - (v - 2 * first_rank + 5)
            expected = [(v, first_rank)]
            expected.extend(
                (v - 2 * first_rank + 2 * lower, lower)
                for lower in range(first_rank - 1, 3, -1)
            )
            expected.append((v - 2 * first_rank + 7, 3))
            expected.extend(canonical(y, 2))
            assert canonical(slack, first_rank) == expected
            checked += 1
        previous_right = right
    return {
        "first_carry_ranks_audited": [4, max_first_rank],
        "partition_intervals": intervals,
        "endpoint_and_midpoint_checks": checked,
        "largest_scalar": scalar[max_first_rank],
        "counterexamples": 0,
        "finite_checks_support_an_all_parameter_algebraic_partition": True,
    }


def second_carry_threshold_audit() -> dict[str, object]:
    """Audit the exact rank-9 split at V*=19,840,461."""
    x8 = 19_961_710
    v_star = 19_840_461
    assert canonical(v_star, 3) == [(492, 3), (473, 2), (453, 1)]
    assert lower_shadow(v_star, 3) == 121_260
    assert v_star + lower_shadow(v_star, 3) == x8 + 11
    assert (
        v_star + 1 + lower_shadow(v_star + 1, 3) > x8 + 11
    )
    v_star_star = 19_838_163
    assert canonical(v_star_star, 4) == [
        (149, 4), (90, 3), (37, 2), (16, 1)
    ]
    inner = v_star_star + lower_shadow(v_star_star, 4)
    assert lower_shadow(v_star_star, 4) == 544_317
    assert canonical(inner, 3) == [(497, 3), (301, 2), (90, 1)]
    assert lower_shadow(inner, 3) == 123_558
    assert v_star_star + lower_shadow(inner, 3) == x8 + 11
    next_inner = v_star_star + 1 + lower_shadow(v_star_star + 1, 4)
    assert (
        v_star_star + 1 + lower_shadow(next_inner, 3) > x8 + 11
    )
    v9_right = 199_234_923_081_195
    v9_star = 199_229_291_300_636
    assert canonical(v9_star, 3) == [
        (106130, 3), (45173, 2), (43498, 1)
    ]
    assert lower_shadow(v9_star, 3) == 5_631_780_559
    assert v9_star + lower_shadow(v9_star, 3) == v9_right
    assert v9_star + 1 + lower_shadow(v9_star + 1, 3) > v9_right

    lower_samples = [6329, 74997, 149997, v_star]
    upper_samples = [v_star + 1, 19_900_000, 19_961_721]
    for v in lower_samples + upper_samples:
        slack = comb(v + 1, 2) + 4
        for rank in range(2, 9):
            slack = upper_raise(slack, rank) - v
        y = x8 - (v - 11)
        residual3 = upper_raise(y, 2) - v
        expected = [(v, 9)]
        expected.extend(
            (v - 18 + 2 * lower, lower)
            for lower in range(8, 4, -1)
        )
        if v <= v_star:
            assert residual3 >= 0
            expected.append((v - 9, 4))
            expected.extend(canonical(residual3, 3))
        else:
            z = -residual3
            assert 0 < z <= v < comb(v - 11, 2)
            expected.extend([(v - 10, 4), (v - 11, 3)])
            expected.extend(canonical(comb(v - 11, 2) - z, 2))
        assert canonical(slack, 9) == expected
    return {
        "V_interval": [6329, 19_961_721],
        "exact_threshold_V_star": v_star,
        "next_block_threshold_V_star_star": v_star_star,
        "next_first_carry_interval_rank9": [19_961_722, v9_right],
        "rank10_residual_threshold_in_rank9_interval": v9_star,
        "lower_segment_samples": lower_samples,
        "upper_segment_samples": upper_samples,
        "rank9_normal_form_checks": len(lower_samples + upper_samples),
        "counterexamples": 0,
        "finite_checks_support_algebraic_segment_theorems": True,
    }


def rank5_constant_threshold_audit() -> dict[str, object]:
    """Audit the sharp h=binom(376,2) endpoint reduction boundaries.

    The universal statement is proved algebraically in REPORT.md.  These
    selected exact integers only guard the two canonical cap transitions and
    both sides of the equality threshold.
    """
    threshold = comb(376, 2)
    tested = 0
    for v in (379, 400, 1_000, 74_997):
        b5 = comb(v + 1, 5) + comb(v, 4)
        f5 = (
            comb(v + 1, 5)
            + comb(v - 1, 4)
            + comb(v - 2, 3)
        )
        b4 = comb(v + 1, 4) + comb(v, 3)
        f4 = (
            comb(v + 1, 4)
            + comb(v - 1, 3)
            + comb(v - 2, 2)
        )
        cap = comb(v - 2, 2)
        assert f5 == b5 - cap
        assert lower_shadow(f5, 5) == f4
        assert b4 - f4 == v - 2
        assert threshold + 1 < cap
        samples = {
            -1, 0, 1, threshold - 1, threshold, threshold + 1,
            cap - 1, cap, cap + 1,
        }
        for h in sorted(samples):
            e5 = f5 + h
            e4 = v + lower_shadow(e5, 5)
            e3 = v + lower_shadow(e4, 4)
            closes = e3 <= comb(v + 2, 3) + 28
            assert closes == (h <= threshold)
            if 0 <= h < cap:
                d = 2 + lower_shadow(h, 2)
                assert e4 == b4 + d
                assert e3 == comb(v + 2, 3) + lower_shadow(d, 2)
            tested += 1
    assert lower_shadow(threshold, 2) == 376
    assert lower_shadow(threshold + 1, 2) == 377
    assert lower_shadow(378, 2) == 28
    assert lower_shadow(379, 2) == 29
    rank6_tested = 0
    for v in (70_501, 70_510):
        f6 = (
            comb(v + 1, 6)
            + comb(v - 1, 5)
            + comb(v - 2, 4)
        )
        cap = comb(v - 2, 4)
        required_g = comb(v - 4, 2) - comb(70_496, 2)
        assert lower_shadow(v - threshold, v - 5) == required_g
        for g in (-1, 0, required_g - 1, required_g,
                  required_g + 1, cap, cap + 1):
            e6 = f6 - g
            e5 = v + lower_shadow(e6, 6)
            e4 = v + lower_shadow(e5, 5)
            e3 = v + lower_shadow(e4, 4)
            closes = e3 <= comb(v + 2, 3) + 28
            assert closes == (g >= required_g)
            rank6_tested += 1
    return {
        "valid_for_all_V_at_least": 379,
        "sharp_h_threshold": threshold,
        "threshold_endpoint_excess": 28,
        "threshold_plus_one_endpoint_excess": 29,
        "selected_branch_checks": tested,
        "rank6_reverse_threshold_checks": rank6_tested,
        "counterexamples": 0,
        "finite_checks_support_an_all_parameter_algebraic_reduction": True,
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


def primes_through(limit: int) -> list[int]:
    return [
        p for p in range(2, limit + 1)
        if all(p % d for d in range(2, int(p**0.5) + 1))
    ]


def cyclic_binomial_product(residues: list[int], modulus: int) -> list[int]:
    values = [0] * modulus
    values[0] = 1
    for residue in residues:
        updated = values.copy()
        for index, value in enumerate(values):
            updated[(index + residue) % modulus] -= value
        values = updated
    return values


def signed_class(residue: int, prime: int) -> int:
    residue %= prime
    if not residue:
        raise ValueError((residue, prime))
    return min(residue, prime - residue)


def cyclic_two_support_classification_audit(max_s: int = 8) -> dict[str, object]:
    """Exhaust small odd-prime instances of the all-parameter classification."""
    tested = 0
    two_support = 0
    predicted = 0
    for prime in (3, 5, 7):
        for size in range(1, max_s + 1):
            for residues in combinations_with_replacement(
                range(1, prime), size
            ):
                product = cyclic_binomial_product(list(residues), prime)
                support = [i for i, value in enumerate(product) if value]
                is_two_support = len(support) == 2
                predicted_class: int | None = None
                if (size - 1) % (prime - 1) == 0:
                    t = (size - 1) // (prime - 1)
                    counts = {
                        cls: sum(
                            signed_class(residue, prime) == cls
                            for residue in residues
                        )
                        for cls in range(1, (prime - 1) // 2 + 1)
                    }
                    candidates = [
                        cls for cls, count in counts.items()
                        if count == 2 * t + 1
                        and all(
                            other_count == 2 * t
                            for other, other_count in counts.items()
                            if other != cls
                        )
                    ]
                    if len(candidates) == 1:
                        predicted_class = candidates[0]
                is_predicted = predicted_class is not None
                assert is_two_support == is_predicted
                if is_two_support:
                    assert product[support[0]] == -product[support[1]]
                    difference_class = signed_class(
                        support[0] - support[1], prime
                    )
                    assert difference_class == predicted_class
                    two_support += 1
                predicted += is_predicted
                tested += 1
    return {
        "odd_primes": [3, 5, 7],
        "size_range": [1, max_s],
        "residue_multisets_tested": tested,
        "two_support_instances": two_support,
        "predicted_instances": predicted,
        "counterexamples": 0,
        "finite_scope_only": True,
    }


def prime_histogram_audit(max_exponent: int) -> dict[str, object]:
    splits = 0
    low_energy_splits = 0
    odd_prime_low_energy_splits = 0
    single_outside_energy_recursions = 0
    for n in range(3, 8):
        for exponents in combinations_with_replacement(
            range(1, max_exponent + 1), n
        ):
            e = energy(exponents)
            for prime in primes_through(max_exponent):
                m = sum(a % prime == 0 for a in exponents)
                if not 0 < m < n:
                    continue
                splits += 1
                outside_exponents = [a for a in exponents if a % prime]
                if len(outside_exponents) == 1:
                    divided_core = tuple(
                        a // prime for a in exponents if a % prime == 0
                    )
                    assert e == 2 * energy(divided_core)
                    single_outside_energy_recursions += 1
                if e >= 6 * m:
                    continue
                low_energy_splits += 1
                outside = [a % prime for a in exponents if a % prime]
                s = len(outside)
                assert (s - 1) % (prime - 1) == 0
                t = (s - 1) // (prime - 1)
                product = cyclic_binomial_product(outside, prime)
                support = [i for i, value in enumerate(product) if value]
                assert len(support) == 2
                assert product[support[0]] == -product[support[1]]
                if prime == 2:
                    continue
                odd_prime_low_energy_splits += 1
                distinguished = signed_class(
                    support[0] - support[1], prime
                )
                counts = {
                    cls: sum(
                        signed_class(residue, prime) == cls
                        for residue in outside
                    )
                    for cls in range(1, (prime - 1) // 2 + 1)
                }
                for cls, count in counts.items():
                    assert count == 2 * t + (cls == distinguished)
    return {
        "max_exponent": max_exponent,
        "n_range": [3, 7],
        "nontrivial_prime_splits": splits,
        "low_energy_splits": low_energy_splits,
        "odd_prime_low_energy_splits": odd_prime_low_energy_splits,
        "single_outside_exact_energy_recursions":
            single_outside_energy_recursions,
        "histogram_counterexamples": 0,
        "histogram_rule":
            "nu_{+-d}=2t+1 and nu_{+-a}=2t otherwise; s-1=t(p-1)",
        "finite_scope_only": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=180)
    parser.add_argument("--max-exponent", type=int, default=9)
    parser.add_argument(
        "--spot-m", type=int,
        help="optional exact compressed original-start d_3 spot check",
    )
    args = parser.parse_args()
    if args.max_m < 14 or args.max_exponent < 6:
        raise SystemExit("use --max-m>=14 and --max-exponent>=6")
    result: dict[str, object] = {
        "macaulay_original_start": macaulay_audit(args.max_m),
        "macaulay_general_first_carry_partition":
            general_first_carry_partition_audit(),
        "macaulay_first_carry_interval": first_carry_interval_audit(),
        "macaulay_second_carry_threshold": second_carry_threshold_audit(),
        "macaulay_rank5_constant_threshold":
            rank5_constant_threshold_audit(),
        "odd_prime_cyclic_two_support_classification":
            cyclic_two_support_classification_audit(),
        "prime_split_signed_histogram":
            prime_histogram_audit(args.max_exponent),
        "scope": "finite audits only; all-parameter proofs are in REPORT.md",
        "status": "PASS",
    }
    if args.spot_m is not None:
        started = time.monotonic()
        value, expansion = lazy_original_d3(args.spot_m)
        result["large_original_start_spot"] = {
            "M": args.spot_m,
            "d3": value,
            "excess_over_binom_Mminus1_3":
                value - comb(args.spot_m - 1, 3),
            "canonical_expansion": expansion,
            "elapsed_seconds": time.monotonic() - started,
            "finite_scope_only": True,
        }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
