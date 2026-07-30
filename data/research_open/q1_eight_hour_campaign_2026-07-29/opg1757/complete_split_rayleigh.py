#!/usr/bin/env python3
"""Exact two-orbit Rayleigh certificates for complete split graphs.

Let S_{s,r} = K_s join \bar K_r.  Every clique edge has activity ``alpha``
and every clique--independent edge has activity ``beta``.  This module
constructs exact certificates for

    Z_e Z_f - Z Z_ef >= 0,

where Z is the weighted spanning-forest enumerator and Z_e denotes the
weighted sum over forests containing e.

The proof is finite in ``s`` but uniform in the number ``r`` of independent
vertices.  After distinguishing the pages containing e and f, put
``t = r - page_shift``.  Each reduced Rayleigh numerator is converted exactly
to

    sum c[i,j,k] alpha**i beta**j binomial(t, k).

Nonnegative coefficients are a certificate for every integer t >= 0 and all
alpha,beta > 0.  The implementation intentionally uses exact SymPy arithmetic;
there is no numerical sampling in the certificate path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import sympy as sp


ALPHA, BETA, T = sp.symbols("alpha beta t")
Edge = tuple[int, int]
Block = tuple[int, ...]
Partition = tuple[Block, ...]
Vector = dict[Partition, sp.Expr]


def canonical_partition(blocks: Iterable[Iterable[int]]) -> Partition:
    """Return the canonical tuple representation of a set partition."""

    normalized = (tuple(sorted(block)) for block in blocks)
    return tuple(sorted(normalized, key=lambda block: block[0]))


def set_partitions(n: int) -> list[Partition]:
    """List all set partitions of range(n), once each."""

    if n < 1:
        raise ValueError("n must be positive")
    partitions: list[Partition] = [((0,),)]
    for vertex in range(1, n):
        extended: list[Partition] = []
        for partition in partitions:
            extended.append(canonical_partition((*partition, (vertex,))))
            for index in range(len(partition)):
                blocks = list(partition)
                blocks[index] = (*blocks[index], vertex)
                extended.append(canonical_partition(blocks))
        partitions = extended
    return partitions


def normalize_edge(edge: Edge) -> Edge:
    u, v = edge
    if u == v:
        raise ValueError("loops are not core edges")
    return (u, v) if u < v else (v, u)


@dataclass(frozen=True)
class CountSpec:
    """A marked forest count represented after its distinguished pages."""

    core_edges: tuple[Edge, ...] = ()
    page_masks: tuple[tuple[int, ...], ...] = ()
    # The number of unforced distinguished pages in addition to T ordinary
    # pages.  Thus the unforced page operator is raised to T + shift.
    shift: int = 0


@dataclass(frozen=True)
class PairClass:
    """Four counts defining one edge-pair orbit."""

    page_shift: int
    z: CountSpec
    z_e: CountSpec
    z_f: CountSpec
    z_ef: CountSpec


def pair_classes(s: int) -> dict[str, PairClass]:
    """Return representatives of every unordered edge-pair orbit."""

    if s < 3:
        raise ValueError("the certificate is organized for s >= 3")

    empty = ()
    core_edge = ((0, 1),)
    classes: dict[str, PairClass] = {
        "core_core_adjacent": PairClass(
            page_shift=0,
            z=CountSpec(),
            z_e=CountSpec(core_edges=core_edge),
            z_f=CountSpec(core_edges=core_edge),  # symmetric single-edge count
            z_ef=CountSpec(core_edges=((0, 1), (0, 2))),
        ),
        "core_spoke_incident": PairClass(
            page_shift=1,
            z=CountSpec(shift=1),
            z_e=CountSpec(core_edges=core_edge, shift=1),
            z_f=CountSpec(page_masks=((0,),)),
            z_ef=CountSpec(core_edges=core_edge, page_masks=((0,),)),
        ),
        "core_spoke_nonincident": PairClass(
            page_shift=1,
            z=CountSpec(shift=1),
            z_e=CountSpec(core_edges=core_edge, shift=1),
            z_f=CountSpec(page_masks=((2,),)),
            z_ef=CountSpec(core_edges=core_edge, page_masks=((2,),)),
        ),
        "spoke_spoke_same_page": PairClass(
            page_shift=1,
            z=CountSpec(shift=1),
            z_e=CountSpec(page_masks=((0,),)),
            z_f=CountSpec(page_masks=((1,),)),
            z_ef=CountSpec(page_masks=((0, 1),)),
        ),
        "spoke_spoke_different_pages_same_core": PairClass(
            page_shift=2,
            z=CountSpec(shift=2),
            z_e=CountSpec(page_masks=((0,),), shift=1),
            z_f=CountSpec(page_masks=((0,),), shift=1),
            z_ef=CountSpec(page_masks=((0,), (0,))),
        ),
        "spoke_spoke_different_pages_different_core": PairClass(
            page_shift=2,
            z=CountSpec(shift=2),
            z_e=CountSpec(page_masks=((0,),), shift=1),
            z_f=CountSpec(page_masks=((1,),), shift=1),
            z_ef=CountSpec(page_masks=((0,), (1,))),
        ),
    }
    if s >= 4:
        classes["core_core_disjoint"] = PairClass(
            page_shift=0,
            z=CountSpec(),
            z_e=CountSpec(core_edges=core_edge),
            z_f=CountSpec(core_edges=core_edge),  # symmetric single-edge count
            z_ef=CountSpec(core_edges=((0, 1), (2, 3))),
        )
    return classes


class CompleteSplitTransfer:
    """Partition transfer engine for one fixed clique size s."""

    def __init__(self, s: int):
        if s < 1:
            raise ValueError("s must be positive")
        self.s = s
        self.lambda_ = 1 + s * BETA
        self.partitions = set_partitions(s)
        self._core_vector_cache: dict[tuple[Edge, ...], Vector] = {}
        self._chain_cache: dict[
            tuple[tuple[Edge, ...], tuple[tuple[int, ...], ...]],
            tuple[sp.Expr, ...],
        ] = {}
        self._count_cache: dict[CountSpec, sp.Expr] = {}

    @staticmethod
    def _clean(vector: Mapping[Partition, sp.Expr]) -> Vector:
        cleaned: Vector = {}
        for partition, coefficient in vector.items():
            expanded = sp.expand(coefficient)
            if expanded != 0:
                cleaned[partition] = expanded
        return cleaned

    def core_vector(self, forced_edges: Sequence[Edge] = ()) -> Vector:
        """Core-forest state vector with all ``forced_edges`` present."""

        key = tuple(sorted(normalize_edge(edge) for edge in forced_edges))
        if key in self._core_vector_cache:
            return self._core_vector_cache[key]
        forced = frozenset(key)
        vector: Vector = {}
        for partition in self.partitions:
            block_of = {
                vertex: block_index
                for block_index, block in enumerate(partition)
                for vertex in block
            }
            if any(block_of[u] != block_of[v] for u, v in forced):
                continue

            multiplicity = sp.S.One
            valid = True
            for block in partition:
                block_set = frozenset(block)
                block_forced = tuple(
                    edge
                    for edge in forced
                    if edge[0] in block_set and edge[1] in block_set
                )
                # Count trees of K_block containing the prescribed forest.
                # If its component sizes are q_1,...,q_c, the
                # Cayley--Moon extension formula is
                #       |block|^(c-2) product_i q_i.
                parent = {vertex: vertex for vertex in block}

                def find(vertex: int) -> int:
                    while parent[vertex] != vertex:
                        parent[vertex] = parent[parent[vertex]]
                        vertex = parent[vertex]
                    return vertex

                for u, v in block_forced:
                    root_u, root_v = find(u), find(v)
                    if root_u == root_v:
                        valid = False
                        break
                    parent[root_u] = root_v
                if not valid:
                    break
                component_sizes: defaultdict[int, int] = defaultdict(int)
                for vertex in block:
                    component_sizes[find(vertex)] += 1
                block_size = len(block)
                extension_count = (
                    sp.Integer(block_size) ** (len(component_sizes) - 2)
                    * sp.prod(component_sizes.values())
                )
                multiplicity *= extension_count
            if valid and multiplicity:
                vector[partition] = sp.expand(
                    multiplicity * ALPHA ** (self.s - len(partition))
                )
        self._core_vector_cache[key] = vector
        return vector

    def _merge_by_page(
        self, partition: Partition, selected_vertices: frozenset[int]
    ) -> Partition | None:
        """Apply one page's spokes to a core connectivity partition."""

        if not selected_vertices:
            return partition
        selected_blocks: list[int] = []
        for index, block in enumerate(partition):
            count = sum(vertex in selected_vertices for vertex in block)
            if count > 1:
                # The two spokes plus the old core path form a cycle.
                return None
            if count == 1:
                selected_blocks.append(index)
        if len(selected_blocks) <= 1:
            return partition
        merged = tuple(
            vertex
            for index in selected_blocks
            for vertex in partition[index]
        )
        remaining = [
            block
            for index, block in enumerate(partition)
            if index not in selected_blocks
        ]
        return canonical_partition((*remaining, merged))

    def page_transfer(
        self, vector: Mapping[Partition, sp.Expr], forced_mask: Sequence[int] = ()
    ) -> Vector:
        """Process one page, forcing the specified incident spokes."""

        forced = frozenset(forced_mask)
        if any(vertex < 0 or vertex >= self.s for vertex in forced):
            raise ValueError("page mask contains a non-core vertex")
        optional = tuple(vertex for vertex in range(self.s) if vertex not in forced)
        result: defaultdict[Partition, sp.Expr] = defaultdict(lambda: sp.S.Zero)
        for partition, old_coefficient in vector.items():
            for bits in range(1 << len(optional)):
                selected = forced | frozenset(
                    optional[index]
                    for index in range(len(optional))
                    if bits & (1 << index)
                )
                destination = self._merge_by_page(partition, selected)
                if destination is not None:
                    result[destination] += old_coefficient * BETA ** len(selected)
        return self._clean(result)

    def nilpotent_part(self, vector: Mapping[Partition, sp.Expr]) -> Vector:
        """Apply N = U - (1+s*beta)I, where U is an unforced page."""

        result: defaultdict[Partition, sp.Expr] = defaultdict(lambda: sp.S.Zero)
        for partition, coefficient in self.page_transfer(vector).items():
            result[partition] += coefficient
        for partition, coefficient in vector.items():
            result[partition] -= self.lambda_ * coefficient
        return self._clean(result)

    def _chain_sums(
        self,
        core_edges: Sequence[Edge],
        page_masks: Sequence[Sequence[int]],
    ) -> tuple[sp.Expr, ...]:
        core_key = tuple(sorted(normalize_edge(edge) for edge in core_edges))
        mask_key = tuple(tuple(sorted(set(mask))) for mask in page_masks)
        key = (core_key, mask_key)
        if key in self._chain_cache:
            return self._chain_cache[key]

        vector = self.core_vector(core_key)
        for mask in mask_key:
            vector = self.page_transfer(vector, mask)

        sums: list[sp.Expr] = []
        for _ in range(self.s):
            sums.append(sum(vector.values(), sp.S.Zero))
            vector = self.nilpotent_part(vector)
        if vector:
            raise AssertionError(f"N^{self.s} is not zero for s={self.s}")
        result = tuple(sums)
        self._chain_cache[key] = result
        return result

    def reduced_count(self, spec: CountSpec) -> sp.Expr:
        """Return R where the actual count is lambda**(T+shift) * R."""

        if spec in self._count_cache:
            return self._count_cache[spec]
        sums = self._chain_sums(spec.core_edges, spec.page_masks)
        result = sum(
            sp.expand_func(sp.binomial(T + spec.shift, order))
            * coefficient
            / self.lambda_**order
            for order, coefficient in enumerate(sums)
        )
        self._count_cache[spec] = result
        return result

    def exact_count_at_t(self, spec: CountSpec, t_value: int) -> sp.Expr:
        """Evaluate the actual marked count for one nonnegative integer t."""

        if t_value < 0:
            raise ValueError("t must be nonnegative")
        return sp.expand(
            self.lambda_ ** (t_value + spec.shift)
            * self.reduced_count(spec).subs(T, t_value)
        )

    def reduced_rayleigh_margin(self, pair_class: PairClass) -> sp.Expr:
        """Return a positive-factor-normalized Rayleigh margin."""

        z = self.reduced_count(pair_class.z)
        z_e = self.reduced_count(pair_class.z_e)
        z_f = self.reduced_count(pair_class.z_f)
        z_ef = self.reduced_count(pair_class.z_ef)

        positive_shift = pair_class.z_e.shift + pair_class.z_f.shift
        negative_shift = pair_class.z.shift + pair_class.z_ef.shift
        common_shift = min(positive_shift, negative_shift)
        return (
            self.lambda_ ** (positive_shift - common_shift) * z_e * z_f
            - self.lambda_ ** (negative_shift - common_shift) * z * z_ef
        )


def newton_rows(
    polynomial: sp.Poly,
) -> list[tuple[int, int, int, sp.Rational]]:
    """Convert a polynomial in alpha,beta,t to the binomial basis in t."""

    grouped: defaultdict[tuple[int, int], sp.Expr] = defaultdict(lambda: sp.S.Zero)
    for (alpha_degree, beta_degree, t_degree), coefficient in polynomial.terms():
        grouped[(alpha_degree, beta_degree)] += coefficient * T**t_degree

    rows: list[tuple[int, int, int, sp.Rational]] = []
    for (alpha_degree, beta_degree), t_polynomial in grouped.items():
        univariate = sp.Poly(t_polynomial, T)
        values = [univariate.eval(value) for value in range(univariate.degree() + 1)]
        order = 0
        while values:
            coefficient = sp.Rational(values[0])
            if coefficient:
                rows.append(
                    (alpha_degree, beta_degree, order, coefficient)
                )
            values = [
                values[index + 1] - values[index]
                for index in range(len(values) - 1)
            ]
            order += 1

    rows.sort()
    # Exact reconstruction is an independent guard against a basis-conversion
    # indexing error.
    reconstructed = sum(
        coefficient
        * ALPHA**alpha_degree
        * BETA**beta_degree
        * sp.expand_func(sp.binomial(T, order))
        for alpha_degree, beta_degree, order, coefficient in rows
    )
    if sp.expand(reconstructed - polynomial.as_expr()) != 0:
        raise AssertionError("Newton/binomial reconstruction failed")
    return rows


def _rational_text(value: sp.Rational) -> str:
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def class_certificate(
    transfer: CompleteSplitTransfer,
    name: str,
    pair_class: PairClass,
    include_rows: bool,
) -> dict[str, object]:
    """Create and validate one exact coefficient certificate."""

    expression = sp.cancel(
        sp.together(sp.expand_func(transfer.reduced_rayleigh_margin(pair_class)))
    )
    numerator, denominator = expression.as_numer_denom()
    denominator_at_zero = sp.expand(denominator).subs(BETA, 0)
    if denominator_at_zero < 0:
        numerator, denominator = -numerator, -denominator

    if denominator.free_symbols - {BETA}:
        raise AssertionError(f"{name}: unexpected denominator variables")
    denominator_polynomial = sp.Poly(sp.expand(denominator), BETA)
    if denominator_polynomial.eval(0) <= 0 or any(
        coefficient < 0 for _, coefficient in denominator_polynomial.terms()
    ):
        raise AssertionError(f"{name}: denominator is not manifestly positive")

    ordinary = sp.Poly(sp.expand(numerator), ALPHA, BETA, T)
    ordinary_negative = sum(
        1 for _, coefficient in ordinary.terms() if coefficient < 0
    )
    rows = newton_rows(ordinary)
    negative_rows = [row for row in rows if row[3] < 0]
    if negative_rows:
        raise AssertionError(
            f"{name}: {len(negative_rows)} negative binomial-basis coefficients"
        )

    serialized_rows = [
        [alpha_degree, beta_degree, order, _rational_text(coefficient)]
        for alpha_degree, beta_degree, order, coefficient in rows
    ]
    digest_payload = json.dumps(
        {
            "denominator": str(sp.factor(denominator)),
            "rows": serialized_rows,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    result: dict[str, object] = {
        "page_shift": pair_class.page_shift,
        "domain": f"r >= {pair_class.page_shift}; t = r-{pair_class.page_shift} >= 0",
        "denominator": str(sp.factor(denominator)),
        "ordinary_monomials": len(ordinary.terms()),
        "ordinary_negative_coefficients": ordinary_negative,
        "binomial_basis_monomials": len(rows),
        "minimum_binomial_coefficient": _rational_text(
            min(row[3] for row in rows)
        ),
        "maximum_binomial_coefficient": _rational_text(
            max(row[3] for row in rows)
        ),
        "sha256": hashlib.sha256(digest_payload).hexdigest(),
    }
    if include_rows:
        result["rows_alpha_beta_binomial_t"] = serialized_rows
    return result


def build_certificate(
    s_values: Sequence[int], include_rows: bool = True
) -> dict[str, object]:
    """Build exact all-r certificates for the requested clique sizes."""

    output: dict[str, object] = {
        "schema": "amra.complete_split.two_orbit_rayleigh.v1",
        "claim": (
            "For each listed s, every r>=0 and alpha,beta>0, every existing "
            "edge-pair orbit of K_s join independent(r) has "
            "Z_e Z_f - Z Z_ef >= 0."
        ),
        "scope_warning": (
            "This is a two-orbit activity theorem, not the full multivariate "
            "I-Rayleigh property and not a proof for unlisted s."
        ),
        "basis": "alpha^i beta^j binomial(t,k), with t=r-page_shift",
        "s_values": {},
    }
    by_s: dict[str, object] = output["s_values"]  # type: ignore[assignment]
    for s in s_values:
        print(f"[complete-split] s={s}: constructing exact certificate", flush=True)
        transfer = CompleteSplitTransfer(s)
        classes: dict[str, object] = {}
        for name, pair_class in pair_classes(s).items():
            print(f"[complete-split] s={s}: {name}", flush=True)
            classes[name] = class_certificate(
                transfer, name, pair_class, include_rows=include_rows
            )
        by_s[str(s)] = {
            "partition_states": len(transfer.partitions),
            "core_forests_counted_by_cayley_moon": int(
                sum(transfer.core_vector().values()).subs(ALPHA, 1)
            ),
            "nilpotence": f"N^{s}=0 checked exactly on every marked vector used",
            "edge_pair_classes": classes,
        }
    return output


def component_tree_weight(a: int, b: int) -> sp.Expr:
    """Weighted spanning-tree enumerator of one (a,b) split component."""

    if a < 1 or b < 0:
        raise ValueError("require a>=1 and b>=0")
    if a == 1 and b == 0:
        return sp.S.One
    return sp.expand(
        BETA**b
        * sp.Integer(a) ** (b - 1)
        * (ALPHA * a + BETA * b) ** (a - 1)
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--s",
        nargs="+",
        type=int,
        default=[3, 4, 5, 6],
        help="clique sizes to certify (default: 3 4 5 6)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="optional JSON output path",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="omit the full exact coefficient rows from JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = build_certificate(args.s, include_rows=not args.summary_only)
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"[complete-split] wrote {args.output}", flush=True)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
