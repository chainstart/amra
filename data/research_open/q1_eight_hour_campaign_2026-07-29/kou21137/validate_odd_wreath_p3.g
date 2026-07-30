# Exact no-go check for the most direct odd-prime analogue:
# UT_3(F_3) wr C_3.  The group has the desired exponent 9, and its generated
# cube subgroup is nonabelian, but the 219 cube values do not fill that
# subgroup of order 243.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

field := GF(3);;
matrix := IdentityMat(3, field);;
matrix[1][2] := One(field);;
x := matrix;;
matrix := IdentityMat(3, field);;
matrix[2][3] := One(field);;
y := matrix;;
matrix_seed := Group(x, y);;
seed := Image(IsomorphismPermGroup(matrix_seed));;
permutation_wreath := WreathProduct(seed, Group((1, 2, 3)));;
wreath := Image(IsomorphismPcGroup(permutation_wreath));;

elements := Elements(wreath);;
cube_values := Set(elements, element -> element^3);;
cube_group := Group(cube_values);;
centre := Centre(wreath);;
cube_derived := DerivedSubgroup(cube_group);;

AssertOrFail(Size(seed) = 27, "wrong seed order");
AssertOrFail(Exponent(seed) = 3, "wrong seed exponent");
AssertOrFail(Size(wreath) = 59049, "wrong wreath order");
AssertOrFail(Exponent(wreath) = 9, "wrong wreath exponent");
AssertOrFail(Length(cube_values) = 219, "wrong cube-value count");
AssertOrFail(Size(cube_group) = 243, "wrong generated cube-group order");
AssertOrFail(
    Length(cube_values) < Size(cube_group),
    "cube values unexpectedly form a subgroup"
);
AssertOrFail(not IsAbelian(cube_group), "generated cube group is abelian");
AssertOrFail(Size(centre) = 3, "wrong wreath centre order");
AssertOrFail(
    cube_derived = centre,
    "derived subgroup of generated cubes is not the wreath centre"
);

# Deterministic first closure failure in GAP's sorted cube-value order.
witness := fail;;
for left_index in [1 .. Length(cube_values)] do
    for right_index in [1 .. Length(cube_values)] do
        product := cube_values[left_index] * cube_values[right_index];;
        if not product in cube_values then
            witness := [left_index, right_index, product];;
            break;
        fi;
    od;
    if witness <> fail then
        break;
    fi;
od;
AssertOrFail(witness <> fail, "failed to find a closure witness");

left_cube := cube_values[witness[1]];;
right_cube := cube_values[witness[2]];;
left_root := First(elements, element -> element^3 = left_cube);;
right_root := First(elements, element -> element^3 = right_cube);;
pcgs := Pcgs(wreath);;

# The smallest central quotient still fails closure; its generated cube group
# is abelian.  Moreover, every nontrivial normal subgroup of this p-group
# meets its order-three centre, so no proper quotient can preserve the
# nonabelian commutator of cube_group.
central_map := NaturalHomomorphismByNormalSubgroup(wreath, centre);;
central_quotient := Image(central_map);;
quotient_cube_values := Set(
    Elements(central_quotient),
    element -> element^3
);;
quotient_cube_group := Group(quotient_cube_values);;
AssertOrFail(
    Length(quotient_cube_values) = 73,
    "wrong central-quotient cube-value count"
);
AssertOrFail(
    Size(quotient_cube_group) = 81,
    "wrong central-quotient generated cube-group order"
);
AssertOrFail(
    Length(quotient_cube_values) < Size(quotient_cube_group),
    "central quotient unexpectedly has cube closure"
);
AssertOrFail(
    IsAbelian(quotient_cube_group),
    "central quotient did not kill cube-group noncommutativity"
);

# A second targeted repair starts from the extraspecial group of order 27 and
# exponent 9, then removes the diagonal centre of its wreath product.  This
# does make the quotient's cube values a subgroup, but that subgroup is
# abelian, so it still cannot answer KOU-21.137 negatively.
exponent_nine_seed := ExtraspecialGroup(27, 9);;
exponent_nine_perm_seed := Image(
    IsomorphismPermGroup(exponent_nine_seed)
);;
exponent_nine_wreath := WreathProduct(
    exponent_nine_perm_seed, Group((1, 2, 3))
);;
exponent_nine_centre := Centre(exponent_nine_wreath);;
exponent_nine_cube_values := Set(
    Elements(exponent_nine_wreath), element -> element^3
);;
exponent_nine_cube_group := Group(exponent_nine_cube_values);;
AssertOrFail(
    Exponent(exponent_nine_wreath) = 27,
    "exponent-nine seed wreath does not have exponent 27"
);
AssertOrFail(
    Length(exponent_nine_cube_values) = 243
    and Size(exponent_nine_cube_group) = 243,
    "unquotiented exponent-nine seed cubes are not closed"
);
AssertOrFail(
    not IsAbelian(exponent_nine_cube_group),
    "unquotiented exponent-nine seed cube subgroup is abelian"
);
AssertOrFail(
    DerivedSubgroup(exponent_nine_cube_group) = exponent_nine_centre,
    "cube derived subgroup is not the forced diagonal centre"
);
repair_map := NaturalHomomorphismByNormalSubgroup(
    exponent_nine_wreath, exponent_nine_centre
);;
repair_quotient := Image(repair_map);;
repair_cube_values := Set(
    Elements(repair_quotient), element -> element^3
);;
repair_cube_group := Group(repair_cube_values);;
AssertOrFail(Size(repair_quotient) = 19683, "wrong repair quotient order");
AssertOrFail(Exponent(repair_quotient) = 9, "wrong repair exponent");
AssertOrFail(
    Length(repair_cube_values) = 81
    and Size(repair_cube_group) = 81,
    "wrong repair cube count"
);
AssertOrFail(
    IsAbelian(repair_cube_group),
    "repair unexpectedly produced nonabelian cubes"
);

Print(
    "NO_GO|seed_order=", Size(seed),
    "|seed_exponent=", Exponent(seed),
    "|wreath_order=", Size(wreath),
    "|wreath_exponent=", Exponent(wreath),
    "|cube_values=", Length(cube_values),
    "|cube_generated_order=", Size(cube_group),
    "|cube_generated_abelian=", IsAbelian(cube_group),
    "|centre_order=", Size(centre),
    "|cube_derived_equals_centre=", cube_derived = centre,
    "\n"
);
Print(
    "WITNESS|left_index=", witness[1],
    "|right_index=", witness[2],
    "|left_root_pc=", ExponentsOfPcElement(pcgs, left_root),
    "|right_root_pc=", ExponentsOfPcElement(pcgs, right_root),
    "|left_cube_pc=", ExponentsOfPcElement(pcgs, left_cube),
    "|right_cube_pc=", ExponentsOfPcElement(pcgs, right_cube),
    "|product_pc=", ExponentsOfPcElement(pcgs, witness[3]),
    "|product_is_cube=", witness[3] in cube_values,
    "\n"
);
Print(
    "CENTRAL_QUOTIENT|order=", Size(central_quotient),
    "|cube_values=", Length(quotient_cube_values),
    "|cube_generated_order=", Size(quotient_cube_group),
    "|cube_generated_abelian=", IsAbelian(quotient_cube_group),
    "\n"
);
Print(
    "EXP9_SEED_REPAIR|wreath_exponent=", Exponent(exponent_nine_wreath),
    "|wreath_cube_values=", Length(exponent_nine_cube_values),
    "|wreath_cube_derived=", Size(DerivedSubgroup(exponent_nine_cube_group)),
    "|order=", Size(repair_quotient),
    "|exponent=", Exponent(repair_quotient),
    "|class=", NilpotencyClassOfGroup(repair_quotient),
    "|cube_values=", Length(repair_cube_values),
    "|cube_generated_order=", Size(repair_cube_group),
    "|closed=", Length(repair_cube_values) = Size(repair_cube_group),
    "|cube_generated_abelian=", IsAbelian(repair_cube_group),
    "\n"
);
Print("DONE\n");
QUIT;
