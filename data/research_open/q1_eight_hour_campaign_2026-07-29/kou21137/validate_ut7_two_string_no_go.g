# Exact audit for the two-string subgroup of UT(7,3).
#
# The two generators are the length-three Jordan strings on coordinates
# 1,...,4 and 4,...,7.  This script checks the ambient group, its raw cube
# set, the central-monolith obstruction for every normal quotient, and the
# four maximal subgroups (which cover every proper subgroup).

SizeScreen([1000, 40]);;
f := GF(3);;
n := 7;;
x := IdentityMat(n, f);;
y := IdentityMat(n, f);;
for i in [1..3] do
    x[i][i + 1] := One(f);
od;
for i in [4..6] do
    y[i][i + 1] := One(f);
od;

matrix_group := Group(x, y);;
iso := IsomorphismPcGroup(matrix_group);;
group := Image(iso);;
px := Image(iso, x);;
py := Image(iso, y);;
elements := Elements(group);;
cubes := Set(elements, g -> g^3);;
cube_group := Subgroup(group, cubes);;
z := Comm(px^3, py^3);;
derived_cubes := DerivedSubgroup(cube_group);;
centre_group := Centre(group);;

if Size(group) <> 1594323 then
    Error("unexpected order for the two-string group");
fi;
if NilpotencyClassOfGroup(group) <> 6 or Exponent(group) <> 9 then
    Error("unexpected class or exponent");
fi;
if Length(cubes) <> 649 or Size(cube_group) <> 59049 then
    Error("unexpected raw-cube or generated-cube size");
fi;
if Length(cubes) = Size(cube_group) then
    Error("the ambient raw cube set should not be closed");
fi;
if Size(derived_cubes) <> 3 or derived_cubes <> Subgroup(group, [z]) then
    Error("the cube subgroup should have derived subgroup <[x^3,y^3]>");
fi;
if Size(centre_group) <> 3 or centre_group <> Subgroup(group, [z]) then
    Error("the ambient centre should be the commutator witness");
fi;
if IsPowerfulPGroup(cube_group) then
    Error("the generated cube subgroup should be non-powerful");
fi;

Print(
    "UT7_TWO_STRING",
    "|order=", Size(group),
    "|class=", NilpotencyClassOfGroup(group),
    "|exponent=", Exponent(group),
    "|raw_cubes=", Length(cubes),
    "|cube_group=", Size(cube_group),
    "|cube_group_class=", NilpotencyClassOfGroup(cube_group),
    "|cube_group_exponent=", Exponent(cube_group),
    "|cube_derived=", Size(derived_cubes),
    "|centre=", Size(centre_group),
    "|raw_closed=false",
    "|cube_group_powerful=false\n"
);;

# Every non-trivial normal subgroup of a finite p-group meets the centre.
# Since the centre here is <z> of order 3, every non-trivial normal quotient
# kills the complete derived subgroup <z> of the cube-generated subgroup.
# The exhaustive list below is a machine cross-check of that universal
# structural argument.
normal_subgroups := NormalSubgroups(group);;
nontrivial_normals := Filtered(normal_subgroups, subgroup -> Size(subgroup) > 1);;
if not ForAll(nontrivial_normals, subgroup -> z in subgroup) then
    Error("a non-trivial normal subgroup failed to contain z");
fi;
if Length(normal_subgroups) <> 641 then
    Error("unexpected number of normal subgroups");
fi;

Print(
    "NORMAL_QUOTIENTS",
    "|normal_subgroups=", Length(normal_subgroups),
    "|nontrivial=", Length(nontrivial_normals),
    "|all_nontrivial_kill_cube_derived=true",
    "|trivial_quotient_raw_closed=false",
    "|kou_hits=0\n"
);;

# Every proper subgroup lies in a maximal subgroup.  Thus it is enough to
# show that cubes commute in each maximal subgroup: any closed raw cube set
# in a proper subgroup then generates an abelian (hence powerful) subgroup.
maximals := MaximalSubgroups(group);;
if Length(maximals) <> 4 then
    Error("a two-generated 3-group should have four maximal subgroups");
fi;

maximal_rows := [];;
for index in [1..Length(maximals)] do
    maximal := maximals[index];
    maximal_cubes := Set(Elements(maximal), g -> g^3);
    maximal_cube_group := Subgroup(maximal, maximal_cubes);
    row := [
        index,
        Size(maximal),
        Length(maximal_cubes),
        Size(maximal_cube_group),
        Length(maximal_cubes) = Size(maximal_cube_group),
        IsAbelian(maximal_cube_group),
        IsPowerfulPGroup(maximal_cube_group)
    ];
    Add(maximal_rows, row);
    Print(
        "MAXIMAL",
        "|index=", index,
        "|order=", row[2],
        "|raw_cubes=", row[3],
        "|cube_group=", row[4],
        "|raw_closed=", row[5],
        "|cube_group_abelian=", row[6],
        "|cube_group_powerful=", row[7],
        "\n"
    );
od;

if not ForAll(maximal_rows, row -> row[6] and row[7]) then
    Error("a maximal subgroup has nonabelian or non-powerful cube subgroup");
fi;

Print(
    "PROPER_SUBGROUPS",
    "|maximal_subgroups=4",
    "|all_maximal_cube_groups_abelian=true",
    "|all_closed_raw_cube_subgroups_powerful=true",
    "|kou_hits=0\n"
);;
Print("DONE\n");;
QUIT;
