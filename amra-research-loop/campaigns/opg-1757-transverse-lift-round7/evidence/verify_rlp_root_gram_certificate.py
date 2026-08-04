#!/usr/bin/env python3
"""Exact Bernstein certificate for the q0-chart RLP root Gram corner.

The large determinant polynomial is formed exactly by Kronecker substitution
in base 2**64.  Positive and negative input parts are multiplied separately,
and an explicit l1 bound proves that no base carry can mix adjacent tensor
coefficients.  The five tensor axes are then converted to Bernstein form with
integer sign-equivalent transforms.  Only Python's standard library is used.
"""

from __future__ import annotations

from array import array
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial, lcm, prod
import multiprocessing
import struct

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    variable,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    coefficient,
    common_monomial,
    divide_monomial,
)
from verify_rlp_projective_corner_reduction import (
    f4_factor,
    product,
    reconstruct_h1884,
    root_coordinates,
    scale,
    small_direction_faces,
)


# Fast-to-slow dense axes are y,a,v,t,B.  These are one plus the exact
# output degrees of D4=4*R0*Kbar-(1-a+B)*R1**2.
SHAPE = (27, 10, 31, 27, 16)
OTHER_SHAPE = SHAPE[:-1]
OTHER_SIZE = prod(OTHER_SHAPE)
TOTAL_SIZE = prod(SHAPE)
SLOTS = (0, 1, 6, 7, 5)
STRIDES = tuple(prod(SHAPE[:index]) for index in range(len(SHAPE)))
BASE_BITS = 64
DIGIT_BYTES = BASE_BITS // 8
BASE = 1 << BASE_BITS
PRODUCT_OPERANDS = ()

EXPECTED_ROW_SHA256 = (
    "a4bd7b65204c57b270d4d04a8788a7452489b6af2acd4b6dcaab3cf530e5a0e8",
    "8f9880e6de7c29d3d1dfceadf05d1570781c05cf1f85feef86155e87d6c592c0",
    "ea0f83ba0480bc82d752517b437e21b919f2f6727ff993580d9a1ddd1d98a222",
    "3cdc0d54a8c5585f013425392eabff14baa38021ae4732d8899e5928791961a0",
    "8a490b0f9e1af8e39a7aca18db6a1e20dd99cffd1150fde71f251b15633e73bc",
    "41ad30133c689b8afad55a28ff28d4824307fd483111307d8a3db2f9cf3ad37d",
    "51d853ab41b07f3563e7970e41138ac4f335514d44ce242d4898ba994e5d693c",
    "397137a16b35baacfb53eb946f6e03755d45e9cf7319d953a8369f9f358376c3",
    "10b211d43bfee326693398116877cdabf4b4491c3e1b703b933854ea76e5a119",
    "e9c8de493a297cc6b8adcca8e236c3047beb9371e15e32810193e4fbdd35941d",
    "9f3f628cd552c8a66a18a2aff1b675cc3bd1ebf007d44f8147c5ea28e03540d3",
    "6d4ad77c50d7ca6411bb88db4506aca95bf59866447351b6dba0a6dfe72d5eeb",
    "9d2b4ce115947771442e3ce1d3662bf65c0b1980e80aac713baad25f5264db17",
    "3a52584b8310dd519918e1bf3276c36871d0016e14d939c0c2219f9fbdce3e30",
    "13ceb040f3480edcef9fc559aa7b3fda2182ff661c8274a5e18142cdd17f74ca",
    "137dae8dc6adae55f302da5934bd65db901219bc50ceac3f3b18b909c68e8bdb",
)


def index_of(monomial):
    return sum(monomial[slot] * stride for slot, stride in zip(SLOTS, STRIDES))


def sign_mass(poly, positive):
    return sum(
        abs(value.numerator)
        for value in poly.values()
        if (value > 0) == positive
    )


def packed_sign(poly, positive):
    raw = bytearray(TOTAL_SIZE * DIGIT_BYTES)
    for monomial, value in poly.items():
        assert value.denominator == 1
        integer = value.numerator
        if (integer > 0) != positive:
            continue
        magnitude = abs(integer)
        assert magnitude < BASE
        struct.pack_into("<Q", raw, index_of(monomial) * DIGIT_BYTES, magnitude)
    return int.from_bytes(raw, "little")


def multiply_packed(index):
    left, right = PRODUCT_OPERANDS[index]
    product_integer = left * right
    assert product_integer.bit_length() <= TOTAL_SIZE * BASE_BITS
    return index, product_integer.to_bytes(TOTAL_SIZE * DIGIT_BYTES, "little")


def accumulate_raw(target, raw, multiplier):
    values = memoryview(raw).cast("Q")
    maximum = 0
    for index, value in enumerate(values):
        maximum = max(maximum, value)
        target[index] += multiplier * value
    return maximum


def signed_convolution(left, right, square=False):
    """Return an exact dense convolution plus carry-safety diagnostics."""
    global PRODUCT_OPERANDS
    left_positive = packed_sign(left, True)
    left_negative = packed_sign(left, False)
    right_positive = packed_sign(right, True)
    right_negative = packed_sign(right, False)
    if square:
        assert left is right
        products = (
            (left_positive, left_positive, 1, True, True),
            (left_negative, left_negative, 1, False, False),
            (left_positive, left_negative, -2, True, False),
        )
    else:
        products = (
            (left_positive, right_positive, 1, True, True),
            (left_negative, right_negative, 1, False, False),
            (left_positive, right_negative, -1, True, False),
            (left_negative, right_positive, -1, False, True),
        )

    # Every coefficient of a nonnegative convolution is at most the product
    # of the two l1 masses.  Staying below BASE proves that packed digits do
    # not carry into their neighbours.
    carry_bounds = tuple(
        sign_mass(left, left_sign) * sign_mass(right, right_sign)
        for _, _, _, left_sign, right_sign in products
    )
    assert max(carry_bounds) < BASE

    PRODUCT_OPERANDS = tuple((left_int, right_int)
                             for left_int, right_int, _, _, _ in products)
    result = array("q", [0]) * TOTAL_SIZE
    maxima = [0] * len(products)
    context = multiprocessing.get_context("fork")
    with context.Pool(processes=len(products)) as pool:
        for index, raw in pool.imap_unordered(multiply_packed, range(len(products))):
            maxima[index] = accumulate_raw(result, raw, products[index][2])
    PRODUCT_OPERANDS = ()
    assert all(maximum <= bound for maximum, bound in zip(maxima, carry_bounds))
    return result, {
        "component_maxima": maxima,
        "carry_upper_bounds": list(carry_bounds),
        "carry_upper_bound_bits": [bound.bit_length() for bound in carry_bounds],
    }


def build_kernels():
    one = constant(1)
    y, a, B, v, t = (variable(slot) for slot in (0, 1, 5, 6, 7))
    A = add(one, a, -1)
    C1 = add(A, B)
    C2 = add(
        multiply(A, add(one, product(t, v, y))),
        product(B, v, y, add(A, multiply(a, t))),
    )
    h1884 = reconstruct_h1884()[0]
    normalized = small_direction_faces(h1884)[1]
    root = root_coordinates(normalized)
    rows = [coefficient(root, 2, degree) for degree in range(5)]
    B_monomial = (0, 0, 0, 0, 0, 1, 0, 0)
    assert common_monomial(rows[0]) == B_monomial
    assert common_monomial(rows[1]) == B_monomial
    R0 = divide_monomial(rows[0], B_monomial)
    R1 = divide_monomial(rows[1], B_monomial)

    r3_common = (1, 0, 0, 0, 0, 1, 1, 0)
    F4 = f4_factor()
    H260 = scale(
        divide_polynomial(
            divide_polynomial(divide_monomial(rows[3], r3_common), C2),
            F4,
        ),
        Fraction(-1, 2),
    )
    assert rows[3] == scale(product(y, B, v, C2, F4, H260), -2)
    assert rows[4] == product(y, y, B, B, v, v, C1, C2, F4, F4)
    K24 = add(
        multiply(C1, rows[2]),
        product(C2, multiply(H260, H260)),
        -1,
    )
    assert common_monomial(K24) == B_monomial
    Kbar = divide_monomial(K24, B_monomial)

    assert (len(R0), digest(R0)) == (
        16469,
        "6854fed45787e239c68a332feb2af01ae49335f702a21ec83632719df17c5995",
    )
    assert (len(R1), digest(R1)) == (
        11141,
        "4d8481f1153caec85057bd8db8d81f5b14cf18474f4bba80c5df480d50ce571c",
    )
    assert (len(Kbar), digest(Kbar)) == (
        8599,
        "e851b946099e4d6314c5c7ecda93095343c9fa8f7af293dc6c6d8745de0c0af3",
    )
    return C1, R0, R1, Kbar


def active_degrees(poly):
    return [max(monomial[slot] for monomial in poly) for slot in SLOTS]


def scaled_bernstein_record(poly, expected_digest, strict):
    upper = {
        0: Fraction(1),
        1: Fraction(1, 128),
        5: Fraction(1),
        6: Fraction(1, 128),
        7: Fraction(1, 32),
    }
    scaled = {
        monomial: value * prod(upper[slot] ** monomial[slot] for slot in SLOTS)
        for monomial, value in poly.items()
    }
    degrees = active_degrees(scaled)
    transformed = bernstein_transform(scaled, SLOTS)
    full_count = prod(degree + 1 for degree in degrees)
    values = list(transformed.values())
    assert digest(transformed) == expected_digest
    assert values and all(value > 0 for value in values)
    if strict:
        assert len(values) == full_count
    return {
        "power_terms": len(poly),
        "power_sha256": digest(poly),
        "degrees_y_a_v_t_B": active_degrees(poly),
        "controls": full_count,
        "positive_controls": len(values),
        "zero_controls": full_count - len(values),
        "negative_controls": 0,
        "minimum_nonzero": str(min(values)),
        "maximum": str(max(values)),
        "bernstein_sha256": digest(transformed),
    }


def determinant_power_tensor(R0, R1, Kbar):
    assert [left + right for left, right in zip(active_degrees(R0), active_degrees(Kbar))] == [26, 9, 30, 26, 15]
    assert [2 * degree for degree in active_degrees(R1)] == [26, 8, 30, 26, 14]
    assert tuple(SHAPE[index] - 1 for index in range(5)) == (26, 9, 30, 26, 15)

    first, first_record = signed_convolution(R0, Kbar)
    determinant = array("q", (4 * value for value in first))
    del first

    square_tensor, square_record = signed_convolution(R1, R1, square=True)
    a_stride = STRIDES[1]
    B_stride = STRIDES[4]
    # -C1*R1^2 = -(1-a+B)*R1^2.
    for index, value in enumerate(square_tensor):
        if not value:
            continue
        determinant[index] -= value
        determinant[index + a_stride] += value
        determinant[index + B_stride] -= value
    assert (min(determinant), max(determinant)) == (-1263602640, 1221821256)

    checksum = sha256()
    for value in determinant:
        checksum.update(struct.pack("<q", value))
    assert checksum.hexdigest() == (
        "ce411cab1010f925b58a484d63eb1ff4e70a76b895dbbccc1e8c23f8cf53e70b"
    )
    return determinant, {
        "R0_times_Kbar": first_record,
        "R1_square": square_record,
        "minimum_power_coefficient": min(determinant),
        "maximum_power_coefficient": max(determinant),
        "power_tensor_sha256_le_i64": checksum.hexdigest(),
    }


def b_bernstein_row(power_tensor, index):
    degree = SHAPE[-1] - 1
    denominator = lcm(*(comb(degree, power) for power in range(degree + 1)))
    weights = [
        comb(index, power) * (denominator // comb(degree, power))
        if power <= index else 0
        for power in range(degree + 1)
    ]
    result = [0] * OTHER_SIZE
    for power in range(index + 1):
        weight = weights[power]
        offset = power * OTHER_SIZE
        for inner in range(OTHER_SIZE):
            result[inner] += weight * power_tensor[offset + inner]
    return result


def scale_to_integer_box(values):
    # Clear a common positive denominator after a->a/128, v->v/128,
    # t->t/32.  The y and B boxes are already unit intervals.
    y_size, a_size, v_size, t_size = OTHER_SHAPE
    result = [0] * len(values)
    index = 0
    for t_degree in range(t_size):
        t_scale = 32 ** (t_size - 1 - t_degree)
        for v_degree in range(v_size):
            v_scale = 128 ** (v_size - 1 - v_degree)
            for a_degree in range(a_size):
                a_scale = 128 ** (a_size - 1 - a_degree)
                scale_factor = t_scale * v_scale * a_scale
                for _ in range(y_size):
                    result[index] = values[index] * scale_factor
                    index += 1
    return result


def transform_axis(values, shape, axis):
    """Integer transform with the sign of the rational Bernstein controls."""
    length = shape[axis]
    degree = length - 1
    stride = prod(shape[:axis])
    block = stride * length
    kernel = [factorial(degree) // factorial(offset) for offset in range(length)]
    input_weights = [factorial(degree - exponent) for exponent in range(length)]
    result = [0] * len(values)
    for start in range(0, len(values), block):
        for offset in range(stride):
            line = [
                values[start + offset + exponent * stride] * input_weights[exponent]
                for exponent in range(length)
            ]
            for target in range(length):
                result[start + offset + target * stride] = sum(
                    line[exponent] * kernel[target - exponent]
                    for exponent in range(target + 1)
                )
    return result


def certify_row(values):
    transformed = scale_to_integer_box(values)
    for axis in range(len(OTHER_SHAPE)):
        transformed = transform_axis(transformed, OTHER_SHAPE, axis)
    minimum = min(transformed)
    negative = sum(value < 0 for value in transformed)
    zeros = sum(value == 0 for value in transformed)
    checksum = sha256()
    for value in transformed:
        encoded = str(value).encode("ascii")
        checksum.update(len(encoded).to_bytes(4, "big"))
        checksum.update(encoded)
    return {
        "minimum": minimum,
        "negative_controls": negative,
        "zero_controls": zeros,
        "positive_controls": len(transformed) - zeros - negative,
        "maximum_bit_length": max(value.bit_length() for value in transformed),
        "sha256": checksum.hexdigest(),
    }


def determinant_bernstein_record(power_tensor):
    rows = []
    combined = sha256()
    for index in range(SHAPE[-1]):
        record = certify_row(b_bernstein_row(power_tensor, index))
        assert record["minimum"] == 0
        assert record["negative_controls"] == 0
        assert record["zero_controls"] == 810
        assert record["sha256"] == EXPECTED_ROW_SHA256[index]
        rows.append(record)
        combined.update(index.to_bytes(2, "big"))
        combined.update(bytes.fromhex(record["sha256"]))
    assert combined.hexdigest() == (
        "a67b71d9eb45d916cd832016834eaffe30b9bb3b46bb3142a245769fb1d57e52"
    )
    return {
        "tensor_shape_y_a_v_t_B": list(SHAPE),
        "controls": TOTAL_SIZE,
        "positive_controls": sum(row["positive_controls"] for row in rows),
        "zero_controls": sum(row["zero_controls"] for row in rows),
        "negative_controls": 0,
        "B_row_sha256": [row["sha256"] for row in rows],
        "combined_row_sha256": combined.hexdigest(),
        "maximum_control_bit_length": max(row["maximum_bit_length"] for row in rows),
    }


def main():
    C1, R0, R1, Kbar = build_kernels()
    assert digest(C1) == "d0cdb7bd781c988d3436ce0b15096c8c10e3f891e3aeec5b5b25d21285207922"
    r0_record = scaled_bernstein_record(
        R0,
        "9e5940aec396a41fb98e114e07d106f699e31c411f3abbc875275020584a8042",
        strict=False,
    )
    kbar_record = scaled_bernstein_record(
        Kbar,
        "c00eecdb62d3a5a775e34d421dd10af7fac0eb9f1a73ec6a06efdc17f976aabc",
        strict=True,
    )
    assert (r0_record["controls"], r0_record["positive_controls"]) == (184320, 182400)
    assert kbar_record["controls"] == kbar_record["positive_controls"] == 108864

    power_tensor, convolution = determinant_power_tensor(R0, R1, Kbar)
    determinant_record = determinant_bernstein_record(power_tensor)
    assert determinant_record["controls"] == 3615840
    assert determinant_record["positive_controls"] == 3602880
    assert determinant_record["zero_controls"] == 12960

    import json
    print(json.dumps({
        "schema": "amra.opg1757.round7.rlp-root-gram-certificate.v1",
        "domain": {
            "chart": "q0-maximal small-direction blow-up x=B*v*t*y",
            "box": "0<=y<=1, 0<=a<=1/128, 0<=B<=1, 0<=v<=1/128, 0<=t<=1/32",
            "root_coordinate": "w=(1+t*y)*(1+t*v*y)*z-(t^2*v*y^2+2*t*v*y+v^2*y-2*v*y+v+y)",
        },
        "kernel_identity": {
            "r0": "B*R0",
            "r1": "B*R1",
            "lower_minor": "4*y^2*B^3*v^2*C2*F4^2*Kbar",
            "four_times_gram_determinant": "y^2*B^4*v^2*C2*F4^2*D4",
            "D4": "4*R0*Kbar-(1-a+B)*R1^2",
        },
        "R0_bernstein": r0_record,
        "Kbar_bernstein": kbar_record,
        "D4_power_convolution": convolution,
        "D4_bernstein": determinant_record,
        "conclusion": "the tridiagonal root Gram is positive semidefinite throughout the stated local box, so the normalized q0-chart polynomial is nonnegative there for every real w",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "this closes the exact small-direction singular box only; the complementary compact projective region, the full q3:RLP chamber, the generic Delta_b sign, and OPG-1757 remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
