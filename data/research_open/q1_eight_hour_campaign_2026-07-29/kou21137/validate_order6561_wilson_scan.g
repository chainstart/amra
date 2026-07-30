# Complete Wilson-target scan for groups of order 3^8.
#
# Dependency:
#   GAP with SmallGrp and SglPPow 2.4 (or a later compatible release).
#
# A finite 3-group G can be a counterexample to Wilson's question only if
#
#   H = < g^3 : g in G >
#
# is not powerful.  We therefore compute H first without enumerating G.  Only
# for a non-powerful H do we enumerate the raw cube values P_3(G) and test
# whether |P_3(G)| = |H|.  Since P_3(G) is contained in H, equality is
# equivalent to the raw cube values forming a subgroup.
#
# The optional globals AMRA_SCAN_START and AMRA_SCAN_FINISH allow the complete
# catalogue to be split into independently reproducible shards:
#
#   gap -q -c 'AMRA_SCAN_START:=1;; AMRA_SCAN_FINISH:=261686;;
#              Read("validate_order6561_wilson_scan.g");'

if LoadPackage("SglPPow") <> true then
    Error("SglPPow is required");
fi;

catalogueSize := NumberSmallGroups(3^8);;
if catalogueSize <> 1396077 then
    Error("unexpected SglPPow order-6561 catalogue size");
fi;

if IsBound(AMRA_SCAN_START) then
    scanStart := AMRA_SCAN_START;;
else
    scanStart := 1;;
fi;
if IsBound(AMRA_SCAN_FINISH) then
    scanFinish := AMRA_SCAN_FINISH;;
else
    scanFinish := catalogueSize;;
fi;
if scanStart < 1 or scanFinish > catalogueSize or scanStart > scanFinish then
    Error("invalid catalogue range");
fi;

nonabelianAgemoIds := [];;
nonpowerfulAgemoIds := [];;
closedNonpowerfulIds := [];;
started := Runtime();;

for id in [scanStart..scanFinish] do
    group := SmallGroup(3^8, id);;
    cubeGroup := Agemo(group, 3);;

    # Every abelian 3-group is powerful, so this inexpensive test avoids a
    # second subgroup calculation for the overwhelming majority of entries.
    if not IsAbelian(cubeGroup) then
        Add(nonabelianAgemoIds, id);
        if not IsPowerfulPGroup(cubeGroup) then
            Add(nonpowerfulAgemoIds, id);
            rawCubes := Set(Elements(group), g -> g^3);;
            if Length(rawCubes) = Size(cubeGroup) then
                Add(closedNonpowerfulIds, id);
                Print(
                    "WILSON_HIT",
                    "|id=", id,
                    "|pclass=", PClassPGroup(group),
                    "|class=", NilpotencyClassOfGroup(group),
                    "|exponent=", Exponent(group),
                    "|raw_cubes=", Length(rawCubes),
                    "|cube_group=", Size(cubeGroup),
                    "|cube_class=", NilpotencyClassOfGroup(cubeGroup),
                    "|cube_exponent=", Exponent(cubeGroup),
                    "|cube_derived=", Size(DerivedSubgroup(cubeGroup)),
                    "\n"
                );
            fi;
        fi;
    fi;

    if id mod 25000 = 0 then
        Print(
            "PROGRESS",
            "|id=", id,
            "|nonabelian_agemo=", Length(nonabelianAgemoIds),
            "|nonpowerful_agemo=", Length(nonpowerfulAgemoIds),
            "|closed_nonpowerful=", Length(closedNonpowerfulIds),
            "|runtime_ms=", Runtime() - started,
            "\n"
        );
    fi;
od;

Print(
    "ORDER6561_WILSON_SCAN",
    "|range=", scanStart, "..", scanFinish,
    "|groups=", scanFinish - scanStart + 1,
    "|nonabelian_agemo=", Length(nonabelianAgemoIds),
    "|nonpowerful_agemo=", Length(nonpowerfulAgemoIds),
    "|closed_nonpowerful=", Length(closedNonpowerfulIds),
    "|runtime_ms=", Runtime() - started,
    "\n"
);;
Print("NONPOWERFUL_AGEMO_IDS|", nonpowerfulAgemoIds, "\n");;
Print("CLOSED_NONPOWERFUL_IDS|", closedNonpowerfulIds, "\n");;
QUIT;
