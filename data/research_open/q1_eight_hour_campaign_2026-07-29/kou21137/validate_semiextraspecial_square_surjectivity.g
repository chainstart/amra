# Exhaustive SmallGroups check of the semi-extraspecial square-surjectivity
# theorem.  The mathematical proof is in THEOREM_DRAFT.md; this script is an
# independent finite-instance regression and is not used as a proof.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

IsExtraspecialLocal := function(group)
    local centre, derived, frattini;
    if IsAbelian(group) then
        return false;
    fi;
    centre := Centre(group);
    derived := DerivedSubgroup(group);
    frattini := FrattiniSubgroup(group);
    return Size(centre) = 2
        and centre = derived
        and centre = frattini
        and IsElementaryAbelian(centre);
end;;

# This is the defining quotient condition, not a library predicate.
IsSemiExtraspecialByDefinition := function(group)
    local centre, derived, frattini, maximal_central;
    if IsAbelian(group) then
        return false;
    fi;
    centre := Centre(group);
    derived := DerivedSubgroup(group);
    frattini := FrattiniSubgroup(group);
    if not (
        centre = derived
        and centre = frattini
        and IsElementaryAbelian(centre)
    ) then
        return false;
    fi;
    for maximal_central in MaximalSubgroups(centre) do
        if not IsExtraspecialLocal(FactorGroup(group, maximal_central)) then
            return false;
        fi;
    od;
    return true;
end;;

# For special groups this is the equivalent Camina condition.  It supplies a
# second implementation against which the quotient definition is checked.
IsSemiExtraspecialByClasses := function(group)
    local centre, derived, frattini, conjugacy_class, representative;
    if IsAbelian(group) then
        return false;
    fi;
    centre := Centre(group);
    derived := DerivedSubgroup(group);
    frattini := FrattiniSubgroup(group);
    if not (
        centre = derived
        and centre = frattini
        and IsElementaryAbelian(centre)
    ) then
        return false;
    fi;
    for conjugacy_class in ConjugacyClasses(group) do
        representative := Representative(conjugacy_class);
        if not representative in centre
           and Size(conjugacy_class) <> Size(centre) then
            return false;
        fi;
    od;
    return true;
end;;

QuadraticFibreSize := function(group, centre, central_element)
    return Length(
        Filtered(
            Elements(group),
            element -> element^2 = central_element
        )
    ) / Size(centre);
end;;

expected_ids := rec(
    order8 := [3, 4],
    order16 := [],
    order32 := [49, 50],
    order64 := [241, 242, 243, 244, 245],
    order128 := [2326, 2327]
);;

total_groups := 0;;
total_hits := 0;;

for order in [8, 16, 32, 64, 128] do
    hits := [];;
    for identifier in [1 .. NumberSmallGroups(order)] do
        group := SmallGroup(order, identifier);;
        by_definition := IsSemiExtraspecialByDefinition(group);;
        by_classes := IsSemiExtraspecialByClasses(group);;
        AssertOrFail(
            by_definition = by_classes,
            Concatenation(
                "definition/Camina disagreement at SmallGroup(",
                String(order), ",", String(identifier), ")"
            )
        );
        total_groups := total_groups + 1;;
        if by_definition then
            centre := Centre(group);;
            square_values := Set(Elements(group), element -> element^2);;
            centre_values := Set(Elements(centre));;
            quotient_dimension := LogInt(Size(group) / Size(centre), 2);;
            centre_dimension := LogInt(Size(centre), 2);;
            AssertOrFail(
                quotient_dimension mod 2 = 0,
                "semi-extraspecial quotient has odd dimension"
            );
            half_dimension := quotient_dimension / 2;;
            AssertOrFail(
                centre_dimension <= half_dimension,
                "the Beisiegel/Pfaffian dimension bound failed"
            );
            AssertOrFail(
                square_values = centre_values,
                "square map is not onto the centre"
            );

            # Each coset of the centre has one square, so division by |Z|
            # converts root counts in the group to q-fibre counts on G/Z.
            fibre_sizes := [];;
            for central_element in centre_values do
                Add(
                    fibre_sizes,
                    QuadraticFibreSize(group, centre, central_element)
                );
            od;
            fourier_lower_bound :=
                2^(half_dimension - centre_dimension)
                * (
                    2^half_dimension
                    - 2^centre_dimension
                    + 1
                );;
            AssertOrFail(
                Minimum(fibre_sizes) >= fourier_lower_bound,
                "Fourier/Gauss fibre lower bound failed"
            );
            AssertOrFail(
                Exponent(group) = 4,
                "nonabelian semi-extraspecial 2-group has wrong exponent"
            );
            Add(hits, identifier);;
            total_hits := total_hits + 1;;
            Print(
                "PASS|SmallGroup(", order, ",", identifier, ")",
                "|centre=", Size(centre),
                "|dimV=", quotient_dimension,
                "|dimZ=", centre_dimension,
                "|square_values=", Length(square_values),
                "|min_q_fibre=", Minimum(fibre_sizes),
                "|fourier_lower_bound=", fourier_lower_bound,
                "\n"
            );
        fi;
    od;
    expected := expected_ids.(Concatenation("order", String(order)));;
    AssertOrFail(
        hits = expected,
        Concatenation("unexpected hit list at order ", String(order))
    );
    Print("ORDER|", order, "|ids=", hits, "\n");
od;

AssertOrFail(total_groups = 2665, "wrong number of SmallGroups scanned");
AssertOrFail(total_hits = 11, "wrong number of semi-extraspecial groups");
Print("DONE|groups=2665|semi_extraspecial=11|orders=8..128\n");
QUIT;
