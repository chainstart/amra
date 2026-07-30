# Exact p=3 checks for the structural position theorem.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

CheckSeed := function(label, seed, expected_b, expected_h, expected_derived)
    local perm_seed, wreath, power_values, power_group, derived, frattini,
          abelianization, quotient_map, quotient;
    perm_seed := Image(IsomorphismPermGroup(seed));
    wreath := WreathProduct(perm_seed, Group((1, 2, 3)));
    power_values := Set(Elements(wreath), element -> element^3);
    power_group := Group(power_values);
    derived := DerivedSubgroup(wreath);
    frattini := FrattiniSubgroup(wreath);
    abelianization := FactorGroup(seed, DerivedSubgroup(seed));
    quotient_map := NaturalHomomorphismByNormalSubgroup(
        wreath, power_group
    );
    quotient := Image(quotient_map);

    AssertOrFail(
        Size(abelianization) = expected_b,
        Concatenation(label, ": wrong seed abelianization order")
    );
    AssertOrFail(
        Length(power_values) = expected_h
        and Size(power_group) = expected_h,
        Concatenation(label, ": cube values are not the expected subgroup")
    );
    AssertOrFail(
        IsSubgroup(derived, power_group),
        Concatenation(label, ": power subgroup is not inside derived")
    );
    AssertOrFail(
        Size(derived) = expected_derived,
        Concatenation(label, ": wrong derived order")
    );
    AssertOrFail(
        frattini = derived,
        Concatenation(label, ": Frattini and derived subgroups differ")
    );
    AssertOrFail(
        Index(derived, power_group) = expected_b,
        Concatenation(label, ": wrong p=3 structural index")
    );
    AssertOrFail(
        NilpotencyClassOfGroup(quotient) = 2,
        Concatenation(label, ": W/H does not have class p-1")
    );

    Print(
        "STRUCTURAL_P3|seed=", label,
        "|seed_order=", Size(seed),
        "|B_order=", Size(abelianization),
        "|H_order=", Size(power_group),
        "|derived_order=", Size(derived),
        "|frattini_order=", Size(frattini),
        "|derived_over_H=", Index(derived, power_group),
        "|quotient_order=", Size(quotient),
        "|quotient_class=", NilpotencyClassOfGroup(quotient),
        "\n"
    );
end;;

CheckSeed("C3", CyclicGroup(3), 3, 3, 9);
CheckSeed("extraspecial_27_exp9", ExtraspecialGroup(27, 9), 9, 243, 2187);
Print("DONE\n");
QUIT;
