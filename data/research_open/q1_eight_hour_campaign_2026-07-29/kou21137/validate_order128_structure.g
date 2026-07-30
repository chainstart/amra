# Structural audit of the ten minimum-order KOU-21.137 counterexamples.
#
# This script does four independent things:
#   1. constructs the common order-64 central quotient from an explicit
#      presentation, rather than defining it by a SmallGroups identifier;
#   2. scans all 2328 groups of order 128 and proves, within that catalogue,
#      that the target property is equivalent to having centre C2 and that
#      common central quotient;
#   3. constructs the ten groups as two central-lift patterns with three
#      binary relator twists, recording the isomorphism collisions;
#   4. checks the four order-64 maximal-subgroup near misses which separate
#      weak power closure in the group itself from section-wise power closure.
#
# Any mismatch stops GAP with a nonzero exit status.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

SquareValues := function(group)
    return Set(Elements(group), element -> element^2);
end;;

HasTargetProperty := function(group)
    local values, generated;
    if Exponent(group) <> 8 then
        return false;
    fi;
    values := SquareValues(group);
    generated := Group(values);
    return Length(values) = Size(generated)
        and not IsAbelian(generated);
end;;

BuildCentralQuotientModel := function()
    local free, generators, relations, special, i, j, hit, fp_group,
          isomorphism;

    free := FreeGroup("q1", "q2", "q3", "q4", "q5", "q6");
    generators := GeneratorsOfGroup(free);
    relations := List(generators, generator -> generator^2);
    special := [
        [2, 1, 4],
        [3, 1, 5],
        [4, 3, 6],
        [5, 2, 6]
    ];

    for i in [2 .. 6] do
        for j in [1 .. i - 1] do
            hit := Filtered(
                special,
                triple -> triple[1] = i and triple[2] = j
            );
            if Length(hit) = 1 then
                Add(
                    relations,
                    Comm(generators[i], generators[j])
                        * generators[hit[1][3]]^-1
                );
            else
                Add(relations, Comm(generators[i], generators[j]));
            fi;
        od;
    od;

    fp_group := free / relations;
    isomorphism := IsomorphismPcGroup(fp_group);
    AssertOrFail(
        isomorphism <> fail,
        "explicit central-quotient presentation did not yield a pc group"
    );
    return Image(isomorphism);
end;;

BuildCentralLift := function(kind, a, b, c)
    local free, generators, z, relations, i, j, rhs, fp_group,
          isomorphism;

    free := FreeGroup("g1", "g2", "g3", "g4", "g5", "g6", "z");
    generators := GeneratorsOfGroup(free);
    z := generators[7];

    relations := [
        generators[1]^2,
        generators[2]^2 * z^-a,
        generators[3]^2 * z^-b,
        generators[6]^2,
        z^2
    ];
    if kind = "D" then
        Append(relations, [generators[4]^2, generators[5]^2]);
    elif kind = "Q" then
        Append(
            relations,
            [generators[4]^2 * z^-1, generators[5]^2 * z^-1]
        );
    else
        Error("unknown central-lift kind");
    fi;

    for i in [2 .. 7] do
        for j in [1 .. i - 1] do
            rhs := One(free);
            if [i, j] = [2, 1] then
                rhs := generators[4];
            elif [i, j] = [3, 1] then
                rhs := generators[5];
            elif [i, j] = [3, 2] then
                rhs := z^c;
            elif [i, j] = [4, 3] then
                rhs := generators[6];
            elif [i, j] = [5, 2] then
                rhs := generators[6] * z;
            elif [i, j] = [5, 4] then
                rhs := z;
            elif [i, j] = [6, 1] then
                rhs := z;
            fi;

            if kind = "Q"
               and ([i, j] = [4, 1] or [i, j] = [5, 1]
                    or [i, j] = [4, 2] or [i, j] = [5, 3]) then
                rhs := z;
            fi;
            Add(
                relations,
                Comm(generators[i], generators[j]) * rhs^-1
            );
        od;
    od;

    fp_group := free / relations;
    isomorphism := IsomorphismPcGroup(fp_group);
    AssertOrFail(
        isomorphism <> fail,
        "central-lift presentation did not yield a pc group"
    );
    return Image(isomorphism);
end;;

central_quotient_model := BuildCentralQuotientModel();;
AssertOrFail(Size(central_quotient_model) = 64, "Q has wrong order");;
AssertOrFail(
    Exponent(central_quotient_model) = 4,
    "Q has wrong exponent"
);;
AssertOrFail(
    NilpotencyClassOfGroup(central_quotient_model) = 3,
    "Q has wrong class"
);;
AssertOrFail(
    Size(Centre(central_quotient_model)) = 2,
    "Q has wrong centre"
);;
AssertOrFail(
    Size(DerivedSubgroup(central_quotient_model)) = 8,
    "Q has wrong derived subgroup"
);;
AssertOrFail(
    IdGroup(central_quotient_model) = [64, 138],
    "explicit Q presentation does not match the catalogue audit label"
);;

target_ids := [];;
central_cover_ids := [];;
for catalogue_id in [1 .. NumberSmallGroups(128)] do
    group := SmallGroup(128, catalogue_id);;
    if HasTargetProperty(group) then
        Add(target_ids, catalogue_id);
    fi;

    centre := Centre(group);;
    if Size(centre) = 2
       and IdGroup(group / centre) = IdGroup(central_quotient_model) then
        Add(central_cover_ids, catalogue_id);
    fi;
od;

expected_ids := [928 .. 937];;
AssertOrFail(
    target_ids = expected_ids,
    "unexpected order-128 target-property list"
);;
AssertOrFail(
    central_cover_ids = expected_ids,
    "unexpected order-128 central-cover list"
);;
AssertOrFail(
    target_ids = central_cover_ids,
    "target and central-quotient characterizations disagree"
);;

near_miss_labels := [];;
for order in [1, 2, 4, 8, 16, 32, 64] do
    for catalogue_id in [1 .. NumberSmallGroups(order)] do
        group := SmallGroup(order, catalogue_id);;
        if Exponent(group) = 8
           and not IsAbelian(FrattiniSubgroup(group)) then
            Add(near_miss_labels, [order, catalogue_id]);
        fi;
    od;
od;
AssertOrFail(
    near_miss_labels = [[64, 32], [64, 33], [64, 36], [64, 37]],
    "unexpected sub-128 exponent-8 groups with nonabelian Frattini subgroup"
);;

for label in near_miss_labels do
    group := SmallGroup(label[1], label[2]);;
    square_values := SquareValues(group);;
    square_group := Group(square_values);;
    AssertOrFail(
        Length(square_values) = 12 and Size(square_group) = 16,
        "near miss has wrong square-value profile"
    );
    AssertOrFail(
        square_group = FrattiniSubgroup(group)
        and not IsAbelian(square_group),
        "near miss does not generate its nonabelian Frattini subgroup"
    );
    AssertOrFail(
        Length(square_values) <> Size(square_group),
        "near miss square values unexpectedly form a subgroup"
    );
od;

d_type_ids := [];;
q_type_ids := [];;
camina_base_ids := [];;
for catalogue_id in expected_ids do
    group := SmallGroup(128, catalogue_id);;
    centre := Centre(group);;
    derived := DerivedSubgroup(group);;
    frattini := FrattiniSubgroup(group);;
    square_values := SquareValues(group);;
    square_group := Group(square_values);;
    lower_central := LowerCentralSeries(group);;
    fourth_values := Set(Elements(group), element -> element^4);;
    fourth_group := Group(fourth_values);;
    class_two_maximals := Filtered(
        MaximalSubgroups(group),
        subgroup -> NilpotencyClassOfGroup(subgroup) = 2
    );;

    AssertOrFail(
        IsSubgroup(derived, centre),
        "central quotient kernel is not contained in the derived subgroup"
    );
    AssertOrFail(
        IdGroup(group / centre) = [64, 138],
        "wrong common central quotient"
    );
    AssertOrFail(
        IdGroup(group / lower_central[3]) = [32, 27],
        "wrong common class-two quotient"
    );
    AssertOrFail(
        DerivedSubgroup(derived) = centre
        and lower_central[4] = centre,
        "centre is not simultaneously G'' and gamma_4(G)"
    );
    AssertOrFail(
        square_group = derived and square_group = frattini,
        "squares, derived, and Frattini do not agree"
    );
    AssertOrFail(
        Length(square_values) = 16 and Size(square_group) = 16,
        "wrong square-value closure profile"
    );
    AssertOrFail(
        Length(fourth_values) = 2 and Size(fourth_group) = 2,
        "fourth powers are not closed"
    );

    AssertOrFail(
        Length(class_two_maximals) = 1,
        "there is not a unique class-two maximal subgroup"
    );
    base := class_two_maximals[1];;
    base_centre := Centre(base);;
    AssertOrFail(
        IsNormal(group, base) and Size(base) = 64,
        "the distinguished base is not a normal maximal subgroup"
    );
    AssertOrFail(
        base_centre = DerivedSubgroup(base)
        and base_centre = FrattiniSubgroup(base)
        and IdGroup(base_centre) = [4, 2],
        "the distinguished base is not special with centre C2^2"
    );
    AssertOrFail(
        IdGroup(base / base_centre) = [16, 14],
        "the special base does not have elementary-abelian rank-four quotient"
    );
    AssertOrFail(
        IsSubgroup(base, centre)
        and IdGroup(base / centre) = [32, 49],
        "the base modulo Z(G) is not the plus extraspecial group"
    );

    outside_involutions := [];;
    for candidate in Elements(group) do
        if not candidate in base and Order(candidate) = 2 then
            Add(outside_involutions, candidate);
        fi;
    od;
    AssertOrFail(
        Length(outside_involutions) = 8
        and Set(Elements(
            ConjugacyClass(group, outside_involutions[1])
        )) = Set(outside_involutions),
        "outside involutions do not form one class of size eight"
    );
    top := Subgroup(group, [outside_involutions[1]]);;
    AssertOrFail(
        Size(Intersection(base, top)) = 1
        and Size(Group(Concatenation(
            GeneratorsOfGroup(base),
            GeneratorsOfGroup(top)
        ))) = 128,
        "the distinguished base does not split over an outside involution"
    );
    AssertOrFail(
        CommutatorSubgroup(base, top) = derived,
        "[B,t] does not equal G'"
    );

    is_camina_base := true;;
    for candidate in Difference(
        Elements(base),
        Elements(DerivedSubgroup(base))
    ) do
        if Set(Elements(ConjugacyClass(base, candidate)))
           <> Set(Elements(RightCoset(
               DerivedSubgroup(base),
               candidate
           ))) then
            is_camina_base := false;;
            break;
        fi;
    od;
    if is_camina_base then
        Add(camina_base_ids, catalogue_id);
    fi;

    derived_id := IdGroup(derived);;
    if derived_id = [16, 11] then
        Add(d_type_ids, catalogue_id);
        expected_near_miss_count := 2;;
        expected_fixed_group := [8, 3];;
    elif derived_id = [16, 12] then
        Add(q_type_ids, catalogue_id);
        expected_near_miss_count := 3;;
        expected_fixed_group := [8, 4];;
    else
        Error("unexpected derived-subgroup type");
    fi;
    AssertOrFail(
        IdGroup(Centralizer(base, outside_involutions[1]))
            = expected_fixed_group,
        "wrong fixed subgroup for an outside involution"
    );

    maximal_near_miss_count := Length(
        Filtered(
            MaximalSubgroups(group),
            subgroup -> IdGroup(subgroup) in near_miss_labels
        )
    );;
    AssertOrFail(
        maximal_near_miss_count = expected_near_miss_count,
        "wrong number of maximal near-miss sections"
    );

    direct_factors := DirectFactorsOfGroup(base);;
    if catalogue_id = 928 then
        AssertOrFail(
            List(direct_factors, IdGroup) = [[8, 3], [8, 3]],
            "ID 928 base is not D8 x D8"
        );
    elif catalogue_id = 937 then
        AssertOrFail(
            List(direct_factors, IdGroup) = [[8, 4], [8, 4]],
            "ID 937 base is not Q8 x Q8"
        );
    else
        AssertOrFail(
            Length(direct_factors) = 1
            and Size(direct_factors[1]) = 64,
            "a non-endpoint base unexpectedly decomposes directly"
        );
    fi;
od;

AssertOrFail(d_type_ids = [928 .. 933], "wrong D-type family");;
AssertOrFail(q_type_ids = [934 .. 937], "wrong Q-type family");;
AssertOrFail(
    camina_base_ids = [931 .. 935],
    "wrong Camina special-base subfamily"
);;

d_parameter_ids := [];;
q_parameter_ids := [];;
for a in [0, 1] do
    for b in [0, 1] do
        for c in [0, 1] do
            d_lift := BuildCentralLift("D", a, b, c);;
            q_lift := BuildCentralLift("Q", a, b, c);;
            AssertOrFail(
                Size(d_lift) = 128 and Size(q_lift) = 128,
                "central lift has wrong order"
            );
            AssertOrFail(
                IdGroup(d_lift / Centre(d_lift)) = [64, 138]
                and IdGroup(q_lift / Centre(q_lift)) = [64, 138],
                "central lift has wrong quotient"
            );
            AssertOrFail(
                HasTargetProperty(d_lift) and HasTargetProperty(q_lift),
                "central lift lost the target property"
            );
            Add(d_parameter_ids, IdGroup(d_lift)[2]);
            Add(q_parameter_ids, IdGroup(q_lift)[2]);
        od;
    od;
od;

AssertOrFail(
    d_parameter_ids = [928, 931, 929, 932, 929, 932, 930, 933],
    "wrong D-pattern parameter identifications"
);;
AssertOrFail(
    q_parameter_ids = [934, 936, 935, 936, 935, 936, 935, 937],
    "wrong Q-pattern parameter identifications"
);;
AssertOrFail(
    Set(d_parameter_ids) = [928 .. 933],
    "D-pattern presentations do not exhaust the D-type family"
);;
AssertOrFail(
    Set(q_parameter_ids) = [934 .. 937],
    "Q-pattern presentations do not exhaust the Q-type family"
);;

wreath_ids := [];;
for catalogue_id in [1 .. NumberSmallGroups(8)] do
    seed := SmallGroup(8, catalogue_id);;
    wreath := WreathProduct(seed, Group((1, 2)));;
    Add(wreath_ids, IdGroup(wreath)[2]);
od;
AssertOrFail(
    wreath_ids = [67, 628, 928, 937, 1578],
    "unexpected order-eight seed wreath products"
);;
AssertOrFail(
    Intersection(Set(wreath_ids), expected_ids) = [928, 937],
    "the target family has unexpected ordinary wreath products"
);;

Print(
    "PASS|Q_presentation_order=64",
    "|Q_id=[64,138]",
    "|target_iff_central_cover=", Length(target_ids),
    "|D_types=", Length(d_type_ids),
    "|Q_types=", Length(q_type_ids),
    "|Camina_bases=", Length(camina_base_ids),
    "|near_misses=", Length(near_miss_labels),
    "|ordinary_wreath_endpoints=[928,937]",
    "\n"
);
Print(
    "PARAMETERS|D=", d_parameter_ids,
    "|Q=", q_parameter_ids,
    "\n"
);
Print("DONE\n");
QUIT;
