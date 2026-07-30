"""Algebraic sign closure for endpoint stars in forest edge correlation.

Let ``e`` and ``f`` be two distinct inherited edges of an arbitrary finite
graph.  Split all forests into the four exact-inclusion categories

``a``
    neither ``e`` nor ``f`` is present;
``b``
    ``e`` is present and ``f`` is absent;
``c``
    ``e`` is absent and ``f`` is present;
``d``
    both ``e`` and ``f`` are present.

The usual negative-correlation margin is exactly ``b*c - a*d``.

Appending a new degree-two vertex adjacent to the two endpoints of ``e``
adds a length-two path parallel to ``e``.  The exact category transform is

``(a,b,c,d) -> (3*a+b, 3*b, 3*c+d, 3*d)``.

It follows identically that the margin is multiplied by 9.  The analogous
operation at ``f`` also multiplies the margin by 9.  Hence arbitrary numbers
of such endpoint stars preserve the sign, independently of the rest of the
graph.  This is a symbolic closure theorem, not a finite-search inference.

The same four counts also determine every pair involving the two new path
edges.  If they are called ``g`` and ``h``, and ``N`` and ``N_e`` are the
old total-forest and ``e``-inclusion counts, then the six pair margins on
``{e,f,g,h}`` are

``M'(e,f)=9M``, ``M'(g,f)=M'(h,f)=2M``,
``M'(e,g)=M'(e,h)=2*N_e**2``, and
``M'(g,h)=N*(N-N_e)``.

Thus negative correlation of the one old pair ``e,f`` propagates to every
pair among the old pair and the two new path edges.  This still says nothing
about pairs of inherited edges neither of which is ``e``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence


EndpointEdge = Literal["e", "f"]


@dataclass(frozen=True)
class ExactInclusionCounts:
    """Four forest counts classified by exact inclusion of ``e`` and ``f``."""

    neither: int
    e_only: int
    f_only: int
    both: int

    def __post_init__(self) -> None:
        if any(
            type(value) is not int or value < 0
            for value in (
                self.neither,
                self.e_only,
                self.f_only,
                self.both,
            )
        ):
            raise ValueError(
                "exact-inclusion counts must be non-negative integers"
            )

    @property
    def margin(self) -> int:
        """Return ``N_e*N_f - N*N_ef = b*c - a*d``."""

        return (
            self.e_only * self.f_only
            - self.neither * self.both
        )

    @property
    def forest_channels(self) -> tuple[int, int, int, int]:
        """Return ``(N, N_e, N_f, N_ef)``."""

        total = (
            self.neither + self.e_only + self.f_only + self.both
        )
        return (
            total,
            self.e_only + self.both,
            self.f_only + self.both,
            self.both,
        )

    @classmethod
    def from_forest_channels(
        cls,
        channels: Sequence[int],
    ) -> ExactInclusionCounts:
        """Invert ``(N,N_e,N_f,N_ef)`` into ``(a,b,c,d)``."""

        values = tuple(channels)
        if (
            len(values) != 4
            or any(type(value) is not int for value in values)
        ):
            raise ValueError("forest channels must be four integers")
        total, edge_e, edge_f, pair = values
        return cls(
            total - edge_e - edge_f + pair,
            edge_e - pair,
            edge_f - pair,
            pair,
        )


def append_parallel_two_edge_path(
    counts: ExactInclusionCounts,
    endpoint_edge: EndpointEdge,
) -> ExactInclusionCounts:
    """Append one degree-two path parallel to ``e`` or ``f`` exactly."""

    a, b, c, d = (
        counts.neither,
        counts.e_only,
        counts.f_only,
        counts.both,
    )
    if endpoint_edge == "e":
        updated = ExactInclusionCounts(
            3 * a + b,
            3 * b,
            3 * c + d,
            3 * d,
        )
    elif endpoint_edge == "f":
        updated = ExactInclusionCounts(
            3 * a + c,
            3 * b + d,
            3 * c,
            3 * d,
        )
    else:
        raise ValueError("endpoint_edge must be 'e' or 'f'")
    if updated.margin != 9 * counts.margin:
        raise ArithmeticError("parallel-path margin identity failed")
    return updated


def append_endpoint_paths(
    counts: ExactInclusionCounts,
    e_path_count: int,
    f_path_count: int,
) -> ExactInclusionCounts:
    """Append arbitrary numbers of endpoint paths using a closed form."""

    if (
        type(e_path_count) is not int
        or type(f_path_count) is not int
        or e_path_count < 0
        or f_path_count < 0
    ):
        raise ValueError("path counts must be non-negative integers")
    a, b, c, d = (
        counts.neither,
        counts.e_only,
        counts.f_only,
        counts.both,
    )

    e_scale = 3**e_path_count
    e_linear = (
        0
        if e_path_count == 0
        else e_path_count * 3 ** (e_path_count - 1)
    )
    after_e = ExactInclusionCounts(
        e_scale * a + e_linear * b,
        e_scale * b,
        e_scale * c + e_linear * d,
        e_scale * d,
    )

    f_scale = 3**f_path_count
    f_linear = (
        0
        if f_path_count == 0
        else f_path_count * 3 ** (f_path_count - 1)
    )
    updated = ExactInclusionCounts(
        f_scale * after_e.neither
        + f_linear * after_e.f_only,
        f_scale * after_e.e_only
        + f_linear * after_e.both,
        f_scale * after_e.f_only,
        f_scale * after_e.both,
    )
    expected_margin = 9 ** (e_path_count + f_path_count) * counts.margin
    if updated.margin != expected_margin:
        raise ArithmeticError("multi-path margin identity failed")
    return updated


def parallel_path_local_pair_margins(
    counts: ExactInclusionCounts,
) -> dict[tuple[str, str], int]:
    """Return all six margins on ``e,f`` and a new parallel path ``g,h``.

    A new vertex ``x`` and the two edges ``g=xu`` and ``h=xv`` are appended
    at the endpoints of ``e=uv`` while the inherited edge ``e`` is retained.
    The result is indexed by canonical label pairs.  It is exact for an
    arbitrary finite graph and uses no independence assumption.

    The formulas prove a local closure statement: if the inherited
    ``e,f`` margin is non-negative, all six returned margins are
    non-negative.  Pairs of old edges outside ``{e,f}`` are not covered.
    """

    total, edge_e, _, _ = counts.forest_channels
    margin = counts.margin
    margins = {
        ("e", "f"): 9 * margin,
        ("e", "g"): 2 * edge_e**2,
        ("e", "h"): 2 * edge_e**2,
        ("f", "g"): 2 * margin,
        ("f", "h"): 2 * margin,
        ("g", "h"): total * (total - edge_e),
    }
    if any(type(value) is not int for value in margins.values()):
        raise ArithmeticError("parallel-path local margin identity failed")
    return margins


def parallel_path_bundle_margin_classes(
    counts: ExactInclusionCounts,
    path_count: int,
) -> dict[str, int]:
    """Return every margin class after adding parallel two-edge paths.

    ``path_count`` distinct new vertices are each joined to the two endpoints
    of ``e``.  Symmetry leaves five possible pair classes inside the local
    edge set consisting of ``e``, ``f``, and all new path edges.  The
    ``different_path_edges`` class is present only when at least two paths
    were added.

    If the original ``e,f`` margin is non-negative, every returned class is
    non-negative.  As with :func:`parallel_path_local_pair_margins`, no claim
    is made for a pair of inherited edges outside ``{e,f}``.
    """

    if type(path_count) is not int or path_count < 1:
        raise ValueError("path_count must be a positive integer")
    total, edge_e, _, _ = counts.forest_channels
    paths_before_last = path_count - 1
    before_scale = 3**paths_before_last
    before_linear = (
        0
        if paths_before_last == 0
        else paths_before_last * 3 ** (paths_before_last - 1)
    )
    total_before_last = (
        before_scale * total + before_linear * edge_e
    )
    edge_e_before_last = before_scale * edge_e
    margins = {
        "e_f": 9**path_count * counts.margin,
        "e_path_edge": 2 * edge_e_before_last**2,
        "f_path_edge": 2 * 9 ** paths_before_last * counts.margin,
        "same_path_edges": (
            total_before_last
            * (total_before_last - edge_e_before_last)
        ),
    }
    if path_count >= 2:
        margins["different_path_edges"] = (
            4 * 9 ** (path_count - 2) * edge_e**2
        )
    return margins


def append_base_only_star_of_size_at_most_one(
    counts: ExactInclusionCounts,
    neighbourhood_size: int,
) -> ExactInclusionCounts:
    """Append an isolated vertex or an inherited-edge-independent leaf."""

    if neighbourhood_size == 0:
        factor = 1
    elif neighbourhood_size == 1:
        factor = 2
    else:
        raise ValueError("neighbourhood_size must be zero or one")
    updated = ExactInclusionCounts(
        factor * counts.neither,
        factor * counts.e_only,
        factor * counts.f_only,
        factor * counts.both,
    )
    if updated.margin != factor**2 * counts.margin:
        raise ArithmeticError("small-star margin identity failed")
    return updated
