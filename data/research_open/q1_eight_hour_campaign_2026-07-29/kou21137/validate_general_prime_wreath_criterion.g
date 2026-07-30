# Direct finite regression for the all-groups prime-wreath criterion.
# The p=3 scan covers all SmallGroups through order 16; the p=5 scan covers
# all SmallGroups through order 10 and includes the nonabelian D10 seeds.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

PredictedPrimeWreathClosure := function(group, prime)
    local elements, power_values, derived, element,
          conjugacy_values, coset_values;
    elements := Elements(group);
    power_values := Set(elements, element -> element^prime);
    if Length(power_values) = Size(group) then
        return true;
    fi;
    derived := DerivedSubgroup(group);
    if power_values <> Set(Elements(derived)) then
        return false;
    fi;
    for element in elements do
        if not element in derived then
            conjugacy_values :=
                Set(Elements(ConjugacyClass(group, element)));
            coset_values :=
                Set(List(power_values, value -> element * value));
            if conjugacy_values <> coset_values then
                return false;
            fi;
        fi;
    od;
    return true;
end;;

ScanPrime := function(prime, maximum_order)
    local top, total, hits, order, identifier, seed, predicted,
          perm_seed, wreath, power_values, actual;
    top := Image(IsomorphismPermGroup(CyclicGroup(prime)));
    total := 0;
    hits := 0;
    for order in [1 .. maximum_order] do
        for identifier in [1 .. NumberSmallGroups(order)] do
            seed := SmallGroup(order, identifier);
            predicted := PredictedPrimeWreathClosure(seed, prime);
            perm_seed := Image(IsomorphismPermGroup(seed));
            wreath := WreathProduct(perm_seed, top);
            power_values :=
                Set(Elements(wreath), element -> element^prime);
            actual := Length(power_values) = Size(Group(power_values));
            AssertOrFail(
                actual = predicted,
                Concatenation(
                    "prime-wreath criterion mismatch for p=",
                    String(prime), " at SmallGroup(",
                    String(order), ",", String(identifier), ")"
                )
            );
            total := total + 1;
            if actual then
                hits := hits + 1;
            fi;
        od;
    od;
    Print(
        "PRIME_SCAN|p=", prime,
        "|orders=1..", maximum_order,
        "|groups=", total,
        "|hits=", hits,
        "\n"
    );
end;;

ScanPrime(3, 16);
ScanPrime(5, 10);
Print("DONE\n");
QUIT;
