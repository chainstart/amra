# Independent finite-instance checks for the wreath-product theorem used in
# the KOU-21.137 analysis.  This script is deliberately assertion-heavy: any
# disagreement stops GAP with a nonzero exit status.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

UT3CharacteristicTwo := function(q)
    local field, vector_space, basis, generators, scalar, matrix;
    field := GF(q);
    vector_space := AsVectorSpace(GF(2), field);
    basis := BasisVectors(Basis(vector_space));
    generators := [];
    for scalar in basis do
        matrix := IdentityMat(3, field);
        matrix[1][2] := scalar;
        Add(generators, matrix);
        matrix := IdentityMat(3, field);
        matrix[2][3] := scalar;
        Add(generators, matrix);
    od;
    return Group(generators);
end;;

CheckSeed := function(label, abstract_seed, expected_seed_order,
                      expected_centre_order, expected_seed_rank)
    local seed_isomorphism, seed, top, wreath, square_values, square_group,
          seed_centre, seed_derived, seed_frattini, wreath_derived,
          wreath_frattini, expected_square_order, wreath_rank;

    AssertOrFail(
        Size(abstract_seed) = expected_seed_order,
        Concatenation(label, ": wrong seed order")
    );
    AssertOrFail(
        Exponent(abstract_seed) = 4,
        Concatenation(label, ": seed does not have exponent 4")
    );

    seed_centre := Centre(abstract_seed);
    seed_derived := DerivedSubgroup(abstract_seed);
    seed_frattini := FrattiniSubgroup(abstract_seed);
    AssertOrFail(
        Size(seed_centre) = expected_centre_order,
        Concatenation(label, ": wrong centre order")
    );
    AssertOrFail(
        seed_centre = seed_derived and seed_centre = seed_frattini,
        Concatenation(label, ": seed is not special")
    );
    AssertOrFail(
        Length(MinimalGeneratingSet(abstract_seed)) = expected_seed_rank,
        Concatenation(label, ": wrong seed generator rank")
    );

    seed_isomorphism := IsomorphismPermGroup(abstract_seed);
    seed := Image(seed_isomorphism);
    top := Group((1, 2));
    wreath := WreathProduct(seed, top);
    square_values := Set(Elements(wreath), element -> element^2);
    square_group := Group(square_values);
    expected_square_order := Size(seed) * expected_centre_order;

    AssertOrFail(
        Size(wreath) = 2 * Size(seed)^2,
        Concatenation(label, ": wrong wreath-product order")
    );
    AssertOrFail(
        Exponent(wreath) = 8,
        Concatenation(label, ": wreath product does not have exponent 8")
    );
    AssertOrFail(
        Size(square_values) = expected_square_order,
        Concatenation(label, ": wrong number of square values")
    );
    AssertOrFail(
        Size(square_group) = Length(square_values),
        Concatenation(label, ": square values are not a subgroup")
    );
    AssertOrFail(
        not IsAbelian(square_group),
        Concatenation(label, ": square subgroup is abelian")
    );
    AssertOrFail(
        Exponent(square_group) = 4
        and Size(DerivedSubgroup(square_group)) > 1,
        Concatenation(label, ": square subgroup powerfulness witness failed")
    );

    wreath_derived := DerivedSubgroup(wreath);
    wreath_frattini := FrattiniSubgroup(wreath);
    AssertOrFail(
        square_group = wreath_derived and square_group = wreath_frattini,
        Concatenation(label, ": squares, derived, and Frattini disagree")
    );
    AssertOrFail(
        NilpotencyClassOfGroup(wreath) = 4,
        Concatenation(label, ": wrong nilpotency class")
    );
    AssertOrFail(
        Size(Centre(wreath)) = expected_centre_order,
        Concatenation(label, ": wrong wreath-product centre order")
    );
    wreath_rank := Length(MinimalGeneratingSet(wreath));
    AssertOrFail(
        wreath_rank = expected_seed_rank + 1,
        Concatenation(label, ": wrong wreath-product generator rank")
    );

    Print(
        "PASS|", label,
        "|seed_order=", Size(seed),
        "|seed_centre=", Size(seed_centre),
        "|wreath_order=", Size(wreath),
        "|wreath_exponent=", Exponent(wreath),
        "|square_order=", Size(square_group),
        "|square_structure=", StructureDescription(square_group),
        "|class=", NilpotencyClassOfGroup(wreath),
        "|rank=", wreath_rank,
        "|centre=", Size(Centre(wreath)),
        "\n"
    );
end;;

CheckSeed("D8", DihedralGroup(8), 8, 2, 2);
CheckSeed("Q8", QuaternionGroup(8), 8, 2, 2);
CheckSeed("extraspecial_plus_32", ExtraspecialGroup(32, "+"), 32, 2, 4);
CheckSeed("extraspecial_minus_32", ExtraspecialGroup(32, "-"), 32, 2, 4);
CheckSeed("UT3_F4", UT3CharacteristicTwo(4), 64, 4, 4);

Print("DONE|5\n");
QUIT;
