#!/usr/bin/env python3
"""Arithmetic certificate for the near-sharp #809 stability theorem."""

from __future__ import annotations

import argparse
import json


def stability_cost(
    g: int, parity: str, a: int, h: int, centre_offset: int = 0
) -> int:
    if g < 4 or parity not in {"even", "odd"}:
        raise ValueError("requires g>=4 and parity even/odd")
    if h < 0:
        raise ValueError("h must be nonnegative")
    if not 0 <= centre_offset <= h:
        raise ValueError("centre offset must lie in [0,h]")
    if parity == "even":
        if a < 2 or a % 2:
            raise ValueError("even row requires even a>=2")
        offset = (a - 2) * (a + 4) // 2
    else:
        if a < 1 or a % 2 != 1:
            raise ValueError("odd row requires odd a>=1")
        offset = (a - 1) * (a + 3) // 2
    return (
        offset
        + h * (2 * g - h - 1)
        + 2 * centre_offset * (h - centre_offset)
    )


def certificate(max_g: int = 250) -> dict[str, int | bool]:
    parameter_rows = 0
    positive_h_rows = 0
    nonbaseline_a_rows = 0
    near_band_rows = 0
    centre_offset_samples = 0
    localization_checks = 0
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            first_a = 2 if parity == "even" else 1
            for a in range(first_a, 2 * g - 2, 2):
                kappa = 2 * g - a
                for h in range(kappa - 2):
                    cost = stability_cost(g, parity, a, h)
                    remainder = (
                        (a * a - 4 if parity == "even" else a * a - 1)
                        + 2 * h * (2 * g - h - 1)
                    )
                    baseline_a = 2 if parity == "even" else 1
                    # The vertex-deficit cost is R/2 plus a-baseline.
                    assert 2 * cost == remainder + 2 * (a - baseline_a)
                    assert cost >= 0
                    parameter_rows += 1

                    if h:
                        assert cost >= 2 * g - 2
                        positive_h_rows += 1
                    if a != baseline_a:
                        threshold = 8 if parity == "even" else 6
                        assert cost >= threshold
                        nonbaseline_a_rows += 1

                    threshold = min(
                        8 if parity == "even" else 6,
                        2 * g - 2,
                    )
                    if cost < threshold:
                        assert a == baseline_a and h == 0
                        near_band_rows += 1

                    # The exact p-concavity remainder is
                    # 2*u*(h-u).  Sample endpoints and interior extrema
                    # without turning the certificate into a quartic loop.
                    offsets = {0, h}
                    if h:
                        offsets |= {1, h // 2}
                    for centre_offset in offsets:
                        if not 0 <= centre_offset <= h:
                            continue
                        refined = stability_cost(
                            g, parity, a, h, centre_offset
                        )
                        assert refined == (
                            cost
                            + 2 * centre_offset * (h - centre_offset)
                        )
                        assert refined >= cost
                        square_constant = 9 if parity == "even" else 4
                        assert (a + 1) ** 2 <= 2 * refined + square_constant
                        assert h * (2 * g - h - 1) <= refined
                        if h:
                            endpoint_distance = min(centre_offset, h - centre_offset)
                            assert endpoint_distance * h <= refined
                        localization_checks += 1
                        centre_offset_samples += 1

    return {
        "max_g": max_g,
        "parameter_rows": parameter_rows,
        "positive_h_rows": positive_h_rows,
        "nonbaseline_a_rows": nonbaseline_a_rows,
        "near_band_rows": near_band_rows,
        "centre_offset_samples": centre_offset_samples,
        "localization_checks": localization_checks,
        "pass": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-g", type=int, default=250)
    args = parser.parse_args()
    print(json.dumps(certificate(args.max_g), sort_keys=True))


if __name__ == "__main__":
    main()
