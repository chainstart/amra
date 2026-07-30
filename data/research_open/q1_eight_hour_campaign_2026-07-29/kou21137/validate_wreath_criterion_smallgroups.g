# Bounded regression test for the exact A wr C2 square-subgroup criterion.
# This is not a proof; it is an independent search for missing hypotheses
# across every SmallGroups type of every order at most 32.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

total := 0;;
criterion_true := 0;;
proper_cases := 0;;
nonabelian_square_cases := 0;;

for order in [1 .. 32] do
    count := NumberSmallGroups(order);;
    for catalogue_id in [1 .. count] do
        seed := SmallGroup(order, catalogue_id);;
        seed_elements := Elements(seed);;
        square_values := Set(seed_elements, element -> element^2);;
        square_group := Group(square_values);;
        seed_squares_closed :=
            Length(square_values) = Size(square_group);;

        coset_class_condition := seed_squares_closed;;
        if coset_class_condition then
            for element in seed_elements do
                if not element in square_values then
                    conjugacy_values := Set(
                        Elements(ConjugacyClass(seed, element))
                    );;
                    coset_values := Set(
                        List(square_values, square -> element * square)
                    );;
                    if conjugacy_values <> coset_values then
                        coset_class_condition := false;;
                        break;
                    fi;
                fi;
            od;
        fi;

        perm_seed := Image(IsomorphismPermGroup(seed));;
        wreath := WreathProduct(perm_seed, Group((1, 2)));;
        wreath_square_values := Set(
            Elements(wreath), element -> element^2
        );;
        wreath_square_group := Group(wreath_square_values);;
        wreath_squares_closed :=
            Length(wreath_square_values) = Size(wreath_square_group);;

        AssertOrFail(
            wreath_squares_closed = coset_class_condition,
            Concatenation(
                "criterion mismatch at SmallGroup(",
                String(order), ",", String(catalogue_id), ")"
            )
        );

        if wreath_squares_closed then
            criterion_true := criterion_true + 1;;
            AssertOrFail(
                Length(wreath_square_values)
                    = order * Length(square_values),
                "fiber-product order mismatch"
            );
            if not IsAbelian(wreath_square_group) then
                nonabelian_square_cases := nonabelian_square_cases + 1;;
            fi;

            if order > 1 and Length(square_values) < order then
                proper_cases := proper_cases + 1;;
                AssertOrFail(
                    square_group = DerivedSubgroup(seed),
                    "proper seed squares do not equal seed derived subgroup"
                );
                AssertOrFail(
                    wreath_square_group = DerivedSubgroup(wreath),
                    "wreath squares do not equal wreath derived subgroup"
                );
                if IsPGroup(seed) and PrimePGroup(seed) = 2 then
                    AssertOrFail(
                        wreath_square_group = FrattiniSubgroup(wreath),
                        "2-group wreath squares do not equal Frattini"
                    );
                fi;
            fi;
        fi;
        total := total + 1;;
    od;
od;

Print(
    "PASS|orders=1..32",
    "|groups=", total,
    "|criterion_true=", criterion_true,
    "|proper_cases=", proper_cases,
    "|nonabelian_square_cases=", nonabelian_square_cases,
    "\n"
);
Print("DONE\n");
QUIT;
