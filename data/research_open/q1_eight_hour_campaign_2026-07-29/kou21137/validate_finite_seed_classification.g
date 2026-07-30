# Exhaustive SmallGroups regression for the five-class classification of
# finite seeds A such that the square values of A wr C2 form a subgroup.
# The script checks the exact wreath criterion, not the enormous wreath groups.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

IsSemiExtraspecialLocal := function(group)
    local centre, derived, frattini, conjugacy_class, representative;
    if IsAbelian(group) or not IsPGroup(group)
       or PrimePGroup(group) <> 2 then
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

WreathCriterionHolds := function(group)
    local elements, square_values, square_group, element,
          conjugacy_values, coset_values;
    elements := Elements(group);
    square_values := Set(elements, element -> element^2);
    square_group := Group(square_values);
    if Length(square_values) <> Size(square_group) then
        return false;
    fi;
    for element in elements do
        if not element in square_values then
            conjugacy_values :=
                Set(Elements(ConjugacyClass(group, element)));
            coset_values :=
                Set(List(square_values, square -> element * square));
            if conjugacy_values <> coset_values then
                return false;
            fi;
        fi;
    od;
    return true;
end;;

ActsFixedPointFreelyOutside := function(group, kernel)
    local element;
    for element in Elements(group) do
        if not element in kernel
           and Size(Centralizer(kernel, element)) <> 1 then
            return false;
        fi;
    od;
    return true;
end;;

# Return 0 outside the classification and 1..5 for the five disjoint classes.
FiniteSeedClass := function(group)
    local order, kernel, quotient, quotient_id;
    order := Size(group);
    if order mod 2 = 1 then
        return 1;
    fi;
    if IsElementaryAbelian(group) then
        return 2;
    fi;
    if IsSemiExtraspecialLocal(group) then
        return 3;
    fi;

    kernel := FittingSubgroup(group);
    if Size(kernel) = 1
       or Size(kernel) mod 2 = 0
       or not IsAbelian(kernel)
       or not ActsFixedPointFreelyOutside(group, kernel) then
        return 0;
    fi;
    quotient := FactorGroup(group, kernel);
    if Size(quotient) = 2 then
        return 4;
    fi;
    if Size(quotient) = 8 then
        quotient_id := IdGroup(quotient);
        if quotient_id = [8, 4] then
            return 5;
        fi;
    fi;
    return 0;
end;;

class_counts := [0, 0, 0, 0, 0];;
criterion_count := 0;;
total := 0;;
q8_hits := [];;
semi_hits := [];;

for order in [1 .. 128] do
    for identifier in [1 .. NumberSmallGroups(order)] do
        group := SmallGroup(order, identifier);
        criterion := WreathCriterionHolds(group);
        seed_class := FiniteSeedClass(group);
        AssertOrFail(
            criterion = (seed_class > 0),
            Concatenation(
                "five-class mismatch at SmallGroup(",
                String(order), ",", String(identifier), ")",
                ": criterion=", String(criterion),
                ", class=", String(seed_class)
            )
        );
        total := total + 1;
        if criterion then
            criterion_count := criterion_count + 1;
            class_counts[seed_class] := class_counts[seed_class] + 1;
            if seed_class = 3 then
                Add(semi_hits, [order, identifier]);
            elif seed_class = 5 then
                Add(q8_hits, [order, identifier]);
            fi;
        fi;
    od;
od;

AssertOrFail(total = Sum([1 .. 128], NumberSmallGroups), "wrong group total");
AssertOrFail(criterion_count = Sum(class_counts), "wrong class total");
AssertOrFail(
    semi_hits = [
        [8, 3], [8, 4], [32, 49], [32, 50],
        [64, 241], [64, 242], [64, 243], [64, 244], [64, 245],
        [128, 2326], [128, 2327]
    ],
    "unexpected semi-extraspecial list"
);

Print(
    "FINITE_SEEDS|orders=1..128",
    "|groups=", total,
    "|criterion=", criterion_count,
    "|class_counts=", class_counts,
    "|q8_hits=", q8_hits,
    "\n"
);
Print("DONE\n");
QUIT;
