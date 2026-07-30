# Fail-closed p=3 regression for the general diagonal-power no-go theorem in
# A wr Cp.  The script uses the exact cube-value and generated-subgroup
# formulas proved in ODD_DIAGONAL_QUOTIENT_NO_GO.md; it never enumerates the
# enormous wreath products.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

expected_admissible := rec(
    order27 := 2,
    order81 := 10,
    order243 := 33,
    order729 := 234
);;

expected_proper_targets := rec(
    order27 := 0,
    order81 := 4,
    order243 := 14,
    order729 := 147
);;

expected_closed := rec(
    order27 := [4],
    order81 := [],
    order243 := [66],
    order729 := [471, 472, 473, 474]
);;

for order in [27, 81, 243, 729] do
    admissible_count := 0;;
    proper_target_count := 0;;
    closed_ids := [];;

    for identifier in [1 .. NumberSmallGroups(order)] do
        seed := SmallGroup(order, identifier);;
        if Exponent(seed) = 9 then
            cube_values := Set(Elements(seed), element -> element^3);;
            cube_subgroup := Group(cube_values);;
            derived := DerivedSubgroup(seed);;
            centre := Centre(seed);;

            if Length(cube_values) = Size(cube_subgroup)
               and IsSubgroup(centre, cube_subgroup) then
                admissible_count := admissible_count + 1;;
                combined := ClosureGroup(cube_subgroup, derived);;
                class_moment := Sum(
                    ConjugacyClasses(seed),
                    conjugacy_class -> Size(conjugacy_class)^3
                );;

                # Exact formulas before quotienting by diagonal cubes.
                cube_set_size :=
                    Size(cube_subgroup)^3
                    + class_moment
                    - Size(cube_subgroup);;
                generated_size :=
                    Size(seed) * Size(combined)^2;;

                # Exact central-power closure criterion: since these are
                # nontrivial 3-groups, U<A automatically.
                central_power_criterion := cube_subgroup = derived;;
                if central_power_criterion then
                    for element in Elements(seed) do
                        if not element in cube_subgroup
                           and Set(Elements(
                               ConjugacyClass(seed, element)
                           )) <> Set(List(
                               cube_values,
                               cube -> element * cube
                           )) then
                            central_power_criterion := false;;
                            break;
                        fi;
                    od;
                fi;
                AssertOrFail(
                    (cube_set_size = generated_size)
                        = central_power_criterion,
                    "central-power closure criterion failed"
                );

                if IsSubgroup(derived, cube_subgroup)
                   and Size(cube_subgroup) < Size(derived) then
                    proper_target_count := proper_target_count + 1;;
                    u := Size(cube_subgroup);;
                    d := Size(derived);;
                    z := Size(centre);;
                    moment_deficit := Size(seed) * d^2 - class_moment;;
                    closure_deficit := u^3 - u;;

                    AssertOrFail(
                        d >= 3 * u,
                        "proper 3-subgroup did not have index at least three"
                    );
                    AssertOrFail(
                        moment_deficit >= z * (d^2 - 1),
                        "central-class moment lower bound failed"
                    );
                    AssertOrFail(
                        z >= u,
                        "central cube subgroup larger than the centre"
                    );
                    AssertOrFail(
                        moment_deficit > closure_deficit,
                        "moment obstruction failed"
                    );
                    AssertOrFail(
                        cube_set_size < generated_size,
                        "a forbidden proper-target seed has cube closure"
                    );
                fi;

                if cube_set_size = generated_size then
                    Add(closed_ids, identifier);
                    AssertOrFail(
                        cube_subgroup = derived,
                        "closed bounded-search hit has U different from A'"
                    );
                    AssertOrFail(
                        NilpotencyClassOfGroup(seed) = 2,
                        "closed bounded-search hit is not class two"
                    );
                fi;
            fi;
        fi;
    od;

    key := Concatenation("order", String(order));;
    AssertOrFail(
        admissible_count = expected_admissible.(key),
        Concatenation("wrong admissible count at order ", String(order))
    );
    AssertOrFail(
        proper_target_count = expected_proper_targets.(key),
        Concatenation("wrong proper-target count at order ", String(order))
    );
    AssertOrFail(
        closed_ids = expected_closed.(key),
        Concatenation("wrong wreath-closure list at order ", String(order))
    );

    Print(
        "ORDER|", order,
        "|admissible=", admissible_count,
        "|proper_targets=", proper_target_count,
        "|wreath_closed=", closed_ids,
        "\n"
    );
od;

# Exact numerical near-miss certificate for the four order-81 candidates.
for identifier in [7 .. 10] do
    seed := SmallGroup(81, identifier);;
    cube_subgroup := Group(Set(Elements(seed), element -> element^3));;
    derived := DerivedSubgroup(seed);;
    class_moment := Sum(
        ConjugacyClasses(seed),
        conjugacy_class -> Size(conjugacy_class)^3
    );;
    cube_set_size :=
        Size(cube_subgroup)^3 + class_moment - Size(cube_subgroup);;
    generated_size := Size(seed) * Size(derived)^2;;
    AssertOrFail(
        cube_set_size = 4617 and generated_size = 6561,
        "wrong order-81 near-miss sizes"
    );
    AssertOrFail(
        cube_set_size / Size(cube_subgroup) = 1539
        and generated_size / Size(cube_subgroup) = 2187,
        "wrong diagonal-quotient near-miss sizes"
    );
od;

Print(
    "NO_GO|orders=27,81,243,729",
    "|proper_targets=165",
    "|proper_target_closures=0",
    "|near_miss_ids=[81,7..10]",
    "|near_miss_quotient_cube_values=1539",
    "|near_miss_quotient_generated=2187",
    "\n"
);
Print("DONE\n");
QUIT;
