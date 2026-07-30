# GAP-side semantic cross-check for the independent Cayley-table verifier.
#
# This script intentionally uses GAP's group predicates.  Agreement with the
# table-only Python implementation is therefore a two-route check rather than
# two copies of the same predicate code.

SizeScreen([100000, 100000]);;

expected_orders := [1, 2, 4, 8, 16, 32, 64, 128];;
expected_counts := [1, 1, 2, 5, 14, 51, 267, 2328];;
smallgrp_info := PackageInfo("smallgrp");;

if Length(smallgrp_info) = 0 then
    Error("the GAP smallgrp package is unavailable");
fi;

Print("AMRA_KOU21137_GAP_CROSSCHECK_V1\n");
Print(
    "META|gap=", GAPInfo.Version,
    "|smallgrp=", smallgrp_info[1].Version, "\n"
);

for order_index in [1 .. Length(expected_orders)] do
    order := expected_orders[order_index];;
    count := NumberSmallGroups(order);;
    if count <> expected_counts[order_index] then
        Error("unexpected SmallGroups count");
    fi;

    exponent_eight_count := 0;;
    square_subgroup_count := 0;;
    nonabelian_square_values_count := 0;;
    hit_count := 0;;

    for catalogue_id in [1 .. count] do
        group := SmallGroup(order, catalogue_id);;
        if Exponent(group) = 8 then
            exponent_eight_count := exponent_eight_count + 1;
            square_values := Set(
                List(Elements(group), element -> element^2)
            );;
            square_generated := Subgroup(group, square_values);;
            square_values_nonabelian := ForAny(
                square_values,
                left -> ForAny(
                    square_values,
                    right -> left * right <> right * left
                )
            );;
            if square_values_nonabelian then
                nonabelian_square_values_count :=
                    nonabelian_square_values_count + 1;
            fi;
            if Length(square_values) = Size(square_generated) then
                square_subgroup_count := square_subgroup_count + 1;
                if not IsAbelian(square_generated) then
                    hit_count := hit_count + 1;
                    derived := DerivedSubgroup(group);;
                    frattini := FrattiniSubgroup(group);;
                    centre := Centre(group);;
                    pcgs := Pcgs(group);;
                    power_vectors := List(
                        [1 .. Length(pcgs)],
                        index -> ExponentsOfPcElement(
                            pcgs, pcgs[index]^2
                        )
                    );;
                    commutator_vectors := List(
                        [1 .. Length(pcgs) - 1],
                        left_index -> List(
                            [left_index + 1 .. Length(pcgs)],
                            right_index -> [
                                right_index,
                                left_index,
                                ExponentsOfPcElement(
                                    pcgs,
                                    Comm(
                                        pcgs[right_index],
                                        pcgs[left_index]
                                    )
                                )
                            ]
                        )
                    );;
                    Print(
                        "HIT|", order, "|", catalogue_id,
                        "|square_size=", Length(square_values),
                        "|square_id=", IdGroup(square_generated),
                        "|derived_id=", IdGroup(derived),
                        "|frattini_id=", IdGroup(frattini),
                        "|centre_id=", IdGroup(centre),
                        "|derived_equals_squares=",
                        derived = square_generated,
                        "|frattini_equals_squares=",
                        frattini = square_generated,
                        "|class=", NilpotencyClassOfGroup(group),
                        "|rank=", RankPGroup(group),
                        "|automorphisms=", Size(AutomorphismGroup(group)),
                        "|abelian_invariants=", AbelianInvariants(group),
                        "|element_orders=",
                        Collected(List(Elements(group), Order)),
                        "|lower_central_sizes=",
                        List(LowerCentralSeries(group), Size),
                        "|derived_series_sizes=",
                        List(DerivedSeriesOfGroup(group), Size),
                        "|power_vectors=", power_vectors,
                        "|commutator_vectors=", commutator_vectors,
                        "\n"
                    );
                fi;
            fi;
        fi;
    od;

    Print(
        "SUMMARY|", order,
        "|groups=", count,
        "|exponent_eight=", exponent_eight_count,
        "|square_subgroup=", square_subgroup_count,
        "|nonabelian_square_values=", nonabelian_square_values_count,
        "|hits=", hit_count,
        "\n"
    );
od;
Print("DONE\n");
QUIT;
