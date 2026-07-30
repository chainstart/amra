"""Exact two-star extension certificate for the OPG-1757 frontier.

The fixed nine-vertex base graph has one inherited edge pair ``(e, f)``.
This module appends

* two mutually nonadjacent star vertices with arbitrary base-only
  neighbourhoods ``R, Q``; and
* an arbitrary number ``t >= 0`` of mutually nonadjacent false twins with
  the recorded five-vertex neighbourhood ``S``.

Only the inherited pair is certified.  The two arbitrary stars and all
repeated twins have no edges among themselves.

The exact kernel accumulates selected incident-edge masks ``A, B`` and then
uses a two-dimensional subset zeta transform to cover every unordered pair
of the 512 possible neighbourhoods.  Its output contains the first five
normalized Krylov values for all four forced-edge channels.  Since every
nonidentity part of the fixed ``S`` transfer merges at least two of the at
most five ``S``-blocks, ``(T_S - 6I)^5 = 0`` on every base partition.
Consequently those five values determine each count for every integer
``t >= 0``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
from typing import Iterator, Mapping, Sequence


CERTIFICATE_SCHEMA = "amra.opg1757.two-star-defect.v1"
KERNEL_MAGIC = b"AM2SDP1\n"
BASE_GRAPH6 = "H?`bM~^"
INHERITED_EDGE_PAIR = (0, 2)
REPEATED_FALSE_TWIN_NEIGHBOURHOOD = (1, 5, 6, 7, 8)
BASE_VERTEX_COUNT = 9
KERNEL_BASE_EDGES = (
    (0, 4),
    (1, 5),
    (2, 5),
    (1, 6),
    (2, 6),
    (5, 6),
    (0, 7),
    (1, 7),
    (3, 7),
    (4, 7),
    (5, 7),
    (6, 7),
    (0, 8),
    (1, 8),
    (3, 8),
    (4, 8),
    (5, 8),
    (6, 8),
    (7, 8),
)
MASK_COUNT = 1 << BASE_VERTEX_COUNT
UNORDERED_MASK_PAIR_COUNT = MASK_COUNT * (MASK_COUNT + 1) // 2
LEGAL_SELECTED_EDGE_PAIR_COUNT = 20_823_456
COUNT_CHANNEL_NAMES = (
    "forest_count",
    "forest_count_e",
    "forest_count_f",
    "forest_count_ef",
)
KRYLOV_ORDER = 5
COUNT_POWER_BASE = 6
COUNT_NORMALIZATION = COUNT_POWER_BASE**4
MARGIN_POWER_BASE = COUNT_POWER_BASE**2
MARGIN_NORMALIZATION = COUNT_NORMALIZATION**2
KERNEL_COLUMN_COUNT = 2 + len(COUNT_CHANNEL_NAMES) * KRYLOV_ORDER
RATIO_SAMPLE_TWIN_COUNTS = (0, 1, 2, 4, 10, 25, 100, 187, 1000, 10_000)
EXPECTED_CATEGORY_COUNTS = {
    "all_nine_binomial_coefficients_strictly_positive": 83_040,
    "nonnegative_first_zero_at_degree_6": 6_588,
    "nonnegative_first_zero_at_degree_7": 41_700,
    "mixed_or_negative": 0,
}
EXPECTED_CLOSEST_MASK_PAIR_AT_10000 = (17, 36)
EXPECTED_CLOSEST_NEIGHBOURHOODS_AT_10000 = ((0, 4), (2, 5))
COMPILE_FLAGS = ("-O3", "-std=c++20")


class TwoStarCertificateError(RuntimeError):
    """Raised when the two-star exact certificate fails closed."""


@dataclass(frozen=True)
class CountClosedForm:
    """Represent ``base**t * P(t) / denominator`` exactly."""

    power_base: int
    denominator: int
    polynomial_coefficients: tuple[int, ...]

    def evaluate(self, twin_count: int) -> int:
        if type(twin_count) is not int or twin_count < 0:
            raise ValueError("twin_count must be a non-negative integer")
        polynomial = sum(
            coefficient * twin_count**degree
            for degree, coefficient in enumerate(
                self.polynomial_coefficients
            )
        )
        numerator = self.power_base**twin_count * polynomial
        quotient, remainder = divmod(numerator, self.denominator)
        if remainder:
            raise TwoStarCertificateError(
                f"closed form is nonintegral at t={twin_count}"
            )
        return quotient

    def as_dict(self) -> dict[str, object]:
        return {
            "power_base": self.power_base,
            "denominator": self.denominator,
            "polynomial_coefficients": list(
                self.polynomial_coefficients
            ),
        }


@dataclass(frozen=True)
class _KernelRow:
    first_mask: int
    second_mask: int
    count_newton_coefficients: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class _KernelMetadata:
    row_count: int
    column_count: int
    legal_selected_edge_pair_count: int
    output_sha256: str


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("utf-8")


def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(_canonical_json_bytes(payload))
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def _decode_compact_graph6(record: str) -> tuple[tuple[int, int], ...]:
    value = record.strip()
    if not value or value[0] == "~":
        raise TwoStarCertificateError("unsupported compact graph6 record")
    order = ord(value[0]) - 63
    if order != BASE_VERTEX_COUNT:
        raise TwoStarCertificateError(
            f"base graph order changed: {order}"
        )
    required_bits = order * (order - 1) // 2
    required_characters = (required_bits + 5) // 6
    if len(value) != required_characters + 1:
        raise TwoStarCertificateError("graph6 payload length is invalid")
    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        if not 0 <= encoded < 64:
            raise TwoStarCertificateError(
                "graph6 contains an invalid character"
            )
        bits.extend(
            (encoded >> shift) & 1 for shift in range(5, -1, -1)
        )
    possible_edges = (
        (left, right)
        for right in range(1, order)
        for left in range(right)
    )
    return tuple(
        edge
        for bit, edge in zip(bits[:required_bits], possible_edges)
        if bit
    )


def _mask_neighbourhood(mask: int) -> tuple[int, ...]:
    if type(mask) is not int or not 0 <= mask < MASK_COUNT:
        raise ValueError("mask must be an integer in [0, 512)")
    return tuple(
        vertex
        for vertex in range(BASE_VERTEX_COUNT)
        if mask & (1 << vertex)
    )


def _kernel_path() -> Path:
    path = Path(__file__).resolve().with_name(
        "opg_uniform_forest_two_star_kernel.cpp"
    )
    if not path.is_file():
        raise TwoStarCertificateError(
            f"two-star exact kernel is unavailable: {path}"
        )
    return path


def _compiler_record() -> dict[str, object]:
    compiler_name = shutil.which("g++")
    if compiler_name is None:
        raise TwoStarCertificateError(
            "g++ is required for the exact two-star kernel"
        )
    compiler = Path(compiler_name).resolve()
    try:
        completed = subprocess.run(
            [str(compiler), "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise TwoStarCertificateError(
            f"failed to inspect g++: {error}"
        ) from error
    first_line = completed.stdout.splitlines()
    if not first_line:
        raise TwoStarCertificateError("g++ returned an empty version")
    return {
        "path": str(compiler),
        "sha256": _file_sha256(compiler),
        "version_first_line": first_line[0],
        "compile_flags": list(COMPILE_FLAGS),
    }


def _compile_and_run_kernel(
    output_path: Path,
    compiler_record: Mapping[str, object],
) -> str:
    compiler = Path(str(compiler_record["path"]))
    kernel = _kernel_path()
    with tempfile.TemporaryDirectory(
        prefix="amra-opg1757-two-star-build-"
    ) as temporary_directory:
        executable = Path(temporary_directory) / "two-star-kernel"
        compile_command = [
            str(compiler),
            *COMPILE_FLAGS,
            str(kernel),
            "-o",
            str(executable),
        ]
        try:
            subprocess.run(
                compile_command,
                check=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            completed = subprocess.run(
                [str(executable), str(output_path)],
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )
        except subprocess.CalledProcessError as error:
            diagnostic = (
                error.stderr.strip()
                or error.stdout.strip()
                or str(error)
            )
            raise TwoStarCertificateError(
                f"two-star exact kernel failed: {diagnostic}"
            ) from error
        except (OSError, subprocess.TimeoutExpired) as error:
            raise TwoStarCertificateError(
                f"two-star exact kernel could not run: {error}"
            ) from error
    return completed.stdout.strip()


def _read_kernel_rows(
    path: Path,
) -> tuple[_KernelMetadata, Iterator[_KernelRow]]:
    if not path.is_file():
        raise TwoStarCertificateError("kernel output is unavailable")
    output_sha256 = _file_sha256(path)
    handle = path.open("rb")
    magic = handle.read(len(KERNEL_MAGIC))
    if magic != KERNEL_MAGIC:
        handle.close()
        raise TwoStarCertificateError("kernel output magic is invalid")
    header = handle.read(3 * 8)
    if len(header) != 3 * 8:
        handle.close()
        raise TwoStarCertificateError("kernel output header is truncated")
    row_count, column_count, legal_pair_count = struct.unpack(
        "<qqq", header
    )
    expected_size = (
        len(KERNEL_MAGIC)
        + len(header)
        + row_count * column_count * 8
    )
    if (
        row_count != UNORDERED_MASK_PAIR_COUNT
        or column_count != KERNEL_COLUMN_COUNT
        or legal_pair_count != LEGAL_SELECTED_EDGE_PAIR_COUNT
        or path.stat().st_size != expected_size
    ):
        handle.close()
        raise TwoStarCertificateError(
            "kernel output dimensions/counts are invalid"
        )
    metadata = _KernelMetadata(
        row_count,
        column_count,
        legal_pair_count,
        output_sha256,
    )

    def iterator() -> Iterator[_KernelRow]:
        row_struct = struct.Struct(f"<{column_count}q")
        try:
            expected_first = 0
            expected_second = 0
            for _ in range(row_count):
                raw = handle.read(row_struct.size)
                if len(raw) != row_struct.size:
                    raise TwoStarCertificateError(
                        "kernel output row is truncated"
                    )
                values = row_struct.unpack(raw)
                first_mask, second_mask = values[:2]
                if (
                    first_mask != expected_first
                    or second_mask != expected_second
                ):
                    raise TwoStarCertificateError(
                        "kernel mask-pair ordering is incomplete"
                    )
                expected_second += 1
                if expected_second == MASK_COUNT:
                    expected_first += 1
                    expected_second = expected_first
                coefficients = tuple(
                    tuple(
                        values[
                            2 + channel * KRYLOV_ORDER:
                            2 + (channel + 1) * KRYLOV_ORDER
                        ]
                    )
                    for channel in range(len(COUNT_CHANNEL_NAMES))
                )
                yield _KernelRow(
                    first_mask,
                    second_mask,
                    coefficients,
                )
            if handle.read(1):
                raise TwoStarCertificateError(
                    "kernel output has trailing bytes"
                )
        finally:
            handle.close()

    return metadata, iterator()


def _evaluate_newton(
    coefficients: Sequence[int],
    value: int,
) -> int:
    if len(coefficients) != KRYLOV_ORDER:
        raise ValueError("count Newton form must have five coefficients")
    return sum(
        coefficient * math.comb(value, degree)
        for degree, coefficient in enumerate(coefficients)
    )


def _forward_differences(values: Sequence[int]) -> tuple[int, ...]:
    differences = list(values)
    coefficients = []
    while differences:
        coefficients.append(differences[0])
        differences = [
            differences[index + 1] - differences[index]
            for index in range(len(differences) - 1)
        ]
    return tuple(coefficients)


def _margin_binomial_coefficients(
    count_newton_coefficients: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    if (
        len(count_newton_coefficients) != len(COUNT_CHANNEL_NAMES)
        or any(
            len(coefficients) != KRYLOV_ORDER
            for coefficients in count_newton_coefficients
        )
    ):
        raise ValueError("invalid four-channel Newton coefficients")
    values = []
    for twin_count in range(2 * KRYLOV_ORDER - 1):
        counts = tuple(
            _evaluate_newton(coefficients, twin_count)
            for coefficients in count_newton_coefficients
        )
        values.append(
            counts[1] * counts[2] - counts[0] * counts[3]
        )
    return _forward_differences(values)


def _multiply_polynomials(
    left: Sequence[Fraction],
    right: Sequence[Fraction],
) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] += (
                left_coefficient * right_coefficient
            )
    return result


def _shift_polynomial(
    coefficients: Sequence[Fraction],
    shift: int,
) -> list[Fraction]:
    result = [Fraction(0)] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        for output_degree in range(degree + 1):
            result[output_degree] += (
                coefficient
                * math.comb(degree, output_degree)
                * shift ** (degree - output_degree)
            )
    return result


def _normalize_polynomial(
    coefficients: Sequence[Fraction],
) -> tuple[tuple[int, ...], int]:
    denominator = math.lcm(
        *(coefficient.denominator for coefficient in coefficients)
    )
    integers = [
        int(coefficient * denominator)
        for coefficient in coefficients
    ]
    common_divisor = denominator
    for integer in integers:
        common_divisor = math.gcd(common_divisor, abs(integer))
    integers = [integer // common_divisor for integer in integers]
    denominator //= common_divisor
    while len(integers) > 1 and integers[-1] == 0:
        integers.pop()
    return tuple(integers), denominator


def _newton_to_closed_form(
    coefficients: Sequence[int],
    *,
    power_base: int,
    normalization: int,
) -> CountClosedForm:
    polynomial = [Fraction(0)] * len(coefficients)
    binomial_basis = [Fraction(1)]
    for degree, coefficient in enumerate(coefficients):
        for index, basis_coefficient in enumerate(binomial_basis):
            polynomial[index] += coefficient * basis_coefficient
        next_basis = _multiply_polynomials(
            binomial_basis,
            (Fraction(-degree), Fraction(1)),
        )
        binomial_basis = [
            basis_coefficient / (degree + 1)
            for basis_coefficient in next_basis
        ]
    polynomial = [
        coefficient / normalization
        for coefficient in polynomial
    ]
    integer_coefficients, denominator = _normalize_polynomial(
        polynomial
    )
    return CountClosedForm(
        power_base,
        denominator,
        integer_coefficients,
    )


def _ratio_from_newton(
    coefficients: Sequence[Sequence[int]],
    twin_count: int,
) -> Fraction:
    counts = tuple(
        _evaluate_newton(channel, twin_count)
        for channel in coefficients
    )
    right = counts[1] * counts[2]
    if right <= 0:
        raise TwoStarCertificateError(
            "right product is not strictly positive"
        )
    return Fraction(counts[0] * counts[3], right)


def _ratio_increment_certificate(
    count_forms: Sequence[CountClosedForm],
) -> dict[str, object]:
    rational_polynomials = [
        tuple(
            Fraction(coefficient, form.denominator)
            for coefficient in form.polynomial_coefficients
        )
        for form in count_forms
    ]
    left = _multiply_polynomials(
        rational_polynomials[0],
        rational_polynomials[3],
    )
    right = _multiply_polynomials(
        rational_polynomials[1],
        rational_polynomials[2],
    )
    next_left_current_right = _multiply_polynomials(
        _shift_polynomial(left, 1),
        right,
    )
    current_left_next_right = _multiply_polynomials(
        left,
        _shift_polynomial(right, 1),
    )
    increment = [
        next_left - next_right
        for next_left, next_right in zip(
            next_left_current_right,
            current_left_next_right,
        )
    ]
    coefficients, denominator = _normalize_polynomial(increment)
    if not all(coefficient > 0 for coefficient in coefficients):
        raise TwoStarCertificateError(
            "closest-family ratio is not symbolically increasing"
        )
    return {
        "denominator": denominator,
        "polynomial_coefficients": list(coefficients),
        "all_coefficients_strictly_positive": True,
        "conclusion": "ratio(t+1) > ratio(t) for every integer t >= 0",
    }


def _build_analysis(
    kernel_output: Path,
) -> dict[str, object]:
    metadata, rows = _read_kernel_rows(kernel_output)
    record_digest = hashlib.sha256()
    categories = {
        key: 0 for key in EXPECTED_CATEGORY_COUNTS
    }
    best_samples: dict[int, tuple[Fraction, int, int]] = {}
    closest_row: _KernelRow | None = None

    for row in rows:
        packed = struct.pack(
            f"<{KERNEL_COLUMN_COUNT}q",
            row.first_mask,
            row.second_mask,
            *(
                coefficient
                for channel in row.count_newton_coefficients
                for coefficient in channel
            ),
        )
        record_digest.update(packed)
        margin_coefficients = _margin_binomial_coefficients(
            row.count_newton_coefficients
        )
        if margin_coefficients[0] <= 0:
            raise TwoStarCertificateError(
                "a two-star margin is non-positive at t=0"
            )
        if any(coefficient < 0 for coefficient in margin_coefficients):
            categories["mixed_or_negative"] += 1
        elif all(
            coefficient > 0 for coefficient in margin_coefficients
        ):
            categories[
                "all_nine_binomial_coefficients_strictly_positive"
            ] += 1
        else:
            first_zero = next(
                index
                for index, coefficient in enumerate(margin_coefficients)
                if coefficient == 0
            )
            key = f"nonnegative_first_zero_at_degree_{first_zero}"
            if key not in categories:
                raise TwoStarCertificateError(
                    "unexpected zero pattern in a margin certificate"
                )
            categories[key] += 1

        for twin_count in RATIO_SAMPLE_TWIN_COUNTS:
            ratio = _ratio_from_newton(
                row.count_newton_coefficients,
                twin_count,
            )
            incumbent = best_samples.get(twin_count)
            if incumbent is None or ratio > incumbent[0]:
                best_samples[twin_count] = (
                    ratio,
                    row.first_mask,
                    row.second_mask,
                )
        if (
            row.first_mask,
            row.second_mask,
        ) == EXPECTED_CLOSEST_MASK_PAIR_AT_10000:
            closest_row = row

    if categories != EXPECTED_CATEGORY_COUNTS:
        raise TwoStarCertificateError(
            f"two-star category regression: {categories}"
        )
    closest_at_10000 = best_samples[10_000]
    if closest_at_10000[1:] != EXPECTED_CLOSEST_MASK_PAIR_AT_10000:
        raise TwoStarCertificateError(
            "closest t=10000 mask pair changed"
        )
    if closest_row is None:
        raise TwoStarCertificateError("closest-family row is missing")

    count_forms = tuple(
        _newton_to_closed_form(
            coefficients,
            power_base=COUNT_POWER_BASE,
            normalization=COUNT_NORMALIZATION,
        )
        for coefficients in closest_row.count_newton_coefficients
    )
    margin_binomial = _margin_binomial_coefficients(
        closest_row.count_newton_coefficients
    )
    margin_form = _newton_to_closed_form(
        margin_binomial,
        power_base=MARGIN_POWER_BASE,
        normalization=MARGIN_NORMALIZATION,
    )
    expected_margin = CountClosedForm(
        36,
        4,
        (7_348_320, 4_274_370, 957_684, 101_247, 4_848, 75),
    )
    if margin_form != expected_margin:
        raise TwoStarCertificateError(
            "closest-family margin polynomial regression"
        )
    for twin_count in range(9):
        normalized_counts = tuple(
            _evaluate_newton(coefficients, twin_count)
            for coefficients in closest_row.count_newton_coefficients
        )
        normalized_margin = (
            normalized_counts[1] * normalized_counts[2]
            - normalized_counts[0] * normalized_counts[3]
        )
        direct_margin = margin_form.evaluate(twin_count)
        expected_scaled = (
            MARGIN_POWER_BASE**twin_count
            * normalized_margin
        )
        expected_scaled, remainder = divmod(
            expected_scaled,
            MARGIN_NORMALIZATION,
        )
        if remainder:
            raise TwoStarCertificateError(
                "normalized margin is nonintegral"
            )
        if direct_margin != expected_scaled:
            raise TwoStarCertificateError(
                "closest-family margin form misses a Krylov sample"
            )

    rational_polynomials = [
        tuple(
            Fraction(coefficient, form.denominator)
            for coefficient in form.polynomial_coefficients
        )
        for form in count_forms
    ]
    right_polynomial = _multiply_polynomials(
        rational_polynomials[1],
        rational_polynomials[2],
    )
    margin_polynomial = tuple(
        Fraction(coefficient, margin_form.denominator)
        for coefficient in margin_form.polynomial_coefficients
    )
    asymptotic_coefficient = (
        margin_polynomial[-1] / right_polynomial[-1]
    )
    if asymptotic_coefficient != Fraction(7776, 734375):
        raise TwoStarCertificateError(
            "closest-family asymptotic gap regression"
        )

    ratio_samples = []
    for twin_count in RATIO_SAMPLE_TWIN_COUNTS:
        ratio, first_mask, second_mask = best_samples[twin_count]
        ratio_samples.append(
            {
                "twin_count": twin_count,
                "first_mask": first_mask,
                "second_mask": second_mask,
                "first_neighbourhood": list(
                    _mask_neighbourhood(first_mask)
                ),
                "second_neighbourhood": list(
                    _mask_neighbourhood(second_mask)
                ),
                "ratio_numerator": str(ratio.numerator),
                "ratio_denominator": str(ratio.denominator),
            }
        )

    closest_ratio = closest_at_10000[0]
    return {
        "kernel": {
            "row_count": metadata.row_count,
            "column_count": metadata.column_count,
            "legal_selected_edge_pair_count": (
                metadata.legal_selected_edge_pair_count
            ),
            "binary_output_sha256": metadata.output_sha256,
            "canonical_record_sha256": record_digest.hexdigest(),
        },
        "categories": categories,
        "ratio_sample_maxima": ratio_samples,
        "closest_family": {
            "criterion": (
                "maximum inherited-pair ratio among all 131328 "
                "unordered neighbourhood pairs at t=10000"
            ),
            "first_mask": closest_row.first_mask,
            "second_mask": closest_row.second_mask,
            "first_neighbourhood": list(
                _mask_neighbourhood(closest_row.first_mask)
            ),
            "second_neighbourhood": list(
                _mask_neighbourhood(closest_row.second_mask)
            ),
            "count_closed_forms": {
                name: form.as_dict()
                for name, form in zip(COUNT_CHANNEL_NAMES, count_forms)
            },
            "margin_closed_form": margin_form.as_dict(),
            "margin_polynomial_factorization": (
                "3*36^t/4 * "
                "(25*t^5 + 1616*t^4 + 33749*t^3 + "
                "319228*t^2 + 1424790*t + 2449440)"
            ),
            "ratio_at_t_10000": {
                "numerator": str(closest_ratio.numerator),
                "denominator": str(closest_ratio.denominator),
                "relative_gap_numerator": str(
                    closest_ratio.denominator
                    - closest_ratio.numerator
                ),
                "relative_gap_denominator": str(
                    closest_ratio.denominator
                ),
            },
            "ratio_increment_certificate": (
                _ratio_increment_certificate(count_forms)
            ),
            "asymptotic_relative_gap": {
                "coefficient_numerator": asymptotic_coefficient.numerator,
                "coefficient_denominator": (
                    asymptotic_coefficient.denominator
                ),
                "power_of_t": -3,
                "statement": (
                    "1-ratio(t) ~ (7776/734375)*t^(-3)"
                ),
            },
        },
    }


def build_two_star_certificate() -> dict[str, object]:
    """Recompute and return the complete compact two-star certificate."""

    edges = _decode_compact_graph6(BASE_GRAPH6)
    if edges != KERNEL_BASE_EDGES:
        raise TwoStarCertificateError(
            "graph6 edge list differs from the exact kernel"
        )
    if tuple(edges[index] for index in INHERITED_EDGE_PAIR) != (
        (0, 4),
        (2, 5),
    ):
        raise TwoStarCertificateError(
            "inherited edge-pair endpoints changed"
        )
    compiler = _compiler_record()
    with tempfile.TemporaryDirectory(
        prefix="amra-opg1757-two-star-output-"
    ) as temporary_directory:
        kernel_output = (
            Path(temporary_directory) / "two-star-kernel-output.bin"
        )
        kernel_stdout = _compile_and_run_kernel(
            kernel_output,
            compiler,
        )
        analysis = _build_analysis(kernel_output)

    module_path = Path(__file__).resolve()
    kernel_path = _kernel_path()
    return {
        "schema": CERTIFICATE_SCHEMA,
        "status": "certified",
        "scope": {
            "base_graph6": BASE_GRAPH6,
            "base_vertex_count": BASE_VERTEX_COUNT,
            "base_edge_count": len(edges),
            "base_edges": [list(edge) for edge in edges],
            "inherited_edge_pair_indexes": list(
                INHERITED_EDGE_PAIR
            ),
            "inherited_edge_pair_endpoints": [
                list(edges[index])
                for index in INHERITED_EDGE_PAIR
            ],
            "repeated_false_twin_neighbourhood": list(
                REPEATED_FALSE_TWIN_NEIGHBOURHOOD
            ),
            "repeated_false_twin_count": "every integer t >= 0",
            "additional_star_vertex_count": 2,
            "additional_star_neighbourhood_domain": (
                "all unordered pairs R,Q of subsets of the nine "
                "base vertices, with repetition allowed"
            ),
            "unordered_neighbourhood_pair_count": (
                UNORDERED_MASK_PAIR_COUNT
            ),
            "edges_among_all_added_vertices": 0,
            "all_edge_pairs_checked": False,
            "certified_edge_pair": "the inherited edge pair only",
        },
        "method": {
            "base_distribution": (
                "independent enumeration of all 2^19 base-edge subsets "
                "with four forced-edge channels"
            ),
            "two_star_accumulation": (
                "exact selected masks A,B followed by a two-dimensional "
                "subset zeta transform over R superset A and Q superset B"
            ),
            "selected_mask_legality": (
                "A is injective on current partition blocks, followed by "
                "B injective on the partition obtained after A"
            ),
            "fixed_transfer_recurrence": (
                "(T_S-6I)^5=0 because every nonidentity transition "
                "strictly decreases the number of blocks occupied by "
                "the five vertices of S"
            ),
            "count_form": (
                "C_i(t)=6^t/1296 * sum(k=0..4, "
                "d_i,k*binomial(t,k))"
            ),
            "margin_form": (
                "M(t)=36^t/1679616 * sum(k=0..8, "
                "h_k*binomial(t,k))"
            ),
            "all_t_positivity": (
                "for every unordered R,Q, h_0>0 and every h_k>=0"
            ),
            "kernel_stdout": kernel_stdout,
        },
        "summary": {
            "unordered_neighbourhood_pair_count": (
                UNORDERED_MASK_PAIR_COUNT
            ),
            "all_pairs_have_strictly_positive_margin_for_all_t": True,
            "selected_inherited_pair_is_never_a_counterexample": True,
            "whole_graph_family_counterexample_exhaustion_claimed": (
                False
            ),
            "category_counts": analysis["categories"],
        },
        "completeness": {
            "canonical_mask_pair_order": (
                "first_mask=0..511; second_mask=first_mask..511"
            ),
            **analysis["kernel"],
        },
        "ratio_sample_maxima": analysis["ratio_sample_maxima"],
        "closest_family": analysis["closest_family"],
        "implementation": [
            {
                "path": str(module_path),
                "sha256": _file_sha256(module_path),
            },
            {
                "path": str(kernel_path),
                "sha256": _file_sha256(kernel_path),
            },
        ],
        "toolchain": {
            "compiler": compiler,
        },
    }


def verify_two_star_certificate(payload: object) -> None:
    """Fail closed by rebuilding and byte-comparing the certificate."""

    if not isinstance(payload, dict):
        raise TwoStarCertificateError(
            "two-star certificate must be a JSON object"
        )
    if (
        payload.get("schema") != CERTIFICATE_SCHEMA
        or payload.get("status") != "certified"
    ):
        raise TwoStarCertificateError(
            "two-star certificate schema/status is invalid"
        )
    expected = build_two_star_certificate()
    if _canonical_json_bytes(payload) != _canonical_json_bytes(expected):
        raise TwoStarCertificateError(
            "two-star certificate differs from exact recomputation"
        )


def write_two_star_certificate(
    path: Path,
    payload: object,
) -> None:
    """Verify, then atomically persist a two-star certificate."""

    verify_two_star_certificate(payload)
    _atomic_write_json(path, payload)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Certify two arbitrary base-only star extensions of the "
            "OPG-1757 false-twin frontier."
        )
    )
    commands = parser.add_subparsers(dest="command", required=True)
    certify = commands.add_parser("certify")
    certify.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("certificate", type=Path)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "certify":
            payload = build_two_star_certificate()
            write_two_star_certificate(arguments.output, payload)
            result = {
                "status": "certified",
                "output": str(arguments.output),
                "unordered_neighbourhood_pair_count": (
                    UNORDERED_MASK_PAIR_COUNT
                ),
            }
        else:
            payload = json.loads(
                arguments.certificate.read_text(encoding="utf-8")
            )
            verify_two_star_certificate(payload)
            result = {
                "status": "verified",
                "certificate": str(arguments.certificate),
                "unordered_neighbourhood_pair_count": (
                    UNORDERED_MASK_PAIR_COUNT
                ),
            }
    except (
        json.JSONDecodeError,
        OSError,
        subprocess.SubprocessError,
        TwoStarCertificateError,
        TypeError,
        ValueError,
    ) as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
