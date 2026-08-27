#!/usr/bin/env python3
"""Extract the second Newton face at the negative-root a-max accumulation."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from search_opg_round7_pnl_root_radial_boxes import (  # noqa: E402
    RADIAL_SLOTS,
    root_polynomial,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    variable,
)
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_negative_q0_no_positive_gram import common_monomial, scale  # noqa: E402
from verify_pnl_double_corner_blowup import (  # noqa: E402
    radial_projective_chart,
    row,
    substitute_slot,
)
from verify_rlp_projective_corner_reduction import reverse_slot  # noqa: E402


LOCAL_SLOTS = (0, 2, 1, 4, 5, 6, 7)


def centered_chart(side):
    radial = radial_projective_chart(root_polynomial("negative"), RADIAL_SLOTS, 0, 7)
    for slot in (1, 5, 6):
        radial = reverse_slot(radial, slot)

    d = variable(7)
    if side == "above":
        numerator = add(constant(2), d)
    else:
        numerator = scale(add(constant(1), d, -1), 2)
    centered, degree = substitute_slot(radial, 7, numerator, constant(3))
    assert degree == 6
    return centered


def face_record(poly):
    order = min(sum(m[slot] for slot in LOCAL_SLOTS) for m in poly)
    face = {
        monomial: value
        for monomial, value in poly.items()
        if sum(monomial[slot] for slot in LOCAL_SLOTS) == order
    }
    return order, face


def main():
    for side in ("below", "above"):
        centered = centered_chart(side)
        order, face = face_record(centered)
        print(
            side,
            "centered", row(centered),
            "newton_order", order,
            "face", row(face),
            "common", common_monomial(face),
            "digest", digest(face),
            flush=True,
        )
        for monomial, value in sorted(face.items()):
            print(side, monomial, value)
        for maximum_slot in LOCAL_SLOTS:
            second = radial_projective_chart(
                centered, LOCAL_SLOTS, maximum_slot, order
            )
            slots = (maximum_slot, *(slot for slot in LOCAL_SLOTS if slot != maximum_slot))
            shape = tuple(max(m[slot] for m in second) + 1 for slot in slots)
            dense_size = 1
            for extent in shape:
                dense_size *= extent
            print(
                side, "maximum", maximum_slot, "row", row(second),
                "slots", slots, "shape", shape, "dense_size", dense_size,
                flush=True,
            )


if __name__ == "__main__":
    main()
