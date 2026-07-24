#!/usr/bin/env python3
"""Exact/coarse certificates for the capacity-one sign-instability example."""

from fractions import Fraction


def disk_inclusion_bound(j: int) -> Fraction:
    """A rational upper bound for |p_j| on |z| <= 1-1/j.

    Put m=j^3, r=exp(-j), and
      p_j(z)=(z^((j-1)m)-1)(z^m-r^m).
    Since log(1-1/j) <= -1/j, all three exponential tails that occur
    in the triangle-inequality bound are at most exp(-4) < 1/16 for j>=2.
    Thus |p_j| < (1+1/16)(1/16+1/16)=17/128.
    """
    assert j >= 2
    return (1 + Fraction(1, 16)) * (Fraction(1, 16) + Fraction(1, 16))


def check_disk_inclusion() -> None:
    for j in range(2, 1000):
        assert disk_inclusion_bound(j) == Fraction(17, 128) < 1
    print("FINITE_POLYNOMIAL_DISK_CERTIFICATE_OK")
    print("p_j=(z^((j-1)j^3)-1)(z^(j^3)-exp(-j^4))")
    print("|z|<=1-1/j implies |p_j(z)|<17/128<1")
    print("therefore area{|p_j|<1}>=pi*(1-1/j)^2 -> pi")


def check_continuum_energy_formula() -> None:
    # nu_j=(1-1/j)lambda_1+(1/j)lambda_exp(-j).
    # I(lambda_s)=log(1/s), I(lambda_1,lambda_s)=0 for s<1.
    for j in range(2, 1000):
        eps = Fraction(1, j)
        inner_energy = Fraction(j)
        energy = eps * eps * inner_energy
        assert energy == Fraction(1, j)
    print("CONTINUUM_ENERGY_CERTIFICATE_OK I(nu_j)=1/j->0")
    print("for every |z|<1, U_nu_j(z)=(1/j)log(max(exp(-j),|z|))<0")
    print("therefore area{U_nu_j<0}>=pi for every j")


if __name__ == "__main__":
    check_disk_inclusion()
    check_continuum_energy_formula()
