# Relation-level orbit audit for the 6+4 central-lift classification.
#
# For each of the two lift patterns and all eight parameter triples, this
# script enumerates all ordered bases of the relevant two-dimensional
# F_2-space, all admissible outside-involution lifts, and all corrections by
# the derived subgroup.  A candidate is accepted only if the transformed
# seven generators generate the whole group and satisfy the complete
# normalized presentation.  The resulting parameter and basis orbits are
# asserted below.

SizeScreen([100000, 100000]);;
SetInfoLevel(InfoWarning, 0);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

BuildFamily := function(epsilon, a, b, c)
    local free, generators, z, relations, powers, right_hand_side,
          i, j, PairRightHandSide, fp_group;

    free := FreeGroup("g1", "g2", "g3", "g4", "g5", "g6", "g7");
    generators := GeneratorsOfGroup(free);
    z := generators[7];
    relations := [];
    powers := [
        One(free), z^a, z^b, z^epsilon, z^epsilon,
        One(free), One(free)
    ];
    for i in [1 .. 7] do
        Add(relations, generators[i]^2 * powers[i]^-1);
    od;

    PairRightHandSide := function(larger, smaller)
        if [larger, smaller] = [2, 1] then
            return generators[4];
        elif [larger, smaller] = [3, 1] then
            return generators[5];
        elif [larger, smaller] = [3, 2] then
            return z^c;
        elif [larger, smaller] = [4, 3] then
            return generators[6];
        elif [larger, smaller] = [5, 2] then
            return generators[6] * z;
        elif [larger, smaller] = [5, 4] then
            return z;
        elif epsilon = 0 and [larger, smaller] = [6, 1] then
            return z;
        elif epsilon = 1
             and [larger, smaller]
                 in [[4, 1], [5, 1], [6, 1], [4, 2], [5, 3]] then
            return z;
        fi;
        return One(free);
    end;

    for i in [2 .. 7] do
        for j in [1 .. i - 1] do
            right_hand_side := PairRightHandSide(i, j);
            Add(
                relations,
                Comm(generators[i], generators[j])
                    * right_hand_side^-1
            );
        od;
    od;
    fp_group := free / relations;
    return PcGroupFpGroup(fp_group);
end;;

NormalizedParameters := function(epsilon, tuple)
    local x, y, u, r, s, d, z, a, b, c, expected_powers,
          ExpectedCommutator, i, j;

    x := tuple[1];
    y := tuple[2];
    u := tuple[3];
    r := tuple[4];
    s := tuple[5];
    d := tuple[6];
    z := tuple[7];

    if y^2 = One(Parent(y)) then
        a := 0;
    elif y^2 = z then
        a := 1;
    else
        return fail;
    fi;
    if u^2 = One(Parent(u)) then
        b := 0;
    elif u^2 = z then
        b := 1;
    else
        return fail;
    fi;
    if Comm(u, y) = One(Parent(y)) then
        c := 0;
    elif Comm(u, y) = z then
        c := 1;
    else
        return fail;
    fi;

    expected_powers := [
        One(Parent(y)), z^a, z^b, z^epsilon, z^epsilon,
        One(Parent(y)), One(Parent(y))
    ];
    for i in [1 .. 7] do
        if tuple[i]^2 <> expected_powers[i] then
            return fail;
        fi;
    od;

    ExpectedCommutator := function(larger, smaller)
        if [larger, smaller] = [2, 1] then
            return r;
        elif [larger, smaller] = [3, 1] then
            return s;
        elif [larger, smaller] = [3, 2] then
            return z^c;
        elif [larger, smaller] = [4, 3] then
            return d;
        elif [larger, smaller] = [5, 2] then
            return d * z;
        elif [larger, smaller] = [5, 4] then
            return z;
        elif epsilon = 0 and [larger, smaller] = [6, 1] then
            return z;
        elif epsilon = 1
             and [larger, smaller]
                 in [[4, 1], [5, 1], [6, 1], [4, 2], [5, 3]] then
            return z;
        fi;
        return One(Parent(y));
    end;

    for i in [2 .. 7] do
        for j in [1 .. i - 1] do
            if Comm(tuple[i], tuple[j]) <> ExpectedCommutator(i, j) then
                return fail;
            fi;
        od;
    od;
    return [a, b, c];
end;;

VectorRepresentative := function(y, u, vector)
    if vector = [1, 0] then
        return y;
    elif vector = [0, 1] then
        return u;
    elif vector = [1, 1] then
        return y * u;
    fi;
    Error("bad nonzero vector");
end;;

NormalizedOrbit := function(epsilon, a, b, c)
    local group, generators, x, y, u, derived, z, nonzero,
          ordered_bases, first_vector, second_vector, basis,
          x_candidates, x_new, y_correction, u_correction,
          y_new, u_new, r_new, s_new, d_new, tuple, parameters,
          parameter_set, basis_set;

    group := BuildFamily(epsilon, a, b, c);
    AssertOrFail(Size(group) = 128, "central-lift presentation has wrong order");
    generators := GeneratorsOfGroup(group);
    AssertOrFail(Length(generators) = 7, "unexpected pc generator count");
    x := generators[1];
    y := generators[2];
    u := generators[3];
    derived := DerivedSubgroup(group);
    z := First(Elements(Centre(group)), element -> element <> One(group));

    nonzero := [[1, 0], [0, 1], [1, 1]];
    ordered_bases := [];
    for first_vector in nonzero do
        for second_vector in nonzero do
            if first_vector <> second_vector then
                Add(ordered_bases, [first_vector, second_vector]);
            fi;
        od;
    od;
    AssertOrFail(Length(ordered_bases) = 6, "wrong GL(2,2) basis count");

    x_candidates := Filtered(
        RightCoset(derived, x),
        candidate -> Order(candidate) = 2
    );
    parameter_set := [];
    basis_set := [];
    for basis in ordered_bases do
        for x_new in x_candidates do
            for y_correction in Elements(derived) do
                y_new :=
                    VectorRepresentative(y, u, basis[1]) * y_correction;
                for u_correction in Elements(derived) do
                    u_new :=
                        VectorRepresentative(y, u, basis[2]) * u_correction;
                    r_new := Comm(y_new, x_new);
                    s_new := Comm(u_new, x_new);
                    d_new := Comm(r_new, u_new);
                    tuple := [
                        x_new, y_new, u_new, r_new, s_new, d_new, z
                    ];
                    parameters := NormalizedParameters(epsilon, tuple);
                    if parameters <> fail and Size(Group(tuple)) = 128 then
                        AddSet(parameter_set, parameters);
                        AddSet(basis_set, basis);
                    fi;
                od;
            od;
        od;
    od;
    return rec(parameters := parameter_set, bases := basis_set);
end;;

ExpectedParameterOrbit := function(epsilon, a, b, c)
    local expected, source_zero, aa, bb, candidate_zero;
    if epsilon = 0 then
        return Set([[a, b, c], [b, a, c]]);
    fi;

    source_zero := (a + c) mod 2 = 0 and (b + c) mod 2 = 0;
    expected := [];
    for aa in [0, 1] do
        for bb in [0, 1] do
            candidate_zero :=
                (aa + c) mod 2 = 0 and (bb + c) mod 2 = 0;
            if candidate_zero = source_zero then
                Add(expected, [aa, bb, c]);
            fi;
        od;
    od;
    return Set(expected);
end;;

nonzero_vectors := [[1, 0], [0, 1], [1, 1]];;
all_ordered_bases := [];;
for first_vector in nonzero_vectors do
    for second_vector in nonzero_vectors do
        if first_vector <> second_vector then
            Add(all_ordered_bases, [first_vector, second_vector]);
        fi;
    od;
od;
Sort(all_ordered_bases);;
swap_bases := [
    [[0, 1], [1, 0]],
    [[1, 0], [0, 1]]
];;
Sort(swap_bases);;

for epsilon in [0, 1] do
    for a in [0, 1] do
        for b in [0, 1] do
            for c in [0, 1] do
                orbit := NormalizedOrbit(epsilon, a, b, c);;
                AssertOrFail(
                    orbit.parameters
                        = ExpectedParameterOrbit(epsilon, a, b, c),
                    "wrong normalized parameter orbit"
                );
                if epsilon = 0 then
                    AssertOrFail(
                        orbit.bases = swap_bases,
                        "D-pattern basis action is not identity/swap"
                    );
                else
                    AssertOrFail(
                        orbit.bases = all_ordered_bases,
                        "Q-pattern basis action is not all GL(2,2)"
                    );
                fi;
            od;
        od;
    od;
od;

Print(
    "PASS|D_action=S2_on_(a,b)_with_c_fixed",
    "|D_orbits=6",
    "|Q_action=GL(2,2)_on_(a+c,b+c)_with_c_fixed",
    "|Q_orbits=4",
    "\n"
);
Print("DONE\n");
QUIT;
