#!/usr/bin/env python3
"""Finite arithmetic guard for opposite-star defect-slack energy."""

from __future__ import annotations

import itertools
import json


def profile(
    ell: int,
    residuals: tuple[int, ...],
    h_mass: int,
    defect: int,
    degree_spread: int,
    reserve: int,
) -> dict[str, int | bool]:
    if len(residuals) != ell:
        raise ValueError("one residual is required per leaf")
    if ell < 1 or min(residuals) < 2:
        raise ValueError("the opposite-star chart has ell>=1 and rho_c>=2")
    if h_mass > defect:
        raise ValueError("zero-star mass must not exceed D_B")

    residual_mass = sum(residuals)
    surcharge = sum(max(0, rho - ell - 1) for rho in residuals)
    correction = sum(min(ell - 1, rho - 2) for rho in residuals)
    exact_identity = correction == residual_mass - 2 * ell - surcharge
    reserve_rhs = (
        2 * h_mass
        + 2 * residual_mass
        - 2 * (degree_spread + 2) * ell
        - correction
    )
    reserve_energy = 2 * reserve >= reserve_rhs
    reserve_failure = reserve <= defect - 1
    conclusion = (
        residual_mass + surcharge
        <= 2 * (degree_spread + 1) * ell
        + 2 * (defect - h_mass)
        - 2
    )
    tight_endpoint_excluded = (
        not (reserve_energy and reserve_failure)
        or degree_spread * ell + (defect - h_mass) >= 1
    )
    return {
        "residual_mass": residual_mass,
        "surcharge": surcharge,
        "correction": correction,
        "reserve_rhs": reserve_rhs,
        "exact_identity": exact_identity,
        "antecedent": reserve_energy and reserve_failure,
        "conclusion": conclusion,
        "tight_endpoint_excluded": tight_endpoint_excluded,
        "pass": exact_identity
        and (not (reserve_energy and reserve_failure) or conclusion)
        and tight_endpoint_excluded,
    }


def exhaustive_certificate(
    max_ell: int = 4,
    max_rho: int = 8,
    max_slack: int = 5,
) -> dict[str, int | bool]:
    profiles = 0
    antecedents = 0
    strict_improvements = 0
    for ell in range(1, max_ell + 1):
        for residuals in itertools.product(range(2, max_rho + 1), repeat=ell):
            for h_mass in range(2 * ell, 2 * ell + 4):
                for slack in range(max_slack + 1):
                    defect = h_mass + slack
                    for degree_spread in range(5):
                        residual_mass = sum(residuals)
                        surcharge = sum(
                            max(0, rho - ell - 1) for rho in residuals
                        )
                        correction = sum(
                            min(ell - 1, rho - 2) for rho in residuals
                        )
                        reserve_rhs = (
                            2 * h_mass
                            + 2 * residual_mass
                            - 2 * (degree_spread + 2) * ell
                            - correction
                        )
                        least_reserve = max(0, (reserve_rhs + 1) // 2)
                        if least_reserve <= defect - 1:
                            result = profile(
                                ell,
                                residuals,
                                h_mass,
                                defect,
                                degree_spread,
                                least_reserve,
                            )
                            assert result["pass"]
                            antecedents += 1
                            if surcharge > 0:
                                strict_improvements += 1
                        profiles += 1
    return {
        "profiles": profiles,
        "antecedents": antecedents,
        "strict_improvements": strict_improvements,
        "pass": True,
    }


def main() -> int:
    print(json.dumps(exhaustive_certificate(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
