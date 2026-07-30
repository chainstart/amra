# Independent direct audit of every non-powerful cube-generated subgroup
# found in the complete SglPPow order-6561 scan.

if LoadPackage("SglPPow") <> true then
    Error("SglPPow is required");
fi;

candidateIds := [
    1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924,
    1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933,
    1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978,
    1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987,
    2067, 2068, 2071, 2072, 2077, 2078, 2083, 2084, 2087,
    2088, 2093, 2096, 2097, 2100, 2101, 2106, 2127, 2128,
    2131, 2135, 2139, 2143, 2147, 2151, 2155, 2159, 2160
];;

rows := [];;
closedIds := [];;
for id in candidateIds do
    group := SmallGroup(3^8, id);;
    cubeGroup := Agemo(group, 3);;
    cubeDerived := DerivedSubgroup(cubeGroup);;
    cubePowerSubgroup := Agemo(cubeGroup, 3);;
    rawCubes := Set(Elements(group), g -> g^3);;

    if IsAbelian(cubeGroup) then
        Error("candidate cube-generated subgroup is abelian");
    fi;
    if IsPowerfulPGroup(cubeGroup) then
        Error("candidate cube-generated subgroup is powerful");
    fi;
    if IsSubgroup(cubePowerSubgroup, cubeDerived) then
        Error("direct H' not-subset H^3 test failed");
    fi;
    if Length(rawCubes) = Size(cubeGroup) then
        Add(closedIds, id);
    fi;

    Add(rows, [
        PClassPGroup(group),
        NilpotencyClassOfGroup(group),
        Exponent(group),
        Length(rawCubes),
        Size(cubeGroup),
        NilpotencyClassOfGroup(cubeGroup),
        Exponent(cubeGroup),
        Size(cubeDerived),
        Size(cubePowerSubgroup)
    ]);
od;

if Length(Set(candidateIds)) <> 63 then
    Error("candidate list is not a 63-element set");
fi;
if Length(closedIds) <> 0 then
    Error("a Wilson counterexample was found");
fi;

Print(
    "ORDER6561_NONPOWERFUL_CANDIDATES",
    "|count=", Length(candidateIds),
    "|all_nonabelian=true",
    "|all_nonpowerful_native=true",
    "|all_derived_not_in_cube_power=true",
    "|raw_closed=0",
    "\n"
);;
Print("INVARIANT_ROWS_COLLECTED|", Collected(rows), "\n");;
Print("CLOSED_IDS|", closedIds, "\n");;
QUIT;
