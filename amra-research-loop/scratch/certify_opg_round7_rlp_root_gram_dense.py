#!/usr/bin/env python3
"""Exact dense Bernstein discovery for the q0-chart RLP root Gram.

The large products are formed by Kronecker substitution into base 2**64.
All input coefficients are integers, and separate positive/negative products
avoid signed carries.  The resulting 5-D coefficient tensor is transformed
one B-Bernstein row at a time; the remaining four axes use an integer,
sign-equivalent form of the power-to-Bernstein transform.
"""

from __future__ import annotations

from array import array
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial, lcm
import multiprocessing
from pathlib import Path
import struct
import sys
import time


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_mixed_three_negative import divide_polynomial  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    multiply,
    variable,
)
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    coefficient,
    common_monomial,
    divide_monomial,
)
from verify_rlp_projective_corner_reduction import (  # noqa: E402
    f4_factor,
    product,
    reconstruct_h1884,
    root_coordinates,
    scale,
    small_direction_faces,
)


# y,a,v,t are the fast axes and B is the outermost/slowest axis.  These are
# the exact output degrees of 4*R0*Kbar-C1*R1**2.
SHAPE = (27, 10, 31, 27, 16)
OTHER_SHAPE = SHAPE[:-1]
OTHER_SIZE = 27 * 10 * 31 * 27
TOTAL_SIZE = OTHER_SIZE * 16
SLOTS = (0, 1, 6, 7, 5)
DIGIT_BYTES = 8
PRODUCT_OPERANDS = ()


def strides(shape):
    result = []
    stride = 1
    for size in shape:
        result.append(stride)
        stride *= size
    return tuple(result)


STRIDES = strides(SHAPE)


def index_of(monomial):
    return sum(monomial[slot] * stride for slot, stride in zip(SLOTS, STRIDES))


def packed_sign(poly, positive):
    raw = bytearray(TOTAL_SIZE * DIGIT_BYTES)
    for monomial, value in poly.items():
        assert value.denominator == 1
        integer = value.numerator
        if (integer > 0) != positive:
            continue
        magnitude = abs(integer)
        assert magnitude < 1 << 64
        struct.pack_into("<Q", raw, index_of(monomial) * DIGIT_BYTES, magnitude)
    return int.from_bytes(raw, "little")


def multiply_packed(index):
    left, right = PRODUCT_OPERANDS[index]
    product_integer = left * right
    assert product_integer.bit_length() <= TOTAL_SIZE * 64
    return index, product_integer.to_bytes(TOTAL_SIZE * DIGIT_BYTES, "little")


def accumulate_raw(target, raw, multiplier):
    values = memoryview(raw).cast("Q")
    maximum = 0
    for index, value in enumerate(values):
        maximum = max(maximum, value)
        target[index] += multiplier * value
    return maximum


def signed_convolution(left, right, square=False):
    global PRODUCT_OPERANDS
    left_positive = packed_sign(left, True)
    left_negative = packed_sign(left, False)
    right_positive = packed_sign(right, True)
    right_negative = packed_sign(right, False)
    if square:
        assert left is right
        products = (
            (left_positive, left_positive, 1),
            (left_negative, left_negative, 1),
            (left_positive, left_negative, -2),
        )
    else:
        products = (
            (left_positive, right_positive, 1),
            (left_negative, right_negative, 1),
            (left_positive, right_negative, -1),
            (left_negative, right_positive, -1),
        )
    PRODUCT_OPERANDS = tuple((left, right) for left, right, _ in products)
    result = array("q", [0]) * TOTAL_SIZE
    maxima = [0] * len(products)
    context = multiprocessing.get_context("fork")
    with context.Pool(processes=len(products)) as pool:
        for index, raw in pool.imap_unordered(multiply_packed, range(len(products))):
            maxima[index] = accumulate_raw(result, raw, products[index][2])
    PRODUCT_OPERANDS = ()
    assert max(maxima) < 1 << 63
    return result, tuple(maxima)


def build_rows():
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
    R0 = divide_monomial(rows[0], common_monomial(rows[0]))
    R1 = divide_monomial(rows[1], common_monomial(rows[1]))
    reduced_r3 = divide_monomial(rows[3], (1, 0, 0, 0, 0, 1, 1, 0))
    H = scale(
        divide_polynomial(divide_polynomial(reduced_r3, C2), f4_factor()),
        Fraction(-1, 2),
    )
    K24 = add(
        multiply(C1, rows[2]),
        product(C2, multiply(H, H)),
        -1,
    )
    Kbar = divide_monomial(K24, common_monomial(K24))
    return R0, R1, Kbar


def determinant_power_tensor(R0, R1, Kbar):
    started = time.monotonic()
    first, first_maxima = signed_convolution(R0, Kbar)
    print("R0*Kbar", time.monotonic() - started, first_maxima, flush=True)
    determinant = array("q", (4 * value for value in first))
    del first

    started = time.monotonic()
    square_tensor, square_maxima = signed_convolution(R1, R1, square=True)
    print("R1^2", time.monotonic() - started, square_maxima, flush=True)
    a_stride = STRIDES[1]
    B_stride = STRIDES[4]
    # -C1*R1^2 = -(1-a+B)*R1^2.
    for index, value in enumerate(square_tensor):
        if not value:
            continue
        determinant[index] -= value
        determinant[index + a_stride] += value
        determinant[index + B_stride] -= value
    return determinant


def b_bernstein_row(power_tensor, index):
    degree = SHAPE[-1] - 1
    denominator = 1
    for power in range(degree + 1):
        denominator = lcm(denominator, comb(degree, power))
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
    # Clear the common denominator after a->a/128, v->v/128, t->t/32.
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
    length = shape[axis]
    degree = length - 1
    stride = 1
    for size in shape[:axis]:
        stride *= size
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
                total = 0
                for exponent in range(target + 1):
                    total += line[exponent] * kernel[target - exponent]
                result[start + offset + target * stride] = total
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
    return minimum, negative, zeros, checksum.hexdigest()


def main():
    R0, R1, Kbar = build_rows()
    power_tensor = determinant_power_tensor(R0, R1, Kbar)
    print("power min/max", min(power_tensor), max(power_tensor), flush=True)
    for index in range(SHAPE[-1]):
        started = time.monotonic()
        record = certify_row(b_bernstein_row(power_tensor, index))
        print("B row", index, record, "seconds", time.monotonic() - started, flush=True)
        assert record[1] == 0


if __name__ == "__main__":
    main()
