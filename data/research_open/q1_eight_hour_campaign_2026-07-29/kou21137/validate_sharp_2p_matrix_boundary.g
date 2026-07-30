# Matrix regression for the class-(2p-1)/class-2p boundary.
#
# For UT_{2p}(F_p), every p-th power has the form I+A^p.  Products of
# two such corrections vanish because A^p B^p lies on superdiagonal at
# least 2p, outside a 2p by 2p matrix.  The explicit pair below checks
# this commuting side.  In UT_{2p+1}(F_p), two length-p Jordan strings
# meeting at one endpoint give noncommuting p-th powers.

SizeScreen([100000, 100000]);;

AssertOrFail := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

CheckBoundary := function(p)
    local field, small_n, large_n, small_identity, large_identity,
          small_x, small_y, large_x, large_y, top_commutator, index;

    field := GF(p);
    small_n := 2 * p;
    large_n := 2 * p + 1;
    small_identity := IdentityMat(small_n, field);
    large_identity := IdentityMat(large_n, field);

    # Two length-p strings in dimension 2p.  Their p-th-power matrix
    # units cannot compose in either order.
    small_x := IdentityMat(small_n, field);
    small_y := IdentityMat(small_n, field);
    for index in [1 .. p] do
        small_x[index][index + 1] := One(field);
    od;
    for index in [p .. 2 * p - 1] do
        small_y[index][index + 1] := One(field);
    od;
    AssertOrFail(
        small_x^(p^2) = small_identity
        and small_y^(p^2) = small_identity,
        "small-boundary elements do not have exponent dividing p^2"
    );
    AssertOrFail(
        small_x^p <> small_identity and small_y^p <> small_identity,
        "small-boundary p-th powers vanished"
    );
    AssertOrFail(
        small_x^p * small_y^p = small_y^p * small_x^p,
        "explicit class-(2p-1) pair does not commute"
    );

    # Two length-p strings meeting at p+1 in dimension 2p+1.
    large_x := IdentityMat(large_n, field);
    large_y := IdentityMat(large_n, field);
    for index in [1 .. p] do
        large_x[index][index + 1] := One(field);
    od;
    for index in [p + 1 .. 2 * p] do
        large_y[index][index + 1] := One(field);
    od;
    AssertOrFail(
        large_x^(p^2) = large_identity
        and large_y^(p^2) = large_identity,
        "large-boundary elements do not have exponent dividing p^2"
    );
    AssertOrFail(
        large_x^p <> large_identity and large_y^p <> large_identity,
        "large-boundary p-th powers vanished"
    );
    AssertOrFail(
        large_x^p * large_y^p <> large_y^p * large_x^p,
        "class-2p witness p-th powers commute"
    );
    top_commutator := Comm(large_x, large_y);
    for index in [1 .. p - 1] do
        top_commutator := Comm(top_commutator, large_x);
    od;
    for index in [1 .. p - 1] do
        top_commutator := Comm(top_commutator, large_y);
    od;
    AssertOrFail(
        top_commutator <> large_identity,
        "weight-2p commutator vanished"
    );

    Print(
        "UT_BOUNDARY|p=", p,
        "|class_below=", 2 * p - 1,
        "|below_pair_commutes=true",
        "|witness_class=", 2 * p,
        "|witness_pair_commutes=false",
        "|top_weight_nontrivial=true\n"
    );
end;;

CheckBoundary(3);
CheckBoundary(5);
Print("DONE\n");
QUIT;
