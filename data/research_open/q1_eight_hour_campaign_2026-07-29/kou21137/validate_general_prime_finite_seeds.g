# Exhaustive SmallGroups regression for the all-prime finite-seed
# classification.  For p=2,3,5 it scans every group of order at most 128.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
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

HasCaminaCondition := function(group, derived)
    local element, class_values, coset_values, derived_values;
    derived_values := Set(Elements(derived));
    for element in Elements(group) do
        if not element in derived then
            class_values :=
                Set(Elements(ConjugacyClass(group, element)));
            coset_values :=
                Set(List(derived_values, value -> element * value));
            if class_values <> coset_values then
                return false;
            fi;
        fi;
    od;
    return true;
end;;

PrimeWreathSeedCriterion := function(group, prime)
    local power_values, derived;
    power_values := Set(Elements(group), element -> element^prime);
    if Length(power_values) = Size(group) then
        return true;
    fi;
    derived := DerivedSubgroup(group);
    return power_values = Set(Elements(derived))
        and HasCaminaCondition(group, derived);
end;;

PrimeFiniteSeedClass := function(group, prime)
    local power_values, derived, kernel, quotient;
    if Size(group) mod prime <> 0 then
        return 1;
    fi;
    if IsElementaryAbelian(group)
       and IsPGroup(group) and PrimePGroup(group) = prime then
        return 2;
    fi;

    power_values := Set(Elements(group), element -> element^prime);
    derived := DerivedSubgroup(group);
    if IsPGroup(group) and PrimePGroup(group) = prime
       and not IsAbelian(group)
       and NilpotencyClassOfGroup(group) = 2
       and power_values = Set(Elements(derived))
       and HasCaminaCondition(group, derived) then
        return 3;
    fi;

    kernel := FittingSubgroup(group);
    if Size(kernel) = 1
       or not ActsFixedPointFreelyOutside(group, kernel) then
        return 0;
    fi;
    quotient := FactorGroup(group, kernel);
    if Size(quotient) = prime
       and IsCyclic(quotient) then
        return 4;
    fi;
    if prime = 2 and Size(quotient) = 8
       and IdGroup(quotient) = [8, 4] then
        return 5;
    fi;
    return 0;
end;;

ScanPrime := function(prime)
    local total, criterion_count, class_counts, order, identifier,
          group, criterion, seed_class;
    total := 0;
    criterion_count := 0;
    class_counts := [0, 0, 0, 0, 0];
    for order in [1 .. 128] do
        for identifier in [1 .. NumberSmallGroups(order)] do
            group := SmallGroup(order, identifier);
            criterion := PrimeWreathSeedCriterion(group, prime);
            seed_class := PrimeFiniteSeedClass(group, prime);
            AssertOrFail(
                criterion = (seed_class > 0),
                Concatenation(
                    "finite prime-seed mismatch for p=", String(prime),
                    " at SmallGroup(", String(order), ",",
                    String(identifier), "), class=", String(seed_class)
                )
            );
            total := total + 1;
            if criterion then
                criterion_count := criterion_count + 1;
                class_counts[seed_class] :=
                    class_counts[seed_class] + 1;
            fi;
        od;
    od;
    Print(
        "FINITE_PRIME_SEEDS|p=", prime,
        "|orders=1..128|groups=", total,
        "|criterion=", criterion_count,
        "|class_counts=", class_counts,
        "\n"
    );
end;;

ScanPrime(2);
ScanPrime(3);
ScanPrime(5);
Print("DONE\n");
QUIT;
