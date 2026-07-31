#!/usr/bin/env python3
"""Exact guard for the rank-248 three-chart compression for Erdős #776.

The finite scans in this file are falsifier searches only.  The identities
being guarded are proved in BREAKTHROUGH_ATTACK.md.  All arithmetic is over
Python integers; no floating point comparison is used.
"""

from __future__ import annotations

import importlib.util
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ENGINE_PATH = (
    ROOT
    / "artifacts"
    / "erdos_master_rotation"
    / "R002"
    / "core_776_635"
    / "776"
    / "verify_rank5_rotation.py"
)


def load_engine():
    spec = importlib.util.spec_from_file_location("r002_rank5", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = load_engine()


def moving_h(parameter: int, rank: int) -> int:
    residual_rank = rank - 15
    return comb(parameter - 12, rank) + sum(
        comb(parameter - 28 + j, residual_rank + j)
        for j in range(1, 15)
    )


def shortened_state(parameter: int, target_rank: int) -> int:
    rank = parameter - 12
    runs = []
    while rank > target_rank:
        runs = ENGINE.defect_step(runs, rank, parameter)
        rank -= 1
    return ENGINE.runs_value(runs)


def forward_gap(parameter: int, constant: int, target_rank: int) -> int:
    """Run f_1=V-c, f_(r+1)=U_r(f_r)-V through target_rank.

    A negative value is returned immediately: after that point the displayed
    one-chart recurrence is no longer a legal canonical chart.
    """
    value = parameter - constant
    for rank in range(1, target_rank):
        if value < 0:
            return value
        value = ENGINE.upper_raise(value, rank) - parameter
    return value


def auxiliary_state(parameter: int, target_rank: int = 42) -> int:
    """E_(M-1)=0, E_(q-1)=V+KK_q(E_q), M=V-221."""
    ambient = parameter - 221
    rank = ambient - 1
    runs = []
    while rank > target_rank:
        runs = ENGINE.defect_step(runs, rank, parameter)
        rank -= 1
    return ENGINE.runs_value(runs)


def expanded_prefix(runs: list[tuple[int, int, int]], length: int):
    out: list[tuple[int, int]] = []
    for high, low, offset in runs:
        for lower in range(high, low - 1, -1):
            out.append((lower + offset, lower))
            if len(out) == length:
                return out
    return out


def auxiliary_runs(parameter: int):
    ambient = parameter - 221
    rank = ambient - 1
    runs = []
    while rank > 42:
        runs = ENGINE.defect_step(runs, rank, parameter)
        rank -= 1
    return runs


def check_symbolic_identities() -> None:
    # The two Pascal peels are numerical identities at every legal row.
    for parameter in (288, 301, 379, 500):
        for constant in (53, 109):
            next_constant = 2 * constant + 3
            left = parameter - constant
            residual = parameter - next_constant
            for rank in range(2, min(35, parameter - constant)):
                left = ENGINE.upper_raise(left, rank - 1) - parameter
                if residual >= 0:
                    expected = comb(parameter - constant - 2, rank) + residual
                    assert left == expected, (
                        parameter,
                        constant,
                        rank,
                        left,
                        expected,
                    )
                    residual = ENGINE.upper_raise(residual, rank - 1) - parameter
                else:
                    break


def check_gap_conjugacy() -> None:
    # At q=V-14 the moving-block gap is V-53.  Until first entry, its
    # subsequent values are exactly the upper-shift-minus-V orbit.
    for parameter in (288, 301, 379, 500):
        rank = parameter - 12
        runs = []
        states: dict[int, int] = {}
        bottom = max(248, 44)
        while rank >= bottom:
            states[rank] = ENGINE.runs_value(runs)
            if rank == bottom:
                break
            runs = ENGINE.defect_step(runs, rank, parameter)
            rank -= 1

        rank = parameter - 14
        residual_rank = 1
        value = states[rank]
        gap = moving_h(parameter, rank) - value
        assert gap == parameter - 53
        forward = gap
        while rank > max(248, 44):
            next_rank = rank - 1
            direct_gap = (
                moving_h(parameter, next_rank)
                - states[next_rank]
            )
            forward = ENGINE.upper_raise(forward, residual_rank) - parameter
            residual_rank += 1
            assert direct_gap == forward
            assert direct_gap > 0
            rank = next_rank


def check_rank248_rows() -> None:
    for parameter in (288, 301, 379, 500):
        rank248_gap = moving_h(parameter, 248) - shortened_state(parameter, 248)
        target = parameter - 261
        forward = forward_gap(parameter, 53, target)
        assert rank248_gap == forward > 0

        # On the two legal peeled charts.
        f109 = forward_gap(parameter, 109, target - 1)
        f221 = forward_gap(parameter, 221, target - 2)
        assert forward == comb(parameter - 55, target) + f109
        assert f109 == comb(parameter - 111, target - 1) + f221

        ambient = parameter - 221
        e42 = auxiliary_state(parameter)
        assert f221 == comb(ambient, 42) - e42 > 0


def precarry_formula(ambient: int, rank: int) -> int:
    def threshold(index: int) -> int:
        return 224 * ((1 << index) - 1)

    return sum(
        comb(ambient - threshold(rank - lower) - 2, lower)
        for lower in range(2, rank + 1)
    ) + ambient - threshold(rank - 1)


def check_auxiliary_precarry() -> None:
    # f_1=M, f_(r+1)=U_r(f_r)-(M+221).  Before the scalar threshold
    # A_(r-1)=224(2^(r-1)-1) reaches M, the whole chart is explicit.
    for ambient in (279, 1000, 100_000, 1_000_000):
        value = ambient
        rank = 1
        while 224 * ((1 << (rank - 1)) - 1) < ambient:
            assert value == precarry_formula(ambient, rank)
            if 224 * ((1 << rank) - 1) >= ambient:
                break
            value = ENGINE.upper_raise(value, rank) - (ambient + 221)
            rank += 1

    # Consequently no fixed diagonal-seed rank works for all M.
    # At this exact pre-carry point Gamma_r=-(M+222).
    ambient = 1_000_000
    tax = ambient + 221
    f_value = ambient
    g_value = ambient + 1
    for rank in range(1, 11):
        g_next = ENGINE.upper_raise(g_value, rank) - (tax + 1)
        gamma = g_next - (f_value + ENGINE.upper_raise(f_value, rank))
        assert gamma == -(ambient + 222)
        f_value = ENGINE.upper_raise(f_value, rank) - tax
        g_value = g_next


def first_diagonal_seed(ambient: int) -> tuple[int, int, int]:
    """Return (first-carry index j, first nonnegative seed rank, surplus)."""
    tax = ambient + 221
    f_value = ambient
    g_value = ambient + 1
    carry_index = 1
    while 224 * ((1 << carry_index) - 1) < ambient:
        carry_index += 1
    for rank in range(1, carry_index + 5):
        g_next = ENGINE.upper_raise(g_value, rank) - (tax + 1)
        gamma = g_next - (f_value + ENGINE.upper_raise(f_value, rank))
        if gamma >= 0:
            return carry_index, rank, gamma
        f_value = ENGINE.upper_raise(f_value, rank) - tax
        g_value = g_next
    raise AssertionError((ambient, carry_index))


def first_carry_index(ambient: int) -> int:
    carry_index = 1
    while 224 * ((1 << carry_index) - 1) < ambient:
        carry_index += 1
    return carry_index


def direct_diagonal_surplus(ambient: int, target_rank: int) -> int:
    """Compute Gamma_target_rank from the uncompressed adjacent orbits."""
    tax = ambient + 221
    f_value = ambient
    g_value = ambient + 1
    for rank in range(1, target_rank + 1):
        g_next = ENGINE.upper_raise(g_value, rank) - (tax + 1)
        gamma = g_next - (f_value + ENGINE.upper_raise(f_value, rank))
        if rank == target_rank:
            return gamma
        f_value = ENGINE.upper_raise(f_value, rank) - tax
        g_value = g_next
    raise AssertionError(target_rank)


def fixed_postcarry_tails(ambient: int) -> tuple[int, list[int]]:
    """Return j and the exact low-tail surpluses gamma_3,gamma_4,gamma_5."""
    carry_index = first_carry_index(ambient)
    if carry_index < 2:
        raise ValueError(ambient)
    previous_threshold = 224 * ((1 << (carry_index - 2)) - 1)
    current_threshold = 224 * ((1 << (carry_index - 1)) - 1)
    a = previous_threshold
    b = ambient - current_threshold
    c = a + b + 222
    tax = ambient + 221
    assert tax == 2 * a + b + 445
    assert 1 <= b <= 2 * a + 448

    x_value = comb(c, 3) + comb(b, 2) - tax
    y_value = comb(c + 1, 3) + comb(b + 1, 2) - (tax + 1)
    gammas: list[int] = []
    for rank in range(3, 6):
        x_next = ENGINE.upper_raise(x_value, rank) - tax
        y_next = ENGINE.upper_raise(y_value, rank) - (tax + 1)
        gammas.append(
            y_next - (x_value + ENGINE.upper_raise(x_value, rank))
        )
        x_value = x_next
        y_value = y_next
    return carry_index, gammas


def check_fixed_postcarry_localization() -> None:
    # Directly compare the global Gamma orbit with the rank-3 -> rank-5
    # low-tail reduction, including left/right carry-strip endpoints.
    strategic = [225, 226, 279, 378, 448, 449, 672, 673, 1000, 18_895]
    for ambient in strategic:
        carry_index, gammas = fixed_postcarry_tails(ambient)
        for offset, gamma in enumerate(gammas, start=1):
            assert gamma == direct_diagonal_surplus(
                ambient,
                carry_index + offset,
            )

    # The signed rank-2 tail needs at most one borrow.  Check its exact
    # normal form and both endpoints on exponentially distant strips.
    def polynomial_choose_2(value: int) -> int:
        return value * (value - 1) // 2

    for carry_index in range(2, 31):
        strip_length = 224 * (1 << (carry_index - 1))
        previous_threshold = 224 * ((1 << (carry_index - 1)) - 1)
        for b in (1, strip_length):
            ambient = previous_threshold + b
            c = b + strip_length // 2 - 2
            complement = strip_length - b
            tax = ambient + 221
            direct_x3 = comb(c, 3) + comb(b, 2) - tax
            signed_tail = polynomial_choose_2(b - 2) - complement
            assert direct_x3 == comb(c, 3) + signed_tail
            if signed_tail < 0:
                borrowed_tail = comb(c - 1, 2) + signed_tail
                assert borrowed_tail >= 0
                assert direct_x3 == comb(c - 1, 3) + borrowed_tail

            direct_y3 = comb(c + 1, 3) + comb(b + 1, 2) - (tax + 1)
            adjacent_signed_tail = (
                polynomial_choose_2(b - 1) - (complement - 1)
            )
            assert direct_y3 == comb(c + 1, 3) + adjacent_signed_tail


def finite_seed_scan(limit: int = 10_000) -> dict[str, int]:
    maximum_delay = -1
    first_at_maximum = -1
    minimum_gamma5: tuple[int, int] | None = None
    for ambient in range(67, limit + 1):
        carry_index, seed_rank, _ = first_diagonal_seed(ambient)
        delay = seed_rank - carry_index
        if delay > maximum_delay:
            maximum_delay = delay
            first_at_maximum = ambient
        if ambient >= 225:
            _, gammas = fixed_postcarry_tails(ambient)
            gamma5 = gammas[-1]
            if minimum_gamma5 is None or gamma5 < minimum_gamma5[0]:
                minimum_gamma5 = (gamma5, ambient)
    assert maximum_delay == 3
    assert minimum_gamma5 is not None and minimum_gamma5[0] > 0

    # Stress both exact carry-interval endpoints far beyond the dense scan.
    for carry_index in range(1, 31):
        endpoint = 224 * ((1 << carry_index) - 1)
        if endpoint < 67:
            continue
        observed_index, seed_rank, _ = first_diagonal_seed(endpoint)
        assert observed_index == carry_index
        assert seed_rank - carry_index == 3
        if carry_index >= 2:
            left_endpoint = 224 * ((1 << (carry_index - 1)) - 1) + 1
            for ambient in (left_endpoint, endpoint):
                observed_index, gammas = fixed_postcarry_tails(ambient)
                assert observed_index == carry_index
                assert gammas[-1] > 0
    return {
        "dense_seed_scan_limit_M": limit,
        "maximum_postcarry_delay": maximum_delay,
        "first_M_at_maximum_delay": first_at_maximum,
        "minimum_fixed_rank_gamma5": {
            "value": minimum_gamma5[0],
            "at_M": minimum_gamma5[1],
        },
        "stress_tested_carry_intervals_through": 30,
    }


def finite_falsifier_scan(limit: int = 500) -> dict[str, object]:
    min_aux_margin: tuple[int, int] | None = None
    prefix_failures: list[int] = []
    for parameter in range(288, limit + 1):
        ambient = parameter - 221
        runs = auxiliary_runs(parameter)
        e42 = ENGINE.runs_value(runs)
        margin = comb(ambient, 42) - e42
        if min_aux_margin is None or margin < min_aux_margin[0]:
            min_aux_margin = (margin, parameter)
        prefix = expanded_prefix(runs, 2)
        expected = [(ambient - 1, 42), (ambient - 2, 41)]
        if prefix != expected:
            prefix_failures.append(parameter)

    assert min_aux_margin is not None and min_aux_margin[0] > 0
    assert not prefix_failures

    # Two deliberately overstrong ideas are killed exactly.
    parameter = 288
    ambient = parameter - 221
    endpoint = ambient - 42
    f221 = forward_gap(parameter, 221, endpoint)
    assert f221 < comb(ambient - 3, endpoint)

    # Positivity does not come from monotone growth of the forward gap.
    parameter = 301
    ambient = parameter - 221
    endpoint = ambient - 42
    value = ambient
    decrease = None
    for rank in range(1, endpoint):
        next_value = ENGINE.upper_raise(value, rank) - parameter
        if next_value < value:
            decrease = (rank, value, next_value)
            break
        value = next_value
    assert decrease == (
        37,
        3612014796037017570710,
        3599951240723699028267,
    )

    return {
        "finite_scan": f"288 <= V <= {limit}",
        "minimum_auxiliary_margin": {
            "value": min_aux_margin[0],
            "at_V": min_aux_margin[1],
        },
        "rank42_prefix_failures": len(prefix_failures),
        "refuted_simplex_bound_at_V": 288,
        "refuted_monotone_gap_at_V": 301,
        "status": "PASS (finite scans are falsifier evidence only)",
    }


def main() -> None:
    check_symbolic_identities()
    check_gap_conjugacy()
    check_rank248_rows()
    check_auxiliary_precarry()
    check_fixed_postcarry_localization()
    print(finite_falsifier_scan())
    print(finite_seed_scan())


if __name__ == "__main__":
    main()
