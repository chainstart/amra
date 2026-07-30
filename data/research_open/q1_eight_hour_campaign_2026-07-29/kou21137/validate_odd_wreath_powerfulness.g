# Exact p=3 and p=5 regressions for the odd-prime wreath no-go theorem.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

CheckSeed := function(p, seed, label)
    local perm_seed, factors, ambient, embeddings, diagonal_generators,
          central_generators, seed_generator, diagonal, coordinate,
          power_group, derived_of_power, powers_inside_power,
          generated_powers_inside_power, seed_power_values;
    perm_seed := Image(IsomorphismPermGroup(seed));
    seed_power_values := Set(
        Elements(perm_seed),
        element -> element^p
    );
    AssertOrFail(
        Set(seed_power_values)
            = Set(Elements(DerivedSubgroup(perm_seed))),
        Concatenation(label, ": seed does not have P_p(A)=A'")
    );
    factors := List([1 .. p], coordinate -> perm_seed);
    ambient := DirectProduct(factors);
    embeddings := List(
        [1 .. p],
        coordinate -> Embedding(ambient, coordinate)
    );
    diagonal_generators := [];
    for seed_generator in GeneratorsOfGroup(perm_seed) do
        diagonal := One(ambient);
        for coordinate in [1 .. p] do
            diagonal := diagonal
                * Image(embeddings[coordinate], seed_generator);
        od;
        Add(diagonal_generators, diagonal);
    od;
    central_generators := [];
    for coordinate in [1 .. p] do
        Append(
            central_generators,
            List(
                GeneratorsOfGroup(DerivedSubgroup(perm_seed)),
                generator -> Image(embeddings[coordinate], generator)
            )
        );
    od;
    power_group := Group(
        Concatenation(diagonal_generators, central_generators)
    );
    derived_of_power := DerivedSubgroup(power_group);
    powers_inside_power := Set(
        Elements(power_group),
        element -> element^p
    );
    generated_powers_inside_power := Group(powers_inside_power);

    AssertOrFail(
        derived_of_power = generated_powers_inside_power,
        Concatenation(label, ": H' and H^p differ")
    );
    AssertOrFail(
        Length(powers_inside_power) = Size(generated_powers_inside_power),
        Concatenation(label, ": raw P_p(H) is not H^p")
    );
    AssertOrFail(
        IsSubgroup(generated_powers_inside_power, derived_of_power),
        Concatenation(label, ": H is not powerful")
    );
    Print(
        "ODD_WREATH_POWERFUL|p=", p,
        "|seed=", label,
        "|H=", Size(power_group),
        "|Hderived=", Size(derived_of_power),
        "|Hp=", Size(generated_powers_inside_power),
        "|classified_closed=true|powerful=true\n"
    );
end;;

CheckSeed(3, ExtraspecialGroup(27, 9), "extraspecial_27_exp9");
CheckSeed(5, ExtraspecialGroup(125, 25), "extraspecial_125_exp25");
Print("DONE\n");
QUIT;
