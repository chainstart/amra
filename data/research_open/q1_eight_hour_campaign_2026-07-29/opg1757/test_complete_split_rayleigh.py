"""Independent checks for complete_split_rayleigh.py."""

from __future__ import annotations

import importlib.util
import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


MODULE_PATH = Path(__file__).with_name("complete_split_rayleigh.py")
CERTIFICATE_PATH = Path(__file__).with_name(
    "complete_split_rayleigh_certificate.json"
)
S7_CERTIFICATE_PATH = Path(__file__).with_name(
    "complete_split_rayleigh_s7_certificate.json"
)
GENERAL_MODULE_PATH = Path(__file__).with_name(
    "general_s_disjoint_low_degree.py"
)
GENERAL_CERTIFICATE_PATH = Path(__file__).with_name(
    "general_s_disjoint_alpha2_beta4_12_certificate.json"
)
EXTENDED_MODULE_PATH = Path(__file__).with_name(
    "general_s_disjoint_extended.py"
)
EXTENDED_CERTIFICATE_PATH = Path(__file__).with_name(
    "general_s_disjoint_alpha2_beta4_24_alpha3_beta2_24_certificate.json"
)
TP2_MODULE_PATH = Path(__file__).with_name("tp2_barrier_search.py")
TP2_CERTIFICATE_PATH = Path(__file__).with_name(
    "tp2_barrier_certificate.json"
)
FIXED_PAGE_MODULE_PATH = Path(__file__).with_name(
    "fixed_page_union_formula.py"
)
FIXED_PAGE_CERTIFICATE_PATH = Path(__file__).with_name(
    "fixed_page_union_certificate.json"
)
B4_UNIFORM_MODULE_PATH = Path(__file__).with_name(
    "verify_b4_uniform_positivity.py"
)
B4_UNIFORM_AUDIT_PATH = Path(__file__).with_name(
    "b4_uniform_positivity_audit.json"
)
FIVE_PAGE_MODULE_PATH = Path(__file__).with_name(
    "five_page_union_formula.py"
)
FIVE_PAGE_CERTIFICATE_PATH = Path(__file__).with_name(
    "five_page_union_certificate.json"
)
B5_UNIFORM_MODULE_PATH = Path(__file__).with_name(
    "verify_b5_uniform_positivity.py"
)
B5_UNIFORM_AUDIT_PATH = Path(__file__).with_name(
    "b5_uniform_positivity_audit.json"
)
SIX_PAGE_MODULE_PATH = Path(__file__).with_name(
    "six_page_union_formula.py"
)
SIX_PAGE_CERTIFICATE_PATH = Path(__file__).with_name(
    "six_page_union_certificate.json"
)
B6_UNIFORM_MODULE_PATH = Path(__file__).with_name(
    "verify_b6_uniform_positivity.py"
)
B6_UNIFORM_AUDIT_PATH = Path(__file__).with_name(
    "b6_uniform_positivity_audit.json"
)
SEVEN_PAGE_MODULE_PATH = Path(__file__).with_name(
    "seven_page_union_formula.py"
)
SEVEN_PAGE_CERTIFICATE_PATH = Path(__file__).with_name(
    "seven_page_union_certificate.json"
)
B7_UNIFORM_MODULE_PATH = Path(__file__).with_name(
    "verify_b7_uniform_positivity.py"
)
B7_UNIFORM_AUDIT_PATH = Path(__file__).with_name(
    "b7_uniform_positivity_audit.json"
)
GENERAL_K_EXTREMAL_MODULE_PATH = Path(__file__).with_name(
    "verify_general_k_extremal_coefficients.py"
)
GENERAL_K_EXTREMAL_AUDIT_PATH = Path(__file__).with_name(
    "general_k_extremal_audit.json"
)
GENERAL_K_LOW_MODULE_PATH = Path(__file__).with_name(
    "verify_general_k_low_coefficients.py"
)
GENERAL_K_LOW_AUDIT_PATH = Path(__file__).with_name(
    "general_k_low_coefficients_audit.json"
)
F_LEADING_LAGRANGE_MODULE_PATH = Path(__file__).with_name(
    "verify_f_leading_lagrange.py"
)
F_LEADING_LAGRANGE_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_lagrange_audit.json"
)
F_LEADING_SWAP_MODULE_PATH = Path(__file__).with_name(
    "verify_f_leading_swap_obstruction.py"
)
F_LEADING_SWAP_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_swap_obstruction_audit.json"
)
F_LEADING_K4_OUTSIDE_MODULE_PATH = Path(__file__).with_name(
    "verify_f_leading_k4_outside_stability.py"
)
F_LEADING_K4_OUTSIDE_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_k4_outside_stability_audit.json"
)
F_LEADING_SERIES_MODULE_PATH = Path(__file__).with_name(
    "verify_f_leading_series_subdivision.py"
)
F_LEADING_SERIES_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_series_subdivision_audit.json"
)
F_LEADING_FIRST_ACTIVE_MODULE_PATH = Path(__file__).with_name(
    "verify_f_leading_first_active_potential.py"
)
F_LEADING_FIRST_ACTIVE_AUDIT_PATH = Path(__file__).with_name(
    "f_leading_first_active_potential_audit.json"
)

GENERAL_SPEC = importlib.util.spec_from_file_location(
    "general_s_disjoint_low_degree", GENERAL_MODULE_PATH
)
assert GENERAL_SPEC is not None and GENERAL_SPEC.loader is not None
general_s = importlib.util.module_from_spec(GENERAL_SPEC)
sys.modules[GENERAL_SPEC.name] = general_s
GENERAL_SPEC.loader.exec_module(general_s)
EXTENDED_SPEC = importlib.util.spec_from_file_location(
    "general_s_disjoint_extended", EXTENDED_MODULE_PATH
)
assert EXTENDED_SPEC is not None and EXTENDED_SPEC.loader is not None
extended = importlib.util.module_from_spec(EXTENDED_SPEC)
sys.modules[EXTENDED_SPEC.name] = extended
EXTENDED_SPEC.loader.exec_module(extended)
TP2_SPEC = importlib.util.spec_from_file_location(
    "tp2_barrier_search", TP2_MODULE_PATH
)
assert TP2_SPEC is not None and TP2_SPEC.loader is not None
tp2 = importlib.util.module_from_spec(TP2_SPEC)
sys.modules[TP2_SPEC.name] = tp2
TP2_SPEC.loader.exec_module(tp2)
FIXED_PAGE_SPEC = importlib.util.spec_from_file_location(
    "fixed_page_union_formula", FIXED_PAGE_MODULE_PATH
)
assert FIXED_PAGE_SPEC is not None and FIXED_PAGE_SPEC.loader is not None
fixed_page = importlib.util.module_from_spec(FIXED_PAGE_SPEC)
sys.modules[FIXED_PAGE_SPEC.name] = fixed_page
FIXED_PAGE_SPEC.loader.exec_module(fixed_page)
B4_UNIFORM_SPEC = importlib.util.spec_from_file_location(
    "verify_b4_uniform_positivity", B4_UNIFORM_MODULE_PATH
)
assert B4_UNIFORM_SPEC is not None and B4_UNIFORM_SPEC.loader is not None
b4_uniform = importlib.util.module_from_spec(B4_UNIFORM_SPEC)
sys.modules[B4_UNIFORM_SPEC.name] = b4_uniform
B4_UNIFORM_SPEC.loader.exec_module(b4_uniform)
FIVE_PAGE_SPEC = importlib.util.spec_from_file_location(
    "five_page_union_formula", FIVE_PAGE_MODULE_PATH
)
assert FIVE_PAGE_SPEC is not None and FIVE_PAGE_SPEC.loader is not None
five_page = importlib.util.module_from_spec(FIVE_PAGE_SPEC)
sys.modules[FIVE_PAGE_SPEC.name] = five_page
FIVE_PAGE_SPEC.loader.exec_module(five_page)
B5_UNIFORM_SPEC = importlib.util.spec_from_file_location(
    "verify_b5_uniform_positivity", B5_UNIFORM_MODULE_PATH
)
assert B5_UNIFORM_SPEC is not None and B5_UNIFORM_SPEC.loader is not None
b5_uniform = importlib.util.module_from_spec(B5_UNIFORM_SPEC)
sys.modules[B5_UNIFORM_SPEC.name] = b5_uniform
B5_UNIFORM_SPEC.loader.exec_module(b5_uniform)
SIX_PAGE_SPEC = importlib.util.spec_from_file_location(
    "six_page_union_formula", SIX_PAGE_MODULE_PATH
)
assert SIX_PAGE_SPEC is not None and SIX_PAGE_SPEC.loader is not None
six_page = importlib.util.module_from_spec(SIX_PAGE_SPEC)
sys.modules[SIX_PAGE_SPEC.name] = six_page
SIX_PAGE_SPEC.loader.exec_module(six_page)
B6_UNIFORM_SPEC = importlib.util.spec_from_file_location(
    "verify_b6_uniform_positivity", B6_UNIFORM_MODULE_PATH
)
assert B6_UNIFORM_SPEC is not None and B6_UNIFORM_SPEC.loader is not None
b6_uniform = importlib.util.module_from_spec(B6_UNIFORM_SPEC)
sys.modules[B6_UNIFORM_SPEC.name] = b6_uniform
B6_UNIFORM_SPEC.loader.exec_module(b6_uniform)
SEVEN_PAGE_SPEC = importlib.util.spec_from_file_location(
    "seven_page_union_formula", SEVEN_PAGE_MODULE_PATH
)
assert SEVEN_PAGE_SPEC is not None and SEVEN_PAGE_SPEC.loader is not None
seven_page = importlib.util.module_from_spec(SEVEN_PAGE_SPEC)
sys.modules[SEVEN_PAGE_SPEC.name] = seven_page
SEVEN_PAGE_SPEC.loader.exec_module(seven_page)
B7_UNIFORM_SPEC = importlib.util.spec_from_file_location(
    "verify_b7_uniform_positivity", B7_UNIFORM_MODULE_PATH
)
assert B7_UNIFORM_SPEC is not None and B7_UNIFORM_SPEC.loader is not None
b7_uniform = importlib.util.module_from_spec(B7_UNIFORM_SPEC)
sys.modules[B7_UNIFORM_SPEC.name] = b7_uniform
B7_UNIFORM_SPEC.loader.exec_module(b7_uniform)
GENERAL_K_EXTREMAL_SPEC = importlib.util.spec_from_file_location(
    "verify_general_k_extremal_coefficients",
    GENERAL_K_EXTREMAL_MODULE_PATH,
)
assert (
    GENERAL_K_EXTREMAL_SPEC is not None
    and GENERAL_K_EXTREMAL_SPEC.loader is not None
)
general_k_extremal = importlib.util.module_from_spec(GENERAL_K_EXTREMAL_SPEC)
sys.modules[GENERAL_K_EXTREMAL_SPEC.name] = general_k_extremal
GENERAL_K_EXTREMAL_SPEC.loader.exec_module(general_k_extremal)
GENERAL_K_LOW_SPEC = importlib.util.spec_from_file_location(
    "verify_general_k_low_coefficients",
    GENERAL_K_LOW_MODULE_PATH,
)
assert GENERAL_K_LOW_SPEC is not None and GENERAL_K_LOW_SPEC.loader is not None
general_k_low = importlib.util.module_from_spec(GENERAL_K_LOW_SPEC)
sys.modules[GENERAL_K_LOW_SPEC.name] = general_k_low
GENERAL_K_LOW_SPEC.loader.exec_module(general_k_low)
F_LEADING_LAGRANGE_SPEC = importlib.util.spec_from_file_location(
    "verify_f_leading_lagrange",
    F_LEADING_LAGRANGE_MODULE_PATH,
)
assert (
    F_LEADING_LAGRANGE_SPEC is not None
    and F_LEADING_LAGRANGE_SPEC.loader is not None
)
f_leading_lagrange = importlib.util.module_from_spec(
    F_LEADING_LAGRANGE_SPEC
)
sys.modules[F_LEADING_LAGRANGE_SPEC.name] = f_leading_lagrange
F_LEADING_LAGRANGE_SPEC.loader.exec_module(f_leading_lagrange)
F_LEADING_SWAP_SPEC = importlib.util.spec_from_file_location(
    "verify_f_leading_swap_obstruction",
    F_LEADING_SWAP_MODULE_PATH,
)
assert (
    F_LEADING_SWAP_SPEC is not None
    and F_LEADING_SWAP_SPEC.loader is not None
)
f_leading_swap = importlib.util.module_from_spec(F_LEADING_SWAP_SPEC)
sys.modules[F_LEADING_SWAP_SPEC.name] = f_leading_swap
F_LEADING_SWAP_SPEC.loader.exec_module(f_leading_swap)
F_LEADING_K4_OUTSIDE_SPEC = importlib.util.spec_from_file_location(
    "verify_f_leading_k4_outside_stability",
    F_LEADING_K4_OUTSIDE_MODULE_PATH,
)
assert (
    F_LEADING_K4_OUTSIDE_SPEC is not None
    and F_LEADING_K4_OUTSIDE_SPEC.loader is not None
)
f_leading_k4_outside = importlib.util.module_from_spec(
    F_LEADING_K4_OUTSIDE_SPEC
)
sys.modules[F_LEADING_K4_OUTSIDE_SPEC.name] = f_leading_k4_outside
F_LEADING_K4_OUTSIDE_SPEC.loader.exec_module(f_leading_k4_outside)
F_LEADING_SERIES_SPEC = importlib.util.spec_from_file_location(
    "verify_f_leading_series_subdivision",
    F_LEADING_SERIES_MODULE_PATH,
)
assert (
    F_LEADING_SERIES_SPEC is not None
    and F_LEADING_SERIES_SPEC.loader is not None
)
f_leading_series = importlib.util.module_from_spec(F_LEADING_SERIES_SPEC)
sys.modules[F_LEADING_SERIES_SPEC.name] = f_leading_series
F_LEADING_SERIES_SPEC.loader.exec_module(f_leading_series)
F_LEADING_FIRST_ACTIVE_SPEC = importlib.util.spec_from_file_location(
    "verify_f_leading_first_active_potential",
    F_LEADING_FIRST_ACTIVE_MODULE_PATH,
)
assert (
    F_LEADING_FIRST_ACTIVE_SPEC is not None
    and F_LEADING_FIRST_ACTIVE_SPEC.loader is not None
)
f_leading_first_active = importlib.util.module_from_spec(
    F_LEADING_FIRST_ACTIVE_SPEC
)
sys.modules[F_LEADING_FIRST_ACTIVE_SPEC.name] = f_leading_first_active
F_LEADING_FIRST_ACTIVE_SPEC.loader.exec_module(f_leading_first_active)
SPEC = importlib.util.spec_from_file_location("complete_split_rayleigh", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
csr = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = csr
SPEC.loader.exec_module(csr)


def brute_marked_counts(
    s: int,
    r: int,
    alpha: int,
    beta: int,
    first_edge: tuple[int, int],
    second_edge: tuple[int, int],
) -> tuple[int, int, int, int]:
    """Enumerate every edge subset, independently of the transfer code."""

    core_edges = list(itertools.combinations(range(s), 2))
    spoke_edges = [(core, s + page) for page in range(r) for core in range(s)]
    edges = core_edges + spoke_edges
    normalized_first = tuple(sorted(first_edge))
    normalized_second = tuple(sorted(second_edge))
    z = z_e = z_f = z_ef = 0

    for bits in range(1 << len(edges)):
        parent = list(range(s + r))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        selected: list[tuple[int, int]] = []
        acyclic = True
        weight = 1
        for index, edge in enumerate(edges):
            if not bits & (1 << index):
                continue
            u, v = edge
            root_u, root_v = find(u), find(v)
            if root_u == root_v:
                acyclic = False
                break
            parent[root_u] = root_v
            selected.append(tuple(sorted(edge)))
            weight *= alpha if index < len(core_edges) else beta
        if not acyclic:
            continue
        has_e = normalized_first in selected
        has_f = normalized_second in selected
        z += weight
        z_e += weight * has_e
        z_f += weight * has_f
        z_ef += weight * has_e * has_f
    return z, z_e, z_f, z_ef


def representative_edges(
    s: int, class_name: str
) -> tuple[tuple[int, int], tuple[int, int]]:
    page_zero = s
    page_one = s + 1
    return {
        "core_core_adjacent": ((0, 1), (0, 2)),
        "core_core_disjoint": ((0, 1), (2, 3)),
        "core_spoke_incident": ((0, 1), (0, page_zero)),
        "core_spoke_nonincident": ((0, 1), (2, page_zero)),
        "spoke_spoke_same_page": ((0, page_zero), (1, page_zero)),
        "spoke_spoke_different_pages_same_core": (
            (0, page_zero),
            (0, page_one),
        ),
        "spoke_spoke_different_pages_different_core": (
            (0, page_zero),
            (1, page_one),
        ),
    }[class_name]


def test_partition_counts_and_component_tree_formula() -> None:
    assert len(csr.set_partitions(3)) == 5
    assert len(csr.set_partitions(4)) == 15
    assert csr.component_tree_weight(1, 0) == 1
    # A two-core, one-page component is a weighted triangle.
    assert csr.component_tree_weight(2, 1) == (
        csr.BETA**2 + 2 * csr.ALPHA * csr.BETA
    )


def test_transfer_counts_against_full_subset_enumeration() -> None:
    s, r, alpha, beta = 3, 2, 2, 3
    transfer = csr.CompleteSplitTransfer(s)
    for class_name, pair_class in csr.pair_classes(s).items():
        first, second = representative_edges(s, class_name)
        brute = brute_marked_counts(s, r, alpha, beta, first, second)
        t_value = r - pair_class.page_shift
        exact = tuple(
            int(
                transfer.exact_count_at_t(spec, t_value).subs(
                    {csr.ALPHA: alpha, csr.BETA: beta}
                )
            )
            for spec in (
                pair_class.z,
                pair_class.z_e,
                pair_class.z_f,
                pair_class.z_ef,
            )
        )
        assert exact == brute, class_name
        assert exact[1] * exact[2] - exact[0] * exact[3] >= 0


def test_all_r_symbolic_certificate_for_s3() -> None:
    certificate = csr.build_certificate([3], include_rows=False)
    classes = certificate["s_values"]["3"]["edge_pair_classes"]
    assert len(classes) == 6
    for class_certificate in classes.values():
        assert class_certificate["minimum_binomial_coefficient"] != "0"
        assert len(class_certificate["sha256"]) == 64


def test_newton_conversion_handles_negative_power_basis_coefficients() -> None:
    polynomial = sp.Poly(
        csr.ALPHA * (csr.T**2 - csr.T + 2), csr.ALPHA, csr.BETA, csr.T
    )
    rows = csr.newton_rows(polynomial)
    assert all(coefficient >= 0 for _, _, _, coefficient in rows)
    assert rows == [(1, 0, 0, 2), (1, 0, 2, 2)]


def test_static_json_rows_roundtrip_and_digest() -> None:
    """Audit every saved coefficient row independently of generation."""

    for certificate_path in (CERTIFICATE_PATH, S7_CERTIFICATE_PATH):
        saved = json.loads(certificate_path.read_text(encoding="utf-8"))
        for s_certificate in saved["s_values"].values():
            for class_certificate in s_certificate["edge_pair_classes"].values():
                _audit_finite_s_class_certificate(class_certificate)


def _audit_finite_s_class_certificate(
    class_certificate: dict[str, object]
) -> None:
    serialized_rows = class_certificate["rows_alpha_beta_binomial_t"]
    rows = [
        (
            int(alpha_degree),
            int(beta_degree),
            int(order),
            sp.Rational(coefficient),
        )
        for alpha_degree, beta_degree, order, coefficient in serialized_rows
    ]
    assert rows
    assert all(coefficient > 0 for _, _, _, coefficient in rows)

    # Rebuild the ordinary polynomial and transform it back.  This detects a
    # corrupt row, wrong basis index, or truncated JSON.
    expression = sum(
        coefficient
        * csr.ALPHA**alpha_degree
        * csr.BETA**beta_degree
        * sp.expand_func(sp.binomial(csr.T, order))
        for alpha_degree, beta_degree, order, coefficient in rows
    )
    roundtrip = csr.newton_rows(
        sp.Poly(sp.expand(expression), csr.ALPHA, csr.BETA, csr.T)
    )
    assert roundtrip == rows

    digest_payload = json.dumps(
        {
            "denominator": class_certificate["denominator"],
            "rows": serialized_rows,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert (
        hashlib.sha256(digest_payload).hexdigest()
        == class_certificate["sha256"]
    )


def test_general_s_low_degree_static_certificate() -> None:
    saved = json.loads(GENERAL_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    rows = saved["rows_beta_tbin_ubin_coefficient"]
    assert rows
    assert all(sp.Rational(row[3]) > 0 for row in rows)
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_rows"]

    by_beta: dict[int, sp.Expr] = {}
    for beta_degree, t_order, u_order, coefficient in rows:
        by_beta.setdefault(int(beta_degree), sp.S.Zero)
        by_beta[int(beta_degree)] += (
            sp.Rational(coefficient)
            * sp.expand_func(sp.binomial(general_s.T, int(t_order)))
            * sp.expand_func(sp.binomial(general_s.U, int(u_order)))
        )
    assert set(by_beta) == set(range(4, 13))
    for beta_degree, expression in by_beta.items():
        ordinary = sp.sympify(
            saved["ordinary_layer_formulas"][str(beta_degree)],
            locals={"s": general_s.S, "t": general_s.T},
        )
        assert (
            sp.expand(
                expression
                - ordinary.subs(general_s.S, general_s.U + 4)
            )
            == 0
        )


def test_general_s_transfer_rederives_beta4_through_beta6() -> None:
    """A quick fresh derivation, independent of the saved beta<=12 JSON."""

    fresh = general_s.build_certificate(max_beta=6)
    saved = json.loads(GENERAL_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    expected_rows = [
        row
        for row in saved["rows_beta_tbin_ubin_coefficient"]
        if int(row[0]) <= 6
    ]
    assert fresh["rows_beta_tbin_ubin_coefficient"] == expected_rows


def test_general_s_layers_match_finite_s_margin_normalization() -> None:
    """Rule out a denominator or coefficient-layer normalization mismatch."""

    saved = json.loads(GENERAL_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    formulas = {
        beta_degree: sp.sympify(
            saved["ordinary_layer_formulas"][str(beta_degree)],
            locals={"s": general_s.S, "t": general_s.T},
        )
        for beta_degree in range(4, 13)
    }
    for s in (4, 5, 6):
        transfer = csr.CompleteSplitTransfer(s)
        pair_class = csr.pair_classes(s)["core_core_disjoint"]
        normalized = sp.cancel(
            transfer.reduced_rayleigh_margin(pair_class)
            * transfer.lambda_ ** (2 * s - 4)
        )
        numerator, denominator = normalized.as_numer_denom()
        assert denominator == 1
        polynomial = sp.Poly(sp.expand(numerator), csr.ALPHA, csr.BETA)
        for beta_degree, formula in formulas.items():
            finite_layer = polynomial.coeff_monomial(
                csr.ALPHA**2 * csr.BETA**beta_degree
            )
            general_layer = formula.subs(
                {general_s.S: s, general_s.T: csr.T}
            )
            assert sp.expand(finite_layer - general_layer) == 0


def test_extended_alpha2_alpha3_static_certificate() -> None:
    saved = json.loads(EXTENDED_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    assert saved["beta_degrees_by_alpha"] == {
        "2": [4, 24],
        "3": [2, 24],
    }
    for alpha_degree in ("2", "3"):
        section = saved["alpha_degrees"][alpha_degree]
        rows = section["rows_beta_tbin_ubin_coefficient"]
        assert rows
        assert section["negative_rows"] == []
        assert section["all_newton_coefficients_nonnegative"] is True
        assert all(int(row[3]) > 0 for row in rows)
        payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
        assert hashlib.sha256(payload).hexdigest() == section["sha256_rows"]
        minimum = 4 if alpha_degree == "2" else 2
        assert section["beta_degrees"] == [minimum, 24]
        assert {int(row[0]) for row in rows} == set(range(minimum, 25))

    # The independent bounded-grid implementation must reproduce every old
    # alpha^2 row, not merely agree on signs.
    old = json.loads(GENERAL_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    old_rows = old["rows_beta_tbin_ubin_coefficient"]
    extended_alpha2 = saved["alpha_degrees"]["2"][
        "rows_beta_tbin_ubin_coefficient"
    ]
    assert [
        row for row in extended_alpha2 if int(row[0]) <= 12
    ] == old_rows


def test_extended_alpha3_matches_finite_s_symbolic_margin() -> None:
    """Independently check the new core-vector alpha^3 decomposition."""

    saved = json.loads(EXTENDED_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    rows_by_alpha = {
        alpha_degree: saved["alpha_degrees"][str(alpha_degree)][
            "rows_beta_tbin_ubin_coefficient"
        ]
        for alpha_degree in (2, 3)
    }
    for s in (4, 5):
        transfer = csr.CompleteSplitTransfer(s)
        pair_class = csr.pair_classes(s)["core_core_disjoint"]
        normalized = sp.cancel(
            transfer.reduced_rayleigh_margin(pair_class)
            * transfer.lambda_ ** (2 * s - 4)
        )
        numerator, denominator = normalized.as_numer_denom()
        assert denominator == 1
        polynomial = sp.Poly(sp.expand(numerator), csr.ALPHA, csr.BETA)
        for alpha_degree in (2, 3):
            for beta_degree in range(4, 9):
                reconstructed = sum(
                    sp.Integer(coefficient)
                    * sp.expand_func(sp.binomial(csr.T, int(t_order)))
                    * sp.binomial(s - 4, int(u_order))
                    for (
                        row_beta,
                        t_order,
                        u_order,
                        coefficient,
                    ) in rows_by_alpha[alpha_degree]
                    if int(row_beta) == beta_degree
                )
                finite_layer = polynomial.coeff_monomial(
                    csr.ALPHA**alpha_degree
                    * csr.BETA**beta_degree
                )
                assert sp.expand(reconstructed - finite_layer) == 0


def test_extended_fast_rederivation_through_beta6() -> None:
    fresh = extended.build_certificate(max_beta=6)
    saved = json.loads(EXTENDED_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    for alpha_degree in ("2", "3"):
        expected = [
            row
            for row in saved["alpha_degrees"][alpha_degree][
                "rows_beta_tbin_ubin_coefficient"
            ]
            if int(row[0]) <= 6
        ]
        assert fresh["alpha_degrees"][alpha_degree][
            "rows_beta_tbin_ubin_coefficient"
        ] == expected


def test_tp2_universal_fixed_pair_barrier_identities() -> None:
    """The failed fixed-(j,k) TP2 claim and its cancellation are exact."""

    for s in range(4, 11):
        maximum = 2 * s
        chains = {
            0: general_s.truncated_profile_chain(
                extended.profile(singletons=s), maximum
            ),
            1: general_s.truncated_profile_chain(
                extended.profile(2, singletons=s - 2), maximum
            ),
            2: general_s.truncated_profile_chain(
                extended.profile(2, 2, singletons=s - 4), maximum
            ),
        }
        symmetric_01 = [
            2 * middle - left - right
            for middle, left, right in zip(
                chains[1][1], chains[0][1], chains[2][1]
            )
        ]
        expected = sp.Poly(
            -csr.BETA**4 * (1 + csr.BETA) ** (s - 4),
            csr.BETA,
        )
        assert symmetric_01 == [
            int(expected.coeff_monomial(csr.BETA**degree))
            for degree in range(maximum + 1)
        ]

        diagonal_11 = [
            left - right
            for left, right in zip(
                tp2.convolution(
                    chains[1][1], chains[1][1], maximum
                ),
                tp2.convolution(
                    chains[0][1], chains[2][1], maximum
                ),
            )
        ]
        expected_diagonal = sp.Poly(
            (1 + s * csr.BETA)
            * csr.BETA**4
            * (1 + csr.BETA) ** (s - 4),
            csr.BETA,
        )
        assert diagonal_11 == [
            int(
                expected_diagonal.coeff_monomial(
                    csr.BETA**degree
                )
            )
            for degree in range(maximum + 1)
        ]


def test_tp2_barrier_static_certificate_and_full_small_s_search() -> None:
    saved = json.loads(TP2_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    profile_failure = saved["minimal_destination_profile_counterexample"]
    assert profile_failure == tp2.minimal_profile_counterexample()
    assert int(profile_failure["coefficient"]) == -4

    search = saved["pooled_search"]
    rows = search["rows_s_tbin_beta_coefficient"]
    assert search["covers_full_polynomial_for_each_searched_s"] is True
    assert search["safe_full_degree_bound"] == 40
    assert search["negative_rows"] == []
    assert all(int(row[3]) > 0 for row in rows)
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == search["sha256_rows"]

    # The claimed triangular support is itself checked, not just described.
    for s in range(4, 13):
        support = {
            (int(newton_order), int(beta_degree))
            for row_s, newton_order, beta_degree, _ in rows
            if int(row_s) == s
        }
        expected = {
            (newton_order, beta_degree)
            for newton_order in range(2, 2 * s - 4)
            for beta_degree in range(2 * newton_order, 4 * s - 9)
        }
        assert support == expected

        # The first nonzero pooled layer has a closed all-s factorization.
        beta = csr.BETA
        expected_b2 = sp.Poly(
            4
            * beta**4
            * (1 + 2 * beta) ** (2 * s - 6)
            * (1 + s * beta) ** (2 * s - 8),
            beta,
        )
        saved_b2 = {
            int(beta_degree): int(coefficient)
            for row_s, newton_order, beta_degree, coefficient in rows
            if int(row_s) == s and int(newton_order) == 2
        }
        assert saved_b2 == {
            degree: int(
                expected_b2.coeff_monomial(beta**degree)
            )
            for degree in range(expected_b2.degree() + 1)
            if expected_b2.coeff_monomial(beta**degree)
        }

        # The second nonzero layer also has an all-s positive closed form.
        if s == 4:
            expected_b3_expression = 24 * beta**6
        else:
            x = 1 + 3 * beta
            z = 1 + 2 * beta
            lam = 1 + s * beta
            k_polynomial = (
                1
                + 12 * beta
                + (6 * s + 30) * beta**2
                + 28 * s * beta**3
                + 6 * s**2 * beta**4
            )
            expected_b3_expression = (
                12
                * beta**4
                * lam ** (2 * s - 10)
                * (
                    x ** (2 * s - 8) * k_polynomial
                    - z ** (2 * s - 6) * lam**2
                )
            )
        expected_b3 = sp.Poly(sp.expand(expected_b3_expression), beta)
        saved_b3 = {
            int(beta_degree): int(coefficient)
            for row_s, newton_order, beta_degree, coefficient in rows
            if int(row_s) == s and int(newton_order) == 3
        }
        assert saved_b3 == {
            degree: int(
                expected_b3.coeff_monomial(beta**degree)
            )
            for degree in range(expected_b3.degree() + 1)
            if expected_b3.coeff_monomial(beta**degree)
        }


def test_tp2_pooled_search_fresh_prefix() -> None:
    saved = json.loads(TP2_CERTIFICATE_PATH.read_text(encoding="utf-8"))
    fresh = tp2.build_certificate(4, 5, 10)
    expected = [
        row
        for row in saved["pooled_search"]["rows_s_tbin_beta_coefficient"]
        if int(row[0]) <= 5 and int(row[2]) <= 10
    ]
    assert fresh["pooled_search"]["rows_s_tbin_beta_coefficient"] == expected


def test_tp2_b3_three_page_enumeration_and_positive_remainder() -> None:
    beta = csr.BETA

    def three_page_forest(weights: list[int]) -> sp.Expr:
        factors = [1 + 3 * weight * beta for weight in weights]
        result = sp.prod(factors)
        for index, weight in enumerate(weights):
            others = factors[:index] + factors[index + 1 :]
            result += (
                3 * beta**2 * weight**2 * sp.prod(others)
                + beta**3 * weight**3 * sp.prod(others)
            )
        for first, first_weight in enumerate(weights):
            for second, second_weight in enumerate(weights):
                if first == second:
                    continue
                others = [
                    factor
                    for index, factor in enumerate(factors)
                    if index not in (first, second)
                ]
                result += (
                    3
                    * beta**4
                    * first_weight**2
                    * second_weight**2
                    * sp.prod(others)
                )
        return sp.expand(result)

    for s in range(4, 9):
        h0 = three_page_forest([1] * s)
        h1 = three_page_forest([2] + [1] * (s - 2))
        h2 = three_page_forest([2, 2] + [1] * (s - 4))
        k_polynomial = (
            1
            + 12 * beta
            + (6 * s + 30) * beta**2
            + 28 * s * beta**3
            + 6 * s**2 * beta**4
        )
        assert sp.expand(
            h1**2
            - h0 * h2
            - 12
            * beta**4
            * (1 + 3 * beta) ** (2 * s - 8)
            * k_polynomial
        ) == 0

    for m in range(0, 17, 2):
        s = (m + 8) // 2
        x = 1 + 3 * beta
        z = 1 + 2 * beta
        lam = 1 + s * beta
        k_polynomial = (
            1
            + 12 * beta
            + (3 * m + 54) * beta**2
            + (14 * m + 112) * beta**3
            + (
                sp.Rational(3, 2) * m**2 + 24 * m + 96
            )
            * beta**4
        )
        left = sp.expand(
            x**m * k_polynomial - z ** (m + 2) * lam**2
        )
        if m == 0:
            assert sp.expand(
                left - 2 * beta**2 * (1 + 4 * beta) ** 2
            ) == 0
            continue
        e_m = (
            sp.Rational(m**2 + 18 * m + 8, 4) * beta**2
            + (7 * m**2 + 42 * m + 24) * beta**3
            + sp.Rational(
                3 * m**3 + 82 * m**2 + 314 * m + 208, 2
            )
            * beta**4
            + sp.Rational(
                (m + 8) * (17 * m**2 + 62 * m + 48), 2
            )
            * beta**5
            + sp.Rational(
                (m + 8) ** 2 * (3 * m**2 + 9 * m + 8), 4
            )
            * beta**6
        )
        right = z ** (m - 2) * e_m + sum(
            sp.binomial(m, order)
            * beta**order
            * z ** (m - order)
            * k_polynomial
            for order in range(3, m + 1)
        )
        assert sp.expand(left - right) == 0
        assert all(
            coefficient > 0
            for (_,), coefficient in sp.Poly(e_m, beta).terms()
        )


def test_fixed_four_page_symbolic_determinant_and_b4_formula() -> None:
    """Freshly derive D4 from the 15 page-partition states."""

    _, determinant = fixed_page.derive_four_page_determinant()
    assert determinant == (
        24
        * fixed_page.BETA**4
        * (1 + 4 * fixed_page.BETA) ** (2 * fixed_page.S - 10)
        * fixed_page.k4_polynomial()
    )
    for s in range(5, 10):
        expected = sp.Poly(fixed_page.b4_expression_at_s(s), fixed_page.BETA)
        pooled = {
            degree: int(coefficient)
            for order, degree, coefficient in tp2.pooled_t_newton_rows(
                s, 4 * s - 8
            )
            if order == 4
        }
        assert pooled == {
            degree: int(
                expected.coeff_monomial(fixed_page.BETA**degree)
            )
            for degree in range(expected.degree() + 1)
            if expected.coeff_monomial(fixed_page.BETA**degree)
        }


def test_fixed_page_static_certificate_and_b4_counterexample_scan() -> None:
    saved = json.loads(
        FIXED_PAGE_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    b4 = saved["B4"]
    rows = b4["full_small_s_rows_s_beta_coefficient"]
    assert b4["all_saved_coefficients_positive"] is True
    assert all(int(row[2]) > 0 for row in rows)
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == b4["sha256_rows"]

    search = saved["B4_bracket_counterexample_search"]
    assert search["s_range"] == [5, 500]
    assert search["first_negative"] == []
    assert search["all_searched_coefficients_nonnegative"] is True
    summaries = search["summaries_s_first_degree_last_degree_minimum"]
    assert len(summaries) == 496
    for s, first_degree, last_degree, minimum in summaries:
        assert int(first_degree) == 4
        assert int(last_degree) == 2 * int(s) - 2
        assert int(minimum) > 0

    # Recompute a nontrivial prefix independently of the static JSON.
    for s in range(5, 31):
        coefficients = fixed_page.b4_bracket_coefficients(s)
        assert all(coefficient >= 0 for coefficient in coefficients)
        support = [
            degree
            for degree, coefficient in enumerate(coefficients)
            if coefficient
        ]
        assert support == list(range(4, 2 * s - 1))


def test_b4_uniform_exact_remaining_lemma_regression() -> None:
    saved = json.loads(B4_UNIFORM_AUDIT_PATH.read_text(encoding="utf-8"))
    assert saved["status"] == (
        "proved by a manifestly coefficientwise positive s-recurrence"
    )
    rows = saved["regression_rows_s_first_coefficient_nonzero_count"]
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_rows"]
    assert saved["amgm_strengthening_failure"]["exact_coefficient"] == "-60"

    gap = b4_uniform.amgm_gap_coefficients(5)
    assert gap[4] == -60
    for s in range(5, 31):
        direct = fixed_page.b4_bracket_coefficients(s)
        reconstructed = [
            b4_uniform.bracket_coefficient_formula(s, degree)
            for degree in range(len(direct))
        ]
        assert direct == reconstructed
        assert reconstructed[:4] == [0, 0, 0, 0]
        assert reconstructed[4] == (
            (s - 4) * (s**3 + 6 * s**2 - 10 * s - 141)
        )
        recurrence_direct = b4_uniform.recurrence_remainder_direct(s)
        recurrence_positive = (
            b4_uniform.recurrence_remainder_positive_decomposition(s)
        )
        assert recurrence_direct == recurrence_positive
        assert all(coefficient >= 0 for coefficient in recurrence_positive)

    assert fixed_page.b4_bracket_coefficients(5) == (
        [0, 0, 0, 0]
        + b4_uniform.scale_polynomial(
            fixed_page.integer_convolution(
                fixed_page.linear_power(5, 2),
                [7, 40, 75],
            ),
            12,
        )
    )


def test_five_page_b5_formula_and_recurrence_audit() -> None:
    saved = json.loads(
        FIVE_PAGE_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    assert saved["partition_state_count"] == 52
    assert saved["bracket_counterexample_search"]["s_range"] == [6, 200]
    assert saved["bracket_counterexample_search"]["first_negative"] is None
    recurrence = saved["candidate_positive_recurrence_search"]
    assert recurrence["s_range"] == [6, 199]
    assert recurrence["first_negative"] is None

    rows = saved["pooled_transfer_rows_s5_to_s9"]
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_pooled_rows"]

    assert sp.expand(five_page.b5_expression_at_s(5)) == 12000 * (
        fixed_page.BETA**10
    )
    for s in range(6, 31):
        bracket = five_page.b5_bracket_coefficients(s)
        support = [
            degree
            for degree, coefficient in enumerate(bracket)
            if coefficient
        ]
        assert support == list(range(6, 2 * s + 1))
        assert all(coefficient >= 0 for coefficient in bracket)
        remainder = five_page.recurrence_remainder_coefficients(s)
        assert all(coefficient >= 0 for coefficient in remainder)


def test_b5_uniform_symbolic_tail_certificate() -> None:
    saved = json.loads(B5_UNIFORM_AUDIT_PATH.read_text(encoding="utf-8"))
    assert saved["status"] == "proved"
    assert len(saved["merged_initial_I_over_beta2_coefficients"]) == 12
    assert len(saved["low_degree_F_coefficients_in_n_s_minus_6"]) == 8
    assert saved["tail_base_G8_degree_coefficient"] == [
        [14, "817713831936"],
        [15, "1067728633856"],
        [16, "611683139584"],
    ]
    payload = json.dumps(
        [
            saved["merged_initial_I_over_beta2_coefficients"],
            saved["low_degree_F_coefficients_in_n_s_minus_6"],
            saved["truncated_tail_boundary_beta14"],
            saved["truncated_tail_boundary_beta15"],
            saved["tail_base_G8_degree_coefficient"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == (
        saved["sha256_symbolic_payload"]
    )

    for s in range(6, 16):
        direct = five_page.b5_bracket_coefficients(s)
        reconstructed = [
            int(b5_uniform.f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        assert reconstructed == direct


def test_six_page_b6_formula_and_finite_audit() -> None:
    saved = json.loads(
        SIX_PAGE_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    assert saved["partition_state_count"] == 203
    rows = saved["pooled_transfer_rows_s6_to_s9"]
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_pooled_rows"]
    assert len(rows) == 36

    bracket = saved["bracket_counterexample_search"]
    assert bracket["s_range"] == [7, 200]
    assert bracket["first_negative"] is None
    recurrence = saved["candidate_recurrence_search"]
    assert recurrence["s_range"] == [7, 199]
    assert recurrence["first_negative"] is None

    assert six_page.b6_coefficients(6) == (
        [0] * 12 + [3732480, 27371520, 74649600]
    )
    for s in range(7, 31):
        coefficients = six_page.b6_bracket_coefficients(s)
        support = [
            degree
            for degree, coefficient in enumerate(coefficients)
            if coefficient
        ]
        assert support == list(range(8, 2 * s + 3))
        assert all(coefficient >= 0 for coefficient in coefficients)
        remainder = six_page.recurrence_remainder_coefficients(s)
        assert all(coefficient >= 0 for coefficient in remainder)


def test_b6_uniform_symbolic_tail_certificate() -> None:
    saved = json.loads(B6_UNIFORM_AUDIT_PATH.read_text(encoding="utf-8"))
    assert saved["status"] == "proved"
    assert len(saved["low_degree_F_coefficients_in_n_s_minus_7"]) == 12
    assert len(saved["merged_three_layer_I_over_beta2_coefficients"]) == 17
    assert len(saved["tail_base_G15_degree_coefficient"]) == 13
    payload = json.dumps(
        [
            saved["low_degree_F_coefficients_in_n_s_minus_7"],
            saved["merged_three_layer_I_over_beta2_coefficients"],
            saved["truncated_tail_boundary_beta20"],
            saved["truncated_tail_boundary_beta21"],
            saved["tail_base_G15_degree_coefficient"],
            saved["finite_early_tail_s_count_minimum"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == (
        saved["sha256_symbolic_payload"]
    )
    for s in range(7, 13):
        direct = six_page.b6_bracket_coefficients(s)
        reconstructed = [
            int(b6_uniform.f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        assert reconstructed == direct


def test_seven_page_b7_formula_and_finite_audit() -> None:
    saved = json.loads(
        SEVEN_PAGE_CERTIFICATE_PATH.read_text(encoding="utf-8")
    )
    assert saved["partition_state_count"] == 877
    rows = saved["pooled_transfer_rows_s7_to_s10"]
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_pooled_rows"]
    assert len(rows) == 44
    assert saved["finite_bracket_audit"]["first_negative"] is None
    assert saved["finite_recurrence_audit"]["first_negative"] is None
    assert seven_page.b7_coefficients(7) == (
        [0] * 14
        + [
            1253568960,
            21961658880,
            165977864640,
            622090264320,
            1029362866560,
        ]
    )
    for s in range(8, 21):
        coefficients = seven_page.b7_bracket_coefficients(s)
        support = [
            degree
            for degree, coefficient in enumerate(coefficients)
            if coefficient
        ]
        assert support == list(range(10, 2 * s + 5))
        assert all(coefficient >= 0 for coefficient in coefficients)
        remainder = seven_page.recurrence_remainder_coefficients(s)
        assert all(coefficient >= 0 for coefficient in remainder)


def test_b7_uniform_symbolic_tail_certificate() -> None:
    saved = json.loads(B7_UNIFORM_AUDIT_PATH.read_text(encoding="utf-8"))
    assert saved["status"] == "proved"
    assert len(saved["low_degree_F_coefficients_in_n_s_minus_8"]) == 16
    assert len(saved["merged_three_layer_I_over_beta2_coefficients"]) == 21
    assert len(saved["tail_base_G26_degree_coefficient"]) == 31
    payload = json.dumps(
        [
            saved["low_degree_F_coefficients_in_n_s_minus_8"],
            saved["merged_three_layer_I_over_beta2_coefficients"],
            saved["truncated_tail_boundary_beta26"],
            saved["truncated_tail_boundary_beta27"],
            saved["tail_base_G26_degree_coefficient"],
            saved["finite_early_tail_s_count_minimum"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == (
        saved["sha256_symbolic_payload"]
    )
    for s in range(8, 13):
        direct = seven_page.b7_bracket_coefficients(s)
        reconstructed = [
            int(b7_uniform.f_coefficient_formula(sp.Integer(s), degree))
            for degree in range(len(direct))
        ]
        assert reconstructed == direct


def test_general_k_extremal_component_partition_certificate() -> None:
    saved = json.loads(
        GENERAL_K_EXTREMAL_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == "proved"
    assert len(saved["component_partition_rows"]) == 12
    assert len(saved["cycle_second_difference_rows"]) == 18
    payload = json.dumps(
        [
            saved["component_partition_rows"],
            saved["cycle_second_difference_rows"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert general_k_extremal.build_audit() == saved


def test_general_k_low_coefficient_and_support_certificate() -> None:
    saved = json.loads(
        GENERAL_K_LOW_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == "proved"
    assert len(saved["brute_cycle_classification_rows"]) == 27
    assert len(saved["saved_kernel_crosscheck_rows"]) == 12
    assert len(saved["finite_F_support_crosscheck_rows"]) == 6
    assert len(saved["minimal_mask_complete_graph_rows"]) == 4
    assert len(saved["beta3_exact_interpolation_rows"]) == 72
    assert len(saved["beta4_exact_interpolation_rows"]) == 99
    assert len(saved["beta4_independent_edge_subset_rows"]) == 4
    assert len(saved["beta4_saved_formula_crosscheck_rows"]) == 10
    assert len(saved["F_leading_newton_rows_k2_to_k12"]) == 11
    payload = json.dumps(
        [
            saved["brute_cycle_classification_rows"],
            saved["saved_kernel_crosscheck_rows"],
            saved["finite_F_support_crosscheck_rows"],
            saved["minimal_mask_complete_graph_rows"],
            saved["beta3_exact_interpolation_rows"],
            saved["beta4_exact_interpolation_rows"],
            saved["beta4_independent_edge_subset_rows"],
            saved["beta4_saved_formula_crosscheck_rows"],
            saved["F_leading_newton_rows_k2_to_k12"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert general_k_low.build_audit() == saved


def test_f_leading_rooted_tree_lagrange_certificate() -> None:
    saved = json.loads(
        F_LEADING_LAGRANGE_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == "proved_formula_not_general_positivity"
    assert saved["rooted_identity_order"] == 12
    assert len(saved["profile_dp_crosscheck_rows_s4_to_s12"]) == 27
    assert len(saved["symbolic_crosscheck_rows_k2_to_k7"]) == 6
    assert len(saved["termwise_sign_obstruction_rows"]) == 4
    assert len(saved["base4_newton_rows_k2_to_k30"]) == 29
    assert len(saved["base4_lagrange_vs_dp_rows"]) == 87
    assert [
        row[1] for row in saved["base4_newton_rows_k2_to_k30"]
    ] == [(page_count - 2) // 2 for page_count in range(2, 31)]
    payload = json.dumps(
        [
            saved["profile_dp_crosscheck_rows_s4_to_s12"],
            saved["symbolic_crosscheck_rows_k2_to_k7"],
            saved["termwise_sign_obstruction_rows"],
            saved["base4_newton_rows_k2_to_k30"],
            saved["base4_lagrange_vs_dp_rows"],
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert f_leading_lagrange.build_audit() == saved


def test_f_leading_color_swap_obstruction_certificate() -> None:
    saved = json.loads(
        F_LEADING_SWAP_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == (
        "proved_obstruction_and_local_repair_not_general_injection"
    )
    collision = saved["naive_fundamental_cycle_collision"]
    assert collision["total_edge_copies"] == 4
    assert collision["remaining_degree_k"] == 2
    assert len(collision["preimages"]) == 2
    fixed = saved["fixed_union_k4_obstruction"]
    assert fixed["positive_count"] == 2
    assert fixed["negative_count"] == 4
    assert len(saved["fixed_union_nonzero_balance_rows_at_total_6"]) == 3
    assert len(saved["local_k4_repair_rows"]) == 4
    payload = json.dumps(
        [
            collision,
            fixed,
            saved["fixed_union_nonzero_balance_rows_at_total_6"],
            saved["local_k4_repair_rows"],
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert f_leading_swap.build_audit() == saved


def test_f_leading_k4_outside_stability_certificate() -> None:
    saved = json.loads(
        F_LEADING_K4_OUTSIDE_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == (
        "proved_outside_stable_local_lemma_not_global_positivity"
    )
    state_rows = saved["state_rows_q0_to_q3"]
    assert [row[0] for row in state_rows] == [0, 1, 2, 3]
    assert [row[2] for row in state_rows] == [1, 5, 34, 299]
    assert [row[3] for row in state_rows] == [1, 5, 26, 141]
    assert all(row[5:7] == [0, 0] for row in state_rows)
    assert len(saved["inverse_rows"]) == 4
    subdivided = saved["minimal_uncovered_subdivided_k4"]
    assert subdivided["q"] == 1
    assert subdivided["remaining_degree_k"] == 5
    assert (subdivided["positive_count"], subdivided["negative_count"]) == (
        10,
        12,
    )
    payload = json.dumps(
        [state_rows, saved["inverse_rows"], subdivided],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert f_leading_k4_outside.build_audit() == saved


def test_f_leading_series_subdivision_certificate() -> None:
    saved = json.loads(
        F_LEADING_SERIES_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == "proved_finite_coupled_routing_not_general"
    assert saved["deficit_class_count"] == 42
    assert saved["deficit_classes_by_remaining_degree"] == {
        "5": 12,
        "6": 30,
    }
    normal_forms = saved["normal_form_rows"]
    assert len(normal_forms) == 16
    assert sum(row[2] for row in normal_forms) == 42
    assert [sum(row[1] == degree for row in normal_forms) for degree in (5, 6)] == [
        5,
        11,
    ]
    injection = saved["q1_k5_finite_injection"]
    assert (injection["positive_count"], injection["negative_count"]) == (
        2240,
        2140,
    )
    assert injection["maximum_colored_copy_moves"] == 2
    assert injection["distance_counts"] == {"1": 239, "2": 1901}
    assert len(injection["target_indices_in_sorted_positive_list"]) == 2140
    target_payload = json.dumps(
        injection["target_indices_in_sorted_positive_list"],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(target_payload).hexdigest() == (
        injection["sha256_target_indices"]
    )
    balanced = saved["q1_k5_balanced_rule_compression"]
    assert balanced["distance_counts"] == {"1": 594, "2": 1546}
    assert balanced["rule_orbit_count"] == 22
    assert len(balanced["rule_rows"]) == 22
    balanced_payload = json.dumps(
        balanced["target_indices_in_sorted_positive_list"],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(balanced_payload).hexdigest() == (
        balanced["sha256_target_indices"]
    )
    tree_filter = saved["tree_replacement_filter"]
    assert tree_filter["isolated_negative_count"] == 150
    assert tree_filter["maximum_matching_size"] == 1790
    assert tree_filter["isolate_normal_form_counts"] == {
        "single_edge_subdivision_k4": 4,
        "three_arm_y_replacement": 146,
    }
    bridge = saved["first_component_bridge_repair"]
    assert bridge["source_count"] == 150
    assert bridge["source_pair_orbit_count"] == 42
    assert bridge["source_pair_orbit_normal_form_counts"] == {
        "single_edge_subdivision_k4": 1,
        "three_arm_y_replacement": 41,
    }
    assert bridge["candidate_degree_counts"] == {"2": 150}
    assert bridge["candidate_action_type_counts"] == {
        "active_bridge": 100,
        "terminal_bridge": 200,
    }
    assert bridge["candidate_target_count"] == 300
    assert bridge["maximum_candidate_target_indegree"] == 1
    assert bridge["selected_target_count"] == 150
    assert bridge["saturated_repair_target_count"] == 32
    assert bridge["saturated_image_intersection_count"] == 0
    assert bridge["tree_replacement_target_universe_count"] == 2150
    assert bridge["bridge_targets_inside_tree_universe_count"] == 300
    assert bridge["tree_plus_bridge_maximum_matching_size"] == 1790
    assert bridge["tree_plus_bridge_hall_witness_source_count"] == 900
    assert bridge["tree_plus_bridge_hall_witness_target_count"] == 550
    assert bridge["tree_plus_bridge_hall_deficiency"] == 350
    assert bridge["tree_plus_bridge_hall_witness_isolate_count"] == 150
    routing = saved["coupled_first_component_routing"]
    assert routing["hall_source_summary"]["object_count"] == 900
    assert routing["hall_source_summary"]["orbit_count"] == 231
    assert routing["hall_target_summary"]["object_count"] == 550
    assert routing["hall_target_summary"]["orbit_count"] == 139
    assert routing["fresh_target_summary"]["object_count"] == 90
    assert routing["fresh_target_summary"]["orbit_count"] == 27
    assert routing["base_plus_all_fresh_maximum_matching_size"] == 1844
    assert routing["fundamental_candidate_counts"] == {
        "E_active": 830,
        "F_active": 320,
        "core_cross": 1560,
    }
    assert routing["fundamental_subset_rows"][-1] == [
        ["core_cross", "E_active", "F_active"],
        8844,
        2240,
        2140,
    ]
    assert routing["extra_balanced_rule_orbit_count"] == 21
    assert routing["best_single_extra_rule_matching_size"] == 2018
    assert routing["best_pair_extra_rule_matching_size"] == 2110
    assert routing["minimum_extra_rule_orbit_count_for_full_matching"] == 3
    assert routing["augmenting_chain_count"] == 350
    assert routing["augmenting_chain_length_counts"] == {
        "2": 168,
        "3": 112,
        "4": 47,
        "5": 14,
        "6": 6,
        "7": 2,
        "8": 1,
    }
    assert routing["maximum_augmenting_chain_length"] == 8
    assert routing["chain_endpoint_inside_tree_universe_count"] == 261
    assert routing["chain_endpoint_outside_tree_universe_count"] == 89
    assert routing["final_rule_counts"] == {
        "E_active": 203,
        "F_active": 52,
        "base_tree_or_bridge": 1590,
        "core_cross": 295,
    }
    assert routing["final_image_count"] == 2140
    assert routing["unused_positive_target_count"] == 100
    routed_payload = json.dumps(
        routing["target_indices_in_sorted_positive_list"],
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(routed_payload).hexdigest() == (
        routing["sha256_target_indices"]
    )
    chain_payload = json.dumps(
        routing["augmentation_chains"], separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(chain_payload).hexdigest() == (
        routing["sha256_augmentation_chains"]
    )
    payload = json.dumps(
        [
            normal_forms,
            injection["target_indices_in_sorted_positive_list"],
            balanced["target_indices_in_sorted_positive_list"],
            balanced["rule_rows"],
            tree_filter["first_failure"],
            {
                key: value
                for key, value in bridge.items()
                if key != "definition"
            },
            {
                key: value
                for key, value in routing.items()
                if key != "definition"
            },
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert f_leading_series.build_audit() == saved


def test_f_leading_first_active_potential_certificate() -> None:
    saved = json.loads(
        F_LEADING_FIRST_ACTIVE_AUDIT_PATH.read_text(encoding="utf-8")
    )
    assert saved["status"] == (
        "static_potential_refuted_fourth_rule_finite_audited"
    )
    cycle = saved["q1_static_source_potential_obstruction"]
    assert cycle["source_indices"] == [1054, 1174]
    assert cycle["common_target_index"] == 903
    assert cycle["directed_cycle_occurrences"] == [
        [317, 2, 1054, 1174, 903],
        [349, 2, 1174, 1054, 903],
    ]
    rows = saved["q2_layer_rows_k1_to_k7"]
    assert rows == [
        [1, 2, 2, 2, 3, 2, 2, 2, 0, 2, 0, 2],
        [2, 115, 115, 203, 228, 115, 115, 115, 0, 115, 4, 115],
        [
            3,
            1585,
            1589,
            3479,
            3755,
            1583,
            1585,
            1585,
            0,
            1585,
            328,
            1585,
        ],
        [
            4,
            10730,
            11024,
            27072,
            28764,
            10692,
            10730,
            10730,
            0,
            10730,
            4016,
            10730,
        ],
        [
            5,
            43648,
            45620,
            130976,
            137028,
            43488,
            43648,
            43648,
            0,
            43648,
            20744,
            43648,
        ],
        [
            6,
            112200,
            117384,
            470296,
            482120,
            111960,
            112196,
            112200,
            37040,
            112200,
            52544,
            112196,
        ],
        [
            7,
            172800,
            177984,
            1233264,
            1242672,
            172536,
            172768,
            172800,
            30528,
            172768,
            55296,
            172800,
        ],
    ]
    witness = saved["minimal_fourth_rule_hall_witness"]
    assert (witness["source_count"], witness["target_count"]) == (8, 6)
    assert witness["deficiency"] == 2
    assert len(witness["active_active_escape_rows"]) == 8
    assert witness["shortest_augmentation_length_counts"] == {"3": 2}
    completion = saved["q2_k7_single_signature_completion"]
    assert completion["rule_signature"] == [[0, 2], [4, 5]]
    assert (
        completion["four_rule_hall_source_count"],
        completion["four_rule_hall_target_count"],
        completion["four_rule_hall_deficiency"],
    ) == (2272, 2240, 32)
    assert completion["four_rule_hall_escape_signature_orbit_count"] == 20
    assert completion["four_rule_hall_escape_edge_count"] == 25296
    assert completion["added_edge_count"] == 55296
    assert completion["added_target_count"] == 26496
    assert completion["maximum_added_target_indegree"] == 4
    assert completion["maximum_added_source_outdegree"] == 2
    assert completion["matching_size"] == 172800
    assert completion["minimum_additional_signature_orbit_count"] == 1
    assert completion["maximum_augmentation_length"] == 10
    outside = completion["outside_stability_counterexample"]
    assert outside["q"] == 3
    assert outside["source_red_extension_is_forest"] is True
    assert outside["target_red_extension_is_forest"] is False
    payload = json.dumps(
        [cycle, rows, witness, completion],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert hashlib.sha256(payload).hexdigest() == saved["sha256_payload"]
    assert f_leading_first_active.build_audit() == saved
