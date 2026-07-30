# Exploratory exact test for odd-prime wreath quotients in KOU-21.137.
#
# Let A be the extraspecial group of order 3^3 and exponent 3, and form the
# regular wreath product A wr C3.  The resulting group has order 3^10 and
# exponent 9.  This script determines, without assuming closure, whether its
# set of cubes is a subgroup and whether that subgroup is abelian.

SizeScreen([100000, 100000]);;

A := ExtraspecialGroup(27, 3);;
iso := IsomorphismPermGroup(A);;
APerm := Image(iso);;
top := Group((1, 2, 3));;
W := WreathProduct(APerm, top);;

Print(
    "SEED|order=", Size(APerm),
    "|exponent=", Exponent(APerm),
    "|centre=", Size(Centre(APerm)),
    "|derived=", Size(DerivedSubgroup(APerm)),
    "\n"
);
Print(
    "WREATH|order=", Size(W),
    "|exponent=", Exponent(W),
    "|class=", NilpotencyClassOfGroup(W),
    "|centre=", Size(Centre(W)),
    "\n"
);

cubes := Set(Elements(W), element -> element^3);;
cube_group := Group(cubes);;
Print(
    "CUBES|values=", Length(cubes),
    "|generated=", Size(cube_group),
    "|closed=", Length(cubes) = Size(cube_group),
    "|abelian=", IsAbelian(cube_group),
    "|derived=", Size(DerivedSubgroup(cube_group)),
    "\n"
);

if Length(cubes) <> Size(cube_group) then
    witness := fail;;
    for left in cubes do
        for right in cubes do
            if not left * right in cubes then
                witness := [left, right, left * right];
                break;
            fi;
        od;
        if witness <> fail then
            break;
        fi;
    od;
    Print("NOT_CLOSED_WITNESS|", witness, "\n");
fi;

central_subgroups := ConjugacyClassesSubgroups(Centre(W));;
for subgroup_class in central_subgroups do
    central_subgroup := Representative(subgroup_class);;
    if Size(central_subgroup) > 1 then
        quotient_map := NaturalHomomorphismByNormalSubgroup(
            W, central_subgroup
        );;
        quotient := Image(quotient_map);;
        quotient_powers := Set(
            Elements(quotient), element -> element^3
        );;
        quotient_power_group := Group(quotient_powers);;
        Print(
            "CENTRAL_QUOTIENT|kernel=", Size(central_subgroup),
            "|order=", Size(quotient),
            "|exponent=", Exponent(quotient),
            "|values=", Length(quotient_powers),
            "|generated=", Size(quotient_power_group),
            "|closed=",
                Length(quotient_powers) = Size(quotient_power_group),
            "|abelian=", IsAbelian(quotient_power_group),
            "|derived=", Size(DerivedSubgroup(quotient_power_group)),
            "\n"
        );
    fi;
od;

# Targeted repair: use the exponent-9 extraspecial seed and quotient its
# wreath product by the diagonal centre.  This kills the possible order-27
# behavior of top-coset elements while retaining exponent 9 in the base.
A9 := ExtraspecialGroup(27, 9);;
iso9 := IsomorphismPermGroup(A9);;
A9Perm := Image(iso9);;
W9 := WreathProduct(A9Perm, top);;
diagonal_centre := Centre(W9);;
quotient_map9 := NaturalHomomorphismByNormalSubgroup(
    W9, diagonal_centre
);;
Q9 := Image(quotient_map9);;
q9_cubes := Set(Elements(Q9), element -> element^3);;
q9_cube_group := Group(q9_cubes);;
Print(
    "EXP9_CENTRAL_QUOTIENT",
    "|seed_order=", Size(A9Perm),
    "|seed_exponent=", Exponent(A9Perm),
    "|wreath_order=", Size(W9),
    "|wreath_centre=", Size(diagonal_centre),
    "|order=", Size(Q9),
    "|exponent=", Exponent(Q9),
    "|class=", NilpotencyClassOfGroup(Q9),
    "|values=", Length(q9_cubes),
    "|generated=", Size(q9_cube_group),
    "|closed=", Length(q9_cubes) = Size(q9_cube_group),
    "|abelian=", IsAbelian(q9_cube_group),
    "|derived=", Size(DerivedSubgroup(q9_cube_group)),
    "\n"
);

QUIT;
