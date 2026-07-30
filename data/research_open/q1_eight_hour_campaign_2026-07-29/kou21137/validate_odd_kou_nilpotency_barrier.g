# Exhaustive p=3 scan for the nilpotency-class barrier in exponent-nine
# groups.  Every SmallGroups type of order at most 729 is checked.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

max_class := 10;;
exp_nine_counts := List([1 .. max_class], index -> 0);;
nonabelian_power_counts := List([1 .. max_class], index -> 0);;
closed_power_counts := List([1 .. max_class], index -> 0);;
closed_nonabelian_counts := List([1 .. max_class], index -> 0);;
first_nonabelian := List([1 .. max_class], index -> fail);;
total_groups := 0;;

for exponent_index in [1 .. 6] do
    order := 3^exponent_index;
    for identifier in [1 .. NumberSmallGroups(order)] do
        group := SmallGroup(order, identifier);
        total_groups := total_groups + 1;
        if Exponent(group) = 9 then
            class := NilpotencyClassOfGroup(group);
            AssertOrFail(
                class <= max_class,
                "nilpotency class exceeds allocated table"
            );
            power_values := Set(
                Elements(group), element -> element^3
            );
            power_group := Group(power_values);
            closed := Length(power_values) = Size(power_group);
            power_abelian := IsAbelian(power_group);

            exp_nine_counts[class] := exp_nine_counts[class] + 1;
            if closed then
                closed_power_counts[class] :=
                    closed_power_counts[class] + 1;
            fi;
            if not power_abelian then
                nonabelian_power_counts[class] :=
                    nonabelian_power_counts[class] + 1;
                if first_nonabelian[class] = fail then
                    first_nonabelian[class] := [order, identifier];
                fi;
                if closed then
                    closed_nonabelian_counts[class] :=
                        closed_nonabelian_counts[class] + 1;
                fi;
            fi;
        fi;
    od;
od;

for class in [1 .. max_class] do
    if exp_nine_counts[class] > 0 then
        Print(
            "ODD_KOU_CLASS|p=3|class=", class,
            "|exp9=", exp_nine_counts[class],
            "|power_nonabelian=", nonabelian_power_counts[class],
            "|power_closed=", closed_power_counts[class],
            "|closed_nonabelian=", closed_nonabelian_counts[class],
            "|first_nonabelian=", first_nonabelian[class],
            "\n"
        );
    fi;
od;

AssertOrFail(
    Sum(nonabelian_power_counts{[1 .. 3]}) = 0,
    "class-at-most-three exponent-nine group has noncommuting cubes"
);

Print(
    "ODD_KOU_SCAN|p=3|orders=3..729|groups=", total_groups,
    "|exp9=", Sum(exp_nine_counts),
    "|power_nonabelian=", Sum(nonabelian_power_counts),
    "|closed_nonabelian=", Sum(closed_nonabelian_counts),
    "\n"
);

# Exact matrix witness at the class-2p upper boundary:
# UT_7(F_3) has exponent 9 and class 6, and these two cubes do not commute.
field := GF(3);;
identity := IdentityMat(7, field);;
x := IdentityMat(7, field);;
y := IdentityMat(7, field);;
for index in [1 .. 3] do
    x[index][index + 1] := One(field);
od;
for index in [4 .. 6] do
    y[index][index + 1] := One(field);
od;
AssertOrFail(x^9 = identity and y^9 = identity, "wrong witness exponent");
AssertOrFail(x^3 <> identity and y^3 <> identity, "witness cubes vanished");
AssertOrFail(x^3 * y^3 <> y^3 * x^3, "witness cubes commute");
Print(
    "UT7_WITNESS|p=3|ambient_class=6|ambient_exponent=9",
    "|x_order=9|y_order=9|cubes_commute=false\n"
);
Print("DONE\n");
QUIT;
